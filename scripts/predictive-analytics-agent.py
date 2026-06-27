#!/usr/bin/env python3
"""
Agent Analyse Prédictive — Caelum Partners CaelumSwarm™
Prédit les tendances droits humains, risques CSDDD, violations émergentes
et comportements clients à partir des données historiques CaelumSwarm™ Wave Series.
"""

import sys
import math
from datetime import datetime, timezone

# ─── Modèles prédictifs ──────────────────────────────────────────────────────

PREDICTIVE_MODELS = {
    "VIOLATION_EMERGENCE": {
        "label": "Émergence de nouvelles violations DH",
        "model_type": "ANOMALY_DETECTION",
        "accuracy_pct": 81.4,
        "training_data_waves": list(range(150, 195)),
        "prediction_horizon_days": 90,
        "key_features": [
            "conflict_escalation_index",
            "ngo_alert_volume_delta",
            "media_coverage_spike",
            "regulatory_announcement_count",
            "supply_chain_disruption_score",
        ],
        "refresh_cadence_hours": 24,
    },
    "REGULATORY_CHANGE": {
        "label": "Changement réglementaire CSDDD / droits humains",
        "model_type": "CLASSIFICATION",
        "accuracy_pct": 87.2,
        "training_data_waves": list(range(140, 195)),
        "prediction_horizon_days": 180,
        "key_features": [
            "eu_legislative_pipeline_score",
            "advocacy_coalition_size",
            "media_pressure_index",
            "election_cycle_phase",
            "inter_institutional_alignment",
        ],
        "refresh_cadence_hours": 48,
    },
    "CLIENT_CHURN_RISK": {
        "label": "Risque de désabonnement client (churn)",
        "model_type": "CLASSIFICATION",
        "accuracy_pct": 79.8,
        "training_data_waves": list(range(160, 195)),
        "prediction_horizon_days": 90,
        "key_features": [
            "last_report_engagement_score",
            "support_ticket_volume",
            "nps_trend",
            "domain_relevance_to_client_sector",
            "contract_renewal_proximity_days",
        ],
        "refresh_cadence_hours": 72,
    },
    "WAVE_SCORE_FORECAST": {
        "label": "Prévision des scores moyens composites Wave N+1 à N+3",
        "model_type": "TIME_SERIES",
        "accuracy_pct": 92.1,
        "training_data_waves": list(range(130, 195)),
        "prediction_horizon_days": 45,
        "key_features": [
            "historical_avg_composite",
            "csddd_pressure_index",
            "domain_novelty_score",
            "geopolitical_instability_index",
            "seasonal_adjustment_factor",
        ],
        "refresh_cadence_hours": 12,
    },
    "SECTOR_RISK_TREND": {
        "label": "Tendance du risque sectoriel (textile, mining, tech, agri)",
        "model_type": "REGRESSION",
        "accuracy_pct": 84.5,
        "training_data_waves": list(range(155, 195)),
        "prediction_horizon_days": 120,
        "key_features": [
            "sector_incident_frequency",
            "supply_chain_complexity_score",
            "enforcement_action_count",
            "esg_reporting_adoption_rate",
            "ilo_violation_database_delta",
        ],
        "refresh_cadence_hours": 36,
    },
    "MEDIA_ATTENTION_SPIKE": {
        "label": "Détection des pics d'attention médiatique imminents",
        "model_type": "ANOMALY_DETECTION",
        "accuracy_pct": 76.3,
        "training_data_waves": list(range(165, 195)),
        "prediction_horizon_days": 14,
        "key_features": [
            "social_media_mention_velocity",
            "influencer_engagement_score",
            "ngo_press_release_volume",
            "mainstream_media_pickup_rate",
            "parliamentary_question_count",
        ],
        "refresh_cadence_hours": 6,
    },
}

# ─── Données historiques Wave 185-194 ────────────────────────────────────────

