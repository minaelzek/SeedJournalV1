# ADR-005: HNSW index outside Alembic CI path

**Status:** Accepted

## Context

Creating an HNSW index on `memory_embeddings` during `alembic upgrade` failed in GitHub Actions when the statement errored inside a single migration transaction (PostgreSQL aborts the whole transaction).

## Decision

- Alembic revision **002** is a **no-op** in `upgrade()`.
- Optional production index: `infra/sql/create_hnsw_index.sql` run manually when embeddings exist.
- Application falls back to Python cosine search when pgvector SQL path fails.

## Consequences

- CI migrate step is reliable.
- Operators must document HNSW apply on Neon for large-scale search performance.