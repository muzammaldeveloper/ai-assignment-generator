"""Tests for Authentication API."""

from __future__ import annotations


class TestRegister:
    """Tests for POST /api/v1/auth/register."""

    def test_register_success(self, client):
        """Should register a new user and return tokens."""
        response = client.post("/api/v1/auth/register", json={
            "name": "New User",
            "email": "newuser@example.com",
            "password": "StrongPass1",
        })
        data = response.get_json()

        assert response.status_code == 201
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]
        assert data["data"]["user"]["email"] == "newuser@example.com"

    def test_register_duplicate_email(self, client, test_user):
        """Should reject duplicate email with 409."""
        response = client.post("/api/v1/auth/register", json={
            "name": "Another",
            "email": "test@example.com",
            "password": "StrongPass1",
        })
        assert response.status_code == 409

    def test_register_weak_password(self, client):
        """Should reject weak password with 422."""
        response = client.post("/api/v1/auth/register", json={
            "name": "User",
            "email": "weak@example.com",
            "password": "weak",
        })
        assert response.status_code == 422

    def test_register_missing_fields(self, client):
        """Should reject missing required fields."""
        response = client.post("/api/v1/auth/register", json={
            "name": "User",
        })
        assert response.status_code == 422


class TestLogin:
    """Tests for POST /api/v1/auth/login."""

    def test_login_success(self, client, test_user):
        """Should login and return tokens."""
        response = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "TestPass123",
        })
        data = response.get_json()

        assert response.status_code == 200
        assert data["success"] is True
        assert "access_token" in data["data"]

    def test_login_wrong_password(self, client, test_user):
        """Should reject wrong password with 401."""
        response = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "WrongPass1",
        })
        assert response.status_code == 401

    def test_login_nonexistent_email(self, client):
        """Should reject nonexistent email with 401."""
        response = client.post("/api/v1/auth/login", json={
            "email": "nobody@example.com",
            "password": "Whatever1",
        })
        assert response.status_code == 401


class TestMe:
    """Tests for GET /api/v1/auth/me."""

    def test_get_profile_authenticated(self, client, auth_headers):
        """Should return user profile when authenticated."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        data = response.get_json()

        assert response.status_code == 200
        assert data["data"]["email"] == "test@example.com"

    def test_get_profile_unauthenticated(self, client):
        """Should return 401 without token."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401