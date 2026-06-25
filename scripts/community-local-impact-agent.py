#!/usr/bin/env python3
"""
Community & Local Impact Agent — Caelum Partners CaelumSwarm™
Évalue l'impact local et communautaire des violations droits humains.
Mesure les effets sur les communautés riveraines des opérations.
"""

import sys
from datetime import datetime, timezone

COMMUNITY_IMPACT_DIMENSIONS = {
    "livelihoods": {"weight": 0.20, "label": "Moyens de subsistance"},
    "health_wellbeing": {"weight": 0.20, "label": "Santé et bien-être"},
    "cultural_heritage": {"weight": 0.15, "label": "Patrimoine culturel"},
    "land_resources": {"weight": 0.20, "label": "Accès terres et ressources"},
    "social_cohesion": {"weight": 0.15, "label": "Cohésion sociale"},
    "political_voice": {"weight": 0.10, "label": "Voix politique"},
}

COMMUNITY_TYPES = {
    "INDIGENOUS": {
        "label": "Peuples autochtones",
        "protection_frameworks": ["UNDRIP 2007", "ILO C169", "CSDDD Art.3"],
        "consultation_standard": "CLIP — Consentement Libre Informé Préalable",
        "vulnerability_multiplier": 1.5,
    },
    "RURAL_AGRICULTURAL": {
        "label": "Communautés rurales agricoles",
        "protection_frameworks": ["UNDROP 2018", "ICESCR Art.11"],
        "consultation_standard": "Participation significative",
        "vulnerability_multiplier": 1.2,
    },
    "URBAN_MARGINALIZED": {
        "label": "Communautés urbaines marginalisées",
        "protection_frameworks": ["ICCPR", "ICESCR", "CSDDD"],
        "consultation_standard": "Engagement communautaire",
        "vulnerability_multiplier": 1.1,
    },
    "MIGRANT_WORKERS": {
        "label": "Travailleurs migrants",
        "protection_frameworks": ["ICRMW 1990", "ILO C97", "ILO C143"],
        "consultation_standard": "Information linguistique + syndicats",
        "vulnerability_multiplier": 1.3,
    },
    "STATELESS": {
        "label": "Populations apatrides",
        "protection_frameworks": ["Convention 1954", "Convention 1961", "UNHCR Guidelines"],
        "consultation_standard": "Représentation par mandataire autorisé",
        "vulnerability_multiplier": 1.6,
    },
}

SROI_INDICATORS = {
    "jobs_lost": {"unit": "emplois", "weight_EUR_per_unit": 15_000},
    "households_displaced": {"unit": "ménages", "weight_EUR_per_unit": 35_000},
    "children_school_dropout": {"unit": "enfants", "weight_EUR_per_unit": 25_000},
    "health_cases": {"unit": "cas médicaux", "weight_EUR_per_unit": 8_000},
    "cultural_sites_lost": {"unit": "sites", "weight_EUR_per_unit": 500_000},
    "water_access_lost": {"unit": "personnes", "weight_EUR_per_unit": 2_000},
}

COMMUNITY_BENEFIT_PROGRAMS = {
    "LIVELIHOOD_RESTORATION": {
        "label": "Programme restauration moyens subsistance",
        "cost_per_household_EUR": 5_000,
        "effectiveness": 0.75,
        "timeline_months": 12,
    },
    "COMMUNITY_HEALTH_FUND": {
        "label": "Fonds santé communautaire",
        "cost_per_household_EUR": 2_000,
        "effectiveness": 0.80,
        "timeline_months": 6,
    },
    "CULTURAL_PRESERVATION": {
        "label": "Préservation patrimoine culturel",
        "cost_per_household_EUR": 1_500,
        "effectiveness": 0.60,
        "timeline_months": 24,
    },
    "LAND_RESTORATION": {
        "label": "Restauration accès foncier",
        "cost_per_household_EUR": 8_000,
        "effectiveness": 0.65,
        "timeline_months": 18,
    },
}


def assess_community_impact(entity: dict, domain: str, community_type: str = "INDIGENOUS") -> dict:
    """Évalue l'impact sur une communauté spécifique."""
    score = entity.get("composite_score", 0)
    community = COMMUNITY_TYPES.get(community_type, COMMUNITY_TYPES["URBAN_MARGINALIZED"])
    vulnerability = community.get("vulnerability_multiplier", 1.0)

    dimension_impacts = {}
    for dim, cfg in COMMUNITY_IMPACT_DIMENSIONS.items():
        raw_impact = score * cfg["weight"] * vulnerability
        dimension_impacts[dim] = {
            "label": cfg["label"],
            "impact_score": round(min(raw_impact, 100), 1),
            "severity": "GRAVE" if raw_impact >= 60 else "SIGNIFICATIF" if raw_impact >= 35 else "MODÉRÉ" if raw_impact >= 15 else "MINEUR",
        }

    est_households = int(score * 500 * vulnerability)
    est_population = est_households * 4

    sroi_total = 0
    sroi_breakdown = {}
    for indicator, cfg in SROI_INDICATORS.items():
        units = int(est_population * score / 10000)
        value_EUR = units * cfg["weight_EUR_per_unit"]
        sroi_breakdown[indicator] = {"units": units, "value_EUR": value_EUR}
        sroi_total += value_EUR

    overall_impact = (
        "DÉVASTATEUR" if score >= 80 and vulnerability >= 1.4
        else "GRAVE" if score >= 60
        else "SIGNIFICATIF" if score >= 40
        else "MODÉRÉ" if score >= 20
        else "MINEUR"
    )

    remediation_cost = est_households * COMMUNITY_BENEFIT_PROGRAMS["LIVELIHOOD_RESTORATION"]["cost_per_household_EUR"]

    return {
        "entity_id": entity.get("id"),
        "entity_name": entity.get("name"),
        "domain": domain,
        "community_type": community_type,
        "community_label": community["label"],
        "composite_score": score,
        "vulnerability_multiplier": vulnerability,
        "overall_impact": overall_impact,
        "affected_population": {
            "estimated_households": est_households,
            "estimated_persons": est_population,
        },
        "dimension_impacts": dimension_impacts,
        "sroi_analysis": {
            "total_social_value_at_risk_EUR": sroi_total,
            "breakdown": sroi_breakdown,
            "remediation_cost_EUR": remediation_cost,
            "roi_ratio": round(sroi_total / max(remediation_cost, 1), 2),
        },
        "protection_frameworks": community["protection_frameworks"],
        "consultation_standard": community["consultation_standard"],
        "clip_required": community_type == "INDIGENOUS",
        "recommended_programs": [
            prog for prog_key, prog in COMMUNITY_BENEFIT_PROGRAMS.items()
            if prog["effectiveness"] >= 0.70
        ][:2],
        "csddd_art8_triggered": score >= 20,
        "ungp_18_consultation_required": score >= 30,
    }


