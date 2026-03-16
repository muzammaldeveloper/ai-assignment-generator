"""
AI Assignment Generation Pipeline Service.

Orchestrates the complete assignment generation workflow:
Research → Outline → Content → Images → Documents

This is the main brain of the system that ties all services together.
"""

from __future__ import annotations

import json
from typing import Optional

from config.settings import Settings
from app.extensions import db
from app.models.assignment import Assignment, AssignmentStatus
from app.models.section import Section
from app.models.image import Image
from app.models.reference import Reference
from app.services.research_service import ResearchService
from app.services.outline_service import OutlineService
from app.services.text_generation_service import TextGenerationService
from app.services.image_generation_service import ImageGenerationService
from app.services.document_service import DocumentService
from app.utils.logger import get_logger
from app.utils.prompt_guard import guard_prompt
from app.utils.validators import sanitize_topic

logger = get_logger(__name__)


class PipelineService:
    """
    Orchestrates the complete AI assignment generation pipeline.

    Pipeline Steps:
        1. Input validation & sanitization
        2. Web research via Tavily
        3. Outline generation via OpenAI
        4. Section content generation via OpenAI
        5. Image generation via Google Gemini (graceful degradation)
        6. DOCX document generation
        7. PDF document generation
        8. Database persistence

    Each step updates the assignment status and progress for
    real-time tracking by the client.
    """

    def __init__(self, settings: Settings) -> None:
        """
        Initialize all sub-services from settings.

        Args:
            settings: Application settings with API keys and config.
        """
        self._settings = settings

        self._research = ResearchService(
            api_key=settings.tavily_api_key,
            max_results=settings.tavily_max_results,
        )
        self._outline = OutlineService(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=settings.groq_temperature,
        )
        self._text_gen = TextGenerationService(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            max_tokens=settings.groq_max_tokens,
            temperature=settings.groq_temperature,
        )
        self._image_gen = ImageGenerationService(
            api_key=settings.gemini_api_key,
            model=settings.gemini_model,
            storage_path=f"{settings.storage_local_path}/images",
        )
        self._doc_gen = DocumentService(
            storage_path=f"{settings.storage_local_path}/documents",
        )

        logger.info("PipelineService initialized with all sub-services")

    def execute(self, assignment_id: str) -> None:
        """
        Execute the full assignment generation pipeline.

        This is the main entry point called by Celery tasks.
        Updates assignment status/progress at each step.

        Args:
            assignment_id: UUID of the assignment to generate.

        Raises:
            RuntimeError: If any critical step fails.
        """
        assignment = db.session.get(Assignment, assignment_id)
        if not assignment:
            logger.error("Assignment not found | id=%s", assignment_id)
            raise RuntimeError(f"Assignment not found: {assignment_id}")

        logger.info(
            "Pipeline started | id=%s | topic='%s' | level=%s | words=%d",
            assignment.id, assignment.topic,
            assignment.academic_level, assignment.word_count,
        )

        try:
            # ── Step 1: Validate & Sanitize ──
            clean_topic = sanitize_topic(assignment.topic)
            guard_prompt(clean_topic)

            # ── Step 2: Web Research ──
            assignment.update_status(AssignmentStatus.RESEARCHING, progress=10)
            db.session.commit()

            research_context = self._research.research_topic(
                topic=clean_topic,
                academic_level=assignment.academic_level,
            )
            assignment.research_context = research_context.summary
            db.session.commit()

            logger.info("Step 2/7 DONE: Research | results=%d", len(research_context.results))

            # ── Step 3: Generate Outline ──
            assignment.update_status(AssignmentStatus.OUTLINING, progress=25)
            db.session.commit()

            outline = self._outline.generate_outline(
                topic=clean_topic,
                academic_level=assignment.academic_level,
                word_count=assignment.word_count,
                research_summary=research_context.summary,
            )
            assignment.outline_json = json.dumps({
                "title": outline.title,
                "abstract": outline.abstract,
                "sections": [
                    {"title": s.title, "description": s.description}
                    for s in outline.sections
                ],
            })
            db.session.commit()

            logger.info("Step 3/7 DONE: Outline | sections=%d", len(outline.sections))

            # ── Step 4: Generate Content ──
            assignment.update_status(AssignmentStatus.GENERATING, progress=40)
            db.session.commit()

            source_urls = [r.url for r in research_context.results if r.url]
            content = self._text_gen.generate_full_content(
                outline=outline,
                topic=clean_topic,
                academic_level=assignment.academic_level,
                word_count=assignment.word_count,
                citation_style=assignment.citation_style,
                research_context=research_context.summary,
                source_urls=source_urls,
            )

            # Save sections to database
            # Introduction (order=0)
            db.session.add(Section(
                assignment_id=assignment.id,
                title="Introduction",
                content=content.introduction,
                order=0,
            ))

            for section in content.sections:
                db.session.add(Section(
                    assignment_id=assignment.id,
                    title=section.title,
                    content=section.content,
                    order=section.order,
                    image_prompt=section.image_prompt,
                ))

            # Conclusion
            db.session.add(Section(
                assignment_id=assignment.id,
                title="Conclusion",
                content=content.conclusion,
                order=len(content.sections) + 1,
            ))

            # References
            for ref_text in content.references:
                db.session.add(Reference(
                    assignment_id=assignment.id,
                    citation=ref_text,
                ))

            db.session.commit()

            logger.info("Step 4/7 DONE: Content | sections=%d | refs=%d",
                        len(content.sections), len(content.references))

            # ── Step 5: Generate Images (Graceful) ──
            assignment.update_status(AssignmentStatus.IMAGING, progress=60)
            db.session.commit()

            image_requests = [
                {"title": s.title, "image_prompt": s.image_prompt}
                for s in content.sections
                if s.image_prompt
            ]

            generated_images = self._image_gen.generate_section_images(
                sections=image_requests,
                assignment_id=assignment.id,
            )

            # Save successful images to database
            for img in generated_images:
                if img.success:
                    db.session.add(Image(
                        assignment_id=assignment.id,
                        image_url=img.image_path,
                        caption=img.caption,
                        prompt=img.prompt,
                    ))
            db.session.commit()

            success_images = [img for img in generated_images if img.success]
            logger.info("Step 5/7 DONE: Images | success=%d / %d",
                        len(success_images), len(generated_images))

            # ── Step 6: Generate DOCX ──
            assignment.update_status(AssignmentStatus.FORMATTING, progress=80)
            db.session.commit()

            docx_path = self._doc_gen.generate_docx(
                content=content,
                images=generated_images,
                template=assignment.template,
                assignment_id=assignment.id,
            )
            assignment.docx_path = docx_path

            logger.info("Step 6/7 DONE: DOCX | path=%s", docx_path)

            # ── Step 7: Generate PDF ──
            pdf_path = self._doc_gen.generate_pdf(
                content=content,
                images=generated_images,
                template=assignment.template,
                assignment_id=assignment.id,
            )
            assignment.pdf_path = pdf_path

            logger.info("Step 7/7 DONE: PDF | path=%s", pdf_path)

            # ── Mark Completed ──
            assignment.update_status(AssignmentStatus.COMPLETED, progress=100)
            db.session.commit()

            logger.info(
                "✅ Pipeline COMPLETED | id=%s | topic='%s'",
                assignment.id, assignment.topic,
            )

        except Exception as e:
            logger.exception(
                "❌ Pipeline FAILED | id=%s | error=%s",
                assignment.id, str(e),
            )
            assignment.mark_failed(str(e))
            db.session.commit()
            raise