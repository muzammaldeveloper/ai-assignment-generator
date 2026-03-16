"""
API Blueprint Registration.
"""

from __future__ import annotations
from flask import Blueprint

api_bp = Blueprint("api", __name__)


def _register_sub_blueprints() -> None:
    from app.api.health_api import health_bp
    from app.api.user_api import auth_bp
    from app.api.assignment_api import assignment_bp

    api_bp.register_blueprint(health_bp)
    api_bp.register_blueprint(auth_bp, url_prefix="/auth")
    api_bp.register_blueprint(assignment_bp, url_prefix="/assignments")


_register_sub_blueprints()