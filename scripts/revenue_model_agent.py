"""
revenue_model_agent.py — CaelumSwarm™ Revenue Model Agent
3 scenarios: A (Bootstrap/Freemium), B (SaaS B2B), C (IP Licensing)
Monte Carlo 100K simulations per scenario
"""
import json
import random
import os

RANDOM_SEED = 2024
N_SIMULATIONS = 100_000


def build_scenario_a():
    """Scenario A — Bootstrap / Freemium: 0 → 100K€ year 1."""
    return {
        "id": "A",
        "name": "Bootstrap / Freemium",
        "description": (
            "Self-funded growth via freemium SaaS tier. Acquire SME users via LinkedIn "
            "and GitHub, convert to paid at 8%. Target: 100K€ ARR end of year 1."
        ),
        "target_revenue_eur_yr1": 100_000,
        "milestones": [
            {"month": 1,  "action": "MVP launch, 50 free users",                         "revenue_eur": 0},
            {"month": 2,  "action": "ProductHunt launch, 200 free users",                 "revenue_eur": 0},
            {"month": 3,  "action": "First 5 paid conversions @ 99€/mo",                  "revenue_eur": 495},
            {"month": 4,  "action": "10 paid users, content machine active",              "revenue_eur": 990},
            {"month": 5,  "action": "20 paid users, first case study published",          "revenue_eur": 1_980},
            {"month": 6,  "action": "35 paid users, referral loop initiated",             "revenue_eur": 3_465},
            {"month": 7,  "action": "55 paid users, enterprise trial started",            "revenue_eur": 5_445},
            {"month": 8,  "action": "75 paid users + 1 enterprise pilot @ 2K€/mo",       "revenue_eur": 9_425},
            {"month": 9,  "action": "100 paid users + 2 enterprise pilots",               "revenue_eur": 13_900},
            {"month": 10, "action": "130 paid users + 3 enterprise clients",              "revenue_eur": 18_870},
            {"month": 11, "action": "160 paid users + 4 enterprise clients",              "revenue_eur": 23_840},
            {"month": 12, "action": "200 paid users + 5 enterprise clients — 100K€ ARR", "revenue_eur": 100_000},
        ],
        "risks": [
            "Slow freemium-to-paid conversion (<5%)",
            "Enterprise sales cycle > 3 months",
            "CSDDD awareness low in SME segment",
            "Solo founder bandwidth constraints",
        ],
        "base_success_prob": 0.58,
        "revenue_variance": 0.35,
    }


def build_scenario_b():
    """Scenario B — SaaS B2B: 0 → 500K€ year 1, 10 enterprise clients."""
    return {
        "id": "B",
        "name": "SaaS B2B Enterprise",
        "description": (
            "Direct outbound to Fortune 500 compliance & legal teams. "
            "Land 10 enterprise clients at avg 50K€/yr. CSDDD deadline urgency driver."
        ),
        "target_revenue_eur_yr1": 500_000,
        "target_clients": 10,
        "avg_contract_eur": 50_000,
        "milestones": [
            {"month": 1,  "action": "ICP definition, 200-account target list built",       "revenue_eur": 0},
            {"month": 2,  "action": "Outbound sequence launched, 50 demos booked",         "revenue_eur": 0},
            {"month": 3,  "action": "Client 1 signed — 50K€ ACV",                         "revenue_eur": 50_000},
            {"month": 4,  "action": "Clients 2-3 signed — cumulative 150K€",              "revenue_eur": 150_000},
            {"month": 5,  "action": "Clients 4-5 signed — 250K€ cumulative",              "revenue_eur": 250_000},
            {"month": 6,  "action": "Clients 6-7 signed — 350K€ cumulative",              "revenue_eur": 350_000},
            {"month": 7,  "action": "Partnerships (Big4) initiated",                       "revenue_eur": 350_000},
            {"month": 8,  "action": "Client 8 signed + upsell client 1 — 430K€",          "revenue_eur": 430_000},
            {"month": 9,  "action": "Client 9 signed — 480K€ cumulative",                 "revenue_eur": 480_000},
            {"month": 10, "action": "Client 10 signed — 500K€ target hit",                "revenue_eur": 500_000},
            {"month": 11, "action": "Pipeline for Year 2: 5 new prospects advanced",      "revenue_eur": 500_000},
            {"month": 12, "action": "Year 1 closed: 10 clients, 500K€ ARR",               "revenue_eur": 500_000},
        ],
        "risks": [
            "Enterprise sales cycles 6-9 months",
            "Legal/procurement delays",
            "Competition from Big4 advisory arms",
            "CSDDD postponement by EU legislators",
            "Pricing pressure on first 3 logos",
        ],
        "base_success_prob": 0.42,
        "revenue_variance": 0.45,
    }


