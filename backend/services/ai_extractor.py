"""
AI information extraction service.
Uses Groq free API with strict JSON schema outputs.
Parses JSON floats directly into Decimal, implements typed exceptions,
auto-splits HTTP 413 oversized chunks, handles massive multi-hundred-page PDFs
via bounded head + tail windowing within free-tier TPM limits,
merges multi-chunk extractions deterministically, and never logs confidential invoice text.
"""

import json
import re
import time
import logging
from decimal import Decimal
from typing import List
from openai import OpenAI, APIConnectionError, RateLimitError, AuthenticationError, APIStatusError
from core.config import settings
from models.schemas import InvoiceExtractionSchema, LineItemSchema

logger = logging.getLogger("ai_extractor")
logger.setLevel(logging.INFO)


class AIExtractionError(Exception):
    """Base exception for AI extraction pipeline."""
    pass


class AITransientError(AIExtractionError):
    """Transient errors (Rate limits, Network timeouts) that Celery must retry."""
    pass


class AIAuthenticationError(AIExtractionError):
    """Permanent configuration or authentication failure."""
    pass


class AIMalformedResponseError(AIExtractionError):
    """LLM returned unparseable or schema-violating output."""
    pass


def line_items_equal(a: LineItemSchema, b: LineItemSchema) -> bool:
    """Checks if two line items have identical values across all present fields."""
    desc_a = (a.description or "").strip().lower()
    desc_b = (b.description or "").strip().lower()
    if desc_a != desc_b:
        return False

    for attr in ["quantity", "unit_price", "total"]:
        val_a = getattr(a, attr, None)
        val_b = getattr(b, attr, None)
        if val_a != val_b:
            return False
    return True


