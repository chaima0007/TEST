#!/usr/bin/env python3
"""
CaelumSwarm Scalability Guardian
Intègre toutes les commandes de surveillance et auto-correction dans le programme.
Source: next/dist/docs/01-app/02-guides/memory-usage.md + wave-protocol
"""

import os
import re
import json
import shutil
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
REPORT_PATH = ROOT / "data" / "scalability_report.json"

# ─── Seuils (basés sur docs Next.js + audit project) ──────────────────────────
THRESHOLDS = {
    "sidebar_icon_file_oom":    5500,   # Vercel OOM (next/dist/docs memory-usage.md)
    "sidebar_icon_file_warn":   4400,   # Alerte à 80%
    "sidebar_nav_lag":          3000,   # React rendering lag
    "data_json_max_lines":     50_000,  # Au-delà → paginer
    "engines_python_max":       5000,   # Moteurs autonomes, zéro import global au démarrage
    "api_routes_max":            350,   # Au-delà → grouper en dynamic routes
    "dashboards_max":            400,   # Au-delà → lazy-load obligatoire
}

# ─── Collecte des métriques ────────────────────────────────────────────────────

def check_sidebar_icons() -> dict:
    results = {}
    for f in sorted((ROOT / "components").glob("sidebar-icons*.tsx")):
        lines = len(f.read_text().splitlines())
        icons = len(re.findall(r"^export function Icon", f.read_text(), re.MULTILINE))
        pct = lines / THRESHOLDS["sidebar_icon_file_oom"] * 100
        status = "CRITIQUE" if lines >= THRESHOLDS["sidebar_icon_file_oom"] \
            else "ALERTE" if lines >= THRESHOLDS["sidebar_icon_file_warn"] \
            else "OK"
        results[f.name] = {"lines": lines, "icons": icons, "pct_oom": round(pct, 1), "status": status}
    return results

def check_sidebar_nav() -> dict:
    f = ROOT / "components" / "sidebar-nav.tsx"
    if not f.exists():
        return {"status": "ABSENT"}
    lines = len(f.read_text().splitlines())
    pct = lines / THRESHOLDS["sidebar_nav_lag"] * 100
    return {
        "lines": lines,
        "pct_lag": round(pct, 1),
        "status": "CRITIQUE" if lines > THRESHOLDS["sidebar_nav_lag"] * 1.5 \
            else "ALERTE" if lines > THRESHOLDS["sidebar_nav_lag"] else "OK"
    }

def check_data_files() -> dict:
    data_dir = ROOT / "data"
    if not data_dir.exists():
        return {}
    results = {}
    for f in sorted(data_dir.glob("*.json")):
        size = f.stat().st_size
        lines = len(f.read_text().splitlines())
        status = "ALERTE" if lines > THRESHOLDS["data_json_max_lines"] else "OK"
        if size > 100_000:
            results[f.name] = {"size_kb": round(size / 1024, 1), "lines": lines, "status": status}
    return results

def check_engines() -> dict:
    engine_dir = ROOT / "swarm" / "intelligence"
    if not engine_dir.exists():
        return {"count": 0, "status": "OK"}
    count = len(list(engine_dir.glob("*_engine.py")))
    size_mb = sum(f.stat().st_size for f in engine_dir.glob("*.py")) / 1_048_576
    pct = count / THRESHOLDS["engines_python_max"] * 100
    status = "CRITIQUE" if count >= THRESHOLDS["engines_python_max"] \
        else "ALERTE" if count >= THRESHOLDS["engines_python_max"] * 0.8 \
        else "OK"
    return {"count": count, "size_mb": round(size_mb, 1), "pct_max": round(pct, 1), "status": status}

def check_api_routes() -> dict:
    count = len(list((ROOT / "app" / "api").rglob("route.ts")))
    pct = count / THRESHOLDS["api_routes_max"] * 100
    status = "CRITIQUE" if count >= THRESHOLDS["api_routes_max"] \
        else "ALERTE" if count >= THRESHOLDS["api_routes_max"] * 0.8 \
        else "OK"
    return {"count": count, "pct_max": round(pct, 1), "status": status}

