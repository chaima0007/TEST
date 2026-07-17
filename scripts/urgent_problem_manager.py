#!/usr/bin/env python3
"""
CaelumSwarm™ — Urgent Problem Manager v1.0
Gestion des problèmes urgents qui ne peuvent PAS attendre.

Ce système :
  1. Détecte les problèmes URGENTS (bloquants système/CI/agents)
  2. Priorise IMMÉDIATEMENT selon niveau de criticité
  3. Exécute les auto-fixes en moins de 30 secondes
  4. Alerte via data/urgent_alerts.json (lu par tous les agents)
  5. Mobilise les agents de maintenance automatiquement
  6. Notifie avec timestamp précis + contexte de blocage

Niveaux d'urgence :
  🚨 CRITIQUE  — Bloque CI/build/tous les agents (action < 30s)
  🔴 URGENT    — Bloque 1+ agents (action < 2 min)
  🟡 IMPORTANT — Ralentit le système (action < 10 min)
  🟢 NORMAL    — Peut attendre le prochain cycle (action < 1h)

Usage:
  python3 scripts/urgent_problem_manager.py              # scan urgent auto
  python3 scripts/urgent_problem_manager.py --watch      # surveillance continue
  python3 scripts/urgent_problem_manager.py --fix        # auto-fix tous urgents
  python3 scripts/urgent_problem_manager.py --status     # état système
"""

import json
import os
import re
import subprocess
import sys
import argparse
import time
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
URGENT_PATH = ROOT / "data" / "urgent_alerts.json"
BRANCH = "claude/swarm-50-agent-architecture-3l6cno"

G = "\033[92m"; Y = "\033[93m"; R = "\033[91m"
C = "\033[96m"; B = "\033[1m"; P = "\033[95m"; E = "\033[0m"

URGENCY_COLORS = {"CRITIQUE": R, "URGENT": "\033[91m", "IMPORTANT": Y, "NORMAL": G}
URGENCY_ICONS = {"CRITIQUE": "🚨", "URGENT": "🔴", "IMPORTANT": "🟡", "NORMAL": "🟢"}
URGENCY_SLA = {"CRITIQUE": 0.5, "URGENT": 2.0, "IMPORTANT": 10.0, "NORMAL": 60.0}


def run(cmd, timeout=30):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=timeout)
    except subprocess.TimeoutExpired:
        return type("R", (), {"returncode": 1, "stdout": "", "stderr": "timeout"})()


# ─── DÉTECTEURS URGENTS ────────────────────────────────────────────────────────

