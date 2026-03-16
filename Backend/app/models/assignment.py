"""
Assignment Model.

Core model representing a generated academic assignment.
Tracks full lifecycle from pending → completed/failed.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum

from app.extensions import db


class AssignmentStatus(str, Enum):
    """Assignment generation lifecycle status."""
    PENDING = "pending"
    RESEARCHING = "researching"
    OUTLINING = "outlining"
    GENERATING = "generating"
    IMAGING = "imaging"
    FORMATTING = "formatting"
    COMPLETED = "completed"
    FAILED = "failed"


class AcademicLevel(str, Enum):
    """Supported academic levels."""
    SCHOOL = "school"
    COLLEGE = "college"
    UNIVERSITY = "university"
    RESEARCH = "research"


class CitationStyle(str, Enum):
    """Supported citation formatting styles."""
    APA = "apa"
    MLA = "mla"
    HARVARD = "harvard"
    IEEE = "ieee"


class Assignment(db.Model):
    """
    Assignment database model.

    Stores full metadata, status tracking, generated content paths,
    and relationships to sections, images, and references.

    Attributes:
        id: UUID primary key.
        user_id: Foreign key to owning user.
        topic: Assignment topic string.
        academic_level: School/College/University/Research.
        word_count: Target word count.
        citation_style: APA/MLA/Harvard/IEEE.
        template: Document template name.
        status: Current generation pipeline status.
        research_context: Collected web research text.
        outline_json: JSON outline structure.
        docx_path: Generated DOCX file path.
        pdf_path: Generated PDF file path.
        error_message: Failure details (if status=failed).
        progress_percent: Generation progress (0-100).
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
        completed_at: Completion timestamp.
    """

    __tablename__ = "assignments"

    id: str = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    user_id: str = db.Column(
        db.String(36),
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    topic: str = db.Column(db.String(500), nullable=False)
    academic_level: str = db.Column(
        db.String(20), nullable=False, default=AcademicLevel.UNIVERSITY.value,
    )
    word_count: int = db.Column(db.Integer, nullable=False, default=1500)
    citation_style: str = db.Column(
        db.String(20), nullable=False, default=CitationStyle.APA.value,
    )
    template: str = db.Column(db.String(50), nullable=False, default="professional")
    status: str = db.Column(
        db.String(20),
        nullable=False,
        default=AssignmentStatus.PENDING.value,
        index=True,
    )
    research_context: str = db.Column(db.Text, nullable=True)
    outline_json: str = db.Column(db.Text, nullable=True)
    docx_path: str = db.Column(db.String(500), nullable=True)
    pdf_path: str = db.Column(db.String(500), nullable=True)
    error_message: str = db.Column(db.Text, nullable=True)
    progress_percent: int = db.Column(db.Integer, default=0, nullable=False)
    created_at: datetime = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    completed_at: datetime = db.Column(
        db.DateTime(timezone=True), nullable=True
    )

    # ── Relationships ──
    user = db.relationship("User", back_populates="assignments")
    sections = db.relationship(
        "Section",
        back_populates="assignment",
        lazy="selectin",
        cascade="all, delete-orphan",
        order_by="Section.order",
    )
    images = db.relationship(
        "Image",
        back_populates="assignment",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    references = db.relationship(
        "Reference",
        back_populates="assignment",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def update_status(self, status: AssignmentStatus, progress: int = 0) -> None:
        """
        Update assignment status and progress.

        Args:
            status: New assignment status.
            progress: Progress percentage (0-100).
        """
        self.status = status.value
        self.progress_percent = min(progress, 100)
        if status == AssignmentStatus.COMPLETED:
            self.completed_at = datetime.now(timezone.utc)

    def mark_failed(self, error_message: str) -> None:
        """
        Mark the assignment as failed with error details.

        Args:
            error_message: Description of what went wrong.
        """
        self.status = AssignmentStatus.FAILED.value
        self.error_message = error_message

    def __repr__(self) -> str:
        return f"<Assignment id={self.id} topic='{self.topic[:40]}' status={self.status}>"