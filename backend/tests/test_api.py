"""
Integration tests for FastAPI endpoints.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_health_check_endpoint():
    """Asserts that the system health check returns 200 OK and valid status."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "llm_provider" in data


@pytest.mark.asyncio
async def test_search_endpoint_empty():
    """Asserts that searching without parameters or empty query responds appropriately."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/search")
        assert response.status_code == 422  # Missing required query param 'q'
