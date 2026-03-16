"""
Global Error Handlers.

Returns consistent JSON error responses for all error types.
Includes structured logging for debugging and monitoring.
"""

from __future__ import annotations

from flask import Flask, jsonify, g
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from app.utils.logger import get_logger

logger = get_logger(__name__)


def register_error_handlers(app: Flask) -> None:
    """Register all global error handlers."""

    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        """422 — Marshmallow validation failures."""
        request_id = getattr(g, "request_id", "unknown")
        logger.warning(
            "Validation error | request_id=%s | errors=%s",
            request_id, error.messages,
        )
        return jsonify({
            "success": False,
            "error": "Validation Error",
            "message": "The provided data is invalid.",
            "details": error.messages,
            "request_id": request_id,
        }), 422

    @app.errorhandler(ValueError)
    def handle_value_error(error: ValueError):
        """400 — Bad Request (prompt injection, bad input)."""
        request_id = getattr(g, "request_id", "unknown")
        logger.warning(
            "Value error | request_id=%s | message=%s",
            request_id, str(error),
        )
        return jsonify({
            "success": False,
            "error": "Bad Request",
            "message": str(error),
            "request_id": request_id,
        }), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": "The requested resource was not found.",
        }), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": "Method Not Allowed",
            "message": "The HTTP method is not allowed for this endpoint.",
        }), 405

    @app.errorhandler(429)
    def handle_rate_limit(error):
        return jsonify({
            "success": False,
            "error": "Rate Limit Exceeded",
            "message": "Too many requests. Please try again later.",
        }), 429

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        logger.warning("HTTP error | code=%d | desc=%s", error.code, error.description)
        return jsonify({
            "success": False,
            "error": error.name,
            "message": error.description,
        }), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        """500 — Catch-all. Logs full traceback, returns generic message."""
        request_id = getattr(g, "request_id", "unknown")
        logger.exception(
            "Unhandled exception | request_id=%s | error=%s",
            request_id, str(error),
        )
        return jsonify({
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
            "request_id": request_id,
        }), 500