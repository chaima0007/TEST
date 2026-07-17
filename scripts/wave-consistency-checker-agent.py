#!/usr/bin/env python3
"""Wave Consistency Checker Agent — CaelumSwarm™ Dev Support
Vérifie que chaque wave (engine + route + dashboard + sidebar) est complète
et conforme au protocole Wave Development Protocol.
"""
import re
import json
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

AGENT_NAME = "WaveConsistencyCheckerAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def extract_engine_slugs(root: Path) -> list[str]:
    """Extrait tous les slugs depuis les fichiers engine Python."""
    slugs = []
    for f in sorted((root / "swarm" / "intelligence").glob("*_engine.py")):
        slug = f.stem.replace("_", "-")
        slugs.append(slug)
    return slugs


def check_engine_compliance(engine_path: Path) -> dict:
    issues = []
    source = engine_path.read_text(encoding="utf-8", errors="ignore")

    # Vérifie distribution 4/2/1/1 dans les commentaires ou le code
    if "critique" not in source:
        issues.append("Niveau 'critique' absent")

    # Vérifie formule
    if "0.30" not in source or "0.25" not in source or "0.20" not in source:
        issues.append("Formule de pondération incorrecte (0.30/0.25/0.25/0.20)")

    # Vérifie index
    if "estimated_" not in source or "_index" not in source:
        issues.append("Champ estimated_*_index absent")

    # Vérifie run_engine()
    if "def run_engine" not in source:
        issues.append("Fonction run_engine() absente")

    # Vérifie __main__
    if '__name__ == "__main__"' not in source:
        issues.append("Bloc __main__ absent")

    return {"file": engine_path.name, "issues": issues, "ok": len(issues) == 0}


def check_route_compliance(route_path: Path) -> dict:
    issues = []
    source = route_path.read_text(encoding="utf-8", errors="ignore")

    if "sealResponse" not in source:
        issues.append("sealResponse manquant")
    if "SWARM_API_URL" not in source:
        issues.append("Guard SWARM_API_URL manquant")
    if "revalidate" not in source:
        issues.append("revalidate absent")
    if "status: 502" not in source:
        issues.append("status 502 manquant (fallback)")
    if "status: 503" in source:
        issues.append("status 503 interdit → utiliser 502")

    return {"file": str(route_path), "issues": issues, "ok": len(issues) == 0}


def check_dashboard_compliance(dash_path: Path) -> dict:
    issues = []
    source = dash_path.read_text(encoding="utf-8", errors="ignore")
    lines = source.splitlines()

    if not (lines and (lines[0].strip() == '"use client";' or lines[0].strip() == '"use client"')):
        issues.append('"use client" absent en ligne 1 absolue')

    if "payload ?? d" not in source and "payload??d" not in source:
        issues.append("Pattern 'd.payload ?? d' absent")

    if "r={36}" not in source and "r=36" not in source and 'r="36"' not in source:
        issues.append("GaugeRing r=36 absent")

    if "viewBox" not in source or "0 0 88 88" not in source:
        issues.append("GaugeRing viewBox='0 0 88 88' absent")

    # Vérifier apostrophes JSX non échappées
    for i, line in enumerate(lines, 1):
        if re.search(r">([^<]*)['']([^<]*)<", line):
            issues.append(f"Ligne {i}: apostrophe non échappée")
            break

    return {"file": str(dash_path.name), "issues": issues, "ok": len(issues) == 0}


def check_sidebar_entries(root: Path, slugs: list[str]) -> dict:
    sidebar = root / "components" / "Sidebar.tsx"
    if not sidebar.exists():
        return {"error": "Sidebar.tsx introuvable"}

    source = sidebar.read_text(encoding="utf-8", errors="ignore")
    missing_hrefs = []

    for slug in slugs:
        href = f"/dashboard/{slug}"
        if href not in source:
            missing_hrefs.append(href)

    # Vérifier doublons d'icônes
    icon_defs = re.findall(r'^function (Icon\w+)', source, re.MULTILINE)
    seen = set()
    duplicates = []
    for icon in icon_defs:
        if icon in seen:
            duplicates.append(icon)
        seen.add(icon)

    # Vérifier usage JSX d'icônes (interdit)
    jsx_icons = re.findall(r'icon:\s*<(Icon\w+)\s*/>', source)

    return {
        "missing_dashboard_links": missing_hrefs[:10],  # Top 10
        "duplicate_icons": duplicates,
        "jsx_icon_violations": jsx_icons,
        "ok": len(missing_hrefs) == 0 and len(duplicates) == 0 and len(jsx_icons) == 0
    }


