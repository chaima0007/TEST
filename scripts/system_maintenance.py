#!/usr/bin/env python3
"""
CaelumSwarm™ — System Maintenance Agent v1.0
Maintenance permanente de tout le système et l'infrastructure.

Cycle de maintenance (exécuté à chaque wave ou sur demande) :
  1. Audit infrastructure complète (fichiers, routes, engines)
  2. Nettoyage automatique (doublons, fichiers orphelins)
  3. Vérification sécurité globale
  4. Mise à jour bases de données (errors, solutions, knowledge, foresight)
  5. Rapport de santé détaillé avec recommandations
  6. Score de maintenance global (0-100%)

Usage:
  python3 scripts/system_maintenance.py           # maintenance complète
  python3 scripts/system_maintenance.py --quick   # vérification rapide
  python3 scripts/system_maintenance.py --auto    # maintenance + corrections auto
"""

import json
import math
import random
import re
import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
MAINTENANCE_LOG = ROOT / "data" / "maintenance_log.json"

G = "\033[92m"; Y = "\033[93m"; R = "\033[91m"
C = "\033[96m"; B = "\033[1m"; P = "\033[95m"; E = "\033[0m"

BRANCH = "claude/swarm-50-agent-architecture-3l6cno"


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)


# ─── Modules de maintenance ───────────────────────────────────────────────────

def check_infrastructure() -> dict:
    """Audit complet de l'infrastructure."""
    engines = list((ROOT / "swarm" / "intelligence").glob("*_engine.py"))
    routes = [p for p in (ROOT / "app" / "api").rglob("route.ts") if "auth/" not in str(p)]
    scripts = list((ROOT / "scripts").glob("*.py")) + list((ROOT / "scripts").glob("*.sh"))
    data_files = list((ROOT / "data").glob("*.json"))
    sidebar_4 = ROOT / "components" / "sidebar-icons-4.tsx"
    sidebar_lines = len(sidebar_4.read_text("utf-8", errors="ignore").splitlines()) if sidebar_4.exists() else 0

    return {
        "engines_count": len(engines),
        "routes_intel_count": len(routes),
        "scripts_count": len(scripts),
        "data_files_count": len(data_files),
        "sidebar_4_lines": sidebar_lines,
        "sidebar_split_needed": sidebar_lines > 5500,
        "infrastructure_score": min(100, round(
            (min(1, len(routes) / 100) * 40 +
             min(1, len(engines) / 200) * 20 +
             (1 - max(0, (sidebar_lines - 4000) / 6000)) * 20 +
             min(1, len(scripts) / 15) * 20) * 100 / 100, 1
        )),
    }


def check_security() -> dict:
    """Audit sécurité complet."""
    routes = [p for p in (ROOT / "app" / "api").rglob("route.ts") if "auth/" not in str(p)]
    patterns = {
        "sealResponse": 0,
        "SWARM_API_URL": 0,
        "502": 0,
        "revalidate": 0,
    }
    for rf in routes:
        content = rf.read_text("utf-8", errors="ignore")
        for pat in patterns:
            if pat in content:
                patterns[pat] += 1

    total = max(1, len(routes))
    scores = {k: round(v / total * 100, 1) for k, v in patterns.items()}
    avg = round(sum(scores.values()) / len(scores), 1)

    return {
        "routes_total": len(routes),
        "pattern_scores": scores,
        "security_score": avg,
        "fully_secure": sum(1 for rf in routes if all(
            p in rf.read_text("utf-8", errors="ignore")
            for p in ["sealResponse", "SWARM_API_URL", "502"]
        )),
    }


def check_git_health() -> dict:
    """Santé du repository git."""
    r_status = run(["git", "status", "--short"])
    dirty = [l for l in r_status.stdout.splitlines() if l.startswith("??") or l.startswith(" M")]

    r_log = run(["git", "log", "-20", "--format=%ae"])
    emails = r_log.stdout.strip().splitlines()
    correct = sum(1 for e in emails if e == "noreply@anthropic.com")

    r_branch = run(["git", "branch", "--show-current"])
    current = r_branch.stdout.strip()

    r_ahead = run(["git", "log", "--oneline", f"origin/{BRANCH}..HEAD"])
    commits_ahead = len(r_ahead.stdout.strip().splitlines()) if r_ahead.stdout.strip() else 0

    return {
        "branch_ok": current == BRANCH,
        "current_branch": current,
        "dirty_files": len(dirty),
        "author_correct_pct": round(correct / max(1, len(emails)) * 100, 1),
        "commits_ahead_of_origin": commits_ahead,
        "git_score": round(
            (1 if current == BRANCH else 0) * 30 +
            max(0, 1 - len(dirty) * 0.2) * 40 +
            (correct / max(1, len(emails))) * 30,
            1
        ) * 100 / 100,
    }


