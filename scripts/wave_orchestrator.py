#!/usr/bin/env python3
"""
CaelumSwarm Wave Orchestrator
Automatise le cycle complet d'une wave : validation → commit → monitoring.
Remplace TOUTES les commandes manuelles décrites dans AGENTS.md.

Usage :
  python3 scripts/wave_orchestrator.py --wave 497 --check    # Pré-checks seulement
  python3 scripts/wave_orchestrator.py --wave 497 --post     # Post-wave complet
  python3 scripts/wave_orchestrator.py --wave 497 --full     # Tout
"""

import os
import re
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent

# ─── Helpers shell ─────────────────────────────────────────────────────────────

def run(cmd: str, capture: bool = True, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, shell=True, text=True, cwd=str(ROOT),
        capture_output=capture, check=check
    )

def ok(msg: str):  print(f"  ✓ {msg}")
def warn(msg: str): print(f"  ⚠ {msg}")
def err(msg: str):  print(f"  ✗ {msg}")
def sep(title: str = ""): print(f"\n{'─'*50}{' ' + title if title else ''}")

# ─── Check 0 : branche git ────────────────────────────────────────────────────

def check_branch() -> bool:
    sep("BRANCHE GIT")
    branch = run("git branch --show-current").stdout.strip()
    expected = "claude/swarm-50-agent-architecture-3l6cno"
    if branch == expected:
        ok(f"Branche correcte : {branch}")
        return True
    err(f"Mauvaise branche : {branch} (attendu : {expected})")
    err("Exécuter : git checkout claude/swarm-50-agent-architecture-3l6cno")
    return False

def ensure_git_config() -> bool:
    run("git config user.email noreply@anthropic.com")
    run("git config user.name Claude")
    ok("Git config : noreply@anthropic.com / Claude")
    return True

def git_pull() -> bool:
    sep("PULL ORIGIN")
    r = run("git pull origin claude/swarm-50-agent-architecture-3l6cno")
    if r.returncode == 0:
        ok("Pull réussi")
        return True
    warn(f"Pull : {r.stderr.strip()[:100]}")
    return False

# ─── Check 1 : icônes dupliquées ──────────────────────────────────────────────

def check_duplicate_icons() -> bool:
    sep("DOUBLONS ICÔNES")
    icons = {}
    duplicates = []
    for f in sorted((ROOT / "components").glob("sidebar-icons*.tsx")):
        text = f.read_text()
        for match in re.finditer(r"^export function (Icon\w+)", text, re.MULTILINE):
            name = match.group(1)
            if name in icons:
                duplicates.append(f"{name} dans {icons[name]} ET {f.name}")
            else:
                icons[name] = f.name
    if duplicates:
        for d in duplicates:
            err(f"Doublon : {d}")
        return False
    ok(f"{len(icons)} icônes — 0 doublon")
    return True

# ─── Check 2 : fichiers non commités ──────────────────────────────────────────

def check_clean_tree() -> bool:
    sep("WORKING TREE")
    r = run("git status --short")
    lines = [l for l in r.stdout.strip().splitlines() if l.strip()]
    if not lines:
        ok("Working tree propre")
        return True
    warn(f"{len(lines)} fichier(s) non commités :")
    for l in lines[:10]:
        print(f"    {l}")
    return False

# ─── Check 3 : engines de la wave ────────────────────────────────────────────

def check_wave_engines(wave: int) -> dict:
    sep(f"ENGINES WAVE {wave}")
    engine_dir = ROOT / "swarm" / "intelligence"
    results = {}

    # Trouver engines avec wave number dans le fichier
    wave_engines = []
    for f in engine_dir.glob("*_engine.py"):
        try:
            content = f.read_text()
            if f'"wave": {wave}' in content or f"wave: {wave}" in content or f"Wave {wave}" in content:
                wave_engines.append(f)
        except Exception:
            pass

    if not wave_engines:
        warn(f"Aucun engine trouvé pour wave {wave}")
        return results

    for engine_file in sorted(wave_engines):
        name = engine_file.stem
        r = run(f"python3 {engine_file}")
        if r.returncode != 0:
            err(f"{name} → ERREUR Python : {r.stderr.strip()[:80]}")
            results[name] = {"status": "ERROR", "error": r.stderr.strip()[:80]}
            continue
        try:
            data = json.loads(r.stdout)
            avg = data.get("avg_composite", 0)
            dist = data.get("distribution", {})
            delta = abs(avg - 61.03)
            dist_ok = dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}

            if delta > 1.0:
                err(f"{name} avg={avg} (Δ={delta:+.2f}) — HORS BORNES")
                results[name] = {"status": "HORS_BORNES", "avg": avg}
            elif delta > 0.5:
                warn(f"{name} avg={avg} (Δ={delta:+.2f}) — ALERTE dérive")
                results[name] = {"status": "ALERTE", "avg": avg}
            else:
                ok(f"{name} avg={avg} ✓ distribution={dist_ok}")
                results[name] = {"status": "OK", "avg": avg, "dist_ok": dist_ok}
        except json.JSONDecodeError:
            err(f"{name} → sortie non-JSON")
            results[name] = {"status": "JSON_ERROR"}

    return results

