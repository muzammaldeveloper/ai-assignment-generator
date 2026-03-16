"""
User Marshmallow Schemas.

Handles validation for registration, login, and user serialization.
"""

from __future__ import annotations

from marshmallow import Schema, fields, validate, validates, ValidationError


class UserRegisterSchema(Schema):
    """
    Schema for user registration requests.

    Validates email, name, and password strength.
    """

    name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=150),
        metadata={"description": "User display name"},
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(max=255),
        metadata={"description": "User email address"},
    )
    password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=128),
        load_only=True,
        metadata={"description": "User password (min 8 characters)"},
    )

    @validates("password")
    def validate_password_strength(self, value: str) -> None:
        """
        Ensure password meets minimum strength requirements.

        Rules:
            - At least 8 characters (enforced by Length validator)
            - At least one uppercase letter
            - At least one lowercase letter
            - At least one digit
        """
        if not any(c.isupper() for c in value):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(c.islower() for c in value):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not any(c.isdigit() for c in value):
            raise ValidationError("Password must contain at least one digit.")


class UserLoginSchema(Schema):
    """Schema for user login requests."""

    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


class UserResponseSchema(Schema):
    """Schema for user data in API responses."""

    id = fields.String(dump_only=True)
    name = fields.String()
    email = fields.Email()
    is_active = fields.Boolean()
    created_at = fields.DateTime()