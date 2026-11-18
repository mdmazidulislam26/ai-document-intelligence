"""
Regression tests for Hotfix Batch A addressing Phase 5.2 Independent Review findings:
1. Production placeholder/default secrets rejection (AUTH_SECRET_KEY, INTERNAL_SERVICE_TOKEN, API_KEYS_JSON, DB password).
2. GHR-01 CAS lease fencing: retries > 0 cannot bypass active lease, stale worker aborts if lease cleared/reassigned,
   /reprocess returns 409 Conflict when an active lease exists.
3. GHR-05/08: Production disables auto-migrate even if AUTO_RUN_MIGRATIONS=true; docker-compose.prod.yml enforces required vars & separate migrate service.
4. GHR-07: Concurrent rate-limiting contention & production fail-closed behavior during Redis outage.
"""

import os
import sys
import re
import json
import uuid
import tempfile
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
import pytest
from fastapi import HTTPException
from celery.exceptions import MaxRetriesExceededError, Retry
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(BACKEND_DIR)
for import_root in (REPO_ROOT, BACKEND_DIR):
    if import_root not in sys.path:
        sys.path.insert(0, import_root)

from core.config import Settings, settings
from core.database import get_db
from core.rate_limit import RateLimiter, compute_rate_limit_subject
from core.security import verify_api_key
from main import app
from models.schemas import InvoiceExtractionSchema, LineItemSchema
from tasks.processing_tasks import process_document_task
from services.ai_extractor import AITransientError
from evaluation.evaluate import classify_arithmetic_status

DEV_HEADERS = {"X-API-Key": "dev-local-api-key-change-me"}


def test_production_rejects_placeholder_and_weak_secrets():
    """Security Hotfix: public .env.example placeholders must fail closed in production."""
    strong_secret = "R4nd0m!Prod-Auth-Key_2026#G7x9vP2s"
    strong_db = "postgresql+asyncpg://appuser:Str0ngProdPass!99@db:5432/doc_intelligence"
    strong_sync_db = "postgresql+psycopg2://appuser:Str0ngProdPass!99@db:5432/doc_intelligence"
    strong_keys = json.dumps({"prod-key-9876543210abcdef": {"owner_id": "acme", "role": "user"}})

    # 1. Placeholder AUTH_SECRET_KEY rejected
    s_bad_secret = Settings(
        ENVIRONMENT="production",
        AUTH_SECRET_KEY="replace-with-strong-random-32byte-secret",
        API_KEYS_JSON=strong_keys,
        DATABASE_URL=strong_db,
        SYNC_DATABASE_URL=strong_sync_db,
    )
    with pytest.raises(RuntimeError, match="AUTH_SECRET_KEY"):
        s_bad_secret.validate_production_security()

    # 2. Placeholder INTERNAL_SERVICE_TOKEN rejected
    s_bad_internal = Settings(
        ENVIRONMENT="production",
        AUTH_SECRET_KEY=strong_secret,
        INTERNAL_SERVICE_TOKEN="replace-with-internal-service-secret",
        API_KEYS_JSON=strong_keys,
        DATABASE_URL=strong_db,
        SYNC_DATABASE_URL=strong_sync_db,
    )
    with pytest.raises(RuntimeError, match="INTERNAL_SERVICE_TOKEN"):
        s_bad_internal.validate_production_security()

    # 3. Dev placeholder API key rejected in production
    s_bad_apikey = Settings(
        ENVIRONMENT="production",
        AUTH_SECRET_KEY=strong_secret,
        API_KEYS_JSON=json.dumps({"dev-local-api-key-change-me": {"owner_id": "default", "role": "user"}}),
        DATABASE_URL=strong_db,
        SYNC_DATABASE_URL=strong_sync_db,
    )
    with pytest.raises(RuntimeError, match="API key"):
        s_bad_apikey.validate_production_security()

    with patch.object(settings, "ENVIRONMENT", "production"):
        assert verify_api_key("dev-local-api-key-change-me") is None

    # 4. Weak DB password rejected in production
    s_bad_db = Settings(
        ENVIRONMENT="production",
        AUTH_SECRET_KEY=strong_secret,
        API_KEYS_JSON=strong_keys,
        DATABASE_URL="postgresql+asyncpg://postgres:postgres@db:5432/doc_intelligence",
        SYNC_DATABASE_URL=strong_sync_db,
    )
    with pytest.raises(RuntimeError, match="database password"):
        s_bad_db.validate_production_security()

    # 5. Long but repetitive secrets must not pass merely because of length
    s_repeated_secret = Settings(
        ENVIRONMENT="production",
        AUTH_SECRET_KEY="a" * 40,
        API_KEYS_JSON=strong_keys,
        DATABASE_URL=strong_db,
        SYNC_DATABASE_URL=strong_sync_db,
    )
    with pytest.raises(RuntimeError, match="AUTH_SECRET_KEY"):
        s_repeated_secret.validate_production_security()

    # 6. Reject generic weak database passwords even when longer than 16 chars.
    weak_password_db = "postgresql+asyncpg://appuser:weakpassword123456@db:5432/doc_intelligence"
    s_weak_db = Settings(
        ENVIRONMENT="production",
        AUTH_SECRET_KEY=strong_secret,
        API_KEYS_JSON=strong_keys,
        DATABASE_URL=weak_password_db,
        SYNC_DATABASE_URL=strong_sync_db,
    )
    with pytest.raises(RuntimeError, match="database password"):
        s_weak_db.validate_production_security()

    # 7. Valid high-entropy production config passes
    s_ok = Settings(
        ENVIRONMENT="production",
        AUTH_SECRET_KEY=strong_secret,
        INTERNAL_SERVICE_TOKEN="internal-prod-token-9876543210",
        API_KEYS_JSON=strong_keys,
        DATABASE_URL=strong_db,
        SYNC_DATABASE_URL=strong_sync_db,
    )
    s_ok.validate_production_security()


