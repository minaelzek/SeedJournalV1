def test_dev_auth_and_me(client, auth_headers):
    r = client.get("/v1/me", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "pytest@seedjournal.test"
    assert data["ai_depth_enabled"] is True


def test_create_and_list_entry(client, auth_headers):
    r = client.post(
        "/v1/entries",
        headers=auth_headers,
        json={"title": "Morning", "body": "Today I noticed how quiet the room felt."},
    )
    assert r.status_code == 201
    created = r.json()
    assert created["word_count"] >= 8
    assert created["reflection_completed"] is False

    r2 = client.get("/v1/entries", headers=auth_headers)
    assert r2.status_code == 200
    items = r2.json()["items"]
    assert any(i["id"] == created["id"] for i in items)


def test_tree_requires_auth(client):
    r = client.get("/v1/tree")
    assert r.status_code == 401