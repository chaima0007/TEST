#!/usr/bin/env python3
"""
Stakeholder Mapping Agent — Caelum Partners CaelumSwarm™
Expert cartographie des parties prenantes selon ISO 26000 & UNGP.
Identifie, priorise et engage les parties prenantes affectées par domaine.
"""

import sys
from datetime import datetime, timezone

STAKEHOLDER_CATEGORIES = {
    "AFFECTED_COMMUNITIES": {
        "label": "Communautés affectées",
        "iso_26000_ref": "6.5 Droits de l'Homme",
        "ungp_ref": "UNGP 18 — Consultation significative",
        "engagement_priority": 1,
        "power_interest": "HIGH_INTEREST",
    },
    "CIVIL_SOCIETY": {
        "label": "Société civile & ONG",
        "iso_26000_ref": "6.2 Gouvernance",
        "ungp_ref": "UNGP 21 — Mécanismes de réclamation",
        "engagement_priority": 1,
        "power_interest": "HIGH_INTEREST",
    },
    "REGULATORS": {
        "label": "Régulateurs & Autorités",
        "iso_26000_ref": "6.6 Pratiques loyales",
        "ungp_ref": "UNGP 3 — Obligation de l'État",
        "engagement_priority": 2,
        "power_interest": "HIGH_POWER",
    },
    "INVESTORS": {
        "label": "Investisseurs & Actionnaires",
        "iso_26000_ref": "6.8 Développement communautaire",
        "ungp_ref": "UNGP 15 — Responsabilité entreprise",
        "engagement_priority": 2,
        "power_interest": "HIGH_POWER_INTEREST",
    },
    "EMPLOYEES": {
        "label": "Salariés & Syndicats",
        "iso_26000_ref": "6.4 Pratiques travail",
        "ungp_ref": "UNGP 16 — Politique de droits",
        "engagement_priority": 2,
        "power_interest": "MEDIUM_POWER_HIGH_INTEREST",
    },
    "SUPPLIERS": {
        "label": "Fournisseurs & Sous-traitants",
        "iso_26000_ref": "6.6 Pratiques loyales",
        "ungp_ref": "UNGP 17 — Diligence raisonnable",
        "engagement_priority": 2,
        "power_interest": "MEDIUM_POWER",
    },
    "MEDIA": {
        "label": "Médias & Journalistes",
        "iso_26000_ref": "6.2 Gouvernance",
        "ungp_ref": "UNGP 26 — Mécanismes non-judiciaires",
        "engagement_priority": 3,
        "power_interest": "MEDIUM_POWER",
    },
    "COMPETITORS": {
        "label": "Concurrents & Pairs sectoriels",
        "iso_26000_ref": "6.6 Pratiques loyales",
        "ungp_ref": "UNGP 15 — Responsabilité collective",
        "engagement_priority": 4,
        "power_interest": "LOW_INTEREST",
    },
}

DOMAIN_STAKEHOLDER_MAP = {
    "statelessness-document-rights": {
        "primary": ["AFFECTED_COMMUNITIES", "CIVIL_SOCIETY", "REGULATORS"],
        "secondary": ["INVESTORS", "MEDIA"],
        "key_ngos": ["UNHCR", "Open Society Foundations", "Tilburg Law School Statelessness"],
        "key_regulators": ["UNHCR", "Comités ONU (CRC, ICCPR)", "Ministères intérieur nationaux"],
        "community_voices": ["Représentants Rohingyas", "Association Bidun Kuwait", "Biharis Bangladesh"],
    },
    "offshore-tax-haven-rights": {
        "primary": ["REGULATORS", "CIVIL_SOCIETY", "INVESTORS"],
        "secondary": ["MEDIA", "AFFECTED_COMMUNITIES"],
        "key_ngos": ["Tax Justice Network", "Oxfam", "Global Financial Integrity"],
        "key_regulators": ["OCDE BEPS", "GAFI", "Commission EU DG TAXUD", "FMI"],
        "community_voices": ["Citoyens pays en développement", "Syndicats services publics"],
    },
    "deepfake-synthetic-media-rights": {
        "primary": ["CIVIL_SOCIETY", "REGULATORS", "AFFECTED_COMMUNITIES"],
        "secondary": ["MEDIA", "EMPLOYEES", "INVESTORS"],
        "key_ngos": ["Access Now", "Electronic Frontier Foundation", "Algorithm Watch"],
        "key_regulators": ["EDPB", "AI Office EU", "DSA Coordinateurs nationaux"],
        "community_voices": ["Victimes deepfakes", "Journalistes ciblés", "Activistes surveillance"],
    },
}

