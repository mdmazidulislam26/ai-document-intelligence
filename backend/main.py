"""
Main entry point for the FastAPI Document Intelligence System.
Initializes lifespan events, CORS, database schemas, and API routers.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import init_db
from core.config import settings
from api.routes import documents, corrections, search

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager that initializes database tables and pgvector on startup.
    """
    logger.info("Starting up Document Intelligence API...")
    try:
        await init_db()
        logger.info("PostgreSQL database tables and pgvector extension initialized.")
    except Exception as e:
        logger.exception(f"Database initialization error: {str(e)}")
    
    yield
    logger.info("Shutting down Document Intelligence API...")


app = FastAPI(
    title="AI-Powered Document Intelligence API",
    description="Automated financial document processing, zero-hallucination extraction, validation, and hybrid search.",
    version="1.0.0",
    lifespan=lifespan
)

# Robust CORS configuration: allows localhost, 127.0.0.1, and Codespaces preview domains
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(documents.router, prefix="/api")
app.include_router(corrections.router, prefix="/api")
app.include_router(search.router, prefix="/api")


@app.get("/api/health", tags=["Health"])
async def health_check():
    """
    Service health check endpoint.
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "llm_provider": settings.LLM_PROVIDER,
        "embedding_model": settings.EMBEDDING_MODEL_NAME
    }
