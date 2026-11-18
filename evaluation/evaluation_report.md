# Document Intelligence Evaluation Report (Measured Benchmark)

## 1. Dataset & Methodology
- **Total Labeled Documents:** 10 (Digital 1-page & 12-page PDFs, clean & skewed/noisy scanned PDFs, PNG & degraded JPG images, multi-sheet XLSX, CSV, incomplete null-field PDF, and math-discrepancy PDF).
- **Pipeline Evaluated:** `DocumentParserService` (PyMuPDF / OpenCV + Tesseract OCR / Pandas) -> `AIExtractorService` (Groq LLM) -> `DocumentValidator` (Decimal arithmetic).
- **Hallucination Definition:** Percentage of deliberately absent (`null`) ground-truth fields for which the extractor invented a non-null value.

## 2. Measured Overall Metrics

| Metric | Measured Result |
|---|---|
| **Document Processing Success Rate** | **100.00%** (10/10) |
| **Document Processing Failure Rate** | **0.00%** (0/10) |
| **Overall Scalar Field Accuracy** | **88.75%** |
| **Line-Item Precision / Recall / F1** | **100.00% / 96.55% / 98.25%** |
| **Line-Item Exact Document Match** | **90.00%** |
| **Arithmetic Consistency (Valid Docs)** | **100.00%** (9/9) |
| **Discrepancy Detection (Invalid Docs)** | **100.00%** (1/1) |
| **Hallucination Rate (on Null Truth Fields)** | **0.00%** (0/4) |
| **Avg Parse / OCR Latency** | **0.62 sec/doc** |
| **Avg AI Extraction Latency** | **1.48 sec/doc** |
| **Avg Total Pipeline Latency** | **2.10 sec/doc** |

## 3. Field-Level Extraction Accuracy

| Field | Correct / Total | Measured Accuracy |
|---|---|---|
| `invoice_number` | 9 / 10 | **90.00%** |
| `invoice_date` | 9 / 10 | **90.00%** |
| `supplier_name` | 9 / 10 | **90.00%** |
| `customer_name` | 8 / 10 | **80.00%** |
| `subtotal` | 9 / 10 | **90.00%** |
| `tax` | 9 / 10 | **90.00%** |
| `total_amount` | 9 / 10 | **90.00%** |
| `currency` | 9 / 10 | **90.00%** |

## 4. Per-Document Results

| Doc ID | Category | Pages | Status | Parse/OCR (s) | AI (s) | Scalar Match | Line-Item F1 | Math Passed | Notes |
|---|---|---:|---|---:|---:|---:|---:|---|---|
| `doc_01` | digital_pdf | 1 | success | 0.01 | 1.66 | 8/8 | 100.0% | True | Exact |
| `doc_02` | multipage_pdf | 12 | success | 0.00 | 2.57 | 8/8 | 100.0% | True | Exact |
| `doc_03` | scanned_pdf | 2 | success | 2.25 | 1.00 | 8/8 | 100.0% | True | Exact |
| `doc_04` | scanned_pdf_poor | 1 | success | 1.60 | 2.11 | 0/8 | 0.0% | True | invoice_number: expected='SKW-7710', got=None; invoice_date: expected='2024-08-05', got=None; supplier_name: expected='Pacific Freight Logistics', got=None; customer_name: expected='Harbor Imports LLC', got=None; subtotal: expected=450.0, got=None; tax: expected=45.0, got=None; total_amount: expected=495.0, got=None; currency: expected='USD', got=None |
| `doc_05` | png_image | 1 | success | 1.19 | 1.47 | 8/8 | 100.0% | True | Exact |
| `doc_06` | jpg_image_poor | 1 | success | 1.03 | 0.95 | 7/8 | 100.0% | True | customer_name: expected='Greenfield Builders', got='Greenfieid Builders' |
| `doc_07` | xlsx_multisheet | 1 | success | 0.11 | 1.41 | 8/8 | 100.0% | True | Exact |
| `doc_08` | csv | 1 | success | 0.00 | 1.41 | 8/8 | 100.0% | True | Exact |
| `doc_09` | incomplete_pdf | 1 | success | 0.00 | 0.64 | 8/8 | 100.0% | True | Exact |
| `doc_10` | discrepancy_pdf | 1 | success | 0.00 | 1.61 | 8/8 | 100.0% | False | Exact |

## 5. Dataset Limitations & Reproducibility
- This benchmark uses 10 deterministically generated multi-format documents (`evaluation/generate_dataset.py`) to guarantee full reproducibility without exposing private customer financial documents.
- Synthetic scanned/noisy images approximate real scan degradation (skew, Gaussian noise, low contrast, JPEG compression) and do not replace large proprietary enterprise vendor corpora (100+ layouts).
- Legacy `.xls` reading is tested via unit tests (`xlrd`); `.xlsx` and `.csv` are included directly in this benchmark.
- Re-run anytime via `python evaluation/generate_dataset.py && python evaluation/evaluate.py`.
