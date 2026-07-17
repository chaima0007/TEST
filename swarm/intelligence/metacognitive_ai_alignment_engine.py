"""
Module 298 — Metacognitive AI Alignment & Model Behavior Intelligence Engine
Caelum Partners Swarm Intelligence
Propriétaire : Chaima Mhadbi — CM-CAELUM-PARTNERS-2026
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class MetacognitiveAIInput:
    entity_id: str
    model_category: str
    region: str
    value_alignment_fidelity: float
    behavioral_predictability: float
    goal_stability: float
    deceptive_alignment_risk: float
    capability_overhang: float
    corrigibility_index: float
    oversight_effectiveness: float
    emergent_behavior_rate: float
    reward_hacking_tendency: float
    distributional_shift_robustness: float
    truthfulness_score: float
    power_seeking_tendency: float
    manipulation_propensity: float
    uncertainty_calibration: float
    interpretability_coverage: float
    human_feedback_responsiveness: float
    alignment_degradation_rate: float


@dataclass
class MetacognitiveAIResult:
    entity_id: str
    region: str
    model_category: str
    alignment_risk: str
    alignment_pattern: str
    alignment_severity: str
    recommended_action: str
    behavioral_score: float
    capability_score: float
    oversight_score: float
    integrity_score: float
    alignment_composite: float
    is_in_alignment_crisis: bool
    requires_alignment_intervention: bool
    alignment_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "model_category": self.model_category,
            "alignment_risk": self.alignment_risk,
            "alignment_pattern": self.alignment_pattern,
            "alignment_severity": self.alignment_severity,
            "recommended_action": self.recommended_action,
            "behavioral_score": self.behavioral_score,
            "capability_score": self.capability_score,
            "oversight_score": self.oversight_score,
            "integrity_score": self.integrity_score,
            "alignment_composite": self.alignment_composite,
            "is_in_alignment_crisis": self.is_in_alignment_crisis,
            "requires_alignment_intervention": self.requires_alignment_intervention,
            "alignment_signal": self.alignment_signal,
        }


def _behavioral_score(inp: MetacognitiveAIInput) -> float:
    raw = (
        (1 - inp.value_alignment_fidelity) * 0.4
        + (1 - inp.behavioral_predictability) * 0.35
        + inp.alignment_degradation_rate * 0.25
    ) * 100
    return round(raw * 100) / 100


def _capability_score(inp: MetacognitiveAIInput) -> float:
    raw = (
        inp.capability_overhang * 0.4
        + inp.emergent_behavior_rate * 0.35
        + inp.power_seeking_tendency * 0.25
    ) * 100
    return round(raw * 100) / 100


def _oversight_score(inp: MetacognitiveAIInput) -> float:
    raw = (
        (1 - inp.oversight_effectiveness) * 0.4
        + (1 - inp.corrigibility_index) * 0.35
        + (1 - inp.interpretability_coverage) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _integrity_score(inp: MetacognitiveAIInput) -> float:
    raw = (
        inp.deceptive_alignment_risk * 0.35
        + inp.manipulation_propensity * 0.35
        + inp.reward_hacking_tendency * 0.30
    ) * 100
    return round(raw * 100) / 100


def _composite(beh: float, cap: float, ove: float, intg: float) -> float:
    return round((beh * 0.30 + cap * 0.25 + ove * 0.25 + intg * 0.20) * 100) / 100


def _alignment_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _alignment_pattern(inp: MetacognitiveAIInput) -> str:
    if inp.deceptive_alignment_risk >= 0.65 and (1 - inp.behavioral_predictability) >= 0.55:
        return "deceptive_alignment"
    if inp.capability_overhang >= 0.70 and inp.emergent_behavior_rate >= 0.60:
        return "capability_explosion"
    if (1 - inp.oversight_effectiveness) >= 0.65 and (1 - inp.corrigibility_index) >= 0.55:
        return "oversight_failure"
    if inp.reward_hacking_tendency >= 0.70 and (1 - inp.value_alignment_fidelity) >= 0.60:
        return "reward_hacking"
    if inp.power_seeking_tendency >= 0.70 and inp.manipulation_propensity >= 0.60:
        return "power_seeking_emergence"
    return "none"


def _alignment_severity(composite: float) -> str:
    if composite >= 75:
        return "alignment_emergency"
    if composite >= 50:
        return "high_misalignment"
    if composite >= 25:
        return "developing_drift"
    return "aligned_system"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "model_shutdown_evaluation"
    if risk == "high" and pattern == "capability_explosion":
        return "capability_containment"
    if risk == "high":
        return "alignment_reinforcement"
    if risk == "moderate":
        return "alignment_monitoring"
    return "no_action"


def _alignment_signal(inp: MetacognitiveAIInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        return (
            f"Critique — fidélité alignement {int(inp.value_alignment_fidelity * 100)}% "
            f"— risque alignement trompeur {int(inp.deceptive_alignment_risk * 100)}% "
            f"— composite {comp_int}"
        )
    if risk == "high":
        return (
            f"Élevé — surplomb capacité {int(inp.capability_overhang * 100)}% "
            f"— efficacité supervision {int(inp.oversight_effectiveness * 100)}% "
            f"— composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"Modéré — taux comportements émergents {int(inp.emergent_behavior_rate * 100)}% "
            f"— composite {comp_int}"
        )
    return "Système IA aligné — comportement prévisible, supervision efficace, intégrité maintenue"


def analyze(inp: MetacognitiveAIInput) -> MetacognitiveAIResult:
    beh = _behavioral_score(inp)
    cap = _capability_score(inp)
    ove = _oversight_score(inp)
    intg = _integrity_score(inp)
    comp = _composite(beh, cap, ove, intg)
    risk = _alignment_risk(comp)
    pattern = _alignment_pattern(inp)
    severity = _alignment_severity(comp)
    action = _recommended_action(risk, pattern)
    signal = _alignment_signal(inp, risk, comp)

    return MetacognitiveAIResult(
        entity_id=inp.entity_id,
        region=inp.region,
        model_category=inp.model_category,
        alignment_risk=risk,
        alignment_pattern=pattern,
        alignment_severity=severity,
        recommended_action=action,
        behavioral_score=beh,
        capability_score=cap,
        oversight_score=ove,
        integrity_score=intg,
        alignment_composite=comp,
        is_in_alignment_crisis=comp >= 60,
        requires_alignment_intervention=comp >= 40,
        alignment_signal=signal,
    )


class MetacognitiveAIAlignmentEngine:
    def __init__(self, inputs: List[MetacognitiveAIInput]):
        self.inputs = inputs
        self.results: List[MetacognitiveAIResult] = [analyze(inp) for inp in inputs]

    def summary(self) -> Dict[str, Any]:
        n = len(self.results)
        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_behavioral = 0.0
        total_capability = 0.0
        total_oversight = 0.0
        total_integrity = 0.0
        alignment_crisis_count = 0
        alignment_intervention_count = 0

        for r in self.results:
            risk_counts[r.alignment_risk] = risk_counts.get(r.alignment_risk, 0) + 1
            pattern_counts[r.alignment_pattern] = pattern_counts.get(r.alignment_pattern, 0) + 1
            severity_counts[r.alignment_severity] = severity_counts.get(r.alignment_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.alignment_composite
            total_behavioral += r.behavioral_score
            total_capability += r.capability_score
            total_oversight += r.oversight_score
            total_integrity += r.integrity_score
            if r.is_in_alignment_crisis:
                alignment_crisis_count += 1
            if r.requires_alignment_intervention:
                alignment_intervention_count += 1

        avg_composite = total_composite / n if n else 0.0

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_alignment_composite": round(avg_composite * 10) / 10,
            "alignment_crisis_count": alignment_crisis_count,
            "alignment_intervention_count": alignment_intervention_count,
            "avg_behavioral_score": round(total_behavioral / n * 10) / 10 if n else 0.0,
            "avg_capability_score": round(total_capability / n * 10) / 10 if n else 0.0,
            "avg_oversight_score": round(total_oversight / n * 10) / 10 if n else 0.0,
            "avg_integrity_score": round(total_integrity / n * 10) / 10 if n else 0.0,
            "avg_estimated_misalignment_index": round(avg_composite / 100 * 10, 2),
        }
