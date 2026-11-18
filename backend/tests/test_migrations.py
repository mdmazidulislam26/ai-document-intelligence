"""
Unit and PostgreSQL integration tests for Alembic database migrations.
"""

import os
from datetime import datetime, date
from decimal import Decimal
import pytest
from sqlalchemy import create_engine, text, inspect
from alembic import command
from alembic.config import Config as AlembicConfig
from alembic.script import ScriptDirectory

from core.config import settings
import models.document  # noqa: F401


BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALEMBIC_INI = os.path.join(BACKEND_DIR, "alembic.ini")
ALEMBIC_DIR = os.path.join(BACKEND_DIR, "alembic")


def _get_alembic_config() -> AlembicConfig:
    cfg = AlembicConfig(ALEMBIC_INI)
    cfg.set_main_option("script_location", ALEMBIC_DIR)
    cfg.set_main_option("sqlalchemy.url", settings.SYNC_DATABASE_URL.replace("%", "%%"))
    return cfg


def test_alembic_script_directory_integrity():
    """Unit test: verifies linear migration history with a single head."""
    cfg = _get_alembic_config()
    script = ScriptDirectory.from_config(cfg)
    heads = script.get_heads()
    assert len(heads) == 1
    assert heads[0] == "0006_security_owner_scope"

    revisions = list(script.walk_revisions())
    assert len(revisions) >= 6


