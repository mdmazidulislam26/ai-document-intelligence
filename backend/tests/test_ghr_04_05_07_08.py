"""
Targeted automated tests for Phase 5.2 Part 2:
- GHR-04: Preserve unknown/null currency across extraction, API, and manual corrections
- GHR-05: Enforce migration safety (at head, behind head, missing revision, migration failure, fresh DB)
- GHR-07: Cross-process stable SHA-256 rate limit keys & atomic Redis enforcement
- GHR-08: Docker Compose parameterized credentials & clean .env.example
"""

import os
import sys
import uuid
import json
import subprocess
from decimal import Decimal
from unittest.mock import patch
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from alembic import command
from alembic.config import Config as AlembicConfig

from core.config import settings
from core.database import get_db, verify_migration_status_sync, MigrationSafetyError
from core.rate_limit import compute_rate_limit_subject, RateLimiter
from main import app, lifespan
from models.document import ExtractedInvoice
from models.schemas import InvoiceExtractionSchema
from tasks.processing_tasks import process_document_task

DEV_HEADERS = {"X-API-Key": "dev-local-api-key-change-me"}
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(BACKEND_DIR)


def test_ghr04_orm_and_schema_default_currency_is_none():
    schema = InvoiceExtractionSchema(invoice_number="INV-NOCURR-1", total_amount=Decimal("100.00"))
    assert schema.currency is None

    orm_obj = ExtractedInvoice(document_id=1, invoice_number="INV-NOCURR-1", total_amount=Decimal("100.00"))
    assert orm_obj.currency is None


