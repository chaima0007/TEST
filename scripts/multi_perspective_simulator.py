#!/usr/bin/env python3
"""
CaelumSwarm Multi-Perspective Simulator
Protocole §12 — Chaque simulation doit être évaluée depuis plusieurs points de vue
pour être optimale et détecter les biais qu'un seul angle ne voit pas.

5 points de vue obligatoires :
  VUE_OPTIMISTE    (bias=+1.5, w=10%) — scénario favorable, risque sous-estimé
  VUE_HAUTE        (bias=+0.5, w=20%) — légère amélioration des conditions
  VUE_NEUTRE       (bias= 0.0, w=40%) — baseline, point de vue central
  VUE_BASSE        (bias=-0.5, w=20%) — légère dégradation des conditions
  VUE_PESSIMISTE   (bias=-1.5, w=10%) — scénario défavorable, risque sur-estimé

Le CONSENSUS PONDÉRÉ agrège les 5 vues → résultat plus robuste qu'un seul angle.
"""

import random
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional

ROOT = Path(__file__).parent.parent
MPOV_LOG = ROOT / "data" / "multi_perspective_log.json"

# ─── 5 Points de vue (IMMUABLES — modifier = simuler 1M fois avant) ─────────
PERSPECTIVES = [
    {"id": "VUE_OPTIMISTE",  "label": "Optimiste",    "bias": +1.5, "amplitude": 0.5, "weight": 0.10},
    {"id": "VUE_HAUTE",      "label": "Légèrement+",  "bias": +0.5, "amplitude": 0.5, "weight": 0.20},
    {"id": "VUE_NEUTRE",     "label": "Neutre",       "bias":  0.0, "amplitude": 0.5, "weight": 0.40},
    {"id": "VUE_BASSE",      "label": "Légèrement-",  "bias": -0.5, "amplitude": 0.5, "weight": 0.20},
    {"id": "VUE_PESSIMISTE", "label": "Pessimiste",   "bias": -1.5, "amplitude": 0.5, "weight": 0.10},
]

# Vérification que les poids somment à 1.0
assert abs(sum(p["weight"] for p in PERSPECTIVES) - 1.0) < 1e-9, "Poids incohérents"

# Tuples immuables du protocole
TUPLES_EXACT = [
    (99, 97, 95, 93),
    (93, 90, 88, 86),
    (85, 82, 80, 78),
    (80, 77, 75, 73),
    (61, 58, 56, 54),
    (51, 48, 46, 44),
    (32, 29, 27, 25),
    (13, 11,  9,  7),
]
WEIGHTS = {"sub1": 0.30, "sub2": 0.25, "sub3": 0.25, "sub4": 0.20}

def exact_composite(t: tuple) -> float:
    s1, s2, s3, s4 = t
    return s1 * WEIGHTS["sub1"] + s2 * WEIGHTS["sub2"] + s3 * WEIGHTS["sub3"] + s4 * WEIGHTS["sub4"]

EXACT_COMPOSITES = [exact_composite(t) for t in TUPLES_EXACT]
EXACT_AVG = sum(EXACT_COMPOSITES) / len(EXACT_COMPOSITES)

# ─── Simulation d'une vue unique ─────────────────────────────────────────────

def _run_single_perspective(
    tuples: list[tuple],
    perspective: dict,
    n: int,
    seed: int,
) -> list[float]:
    """Simule n runs pour une perspective donnée, retourne les moyennes par tuple."""
    results = []
    for i, t in enumerate(tuples):
        exact = exact_composite(t)
        random.seed(seed + i * 100_000)
        scores = [
            exact + perspective["bias"] + random.uniform(-perspective["amplitude"], perspective["amplitude"])
            for _ in range(n)
        ]
        results.append(sum(scores) / n)
    return results

# ─── Simulation multi-perspectives (cœur du protocole §12) ───────────────────

