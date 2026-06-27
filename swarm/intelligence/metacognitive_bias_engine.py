"""
Module 321 — Metacognitive Bias & Cognitive Vulnerability Intelligence Engine
Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class MetacognitiveBiasInput:
    entity_id: str
    decision_system_type: str
    region: str

    # 17 float fields (0.0–1.0)
    confirmation_bias_intensity: float
    dunning_kruger_index: float
    availability_heuristic_dominance: float
    anchoring_distortion_rate: float
    groupthink_susceptibility: float
    sunk_cost_fallacy_grip: float
    overconfidence_calibration_gap: float
    black_swan_blindness: float
    narrative_fallacy_exposure: float
    planning_fallacy_severity: float
    hindsight_bias_contamination: float
    status_quo_bias_strength: float
    cognitive_load_saturation: float
    metacognitive_accuracy: float        # inverse: high = good
    epistemic_humility_deficit: float
    debiasing_capacity: float            # inverse: high = good
    echo_chamber_intensity: float


@dataclass
class MetacognitiveBiasResult:
    entity_id: str
    region: str
    decision_system_type: str
    bias_risk: str
    bias_pattern: str
    bias_severity: str
    recommended_action: str
    reasoning_score: float
    heuristic_score: float
    group_score: float
    meta_score: float
    bias_composite: float
    is_bias_crisis: bool
    requires_bias_intervention: bool
    bias_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "decision_system_type": self.decision_system_type,
            "bias_risk": self.bias_risk,
            "bias_pattern": self.bias_pattern,
            "bias_severity": self.bias_severity,
            "recommended_action": self.recommended_action,
            "reasoning_score": self.reasoning_score,
            "heuristic_score": self.heuristic_score,
            "group_score": self.group_score,
            "meta_score": self.meta_score,
            "bias_composite": self.bias_composite,
            "is_bias_crisis": self.is_bias_crisis,
            "requires_bias_intervention": self.requires_bias_intervention,
            "bias_signal": self.bias_signal,
        }


def _reasoning_score(inp: MetacognitiveBiasInput) -> float:
    raw = (
        inp.confirmation_bias_intensity * 0.4
        + inp.dunning_kruger_index * 0.35
        + inp.overconfidence_calibration_gap * 0.25
    ) * 100
    return round(max(0.0, min(100.0, raw)) * 10) / 10


def _heuristic_score(inp: MetacognitiveBiasInput) -> float:
    raw = (
        inp.availability_heuristic_dominance * 0.4
        + inp.anchoring_distortion_rate * 0.35
        + inp.narrative_fallacy_exposure * 0.25
    ) * 100
    return round(max(0.0, min(100.0, raw)) * 10) / 10


def _group_score(inp: MetacognitiveBiasInput) -> float:
    raw = (
        inp.groupthink_susceptibility * 0.4
        + inp.echo_chamber_intensity * 0.35
        + inp.status_quo_bias_strength * 0.25
    ) * 100
    return round(max(0.0, min(100.0, raw)) * 10) / 10


def _meta_score(inp: MetacognitiveBiasInput) -> float:
    raw = (
        (1.0 - inp.metacognitive_accuracy) * 0.4
        + inp.epistemic_humility_deficit * 0.35
        + (1.0 - inp.debiasing_capacity) * 0.25
    ) * 100
    return round(max(0.0, min(100.0, raw)) * 10) / 10


def _composite(
    reasoning: float,
    heuristic: float,
    group: float,
    meta: float,
) -> float:
    raw = (
        reasoning * 0.30
        + heuristic * 0.25
        + group * 0.25
        + meta * 0.20
    )
    return round(max(0.0, min(100.0, raw)) * 10) / 10


def _bias_risk(composite: float) -> str:
    if composite >= 60.0:
        return "critical"
    if composite >= 40.0:
        return "high"
    if composite >= 20.0:
        return "moderate"
    return "low"


def _bias_pattern(inp: MetacognitiveBiasInput) -> str:
    if inp.dunning_kruger_index >= 0.70 and inp.overconfidence_calibration_gap >= 0.65:
        return "dunning_kruger_crisis"
    if inp.groupthink_susceptibility >= 0.70 and inp.echo_chamber_intensity >= 0.65:
        return "groupthink_capture"
    if inp.black_swan_blindness >= 0.70 and inp.overconfidence_calibration_gap >= 0.60:
        return "black_swan_blindness"
    if inp.narrative_fallacy_exposure >= 0.70 and inp.confirmation_bias_intensity >= 0.65:
        return "narrative_trap"
    if inp.metacognitive_accuracy <= 0.30 and inp.epistemic_humility_deficit >= 0.65:
        return "metacognitive_collapse"
    return "none"


def _bias_severity(composite: float) -> str:
    if composite >= 75.0:
        return "cognitive_emergency"
    if composite >= 50.0:
        return "high_bias_risk"
    if composite >= 25.0:
        return "bias_accumulation"
    return "cognitive_clarity"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "cognitive_emergency_debiasing"
    if risk == "high" and pattern == "groupthink_capture":
        return "red_team_intervention"
    if risk == "high":
        return "systematic_debiasing"
    if risk == "moderate":
        return "bias_monitoring"
    return "no_action"


def _bias_signal(
    inp: MetacognitiveBiasInput,
    risk: str,
    pattern: str,
    composite: float,
) -> str:
    if risk == "low":
        return (
            "Cognition saine — biais maîtrisés, raisonnement calibré, "
            "métacognition fonctionnelle, humilité épistémique adéquate"
        )

    pattern_labels: Dict[str, str] = {
        "dunning_kruger_crisis":  "crise Dunning-Kruger",
        "groupthink_capture":     "capture groupthink",
        "black_swan_blindness":   "cécité cygne noir",
        "narrative_trap":         "piège narratif",
        "metacognitive_collapse": "effondrement métacognitif",
        "none":                   "biais diffus non classifié",
    }
    pattern_str = pattern_labels.get(pattern, pattern)

    return (
        f"[{risk.upper()}] Patron détecté: {pattern_str} — "
        f"raisonnement {inp.confirmation_bias_intensity:.0%}, "
        f"DK {inp.dunning_kruger_index:.0%}, "
        f"groupthink {inp.groupthink_susceptibility:.0%}, "
        f"précision méta {inp.metacognitive_accuracy:.0%} — "
        f"composite {composite}"
    )


def analyze(inp: MetacognitiveBiasInput) -> MetacognitiveBiasResult:
    reasoning = _reasoning_score(inp)
    heuristic = _heuristic_score(inp)
    group     = _group_score(inp)
    meta      = _meta_score(inp)
    composite = _composite(reasoning, heuristic, group, meta)
    risk      = _bias_risk(composite)
    pattern   = _bias_pattern(inp)
    severity  = _bias_severity(composite)
    action    = _recommended_action(risk, pattern)
    signal    = _bias_signal(inp, risk, pattern, composite)

    return MetacognitiveBiasResult(
        entity_id=inp.entity_id,
        region=inp.region,
        decision_system_type=inp.decision_system_type,
        bias_risk=risk,
        bias_pattern=pattern,
        bias_severity=severity,
        recommended_action=action,
        reasoning_score=reasoning,
        heuristic_score=heuristic,
        group_score=group,
        meta_score=meta,
        bias_composite=composite,
        is_bias_crisis=composite >= 60.0,
        requires_bias_intervention=composite >= 40.0,
        bias_signal=signal,
    )


class MetacognitiveBiasEngine:
    def __init__(self) -> None:
        self.results: List[MetacognitiveBiasResult] = []

    def analyze(self, entities: List[MetacognitiveBiasInput]) -> Dict[str, Any]:
        self.results = [analyze(e) for e in entities]
        n = len(self.results)

        if n == 0:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_bias_composite": 0.0,
                "bias_crisis_count": 0,
                "bias_intervention_count": 0,
                "avg_reasoning_score": 0.0,
                "avg_heuristic_score": 0.0,
                "avg_group_score": 0.0,
                "avg_meta_score": 0.0,
                "avg_estimated_cognitive_vulnerability_index": 0.0,
            }

        risk_counts: Dict[str, int]     = {}
        pattern_counts: Dict[str, int]  = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int]   = {}
        total_composite = 0.0
        total_reasoning = 0.0
        total_heuristic = 0.0
        total_group     = 0.0
        total_meta      = 0.0
        crisis_count      = 0
        intervention_count = 0

        for r in self.results:
            risk_counts[r.bias_risk]             = risk_counts.get(r.bias_risk, 0) + 1
            pattern_counts[r.bias_pattern]       = pattern_counts.get(r.bias_pattern, 0) + 1
            severity_counts[r.bias_severity]     = severity_counts.get(r.bias_severity, 0) + 1
            action_counts[r.recommended_action]  = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.bias_composite
            total_reasoning += r.reasoning_score
            total_heuristic += r.heuristic_score
            total_group     += r.group_score
            total_meta      += r.meta_score
            if r.is_bias_crisis:
                crisis_count += 1
            if r.requires_bias_intervention:
                intervention_count += 1

        avg_composite = round(total_composite / n * 10) / 10

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_bias_composite": avg_composite,
            "bias_crisis_count": crisis_count,
            "bias_intervention_count": intervention_count,
            "avg_reasoning_score": round(total_reasoning / n * 10) / 10,
            "avg_heuristic_score": round(total_heuristic / n * 10) / 10,
            "avg_group_score":     round(total_group     / n * 10) / 10,
            "avg_meta_score":      round(total_meta      / n * 10) / 10,
            "avg_estimated_cognitive_vulnerability_index": round(avg_composite / 100 * 10, 2),
        }