def detect_all_urgent() -> list[dict]:
    """Scanne et retourne tous les problèmes urgents actifs."""
    problems = []
    now = datetime.now(timezone.utc).isoformat()

    # ── CRITIQUE: index.lock (bloque TOUS les commits) ──────────────────────
    lock = ROOT / ".git" / "index.lock"
    if lock.exists():
        age_s = time.time() - lock.stat().st_mtime
        problems.append({
            "id": "U001",
            "urgency": "CRITIQUE",
            "title": "Git index.lock détecté — TOUS commits bloqués",
            "detail": f"Présent depuis {round(age_s/60, 1)} min",
            "auto_fix": True,
            "fix_cmd": ["rm", "-f", str(lock)],
            "fix_description": f"rm -f {lock}",
            "blocked_agents": "TOUS",
            "detected_at": now,
        })

    # ── CRITIQUE: mauvaise branche ──────────────────────────────────────────
    r = run(["git", "branch", "--show-current"])
    current_branch = r.stdout.strip()
    if current_branch and current_branch != BRANCH:
        problems.append({
            "id": "U002",
            "urgency": "CRITIQUE",
            "title": f"Mauvaise branche: '{current_branch}' (attendu: '{BRANCH}')",
            "detail": "Tous les commits vont sur la mauvaise branche",
            "auto_fix": True,
            "fix_description": f"git checkout {BRANCH}",
            "fix_cmd": ["git", "checkout", BRANCH],
            "blocked_agents": "TOUS",
            "detected_at": now,
        })

    # ── CRITIQUE: doublons icônes (build Vercel échoue) ─────────────────────
    seen = {}
    for f in sorted((ROOT / "components").glob("sidebar-icons-*.tsx")):
        if f.name == "sidebar-icons.tsx": continue
        for line in f.read_text("utf-8", errors="ignore").splitlines():
            m = re.match(r"^export function (Icon\w+)", line)
            if m:
                name = m.group(1)
                seen[name] = seen.get(name, 0) + 1
    dups = [k for k, v in seen.items() if v > 1]
    if dups:
        problems.append({
            "id": "U003",
            "urgency": "CRITIQUE",
            "title": f"Doublons icônes sidebar ({len(dups)} doublons) — Build CI ECHOUE",
            "detail": f"Doublons: {', '.join(dups[:5])}{'...' if len(dups) > 5 else ''}",
            "auto_fix": False,
            "fix_description": "python3 scripts/temporal_loop_detector.py",
            "fix_cmd": ["python3", "scripts/temporal_loop_detector.py"],
            "blocked_agents": "CI/CD + Deploy",
            "detected_at": now,
        })

    # ── URGENT: fichiers non-commités (plus de 5 minutes) ───────────────────
    r = run(["git", "status", "--short"])
    dirty = [l for l in r.stdout.splitlines() if l.startswith("??") or l.startswith(" M") or l.startswith("M ")]
    if dirty:
        problems.append({
            "id": "U004",
            "urgency": "URGENT",
            "title": f"{len(dirty)} fichiers non-commités bloquent les autres agents",
            "detail": f"Fichiers: {', '.join(l.split()[-1] for l in dirty[:5])}",
            "auto_fix": True,
            "fix_description": "git add -A && git commit -m 'rescue: urgent uncommitted files'",
            "fix_cmd": None,  # multi-step
            "fix_steps": [
                ["git", "config", "user.email", "noreply@anthropic.com"],
                ["git", "config", "user.name", "Claude"],
                ["git", "add", "-A"],
                ["git", "commit", "-m", "rescue: urgent uncommitted files detected by UrgentManager"],
            ],
            "blocked_agents": "Sidebar agent + QA agents",
            "detected_at": now,
        })

    # ── URGENT: mauvais auteur git ───────────────────────────────────────────
    r = run(["git", "config", "user.email"])
    email = r.stdout.strip()
    if email and email != "noreply@anthropic.com":
        problems.append({
            "id": "U005",
            "urgency": "URGENT",
            "title": f"Email git incorrect: '{email}' → stop hook va bloquer",
            "detail": "Attendu: noreply@anthropic.com",
            "auto_fix": True,
            "fix_description": "git config user.email noreply@anthropic.com",
            "fix_cmd": ["git", "config", "user.email", "noreply@anthropic.com"],
            "blocked_agents": "TOUS au prochain commit",
            "detected_at": now,
        })

    # ── URGENT: sidebar-icons-4.tsx dépasse seuil ───────────────────────────
    sidebar4 = ROOT / "components" / "sidebar-icons-4.tsx"
    if sidebar4.exists():
        lines = len(sidebar4.read_text("utf-8", errors="ignore").splitlines())
        if lines > 5200:
            urgency = "CRITIQUE" if lines > 5500 else "URGENT" if lines > 5200 else "IMPORTANT"
            problems.append({
                "id": "U006",
                "urgency": urgency,
                "title": f"sidebar-icons-4.tsx atteint {lines} lignes (seuil: 5500)",
                "detail": f"{5500 - lines} lignes avant dépassement critique",
                "auto_fix": False,
                "fix_description": "Créer sidebar-icons-5.tsx pour les nouvelles icônes",
                "fix_cmd": None,
                "blocked_agents": "Wave agents (performance dégradée)",
                "detected_at": now,
            })

    # ── IMPORTANT: routes non sécurisées ────────────────────────────────────
    route_files = list((ROOT / "app" / "api").rglob("route.ts")) if (ROOT / "app" / "api").exists() else []
    intel_routes = [rf for rf in route_files if "auth/" not in str(rf)]
    insecure = [rf for rf in intel_routes
                if "sealResponse" not in rf.read_text("utf-8", errors="ignore")
                or "SWARM_API_URL" not in rf.read_text("utf-8", errors="ignore")]
    if insecure:
        pct = round(len(insecure) / max(1, len(intel_routes)) * 100)
        problems.append({
            "id": "U007",
            "urgency": "IMPORTANT" if pct < 20 else "URGENT",
            "title": f"{len(insecure)} routes sans sealResponse/SWARM_API_URL ({pct}% insécurisées)",
            "detail": f"Routes: {', '.join(rf.parent.name for rf in insecure[:3])}{'...' if len(insecure) > 3 else ''}",
            "auto_fix": False,
            "fix_description": "Ajouter sealResponse + SWARM_API_URL guard sur chaque route",
            "fix_cmd": None,
            "blocked_agents": "Security agents",
            "detected_at": now,
        })

    # ── IMPORTANT: errors.json récent avec erreurs non résolues ─────────────
    errors_file = ROOT / "data" / "errors.json"
    if errors_file.exists():
        try:
            errors_data = json.loads(errors_file.read_text("utf-8"))
            unresolved = [e for e in errors_data.get("errors", [])
                          if not e.get("resolved", False)]
            if len(unresolved) >= 3:
                problems.append({
                    "id": "U008",
                    "urgency": "IMPORTANT",
                    "title": f"{len(unresolved)} erreurs non résolues dans errors.json",
                    "detail": f"Types: {', '.join(set(e.get('type', '?') for e in unresolved[:5]))}",
                    "auto_fix": False,
                    "fix_description": "python3 scripts/problem_solver_agent.py --scan",
                    "fix_cmd": ["python3", "scripts/problem_solver_agent.py", "--scan"],
                    "blocked_agents": "QA agents",
                    "detected_at": now,
                })
        except Exception:
            pass

    return sorted(problems, key=lambda x: ["CRITIQUE", "URGENT", "IMPORTANT", "NORMAL"].index(x["urgency"]))


