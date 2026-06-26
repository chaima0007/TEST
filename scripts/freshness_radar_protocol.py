#!/usr/bin/env python3
"""
freshness_radar_protocol.py — RADAR DE FRAÎCHEUR (remise à niveau si les lois changent).

Surveille chaque fait juridique et indique quand il doit être RE-VÉRIFIÉ à la source
officielle. Les lois changent : une expertise fiable se re-source régulièrement.

Cadence par défaut : re-vérification recommandée tous les 180 jours (semestriel).
  - 🔴 EN RETARD : date de revue dépassée → à re-sourcer en priorité.
  - 🟠 BIENTÔT   : échéance dans les 30 jours.
  - 🟢 À JOUR    : encore frais.

Honnête : « remettre à niveau » = re-vérifier la source, PAS juste changer la date.

Sortie : data/belgium/radar_fraicheur.md
Usage : python3 scripts/freshness_radar_protocol.py [--cadence 180]
"""
import json
import glob
import sys
from datetime import date, datetime, timedelta

OUT = "data/belgium/radar_fraicheur.md"
DEFAUT_CADENCE = 180


def main():
    cadence = DEFAUT_CADENCE
    if "--cadence" in sys.argv:
        cadence = int(sys.argv[sys.argv.index("--cadence") + 1])
    today = date(2026, 6, 26)

    lignes_faits = []
    for f in sorted(glob.glob("data/belgium/bail_*.json")):
        try:
            mod = json.load(open(f, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        titre = mod.get("titre", f)
        for fait in mod.get("faits", []):
            dv = fait.get("date_verification", "")
            try:
                d = datetime.strptime(dv, "%Y-%m-%d").date()
            except ValueError:
                d = None
            if d is None:
                etat, due, jours = "🔴 EN RETARD", "?", None
            else:
                echeance = d + timedelta(days=cadence)
                reste = (echeance - today).days
                due = echeance.isoformat()
                jours = reste
                if reste < 0:
                    etat = "🔴 EN RETARD"
                elif reste <= 30:
                    etat = "🟠 BIENTÔT"
                else:
                    etat = "🟢 À JOUR"
            lignes_faits.append((etat, jours if jours is not None else -9999,
                                 fait.get("id", "?"), titre, due))

    # tri : les plus urgents d'abord
    ordre = {"🔴 EN RETARD": 0, "🟠 BIENTÔT": 1, "🟢 À JOUR": 2}
    lignes_faits.sort(key=lambda x: (ordre[x[0]], x[1]))

    retard = sum(1 for l in lignes_faits if l[0].startswith("🔴"))
    bientot = sum(1 for l in lignes_faits if l[0].startswith("🟠"))

    L = ["# 🛰️ Radar de fraîcheur — remise à niveau du savoir juridique", ""]
    L.append(f"*Cadence de re-vérification : tous les {cadence} jours. "
             f"Remettre à niveau = re-vérifier la source officielle (les lois changent), pas seulement la date. "
             f"Revu le {today.isoformat()}.*")
    L.append("")
    L.append(f"## Synthèse : 🔴 {retard} en retard · 🟠 {bientot} bientôt · total {len(lignes_faits)} faits")
    L.append("")
    L.append("| État | Fait | Module | À re-vérifier avant |")
    L.append("|---|---|---|---|")
    for etat, _, fid, titre, due in lignes_faits:
        court = titre.replace("Bail de résidence principale — ", "")
        L.append(f"| {etat} | {fid} | {court} | {due} |")
    L.append("")
    L.append("## Recommandation")
    if retard:
        L.append(f"⚠️ {retard} fait(s) à re-sourcer maintenant auprès des sources officielles.")
    elif bientot:
        L.append(f"🟠 {bientot} fait(s) à re-vérifier dans le mois.")
    else:
        L.append("🟢 Tout est frais. Prochaine revue planifiée selon la cadence.")
    L.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    print("═══ RADAR DE FRAÎCHEUR ═══")
    print(f"  Faits suivis : {len(lignes_faits)} | 🔴 retard : {retard} | 🟠 bientôt : {bientot} | cadence : {cadence} j")
    print(f"  → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
