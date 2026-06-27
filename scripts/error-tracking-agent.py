#!/usr/bin/env python3
"""Error Tracking Agent — CaelumSwarm™ Dev Support
Agrège et analyse les erreurs : logs Next.js, erreurs Python engines,
erreurs API 502, patterns d'erreurs répétitifs, alertes proactives.
"""
import re
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict, Counter

AGENT_NAME = "ErrorTrackingAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

ERROR_PATTERNS = [
    (r"Error:\s+(.+)", "JS_ERROR"),
    (r"TypeError:\s+(.+)", "TYPE_ERROR"),
    (r"Cannot read propert(?:y|ies) of (?:null|undefined)", "NULL_REFERENCE"),
    (r"SWARM_API_URL not configured", "MISSING_ENV"),
    (r"Upstream (\d+)", "UPSTREAM_ERROR"),
    (r"SyntaxError:\s+(.+)", "SYNTAX_ERROR"),
    (r"ECONNREFUSED", "CONNECTION_REFUSED"),
    (r"ETIMEDOUT", "TIMEOUT"),
    (r"fetch failed", "FETCH_FAILED"),
    (r"502", "HTTP_502"),
]


def scan_for_console_errors(root: Path) -> list[dict]:
    """Cherche les patterns d'erreurs dans les fichiers source."""
    errors_found = []
    ts_files = list((root / "app").rglob("*.ts")) + list((root / "app").rglob("*.tsx"))

    for filepath in ts_files[:30]:
        try:
            source = filepath.read_text(encoding="utf-8", errors="ignore")
            for pattern, error_type in ERROR_PATTERNS:
                matches = re.findall(pattern, source)
                if matches:
                    for match in matches[:2]:
                        msg = match if isinstance(match, str) else str(match)
                        if len(msg) > 5:
                            errors_found.append({
                                "file": str(filepath.relative_to(root)),
                                "type": error_type,
                                "message": msg[:80],
                                "is_handled": "catch" in source or "try" in source,
                            })
        except Exception:
            pass

    return errors_found


def analyze_502_patterns(root: Path) -> dict:
    """Analyse les patterns de 502 dans les routes."""
    routes = list((root / "app" / "api").rglob("route.ts"))
    routes_with_502 = 0
    routes_without_502 = []

    for route in routes:
        source = route.read_text(encoding="utf-8", errors="ignore")
        if "502" in source:
            routes_with_502 += 1
        else:
            routes_without_502.append(route.parent.name)

    return {
        "total_routes": len(routes),
        "with_502_handler": routes_with_502,
        "without_502_handler": routes_without_502[:5],
        "coverage_pct": round(routes_with_502 / len(routes) * 100, 1) if routes else 0,
    }


def generate_sentry_config() -> str:
    """Génère la configuration Sentry pour le tracking d'erreurs."""
    return """// sentry.client.config.ts — CaelumSwarm™ Error Tracking
// Généré par ErrorTrackingAgent
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,

  // Taux d'échantillonnage (0.1 = 10% en production)
  tracesSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,

  // Filtrer les erreurs non critiques
  beforeSend(event) {
    // Ne pas envoyer les 502 attendus (upstream non configuré)
    if (event.message?.includes("SWARM_API_URL not configured")) {
      return null;
    }
    return event;
  },

  // Contexte CaelumSwarm
  initialScope: {
    tags: {
      platform: "CaelumSwarm™",
      csddd_version: "EU 2024/1760",
    },
  },
});
"""


def run_tracker(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}CaelumSwarm™ Error Tracking Agent v{VERSION}{RESET}\n")

    errors = scan_for_console_errors(root)
    patterns_502 = analyze_502_patterns(root)

    # Grouper par type
    by_type = Counter(e["type"] for e in errors)

    print(f"{BOLD}Patterns d'erreurs détectés :{RESET}")
    for error_type, count in by_type.most_common():
        color = RED if count > 10 else YELLOW if count > 3 else "\033[34m"
        print(f"  {color}{count:4d}x{RESET}  {error_type}")

    print(f"\n{BOLD}Couverture 502 fallback :{RESET}")
    print(f"  Routes avec handler 502 : {patterns_502['with_502_handler']}/{patterns_502['total_routes']} ({patterns_502['coverage_pct']}%)")
    if patterns_502["without_502_handler"]:
        print(f"  {YELLOW}Sans handler : {patterns_502['without_502_handler'][:3]}{RESET}")

    unhandled = [e for e in errors if not e["is_handled"]]
    if unhandled:
        print(f"\n{YELLOW}Erreurs potentiellement non gérées :{RESET}")
        for e in unhandled[:5]:
            print(f"  {e['file']}: [{e['type']}] {e['message'][:60]}")

    # Générer config Sentry
    sentry_file = root / "sentry.client.config.ts"
    if not sentry_file.exists():
        sentry_file.write_text(generate_sentry_config(), encoding="utf-8")
        print(f"\n{GREEN}✓ sentry.client.config.ts généré{RESET}")

    print(f"\n{BOLD}Recommandations :{RESET}")
    recs = [
        "📊 Configurer Sentry DSN dans .env.local pour le tracking d'erreurs production",
        "🔔 Ajouter des alertes Sentry pour les erreurs 502 répétitives",
        f"⚡ {100-patterns_502['coverage_pct']:.0f}% des routes sans fallback 502 — risque d'erreurs non gérées",
        "📈 Utiliser Vercel Analytics ou Netlify Analytics pour les métriques réelles",
        "🛡️ Ajouter un Error Boundary React sur chaque dashboard",
    ]
    for rec in recs:
        print(f"  {rec}")
    print()

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "errors_found": len(errors),
        "by_type": dict(by_type),
        "patterns_502": patterns_502,
        "unhandled_count": len(unhandled),
        "recommendations": recs,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_tracker(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
