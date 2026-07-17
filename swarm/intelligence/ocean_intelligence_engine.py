from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class OceanIntelligenceInput:
    entity_id: str
    ocean_domain: str
    region: str
    ocean_acidification_severity: float
    plastic_pollution_saturation: float
    deep_sea_mining_disruption: float
    maritime_trade_route_vulnerability: float
    illegal_fishing_intensity: float
    coral_reef_collapse_rate: float
    submarine_cable_security_risk: float
    marine_biodiversity_collapse: float
    ocean_heat_content_anomaly: float
    arctic_route_geopolitics: float
    blue_carbon_sequestration_loss: float
    piracy_maritime_crime_index: float
    exclusive_economic_zone_conflict: float
    ocean_sovereignty_dispute_intensity: float
    plastic_microplastic_food_chain: float
    seabed_resource_competition: float
    maritime_surveillance_gap: float


@dataclass
class OceanIntelligenceResult:
    entity_id: str
    region: str
    ocean_domain: str
    ocean_risk: str
    ocean_pattern: str
    ocean_severity: str
    recommended_action: str
    ecological_score: float
    economic_score: float
    security_score: float
    geopolitical_score: float
    ocean_composite: float
    is_ocean_crisis: bool
    requires_ocean_intervention: bool
    ocean_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "ocean_domain": self.ocean_domain,
            "ocean_risk": self.ocean_risk,
            "ocean_pattern": self.ocean_pattern,
            "ocean_severity": self.ocean_severity,
            "recommended_action": self.recommended_action,
            "ecological_score": self.ecological_score,
            "economic_score": self.economic_score,
            "security_score": self.security_score,
            "geopolitical_score": self.geopolitical_score,
            "ocean_composite": self.ocean_composite,
            "is_ocean_crisis": self.is_ocean_crisis,
            "requires_ocean_intervention": self.requires_ocean_intervention,
            "ocean_signal": self.ocean_signal,
        }


def _ecological_score(e: OceanIntelligenceInput) -> float:
    raw = (
        e.ocean_acidification_severity * 0.4
        + e.coral_reef_collapse_rate * 0.35
        + e.marine_biodiversity_collapse * 0.25
    ) * 100
    return round(raw * 100) / 100


def _economic_score(e: OceanIntelligenceInput) -> float:
    raw = (
        e.maritime_trade_route_vulnerability * 0.4
        + e.deep_sea_mining_disruption * 0.35
        + e.illegal_fishing_intensity * 0.25
    ) * 100
    return round(raw * 100) / 100


