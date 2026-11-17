"""
Hybrid, semantic, and keyword search API endpoints over extracted documents.
Returns rich relevance ranking and RRF metadata.
"""

from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from models.schemas import SearchResultItem
from services.vector_service import VectorService

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("", response_model=List[SearchResultItem])
async def search_documents(
    q: str = Query(..., min_length=1, description="Search term, company name, or invoice number"),
    type: str = Query("hybrid", pattern="^(keyword|semantic|hybrid)$", description="Search mode"),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Executes high-performance search across processed documents:
    - keyword: PostgreSQL Full-Text Search (ts_rank) & partial identifier match
    - semantic: Cosine distance matching via pgvector and FastEmbed embeddings
    - hybrid: Reciprocal Rank Fusion (RRF) combining keyword and semantic rankings
    """
    try:
        raw_results = await VectorService.hybrid_search(
            db=db,
            query_text=q,
            search_type=type,
            limit=limit
        )

        output = []
        for r in raw_results:
            sim_score = r.get("score")
            output.append(
                SearchResultItem(
                    document_id=r.get("document_id"),
                    filename=r.get("filename", ""),
                    supplier_name=r.get("supplier_name"),
                    invoice_number=r.get("invoice_number"),
                    total_amount=r.get("total_amount"),
                    currency=r.get("currency"),
                    status=r.get("status", "unknown"),
                    similarity_score=round(float(sim_score), 4) if sim_score is not None else None,
                    rrf_score=r.get("rrf_score"),
                    match_type=r.get("match_type", type),
                    keyword_rank=r.get("keyword_rank"),
                    semantic_rank=r.get("semantic_rank")
                )
            )
        return output

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search query execution failed: {str(e)}")
