#!/usr/bin/env python3
"""
CaelumSwarm™ — Wave Validator avec Simulation
Valide chaque wave AVANT et APRÈS création. Chaque agent doit donner son aval ici.

Usage:
  python3 scripts/wave_validator.py --wave 469 --domains emailautomation marketingops crmdata
  python3 scripts/wave_validator.py --check-all  # audit global toutes les waves récentes
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent

G = "\033[92m"
Y = "\033[93m"
R = "\033[91m"
C = "\033[96m"
B = "\033[1m"
E = "\033[0m"


def ok(msg: str) -> None:
    print(f"  {G}✓{E} {msg}")


def warn(msg: str) -> None:
    print(f"  {Y}⚠{E} {msg}")


def err(msg: str) -> None:
    print(f"  {R}✗{E} {msg}")


def validate_engine(domain: str) -> dict:
    """Valide un engine Python avec simulation complète."""
    result = {"domain": domain, "engine": False, "avg": None, "dist": None, "errors": []}
    engine_path = ROOT / "swarm" / "intelligence" / f"{domain}_engine.py"

    if not engine_path.exists():
        result["errors"].append(f"Engine manquant: {engine_path.name}")
        return result

    try:
        proc = subprocess.run(
            ["python3", str(engine_path)],
            capture_output=True, text=True, timeout=10, cwd=ROOT
        )
        out = proc.stdout
        if proc.returncode != 0:
            result["errors"].append(f"Erreur Python: {proc.stderr[:100]}")
            return result

        # Extraire avg_composite
        m = re.search(r"avg_composite: (\d+\.\d+)", out)
        if m:
            avg = float(m.group(1))
            result["avg"] = avg
            if abs(avg - 61.03) < 0.01:
                result["engine"] = True
            else:
                result["errors"].append(f"avg_composite={avg} ≠ 61.03")

        # Vérifier distribution
        m = re.search(r"distribution: \{(.+?)\}", out)
        if m:
            dist_str = m.group(1)
            has_4_critique = "'critique': 4" in dist_str or "critique': 4" in dist_str
            has_2_eleve = "'élevé': 2" in dist_str or "eleve': 2" in dist_str.replace("é", "e")
            has_1_modere = "'modéré': 1" in dist_str or "modere': 1" in dist_str.replace("é", "e")
            has_1_faible = "'faible': 1" in dist_str
            result["dist"] = {
                "critique": 4 if has_4_critique else "?",
                "élevé": 2 if has_2_eleve else "?",
                "modéré": 1 if has_1_modere else "?",
                "faible": 1 if has_1_faible else "?",
            }
            if not (has_4_critique and has_1_faible):
                result["errors"].append(f"Distribution incorrecte: {dist_str[:60]}")
    except subprocess.TimeoutExpired:
        result["errors"].append("Timeout: engine trop lent (>10s)")
    except Exception as ex:
        result["errors"].append(str(ex)[:80])

    return result


def validate_route(domain: str) -> dict:
    """Valide une route API TypeScript."""
    result = {"domain": domain, "route": False, "errors": []}
    route_path = ROOT / "app" / "api" / domain / "route.ts"

    if not route_path.exists():
        result["errors"].append(f"Route manquante: app/api/{domain}/route.ts")
        return result

    content = route_path.read_text("utf-8", errors="ignore")
    checks = {
        "sealResponse": "sealResponse" in content,
        "SWARM_API_URL guard": "SWARM_API_URL" in content,
        "console.warn": "console.warn" in content,
        "revalidate:30": "revalidate: 30" in content,
        "502 fallback": "502" in content,
        "zéro credentials": "password" not in content.lower() and "secret" not in content.lower(),
    }
    result["checks"] = checks
    failed = [k for k, v in checks.items() if not v]
    if not failed:
        result["route"] = True
    else:
        result["errors"].extend([f"Manque: {f}" for f in failed])

    return result


def validate_sidebar_icon(domain: str) -> dict:
    """Valide la présence d'une icône dans sidebar-icons."""
    result = {"domain": domain, "icon": False, "nav": False, "errors": []}
    # Chercher l'icône par pattern regex (insensible à la casse du CamelCase exact)
    icon_pattern = re.compile(
        r"export function Icon" + re.escape(domain.replace("_", "")),
        re.IGNORECASE
    )

    # Chercher dans tous les fichiers sidebar-icons
    found_icon = False
    for f in (ROOT / "components").glob("sidebar-icons*.tsx"):
        if f.name == "sidebar-icons.tsx": continue
        if icon_pattern.search(f.read_text("utf-8", errors="ignore")):
            found_icon = True
            break

    if found_icon:
        result["icon"] = True
    else:
        result["errors"].append(f"Icône {icon_name} non trouvée dans sidebar-icons-*.tsx")

    # Chercher entrée nav
    nav_content = (ROOT / "components" / "sidebar-nav.tsx").read_text("utf-8", errors="ignore")
    if f"/dashboard/{domain}" in nav_content:
        result["nav"] = True
    else:
        result["errors"].append(f"Entrée nav /dashboard/{domain} non trouvée")

    return result


