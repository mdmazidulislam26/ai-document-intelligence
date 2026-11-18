# Large PDF Capacity & Peak RSS Memory Benchmark Report

## 1. Methodology & Scope
- **Test Mechanism:** Evaluates only `DocumentParserService.stream_pdf_pages()` on generated multi-page PDFs up to 1,000 pages.
- **Scope Limitation:** This parser-iterator microbenchmark does not invoke OCR, `extract_full_text()` aggregation, AI extraction, database persistence, or the complete document pipeline.
- **Memory Measurement:** Linux process RSS (`VmRSS` and `VmHWM`) is sampled during this iterator-only run; the figures are not end-to-end pipeline memory measurements.
- **Runtime Context:** Reported as executed inside the project container runtime on Linux x86_64.

## 2. Measured Scalability & Memory Results

| Document Pages | File Size (MB) | Elapsed Time (s) | Throughput (pages/sec) | Initial RSS (MB) | Peak RSS (MB) | Net RSS Growth (MB) | Bounded Memory Status |
|---:|---:|---:|---:|---:|---:|---:|:---:|
| **100** | 0.07 | 0.04 | 2594.7 | 119.5 | 120.2 | 0.7 | **PASSED** |
| **500** | 0.33 | 0.16 | 3179.2 | 120.8 | 120.8 | 0.0 | **PASSED** |
| **1000** | 0.67 | 0.42 | 2360.9 | 121.7 | 121.7 | 0.0 | **PASSED** |

## 3. Findings & Performance Analysis
- **1,000-Page Execution:** Successfully parsed 1,000 pages in **0.42 seconds** (2360.9 pages/second).
- **Parser-Iterator RSS Observation:** Net process RSS growth was **0.0 MB** during this iterator-only 1,000-page run. This does not establish bounded memory for OCR, full-text aggregation, or the complete AI pipeline.
- Re-run benchmark anytime via `docker compose exec backend python /app/evaluation/benchmark_large_pdf.py`.