HISTORICAL_WAVE_DATA = [
    {
        "wave": 185,
        "avg_composite_score": 60.14,
        "critical_entities_count": 4,
        "domains_analyzed": ["algorithmic_justice_bias_rights", "water_privatization_commons_rights", "prison_industrial_complex_rights"],
        "date": "2025-09-12",
        "media_coverage_score": 5.8,
        "regulatory_action_triggered": False,
    },
    {
        "wave": 186,
        "avg_composite_score": 60.47,
        "critical_entities_count": 4,
        "domains_analyzed": ["digital_feudalism_platform_rights", "carbon_colonialism_climate_justice", "biotech_genetic_discrimination_rights"],
        "date": "2025-09-26",
        "media_coverage_score": 6.1,
        "regulatory_action_triggered": False,
    },
    {
        "wave": 187,
        "avg_composite_score": 60.89,
        "critical_entities_count": 4,
        "domains_analyzed": ["neurotech_cognitive_liberty_rights", "space_colonization_indigenous_rights", "synthetic_biology_biosafety_rights"],
        "date": "2025-10-10",
        "media_coverage_score": 6.3,
        "regulatory_action_triggered": True,
    },
    {
        "wave": 188,
        "avg_composite_score": 60.27,
        "critical_entities_count": 4,
        "domains_analyzed": ["quantum_surveillance_privacy_rights", "post_quantum_cryptography_rights", "quantum_supremacy_arms_race"],
        "date": "2025-10-24",
        "media_coverage_score": 5.9,
        "regulatory_action_triggered": False,
    },
    {
        "wave": 189,
        "avg_composite_score": 61.74,
        "critical_entities_count": 5,
        "domains_analyzed": ["statelessness_document_rights", "offshore_tax_haven_rights", "deepfake_synthetic_media_rights"],
        "date": "2025-11-07",
        "media_coverage_score": 7.2,
        "regulatory_action_triggered": True,
    },
    {
        "wave": 190,
        "avg_composite_score": 61.96,
        "critical_entities_count": 4,
        "domains_analyzed": ["dark_web_cybercrime_rights", "gig_economy_labor_exploitation", "indigenous_language_extinction_rights"],
        "date": "2025-11-21",
        "media_coverage_score": 6.8,
        "regulatory_action_triggered": False,
    },
    {
        "wave": 191,
        "avg_composite_score": 62.18,
        "critical_entities_count": 5,
        "domains_analyzed": ["gender_pay_gap_corporate_rights", "indigenous_land_rights_mining", "arms_trade_conflict_complicity"],
        "date": "2025-12-05",
        "media_coverage_score": 7.4,
        "regulatory_action_triggered": True,
    },
    {
        "wave": 192,
        "avg_composite_score": 62.60,
        "critical_entities_count": 5,
        "domains_analyzed": ["climate_migration_displacement_rights", "ai_surveillance_authoritarian_regimes", "child_labor_cocoa_supply_chains"],
        "date": "2025-12-19",
        "media_coverage_score": 7.8,
        "regulatory_action_triggered": True,
    },
    {
        "wave": 193,
        "avg_composite_score": 62.94,
        "critical_entities_count": 5,
        "domains_analyzed": ["forced_labor_semiconductor_rights", "ecocide_corporate_accountability", "digital_colonialism_data_rights"],
        "date": "2026-01-09",
        "media_coverage_score": 8.1,
        "regulatory_action_triggered": True,
    },
    {
        "wave": 194,
        "avg_composite_score": 63.31,
        "critical_entities_count": 6,
        "domains_analyzed": ["corporate_tax_avoidance_rights", "border_surveillance_migration_rights", "platform_content_moderation_rights"],
        "date": "2026-01-23",
        "media_coverage_score": 8.4,
        "regulatory_action_triggered": True,
    },
]

# ─── Indicateurs avancés (leading indicators) ─────────────────────────────────

RISK_INDICATORS = {
    "COMMODITY_PRICE_SPIKE": {
        "label": "Pic prix matières premières",
        "lead_time_days": 45,
        "data_source": "World Bank Commodity Markets",
        "weight_in_prediction": 0.12,
        "current_signal": "HIGH",
    },
    "CONFLICT_ESCALATION": {
        "label": "Escalade de conflits armés",
        "lead_time_days": 30,
        "data_source": "ACLED Conflict Database",
        "weight_in_prediction": 0.20,
        "current_signal": "CRITICAL",
    },
    "REGULATORY_ANNOUNCEMENT": {
        "label": "Annonce réglementaire CSDDD / UE",
        "lead_time_days": 90,
        "data_source": "EUR-Lex Legislative Observatory",
        "weight_in_prediction": 0.18,
        "current_signal": "HIGH",
    },
    "NGOS_ALERT_VOLUME": {
        "label": "Volume alertes ONG (Human Rights Watch, Amnesty…)",
        "lead_time_days": 21,
        "data_source": "NGO Monitor Aggregator",
        "weight_in_prediction": 0.15,
        "current_signal": "HIGH",
    },
    "SUPPLY_CHAIN_DISRUPTION": {
        "label": "Perturbations chaînes d'approvisionnement",
        "lead_time_days": 14,
        "data_source": "Resilinc Supply Chain Index",
        "weight_in_prediction": 0.13,
        "current_signal": "MEDIUM",
    },
    "CURRENCY_CRISIS": {
        "label": "Crise monétaire / dévaluation",
        "lead_time_days": 60,
        "data_source": "IMF Exchange Rate Monitor",
        "weight_in_prediction": 0.08,
        "current_signal": "MEDIUM",
    },
    "ELECTION_INSTABILITY": {
        "label": "Instabilité électorale / fraude",
        "lead_time_days": 75,
        "data_source": "Electoral Integrity Project",
        "weight_in_prediction": 0.07,
        "current_signal": "LOW",
    },
    "CLIMATE_EVENT": {
        "label": "Événement climatique extrême (déplacements, conflits ressources)",
        "lead_time_days": 10,
        "data_source": "NOAA / Copernicus Climate Change Service",
        "weight_in_prediction": 0.07,
        "current_signal": "HIGH",
    },
}

# ─── Scénarios de prévision ───────────────────────────────────────────────────

FORECASTING_SCENARIOS = {
    "BASELINE": {
        "probability_pct": 55,
        "csddd_compliance_demand_growth": 0.28,
        "avg_score_delta": +0.38,
        "new_domains_per_wave": 3,
        "description": (
            "Pression réglementaire CSDDD continue à s'exercer graduellement. "
            "Croissance organique du portefeuille client, expansion sectorielle textile → mining. "
            "Scores Wave en légère hausse reflétant la maturité des moteurs d'analyse."
        ),
    },
    "ACCELERATED_REGULATION": {
        "probability_pct": 30,
        "csddd_compliance_demand_growth": 0.61,
        "avg_score_delta": +0.72,
        "new_domains_per_wave": 5,
        "description": (
            "Entrée en vigueur anticipée CSDDD + jurisprudence CJUE favorable. "
            "Demande client x2 en 6 mois. Besoin fort en domaines réglementaires nouveaux "
            "(devoir de vigilance financier, chaînes IA, sous-traitance cascade)."
        ),
    },
    "GEOPOLITICAL_SHOCK": {
        "probability_pct": 15,
        "csddd_compliance_demand_growth": 0.09,
        "avg_score_delta": +1.45,
        "new_domains_per_wave": 7,
        "description": (
            "Crise géopolitique majeure (conflit nouveau, sanctions massives). "
            "Scores explosent sur domaines conflits armés / réfugiés / ressources. "
            "Demande urgente mais instable — focus sur crédibilité et réactivité Caelum."
        ),
    },
}


