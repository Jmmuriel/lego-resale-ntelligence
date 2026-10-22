import pytest

from backend.security import reset_rate_limits
from src.limits import reset_llm_budget


SECURITY_ENV_VARS = (
    "LRI_DEMO_ALLOW_WRITES",
    "LRI_ENABLE_DOCS",
    "LRI_RATE_LIMIT_PER_MINUTE",
    "LRI_RATE_LIMIT_PER_DAY",
    "LRI_LLM_DAILY_CAP",
    "LRI_LLM_MAX_INPUT_CHARS",
    "LRI_FETCH_TIMEOUT_SECONDS",
    "LRI_FETCH_MAX_BYTES",
    "LRI_MAX_BODY_BYTES",
)


@pytest.fixture(autouse=True)
def secure_defaults(monkeypatch):
    """Run every test with production defaults and fresh in-memory counters.

    A local .env (loaded by src.extract) must not change what the tests see.
    """
    for name in SECURITY_ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    reset_rate_limits()
    reset_llm_budget()
    yield
    reset_rate_limits()
    reset_llm_budget()


@pytest.fixture
def allow_demo_writes(monkeypatch):
    monkeypatch.setenv("LRI_DEMO_ALLOW_WRITES", "1")
