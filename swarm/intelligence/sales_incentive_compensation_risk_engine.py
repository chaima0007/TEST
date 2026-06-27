from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class CompRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CompPattern(str, Enum):
    none                   = "none"
    quarter_end_dumping    = "quarter_end_dumping"
    discount_abuse         = "discount_abuse"
    quota_ratchet_gaming   = "quota_ratchet_gaming"
    cherry_picking         = "cherry_picking"
    accelerator_exploitation = "accelerator_exploitation"


class CompSeverity(str, Enum):
    aligned    = "aligned"
    watch      = "watch"
    misaligned = "misaligned"
    exploiting = "exploiting"


class CompAction(str, Enum):
    no_action              = "no_action"
    comp_plan_review       = "comp_plan_review"
    deal_desk_escalation   = "deal_desk_escalation"
    quota_recalibration    = "quota_recalibration"
    plan_redesign          = "plan_redesign"


@dataclass
class CompRiskInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    quota_attainment_pct: float
    quota_attainment_prior_pct: float
    avg_deal_discount_pct: float
    discount_policy_max_pct: float
    deals_discounted_above_policy_count: int
    q3_deals_closed: int
    q4_deals_closed: int
    last_week_of_quarter_deals_pct: float
    deal_size_variance_score: float
    strategic_account_deals_pct: float
    transactional_account_deals_pct: float
    accelerator_threshold_pct: float
    deals_closed_just_above_accelerator: int
    deals_delayed_to_next_period_count: int
    avg_margin_pct: float
    margin_benchmark_pct: float
    customer_satisfaction_score: float
    multi_year_contract_pct: float
    comp_complaint_count: int


@dataclass
class CompRiskResult:
    rep_id: str
    region: str
    comp_risk: CompRisk
    comp_pattern: CompPattern
    comp_severity: CompSeverity
    recommended_action: CompAction
    timing_manipulation_score: float
    discount_behavior_score: float
    quota_gaming_score: float
    strategic_alignment_score: float
    comp_risk_composite: float
    is_comp_misaligned: bool
    requires_immediate_review: bool
    estimated_margin_impact_pct: float
    comp_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "comp_risk":                    self.comp_risk.value,
            "comp_pattern":                 self.comp_pattern.value,
            "comp_severity":                self.comp_severity.value,
            "recommended_action":           self.recommended_action.value,
            "timing_manipulation_score":    self.timing_manipulation_score,
            "discount_behavior_score":      self.discount_behavior_score,
            "quota_gaming_score":           self.quota_gaming_score,
            "strategic_alignment_score":    self.strategic_alignment_score,
            "comp_risk_composite":          self.comp_risk_composite,
            "is_comp_misaligned":           self.is_comp_misaligned,
            "requires_immediate_review":    self.requires_immediate_review,
            "estimated_margin_impact_pct":  self.estimated_margin_impact_pct,
            "comp_signal":                  self.comp_signal,
        }


