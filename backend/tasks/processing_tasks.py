"""
Celery background worker pipeline tasks.
Executes OCR parsing, AI extraction, validation, and vector storage asynchronously.
"""

import asyncio
import logging
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from core.celery_app import celery_app
from core.config import settings
from models.document import Document, ExtractedInvoice, ValidationLog
from services.document_parser import DocumentParserService
from services.ai_extractor import AIExtractorService
from services.validator import DocumentValidator
from services.vector_service import VectorService

logger = logging.getLogger("processing_tasks")
logger.setLevel(logging.INFO)

# Synchronous engine for Celery tasks
sync_engine = create_engine(settings.SYNC_DATABASE_URL, pool_pre_ping=True)
SessionLocalSync = sessionmaker(bind=sync_engine, expire_on_commit=False)


@celery_app.task(name="tasks.processing_tasks.process_document_task", bind=True, max_retries=2)
def process_document_task(self, document_id: int):
    """
    Main background pipeline for document processing.
    """
    logger.info(f"Starting processing for document_id: {document_id}")
    session = SessionLocalSync()

    try:
        doc = session.query(Document).filter(Document.id == document_id).first()
        if not doc:
            logger.error(f"Document with ID {document_id} not found.")
            return False

        # Step 1: Update status to processing
        doc.status = "processing"
        session.commit()

        # Step 2: Extract text via DocumentParserService
        logger.info(f"Extracting text from: {doc.file_path}")
        raw_text, page_count = DocumentParserService.extract_full_text(doc.file_path)
        
        if not raw_text.strip():
            doc.status = "failed"
            doc.error_message = "No readable text could be extracted from document."
            session.commit()
            return False

        # Step 3: Run AI Information Extraction
        logger.info("Running AI structured extraction...")
        ai_service = AIExtractorService()
        extracted_data = ai_service.extract_invoice_data(raw_text)

        # Step 4: Validate Data
        logger.info("Executing validation rules...")
        val_errors = []

        # Mathematical checks
        math_results = DocumentValidator.validate_math(extracted_data)
        for res in math_results:
            if not res.passed:
                val_errors.append(res)

        # Required fields checks
        req_results = DocumentValidator.validate_required_fields(extracted_data)
        for res in req_results:
            if not res.passed:
                val_errors.append(res)

        # Duplicate invoice checks
        if extracted_data.invoice_number and extracted_data.supplier_name:
            dup_stmt = select(ExtractedInvoice).where(
                ExtractedInvoice.invoice_number == extracted_data.invoice_number,
                ExtractedInvoice.supplier_name == extracted_data.supplier_name,
                ExtractedInvoice.document_id != document_id
            )
            existing_dup = session.execute(dup_stmt).scalars().first()
            if existing_dup:
                from services.validator import ValidationRuleResult
                val_errors.append(
                    ValidationRuleResult(
                        rule_name="DUPLICATE_INVOICE_DETECTED",
                        passed=False,
                        error_description=(
                            f"Invoice '{extracted_data.invoice_number}' for supplier '{extracted_data.supplier_name}' "
                            f"already exists in document #{existing_dup.document_id}."
                        ),
                        severity="CRITICAL"
                    )
                )

        # Step 5: Generate Vector Embedding for Semantic Search
        logger.info("Generating FastEmbed semantic vector embedding...")
        summary_for_embedding = (
            f"Supplier: {extracted_data.supplier_name or 'N/A'}. "
            f"Invoice: {extracted_data.invoice_number or 'N/A'}. "
            f"Total: {extracted_data.total_amount or 0.0} {extracted_data.currency or 'USD'}. "
            f"Customer: {extracted_data.customer_name or 'N/A'}. "
            f"Content: {raw_text[:1000]}"
        )
        embedding_vector = VectorService.generate_embedding(summary_for_embedding)

        # Step 6: Parse invoice_date if string
        parsed_date = None
        if extracted_data.invoice_date:
            try:
                parsed_date = datetime.strptime(extracted_data.invoice_date, "%Y-%m-%d").date()
            except ValueError:
                parsed_date = None

        # Convert line items to raw list of dicts
        line_items_dict = [item.model_dump() for item in extracted_data.line_items]

        # Step 7: Persist Extracted Record
        extracted_record = session.query(ExtractedInvoice).filter(ExtractedInvoice.document_id == document_id).first()
        if not extracted_record:
            extracted_record = ExtractedInvoice(
                document_id=document_id,
                invoice_number=extracted_data.invoice_number,
                invoice_date=parsed_date,
                supplier_name=extracted_data.supplier_name,
                customer_name=extracted_data.customer_name,
                subtotal=extracted_data.subtotal,
                tax=extracted_data.tax,
                total_amount=extracted_data.total_amount,
                currency=extracted_data.currency,
                line_items=line_items_dict,
                raw_text=raw_text,
                embedding=embedding_vector
            )
            session.add(extracted_record)
        else:
            extracted_record.invoice_number = extracted_data.invoice_number
            extracted_record.invoice_date = parsed_date
            extracted_record.supplier_name = extracted_data.supplier_name
            extracted_record.customer_name = extracted_data.customer_name
            extracted_record.subtotal = extracted_data.subtotal
            extracted_record.tax = extracted_data.tax
            extracted_record.total_amount = extracted_data.total_amount
            extracted_record.currency = extracted_data.currency
            extracted_record.line_items = line_items_dict
            extracted_record.raw_text = raw_text
            extracted_record.embedding = embedding_vector

        # Step 8: Persist Validation Logs
        # Clear old logs if reprocessing
        session.query(ValidationLog).filter(ValidationLog.document_id == document_id).delete()
        for err in val_errors:
            log_entry = ValidationLog(
                document_id=document_id,
                rule_name=err.rule_name,
                error_description=err.error_description,
                severity=err.severity
            )
            session.add(log_entry)

        # Step 9: Final Status Assignment
        if val_errors:
            doc.status = "requires_manual_review"
        else:
            doc.status = "validated"

        session.commit()
        logger.info(f"Successfully processed document_id {document_id}. Final status: {doc.status}")
        return True

    except Exception as e:
        session.rollback()
        logger.exception(f"Unhandled error in process_document_task for doc #{document_id}: {str(e)}")
        doc = session.query(Document).filter(Document.id == document_id).first()
        if doc:
            doc.status = "failed"
            doc.error_message = str(e)
            session.commit()
        raise e
    finally:
        session.close()
