"""
Climate Tipping Points Intelligence Engine
Module 305 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ClimateTippingInput:
    entity_id: str
    ecosystem_type: str
    region: str
    # 17 float fields (0.0-1.0)
    temperature_anomaly: float
    ice_sheet_loss_rate: float
    permafrost_thaw_index: float
    ocean_acidification_level: float
    methane_release_rate: float
    coral_bleaching_intensity: float
    arctic_sea_ice_decline: float
    amazon_dieback_risk: float
    jet_stream_disruption: float
    monsoon_destabilization: float
    sea_level_rise_velocity: float
    biodiversity_collapse_rate: float
    carbon_feedback_loop: float
    tipping_cascade_risk: float
    albedo_loss_factor: float
    ecosystem_resilience: float  # inverse: high = good
    adaptation_capacity: float   # inverse: high = good


@dataclass
class ClimateTippingResult:
    entity_id: str
    region: str
    ecosystem_type: str
    tipping_risk: str
    tipping_pattern: str
    tipping_severity: str
    recommended_action: str
    thermal_score: float
    ecosystem_score: float
    feedback_score: float
    vulnerability_score: float
    tipping_composite: float
    is_tipping_crisis: bool
    requires_tipping_intervention: bool
    tipping_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "ecosystem_type": self.ecosystem_type,
            "tipping_risk": self.tipping_risk,
            "tipping_pattern": self.tipping_pattern,
            "tipping_severity": self.tipping_severity,
            "recommended_action": self.recommended_action,
            "thermal_score": self.thermal_score,
            "ecosystem_score": self.ecosystem_score,
            "feedback_score": self.feedback_score,
            "vulnerability_score": self.vulnerability_score,
            "tipping_composite": self.tipping_composite,
            "is_tipping_crisis": self.is_tipping_crisis,
            "requires_tipping_intervention": self.requires_tipping_intervention,
            "tipping_signal": self.tipping_signal,
        }


def _thermal_score(inp: ClimateTippingInput) -> float:
    raw = (
        inp.temperature_anomaly * 0.4
        + inp.ice_sheet_loss_rate * 0.35
        + inp.permafrost_thaw_index * 0.25
    ) * 100
    return round(raw * 100) / 100


def _ecosystem_score(inp: ClimateTippingInput) -> float:
    raw = (
        inp.coral_bleaching_intensity * 0.4
        + inp.amazon_dieback_risk * 0.35
        + inp.biodiversity_collapse_rate * 0.25
    ) * 100
    return round(raw * 100) / 100


def _feedback_score(inp: ClimateTippingInput) -> float:
    raw = (
        inp.carbon_feedback_loop * 0.4
        + inp.methane_release_rate * 0.35
        + inp.albedo_loss_factor * 0.25
    ) * 100
    return round(raw * 100) / 100


def _vulnerability_score(inp: ClimateTippingInput) -> float:
    raw = (
        inp.tipping_cascade_risk * 0.4
        + (1 - inp.ecosystem_resilience) * 0.35
        + (1 - inp.adaptation_capacity) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    thermal: float,
    ecosystem: float,
    feedback: float,
    vulnerability: float,
) -> float:
    return round(
        thermal * 0.30
        + ecosystem * 0.25
        + feedback * 0.25
        + vulnerability * 0.20,
        2,
    )


def _tipping_pattern(inp: ClimateTippingInput) -> str:
    if inp.temperature_anomaly >= 0.70 and inp.carbon_feedback_loop >= 0.65:
        return "thermal_runaway"
    if inp.permafrost_thaw_index >= 0.70 and inp.methane_release_rate >= 0.65:
        return "permafrost_collapse"
    if inp.ocean_acidification_level >= 0.70 and inp.coral_bleaching_intensity >= 0.65:
        return "ocean_system_failure"
    if inp.amazon_dieback_risk >= 0.70 and inp.biodiversity_collapse_rate >= 0.60:
        return "biosphere_cascade"
    if inp.arctic_sea_ice_decline >= 0.70 and inp.albedo_loss_factor >= 0.65:
        return "arctic_tipping"
    return "none"


def _tipping_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _tipping_severity(composite: float) -> str:
    if composite >= 75:
        return "planetary_emergency"
    if composite >= 50:
        return "critical_tipping"
    if composite >= 25:
        return "tipping_developing"
    return "ecosystem_stable"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "planetary_emergency_protocol"
    if risk == "high" and pattern == "thermal_runaway":
        return "carbon_emergency_brake"
    if risk == "high":
        return "ecosystem_crisis_response"
    if risk == "moderate":
        return "tipping_monitoring"
    return "no_action"


def _tipping_signal(inp: ClimateTippingInput, risk: str, composite: float) -> str:
    if risk == "critical":
        return (
            f"Critique — anomalie thermique {int(inp.temperature_anomaly * 100)}% "
            f"— risque cascade basculement {int(inp.tipping_cascade_risk * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — dégradation pergélisol {int(inp.permafrost_thaw_index * 100)}% "
            f"— résilience écosystème {int(inp.ecosystem_resilience * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — acidification océan {int(inp.ocean_acidification_level * 100)}% "
            f"— composite {int(composite)}"
        )
    return "Écosystème stable — résilience climatique solide, capacité d'adaptation optimale, aucun point de basculement imminent"


def analyze(inp: ClimateTippingInput) -> ClimateTippingResult:
    thermal = _thermal_score(inp)
    ecosystem = _ecosystem_score(inp)
    feedback = _feedback_score(inp)
    vulnerability = _vulnerability_score(inp)
    comp = _composite(thermal, ecosystem, feedback, vulnerability)
    pat = _tipping_pattern(inp)
    risk = _tipping_risk(comp)
    sev = _tipping_severity(comp)
    action = _recommended_action(risk, pat)
    sig = _tipping_signal(inp, risk, comp)

    return ClimateTippingResult(
        entity_id=inp.entity_id,
        region=inp.region,
        ecosystem_type=inp.ecosystem_type,
        tipping_risk=risk,
        tipping_pattern=pat,
        tipping_severity=sev,
        recommended_action=action,
        thermal_score=thermal,
        ecosystem_score=ecosystem,
        feedback_score=feedback,
        vulnerability_score=vulnerability,
        tipping_composite=comp,
        is_tipping_crisis=comp >= 60,
        requires_tipping_intervention=comp >= 40,
        tipping_signal=sig,
    )


class ClimateTippingPointsEngine:
    def __init__(self, inputs: List[ClimateTippingInput]):
        self.inputs = inputs
        self.results: List[ClimateTippingResult] = [analyze(i) for i in inputs]

    def assess(self, entities: List[ClimateTippingInput]) -> Dict[str, Any]:
        results = [analyze(e) for e in entities]
        n = len(results)
        if n == 0:
            return {}

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_thermal = 0.0
        total_ecosystem = 0.0
        total_feedback = 0.0
        total_vulnerability = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in results:
            risk_counts[r.tipping_risk] = risk_counts.get(r.tipping_risk, 0) + 1
            pattern_counts[r.tipping_pattern] = pattern_counts.get(r.tipping_pattern, 0) + 1
            severity_counts[r.tipping_severity] = severity_counts.get(r.tipping_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1

            total_composite += r.tipping_composite
            total_thermal += r.thermal_score
            total_ecosystem += r.ecosystem_score
            total_feedback += r.feedback_score
            total_vulnerability += r.vulnerability_score

            if r.is_tipping_crisis:
                crisis_count += 1
            if r.requires_tipping_intervention:
                intervention_count += 1

        avg_composite = round(total_composite / n * 10) / 10

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_tipping_composite": avg_composite,
            "tipping_crisis_count": crisis_count,
            "tipping_intervention_count": intervention_count,
            "avg_thermal_score": round(total_thermal / n * 10) / 10,
            "avg_ecosystem_score": round(total_ecosystem / n * 10) / 10,
            "avg_feedback_score": round(total_feedback / n * 10) / 10,
            "avg_vulnerability_score": round(total_vulnerability / n * 10) / 10,
            "avg_estimated_tipping_index": round(avg_composite / 100 * 10, 2),
        }
