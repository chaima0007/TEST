"""Emotional Intelligence & Market Behavior Analysis Engine — detects behavioral/emotional market dynamics."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EmotionalRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class BehaviorPattern(str, Enum):
    NONE = "none"
    SENTIMENT_COLLAPSE = "sentiment_collapse"
    PANIC_CASCADE = "panic_cascade"
    IRRATIONAL_EXUBERANCE = "irrational_exuberance"
    HERDING_BEHAVIOR = "herding_behavior"
    COGNITIVE_BIAS_SURGE = "cognitive_bias_surge"


class EmotionalSeverity(str, Enum):
    RATIONAL = "rational"
    WATCHFUL = "watchful"
    VOLATILE = "volatile"
    CHAOTIC = "chaotic"


class EmotionalAction(str, Enum):
    NO_ACTION = "no_action"
    SENTIMENT_MONITORING = "sentiment_monitoring"
    BEHAVIORAL_ALERT = "behavioral_alert"
    BIAS_CORRECTION = "bias_correction"
    STAKEHOLDER_REFRAMING = "stakeholder_reframing"
    SENTIMENT_INTERVENTION = "sentiment_intervention"
    BEHAVIOR_CIRCUIT_BREAKER = "behavior_circuit_breaker"
    CRISIS_COMMUNICATION = "crisis_communication"
    EMERGENCY_SENTIMENT_RESET = "emergency_sentiment_reset"


@dataclass
class EmotionalInput:
    segment_id: str
    market_segment: str                       # b2b/b2c/institutional/retail/partner/internal
    region: str
    sentiment_index: float                    # 0-1, 1=very positive
    trust_score: float                        # 0-1, 1=high trust
    emotional_volatility_index: float         # 0-1, 1=highly volatile
    cognitive_bias_score: float               # 0-1, 1=highly biased
    decision_rationality_score: float         # 0-1, 1=fully rational
    fear_greed_index: float                   # 0=extreme fear, 1=extreme greed, 0.5=neutral
    herd_behavior_score: float                # 0-1, 1=strong herding
    loss_aversion_coefficient: float          # 1.0-3.0, >2.0=high
    anchoring_bias_score: float               # 0-1, 1=strongly anchored
    confirmation_bias_score: float            # 0-1, 1=strong confirmation bias
    social_proof_influence: float             # 0-1
    media_sentiment_amplification: float      # 0-1, 1=strong amplification
    behavioral_momentum_score: float          # 0-1, 1=strong momentum
    stress_indicator: float                   # 0-1, 1=high stress
    empathy_alignment_score: float            # 0-1, 1=well aligned
    narrative_coherence_score: float          # 0-1, 1=coherent
    resilience_sentiment_score: float         # 0-1, 1=resilient


@dataclass
class EmotionalResult:
    segment_id: str
    region: str
    emotional_risk: EmotionalRisk
    behavior_pattern: BehaviorPattern
    emotional_severity: EmotionalSeverity
    recommended_action: EmotionalAction
    sentiment_score: float
    rationality_score: float
    bias_score: float
    resilience_score: float
    emotional_composite: float
    has_emotional_crisis: bool
    requires_behavioral_intervention: bool
    estimated_sentiment_disruption_index: float   # 0-10
    emotional_signal: str

    def to_dict(self) -> dict:
        return {
            "segment_id": self.segment_id,
            "region": self.region,
            "emotional_risk": self.emotional_risk.value,
            "behavior_pattern": self.behavior_pattern.value,
            "emotional_severity": self.emotional_severity.value,
            "recommended_action": self.recommended_action.value,
            "sentiment_score": self.sentiment_score,
            "rationality_score": self.rationality_score,
            "bias_score": self.bias_score,
            "resilience_score": self.resilience_score,
            "emotional_composite": self.emotional_composite,
            "has_emotional_crisis": self.has_emotional_crisis,
            "requires_behavioral_intervention": self.requires_behavioral_intervention,
            "estimated_sentiment_disruption_index": self.estimated_sentiment_disruption_index,
            "emotional_signal": self.emotional_signal,
        }


# ── sub-score calculators ─────────────────────────────────────────────────────

def _sentiment_score(inp: EmotionalInput) -> float:
    """0.30 weight — penalize low sentiment_index, low trust_score, high emotional_volatility_index."""
    score = 0.0
    if inp.sentiment_index <= 0.25:
        score += 40
    elif inp.sentiment_index <= 0.50:
        score += 22
    elif inp.sentiment_index <= 0.70:
        score += 9
    if inp.trust_score <= 0.25:
        score += 35
    elif inp.trust_score <= 0.50:
        score += 18
    elif inp.trust_score <= 0.70:
        score += 7
    if inp.emotional_volatility_index >= 0.75:
        score += 25
    elif inp.emotional_volatility_index >= 0.50:
        score += 12
    elif inp.emotional_volatility_index >= 0.30:
        score += 5
    return round(min(score, 100.0), 2)


def _rationality_score(inp: EmotionalInput) -> float:
    """0.25 weight — penalize low decision_rationality_score, high cognitive_bias_score, high herd_behavior_score."""
    score = 0.0
    if inp.decision_rationality_score <= 0.25:
        score += 40
    elif inp.decision_rationality_score <= 0.50:
        score += 22
    elif inp.decision_rationality_score <= 0.70:
        score += 9
    if inp.cognitive_bias_score >= 0.75:
        score += 35
    elif inp.cognitive_bias_score >= 0.50:
        score += 18
    elif inp.cognitive_bias_score >= 0.30:
        score += 7
    if inp.herd_behavior_score >= 0.75:
        score += 25
    elif inp.herd_behavior_score >= 0.50:
        score += 12
    elif inp.herd_behavior_score >= 0.30:
        score += 5
    return round(min(score, 100.0), 2)


def _bias_score(inp: EmotionalInput) -> float:
    """0.25 weight — penalize high anchoring_bias_score, high confirmation_bias_score, high loss_aversion_coefficient (scaled: (coeff-1.0)/2.0)."""
    score = 0.0
    if inp.anchoring_bias_score >= 0.75:
        score += 35
    elif inp.anchoring_bias_score >= 0.50:
        score += 18
    elif inp.anchoring_bias_score >= 0.30:
        score += 7
    if inp.confirmation_bias_score >= 0.75:
        score += 35
    elif inp.confirmation_bias_score >= 0.50:
        score += 18
    elif inp.confirmation_bias_score >= 0.30:
        score += 7
    # loss_aversion scaled: (coeff-1.0)/2.0 gives 0-1 for coeff in [1.0,3.0]
    la_scaled = (inp.loss_aversion_coefficient - 1.0) / 2.0
    if la_scaled >= 0.75:
        score += 30
    elif la_scaled >= 0.50:
        score += 15
    elif la_scaled >= 0.30:
        score += 6
    return round(min(score, 100.0), 2)


def _resilience_score(inp: EmotionalInput) -> float:
    """0.20 weight — penalize low resilience_sentiment_score, high stress_indicator, high media_sentiment_amplification."""
    score = 0.0
    if inp.resilience_sentiment_score <= 0.25:
        score += 40
    elif inp.resilience_sentiment_score <= 0.50:
        score += 22
    elif inp.resilience_sentiment_score <= 0.70:
        score += 9
    if inp.stress_indicator >= 0.75:
        score += 35
    elif inp.stress_indicator >= 0.50:
        score += 18
    elif inp.stress_indicator >= 0.30:
        score += 7
    if inp.media_sentiment_amplification >= 0.75:
        score += 25
    elif inp.media_sentiment_amplification >= 0.50:
        score += 12
    elif inp.media_sentiment_amplification >= 0.30:
        score += 5
    return round(min(score, 100.0), 2)


def _composite(sent: float, rat: float, bias: float, res: float) -> float:
    return round(sent * 0.30 + rat * 0.25 + bias * 0.25 + res * 0.20, 2)


def _risk(composite: float) -> EmotionalRisk:
    if composite >= 60:
        return EmotionalRisk.CRITICAL
    if composite >= 40:
        return EmotionalRisk.HIGH
    if composite >= 20:
        return EmotionalRisk.MODERATE
    return EmotionalRisk.LOW


def _severity(composite: float) -> EmotionalSeverity:
    if composite >= 60:
        return EmotionalSeverity.CHAOTIC
    if composite >= 40:
        return EmotionalSeverity.VOLATILE
    if composite >= 20:
        return EmotionalSeverity.WATCHFUL
    return EmotionalSeverity.RATIONAL


def _pattern(inp: EmotionalInput) -> BehaviorPattern:
    # Priority order
    if inp.sentiment_index <= 0.3 or inp.trust_score <= 0.3:
        return BehaviorPattern.SENTIMENT_COLLAPSE
    if inp.emotional_volatility_index >= 0.7 and inp.fear_greed_index <= 0.3:
        return BehaviorPattern.PANIC_CASCADE
    if inp.fear_greed_index >= 0.8 and inp.herd_behavior_score >= 0.6:
        return BehaviorPattern.IRRATIONAL_EXUBERANCE
    if inp.herd_behavior_score >= 0.7 and inp.social_proof_influence >= 0.6:
        return BehaviorPattern.HERDING_BEHAVIOR
    if inp.cognitive_bias_score >= 0.7 or (inp.anchoring_bias_score >= 0.6 and inp.confirmation_bias_score >= 0.6):
        return BehaviorPattern.COGNITIVE_BIAS_SURGE
    return BehaviorPattern.NONE


def _action(risk: EmotionalRisk, pattern: BehaviorPattern) -> EmotionalAction:
    if risk == EmotionalRisk.CRITICAL:
        if pattern == BehaviorPattern.SENTIMENT_COLLAPSE:
            return EmotionalAction.EMERGENCY_SENTIMENT_RESET
        if pattern == BehaviorPattern.PANIC_CASCADE:
            return EmotionalAction.CRISIS_COMMUNICATION
        return EmotionalAction.BEHAVIOR_CIRCUIT_BREAKER
    if risk == EmotionalRisk.HIGH:
        if pattern == BehaviorPattern.SENTIMENT_COLLAPSE:
            return EmotionalAction.SENTIMENT_INTERVENTION
        if pattern == BehaviorPattern.PANIC_CASCADE:
            return EmotionalAction.BEHAVIOR_CIRCUIT_BREAKER
        if pattern == BehaviorPattern.HERDING_BEHAVIOR:
            return EmotionalAction.BEHAVIORAL_ALERT
        if pattern == BehaviorPattern.COGNITIVE_BIAS_SURGE:
            return EmotionalAction.BIAS_CORRECTION
        return EmotionalAction.STAKEHOLDER_REFRAMING
    if risk == EmotionalRisk.MODERATE:
        return EmotionalAction.SENTIMENT_MONITORING
    return EmotionalAction.NO_ACTION


def _signal(inp: EmotionalInput, comp: float, risk: EmotionalRisk) -> str:
    if comp < 20:
        return "Comportement marché rationnel — sentiment positif, biais contenus, résilience émotionnelle forte"
    label = risk.value.replace("_", " ").title()
    return (
        f"{label} — sentiment {round(inp.sentiment_index * 100)}%"
        f" — confiance {round(inp.trust_score * 100)}%"
        f" — volatilité {round(inp.emotional_volatility_index * 100)}%"
        f" — composite {round(comp)}"
    )


# ── Mock segments ─────────────────────────────────────────────────────────────

_MOCK_SEGMENTS: list[EmotionalInput] = [
    # Fields after region: sentiment_index trust_score emotional_volatility_index cognitive_bias_score
    #   decision_rationality_score fear_greed_index herd_behavior_score loss_aversion_coefficient
    #   anchoring_bias_score confirmation_bias_score social_proof_influence media_sentiment_amplification
    #   behavioral_momentum_score stress_indicator empathy_alignment_score narrative_coherence_score
    #   resilience_sentiment_score  (17 fields)
    # EM-001 b2b EMEA critical sentiment_collapse
    EmotionalInput("EM-001", "b2b", "EMEA",
                   0.15, 0.18, 0.80, 0.75, 0.20, 0.15, 0.85, 2.5, 0.78, 0.80, 0.72, 0.85, 0.70, 0.82, 0.25, 0.15, 0.18),
    # EM-002 b2c NAMER low rational
    EmotionalInput("EM-002", "b2c", "NAMER",
                   0.85, 0.88, 0.12, 0.15, 0.88, 0.55, 0.15, 1.2, 0.15, 0.18, 0.12, 0.20, 0.18, 0.10, 0.85, 0.88, 0.85),
    # EM-003 institutional APAC high panic_cascade
    EmotionalInput("EM-003", "institutional", "APAC",
                   0.40, 0.38, 0.75, 0.60, 0.35, 0.22, 0.72, 1.8, 0.55, 0.52, 0.68, 0.58, 0.55, 0.72, 0.38, 0.42, 0.38),
    # EM-004 retail LATAM moderate watchful
    EmotionalInput("EM-004", "retail", "LATAM",
                   0.58, 0.55, 0.38, 0.42, 0.55, 0.48, 0.40, 1.6, 0.42, 0.45, 0.40, 0.45, 0.42, 0.38, 0.55, 0.52, 0.55),
    # EM-005 b2c MEA critical panic_cascade
    EmotionalInput("EM-005", "b2c", "MEA",
                   0.22, 0.20, 0.82, 0.72, 0.18, 0.18, 0.78, 2.6, 0.70, 0.68, 0.80, 0.72, 0.82, 0.80, 0.22, 0.20, 0.20),
    # EM-006 partner EMEA moderate cognitive_bias_surge
    EmotionalInput("EM-006", "partner", "EMEA",
                   0.52, 0.50, 0.42, 0.72, 0.48, 0.52, 0.45, 1.9, 0.65, 0.62, 0.38, 0.40, 0.42, 0.42, 0.55, 0.50, 0.50),
    # EM-007 institutional NAMER high herding_behavior
    EmotionalInput("EM-007", "institutional", "NAMER",
                   0.45, 0.42, 0.55, 0.55, 0.42, 0.42, 0.75, 1.7, 0.72, 0.65, 0.48, 0.50, 0.68, 0.42, 0.45, 0.42, 0.40),
    # EM-008 internal APAC low rational
    EmotionalInput("EM-008", "internal", "APAC",
                   0.80, 0.82, 0.18, 0.20, 0.80, 0.52, 0.18, 1.3, 0.20, 0.22, 0.15, 0.18, 0.20, 0.10, 0.82, 0.80, 0.82),
]


class EmotionalIntelligenceMarketBehaviorEngine:
    """Detects behavioral and emotional market dynamics to guide intervention strategies."""

    def __init__(self) -> None:
        self._results: list[EmotionalResult] = []

    def analyze(self, inp: EmotionalInput) -> EmotionalResult:
        sent_s = _sentiment_score(inp)
        rat_s = _rationality_score(inp)
        bias_s = _bias_score(inp)
        res_s = _resilience_score(inp)
        comp = _composite(sent_s, rat_s, bias_s, res_s)

        risk = _risk(comp)
        severity = _severity(comp)
        pattern = _pattern(inp)
        action = _action(risk, pattern)

        has_crisis = (
            comp >= 40
            or inp.emotional_volatility_index >= 0.65
            or inp.fear_greed_index <= 0.25
            or inp.fear_greed_index >= 0.85
        )
        requires_intervention = (
            comp >= 25
            or inp.cognitive_bias_score >= 0.65
            or inp.stress_indicator >= 0.70
        )
        disruption_idx = round(min(comp / 100 * (1 - inp.resilience_sentiment_score + 0.01) * 10, 10.0), 2)
        sig = _signal(inp, comp, risk)

        result = EmotionalResult(
            segment_id=inp.segment_id,
            region=inp.region,
            emotional_risk=risk,
            behavior_pattern=pattern,
            emotional_severity=severity,
            recommended_action=action,
            sentiment_score=sent_s,
            rationality_score=rat_s,
            bias_score=bias_s,
            resilience_score=res_s,
            emotional_composite=comp,
            has_emotional_crisis=has_crisis,
            requires_behavioral_intervention=requires_intervention,
            estimated_sentiment_disruption_index=disruption_idx,
            emotional_signal=sig,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[EmotionalInput]) -> list[EmotionalResult]:
        for inp in inputs:
            self.analyze(inp)
        self._results.sort(key=lambda r: r.emotional_composite, reverse=True)
        return self._results

    def load_mock_segments(self) -> list[EmotionalResult]:
        self._results.clear()
        return self.analyze_batch(_MOCK_SEGMENTS)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_emotional_composite": 0.0,
                "emotional_crisis_count": 0,
                "behavioral_intervention_count": 0,
                "avg_sentiment_score": 0.0,
                "avg_rationality_score": 0.0,
                "avg_bias_score": 0.0,
                "avg_resilience_score": 0.0,
                "avg_estimated_sentiment_disruption_index": 0.0,
            }
        risk_counts: dict[str, int] = {}
        pattern_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_comp = total_sent = total_rat = total_bias = total_res = total_idx = 0.0
        for r in self._results:
            risk_counts[r.emotional_risk.value] = risk_counts.get(r.emotional_risk.value, 0) + 1
            pattern_counts[r.behavior_pattern.value] = pattern_counts.get(r.behavior_pattern.value, 0) + 1
            severity_counts[r.emotional_severity.value] = severity_counts.get(r.emotional_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.emotional_composite
            total_sent += r.sentiment_score
            total_rat += r.rationality_score
            total_bias += r.bias_score
            total_res += r.resilience_score
            total_idx += r.estimated_sentiment_disruption_index
        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_emotional_composite": round(total_comp / n, 2),
            "emotional_crisis_count": sum(1 for r in self._results if r.has_emotional_crisis),
            "behavioral_intervention_count": sum(1 for r in self._results if r.requires_behavioral_intervention),
            "avg_sentiment_score": round(total_sent / n, 2),
            "avg_rationality_score": round(total_rat / n, 2),
            "avg_bias_score": round(total_bias / n, 2),
            "avg_resilience_score": round(total_res / n, 2),
            "avg_estimated_sentiment_disruption_index": round(total_idx / n, 2),
        }
