#!/usr/bin/env python3
"""
Corrective Action Plan Agent — Caelum Partners CaelumSwarm™
Génère des plans d'action correctifs automatiques selon CSDDD Art.9 & Art.10.
Priorisé, chiffré, avec KPIs et propriétaires assignés.
"""

import sys
from datetime import datetime, timedelta, timezone

ACTION_PLAN_TEMPLATES = {
    "critique": {
        "horizon_days": 90,
        "phases": [
            {
                "phase": "URGENCE (J0–J30)",
                "actions": [
                    "Notification immédiate Conseil d'Administration et Direction Générale",
                    "Suspension ou restriction des opérations/contrats concernés",
                    "Mission d'audit terrain indépendant mandatée (cabinet tier)",
                    "Engagement direct avec communautés affectées (UNGP 18)",
                    "Communication de crise préparée (media + régulateurs)",
                ],
                "kpis": ["Rapport audit terrain J+30", "Réponse écrite DG J+7"],
                "owner": "DG + Directeur RSE",
            },
            {
                "phase": "CORRECTION (J30–J60)",
                "actions": [
                    "Plan de cessation de l'impact formalisé et soumis à validation",
                    "Mécanisme de réparation pour victimes établi (CSDDD Art.11)",
                    "Contrats avec fournisseurs révisés — clause droits humains renforcée",
                    "Formation équipes opérationnelles sur terrain",
                ],
                "kpis": ["Plan cessation validé J+45", "Mécanisme réparation opérationnel J+60"],
                "owner": "Directeur RSE + Juridique + Achats",
            },
            {
                "phase": "PRÉVENTION SYSTÉMIQUE (J60–J90)",
                "actions": [
                    "Révision politique droits humains groupe entière",
                    "Due diligence approfondie sur tous fournisseurs T1 du segment",
                    "KPIs de suivi intégrés au tableau de bord RSE trimestriel",
                    "Rapport public CSDDD Art.13 mis à jour",
                    "Mécanisme d'alerte précoce déployé (CaelumSwarm™ alertes)",
                ],
                "kpis": ["Politique DH révisée J+75", "Rapport public J+90", "Tous KPIs actifs J+90"],
                "owner": "DG + Conseil d'Administration",
            },
        ],
        "budget_range_EUR": (50_000, 250_000),
        "csddd_articles": ["Art.9", "Art.10", "Art.11", "Art.13"],
    },
    "élevé": {
        "horizon_days": 180,
        "phases": [
            {
                "phase": "ÉVALUATION (J0–J45)",
                "actions": [
                    "Évaluation détaillée de l'impact — rapport interne",
                    "Consultation parties prenantes affectées (entretiens structurés)",
                    "Analyse causes racines de la défaillance",
                    "Cartographie fournisseurs segment à risque",
                ],
                "kpis": ["Rapport évaluation J+45", "Consultation documentée J+30"],
                "owner": "Directeur RSE + Équipe conformité",
            },
            {
                "phase": "PLAN PRÉVENTION (J45–J120)",
                "actions": [
                    "Plan de prévention formalisé soumis à DG",
                    "Révision contrats fournisseurs concernés",
                    "Formation équipes achats et opérations",
                    "Indicateurs de performance définis et publiés",
                ],
                "kpis": ["Plan prévention approuvé J+60", "Contrats révisés J+90"],
                "owner": "Achats + RSE",
            },
            {
                "phase": "SUIVI & REPORTING (J120–J180)",
                "actions": [
                    "Premier rapport d'avancement publié (CSDDD Art.13)",
                    "Audit de vérification tier indépendant",
                    "Mise à jour scoring CaelumSwarm™ selon évolution",
                ],
                "kpis": ["Rapport avancement J+150", "Scoring mis à jour J+180"],
                "owner": "RSE + Communication",
            },
        ],
        "budget_range_EUR": (15_000, 80_000),
        "csddd_articles": ["Art.8", "Art.9", "Art.12"],
    },
    "modéré": {
        "horizon_days": 365,
        "phases": [
            {
                "phase": "SURVEILLANCE RENFORCÉE (J0–J90)",
                "actions": [
                    "Revue annuelle due diligence anticipée",
                    "Ajout indicateurs de suivi au dashboard RSE",
                    "Formation de sensibilisation équipes concernées",
                ],
                "kpis": ["Indicateurs actifs J+30", "Formation complétée J+90"],
                "owner": "Équipe conformité",
            },
            {
                "phase": "AMÉLIORATION CONTINUE (J90–J365)",
                "actions": [
                    "Benchmarking pratiques secteur",
                    "Intégration dans rapport CSRD annuel",
                    "Révision politique si dégradation score",
                ],
                "kpis": ["Section CSRD complétée", "Benchmarking documenté"],
                "owner": "RSE + Direction",
            },
        ],
        "budget_range_EUR": (5_000, 25_000),
        "csddd_articles": ["Art.8", "Art.12"],
    },
    "faible": {
        "horizon_days": 365,
        "phases": [
            {
                "phase": "SURVEILLANCE STANDARD (Annuel)",
                "actions": [
                    "Revue annuelle de routine",
                    "Mentionner positivement dans rapport CSRD",
                    "Documenter les bonnes pratiques internes",
                ],
                "kpis": ["Revue annuelle complétée", "CSRD section mise à jour"],
                "owner": "Équipe conformité (routine)",
            },
        ],
        "budget_range_EUR": (1_000, 5_000),
        "csddd_articles": ["Art.12"],
    },
}

