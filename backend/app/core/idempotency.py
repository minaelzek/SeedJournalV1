from datetime import datetime, timedelta, timezone

_idempotency_cache: dict[str, tuple[datetime, str]] = {}
TTL = timedelta(hours=24)


def get_cached_response(key: str) -> str | None:
    row = _idempotency_cache.get(key)
    if row is None:
        return None
    created, body = row
    if datetime.now(timezone.utc) - created > TTL:
        del _idempotency_cache[key]
        return None
    return body


def store_cached_response(key: str, body: str) -> None:
    _idempotency_cache[key] = (datetime.now(timezone.utc), body)