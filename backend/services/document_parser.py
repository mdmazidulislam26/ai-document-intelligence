"""
Document parsing engine with memory-safe streaming, OpenCV deskew OCR,
and targeted page extraction for large multi-page PDFs (up to 1000 pages).
"""

import os
import io
import re
import logging
from typing import Generator, Tuple, List, Dict, Any
import cv2
import numpy as np
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import pandas as pd

logger = logging.getLogger("document_parser")
logger.setLevel(logging.INFO)

FINANCIAL_KEYWORDS = {
    "invoice", "tax invoice", "receipt", "bill to", "total", "subtotal",
    "amount due", "balance", "vat", "gst", "qty", "description", "unit price"
}


class DocumentParserService:
    @classmethod
    def deskew_image(cls, cv_img: np.ndarray) -> np.ndarray:
        """Corrects image skew angle up to +/- 45 degrees using OpenCV minimum area rectangle."""
        try:
            gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            coords = np.column_stack(np.where(thresh > 0))
            if len(coords) < 50:
                return cv_img
            angle = cv2.minAreaRect(coords)[-1]
            if angle < -45:
                angle = -(90 + angle)
            elif angle > 45:
                angle = 90 - angle
            else:
                angle = -angle

            if abs(angle) > 0.5:
                (h, w) = cv_img.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                rotated = cv2.warpAffine(cv_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
                return rotated
        except Exception as e:
            logger.debug(f"Deskew skipped: {e}")
        return cv_img

    @classmethod
    def ocr_page_image(cls, pil_img: Image.Image) -> str:
        """High-clarity adaptive OCR pipeline with deskew, upscaling, and Otsu binarization."""
        cv_img = np.array(pil_img.convert("RGB"))
        cv_img = cls.deskew_image(cv_img)

        h, w = cv_img.shape[:2]
        if w < 1600:
            scale = 2.0
            cv_img = cv2.resize(cv_img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
        # Apply adaptive contrast enhancement (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        custom_config = r"--oem 3 --psm 6"
        text = pytesseract.image_to_string(thresh, config=custom_config).strip()
        if not text:
            text = pytesseract.image_to_string(gray, config=r"--oem 3 --psm 3").strip()
        return text

    @classmethod
    def stream_pdf_pages(cls, file_path: str) -> Generator[Tuple[int, str], None, None]:
        """Memory-safe generator streaming one PDF page at a time with OCR fallback."""
        try:
            doc = fitz.open(file_path)
        except Exception as e:
            raise ValueError(f"Corrupted or invalid PDF file: {str(e)}")

        try:
            total_pages = len(doc)
            for page_index in range(total_pages):
                page = doc.load_page(page_index)
                text = page.get_text("text").strip()
                # Fallback to OCR if page has negligible digital text
                if len(text) < 50:
                    pix = page.get_pixmap(dpi=300)
                    pil_img = Image.open(io.BytesIO(pix.tobytes("png")))
                    text = cls.ocr_page_image(pil_img)
                yield (page_index + 1, text)
        finally:
            doc.close()

    @classmethod
    def parse_image_file(cls, file_path: str) -> str:
        """Parses standalone image files (PNG, JPG, TIFF) via OCR."""
        try:
            with Image.open(file_path) as img:
                return cls.ocr_page_image(img)
        except Exception as e:
            raise ValueError(f"Corrupted image file: {str(e)}")

    @classmethod
    def parse_spreadsheet(cls, file_path: str, ext: str) -> str:
        """Parses XLSX, XLS, and CSV files into tabular representations."""
        buffer = []
        try:
            if ext in [".xlsx", ".xls"]:
                excel_file = pd.ExcelFile(file_path)
                for sheet in excel_file.sheet_names:
                    df = pd.read_excel(excel_file, sheet_name=sheet).fillna("")
                    buffer.append(f"--- Sheet: {sheet} ---\n" + df.to_string(index=False))
            elif ext == ".csv":
                df = pd.read_csv(file_path).fillna("")
                buffer.append("--- CSV Records ---\n" + df.to_string(index=False))
        except Exception as e:
            raise ValueError(f"Corrupted spreadsheet file: {str(e)}")
        return "\n\n".join(buffer)

    @classmethod
    def extract_full_text(cls, file_path: str) -> Tuple[str, int]:
        """
        Extracts document text. For large PDFs, applies intelligent page scoring
        to ensure financial summaries, line items, and metadata are prioritized.
        """
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == ".pdf":
            pages_text = []
            page_scores = []
            page_count = 0

            # Stream pages one by one without keeping unneeded pixmaps in RAM
            for page_num, text in cls.stream_pdf_pages(file_path):
                page_count += 1
                pages_text.append((page_num, text))

                # Score page relevance based on financial keywords
                lower_text = text.lower()
                matches = sum(1 for kw in FINANCIAL_KEYWORDS if kw in lower_text)
                page_scores.append((page_num, matches, text))

            if page_count <= 10:
                # Up to 10 pages, retain full content
                full = [f"--- Page {p} ---\n{t}" for p, t in pages_text if t.strip()]
                return "\n\n".join(full), page_count

            # For large PDFs (up to 1000 pages):
            # Prioritize: First 3 pages, Last 3 pages, and top scoring financial pages
            selected_pages = set()
            for p in range(1, min(4, page_count + 1)):
                selected_pages.add(p)
            for p in range(max(1, page_count - 2), page_count + 1):
                selected_pages.add(p)

            # Sort by keyword matches descending
            sorted_by_score = sorted(page_scores, key=lambda x: x[1], reverse=True)
            for p_num, score, _ in sorted_by_score:
                if len(selected_pages) >= 15:
                    break
                if score > 0:
                    selected_pages.add(p_num)

            filtered = [
                f"--- Page {p} ---\n{t}"
                for p, t in pages_text
                if p in selected_pages and t.strip()
            ]
            return "\n\n".join(filtered), page_count

        elif ext in [".jpg", ".jpeg", ".png", ".tiff", ".tif"]:
            return cls.parse_image_file(file_path), 1
        elif ext in [".xlsx", ".xls", ".csv"]:
            return cls.parse_spreadsheet(file_path, ext), 1

        raise ValueError(f"Unsupported document format: {ext}")
