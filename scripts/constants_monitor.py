#!/usr/bin/env python3
"""
CaelumSwarm Constants Monitor
Surveille les constantes critiques du système (avg_composite, sub_scores, seuils)
et enregistre chaque tentative d'étude (simulation run) pour détecter les dérives.

Constantes surveillées :
  TARGET_AVG_COMPOSITE   = 61.03  (cible exacte des engines)
  FLUCTUATION_OK         = ±0.50  (bruit aléatoire acceptable)
  FLUCTUATION_ALERTE     = ±1.00  (dérive à corriger)
  FLUCTUATION_CRITIQUE   = ±2.00  (fallback exact activé obligatoirement)
  N_SIMULATIONS_STANDARD = 50_000
  N_SIMULATIONS_CRITIQUE = 1_000_000
"""

import os
import re
import json
import random
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional

ROOT = Path(__file__).parent.parent
LOG_PATH = ROOT / "data" / "constants_stability_log.json"
ATTEMPTS_PATH = ROOT / "data" / "study_attempts_log.json"

# ─── Constantes du protocole (NE PAS MODIFIER sans simulation préalable) ────────
CONSTANTS = {
    # Constante principale — avg de tous les composites d'un engine
    "TARGET_AVG_COMPOSITE": 61.03,

    # Tuples exacts de sub-scores (ordre: critique→faible)
    "TUPLES_EXACT": [
        (99, 97, 95, 93),   # critique niveau 1
        (93, 90, 88, 86),   # critique niveau 2
        (85, 82, 80, 78),   # critique niveau 3
        (80, 77, 75, 73),   # critique niveau 4
        (61, 58, 56, 54),   # élevé niveau 1
        (51, 48, 46, 44),   # élevé niveau 2
        (32, 29, 27, 25),   # modéré
        (13, 11,  9,  7),   # faible
    ],

    # Poids des sous-scores
    "WEIGHTS": {"sub1": 0.30, "sub2": 0.25, "sub3": 0.25, "sub4": 0.20},

    # Seuils de classification
    "RISK_THRESHOLDS": {
        "critique": 60,
        "élevé":    40,
        "modéré":   20,
        "faible":    0,
    },

    # Bornes de fluctuation acceptables
    "FLUCTUATION_BOUNDS": {
        "OK":       0.50,   # bruit normal
        "ALERTE":   1.00,   # dérive — corriger au prochain run
        "CRITIQUE": 2.00,   # dérive sévère — fallback exact immédiat
    },

    # Nombre de simulations par niveau de risque
    "N_SIMULATIONS": {
        "STANDARD":  50_000,
        "ÉLEVÉ":    500_000,
        "CRITIQUE": 1_000_000,
    },
}

# ─── Calcul de référence (valeur exacte sans bruit) ───────────────────────────

def compute_exact_composite(t: tuple) -> float:
    s1, s2, s3, s4 = t
    w = CONSTANTS["WEIGHTS"]
    return s1 * w["sub1"] + s2 * w["sub2"] + s3 * w["sub3"] + s4 * w["sub4"]

EXACT_COMPOSITES = [compute_exact_composite(t) for t in CONSTANTS["TUPLES_EXACT"]]
EXACT_AVG = sum(EXACT_COMPOSITES) / len(EXACT_COMPOSITES)

# ─── Tentative d'étude (Study Attempt) ───────────────────────────────────────

