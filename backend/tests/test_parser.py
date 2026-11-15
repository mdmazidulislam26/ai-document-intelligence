"""
Unit tests for the document parsing service (PDF, CSV, Excel, Image).
"""

import os
import tempfile
import pytest
import pandas as pd
from services.document_parser import DocumentParserService


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
