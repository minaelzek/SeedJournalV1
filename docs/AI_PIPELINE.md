# SeedJournal — AI Pipeline Design

**Version:** 0.1 (Phase 2)

---

## Stages

| Stage | Trigger | Output |
|-------|---------|--------|
| Reflection analysis | Entry saved/completed | themes, depth_score, sensitivity_flags |
| Memory extraction | After analysis | 0–5 structured memories (JSON) |
| Embedding | New memory | vector(1536) in pgvector |
| Retrieval | Guide turn / search | top-k memories (min score) |
| AI guide | User continues | ≤2 questions; listen-first tone |
| Growth signals | Post extraction | growth_events (rules + analysis) |
| Tree projection | After growth | `tree_states` update |

---

## Analysis output (JSON)

```json
{
  "themes": ["string"],
  "depth_score": 0.0,
  "emotional_tone": "neutral",
  "sensitivity_flags": ["none"]
}
```

`crisis_language` flag → guide must not counsel; point to real-world help + app static resources.

---

## Memory extraction rules

- Max 5 per entry; skip trivia
- `confidence < 0.55` discard (tunable)
- Dedupe via embedding similarity > 0.92 vs recent memories

---

## Guide system prompt pillars

1. Gentle reflection guide — not therapist  
2. Listen; brief theme reflection  
3. At most two questions per message  
4. Invite user to save when enough explored  
5. Use only provided memories; admit uncertainty  
6. No diagnosis, medication, or commands  

**Turn cap:** 6 total per session (enforced server-side).

---

## Growth (internal, not XP UI)

| Signal | Source |
|--------|--------|
| depth | depth_score capped per entry |
| memory | new memory confidence (weekly cap) |
| flower | growth_event memory type |
| consistency | sqrt curve over 30d entries |
| absence | may shift season toward winter — no shame copy |

**Stages (growth_index internal):** sprout ≥0.08, sapling ≥0.22, sakura ≥0.45, blooming ≥0.70 + flower memory

---

## Env configuration

`LLM_PROVIDER`, `LLM_MODEL_FAST`, `LLM_MODEL_GUIDE`, `EMBEDDING_MODEL`, `LLM_TIMEOUT_SEC`

**Local:** `LLM_PROVIDER=stub` for dev without API keys.

---

## Failures

LLM timeout → “Your words are saved.” Invalid JSON → retry once. Embedding fail → retry queue. Rate limit → 429 + Retry-After.

Jobs idempotent on `(entry_id, job_type)`.