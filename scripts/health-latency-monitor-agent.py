#!/usr/bin/env python3
"""Health & Latency Monitor Agent — CaelumSwarm™ | CSDDD Compliance Platform
Vérifie en temps réel la santé et la latence de tous les endpoints API CaelumSwarm.
"""

import json
import time
import os
import sys
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import urllib.request
import urllib.error

AGENT_NAME = "HealthLatencyMonitorAgent"
VERSION = "1.0.0"
WAVE = "MONITOR-01"

# Configuration
BASE_URL = os.environ.get("CAELUM_BASE_URL", "http://localhost:3000")
LATENCY_WARNING_MS = 1000
LATENCY_CRITICAL_MS = 2000
TIMEOUT_S = 10
REPEAT_COUNT = 3  # Nombre de requêtes par endpoint pour calculer avg

# Couleurs ANSI pour terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def discover_api_routes(project_root: str) -> list[str]:
    """Découvre automatiquement tous les slugs API dans app/api/"""
    api_dir = Path(project_root) / "app" / "api"
    slugs = []
    if api_dir.exists():
        for item in sorted(api_dir.iterdir()):
            if item.is_dir() and (item / "route.ts").exists():
                slugs.append(item.name)
    return slugs


def check_endpoint(slug: str, base_url: str, repeat: int = 3) -> dict:
    """Teste un endpoint API et mesure sa latence."""
    url = f"{base_url}/api/{slug}"
    latencies = []
    last_error = None
    last_data = None
    status = "OK"

    for _ in range(repeat):
        start = time.perf_counter()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": f"CaelumMonitor/{VERSION}"})
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as response:
                body = response.read().decode("utf-8")
                elapsed_ms = (time.perf_counter() - start) * 1000
                latencies.append(elapsed_ms)
                try:
                    last_data = json.loads(body)
                except json.JSONDecodeError:
                    last_data = None
                    status = "WARNING"
                    last_error = "Invalid JSON response"
        except urllib.error.HTTPError as e:
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)
            if e.code == 502:
                status = "WARNING"
                last_error = f"502 Bad Gateway (upstream not configured)"
            else:
                status = "CRITICAL"
                last_error = f"HTTP {e.code}: {e.reason}"
        except urllib.error.URLError as e:
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)
            status = "CRITICAL"
            last_error = f"Connection error: {e.reason}"
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)
            status = "CRITICAL"
            last_error = str(e)
        time.sleep(0.1)

    avg_latency = statistics.mean(latencies) if latencies else 0

    # Vérification de la structure de la réponse
    integrity_ok = False
    if last_data is not None:
        payload = last_data.get("payload", last_data)
        if isinstance(payload, dict):
            has_engine = "engine" in payload or "agent" in payload or "ENGINE" in str(payload)
            integrity_ok = True

    # Évaluation de la latence
    if status == "OK":
        if avg_latency > LATENCY_CRITICAL_MS:
            status = "CRITICAL"
            last_error = f"Latency {avg_latency:.0f}ms exceeds critical threshold {LATENCY_CRITICAL_MS}ms"
        elif avg_latency > LATENCY_WARNING_MS:
            status = "WARNING"
            last_error = f"Latency {avg_latency:.0f}ms exceeds warning threshold {LATENCY_WARNING_MS}ms"

    return {
        "slug": slug,
        "url": url,
        "status": status,
        "avg_latency_ms": round(avg_latency, 2),
        "min_latency_ms": round(min(latencies), 2) if latencies else 0,
        "max_latency_ms": round(max(latencies), 2) if latencies else 0,
        "integrity_ok": integrity_ok,
        "error": last_error,
        "tested_at": datetime.now(timezone.utc).isoformat(),
    }


