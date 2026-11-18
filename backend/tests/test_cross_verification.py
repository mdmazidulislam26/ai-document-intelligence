"""
End-to-end integration tests for PDF-to-PDF and PDF-to-Excel/CSV cross-verification APIs.
"""

import os
import uuid
import tempfile
from decimal import Decimal
from datetime import date
import pandas as pd
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.config import settings
from core.database import get_db
from main import app

DEV_HEADERS = {"X-API-Key": "dev-local-api-key-change-me"}


@pytest.fixture
def cross_verify_fixtures():
    engine = create_engine(settings.SYNC_DATABASE_URL)
    created_doc_ids = []
    temp_files = []

    csv_fd, csv_path = tempfile.mkstemp(suffix=".csv")
    os.close(csv_fd)
    with open(csv_path, "w") as f:
        f.write(
            "Invoice Number,Invoice Date,Supplier,Customer,Subtotal,Tax,Total Amount,Currency\n"
            "INV-CV-1001,2024-05-10,Alpha Tech Ltd.,Enterprise Corp,1000.00,100.00,1100.00,USD\n"
            "INV-CV-1002,2024-05-11,Beta Logistics,Enterprise Corp,450.00,45.00,495.00,USD\n"
        )
    temp_files.append(csv_path)

    xlsx_fd, xlsx_path = tempfile.mkstemp(suffix=".xlsx")
    os.close(xlsx_fd)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        pd.DataFrame([{"Invoice Number": "INV-OTHER-1", "Supplier": "Other", "Total Amount": 99.00}]).to_excel(
            writer, sheet_name="Summary", index=False
        )
        pd.DataFrame([
            {
                "Invoice Number": "INV-CV-1001",
                "Supplier": "Alpha Tech Ltd.",
                "Customer": "Enterprise Corp",
                "Subtotal": 1000.00,
                "Tax": 100.00,
                "Total Amount": 1100.00,
                "Currency": "USD",
            }
        ]).to_excel(writer, sheet_name="Q2_Ledger", index=False)
    temp_files.append(xlsx_path)

    def _insert_doc(filename, file_path, file_type, status="validated"):
        with engine.connect() as conn:
            doc_id = conn.execute(
                text("""
                    INSERT INTO documents (owner_id, filename, file_path, file_type, file_size_bytes, status, created_at, updated_at)
                    VALUES ('default', :fn, :fp, :ft, 512, :st, NOW(), NOW())
                    RETURNING id
                """),
                {"fn": filename, "fp": file_path, "ft": file_type, "st": status},
            ).scalar()
            conn.commit()
            created_doc_ids.append(doc_id)
            return doc_id

    def _insert_invoice(doc_id, inv_num, supplier, customer, sub, tax, tot, curr="USD", items="[]"):
        with engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO extracted_invoices
                        (document_id, invoice_number, invoice_date, supplier_name, customer_name,
                         subtotal, tax, total_amount, currency, line_items, is_manually_corrected)
                    VALUES
                        (:doc_id, :inv, :dt, :sup, :cust, :sub, :tax, :tot, :curr, CAST(:items AS jsonb), FALSE)
                """),
                {
                    "doc_id": doc_id,
                    "inv": inv_num,
                    "dt": date(2024, 5, 10),
                    "sup": supplier,
                    "cust": customer,
                    "sub": sub,
                    "tax": tax,
                    "tot": tot,
                    "curr": curr,
                    "items": items,
                },
            )
            conn.commit()

    pdf_match_id = _insert_doc("primary_match.pdf", f"/tmp/cv_{uuid.uuid4().hex}.pdf", ".pdf")
    _insert_invoice(
        pdf_match_id,
        "INV-CV-1001",
        "Alpha Tech Ltd.",
        "Enterprise Corp",
        Decimal("1000.00"),
        Decimal("100.00"),
        Decimal("1100.00"),
        "USD",
        '[{"description": "Cloud Cluster", "quantity": 1, "unit_price": 1000.00, "total": 1000.00}]',
    )

    pdf_mismatch_id = _insert_doc("ref_mismatch.pdf", f"/tmp/cv_{uuid.uuid4().hex}.pdf", ".pdf")
    _insert_invoice(
        pdf_mismatch_id,
        "INV-CV-1001",
        "Alpha Tech Ltd.",
        "Different Client LLC",
        Decimal("900.00"),
        Decimal("90.00"),
        Decimal("990.00"),
        "EUR",
        '[{"description": "Cloud Cluster", "quantity": 1, "unit_price": 450.00, "total": 450.00},'
        ' {"description": "Support", "quantity": 1, "unit_price": 450.00, "total": 450.00}]',
    )

    pdf_missing_id = _insert_doc("missing_in_ledger.pdf", f"/tmp/cv_{uuid.uuid4().hex}.pdf", ".pdf")
    _insert_invoice(
        pdf_missing_id,
        "INV-UNKNOWN-9999",
        "Unknown Vendor",
        "Enterprise Corp",
        Decimal("200.00"),
        Decimal("20.00"),
        Decimal("220.00"),
    )

    csv_ref_id = _insert_doc("ledger.csv", csv_path, ".csv")
    xlsx_ref_id = _insert_doc("ledger.xlsx", xlsx_path, ".xlsx")
    unprocessed_id = _insert_doc("queued_doc.pdf", f"/tmp/cv_{uuid.uuid4().hex}.pdf", ".pdf", status="queued")

    yield {
        "engine": engine,
        "pdf_match_id": pdf_match_id,
        "pdf_mismatch_id": pdf_mismatch_id,
        "pdf_missing_id": pdf_missing_id,
        "csv_ref_id": csv_ref_id,
        "xlsx_ref_id": xlsx_ref_id,
        "unprocessed_id": unprocessed_id,
    }

    with engine.connect() as conn:
        for d_id in created_doc_ids:
            conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": d_id})
        conn.commit()
    engine.dispose()
    for path in temp_files:
        if os.path.exists(path):
            os.remove(path)


@pytest.mark.asyncio
async def test_pdf_to_csv_and_xlsx_cross_verification_match(cross_verify_fixtures):
    fx = cross_verify_fixtures
    test_engine = create_async_engine(settings.DATABASE_URL)
    TestSession = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp_csv = await client.post(
                f"/api/documents/{fx['pdf_match_id']}/cross-verify",
                json={"reference_document_id": fx["csv_ref_id"]},
                headers=DEV_HEADERS,
            )
            assert resp_csv.status_code == 200
            data_csv = resp_csv.json()
            assert data_csv["verification_mode"] == "pdf_to_spreadsheet"
            assert data_csv["overall_status"] == "matched"
            assert data_csv["discrepancy_count"] == 0

            resp_xlsx = await client.post(
                f"/api/documents/{fx['pdf_match_id']}/cross-verify",
                json={"reference_document_id": fx["xlsx_ref_id"]},
                headers=DEV_HEADERS,
            )
            assert resp_xlsx.status_code == 200
            assert resp_xlsx.json()["overall_status"] == "matched"

            hist_resp = await client.get(
                f"/api/documents/{fx['pdf_match_id']}/cross-verify/history",
                headers=DEV_HEADERS,
            )
            assert hist_resp.status_code == 200
            assert len(hist_resp.json()) >= 2
    finally:
        app.dependency_overrides.clear()
        await test_engine.dispose()


@pytest.mark.asyncio
async def test_pdf_to_pdf_mismatch_updates_validation_and_status(cross_verify_fixtures):
    fx = cross_verify_fixtures
    test_engine = create_async_engine(settings.DATABASE_URL)
    TestSession = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post(
                f"/api/documents/{fx['pdf_match_id']}/cross-verify",
                json={"reference_document_id": fx["pdf_mismatch_id"]},
                headers=DEV_HEADERS,
            )
            assert resp.status_code == 200
            data = resp.json()
            assert data["verification_mode"] == "pdf_to_pdf"
            assert data["overall_status"] == "mismatched"
            assert data["discrepancy_count"] >= 5

            doc_resp = await client.get(f"/api/documents/{fx['pdf_match_id']}", headers=DEV_HEADERS)
            assert doc_resp.status_code == 200
            assert doc_resp.json()["status"] == "requires_manual_review"
    finally:
        app.dependency_overrides.clear()
        await test_engine.dispose()


@pytest.mark.asyncio
async def test_cross_verify_missing_and_invalid_inputs(cross_verify_fixtures):
    fx = cross_verify_fixtures
    test_engine = create_async_engine(settings.DATABASE_URL)
    TestSession = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            r_miss = await client.post(
                f"/api/documents/{fx['pdf_missing_id']}/cross-verify",
                json={"reference_document_id": fx["csv_ref_id"]},
                headers=DEV_HEADERS,
            )
            assert r_miss.status_code == 200
            assert r_miss.json()["overall_status"] == "missing_in_reference"

            r_self = await client.post(
                f"/api/documents/{fx['pdf_match_id']}/cross-verify",
                json={"reference_document_id": fx["pdf_match_id"]},
                headers=DEV_HEADERS,
            )
            assert r_self.status_code == 400

            r_inc = await client.post(
                f"/api/documents/{fx['unprocessed_id']}/cross-verify",
                json={"reference_document_id": fx["csv_ref_id"]},
                headers=DEV_HEADERS,
            )
            assert r_inc.status_code == 400

            r_404 = await client.post(
                "/api/documents/999999/cross-verify",
                json={"reference_document_id": fx["csv_ref_id"]},
                headers=DEV_HEADERS,
            )
            assert r_404.status_code == 404
    finally:
        app.dependency_overrides.clear()
        await test_engine.dispose()
