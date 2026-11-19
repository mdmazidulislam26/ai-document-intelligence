"""
Automated unit tests for FileSecurityValidator and secure upload routing.
"""

import pytest
from services.file_security import FileSecurityValidator


def test_sanitize_filename_prevents_path_traversal():
    """Strips path traversal sequences like ../ and null bytes."""
    malicious_name = "../../../etc/passwd"
    sanitized = FileSecurityValidator.sanitize_filename(malicious_name)
    assert sanitized == "passwd"
    assert ".." not in sanitized

    windows_traversal = "..\\..\\boot.ini"
    sanitized_win = FileSecurityValidator.sanitize_filename(windows_traversal)
    assert ".." not in sanitized_win


def test_validate_valid_pdf_signature():
    """Passes true PDF content starting with %PDF- header."""
    valid_pdf = b"%PDF-1.4\n%test content"
    is_valid, msg = FileSecurityValidator.validate_file_content(valid_pdf, ".pdf")
    assert is_valid is True
    assert msg == ""


def test_reject_mismatched_signature():
    """Rejects binary executable or random text claiming to be a PDF."""
    fake_pdf = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00"
    is_valid, msg = FileSecurityValidator.validate_file_content(fake_pdf, ".pdf")
    assert is_valid is False
    assert "File signature mismatch" in msg


def test_validate_png_and_jpeg_signatures():
    """Validates real image magic bytes."""
    png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    is_valid, _ = FileSecurityValidator.validate_file_content(png_bytes, ".png")
    assert is_valid is True

    jpg_bytes = b"\xff\xd8\xff\xe0\x00\x10JFIF"
    is_valid, _ = FileSecurityValidator.validate_file_content(jpg_bytes, ".jpg")
    assert is_valid is True


def test_validate_tiff_and_xls_signatures():
    """Validates TIFF (little/big endian) and legacy Excel (.xls) magic bytes."""
    tiff_le = b"II*\x00\x08\x00\x00\x00"
    tiff_be = b"MM\x00*\x00\x00\x00\x08"
    assert FileSecurityValidator.validate_file_content(tiff_le, ".tiff")[0] is True
    assert FileSecurityValidator.validate_file_content(tiff_be, ".tif")[0] is True

    spoofed_tiff = b"%PDF-1.4\nfake"
    ok_t, msg_t = FileSecurityValidator.validate_file_content(spoofed_tiff, ".tiff")
    assert ok_t is False
    assert "signature mismatch" in msg_t.lower()

    valid_xls = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + (b"\x00" * 64)
    assert FileSecurityValidator.validate_file_content(valid_xls, ".xls")[0] is True

    spoofed_xls = b"PK\x03\x04not_an_xls"
    ok_x, msg_x = FileSecurityValidator.validate_file_content(spoofed_xls, ".xls")
    assert ok_x is False
    assert "signature mismatch" in msg_x.lower()


def test_reject_empty_file():
    """Rejects empty 0-byte file uploads."""
    is_valid, msg = FileSecurityValidator.validate_file_content(b"", ".csv")
    assert is_valid is False
    assert "empty" in msg.lower()


def test_validate_csv_structure():
    """Verifies CSV content validation."""
    valid_csv = b"Invoice,Supplier,Total\nINV-01,Test Corp,100.00\n"
    is_valid, _ = FileSecurityValidator.validate_file_content(valid_csv, ".csv")
    assert is_valid is True


def test_reject_unsupported_extension():
    """Rejects forbidden extensions."""
    is_valid, msg = FileSecurityValidator.validate_file_content(b"some content", ".exe")
    assert is_valid is False
    assert "Unsupported file extension" in msg
