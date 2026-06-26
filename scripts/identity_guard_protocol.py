#!/usr/bin/env python3
"""
identity_guard_protocol.py — PROTOCOLE EN VIGUEUR : ne jamais oublier ni inventer l'identité.

Garantit deux choses :
  1. Le profil (data/governance/profile.json) contient un VRAI prénom/nom (pas un placeholder).
  2. Aucun document généré ne part avec un placeholder de nom ([PRÉNOM NOM], [À COMPLÉTER]).

Si le profil est encore en placeholder : le protocole le signale clairement (il NE faut pas
inventer — il faut demander le nom). Une fois le profil rempli, ce nom fait foi partout.

Usage :
  python3 scripts/identity_guard_protocol.py            # vérifie profil + documents
  python3 scripts/identity_guard_protocol.py --quiet    # code retour seul
"""
import json
import os
import glob
import sys

PROFILE = "data/governance/profile.json"
PLACEHOLDERS = ["[PRÉNOM NOM]", "[PRENOM NOM]", "[À COMPLÉTER]", "[A COMPLETER]"]
# Documents nominatifs à surveiller (locaux ; les exports Drive en dérivent)
DOCS = ["data/presentation_ecole.md"]


def lire_profil():
    if not os.path.exists(PROFILE):
        return None
    try:
        return json.load(open(PROFILE, encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def main():
    quiet = "--quiet" in sys.argv
    alertes, ok = [], True

    prof = lire_profil()
    if prof is None:
        alertes.append("profil introuvable ou illisible (data/governance/profile.json)")
        ok = False
        prenom = nom = "[À COMPLÉTER]"
        statut = "ABSENT"
    else:
        ident = prof.get("identite", {})
        prenom = ident.get("prenom", "[À COMPLÉTER]")
        nom = ident.get("nom", "[À COMPLÉTER]")
        statut = ident.get("statut", "")
        if any(p in (prenom + nom) for p in PLACEHOLDERS) or "PLACEHOLDER" in statut.upper():
            alertes.append("IDENTITÉ EN ATTENTE → demander le prénom/nom, NE PAS inventer.")
            ok = False

    # Scan des documents nominatifs locaux
    for d in DOCS:
        if not os.path.exists(d):
            continue
        try:
            txt = open(d, encoding="utf-8").read()
        except OSError:
            continue
        if any(p in txt for p in PLACEHOLDERS):
            alertes.append(f"{d} contient encore un placeholder de nom.")
            ok = False

    if not quiet:
        print("═══ PROTOCOLE IDENTITÉ (en vigueur) ═══")
        print(f"  Prénom : {prenom}")
        print(f"  Nom    : {nom}")
        for a in alertes:
            print(f"  ⚠️  {a}")
        if ok:
            print("\n✓ Identité connue et appliquée partout.")
        else:
            print("\n⛔ ACTION REQUISE : compléter data/governance/profile.json avec le vrai nom,")
            print("   puis relancer. Règle absolue : demander, jamais inventer.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
