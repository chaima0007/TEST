#!/usr/bin/env python3
"""
Compliance Audit Agent — Caelum Partners CaelumSwarm™
Auditeur expert conformité EU CSDDD 2024 / CSRD / UNGP
Analyse automatique des gaps de conformité par engine/domaine.
"""

import json
import os
import sys
from datetime import datetime, timezone

COMPLIANCE_FRAMEWORKS = {
    "EU_CSDDD_2024": {
        "name": "EU Corporate Sustainability Due Diligence Directive 2024",
        "articles": {
            "Art.8": "Identification et évaluation des impacts négatifs",
            "Art.9": "Prévention des impacts négatifs potentiels",
            "Art.10": "Cessation ou minimisation des impacts réels",
            "Art.11": "Établissement et maintien d'une procédure de réclamation",
            "Art.12": "Suivi de l'efficacité des mesures",
            "Art.13": "Communication publique",
        },
        "thresholds": {"critical": 60, "elevated": 40, "moderate": 20},
    },
    "UNGP_2011": {
        "name": "UN Guiding Principles on Business and Human Rights",
        "pillars": {
            "P1": "Protéger — Obligation des États",
            "P2": "Respecter — Responsabilité des entreprises",
            "P3": "Remédier — Accès aux voies de recours",
        },
    },
    "CSRD_2023": {
        "name": "Corporate Sustainability Reporting Directive",
        "standards": ["ESRS E1-E5", "ESRS S1-S4", "ESRS G1"],
    },
    "OCDE_MNE": {
        "name": "Lignes directrices OCDE pour les entreprises multinationales 2023",
        "chapters": ["II: Politiques générales", "IV: Droits de l'homme", "V: Emploi"],
    },
}

RISK_MATRIX = {
    "critique": {
        "score_range": (60, 100),
        "urgency": "IMMÉDIAT",
        "action_delay_days": 30,
        "escalation": "Conseil d'administration + DG",
        "csrd_disclosure": "Obligatoire — Impact matériel significatif",
        "csddd_obligation": "Art.10 — Cessation immédiate requise",
    },
    "élevé": {
        "score_range": (40, 59),
        "urgency": "PRIORITAIRE",
        "action_delay_days": 90,
        "escalation": "Directeur RSE + Comité de risques",
        "csrd_disclosure": "Obligatoire — Risque financier matériel",
        "csddd_obligation": "Art.9 — Plan de prévention sous 90 jours",
    },
    "modéré": {
        "score_range": (20, 39),
        "urgency": "PLANIFIÉ",
        "action_delay_days": 180,
        "escalation": "Équipe conformité",
        "csrd_disclosure": "Recommandé — Surveillance renforcée",
        "csddd_obligation": "Art.8 — Réévaluation annuelle",
    },
    "faible": {
        "score_range": (0, 19),
        "urgency": "SURVEILLANCE",
        "action_delay_days": 365,
        "escalation": "Équipe conformité (routine)",
        "csrd_disclosure": "Optionnel — Mention positive possible",
        "csddd_obligation": "Art.12 — Suivi standard",
    },
}

SECTOR_PROFILES = {
    "tech_digital": {
        "label": "Technologie & Numérique",
        "high_risk_domains": ["deepfake-synthetic-media", "ai-surveillance", "dark-web-cybercrime"],
        "key_regulation": "AI Act 2024 + DSGVO/RGPD",
    },
    "finance_banking": {
        "label": "Finance & Banque",
        "high_risk_domains": ["offshore-tax-haven", "financial-exclusion", "predatory-lending"],
        "key_regulation": "SFDR + EU Taxonomy + AMLD6",
    },
    "extractive_industry": {
        "label": "Industries extractives",
        "high_risk_domains": ["land-grabbing", "environmental-pollution", "indigenous-rights"],
        "key_regulation": "EITI + CSDDD Annex I (high-risk sectors)",
    },
    "supply_chain": {
        "label": "Chaîne d'approvisionnement",
        "high_risk_domains": ["forced-labor", "child-labor", "living-wage"],
        "key_regulation": "CSDDD Art.8 + ILO Core Conventions",
    },
    "pharma_health": {
        "label": "Pharma & Santé",
        "high_risk_domains": ["pharmaceutical-access", "vaccine-equity", "disability-rights"],
        "key_regulation": "WHO Framework + TRIPS Agreement",
    },
}


