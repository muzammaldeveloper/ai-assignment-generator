"""
User Model.

Represents registered users who can generate assignments.
Includes password hashing via bcrypt for security.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import bcrypt

from app.extensions import db


class User(db.Model):
    """
    User database model.

    Attributes:
        id: Unique UUID primary key.
        email: Unique user email (indexed for fast lookup).
        password_hash: Bcrypt-hashed password.
        name: Display name.
        is_active: Whether the account is active.
        created_at: Account creation timestamp (UTC).
        updated_at: Last modification timestamp (UTC).
    """

    __tablename__ = "users"

    id: str = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    email: str = db.Column(
        db.String(255), unique=True, nullable=False, index=True
    )
    password_hash: str = db.Column(db.String(512), nullable=False)
    name: str = db.Column(db.String(150), nullable=False)
    is_active: bool = db.Column(db.Boolean, default=True, nullable=False)
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

    # ── Relationships ──
    assignments = db.relationship(
        "Assignment",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def set_password(self, raw_password: str) -> None:
        """
        Hash and store the user's password using bcrypt.

        Args:
            raw_password: The plain-text password to hash.
        """
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(
            raw_password.encode("utf-8"), salt
        ).decode("utf-8")

    def check_password(self, raw_password: str) -> bool:
        """
        Verify a plain-text password against the stored hash.

        Args:
            raw_password: The plain-text password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(
            raw_password.encode("utf-8"),
            self.password_hash.encode("utf-8"),
        )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"