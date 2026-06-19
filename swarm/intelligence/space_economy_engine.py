from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SpaceEconomyInput:
    entity_id: str
    space_segment: str
    region: str
    orbital_asset_concentration: float
    launch_cost_competitiveness: float
    satellite_constellation_density: float
    space_debris_collision_risk: float
    spectrum_congestion: float
    space_sovereignty_gap: float
    launch_vehicle_dependency: float
    ground_infrastructure_resilience: float
    space_weather_vulnerability: float
    commercialization_readiness: float
    space_mining_viability: float
    anti_satellite_threat: float
    orbital_slot_scarcity: float
    space_insurance_gap: float
    regulatory_space_framework: float
    international_cooperation_index: float
    new_space_innovation_rate: float


@dataclass
class SpaceEconomyResult:
    entity_id: str
    region: str
    space_segment: str
    space_risk: str
    space_pattern: str
    space_severity: str
    recommended_action: str
    orbital_score: float
    sovereignty_score: float
    commercial_score: float
    resilience_score: float
    space_composite: float
    is_in_space_crisis: bool
    requires_space_intervention: bool
    space_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "space_segment": self.space_segment,
            "space_risk": self.space_risk,
            "space_pattern": self.space_pattern,
            "space_severity": self.space_severity,
            "recommended_action": self.recommended_action,
            "orbital_score": self.orbital_score,
            "sovereignty_score": self.sovereignty_score,
            "commercial_score": self.commercial_score,
            "resilience_score": self.resilience_score,
            "space_composite": self.space_composite,
            "is_in_space_crisis": self.is_in_space_crisis,
            "requires_space_intervention": self.requires_space_intervention,
            "space_signal": self.space_signal,
        }


def _compute_orbital_score(inp: SpaceEconomyInput) -> float:
    raw = (
        inp.space_debris_collision_risk * 0.4
        + inp.spectrum_congestion * 0.35
        + inp.orbital_slot_scarcity * 0.25
    ) * 100
    return round(raw, 2)


def _compute_sovereignty_score(inp: SpaceEconomyInput) -> float:
    raw = (
        inp.space_sovereignty_gap * 0.4
        + inp.anti_satellite_threat * 0.35
        + inp.launch_vehicle_dependency * 0.25
    ) * 100
    return round(raw, 2)


def _compute_commercial_score(inp: SpaceEconomyInput) -> float:
    raw = (
        (1 - inp.commercialization_readiness) * 0.4
        + (1 - inp.new_space_innovation_rate) * 0.35
        + inp.space_insurance_gap * 0.25
    ) * 100
    return round(raw, 2)


def _compute_resilience_score(inp: SpaceEconomyInput) -> float:
    raw = (
        inp.space_weather_vulnerability * 0.4
        + (1 - inp.ground_infrastructure_resilience) * 0.35
        + inp.orbital_asset_concentration * 0.25
    ) * 100
    return round(raw, 2)


def _compute_composite(orbital: float, sovereignty: float, commercial: float, resilience: float) -> float:
    return round(orbital * 0.30 + sovereignty * 0.25 + commercial * 0.25 + resilience * 0.20, 2)


def _space_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _space_pattern(inp: SpaceEconomyInput) -> str:
    if inp.space_debris_collision_risk >= 0.70 and inp.satellite_constellation_density >= 0.65:
        return "orbital_collision_cascade"
    if inp.space_sovereignty_gap >= 0.70 and inp.anti_satellite_threat >= 0.60:
        return "space_sovereignty_loss"
    if inp.spectrum_congestion >= 0.70 and inp.orbital_slot_scarcity >= 0.65:
        return "spectrum_war"
    if inp.launch_vehicle_dependency >= 0.70 and (1 - inp.launch_cost_competitiveness) >= 0.60:
        return "launch_monopoly"
    if inp.space_weather_vulnerability >= 0.70 and (1 - inp.ground_infrastructure_resilience) >= 0.60:
        return "space_weather_blackout"
    return "none"