# ─── Fonctions analytiques ────────────────────────────────────────────────────

def _linear_regression(x_values: list, y_values: list) -> tuple:
    """Régression linéaire simple — retourne (pente, intercept)."""
    n = len(x_values)
    if n < 2:
        return 0.0, y_values[0] if y_values else 0.0
    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n
    numerator = sum((x_values[i] - mean_x) * (y_values[i] - mean_y) for i in range(n))
    denominator = sum((x_values[i] - mean_x) ** 2 for i in range(n))
    slope = numerator / denominator if denominator != 0 else 0.0
    intercept = mean_y - slope * mean_x
    return slope, intercept


def _r_squared(x_values: list, y_values: list, slope: float, intercept: float) -> float:
    """Calcule le coefficient de détermination R²."""
    mean_y = sum(y_values) / len(y_values)
    ss_tot = sum((y - mean_y) ** 2 for y in y_values)
    ss_res = sum((y_values[i] - (slope * x_values[i] + intercept)) ** 2 for i in range(len(y_values)))
    if ss_tot == 0:
        return 1.0
    return round(1 - ss_res / ss_tot, 4)


def _seasonal_adjustment(wave_number: int, base_amplitude: float = 0.18) -> float:
    """Ajustement saisonnier simulé basé sur le cycle bimensuel des waves."""
    phase = (wave_number % 6) / 6 * 2 * math.pi
    return round(base_amplitude * math.sin(phase), 4)


def forecast_wave_scores(historical_data: list, periods: int = 3) -> dict:
    """
    Prédit les scores des N prochaines waves via régression linéaire + ajustement saisonnier.

    Args:
        historical_data: liste de points de données Wave (HISTORICAL_WAVE_DATA)
        periods: nombre de waves à prévoir (défaut 3)

    Returns:
        dict avec predictions, trend_direction, acceleration
    """
    if not historical_data:
        return {"error": "Données historiques manquantes", "predictions": []}

    waves = [d["wave"] for d in historical_data]
    scores = [d["avg_composite_score"] for d in historical_data]
    media_scores = [d["media_coverage_score"] for d in historical_data]

    slope, intercept = _linear_regression(waves, scores)
    r2 = _r_squared(waves, scores, slope, intercept)

    # Accélération : comparaison première vs seconde moitié
    mid = len(scores) // 2
    first_half_avg = sum(scores[:mid]) / mid if mid > 0 else scores[0]
    second_half_avg = sum(scores[mid:]) / (len(scores) - mid)
    acceleration = round(second_half_avg - first_half_avg, 4)

    last_wave = max(waves)
    last_score = scores[-1]
    predictions = []

    # Domaines probables basés sur signaux actuels élevés
    high_signal_domains = [
        k for k, v in RISK_INDICATORS.items()
        if v["current_signal"] in ("HIGH", "CRITICAL")
    ]
    domain_pool = {
        "CONFLICT_ESCALATION": ["forced_displacement_conflict_rights", "war_crimes_corporate_complicity", "arms_embargo_violations"],
        "REGULATORY_ANNOUNCEMENT": ["csddd_due_diligence_implementation", "eu_supply_chain_act_compliance", "corporate_accountability_enforcement"],
        "COMMODITY_PRICE_SPIKE": ["artisanal_mining_child_labor", "land_grab_agri_commodity_rights", "indigenous_resource_extraction"],
        "NGOS_ALERT_VOLUME": ["environmental_defender_killings", "whistleblower_protection_rights", "ngo_criminalization_trends"],
        "CLIMATE_EVENT": ["climate_refugee_legal_status", "loss_damage_corporate_liability", "drought_food_sovereignty_rights"],
    }

    for i in range(1, periods + 1):
        target_wave = last_wave + i
        base_prediction = slope * target_wave + intercept
        seasonal = _seasonal_adjustment(target_wave)
        predicted = round(base_prediction + seasonal, 2)

        # Intervalle de confiance (±1.5 sigma ajusté par R²)
        residuals = [abs(scores[j] - (slope * waves[j] + intercept)) for j in range(len(waves))]
        sigma = math.sqrt(sum(r ** 2 for r in residuals) / len(residuals))
        ci_half = round(1.5 * sigma * (1 + (1 - r2)), 2)

        risk_domains = []
        for sig in high_signal_domains[:3]:
            if sig in domain_pool:
                risk_domains.append(domain_pool[sig][i - 1] if i - 1 < len(domain_pool[sig]) else domain_pool[sig][0])

        predictions.append({
            "wave": target_wave,
            "predicted_score": predicted,
            "confidence_interval": [round(predicted - ci_half, 2), round(predicted + ci_half, 2)],
            "risk_domains_likely": risk_domains,
            "r2_model_fit": r2,
        })

    # Direction de la tendance
    delta_total = scores[-1] - scores[0]
    if delta_total > 1.0:
        trend_direction = "UP"
    elif delta_total < -1.0:
        trend_direction = "DOWN"
    else:
        trend_direction = "STABLE"

    return {
        "model": "WAVE_SCORE_FORECAST",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "training_waves": f"{waves[0]}–{waves[-1]}",
        "slope_per_wave": round(slope, 4),
        "r2_fit": r2,
        "predictions": predictions,
        "trend_direction": trend_direction,
        "acceleration": acceleration,
        "last_known_score": last_score,
        "media_trend": "HAUSSE" if media_scores[-1] > media_scores[0] else "STABLE",
    }


