"""
Vector embedding generation and pgvector hybrid search service.
Uses FastEmbed locally on CPU (100% free, zero external API cost).
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
    """
    Manages vector embeddings and hybrid similarity queries.
    """
    _model_instance: Optional[TextEmbedding] = None

    @classmethod
    def get_model(cls) -> TextEmbedding:
        """
        Lazily initializes and caches the FastEmbed model singleton.
        """
        if cls._model_instance is None:
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL_NAME}")
            cls._model_instance = TextEmbedding(model_name=settings.EMBEDDING_MODEL_NAME)
        return cls._model_instance

    @classmethod
    def generate_embedding(cls, text_content: str) -> List[float]:
        """
        Generates a 384-dimensional dense vector embedding from text.
        """
        if not text_content or not text_content.strip():
            return [0.0] * settings.EMBEDDING_DIMENSION

        model = cls.get_model()
        # FastEmbed returns an iterator of numpy ndarrays
        embeddings = list(model.embed([text_content[:4000]]))
        return embeddings[0].tolist()

    @classmethod
    async def hybrid_search(
        cls,
        db: AsyncSession,
        query_text: str,
        search_type: str = "hybrid",
        limit: int = 10
    ) -> List[dict]:
        """
        Executes Keyword, Semantic (Cosine Distance), or Hybrid Search
        over the documents and extracted_invoices tables.
        """
        results = []

        if search_type == "keyword":
            # Keyword search using ILIKE across supplier, invoice number, and filename
            sql = text("""
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
            exec_res = await db.execute(sql, {"q": f"%{query_text}%", "limit": limit})
            for row in exec_res.mappings():
                results.append(dict(row))

        elif search_type == "semantic":
            # Semantic search using pgvector Cosine distance (<=> operator)
            query_vector = cls.generate_embedding(query_text)
            sql = text("""
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
            exec_res = await db.execute(sql, {"vector": str(query_vector), "limit": limit})
            for row in exec_res.mappings():
                results.append(dict(row))

        else:
            # Hybrid search combining semantic cosine similarity and text match
            query_vector = cls.generate_embedding(query_text)
            sql = text("""
                SELECT 
                    d.id AS document_id,
                    d.filename,
                    d.status,
                    e.supplier_name,
                    e.invoice_number,
                    e.total_amount,
                    (
                        (1 - (e.embedding <=> :vector::vector)) * 0.7 +
                        CASE 
                            WHEN e.supplier_name ILIKE :q OR e.invoice_number ILIKE :q THEN 0.3
                            ELSE 0.0
                        END
                    ) AS score
                FROM extracted_invoices e
                JOIN documents d ON d.id = e.document_id
                WHERE e.embedding IS NOT NULL
                ORDER BY score DESC
                LIMIT :limit;
            """)
            exec_res = await db.execute(sql, {
                "vector": str(query_vector),
                "q": f"%{query_text}%",
                "limit": limit
            })
            for row in exec_res.mappings():
                results.append(dict(row))

        return results
