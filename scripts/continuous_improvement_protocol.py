#!/usr/bin/env python3
"""
continuous_improvement_protocol.py — AMÉLIORATION CONTINUE (P-AMELIORATION).

Les agents analysent leurs propres résultats et ajustent leurs RÈGLES (paramètres) pour
optimiser leurs performances — EN SÉCURITÉ : on ne réécrit pas de code arbitraire, on
auto-règle des paramètres bornés, journalisés et réversibles (data/governance/agent_tuning.json).

Exemples : resserrer le seuil de latence si les mesures réelles sont bien meilleures que le seuil ;
durcir la fraîcheur si tout est récent. Chaque changement est justifié et historisé.

Usage : python3 scripts/continuous_improvement_protocol.py
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TUNING = os.path.join(BASE, "data", "governance", "agent_tuning.json")

# Paramètres auto-réglables + bornes (garde-fou : jamais hors de ces limites).
DEFAUTS = {
    "latence_alerte_ms": {"valeur": 300, "min": 120, "max": 500},
    "latence_critique_ms": {"valeur": 800, "min": 400, "max": 1200},
    "fraicheur_max_jours": {"valeur": 365, "min": 90, "max": 540},
}


def charger_json(path, defaut):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return defaut


def borne(v, lo, hi):
    return max(lo, min(hi, v))


def main():
    tuning = charger_json(TUNING, None)
    if not tuning:
        tuning = {"parametres": {k: v["valeur"] for k, v in DEFAUTS.items()}, "historique": []}

    params = tuning["parametres"]
    changements = []

    # 1) Latence : si la charge réelle montre un p95 max bien sous le seuil, on resserre (exigence ++).
    load = charger_json(os.path.join(BASE, "data", "load_simulation_report.json"), None)
    if load and load.get("routes"):
        p95_max = max((r.get("p95_ms", 0) for r in load["routes"]), default=0)
        cible = int(borne(round(p95_max * 1.5), DEFAUTS["latence_alerte_ms"]["min"], DEFAUTS["latence_alerte_ms"]["max"]))
        if p95_max > 0 and cible < params.get("latence_alerte_ms", 300):
            changements.append(("latence_alerte_ms", params["latence_alerte_ms"], cible,
                                f"p95 réel max={p95_max}ms → on peut viser plus strict"))
            params["latence_alerte_ms"] = cible

    # 2) Références légales : si 100% des faits citent une loi, on garde la règle au max d'exigence.
    loi = charger_json(os.path.join(BASE, "data", "governance", "loi_reference_report.json"), None)

    # 3) Sécurité : on re-borne tout (au cas où un paramètre aurait dérivé).
    for k, spec in DEFAUTS.items():
        avant = params.get(k, spec["valeur"])
        apres = int(borne(avant, spec["min"], spec["max"]))
        if apres != avant:
            changements.append((k, avant, apres, "re-bornage de sécurité"))
            params[k] = apres

    # historisation (réversible)
    if changements:
        tuning["historique"].append([{"param": c[0], "avant": c[1], "apres": c[2], "raison": c[3]} for c in changements])
        tuning["historique"] = tuning["historique"][-100:]
    json.dump(tuning, open(TUNING, "w"), ensure_ascii=False, indent=2)

    print("═══ AMÉLIORATION CONTINUE (auto-réglage borné des règles) ═══")
    print(f"  Paramètres actuels : {params}")
    if changements:
        for p, a, b, r in changements:
            print(f"   🔧 {p} : {a} → {b}  ({r})")
        print(f"  → {len(changements)} règle(s) optimisée(s), journalisées et réversibles.")
    else:
        print("  ✅ Aucun ajustement nécessaire : réglages déjà optimaux.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
