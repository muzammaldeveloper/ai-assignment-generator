"""
Text Generation Service.

Uses OpenAI to generate section content for each part
of the assignment outline. Includes citation generation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential

from app.services.outline_service import AssignmentOutline, OutlineSection
from app.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class GeneratedSection:
    """A single generated section with content and image prompt."""
    title: str
    content: str
    order: int
    image_prompt: str


@dataclass
class GeneratedContent:
    """Complete generated assignment content."""
    title: str
    introduction: str
    sections: List[GeneratedSection]
    conclusion: str
    references: List[str]


class TextGenerationService:
    """
    Generates full assignment text content from an outline.

    Each section is generated individually with proper academic
    tone, citation style, and research-backed content.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "llama-3.3-70b-versatile",
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> None:
        self._client = Groq(api_key=api_key)
        self._model = model
        self._max_tokens = max_tokens
        self._temperature = temperature
        logger.info("TextGenerationService initialized | model=%s", model)

    def _build_section_prompt(
        self,
        section: OutlineSection,
        topic: str,
        academic_level: str,
        citation_style: str,
        word_target: int,
        research_context: str,
    ) -> str:
        """Build prompt for generating a single section."""
        return f"""Write the "{section.title}" section for an academic assignment.

TOPIC: {topic}
ACADEMIC LEVEL: {academic_level}
CITATION STYLE: {citation_style}
TARGET WORDS FOR THIS SECTION: approximately {word_target} words

SECTION DESCRIPTION: {section.description}
KEY POINTS TO COVER:
{chr(10).join(f"- {kp}" for kp in section.key_points)}

RESEARCH CONTEXT:
{research_context[:3000]}

RULES:
1. Write in formal academic tone appropriate for {academic_level} level.
2. Use {citation_style} citation format for any references.
3. Include specific facts, data, and examples from the research context.
4. Use clear paragraph breaks.
5. Do NOT include the section title in your response — just the body text.
6. Write approximately {word_target} words.

Write the section content now:"""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    def _generate_single_section(
        self,
        section: OutlineSection,
        topic: str,
        academic_level: str,
        citation_style: str,
        word_target: int,
        research_context: str,
    ) -> str:
        """Generate content for a single section with retry."""
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"You are an expert academic writer at the {academic_level} level. "
                            f"Write clear, well-structured, factual content. "
                            f"Use {citation_style} citation style."
                        ),
                    },
                    {
                        "role": "user",
                        "content": self._build_section_prompt(
                            section, topic, academic_level,
                            citation_style, word_target, research_context,
                        ),
                    },
                ],
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(
                "Section generation failed | title='%s' | error=%s",
                section.title, str(e),
            )
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    def _generate_introduction(
        self, outline: AssignmentOutline, academic_level: str, word_target: int,
    ) -> str:
        """Generate the Introduction section."""
        section_titles = ", ".join(s.title for s in outline.sections)
        response = self._client.chat.completions.create(
            model=self._model,
            temperature=self._temperature,
            max_tokens=1024,
            messages=[
                {
                    "role": "system",
                    "content": f"You are an expert academic writer at the {academic_level} level.",
                },
                {
                    "role": "user",
                    "content": f"""Write an Introduction for an academic assignment.

TITLE: {outline.title}
ABSTRACT: {outline.abstract}
SECTIONS COVERED: {section_titles}
TARGET WORDS: {word_target}

Write a compelling introduction that:
1. Introduces the topic and its importance
2. Provides background context
3. States the purpose of the assignment
4. Briefly outlines what sections will cover""",
                },
            ],
        )
        return response.choices[0].message.content.strip()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    def _generate_conclusion(
        self, outline: AssignmentOutline, academic_level: str, word_target: int,
    ) -> str:
        """Generate the Conclusion section."""
        points = "\n".join(f"- {p}" for p in outline.conclusion_points)
        response = self._client.chat.completions.create(
            model=self._model,
            temperature=self._temperature,
            max_tokens=1024,
            messages=[
                {
                    "role": "system",
                    "content": f"You are an expert academic writer at the {academic_level} level.",
                },
                {
                    "role": "user",
                    "content": f"""Write a Conclusion for an academic assignment.

TITLE: {outline.title}
KEY CONCLUSION POINTS:
{points}
TARGET WORDS: {word_target}

Summarize key findings, restate importance, and suggest future directions.""",
                },
            ],
        )
        return response.choices[0].message.content.strip()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    def _generate_references(
        self,
        topic: str,
        citation_style: str,
        source_urls: List[str],
    ) -> List[str]:
        """Generate formatted references from source URLs."""
        urls_text = "\n".join(f"- {url}" for url in source_urls[:10])
        response = self._client.chat.completions.create(
            model=self._model,
            temperature=0.3,
            max_tokens=1024,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a citation formatting expert. Use {citation_style} style.",
                },
                {
                    "role": "user",
                    "content": f"""Generate formatted {citation_style} references for this assignment.

TOPIC: {topic}
SOURCE URLS:
{urls_text}

Generate 5-8 properly formatted {citation_style} references.
Output each reference on a new line, numbered.
Include both the provided URLs and any commonly cited academic sources for this topic.""",
                },
            ],
        )

        raw = response.choices[0].message.content.strip()
        references = [line.strip() for line in raw.split("\n") if line.strip()]
        return references

    def generate_full_content(
        self,
        outline: AssignmentOutline,
        topic: str,
        academic_level: str,
        word_count: int,
        citation_style: str,
        research_context: str,
        source_urls: List[str],
    ) -> GeneratedContent:
        """
        Generate complete assignment content from an outline.

        Generates Introduction, all body sections, Conclusion,
        and formatted References.

        Args:
            outline: Structured assignment outline.
            topic: Assignment topic.
            academic_level: Academic level.
            word_count: Total target word count.
            citation_style: Citation formatting style.
            research_context: Research summary text.
            source_urls: List of source URLs from research.

        Returns:
            GeneratedContent: Complete generated assignment.
        """
        logger.info(
            "Generating full content | topic='%s' | sections=%d | words=%d",
            topic, len(outline.sections), word_count,
        )

        # Calculate word distribution
        num_sections = len(outline.sections) + 2  # +intro +conclusion
        intro_words = int(word_count * 0.12)
        conclusion_words = int(word_count * 0.10)
        body_words = word_count - intro_words - conclusion_words
        per_section_words = body_words // max(len(outline.sections), 1)

        # Generate Introduction
        logger.info("Generating Introduction...")
        introduction = self._generate_introduction(outline, academic_level, intro_words)

        # Generate Body Sections
        sections: List[GeneratedSection] = []
        for idx, section_outline in enumerate(outline.sections):
            logger.info("Generating section %d/%d: '%s'", idx + 1, len(outline.sections), section_outline.title)
            content = self._generate_single_section(
                section=section_outline,
                topic=topic,
                academic_level=academic_level,
                citation_style=citation_style,
                word_target=per_section_words,
                research_context=research_context,
            )

            # Build image prompt from hint
            image_prompt = (
                f"Professional academic illustration: {section_outline.image_prompt_hint}. "
                f"Topic: {topic}. Clean, modern, educational style."
            )

            sections.append(GeneratedSection(
                title=section_outline.title,
                content=content,
                order=idx + 1,
                image_prompt=image_prompt if section_outline.include_image else "",
            ))

        # Generate Conclusion
        logger.info("Generating Conclusion...")
        conclusion = self._generate_conclusion(outline, academic_level, conclusion_words)

        # Generate References
        logger.info("Generating References...")
        references = self._generate_references(topic, citation_style, source_urls)

        total_words = (
            len(introduction.split())
            + sum(len(s.content.split()) for s in sections)
            + len(conclusion.split())
        )
        logger.info("Content generation completed | total_words≈%d", total_words)

        return GeneratedContent(
            title=outline.title,
            introduction=introduction,
            sections=sections,
            conclusion=conclusion,
            references=references,
        )