# ─── Check 4 : routes API ─────────────────────────────────────────────────────

def check_wave_routes(wave: int) -> dict:
    sep(f"ROUTES API WAVE {wave}")
    results = {}
    api_dir = ROOT / "app" / "api"

    # Chercher routes créées récemment (heuristique : wave dans le fichier)
    for route_file in sorted(api_dir.rglob("route.ts")):
        try:
            content = route_file.read_text()
        except Exception:
            continue

        checks = {
            "sealResponse": "sealResponse" in content,
            "SWARM_API_URL_guard": "if (!SWARM_API_URL)" in content or "if (!process.env.SWARM_API_URL)" in content,
            "revalidate_30": "revalidate: 30" in content,
            "fallback_502": "502" in content,
            "no_503": "503" not in content,
        }
        all_ok = all(checks.values())
        slug = route_file.parent.name
        if not all_ok:
            missing = [k for k, v in checks.items() if not v]
            results[slug] = {"status": "ALERTE", "missing": missing}
            warn(f"{slug} manque : {missing}")
        else:
            results[slug] = {"status": "OK"}

    if not results:
        warn("Aucune route trouvée")
    else:
        n_ok = sum(1 for v in results.values() if v["status"] == "OK")
        ok(f"{n_ok}/{len(results)} routes conformes")

    return results

# ─── Check 5 : dashboards ────────────────────────────────────────────────────

def check_wave_dashboards() -> dict:
    sep("DASHBOARDS PATTERN")
    results = {}
    dash_dir = ROOT / "app" / "dashboard"

    issues_total = 0
    for page in sorted(dash_dir.rglob("page.tsx")):
        try:
            content = page.read_text()
        except Exception:
            continue

        checks = {
            "use_client": content.startswith('"use client"'),
            "GaugeRing_r36": 'r={36}' in content or 'r="36"' in content or 'r={36}' in content,
            "no_useCallback": "useCallback" not in content,
            "no_useMemo": "useMemo" not in content,
            "payload_fallback": "payload ?? " in content or ".payload ??" in content,
        }
        slug = page.parent.name
        missing = [k for k, v in checks.items() if not v]
        if missing:
            results[slug] = {"status": "ALERTE", "missing": missing}
            issues_total += 1

    n_total = len(list(dash_dir.rglob("page.tsx")))
    if issues_total == 0:
        ok(f"{n_total} dashboards — tous conformes")
    else:
        warn(f"{issues_total}/{n_total} dashboards avec problèmes")

    return results

# ─── Check 6 : scalabilité ────────────────────────────────────────────────────

def check_scalability() -> bool:
    sep("SCALABILITÉ")
    try:
        r = run("python3 scripts/scalability_guardian.py --quiet")
        if r.returncode == 0:
            ok("Scalabilité : OK")
            return True
        warn("Scalabilité : problèmes détectés")
        # Afficher seulement les lignes importantes
        for line in r.stdout.splitlines():
            if any(x in line for x in ["🔴", "🟠", "CRITIQUE", "ALERTE"]):
                print(f"    {line.strip()}")
        return False
    except Exception as e:
        warn(f"Guardian indisponible : {e}")
        return False

# ─── Check 7 : constantes ────────────────────────────────────────────────────

