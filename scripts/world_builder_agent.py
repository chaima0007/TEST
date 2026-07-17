"""
world_builder_agent.py — CaelumSwarm™ World Builder (Main Orchestrator)
Runs ip_strategy_agent, gomarket_zero_agent, revenue_model_agent
Synthesizes US market opportunity score + 12 ROI-ranked actions
Monte Carlo 100K protocol per decision
"""
import json
import random
import subprocess
import sys
import os

RANDOM_SEED = 9999
N_SIMULATIONS = 100_000

# 12 immediate actions ranked by ROI
ACTIONS = [
    {
        "rank": 1,
        "action": "File provisional patent on Multi-Agent Human Rights Analysis Method",
        "category": "IP",
        "roi_score": 95.0,
        "delay_days": 7,
        "cost_usd": 1_500,
        "expected_value_usd": 4_500_000,
        "base_success_prob": 0.72,
    },
    {
        "rank": 2,
        "action": "Launch LinkedIn CSDDD content series (3 posts/week)",
        "category": "GTM",
        "roi_score": 92.0,
        "delay_days": 1,
        "cost_usd": 0,
        "expected_value_usd": 200_000,
        "base_success_prob": 0.85,
    },
    {
        "rank": 3,
        "action": "Submit ProductHunt launch (CaelumSwarm™ CSDDD compliance agent)",
        "category": "GTM",
        "roi_score": 88.5,
        "delay_days": 14,
        "cost_usd": 0,
        "expected_value_usd": 150_000,
        "base_success_prob": 0.70,
    },
    {
        "rank": 4,
        "action": "File provisional patent on Composite ESG/CSDDD Scoring Algorithm",
        "category": "IP",
        "roi_score": 87.0,
        "delay_days": 14,
        "cost_usd": 1_500,
        "expected_value_usd": 6_200_000,
        "base_success_prob": 0.68,
    },
    {
        "rank": 5,
        "action": "Publish open-source CSDDD toolkit on GitHub with CaelumSwarm branding",
        "category": "GTM",
        "roi_score": 85.0,
        "delay_days": 7,
        "cost_usd": 0,
        "expected_value_usd": 300_000,
        "base_success_prob": 0.80,
    },
    {
        "rank": 6,
        "action": "Build ICP list: 200 US Fortune 500 compliance officers (LinkedIn Sales Nav)",
        "category": "Sales",
        "roi_score": 82.0,
        "delay_days": 3,
        "cost_usd": 0,
        "expected_value_usd": 500_000,
        "base_success_prob": 0.60,
    },
    {
        "rank": 7,
        "action": "Post 'Show HN' on Hacker News for CaelumSwarm™ technical architecture",
        "category": "GTM",
        "roi_score": 80.0,
        "delay_days": 2,
        "cost_usd": 0,
        "expected_value_usd": 120_000,
        "base_success_prob": 0.55,
    },
    {
        "rank": 8,
        "action": "Submit CFP to RSA Conference 2026 (AI for Supply Chain Compliance track)",
        "category": "GTM",
        "roi_score": 75.0,
        "delay_days": 30,
        "cost_usd": 0,
        "expected_value_usd": 400_000,
        "base_success_prob": 0.40,
    },
    {
        "rank": 9,
        "action": "Negotiate Scenario B pilot with 1 US enterprise (50K€ ACV)",
        "category": "Sales",
        "roi_score": 72.0,
        "delay_days": 21,
        "cost_usd": 0,
        "expected_value_usd": 500_000,
        "base_success_prob": 0.42,
    },
    {
        "rank": 10,
        "action": "Launch Substack 'Compliance Intelligence Brief' (weekly, bilingual)",
        "category": "GTM",
        "roi_score": 68.0,
        "delay_days": 5,
        "cost_usd": 0,
        "expected_value_usd": 80_000,
        "base_success_prob": 0.75,
    },
    {
        "rank": 11,
        "action": "File patents on Quantum Simulation Engine + Supply Chain Audit System",
        "category": "IP",
        "roi_score": 65.0,
        "delay_days": 30,
        "cost_usd": 3_000,
        "expected_value_usd": 14_200_000,
        "base_success_prob": 0.50,
    },
    {
        "rank": 12,
        "action": "Initiate IP licensing conversations with 3 US ESG data vendors",
        "category": "Licensing",
        "roi_score": 60.0,
        "delay_days": 45,
        "cost_usd": 0,
        "expected_value_usd": 1_000_000,
        "base_success_prob": 0.31,
    },
]