@pytest.fixture
def isolated_pg_schema():
    schema_name = "test_alembic_isolated"
    engine = create_engine(settings.SYNC_DATABASE_URL)

    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector SCHEMA public;"))
        conn.execute(text(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"))
        conn.execute(text(f"CREATE SCHEMA {schema_name};"))
        conn.commit()

    yield engine, schema_name

    with engine.connect() as conn:
        conn.execute(text(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;"))
        conn.commit()
    engine.dispose()


def test_clean_database_upgrade_and_schema_parity(isolated_pg_schema):
    engine, schema_name = isolated_pg_schema
    cfg = _get_alembic_config()

    with engine.connect() as conn:
        conn.execute(text(f"SET search_path TO {schema_name}, public;"))
        conn.commit()

        cfg.attributes["connection"] = conn
        cfg.attributes["version_table_schema"] = schema_name
        command.upgrade(cfg, "head")
        conn.commit()

        inspector = inspect(conn)
        assert inspector.has_table("documents", schema=schema_name)
        assert inspector.has_table("extracted_invoices", schema=schema_name)
        assert inspector.has_table("validation_logs", schema=schema_name)
        assert inspector.has_table("cross_verification_history", schema=schema_name)
        assert inspector.has_table("task_outbox", schema=schema_name)
        assert inspector.has_table("alembic_version", schema=schema_name)

        doc_cols = {c["name"] for c in inspector.get_columns("documents", schema=schema_name)}
        assert "owner_id" in doc_cols
        doc_idx = {i["name"] for i in inspector.get_indexes("documents", schema=schema_name)}
        assert "ix_documents_owner_id" in doc_idx

        col_rows = conn.execute(
            text("""
                SELECT column_name, data_type, numeric_precision, numeric_scale
                FROM information_schema.columns
                WHERE table_schema = :schema
                  AND table_name = 'extracted_invoices'
            """),
            {"schema": schema_name},
        ).mappings()
        cols = {r["column_name"]: dict(r) for r in col_rows}

        for money_col in ["subtotal", "tax", "total_amount"]:
            assert cols[money_col]["data_type"] == "numeric"
            assert cols[money_col]["numeric_precision"] == 12
            assert cols[money_col]["numeric_scale"] == 2

        assert cols["invoice_date"]["data_type"] == "date"
        assert cols["search_vector"]["data_type"] == "tsvector"
        assert cols["embedding"]["data_type"] == "USER-DEFINED"


def test_legacy_database_upgrade_and_rollback_preserves_data(isolated_pg_schema):
    engine, schema_name = isolated_pg_schema
    cfg = _get_alembic_config()

    with engine.connect() as conn:
        conn.execute(text(f"SET search_path TO {schema_name}, public;"))

        conn.execute(text("""
            CREATE TABLE documents (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                file_path VARCHAR(512) NOT NULL UNIQUE,
                file_type VARCHAR(32) NOT NULL,
                file_size_bytes INTEGER NOT NULL DEFAULT 0,
                status VARCHAR(64) NOT NULL DEFAULT 'queued',
                error_message TEXT,
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
            CREATE TABLE extracted_invoices (
                id SERIAL PRIMARY KEY,
                document_id INTEGER NOT NULL UNIQUE REFERENCES documents(id) ON DELETE CASCADE,
                invoice_number VARCHAR(128),
                invoice_date TIMESTAMP,
                supplier_name VARCHAR(255),
                customer_name VARCHAR(255),
                subtotal DOUBLE PRECISION,
                tax DOUBLE PRECISION,
                total_amount DOUBLE PRECISION,
                currency VARCHAR(16),
                line_items JSONB NOT NULL DEFAULT '[]'::jsonb,
                is_manually_corrected BOOLEAN NOT NULL DEFAULT FALSE,
                raw_text TEXT,
                embedding vector(384)
            );
            CREATE TABLE validation_logs (
                id SERIAL PRIMARY KEY,
                document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
                rule_name VARCHAR(128) NOT NULL,
                error_description TEXT NOT NULL,
                severity VARCHAR(32) NOT NULL DEFAULT 'WARNING',
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """))

        conn.execute(text("""
            INSERT INTO documents (id, filename, file_path, file_type, file_size_bytes, status)
            VALUES (1, 'legacy_inv.pdf', '/tmp/legacy_inv.pdf', '.pdf', 1024, 'validated');
        """))
        conn.execute(text("""
            INSERT INTO extracted_invoices
                (document_id, invoice_number, invoice_date, supplier_name, subtotal, tax, total_amount, currency, raw_text)
            VALUES
                (1, 'INV-LEGACY-1', '2024-05-15 14:30:00', 'Legacy Corp', 123.456, 12.344, 135.80, 'USD', 'Cloud Hosting Fee');
        """))
        conn.commit()

        cfg.attributes["connection"] = conn
        cfg.attributes["version_table_schema"] = schema_name
        command.upgrade(cfg, "head")
        conn.commit()

        row = conn.execute(text("""
            SELECT d.owner_id, e.invoice_number, e.invoice_date, e.subtotal, e.tax, e.total_amount,
                   e.search_vector::text AS sv
            FROM extracted_invoices e
            JOIN documents d ON d.id = e.document_id
            WHERE e.document_id = 1
        """)).mappings().first()

        assert row["owner_id"] == "default"
        assert row["invoice_number"] == "INV-LEGACY-1"
        assert row["invoice_date"] == date(2024, 5, 15)
        assert row["subtotal"] == Decimal("123.46")
        assert row["tax"] == Decimal("12.34")
        assert row["total_amount"] == Decimal("135.80")

        command.downgrade(cfg, "0002_financial_precision")
        conn.commit()

        row_down2 = conn.execute(text("SELECT total_amount FROM extracted_invoices WHERE document_id = 1")).scalar()
        assert row_down2 == Decimal("135.80")

        command.downgrade(cfg, "0001_initial_schema")
        conn.commit()

        row_down1 = conn.execute(text("""
            SELECT invoice_date, total_amount
            FROM extracted_invoices
            WHERE document_id = 1
        """)).mappings().first()
        assert isinstance(row_down1["invoice_date"], datetime)
        assert abs(row_down1["total_amount"] - 135.80) < 0.001

        command.upgrade(cfg, "head")
        conn.commit()

        row_reup = conn.execute(text("SELECT total_amount FROM extracted_invoices WHERE document_id = 1")).scalar()
        assert row_reup == Decimal("135.80")
