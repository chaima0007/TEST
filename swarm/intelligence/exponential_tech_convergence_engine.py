"""
Module 291 — Exponential Technology Convergence & Disruption Anticipation Engine
Caelum Partners — Chaima Mhadbi, Bruxelles
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ExponentialTechInput:
    entity_id: str
    tech_cluster: str
    region: str
    ai_capability_acceleration: float
    quantum_computing_readiness: float
    biotech_convergence_rate: float
    nanotech_integration: float
    robotics_autonomy_level: float
    energy_transition_speed: float
    network_effect_multiplier: float
    disruption_velocity: float
    incumbent_displacement_rate: float
    regulatory_adaptation_lag: float
    talent_concentration: float
    innovation_inequality: float
    platform_dominance_risk: float
    open_source_disruption: float
    exponential_blind_spot: float
    technology_sovereignty_gap: float
    adoption_curve_inflection: float


@dataclass
class ExponentialTechResult:
    entity_id: str
    region: str
    tech_cluster: str
    disruption_risk: str
    disruption_pattern: str
    disruption_severity: str
    recommended_action: str
    acceleration_score: float
    displacement_score: float
    concentration_score: float
    sovereignty_score: float
    disruption_composite: float
    is_in_disruption_crisis: bool
    requires_disruption_intervention: bool
    disruption_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "tech_cluster": self.tech_cluster,
            "disruption_risk": self.disruption_risk,
            "disruption_pattern": self.disruption_pattern,
            "disruption_severity": self.disruption_severity,
            "recommended_action": self.recommended_action,
            "acceleration_score": self.acceleration_score,
            "displacement_score": self.displacement_score,
            "concentration_score": self.concentration_score,
            "sovereignty_score": self.sovereignty_score,
            "disruption_composite": self.disruption_composite,
            "is_in_disruption_crisis": self.is_in_disruption_crisis,
            "requires_disruption_intervention": self.requires_disruption_intervention,
            "disruption_signal": self.disruption_signal,
        }


def _acceleration_score(inp: ExponentialTechInput) -> float:
    raw = (
        inp.ai_capability_acceleration * 0.35
        + inp.disruption_velocity * 0.35
        + inp.adoption_curve_inflection * 0.30
    )
    return round(raw * 100, 2)


def _displacement_score(inp: ExponentialTechInput) -> float:
    raw = (
        inp.incumbent_displacement_rate * 0.40
        + inp.open_source_disruption * 0.35
        + inp.network_effect_multiplier * 0.25
    )
    return round(raw * 100, 2)


def _concentration_score(inp: ExponentialTechInput) -> float:
    raw = (
        inp.talent_concentration * 0.40
        + inp.platform_dominance_risk * 0.35
        + inp.innovation_inequality * 0.25
    )
    return round(raw * 100, 2)


def _sovereignty_score(inp: ExponentialTechInput) -> float:
    raw = (
        inp.technology_sovereignty_gap * 0.40
        + inp.exponential_blind_spot * 0.35
        + inp.regulatory_adaptation_lag * 0.25
    )
    return round(raw * 100, 2)


def _disruption_composite(acc: float, disp: float, conc: float, sov: float) -> float:
    return round(acc * 0.30 + disp * 0.25 + conc * 0.25 + sov * 0.20, 2)


def _disruption_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _disruption_pattern(inp: ExponentialTechInput) -> str:
    if inp.ai_capability_acceleration >= 0.70 and (inp.quantum_computing_readiness + inp.biotech_convergence_rate) / 2 >= 0.60:
        return "convergence_singularity"
    if inp.incumbent_displacement_rate >= 0.70 and inp.disruption_velocity >= 0.65:
        return "incumbent_collapse"
    if inp.platform_dominance_risk >= 0.70 and inp.talent_concentration >= 0.65:
        return "platform_monopolization"
    if inp.technology_sovereignty_gap >= 0.70 and inp.exponential_blind_spot >= 0.60:
        return "sovereignty_vacuum"
    if inp.innovation_inequality >= 0.70 and inp.regulatory_adaptation_lag >= 0.60:
        return "innovation_inequality_spiral"
    return "none"


def _disruption_severity(composite: float) -> str:
    if composite >= 75:
        return "exponential_rupture"
    if composite >= 50:
        return "high_disruption"
    if composite >= 25:
        return "disruption_developing"
    return "controlled_innovation"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "disruption_emergency_response"
    if risk == "high" and pattern == "convergence_singularity":
        return "singularity_preparedness"
    if risk == "high":
        return "disruption_hedging"
    if risk == "moderate":
        return "tech_monitoring"
    return "no_action"


def _disruption_signal(inp: ExponentialTechInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        return (
            f"Critique — accélération IA {int(inp.ai_capability_acceleration * 100)}%"
            f" — déplacement {int(inp.incumbent_displacement_rate * 100)}%"
            f" — composite {comp_int}"
        )
    if risk == "high":
        return (
            f"Élevé — concentration talentielle {int(inp.talent_concentration * 100)}%"
            f" — vitesse disruption {int(inp.disruption_velocity * 100)}%"
            f" — composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"Modéré — inégalité innovation {int(inp.innovation_inequality * 100)}%"
            f" — composite {comp_int}"
        )
    return "Convergence technologique maîtrisée — souveraineté préservée, disruption anticipée"


def analyze_entity(inp: ExponentialTechInput) -> ExponentialTechResult:
    acc = _acceleration_score(inp)
    disp = _displacement_score(inp)
    conc = _concentration_score(inp)
    sov = _sovereignty_score(inp)
    composite = _disruption_composite(acc, disp, conc, sov)
    risk = _disruption_risk(composite)
    pattern = _disruption_pattern(inp)
    severity = _disruption_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _disruption_signal(inp, risk, composite)

    return ExponentialTechResult(
        entity_id=inp.entity_id,
        region=inp.region,
        tech_cluster=inp.tech_cluster,
        disruption_risk=risk,
        disruption_pattern=pattern,
        disruption_severity=severity,
        recommended_action=action,
        acceleration_score=acc,
        displacement_score=disp,
        concentration_score=conc,
        sovereignty_score=sov,
        disruption_composite=composite,
        is_in_disruption_crisis=composite >= 60,
        requires_disruption_intervention=composite >= 40,
        disruption_signal=signal,
    )


class ExponentialTechConvergenceEngine:
    def __init__(self) -> None:
        self.results: List[ExponentialTechResult] = []

    def process(self, inputs: List[ExponentialTechInput]) -> None:
        self.results = [analyze_entity(inp) for inp in inputs]

    def summary(self) -> Dict[str, Any]:
        n = len(self.results)
        if n == 0:
            return {}

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_acc = 0.0
        total_disp = 0.0
        total_conc = 0.0
        total_sov = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in self.results:
            risk_counts[r.disruption_risk] = risk_counts.get(r.disruption_risk, 0) + 1
            pattern_counts[r.disruption_pattern] = pattern_counts.get(r.disruption_pattern, 0) + 1
            severity_counts[r.disruption_severity] = severity_counts.get(r.disruption_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.disruption_composite
            total_acc += r.acceleration_score
            total_disp += r.displacement_score
            total_conc += r.concentration_score
            total_sov += r.sovereignty_score
            if r.is_in_disruption_crisis:
                crisis_count += 1
            if r.requires_disruption_intervention:
                intervention_count += 1

        avg_composite = round(total_composite / n, 2)

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_disruption_composite": avg_composite,
            "disruption_crisis_count": crisis_count,
            "disruption_intervention_count": intervention_count,
            "avg_acceleration_score": round(total_acc / n, 2),
            "avg_displacement_score": round(total_disp / n, 2),
            "avg_concentration_score": round(total_conc / n, 2),
            "avg_sovereignty_score": round(total_sov / n, 2),
            "avg_estimated_disruption_index": round(avg_composite / 100 * 10, 2),
        }