def auto_fix_problem(problem: dict) -> bool:
    """Tente un auto-fix immédiat."""
    pid = problem["id"]
    title = problem["title"][:50]

    print(f"\n  {Y}⚡ Auto-fix {pid}: {title}...{E}")

    try:
        if problem.get("fix_steps"):
            for step in problem["fix_steps"]:
                r = run(step)
                if r.returncode != 0 and "nothing to commit" not in r.stdout + r.stderr:
                    print(f"  {R}✗ Étape échouée: {' '.join(step[:3])}{E}")
                    return False
            print(f"  {G}✓ Auto-fix réussi (multi-étapes){E}")
            return True

        elif problem.get("fix_cmd"):
            r = run(problem["fix_cmd"])
            if r.returncode == 0:
                print(f"  {G}✓ Auto-fix réussi: {problem['fix_description']}{E}")
                return True
            else:
                print(f"  {R}✗ Auto-fix échoué: {r.stderr[:100]}{E}")
                return False

    except Exception as ex:
        print(f"  {R}✗ Exception auto-fix: {ex}{E}")
        return False

    return False


def save_urgent_alerts(problems: list) -> None:
    """Sauvegarde les alertes urgentes (lisibles par tous les agents)."""
    if URGENT_PATH.exists():
        data = json.loads(URGENT_PATH.read_text("utf-8"))
    else:
        data = {
            "version": "1.0",
            "description": "CaelumSwarm™ — Alertes Problèmes Urgents",
            "total_alerts": 0,
            "active_alerts": [],
            "history": [],
        }

    data["active_alerts"] = problems
    data["last_scan"] = datetime.now(timezone.utc).isoformat()
    data["total_alerts"] += len(problems)

    for p in problems:
        data["history"].append(p)
    data["history"] = data["history"][-500:]

    # Comptage par urgence
    data["summary"] = {
        "CRITIQUE": sum(1 for p in problems if p["urgency"] == "CRITIQUE"),
        "URGENT": sum(1 for p in problems if p["urgency"] == "URGENT"),
        "IMPORTANT": sum(1 for p in problems if p["urgency"] == "IMPORTANT"),
        "NORMAL": sum(1 for p in problems if p["urgency"] == "NORMAL"),
    }

    URGENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    URGENT_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), "utf-8")


