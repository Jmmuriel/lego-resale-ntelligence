"""Small in-process usage limits shared by the FastAPI backend and the Streamlit app.

The public demo runs a single process, so counters kept in memory are enough: no
Redis. They reset when the process restarts.
"""

import logging
import math
import os
import threading
import time
from collections.abc import Callable, Iterable


log = logging.getLogger(__name__)

DAY_SECONDS = 86_400
DEFAULT_LLM_DAILY_CAP = 100
DEFAULT_LLM_MAX_INPUT_CHARS = 4_000
MAX_TRACKED_BUCKETS = 50_000

_TRUE_VALUES = {"1", "true", "yes", "on"}


def env_flag(name: str) -> bool:
    """Return True only when the variable is explicitly set to 1/true/yes/on."""
    return os.getenv(name, "").strip().lower() in _TRUE_VALUES


def env_int(name: str, default: int, minimum: int = 0) -> int:
    """Read an integer setting, falling back to the default when unset or invalid."""
    raw_value = os.getenv(name, "").strip()
    if not raw_value:
        return default

    try:
        value = int(raw_value)
    except ValueError:
        log.warning("Ignoring invalid %s=%r; using %s", name, raw_value, default)
        return default

    if value < minimum:
        log.warning("Ignoring %s=%s below minimum %s; using %s", name, value, minimum, default)
        return default

    return value


class FixedWindowLimiter:
    """Thread-safe fixed-window counters kept in process memory."""

    def __init__(self, clock: Callable[[], float] = time.time) -> None:
        self._clock = clock
        self._lock = threading.Lock()
        self._counts: dict[tuple[str, int, int], int] = {}
        self._last_prune_minute = -1

    def hit(self, key: str, limits: Iterable[tuple[int, int]]) -> int | None:
        """Count one request for key.

        `limits` holds (max_requests, period_seconds) pairs. Returns None when the
        request is allowed, or the seconds to wait when any window is already full
        (the request is then not counted).
        """
        now = self._clock()
        with self._lock:
            self._prune(now)
            buckets = []
            for limit, period in limits:
                window = int(now // period)
                bucket = (key, period, window)
                if self._counts.get(bucket, 0) >= limit:
                    return max(1, math.ceil((window + 1) * period - now))
                buckets.append(bucket)

            for bucket in buckets:
                self._counts[bucket] = self._counts.get(bucket, 0) + 1

        return None

    def reset(self) -> None:
        with self._lock:
            self._counts.clear()

    def _prune(self, now: float) -> None:
        minute = int(now // 60)
        if minute != self._last_prune_minute:
            self._last_prune_minute = minute
            expired = [bucket for bucket in self._counts if bucket[2] < int(now // bucket[1])]
            for bucket in expired:
                del self._counts[bucket]

        if len(self._counts) > MAX_TRACKED_BUCKETS:
            # Bound memory under address rotation. Per-client limits start over;
            # the global LLM cap is a separate limiter and still applies.
            log.warning("Rate limiter tracked too many clients; clearing counters")
            self._counts.clear()


class LLMBudgetExceeded(RuntimeError):
    """The process-wide daily cap on paid LLM calls has been reached."""

    def __init__(self, retry_after: int) -> None:
        super().__init__("Se ha alcanzado el límite diario de análisis con IA.")
        self.retry_after = retry_after


_llm_limiter = FixedWindowLimiter()


def reserve_llm_call() -> None:
    """Count one paid LLM call against LRI_LLM_DAILY_CAP (per UTC day, per process)."""
    daily_cap = env_int("LRI_LLM_DAILY_CAP", DEFAULT_LLM_DAILY_CAP)
    retry_after = _llm_limiter.hit("llm", [(daily_cap, DAY_SECONDS)])
    if retry_after is not None:
        log.warning("Daily LLM cap of %s calls reached", daily_cap)
        raise LLMBudgetExceeded(retry_after)


def reset_llm_budget() -> None:
    _llm_limiter.reset()


def truncate_llm_input(text: str) -> str:
    """Cap the text sent to the LLM at LRI_LLM_MAX_INPUT_CHARS characters."""
    max_chars = env_int("LRI_LLM_MAX_INPUT_CHARS", DEFAULT_LLM_MAX_INPUT_CHARS, minimum=1)
    return text[:max_chars]