def run_checker(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}{'='*70}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ Wave Consistency Checker v{VERSION}{RESET}")
    print(f"{BOLD}{CYAN}{'='*70}{RESET}\n")

    engine_files = sorted((root / "swarm" / "intelligence").glob("*_engine.py"))
    api_dirs = sorted((root / "app" / "api").glob("*/"))
    dash_dirs = sorted((root / "app" / "dashboard").glob("*/"))

    api_slugs = {d.name for d in api_dirs if (d / "route.ts").exists()}
    dash_slugs = {d.name for d in dash_dirs if (d / "page.tsx").exists()}
    engine_slugs = {f.stem.replace("_", "-") for f in engine_files}

    print(f"  Engines Python : {len(engine_files)}")
    print(f"  Routes API     : {len(api_slugs)}")
    print(f"  Dashboards     : {len(dash_slugs)}")

    # Engines sans route
    missing_routes = engine_slugs - api_slugs
    # Engines sans dashboard
    missing_dashboards = engine_slugs - dash_slugs
    # Routes sans engine
    orphan_routes = api_slugs - engine_slugs

    print(f"\n{BOLD}Gaps détectés :{RESET}")
    if missing_routes:
        print(f"  {RED}Routes manquantes ({len(missing_routes)}) :{RESET}")
        for s in sorted(missing_routes)[:5]:
            print(f"    - {s}")
    else:
        print(f"  {GREEN}✓ Toutes les routes API présentes{RESET}")

    if missing_dashboards:
        print(f"  {YELLOW}Dashboards manquants ({len(missing_dashboards)}) :{RESET}")
        for s in sorted(missing_dashboards)[:5]:
            print(f"    - {s}")
    else:
        print(f"  {GREEN}✓ Tous les dashboards présents{RESET}")

    # Compliance check échantillon (10 engines max)
    engine_issues = 0
    print(f"\n{BOLD}Vérification compliance engines (échantillon 10) :{RESET}")
    for engine_path in list(engine_files)[:10]:
        result = check_engine_compliance(engine_path)
        if not result["ok"]:
            engine_issues += 1
            print(f"  {YELLOW}⚠{RESET} {engine_path.name}: {', '.join(result['issues'][:2])}")
        else:
            print(f"  {GREEN}✓{RESET} {engine_path.name}")

    # Vérification Sidebar
    print(f"\n{BOLD}Vérification Sidebar :{RESET}")
    sidebar_result = check_sidebar_entries(root, list(engine_slugs))
    if sidebar_result.get("ok"):
        print(f"  {GREEN}✓ Sidebar cohérente{RESET}")
    else:
        if sidebar_result.get("missing_dashboard_links"):
            print(f"  {YELLOW}Liens manquants: {len(sidebar_result['missing_dashboard_links'])}{RESET}")
        if sidebar_result.get("duplicate_icons"):
            print(f"  {RED}Icônes dupliquées: {sidebar_result['duplicate_icons']}{RESET}")
        if sidebar_result.get("jsx_icon_violations"):
            print(f"  {RED}Violations JSX icon: {sidebar_result['jsx_icon_violations']}{RESET}")

    overall_score = max(0, 100
        - len(missing_routes) * 5
        - len(missing_dashboards) * 5
        - engine_issues * 10
        - len(sidebar_result.get("duplicate_icons", [])) * 20
        - len(sidebar_result.get("jsx_icon_violations", [])) * 15)

    print(f"\n{BOLD}Score cohérence globale: {overall_score}/100{RESET}\n")

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "engines": len(engine_files),
        "api_routes": len(api_slugs),
        "dashboards": len(dash_slugs),
        "missing_routes": sorted(list(missing_routes)),
        "missing_dashboards": sorted(list(missing_dashboards)),
        "orphan_routes": sorted(list(orphan_routes)),
        "sidebar": sidebar_result,
        "consistency_score": overall_score,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_checker(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
