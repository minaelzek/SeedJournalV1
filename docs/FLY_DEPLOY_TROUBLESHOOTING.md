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