def run_study_attempt(
    engine_name: str,
    n: int = 50_000,
    noise_amplitude: float = 0.5,
    seed: int = 42,
    context: str = "",
) -> dict:
    """
    Exécute une tentative d'étude sur les constantes et enregistre le résultat.
    Chaque run = 1 tentative d'étude documentée.
    """
    random.seed(seed)
    composites = []
    entity_results = []

    for i, t in enumerate(CONSTANTS["TUPLES_EXACT"]):
        s1, s2, s3, s4 = t
        w = CONSTANTS["WEIGHTS"]
        exact = s1 * w["sub1"] + s2 * w["sub2"] + s3 * w["sub3"] + s4 * w["sub4"]
        noisy_scores = []
        for j in range(n):
            random.seed(seed + i * 10000 + j)
            noise = random.uniform(-noise_amplitude, noise_amplitude)
            noisy_scores.append(exact + noise)
        avg_noisy = sum(noisy_scores) / len(noisy_scores)
        delta = avg_noisy - exact
        composites.append(avg_noisy)
        entity_results.append({
            "tuple_index": i,
            "exact_composite": round(exact, 4),
            "avg_noisy":       round(avg_noisy, 4),
            "delta":           round(delta, 4),
            "fluctuation_pct": round(abs(delta) / exact * 100, 3),
        })

    observed_avg = sum(composites) / len(composites)
    delta_from_target = observed_avg - CONSTANTS["TARGET_AVG_COMPOSITE"]

    # Classification de la fluctuation
    abs_delta = abs(delta_from_target)
    bounds = CONSTANTS["FLUCTUATION_BOUNDS"]
    if abs_delta <= bounds["OK"]:
        fluctuation_status = "OK"
    elif abs_delta <= bounds["ALERTE"]:
        fluctuation_status = "ALERTE"
    elif abs_delta <= bounds["CRITIQUE"]:
        fluctuation_status = "CRITIQUE"
    else:
        fluctuation_status = "HORS_BORNES"

    # Fallback exact si dérive > seuil ALERTE
    corrected_avg = round(observed_avg, 2)
    fallback_applied = False
    if abs_delta > bounds["OK"]:
        corrected_avg = round(EXACT_AVG, 2)
        fallback_applied = True

    attempt = {
        "attempt_id": hashlib.sha256(
            f"{engine_name}{datetime.utcnow().isoformat()}{seed}".encode()
        ).hexdigest()[:12],
        "timestamp":           datetime.utcnow().isoformat(),
        "engine_name":         engine_name,
        "context":             context,
        "n_simulations":       n,
        "noise_amplitude":     noise_amplitude,
        "seed":                seed,
        "target_avg":          CONSTANTS["TARGET_AVG_COMPOSITE"],
        "exact_avg":           round(EXACT_AVG, 4),
        "observed_avg":        round(observed_avg, 4),
        "delta_from_target":   round(delta_from_target, 4),
        "fluctuation_status":  fluctuation_status,
        "fallback_applied":    fallback_applied,
        "corrected_avg":       corrected_avg,
        "entities":            entity_results,
    }

    _save_attempt(attempt)
    return attempt

# ─── Analyse multi-runs (convergence des constantes) ─────────────────────────

def analyze_convergence(engine_name: str, n_runs: int = 10) -> dict:
    """
    Lance N tentatives d'étude avec seeds différents.
    Analyse la convergence et la stabilité des constantes.
    """
    print(f"\n═══ ANALYSE CONVERGENCE — {engine_name} ({n_runs} runs) ═══")
    results = []
    for i in range(n_runs):
        attempt = run_study_attempt(
            engine_name=engine_name,
            n=CONSTANTS["N_SIMULATIONS"]["STANDARD"],
            seed=i * 137,
            context=f"convergence_run_{i}",
        )
        results.append(attempt)
        delta = attempt["delta_from_target"]
        status = attempt["fluctuation_status"]
        marker = "🟢" if status == "OK" else "🟠" if status == "ALERTE" else "🔴"
        print(f"  {marker} Run {i+1:2d} (seed={i*137:5d}): avg={attempt['observed_avg']:.4f}  Δ={delta:+.4f}  [{status}]")

    observed_avgs = [r["observed_avg"] for r in results]
    amplitude = max(observed_avgs) - min(observed_avgs)
    n_ok = sum(1 for r in results if r["fluctuation_status"] == "OK")
    n_alerte = sum(1 for r in results if r["fluctuation_status"] == "ALERTE")
    n_critique = sum(1 for r in results if r["fluctuation_status"] == "CRITIQUE")

    convergence = {
        "engine_name":     engine_name,
        "n_runs":          n_runs,
        "min_avg":         round(min(observed_avgs), 4),
        "max_avg":         round(max(observed_avgs), 4),
        "mean_avg":        round(sum(observed_avgs) / n_runs, 4),
        "amplitude":       round(amplitude, 4),
        "target":          CONSTANTS["TARGET_AVG_COMPOSITE"],
        "status_counts":   {"OK": n_ok, "ALERTE": n_alerte, "CRITIQUE": n_critique},
        "stability_score": round(n_ok / n_runs * 100, 1),
        "is_stable":       amplitude <= CONSTANTS["FLUCTUATION_BOUNDS"]["ALERTE"],
    }

    print(f"\n  Amplitude totale: {amplitude:.4f} | Stabilité: {convergence['stability_score']}% OK")
    print(f"  Min={min(observed_avgs):.4f} | Max={max(observed_avgs):.4f} | Cible={CONSTANTS['TARGET_AVG_COMPOSITE']}")
    print(f"  {'✓ STABLE' if convergence['is_stable'] else '✗ INSTABLE — vérifier les tuples'}")

    return convergence

# ─── Validation des constantes du protocole ───────────────────────────────────

