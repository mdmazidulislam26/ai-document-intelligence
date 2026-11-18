"""
PostgreSQL & pgvector integration tests for Hybrid Search indexes.
"""

from decimal import Decimal
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.config import settings
from core.database import get_db
from main import app
from services.vector_service import VectorService

DEV_HEADERS = {"X-API-Key": "dev-local-api-key-change-me"}


@pytest.fixture
def seeded_search_data():
    engine = create_engine(settings.SYNC_DATABASE_URL)

    emb_cloud = VectorService.generate_embedding(
        "Supplier: TechFlow Solutions Ltd. Invoice: INV-IDX-8801. Cloud Server Hosting Cybersecurity Audit"
    )
    emb_office = VectorService.generate_embedding(
        "Supplier: SuperMart Express. Receipt: REC-IDX-7741. Office Supplies Packaging Paper"
    )

    emb_cloud_str = "[" + ",".join(map(str, emb_cloud)) + "]"
    emb_office_str = "[" + ",".join(map(str, emb_office)) + "]"

    inserted_doc_ids = []

    with engine.connect() as conn:
        conn.execute(text("""
            DELETE FROM documents
            WHERE file_path IN ('/tmp/idx_test_cloud_unique.pdf', '/tmp/idx_test_office_unique.png');
        """))

        res1 = conn.execute(text("""
            INSERT INTO documents (owner_id, filename, file_path, file_type, file_size_bytes, status, created_at, updated_at)
            VALUES ('default', 'idx_test_cloud.pdf', '/tmp/idx_test_cloud_unique.pdf', '.pdf', 2048, 'validated', NOW(), NOW())
            RETURNING id;
        """))
        doc1_id = res1.scalar()
        inserted_doc_ids.append(doc1_id)

        conn.execute(
            text("""
                INSERT INTO extracted_invoices
                    (document_id, invoice_number, supplier_name, customer_name, subtotal, tax, total_amount,
                     currency, line_items, is_manually_corrected, raw_text, embedding)
                VALUES
                    (:doc_id, 'INV-IDX-8801', 'TechFlow Solutions Ltd.', 'Apex Innovations Inc.', 500.00, 50.00, 550.00,
                     'USD', '[]'::jsonb, FALSE, 'Cloud Server Hosting and Cybersecurity Audit services', CAST(:emb AS vector))
            """),
            {"doc_id": doc1_id, "emb": emb_cloud_str},
        )

        res2 = conn.execute(text("""
            INSERT INTO documents (owner_id, filename, file_type, file_path, file_size_bytes, status, created_at, updated_at)
            VALUES ('default', 'idx_test_office.png', '.png', '/tmp/idx_test_office_unique.png', 1024, 'validated', NOW(), NOW())
            RETURNING id;
        """))
        doc2_id = res2.scalar()
        inserted_doc_ids.append(doc2_id)

        conn.execute(
            text("""
                INSERT INTO extracted_invoices
                    (document_id, invoice_number, supplier_name, customer_name, subtotal, tax, total_amount,
                     currency, line_items, is_manually_corrected, raw_text, embedding)
                VALUES
                    (:doc_id, 'REC-IDX-7741', 'SuperMart Express', 'John Doe', 150.00, 15.00, 165.00,
                     'USD', '[]'::jsonb, FALSE, 'Office Supplies and Packaging Paper purchase', CAST(:emb AS vector))
            """),
            {"doc_id": doc2_id, "emb": emb_office_str},
        )
        conn.commit()

    yield engine, inserted_doc_ids

    with engine.connect() as conn:
        for d_id in inserted_doc_ids:
            conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": d_id})
        conn.commit()
    engine.dispose()