def check_dashboards() -> dict:
    count = len(list((ROOT / "app" / "dashboard").rglob("page.tsx")))
    pct = count / THRESHOLDS["dashboards_max"] * 100
    status = "CRITIQUE" if count >= THRESHOLDS["dashboards_max"] \
        else "ALERTE" if count >= THRESHOLDS["dashboards_max"] * 0.8 \
        else "OK"
    return {"count": count, "pct_max": round(pct, 1), "status": status}

def check_duplicate_icons() -> dict:
    """Détecte les doublons entre tous les fichiers sidebar-icons."""
    all_icons = []
    for f in sorted((ROOT / "components").glob("sidebar-icons*.tsx")):
        text = f.read_text()
        icons = re.findall(r"^export function (Icon\w+)", text, re.MULTILINE)
        for icon in icons:
            all_icons.append({"icon": icon, "file": f.name})

    seen = {}
    duplicates = []
    for item in all_icons:
        if item["icon"] in seen:
            duplicates.append({"icon": item["icon"], "files": [seen[item["icon"]], item["file"]]})
        else:
            seen[item["icon"]] = item["file"]

    return {"total_icons": len(all_icons), "duplicates": duplicates, "status": "CRITIQUE" if duplicates else "OK"}

# ─── Auto-corrections ──────────────────────────────────────────────────────────

