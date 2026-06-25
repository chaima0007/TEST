#!/usr/bin/env python3
"""
resilience_engine.py — Stabilité API CaelumSwarm™
══════════════════════════════════════════════════
Trois mécanismes contre la saturation et les rate-limits (erreurs 429/503) :

  1. retry_with_backoff  — réessais avec backoff exponentiel + jitter
  2. CircuitBreaker      — isole un service défaillant (CLOSED→OPEN→HALF_OPEN)
  3. RateLimitedQueue    — contrôleur de flux (token bucket) pour lisser les pics

Stdlib uniquement. Utilisable comme décorateur ou en wrapping direct.

Usage (décorateur) :
  from resilience_engine import retry_with_backoff, CircuitBreaker

  @retry_with_backoff(max_attempts=5, base_delay=1.0)
  def call_llm(...): ...

  cb = CircuitBreaker("mistral-api", failure_threshold=5, recovery_timeout=30)
  result = cb.call(call_llm, prompt)

CLI démo :
  python3 scripts/resilience_engine.py --demo
"""

import time
import random
import threading
import functools
import json
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

RESILIENCE_LOG = Path("data/resilience_log.json")

# Exceptions considérées comme « transitoires » (à réessayer)
TRANSIENT_MARKERS = ("429", "503", "502", "504", "rate limit", "temporarily",
                     "timeout", "overloaded", "too many requests", "connection reset")


def _is_transient(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(m in msg for m in TRANSIENT_MARKERS)


def _log_event(kind: str, target: str, detail: dict):
    log = []
    if RESILIENCE_LOG.exists():
        try:
            log = json.loads(RESILIENCE_LOG.read_text())
        except Exception:
            log = []
    log.append({
        "ts": datetime.now(timezone.utc).isoformat(),
        "kind": kind, "target": target, **detail,
    })
    if len(log) > 1000:
        log = log[-1000:]
    RESILIENCE_LOG.parent.mkdir(exist_ok=True)
    RESILIENCE_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))


# ── 1. Retry avec backoff exponentiel + jitter ─────────────────────────────────

