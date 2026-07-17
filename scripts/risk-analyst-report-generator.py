#!/usr/bin/env python3
"""
Risk Analyst & Report Generator Agent — Caelum Partners CaelumSwarm™
Analyse de risques multi-dimensionnelle + génération automatique de rapports
PDF-ready (JSON structuré pour rendu) selon standards EU CSDDD / CSRD.
"""

import json
import math
import sys
from datetime import datetime, timezone

RISK_DIMENSIONS = {
    "likelihood": {"label": "Probabilité d'occurrence", "weight": 0.30},
    "severity": {"label": "Sévérité de l'impact", "weight": 0.35},
    "reversibility": {"label": "Irréversibilité", "weight": 0.20},
    "breadth": {"label": "Étendue géographique/population", "weight": 0.15},
}

RISK_CATEGORIES = {
    "droits_civils": ["statelessness", "documentation", "identity"],
    "droits_economiques": ["tax-haven", "financial-exclusion", "labor-exploitation"],
    "droits_numeriques": ["deepfake", "surveillance", "cybercrime", "data-rights"],
    "droits_environnementaux": ["land-grabbing", "pollution", "climate-migration"],
    "droits_sociaux": ["healthcare", "education", "housing", "food"],
}

MATERIALITY_THRESHOLDS = {
    "financial_material": 40,
    "impact_material": 30,
    "double_materiality": 55,
}

REPORT_SECTIONS = [
    "executive_summary",
    "risk_matrix",
    "entity_profiles",
    "trend_analysis",
    "recommendations",
    "regulatory_mapping",
    "kpi_dashboard",
    "appendices",
]


def calculate_risk_score(entity: dict) -> dict:
    """Calcule un score de risque multi-dimensionnel."""
    base = entity.get("composite_score", 0)
    subscores = {k: v for k, v in entity.items() if k.endswith("_score") and k != "composite_score"}

    variance = 0
    if subscores:
        vals = list(subscores.values())
        mean = sum(vals) / len(vals)
        variance = math.sqrt(sum((v - mean) ** 2 for v in vals) / len(vals))

    concentration_risk = min(variance / 20, 1.0)

    likelihood = min(base / 100, 1.0)
    severity = min((base + variance * 0.5) / 100, 1.0)
    reversibility = min(base / 120, 1.0)
    breadth = min((base * 0.8) / 100, 1.0)

    weighted_score = (
        likelihood * RISK_DIMENSIONS["likelihood"]["weight"]
        + severity * RISK_DIMENSIONS["severity"]["weight"]
        + reversibility * RISK_DIMENSIONS["reversibility"]["weight"]
        + breadth * RISK_DIMENSIONS["breadth"]["weight"]
    ) * 100

    financial_material = base >= MATERIALITY_THRESHOLDS["financial_material"]
    impact_material = base >= MATERIALITY_THRESHOLDS["impact_material"]
    double_material = base >= MATERIALITY_THRESHOLDS["double_materiality"]

    return {
        "base_score": base,
        "multi_dim_score": round(weighted_score, 2),
        "variance": round(variance, 2),
        "concentration_risk": round(concentration_risk, 3),
        "dimension_scores": {
            "likelihood": round(likelihood * 100, 1),
            "severity": round(severity * 100, 1),
            "reversibility": round(reversibility * 100, 1),
            "breadth": round(breadth * 100, 1),
        },
        "materiality": {
            "financial_material": financial_material,
            "impact_material": impact_material,
            "double_material": double_material,
        },
    }


def detect_risk_category(domain_slug: str) -> str:
    """Détecte la catégorie de risque droits humains pour un domaine."""
    domain_lower = domain_slug.lower()
    for category, keywords in RISK_CATEGORIES.items():
        if any(kw in domain_lower for kw in keywords):
            return category
    return "droits_civils"


