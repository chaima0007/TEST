#!/usr/bin/env python3
"""Cache Optimization Agent — CaelumSwarm™ Dev Support
Analyse et optimise les stratégies de cache : ISR Next.js, headers HTTP,
revalidation, CDN Netlify, Redis/Upstash recommandations.
"""
import re
import json
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "CacheOptimizationAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

RECOMMENDED_REVALIDATE = {
    "engine": 30,        # Données compliance CSDDD: 30s
    "dashboard": 300,    # Dashboards: 5 min
    "static": 3600,      # Pages statiques: 1h
    "api_health": 10,    # Health check: 10s
}


def analyze_cache_config(root: Path) -> dict:
    routes = list((root / "app" / "api").rglob("route.ts"))
    results = []

    for route in routes:
        source = route.read_text(encoding="utf-8", errors="ignore")
        slug = route.parent.name

        rev_match = re.search(r'export\s+const\s+revalidate\s*=\s*(\d+)', source)
        route_rev = int(rev_match.group(1)) if rev_match else None

        fetch_rev_match = re.search(r'next:\s*\{\s*revalidate:\s*(\d+)\s*\}', source)
        fetch_rev = int(fetch_rev_match.group(1)) if fetch_rev_match else None

        recommendation = RECOMMENDED_REVALIDATE["engine"]

        issues = []
        if route_rev is None:
            issues.append("revalidate absent — page sera régénérée à chaque requête (SSR)")
        elif route_rev > 300:
            issues.append(f"revalidate={route_rev}s trop long pour données CSDDD (recommandé: {recommendation}s)")
        elif route_rev < 10:
            issues.append(f"revalidate={route_rev}s trop court — surcharge serveur")

        if fetch_rev and route_rev and fetch_rev != route_rev:
            issues.append(f"Incohérence: route revalidate={route_rev}s vs fetch revalidate={fetch_rev}s")

        results.append({
            "slug": slug,
            "route_revalidate": route_rev,
            "fetch_revalidate": fetch_rev,
            "recommended": recommendation,
            "issues": issues,
            "score": 100 - len(issues) * 25,
        })

    return results


def generate_redis_config() -> str:
    return """// lib/cache/redis-client.ts — CaelumSwarm™ Cache Layer
// Utiliser Upstash Redis pour le cache distribué
import { Redis } from "@upstash/redis";

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL || "",
  token: process.env.UPSTASH_REDIS_REST_TOKEN || "",
});

const CACHE_TTL = {
  engine: 30,      // 30s pour les engines CSDDD
  dashboard: 300,  // 5min pour les dashboards
  health: 10,      // 10s pour le health check
} as const;

export async function getCachedEngine(slug: string): Promise<unknown | null> {
  if (!process.env.UPSTASH_REDIS_REST_URL) return null;
  try {
    return await redis.get(`engine:${slug}`);
  } catch {
    return null;
  }
}

export async function setCachedEngine(slug: string, data: unknown): Promise<void> {
  if (!process.env.UPSTASH_REDIS_REST_URL) return;
  try {
    await redis.setex(`engine:${slug}`, CACHE_TTL.engine, JSON.stringify(data));
  } catch {
    // Cache failures are non-blocking
  }
}

export async function invalidateEngine(slug: string): Promise<void> {
  if (!process.env.UPSTASH_REDIS_REST_URL) return;
  try {
    await redis.del(`engine:${slug}`);
  } catch {}
}
"""


def run_optimizer(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}{'='*65}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ Cache Optimization Agent v{VERSION}{RESET}")
    print(f"{BOLD}{CYAN}{'='*65}{RESET}\n")

    cache_analysis = analyze_cache_config(root)

    total = len(cache_analysis)
    optimal = sum(1 for r in cache_analysis if not r["issues"])

    print(f"{BOLD}Analyse cache ({optimal}/{total} routes optimales) :{RESET}\n")

    problem_routes = [r for r in cache_analysis if r["issues"]]
    for route in problem_routes[:10]:
        color = YELLOW if route["score"] >= 75 else RED
        print(f"  {color}{route['score']:3d}/100{RESET}  {route['slug']}")
        for issue in route["issues"][:2]:
            print(f"    → {issue}")

    if not problem_routes:
        print(f"  {GREEN}✓ Tous les caches bien configurés{RESET}")

    # Générer le client Redis
    cache_dir = root / "lib" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    redis_file = cache_dir / "redis-client.ts"
    if not redis_file.exists():
        redis_file.write_text(generate_redis_config(), encoding="utf-8")
        print(f"\n{GREEN}✓ lib/cache/redis-client.ts généré (Upstash Redis){RESET}")

    avg_score = sum(r["score"] for r in cache_analysis) / len(cache_analysis) if cache_analysis else 100

    print(f"\n{BOLD}Score cache global : {avg_score:.1f}/100{RESET}")

    print(f"\n{BOLD}Recommandations :{RESET}")
    recs = [
        "⚡ Configurer Upstash Redis pour le cache distribué (plan gratuit suffisant)",
        "🔄 Uniformiser revalidate=30 sur toutes les routes API engines",
        "📊 Activer Netlify Edge Cache pour les routes statiques",
        "🌐 Configurer Cache-Control: s-maxage=30 dans netlify.toml sur /api/*",
        "📈 Utiliser stale-while-revalidate=60 pour améliorer la perception de performance",
        "🗄️ Ajouter UPSTASH_REDIS_REST_URL + UPSTASH_REDIS_REST_TOKEN dans .env",
    ]
    for rec in recs:
        print(f"  {rec}")
    print()

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "routes_analyzed": total,
        "optimal_routes": optimal,
        "avg_cache_score": round(avg_score, 2),
        "cache_analysis": cache_analysis[:10],
        "recommendations": recs,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_optimizer(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
