# SeedJournal — Technical Architecture

**Version:** 0.2 (MVP shipped) · See [API.md](API.md) and [REPOSITORY.md](REPOSITORY.md)

---

## System context

- **iOS** (SwiftUI) → HTTPS + JWT → **FastAPI** `/v1`
- FastAPI → **PostgreSQL + pgvector**
- FastAPI → **LLM provider** (pluggable)

---

## Monorepo

```
ios/SeedJournal/     # Xcode
backend/app/         # FastAPI
backend/alembic/     # migrations
infra/               # docker-compose
docs/
```

---

## Backend modules

| Module | Responsibility |
|--------|----------------|
| `core` | Settings, security, logging, deps |
| `identity` | Apple auth, JWT, users |
| `journal` | Entries, reflection sessions/turns |
| `intelligence` | Analysis jobs |
| `memories` | CRUD + vector search |
| `growth` | Tree state, seasons, signals |
| `ai_guide` | Prompts, LLM client |
| `workers` | Async pipeline |

**Rule:** `routers` → `services` → `repositories` only.

---

## API (v1 core)

| Method | Path |
|--------|------|
| POST | `/auth/apple` |
| GET | `/me` |
| POST / GET | `/entries` |
| GET | `/entries/{id}` |
| POST | `/entries/{id}/reflection/start` |
| POST | `/entries/{id}/reflection/message` |
| POST | `/entries/{id}/reflection/complete` |
| PATCH | `/me` |
| GET | `/me/export` |
| GET | `/insights/patterns` |
| GET | `/insights/first-mention` |
| GET | `/memories` |
| POST | `/memories/search` |
| PATCH | `/memories/{id}` |
| GET | `/tree` |
| DELETE | `/me` |

Errors: problem+json. OpenAPI at `/openapi.json`.

---

## iOS layering

```
Features/ Tree, Journal, Reflection, History, Settings
Core/ Design, Network, Domain, Persistence (Keychain)
```

Swift async/await, `@MainActor` view models. Sheets for journal/settings — no tab bar.

---

## AI orchestration

```
Entry complete → Analysis → Memory extraction → Embeddings
              → Growth signals → Tree projection
```

Interactive guide: sync LLM with timeout; turn cap enforced server-side.

```python
class LLMClient(Protocol):
    async def complete(self, messages, *, model: str, json_mode: bool) -> str: ...
```

---

## Security

TLS, secrets via env, no journal bodies in logs, parameterized SQL, per-user rate limits on auth/AI, cascade delete on account removal.

---

## ADRs

| ID | Decision |
|----|----------|
| ADR-001 | pgvector in Postgres (not separate vector DB) |
| ADR-002 | Tree-centric navigation |
| ADR-003 | Sign in with Apple only for v1 |