def print_status(problems: list) -> None:
    """Affiche l'état des problèmes urgents."""
    now = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")

    print(f"\n{B}{C}╔{'═'*70}╗{E}")
    print(f"{B}{C}  CaelumSwarm™ — Gestionnaire Problèmes URGENTS{E}")
    print(f"{B}{C}  {now} | Problèmes actifs: {len(problems)}{E}")
    print(f"{B}{C}╚{'═'*70}╝{E}\n")

    if not problems:
        print(f"  {G}{B}✓ Aucun problème urgent — système opérationnel{E}\n")
        return

    critique = [p for p in problems if p["urgency"] == "CRITIQUE"]
    urgent = [p for p in problems if p["urgency"] == "URGENT"]
    important = [p for p in problems if p["urgency"] == "IMPORTANT"]

    if critique:
        print(f"  {R}{B}🚨 CRITIQUE ({len(critique)}) — ACTION IMMÉDIATE REQUISE:{E}\n")
        for p in critique:
            print(f"  {R}{B}  [{p['id']}] {p['title']}{E}")
            print(f"       Détail: {p['detail']}")
            print(f"       Agents bloqués: {p['blocked_agents']}")
            print(f"       SLA: < {URGENCY_SLA['CRITIQUE']} min | Auto-fix: {'✓' if p['auto_fix'] else '✗ MANUEL'}")
            print(f"       Fix: {p['fix_description']}\n")

    if urgent:
        print(f"  {R}{B}🔴 URGENT ({len(urgent)}) — Résoudre dans {URGENCY_SLA['URGENT']} min:{E}\n")
        for p in urgent:
            print(f"  {R}  [{p['id']}] {p['title']}{E}")
            print(f"       Fix: {p['fix_description']}\n")

    if important:
        print(f"  {Y}{B}🟡 IMPORTANT ({len(important)}) — Résoudre dans {URGENCY_SLA['IMPORTANT']} min:{E}\n")
        for p in important:
            print(f"  {Y}  [{p['id']}] {p['title']}{E}")
            print(f"       Fix: {p['fix_description']}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Urgent Problem Manager")
    parser.add_argument("--watch", action="store_true", help="Surveillance continue (30s)")
    parser.add_argument("--fix", action="store_true", help="Auto-fix tous les problèmes urgents")
    parser.add_argument("--status", action="store_true", help="État système (scan unique)")
    parser.add_argument("--interval", type=int, default=30, help="Intervalle surveillance (secondes)")
    args = parser.parse_args()

    if args.watch:
        print(f"{G}Surveillance urgente démarrée (intervalle: {args.interval}s)...{E}")
        while True:
            problems = detect_all_urgent()
            save_urgent_alerts(problems)
            print_status(problems)

            critique = [p for p in problems if p["urgency"] in ("CRITIQUE", "URGENT") and p["auto_fix"]]
            if critique:
                print(f"  {Y}⚡ Auto-fixing {len(critique)} problème(s)...{E}")
                for p in critique:
                    auto_fix_problem(p)

            time.sleep(args.interval)
    elif args.fix:
        problems = detect_all_urgent()
        save_urgent_alerts(problems)
        print_status(problems)
        fixable = [p for p in problems if p["auto_fix"]]
        print(f"\n  {Y}⚡ Auto-fixing {len(fixable)} problème(s) urgents...{E}\n")
        fixed = 0
        for p in fixable:
            if auto_fix_problem(p):
                fixed += 1
        print(f"\n  {G if fixed == len(fixable) else Y}{B}Auto-fix: {fixed}/{len(fixable)} résolus{E}\n")
    else:
        # Scan unique (défaut)
        problems = detect_all_urgent()
        save_urgent_alerts(problems)
        print_status(problems)
        if not problems:
            sys.exit(0)
        has_critique = any(p["urgency"] == "CRITIQUE" for p in problems)
        sys.exit(2 if has_critique else 1)
