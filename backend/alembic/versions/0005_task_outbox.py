"""Add task_outbox table for transactional Celery dispatch and broker outage recovery.

Revision ID: 0005_task_outbox
Revises: 0004_cross_verify_history
Create Date: 2026-11-17 00:25:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic (must be <= 32 chars).
revision: str = "0005_task_outbox"
down_revision: Union[str, None] = "0004_cross_verify_history"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _get_existing_indexes(inspector: sa.Inspector, table_name: str, schema: str) -> set[str]:
    return {idx["name"] for idx in inspector.get_indexes(table_name, schema=schema)}


def upgrade() -> None:
    bind = op.get_bind()
    current_schema = bind.execute(sa.text("SELECT current_schema()")).scalar()
    inspector = sa.inspect(bind)

    if not inspector.has_table("task_outbox", schema=current_schema):
        op.create_table(
            "task_outbox",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("document_id", sa.Integer(), nullable=False),
            sa.Column("task_name", sa.String(length=128), nullable=False),
            sa.Column("status", sa.String(length=32), nullable=False),
            sa.Column("attempts", sa.Integer(), nullable=False),
            sa.Column("last_error", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("dispatched_at", sa.DateTime(), nullable=True),
            sa.Column("next_attempt_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
        )

    existing_indexes = _get_existing_indexes(inspector, "task_outbox", current_schema)
    if "ix_task_outbox_id" not in existing_indexes:
        op.create_index("ix_task_outbox_id", "task_outbox", ["id"], unique=False)
    if "ix_task_outbox_document_id" not in existing_indexes:
        op.create_index("ix_task_outbox_document_id", "task_outbox", ["document_id"], unique=False)
    if "ix_task_outbox_status" not in existing_indexes:
        op.create_index("ix_task_outbox_status", "task_outbox", ["status"], unique=False)
    if "idx_task_outbox_pending_next" not in existing_indexes:
        op.create_index("idx_task_outbox_pending_next", "task_outbox", ["status", "next_attempt_at"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    current_schema = bind.execute(sa.text("SELECT current_schema()")).scalar()
    inspector = sa.inspect(bind)

    if inspector.has_table("task_outbox", schema=current_schema):
        existing_indexes = _get_existing_indexes(inspector, "task_outbox", current_schema)
        for idx_name in [
            "idx_task_outbox_pending_next",
            "ix_task_outbox_status",
            "ix_task_outbox_document_id",
            "ix_task_outbox_id",
        ]:
            if idx_name in existing_indexes:
                op.drop_index(idx_name, table_name="task_outbox")
        op.drop_table("task_outbox")
