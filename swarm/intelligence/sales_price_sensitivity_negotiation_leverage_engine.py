from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class NegotiationRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class NegotiationPattern(str, Enum):
    none                  = "none"
    first_mover_conceder  = "first_mover_conceder"
    anchor_avoider        = "anchor_avoider"
    multi_round_eroder    = "multi_round_eroder"
    deadline_capitulator  = "deadline_capitulator"
    bundler_destroyer     = "bundler_destroyer"


class NegotiationSeverity(str, Enum):
    disciplined  = "disciplined"
    softening    = "softening"
    eroding      = "eroding"
    collapsing   = "collapsing"


class NegotiationAction(str, Enum):
    no_action                        = "no_action"
    negotiation_awareness_coaching   = "negotiation_awareness_coaching"
    anchor_technique_coaching        = "anchor_technique_coaching"
    concession_discipline_coaching   = "concession_discipline_coaching"
    value_framing_coaching           = "value_framing_coaching"
    deal_desk_negotiation_support    = "deal_desk_negotiation_support"
    executive_negotiation_reset      = "executive_negotiation_reset"


@dataclass
class NegotiationInput:
    rep_id:                              str
    region:                              str
    evaluation_period_id:                str
    first_concession_without_ask_pct:    float   # 0-1 % deals where rep conceded before buyer asked
    avg_concession_rounds_per_deal:      float   # avg # of back-and-forth rounds
    price_anchor_usage_rate_pct:         float   # 0-1 % deals where rep anchored high first
    concession_size_avg_pct:             float   # 0-1 avg size of price concession
    deal_closed_below_floor_price_pct:   float   # 0-1 % deals closed below price floor
    multi_element_trade_rate_pct:        float   # 0-1 % concessions traded for something
    deadline_pressure_concession_pct:   float   # 0-1 % deals where end-of-period pressure caused concession
    bundle_unbundling_rate_pct:          float   # 0-1 % deals where bundle was stripped apart
    legal_hold_up_capitulation_pct:      float   # 0-1 % legal redlines where rep caved on price
    negotiation_preparation_score:       float   # 0-1 (self-assessed or manager-assessed)
    walk_away_rate_pct:                  float   # 0-1 % deals rep walked from on price
    final_price_vs_list_pct:             float   # 0-1 (1.0 = full list price; <1 = discount)
    value_selling_score:                 float   # 0-1 (how often rep sells value vs features)
    competitor_price_match_rate_pct:     float   # 0-1 % deals where rep matched comp price
    procurement_win_rate_pct:            float   # 0-1 win rate when procurement involved
    multi_year_deal_rate_pct:            float   # 0-1 % deals that are multi-year
    payment_terms_concession_pct:        float   # 0-1 % deals where payment terms extended
    total_closed_deals:                  int
    avg_deal_value_usd:                  float


@dataclass
class NegotiationResult:
    rep_id:                          str
    region:                          str
    negotiation_risk:                NegotiationRisk
    negotiation_pattern:             NegotiationPattern
    negotiation_severity:            NegotiationSeverity
    recommended_action:              NegotiationAction
    discipline_score:                float
    leverage_score:                  float
    preparation_score:               float
    value_anchoring_score:           float
    negotiation_composite:           float
    has_negotiation_gap:             bool
    requires_negotiation_coaching:   bool
    estimated_margin_left_usd:       float
    negotiation_signal:              str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                        self.rep_id,
            "region":                        self.region,
            "negotiation_risk":              self.negotiation_risk.value,
            "negotiation_pattern":           self.negotiation_pattern.value,
            "negotiation_severity":          self.negotiation_severity.value,
            "recommended_action":            self.recommended_action.value,
            "discipline_score":              self.discipline_score,
            "leverage_score":                self.leverage_score,
            "preparation_score":             self.preparation_score,
            "value_anchoring_score":         self.value_anchoring_score,
            "negotiation_composite":         self.negotiation_composite,
            "has_negotiation_gap":           self.has_negotiation_gap,
            "requires_negotiation_coaching": self.requires_negotiation_coaching,
            "estimated_margin_left_usd":     self.estimated_margin_left_usd,
            "negotiation_signal":            self.negotiation_signal,
        }


