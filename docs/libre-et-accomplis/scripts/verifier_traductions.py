#!/usr/bin/env python3
"""Libre & Accomplis — Vérification des traductions.

Vérifie que toutes les langues du fichier de traductions contiennent
exactement les mêmes clés que la langue de référence (la première).
Sort avec le code 1 si des clés manquent ou sont en trop, ce qui permet
de brancher ce script dans la CI (règle d'or : validation multilingue).

Usage :
    python3 verifier_traductions.py [chemin/vers/messages.json]
"""
import json
import sys
from pathlib import Path

FICHIER_PAR_DEFAUT = Path(__file__).resolve().parent.parent / "traductions" / "messages.json"


def verifier(fichier: Path) -> int:
    data = json.loads(fichier.read_text(encoding="utf-8"))
    langues = list(data.keys())
    if not langues:
        print("❌ Aucune langue trouvée dans le fichier.")
        return 1

    reference = langues[0]
    cles_reference = set(data[reference])
    print(f"Langue de référence : {reference} ({len(cles_reference)} clés)")

    erreurs = 0
    for langue in langues[1:]:
        cles = set(data[langue])
        manquantes = cles_reference - cles
        en_trop = cles - cles_reference
        if manquantes:
            print(f"❌ {langue} : clés manquantes -> {sorted(manquantes)}")
            erreurs += 1
        if en_trop:
            print(f"❌ {langue} : clés en trop -> {sorted(en_trop)}")
            erreurs += 1
        if not manquantes and not en_trop:
            print(f"✅ {langue} : toutes les clés sont traduites.")

        vides = [cle for cle, valeur in data[langue].items() if not str(valeur).strip()]
        if vides:
            print(f"❌ {langue} : traductions vides -> {sorted(vides)}")
            erreurs += 1

    if erreurs:
        print(f"\n❌ Validation multilingue échouée ({erreurs} problème(s)).")
        return 1
    print(f"\n✅ Validation multilingue réussie pour {len(langues)} langues.")
    return 0


if __name__ == "__main__":
    cible = Path(sys.argv[1]) if len(sys.argv) > 1 else FICHIER_PAR_DEFAUT
    sys.exit(verifier(cible))
