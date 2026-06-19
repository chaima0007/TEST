"""
Module 282 — Neuro-Economic Decision Architecture Engine
Applying neuroscience principles to economic decision-making:
cognitive biases, neuroeconomics, decision architecture optimization.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class NeuroEconomicInput:
    entity_id: str
    decision_domain: str
    region: str
    cognitive_load: float
    loss_aversion_bias: float
    anchoring_effect: float
    framing_susceptibility: float
    sunk_cost_fallacy: float
    hyperbolic_discounting: float
    overconfidence_index: float
    herding_tendency: float
    attention_scarcity: float
    emotional_override: float
    decision_fatigue: float
    information_asymmetry: float
    choice_paralysis: float
    recency_bias: float
    rational_override_capacity: float
    metacognitive_awareness: float
    decision_coherence: float


@dataclass
class NeuroEconomicResult:
    entity_id: str
    region: str
    decision_domain: str
    decision_risk: str
    decision_pattern: str
    decision_severity: str
    recommended_action: str
    cognitive_score: float
    bias_score: float
    fatigue_score: float
    coherence_score: float
    decision_composite: float
    is_in_decision_crisis: bool
    requires_architecture_intervention: bool
    decision_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "decision_domain": self.decision_domain,
            "decision_risk": self.decision_risk,
            "decision_pattern": self.decision_pattern,
            "decision_severity": self.decision_severity,
            "recommended_action": self.recommended_action,
            "cognitive_score": self.cognitive_score,
            "bias_score": self.bias_score,
            "fatigue_score": self.fatigue_score,
            "coherence_score": self.coherence_score,
            "decision_composite": self.decision_composite,
            "is_in_decision_crisis": self.is_in_decision_crisis,
            "requires_architecture_intervention": self.requires_architecture_intervention,
            "decision_signal": self.decision_signal,
        }


def _compute_cognitive_score(inp: NeuroEconomicInput) -> float:
    raw = (
        inp.cognitive_load * 0.35
        + inp.attention_scarcity * 0.35
        + inp.decision_fatigue * 0.30
    ) * 100
    return round(raw, 2)


def _compute_bias_score(inp: NeuroEconomicInput) -> float:
    raw = (
        inp.loss_aversion_bias * 0.25
        + inp.anchoring_effect * 0.20
        + inp.framing_susceptibility * 0.20
        + inp.overconfidence_index * 0.20
        + inp.recency_bias * 0.15
    ) * 100
    return round(raw, 2)


def _compute_fatigue_score(inp: NeuroEconomicInput) -> float:
    raw = (
        inp.emotional_override * 0.35
        + inp.herding_tendency * 0.30
        + inp.hyperbolic_discounting * 0.35
    ) * 100
    return round(raw, 2)


def _compute_coherence_score(inp: NeuroEconomicInput) -> float:
    raw = (
        (1 - inp.decision_coherence) * 0.4
        + (1 - inp.rational_override_capacity) * 0.3
        + (1 - inp.metacognitive_awareness) * 0.3
    ) * 100
    return round(raw, 2)


def _compute_composite(
    cognitive: float, bias: float, fatigue: float, coherence: float
) -> float:
    return round(
        cognitive * 0.30 + bias * 0.25 + fatigue * 0.25 + coherence * 0.20, 2
    )


def _decision_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _decision_pattern(inp: NeuroEconomicInput) -> str:
    if inp.cognitive_load >= 0.70 and inp.attention_scarcity >= 0.60:
        return "cognitive_overload"
    if (inp.loss_aversion_bias + inp.anchoring_effect + inp.overconfidence_index) / 3 >= 0.65:
        return "bias_cascade"
    if inp.emotional_override >= 0.70 and (1 - inp.rational_override_capacity) >= 0.60:
        return "emotional_hijack"
    if inp.choice_paralysis >= 0.70 and inp.information_asymmetry >= 0.60:
        return "decision_paralysis"
    if inp.herding_tendency >= 0.70 and (1 - inp.metacognitive_awareness) >= 0.60:
        return "herding_collapse"
    return "none"


def _decision_severity(composite: float) -> str:
    if composite >= 75:
        return "severely_impaired"
    if composite >= 50:
        return "high_distortion"
    if composite >= 25:
        return "moderate_bias"
    return "rational_clarity"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "decision_architecture_reset"
    if risk == "high" and pattern == "bias_cascade":
        return "debiasing_protocol"
    if risk == "high":
        return "cognitive_augmentation"
    if risk == "moderate":
        return "decision_monitoring"
    return "no_action"


def _decision_signal(
    inp: NeuroEconomicInput,
    bias_score: float,
    composite: float,
    risk: str,
) -> str:
    if risk == "critical":
        return (
            f"Critique — charge cognitive {int(inp.cognitive_load * 100)}% "
            f"— biais composite {int(bias_score)}% "
            f"— composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — surcharge émotionnelle {int(inp.emotional_override * 100)}% "
            f"— cohérence décisionnelle {int(inp.decision_coherence * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — biais d'ancrage {int(inp.anchoring_effect * 100)}% "
            f"— composite {int(composite)}"
        )
    return "Architecture décisionnelle optimale — biais contenus, clarté cognitive élevée"


def _assess_single(inp: NeuroEconomicInput) -> NeuroEconomicResult:
    cognitive = _compute_cognitive_score(inp)
    bias = _compute_bias_score(inp)
    fatigue = _compute_fatigue_score(inp)
    coherence = _compute_coherence_score(inp)
    composite = _compute_composite(cognitive, bias, fatigue, coherence)

    risk = _decision_risk(composite)
    pattern = _decision_pattern(inp)
    severity = _decision_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _decision_signal(inp, bias, composite, risk)

    return NeuroEconomicResult(
        entity_id=inp.entity_id,
        region=inp.region,
        decision_domain=inp.decision_domain,
        decision_risk=risk,
        decision_pattern=pattern,
        decision_severity=severity,
        recommended_action=action,
        cognitive_score=cognitive,
        bias_score=bias,
        fatigue_score=fatigue,
        coherence_score=coherence,
        decision_composite=composite,
        is_in_decision_crisis=composite >= 60,
        requires_architecture_intervention=composite >= 40,
        decision_signal=signal,
    )


class NeuroEconomicDecisionEngine:

    def assess_batch(self, inputs: List[NeuroEconomicInput]) -> List[NeuroEconomicResult]:
        return [_assess_single(inp) for inp in inputs]

    def summary(self, results: List[NeuroEconomicResult]) -> Dict[str, Any]:
        total = len(results)
        if total == 0:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_decision_composite": 0.0,
                "decision_crisis_count": 0,
                "architecture_intervention_count": 0,
                "avg_cognitive_score": 0.0,
                "avg_bias_score": 0.0,
                "avg_fatigue_score": 0.0,
                "avg_coherence_score": 0.0,
                "avg_estimated_decision_risk_index": 0.0,
            }

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        sum_composite = 0.0
        sum_cognitive = 0.0
        sum_bias = 0.0
        sum_fatigue = 0.0
        sum_coherence = 0.0
        decision_crisis_count = 0
        architecture_intervention_count = 0

        for r in results:
            risk_counts[r.decision_risk] = risk_counts.get(r.decision_risk, 0) + 1
            pattern_counts[r.decision_pattern] = pattern_counts.get(r.decision_pattern, 0) + 1
            severity_counts[r.decision_severity] = severity_counts.get(r.decision_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            sum_composite += r.decision_composite
            sum_cognitive += r.cognitive_score
            sum_bias += r.bias_score
            sum_fatigue += r.fatigue_score
            sum_coherence += r.coherence_score
            if r.is_in_decision_crisis:
                decision_crisis_count += 1
            if r.requires_architecture_intervention:
                architecture_intervention_count += 1

        avg_composite = sum_composite / total

        return {
            "total": total,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_decision_composite": round(avg_composite, 1),
            "decision_crisis_count": decision_crisis_count,
            "architecture_intervention_count": architecture_intervention_count,
            "avg_cognitive_score": round(sum_cognitive / total, 1),
            "avg_bias_score": round(sum_bias / total, 1),
            "avg_fatigue_score": round(sum_fatigue / total, 1),
            "avg_coherence_score": round(sum_coherence / total, 1),
            "avg_estimated_decision_risk_index": round(avg_composite / 100 * 10, 2),
        }
