"""
Document parsing engine.
Supports digital PDFs, scanned image PDFs, raw images (JPG, PNG, TIFF),
and tabular spreadsheets (XLSX, XLS, CSV) with memory streaming for up to 1000+ pages.
"""

import os
import io
import math
import logging
from typing import Generator, Tuple, Optional
import cv2
import numpy as np
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import pandas as pd

logger = logging.getLogger("document_parser")
logger.setLevel(logging.INFO)


class DocumentParserService:
    """
    Robust document parser that extracts clean text from multiple file types.
    """

    @staticmethod
    def preprocess_image_for_ocr(pil_img: Image.Image) -> np.ndarray:
        """
        Applies grayscale, deskewing, and Otsu adaptive thresholding
        to improve OCR accuracy on noisy or poorly scanned documents.
        """
        # Convert PIL Image to OpenCV BGR/Grayscale format
        cv_img = np.array(pil_img.convert("RGB"))
        gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)

        # Deskew image if tilted
        coords = np.column_stack(np.where(gray > 0))
        if coords.size > 0:
            angle = cv2.minAreaRect(coords)[-1]
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle
            # Only rotate if the detected skew is significant
            if abs(angle) > 0.5 and abs(angle) < 45:
                (h, w) = gray.shape[:2]
                center = (w // 2, h // 2)
                rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
                gray = cv2.warpAffine(
                    gray,
                    rotation_matrix,
                    (w, h),
                    flags=cv2.INTER_CUBIC,
                    borderMode=cv2.BORDER_REPLICATE
                )

        # Contrast enhancement using CLAHE and Otsu thresholding
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast_enhanced = clahe.apply(gray)
        _, thresh = cv2.threshold(
            contrast_enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        return thresh

    @classmethod
    def ocr_page_image(cls, pil_img: Image.Image) -> str:
        """
        Preprocesses and extracts text from an image using Tesseract OCR.
        """
        processed_cv_img = cls.preprocess_image_for_ocr(pil_img)
        # Use Tesseract with automatic page segmentation (PSM 3)
        custom_config = r"--oem 3 --psm 3"
        text = pytesseract.image_to_string(processed_cv_img, config=custom_config)
        return text.strip()

    @classmethod
    def stream_pdf_pages(
        cls, file_path: str, batch_size: int = 10
    ) -> Generator[Tuple[int, str], None, None]:
        """
        Streams pages from a PDF one by one. If text is sparse (< 50 chars),
        renders page to image and performs OCR fallback.
        Memory safe for PDFs containing 1000+ pages.
        """
        try:
            doc = fitz.open(file_path)
        except Exception as e:
            logger.error(f"Failed to open PDF {file_path}: {str(e)}")
            raise ValueError(f"Corrupted or invalid PDF file: {str(e)}")

        total_pages = len(doc)
        logger.info(f"Processing PDF with {total_pages} total pages: {file_path}")

        try:
            for page_index in range(total_pages):
                page = doc.load_page(page_index)
                extracted_text = page.get_text("text").strip()

                # If text density is low, fall back to OCR
                if len(extracted_text) < 50:
                    logger.info(
                        f"Low text density ({len(extracted_text)} chars) on page {page_index + 1}. Running OCR..."
                    )
                    # Render page to pixmap at 200 DPI
                    pix = page.get_pixmap(dpi=200)
                    img_bytes = pix.tobytes("png")
                    pil_img = Image.open(io.BytesIO(img_bytes))
                    extracted_text = cls.ocr_page_image(pil_img)

                yield (page_index + 1, extracted_text)
        finally:
            doc.close()

    @classmethod
    def parse_image_file(cls, file_path: str) -> str:
        """
        Parses standalone image files (JPG, PNG, TIFF).
        """
        try:
            with Image.open(file_path) as img:
                return cls.ocr_page_image(img)
        except Exception as e:
            logger.error(f"Corrupted or unreadable image file {file_path}: {str(e)}")
            raise ValueError(f"Invalid or corrupted image: {str(e)}")

    @classmethod
    def parse_spreadsheet(cls, file_path: str, ext: str) -> str:
        """
        Parses all sheets of Excel (.xlsx, .xls) or CSV files into formatted tabular text.
        """
        try:
            buffer = []
            if ext in [".xlsx", ".xls"]:
                excel_file = pd.ExcelFile(file_path)
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(excel_file, sheet_name=sheet_name)
                    # Replace NaN with empty string
                    df = df.fillna("")
                    buffer.append(f"--- Sheet: {sheet_name} ---")
                    buffer.append(df.to_string(index=False))
            elif ext == ".csv":
                df = pd.read_csv(file_path)
                df = df.fillna("")
                buffer.append("--- CSV Data ---")
                buffer.append(df.to_string(index=False))
            else:
                raise ValueError(f"Unsupported spreadsheet format: {ext}")

            return "\n\n".join(buffer)
        except Exception as e:
            logger.error(f"Failed to parse spreadsheet {file_path}: {str(e)}")
            raise ValueError(f"Corrupted or invalid spreadsheet: {str(e)}")

    @classmethod
    def extract_full_text(cls, file_path: str, max_pages: Optional[int] = 100) -> Tuple[str, int]:
        """
        Unified extraction method that dispatches processing according to file extension.
        Returns extracted text and total pages/sheets processed.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == ".pdf":
            pages_text = []
            count = 0
            for page_num, text in cls.stream_pdf_pages(file_path):
                pages_text.append(f"--- Page {page_num} ---\n{text}")
                count += 1
                if max_pages and count >= max_pages:
                    logger.warning(f"Reached page limit cutoff ({max_pages} pages).")
                    break
            return "\n\n".join(pages_text), count

        elif ext in [".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp"]:
            text = cls.parse_image_file(file_path)
            return text, 1

        elif ext in [".xlsx", ".xls", ".csv"]:
            text = cls.parse_spreadsheet(file_path, ext)
            return text, 1

        else:
            raise ValueError(f"Unsupported file format: {ext}")
