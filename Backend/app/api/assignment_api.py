"""
Assignment API — Generate, List, Detail, Download.

LOCAL MODE: Runs pipeline synchronously (no Redis/Celery needed).
"""

from __future__ import annotations

import os
import threading

from flask import Blueprint, jsonify, request, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db, limiter
from app.models.assignment import Assignment, AssignmentStatus
from app.schemas.assignment_schema import (
    AssignmentCreateSchema,
    AssignmentResponseSchema,
    AssignmentListSchema,
)
from app.utils.logger import get_logger
from app.utils.prompt_guard import guard_prompt

logger = get_logger(__name__)
assignment_bp = Blueprint("assignments", __name__)

_create_schema = AssignmentCreateSchema()
_response_schema = AssignmentResponseSchema()
_list_schema = AssignmentListSchema(many=True)


def _run_pipeline_sync(app, assignment_id: str) -> None:
    """
    Run the AI pipeline in a background thread (local mode).

    This replaces Celery for local development — no Redis needed.
    """
    with app.app_context():
        try:
            from app.services.pipeline_service import PipelineService
            settings = app.config["SETTINGS"]
            pipeline = PipelineService(settings=settings)
            pipeline.execute(assignment_id=assignment_id)
        except Exception as e:
            logger.exception("Pipeline failed | id=%s | error=%s", assignment_id, str(e))
            assignment = db.session.get(Assignment, assignment_id)
            if assignment:
                assignment.mark_failed(str(e))
                db.session.commit()


@assignment_bp.route("/generate", methods=["POST"])
@jwt_required()
@limiter.limit("20/hour")
def generate_assignment():
    """
    Generate a new assignment.

    Starts pipeline in background thread (no Redis needed).

    Request Body:
        {
            "topic": "Artificial Intelligence in Healthcare",
            "academic_level": "university",
            "word_count": 1500,
            "citation_style": "apa",
            "template": "professional"
        }

    Returns:
        202: Assignment queued.
    """
    user_id = get_jwt_identity()
    data = _create_schema.load(request.get_json())

    # Prompt injection check
    guard_prompt(data["topic"])

    # Create assignment record
    assignment = Assignment(
        user_id=user_id,
        topic=data["topic"],
        academic_level=data["academic_level"],
        word_count=data["word_count"],
        citation_style=data["citation_style"],
        template=data["template"],
        status=AssignmentStatus.PENDING.value,
        progress_percent=0,
    )
    db.session.add(assignment)
    db.session.commit()

    # Run in background thread (local mode — no Celery/Redis)
    app = current_app._get_current_object()
    thread = threading.Thread(
        target=_run_pipeline_sync,
        args=(app, assignment.id),
        daemon=True,
    )
    thread.start()

    logger.info("Assignment queued (local) | id=%s | topic='%s'", assignment.id, assignment.topic)

    return jsonify({
        "success": True,
        "message": "Assignment generation started! Check status with GET /assignments/<id>",
        "data": {
            "assignment_id": assignment.id,
            "status": assignment.status,
            "status_url": f"/api/v1/assignments/{assignment.id}",
        },
    }), 202


@assignment_bp.route("", methods=["GET"])
@jwt_required()
def list_assignments():
    """List all assignments (paginated)."""
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 50)
    status_filter = request.args.get("status", None, type=str)

    query = Assignment.query.filter_by(user_id=user_id)
    if status_filter:
        query = query.filter_by(status=status_filter)

    query = query.order_by(Assignment.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "success": True,
        "data": {
            "assignments": _list_schema.dump(pagination.items),
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "total_pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            },
        },
    }), 200


@assignment_bp.route("/<string:assignment_id>", methods=["GET"])
@jwt_required()
def get_assignment(assignment_id: str):
    """Get full assignment details."""
    user_id = get_jwt_identity()
    assignment = db.session.get(Assignment, assignment_id)

    if not assignment:
        return jsonify({"success": False, "message": "Assignment not found."}), 404
    if assignment.user_id != user_id:
        return jsonify({"success": False, "message": "Access denied."}), 403

    return jsonify({
        "success": True,
        "data": _response_schema.dump(assignment),
    }), 200


