#!/usr/bin/env python3
"""
croissance_protocol.py — Pilotage stratégique de la croissance (P-CROISSANCE).

Couche de SYNTHÈSE (ne duplique pas les entrées) : lit les opportunités et calcule un
« score de levier » pour décider OÙ calibrer la flotte en priorité. Vérifie aussi un garde-fou
de scalabilité (ne pas pousser la croissance si la plateforme est saturée).

  score_levier = (impact × probabilité × scalabilité) / effort

Honnête : aide à la décision, scores estimés (1-5), aucun revenu promis.

Usage : python3 scripts/croissance_protocol.py
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "data", "governance", "croissance_opportunites.json")
SCAL = os.path.join(BASE, "data", "scalability_report.json")
OUT = os.path.join(BASE, "data", "governance", "croissance_report.json")


def charger(path, defaut):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return defaut


def main():
    conf = charger(SRC, None)
    if not conf or not conf.get("opportunites"):
        print("⛔ Pas d'opportunités à piloter (croissance_opportunites.json).")
        return 1

    classees = []
    for o in conf["opportunites"]:
        eff = max(1, o.get("effort", 1))
        score = round(o.get("impact", 0) * o.get("probabilite", 0) * o.get("scalabilite", 0) / eff, 1)
        classees.append({**o, "score_levier": score})
    classees.sort(key=lambda x: x["score_levier"], reverse=True)

    # Garde-fou scalabilité : si la plateforme est en surcharge, consolider d'abord.
    scal = charger(SCAL, {})
    verdict = scal.get("verdict_global", "OK")
    gate = "✅ feu vert" if verdict != "CRITIQUE" else "🔴 consolider la scalabilité AVANT de pousser"

    print("═══ PILOTAGE STRATÉGIQUE DE LA CROISSANCE (score de levier) ═══")
    print(f"  Garde-fou scalabilité : {gate}")
    print(f"  {'Opportunité':40s} {'levier':>7}")
    for c in classees:
        print(f"  {c['nom'][:40]:40s} {c['score_levier']:>7}")
    top = [c["nom"] for c in classees[:3]]
    print(f"  → Calibrer la flotte sur : {', '.join(top)}")

    json.dump({"verdict_scalabilite": verdict, "classement": classees, "top3": top},
              open(OUT, "w"), ensure_ascii=False, indent=2)
    print(f"  → rapport : data/governance/croissance_report.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
