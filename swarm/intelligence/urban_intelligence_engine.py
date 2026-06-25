from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class UrbanIntelligenceInput:
    entity_id: str
    city_type: str
    region: str
    surveillance_density: float
    digital_infrastructure_vulnerability: float
    social_control_index: float
    inequality_tension_index: float
    migration_pressure: float
    housing_crisis_index: float
    mobility_gridlock_risk: float
    energy_grid_fragility: float
    water_system_stress: float
    food_supply_resilience: float
    civic_ai_governance_gap: float
    algorithmic_discrimination_risk: float
    smart_city_lock_in: float
    data_extractivism_index: float
    urban_heat_island_intensity: float
    infrastructure_decay_rate: float
    civic_engagement_erosion: float


@dataclass
class UrbanIntelligenceResult:
    entity_id: str
    region: str
    city_type: str
    urban_risk: str
    urban_pattern: str
    urban_severity: str
    recommended_action: str
    surveillance_score: float
    resilience_score: float
    social_score: float
    governance_score: float
    urban_composite: float
    is_urban_crisis: bool
    requires_urban_intervention: bool
    urban_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "city_type": self.city_type,
            "urban_risk": self.urban_risk,
            "urban_pattern": self.urban_pattern,
            "urban_severity": self.urban_severity,
            "recommended_action": self.recommended_action,
            "surveillance_score": self.surveillance_score,
            "resilience_score": self.resilience_score,
            "social_score": self.social_score,
            "governance_score": self.governance_score,
            "urban_composite": self.urban_composite,
            "is_urban_crisis": self.is_urban_crisis,
            "requires_urban_intervention": self.requires_urban_intervention,
            "urban_signal": self.urban_signal,
        }


def _surveillance_score(e: UrbanIntelligenceInput) -> float:
    raw = (
        e.surveillance_density * 0.4
        + e.social_control_index * 0.35
        + e.algorithmic_discrimination_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _resilience_score(e: UrbanIntelligenceInput) -> float:
    raw = (
        e.digital_infrastructure_vulnerability * 0.4
        + e.energy_grid_fragility * 0.35
        + e.water_system_stress * 0.25
    ) * 100
    return round(raw * 100) / 100


def _social_score(e: UrbanIntelligenceInput) -> float:
    raw = (
        e.inequality_tension_index * 0.4
        + e.housing_crisis_index * 0.35
        + e.civic_engagement_erosion * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: UrbanIntelligenceInput) -> float:
    raw = (
        e.civic_ai_governance_gap * 0.4
        + e.smart_city_lock_in * 0.35
        + e.data_extractivism_index * 0.25
    ) * 100
    return round(raw * 100) / 100


def _urban_composite(
    surveillance: float,
    resilience: float,
    social: float,
    governance: float,
) -> float:
    return round(
        (surveillance * 0.30 + resilience * 0.25 + social * 0.25 + governance * 0.20) * 100
    ) / 100


def _urban_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _urban_pattern(e: UrbanIntelligenceInput) -> str:
    if e.surveillance_density >= 0.70 and e.social_control_index >= 0.65:
        return "surveillance_state"
    if e.digital_infrastructure_vulnerability >= 0.70 and e.energy_grid_fragility >= 0.65:
        return "infrastructure_collapse"
    if e.inequality_tension_index >= 0.70 and e.housing_crisis_index >= 0.65:
        return "social_explosion"
    if e.algorithmic_discrimination_risk >= 0.70 and e.civic_ai_governance_gap >= 0.60:
        return "algorithmic_oppression"
    if e.smart_city_lock_in >= 0.70 and e.data_extractivism_index >= 0.65:
        return "smart_city_monopoly"
    return "none"


def _urban_severity(composite: float) -> str:
    if composite >= 75:
        return "urban_emergency"
    if composite >= 50:
        return "high_urban_risk"
    if composite >= 25:
        return "urban_tension"
    return "urban_resilient"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "urban_emergency_intervention"
    if risk == "high" and pattern == "surveillance_state":
        return "civil_liberties_audit"
    if risk == "high":
        return "urban_resilience_program"
    if risk == "moderate":
        return "urban_monitoring"
    return "no_action"


def _urban_signal(e: UrbanIntelligenceInput, risk: str, composite: float) -> str:
    if risk == "critical":
        return (
            f"Critique — densité surveillance {int(e.surveillance_density * 100)}%"
            f" — tension sociale {int(e.inequality_tension_index * 100)}%"
            f" — composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — vulnérabilité infrastructure {int(e.digital_infrastructure_vulnerability * 100)}%"
            f" — écart gouvernance IA {int(e.civic_ai_governance_gap * 100)}%"
            f" — composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — fragmentation urbaine {int(e.housing_crisis_index * 100)}%"
            f" — composite {int(composite)}"
        )
    return "Ville résiliente — gouvernance urbaine saine, cohésion sociale élevée"


def analyze_urban(e: UrbanIntelligenceInput) -> UrbanIntelligenceResult:
    surveillance = _surveillance_score(e)
    resilience = _resilience_score(e)
    social = _social_score(e)
    governance = _governance_score(e)
    composite = _urban_composite(surveillance, resilience, social, governance)
    risk = _urban_risk(composite)
    pattern = _urban_pattern(e)
    severity = _urban_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _urban_signal(e, risk, composite)

    return UrbanIntelligenceResult(
        entity_id=e.entity_id,
        region=e.region,
        city_type=e.city_type,
        urban_risk=risk,
        urban_pattern=pattern,
        urban_severity=severity,
        recommended_action=action,
        surveillance_score=surveillance,
        resilience_score=resilience,
        social_score=social,
        governance_score=governance,
        urban_composite=composite,
        is_urban_crisis=composite >= 60,
        requires_urban_intervention=composite >= 40,
        urban_signal=signal,
    )


class UrbanIntelligenceEngine:
    def analyze(self, entities: List[UrbanIntelligenceInput]) -> Dict[str, Any]:
        results = [analyze_urban(e) for e in entities]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_surveillance = 0.0
        total_resilience = 0.0
        total_social = 0.0
        total_governance = 0.0
        total_composite = 0.0
        urban_crisis_count = 0
        urban_intervention_count = 0

        for r in results:
            risk_counts[r.urban_risk] = risk_counts.get(r.urban_risk, 0) + 1
            pattern_counts[r.urban_pattern] = pattern_counts.get(r.urban_pattern, 0) + 1
            severity_counts[r.urban_severity] = severity_counts.get(r.urban_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_surveillance += r.surveillance_score
            total_resilience += r.resilience_score
            total_social += r.social_score
            total_governance += r.governance_score
            total_composite += r.urban_composite
            if r.is_urban_crisis:
                urban_crisis_count += 1
            if r.requires_urban_intervention:
                urban_intervention_count += 1

        n = len(results) or 1
        avg_composite = round(total_composite / n * 10) / 10

        return {
            "total": len(results),
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_urban_composite": avg_composite,
            "urban_crisis_count": urban_crisis_count,
            "urban_intervention_count": urban_intervention_count,
            "avg_surveillance_score": round(total_surveillance / n * 10) / 10,
            "avg_resilience_score": round(total_resilience / n * 10) / 10,
            "avg_social_score": round(total_social / n * 10) / 10,
            "avg_governance_score": round(total_governance / n * 10) / 10,
            "avg_estimated_urban_risk_index": round(avg_composite / 100 * 10, 2),
        }
