#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Veille marché & opportunités — radar continu.
=============================================
Surveille l'émergence de frustrations / besoins non satisfaits (Reddit, forums, presse)
pour adapter vite les projets. Gère data/market_opportunities.json :
  - affiche le radar trié par priorité,
  - SIGNALE les opportunités 'nouveau' non encore traitées (à instruire),
  - rappelle les requêtes de veille à relancer (cadence).

HONNÊTETÉ : la collecte web réelle nécessite un accès réseau (Exa/recherche), fait
lors d'une passe de veille ; ce script gère et priorise le radar. Les signaux inscrits
sont datés et sourcés (jamais inventés).

Usage :
  python3 scripts/market_watch.py             # affiche le radar + ce qui est à traiter
  python3 scripts/market_watch.py --json      # sortie JSON (pour la plateforme)
"""
from __future__ import annotations
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RADAR = os.path.join(ROOT, "data", "market_opportunities.json")

# Requêtes de veille à relancer périodiquement (méthode reproductible).
REQUETES_VEILLE = [
    "reddit r/belgium nouvelle obligation entreprise frustration",
    "AI Act PME confusion deadline 2026 unmet need",
    "Peppol e-facturation indépendant quel outil choisir avis",
    "GDPR NIS2 CSRD trop cher PME forum plainte",
    "entrepreneurs wallons bruxellois complexité administrative 2026",
    "comptables fiduciaires charge conformité clients PME",
]
PRIO = {"haute": 0, "moyenne": 1, "basse": 2}


def charger() -> dict:
    try:
        return json.load(open(RADAR, encoding="utf-8"))
    except Exception:
        return {"opportunites": []}


def synthese(d: dict) -> dict:
    opp = d.get("opportunites", [])
    a_traiter = [o for o in opp if o.get("statut") in ("nouveau", "en_cours")]
    nouveaux = [o for o in opp if o.get("statut") == "nouveau"]
    verdict = "ALERTE" if nouveaux else "OK"
    return {
        "total": len(opp), "nouveaux": len(nouveaux), "a_traiter": len(a_traiter),
        "verdict": verdict,
        "top_a_traiter": [
            {"id": o["id"], "priorite": o.get("priorite"), "opportunite": o.get("opportunite")}
            for o in sorted(a_traiter, key=lambda x: PRIO.get(x.get("priorite"), 9))
        ],
    }


def main() -> int:
    d = charger()
    s = synthese(d)
    if "--json" in sys.argv:
        print(json.dumps(s, ensure_ascii=False))
        return 0

    print("═══ VEILLE MARCHÉ & OPPORTUNITÉS ═══")
    print(f"  Radar : {s['total']} opportunités · 🆕 nouveau {s['nouveaux']} · à traiter {s['a_traiter']}")
    for o in sorted(d.get("opportunites", []), key=lambda x: PRIO.get(x.get("priorite"), 9)):
        flag = "🆕" if o.get("statut") == "nouveau" else ("⏳" if o.get("statut") == "en_cours" else "✓")
        print(f"  {flag} [{o.get('priorite',''):<8}] {o['id']:<22} {o.get('projet','')}")
        print(f"      → {o.get('opportunite','')[:90]}")
    print(f"\n  Verdict : {s['verdict']}" + (f" — {s['nouveaux']} opportunité(s) à instruire" if s['nouveaux'] else ""))
    print("\n  Requêtes de veille à relancer (passe web) :")
    for q in REQUETES_VEILLE:
        print(f"    · {q}")
    print(f"\n  → Radar : {os.path.relpath(RADAR, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
