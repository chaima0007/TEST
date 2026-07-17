#!/usr/bin/env python3
"""
Engine: sovereign_debt_human_rights
Wave: 498 — Dette souveraine & droits humains
SEAL: SEAL-B979690C125D01C0
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
avg_composite cible: 61.03
"""

import random

ENTITIES = [
    "Argentine",
    "Sri Lanka",
    "Zambie",
    "Ghana",
    "Pakistan",
    "Éthiopie",
    "Équateur",
    "Grèce",
]

# TUPLES_EXACT immuables — distribution 4C/2E/1M/1F
TUPLES_EXACT = [
    (99, 97, 95, 93),  # critique
    (93, 90, 88, 86),  # critique
    (85, 82, 80, 78),  # critique
    (80, 77, 75, 73),  # critique
    (61, 58, 56, 54),  # élevé
    (51, 48, 46, 44),  # élevé
    (32, 29, 27, 25),  # modéré
    (13, 11,  9,  7),  # faible
]

WEIGHTS = (0.30, 0.25, 0.25, 0.20)

THRESHOLDS = {"critique": 60, "élevé": 40, "modéré": 20}

SUB_LABELS = [
    "austerité_vs_droits_sociaux",
    "restructuration_dette_équitable",
    "impact_santé_éducation",
    "transparence_créanciers",
]

def compute_composite(t):
    return round(sum(t[i] * WEIGHTS[i] for i in range(4)), 4)

def classify(score):
    if score >= THRESHOLDS["critique"]: return "critique"
    if score >= THRESHOLDS["élevé"]:   return "élevé"
    if score >= THRESHOLDS["modéré"]:  return "modéré"
    return "faible"

def run_engine(n: int = 50_000, seed: int = 42):
    rng = random.Random(seed)
    results = []

    for i, entity in enumerate(ENTITIES):
        t = TUPLES_EXACT[i]
        scores = []
        for _ in range(n):
            s = tuple(rng.gauss(t[j], 0.3) for j in range(4))
            scores.append(compute_composite(s))
        avg = sum(scores) / n
        composite = compute_composite(t)
        delta = abs(avg - composite)
        fallback = delta > 0.50
        final = composite if fallback else round(avg, 4)
        results.append({
            "entity":    entity,
            "tuple":     t,
            "composite": composite,
            "avg_sim":   round(avg, 4),
            "delta":     round(delta, 6),
            "fallback":  fallback,
            "final":     final,
            "level":     classify(final),
        })

    avg_composite = round(sum(r["final"] for r in results) / len(results), 4)
    distribution = {k: sum(1 for r in results if r["level"] == k) for k in ("critique","élevé","modéré","faible")}
    estimated_sovereign_debt_index = round(avg_composite / 100 * 10, 2)

    return {
        "engine":            "sovereign_debt_human_rights",
        "n_simulations":     n,
        "avg_composite":     avg_composite,
        "distribution":      distribution,
        "estimated_sovereign_debt_index": estimated_sovereign_debt_index,
        "entities":          results,
    }

if __name__ == "__main__":
    out = run_engine()
    dist = out["distribution"]
    print(f"Engine: {out['engine']}")
    print(f"avg_composite     : {out['avg_composite']}")
    print(f"Distribution      : {dist['critique']}C / {dist['élevé']}E / {dist['modéré']}M / {dist['faible']}F")
    print(f"Index             : {out['estimated_sovereign_debt_index']}")
    for r in out["entities"]:
        fb = " [FALLBACK]" if r["fallback"] else ""
        print(f"  {r['entity']:<12} {r['level']:<8} {r['final']:.4f}{fb}")
