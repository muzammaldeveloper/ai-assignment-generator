"""
Image Model.

Represents AI-generated images associated with assignment sections.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.extensions import db


class Image(db.Model):
    """
    Image database model.

    Attributes:
        id: UUID primary key.
        assignment_id: Parent assignment foreign key.
        section_id: Associated section (optional).
        image_url: Path or URL to the generated image.
        caption: Image caption text.
        prompt: The prompt used for generation.
    """

    __tablename__ = "images"

    id: str = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()),
    )
    assignment_id: str = db.Column(
        db.String(36),
        db.ForeignKey("assignments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    section_id: str = db.Column(db.String(36), nullable=True, index=True)
    image_url: str = db.Column(db.String(1000), nullable=False)
    caption: str = db.Column(db.String(500), nullable=True)
    prompt: str = db.Column(db.Text, nullable=True)
    created_at: datetime = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    assignment = db.relationship("Assignment", back_populates="images")

    def __repr__(self) -> str:
        return f"<Image id={self.id} caption='{(self.caption or '')[:30]}'>"