class SalesIncentiveCompensationRiskEngine:

    def __init__(self) -> None:
        self._results: list[CompRiskResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100)
    # ------------------------------------------------------------------

    def _timing_manipulation_score(self, inp: CompRiskInput) -> float:
        score = 0.0

        # Last week of quarter concentration
        if inp.last_week_of_quarter_deals_pct >= 0.50:
            score += 45.0
        elif inp.last_week_of_quarter_deals_pct >= 0.35:
            score += 28.0
        elif inp.last_week_of_quarter_deals_pct >= 0.20:
            score += 12.0

        # Quarter spike (Q4 vs Q3 ratio)
        total_q = inp.q3_deals_closed + inp.q4_deals_closed
        if total_q > 0 and inp.q3_deals_closed > 0:
            q4_ratio = inp.q4_deals_closed / inp.q3_deals_closed
            if q4_ratio >= 3.0:
                score += 30.0
            elif q4_ratio >= 2.0:
                score += 15.0
            elif q4_ratio >= 1.5:
                score += 6.0

        # Intentional delays to next period
        if inp.deals_delayed_to_next_period_count >= 3:
            score += 20.0
        elif inp.deals_delayed_to_next_period_count >= 1:
            score += 10.0

        # Comp complaint (indicates dissatisfaction with timing)
        if inp.comp_complaint_count >= 2:
            score += 5.0

        return min(score, 100.0)

    def _discount_behavior_score(self, inp: CompRiskInput) -> float:
        score = 0.0

        # Discount above policy
        if inp.deals_discounted_above_policy_count >= 5:
            score += 40.0
        elif inp.deals_discounted_above_policy_count >= 3:
            score += 25.0
        elif inp.deals_discounted_above_policy_count >= 1:
            score += 12.0

        # Average discount vs policy max
        if inp.discount_policy_max_pct > 0:
            discount_excess = inp.avg_deal_discount_pct - inp.discount_policy_max_pct
            if discount_excess >= 10.0:
                score += 35.0
            elif discount_excess >= 5.0:
                score += 20.0
            elif discount_excess >= 2.0:
                score += 8.0

        # Margin degradation
        margin_decline = inp.margin_benchmark_pct - inp.avg_margin_pct
        if margin_decline >= 10.0:
            score += 20.0
        elif margin_decline >= 5.0:
            score += 10.0

        # Low customer satisfaction despite discounts = ineffective
        if inp.customer_satisfaction_score < 50.0 and inp.avg_deal_discount_pct >= inp.discount_policy_max_pct * 0.8:
            score += 5.0

        return min(score, 100.0)

    def _quota_gaming_score(self, inp: CompRiskInput) -> float:
        score = 0.0

        # Deals clustered just above accelerator threshold
        if inp.deals_closed_just_above_accelerator >= 4:
            score += 35.0
        elif inp.deals_closed_just_above_accelerator >= 2:
            score += 18.0

        # Attainment just at accelerator (sandbagging last period to reset)
        if 99.0 <= inp.quota_attainment_pct <= 105.0 and inp.quota_attainment_prior_pct >= 140.0:
            score += 30.0
        elif inp.quota_attainment_prior_pct >= 140.0 and inp.quota_attainment_pct < 100.0:
            score += 15.0

        # Delayed deals to control pacing
        if inp.deals_delayed_to_next_period_count >= 2:
            score += 20.0
        elif inp.deals_delayed_to_next_period_count >= 1:
            score += 8.0

        # Multi-year contract avoidance (to keep pipeline for next period)
        if inp.multi_year_contract_pct < 0.10:
            score += 15.0
        elif inp.multi_year_contract_pct < 0.20:
            score += 7.0

        return min(score, 100.0)

    def _strategic_alignment_score(self, inp: CompRiskInput) -> float:
        score = 0.0

        # Cherry-picking transactional over strategic
        if inp.transactional_account_deals_pct >= 0.80:
            score += 40.0
        elif inp.transactional_account_deals_pct >= 0.65:
            score += 22.0
        elif inp.transactional_account_deals_pct >= 0.50:
            score += 10.0

        # Low strategic account penetration
        if inp.strategic_account_deals_pct < 0.10:
            score += 30.0
        elif inp.strategic_account_deals_pct < 0.20:
            score += 15.0

        # Deal size variance (cherry-picking small easy wins)
        if inp.deal_size_variance_score >= 70.0:
            score += 20.0
        elif inp.deal_size_variance_score >= 50.0:
            score += 10.0

        # Margin degradation from wrong deal mix
        margin_decline = inp.margin_benchmark_pct - inp.avg_margin_pct
        if margin_decline >= 8.0:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: CompRiskInput,
                         timing: float, discount: float,
                         gaming: float, alignment: float) -> CompPattern:
        # Priority: accelerator_exploitation > cherry_picking > quota_ratchet_gaming
        #           > discount_abuse > quarter_end_dumping > none
        if inp.deals_closed_just_above_accelerator >= 3 and gaming >= 30:
            return CompPattern.accelerator_exploitation
        if alignment >= 30 and inp.strategic_account_deals_pct < 0.15:
            return CompPattern.cherry_picking
        if gaming >= 25 and inp.quota_attainment_prior_pct >= 130.0:
            return CompPattern.quota_ratchet_gaming
        if discount >= 25 and inp.deals_discounted_above_policy_count >= 2:
            return CompPattern.discount_abuse
        if timing >= 25 and inp.last_week_of_quarter_deals_pct >= 0.30:
            return CompPattern.quarter_end_dumping
        return CompPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> CompRisk:
        if composite >= 60:
            return CompRisk.critical
        if composite >= 40:
            return CompRisk.high
        if composite >= 20:
            return CompRisk.moderate
        return CompRisk.low

    def _severity(self, composite: float) -> CompSeverity:
        if composite >= 60:
            return CompSeverity.exploiting
        if composite >= 40:
            return CompSeverity.misaligned
        if composite >= 20:
            return CompSeverity.watch
        return CompSeverity.aligned

    def _action(self, risk: CompRisk, pattern: CompPattern) -> CompAction:
        if risk == CompRisk.critical:
            return CompAction.plan_redesign
        if risk == CompRisk.high:
            if pattern in (CompPattern.discount_abuse, CompPattern.accelerator_exploitation):
                return CompAction.deal_desk_escalation
            return CompAction.quota_recalibration
        if risk == CompRisk.moderate:
            return CompAction.comp_plan_review
        return CompAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _is_comp_misaligned(self, composite: float, inp: CompRiskInput) -> bool:
        return (
            composite >= 40
            or inp.deals_discounted_above_policy_count >= 5
            or inp.last_week_of_quarter_deals_pct >= 0.50
        )

    def _requires_immediate_review(self, composite: float, inp: CompRiskInput) -> bool:
        return (
            composite >= 30
            or inp.comp_complaint_count >= 2
            or (inp.avg_margin_pct < inp.margin_benchmark_pct * 0.80)
        )

    # ------------------------------------------------------------------
    # Margin impact
    # ------------------------------------------------------------------

    def _margin_impact(self, inp: CompRiskInput, composite: float) -> float:
        decline = inp.margin_benchmark_pct - inp.avg_margin_pct
        return round(max(decline, 0.0) * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: CompRiskInput, pattern: CompPattern, composite: float) -> str:
        if composite < 5 and pattern == CompPattern.none:
            return "Incentive comp behavior aligned with company objectives"
        parts: list[str] = []
        if inp.last_week_of_quarter_deals_pct >= 0.25:
            parts.append(f"{inp.last_week_of_quarter_deals_pct*100:.0f}% of deals in last week of quarter")
        if inp.deals_discounted_above_policy_count >= 1:
            parts.append(f"{inp.deals_discounted_above_policy_count} deals above discount policy")
        if inp.deals_closed_just_above_accelerator >= 2:
            parts.append(f"{inp.deals_closed_just_above_accelerator} deals just above accelerator threshold")
        if inp.deals_delayed_to_next_period_count >= 1:
            parts.append(f"{inp.deals_delayed_to_next_period_count} deals delayed to next period")
        label = pattern.value.replace("_", " ")
        summary = " — ".join(parts) if parts else "comp risk indicators detected"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: CompRiskInput) -> CompRiskResult:
        ti = round(self._timing_manipulation_score(inp), 1)
        di = round(self._discount_behavior_score(inp), 1)
        ga = round(self._quota_gaming_score(inp), 1)
        al = round(self._strategic_alignment_score(inp), 1)

        composite = round(ti * 0.25 + di * 0.30 + ga * 0.25 + al * 0.20, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, ti, di, ga, al)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        is_cm = self._is_comp_misaligned(composite, inp)
        is_ri = self._requires_immediate_review(composite, inp)
        margin= self._margin_impact(inp, composite)
        signal= self._signal(inp, pattern, composite)

        result = CompRiskResult(
            rep_id=inp.rep_id,
            region=inp.region,
            comp_risk=risk,
            comp_pattern=pattern,
            comp_severity=severity,
            recommended_action=action,
            timing_manipulation_score=ti,
            discount_behavior_score=di,
            quota_gaming_score=ga,
            strategic_alignment_score=al,
            comp_risk_composite=composite,
            is_comp_misaligned=is_cm,
            requires_immediate_review=is_ri,
            estimated_margin_impact_pct=margin,
            comp_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[CompRiskInput]) -> list[CompRiskResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_comp_risk_composite": 0.0,
                "misaligned_count": 0,
                "immediate_review_count": 0,
                "avg_timing_manipulation_score": 0.0,
                "avg_discount_behavior_score": 0.0,
                "avg_quota_gaming_score": 0.0,
                "avg_strategic_alignment_score": 0.0,
                "avg_estimated_margin_impact_pct": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_ti = total_di = total_ga = total_al = total_margin = 0.0

        for r in self._results:
            risk_counts[r.comp_risk.value]        = risk_counts.get(r.comp_risk.value, 0) + 1
            pattern_counts[r.comp_pattern.value]  = pattern_counts.get(r.comp_pattern.value, 0) + 1
            severity_counts[r.comp_severity.value] = severity_counts.get(r.comp_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp   += r.comp_risk_composite
            total_ti     += r.timing_manipulation_score
            total_di     += r.discount_behavior_score
            total_ga     += r.quota_gaming_score
            total_al     += r.strategic_alignment_score
            total_margin += r.estimated_margin_impact_pct

        n = len(self._results)

        return {
            "total":                             n,
            "risk_counts":                       risk_counts,
            "pattern_counts":                    pattern_counts,
            "severity_counts":                   severity_counts,
            "action_counts":                     action_counts,
            "avg_comp_risk_composite":           round(total_comp / n, 1),
            "misaligned_count":                  sum(1 for r in self._results if r.is_comp_misaligned),
            "immediate_review_count":            sum(1 for r in self._results if r.requires_immediate_review),
            "avg_timing_manipulation_score":     round(total_ti / n, 1),
            "avg_discount_behavior_score":       round(total_di / n, 1),
            "avg_quota_gaming_score":            round(total_ga / n, 1),
            "avg_strategic_alignment_score":     round(total_al / n, 1),
            "avg_estimated_margin_impact_pct":   round(total_margin / n, 2),
        }
