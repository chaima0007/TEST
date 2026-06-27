from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AttainmentTier(str, Enum):
    OVERACHIEVER  = "overachiever"    # ≥ 110%
    ON_TRACK      = "on_track"        # ≥ 90%
    AT_RISK       = "at_risk"         # ≥ 70%
    BEHIND        = "behind"          # ≥ 50%
    CRITICAL      = "critical"        # < 50%


class GapRisk(str, Enum):
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"


class PipelineCoverage(str, Enum):
    STRONG     = "strong"      # pipeline ≥ 3× gap
    ADEQUATE   = "adequate"    # pipeline ≥ 2× gap
    THIN       = "thin"        # pipeline ≥ 1× gap
    INSUFFICIENT = "insufficient"  # pipeline < 1× gap


class QuotaAction(str, Enum):
    ACCELERATE_PIPELINE   = "accelerate_pipeline"
    FOCUS_LATE_STAGE      = "focus_late_stage"
    BUILD_PIPELINE        = "build_pipeline"
    EXECUTIVE_INTERVENTION = "executive_intervention"
    MAINTAIN_PACE         = "maintain_pace"
    CELEBRATE_AND_EXPAND  = "celebrate_and_expand"


@dataclass
class QuotaGapInput:
    rep_id:                 str
    rep_name:               str
    manager_id:             str
    region:                 str
    segment:                str        # "smb", "mid_market", "enterprise"
    annual_quota:           float
    period_quota:           float      # quota for current period (e.g. quarter)
    closed_won_value:       float      # booked revenue this period
    commit_value:           float      # committed deals (likely to close)
    best_case_value:        float      # best-case pipeline value
    pipeline_value:         float      # total open pipeline
    late_stage_value:       float      # pipeline in late stages (proposal+)
    days_in_period:         int        # total days in period
    days_remaining:         int        # days left in period
    avg_deal_size:          float      # rep's average deal size
    win_rate:               float      # historical win rate 0–1
    avg_sales_cycle_days:   int        # average cycle length
    deals_in_pipeline:      int        # count of active deals
    overdue_deals:          int        # deals past expected close date
    last_activity_days:     int        # days since last CRM activity
    is_ramping:             bool       # new rep still in ramp period
    ramp_factor:            float      # effective quota multiplier during ramp (e.g. 0.75)


@dataclass
class QuotaGapResult:
    rep_id:                 str
    rep_name:               str
    manager_id:             str
    gap_to_quota:           float      # period_quota - closed_won_value (0 if over quota)
    attainment_pct:         float      # closed_won_value / period_quota × 100
    attainment_tier:        AttainmentTier
    projected_attainment:   float      # projected close by period end (%)
    gap_risk:               GapRisk
    pipeline_coverage:      PipelineCoverage
    recommended_action:     QuotaAction
    required_win_rate:      float      # win rate needed to close gap with current pipeline
    deals_needed:           int        # deals needed at avg size to close gap
    days_remaining:         int
    quota_achievement_score: float     # 0–100 composite
    pipeline_health_score:  float      # 0–100
    is_at_risk:             bool
    effective_quota:        float      # adjusted quota (ramp-corrected)

    def to_dict(self) -> dict:
        return {
            "rep_id":                   self.rep_id,
            "rep_name":                 self.rep_name,
            "gap_to_quota":             self.gap_to_quota,
            "attainment_pct":           self.attainment_pct,
            "attainment_tier":          self.attainment_tier.value,
            "projected_attainment":     self.projected_attainment,
            "gap_risk":                 self.gap_risk.value,
            "pipeline_coverage":        self.pipeline_coverage.value,
            "recommended_action":       self.recommended_action.value,
            "required_win_rate":        self.required_win_rate,
            "deals_needed":             self.deals_needed,
            "quota_achievement_score":  self.quota_achievement_score,
            "pipeline_health_score":    self.pipeline_health_score,
            "is_at_risk":               self.is_at_risk,
            "effective_quota":          self.effective_quota,
        }


