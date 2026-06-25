#!/usr/bin/env python3
"""
BALAYAGE COMPLET DE FIABILITÉ — exécute TOUS les moteurs du swarm
=================================================================
Pour chaque swarm/intelligence/*_engine.py :
  - l'exécute (python3 fichier.py) : valide la syntaxe, les imports et,
    pour les wave engines, les assertions __main__.
Un moteur est FIABLE s'il se termine avec un code retour 0.

Sortie : compteurs PASS / FAIL + liste détaillée des échecs.
Code retour 0 si 100% fiable, 1 sinon (CI-friendly).
Usage : python3 scripts/full_engine_sweep.py [--workers N]
"""
from __future__ import annotations
import argparse, concurrent.futures as cf, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENG = os.path.join(ROOT, "swarm", "intelligence")
REPORT = os.path.join(ROOT, "data", "full_engine_sweep_report.json")


def run_one(path):
    try:
        p = subprocess.run([sys.executable, path], capture_output=True,
                           text=True, timeout=30, cwd=os.path.join(ROOT, "swarm"))
        if p.returncode == 0:
            return (path, True, "")
        tail = (p.stderr or p.stdout).strip().splitlines()[-1:] or [""]
        return (path, False, tail[0][:140])
    except subprocess.TimeoutExpired:
        return (path, False, "timeout>30s")
    except Exception as e:  # pragma: no cover
        return (path, False, f"{type(e).__name__}: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    files = sorted(os.path.join(ENG, f) for f in os.listdir(ENG)
                   if f.endswith("_engine.py"))
    print(f"Balayage de {len(files)} moteurs (workers={args.workers})...")

    passed, failed = 0, []
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for path, ok, err in ex.map(run_one, files):
            if ok:
                passed += 1
            else:
                failed.append({"engine": os.path.basename(path), "error": err})

    summary = {
        "total": len(files), "passed": passed, "failed": len(failed),
        "reliability_pct": round(passed / max(len(files), 1) * 100, 2),
        "failures": failed,
    }
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("=" * 60)
    print(f"  Total moteurs : {summary['total']}")
    print(f"  ✓ FIABLES     : {passed}")
    print(f"  ✗ ÉCHECS      : {len(failed)}")
    print(f"  Fiabilité     : {summary['reliability_pct']}%")
    if failed:
        print("\n── ÉCHECS ──")
        for f in failed[:50]:
            print(f"  ✗ {f['engine']} :: {f['error']}")
    print("=" * 60)
    print(f"Rapport : {REPORT}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