def generate_community_report(entities: list, domain: str) -> dict:
    """Rapport complet d'impact communautaire."""
    assessments = [assess_community_impact(e, domain, "INDIGENOUS") for e in entities]

    total_affected = sum(a["affected_population"]["estimated_persons"] for a in assessments)
    total_sroi = sum(a["sroi_analysis"]["total_social_value_at_risk_EUR"] for a in assessments)
    total_remediation = sum(a["sroi_analysis"]["remediation_cost_EUR"] for a in assessments)

    devastating = [a for a in assessments if a["overall_impact"] == "DÉVASTATEUR"]

    return {
        "report_type": "COMMUNITY_LOCAL_IMPACT",
        "report_id": f"CLI-{domain[:6].upper()}-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Community & Local Impact Agent v1.0",
        "domain": domain,
        "summary": {
            "entities_assessed": len(assessments),
            "devastating_impact_count": len(devastating),
            "total_affected_persons": total_affected,
            "total_social_value_at_risk_EUR": total_sroi,
            "total_remediation_cost_EUR": total_remediation,
            "portfolio_roi": round(total_sroi / max(total_remediation, 1), 2),
        },
        "entity_assessments": assessments,
        "ungp_compliance": {
            "ungp18_consultation": "REQUIS pour toutes entités score ≥30",
            "ungp29_grievance": "REQUIS — Mécanisme réclamation communautaire",
            "undrip_clip": "REQUIS pour communautés autochtones",
        },
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — COMMUNITY & LOCAL IMPACT AGENT")
    print("  Évaluation Impact Local & Communautaire + SROI")
    print("=" * 70)

    entities = [
        {"id": "SDR-001", "name": "Myanmar — Rohingyas 1M Apatrides", "composite_score": 94.40, "risk_level": "critique"},
        {"id": "SDR-004", "name": "Kuwait — Bidun 100K Sans Citoyenneté", "composite_score": 83.45, "risk_level": "critique"},
        {"id": "SDR-007", "name": "Ukraine — Réfugiés Post-Guerre", "composite_score": 26.55, "risk_level": "modéré"},
    ]

    report = generate_community_report(entities, "statelessness-document-rights")

    s = report["summary"]
    print(f"\n🏘️  RAPPORT IMPACT COMMUNAUTAIRE: {report['report_id']}")
    print(f"   Entités évaluées: {s['entities_assessed']}")
    print(f"   Impact dévastateur: {s['devastating_impact_count']}")
    print(f"   Personnes affectées (est.): {s['total_affected_persons']:,}")
    print(f"   Valeur sociale à risque: {s['total_social_value_at_risk_EUR']:,.0f}€")
    print(f"   Coût remédiation: {s['total_remediation_cost_EUR']:,.0f}€")
    print(f"   Ratio ROI social: x{s['portfolio_roi']:.1f}")

    for assessment in report["entity_assessments"][:2]:
        pop = assessment["affected_population"]
        sroi = assessment["sroi_analysis"]
        print(f"\n   📍 {assessment['entity_id']} — {assessment['entity_name'][:45]}")
        print(f"      Communauté: {assessment['community_label']}")
        print(f"      Impact global: {assessment['overall_impact']}")
        print(f"      Ménages affectés: {pop['estimated_households']:,}")
        print(f"      Personnes affectées: {pop['estimated_persons']:,}")
        print(f"      Valeur sociale à risque: {sroi['total_social_value_at_risk_EUR']:,.0f}€")
        print(f"      CLIP requis: {'✅ OUI' if assessment['clip_required'] else '❌ NON'}")

        print(f"      Dimensions impact:")
        for dim, imp in list(assessment["dimension_impacts"].items())[:3]:
            print(f"        • {imp['label']}: {imp['impact_score']:.0f} ({imp['severity']})")

    print(f"\n⚖️  CONFORMITÉ UNGP:")
    for norm, desc in report["ungp_compliance"].items():
        print(f"   • {norm}: {desc}")

    print(f"\n✅ Community & Local Impact Agent — Rapport généré avec succès")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
