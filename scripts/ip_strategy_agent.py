"""
ip_strategy_agent.py — CaelumSwarm™ IP Strategy Agent
Monte Carlo 50K simulation per patent axis
"""
import json
import random
import math
import os

AXES = [
    {
        "id": 1,
        "title": "Multi-Agent Human Rights Analysis Method",
        "technical_description": (
            "Distributed multi-agent architecture for real-time human rights risk "
            "assessment using composite scoring across supply chain nodes, leveraging "
            "LLM ensembles with cross-validation and uncertainty quantification."
        ),
        "us_target_market": "ESG data providers, Fortune 500 Legal & Compliance teams",
        "estimated_value_usd": 4_500_000,
        "base_success_prob": 0.72,
        "novelty_score": 0.85,
        "prior_art_risk": 0.15,
    },
    {
        "id": 2,
        "title": "Composite ESG/CSDDD Scoring Algorithm",
        "technical_description": (
            "Proprietary weighted composite index for ESG and EU CSDDD compliance "
            "scoring: sub-indicator aggregation with adaptive thresholds, dynamic "
            "reweighting per regulatory update cycles, and explainable audit trail."
        ),
        "us_target_market": "Financial institutions, asset managers, ESG rating agencies",
        "estimated_value_usd": 6_200_000,
        "base_success_prob": 0.68,
        "novelty_score": 0.78,
        "prior_art_risk": 0.22,
    },
    {
        "id": 3,
        "title": "Dynamic Compliance Interface",
        "technical_description": (
            "Adaptive UI/UX system that dynamically reconfigures compliance dashboards "
            "based on jurisdiction, user role, and real-time regulatory change signals. "
            "Patent covers the rule-engine binding layer and live re-render protocol."
        ),
        "us_target_market": "LegalTech SaaS platforms, RegTech vendors, enterprise GRC tools",
        "estimated_value_usd": 3_100_000,
        "base_success_prob": 0.61,
        "novelty_score": 0.70,
        "prior_art_risk": 0.30,
    },
    {
        "id": 4,
        "title": "Quantum Simulation Engine for Compliance",
        "technical_description": (
            "Quantum-inspired Monte Carlo simulation engine for modeling cascading "
            "compliance risk scenarios across multi-tier supply chains. Uses variational "
            "quantum eigensolver analogs on classical hardware for exponential speedup."
        ),
        "us_target_market": "Defense contractors, pharma supply chains, semiconductor fabs",
        "estimated_value_usd": 8_900_000,
        "base_success_prob": 0.54,
        "novelty_score": 0.93,
        "prior_art_risk": 0.18,
    },
    {
        "id": 5,
        "title": "Automated Supply Chain Audit System",
        "technical_description": (
            "End-to-end automated audit pipeline combining OCR, NLP entity extraction, "
            "graph traversal across supplier tiers, and anomaly detection for CSDDD/CSRD "
            "due diligence. Patent covers the graph-audit binding method and alert schema."
        ),
        "us_target_market": "Retail, automotive, electronics — Tier-1 procurement teams",
        "estimated_value_usd": 5_300_000,
        "base_success_prob": 0.76,
        "novelty_score": 0.80,
        "prior_art_risk": 0.20,
    },
]

N_SIMULATIONS = 50_000
RANDOM_SEED = 42


def run_monte_carlo(axis: dict, n: int = N_SIMULATIONS) -> dict:
    """Monte Carlo simulation for patent grant & commercialisation success."""
    random.seed(RANDOM_SEED + axis["id"])
    successes = 0
    revenues = []

    base_p = axis["base_success_prob"]
    novelty = axis["novelty_score"]
    prior_art_risk = axis["prior_art_risk"]
    base_value = axis["estimated_value_usd"]

    for _ in range(n):
        # USPTO grant probability
        grant_noise = random.gauss(0, 0.08)
        grant_p = max(0.0, min(1.0, base_p + grant_noise - prior_art_risk * 0.3))
        granted = random.random() < grant_p

        if not granted:
            revenues.append(0.0)
            continue

        # Commercialisation multiplier
        market_factor = random.uniform(0.5, 1.8)
        novelty_bonus = novelty * random.uniform(0.8, 1.2)
        revenue = base_value * market_factor * novelty_bonus * random.gauss(1.0, 0.15)
        revenue = max(0.0, revenue)
        revenues.append(revenue)
        successes += 1

    success_prob = successes / n
    avg_revenue = sum(revenues) / n
    revenues_sorted = sorted(revenues)
    p10 = revenues_sorted[int(0.10 * n)]
    p50 = revenues_sorted[int(0.50 * n)]
    p90 = revenues_sorted[int(0.90 * n)]

    return {
        "success_probability": round(success_prob, 4),
        "avg_expected_revenue_usd": round(avg_revenue, 2),
        "p10_usd": round(p10, 2),
        "p50_usd": round(p50, 2),
        "p90_usd": round(p90, 2),
        "n_simulations": n,
    }


def main():
    print("=" * 65)
    print("  CaelumSwarm™ — IP Strategy Agent")
    print(f"  Monte Carlo {N_SIMULATIONS:,} simulations per axis")
    print("=" * 65)

    results = []
    total_base_value = 0

    for axis in AXES:
        mc = run_monte_carlo(axis)
        axis_result = {**axis, "monte_carlo": mc}
        results.append(axis_result)
        total_base_value += axis["estimated_value_usd"]

        print(f"\n[Axis {axis['id']}] {axis['title']}")
        print(f"  Market       : {axis['us_target_market']}")
        print(f"  Base value   : ${axis['estimated_value_usd']:,.0f}")
        print(f"  Grant prob   : {mc['success_probability']*100:.1f}%")
        print(f"  Avg revenue  : ${mc['avg_expected_revenue_usd']:,.0f}")
        print(f"  P10 / P50 / P90 : ${mc['p10_usd']:,.0f} / ${mc['p50_usd']:,.0f} / ${mc['p90_usd']:,.0f}")

    estimated_patent_portfolio_value = round(total_base_value / 1e6, 2)

    summary = {
        "agent": "ip_strategy_agent",
        "version": "1.0.0",
        "n_axes": len(AXES),
        "total_base_value_usd": total_base_value,
        "estimated_patent_portfolio_value_M_usd": estimated_patent_portfolio_value,
        "axes": results,
    }

    out_path = os.path.join(os.path.dirname(__file__), "..", "data", "ip_strategy.json")
    out_path = os.path.normpath(out_path)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 65)
    print(f"  TOTAL base portfolio value  : ${total_base_value:,.0f}")
    print(f"  estimated_patent_portfolio_value = {estimated_patent_portfolio_value} M$")
    print(f"  Output saved to: {out_path}")
    print("=" * 65)

    return summary


if __name__ == "__main__":
    main()
