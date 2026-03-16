"""Tests for Document Generation Service."""

from __future__ import annotations

import os
import tempfile

import pytest

from app.services.document_service import DocumentService
from app.services.text_generation_service import GeneratedContent, GeneratedSection


@pytest.fixture
def doc_service():
    """Create a DocumentService with a temp directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield DocumentService(storage_path=tmpdir)


@pytest.fixture
def sample_content():
    """Create sample generated content for testing."""
    return GeneratedContent(
        title="Test Assignment: AI in Healthcare",
        introduction="This is the introduction paragraph for the test assignment.",
        sections=[
            GeneratedSection(
                title="Background",
                content="This section covers the background of AI in healthcare.",
                order=1,
                image_prompt="",
            ),
            GeneratedSection(
                title="Applications",
                content="AI has many applications in modern healthcare systems.",
                order=2,
                image_prompt="",
            ),
        ],
        conclusion="In conclusion, AI has transformed healthcare significantly.",
        references=[
            "Smith, J. (2025). AI in Healthcare. Journal of Medicine, 10(1), 1-15.",
            "Doe, A. (2024). Machine Learning Trends. Tech Review, 5(2), 20-30.",
        ],
    )


class TestDocxGeneration:
    """Tests for DOCX document generation."""

    def test_generate_docx_creates_file(self, doc_service, sample_content):
        """Should create a valid DOCX file."""
        path = doc_service.generate_docx(
            content=sample_content,
            images=[],
            template="professional",
            assignment_id="test-123",
        )

        assert os.path.exists(path)
        assert path.endswith(".docx")
        assert os.path.getsize(path) > 0

    def test_generate_docx_all_templates(self, doc_service, sample_content):
        """Should work with all template styles."""
        for template in ["professional", "academic", "modern", "minimal", "colorful"]:
            path = doc_service.generate_docx(
                content=sample_content,
                images=[],
                template=template,
                assignment_id=f"test-{template}",
            )
            assert os.path.exists(path)


class TestPdfGeneration:
    """Tests for PDF document generation."""

    def test_generate_pdf_creates_file(self, doc_service, sample_content):
        """Should create a valid PDF file."""
        path = doc_service.generate_pdf(
            content=sample_content,
            images=[],
            template="professional",
            assignment_id="test-456",
        )

        assert os.path.exists(path)
        assert path.endswith(".pdf")
        assert os.path.getsize(path) > 0