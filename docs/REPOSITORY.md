# Repository map

**Source of truth:** https://github.com/minaelzek/SeedJournalV1  
**Default branch:** `main`  
**License:** MIT

---

## Layout

```
SeedJournalV1/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/v1/          # HTTP routers (thin)
│   │   ├── core/            # config, security, middleware
│   │   ├── db/              # SQLAlchemy models
│   │   ├── identity/        # Apple auth, users
│   │   ├── journal/         # entries
│   │   ├── reflection/      # guided turns
│   │   ├── intelligence/    # analysis, extraction, embeddings
│   │   ├── memories/        # memory CRUD + search
│   │   ├── growth/          # tree projection, seasons
│   │   ├── ai_guide/        # LLM client + prompts
│   │   └── workers/         # post-reflection pipeline
│   ├── alembic/versions/    # schema migrations
│   └── tests/
├── ios/                     # SwiftUI (XcodeGen → SeedJournal.xcodeproj)
├── infra/                   # docker-compose, terraform, SQL utilities
├── docs/                    # product, architecture, ADRs, ship runbooks
└── .github/workflows/       # CI, Pages, optional Fly deploy
```

---

## Architecture decisions

| ADR | Topic |
|-----|--------|
| [001](adr/001-pgvector-in-postgres.md) | pgvector in PostgreSQL |
| [002](adr/002-tree-centric-navigation.md) | Tree-centric navigation (no tab bar) |
| [003](adr/003-sign-in-with-apple.md) | Sign in with Apple v1 |
| [004](adr/004-inline-pipeline-in-tests.md) | Inline intelligence pipeline under pytest |
| [005](adr/005-optional-hnsw-index.md) | HNSW index outside Alembic CI |

---

## CI

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `backend.yml` | `backend/**` | Migrate + pytest |
| `ios.yml` | `ios/**` | XcodeGen + simulator build |
| `pages.yml` | `main` | Privacy static site |
| `deploy-staging.yml` | manual | Fly deploy |

---

## Documentation index

| Audience | Start here |
|----------|------------|
| New contributor | [CONTRIBUTING.md](../CONTRIBUTING.md), [PRODUCT_SPEC.md](PRODUCT_SPEC.md) |
| Backend dev | [backend/README.md](../backend/README.md), [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) |
| iOS dev | [ios/SeedJournal/README.md](../ios/SeedJournal/README.md), [SCREEN_MAP.md](SCREEN_MAP.md) |
| Ship / ops | [COMPLETION_STATUS.md](COMPLETION_STATUS.md), [SHIP_PREP.md](SHIP_PREP.md), [STAGING_VERIFY.md](STAGING_VERIFY.md) |
| QA | [EMOTIONAL_QA_SCRIPT.md](EMOTIONAL_QA_SCRIPT.md) |
| CI failures | [TROUBLESHOOTING_CI.md](TROUBLESHOOTING_CI.md) |

---

## Git workflow

- **Branch:** `feat/*`, `fix/*`, `docs/*`, `chore/*`, `ci/*`, `refactor/*`
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/) (see CONTRIBUTING)
- **PRs:** one concern; link issue if applicable; green CI required