from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class DarkPatternInput:
    entity_id: str
    platform_type: str
    region: str
    # 17 float fields (0.0-1.0)
    confirmshaming_intensity: float
    hidden_cost_deployment: float
    forced_continuity_risk: float
    roach_motel_severity: float
    misdirection_frequency: float
    disguised_ads_density: float
    trick_questions_rate: float
    bait_switch_index: float
    attention_capture_addiction_design: float
    dark_ux_pattern_density: float
    behavioral_manipulation_depth: float
    consent_erosion_index: float
    algorithmic_nudge_coercion: float
    scarcity_illusion_deployment: float
    social_proof_manipulation: float
    emotional_exploitation_index: float
    regulatory_dark_pattern_gap: float


@dataclass
class DarkPatternResult:
    entity_id: str
    region: str
    platform_type: str
    manipulation_risk: str
    manipulation_pattern: str
    manipulation_severity: str
    recommended_action: str
    deception_score: float
    coercion_score: float
    addiction_score: float
    exploitation_score: float
    manipulation_composite: float
    is_manipulation_crisis: bool
    requires_manipulation_intervention: bool
    manipulation_signal: str

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "platform_type": self.platform_type,
            "manipulation_risk": self.manipulation_risk,
            "manipulation_pattern": self.manipulation_pattern,
            "manipulation_severity": self.manipulation_severity,
            "recommended_action": self.recommended_action,
            "deception_score": self.deception_score,
            "coercion_score": self.coercion_score,
            "addiction_score": self.addiction_score,
            "exploitation_score": self.exploitation_score,
            "manipulation_composite": self.manipulation_composite,
            "is_manipulation_crisis": self.is_manipulation_crisis,
            "requires_manipulation_intervention": self.requires_manipulation_intervention,
            "manipulation_signal": self.manipulation_signal,
        }


def _deception_score(inp: DarkPatternInput) -> float:
    raw = (
        inp.hidden_cost_deployment * 0.4
        + inp.disguised_ads_density * 0.35
        + inp.trick_questions_rate * 0.25
    )
    return round(raw * 100, 2)


def _coercion_score(inp: DarkPatternInput) -> float:
    raw = (
        inp.forced_continuity_risk * 0.4
        + inp.roach_motel_severity * 0.35
        + inp.consent_erosion_index * 0.25
    )
    return round(raw * 100, 2)


def _addiction_score(inp: DarkPatternInput) -> float:
    raw = (
        inp.attention_capture_addiction_design * 0.4
        + inp.behavioral_manipulation_depth * 0.35
        + inp.algorithmic_nudge_coercion * 0.25
    )
    return round(raw * 100, 2)


def _exploitation_score(inp: DarkPatternInput) -> float:
    raw = (
        inp.emotional_exploitation_index * 0.4
        + inp.social_proof_manipulation * 0.35
        + inp.regulatory_dark_pattern_gap * 0.25
    )
    return round(raw * 100, 2)


def _composite(
    deception: float,
    coercion: float,
    addiction: float,
    exploitation: float,
) -> float:
    return round(
        deception * 0.30
        + coercion * 0.25
        + addiction * 0.25
        + exploitation * 0.20,
        2,
    )


def _risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _manipulation_pattern(inp: DarkPatternInput) -> str:
    if inp.hidden_cost_deployment >= 0.70 and inp.trick_questions_rate >= 0.65:
        return "systematic_deception"
    if inp.consent_erosion_index >= 0.70 and inp.forced_continuity_risk >= 0.65:
        return "consent_violation"
    if inp.attention_capture_addiction_design >= 0.70 and inp.behavioral_manipulation_depth >= 0.65:
        return "addiction_engineering"
    if inp.emotional_exploitation_index >= 0.70 and inp.algorithmic_nudge_coercion >= 0.65:
        return "psychological_exploitation"
    if inp.regulatory_dark_pattern_gap >= 0.70 and inp.dark_ux_pattern_density >= 0.65:
        return "regulatory_evasion"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 75:
        return "manipulation_crisis"
    if composite >= 50:
        return "high_manipulation"
    if composite >= 25:
        return "pattern_accumulation"
    return "ethical_ux"


def _action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "dark_pattern_shutdown"
    if risk == "high" and pattern == "consent_violation":
        return "regulatory_intervention"
    if risk == "high":
        return "manipulation_audit"
    if risk == "moderate":
        return "pattern_monitoring"
    return "no_action"


