# SeedJournal

[![Backend CI](https://github.com/minaelzek/SeedJournalV1/actions/workflows/backend.yml/badge.svg)](https://github.com/minaelzek/SeedJournalV1/actions/workflows/backend.yml)
[![iOS CI](https://github.com/minaelzek/SeedJournalV1/actions/workflows/ios.yml/badge.svg)](https://github.com/minaelzek/SeedJournalV1/actions/workflows/ios.yml)

CI failed? See [`docs/TROUBLESHOOTING_CI.md`](docs/TROUBLESHOOTING_CI.md).

**MVP status:** [`docs/COMPLETION_STATUS.md`](docs/COMPLETION_STATUS.md) — code complete. **Ship:** [`docs/SHIP_CHECKLIST.md`](docs/SHIP_CHECKLIST.md).

A premium AI-guided reflection journal for young adults. Thoughts become memories; memories become insights; growth is shown through a living sakura tree—not gamification.

**Public repo** — [`SECURITY.md`](SECURITY.md) · [Privacy policy (GitHub Pages)](https://minaelzek.github.io/SeedJournalV1/privacy/) *(enable Pages: [`docs/ENABLE_GITHUB_PAGES.md`](docs/ENABLE_GITHUB_PAGES.md))*

## Quick start

```bash
# Database
cd infra && docker compose up -d

# API
cd backend && cp .env.example .env
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# iOS (macOS)
cd ios && xcodegen generate && open SeedJournal.xcodeproj
```

Simulator: DEBUG → `http://127.0.0.1:8000/v1` · Dev sign-in in DEBUG builds.

**CI green?** → [`docs/NEXT_STEPS_AFTER_CI.md`](docs/NEXT_STEPS_AFTER_CI.md) (Fly staging, Xcode, TestFlight)

## Ship path

| Step | Doc |
|------|-----|
| GitHub / CI | [`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md) |
| Privacy URL | [`docs/ENABLE_GITHUB_PAGES.md`](docs/ENABLE_GITHUB_PAGES.md) |
| Local + Xcode | [`docs/SHIP_PREP.md`](docs/SHIP_PREP.md) |
| Staging API | [`docs/STAGING_VERIFY.md`](docs/STAGING_VERIFY.md) |
| TestFlight | [`docs/TESTFLIGHT.md`](docs/TESTFLIGHT.md) |
| App Store | [`docs/APP_STORE_READINESS.md`](docs/APP_STORE_READINESS.md) · [`docs/APP_STORE_SCREENSHOTS.md`](docs/APP_STORE_SCREENSHOTS.md) |

## Stack

| Layer | Technology |
|-------|------------|
| iOS | Swift, SwiftUI, Sign in with Apple, Keychain |
| API | Python, FastAPI, Alembic |
| Data | PostgreSQL 16, pgvector |
| AI | Pluggable LLM (stub dev / OpenAI prod) |

## Philosophy

- **Journal** = input  
- **AI** = gentle guide (not therapist, not coach)  
- **Memory system** = intelligence  
- **Sakura tree** = emotional representation of growth  

## Documentation

- [Repository map & ADRs](docs/REPOSITORY.md)
- [HTTP API reference](docs/API.md)
- [Product spec](docs/PRODUCT_SPEC.md)
- [Technical architecture](docs/TECHNICAL_ARCHITECTURE.md)
- [Execution plan](docs/EXECUTION_PLAN.md)
- [Database schema](docs/DATABASE_SCHEMA.md)
- [AI pipeline](docs/AI_PIPELINE.md)
- [Screen map](docs/SCREEN_MAP.md)

## License

[MIT](LICENSE)