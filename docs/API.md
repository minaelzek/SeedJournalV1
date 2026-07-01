# HTTP API (v1)

Base: `/v1` · OpenAPI: `/openapi.json` · Auth: `Authorization: Bearer <access_token>`

## Identity

| Method | Path | Notes |
|--------|------|--------|
| POST | `/auth/apple` | Body: `{ "identity_token": "<apple jwt>" }` |
| GET | `/me` | Current user |
| PATCH | `/me` | `timezone`, `ai_depth_enabled` |
| GET | `/me/export` | JSON export |
| DELETE | `/me` | Delete account + data |

## Journal

| Method | Path | Notes |
|--------|------|--------|
| POST | `/entries` | Optional header `Idempotency-Key` |
| GET | `/entries` | Cursor pagination |
| GET | `/entries/{id}` | Full entry |

## Reflection

| Method | Path | Notes |
|--------|------|--------|
| GET | `/entries/{id}/reflection` | Session state |
| POST | `/entries/{id}/reflection/start` | Begin guided turns |
| POST | `/entries/{id}/reflection/message` | User turn + assistant reply |
| POST | `/entries/{id}/reflection/complete` | Triggers intelligence pipeline |

## Memories & growth

| Method | Path | Notes |
|--------|------|--------|
| GET | `/memories` | List |
| PATCH | `/memories/{id}` | Dismiss |
| POST | `/memories/search` | Semantic search |
| GET | `/tree` | Sakura tree state |

## Insights

| Method | Path | Notes |
|--------|------|--------|
| GET | `/insights/patterns` | Non-diagnostic summaries |
| GET | `/insights/first-mention?q=` | Earliest related memories |

## Health

| Method | Path |
|--------|------|
| GET | `/health` (root) |
| GET | `/v1/health` |