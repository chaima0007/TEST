#!/usr/bin/env python3
"""
success_simulation.py — Simulation de réussite « sur tous les fronts » (Monte-Carlo).

Applique les ÉTUDES DE MARCHÉ (paramètres lus dans data/governance/etudes_synthese.json)
et exécute un GRAND nombre de tirages aléatoires (par défaut 1 000 000 000 = 1 milliard),
en lots vectorisés (numpy) pour rester rapide et économe en mémoire.

Cinq fronts modélisés, chacun avec un critère de réussite explicite :
  1. Caelum — revenu récurrent (MRR ≥ seuil de viabilité)
  2. La Loi Avec Moi — audience (visites mensuelles ≥ objectif)
  3. La Loi Avec Moi — financement (subsides/dons obtenus)
  4. Technique — fiabilité (latence p95 ET uptime dans les cibles)
  5. Contenu — viabilité (≥ seuil)
« Réussite sur tous les fronts » = les 5 critères satisfaits simultanément (tirage strict).

Honnêteté : ce sont des HYPOTHÈSES de modélisation calibrées sur des données sourcées,
pas une prédiction certaine. Les probabilités sont des fréquences observées sur N tirages.

Usage : python3 scripts/success_simulation.py [N] [taille_lot]
"""
import json
import os
import sys
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARAMS = os.path.join(BASE, "data", "governance", "etudes_synthese.json")
OUT_MD = os.path.join(BASE, "data", "governance", "success_simulation_report.md")
OUT_JSON = os.path.join(BASE, "data", "governance", "success_simulation_report.json")


def tri(rng, n, lo, mode, hi):
    return rng.triangular(lo, mode, hi, size=n)


