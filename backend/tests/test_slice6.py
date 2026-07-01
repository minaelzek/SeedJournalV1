def test_export_requires_auth(client):
    r = client.get("/v1/me/export")
    assert r.status_code == 401


def test_insights_patterns_auth(client, auth_headers):
    r = client.get("/v1/insights/patterns", headers=auth_headers)
    assert r.status_code == 200
    assert "narrative" in r.json()


def test_patch_me_ai_depth(client, auth_headers):
    r = client.patch("/v1/me", headers=auth_headers, json={"ai_depth_enabled": False})
    assert r.status_code == 200
    assert r.json()["ai_depth_enabled"] is False


def test_entry_idempotency(client, auth_headers):
    headers = {**auth_headers, "Idempotency-Key": "test-key-1"}
    body = {"body": "Same entry"}
    r1 = client.post("/v1/entries", headers=headers, json=body)
    r2 = client.post("/v1/entries", headers=headers, json=body)
    assert r1.status_code == 201 and r2.status_code == 201
    assert r1.json()["id"] == r2.json()["id"]


def test_delete_account(client, auth_headers_ephemeral):
    r = client.delete("/v1/me", headers=auth_headers_ephemeral)
    assert r.status_code == 204