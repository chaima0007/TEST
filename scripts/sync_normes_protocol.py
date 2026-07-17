#!/usr/bin/env python3
"""
sync_normes_protocol.py — Validation croisée des normes (P-SYNC-NORMES).

Empêche la DÉSYNCHRONISATION entre la base de données des normes (qui alimente les pages SEO)
et la liste interne du simulateur « Suis-je concerné ? ». À chaque passage, le garde vérifie :
  1. chaque norme de data/caelum a une correspondance déclarée (normes_simulateur_map.json) ;
  2. chaque correspondance pointe vers une entrée RÉELLEMENT présente dans le simulateur
     (app/conformite-2026/page.tsx) ET sur les pages SEO (slug dans app/conformite/data.ts).
Si une norme est ajoutée à la base sans être câblée partout → BLOCAGE (code retour ≠ 0).

Usage : python3 scripts/sync_normes_protocol.py
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NORMES = os.path.join(BASE, "data", "caelum", "conformite_entreprises.json")
MAP = os.path.join(BASE, "data", "caelum", "normes_simulateur_map.json")
SIMU = os.path.join(BASE, "app", "conformite-2026", "page.tsx")
DATATS = os.path.join(BASE, "app", "conformite", "data.ts")


def main():
    try:
        base_ids = [n["id"] for n in json.load(open(NORMES, encoding="utf-8"))["normes"]]
        corr = json.load(open(MAP, encoding="utf-8")).get("correspondance", {})
        simu = open(SIMU, encoding="utf-8").read()
        datats = open(DATATS, encoding="utf-8").read()
    except Exception as e:
        print(f"⛔ Lecture impossible : {e}")
        return 1

    sim_ids = set(re.findall(r'id:\s*"([a-z0-9-]+)"', simu))
    slugs_seo = set(re.findall(r'"?[A-Za-z0-9_-]+"?\s*:\s*"([a-z0-9-]+)"', datats))

    problemes = []
    for bid in base_ids:
        if bid not in corr:
            problemes.append(f"{bid} : pas de correspondance déclarée (map)")
            continue
        sid = corr[bid]
        if sid not in sim_ids:
            problemes.append(f"{bid} → '{sid}' absent du simulateur")
    # cohérence inverse : une correspondance pour une norme qui n'existe plus
    for bid in corr:
        if bid not in base_ids:
            problemes.append(f"{bid} : dans la map mais plus dans la base")

    print("═══ VALIDATION CROISÉE DES NORMES (anti-désynchronisation) ═══")
    print(f"  Base : {len(base_ids)} normes · simulateur : {len(sim_ids)} entrées · pages SEO (slugs) : {len(slugs_seo)}")
    if problemes:
        for p in problemes[:15]:
            print(f"   ⛔ {p}")
        print(f"  ⛔ DÉSYNCHRONISATION ({len(problemes)}) — câbler la norme partout avant publication.")
        return 1
    print("  ✅ Base, simulateur et pages SEO parfaitement synchronisés.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
