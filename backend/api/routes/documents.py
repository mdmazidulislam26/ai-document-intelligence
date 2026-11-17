"""
Document upload, status querying, retrieval, and reprocessing endpoints.
Updated with strict pre-upload signature validation, path-traversal defense,
and post-commit transactional Celery dispatch.
"""

import os
import uuid
import logging
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from core.database import get_db
from core.config import settings
from models.document import Document
from models.schemas import DocumentResponse, DocumentStatusResponse
from services.file_security import FileSecurityValidator, ALLOWED_EXTENSIONS
from tasks.processing_tasks import process_document_task

logger = logging.getLogger("documents_router")
router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=List[DocumentStatusResponse], status_code=202)
async def upload_documents(
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Accepts single or multi-file uploads.
    Validates magic bytes, sanitizes filenames, safely writes to disk,
    commits database records, and dispatches Celery tasks strictly AFTER commit.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided.")

    saved_files_on_disk = []
    created_docs = []
    responses = []

    try:
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

        for file in files:
            orig_filename = file.filename or "uploaded_file"
            sanitized_name = FileSecurityValidator.sanitize_filename(orig_filename)
            _, ext = os.path.splitext(sanitized_name)
            ext = ext.lower()

            if ext not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported format '{ext}' for file '{orig_filename}'. Allowed: {sorted(list(ALLOWED_EXTENSIONS))}"
                )

            # Read content with size check in memory
            content = await file.read()
            if len(content) == 0:
                raise HTTPException(status_code=400, detail=f"File '{orig_filename}' is empty (0 bytes).")

            if len(content) > max_bytes:
                raise HTTPException(
                    status_code=413,
                    detail=f"File '{orig_filename}' exceeds limit of {settings.MAX_UPLOAD_SIZE_MB}MB."
                )

            # Deep Magic-Byte / Signature Validation
            is_valid, error_msg = FileSecurityValidator.validate_file_content(content, ext)
            if not is_valid:
                raise HTTPException(status_code=400, detail=f"Invalid file content for '{orig_filename}': {error_msg}")

            # Generate random server storage name to prevent collisions and path traversal
            unique_name = f"{uuid.uuid4().hex}{ext}"
            file_path = os.path.abspath(os.path.join(settings.UPLOAD_DIR, unique_name))

            # Ensure resolved path is strictly within UPLOAD_DIR
            if not file_path.startswith(os.path.abspath(settings.UPLOAD_DIR)):
                raise HTTPException(status_code=400, detail="Invalid destination path traversal detected.")

            # Save file to disk
            with open(file_path, "wb") as f:
                f.write(content)
            saved_files_on_disk.append(file_path)

            doc = Document(
                filename=sanitized_name,
                file_path=file_path,
                file_type=ext,
                file_size_bytes=len(content),
                status="queued"
            )
            db.add(doc)
            created_docs.append(doc)

        # Commit all records to the database FIRST
        await db.commit()

        # Refresh docs to obtain committed IDs
        for doc in created_docs:
            await db.refresh(doc)
            responses.append(
                DocumentStatusResponse(
                    id=doc.id,
                    filename=doc.filename,
                    status=doc.status,
                    error_message=None
                )
            )

    except HTTPException:
        await db.rollback()
        # Clean up files created in this failed request
        for p in saved_files_on_disk:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except OSError:
                    pass
        raise

    except Exception as e:
        await db.rollback()
        for p in saved_files_on_disk:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except OSError:
                    pass
        logger.exception(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during document upload.")

    # POST-COMMIT CELERY DISPATCH
    # Database commit succeeded; dispatch Celery processing tasks
    for doc in created_docs:
        try:
            process_document_task.delay(doc.id)
        except Exception as broker_err:
            logger.error(f"Failed to dispatch Celery task for doc #{doc.id}: {broker_err}")
            # Document record remains safely in DB as 'queued' so it can be reprocessed

    return responses


@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Retrieves paginated list of documents with extraction results and validation status."""
    query = (
        select(Document)
        .options(
            selectinload(Document.extracted_invoice),
            selectinload(Document.validation_logs)
        )
        .order_by(desc(Document.created_at))
        .offset(skip)
        .limit(limit)
    )

    if status:
        query = query.where(Document.status == status)

    result = await db.execute(query)
    documents = result.scalars().all()
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Fetches full metadata, extracted invoice fields, and validation logs for a given document."""
    query = (
        select(Document)
        .options(
            selectinload(Document.extracted_invoice),
            selectinload(Document.validation_logs)
        )
        .where(Document.id == document_id)
    )
    result = await db.execute(query)
    doc = result.scalars().first()

    if not doc:
        raise HTTPException(status_code=404, detail=f"Document #{document_id} not found.")

    return doc


@router.get("/{document_id}/status", response_model=DocumentStatusResponse)
async def get_document_status(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Lightweight endpoint for polling document processing status."""
    query = select(Document.id, Document.filename, Document.status, Document.error_message).where(
        Document.id == document_id
    )
    result = await db.execute(query)
    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail=f"Document #{document_id} not found.")

    return DocumentStatusResponse(
        id=row.id,
        filename=row.filename,
        status=row.status,
        error_message=row.error_message
    )


@router.post("/{document_id}/reprocess", response_model=DocumentStatusResponse)
async def reprocess_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Requeues a failed or unvalidated document for background reprocessing."""
    query = select(Document).where(Document.id == document_id)
    result = await db.execute(query)
    doc = result.scalars().first()

    if not doc:
        raise HTTPException(status_code=404, detail=f"Document #{document_id} not found.")

    doc.status = "queued"
    doc.error_message = None
    await db.commit()

    # Trigger Celery pipeline post-commit
    process_document_task.delay(doc.id)

    return DocumentStatusResponse(
        id=doc.id,
        filename=doc.filename,
        status=doc.status,
        error_message=None
    )
