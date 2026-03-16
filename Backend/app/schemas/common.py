"""
Common Schema Utilities.

Shared validators and helpers used across multiple schemas.
"""

from __future__ import annotations

from marshmallow import ValidationError


def validate_not_empty(value: str) -> None:
    """Validate that a string is not empty or whitespace-only."""
    if not value or not value.strip():
        raise ValidationError("Field must not be empty or whitespace-only.")


def validate_min_alpha_chars(min_count: int = 3):
    """Factory: validate minimum alphabetic characters."""
    def _validator(value: str) -> None:
        alpha_count = sum(1 for c in value if c.isalpha())
        if alpha_count < min_count:
            raise ValidationError(
                f"Field must contain at least {min_count} alphabetic characters."
            )
    return _validator