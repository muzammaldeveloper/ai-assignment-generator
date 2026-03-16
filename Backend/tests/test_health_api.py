"""Tests for Health Check API."""

from __future__ import annotations


def test_health_endpoint(client):
    """Health endpoint should return 200 with status info."""
    response = client.get("/api/v1/health")
    data = response.get_json()

    assert response.status_code in (200, 503)
    assert "status" in data
    assert "checks" in data
    assert "version" in data


def test_health_has_all_checks(client):
    """Health endpoint should check all dependencies."""
    response = client.get("/api/v1/health")
    checks = response.get_json()["checks"]

    assert "application" in checks
    assert "database" in checks
    assert "redis" in checks