@pytest.mark.asyncio
async def test_ghr04_unknown_currency_preserved_across_pipeline_and_corrections():
    sync_engine = create_engine(settings.SYNC_DATABASE_URL)
    test_async_engine = create_async_engine(settings.DATABASE_URL)
    TestSession = async_sessionmaker(bind=test_async_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    doc_id = None

    try:
        with sync_engine.connect() as conn:
            doc_id = conn.execute(
                text("""
                    INSERT INTO documents (owner_id, filename, file_path, file_type, file_size_bytes, status, created_at, updated_at)
                    VALUES ('default', 'nocurr.pdf', :fp, '.pdf', 100, 'queued', NOW(), NOW())
                    RETURNING id
                """),
                {"fp": f"/tmp/ghr04_{uuid.uuid4().hex}.pdf"},
            ).scalar()
            conn.commit()

        extracted_null_curr = InvoiceExtractionSchema(
            invoice_number="INV-NULL-CURR",
            invoice_date="2024-05-01",
            supplier_name="Global Co",
            subtotal=Decimal("100.00"),
            tax=Decimal("10.00"),
            total_amount=Decimal("110.00"),
            currency=None,
        )

        with patch("tasks.processing_tasks.DocumentParserService.extract_full_text", return_value=("Invoice text", 1)), \
             patch("tasks.processing_tasks.AIExtractorService.extract_invoice_data", return_value=extracted_null_curr):
            assert process_document_task(doc_id) is True

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            g1 = await client.get(f"/api/documents/{doc_id}", headers=DEV_HEADERS)
            assert g1.status_code == 200
            assert g1.json()["extracted_invoice"]["currency"] is None

            p1 = await client.put(
                f"/api/documents/{doc_id}/correct",
                json={"invoice_number": "INV-NULL-CURR-EDITED"},
                headers=DEV_HEADERS,
            )
            assert p1.status_code == 200
            assert p1.json()["extracted_invoice"]["invoice_number"] == "INV-NULL-CURR-EDITED"
            assert p1.json()["extracted_invoice"]["currency"] is None

            p2 = await client.put(
                f"/api/documents/{doc_id}/correct",
                json={"customer_name": "Updated Client", "currency": None},
                headers=DEV_HEADERS,
            )
            assert p2.status_code == 200
            assert p2.json()["extracted_invoice"]["currency"] is None

            p3 = await client.put(
                f"/api/documents/{doc_id}/correct",
                json={"currency": "eur"},
                headers=DEV_HEADERS,
            )
            assert p3.status_code == 200
            assert p3.json()["extracted_invoice"]["currency"] == "EUR"

            p4 = await client.put(
                f"/api/documents/{doc_id}/correct",
                json={"currency": ""},
                headers=DEV_HEADERS,
            )
            assert p4.status_code == 200
            assert p4.json()["extracted_invoice"]["currency"] is None
    finally:
        app.dependency_overrides.clear()
        await test_async_engine.dispose()
        if doc_id is not None:
            with sync_engine.connect() as conn:
                conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": doc_id})
                conn.commit()
        sync_engine.dispose()


@pytest.mark.asyncio
async def test_ghr05_migration_safety_checks_and_fail_fast():
    engine = create_engine(settings.SYNC_DATABASE_URL)
    schema_name = "test_ghr05_mig_safety"
    cfg = AlembicConfig(os.path.join(BACKEND_DIR, "alembic.ini"))
    cfg.set_main_option("script_location", os.path.join(BACKEND_DIR, "alembic"))
    cfg.set_main_option("sqlalchemy.url", settings.SYNC_DATABASE_URL.replace("%", "%%"))

    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector SCHEMA public;"))
            conn.execute(text(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"))
            conn.execute(text(f"CREATE SCHEMA {schema_name};"))
            conn.commit()

            conn.execute(text(f"SET search_path TO {schema_name};"))
            conn.commit()

            with pytest.raises(MigrationSafetyError, match="no applied Alembic migrations"):
                verify_migration_status_sync(connection=conn, alembic_cfg=cfg)

            conn.execute(text(f"SET search_path TO {schema_name}, public;"))
            cfg.attributes["connection"] = conn
            cfg.attributes["version_table_schema"] = schema_name
            command.upgrade(cfg, "head")
            conn.commit()

            conn.execute(text(f"SET search_path TO {schema_name};"))
            status = verify_migration_status_sync(connection=conn, alembic_cfg=cfg)
            assert status["up_to_date"] is True

            conn.execute(text(f"SET search_path TO {schema_name}, public;"))
            command.downgrade(cfg, "0007_worker_lease_currency")
            conn.commit()
            conn.execute(text(f"SET search_path TO {schema_name};"))
            with pytest.raises(MigrationSafetyError, match="out of date"):
                verify_migration_status_sync(connection=conn, alembic_cfg=cfg)

            conn.execute(text(f"UPDATE {schema_name}.alembic_version SET version_num = '9999_missing_rev'"))
            conn.commit()
            with pytest.raises(MigrationSafetyError, match="unknown/missing Alembic revision"):
                verify_migration_status_sync(connection=conn, alembic_cfg=cfg)

        secure_prod_key = "R4nd0m!Production-Auth-Key_2026#G7x9vP2s"
        secure_keys_json = json.dumps({"r4nd0mApiKey_2026#G7x9vP2s!": {"owner_id": "admin", "role": "admin"}})
        with patch.object(settings, "ENVIRONMENT", "production"), \
             patch.object(settings, "AUTH_SECRET_KEY", secure_prod_key), \
             patch.object(settings, "API_KEYS_JSON", secure_keys_json), \
             patch.object(settings, "INTERNAL_SERVICE_TOKEN", "T0k3n!Internal-Secret_2026#xP9v"), \
             patch.object(settings, "DATABASE_URL", "postgresql+asyncpg://app_user:StrongProdPass99!@db:5432/doc_intelligence"), \
             patch.object(settings, "SYNC_DATABASE_URL", "postgresql+psycopg2://app_user:StrongProdPass99!@db:5432/doc_intelligence"), \
             patch.object(settings, "AUTO_RUN_MIGRATIONS", None), \
             patch("core.database.verify_migration_status_sync", side_effect=MigrationSafetyError("DB behind head")):
            with pytest.raises(MigrationSafetyError, match="DB behind head"):
                async with lifespan(app):
                    pass

        with patch.object(settings, "ENVIRONMENT", "development"), \
             patch.object(settings, "AUTO_RUN_MIGRATIONS", True), \
             patch("core.database.run_migrations_sync", side_effect=RuntimeError("Migration script error")):
            with pytest.raises(RuntimeError, match="Migration script error"):
                async with lifespan(app):
                    pass
    finally:
        with engine.connect() as conn:
            conn.execute(text(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"))
            conn.commit()
        engine.dispose()


def test_ghr07_rate_limit_keys_consistent_across_processes():
    code = (
        "import sys; sys.path.insert(0, '.'); "
        "from core.rate_limit import compute_rate_limit_subject; "
        "print(compute_rate_limit_subject('10.20.30.40', 'secret-api-key-123'))"
    )
    env1 = {**os.environ, "PYTHONHASHSEED": "11"}
    env2 = {**os.environ, "PYTHONHASHSEED": "9999"}

    res1 = subprocess.run([sys.executable, "-c", code], cwd=BACKEND_DIR, env=env1, capture_output=True, text=True, check=True)
    res2 = subprocess.run([sys.executable, "-c", code], cwd=BACKEND_DIR, env=env2, capture_output=True, text=True, check=True)

    key1 = res1.stdout.strip()
    key2 = res2.stdout.strip()
    assert len(key1) == 32
    assert key1 == key2
    assert "secret-api-key-123" not in key1
    assert "10.20.30.40" not in key1


def test_ghr07_atomic_redis_rate_limiting():
    RateLimiter.reset()
    try:
        subj = compute_rate_limit_subject("127.0.0.1", "worker-test-key")
        RateLimiter.check_limit(subj, "ghr07_test", max_requests=2, window_seconds=60)
        RateLimiter.check_limit(subj, "ghr07_test", max_requests=2, window_seconds=60)

        with pytest.raises(Exception) as exc_info:
            RateLimiter.check_limit(subj, "ghr07_test", max_requests=2, window_seconds=60)
        assert getattr(exc_info.value, "status_code", None) == 429

        r_client = RateLimiter._get_redis()
        if r_client is not None:
            assert r_client.zcard(f"ratelimit:ghr07_test:{subj}") == 2
    finally:
        RateLimiter.reset()


def test_ghr08_docker_compose_uses_env_vars_not_hardcoded_credentials():
    compose_path = os.path.join(REPO_ROOT, "docker-compose.yml")
    env_example_path = os.path.join(REPO_ROOT, ".env.example")

    if os.path.exists(compose_path):
        with open(compose_path, "r") as f:
            compose_content = f.read()
        assert "postgres:postgres@" not in compose_content
        assert "${POSTGRES_USER" in compose_content
        assert "${POSTGRES_PASSWORD" in compose_content
        assert "${POSTGRES_DB" in compose_content

    if os.path.exists(env_example_path):
        with open(env_example_path, "r") as f:
            env_content = f.read()
        assert "POSTGRES_PASSWORD=" in env_content
        assert "your_groq_api_key_here" in env_content
