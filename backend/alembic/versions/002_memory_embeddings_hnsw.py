"""Optional HNSW index (run manually on production if desired)

Revision ID: 002
Revises: 001
Create Date: 2026-03-30

CI runs this as a no-op. After deploy with real traffic, optional:

  psql $DATABASE_URL -f infra/sql/create_hnsw_index.sql

"""

from typing import Sequence, Union

from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Intentionally empty — HNSW on empty tables can fail on some pgvector builds
    # and a failed statement aborts Alembic's transaction (CI migrate step).
    pass


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_memory_embeddings_hnsw")