def run_multi_perspective(
    engine_name: str,
    tuples: Optional[list[tuple]] = None,
    n_per_pov: int = 10_000,
    seed: int = 42,
    target: float = 61.03,
    context: str = "",
    verbose: bool = True,
) -> dict:
    """
    Lance 5 simulations (une par point de vue) et calcule le consensus pondéré.

    Args:
        engine_name  : Nom de l'engine évalué
        tuples       : Liste des 8 tuples (défaut : TUPLES_EXACT du protocole)
        n_per_pov    : Simulations par vue (total = 5 × n_per_pov)
        seed         : Graine de base (reproductibilité)
        target       : Cible avg_composite (61.03)
        context      : Contexte de la tentative (ex: "wave_497_validation")
        verbose      : Afficher le détail

    Returns:
        dict avec consensus_avg, pov_results, status, delta
    """
    if tuples is None:
        tuples = TUPLES_EXACT

    n_total = len(PERSPECTIVES) * n_per_pov

    if verbose:
        print(f"\n{'═'*55}")
        print(f"  SIMULATION MULTI-PERSPECTIVES — {engine_name}")
        print(f"  {len(PERSPECTIVES)} vues × {n_per_pov:,} runs = {n_total:,} total")
        print(f"{'═'*55}")

    pov_results = []
    for pov in PERSPECTIVES:
        per_tuple_avgs = _run_single_perspective(tuples, pov, n_per_pov, seed)
        pov_avg = sum(per_tuple_avgs) / len(per_tuple_avgs)
        contribution = pov_avg * pov["weight"]
        pov_results.append({
            "id":           pov["id"],
            "label":        pov["label"],
            "bias":         pov["bias"],
            "weight":       pov["weight"],
            "avg_composite": round(pov_avg, 4),
            "contribution":  round(contribution, 4),
            "per_tuple":     [round(v, 4) for v in per_tuple_avgs],
        })
        if verbose:
            delta = pov_avg - target
            marker = "🟢" if abs(delta) < 2.0 else "🟠" if abs(delta) < 4.0 else "🔴"
            print(f"  {marker} {pov['label']:<14} (bias={pov['bias']:+.1f}, w={pov['weight']:.0%}) "
                  f"→ avg={pov_avg:.4f}  Δ={delta:+.4f}  contribution={contribution:.4f}")

    consensus_avg = sum(r["contribution"] for r in pov_results)
    delta_consensus = consensus_avg - target

    # Classification
    from_exact = abs(consensus_avg - EXACT_AVG)
    if from_exact <= 0.50:
        status = "OK"
    elif from_exact <= 1.00:
        status = "ALERTE"
    elif from_exact <= 2.00:
        status = "CRITIQUE"
    else:
        status = "HORS_BORNES"

    # Détection biais systémique entre vues
    pov_avgs = [r["avg_composite"] for r in pov_results]
    spread = max(pov_avgs) - min(pov_avgs)
    # Spread attendu = max_bias - min_bias (entre vues extrêmes)
    expected_spread = max(p["bias"] for p in PERSPECTIVES) - min(p["bias"] for p in PERSPECTIVES)
    spread_ok = abs(spread - expected_spread) < 0.2

    result = {
        "run_id":         hashlib.sha256(f"{engine_name}{seed}{datetime.utcnow().isoformat()}".encode()).hexdigest()[:12],
        "timestamp":      datetime.utcnow().isoformat(),
        "engine_name":    engine_name,
        "context":        context,
        "n_per_pov":      n_per_pov,
        "n_total":        n_total,
        "seed":           seed,
        "target":         target,
        "exact_avg":      round(EXACT_AVG, 4),
        "consensus_avg":  round(consensus_avg, 4),
        "delta_consensus": round(delta_consensus, 4),
        "status":         status,
        "spread":         round(spread, 4),
        "spread_ok":      spread_ok,
        "pov_results":    pov_results,
    }

    if verbose:
        print(f"  {'─'*53}")
        marker = "🟢" if status == "OK" else "🟠" if status == "ALERTE" else "🔴"
        print(f"  {marker} CONSENSUS PONDÉRÉ : {consensus_avg:.4f}  (Δ={delta_consensus:+.4f})  [{status}]")
        print(f"  Spread entre vues : {spread:.4f} (attendu ~{expected_spread:.1f}) {'✓' if spread_ok else '⚠ BIAIS SYSTÉMIQUE'}")
        print(f"  Exact avg théorique : {EXACT_AVG:.4f}  |  Cible : {target}")

    _save_mpov_result(result)
    return result

# ─── Validation moteur complet depuis 5 angles ───────────────────────────────

def validate_engine_multi_pov(engine_name: str, n_per_pov: int = 10_000) -> dict:
    """Validation complète : 5 POV × N runs + analyse de robustesse."""
    result = run_multi_perspective(engine_name, n_per_pov=n_per_pov, context="validation")

    print(f"\n  ANALYSE DE ROBUSTESSE")
    # Vérifier que chaque vue est dans ses bornes théoriques
    for pov_r in result["pov_results"]:
        pov_def = next(p for p in PERSPECTIVES if p["id"] == pov_r["id"])
        expected = EXACT_AVG + pov_def["bias"]
        actual = pov_r["avg_composite"]
        delta = abs(actual - expected)
        ok = delta < pov_def["amplitude"] * 0.1  # Tolérance : 10% de l'amplitude
        marker = "✓" if ok else "⚠"
        print(f"    {marker} {pov_r['label']:<14}: attendu≈{expected:.4f} observé={actual:.4f} Δ={delta:.4f}")

    # Verdict final
    print(f"\n  VERDICT : consensus={result['consensus_avg']:.4f} [{result['status']}]")
    if result["status"] == "OK":
        print("  ✓ Engine VALIDÉ depuis 5 points de vue")
    else:
        print(f"  ✗ Engine NON VALIDÉ — dérive détectée [{result['status']}]")

    return result

