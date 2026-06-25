"""
Module 289 — Narrative Control & Memetic Sovereignty Engine
Monitoring and defending narrative sovereignty — detecting hostile memetic operations,
narrative hijacking, information warfare against Caelum Partners' brand and strategic positioning.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class NarrativeControlInput:
    entity_id: str
    narrative_domain: str
    region: str
    narrative_coherence: float
    message_amplification_rate: float
    counter_narrative_exposure: float
    memetic_mutation_speed: float
    brand_narrative_integrity: float
    hostile_framing_intensity: float
    misinformation_penetration: float
    narrative_capture_risk: float
    audience_trust_level: float
    cultural_resonance_alignment: float
    emotional_narrative_charge: float
    viral_spread_coefficient: float
    institutional_narrative_support: float
    narrative_resilience: float
    sovereignty_gap: float
    strategic_communication_effectiveness: float
    memetic_immune_response: float


@dataclass
class NarrativeControlResult:
    entity_id: str
    region: str
    narrative_domain: str
    narrative_risk: str
    narrative_pattern: str
    narrative_severity: str
    recommended_action: str
    integrity_score: float
    penetration_score: float
    resilience_score: float
    sovereignty_score: float
    narrative_composite: float
    is_in_narrative_crisis: bool
    requires_narrative_intervention: bool
    narrative_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "narrative_domain": self.narrative_domain,
            "narrative_risk": self.narrative_risk,
            "narrative_pattern": self.narrative_pattern,
            "narrative_severity": self.narrative_severity,
            "recommended_action": self.recommended_action,
            "integrity_score": self.integrity_score,
            "penetration_score": self.penetration_score,
            "resilience_score": self.resilience_score,
            "sovereignty_score": self.sovereignty_score,
            "narrative_composite": self.narrative_composite,
            "is_in_narrative_crisis": self.is_in_narrative_crisis,
            "requires_narrative_intervention": self.requires_narrative_intervention,
            "narrative_signal": self.narrative_signal,
        }


def _integrity_score(e: NarrativeControlInput) -> float:
    raw = (
        (1 - e.narrative_coherence) * 0.4
        + (1 - e.brand_narrative_integrity) * 0.35
        + (1 - e.audience_trust_level) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _penetration_score(e: NarrativeControlInput) -> float:
    raw = (
        e.misinformation_penetration * 0.4
        + e.hostile_framing_intensity * 0.35
        + e.counter_narrative_exposure * 0.25
    ) * 100
    return round(raw * 100) / 100


def _resilience_score(e: NarrativeControlInput) -> float:
    raw = (
        (1 - e.narrative_resilience) * 0.4
        + (1 - e.memetic_immune_response) * 0.35
        + (1 - e.strategic_communication_effectiveness) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _sovereignty_score(e: NarrativeControlInput) -> float:
    raw = (
        e.sovereignty_gap * 0.4
        + e.narrative_capture_risk * 0.35
        + e.memetic_mutation_speed * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(integrity: float, penetration: float, resilience: float, sovereignty: float) -> float:
    raw = (
        integrity * 0.30
        + penetration * 0.25
        + resilience * 0.25
        + sovereignty * 0.20
    )
    return round(raw * 100) / 100


def _narrative_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _narrative_pattern(e: NarrativeControlInput) -> str:
    if e.narrative_capture_risk >= 0.65 and (1 - e.brand_narrative_integrity) >= 0.55:
        return "narrative_hijacking"
    if e.hostile_framing_intensity >= 0.65 and e.misinformation_penetration >= 0.55:
        return "memetic_attack"
    if e.viral_spread_coefficient >= 0.70 and (1 - e.narrative_coherence) >= 0.55:
        return "viral_narrative_collapse"
    if (1 - e.audience_trust_level) >= 0.70 and e.counter_narrative_exposure >= 0.60:
        return "audience_defection"
    if e.sovereignty_gap >= 0.70 and (1 - e.narrative_resilience) >= 0.60:
        return "sovereignty_erosion"
    return "none"


def _narrative_severity(composite: float) -> str:
    if composite >= 75:
        return "narrative_collapse"
    if composite >= 50:
        return "high_vulnerability"
    if composite >= 25:
        return "developing_threat"
    return "narrative_sovereign"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "narrative_emergency_response"
    if risk == "high" and pattern == "memetic_attack":
        return "counter_memetic_operation"
    if risk == "high":
        return "narrative_reinforcement"
    if risk == "moderate":
        return "narrative_monitoring"
    return "no_action"


def _narrative_signal(e: NarrativeControlInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        return (
            f"Critique — intégrité narrative {int(e.narrative_coherence * 100)}% — "
            f"pénétration désinformation {int(e.misinformation_penetration * 100)}% — "
            f"composite {comp_int}"
        )
    if risk == "high":
        return (
            f"Élevé — risque capture narrative {int(e.narrative_capture_risk * 100)}% — "
            f"confiance audience {int(e.audience_trust_level * 100)}% — "
            f"composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"Modéré — exposition contre-narratives {int(e.counter_narrative_exposure * 100)}% — "
            f"composite {comp_int}"
        )
    return "Souveraineté narrative maintenue — cohérence des messages, résilience mémetique forte"


def analyze_narrative(e: NarrativeControlInput) -> NarrativeControlResult:
    integrity = _integrity_score(e)
    penetration = _penetration_score(e)
    resilience = _resilience_score(e)
    sovereignty = _sovereignty_score(e)
    composite = _composite(integrity, penetration, resilience, sovereignty)

    risk = _narrative_risk(composite)
    pattern = _narrative_pattern(e)
    severity = _narrative_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _narrative_signal(e, risk, composite)

    return NarrativeControlResult(
        entity_id=e.entity_id,
        region=e.region,
        narrative_domain=e.narrative_domain,
        narrative_risk=risk,
        narrative_pattern=pattern,
        narrative_severity=severity,
        recommended_action=action,
        integrity_score=integrity,
        penetration_score=penetration,
        resilience_score=resilience,
        sovereignty_score=sovereignty,
        narrative_composite=composite,
        is_in_narrative_crisis=composite >= 60,
        requires_narrative_intervention=composite >= 40,
        narrative_signal=signal,
    )


class NarrativeControlEngine:
    def __init__(self, inputs: List[NarrativeControlInput]):
        self.inputs = inputs
        self.results = [analyze_narrative(e) for e in inputs]

    def summary(self) -> Dict[str, Any]:
        n = len(self.results)
        if n == 0:
            return {}

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_integrity = 0.0
        total_penetration = 0.0
        total_resilience = 0.0
        total_sovereignty = 0.0
        narrative_crisis_count = 0
        narrative_intervention_count = 0

        for r in self.results:
            risk_counts[r.narrative_risk] = risk_counts.get(r.narrative_risk, 0) + 1
            pattern_counts[r.narrative_pattern] = pattern_counts.get(r.narrative_pattern, 0) + 1
            severity_counts[r.narrative_severity] = severity_counts.get(r.narrative_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1

            total_composite += r.narrative_composite
            total_integrity += r.integrity_score
            total_penetration += r.penetration_score
            total_resilience += r.resilience_score
            total_sovereignty += r.sovereignty_score

            if r.is_in_narrative_crisis:
                narrative_crisis_count += 1
            if r.requires_narrative_intervention:
                narrative_intervention_count += 1

        avg_composite = total_composite / n

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_narrative_composite": round(avg_composite * 10) / 10,
            "narrative_crisis_count": narrative_crisis_count,
            "narrative_intervention_count": narrative_intervention_count,
            "avg_integrity_score": round(total_integrity / n * 10) / 10,
            "avg_penetration_score": round(total_penetration / n * 10) / 10,
            "avg_resilience_score": round(total_resilience / n * 10) / 10,
            "avg_sovereignty_score": round(total_sovereignty / n * 10) / 10,
            "avg_estimated_narrative_threat_index": round(avg_composite / 100 * 10, 2),
        }
