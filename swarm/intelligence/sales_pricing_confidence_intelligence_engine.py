from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class PricingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class PricingPattern(str, Enum):
    none                          = "none"
    preemptive_discounting        = "preemptive_discounting"
    anchor_too_low                = "anchor_too_low"
    value_articulation_gap        = "value_articulation_gap"
    approval_escalation_dependency = "approval_escalation_dependency"
    competitor_price_panic        = "competitor_price_panic"


class PricingSeverity(str, Enum):
    confident     = "confident"
    cautious      = "cautious"
    hesitant      = "hesitant"
    capitulating  = "capitulating"


class PricingAction(str, Enum):
    no_action                      = "no_action"
    value_selling_coaching         = "value_selling_coaching"
    pricing_anchoring_coaching     = "pricing_anchoring_coaching"
    negotiation_confidence_coaching = "negotiation_confidence_coaching"
    approval_process_coaching      = "approval_process_coaching"
    competitive_pricing_training   = "competitive_pricing_training"


@dataclass
class PricingInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    avg_initial_discount_offered_pct: float
    discount_offered_before_asked_pct: float
    full_price_close_rate_pct: float
    avg_final_discount_pct: float
    discount_escalation_to_manager_pct: float
    price_objection_concession_rate_pct: float
    roi_articulated_in_proposal_pct: float
    value_proof_attached_pct: float
    competitor_price_match_rate_pct: float
    discount_without_concession_pct: float
    time_to_first_discount_days: float
    multi_product_bundle_rate_pct: float
    price_increase_accepted_rate_pct: float
    deals_closed_above_list_pct: float
    avg_discount_negotiation_rounds: float
    late_stage_price_re_open_pct: float
    total_deals_evaluated: int
    avg_deal_size_usd: float
    avg_opportunity_value_usd: float


@dataclass
class PricingResult:
    rep_id: str
    region: str
    pricing_risk: PricingRisk
    pricing_pattern: PricingPattern
    pricing_severity: PricingSeverity
    recommended_action: PricingAction
    confidence_score: float
    value_score: float
    discipline_score: float
    competitive_score: float
    pricing_composite: float
    has_pricing_gap: bool
    requires_pricing_coaching: bool
    estimated_margin_erosion_usd: float
    pricing_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "pricing_risk":                 self.pricing_risk.value,
            "pricing_pattern":              self.pricing_pattern.value,
            "pricing_severity":             self.pricing_severity.value,
            "recommended_action":           self.recommended_action.value,
            "confidence_score":             self.confidence_score,
            "value_score":                  self.value_score,
            "discipline_score":             self.discipline_score,
            "competitive_score":            self.competitive_score,
            "pricing_composite":            self.pricing_composite,
            "has_pricing_gap":              self.has_pricing_gap,
            "requires_pricing_coaching":    self.requires_pricing_coaching,
            "estimated_margin_erosion_usd": self.estimated_margin_erosion_usd,
            "pricing_signal":               self.pricing_signal,
        }


class SalesPricingConfidenceIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[PricingResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _confidence_score(self, inp: PricingInput) -> float:
        score = 0.0

        if inp.discount_offered_before_asked_pct >= 0.50:
            score += 40.0
        elif inp.discount_offered_before_asked_pct >= 0.30:
            score += 22.0
        elif inp.discount_offered_before_asked_pct >= 0.15:
            score += 8.0

        if inp.time_to_first_discount_days <= 3.0:
            score += 35.0
        elif inp.time_to_first_discount_days <= 7.0:
            score += 18.0

        if inp.full_price_close_rate_pct <= 0.10:
            score += 25.0
        elif inp.full_price_close_rate_pct <= 0.25:
            score += 12.0

        return min(score, 100.0)

    def _value_score(self, inp: PricingInput) -> float:
        score = 0.0

        if inp.roi_articulated_in_proposal_pct <= 0.25:
            score += 40.0
        elif inp.roi_articulated_in_proposal_pct <= 0.50:
            score += 22.0
        elif inp.roi_articulated_in_proposal_pct <= 0.75:
            score += 8.0

        if inp.value_proof_attached_pct <= 0.20:
            score += 35.0
        elif inp.value_proof_attached_pct <= 0.50:
            score += 18.0

        if inp.price_objection_concession_rate_pct >= 0.70:
            score += 25.0
        elif inp.price_objection_concession_rate_pct >= 0.45:
            score += 12.0

        return min(score, 100.0)

    def _discipline_score(self, inp: PricingInput) -> float:
        score = 0.0

        if inp.avg_initial_discount_offered_pct >= 0.25:
            score += 40.0
        elif inp.avg_initial_discount_offered_pct >= 0.15:
            score += 22.0
        elif inp.avg_initial_discount_offered_pct >= 0.08:
            score += 8.0

        if inp.avg_discount_negotiation_rounds >= 4.0:
            score += 35.0
        elif inp.avg_discount_negotiation_rounds >= 2.5:
            score += 18.0

        if inp.late_stage_price_re_open_pct >= 0.40:
            score += 25.0
        elif inp.late_stage_price_re_open_pct >= 0.20:
            score += 12.0

        return min(score, 100.0)

    def _competitive_score(self, inp: PricingInput) -> float:
        score = 0.0

        if inp.competitor_price_match_rate_pct >= 0.60:
            score += 45.0
        elif inp.competitor_price_match_rate_pct >= 0.40:
            score += 25.0
        elif inp.competitor_price_match_rate_pct >= 0.20:
            score += 10.0

        if inp.discount_without_concession_pct >= 0.60:
            score += 30.0
        elif inp.discount_without_concession_pct >= 0.35:
            score += 15.0

        if inp.discount_escalation_to_manager_pct >= 0.50:
            score += 25.0
        elif inp.discount_escalation_to_manager_pct >= 0.25:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: PricingInput,
                          confidence: float, value: float,
                          discipline: float, competitive: float) -> PricingPattern:
        # Approval escalation dependency: high escalation + low full-price closes
        if inp.discount_escalation_to_manager_pct >= 0.45 and inp.full_price_close_rate_pct <= 0.15:
            return PricingPattern.approval_escalation_dependency

        # Competitor price panic: matches competitor price without concession value
        if competitive >= 35 and inp.competitor_price_match_rate_pct >= 0.50:
            return PricingPattern.competitor_price_panic

        # Preemptive discounting: offering discount before being asked
        if confidence >= 35 and inp.discount_offered_before_asked_pct >= 0.40:
            return PricingPattern.preemptive_discounting

        # Value articulation gap: no ROI evidence + no value proof
        if value >= 35 and inp.roi_articulated_in_proposal_pct <= 0.35:
            return PricingPattern.value_articulation_gap

        # Anchor too low: initial discount very high, sets bad expectations
        if inp.avg_initial_discount_offered_pct >= 0.20 and discipline >= 25:
            return PricingPattern.anchor_too_low

        return PricingPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> PricingRisk:
        if composite >= 60:
            return PricingRisk.critical
        if composite >= 40:
            return PricingRisk.high
        if composite >= 20:
            return PricingRisk.moderate
        return PricingRisk.low

    def _severity(self, composite: float) -> PricingSeverity:
        if composite >= 60:
            return PricingSeverity.capitulating
        if composite >= 40:
            return PricingSeverity.hesitant
        if composite >= 20:
            return PricingSeverity.cautious
        return PricingSeverity.confident

    def _action(self, risk: PricingRisk, pattern: PricingPattern) -> PricingAction:
        if risk == PricingRisk.critical:
            if pattern == PricingPattern.competitor_price_panic:
                return PricingAction.competitive_pricing_training
            if pattern == PricingPattern.approval_escalation_dependency:
                return PricingAction.approval_process_coaching
            return PricingAction.negotiation_confidence_coaching
        if risk == PricingRisk.high:
            if pattern == PricingPattern.value_articulation_gap:
                return PricingAction.value_selling_coaching
            if pattern == PricingPattern.anchor_too_low:
                return PricingAction.pricing_anchoring_coaching
            return PricingAction.negotiation_confidence_coaching
        if risk == PricingRisk.moderate:
            return PricingAction.value_selling_coaching
        return PricingAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_pricing_gap(self, composite: float, inp: PricingInput) -> bool:
        return (
            composite >= 40
            or inp.avg_final_discount_pct >= 0.20
            or inp.full_price_close_rate_pct <= 0.15
        )

    def _requires_pricing_coaching(self, composite: float, inp: PricingInput) -> bool:
        return (
            composite >= 30
            or inp.discount_offered_before_asked_pct >= 0.25
            or inp.roi_articulated_in_proposal_pct <= 0.40
        )

    # ------------------------------------------------------------------
    # Margin erosion estimate
    # ------------------------------------------------------------------

    def _estimated_margin_erosion(self, inp: PricingInput, composite: float) -> float:
        return round(
            inp.total_deals_evaluated
            * inp.avg_opportunity_value_usd
            * inp.avg_final_discount_pct
            * (composite / 100.0),
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: PricingInput,
                 pattern: PricingPattern, composite: float) -> str:
        if pattern == PricingPattern.none and composite < 20:
            return "Pricing confidence healthy — discount discipline, value articulation, and competitive positioning within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.avg_final_discount_pct * 100:.0f}% avg final discount")
        parts.append(f"{inp.discount_offered_before_asked_pct * 100:.0f}% preemptive discounting")
        parts.append(f"{inp.full_price_close_rate_pct * 100:.0f}% full-price closes")
        label = pattern.value.replace("_", " ") if pattern != PricingPattern.none else "Pricing risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: PricingInput) -> PricingResult:
        confidence  = round(self._confidence_score(inp), 1)
        value       = round(self._value_score(inp), 1)
        discipline  = round(self._discipline_score(inp), 1)
        competitive = round(self._competitive_score(inp), 1)

        composite = round(
            confidence * 0.30 + value * 0.25 + discipline * 0.25 + competitive * 0.20, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, confidence, value, discipline, competitive)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_pricing_gap(composite, inp)
        coach  = self._requires_pricing_coaching(composite, inp)
        loss   = self._estimated_margin_erosion(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = PricingResult(
            rep_id=inp.rep_id,
            region=inp.region,
            pricing_risk=risk,
            pricing_pattern=pattern,
            pricing_severity=severity,
            recommended_action=action,
            confidence_score=confidence,
            value_score=value,
            discipline_score=discipline,
            competitive_score=competitive,
            pricing_composite=composite,
            has_pricing_gap=gap,
            requires_pricing_coaching=coach,
            estimated_margin_erosion_usd=loss,
            pricing_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[PricingInput]) -> list[PricingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_pricing_composite": 0.0,
                "pricing_gap_count": 0,
                "coaching_count": 0,
                "avg_confidence_score": 0.0,
                "avg_value_score": 0.0,
                "avg_discipline_score": 0.0,
                "avg_competitive_score": 0.0,
                "total_estimated_margin_erosion_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_con = total_val = total_dis = total_com = total_loss = 0.0

        for r in self._results:
            risk_counts[r.pricing_risk.value]       = risk_counts.get(r.pricing_risk.value, 0) + 1
            pattern_counts[r.pricing_pattern.value] = pattern_counts.get(r.pricing_pattern.value, 0) + 1
            severity_counts[r.pricing_severity.value] = severity_counts.get(r.pricing_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.pricing_composite
            total_con  += r.confidence_score
            total_val  += r.value_score
            total_dis  += r.discipline_score
            total_com  += r.competitive_score
            total_loss += r.estimated_margin_erosion_usd

        n = len(self._results)

        return {
            "total":                                   n,
            "risk_counts":                             risk_counts,
            "pattern_counts":                          pattern_counts,
            "severity_counts":                         severity_counts,
            "action_counts":                           action_counts,
            "avg_pricing_composite":                   round(total_comp / n, 1),
            "pricing_gap_count":                       sum(1 for r in self._results if r.has_pricing_gap),
            "coaching_count":                          sum(1 for r in self._results if r.requires_pricing_coaching),
            "avg_confidence_score":                    round(total_con / n, 1),
            "avg_value_score":                         round(total_val / n, 1),
            "avg_discipline_score":                    round(total_dis / n, 1),
            "avg_competitive_score":                   round(total_com / n, 1),
            "total_estimated_margin_erosion_usd":      round(total_loss, 2),
        }
