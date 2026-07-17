#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocole de REPRISE — pour toujours repartir où on s'est arrêté.

Lit data/governance/reprise.json (le fil de progression) + le catalogue réel,
et produit data/REPRISE.md : un mémo clair, lisible en 10 secondes au démarrage.

But : après un redémarrage du conteneur, on ouvre REPRISE.md et on sait
exactement quoi faire ensuite. Zéro perte de fil.
"""
import json
import pathlib
from datetime import date

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
GOV = REPO / "data" / "governance"
CAT = REPO / "data" / "belgium" / "_catalogue.json"
REPRISE = GOV / "reprise.json"
OUT = REPO / "data" / "REPRISE.md"


def lire(p, d=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return d


def construire():
    r = lire(REPRISE, {})
    cat = lire(CAT, {})
    tot = cat.get("totaux", {})
    L = []
    L.append("# 🧭 REPRISE — où on en est")
    L.append("")
    L.append(f"*Mémo régénéré le {date.today().isoformat()}. À lire en premier après un redémarrage.*")
    L.append("")
    L.append(f"**Focus actuel :** {r.get('focus_actuel','—')}")
    L.append("")
    L.append("## 👉 Prochaine étape")
    L.append(f"{r.get('prochaine_etape','—')}")
    L.append("")
    if tot:
        L.append("## 📊 État réel (chiffres vérifiés)")
        L.append(f"- Réponses sourcées : **{tot.get('faits','?')}**")
        L.append(f"- Modules : {tot.get('modules','?')} · sources officielles : {tot.get('sources_officielles','?')}")
        L.append(f"- Fiches avec contacts : {tot.get('faits_avec_contacts','?')} · alertes de délai : {tot.get('faits_avec_alerte_delai','?')}")
        L.append("")
    L.append("## ✅ Fait récemment")
    for x in r.get("fait_recemment", []):
        L.append(f"- {x}")
    L.append("")
    L.append("## 📁 Projets")
    for cle, p in r.get("projets", {}).items():
        L.append(f"- **{cle}** — {p.get('etat','')} → *prochaine étape :* {p.get('prochaine_etape','')}")
    L.append("")
    L.append(f"> Règle d'or : {r.get('regle_or','commit + push après chaque étape.')}")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    return r


if __name__ == "__main__":
    r = construire()
    print("═══ POINT DE REPRISE ═══")
    print(f"  Focus : {r.get('focus_actuel','—')}")
    print(f"  Prochaine étape : {r.get('prochaine_etape','—')}")
    print(f"  → {OUT}")
    print("✓ Mémo de reprise à jour (data/REPRISE.md).")