class SalesPriceSensitivityNegotiationLeverageEngine:
    """Detects reps who fold under pressure, training buyers to demand discounts every time."""

    def __init__(self) -> None:
        self._results: List[NegotiationResult] = []

    # ── sub-scores ─────────────────────────────────────────────────────────────

    def _discipline_score(self, inp: NegotiationInput) -> float:
        s = 0.0
        if   inp.first_concession_without_ask_pct  >= 0.55: s += 40
        elif inp.first_concession_without_ask_pct  >= 0.32: s += 22
        elif inp.first_concession_without_ask_pct  >= 0.15: s += 8
        if   inp.deal_closed_below_floor_price_pct >= 0.30: s += 35
        elif inp.deal_closed_below_floor_price_pct >= 0.15: s += 18
        if   inp.multi_element_trade_rate_pct       <= 0.20: s += 25
        elif inp.multi_element_trade_rate_pct       <= 0.45: s += 12
        return min(s, 100.0)

    def _leverage_score(self, inp: NegotiationInput) -> float:
        s = 0.0
        if   inp.avg_concession_rounds_per_deal     >= 4.0: s += 45
        elif inp.avg_concession_rounds_per_deal     >= 2.5: s += 25
        elif inp.avg_concession_rounds_per_deal     >= 1.5: s += 10
        if   inp.deadline_pressure_concession_pct   >= 0.55: s += 30
        elif inp.deadline_pressure_concession_pct   >= 0.30: s += 15
        if   inp.procurement_win_rate_pct           <= 0.25: s += 25
        elif inp.procurement_win_rate_pct           <= 0.50: s += 12
        return min(s, 100.0)

    def _preparation_score(self, inp: NegotiationInput) -> float:
        s = 0.0
        if   inp.negotiation_preparation_score      <= 0.25: s += 40
        elif inp.negotiation_preparation_score      <= 0.50: s += 22
        elif inp.negotiation_preparation_score      <= 0.70: s += 8
        if   inp.walk_away_rate_pct                 <= 0.02: s += 35
        elif inp.walk_away_rate_pct                 <= 0.06: s += 18
        if   inp.legal_hold_up_capitulation_pct     >= 0.55: s += 25
        elif inp.legal_hold_up_capitulation_pct     >= 0.30: s += 12
        return min(s, 100.0)

    def _value_anchoring_score(self, inp: NegotiationInput) -> float:
        s = 0.0
        if   inp.price_anchor_usage_rate_pct        <= 0.20: s += 45
        elif inp.price_anchor_usage_rate_pct        <= 0.45: s += 25
        elif inp.price_anchor_usage_rate_pct        <= 0.65: s += 10
        if   inp.competitor_price_match_rate_pct    >= 0.55: s += 30
        elif inp.competitor_price_match_rate_pct    >= 0.30: s += 15
        if   inp.value_selling_score                <= 0.25: s += 25
        elif inp.value_selling_score                <= 0.55: s += 12
        return min(s, 100.0)

    # ── composite ──────────────────────────────────────────────────────────────

    def _composite(self, di: float, le: float, pr: float, va: float) -> float:
        return min(round(di * 0.30 + le * 0.25 + pr * 0.25 + va * 0.20, 2), 100.0)

    # ── pattern ────────────────────────────────────────────────────────────────

    def _pattern(self, inp: NegotiationInput) -> NegotiationPattern:
        if inp.first_concession_without_ask_pct >= 0.55 and inp.price_anchor_usage_rate_pct <= 0.20:
            return NegotiationPattern.first_mover_conceder
        if inp.price_anchor_usage_rate_pct <= 0.15 and inp.final_price_vs_list_pct <= 0.75:
            return NegotiationPattern.anchor_avoider
        if inp.avg_concession_rounds_per_deal >= 4.0 and inp.concession_size_avg_pct >= 0.15:
            return NegotiationPattern.multi_round_eroder
        if inp.deadline_pressure_concession_pct >= 0.60 and inp.deal_closed_below_floor_price_pct >= 0.20:
            return NegotiationPattern.deadline_capitulator
        if inp.bundle_unbundling_rate_pct >= 0.45 and inp.multi_element_trade_rate_pct <= 0.15:
            return NegotiationPattern.bundler_destroyer
        return NegotiationPattern.none

    # ── thresholds ─────────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> NegotiationRisk:
        if   composite >= 60: return NegotiationRisk.critical
        elif composite >= 40: return NegotiationRisk.high
        elif composite >= 20: return NegotiationRisk.moderate
        return NegotiationRisk.low

    def _severity(self, composite: float) -> NegotiationSeverity:
        if   composite >= 60: return NegotiationSeverity.collapsing
        elif composite >= 40: return NegotiationSeverity.eroding
        elif composite >= 20: return NegotiationSeverity.softening
        return NegotiationSeverity.disciplined

    def _action(self, risk: NegotiationRisk, pattern: NegotiationPattern) -> NegotiationAction:
        if risk == NegotiationRisk.critical:
            if pattern in (NegotiationPattern.multi_round_eroder, NegotiationPattern.deadline_capitulator):
                return NegotiationAction.executive_negotiation_reset
            return NegotiationAction.deal_desk_negotiation_support
        if risk == NegotiationRisk.high:
            if pattern == NegotiationPattern.first_mover_conceder:
                return NegotiationAction.concession_discipline_coaching
            if pattern == NegotiationPattern.anchor_avoider:
                return NegotiationAction.anchor_technique_coaching
            if pattern == NegotiationPattern.multi_round_eroder:
                return NegotiationAction.concession_discipline_coaching
            if pattern == NegotiationPattern.deadline_capitulator:
                return NegotiationAction.value_framing_coaching
            if pattern == NegotiationPattern.bundler_destroyer:
                return NegotiationAction.value_framing_coaching
            return NegotiationAction.concession_discipline_coaching
        if risk == NegotiationRisk.moderate:
            return NegotiationAction.negotiation_awareness_coaching
        return NegotiationAction.no_action

    # ── flags ──────────────────────────────────────────────────────────────────

    def _has_gap(self, inp: NegotiationInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.final_price_vs_list_pct         <= 0.80
            or inp.first_concession_without_ask_pct >= 0.30
        )

    def _requires_coaching(self, inp: NegotiationInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.price_anchor_usage_rate_pct     <= 0.45
            or inp.deal_closed_below_floor_price_pct >= 0.10
        )

    # ── margin left on table ───────────────────────────────────────────────────

    def _margin_left(self, inp: NegotiationInput, composite: float) -> float:
        avg_concession_pct = inp.concession_size_avg_pct * inp.avg_concession_rounds_per_deal
        return round(
            inp.total_closed_deals * inp.avg_deal_value_usd * min(avg_concession_pct, 0.5) * (composite / 100),
            2
        )

    # ── signal ─────────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        NegotiationPattern.first_mover_conceder:  "First-mover conceder",
        NegotiationPattern.anchor_avoider:        "Anchor avoider",
        NegotiationPattern.multi_round_eroder:    "Multi-round eroder",
        NegotiationPattern.deadline_capitulator:  "Deadline capitulator",
        NegotiationPattern.bundler_destroyer:     "Bundler destroyer",
    }

    def _signal(self, inp: NegotiationInput, pattern: NegotiationPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Negotiation discipline healthy — concession rate, anchor usage, "
                "and price-to-list ratio within acceptable benchmarks"
            )
        label      = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        first_pct  = round(inp.first_concession_without_ask_pct * 100)
        anchor_pct = round(inp.price_anchor_usage_rate_pct * 100)
        floor_pct  = round(inp.deal_closed_below_floor_price_pct * 100)
        comp_int   = round(composite)
        return (
            f"{label} — {first_pct}% unprompted concessions — {anchor_pct}% anchor usage — "
            f"{floor_pct}% deals below floor — composite {comp_int}"
        )

    # ── public API ─────────────────────────────────────────────────────────────

    def assess(self, inp: NegotiationInput) -> NegotiationResult:
        di   = self._discipline_score(inp)
        le   = self._leverage_score(inp)
        pr   = self._preparation_score(inp)
        va   = self._value_anchoring_score(inp)
        comp = self._composite(di, le, pr, va)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = NegotiationResult(
            rep_id                        = inp.rep_id,
            region                        = inp.region,
            negotiation_risk              = risk,
            negotiation_pattern           = pattern,
            negotiation_severity          = severity,
            recommended_action            = action,
            discipline_score              = di,
            leverage_score                = le,
            preparation_score             = pr,
            value_anchoring_score         = va,
            negotiation_composite         = comp,
            has_negotiation_gap           = self._has_gap(inp, comp),
            requires_negotiation_coaching = self._requires_coaching(inp, comp),
            estimated_margin_left_usd     = self._margin_left(inp, comp),
            negotiation_signal            = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[NegotiationInput]) -> List[NegotiationResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_negotiation_composite": 0.0,
                "negotiation_gap_count": 0,
                "coaching_count": 0,
                "avg_discipline_score": 0.0,
                "avg_leverage_score": 0.0,
                "avg_preparation_score": 0.0,
                "avg_value_anchoring_score": 0.0,
                "total_estimated_margin_left_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_di = total_le = total_pr = total_va = total_ml = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.negotiation_risk.value]         = risk_counts.get(res.negotiation_risk.value, 0) + 1
            pattern_counts[res.negotiation_pattern.value]   = pattern_counts.get(res.negotiation_pattern.value, 0) + 1
            severity_counts[res.negotiation_severity.value] = severity_counts.get(res.negotiation_severity.value, 0) + 1
            action_counts[res.recommended_action.value]     = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.negotiation_composite
            total_di   += res.discipline_score
            total_le   += res.leverage_score
            total_pr   += res.preparation_score
            total_va   += res.value_anchoring_score
            total_ml   += res.estimated_margin_left_usd
            if res.has_negotiation_gap:           gap_count      += 1
            if res.requires_negotiation_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                             n,
            "risk_counts":                       risk_counts,
            "pattern_counts":                    pattern_counts,
            "severity_counts":                   severity_counts,
            "action_counts":                     action_counts,
            "avg_negotiation_composite":         round(total_comp / n, 1),
            "negotiation_gap_count":             gap_count,
            "coaching_count":                    coaching_count,
            "avg_discipline_score":              round(total_di / n, 1),
            "avg_leverage_score":                round(total_le / n, 1),
            "avg_preparation_score":             round(total_pr / n, 1),
            "avg_value_anchoring_score":         round(total_va / n, 1),
            "total_estimated_margin_left_usd":   round(total_ml, 2),
        }
