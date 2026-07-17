#!/usr/bin/env python3
"""Architecture Review Agent — CaelumSwarm™ Dev Support
Analyse l'architecture Next.js + Python : patterns, coupling, cohésion,
séparation des responsabilités, scalabilité CSDDD.
"""
import re
import json
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

AGENT_NAME = "ArchitectureReviewAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

ARCHITECTURE_LAYERS = {
    "presentation": ["app/dashboard", "components"],
    "api": ["app/api"],
    "business_logic": ["swarm/intelligence"],
    "infrastructure": ["lib", "scripts"],
    "config": ["next.config", "tsconfig", "package.json"],
}

COUPLING_RULES = [
    ("presentation → api", "OK — fetch('/api/...')"),
    ("presentation → business_logic", "VIOLATION — dashboard ne doit pas importer engine Python"),
    ("api → business_logic", "OK — route peut appeler engine"),
    ("api → infrastructure", "OK — route peut utiliser lib/"),
    ("business_logic → presentation", "VIOLATION — engine ne doit pas importer composants UI"),
]


def count_files_in_layer(root: Path, layer: str) -> dict:
    dirs = ARCHITECTURE_LAYERS.get(layer, [])
    total = 0
    files_by_type = defaultdict(int)
    for d in dirs:
        layer_path = root / d
        if layer_path.exists():
            for f in layer_path.rglob("*"):
                if f.is_file() and not f.name.startswith("."):
                    total += 1
                    files_by_type[f.suffix] += 1
    return {"total": total, "by_type": dict(files_by_type)}


def check_layer_violations(root: Path) -> list[dict]:
    violations = []

    # Vérifier que les dashboards n'importent pas depuis swarm/
    for dash in (root / "app" / "dashboard").rglob("page.tsx"):
        source = dash.read_text(encoding="utf-8", errors="ignore")
        if "swarm/intelligence" in source or "from '../../swarm" in source:
            violations.append({
                "severity": "CRITICAL",
                "type": "LAYER_VIOLATION",
                "file": str(dash.relative_to(root)),
                "message": "Dashboard importe directement depuis swarm/intelligence — violation de couche"
            })

    # Vérifier que les engines Python n'importent pas de React/Next
    for engine in (root / "swarm" / "intelligence").glob("*.py"):
        source = engine.read_text(encoding="utf-8", errors="ignore")
        for forbidden in ["import React", "from 'next'", "from \"next\""]:
            if forbidden in source:
                violations.append({
                    "severity": "CRITICAL",
                    "type": "LAYER_VIOLATION",
                    "file": str(engine.relative_to(root)),
                    "message": f"Engine Python contient '{forbidden}' — violation de couche"
                })

    # Vérifier les routes API — pas d'accès direct à la DB sans lib/
    for route in (root / "app" / "api").rglob("route.ts"):
        source = route.read_text(encoding="utf-8", errors="ignore")
        direct_db = re.findall(r'(?:mysql|postgres|mongodb|sqlite|prisma)\.', source)
        if direct_db and "lib/" not in source:
            violations.append({
                "severity": "WARNING",
                "type": "COUPLING_VIOLATION",
                "file": str(route.relative_to(root)),
                "message": f"Accès DB direct dans la route sans abstraction lib/: {direct_db[0]}"
            })

    return violations


def analyze_cohesion(root: Path) -> dict:
    """Mesure la cohésion de chaque module."""
    engine_files = list((root / "swarm" / "intelligence").glob("*_engine.py"))
    route_files = list((root / "app" / "api").rglob("route.ts"))
    dash_files = list((root / "app" / "dashboard").rglob("page.tsx"))

    # Ratio équilibre engine/route/dashboard
    engines = len(engine_files)
    routes = len(route_files)
    dashboards = len(dash_files)

    balance_score = 100
    if engines > 0:
        route_ratio = routes / engines
        dash_ratio = dashboards / engines
        if route_ratio < 0.8:
            balance_score -= int((1 - route_ratio) * 50)
        if dash_ratio < 0.8:
            balance_score -= int((1 - dash_ratio) * 50)

    return {
        "engines": engines,
        "routes": routes,
        "dashboards": dashboards,
        "balance_score": max(0, balance_score),
        "missing_routes": max(0, engines - routes),
        "missing_dashboards": max(0, engines - dashboards),
    }


