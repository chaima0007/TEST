#!/usr/bin/env python3
"""
regional_comparator.py — COMPARATEUR INTER-RÉGIONAL (avant-gardiste).

Lit les modules de bail belges (data/belgium/*.json) et produit une comparaison claire,
par thème, entre Wallonie / Bruxelles / Flandre. Ce que peu d'outils offrent simplement.
Chaque réponse reste sourcée (les sources sont dans les modules d'origine).

Sortie : data/belgium/comparatif_regions.md

Usage : python3 scripts/regional_comparator.py
"""
import json
import glob

REGIONS = {"BWAL": "Wallonie", "BBRU": "Bruxelles", "BVLG": "Flandre"}
THEMES = {"DUREE": "Durée du bail", "GARANTIE": "Garantie locative",
          "PREAVIS": "Préavis / résiliation", "INDEX": "Indexation du loyer",
          "EDL": "État des lieux", "REP": "Réparations & entretien (qui paie quoi)",
          "SALUB": "Salubrité / logement décent", "EXP": "Expulsion (procédure)",
          "PEB": "PEB / performance énergétique (location)"}
ORDRE_THEMES = ["DUREE", "GARANTIE", "PREAVIS", "INDEX", "EDL", "REP", "SALUB", "EXP", "PEB"]


def main():
    # data[theme][region] = reponse
    data = {t: {} for t in THEMES}
    bases = {}
    for f in sorted(glob.glob("data/belgium/bail_*.json")):
        try:
            mod = json.load(open(f, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for fait in mod.get("faits", []):
            parts = fait.get("id", "").split("-")
            if len(parts) < 2:
                continue
            region, theme = parts[0], parts[1]
            if region in REGIONS and theme in THEMES:
                data[theme][region] = fait.get("reponse", "")
                bases[region] = mod.get("base_legale_principale", {}).get("intitule", "")

    L = ["# ⚖️ Comparatif du bail de résidence principale — Wallonie · Bruxelles · Flandre", ""]
    L.append("*Information générale sourcée (voir modules régionaux pour les sources officielles). "
             "Ne constitue pas un conseil juridique individualisé. Revu le 2026-06-26.*")
    L.append("")
    L.append("## Bases légales par région")
    for code, nom in REGIONS.items():
        if code in bases:
            L.append(f"- **{nom}** : {bases[code]}")
    L.append("")

    for theme in ORDRE_THEMES:
        L.append(f"## {THEMES[theme]}")
        for code, nom in REGIONS.items():
            rep = data[theme].get(code)
            if rep:
                L.append(f"- **{nom}** — {rep}")
        L.append("")

    contenu = "\n".join(L) + "\n"
    with open("data/belgium/comparatif_regions.md", "w", encoding="utf-8") as f:
        f.write(contenu)

    couverture = sum(1 for t in THEMES for r in REGIONS if data[t].get(r))
    print("═══ COMPARATEUR INTER-RÉGIONAL ═══")
    print(f"  Thèmes : {len(THEMES)} | Régions : {len(REGIONS)} | Cases remplies : {couverture}/{len(THEMES)*len(REGIONS)}")
    print("  → data/belgium/comparatif_regions.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
