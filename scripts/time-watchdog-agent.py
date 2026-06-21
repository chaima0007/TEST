"""
time-watchdog-agent.py — Caelum Partners
Surveille les durées d'opérations critiques et déclenche des solutions
automatiques si un seuil temporel est dépassé.
"""

import time
import json
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Callable

# ─── Seuils temporels (en secondes) ─────────────────────────────────────────

THRESHOLDS = {
    "netlify_build":        {"warn": 180, "critical": 300, "abort": 600},
    "npm_build":            {"warn": 60,  "critical": 120, "abort": 240},
    "engine_validation":    {"warn": 5,   "critical": 15,  "abort": 30},
    "wave_complete":        {"warn": 300, "critical": 600, "abort": 900},
    "git_push":             {"warn": 15,  "critical": 30,  "abort": 60},
    "sidebar_edit":         {"warn": 30,  "critical": 60,  "abort": 120},
}

# ─── Solutions automatiques par type d'opération ────────────────────────────

SOLUTIONS = {
    "netlify_build": [
        "Vérifier netlify.toml : publish=.next + [[plugins]] @netlify/plugin-nextjs",
        "Vérifier next.config.ts : ignoreBuildErrors=true, ignoreDuringBuilds=true",
        "Vérifier les icônes Sidebar : icon: IconName (ComponentType, pas JSX object)",
        "Vérifier NODE_OPTIONS=--max-old-space-size=4096 dans [build.environment]",
        "Ouvrir le deploy log Netlify et chercher la première ligne d'erreur",
        "Forcer un rebuild : Trigger deploy > Clear cache and deploy site",
    ],
    "npm_build": [
        "Augmenter NODE_OPTIONS : --max-old-space-size=8192",
        "Nettoyer le cache : rm -rf .next && npm run build",
        "Vérifier les imports circulaires dans les composants",
        "Vérifier les erreurs TypeScript : npx tsc --noEmit",
    ],
    "engine_validation": [
        "Vérifier la distribution : exactement 4c/2é/1m/1f",
        "Vérifier la formule : sub1×0.30 + sub2×0.25 + sub3×0.25 + sub4×0.20",
        "Vérifier les seuils : critique≥60, élevé≥40, modéré≥20, faible<20",
        "Vérifier les assertions assert dist == {'critique':4, 'élevé':2, ...}",
    ],
    "wave_complete": [
        "Arrêter les agents background : TaskStop sur tous les agents actifs",
        "Reprendre en mode manuel : engines → routes → sidebar → dashboards",
        "Committer immédiatement chaque groupe de fichiers créés",
        "Vérifier git status --short : aucun ?? autorisé avant fin de wave",
    ],
    "git_push": [
        "Vérifier la connexion réseau : ping github.com",
        "Retry avec backoff : 2s, 4s, 8s, 16s",
        "Vérifier les conflits : git pull --rebase origin claude/swarm-50-agent-architecture-3l6cno",
        "Vérifier la branche courante : git branch --show-current",
    ],
    "sidebar_edit": [
        "Vérifier les doublons : grep '^function Icon' Sidebar.tsx | sort | uniq -d",
        "Vérifier le format : icon: IconName (pas icon: <IconName className=/>)",
        "Un seul agent à la fois sur Sidebar.tsx",
        "git pull avant toute modification Sidebar.tsx",
    ],
}

# ─── Classe principale ───────────────────────────────────────────────────────

