#!/usr/bin/env python3
"""
project_valuation_protocol.py — VALORISATION multi-critères des projets (sous protocole).

Honnête : score de POTENTIEL (pas un prix en euros). Lit data/governance/project_valuation.json,
calcule un score pondéré /100 par projet, classe, et produit un rapport.

Sortie : data/governance/valorisation_rapport.md
Usage : python3 scripts/project_valuation_protocol.py
"""
import json

SRC = "data/governance/project_valuation.json"
OUT = "data/governance/valorisation_rapport.md"


def main():
    cfg = json.load(open(SRC, encoding="utf-8"))
    pond = cfg["ponderation"]
    resultats = []
    for p in cfg["projets"]:
        # risque compté à l'envers (5 = pire)
        comp = {
            "valeur_strategique": p["valeur_strategique"] / 5,
            "maturite": p["maturite"] / 5,
            "preuve_fiabilite": p["preuve_fiabilite"] / 5,
            "potentiel_revenu": p["potentiel_revenu"] / 5,
            "risque": (5 - p["risque"]) / 5,
        }
        score = round(sum(comp[k] * pond[k] for k in pond) * 100, 1)
        resultats.append((score, p))
    resultats.sort(reverse=True, key=lambda x: x[0])

    L = ["# 💎 Valorisation des projets (potentiel, sous protocole)", ""]
    L.append(f"*{cfg['note_honnete']} Revu le {cfg['derniere_revue']}.*")
    L.append("")
    L.append("| Rang | Projet | Score /100 | Justification |")
    L.append("|---|---|---|---|")
    for i, (score, p) in enumerate(resultats, 1):
        L.append(f"| {i} | **{p['nom']}** | {score} | {p['justification']} |")
    L.append("")
    L.append("## Lecture")
    meilleur = resultats[0][1]["nom"]
    L.append(f"- Priorité de valeur : **{meilleur}** (score le plus élevé).")
    L.append("- Le score combine valeur stratégique, maturité, fiabilité prouvée, potentiel de revenu et risque (inversé).")
    L.append("- Indicatif : il guide l'effort, il ne fixe pas un prix de marché.")
    L.append("")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    print("═══ VALORISATION DES PROJETS ═══")
    for score, p in resultats:
        print(f"  {score:5.1f}/100  {p['nom']}")
    print(f"  → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
