"""Sales Quota Gaming Detection Engine — detects when sales reps manipulate
deal timing, pipeline coverage, or reporting to game quota metrics and
compensation plans, including pull-forwards, sandbagging rollover, and
strategic pipeline inflation to influence future quota assignments."""

from __future__ import annotations

import dataclasses
from enum import Enum


class QuotaGamingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class GamingPattern(str, Enum):
    none                    = "none"
    pull_forward_abuse      = "pull_forward_abuse"
    pipeline_inflation      = "pipeline_inflation"
    close_date_manipulation = "close_date_manipulation"
    quota_anchor_gaming     = "quota_anchor_gaming"
    comp_period_stuffing    = "comp_period_stuffing"


class GamingSeverity(str, Enum):
    clean       = "clean"
    watch       = "watch"
    suspicious  = "suspicious"
    confirmed   = "confirmed"


class GamingAction(str, Enum):
    no_action            = "no_action"
    manager_review       = "manager_review"
    comp_plan_audit      = "comp_plan_audit"
    quota_recalibration  = "quota_recalibration"
    compensation_clawback = "compensation_clawback"


@dataclasses.dataclass
class QuotaGamingInput:
    rep_id:                              str
    region:                              str
    evaluation_period_id:                str
    deals_closed_in_final_week_pct:      float
    deals_pulled_from_next_period_count: int
    avg_close_date_changes_per_deal:     float
    deals_reopened_after_close_count:    int
    pipeline_coverage_ratio:             float
    company_avg_pipeline_coverage:       float
    fake_pipeline_flag_count:            int
    over_attainment_pct:                 float
    prior_period_over_attainment_pct:    float
    quota_increase_last_period_pct:      float
    deals_lost_immediately_after_close:  int
    revenue_reversed_usd:                float
    total_revenue_closed_usd:            float
    end_of_period_discount_avg_pct:      float
    normal_period_discount_avg_pct:      float
    pipeline_created_last_week_of_period: float
    pipeline_created_rest_of_period:     float
    manager_override_count:              int
    comp_accelerator_deals_count:        int