def audit_entity(entity: dict, domain_slug: str) -> dict:
    """Audit complet d'une entité selon les frameworks de conformité."""
    score = entity.get("composite_score", 0)
    risk = entity.get("risk_level", "faible")
    matrix = RISK_MATRIX.get(risk, RISK_MATRIX["faible"])

    gap_analysis = []
    for article, description in COMPLIANCE_FRAMEWORKS["EU_CSDDD_2024"]["articles"].items():
        severity = "CONFORME" if score < 20 else "NON-CONFORME" if score >= 60 else "PARTIEL"
        gap_analysis.append({"article": article, "description": description, "status": severity})

    action_plan = []
    if score >= 60:
        action_plan = [
            f"J+0 — Notification immédiate {matrix['escalation']}",
            f"J+7 — Audit terrain indépendant commandé",
            f"J+14 — Plan de cessation/remédiation soumis au CA",
            f"J+30 — Rapport d'avancement CSDDD Art.13",
            f"J+90 — Vérification tierce partie indépendante",
        ]
    elif score >= 40:
        action_plan = [
            f"J+7 — Réunion {matrix['escalation']}",
            f"J+30 — Plan de prévention formalisé",
            f"J+60 — KPIs de suivi définis et publiés",
            f"J+90 — Premier rapport d'avancement",
        ]
    elif score >= 20:
        action_plan = [
            f"J+30 — Évaluation approfondie planifiée",
            f"J+90 — Mise à jour politique interne",
            f"J+180 — Revue annuelle conformité",
        ]
    else:
        action_plan = [
            f"J+365 — Revue de surveillance standard",
            "Documenter les bonnes pratiques pour partage sectoriel",
        ]

    return {
        "entity_id": entity.get("id"),
        "entity_name": entity.get("name"),
        "domain": domain_slug,
        "audit_date": datetime.now(timezone.utc).isoformat(),
        "composite_score": score,
        "risk_level": risk,
        "urgency": matrix["urgency"],
        "action_required_within_days": matrix["action_delay_days"],
        "escalation_level": matrix["escalation"],
        "csddd_obligation": matrix["csddd_obligation"],
        "csrd_disclosure_required": matrix["csrd_disclosure"],
        "gap_analysis_csddd": gap_analysis,
        "action_plan": action_plan,
        "frameworks_triggered": [
            "EU CSDDD 2024" if score >= 20 else None,
            "UNGP 2011" if score >= 40 else None,
            "CSRD 2023" if score >= 60 else None,
        ],
    }


def generate_compliance_report(entities: list, domain_slug: str, metadata: dict) -> dict:
    """Génère un rapport de conformité complet pour un domaine."""
    audits = [audit_entity(e, domain_slug) for e in entities]

    critiques = [a for a in audits if a["risk_level"] == "critique"]
    eleves = [a for a in audits if a["risk_level"] == "élevé"]
    moderes = [a for a in audits if a["risk_level"] == "modéré"]
    faibles = [a for a in audits if a["risk_level"] == "faible"]

    avg_score = sum(a["composite_score"] for a in audits) / len(audits) if audits else 0

    overall_compliance_status = (
        "NON-CONFORME CRITIQUE" if len(critiques) >= 3
        else "NON-CONFORME ÉLEVÉ" if len(critiques) >= 1 or len(eleves) >= 3
        else "PARTIELLEMENT CONFORME" if len(eleves) >= 1
        else "CONFORME AVEC RÉSERVES" if len(moderes) >= 1
        else "CONFORME"
    )

    immediate_actions = [
        action
        for audit in critiques
        for action in audit["action_plan"][:2]
    ]

    return {
        "report_type": "COMPLIANCE_AUDIT",
        "report_id": f"CA-{domain_slug.upper()[:8]}-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Compliance Audit Agent v1.0",
        "domain": domain_slug,
        "metadata": metadata,
        "executive_summary": {
            "overall_status": overall_compliance_status,
            "avg_composite_score": round(avg_score, 2),
            "total_entities": len(audits),
            "entities_requiring_immediate_action": len(critiques),
            "entities_requiring_priority_action": len(eleves),
            "frameworks_triggered": list({
                fw for a in audits for fw in a.get("frameworks_triggered", []) if fw
            }),
        },
        "risk_distribution": {
            "critique": len(critiques),
            "élevé": len(eleves),
            "modéré": len(moderes),
            "faible": len(faibles),
        },
        "immediate_actions_required": immediate_actions,
        "entity_audits": audits,
        "regulatory_calendar": {
            "CSDDD_application_date": "2027-07-26",
            "CSRD_reporting_start": "2025-01-01",
            "next_review_date": datetime.now(timezone.utc).strftime("%Y-%m-01"),
        },
        "disclaimer": (
            "Ce rapport est généré automatiquement par CaelumSwarm™. "
            "Il constitue une aide à la décision et ne remplace pas l'avis juridique d'un expert qualifié."
        ),
    }


