from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class PricingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class PricingPattern(str, Enum):
    none                   = "none"
    discount_reflex        = "discount_reflex"
    margin_eroder          = "margin_eroder"
    late_stage_capitulator = "late_stage_capitulator"
    multi_discount_stacker = "multi_discount_stacker"
    value_misaligner       = "value_misaligner"


class PricingSeverity(str, Enum):
    disciplined  = "disciplined"
    managed      = "managed"
    aggressive   = "aggressive"
    uncontrolled = "uncontrolled"


class PricingAction(str, Enum):
    no_action                   = "no_action"
    discount_awareness_coaching  = "discount_awareness_coaching"
    value_selling_coaching       = "value_selling_coaching"
    negotiation_discipline_coaching = "negotiation_discipline_coaching"
    margin_recovery_coaching     = "margin_recovery_coaching"
    pricing_approval_requirement = "pricing_approval_requirement"
    pricing_intervention         = "pricing_intervention"


@dataclass
class PricingInput:
    rep_id:                           str
    region:                           str
    evaluation_period_id:             str
    avg_discount_pct:                 float   # average discount given (0–1)
    discount_frequency_pct:           float   # % of deals receiving ANY discount (0–1)
    max_discount_given_pct:           float   # largest single discount (0–1)
    avg_gross_margin_pct:             float   # avg gross margin on closed deals (0–1)
    target_gross_margin_pct:          float   # company target margin (0–1)
    late_stage_discount_rate_pct:     float   # % of deals discounted after proposal (0–1)
    multi_discount_deal_rate_pct:     float   # % of deals with 2+ discount rounds (0–1)
    price_objection_rate_pct:         float   # % of calls with price objection (0–1)
    first_ask_concession_rate_pct:    float   # % of times first ask = immediate concession (0–1)
    list_price_close_rate_pct:        float   # % of deals closed at list price (0–1)
    approval_override_rate_pct:       float   # % of deals needing pricing override (0–1)
    competitor_price_match_rate_pct:  float   # % of deals matched to competitor price (0–1)
    avg_deal_cycle_vs_discount_corr:  float   # correlation deal length with discounting (0–1)
    total_deals_closed:               int
    avg_deal_size_usd:                float
    total_revenue_usd:                float
    quota_usd:                        float
    avg_opportunity_value_usd:        float


@dataclass
class PricingResult:
    rep_id:                        str
    region:                        str
    pricing_risk:                  PricingRisk
    pricing_pattern:               PricingPattern
    pricing_severity:              PricingSeverity
    recommended_action:            PricingAction
    discount_depth_score:          float
    discount_frequency_score:      float
    margin_protection_score:       float
    negotiation_discipline_score:  float
    pricing_composite:             float
    has_pricing_gap:               bool
    requires_pricing_coaching:     bool
    estimated_margin_loss_usd:     float
    pricing_signal:                str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                        self.rep_id,
            "region":                        self.region,
            "pricing_risk":                  self.pricing_risk.value,
            "pricing_pattern":               self.pricing_pattern.value,
            "pricing_severity":              self.pricing_severity.value,
            "recommended_action":            self.recommended_action.value,
            "discount_depth_score":          self.discount_depth_score,
            "discount_frequency_score":      self.discount_frequency_score,
            "margin_protection_score":       self.margin_protection_score,
            "negotiation_discipline_score":  self.negotiation_discipline_score,
            "pricing_composite":             self.pricing_composite,
            "has_pricing_gap":               self.has_pricing_gap,
            "requires_pricing_coaching":     self.requires_pricing_coaching,
            "estimated_margin_loss_usd":     self.estimated_margin_loss_usd,
            "pricing_signal":                self.pricing_signal,
        }


