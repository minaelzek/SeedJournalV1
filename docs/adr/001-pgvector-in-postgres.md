# ADR-001: pgvector in PostgreSQL

**Status:** Accepted

## Context

Memories need semantic retrieval. Separate vector DB adds ops complexity for a small team.

## Decision

Use PostgreSQL 16 with pgvector extension in the same database as relational data.

## Consequences

- Single backup/replication story
- JOIN memories with entries in one query
- Must tune HNSW index and embedding dimension in migrations