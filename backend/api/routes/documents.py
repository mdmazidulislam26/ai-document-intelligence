"""
Document upload, status querying, retrieval, cross-verification, outbox reconciliation,
and reprocessing endpoints with authentication, owner-scoped authorization, streaming upload limits,
and rate limiting.
"""

import os
import uuid
import logging
from typing import List, Optional, Dict
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from core.database import get_db
from core.config import settings
from core.security import AuthPrincipal, get_current_principal
from core.rate_limit import rate_limit_upload, rate_limit_write
from models.document import Document, CrossVerificationHistory, TaskOutbox
from models.schemas import (
    DocumentResponse,
    DocumentStatusResponse,
    CrossVerifyRequest,
    CrossVerificationResponse,
)
from services.file_security import FileSecurityValidator, ALLOWED_EXTENSIONS
from services.cross_verification_service import CrossVerificationService
from services.outbox_service import OutboxService

logger = logging.getLogger("documents_router")
router = APIRouter(prefix="/documents", tags=["Documents"])


def _assert_document_access(doc: Document, principal: AuthPrincipal) -> None:
    if not principal.is_admin and doc.owner_id != principal.owner_id:
        raise HTTPException(status_code=403, detail="Access denied to requested document.")


@router.post(
    "/upload",
    response_model=List[DocumentStatusResponse],
    status_code=202,
    dependencies=[Depends(rate_limit_upload)],
)
async def upload_documents(
    files: List[UploadFile] = File(...),
    principal: AuthPrincipal = Depends(get_current_principal),
    db: AsyncSession = Depends(get_db),
):
    """
    Accepts single or multi-file uploads with streaming size cap, magic-byte & zip-bomb validation,
    owner scoping, atomic outbox persistence, and post-commit Celery dispatch.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided.")

    if len(files) > settings.MAX_FILES_PER_UPLOAD:
        raise HTTPException(
            status_code=400,
            detail=f"Too many files in one upload. Maximum allowed: {settings.MAX_FILES_PER_UPLOAD}."
        )

    saved_files_on_disk = []
    created_docs = []
    outbox_entries = []
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

            # Stream file in 1MB chunks to abort oversized payloads before exhausting RAM
            chunks = []
            total_size = 0
            while chunk := await file.read(1024 * 1024):
                total_size += len(chunk)
                if total_size > max_bytes:
                    raise HTTPException(
                        status_code=413,
                        detail=f"File '{orig_filename}' exceeds limit of {settings.MAX_UPLOAD_SIZE_MB}MB."
                    )
                chunks.append(chunk)

            if total_size == 0:
                raise HTTPException(status_code=400, detail=f"File '{orig_filename}' is empty (0 bytes).")

            content = b"".join(chunks)

            is_valid, error_msg = FileSecurityValidator.validate_file_content(content, ext)
            if not is_valid:
                raise HTTPException(status_code=400, detail=f"Invalid file content for '{orig_filename}': {error_msg}")

            unique_name = f"{uuid.uuid4().hex}{ext}"
            file_path = os.path.abspath(os.path.join(settings.UPLOAD_DIR, unique_name))

            if not file_path.startswith(os.path.abspath(settings.UPLOAD_DIR)):
                raise HTTPException(status_code=400, detail="Invalid destination path traversal detected.")

            with open(file_path, "wb") as f:
                f.write(content)
            saved_files_on_disk.append(file_path)

            doc = Document(
                owner_id=principal.owner_id,
                filename=sanitized_name,
                file_path=file_path,
                file_type=ext,
                file_size_bytes=total_size,
                status="queued",
            )
            db.add(doc)
            await db.flush()

            outbox = TaskOutbox(document_id=doc.id, status="pending")
            db.add(outbox)
            created_docs.append(doc)
            outbox_entries.append(outbox)

        await db.commit()

        for doc in created_docs:
            await db.refresh(doc)
            responses.append(
                DocumentStatusResponse(
                    id=doc.id,
                    filename=doc.filename,
                    status=doc.status,
                    error_message=None,
                )
            )
        for ob in outbox_entries:
            await db.refresh(ob)

    except HTTPException:
        await db.rollback()
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
        logger.exception(f"Upload failed: {type(e).__name__}")
        raise HTTPException(status_code=500, detail="Internal server error during document upload.")

    await OutboxService.dispatch_outbox_entries_async(db, [ob.id for ob in outbox_entries])
    return responses


@router.post("/reconcile", response_model=Dict[str, int], dependencies=[Depends(rate_limit_write)])
async def reconcile_outbox_and_stuck_documents(
    principal: AuthPrincipal = Depends(get_current_principal),
    db: AsyncSession = Depends(get_db),
):
    """Reconciles pending TaskOutbox items and rescues stuck 'queued' or stale 'processing' documents."""
    return await OutboxService.reconcile_pending_and_stuck_async(db)


@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    principal: AuthPrincipal = Depends(get_current_principal),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves paginated list of documents scoped to authenticated principal's owner_id."""
    query = (
        select(Document)
        .options(
            selectinload(Document.extracted_invoice),
            selectinload(Document.validation_logs),
        )
        .order_by(desc(Document.created_at))
        .offset(skip)
        .limit(limit)
    )

    if not principal.is_admin:
        query = query.where(Document.owner_id == principal.owner_id)
    if status:
        query = query.where(Document.status == status)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    principal: AuthPrincipal = Depends(get_current_principal),
    db: AsyncSession = Depends(get_db),
):
    """Fetches full metadata, extracted invoice fields, and validation logs if authorized."""
    query = (
        select(Document)
        .options(
            selectinload(Document.extracted_invoice),
            selectinload(Document.validation_logs),
        )
        .where(Document.id == document_id)
    )
    result = await db.execute(query)
    doc = result.scalars().first()

    if not doc:
        raise HTTPException(status_code=404, detail=f"Document #{document_id} not found.")
    _assert_document_access(doc, principal)
    return doc


