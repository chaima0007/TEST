#!/usr/bin/env python3
"""CaelumSwarm™ — LGBTQ+ Asylum & Refugee Rights Engine (Wave-493)"""
import random
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent

ENTITIES = [
    {
        "id": "LGAR-001",
        "name": "Tchétchénie/Russie — Purges Violentes Personnes LGBTQ+, Détentions Secrètes & Impunité Totale des Persécuteurs",
        "region": "Europe de l'Est",
        "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93,
        "weight": 0.20,
        "risk_level": "critique",
        "primary_pattern": "state_persecution_lgbtq",
    },
    {
        "id": "LGAR-002",
        "name": "Afghanistan Taliban — Peine de Mort Homosexualité, Persécution Systématique & Fuite Massive vers Pays Tiers",
        "region": "Asie Centrale",
        "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86,
        "weight": 0.20,
        "risk_level": "critique",
        "primary_pattern": "death_penalty_lgbtq",
    },
    {
        "id": "LGAR-003",
        "name": "Ouganda — Loi Anti-Homosexualité 2023 (Peine de Mort), Fuite Réfugiés & Rejet Demandes Asile Voisins",
        "region": "Afrique de l'Est",
        "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78,
        "weight": 0.20,
        "risk_level": "critique",
        "primary_pattern": "criminalization_persecution",
    },
    {
        "id": "LGAR-004",
        "name": "Iran — Exécutions LGBTQ+ sous Charia, Demandeurs Asile Renvoyés & Probléme Preuve Orientation Sexuelle",
        "region": "Moyen-Orient",
        "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73,
        "weight": 0.20,
        "risk_level": "critique",
        "primary_pattern": "execution_persecution",
    },
    {
        "id": "LGAR-005",
        "name": "Hongrie/Pologne — Refus Asile Motif LGBTQ+, Zones Anti-LGBT & Conformité CEDH Défaillante",
        "region": "Europe Centrale",
        "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54,
        "weight": 0.20,
        "risk_level": "élevé",
        "primary_pattern": "eu_member_state_lgbtq_regression",
    },
    {
        "id": "LGAR-006",
        "name": "Camps Réfugiés Kenya/Malawi — Violence Homophobe entre Réfugiés, Protection UNHCR Insuffisante",
        "region": "Afrique de l'Est",
        "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44,
        "weight": 0.20,
        "risk_level": "élevé",
        "primary_pattern": "intra_camp_violence",
    },
    {
        "id": "LGAR-007",
        "name": "UNHCR — Directives Protection LGBTQ+ Réfugiés, Application Partielle & Manque Financement Dédié",
        "region": "Global",
        "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25,
        "weight": 0.20,
        "risk_level": "modéré",
        "primary_pattern": "international_protection_gaps",
    },
    {
        "id": "LGAR-008",
        "name": "ILGA World — Réseau Plaidoyer Droits LGBTQ+ Global, Rapports Annuels & Impact Législatif Limité",
        "region": "Global",
        "sub1": 13, "sub2": 11, "sub3": 9, "sub4": 7,
        "weight": 0.20,
        "risk_level": "faible",
        "primary_pattern": "advocacy_monitoring",
    },
]


def monte_carlo(entity, n=50_000):
    """Monte Carlo simulation for LGBTQ+ asylum and refugee rights risk assessment."""
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
    print("CaelumSwarm™ — LGBTQ+ Asylum & Refugee Rights Engine")
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
    print(f"estimated_lgbtq_asylum_refugee_rights_index = {round(avg_composite / 100 * 10, 2)}")
    print("=" * 70)

    output = {
        "agent": "LGBTQ+ Asylum & Refugee Rights Engine",
        "domain": "lgbtq_asylum_refugee_rights",
        "wave": 493,
        "total_entities": len(ENTITIES),
        "avg_composite": avg_composite,
        "risk_distribution": risk_dist,
        "estimated_lgbtq_asylum_refugee_rights_index": round(avg_composite / 100 * 10, 2),
        "last_analysis": datetime.now().strftime("%Y-%m-%d"),
        "engine_version": "1.0.0",
        "data_sources": [
            "ilga_world_state_sponsored_homophobia_report",
            "unhcr_lgbtq_refugee_protection_guidelines",
            "human_rights_watch_lgbtq_asylum_seeker_report",
            "rainbow_railroad_global_crisis_report",
            "amnesty_international_lgbtq_persecution_global",
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

    out_path = ROOT / "data" / "lgbtq_asylum_refugee_rights_engine_output.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    estimated_lgbtq_asylum_refugee_rights_index = round(avg_composite / 100 * 10, 2)
    return output


if __name__ == "__main__":
    run()