@dataclasses.dataclass
class QuotaGamingResult:
    rep_id:                          str
    region:                          str
    quota_gaming_risk:               QuotaGamingRisk
    gaming_pattern:                  GamingPattern
    gaming_severity:                 GamingSeverity
    recommended_action:              GamingAction
    timing_manipulation_score:       float
    pipeline_integrity_score:        float
    compensation_gaming_score:       float
    reporting_distortion_score:      float
    gaming_composite:                float
    is_gaming_quota:                 bool
    requires_comp_audit:             bool
    estimated_inflated_pipeline_usd: float
    gaming_signal:                   str

    def to_dict(self) -> dict:
        return {
            "rep_id":                          self.rep_id,
            "region":                          self.region,
            "quota_gaming_risk":               self.quota_gaming_risk.value,
            "gaming_pattern":                  self.gaming_pattern.value,
            "gaming_severity":                 self.gaming_severity.value,
            "recommended_action":              self.recommended_action.value,
            "timing_manipulation_score":       round(self.timing_manipulation_score, 1),
            "pipeline_integrity_score":        round(self.pipeline_integrity_score, 1),
            "compensation_gaming_score":       round(self.compensation_gaming_score, 1),
            "reporting_distortion_score":      round(self.reporting_distortion_score, 1),
            "gaming_composite":                round(self.gaming_composite, 1),
            "is_gaming_quota":                 self.is_gaming_quota,
            "requires_comp_audit":             self.requires_comp_audit,
            "estimated_inflated_pipeline_usd": round(self.estimated_inflated_pipeline_usd, 2),
            "gaming_signal":                   self.gaming_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class SalesQuotaGamingDetectionEngine:
    """Identifies quota gaming behaviors that manipulate compensation and distort revenue reporting."""

    def __init__(self) -> None:
        self._results: list[QuotaGamingResult] = []

    # ── sub-scores (HIGHER = more gaming risk) ───────────────────────────────

    def _timing_manipulation_score(self, inp: QuotaGamingInput) -> float:
        score = 0.0
        # End-of-period deal stuffing
        if inp.deals_closed_in_final_week_pct >= 60:
            score += 40.0
        elif inp.deals_closed_in_final_week_pct >= 40:
            score += 25.0
        elif inp.deals_closed_in_final_week_pct >= 25:
            score += 12.0
        # Pull forwards from next period
        if inp.deals_pulled_from_next_period_count >= 5:
            score += 35.0
        elif inp.deals_pulled_from_next_period_count >= 3:
            score += 20.0
        elif inp.deals_pulled_from_next_period_count >= 1:
            score += 10.0
        # Excessive close date changes
        if inp.avg_close_date_changes_per_deal >= 5:
            score += 25.0
        elif inp.avg_close_date_changes_per_deal >= 3:
            score += 14.0
        elif inp.avg_close_date_changes_per_deal >= 2:
            score += 7.0
        return _clamp(score)

    def _pipeline_integrity_score(self, inp: QuotaGamingInput) -> float:
        score = 0.0
        # Pipeline inflation vs company average
        if inp.company_avg_pipeline_coverage > 0:
            coverage_excess = inp.pipeline_coverage_ratio / inp.company_avg_pipeline_coverage
            if coverage_excess >= 3.0:
                score += 40.0
            elif coverage_excess >= 2.0:
                score += 25.0
            elif coverage_excess >= 1.5:
                score += 12.0
        # Fake pipeline flags (admin-detected)
        if inp.fake_pipeline_flag_count >= 5:
            score += 35.0
        elif inp.fake_pipeline_flag_count >= 3:
            score += 22.0
        elif inp.fake_pipeline_flag_count >= 1:
            score += 10.0
        # Last-week pipeline creation surge
        if inp.pipeline_created_rest_of_period > 0:
            last_week_ratio = inp.pipeline_created_last_week_of_period / inp.pipeline_created_rest_of_period
            if last_week_ratio >= 0.6:
                score += 25.0
            elif last_week_ratio >= 0.4:
                score += 14.0
            elif last_week_ratio >= 0.25:
                score += 7.0
        return _clamp(score)

    def _compensation_gaming_score(self, inp: QuotaGamingInput) -> float:
        score = 0.0
        # Consistent high over-attainment (anchoring quota low)
        if inp.over_attainment_pct >= 150:
            score += 35.0
        elif inp.over_attainment_pct >= 130:
            score += 22.0
        elif inp.over_attainment_pct >= 115:
            score += 10.0
        # Prior period also over-attained (systematic pattern)
        if inp.prior_period_over_attainment_pct >= 150 and inp.over_attainment_pct >= 130:
            score += 25.0
        elif inp.prior_period_over_attainment_pct >= 130:
            score += 12.0
        # Comp accelerator abuse (clustering deals at threshold)
        if inp.comp_accelerator_deals_count >= 5:
            score += 25.0
        elif inp.comp_accelerator_deals_count >= 3:
            score += 15.0
        elif inp.comp_accelerator_deals_count >= 1:
            score += 7.0
        # Heavy discounting at period end to force closings
        discount_delta = inp.end_of_period_discount_avg_pct - inp.normal_period_discount_avg_pct
        if discount_delta >= 15:
            score += 20.0
        elif discount_delta >= 8:
            score += 10.0
        elif discount_delta >= 4:
            score += 5.0
        return _clamp(score)

    def _reporting_distortion_score(self, inp: QuotaGamingInput) -> float:
        score = 0.0
        # Revenue reversals (closed deals that un-closed)
        if inp.total_revenue_closed_usd > 0:
            reversal_ratio = inp.revenue_reversed_usd / inp.total_revenue_closed_usd
            if reversal_ratio >= 0.2:
                score += 45.0
            elif reversal_ratio >= 0.1:
                score += 28.0
            elif reversal_ratio >= 0.05:
                score += 12.0
        # Deals lost immediately after close (phantom wins)
        if inp.deals_lost_immediately_after_close >= 4:
            score += 35.0
        elif inp.deals_lost_immediately_after_close >= 2:
            score += 20.0
        elif inp.deals_lost_immediately_after_close >= 1:
            score += 10.0
        # Deals reopened after close (manipulation of period attribution)
        if inp.deals_reopened_after_close_count >= 4:
            score += 25.0
        elif inp.deals_reopened_after_close_count >= 2:
            score += 14.0
        elif inp.deals_reopened_after_close_count >= 1:
            score += 7.0
        # Manager overrides (forcing numbers)
        if inp.manager_override_count >= 5:
            score += 15.0
        elif inp.manager_override_count >= 3:
            score += 8.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> QuotaGamingRisk:
        if composite < 20:
            return QuotaGamingRisk.low
        if composite < 40:
            return QuotaGamingRisk.moderate
        if composite < 60:
            return QuotaGamingRisk.high
        return QuotaGamingRisk.critical

    def _classify_severity(self, composite: float) -> GamingSeverity:
        if composite < 20:
            return GamingSeverity.clean
        if composite < 40:
            return GamingSeverity.watch
        if composite < 60:
            return GamingSeverity.suspicious
        return GamingSeverity.confirmed

    def _classify_pattern(
        self,
        inp: QuotaGamingInput,
        timing: float,
        pipeline: float,
        comp: float,
        reporting: float,
    ) -> GamingPattern:
        # Period stuffing: revenue reversals + last-week closures
        if reporting >= 35 and inp.deals_lost_immediately_after_close >= 2:
            return GamingPattern.comp_period_stuffing
        # Quota anchor: consistent multi-period over-attainment
        if inp.over_attainment_pct >= 140 and inp.prior_period_over_attainment_pct >= 130:
            return GamingPattern.quota_anchor_gaming
        # Close date manipulation
        if timing >= 35 and inp.avg_close_date_changes_per_deal >= 3:
            return GamingPattern.close_date_manipulation
        # Pipeline inflation
        if pipeline >= 30:
            return GamingPattern.pipeline_inflation
        # Pull forward abuse
        if inp.deals_pulled_from_next_period_count >= 3:
            return GamingPattern.pull_forward_abuse
        return GamingPattern.none

    def _recommended_action(
        self, risk: QuotaGamingRisk, composite: float
    ) -> GamingAction:
        if composite >= 60:
            return GamingAction.compensation_clawback
        if composite >= 50:
            return GamingAction.quota_recalibration
        if risk == QuotaGamingRisk.high:
            return GamingAction.comp_plan_audit
        if risk == QuotaGamingRisk.moderate:
            return GamingAction.manager_review
        return GamingAction.no_action

    def _signal(
        self,
        pattern: GamingPattern,
        composite: float,
        inp: QuotaGamingInput,
    ) -> str:
        if pattern == GamingPattern.none:
            return "Quota attainment behavior within normal parameters"
        msgs = {
            GamingPattern.comp_period_stuffing: (
                f"{inp.deals_lost_immediately_after_close} deals reversed post-close — "
                f"${inp.revenue_reversed_usd:,.0f} revenue reversed"
            ),
            GamingPattern.quota_anchor_gaming: (
                f"Over-attainment {inp.over_attainment_pct:.0f}% this period, "
                f"{inp.prior_period_over_attainment_pct:.0f}% prior"
            ),
            GamingPattern.close_date_manipulation: (
                f"{inp.avg_close_date_changes_per_deal:.1f} avg close date changes — "
                f"{inp.deals_closed_in_final_week_pct:.0f}% closed in final week"
            ),
            GamingPattern.pipeline_inflation: (
                f"{inp.fake_pipeline_flag_count} fake pipeline flag(s) — "
                f"coverage {inp.pipeline_coverage_ratio:.1f}x vs "
                f"{inp.company_avg_pipeline_coverage:.1f}x avg"
            ),
            GamingPattern.pull_forward_abuse: (
                f"{inp.deals_pulled_from_next_period_count} deals pulled from next period"
            ),
        }
        base = msgs.get(pattern, f"gaming composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: QuotaGamingInput) -> QuotaGamingResult:
        timing    = self._timing_manipulation_score(inp)
        pipeline  = self._pipeline_integrity_score(inp)
        comp      = self._compensation_gaming_score(inp)
        reporting = self._reporting_distortion_score(inp)

        composite = _clamp(
            timing    * 0.30
            + pipeline * 0.25
            + comp     * 0.25
            + reporting * 0.20
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        pattern  = self._classify_pattern(inp, timing, pipeline, comp, reporting)
        action   = self._recommended_action(risk, composite)

        is_gaming_quota = (
            composite >= 40
            or inp.revenue_reversed_usd > inp.total_revenue_closed_usd * 0.1
            or inp.fake_pipeline_flag_count >= 3
        )
        requires_comp_audit = (
            composite >= 30
            or inp.over_attainment_pct >= 140
            or inp.deals_pulled_from_next_period_count >= 3
        )

        estimated_inflated_pipeline_usd = (
            inp.pipeline_created_last_week_of_period * (composite / 100.0)
            if inp.pipeline_created_last_week_of_period > 0 else 0.0
        )

        result = QuotaGamingResult(
            rep_id=inp.rep_id,
            region=inp.region,
            quota_gaming_risk=risk,
            gaming_pattern=pattern,
            gaming_severity=severity,
            recommended_action=action,
            timing_manipulation_score=timing,
            pipeline_integrity_score=pipeline,
            compensation_gaming_score=comp,
            reporting_distortion_score=reporting,
            gaming_composite=composite,
            is_gaming_quota=is_gaming_quota,
            requires_comp_audit=requires_comp_audit,
            estimated_inflated_pipeline_usd=estimated_inflated_pipeline_usd,
            gaming_signal=self._signal(pattern, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[QuotaGamingInput]
    ) -> list[QuotaGamingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                              0,
                "risk_counts":                        {},
                "pattern_counts":                     {},
                "severity_counts":                    {},
                "action_counts":                      {},
                "avg_gaming_composite":               0.0,
                "gaming_count":                       0,
                "comp_audit_count":                   0,
                "avg_timing_manipulation_score":      0.0,
                "avg_pipeline_integrity_score":       0.0,
                "avg_compensation_gaming_score":      0.0,
                "avg_reporting_distortion_score":     0.0,
                "total_estimated_inflated_pipeline_usd": 0.0,
            }

        risk_counts:    dict[str, int] = {}
        pattern_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:  dict[str, int] = {}
        total_comp = total_tim = total_pipe = total_cmp = total_rep = total_infl = 0.0
        gaming = audit = 0

        for r in self._results:
            risk_counts[r.quota_gaming_risk.value]  = risk_counts.get(r.quota_gaming_risk.value, 0) + 1
            pattern_counts[r.gaming_pattern.value]  = pattern_counts.get(r.gaming_pattern.value, 0) + 1
            severity_counts[r.gaming_severity.value] = severity_counts.get(r.gaming_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.gaming_composite
            total_tim  += r.timing_manipulation_score
            total_pipe += r.pipeline_integrity_score
            total_cmp  += r.compensation_gaming_score
            total_rep  += r.reporting_distortion_score
            total_infl += r.estimated_inflated_pipeline_usd
            if r.is_gaming_quota:
                gaming += 1
            if r.requires_comp_audit:
                audit += 1

        n = len(self._results)
        return {
            "total":                               n,
            "risk_counts":                         risk_counts,
            "pattern_counts":                      pattern_counts,
            "severity_counts":                     severity_counts,
            "action_counts":                       action_counts,
            "avg_gaming_composite":                round(total_comp / n, 1),
            "gaming_count":                        gaming,
            "comp_audit_count":                    audit,
            "avg_timing_manipulation_score":       round(total_tim  / n, 1),
            "avg_pipeline_integrity_score":        round(total_pipe / n, 1),
            "avg_compensation_gaming_score":       round(total_cmp  / n, 1),
            "avg_reporting_distortion_score":      round(total_rep  / n, 1),
            "total_estimated_inflated_pipeline_usd": round(total_infl, 2),
        }
