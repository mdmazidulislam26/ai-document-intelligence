"""
Vector embedding generation and robust hybrid search service.
Uses stored generated tsvector + GIN index for Full-Text Search,
pgvector HNSW cosine distance index for dense semantic search,
Reciprocal Rank Fusion (RRF), and strict owner_id scoping across both branches.
"""

import logging
from typing import List, Dict, Any, Optional
from decimal import Decimal
from fastembed import TextEmbedding
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from core.config import settings

logger = logging.getLogger("vector_service")
logger.setLevel(logging.INFO)


class VectorService:
    _model_instance: Optional[TextEmbedding] = None

    @classmethod
    def get_model(cls) -> TextEmbedding:
        if cls._model_instance is None:
            cls._model_instance = TextEmbedding(model_name=settings.EMBEDDING_MODEL_NAME)
        return cls._model_instance

    @classmethod
    def generate_embedding(cls, text_content: str) -> List[float]:
        if not text_content or not text_content.strip():
            return [0.0] * settings.EMBEDDING_DIMENSION
        model = cls.get_model()
        clean = " ".join(text_content[:2000].split())
        embeddings = list(model.embed([clean]))
        return embeddings[0].tolist()

    @classmethod
    async def execute_keyword_search(
        cls,
        db: AsyncSession,
        query_text: str,
        limit: int = 30,
        owner_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Executes index-compatible Full-Text Search using the stored 'search_vector' GIN index
        with owner_id authorization scoping.
        """
        clean_q = query_text.strip()
        if not clean_q:
            return []
        pattern = f"%{clean_q}%"

        sql = text("""
            WITH fts_hits AS (
                SELECT
                    e.document_id,
                    ts_rank_cd(e.search_vector, plainto_tsquery('english', :clean_q)) AS fts_score
                FROM extracted_invoices e
                JOIN documents d ON d.id = e.document_id
                WHERE e.search_vector @@ plainto_tsquery('english', :clean_q)
                  AND (CAST(:owner_id AS varchar) IS NULL OR d.owner_id = CAST(:owner_id AS varchar))
            ),
            identifier_hits AS (
                SELECT
                    e.document_id,
                    CASE
                        WHEN LOWER(e.invoice_number) = LOWER(:clean_q) THEN 10.0
                        WHEN LOWER(e.supplier_name) = LOWER(:clean_q) THEN 8.0
                        WHEN e.invoice_number ILIKE :pattern THEN 5.0
                        WHEN e.supplier_name ILIKE :pattern THEN 4.0
                        WHEN e.customer_name ILIKE :pattern THEN 3.0
                        ELSE 1.5
                    END AS id_score
                FROM extracted_invoices e
                JOIN documents d ON d.id = e.document_id
                WHERE (CAST(:owner_id AS varchar) IS NULL OR d.owner_id = CAST(:owner_id AS varchar))
                  AND (
                      LOWER(e.invoice_number) = LOWER(:clean_q)
                      OR LOWER(e.supplier_name) = LOWER(:clean_q)
                      OR e.invoice_number ILIKE :pattern
                      OR e.supplier_name ILIKE :pattern
                      OR e.customer_name ILIKE :pattern
                      OR d.filename ILIKE :pattern
                  )
            ),
            combined AS (
                SELECT
                    COALESCE(f.document_id, i.document_id) AS document_id,
                    GREATEST(COALESCE(i.id_score, 0.0), COALESCE(f.fts_score, 0.0)) AS kw_score
                FROM fts_hits f
                FULL OUTER JOIN identifier_hits i ON f.document_id = i.document_id
            )
            SELECT
                d.id AS document_id,
                d.filename,
                d.status,
                e.supplier_name,
                e.invoice_number,
                e.total_amount,
                e.currency,
                c.kw_score
            FROM combined c
            JOIN documents d ON d.id = c.document_id
            JOIN extracted_invoices e ON e.document_id = c.document_id
            ORDER BY c.kw_score DESC, d.id ASC
            LIMIT :limit;
        """)

        res = await db.execute(sql, {"clean_q": clean_q, "pattern": pattern, "limit": limit, "owner_id": owner_id})
        results = []
        for row in res.mappings():
            item = dict(row)
            if item.get("total_amount") is not None:
                item["total_amount"] = Decimal(str(item["total_amount"]))
            results.append(item)
        return results

    @classmethod
    async def execute_semantic_search(
        cls,
        db: AsyncSession,
        query_text: str,
        limit: int = 30,
        owner_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Executes dense vector cosine distance matching using pgvector HNSW index
        with owner_id authorization scoping so unauthorized documents never leak.
        """
        clean_q = query_text.strip()
        if not clean_q:
            return []

        query_vector = cls.generate_embedding(clean_q)
        if not any(v != 0.0 for v in query_vector):
            return []

        vector_str = "[" + ",".join(map(str, query_vector)) + "]"
        candidate_limit = max(limit * 2, limit)

        sql = text("""
            WITH top_semantic AS (
                SELECT
                    e.document_id,
                    d.filename,
                    d.status,
                    e.supplier_name,
                    e.invoice_number,
                    e.total_amount,
                    e.currency,
                    (1 - (e.embedding <=> CAST(:vector AS vector))) AS sem_score
                FROM extracted_invoices e
                JOIN documents d ON d.id = e.document_id
                WHERE e.embedding IS NOT NULL
                  AND (CAST(:owner_id AS varchar) IS NULL OR d.owner_id = CAST(:owner_id AS varchar))
                ORDER BY e.embedding <=> CAST(:vector AS vector) ASC
                LIMIT :candidate_limit
            )
            SELECT
                document_id,
                filename,
                status,
                supplier_name,
                invoice_number,
                total_amount,
                currency,
                sem_score
            FROM top_semantic
            ORDER BY sem_score DESC, document_id ASC
            LIMIT :limit;
        """)

        res = await db.execute(
            sql,
            {"vector": vector_str, "candidate_limit": candidate_limit, "limit": limit, "owner_id": owner_id},
        )
        results = []
        for row in res.mappings():
            item = dict(row)
            if item.get("total_amount") is not None:
                item["total_amount"] = Decimal(str(item["total_amount"]))
            results.append(item)
        return results

    @classmethod
    def apply_reciprocal_rank_fusion(
        cls,
        keyword_results: List[Dict[str, Any]],
        semantic_results: List[Dict[str, Any]],
        k: int = 60,
        limit: int = 15
    ) -> List[Dict[str, Any]]:
        """
        Fuses keyword and semantic ranked lists using standard Reciprocal Rank Fusion:
        RRF_score(d) = sum(1 / (k + rank_i(d)))
        """
        doc_map = {}
        rrf_scores = {}
        kw_ranks = {}
        sem_ranks = {}

        for rank_idx, doc in enumerate(keyword_results):
            doc_id = doc["document_id"]
            rank = rank_idx + 1
            kw_ranks[doc_id] = rank
            doc_map[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))

        for rank_idx, doc in enumerate(semantic_results):
            doc_id = doc["document_id"]
            rank = rank_idx + 1
            sem_ranks[doc_id] = rank
            if doc_id not in doc_map:
                doc_map[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))

        sorted_doc_ids = sorted(
            doc_map.keys(),
            key=lambda d_id: (rrf_scores[d_id], -d_id),
            reverse=True
        )

        fused_results = []
        for d_id in sorted_doc_ids[:limit]:
            doc_item = dict(doc_map[d_id])
            has_kw = d_id in kw_ranks
            has_sem = d_id in sem_ranks

            if has_kw and has_sem:
                match_type = "hybrid"
            elif has_kw:
                match_type = "keyword_only"
            else:
                match_type = "semantic_only"

            doc_item["match_type"] = match_type
            doc_item["keyword_rank"] = kw_ranks.get(d_id)
            doc_item["semantic_rank"] = sem_ranks.get(d_id)
            doc_item["rrf_score"] = round(float(rrf_scores[d_id]), 6)
            doc_item["score"] = doc_item.get("sem_score") or doc_item.get("kw_score") or doc_item["rrf_score"]
            fused_results.append(doc_item)

        return fused_results

    @classmethod
    async def hybrid_search(
        cls,
        db: AsyncSession,
        query_text: str,
        search_type: str = "hybrid",
        limit: int = 15,
        owner_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Unified search router supporting 'keyword', 'semantic', or 'hybrid' (RRF)
        with strict owner_id scoping.
        """
        if not query_text or not query_text.strip():
            return []

        if search_type == "keyword":
            kw_res = await cls.execute_keyword_search(db, query_text, limit=limit, owner_id=owner_id)
            for idx, r in enumerate(kw_res):
                r["match_type"] = "keyword_only"
                r["keyword_rank"] = idx + 1
                r["score"] = r.get("kw_score", 1.0)
            return kw_res

        elif search_type == "semantic":
            sem_res = await cls.execute_semantic_search(db, query_text, limit=limit, owner_id=owner_id)
            for idx, r in enumerate(sem_res):
                r["match_type"] = "semantic_only"
                r["semantic_rank"] = idx + 1
                r["score"] = r.get("sem_score", 0.0)
            return sem_res

        else:
            kw_res = await cls.execute_keyword_search(db, query_text, limit=30, owner_id=owner_id)
            sem_res = await cls.execute_semantic_search(db, query_text, limit=30, owner_id=owner_id)
            return cls.apply_reciprocal_rank_fusion(kw_res, sem_res, k=60, limit=limit)
