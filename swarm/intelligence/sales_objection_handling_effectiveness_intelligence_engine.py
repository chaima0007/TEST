from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ObjectionRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ObjectionPattern(str, Enum):
    none                  = "none"
    price_capitulation    = "price_capitulation"
    value_gap_avoidance   = "value_gap_avoidance"
    competitor_deflection = "competitor_deflection"
    timing_deferral       = "timing_deferral"
    objection_avoidance   = "objection_avoidance"


class ObjectionSeverity(str, Enum):
    proficient  = "proficient"
    managing    = "managing"
    struggling  = "struggling"
    collapsing  = "collapsing"


class ObjectionAction(str, Enum):
    no_action                    = "no_action"
    objection_scripting_coaching = "objection_scripting_coaching"
    roi_articulation_coaching    = "roi_articulation_coaching"
    competitive_response_coaching = "competitive_response_coaching"
    closing_technique_coaching   = "closing_technique_coaching"
    objection_handling_reset     = "objection_handling_reset"


@dataclass
class ObjectionInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    price_objection_to_discount_rate_pct: float
    avg_discount_after_price_objection_pct: float
    price_objection_win_rate_pct: float
    value_objection_close_rate_pct: float
    roi_case_presented_after_objection_pct: float
    proof_of_concept_offered_rate_pct: float
    competitive_objection_win_rate_pct: float
    deals_lost_after_competitive_comparison_pct: float
    battle_card_used_in_competitive_deal_pct: float
    timing_objection_to_slip_rate_pct: float
    next_step_set_after_timing_objection_pct: float
    urgency_event_used_to_counter_timing_pct: float
    total_objections_logged_per_deal: float
    objection_resolved_before_next_stage_pct: float
    deals_with_unresolved_objections_at_close_pct: float
    repeat_objection_rate_pct: float
    executive_referenced_to_resolve_objection_pct: float
    total_deals_with_objections: int
    avg_opportunity_value_usd: float


@dataclass
class ObjectionResult:
    rep_id: str
    region: str
    objection_risk: ObjectionRisk
    objection_pattern: ObjectionPattern
    objection_severity: ObjectionSeverity
    recommended_action: ObjectionAction
    price_score: float
    value_score: float
    competitive_score: float
    timing_score: float
    objection_composite: float
    has_objection_gap: bool
    requires_objection_coaching: bool
    estimated_revenue_surrendered_usd: float
    objection_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                            self.rep_id,
            "region":                            self.region,
            "objection_risk":                    self.objection_risk.value,
            "objection_pattern":                 self.objection_pattern.value,
            "objection_severity":                self.objection_severity.value,
            "recommended_action":                self.recommended_action.value,
            "price_score":                       self.price_score,
            "value_score":                       self.value_score,
            "competitive_score":                 self.competitive_score,
            "timing_score":                      self.timing_score,
            "objection_composite":               self.objection_composite,
            "has_objection_gap":                 self.has_objection_gap,
            "requires_objection_coaching":       self.requires_objection_coaching,
            "estimated_revenue_surrendered_usd": self.estimated_revenue_surrendered_usd,
            "objection_signal":                  self.objection_signal,
        }


class SalesObjectionHandlingEffectivenessIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[ObjectionResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _price_score(self, inp: ObjectionInput) -> float:
        score = 0.0

        if inp.price_objection_to_discount_rate_pct >= 0.70:
            score += 40.0
        elif inp.price_objection_to_discount_rate_pct >= 0.50:
            score += 22.0
        elif inp.price_objection_to_discount_rate_pct >= 0.30:
            score += 8.0

        if inp.avg_discount_after_price_objection_pct >= 0.20:
            score += 35.0
        elif inp.avg_discount_after_price_objection_pct >= 0.10:
            score += 18.0

        if inp.price_objection_win_rate_pct <= 0.30:
            score += 25.0
        elif inp.price_objection_win_rate_pct <= 0.50:
            score += 12.0

        return min(score, 100.0)

    def _value_score(self, inp: ObjectionInput) -> float:
        score = 0.0

        if inp.value_objection_close_rate_pct <= 0.25:
            score += 40.0
        elif inp.value_objection_close_rate_pct <= 0.45:
            score += 22.0
        elif inp.value_objection_close_rate_pct <= 0.65:
            score += 8.0

        if inp.roi_case_presented_after_objection_pct <= 0.30:
            score += 35.0
        elif inp.roi_case_presented_after_objection_pct <= 0.55:
            score += 18.0

        if inp.proof_of_concept_offered_rate_pct <= 0.20:
            score += 25.0
        elif inp.proof_of_concept_offered_rate_pct <= 0.40:
            score += 12.0

        return min(score, 100.0)

    def _competitive_score(self, inp: ObjectionInput) -> float:
        score = 0.0

        if inp.competitive_objection_win_rate_pct <= 0.30:
            score += 45.0
        elif inp.competitive_objection_win_rate_pct <= 0.50:
            score += 25.0
        elif inp.competitive_objection_win_rate_pct <= 0.65:
            score += 10.0

        if inp.deals_lost_after_competitive_comparison_pct >= 0.55:
            score += 30.0
        elif inp.deals_lost_after_competitive_comparison_pct >= 0.35:
            score += 15.0

        if inp.battle_card_used_in_competitive_deal_pct <= 0.25:
            score += 25.0
        elif inp.battle_card_used_in_competitive_deal_pct <= 0.50:
            score += 12.0

        return min(score, 100.0)

    def _timing_score(self, inp: ObjectionInput) -> float:
        score = 0.0

        if inp.timing_objection_to_slip_rate_pct >= 0.65:
            score += 40.0
        elif inp.timing_objection_to_slip_rate_pct >= 0.45:
            score += 22.0
        elif inp.timing_objection_to_slip_rate_pct >= 0.25:
            score += 8.0

        if inp.next_step_set_after_timing_objection_pct <= 0.40:
            score += 35.0
        elif inp.next_step_set_after_timing_objection_pct <= 0.65:
            score += 18.0

        if inp.urgency_event_used_to_counter_timing_pct <= 0.20:
            score += 25.0
        elif inp.urgency_event_used_to_counter_timing_pct <= 0.40:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: ObjectionInput,
                         price: float, value: float,
                         competitive: float, timing: float) -> ObjectionPattern:
        # Price capitulation: always discounts when price objection raised
        if inp.price_objection_to_discount_rate_pct >= 0.65 and inp.avg_discount_after_price_objection_pct >= 0.15:
            return ObjectionPattern.price_capitulation

        # Value gap avoidance: can't articulate ROI, doesn't present business case
        if value >= 40 and inp.roi_case_presented_after_objection_pct <= 0.25:
            return ObjectionPattern.value_gap_avoidance

        # Competitor deflection: loses when compared directly to competitors
        if inp.competitive_objection_win_rate_pct <= 0.25 and inp.deals_lost_after_competitive_comparison_pct >= 0.50:
            return ObjectionPattern.competitor_deflection

        # Timing deferral: always accepts "not now" without creating urgency
        if inp.timing_objection_to_slip_rate_pct >= 0.60 and inp.next_step_set_after_timing_objection_pct <= 0.35:
            return ObjectionPattern.timing_deferral

        # Objection avoidance: doesn't surface or log objections, avoids difficult conversations
        if inp.total_objections_logged_per_deal <= 0.5 and price >= 30:
            return ObjectionPattern.objection_avoidance

        return ObjectionPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> ObjectionRisk:
        if composite >= 60:
            return ObjectionRisk.critical
        if composite >= 40:
            return ObjectionRisk.high
        if composite >= 20:
            return ObjectionRisk.moderate
        return ObjectionRisk.low

    def _severity(self, composite: float) -> ObjectionSeverity:
        if composite >= 60:
            return ObjectionSeverity.collapsing
        if composite >= 40:
            return ObjectionSeverity.struggling
        if composite >= 20:
            return ObjectionSeverity.managing
        return ObjectionSeverity.proficient

    def _action(self, risk: ObjectionRisk, pattern: ObjectionPattern) -> ObjectionAction:
        if risk == ObjectionRisk.critical:
            if pattern == ObjectionPattern.price_capitulation:
                return ObjectionAction.closing_technique_coaching
            if pattern == ObjectionPattern.value_gap_avoidance:
                return ObjectionAction.roi_articulation_coaching
            return ObjectionAction.objection_handling_reset
        if risk == ObjectionRisk.high:
            if pattern == ObjectionPattern.competitor_deflection:
                return ObjectionAction.competitive_response_coaching
            if pattern == ObjectionPattern.timing_deferral:
                return ObjectionAction.closing_technique_coaching
            return ObjectionAction.objection_scripting_coaching
        if risk == ObjectionRisk.moderate:
            return ObjectionAction.objection_scripting_coaching
        return ObjectionAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_objection_gap(self, composite: float, inp: ObjectionInput) -> bool:
        return (
            composite >= 40
            or inp.value_objection_close_rate_pct <= 0.35
            or inp.competitive_objection_win_rate_pct <= 0.30
        )

    def _requires_objection_coaching(self, composite: float, inp: ObjectionInput) -> bool:
        return (
            composite >= 30
            or inp.price_objection_to_discount_rate_pct >= 0.50
            or inp.timing_objection_to_slip_rate_pct >= 0.45
        )

    # ------------------------------------------------------------------
    # Revenue surrendered estimate
    # ------------------------------------------------------------------

    def _estimated_revenue_surrendered(self, inp: ObjectionInput, composite: float) -> float:
        return round(
            inp.total_deals_with_objections
            * inp.avg_opportunity_value_usd
            * inp.price_objection_to_discount_rate_pct
            * inp.avg_discount_after_price_objection_pct
            * (composite / 100.0),
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: ObjectionInput,
                 pattern: ObjectionPattern, composite: float) -> str:
        if pattern == ObjectionPattern.none and composite < 20:
            return "Objection handling proficient — price defense, value articulation, and competitive positioning within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.price_objection_to_discount_rate_pct * 100:.0f}% price objections lead to discount")
        parts.append(f"{inp.value_objection_close_rate_pct * 100:.0f}% value objection close rate")
        parts.append(f"{inp.competitive_objection_win_rate_pct * 100:.0f}% competitive win rate")
        label = pattern.value.replace("_", " ") if pattern != ObjectionPattern.none else "Objection handling risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: ObjectionInput) -> ObjectionResult:
        price       = round(self._price_score(inp), 1)
        value       = round(self._value_score(inp), 1)
        competitive = round(self._competitive_score(inp), 1)
        timing      = round(self._timing_score(inp), 1)

        composite = round(
            price * 0.30 + value * 0.30 + competitive * 0.25 + timing * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, price, value, competitive, timing)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_objection_gap(composite, inp)
        coach  = self._requires_objection_coaching(composite, inp)
        loss   = self._estimated_revenue_surrendered(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = ObjectionResult(
            rep_id=inp.rep_id,
            region=inp.region,
            objection_risk=risk,
            objection_pattern=pattern,
            objection_severity=severity,
            recommended_action=action,
            price_score=price,
            value_score=value,
            competitive_score=competitive,
            timing_score=timing,
            objection_composite=composite,
            has_objection_gap=gap,
            requires_objection_coaching=coach,
            estimated_revenue_surrendered_usd=loss,
            objection_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[ObjectionInput]) -> list[ObjectionResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_objection_composite": 0.0,
                "objection_gap_count": 0,
                "coaching_count": 0,
                "avg_price_score": 0.0,
                "avg_value_score": 0.0,
                "avg_competitive_score": 0.0,
                "avg_timing_score": 0.0,
                "total_estimated_revenue_surrendered_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_pri = total_val = total_com = total_tim = total_loss = 0.0

        for r in self._results:
            risk_counts[r.objection_risk.value]         = risk_counts.get(r.objection_risk.value, 0) + 1
            pattern_counts[r.objection_pattern.value]   = pattern_counts.get(r.objection_pattern.value, 0) + 1
            severity_counts[r.objection_severity.value] = severity_counts.get(r.objection_severity.value, 0) + 1
            action_counts[r.recommended_action.value]   = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.objection_composite
            total_pri  += r.price_score
            total_val  += r.value_score
            total_com  += r.competitive_score
            total_tim  += r.timing_score
            total_loss += r.estimated_revenue_surrendered_usd

        n = len(self._results)

        return {
            "total":                                        n,
            "risk_counts":                                  risk_counts,
            "pattern_counts":                               pattern_counts,
            "severity_counts":                              severity_counts,
            "action_counts":                                action_counts,
            "avg_objection_composite":                      round(total_comp / n, 1),
            "objection_gap_count":                          sum(1 for r in self._results if r.has_objection_gap),
            "coaching_count":                               sum(1 for r in self._results if r.requires_objection_coaching),
            "avg_price_score":                              round(total_pri / n, 1),
            "avg_value_score":                              round(total_val / n, 1),
            "avg_competitive_score":                        round(total_com / n, 1),
            "avg_timing_score":                             round(total_tim / n, 1),
            "total_estimated_revenue_surrendered_usd":      round(total_loss, 2),
        }
