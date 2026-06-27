#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expertise rentabilité par domaine — rend data/governance/rentabilite.json
en rapport lisible (data/governance/rentabilite_report.md).

Honnête : évaluation qualitative (demande, concurrence, pistes de revenus),
sans chiffre € inventé.
"""
import json
import pathlib
from datetime import date

HERE = pathlib.Path(__file__).resolve().parent
GOV = HERE.parent / "data" / "governance"
SRC = GOV / "rentabilite.json"
OUT = GOV / "rentabilite_report.md"


def construire():
    d = json.loads(SRC.read_text(encoding="utf-8"))
    L = ["# 💶 Expertise — rentabilité par domaine", "",
         f"*Généré le {date.today().isoformat()}. Évaluation qualitative honnête, sans chiffre inventé.*", "",
         f"**Modèle global :** {d.get('modele_global','')}", "",
         "| Domaine | Demande | Concurrence | Potentiel direct | Verdict |",
         "|---|---|---|---|---|"]
    for x in d.get("domaines", []):
        L.append(f"| {x['domaine']} | {x['demande']} | {x['concurrence']} | {x['potentiel']} | {x['verdict']} |")
    L += ["", "## Pistes de revenus par domaine", ""]
    for x in d.get("domaines", []):
        L.append(f"- **{x['domaine']}** : " + " · ".join(x.get("pistes_revenus", [])))
    L += ["", "## Synthèse du directeur", "", d.get("synthese_directeur", "")]
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    return len(d.get("domaines", []))


if __name__ == "__main__":
    n = construire()
    print("═══ EXPERTISE RENTABILITÉ ═══")
    print(f"  Domaines analysés : {n}")
    print(f"  → {OUT}")
    print("✓ Expertise rentabilité générée (qualitative, honnête).")
