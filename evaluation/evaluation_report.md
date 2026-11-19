# Document Intelligence Evaluation Report (10-Document Synthetic Benchmark)

## 1. Dataset & Methodology
- **Total Labeled Documents:** 10 (Digital 1-page & 12-page PDFs, clean & skewed/noisy scanned PDFs, PNG & degraded JPG images, multi-sheet XLSX, CSV, incomplete null-field PDF, and math-discrepancy PDF).
- **Pipeline Evaluated:** `DocumentParserService` (PyMuPDF / OpenCV + Tesseract OCR / Pandas) -> `AIExtractorService` (Groq LLM) -> `DocumentValidator` (Decimal arithmetic).
- **Hallucination Definition:** Percentage of deliberately absent (`null`) ground-truth fields for which the extractor invented a non-null value.
- **Arithmetic Consistency Rule:** Requires essential monetary fields to be present before classifying as a math pass; unextracted documents are classified as `not_evaluable`.

## 2. Measured Overall Metrics

| Metric | Measured Result | Denominator / Notes |
|---|---|---|
| **Pipeline Execution Success Rate** | **100.00%** | 10/10 completed without crash |
| **Field Extraction Success Rate** | **90.00%** | 9/10 extracted usable fields |
| **Document Processing Failure Rate** | **0.00%** | 0/10 failed |
| **Overall Scalar Field Accuracy** | **88.75%** | 71/80 scalar fields matched |
| **Line-Item 4-Field Strict F1** | **98.25%** | P: 100.00% (28/28), R: 96.55% (28/29) |
| **Line-Item Exact Document Match** | **90.00%** | 9/10 executed docs with 100% exact item sets |
| **Arithmetic Consistency (Evaluable Valid Docs)** | **100.00%** | 8/8 evaluable valid docs (1 unreadable scan not evaluable) |
| **Discrepancy Detection (Invalid Docs)** | **100.00%** | 1/1 intentional math errors caught |
| **Hallucination Rate (on Null Truth Fields)** | **0.00%** | 0/4 deliberately absent fields invented |
| **Avg Parse / OCR Latency** | **0.58 sec/doc** | Real PyMuPDF + Tesseract OCR |
| **Avg AI Extraction Latency** | **1.21 sec/doc** | Live Groq LLM inference |
| **Avg Total Pipeline Latency** | **1.79 sec/doc** | Total per document |

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

| Doc ID | Category | Pages | Status | Parse/OCR (s) | AI (s) | Scalar Match | Line-Item F1 | Math Status | Notes |
|---|---|---:|---|---:|---:|---:|---:|---|---|
| `doc_01` | digital_pdf | 1 | success | 0.01 | 1.55 | 8/8 | 100.0% | `pass` | Exact |
| `doc_02` | multipage_pdf | 12 | success | 0.00 | 2.73 | 8/8 | 100.0% | `pass` | Exact |
| `doc_03` | scanned_pdf | 2 | success | 2.14 | 1.15 | 8/8 | 100.0% | `pass` | Exact |
| `doc_04` | scanned_pdf_poor | 1 | success | 1.46 | 0.79 | 0/8 | 0.0% | `not_evaluable` | invoice_number: expected='SKW-7710', got=None; invoice_date: expected='2024-08-05', got=None; supplier_name: expected='Pacific Freight Logistics', got=None; customer_name: expected='Harbor Imports LLC', got=None; subtotal: expected=450.0, got=None; tax: expected=45.0, got=None; total_amount: expected=495.0, got=None; currency: expected='USD', got=None |
| `doc_05` | png_image | 1 | success | 1.03 | 0.91 | 8/8 | 100.0% | `pass` | Exact |
| `doc_06` | jpg_image_poor | 1 | success | 1.07 | 0.88 | 7/8 | 100.0% | `pass` | customer_name: expected='Greenfield Builders', got='Greenfieid Builders' |
| `doc_07` | xlsx_multisheet | 1 | success | 0.12 | 0.98 | 8/8 | 100.0% | `pass` | Exact |
| `doc_08` | csv | 1 | success | 0.00 | 1.41 | 8/8 | 100.0% | `pass` | Exact |
| `doc_09` | incomplete_pdf | 1 | success | 0.00 | 0.88 | 8/8 | 100.0% | `pass` | Exact |
| `doc_10` | discrepancy_pdf | 1 | success | 0.00 | 0.82 | 8/8 | 100.0% | `fail` | Exact |

## 5. Dataset Limitations & Candid Observations
- **Degraded Scans (`doc_04`):** With 2.5° skew, speckle noise, and low contrast, Tesseract OCR yielded unreadable text, resulting in 0/8 fields extracted. This document is correctly classified as `math_status = not_evaluable` rather than an arithmetic pass.
- **JPEG Character Degradation (`doc_06`):** Low quality JPEG artifact caused 1 character OCR misreading (`Greenfieid` vs `Greenfield`), resulting in 7/8 scalar accuracy.
- **Hallucination Evaluation:** On this synthetic dataset, 4 ground-truth fields were deliberately null; 0/4 were populated by the extractor. This is a small-sample observation, not a general zero-hallucination guarantee.
- Re-run anytime via `python evaluation/generate_dataset.py && python evaluation/evaluate.py`.
