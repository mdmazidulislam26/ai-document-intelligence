"""
AI information extraction service.
Seamlessly parses multi-row CSV/Excel spreadsheets, extracting header metadata
from primary entries and calculating accurate line-item reconciliations.
"""

import json
import re
import logging
from openai import OpenAI
from core.config import settings
from models.schemas import InvoiceExtractionSchema

logger = logging.getLogger("ai_extractor")
logger.setLevel(logging.INFO)


class AIExtractorService:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=settings.GROQ_API_KEY,
        )
        self.model = settings.LLM_MODEL

    def extract_invoice_data(self, document_text: str) -> InvoiceExtractionSchema:
        if not document_text or not document_text.strip():
            return InvoiceExtractionSchema()

        truncated_text = document_text[:32000]

        system_prompt = (
            "You are an expert financial data extraction engine. Analyze the document and return ONLY a valid JSON object matching this schema:\n"
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
            "RULES FOR CSV / SPREADSHEETS:\n"
            "1. 'supplier_name': Extract the supplier/vendor name from the first row or primary vendor.\n"
            "2. 'customer_name': Extract the common billed customer across rows.\n"
            "3. 'invoice_number': Extract the invoice number from the first row.\n"
            "4. 'invoice_date': Extract the date from the first row in YYYY-MM-DD format.\n"
            "5. 'line_items': Each row MUST be an item in the array. 'total' for each row is its subtotal amount.\n"
            "6. 'subtotal': Mathematical sum of all row subtotals.\n"
            "7. 'tax': Mathematical sum of all row taxes.\n"
            "8. 'total_amount': Subtotal + Tax.\n"
            "9. Return ONLY raw JSON without markdown code fences."
        )

        user_prompt = f"Document Content:\n\n{truncated_text}"
        raw_response = ""

        try:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.0,
                    max_tokens=3000,
                )
                raw_response = response.choices[0].message.content or "{}"
            except Exception:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.0,
                    max_tokens=3000,
                )
                raw_response = response.choices[0].message.content or "{}"

            cleaned = re.sub(r"^```[a-zA-Z]*\s*", "", raw_response.strip())
            cleaned = re.sub(r"\s*```$", "", cleaned).strip()

            json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if json_match:
                cleaned = json_match.group(0)

            parsed_json = json.loads(cleaned)
            return InvoiceExtractionSchema(**parsed_json)

        except Exception as e:
            logger.error(f"Error during AI extraction: {str(e)} | Raw: {raw_response[:200]}")
            return InvoiceExtractionSchema()
