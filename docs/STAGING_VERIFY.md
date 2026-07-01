# Staging deploy & verify

Target API: **https://seedjournal-api-staging.fly.dev**  
iOS: scheme **SeedJournal-Staging** → `ios/Config/Staging.xcconfig`

---

## Part 1 — One-time Fly + database setup

### 1. Neon (or Supabase) database

1. Create a Postgres 16 project.
2. SQL console:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

3. Build async URL (required by the app):

```
postgresql+asyncpg://USER:PASSWORD@HOST/neondb?sslmode=require
```

Copy it — you will use it only in `fly secrets`, never in git.

### 2. Install Fly CLI

- Windows: `powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"`
- Mac: `brew install flyctl`

```bash
fly auth login
```

### 3. Create app and secrets

From repo root:

```bash
cd backend
fly apps create seedjournal-api-staging
fly secrets set -a seedjournal-api-staging \
  DATABASE_URL="postgresql+asyncpg://..." \
  JWT_SECRET="$(openssl rand -hex 32)" \
  APPLE_CLIENT_ID="com.seedjournal.app" \
  APP_ENV="production" \
  LLM_PROVIDER="openai" \
  OPENAI_API_KEY="sk-your-key" \
  CORS_ORIGINS="https://minaelzek.github.io"
```

| Secret | Notes |
|--------|--------|
| `DATABASE_URL` | Must be `postgresql+asyncpg://` |
| `JWT_SECRET` | Long random string |
| `APP_ENV` | **`production`** on staging (disables dev JSON Apple auth) |
| `LLM_PROVIDER` | `openai` for real AI, or `stub` to save cost while testing infra |
| `OPENAI_API_KEY` | Required if `LLM_PROVIDER=openai` |

### 4. Deploy

```bash
cd backend
fly deploy --depot=false -c fly.staging.toml
```

Stuck on `Waiting for depot builder...`? Use `--depot=false` (above) or see [`FLY_DEPLOY_TROUBLESHOOTING.md`](FLY_DEPLOY_TROUBLESHOOTING.md).

Wait until `Visit your newly deployed app at https://seedjournal-api-staging.fly.dev`.

Migrations run on container start (`alembic upgrade head` in Dockerfile).

### 5. GitHub auto-deploy (optional)

1. `fly tokens create deploy -a seedjournal-api-staging` → copy token  
2. GitHub repo → **Settings → Secrets → Actions** → `FLY_API_TOKEN`  
3. **Actions → Deploy Staging (Fly) → Run workflow**

---

## Part 2 — Verify API (no phone yet)

### Windows (PowerShell)

```powershell
.\scripts\smoke_staging.ps1 -BaseUrl https://seedjournal-api-staging.fly.dev
```

### Git Bash / Mac

```bash
bash scripts/smoke_staging.sh https://seedjournal-api-staging.fly.dev
```

### Manual checks

| URL | Expected |
|-----|----------|
| `https://seedjournal-api-staging.fly.dev/health` | `{"status":"ok"}` |
| `https://seedjournal-api-staging.fly.dev/v1/health` | `status` + `service` |
| `https://seedjournal-api-staging.fly.dev/docs` | FastAPI Swagger (optional) |

### If health fails

```bash
fly logs -a seedjournal-api-staging
fly status -a seedjournal-api-staging
fly ssh console -a seedjournal-api-staging -C "alembic current"
```

Common issues:

- **Crash loop** — wrong `DATABASE_URL` or DB not reachable from Fly  
- **Migration error** — pgvector extension missing on Neon  
- **Cold start** — first request after idle may take ~10s (`min_machines_running = 0`)

---

## Part 3 — Verify iOS against staging (Mac + iPhone)

1. Confirm `ios/Config/Staging.xcconfig`:

```
SEEDJOURNAL_API_BASE_URL = https:/$()/seedjournal-api-staging.fly.dev/v1
```

2. `cd ios && xcodegen generate && open SeedJournal.xcodeproj`

3. Select scheme **SeedJournal-Staging**, run on **physical device**.

4. **Sign in with Apple** (dev JSON sign-in does **not** work when `APP_ENV=production`).

5. Smoke test on device:

- [ ] Sign in succeeds  
- [ ] Save a journal entry  
- [ ] Optional reflection → complete  
- [ ] Tree home loads (`GET /v1/tree`)  
- [ ] Settings → Privacy policy opens GitHub Pages URL  

---

## Part 4 — When staging is verified

Reply **“staging is deployed”** with:

- Smoke script output (health ok), or  
- Any `fly logs` error if stuck  

Then we can tune OpenAI vs stub, rate limits, or TestFlight archive steps.

---

## Quick reference

| Item | Value |
|------|--------|
| Fly app | `seedjournal-api-staging` |
| Deploy config | `backend/fly.staging.toml` |
| iOS API base | `https://seedjournal-api-staging.fly.dev/v1` |
| Privacy | `https://minaelzek.github.io/SeedJournalV1/privacy/` |