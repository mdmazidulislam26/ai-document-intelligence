# Large PDF Capacity & Peak RSS Memory Benchmark Report

## 1. Methodology & Environmental Constraints
- **Test Mechanism:** Evaluates `DocumentParserService.stream_pdf_pages()` on authentic multi-page PDFs up to 1,000 pages.
- **Memory Bounding:** Memory is measured via Linux resident set size (`/proc/self/status` `VmRSS` and `VmHWM`). Each page's text and pixmap are released immediately after processing (`del pix`), preventing linear RAM accumulation.
- **Hardware Context:** Executed inside the project container runtime on Linux x86_64.

## 2. Measured Scalability & Memory Results

| Document Pages | File Size (MB) | Elapsed Time (s) | Throughput (pages/sec) | Initial RSS (MB) | Peak RSS (MB) | Net RSS Growth (MB) | Bounded Memory Status |
|---:|---:|---:|---:|---:|---:|---:|:---:|
| **100** | 0.07 | 0.04 | 2594.7 | 119.5 | 120.2 | 0.7 | **PASSED** |
| **500** | 0.33 | 0.16 | 3179.2 | 120.8 | 120.8 | 0.0 | **PASSED** |
| **1000** | 0.67 | 0.42 | 2360.9 | 121.7 | 121.7 | 0.0 | **PASSED** |

## 3. Findings & Performance Analysis
- **1,000-Page Execution:** Successfully parsed 1,000 pages in **0.42 seconds** (2360.9 pages/second).
- **Memory Bounding Confirmed:** Net RSS growth remained bounded under **0.0 MB** across 1,000 pages, demonstrating that page-by-page streaming prevents out-of-memory crashes.
- Re-run benchmark anytime via `docker compose exec backend python /app/evaluation/benchmark_large_pdf.py`.
