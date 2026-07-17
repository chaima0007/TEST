from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class ValueRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ValuePattern(str, Enum):
    none                = "none"
    value_vacuum        = "value_vacuum"
    price_before_value  = "price_before_value"
    proof_dependent     = "proof_dependent"
    roi_ambiguity       = "roi_ambiguity"
    executive_disconnect = "executive_disconnect"


class ValueSeverity(str, Enum):
    compelling   = "compelling"
    adequate     = "adequate"
    deteriorating = "deteriorating"
    failing      = "failing"


class ValueAction(str, Enum):
    no_action                    = "no_action"
    value_message_refresh        = "value_message_refresh"
    roi_quantification_coaching  = "roi_quantification_coaching"
    proof_strategy_coaching      = "proof_strategy_coaching"
    executive_value_coaching     = "executive_value_coaching"
    value_repositioning_program  = "value_repositioning_program"
    commercial_reset             = "commercial_reset"


@dataclass
class ValueInput:
    rep_id:                          str
    region:                          str
    evaluation_period_id:            str
    value_message_consistency_score: float  # 0-1 message quality
    pricing_objection_rate_pct:      float  # 0-1
    roi_challenge_rate_pct:          float  # 0-1 buyer challenges ROI
    value_prop_adoption_rate_pct:    float  # 0-1 uses approved messaging
    executive_engagement_on_value_pct: float  # 0-1 exec value convos
    reference_request_rate_pct:      float  # 0-1 buyers ask for proof
    competitive_loss_on_value_pct:   float  # 0-1 lost on value cited
    discount_to_close_rate_pct:      float  # 0-1 deals needing discount
    avg_discount_depth_pct:          float  # 0-1 avg discount when applied
    value_story_usage_rate_pct:      float  # 0-1 success stories used
    business_case_creation_rate_pct: float  # 0-1 business cases created
    quantified_roi_presented_pct:    float  # 0-1 presents ROI numerically
    persona_message_alignment_score: float  # 0-1 right message right buyer
    industry_vertical_win_rate:      float  # 0-1 win rate in target verticals
    late_stage_value_reframe_pct:    float  # 0-1 re-pitches value late in cycle
    value_champion_development_rate: float  # 0-1 coaches champion to sell value
    price_sensitivity_trigger_rate:  float  # 0-1 price raised before value set
    total_closed_deals:              int
    avg_deal_value_usd:              float


@dataclass
class ValueResult:
    rep_id:                       str
    region:                       str
    value_risk:                   ValueRisk
    value_pattern:                ValuePattern
    value_severity:               ValueSeverity
    recommended_action:           ValueAction
    message_quality_score:        float
    value_defense_score:          float
    proof_score:                  float
    deal_economics_score:         float
    value_composite:              float
    has_value_gap:                bool
    requires_value_coaching:      bool
    estimated_lost_revenue_usd:   float
    value_signal:                 str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "value_risk":                   self.value_risk.value,
            "value_pattern":                self.value_pattern.value,
            "value_severity":               self.value_severity.value,
            "recommended_action":           self.recommended_action.value,
            "message_quality_score":        self.message_quality_score,
            "value_defense_score":          self.value_defense_score,
            "proof_score":                  self.proof_score,
            "deal_economics_score":         self.deal_economics_score,
            "value_composite":              self.value_composite,
            "has_value_gap":                self.has_value_gap,
            "requires_value_coaching":      self.requires_value_coaching,
            "estimated_lost_revenue_usd":   self.estimated_lost_revenue_usd,
            "value_signal":                 self.value_signal,
        }


