#!/usr/bin/env python3
"""
Wage Equity & Working Conditions Agent — Caelum Partners CaelumSwarm™
Analyse équité salariale et conditions de travail selon ILO C100, C131, C155.
Identifie les écarts et génère les recommandations de conformité.
"""

import sys
from datetime import datetime, timezone

WAGE_STANDARDS = {
    "ILO_C131_MINIMUM_WAGE": {
        "label": "ILO C131 — Salaire minimum",
        "description": "Fixation salaire minimum avec processus consultatif",
        "ratified_countries": 56,
    },
    "ILO_C100_EQUAL_PAY": {
        "label": "ILO C100 — Égalité rémunération",
        "description": "Égalité de rémunération pour travail de valeur égale",
        "ratified_countries": 174,
    },
    "LIVING_WAGE_ANKER": {
        "label": "Salaire décent (méthode Anker)",
        "description": "Coût vie réel + épargne 10% + 1 personne dépendante",
        "benchmark": "Global Living Wage Coalition",
    },
    "EU_PAY_TRANSPARENCY_2023": {
        "label": "Directive EU Pay Transparency 2023",
        "description": "Transparence salariale obligatoire — écart H/F < 5%",
        "applicable": "Entreprises UE >100 salariés",
        "deadline": "2026-06-07",
    },
    "CSRD_ESRS_S1": {
        "label": "CSRD ESRS S1 — Travailleurs propres opérations",
        "description": "Reporting salaires, conditions travail, santé sécurité",
        "applicable": "Grandes entreprises UE",
        "deadline": "2025-01-01",
    },
}

GENDER_PAY_GAP_BENCHMARKS = {
    "EU_AVERAGE": 13.0,
    "OECD_AVERAGE": 12.0,
    "GLOBAL_AVERAGE": 20.0,
    "ILO_TARGET": 0.0,
    "EU_DIRECTIVE_MAX": 5.0,
}

WORKING_CONDITIONS_INDICATORS = {
    "hours_week": {
        "ilo_limit": 48,
        "recommended": 40,
        "label": "Heures travail hebdomadaires",
        "ilo_ref": "C1, C47",
    },
    "overtime_compensation": {
        "ilo_minimum": 1.25,
        "recommended": 1.50,
        "label": "Majoration heures sup. (coefficient)",
        "ilo_ref": "C1",
    },
    "paid_leave_days": {
        "ilo_minimum": 21,
        "recommended": 25,
        "label": "Jours congé payé annuel",
        "ilo_ref": "C132",
    },
    "sick_leave_paid": {
        "ilo_minimum": True,
        "label": "Congé maladie payé",
        "ilo_ref": "C130",
    },
    "maternity_leave_weeks": {
        "ilo_minimum": 14,
        "recommended": 18,
        "label": "Durée congé maternité (semaines)",
        "ilo_ref": "C183",
    },
    "occupational_health_committee": {
        "ilo_minimum": True,
        "label": "Comité santé sécurité",
        "ilo_ref": "C155",
    },
}

SECTOR_WAGE_RISKS = {
    "textile_garment": {
        "gender_pay_gap_est": 25,
        "living_wage_gap_est": 40,
        "key_violations": ["living_wage", "overtime", "forced_overtime"],
        "hotspot_countries": ["Bangladesh", "Cambodia", "Myanmar", "Pakistan"],
    },
    "agriculture": {
        "gender_pay_gap_est": 35,
        "living_wage_gap_est": 55,
        "key_violations": ["seasonal_labor", "piece_rate_below_minimum", "housing_deductions"],
        "hotspot_countries": ["Morocco", "Jordan", "Guatemala", "Thailand"],
    },
    "construction": {
        "gender_pay_gap_est": 20,
        "living_wage_gap_est": 30,
        "key_violations": ["wage_theft", "safety", "document_confiscation"],
        "hotspot_countries": ["Qatar", "UAE", "Saudi Arabia", "Kuwait"],
    },
    "tech_software": {
        "gender_pay_gap_est": 18,
        "living_wage_gap_est": 5,
        "key_violations": ["gender_pay_gap", "freelancer_misclassification"],
        "hotspot_countries": ["USA", "EU (certains)", "India"],
    },
    "domestic_work": {
        "gender_pay_gap_est": 40,
        "living_wage_gap_est": 60,
        "key_violations": ["exclusion_labor_law", "excessive_hours", "document_confiscation"],
        "hotspot_countries": ["Gulf states", "Lebanon", "Singapore"],
    },
}


