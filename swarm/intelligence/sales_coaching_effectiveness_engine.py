from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class CoachingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CoachingPattern(str, Enum):
    none                    = "none"
    insufficient_frequency  = "insufficient_frequency"
    no_behavioral_change    = "no_behavioral_change"
    topic_misalignment      = "topic_misalignment"
    manager_ineffectiveness = "manager_ineffectiveness"
    coaching_resistance     = "coaching_resistance"


class CoachingSeverity(str, Enum):
    effective   = "effective"
    developing  = "developing"
    stalled     = "stalled"
    regressing  = "regressing"


class CoachingAction(str, Enum):
    no_action                  = "no_action"
    increase_coaching_frequency = "increase_coaching_frequency"
    coaching_topic_reset        = "coaching_topic_reset"
    manager_coaching_training   = "manager_coaching_training"
    external_coach_engagement   = "external_coach_engagement"
    performance_management      = "performance_management"


@dataclass
class CoachingEffectivenessInput:
    rep_id: str
    region: str
    manager_id: str
    coaching_sessions_last_90d: int
    coaching_sessions_benchmark: int
    win_rate_before_coaching_pct: float
    win_rate_after_coaching_pct: float
    quota_attainment_before_pct: float
    quota_attainment_after_pct: float
    activity_score_before: float
    activity_score_after: float
    avg_deal_size_before_usd: float
    avg_deal_size_after_usd: float
    avg_discount_before_pct: float
    avg_discount_after_pct: float
    coaching_topic_alignment_score: float
    days_to_behavioral_change: int
    recidivism_count: int
    manager_coaching_effectiveness_pct: float
    deal_quality_improvement_score: float
    self_assessed_readiness_score: float
    peer_comparison_percentile: float


@dataclass
class CoachingEffectivenessResult:
    rep_id: str
    region: str
    coaching_risk: CoachingRisk
    coaching_pattern: CoachingPattern
    coaching_severity: CoachingSeverity
    recommended_action: CoachingAction
    coaching_frequency_score: float
    coaching_impact_score: float
    coaching_alignment_score: float
    manager_effectiveness_score: float
    coaching_effectiveness_composite: float
    is_coaching_ineffective: bool
    requires_coaching_redesign: bool
    estimated_revenue_impact_usd: float
    coaching_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "coaching_risk":                    self.coaching_risk.value,
            "coaching_pattern":                 self.coaching_pattern.value,
            "coaching_severity":                self.coaching_severity.value,
            "recommended_action":               self.recommended_action.value,
            "coaching_frequency_score":         self.coaching_frequency_score,
            "coaching_impact_score":            self.coaching_impact_score,
            "coaching_alignment_score":         self.coaching_alignment_score,
            "manager_effectiveness_score":      self.manager_effectiveness_score,
            "coaching_effectiveness_composite": self.coaching_effectiveness_composite,
            "is_coaching_ineffective":          self.is_coaching_ineffective,
            "requires_coaching_redesign":       self.requires_coaching_redesign,
            "estimated_revenue_impact_usd":     self.estimated_revenue_impact_usd,
            "coaching_signal":                  self.coaching_signal,
        }


