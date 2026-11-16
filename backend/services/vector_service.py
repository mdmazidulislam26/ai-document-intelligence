"""
Vector embedding generation and robust hybrid search service.
"""

import logging
from typing import List, Optional
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
        embeddings = list(model.embed([text_content[:4000]]))
        return embeddings[0].tolist()

    @classmethod
    async def hybrid_search(
        cls,
        db: AsyncSession,
        query_text: str,
        search_type: str = "hybrid",
        limit: int = 15
    ) -> List[dict]:
        clean_q = f"%{query_text.strip()}%"
        results = []

        # 1. Keyword-based matching
        if search_type in ["keyword", "hybrid"]:
            sql_kw = text("""
                SELECT 
                    d.id AS document_id,
                    d.filename,
                    d.status,
                    e.supplier_name,
                    e.invoice_number,
                    e.total_amount,
                    1.0 AS score
                FROM documents d
                LEFT JOIN extracted_invoices e ON d.id = e.document_id
                WHERE 
                    e.supplier_name ILIKE :q
                    OR e.invoice_number ILIKE :q
                    OR d.filename ILIKE :q
                    OR e.raw_text ILIKE :q
                LIMIT :limit;
            """)
            res_kw = await db.execute(sql_kw, {"q": clean_q, "limit": limit})
            for row in res_kw.mappings():
                results.append(dict(row))

        # 2. Semantic matching if requested or if keyword yields few results
        if search_type in ["semantic", "hybrid"]:
            try:
                query_vector = cls.generate_embedding(query_text)
                vector_str = "[" + ",".join(map(str, query_vector)) + "]"
                sql_sem = text("""
                    SELECT 
                        d.id AS document_id,
                        d.filename,
                        d.status,
                        e.supplier_name,
                        e.invoice_number,
                        e.total_amount,
                        (1 - (e.embedding <=> :vector::vector)) AS score
                    FROM extracted_invoices e
                    JOIN documents d ON d.id = e.document_id
                    WHERE e.embedding IS NOT NULL
                    ORDER BY e.embedding <=> :vector::vector ASC
                    LIMIT :limit;
                """)
                res_sem = await db.execute(sql_sem, {"vector": vector_str, "limit": limit})
                for row in res_sem.mappings():
                    # Deduplicate if already present from keyword
                    if not any(r["document_id"] == row["document_id"] for r in results):
                        results.append(dict(row))
            except Exception as e:
                logger.error(f"Semantic search query error: {e}")

        return results[:limit]
