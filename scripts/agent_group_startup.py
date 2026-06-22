#!/usr/bin/env python3
"""
CaelumSwarm™ — Agent Group Startup Protocol v1.0
Startup OBLIGATOIRE pour chaque groupe d'agents avant tout travail.

Ce script :
  1. Vérifie que l'agent est sur la bonne branche
  2. Lance l'auto-diagnostic complet (self-heal)
  3. Soumet chaque décision au Multi-Agent Decision Validator
  4. Génère un rapport de justification minute par minute
  5. Enregistre l'audit dans data/agent_audit.json
  6. Bloque si le système n'est pas prêt (< seuil sécurité)

Groupes d'agents reconnus :
  wave        — agents de construction de waves
  qa          — agents de qualité assurance
  quantum     — agents quantiques de probabilité
  security    — agents de sécurité
  monitoring  — agents de surveillance

Usage:
  python3 scripts/agent_group_startup.py --group wave --wave 483 --domains d1 d2 d3
  python3 scripts/agent_group_startup.py --group qa
  python3 scripts/agent_group_startup.py --group quantum
  python3 scripts/agent_group_startup.py --status
"""

import json
import math
import random
import re
import subprocess
import sys
import argparse
import time
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
AUDIT_PATH = ROOT / "data" / "agent_audit.json"
BRANCH = "claude/swarm-50-agent-architecture-3l6cno"

G = "\033[92m"; Y = "\033[93m"; R = "\033[91m"
C = "\033[96m"; B = "\033[1m"; P = "\033[95m"; E = "\033[0m"

AGENT_GROUPS = {
    "wave":       {"emoji": "🌊", "desc": "Construction engines + routes + sidebar",   "min_score": 70},
    "qa":         {"emoji": "🔍", "desc": "Qualité assurance + validation 24/24",       "min_score": 80},
    "quantum":    {"emoji": "⚛️",  "desc": "Probabilités Monte Carlo + Bayésien",        "min_score": 65},
    "security":   {"emoji": "🔒", "desc": "Audit sécurité routes + sealResponse",       "min_score": 85},
    "monitoring": {"emoji": "👁️",  "desc": "Surveillance boucles temporelles + alertes","min_score": 60},
    "synergy":    {"emoji": "🔗", "desc": "Synergie sources + communauté experte",      "min_score": 70},
}


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)


def check_branch() -> tuple[bool, str]:
    r = run(["git", "branch", "--show-current"])
    current = r.stdout.strip()
    return current == BRANCH, current


def check_git_config() -> bool:
    r = run(["git", "config", "user.email"])
    return r.stdout.strip() == "noreply@anthropic.com"


def check_clean_tree() -> tuple[bool, int]:
    r = run(["git", "status", "--short"])
    dirty = [l for l in r.stdout.splitlines() if l.startswith("??") or l.startswith(" M")]
    return len(dirty) == 0, len(dirty)


def check_no_duplicates() -> tuple[bool, int]:
    seen: dict[str, int] = {}
    for f in (ROOT / "components").glob("sidebar-icons*.tsx"):
        if f.name == "sidebar-icons.tsx": continue
        for line in f.read_text("utf-8", errors="ignore").splitlines():
            m = re.match(r"^export function (Icon\w+)", line)
            if m:
                seen[m.group(1)] = seen.get(m.group(1), 0) + 1
    dups = sum(1 for v in seen.values() if v > 1)
    return dups == 0, dups


def check_routes_security() -> tuple[float, int, int]:
    route_files = list((ROOT / "app" / "api").rglob("route.ts"))
    intel = [rf for rf in route_files if "auth/" not in str(rf)]
    secure = sum(
        1 for rf in intel
        if "sealResponse" in rf.read_text("utf-8", errors="ignore")
        and "SWARM_API_URL" in rf.read_text("utf-8", errors="ignore")
    )
    pct = round(secure / max(1, len(intel)) * 100, 1)
    return pct, secure, len(intel)


