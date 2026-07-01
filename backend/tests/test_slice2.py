def test_reflection_start_and_complete(client, auth_headers):
    r = client.post(
        "/v1/entries",
        headers=auth_headers,
        json={"body": "I keep wondering what home means to me now."},
    )
    assert r.status_code == 201
    entry_id = r.json()["id"]

    r2 = client.post(f"/v1/entries/{entry_id}/reflection/start", headers=auth_headers)
    assert r2.status_code == 200
    data = r2.json()
    assert data["turn_count"] >= 1
    assert data["assistant_message"] is not None

    r3 = client.post(
        f"/v1/entries/{entry_id}/reflection/message",
        headers=auth_headers,
        json={"message": "It feels like belonging, but I'm not sure where."},
    )
    assert r3.status_code == 200
    assert r3.json()["user_turn"]["role"] == "user"

    r4 = client.post(f"/v1/entries/{entry_id}/reflection/complete", headers=auth_headers)
    assert r4.status_code == 200
    assert r4.json()["reflection_completed"] is True

    r5 = client.get(f"/v1/entries/{entry_id}", headers=auth_headers)
    assert r5.json()["reflection_completed"] is True


def test_complete_without_reflection(client, auth_headers):
    r = client.post("/v1/entries", headers=auth_headers, json={"body": "Short note."})
    entry_id = r.json()["id"]
    r2 = client.post(f"/v1/entries/{entry_id}/reflection/complete", headers=auth_headers)
    assert r2.status_code == 200
    assert r2.json()["reflection_completed"] is True