def test_ghr05_production_disables_auto_migrate_even_if_env_flag_true():
    """GHR-05: ENVIRONMENT=production must NEVER auto-run migrations even if AUTO_RUN_MIGRATIONS=true."""
    s_prod = Settings(ENVIRONMENT="production", AUTO_RUN_MIGRATIONS=True)
    assert s_prod.should_auto_migrate() is False

    s_dev = Settings(ENVIRONMENT="development", AUTO_RUN_MIGRATIONS=True)
    assert s_dev.should_auto_migrate() is True


def test_ghr08_prod_compose_requires_explicit_secrets_and_separate_migrate():
    """GHR-08 / GHR-05: Verifies docker-compose.prod.yml enforces required env vars and separate migrate step."""
    prod_compose = os.path.join(REPO_ROOT, "docker-compose.prod.yml")
    if os.path.exists(prod_compose):
        with open(prod_compose, "r") as f:
            content = f.read()
        assert ":-postgres" not in content
        assert "${POSTGRES_PASSWORD:?" in content
        assert "${AUTH_SECRET_KEY:?" in content
        assert "migrate:" in content
        assert "service_completed_successfully" in content

        # Inspect actual command fields; comments must not affect the assertion.
        for service_name in ("backend", "celery_worker"):
            service_match = re.search(
                rf"(?ms)^  {service_name}:\n(.*?)(?=^  [A-Za-z0-9_-]+:\n|\Z)",
                content,
            )
            assert service_match, f"Missing production service: {service_name}"
            command_match = re.search(r"(?m)^\s+command:\s*(.+)$", service_match.group(1))
            assert command_match, f"Missing command for production service: {service_name}"
            assert "--reload" not in command_match.group(1), f"Development reload enabled for {service_name}"


