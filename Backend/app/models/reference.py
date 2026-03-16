"""
Reference Model.

Represents academic citations and source references.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.extensions import db


class Reference(db.Model):
    """
    Reference database model.

    Attributes:
        id: UUID primary key.
        assignment_id: Parent assignment foreign key.
        citation: Formatted citation text.
        source_url: Original source URL.
        title: Source document title.
    """

    __tablename__ = "references"

    id: str = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()),
    )
    assignment_id: str = db.Column(
        db.String(36),
        db.ForeignKey("assignments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    citation: str = db.Column(db.Text, nullable=False)
    source_url: str = db.Column(db.String(1000), nullable=True)
    title: str = db.Column(db.String(500), nullable=True)
    created_at: datetime = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    assignment = db.relationship("Assignment", back_populates="references")

    def __repr__(self) -> str:
        return f"<Reference id={self.id} title='{(self.title or '')[:30]}'>"