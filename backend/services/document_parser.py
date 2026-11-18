"""
Document parsing engine with memory-safe streaming, OpenCV deskew OCR,
configurable OCR resolution, partial-corruption resilience, and zero page-cap
for large multi-page PDFs (up to 1000 pages).
"""

import os
import io
import logging
from typing import Generator, Tuple, List, Optional
import cv2
import numpy as np
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import pandas as pd

logger = logging.getLogger("document_parser")
logger.setLevel(logging.INFO)

# Configurable OCR settings
OCR_DPI: int = int(os.getenv("OCR_DPI", "200"))
OCR_MIN_TEXT_CHARS: int = int(os.getenv("OCR_MIN_TEXT_CHARS", "50"))


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
        """High-clarity adaptive OCR pipeline with deskew and Otsu binarization."""
        cv_img = np.array(pil_img.convert("RGB"))
        cv_img = cls.deskew_image(cv_img)

        h, w = cv_img.shape[:2]
        if w < 1600:
            scale = 1.5
            cv_img = cv2.resize(cv_img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
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
        """
        Memory-safe generator streaming one PDF page at a time.
        Releases image buffers immediately after processing to prevent RAM bloat on 1000-page files.
        Resilient to individual page rendering corruptions.
        """
        try:
            doc = fitz.open(file_path)
        except Exception as e:
            raise ValueError(f"Corrupted or invalid PDF file: {str(e)}")

        try:
            total_pages = len(doc)
            for page_index in range(total_pages):
                page_num = page_index + 1
                try:
                    page = doc.load_page(page_index)
                    text = page.get_text("text").strip()

                    # Fallback to OCR only if digital text is insufficient (< 50 chars)
                    if len(text) < OCR_MIN_TEXT_CHARS:
                        try:
                            pix = page.get_pixmap(dpi=OCR_DPI)
                            img_bytes = pix.tobytes("png")
                            del pix  # Immediately release PyMuPDF pixmap memory

                            with Image.open(io.BytesIO(img_bytes)) as pil_img:
                                text = cls.ocr_page_image(pil_img)
                        except Exception as ocr_err:
                            logger.warning(f"OCR failed on page {page_num} of {file_path}: {ocr_err}")
                            text = ""

                    yield (page_num, text)

                except Exception as page_err:
                    logger.warning(f"Skipping corrupted page {page_num} in {file_path}: {page_err}")
                    yield (page_num, f"[Page {page_num} unreadable due to corruption]")

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
        Extracts all pages from PDF, image, or spreadsheet without any arbitrary page-cap truncation.
        Every valid page is preserved in stream order with its page provenance.
        """
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == ".pdf":
            pages_output = []
            page_count = 0

            for page_num, text in cls.stream_pdf_pages(file_path):
                page_count += 1
                if text.strip():
                    pages_output.append(f"--- Page {page_num} ---\n{text}")

            full_text = "\n\n".join(pages_output)
            return full_text, page_count

        elif ext in [".jpg", ".jpeg", ".png", ".tiff", ".tif"]:
            return cls.parse_image_file(file_path), 1
        elif ext in [".xlsx", ".xls", ".csv"]:
            return cls.parse_spreadsheet(file_path, ext), 1

        raise ValueError(f"Unsupported document format: {ext}")