def build_scenario_c():
    """Scenario C — IP Licensing: 0 → 1M€ via patents + US royalties."""
    return {
        "id": "C",
        "name": "IP Licensing + US Royalties",
        "description": (
            "License patent portfolio to US/EU compliance data vendors and Big4 firms. "
            "5 axes filed, royalty rate 3-7% of licensee revenue. Target 1M€ Y1."
        ),
        "target_revenue_eur_yr1": 1_000_000,
        "milestones": [
            {"month": 1,  "action": "Patent applications filed (all 5 axes)",              "revenue_eur": 0},
            {"month": 2,  "action": "IP valuation report commissioned",                    "revenue_eur": 0},
            {"month": 3,  "action": "Licensing deck prepared, 10 targets identified",      "revenue_eur": 0},
            {"month": 4,  "action": "NDA + term sheet with Licensee A (US data vendor)",   "revenue_eur": 0},
            {"month": 5,  "action": "License A signed — 200K€ upfront + royalties",        "revenue_eur": 200_000},
            {"month": 6,  "action": "License B signed — 150K€ upfront (EU ESG vendor)",   "revenue_eur": 350_000},
            {"month": 7,  "action": "License C signed — 200K€ (Big4 advisory arm)",        "revenue_eur": 550_000},
            {"month": 8,  "action": "US royalty Q1 payments received — 80K€",              "revenue_eur": 630_000},
            {"month": 9,  "action": "License D signed — 150K€ (financial data platform)", "revenue_eur": 780_000},
            {"month": 10, "action": "US royalty Q2 + sublicense fees — 120K€",             "revenue_eur": 900_000},
            {"month": 11, "action": "License E signed — 75K€ (RegTech startup)",           "revenue_eur": 975_000},
            {"month": 12, "action": "Year-end royalty true-up — 1M€ target achieved",     "revenue_eur": 1_000_000},
        ],
        "risks": [
            "USPTO grant delays (avg 2-3 years)",
            "Prior art challenges during prosecution",
            "Licensee revenue lower than projected",
            "EU patent vs US patent strategy divergence",
            "Litigation risk from large IP holders",
        ],
        "base_success_prob": 0.31,
        "revenue_variance": 0.60,
    }


def run_monte_carlo(scenario: dict, n: int = N_SIMULATIONS) -> dict:
    """Monte Carlo simulation for year-1 revenue achievement."""
    random.seed(RANDOM_SEED + ord(scenario["id"]))

    target = scenario["target_revenue_eur_yr1"]
    base_p = scenario["base_success_prob"]
    variance = scenario["revenue_variance"]

    successes = 0
    simulated_revenues = []

    for _ in range(n):
        # Success gate: stochastic success probability
        noise = random.gauss(0, 0.10)
        adjusted_p = max(0.0, min(1.0, base_p + noise))
        success = random.random() < adjusted_p

        if success:
            # Revenue realization: lognormal around target
            mu = target * random.uniform(0.85, 1.20)
            sigma = mu * variance
            realized = random.gauss(mu, sigma)
            realized = max(0.0, realized)
        else:
            realized = target * random.uniform(0.0, 0.45)

        simulated_revenues.append(realized)
        if realized >= target * 0.90:  # within 10% of target = success
            successes += 1

    success_rate = successes / n
    avg_revenue = sum(simulated_revenues) / n
    sorted_rev = sorted(simulated_revenues)
    p10 = sorted_rev[int(0.10 * n)]
    p25 = sorted_rev[int(0.25 * n)]
    p50 = sorted_rev[int(0.50 * n)]
    p75 = sorted_rev[int(0.75 * n)]
    p90 = sorted_rev[int(0.90 * n)]

    return {
        "success_rate": round(success_rate, 4),
        "avg_simulated_revenue_eur": round(avg_revenue, 2),
        "p10_eur": round(p10, 2),
        "p25_eur": round(p25, 2),
        "p50_eur": round(p50, 2),
        "p75_eur": round(p75, 2),
        "p90_eur": round(p90, 2),
        "n_simulations": n,
    }


def main():
    print("=" * 65)
    print("  CaelumSwarm™ — Revenue Model Agent")
    print(f"  Monte Carlo {N_SIMULATIONS:,} simulations per scenario")
    print("=" * 65)

    scenarios = [build_scenario_a(), build_scenario_b(), build_scenario_c()]
    results = []

    for sc in scenarios:
        mc = run_monte_carlo(sc)
        sc_result = {**sc, "monte_carlo": mc}
        results.append(sc_result)

        print(f"\n{'='*65}")
        print(f"  Scenario {sc['id']} — {sc['name']}")
        print(f"  Target Y1  : {sc['target_revenue_eur_yr1']:,}€")
        print(f"  {sc['description']}")
        print(f"\n  Monte Carlo ({N_SIMULATIONS:,} sims):")
        print(f"    Success rate     : {mc['success_rate']*100:.1f}%")
        print(f"    Avg revenue      : {mc['avg_simulated_revenue_eur']:,.0f}€")
        print(f"    P10 / P50 / P90  : {mc['p10_eur']:,.0f}€ / {mc['p50_eur']:,.0f}€ / {mc['p90_eur']:,.0f}€")
        print(f"\n  Monthly milestones (Y1):")
        for m in sc["milestones"]:
            rev_str = f"{m['revenue_eur']:>10,}€" if m["revenue_eur"] > 0 else "           —"
            print(f"    M{m['month']:02d}: {rev_str}  {m['action']}")
        print(f"\n  Risks:")
        for r in sc["risks"]:
            print(f"    • {r}")

    output = {
        "agent": "revenue_model_agent",
        "version": "1.0.0",
        "n_scenarios": len(scenarios),
        "n_simulations_per_scenario": N_SIMULATIONS,
        "scenarios": results,
    }

    out_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "revenue_model.json"
    )
    out_path = os.path.normpath(out_path)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 65)
    print(f"  Output saved to: {out_path}")
    print("=" * 65)

    return output


if __name__ == "__main__":
    main()
