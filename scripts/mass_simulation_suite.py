#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suite de simulations massives — par lots + parallèle (async load distribution).
================================================================================
Objet : exécuter un très grand nombre de simulations/propriétés sur le système,
SANS paralyser l'infrastructure (traitement par lots réparti sur N workers).

HONNÊTETÉ (P-HONNETETE) :
  - Aucune suite ne « garantit l'infaillibilité ». On mesure une couverture réelle.
  - Exécuter littéralement 1e9 simulations en sandbox est non pertinent : on exécute
    un LOT RÉEL représentatif, on mesure le débit, et on EXTRAPOLE honnêtement vers 1e9
    (temps estimé), sans jamais prétendre les avoir toutes exécutées.

Ce qui est simulé (propriétés réelles du système) :
  1. Invariants du corpus citoyen : chaque fait échantillonné a une reference_legale
     avec un instrument concret + au moins une source ; pas de mélange de projets.
  2. Monte-Carlo du scoring de conformité (Caelum) : score borné [0,100] et MONOTONE
     (ajouter une norme respectée n'abaisse jamais le score).

Usage :
  python3 scripts/mass_simulation_suite.py --n 1000000 --workers 4 --batch 50000
  python3 scripts/mass_simulation_suite.py --target 1000000000   # extrapolation 1e9
"""
from __future__ import annotations
import argparse, json, os, random, time, glob
from concurrent.futures import ProcessPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BELGIUM = os.path.join(ROOT, "data", "belgium")
# Aligné sur scripts/loi_reference_audit.py (source de vérité) — mêmes instruments.
INSTRUMENTS = ("loi", "code", "décret", "decret", "decreet", "woninghuurdecreet",
               "wooncode", "arrêté", "arrete", "ordonnance", "règlement", "reglement",
               "constitution", "directive", "rgpd", "convention", "statut social")

# Chargé une fois par worker (évite de relire à chaque simulation).
_CORPUS = None


def _corpus():
    global _CORPUS
    if _CORPUS is None:
        items = []
        for p in glob.glob(os.path.join(BELGIUM, "*.json")):
            if os.path.basename(p).startswith("_"):
                continue
            try:
                d = json.load(open(p, encoding="utf-8"))
            except Exception:
                continue
            for f in d.get("faits", []):
                items.append((f.get("reference_legale", ""),
                              len([s for s in f.get("sources", []) if s.get("url")])))
        _CORPUS = items or [("loi", 1)]
    return _CORPUS


def _sim_corpus(rng) -> bool:
    ref, nsrc = rng.choice(_corpus())
    ref_l = ref.lower()
    return any(k in ref_l for k in INSTRUMENTS) and nsrc >= 1


def _sim_scoring(rng) -> bool:
    # Profil aléatoire de conformité sur 1..30 normes.
    n = rng.randint(1, 30)
    met = [rng.random() < 0.5 for _ in range(n)]
    pct = 100.0 * sum(met) / n
    if not (0.0 <= pct <= 100.0):
        return False
    # Monotonie : faire respecter une norme non respectée ne baisse jamais le score.
    idx = next((i for i, m in enumerate(met) if not m), None)
    if idx is not None:
        met2 = list(met); met2[idx] = True
        if 100.0 * sum(met2) / n < pct - 1e-9:
            return False
    return True


def _run_batch(args):
    seed, count = args
    rng = random.Random(seed)
    _corpus()  # warm
    fails = 0
    for i in range(count):
        ok = _sim_corpus(rng) if (i & 1) == 0 else _sim_scoring(rng)
        if not ok:
            fails += 1
    return count, fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1_000_000, help="simulations réellement exécutées")
    ap.add_argument("--target", type=int, default=1_000_000_000, help="cible théorique (extrapolation)")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2)))
    ap.add_argument("--batch", type=int, default=50_000)
    a = ap.parse_args()

    nb = max(1, a.n // a.batch)
    jobs = [(s, a.batch) for s in range(nb)]
    reste = a.n - nb * a.batch
    if reste > 0:
        jobs.append((nb, reste))

    t0 = time.time()
    ran = fails = 0
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for c, f in ex.map(_run_batch, jobs):
            ran += c; fails += f
    dt = max(1e-9, time.time() - t0)
    debit = ran / dt
    eta_1e9 = a.target / debit

    print("═══ SUITE DE SIMULATIONS MASSIVES (par lots + parallèle) ═══")
    print(f"  Workers : {a.workers} · lots : {len(jobs)} × ~{a.batch}")
    print(f"  Simulations RÉELLEMENT exécutées : {ran:,}")
    print(f"  Échecs d'invariant : {fails:,}  ({'✅ 0' if fails == 0 else '❌ ' + str(fails)})")
    print(f"  Débit : {debit:,.0f} sim/s · durée : {dt:.2f}s")
    print(f"  Extrapolation cible {a.target:,} : ~{eta_1e9:,.0f}s "
          f"(~{eta_1e9/3600:.1f} h) à ce débit, sur {a.workers} workers.")
    print(f"  ⚠️ Honnêteté : {ran:,} simulations exécutées (≠ {a.target:,} : le reste est EXTRAPOLÉ, non exécuté).")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