def check_icon_integrity() -> dict:
    """Intégrité des icônes sidebar."""
    seen: dict[str, list[str]] = {}
    total_icons = 0
    for f in sorted((ROOT / "components").glob("sidebar-icons*.tsx")):
        if f.name == "sidebar-icons.tsx": continue
        count = 0
        for line in f.read_text("utf-8", errors="ignore").splitlines():
            m = re.match(r"^export function (Icon\w+)", line)
            if m:
                seen.setdefault(m.group(1), []).append(f.name)
                count += 1
        total_icons += count

    dups = {k: v for k, v in seen.items() if len(v) > 1}
    return {
        "total_icons": total_icons,
        "unique_icons": len(seen),
        "duplicates": len(dups),
        "duplicate_names": list(dups.keys())[:5],
        "icon_score": round((1 - len(dups) / max(1, len(seen))) * 100, 1),
    }


def check_databases() -> dict:
    """État des bases de données du système."""
    db_status = {}
    db_files = {
        "errors": ROOT / "data" / "errors.json",
        "solutions": ROOT / "data" / "solutions.json",
        "knowledge_base": ROOT / "data" / "knowledge_base.json",
        "foresight": ROOT / "data" / "foresight_report.json",
        "agent_audit": ROOT / "data" / "agent_audit.json",
        "maintenance_log": MAINTENANCE_LOG,
    }

    for name, path in db_files.items():
        if path.exists():
            size = path.stat().st_size
            try:
                data = json.loads(path.read_text("utf-8"))
                records = len(data.get("errors", data.get("sessions", data.get("history", []))))
            except Exception:
                records = 0
            db_status[name] = {"exists": True, "size_kb": round(size / 1024, 1), "records": records}
        else:
            db_status[name] = {"exists": False, "size_kb": 0, "records": 0}

    existing_count = sum(1 for v in db_status.values() if v["exists"])
    return {
        "databases": db_status,
        "db_score": round(existing_count / len(db_files) * 100, 1),
        "total_dbs": len(db_files),
        "active_dbs": existing_count,
    }


# ─── Auto-corrections ─────────────────────────────────────────────────────────

def auto_repair(infra: dict, sec: dict, git: dict, icons: dict, auto: bool = False) -> list[str]:
    """Applique les corrections automatiques possibles."""
    actions = []

    # 1. Rescue fichiers orphelins
    if git["dirty_files"] > 0 and auto:
        r = run(["git", "status", "--short"])
        files = [l[3:].strip() for l in r.stdout.splitlines() if l.startswith("??") or l.startswith(" M")]
        if files:
            run(["git", "add"] + files)
            result = run(["git", "commit", "-m", f"maintenance: rescue {len(files)} fichier(s) non-commités"])
            if result.returncode == 0:
                actions.append(f"Rescue commit: {len(files)} fichier(s) commités")

    # 2. Supprimer doublons icônes
    if icons["duplicates"] > 0 and auto:
        result = run(["python3", "scripts/temporal_loop_detector.py"])
        if result.returncode == 0:
            actions.append(f"Doublons icônes: {icons['duplicates']} supprimés via temporal_loop_detector")
            run(["git", "add", "components/"])
            run(["git", "commit", "-m", f"maintenance: remove {icons['duplicates']} duplicate icon(s)"])

    # 3. Supprimer index.lock
    lock = ROOT / ".git" / "index.lock"
    if lock.exists():
        lock.unlink()
        actions.append("index.lock supprimé")

    return actions


def log_maintenance(report: dict) -> None:
    """Enregistre le rapport de maintenance."""
    if not MAINTENANCE_LOG.exists():
        log = {"version": "1.0", "total_runs": 0, "history": [], "average_score": 0}
    else:
        log = json.loads(MAINTENANCE_LOG.read_text("utf-8"))

    session = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "global_score": report["global_score"],
        "infra_score": report["infrastructure"]["infrastructure_score"],
        "security_score": report["security"]["security_score"],
        "git_score": report["git"]["git_score"],
        "icon_score": report["icons"]["icon_score"],
        "db_score": report["databases"]["db_score"],
        "actions_taken": report.get("actions", []),
    }
    log["history"].append(session)
    log["history"] = log["history"][-30:]
    log["total_runs"] += 1

    # Moyenne sur les 5 dernières sessions
    recent = log["history"][-5:]
    log["average_score"] = round(sum(s["global_score"] for s in recent) / len(recent), 1)
    log["last_run"] = datetime.now(timezone.utc).isoformat()

    MAINTENANCE_LOG.parent.mkdir(parents=True, exist_ok=True)
    MAINTENANCE_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False), "utf-8")