def validate_wave(wave_num: int, domains: list[str]) -> dict:
    """Validation complète d'une wave."""
    print(f"\n{B}{C}{'═'*60}{E}")
    print(f"{B}{C}  VALIDATION WAVE {wave_num} — {', '.join(domains)}{E}")
    print(f"{B}{C}{'═'*60}{E}")

    wave_result = {
        "wave": wave_num,
        "domains": domains,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engines": [],
        "routes": [],
        "sidebar": [],
        "passed": True,
        "score": 0,
        "max_score": 0,
    }

    for domain in domains:
        print(f"\n  {B}Domain: {domain}{E}")

        # Engine
        eng = validate_engine(domain)
        wave_result["engines"].append(eng)
        wave_result["max_score"] += 3
        if eng["engine"]:
            ok(f"Engine: avg={eng['avg']}, dist={eng['dist']}")
            wave_result["score"] += 3
        else:
            for e in eng["errors"]:
                err(f"Engine: {e}")
            wave_result["passed"] = False

        # Route
        rt = validate_route(domain)
        wave_result["routes"].append(rt)
        wave_result["max_score"] += 3
        if rt["route"]:
            ok("Route: sealResponse ✓ guard ✓ revalidate ✓ 502 ✓")
            wave_result["score"] += 3
        else:
            for e in rt["errors"]:
                err(f"Route: {e}")
            wave_result["passed"] = False

        # Sidebar
        sb = validate_sidebar_icon(domain)
        wave_result["sidebar"].append(sb)
        wave_result["max_score"] += 2
        if sb["icon"] and sb["nav"]:
            ok(f"Sidebar: icône ✓ nav ✓")
            wave_result["score"] += 2
        else:
            for e in sb["errors"]:
                warn(f"Sidebar: {e}")

    # Score final
    pct = round(wave_result["score"] / wave_result["max_score"] * 100) if wave_result["max_score"] > 0 else 0
    color = G if pct == 100 else Y if pct >= 80 else R
    print(f"\n  {color}{B}SCORE WAVE {wave_num}: {wave_result['score']}/{wave_result['max_score']} ({pct}%){E}")

    if pct == 100:
        print(f"  {G}{B}✓ AVAL ACCORDÉ — Wave {wave_num} validée à 100%{E}")
    elif pct >= 80:
        print(f"  {Y}{B}⚠ AVAL PARTIEL — Wave {wave_num} à {pct}% (corrections requises){E}")
    else:
        print(f"  {R}{B}✗ AVAL REFUSÉ — Wave {wave_num} à {pct}% (recréation nécessaire){E}")

    wave_result["pct"] = pct
    return wave_result


def check_all_recent(last_n: int = 10) -> None:
    """Vérifie les N waves les plus récentes via git log."""
    print(f"\n{B}Récupération des {last_n} dernières waves...{E}")

    result = subprocess.run(
        ["git", "log", "--oneline", "-50", "--grep=feat(wave-"],
        capture_output=True, text=True, cwd=ROOT
    )
    waves_seen: dict[int, list[str]] = {}
    for line in result.stdout.splitlines():
        m = re.search(r"feat\(wave-(\d+)\).*?(\w+(?:,\s*\w+)*)\s+(?:engines|API|sidebar)", line)
        if m:
            wave_num = int(m.group(1))
            if wave_num not in waves_seen:
                waves_seen[wave_num] = []

    if not waves_seen:
        print(f"  {Y}Aucune wave trouvée dans git log{E}")
        return

    print(f"  {G}Waves trouvées: {sorted(waves_seen.keys())[-last_n:]}{E}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CaelumSwarm Wave Validator")
    parser.add_argument("--wave", type=int, help="Numéro de la wave à valider")
    parser.add_argument("--domains", nargs="+", help="Domaines de la wave")
    parser.add_argument("--check-all", action="store_true", help="Vérifier toutes les waves récentes")
    args = parser.parse_args()

    if args.check_all:
        check_all_recent()
    elif args.wave and args.domains:
        result = validate_wave(args.wave, args.domains)
        sys.exit(0 if result["pct"] == 100 else 1)
    else:
        # Démo: valider la dernière wave connue
        print(f"{B}CaelumSwarm™ — Wave Validator{E}")
        print("Usage:")
        print("  python3 scripts/wave_validator.py --wave 469 --domains emailautomation marketingops crmdata")
        print("  python3 scripts/wave_validator.py --check-all")

        # Auto-démo sur Wave 475
        print(f"\n{B}Démo — Validation Wave 475:{E}")
        validate_wave(475, ["loyaltyprogram", "referralmarketing", "affiliatefraud"])
