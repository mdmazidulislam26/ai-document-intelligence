"""
Reproducible multi-format labeled benchmark dataset generator for GHR-06.
Generates 10 labeled financial documents across:
- Digital PDFs (1-page and 12-page multi-page)
- Scanned image-only PDFs (clean 2-page and skewed/noisy 1-page)
- PNG and degraded/skewed JPG images
- Multi-sheet XLSX workbook and CSV file
- Incomplete (null fields for hallucination measurement) and math-discrepancy PDFs
"""

import os
import io
import json
import fitz  # PyMuPDF
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "benchmark_dataset")
FILES_DIR = os.path.join(DATASET_DIR, "files")
MANIFEST_PATH = os.path.join(DATASET_DIR, "dataset_manifest.json")


def _get_font(size: int = 24):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def _render_lines_to_image(
    lines: list[str],
    width: int = 1500,
    height: int = 1800,
    font_size: int = 24,
    skew_deg: float = 0.0,
    noisy: bool = False,
    low_contrast: bool = False,
    seed: int = 42,
) -> Image.Image:
    bg_val = 232 if low_contrast else 255
    fg_val = 55 if low_contrast else 10
    img = Image.new("RGB", (width, height), color=(bg_val, bg_val, bg_val))
    draw = ImageDraw.Draw(img)
    font = _get_font(font_size)

    y = 70
    line_step = int(font_size * 1.6)
    for line in lines:
        draw.text((70, y), line, fill=(fg_val, fg_val, fg_val), font=font)
        y += line_step

    if noisy:
        rng = np.random.default_rng(seed)
        arr = np.array(img, dtype=np.int16)
        noise = rng.normal(0, 12, arr.shape).astype(np.int16)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(arr)
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

    if abs(skew_deg) > 0.01:
        img = img.rotate(skew_deg, expand=False, fillcolor=(bg_val, bg_val, bg_val))

    return img


def _write_digital_pdf(path: str, pages_lines: list[list[str]]) -> None:
    doc = fitz.open()
    for page_lines in pages_lines:
        page = doc.new_page(width=595, height=842)
        text = "\n".join(page_lines)
        page.insert_text((45, 50), text, fontsize=10.5, fontname="cour")
    doc.save(path)
    doc.close()


def _write_scanned_pdf(path: str, images: list[Image.Image]) -> None:
    doc = fitz.open()
    for img in images:
        page = doc.new_page(width=595, height=842)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        page.insert_image(page.rect, stream=buf.getvalue())
    doc.save(path)
    doc.close()


