"""
End-to-end real-world evaluation suite for GHR-06.
Runs real documents through:
  DocumentParserService (PyMuPDF / OpenCV + Tesseract OCR / Pandas)
  -> AIExtractorService (Groq LLM)
  -> DocumentValidator (Decimal arithmetic & required field checks)
"""

import os
import sys
import json
import time
import argparse
from decimal import Decimal
from typing import Dict, Any, List, Tuple, Optional

EVAL_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EVAL_DIR, ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")

for p in (BACKEND_DIR, ROOT_DIR):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

from models.schemas import InvoiceExtractionSchema, LineItemSchema
from services.document_parser import DocumentParserService
from services.ai_extractor import AIExtractorService, AITransientError
from services.validator import DocumentValidator, to_decimal, normalize_identifier, normalize_text

DEFAULT_MANIFEST = os.path.join(EVAL_DIR, "benchmark_dataset", "dataset_manifest.json")
REPORT_PATH = os.path.join(EVAL_DIR, "evaluation_report.md")

SCALAR_FIELDS = [
    "invoice_number",
    "invoice_date",
    "supplier_name",
    "customer_name",
    "subtotal",
    "tax",
    "total_amount",
    "currency",
]


def compare_scalar_field(field: str, extracted_val: Any, truth_val: Any) -> bool:
    if truth_val is None:
        return extracted_val is None
    if extracted_val is None:
        return False

    if field == "invoice_number":
        return normalize_identifier(str(extracted_val)) == normalize_identifier(str(truth_val))
    if field == "invoice_date":
        return str(extracted_val).strip()[:10] == str(truth_val).strip()[:10]
    if field in ("supplier_name", "customer_name"):
        return normalize_text(str(extracted_val)) == normalize_text(str(truth_val))
    if field == "currency":
        return str(extracted_val).strip().upper() == str(truth_val).strip().upper()
    if field in ("subtotal", "tax", "total_amount"):
        pred_dec = to_decimal(extracted_val)
        truth_dec = to_decimal(truth_val)
        if pred_dec is None or truth_dec is None:
            return False
        return abs(pred_dec - truth_dec) <= Decimal("0.05")

    return str(extracted_val).strip().lower() == str(truth_val).strip().lower()


def _line_item_matches(pred_item: LineItemSchema, truth_item: Dict[str, Any]) -> bool:
    pred_desc = normalize_text(pred_item.description or "")
    truth_desc = normalize_text(str(truth_item.get("description") or ""))
    if not pred_desc or not truth_desc:
        desc_match = pred_desc == truth_desc
    else:
        truth_tokens = set(truth_desc.split())
        pred_tokens = set(pred_desc.split())
        overlap = len(truth_tokens & pred_tokens) / max(len(truth_tokens), 1)
        desc_match = (truth_desc in pred_desc) or (pred_desc in truth_desc) or (overlap >= 0.7)

    pred_tot = to_decimal(pred_item.total)
    truth_tot = to_decimal(truth_item.get("total"))
    if pred_tot is None or truth_tot is None:
        tot_match = (pred_tot is None and truth_tot is None)
    else:
        tot_match = abs(pred_tot - truth_tot) <= Decimal("0.05")

    return desc_match and tot_match


def evaluate_line_items(
    pred_items: List[LineItemSchema],
    truth_items: List[Dict[str, Any]],
) -> Dict[str, Any]:
    if not truth_items and not pred_items:
        return {"matched": 0, "pred_count": 0, "truth_count": 0, "precision": 1.0, "recall": 1.0, "f1": 1.0, "exact": True}

    matched_truth_indices = set()
    matched_count = 0
    for p_it in pred_items:
        for idx, t_it in enumerate(truth_items):
            if idx not in matched_truth_indices and _line_item_matches(p_it, t_it):
                matched_truth_indices.add(idx)
                matched_count += 1
                break

    precision = matched_count / len(pred_items) if pred_items else 0.0
    recall = matched_count / len(truth_items) if truth_items else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    exact = (matched_count == len(truth_items) == len(pred_items))

    return {
        "matched": matched_count,
        "pred_count": len(pred_items),
        "truth_count": len(truth_items),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "exact": exact,
    }


