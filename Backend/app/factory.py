"""Flask application factory."""

from __future__ import annotations

import uuid
from datetime import timedelta
from typing import Optional

from flask import Flask, g, request

from config.settings import Settings, get_settings


def create_app(settings: Optional[Settings] = None) -> Flask:
    """Create and configure the Flask app."""
    app = Flask(__name__)

    settings = settings or get_settings()
    settings.validate_for_runtime()
    _configure_app(app, settings)
    _register_extensions(app, settings)
    _register_blueprints(app)
    _register_error_handlers(app)
    _register_middleware(app)
    _register_jwt_callbacks(app)
    _setup_logging(app, settings)

    # For local SQLite development, auto-create tables to simplify setup.
    if settings.is_development and "sqlite" in settings.database_url:
        with app.app_context():
            from app.extensions import db
            from app.models import User, Assignment, Section, Image, Reference  # noqa: F401
            db.create_all()

    app.logger.info(
        "AI Assignment Generator started | env=%s | db=%s",
        settings.flask_env.value,
        "SQLite" if "sqlite" in settings.database_url else "PostgreSQL",
    )

    return app


def _configure_app(app: Flask, settings: Settings) -> None:
    app.config["SECRET_KEY"] = settings.secret_key
    app.config["DEBUG"] = settings.debug and settings.is_development
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.sqlalchemy_database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = settings.max_content_length_mb * 1024 * 1024
    app.config["SESSION_COOKIE_SECURE"] = settings.is_production
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # SQLite doesn't need pool settings
    if "sqlite" not in settings.database_url:
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "pool_size": 20,
            "pool_recycle": 3600,
            "pool_pre_ping": True,
        }

    app.config["JWT_SECRET_KEY"] = settings.jwt_secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        minutes=settings.jwt_access_token_expires_minutes
    )
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
        days=settings.jwt_refresh_token_expires_days
    )
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    app.config["RATELIMIT_STORAGE_URI"] = settings.rate_limit_storage_uri
    app.config["RATELIMIT_DEFAULT"] = settings.rate_limit_default
    app.config["RATELIMIT_HEADERS_ENABLED"] = True
    app.config["SETTINGS"] = settings


def _register_extensions(app: Flask, settings: Settings) -> None:
    from app.extensions import cors, db, jwt, limiter, ma, migrate

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": settings.cors_origins}},
        supports_credentials=True,
    )
    limiter.init_app(app)


def _register_blueprints(app: Flask) -> None:
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api/v1")


def _register_error_handlers(app: Flask) -> None:
    from app.errors.handlers import register_error_handlers
    register_error_handlers(app)


def _register_middleware(app: Flask) -> None:
    @app.before_request
    def _inject_request_id():
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    @app.after_request
    def _add_headers(response):
        response.headers["X-Request-ID"] = getattr(g, "request_id", "unknown")
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response


def _register_jwt_callbacks(app: Flask) -> None:
    from app.extensions import jwt

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return {"success": False, "error": "Token Expired",
                "message": "Token expired. Please login again."}, 401

    @jwt.invalid_token_loader
    def invalid_token(error):
        return {"success": False, "error": "Invalid Token",
                "message": "The provided token is invalid."}, 401

    @jwt.unauthorized_loader
    def missing_token(error):
        return {"success": False, "error": "Authorization Required",
                "message": "Access token is required."}, 401


def _setup_logging(app: Flask, settings: Settings) -> None:
    import logging
    level = logging.DEBUG if settings.is_development else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    for noisy in ["urllib3", "httpx", "groq", "httpcore"]:
        logging.getLogger(noisy).setLevel(logging.WARNING)