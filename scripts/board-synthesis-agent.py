#!/usr/bin/env python3
"""
Board Synthesis Agent — Caelum Partners CaelumSwarm™
Synthèse exécutive pour Conseil d'Administration.
Agrège tous les rapports CaelumSwarm™ en un brief stratégique concis.
"""

import sys
from datetime import datetime, timezone

BOARD_REPORT_SECTIONS = [
    "executive_brief",
    "risk_thermometer",
    "top_3_priorities",
    "regulatory_radar",
    "financial_exposure",
    "strategic_options",
    "decision_required",
]

STRATEGIC_FRAMES = {
    "PROTECT": "Protéger — Éviter sanctions, contentieux, réputation",
    "COMPLY": "Conformer — Répondre aux obligations légales CSDDD/CSRD",
    "LEAD": "Progresser — Différenciation compétitive ESG",
    "PARTNER": "Coopérer — Alliances sectorielles, reporting collectif",
}

BOARD_DECISION_TYPES = {
    "APPROVE_BUDGET": "Approuver budget plan d'action correctif",
    "MANDATE_AUDIT": "Mandater audit terrain indépendant",
    "POLICY_UPDATE": "Mettre à jour politique droits humains groupe",
    "SUPPLIER_EXIT": "Décision sortie fournisseur à risque critique",
    "CSRD_SIGN_OFF": "Valider et signer rapport CSRD annuel",
    "CRISIS_RESPONSE": "Activer protocole crise droits humains",
}


def generate_risk_thermometer(domains_data: list) -> dict:
    """Génère un thermomètre de risque synthétique."""
    all_scores = [d.get("avg_composite", 0) for d in domains_data]
    portfolio_avg = sum(all_scores) / len(all_scores) if all_scores else 0

    criticals = sum(d.get("critical_count", 0) for d in domains_data)
    total_entities = sum(d.get("entity_count", 0) for d in domains_data)

    portfolio_status = (
        "CRISE" if portfolio_avg >= 75
        else "ALERTE" if portfolio_avg >= 60
        else "VIGILANCE" if portfolio_avg >= 45
        else "STABLE" if portfolio_avg >= 25
        else "BON"
    )

    return {
        "portfolio_avg": round(portfolio_avg, 1),
        "portfolio_status": portfolio_status,
        "total_entities": total_entities,
        "critical_entities": criticals,
        "pct_critical": round(criticals / total_entities * 100, 0) if total_entities > 0 else 0,
        "trend": "→ STABLE",
        "domains_count": len(domains_data),
    }