def _security_score(e: OceanIntelligenceInput) -> float:
    raw = (
        e.submarine_cable_security_risk * 0.4
        + e.piracy_maritime_crime_index * 0.35
        + e.maritime_surveillance_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _geopolitical_score(e: OceanIntelligenceInput) -> float:
    raw = (
        e.ocean_sovereignty_dispute_intensity * 0.4
        + e.exclusive_economic_zone_conflict * 0.35
        + e.seabed_resource_competition * 0.25
    ) * 100
    return round(raw * 100) / 100


def _ocean_composite(
    ecological: float,
    economic: float,
    security: float,
    geopolitical: float,
) -> float:
    return round(
        (ecological * 0.30 + economic * 0.25 + security * 0.25 + geopolitical * 0.20) * 100
    ) / 100


def _ocean_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _ocean_pattern(e: OceanIntelligenceInput) -> str:
    if e.ocean_acidification_severity >= 0.70 and e.coral_reef_collapse_rate >= 0.65:
        return "ecological_ocean_collapse"
    if e.submarine_cable_security_risk >= 0.70 and e.piracy_maritime_crime_index >= 0.65:
        return "maritime_security_crisis"
    if e.maritime_trade_route_vulnerability >= 0.70 and e.deep_sea_mining_disruption >= 0.65:
        return "blue_economy_disruption"
    if e.ocean_sovereignty_dispute_intensity >= 0.70 and e.exclusive_economic_zone_conflict >= 0.65:
        return "ocean_sovereignty_war"
    if e.plastic_pollution_saturation >= 0.70 and e.plastic_microplastic_food_chain >= 0.65:
        return "plastic_collapse"
    return "none"


def _ocean_severity(composite: float) -> str:
    if composite >= 75:
        return "ocean_emergency"
    if composite >= 50:
        return "ocean_crisis"
    if composite >= 25:
        return "ocean_stress"
    return "ocean_stable"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "ocean_emergency_response"
    if risk == "high" and pattern == "maritime_security_crisis":
        return "naval_security_deployment"
    if risk == "high":
        return "ocean_resilience_program"
    if risk == "moderate":
        return "ocean_monitoring"
    return "no_action"


def _ocean_signal(e: OceanIntelligenceInput, risk: str, composite: float) -> str:
    if risk == "critical":
        return (
            f"Critique — acidification océanique {int(e.ocean_acidification_severity * 100)}%"
            f" — effondrement récifs coralliens {int(e.coral_reef_collapse_rate * 100)}%"
            f" — composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — vulnérabilité routes maritimes {int(e.maritime_trade_route_vulnerability * 100)}%"
            f" — risque câbles sous-marins {int(e.submarine_cable_security_risk * 100)}%"
            f" — composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — pollution plastique {int(e.plastic_pollution_saturation * 100)}%"
            f" — composite {int(composite)}"
        )
    return "Océan stable — écosystèmes marins sains, souveraineté maritime préservée"


def analyze_ocean(e: OceanIntelligenceInput) -> OceanIntelligenceResult:
    ecological = _ecological_score(e)
    economic = _economic_score(e)
    security = _security_score(e)
    geopolitical = _geopolitical_score(e)
    composite = _ocean_composite(ecological, economic, security, geopolitical)
    risk = _ocean_risk(composite)
    pattern = _ocean_pattern(e)
    severity = _ocean_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _ocean_signal(e, risk, composite)

    return OceanIntelligenceResult(
        entity_id=e.entity_id,
        region=e.region,
        ocean_domain=e.ocean_domain,
        ocean_risk=risk,
        ocean_pattern=pattern,
        ocean_severity=severity,
        recommended_action=action,
        ecological_score=ecological,
        economic_score=economic,
        security_score=security,
        geopolitical_score=geopolitical,
        ocean_composite=composite,
        is_ocean_crisis=composite >= 60,
        requires_ocean_intervention=composite >= 40,
        ocean_signal=signal,
    )


class OceanIntelligenceEngine:
    def analyze(self, entities: List[OceanIntelligenceInput]) -> Dict[str, Any]:
        results = [analyze_ocean(e) for e in entities]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_ecological = 0.0
        total_economic = 0.0
        total_security = 0.0
        total_geopolitical = 0.0
        total_composite = 0.0
        ocean_crisis_count = 0
        ocean_intervention_count = 0

        for r in results:
            risk_counts[r.ocean_risk] = risk_counts.get(r.ocean_risk, 0) + 1
            pattern_counts[r.ocean_pattern] = pattern_counts.get(r.ocean_pattern, 0) + 1
            severity_counts[r.ocean_severity] = severity_counts.get(r.ocean_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_ecological += r.ecological_score
            total_economic += r.economic_score
            total_security += r.security_score
            total_geopolitical += r.geopolitical_score
            total_composite += r.ocean_composite
            if r.is_ocean_crisis:
                ocean_crisis_count += 1
            if r.requires_ocean_intervention:
                ocean_intervention_count += 1

        n = len(results) or 1
        avg_composite = round(total_composite / n * 10) / 10

        return {
            "total": len(results),
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_ocean_composite": avg_composite,
            "ocean_crisis_count": ocean_crisis_count,
            "ocean_intervention_count": ocean_intervention_count,
            "avg_ecological_score": round(total_ecological / n * 10) / 10,
            "avg_economic_score": round(total_economic / n * 10) / 10,
            "avg_security_score": round(total_security / n * 10) / 10,
            "avg_geopolitical_score": round(total_geopolitical / n * 10) / 10,
            "avg_estimated_ocean_risk_index": round(avg_composite / 100 * 10, 2),
        }
