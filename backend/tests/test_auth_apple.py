def test_apple_auth_rejects_invalid_token(client):
    r = client.post("/v1/auth/apple", json={"identity_token": "not-a-real-jwt"})
    assert r.status_code == 401


def test_apple_auth_rejects_dev_json_in_production_mode(client, monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    from app.core.config import get_settings

    get_settings.cache_clear()
    r = client.post(
        "/v1/auth/apple",
        json={"identity_token": '{"sub":"x","email":"y@test.com"}'},
    )
    assert r.status_code == 401
    get_settings.cache_clear()