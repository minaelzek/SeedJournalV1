# ADR-004: Inline intelligence pipeline under pytest

**Status:** Accepted

## Context

`reflection/complete` enqueues memory extraction via FastAPI `BackgroundTasks`. Starlette's `TestClient` does not reliably await background work before assertions, causing flaky `test_slice3` failures in CI.

## Decision

When `PYTEST_CURRENT_TEST` is set, run `enqueue_entry_pipeline` **await** inline in the complete handler. Production behavior unchanged (background task).

## Consequences

- CI and local pytest are deterministic for memory/tree tests.
- Must not set `PYTEST_CURRENT_TEST` in production deploys (pytest sets it automatically).
- Single code path in `reflection` router gated by `app.workers.hooks.pipeline_runs_inline()`.