@router.get("/{document_id}/status", response_model=DocumentStatusResponse)
async def get_document_status(
    document_id: int,
    principal: AuthPrincipal = Depends(get_current_principal),
    db: AsyncSession = Depends(get_db),
):
    """Lightweight endpoint for polling document processing status."""
    query = select(
        Document.id, Document.owner_id, Document.filename, Document.status, Document.error_message
    ).where(Document.id == document_id)
    result = await db.execute(query)
    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail=f"Document #{document_id} not found.")
    if not principal.is_admin and row.owner_id != principal.owner_id:
        raise HTTPException(status_code=403, detail="Access denied to requested document.")

    return DocumentStatusResponse(
        id=row.id,
        filename=row.filename,
        status=row.status,
        error_message=row.error_message,
    )


@router.post("/{document_id}/reprocess", response_model=DocumentStatusResponse, dependencies=[Depends(rate_limit_write)])
async def reprocess_document(
    document_id: int,
    principal: AuthPrincipal = Depends(get_current_principal),
    db: AsyncSession = Depends(get_db),
):
    """Requeues an owned document safely via transactional outbox."""
    query = select(Document).where(Document.id == document_id)
    result = await db.execute(query)
    doc = result.scalars().first()

    if not doc:
        raise HTTPException(status_code=404, detail=f"Document #{document_id} not found.")
    _assert_document_access(doc, principal)

    doc.status = "queued"
    doc.error_message = None

    outbox = TaskOutbox(document_id=doc.id, status="pending")
    db.add(outbox)
    await db.commit()
    await db.refresh(outbox)

    await OutboxService.dispatch_outbox_entries_async(db, [outbox.id])

    return DocumentStatusResponse(
        id=doc.id,
        filename=doc.filename,
        status=doc.status,
        error_message=None,
    )


@router.post("/{document_id}/cross-verify", response_model=CrossVerificationResponse, dependencies=[Depends(rate_limit_write)])
async def cross_verify_document(
    document_id: int,
    payload: CrossVerifyRequest,
    principal: AuthPrincipal = Depends(get_current_principal),
    db: AsyncSession = Depends(get_db),
):
    """Cross-verifies an owned processed document against an owned reference document."""
    owner_scope = None if principal.is_admin else principal.owner_id
    return await CrossVerificationService.execute_cross_verification(
        db=db,
        document_id=document_id,
        reference_document_id=payload.reference_document_id,
        owner_id=owner_scope,
    )


@router.get("/{document_id}/cross-verify/history", response_model=List[CrossVerificationResponse])
async def get_cross_verification_history(
    document_id: int,
    principal: AuthPrincipal = Depends(get_current_principal),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves persistent cross-verification history for an authorized document."""
    doc = (await db.execute(select(Document).where(Document.id == document_id))).scalars().first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document #{document_id} not found.")
    _assert_document_access(doc, principal)

    stmt = (
        select(CrossVerificationHistory)
        .where(CrossVerificationHistory.document_id == document_id)
        .order_by(desc(CrossVerificationHistory.created_at), desc(CrossVerificationHistory.id))
    )
    rows = (await db.execute(stmt)).scalars().all()
    return [
        CrossVerificationResponse(
            id=r.id,
            document_id=r.document_id,
            reference_document_id=r.reference_document_id,
            verification_mode=r.verification_mode,
            overall_status=r.overall_status,
            discrepancy_count=r.discrepancy_count,
            comparison_details=r.comparison_details,
            validation_logs=[],
            created_at=r.created_at,
        )
        for r in rows
    ]
