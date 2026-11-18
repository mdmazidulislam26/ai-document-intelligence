"""
Database connection and session lifecycle management.
Provides asynchronous session generators for FastAPI dependency injection
and executes Alembic migrations safely on startup without relying on Base.metadata.create_all().
"""

import os
import asyncio
import logging
from typing import AsyncGenerator
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import declarative_base
from alembic import command
from alembic.config import Config as AlembicConfig
from core.config import settings

logger = logging.getLogger("database")

# Create async engine with connection pooling
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Base declarative class for all models
Base = declarative_base()


def run_migrations_sync() -> None:
    """
    Executes Alembic 'upgrade head' synchronously under a PostgreSQL advisory lock
    so concurrent workers or instances cannot race on schema migrations.
    """
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    alembic_ini_path = os.path.join(backend_dir, "alembic.ini")
    alembic_script_dir = os.path.join(backend_dir, "alembic")

    alembic_cfg = AlembicConfig(alembic_ini_path)
    alembic_cfg.set_main_option("script_location", alembic_script_dir)
    alembic_cfg.set_main_option("sqlalchemy.url", settings.SYNC_DATABASE_URL.replace("%", "%%"))

    sync_engine = create_engine(settings.SYNC_DATABASE_URL, pool_pre_ping=True)
    try:
        with sync_engine.connect() as conn:
            # Acquire session-level advisory lock for safe concurrent startup
            conn.execute(text("SELECT pg_advisory_lock(84729103);"))
            conn.commit()
            try:
                alembic_cfg.attributes["connection"] = conn
                command.upgrade(alembic_cfg, "head")
                conn.commit()
            finally:
                conn.execute(text("SELECT pg_advisory_unlock(84729103);"))
                conn.commit()
    finally:
        sync_engine.dispose()


async def init_db() -> None:
    """
    Initializes PostgreSQL pgvector extension and brings schema to latest Alembic head.
    """
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

    await asyncio.to_thread(run_migrations_sync)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an asynchronous database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()