from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class DiscountRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class DiscountPattern(str, Enum):
    none               = "none"
    panic_discounter   = "panic_discounter"
    relationship_briber = "relationship_briber"
    price_first_seller = "price_first_seller"
    approval_bypasser  = "approval_bypasser"
    chronic_leaker     = "chronic_leaker"


class DiscountSeverity(str, Enum):
    disciplined  = "disciplined"
    drifting     = "drifting"
    leaking      = "leaking"
    eroding      = "eroding"


class DiscountAction(str, Enum):
    no_action                      = "no_action"
    discount_monitoring            = "discount_monitoring"
    pricing_discipline_coaching    = "pricing_discipline_coaching"
    approval_process_enforcement   = "approval_process_enforcement"
    value_selling_coaching         = "value_selling_coaching"
    deal_desk_review               = "deal_desk_review"
    pricing_authority_reset        = "pricing_authority_reset"


@dataclass
class DiscountInput:
    rep_id:                            str
    region:                            str
    evaluation_period_id:              str
    avg_discount_depth_pct:            float  # 0-1 avg discount applied
    discount_frequency_pct:            float  # 0-1 (% deals discounted)
    unauthorized_discount_rate_pct:    float  # 0-1 (% discounts without approval)
    early_discount_offer_rate_pct:     float  # 0-1 (% times discount offered in first meeting)
    discount_as_first_response_pct:    float  # 0-1 (% objections handled by discount)
    gross_margin_vs_target_pct:        float  # -1 to 1 (negative = below target)
    price_objection_concession_rate_pct: float  # 0-1 (% price objections resolved via discount)
    multi_level_discount_rate_pct:     float  # 0-1 (% deals with >1 discount round)
    discount_to_close_conversion_pct:  float  # 0-1 (% discounts that actually close)
    competitor_price_match_rate_pct:   float  # 0-1 (% time matches competitor price)
    list_price_win_rate_pct:           float  # 0-1 (% deals won at list price)
    end_of_quarter_spike_rate_pct:     float  # 0-1 (% discounts in last 2 weeks of quarter)
    approval_request_bypass_count:     int    # count of unapproved discounts
    avg_deal_cycle_with_discount_days: float  # avg cycle when discounted
    value_objection_to_discount_pct:   float  # 0-1 (% value objections → discount not reframe)
    deal_size_after_discount_shrink_pct: float  # 0-1 (deal size reduction after discount)
    repeat_discount_same_customer_pct: float  # 0-1 (% repeat customers asking for same discount)
    total_closed_deals:                int
    avg_deal_value_usd:                float


@dataclass
class DiscountResult:
    rep_id:                             str
    region:                             str
    discount_risk:                      DiscountRisk
    discount_pattern:                   DiscountPattern
    discount_severity:                  DiscountSeverity
    recommended_action:                 DiscountAction
    frequency_score:                    float
    depth_score:                        float
    discipline_score:                   float
    value_defense_score:                float
    discount_composite:                 float
    has_discount_gap:                   bool
    requires_discount_intervention:     bool
    estimated_margin_erosion_usd:       float
    discount_signal:                    str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "discount_risk":                    self.discount_risk.value,
            "discount_pattern":                 self.discount_pattern.value,
            "discount_severity":                self.discount_severity.value,
            "recommended_action":               self.recommended_action.value,
            "frequency_score":                  self.frequency_score,
            "depth_score":                      self.depth_score,
            "discipline_score":                 self.discipline_score,
            "value_defense_score":              self.value_defense_score,
            "discount_composite":               self.discount_composite,
            "has_discount_gap":                 self.has_discount_gap,
            "requires_discount_intervention":   self.requires_discount_intervention,
            "estimated_margin_erosion_usd":     self.estimated_margin_erosion_usd,
            "discount_signal":                  self.discount_signal,
        }


