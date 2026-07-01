# SeedJournal — Execution Plan

Premium AI-guided reflection journal · App Store trajectory

---

## North Star

User opens app → **private sanctuary** → writes what they usually avoid → AI deepens reflection without taking control → **memories** accumulate → **sakura tree** subtly reflects inner growth over months.

---

## Phase 2 Deliverables (Complete)

Create under `docs/` before major implementation:

| Artifact | Path | Purpose |
|----------|------|---------|
| Product specification | `docs/PRODUCT_SPEC.md` | Jobs-to-be-done, flows, non-goals |
| Technical architecture | `docs/TECHNICAL_ARCHITECTURE.md` | Services, contracts, deployment |
| Database schema | `docs/DATABASE_SCHEMA.md` + `backend/alembic/` later | PostgreSQL + pgvector |
| AI pipeline design | `docs/AI_PIPELINE.md` | Stages, prompts, safety |
| Screen map | `docs/SCREEN_MAP.md` | Tree-centric IA, no tab bar |

**Gate:** Architecture + schema reviewed against product principles (no gamification, no social).

---

## Phase 3 — Implementation (Incremental Vertical Slices)

### Slice 0 — Foundation ✅

- Init `git`, README, `.gitignore`, `docker-compose.yml` (Postgres + pgvector)
- FastAPI skeleton: health, `/v1`, OpenAPI, settings, Alembic
- iOS Xcode project: `SeedJournal`, design tokens, empty Tree placeholder
- Sign in with Apple + JWT (or session cookie pattern for web admin later)
- **Review:** security (token storage Keychain), no secrets in repo

### Slice 1 — Journal Core ✅

- Create/read journal entries (user-owned)
- SwiftUI: tree home + floating/sheet **Journal** compose
- API: `POST/GET /v1/entries`
- **Review:** UX calm typography, no chat bubbles as default metaphor

### Slice 2 — AI Guide (Controlled) ✅

- Post-save optional 1–2 questions; user chooses **Continue** or **Save**
- Conversation stored as `reflection_turns` linked to entry
- Prompt layer: listen-first, no authority tone
- **Review:** AI behavior checklist vs product principles

### Slice 3 — Memory Extraction + Vectors ✅

- Background job: extract memory candidates (values, beliefs, goals, patterns, moments, realizations)
- Embed with pgvector; link `source_entry_id`
- Retrieval API for “related memories” and timeline queries
- **Review:** hallucination guards, logging excludes body text

### Slice 4 — Sakura Tree v1 ✅

- State model: Seed → Sprout → Sapling → Sakura → Blooming
- Roots / branches / leaves / flowers as **data-driven visualization** (not XP)
- Growth inputs: depth signals from analysis + memory importance + gentle consistency (no streak UI)
- Seasons: winter narrative without punishment
- **Review:** UX + architecture — tree module isolated from journal text

### Slice 5 — History & Self-Queries ✅

- Past reflections browser (editorial list, not feed)
- “When did I first talk about X?” via semantic search + UI
- Pattern summaries (careful, non-diagnostic language)
- **Review:** performance on vector search, pagination

### Slice 6 — Production Hardening ✅

- Rate limits, idempotency keys, retries on AI steps
- Observability (metrics, tracing), backup strategy
- Privacy policy hooks, export/delete account (GDPR-style)
- **Review:** security audit pass

---

## Phase 4 — App Store Polish

| Area | Actions |
|------|---------|
| Visual | Token audit, dark mode, tree animation budget (60fps target) |
| Motion | Subtle bloom/season transitions; reduce motion respect |
| Onboarding | 3 calm screens: sanctuary, tree metaphor, AI as guide |
| Accessibility | VoiceOver tree summary, Dynamic Type, contrast |
| Performance | Cold start, entry save latency, offline graceful messaging |
| Emotional QA | Script-based walkthrough: “mature, not childish” |
| Submission | Screenshots, App Privacy labels, age rating, review notes |

---

## Agentic Loop (Every Major Feature)

After each slice:

1. **Code review** — layering, tests, no gamification leaks  
2. **Architecture review** — module boundaries, API stability  
3. **UX review** — calm, premium, user control  
4. **Security review** — auth, PII, logs, AI data handling  

Fix issues before next slice.

---

## Recommended Repo Structure (Phase 3)

```
SeedJournalV1/
├── docs/
│   ├── PHASE1_REPOSITORY_ANALYSIS.md
│   ├── EXECUTION_PLAN.md
│   ├── PRODUCT_SPEC.md          (Phase 2)
│   ├── TECHNICAL_ARCHITECTURE.md
│   ├── DATABASE_SCHEMA.md
│   ├── AI_PIPELINE.md
│   ├── SCREEN_MAP.md
│   └── adr/
├── ios/
│   └── SeedJournal/
├── backend/
│   ├── app/
│   ├── alembic/
│   ├── tests/
│   └── pyproject.toml
├── infra/
│   └── docker-compose.yml
└── README.md
```

---

## Decision Log (Initial)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Navigation | Tree-centric, no tab bar | Product philosophy — object not dashboard |
| Auth | Sign in with Apple | Premium iOS norm, privacy |
| Vector store | pgvector in Postgres | One datastore, simpler ops |
| AI UI | Optional follow-up questions, user ends session | User control |
| Tree growth | Signal-based, non-linear seasons | Avoid XP; emotional honesty |
| Backend language | Python FastAPI | Stated preference, strong AI ecosystem |

---

## Immediate Next Actions

1. **Ship prep:** Xcode project, Sign in with Apple, Keychain, production deploy, TestFlight.  
2. **Define LLM provider + Apple Developer** credentials in secure env (not in repo).  
3. `docker compose up` in `infra/` for local Postgres.

Phase 2 complete. Slice 0 foundation landed.