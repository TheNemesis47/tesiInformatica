"""Test per il RateLimiter."""

from __future__ import annotations

import time

import pytest

from vision_caption.core.services.rate_limiter import RateLimiter


class TestRateLimiter:
    """Test per il rate limiter della pipeline."""

    def test_first_call_always_allowed(self) -> None:
        """Il primo can_proceed() è sempre True (nessun evento precedente)."""
        limiter = RateLimiter(min_interval_sec=3.0)
        assert limiter.can_proceed() is True

    def test_blocked_after_record(self) -> None:
        """can_proceed() è False subito dopo record()."""
        limiter = RateLimiter(min_interval_sec=3.0)
        limiter.record()
        assert limiter.can_proceed() is False

    def test_allowed_after_interval(self) -> None:
        """can_proceed() diventa True dopo min_interval_sec."""
        limiter = RateLimiter(min_interval_sec=0.05)  # 50ms per test veloce
        limiter.record()
        assert limiter.can_proceed() is False
        time.sleep(0.06)
        assert limiter.can_proceed() is True

    def test_seconds_until_next_decreases(self) -> None:
        """seconds_until_next diminuisce col passare del tempo."""
        limiter = RateLimiter(min_interval_sec=1.0)
        limiter.record()
        t1 = limiter.seconds_until_next
        time.sleep(0.05)
        t2 = limiter.seconds_until_next
        assert t2 < t1

    def test_seconds_until_next_zero_when_allowed(self) -> None:
        """seconds_until_next è 0.0 quando si può procedere."""
        limiter = RateLimiter(min_interval_sec=0.0)
        assert limiter.seconds_until_next == 0.0

    def test_zero_interval_always_allows(self) -> None:
        """Con min_interval_sec=0.0, can_proceed() è sempre True."""
        limiter = RateLimiter(min_interval_sec=0.0)
        limiter.record()
        assert limiter.can_proceed() is True
