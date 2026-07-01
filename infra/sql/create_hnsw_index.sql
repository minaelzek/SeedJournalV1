-- Run on production/staging Neon after memories exist (optional, speeds vector search)
CREATE INDEX IF NOT EXISTS ix_memory_embeddings_hnsw
ON memory_embeddings
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);