#!/usr/bin/env python3
"""
tba_protocol.py — Tableau de Bord d'Avancement (P-TBA).

Référence opérationnelle unique pour la continuité entre sessions :
  - lit data/governance/tba.json (état réel par projet/tâche, % d'avancement) ;
  - calcule l'avancement global de chaque projet et de la flotte ;
  - rend un tableau Markdown consultable à tout moment (data/TBA.md) avec des jauges ;
  - valide la cohérence (pourcentages 0..100) et journalise le point de sortie.

Mise à jour : éditer data/governance/tba.json puis relancer (ou via l'orchestrateur).

Usage : python3 scripts/tba_protocol.py
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TBA = os.path.join(BASE, "data", "governance", "tba.json")
OUT = os.path.join(BASE, "data", "TBA.md")


def jauge(pct, largeur=20):
    pct = max(0, min(100, int(round(pct))))
    plein = round(pct / 100 * largeur)
    return "█" * plein + "░" * (largeur - plein)


def avancement_projet(projet):
    taches = projet.get("taches", [])
    if not taches:
        return 0
    return round(sum(t.get("pct", 0) for t in taches) / len(taches))


def main():
    try:
        d = json.load(open(TBA, encoding="utf-8"))
    except Exception as e:
        print(f"⛔ TBA illisible : {e}")
        return 1

    projets = d.get("projets", [])
    # validation
    erreurs = []
    for p in projets:
        for t in p.get("taches", []):
            pct = t.get("pct")
            if not isinstance(pct, (int, float)) or not (0 <= pct <= 100):
                erreurs.append(f"{p['nom']} / {t.get('nom','?')} : pct invalide ({pct})")
    if erreurs:
        for e in erreurs[:10]:
            print(f"  ⛔ {e}")
        return 1

    globaux = [(p["nom"], avancement_projet(p)) for p in projets]
    flotte = round(sum(g[1] for g in globaux) / len(globaux)) if globaux else 0

    lignes = []
    lignes.append("# 📊 Tableau de Bord d'Avancement — Caelum Partners")
    lignes.append("")
    lignes.append(f"_Dernière mise à jour : {d.get('derniere_mise_a_jour','n/a')}_")
    lignes.append("")
    lignes.append(f"## 🚀 Avancement global de la flotte : **{flotte}%**")
    lignes.append(f"`{jauge(flotte)}` {flotte}%")
    lignes.append("")
    for nom, g in globaux:
        lignes.append(f"- **{nom}** — `{jauge(g, 14)}` {g}%")
    lignes.append("")

    for p in projets:
        g = avancement_projet(p)
        lignes.append(f"## {p['nom']} — {g}%")
        lignes.append(f"`{jauge(g)}` {g}%")
        lignes.append("")
        lignes.append(f"> **Point de sortie :** {p.get('point_de_sortie','—')}")
        lignes.append("")
        lignes.append("| Tâche | Avancement | Statut |")
        lignes.append("|---|---|---|")
        for t in p.get("taches", []):
            lignes.append(f"| {t['nom']} | `{jauge(t['pct'], 12)}` {t['pct']}% | {t.get('statut','')} |")
        lignes.append("")
        for t in p.get("taches", []):
            if t.get("prochaines_etapes"):
                lignes.append(f"- **{t['nom']}** → prochaines étapes : {', '.join(t['prochaines_etapes'])}")
        lignes.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))

    print("═══ TABLEAU DE BORD D'AVANCEMENT (TBA) ═══")
    for nom, g in globaux:
        print(f"  {jauge(g, 16)} {g:3d}%  {nom}")
    print(f"  → Flotte globale : {flotte}% · rapport : data/TBA.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
