# Ship checklist (operator)

Print or keep open while deploying. **Repo is complete** — check boxes as *you* finish each gate.

---

## Gate 0 — GitHub (5 min)

- [ ] https://github.com/minaelzek/SeedJournalV1/actions — **Backend**, **iOS**, **Pages** green on `main`
- [ ] Privacy loads on phone: https://minaelzek.github.io/SeedJournalV1/privacy/

```powershell
.\scripts\validate_ship_prereqs.ps1
```

---

## Gate 1 — Database (Neon ~10 min)

Guide: [`NEON_SETUP_BEGINNER.md`](NEON_SETUP_BEGINNER.md) — **skip** Neon’s “connect editor” prompt.

- [ ] Postgres 16 project created
- [ ] SQL run:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

- [ ] Connection string converted to **`postgresql+asyncpg://...?sslmode=require`**

---

## Gate 2 — Fly staging (~20 min)

```powershell
fly auth login
cd backend
fly apps create seedjournal-api-staging
fly secrets set -a seedjournal-api-staging DATABASE_URL="postgresql+asyncpg://..." JWT_SECRET="<64-char-random>" APPLE_CLIENT_ID="com.seedjournal.app" APP_ENV="production" LLM_PROVIDER="stub" CORS_ORIGINS="https://minaelzek.github.io"
# Add OPENAI_API_KEY if LLM_PROVIDER=openai
fly deploy --depot=false -c fly.staging.toml
```

If stuck on **Waiting for depot builder**, see [`FLY_DEPLOY_TROUBLESHOOTING.md`](FLY_DEPLOY_TROUBLESHOOTING.md).

- [ ] `fly status -a seedjournal-api-staging` shows running machine
- [ ] Smoke:

```powershell
.\scripts\smoke_staging.ps1 -BaseUrl https://seedjournal-api-staging.fly.dev
```

**Optional CI deploy:** GitHub secret `FLY_API_TOKEN` → Actions → **Deploy Staging (Fly)** → Run workflow (runs smoke after deploy).

Detail: [`STAGING_VERIFY.md`](STAGING_VERIFY.md)

---

## Gate 3 — iOS device (Mac ~45 min)

- [ ] `brew install xcodegen && cd ios && xcodegen generate`
- [ ] Xcode → Signing → your Team → `com.seedjournal.app`
- [ ] **1024×1024** App Icon in Assets
- [ ] Scheme **SeedJournal-Staging** on **physical iPhone**
- [ ] Sign in with Apple works
- [ ] Save entry → tree updates

Detail: [`TESTFLIGHT.md`](TESTFLIGHT.md)

---

## Gate 4 — TestFlight (~30 min)

- [ ] Archive **SeedJournal-Staging** or Release per runbook
- [ ] Upload to App Store Connect
- [ ] Internal testers invited
- [ ] [`EMOTIONAL_QA_SCRIPT.md`](EMOTIONAL_QA_SCRIPT.md) completed — no fail criteria

---

## Gate 5 — App Store

- [ ] Screenshots per [`APP_STORE_SCREENSHOTS.md`](APP_STORE_SCREENSHOTS.md)
- [ ] Privacy nutrition labels per [`APP_STORE_READINESS.md`](APP_STORE_READINESS.md)
- [ ] Review notes (not medical / not social)
- [ ] Production API (`Release.xcconfig`) + `fly deploy -c fly.production.toml`

---

## When stuck

| Symptom | Doc |
|---------|-----|
| CI / Alembic | [`TROUBLESHOOTING_CI.md`](TROUBLESHOOTING_CI.md) |
| Fly crash / DB | `fly logs -a seedjournal-api-staging` |
| Apple sign-in | [`SHIP_PREP.md`](SHIP_PREP.md) § Sign in with Apple |

**Done when:** Gates 0–4 complete → TestFlight beta. Gate 5 → public App Store.