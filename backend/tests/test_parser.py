"""
Unit tests for the document parsing service (PDF, CSV, Excel, Image).
"""

import os
import tempfile
from unittest.mock import patch, MagicMock
import pytest
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from services.document_parser import DocumentParserService
from services.file_security import FileSecurityValidator


def test_parse_csv_spreadsheet():
    """Verifies CSV parsing converts cleanly into structured tabular text."""
    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w+", delete=False) as f:
        f.write("Invoice,Supplier,Total\nINV-101,Global Logistics,550.00\nINV-102,Tech Supply,1200.50\n")
        temp_path = f.name

    try:
        text, pages = DocumentParserService.extract_full_text(temp_path)
        assert pages == 1
        assert "Global Logistics" in text
        assert "550" in text
    finally:
        os.remove(temp_path)


def test_corrupted_file_handling():
    """Ensures corrupted files raise ValueError gracefully without crashing the pipeline."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", mode="wb", delete=False) as f:
        f.write(b"%PDF-1.4 Corrupted content totally invalid bytes")
        temp_path = f.name

    try:
        with pytest.raises(ValueError):
            DocumentParserService.extract_full_text(temp_path)
    finally:
        os.remove(temp_path)


def test_parse_tiff_image_with_real_ocr():
    """Creates a real TIFF invoice image, validates magic bytes, and extracts text via OCR."""
    img = Image.new("RGB", (1200, 500), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default(size=32)
    except TypeError:
        font = ImageFont.load_default()

    lines = [
        "INVOICE: INV-TIF-301",
        "Supplier: Nordic Paper Supply",
        "Subtotal: 100.00 USD",
        "Total Amount: 110.00 USD",
    ]
    y = 60
    for line in lines:
        draw.text((60, y), line, fill=(10, 10, 10), font=font)
        y += 70

    fd, temp_path = tempfile.mkstemp(suffix=".tiff")
    os.close(fd)
    try:
        img.save(temp_path, format="TIFF")
        with open(temp_path, "rb") as f:
            is_valid, err = FileSecurityValidator.validate_file_content(f.read(), ".tiff")
        assert is_valid is True, err

        text, pages = DocumentParserService.extract_full_text(temp_path)
        assert pages == 1
        assert any(token in text for token in ("301", "110", "Nordic", "INVOICE"))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_parse_xls_multisheet_and_corrupted_handling():
    """Verifies corrupted .xls raises ValueError and multi-sheet .xls invokes xlrd/pandas parsing."""
    fd, corrupt_path = tempfile.mkstemp(suffix=".xls")
    os.close(fd)
    try:
        with open(corrupt_path, "wb") as f:
            f.write(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1corrupted_biff_stream")
        with pytest.raises(ValueError, match="Corrupted spreadsheet file"):
            DocumentParserService.extract_full_text(corrupt_path)

        mock_excel = MagicMock()
        mock_excel.sheet_names = ["Summary", "Line_Items"]
        df_summary = pd.DataFrame([{"Invoice": "XLS-101", "Total": 250.00}])
        df_items = pd.DataFrame([{"Description": "Cloud Node", "Total": 250.00}])

        with patch("services.document_parser.pd.ExcelFile", return_value=mock_excel), \
             patch("services.document_parser.pd.read_excel", side_effect=[df_summary, df_items]):
            text, pages = DocumentParserService.extract_full_text(corrupt_path)
            assert pages == 1
            assert "--- Sheet: Summary ---" in text
            assert "XLS-101" in text
            assert "--- Sheet: Line_Items ---" in text
            assert "Cloud Node" in text
    finally:
        if os.path.exists(corrupt_path):
            os.remove(corrupt_path)
