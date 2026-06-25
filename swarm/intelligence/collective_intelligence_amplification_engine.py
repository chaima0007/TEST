from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CollectiveIntelligenceInput:
    entity_id: str
    aggregation_method: str
    region: str
    crowd_accuracy_rate: float
    diversity_of_perspective: float
    independence_of_judgment: float
    aggregation_mechanism_quality: float
    information_cascade_risk: float
    groupthink_susceptibility: float
    echo_chamber_intensity: float
    wisdom_extraction_efficiency: float
    minority_opinion_integration: float
    polarization_index: float
    noise_signal_ratio: float
    prediction_market_calibration: float
    delphi_convergence: float
    collective_blind_spot: float
    cognitive_diversity_index: float
    consensus_manipulation_risk: float
    deliberation_quality: float


@dataclass
class CollectiveIntelligenceResult:
    entity_id: str
    region: str
    aggregation_method: str
    ci_risk: str
    ci_pattern: str
    ci_severity: str
    recommended_action: str
    accuracy_score: float
    diversity_score: float
    aggregation_score: float
    integrity_score: float
    ci_composite: float
    is_in_ci_crisis: bool
    requires_ci_intervention: bool
    ci_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "aggregation_method": self.aggregation_method,
            "ci_risk": self.ci_risk,
            "ci_pattern": self.ci_pattern,
            "ci_severity": self.ci_severity,
            "recommended_action": self.recommended_action,
            "accuracy_score": self.accuracy_score,
            "diversity_score": self.diversity_score,
            "aggregation_score": self.aggregation_score,
            "integrity_score": self.integrity_score,
            "ci_composite": self.ci_composite,
            "is_in_ci_crisis": self.is_in_ci_crisis,
            "requires_ci_intervention": self.requires_ci_intervention,
            "ci_signal": self.ci_signal,
        }


def _compute_accuracy_score(inp: CollectiveIntelligenceInput) -> float:
    return (
        (1 - inp.crowd_accuracy_rate) * 0.4
        + inp.noise_signal_ratio * 0.35
        + (1 - inp.prediction_market_calibration) * 0.25
    ) * 100


def _compute_diversity_score(inp: CollectiveIntelligenceInput) -> float:
    return (
        (1 - inp.diversity_of_perspective) * 0.4
        + (1 - inp.cognitive_diversity_index) * 0.35
        + (1 - inp.minority_opinion_integration) * 0.25
    ) * 100


def _compute_aggregation_score(inp: CollectiveIntelligenceInput) -> float:
    return (
        (1 - inp.aggregation_mechanism_quality) * 0.35
        + (1 - inp.wisdom_extraction_efficiency) * 0.35
        + (1 - inp.deliberation_quality) * 0.30
    ) * 100


def _compute_integrity_score(inp: CollectiveIntelligenceInput) -> float:
    return (
        inp.groupthink_susceptibility * 0.35
        + inp.echo_chamber_intensity * 0.30
        + inp.consensus_manipulation_risk * 0.35
    ) * 100


def _compute_composite(
    accuracy: float, diversity: float, aggregation: float, integrity: float
) -> float:
    return accuracy * 0.30 + diversity * 0.25 + aggregation * 0.25 + integrity * 0.20


def _ci_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _ci_pattern(inp: CollectiveIntelligenceInput) -> str:
    if inp.groupthink_susceptibility >= 0.65 and inp.echo_chamber_intensity >= 0.60:
        return "groupthink_cascade"
    if (1 - inp.crowd_accuracy_rate) >= 0.65 and (1 - inp.wisdom_extraction_efficiency) >= 0.60:
        return "wisdom_collapse"
    if inp.information_cascade_risk >= 0.65 and (1 - inp.independence_of_judgment) >= 0.60:
        return "information_cascade_failure"
    if inp.polarization_index >= 0.70 and (1 - inp.diversity_of_perspective) >= 0.60:
        return "polarization_spiral"
    if inp.consensus_manipulation_risk >= 0.70:
        return "manipulation_attack"
    return "none"


