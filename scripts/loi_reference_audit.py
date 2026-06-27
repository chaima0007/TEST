#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit des RÉFÉRENCES LÉGALES — chaque réponse doit citer une vraie loi écrite et en vigueur.

Vérifie que le champ reference_legale de chaque fait désigne un instrument légal
concret (loi, Code, décret, arrêté, règlement, Constitution, directive…),
idéalement avec un article ou une date.

Honnête : on mesure la PRÉCISION de la référence (pas une preuve absolue de
mise en vigueur — c'est la source officielle liée qui fait foi).

Sortie : data/governance/loi_reference_report.md
"""
import json
import glob
import os
import re
import pathlib
from datetime import date

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
DATA = REPO / "data" / "belgium"
OUT = REPO / "data" / "governance" / "loi_reference_report.md"

INSTRUMENTS = re.compile(
    r"\b(loi|code|décret|decret|decreet|woninghuurdecreet|wooncode|arrêté|arrete|"
    r"ordonnance|règlement|reglement|constitution|directive|RGPD|convention|"
    r"statut social|arrêté royal)\b", re.IGNORECASE)
PRECIS = re.compile(r"art\.|article|\b1[89]\d{2}\b|\b20\d{2}\b")  # article ou année


def construire():
    vagues = []
    total = concret = avec_article = 0
    for fp in sorted(glob.glob(str(DATA / "*.json"))):
        if os.path.basename(fp).startswith("_"):
            continue
        d = json.loads(pathlib.Path(fp).read_text(encoding="utf-8"))
        for f in d.get("faits", []):
            total += 1
            ref = f.get("reference_legale", "") or ""
            a_instrument = bool(INSTRUMENTS.search(ref))
            a_precis = bool(PRECIS.search(ref))
            if a_instrument:
                concret += 1
            if a_precis:
                avec_article += 1
            if not a_instrument:
                vagues.append((os.path.basename(fp), f.get("id"), ref[:80]))

    pct = round(100 * concret / total) if total else 0
    L = []
    L.append("# ⚖️ Audit des références légales")
    L.append("")
    L.append(f"*Généré le {date.today().isoformat()}. Chaque réponse doit citer une loi écrite et en vigueur.*")
    L.append("")
    L.append(f"**{total} réponses · {concret} citent un instrument légal concret ({pct}%) · "
             f"{avec_article} avec article/année.**")
    L.append("")
    if vagues:
        L.append("## ⚠️ Références trop vagues (à préciser avec une vraie loi)")
        for fichier, fid, ref in vagues:
            L.append(f"- {fichier} / {fid} : « {ref} »")
    else:
        L.append("## ✅ Toutes les réponses citent un instrument légal concret.")
    L.append("")
    L.append("> Rappel : la source officielle liée (Justel, administration) fait foi pour la mise en vigueur.")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    return total, concret, pct, len(vagues), vagues


if __name__ == "__main__":
    total, concret, pct, nb_vagues, vagues = construire()
    print("═══ AUDIT DES RÉFÉRENCES LÉGALES ═══")
    print(f"  Réponses : {total} | avec loi concrète : {concret} ({pct}%) | vagues : {nb_vagues}")
    for fichier, fid, ref in vagues[:30]:
        print(f"   ⚠️ {fichier}/{fid}: {ref}")
    print(f"  → {OUT}")
