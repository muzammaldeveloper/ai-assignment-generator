"""Health Check — works without Redis."""

from __future__ import annotations
from flask import Blueprint, jsonify
from app.extensions import db

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Check system health."""
    db_status = "healthy"
    try:
        db.session.execute(db.text("SELECT 1"))
    except Exception:
        db_status = "unhealthy"

    return jsonify({
        "status": "healthy" if db_status == "healthy" else "degraded",
        "checks": {
            "application": "healthy",
            "database": db_status,
        },
        "version": "2.0.0",
        "mode": "local",
    }), 200 if db_status == "healthy" else 503