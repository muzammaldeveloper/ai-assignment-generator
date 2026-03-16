"""
Pytest Fixtures.

Provides test Flask app, test client, database setup,
and test user/token fixtures for all tests.
"""

from __future__ import annotations

import os
import pytest

from app.factory import create_app
from app.extensions import db as _db
from app.models.user import User
from config.settings import Settings


@pytest.fixture(scope="session")
def app():
    """Create a test Flask application."""
    test_settings = Settings(
        secret_key="test-secret-key-minimum-16-chars",
        jwt_secret_key="test-jwt-secret-key-minimum-16",
        database_url=os.getenv(
            "TEST_DATABASE_URL",
            "postgresql://postgres:password@localhost:5432/ai_assignment_test",
        ),
        redis_url="redis://localhost:6379/1",
        openai_api_key="test-openai-key",
        gemini_api_key="test-gemini-key",
        tavily_api_key="test-tavily-key",
        flask_env="testing",
        debug=True,
    )

    app = create_app(settings=test_settings)

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def db(app):
    """Provide a clean database session for each test."""
    with app.app_context():
        _db.session.begin_nested()
        yield _db
        _db.session.rollback()


@pytest.fixture(scope="function")
def client(app):
    """Provide a Flask test client."""
    return app.test_client()


@pytest.fixture(scope="function")
def test_user(app, db):
    """Create and return a test user."""
    with app.app_context():
        user = User(
            name="Test User",
            email="test@example.com",
        )
        user.set_password("TestPass123")
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user


@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    """Get JWT auth headers for the test user."""
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "TestPass123",
    })
    token = response.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}