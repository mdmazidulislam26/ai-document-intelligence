"""
Automated tests for the GHR-06 evaluation framework:
1. Reproducible dataset generation across all required formats.
2. Real DocumentParserService & Tesseract OCR execution on generated fixtures.
3. Metric calculation accuracy (field accuracy, line-item F1, hallucination rate, arithmetic consistency).
"""

import os
import sys
from decimal import Decimal

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(TESTS_DIR)
REPO_ROOT = os.path.dirname(BACKEND_DIR)

EVAL_DIR = next(
    (p for p in (os.path.join(BACKEND_DIR, "evaluation"), os.path.join(REPO_ROOT, "evaluation")) if os.path.isdir(p)),
    os.path.join(BACKEND_DIR, "evaluation"),
)
if EVAL_DIR not in sys.path:
    sys.path.insert(0, EVAL_DIR)

from generate_dataset import build_dataset, DATASET_DIR
from evaluate import compare_scalar_field, evaluate_line_items, compute_benchmark_summary
from models.schemas import LineItemSchema
from services.document_parser import DocumentParserService


def test_dataset_generator_creates_all_formats_and_parsers_read_them():
    """Verifies real binary fixtures for all formats are created and parsed cleanly."""
    manifest = build_dataset()
    assert len(manifest) == 10

    categories = {item["category"] for item in manifest}
    assert {
        "digital_pdf",
        "multipage_pdf",
        "scanned_pdf",
        "scanned_pdf_poor",
        "png_image",
        "jpg_image_poor",
        "xlsx_multisheet",
        "csv",
        "incomplete_pdf",
        "discrepancy_pdf",
    }.issubset(categories)

    by_id = {item["id"]: item for item in manifest}

    text_mp, pages_mp = DocumentParserService.extract_full_text(os.path.join(DATASET_DIR, by_id["doc_02"]["file"]))
    assert pages_mp == 12
    assert "INV-MP-1200" in text_mp
    assert "1540.00" in text_mp

    text_scn, pages_scn = DocumentParserService.extract_full_text(os.path.join(DATASET_DIR, by_id["doc_03"]["file"]))
    assert pages_scn == 2
    assert "SCN-4401" in text_scn or "4401" in text_scn

    text_poor_pdf, pages_poor = DocumentParserService.extract_full_text(os.path.join(DATASET_DIR, by_id["doc_04"]["file"]))
    assert pages_poor == 1
    assert len(text_poor_pdf.strip()) > 0

    text_png, _ = DocumentParserService.extract_full_text(os.path.join(DATASET_DIR, by_id["doc_05"]["file"]))
    assert "REC-7741" in text_png or "SuperMart" in text_png

    text_jpg, _ = DocumentParserService.extract_full_text(os.path.join(DATASET_DIR, by_id["doc_06"]["file"]))
    assert "275" in text_jpg or "Metro" in text_jpg

    text_xlsx, _ = DocumentParserService.extract_full_text(os.path.join(DATASET_DIR, by_id["doc_07"]["file"]))
    assert "Invoice_Summary" in text_xlsx
    assert "Line_Items" in text_xlsx
    assert "XLS-9001" in text_xlsx

    text_csv, _ = DocumentParserService.extract_full_text(os.path.join(DATASET_DIR, by_id["doc_08"]["file"]))
    assert "CSV-5501" in text_csv


def test_evaluation_metrics_hallucination_and_line_item_f1():
    """Verifies exact calculation of scalar accuracy, hallucination rate, line-item F1, and math consistency."""
    assert compare_scalar_field("currency", None, None) is True
    assert compare_scalar_field("currency", "USD", None) is False
    assert compare_scalar_field("total_amount", Decimal("100.02"), 100.00) is True
    assert compare_scalar_field("total_amount", Decimal("100.50"), 100.00) is False

    pred_items = [
        LineItemSchema(description="Cloud Server Hosting", quantity=Decimal("2"), unit_price=Decimal("150.00"), total=Decimal("300.00")),
        LineItemSchema(description="Extra Hallucinated Item", quantity=Decimal("1"), unit_price=Decimal("10.00"), total=Decimal("10.00")),
    ]
    truth_items = [
        {"description": "Cloud Server Hosting", "quantity": 2, "unit_price": 150.00, "total": 300.00},
        {"description": "Cybersecurity Audit", "quantity": 1, "unit_price": 200.00, "total": 200.00},
    ]
    li = evaluate_line_items(pred_items, truth_items)
    assert li["matched"] == 1
    assert li["precision"] == 0.5
    assert li["recall"] == 0.5
    assert li["f1"] == 0.5
    assert li["exact"] is False

    records = [
        {
            "id": "d1",
            "status": "success",
            "parse_sec": 0.2,
            "ai_sec": 0.8,
            "total_sec": 1.0,
            "field_matches": {
                "invoice_number": True,
                "invoice_date": True,
                "supplier_name": True,
                "customer_name": True,
                "subtotal": True,
                "tax": False,
                "total_amount": True,
                "currency": True,
            },
            "null_truth_fields": 2,
            "hallucinated_fields": 1,
            "line_items_metrics": li,
            "expected_math_valid": True,
            "math_passed": True,
        },
        {
            "id": "d2",
            "status": "failed",
            "parse_sec": 0.1,
            "ai_sec": 0.0,
            "total_sec": 0.1,
            "field_matches": {},
            "null_truth_fields": 0,
            "hallucinated_fields": 0,
            "line_items_metrics": {"matched": 0, "pred_count": 0, "truth_count": 0, "precision": 0.0, "recall": 0.0, "f1": 0.0, "exact": False},
            "expected_math_valid": False,
            "math_passed": False,
        },
    ]
    summary = compute_benchmark_summary(records)
    assert summary["success_rate_pct"] == 50.0
    assert summary["failure_rate_pct"] == 50.0
    assert summary["hallucination_rate_pct"] == 50.0
    assert summary["arithmetic_consistency_pct"] == 100.0
