from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class OnboardingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class OnboardingPattern(str, Enum):
    none                    = "none"
    slow_ramp               = "slow_ramp"
    training_gap            = "training_gap"
    manager_neglect         = "manager_neglect"
    early_attrition_signal  = "early_attrition_signal"
    product_knowledge_gap   = "product_knowledge_gap"


class OnboardingSeverity(str, Enum):
    ramping     = "ramping"
    developing  = "developing"
    struggling  = "struggling"
    at_risk     = "at_risk"


class OnboardingAction(str, Enum):
    no_action                      = "no_action"
    ramp_support_coaching          = "ramp_support_coaching"
    training_acceleration_plan     = "training_acceleration_plan"
    manager_engagement_review      = "manager_engagement_review"
    early_retention_intervention   = "early_retention_intervention"
    product_enablement_bootcamp    = "product_enablement_bootcamp"


@dataclass
class OnboardingEffectivenessInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    days_since_start: int
    days_to_first_meeting: int
    days_to_first_opportunity: int
    days_to_first_closed_deal: int
    training_modules_completed_pct: float
    product_certification_completed: bool
    manager_1on1_count: int
    expected_manager_1on1_count: int
    mentor_sessions_count: int
    pipeline_coverage_vs_ramp_target_pct: float
    quota_attainment_week_8_pct: float
    quota_attainment_week_16_pct: float
    crm_adoption_score: float
    avg_activity_score_vs_team_pct: float
    deals_in_pipeline_count: int
    avg_deal_size_vs_team_pct: float
    sentiment_score: float
    late_crm_update_rate_pct: float
    avg_opportunity_value_usd: float


@dataclass
class OnboardingEffectivenessResult:
    rep_id: str
    region: str
    onboarding_risk: OnboardingRisk
    onboarding_pattern: OnboardingPattern
    onboarding_severity: OnboardingSeverity
    recommended_action: OnboardingAction
    ramp_velocity_score: float
    training_completion_score: float
    manager_support_score: float
    early_performance_score: float
    onboarding_composite: float
    has_onboarding_gap: bool
    requires_onboarding_intervention: bool
    estimated_ramp_delay_cost_usd: float
    onboarding_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "onboarding_risk":                  self.onboarding_risk.value,
            "onboarding_pattern":               self.onboarding_pattern.value,
            "onboarding_severity":              self.onboarding_severity.value,
            "recommended_action":               self.recommended_action.value,
            "ramp_velocity_score":              self.ramp_velocity_score,
            "training_completion_score":        self.training_completion_score,
            "manager_support_score":            self.manager_support_score,
            "early_performance_score":          self.early_performance_score,
            "onboarding_composite":             self.onboarding_composite,
            "has_onboarding_gap":               self.has_onboarding_gap,
            "requires_onboarding_intervention": self.requires_onboarding_intervention,
            "estimated_ramp_delay_cost_usd":    self.estimated_ramp_delay_cost_usd,
            "onboarding_signal":                self.onboarding_signal,
        }


class SalesOnboardingEffectivenessIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[OnboardingEffectivenessResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _ramp_velocity_score(self, inp: OnboardingEffectivenessInput) -> float:
        score = 0.0

        if inp.days_to_first_opportunity >= 60:
            score += 35.0
        elif inp.days_to_first_opportunity >= 45:
            score += 20.0
        elif inp.days_to_first_opportunity >= 30:
            score += 8.0

        if inp.days_to_first_closed_deal >= 120:
            score += 35.0
        elif inp.days_to_first_closed_deal >= 90:
            score += 18.0
        elif inp.days_to_first_closed_deal >= 60:
            score += 7.0

        if inp.pipeline_coverage_vs_ramp_target_pct < 0.50:
            score += 25.0
        elif inp.pipeline_coverage_vs_ramp_target_pct < 0.75:
            score += 12.0

        return min(score, 100.0)

    def _training_completion_score(self, inp: OnboardingEffectivenessInput) -> float:
        score = 0.0

        if inp.training_modules_completed_pct < 0.40:
            score += 40.0
        elif inp.training_modules_completed_pct < 0.60:
            score += 22.0
        elif inp.training_modules_completed_pct < 0.80:
            score += 8.0

        if not inp.product_certification_completed and inp.days_since_start >= 60:
            score += 30.0
        elif not inp.product_certification_completed and inp.days_since_start >= 30:
            score += 15.0

        if inp.crm_adoption_score < 0.40:
            score += 25.0
        elif inp.crm_adoption_score < 0.60:
            score += 12.0

        return min(score, 100.0)

    def _manager_support_score(self, inp: OnboardingEffectivenessInput) -> float:
        score = 0.0

        expected = max(inp.expected_manager_1on1_count, 1)
        completion_rate = inp.manager_1on1_count / expected
        if completion_rate < 0.40:
            score += 40.0
        elif completion_rate < 0.60:
            score += 22.0
        elif completion_rate < 0.80:
            score += 8.0

        if inp.mentor_sessions_count == 0 and inp.days_since_start >= 30:
            score += 30.0
        elif inp.mentor_sessions_count <= 1 and inp.days_since_start >= 60:
            score += 15.0

        if inp.avg_activity_score_vs_team_pct < 0.50:
            score += 25.0
        elif inp.avg_activity_score_vs_team_pct < 0.70:
            score += 12.0

        return min(score, 100.0)

    def _early_performance_score(self, inp: OnboardingEffectivenessInput) -> float:
        score = 0.0

        if inp.days_since_start >= 60 and inp.quota_attainment_week_8_pct < 0.20:
            score += 35.0
        elif inp.days_since_start >= 60 and inp.quota_attainment_week_8_pct < 0.40:
            score += 18.0

        if inp.days_since_start >= 120 and inp.quota_attainment_week_16_pct < 0.40:
            score += 35.0
        elif inp.days_since_start >= 120 and inp.quota_attainment_week_16_pct < 0.60:
            score += 18.0

        if inp.sentiment_score < 0.30:
            score += 20.0
        elif inp.sentiment_score < 0.50:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: OnboardingEffectivenessInput,
                          ramp: float, training: float,
                          manager: float, performance: float) -> OnboardingPattern:
        if inp.sentiment_score < 0.30 and performance >= 25:
            return OnboardingPattern.early_attrition_signal

        if manager >= 35 and inp.manager_1on1_count < inp.expected_manager_1on1_count * 0.50:
            return OnboardingPattern.manager_neglect

        if training >= 30 and inp.training_modules_completed_pct < 0.60:
            return OnboardingPattern.training_gap

        if not inp.product_certification_completed and inp.days_since_start >= 60 and training >= 20:
            return OnboardingPattern.product_knowledge_gap

        if ramp >= 25 and inp.pipeline_coverage_vs_ramp_target_pct < 0.60:
            return OnboardingPattern.slow_ramp

        return OnboardingPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> OnboardingRisk:
        if composite >= 60:
            return OnboardingRisk.critical
        if composite >= 40:
            return OnboardingRisk.high
        if composite >= 20:
            return OnboardingRisk.moderate
        return OnboardingRisk.low

    def _severity(self, composite: float) -> OnboardingSeverity:
        if composite >= 60:
            return OnboardingSeverity.at_risk
        if composite >= 40:
            return OnboardingSeverity.struggling
        if composite >= 20:
            return OnboardingSeverity.developing
        return OnboardingSeverity.ramping

    def _action(self, risk: OnboardingRisk, pattern: OnboardingPattern) -> OnboardingAction:
        if risk == OnboardingRisk.critical:
            if pattern == OnboardingPattern.early_attrition_signal:
                return OnboardingAction.early_retention_intervention
            if pattern == OnboardingPattern.manager_neglect:
                return OnboardingAction.manager_engagement_review
            return OnboardingAction.early_retention_intervention
        if risk == OnboardingRisk.high:
            if pattern == OnboardingPattern.training_gap:
                return OnboardingAction.training_acceleration_plan
            if pattern == OnboardingPattern.product_knowledge_gap:
                return OnboardingAction.product_enablement_bootcamp
            return OnboardingAction.ramp_support_coaching
        if risk == OnboardingRisk.moderate:
            return OnboardingAction.ramp_support_coaching
        return OnboardingAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_onboarding_gap(self, composite: float,
                              inp: OnboardingEffectivenessInput) -> bool:
        return (
            composite >= 40
            or inp.training_modules_completed_pct < 0.40
            or inp.pipeline_coverage_vs_ramp_target_pct < 0.50
        )

    def _requires_onboarding_intervention(self, composite: float,
                                            inp: OnboardingEffectivenessInput) -> bool:
        expected = max(inp.expected_manager_1on1_count, 1)
        return (
            composite >= 30
            or inp.sentiment_score < 0.40
            or inp.manager_1on1_count / expected < 0.50
        )

    # ------------------------------------------------------------------
    # Ramp delay cost
    # ------------------------------------------------------------------

    def _estimated_ramp_delay_cost(self, inp: OnboardingEffectivenessInput,
                                    composite: float) -> float:
        expected_deals_per_month = 2.0
        delay_months = max(0.0, (composite / 100.0) * 3.0)
        return round(expected_deals_per_month * delay_months * inp.avg_opportunity_value_usd, 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: OnboardingEffectivenessInput,
                 pattern: OnboardingPattern, composite: float) -> str:
        if pattern == OnboardingPattern.none and composite < 20:
            return "Onboarding velocity healthy — rep progressing within expected ramp benchmarks"
        parts: list[str] = []
        if inp.training_modules_completed_pct < 1.0:
            parts.append(f"{inp.training_modules_completed_pct*100:.0f}% training complete")
        if inp.pipeline_coverage_vs_ramp_target_pct < 1.0:
            parts.append(f"{inp.pipeline_coverage_vs_ramp_target_pct*100:.0f}% pipeline target")
        expected = max(inp.expected_manager_1on1_count, 1)
        mgr_rate = inp.manager_1on1_count / expected
        if mgr_rate < 1.0:
            parts.append(f"{mgr_rate*100:.0f}% manager 1:1 attendance")
        label = pattern.value.replace("_", " ") if pattern != OnboardingPattern.none else "Onboarding risk"
        summary = " — ".join(parts) if parts else "ramp velocity declining"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: OnboardingEffectivenessInput) -> OnboardingEffectivenessResult:
        ramp        = round(self._ramp_velocity_score(inp), 1)
        training    = round(self._training_completion_score(inp), 1)
        manager     = round(self._manager_support_score(inp), 1)
        performance = round(self._early_performance_score(inp), 1)

        composite = round(
            ramp * 0.30 + training * 0.30 + manager * 0.25 + performance * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, ramp, training, manager, performance)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap          = self._has_onboarding_gap(composite, inp)
        intervention = self._requires_onboarding_intervention(composite, inp)
        delay_cost   = self._estimated_ramp_delay_cost(inp, composite)
        signal       = self._signal(inp, pattern, composite)

        result = OnboardingEffectivenessResult(
            rep_id=inp.rep_id,
            region=inp.region,
            onboarding_risk=risk,
            onboarding_pattern=pattern,
            onboarding_severity=severity,
            recommended_action=action,
            ramp_velocity_score=ramp,
            training_completion_score=training,
            manager_support_score=manager,
            early_performance_score=performance,
            onboarding_composite=composite,
            has_onboarding_gap=gap,
            requires_onboarding_intervention=intervention,
            estimated_ramp_delay_cost_usd=delay_cost,
            onboarding_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[OnboardingEffectivenessInput]) -> list[OnboardingEffectivenessResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_onboarding_composite": 0.0,
                "onboarding_gap_count": 0,
                "intervention_count": 0,
                "avg_ramp_velocity_score": 0.0,
                "avg_training_completion_score": 0.0,
                "avg_manager_support_score": 0.0,
                "avg_early_performance_score": 0.0,
                "total_estimated_ramp_delay_cost_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_ramp = total_train = total_mgr = total_perf = total_cost = 0.0

        for r in self._results:
            risk_counts[r.onboarding_risk.value]       = risk_counts.get(r.onboarding_risk.value, 0) + 1
            pattern_counts[r.onboarding_pattern.value] = pattern_counts.get(r.onboarding_pattern.value, 0) + 1
            severity_counts[r.onboarding_severity.value] = severity_counts.get(r.onboarding_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.onboarding_composite
            total_ramp  += r.ramp_velocity_score
            total_train += r.training_completion_score
            total_mgr   += r.manager_support_score
            total_perf  += r.early_performance_score
            total_cost  += r.estimated_ramp_delay_cost_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_onboarding_composite":                 round(total_comp / n, 1),
            "onboarding_gap_count":                     sum(1 for r in self._results if r.has_onboarding_gap),
            "intervention_count":                       sum(1 for r in self._results if r.requires_onboarding_intervention),
            "avg_ramp_velocity_score":                  round(total_ramp / n, 1),
            "avg_training_completion_score":            round(total_train / n, 1),
            "avg_manager_support_score":                round(total_mgr / n, 1),
            "avg_early_performance_score":              round(total_perf / n, 1),
            "total_estimated_ramp_delay_cost_usd":      round(total_cost, 2),
        }
