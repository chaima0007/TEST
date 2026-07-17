#!/usr/bin/env python3
"""
observability.py — Observabilité & Traçabilité CaelumSwarm™
════════════════════════════════════════════════════════════
Journalisation structurée (JSON), tracing distribué léger et métriques,
pour suivre le comportement de la flotte d'agents en temps réel et
diagnostiquer les échecs silencieux.

  - StructuredLogger : logs JSON (trace_id, span_id, agent, niveau, durée)
  - Tracer / Span    : tracing distribué (chaîne de raisonnement des agents)
  - MetricsCollector : compteurs, jauges, histogrammes (latence p50/p95/p99)

Stdlib uniquement. Logs append-only en JSONL pour ingestion facile.

Usage :
  from observability import get_logger, Tracer, metrics

  log = get_logger("orchestrator")
  log.info("agent lancé", agent="seal-42", wave=499)

  tracer = Tracer("wave-pipeline")
  with tracer.span("run_engine", agent="engine-7") as span:
      ...
      span.tag("result", "ok")

  metrics.incr("api_calls"); metrics.observe("latency_ms", 142.0)

CLI :
  python3 scripts/observability.py --demo
  python3 scripts/observability.py --tail 20
  python3 scripts/observability.py --metrics
"""

import os
import json
import time
import random
import threading
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

LOG_FILE     = Path("data/observability/events.jsonl")
METRICS_FILE = Path("data/observability/metrics.json")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

LEVELS = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40, "CRITICAL": 50}
_LOCK = threading.Lock()


def _new_id(n: int = 8) -> str:
    return "".join(random.choice("0123456789abcdef") for _ in range(n))


def _write_event(event: dict):
    line = json.dumps(event, ensure_ascii=False)
    with _LOCK:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")


# ── Logger structuré ───────────────────────────────────────────────────────────

class StructuredLogger:
    def __init__(self, component: str, min_level: str = "DEBUG"):
        self.component = component
        self.min_level = LEVELS.get(min_level, 10)

    def _emit(self, level: str, msg: str, **fields):
        if LEVELS.get(level, 0) < self.min_level:
            return
        event = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "component": self.component,
            "msg": msg,
        }
        # trace context si présent dans les fields
        event.update(fields)
        _write_event(event)
        if level in ("ERROR", "CRITICAL"):
            metrics.incr(f"log.{level.lower()}")

    def debug(self, msg, **f): self._emit("DEBUG", msg, **f)
    def info(self, msg, **f):  self._emit("INFO", msg, **f)
    def warn(self, msg, **f):  self._emit("WARN", msg, **f)
    def error(self, msg, **f): self._emit("ERROR", msg, **f)
    def critical(self, msg, **f): self._emit("CRITICAL", msg, **f)


_loggers = {}
def get_logger(component: str) -> StructuredLogger:
    if component not in _loggers:
        _loggers[component] = StructuredLogger(component)
    return _loggers[component]


# ── Tracing distribué ──────────────────────────────────────────────────────────

class Span:
    def __init__(self, tracer, name: str, parent_id: str | None, **tags):
        self.tracer = tracer
        self.name = name
        self.span_id = _new_id()
        self.parent_id = parent_id
        self.trace_id = tracer.trace_id
        self.tags = dict(tags)
        self._start = None

    def tag(self, key: str, value):
        self.tags[key] = value
        return self

    def __enter__(self):
        self._start = time.monotonic()
        self.tracer._stack.append(self.span_id)
        return self

    def __exit__(self, exc_type, exc, tb):
        duration_ms = round((time.monotonic() - self._start) * 1000, 3)
        if self.tracer._stack and self.tracer._stack[-1] == self.span_id:
            self.tracer._stack.pop()
        status = "error" if exc_type else "ok"
        _write_event({
            "ts": datetime.now(timezone.utc).isoformat(),
            "type": "span",
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "duration_ms": duration_ms,
            "status": status,
            "tags": self.tags,
            **({"error": str(exc)[:200]} if exc else {}),
        })
        metrics.observe(f"span.{self.name}.ms", duration_ms)
        return False  # ne supprime pas l'exception