def test_embedding_dimension_matches_db_column(seeded_search_data):
    engine, _ = seeded_search_data
    assert settings.EMBEDDING_DIMENSION == 384

    vec = VectorService.generate_embedding("Sample check")
    assert len(vec) == 384

    with engine.connect() as conn:
        type_str = conn.execute(text("""
            SELECT format_type(a.atttypid, a.atttypmod)
            FROM pg_attribute a
            JOIN pg_class c ON a.attrelid = c.oid
            WHERE c.relname = 'extracted_invoices'
              AND a.attname = 'embedding'
              AND NOT a.attisdropped
        """)).scalar()
        assert "vector(384)" in type_str


def test_gin_fts_and_hnsw_explain_plans(seeded_search_data):
    engine, _ = seeded_search_data
    query_vec = VectorService.generate_embedding("Cloud infrastructure hosting")
    vec_str = "[" + ",".join(map(str, query_vec)) + "]"

    with engine.connect() as conn:
        conn.execute(text("SET LOCAL enable_seqscan = off;"))

        fts_plan_rows = conn.execute(text("""
            EXPLAIN (ANALYZE, BUFFERS)
            SELECT e.document_id, ts_rank_cd(e.search_vector, plainto_tsquery('english', 'Cybersecurity')) AS rank
            FROM extracted_invoices e
            WHERE e.search_vector @@ plainto_tsquery('english', 'Cybersecurity')
        """)).scalars().all()
        fts_plan = "\n".join(fts_plan_rows)
        assert "idx_extracted_invoices_search_vector" in fts_plan

        hnsw_plan_rows = conn.execute(
            text("""
                EXPLAIN (ANALYZE, BUFFERS)
                SELECT e.document_id, (1 - (e.embedding <=> CAST(:vec AS vector))) AS sim
                FROM extracted_invoices e
                WHERE e.embedding IS NOT NULL
                ORDER BY e.embedding <=> CAST(:vec AS vector) ASC
                LIMIT 10
            """),
            {"vec": vec_str},
        ).scalars().all()
        hnsw_plan = "\n".join(hnsw_plan_rows)
        assert "idx_extracted_invoices_embedding_hnsw" in hnsw_plan


@pytest.mark.asyncio
async def test_hybrid_search_pg_integration_and_api(seeded_search_data):
    _, doc_ids = seeded_search_data
    cloud_doc_id = doc_ids[0]

    test_async_engine = create_async_engine(settings.DATABASE_URL)
    TestAsyncSession = async_sessionmaker(bind=test_async_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with TestAsyncSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    try:
        async with TestAsyncSession() as db:
            kw_exact = await VectorService.hybrid_search(db, "INV-IDX-8801", search_type="keyword", limit=10, owner_id="default")
            assert any(r["document_id"] == cloud_doc_id for r in kw_exact)
            assert kw_exact[0]["document_id"] == cloud_doc_id

            sem_res = await VectorService.hybrid_search(db, "internet server security", search_type="semantic", limit=10, owner_id="default")
            assert any(r["document_id"] == cloud_doc_id for r in sem_res)
            top_sem = next(r for r in sem_res if r["document_id"] == cloud_doc_id)
            assert 0.0 <= float(top_sem["score"]) <= 1.0

            hyb_res = await VectorService.hybrid_search(db, "TechFlow Cybersecurity", search_type="hybrid", limit=10, owner_id="default")
            assert len(hyb_res) >= 1
            assert hyb_res[0]["document_id"] == cloud_doc_id
            assert hyb_res[0]["match_type"] == "hybrid"
            assert hyb_res[0]["rrf_score"] > 0

            punct_res = await VectorService.hybrid_search(db, "--- ??? !!!", search_type="hybrid", limit=10, owner_id="default")
            assert isinstance(punct_res, list)

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get(
                "/api/search",
                params={"q": "INV-IDX-8801", "type": "hybrid", "limit": 5},
                headers=DEV_HEADERS,
            )
            assert resp.status_code == 200
            data = resp.json()
            assert len(data) >= 1
            assert data[0]["invoice_number"] == "INV-IDX-8801"
            assert Decimal(str(data[0]["total_amount"])) == Decimal("550.00")
    finally:
        app.dependency_overrides.clear()
        await test_async_engine.dispose()