def _ci_severity(composite: float) -> str:
    if composite >= 75:
        return "collective_failure"
    if composite >= 50:
        return "high_dysfunction"
    if composite >= 25:
        return "developing_distortion"
    return "collective_wisdom_active"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "ci_emergency_reset"
    if risk == "high" and pattern == "manipulation_attack":
        return "integrity_firewall"
    if risk == "high":
        return "diversity_amplification"
    if risk == "moderate":
        return "ci_monitoring"
    return "no_action"


def _ci_signal(inp: CollectiveIntelligenceInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        return (
            f"Critique — précision collective {int(inp.crowd_accuracy_rate * 100)}%"
            f" — pensée de groupe {int(inp.groupthink_susceptibility * 100)}%"
            f" — composite {comp_int}"
        )
    if risk == "high":
        return (
            f"Élevé — polarisation {int(inp.polarization_index * 100)}%"
            f" — diversité perspectives {int(inp.diversity_of_perspective * 100)}%"
            f" — composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"Modéré — bruit/signal {int(inp.noise_signal_ratio * 100)}%"
            f" — composite {comp_int}"
        )
    return "Intelligence collective optimale — agrégation précise, diversité maintenue, sagesse amplifiée"


def analyze_collective_intelligence(inp: CollectiveIntelligenceInput) -> CollectiveIntelligenceResult:
    accuracy = round(_compute_accuracy_score(inp), 2)
    diversity = round(_compute_diversity_score(inp), 2)
    aggregation = round(_compute_aggregation_score(inp), 2)
    integrity = round(_compute_integrity_score(inp), 2)
    composite = round(_compute_composite(accuracy, diversity, aggregation, integrity), 2)

    risk = _ci_risk(composite)
    pattern = _ci_pattern(inp)
    severity = _ci_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _ci_signal(inp, risk, composite)

    return CollectiveIntelligenceResult(
        entity_id=inp.entity_id,
        region=inp.region,
        aggregation_method=inp.aggregation_method,
        ci_risk=risk,
        ci_pattern=pattern,
        ci_severity=severity,
        recommended_action=action,
        accuracy_score=accuracy,
        diversity_score=diversity,
        aggregation_score=aggregation,
        integrity_score=integrity,
        ci_composite=composite,
        is_in_ci_crisis=composite >= 60,
        requires_ci_intervention=composite >= 40,
        ci_signal=signal,
    )


class CollectiveIntelligenceAmplificationEngine:
    def __init__(self, inputs: List[CollectiveIntelligenceInput]):
        self.inputs = inputs
        self.results: List[CollectiveIntelligenceResult] = [
            analyze_collective_intelligence(inp) for inp in inputs
        ]

    def summarize(self) -> Dict[str, Any]:
        results = self.results
        n = len(results)
        if n == 0:
            return {}

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_accuracy = 0.0
        total_diversity = 0.0
        total_aggregation = 0.0
        total_integrity = 0.0
        ci_crisis_count = 0
        ci_intervention_count = 0

        for r in results:
            risk_counts[r.ci_risk] = risk_counts.get(r.ci_risk, 0) + 1
            pattern_counts[r.ci_pattern] = pattern_counts.get(r.ci_pattern, 0) + 1
            severity_counts[r.ci_severity] = severity_counts.get(r.ci_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1

            total_composite += r.ci_composite
            total_accuracy += r.accuracy_score
            total_diversity += r.diversity_score
            total_aggregation += r.aggregation_score
            total_integrity += r.integrity_score

            if r.is_in_ci_crisis:
                ci_crisis_count += 1
            if r.requires_ci_intervention:
                ci_intervention_count += 1

        avg_composite = total_composite / n
        avg_ci_dysfunction_index = round(avg_composite / 100 * 10, 2)

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_ci_composite": round(avg_composite, 2),
            "ci_crisis_count": ci_crisis_count,
            "ci_intervention_count": ci_intervention_count,
            "avg_accuracy_score": round(total_accuracy / n, 2),
            "avg_diversity_score": round(total_diversity / n, 2),
            "avg_aggregation_score": round(total_aggregation / n, 2),
            "avg_integrity_score": round(total_integrity / n, 2),
            "avg_estimated_ci_dysfunction_index": avg_ci_dysfunction_index,
        }