def run_demo():
    """Démonstration avec des données Wave 193."""
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — COMPLIANCE AUDIT AGENT")
    print("  Auditeur Expert Conformité EU CSDDD 2024 / CSRD / UNGP")
    print("=" * 70)

    demo_entities = [
        {"id": "SDR-001", "name": "Myanmar — Rohingyas 1M Apatrides", "composite_score": 94.40, "risk_level": "critique"},
        {"id": "SDR-002", "name": "Côte d'Ivoire — 700K Apatrides Post-Conflit", "composite_score": 87.65, "risk_level": "critique"},
        {"id": "SDR-003", "name": "Bangladesh — Bihari 300K Apatrides", "composite_score": 87.00, "risk_level": "critique"},
        {"id": "SDR-004", "name": "Kuwait — Bidun 100K Sans Citoyenneté", "composite_score": 83.45, "risk_level": "critique"},
        {"id": "SDR-005", "name": "République Dominicaine — Dénationalisation", "composite_score": 57.50, "risk_level": "élevé"},
        {"id": "SDR-006", "name": "Thaïlande — Peuples Montagnards", "composite_score": 53.45, "risk_level": "élevé"},
        {"id": "SDR-007", "name": "Ukraine — Réfugiés Post-Guerre", "composite_score": 26.55, "risk_level": "modéré"},
        {"id": "SDR-008", "name": "Lettonie — Résolution Apatridie Soviet", "composite_score": 8.30, "risk_level": "faible"},
    ]

    metadata = {"wave": 193, "domain_full": "statelessness-document-rights-engine"}
    report = generate_compliance_report(demo_entities, "statelessness-document-rights", metadata)

    print(f"\n📋 RAPPORT: {report['report_id']}")
    print(f"   Domaine: {report['domain']}")
    print(f"   Statut global: {report['executive_summary']['overall_status']}")
    print(f"   Score moyen: {report['executive_summary']['avg_composite_score']}")
    print(f"   Entités nécessitant action immédiate: {report['executive_summary']['entities_requiring_immediate_action']}")
    print(f"   Frameworks déclenchés: {', '.join(report['executive_summary']['frameworks_triggered'])}")

    print(f"\n⚡ ACTIONS IMMÉDIATES REQUISES:")
    for action in report["immediate_actions_required"][:4]:
        print(f"   • {action}")

    print(f"\n📊 DISTRIBUTION RISQUES:")
    for level, count in report["risk_distribution"].items():
        bar = "█" * count
        print(f"   {level:10} {bar} ({count})")

    print(f"\n📅 CALENDRIER RÉGLEMENTAIRE:")
    for k, v in report["regulatory_calendar"].items():
        print(f"   {k}: {v}")

    print(f"\n✅ Compliance Audit Agent — Rapport généré avec succès")
    print(f"   {len(demo_entities)} entités auditées | {report['executive_summary']['entities_requiring_immediate_action']} actions immédiates")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