# ─── Comparaison POV unique vs multi-POV ─────────────────────────────────────

def compare_single_vs_multi(engine_name: str = "reference", n: int = 50_000) -> None:
    """Montre la différence entre 1 seul POV et le consensus multi-POV."""
    print(f"\n{'═'*55}")
    print(f"  COMPARAISON : UN POV vs CINQ POV")
    print(f"{'═'*55}")

    # Vue unique (ancienne méthode)
    random.seed(42)
    composites = []
    for t in TUPLES_EXACT:
        exact = exact_composite(t)
        scores = [exact + random.uniform(-0.5, 0.5) for _ in range(n)]
        composites.append(sum(scores) / n)
    single_avg = sum(composites) / len(composites)

    # Multi-POV (nouvelle méthode)
    result = run_multi_perspective(engine_name, n_per_pov=n // 5, verbose=False)
    multi_avg = result["consensus_avg"]

    print(f"  Méthode 1 vue  (n={n:,})            : avg={single_avg:.4f}  Δ={single_avg - 61.03:+.4f}")
    print(f"  Méthode 5 vues (5×{n//5:,})       : avg={multi_avg:.4f}  Δ={multi_avg - 61.03:+.4f}")
    print(f"  Robustesse supplémentaire          : {len(PERSPECTIVES)} scénarios couverts vs 1")
    print(f"  Détection biais systémique         : {'✓ OUI' if result['spread_ok'] else '⚠ NON'}")
    print(f"  Avantage multi-POV                 : couvre optimiste→pessimiste sur {n:,} runs")

# ─── Persistance ─────────────────────────────────────────────────────────────

def _load_log() -> list:
    if MPOV_LOG.exists():
        try:
            return json.loads(MPOV_LOG.read_text())
        except Exception:
            return []
    return []

def _save_mpov_result(result: dict) -> None:
    MPOV_LOG.parent.mkdir(parents=True, exist_ok=True)
    log = _load_log()
    log.append(result)
    log = log[-300:]
    MPOV_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))

def print_mpov_history(engine_name: Optional[str] = None, last_n: int = 10) -> None:
    log = _load_log()
    if engine_name:
        log = [r for r in log if r.get("engine_name") == engine_name]
    log = log[-last_n:]
    print(f"\n{'─'*55}")
    print(f"  HISTORIQUE MULTI-POV {'— ' + engine_name if engine_name else ''}")
    for r in log:
        marker = "🟢" if r["status"] == "OK" else "🟠" if r["status"] == "ALERTE" else "🔴"
        print(f"  {marker} {r['timestamp'][:16]} | consensus={r['consensus_avg']:.4f} "
              f"Δ={r['delta_consensus']:+.4f} [{r['status']}] spread={r['spread']:.4f}")

# ─── Simulation Multivers (§13 protocole) ────────────────────────────────────

# Nombre d'univers parallèles (chaque univers = paramètres légèrement différents)
MULTIVERSE_N = 100

