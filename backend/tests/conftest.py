import os

import pytest
from fastapi.testclient import TestClient

from app.main import app

# Use dev auth + real DB when DATABASE_URL is reachable (e.g. docker compose up).
os.environ.setdefault("APP_ENV", "development")


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _dev_auth_headers(client: TestClient, sub: str, email: str) -> dict[str, str]:
    try:
        r = client.post(
            "/v1/auth/apple",
            json={"identity_token": f'{{"sub":"{sub}","email":"{email}"}}'},
        )
    except ConnectionRefusedError:
        pytest.skip("Postgres not reachable — run: cd infra && docker compose up -d")
    if r.status_code != 200:
        pytest.skip(f"Auth failed ({r.status_code}): run alembic upgrade head")
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers(client: TestClient) -> dict[str, str]:
    return _dev_auth_headers(client, "pytest-user-slice1", "pytest@seedjournal.test")


@pytest.fixture
def auth_headers_ephemeral(client: TestClient) -> dict[str, str]:
    """Fresh user for tests that delete the account."""
    import uuid

    sub = f"pytest-ephemeral-{uuid.uuid4().hex[:12]}"
    return _dev_auth_headers(client, sub, f"{sub}@seedjournal.test")