class SalesPricingDisciplineIntelligenceEngine:

    def __init__(self) -> None:
        self._results: List[PricingResult] = []

    def _discount_depth_score(self, inp: PricingInput) -> float:
        s = 0.0
        if inp.avg_discount_pct >= 0.25:
            s += 45
        elif inp.avg_discount_pct >= 0.15:
            s += 28
        elif inp.avg_discount_pct >= 0.08:
            s += 12
        if inp.max_discount_given_pct >= 0.40:
            s += 35
        elif inp.max_discount_given_pct >= 0.28:
            s += 18
        elif inp.max_discount_given_pct >= 0.18:
            s += 6
        if inp.price_objection_rate_pct >= 0.60:
            s += 20
        elif inp.price_objection_rate_pct >= 0.40:
            s += 10
        return min(s, 100.0)

    def _discount_frequency_score(self, inp: PricingInput) -> float:
        s = 0.0
        if inp.discount_frequency_pct >= 0.70:
            s += 45
        elif inp.discount_frequency_pct >= 0.50:
            s += 28
        elif inp.discount_frequency_pct >= 0.35:
            s += 12
        if inp.multi_discount_deal_rate_pct >= 0.40:
            s += 35
        elif inp.multi_discount_deal_rate_pct >= 0.25:
            s += 18
        elif inp.multi_discount_deal_rate_pct >= 0.12:
            s += 6
        if inp.list_price_close_rate_pct <= 0.20:
            s += 20
        elif inp.list_price_close_rate_pct <= 0.40:
            s += 10
        return min(s, 100.0)

    def _margin_protection_score(self, inp: PricingInput) -> float:
        s = 0.0
        margin_gap = inp.target_gross_margin_pct - inp.avg_gross_margin_pct
        if margin_gap >= 0.15:
            s += 45
        elif margin_gap >= 0.08:
            s += 28
        elif margin_gap >= 0.03:
            s += 12
        if inp.approval_override_rate_pct >= 0.30:
            s += 35
        elif inp.approval_override_rate_pct >= 0.18:
            s += 18
        elif inp.approval_override_rate_pct >= 0.08:
            s += 6
        if inp.competitor_price_match_rate_pct >= 0.40:
            s += 20
        elif inp.competitor_price_match_rate_pct >= 0.25:
            s += 10
        return min(s, 100.0)

    def _negotiation_discipline_score(self, inp: PricingInput) -> float:
        s = 0.0
        if inp.first_ask_concession_rate_pct >= 0.60:
            s += 45
        elif inp.first_ask_concession_rate_pct >= 0.40:
            s += 28
        elif inp.first_ask_concession_rate_pct >= 0.25:
            s += 12
        if inp.late_stage_discount_rate_pct >= 0.50:
            s += 35
        elif inp.late_stage_discount_rate_pct >= 0.35:
            s += 18
        elif inp.late_stage_discount_rate_pct >= 0.20:
            s += 6
        if inp.avg_deal_cycle_vs_discount_corr >= 0.60:
            s += 20
        elif inp.avg_deal_cycle_vs_discount_corr >= 0.40:
            s += 10
        return min(s, 100.0)

    def _composite(self, dd: float, df: float, mp: float, nd: float) -> float:
        return round(dd * 0.30 + df * 0.25 + mp * 0.25 + nd * 0.20, 2)

    def _pattern(self, inp: PricingInput) -> PricingPattern:
        if inp.avg_discount_pct >= 0.20 and inp.first_ask_concession_rate_pct >= 0.55:
            return PricingPattern.discount_reflex
        margin_gap = inp.target_gross_margin_pct - inp.avg_gross_margin_pct
        if margin_gap >= 0.12 and inp.approval_override_rate_pct >= 0.25:
            return PricingPattern.margin_eroder
        if inp.late_stage_discount_rate_pct >= 0.45 and inp.multi_discount_deal_rate_pct >= 0.30:
            return PricingPattern.late_stage_capitulator
        if inp.multi_discount_deal_rate_pct >= 0.35 and inp.discount_frequency_pct >= 0.55:
            return PricingPattern.multi_discount_stacker
        if inp.price_objection_rate_pct >= 0.55 and inp.list_price_close_rate_pct <= 0.25:
            return PricingPattern.value_misaligner
        return PricingPattern.none

    def _risk(self, composite: float) -> PricingRisk:
        if composite >= 60: return PricingRisk.critical
        if composite >= 40: return PricingRisk.high
        if composite >= 20: return PricingRisk.moderate
        return PricingRisk.low

    def _severity(self, composite: float) -> PricingSeverity:
        if composite >= 60: return PricingSeverity.uncontrolled
        if composite >= 40: return PricingSeverity.aggressive
        if composite >= 20: return PricingSeverity.managed
        return PricingSeverity.disciplined

    def _action(self, risk: PricingRisk, pattern: PricingPattern) -> PricingAction:
        if risk == PricingRisk.critical:
            if pattern == PricingPattern.margin_eroder:
                return PricingAction.pricing_intervention
            return PricingAction.pricing_approval_requirement
        if risk == PricingRisk.high:
            if pattern == PricingPattern.discount_reflex:
                return PricingAction.discount_awareness_coaching
            if pattern == PricingPattern.value_misaligner:
                return PricingAction.value_selling_coaching
            if pattern == PricingPattern.late_stage_capitulator:
                return PricingAction.negotiation_discipline_coaching
            if pattern == PricingPattern.multi_discount_stacker:
                return PricingAction.margin_recovery_coaching
            return PricingAction.negotiation_discipline_coaching
        if risk == PricingRisk.moderate:
            return PricingAction.discount_awareness_coaching
        return PricingAction.no_action

    def _has_gap(self, inp: PricingInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.avg_discount_pct >= 0.15
            or inp.discount_frequency_pct >= 0.50
        )

    def _requires_coaching(self, inp: PricingInput, composite: float) -> bool:
        return (
            composite >= 20
            or inp.first_ask_concession_rate_pct >= 0.35
            or inp.multi_discount_deal_rate_pct >= 0.20
        )

    def _margin_loss(self, inp: PricingInput, composite: float) -> float:
        margin_gap = max(0.0, inp.target_gross_margin_pct - inp.avg_gross_margin_pct)
        return round(inp.total_revenue_usd * margin_gap * (composite / 100.0), 2)

    def _signal(self, inp: PricingInput, pattern: PricingPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Pricing discipline strong — discount depth, frequency, "
                "and negotiation posture within benchmarks"
            )
        labels = {
            PricingPattern.discount_reflex:        "Discount reflex",
            PricingPattern.margin_eroder:          "Margin eroder",
            PricingPattern.late_stage_capitulator: "Late-stage capitulator",
            PricingPattern.multi_discount_stacker: "Multi-discount stacker",
            PricingPattern.value_misaligner:       "Value misaligner",
        }
        label    = labels.get(pattern, "Pricing gap detected")
        disc_pct = round(inp.avg_discount_pct * 100)
        freq_pct = round(inp.discount_frequency_pct * 100)
        margin   = round(inp.avg_gross_margin_pct * 100)
        comp_int = round(composite)
        return (
            f"{label} — {disc_pct}% avg discount — "
            f"{freq_pct}% deals discounted — "
            f"{margin}% avg gross margin — composite {comp_int}"
        )

    def assess(self, inp: PricingInput) -> PricingResult:
        dd = self._discount_depth_score(inp)
        df = self._discount_frequency_score(inp)
        mp = self._margin_protection_score(inp)
        nd = self._negotiation_discipline_score(inp)
        comp    = self._composite(dd, df, mp, nd)
        pattern = self._pattern(inp)
        risk    = self._risk(comp)
        sev     = self._severity(comp)
        action  = self._action(risk, pattern)
        result  = PricingResult(
            rep_id                       = inp.rep_id,
            region                       = inp.region,
            pricing_risk                 = risk,
            pricing_pattern              = pattern,
            pricing_severity             = sev,
            recommended_action           = action,
            discount_depth_score         = round(dd, 2),
            discount_frequency_score     = round(df, 2),
            margin_protection_score      = round(mp, 2),
            negotiation_discipline_score = round(nd, 2),
            pricing_composite            = comp,
            has_pricing_gap              = self._has_gap(inp, comp),
            requires_pricing_coaching    = self._requires_coaching(inp, comp),
            estimated_margin_loss_usd    = self._margin_loss(inp, comp),
            pricing_signal               = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[PricingInput]) -> List[PricingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        rr = self._results
        if not rr:
            return {
                "total": 0, "risk_counts": {}, "pattern_counts": {},
                "severity_counts": {}, "action_counts": {},
                "avg_pricing_composite": 0.0, "pricing_gap_count": 0,
                "coaching_count": 0, "avg_discount_depth_score": 0.0,
                "avg_discount_frequency_score": 0.0,
                "avg_margin_protection_score": 0.0,
                "avg_negotiation_discipline_score": 0.0,
                "total_estimated_margin_loss_usd": 0.0,
            }
        n = len(rr)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tdd = tdf = tmp = tnd = trev = 0.0
        gc = cc = 0
        for r in rr:
            rc[r.pricing_risk.value]          = rc.get(r.pricing_risk.value, 0) + 1
            pc[r.pricing_pattern.value]       = pc.get(r.pricing_pattern.value, 0) + 1
            sc[r.pricing_severity.value]      = sc.get(r.pricing_severity.value, 0) + 1
            ac[r.recommended_action.value]    = ac.get(r.recommended_action.value, 0) + 1
            tdd  += r.discount_depth_score
            tdf  += r.discount_frequency_score
            tmp  += r.margin_protection_score
            tnd  += r.negotiation_discipline_score
            trev += r.estimated_margin_loss_usd
            gc   += r.has_pricing_gap
            cc   += r.requires_pricing_coaching
        return {
            "total":                               n,
            "risk_counts":                         rc,
            "pattern_counts":                      pc,
            "severity_counts":                     sc,
            "action_counts":                       ac,
            "avg_pricing_composite":               round(sum(r.pricing_composite for r in rr) / n, 1),
            "pricing_gap_count":                   gc,
            "coaching_count":                      cc,
            "avg_discount_depth_score":            round(tdd / n, 1),
            "avg_discount_frequency_score":        round(tdf / n, 1),
            "avg_margin_protection_score":         round(tmp / n, 1),
            "avg_negotiation_discipline_score":    round(tnd / n, 1),
            "total_estimated_margin_loss_usd":     round(trev, 2),
        }