def compute_benchmark_summary(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_docs = len(records)
    succeeded = [r for r in records if r["status"] == "success"]
    failed = [r for r in records if r["status"] != "success"]

    field_stats = {f: {"correct": 0, "total": 0} for f in SCALAR_FIELDS}
    null_truth_total = 0
    hallucinated_count = 0

    total_li_matched = 0
    total_li_pred = 0
    total_li_truth = 0
    exact_li_docs = 0

    valid_math_expected = 0
    valid_math_passed = 0
    invalid_math_expected = 0
    invalid_math_caught = 0

    for r in succeeded:
        for f, is_correct in r["field_matches"].items():
            field_stats[f]["total"] += 1
            if is_correct:
                field_stats[f]["correct"] += 1

        null_truth_total += r["null_truth_fields"]
        hallucinated_count += r["hallucinated_fields"]

        li = r["line_items_metrics"]
        total_li_matched += li["matched"]
        total_li_pred += li["pred_count"]
        total_li_truth += li["truth_count"]
        if li["exact"]:
            exact_li_docs += 1

        if r["expected_math_valid"]:
            valid_math_expected += 1
            if r["math_passed"]:
                valid_math_passed += 1
        else:
            invalid_math_expected += 1
            if not r["math_passed"]:
                invalid_math_caught += 1

    per_field_pct = {
        f: (st["correct"] / st["total"] * 100.0) if st["total"] > 0 else None
        for f, st in field_stats.items()
    }

    total_scalar_correct = sum(st["correct"] for st in field_stats.values())
    total_scalar_eval = sum(st["total"] for st in field_stats.values())
    overall_scalar_acc = (total_scalar_correct / total_scalar_eval * 100.0) if total_scalar_eval > 0 else 0.0

    li_precision = (total_li_matched / total_li_pred * 100.0) if total_li_pred > 0 else 0.0
    li_recall = (total_li_matched / total_li_truth * 100.0) if total_li_truth > 0 else 0.0
    li_f1 = (2 * li_precision * li_recall / (li_precision + li_recall)) if (li_precision + li_recall) > 0 else 0.0

    hallucination_rate = (hallucinated_count / null_truth_total * 100.0) if null_truth_total > 0 else None

    success_rate = (len(succeeded) / total_docs * 100.0) if total_docs > 0 else 0.0
    failure_rate = (len(failed) / total_docs * 100.0) if total_docs > 0 else 0.0

    avg_parse_sec = sum(r["parse_sec"] for r in succeeded) / len(succeeded) if succeeded else 0.0
    avg_ai_sec = sum(r["ai_sec"] for r in succeeded) / len(succeeded) if succeeded else 0.0
    avg_total_sec = sum(r["total_sec"] for r in succeeded) / len(succeeded) if succeeded else 0.0

    return {
        "total_docs": total_docs,
        "succeeded_docs": len(succeeded),
        "failed_docs": len(failed),
        "success_rate_pct": success_rate,
        "failure_rate_pct": failure_rate,
        "per_field_accuracy_pct": per_field_pct,
        "field_stats": field_stats,
        "overall_scalar_accuracy_pct": overall_scalar_acc,
        "line_item_precision_pct": li_precision,
        "line_item_recall_pct": li_recall,
        "line_item_f1_pct": li_f1,
        "line_item_exact_doc_pct": (exact_li_docs / len(succeeded) * 100.0) if succeeded else 0.0,
        "null_truth_fields": null_truth_total,
        "hallucinated_fields": hallucinated_count,
        "hallucination_rate_pct": hallucination_rate,
        "valid_math_expected": valid_math_expected,
        "valid_math_passed": valid_math_passed,
        "arithmetic_consistency_pct": (valid_math_passed / valid_math_expected * 100.0) if valid_math_expected > 0 else 0.0,
        "invalid_math_expected": invalid_math_expected,
        "invalid_math_caught": invalid_math_caught,
        "discrepancy_detection_pct": (invalid_math_caught / invalid_math_expected * 100.0) if invalid_math_expected > 0 else None,
        "avg_parse_sec": avg_parse_sec,
        "avg_ai_sec": avg_ai_sec,
        "avg_total_sec": avg_total_sec,
    }


def _extract_with_retry(ai_service: AIExtractorService, text: str, max_attempts: int = 3) -> InvoiceExtractionSchema:
    for attempt in range(max_attempts):
        try:
            return ai_service.extract_invoice_data(text)
        except AITransientError:
            if attempt == max_attempts - 1:
                raise
            time.sleep(3.0 * (attempt + 1))
    raise RuntimeError("Unreachable")


def run_benchmark(manifest_path: str = DEFAULT_MANIFEST, inter_doc_delay: float = 1.0) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    dataset_dir = os.path.dirname(manifest_path)
    with open(manifest_path, "r") as f:
        dataset = json.load(f)

    ai_service = AIExtractorService()
    records: List[Dict[str, Any]] = []

    print("=" * 72)
    print(f"RUNNING REAL-WORLD END-TO-END BENCHMARK ({len(dataset)} DOCUMENTS)")
    print("=" * 72)

    for idx, item in enumerate(dataset):
        doc_id = item["id"]
        rel_file = item["file"]
        abs_file = os.path.join(dataset_dir, rel_file)
        truth = item["ground_truth"]
        expected_math_valid = bool(item.get("expected_math_valid", True))

        t0 = time.perf_counter()
        parse_sec = 0.0
        ai_sec = 0.0
        val_sec = 0.0

        try:
            t_p0 = time.perf_counter()
            raw_text, page_count = DocumentParserService.extract_full_text(abs_file)
            parse_sec = time.perf_counter() - t_p0

            if not raw_text or not raw_text.strip():
                raise ValueError("No readable text extracted from document.")

            t_a0 = time.perf_counter()
            extracted = _extract_with_retry(ai_service, raw_text)
            ai_sec = time.perf_counter() - t_a0

            t_v0 = time.perf_counter()
            math_errors = DocumentValidator.validate_math(extracted)
            val_sec = time.perf_counter() - t_v0
            total_sec = time.perf_counter() - t0

            field_matches = {}
            discrepancies = []
            null_truth_fields = 0
            hallucinated_fields = 0

            for f in SCALAR_FIELDS:
                expected_val = truth.get(f)
                actual_val = getattr(extracted, f, None)
                matched = compare_scalar_field(f, actual_val, expected_val)
                field_matches[f] = matched
                if expected_val is None:
                    null_truth_fields += 1
                    if actual_val is not None:
                        hallucinated_fields += 1
                if not matched:
                    discrepancies.append(f"{f}: expected={expected_val!r}, got={actual_val!r}")

            li_metrics = evaluate_line_items(extracted.line_items, truth.get("line_items", []))
            math_passed = (len(math_errors) == 0)

            records.append({
                "id": doc_id,
                "category": item.get("category", "unknown"),
                "file": rel_file,
                "pages": page_count,
                "status": "success",
                "error": None,
                "parse_sec": parse_sec,
                "ai_sec": ai_sec,
                "val_sec": val_sec,
                "total_sec": total_sec,
                "field_matches": field_matches,
                "discrepancies": discrepancies,
                "null_truth_fields": null_truth_fields,
                "hallucinated_fields": hallucinated_fields,
                "line_items_metrics": li_metrics,
                "expected_math_valid": expected_math_valid,
                "math_passed": math_passed,
            })

            print(
                f"[{idx+1}/{len(dataset)}] {doc_id} ({item.get('category')}, {page_count}p) | "
                f"parse={parse_sec:.2f}s ai={ai_sec:.2f}s | "
                f"scalar={sum(field_matches.values())}/{len(SCALAR_FIELDS)} | "
                f"items_f1={li_metrics['f1']*100:.1f}% | math_ok={math_passed}"
            )
            if discrepancies:
                for d in discrepancies:
                    print(f"    -> Discrepancy: {d}")

        except Exception as exc:
            total_sec = time.perf_counter() - t0
            records.append({
                "id": doc_id,
                "category": item.get("category", "unknown"),
                "file": rel_file,
                "pages": 0,
                "status": "failed",
                "error": f"{type(exc).__name__}: {str(exc)}",
                "parse_sec": parse_sec,
                "ai_sec": ai_sec,
                "val_sec": val_sec,
                "total_sec": total_sec,
                "field_matches": {},
                "discrepancies": [],
                "null_truth_fields": 0,
                "hallucinated_fields": 0,
                "line_items_metrics": {"matched": 0, "pred_count": 0, "truth_count": 0, "precision": 0.0, "recall": 0.0, "f1": 0.0, "exact": False},
                "expected_math_valid": expected_math_valid,
                "math_passed": False,
            })
            print(f"[{idx+1}/{len(dataset)}] {doc_id} FAILED: {type(exc).__name__}: {exc}")

        if inter_doc_delay > 0 and idx < len(dataset) - 1:
            time.sleep(inter_doc_delay)

    summary = compute_benchmark_summary(records)
    _write_markdown_report(summary, records, REPORT_PATH)
    return summary, records


def _fmt_pct(val: Optional[float]) -> str:
    return f"{val:.2f}%" if val is not None else "N/A"


def _write_markdown_report(summary: Dict[str, Any], records: List[Dict[str, Any]], report_path: str) -> None:
    pf = summary["per_field_accuracy_pct"]
    fs = summary["field_stats"]

    lines = [
        "# Document Intelligence Evaluation Report (Measured Benchmark)",
        "",
        "## 1. Dataset & Methodology",
        f"- **Total Labeled Documents:** {summary['total_docs']} (Digital 1-page & 12-page PDFs, clean & skewed/noisy scanned PDFs, PNG & degraded JPG images, multi-sheet XLSX, CSV, incomplete null-field PDF, and math-discrepancy PDF).",
        "- **Pipeline Evaluated:** `DocumentParserService` (PyMuPDF / OpenCV + Tesseract OCR / Pandas) -> `AIExtractorService` (Groq LLM) -> `DocumentValidator` (Decimal arithmetic).",
        "- **Hallucination Definition:** Percentage of deliberately absent (`null`) ground-truth fields for which the extractor invented a non-null value.",
        "",
        "## 2. Measured Overall Metrics",
        "",
        "| Metric | Measured Result |",
        "|---|---|",
        f"| **Document Processing Success Rate** | **{summary['success_rate_pct']:.2f}%** ({summary['succeeded_docs']}/{summary['total_docs']}) |",
        f"| **Document Processing Failure Rate** | **{summary['failure_rate_pct']:.2f}%** ({summary['failed_docs']}/{summary['total_docs']}) |",
        f"| **Overall Scalar Field Accuracy** | **{summary['overall_scalar_accuracy_pct']:.2f}%** |",
        f"| **Line-Item Precision / Recall / F1** | **{summary['line_item_precision_pct']:.2f}% / {summary['line_item_recall_pct']:.2f}% / {summary['line_item_f1_pct']:.2f}%** |",
        f"| **Line-Item Exact Document Match** | **{summary['line_item_exact_doc_pct']:.2f}%** |",
        f"| **Arithmetic Consistency (Valid Docs)** | **{summary['arithmetic_consistency_pct']:.2f}%** ({summary['valid_math_passed']}/{summary['valid_math_expected']}) |",
        f"| **Discrepancy Detection (Invalid Docs)** | **{_fmt_pct(summary['discrepancy_detection_pct'])}** ({summary['invalid_math_caught']}/{summary['invalid_math_expected']}) |",
        f"| **Hallucination Rate (on Null Truth Fields)** | **{_fmt_pct(summary['hallucination_rate_pct'])}** ({summary['hallucinated_fields']}/{summary['null_truth_fields']}) |",
        f"| **Avg Parse / OCR Latency** | **{summary['avg_parse_sec']:.2f} sec/doc** |",
        f"| **Avg AI Extraction Latency** | **{summary['avg_ai_sec']:.2f} sec/doc** |",
        f"| **Avg Total Pipeline Latency** | **{summary['avg_total_sec']:.2f} sec/doc** |",
        "",
        "## 3. Field-Level Extraction Accuracy",
        "",
        "| Field | Correct / Total | Measured Accuracy |",
        "|---|---|---|",
    ]
    for f in SCALAR_FIELDS:
        lines.append(f"| `{f}` | {fs[f]['correct']} / {fs[f]['total']} | **{_fmt_pct(pf[f])}** |")

    lines.extend([
        "",
        "## 4. Per-Document Results",
        "",
        "| Doc ID | Category | Pages | Status | Parse/OCR (s) | AI (s) | Scalar Match | Line-Item F1 | Math Passed | Notes |",
        "|---|---|---:|---|---:|---:|---:|---:|---|---|",
    ])
    for r in records:
        if r["status"] == "success":
            sc_ok = sum(r["field_matches"].values())
            sc_tot = len(r["field_matches"])
            note = "; ".join(r["discrepancies"]) if r["discrepancies"] else "Exact"
            lines.append(
                f"| `{r['id']}` | {r['category']} | {r['pages']} | success | {r['parse_sec']:.2f} | {r['ai_sec']:.2f} | "
                f"{sc_ok}/{sc_tot} | {r['line_items_metrics']['f1']*100:.1f}% | {r['math_passed']} | {note} |"
            )
        else:
            lines.append(
                f"| `{r['id']}` | {r['category']} | {r['pages']} | failed | {r['parse_sec']:.2f} | {r['ai_sec']:.2f} | "
                f"0/0 | 0.0% | False | {r['error']} |"
            )

    lines.extend([
        "",
        "## 5. Dataset Limitations & Reproducibility",
        "- This benchmark uses 10 deterministically generated multi-format documents (`evaluation/generate_dataset.py`) to guarantee full reproducibility without exposing private customer financial documents.",
        "- Synthetic scanned/noisy images approximate real scan degradation (skew, Gaussian noise, low contrast, JPEG compression) and do not replace large proprietary enterprise vendor corpora (100+ layouts).",
        "- Legacy `.xls` reading is tested via unit tests (`xlrd`); `.xlsx` and `.csv` are included directly in this benchmark.",
        "- Re-run anytime via `python evaluation/generate_dataset.py && python evaluation/evaluate.py`.",
    ])

    with open(report_path, "w") as rf:
        rf.write("\n".join(lines) + "\n")
    print(f"\nReport written to: {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Document Intelligence benchmark evaluation.")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--delay", type=float, default=1.0, help="Delay in seconds between documents.")
    args = parser.parse_args()
    run_benchmark(manifest_path=args.manifest, inter_doc_delay=args.delay)
