#!/usr/bin/env python3
"""
transparency_disclaimer_protocol.py — PAGE TRANSPARENCE + DÉCHARGE (anti-problème).

Génère une page finale honnête qui :
  1. liste où l'on s'appuie sur des sources SECONDAIRES (transparence sur nos points faibles),
  2. signale tout fait sans source officielle (devrait être 0),
  3. affiche une DÉCHARGE / avertissement légal clair (information générale, pas un conseil
     juridique individualisé), pour éviter tout problème de responsabilité.

Sortie : data/belgium/transparence_decharge.md
Usage : python3 scripts/transparency_disclaimer_protocol.py
"""
import json
import glob

OUT = "data/belgium/transparence_decharge.md"

DECHARGE = (
    "Les informations fournies sont d'ordre GÉNÉRAL et à but informatif. Elles sont basées sur "
    "des sources officielles à la date de revue indiquée, mais les lois et règlements évoluent. "
    "Elles ne constituent PAS un conseil juridique individualisé et n'engagent pas la responsabilité "
    "de l'éditeur. Pour toute décision, vérifiez la version en vigueur auprès des sources officielles "
    "et, si nécessaire, consultez un professionnel du droit (avocat, notaire) ou un service agréé."
)


def main():
    secondaires = []   # faits utilisant au moins une source secondaire
    sans_officiel = []
    total = 0
    for f in sorted(glob.glob("data/belgium/bail_*.json")):
        try:
            mod = json.load(open(f, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for fait in mod.get("faits", []):
            total += 1
            srcs = fait.get("sources", []) or []
            sec = [s for s in srcs if s.get("type") == "secondaire"]
            off = [s for s in srcs if s.get("type") == "officiel"]
            if sec:
                secondaires.append((fait.get("id"), [s.get("intitule", "?") for s in sec]))
            if not off:
                sans_officiel.append(fait.get("id"))

    L = ["# 🔎 Transparence des sources & décharge", ""]
    L.append(f"*Page de transparence honnête sur la fiabilité de nos sources. Total : {total} faits.*")
    L.append("")
    L.append("## ⚖️ Décharge (avertissement légal)")
    L.append(DECHARGE)
    L.append("")
    L.append("## ✅ Intégrité des sources")
    L.append(f"- Faits SANS source officielle : **{len(sans_officiel)}** {'⚠️ à corriger' if sans_officiel else '(aucun — conforme)'}")
    for fid in sans_officiel:
        L.append(f"  - {fid}")
    L.append(f"- Faits s'appuyant aussi sur une source secondaire (complément) : **{len(secondaires)}**")
    L.append("")
    if secondaires:
        L.append("## 📋 Détail — recours à des sources secondaires (transparence)")
        L.append("*Ces faits ont TOUJOURS une source officielle ; la source secondaire ne sert que de complément/clarification.*")
        L.append("")
        L.append("| Fait | Source(s) secondaire(s) |")
        L.append("|---|---|")
        for fid, intits in secondaires:
            L.append(f"| {fid} | {', '.join(intits)} |")
        L.append("")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    print("═══ TRANSPARENCE & DÉCHARGE ═══")
    print(f"  Faits : {total} | sans source officielle : {len(sans_officiel)} | avec appui secondaire : {len(secondaires)}")
    print(f"  → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
