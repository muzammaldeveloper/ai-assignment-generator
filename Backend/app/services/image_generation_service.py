"""
Image Generation Service.

Generates contextual images for assignment sections using
Google Gemini API. Includes graceful degradation — if image
generation fails, the assignment continues without images.
"""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import List, Optional

import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

from app.utils.file_helpers import ensure_directory, generate_unique_filename
from app.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class GeneratedImage:
    """Result of a single image generation."""
    section_title: str
    image_path: str
    caption: str
    prompt: str
    success: bool = True
    error: str = ""


class ImageGenerationService:
    """
    Image generation service using Google Gemini.

    Generates educational/academic images for each assignment section.
    Designed for graceful degradation — failures don't break the pipeline.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.0-flash-exp",
        storage_path: str = "storage/images",
    ) -> None:
        genai.configure(api_key=api_key)
        self._model_name = model
        self._model = genai.GenerativeModel(model)
        self._storage_path = storage_path
        ensure_directory(storage_path)
        logger.info("ImageGenerationService initialized | model=%s", model)

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True,
    )
    def _generate_single_image(self, prompt: str) -> Optional[bytes]:
        """
        Generate a single image from a text prompt.

        Args:
            prompt: Image generation prompt.

        Returns:
            Optional[bytes]: Image bytes if successful, None otherwise.
        """
        try:
            response = self._model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    candidate_count=1,
                ),
            )

            # Extract image data from response
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "inline_data") and part.inline_data:
                        return base64.b64decode(part.inline_data.data)

            logger.warning("No image data in Gemini response | prompt='%s'", prompt[:60])
            return None

        except Exception as e:
            logger.error("Image generation failed | prompt='%s' | error=%s", prompt[:60], str(e))
            raise

    def generate_section_images(
        self,
        sections: List[dict],
        assignment_id: str,
    ) -> List[GeneratedImage]:
        """
        Generate images for all assignment sections.

        Uses graceful degradation — if one image fails,
        it continues with the remaining sections.

        Args:
            sections: List of dicts with 'title' and 'image_prompt' keys.
            assignment_id: Parent assignment ID for file naming.

        Returns:
            List[GeneratedImage]: Results for each section (success or failure).
        """
        logger.info(
            "Generating images | assignment=%s | sections=%d",
            assignment_id, len(sections),
        )

        results: List[GeneratedImage] = []

        for idx, section in enumerate(sections):
            prompt = section.get("image_prompt", "")
            title = section.get("title", f"Section {idx + 1}")

            if not prompt:
                logger.info("Skipping image (no prompt) | section='%s'", title)
                continue

            try:
                image_bytes = self._generate_single_image(prompt)

                if image_bytes:
                    # Save image to disk
                    filename = generate_unique_filename("png", prefix=f"img_{assignment_id[:8]}")
                    filepath = os.path.join(self._storage_path, filename)

                    with open(filepath, "wb") as f:
                        f.write(image_bytes)

                    caption = f"Figure {idx + 1}: {title}"

                    results.append(GeneratedImage(
                        section_title=title,
                        image_path=filepath,
                        caption=caption,
                        prompt=prompt,
                        success=True,
                    ))
                    logger.info("Image saved | section='%s' | path=%s", title, filepath)
                else:
                    results.append(GeneratedImage(
                        section_title=title,
                        image_path="",
                        caption="",
                        prompt=prompt,
                        success=False,
                        error="No image data returned",
                    ))

            except Exception as e:
                logger.warning(
                    "Image generation failed (graceful skip) | section='%s' | error=%s",
                    title, str(e),
                )
                results.append(GeneratedImage(
                    section_title=title,
                    image_path="",
                    caption="",
                    prompt=prompt,
                    success=False,
                    error=str(e),
                ))

        success_count = sum(1 for r in results if r.success)
        logger.info(
            "Image generation completed | total=%d | success=%d | failed=%d",
            len(results), success_count, len(results) - success_count,
        )
        return results