# Next steps — CI is green

Backend, iOS, and Pages workflows are passing. Do these in order.

---

## A. Confirm live URLs (2 min)

| Check | URL |
|-------|-----|
| Privacy policy | https://minaelzek.github.io/SeedJournalV1/privacy/ |
| Repo | https://github.com/minaelzek/SeedJournalV1 |
| Actions | https://github.com/minaelzek/SeedJournalV1/actions |

Open the privacy link on your phone. If it loads, App Review URL in xcconfig is valid.

---

## B. Staging API on Fly.io (~30 min)

Needs: [Fly account](https://fly.io), [Neon](https://neon.tech) or other Postgres 16 + pgvector.

### B1. Database (Neon)

1. New project → SQL editor:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

2. Copy connection string → convert to async:

`postgresql+asyncpg://USER:PASS@HOST/DB?sslmode=require`

### B2. Fly app

```powershell
cd backend
fly auth login
fly apps create seedjournal-api-staging
fly secrets set DATABASE_URL="postgresql+asyncpg://..." JWT_SECRET="<openssl rand -hex 32>" APPLE_CLIENT_ID="com.seedjournal.app" APP_ENV="production" LLM_PROVIDER="openai" OPENAI_API_KEY="sk-..." CORS_ORIGINS="https://minaelzek.github.io"
fly deploy
```

### B3. Smoke test

```bash
bash scripts/smoke_staging.sh https://seedjournal-api-staging.fly.dev
```

### B4. iOS staging URL

Edit `ios/Config/Staging.xcconfig` if your Fly app name differs.

Step-by-step verify: [`STAGING_VERIFY.md`](STAGING_VERIFY.md) · reference: [`STAGING_DEPLOY.md`](STAGING_DEPLOY.md)

---

## C. iOS on your Mac (~45 min)

```bash
brew install xcodegen
cd ios && xcodegen generate && open SeedJournal.xcodeproj
```

1. Signing → Team → `com.seedjournal.app`
2. App Icon 1024×1024 in Assets
3. Scheme **SeedJournal-Staging** on a **physical device** (Sign in with Apple)

Detail: [`TESTFLIGHT.md`](TESTFLIGHT.md)

---

## D. TestFlight → E. App Store

See [`TESTFLIGHT.md`](TESTFLIGHT.md) and [`APP_STORE_READINESS.md`](APP_STORE_READINESS.md).

---

## Optional: deploy staging from GitHub

1. Create Fly app + set secrets on Fly (`fly secrets set`) — see section B  
2. GitHub → **Settings → Secrets → Actions** → `FLY_API_TOKEN`  
3. **Actions** → **Deploy Staging (Fly)** → **Run workflow**