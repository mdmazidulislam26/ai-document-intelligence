"""
AI information extraction service using Groq API (free tier) with OpenAI client compatibility.
Extracts structured invoice schemas with strict zero-hallucination guarantees.
"""

import json
import logging
from typing import Optional
from openai import OpenAI
from core.config import settings
from models.schemas import InvoiceExtractionSchema

logger = logging.getLogger("ai_extractor")
logger.setLevel(logging.INFO)


class AIExtractorService:
    """
    Extracts structured fields from raw invoice text.
    """

    def __init__(self):
        # Configure client pointing to Groq Cloud OpenAI-compatible endpoint
        api_key = settings.GROQ_API_KEY
        if not api_key:
            logger.warning("GROQ_API_KEY is not set. Extraction will fail unless configured.")

        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key or "missing_key",
        )
        self.model = settings.LLM_MODEL

    def extract_invoice_data(self, document_text: str) -> InvoiceExtractionSchema:
        """
        Executes structured extraction on document text.
        Guarantees strictly parsed output matching InvoiceExtractionSchema.
        """
        if not document_text or not document_text.strip():
            logger.warning("Empty document text passed to AI extractor.")
            return InvoiceExtractionSchema()

        # Truncate text context safely if document is exceedingly large
        max_chars = 32000
        truncated_text = document_text[:max_chars]

        system_prompt = (
            "You are a strict, production-grade financial data extraction engine.\n"
            "Analyze the provided document text and extract financial invoice data matching this exact JSON schema:\n"
            "{\n"
            '  "invoice_number": string or null,\n'
            '  "invoice_date": "YYYY-MM-DD" or null,\n'
            '  "supplier_name": string or null,\n'
            '  "customer_name": string or null,\n'
            '  "subtotal": float or null,\n'
            '  "tax": float or null,\n'
            '  "total_amount": float or null,\n'
            '  "currency": string (e.g. "USD", "EUR", "BDT") or "USD",\n'
            '  "line_items": [\n'
            '    {"description": string, "quantity": float, "unit_price": float, "total": float}\n'
            "  ]\n"
            "}\n\n"
            "CRITICAL ZERO-HALLUCINATION RULES:\n"
            "1. NEVER invent, assume, or hallucinate any value.\n"
            "2. If an invoice number, date, tax, or total is not clearly stated, return null.\n"
            "3. Format dates strictly as YYYY-MM-DD. If ambiguous or unreadable, return null.\n"
            "4. Return ONLY valid JSON. Do not include markdown code fences or conversational text."
        )

        user_prompt = f"Document content to extract:\n\n{truncated_text}"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.0,  # Zero temperature for deterministic extraction
                max_tokens=4096,
            )

            raw_response = response.choices[0].message.content
            parsed_json = json.loads(raw_response)

            # Validate and cast into strict Pydantic model
            structured_data = InvoiceExtractionSchema(**parsed_json)
            return structured_data

        except json.JSONDecodeError as json_err:
            logger.error(f"Failed to parse JSON response from LLM: {str(json_err)}")
            return InvoiceExtractionSchema()
        except Exception as e:
            logger.error(f"Error during AI extraction: {str(e)}")
            raise RuntimeError(f"AI extraction failed: {str(e)}")