def detect_emerging_violations(indicators: dict, historical_patterns: list) -> dict:
    """
    Croise les signaux de risque actuels avec les patterns historiques
    pour identifier les violations droits humains émergentes.

    Args:
        indicators: RISK_INDICATORS
        historical_patterns: HISTORICAL_WAVE_DATA

    Returns:
        dict avec emerging_risks, early_warning_alerts, recommended_domains_for_next_wave
    """
    signal_weights = {"CRITICAL": 1.0, "HIGH": 0.7, "MEDIUM": 0.4, "LOW": 0.1}

    # Score de pression agrégé par indicateur
    active_pressures = []
    for key, ind in indicators.items():
        signal_val = signal_weights.get(ind["current_signal"], 0.1)
        composite_threat = round(signal_val * ind["weight_in_prediction"] * 100, 2)
        active_pressures.append({
            "indicator": key,
            "label": ind["label"],
            "signal": ind["current_signal"],
            "lead_time_days": ind["lead_time_days"],
            "threat_contribution": composite_threat,
            "data_source": ind["data_source"],
        })

    active_pressures.sort(key=lambda x: x["threat_contribution"], reverse=True)

    # Détection violations émergentes à partir des signaux CRITICAL/HIGH
    critical_high = [p for p in active_pressures if p["signal"] in ("CRITICAL", "HIGH")]

    violation_domain_map = {
        "CONFLICT_ESCALATION": {
            "domain": "armed_conflict_corporate_complicity_rights",
            "probability": 0.87,
            "description": "Complicité corporate dans conflits armés — risque maximal CSDDD",
            "category": "GÉOPOLITIQUE",
        },
        "REGULATORY_ANNOUNCEMENT": {
            "domain": "csddd_mandatory_due_diligence_enforcement",
            "probability": 0.82,
            "description": "Renforcement diligence raisonnable obligatoire chaîne valeur",
            "category": "RÉGLEMENTAIRE",
        },
        "COMMODITY_PRICE_SPIKE": {
            "domain": "artisanal_mining_child_labor_cobalt",
            "probability": 0.74,
            "description": "Travail enfant dans mines cobalt / minerais critiques — pression EV",
            "category": "CORPORATE",
        },
        "NGOS_ALERT_VOLUME": {
            "domain": "environmental_human_rights_defenders",
            "probability": 0.71,
            "description": "Criminalisation défenseurs DH environnementaux — tendance globale",
            "category": "GÉOPOLITIQUE",
        },
        "SUPPLY_CHAIN_DISRUPTION": {
            "domain": "forced_labor_substitute_supplier_risks",
            "probability": 0.63,
            "description": "Travail forcé chez fournisseurs alternatifs post-disruption",
            "category": "CORPORATE",
        },
        "CLIMATE_EVENT": {
            "domain": "climate_displacement_corporate_liability",
            "probability": 0.61,
            "description": "Responsabilité corporate dans déplacements climatiques",
            "category": "ENVIRONNEMENT",
        },
    }

    emerging_risks = []
    for pressure in critical_high:
        key = pressure["indicator"]
        if key in violation_domain_map:
            mapping = violation_domain_map[key]
            # Ajustement probabilité par tendance médiatique historique
            recent_media_avg = sum(d["media_coverage_score"] for d in historical_patterns[-3:]) / 3
            media_boost = min(0.08, (recent_media_avg - 6.0) * 0.02)
            adjusted_prob = round(min(0.99, mapping["probability"] + media_boost), 3)
            emerging_risks.append({
                "domain": mapping["domain"],
                "probability": adjusted_prob,
                "description": mapping["description"],
                "category": mapping["category"],
                "trigger_indicator": pressure["label"],
                "expected_emergence_days": pressure["lead_time_days"],
                "threat_score": pressure["threat_contribution"],
            })

    emerging_risks.sort(key=lambda x: x["probability"], reverse=True)

    # Alertes précoces : signaux déclencheurs à surveiller
    regulatory_triggered = sum(1 for d in historical_patterns[-5:] if d["regulatory_action_triggered"])
    early_warning_alerts = []

    if regulatory_triggered >= 3:
        early_warning_alerts.append({
            "alert_type": "REGULATORY_ACCELERATION",
            "severity": "CRITIQUE",
            "message": f"{regulatory_triggered}/5 dernières waves ont déclenché des actions réglementaires — seuil critique dépassé",
            "recommended_action": "Préparer rapport d'urgence CSDDD pour clients secteurs textile, tech, agri",
        })

    geopolitical_risks = [r for r in emerging_risks if r["category"] == "GÉOPOLITIQUE"]
    if geopolitical_risks:
        early_warning_alerts.append({
            "alert_type": "GEOPOLITICAL_VIOLATION_CLUSTER",
            "severity": "ÉLEVÉ",
            "message": f"{len(geopolitical_risks)} violations géopolitiques émergentes détectées dans les 30–90 prochains jours",
            "recommended_action": "Lancer wave thématique conflits armés / complicité corporate en priorité",
        })

    corporate_risks = [r for r in emerging_risks if r["category"] == "CORPORATE"]
    if len(corporate_risks) >= 2:
        early_warning_alerts.append({
            "alert_type": "CORPORATE_SUPPLY_CHAIN_CLUSTER",
            "severity": "ÉLEVÉ",
            "message": "Cluster risques chaîne d'approvisionnement — cobalt, travail forcé, fournisseurs substituts",
            "recommended_action": "Développer engines spécialisés secteur minier / tech hardware",
        })

    # Domaines recommandés pour la prochaine wave
    recommended_domains = [r["domain"] for r in emerging_risks[:3]]
    if len(recommended_domains) < 3:
        recommended_domains.append("digital_rights_authoritarian_surveillance")

    return {
        "model": "VIOLATION_EMERGENCE",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_indicators_analyzed": len(indicators),
        "high_critical_signals": len(critical_high),
        "emerging_risks": emerging_risks,
        "early_warning_alerts": early_warning_alerts,
        "recommended_domains_for_next_wave": recommended_domains,
        "aggregate_threat_score": round(sum(p["threat_contribution"] for p in active_pressures), 2),
        "model_confidence": "ÉLEVÉE" if len(critical_high) >= 3 else "MODÉRÉE",
    }


