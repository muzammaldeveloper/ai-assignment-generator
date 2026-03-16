"""
Marshmallow Schemas Package.

Data validation, serialization, and deserialization.
"""

from app.schemas.assignment_schema import (
    AssignmentCreateSchema,
    AssignmentListSchema,
    AssignmentResponseSchema,
)
from app.schemas.user_schema import UserRegisterSchema, UserLoginSchema, UserResponseSchema

__all__ = [
    "AssignmentCreateSchema",
    "AssignmentListSchema",
    "AssignmentResponseSchema",
    "UserRegisterSchema",
    "UserLoginSchema",
    "UserResponseSchema",
]