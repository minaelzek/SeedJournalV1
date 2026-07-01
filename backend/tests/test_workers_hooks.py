from app.workers.hooks import pipeline_runs_inline


def test_pipeline_runs_inline_false_by_default(monkeypatch):
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    assert pipeline_runs_inline() is False


def test_pipeline_runs_inline_true_under_pytest(monkeypatch):
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "tests/test_foo.py::test_bar")
    assert pipeline_runs_inline() is True