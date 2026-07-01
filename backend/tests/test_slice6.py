def test_export_requires_auth(client):
    r = client.get("/v1/me/export")
    assert r.status_code == 401


def test_insights_patterns_auth(client, auth_headers):
    r = client.get("/v1/insights/patterns", headers=auth_headers)
    assert r.status_code == 200
    assert "narrative" in r.json()


def test_delete_account(client, auth_headers):
    r = client.delete("/v1/me", headers=auth_headers)
    assert r.status_code == 204