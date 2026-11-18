"""
Main entry point for the FastAPI Document Intelligence System.
Fails fast on startup if required database migrations are missing or inconsistent (GHR-05).
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import init_db
from core.config import settings
from api.routes import auth, documents, corrections, search

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager verifying Alembic migration status before serving traffic.
    Does NOT swallow database or migration failures.
    """
    logger.info("Starting up Document Intelligence API...")
    mig_status = await init_db()
    logger.info(f"Database migration verification passed: heads={mig_status.get('current_heads')}")
    yield
    logger.info("Shutting down Document Intelligence API...")


app = FastAPI(
    title="AI-Powered Document Intelligence API",
    description="Automated financial document processing, zero-hallucination extraction, validation, and hybrid search.",
    version="1.0.0",
    lifespan=lifespan,
)

cors_kwargs = {
    "allow_origins": settings.get_allowed_origins(),
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Authorization", "Content-Type", "X-API-Key", "X-Internal-Service-Token"],
}
if settings.ALLOWED_ORIGIN_REGEX:
    cors_kwargs["allow_origin_regex"] = settings.ALLOWED_ORIGIN_REGEX

app.add_middleware(CORSMiddleware, **cors_kwargs)

app.include_router(auth.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(corrections.router, prefix="/api")
app.include_router(search.router, prefix="/api")


@app.get("/api/health", tags=["Health"])
async def health_check():
    """Public service health check endpoint (no sensitive credentials exposed)."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "llm_provider": settings.LLM_PROVIDER,
        "embedding_model": settings.EMBEDDING_MODEL_NAME,
    }
