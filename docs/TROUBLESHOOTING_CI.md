# Backend CI troubleshooting

Workflow: **`.github/workflows/backend.yml`**  
View logs: https://github.com/minaelzek/SeedJournalV1/actions/workflows/backend.yml

---

## What the job does

1. Start **pgvector/pg16** service on `localhost:5432`
2. `pip install -e ".[dev]"` in `backend/`
3. `alembic upgrade head` (migrations 001 + 002)
4. `pytest -v`

---

## Common failures

### Migrate step — `alembic upgrade head`

| Symptom | Fix |
|---------|-----|
| `connection refused` | Postgres service not ready — workflow waits 30s; re-run job |
| `extension "vector" does not exist` | Wrong Postgres image — must be `pgvector/pgvector:pg16` |
| HNSW / index error | Migration **002 is a no-op**; run `infra/sql/create_hnsw_index.sql` on prod manually |
| `type "memory_type" already exists` | Fixed in 001 via `CREATE TYPE ... EXCEPTION` + `create_type=False` |

### Pytest — auth skipped vs failed

- **`skipped`** — cannot reach DB (should not happen in CI if migrate passed)
- **`failed`** — open test name in log

| Test file | Typical cause |
|-----------|----------------|
| `test_slice3` | Pipeline / memories — fixed by inline pipeline under pytest |
| `test_slice6` | `test_delete_account` needs ephemeral user (already separate fixture) |
| `test_slice2` | Reflection + AI — needs `APP_ENV=development` dev auth |

### Email: "all jobs have failed"

Usually only the **`test`** job exists. Check which **step** failed (Install / Migrate / Pytest).

**Deploy Staging (Fly)** is a **separate** workflow — fails if `FLY_API_TOKEN` is missing when you run it manually.

---

## Reproduce locally (Windows)

```powershell
cd infra
docker compose up -d
cd ..\backend
$env:DATABASE_URL="postgresql+asyncpg://seedjournal:seedjournal_dev@127.0.0.1:5432/seedjournal"
$env:APP_ENV="development"
$env:JWT_SECRET="ci-secret"
alembic upgrade head
pytest -v
```

Requires **Docker Desktop running**.

---

## After a fix

Push to `main` → Backend CI runs automatically on `backend/**` changes.

Or: **Actions → Backend CI → Run workflow**.