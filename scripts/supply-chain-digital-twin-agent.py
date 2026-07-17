"""
Supply Chain Digital Twin Agent — CaelumSwarm™
Technology: Digital Twin + IoT + Blockchain + AI simulation
Role: Jumeau numérique chaîne de valeur pour simulation risques CSDDD 2024
"""

import hashlib
import json
import random
import datetime

DIGITAL_TWIN_ARCHITECTURE = {
    "layers": {
        "physical": "Fournisseurs réels (Tier 1-2-3) avec capteurs IoT",
        "data": "Collecte temps réel (ERP, IoT, APIs tiers, ONG feeds)",
        "simulation": "Modèle digital twin (graphe de connaissance + ML)",
        "intelligence": "IA prédictive — scenarios risques, what-if analysis",
        "visualization": "Dashboard 3D chaîne de valeur + alertes temps réel",
    },
    "update_frequency": "Every 15min (IoT) / 1h (ERP sync) / 24h (ONG feeds)",
    "nodes_count": 847,
    "relationships_count": 3241,
    "data_sources": 23,
}

SUPPLY_CHAIN_GRAPH = {
    "tiers": {
        "tier_0": {"name": "Entreprise cliente", "count": 1},
        "tier_1": {"name": "Fournisseurs directs", "count": 45, "coverage": "100%"},
        "tier_2": {"name": "Sous-fournisseurs", "count": 312, "coverage": "78%"},
        "tier_3": {"name": "Matières premières", "count": 490, "coverage": "34%"},
    },
    "node_attributes": [
        "country", "sector", "risk_score", "csddd_wave_index",
        "employees", "certifications", "last_audit_date",
        "geopolitical_risk_level", "environmental_risk_level",
        "child_labor_risk", "forced_labor_risk",
    ],
    "relationships": {
        "SUPPLIES_TO": "Fournisseur → Client",
        "LOCATED_IN": "Entité → Pays",
        "CERTIFIED_BY": "Entité → Certification",
        "SHARES_RISK_WITH": "Entité → Entité (même zone géo/risque)",
        "AUDITED_BY": "Entité → Organisme audit",
    },
}

SIMULATION_SCENARIOS = {
    "geopolitical_disruption": {
        "trigger": "Conflit armé dans pays fournisseur Tier 2",
        "affected_nodes": "Simulation propagation sur le graphe",
        "impact": {
            "supply_disruption_%": 23,
            "affected_tier1_suppliers": 8,
            "csddd_risk_increase": "+12 points composite",
            "alternative_sourcing_options": 3,
        },
        "mitigation": "Diversification géographique recommandée (< 30% par pays)",
    },
    "child_labor_scandal": {
        "trigger": "Rapport ONG sur travail enfants chez Tier 3 cacao",
        "propagation": "Tier 3 → Tier 2 → Tier 1 → Entreprise (contamination réputation)",
        "media_exposure_days": 14,
        "financial_impact_eur": 45000000,
        "csddd_art9_remediation_required": True,
    },
    "climate_shock": {
        "trigger": "Sécheresse extrême zone agricole fournisseur clé",
        "supply_reduction_%": 35,
        "price_impact": "+28%",
        "workers_affected": 12000,
        "human_rights_risk": "Migration forcée, perte revenus",
    },
    "regulatory_change": {
        "trigger": "Extension CSDDD aux PME (< 250 salariés) 2026",
        "new_suppliers_in_scope": 189,
        "compliance_gap_count": 67,
        "estimated_remediation_months": 18,
    },
}

IOT_DATA_STREAMS = {
    "factory_sensors": {
        "metrics": ["temperature", "humidity", "air_quality_index", "noise_db", "machine_hours"],
        "purpose": "Détection conditions dangereuses — droits travailleurs",
        "alert_threshold": {"air_quality_index": ">150 AQI → alerte critique"},
    },
    "logistics_tracking": {
        "metrics": ["gps_position", "transport_duration", "border_crossings", "customs_delays"],
        "purpose": "Traçabilité chaîne — conformité CSDDD Art.8",
    },
    "environmental_sensors": {
        "metrics": ["water_quality", "soil_contamination", "co2_emissions", "deforestation_alerts"],
        "purpose": "Surveillance impacts environnementaux",
        "data_source": "Satellite + IoT terrain",
    },
}

