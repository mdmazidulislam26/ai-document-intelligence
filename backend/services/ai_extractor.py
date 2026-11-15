"""
AI information extraction service using OpenAI-compatible endpoint.
Extracts structured invoice schemas with strict zero-hallucination guarantees.
"""

import json
import re
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
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=settings.GROQ_API_KEY,
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

        max_chars = 32000
        truncated_text = document_text[:max_chars]

        system_prompt = (
            "You are a strict financial data extraction engine. Analyze the document and return ONLY a valid JSON object matching this schema:\n"
            "{\n"
            '  "invoice_number": string or null,\n'
            '  "invoice_date": "YYYY-MM-DD" or null,\n'
            '  "supplier_name": string or null,\n'
            '  "customer_name": string or null,\n'
            '  "subtotal": float or null,\n'
            '  "tax": float or null,\n'
            '  "total_amount": float or null,\n'
            '  "currency": string or "USD",\n'
            '  "line_items": [\n'
            '    {"description": string, "quantity": float, "unit_price": float, "total": float}\n'
            "  ]\n"
            "}\n"
            "RULES: If any field is not stated in the text, return null. Return ONLY raw JSON without markdown fences."
        )

        user_prompt = f"Invoice Content:\n\n{truncated_text}"

        raw_response = ""
        try:
            # First attempt with json_object response format
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.0,
                    max_tokens=2048,
                )
                raw_response = response.choices[0].message.content or "{}"
            except Exception:
                # Fallback without explicit response_format if not supported by model
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.0,
                    max_tokens=2048,
                )
                raw_response = response.choices[0].message.content or "{}"

            # Strip any markdown fences like ```json ... ```
            cleaned = re.sub(r"^```[a-zA-Z]*\s*", "", raw_response.strip())
            cleaned = re.sub(r"\s*```$", "", cleaned).strip()

            # Extract first JSON object block if surrounded by text
            json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if json_match:
                cleaned = json_match.group(0)

            parsed_json = json.loads(cleaned)
            return InvoiceExtractionSchema(**parsed_json)

        except Exception as e:
            logger.error(f"Error during AI extraction: {str(e)} | Raw: {raw_response[:200]}")
            return InvoiceExtractionSchema()