REMEDIATION_TYPES = {
    "CESSATION": "Arrêt immédiat de l'activité causant l'impact",
    "MITIGATION": "Réduction de l'impact dans les opérations en cours",
    "REMEDIATION": "Réparation des dommages causés aux victimes",
    "RESTORATION": "Restauration à l'état antérieur (si possible)",
    "COMPENSATION": "Compensation financière aux victimes (en dernier recours)",
}

KPI_LIBRARY = {
    "OUTCOME": [
        "Nombre de victimes ayant accès au mécanisme de réparation",
        "% réduction du score composite en 6 mois",
        "Nombre de réclamations traitées dans les délais CSDDD",
    ],
    "PROCESS": [
        "% fournisseurs audités selon nouveau protocole",
        "% équipes formées sur les risques identifiés",
        "Délai moyen de traitement réclamation (objectif <30j)",
    ],
    "IMPACT": [
        "Réduction mesurable de l'impact négatif (méthodologie SROI)",
        "Amélioration score droits humains entités concernées",
        "Reconnaissance externe (rating ESG, certification B-Corp)",
    ],
}


def generate_corrective_plan(entity: dict, domain: str, wave: int = 193) -> dict:
    """Génère un plan d'action correctif complet pour une entité."""
    risk_level = entity.get("risk_level", "faible")
    score = entity.get("composite_score", 0)
    template = ACTION_PLAN_TEMPLATES.get(risk_level, ACTION_PLAN_TEMPLATES["faible"])

    start_date = datetime.now(timezone.utc)
    end_date = start_date + timedelta(days=template["horizon_days"])

    remediation_type = (
        "CESSATION" if score >= 85
        else "MITIGATION" if score >= 65
        else "REMEDIATION" if score >= 40
        else "COMPENSATION" if score >= 20
        else "RESTORATION"
    )

    selected_kpis = {
        "outcome": KPI_LIBRARY["OUTCOME"][:2],
        "process": KPI_LIBRARY["PROCESS"][:2],
        "impact": KPI_LIBRARY["IMPACT"][:1],
    }

    budget_low, budget_high = template["budget_range_EUR"]
    budget_estimate = budget_low + (budget_high - budget_low) * (score / 100)

    return {
        "plan_id": f"CAP-{entity.get('id', 'UNK')}-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": start_date.isoformat(),
        "generated_by": "CaelumSwarm™ Corrective Action Plan Agent v1.0",
        "wave": wave,
        "entity": {
            "id": entity.get("id"),
            "name": entity.get("name"),
            "domain": domain,
            "composite_score": score,
            "risk_level": risk_level,
        },
        "plan_overview": {
            "horizon_days": template["horizon_days"],
            "start_date": start_date.strftime("%Y-%m-%d"),
            "target_completion": end_date.strftime("%Y-%m-%d"),
            "remediation_type": remediation_type,
            "remediation_description": REMEDIATION_TYPES[remediation_type],
            "csddd_articles": template["csddd_articles"],
            "budget_estimate_EUR": round(budget_estimate, -3),
        },
        "phases": template["phases"],
        "kpis": selected_kpis,
        "governance": {
            "steering_committee": "Comité de pilotage CSDDD — réunion mensuelle",
            "executive_sponsor": "Directeur Général",
            "reporting_frequency": "Mensuel vers DG, Trimestriel vers CA",
            "external_verification": f"Audit indépendant J+{template['horizon_days']//2}",
        },
        "success_criteria": {
            "minimum": f"Score composite réduit de ≥15 pts en {template['horizon_days']}j",
            "target": f"Score composite < {max(score - 20, 20):.0f} sous {template['horizon_days']}j",
            "stretch": f"Score composite < {max(score - 35, 10):.0f} sous {template['horizon_days']}j",
        },
    }