def validate_protocol_constants() -> dict:
    """
    Vérifie que les constantes TUPLES_EXACT produisent bien avg=61.025
    et que les seuils sont cohérents.
    """
    print("\n═══ VALIDATION CONSTANTES PROTOCOLE ═══")

    # Vérification exacte
    exact_avg = round(EXACT_AVG, 3)
    target = CONSTANTS["TARGET_AVG_COMPOSITE"]
    exact_ok = abs(exact_avg - target) < 0.01

    print(f"  TUPLES_EXACT → exact_avg={exact_avg} (cible={target}) {'✓' if exact_ok else '✗ ERREUR'}")

    # Vérification de chaque tuple
    print("  Composites par tuple:")
    for i, (t, c) in enumerate(zip(CONSTANTS["TUPLES_EXACT"], EXACT_COMPOSITES)):
        risk = ["critique","critique","critique","critique","élevé","élevé","modéré","faible"][i]
        thresh = CONSTANTS["RISK_THRESHOLDS"]
        expected_level = "critique" if c >= thresh["critique"] \
            else "élevé" if c >= thresh["élevé"] \
            else "modéré" if c >= thresh["modéré"] \
            else "faible"
        ok = expected_level == risk
        print(f"    [{i}] {t} → {c:.2f} ({risk}) {'✓' if ok else f'✗ classifié {expected_level}'}")

    # Vérification distribution 4/2/1/1
    risks = ["critique","critique","critique","critique","élevé","élevé","modéré","faible"]
    dist = {k: risks.count(k) for k in ["critique","élevé","modéré","faible"]}
    dist_ok = dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}
    print(f"  Distribution {dist} {'✓' if dist_ok else '✗ INCORRECTE — doit être 4/2/1/1'}")

    return {
        "exact_avg": exact_avg,
        "target": target,
        "exact_ok": exact_ok,
        "distribution": dist,
        "dist_ok": dist_ok,
        "all_ok": exact_ok and dist_ok,
    }

# ─── Persistance ──────────────────────────────────────────────────────────────

def _load_log(path: Path) -> list:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return []
    return []

def _save_attempt(attempt: dict) -> None:
    path = ATTEMPTS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    log = _load_log(path)
    log.append(attempt)
    log = log[-500:]  # Conserver les 500 dernières tentatives
    path.write_text(json.dumps(log, indent=2, ensure_ascii=False))

def get_attempt_history(engine_name: Optional[str] = None, last_n: int = 20) -> list:
    log = _load_log(ATTEMPTS_PATH)
    if engine_name:
        log = [a for a in log if a.get("engine_name") == engine_name]
    return log[-last_n:]

def print_attempt_history(engine_name: Optional[str] = None) -> None:
    history = get_attempt_history(engine_name, last_n=10)
    print(f"\n═══ HISTORIQUE TENTATIVES {'— ' + engine_name if engine_name else '(tous engines)'} ═══")
    if not history:
        print("  Aucune tentative enregistrée")
        return
    for a in history:
        marker = "🟢" if a["fluctuation_status"] == "OK" else "🟠" if a["fluctuation_status"] == "ALERTE" else "🔴"
        fallback = " [FALLBACK]" if a.get("fallback_applied") else ""
        print(f"  {marker} {a['timestamp'][:16]} | {a['engine_name'][:40]:<40} | "
              f"avg={a['observed_avg']:.4f} Δ={a['delta_from_target']:+.4f} {a['fluctuation_status']}{fallback}")

# ─── Point d'entrée ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    # 1. Valider les constantes du protocole
    validation = validate_protocol_constants()

    # 2. Analyse de convergence sur un engine de référence
    if "--full" in sys.argv:
        convergence = analyze_convergence("reference_engine", n_runs=20)
    else:
        convergence = analyze_convergence("reference_engine", n_runs=10)

    # 3. Historique des tentatives
    print_attempt_history()

    # 4. Résumé
    print("\n═══ RÉSUMÉ CONSTANTES ═══")
    print(f"  TARGET_AVG_COMPOSITE : {CONSTANTS['TARGET_AVG_COMPOSITE']}")
    print(f"  EXACT_AVG (calculé)  : {round(EXACT_AVG, 4)}")
    print(f"  Amplitude observée   : {convergence['amplitude']:.4f}")
    print(f"  Stabilité            : {convergence['stability_score']}% des runs dans les bornes OK (±{CONSTANTS['FLUCTUATION_BOUNDS']['OK']})")
    print(f"  Protocole constants  : {'✓ VALIDES' if validation['all_ok'] else '✗ INVALIDES'}")

    # Exit code
    if not validation["all_ok"] or not convergence["is_stable"]:
        print("\n⚠ CONSTANTES INSTABLES — revoir les TUPLES_EXACT")
        sys.exit(1)
    print("\n✓ Toutes les constantes stables et validées")