ENGAGEMENT_METHODS = {
    "CONSULTATION": {
        "label": "Consultation structurée",
        "format": "Réunions formelles avec ordre du jour",
        "frequency": "Trimestriel",
        "documentation": "Compte-rendu signé + suivi actions",
    },
    "DIALOGUE": {
        "label": "Dialogue multi-parties",
        "format": "Table ronde multi-parties prenantes",
        "frequency": "Semestriel",
        "documentation": "Rapport dialogue publié",
    },
    "PARTNERSHIP": {
        "label": "Partenariat stratégique",
        "format": "Convention de partenariat signée",
        "frequency": "Continu",
        "documentation": "Rapport annuel co-signé",
    },
    "SURVEY": {
        "label": "Enquête et sondage",
        "format": "Questionnaire anonymisé + analyse",
        "frequency": "Annuel",
        "documentation": "Rapport statistique interne",
    },
    "GRIEVANCE_MECHANISM": {
        "label": "Mécanisme de réclamation",
        "format": "Hotline + formulaire web sécurisé",
        "frequency": "Continu (réponse <30j)",
        "documentation": "Registre réclamations + suivi CSDDD Art.11",
    },
}


def map_stakeholders(domain: str, entity: dict) -> dict:
    """Cartographie les parties prenantes pour une entité donnée."""
    domain_config = DOMAIN_STAKEHOLDER_MAP.get(domain, {})
    primary_categories = domain_config.get("primary", list(STAKEHOLDER_CATEGORIES.keys())[:3])
    secondary_categories = domain_config.get("secondary", [])

    stakeholders = []
    for cat_key in primary_categories:
        cat = STAKEHOLDER_CATEGORIES.get(cat_key, {})
        stakeholders.append({
            "category": cat_key,
            "label": cat.get("label", cat_key),
            "priority": "PRIMARY",
            "engagement_priority": cat.get("engagement_priority", 3),
            "power_interest_matrix": cat.get("power_interest", "MEDIUM"),
            "iso_26000_ref": cat.get("iso_26000_ref", ""),
            "ungp_ref": cat.get("ungp_ref", ""),
            "recommended_method": "CONSULTATION" if "HIGH" in cat.get("power_interest", "") else "DIALOGUE",
        })

    for cat_key in secondary_categories:
        cat = STAKEHOLDER_CATEGORIES.get(cat_key, {})
        stakeholders.append({
            "category": cat_key,
            "label": cat.get("label", cat_key),
            "priority": "SECONDARY",
            "engagement_priority": cat.get("engagement_priority", 3),
            "power_interest_matrix": cat.get("power_interest", "LOW"),
            "iso_26000_ref": cat.get("iso_26000_ref", ""),
            "ungp_ref": cat.get("ungp_ref", ""),
            "recommended_method": "SURVEY",
        })

    stakeholders.sort(key=lambda x: x["engagement_priority"])

    score = entity.get("composite_score", 0)
    engagement_urgency = "IMMÉDIAT" if score >= 70 else "PRIORITAIRE" if score >= 50 else "PLANIFIÉ"

    return {
        "entity_id": entity.get("id"),
        "entity_name": entity.get("name"),
        "domain": domain,
        "composite_score": score,
        "engagement_urgency": engagement_urgency,
        "stakeholder_map": {
            "total": len(stakeholders),
            "primary_count": len(primary_categories),
            "secondary_count": len(secondary_categories),
            "stakeholders": stakeholders,
        },
        "specific_actors": {
            "key_ngos": domain_config.get("key_ngos", []),
            "key_regulators": domain_config.get("key_regulators", []),
            "community_voices": domain_config.get("community_voices", []),
        },
        "engagement_plan": _generate_engagement_plan(score, stakeholders),
    }


