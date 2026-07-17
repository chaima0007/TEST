#!/usr/bin/env python3
"""CaelumSwarm™ — Algorithmic Wage Theft & Gig Economy Engine (Wave-493)"""
import random
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent

ENTITIES = [
    {
        "id": "AWGE-001",
        "name": "Uber/Lyft USA — Algorithmes Tarification Dynamique, Désactivation Arbitraire & Vol Salaire Documenté 1.4 Mrd$",
        "region": "Amérique du Nord",
        "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93,
        "weight": 0.20,
        "risk_level": "critique",
        "primary_pattern": "algorithmic_deactivation_wage_theft",
    },
    {
        "id": "AWGE-002",
        "name": "Amazon Flex/Mechanical Turk — Rémunération sous SMIC, Surveillance IA Conducteurs & Réduction Paiements Rétroactive",
        "region": "Amérique du Nord",
        "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86,
        "weight": 0.20,
        "risk_level": "critique",
        "primary_pattern": "algorithmic_pay_reduction",
    },
    {
        "id": "AWGE-003",
        "name": "Deliveroo/Glovo Europe — Tarification par Course Opaque, Zéro Transparence Algorithme & Syndicats Bloqués",
        "region": "Europe Occidentale",
        "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78,
        "weight": 0.20,
        "risk_level": "critique",
        "primary_pattern": "opaque_algorithmic_pricing",
    },
    {
        "id": "AWGE-004",
        "name": "Plateformes Gig Inde (Zomato/Swiggy/Ola) — 50M+ Travailleurs, Absence Contrat & Frais Cachés Déduits Algorithme",
        "region": "Asie du Sud",
        "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73,
        "weight": 0.20,
        "risk_level": "critique",
        "primary_pattern": "hidden_fee_algorithmic_deduction",
    },
    {
        "id": "AWGE-005",
        "name": "Fiverr/Upwork Global — Commissions Opaques 20%, Scores Rétrogradation Arbitraire & Blocage Comptes sans Recours",
        "region": "Global",
        "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54,
        "weight": 0.20,
        "risk_level": "élevé",
        "primary_pattern": "platform_commission_opacity",
    },
    {
        "id": "AWGE-006",
        "name": "Gig Workers Collective — Organisation Résistance, Grèves Nationales & Litiges Collectifs vs Plateformes",
        "region": "Amérique du Nord",
        "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44,
        "weight": 0.20,
        "risk_level": "élevé",
        "primary_pattern": "worker_collective_action",
    },
    {
        "id": "AWGE-007",
        "name": "Directive EU Travailleurs Plateforme 2024 — Présomption Salariat, Application Nationale Variable & Résistance Lobbying",
        "region": "Europe",
        "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25,
        "weight": 0.20,
        "risk_level": "modéré",
        "primary_pattern": "regulatory_framework_partial",
    },
    {
        "id": "AWGE-008",
        "name": "OIT — Recommandation Travail Décent Économie Plateforme, Ratification Limitée & Impact Terrain Minimal",
        "region": "Global",
        "sub1": 13, "sub2": 11, "sub3": 9, "sub4": 7,
        "weight": 0.20,
        "risk_level": "faible",
        "primary_pattern": "international_labour_standard",
    },
]


def monte_carlo(entity, n=50_000):
    """Monte Carlo simulation for algorithmic wage theft risk assessment."""
    random.seed(42)
    successes = 0
    s1, s2, s3, s4 = entity["sub1"], entity["sub2"], entity["sub3"], entity["sub4"]
    for _ in range(n):
        sim_s1 = random.gauss(s1, 3.0)
        sim_s2 = random.gauss(s2, 3.0)
        sim_s3 = random.gauss(s3, 3.0)
        sim_s4 = random.gauss(s4, 3.0)
        sim_composite = sim_s1 * 0.30 + sim_s2 * 0.25 + sim_s3 * 0.25 + sim_s4 * 0.20
        if sim_composite >= 20:
            successes += 1
    return {
        "success_rate": round(successes / n * 100, 2),
        "simulations": n,
    }


def run():
    print("=" * 70)
    print("CaelumSwarm™ — Algorithmic Wage Theft & Gig Economy Engine")
    print(f"Wave-493 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    composites = []
    results = []

    for e in ENTITIES:
        composite = e["sub1"] * 0.30 + e["sub2"] * 0.25 + e["sub3"] * 0.25 + e["sub4"] * 0.20
        composite = round(composite, 2)
        composites.append(composite)

        mc = monte_carlo(e)
        results.append({**e, "composite": composite, "mc": mc})

        print(f"  [{e['risk_level'].upper()}] {e['id']}")
        print(f"    {e['name'][:75]}...")
        print(f"    composite={composite:.2f} | MC={mc['success_rate']}% ({mc['simulations']:,} sims)")

    avg_composite = round(sum(composites) / len(composites), 2)

    risk_dist = {}
    for e in results:
        risk_dist[e["risk_level"]] = risk_dist.get(e["risk_level"], 0) + 1

    print()
    print("-" * 70)
    print(f"avg_composite = {avg_composite}")
    print(f"Risk distribution: {risk_dist}")
    print(f"estimated_algorithmic_wage_theft_gig_economy_index = {round(avg_composite / 100 * 10, 2)}")
    print("=" * 70)

    output = {
        "agent": "Algorithmic Wage Theft & Gig Economy Engine",
        "domain": "algorithmic_wage_theft_gig_economy",
        "wave": 493,
        "total_entities": len(ENTITIES),
        "avg_composite": avg_composite,
        "risk_distribution": risk_dist,
        "estimated_algorithmic_wage_theft_gig_economy_index": round(avg_composite / 100 * 10, 2),
        "last_analysis": datetime.now().strftime("%Y-%m-%d"),
        "engine_version": "1.0.0",
        "data_sources": [
            "economic_policy_institute_wage_theft_gig_economy_report",
            "ilo_world_employment_social_outlook_platform_work",
            "algorithmic_management_worker_surveillance_uc_berkeley",
            "eu_platform_work_directive_impact_assessment_2024",
            "gig_workers_collective_wage_theft_documentation",
        ],
        "entities": [
            {
                "id": e["id"],
                "name": e["name"],
                "region": e["region"],
                "composite": r["composite"],
                "risk_level": e["risk_level"],
                "primary_pattern": e["primary_pattern"],
            }
            for e, r in zip(ENTITIES, results)
        ],
    }

    out_path = ROOT / "data" / "algorithmic_wage_theft_gig_economy_engine_output.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    estimated_algorithmic_wage_theft_gig_economy_index = round(avg_composite / 100 * 10, 2)
    return output


if __name__ == "__main__":
    run()
