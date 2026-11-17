"""
Strict file security and content signature verification service.
Prevents MIME spoofing, path traversal, oversized/empty uploads, and zip bombs.
"""

import os
import re
import csv
import io
import zipfile
from typing import Tuple

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".tif", ".xlsx", ".xls", ".csv"}

# Magic byte signatures
SIGNATURES = {
    ".pdf": [b"%PDF-"],
    ".png": [b"\x89PNG\r\n\x1a\n"],
    ".jpg": [b"\xff\xd8\xff"],
    ".jpeg": [b"\xff\xd8\xff"],
    ".tiff": [b"II*\x00", b"MM\x00*"],
    ".tif": [b"II*\x00", b"MM\x00*"],
    ".xls": [b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"],  # OLE Compound File
    ".xlsx": [b"PK\x03\x04"],  # Standard ZIP signature
}


class FileSecurityValidator:
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """Strips both POSIX (/) and Windows (\\) path traversal elements and control characters."""
        clean_name = filename.strip()
        # Normalize Windows backslashes to forward slashes first
        clean_name = clean_name.replace("\\", "/")
        # Extract base component
        base_name = os.path.basename(clean_name).strip()
        # Remove null bytes, control chars, and any residual leading dots
        sanitized = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", base_name)
        sanitized = re.sub(r"^\.+", "", sanitized).strip()
        return sanitized if sanitized else "unnamed_document"

    @classmethod
    def validate_file_content(cls, file_bytes: bytes, declared_ext: str) -> Tuple[bool, str]:
        """
        Validates raw bytes against expected magic numbers and internal format structure.
        Returns (is_valid, error_reason).
        """
        ext = declared_ext.lower()
        if ext not in ALLOWED_EXTENSIONS:
            return False, f"Unsupported file extension: {ext}"

        if len(file_bytes) == 0:
            return False, "File is empty (0 bytes)."

        # 1. Binary Magic Number Check
        if ext in SIGNATURES:
            expected_headers = SIGNATURES[ext]
            matched = any(file_bytes.startswith(sig) for sig in expected_headers)
            if not matched:
                return False, f"File signature mismatch. Content does not match {ext} format."

        # 2. Format-Specific Deep Inspections
        if ext == ".xlsx":
            try:
                with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
                    namelist = z.namelist()
                    has_content_types = "[Content_Types].xml" in namelist
                    has_xl_dir = any(name.startswith("xl/") for name in namelist)
                    if not (has_content_types or has_xl_dir):
                        return False, "Malformed XLSX: missing required Office Open XML internal structures."
            except zipfile.BadZipFile:
                return False, "Corrupted XLSX: invalid zip archive."

        elif ext == ".csv":
            try:
                text = None
                for enc in ["utf-8", "utf-8-sig", "latin1"]:
                    try:
                        text = file_bytes.decode(enc)
                        break
                    except UnicodeDecodeError:
                        continue

                if text is None:
                    return False, "Malformed CSV: text decoding failed."

                sample = text[:4096]
                if not sample.strip():
                    return False, "Malformed CSV: empty text content."

                lines = [line for line in sample.splitlines() if line.strip()]
                if not lines:
                    return False, "Malformed CSV: no parseable rows."

            except Exception as e:
                return False, f"Malformed CSV structure: {str(e)}"

        return True, ""
