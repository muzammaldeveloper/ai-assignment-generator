"""
Assignment Outline Generation Service.

Uses OpenAI to generate a structured assignment outline
based on topic, academic level, word count, and research context.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import List

from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential

from app.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class OutlineSection:
    """Single section in the assignment outline."""
    title: str
    description: str
    key_points: List[str] = field(default_factory=list)
    include_image: bool = True
    image_prompt_hint: str = ""


@dataclass
class AssignmentOutline:
    """Complete assignment outline."""
    title: str
    abstract: str
    sections: List[OutlineSection] = field(default_factory=list)
    conclusion_points: List[str] = field(default_factory=list)


class OutlineService:
    """
    Generates structured assignment outlines using OpenAI.

    The outline drives the entire content generation pipeline —
    it defines sections, key points, and image placement.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "llama-3.3-70b-versatile",
        temperature: float = 0.7,
    ) -> None:
        self._client = Groq(api_key=api_key)
        self._model = model
        self._temperature = temperature
        logger.info("OutlineService initialized | model=%s", model)

    def _build_system_prompt(self, academic_level: str) -> str:
        """Build the system prompt for outline generation."""
        return f"""You are an expert academic assignment outline generator.
You generate structured assignment outlines at the {academic_level} level.

RULES:
1. Generate a clear, logical outline with 5-8 main sections.
2. Each section must have a title, description, 3-5 key points, and an image prompt hint.
3. The outline must flow logically: Introduction → Background → Core Content → Applications → Conclusion.
4. Output ONLY valid JSON matching this exact schema:

{{
    "title": "Assignment Title",
    "abstract": "Brief 2-3 sentence abstract",
    "sections": [
        {{
            "title": "Section Title",
            "description": "What this section covers",
            "key_points": ["point1", "point2", "point3"],
            "include_image": true,
            "image_prompt_hint": "Description for image generation"
        }}
    ],
    "conclusion_points": ["conclusion point 1", "conclusion point 2"]
}}

Do NOT include Introduction or Conclusion in the sections array — they are handled separately.
Output ONLY the JSON, no explanations."""

    def _build_user_prompt(
        self, topic: str, word_count: int, research_summary: str,
    ) -> str:
        """Build the user prompt with topic and research context."""
        return f"""Generate an assignment outline for the following:

TOPIC: {topic}
TARGET WORD COUNT: {word_count}
RESEARCH CONTEXT:
{research_summary[:4000]}

Generate a comprehensive, well-structured outline."""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    def generate_outline(
        self,
        topic: str,
        academic_level: str,
        word_count: int,
        research_summary: str,
    ) -> AssignmentOutline:
        """
        Generate a structured assignment outline.

        Args:
            topic: Assignment topic.
            academic_level: Academic level.
            word_count: Target word count.
            research_summary: Compiled research text.

        Returns:
            AssignmentOutline: Parsed outline structure.

        Raises:
            RuntimeError: If generation or parsing fails.
        """
        logger.info(
            "Generating outline | topic='%s' | level=%s | words=%d",
            topic, academic_level, word_count,
        )

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                temperature=self._temperature,
                max_tokens=2048,
                messages=[
                    {"role": "system", "content": self._build_system_prompt(academic_level)},
                    {"role": "user", "content": self._build_user_prompt(topic, word_count, research_summary)},
                ],
                response_format={"type": "json_object"},
            )

            raw_json = response.choices[0].message.content.strip()
            data = json.loads(raw_json)

            outline = AssignmentOutline(
                title=data.get("title", topic),
                abstract=data.get("abstract", ""),
                sections=[
                    OutlineSection(
                        title=s.get("title", ""),
                        description=s.get("description", ""),
                        key_points=s.get("key_points", []),
                        include_image=s.get("include_image", True),
                        image_prompt_hint=s.get("image_prompt_hint", ""),
                    )
                    for s in data.get("sections", [])
                ],
                conclusion_points=data.get("conclusion_points", []),
            )

            logger.info(
                "Outline generated | title='%s' | sections=%d",
                outline.title, len(outline.sections),
            )
            return outline

        except json.JSONDecodeError as e:
            logger.error("Outline JSON parse failed | error=%s", str(e))
            raise RuntimeError(f"Failed to parse outline JSON: {e}") from e
        except Exception as e:
            logger.error("Outline generation failed | error=%s", str(e))
            raise RuntimeError(f"Outline generation failed: {e}") from e