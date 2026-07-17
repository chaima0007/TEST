#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulation de revenus — Stratégie grands comptes Caelum.
========================================================
Monte Carlo sur 3 ans, 3 scénarios (Prudent / Base / Ambitieux), 3 segments.
Objectif : chiffrer honnêtement le potentiel de rentabilité (jusqu'au million d'ARR).

HONNÊTETÉ : ce sont des PROJECTIONS sous hypothèses explicites, PAS des résultats acquis.
Hypothèses ancrées sur les études internes (ETUDE_MARCHE_CAELUM / ETUDE_PRIX_CAELUM) :
  - marché PME Belgique ~1,186,099 (Statbel) ; ~3,728 cabinets (ITAA) ;
  - grandes entreprises soumises CSRD/DORA/NIS2 : quelques milliers en Belgique.
Les taux de pénétration sont volontairement prudents et bornés.

Usage : python3 scripts/revenue_simulation_grands_comptes.py [--n 100000]
Sortie : data/revenue_projection.json
"""
from __future__ import annotations
import json, os, sys, random
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "revenue_projection.json")

# Marché adressable (TAM) par segment — bornes prudentes.
MARCHE = {
    "grands_comptes": 3000,    # grandes entreprises BE soumises CSRD/DORA/NIS2
    "mid_market": 15000,       # ETI / moyennes entreprises
    "via_fiduciaires": 3728,   # cabinets ITAA = canal indirect (marque blanche)
}
# ACV (valeur annuelle du contrat) par segment : (min, max) en €.
ACV = {
    "grands_comptes": (18000, 60000),
    "mid_market": (3000, 12000),
    "via_fiduciaires": (5000, 30000),  # par cabinet (qui regroupe plusieurs PME)
}
# Pénétration cumulée visée par scénario et par an (% du TAM).
PENETRATION = {
    "Prudent":   {1: 0.001, 2: 0.005, 3: 0.012},
    "Base":      {1: 0.002, 2: 0.010, 3: 0.025},
    "Ambitieux": {1: 0.004, 2: 0.018, 3: 0.045},
}
CHURN = 0.10           # attrition annuelle
MARGE_BRUTE = 0.80     # SaaS + conseil outillé


def simuler(scenario: str, n: int) -> dict:
    rng = random.Random(hash(scenario) & 0xFFFFFFFF)
    annees = {}
    for an in (1, 2, 3):
        arr_samples = []
        for _ in range(n // 3):
            arr = 0.0
            for seg, tam in MARCHE.items():
                pen = PENETRATION[scenario][an] * rng.uniform(0.7, 1.3)  # bruit
                clients = tam * pen * (1 - CHURN * (an - 1) * 0.3)
                lo, hi = ACV[seg]
                acv = rng.uniform(lo, hi)
                arr += clients * acv
            arr_samples.append(arr)
        arr_samples.sort()
        annees[an] = {
            "p10": round(arr_samples[int(len(arr_samples) * 0.10)]),
            "median": round(arr_samples[int(len(arr_samples) * 0.50)]),
            "p90": round(arr_samples[int(len(arr_samples) * 0.90)]),
            "marge_brute_median": round(arr_samples[int(len(arr_samples) * 0.50)] * MARGE_BRUTE),
        }
    return annees


def main() -> int:
    n = 100_000
    if "--n" in sys.argv:
        try:
            n = int(sys.argv[sys.argv.index("--n") + 1])
        except Exception:
            pass

    resultats = {sc: simuler(sc, n) for sc in PENETRATION}

    rapport = {
        "genere_le": datetime.now(timezone.utc).isoformat(),
        "monte_carlo_n": n,
        "devise": "EUR",
        "hypotheses": {
            "marche_adressable": MARCHE, "acv_eur": ACV,
            "penetration_par_scenario": PENETRATION, "churn_annuel": CHURN, "marge_brute": MARGE_BRUTE,
        },
        "projections_arr": resultats,
        "avertissement": "PROJECTIONS sous hypothèses explicites — pas des résultats garantis. "
                         "À réviser avec les vrais coûts, prix et taux de conversion observés.",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(rapport, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    def m(x):
        return f"{x/1_000_000:.2f} M€" if x >= 1_000_000 else f"{x/1000:.0f} k€"

    print("═══ PROJECTION DE REVENUS — GRANDS COMPTES (Monte Carlo) ═══")
    for sc, an in resultats.items():
        print(f"\n  {sc} :")
        for y in (1, 2, 3):
            d = an[y]
            print(f"    An {y} — ARR médian {m(d['median'])}  (p10 {m(d['p10'])} · p90 {m(d['p90'])}) · "
                  f"marge brute {m(d['marge_brute_median'])}")
    print(f"\n  → {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
