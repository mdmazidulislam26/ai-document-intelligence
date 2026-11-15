"""
Document upload, status querying, retrieval, and reprocessing endpoints.
"""

import os
import shutil
import uuid
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from core.database import get_db
from core.config import settings
from models.document import Document, ExtractedInvoice, ValidationLog
from models.schemas import DocumentResponse, DocumentStatusResponse
from tasks.processing_tasks import process_document_task

router = APIRouter(prefix="/documents", tags=["Documents"])

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".tif", ".xlsx", ".xls", ".csv"}


@router.post("/upload", response_model=List[DocumentStatusResponse], status_code=202)
async def upload_documents(
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Accepts single or multi-file uploads (PDF, JPG, PNG, TIFF, XLSX, XLS, CSV).
    Saves files securely and dispatches Celery background tasks for processing.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided.")

    responses = []

    for file in files:
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format: {file.filename}. Allowed: {list(ALLOWED_EXTENSIONS)}"
            )

        # Generate unique storage filename to avoid collisions
        unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

        # Write file content to disk safely in chunks
        content_length = 0
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):  # 1MB chunks
                content_length += len(chunk)
                if content_length > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
                    os.remove(file_path)
                    raise HTTPException(
                        status_code=413,
                        detail=f"File {file.filename} exceeds maximum size limit of {settings.MAX_UPLOAD_SIZE_MB}MB."
                    )
                buffer.write(chunk)

        # Create Document record in database
        doc = Document(
            filename=file.filename,
            file_path=file_path,
            file_type=file_ext,
            file_size_bytes=content_length,
            status="queued"
        )
        db.add(doc)
        await db.flush()  # Flush to obtain generated doc.id

        # Dispatch async task to Celery worker
        process_document_task.delay(doc.id)

        responses.append(
            DocumentStatusResponse(
                id=doc.id,
                filename=doc.filename,
                status=doc.status,
                error_message=None
            )
        )

    await db.commit()
    return responses


@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves paginated list of documents with their extraction results and validation status.
    """
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
    """
    Fetches full metadata, extracted invoice fields, and validation logs for a given document.
    """
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
    """
    Lightweight endpoint for polling document processing status.
    """
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
    """
    Requeues a failed or unvalidated document for background reprocessing.
    """
    query = select(Document).where(Document.id == document_id)
    result = await db.execute(query)
    doc = result.scalars().first()

    if not doc:
        raise HTTPException(status_code=404, detail=f"Document #{document_id} not found.")

    doc.status = "queued"
    doc.error_message = None
    await db.commit()

    # Trigger Celery pipeline
    process_document_task.delay(doc.id)

    return DocumentStatusResponse(
        id=doc.id,
        filename=doc.filename,
        status=doc.status,
        error_message=None
    )