def print_maintenance_report(quick: bool = False, auto: bool = False) -> dict:
    print(f"\n{B}{C}╔{'═'*64}╗{E}")
    print(f"{B}{C}  CaelumSwarm™ — System Maintenance Agent v1.0{E}")
    print(f"{B}{C}  Maintenance permanente infrastructure & système{E}")
    if auto:
        print(f"{B}{C}  Mode AUTO — corrections appliquées immédiatement{E}")
    print(f"{B}{C}╚{'═'*64}╝{E}\n")

    # Exécuter tous les checks
    infra = check_infrastructure()
    sec = check_security()
    git_h = check_git_health()
    icons = check_icon_integrity()
    dbs = check_databases()

    def score_color(s): return G if s >= 85 else Y if s >= 65 else R
    def score_bar(s, w=20): return "█" * int(s / 100 * w) + "░" * (w - int(s / 100 * w))

    # 1. Infrastructure
    print(f"{B}[1/5] INFRASTRUCTURE{E}")
    print(f"  Engines Python : {infra['engines_count']} | Routes intel : {infra['routes_intel_count']}")
    print(f"  Scripts        : {infra['scripts_count']} | Bases données : {infra['data_files_count']}")
    print(f"  Sidebar-4.tsx  : {infra['sidebar_4_lines']} lignes {'⚠️ SPLIT REQUIS' if infra['sidebar_split_needed'] else '✓'}")
    s = infra["infrastructure_score"]
    print(f"  {score_color(s)}Score: {s}% {score_bar(s)}{E}\n")

    # 2. Sécurité
    if not quick:
        print(f"{B}[2/5] SÉCURITÉ ROUTES ({sec['routes_total']} routes intel){E}")
        for pat, pct in sec["pattern_scores"].items():
            c = G if pct >= 95 else Y if pct >= 75 else R
            print(f"  {c}{pat:20} {pct:5.1f}% {score_bar(pct, 15)}{E}")
        print(f"  Entièrement sécurisées: {sec['fully_secure']}/{sec['routes_total']}")
        s = sec["security_score"]
        print(f"  {score_color(s)}Score: {s}% {score_bar(s)}{E}\n")

    # 3. Git
    print(f"{B}[3/5] SANTÉ GIT{E}")
    bc = G if git_h["branch_ok"] else R
    print(f"  {bc}Branche: {git_h['current_branch']}{E}")
    dc = G if git_h["dirty_files"] == 0 else Y if git_h["dirty_files"] < 3 else R
    print(f"  {dc}Fichiers dirty: {git_h['dirty_files']} | Auteur correct: {git_h['author_correct_pct']}%{E}")
    print(f"  Commits ahead: {git_h['commits_ahead_of_origin']}")
    s = min(100, round(git_h["git_score"] * 100, 1))
    print(f"  {score_color(s)}Score: {s:.0f}% {score_bar(s)}{E}\n")

    # 4. Icônes
    print(f"{B}[4/5] INTÉGRITÉ ICÔNES{E}")
    dc = G if icons["duplicates"] == 0 else R
    print(f"  Total icônes : {icons['total_icons']} | Uniques : {icons['unique_icons']}")
    print(f"  {dc}Doublons : {icons['duplicates']}{' — ' + str(icons['duplicate_names']) if icons['duplicates'] > 0 else ''}{E}")
    s = icons["icon_score"]
    print(f"  {score_color(s)}Score: {s}% {score_bar(s)}{E}\n")

    # 5. Bases de données
    print(f"{B}[5/5] BASES DE DONNÉES{E}")
    for db_name, db_info in dbs["databases"].items():
        c = G if db_info["exists"] else Y
        if db_info["exists"]:
            print(f"  {c}✓ {db_name:20} {db_info['size_kb']:6.1f}KB | {db_info['records']} enregistrements{E}")
        else:
            print(f"  {c}? {db_name:20} absent (sera créé à la première exécution){E}")
    s = dbs["db_score"]
    print(f"  {score_color(s)}Score: {s}% {score_bar(s)}{E}\n")

    # Auto-corrections
    actions = []
    if auto or git_h["dirty_files"] > 0 or icons["duplicates"] > 0:
        print(f"{B}AUTO-MAINTENANCE{E}")
        actions = auto_repair(infra, sec, git_h, icons, auto=auto)
        if actions:
            for a in actions:
                print(f"  {G}✓ {a}{E}")
        else:
            print(f"  {Y}Aucune correction auto appliquée (lancer --auto pour activer){E}")
        print()

    # Score global
    global_score = round((
        infra["infrastructure_score"] * 0.20 +
        sec["security_score"] * 0.30 +
        git_h["git_score"] * 100 * 0.20 +
        icons["icon_score"] * 0.15 +
        dbs["db_score"] * 0.15
    ), 1)

    print(f"{B}{'═'*66}{E}")
    print(f"\n  {score_color(global_score)}{B}SCORE MAINTENANCE GLOBAL : {global_score}%{E}")

    if global_score >= 85:
        print(f"  {G}✓ Système en excellente santé — continuer les waves{E}")
    elif global_score >= 70:
        print(f"  {Y}⚠ Système fonctionnel — corriger les points orange{E}")
    else:
        print(f"  {R}✗ Maintenance urgente requise — voir items rouges ci-dessus{E}")

    report = {
        "global_score": global_score,
        "infrastructure": infra,
        "security": sec,
        "git": git_h,
        "icons": icons,
        "databases": dbs,
        "actions": actions,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    log_maintenance(report)
    print(f"\n  {C}Rapport enregistré dans data/maintenance_log.json{E}\n")

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="System Maintenance Agent")
    parser.add_argument("--quick", action="store_true", help="Vérification rapide")
    parser.add_argument("--auto", action="store_true", help="Corrections automatiques")
    args = parser.parse_args()
    report = print_maintenance_report(quick=args.quick, auto=args.auto)
    sys.exit(0 if report["global_score"] >= 70 else 1)
