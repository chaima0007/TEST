#!/usr/bin/env python3
"""
Real-Time Alert Agent — Caelum Partners CaelumSwarm™
Surveillance et alertes temps réel sur les scores critiques, dépassements
de seuils, anomalies statistiques et événements droits humains.
"""

import sys
import time
import random
from datetime import datetime, timezone
from typing import Optional

ALERT_LEVELS = {
    "URGENCE": {"color": "RED", "notify": ["CEO", "DG", "Conseil"], "delay_minutes": 0, "escalation_hours": 1},
    "CRITIQUE": {"color": "RED", "notify": ["DG", "Directeur RSE"], "delay_minutes": 5, "escalation_hours": 4},
    "ÉLEVÉ": {"color": "ORANGE", "notify": ["Directeur RSE", "Équipe conformité"], "delay_minutes": 30, "escalation_hours": 24},
    "MODÉRÉ": {"color": "YELLOW", "notify": ["Équipe conformité"], "delay_minutes": 120, "escalation_hours": 72},
    "INFO": {"color": "BLUE", "notify": ["Équipe analytique"], "delay_minutes": 480, "escalation_hours": 168},
}

ALERT_TYPES = {
    "SCORE_SPIKE": "Hausse soudaine du score composite (+10 pts en <24h)",
    "THRESHOLD_BREACH": "Dépassement du seuil critique (≥60)",
    "NEW_ENTITY_CRITICAL": "Nouvelle entité détectée en zone critique",
    "DISTRIBUTION_ANOMALY": "Distribution risques déviante (>5 critiques)",
    "SUBSCORE_DIVERGENCE": "Divergence extrême entre sous-scores (>30 pts écart)",
    "LEGAL_TRIGGER": "Nouveau développement juridique impactant le domaine",
    "MEDIA_SURGE": "Pic médiatique négatif détecté sur l'entité",
    "COMPLAINT_RECEIVED": "Mécanisme de réclamation — nouvelle plainte formelle",
    "DEADLINE_APPROACHING": "Échéance réglementaire dans <30 jours",
    "CI_STATUS_CHANGE": "Changement statut pays (sanctions, instabilité politique)",
}

NOTIFICATION_CHANNELS = {
    "EMAIL": {"enabled": True, "format": "HTML report attachment"},
    "SLACK": {"enabled": True, "format": "#alerts-droits-humains channel"},
    "WEBHOOK": {"enabled": True, "format": "POST /api/internal/alerts"},
    "DASHBOARD": {"enabled": True, "format": "In-app notification badge"},
    "SMS": {"enabled": False, "format": "Only for URGENCE level"},
}


def generate_alert(
    alert_type: str,
    entity_id: str,
    entity_name: str,
    domain: str,
    score: float,
    previous_score: Optional[float] = None,
    details: str = "",
) -> dict:
    """Génère une alerte structurée."""
    if score >= 90:
        level = "URGENCE"
    elif score >= 70:
        level = "CRITIQUE"
    elif score >= 50:
        level = "ÉLEVÉ"
    elif score >= 30:
        level = "MODÉRÉ"
    else:
        level = "INFO"

    if alert_type == "SCORE_SPIKE" and previous_score is not None:
        delta = score - previous_score
        if delta >= 20:
            level = "URGENCE"
        elif delta >= 10:
            level = "CRITIQUE"

    alert_config = ALERT_LEVELS[level]
    alert_id = f"ALT-{entity_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "alert_id": alert_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "color": alert_config["color"],
        "type": alert_type,
        "type_description": ALERT_TYPES.get(alert_type, alert_type),
        "entity": {
            "id": entity_id,
            "name": entity_name,
            "domain": domain,
            "current_score": score,
            "previous_score": previous_score,
            "delta": round(score - previous_score, 2) if previous_score is not None else None,
        },
        "notification": {
            "recipients": alert_config["notify"],
            "delay_minutes": alert_config["delay_minutes"],
            "escalation_if_no_ack_hours": alert_config["escalation_hours"],
            "channels": [ch for ch, cfg in NOTIFICATION_CHANNELS.items() if cfg["enabled"]],
        },
        "details": details,
        "recommended_action": _get_recommended_action(alert_type, level, entity_id),
        "auto_created_ticket": f"TICK-{alert_id}",
    }


def _get_recommended_action(alert_type: str, level: str, entity_id: str) -> str:
    actions = {
        "SCORE_SPIKE": f"Analyser causes hausse score {entity_id}. Vérifier sources terrain. Déclencher audit si confirmé.",
        "THRESHOLD_BREACH": f"Activer protocole CSDDD Art.10 pour {entity_id}. Notifier Conseil dans 24h.",
        "LEGAL_TRIGGER": f"Réviser scoring {entity_id} selon nouveau cadre légal. Mettre à jour rapport conformité.",
        "MEDIA_SURGE": f"Préparer position publique. Vérifier exposition {entity_id} dans rapport CSRD.",
        "COMPLAINT_RECEIVED": f"Enregistrer réclamation. Délai de réponse: 30 jours (CSDDD Art.11).",
        "DEADLINE_APPROACHING": f"Vérifier conformité {entity_id} avant échéance. Escalader si gaps identifiés.",
    }
    return actions.get(alert_type, f"Analyser {entity_id} et prendre mesures appropriées selon niveau {level}.")


