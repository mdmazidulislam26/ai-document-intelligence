"""
Comprehensive security tests covering:
1. Explicit CORS origin policy (rejects untrusted origins).
2. Unauthenticated rejection (401) and HMAC-signed Bearer token issuance/verification.
3. Cross-tenant authorization (owner_id isolation across documents, corrections, cross-verify, and both search branches).
4. ZIP/XLSX zip-bomb protection (entry count, uncompressed size, compression ratio, traversal entry).
5. Streaming upload size limit (413).
6. Rate limiting (429 Too Many Requests with Retry-After).
7. Sensitive invoice logging redaction.
"""

import io
import json
import uuid
import zipfile
import logging
from unittest.mock import patch, MagicMock
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.config import settings
from core.database import get_db
from core.rate_limit import RateLimiter
from main import app
from services.file_security import FileSecurityValidator
from services.ai_extractor import AIExtractorService, AIMalformedResponseError
from services.vector_service import VectorService

TENANT_A_KEY = "key-tenant-alpha-secret"
TENANT_B_KEY = "key-tenant-beta-secret"
TEST_KEYS_JSON = json.dumps({
    TENANT_A_KEY: {"owner_id": "tenant_alpha", "role": "user"},
    TENANT_B_KEY: {"owner_id": "tenant_beta", "role": "user"},
})


