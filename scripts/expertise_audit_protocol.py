#!/usr/bin/env python3
"""
expertise_audit_protocol.py — MÉTA-AUDIT : l'expertise sur l'expertise.

Audite de façon critique notre propre base de savoir (data/belgium/) pour trouver les
faiblesses AVANT les autres : trous de couverture, faits faiblement sourcés, sources
uniquement secondaires, fraîcheur. Donne une note et des recommandations honnêtes.

C'est de l'assurance qualité de haut niveau : on se critique nous-mêmes, sans complaisance.

Sortie : data/belgium/audit_expertise.md

Usage : python3 scripts/expertise_audit_protocol.py
"""
import json
import glob
from datetime import date, datetime

REGIONS = {"BWAL": "Wallonie", "BBRU": "Bruxelles", "BVLG": "Flandre"}
THEMES = {"DUREE": "Durée", "GARANTIE": "Garantie locative", "PREAVIS": "Préavis",
          "INDEX": "Indexation", "EDL": "État des lieux", "REP": "Réparations", "SALUB": "Salubrité"}
# Thèmes importants encore possibles (pistes de croissance de l'expertise)
THEMES_CANDIDATS = ["Sous-location", "Colocation / bail étudiant", "Expulsion (procédure)",
                    "Charges & décompte", "Discrimination au logement", "Permis de location"]
OUT = "data/belgium/audit_expertise.md"


def _stale(dv):
    try:
        return (date(2026, 6, 26) - datetime.strptime(dv, "%Y-%m-%d").date()).days > 365
    except ValueError:
        return True


def main():
    present = {}            # (region, theme) -> fait
    faibles, sans_officiel, perimes = [], [], []
    for f in glob.glob("data/belgium/bail_*.json"):
        try:
            mod = json.load(open(f, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for fait in mod.get("faits", []):
            parts = fait.get("id", "").split("-")
            if len(parts) < 2:
                continue
            region, theme = parts[0], parts[1]
            present[(region, theme)] = fait
            srcs = fait.get("sources", []) or []
            if len(srcs) < 2:
                faibles.append(fait.get("id"))
            if not any(s.get("type") == "officiel" for s in srcs):
                sans_officiel.append(fait.get("id"))
            if _stale(fait.get("date_verification", "")):
                perimes.append(fait.get("id"))

    # Matrice de couverture
    manquants = []
    for r in REGIONS:
        for t in THEMES:
            if (r, t) not in present:
                manquants.append(f"{REGIONS[r]} — {THEMES[t]}")

    total_cellules = len(REGIONS) * len(THEMES)
    remplies = total_cellules - len(manquants)
    couverture = round(100 * remplies / total_cellules)

    # Note honnête /100
    note = couverture
    note -= 5 * len(sans_officiel)        # grave
    note -= 1 * len(faibles)              # mineur
    note -= 2 * len(perimes)
    note = max(0, min(100, note))
    mention = "EXCELLENT" if note >= 90 else "BON" if note >= 75 else "À CONSOLIDER" if note >= 50 else "FAIBLE"

    L = ["# 🔬 Méta-audit — l'expertise sur l'expertise", ""]
    L.append("*Auto-critique honnête de notre base de savoir, pour trouver nos faiblesses avant les autres. "
             "Revu le 2026-06-26.*")
    L.append("")
    L.append(f"## Note de qualité : {note}/100 — {mention}")
    L.append(f"- Couverture : {remplies}/{total_cellules} cases ({couverture}%)")
    L.append(f"- Faits faiblement sourcés (<2 sources) : {len(faibles)}")
    L.append(f"- Faits SANS source officielle : {len(sans_officiel)} {'⚠️' if sans_officiel else '✓'}")
    L.append(f"- Faits périmés (>365 j) : {len(perimes)}")
    L.append("")
    if manquants:
        L.append("## ❗ Trous de couverture (à combler)")
        for m in manquants:
            L.append(f"- {m}")
        L.append("")
    else:
        L.append("## ✅ Couverture complète sur les thèmes actuels")
        L.append("")
    L.append("## 🌱 Pistes pour approfondir l'expertise (thèmes non encore couverts)")
    for c in THEMES_CANDIDATS:
        L.append(f"- {c}")
    L.append("")
    L.append("## 🧭 Recommandation")
    if sans_officiel:
        L.append("Priorité : re-sourcer officiellement les faits signalés (sécurité).")
    elif manquants:
        L.append("Priorité : combler les trous de couverture ci-dessus.")
    else:
        L.append("Base solide. Prochaine étape : ajouter un thème candidat ou la version NL.")
    L.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    print("═══ MÉTA-AUDIT DE L'EXPERTISE ═══")
    print(f"  Note : {note}/100 ({mention}) | Couverture {couverture}% | sans source officielle : {len(sans_officiel)}")
    print(f"  → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
