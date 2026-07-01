# Fly deploy troubleshooting

## Stuck on `Waiting for depot builder...`

Fly’s default remote build uses **Depot**. That line means “waiting for a build machine”—often **2–8 minutes**, sometimes **hangs** (Depot/Fly capacity or regional issues).

### Fix 1 — Use legacy Fly builder (recommended workaround)

From `backend/`:

```powershell
fly deploy --depot=false -c fly.staging.toml
```

Production:

```powershell
fly deploy --depot=false -c fly.production.toml
```

Slower than Depot when it works, but usually **completes** when Depot is stuck.

### Fix 2 — Reset builder (dashboard)

1. https://fly.io/dashboard → your app → **Builders** (or App builders)  
2. **Reset** builder, wait 2 min, deploy again  

### Fix 3 — Build locally (needs Docker Desktop running)

```powershell
cd backend
fly deploy --local-only -c fly.staging.toml
```

Uses your machine’s Docker; good on Windows if Depot and legacy remote both fail.

### Fix 4 — GitHub Actions deploy

If local CLI keeps hanging:

1. Set GitHub secret **`FLY_API_TOKEN`** (`fly tokens create deploy -a seedjournal-api-staging`)  
2. **Actions → Deploy Staging (Fly) → Run workflow**  

Uses Fly’s CI environment; may succeed when your laptop CLI does not.

---

## 502 Bad Gateway right after deploy

DNS and machine exist, but Fly’s proxy gets no healthy app (common on **first deploy**).

```powershell
fly status -a seedjournal-api-staging
fly logs -a seedjournal-api-staging
```

**Typical log patterns:**

| Message | Fix |
|---------|-----|
| `could not translate host name "YOUR_NEON_URL"` | You pasted the **doc placeholder**. Set a real Neon host in `fly secrets set` (see below). |
| `could not connect to server` / `SSL` / `password authentication` | Fix `DATABASE_URL`: must be `postgresql+asyncpg://user:pass@host/db?sslmode=require` (Neon **pooled** or direct host) |
| `extension "vector" does not exist` | Neon SQL: `CREATE EXTENSION IF NOT EXISTS vector;` |
| Alembic / `DuplicateTable` / migration | `fly ssh console -a seedjournal-api-staging -C "alembic upgrade head"` and read error |
| App starts then killed | `fly scale memory 512 -a seedjournal-api-staging` if OOM |

After fixing secrets:

```powershell
fly secrets set -a seedjournal-api-staging DATABASE_URL="postgresql+asyncpg://..."
fly apps restart seedjournal-api-staging
```

Wait 30–60s (cold start), then:

```powershell
.\scripts\smoke_staging.ps1 -BaseUrl https://seedjournal-api-staging.fly.dev
```

---

## After deploy: app won’t start

```powershell
fly logs -a seedjournal-api-staging
fly status -a seedjournal-api-staging
```

| Log hint | Fix |
|----------|-----|
| `DATABASE_URL` / connection refused | Neon URL must be `postgresql+asyncpg://...?sslmode=require`; allow Neon from Fly IPs |
| `extension "vector" does not exist` | Run `CREATE EXTENSION vector;` on Neon |
| Alembic error | `fly ssh console -a seedjournal-api-staging -C "alembic current"` |
| Health check failing | Cold start: wait 30s, retry `/health` |

---

## Smoke test

```powershell
.\scripts\smoke_staging.ps1 -BaseUrl https://seedjournal-api-staging.fly.dev
```

---

## Status pages

- https://status.flyio.net/  
- Fly community: search “depot builder” for current outages