class QuotaGapAnalysisEngine:
    def __init__(self) -> None:
        self._results: list[QuotaGapResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: QuotaGapInput) -> QuotaGapResult:
        effective_quota  = self._effective_quota(inp)
        gap              = self._gap_to_quota(inp, effective_quota)
        attainment_pct   = self._attainment_pct(inp, effective_quota)
        tier             = self._attainment_tier(attainment_pct)
        projected        = self._projected_attainment(inp, effective_quota)
        pipeline_cov     = self._pipeline_coverage(inp, gap)
        req_win_rate     = self._required_win_rate(inp, gap)
        deals_needed     = self._deals_needed(inp, gap)
        ach_score        = self._achievement_score(inp, attainment_pct, projected)
        pipe_health      = self._pipeline_health_score(inp)
        gap_risk         = self._gap_risk(inp, attainment_pct, projected, pipeline_cov)
        action           = self._recommended_action(inp, gap_risk, pipeline_cov, attainment_pct)
        at_risk          = gap_risk in (GapRisk.HIGH, GapRisk.CRITICAL)

        result = QuotaGapResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            manager_id=inp.manager_id,
            gap_to_quota=round(gap, 2),
            attainment_pct=attainment_pct,
            attainment_tier=tier,
            projected_attainment=projected,
            gap_risk=gap_risk,
            pipeline_coverage=pipeline_cov,
            recommended_action=action,
            required_win_rate=req_win_rate,
            deals_needed=deals_needed,
            days_remaining=inp.days_remaining,
            quota_achievement_score=ach_score,
            pipeline_health_score=pipe_health,
            is_at_risk=at_risk,
            effective_quota=round(effective_quota, 2),
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[QuotaGapInput]
    ) -> list[QuotaGapResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def at_risk_reps(self) -> list[QuotaGapResult]:
        return [r for r in self._results if r.is_at_risk]

    @property
    def overachievers(self) -> list[QuotaGapResult]:
        return [r for r in self._results
                if r.attainment_tier == AttainmentTier.OVERACHIEVER]

    @property
    def critical_reps(self) -> list[QuotaGapResult]:
        return [r for r in self._results
                if r.gap_risk == GapRisk.CRITICAL]

    @property
    def total_gap(self) -> float:
        return round(sum(r.gap_to_quota for r in self._results), 2)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _effective_quota(self, inp: QuotaGapInput) -> float:
        if inp.is_ramping and 0 < inp.ramp_factor < 1:
            return inp.period_quota * inp.ramp_factor
        return inp.period_quota

    def _gap_to_quota(self, inp: QuotaGapInput, effective_quota: float) -> float:
        return max(0.0, effective_quota - inp.closed_won_value)

    def _attainment_pct(self, inp: QuotaGapInput, effective_quota: float) -> float:
        if effective_quota <= 0:
            return 100.0
        return round((inp.closed_won_value / effective_quota) * 100, 1)

    def _attainment_tier(self, pct: float) -> AttainmentTier:
        if pct >= 110: return AttainmentTier.OVERACHIEVER
        if pct >= 90:  return AttainmentTier.ON_TRACK
        if pct >= 70:  return AttainmentTier.AT_RISK
        if pct >= 50:  return AttainmentTier.BEHIND
        return AttainmentTier.CRITICAL

    def _projected_attainment(self, inp: QuotaGapInput, effective_quota: float) -> float:
        if effective_quota <= 0:
            return 100.0
        if inp.days_in_period <= 0:
            return self._attainment_pct(inp, effective_quota)

        days_elapsed = max(1, inp.days_in_period - inp.days_remaining)
        run_rate     = inp.closed_won_value / days_elapsed   # won per day
        projected_won = inp.closed_won_value + (run_rate * inp.days_remaining)

        # Blend with pipeline (commit + win_rate × late stage)
        pipeline_contribution = (
            inp.commit_value + inp.win_rate * inp.late_stage_value * 0.5
        )
        blended = projected_won * 0.6 + (inp.closed_won_value + pipeline_contribution) * 0.4

        return round(min(200.0, (blended / effective_quota) * 100), 1)

    def _pipeline_coverage(
        self, inp: QuotaGapInput, gap: float
    ) -> PipelineCoverage:
        if gap <= 0:
            return PipelineCoverage.STRONG
        ratio = inp.pipeline_value / gap
        if ratio >= 3.0: return PipelineCoverage.STRONG
        if ratio >= 2.0: return PipelineCoverage.ADEQUATE
        if ratio >= 1.0: return PipelineCoverage.THIN
        return PipelineCoverage.INSUFFICIENT

    def _required_win_rate(self, inp: QuotaGapInput, gap: float) -> float:
        if gap <= 0 or inp.pipeline_value <= 0:
            return 0.0
        return round(min(1.0, gap / inp.pipeline_value), 3)

    def _deals_needed(self, inp: QuotaGapInput, gap: float) -> int:
        if gap <= 0 or inp.avg_deal_size <= 0:
            return 0
        return max(0, int((gap / inp.avg_deal_size) + 0.999))  # ceiling

    def _achievement_score(
        self, inp: QuotaGapInput, attainment_pct: float, projected: float
    ) -> float:
        # Base from attainment
        score = min(60.0, attainment_pct * 0.6)
        # Projected contribution
        score += min(25.0, projected * 0.25 * 0.5)
        # Days remaining bonus (more time = more opportunity)
        if inp.days_remaining > 30: score += 10
        elif inp.days_remaining > 14: score += 5
        # Activity penalty
        if inp.last_activity_days > 14: score -= 10
        elif inp.last_activity_days > 7: score -= 5
        return round(max(0.0, min(100.0, score)), 1)

    def _pipeline_health_score(self, inp: QuotaGapInput) -> float:
        score = 50.0
        # Win rate vs pipeline coverage
        if inp.win_rate >= 0.4:      score += 15
        elif inp.win_rate >= 0.25:   score += 7
        else:                        score -= 10
        # Late stage concentration
        if inp.pipeline_value > 0:
            late_pct = inp.late_stage_value / inp.pipeline_value
            if late_pct >= 0.5:     score += 15
            elif late_pct >= 0.3:   score += 8
            else:                   score -= 5
        # Overdue deals penalty
        if inp.deals_in_pipeline > 0:
            overdue_pct = inp.overdue_deals / inp.deals_in_pipeline
            if overdue_pct >= 0.5:  score -= 20
            elif overdue_pct >= 0.3: score -= 10
        # Recency
        if inp.last_activity_days > 7: score -= 10
        return round(max(0.0, min(100.0, score)), 1)

    def _gap_risk(
        self,
        inp: QuotaGapInput,
        attainment_pct: float,
        projected: float,
        pipeline_cov: PipelineCoverage,
    ) -> GapRisk:
        risk_score = 0
        if attainment_pct < 50:  risk_score += 3
        elif attainment_pct < 70: risk_score += 2
        elif attainment_pct < 90: risk_score += 1
        if projected < 70:       risk_score += 3
        elif projected < 90:     risk_score += 1
        if pipeline_cov == PipelineCoverage.INSUFFICIENT: risk_score += 2
        elif pipeline_cov == PipelineCoverage.THIN:        risk_score += 1
        if inp.days_remaining <= 14: risk_score += 2
        elif inp.days_remaining <= 30: risk_score += 1
        if inp.last_activity_days > 14: risk_score += 1

        if risk_score >= 7: return GapRisk.CRITICAL
        if risk_score >= 4: return GapRisk.HIGH
        if risk_score >= 2: return GapRisk.MEDIUM
        return GapRisk.LOW

    def _recommended_action(
        self,
        inp: QuotaGapInput,
        gap_risk: GapRisk,
        pipeline_cov: PipelineCoverage,
        attainment_pct: float,
    ) -> QuotaAction:
        if attainment_pct >= 110:
            return QuotaAction.CELEBRATE_AND_EXPAND
        if gap_risk == GapRisk.CRITICAL:
            return QuotaAction.EXECUTIVE_INTERVENTION
        if pipeline_cov == PipelineCoverage.INSUFFICIENT:
            return QuotaAction.BUILD_PIPELINE
        if inp.late_stage_value > 0 and gap_risk == GapRisk.HIGH:
            return QuotaAction.FOCUS_LATE_STAGE
        if pipeline_cov in (PipelineCoverage.THIN, PipelineCoverage.ADEQUATE):
            return QuotaAction.ACCELERATE_PIPELINE
        return QuotaAction.MAINTAIN_PACE

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                        0,
                "tier_counts":                  {},
                "risk_counts":                  {},
                "coverage_counts":              {},
                "action_counts":                {},
                "avg_attainment_pct":           0.0,
                "avg_projected_attainment":     0.0,
                "avg_achievement_score":        0.0,
                "avg_pipeline_health_score":    0.0,
                "total_gap":                    0.0,
                "at_risk_count":                0,
                "overachiever_count":           0,
                "critical_count":               0,
            }

        tier_counts:     dict[str, int] = {}
        risk_counts:     dict[str, int] = {}
        cov_counts:      dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_att  = 0.0
        total_proj = 0.0
        total_ach  = 0.0
        total_pipe = 0.0

        for r in self._results:
            tier_counts[r.attainment_tier.value]    = tier_counts.get(r.attainment_tier.value, 0) + 1
            risk_counts[r.gap_risk.value]           = risk_counts.get(r.gap_risk.value, 0) + 1
            cov_counts[r.pipeline_coverage.value]   = cov_counts.get(r.pipeline_coverage.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_att  += r.attainment_pct
            total_proj += r.projected_attainment
            total_ach  += r.quota_achievement_score
            total_pipe += r.pipeline_health_score

        return {
            "total":                        n,
            "tier_counts":                  tier_counts,
            "risk_counts":                  risk_counts,
            "coverage_counts":              cov_counts,
            "action_counts":                action_counts,
            "avg_attainment_pct":           round(total_att / n, 1),
            "avg_projected_attainment":     round(total_proj / n, 1),
            "avg_achievement_score":        round(total_ach / n, 1),
            "avg_pipeline_health_score":    round(total_pipe / n, 1),
            "total_gap":                    self.total_gap,
            "at_risk_count":                len(self.at_risk_reps),
            "overachiever_count":           len(self.overachievers),
            "critical_count":               len(self.critical_reps),
        }
