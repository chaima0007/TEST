#!/usr/bin/env python3
"""
control_gates_protocol.py — SAS DE CONTRÔLE (quality gates) anti-surcharge.

Principe : au lieu de tout lancer tout le temps (surcharge), on traverse des SAS successifs.
Chaque sas ne lance que les contrôles pertinents, et on S'ARRÊTE au premier sas rouge
(comme un sas étanche : impossible d'avancer si le précédent n'est pas validé).

Doublage RAISONNÉ (sobriété) : on ne double PAS partout. On double seulement au SAS CRITIQUE
(avant livraison/irréversible) avec une 2ᵉ vérification indépendante = défense en profondeur
là où le risque le justifie.

Sas :
  SAS 1 — ENTRÉE      : identité (qui, profil correct)
  SAS 2 — INTÉGRITÉ   : certification (compile, JSON, non-régression, préfixes)
  SAS 3 — CONTENU     : sources officielles obligatoires
  SAS 4 — LIVRAISON*  : DOUBLE contrôle indépendant (identité + contenu) avant tout envoi/commit

Usage :
  python3 scripts/control_gates_protocol.py            # traverse tous les sas
  python3 scripts/control_gates_protocol.py --until 2  # s'arrête après le sas 2
"""
import subprocess
import sys

PY = sys.executable

SAS = [
    ("SAS 1 — ENTRÉE (identité)", [
        [PY, "scripts/identity_guard_protocol.py", "--quiet"],
    ]),
    ("SAS 2 — INTÉGRITÉ (certification)", [
        [PY, "scripts/certification_protocol.py", "--quiet"],
    ]),
    ("SAS 3 — CONTENU (sources officielles)", [
        [PY, "scripts/legal_content_verifier.py"],
    ]),
    ("SAS 4 — LIVRAISON (double contrôle indépendant)", [
        [PY, "scripts/identity_guard_protocol.py", "--quiet"],   # 1ère passe
        [PY, "scripts/legal_content_verifier.py"],               # 2ᵉ passe indépendante
    ]),
]


def lancer(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0


def main():
    until = None
    if "--until" in sys.argv:
        until = int(sys.argv[sys.argv.index("--until") + 1])

    print("═══ SAS DE CONTRÔLE — passage étanche ═══")
    for i, (nom, cmds) in enumerate(SAS, start=1):
        ok = all(lancer(c) for c in cmds)
        marque = "✓" if ok else "✗"
        double = " (×2 indépendant)" if len(cmds) > 1 else ""
        print(f"  {marque} {nom}{double}")
        if not ok:
            print(f"\n⛔ BLOQUÉ au {nom}. On n'avance pas tant que ce sas n'est pas vert.")
            print("   → corriger, puis relancer. (Sas étanche = zéro surcharge inutile en aval.)")
            return 1
        if until and i >= until:
            print(f"\n⏸  Arrêt demandé après le sas {i}. Tout vert jusqu'ici.")
            return 0

    print("\n✓ TOUS LES SAS FRANCHIS — livraison autorisée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
