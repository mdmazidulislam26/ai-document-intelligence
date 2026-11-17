"""
Vector embedding generation and robust hybrid search service.
Implements PostgreSQL Full-Text Search (tsvector), FastEmbed cosine vector search,
and Reciprocal Rank Fusion (RRF) for deterministic, high-relevance hybrid ranking.
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
        # Clean text
        clean = " ".join(text_content[:2000].split())
        embeddings = list(model.embed([clean]))
        return embeddings[0].tolist()

    @classmethod
    async def execute_keyword_search(cls, db: AsyncSession, query_text: str, limit: int = 30) -> List[Dict[str, Any]]:
        """
        Executes full-text and pattern search on supplier, invoice number, customer, and raw text.
        """
        clean_q = query_text.strip()
        pattern = f"%{clean_q}%"

        # SQL combines exact/partial matching with full-text search ts_rank
        sql = text("""
            SELECT 
                d.id AS document_id,
                d.filename,
                d.status,
                e.supplier_name,
                e.invoice_number,
                e.total_amount,
                e.currency,
                (
                    CASE 
                        WHEN LOWER(e.invoice_number) = LOWER(:clean_q) THEN 10.0
                        WHEN LOWER(e.supplier_name) = LOWER(:clean_q) THEN 8.0
                        WHEN e.invoice_number ILIKE :pattern THEN 5.0
                        WHEN e.supplier_name ILIKE :pattern THEN 4.0
                        ELSE ts_rank_cd(
                            to_tsvector('english', coalesce(e.supplier_name,'') || ' ' || coalesce(e.invoice_number,'') || ' ' || coalesce(e.customer_name,'') || ' ' || coalesce(e.raw_text,'')),
                            plainto_tsquery('english', :clean_q)
                        )
                    END
                ) AS kw_score
            FROM documents d
            JOIN extracted_invoices e ON d.id = e.document_id
            WHERE 
                e.invoice_number ILIKE :pattern
                OR e.supplier_name ILIKE :pattern
                OR e.customer_name ILIKE :pattern
                OR d.filename ILIKE :pattern
                OR to_tsvector('english', coalesce(e.supplier_name,'') || ' ' || coalesce(e.invoice_number,'') || ' ' || coalesce(e.customer_name,'') || ' ' || coalesce(e.raw_text,'')) @@ plainto_tsquery('english', :clean_q)
            ORDER BY kw_score DESC, d.id ASC
            LIMIT :limit;
        """)

        res = await db.execute(sql, {"clean_q": clean_q, "pattern": pattern, "limit": limit})
        results = []
        for row in res.mappings():
            item = dict(row)
            if item.get("total_amount") is not None:
                item["total_amount"] = Decimal(str(item["total_amount"]))
            results.append(item)
        return results

    @classmethod
    async def execute_semantic_search(cls, db: AsyncSession, query_text: str, limit: int = 30) -> List[Dict[str, Any]]:
        """
        Executes dense vector cosine distance matching using pgvector and FastEmbed.
        """
        query_vector = cls.generate_embedding(query_text)
        vector_str = "[" + ",".join(map(str, query_vector)) + "]"

        sql = text("""
            SELECT 
                d.id AS document_id,
                d.filename,
                d.status,
                e.supplier_name,
                e.invoice_number,
                e.total_amount,
                e.currency,
                (1 - (e.embedding <=> :vector::vector)) AS sem_score
            FROM extracted_invoices e
            JOIN documents d ON d.id = e.document_id
            WHERE e.embedding IS NOT NULL
            ORDER BY e.embedding <=> :vector::vector ASC, d.id ASC
            LIMIT :limit;
        """)

        res = await db.execute(sql, {"vector": vector_str, "limit": limit})
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

        # 1. Process keyword ranks
        for rank_idx, doc in enumerate(keyword_results):
            doc_id = doc["document_id"]
            rank = rank_idx + 1
            kw_ranks[doc_id] = rank
            doc_map[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))

        # 2. Process semantic ranks
        for rank_idx, doc in enumerate(semantic_results):
            doc_id = doc["document_id"]
            rank = rank_idx + 1
            sem_ranks[doc_id] = rank
            if doc_id not in doc_map:
                doc_map[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))

        # 3. Sort by RRF score descending, tie-break by document_id
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
            # Similarity score display fallback
            doc_item["score"] = doc_item.get("sem_score") or doc_item.get("kw_score") or doc_item["rrf_score"]
            fused_results.append(doc_item)

        return fused_results

    @classmethod
    async def hybrid_search(
        cls,
        db: AsyncSession,
        query_text: str,
        search_type: str = "hybrid",
        limit: int = 15
    ) -> List[Dict[str, Any]]:
        """
        Unified search endpoint router supporting 'keyword', 'semantic', or 'hybrid' (RRF).
        """
        if not query_text or not query_text.strip():
            return []

        if search_type == "keyword":
            kw_res = await cls.execute_keyword_search(db, query_text, limit=limit)
            for idx, r in enumerate(kw_res):
                r["match_type"] = "keyword_only"
                r["keyword_rank"] = idx + 1
                r["score"] = r.get("kw_score", 1.0)
            return kw_res

        elif search_type == "semantic":
            sem_res = await cls.execute_semantic_search(db, query_text, limit=limit)
            for idx, r in enumerate(sem_res):
                r["match_type"] = "semantic_only"
                r["semantic_rank"] = idx + 1
                r["score"] = r.get("sem_score", 0.0)
            return sem_res

        else:  # 'hybrid' with RRF
            kw_res = await cls.execute_keyword_search(db, query_text, limit=30)
            sem_res = await cls.execute_semantic_search(db, query_text, limit=30)
            return cls.apply_reciprocal_rank_fusion(kw_res, sem_res, k=60, limit=limit)
