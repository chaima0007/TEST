#!/usr/bin/env python3
"""
rapid_resolution_protocol.py — SYSTÈME DE RÉSOLUTION RAPIDE DES PROBLÈMES.

Honnête : ne résout pas « tout à la vitesse de la lumière » (ça n'existe pas). Mais il rend
la résolution RAPIDE et FIABLE : il détecte, score, priorise, route vers le bon protocole,
calcule une probabilité de résolution, mesure sa propre latence, et journalise tout.

Score de priorité = gravité × urgence × impact (chacun 1..5) → P0 (critique) à P3 (faible).
Routage : associe une catégorie à un protocole/agent existant.
Latence : mesure le temps de traitement (la « vitesse » réelle, affichée en ms).

Usage :
  python3 scripts/rapid_resolution_protocol.py            # démonstration
  python3 scripts/rapid_resolution_protocol.py "fuite de données" --cat securite -g 5 -u 5 -i 5
"""
import json
import sys
import time
import os

LOG = "data/resolution_log.json"

ROUTAGE = {
    "securite": "scripts/security-audit-agent.py + charte R7 (zéro credential)",
    "donnees": "scripts/data-integrity-origin-agent.py + legal_content_verifier.py",
    "juridique": "scripts/legal_content_verifier.py (source officielle obligatoire)",
    "build": "scripts/build_guard.py + certification_protocol.py",
    "qualite": "scripts/certification_protocol.py (P1..P7)",
    "contenu": "scripts/learning_ledger_protocol.py (validation + sourcing)",
    "autre": "triage manuel + decision_protocol.py",
}

NIVEAUX = [(64, "P0_CRITIQUE"), (27, "P1_ELEVE"), (8, "P2_MODERE"), (0, "P3_FAIBLE")]


def classer(score):
    for seuil, nom in NIVEAUX:
        if score >= seuil:
            return nom
    return "P3_FAIBLE"


def probabilite_resolution(gravite, urgence, impact, categorie):
    # Heuristique transparente : un problème bien catégorisé et routable est plus résoluble.
    base = 0.95 if categorie in ROUTAGE and categorie != "autre" else 0.70
    # plus c'est grave/complexe, plus l'incertitude monte légèrement
    penalite = 0.02 * max(0, (gravite + impact) - 6)
    return round(max(0.50, min(0.99, base - penalite)), 2)


def resoudre(probleme, categorie, gravite, urgence, impact):
    t0 = time.perf_counter()
    score = gravite * urgence * impact
    niveau = classer(score)
    route = ROUTAGE.get(categorie, ROUTAGE["autre"])
    proba = probabilite_resolution(gravite, urgence, impact, categorie)
    latence_ms = round((time.perf_counter() - t0) * 1000, 3)
    return {
        "probleme": probleme, "categorie": categorie,
        "gravite": gravite, "urgence": urgence, "impact": impact,
        "score_priorite": score, "niveau": niveau,
        "routage": route, "probabilite_resolution": proba,
        "latence_ms": latence_ms,
    }


def journaliser(resultat):
    log = []
    if os.path.exists(LOG):
        try:
            log = json.load(open(LOG, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            log = []
    log.append(resultat)
    os.makedirs("data", exist_ok=True)
    with open(LOG, "w", encoding="utf-8") as f:
        json.dump(log[-500:], f, indent=2, ensure_ascii=False)


def parse_args(argv):
    probleme = "Démonstration : incohérence de source sur un fait juridique"
    cat, g, u, i = "donnees", 4, 4, 4
    rest = []
    it = iter(range(len(argv)))
    skip = set()
    for idx in range(len(argv)):
        if idx in skip:
            continue
        a = argv[idx]
        if a == "--cat" and idx + 1 < len(argv):
            cat = argv[idx + 1]; skip.add(idx + 1)
        elif a == "-g" and idx + 1 < len(argv):
            g = int(argv[idx + 1]); skip.add(idx + 1)
        elif a == "-u" and idx + 1 < len(argv):
            u = int(argv[idx + 1]); skip.add(idx + 1)
        elif a == "-i" and idx + 1 < len(argv):
            i = int(argv[idx + 1]); skip.add(idx + 1)
        elif not a.startswith("-"):
            rest.append(a)
    if rest:
        probleme = " ".join(rest)
    clamp = lambda x: max(1, min(5, x))
    return probleme, cat, clamp(g), clamp(u), clamp(i)


def main():
    probleme, cat, g, u, i = parse_args(sys.argv[1:])
    r = resoudre(probleme, cat, g, u, i)
    journaliser(r)
    print("═══ RÉSOLUTION RAPIDE ═══")
    print(f"  Problème   : {r['probleme']}")
    print(f"  Catégorie  : {r['categorie']}")
    print(f"  Priorité   : {r['niveau']} (score {r['score_priorite']})")
    print(f"  Routage    : {r['routage']}")
    print(f"  P(résolution) : {int(r['probabilite_resolution']*100)}%")
    print(f"  Latence    : {r['latence_ms']} ms")
    print(f"  → journalisé dans {LOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
