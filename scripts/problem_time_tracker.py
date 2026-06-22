#!/usr/bin/env python3
"""
CaelumSwarm™ — Problem Time Tracker v1.0
Agents chronomètres : mesurent le temps de résolution de chaque problème
et identifient les problèmes récurrents les plus difficiles.

Ce système :
  1. Enregistre le début/fin de chaque résolution de problème
  2. Calcule le temps réel vs temps théorique
  3. Identifie les problèmes où l'agent bloque le plus longtemps
  4. Génère un rapport de difficulté par catégorie
  5. Alerte si un problème dépasse son temps moyen x2
  6. Fournit les patterns de blocage pour préparer les agents futurs

Usage:
  python3 scripts/problem_time_tracker.py --start P001     # démarre chrono
  python3 scripts/problem_time_tracker.py --stop P001      # arrête chrono
  python3 scripts/problem_time_tracker.py --report         # rapport complet
  python3 scripts/problem_time_tracker.py --hardest        # top 5 problèmes difficiles
  python3 scripts/problem_time_tracker.py --alert          # alertes dépassement
"""

import json
import sys
import argparse
import time
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
TRACKER_PATH = ROOT / "data" / "time_tracker.json"
ALERTS_PATH = ROOT / "data" / "time_alerts.json"
INFINITE_DB_PATH = ROOT / "data" / "infinite_solutions.json"

G = "\033[92m"; Y = "\033[93m"; R = "\033[91m"
C = "\033[96m"; B = "\033[1m"; P = "\033[95m"; E = "\033[0m"

# Temps théoriques en minutes (référence depuis le catalogue)
THEORETICAL_TIMES = {
    "P001": 2.5,
    "P002": 0.5,
    "P003": 15.0,
    "P004": 10.0,
    "P005": 20.0,
    "P006": 1.0,
    "P007": 3.0,
    "P008": 30.0,
    "P009": 12.0,
    "P010": 25.0,
    "P011": 20.0,
    "P012": 8.0,
}

# Catégories de problèmes
PROBLEM_CATEGORIES = {
    "P001": "git",
    "P002": "git",
    "P003": "sidebar",
    "P004": "security",
    "P005": "engine",
    "P006": "git",
    "P007": "git",
    "P008": "sidebar",
    "P009": "dashboard",
    "P010": "ci_cd",
    "P011": "coordination",
    "P012": "engine",
}

# Titres courts
PROBLEM_TITLES = {
    "P001": "Fichiers non-commités",
    "P002": "Mauvais auteur git",
    "P003": "Doublons icônes sidebar",
    "P004": "Route non sécurisée",
    "P005": "Engine avg_composite incorrect",
    "P006": "Git index.lock bloqué",
    "P007": "Mauvaise branche",
    "P008": "Sidebar overflow (>5500 lignes)",
    "P009": "Dashboard sans 'use client'",
    "P010": "Build Vercel échoue",
    "P011": "Conflit merge parallèle",
    "P012": "Engine crash / ImportError",
}

# Niveaux de difficulté calculés (ratio temps réel / théorique)
DIFFICULTY_THRESHOLDS = {
    "FACILE": 1.0,       # < 1x le temps théorique
    "NORMAL": 2.0,       # 1x à 2x
    "DIFFICILE": 3.5,    # 2x à 3.5x
    "BLOQUANT": 999,     # > 3.5x
}


def load_tracker() -> dict:
    if TRACKER_PATH.exists():
        return json.loads(TRACKER_PATH.read_text("utf-8"))
    return {
        "version": "1.0",
        "description": "CaelumSwarm™ — Chronomètre des Problèmes",
        "active_timers": {},
        "completed_sessions": [],
        "statistics": {
            "by_problem": {},
            "by_category": {},
            "hardest_problems": [],
            "total_time_lost_minutes": 0.0,
            "most_recurring": {},
        },
        "total_sessions": 0,
    }


def save_tracker(tracker: dict) -> None:
    TRACKER_PATH.parent.mkdir(parents=True, exist_ok=True)
    TRACKER_PATH.write_text(json.dumps(tracker, indent=2, ensure_ascii=False), "utf-8")


