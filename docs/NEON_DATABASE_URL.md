# Neon → Fly `DATABASE_URL`

**New to Neon?** Start with [`NEON_SETUP_BEGINNER.md`](NEON_SETUP_BEGINNER.md) (skip the “connect editor” step).

## 1. Neon console

1. https://console.neon.tech → your project  
2. **SQL Editor** → run:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

3. **Dashboard → Connection details**  
   - Copy connection string (direct or pooled).  
   - Host looks like: `ep-cool-name-12345678.us-east-2.aws.neon.tech`  
   - **Not** `YOUR_NEON_URL` or `localhost`.

## 2. Convert for SeedJournal

Neon gives something like:

```text
postgresql://neondb_owner:SECRET@ep-xxxx.neon.tech/neondb?sslmode=require
```

Change the prefix only:

```text
postgresql+asyncpg://neondb_owner:SECRET@ep-xxxx.neon.tech/neondb?sslmode=require
```

**Password special characters** (`@`, `#`, `%`, etc.): URL-encode them, or reset the Neon role password to alphanumeric only for staging.

## 3. Set on Fly (PowerShell)

Use your **real** string in one line (quotes):

```powershell
fly secrets set -a seedjournal-api-staging `
  DATABASE_URL="postgresql+asyncpg://neondb_owner:YOUR_PASSWORD@ep-xxxx.us-east-2.aws.neon.tech/neondb?sslmode=require" `
  JWT_SECRET="paste-a-long-random-string-here-min-32-chars"
```

Also ensure (if not set yet):

```powershell
fly secrets set -a seedjournal-api-staging `
  APPLE_CLIENT_ID="com.seedjournal.app" `
  APP_ENV="production" `
  LLM_PROVIDER="stub" `
  CORS_ORIGINS="https://minaelzek.github.io"
```

**No redeploy required** — Fly restarts machines when secrets change.

## 4. Verify

```powershell
fly logs -a seedjournal-api-staging
```

You should see Alembic run, then Uvicorn listening — not `YOUR_NEON_URL`.

```powershell
.\scripts\smoke_staging.ps1 -BaseUrl https://seedjournal-api-staging.fly.dev
```

`fly status` → **STATE: started**, checks **passing**.