def analyze_wage_equity(entity: dict, domain: str, sector: str = "textile_garment") -> dict:
    """Analyse l'équité salariale et les conditions de travail."""
    score = entity.get("composite_score", 0)
    sector_profile = SECTOR_WAGE_RISKS.get(sector, SECTOR_WAGE_RISKS["textile_garment"])

    gender_gap = sector_profile["gender_pay_gap_est"] * (score / 80)
    living_wage_gap = sector_profile["living_wage_gap_est"] * (score / 100)

    eu_directive_compliant = gender_gap <= GENDER_PAY_GAP_BENCHMARKS["EU_DIRECTIVE_MAX"]

    condition_gaps = {}
    for indicator, standards in WORKING_CONDITIONS_INDICATORS.items():
        if "ilo_minimum" in standards and isinstance(standards["ilo_minimum"], (int, float)):
            current_pct = max(0, 100 - score * 0.5)
            ilo_pct = 100
            gap = max(0, ilo_pct - current_pct)
            condition_gaps[indicator] = {
                "label": standards["label"],
                "gap_pct": round(gap, 1),
                "ilo_ref": standards.get("ilo_ref", ""),
                "compliant": gap < 10,
            }

    violations = [
        {
            "violation": viol,
            "severity": "GRAVE" if score >= 60 else "MODÉRÉ",
            "ilo_convention": "ILO C29/C105/C131",
        }
        for viol in sector_profile["key_violations"][:3]
    ]

    remediation_actions = []
    if gender_gap > GENDER_PAY_GAP_BENCHMARKS["EU_DIRECTIVE_MAX"]:
        remediation_actions.append({
            "action": f"Audit salarial genre — écart actuel estimé {gender_gap:.0f}%",
            "deadline_months": 6,
            "regulation": "EU Pay Transparency Directive 2023",
        })
    if living_wage_gap > 20:
        remediation_actions.append({
            "action": f"Plan ajustement salaires vers salaire décent — gap {living_wage_gap:.0f}%",
            "deadline_months": 12,
            "regulation": "ILO C131 + Global Living Wage Coalition",
        })
    remediation_actions.append({
        "action": "Audit conditions travail fournisseurs T1 — protocole ILO",
        "deadline_months": 6,
        "regulation": "CSDDD Art.8 + ILO C155",
    })

    return {
        "entity_id": entity.get("id"),
        "entity_name": entity.get("name"),
        "domain": domain,
        "sector": sector,
        "composite_score": score,
        "wage_analysis": {
            "estimated_gender_pay_gap_pct": round(gender_gap, 1),
            "estimated_living_wage_gap_pct": round(living_wage_gap, 1),
            "eu_directive_compliant": eu_directive_compliant,
            "eu_directive_max": GENDER_PAY_GAP_BENCHMARKS["EU_DIRECTIVE_MAX"],
            "gap_vs_oecd_avg": round(gender_gap - GENDER_PAY_GAP_BENCHMARKS["OECD_AVERAGE"], 1),
        },
        "working_conditions": {
            "condition_gaps": condition_gaps,
            "violations_identified": violations,
            "hotspot_countries": sector_profile["hotspot_countries"],
        },
        "ilo_conventions_triggered": list({
            viol.get("ilo_convention", "") for viol in violations
        }),
        "csrd_esrs_s1_disclosure_required": score >= 20,
        "remediation_plan": remediation_actions,
        "estimated_remediation_cost_EUR": int(score * 50_000 * (living_wage_gap / 100 + 0.1)),
    }