class SalesDiscountLeakageMarginErosionIntelligenceEngine:
    """Detects reps leaking margin through excessive, unauthorized, or panic discounting."""

    def __init__(self) -> None:
        self._results: List[DiscountResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _frequency_score(self, inp: DiscountInput) -> float:
        s = 0.0
        if   inp.discount_frequency_pct             >= 0.70: s += 40
        elif inp.discount_frequency_pct             >= 0.50: s += 22
        elif inp.discount_frequency_pct             >= 0.35: s += 8
        if   inp.multi_level_discount_rate_pct      >= 0.45: s += 35
        elif inp.multi_level_discount_rate_pct      >= 0.25: s += 18
        if   inp.end_of_quarter_spike_rate_pct      >= 0.55: s += 25
        elif inp.end_of_quarter_spike_rate_pct      >= 0.35: s += 12
        return min(s, 100.0)

    def _depth_score(self, inp: DiscountInput) -> float:
        s = 0.0
        if   inp.avg_discount_depth_pct             >= 0.30: s += 40
        elif inp.avg_discount_depth_pct             >= 0.18: s += 22
        elif inp.avg_discount_depth_pct             >= 0.10: s += 8
        if   inp.deal_size_after_discount_shrink_pct >= 0.25: s += 35
        elif inp.deal_size_after_discount_shrink_pct >= 0.12: s += 18
        if   inp.gross_margin_vs_target_pct          <= -0.15: s += 25
        elif inp.gross_margin_vs_target_pct          <= -0.05: s += 12
        return min(s, 100.0)

    def _discipline_score(self, inp: DiscountInput) -> float:
        s = 0.0
        if   inp.unauthorized_discount_rate_pct     >= 0.40: s += 40
        elif inp.unauthorized_discount_rate_pct     >= 0.20: s += 22
        elif inp.unauthorized_discount_rate_pct     >= 0.08: s += 8
        if   inp.early_discount_offer_rate_pct      >= 0.50: s += 35
        elif inp.early_discount_offer_rate_pct      >= 0.28: s += 18
        if   inp.approval_request_bypass_count      >= 4: s += 25
        elif inp.approval_request_bypass_count      >= 2: s += 12
        return min(s, 100.0)

    def _value_defense_score(self, inp: DiscountInput) -> float:
        s = 0.0
        if   inp.discount_as_first_response_pct     >= 0.55: s += 45
        elif inp.discount_as_first_response_pct     >= 0.30: s += 25
        elif inp.discount_as_first_response_pct     >= 0.15: s += 10
        if   inp.price_objection_concession_rate_pct >= 0.55: s += 30
        elif inp.price_objection_concession_rate_pct >= 0.30: s += 15
        if   inp.list_price_win_rate_pct             <= 0.10: s += 25
        elif inp.list_price_win_rate_pct             <= 0.25: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────────

    def _composite(self, fr: float, de: float, di: float, vd: float) -> float:
        return min(round(fr * 0.25 + de * 0.30 + di * 0.25 + vd * 0.20, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, inp: DiscountInput) -> DiscountPattern:
        if inp.end_of_quarter_spike_rate_pct >= 0.45 and inp.avg_discount_depth_pct >= 0.20:
            return DiscountPattern.panic_discounter
        if inp.repeat_discount_same_customer_pct >= 0.50 and inp.list_price_win_rate_pct <= 0.15:
            return DiscountPattern.relationship_briber
        if inp.early_discount_offer_rate_pct >= 0.45 and inp.discount_as_first_response_pct >= 0.40:
            return DiscountPattern.price_first_seller
        if inp.unauthorized_discount_rate_pct >= 0.30 and inp.approval_request_bypass_count >= 3:
            return DiscountPattern.approval_bypasser
        if inp.discount_frequency_pct >= 0.60 and inp.multi_level_discount_rate_pct >= 0.35:
            return DiscountPattern.chronic_leaker
        return DiscountPattern.none

    # ── thresholds ────────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> DiscountRisk:
        if   composite >= 60: return DiscountRisk.critical
        elif composite >= 40: return DiscountRisk.high
        elif composite >= 20: return DiscountRisk.moderate
        return DiscountRisk.low

    def _severity(self, composite: float) -> DiscountSeverity:
        if   composite >= 60: return DiscountSeverity.eroding
        elif composite >= 40: return DiscountSeverity.leaking
        elif composite >= 20: return DiscountSeverity.drifting
        return DiscountSeverity.disciplined

    def _action(self, risk: DiscountRisk, pattern: DiscountPattern) -> DiscountAction:
        if risk == DiscountRisk.critical:
            if pattern in (DiscountPattern.approval_bypasser, DiscountPattern.chronic_leaker):
                return DiscountAction.pricing_authority_reset
            return DiscountAction.deal_desk_review
        if risk == DiscountRisk.high:
            if pattern == DiscountPattern.panic_discounter:
                return DiscountAction.value_selling_coaching
            if pattern == DiscountPattern.relationship_briber:
                return DiscountAction.pricing_discipline_coaching
            if pattern == DiscountPattern.price_first_seller:
                return DiscountAction.value_selling_coaching
            if pattern == DiscountPattern.approval_bypasser:
                return DiscountAction.approval_process_enforcement
            if pattern == DiscountPattern.chronic_leaker:
                return DiscountAction.deal_desk_review
            return DiscountAction.pricing_discipline_coaching
        if risk == DiscountRisk.moderate:
            return DiscountAction.discount_monitoring
        return DiscountAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────────

    def _has_gap(self, inp: DiscountInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.avg_discount_depth_pct >= 0.20
            or inp.unauthorized_discount_rate_pct >= 0.15
        )

    def _requires_intervention(self, inp: DiscountInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.discount_frequency_pct >= 0.50
            or inp.gross_margin_vs_target_pct <= -0.08
        )

    # ── margin erosion ────────────────────────────────────────────────────────

    def _margin_erosion(self, inp: DiscountInput, composite: float) -> float:
        base_revenue    = inp.total_closed_deals * inp.avg_deal_value_usd
        erosion_rate    = inp.avg_discount_depth_pct * inp.discount_frequency_pct
        risk_multiplier = composite / 100
        return round(base_revenue * erosion_rate * risk_multiplier, 2)

    # ── signal ────────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        DiscountPattern.panic_discounter:    "Panic discounter",
        DiscountPattern.relationship_briber: "Relationship briber",
        DiscountPattern.price_first_seller:  "Price-first seller",
        DiscountPattern.approval_bypasser:   "Approval bypasser",
        DiscountPattern.chronic_leaker:      "Chronic leaker",
    }

    def _signal(self, inp: DiscountInput, pattern: DiscountPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Discount discipline healthy — frequency, depth, authorization, "
                "and value defense within benchmarks"
            )
        label       = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        disc_pct    = round(inp.discount_frequency_pct * 100)
        depth_pct   = round(inp.avg_discount_depth_pct * 100)
        unauth_pct  = round(inp.unauthorized_discount_rate_pct * 100)
        comp_int    = round(composite)
        return (
            f"{label} — {disc_pct}% deals discounted — avg depth {depth_pct}% — "
            f"{unauth_pct}% unauthorized — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, inp: DiscountInput) -> DiscountResult:
        fr  = self._frequency_score(inp)
        de  = self._depth_score(inp)
        di  = self._discipline_score(inp)
        vd  = self._value_defense_score(inp)
        comp = self._composite(fr, de, di, vd)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = DiscountResult(
            rep_id                          = inp.rep_id,
            region                          = inp.region,
            discount_risk                   = risk,
            discount_pattern                = pattern,
            discount_severity               = severity,
            recommended_action              = action,
            frequency_score                 = fr,
            depth_score                     = de,
            discipline_score                = di,
            value_defense_score             = vd,
            discount_composite              = comp,
            has_discount_gap                = self._has_gap(inp, comp),
            requires_discount_intervention  = self._requires_intervention(inp, comp),
            estimated_margin_erosion_usd    = self._margin_erosion(inp, comp),
            discount_signal                 = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[DiscountInput]) -> List[DiscountResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_discount_composite": 0.0,
                "discount_gap_count": 0,
                "intervention_count": 0,
                "avg_frequency_score": 0.0,
                "avg_depth_score": 0.0,
                "avg_discipline_score": 0.0,
                "avg_value_defense_score": 0.0,
                "total_estimated_margin_erosion_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_fr = total_de = total_di = total_vd = total_me = 0.0
        gap_count = intervention_count = 0

        for res in self._results:
            risk_counts[res.discount_risk.value]         = risk_counts.get(res.discount_risk.value, 0) + 1
            pattern_counts[res.discount_pattern.value]   = pattern_counts.get(res.discount_pattern.value, 0) + 1
            severity_counts[res.discount_severity.value] = severity_counts.get(res.discount_severity.value, 0) + 1
            action_counts[res.recommended_action.value]  = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.discount_composite
            total_fr   += res.frequency_score
            total_de   += res.depth_score
            total_di   += res.discipline_score
            total_vd   += res.value_defense_score
            total_me   += res.estimated_margin_erosion_usd
            if res.has_discount_gap:              gap_count          += 1
            if res.requires_discount_intervention: intervention_count += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_discount_composite":               round(total_comp / n, 1),
            "discount_gap_count":                   gap_count,
            "intervention_count":                   intervention_count,
            "avg_frequency_score":                  round(total_fr / n, 1),
            "avg_depth_score":                      round(total_de / n, 1),
            "avg_discipline_score":                 round(total_di / n, 1),
            "avg_value_defense_score":              round(total_vd / n, 1),
            "total_estimated_margin_erosion_usd":   round(total_me, 2),
        }