def generate_kpi_dashboard(entities: list, domain: str) -> dict:
    """Génère un tableau de bord KPIs pour le suivi."""
    scores = [e.get("composite_score", 0) for e in entities]
    risk_levels = [e.get("risk_level", "faible") for e in entities]

    return {
        "kpis": {
            "avg_score": round(sum(scores) / len(scores), 2) if scores else 0,
            "max_score": max(scores) if scores else 0,
            "min_score": min(scores) if scores else 0,
            "median_score": round(sorted(scores)[len(scores) // 2], 2) if scores else 0,
            "pct_critical": round(risk_levels.count("critique") / len(risk_levels) * 100, 1) if risk_levels else 0,
            "pct_elevated": round(risk_levels.count("élevé") / len(risk_levels) * 100, 1) if risk_levels else 0,
            "entities_double_material": sum(
                1 for s in scores if s >= MATERIALITY_THRESHOLDS["double_materiality"]
            ),
        },
        "traffic_light": (
            "RED" if risk_levels.count("critique") >= 3
            else "ORANGE" if risk_levels.count("critique") >= 1 or risk_levels.count("élevé") >= 3
            else "YELLOW" if risk_levels.count("élevé") >= 1
            else "GREEN"
        ),
        "trend_indicator": "STABLE",
        "next_review": "Q2 2026",
    }


def generate_report(entities: list, domain: str, wave: int = 193) -> dict:
    """Génère le rapport complet d'analyse de risques."""
    risk_analyses = [
        {"entity": e, "risk_analysis": calculate_risk_score(e)}
        for e in entities
    ]

    kpi_dash = generate_kpi_dashboard(entities, domain)
    risk_category = detect_risk_category(domain)

    high_priority = [
        r for r in risk_analyses
        if r["risk_analysis"]["base_score"] >= 60
    ]

    recommendations = []
    for item in high_priority[:3]:
        e = item["entity"]
        recommendations.append({
            "priority": "CRITIQUE",
            "entity": e.get("name", ""),
            "action": f"Engager un audit de terrain indépendant pour {e.get('id', '')}",
            "framework": "CSDDD Art.10",
            "deadline_days": 30,
        })

    for item in [r for r in risk_analyses if 40 <= r["risk_analysis"]["base_score"] < 60][:2]:
        e = item["entity"]
        recommendations.append({
            "priority": "ÉLEVÉ",
            "entity": e.get("name", ""),
            "action": f"Développer un plan de prévention formalisé pour {e.get('id', '')}",
            "framework": "CSDDD Art.9",
            "deadline_days": 90,
        })

    recommendations.append({
        "priority": "SYSTÉMIQUE",
        "entity": "TOUS",
        "action": f"Intégrer le domaine '{domain}' dans le rapport CSRD annuel — section ESRS S4",
        "framework": "CSRD 2023",
        "deadline_days": 60,
    })

    return {
        "report_type": "RISK_ANALYSIS",
        "report_id": f"RA-{domain.upper()[:6]}-{datetime.now().strftime('%Y%m%d-%H%M')}",
        "wave": wave,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Risk Analyst Agent v1.0",
        "domain": domain,
        "risk_category": risk_category,
        "executive_summary": {
            "kpi_dashboard": kpi_dash,
            "entities_analyzed": len(entities),
            "high_priority_count": len(high_priority),
            "double_materiality_count": kpi_dash["kpis"]["entities_double_material"],
            "overall_traffic_light": kpi_dash["traffic_light"],
        },
        "risk_matrix": risk_analyses,
        "recommendations": recommendations,
        "regulatory_mapping": {
            "CSDDD_2024": {
                "applicable": True,
                "articles_triggered": ["Art.8", "Art.9", "Art.10", "Art.13"] if kpi_dash["kpis"]["avg_score"] >= 40 else ["Art.8", "Art.12"],
                "compliance_deadline": "2027-07-26",
            },
            "CSRD_2023": {
                "applicable": kpi_dash["kpis"]["entities_double_material"] > 0,
                "esrs_section": "ESRS S4 — Consumers and end-users",
                "reporting_start": "2025-01-01",
            },
            "UNGP_2011": {
                "applicable": True,
                "pillar_triggered": "P2 — Respect" if kpi_dash["kpis"]["avg_score"] >= 20 else "P3 — Remedy",
            },
        },
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — RISK ANALYST & REPORT GENERATOR AGENT")
    print("  Analyse Multi-Dimensionnelle + Génération Automatique Rapports")
    print("=" * 70)

    entities = [
        {"id": "OTH-001", "name": "Îles Caïmans — 0% Impôt", "composite_score": 91.60, "risk_level": "critique", "tax_avoidance_scale_score": 94, "public_service_underfunding_score": 91, "inequality_amplification_score": 89, "corporate_transparency_deficit_score": 92},
        {"id": "OTH-002", "name": "Luxembourg — Rulings Fiscaux Secrets", "composite_score": 87.40, "risk_level": "critique", "tax_avoidance_scale_score": 88, "public_service_underfunding_score": 85, "inequality_amplification_score": 87, "corporate_transparency_deficit_score": 90},
        {"id": "OTH-003", "name": "Îles Vierges Britanniques", "composite_score": 91.15, "risk_level": "critique", "tax_avoidance_scale_score": 92, "public_service_underfunding_score": 88, "inequality_amplification_score": 91, "corporate_transparency_deficit_score": 94},
        {"id": "OTH-004", "name": "Suisse — Secret Bancaire", "composite_score": 82.90, "risk_level": "critique", "tax_avoidance_scale_score": 85, "public_service_underfunding_score": 78, "inequality_amplification_score": 86, "corporate_transparency_deficit_score": 82},
        {"id": "OTH-005", "name": "Dubai/EAU — Golden Visa", "composite_score": 58.55, "risk_level": "élevé", "tax_avoidance_scale_score": 58, "public_service_underfunding_score": 55, "inequality_amplification_score": 60, "corporate_transparency_deficit_score": 62},
        {"id": "OTH-006", "name": "Singapour — Hub Asie", "composite_score": 53.40, "risk_level": "élevé", "tax_avoidance_scale_score": 55, "public_service_underfunding_score": 48, "inequality_amplification_score": 58, "corporate_transparency_deficit_score": 52},
        {"id": "OTH-007", "name": "Irlande — Taux 12.5%", "composite_score": 26.65, "risk_level": "modéré", "tax_avoidance_scale_score": 30, "public_service_underfunding_score": 25, "inequality_amplification_score": 28, "corporate_transparency_deficit_score": 22},
        {"id": "OTH-008", "name": "Danemark — OCDE 15%", "composite_score": 6.45, "risk_level": "faible", "tax_avoidance_scale_score": 7, "public_service_underfunding_score": 5, "inequality_amplification_score": 6, "corporate_transparency_deficit_score": 8},
    ]

    report = generate_report(entities, "offshore-tax-haven-rights", wave=193)

    kpi = report["executive_summary"]["kpi_dashboard"]["kpis"]
    print(f"\n📊 RAPPORT: {report['report_id']}")
    print(f"   Domaine: {report['domain']} | Catégorie: {report['risk_category']}")
    print(f"   Feu de signalisation: {report['executive_summary']['overall_traffic_light']}")
    print(f"   Score moyen: {kpi['avg_score']} | Max: {kpi['max_score']} | Médiane: {kpi['median_score']}")
    print(f"   Double matérialité CSRD: {kpi['entities_double_material']}/{len(entities)} entités")

    print(f"\n⚡ TOP RECOMMANDATIONS:")
    for i, rec in enumerate(report["recommendations"][:4], 1):
        print(f"   {i}. [{rec['priority']}] {rec['action'][:65]}...")
        print(f"      Cadre: {rec['framework']} | Délai: {rec['deadline_days']}j")

    print(f"\n📐 ANALYSE MULTI-DIMENSIONNELLE (Top entité critique):")
    top = report["risk_matrix"][0]["risk_analysis"]
    for dim, score in top["dimension_scores"].items():
        bar = "█" * int(score / 10)
        print(f"   {dim:15} {bar} {score:.0f}")

    print(f"\n📋 MAPPING RÉGLEMENTAIRE:")
    for framework, details in report["regulatory_mapping"].items():
        print(f"   {framework}: {'APPLICABLE' if details['applicable'] else 'non applicable'}")

    print(f"\n✅ Risk Analyst Agent — Rapport généré avec succès")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