def generate_board_brief(
    company: str,
    domains_data: list,
    wave: int = 193,
    prepared_by: str = "CaelumSwarm™",
) -> dict:
    """Génère le brief complet pour le Conseil d'Administration."""
    thermometer = generate_risk_thermometer(domains_data)

    top_3 = sorted(domains_data, key=lambda x: x.get("avg_composite", 0), reverse=True)[:3]

    total_budget = sum(d.get("estimated_action_budget_EUR", 50_000) for d in domains_data)
    legal_risk_EUR = sum(
        d.get("entity_count", 8) * d.get("avg_composite", 50) * 10_000
        for d in domains_data
    )

    strategic_recommendation = (
        STRATEGIC_FRAMES["PROTECT"] if thermometer["portfolio_avg"] >= 65
        else STRATEGIC_FRAMES["COMPLY"] if thermometer["portfolio_avg"] >= 45
        else STRATEGIC_FRAMES["LEAD"] if thermometer["portfolio_avg"] >= 25
        else STRATEGIC_FRAMES["PARTNER"]
    )

    decisions_required = []
    if thermometer["critical_entities"] >= 4:
        decisions_required.append({
            "type": "APPROVE_BUDGET",
            "description": BOARD_DECISION_TYPES["APPROVE_BUDGET"],
            "amount_EUR": total_budget,
            "urgency": "CE CONSEIL",
        })
    if thermometer["portfolio_avg"] >= 60:
        decisions_required.append({
            "type": "MANDATE_AUDIT",
            "description": BOARD_DECISION_TYPES["MANDATE_AUDIT"],
            "urgency": "30 JOURS",
        })
    decisions_required.append({
        "type": "POLICY_UPDATE",
        "description": BOARD_DECISION_TYPES["POLICY_UPDATE"],
        "urgency": "60 JOURS",
    })

    return {
        "brief_id": f"BOARD-{company[:6].upper()}-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": f"CaelumSwarm™ Board Synthesis Agent v1.0 — Préparé par {prepared_by}",
        "company": company,
        "wave": wave,
        "classification": "CONFIDENTIEL — Conseil d'Administration uniquement",
        "executive_brief": {
            "one_liner": (
                f"Le portefeuille droits humains Caelum {wave} présente un score moyen de "
                f"{thermometer['portfolio_avg']}/100 ({thermometer['portfolio_status']}) "
                f"avec {thermometer['critical_entities']} entités en zone critique sur {thermometer['total_entities']}."
            ),
            "bottom_line": (
                "ACTION IMMÉDIATE REQUISE" if thermometer["portfolio_avg"] >= 60
                else "PLAN PRÉVENTION À FORMALISER" if thermometer["portfolio_avg"] >= 40
                else "SURVEILLANCE RENFORCÉE SUFFISANTE"
            ),
        },
        "risk_thermometer": thermometer,
        "top_3_priorities": [
            {
                "rank": i + 1,
                "domain": d.get("domain", ""),
                "avg_score": d.get("avg_composite", 0),
                "critical_count": d.get("critical_count", 0),
                "key_risk": d.get("key_risk", "Violation droits humains"),
                "action_required": d.get("action_required", "Audit terrain"),
            }
            for i, d in enumerate(top_3)
        ],
        "financial_exposure": {
            "action_budget_required_EUR": total_budget,
            "csddd_penalty_exposure_EUR": round(legal_risk_EUR, -5),
            "reputation_value_at_risk_pct": max(3, thermometer["portfolio_avg"] / 10),
            "csrd_non_disclosure_risk": "Amende CSRD + exclusion indices ESG",
        },
        "strategic_recommendation": strategic_recommendation,
        "regulatory_radar": {
            "immediate": "CSRD 2025 — Rapport annuel doit intégrer ESRS S4",
            "short_term": "CSDDD 2027 — Plan diligence devait être en cours",
            "medium_term": "AI Act 2026 — Systèmes IA haut risque à cartographier",
        },
        "decisions_required": decisions_required,
        "next_board_update": "60 jours — Rapport d'avancement plans correctifs",
        "prepared_by": f"CaelumSwarm™ Board Synthesis Agent | {datetime.now().strftime('%d/%m/%Y')}",
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — BOARD SYNTHESIS AGENT")
    print("  Synthèse Exécutive pour Conseil d'Administration")
    print("=" * 70)

    domains_data = [
        {
            "domain": "statelessness-document-rights",
            "avg_composite": 62.29,
            "entity_count": 8,
            "critical_count": 4,
            "estimated_action_budget_EUR": 180_000,
            "key_risk": "4 millions d'apatrides sans accès documents identité",
            "action_required": "Audit terrain urgence — Myanmar, Côte d'Ivoire",
        },
        {
            "domain": "offshore-tax-haven-rights",
            "avg_composite": 62.26,
            "entity_count": 8,
            "critical_count": 4,
            "estimated_action_budget_EUR": 120_000,
            "key_risk": "Exposition fournisseurs/clients dans juridictions GAFI",
            "action_required": "Cartographie exposition offshore — audit conformité",
        },
        {
            "domain": "deepfake-synthetic-media-rights",
            "avg_composite": 59.63,
            "entity_count": 8,
            "critical_count": 4,
            "estimated_action_budget_EUR": 95_000,
            "key_risk": "Usage outils IA génératifs non conformes AI Act",
            "action_required": "Inventaire systèmes IA — évaluation conformité AI Act",
        },
    ]

    brief = generate_board_brief("Caelum Partners SPRL", domains_data, wave=193)

    print(f"\n📊 BRIEF CONSEIL: {brief['brief_id']}")
    print(f"   {brief['classification']}")
    print(f"\n   RÉSUMÉ EXÉCUTIF:")
    print(f"   {brief['executive_brief']['one_liner']}")
    print(f"\n   CONCLUSION: {brief['executive_brief']['bottom_line']}")

    t = brief["risk_thermometer"]
    print(f"\n🌡️  THERMOMÈTRE DE RISQUE:")
    print(f"   Score portefeuille: {t['portfolio_avg']}/100 — {t['portfolio_status']}")
    print(f"   Entités critiques: {t['critical_entities']}/{t['total_entities']} ({t['pct_critical']:.0f}%)")
    print(f"   Domaines surveillés: {t['domains_count']}")

    print(f"\n🎯 TOP 3 PRIORITÉS:")
    for p in brief["top_3_priorities"]:
        print(f"   {p['rank']}. {p['domain'][:40]} — Score: {p['avg_score']} | Critiques: {p['critical_count']}")
        print(f"      Risque: {p['key_risk'][:60]}")
        print(f"      Action: {p['action_required'][:55]}")

    f = brief["financial_exposure"]
    print(f"\n💰 EXPOSITION FINANCIÈRE:")
    print(f"   Budget plan d'action requis: {f['action_budget_required_EUR']:,.0f}€")
    print(f"   Risque amende CSDDD: {f['csddd_penalty_exposure_EUR']:,.0f}€")
    print(f"   Risque valeur réputation: -{f['reputation_value_at_risk_pct']:.1f}%")

    print(f"\n📋 RECOMMANDATION STRATÉGIQUE: {brief['strategic_recommendation']}")

    print(f"\n✅ DÉCISIONS REQUISES CE CONSEIL:")
    for dec in brief["decisions_required"]:
        amount = f" — {dec['amount_EUR']:,.0f}€" if 'amount_EUR' in dec else ""
        print(f"   [{dec['urgency']}] {dec['description']}{amount}")

    print(f"\n📅 Prochain rapport CA: {brief['next_board_update']}")
    print(f"\n✅ Board Synthesis Agent — Brief exécutif généré avec succès")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