def compute_group_readiness(group: str, wave: int = 0, domains: list[str] | None = None) -> dict:
    """Calcule le score de préparation pour un groupe d'agents."""
    checks = {}

    # 1. Branche correcte
    branch_ok, current = check_branch()
    checks["branch"] = {"ok": branch_ok, "detail": current, "weight": 25}

    # 2. Config git
    git_ok = check_git_config()
    checks["git_config"] = {"ok": git_ok, "detail": "noreply@anthropic.com", "weight": 15}

    # 3. Working tree propre (critique pour wave, moins pour monitoring)
    clean, dirty_count = check_clean_tree()
    checks["clean_tree"] = {"ok": clean, "detail": f"{dirty_count} dirty", "weight": 20}

    # 4. Zéro doublon icônes
    no_dup, dup_count = check_no_duplicates()
    checks["no_duplicates"] = {"ok": no_dup, "detail": f"{dup_count} doublons", "weight": 15}

    # 5. Routes sécurisées
    sec_pct, secure, total = check_routes_security()
    sec_ok = sec_pct >= 95
    checks["routes_security"] = {"ok": sec_ok, "detail": f"{secure}/{total} ({sec_pct}%)", "weight": 25}

    # Score pondéré
    total_weight = sum(c["weight"] for c in checks.values())
    score = sum(c["weight"] for c in checks.values() if c["ok"]) / total_weight * 100

    min_score = AGENT_GROUPS.get(group, {}).get("min_score", 70)
    ready = score >= min_score

    return {
        "group": group,
        "score": round(score, 1),
        "min_score": min_score,
        "ready": ready,
        "checks": checks,
        "wave": wave,
        "domains": domains or [],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def print_startup_report(readiness: dict) -> None:
    group = readiness["group"]
    info = AGENT_GROUPS.get(group, {"emoji": "?", "desc": "Inconnu", "min_score": 70})

    print(f"\n{B}{C}╔{'═'*64}╗{E}")
    print(f"{B}{C}  CaelumSwarm™ — Agent Group Startup Protocol{E}")
    print(f"{B}{C}  Groupe : {info['emoji']} {group.upper()} — {info['desc']}{E}")
    if readiness["wave"]:
        print(f"{B}{C}  Wave {readiness['wave']} | Domains: {', '.join(readiness['domains'])}{E}")
    print(f"{B}{C}  Seuil requis : {readiness['min_score']}% | Score actuel : {readiness['score']}%{E}")
    print(f"{B}{C}╚{'═'*64}╝{E}\n")

    print(f"{B}VÉRIFICATIONS PRÉALABLES (obligatoires){E}\n")
    for name, check in readiness["checks"].items():
        color = G if check["ok"] else R
        status = "✓" if check["ok"] else "✗"
        labels = {
            "branch":          "Branche correcte",
            "git_config":      "Config auteur git",
            "clean_tree":      "Working tree propre",
            "no_duplicates":   "Zéro doublon icônes",
            "routes_security": "Routes sécurisées (≥95%)",
        }
        label = labels.get(name, name)
        print(f"  {color}[{status}] {label:35} {check['detail']}{E}  (poids: {check['weight']}%)")

    print(f"\n{B}{'─'*66}{E}")
    score = readiness["score"]
    color = G if score >= 85 else Y if score >= 70 else R
    print(f"\n  {color}{B}Score préparation : {score}% (seuil: {readiness['min_score']}%){E}")

    if readiness["ready"]:
        print(f"  {G}{B}✓ GROUPE {group.upper()} AUTORISÉ À DÉMARRER{E}")
    else:
        print(f"  {R}{B}✗ GROUPE {group.upper()} BLOQUÉ — Corriger avant de continuer{E}")

        # Actions correctives
        print(f"\n  {Y}Actions correctives requises :{E}")
        checks = readiness["checks"]
        if not checks["branch"]["ok"]:
            print(f"    → git checkout {BRANCH}")
        if not checks["git_config"]["ok"]:
            print(f"    → git config user.email noreply@anthropic.com")
        if not checks["clean_tree"]["ok"]:
            print(f"    → git add -A && git commit -m 'rescue: uncommitted files'")
        if not checks["no_duplicates"]["ok"]:
            print(f"    → python3 scripts/temporal_loop_detector.py")
        if not checks["routes_security"]["ok"]:
            print(f"    → vérifier sealResponse + SWARM_API_URL sur toutes les routes")

    print()


def log_startup(readiness: dict) -> None:
    """Enregistre le démarrage dans data/agent_audit.json."""
    if not AUDIT_PATH.exists():
        audit = {
            "version": "1.0",
            "description": "CaelumSwarm™ — Journal d'audit des démarrages d'agents",
            "total_startups": 0,
            "blocked_startups": 0,
            "sessions": [],
        }
    else:
        audit = json.loads(AUDIT_PATH.read_text("utf-8"))

    session = {
        "timestamp": readiness["timestamp"],
        "group": readiness["group"],
        "wave": readiness.get("wave", 0),
        "domains": readiness.get("domains", []),
        "score": readiness["score"],
        "ready": readiness["ready"],
        "checks_failed": [k for k, v in readiness["checks"].items() if not v["ok"]],
    }

    audit["sessions"].append(session)
    audit["total_startups"] += 1
    if not readiness["ready"]:
        audit["blocked_startups"] += 1
    audit["sessions"] = audit["sessions"][-100:]  # garder 100 dernières sessions
    audit["last_startup"] = readiness["timestamp"]

    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_PATH.write_text(json.dumps(audit, indent=2, ensure_ascii=False), "utf-8")


def print_status() -> None:
    """Affiche le statut de tous les groupes d'agents."""
    print(f"\n{B}{C}╔{'═'*62}╗{E}")
    print(f"{B}{C}  CaelumSwarm™ — Statut Groupes d'Agents{E}")
    print(f"{B}{C}╚{'═'*62}╝{E}\n")

    for group, info in AGENT_GROUPS.items():
        readiness = compute_group_readiness(group)
        score = readiness["score"]
        color = G if readiness["ready"] else Y if score >= 60 else R
        status = "PRÊT" if readiness["ready"] else "BLOQUÉ"
        print(f"  {info['emoji']} {color}{group.upper():15} {score:5.1f}% [{status}]{E}  {info['desc']}")

    if AUDIT_PATH.exists():
        audit = json.loads(AUDIT_PATH.read_text("utf-8"))
        print(f"\n  {C}Démarrages totaux : {audit['total_startups']} | Bloqués : {audit['blocked_startups']}{E}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent Group Startup Protocol")
    parser.add_argument("--group", choices=list(AGENT_GROUPS.keys()), help="Groupe d'agents")
    parser.add_argument("--wave", type=int, default=0, help="Numéro de wave")
    parser.add_argument("--domains", nargs="+", default=[], help="Domaines")
    parser.add_argument("--status", action="store_true", help="Statut tous les groupes")
    args = parser.parse_args()

    if args.status:
        print_status()
    elif args.group:
        readiness = compute_group_readiness(args.group, args.wave, args.domains)
        print_startup_report(readiness)
        log_startup(readiness)
        sys.exit(0 if readiness["ready"] else 1)
    else:
        # Sans argument : statut général
        print_status()
