# SeedJournal — completion status

**Repository milestone:** MVP **code + docs + CI** complete (2026-03-30).  
**Product milestone:** App Store live — requires **your** Apple, Fly/Neon, and QA steps below.

---

## Done in repository

| Area | Status |
|------|--------|
| Phase 1–2 docs | ✅ |
| Slices 0–6 (backend + iOS features) | ✅ |
| Phase 4 baseline (onboarding, a11y tree, settings, privacy link) | ✅ |
| CI: Backend, iOS, Pages, manual Fly deploy workflow | ✅ |
| Alembic 001–002, stub + OpenAI providers | ✅ |
| Git hygiene: ADRs, API.md, CONTRIBUTING, PR/issue templates | ✅ |
| Public repo: LICENSE, SECURITY, Dependabot | ✅ |

---

## Requires operator (cannot be automated in git)

| Step | Owner | Doc |
|------|--------|-----|
| GitHub Pages live URL verified | You | [`ENABLE_GITHUB_PAGES.md`](ENABLE_GITHUB_PAGES.md) |
| Neon + Fly staging/prod API | You | [`STAGING_VERIFY.md`](STAGING_VERIFY.md) |
| XcodeGen + Team + App Icon 1024 | You (Mac) | [`SHIP_PREP.md`](SHIP_PREP.md) |
| Sign in with Apple on device | You | [`TESTFLIGHT.md`](TESTFLIGHT.md) |
| TestFlight + emotional QA | You | [`EMOTIONAL_QA_SCRIPT.md`](EMOTIONAL_QA_SCRIPT.md) |
| App Store Connect metadata | You | [`APP_STORE_SCREENSHOTS.md`](APP_STORE_SCREENSHOTS.md) |
| Production `api.seedjournal.app` DNS + TLS | You | `ios/Config/Release.xcconfig` |

---

## Definition of “total completion”

1. **Engineering (repo):** Feature scope in `EXECUTION_PLAN.md` implemented; `main` CI green — **achieved**.  
2. **Shippable beta:** Staging API + TestFlight build + internal QA — **your next gate**.  
3. **App Store:** Review approval — **after beta**.

---

## Single entry point after clone

```bash
# 1. Read
docs/REPOSITORY.md

# 2. Local API
infra/docker compose up -d
cd backend && pip install -e ".[dev]" && alembic upgrade head && uvicorn app.main:app --reload

# 3. Ship path
docs/NEXT_STEPS_AFTER_CI.md
```