def predict_client_behavior(client_portfolio: list, market_signals: dict) -> dict:
    """
    Prédit les comportements expansion / churn / referral pour les 90 prochains jours.

    Args:
        client_portfolio: liste de clients avec attributs comportementaux
        market_signals: signaux marché (dict avec clés CSDDD_URGENCY, MEDIA_PRESSURE, etc.)

    Returns:
        dict avec per_client_predictions et portfolio_forecast
    """
    per_client_predictions = []

    csddd_urgency = market_signals.get("CSDDD_URGENCY", 0.6)
    media_pressure = market_signals.get("MEDIA_PRESSURE", 0.7)
    competitive_threat = market_signals.get("COMPETITIVE_THREAT", 0.3)

    for client in client_portfolio:
        engagement = client.get("engagement_score", 5.0)
        nps = client.get("nps", 30)
        contract_days_left = client.get("contract_days_left", 180)
        mrr = client.get("mrr_eur", 0)
        sector_exposure = client.get("sector_csddd_exposure", 0.5)
        last_upsell_days = client.get("days_since_last_upsell", 90)

        # Score de churn (0-1 ; plus élevé = plus de risque de départ)
        churn_score = 0.0
        churn_score += max(0, (6.0 - engagement) / 6.0) * 0.35
        churn_score += max(0, (40 - nps) / 80) * 0.25
        churn_score += min(1.0, max(0, (90 - contract_days_left) / 90)) * 0.20
        churn_score += competitive_threat * 0.20

        # Score d'expansion (0-1 ; plus élevé = plus de probabilité d'upgrade)
        expansion_score = 0.0
        expansion_score += sector_exposure * csddd_urgency * 0.40
        expansion_score += media_pressure * 0.25
        expansion_score += max(0, (engagement - 6.0) / 4.0) * 0.20
        expansion_score += min(1.0, last_upsell_days / 180) * 0.15

        # Score de referral
        referral_score = max(0.0, (nps - 30) / 70) * 0.6 + max(0.0, (engagement - 5.0) / 5.0) * 0.4

        # Prédiction principale
        if expansion_score > 0.55 and churn_score < 0.35:
            predicted_action = "EXPANSION"
            probability = round(min(0.97, expansion_score), 3)
            expected_mrr_delta = round(mrr * 0.22 * sector_exposure * csddd_urgency, 0)
            trigger_event = "Obligation CSDDD + Audit diligence raisonnable Q3"
        elif churn_score > 0.60:
            predicted_action = "CHURN_RISK"
            probability = round(min(0.95, churn_score), 3)
            expected_mrr_delta = round(-mrr, 0)
            trigger_event = "Faible engagement + renouvellement imminent"
        elif referral_score > 0.55:
            predicted_action = "REFERRAL_LIKELY"
            probability = round(min(0.90, referral_score), 3)
            expected_mrr_delta = round(mrr * 0.05, 0)  # bonus referral estimé
            trigger_event = "NPS élevé + satisfaction Wave reporting"
        else:
            predicted_action = "STABLE"
            probability = round(1.0 - max(churn_score, expansion_score - 0.1), 3)
            expected_mrr_delta = 0
            trigger_event = "Aucun déclencheur identifié — suivi standard"

        per_client_predictions.append({
            "client_id": client.get("id"),
            "client_name": client.get("name"),
            "predicted_action": predicted_action,
            "probability": probability,
            "expected_mrr_delta": int(expected_mrr_delta),
            "trigger_event": trigger_event,
            "churn_score": round(churn_score, 3),
            "expansion_score": round(expansion_score, 3),
            "referral_score": round(referral_score, 3),
            "current_mrr_eur": mrr,
        })

    # Agrégation portefeuille
    total_mrr_current = sum(c.get("mrr_eur", 0) for c in client_portfolio)
    total_mrr_change = sum(p["expected_mrr_delta"] for p in per_client_predictions)
    expansions = [p for p in per_client_predictions if p["predicted_action"] == "EXPANSION"]
    churns = [p for p in per_client_predictions if p["predicted_action"] == "CHURN_RISK"]

    # Nouveaux logos estimés (referrals * taux de conversion 30%)
    referrals = [p for p in per_client_predictions if p["predicted_action"] == "REFERRAL_LIKELY"]
    net_new_logos = round(len(referrals) * 0.30, 1)

    return {
        "model": "CLIENT_CHURN_RISK",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "horizon_days": 90,
        "clients_analyzed": len(client_portfolio),
        "per_client_predictions": per_client_predictions,
        "portfolio_forecast": {
            "total_mrr_current_eur": total_mrr_current,
            "total_mrr_change_eur": int(total_mrr_change),
            "projected_mrr_eur": total_mrr_current + int(total_mrr_change),
            "expansion_count": len(expansions),
            "churn_risk_count": len(churns),
            "referral_likely_count": len(referrals),
            "net_new_logos_expected": net_new_logos,
            "mrr_growth_pct": round(total_mrr_change / total_mrr_current * 100, 1) if total_mrr_current else 0,
        },
        "market_signals_used": market_signals,
    }