def test_ghr01_retry_cannot_bypass_active_lease_and_stale_worker_fenced_out():
    """
    GHR-01:
    1. A retry delivery (retries=1) arriving while another worker holds a live lease must NOT steal it.
    2. A stale worker whose lease/worker_id was cleared/reassigned mid-flight must abort final write.
    """
    engine = create_engine(settings.SYNC_DATABASE_URL)
    doc_id = None
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    with open(path, "wb") as f:
        f.write(b"%PDF-1.4\n%fencing")

    try:
        with engine.connect() as conn:
            doc_id = conn.execute(
                text("""
                    INSERT INTO documents
                        (owner_id, filename, file_path, file_type, file_size_bytes, status,
                         worker_id, lease_epoch, processing_lease_until, last_heartbeat_at, created_at, updated_at)
                    VALUES
                        ('default', 'fenced.pdf', :fp, '.pdf', 64, 'processing',
                         'live-worker-1', 5, NOW() + INTERVAL '5 minutes', NOW(), NOW(), NOW())
                    RETURNING id
                """),
                {"fp": path},
            ).scalar()
            conn.commit()

        # 1. Retry delivery (retries=1) while live-worker-1 holds valid lease -> rejected
        with patch.object(process_document_task.request, "retries", 1):
            res = process_document_task(doc_id)
            assert res is False

        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT worker_id, lease_epoch FROM documents WHERE id = :id"),
                {"id": doc_id},
            ).mappings().first()
            assert row["worker_id"] == "live-worker-1"
            assert row["lease_epoch"] == 5

            # Reset to queued for stale-worker fencing test
            conn.execute(
                text("""
                    UPDATE documents
                    SET status = 'queued', worker_id = NULL, processing_lease_until = NULL, lease_epoch = 10
                    WHERE id = :id
                """),
                {"id": doc_id},
            )
            conn.commit()

        # 2. Stale worker starts, then reconciliation/reprocess clears worker_id & bumps lease_epoch mid-flight
        def slow_parser_with_midflight_takeover(_path):
            with engine.connect() as conn2:
                conn2.execute(
                    text("""
                        UPDATE documents
                        SET status = 'queued', worker_id = NULL, processing_lease_until = NULL, lease_epoch = 12
                        WHERE id = :id
                    """),
                    {"id": doc_id},
                )
                conn2.commit()
            return ("Invoice #STALE-1 Total: 100.00", 1)

        stale_extraction = InvoiceExtractionSchema(
            invoice_number="INV-STALE-1",
            invoice_date="2024-06-01",
            supplier_name="Stale Corp",
            subtotal=Decimal("100.00"),
            tax=Decimal("0.00"),
            total_amount=Decimal("100.00"),
        )

        with patch("tasks.processing_tasks.DocumentParserService.extract_full_text", side_effect=slow_parser_with_midflight_takeover), \
             patch("tasks.processing_tasks.AIExtractorService.extract_invoice_data", return_value=stale_extraction):
            res_stale = process_document_task(doc_id)
            assert res_stale is False

        with engine.connect() as conn:
            row_after = conn.execute(
                text("SELECT status, lease_epoch FROM documents WHERE id = :id"),
                {"id": doc_id},
            ).mappings().first()
            assert row_after["status"] == "queued"
            assert row_after["lease_epoch"] == 12
            inv_cnt = conn.execute(
                text("SELECT COUNT(*) FROM extracted_invoices WHERE document_id = :id"),
                {"id": doc_id},
            ).scalar()
            assert inv_cnt == 0
    finally:
        if doc_id is not None:
            with engine.connect() as conn:
                conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": doc_id})
                conn.commit()
        engine.dispose()
        if os.path.exists(path):
            os.remove(path)


