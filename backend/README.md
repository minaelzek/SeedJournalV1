# SeedJournal API

## Local setup

```bash
cd infra && docker compose up -d
cd ../backend
cp .env.example .env
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- Health: http://127.0.0.1:8000/health  
- OpenAPI: http://127.0.0.1:8000/openapi.json  
- API v1: http://127.0.0.1:8000/v1

**Dev auth:** `POST /v1/auth/apple` with `identity_token` = `{"sub":"your-id","email":"optional@test.com"}` when `APP_ENV=development`.

**Intelligence (Slice 3):** After `reflection/complete`, background pipeline analyzes entry, extracts memories, embeds (stub vectors in dev), updates tree leaves.

**Reflection (Slice 2):** `POST /v1/entries/{id}/reflection/start`, `.../message`, `.../complete` — max 6 turns, stub LLM in dev.