
AI Prompts & Disclosure of AI-Assisted Development

Deliverable Requirement 9: "AI prompts and disclosure of AI-assisted
development, where applicable."

1. Disclosure of AI-Assisted Development

In accordance with the assignment deliverables, this project utilized Large
Language Models (LLMs) both as an integrated runtime component of the
application and as an engineering aid during development:

1.  Application Runtime Engine:
      - Provider: Groq Cloud API (Free Tier).
      - Model: llama-3.1-8b-instant.
      - Role: Extracts structured financial invoice entities (invoice_number,
        invoice_date, supplier_name, customer_name, subtotal, tax, total_amount,
        currency, and itemized line_items) from parsed text.
      - Extraction policy: The prompt requests null for information that is
        missing or unreadable. Structured output and deterministic validation
        reduce risk, but do not constitute a universal zero-hallucination guarantee.
2.  Development Methodology:
      - AI tools were utilized for architectural auditing, drafting
        unit/integration test scenarios, generating synthetic benchmark document
        fixtures, and optimizing SQL queries (e.g. PostgreSQL ts_rank_cd and
        pgvector HNSW CTE indexing).
      - Code, database schemas, and mathematical validation algorithms were
        reviewed and tested during development. See the repository's current
        CI run and evaluation reports for the actual test and benchmark results.

2. Runtime System Prompt Architecture

The AI extraction service (backend/services/ai_extractor.py) executes with the
following deterministic prompt and schema rules:

System Prompt (AIExtractorService.extract_from_chunk):

You are an expert financial data extraction engine. Analyze the document and return ONLY a valid JSON object matching this schema:
{
  "invoice_number": string or null,
  "invoice_date": "YYYY-MM-DD" or null,
  "supplier_name": string or null,
  "customer_name": string or null,
  "subtotal": number or null,
  "tax": number or null,
  "total_amount": number or null,
  "currency": string or null,
  "line_items": [
    {"description": string, "quantity": number, "unit_price": number, "total": number}
  ]
}
RULES:
1. Do not infer missing facts: If any field is not explicitly present or discernable, return null. This is a prompt instruction, not a guarantee that model output is always correct.
2. Never assume USD or any currency unless explicitly stated or indicated by symbol ($ -> USD, € -> EUR, £ -> GBP).
3. Format invoice_date strictly as YYYY-MM-DD if available.
4. For spreadsheets, each row should map to a line item.
5. Return ONLY raw JSON without markdown code fences.

Deterministic Parsing & Lossless Coercion:

  - The raw JSON response is parsed using Python's json.loads(...,
    parse_float=Decimal) to avoid intermediate floating-point rounding errors.
  - Output is validated against InvoiceExtractionSchema (Pydantic v2) with
    @field_validator hooks ensuring monetary fields coerce to Decimal and
    missing currency normalizes to None.
  - Merging across multi-chunk documents (merge_extractions) applies boundary
    sliding-window matching (line_items_equal) to eliminate chunk-overlap
    duplicates without discarding legitimate identical line items.

3. Mathematical Validation & Safety Boundaries

AI outputs are treated as untrusted and subjected to deterministic
post-extraction validation (DocumentValidator):

  - \sum (\text{line\_items.total}) \approx \text{subtotal} (tolerance: 0.05).
  - \text{subtotal} + \text{tax} \approx \text{total\_amount} (tolerance: 0.05).
  - If subtotal or total is missing, arithmetic validation is classified as
    not_evaluable.
  - If discrepancies occur, the document status is transitioned to
    requires_manual_review and specific ValidationLog entries are persisted. EOF
