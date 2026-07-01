# Phase 1: Repository Analysis

**Date:** 2026-03-30  
**Status:** Greenfield — no prior codebase

---

## 1. Inspection Summary

| Area | Finding |
|------|---------|
| **Repository** | Empty workspace; no `git` init, no `package.json`, no Xcode project |
| **iOS** | None — build from Swift + SwiftUI |
| **Backend** | None — build from Python FastAPI |
| **Database** | None — PostgreSQL + pgvector to be provisioned |
| **CI/CD** | None |
| **Design system** | None — define Zen / editorial luxury tokens |
| **Secrets / env** | None — require `.env.example`, Keychain, server-side API keys |
| **Tests** | None — plan XCTest + pytest from day one |

**Conclusion:** SeedJournal is a **net-new premium product**. No migration or legacy constraints. All conventions must be established deliberately.

---

## 2. Target Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     iOS App (SwiftUI)                            │
│  Tree (home) · Journal · Reflection thread · History · Settings │
│  Local: Keychain, optional on-device cache, minimal PII offline │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS (JWT / session)
┌────────────────────────────▼────────────────────────────────────┐
│              API Gateway — FastAPI                               │
│  Auth · Journal · Memories · Tree state · AI orchestration     │
└────────────┬───────────────────────────────┬────────────────────┘
             │                               │
    ┌────────▼────────┐              ┌───────▼────────┐
    │  PostgreSQL     │              │  LLM Provider  │
    │  + pgvector     │              │  (pluggable)   │
    │  users, entries │              └────────────────┘
    │  memories, tree │
    └─────────────────┘
```

### Modular boundaries

| Module | Responsibility |
|--------|----------------|
| **identity** | Sign in with Apple (primary), account, encryption keys metadata |
| **journal** | Raw entries, sessions, reflection turns |
| **intelligence** | Analysis jobs, memory extraction, embeddings, retrieval |
| **growth** | Tree state machine, seasons, non-punitive decay |
| **ai_guide** | Prompt contracts, tone guardrails, user-controlled depth |
| **sync** | Idempotent writes, conflict policy (server wins for AI artifacts) |

### iOS layering (recommended)

- **Presentation:** SwiftUI views, animations, accessibility
- **Domain:** Use cases (StartReflection, SaveEntry, FetchTreeState)
- **Data:** API client, DTO mapping, Keychain
- **Design:** Tokens (color, type, spacing), components (TreeCanvas, JournalSheet)

### Backend layering

- **routers** → thin HTTP
- **services** → business logic
- **repositories** → SQL + vector queries
- **workers** → async pipeline (optional Celery/ARQ or FastAPI BackgroundTasks → queue later)

---

## 3. Conventions to Establish (Phase 3)

- **Monorepo layout:** `ios/SeedJournal`, `backend/`, `docs/`, `infra/` (docker-compose for local PG)
- **API:** REST + OpenAPI; version prefix `/v1`
- **IDs:** UUID v7 or ULID for sortable entries
- **Time:** UTC in DB; user timezone on client for “seasons”
- **Logging:** Structured JSON server-side; no journal body in logs
- **i18n:** English first; string catalogs prepared
- **Accessibility:** Dynamic Type, VoiceOver labels on tree metaphors

---

## 4. Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| **AI as therapy replacement** | High (App Review / trust) | Copy + prompts: “reflection tool, not medical advice”; crisis resources link in settings |
| **Privacy breach of journal content** | Critical | E2E optional later; minimum: TLS, encryption at rest, strict RBAC, audit access |
| **Gamification creep** | High (brand) | Code review checklist: no XP, streaks, badges in tree module |
| **Tree feels like punishment** | High (UX) | Winter/leaf loss = narrative season, never locked features or shame copy |
| **LLM cost / latency** | Medium | Stage pipeline: fast model for extraction, quality model for guide; cache embeddings |
| **Memory hallucination in retrieval** | Medium | Store source `entry_id`; cite in AI replies; confidence thresholds |
| **Empty repo → big-bang delivery** | Medium | Vertical slices (auth → single entry → one memory → minimal tree) |
| **Apple HIG / premium bar** | Medium | Phase 4 polish gate; custom tree renderer performance budget |
| **pgvector ops complexity** | Low–Medium | Managed Postgres (Neon/Supabase/RDS) with extension enabled |
| **Solo-agent consistency** | Medium | ADRs in `docs/adr/`, single design token source |

---

## 5. Dependencies (Planned)

**iOS:** iOS 17+, SwiftUI, async/await, Keychain Services, Sign in with Apple  
**Backend:** Python 3.11+, FastAPI, SQLAlchemy 2, Alembic, pgvector, httpx, pydantic-settings  
**Infra (dev):** Docker Compose (Postgres 16 + pgvector), optional LocalStack not required v1  
**AI:** Provider-agnostic interface (OpenAI / Anthropic / local via config)

---

## 6. Phase 1 Exit Criteria

- [x] Repository state documented (greenfield)
- [x] Architecture overview defined
- [x] Implementation plan drafted (see `EXECUTION_PLAN.md`)
- [x] Risks registered
- [ ] Stakeholder alignment on Phase 2 artifacts (product spec, schema, screens) — next step

**No application code written in Phase 1** per build strategy.