def start_timer(problem_id: str, context: str = "") -> None:
    """Démarre le chronomètre pour un problème."""
    tracker = load_tracker()
    now = datetime.now(timezone.utc).isoformat()

    if problem_id in tracker["active_timers"]:
        started = tracker["active_timers"][problem_id]["started_at"]
        print(f"{Y}⚠ Chrono {problem_id} déjà en cours depuis {started[:19]}{E}")
        return

    tracker["active_timers"][problem_id] = {
        "problem_id": problem_id,
        "title": PROBLEM_TITLES.get(problem_id, "Inconnu"),
        "category": PROBLEM_CATEGORIES.get(problem_id, "unknown"),
        "theoretical_minutes": THEORETICAL_TIMES.get(problem_id, 10.0),
        "started_at": now,
        "context": context,
    }

    save_tracker(tracker)
    title = PROBLEM_TITLES.get(problem_id, "?")
    theo = THEORETICAL_TIMES.get(problem_id, 10.0)
    print(f"{G}⏱ Chrono démarré — {problem_id}: {title} (théorique: {theo} min){E}")


def stop_timer(problem_id: str, success: bool = True, notes: str = "") -> None:
    """Arrête le chronomètre et enregistre le résultat."""
    tracker = load_tracker()
    now = datetime.now(timezone.utc)

    if problem_id not in tracker["active_timers"]:
        print(f"{R}✗ Aucun chrono actif pour {problem_id}{E}")
        return

    timer = tracker["active_timers"].pop(problem_id)
    started = datetime.fromisoformat(timer["started_at"])
    elapsed_seconds = (now - started).total_seconds()
    elapsed_minutes = round(elapsed_seconds / 60, 2)
    theoretical = timer["theoretical_minutes"]
    ratio = round(elapsed_minutes / max(0.1, theoretical), 2)

    # Calcul du niveau de difficulté
    difficulty = "FACILE"
    for level, threshold in DIFFICULTY_THRESHOLDS.items():
        if ratio < threshold:
            difficulty = level
            break

    session = {
        "problem_id": problem_id,
        "title": timer["title"],
        "category": timer["category"],
        "started_at": timer["started_at"],
        "stopped_at": now.isoformat(),
        "elapsed_minutes": elapsed_minutes,
        "theoretical_minutes": theoretical,
        "ratio": ratio,
        "difficulty": difficulty,
        "success": success,
        "context": timer.get("context", ""),
        "notes": notes,
        "overtime_factor": max(0, ratio - 1.0),
    }

    tracker["completed_sessions"].append(session)
    tracker["completed_sessions"] = tracker["completed_sessions"][-1000:]  # max 1000
    tracker["total_sessions"] += 1

    # Mettre à jour les statistiques par problème
    pid_stats = tracker["statistics"]["by_problem"]
    if problem_id not in pid_stats:
        pid_stats[problem_id] = {
            "count": 0,
            "total_minutes": 0.0,
            "avg_minutes": 0.0,
            "max_minutes": 0.0,
            "min_minutes": 9999.0,
            "success_count": 0,
            "difficulty_counts": {"FACILE": 0, "NORMAL": 0, "DIFFICILE": 0, "BLOQUANT": 0},
        }
    stat = pid_stats[problem_id]
    stat["count"] += 1
    stat["total_minutes"] += elapsed_minutes
    stat["avg_minutes"] = round(stat["total_minutes"] / stat["count"], 2)
    stat["max_minutes"] = max(stat["max_minutes"], elapsed_minutes)
    stat["min_minutes"] = min(stat["min_minutes"], elapsed_minutes)
    if success:
        stat["success_count"] += 1
    stat["difficulty_counts"][difficulty] += 1

    # Stats par catégorie
    cat = timer["category"]
    cat_stats = tracker["statistics"]["by_category"]
    if cat not in cat_stats:
        cat_stats[cat] = {"count": 0, "total_minutes": 0.0, "avg_minutes": 0.0}
    cat_stats[cat]["count"] += 1
    cat_stats[cat]["total_minutes"] += elapsed_minutes
    cat_stats[cat]["avg_minutes"] = round(cat_stats[cat]["total_minutes"] / cat_stats[cat]["count"], 2)

    # Top problèmes difficiles
    difficulty_scores = {
        pid: s["avg_minutes"] / max(0.1, THEORETICAL_TIMES.get(pid, 10.0))
        for pid, s in pid_stats.items()
        if s["count"] > 0
    }
    tracker["statistics"]["hardest_problems"] = [
        {"problem_id": pid, "ratio": round(r, 2), "title": PROBLEM_TITLES.get(pid, "?")}
        for pid, r in sorted(difficulty_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    ]

    # Problèmes les plus récurrents
    tracker["statistics"]["most_recurring"] = dict(
        sorted(
            {pid: s["count"] for pid, s in pid_stats.items()}.items(),
            key=lambda x: x[1], reverse=True
        )[:10]
    )

    # Temps total perdu
    tracker["statistics"]["total_time_lost_minutes"] = round(
        sum(s.get("overtime_factor", 0) * s.get("theoretical_minutes", 10) * s.get("count", 1)
            for pid, s in pid_stats.items()), 1
    )

    save_tracker(tracker)

    # Affichage résultat
    diff_color = G if difficulty == "FACILE" else C if difficulty == "NORMAL" else Y if difficulty == "DIFFICILE" else R
    print(f"\n{B}Chrono {problem_id} arrêté — {timer['title']}{E}")
    print(f"  Temps réel:     {elapsed_minutes} min")
    print(f"  Temps théorique: {theoretical} min")
    print(f"  Ratio:          {ratio}x")
    print(f"  Difficulté:     {diff_color}{B}{difficulty}{E}")
    print(f"  Succès:         {'✓' if success else '✗'}")

    if ratio > 2.0:
        print(f"\n  {R}{B}⚠ ALERTE: Ce problème a pris {ratio}x plus longtemps que prévu!{E}")
        _record_alert(problem_id, elapsed_minutes, theoretical, ratio, difficulty)


def _record_alert(pid: str, elapsed: float, theoretical: float, ratio: float, difficulty: str) -> None:
    """Enregistre une alerte de dépassement."""
    if ALERTS_PATH.exists():
        alerts = json.loads(ALERTS_PATH.read_text("utf-8"))
    else:
        alerts = {"version": "1.0", "alerts": [], "total": 0}

    alerts["alerts"].append({
        "problem_id": pid,
        "title": PROBLEM_TITLES.get(pid, "?"),
        "elapsed_minutes": elapsed,
        "theoretical_minutes": theoretical,
        "ratio": ratio,
        "difficulty": difficulty,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    alerts["total"] += 1
    alerts["alerts"] = alerts["alerts"][-200:]

    ALERTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    ALERTS_PATH.write_text(json.dumps(alerts, indent=2, ensure_ascii=False), "utf-8")


def print_report(tracker: dict) -> None:
    """Affiche le rapport complet du chronomètre."""
    print(f"\n{B}{C}╔{'═'*68}╗{E}")
    print(f"{B}{C}  CaelumSwarm™ — Rapport Temps de Résolution{E}")
    print(f"{B}{C}  Sessions totales: {tracker['total_sessions']} | "
          f"Actives: {len(tracker['active_timers'])}{E}")
    print(f"{B}{C}╚{'═'*68}╝{E}\n")

    stats = tracker["statistics"]

    if not stats["by_problem"]:
        print(f"  {Y}Aucune session enregistrée — démarrez un chrono avec --start PID{E}\n")
        return

    # Tableau par problème
    print(f"  {B}PERFORMANCE PAR PROBLÈME:{E}\n")
    header = f"  {'PID':6} {'Titre':35} {'Moy':6} {'Théo':6} {'Ratio':6} {'N':4} {'Taux%':6}"
    print(f"{C}{header}{E}")
    print(f"  {'─'*65}")

    for pid, stat in sorted(stats["by_problem"].items()):
        theo = THEORETICAL_TIMES.get(pid, 10.0)
        ratio = stat["avg_minutes"] / max(0.1, theo)
        success_rate = round(stat["success_count"] / max(1, stat["count"]) * 100)
        color = G if ratio < 1.5 else Y if ratio < 3.0 else R
        title = PROBLEM_TITLES.get(pid, "?")[:33]
        print(f"{color}  {pid:6} {title:35} {stat['avg_minutes']:5.1f}m "
              f"{theo:5.1f}m {ratio:5.2f}x {stat['count']:3}  {success_rate:5}%{E}")

    # Stats par catégorie
    print(f"\n  {B}PERFORMANCE PAR CATÉGORIE:{E}\n")
    for cat, cat_stat in sorted(stats["by_category"].items()):
        bar_len = min(30, int(cat_stat["avg_minutes"] / 2))
        bar = "█" * bar_len
        print(f"  {cat:20} {cat_stat['avg_minutes']:5.1f} min avg ({cat_stat['count']} sessions)  {Y}{bar}{E}")

    # Temps total perdu
    print(f"\n  {R}Temps total perdu en overtime: {stats['total_time_lost_minutes']} minutes{E}")

    # Chronomètres actifs
    if tracker["active_timers"]:
        print(f"\n  {Y}{B}CHRONOMÈTRES ACTIFS:{E}")
        now = datetime.now(timezone.utc)
        for pid, timer in tracker["active_timers"].items():
            started = datetime.fromisoformat(timer["started_at"])
            elapsed = round((now - started).total_seconds() / 60, 1)
            theo = timer["theoretical_minutes"]
            over = elapsed > theo * 1.5
            color = R if over else Y
            print(f"  {color}  • {pid}: {timer['title'][:40]} — {elapsed} min écoulées "
                  f"(théo: {theo} min){' ⚠ EN RETARD' if over else ''}{E}")


def print_hardest(tracker: dict) -> None:
    """Affiche le top 5 des problèmes les plus difficiles."""
    print(f"\n{B}{C}╔{'═'*68}╗{E}")
    print(f"{B}{C}  CaelumSwarm™ — Top Problèmes les Plus Difficiles{E}")
    print(f"{B}{C}╚{'═'*68}╝{E}\n")

    hardest = tracker["statistics"].get("hardest_problems", [])
    if not hardest:
        print(f"  {Y}Pas encore de données — commencez à tracker les problèmes{E}\n")
        # Afficher les prédictions basées sur les temps théoriques
        print(f"  {B}Prédiction basée sur temps théoriques:{E}\n")
        sorted_by_time = sorted(THEORETICAL_TIMES.items(), key=lambda x: x[1], reverse=True)
        for pid, minutes in sorted_by_time[:5]:
            cat = PROBLEM_CATEGORIES.get(pid, "?")
            title = PROBLEM_TITLES.get(pid, "?")
            print(f"  {Y}  • {pid} ({cat}): {title} — {minutes} min théoriques{E}")
        return

    print(f"  {B}Classement par ratio (temps réel / temps théorique):{E}\n")
    for i, hp in enumerate(hardest[:5], 1):
        ratio = hp["ratio"]
        color = R if ratio > 3.0 else Y if ratio > 2.0 else G
        cat = PROBLEM_CATEGORIES.get(hp["problem_id"], "?")
        stat = tracker["statistics"]["by_problem"].get(hp["problem_id"], {})
        count = stat.get("count", 0)
        avg = stat.get("avg_minutes", 0)
        print(f"  {color}{B}#{i} {hp['problem_id']} ({cat}){E}")
        print(f"      {hp['title']}")
        print(f"      Ratio: {ratio}x | Avg: {avg} min | Survenu: {count}x")
        print()

    print(f"\n  {B}Recommandations:{E}")
    if hardest:
        top = hardest[0]
        pid = top["problem_id"]
        cat = PROBLEM_CATEGORIES.get(pid, "?")
        print(f"  {R}⚡ Le problème {pid} ({cat}) est le plus chronophage.{E}")
        print(f"  → Priorité: automatiser la détection + résolution de {pid}")
        print(f"  → Utiliser: python3 scripts/infinite_solution_db.py --search {pid}")


def print_alerts() -> None:
    """Affiche les alertes de dépassement de temps."""
    if not ALERTS_PATH.exists():
        print(f"{Y}Aucune alerte enregistrée{E}")
        return

    alerts = json.loads(ALERTS_PATH.read_text("utf-8"))
    recent = alerts["alerts"][-10:]

    print(f"\n{B}{C}╔{'═'*68}╗{E}")
    print(f"{B}{C}  CaelumSwarm™ — Alertes Dépassement Temps{E}")
    print(f"{B}{C}  Total alertes: {alerts['total']}{E}")
    print(f"{B}{C}╚{'═'*68}╝{E}\n")

    if not recent:
        print(f"  {G}Aucune alerte récente{E}\n")
        return

    for alert in reversed(recent):
        ratio = alert["ratio"]
        color = R if ratio > 3.0 else Y
        print(f"  {color}{B}[{alert['difficulty']}] {alert['problem_id']}: {alert['title'][:40]}{E}")
        print(f"       {alert['elapsed_minutes']} min réelles vs {alert['theoretical_minutes']} min théoriques ({ratio}x)")
        print(f"       {alert['timestamp'][:19]}")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Problem Time Tracker")
    parser.add_argument("--start", metavar="PID", help="Démarrer chrono (ex: P001)")
    parser.add_argument("--stop", metavar="PID", help="Arrêter chrono (ex: P001)")
    parser.add_argument("--fail", action="store_true", help="Marquer comme échec (avec --stop)")
    parser.add_argument("--notes", default="", help="Notes sur la résolution")
    parser.add_argument("--report", action="store_true", help="Rapport complet")
    parser.add_argument("--hardest", action="store_true", help="Top 5 problèmes difficiles")
    parser.add_argument("--alert", action="store_true", help="Alertes dépassement")
    parser.add_argument("--context", default="", help="Contexte du problème")
    args = parser.parse_args()

    if args.start:
        start_timer(args.start, args.context)
    elif args.stop:
        stop_timer(args.stop, success=not args.fail, notes=args.notes)
    elif args.hardest:
        tracker = load_tracker()
        print_hardest(tracker)
    elif args.alert:
        print_alerts()
    else:
        tracker = load_tracker()
        print_report(tracker)