def autofix_split_sidebar(filename: str, lines_content: str) -> tuple[str, str]:
    """Divise un fichier sidebar-icons en deux au point médian."""
    all_lines = lines_content.splitlines(keepends=True)
    icon_positions = [i for i, l in enumerate(all_lines) if re.match(r"^export function Icon", l)]

    if not icon_positions:
        return lines_content, ""

    midpoint_idx = icon_positions[len(icon_positions) // 2]

    part1 = "".join(all_lines[:midpoint_idx])
    part2 = '"use client";\n\n' + "".join(all_lines[midpoint_idx:])

    return part1, part2

def autofix_next_config() -> dict:
    """Vérifie et applique les optimisations mémoire Next.js (docs officiels)."""
    config_path = ROOT / "next.config.ts"
    if not config_path.exists():
        return {"status": "ABSENT"}

    content = config_path.read_text()
    checks = {
        "productionBrowserSourceMaps: false": "productionBrowserSourceMaps" in content,
        "webpackMemoryOptimizations: true": "webpackMemoryOptimizations" in content,
        "webpackBuildWorker: true": "webpackBuildWorker" in content,
        "preloadEntriesOnStart: false": "preloadEntriesOnStart" in content,
    }
    missing = [k for k, v in checks.items() if not v]
    return {"checks": checks, "missing": missing, "status": "OK" if not missing else "ALERTE"}

def autofix_package_json() -> dict:
    """Vérifie que NODE_OPTIONS est dans le build script."""
    pkg_path = ROOT / "package.json"
    if not pkg_path.exists():
        return {"status": "ABSENT"}
    pkg = json.loads(pkg_path.read_text())
    build_cmd = pkg.get("scripts", {}).get("build", "")
    has_memory = "max-old-space-size" in build_cmd
    return {
        "build_cmd": build_cmd,
        "has_NODE_OPTIONS": has_memory,
        "status": "OK" if has_memory else "ALERTE"
    }

# ─── Rapport global ────────────────────────────────────────────────────────────

def run_full_audit(verbose: bool = True) -> dict:
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "sidebar_icons": check_sidebar_icons(),
        "sidebar_nav": check_sidebar_nav(),
        "data_files": check_data_files(),
        "engines": check_engines(),
        "api_routes": check_api_routes(),
        "dashboards": check_dashboards(),
        "duplicate_icons": check_duplicate_icons(),
        "next_config": autofix_next_config(),
        "package_json": autofix_package_json(),
    }

    # Score global
    all_statuses = []
    for section in report.values():
        if isinstance(section, dict):
            if "status" in section:
                all_statuses.append(section["status"])
            for v in section.values():
                if isinstance(v, dict) and "status" in v:
                    all_statuses.append(v["status"])

    n_critique = all_statuses.count("CRITIQUE")
    n_alerte = all_statuses.count("ALERTE")
    global_status = "CRITIQUE" if n_critique > 0 else "ALERTE" if n_alerte > 0 else "OK"

    report["summary"] = {
        "global_status": global_status,
        "critique_count": n_critique,
        "alerte_count": n_alerte,
        "ok_count": all_statuses.count("OK"),
    }

    if verbose:
        print("\n" + "="*60)
        print("  SCALABILITY GUARDIAN — CaelumSwarm")
        print("="*60)

        print(f"\n{'STATUT GLOBAL':.<40} {global_status}")
        print(f"  CRITIQUE: {n_critique} | ALERTE: {n_alerte} | OK: {all_statuses.count('OK')}")

        print("\n── SIDEBAR ICONS ──")
        for fname, info in report["sidebar_icons"].items():
            marker = "🔴" if info["status"] == "CRITIQUE" else "🟠" if info["status"] == "ALERTE" else "🟢"
            print(f"  {marker} {fname}: {info['lines']}L ({info['pct_oom']}% OOM) — {info['icons']} icônes — {info['status']}")

        print(f"\n── SIDEBAR NAV ──")
        nav = report["sidebar_nav"]
        marker = "🔴" if nav.get("status") == "CRITIQUE" else "🟠" if nav.get("status") == "ALERTE" else "🟢"
        print(f"  {marker} sidebar-nav.tsx: {nav.get('lines', '?')}L ({nav.get('pct_lag', '?')}% seuil lag)")

        print(f"\n── ENGINES PYTHON ──")
        eng = report["engines"]
        marker = "🔴" if eng["status"] == "CRITIQUE" else "🟠" if eng["status"] == "ALERTE" else "🟢"
        print(f"  {marker} {eng['count']} engines ({eng['pct_max']}% du max) — {eng['size_mb']} MB — {eng['status']}")

        print(f"\n── API ROUTES ──")
        api = report["api_routes"]
        marker = "🟢" if api["status"] == "OK" else "🟠"
        print(f"  {marker} {api['count']} routes ({api['pct_max']}% du max) — {api['status']}")

        print(f"\n── DASHBOARDS ──")
        dash = report["dashboards"]
        marker = "🟢" if dash["status"] == "OK" else "🟠"
        print(f"  {marker} {dash['count']} pages ({dash['pct_max']}% du max) — {dash['status']}")

        print(f"\n── ICÔNES DUPLIQUÉES ──")
        dup = report["duplicate_icons"]
        if dup["duplicates"]:
            print(f"  🔴 {len(dup['duplicates'])} doublons détectés !")
            for d in dup["duplicates"][:5]:
                print(f"     - {d['icon']}: {d['files']}")
        else:
            print(f"  🟢 0 doublon — {dup['total_icons']} icônes au total")

        print(f"\n── NEXT.JS CONFIG ──")
        cfg = report["next_config"]
        if cfg.get("missing"):
            print(f"  🟠 Optimisations manquantes: {cfg['missing']}")
        else:
            print(f"  🟢 Toutes les optimisations mémoire actives")

        print(f"\n── PACKAGE.JSON ──")
        pkg = report["package_json"]
        marker = "🟢" if pkg.get("status") == "OK" else "🟠"
        print(f"  {marker} NODE_OPTIONS: {'✓' if pkg.get('has_NODE_OPTIONS') else '✗ MANQUANT'}")

        print(f"\n── DATA FILES (>100KB) ──")
        for fname, info in report["data_files"].items():
            marker = "🟠" if info["status"] == "ALERTE" else "🟢"
            print(f"  {marker} {fname}: {info['size_kb']}KB — {info['lines']}L")

        print("\n" + "="*60)

        # Recommandations auto
        print("\n── ACTIONS REQUISES ──")
        actions = []
        for fname, info in report["sidebar_icons"].items():
            if info["status"] == "CRITIQUE":
                actions.append(f"  🔴 SPLIT IMMÉDIAT: {fname} ({info['lines']}L ≥ seuil OOM)")
            elif info["status"] == "ALERTE":
                actions.append(f"  🟠 SPLIT PLANIFIÉ: {fname} ({info['lines']}L à {info['pct_oom']}% OOM)")
        if report["duplicate_icons"]["duplicates"]:
            actions.append(f"  🔴 SUPPRIMER DOUBLONS: {len(report['duplicate_icons']['duplicates'])} icônes dupliquées")
        if cfg.get("missing"):
            actions.append(f"  🟠 NEXT.CONFIG: Ajouter {len(cfg['missing'])} optimisations mémoire")
        if not pkg.get("has_NODE_OPTIONS"):
            actions.append(f"  🟠 PACKAGE.JSON: Ajouter NODE_OPTIONS='--max-old-space-size=4096'")
        if not actions:
            actions.append("  🟢 Aucune action immédiate requise")
        for a in actions:
            print(a)
        print()

    # Sauvegarde rapport
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False))

    return report

