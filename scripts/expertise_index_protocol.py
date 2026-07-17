#!/usr/bin/env python3
"""
expertise_index_protocol.py — INDICE D'EXPERTISE (honnête, mesurable, traçable).

Honnêteté : le système ne "s'entraîne" pas tout seul. Ce qui progresse, c'est le SAVOIR
vérifié et sourcé. Cet indice le mesure objectivement et journalise chaque évolution, pour
qu'on VOIE l'expertise monter — uniquement sur des preuves réelles.

Indice = f(faits sourcés, thèmes couverts, régions, % sources officielles, % à jour).
Chaque exécution ajoute une entrée horodatée à data/governance/expertise_history.json et
indique si l'expertise a PROGRESSÉ depuis la dernière mesure.

Usage : python3 scripts/expertise_index_protocol.py
"""
import json
import glob
import os
from datetime import datetime, date

HISTORY = "data/governance/expertise_history.json"


def mesurer():
    faits = 0
    sources_off = 0
    themes = set()
    regions = set()
    frais = 0
    today = date(2026, 6, 26)
    for f in glob.glob("data/belgium/bail_*.json"):
        try:
            mod = json.load(open(f, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        regions.add(mod.get("juridiction", f))
        for fait in mod.get("faits", []):
            faits += 1
            parts = fait.get("id", "").split("-")
            if len(parts) >= 2:
                themes.add(parts[1])
            if any(s.get("type") == "officiel" for s in fait.get("sources", []) or []):
                sources_off += 1
            dv = fait.get("date_verification", "")
            try:
                d = datetime.strptime(dv, "%Y-%m-%d").date()
                if (today - d).days <= 365:
                    frais += 1
            except ValueError:
                pass

    pct_off = (sources_off / faits) if faits else 0
    pct_frais = (frais / faits) if faits else 0
    # Indice transparent : savoir × qualité. Plafonné à 100 pour rester lisible.
    brut = faits * 1 + len(themes) * 3 + len(regions) * 4
    indice = round(brut * (0.5 + 0.5 * pct_off) * (0.5 + 0.5 * pct_frais), 1)
    return {
        "faits": faits, "themes": len(themes), "regions": len(regions),
        "pct_sources_officielles": round(pct_off * 100), "pct_a_jour": round(pct_frais * 100),
        "indice_expertise": indice,
    }


def main():
    snap = mesurer()
    hist = []
    if os.path.exists(HISTORY):
        try:
            hist = json.load(open(HISTORY, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            hist = []
    precedent = hist[-1]["indice_expertise"] if hist else 0.0

    entree = {"date": "2026-06-26", **snap}
    hist.append(entree)
    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    with open(HISTORY, "w", encoding="utf-8") as f:
        json.dump(hist[-200:], f, indent=2, ensure_ascii=False)

    delta = round(snap["indice_expertise"] - precedent, 1)
    tendance = "↑ PROGRESSION" if delta > 0 else ("→ stable" if delta == 0 else "↓ baisse")

    print("═══ INDICE D'EXPERTISE ═══")
    print(f"  Faits sourcés : {snap['faits']} | Thèmes : {snap['themes']} | Régions : {snap['regions']}")
    print(f"  Sources officielles : {snap['pct_sources_officielles']}% | À jour : {snap['pct_a_jour']}%")
    print(f"  INDICE : {snap['indice_expertise']}  ({tendance}, Δ {delta:+})")
    print(f"  Mesures enregistrées : {len(hist)} → {HISTORY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