def generate_architecture_map(root: Path) -> str:
    """Génère un diagramme ASCII de l'architecture."""
    lines = [
        "┌─────────────────────────────────────────────────────────┐",
        "│          CaelumSwarm™ Architecture Map                  │",
        "├─────────────────────────────────────────────────────────┤",
        "│  PRESENTATION LAYER                                     │",
        "│  app/dashboard/**/page.tsx  ←  User Interfaces          │",
        "│  components/Sidebar.tsx     ←  Navigation               │",
        "├─────────────────────────────────────────────────────────┤",
        "│  API LAYER                                              │",
        "│  app/api/**/route.ts        ←  REST Endpoints          │",
        "│  lib/digital-seal.ts        ←  Security Middleware      │",
        "├─────────────────────────────────────────────────────────┤",
        "│  BUSINESS LOGIC LAYER                                   │",
        "│  swarm/intelligence/*.py    ←  CSDDD Engines            │",
        "├─────────────────────────────────────────────────────────┤",
        "│  INFRASTRUCTURE LAYER                                   │",
        "│  scripts/*.py               ←  Agents Support           │",
        "│  .env / next.config.js      ←  Configuration            │",
        "└─────────────────────────────────────────────────────────┘",
        "",
        "FLOW: Browser → Sidebar → Dashboard → /api/engine → SWARM_API_URL",
        "      ↑ fallback FALLBACK_ENTITIES (502 upstream)",
    ]
    return "\n".join(lines)


def run_review(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}{'='*65}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ Architecture Review Agent v{VERSION}{RESET}")
    print(f"{BOLD}{CYAN}{'='*65}{RESET}\n")

    print(generate_architecture_map(root))
    print()

    # Inventaire par couche
    print(f"{BOLD}Inventaire par couche :{RESET}")
    for layer, dirs in ARCHITECTURE_LAYERS.items():
        stats = count_files_in_layer(root, layer)
        print(f"  {layer:<20} {stats['total']:4d} fichiers  {dict(list(stats['by_type'].items())[:3])}")

    # Violations
    violations = check_layer_violations(root)
    print(f"\n{BOLD}Violations d'architecture :{RESET}")
    if violations:
        for v in violations:
            color = RED if v["severity"] == "CRITICAL" else YELLOW
            print(f"  {color}[{v['severity']}]{RESET} {v['file']}: {v['message']}")
    else:
        print(f"  {GREEN}✓ Aucune violation détectée{RESET}")

    # Cohésion
    cohesion = analyze_cohesion(root)
    print(f"\n{BOLD}Analyse de cohésion :{RESET}")
    print(f"  Engines    : {cohesion['engines']}")
    print(f"  Routes API : {cohesion['routes']}")
    print(f"  Dashboards : {cohesion['dashboards']}")
    color = GREEN if cohesion['balance_score'] >= 90 else YELLOW if cohesion['balance_score'] >= 70 else RED
    print(f"  Score équilibre : {color}{cohesion['balance_score']}/100{RESET}")
    if cohesion['missing_routes'] > 0:
        print(f"  {YELLOW}Routes manquantes : {cohesion['missing_routes']}{RESET}")
    if cohesion['missing_dashboards'] > 0:
        print(f"  {YELLOW}Dashboards manquants : {cohesion['missing_dashboards']}{RESET}")

    print(f"\n{BOLD}Recommandations architecturales :{RESET}")
    recs = [
        "📐 Envisager un dossier lib/engines/ pour les types TypeScript partagés entre routes et dashboards",
        "🔌 Ajouter un middleware Next.js (middleware.ts) pour l'authentification JWT sur /api/*",
        "📦 Extraire les FALLBACK_ENTITIES dans lib/fallback-data/ pour réduire la taille des dashboards",
        "🔄 Créer un lib/swarm-client.ts singleton pour les appels SWARM_API_URL avec retry automatique",
        "🗂️ Envisager app/api/v1/ pour versioning des endpoints CSDDD",
        "🧪 Ajouter un dossier __tests__/ à côté de chaque engine Python pour les tests unitaires",
    ]
    for rec in recs:
        print(f"  {rec}")

    print()

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "layers": {layer: count_files_in_layer(root, layer) for layer in ARCHITECTURE_LAYERS},
        "violations": violations,
        "cohesion": cohesion,
        "recommendations": recs,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_review(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
