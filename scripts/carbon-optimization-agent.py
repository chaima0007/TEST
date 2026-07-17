#!/usr/bin/env python3
"""
Carbon Optimization Agent — Caelum Partners CaelumSwarm™
Analyse et optimisation de l'empreinte carbone liée aux violations droits humains.
Corrèle impact carbone avec scores sociaux — approche double matérialité CSRD.
"""

import sys
from datetime import datetime, timezone

CARBON_DOMAIN_FACTORS = {
    "statelessness-document-rights": {
        "primary_carbon_link": "Déplacements forcés → transport émergence humanitaire",
        "scope_3_exposure": "MODÉRÉ",
        "carbon_intensity_factor": 0.3,
        "co2_proxy_ton_per_entity": 45_000,
        "nature_link": "Dégradation terres = apatridie autochtones",
    },
    "offshore-tax-haven-rights": {
        "primary_carbon_link": "Évasion fiscale → sous-investissement transition verte État",
        "scope_3_exposure": "ÉLEVÉ",
        "carbon_intensity_factor": 0.8,
        "co2_proxy_ton_per_entity": 250_000,
        "nature_link": "Financement industrie fossile via paradis fiscaux",
    },
    "deepfake-synthetic-media-rights": {
        "primary_carbon_link": "IA générative → consommation énergie serveurs (data centers)",
        "scope_3_exposure": "ÉLEVÉ",
        "carbon_intensity_factor": 0.6,
        "co2_proxy_ton_per_entity": 12_000,
        "nature_link": "Data centers → eau + énergie (refroidissement)",
    },
    "dark-web-cybercrime-rights": {
        "primary_carbon_link": "Cryptomonnaies → preuve de travail énergivore",
        "scope_3_exposure": "TRÈS ÉLEVÉ",
        "carbon_intensity_factor": 1.2,
        "co2_proxy_ton_per_entity": 85_000,
        "nature_link": "Mining crypto → déforestation (énergies renouvelables déplacées)",
    },
    "gig-economy-labor-exploitation": {
        "primary_carbon_link": "Livraisons courte distance → émissions last-mile",
        "scope_3_exposure": "MODÉRÉ",
        "carbon_intensity_factor": 0.4,
        "co2_proxy_ton_per_entity": 18_000,
        "nature_link": "Emballages usage unique → déchets plastique",
    },
    "default": {
        "primary_carbon_link": "Lien carbone indirect via chaîne de valeur",
        "scope_3_exposure": "MODÉRÉ",
        "carbon_intensity_factor": 0.5,
        "co2_proxy_ton_per_entity": 30_000,
        "nature_link": "Impact biodiversité via opérations",
    },
}

CARBON_REDUCTION_LEVERS = {
    "SUPPLIER_DECARBONIZATION": {
        "label": "Décarbonisation fournisseurs (Scope 3)",
        "potential_reduction_pct": 35,
        "implementation_cost": "ÉLEVÉ",
        "timeline_years": 3,
        "co_benefit": "Amélioration droits humains chaîne valeur T1-T3",
    },
    "RENEWABLE_ENERGY": {
        "label": "Passage énergies renouvelables (Scope 2)",
        "potential_reduction_pct": 25,
        "implementation_cost": "MODÉRÉ",
        "timeline_years": 1,
        "co_benefit": "Indépendance énergétique pays fournisseurs",
    },
    "OPERATIONAL_EFFICIENCY": {
        "label": "Efficacité opérationnelle (Scope 1)",
        "potential_reduction_pct": 15,
        "implementation_cost": "FAIBLE",
        "timeline_years": 1,
        "co_benefit": "Réduction coûts → investissement conformité DH",
    },
    "CARBON_OFFSETTING": {
        "label": "Compensation carbone certifiée (Gold Standard)",
        "potential_reduction_pct": 10,
        "implementation_cost": "MODÉRÉ",
        "timeline_years": 0,
        "co_benefit": "Projets co-bénéfices droits humains (reforestation communautaire)",
    },
    "CIRCULAR_ECONOMY": {
        "label": "Économie circulaire & allongement durée vie",
        "potential_reduction_pct": 20,
        "implementation_cost": "MODÉRÉ",
        "timeline_years": 2,
        "co_benefit": "Réduction déchets dans communautés vulnérables",
    },
}

CARBON_TARGETS = {
    "SBTi_1_5C": {"reduction_2030": 50, "reduction_2050": 100, "standard": "Science Based Targets initiative"},
    "EU_GREEN_DEAL": {"reduction_2030": 55, "reduction_2050": 100, "standard": "EU Fit for 55"},
    "NET_ZERO_2040": {"reduction_2030": 45, "reduction_2040": 100, "standard": "Net Zero 2040 Caelum"},
}


