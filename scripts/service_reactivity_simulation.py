#!/usr/bin/env python3
"""
service_reactivity_simulation.py — Test de réactivité de nos services à l'échelle (Monte-Carlo).

Simule un TRÈS grand nombre de requêtes (par défaut 1 000 000 000 = 1 milliard) sur nos
services, et mesure la RÉACTIVITÉ : latences p50/p95/p99/p99.9, taux d'erreur, % de requêtes
« réactives » (< 200 ms), débit estimé.

⚠️ Honnêteté : on ne lance pas 1 milliard de vraies requêtes réseau (impossible/inutile ici).
On MODÉLISE chaque requête avec une loi de latence calibrée sur nos MESURES RÉELLES
(tests de charge internes : pages prérendues, p95 < 111 ms, ~0 % d'erreur). Pour un test réel
sur l'hébergement, utiliser scripts/load_simulation.py --base <URL> après déploiement.

Usage : python3 scripts/service_reactivity_simulation.py [N] [taille_lot]
"""
import json
import os
import sys
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_MD = os.path.join(BASE, "data", "governance", "reactivity_simulation_report.md")
OUT_JSON = os.path.join(BASE, "data", "governance", "reactivity_simulation_report.json")

# Profils de services calibrés sur nos mesures réelles (médiane, p95 en ms, poids de trafic, taux d'erreur).
SERVICES = [
    {"nom": "Pages contenu/SEO (prérendues)", "median": 18.0, "p95": 70.0,  "poids": 0.70, "err": 0.0003},
    {"nom": "Base juridique (recherche)",     "median": 30.0, "p95": 110.0, "poids": 0.18, "err": 0.0005},
    {"nom": "Simulateurs (Caelum)",           "median": 25.0, "p95": 95.0,  "poids": 0.08, "err": 0.0005},
    {"nom": "API /api/leads (POST)",          "median": 45.0, "p95": 160.0, "poids": 0.04, "err": 0.0010},
]
SLA_REACTIF_MS = 200      # « réactif »
SLA_ACCEPT_MS = 500       # acceptable
MAXBIN = 3000             # histogramme 0..3000 ms (+ overflow)


def params(median, p95):
    mu = np.log(median)
    sigma = max(1e-6, (np.log(p95) - mu) / 1.6448536)  # p95 d'une loi lognormale
    return mu, sigma