@pytest.mark.asyncio
async def test_ghr01_reprocess_rejects_active_lease_with_409():
    """GHR-01: POST /api/documents/{id}/reprocess returns 409 Conflict if document holds active lease."""
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
                    INSERT INTO documents
                        (owner_id, filename, file_path, file_type, file_size_bytes, status,
                         worker_id, lease_epoch, processing_lease_until, created_at, updated_at)
                    VALUES
                        ('default', 'active_reproc.pdf', :fp, '.pdf', 100, 'processing',
                         'active-worker', 1, NOW() + INTERVAL '5 minutes', NOW(), NOW())
                    RETURNING id
                """),
                {"fp": f"/tmp/reproc_409_{uuid.uuid4().hex}.pdf"},
            ).scalar()
            conn.commit()

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post(f"/api/documents/{doc_id}/reprocess", headers=DEV_HEADERS)
            assert resp.status_code == 409
    finally:
        app.dependency_overrides.clear()
        await test_async_engine.dispose()
        if doc_id is not None:
            with sync_engine.connect() as conn:
                conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": doc_id})
                conn.commit()
        sync_engine.dispose()


def test_ghr07_concurrent_rate_limiting_and_prod_fail_closed():
    """GHR-07: Verifies atomic Lua contention under 10 concurrent threads and production 503 fail-closed."""
    RateLimiter.reset()
    try:
        subj = compute_rate_limit_subject("10.0.0.1", "concurrent-key")

        def _hit(_i):
            try:
                RateLimiter.check_limit(subj, "ghr07_conc", max_requests=5, window_seconds=60)
                return 200
            except HTTPException as exc:
                return exc.status_code

        with ThreadPoolExecutor(max_workers=10) as pool:
            codes = list(pool.map(_hit, range(10)))

        assert codes.count(200) == 5
        assert codes.count(429) == 5

        # Production fail-closed when Redis is unavailable
        with patch.object(settings, "ENVIRONMENT", "production"), \
             patch.object(settings, "RATE_LIMIT_FAIL_CLOSED_IN_PROD", True), \
             patch.object(RateLimiter, "_get_redis", return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                RateLimiter.check_limit(subj, "ghr07_outage", max_requests=10)
            assert exc_info.value.status_code == 503
    finally:
        RateLimiter.reset()


@pytest.mark.parametrize(
    "failure_stage",
    ["parser_exception", "empty_text", "transient_max_retries", "unexpected_exception"],
)
def test_ghr01_stale_worker_failure_paths_cannot_overwrite_new_lease(failure_stage):
    """Every terminal error path must CAS against the worker's claimed epoch."""
    engine = create_engine(settings.SYNC_DATABASE_URL)
    doc_id = None
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    with open(path, "wb") as f:
        f.write(b"%PDF-1.4\\n%stale-failure-fencing")

    def simulate_takeover():
        with engine.connect() as conn:
            conn.execute(
                text("""
                    UPDATE documents
                    SET status = 'queued', worker_id = NULL,
                        processing_lease_until = NULL, last_heartbeat_at = NULL,
                        lease_epoch = 12
                    WHERE id = :id
                """),
                {"id": doc_id},
            )
            conn.commit()

    try:
        with engine.connect() as conn:
            doc_id = conn.execute(
                text("""
                    INSERT INTO documents
                        (owner_id, filename, file_path, file_type, file_size_bytes, status,
                         worker_id, lease_epoch, processing_lease_until, last_heartbeat_at, created_at, updated_at)
                    VALUES
                        ('default', 'stale-failure.pdf', :fp, '.pdf', 64, 'queued',
                         NULL, 10, NULL, NULL, NOW(), NOW())
                    RETURNING id
                """),
                {"fp": path},
            ).scalar()
            conn.execute(
                text("""
                    INSERT INTO task_outbox (document_id, task_name, status, attempts, created_at, next_attempt_at)
                    VALUES (:id, 'tasks.processing_tasks.process_document_task', 'pending', 0, NOW(), NOW())
                """),
                {"id": doc_id},
            )
            conn.commit()

        parser = patch("tasks.processing_tasks.DocumentParserService.extract_full_text")
        extractor = patch("tasks.processing_tasks.AIExtractorService.extract_invoice_data")
        embedder = patch("tasks.processing_tasks.VectorService.generate_embedding")
        with patch.object(settings, "WORKER_HEARTBEAT_INTERVAL_SECONDS", 0), parser as parse_mock, extractor as ai_mock, embedder as embed_mock:
            if failure_stage == "parser_exception":
                def fail_parser(_path):
                    simulate_takeover()
                    raise ValueError("simulated parser failure")
                parse_mock.side_effect = fail_parser
            elif failure_stage == "empty_text":
                def return_empty(_path):
                    simulate_takeover()
                    return ("", 0)
                parse_mock.side_effect = return_empty
            else:
                parse_mock.return_value = ("Invoice INV-TEST total 10.00 USD", 1)
                if failure_stage == "transient_max_retries":
                    def fail_ai(_raw_text):
                        simulate_takeover()
                        raise AITransientError("simulated transient provider failure")
                    ai_mock.side_effect = fail_ai
                else:
                    ai_mock.return_value = InvoiceExtractionSchema(
                        invoice_number="INV-TEST",
                        invoice_date="2024-06-01",
                        supplier_name="Test Supplier",
                        subtotal=Decimal("10.00"),
                        tax=Decimal("0.00"),
                        total_amount=Decimal("10.00"),
                        currency="USD",
                    )
                    def fail_embedding(_summary):
                        simulate_takeover()
                        raise RuntimeError("simulated unexpected embedding failure")
                    embed_mock.side_effect = fail_embedding

            if failure_stage == "transient_max_retries":
                with patch.object(process_document_task.request, "retries", 3), \
                     patch.object(process_document_task, "retry", side_effect=MaxRetriesExceededError()):
                    result = process_document_task(doc_id)
            else:
                result = process_document_task(doc_id)

        assert result is False
        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT status, worker_id, lease_epoch FROM documents WHERE id = :id"),
                {"id": doc_id},
            ).mappings().first()
            assert row["status"] == "queued"
            assert row["worker_id"] is None
            assert row["lease_epoch"] == 12

            outbox = conn.execute(
                text("SELECT status, last_error FROM task_outbox WHERE document_id = :id"),
                {"id": doc_id},
            ).mappings().first()
            assert outbox["status"] == "pending"
            assert outbox["last_error"] is None
    finally:
        if doc_id is not None:
            with engine.connect() as conn:
                conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": doc_id})
                conn.commit()
        engine.dispose()
        if os.path.exists(path):
            os.remove(path)


