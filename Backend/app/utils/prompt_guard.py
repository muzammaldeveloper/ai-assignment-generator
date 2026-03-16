"""
Prompt Injection Prevention.

Detects and blocks common prompt injection patterns
to protect AI services from manipulation attacks.
"""

from __future__ import annotations

import re
from typing import List

from app.utils.logger import get_logger

logger = get_logger(__name__)

# ── Known Injection Patterns ──
INJECTION_PATTERNS: List[str] = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?above\s+instructions",
    r"disregard\s+(all\s+)?previous",
    r"forget\s+(all\s+)?previous",
    r"you\s+are\s+now\s+a",
    r"act\s+as\s+if\s+you\s+are",
    r"pretend\s+you\s+are",
    r"system\s*:\s*",
    r"<\|im_start\|>",
    r"<\|im_end\|>",
    r"\[INST\]",
    r"\[/INST\]",
    r"```\s*system",
    r"override\s+instructions",
    r"new\s+instructions?\s*:",
    r"do\s+not\s+follow\s+previous",
    r"jailbreak",
    r"DAN\s+mode",
    r"developer\s+mode",
    r"sudo\s+mode",
    r"bypass\s+(all\s+)?restrictions",
]

_COMPILED_PATTERNS = [
    re.compile(pattern, re.IGNORECASE) for pattern in INJECTION_PATTERNS
]


def detect_prompt_injection(text: str) -> bool:
    """
    Scan text for known prompt injection patterns.

    Args:
        text: User input to check.

    Returns:
        bool: True if injection detected, False otherwise.
    """
    for pattern in _COMPILED_PATTERNS:
        if pattern.search(text):
            logger.warning(
                "Prompt injection detected | pattern=%s | text_preview=%s",
                pattern.pattern,
                text[:100],
            )
            return True
    return False


def guard_prompt(text: str) -> str:
    """
    Validate text and raise error if injection detected.

    Args:
        text: User input to validate.

    Returns:
        str: Original text if safe.

    Raises:
        ValueError: If injection detected.
    """
    if detect_prompt_injection(text):
        raise ValueError(
            "Input rejected: potential prompt injection detected. "
            "Please provide a valid academic topic."
        )
    return text