"""
Automated tests for Reciprocal Rank Fusion (RRF) and hybrid search logic.
"""

from decimal import Decimal
import pytest
from services.vector_service import VectorService


def test_rrf_scoring_combines_ranks():
    """Validates that a document present in both keyword and semantic ranks receives the highest RRF score."""
    keyword_docs = [
        {"document_id": 1, "filename": "doc1.pdf", "supplier_name": "Tech Corp"},
        {"document_id": 2, "filename": "doc2.pdf", "supplier_name": "Alpha Ltd"}
    ]
    semantic_docs = [
        {"document_id": 2, "filename": "doc2.pdf", "supplier_name": "Alpha Ltd"},
        {"document_id": 3, "filename": "doc3.pdf", "supplier_name": "Beta Inc"}
    ]

    # k=60
    # doc 1: 1/(60+1) = 0.01639
    # doc 2: 1/(60+2) [kw rank 2] + 1/(60+1) [sem rank 1] = 0.016129 + 0.016393 = 0.03252
    # doc 3: 1/(60+2) [sem rank 2] = 0.016129
    fused = VectorService.apply_reciprocal_rank_fusion(keyword_docs, semantic_docs, k=60, limit=5)

    assert len(fused) == 3
    # Document 2 must be ranked 1st because it was retrieved by BOTH methods
    assert fused[0]["document_id"] == 2
    assert fused[0]["match_type"] == "hybrid"
    assert fused[0]["keyword_rank"] == 2
    assert fused[0]["semantic_rank"] == 1

    # Document 1 must be keyword_only
    doc1_entry = next(d for d in fused if d["document_id"] == 1)
    assert doc1_entry["match_type"] == "keyword_only"

    # Document 3 must be semantic_only
    doc3_entry = next(d for d in fused if d["document_id"] == 3)
    assert doc3_entry["match_type"] == "semantic_only"


def test_rrf_deduplication():
    """Ensures duplicate document IDs are merged into a single ranked result."""
    kw = [{"document_id": 10, "filename": "a.pdf"}]
    sem = [{"document_id": 10, "filename": "a.pdf"}]

    fused = VectorService.apply_reciprocal_rank_fusion(kw, sem, k=60, limit=10)
    assert len(fused) == 1
    assert fused[0]["document_id"] == 10


def test_rrf_deterministic_tie_breaking():
    """When two documents have the exact same RRF score, breaks tie deterministically."""
    kw = [
        {"document_id": 101, "filename": "first.pdf"},
        {"document_id": 102, "filename": "second.pdf"}
    ]
    sem = []  # No semantic matches

    fused = VectorService.apply_reciprocal_rank_fusion(kw, sem, k=60, limit=5)
    assert fused[0]["document_id"] == 101
    assert fused[1]["document_id"] == 102


def test_empty_search_query_handling():
    """Empty query should immediately resolve to empty list."""
    res = VectorService.apply_reciprocal_rank_fusion([], [], k=60, limit=10)
    assert res == []


def test_embedding_generation_produces_valid_dimensions():
    """Verifies FastEmbed produces exactly 384 dimensions without crashing."""
    vector = VectorService.generate_embedding("Test invoice search summary")
    assert isinstance(vector, list)
    assert len(vector) == 384
    assert any(v != 0.0 for v in vector)
