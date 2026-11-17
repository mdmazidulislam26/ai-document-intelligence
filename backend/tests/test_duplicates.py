"""
Automated tests for duplicate invoice validation across synchronous and asynchronous sessions.
"""

from decimal import Decimal
from datetime import date
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from models.document import Base, Document, ExtractedInvoice
from services.validator import DocumentValidator


@pytest.fixture(scope="module")
def sync_db_session():
    """Creates a temporary sync database session for testing duplicate detection."""
    engine = create_engine(settings.SYNC_DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.query(ExtractedInvoice).delete()
    session.query(Document).delete()
    session.commit()
    session.close()


def test_duplicate_same_supplier_and_invoice_detected(sync_db_session):
    """Detects duplicate when both supplier and invoice number match another document."""
    # Seed doc 1
    doc1 = Document(filename="invoice_1.pdf", file_path="/tmp/test_dup1.pdf", file_type=".pdf", status="validated")
    sync_db_session.add(doc1)
    sync_db_session.flush()

    inv1 = ExtractedInvoice(
        document_id=doc1.id,
        invoice_number="INV-DUP-100",
        supplier_name="Alpha Tech Ltd",
        total_amount=Decimal("500.00"),
        invoice_date=date(2024, 5, 1)
    )
    sync_db_session.add(inv1)
    sync_db_session.commit()

    # Check incoming duplicate
    errors = DocumentValidator.check_duplicate_invoice_sync(
        session=sync_db_session,
        invoice_number="inv-dup-100",
        supplier_name="  alpha tech ltd  ",
        current_doc_id=99999  # New incoming document
    )

    assert len(errors) == 1
    assert errors[0].rule_name == "DUPLICATE_INVOICE_DETECTED"
    assert errors[0].severity == "CRITICAL"


def test_different_supplier_same_invoice_not_duplicate(sync_db_session):
    """Does NOT flag duplicate if same invoice number belongs to a different supplier."""
    errors = DocumentValidator.check_duplicate_invoice_sync(
        session=sync_db_session,
        invoice_number="INV-DUP-100",
        supplier_name="Beta Logistics Corp",
        current_doc_id=99999
    )

    assert len(errors) == 0


def test_same_supplier_different_invoice_not_duplicate(sync_db_session):
    """Does NOT flag duplicate if same supplier has a new unique invoice number."""
    errors = DocumentValidator.check_duplicate_invoice_sync(
        session=sync_db_session,
        invoice_number="INV-NEW-999",
        supplier_name="Alpha Tech Ltd",
        current_doc_id=99999
    )

    assert len(errors) == 0


def test_current_document_excluded_from_self_duplicate(sync_db_session):
    """Document being re-evaluated should exclude itself from duplicate detection."""
    # Find doc 1 id
    doc = sync_db_session.query(ExtractedInvoice).filter(ExtractedInvoice.invoice_number == "INV-DUP-100").first()
    assert doc is not None

    errors = DocumentValidator.check_duplicate_invoice_sync(
        session=sync_db_session,
        invoice_number="INV-DUP-100",
        supplier_name="Alpha Tech Ltd",
        current_doc_id=doc.document_id  # Checking self
    )

    assert len(errors) == 0