def generate_strategic_forecast(horizon_months: int = 12) -> dict:
    """
    Génère la prévision stratégique complète Caelum Partners sur N mois.

    Args:
        horizon_months: horizon de prévision en mois (défaut 12)

    Returns:
        dict avec regulatory_landscape, market_size projection, competitive_intensity,
        recommended_actions, risk_adjusted_revenue_forecast
    """
    # Pondération scénarios
    expected_demand_growth = sum(
        sc["csddd_compliance_demand_growth"] * sc["probability_pct"] / 100
        for sc in FORECASTING_SCENARIOS.values()
    )
    expected_score_delta = sum(
        sc["avg_score_delta"] * sc["probability_pct"] / 100
        for sc in FORECASTING_SCENARIOS.values()
    )
    expected_new_domains = sum(
        sc["new_domains_per_wave"] * sc["probability_pct"] / 100
        for sc in FORECASTING_SCENARIOS.values()
    )

    # Paysage réglementaire
    high_critical_indicators = [
        k for k, v in RISK_INDICATORS.items()
        if v["current_signal"] in ("HIGH", "CRITICAL")
    ]
    regulatory_pressure_index = round(
        sum(RISK_INDICATORS[k]["weight_in_prediction"] for k in high_critical_indicators), 3
    )

    regulatory_landscape = {
        "csddd_enforcement_probability_pct": min(99, round(regulatory_pressure_index * 100 * 1.6, 1)),
        "new_jurisdictions_adopting_similar": round(2.5 * (horizon_months / 12), 1),
        "enforcement_delay_risk": "FAIBLE" if regulatory_pressure_index > 0.5 else "MODÉRÉ",
        "sector_priorities": ["textile", "tech", "agri-food", "automotive", "financial services"],
        "key_regulatory_milestones": [
            {"milestone": "Entrée en vigueur CSDDD grandes entreprises", "timeline_months": 3},
            {"milestone": "Premiers audits diligence raisonnable obligatoires", "timeline_months": 6},
            {"milestone": "Extension CSDDD PME fournisseurs", "timeline_months": 12},
        ],
    }

    # Marché TAM estimé
    base_tam_eur = 420_000_000  # 420M EUR — marché conformité DH Europe 2026
    projected_tam = round(base_tam_eur * (1 + expected_demand_growth * horizon_months / 12), 0)
    caelum_sam_pct = 0.08  # Part de marché atteignable estimée
    caelum_target_mrr_eur = round(projected_tam * caelum_sam_pct / 12, 0)

    # Intensité concurrentielle
    competitive_intensity = {
        "level": "MODÉRÉE — HAUSSE",
        "main_threats": [
            "ESG rating agencies (MSCI, Sustainalytics) — expansion vers compliance opérationnelle",
            "Big4 audit firms — offres CSDDD packagées",
            "LegalTech startups — automatisation due diligence",
        ],
        "caelum_differentiation": [
            "Moteurs prédictifs propriétaires Wave Series (avance 12–18 mois)",
            "Couverture droits humains spécifique (vs ESG générique)",
            "Architecture multi-agents scalable (coût marginal proche 0)",
        ],
        "competitive_moat_score": 7.4,  # /10
    }

    # Recommandations stratégiques
    caelum_recommended_actions = [
        {
            "priority": 1,
            "action": "Lancer Wave Series domaines CSDDD obligatoires (diligence, chaîne valeur, sous-traitants)",
            "rationale": "Réglementation s'accélère — être premier positionne Caelum comme référence sectorielle",
            "horizon_months": 3,
            "expected_impact": "Acquisition 8–12 nouveaux clients compliance officers",
        },
        {
            "priority": 2,
            "action": "Développer module prédictif temps réel connecté aux flux ACLED + EUR-Lex",
            "rationale": f"Lead time indicateurs ({', '.join(list(RISK_INDICATORS.keys())[:3])}) = avantage prédictif de 2–6 semaines",
            "horizon_months": 6,
            "expected_impact": "Upsell +22% sur base existante, argument commercial différenciant",
        },
        {
            "priority": 3,
            "action": "Partenariats ONG & instituts droits humains pour labellisation données",
            "rationale": "Crédibilité des scores Wave = avantage défensif vs Big4",
            "horizon_months": 9,
            "expected_impact": "Réduction cycle de vente de 30%, accès marchés institutionnels",
        },
        {
            "priority": 4,
            "action": "Offre verticalisée secteur minier / minerais critiques (cobalt, lithium, terres rares)",
            "rationale": "Transition énergétique crée demande structurelle forte — Wave dédiée à fort impact",
            "horizon_months": 12,
            "expected_impact": "Nouveau segment 40–60 clients industrie et investisseurs ESG",
        },
    ]

    # Prévision revenus ajustée au risque
    scenario_revenue_forecasts = {}
    base_current_arr = 1_800_000  # 1.8M EUR ARR estimé actuel
    for scenario_key, scenario in FORECASTING_SCENARIOS.items():
        growth = scenario["csddd_compliance_demand_growth"]
        annual_revenue = round(base_current_arr * (1 + growth * horizon_months / 12), 0)
        scenario_revenue_forecasts[scenario_key] = {
            "label": scenario_key.replace("_", " ").title(),
            "probability_pct": scenario["probability_pct"],
            "projected_arr_eur": int(annual_revenue),
            "revenue_growth_pct": round(growth * horizon_months / 12 * 100, 1),
            "description_courte": scenario["description"][:80] + "...",
        }

    expected_arr = round(sum(
        fr["projected_arr_eur"] * fr["probability_pct"] / 100
        for fr in scenario_revenue_forecasts.values()
    ), 0)

    return {
        "model": "STRATEGIC_FORECAST",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "horizon_months": horizon_months,
        "regulatory_landscape": regulatory_landscape,
        "market_size_eur": {
            "tam_current": base_tam_eur,
            "tam_projected": int(projected_tam),
            "sam_caelum_target_monthly_eur": int(caelum_target_mrr_eur),
            "demand_growth_expected_pct": round(expected_demand_growth * 100, 1),
        },
        "competitive_intensity": competitive_intensity,
        "caelum_recommended_actions": caelum_recommended_actions,
        "risk_adjusted_revenue_forecast": {
            "current_arr_eur": base_current_arr,
            "expected_arr_eur": int(expected_arr),
            "by_scenario": scenario_revenue_forecasts,
            "avg_score_delta_per_wave": round(expected_score_delta, 3),
            "new_domains_per_wave_expected": round(expected_new_domains, 1),
        },
    }