def _space_severity(composite: float) -> str:
    if composite >= 75:
        return "orbital_emergency"
    if composite >= 50:
        return "high_space_risk"
    if composite >= 25:
        return "space_stress"
    return "space_optimum"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "space_emergency_protocol"
    if risk == "high" and pattern == "orbital_collision_cascade":
        return "debris_mitigation"
    if risk == "high":
        return "space_resilience_program"
    if risk == "moderate":
        return "space_monitoring"
    return "no_action"


def _space_signal(inp: SpaceEconomyInput, composite: float, risk: str) -> str:
    if risk == "critical":
        return (
            f"Critique — risque collision débris {int(inp.space_debris_collision_risk * 100)}%"
            f" — menace antisatellite {int(inp.anti_satellite_threat * 100)}%"
            f" — composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — congestion spectre {int(inp.spectrum_congestion * 100)}%"
            f" — souveraineté spatiale {100 - int(inp.space_sovereignty_gap * 100)}%"
            f" — composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — vulnérabilité météo spatiale {int(inp.space_weather_vulnerability * 100)}%"
            f" — composite {int(composite)}"
        )
    return "Économie spatiale optimale — infrastructure orbitale sécurisée, souveraineté maintenue"


def analyze_space_entity(inp: SpaceEconomyInput) -> SpaceEconomyResult:
    orbital = _compute_orbital_score(inp)
    sovereignty = _compute_sovereignty_score(inp)
    commercial = _compute_commercial_score(inp)
    resilience = _compute_resilience_score(inp)
    composite = _compute_composite(orbital, sovereignty, commercial, resilience)
    risk = _space_risk(composite)
    pattern = _space_pattern(inp)
    severity = _space_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _space_signal(inp, composite, risk)

    return SpaceEconomyResult(
        entity_id=inp.entity_id,
        region=inp.region,
        space_segment=inp.space_segment,
        space_risk=risk,
        space_pattern=pattern,
        space_severity=severity,
        recommended_action=action,
        orbital_score=orbital,
        sovereignty_score=sovereignty,
        commercial_score=commercial,
        resilience_score=resilience,
        space_composite=composite,
        is_in_space_crisis=composite >= 60,
        requires_space_intervention=composite >= 40,
        space_signal=signal,
    )


class SpaceEconomyEngine:
    def __init__(self, inputs: List[SpaceEconomyInput]):
        self.inputs = inputs
        self.results: List[SpaceEconomyResult] = [analyze_space_entity(inp) for inp in inputs]

    def summary(self) -> Dict[str, Any]:
        n = len(self.results)
        if n == 0:
            return {}

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_orbital = 0.0
        total_sovereignty = 0.0
        total_commercial = 0.0
        total_resilience = 0.0
        space_crisis_count = 0
        space_intervention_count = 0

        for r in self.results:
            risk_counts[r.space_risk] = risk_counts.get(r.space_risk, 0) + 1
            pattern_counts[r.space_pattern] = pattern_counts.get(r.space_pattern, 0) + 1
            severity_counts[r.space_severity] = severity_counts.get(r.space_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.space_composite
            total_orbital += r.orbital_score
            total_sovereignty += r.sovereignty_score
            total_commercial += r.commercial_score
            total_resilience += r.resilience_score
            if r.is_in_space_crisis:
                space_crisis_count += 1
            if r.requires_space_intervention:
                space_intervention_count += 1

        avg_composite = total_composite / n

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_space_composite": round(avg_composite, 1),
            "space_crisis_count": space_crisis_count,
            "space_intervention_count": space_intervention_count,
            "avg_orbital_score": round(total_orbital / n, 1),
            "avg_sovereignty_score": round(total_sovereignty / n, 1),
            "avg_commercial_score": round(total_commercial / n, 1),
            "avg_resilience_score": round(total_resilience / n, 1),
            "avg_estimated_space_risk_index": round(avg_composite / 100 * 10, 2),
        }
