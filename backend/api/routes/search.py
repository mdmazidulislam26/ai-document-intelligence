"""
Hybrid, semantic, and keyword search API endpoints over extracted documents.
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
    - keyword: Full-text matching in supplier, invoice number, and filename
    - semantic: Cosine distance matching via pgvector and FastEmbed embeddings
    - hybrid: Combined weighted ranking of keyword and semantic signals
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
            output.append(
                SearchResultItem(
                    document_id=r.get("document_id"),
                    filename=r.get("filename", ""),
                    supplier_name=r.get("supplier_name"),
                    invoice_number=r.get("invoice_number"),
                    total_amount=r.get("total_amount"),
                    status=r.get("status", "unknown"),
                    similarity_score=round(float(r.get("score", 0.0)), 4) if r.get("score") is not None else None
                )
            )
        return output

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search query execution failed: {str(e)}")
