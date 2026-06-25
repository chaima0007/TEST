#!/usr/bin/env python3
"""
CaelumSwarm™ — Système de Niveaux d'Alerte Quantiques
Visualise en temps réel dans quel seuil se trouve le système.

Niveaux :
  VERT    (>= 95%) — Conditions optimales
  ORANGE  (>= 80%) — Surveillance requise
  ROUGE   (>= 60%) — Action corrective immédiate
  NOIR    (<  60%) — Urgence critique

Usage:
  python3 scripts/alert_levels.py
"""

import json
import math
import random
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
random.seed(None)  # vrai aléatoire

# Couleurs
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
PURPLE = "\033[95m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

LEVELS = {
    "VERT":   (95, 100, GREEN,  "Conditions optimales — continuer"),
    "ORANGE": (80,  95, YELLOW, "Surveillance requise — corriger avant prochaine wave"),
    "ROUGE":  (60,  80, RED,    "Action corrective immédiate requise"),
    "NOIR":   ( 0,  60, PURPLE, "URGENCE CRITIQUE — stopper et réparer"),
}


def level_for(pct: float) -> tuple[str, str, str]:
    for name, (lo, hi, color, action) in LEVELS.items():
        if lo <= pct < hi:
            return name, color, action
    return "VERT", GREEN, "Conditions optimales"


def gauge(value: float, width: int = 40) -> str:
    """Affiche une jauge visuelle colorée."""
    filled = int(value / 100 * width)
    name, color, _ = level_for(value)
    bar = color + "█" * filled + RESET + "░" * (width - filled)
    return f"[{bar}] {color}{value:.1f}%{RESET}"


def compute_indicators() -> dict[str, float]:
    """Calcule tous les indicateurs de santé du système."""
    indicators: dict[str, float] = {}

    # 1. Routes sécurisées
    route_files = list((ROOT / "app" / "api").rglob("route.ts"))
    secure = sum(
        1 for rf in route_files
        if "sealResponse" in rf.read_text("utf-8", errors="ignore")
        and "SWARM_API_URL" in rf.read_text("utf-8", errors="ignore")
        and "502" in rf.read_text("utf-8", errors="ignore")
        and "auth/" not in str(rf)
    )
    auth_count = sum(1 for rf in route_files if "auth/" in str(rf))
    intel_routes = len(route_files) - auth_count
    indicators["routes_security"] = round(secure / intel_routes * 100, 1) if intel_routes > 0 else 100

    # 2. Sidebar santé (inverse du risque OOM)
    sidebar_file = ROOT / "components" / "sidebar-icons-4.tsx"
    sidebar_lines = len(sidebar_file.read_text("utf-8", errors="ignore").splitlines()) if sidebar_file.exists() else 4500
    oom_risk = max(0, (sidebar_lines - 4000) / 6000)
    indicators["sidebar_health"] = round((1 - oom_risk) * 100, 1)

    # 3. Doublons icônes (100% si zéro doublon)
    seen: dict[str, int] = {}
    for f in (ROOT / "components").glob("sidebar-icons*.tsx"):
        if f.name == "sidebar-icons.tsx": continue
        for line in f.read_text("utf-8", errors="ignore").splitlines():
            m = re.match(r"^export function (Icon\w+)", line)
            if m:
                seen[m.group(1)] = seen.get(m.group(1), 0) + 1
    dup_count = sum(1 for v in seen.values() if v > 1)
    total_icons = len(seen)
    indicators["sidebar_uniqueness"] = round((1 - dup_count / max(1, total_icons)) * 100, 1)

    # 4. Working tree propre
    r = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, cwd=ROOT)
    untracked = sum(1 for l in r.stdout.splitlines() if l.startswith("??"))
    unstaged = sum(1 for l in r.stdout.splitlines() if l.startswith(" M"))
    dirty = untracked + unstaged
    indicators["git_cleanliness"] = round(max(0, 100 - dirty * 15), 1)  # -15% par fichier sale

    # 5. Auteur git
    r = subprocess.run(["git", "log", "-10", "--format=%ae"], capture_output=True, text=True, cwd=ROOT)
    emails = r.stdout.strip().splitlines()
    correct = sum(1 for e in emails if e == "noreply@anthropic.com")
    indicators["git_author"] = round(correct / max(1, len(emails)) * 100, 1)

    # 6. Erreurs DB (moins d'erreurs ouvertes = meilleur)
    db_path = ROOT / "data" / "errors.json"
    if db_path.exists():
        db = json.loads(db_path.read_text("utf-8"))
        open_err = sum(1 for e in db["errors"] if e["status"] == "open")
        recurring = sum(1 for e in db["errors"] if e["recurrence_count"] > 3)
        indicators["error_db_health"] = round(max(0, 100 - open_err * 10 - recurring * 5), 1)
    else:
        indicators["error_db_health"] = 50.0

    # 7. Score quantique global (Monte Carlo simplifié)
    probs = [
        indicators["routes_security"] / 100,
        indicators["sidebar_health"] / 100,
        indicators["sidebar_uniqueness"] / 100,
        indicators["git_cleanliness"] / 100,
        indicators["git_author"] / 100,
    ]
    # Probabilité jointe (toutes les conditions satisfaites)
    p_joint = math.prod(probs)
    indicators["quantum_score"] = round(p_joint * 100, 2)

    return indicators


