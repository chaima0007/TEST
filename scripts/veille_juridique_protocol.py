#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Veille juridique — signale ce qu'il faut revoir quand les lois changent.

Lit data/governance/veille_juridique.json (signaux connus) + les modules,
calcule l'ancienneté des vérifications, et produit un rapport de revue :
- signaux de changement à surveiller (par priorité),
- fiches dont la date de vérification dépasse la cadence (à revérifier).

Honnête : l'agent SIGNALE ; la mise à jour réelle se fait sous protocole
(vérification de la source officielle avant toute modification).

Sortie : data/governance/veille_juridique_report.md
"""
import json
import glob
import os
import pathlib
from datetime import date, datetime

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
GOV = REPO / "data" / "governance"
DATA = REPO / "data" / "belgium"
VEILLE = GOV / "veille_juridique.json"
OUT = GOV / "veille_juridique_report.md"


def lire(p, d=None):
    try:
        return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    except Exception:
        return d


def parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None


def construire():
    v = lire(VEILLE, {})
    cadence = v.get("cadence_revue_jours", 180)
    today = date.today()

    # fiches à revérifier (date_verification trop ancienne)
    a_reverifier = []
    total = 0
    for fp in sorted(glob.glob(str(DATA / "*.json"))):
        if os.path.basename(fp).startswith("_"):
            continue
        d = lire(fp, {})
        for f in d.get("faits", []):
            total += 1
            dv = parse_date(f.get("date_verification", ""))
            if dv and (today - dv).days > cadence:
                a_reverifier.append((os.path.basename(fp), f.get("id"), (today - dv).days))

    signaux = sorted(v.get("signaux", []), key=lambda s: {"haute": 0, "moyenne": 1, "basse": 2}.get(s.get("priorite"), 3))

    L = []
    L.append("# Veille juridique — quoi revoir, et quand")
    L.append("")
    L.append(f"*Généré le {today.isoformat()}. Cadence de revue : {cadence} jours. "
             "L'agent signale ; la mise à jour se fait après vérification de la source officielle.*")
    L.append("")
    L.append(f"**Signaux suivis : {len(signaux)} · fiches à revérifier (cadence dépassée) : {len(a_reverifier)}/{total}**")
    L.append("")
    L.append("## Signaux de changement à surveiller")
    L.append("")
    L.append("| Priorité | Sujet | Régions | Modules impactés | Statut |")
    L.append("|---|---|---|---|---|")
    for s in signaux:
        L.append(f"| {s.get('priorite','')} | {s.get('sujet','')} | {', '.join(s.get('regions', []))} | "
                 f"{', '.join(s.get('modules_impactes', []))} | {s.get('statut','')} |")
    L.append("")
    if a_reverifier:
        L.append("## Fiches dont la vérification est à rafraîchir")
        for fichier, fid, age in a_reverifier[:100]:
            L.append(f"- {fichier} / {fid} — vérifié il y a {age} jours")
    else:
        L.append("## Fiches à rafraîchir")
        L.append("Aucune : toutes les vérifications sont dans la cadence ✅")
    L.append("")
    L.append("> Rappel : ne jamais modifier une fiche sans revérifier la source officielle (P-SOURCES).")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    return len(signaux), len(a_reverifier), total


if __name__ == "__main__":
    nb_sig, nb_rev, total = construire()
    print("═══ VEILLE JURIDIQUE ═══")
    print(f"  Signaux suivis : {nb_sig}")
    print(f"  Fiches à revérifier (cadence dépassée) : {nb_rev}/{total}")
    print(f"  → {OUT}")
    print("✓ Veille à jour (signale ; n'écrit jamais sans vérifier la source).")
