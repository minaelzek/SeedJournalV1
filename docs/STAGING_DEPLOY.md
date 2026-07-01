# Staging Deployment

> **Start here:** [`SHIP_CHECKLIST.md`](SHIP_CHECKLIST.md) and [`STAGING_VERIFY.md`](STAGING_VERIFY.md) (canonical step-by-step). This file is extended reference.

Deploy the FastAPI backend to **Fly.io** (recommended) or **Railway**. iOS TestFlight builds point at staging via `Staging.xcconfig`.

---

## Prerequisites

- [Fly CLI](https://fly.io/docs/hands-on/install-flyctl/) (`fly auth login`)
- Postgres **16** with **pgvector** ([Neon](https://neon.tech), [Supabase](https://supabase.com), or Fly Postgres)
- Apple Developer: Sign in with Apple configured for `com.seedjournal.app`

---

## 1. Database (Neon example)

1. Create project → enable `vector` extension in SQL console:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

2. Copy connection string. For async SQLAlchemy use:

```
postgresql+asyncpg://USER:PASS@HOST/DB?sslmode=require
```

---

## 2. Fly.io API

```bash
cd backend
fly apps create seedjournal-api-staging   # or use fly.toml app name
fly secrets set \
  DATABASE_URL="postgresql+asyncpg://..." \
  JWT_SECRET="$(openssl rand -hex 32)" \
  APPLE_CLIENT_ID="com.seedjournal.app" \
  LLM_PROVIDER="openai" \
  OPENAI_API_KEY="sk-..." \
  CORS_ORIGINS="https://seedjournal.app"
fly deploy
```

Verify:

```bash
curl https://seedjournal-api-staging.fly.dev/health
curl https://seedjournal-api-staging.fly.dev/v1/health
```

**Note:** Rename `app` in `fly.toml` to your Fly app name before deploy.

---

## 3. Migrations

Migrations run on container start (`Dockerfile` CMD). To run manually:

```bash
fly ssh console -C "alembic upgrade head"
```

---

## 4. iOS → staging API

1. Edit `ios/Config/Staging.xcconfig`:

```
SEEDJOURNAL_API_BASE_URL = https://YOUR_APP.fly.dev/v1
```

2. In Xcode: add **Staging** build configuration (duplicate Release), assign `Staging.xcconfig`.
3. Archive with **Staging** for TestFlight against staging API.

`APIConfig.swift` reads `SEEDJOURNAL_API_BASE_URL` from Info.plist (injected via xcconfig).

For **DEBUG** simulator, localhost is still default unless you override in scheme environment.

---

## 5. GitHub Actions

| Workflow | Purpose |
|----------|---------|
| `.github/workflows/backend.yml` | Postgres + pgvector, `pytest` |
| `.github/workflows/ios.yml` | macOS: XcodeGen + Simulator builds (Debug + Staging) |

Optional: uncomment `deploy-staging` / `testflight` jobs when secrets are configured.

## 5b. Terraform (optional)

`infra/terraform/staging/` registers the Fly app name. Deploy code with `fly deploy`; set secrets with `fly secrets set`. See `infra/terraform/staging/README.md`.

---

## 6. Railway (alternative)

1. New project → Deploy from repo → root `backend/`
2. Add PostgreSQL plugin or external `DATABASE_URL`
3. Set env vars from `backend/.env.example`
4. Start command: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## 7. Post-deploy smoke test

```bash
# Dev-style auth only works when APP_ENV=development — staging should use real Apple tokens from iOS
curl -s https://YOUR_API/health | jq .
```

Use the iOS app (Sign in with Apple) against staging URL to validate end-to-end.

---

## Security checklist (staging)

- [ ] `APP_ENV=production` on Fly
- [ ] Strong `JWT_SECRET` (32+ bytes random)
- [ ] `CORS_ORIGINS` limited (not `*` in production)
- [ ] No `.env` in Docker image (secrets via platform)
- [ ] TLS only (Fly force HTTPS)