class SalesCoachingEffectivenessEngine:

    def __init__(self) -> None:
        self._results: list[CoachingEffectivenessResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk / less effective)
    # ------------------------------------------------------------------

    def _coaching_frequency_score(self, inp: CoachingEffectivenessInput) -> float:
        score = 0.0

        # Insufficient session volume vs. benchmark
        benchmark = max(inp.coaching_sessions_benchmark, 1)
        if inp.coaching_sessions_last_90d == 0:
            score += 50.0
        elif inp.coaching_sessions_last_90d < benchmark * 0.50:
            score += 35.0
        elif inp.coaching_sessions_last_90d < benchmark * 0.75:
            score += 20.0

        # Long lag between coaching and behavioral change
        if inp.days_to_behavioral_change >= 30:
            score += 20.0
        elif inp.days_to_behavioral_change >= 15:
            score += 10.0

        # Recidivism — same issue being re-coached repeatedly
        if inp.recidivism_count >= 3:
            score += 20.0
        elif inp.recidivism_count >= 1:
            score += 8.0

        return min(score, 100.0)

    def _coaching_impact_score(self, inp: CoachingEffectivenessInput) -> float:
        score = 0.0

        # Win rate regression post-coaching
        win_delta = inp.win_rate_after_coaching_pct - inp.win_rate_before_coaching_pct
        if win_delta < -0.05:
            score += 35.0
        elif win_delta < 0.0:
            score += 18.0

        # Quota attainment regression
        quota_delta = inp.quota_attainment_after_pct - inp.quota_attainment_before_pct
        if quota_delta < -10.0:
            score += 30.0
        elif quota_delta < 0.0:
            score += 15.0

        # Activity score regression
        activity_delta = inp.activity_score_after - inp.activity_score_before
        if activity_delta < -10.0:
            score += 20.0
        elif activity_delta < 0.0:
            score += 10.0

        # Persistent re-coaching on same topics (impact not sticking)
        if inp.recidivism_count >= 2:
            score += 15.0

        return min(score, 100.0)

    def _coaching_alignment_score(self, inp: CoachingEffectivenessInput) -> float:
        score = 0.0

        # Coaching topics don't match actual performance gaps
        if inp.coaching_topic_alignment_score < 40.0:
            score += 40.0
        elif inp.coaching_topic_alignment_score < 60.0:
            score += 25.0
        elif inp.coaching_topic_alignment_score < 75.0:
            score += 10.0

        # Discount behavior worsened after coaching = misaligned pricing guidance
        discount_delta = inp.avg_discount_after_pct - inp.avg_discount_before_pct
        if discount_delta >= 3.0:
            score += 20.0
        elif discount_delta >= 1.0:
            score += 10.0

        # Rep doesn't feel coaching is relevant (low self-assessed readiness)
        if inp.self_assessed_readiness_score < 40.0:
            score += 15.0
        elif inp.self_assessed_readiness_score < 60.0:
            score += 8.0

        return min(score, 100.0)

    def _manager_effectiveness_score(self, inp: CoachingEffectivenessInput) -> float:
        score = 0.0

        # Manager's historical effectiveness rate
        if inp.manager_coaching_effectiveness_pct < 0.30:
            score += 40.0
        elif inp.manager_coaching_effectiveness_pct < 0.50:
            score += 25.0
        elif inp.manager_coaching_effectiveness_pct < 0.70:
            score += 10.0

        # Rep falls significantly below peers post-coaching
        if inp.peer_comparison_percentile < 25.0:
            score += 30.0
        elif inp.peer_comparison_percentile < 40.0:
            score += 15.0

        # Deal quality actually declined (negative improvement score)
        if inp.deal_quality_improvement_score < -10.0:
            score += 20.0
        elif inp.deal_quality_improvement_score < 0.0:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: CoachingEffectivenessInput,
                         frequency: float, impact: float,
                         alignment: float, manager: float) -> CoachingPattern:
        # Priority: coaching_resistance > manager_ineffectiveness > topic_misalignment
        #           > no_behavioral_change > insufficient_frequency > none
        if inp.recidivism_count >= 3 and impact >= 40:
            return CoachingPattern.coaching_resistance
        if manager >= 40 and inp.manager_coaching_effectiveness_pct < 0.40:
            return CoachingPattern.manager_ineffectiveness
        if alignment >= 35 and inp.coaching_topic_alignment_score < 50:
            return CoachingPattern.topic_misalignment
        if impact >= 30 and inp.win_rate_after_coaching_pct <= inp.win_rate_before_coaching_pct \
                and inp.quota_attainment_after_pct <= inp.quota_attainment_before_pct:
            return CoachingPattern.no_behavioral_change
        benchmark = max(inp.coaching_sessions_benchmark, 1)
        if frequency >= 30 and inp.coaching_sessions_last_90d < benchmark * 0.50:
            return CoachingPattern.insufficient_frequency
        return CoachingPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> CoachingRisk:
        if composite >= 60:
            return CoachingRisk.critical
        if composite >= 40:
            return CoachingRisk.high
        if composite >= 20:
            return CoachingRisk.moderate
        return CoachingRisk.low

    def _severity(self, composite: float) -> CoachingSeverity:
        if composite >= 60:
            return CoachingSeverity.regressing
        if composite >= 40:
            return CoachingSeverity.stalled
        if composite >= 20:
            return CoachingSeverity.developing
        return CoachingSeverity.effective

    def _action(self, risk: CoachingRisk, pattern: CoachingPattern) -> CoachingAction:
        if risk == CoachingRisk.critical:
            if pattern == CoachingPattern.coaching_resistance:
                return CoachingAction.performance_management
            if pattern == CoachingPattern.manager_ineffectiveness:
                return CoachingAction.external_coach_engagement
            return CoachingAction.coaching_topic_reset
        if risk == CoachingRisk.high:
            if pattern == CoachingPattern.manager_ineffectiveness:
                return CoachingAction.manager_coaching_training
            if pattern == CoachingPattern.insufficient_frequency:
                return CoachingAction.increase_coaching_frequency
            return CoachingAction.coaching_topic_reset
        if risk == CoachingRisk.moderate:
            if pattern == CoachingPattern.insufficient_frequency:
                return CoachingAction.increase_coaching_frequency
            return CoachingAction.coaching_topic_reset
        return CoachingAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _is_coaching_ineffective(self, composite: float, inp: CoachingEffectivenessInput) -> bool:
        return (
            composite >= 40
            or inp.recidivism_count >= 3
            or inp.win_rate_after_coaching_pct < inp.win_rate_before_coaching_pct - 0.05
        )

    def _requires_coaching_redesign(self, composite: float, inp: CoachingEffectivenessInput) -> bool:
        return (
            composite >= 30
            or inp.coaching_topic_alignment_score < 40.0
            or inp.manager_coaching_effectiveness_pct < 0.30
        )

    # ------------------------------------------------------------------
    # Revenue impact
    # ------------------------------------------------------------------

    def _estimated_revenue_impact(self, inp: CoachingEffectivenessInput, composite: float) -> float:
        deal_degradation = max(inp.avg_deal_size_before_usd - inp.avg_deal_size_after_usd, 0.0)
        return round(deal_degradation * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: CoachingEffectivenessInput,
                pattern: CoachingPattern, composite: float) -> str:
        if pattern == CoachingPattern.none and composite < 10:
            return "Coaching driving measurable performance improvement"
        parts: list[str] = []
        win_delta = inp.win_rate_after_coaching_pct - inp.win_rate_before_coaching_pct
        quota_delta = inp.quota_attainment_after_pct - inp.quota_attainment_before_pct
        if win_delta < 0:
            parts.append(f"win rate {win_delta*100:+.0f}pp post-coaching")
        if quota_delta < 0:
            parts.append(f"attainment {quota_delta:+.0f}pp post-coaching")
        if inp.recidivism_count >= 1:
            parts.append(f"{inp.recidivism_count} recidivism incidents")
        if inp.coaching_topic_alignment_score < 60:
            parts.append(f"{inp.coaching_topic_alignment_score:.0f}% topic alignment")
        label = pattern.value.replace("_", " ") if pattern != CoachingPattern.none else "Coaching risk"
        summary = " — ".join(parts) if parts else "coaching effectiveness degraded"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: CoachingEffectivenessInput) -> CoachingEffectivenessResult:
        frequency = round(self._coaching_frequency_score(inp), 1)
        impact    = round(self._coaching_impact_score(inp), 1)
        alignment = round(self._coaching_alignment_score(inp), 1)
        manager   = round(self._manager_effectiveness_score(inp), 1)

        composite = round(frequency * 0.20 + impact * 0.35 + alignment * 0.25 + manager * 0.20, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, frequency, impact, alignment, manager)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        is_ci  = self._is_coaching_ineffective(composite, inp)
        is_cr  = self._requires_coaching_redesign(composite, inp)
        rev    = self._estimated_revenue_impact(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = CoachingEffectivenessResult(
            rep_id=inp.rep_id,
            region=inp.region,
            coaching_risk=risk,
            coaching_pattern=pattern,
            coaching_severity=severity,
            recommended_action=action,
            coaching_frequency_score=frequency,
            coaching_impact_score=impact,
            coaching_alignment_score=alignment,
            manager_effectiveness_score=manager,
            coaching_effectiveness_composite=composite,
            is_coaching_ineffective=is_ci,
            requires_coaching_redesign=is_cr,
            estimated_revenue_impact_usd=rev,
            coaching_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[CoachingEffectivenessInput]) -> list[CoachingEffectivenessResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_coaching_effectiveness_composite": 0.0,
                "ineffective_coaching_count": 0,
                "coaching_redesign_count": 0,
                "avg_coaching_frequency_score": 0.0,
                "avg_coaching_impact_score": 0.0,
                "avg_coaching_alignment_score": 0.0,
                "avg_manager_effectiveness_score": 0.0,
                "total_estimated_revenue_impact_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_freq = total_imp = total_aln = total_mgr = total_rev = 0.0

        for r in self._results:
            risk_counts[r.coaching_risk.value]         = risk_counts.get(r.coaching_risk.value, 0) + 1
            pattern_counts[r.coaching_pattern.value]   = pattern_counts.get(r.coaching_pattern.value, 0) + 1
            severity_counts[r.coaching_severity.value] = severity_counts.get(r.coaching_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.coaching_effectiveness_composite
            total_freq += r.coaching_frequency_score
            total_imp  += r.coaching_impact_score
            total_aln  += r.coaching_alignment_score
            total_mgr  += r.manager_effectiveness_score
            total_rev  += r.estimated_revenue_impact_usd

        n = len(self._results)

        return {
            "total":                                  n,
            "risk_counts":                            risk_counts,
            "pattern_counts":                         pattern_counts,
            "severity_counts":                        severity_counts,
            "action_counts":                          action_counts,
            "avg_coaching_effectiveness_composite":   round(total_comp / n, 1),
            "ineffective_coaching_count":             sum(1 for r in self._results if r.is_coaching_ineffective),
            "coaching_redesign_count":                sum(1 for r in self._results if r.requires_coaching_redesign),
            "avg_coaching_frequency_score":           round(total_freq / n, 1),
            "avg_coaching_impact_score":              round(total_imp / n, 1),
            "avg_coaching_alignment_score":           round(total_aln / n, 1),
            "avg_manager_effectiveness_score":        round(total_mgr / n, 1),
            "total_estimated_revenue_impact_usd":     round(total_rev, 2),
        }