def _generate_engagement_plan(score: float, stakeholders: list) -> list:
    """Génère un plan d'engagement adapté au score de risque."""
    plan = []
    for sh in stakeholders[:3]:
        method_key = sh.get("recommended_method", "CONSULTATION")
        method = ENGAGEMENT_METHODS.get(method_key, {})
        plan.append({
            "stakeholder": sh["label"],
            "method": method.get("label", method_key),
            "format": method.get("format", ""),
            "frequency": method.get("frequency", ""),
            "timeline": "J+30" if sh["priority"] == "PRIMARY" else "J+60",
            "documentation": method.get("documentation", ""),
        })
    return plan


def generate_stakeholder_report(entities: list, domain: str) -> dict:
    """Rapport de cartographie parties prenantes pour un domaine."""
    maps = [map_stakeholders(domain, e) for e in entities]

    urgent = [m for m in maps if m["engagement_urgency"] == "IMMÉDIAT"]
    all_ngos = list({ngo for m in maps for ngo in m["specific_actors"]["key_ngos"]})
    all_regulators = list({reg for m in maps for reg in m["specific_actors"]["key_regulators"]})

    return {
        "report_type": "STAKEHOLDER_MAP",
        "report_id": f"SM-{domain[:6].upper()}-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Stakeholder Mapping Agent v1.0",
        "domain": domain,
        "summary": {
            "entities_mapped": len(maps),
            "requiring_immediate_engagement": len(urgent),
            "key_ngos": all_ngos,
            "key_regulators": all_regulators,
        },
        "entity_maps": maps,
        "csddd_compliance": {
            "art11_grievance_mechanism": "REQUIS — Mécanisme réclamation à établir",
            "art8_stakeholder_consultation": "REQUIS — Consultation documentée avant décision",
            "ungp18_meaningful_consultation": "REQUIS — Consultation significative populations affectées",
        },
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — STAKEHOLDER MAPPING AGENT")
    print("  Expert Cartographie Parties Prenantes ISO 26000 / UNGP")
    print("=" * 70)

    entities = [
        {"id": "OTH-001", "name": "Îles Caïmans — 0% Impôt", "composite_score": 91.60, "risk_level": "critique"},
        {"id": "OTH-002", "name": "Luxembourg — Rulings Fiscaux Secrets", "composite_score": 87.40, "risk_level": "critique"},
        {"id": "OTH-008", "name": "Danemark — OCDE 15%", "composite_score": 6.45, "risk_level": "faible"},
    ]

    report = generate_stakeholder_report(entities, "offshore-tax-haven-rights")

    print(f"\n🗺️  RAPPORT PARTIES PRENANTES: {report['report_id']}")
    print(f"   Domaine: {report['domain']}")
    print(f"   Entités cartographiées: {report['summary']['entities_mapped']}")
    print(f"   Engagement immédiat requis: {report['summary']['requiring_immediate_engagement']}")

    print(f"\n👥 ACTEURS CLÉS IDENTIFIÉS:")
    print(f"   ONG/OSC: {', '.join(report['summary']['key_ngos'][:3])}")
    print(f"   Régulateurs: {', '.join(report['summary']['key_regulators'][:3])}")

    for mapping in report["entity_maps"][:2]:
        print(f"\n   📍 {mapping['entity_id']} — {mapping['entity_name'][:45]}")
        print(f"      Score: {mapping['composite_score']} | Urgence: {mapping['engagement_urgency']}")
        print(f"      Parties prenantes: {mapping['stakeholder_map']['total']} identifiées")

        print(f"      Plan d'engagement:")
        for step in mapping["engagement_plan"][:2]:
            print(f"        • [{step['timeline']}] {step['stakeholder']} — {step['method']}")

    print(f"\n⚖️  OBLIGATIONS CSDDD:")
    for art, desc in report["csddd_compliance"].items():
        print(f"   • {art}: {desc}")

    print(f"\n✅ Stakeholder Mapping Agent — Cartographie générée avec succès")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
