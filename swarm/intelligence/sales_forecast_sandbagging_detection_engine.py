from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class SandbaggingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class SandbaggingPattern(str, Enum):
    none                    = "none"
    consistent_upside       = "consistent_upside"
    late_quarter_surge      = "late_quarter_surge"
    commit_minimization     = "commit_minimization"
    deal_timing_manipulation= "deal_timing_manipulation"
    forecast_sandbagging    = "forecast_sandbagging"


class SandbaggingSeverity(str, Enum):
    accurate    = "accurate"
    watch       = "watch"
    suspected   = "suspected"
    confirmed   = "confirmed"


class SandbaggingAction(str, Enum):
    no_action               = "no_action"
    forecast_coaching       = "forecast_coaching"
    pipeline_review         = "pipeline_review"
    comp_plan_review        = "comp_plan_review"
    executive_confrontation = "executive_confrontation"


@dataclass
class SandbaggingInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    committed_forecast_usd: float
    actual_closed_usd: float
    prior_period_upside_usd: float
    upside_to_commit_ratio: float
    deals_pulled_from_next_quarter: int
    late_stage_deals_not_committed: int
    forecast_accuracy_last_3_periods: float
    consecutive_upside_periods: int
    commit_vs_pipeline_coverage_ratio: float
    avg_deal_slip_days: float
    deals_slipped_intentionally_count: int
    close_date_pushed_count: int
    close_date_pulled_count: int
    sandbagged_deal_value_usd: float
    quota_attainment_last_period_pct: float
    accelerator_threshold_pct: float
    days_remaining_in_period: int
    total_pipeline_usd: float
    crm_stage_inflation_score: float


@dataclass
class SandbaggingResult:
    rep_id: str
    region: str
    sandbagging_risk: SandbaggingRisk
    sandbagging_pattern: SandbaggingPattern
    sandbagging_severity: SandbaggingSeverity
    recommended_action: SandbaggingAction
    commit_accuracy_score: float
    upside_manipulation_score: float
    deal_timing_score: float
    pattern_consistency_score: float
    sandbagging_composite: float
    is_sandbagging: bool
    requires_intervention: bool
    estimated_hidden_revenue_usd: float
    sandbagging_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "sandbagging_risk":             self.sandbagging_risk.value,
            "sandbagging_pattern":          self.sandbagging_pattern.value,
            "sandbagging_severity":         self.sandbagging_severity.value,
            "recommended_action":           self.recommended_action.value,
            "commit_accuracy_score":        self.commit_accuracy_score,
            "upside_manipulation_score":    self.upside_manipulation_score,
            "deal_timing_score":            self.deal_timing_score,
            "pattern_consistency_score":    self.pattern_consistency_score,
            "sandbagging_composite":        self.sandbagging_composite,
            "is_sandbagging":               self.is_sandbagging,
            "requires_intervention":        self.requires_intervention,
            "estimated_hidden_revenue_usd": self.estimated_hidden_revenue_usd,
            "sandbagging_signal":           self.sandbagging_signal,
        }


