"""
Structured Logging Utility.

Provides request-aware logging with unique request IDs
for full traceability across the application.
"""

from __future__ import annotations

import logging
import sys
from typing import Optional

from flask import g, has_request_context


class RequestContextFilter(logging.Filter):
    """
    Logging filter that injects request context (request_id)
    into every log record for full traceability.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if has_request_context():
            record.request_id = getattr(g, "request_id", "no-request")
        else:
            record.request_id = "system"
        return True


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger with request context injection.

    Args:
        name: Logger name (typically __name__).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name or "ai_assignment")

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt=(
                "%(asctime)s | %(levelname)-8s | %(request_id)s | "
                "%(name)s | %(funcName)s:%(lineno)d | %(message)s"
            ),
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        handler.addFilter(RequestContextFilter())
        logger.addHandler(handler)
        logger.propagate = False

    return logger