class TimeWatchdog:
    def __init__(self, operation: str, verbose: bool = True):
        self.operation = operation
        self.verbose = verbose
        self.start_time = time.time()
        self.thresholds = THRESHOLDS.get(operation, {"warn": 60, "critical": 120, "abort": 300})
        self.solutions = SOLUTIONS.get(operation, ["Vérifier les logs pour plus de détails"])
        self._warned = False
        self._critical = False

    def elapsed(self) -> float:
        return time.time() - self.start_time

    def status(self) -> str:
        e = self.elapsed()
        if e >= self.thresholds["critical"]:
            return "CRITICAL"
        if e >= self.thresholds["warn"]:
            return "WARN"
        return "OK"

    def check(self) -> bool:
        e = self.elapsed()
        t = self.thresholds

        if e >= t["abort"]:
            self._report("ABORT", e)
            return False

        if e >= t["critical"] and not self._critical:
            self._critical = True
            self._report("CRITICAL", e)

        elif e >= t["warn"] and not self._warned:
            self._warned = True
            self._report("WARN", e)

        return True

    def _report(self, level: str, elapsed: float):
        if not self.verbose:
            return
        icons = {"WARN": "⚠️", "CRITICAL": "🔴", "ABORT": "💀", "OK": "✓"}
        icon = icons.get(level, "?")
        print(f"\n{icon}  [{level}] {self.operation} — {elapsed:.1f}s écoulées")
        if level in ("CRITICAL", "ABORT"):
            print(f"   Seuil dépassé : {self.thresholds.get(level.lower(), '?')}s")
            print(f"\n   Solutions automatiques :")
            for i, sol in enumerate(self.solutions, 1):
                print(f"   {i}. {sol}")
        print()

    def done(self, success: bool = True):
        e = self.elapsed()
        if success:
            print(f"✓  {self.operation} terminé en {e:.1f}s")
        else:
            print(f"✗  {self.operation} échoué après {e:.1f}s")
            self._report("ABORT", e)

    def __enter__(self):
        if self.verbose:
            print(f"⏱  Démarrage surveillance : {self.operation}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.done(success=False)
        else:
            self.done(success=True)
        return False


# ─── Surveillance Netlify build ──────────────────────────────────────────────

def watch_netlify_build(max_wait: int = 600, poll_interval: int = 10):
    """Surveille un build Netlify en cours et déclenche les solutions si dépassement."""
    print("=" * 60)
    print("🔭  Netlify Build Watchdog — Caelum Partners")
    print(f"    Seuil warn: {THRESHOLDS['netlify_build']['warn']}s")
    print(f"    Seuil critique: {THRESHOLDS['netlify_build']['critical']}s")
    print(f"    Abandon après: {THRESHOLDS['netlify_build']['abort']}s")
    print("=" * 60)

    watchdog = TimeWatchdog("netlify_build")
    start = datetime.now()

    while True:
        elapsed = watchdog.elapsed()
        if elapsed >= max_wait:
            print(f"\n💀  Temps maximum atteint ({max_wait}s). Solutions :")
            for i, sol in enumerate(SOLUTIONS["netlify_build"], 1):
                print(f"   {i}. {sol}")
            return False

        if not watchdog.check():
            return False

        remaining = max_wait - elapsed
        print(f"   [{datetime.now().strftime('%H:%M:%S')}] En attente... {elapsed:.0f}s écoulées, {remaining:.0f}s restantes", end="\r")
        time.sleep(poll_interval)


# ─── Surveillance engine Python ──────────────────────────────────────────────

def run_engine_with_watchdog(engine_path: str) -> bool:
    """Exécute un engine Python avec surveillance temporelle."""
    with TimeWatchdog("engine_validation") as w:
        try:
            result = subprocess.run(
                ["python3", engine_path],
                capture_output=True, text=True, timeout=w.thresholds["abort"]
            )
            if result.returncode != 0:
                print(f"✗  Engine échoué :\n{result.stderr}")
                return False
            print(result.stdout)
            return True
        except subprocess.TimeoutExpired:
            print(f"💀  Engine timeout après {w.thresholds['abort']}s")
            return False


# ─── Rapport global ──────────────────────────────────────────────────────────

def generate_report(results: dict) -> dict:
    """Génère un rapport de surveillance des temps."""
    report = {
        "generated_at": datetime.now().isoformat(),
        "operations": [],
        "alerts": [],
        "recommendations": [],
    }

    for op, data in results.items():
        elapsed = data.get("elapsed", 0)
        threshold = THRESHOLDS.get(op, {})
        status = "OK"
        if elapsed >= threshold.get("abort", 999999):
            status = "ABORT"
        elif elapsed >= threshold.get("critical", 999999):
            status = "CRITICAL"
        elif elapsed >= threshold.get("warn", 999999):
            status = "WARN"

        entry = {"operation": op, "elapsed": elapsed, "status": status}
        report["operations"].append(entry)

        if status in ("WARN", "CRITICAL", "ABORT"):
            report["alerts"].append(f"{status}: {op} ({elapsed:.1f}s)")
            report["recommendations"].extend(SOLUTIONS.get(op, []))

    return report


# ─── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "netlify":
            watch_netlify_build()

        elif cmd == "engine" and len(sys.argv) > 2:
            success = run_engine_with_watchdog(sys.argv[2])
            sys.exit(0 if success else 1)

        elif cmd == "demo":
            print("=== Démo Time Watchdog ===\n")
            ops = [
                ("netlify_build", 45),
                ("npm_build", 130),
                ("engine_validation", 3),
                ("wave_complete", 720),
            ]
            results = {}
            for op, fake_elapsed in ops:
                results[op] = {"elapsed": fake_elapsed}
                t = THRESHOLDS.get(op, {})
                status = "OK"
                if fake_elapsed >= t.get("critical", 99999):
                    status = "CRITICAL"
                elif fake_elapsed >= t.get("warn", 99999):
                    status = "WARN"
                icon = {"OK": "✓", "WARN": "⚠️", "CRITICAL": "🔴"}.get(status, "?")
                print(f"{icon}  {op}: {fake_elapsed}s → {status}")

            report = generate_report(results)
            print(f"\n📋  Alertes : {len(report['alerts'])}")
            for alert in report["alerts"]:
                print(f"   • {alert}")

            if report["recommendations"]:
                print(f"\n💡  Recommandations :")
                seen = set()
                for rec in report["recommendations"]:
                    if rec not in seen:
                        print(f"   → {rec}")
                        seen.add(rec)
        else:
            print("Usage: python3 time-watchdog-agent.py [netlify|engine <path>|demo]")
    else:
        print("Usage: python3 time-watchdog-agent.py [netlify|engine <path>|demo]")
        print("\nSeuils configurés:")
        for op, t in THRESHOLDS.items():
            print(f"  {op:<25} warn={t['warn']}s  critical={t['critical']}s  abort={t['abort']}s")