def simulate_monitoring_cycle(entities: list, domain: str) -> dict:
    """Simule un cycle de surveillance et génère les alertes pertinentes."""
    alerts = []
    stats = {"URGENCE": 0, "CRITIQUE": 0, "ÉLEVÉ": 0, "MODÉRÉ": 0, "INFO": 0}

    for entity in entities:
        score = entity.get("composite_score", 0)
        entity_id = entity.get("id", "UNK")
        entity_name = entity.get("name", "Unknown")

        if score >= 60:
            alert = generate_alert(
                "THRESHOLD_BREACH", entity_id, entity_name, domain, score,
                details=f"Score {score} dépasse seuil critique ≥60"
            )
            alerts.append(alert)
            stats[alert["level"]] += 1

        simulated_previous = score - random.uniform(-5, 12)
        if score - simulated_previous >= 8:
            alert = generate_alert(
                "SCORE_SPIKE", entity_id, entity_name, domain, score,
                previous_score=round(simulated_previous, 2),
                details=f"Hausse de {score - simulated_previous:.1f} pts détectée"
            )
            if alert["level"] in ("URGENCE", "CRITIQUE"):
                alerts.append(alert)
                stats[alert["level"]] += 1

    alerts.sort(key=lambda x: list(ALERT_LEVELS.keys()).index(x["level"]))

    return {
        "monitoring_cycle_id": f"MC-{datetime.now().strftime('%Y%m%d%H%M')}",
        "domain": domain,
        "cycle_timestamp": datetime.now(timezone.utc).isoformat(),
        "entities_monitored": len(entities),
        "alerts_generated": len(alerts),
        "alert_stats": stats,
        "alerts": alerts,
        "next_cycle_in_minutes": 15,
        "status": "ACTIVE" if any(v > 0 for v in stats.values()) else "NOMINAL",
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — REAL-TIME ALERT AGENT")
    print("  Surveillance Temps Réel & Alertes Automatiques")
    print("=" * 70)

    entities = [
        {"id": "DSM-001", "name": "Russie — Deepfakes Guerre Ukraine", "composite_score": 93.45, "risk_level": "critique"},
        {"id": "DSM-002", "name": "Chine — Faux Discours Taïwan", "composite_score": 90.35, "risk_level": "critique"},
        {"id": "DSM-003", "name": "Iran — Manipulation Protestations", "composite_score": 87.60, "risk_level": "critique"},
        {"id": "DSM-004", "name": "États-Unis — Deepfakes Électoraux", "composite_score": 72.65, "risk_level": "critique"},
        {"id": "DSM-005", "name": "Inde — Fake News Politique", "composite_score": 55.30, "risk_level": "élevé"},
        {"id": "DSM-006", "name": "Brésil — Fraudes Réseaux Sociaux", "composite_score": 49.20, "risk_level": "élevé"},
        {"id": "DSM-007", "name": "UE — Régulation DSA en cours", "composite_score": 22.40, "risk_level": "modéré"},
        {"id": "DSM-008", "name": "Corée du Sud — Législation IA", "composite_score": 7.85, "risk_level": "faible"},
    ]

    result = simulate_monitoring_cycle(entities, "deepfake-synthetic-media-rights")

    print(f"\n🔔 CYCLE DE SURVEILLANCE: {result['monitoring_cycle_id']}")
    print(f"   Entités surveillées: {result['entities_monitored']}")
    print(f"   Alertes générées: {result['alerts_generated']}")
    print(f"   Statut système: {result['status']}")

    print(f"\n📊 DISTRIBUTION ALERTES:")
    for level, count in result["alert_stats"].items():
        if count > 0:
            color_map = {"URGENCE": "🔴", "CRITIQUE": "🔴", "ÉLEVÉ": "🟠", "MODÉRÉ": "🟡", "INFO": "🔵"}
            print(f"   {color_map.get(level, '⚪')} {level}: {count}")

    print(f"\n⚡ TOP ALERTES:")
    for alert in result["alerts"][:4]:
        print(f"\n   [{alert['level']}] {alert['type']}")
        print(f"   Entité: {alert['entity']['id']} — {alert['entity']['name'][:50]}")
        print(f"   Score: {alert['entity']['current_score']}")
        if alert['entity']['delta']:
            print(f"   Delta: {alert['entity']['delta']:+.1f} pts")
        print(f"   → {alert['recommended_action'][:70]}...")
        print(f"   Destinataires: {', '.join(alert['notification']['recipients'])}")

    print(f"\n⏱️  Prochain cycle dans: {result['next_cycle_in_minutes']} minutes")
    print(f"\n✅ Real-Time Alert Agent — Cycle complété")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
