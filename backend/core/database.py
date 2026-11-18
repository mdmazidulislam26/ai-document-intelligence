"""
Database connection, Alembic migration verification, and safe startup lifecycle (GHR-05).
Prevents production startup when required migrations are missing or inconsistent,
and never relies on Base.metadata.create_all() in production.
"""

import os
import asyncio
import logging
from typing import AsyncGenerator, Dict, Any, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import declarative_base
from alembic import command
from alembic.config import Config as AlembicConfig
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from alembic.util.exc import CommandError
from core.config import settings

logger = logging.getLogger("database")

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()


class MigrationSafetyError(RuntimeError):
    """Raised when database Alembic migration state is behind, missing, or inconsistent."""
    pass


def _build_alembic_config(sync_url: Optional[str] = None) -> AlembicConfig:
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    alembic_ini_path = os.path.join(backend_dir, "alembic.ini")
    alembic_script_dir = os.path.join(backend_dir, "alembic")

    cfg = AlembicConfig(alembic_ini_path)
    cfg.set_main_option("script_location", alembic_script_dir)
    url = sync_url or settings.SYNC_DATABASE_URL
    cfg.set_main_option("sqlalchemy.url", url.replace("%", "%%"))
    return cfg


def verify_migration_status_sync(connection=None, alembic_cfg: Optional[AlembicConfig] = None) -> Dict[str, Any]:
    """
    Verifies that the database is at the exact expected Alembic head revision(s)
    and that all applied revisions exist in the Alembic script directory.
    Raises MigrationSafetyError on any mismatch or uninitialized DB.
    """
    cfg = alembic_cfg or _build_alembic_config()
    script = ScriptDirectory.from_config(cfg)
    expected_heads = tuple(sorted(script.get_heads()))

    def _inspect_conn(conn) -> Dict[str, Any]:
        mig_ctx = MigrationContext.configure(conn)
        current_heads = tuple(sorted(mig_ctx.get_current_heads()))

        if not current_heads:
            raise MigrationSafetyError(
                f"Database has no applied Alembic migrations (expected head: {expected_heads}). "
                "Run 'alembic upgrade head' before starting the application."
            )

        for rev in current_heads:
            try:
                script.get_revision(rev)
            except CommandError as exc:
                raise MigrationSafetyError(
                    f"Database contains unknown/missing Alembic revision '{rev}'. "
                    "Verify deployed code matches database schema."
                ) from exc

        if current_heads != expected_heads:
            raise MigrationSafetyError(
                f"Database schema is out of date: current={current_heads}, expected={expected_heads}. "
                "Run 'alembic upgrade head' before serving traffic."
            )

        return {"current_heads": current_heads, "expected_heads": expected_heads, "up_to_date": True}

    if connection is not None:
        return _inspect_conn(connection)

    sync_engine = create_engine(settings.SYNC_DATABASE_URL, pool_pre_ping=True)
    try:
        with sync_engine.connect() as conn:
            return _inspect_conn(conn)
    finally:
        sync_engine.dispose()


def run_migrations_sync() -> None:
    """
    Executes Alembic 'upgrade head' synchronously under a PostgreSQL advisory lock.
    """
    alembic_cfg = _build_alembic_config()
    sync_engine = create_engine(settings.SYNC_DATABASE_URL, pool_pre_ping=True)
    try:
        with sync_engine.connect() as conn:
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


async def init_db() -> Dict[str, Any]:
    """
    Initializes pgvector (in auto-migrate mode) and strictly enforces Alembic migration parity.
    In production (should_auto_migrate() == False), verifies migrations without running create_all()
    or automatic DDL, failing fast if migrations are missing/behind.
    """
    if settings.should_auto_migrate():
        async with engine.begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        await asyncio.to_thread(run_migrations_sync)

    return await asyncio.to_thread(verify_migration_status_sync)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
