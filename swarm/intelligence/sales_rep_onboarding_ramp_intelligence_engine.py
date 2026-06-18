from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class RampRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class RampPattern(str, Enum):
    none                         = "none"
    slow_pipeline_build          = "slow_pipeline_build"
    activity_adoption_lag        = "activity_adoption_lag"
    first_deal_stall             = "first_deal_stall"
    coaching_resistance          = "coaching_resistance"
    early_exit_risk              = "early_exit_risk"


class RampSeverity(str, Enum):
    accelerating = "accelerating"
    on_track     = "on_track"
    lagging      = "lagging"
    derailing    = "derailing"


class RampAction(str, Enum):
    no_action                    = "no_action"
    pipeline_build_coaching      = "pipeline_build_coaching"
    activity_habits_coaching     = "activity_habits_coaching"
    deal_progression_coaching    = "deal_progression_coaching"
    manager_led_intervention     = "manager_led_intervention"
    ramp_extension_review        = "ramp_extension_review"


@dataclass
class RampInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    ramp_week: int
    target_ramp_weeks: int
    pipeline_build_pct_of_target: float
    first_deal_closed: bool
    days_to_first_deal: float
    activity_adoption_score_pct: float
    crm_usage_compliance_pct: float
    calls_per_week_vs_target_pct: float
    emails_per_week_vs_target_pct: float
    meetings_booked_vs_target_pct: float
    coaching_session_attendance_pct: float
    coaching_action_completion_pct: float
    manager_confidence_score: float
    peer_benchmark_percentile: float
    avg_deal_size_vs_cohort_pct: float
    deals_in_pipeline: int
    pipeline_stage_advancement_rate_pct: float
    expected_first_quarter_attainment_pct: float
    avg_opportunity_value_usd: float


@dataclass
class RampResult:
    rep_id: str
    region: str
    ramp_risk: RampRisk
    ramp_pattern: RampPattern
    ramp_severity: RampSeverity
    recommended_action: RampAction
    pipeline_score: float
    activity_score: float
    coaching_score: float
    progression_score: float
    ramp_composite: float
    has_ramp_gap: bool
    requires_ramp_intervention: bool
    estimated_ramp_revenue_loss_usd: float
    ramp_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "ramp_risk":                        self.ramp_risk.value,
            "ramp_pattern":                     self.ramp_pattern.value,
            "ramp_severity":                    self.ramp_severity.value,
            "recommended_action":               self.recommended_action.value,
            "pipeline_score":                   self.pipeline_score,
            "activity_score":                   self.activity_score,
            "coaching_score":                   self.coaching_score,
            "progression_score":                self.progression_score,
            "ramp_composite":                   self.ramp_composite,
            "has_ramp_gap":                     self.has_ramp_gap,
            "requires_ramp_intervention":       self.requires_ramp_intervention,
            "estimated_ramp_revenue_loss_usd":  self.estimated_ramp_revenue_loss_usd,
            "ramp_signal":                      self.ramp_signal,
        }


class SalesRepOnboardingRampIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[RampResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _pipeline_score(self, inp: RampInput) -> float:
        score = 0.0

        if inp.pipeline_build_pct_of_target <= 0.25:
            score += 40.0
        elif inp.pipeline_build_pct_of_target <= 0.50:
            score += 22.0
        elif inp.pipeline_build_pct_of_target <= 0.75:
            score += 8.0

        if inp.deals_in_pipeline <= 1:
            score += 35.0
        elif inp.deals_in_pipeline <= 3:
            score += 18.0

        if inp.expected_first_quarter_attainment_pct <= 0.30:
            score += 25.0
        elif inp.expected_first_quarter_attainment_pct <= 0.60:
            score += 12.0

        return min(score, 100.0)

    def _activity_score(self, inp: RampInput) -> float:
        score = 0.0

        if inp.activity_adoption_score_pct <= 0.40:
            score += 40.0
        elif inp.activity_adoption_score_pct <= 0.65:
            score += 22.0
        elif inp.activity_adoption_score_pct <= 0.80:
            score += 8.0

        if inp.crm_usage_compliance_pct <= 0.50:
            score += 35.0
        elif inp.crm_usage_compliance_pct <= 0.75:
            score += 18.0

        if inp.calls_per_week_vs_target_pct <= 0.40:
            score += 25.0
        elif inp.calls_per_week_vs_target_pct <= 0.70:
            score += 12.0

        return min(score, 100.0)

    def _coaching_score(self, inp: RampInput) -> float:
        score = 0.0

        if inp.coaching_action_completion_pct <= 0.30:
            score += 40.0
        elif inp.coaching_action_completion_pct <= 0.60:
            score += 22.0
        elif inp.coaching_action_completion_pct <= 0.80:
            score += 8.0

        if inp.coaching_session_attendance_pct <= 0.60:
            score += 35.0
        elif inp.coaching_session_attendance_pct <= 0.80:
            score += 18.0

        if inp.manager_confidence_score <= 0.30:
            score += 25.0
        elif inp.manager_confidence_score <= 0.60:
            score += 12.0

        return min(score, 100.0)

    def _progression_score(self, inp: RampInput) -> float:
        score = 0.0

        if inp.peer_benchmark_percentile <= 0.15:
            score += 45.0
        elif inp.peer_benchmark_percentile <= 0.35:
            score += 25.0
        elif inp.peer_benchmark_percentile <= 0.50:
            score += 10.0

        if not inp.first_deal_closed and inp.ramp_week >= inp.target_ramp_weeks * 0.75:
            score += 30.0
        elif not inp.first_deal_closed and inp.ramp_week >= inp.target_ramp_weeks * 0.50:
            score += 15.0

        if inp.pipeline_stage_advancement_rate_pct <= 0.20:
            score += 25.0
        elif inp.pipeline_stage_advancement_rate_pct <= 0.40:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: RampInput,
                          pipeline: float, activity: float,
                          coaching: float, progression: float) -> RampPattern:
        # Early exit risk: very low manager confidence + very low peer percentile
        if inp.manager_confidence_score <= 0.20 and inp.peer_benchmark_percentile <= 0.15:
            return RampPattern.early_exit_risk

        # Coaching resistance: high coaching score but good activity (resists coaching despite showing up)
        if coaching >= 35 and inp.coaching_action_completion_pct <= 0.30:
            return RampPattern.coaching_resistance

        # Slow pipeline build: pipeline risk dominant
        if pipeline >= 35 and inp.pipeline_build_pct_of_target <= 0.40:
            return RampPattern.slow_pipeline_build

        # Activity adoption lag: activity score dominant
        if activity >= 35 and inp.activity_adoption_score_pct <= 0.50:
            return RampPattern.activity_adoption_lag

        # First deal stall: no first deal well into ramp
        if not inp.first_deal_closed and inp.ramp_week >= inp.target_ramp_weeks * 0.60:
            return RampPattern.first_deal_stall

        return RampPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> RampRisk:
        if composite >= 60:
            return RampRisk.critical
        if composite >= 40:
            return RampRisk.high
        if composite >= 20:
            return RampRisk.moderate
        return RampRisk.low

    def _severity(self, composite: float) -> RampSeverity:
        if composite >= 60:
            return RampSeverity.derailing
        if composite >= 40:
            return RampSeverity.lagging
        if composite >= 20:
            return RampSeverity.on_track
        return RampSeverity.accelerating

    def _action(self, risk: RampRisk, pattern: RampPattern) -> RampAction:
        if risk == RampRisk.critical:
            if pattern == RampPattern.early_exit_risk:
                return RampAction.ramp_extension_review
            if pattern == RampPattern.coaching_resistance:
                return RampAction.manager_led_intervention
            return RampAction.ramp_extension_review
        if risk == RampRisk.high:
            if pattern == RampPattern.slow_pipeline_build:
                return RampAction.pipeline_build_coaching
            if pattern == RampPattern.first_deal_stall:
                return RampAction.deal_progression_coaching
            return RampAction.manager_led_intervention
        if risk == RampRisk.moderate:
            if pattern == RampPattern.activity_adoption_lag:
                return RampAction.activity_habits_coaching
            return RampAction.pipeline_build_coaching
        return RampAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_ramp_gap(self, composite: float, inp: RampInput) -> bool:
        return (
            composite >= 40
            or inp.pipeline_build_pct_of_target <= 0.40
            or inp.peer_benchmark_percentile <= 0.25
        )

    def _requires_ramp_intervention(self, composite: float, inp: RampInput) -> bool:
        return (
            composite >= 30
            or inp.coaching_action_completion_pct <= 0.50
            or inp.expected_first_quarter_attainment_pct <= 0.50
        )

    # ------------------------------------------------------------------
    # Revenue loss estimate
    # ------------------------------------------------------------------

    def _estimated_ramp_revenue_loss(self, inp: RampInput, composite: float) -> float:
        ramp_fraction = inp.ramp_week / max(inp.target_ramp_weeks, 1)
        attainment_gap = max(0.0, 1.0 - inp.expected_first_quarter_attainment_pct)
        return round(
            inp.deals_in_pipeline
            * inp.avg_opportunity_value_usd
            * attainment_gap
            * (composite / 100.0)
            * ramp_fraction,
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: RampInput,
                 pattern: RampPattern, composite: float) -> str:
        if pattern == RampPattern.none and composite < 20:
            return "Ramp progression healthy — pipeline build, activity adoption, and coaching engagement within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.pipeline_build_pct_of_target * 100:.0f}% pipeline target built")
        parts.append(f"{inp.activity_adoption_score_pct * 100:.0f}% activity adoption")
        parts.append(f"week {inp.ramp_week} of {inp.target_ramp_weeks}")
        label = pattern.value.replace("_", " ") if pattern != RampPattern.none else "Ramp risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: RampInput) -> RampResult:
        pipeline    = round(self._pipeline_score(inp), 1)
        activity    = round(self._activity_score(inp), 1)
        coaching    = round(self._coaching_score(inp), 1)
        progression = round(self._progression_score(inp), 1)

        composite = round(
            pipeline * 0.35 + activity * 0.30 + coaching * 0.20 + progression * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, pipeline, activity, coaching, progression)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_ramp_gap(composite, inp)
        interv = self._requires_ramp_intervention(composite, inp)
        loss   = self._estimated_ramp_revenue_loss(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = RampResult(
            rep_id=inp.rep_id,
            region=inp.region,
            ramp_risk=risk,
            ramp_pattern=pattern,
            ramp_severity=severity,
            recommended_action=action,
            pipeline_score=pipeline,
            activity_score=activity,
            coaching_score=coaching,
            progression_score=progression,
            ramp_composite=composite,
            has_ramp_gap=gap,
            requires_ramp_intervention=interv,
            estimated_ramp_revenue_loss_usd=loss,
            ramp_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[RampInput]) -> list[RampResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_ramp_composite": 0.0,
                "ramp_gap_count": 0,
                "intervention_count": 0,
                "avg_pipeline_score": 0.0,
                "avg_activity_score": 0.0,
                "avg_coaching_score": 0.0,
                "avg_progression_score": 0.0,
                "total_estimated_ramp_revenue_loss_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_pip = total_act = total_coa = total_pro = total_loss = 0.0

        for r in self._results:
            risk_counts[r.ramp_risk.value]         = risk_counts.get(r.ramp_risk.value, 0) + 1
            pattern_counts[r.ramp_pattern.value]   = pattern_counts.get(r.ramp_pattern.value, 0) + 1
            severity_counts[r.ramp_severity.value] = severity_counts.get(r.ramp_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.ramp_composite
            total_pip  += r.pipeline_score
            total_act  += r.activity_score
            total_coa  += r.coaching_score
            total_pro  += r.progression_score
            total_loss += r.estimated_ramp_revenue_loss_usd

        n = len(self._results)

        return {
            "total":                                     n,
            "risk_counts":                               risk_counts,
            "pattern_counts":                            pattern_counts,
            "severity_counts":                           severity_counts,
            "action_counts":                             action_counts,
            "avg_ramp_composite":                        round(total_comp / n, 1),
            "ramp_gap_count":                            sum(1 for r in self._results if r.has_ramp_gap),
            "intervention_count":                        sum(1 for r in self._results if r.requires_ramp_intervention),
            "avg_pipeline_score":                        round(total_pip / n, 1),
            "avg_activity_score":                        round(total_act / n, 1),
            "avg_coaching_score":                        round(total_coa / n, 1),
            "avg_progression_score":                     round(total_pro / n, 1),
            "total_estimated_ramp_revenue_loss_usd":     round(total_loss, 2),
        }