class SalesValuePropositionDeteriorationIntelligenceEngine:
    """Detects rep-level value proposition decay — price sensitivity, ROI ambiguity, proof dependency."""

    def __init__(self) -> None:
        self._results: List[ValueResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _message_quality_score(self, inp: ValueInput) -> float:
        s = 0.0
        if   inp.value_message_consistency_score   <= 0.30: s += 40
        elif inp.value_message_consistency_score   <= 0.55: s += 22
        elif inp.value_message_consistency_score   <= 0.75: s += 8
        if   inp.value_prop_adoption_rate_pct      <= 0.40: s += 35
        elif inp.value_prop_adoption_rate_pct      <= 0.60: s += 18
        if   inp.persona_message_alignment_score   <= 0.30: s += 25
        elif inp.persona_message_alignment_score   <= 0.55: s += 12
        return min(s, 100.0)

    def _value_defense_score(self, inp: ValueInput) -> float:
        s = 0.0
        if   inp.pricing_objection_rate_pct        >= 0.55: s += 40
        elif inp.pricing_objection_rate_pct        >= 0.35: s += 22
        elif inp.pricing_objection_rate_pct        >= 0.20: s += 8
        if   inp.late_stage_value_reframe_pct      >= 0.45: s += 35
        elif inp.late_stage_value_reframe_pct      >= 0.25: s += 18
        if   inp.roi_challenge_rate_pct            >= 0.40: s += 25
        elif inp.roi_challenge_rate_pct            >= 0.25: s += 12
        return min(s, 100.0)

    def _proof_score(self, inp: ValueInput) -> float:
        s = 0.0
        if   inp.quantified_roi_presented_pct      <= 0.25: s += 40
        elif inp.quantified_roi_presented_pct      <= 0.50: s += 22
        elif inp.quantified_roi_presented_pct      <= 0.70: s += 8
        if   inp.business_case_creation_rate_pct   <= 0.20: s += 35
        elif inp.business_case_creation_rate_pct   <= 0.45: s += 18
        if   inp.reference_request_rate_pct        >= 0.50: s += 25
        elif inp.reference_request_rate_pct        >= 0.30: s += 12
        return min(s, 100.0)

    def _deal_economics_score(self, inp: ValueInput) -> float:
        s = 0.0
        if   inp.discount_to_close_rate_pct        >= 0.60: s += 45
        elif inp.discount_to_close_rate_pct        >= 0.40: s += 25
        elif inp.discount_to_close_rate_pct        >= 0.25: s += 10
        if   inp.avg_discount_depth_pct            >= 0.25: s += 30
        elif inp.avg_discount_depth_pct            >= 0.15: s += 15
        if   inp.price_sensitivity_trigger_rate    >= 0.55: s += 25
        elif inp.price_sensitivity_trigger_rate    >= 0.35: s += 10
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, m: float, v: float, p: float, d: float) -> float:
        return min(round(m * 0.30 + v * 0.30 + p * 0.25 + d * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: ValueInput) -> ValuePattern:
        if inp.value_message_consistency_score <= 0.35 and inp.competitive_loss_on_value_pct >= 0.35:
            return ValuePattern.value_vacuum
        if inp.price_sensitivity_trigger_rate >= 0.45 and inp.discount_to_close_rate_pct >= 0.45:
            return ValuePattern.price_before_value
        if inp.reference_request_rate_pct >= 0.40 and inp.business_case_creation_rate_pct <= 0.30:
            return ValuePattern.proof_dependent
        if inp.roi_challenge_rate_pct >= 0.35 and inp.quantified_roi_presented_pct <= 0.35:
            return ValuePattern.roi_ambiguity
        if inp.executive_engagement_on_value_pct <= 0.25 and inp.late_stage_value_reframe_pct >= 0.35:
            return ValuePattern.executive_disconnect
        return ValuePattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> ValueRisk:
        if   composite >= 60: return ValueRisk.critical
        elif composite >= 40: return ValueRisk.high
        elif composite >= 20: return ValueRisk.moderate
        return ValueRisk.low

    def _severity(self, composite: float) -> ValueSeverity:
        if   composite >= 60: return ValueSeverity.failing
        elif composite >= 40: return ValueSeverity.deteriorating
        elif composite >= 20: return ValueSeverity.adequate
        return ValueSeverity.compelling

    def _action(self, risk: ValueRisk, pattern: ValuePattern) -> ValueAction:
        if risk == ValueRisk.critical:
            if pattern in (ValuePattern.value_vacuum, ValuePattern.price_before_value):
                return ValueAction.commercial_reset
            return ValueAction.value_repositioning_program
        if risk == ValueRisk.high:
            if pattern == ValuePattern.value_vacuum:
                return ValueAction.value_repositioning_program
            if pattern == ValuePattern.price_before_value:
                return ValueAction.roi_quantification_coaching
            if pattern == ValuePattern.proof_dependent:
                return ValueAction.proof_strategy_coaching
            if pattern == ValuePattern.roi_ambiguity:
                return ValueAction.roi_quantification_coaching
            if pattern == ValuePattern.executive_disconnect:
                return ValueAction.executive_value_coaching
            return ValueAction.value_message_refresh
        if risk == ValueRisk.moderate:
            return ValueAction.value_message_refresh
        return ValueAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: ValueInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.pricing_objection_rate_pct      >= 0.35
            or inp.discount_to_close_rate_pct      >= 0.40
        )

    def _requires_coaching(self, inp: ValueInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.quantified_roi_presented_pct    <= 0.50
            or inp.value_message_consistency_score <= 0.60
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _lost_revenue(self, inp: ValueInput, composite: float) -> float:
        value_loss_rate = min(1.0, (inp.competitive_loss_on_value_pct + inp.discount_to_close_rate_pct * inp.avg_discount_depth_pct))
        return round(inp.total_closed_deals * inp.avg_deal_value_usd * value_loss_rate * (composite / 100), 2)

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        ValuePattern.value_vacuum:          "Value vacuum",
        ValuePattern.price_before_value:    "Price before value",
        ValuePattern.proof_dependent:       "Proof dependent",
        ValuePattern.roi_ambiguity:         "ROI ambiguity",
        ValuePattern.executive_disconnect:  "Executive disconnect",
    }

    def _signal(self, inp: ValueInput, pattern: ValuePattern, composite: float) -> str:
        if composite < 20:
            return (
                "Value proposition strong — message consistency, ROI quantification, "
                "proof strategy, and deal economics within benchmarks"
            )
        label     = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        obj_pct   = round(inp.pricing_objection_rate_pct * 100)
        disc_pct  = round(inp.discount_to_close_rate_pct * 100)
        roi_pct   = round(inp.quantified_roi_presented_pct * 100)
        comp_int  = round(composite)
        return (
            f"{label} — {obj_pct}% pricing objections — "
            f"{disc_pct}% deals discounted to close — "
            f"{roi_pct}% with quantified ROI — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: ValueInput) -> ValueResult:
        m  = self._message_quality_score(inp)
        v  = self._value_defense_score(inp)
        p  = self._proof_score(inp)
        d  = self._deal_economics_score(inp)
        comp = self._composite(m, v, p, d)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = ValueResult(
            rep_id                  = inp.rep_id,
            region                  = inp.region,
            value_risk              = risk,
            value_pattern           = pattern,
            value_severity          = severity,
            recommended_action      = action,
            message_quality_score   = m,
            value_defense_score     = v,
            proof_score             = p,
            deal_economics_score    = d,
            value_composite         = comp,
            has_value_gap           = self._has_gap(inp, comp),
            requires_value_coaching = self._requires_coaching(inp, comp),
            estimated_lost_revenue_usd = self._lost_revenue(inp, comp),
            value_signal            = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ValueInput]) -> List[ValueResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_value_composite": 0.0,
                "value_gap_count": 0,
                "coaching_count": 0,
                "avg_message_quality_score": 0.0,
                "avg_value_defense_score": 0.0,
                "avg_proof_score": 0.0,
                "avg_deal_economics_score": 0.0,
                "total_estimated_lost_revenue_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_m = total_v = total_p = total_d = total_lr = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.value_risk.value]       = risk_counts.get(res.value_risk.value, 0) + 1
            pattern_counts[res.value_pattern.value] = pattern_counts.get(res.value_pattern.value, 0) + 1
            severity_counts[res.value_severity.value] = severity_counts.get(res.value_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.value_composite
            total_m    += res.message_quality_score
            total_v    += res.value_defense_score
            total_p    += res.proof_score
            total_d    += res.deal_economics_score
            total_lr   += res.estimated_lost_revenue_usd
            if res.has_value_gap:           gap_count      += 1
            if res.requires_value_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_value_composite":                  round(total_comp / n, 1),
            "value_gap_count":                      gap_count,
            "coaching_count":                       coaching_count,
            "avg_message_quality_score":            round(total_m / n, 1),
            "avg_value_defense_score":              round(total_v / n, 1),
            "avg_proof_score":                      round(total_p / n, 1),
            "avg_deal_economics_score":             round(total_d / n, 1),
            "total_estimated_lost_revenue_usd":     round(total_lr, 2),
        }