def run_monitor(project_root: str = "/home/user/TEST", base_url: Optional[str] = None) -> dict:
    """Lance le monitoring complet de tous les endpoints."""
    if base_url is None:
        base_url = BASE_URL

    print(f"\n{BOLD}{CYAN}{'='*70}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ Health & Latency Monitor Agent v{VERSION}{RESET}")
    print(f"{CYAN}  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}{RESET}")
    print(f"{CYAN}  Target: {base_url}{RESET}")
    print(f"{BOLD}{CYAN}{'='*70}{RESET}\n")

    # Découverte des routes
    slugs = discover_api_routes(project_root)
    print(f"{BLUE}Découverte: {len(slugs)} endpoints API trouvés{RESET}\n")

    results = []
    ok_count = warning_count = critical_count = 0
    all_latencies = []

    for i, slug in enumerate(slugs, 1):
        print(f"  [{i:3d}/{len(slugs)}] Testing: {slug:<55}", end="", flush=True)
        result = check_endpoint(slug, base_url, repeat=REPEAT_COUNT)
        results.append(result)

        latency = result["avg_latency_ms"]
        all_latencies.append(latency)

        if result["status"] == "OK":
            ok_count += 1
            status_str = f"{GREEN}✓ OK{RESET}"
        elif result["status"] == "WARNING":
            warning_count += 1
            status_str = f"{YELLOW}⚠ WARN{RESET}"
        else:
            critical_count += 1
            status_str = f"{RED}✗ CRIT{RESET}"

        latency_color = GREEN if latency < LATENCY_WARNING_MS else (YELLOW if latency < LATENCY_CRITICAL_MS else RED)
        print(f"{status_str} {latency_color}{latency:7.1f}ms{RESET}", end="")

        if result["error"]:
            print(f"  {YELLOW}({result['error'][:50]}){RESET}", end="")
        print()

    # Statistiques globales
    total = len(results)
    uptime_pct = (ok_count + warning_count) / total * 100 if total > 0 else 0
    avg_lat = statistics.mean(all_latencies) if all_latencies else 0
    p95 = sorted(all_latencies)[int(len(all_latencies) * 0.95)] if all_latencies else 0
    p99 = sorted(all_latencies)[int(len(all_latencies) * 0.99)] if all_latencies else 0

    summary = {
        "agent": AGENT_NAME,
        "version": VERSION,
        "wave": WAVE,
        "base_url": base_url,
        "total_endpoints": total,
        "ok": ok_count,
        "warning": warning_count,
        "critical": critical_count,
        "uptime_pct": round(uptime_pct, 2),
        "avg_latency_ms": round(avg_lat, 2),
        "p95_latency_ms": round(p95, 2),
        "p99_latency_ms": round(p99, 2),
        "results": results,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    # Rapport final
    print(f"\n{BOLD}{CYAN}{'='*70}{RESET}")
    print(f"{BOLD}  RAPPORT DE SANTÉ CAELUMSWARM{RESET}")
    print(f"{BOLD}{CYAN}{'='*70}{RESET}")
    print(f"  Total endpoints : {total}")
    print(f"  {GREEN}✓ OK       : {ok_count}{RESET}")
    print(f"  {YELLOW}⚠ WARNING  : {warning_count}{RESET}")
    print(f"  {RED}✗ CRITICAL : {critical_count}{RESET}")
    print(f"  Uptime        : {uptime_pct:.1f}%")
    print(f"  Avg latency   : {avg_lat:.1f}ms")
    print(f"  P95 latency   : {p95:.1f}ms")
    print(f"  P99 latency   : {p99:.1f}ms")

    overall = GREEN + "✓ HEALTHY" if critical_count == 0 and warning_count < total * 0.2 else \
              YELLOW + "⚠ DEGRADED" if critical_count == 0 else RED + "✗ UNHEALTHY"
    print(f"\n  Statut global : {BOLD}{overall}{RESET}\n")

    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CaelumSwarm Health & Latency Monitor")
    parser.add_argument("--url", default=BASE_URL, help="Base URL de l'application (défaut: http://localhost:3000)")
    parser.add_argument("--root", default="/home/user/TEST", help="Racine du projet Next.js")
    parser.add_argument("--json", action="store_true", help="Sortie JSON uniquement")
    parser.add_argument("--repeat", type=int, default=3, help="Nombre de requêtes par endpoint (défaut: 3)")
    args = parser.parse_args()

    REPEAT_COUNT = args.repeat
    result = run_monitor(project_root=args.root, base_url=args.url)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))

    sys.exit(0 if result["critical"] == 0 else 1)