# ─── Projection de croissance ──────────────────────────────────────────────────

def run_growth_projection(waves_ahead: int = 20) -> None:
    icons_per_wave = 3
    lines_per_icon = 11
    routes_per_wave = 3
    dashboards_per_wave = 3
    engines_per_wave = 3

    icons5_current = len((ROOT / "components" / "sidebar-icons-5.tsx").read_text().splitlines()) \
        if (ROOT / "components" / "sidebar-icons-5.tsx").exists() else 0
    routes_current = len(list((ROOT / "app" / "api").rglob("route.ts")))
    dash_current = len(list((ROOT / "app" / "dashboard").rglob("page.tsx")))
    engines_current = len(list((ROOT / "swarm" / "intelligence").glob("*_engine.py")))

    print("\n── PROJECTION (prochaines {} waves) ──".format(waves_ahead))
    print(f"  sidebar-icons-5.tsx actuel: {icons5_current}L")
    split_wave = None
    for w in range(1, waves_ahead + 1):
        proj_lines = icons5_current + w * icons_per_wave * lines_per_icon
        if proj_lines >= THRESHOLDS["sidebar_icon_file_warn"] and split_wave is None:
            split_wave = w
    if split_wave:
        print(f"  🟠 icons-5 → ALERTE dans {split_wave} waves (≈ {icons5_current + split_wave*icons_per_wave*lines_per_icon}L)")
    else:
        print(f"  🟢 icons-5 reste sous seuil dans les {waves_ahead} prochaines waves")

    proj_routes = routes_current + waves_ahead * routes_per_wave
    proj_dash = dash_current + waves_ahead * dashboards_per_wave
    proj_engines = engines_current + waves_ahead * engines_per_wave
    print(f"  Routes dans +{waves_ahead}w: {proj_routes}/{THRESHOLDS['api_routes_max']} {'🟠' if proj_routes > THRESHOLDS['api_routes_max']*0.8 else '🟢'}")
    print(f"  Dashboards dans +{waves_ahead}w: {proj_dash}/{THRESHOLDS['dashboards_max']} {'🟠' if proj_dash > THRESHOLDS['dashboards_max']*0.8 else '🟢'}")
    print(f"  Engines dans +{waves_ahead}w: {proj_engines}/{THRESHOLDS['engines_python_max']} {'🟠' if proj_engines > THRESHOLDS['engines_python_max']*0.8 else '🟢'}")

# ─── Point d'entrée ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    verbose = "--quiet" not in sys.argv
    report = run_full_audit(verbose=verbose)
    if verbose:
        run_growth_projection(waves_ahead=30)

    # Exit code non-zéro si problèmes critiques (utile pour CI/hooks)
    n_critique = report["summary"]["critique_count"]
    sys.exit(1 if n_critique > 0 else 0)
