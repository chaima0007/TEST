#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Garde de hiérarchie des normes (P-HIERARCHIE-NORMES).
=====================================================
Vérifie la hiérarchie UE > fédéral belge > régional et détecte :
  - CONFLIT TEMPOREL : une valeur/texte PÉRIMÉ cité comme en vigueur (ex. CSDDD « 5 % »
    sans la valeur actuelle « 3 % »).
  - CONFLIT TERRITORIAL : une compétence fédérale présentée comme régionale (ex. TVA régionale).

Règle implacable : tout conflit déclenche un GEL (verdict bloquant) → audit croisé sur sources
officielles AVANT de poursuivre. Écrit data/governance/norm_hierarchy_report.json.

Usage : python3 scripts/norm_hierarchy_guard.py [--json]
"""
from __future__ import annotations
import json, os, re, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "data", "governance", "norm_hierarchy.json")
OUT = os.path.join(ROOT, "data", "governance", "norm_hierarchy_report.json")


def textes_corpus():
    """Retourne (label, texte_concaténé) pour chaque entrée Caelum/citoyenne."""
    items = []
    # Caelum normes
    try:
        d = json.load(open(os.path.join(ROOT, "data/caelum/conformite_entreprises.json"), encoding="utf-8"))
        for n in d.get("normes", []):
            blob = " ".join(str(n.get(k, "")) for k in ("norme", "changement", "sanction", "reference_legale"))
            items.append((f"caelum:{n.get('id')}", blob))
    except Exception:
        pass
    # Modules citoyens (un blob par module)
    for f in glob.glob(os.path.join(ROOT, "data/belgium/*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        blob = json.dumps(d, ensure_ascii=False)
        items.append((f"citoyen:{d.get('module')}", blob))
    return items


def main() -> int:
    ref = json.load(open(REF, encoding="utf-8"))
    items = textes_corpus()
    conflits = []

    # Conflits temporels : motif_perime présent SANS motif_actuel dans la même entrée
    for w in ref.get("watchlist_temporel", []):
        dom = w["domaine"].lower()
        for label, blob in items:
            b = blob.lower()
            if dom in b and w["motif_perime"] in blob and w["motif_actuel"] not in blob:
                conflits.append({"type": "temporel", "regle": w["id"], "entree": label, "note": w["note"]})

    # Conflits territoriaux : motif interdit (regex)
    for w in ref.get("watchlist_territorial", []):
        pat = re.compile(w["motif_interdit"], re.IGNORECASE | re.DOTALL)
        for label, blob in items:
            if pat.search(blob):
                conflits.append({"type": "territorial", "regle": w["id"], "entree": label, "note": w["note"]})

    verdict = "GEL" if conflits else "OK"
    rapport = {"verdict": verdict, "conflits": conflits, "entrees_scannees": len(items),
               "hierarchie": ref.get("hierarchie")}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(rapport, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    if "--json" in sys.argv:
        print(json.dumps(rapport, ensure_ascii=False))
        return 1 if conflits else 0

    print("═══ GARDE — HIÉRARCHIE DES NORMES (UE > fédéral > régional) ═══")
    print(f"  Entrées scannées : {len(items)}")
    if conflits:
        print(f"  🛑 GEL — {len(conflits)} conflit(s) détecté(s) :")
        for c in conflits[:15]:
            print(f"     [{c['type']}] {c['entree']} ({c['regle']}) — {c['note'][:80]}")
        print("\n  ⛔ Décisions GELÉES. Audit croisé sources officielles requis AVANT de poursuivre.")
    else:
        print("  ✅ Aucun conflit temporel ni territorial. Hiérarchie cohérente.")
    print(f"  → {os.path.relpath(OUT, ROOT)}")
    return 1 if conflits else 0


if __name__ == "__main__":
    sys.exit(main())
