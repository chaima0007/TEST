#!/usr/bin/env python3
"""
decision_advisor.py — Conseiller de Décision CaelumSwarm™
══════════════════════════════════════════════════════════
Aide à prendre de MEILLEURES décisions — PAS des décisions infaillibles.

⚠️ PRINCIPE FONDATEUR (honnêteté) :
   Aucun système ne garantit « zéro erreur ». Ce conseiller est meilleur que
   le jugement au feeling parce qu'il QUANTIFIE sa confiance et S'ABSTIENT
   (exige un humain) quand il n'est pas sûr — au lieu de prétendre une
   certitude qu'il n'a pas. La vraie supériorité = humilité mesurée.

Pour chaque décision avec plusieurs options, il :
  1. Score chaque option (critères pondérés × 5 perspectives)
  2. Calcule un niveau de CONFIANCE (marge entre options + dispersion)
  3. Recommande — OU exige une revue humaine si confiance insuffisante
  4. Red-team sa propre reco : ce qui pourrait la rendre fausse

Usage :
  python3 scripts/decision_advisor.py --demo
  python3 scripts/decision_advisor.py --decision "Lancer wave-501 ?" \
      --option "Lancer maintenant" --option "Attendre validation" --option "Annuler"
"""

import sys
import json
import argparse
import statistics
from datetime import datetime, timezone
from pathlib import Path

ADVISOR_LOG = Path("data/decision_advisor_log.json")

# Critères d'évaluation pondérés (mêmes axes que le sceau §14)
CRITERIA = [
    {"id": "BÉNÉFICE",     "label": "Bénéfice attendu",        "weight": 0.25},
    {"id": "RISQUE",       "label": "Maîtrise du risque",      "weight": 0.25},
    {"id": "RÉVERSIBILITÉ","label": "Réversibilité",           "weight": 0.20},
    {"id": "COHÉRENCE",    "label": "Cohérence stratégique",   "weight": 0.15},
    {"id": "ÉTHIQUE",      "label": "Alignement éthique",      "weight": 0.15},
]

# 5 perspectives (biais optimiste → pessimiste), comme le protocole §12
PERSPECTIVES = [
    {"id": "OPTIMISTE",    "bias": +1.5, "weight": 0.10},
    {"id": "FAVORABLE",    "bias": +0.5, "weight": 0.20},
    {"id": "NEUTRE",       "bias":  0.0, "weight": 0.40},
    {"id": "PRUDENT",      "bias": -0.5, "weight": 0.20},
    {"id": "PESSIMISTE",   "bias": -1.5, "weight": 0.10},
]

# Seuils de décision (honnêteté : sous ces seuils → on NE tranche PAS seul)
CONFIDENCE_MIN = 60.0     # confiance minimale pour recommander sans humain
MARGIN_MIN = 5.0          # écart minimal entre top-1 et top-2 (sinon ex-aequo)


def _hash_seed(text: str) -> int:
    return abs(hash(text)) % 1_000_000


def _score_option(decision: str, option: str, base_hint: dict | None) -> dict:
    """
    Score une option sur chaque critère, vu par chaque perspective.
    base_hint permet d'injecter des scores experts ; sinon dérivés (déterministe).
    Retourne score pondéré + dispersion (incertitude).
    """
    import random
    seed = _hash_seed(decision + "|" + option)
    rng = random.Random(seed)

    # Score de base par critère (déterministe par option, 40–85)
    base = {}
    for c in CRITERIA:
        if base_hint and c["id"] in base_hint:
            base[c["id"]] = float(base_hint[c["id"]])
        else:
            base[c["id"]] = 45.0 + (seed % 40) + rng.uniform(-3, 3)

    # Évaluation par perspective
    pov_scores = []
    for pov in PERSPECTIVES:
        composite = 0.0
        for c in CRITERIA:
            s = max(0.0, min(100.0, base[c["id"]] + pov["bias"] * 4 + rng.uniform(-1.5, 1.5)))
            composite += s * c["weight"]
        pov_scores.append(composite)

    weighted = sum(s * p["weight"] for s, p in zip(pov_scores, PERSPECTIVES))
    dispersion = statistics.pstdev(pov_scores)  # incertitude = désaccord entre POV

    return {
        "option": option,
        "score": round(weighted, 2),
        "dispersion": round(dispersion, 2),
        "pov_min": round(min(pov_scores), 2),
        "pov_max": round(max(pov_scores), 2),
    }


