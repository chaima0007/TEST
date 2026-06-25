#!/usr/bin/env python3
"""Performance Profiler Agent — CaelumSwarm™ Dev Support
Profile les engines Python (temps d'exécution), analyse les patterns de performance
Next.js (SSR vs SSG, revalidation, cache), et identifie les goulots d'étranglement.
"""
import time
import json
import importlib.util
import sys
import re
from pathlib import Path
from datetime import datetime, timezone
from statistics import mean, stdev

AGENT_NAME = "PerformanceProfilerAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

PERF_THRESHOLDS = {
    "engine_ms": {"ok": 50, "warning": 200, "critical": 1000},
    "route_revalidate": {"ok": 30, "warning": 60, "critical": 300},
}


def profile_engine(engine_path: Path, runs: int = 5) -> dict:
    """Profile l'exécution d'un engine Python."""
    timings = []
    error = None

    try:
        spec = importlib.util.spec_from_file_location(engine_path.stem, str(engine_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "run_engine"):
            return {"engine": engine_path.stem, "error": "run_engine() introuvable", "timings_ms": []}

        for _ in range(runs):
            start = time.perf_counter()
            module.run_engine()
            elapsed_ms = (time.perf_counter() - start) * 1000
            timings.append(round(elapsed_ms, 3))

    except Exception as e:
        error = str(e)

    if not timings:
        return {"engine": engine_path.stem, "error": error or "Aucun timing", "timings_ms": []}

    avg_ms = round(mean(timings), 3)
    std_ms = round(stdev(timings), 3) if len(timings) > 1 else 0

    threshold = PERF_THRESHOLDS["engine_ms"]
    status = "OK" if avg_ms < threshold["ok"] else "WARNING" if avg_ms < threshold["warning"] else "CRITICAL"

    return {
        "engine": engine_path.stem,
        "runs": runs,
        "avg_ms": avg_ms,
        "min_ms": round(min(timings), 3),
        "max_ms": round(max(timings), 3),
        "std_ms": std_ms,
        "status": status,
        "error": error,
    }


def analyze_route_performance(root: Path) -> list[dict]:
    """Analyse les patterns de performance des routes API."""
    results = []
    for route_path in sorted((root / "app" / "api").rglob("route.ts")):
        source = route_path.read_text(encoding="utf-8", errors="ignore")
        slug = route_path.parent.name

        issues = []
        score = 100

        # Vérifier revalidate
        rev_match = re.search(r'revalidate\s*=\s*(\d+)', source)
        if not rev_match:
            issues.append({"type": "MISSING_REVALIDATE", "severity": "HIGH",
                           "message": "revalidate absent — pas de cache ISR"})
            score -= 30
        else:
            rev_val = int(rev_match.group(1))
            if rev_val > 300:
                issues.append({"type": "HIGH_REVALIDATE", "severity": "INFO",
                               "message": f"revalidate={rev_val}s — cache très long (recommandé: 30s)"})
                score -= 5
            elif rev_val < 10:
                issues.append({"type": "LOW_REVALIDATE", "severity": "WARNING",
                               "message": f"revalidate={rev_val}s — cache très court (surcharge serveur)"})
                score -= 15

        # Vérifier next: { revalidate } sur le fetch
        if "next: { revalidate" not in source and "next:{revalidate" not in source:
            issues.append({"type": "MISSING_FETCH_CACHE", "severity": "MEDIUM",
                           "message": "Cache fetch next.revalidate absent sur l'appel upstream"})
            score -= 20

        # Vérifier pas de await dans un loop (N+1 problem)
        loop_await = re.findall(r'for\s*\([^)]+\)[^{]*\{[^}]*await\s+fetch', source, re.DOTALL)
        if loop_await:
            issues.append({"type": "N_PLUS_1_FETCH", "severity": "HIGH",
                           "message": "await fetch() dans une boucle — N+1 requêtes"})
            score -= 40

        results.append({
            "slug": slug,
            "score": max(0, score),
            "issues": issues,
        })

    return sorted(results, key=lambda x: x["score"])


def generate_optimization_report(engine_profiles: list[dict], route_analysis: list[dict]) -> list[str]:
    recs = []

    slow_engines = [e for e in engine_profiles if e.get("status") in ("WARNING", "CRITICAL")]
    if slow_engines:
        recs.append(f"🐌 {len(slow_engines)} engines lents (>{PERF_THRESHOLDS['engine_ms']['ok']}ms) — envisager numpy ou caching")

    missing_cache = [r for r in route_analysis if any(i["type"] == "MISSING_REVALIDATE" for i in r["issues"])]
    if missing_cache:
        recs.append(f"📦 {len(missing_cache)} routes sans cache ISR — ajouter 'export const revalidate = 30'")

    n_plus_1 = [r for r in route_analysis if any(i["type"] == "N_PLUS_1_FETCH" for i in r["issues"])]
    if n_plus_1:
        recs.append(f"🔄 N+1 détecté dans {len(n_plus_1)} routes — utiliser Promise.all() pour les requêtes parallèles")

    recs.append("⚡ Activer 'Edge Runtime' pour les routes simples: export const runtime = 'edge'")
    recs.append("🗄️ Envisager Redis/Upstash pour cacher les résultats d'engines Python")
    recs.append("📊 Utiliser Vercel Analytics ou Netlify Analytics pour les métriques réelles")

    return recs


def run_profiler(project_root: str = "/home/user/TEST", engine_limit: int = 10) -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}{'='*65}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ Performance Profiler Agent v{VERSION}{RESET}")
    print(f"{BOLD}{CYAN}{'='*65}{RESET}\n")

    # Profile engines (limité pour ne pas être trop lent)
    engine_files = sorted((root / "swarm" / "intelligence").glob("*_engine.py"))[:engine_limit]
    print(f"{BOLD}Profiling {len(engine_files)} engines Python (3 runs chacun)...{RESET}\n")

    engine_profiles = []
    for engine_path in engine_files:
        result = profile_engine(engine_path, runs=3)
        engine_profiles.append(result)

        if result.get("error"):
            print(f"  {YELLOW}ERR{RESET}  {engine_path.stem}: {result['error'][:50]}")
        else:
            color = GREEN if result["status"] == "OK" else YELLOW if result["status"] == "WARNING" else RED
            print(f"  {color}{result['avg_ms']:7.2f}ms{RESET}  {engine_path.stem}")

    # Analyse routes
    print(f"\n{BOLD}Analyse performance routes API...{RESET}\n")
    route_analysis = analyze_route_performance(root)

    problem_routes = [r for r in route_analysis if r["score"] < 80]
    if problem_routes:
        print(f"  {YELLOW}Routes avec problèmes de performance:{RESET}")
        for r in problem_routes[:5]:
            print(f"    {r['score']:3d}/100  {r['slug']}")
            for issue in r["issues"][:2]:
                print(f"      {YELLOW}⚠{RESET} {issue['message']}")
    else:
        print(f"  {GREEN}✓ Toutes les routes bien configurées{RESET}")

    # Rapport
    recs = generate_optimization_report(engine_profiles, route_analysis)
    print(f"\n{BOLD}Recommandations d'optimisation:{RESET}")
    for rec in recs:
        print(f"  {rec}")

    avg_engine_ms = mean([e["avg_ms"] for e in engine_profiles if "avg_ms" in e]) if engine_profiles else 0
    avg_route_score = mean([r["score"] for r in route_analysis]) if route_analysis else 100

    print(f"\n{BOLD}Résumé:{RESET}")
    print(f"  Avg engine time : {avg_engine_ms:.2f}ms")
    print(f"  Avg route score : {avg_route_score:.0f}/100\n")

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "engines_profiled": len(engine_profiles),
        "avg_engine_ms": round(avg_engine_ms, 3),
        "engine_profiles": engine_profiles,
        "route_analysis": route_analysis,
        "avg_route_score": round(avg_route_score, 2),
        "recommendations": recs,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--engines", type=int, default=10, help="Nombre d'engines à profiler")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_profiler(args.root, engine_limit=args.engines)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
