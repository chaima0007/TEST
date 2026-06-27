#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère un SPÉCIALISTE par catégorie (domaine), à partir des modules sourcés.

But : pour chaque domaine, un « spécialiste » (assistant guidé) qui aide la
personne à comprendre et FAIRE VALOIR ses droits, à partir des sources officielles.

Honnête : ce sont des assistants guidés (contenu vérifié + contacts utiles),
pas des avocats. Ils renvoient toujours vers les sources officielles et, au
besoin, vers un professionnel.

Source de vérité : data/belgium/*.json (modules)
Sortie : data/governance/specialistes.json
"""
import json
import glob
import os
import pathlib
from datetime import date

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
DATA = REPO / "data" / "belgium"
OUT = REPO / "data" / "governance" / "specialistes.json"


def construire():
    specialistes = []
    for fp in sorted(glob.glob(str(DATA / "*.json"))):
        if os.path.basename(fp).startswith("_"):
            continue
        d = json.loads(pathlib.Path(fp).read_text(encoding="utf-8"))
        faits = d.get("faits", [])
        if not faits:
            continue
        domaine = d.get("domaine") or d.get("titre", "")
        # contacts agrégés (uniques) du domaine
        contacts, vus = [], set()
        for f in faits:
            for c in f.get("contacts", []):
                cle = (c.get("nom", ""), c.get("numero", ""), c.get("lien", ""))
                if cle not in vus and c.get("nom"):
                    vus.add(cle)
                    contacts.append(c)
        questions = [f.get("question", "") for f in faits]
        specialistes.append({
            "id": "SPE-" + d.get("module", os.path.basename(fp)).upper().replace("_", "-"),
            "titre": f"Spécialiste — {domaine}",
            "domaine": domaine,
            "module": d.get("module", ""),
            "mission": (f"Vous aider à comprendre et à faire valoir vos droits en matière de "
                        f"« {domaine.lower()} », à partir de sources officielles, et vous orienter "
                        f"vers le bon interlocuteur."),
            "peut_vous_aider_a": questions,
            "contacts_cles": contacts,
            "nb_reponses": len(faits),
            "gouvernance": "Soumis à tous les protocoles (sources officielles, date de vérification, "
                           "pas d'invention). Ne remplace pas un avocat ; renvoie vers la source et, si besoin, un professionnel.",
        })
    obj = {
        "registre": "Spécialistes par catégorie",
        "but": "Un assistant guidé par domaine pour aider chacun à faire valoir ses droits.",
        "genere_le": date.today().isoformat(),
        "principe_honnete": "Assistants guidés (contenu vérifié + contacts), pas des avocats.",
        "specialistes": specialistes,
    }
    OUT.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return specialistes


if __name__ == "__main__":
    s = construire()
    print("═══ SPÉCIALISTES PAR CATÉGORIE ═══")
    for x in s:
        print(f"  • {x['titre']} ({x['nb_reponses']} réponses, {len(x['contacts_cles'])} contacts)")
    print(f"  Total : {len(s)} spécialistes → {OUT.name}")
    print("✓ Un spécialiste par domaine (généré depuis les modules sourcés).")
