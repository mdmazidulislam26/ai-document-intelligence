"""
Document parsing engine with automatic 2x image upscaling for crystal-clear OCR.
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


class DocumentParserService:
    @classmethod
    def ocr_page_image(cls, pil_img: Image.Image) -> str:
        # Convert to OpenCV RGB
        cv_img = np.array(pil_img.convert("RGB"))
        
        # Upscale 2x if image dimensions are small (preserves decimal dots '.' for OCR)
        h, w = cv_img.shape[:2]
        if w < 1600:
            scale = 2.0
            cv_img = cv2.resize(cv_img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
        
        # High-clarity thresholding for Tesseract
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        custom_config = r"--oem 3 --psm 6"
        text = pytesseract.image_to_string(thresh, config=custom_config).strip()
        
        if not text:
            text = pytesseract.image_to_string(gray, config=r"--oem 3 --psm 3").strip()
            
        return text

    @classmethod
    def stream_pdf_pages(cls, file_path: str) -> Generator[Tuple[int, str], None, None]:
        doc = fitz.open(file_path)
        try:
            for page_index in range(len(doc)):
                page = doc.load_page(page_index)
                text = page.get_text("text").strip()
                if len(text) < 50:
                    pix = page.get_pixmap(dpi=300)
                    pil_img = Image.open(io.BytesIO(pix.tobytes("png")))
                    text = cls.ocr_page_image(pil_img)
                yield (page_index + 1, text)
        finally:
            doc.close()

    @classmethod
    def parse_image_file(cls, file_path: str) -> str:
        with Image.open(file_path) as img:
            return cls.ocr_page_image(img)

    @classmethod
    def parse_spreadsheet(cls, file_path: str, ext: str) -> str:
        buffer = []
        if ext in [".xlsx", ".xls"]:
            excel_file = pd.ExcelFile(file_path)
            for sheet in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet).fillna("")
                buffer.append(f"Sheet: {sheet}\n" + df.to_string(index=False))
        elif ext == ".csv":
            df = pd.read_csv(file_path).fillna("")
            buffer.append("CSV Records:\n" + df.to_string(index=False))
        return "\n\n".join(buffer)

    @classmethod
    def extract_full_text(cls, file_path: str) -> Tuple[str, int]:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext == ".pdf":
            pages_text = []
            count = 0
            for page_num, text in cls.stream_pdf_pages(file_path):
                pages_text.append(f"--- Page {page_num} ---\n{text}")
                count += 1
            return "\n\n".join(pages_text), count
        elif ext in [".jpg", ".jpeg", ".png", ".tiff", ".tif"]:
            return cls.parse_image_file(file_path), 1
        elif ext in [".xlsx", ".xls", ".csv"]:
            return cls.parse_spreadsheet(file_path, ext), 1
        raise ValueError(f"Unsupported format: {ext}")