class SalesForecastSandbaggingDetectionEngine:

    def __init__(self) -> None:
        self._results: list[SandbaggingResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100)
    # ------------------------------------------------------------------

    def _commit_accuracy_score(self, inp: SandbaggingInput) -> float:
        score = 0.0

        # Upside over commit — how much more they closed vs committed
        if inp.committed_forecast_usd > 0:
            upside_ratio = (inp.actual_closed_usd - inp.committed_forecast_usd) / inp.committed_forecast_usd
            if upside_ratio >= 0.50:
                score += 40.0
            elif upside_ratio >= 0.30:
                score += 28.0
            elif upside_ratio >= 0.15:
                score += 14.0

        # Historical forecast accuracy (low accuracy = sandbagger)
        if inp.forecast_accuracy_last_3_periods < 0.60:
            score += 30.0
        elif inp.forecast_accuracy_last_3_periods < 0.75:
            score += 15.0
        elif inp.forecast_accuracy_last_3_periods < 0.85:
            score += 5.0

        # Commit vs pipeline coverage — low commit relative to visible pipeline
        if inp.commit_vs_pipeline_coverage_ratio < 0.30:
            score += 20.0
        elif inp.commit_vs_pipeline_coverage_ratio < 0.45:
            score += 10.0

        # Late stage deals not committed
        if inp.late_stage_deals_not_committed >= 5:
            score += 10.0
        elif inp.late_stage_deals_not_committed >= 3:
            score += 5.0

        return min(score, 100.0)

    def _upside_manipulation_score(self, inp: SandbaggingInput) -> float:
        score = 0.0

        # Upside-to-commit ratio signals chronic lowballing
        if inp.upside_to_commit_ratio >= 3.0:
            score += 45.0
        elif inp.upside_to_commit_ratio >= 2.0:
            score += 28.0
        elif inp.upside_to_commit_ratio >= 1.5:
            score += 14.0

        # Consecutive upside periods — structural pattern
        if inp.consecutive_upside_periods >= 4:
            score += 30.0
        elif inp.consecutive_upside_periods >= 2:
            score += 15.0

        # Known sandbagged deal value
        if inp.sandbagged_deal_value_usd > 0 and inp.committed_forecast_usd > 0:
            sbag_ratio = inp.sandbagged_deal_value_usd / inp.committed_forecast_usd
            if sbag_ratio >= 0.40:
                score += 25.0
            elif sbag_ratio >= 0.20:
                score += 12.0

        return min(score, 100.0)

    def _deal_timing_score(self, inp: SandbaggingInput) -> float:
        score = 0.0

        # Deals pulled from next quarter (accelerating to beat quota)
        if inp.deals_pulled_from_next_quarter >= 4:
            score += 35.0
        elif inp.deals_pulled_from_next_quarter >= 2:
            score += 20.0
        elif inp.deals_pulled_from_next_quarter >= 1:
            score += 10.0

        # Intentional slippage count
        if inp.deals_slipped_intentionally_count >= 3:
            score += 30.0
        elif inp.deals_slipped_intentionally_count >= 1:
            score += 15.0

        # Close date manipulation ratio
        total_moves = inp.close_date_pushed_count + inp.close_date_pulled_count
        if total_moves > 0:
            pull_ratio = inp.close_date_pulled_count / total_moves
            if pull_ratio >= 0.60:
                score += 20.0
            elif pull_ratio >= 0.40:
                score += 10.0

        # Average slip days — long slips = timing games
        if inp.avg_deal_slip_days >= 30:
            score += 15.0
        elif inp.avg_deal_slip_days >= 15:
            score += 7.0

        return min(score, 100.0)

    def _pattern_consistency_score(self, inp: SandbaggingInput) -> float:
        score = 0.0

        # CRM stage inflation (deals over-staged to hide from manager)
        if inp.crm_stage_inflation_score >= 70.0:
            score += 40.0
        elif inp.crm_stage_inflation_score >= 50.0:
            score += 22.0
        elif inp.crm_stage_inflation_score >= 30.0:
            score += 10.0

        # Prior period upside relative to current committed
        if inp.committed_forecast_usd > 0 and inp.prior_period_upside_usd > 0:
            hist_ratio = inp.prior_period_upside_usd / inp.committed_forecast_usd
            if hist_ratio >= 0.50:
                score += 30.0
            elif hist_ratio >= 0.25:
                score += 15.0

        # High attainment last period (likely over-achieved due to sandbagging)
        if inp.quota_attainment_last_period_pct >= 140.0:
            score += 20.0
        elif inp.quota_attainment_last_period_pct >= 120.0:
            score += 10.0

        # Accelerator threshold gaming (commit just above threshold)
        if 0 < inp.accelerator_threshold_pct <= 105.0 and inp.quota_attainment_last_period_pct >= 100.0:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: SandbaggingInput,
                         commit: float, upside: float,
                         timing: float, consistency: float) -> SandbaggingPattern:
        # Priority: forecast_sandbagging > deal_timing_manipulation > commit_minimization
        #           > late_quarter_surge > consistent_upside > none
        if commit >= 30 and upside >= 30 and consistency >= 20:
            return SandbaggingPattern.forecast_sandbagging
        if timing >= 35 and inp.deals_pulled_from_next_quarter >= 2:
            return SandbaggingPattern.deal_timing_manipulation
        if commit >= 25 and inp.late_stage_deals_not_committed >= 3:
            return SandbaggingPattern.commit_minimization
        if inp.days_remaining_in_period <= 14 and inp.close_date_pulled_count >= 2:
            return SandbaggingPattern.late_quarter_surge
        if inp.consecutive_upside_periods >= 2:
            return SandbaggingPattern.consistent_upside
        return SandbaggingPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> SandbaggingRisk:
        if composite >= 60:
            return SandbaggingRisk.critical
        if composite >= 40:
            return SandbaggingRisk.high
        if composite >= 20:
            return SandbaggingRisk.moderate
        return SandbaggingRisk.low

    def _severity(self, composite: float) -> SandbaggingSeverity:
        if composite >= 60:
            return SandbaggingSeverity.confirmed
        if composite >= 40:
            return SandbaggingSeverity.suspected
        if composite >= 20:
            return SandbaggingSeverity.watch
        return SandbaggingSeverity.accurate

    def _action(self, risk: SandbaggingRisk, composite: float) -> SandbaggingAction:
        if risk == SandbaggingRisk.critical:
            return SandbaggingAction.executive_confrontation
        if risk == SandbaggingRisk.high:
            return SandbaggingAction.comp_plan_review
        if risk == SandbaggingRisk.moderate:
            return SandbaggingAction.pipeline_review
        if composite >= 10:
            return SandbaggingAction.forecast_coaching
        return SandbaggingAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _is_sandbagging(self, composite: float, inp: SandbaggingInput) -> bool:
        return (
            composite >= 40
            or inp.consecutive_upside_periods >= 3
            or (inp.committed_forecast_usd > 0 and
                (inp.actual_closed_usd - inp.committed_forecast_usd) / inp.committed_forecast_usd >= 0.40)
        )

    def _requires_intervention(self, composite: float, inp: SandbaggingInput) -> bool:
        return (
            composite >= 30
            or inp.sandbagged_deal_value_usd >= 50_000
            or inp.deals_slipped_intentionally_count >= 2
        )

    # ------------------------------------------------------------------
    # Hidden revenue estimate
    # ------------------------------------------------------------------

    def _hidden_revenue(self, inp: SandbaggingInput, composite: float) -> float:
        return round(inp.sandbagged_deal_value_usd * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: SandbaggingInput, pattern: SandbaggingPattern,
                composite: float) -> str:
        if composite < 5 and pattern == SandbaggingPattern.none:
            return "Forecast accuracy within expected variance — no sandbagging signals"
        parts: list[str] = []
        if inp.committed_forecast_usd > 0:
            upside_ratio = (inp.actual_closed_usd - inp.committed_forecast_usd) / inp.committed_forecast_usd
            if upside_ratio >= 0.15:
                parts.append(f"{upside_ratio*100:.0f}% over commit")
        if inp.consecutive_upside_periods >= 2:
            parts.append(f"{inp.consecutive_upside_periods} consecutive upside periods")
        if inp.deals_pulled_from_next_quarter >= 1:
            parts.append(f"{inp.deals_pulled_from_next_quarter} deals pulled from Q+1")
        if inp.deals_slipped_intentionally_count >= 1:
            parts.append(f"{inp.deals_slipped_intentionally_count} intentional slips")
        if inp.late_stage_deals_not_committed >= 2:
            parts.append(f"{inp.late_stage_deals_not_committed} late-stage deals withheld")
        label = pattern.value.replace("_", " ")
        summary = " — ".join(parts) if parts else "sandbagging indicators present"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: SandbaggingInput) -> SandbaggingResult:
        c = round(self._commit_accuracy_score(inp), 1)
        u = round(self._upside_manipulation_score(inp), 1)
        t = round(self._deal_timing_score(inp), 1)
        p = round(self._pattern_consistency_score(inp), 1)

        composite = round(c * 0.35 + u * 0.30 + t * 0.20 + p * 0.15, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, c, u, t, p)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, composite)

        is_sb = self._is_sandbagging(composite, inp)
        is_ri = self._requires_intervention(composite, inp)
        cost  = self._hidden_revenue(inp, composite)
        signal= self._signal(inp, pattern, composite)

        result = SandbaggingResult(
            rep_id=inp.rep_id,
            region=inp.region,
            sandbagging_risk=risk,
            sandbagging_pattern=pattern,
            sandbagging_severity=severity,
            recommended_action=action,
            commit_accuracy_score=c,
            upside_manipulation_score=u,
            deal_timing_score=t,
            pattern_consistency_score=p,
            sandbagging_composite=composite,
            is_sandbagging=is_sb,
            requires_intervention=is_ri,
            estimated_hidden_revenue_usd=cost,
            sandbagging_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[SandbaggingInput]) -> list[SandbaggingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_sandbagging_composite": 0.0,
                "sandbagging_count": 0,
                "intervention_count": 0,
                "avg_commit_accuracy_score": 0.0,
                "avg_upside_manipulation_score": 0.0,
                "avg_deal_timing_score": 0.0,
                "avg_pattern_consistency_score": 0.0,
                "total_estimated_hidden_revenue_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_c = total_u = total_t = total_p = total_rev = 0.0

        for r in self._results:
            risk_counts[r.sandbagging_risk.value]       = risk_counts.get(r.sandbagging_risk.value, 0) + 1
            pattern_counts[r.sandbagging_pattern.value] = pattern_counts.get(r.sandbagging_pattern.value, 0) + 1
            severity_counts[r.sandbagging_severity.value] = severity_counts.get(r.sandbagging_severity.value, 0) + 1
            action_counts[r.recommended_action.value]   = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.sandbagging_composite
            total_c    += r.commit_accuracy_score
            total_u    += r.upside_manipulation_score
            total_t    += r.deal_timing_score
            total_p    += r.pattern_consistency_score
            total_rev  += r.estimated_hidden_revenue_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_sandbagging_composite":            round(total_comp / n, 1),
            "sandbagging_count":                    sum(1 for r in self._results if r.is_sandbagging),
            "intervention_count":                   sum(1 for r in self._results if r.requires_intervention),
            "avg_commit_accuracy_score":            round(total_c / n, 1),
            "avg_upside_manipulation_score":        round(total_u / n, 1),
            "avg_deal_timing_score":                round(total_t / n, 1),
            "avg_pattern_consistency_score":        round(total_p / n, 1),
            "total_estimated_hidden_revenue_usd":   round(total_rev, 2),
        }