def generate_portfolio_action_plan(entities: list, domain: str) -> dict:
    """Génère un plan d'action pour l'ensemble des entités d'un domaine."""
    plans = [generate_corrective_plan(e, domain) for e in entities]

    critical_plans = [p for p in plans if p["entity"]["risk_level"] == "critique"]
    total_budget = sum(p["plan_overview"]["budget_estimate_EUR"] for p in plans)

    quick_wins = [
        p for p in plans
        if p["entity"]["composite_score"] >= 40 and p["entity"]["composite_score"] < 65
    ]

    return {
        "portfolio_plan_id": f"PAP-{domain[:6].upper()}-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Corrective Action Plan Agent v1.0",
        "domain": domain,
        "summary": {
            "total_entities": len(plans),
            "critical_requiring_immediate_action": len(critical_plans),
            "quick_wins_available": len(quick_wins),
            "total_budget_estimate_EUR": total_budget,
            "portfolio_horizon_months": 18,
        },
        "immediate_priorities": critical_plans[:3],
        "quick_wins": quick_wins[:2],
        "full_plans": plans,
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — CORRECTIVE ACTION PLAN AGENT")
    print("  Plans d'Action Correctifs CSDDD Art.9 & Art.10")
    print("=" * 70)

    entities = [
        {"id": "SDR-001", "name": "Myanmar — Rohingyas 1M Apatrides, Génocide Documentaire", "composite_score": 94.40, "risk_level": "critique"},
        {"id": "SDR-005", "name": "République Dominicaine — Dénationalisation Haïtiens", "composite_score": 57.50, "risk_level": "élevé"},
        {"id": "SDR-007", "name": "Ukraine — Réfugiés Post-Guerre, Enregistrement Partiel", "composite_score": 26.55, "risk_level": "modéré"},
        {"id": "SDR-008", "name": "Lettonie — Résolution Apatridie Soviet", "composite_score": 8.30, "risk_level": "faible"},
    ]

    portfolio = generate_portfolio_action_plan(entities, "statelessness-document-rights")

    print(f"\n📋 PORTFOLIO PLANS CORRECTIFS: {portfolio['portfolio_plan_id']}")
    print(f"   Entités: {portfolio['summary']['total_entities']}")
    print(f"   Actions immédiates critiques: {portfolio['summary']['critical_requiring_immediate_action']}")
    print(f"   Quick wins disponibles: {portfolio['summary']['quick_wins_available']}")
    print(f"   Budget total estimé: {portfolio['summary']['total_budget_estimate_EUR']:,.0f}€")

    print(f"\n⚡ PLANS PRIORITAIRES:")
    for plan in portfolio["immediate_priorities"][:2]:
        e = plan["entity"]
        overview = plan["plan_overview"]
        print(f"\n   🔴 {e['id']} — {e['name'][:50]}")
        print(f"      Score: {e['composite_score']} | Niveau: {e['risk_level']}")
        print(f"      Type remédiation: {overview['remediation_type']} — {overview['remediation_description']}")
        print(f"      Horizon: {overview['horizon_days']}j | Budget: {overview['budget_estimate_EUR']:,.0f}€")
        print(f"      Articles CSDDD: {', '.join(overview['csddd_articles'])}")

        print(f"      Phases:")
        for phase in plan["phases"][:2]:
            print(f"        • {phase['phase']}")
            print(f"          Actions: {len(phase['actions'])} | Owner: {phase['owner']}")
            print(f"          KPIs: {phase['kpis'][0][:55]}...")

        print(f"      Objectif: {plan['success_criteria']['target']}")

    print(f"\n✅ Corrective Action Plan Agent — Plans générés avec succès")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
