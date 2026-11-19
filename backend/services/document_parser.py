"""
Document parsing engine with memory-safe streaming, noise-resilient OpenCV deskew OCR,
configurable OCR resolution, partial-corruption resilience, and zero page-cap
for large multi-page PDFs (up to 1000 pages).
"""

import os
import io
import logging
from typing import Generator, Tuple
import cv2
import numpy as np
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import pandas as pd

logger = logging.getLogger("document_parser")
logger.setLevel(logging.INFO)

OCR_DPI: int = int(os.getenv("OCR_DPI", "200"))
OCR_MIN_TEXT_CHARS: int = int(os.getenv("OCR_MIN_TEXT_CHARS", "50"))


class DocumentParserService:
    @classmethod
    def _alnum_score(cls, text: str) -> int:
        return sum(1 for ch in text if ch.isalnum())

    @classmethod
    def deskew_image(cls, cv_img: np.ndarray) -> np.ndarray:
        """
        Corrects small document skew angles (+/- 15 degrees) safely.
        Uses median blur + adaptive thresholding so uniform background noise
        does not distort minAreaRect angle estimation.
        """
        try:
            gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
            denoised = cv2.medianBlur(gray, 3)
            thresh = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 15
            )
            kernel = np.ones((2, 2), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

            coords = np.column_stack(np.where(cleaned > 0))
            if len(coords) < 100:
                return cv_img

            angle = cv2.minAreaRect(coords)[-1]
            if angle < -45:
                angle = -(90 + angle)
            elif angle > 45:
                angle = 90 - angle
            else:
                angle = -angle

            if 0.5 < abs(angle) <= 15.0:
                (h, w) = cv_img.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                return cv2.warpAffine(cv_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        except Exception as e:
            logger.debug(f"Deskew skipped: {e}")
        return cv_img

    @classmethod
    def ocr_page_image(cls, pil_img: Image.Image) -> str:
        """Noise-resilient OCR pipeline using adaptive thresholding and alphanumeric scoring."""
        orig_cv = np.array(pil_img.convert("RGB"))
        cv_img = cls.deskew_image(orig_cv)

        h, w = cv_img.shape[:2]
        if w < 1600:
            scale = 1.5
            cv_img = cv2.resize(cv_img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
        denoised = cv2.medianBlur(gray, 3)
        adaptive = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 12
        )

        best_text = pytesseract.image_to_string(adaptive, config=r"--oem 3 --psm 6").strip()
        best_score = cls._alnum_score(best_text)

        if best_score < 60:
            _, otsu = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            orig_gray = cv2.cvtColor(orig_cv, cv2.COLOR_RGB2GRAY)
            candidates = [
                pytesseract.image_to_string(otsu, config=r"--oem 3 --psm 6").strip(),
                pytesseract.image_to_string(gray, config=r"--oem 3 --psm 3").strip(),
                pytesseract.image_to_string(orig_gray, config=r"--oem 3 --psm 3").strip(),
            ]
            for cand in candidates:
                score = cls._alnum_score(cand)
                if score > best_score:
                    best_text = cand
                    best_score = score

        return best_text

    @classmethod
    def stream_pdf_pages(cls, file_path: str) -> Generator[Tuple[int, str], None, None]:
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

                    if len(text) < OCR_MIN_TEXT_CHARS:
                        try:
                            pix = page.get_pixmap(dpi=OCR_DPI)
                            img_bytes = pix.tobytes("png")
                            del pix

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
        try:
            with Image.open(file_path) as img:
                return cls.ocr_page_image(img)
        except Exception as e:
            raise ValueError(f"Corrupted image file: {str(e)}")

    @classmethod
    def parse_spreadsheet(cls, file_path: str, ext: str) -> str:
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