def run_monte_carlo_action(action: dict, n: int = N_SIMULATIONS) -> dict:
    random.seed(RANDOM_SEED + action["rank"])
    base_p = action["base_success_prob"]
    ev = action["expected_value_usd"]
    cost = action["cost_usd"]

    successes = 0
    net_values = []

    for _ in range(n):
        noise = random.gauss(0, 0.08)
        p = max(0.0, min(1.0, base_p + noise))
        if random.random() < p:
            revenue = ev * random.uniform(0.6, 1.5) * random.gauss(1.0, 0.20)
            revenue = max(0.0, revenue)
            net = revenue - cost
            successes += 1
        else:
            net = -cost
        net_values.append(net)

    success_rate = successes / n
    avg_net = sum(net_values) / n
    sorted_vals = sorted(net_values)
    p10 = sorted_vals[int(0.10 * n)]
    p50 = sorted_vals[int(0.50 * n)]
    p90 = sorted_vals[int(0.90 * n)]

    return {
        "success_rate": round(success_rate, 4),
        "avg_net_value_usd": round(avg_net, 2),
        "p10_usd": round(p10, 2),
        "p50_usd": round(p50, 2),
        "p90_usd": round(p90, 2),
        "n_simulations": n,
    }


def compute_market_opportunity_score(ip_data: dict, gtm_data: dict, rev_data: dict) -> float:
    """Synthesize global US market opportunity score (0-100)."""
    # IP portfolio factor (max 30 pts)
    portfolio_m = ip_data.get("estimated_patent_portfolio_value_M_usd", 0)
    ip_score = min(30.0, portfolio_m / 1.0)  # 1M$ = 1 pt, cap at 30

    # GTM reach factor (max 25 pts)
    avg_comp = gtm_data.get("avg_composite", 0)
    gtm_score = avg_comp * 25 / 100

    # Revenue scenario factor (max 45 pts)
    scenarios = rev_data.get("scenarios", [])
    if scenarios:
        success_rates = [sc["monte_carlo"]["success_rate"] for sc in scenarios]
        avg_sr = sum(success_rates) / len(success_rates)
        rev_score = avg_sr * 45
    else:
        rev_score = 0.0

    total = ip_score + gtm_score + rev_score
    return round(min(100.0, total), 2)


def run_sub_agents():
    """Run the 3 sub-agents as subprocesses and load their JSON outputs."""
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.normpath(os.path.join(scripts_dir, "..", "data"))

    sub_scripts = [
        ("ip_strategy_agent", os.path.join(scripts_dir, "ip_strategy_agent.py"),
         os.path.join(data_dir, "ip_strategy.json")),
        ("gomarket_zero_agent", os.path.join(scripts_dir, "gomarket_zero_agent.py"),
         os.path.join(data_dir, "gomarket_strategy.json")),
        ("revenue_model_agent", os.path.join(scripts_dir, "revenue_model_agent.py"),
         os.path.join(data_dir, "revenue_model.json")),
    ]

    results = {}
    for name, script_path, json_path in sub_scripts:
        print(f"\n  [orchestrator] Running {name}...")
        ret = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
        )
        if ret.returncode != 0:
            print(f"  ERROR running {name}:\n{ret.stderr}")
            sys.exit(1)
        print(f"  [orchestrator] {name} completed ✓")

        with open(json_path, "r", encoding="utf-8") as f:
            results[name] = json.load(f)

    return results


