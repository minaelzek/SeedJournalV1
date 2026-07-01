import os


def pipeline_runs_inline() -> bool:
    """True during pytest so TestClient sees completed intelligence pipeline."""
    return bool(os.getenv("PYTEST_CURRENT_TEST"))