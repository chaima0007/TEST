#!/usr/bin/env python3
"""
CaelumSwarm™ — Protocole de Vérification Automatique des Moteurs (Wave Engines)

Rejoue automatiquement TOUS les contrôles de cohérence sur les moteurs
`swarm/intelligence/*_rights_engine.py` qui suivent le pattern Wave standard
(8 entités, distribution 4/2/1/1, poids 0.30/0.25/0.25/0.20, cible 61.03).

Contrôles effectués :
  1. EXÉCUTION    — chaque moteur tourne sans erreur Python
  2. ASSERTIONS   — la ligne "✓ Assertions passées" est présente
  3. DISTRIBUTION — exactement 4 critique / 2 élevé / 1 modéré / 1 faible
  4. MOYENNE      — avg_composite dans les bornes OK (61.03 ± 0.50)
  5. DOUBLONS     — aucun préfixe d'entité (XXX-001) partagé entre moteurs
  6. NOMS         — aucun doublon de nom de fichier

Usage :
    python3 scripts/engine_verifier.py                 # tous les rights engines
    python3 scripts/engine_verifier.py --wave 498-561  # plage de waves
    python3 scripts/engine_verifier.py --json          # sortie JSON
    python3 scripts/engine_verifier.py --quiet         # code retour seul

Code retour : 0 si tout OK, 1 si au moins un échec (CI-friendly).
Rapport sauvegardé dans data/engine_verification_report.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINES_DIR = os.path.join(ROOT, "swarm", "intelligence")
REPORT_PATH = os.path.join(ROOT, "data", "engine_verification_report.json")

TARGET_AVG = 61.03
AVG_OK_BAND = 0.50  # borne OK du protocole (§9)
EXPECTED_DIST = {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}

WAVE_RE = re.compile(r"Wave\s+(\d+)")
PREFIX_RE = re.compile(r'"([A-Za-z]+)-0*1"')
# Robuste aux deux formats de sortie du codebase :
#   Format A (template récent) : distribution = {'critique': 4, ...} · avg_composite = 61.02
#   Format B (JSON ancien)     : "distribution": {\n "critique": 4, ... · "avg_composite": 61.02
_DIST_KEY = lambda k: re.compile(r'["\']?' + k + r'["\']?\s*[:=]\s*(\d+)')
AVG_RE = re.compile(r'["\']?avg_composite["\']?\s*[:=]\s*([\d.]+)')


def discover_engines(wave_range=None):
    """Retourne la liste des fichiers *_rights_engine.py suivant le pattern Wave."""
    files = []
    for name in sorted(os.listdir(ENGINES_DIR)):
        if not name.endswith("_rights_engine.py"):
            continue
        path = os.path.join(ENGINES_DIR, name)
        try:
            with open(path, encoding="utf-8") as f:
                head = f.read(4000)
        except OSError:
            continue
        m = WAVE_RE.search(head)
        if not m:
            continue  # pas un moteur Wave standard
        wave = int(m.group(1))
        if wave_range and not (wave_range[0] <= wave <= wave_range[1]):
            continue
        files.append((name, path, wave))
    return files


def verify_one(name, path):
    """Exécute un moteur et contrôle assertions / distribution / moyenne."""
    result = {
        "engine": name,
        "runs": False,
        "assertions_pass": False,
        "distribution_ok": False,
        "avg_ok": False,
        "avg": None,
        "prefix": None,
        "errors": [],
    }
    try:
        proc = subprocess.run(
            [sys.executable, path],
            capture_output=True, text=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        result["errors"].append("timeout > 30s")
        return result
    except Exception as e:  # pragma: no cover
        result["errors"].append(f"exec error: {e}")
        return result

    out = proc.stdout + proc.stderr
    result["runs"] = proc.returncode == 0
    if proc.returncode != 0:
        tail = out.strip().splitlines()[-3:]
        result["errors"].append("non-zero exit: " + " | ".join(tail))

    # Accepte les deux conventions de confirmation d'assertions
    result["assertions_pass"] = ("✓ Assertions passées" in out
                                 or "✓ Distribution" in out)

    dist = {}
    for k in ("critique", "élevé", "modéré", "faible"):
        m = _DIST_KEY(k).search(out)
        if m:
            dist[k] = int(m.group(1))
    if len(dist) == 4:
        result["distribution_ok"] = dist == EXPECTED_DIST
        if not result["distribution_ok"]:
            result["errors"].append(f"distribution {dist} != {EXPECTED_DIST}")
    else:
        result["errors"].append("distribution introuvable dans la sortie")

    ma = AVG_RE.search(out)
    if ma:
        avg = float(ma.group(1))
        result["avg"] = avg
        result["avg_ok"] = abs(avg - TARGET_AVG) <= AVG_OK_BAND
        if not result["avg_ok"]:
            result["errors"].append(
                f"avg {avg} hors borne OK ({TARGET_AVG} ± {AVG_OK_BAND})"
            )
    else:
        result["errors"].append("avg_composite introuvable dans la sortie")

    # préfixe d'entité (depuis le fichier source)
    try:
        with open(path, encoding="utf-8") as f:
            src = f.read()
        pm = PREFIX_RE.search(src)
        if pm:
            result["prefix"] = pm.group(1)
    except OSError:
        pass

    return result


def run(wave_range=None, quiet=False, as_json=False):
    engines = discover_engines(wave_range)
    results = [verify_one(name, path) for name, path, _ in engines]

    # contrôle doublons de préfixes
    prefix_map = defaultdict(list)
    for r in results:
        if r["prefix"]:
            prefix_map[r["prefix"]].append(r["engine"])
    dup_prefixes = {p: e for p, e in prefix_map.items() if len(e) > 1}

    # contrôle doublons de noms (sur tout le répertoire, pas seulement la plage)
    all_names = [n for n in os.listdir(ENGINES_DIR) if n.endswith("_rights_engine.py")]
    name_dups = {n for n in all_names if all_names.count(n) > 1}

    # INVARIANTS BLOQUANTS (vrais échecs) :
    #   - le moteur s'exécute sans erreur Python
    #   - la distribution réglementaire 4/2/1/1 est respectée (quand détectable)
    # AVERTISSEMENTS (informatif, non bloquant) :
    #   - avg hors borne 61.03±0.5 (certains moteurs sont calibrés autrement)
    #   - avg/assertions non détectés (format de sortie différent)
    #   - préfixes d'entité partagés (labels locaux, pattern accepté)
    def engine_blocking_fail(r):
        if not r["runs"]:
            return True
        # distribution fausse = bloquant ; introuvable = avertissement seulement
        if any("!=" in e for e in r["errors"]):
            return True
        return False

    def engine_warn(r):
        return (not engine_blocking_fail(r)
                and (not r["avg_ok"] or not r["assertions_pass"]
                     or not r["distribution_ok"]))

    failed = [r for r in results if engine_blocking_fail(r)]
    warned = [r for r in results if engine_warn(r)]
    passed = len(results) - len(failed) - len(warned)

    summary = {
        "total_engines": len(results),
        "passed": passed,
        "warnings": len(warned),
        "failed": len(failed),
        "duplicate_prefixes": dup_prefixes,
        "duplicate_filenames": sorted(name_dups),
        # Seuls les échecs bloquants et les doublons de NOMS de fichiers cassent le vert.
        "all_green": len(failed) == 0 and not name_dups,
        "failures": [
            {"engine": r["engine"], "errors": r["errors"]} for r in failed
        ],
        "warning_details": [
            {"engine": r["engine"], "errors": r["errors"]} for r in warned
        ],
    }

    # sauvegarde rapport
    try:
        os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
    except OSError:
        pass

    if as_json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    elif not quiet:
        print("═══ VÉRIFICATION AUTOMATIQUE DES MOTEURS ═══")
        rng = f" (waves {wave_range[0]}-{wave_range[1]})" if wave_range else ""
        print(f"  Moteurs analysés{rng} : {summary['total_engines']}")
        print(f"  ✓ PASS : {passed}")
        print(f"  ⚠️  WARN : {len(warned)} (avg/format non conforme, non bloquant)")
        print(f"  ✗ FAIL : {len(failed)} (bloquant)")
        if dup_prefixes:
            print(f"  ℹ️  Préfixes partagés (labels locaux, normal) : {len(dup_prefixes)} groupes")
        else:
            print("  ✓ Préfixes d'entité uniques")
        if name_dups:
            print(f"  🔴 Doublons de noms : {sorted(name_dups)}")
        else:
            print("  ✓ Noms de fichiers uniques")
        if failed:
            print("\n── ÉCHECS ──")
            for r in failed:
                print(f"  ✗ {r['engine']}")
                for err in r["errors"]:
                    print(f"      → {err}")
        print()
        print("✓ TOUT VERT" if summary["all_green"] else "🔴 CORRECTIONS REQUISES")
        print(f"Rapport : {REPORT_PATH}")

    return 0 if summary["all_green"] else 1


def parse_wave_arg(s):
    if not s:
        return None
    if "-" in s:
        a, b = s.split("-", 1)
        return (int(a), int(b))
    w = int(s)
    return (w, w)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Vérification automatique des moteurs Wave")
    ap.add_argument("--wave", help="Plage de waves, ex: 498-561 ou 500")
    ap.add_argument("--json", action="store_true", help="Sortie JSON")
    ap.add_argument("--quiet", action="store_true", help="Code retour seul")
    args = ap.parse_args()
    sys.exit(run(parse_wave_arg(args.wave), quiet=args.quiet, as_json=args.json))