@pytest.mark.parametrize(
    "subtotal,total,expected",
    [
        (Decimal("10.00"), Decimal("10.00"), "pass"),
        (None, Decimal("10.00"), "not_evaluable"),
        (Decimal("10.00"), None, "not_evaluable"),
        (None, None, "not_evaluable"),
    ],
)
def test_ghr06_arithmetic_status_requires_both_essential_amounts(subtotal, total, expected):
    extracted = InvoiceExtractionSchema(subtotal=subtotal, total_amount=total)
    assert classify_arithmetic_status(extracted, []) == expected


def test_ghr06_arithmetic_errors_never_classify_as_pass():
    extracted = InvoiceExtractionSchema(subtotal=Decimal("10.00"), total_amount=Decimal("12.00"))
    assert classify_arithmetic_status(extracted, [object()]) == "fail"


def test_ghr01_celery_retry_releases_current_worker_lease_and_propagates():
    """A retry must free its own lease so the scheduled retry can claim the document."""
    engine = create_engine(settings.SYNC_DATABASE_URL)
    doc_id = None
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    with open(path, "wb") as f:
        f.write(b"%PDF-1.4\\n%celery-retry-release")

    try:
        with engine.connect() as conn:
            doc_id = conn.execute(
                text("""
                    INSERT INTO documents
                        (owner_id, filename, file_path, file_type, file_size_bytes, status,
                         worker_id, lease_epoch, processing_lease_until, last_heartbeat_at, created_at, updated_at)
                    VALUES
                        ('default', 'retry-release.pdf', :fp, '.pdf', 64, 'queued',
                         NULL, 4, NULL, NULL, NOW(), NOW())
                    RETURNING id
                """),
                {"fp": path},
            ).scalar()
            conn.commit()

        def transient_failure(_raw_text):
            raise AITransientError("simulated transient provider failure")

        with patch.object(settings, "WORKER_HEARTBEAT_INTERVAL_SECONDS", 0), \
             patch("tasks.processing_tasks.DocumentParserService.extract_full_text", return_value=("Invoice INV-RETRY total 10.00 USD", 1)), \
             patch("tasks.processing_tasks.AIExtractorService.extract_invoice_data", side_effect=transient_failure), \
             patch.object(process_document_task.request, "retries", 0), \
             patch.object(process_document_task, "retry", side_effect=Retry("scheduled")):
            with pytest.raises(Retry):
                process_document_task(doc_id)

        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT status, worker_id, lease_epoch, processing_lease_until, last_heartbeat_at FROM documents WHERE id = :id"),
                {"id": doc_id},
            ).mappings().first()
            assert row["status"] == "queued"
            assert row["worker_id"] is None
            assert row["lease_epoch"] == 5
            assert row["processing_lease_until"] is None
            assert row["last_heartbeat_at"] is None
    finally:
        if doc_id is not None:
            with engine.connect() as conn:
                conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": doc_id})
                conn.commit()
        engine.dispose()
        if os.path.exists(path):
            os.remove(path)
