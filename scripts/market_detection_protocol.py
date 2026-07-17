#!/usr/bin/env python3
"""
market_detection_protocol.py — DÉTECTION DU MARCHÉ (signaux & opportunités).

Honnête : la détection RÉELLE (recherche web) est faite par l'assistant à chaque passage ;
ce script lit le journal des signaux (data/governance/market_detection.json), les trie par
priorité et produit un brief intégrable aux audits/décisions.

Sortie : data/governance/market_detection_brief.md
Usage : python3 scripts/market_detection_protocol.py
"""
import json

SRC = "data/governance/market_detection.json"
OUT = "data/governance/market_detection_brief.md"
ORDRE = {"🔴 HAUTE": 0, "🟠 MOYENNE": 1, "🟢 À SUIVRE": 2}


def main():
    d = json.load(open(SRC, encoding="utf-8"))
    sig = sorted(d.get("signaux", []), key=lambda s: ORDRE.get(s.get("priorite"), 9))
    hautes = sum(1 for s in sig if s.get("priorite", "").startswith("🔴"))

    L = ["# 📡 Détection du marché — signaux & opportunités", ""]
    L.append(f"*{d['note_honnete']} Dernière détection : {d.get('derniere_detection')}.*")
    L.append("")
    L.append(f"## Synthèse : {len(sig)} signaux ({hautes} en priorité haute)")
    L.append("")
    for s in sig:
        L.append(f"### {s['priorite']} — {s['axe']}")
        L.append(f"- **Signal** : {s['signal']}")
        L.append(f"- **Impact** : {s['impact']}")
        L.append(f"- **Opportunité** : {s['opportunite']}")
        L.append(f"- Source : {s['source']} (vu le {s['date']})")
        L.append("")
    L.append(f"## Verdict expert\n{d.get('verdict_expert','')}")
    L.append("")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    print("═══ DÉTECTION DU MARCHÉ ═══")
    print(f"  Signaux : {len(sig)} | priorité haute : {hautes}")
    print(f"  → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
