from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ValueRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ValuePattern(str, Enum):
    none                     = "none"
    feature_seller           = "feature_seller"
    roi_avoidance            = "roi_avoidance"
    champion_dependency      = "champion_dependency"
    value_gap_at_close       = "value_gap_at_close"
    executive_misalignment   = "executive_misalignment"


class ValueSeverity(str, Enum):
    outcome_driven = "outcome_driven"
    adequate       = "adequate"
    feature_led    = "feature_led"
    value_blind    = "value_blind"


class ValueAction(str, Enum):
    no_action                     = "no_action"
    value_selling_coaching        = "value_selling_coaching"
    roi_case_building_coaching    = "roi_case_building_coaching"
    executive_engagement_coaching = "executive_engagement_coaching"
    business_case_coaching        = "business_case_coaching"
    value_reset_intervention      = "value_reset_intervention"


@dataclass
class ValueInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    business_case_created_pct: float
    roi_quantified_before_proposal_pct: float
    value_metrics_agreed_with_buyer_pct: float
    feature_demo_without_roi_pct: float
    price_reduction_requested_after_demo_pct: float
    economic_value_referenced_in_proposal_pct: float
    executive_sponsor_engaged_pct: float
    c_suite_presentation_rate_pct: float
    decision_maker_roi_meeting_pct: float
    proof_of_value_completed_pct: float
    value_delivered_milestone_tracked_pct: float
    customer_success_metric_defined_pct: float
    competitive_value_differentiation_pct: float
    deals_lost_on_price_pct: float
    discount_avoided_via_value_pct: float
    expansion_driven_by_value_proof_pct: float
    avg_deal_cycle_days: float
    total_deals_closed: int
    avg_opportunity_value_usd: float


@dataclass
class ValueResult:
    rep_id: str
    region: str
    value_risk: ValueRisk
    value_pattern: ValuePattern
    value_severity: ValueSeverity
    recommended_action: ValueAction
    quantification_score: float
    executive_score: float
    proof_score: float
    outcome_score: float
    value_composite: float
    has_value_gap: bool
    requires_value_coaching: bool
    estimated_value_leak_usd: float
    value_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                    self.rep_id,
            "region":                    self.region,
            "value_risk":                self.value_risk.value,
            "value_pattern":             self.value_pattern.value,
            "value_severity":            self.value_severity.value,
            "recommended_action":        self.recommended_action.value,
            "quantification_score":      self.quantification_score,
            "executive_score":           self.executive_score,
            "proof_score":               self.proof_score,
            "outcome_score":             self.outcome_score,
            "value_composite":           self.value_composite,
            "has_value_gap":             self.has_value_gap,
            "requires_value_coaching":   self.requires_value_coaching,
            "estimated_value_leak_usd":  self.estimated_value_leak_usd,
            "value_signal":              self.value_signal,
        }


class SalesProofOfValueIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[ValueResult] = []

    def _quantification_score(self, inp: ValueInput) -> float:
        score = 0.0
        if inp.roi_quantified_before_proposal_pct <= 0.25:
            score += 40.0
        elif inp.roi_quantified_before_proposal_pct <= 0.50:
            score += 22.0
        elif inp.roi_quantified_before_proposal_pct <= 0.70:
            score += 8.0
        if inp.business_case_created_pct <= 0.20:
            score += 35.0
        elif inp.business_case_created_pct <= 0.45:
            score += 18.0
        if inp.feature_demo_without_roi_pct >= 0.60:
            score += 25.0
        elif inp.feature_demo_without_roi_pct >= 0.35:
            score += 12.0
        return min(score, 100.0)

    def _executive_score(self, inp: ValueInput) -> float:
        score = 0.0
        if inp.executive_sponsor_engaged_pct <= 0.25:
            score += 40.0
        elif inp.executive_sponsor_engaged_pct <= 0.50:
            score += 22.0
        elif inp.executive_sponsor_engaged_pct <= 0.70:
            score += 8.0
        if inp.c_suite_presentation_rate_pct <= 0.15:
            score += 35.0
        elif inp.c_suite_presentation_rate_pct <= 0.35:
            score += 18.0
        if inp.decision_maker_roi_meeting_pct <= 0.20:
            score += 25.0
        elif inp.decision_maker_roi_meeting_pct <= 0.45:
            score += 12.0
        return min(score, 100.0)

    def _proof_score(self, inp: ValueInput) -> float:
        score = 0.0
        if inp.proof_of_value_completed_pct <= 0.20:
            score += 45.0
        elif inp.proof_of_value_completed_pct <= 0.40:
            score += 25.0
        elif inp.proof_of_value_completed_pct <= 0.60:
            score += 10.0
        if inp.value_metrics_agreed_with_buyer_pct <= 0.25:
            score += 30.0
        elif inp.value_metrics_agreed_with_buyer_pct <= 0.50:
            score += 15.0
        if inp.competitive_value_differentiation_pct <= 0.30:
            score += 25.0
        elif inp.competitive_value_differentiation_pct <= 0.55:
            score += 12.0
        return min(score, 100.0)

    def _outcome_score(self, inp: ValueInput) -> float:
        score = 0.0
        if inp.deals_lost_on_price_pct >= 0.45:
            score += 40.0
        elif inp.deals_lost_on_price_pct >= 0.25:
            score += 22.0
        elif inp.deals_lost_on_price_pct >= 0.10:
            score += 8.0
        if inp.customer_success_metric_defined_pct <= 0.25:
            score += 35.0
        elif inp.customer_success_metric_defined_pct <= 0.50:
            score += 18.0
        if inp.economic_value_referenced_in_proposal_pct <= 0.30:
            score += 25.0
        elif inp.economic_value_referenced_in_proposal_pct <= 0.55:
            score += 12.0
        return min(score, 100.0)

    def _detect_pattern(self, inp: ValueInput,
                         quant: float, exec_: float,
                         proof: float, outcome: float) -> ValuePattern:
        if inp.feature_demo_without_roi_pct >= 0.55 and quant >= 35:
            return ValuePattern.feature_seller
        if inp.roi_quantified_before_proposal_pct <= 0.20 and inp.business_case_created_pct <= 0.25:
            return ValuePattern.roi_avoidance
        if inp.executive_sponsor_engaged_pct <= 0.20 and exec_ >= 35:
            return ValuePattern.executive_misalignment
        if inp.deals_lost_on_price_pct >= 0.40 and inp.discount_avoided_via_value_pct <= 0.20:
            return ValuePattern.value_gap_at_close
        if inp.proof_of_value_completed_pct <= 0.15 and proof >= 35:
            return ValuePattern.champion_dependency
        return ValuePattern.none

    def _risk_level(self, composite: float) -> ValueRisk:
        if composite >= 60:
            return ValueRisk.critical
        if composite >= 40:
            return ValueRisk.high
        if composite >= 20:
            return ValueRisk.moderate
        return ValueRisk.low

    def _severity(self, composite: float) -> ValueSeverity:
        if composite >= 60:
            return ValueSeverity.value_blind
        if composite >= 40:
            return ValueSeverity.feature_led
        if composite >= 20:
            return ValueSeverity.adequate
        return ValueSeverity.outcome_driven

    def _action(self, risk: ValueRisk, pattern: ValuePattern) -> ValueAction:
        if risk == ValueRisk.critical:
            if pattern == ValuePattern.feature_seller:
                return ValueAction.value_selling_coaching
            if pattern == ValuePattern.roi_avoidance:
                return ValueAction.roi_case_building_coaching
            return ValueAction.value_reset_intervention
        if risk == ValueRisk.high:
            if pattern == ValuePattern.executive_misalignment:
                return ValueAction.executive_engagement_coaching
            if pattern == ValuePattern.value_gap_at_close:
                return ValueAction.business_case_coaching
            return ValueAction.roi_case_building_coaching
        if risk == ValueRisk.moderate:
            return ValueAction.value_selling_coaching
        return ValueAction.no_action

    def _has_value_gap(self, composite: float, inp: ValueInput) -> bool:
        return (
            composite >= 40
            or inp.roi_quantified_before_proposal_pct <= 0.40
            or inp.deals_lost_on_price_pct >= 0.30
        )

    def _requires_value_coaching(self, composite: float, inp: ValueInput) -> bool:
        return (
            composite >= 30
            or inp.feature_demo_without_roi_pct >= 0.40
            or inp.executive_sponsor_engaged_pct <= 0.40
        )

    def _estimated_value_leak(self, inp: ValueInput, composite: float) -> float:
        return round(
            inp.total_deals_closed
            * inp.avg_opportunity_value_usd
            * inp.deals_lost_on_price_pct
            * (composite / 100.0),
            2,
        )

    def _signal(self, inp: ValueInput,
                pattern: ValuePattern, composite: float) -> str:
        if pattern == ValuePattern.none and composite < 20:
            return "Value selling strong — ROI quantification, executive engagement, and proof of value within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.roi_quantified_before_proposal_pct * 100:.0f}% ROI quantified pre-proposal")
        parts.append(f"{inp.executive_sponsor_engaged_pct * 100:.0f}% executive sponsor engaged")
        parts.append(f"{inp.deals_lost_on_price_pct * 100:.0f}% deals lost on price")
        label = pattern.value.replace("_", " ") if pattern != ValuePattern.none else "Value risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    def assess(self, inp: ValueInput) -> ValueResult:
        quant  = round(self._quantification_score(inp), 1)
        exec_  = round(self._executive_score(inp), 1)
        proof  = round(self._proof_score(inp), 1)
        outcome = round(self._outcome_score(inp), 1)
        composite = round(
            quant * 0.30 + exec_ * 0.25 + proof * 0.25 + outcome * 0.20, 1
        )
        composite = min(composite, 100.0)
        pattern  = self._detect_pattern(inp, quant, exec_, proof, outcome)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)
        gap      = self._has_value_gap(composite, inp)
        coach    = self._requires_value_coaching(composite, inp)
        leak     = self._estimated_value_leak(inp, composite)
        signal   = self._signal(inp, pattern, composite)
        result = ValueResult(
            rep_id=inp.rep_id, region=inp.region,
            value_risk=risk, value_pattern=pattern,
            value_severity=severity, recommended_action=action,
            quantification_score=quant, executive_score=exec_,
            proof_score=proof, outcome_score=outcome,
            value_composite=composite,
            has_value_gap=gap, requires_value_coaching=coach,
            estimated_value_leak_usd=leak, value_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[ValueInput]) -> list[ValueResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0, "risk_counts": {}, "pattern_counts": {},
                "severity_counts": {}, "action_counts": {},
                "avg_value_composite": 0.0, "value_gap_count": 0, "coaching_count": 0,
                "avg_quantification_score": 0.0, "avg_executive_score": 0.0,
                "avg_proof_score": 0.0, "avg_outcome_score": 0.0,
                "total_estimated_value_leak_usd": 0.0,
            }
        rc: dict[str, int] = {}
        pc: dict[str, int] = {}
        sc: dict[str, int] = {}
        ac: dict[str, int] = {}
        tc = tq = te = tpr = to = tl = 0.0
        for r in self._results:
            rc[r.value_risk.value]         = rc.get(r.value_risk.value, 0) + 1
            pc[r.value_pattern.value]      = pc.get(r.value_pattern.value, 0) + 1
            sc[r.value_severity.value]     = sc.get(r.value_severity.value, 0) + 1
            ac[r.recommended_action.value] = ac.get(r.recommended_action.value, 0) + 1
            tc  += r.value_composite
            tq  += r.quantification_score
            te  += r.executive_score
            tpr += r.proof_score
            to  += r.outcome_score
            tl  += r.estimated_value_leak_usd
        n = len(self._results)
        return {
            "total":                           n,
            "risk_counts":                     rc,
            "pattern_counts":                  pc,
            "severity_counts":                 sc,
            "action_counts":                   ac,
            "avg_value_composite":             round(tc / n, 1),
            "value_gap_count":                 sum(1 for r in self._results if r.has_value_gap),
            "coaching_count":                  sum(1 for r in self._results if r.requires_value_coaching),
            "avg_quantification_score":        round(tq / n, 1),
            "avg_executive_score":             round(te / n, 1),
            "avg_proof_score":                 round(tpr / n, 1),
            "avg_outcome_score":               round(to / n, 1),
            "total_estimated_value_leak_usd":  round(tl, 2),
        }
