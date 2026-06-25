#!/usr/bin/env python3
"""
Sentiment & Reputation Analysis Agent — Caelum Partners CaelumSwarm™
Analyse sentiment médias, réseaux sociaux et ESG scores pour les entités surveillées.
Corrèle réputation externe avec scores droits humains CaelumSwarm™.
"""

import sys
import math
from datetime import datetime, timezone

SENTIMENT_SOURCES = {
    "PRESS_INTERNATIONAL": {"weight": 0.30, "label": "Presse internationale", "lag_days": 1},
    "NGO_REPORTS": {"weight": 0.25, "label": "Rapports ONG", "lag_days": 7},
    "ESG_RATINGS": {"weight": 0.20, "label": "Agences notation ESG", "lag_days": 30},
    "SOCIAL_MEDIA": {"weight": 0.15, "label": "Réseaux sociaux (filtré)", "lag_days": 0},
    "ACADEMIC": {"weight": 0.10, "label": "Publications académiques", "lag_days": 90},
}

ESG_RATERS = {
    "MSCI_ESG": {"scale": "AAA→CCC", "hr_weight": 0.35, "benchmark": "BBB"},
    "SUSTAINALYTICS": {"scale": "0→40+ (risk)", "hr_weight": 0.30, "benchmark": 25},
    "REFINITIV": {"scale": "0→100", "hr_weight": 0.25, "benchmark": 50},
    "BLOOMBERG_ESG": {"scale": "0→100", "hr_weight": 0.10, "benchmark": 55},
}

REPUTATION_CRISIS_SIGNALS = {
    "media_spike": {"threshold_pct": 300, "description": "Pic médiatique +300% en 48h"},
    "ngo_report": {"threshold_score": -40, "description": "Rapport ONG très critique publié"},
    "activist_campaign": {"threshold_mentions": 10000, "description": "10K+ mentions campagne activiste"},
    "regulatory_action": {"threshold_score": -50, "description": "Action réglementaire annoncée"},
    "legal_proceedings": {"threshold_score": -35, "description": "Procédure judiciaire initiée"},
    "whistleblower": {"threshold_score": -45, "description": "Alerte lanceur d'alerte publiée"},
}

REPUTATION_IMPACT_BY_RISK = {
    "critique": {"reputation_drag": -35, "recovery_months": 24, "investor_concern": "TRÈS ÉLEVÉ"},
    "élevé": {"reputation_drag": -18, "recovery_months": 12, "investor_concern": "ÉLEVÉ"},
    "modéré": {"reputation_drag": -8, "recovery_months": 6, "investor_concern": "MODÉRÉ"},
    "faible": {"reputation_drag": +5, "recovery_months": 0, "investor_concern": "FAIBLE (positif)"},
}


def analyze_sentiment(entity: dict, domain: str) -> dict:
    """Analyse le sentiment pour une entité donnée."""
    score = entity.get("composite_score", 0)
    risk = entity.get("risk_level", "faible")

    base_sentiment = -score / 100

    weighted_sentiment = sum(
        base_sentiment * (1 + (src["lag_days"] / 100)) * src["weight"]
        for src in SENTIMENT_SOURCES.values()
    )

    sentiment_label = (
        "TRÈS NÉGATIF" if weighted_sentiment < -0.60
        else "NÉGATIF" if weighted_sentiment < -0.30
        else "MITIGÉ" if weighted_sentiment < -0.10
        else "NEUTRE" if weighted_sentiment < 0.10
        else "POSITIF"
    )

    reputation_impact = REPUTATION_IMPACT_BY_RISK.get(risk, REPUTATION_IMPACT_BY_RISK["faible"])

    crisis_signals_detected = []
    if score >= 70:
        crisis_signals_detected.append(REPUTATION_CRISIS_SIGNALS["ngo_report"])
    if score >= 85:
        crisis_signals_detected.append(REPUTATION_CRISIS_SIGNALS["media_spike"])
    if score >= 90:
        crisis_signals_detected.append(REPUTATION_CRISIS_SIGNALS["activist_campaign"])

    esg_impact = {}
    for rater, config in ESG_RATERS.items():
        degradation = score * config["hr_weight"] / 100 * 20
        esg_impact[rater] = {
            "impact": f"-{degradation:.1f} points" if degradation > 1 else "Neutre",
            "concern_level": "ÉLEVÉ" if degradation > 8 else "MODÉRÉ" if degradation > 3 else "FAIBLE",
        }

    return {
        "entity_id": entity.get("id"),
        "entity_name": entity.get("name"),
        "domain": domain,
        "analysis_date": datetime.now(timezone.utc).isoformat(),
        "sentiment": {
            "weighted_score": round(weighted_sentiment, 3),
            "label": sentiment_label,
            "confidence": 0.75,
        },
        "reputation_impact": {
            "reputation_drag_pct": reputation_impact["reputation_drag"],
            "recovery_timeline_months": reputation_impact["recovery_months"],
            "investor_concern_level": reputation_impact["investor_concern"],
        },
        "crisis_signals": crisis_signals_detected,
        "esg_rating_impact": esg_impact,
        "communication_recommended": (
            "CRISIS_COMMS" if score >= 70 and len(crisis_signals_detected) >= 2
            else "PROACTIVE_PR" if score >= 50
            else "STANDARD_MONITORING"
        ),
        "media_monitoring_frequency": (
            "CONTINU (toutes les heures)" if score >= 80
            else "QUOTIDIEN" if score >= 50
            else "HEBDOMADAIRE"
        ),
    }


