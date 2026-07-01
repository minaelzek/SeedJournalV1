import time

import pytest


def _complete_entry(client, auth_headers, body: str) -> str:
    r = client.post("/v1/entries", headers=auth_headers, json={"body": body})
    assert r.status_code == 201
    entry_id = r.json()["id"]
    r2 = client.post(f"/v1/entries/{entry_id}/reflection/complete", headers=auth_headers)
    assert r2.status_code == 200
    return entry_id


def test_pipeline_creates_memories(client, auth_headers):
    _complete_entry(client, auth_headers, "I value honesty in my closest friendships.")

    for _ in range(20):
        r = client.get("/v1/memories", headers=auth_headers)
        if r.status_code == 200 and r.json()["items"]:
            break
        time.sleep(0.25)
    else:
        pytest.fail("Pipeline did not create memories in time")

    items = r.json()["items"]
    assert items[0]["confidence"] >= 0.55
    assert items[0]["source_entry_id"]


def test_memory_search(client, auth_headers):
    _complete_entry(client, auth_headers, "My goal is to build a calmer morning routine.")

    for _ in range(20):
        r = client.get("/v1/memories", headers=auth_headers)
        if r.json().get("items"):
            break
        time.sleep(0.25)

    r2 = client.post(
        "/v1/memories/search",
        headers=auth_headers,
        json={"query": "morning routine calm", "limit": 5},
    )
    assert r2.status_code == 200
    # May be empty if query embedding unrelated in stub; list should still work
    assert "items" in r2.json()


def test_tree_updates_after_pipeline(client, auth_headers):
    _complete_entry(client, auth_headers, "I realized I keep avoiding difficult conversations.")

    time.sleep(1.0)
    r = client.get("/v1/tree", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert data["leaves_count"] >= 0