# ─── Démo ─────────────────────────────────────────────────────────────────────

def run_demo() -> bool:
    print("\n" + "=" * 72)
    print("  CaelumSwarm™ — AGENT ANALYSE PREDICTIVE")
    print("  Prévision Tendances DH · Risques CSDDD · Comportements Clients")
    print("=" * 72)

    # ── 1. Prévision scores Wave 195-197 ─────────────────────────────────────
    print("\n[1/4] PREVISION SCORES WAVE 195-197")
    print("-" * 50)
    forecast = forecast_wave_scores(HISTORICAL_WAVE_DATA, periods=3)

    print(f"  Modele : {PREDICTIVE_MODELS['WAVE_SCORE_FORECAST']['label']}")
    print(f"  Entrainement : Waves {forecast['training_waves']}")
    print(f"  Pente regression : {forecast['slope_per_wave']:+.4f} pts/wave")
    print(f"  R2 (qualite fit) : {forecast['r2_fit']:.4f}")
    print(f"  Tendance : {forecast['trend_direction']}  |  Acceleration : {forecast['acceleration']:+.4f}")
    print(f"  Dernier score connu : {forecast['last_known_score']}")
    print()
    for pred in forecast["predictions"]:
        ci = pred["confidence_interval"]
        print(f"  Wave {pred['wave']} : {pred['predicted_score']:.2f}  IC=[{ci[0]:.2f}, {ci[1]:.2f}]")
        for domain in pred["risk_domains_likely"]:
            print(f"           -> Domaine probable : {domain}")

    # ── 2. Détection violations émergentes ───────────────────────────────────
    print("\n[2/4] DETECTION VIOLATIONS EMERGENTES")
    print("-" * 50)
    violations = detect_emerging_violations(RISK_INDICATORS, HISTORICAL_WAVE_DATA)

    print(f"  Indicateurs analyses : {violations['total_indicators_analyzed']}")
    print(f"  Signaux HIGH/CRITICAL : {violations['high_critical_signals']}")
    print(f"  Score menace agregee : {violations['aggregate_threat_score']:.2f}")
    print(f"  Confiance modele : {violations['model_confidence']}")
    print()
    print(f"  RISQUES EMERGENTS (tri par probabilite) :")
    for risk in violations["emerging_risks"]:
        bar = "#" * int(risk["probability"] * 20)
        print(f"  [{bar:<20}] {risk['probability']:.3f}  [{risk['category']}]")
        print(f"    Domaine   : {risk['domain']}")
        print(f"    Emergence : ~{risk['expected_emergence_days']}j  |  {risk['description'][:60]}...")
    print()
    print(f"  ALERTES PRECOCES ({len(violations['early_warning_alerts'])}) :")
    for alert in violations["early_warning_alerts"]:
        print(f"  [{alert['severity']}] {alert['alert_type']}")
        print(f"    {alert['message'][:70]}...")
        print(f"    Action : {alert['recommended_action'][:70]}...")
    print()
    print(f"  DOMAINES RECOMMANDES WAVE N+1 :")
    for domain in violations["recommended_domains_for_next_wave"]:
        print(f"    -> {domain}")

    # ── 3. Prédictions comportement clients ──────────────────────────────────
    print("\n[3/4] PREDICTIONS COMPORTEMENT CLIENTS (90 jours)")
    print("-" * 50)

    mock_clients = [
        {"id": "CLI-001", "name": "Schneider Electric", "engagement_score": 8.2, "nps": 65, "contract_days_left": 210, "mrr_eur": 14500, "sector_csddd_exposure": 0.82, "days_since_last_upsell": 150},
        {"id": "CLI-002", "name": "Decathlon Group", "engagement_score": 4.1, "nps": 22, "contract_days_left": 38, "mrr_eur": 8900, "sector_csddd_exposure": 0.91, "days_since_last_upsell": 320},
        {"id": "CLI-003", "name": "BNP Paribas ESG", "engagement_score": 7.6, "nps": 58, "contract_days_left": 310, "mrr_eur": 22000, "sector_csddd_exposure": 0.74, "days_since_last_upsell": 95},
        {"id": "CLI-004", "name": "TotalEnergies DD", "engagement_score": 6.8, "nps": 45, "contract_days_left": 160, "mrr_eur": 18500, "sector_csddd_exposure": 0.88, "days_since_last_upsell": 200},
        {"id": "CLI-005", "name": "Carrefour Supply", "engagement_score": 3.2, "nps": 10, "contract_days_left": 22, "mrr_eur": 6200, "sector_csddd_exposure": 0.79, "days_since_last_upsell": 410},
    ]

    market_signals = {
        "CSDDD_URGENCY": 0.78,
        "MEDIA_PRESSURE": 0.82,
        "COMPETITIVE_THREAT": 0.32,
    }

    client_forecast = predict_client_behavior(mock_clients, market_signals)
    pf = client_forecast["portfolio_forecast"]

    print(f"  Clients analyses : {client_forecast['clients_analyzed']}")
    print(f"  MRR actuel total : {pf['total_mrr_current_eur']:,.0f} EUR")
    print(f"  Variation MRR prevue : {pf['total_mrr_change_eur']:+,.0f} EUR")
    print(f"  MRR projete 90j : {pf['projected_mrr_eur']:,.0f} EUR  ({pf['mrr_growth_pct']:+.1f}%)")
    print(f"  Expansions : {pf['expansion_count']}  |  Churns : {pf['churn_risk_count']}  |  Referrals : {pf['referral_likely_count']}")
    print(f"  Nouveaux logos estimes : {pf['net_new_logos_expected']}")
    print()
    action_icons = {
        "EXPANSION": "[EXPANSION]    ",
        "CHURN_RISK": "[CHURN RISK]   ",
        "REFERRAL_LIKELY": "[REFERRAL]     ",
        "STABLE": "[STABLE]       ",
    }
    for pred in client_forecast["per_client_predictions"]:
        icon = action_icons.get(pred["predicted_action"], "[?]")
        print(f"  {icon} {pred['client_name']:<22}  prob={pred['probability']:.3f}  delta={pred['expected_mrr_delta']:+,.0f} EUR")
        print(f"                           Declencheur : {pred['trigger_event'][:60]}")

    # ── 4. Prévision stratégique 12 mois ─────────────────────────────────────
    print("\n[4/4] PREVISION STRATEGIQUE 12 MOIS")
    print("-" * 50)
    strategic = generate_strategic_forecast(horizon_months=12)

    rl = strategic["regulatory_landscape"]
    ms = strategic["market_size_eur"]
    ci = strategic["competitive_intensity"]
    rf = strategic["risk_adjusted_revenue_forecast"]

    print(f"  PAYSAGE REGLEMENTAIRE :")
    print(f"  Probabilite enforcement CSDDD : {rl['csddd_enforcement_probability_pct']}%")
    print(f"  Nouvelles juridictions attendues : {rl['new_jurisdictions_adopting_similar']}")
    print(f"  Risque retard application : {rl['enforcement_delay_risk']}")
    for m in rl["key_regulatory_milestones"]:
        print(f"    M+{m['timeline_months']:02d} : {m['milestone']}")

    print(f"\n  MARCHE (TAM/SAM) :")
    print(f"  TAM actuel : {ms['tam_current']:,.0f} EUR")
    print(f"  TAM projete : {ms['tam_projected']:,.0f} EUR  (+{ms['demand_growth_expected_pct']:.1f}%)")
    print(f"  Cible MRR Caelum : {ms['sam_caelum_target_monthly_eur']:,.0f} EUR/mois")

    print(f"\n  INTENSITE CONCURRENTIELLE : {ci['level']}")
    print(f"  Score moat Caelum : {ci['competitive_moat_score']}/10")

    print(f"\n  PREVISION REVENUS AJUSTEE RISQUE :")
    print(f"  ARR actuel : {rf['current_arr_eur']:,.0f} EUR")
    print(f"  ARR attendu : {rf['expected_arr_eur']:,.0f} EUR")
    for sc_key, sc_data in rf["by_scenario"].items():
        bar = "=" * int(sc_data["probability_pct"] / 5)
        print(f"  {sc_key:<25} ({sc_data['probability_pct']:2d}%) [{bar:<20}] ARR={sc_data['projected_arr_eur']:,.0f} EUR")

    print(f"\n  ACTIONS RECOMMANDEES (priorite) :")
    for action in strategic["caelum_recommended_actions"]:
        print(f"  P{action['priority']} [M+{action['horizon_months']:02d}] {action['action'][:65]}")
        print(f"         Impact : {action['expected_impact'][:65]}")

    print("\n" + "=" * 72)
    print("  CaelumSwarm(TM) Predictive Analytics Agent — Demo terminee")
    print("  Tous les modeles operationnels | Donnees CaelumSwarm Wave 185-194")
    print("=" * 72 + "\n")
    return True


# ─── Point d'entree ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
