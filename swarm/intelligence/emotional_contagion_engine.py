"""
Module 303 — Emotional Contagion & Social Epidemic Intelligence Engine
Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
Tracking how emotions spread through populations like epidemics:
panic, euphoria, collective anxiety, rage contagion dynamics.
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class EmotionalContagionInput:
    entity_id: str
    contagion_type: str
    region: str
    contagion_velocity: float
    population_susceptibility: float
    emotional_amplification_rate: float
    social_network_density: float
    fear_cascade_intensity: float
    euphoria_bubble_risk: float
    rage_contagion_potential: float
    anxiety_baseline: float
    collective_resilience: float
    emotional_immune_response: float
    media_amplification_effect: float
    influencer_contagion_leverage: float
    institutional_trust_buffer: float
    cross_border_contagion: float
    recovery_velocity: float
    emotional_polarization_index: float
    contagion_mutation_rate: float


@dataclass
class EmotionalContagionResult:
    entity_id: str
    region: str
    contagion_type: str
    contagion_risk: str
    contagion_pattern: str
    contagion_severity: str
    recommended_action: str
    spread_score: float
    amplification_score: float
    resilience_score: float
    polarization_score: float
    contagion_composite: float
    is_in_contagion_crisis: bool
    requires_contagion_intervention: bool
    contagion_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "contagion_type": self.contagion_type,
            "contagion_risk": self.contagion_risk,
            "contagion_pattern": self.contagion_pattern,
            "contagion_severity": self.contagion_severity,
            "recommended_action": self.recommended_action,
            "spread_score": self.spread_score,
            "amplification_score": self.amplification_score,
            "resilience_score": self.resilience_score,
            "polarization_score": self.polarization_score,
            "contagion_composite": self.contagion_composite,
            "is_in_contagion_crisis": self.is_in_contagion_crisis,
            "requires_contagion_intervention": self.requires_contagion_intervention,
            "contagion_signal": self.contagion_signal,
        }


def _compute_spread_score(e: EmotionalContagionInput) -> float:
    raw = (
        e.contagion_velocity * 0.4
        + e.social_network_density * 0.35
        + e.population_susceptibility * 0.25
    ) * 100
    return round(raw * 100) / 100


def _compute_amplification_score(e: EmotionalContagionInput) -> float:
    raw = (
        e.media_amplification_effect * 0.4
        + e.emotional_amplification_rate * 0.35
        + e.influencer_contagion_leverage * 0.25
    ) * 100
    return round(raw * 100) / 100


def _compute_resilience_score(e: EmotionalContagionInput) -> float:
    raw = (
        (1 - e.collective_resilience) * 0.4
        + (1 - e.emotional_immune_response) * 0.35
        + (1 - e.recovery_velocity) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _compute_polarization_score(e: EmotionalContagionInput) -> float:
    raw = (
        e.emotional_polarization_index * 0.4
        + e.rage_contagion_potential * 0.35
        + e.contagion_mutation_rate * 0.25
    ) * 100
    return round(raw * 100) / 100


def _compute_composite(
    spread: float,
    amplification: float,
    resilience: float,
    polarization: float,
) -> float:
    raw = spread * 0.30 + amplification * 0.25 + resilience * 0.25 + polarization * 0.20
    return round(raw * 100) / 100


def _detect_pattern(e: EmotionalContagionInput) -> str:
    if e.contagion_velocity >= 0.70 and e.fear_cascade_intensity >= 0.65:
        return "panic_epidemic"
    if e.euphoria_bubble_risk >= 0.70 and e.emotional_amplification_rate >= 0.60:
        return "euphoria_mania"
    if e.rage_contagion_potential >= 0.70 and e.social_network_density >= 0.65:
        return "rage_wildfire"
    if e.anxiety_baseline >= 0.70 and e.population_susceptibility >= 0.65:
        return "anxiety_tsunami"
    if e.emotional_polarization_index >= 0.70 and (1 - e.institutional_trust_buffer) >= 0.60:
        return "polarization_spiral"
    return "none"


def _assess_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _assess_severity(composite: float) -> str:
    if composite >= 75:
        return "contagion_emergency"
    if composite >= 50:
        return "high_contagion"
    if composite >= 25:
        return "contagion_developing"
    return "emotional_equilibrium"


def _recommend_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "contagion_circuit_breaker"
    if risk == "high" and pattern == "rage_wildfire":
        return "rage_de_escalation"
    if risk == "high":
        return "emotional_containment"
    if risk == "moderate":
        return "contagion_monitoring"
    return "no_action"


def _build_signal(e: EmotionalContagionInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        vel_pct = int(e.contagion_velocity * 100)
        media_pct = int(e.media_amplification_effect * 100)
        return (
            f"Critique — vélocité contagion {vel_pct}% — "
            f"amplification médias {media_pct}% — composite {comp_int}"
        )
    if risk == "high":
        polar_pct = int(e.emotional_polarization_index * 100)
        resil_pct = int(e.collective_resilience * 100)
        return (
            f"Élevé — polarisation émotionnelle {polar_pct}% — "
            f"résilience collective {resil_pct}% — composite {comp_int}"
        )
    if risk == "moderate":
        susc_pct = int(e.population_susceptibility * 100)
        return f"Modéré — susceptibilité population {susc_pct}% — composite {comp_int}"
    return "Équilibre émotionnel — contagion contrôlée, résilience collective forte, polarisation faible"


def analyze_entity(e: EmotionalContagionInput) -> EmotionalContagionResult:
    spread = _compute_spread_score(e)
    amplification = _compute_amplification_score(e)
    resilience = _compute_resilience_score(e)
    polarization = _compute_polarization_score(e)
    composite = _compute_composite(spread, amplification, resilience, polarization)

    pattern = _detect_pattern(e)
    risk = _assess_risk(composite)
    severity = _assess_severity(composite)
    action = _recommend_action(risk, pattern)
    signal = _build_signal(e, risk, composite)

    return EmotionalContagionResult(
        entity_id=e.entity_id,
        region=e.region,
        contagion_type=e.contagion_type,
        contagion_risk=risk,
        contagion_pattern=pattern,
        contagion_severity=severity,
        recommended_action=action,
        spread_score=spread,
        amplification_score=amplification,
        resilience_score=resilience,
        polarization_score=polarization,
        contagion_composite=composite,
        is_in_contagion_crisis=composite >= 60,
        requires_contagion_intervention=composite >= 40,
        contagion_signal=signal,
    )


class EmotionalContagionEngine:
    def analyze_all(self, entities: List[EmotionalContagionInput]) -> Dict[str, Any]:
        results = [analyze_entity(e) for e in entities]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}
        total_composite = 0.0
        total_spread = 0.0
        total_amplification = 0.0
        total_resilience = 0.0
        total_polarization = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in results:
            risk_counts[r.contagion_risk] = risk_counts.get(r.contagion_risk, 0) + 1
            pattern_counts[r.contagion_pattern] = pattern_counts.get(r.contagion_pattern, 0) + 1
            severity_counts[r.contagion_severity] = severity_counts.get(r.contagion_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.contagion_composite
            total_spread += r.spread_score
            total_amplification += r.amplification_score
            total_resilience += r.resilience_score
            total_polarization += r.polarization_score
            if r.is_in_contagion_crisis:
                crisis_count += 1
            if r.requires_contagion_intervention:
                intervention_count += 1

        n = len(results)
        avg_composite = round(total_composite / n, 2) if n else 0.0

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_contagion_composite": avg_composite,
            "contagion_crisis_count": crisis_count,
            "contagion_intervention_count": intervention_count,
            "avg_spread_score": round(total_spread / n, 2) if n else 0.0,
            "avg_amplification_score": round(total_amplification / n, 2) if n else 0.0,
            "avg_resilience_score": round(total_resilience / n, 2) if n else 0.0,
            "avg_polarization_score": round(total_polarization / n, 2) if n else 0.0,
            "avg_estimated_contagion_index": round(avg_composite / 100 * 10, 2),
        }