def calculate_carbon_risk(entity: dict, domain: str) -> dict:
    """Calcule le risque carbone lié à une entité droits humains."""
    domain_config = CARBON_DOMAIN_FACTORS.get(domain, CARBON_DOMAIN_FACTORS["default"])
    score = entity.get("composite_score", 0)

    carbon_intensity = domain_config["carbon_intensity_factor"]
    base_co2 = domain_config["co2_proxy_ton_per_entity"]

    estimated_co2 = base_co2 * (score / 100) * carbon_intensity
    carbon_price_EUR_ton = 65
    carbon_liability_EUR = estimated_co2 * carbon_price_EUR_ton

    stranded_asset_risk = "ÉLEVÉ" if score >= 70 and domain_config["scope_3_exposure"] == "TRÈS ÉLEVÉ" else "MODÉRÉ" if score >= 50 else "FAIBLE"

    return {
        "entity_id": entity.get("id"),
        "entity_name": entity.get("name"),
        "domain": domain,
        "composite_score": score,
        "carbon_analysis": {
            "primary_link": domain_config["primary_carbon_link"],
            "scope_3_exposure": domain_config["scope_3_exposure"],
            "estimated_co2_tons_yr": round(estimated_co2, 0),
            "carbon_liability_EUR": round(carbon_liability_EUR, -3),
            "nature_biodiversity_link": domain_config["nature_link"],
        },
        "stranded_asset_risk": stranded_asset_risk,
        "reduction_potential": {
            lever_key: {
                "reduction_pct": cfg["potential_reduction_pct"],
                "co2_saved_tons": round(estimated_co2 * cfg["potential_reduction_pct"] / 100, 0),
                "co_benefit": cfg["co_benefit"],
                "timeline_years": cfg["timeline_years"],
            }
            for lever_key, cfg in list(CARBON_REDUCTION_LEVERS.items())[:3]
        },
        "csrd_disclosure": {
            "esrs_e1": "Changement climatique — Émissions Scope 1/2/3",
            "esrs_e4": "Biodiversité — Impact nature via opérations",
            "double_materiality_trigger": estimated_co2 > 10_000,
        },
    }


def generate_carbon_report(entities: list, domain: str) -> dict:
    """Génère le rapport d'optimisation carbone pour un domaine."""
    analyses = [calculate_carbon_risk(e, domain) for e in entities]

    total_co2 = sum(a["carbon_analysis"]["estimated_co2_tons_yr"] for a in analyses)
    total_liability = sum(a["carbon_analysis"]["carbon_liability_EUR"] for a in analyses)

    high_carbon = sorted(analyses, key=lambda x: x["carbon_analysis"]["estimated_co2_tons_yr"], reverse=True)

    return {
        "report_type": "CARBON_OPTIMIZATION",
        "report_id": f"CO-{domain[:6].upper()}-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Carbon Optimization Agent v1.0",
        "domain": domain,
        "portfolio_carbon": {
            "total_co2_tons_yr": round(total_co2, 0),
            "total_carbon_liability_EUR": round(total_liability, -3),
            "highest_emitter": high_carbon[0]["entity_id"] if high_carbon else None,
            "paris_alignment": total_co2 < 100_000,
        },
        "reduction_roadmap": {
            target_name: {
                "target_reduction_pct": target_cfg.get("reduction_2030", 50),
                "co2_to_reduce_tons": round(total_co2 * target_cfg.get("reduction_2030", 50) / 100, 0),
                "standard": target_cfg["standard"],
            }
            for target_name, target_cfg in CARBON_TARGETS.items()
        },
        "entity_analyses": analyses,
        "top_levers": [
            {
                "lever": cfg["label"],
                "potential_reduction_pct": cfg["potential_reduction_pct"],
                "total_portfolio_saving_tons": round(total_co2 * cfg["potential_reduction_pct"] / 100, 0),
                "human_rights_co_benefit": cfg["co_benefit"],
            }
            for lever_key, cfg in CARBON_REDUCTION_LEVERS.items()
        ][:3],
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — CARBON OPTIMIZATION AGENT")
    print("  Empreinte Carbone & Double Matérialité CSRD ESRS E1/E4")
    print("=" * 70)

    entities = [
        {"id": "OTH-001", "name": "Îles Caïmans — Financement Fossile", "composite_score": 91.60, "risk_level": "critique"},
        {"id": "OTH-002", "name": "Luxembourg — Rulings Fiscaux", "composite_score": 87.40, "risk_level": "critique"},
        {"id": "OTH-007", "name": "Irlande — GAFA Optimisation", "composite_score": 26.65, "risk_level": "modéré"},
        {"id": "OTH-008", "name": "Danemark — OCDE 15%", "composite_score": 6.45, "risk_level": "faible"},
    ]

    report = generate_carbon_report(entities, "offshore-tax-haven-rights")

    p = report["portfolio_carbon"]
    print(f"\n🌍 RAPPORT CARBONE: {report['report_id']}")
    print(f"   Domaine: {report['domain']}")
    print(f"   CO2 total estimé: {p['total_co2_tons_yr']:,.0f} tonnes/an")
    print(f"   Passif carbone: {p['total_carbon_liability_EUR']:,.0f}€")
    print(f"   Alignement Paris: {'✅ OUI' if p['paris_alignment'] else '❌ NON'}")
    print(f"   Émetteur principal: {p['highest_emitter']}")

    print(f"\n📊 LEVIERS DE RÉDUCTION TOP 3:")
    for lever in report["top_levers"]:
        print(f"\n   • {lever['lever']}")
        print(f"     Réduction: {lever['potential_reduction_pct']}% → {lever['total_portfolio_saving_tons']:,.0f} t CO2 économisées")
        print(f"     Co-bénéfice DH: {lever['human_rights_co_benefit'][:65]}...")

    print(f"\n🎯 FEUILLE DE ROUTE RÉDUCTION:")
    for target, details in report["reduction_roadmap"].items():
        print(f"   {target}: -{details['target_reduction_pct']}% ({details['co2_to_reduce_tons']:,.0f}t) | {details['standard']}")

    print(f"\n✅ Carbon Optimization Agent — Rapport généré avec succès")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