def main():
    N = int(float(sys.argv[1])) if len(sys.argv) > 1 else 1_000_000_000
    BATCH = int(float(sys.argv[2])) if len(sys.argv) > 2 else 2_000_000
    p = json.load(open(PARAMS, encoding="utf-8"))
    C, L, T, K = p["caelum"], p["laloiavecmoi"], p["technique"], p["contenu"]
    tam = C["tam_pme_be"]
    seuils_mrr = C["seuils_mrr_eur_mois"]

    rng = np.random.default_rng()
    fronts = ["caelum_mrr", "llam_audience", "llam_financement", "technique", "contenu"]
    succ = {f: 0 for f in fronts}
    succ_mrr = {s: 0 for s in seuils_mrr}     # par seuil MRR
    tous = 0                                   # réussite sur TOUS les fronts
    somme_mrr = 0.0
    fait = 0

    while fait < N:
        n = min(BATCH, N - fait)

        # 1) Caelum MRR
        pen = tri(rng, n, C["penetration_pct"]["min"], C["penetration_pct"]["mode"], C["penetration_pct"]["max"]) / 100.0
        arpu = tri(rng, n, C["arpu_eur_mois"]["min"], C["arpu_eur_mois"]["mode"], C["arpu_eur_mois"]["max"])
        mrr = pen * tam * arpu
        somme_mrr += float(mrr.sum())
        f_caelum = mrr >= seuils_mrr[0]
        for s in seuils_mrr:
            succ_mrr[s] += int((mrr >= s).sum())

        # 2) LLAM audience
        vis = tri(rng, n, L["visites_mensuelles_maturite"]["min"], L["visites_mensuelles_maturite"]["mode"], L["visites_mensuelles_maturite"]["max"])
        f_aud = vis >= L["objectif_visites"]

        # 3) LLAM financement (proba tirée puis Bernoulli)
        pf = rng.uniform(L["proba_financement"]["min"], L["proba_financement"]["max"], size=n)
        f_fin = rng.random(n) < pf

        # 4) Technique (latence + uptime)
        p95 = rng.normal(T["p95_ms"]["moyenne"], T["p95_ms"]["ecart_type"], size=n)
        up = rng.normal(T["uptime_pct"]["moyenne"], T["uptime_pct"]["ecart_type"], size=n)
        f_tech = (p95 <= T["seuil_p95_ms"]) & (up >= T["seuil_uptime_pct"])

        # 5) Contenu
        via = rng.normal(K["viabilite_pct"]["moyenne"], K["viabilite_pct"]["ecart_type"], size=n)
        f_cont = via >= K["seuil_viabilite_pct"]

        succ["caelum_mrr"] += int(f_caelum.sum())
        succ["llam_audience"] += int(f_aud.sum())
        succ["llam_financement"] += int(f_fin.sum())
        succ["technique"] += int(f_tech.sum())
        succ["contenu"] += int(f_cont.sum())
        tous += int((f_caelum & f_aud & f_fin & f_tech & f_cont).sum())

        fait += n
        if (fait // BATCH) % 50 == 0:
            print(f"  … {fait:,}/{N:,} tirages")

    pct = {f: 100.0 * succ[f] / N for f in fronts}
    pct_tous = 100.0 * tous / N
    mrr_moyen = somme_mrr / N

    labels = {
        "caelum_mrr": f"Caelum — MRR ≥ {seuils_mrr[0]} €/mois (viabilité)",
        "llam_audience": f"La Loi Avec Moi — audience ≥ {L['objectif_visites']:,} visites/mois",
        "llam_financement": "La Loi Avec Moi — financement (subsides/dons) obtenu",
        "technique": f"Technique — p95 ≤ {T['seuil_p95_ms']} ms et uptime ≥ {T['seuil_uptime_pct']} %",
        "contenu": f"Contenu — viabilité ≥ {K['seuil_viabilite_pct']} %",
    }

    Lr = ["# 🎲 Simulation de réussite — tous les fronts (Monte-Carlo)", ""]
    Lr.append(f"> **{N:,} tirages** (lots de {BATCH:,}). Paramètres issus des études de marché (sourcées).")
    Lr.append("> Hypothèses de modélisation — fréquences observées, pas une certitude.")
    Lr.append("")
    Lr.append("## Probabilité de réussite par front")
    for f in fronts:
        jauge = "█" * int(round(pct[f] / 10)) + "░" * (10 - int(round(pct[f] / 10)))
        Lr.append(f"- **{pct[f]:.1f}%** `{jauge}` — {labels[f]}")
    Lr.append("")
    Lr.append("## Détail Caelum (MRR par seuil)")
    for s in seuils_mrr:
        Lr.append(f"- MRR ≥ {s:,} €/mois : **{100.0*succ_mrr[s]/N:.1f}%**")
    Lr.append(f"- MRR moyen simulé : **{mrr_moyen:,.0f} €/mois**")
    Lr.append("")
    Lr.append(f"## 🏆 Réussite simultanée SUR TOUS LES FRONTS : **{pct_tous:.1f}%**")
    Lr.append("")
    Lr.append("> Lecture : chaque front est très probable ; la réussite simultanée stricte est plus exigeante "
              "(produit des probabilités) — c'est le scénario où TOUT réussit en même temps.")
    Lr.append("")
    Lr.append("### Source des paramètres")
    Lr.append("ETUDE_MARCHE_CAELUM.md · ETUDE_PRIX_CAELUM.md · ETUDE_MARCHE_LALOIAVECMOI.md (données Statbel, "
              "RegTech/Legaltech Europe, ITAA, Droits Quotidiens, benchmarks prix). Tests de charge internes.")
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(Lr) + "\n")
    json.dump({"N": N, "pct_par_front": pct, "pct_tous_les_fronts": pct_tous,
               "mrr_moyen_eur_mois": mrr_moyen,
               "mrr_par_seuil_pct": {str(s): 100.0*succ_mrr[s]/N for s in seuils_mrr}},
              open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("═══ SIMULATION DE RÉUSSITE — TOUS LES FRONTS ═══")
    print(f"  Tirages : {N:,}")
    for f in fronts:
        print(f"  {pct[f]:5.1f}%  {labels[f]}")
    print(f"  MRR moyen simulé : {mrr_moyen:,.0f} €/mois")
    print(f"  🏆 Réussite sur TOUS les fronts : {pct_tous:.1f}%")
    print(f"  → rapport : data/governance/success_simulation_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
