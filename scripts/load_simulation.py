#!/usr/bin/env python3
"""
load_simulation.py — Simulateur de montée en charge (latence & débit).

Teste si le site tient sous forte demande et repère les pages à latence élevée (à éviter).
Mesure, par route : latence p50 / p95 / p99, débit (req/s), taux d'erreur, sous N requêtes
concurrentes. 100 % stdlib (aucune dépendance).

Usage :
  python3 scripts/load_simulation.py --base http://127.0.0.1:3210 \
      --routes /loi-avec-moi,/base-juridique,/transparence,/loi/bail_bruxelles \
      --concurrency 50 --requests 400
"""
import argparse
import json
import os
import statistics
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Seuils de latence (ms) — au-delà = à optimiser AVANT le lancement.
SEUIL_ALERTE_MS = 300
SEUIL_CRITIQUE_MS = 800


def une_requete(url):
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "caelum-loadsim"})
        with urllib.request.urlopen(req, timeout=20) as r:
            r.read()
            code = r.status
    except Exception:
        return (None, False)
    return ((time.perf_counter() - t0) * 1000.0, 200 <= code < 400)


def pct(valeurs, p):
    if not valeurs:
        return 0.0
    valeurs = sorted(valeurs)
    k = max(0, min(len(valeurs) - 1, int(round((p / 100.0) * (len(valeurs) - 1)))))
    return valeurs[k]


def tester_route(base, route, concurrency, requests_total):
    url = base.rstrip("/") + route
    latences, ok = [], 0
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        for lat, success in ex.map(lambda _: une_requete(url), range(requests_total)):
            if lat is not None:
                latences.append(lat)
            if success:
                ok += 1
    duree = time.perf_counter() - t0
    p95 = pct(latences, 95)
    statut = "OK"
    if p95 >= SEUIL_CRITIQUE_MS or ok < requests_total * 0.99:
        statut = "CRITIQUE"
    elif p95 >= SEUIL_ALERTE_MS:
        statut = "ALERTE"
    return {
        "route": route,
        "requetes": requests_total,
        "succes": ok,
        "taux_erreur_pct": round((requests_total - ok) / requests_total * 100, 2) if requests_total else 0,
        "p50_ms": round(pct(latences, 50), 1),
        "p95_ms": round(p95, 1),
        "p99_ms": round(pct(latences, 99), 1),
        "max_ms": round(max(latences), 1) if latences else 0,
        "debit_req_s": round(requests_total / duree, 1) if duree else 0,
        "statut": statut,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:3210")
    ap.add_argument("--routes", default="/loi-avec-moi,/base-juridique,/transparence")
    ap.add_argument("--concurrency", type=int, default=50)
    ap.add_argument("--requests", type=int, default=300)
    args = ap.parse_args()

    routes = [r.strip() for r in args.routes.split(",") if r.strip()]
    print("═══ SIMULATION DE MONTÉE EN CHARGE ═══")
    print(f"  Cible : {args.base} | {args.concurrency} requêtes concurrentes | {args.requests}/route\n")

    resultats = [tester_route(args.base, r, args.concurrency, args.requests) for r in routes]

    print(f"  {'Route':32s} {'p50':>7} {'p95':>7} {'p99':>7} {'req/s':>7} {'err%':>6}  statut")
    pire = "OK"
    ordre = {"OK": 0, "ALERTE": 1, "CRITIQUE": 2}
    for r in resultats:
        icone = {"OK": "✅", "ALERTE": "🟠", "CRITIQUE": "🔴"}[r["statut"]]
        print(f"  {r['route'][:32]:32s} {r['p50_ms']:>7} {r['p95_ms']:>7} {r['p99_ms']:>7} "
              f"{r['debit_req_s']:>7} {r['taux_erreur_pct']:>6}  {icone} {r['statut']}")
        if ordre[r["statut"]] > ordre[pire]:
            pire = r["statut"]

    rapport = {
        "cible": args.base,
        "concurrence": args.concurrency,
        "requetes_par_route": args.requests,
        "seuils_ms": {"alerte": SEUIL_ALERTE_MS, "critique": SEUIL_CRITIQUE_MS},
        "verdict_global": pire,
        "routes": resultats,
    }
    out = os.path.join(BASE, "data", "load_simulation_report.json")
    json.dump(rapport, open(out, "w"), ensure_ascii=False, indent=2)
    print(f"\n  → Verdict global : {pire} · rapport : data/load_simulation_report.json")
    return 1 if pire == "CRITIQUE" else 0


if __name__ == "__main__":
    sys.exit(main())
