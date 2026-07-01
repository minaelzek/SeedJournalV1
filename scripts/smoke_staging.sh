#!/usr/bin/env bash
# Usage: ./scripts/smoke_staging.sh https://your-app.fly.dev
set -euo pipefail
BASE="${1:?Pass API base e.g. https://seedjournal-api-staging.fly.dev}"
curl -sf "$BASE/health" | grep -q '"status":"ok"' && echo "health ok"
curl -sf "$BASE/v1/health" | grep -q '"status":"ok"' && echo "v1 health ok"
echo "Smoke passed for $BASE"