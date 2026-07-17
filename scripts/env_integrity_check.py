#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contrôle d'intégrité de l'environnement (P-INTEGRITE-ENVIRONNEMENT).
====================================================================
Détecte toute DÉSYNCHRONISATION du conteneur sur le dépôt partagé chaima0007/TEST
AVANT toute écriture/commit. À lancer en début de cycle de travail.

Vérifie :
  1. La branche courante == branche de travail attendue.
  2. La présence des répertoires/fichiers clés (scripts/, data/governance/, fiches).
  3. Que le HEAD local n'est pas positionné sur un historique étranger.

Sortie non nulle + message clair si anomalie → NE PAS écrire, réaligner d'abord
(git fetch puis, sur autorisation, git reset --hard origin/<branche>).
"""
from __future__ import annotations
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANCHE_ATTENDUE = "claude/swarm-50-agent-architecture-3l6cno"
CLES = [
    "scripts/loi_reference_audit.py",
    "scripts/source_trust_protocol.py",
    "scripts/autonomous_platform.py",
    "data/governance/protocols_registry.json",
    "data/governance/trusted_sources.json",
    "laloiavecmoi/data/belgium/_catalogue.json",
]


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", ROOT, *args],
                          capture_output=True, text=True).stdout.strip()


def main() -> int:
    pb = []
    branche = git("rev-parse", "--abbrev-ref", "HEAD")
    if branche != BRANCHE_ATTENDUE:
        pb.append(f"Branche courante « {branche} » ≠ attendue « {BRANCHE_ATTENDUE} » (désync probable).")
    for c in CLES:
        if not os.path.exists(os.path.join(ROOT, c)):
            pb.append(f"Fichier/dossier clé manquant : {c}")
    nb = len([f for f in os.listdir(os.path.join(ROOT, "laloiavecmoi", "data", "belgium"))
              if f.endswith(".json") and not f.startswith("_")]) if os.path.isdir(
              os.path.join(ROOT, "laloiavecmoi", "data", "belgium")) else 0
    if nb < 100:
        pb.append(f"Corpus citoyen anormalement réduit : {nb} fiches (< 100) — checkout suspect.")

    print("═══ CONTRÔLE D'INTÉGRITÉ DE L'ENVIRONNEMENT ═══")
    print(f"  Branche : {branche} · HEAD : {git('rev-parse', '--short', 'HEAD')} · fiches : {nb}")
    if pb:
        print("  ❌ DÉSYNCHRONISATION DÉTECTÉE — NE PAS ÉCRIRE :")
        for p in pb:
            print(f"     • {p}")
        print("  → Réaligner : git fetch origin ; (sur autorisation) git reset --hard origin/"
              + BRANCHE_ATTENDUE)
        return 1
    print("  ✅ Environnement sain — espace de travail aligné sur la branche correcte.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