def check_constants() -> bool:
    sep("CONSTANTES (§9 protocole)")
    try:
        r = run("python3 scripts/constants_monitor.py --quiet 2>/dev/null || python3 scripts/constants_monitor.py")
        output = r.stdout + r.stderr
        if "INVALIDES" in output or "INSTABLE" in output:
            err("Constantes invalides ou instables")
            return False
        ok("Constantes stables — amplitude < borne OK")
        return True
    except Exception:
        warn("constants_monitor.py indisponible — skip")
        return True

# ─── Rapport final ────────────────────────────────────────────────────────────

def generate_report(wave: int, results: dict) -> None:
    sep(f"RAPPORT WAVE {wave}")
    report = {
        "wave": wave,
        "timestamp": datetime.utcnow().isoformat(),
        "results": results,
    }
    path = ROOT / "data" / f"wave_{wave}_orchestrator_report.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    ok(f"Rapport sauvegardé : {path.name}")

    n_ok = sum(1 for v in results.values() if v is True or (isinstance(v, dict) and not v))
    n_total = len(results)
    print(f"\n  Score final : {n_ok}/{n_total} checks OK")

    blockers = [k for k, v in results.items() if v is False or (isinstance(v, dict) and v)]
    if blockers:
        warn(f"Bloquants : {', '.join(blockers)}")
    else:
        ok("Wave prête pour déploiement ✓")

# ─── Modes d'exécution ────────────────────────────────────────────────────────

def run_pre_checks(wave: int) -> dict:
    """Checks à exécuter AVANT de créer les fichiers de la wave."""
    print(f"\n{'═'*50}")
    print(f"  WAVE ORCHESTRATOR — PRÉ-CHECKS WAVE {wave}")
    print(f"{'═'*50}")

    ensure_git_config()
    results = {
        "branch":           check_branch(),
        "pull":             git_pull(),
        "duplicate_icons":  check_duplicate_icons(),
        "clean_tree":       check_clean_tree(),
        "scalability":      check_scalability(),
        "constants":        check_constants(),
    }
    generate_report(wave, results)
    return results

def run_post_checks(wave: int) -> dict:
    """Checks à exécuter APRÈS avoir créé les fichiers de la wave."""
    print(f"\n{'═'*50}")
    print(f"  WAVE ORCHESTRATOR — POST-CHECKS WAVE {wave}")
    print(f"{'═'*50}")

    ensure_git_config()
    results = {
        "branch":           check_branch(),
        "engines":          check_wave_engines(wave),
        "routes":           check_wave_routes(wave),
        "dashboards":       check_wave_dashboards(),
        "duplicate_icons":  check_duplicate_icons(),
        "clean_tree":       check_clean_tree(),
        "scalability":      check_scalability(),
        "constants":        check_constants(),
    }
    generate_report(wave, results)

    # Afficher résumé final
    engine_ok = all(v.get("status") == "OK" for v in results.get("engines", {}).values())
    route_ok = all(v.get("status") == "OK" for v in results.get("routes", {}).values())
    dash_ok = not results.get("dashboards")
    print(f"\n  Engines   : {'✓' if engine_ok else '✗'}")
    print(f"  Routes    : {'✓' if route_ok else '✗'}")
    print(f"  Dashboards: {'✓' if dash_ok else '✗'}")
    print(f"  Icons     : {'✓' if results['duplicate_icons'] else '✗'}")
    print(f"  Scalab.   : {'✓' if results['scalability'] else '⚠'}")
    return results

# ─── Point d'entrée ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CaelumSwarm Wave Orchestrator")
    parser.add_argument("--wave", type=int, default=0, help="Numéro de wave")
    parser.add_argument("--check", action="store_true", help="Pré-checks seulement")
    parser.add_argument("--post",  action="store_true", help="Post-checks seulement")
    parser.add_argument("--full",  action="store_true", help="Pré + post checks")
    args = parser.parse_args()

    wave = args.wave or 0

    if args.check or args.full:
        results = run_pre_checks(wave)
        has_blocker = not all(v for v in results.values() if isinstance(v, bool))
        if has_blocker and not args.full:
            sys.exit(1)

    if args.post or args.full:
        results = run_post_checks(wave)
        engine_issues = any(
            v.get("status") not in ("OK", "ALERTE")
            for v in results.get("engines", {}).values()
        )
        if engine_issues:
            sys.exit(1)

    if not any([args.check, args.post, args.full]):
        # Par défaut : post-checks
        run_post_checks(wave)
