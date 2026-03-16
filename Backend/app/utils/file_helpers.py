"""
File I/O Helper Utilities.

Provides functions for file storage, path management,
unique filename generation, and cleanup.
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Optional

from app.utils.logger import get_logger

logger = get_logger(__name__)


def ensure_directory(directory: str) -> Path:
    """Ensure a directory exists, creating it if needed."""
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_unique_filename(extension: str, prefix: str = "assignment") -> str:
    """Generate a unique filename: prefix_uuid12.extension"""
    unique_id = uuid.uuid4().hex[:12]
    return f"{prefix}_{unique_id}.{extension}"


def get_storage_path(
    base_dir: str,
    subdirectory: str,
    filename: Optional[str] = None,
) -> str:
    """Construct full storage path, ensuring the directory exists."""
    directory = ensure_directory(os.path.join(base_dir, subdirectory))
    if filename:
        return str(directory / filename)
    return str(directory)


def cleanup_file(filepath: str) -> bool:
    """Safely delete a file if it exists."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info("File deleted | path=%s", filepath)
            return True
        return False
    except OSError as e:
        logger.error("Failed to delete | path=%s | error=%s", filepath, str(e))
        return False


def get_file_size_mb(filepath: str) -> float:
    """Get file size in megabytes."""
    try:
        return os.path.getsize(filepath) / (1024 * 1024)
    except OSError:
        return 0.0