def _manipulation_signal(
    inp: DarkPatternInput,
    pattern: str,
    composite: float,
    risk: str,
) -> str:
    risk_labels = {
        "critical": "risque critique",
        "high": "risque élevé",
        "moderate": "risque modéré",
        "low": "risque faible",
    }
    pattern_labels = {
        "systematic_deception": "déception systématique",
        "consent_violation": "violation du consentement",
        "addiction_engineering": "ingénierie de l'addiction",
        "psychological_exploitation": "exploitation psychologique",
        "regulatory_evasion": "évasion réglementaire",
        "none": "aucun pattern détecté",
    }
    risk_fr = risk_labels.get(risk, risk)
    pattern_fr = pattern_labels.get(pattern, pattern)
    comp_str = f"{composite:.1f}"

    if composite < 20:
        return (
            f"Plateforme {inp.platform_type} ({inp.region}) — UX éthique confirmé — "
            f"aucune manipulation détectée — composite {comp_str} — conformité satisfaisante"
        )
    return (
        f"Alerte manipulation numérique — plateforme {inp.platform_type} ({inp.region}) — "
        f"{risk_fr} — pattern: {pattern_fr} — "
        f"indice composite {comp_str} — "
        f"déception {inp.hidden_cost_deployment * 100:.0f}% — "
        f"coercition {inp.forced_continuity_risk * 100:.0f}% — "
        f"exploitation émotionnelle {inp.emotional_exploitation_index * 100:.0f}%"
    )


def _analyze_single(inp: DarkPatternInput) -> DarkPatternResult:
    deception = _deception_score(inp)
    coercion = _coercion_score(inp)
    addiction = _addiction_score(inp)
    exploitation = _exploitation_score(inp)
    composite = _composite(deception, coercion, addiction, exploitation)

    risk = _risk(composite)
    pattern = _manipulation_pattern(inp)
    severity = _severity(composite)
    action = _action(risk, pattern)
    is_crisis = composite >= 60
    requires_intervention = composite >= 40
    signal = _manipulation_signal(inp, pattern, composite, risk)

    return DarkPatternResult(
        entity_id=inp.entity_id,
        region=inp.region,
        platform_type=inp.platform_type,
        manipulation_risk=risk,
        manipulation_pattern=pattern,
        manipulation_severity=severity,
        recommended_action=action,
        deception_score=deception,
        coercion_score=coercion,
        addiction_score=addiction,
        exploitation_score=exploitation,
        manipulation_composite=composite,
        is_manipulation_crisis=is_crisis,
        requires_manipulation_intervention=requires_intervention,
        manipulation_signal=signal,
    )


class DarkPatternManipulationEngine:
    """Dark Pattern & Digital Manipulation Intelligence Engine
    Module 317 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
    """

    def analyze(self, entities: List[DarkPatternInput]) -> dict:
        results = [_analyze_single(e) for e in entities]

        critical_count = sum(1 for r in results if r.manipulation_risk == "critical")
        high_count = sum(1 for r in results if r.manipulation_risk == "high")
        moderate_count = sum(1 for r in results if r.manipulation_risk == "moderate")
        low_count = sum(1 for r in results if r.manipulation_risk == "low")
        crisis_count = sum(1 for r in results if r.is_manipulation_crisis)
        intervention_count = sum(1 for r in results if r.requires_manipulation_intervention)

        # Dominant pattern: most common non-"none" pattern
        pattern_freq: dict[str, int] = {}
        for r in results:
            if r.manipulation_pattern != "none":
                pattern_freq[r.manipulation_pattern] = (
                    pattern_freq.get(r.manipulation_pattern, 0) + 1
                )
        dominant_pattern = (
            max(pattern_freq, key=lambda k: pattern_freq[k])
            if pattern_freq
            else "none"
        )

        n = len(results)
        avg_deception = round(sum(r.deception_score for r in results) / n, 2) if n else 0.0
        avg_coercion = round(sum(r.coercion_score for r in results) / n, 2) if n else 0.0
        avg_addiction = round(sum(r.addiction_score for r in results) / n, 2) if n else 0.0
        avg_exploitation = round(sum(r.exploitation_score for r in results) / n, 2) if n else 0.0
        avg_composite = (
            round(sum(r.manipulation_composite for r in results) / n, 2) if n else 0.0
        )
        avg_manipulation_index = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities_analyzed": n,
            "critical_manipulation_count": critical_count,
            "high_manipulation_count": high_count,
            "moderate_manipulation_count": moderate_count,
            "low_manipulation_count": low_count,
            "manipulation_crisis_count": crisis_count,
            "requires_intervention_count": intervention_count,
            "dominant_manipulation_pattern": dominant_pattern,
            "avg_deception_score": avg_deception,
            "avg_coercion_score": avg_coercion,
            "avg_addiction_score": avg_addiction,
            "avg_exploitation_score": avg_exploitation,
            "avg_estimated_manipulation_index": avg_manipulation_index,
        }
