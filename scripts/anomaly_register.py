#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Registre des anomalies — documentations obsolètes/contradictoires (P-DOC-OBSOLETE).
==================================================================================
Met en œuvre la « règle d'or » : une donnée obsolète ne stoppe JAMAIS l'agent ;
elle est capturée, signalée, dépassée par la source officielle.

- Liste les anomalies (data/governance/anomalies_register.json), ouvertes vs résolues.
- Permet d'AJOUTER une anomalie en ligne de commande (capture immédiate, sans interrompre).
- Verdict NON BLOQUANT : ALERTE s'il reste des anomalies ouvertes (jamais GEL ici — la mission continue).

Usage :
  python3 scripts/anomaly_register.py                      # rapport d'écart
  python3 scripts/anomaly_register.py --json
  python3 scripts/anomaly_register.py --add "url|nature|ecart|source_canonique"
"""
from __future__ import annotations
import json, os, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, "data", "governance", "anomalies_register.json")


def charger():
    return json.load(open(REG, encoding="utf-8"))


def ajouter(spec: str):
    d = charger()
    parts = (spec.split("|") + ["", "", "", ""])[:4]
    url, nature, ecart, canon = parts
    nid = "ANO-%03d" % (len(d["anomalies"]) + 1)
    d["anomalies"].append({
        "id": nid, "date_constat": datetime.now(timezone.utc).date().isoformat(),
        "source_litigieuse": url, "nature": nature or "à préciser", "ecart": ecart,
        "source_canonique": canon or "EUR-Lex / Commission / portail officiel",
        "action": "à planifier (MAJ auto ou humaine)", "statut": "ouvert",
    })
    json.dump(d, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"✅ {nid} capturé (statut ouvert). La mission se poursuit.")


def main() -> int:
    if "--add" in sys.argv:
        ajouter(sys.argv[sys.argv.index("--add") + 1]); return 0
    d = charger()
    a = d.get("anomalies", [])
    ouverts = [x for x in a if x.get("statut") != "resolu"]
    if "--json" in sys.argv:
        print(json.dumps({"total": len(a), "ouverts": len(ouverts),
                          "verdict": "ALERTE" if ouverts else "OK"}, ensure_ascii=False))
        return 0
    print("═══ REGISTRE DES ANOMALIES (doc obsolète/contradictoire) ═══")
    print(f"  Total : {len(a)} · ouverts : {len(ouverts)} · résolus : {len(a) - len(ouverts)}")
    for x in a:
        flag = "🔴 ouvert" if x.get("statut") != "resolu" else "✓ résolu"
        print(f"  [{flag}] {x['id']} ({x.get('nature','')}) — {x.get('source_litigieuse','')[:60]}")
        print(f"      écart : {x.get('ecart','')[:100]}")
        print(f"      → source canonique : {x.get('source_canonique','')[:70]}")
    print(f"\n  Verdict : {'ALERTE (anomalies ouvertes à planifier)' if ouverts else 'OK'} — NON bloquant : la mission continue toujours.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
