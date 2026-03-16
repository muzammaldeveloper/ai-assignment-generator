"""
Section Model.

Represents individual content sections within an assignment.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.extensions import db


class Section(db.Model):
    """
    Section database model.

    Attributes:
        id: UUID primary key.
        assignment_id: Parent assignment foreign key.
        title: Section heading.
        content: Section body text.
        order: Display order (ascending).
        image_prompt: Prompt used for image generation.
    """

    __tablename__ = "sections"

    id: str = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()),
    )
    assignment_id: str = db.Column(
        db.String(36),
        db.ForeignKey("assignments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: str = db.Column(db.String(300), nullable=False)
    content: str = db.Column(db.Text, nullable=False)
    order: int = db.Column(db.Integer, nullable=False, default=0)
    image_prompt: str = db.Column(db.Text, nullable=True)
    created_at: datetime = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    assignment = db.relationship("Assignment", back_populates="sections")

    def __repr__(self) -> str:
        return f"<Section id={self.id} title='{self.title[:30]}' order={self.order}>"