#!/usr/bin/env python3
"""
branch_guard.py — Garde Anti-Collision de Branche CaelumSwarm™
═══════════════════════════════════════════════════════════════
Empêche deux sessions Claude d'écraser mutuellement leur travail sur la
même branche. À lancer AVANT tout commit/push (et idéalement au démarrage).

Compare l'état local et distant de la branche courante et classe la situation :

  ✅ SYNC      local == origin            → écriture sûre
  ✅ AHEAD     local devant origin        → commits non poussés, normal
  🛑 BEHIND    origin devant local        → une autre session a poussé → STOP
  🛑 DIVERGED  les deux ont bougé         → collision → STOP
  🛑 SWAPPED   aucune histoire commune    → lignée écrasée → STOP (danger max)

Code retour non-zéro si situation dangereuse → intégrable en pre-commit / protocole.

Usage :
  python3 scripts/branch_guard.py --check          # vérifie (lecture seule)
  python3 scripts/branch_guard.py --check --quiet   # sortie minimale pour CI/hook
  python3 scripts/branch_guard.py --guard           # alias de --check (gate avant écriture)
"""

import sys
import json
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

GUARD_LOG = Path("data/branch_guard_log.json")
EXPECTED_BRANCH = "claude/swarm-50-agent-architecture-3l6cno"


def _git(*args, timeout=30):
    try:
        out = subprocess.run(["git", *args], capture_output=True, text=True, timeout=timeout)
        return out.returncode, out.stdout.strip(), out.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def _log(result: dict):
    log = []
    if GUARD_LOG.exists():
        try:
            log = json.loads(GUARD_LOG.read_text())
        except Exception:
            log = []
    log.append(result)
    if len(log) > 300:
        log = log[-300:]
    GUARD_LOG.parent.mkdir(exist_ok=True)
    GUARD_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))


def check_branch(fetch: bool = True) -> dict:
    """Analyse l'état de synchronisation de la branche courante."""
    rc, branch, _ = _git("rev-parse", "--abbrev-ref", "HEAD")
    if rc != 0:
        return {"status": "ERROR", "safe": False, "detail": "pas un dépôt git"}

    if fetch:
        _git("fetch", "origin", branch, timeout=60)

    rc, local, _ = _git("rev-parse", "HEAD")
    rc2, remote, err2 = _git("rev-parse", f"origin/{branch}")

    # Branche distante absente → première poussée, sûr
    if rc2 != 0:
        return {"status": "NEW_BRANCH", "safe": True, "branch": branch,
                "local": local[:8], "detail": "branche distante inexistante (première poussée)"}

    if local == remote:
        status, safe, detail = "SYNC", True, "local == origin — écriture sûre"
    else:
        # Relations d'ancêtre
        merge_base_rc, base, _ = _git("merge-base", local, remote)
        local_ahead = (base == remote)   # remote est ancêtre de local
        remote_ahead = (base == local)   # local est ancêtre de remote
        no_common = (merge_base_rc != 0 or not base)

        if no_common:
            status, safe, detail = "SWAPPED", False, \
                "AUCUNE histoire commune — la branche distante a été écrasée par une autre lignée !"
        elif local_ahead:
            status, safe, detail = "AHEAD", True, "commits locaux non poussés — normal, push autorisé"
        elif remote_ahead:
            status, safe, detail = "BEHIND", False, \
                "une autre session a poussé des commits — pull AVANT d'écrire (sinon collision)"
        else:
            status, safe, detail = "DIVERGED", False, \
                "local ET origin ont divergé — collision avec une autre session"

    result = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "branch": branch,
        "local": local[:8],
        "remote": remote[:8] if rc2 == 0 else None,
        "status": status,
        "safe": safe,
        "detail": detail,
        "expected_branch_ok": branch == EXPECTED_BRANCH,
    }
    _log(result)
    return result


ICON = {"SYNC": "✅", "AHEAD": "✅", "NEW_BRANCH": "✅",
        "BEHIND": "🛑", "DIVERGED": "🛑", "SWAPPED": "🚨", "ERROR": "❌"}


def print_result(r: dict, quiet: bool):
    if quiet:
        print(f"{ICON.get(r['status'],'?')} {r['status']} — {r['detail']}")
        return
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║       BRANCH GUARD — Anti-Collision CaelumSwarm™          ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    print(f"  Branche : {r.get('branch','?')}")
    print(f"  Local   : {r.get('local','?')}")
    print(f"  Origin  : {r.get('remote','?')}")
    print(f"\n  {ICON.get(r['status'],'?')} {r['status']} — {r['detail']}")
    if not r.get("expected_branch_ok", True):
        print(f"\n  ⚠️  Branche inattendue ! Attendu : {EXPECTED_BRANCH}")
    if not r["safe"]:
        print("\n  ─────────────────────────────────────────────────────────")
        print("  🛑 ÉCRITURE BLOQUÉE — résous d'abord la divergence :")
        if r["status"] == "BEHIND":
            print(f"     git pull --rebase origin {r.get('branch')}")
        elif r["status"] in ("DIVERGED", "SWAPPED"):
            print("     ⚠️  Une autre session travaille sur cette branche.")
            print("     1. Sauvegarde l'autre lignée :")
            print(f"        git push origin origin/{r.get('branch')}:refs/heads/<nouvelle-branche>")
            print("     2. Réaligne ou choisis quelle lignée conserver.")
        print("  ─────────────────────────────────────────────────────────")
    print()


def main():
    ap = argparse.ArgumentParser(description="Branch Guard — anti-collision CaelumSwarm™")
    ap.add_argument("--check", action="store_true", help="Vérifier la synchronisation")
    ap.add_argument("--guard", action="store_true", help="Alias de --check (gate avant écriture)")
    ap.add_argument("--quiet", action="store_true", help="Sortie minimale (hook/CI)")
    ap.add_argument("--no-fetch", action="store_true", help="Ne pas fetch (utilise l'état local connu)")
    args = ap.parse_args()

    if args.check or args.guard:
        r = check_branch(fetch=not args.no_fetch)
        print_result(r, args.quiet)
        sys.exit(0 if r["safe"] else 1)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
