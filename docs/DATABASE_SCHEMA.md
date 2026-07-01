# SeedJournal — Database Schema

**Engine:** PostgreSQL 16 + `vector` extension

---

## Extensions

```sql
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";
```

---

## Enums

- `memory_type`: value, belief, goal, emotional_pattern, important_moment, realization, growth_event
- `tree_stage`: seed, sprout, sapling, sakura, blooming
- `season`: spring, summer, autumn, winter
- `reflection_role`: user, assistant
- `job_status`: pending, running, completed, failed

---

## Tables

### users

`id` UUID PK, `apple_sub` TEXT UNIQUE, `email` TEXT NULL, `timezone` TEXT, `ai_depth_enabled` BOOLEAN, timestamps, `deleted_at` NULL

### refresh_tokens

`id`, `user_id` FK, `token_hash`, `expires_at`, `revoked_at`, `created_at`

### journal_entries

`id`, `user_id`, `title` NULL, `body`, `word_count`, `reflection_completed`, `depth_score` NULL, timestamps  
Index: `(user_id, created_at DESC)`

### reflection_sessions

`id`, `entry_id` UNIQUE FK, `user_id`, `turn_count`, `completed_at`, `created_at`

### reflection_turns

`id`, `session_id`, `role`, `content`, `sequence`, `created_at`  
Unique: `(session_id, sequence)`

### memories

`id`, `user_id`, `source_entry_id`, `type`, `title`, `summary`, `confidence`, `dismissed`, `first_mentioned_at`, `created_at`

### memory_embeddings

`memory_id` PK FK, `embedding` vector(1536), `model`, `created_at`  
Index: HNSW cosine

### analysis_jobs

`id`, `user_id`, `entry_id`, `job_type`, `status`, `payload` JSONB, `error`, timestamps

### tree_states

`user_id` PK FK, `stage`, `season`, `growth_index` REAL (internal), component counts, `last_recomputed_at`, `metadata` JSONB

### growth_events

`id`, `user_id`, `memory_id` NULL, `signal_type`, `magnitude`, `occurred_at`

---

## Semantic search (reference)

```sql
SELECT m.id, m.title, m.summary, m.first_mentioned_at,
       1 - (e.embedding <=> :query_embedding) AS score
FROM memories m
JOIN memory_embeddings e ON e.memory_id = m.id
WHERE m.user_id = :user_id AND m.dismissed = false
  AND (1 - (e.embedding <=> :query_embedding)) >= :min_score
ORDER BY e.embedding <=> :query_embedding
LIMIT :limit;
```

---

## Deletion

Account delete cascades entries, sessions, turns, memories, embeddings, tree, jobs, tokens.

Alembic revision chain starts in Slice 0.