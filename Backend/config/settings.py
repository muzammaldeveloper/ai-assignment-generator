"""
Application Settings — Local Development Friendly.

Uses SQLite by default so no PostgreSQL installation needed.
"""

from __future__ import annotations

from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class StorageBackend(str, Enum):
    LOCAL = "local"
    S3 = "s3"


class Settings(BaseSettings):
    """All settings loaded from .env file automatically."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Flask ──
    flask_app: str = "app.factory:create_app"
    flask_env: EnvironmentType = EnvironmentType.DEVELOPMENT
    secret_key: str = Field(default="dev-secret-key-change-in-production")
    debug: bool = False

    # ── JWT ──
    jwt_secret_key: str = Field(default="dev-jwt-secret-change-in-production")
    jwt_access_token_expires_minutes: int = 60
    jwt_refresh_token_expires_days: int = 30

    # ── Database (SQLite default for local) ──
    database_url: str = Field(default="sqlite:///app.db")

    # ── Redis ──
    redis_url: str = Field(default="redis://localhost:6379/0")

    # ── Groq ──
    groq_api_key: str = Field(default="")
    groq_model: str = "llama-3.3-70b-versatile"
    groq_max_tokens: int = 4096
    groq_temperature: float = 0.7

    # ── Gemini ──
    gemini_api_key: str = Field(default="")
    gemini_model: str = "gemini-2.0-flash-exp"

    # ── Tavily ──
    tavily_api_key: str = Field(default="")
    tavily_max_results: int = 5

    # ── AWS S3 (not needed for local) ──
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_s3_bucket: Optional[str] = None
    aws_s3_region: str = "us-east-1"

    # ── Rate Limiting ──
    rate_limit_default: str = "200/hour"
    rate_limit_generation: str = "20/hour"
    rate_limit_storage_uri: str = "memory://"

    # ── CORS ──
    cors_allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # ── Request Limits ──
    max_content_length_mb: int = 10

    # ── Application ──
    max_concurrent_jobs: int = 10
    assignment_timeout_seconds: int = 120
    storage_backend: StorageBackend = StorageBackend.LOCAL
    storage_local_path: str = "storage"

    @property
    def is_production(self) -> bool:
        return self.flask_env == EnvironmentType.PRODUCTION

    @property
    def is_development(self) -> bool:
        return self.flask_env == EnvironmentType.DEVELOPMENT

    @property
    def sqlalchemy_database_uri(self) -> str:
        return self.database_url

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.cors_allowed_origins.split(",") if o.strip()]

    @field_validator("max_content_length_mb")
    @classmethod
    def validate_max_content_length(cls, value: int) -> int:
        if value < 1:
            raise ValueError("max_content_length_mb must be >= 1")
        return value

    def validate_for_runtime(self) -> None:
        if not self.is_production:
            return

        if self.debug:
            raise ValueError("DEBUG must be false in production")

        if self.secret_key == "dev-secret-key-change-in-production":
            raise ValueError("SECRET_KEY must be changed in production")

        if self.jwt_secret_key == "dev-jwt-secret-change-in-production":
            raise ValueError("JWT_SECRET_KEY must be changed in production")

        if not self.cors_origins:
            raise ValueError("At least one CORS origin must be configured in production")

        if "*" in self.cors_origins:
            raise ValueError("Wildcard CORS is not allowed in production")

        if self.rate_limit_storage_uri == "memory://":
            raise ValueError("Use Redis-backed rate limiting in production")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings (loaded once)."""
    return Settings()