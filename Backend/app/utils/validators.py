"""
Input Validation & Sanitization Utilities.

Provides functions to clean and validate user inputs
before they reach the AI pipeline.
"""

from __future__ import annotations

import re

import bleach


def sanitize_text(text: str) -> str:
    """
    Remove HTML tags, normalize whitespace, and strip the text.

    Args:
        text: Raw user input.

    Returns:
        str: Sanitized text.
    """
    cleaned = bleach.clean(text, tags=[], strip=True)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def sanitize_topic(topic: str) -> str:
    """
    Sanitize an assignment topic — remove dangerous content
    while preserving meaningful academic text.

    Args:
        topic: Raw topic string.

    Returns:
        str: Cleaned topic string.

    Raises:
        ValueError: If topic is empty after cleaning.
    """
    cleaned = sanitize_text(topic)
    # Allow letters, numbers, spaces, hyphens, apostrophes, commas, periods, parens, &, /
    cleaned = re.sub(r"[^\w\s\-',.\(\)&/:]", "", cleaned)

    if len(cleaned) < 3:
        raise ValueError("Topic is too short after sanitization.")
    if len(cleaned) > 500:
        cleaned = cleaned[:500]

    return cleaned