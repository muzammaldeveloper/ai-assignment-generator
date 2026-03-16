"""
Assignment Marshmallow Schemas.

Input validation for assignment creation and serialization for responses.
Includes nested section, image, and reference schemas.
"""

from __future__ import annotations

from marshmallow import Schema, fields, validate, validates, ValidationError, post_load

from app.models.assignment import AcademicLevel, CitationStyle
from app.schemas.common import validate_not_empty, validate_min_alpha_chars


# ── Valid Enum Values ──
VALID_ACADEMIC_LEVELS = [level.value for level in AcademicLevel]
VALID_CITATION_STYLES = [style.value for style in CitationStyle]
VALID_WORD_COUNTS = [800, 1000, 1200, 1500, 2000, 3000, 5000]
VALID_TEMPLATES = ["professional", "academic", "modern", "minimal", "colorful"]


class AssignmentCreateSchema(Schema):
    """
    Schema for validating assignment creation requests.

    Example payload:
        {
            "topic": "Artificial Intelligence in Healthcare",
            "academic_level": "university",
            "word_count": 1500,
            "citation_style": "apa",
            "template": "professional"
        }
    """

    topic = fields.String(
        required=True,
        validate=[
            validate.Length(min=3, max=500),
            validate_not_empty,
            validate_min_alpha_chars(3),
        ],
    )
    academic_level = fields.String(
        required=True,
        validate=validate.OneOf(VALID_ACADEMIC_LEVELS),
    )
    word_count = fields.Integer(
        required=True,
        validate=validate.OneOf(VALID_WORD_COUNTS),
    )
    citation_style = fields.String(
        required=True,
        validate=validate.OneOf(VALID_CITATION_STYLES),
    )
    template = fields.String(
        load_default="professional",
        validate=validate.OneOf(VALID_TEMPLATES),
    )

    @post_load
    def normalize_data(self, data: dict, **kwargs) -> dict:
        """Normalize and clean all input fields."""
        data["topic"] = data["topic"].strip()
        data["academic_level"] = data["academic_level"].lower()
        data["citation_style"] = data["citation_style"].lower()
        data["template"] = data["template"].lower()
        return data


class SectionResponseSchema(Schema):
    """Nested schema for section data."""
    id = fields.String(dump_only=True)
    title = fields.String()
    content = fields.String()
    order = fields.Integer()
    image_prompt = fields.String()


class ImageResponseSchema(Schema):
    """Nested schema for image data."""
    id = fields.String(dump_only=True)
    image_url = fields.String()
    caption = fields.String()


class ReferenceResponseSchema(Schema):
    """Nested schema for reference data."""
    id = fields.String(dump_only=True)
    citation = fields.String()
    source_url = fields.String()
    title = fields.String()


class AssignmentResponseSchema(Schema):
    """
    Full assignment response schema with all nested data.

    Used for single assignment detail endpoints.
    """
    id = fields.String(dump_only=True)
    topic = fields.String()
    academic_level = fields.String()
    word_count = fields.Integer()
    citation_style = fields.String()
    template = fields.String()
    status = fields.String()
    progress_percent = fields.Integer()
    error_message = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    completed_at = fields.DateTime()
    sections = fields.List(fields.Nested(SectionResponseSchema))
    images = fields.List(fields.Nested(ImageResponseSchema))
    references = fields.List(fields.Nested(ReferenceResponseSchema))


class AssignmentListSchema(Schema):
    """
    Lightweight assignment schema for list endpoints.

    Excludes heavy nested data for performance.
    """
    id = fields.String(dump_only=True)
    topic = fields.String()
    academic_level = fields.String()
    word_count = fields.Integer()
    status = fields.String()
    progress_percent = fields.Integer()
    created_at = fields.DateTime()
    completed_at = fields.DateTime()