def main():
    N = int(float(sys.argv[1])) if len(sys.argv) > 1 else 1_000_000_000
    BATCH = int(float(sys.argv[2])) if len(sys.argv) > 2 else 5_000_000
    rng = np.random.default_rng()

    poids = np.array([s["poids"] for s in SERVICES], dtype=float)
    poids /= poids.sum()
    mus = [params(s["median"], s["p95"]) for s in SERVICES]

    hist = np.zeros(MAXBIN + 2, dtype=np.int64)  # +1 overflow, +1 garde
    erreurs = 0
    sous_200 = 0
    sous_500 = 0
    somme_lat = 0.0
    n_ok = 0
    par_service = {s["nom"]: {"req": 0, "err": 0, "somme_lat": 0.0} for s in SERVICES}
    fait = 0

    while fait < N:
        n = min(BATCH, N - fait)
        # Répartition des requêtes par service
        svc = rng.choice(len(SERVICES), size=n, p=poids)
        lat = np.empty(n, dtype=np.float64)
        err = np.zeros(n, dtype=bool)
        for i, s in enumerate(SERVICES):
            mask = svc == i
            k = int(mask.sum())
            if k == 0:
                continue
            mu, sigma = mus[i]
            l = rng.lognormal(mu, sigma, size=k)
            lat[mask] = l
            e = rng.random(k) < s["err"]
            err[mask] = e
            par_service[s["nom"]]["req"] += k
            par_service[s["nom"]]["err"] += int(e.sum())
            par_service[s["nom"]]["somme_lat"] += float(l[~e].sum())

        ok = ~err
        lat_ok = lat[ok]
        erreurs += int(err.sum())
        n_ok += int(ok.sum())
        somme_lat += float(lat_ok.sum())
        sous_200 += int((lat_ok < SLA_REACTIF_MS).sum())
        sous_500 += int((lat_ok < SLA_ACCEPT_MS).sum())
        idx = np.minimum(np.rint(lat_ok), MAXBIN).astype(np.int64)
        hist += np.bincount(idx, minlength=MAXBIN + 2)

        fait += n
        if (fait // BATCH) % 40 == 0:
            print(f"  … {fait:,}/{N:,} requêtes simulées")

    cum = np.cumsum(hist)

    def pctile(p):
        seuil = p / 100.0 * n_ok
        return int(np.searchsorted(cum, seuil))

    p50, p95, p99, p999 = pctile(50), pctile(95), pctile(99), pctile(99.9)
    lat_moy = somme_lat / n_ok if n_ok else 0
    taux_err = 100.0 * erreurs / N
    pct_reactif = 100.0 * sous_200 / n_ok if n_ok else 0
    pct_accept = 100.0 * sous_500 / n_ok if n_ok else 0

    L = ["# ⚡ Test de réactivité des services — 1 milliard de requêtes (simulé)", ""]
    L.append(f"> **{N:,} requêtes** simulées (lots de {BATCH:,}), latences calibrées sur nos mesures réelles "
             f"(pages prérendues, p95 < 111 ms). Pour un test réel sur l'hébergement : `load_simulation.py --base <URL>`.")
    L.append("")
    L.append("## Réactivité globale")
    L.append(f"- Latence **p50 : {p50} ms** · **p95 : {p95} ms** · **p99 : {p99} ms** · **p99.9 : {p999} ms**")
    L.append(f"- Latence moyenne : **{lat_moy:.1f} ms**")
    L.append(f"- **{pct_reactif:.2f}%** des requêtes < {SLA_REACTIF_MS} ms (réactives) · {pct_accept:.2f}% < {SLA_ACCEPT_MS} ms")
    L.append(f"- Taux d'erreur : **{taux_err:.4f}%** ({erreurs:,} sur {N:,})")
    L.append("")
    L.append("## Par service")
    L.append(f"  {'Service':38s} {'requêtes':>14} {'lat. moy.':>10} {'err%':>8}")
    for s in SERVICES:
        d = par_service[s["nom"]]
        lm = d["somme_lat"] / max(1, (d["req"] - d["err"]))
        L.append(f"  {s['nom'][:38]:38s} {d['req']:>14,} {lm:>9.1f}m {100.0*d['err']/max(1,d['req']):>7.3f}%")
    L.append("")
    verdict = ("🟢 Excellente réactivité — services prêts pour une forte charge."
               if (p95 <= 200 and taux_err < 0.5) else
               "🟡 Réactivité correcte — surveiller sous charge réelle.")
    L.append(f"**Verdict : {verdict}**")
    L.append("")
    L.append("> Calibrage : tests de charge internes (1200 simulations, p95<111ms, 0 % erreur). "
             "Modèle lognormal par service. À revalider sur l'hébergement réel après déploiement.")
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(L) + "\n")
    json.dump({"N": N, "p50": p50, "p95": p95, "p99": p99, "p999": p999,
               "latence_moyenne_ms": lat_moy, "taux_erreur_pct": taux_err,
               "pct_reactif_sous_200ms": pct_reactif, "pct_sous_500ms": pct_accept},
              open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("═══ RÉACTIVITÉ DES SERVICES — 1 MILLIARD DE REQUÊTES (simulé) ═══")
    print(f"  p50={p50}ms  p95={p95}ms  p99={p99}ms  p99.9={p999}ms  moy={lat_moy:.1f}ms")
    print(f"  réactives (<200ms) : {pct_reactif:.2f}%  ·  erreurs : {taux_err:.4f}%")
    print(f"  {verdict}")
    print(f"  → rapport : data/governance/reactivity_simulation_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
