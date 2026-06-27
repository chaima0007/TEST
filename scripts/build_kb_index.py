#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construit la BASE UNIQUE (catalogue central) — La Loi Avec Moi.

Une seule structure qui voit TOUT : chaque module reste un fichier séparé
(rien n'est mélangé), mais ce catalogue les unifie et les organise par domaine,
en croisant avec la taxonomie du droit belge.

Source de vérité : data/belgium/*.json + data/governance/domaines_droit_belge.json
Sortie : data/belgium/_catalogue.json (machine) + data/belgium/catalogue.md (lisible)
"""
import json
import pathlib
from datetime import date

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
DATA = REPO / "data" / "belgium"
GOV = REPO / "data" / "governance"
OUT_JSON = DATA / "_catalogue.json"
OUT_MD = DATA / "catalogue.md"


def lire_json(p, defaut=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return defaut


def construire():
    taxo = lire_json(GOV / "domaines_droit_belge.json", {"domaines": []})
    # index module -> domaine
    mod2dom = {}
    for d in taxo.get("domaines", []):
        for m in d.get("modules", []):
            mod2dom[m] = d["nom"]

    modules = []
    total_faits = total_off = total_contacts = total_alertes = 0
    for fp in sorted(DATA.glob("*.json")):
        if fp.name.startswith("_"):
            continue
        d = lire_json(fp, {})
        faits = d.get("faits", [])
        nb_off = sum(1 for f in faits for s in f.get("sources", []) if s.get("type") == "officiel")
        nb_contacts = sum(1 for f in faits if f.get("contacts"))
        nb_alertes = sum(1 for f in faits if f.get("alerte_delai"))
        total_faits += len(faits)
        total_off += nb_off
        total_contacts += nb_contacts
        total_alertes += nb_alertes
        modules.append({
            "fichier": fp.name,
            "module": d.get("module", fp.stem),
            "titre": d.get("titre", fp.stem),
            "domaine": d.get("domaine") or mod2dom.get(d.get("module", ""), "—"),
            "juridiction": d.get("juridiction", ""),
            "faits": len(faits),
            "sources_officielles": nb_off,
            "faits_avec_contacts": nb_contacts,
            "faits_avec_alerte_delai": nb_alertes,
            "derniere_revue": d.get("derniere_revue", ""),
        })

    catalogue = {
        "catalogue": "Base unique — La Loi Avec Moi",
        "genere_le": date.today().isoformat(),
        "totaux": {
            "modules": len(modules),
            "faits": total_faits,
            "sources_officielles": total_off,
            "faits_avec_contacts": total_contacts,
            "faits_avec_alerte_delai": total_alertes,
        },
        "modules": modules,
        "domaines": taxo.get("domaines", []),
    }
    OUT_JSON.write_text(json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # version lisible
    L = ["# Base unique — catalogue central", "",
         f"*Généré le {catalogue['genere_le']}. Une seule base, organisée par domaine. "
         "Chaque module reste séparé (rien n'est mélangé).*", "",
         f"**{total_faits} réponses · {len(modules)} modules · {total_off} sources officielles · "
         f"{total_contacts} fiches avec contacts · {total_alertes} alertes de délai**", "",
         "## Modules en ligne", "",
         "| Domaine | Module | Réponses | Sources off. | Contacts | Délais |",
         "|---|---|---|---|---|---|"]
    for m in modules:
        L.append(f"| {m['domaine']} | {m['titre']} | {m['faits']} | {m['sources_officielles']} | "
                 f"{m['faits_avec_contacts']} | {m['faits_avec_alerte_delai']} |")
    L += ["", "## Couverture des domaines du droit belge", "",
          "| Domaine | Statut | Priorité |", "|---|---|---|"]
    for d in catalogue["domaines"]:
        L.append(f"| {d['nom']} | {d['statut']} | {d.get('priorite','')} |")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    return catalogue


if __name__ == "__main__":
    c = construire()
    t = c["totaux"]
    print("═══ BASE UNIQUE — catalogue central ═══")
    print(f"  Modules : {t['modules']} | Réponses : {t['faits']}")
    print(f"  Sources officielles : {t['sources_officielles']}")
    print(f"  Fiches avec contacts : {t['faits_avec_contacts']} | alertes de délai : {t['faits_avec_alerte_delai']}")
    couverts = sum(1 for d in c["domaines"] if d["statut"] == "couvert")
    print(f"  Domaines couverts : {couverts}/{len(c['domaines'])}")
    print(f"  → {OUT_JSON.name} + {OUT_MD.name}")
    print("✓ Base unique générée (modules séparés, accès unifié).")
