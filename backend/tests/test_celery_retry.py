"""
Automated unit tests for Celery task dispatch, idempotency, and retry behavior.
"""

from unittest.mock import patch, MagicMock
from decimal import Decimal
import pytest
import httpx
from celery.exceptions import Retry
from tasks.processing_tasks import process_document_task
from models.document import Document


def test_process_document_task_nonexistent_doc():
    """Returns False safely if document does not exist without crashing."""
    res = process_document_task(999999)
    assert res is False


@patch("tasks.processing_tasks.DocumentParserService.extract_full_text")
def test_permanent_parser_error_marks_document_failed(mock_parser):
    """Corrupted file extraction should permanently set doc status = failed without retrying."""
    mock_parser.side_effect = ValueError("Corrupted PDF streams")

    mock_doc = MagicMock(spec=Document)
    mock_doc.id = 101
    mock_doc.file_path = "/tmp/test_corrupt.pdf"
    mock_doc.status = "queued"

    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = mock_doc

    with patch("tasks.processing_tasks.SessionLocalSync", return_value=mock_session):
        res = process_document_task(101)
        assert res is False
        assert mock_doc.status == "failed"
        assert "Corrupted PDF streams" in mock_doc.error_message


def test_transient_http_error_invokes_retry():
    """Simulates transient external API error invoking Celery self.retry with backoff."""
    mock_doc = MagicMock(spec=Document)
    mock_doc.id = 202
    mock_doc.file_path = "/tmp/test.pdf"
    mock_doc.status = "queued"

    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = mock_doc

    with patch("tasks.processing_tasks.SessionLocalSync", return_value=mock_session), \
         patch("tasks.processing_tasks.DocumentParserService.extract_full_text", return_value=("Sample text", 1)), \
         patch("tasks.processing_tasks.AIExtractorService.extract_invoice_data", side_effect=httpx.RequestError("Network timeout")), \
         patch.object(process_document_task, "retry", side_effect=Retry()) as mock_retry:

        with pytest.raises(Retry):
            process_document_task(202)

        assert mock_retry.called