class AIExtractorService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.LLM_MODEL
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=self.api_key or "missing_key",
        )

    def _call_chat_completion(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.0,
                max_tokens=1200,
            )
            return response.choices[0].message.content or "{}"
        except (RateLimitError, AuthenticationError, APIConnectionError):
            raise
        except APIStatusError as status_err:
            if status_err.status_code in [401, 403, 413, 429, 502, 503, 504]:
                raise
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.0,
                max_tokens=1200,
            )
            return response.choices[0].message.content or "{}"

    def extract_from_chunk(self, chunk_text: str, _split_depth: int = 0) -> InvoiceExtractionSchema:
        """Sends a single chunk to the LLM with strict JSON schema enforcement, 413 auto-split, and 429 pacing."""
        if not chunk_text or not chunk_text.strip():
            return InvoiceExtractionSchema()

        if not self.api_key or self.api_key.strip() == "":
            raise AIAuthenticationError("GROQ_API_KEY is not configured in environment.")

        system_prompt = (
            "You are an expert financial data extraction engine. Analyze the document and return ONLY a valid JSON object matching this schema:\n"
            "{\n"
            '  "invoice_number": string or null,\n'
            '  "invoice_date": "YYYY-MM-DD" or null,\n'
            '  "supplier_name": string or null,\n'
            '  "customer_name": string or null,\n'
            '  "subtotal": number or null,\n'
            '  "tax": number or null,\n'
            '  "total_amount": number or null,\n'
            '  "currency": string or null,\n'
            '  "line_items": [\n'
            '    {"description": string, "quantity": number, "unit_price": number, "total": number}\n'
            "  ]\n"
            "}\n"
            "RULES:\n"
            "1. ZERO HALLUCINATION: If any field is not explicitly present or discernable, return null.\n"
            "2. Never assume USD or any currency unless explicitly stated or indicated by symbol ($ -> USD, € -> EUR, £ -> GBP).\n"
            "3. Format invoice_date strictly as YYYY-MM-DD if available.\n"
            "4. For spreadsheets, each row should map to a line item.\n"
            "5. Return ONLY raw JSON without markdown code fences."
        )

        user_prompt = f"Document Content:\n\n{chunk_text}"
        raw_response = ""
        max_rl_attempts = 4

        for attempt in range(max_rl_attempts):
            try:
                raw_response = self._call_chat_completion(system_prompt, user_prompt)
                break
            except AuthenticationError as auth_err:
                raise AIAuthenticationError("Groq API authentication failed.") from auth_err
            except RateLimitError as rl_err:
                if attempt == max_rl_attempts - 1:
                    raise AITransientError("Transient Groq API error: RateLimitError") from rl_err
                retry_after = None
                resp = getattr(rl_err, "response", None)
                if resp is not None and getattr(resp, "headers", None):
                    raw_ra = resp.headers.get("retry-after")
                    if raw_ra:
                        try:
                            retry_after = float(raw_ra)
                        except ValueError:
                            retry_after = None
                wait_sec = min(62.0, (retry_after + 1.0) if retry_after is not None else 15.0 * (attempt + 1))
                logger.warning(f"Groq rate limit hit; pacing for {wait_sec:.1f}s (attempt {attempt + 1}/{max_rl_attempts})")
                time.sleep(wait_sec)
            except APIConnectionError as trans_err:
                raise AITransientError(f"Transient Groq API error: {type(trans_err).__name__}") from trans_err
            except APIStatusError as status_err:
                if status_err.status_code == 413 and len(chunk_text) > 2000 and _split_depth < 4:
                    mid = len(chunk_text) // 2
                    logger.warning(
                        f"Groq HTTP 413 on {len(chunk_text)}-char chunk; splitting into two halves (depth={_split_depth + 1})"
                    )
                    left = self.extract_from_chunk(chunk_text[:mid], _split_depth=_split_depth + 1)
                    time.sleep(1.5)
                    right = self.extract_from_chunk(chunk_text[mid:], _split_depth=_split_depth + 1)
                    return self.merge_extractions([left, right])
                if status_err.status_code in [429, 502, 503, 504]:
                    raise AITransientError(f"Groq server status {status_err.status_code}") from status_err
                raise AIExtractionError(f"Groq API status error: {status_err.status_code}") from status_err
            except Exception as e:
                raise AIExtractionError(f"Unexpected AI client error: {type(e).__name__}") from e

        try:
            cleaned = re.sub(r"^```[a-zA-Z]*\s*", "", raw_response.strip())
            cleaned = re.sub(r"\s*```$", "", cleaned).strip()
            json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if json_match:
                cleaned = json_match.group(0)

            parsed_json = json.loads(cleaned, parse_float=Decimal)
            return InvoiceExtractionSchema(**parsed_json)
        except Exception as parse_err:
            logger.error(f"Failed to parse LLM JSON (payload_length={len(raw_response)}): {type(parse_err).__name__}")
            raise AIMalformedResponseError(f"Malformed LLM JSON output: {type(parse_err).__name__}") from parse_err

    @classmethod
    def merge_extractions(cls, extractions: List[InvoiceExtractionSchema]) -> InvoiceExtractionSchema:
        """
        Deterministically merges extractions across multiple chunks.
        Preserves legitimate identical line items while eliminating chunk-overlap duplicates.
        """
        if not extractions:
            return InvoiceExtractionSchema()

        merged = InvoiceExtractionSchema()

        for chunk_idx, ext in enumerate(extractions):
            if not merged.invoice_number and ext.invoice_number:
                merged.invoice_number = ext.invoice_number
            if not merged.invoice_date and ext.invoice_date:
                merged.invoice_date = ext.invoice_date
            if not merged.supplier_name and ext.supplier_name:
                merged.supplier_name = ext.supplier_name
            if not merged.customer_name and ext.customer_name:
                merged.customer_name = ext.customer_name
            if not merged.currency and ext.currency:
                merged.currency = ext.currency

            if merged.subtotal is None and ext.subtotal is not None:
                merged.subtotal = ext.subtotal
            if merged.tax is None and ext.tax is not None:
                merged.tax = ext.tax
            if merged.total_amount is None and ext.total_amount is not None:
                merged.total_amount = ext.total_amount

            if chunk_idx == 0:
                merged.line_items.extend(ext.line_items)
            else:
                incoming_items = list(ext.line_items)
                if merged.line_items and incoming_items:
                    max_overlap_check = min(5, len(merged.line_items), len(incoming_items))
                    overlap_found = 0

                    for k in range(max_overlap_check, 0, -1):
                        tail_slice = merged.line_items[-k:]
                        head_slice = incoming_items[:k]
                        if all(line_items_equal(t, h) for t, h in zip(tail_slice, head_slice)):
                            overlap_found = k
                            break

                    merged.line_items.extend(incoming_items[overlap_found:])
                else:
                    merged.line_items.extend(incoming_items)

        return merged

    def extract_invoice_data(self, document_text: str) -> InvoiceExtractionSchema:
        """
        Splits text into safe-sized chunks.
        For massive 100-1000 page documents (>40,000 chars), extracts compact head and tail windows
        so header metadata and final reconciliation totals stay within free-tier TPM limits.
        """
        if not document_text or not document_text.strip():
            return InvoiceExtractionSchema()

        max_chunk_chars = 10000
        total_len = len(document_text)

        if total_len > 40000:
            window_chars = 4500
            logger.info(f"Massive document detected ({total_len} chars). Applying bounded head-tail windowing.")
            chunks = [document_text[:window_chars], document_text[-window_chars:]]
        elif total_len <= max_chunk_chars:
            return self.extract_from_chunk(document_text)
        else:
            chunks = []
            start = 0
            overlap = 600
            while start < total_len:
                end = min(start + max_chunk_chars, total_len)
                chunks.append(document_text[start:end])
                if end == total_len:
                    break
                start += max_chunk_chars - overlap

        extractions = []
        for idx, chunk in enumerate(chunks):
            if idx > 0:
                time.sleep(2.0)
            logger.info(f"Extracting AI data from chunk {idx + 1}/{len(chunks)}")
            res = self.extract_from_chunk(chunk)
            extractions.append(res)

        return self.merge_extractions(extractions)