BLOCKCHAIN_AUDIT_TRAIL = {
    "network": "Hyperledger Fabric (privé, consortium)",
    "participants": ["Caelum Partners", "Fournisseurs Tier 1", "Auditeurs certifiés", "ONG partenaires", "Régulateurs UE"],
    "smart_contracts": {
        "supplier_onboarding": "Enregistrement immuable certification fournisseur",
        "audit_record": "Résultats audit CSDDD certifiés par tiers",
        "alert_record": "Alertes violations droits humains horodatées",
        "remediation_tracking": "Suivi plan d'action correctif Art.9",
    },
    "immutability": "SHA256 chaining, consensus Raft (3/5 nœuds)",
}


# ─────────────────────────────────────────
# FONCTIONS
# ─────────────────────────────────────────

def simulate_supply_chain_disruption(trigger_event: str, affected_country: str) -> dict:
    """Simule la propagation d'une perturbation dans la chaîne d'approvisionnement."""
    random.seed(hash(trigger_event + affected_country) % (2**31))
    tier3_affected = random.randint(15, 60)
    tier2_affected = int(tier3_affected * 0.4)
    tier1_affected = int(tier2_affected * 0.3)
    financial_impact = random.randint(5_000_000, 80_000_000)
    recovery_weeks = random.randint(4, 24)
    return {
        "trigger_event": trigger_event,
        "affected_country": affected_country,
        "propagation": {
            "tier_3_nodes_affected": tier3_affected,
            "tier_2_nodes_affected": tier2_affected,
            "tier_1_nodes_affected": tier1_affected,
            "total_nodes_affected": tier3_affected + tier2_affected + tier1_affected,
        },
        "impact": {
            "supply_disruption_pct": round(tier1_affected / 45 * 100, 1),
            "financial_impact_eur": financial_impact,
            "workers_at_risk": random.randint(1000, 50000),
            "csddd_risk_delta": f"+{random.randint(5, 20)} points",
        },
        "mitigation": {
            "alternative_suppliers": random.randint(2, 6),
            "estimated_recovery_weeks": recovery_weeks,
            "recommended_action": "Activer fournisseurs alternatifs + audit terrain urgence",
        },
        "simulated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }


def trace_supplier_to_violation(supplier_id: str, violation_type: str) -> dict:
    """Remonte la chaîne de traçabilité d'un fournisseur jusqu'à la violation détectée."""
    trace_path = [
        {
            "node": "Entreprise cliente (Tier 0)",
            "id": "caelum-client-001",
            "role": "Donneur d'ordre",
            "csddd_responsibility": "Art.5 — Politique due diligence",
        },
        {
            "node": "Fournisseur direct (Tier 1)",
            "id": "supplier-t1-" + supplier_id[:8],
            "country": "Côte d'Ivoire",
            "sector": "Agroalimentaire",
            "certifications": ["Rainforest Alliance", "UTZ"],
            "last_audit": "2025-11-15",
        },
        {
            "node": "Sous-fournisseur (Tier 2)",
            "id": "supplier-t2-" + supplier_id[:6],
            "country": "Côte d'Ivoire (région Soubré)",
            "sector": "Collecte cacao",
            "certifications": [],
            "last_audit": "2024-03-20",
            "risk_flags": ["child_labor_risk: HIGH", "audit_gap > 12 mois"],
        },
        {
            "node": "Producteur matière première (Tier 3)",
            "id": supplier_id,
            "country": "Côte d'Ivoire (plantation)",
            "sector": "Agriculture cacao",
            "violation_detected": violation_type,
            "source": "Rapport ONG Terre des Hommes + capteurs IoT",
            "evidence_hash": hashlib.sha256((supplier_id + violation_type).encode()).hexdigest(),
        },
    ]
    return {
        "supplier_id": supplier_id,
        "violation_type": violation_type,
        "trace_depth": len(trace_path),
        "trace_path": trace_path,
        "blockchain_record": {
            "tx_id": hashlib.sha256(supplier_id.encode()).hexdigest()[:32],
            "block_height": random.randint(10000, 99999),
            "network": "Hyperledger Fabric caelum-consortium",
            "status": "IMMUTABLE",
        },
        "csddd_obligations": {
            "Art8": "Due diligence — cartographie risque Tier 3 requise",
            "Art9": "Plan de remédiation — délai 6 mois",
            "Art10": "Rapport annuel — violation à documenter",
        },
        "traced_at": datetime.datetime.utcnow().isoformat() + "Z",
    }


def calculate_supply_chain_risk_exposure(company: str) -> dict:
    """Calcule l'exposition aux risques CSDDD de la chaîne d'approvisionnement d'une entreprise."""
    random.seed(hash(company) % (2**31))
    high_risk_suppliers = random.randint(20, 80)
    medium_risk_suppliers = random.randint(100, 200)
    low_risk_suppliers = 847 - high_risk_suppliers - medium_risk_suppliers
    revenue = 500_000_000
    max_fine_pct = 0.05  # 5% CA — CSDDD Art.22
    return {
        "company": company,
        "revenue_eur": revenue,
        "supply_chain_nodes": 847,
        "risk_distribution": {
            "high_risk": high_risk_suppliers,
            "medium_risk": medium_risk_suppliers,
            "low_risk": max(0, low_risk_suppliers),
        },
        "risk_scores": {
            "child_labor_risk_index": round(random.uniform(0.15, 0.45), 3),
            "forced_labor_risk_index": round(random.uniform(0.08, 0.25), 3),
            "environmental_risk_index": round(random.uniform(0.20, 0.50), 3),
            "geopolitical_risk_index": round(random.uniform(0.10, 0.35), 3),
            "composite_csddd_score": round(random.uniform(0.25, 0.55), 3),
        },
        "financial_exposure": {
            "max_fine_csddd_eur": int(revenue * max_fine_pct),
            "estimated_remediation_cost_eur": random.randint(2_000_000, 15_000_000),
            "reputational_risk_eur": random.randint(10_000_000, 100_000_000),
        },
        "compliance_gaps": {
            "suppliers_without_audit": random.randint(50, 150),
            "suppliers_without_contract_clauses": random.randint(30, 100),
            "tier3_unknown": 490 - int(490 * 0.34),
        },
        "calculated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }


def generate_what_if_scenario(scenario_name: str, parameters: dict) -> dict:
    """Génère un scénario what-if sur le digital twin avec les paramètres fournis."""
    base = SIMULATION_SCENARIOS.get(scenario_name, {}).copy()
    base["scenario_name"] = scenario_name
    base["custom_parameters"] = parameters
    base["twin_state_before"] = {
        "nodes_count": 847,
        "relationships_count": 3241,
        "composite_risk_score": round(random.uniform(0.30, 0.50), 3),
        "compliant_suppliers_pct": round(random.uniform(55, 75), 1),
    }
    impact_multiplier = parameters.get("severity_multiplier", 1.0)
    base["twin_state_after"] = {
        "nodes_count": 847,
        "relationships_count": 3241,
        "composite_risk_score": round(
            base["twin_state_before"]["composite_risk_score"] + 0.12 * impact_multiplier, 3
        ),
        "compliant_suppliers_pct": round(
            base["twin_state_before"]["compliant_suppliers_pct"] - 8 * impact_multiplier, 1
        ),
        "disrupted_nodes": int(50 * impact_multiplier),
    }
    base["recommendation"] = (
        "Diversification géographique + audits d'urgence Tier 2/3 "
        "+ activation clauses contractuelles CSDDD Art.8"
    )
    base["generated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    return base


# ─────────────────────────────────────────
# BLOC PRINCIPAL
# ─────────────────────────────────────────

def main():
    separator = "=" * 70

    # ── Section 1 : Architecture Digital Twin ────────────────────────────
    print(separator)
    print("SECTION 1 — Supply Chain Digital Twin Architecture")
    print(separator)
    print(json.dumps(DIGITAL_TWIN_ARCHITECTURE, indent=2, ensure_ascii=False))

    # ── Section 2 : Graph Statistics ─────────────────────────────────────
    print(f"\n{separator}")
    print("SECTION 2 — Graph Statistics (847 nœuds, 3241 relations, 4 tiers)")
    print(separator)
    tiers = SUPPLY_CHAIN_GRAPH["tiers"]
    total_nodes = sum(v["count"] for v in tiers.values())
    print(f"Total nœuds modélisés : {DIGITAL_TWIN_ARCHITECTURE['nodes_count']}")
    print(f"Total relations       : {DIGITAL_TWIN_ARCHITECTURE['relationships_count']}")
    print(f"Sources de données    : {DIGITAL_TWIN_ARCHITECTURE['data_sources']}")
    print("\nDétail par tier :")
    for tier_id, tier_info in tiers.items():
        coverage = tier_info.get("coverage", "N/A")
        print(f"  {tier_id} — {tier_info['name']}: {tier_info['count']} nœuds (couverture: {coverage})")
    print("\nAttributs nœud :")
    for attr in SUPPLY_CHAIN_GRAPH["node_attributes"]:
        print(f"  • {attr}")
    print("\nTypes de relations :")
    for rel, desc in SUPPLY_CHAIN_GRAPH["relationships"].items():
        print(f"  {rel}: {desc}")

    # ── Section 3 : Geopolitical Disruption Simulation ───────────────────
    print(f"\n{separator}")
    print("SECTION 3 — Simulation: Geopolitical Disruption (conflit zone cacao)")
    print(separator)
    disruption = simulate_supply_chain_disruption(
        trigger_event="Conflit armé — instabilité politique majeure",
        affected_country="Côte d'Ivoire"
    )
    print(json.dumps(disruption, indent=2, ensure_ascii=False))

    # ── Section 4 : Child Labor Scandal Propagation ──────────────────────
    print(f"\n{separator}")
    print("SECTION 4 — Child Labor Scandal Propagation (Tier 3 → Tier 1 → media)")
    print(separator)
    scandal = SIMULATION_SCENARIOS["child_labor_scandal"].copy()
    scandal["propagation_timeline"] = [
        {"day": 0, "event": "Rapport ONG publié — travail enfants détecté Tier 3 (plantation cacao)"},
        {"day": 1, "event": "Digital twin alerte automatique — nœuds Tier 2 connectés marqués HIGH RISK"},
        {"day": 2, "event": "Notification automatique Tier 1 fournisseurs — clause contractuelle activée"},
        {"day": 3, "event": "Médias sociaux — hashtag viral, 850K mentions en 48h"},
        {"day": 5, "event": "Presse nationale — articles Le Monde, Financial Times"},
        {"day": 7, "event": "Régulateur UE — demande rapport due diligence CSDDD Art.10"},
        {"day": 14, "event": "Plan remédiation Art.9 soumis — audit terrain lancé 3 pays"},
    ]
    scandal["csddd_obligations_triggered"] = ["Art.7 (prévention)", "Art.8 (due diligence)", "Art.9 (remédiation)", "Art.10 (rapport)"]
    print(json.dumps(scandal, indent=2, ensure_ascii=False))

    # ── Section 5 : IoT Data Streams ─────────────────────────────────────
    print(f"\n{separator}")
    print("SECTION 5 — IoT Data Streams (3 catégories)")
    print(separator)
    print(json.dumps(IOT_DATA_STREAMS, indent=2, ensure_ascii=False))
    # Simulation live IoT reading
    print("\nSimulation lecture IoT temps réel :")
    live_readings = {
        "factory_sensors": {
            "temperature_c": round(random.uniform(18, 42), 1),
            "humidity_pct": round(random.uniform(40, 90), 1),
            "air_quality_index": random.randint(60, 200),
            "noise_db": round(random.uniform(65, 110), 1),
            "machine_hours_today": random.randint(4, 14),
            "alert": None,
        },
        "logistics": {
            "active_shipments": random.randint(50, 200),
            "border_crossings_pending": random.randint(3, 25),
            "avg_customs_delay_hours": random.randint(2, 72),
        },
        "environmental": {
            "water_quality_index": round(random.uniform(40, 95), 1),
            "co2_tonnes_today": round(random.uniform(0.5, 8.0), 2),
            "deforestation_alerts_active": random.randint(0, 5),
        },
    }
    aqi = live_readings["factory_sensors"]["air_quality_index"]
    if aqi > 150:
        live_readings["factory_sensors"]["alert"] = "CRITIQUE — AQI > 150 : conditions dangereuses détectées"
    print(json.dumps(live_readings, indent=2, ensure_ascii=False))

    # ── Section 6 : Supplier Tracing ─────────────────────────────────────
    print(f"\n{separator}")
    print("SECTION 6 — Supplier Tracing (Nestlé → cacao Tier 3 → violation)")
    print(separator)
    trace = trace_supplier_to_violation(
        supplier_id="sup-t3-cacao-ivory-00847",
        violation_type="CHILD_LABOR_CONFIRMED"
    )
    print(json.dumps(trace, indent=2, ensure_ascii=False))

    # ── Section 7 : Risk Exposure Calculation ────────────────────────────
    print(f"\n{separator}")
    print("SECTION 7 — Risk Exposure Calculation (entreprise 500M€ CA)")
    print(separator)
    exposure = calculate_supply_chain_risk_exposure("Caelum Enterprise SA (exemple 500M EUR CA)")
    print(f"Entreprise             : {exposure['company']}")
    print(f"Chiffre d'affaires     : {exposure['revenue_eur']:,} EUR")
    print(f"Nœuds chaîne           : {exposure['supply_chain_nodes']}")
    print("\nDistribution risques :")
    for level, count in exposure["risk_distribution"].items():
        print(f"  {level}: {count} fournisseurs")
    print("\nScores de risque :")
    for metric, score in exposure["risk_scores"].items():
        print(f"  {metric}: {score}")
    print("\nExposition financière :")
    for item, amount in exposure["financial_exposure"].items():
        print(f"  {item}: {amount:,} EUR")
    print("\nGaps de conformité :")
    for gap, count in exposure["compliance_gaps"].items():
        print(f"  {gap}: {count}")

    # ── Section 8 : Blockchain Audit Trail ───────────────────────────────
    print(f"\n{separator}")
    print("SECTION 8 — Blockchain Audit Trail (Hyperledger Fabric, 5 participants)")
    print(separator)
    print(json.dumps(BLOCKCHAIN_AUDIT_TRAIL, indent=2, ensure_ascii=False))
    # Simulation d'une transaction blockchain
    print("\nSimulation transaction blockchain :")
    tx_data = {
        "event": "AUDIT_RECORD",
        "supplier_id": "sup-t1-cacao-ivory-00023",
        "audit_result": "NON_CONFORMANT",
        "csddd_article": "Art.8",
        "auditor": "Bureau Veritas",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }
    tx_hash = hashlib.sha256(json.dumps(tx_data, sort_keys=True).encode()).hexdigest()
    blockchain_tx = {
        "tx_id": tx_hash[:32],
        "block_height": random.randint(10000, 99999),
        "channel": "caelum-supply-chain",
        "chaincode": "audit_record",
        "status": "COMMITTED",
        "endorsers": ["Caelum Partners", "Bureau Veritas", "Régulateur UE"],
        "payload_hash": tx_hash,
        "data": tx_data,
    }
    print(json.dumps(blockchain_tx, indent=2, ensure_ascii=False))

    # ── Section 9 : CSDDD Compliance Score ───────────────────────────────
    print(f"\n{separator}")
    print("SECTION 9 — CSDDD Compliance Score (Digital Twin — Art.8 Due Diligence)")
    print(separator)
    what_if = generate_what_if_scenario(
        "regulatory_change",
        {"severity_multiplier": 1.2, "scope": "Extension PME 2026"}
    )
    csddd_score = {
        "twin_coverage": {
            "tier_1_pct": 100,
            "tier_2_pct": 78,
            "tier_3_pct": 34,
            "overall_pct": round((100 + 78 + 34) / 3, 1),
        },
        "compliance_articles": {
            "Art5_policy": {"status": "COMPLIANT", "score": 95},
            "Art6_risk_identification": {"status": "COMPLIANT", "score": 88},
            "Art7_prevention": {"status": "PARTIAL", "score": 72},
            "Art8_due_diligence": {"status": "PARTIAL", "score": 65},
            "Art9_remediation": {"status": "IN_PROGRESS", "score": 58},
            "Art10_reporting": {"status": "COMPLIANT", "score": 90},
        },
        "global_csddd_score": 78,
        "grade": "B+",
        "next_review_date": "2026-09-22",
        "what_if_regulatory_extension": {
            "new_suppliers_in_scope": 189,
            "compliance_gap_count": 67,
            "estimated_remediation_months": 18,
            "projected_score_after_remediation": 91,
        },
        "twin_strengths": [
            "Traçabilité Tier 1 complète (100%)",
            "IoT temps réel — détection anomalies < 15 min",
            "Blockchain audit trail — immuabilité certifiée Hyperledger",
            "Simulation scénarios risques — propagation graphe ML",
        ],
        "twin_gaps": [
            "Tier 3 couverture 34% — extension nécessaire",
            "Art.9 remédiation — plans correctifs incomplets (42%)",
            "PME Tier 2 sans clauses contractuelles CSDDD (38 fournisseurs)",
        ],
        "evaluated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    print(json.dumps(csddd_score, indent=2, ensure_ascii=False))

    # ── Section 10 : Statut agent ─────────────────────────────────────────
    print(f"\n{separator}")
    print("Supply Chain Digital Twin Agent — PRÊT (847 nœuds / IoT / Hyperledger / AI Simulation)")
    print(separator)


if __name__ == "__main__":
    main()