def generate_wage_equity_report(entities: list, domain: str, sector: str = "textile_garment") -> dict:
    """Génère le rapport complet équité salariale."""
    analyses = [analyze_wage_equity(e, domain, sector) for e in entities]

    avg_gender_gap = sum(a["wage_analysis"]["estimated_gender_pay_gap_pct"] for a in analyses) / len(analyses) if analyses else 0
    avg_living_gap = sum(a["wage_analysis"]["estimated_living_wage_gap_pct"] for a in analyses) / len(analyses) if analyses else 0
    non_compliant_eu = [a for a in analyses if not a["wage_analysis"]["eu_directive_compliant"]]

    return {
        "report_type": "WAGE_EQUITY_WORKING_CONDITIONS",
        "report_id": f"WE-{domain[:6].upper()}-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Wage Equity & Working Conditions Agent v1.0",
        "domain": domain,
        "sector": sector,
        "portfolio_summary": {
            "entities_assessed": len(analyses),
            "avg_gender_pay_gap_pct": round(avg_gender_gap, 1),
            "avg_living_wage_gap_pct": round(avg_living_gap, 1),
            "non_compliant_eu_directive": len(non_compliant_eu),
            "ilo_standards_at_risk": list(WAGE_STANDARDS.keys())[:3],
        },
        "regulatory_deadlines": {
            "eu_pay_transparency": WAGE_STANDARDS["EU_PAY_TRANSPARENCY_2023"]["deadline"],
            "csrd_esrs_s1": WAGE_STANDARDS["CSRD_ESRS_S1"]["deadline"],
        },
        "entity_analyses": analyses,
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — WAGE EQUITY & WORKING CONDITIONS AGENT")
    print("  Équité Salariale & Conditions Travail — ILO C100/C131/C155")
    print("=" * 70)

    entities = [
        {"id": "GEL-001", "name": "Uber/Deliveroo — 3M Livreurs Sans Droits UE", "composite_score": 87.20, "risk_level": "critique"},
        {"id": "GEL-003", "name": "Amazon Entrepôts — Cadences Robots Sans Pause", "composite_score": 82.80, "risk_level": "critique"},
        {"id": "GEL-007", "name": "Freelancers Union USA — Portabilité Avantages", "composite_score": 28.60, "risk_level": "modéré"},
    ]

    report = generate_wage_equity_report(entities, "gig-economy-labor-exploitation", "tech_software")

    ps = report["portfolio_summary"]
    print(f"\n💰 RAPPORT ÉQUITÉ SALARIALE: {report['report_id']}")
    print(f"   Secteur: {report['sector']}")
    print(f"   Entités évaluées: {ps['entities_assessed']}")
    print(f"   Écart genre moyen estimé: {ps['avg_gender_pay_gap_pct']:.1f}% (max EU: {GENDER_PAY_GAP_BENCHMARKS['EU_DIRECTIVE_MAX']}%)")
    print(f"   Gap salaire décent moyen: {ps['avg_living_wage_gap_pct']:.1f}%")
    print(f"   Non-conforme Directive EU: {ps['non_compliant_eu_directive']}/{ps['entities_assessed']}")

    print(f"\n📅 ÉCHÉANCES RÉGLEMENTAIRES:")
    for reg, deadline in report["regulatory_deadlines"].items():
        print(f"   • {reg}: {deadline}")

    print(f"\n⚡ ANALYSES ENTITÉS:")
    for a in report["entity_analyses"][:2]:
        w = a["wage_analysis"]
        print(f"\n   [{a['entity_id']}] {a['entity_name'][:50]}")
        print(f"   Score: {a['composite_score']} | Gap genre: {w['estimated_gender_pay_gap_pct']:.1f}% | Gap salaire décent: {w['estimated_living_wage_gap_pct']:.1f}%")
        print(f"   Conforme Directive EU: {'✅ OUI' if w['eu_directive_compliant'] else '❌ NON'}")
        print(f"   Violations:")
        for viol in a["working_conditions"]["violations_identified"][:2]:
            print(f"     ⚠️  {viol['violation']} [{viol['severity']}] — {viol['ilo_convention']}")
        print(f"   Plan remédiation:")
        for action in a["remediation_plan"][:2]:
            print(f"     • J+{action['deadline_months']*30}: {action['action'][:55]}...")

    print(f"\n✅ Wage Equity & Working Conditions Agent — Rapport généré avec succès")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
