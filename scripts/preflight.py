#!/usr/bin/env python3
"""
preflight.py — Vérification Avant Déploiement CaelumSwarm™
═══════════════════════════════════════════════════════════
Une seule commande qui enchaîne tous les gardes du projet AVANT de pousser
ou déployer. Si un contrôle CRITIQUE échoue, le preflight échoue (code ≠ 0).

Contrôles enchaînés :
  1. branch_guard      — collision de branche (autre session ?)
  2. build_guard       — patterns d'erreurs de build connus
  3. dependency_scanner — licences interdites + vulnérabilités

Usage :
  python3 scripts/preflight.py            # tous les contrôles
  python3 scripts/preflight.py --strict   # les alertes font aussi échouer
  python3 scripts/preflight.py --skip branch   # ignorer un contrôle
"""

import sys
import subprocess
import argparse
from datetime import datetime, timezone

CHECKS = [
    {"id": "branch", "label": "Garde anti-collision de branche",
     "cmd": ["python3", "scripts/branch_guard.py", "--check", "--quiet"], "critical": True},
    {"id": "build",  "label": "Build Guard (patterns d'erreurs)",
     "cmd": ["python3", "scripts/build_guard.py", "--scan"], "critical": True},
    {"id": "deps",   "label": "Scan sécurité des dépendances",
     "cmd": ["python3", "scripts/dependency_scanner.py", "--scan"], "critical": True},
    {"id": "site",   "label": "Gardien de cohérence du site (marque, contenu)",
     "cmd": ["python3", "scripts/site_guard.py", "--scan", "--quiet"], "critical": True},
]


def run_check(check, strict):
    cmd = list(check["cmd"])
    if check["id"] == "deps" and strict:
        cmd.append("--strict")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def main():
    ap = argparse.ArgumentParser(description="Preflight CaelumSwarm™")
    ap.add_argument("--strict", action="store_true", help="Les alertes non bloquantes font aussi échouer")
    ap.add_argument("--skip", action="append", default=[], help="ID de contrôle à ignorer (branch/build/deps)")
    args = ap.parse_args()

    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║       PREFLIGHT — Vérification avant déploiement            ║")
    print(f"║       {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC                                 ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    results = []
    for check in CHECKS:
        if check["id"] in args.skip:
            print(f"\n  ⏭️  {check['label']} — IGNORÉ")
            continue
        print(f"\n  ▶ {check['label']}…")
        rc, out, err = run_check(check, args.strict)
        ok = rc == 0
        # Dernière ligne utile de la sortie
        summary = ""
        if out:
            lines = [l for l in out.split("\n") if l.strip()]
            summary = lines[-1] if lines else ""
        icon = "✅" if ok else "🛑"
        print(f"  {icon} {'OK' if ok else 'ÉCHEC'}  {summary[:70]}")
        if not ok and err:
            print(f"     ⚠️  {err[:120]}")
        results.append((check, ok))

    print("\n" + "─" * 64)
    failed = [c for c, ok in results if not ok]
    critical_failed = [c for c, ok in results if not ok and c["critical"]]
    passed = sum(1 for _, ok in results if ok)
    print(f"  Résultat : {passed}/{len(results)} contrôles OK")
    if critical_failed:
        print(f"  🛑 DÉPLOIEMENT BLOQUÉ — {len(critical_failed)} contrôle(s) critique(s) en échec :")
        for c in critical_failed:
            print(f"     • {c['label']}  →  python3 {' '.join(c['cmd'][1:2])}")
    else:
        print("  ✅ TOUT EST SÛR — déploiement autorisé.")
    print("─" * 64 + "\n")

    sys.exit(1 if critical_failed else 0)


if __name__ == "__main__":
    main()