def build_dataset() -> list[dict]:
    os.makedirs(FILES_DIR, exist_ok=True)
    manifest = []

    # 1. Clean 1-page Digital PDF
    f1 = os.path.join(FILES_DIR, "01_digital_standard.pdf")
    _write_digital_pdf(f1, [[
        "====================================================",
        "INVOICE",
        "====================================================",
        "Invoice Number: INV-2024-8801",
        "Invoice Date: 2024-05-15",
        "Supplier: TechFlow Solutions Ltd.",
        "Customer: Apex Innovations Inc.",
        "----------------------------------------------------",
        "Item Description                  Qty  Price   Total",
        "Cloud Server Hosting               2   150.00  300.00",
        "Cybersecurity Audit                1   200.00  200.00",
        "Managed DNS Service                1    50.00   50.00",
        "----------------------------------------------------",
        "Subtotal: 550.00 USD",
        "Tax (10%): 55.00 USD",
        "Total Amount: 605.00 USD",
    ]])
    manifest.append({
        "id": "doc_01",
        "file": "files/01_digital_standard.pdf",
        "category": "digital_pdf",
        "description": "Clean 1-page digital PDF invoice",
        "expected_math_valid": True,
        "ground_truth": {
            "invoice_number": "INV-2024-8801",
            "invoice_date": "2024-05-15",
            "supplier_name": "TechFlow Solutions Ltd.",
            "customer_name": "Apex Innovations Inc.",
            "subtotal": 550.00,
            "tax": 55.00,
            "total_amount": 605.00,
            "currency": "USD",
            "line_items": [
                {"description": "Cloud Server Hosting", "quantity": 2, "unit_price": 150.00, "total": 300.00},
                {"description": "Cybersecurity Audit", "quantity": 1, "unit_price": 200.00, "total": 200.00},
                {"description": "Managed DNS Service", "quantity": 1, "unit_price": 50.00, "total": 50.00},
            ],
        },
    })

    # 2. 12-Page Multi-Page Digital PDF
    f2 = os.path.join(FILES_DIR, "02_multipage_12pages.pdf")
    pages_12 = [
        [
            "MASTER SERVICE INVOICE & STATEMENT",
            "Invoice Number: INV-MP-1200",
            "Invoice Date: 2024-07-01",
            "Supplier: Horizon Enterprise Cloud Corp.",
            "Customer: Metro Retail Holdings",
            "Currency: USD",
            "Page 1 of 12 - Billing Header & Scope",
        ],
        ["Page 2 of 12 - Standard Terms and Conditions", "Net 30 days payment required."],
    ]
    mp_items = []
    for p_idx in range(3, 10):
        item_a = f"Compute Node Cluster {p_idx}A"
        item_b = f"Storage Volume Tier {p_idx}B"
        mp_items.append({"description": item_a, "quantity": 1, "unit_price": 100.00, "total": 100.00})
        mp_items.append({"description": item_b, "quantity": 1, "unit_price": 100.00, "total": 100.00})
        pages_12.append([
            f"Page {p_idx} of 12 - Itemized Usage Charges",
            f"Item: {item_a} | Qty: 1 | Unit Price: 100.00 | Total: 100.00",
            f"Item: {item_b} | Qty: 1 | Unit Price: 100.00 | Total: 100.00",
        ])
    pages_12.append(["Page 10 of 12 - SLA Compliance Appendix", "Uptime achieved: 99.98%."])
    pages_12.append(["Page 11 of 12 - Regional Tax Notice", "Standard rate applied."])
    pages_12.append([
        "Page 12 of 12 - Final Summary",
        "Invoice Number: INV-MP-1200",
        "Subtotal: 1400.00 USD",
        "Tax: 140.00 USD",
        "Total Amount: 1540.00 USD",
    ])
    _write_digital_pdf(f2, pages_12)
    manifest.append({
        "id": "doc_02",
        "file": "files/02_multipage_12pages.pdf",
        "category": "multipage_pdf",
        "description": "12-page digital PDF with line items across pages 3-9 and totals on page 12",
        "expected_math_valid": True,
        "ground_truth": {
            "invoice_number": "INV-MP-1200",
            "invoice_date": "2024-07-01",
            "supplier_name": "Horizon Enterprise Cloud Corp.",
            "customer_name": "Metro Retail Holdings",
            "subtotal": 1400.00,
            "tax": 140.00,
            "total_amount": 1540.00,
            "currency": "USD",
            "line_items": mp_items,
        },
    })

    # 3. 2-Page Clean Scanned PDF (Zero embedded text -> OCR)
    f3 = os.path.join(FILES_DIR, "03_scanned_clean.pdf")
    img3_p1 = _render_lines_to_image([
        "COMMERCIAL INVOICE",
        "Invoice Number: SCN-4401",
        "Invoice Date: 2024-06-10",
        "Supplier: Nordic Paper Supply",
        "Customer: Summit Print Works",
        "Currency: EUR",
        "----------------------------------------",
        "Item: A4 Bond Paper Pallet  Qty: 2  Unit: 120.00  Total: 240.00",
    ])
    img3_p2 = _render_lines_to_image([
        "COMMERCIAL INVOICE - PAGE 2",
        "Invoice Number: SCN-4401",
        "Item: Packaging Tape Rolls  Qty: 4  Unit: 15.00  Total: 60.00",
        "----------------------------------------",
        "Subtotal: 300.00 EUR",
        "Tax: 30.00 EUR",
        "Total Amount: 330.00 EUR",
    ])
    _write_scanned_pdf(f3, [img3_p1, img3_p2])
    manifest.append({
        "id": "doc_03",
        "file": "files/03_scanned_clean.pdf",
        "category": "scanned_pdf",
        "description": "2-page raster-only scanned PDF requiring Tesseract OCR",
        "expected_math_valid": True,
        "ground_truth": {
            "invoice_number": "SCN-4401",
            "invoice_date": "2024-06-10",
            "supplier_name": "Nordic Paper Supply",
            "customer_name": "Summit Print Works",
            "subtotal": 300.00,
            "tax": 30.00,
            "total_amount": 330.00,
            "currency": "EUR",
            "line_items": [
                {"description": "A4 Bond Paper Pallet", "quantity": 2, "unit_price": 120.00, "total": 240.00},
                {"description": "Packaging Tape Rolls", "quantity": 4, "unit_price": 15.00, "total": 60.00},
            ],
        },
    })

    # 4. Poor-Quality Skewed + Noisy Scanned PDF
    f4 = os.path.join(FILES_DIR, "04_scanned_skewed_noisy.pdf")
    img4 = _render_lines_to_image(
        [
            "TAX INVOICE",
            "Invoice Number: SKW-7710",
            "Invoice Date: 2024-08-05",
            "Supplier: Pacific Freight Logistics",
            "Customer: Harbor Imports LLC",
            "Item: Container Drayage  Qty: 1  Unit: 450.00  Total: 450.00",
            "Subtotal: 450.00 USD",
            "Tax: 45.00 USD",
            "Total Amount: 495.00 USD",
        ],
        skew_deg=2.5,
        noisy=True,
        low_contrast=True,
        seed=104,
    )
    _write_scanned_pdf(f4, [img4])
    manifest.append({
        "id": "doc_04",
        "file": "files/04_scanned_skewed_noisy.pdf",
        "category": "scanned_pdf_poor",
        "description": "Skewed (2.5 deg), noisy, low-contrast scanned PDF",
        "expected_math_valid": True,
        "ground_truth": {
            "invoice_number": "SKW-7710",
            "invoice_date": "2024-08-05",
            "supplier_name": "Pacific Freight Logistics",
            "customer_name": "Harbor Imports LLC",
            "subtotal": 450.00,
            "tax": 45.00,
            "total_amount": 495.00,
            "currency": "USD",
            "line_items": [
                {"description": "Container Drayage", "quantity": 1, "unit_price": 450.00, "total": 450.00},
            ],
        },
    })

    # 5. Clean PNG Retail Receipt (missing tax -> null)
    f5 = os.path.join(FILES_DIR, "05_receipt_clean.png")
    img5 = _render_lines_to_image([
        "RETAIL RECEIPT",
        "Vendor: SuperMart Express",
        "Receipt No: REC-7741",
        "Date: 2024-04-12",
        "Customer: John Doe",
        "Office Supplies  Qty: 1  Unit: 120.00  Total: 120.00",
        "Packaging Paper  Qty: 1  Unit: 30.00   Total: 30.00",
        "Subtotal: 150.00 USD",
        "Total: 150.00 USD",
    ])
    img5.save(f5, format="PNG")
    manifest.append({
        "id": "doc_05",
        "file": "files/05_receipt_clean.png",
        "category": "png_image",
        "description": "Clean PNG receipt with no tax field (tests null tax preservation)",
        "expected_math_valid": True,
        "ground_truth": {
            "invoice_number": "REC-7741",
            "invoice_date": "2024-04-12",
            "supplier_name": "SuperMart Express",
            "customer_name": "John Doe",
            "subtotal": 150.00,
            "tax": None,
            "total_amount": 150.00,
            "currency": "USD",
            "line_items": [
                {"description": "Office Supplies", "quantity": 1, "unit_price": 120.00, "total": 120.00},
                {"description": "Packaging Paper", "quantity": 1, "unit_price": 30.00, "total": 30.00},
            ],
        },
    })

    # 6. Poor-Quality Skewed JPEG Photo
    f6 = os.path.join(FILES_DIR, "06_invoice_poor_photo.jpg")
    img6 = _render_lines_to_image(
        [
            "INVOICE",
            "Invoice Number: JPG-3092",
            "Date: 2024-09-18",
            "Supplier: Metro Hardware Supply",
            "Customer: Greenfield Builders",
            "Industrial Drill Kit  Qty: 2  Unit: 125.00  Total: 250.00",
            "Subtotal: 250.00 USD",
            "Tax: 25.00 USD",
            "Total Amount: 275.00 USD",
        ],
        skew_deg=-2.5,
        noisy=True,
        low_contrast=True,
        seed=106,
    )
    img6.save(f6, format="JPEG", quality=60)
    manifest.append({
        "id": "doc_06",
        "file": "files/06_invoice_poor_photo.jpg",
        "category": "jpg_image_poor",
        "description": "Poor-quality compressed JPEG (-2.5 deg skew, low contrast, noise)",
        "expected_math_valid": True,
        "ground_truth": {
            "invoice_number": "JPG-3092",
            "invoice_date": "2024-09-18",
            "supplier_name": "Metro Hardware Supply",
            "customer_name": "Greenfield Builders",
            "subtotal": 250.00,
            "tax": 25.00,
            "total_amount": 275.00,
            "currency": "USD",
            "line_items": [
                {"description": "Industrial Drill Kit", "quantity": 2, "unit_price": 125.00, "total": 250.00},
            ],
        },
    })

    # 7. Multi-Sheet Excel (.xlsx) Workbook
    f7 = os.path.join(FILES_DIR, "07_multisheet_workbook.xlsx")
    with pd.ExcelWriter(f7, engine="openpyxl") as writer:
        pd.DataFrame([
            {
                "Invoice Number": "XLS-9001",
                "Invoice Date": "2024-06-20",
                "Supplier": "EuroTech Consulting GmbH",
                "Customer": "Alpine Finance AG",
                "Currency": "EUR",
                "Subtotal": 800.00,
                "Tax": 160.00,
                "Total Amount": 960.00,
            }
        ]).to_excel(writer, sheet_name="Invoice_Summary", index=False)
        pd.DataFrame([
            {"Invoice Number": "XLS-9001", "Item Description": "Security Architecture Review", "Quantity": 2, "Unit Price": 250.00, "Total": 500.00},
            {"Invoice Number": "XLS-9001", "Item Description": "Penetration Testing", "Quantity": 1, "Unit Price": 300.00, "Total": 300.00},
        ]).to_excel(writer, sheet_name="Line_Items", index=False)
    manifest.append({
        "id": "doc_07",
        "file": "files/07_multisheet_workbook.xlsx",
        "category": "xlsx_multisheet",
        "description": "Multi-sheet XLSX workbook with summary and itemized sheets",
        "expected_math_valid": True,
        "ground_truth": {
            "invoice_number": "XLS-9001",
            "invoice_date": "2024-06-20",
            "supplier_name": "EuroTech Consulting GmbH",
            "customer_name": "Alpine Finance AG",
            "subtotal": 800.00,
            "tax": 160.00,
            "total_amount": 960.00,
            "currency": "EUR",
            "line_items": [
                {"description": "Security Architecture Review", "quantity": 2, "unit_price": 250.00, "total": 500.00},
                {"description": "Penetration Testing", "quantity": 1, "unit_price": 300.00, "total": 300.00},
            ],
        },
    })

    # 8. Multi-Row CSV Invoice (GBP)
    f8 = os.path.join(FILES_DIR, "08_services_invoice.csv")
    df_csv = pd.DataFrame([
        {
            "Invoice Number": "CSV-5501",
            "Invoice Date": "2024-06-15",
            "Supplier": "Britannia Cloud Ltd",
            "Customer": "Thames Analytics",
            "Item Description": "Dedicated Compute Node",
            "Quantity": 2,
            "Unit Price": 250.00,
            "Total": 500.00,
            "Subtotal": 900.00,
            "Tax": 180.00,
            "Total Amount": 1080.00,
            "Currency": "GBP",
        },
        {
            "Invoice Number": "CSV-5501",
            "Invoice Date": "2024-06-15",
            "Supplier": "Britannia Cloud Ltd",
            "Customer": "Thames Analytics",
            "Item Description": "Managed PostgreSQL DB",
            "Quantity": 1,
            "Unit Price": 400.00,
            "Total": 400.00,
            "Subtotal": 900.00,
            "Tax": 180.00,
            "Total Amount": 1080.00,
            "Currency": "GBP",
        },
    ])
    df_csv.to_csv(f8, index=False)
    manifest.append({
        "id": "doc_08",
        "file": "files/08_services_invoice.csv",
        "category": "csv",
        "description": "Multi-row CSV invoice in GBP",
        "expected_math_valid": True,
        "ground_truth": {
            "invoice_number": "CSV-5501",
            "invoice_date": "2024-06-15",
            "supplier_name": "Britannia Cloud Ltd",
            "customer_name": "Thames Analytics",
            "subtotal": 900.00,
            "tax": 180.00,
            "total_amount": 1080.00,
            "currency": "GBP",
            "line_items": [
                {"description": "Dedicated Compute Node", "quantity": 2, "unit_price": 250.00, "total": 500.00},
                {"description": "Managed PostgreSQL DB", "quantity": 1, "unit_price": 400.00, "total": 400.00},
            ],
        },
    })

    # 9. Incomplete PDF (missing invoice_date, tax, currency -> Hallucination test)
    f9 = os.path.join(FILES_DIR, "09_incomplete_null_fields.pdf")
    _write_digital_pdf(f9, [[
        "STATEMENT OF CHARGES",
        "Invoice Number: INC-0099",
        "Supplier: Delta Field Services",
        "Customer: Pioneer Energy",
        "Field Inspection Fee   Qty: 1   Unit Price: 320.00   Total: 320.00",
        "Subtotal: 320.00",
        "Total Amount: 320.00",
    ]])
    manifest.append({
        "id": "doc_09",
        "file": "files/09_incomplete_null_fields.pdf",
        "category": "incomplete_pdf",
        "description": "Incomplete invoice missing invoice_date, tax, and currency (hallucination check)",
        "expected_math_valid": True,
        "ground_truth": {
            "invoice_number": "INC-0099",
            "invoice_date": None,
            "supplier_name": "Delta Field Services",
            "customer_name": "Pioneer Energy",
            "subtotal": 320.00,
            "tax": None,
            "total_amount": 320.00,
            "currency": None,
            "line_items": [
                {"description": "Field Inspection Fee", "quantity": 1, "unit_price": 320.00, "total": 320.00},
            ],
        },
    })

    # 10. Arithmetic Discrepancy PDF (400 + 40 != 480)
    f10 = os.path.join(FILES_DIR, "10_math_discrepancy.pdf")
    _write_digital_pdf(f10, [[
        "TAX INVOICE (DISCREPANCY)",
        "Invoice Number: INV-ERR-9920",
        "Invoice Date: 2024-06-01",
        "Supplier: Global Hardware Corp.",
        "Customer: Matrix Logistics",
        "Industrial Router   Qty: 1   Unit Price: 400.00   Total: 400.00",
        "Subtotal: 400.00 USD",
        "Tax (10%): 40.00 USD",
        "Total Amount: 480.00 USD",
    ]])
    manifest.append({
        "id": "doc_10",
        "file": "files/10_math_discrepancy.pdf",
        "category": "discrepancy_pdf",
        "description": "Invoice with deliberate arithmetic discrepancy (400 + 40 != 480)",
        "expected_math_valid": False,
        "ground_truth": {
            "invoice_number": "INV-ERR-9920",
            "invoice_date": "2024-06-01",
            "supplier_name": "Global Hardware Corp.",
            "customer_name": "Matrix Logistics",
            "subtotal": 400.00,
            "tax": 40.00,
            "total_amount": 480.00,
            "currency": "USD",
            "line_items": [
                {"description": "Industrial Router", "quantity": 1, "unit_price": 400.00, "total": 400.00},
            ],
        },
    })

    with open(MANIFEST_PATH, "w") as mf:
        json.dump(manifest, mf, indent=2)

    print(f"Generated {len(manifest)} labeled benchmark documents in {FILES_DIR}")
    print(f"Manifest saved to {MANIFEST_PATH}")
    return manifest


if __name__ == "__main__":
    build_dataset()