@assignment_bp.route("/<string:assignment_id>/download", methods=["GET"])
@jwt_required()
def download_assignment(assignment_id: str):
    """Download DOCX or PDF file."""
    user_id = get_jwt_identity()
    assignment = db.session.get(Assignment, assignment_id)

    if not assignment:
        return jsonify({"success": False, "message": "Assignment not found."}), 404
    if assignment.user_id != user_id:
        return jsonify({"success": False, "message": "Access denied."}), 403
    if assignment.status != AssignmentStatus.COMPLETED.value:
        return jsonify({
            "success": False,
            "message": f"Not ready. Status: {assignment.status} ({assignment.progress_percent}%)",
        }), 400

    file_format = request.args.get("format", "docx", type=str).lower()

    if file_format == "pdf":
        filepath = assignment.pdf_path
        mimetype = "application/pdf"
        name = f"{assignment.topic[:50]}.pdf"
    else:
        filepath = assignment.docx_path
        mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        name = f"{assignment.topic[:50]}.docx"

    if not filepath:
        return jsonify({"success": False, "message": f"{file_format.upper()} file not available."}), 404

    # Resolve to absolute path from project root
    abs_path = os.path.abspath(filepath)
    if not os.path.exists(abs_path):
        logger.error("Download file missing | path=%s | abs=%s", filepath, abs_path)
        return jsonify({"success": False, "message": f"{file_format.upper()} file not found on disk."}), 404

    logger.info("Download | id=%s | format=%s | path=%s", assignment_id, file_format, abs_path)

    return send_file(abs_path, mimetype=mimetype, as_attachment=True, download_name=name)


@assignment_bp.route("/<string:assignment_id>/sections/<string:section_id>", methods=["PATCH"])
@jwt_required()
def update_section(assignment_id: str, section_id: str):
    """Update a section's content after generation."""
    user_id = get_jwt_identity()
    assignment = db.session.get(Assignment, assignment_id)

    if not assignment:
        return jsonify({"success": False, "message": "Assignment not found."}), 404
    if assignment.user_id != user_id:
        return jsonify({"success": False, "message": "Access denied."}), 403

    from app.models.section import Section
    import bleach

    section = db.session.get(Section, section_id)
    if not section or section.assignment_id != assignment_id:
        return jsonify({"success": False, "message": "Section not found."}), 404

    data = request.get_json() or {}

    if "content" in data:
        section.content = bleach.clean(str(data["content"]), tags=[], strip=True)
    if "title" in data:
        section.title = bleach.clean(str(data["title"])[:300], tags=[], strip=True)

    db.session.commit()
    logger.info("Section updated | assignment=%s | section=%s", assignment_id, section_id)

    return jsonify({"success": True, "message": "Section updated successfully."}), 200


@assignment_bp.route("/<string:assignment_id>/regenerate-docs", methods=["POST"])
@jwt_required()
def regenerate_documents(assignment_id: str):
    """Regenerate DOCX and PDF after section edits."""
    user_id = get_jwt_identity()
    assignment = db.session.get(Assignment, assignment_id)

    if not assignment:
        return jsonify({"success": False, "message": "Assignment not found."}), 404
    if assignment.user_id != user_id:
        return jsonify({"success": False, "message": "Access denied."}), 403
    if assignment.status != AssignmentStatus.COMPLETED.value:
        return jsonify({"success": False, "message": "Assignment not completed yet."}), 400

    try:
        from app.services.text_generation_service import GeneratedContent, GeneratedSection
        from app.services.image_generation_service import GeneratedImage
        from app.services.document_service import DocumentService

        settings = current_app.config["SETTINGS"]

        sections = sorted(assignment.sections, key=lambda s: s.order)
        intro = ""
        conclusion = ""
        body_sections = []

        for sec in sections:
            if sec.title.lower() == "introduction":
                intro = sec.content
            elif sec.title.lower() == "conclusion":
                conclusion = sec.content
            else:
                body_sections.append(GeneratedSection(
                    title=sec.title,
                    content=sec.content,
                    order=sec.order,
                    image_prompt=sec.image_prompt or "",
                ))

        refs = [r.citation for r in assignment.references]

        content = GeneratedContent(
            title=assignment.topic,
            introduction=intro,
            sections=body_sections,
            conclusion=conclusion,
            references=refs,
        )

        # Gather existing images
        images = [
            GeneratedImage(
                section_title=img.caption.split(": ", 1)[-1] if ": " in img.caption else "",
                image_path=os.path.abspath(img.image_url) if img.image_url else "",
                caption=img.caption,
                prompt=img.prompt or "",
                success=bool(img.image_url and os.path.exists(os.path.abspath(img.image_url))),
            )
            for img in assignment.images
        ]

        doc_gen = DocumentService(
            storage_path=os.path.abspath(f"{settings.storage_local_path}/documents"),
        )

        docx_path = doc_gen.generate_docx(
            content=content, images=images,
            template=assignment.template, assignment_id=assignment.id,
        )
        pdf_path = doc_gen.generate_pdf(
            content=content, images=images,
            template=assignment.template, assignment_id=assignment.id,
        )

        assignment.docx_path = docx_path
        assignment.pdf_path = pdf_path
        db.session.commit()

        logger.info("Documents regenerated | id=%s", assignment_id)
        return jsonify({"success": True, "message": "Documents regenerated successfully."}), 200

    except Exception as e:
        logger.exception("Document regeneration failed | id=%s", assignment_id)
        return jsonify({"success": False, "message": f"Regeneration failed: {str(e)}"}), 500