def print_alert_dashboard() -> None:
    print(f"\n{BOLD}{CYAN}╔{'═'*62}╗{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ — Niveaux d'Alerte Quantiques{RESET}")
    print(f"{BOLD}{CYAN}  Seuils en temps réel · Probabilités · Actions{RESET}")
    print(f"{BOLD}{CYAN}╚{'═'*62}╝{RESET}\n")

    # Légende des niveaux
    print(f"{BOLD}LÉGENDE DES SEUILS :{RESET}")
    for name, (lo, hi, color, action) in LEVELS.items():
        print(f"  {color}{BOLD}[{name:6}]{RESET} {lo:3}%–{hi:3}% | {action}")

    print(f"\n{BOLD}{'─'*64}{RESET}")
    print(f"{BOLD}INDICATEURS SYSTÈME — SEUILS ACTUELS{RESET}\n")

    indicators = compute_indicators()
    label_map = {
        "routes_security":    "Sécurité routes API",
        "sidebar_health":     "Santé sidebar (anti-OOM)",
        "sidebar_uniqueness": "Unicité icônes (anti-doublon)",
        "git_cleanliness":    "Propreté git (anti-stop-hook)",
        "git_author":         "Auteur git (anti-rebase)",
        "error_db_health":    "Base de données erreurs",
        "quantum_score":      "SCORE QUANTIQUE GLOBAL",
    }

    global_level = "VERT"
    for key, value in indicators.items():
        label = label_map.get(key, key)
        name, color, action = level_for(value)
        g = gauge(value)
        separator = "═" if key == "quantum_score" else " "
        if key == "quantum_score":
            print(f"\n{BOLD}{'─'*64}{RESET}")
        print(f"  {color}{BOLD}{label:35}{RESET} {g}")
        print(f"  {' '*35} {color}Niveau: {name}{RESET} — {action}")
        if key == "quantum_score":
            global_level = name

    # Résumé actionnable
    print(f"\n{BOLD}{'─'*64}{RESET}")
    _, gc, ga = level_for(indicators.get("quantum_score", 0))
    print(f"\n  {gc}{BOLD}ÉTAT GLOBAL : {global_level}{RESET}")

    # Actions recommandées selon le niveau
    if global_level == "VERT":
        print(f"  {GREEN}✓ Tout est optimal — continuer les waves en parallèle{RESET}")
    elif global_level == "ORANGE":
        print(f"  {YELLOW}⚠ Actions recommandées :{RESET}")
        if indicators.get("git_cleanliness", 100) < 85:
            print(f"    → Exécuter: python3 scripts/temporal_loop_detector.py")
        if indicators.get("sidebar_health", 100) < 90:
            print(f"    → Surveiller sidebar-icons-4.tsx (créer sidebar-icons-5.tsx si > 5500 lignes)")
        if indicators.get("sidebar_uniqueness", 100) < 99:
            print(f"    → Exécuter: python3 scripts/temporal_loop_detector.py (doublons)")
    elif global_level in ("ROUGE", "NOIR"):
        print(f"  {RED}✗ ACTIONS CRITIQUES REQUISES :{RESET}")
        print(f"    1. python3 scripts/temporal_loop_detector.py")
        print(f"    2. python3 scripts/strategic_qa_analyzer.py")
        print(f"    3. python3 scripts/quantum_probability_agent.py --risk-report")

    # Sidebar countdown
    sidebar_file = ROOT / "components" / "sidebar-icons-4.tsx"
    sidebar_lines = len(sidebar_file.read_text("utf-8", errors="ignore").splitlines()) if sidebar_file.exists() else 4500
    waves_left = max(0, int((5500 - sidebar_lines) / 9))
    color_sb = GREEN if waves_left > 50 else YELLOW if waves_left > 20 else RED
    print(f"\n  {color_sb}{BOLD}⏱ sidebar-icons-4.tsx : {sidebar_lines} lignes — split dans ~{waves_left} waves{RESET}")

    total_routes = len(list((ROOT / "app" / "api").rglob("route.ts")))
    total_engines = len(list((ROOT / "swarm" / "intelligence").glob("*.py")))
    print(f"  {CYAN}→ {total_engines} engines | {total_routes} routes | score quantique: {indicators.get('quantum_score', 0):.1f}%{RESET}\n")


if __name__ == "__main__":
    print_alert_dashboard()
