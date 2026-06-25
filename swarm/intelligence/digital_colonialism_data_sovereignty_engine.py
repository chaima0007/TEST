#!/usr/bin/env python3
"""CaelumSwarm™ — Digital Colonialism & Data Sovereignty Engine (Wave-493)"""
import random
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent

ENTITIES = [
    {
        "id": "DCDS-001",
        "name": "Meta/Google — Extraction Massive Données Africaines sans Consentement, Profit Unilatéral & Absence Cadre Légal Local",
        "region": "Afrique Sub-Saharienne",
        "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93,
        "weight": 0.20,
        "risk_level": "critique",
        "primary_pattern": "data_extraction_without_consent",
    },
    {
        "id": "DCDS-002",
        "name": "Câbles Sous-Marins & Infrastructure Cloud — Monopole Occidental sur Routage Données Globales du Sud",
        "region": "Global Sud",
        "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86,
        "weight": 0.20,
        "risk_level": "critique",
        "primary_pattern": "infrastructure_control",
    },
    {
        "id": "DCDS-003",
        "name": "Inde — Pression GAFAM contre Loi Protection Données Personnelles & Souveraineté Numérique",
        "region": "Asie du Sud",
        "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78,
        "weight": 0.20,
        "risk_level": "critique",
        "primary_pattern": "sovereignty_erosion",
    },
    {
        "id": "DCDS-004",
        "name": "Brésil/Amérique Latine — Dépendance Plateformes US, Fuite Données Communautés Indigènes & LGPD Contournée",
        "region": "Amérique Latine",
        "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73,
        "weight": 0.20,
        "risk_level": "critique",
        "primary_pattern": "indigenous_data_exploitation",
    },
    {
        "id": "DCDS-005",
        "name": "Union Africaine — Cadre Malabo Cybersécurité, Ratifications Limitées & Souveraineté Numérique Continentale",
        "region": "Afrique",
        "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54,
        "weight": 0.20,
        "risk_level": "élevé",
        "primary_pattern": "regulatory_gap",
    },
    {
        "id": "DCDS-006",
        "name": "Startups Fintech Asie du Sud-Est — APIs Étrangères Imposées, Dépendance Technologique & Capture Données",
        "region": "Asie du Sud-Est",
        "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44,
        "weight": 0.20,
        "risk_level": "élevé",
        "primary_pattern": "api_dependency_capture",
    },
    {
        "id": "DCDS-007",
        "name": "RGPD UE — Standard de Référence Souveraineté Données, Influence Limitée hors Europe",
        "region": "Europe",
        "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25,
        "weight": 0.20,
        "risk_level": "modéré",
        "primary_pattern": "partial_regulatory_protection",
    },
    {
        "id": "DCDS-008",
        "name": "ONU — Groupe Experts Gouvernance Internet, Résolutions Souveraineté Numérique & Impact Limité",
        "region": "Global",
        "sub1": 13, "sub2": 11, "sub3": 9, "sub4": 7,
        "weight": 0.20,
        "risk_level": "faible",
        "primary_pattern": "international_advocacy",
    },
]


def monte_carlo(entity, n=50_000):
    """Monte Carlo simulation for digital colonialism risk assessment."""
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
    print("CaelumSwarm™ — Digital Colonialism & Data Sovereignty Engine")
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
    print(f"estimated_digital_colonialism_data_sovereignty_index = {round(avg_composite / 100 * 10, 2)}")
    print("=" * 70)

    output = {
        "agent": "Digital Colonialism & Data Sovereignty Engine",
        "domain": "digital_colonialism_data_sovereignty",
        "wave": 493,
        "total_entities": len(ENTITIES),
        "avg_composite": avg_composite,
        "risk_distribution": risk_dist,
        "estimated_digital_colonialism_data_sovereignty_index": round(avg_composite / 100 * 10, 2),
        "last_analysis": datetime.now().strftime("%Y-%m-%d"),
        "engine_version": "1.0.0",
        "data_sources": [
            "algorithmic_watch_data_colonialism_global_report",
            "decolonising_digital_data_governance_initiative",
            "unctad_digital_economy_report_data_sovereignty",
            "african_union_malabo_convention_cybersecurity",
            "un_secretary_general_our_common_agenda_digital",
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

    out_path = ROOT / "data" / "digital_colonialism_data_sovereignty_engine_output.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    estimated_digital_colonialism_data_sovereignty_index = round(avg_composite / 100 * 10, 2)
    return output


if __name__ == "__main__":
    run()
