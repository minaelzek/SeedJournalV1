"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-03-30

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Enums: create once, reference with create_type=False (avoids DuplicateObject in CI)
MEMORY_TYPE = postgresql.ENUM(
    "value",
    "belief",
    "goal",
    "emotional_pattern",
    "important_moment",
    "realization",
    "growth_event",
    name="memory_type",
    create_type=False,
)
TREE_STAGE = postgresql.ENUM(
    "seed", "sprout", "sapling", "sakura", "blooming", name="tree_stage", create_type=False
)
SEASON = postgresql.ENUM(
    "spring", "summer", "autumn", "winter", name="season", create_type=False
)
REFLECTION_ROLE = postgresql.ENUM("user", "assistant", name="reflection_role", create_type=False)
JOB_STATUS = postgresql.ENUM(
    "pending", "running", "completed", "failed", name="job_status", create_type=False
)


def _create_enum_types() -> None:
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE memory_type AS ENUM (
                'value', 'belief', 'goal', 'emotional_pattern',
                'important_moment', 'realization', 'growth_event'
            );
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
        """
    )
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE tree_stage AS ENUM ('seed', 'sprout', 'sapling', 'sakura', 'blooming');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
        """
    )
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE season AS ENUM ('spring', 'summer', 'autumn', 'winter');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
        """
    )
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE reflection_role AS ENUM ('user', 'assistant');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
        """
    )
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE job_status AS ENUM ('pending', 'running', 'completed', 'failed');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
        """
    )


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')
    op.execute('CREATE EXTENSION IF NOT EXISTS "vector"')
    _create_enum_types()

    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("apple_sub", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=True),
        sa.Column("timezone", sa.String(length=64), server_default="UTC", nullable=False),
        sa.Column("ai_depth_enabled", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("apple_sub"),
    )

    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_refresh_tokens_user_id", "refresh_tokens", ["user_id"])

    op.create_table(
        "journal_entries",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("word_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("reflection_completed", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("depth_score", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_journal_entries_user_id", "journal_entries", ["user_id"])
    op.create_index("ix_journal_entries_user_created", "journal_entries", ["user_id", "created_at"])

    op.create_table(
        "reflection_sessions",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("entry_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("turn_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["entry_id"], ["journal_entries.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("entry_id"),
    )
    op.create_index("ix_reflection_sessions_user_id", "reflection_sessions", ["user_id"])

    op.create_table(
        "reflection_turns",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("session_id", sa.UUID(), nullable=False),
        sa.Column("role", REFLECTION_ROLE, nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["reflection_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_id", "sequence", name="uq_reflection_turn_sequence"),
    )
    op.create_index("ix_reflection_turns_session_id", "reflection_turns", ["session_id"])

    op.create_table(
        "memories",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("source_entry_id", sa.UUID(), nullable=False),
        sa.Column("type", MEMORY_TYPE, nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Float(), server_default="0", nullable=False),
        sa.Column("dismissed", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("first_mentioned_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["source_entry_id"], ["journal_entries.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_memories_user_id", "memories", ["user_id"])
    op.create_index("ix_memories_source_entry_id", "memories", ["source_entry_id"])

    op.create_table(
        "memory_embeddings",
        sa.Column("memory_id", sa.UUID(), nullable=False),
        sa.Column("embedding", Vector(1536), nullable=False),
        sa.Column("model", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["memory_id"], ["memories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("memory_id"),
    )

    op.create_table(
        "analysis_jobs",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("entry_id", sa.UUID(), nullable=False),
        sa.Column("job_type", sa.String(length=64), nullable=False),
        sa.Column("status", JOB_STATUS, nullable=False),
        sa.Column("payload", postgresql.JSONB(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["entry_id"], ["journal_entries.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analysis_jobs_user_id", "analysis_jobs", ["user_id"])
    op.create_index("ix_analysis_jobs_entry_id", "analysis_jobs", ["entry_id"])

    op.create_table(
        "tree_states",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("stage", TREE_STAGE, server_default="seed", nullable=False),
        sa.Column("season", SEASON, server_default="spring", nullable=False),
        sa.Column("growth_index", sa.Float(), server_default="0", nullable=False),
        sa.Column("roots_count", sa.Integer(), server_default="1", nullable=False),
        sa.Column("branches_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("leaves_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("flowers_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("last_recomputed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
    )

    op.create_table(
        "growth_events",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("memory_id", sa.UUID(), nullable=True),
        sa.Column("signal_type", sa.String(length=64), nullable=False),
        sa.Column("magnitude", sa.Float(), server_default="0", nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["memory_id"], ["memories.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_growth_events_user_id", "growth_events", ["user_id"])


def downgrade() -> None:
    op.drop_table("growth_events")
    op.drop_table("tree_states")
    op.drop_table("analysis_jobs")
    op.drop_table("memory_embeddings")
    op.drop_table("memories")
    op.drop_table("reflection_turns")
    op.drop_table("reflection_sessions")
    op.drop_table("journal_entries")
    op.drop_table("refresh_tokens")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS job_status")
    op.execute("DROP TYPE IF EXISTS reflection_role")
    op.execute("DROP TYPE IF EXISTS season")
    op.execute("DROP TYPE IF EXISTS tree_stage")
    op.execute("DROP TYPE IF EXISTS memory_type")