def test_root_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_v1_health(client):
    r = client.get("/v1/health")
    assert r.status_code == 200


def test_v1_tree_requires_auth(client):
    r = client.get("/v1/tree")
    assert r.status_code == 401