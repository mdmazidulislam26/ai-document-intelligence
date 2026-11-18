"""
Integration tests for FastAPI public health and authenticated endpoints.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from main import app

DEV_HEADERS = {"X-API-Key": "dev-local-api-key-change-me"}


@pytest.mark.asyncio
async def test_health_check_endpoint():
    """Public health check returns 200 OK without exposing secrets."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "llm_provider" in data
        assert "GROQ_API_KEY" not in data


@pytest.mark.asyncio
async def test_search_endpoint_requires_auth_and_validates_query():
    """Asserts unauthenticated search is rejected (401) and missing 'q' when authenticated returns 422."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        unauth_resp = await client.get("/api/search")
        assert unauth_resp.status_code == 401

        auth_resp = await client.get("/api/search", headers=DEV_HEADERS)
        assert auth_resp.status_code == 422