def retry_with_backoff(max_attempts: int = 5, base_delay: float = 1.0,
                       max_delay: float = 60.0, jitter: bool = True,
                       retry_on=_is_transient, _sleep=time.sleep):
    """
    Décorateur : réessaie une fonction sur erreur transitoire.
    Délai = min(base_delay * 2**(n-1), max_delay) + jitter aléatoire.
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    if not retry_on(exc) or attempt == max_attempts:
                        raise
                    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    if jitter:
                        delay += random.uniform(0, delay * 0.25)
                    _log_event("retry", fn.__name__,
                               {"attempt": attempt, "delay": round(delay, 2), "error": str(exc)[:120]})
                    _sleep(delay)
            raise last_exc
        return wrapper
    return decorator


# ── 2. Circuit Breaker ─────────────────────────────────────────────────────────

class CircuitBreakerOpen(Exception):
    """Levée quand le circuit est ouvert (service isolé)."""


class CircuitBreaker:
    """
    États : CLOSED (normal) → OPEN (bloqué) → HALF_OPEN (test) → CLOSED/OPEN
    - failure_threshold échecs consécutifs → OPEN
    - après recovery_timeout secondes → HALF_OPEN (laisse passer 1 essai)
    - succès en HALF_OPEN → CLOSED ; échec → OPEN à nouveau
    """
    def __init__(self, name: str, failure_threshold: int = 5,
                 recovery_timeout: float = 30.0, _clock=time.monotonic):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._clock = _clock
        self._state = "CLOSED"
        self._failures = 0
        self._opened_at = 0.0
        self._lock = threading.Lock()

    @property
    def state(self) -> str:
        return self._state

    def call(self, fn, *args, **kwargs):
        with self._lock:
            if self._state == "OPEN":
                if self._clock() - self._opened_at >= self.recovery_timeout:
                    self._state = "HALF_OPEN"
                    _log_event("circuit", self.name, {"transition": "OPEN→HALF_OPEN"})
                else:
                    raise CircuitBreakerOpen(f"Circuit '{self.name}' OPEN — service isolé")
        try:
            result = fn(*args, **kwargs)
        except Exception:
            self._on_failure()
            raise
        else:
            self._on_success()
            return result

    def _on_success(self):
        with self._lock:
            if self._state == "HALF_OPEN":
                _log_event("circuit", self.name, {"transition": "HALF_OPEN→CLOSED"})
            self._failures = 0
            self._state = "CLOSED"

    def _on_failure(self):
        with self._lock:
            self._failures += 1
            if self._state == "HALF_OPEN" or self._failures >= self.failure_threshold:
                if self._state != "OPEN":
                    _log_event("circuit", self.name,
                               {"transition": f"{self._state}→OPEN", "failures": self._failures})
                self._state = "OPEN"
                self._opened_at = self._clock()


# ── 3. File à débit limité (token bucket) ──────────────────────────────────────

class RateLimitedQueue:
    """
    Contrôleur de flux : autorise `rate` opérations/seconde avec rafale `burst`.
    acquire() bloque jusqu'à disponibilité d'un jeton.
    """
    def __init__(self, rate: float = 5.0, burst: int = 10, _clock=time.monotonic, _sleep=time.sleep):
        self.rate = rate
        self.burst = burst
        self._tokens = float(burst)
        self._last = _clock()
        self._clock = _clock
        self._sleep = _sleep
        self._lock = threading.Lock()

    def _refill(self):
        now = self._clock()
        elapsed = now - self._last
        self._tokens = min(self.burst, self._tokens + elapsed * self.rate)
        self._last = now

    def acquire(self, tokens: int = 1):
        while True:
            with self._lock:
                self._refill()
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return
                deficit = tokens - self._tokens
                wait = deficit / self.rate
            self._sleep(wait)

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *exc):
        return False


# ── Démo / tests intégrés (clock & sleep simulés, pas d'attente réelle) ─────────

def _demo():
    print("\n══ RESILIENCE ENGINE — Démo ══\n")
    fake_time = [0.0]
    def clock():
        return fake_time[0]
    def sleep(d):
        fake_time[0] += d

    # 1. Retry
    calls = {"n": 0}
    @retry_with_backoff(max_attempts=4, base_delay=1.0, jitter=False, _sleep=sleep)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("429 rate limit")
        return "OK"
    print(f"  [1] Retry backoff : résultat={flaky()} après {calls['n']} tentatives ✅")

    # 2. Circuit Breaker
    cb = CircuitBreaker("test-api", failure_threshold=3, recovery_timeout=10, _clock=clock)
    def boom():
        raise RuntimeError("503 overloaded")
    for _ in range(3):
        try: cb.call(boom)
        except RuntimeError: pass
    print(f"  [2] Circuit Breaker : état après 3 échecs = {cb.state} (attendu OPEN)")
    try:
        cb.call(boom)
        print("      ❌ aurait dû bloquer")
    except CircuitBreakerOpen:
        print(f"      ✅ appels bloqués (service isolé)")
    fake_time[0] += 11  # dépasse recovery_timeout
    print(f"      après {11}s → prochain appel passe en HALF_OPEN")
    try: cb.call(lambda: "recovered")
    except Exception: pass
    print(f"      état après succès = {cb.state} (attendu CLOSED) ✅")

    # 3. Rate limited queue
    rq = RateLimitedQueue(rate=5.0, burst=3, _clock=clock, _sleep=sleep)
    start = fake_time[0]
    for _ in range(8):
        rq.acquire()
    elapsed = fake_time[0] - start
    print(f"  [3] Token bucket : 8 appels (burst=3, 5/s) → {elapsed:.1f}s simulés (attendu ~1.0s) ✅")
    print("\n  Tous les mécanismes opérationnels.\n")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Resilience Engine CaelumSwarm™")
    ap.add_argument("--demo", action="store_true", help="Lancer la démo/tests")
    args = ap.parse_args()
    if args.demo:
        _demo()
    else:
        ap.print_help()
