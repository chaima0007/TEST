"""
Module 292 — Psychographic Profiling & Behavioral Segmentation Engine
Caelum Partners — Chaima Mhadbi
Deep behavioral segmentation beyond demographics: values, motivations,
cognitive styles, and purchasing psychology.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class PsychographicInput:
    entity_id: str
    segment_type: str
    region: str
    # 17 float fields
    values_coherence: float
    motivation_alignment: float
    cognitive_rigidity: float
    status_orientation: float
    risk_appetite_behavioral: float
    social_conformity_pressure: float
    identity_brand_fusion: float
    novelty_seeking: float
    loss_sensitivity: float
    authority_deference: float
    tribalism_intensity: float
    cognitive_dissonance_tolerance: float
    future_orientation: float
    hedonism_index: float
    autonomy_drive: float
    empathy_capacity: float
    reciprocity_responsiveness: float


class PsychographicResult:
    def __init__(
        self,
        entity_id: str,
        region: str,
        segment_type: str,
        psych_risk: str,
        psych_pattern: str,
        psych_severity: str,
        recommended_action: str,
        values_score: float,
        motivation_score: float,
        cognitive_score: float,
        social_score: float,
        psych_composite: float,
        is_in_psych_crisis: bool,
        requires_psych_intervention: bool,
        psych_signal: str,
    ):
        self.entity_id = entity_id
        self.region = region
        self.segment_type = segment_type
        self.psych_risk = psych_risk
        self.psych_pattern = psych_pattern
        self.psych_severity = psych_severity
        self.recommended_action = recommended_action
        self.values_score = values_score
        self.motivation_score = motivation_score
        self.cognitive_score = cognitive_score
        self.social_score = social_score
        self.psych_composite = psych_composite
        self.is_in_psych_crisis = is_in_psych_crisis
        self.requires_psych_intervention = requires_psych_intervention
        self.psych_signal = psych_signal

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "segment_type": self.segment_type,
            "psych_risk": self.psych_risk,
            "psych_pattern": self.psych_pattern,
            "psych_severity": self.psych_severity,
            "recommended_action": self.recommended_action,
            "values_score": self.values_score,
            "motivation_score": self.motivation_score,
            "cognitive_score": self.cognitive_score,
            "social_score": self.social_score,
            "psych_composite": self.psych_composite,
            "is_in_psych_crisis": self.is_in_psych_crisis,
            "requires_psych_intervention": self.requires_psych_intervention,
            "psych_signal": self.psych_signal,
        }


def _compute_values_score(inp: PsychographicInput) -> float:
    """0–100, higher = worse engagement risk (values instability)."""
    return (
        (1 - inp.values_coherence) * 0.4
        + (1 - inp.motivation_alignment) * 0.35
        + inp.cognitive_dissonance_tolerance * 0.25
    ) * 100


def _compute_motivation_score(inp: PsychographicInput) -> float:
    """0–100, higher = worse engagement risk (motivation deficit)."""
    return (
        (1 - inp.autonomy_drive) * 0.35
        + inp.loss_sensitivity * 0.35
        + (1 - inp.future_orientation) * 0.30
    ) * 100


def _compute_cognitive_score(inp: PsychographicInput) -> float:
    """0–100, higher = worse engagement risk (cognitive rigidity)."""
    return (
        inp.cognitive_rigidity * 0.4
        + inp.authority_deference * 0.30
        + (1 - inp.novelty_seeking) * 0.30
    ) * 100


def _compute_social_score(inp: PsychographicInput) -> float:
    """0–100, higher = worse engagement risk (social resistance)."""
    return (
        inp.tribalism_intensity * 0.4
        + inp.social_conformity_pressure * 0.35
        + (1 - inp.empathy_capacity) * 0.25
    ) * 100


def _compute_composite(
    values_score: float,
    motivation_score: float,
    cognitive_score: float,
    social_score: float,
) -> float:
    return (
        values_score * 0.30
        + motivation_score * 0.25
        + cognitive_score * 0.25
        + social_score * 0.20
    )


def _psych_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _psych_pattern(inp: PsychographicInput) -> str:
    if (1 - inp.values_coherence) >= 0.65 and inp.identity_brand_fusion >= 0.60:
        return "identity_lock"
    if inp.tribalism_intensity >= 0.70 and inp.social_conformity_pressure >= 0.60:
        return "tribalism_capture"
    if inp.loss_sensitivity >= 0.70 and inp.cognitive_rigidity >= 0.60:
        return "loss_aversion_paralysis"
    if (1 - inp.motivation_alignment) >= 0.65 and (1 - inp.autonomy_drive) >= 0.60:
        return "motivation_void"
    if inp.authority_deference >= 0.70 and (1 - inp.autonomy_drive) >= 0.65:
        return "authority_dependency"
    return "none"


def _psych_severity(composite: float) -> str:
    if composite >= 75:
        return "behavioral_blockade"
    if composite >= 50:
        return "high_resistance"
    if composite >= 25:
        return "moderate_friction"
    return "behavioral_fluidity"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "psychographic_intervention"
    if risk == "high" and pattern == "tribalism_capture":
        return "de_tribalization_protocol"
    if risk == "high":
        return "behavioral_reframing"
    if risk == "moderate":
        return "psych_monitoring"
    return "no_action"


def _psych_signal(inp: PsychographicInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        return (
            f"Critique — cohérence valeurs {int(inp.values_coherence * 100)}% "
            f"— tribalisme {int(inp.tribalism_intensity * 100)}% "
            f"— composite {comp_int}"
        )
    if risk == "high":
        return (
            f"Élevé — sensibilité à la perte {int(inp.loss_sensitivity * 100)}% "
            f"— rigidité cognitive {int(inp.cognitive_rigidity * 100)}% "
            f"— composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"Modéré — pression conformité {int(inp.social_conformity_pressure * 100)}% "
            f"— composite {comp_int}"
        )
    return "Profil psychographique favorable — motivations alignées, fluidité comportementale élevée"


def analyze_psychographic(inp: PsychographicInput) -> PsychographicResult:
    values_score = _compute_values_score(inp)
    motivation_score = _compute_motivation_score(inp)
    cognitive_score = _compute_cognitive_score(inp)
    social_score = _compute_social_score(inp)
    composite = _compute_composite(values_score, motivation_score, cognitive_score, social_score)

    risk = _psych_risk(composite)
    pattern = _psych_pattern(inp)
    severity = _psych_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _psych_signal(inp, risk, composite)

    return PsychographicResult(
        entity_id=inp.entity_id,
        region=inp.region,
        segment_type=inp.segment_type,
        psych_risk=risk,
        psych_pattern=pattern,
        psych_severity=severity,
        recommended_action=action,
        values_score=round(values_score, 2),
        motivation_score=round(motivation_score, 2),
        cognitive_score=round(cognitive_score, 2),
        social_score=round(social_score, 2),
        psych_composite=round(composite, 2),
        is_in_psych_crisis=composite >= 60,
        requires_psych_intervention=composite >= 40,
        psych_signal=signal,
    )


class PsychographicProfilingEngine:
    """
    Swarm-ready engine that processes a batch of PsychographicInput records
    and returns a list of PsychographicResult objects plus a 13-key summary.
    """

    def run(self, inputs: List[PsychographicInput]) -> dict:
        results = [analyze_psychographic(inp) for inp in inputs]
        summary = self._summarize(results)
        return {
            "results": [r.to_dict() for r in results],
            "summary": summary,
        }

    def _summarize(self, results: List[PsychographicResult]) -> dict:
        n = len(results)
        if n == 0:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_psych_composite": 0.0,
                "psych_crisis_count": 0,
                "psych_intervention_count": 0,
                "avg_values_score": 0.0,
                "avg_motivation_score": 0.0,
                "avg_cognitive_score": 0.0,
                "avg_social_score": 0.0,
                "avg_estimated_behavioral_resistance_index": 0.0,
            }

        risk_counts: dict = {}
        pattern_counts: dict = {}
        severity_counts: dict = {}
        action_counts: dict = {}

        total_composite = 0.0
        total_values = 0.0
        total_motivation = 0.0
        total_cognitive = 0.0
        total_social = 0.0
        psych_crisis_count = 0
        psych_intervention_count = 0

        for r in results:
            risk_counts[r.psych_risk] = risk_counts.get(r.psych_risk, 0) + 1
            pattern_counts[r.psych_pattern] = pattern_counts.get(r.psych_pattern, 0) + 1
            severity_counts[r.psych_severity] = severity_counts.get(r.psych_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1

            total_composite += r.psych_composite
            total_values += r.values_score
            total_motivation += r.motivation_score
            total_cognitive += r.cognitive_score
            total_social += r.social_score

            if r.is_in_psych_crisis:
                psych_crisis_count += 1
            if r.requires_psych_intervention:
                psych_intervention_count += 1

        avg_composite = total_composite / n

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_psych_composite": round(avg_composite, 1),
            "psych_crisis_count": psych_crisis_count,
            "psych_intervention_count": psych_intervention_count,
            "avg_values_score": round(total_values / n, 1),
            "avg_motivation_score": round(total_motivation / n, 1),
            "avg_cognitive_score": round(total_cognitive / n, 1),
            "avg_social_score": round(total_social / n, 1),
            "avg_estimated_behavioral_resistance_index": round(avg_composite / 100 * 10, 2),
        }