class Tracer:
    def __init__(self, name: str, trace_id: str | None = None):
        self.name = name
        self.trace_id = trace_id or _new_id(16)
        self._stack = []

    def span(self, name: str, **tags) -> Span:
        parent = self._stack[-1] if self._stack else None
        return Span(self, name, parent, **tags)


# ── Métriques ──────────────────────────────────────────────────────────────────

class MetricsCollector:
    def __init__(self):
        self._counters = defaultdict(float)
        self._gauges = {}
        self._histograms = defaultdict(list)
        self._lock = threading.Lock()

    def incr(self, name: str, value: float = 1.0):
        with self._lock:
            self._counters[name] += value

    def gauge(self, name: str, value: float):
        with self._lock:
            self._gauges[name] = value

    def observe(self, name: str, value: float):
        with self._lock:
            h = self._histograms[name]
            h.append(value)
            if len(h) > 10_000:
                del h[:5_000]

    @staticmethod
    def _percentile(sorted_vals, p):
        if not sorted_vals:
            return 0.0
        k = (len(sorted_vals) - 1) * (p / 100)
        f = int(k)
        c = min(f + 1, len(sorted_vals) - 1)
        return round(sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f), 3)

    def snapshot(self) -> dict:
        with self._lock:
            hist = {}
            for name, vals in self._histograms.items():
                s = sorted(vals)
                hist[name] = {
                    "count": len(s),
                    "p50": self._percentile(s, 50),
                    "p95": self._percentile(s, 95),
                    "p99": self._percentile(s, 99),
                    "max": round(max(s), 3) if s else 0.0,
                }
            return {
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histograms": hist,
            }

    def flush(self):
        snap = self.snapshot()
        snap["ts"] = datetime.now(timezone.utc).isoformat()
        METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
        METRICS_FILE.write_text(json.dumps(snap, indent=2, ensure_ascii=False))
        return snap


metrics = MetricsCollector()


# ── Démo / tail / rapport ──────────────────────────────────────────────────────

def _demo():
    print("\n══ OBSERVABILITY — Démo ══\n")
    log = get_logger("orchestrator")
    log.info("démarrage pipeline", wave=499, agents=3)
    log.warn("rate-limit proche", remaining=12)

    tracer = Tracer("wave-499-pipeline")
    with tracer.span("run_wave", wave=499) as root:
        for i in range(3):
            with tracer.span("run_engine", engine=f"engine-{i}") as s:
                time.sleep(0.001 * (i + 1))
                s.tag("avg_composite", 61.03)
                metrics.incr("engines.run")
                metrics.observe("engine.latency_ms", (i + 1) * 12.5)
        root.tag("status", "complete")

    log.error("exemple d'erreur capturée", agent="engine-x", code=502)

    snap = metrics.flush()
    print(f"  [1] Logs JSONL écrits → {LOG_FILE}")
    print(f"  [2] Trace : trace_id={tracer.trace_id} (4 spans)")
    print(f"  [3] Compteurs : {snap['counters']}")
    if "engine.latency_ms" in snap["histograms"]:
        h = snap["histograms"]["engine.latency_ms"]
        print(f"  [4] Latence engine : p50={h['p50']}ms p95={h['p95']}ms p99={h['p99']}ms max={h['max']}ms")
    print("\n  Observabilité opérationnelle (tracing + logs + métriques).\n")


def _tail(n: int):
    if not LOG_FILE.exists():
        print("Aucun événement.")
        return
    lines = LOG_FILE.read_text().strip().split("\n")
    for line in lines[-n:]:
        try:
            e = json.loads(line)
            if e.get("type") == "span":
                print(f"  ⏱  {e['name']:<16} {e['duration_ms']:>8}ms  [{e['status']}]  trace={e['trace_id'][:8]}")
            else:
                print(f"  {e.get('level','?'):<8} [{e.get('component','?')}] {e.get('msg','')}")
        except Exception:
            pass


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Observability CaelumSwarm™")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--tail", type=int, metavar="N", help="Afficher les N derniers événements")
    ap.add_argument("--metrics", action="store_true", help="Afficher le snapshot métriques")
    args = ap.parse_args()
    if args.demo:
        _demo()
    elif args.tail:
        _tail(args.tail)
    elif args.metrics:
        print(json.dumps(metrics.flush(), indent=2, ensure_ascii=False))
    else:
        ap.print_help()