def main():
    print("=" * 70)
    print("  CaelumSwarm™ — World Builder Agent (Main Orchestrator)")
    print(f"  Monte Carlo {N_SIMULATIONS:,} sims per decision · 12 ROI-ranked actions")
    print("=" * 70)

    # Step 1: Run sub-agents
    print("\n[Phase 1] Running sub-agents...")
    sub_results = run_sub_agents()

    ip_data = sub_results["ip_strategy_agent"]
    gtm_data = sub_results["gomarket_zero_agent"]
    rev_data = sub_results["revenue_model_agent"]

    # Step 2: Compute market opportunity score
    market_score = compute_market_opportunity_score(ip_data, gtm_data, rev_data)

    print(f"\n[Phase 2] US Market Opportunity Score: {market_score}/100")
    print(f"          IP portfolio  : {ip_data['estimated_patent_portfolio_value_M_usd']}M$")
    print(f"          GTM avg score : {gtm_data['avg_composite']}")
    rev_scenarios = rev_data.get("scenarios", [])
    for sc in rev_scenarios:
        print(f"          Scenario {sc['id']} success: {sc['monte_carlo']['success_rate']*100:.1f}%")

    # Step 3: Monte Carlo for each of the 12 actions
    print("\n[Phase 3] Monte Carlo simulations for 12 actions...")
    action_results = []
    for action in ACTIONS:
        mc = run_monte_carlo_action(action)
        action_result = {**action, "monte_carlo": mc}
        action_results.append(action_result)

    # Step 4: Print dashboard
    print("\n" + "=" * 70)
    print("  WORLD BUILDER DASHBOARD — 12 Actions Ranked by ROI")
    print("=" * 70)
    print(f"\n  Global US Market Opportunity Score : {market_score} / 100")
    print(f"  Estimated IP Portfolio Value       : {ip_data['estimated_patent_portfolio_value_M_usd']}M$")
    print(f"  GTM avg_composite                  : {gtm_data['avg_composite']}")
    print(f"  GTM total reach                    : {gtm_data['total_reach_people']:,} people")
    print()
    print(f"  {'#':<4} {'Action':<55} {'ROI':>5} {'Days':>5} {'P(ok)':>6} {'E[Net$]':>12}")
    print("  " + "-" * 90)
    for ar in action_results:
        mc = ar["monte_carlo"]
        print(
            f"  {ar['rank']:<4} {ar['action'][:54]:<55} "
            f"{ar['roi_score']:>5.1f} {ar['delay_days']:>5} "
            f"{mc['success_rate']*100:>5.1f}% {mc['avg_net_value_usd']:>12,.0f}$"
        )

    # Step 5: Save report
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.normpath(os.path.join(scripts_dir, "..", "data", "world_builder_report.json"))

    report = {
        "agent": "world_builder_agent",
        "version": "1.0.0",
        "us_market_opportunity_score": market_score,
        "sub_agent_summaries": {
            "ip_strategy": {
                "n_axes": ip_data["n_axes"],
                "portfolio_value_M_usd": ip_data["estimated_patent_portfolio_value_M_usd"],
            },
            "gomarket": {
                "avg_composite": gtm_data["avg_composite"],
                "n_channels": len(gtm_data["channels"]),
                "total_reach": gtm_data["total_reach_people"],
                "distribution": gtm_data["distribution"],
            },
            "revenue": {
                "n_scenarios": rev_data["n_scenarios"],
                "scenario_success_rates": {
                    sc["id"]: sc["monte_carlo"]["success_rate"]
                    for sc in rev_data["scenarios"]
                },
            },
        },
        "actions_ranked_by_roi": action_results,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print(f"  World Builder report saved to: {out_path}")
    print("=" * 70)

    return report


if __name__ == "__main__":
    main()