def generate_reputation_report(entities: list, domain: str) -> dict:
    """Génère le rapport complet d'analyse sentiment et réputation."""
    analyses = [analyze_sentiment(e, domain) for e in entities]

    crisis_entities = [a for a in analyses if len(a["crisis_signals"]) >= 2]
    very_negative = [a for a in analyses if a["sentiment"]["label"] in ("TRÈS NÉGATIF", "NÉGATIF")]

    avg_reputation_drag = sum(
        a["reputation_impact"]["reputation_drag_pct"] for a in analyses
    ) / len(analyses) if analyses else 0

    return {
        "report_type": "SENTIMENT_REPUTATION",
        "report_id": f"SR-{domain[:6].upper()}-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Sentiment & Reputation Agent v1.0",
        "domain": domain,
        "executive_summary": {
            "entities_analyzed": len(analyses),
            "in_crisis_mode": len(crisis_entities),
            "negative_sentiment_count": len(very_negative),
            "avg_reputation_drag_pct": round(avg_reputation_drag, 1),
            "portfolio_outlook": "CRITIQUE" if len(crisis_entities) >= 2 else "DÉGRADÉ" if len(very_negative) >= 3 else "STABLE",
        },
        "crisis_entities": crisis_entities,
        "entity_analyses": analyses,
        "media_monitoring": {
            "sources_monitored": list(SENTIMENT_SOURCES.keys()),
            "next_report": "24h",
            "alert_threshold": "Sentiment < -0.50 ou signal crise détecté",
        },
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — SENTIMENT & REPUTATION ANALYSIS AGENT")
    print("  Analyse Médias, ESG & Réputation Droits Humains")
    print("=" * 70)

    entities = [
        {"id": "OTH-001", "name": "Îles Caïmans — 0% Impôt, 100K Entreprises", "composite_score": 91.60, "risk_level": "critique"},
        {"id": "OTH-004", "name": "Suisse — Secret Bancaire Résiduel", "composite_score": 82.90, "risk_level": "critique"},
        {"id": "OTH-007", "name": "Irlande — Taux 12.5%, Apple 13B€", "composite_score": 26.65, "risk_level": "modéré"},
        {"id": "OTH-008", "name": "Danemark — OCDE 15% Adopté", "composite_score": 6.45, "risk_level": "faible"},
    ]

    report = generate_reputation_report(entities, "offshore-tax-haven-rights")

    print(f"\n📰 RAPPORT SENTIMENT: {report['report_id']}")
    s = report["executive_summary"]
    print(f"   Entités analysées: {s['entities_analyzed']}")
    print(f"   En mode crise: {s['in_crisis_mode']}")
    print(f"   Sentiment négatif: {s['negative_sentiment_count']}")
    print(f"   Impact réputation moyen: {s['avg_reputation_drag_pct']:+.1f}%")
    print(f"   Perspective portefeuille: {s['portfolio_outlook']}")

    print(f"\n🔍 ANALYSES PAR ENTITÉ:")
    for a in report["entity_analyses"]:
        icon = "🔴" if a["sentiment"]["label"] in ("TRÈS NÉGATIF",) else "🟠" if a["sentiment"]["label"] == "NÉGATIF" else "🟡" if a["sentiment"]["label"] == "MITIGÉ" else "🟢"
        print(f"\n   {icon} {a['entity_id']} — {a['entity_name'][:45]}")
        print(f"      Sentiment: {a['sentiment']['label']} ({a['sentiment']['weighted_score']:+.2f})")
        print(f"      Impact réputation: {a['reputation_impact']['reputation_drag_pct']:+d}% | Récupération: {a['reputation_impact']['recovery_timeline_months']}m")
        print(f"      Signaux crise: {len(a['crisis_signals'])}")
        if a["crisis_signals"]:
            for sig in a["crisis_signals"][:2]:
                print(f"        ⚠️  {sig['description']}")
        print(f"      Communication: {a['communication_recommended']}")
        print(f"      Monitoring: {a['media_monitoring_frequency']}")

    print(f"\n✅ Sentiment & Reputation Agent — Rapport généré avec succès")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
