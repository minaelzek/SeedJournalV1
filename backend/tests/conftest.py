import os

import pytest
from fastapi.testclient import TestClient

from app.main import app

# Use dev auth + real DB when DATABASE_URL is reachable (e.g. docker compose up).
os.environ.setdefault("APP_ENV", "development")


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def auth_headers(client: TestClient) -> dict[str, str]:
    """Dev-only Apple auth: identity_token is JSON with sub."""
    try:
        r = client.post(
            "/v1/auth/apple",
            json={"identity_token": '{"sub":"pytest-user-slice1","email":"pytest@seedjournal.test"}'},
        )
    except ConnectionRefusedError:
        pytest.skip("Postgres not reachable — run: cd infra && docker compose up -d")
    if r.status_code != 200:
        pytest.skip(f"Auth failed ({r.status_code}): run alembic upgrade head")
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}