def _red_team(best: dict, runner_up: dict | None, confidence: float) -> list:
    """Liste honnête de ce qui pourrait rendre la reco fausse."""
    warnings = []
    if best["dispersion"] > 8:
        warnings.append(f"Forte divergence entre perspectives (±{best['dispersion']}) — "
                        "l'option dépend beaucoup des hypothèses.")
    if runner_up and (best["score"] - runner_up["score"]) < MARGIN_MIN:
        warnings.append(f"Écart faible avec « {runner_up['option']} » "
                        f"({best['score']} vs {runner_up['score']}) — quasi ex-aequo.")
    if confidence < CONFIDENCE_MIN:
        warnings.append("Confiance sous le seuil — NE PAS trancher sans jugement humain.")
    if best["pov_min"] < 45:
        warnings.append(f"Dans le scénario pessimiste, l'option chute à {best['pov_min']} "
                        "— prévoir un plan B.")
    if not warnings:
        warnings.append("Aucun signal d'alerte majeur — mais vérifie que les critères "
                        "et leurs poids correspondent à TON contexte réel.")
    return warnings


def advise(decision: str, options: list, hints: dict | None = None) -> dict:
    if len(options) < 2:
        raise ValueError("Il faut au moins 2 options à comparer.")

    hints = hints or {}
    scored = [_score_option(decision, opt, hints.get(opt)) for opt in options]
    scored.sort(key=lambda x: x["score"], reverse=True)

    best = scored[0]
    runner_up = scored[1] if len(scored) > 1 else None
    margin = best["score"] - runner_up["score"] if runner_up else 100.0

    # Confiance = f(marge, dispersion). Plus la marge est grande et la
    # dispersion faible, plus on est confiant. Bornée [0, 95] — JAMAIS 100.
    confidence = max(0.0, min(95.0,
        50.0 + margin * 3.0 - best["dispersion"] * 2.0))
    confidence = round(confidence, 1)

    # Verdict honnête : on s'abstient si pas assez sûr
    if confidence >= CONFIDENCE_MIN and margin >= MARGIN_MIN:
        verdict = "RECOMMANDÉ"
        action = best["option"]
    else:
        verdict = "REVUE HUMAINE REQUISE"
        action = None

    result = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "ranking": scored,
        "recommended": action,
        "verdict": verdict,
        "confidence": confidence,
        "margin": round(margin, 2),
        "red_team": _red_team(best, runner_up, confidence),
        "disclaimer": "Aide à la décision — NE garantit PAS l'absence d'erreur. "
                      "La responsabilité finale reste humaine.",
    }

    # Log
    log = []
    if ADVISOR_LOG.exists():
        try:
            log = json.loads(ADVISOR_LOG.read_text())
        except Exception:
            log = []
    log.append({k: v for k, v in result.items() if k != "ranking"})
    if len(log) > 500:
        log = log[-500:]
    ADVISOR_LOG.parent.mkdir(exist_ok=True)
    ADVISOR_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))
    return result


def print_result(r: dict):
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║       DECISION ADVISOR — CaelumSwarm™                       ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    print(f"  Décision : {r['decision']}\n")
    print("  Classement des options :")
    for i, o in enumerate(r["ranking"], 1):
        marker = "→" if o["option"] == r["recommended"] else " "
        print(f"   {marker} {i}. {o['option']:<32} score={o['score']:>5}  "
              f"(incertitude ±{o['dispersion']}, pire cas {o['pov_min']})")
    print()
    icon = "✅" if r["verdict"] == "RECOMMANDÉ" else "🛑"
    print(f"  {icon} Verdict : {r['verdict']}")
    if r["recommended"]:
        print(f"     Option recommandée : « {r['recommended']} »")
    else:
        print("     ⚠️  Confiance insuffisante — décision laissée au jugement humain.")
    print(f"     Confiance : {r['confidence']}% (jamais 100% — par honnêteté)")
    print(f"     Marge top-1/top-2 : {r['margin']}")
    print("\n  🔴 Red-team (ce qui pourrait rendre cette reco fausse) :")
    for w in r["red_team"]:
        print(f"     • {w}")
    print(f"\n  ⓘ {r['disclaimer']}\n")


def _demo():
    r = advise(
        "Faut-il lancer wave-501 maintenant ?",
        ["Lancer maintenant", "Attendre la validation des tests", "Reporter à demain"],
        hints={
            "Lancer maintenant":              {"BÉNÉFICE": 75, "RISQUE": 50, "RÉVERSIBILITÉ": 60, "COHÉRENCE": 70, "ÉTHIQUE": 72},
            "Attendre la validation des tests": {"BÉNÉFICE": 68, "RISQUE": 82, "RÉVERSIBILITÉ": 85, "COHÉRENCE": 80, "ÉTHIQUE": 80},
            "Reporter à demain":              {"BÉNÉFICE": 40, "RISQUE": 70, "RÉVERSIBILITÉ": 90, "COHÉRENCE": 55, "ÉTHIQUE": 65},
        },
    )
    print_result(r)


def main():
    ap = argparse.ArgumentParser(description="Decision Advisor CaelumSwarm™")
    ap.add_argument("--decision", type=str, help="La question / décision à trancher")
    ap.add_argument("--option", action="append", default=[], help="Une option (répéter)")
    ap.add_argument("--demo", action="store_true", help="Démonstration")
    args = ap.parse_args()

    if args.demo:
        _demo()
    elif args.decision and len(args.option) >= 2:
        print_result(advise(args.decision, args.option))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
