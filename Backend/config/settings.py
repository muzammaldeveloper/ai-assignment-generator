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
    debug: bool = True

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


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings (loaded once)."""
    return Settings()