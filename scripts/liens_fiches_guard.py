#!/usr/bin/env python3
"""
liens_fiches_guard.py — GARDE : aucun lien mort vers les fiches.
================================================================================
Scanne toutes les pages de l'app laloiavecmoi/ pour les références en dur vers
des fiches (`/loi/<module>` et `fiche: "<module>"`) et vérifie que chaque module
référencé existe réellement (champ `module` des JSON de data/belgium).

Pourquoi : le routage /loi/[domaine] matche sur le CHAMP `module`, pas sur le nom
de fichier — 11 fiches ont un nom de fichier ≠ module (ex. bail_wallonie.json →
module bail_residence_principale_wallonie). Un lien écrit de tête casse en silence.

Sortie : code 1 si lien mort (bloque avant commit), 0 sinon.
Usage  : python3 scripts/liens_fiches_guard.py
"""
import json
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "laloiavecmoi", "app")
DATA = os.path.join(ROOT, "laloiavecmoi", "data", "belgium")


def modules_reels():
    mods = set()
    for f in glob.glob(os.path.join(DATA, "*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        try:
            m = json.load(open(f, encoding="utf-8")).get("module")
        except Exception:
            continue
        if m:
            mods.add(m)
    return mods


def main():
    mods = modules_reels()
    morts = []
    for tsx in glob.glob(os.path.join(APP, "**", "*.tsx"), recursive=True):
        src = open(tsx, encoding="utf-8").read()
        rel = os.path.relpath(tsx, ROOT)
        for m in re.finditer(r"/loi/([a-z0-9_]+)", src):
            slug = m.group(1)
            if slug != "domaine" and slug not in mods:  # [domaine] = segment dynamique
                morts.append((rel, f"/loi/{slug}"))
        for m in re.finditer(r'fiche:\s*"([a-z0-9_]+)"', src):
            if m.group(1) not in mods:
                morts.append((rel, f'fiche:"{m.group(1)}"'))

    print("═══ GARDE LIENS FICHES ═══")
    print(f"  Modules réels : {len(mods)} | pages scannées : "
          f"{len(glob.glob(os.path.join(APP, '**', '*.tsx'), recursive=True))}")
    if morts:
        print(f"  ❌ {len(morts)} lien(s) mort(s) :")
        for rel, lien in sorted(set(morts)):
            print(f"     {rel} → {lien}")
        sys.exit(1)
    print("  ✅ Aucun lien mort — toutes les références pointent vers des modules existants.")


if __name__ == "__main__":
    main()