def test_zip_bomb_and_decompression_limits():
    """Rejects XLSX archives with excessive entry count, traversal path, or zip-bomb ratio."""
    buf_trav = io.BytesIO()
    with zipfile.ZipFile(buf_trav, "w") as z:
        z.writestr("../../evil.xml", "<data/>")
    valid_t, msg_t = FileSecurityValidator.validate_file_content(buf_trav.getvalue(), ".xlsx")
    assert valid_t is False
    assert "unsafe archive entry path" in msg_t.lower()

    buf_entries = io.BytesIO()
    with zipfile.ZipFile(buf_entries, "w") as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        for i in range(1005):
            z.writestr(f"xl/sheet_{i}.xml", "x")
    valid_e, msg_e = FileSecurityValidator.validate_file_content(buf_entries.getvalue(), ".xlsx")
    assert valid_e is False
    assert "entry count" in msg_e.lower()

    buf_bomb = io.BytesIO()
    with zipfile.ZipFile(buf_bomb, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("xl/worksheets/sheet1.xml", b"0" * (12 * 1024 * 1024))
    valid_b, msg_b = FileSecurityValidator.validate_file_content(buf_bomb.getvalue(), ".xlsx")
    assert valid_b is False
    assert "zip bomb" in msg_b.lower() or "ratio" in msg_b.lower()


@patch("services.ai_extractor.OpenAI")
def test_sensitive_invoice_data_not_logged_on_parse_error(mock_openai, caplog):
    """Ensures raw invoice text/numbers are never leaked into error logs."""
    mock_instance = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "CONFIDENTIAL_SUPPLIER_SECRET_ACME TOTAL_999888777 INVALID_JSON"
    mock_instance.chat.completions.create.return_value.choices = [mock_choice]
    mock_openai.return_value = mock_instance

    with caplog.at_level(logging.ERROR, logger="ai_extractor"), \
         patch("services.ai_extractor.settings.GROQ_API_KEY", "test_key"):
        svc = AIExtractorService()
        with pytest.raises(AIMalformedResponseError):
            svc.extract_from_chunk("Invoice text")

    assert "CONFIDENTIAL_SUPPLIER_SECRET_ACME" not in caplog.text
    assert "999888777" not in caplog.text


@pytest.mark.asyncio
async def test_cors_explicit_origins_policy():
    """Verifies configured origin is allowed while arbitrary evil origins are rejected."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        ok_resp = await client.options(
            "/api/health",
            headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET"},
        )
        assert ok_resp.headers.get("access-control-allow-origin") == "http://localhost:3000"

        evil_resp = await client.options(
            "/api/health",
            headers={"Origin": "https://evil-attacker.example.com", "Access-Control-Request-Method": "GET"},
        )
        assert "access-control-allow-origin" not in evil_resp.headers


@pytest.mark.asyncio
async def test_auth_cross_tenant_isolation_and_rate_limiting():
    """
    End-to-end security integration test:
    1. Enforces 401 without credentials and validates Bearer token issuance.
    2. Isolates Tenant A documents from Tenant B across GET, PUT /correct, /reprocess, /cross-verify, and /search.
    3. Enforces 413 on oversized upload and 429 on rate-limit exhaustion.
    """
    sync_engine = create_engine(settings.SYNC_DATABASE_URL)
    test_async_engine = create_async_engine(settings.DATABASE_URL)
    TestSession = async_sessionmaker(bind=test_async_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    RateLimiter.reset()

    doc_a_id = None
    doc_b_id = None
    secret_marker = f"SECRET-TENANT-A-{uuid.uuid4().hex[:8]}"

    try:
        emb_a = VectorService.generate_embedding(f"Tenant Alpha Confidential {secret_marker} Hosting")
        emb_a_str = "[" + ",".join(map(str, emb_a)) + "]"

        with sync_engine.connect() as conn:
            doc_a_id = conn.execute(
                text("""
                    INSERT INTO documents (owner_id, filename, file_path, file_type, file_size_bytes, status, created_at, updated_at)
                    VALUES ('tenant_alpha', 'alpha_secret.pdf', :fp, '.pdf', 500, 'validated', NOW(), NOW())
                    RETURNING id
                """),
                {"fp": f"/tmp/sec_a_{uuid.uuid4().hex}.pdf"},
            ).scalar()
            conn.execute(
                text("""
                    INSERT INTO extracted_invoices
                        (document_id, invoice_number, supplier_name, subtotal, tax, total_amount,
                         currency, line_items, is_manually_corrected, raw_text, embedding)
                    VALUES
                        (:doc_id, :inv, 'Alpha Secret Vendor', 100.00, 10.00, 110.00,
                         'USD', '[]'::jsonb, FALSE, :raw, CAST(:emb AS vector))
                """),
                {"doc_id": doc_a_id, "inv": secret_marker, "raw": f"Confidential {secret_marker}", "emb": emb_a_str},
            )

            doc_b_id = conn.execute(
                text("""
                    INSERT INTO documents (owner_id, filename, file_path, file_type, file_size_bytes, status, created_at, updated_at)
                    VALUES ('tenant_beta', 'beta_doc.pdf', :fp, '.pdf', 500, 'validated', NOW(), NOW())
                    RETURNING id
                """),
                {"fp": f"/tmp/sec_b_{uuid.uuid4().hex}.pdf"},
            ).scalar()
            conn.execute(
                text("""
                    INSERT INTO extracted_invoices
                        (document_id, invoice_number, supplier_name, subtotal, tax, total_amount,
                         currency, line_items, is_manually_corrected, raw_text)
                    VALUES
                        (:doc_id, 'INV-BETA-1', 'Beta Vendor', 50.00, 5.00, 55.00,
                         'USD', '[]'::jsonb, FALSE, 'Beta test document')
                """),
                {"doc_id": doc_b_id},
            )
            conn.commit()

        with patch.object(settings, "API_KEYS_JSON", TEST_KEYS_JSON):
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as client:
                assert (await client.get("/api/documents")).status_code == 401
                assert (await client.get(f"/api/documents/{doc_a_id}")).status_code == 401
                assert (await client.get("/api/search", params={"q": secret_marker})).status_code == 401

                tok_resp = await client.post("/api/auth/token", headers={"X-API-Key": TENANT_A_KEY})
                assert tok_resp.status_code == 200
                token_a = tok_resp.json()["access_token"]
                headers_a_bearer = {"Authorization": f"Bearer {token_a}"}
                headers_b = {"X-API-Key": TENANT_B_KEY}

                assert (await client.get(f"/api/documents/{doc_a_id}", headers=headers_a_bearer)).status_code == 200
                assert (await client.get(f"/api/documents/{doc_a_id}", headers={"Authorization": f"Bearer {token_a}x"})).status_code == 401

                assert (await client.get(f"/api/documents/{doc_a_id}", headers=headers_b)).status_code == 403
                assert (await client.get(f"/api/documents/{doc_a_id}/status", headers=headers_b)).status_code == 403
                assert (await client.put(f"/api/documents/{doc_a_id}/correct", json={"currency": "EUR"}, headers=headers_b)).status_code == 403
                assert (await client.post(f"/api/documents/{doc_a_id}/reprocess", headers=headers_b)).status_code == 403
                assert (await client.post(
                    f"/api/documents/{doc_b_id}/cross-verify",
                    json={"reference_document_id": doc_a_id},
                    headers=headers_b,
                )).status_code == 403

                list_b = await client.get("/api/documents", headers=headers_b)
                assert list_b.status_code == 200
                assert all(d["id"] != doc_a_id for d in list_b.json())

                for mode in ("keyword", "semantic", "hybrid"):
                    search_b = await client.get(
                        "/api/search",
                        params={"q": secret_marker, "type": mode},
                        headers=headers_b,
                    )
                    assert search_b.status_code == 200
                    assert all(r["document_id"] != doc_a_id for r in search_b.json())

                with patch.object(settings, "MAX_UPLOAD_SIZE_MB", 1):
                    oversized = b"%PDF-1.4\n" + (b"A" * (1024 * 1024 + 100))
                    r_big = await client.post(
                        "/api/documents/upload",
                        files=[("files", ("big.pdf", oversized, "application/pdf"))],
                        headers=headers_a_bearer,
                    )
                    assert r_big.status_code == 413

                RateLimiter.reset()
                with patch.object(settings, "RATE_LIMIT_SEARCH_PER_MIN", 2):
                    r1 = await client.get("/api/search", params={"q": "test"}, headers=headers_b)
                    r2 = await client.get("/api/search", params={"q": "test"}, headers=headers_b)
                    r3 = await client.get("/api/search", params={"q": "test"}, headers=headers_b)
                    assert r1.status_code == 200
                    assert r2.status_code == 200
                    assert r3.status_code == 429
                    assert "retry-after" in {k.lower() for k in r3.headers.keys()}
    finally:
        RateLimiter.reset()
        app.dependency_overrides.clear()
        await test_async_engine.dispose()
        with sync_engine.connect() as conn:
            for d_id in (doc_a_id, doc_b_id):
                if d_id is not None:
                    conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": d_id})
            conn.commit()
        sync_engine.dispose()
