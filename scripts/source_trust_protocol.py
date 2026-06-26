#!/usr/bin/env python3
"""
source_trust_protocol.py — FILTRAGE & CONFIANCE DES SOURCES (anti-fraude de source).

Vérifie que toute source marquée 'officiel' provient bien d'un domaine de la LISTE BLANCHE
(data/governance/trusted_sources.json). Filtre/segnale tout domaine non fiable. C'est le
garde-fou qui garantit que nos preuves viennent de sources sûres et connues.

Sortie console + data/governance/source_trust_report.md
Usage : python3 scripts/source_trust_protocol.py
"""
import json
import glob
from urllib.parse import urlparse

WL = "data/governance/trusted_sources.json"
OUT = "data/governance/source_trust_report.md"


def domaine(url):
    try:
        net = urlparse(url).netloc.lower()
    except ValueError:
        return ""
    if net.startswith("www."):
        net = net[4:]
    return net


def main():
    wl = json.load(open(WL, encoding="utf-8"))
    tier1 = set(wl["tier1_officiel"])
    tier2 = set(wl["tier2_institutionnel"])
    tier3 = set(wl["tier3_secondaire_complement"])

    faux_officiel = []   # source 'officiel' mais domaine hors tier1
    inconnus = []        # domaine dans aucune liste
    total_src = 0

    for f in sorted(glob.glob("data/belgium/*.json")):
        try:
            mod = json.load(open(f, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for fait in mod.get("faits", []):
            for s in fait.get("sources", []) or []:
                total_src += 1
                dom_norm = domaine(s.get("url", ""))
                in1 = any(dom_norm == d or dom_norm.endswith("." + d) for d in tier1)
                in2 = any(dom_norm == d or dom_norm.endswith("." + d) for d in tier2)
                in3 = any(dom_norm == d or dom_norm.endswith("." + d) for d in tier3)
                if s.get("type") == "officiel" and not in1:
                    faux_officiel.append(f"{fait.get('id')} → {dom_norm} marqué 'officiel' hors tier1")
                if not (in1 or in2 or in3):
                    inconnus.append(f"{fait.get('id')} → {dom_norm} (hors liste blanche)")

    ok = not faux_officiel
    L = ["# 🛡️ Confiance des sources — filtrage", ""]
    L.append(f"*Vérifie que les preuves viennent de sources sûres et connues. {total_src} sources analysées.*")
    L.append("")
    L.append(f"- Sources 'officiel' hors tier1 (fraude de source) : **{len(faux_officiel)}** {'⚠️' if faux_officiel else '✓ aucune'}")
    for x in faux_officiel:
        L.append(f"  - {x}")
    L.append(f"- Domaines hors liste blanche (à surveiller) : **{len(inconnus)}**")
    for x in inconnus[:20]:
        L.append(f"  - {x}")
    L.append("")
    L.append("## Verdict")
    L.append("✅ Toutes les sources 'officiel' proviennent de domaines de confiance." if ok
             else "⛔ Des sources 'officiel' ne viennent PAS d'un domaine de confiance — à corriger.")
    L.append("")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    print("═══ CONFIANCE DES SOURCES ═══")
    print(f"  Sources : {total_src} | 'officiel' hors tier1 : {len(faux_officiel)} | hors liste : {len(inconnus)}")
    print("  ✅ OK" if ok else "  ⛔ À CORRIGER")
    print(f"  → {OUT}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
