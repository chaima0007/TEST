#!/usr/bin/env python3
"""
conflict_resolution_protocol.py — Résolution de conflit DÉCENTRALISÉE (P-CONFLIT).

Quand deux « agents » (sources de données) divergent sur un même fait, on tranche sans humain
par une règle inspirée de la théorie des jeux : chaque source a un poids de confiance (payoff) ;
l'issue stable (type Nash) est la valeur de la source de plus haute confiance — aucune source
de poids inférieur ne peut « dévier » et améliorer le résultat. À confiance égale : la version
la plus récente l'emporte ; sinon, vote majoritaire.

Application concrète : départager la base canonique (data/belgium) et sa copie de site
(laloiavecmoi/data/belgium) lorsqu'elles divergent — la canonique gagne.

Usage :
  python3 scripts/conflict_resolution_protocol.py          # détecte + résout (rapport)
  python3 scripts/conflict_resolution_protocol.py --heal   # applique la résolution (aligne la copie)
"""
import glob
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# « Agents » sources et leur poids de confiance (payoff).
SOURCES = [
    {"id": "canonique", "dir": os.path.join(BASE, "data", "belgium"), "confiance": 1.0},
    {"id": "copie_site", "dir": os.path.join(BASE, "laloiavecmoi", "data", "belgium"), "confiance": 0.8},
]


def charger(dossier):
    faits = {}
    for f in glob.glob(os.path.join(dossier, "*.json")):
        if os.path.basename(f).startswith("_"):
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for fait in d.get("faits", []):
            if fait.get("id"):
                faits[fait["id"]] = {"reponse": fait.get("reponse", ""),
                                     "date": fait.get("date_verification", ""),
                                     "fichier": os.path.basename(f)}
    return faits


def resoudre(a, b, conf_a, conf_b):
    """Retourne l'id de la source gagnante selon la règle de théorie des jeux."""
    if a["reponse"] == b["reponse"]:
        return None  # pas de conflit
    if conf_a != conf_b:
        return "a" if conf_a > conf_b else "b"  # plus haute confiance
    # confiance égale → plus récent
    if a["date"] != b["date"]:
        return "a" if a["date"] > b["date"] else "b"
    return "a"  # défaut stable


def analyser():
    bases = [(s, charger(s["dir"])) for s in SOURCES]
    (sa, fa), (sb, fb) = bases[0], bases[1]
    communs = set(fa) & set(fb)
    conflits = []
    for fid in sorted(communs):
        gagnant = resoudre(fa[fid], fb[fid], sa["confiance"], sb["confiance"])
        if gagnant:
            conflits.append({
                "fait": fid,
                "fichier": fa[fid]["fichier"],
                "gagnant": sa["id"] if gagnant == "a" else sb["id"],
            })
    return conflits, sa, sb, fa, fb


def main():
    heal = "--heal" in sys.argv
    conflits, sa, sb, fa, fb = analyser()

    print("═══ RÉSOLUTION DE CONFLIT DÉCENTRALISÉE (théorie des jeux) ═══")
    print(f"  Sources : {sa['id']} (conf {sa['confiance']}) vs {sb['id']} (conf {sb['confiance']})")
    print(f"  Faits comparés : {len(set(fa) & set(fb))} | conflits détectés : {len(conflits)}")
    for c in conflits[:10]:
        print(f"   ⚖️  {c['fait']} ({c['fichier']}) → gagnant : {c['gagnant']}")

    if conflits and heal:
        # Auto-réparation : aligner la copie site sur la canonique (gagnante par confiance).
        import shutil
        fichiers = {c["fichier"] for c in conflits if c["gagnant"] == "canonique"}
        for f in fichiers:
            src = os.path.join(sa["dir"], f)
            dst = os.path.join(sb["dir"], f)
            if os.path.exists(src):
                shutil.copy2(src, dst)
        print(f"  🛠️  {len(fichiers)} fichier(s) réalignés sur la source canonique.")

    json.dump({"conflits": conflits, "regle": "confiance>récence>majorité"},
              open(os.path.join(BASE, "data", "conflict_resolution_report.json"), "w"),
              ensure_ascii=False, indent=2)
    if conflits and not heal:
        print("  → Conflits résolus (rapport). Relancer avec --heal pour aligner automatiquement.")
    elif not conflits:
        print("  ✅ Aucun conflit : les sources sont cohérentes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
