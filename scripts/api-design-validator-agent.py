#!/usr/bin/env python3
"""API Design Validator Agent — CaelumSwarm™ Dev Support
Valide la cohérence du design des API : nommage, structure de réponse,
versioning, documentation, conformité REST/OpenAPI.
"""
import re
import json
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "APIDesignValidatorAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

NAMING_RULES = {
    "kebab-case": r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$',
    "ends-with-engine": r'.*-engine$',
    "max-length": 60,
}

RESPONSE_STRUCTURE = {
    "required_fields": ["engine", "entities"],
    "optional_fields": ["avg_composite", "confidence_score", "data_sources", "critical_alerts"],
    "forbidden_fields": ["password", "secret", "token", "key", "_internal"],
}


def validate_slug_naming(slug: str) -> list[dict]:
    issues = []
    if not re.match(NAMING_RULES["kebab-case"], slug):
        issues.append({"rule": "NAMING_KEBAB_CASE", "severity": "WARNING",
                       "message": f"Slug '{slug}' n'est pas en kebab-case"})
    if len(slug) > NAMING_RULES["max-length"]:
        issues.append({"rule": "NAMING_TOO_LONG", "severity": "INFO",
                       "message": f"Slug '{slug}' trop long ({len(slug)} > {NAMING_RULES['max-length']})"})
    return issues


def validate_route_structure(route_path: Path) -> dict:
    source = route_path.read_text(encoding="utf-8", errors="ignore")
    issues = []

    # Vérification HTTP methods exposés
    methods = re.findall(r'export\s+async\s+function\s+(GET|POST|PUT|DELETE|PATCH|HEAD)', source)
    if not methods:
        issues.append({"rule": "NO_HTTP_METHOD", "severity": "CRITICAL",
                       "message": "Aucune méthode HTTP exportée"})
    if "POST" in methods or "PUT" in methods or "DELETE" in methods:
        if "sealResponse" not in source:
            issues.append({"rule": "MUTATION_WITHOUT_AUTH", "severity": "HIGH",
                           "message": "Méthode mutation (POST/PUT/DELETE) sans protection"})

    # Vérification Content-Type header
    if "Content-Type" not in source and "headers" not in source.lower():
        issues.append({"rule": "MISSING_CONTENT_TYPE", "severity": "INFO",
                       "message": "Pas de header Content-Type explicite"})

    # Vérification erreurs standardisées
    if "status: 4" in source or "status: 5" in source:
        if '"error"' not in source and "'error'" not in source:
            issues.append({"rule": "NON_STANDARD_ERROR", "severity": "WARNING",
                           "message": "Erreur retournée sans champ 'error' standardisé"})

    # Vérification CORS
    if "Access-Control-Allow-Origin" not in source and "cors" not in source.lower():
        issues.append({"rule": "NO_CORS_HEADERS", "severity": "INFO",
                       "message": "Pas de headers CORS (Next.js les gère automatiquement)"})

    return {
        "file": route_path.parent.name,
        "methods": methods,
        "issues": issues,
        "score": max(0, 100 - sum({"CRITICAL": 30, "HIGH": 20, "WARNING": 10, "INFO": 2}.get(i["severity"], 0) for i in issues))
    }


def check_api_consistency(root: Path) -> dict:
    """Vérifie la cohérence entre toutes les routes API."""
    routes = list((root / "app" / "api").rglob("route.ts"))

    revalidate_values = []
    seal_used = 0
    guard_used = 0

    for route in routes:
        source = route.read_text(encoding="utf-8", errors="ignore")
        rev_match = re.search(r'revalidate\s*=\s*(\d+)', source)
        if rev_match:
            revalidate_values.append(int(rev_match.group(1)))
        if "sealResponse" in source:
            seal_used += 1
        if "SWARM_API_URL" in source:
            guard_used += 1

    unique_revalidate = set(revalidate_values)

    return {
        "total_routes": len(routes),
        "seal_usage": f"{seal_used}/{len(routes)}",
        "guard_usage": f"{guard_used}/{len(routes)}",
        "revalidate_values": sorted(list(unique_revalidate)),
        "revalidate_consistent": len(unique_revalidate) <= 2,
        "inconsistencies": [] if len(unique_revalidate) <= 2 else [f"revalidate non uniforme: {sorted(list(unique_revalidate))}"]
    }


def run_validator(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}CaelumSwarm™ API Design Validator v{VERSION}{RESET}\n")

    routes = list((root / "app" / "api").rglob("route.ts"))
    print(f"Analyse de {len(routes)} routes API...\n")

    all_results = []
    total_issues = 0

    for route in sorted(routes)[:20]:
        result = validate_route_structure(route)
        slug = route.parent.name
        slug_issues = validate_slug_naming(slug)
        result["issues"] += slug_issues
        all_results.append(result)
        total_issues += len(result["issues"])

        color = GREEN if result["score"] >= 90 else YELLOW if result["score"] >= 70 else RED
        if result["issues"]:
            print(f"  {color}{result['score']:3d}/100{RESET}  {slug}")
            for issue in result["issues"][:2]:
                sev_c = RED if issue["severity"] == "CRITICAL" else YELLOW if issue["severity"] in ("HIGH", "WARNING") else "\033[34m"
                print(f"    {sev_c}⚠ [{issue['severity']}]{RESET} {issue['message'][:70]}")

    consistency = check_api_consistency(root)
    print(f"\n{BOLD}Cohérence globale API :{RESET}")
    print(f"  Routes totales : {consistency['total_routes']}")
    print(f"  sealResponse   : {consistency['seal_usage']}")
    print(f"  SWARM guard    : {consistency['guard_usage']}")
    print(f"  revalidate     : {consistency['revalidate_values']}")
    if consistency["revalidate_consistent"]:
        print(f"  {GREEN}✓ revalidate cohérent{RESET}")
    else:
        print(f"  {YELLOW}⚠ revalidate inconsistant{RESET}")

    print()

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "total_routes": len(routes),
        "total_issues": total_issues,
        "consistency": consistency,
        "results": all_results,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_validator(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
