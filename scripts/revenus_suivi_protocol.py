#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Suivi des revenus — rend data/governance/revenus_suivi.json en rapport suivable."""
import json, pathlib
from datetime import date
GOV = pathlib.Path(__file__).resolve().parent.parent / "data" / "governance"
SRC = GOV / "revenus_suivi.json"; OUT = GOV / "revenus_suivi.md"
EMO = {"a_faire":"⬜","en_cours":"🟨","fait":"✅"}
def construire():
    d = json.loads(SRC.read_text(encoding="utf-8"))
    et = d.get("etapes", [])
    faits = sum(1 for e in et if e.get("etat")=="fait")
    L=["# 💶 Suivi des revenus — à la trace","",
       f"*Généré le {date.today().isoformat()}. Avancement : {faits}/{len(et)} étapes faites. "
       "Aucun revenu garanti : on mesure et on ajuste.*","",
       "| # | Étape | Qui | Indicateur | État |","|---|---|---|---|---|"]
    for e in et:
        L.append(f"| {e['n']} | {e['etape']} | {e['qui']} | {e['indicateur']} | {EMO.get(e['etat'],e['etat'])} |")
    OUT.write_text("\n".join(L)+"\n",encoding="utf-8"); return faits,len(et)
if __name__=="__main__":
    f,t=construire(); print("═══ SUIVI DES REVENUS ═══"); print(f"  {f}/{t} étapes faites → {OUT}"); print("✓ Suivi à jour.")