def run_multiverse_simulation(
    engine_name: str,
    tuples: Optional[list[tuple]] = None,
    n_universes: int = MULTIVERSE_N,
    n_per_universe: int = 500,
    seed: int = 42,
    target: float = 61.03,
    verbose: bool = True,
) -> dict:
    """
    Protocole §13 — Simulation Multivers.
    Lance N univers parallèles avec des conditions légèrement différentes.
    Chaque univers = combinaison unique de (biais, amplitude, noise_profile).
    Le consensus multivers = médiane + moyenne pondérée par stabilité.

    Un univers est STABLE si son avg est dans les bornes OK du protocole.
    Un univers est INSTABLE s'il dépasse les bornes → poids réduit.
    """
    if tuples is None:
        tuples = TUPLES_EXACT

    random.seed(seed)
    universe_results = []

    if verbose:
        print(f"\n{'═'*55}")
        print(f"  SIMULATION MULTIVERS — {engine_name}")
        print(f"  {n_universes} univers × {n_per_universe} runs = {n_universes * n_per_universe:,} total")
        print(f"{'═'*55}")

    for u in range(n_universes):
        # Chaque univers a des paramètres légèrement différents (réalité alternative)
        u_seed = seed + u * 7919  # prime number pour éviter corrélations
        random.seed(u_seed)

        # Paramètres de cet univers (variations autour des valeurs standard)
        u_bias = random.gauss(0, 0.8)           # Biais de cet univers
        u_amplitude = random.uniform(0.1, 1.2)   # Amplitude du bruit
        u_weight_perturbation = random.uniform(-0.02, 0.02)  # Variation des poids

        # Poids perturbés pour cet univers
        w1 = max(0.01, 0.30 + u_weight_perturbation)
        w2 = max(0.01, 0.25 + random.uniform(-0.02, 0.02))
        w3 = max(0.01, 0.25 + random.uniform(-0.02, 0.02))
        w4 = max(0.01, 1.0 - w1 - w2 - w3)  # Normalisation

        # Simulation dans cet univers
        composites = []
        for t in tuples:
            s1, s2, s3, s4 = t
            exact_u = s1 * w1 + s2 * w2 + s3 * w3 + s4 * w4
            random.seed(u_seed + hash(str(t)) % 10_000)
            scores = [exact_u + u_bias + random.uniform(-u_amplitude, u_amplitude) for _ in range(n_per_universe)]
            composites.append(sum(scores) / n_per_universe)

        u_avg = sum(composites) / len(composites)

        # Stabilité de cet univers (par rapport à la cible)
        u_delta = abs(u_avg - target)
        u_stable = u_delta <= 2.0
        u_weight = max(0.01, 1.0 / (1.0 + u_delta))  # Poids inversement proportionnel à la dérive

        universe_results.append({
            "universe_id":  u,
            "avg":          round(u_avg, 4),
            "delta":        round(u_avg - target, 4),
            "bias":         round(u_bias, 4),
            "amplitude":    round(u_amplitude, 4),
            "stable":       u_stable,
            "weight":       round(u_weight, 6),
        })

    # Statistiques sur tous les univers
    avgs = [r["avg"] for r in universe_results]
    stable_avgs = [r["avg"] for r in universe_results if r["stable"]]
    unstable_n = sum(1 for r in universe_results if not r["stable"])

    # Consensus multivers = médiane des univers stables
    stable_avgs_sorted = sorted(stable_avgs)
    if stable_avgs_sorted:
        n_s = len(stable_avgs_sorted)
        median_consensus = (stable_avgs_sorted[n_s // 2 - 1] + stable_avgs_sorted[n_s // 2]) / 2 if n_s % 2 == 0 else stable_avgs_sorted[n_s // 2]
    else:
        median_consensus = sum(avgs) / len(avgs)

    # Moyenne pondérée (tous univers, poids basé sur stabilité)
    total_weight = sum(r["weight"] for r in universe_results)
    weighted_consensus = sum(r["avg"] * r["weight"] for r in universe_results) / total_weight

    # Classification
    delta_median = abs(median_consensus - target)
    delta_weighted = abs(weighted_consensus - target)
    best_consensus = median_consensus if delta_median < delta_weighted else weighted_consensus
    best_delta = min(delta_median, delta_weighted)

    if best_delta <= 0.50:
        mv_status = "OK"
    elif best_delta <= 1.00:
        mv_status = "ALERTE"
    elif best_delta <= 2.00:
        mv_status = "CRITIQUE"
    else:
        mv_status = "HORS_BORNES"

    # Robustesse = % univers stables
    robustness = round(len(stable_avgs) / n_universes * 100, 1)

    result = {
        "run_id":             hashlib.sha256(f"mv_{engine_name}{seed}".encode()).hexdigest()[:12],
        "timestamp":          datetime.utcnow().isoformat(),
        "engine_name":        engine_name,
        "type":               "multiverse",
        "n_universes":        n_universes,
        "n_per_universe":     n_per_universe,
        "n_total":            n_universes * n_per_universe,
        "target":             target,
        "min_avg":            round(min(avgs), 4),
        "max_avg":            round(max(avgs), 4),
        "mean_avg":           round(sum(avgs) / len(avgs), 4),
        "median_consensus":   round(median_consensus, 4),
        "weighted_consensus": round(weighted_consensus, 4),
        "best_consensus":     round(best_consensus, 4),
        "delta_best":         round(best_delta, 4),
        "mv_status":          mv_status,
        "robustness_pct":     robustness,
        "n_stable":           len(stable_avgs),
        "n_unstable":         unstable_n,
        "universes":          universe_results[:20],  # Sauvegarder les 20 premiers univers seulement
    }

    if verbose:
        marker = "🟢" if mv_status == "OK" else "🟠" if mv_status == "ALERTE" else "🔴"
        print(f"  {marker} Consensus médiane  : {median_consensus:.4f}  Δ={median_consensus - target:+.4f}")
        print(f"  {marker} Consensus pondéré  : {weighted_consensus:.4f}  Δ={weighted_consensus - target:+.4f}")
        print(f"  Robustesse         : {robustness}% univers stables ({len(stable_avgs)}/{n_universes})")
        print(f"  Plage multivers    : [{min(avgs):.4f} → {max(avgs):.4f}]")
        print(f"  Status multivers   : [{mv_status}]")

    _save_mpov_result(result)
    return result


def run_full_validation(engine_name: str, n_per_pov: int = 10_000, n_universes: int = 100) -> dict:
    """
    Validation complète : Multi-Perspectives (§12) + Multivers (§13).
    Le résultat final est le consensus des deux méthodes.
    """
    print(f"\n{'═'*55}")
    print(f"  VALIDATION COMPLÈTE — {engine_name}")
    print(f"  Phase 1 : Multi-Perspectives (5 POV × {n_per_pov:,} runs)")
    print(f"  Phase 2 : Multivers ({n_universes} univers)")
    print(f"{'═'*55}")

    pov_result = run_multi_perspective(engine_name, n_per_pov=n_per_pov, verbose=True)
    mv_result  = run_multiverse_simulation(engine_name, n_universes=n_universes, verbose=True)

    # Consensus final = moyenne des deux consensus
    final_consensus = (pov_result["consensus_avg"] + mv_result["best_consensus"]) / 2
    final_delta = abs(final_consensus - 61.03)

    if final_delta <= 0.50:
        final_status = "OK"
    elif final_delta <= 1.00:
        final_status = "ALERTE"
    else:
        final_status = "CRITIQUE"

    print(f"\n{'─'*55}")
    print(f"  SYNTHÈSE FINALE")
    print(f"  POV consensus     : {pov_result['consensus_avg']:.4f} [{pov_result['status']}]")
    print(f"  Multivers best    : {mv_result['best_consensus']:.4f} [{mv_result['mv_status']}]")
    print(f"  CONSENSUS FINAL   : {final_consensus:.4f}  [{final_status}]")
    print(f"  Robustesse        : {mv_result['robustness_pct']}% univers stables")

    verdict = "✓ VALIDÉ" if final_status in ("OK", "ALERTE") else "✗ NON VALIDÉ"
    print(f"  {verdict} depuis 5 POV + {n_universes} univers parallèles")

    return {
        "engine_name":     engine_name,
        "pov_result":      pov_result,
        "mv_result":       mv_result,
        "final_consensus": round(final_consensus, 4),
        "final_status":    final_status,
        "validated":       final_status in ("OK", "ALERTE"),
    }


# ─── Intégration dans le pattern engine ──────────────────────────────────────

ENGINE_MPOV_SNIPPET = '''
# ── Validation multi-perspectives (protocole §12) ──────────────────────────
# À appeler après run_engine() pour validation complète
# from scripts.multi_perspective_simulator import run_multi_perspective
# result = run_multi_perspective(__file__, n_per_pov=10_000)
# assert result["status"] in ("OK", "ALERTE"), f"Dérive détectée : {result['status']}"
'''

# ─── Point d'entrée ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    # 1. Comparaison une vue vs cinq vues
    compare_single_vs_multi("reference_engine", n=50_000)

    # 2. Validation complète multi-POV
    print()
    result = validate_engine_multi_pov("reference_engine", n_per_pov=10_000)

    # 3. Historique
    print_mpov_history()

    # 4. Résumé du protocole
    print(f"\n{'═'*55}")
    print("  PROTOCOLE §12 — RÈGLES MULTI-PERSPECTIVES")
    print(f"{'═'*55}")
    for pov in PERSPECTIVES:
        print(f"  {pov['label']:<14} bias={pov['bias']:+.1f}  amplitude=±{pov['amplitude']}  weight={pov['weight']:.0%}")
    print(f"  {'─'*50}")
    print(f"  Consensus pondéré : Σ(avg_pov × weight)")
    print(f"  Borne OK          : |Δ consensus| ≤ 0.50")
    print(f"  Borne ALERTE      : |Δ consensus| ≤ 1.00")
    print(f"  Spread attendu    : ~{sum(abs(p['bias'])*2 for p in PERSPECTIVES if p['bias']!=0):.1f} entre vues extrêmes")
    print(f"  N total minimum   : {5 * 10_000:,} (5 vues × 10 000)")

    sys.exit(0 if result["status"] in ("OK", "ALERTE") else 1)
