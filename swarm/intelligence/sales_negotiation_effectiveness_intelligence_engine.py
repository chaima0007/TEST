from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class NegotiationRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class NegotiationPattern(str, Enum):
    none                    = "none"
    excessive_discounting   = "excessive_discounting"
    premature_concession    = "premature_concession"
    price_erosion           = "price_erosion"
    value_abandonment       = "value_abandonment"
    negotiation_avoidance   = "negotiation_avoidance"


class NegotiationSeverity(str, Enum):
    strong      = "strong"
    developing  = "developing"
    vulnerable  = "vulnerable"
    collapsing  = "collapsing"


class NegotiationAction(str, Enum):
    no_action                    = "no_action"
    negotiation_coaching         = "negotiation_coaching"
    discount_authority_review    = "discount_authority_review"
    value_selling_training       = "value_selling_training"
    pricing_integrity_program    = "pricing_integrity_program"
    deal_desk_escalation         = "deal_desk_escalation"


@dataclass
class NegotiationEffectivenessInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_deals_negotiated: int
    deals_requiring_discount_count: int
    avg_discount_depth_pct: float
    max_discount_given_pct: float
    deals_closed_at_list_price_count: int
    avg_negotiation_rounds: float
    deals_won_after_negotiation_count: int
    deals_lost_on_price_count: int
    first_concession_timing_days: float
    concession_without_request_count: int
    multi_round_deals_count: int
    value_anchor_usage_pct: float
    competitive_pressure_discount_pct: float
    deals_with_procurement_count: int
    procurement_discount_rate_pct: float
    avg_contract_value_vs_target_pct: float
    late_stage_reprice_count: int
    avg_time_to_close_after_negotiation_days: float
    avg_opportunity_value_usd: float


@dataclass
class NegotiationEffectivenessResult:
    rep_id: str
    region: str
    negotiation_risk: NegotiationRisk
    negotiation_pattern: NegotiationPattern
    negotiation_severity: NegotiationSeverity
    recommended_action: NegotiationAction
    discount_discipline_score: float
    concession_behavior_score: float
    value_defense_score: float
    close_effectiveness_score: float
    negotiation_composite: float
    has_pricing_risk: bool
    requires_negotiation_coaching: bool
    estimated_margin_erosion_usd: float
    negotiation_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "negotiation_risk":             self.negotiation_risk.value,
            "negotiation_pattern":          self.negotiation_pattern.value,
            "negotiation_severity":         self.negotiation_severity.value,
            "recommended_action":           self.recommended_action.value,
            "discount_discipline_score":    self.discount_discipline_score,
            "concession_behavior_score":    self.concession_behavior_score,
            "value_defense_score":          self.value_defense_score,
            "close_effectiveness_score":    self.close_effectiveness_score,
            "negotiation_composite":        self.negotiation_composite,
            "has_pricing_risk":             self.has_pricing_risk,
            "requires_negotiation_coaching": self.requires_negotiation_coaching,
            "estimated_margin_erosion_usd": self.estimated_margin_erosion_usd,
            "negotiation_signal":           self.negotiation_signal,
        }


class SalesNegotiationEffectivenessIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[NegotiationEffectivenessResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _discount_discipline_score(self, inp: NegotiationEffectivenessInput) -> float:
        score = 0.0

        if inp.avg_discount_depth_pct >= 0.25:
            score += 40.0
        elif inp.avg_discount_depth_pct >= 0.15:
            score += 22.0
        elif inp.avg_discount_depth_pct >= 0.08:
            score += 8.0

        if inp.max_discount_given_pct >= 0.40:
            score += 30.0
        elif inp.max_discount_given_pct >= 0.25:
            score += 15.0

        total = max(inp.total_deals_negotiated, 1)
        discount_rate = inp.deals_requiring_discount_count / total
        if discount_rate >= 0.70:
            score += 25.0
        elif discount_rate >= 0.50:
            score += 13.0

        return min(score, 100.0)

    def _concession_behavior_score(self, inp: NegotiationEffectivenessInput) -> float:
        score = 0.0

        if inp.first_concession_timing_days <= 1.0:
            score += 40.0
        elif inp.first_concession_timing_days <= 3.0:
            score += 20.0
        elif inp.first_concession_timing_days <= 7.0:
            score += 8.0

        total = max(inp.total_deals_negotiated, 1)
        unsolicited_rate = inp.concession_without_request_count / total
        if unsolicited_rate >= 0.30:
            score += 35.0
        elif unsolicited_rate >= 0.15:
            score += 18.0
        elif unsolicited_rate >= 0.05:
            score += 7.0

        if inp.avg_negotiation_rounds >= 4.0:
            score += 20.0
        elif inp.avg_negotiation_rounds >= 3.0:
            score += 10.0

        return min(score, 100.0)

    def _value_defense_score(self, inp: NegotiationEffectivenessInput) -> float:
        score = 0.0

        if inp.value_anchor_usage_pct < 0.20:
            score += 35.0
        elif inp.value_anchor_usage_pct < 0.40:
            score += 18.0
        elif inp.value_anchor_usage_pct < 0.60:
            score += 7.0

        if inp.avg_contract_value_vs_target_pct < 0.80:
            score += 30.0
        elif inp.avg_contract_value_vs_target_pct < 0.90:
            score += 15.0

        if inp.late_stage_reprice_count >= 3:
            score += 25.0
        elif inp.late_stage_reprice_count >= 1:
            score += 12.0

        return min(score, 100.0)

    def _close_effectiveness_score(self, inp: NegotiationEffectivenessInput) -> float:
        score = 0.0

        total = max(inp.total_deals_negotiated, 1)
        price_loss_rate = inp.deals_lost_on_price_count / total
        if price_loss_rate >= 0.25:
            score += 40.0
        elif price_loss_rate >= 0.15:
            score += 20.0
        elif price_loss_rate >= 0.08:
            score += 8.0

        if inp.avg_time_to_close_after_negotiation_days >= 30.0:
            score += 35.0
        elif inp.avg_time_to_close_after_negotiation_days >= 14.0:
            score += 18.0
        elif inp.avg_time_to_close_after_negotiation_days >= 7.0:
            score += 7.0

        if inp.procurement_discount_rate_pct >= 0.20:
            score += 20.0
        elif inp.procurement_discount_rate_pct >= 0.10:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: NegotiationEffectivenessInput,
                          discount: float, concession: float,
                          value: float, close_eff: float) -> NegotiationPattern:
        if discount >= 40 and inp.avg_discount_depth_pct >= 0.20:
            return NegotiationPattern.excessive_discounting

        if concession >= 35 and inp.first_concession_timing_days <= 2.0:
            return NegotiationPattern.premature_concession

        if value >= 35 and inp.avg_contract_value_vs_target_pct < 0.85:
            return NegotiationPattern.price_erosion

        total = max(inp.total_deals_negotiated, 1)
        list_price_rate = inp.deals_closed_at_list_price_count / total
        if value >= 25 and inp.value_anchor_usage_pct < 0.30 and list_price_rate < 0.10:
            return NegotiationPattern.value_abandonment

        if close_eff >= 25 and inp.avg_negotiation_rounds >= 3.0:
            return NegotiationPattern.negotiation_avoidance

        return NegotiationPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> NegotiationRisk:
        if composite >= 60:
            return NegotiationRisk.critical
        if composite >= 40:
            return NegotiationRisk.high
        if composite >= 20:
            return NegotiationRisk.moderate
        return NegotiationRisk.low

    def _severity(self, composite: float) -> NegotiationSeverity:
        if composite >= 60:
            return NegotiationSeverity.collapsing
        if composite >= 40:
            return NegotiationSeverity.vulnerable
        if composite >= 20:
            return NegotiationSeverity.developing
        return NegotiationSeverity.strong

    def _action(self, risk: NegotiationRisk, pattern: NegotiationPattern) -> NegotiationAction:
        if risk == NegotiationRisk.critical:
            if pattern == NegotiationPattern.excessive_discounting:
                return NegotiationAction.deal_desk_escalation
            if pattern == NegotiationPattern.price_erosion:
                return NegotiationAction.pricing_integrity_program
            return NegotiationAction.deal_desk_escalation
        if risk == NegotiationRisk.high:
            if pattern == NegotiationPattern.premature_concession:
                return NegotiationAction.negotiation_coaching
            if pattern == NegotiationPattern.value_abandonment:
                return NegotiationAction.value_selling_training
            return NegotiationAction.discount_authority_review
        if risk == NegotiationRisk.moderate:
            return NegotiationAction.negotiation_coaching
        return NegotiationAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_pricing_risk(self, composite: float,
                           inp: NegotiationEffectivenessInput) -> bool:
        return (
            composite >= 40
            or inp.avg_discount_depth_pct >= 0.20
            or inp.avg_contract_value_vs_target_pct < 0.80
        )

    def _requires_negotiation_coaching(self, composite: float,
                                         inp: NegotiationEffectivenessInput) -> bool:
        total = max(inp.total_deals_negotiated, 1)
        unsolicited_rate = inp.concession_without_request_count / total
        return (
            composite >= 30
            or inp.avg_discount_depth_pct >= 0.15
            or unsolicited_rate >= 0.20
        )

    # ------------------------------------------------------------------
    # Margin erosion
    # ------------------------------------------------------------------

    def _estimated_margin_erosion(self, inp: NegotiationEffectivenessInput,
                                   composite: float) -> float:
        return round(
            inp.deals_requiring_discount_count * inp.avg_opportunity_value_usd * inp.avg_discount_depth_pct * (composite / 100.0), 2
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: NegotiationEffectivenessInput,
                 pattern: NegotiationPattern, composite: float) -> str:
        if pattern == NegotiationPattern.none and composite < 20:
            return "Negotiation effectiveness healthy — pricing discipline and value defense within benchmarks"
        parts: list[str] = []
        if inp.avg_discount_depth_pct >= 0.08:
            parts.append(f"{inp.avg_discount_depth_pct*100:.0f}% avg discount")
        if inp.first_concession_timing_days <= 7.0:
            parts.append(f"{inp.first_concession_timing_days:.0f}d first concession")
        if inp.avg_contract_value_vs_target_pct < 1.0:
            parts.append(f"{inp.avg_contract_value_vs_target_pct*100:.0f}% of target ACV")
        label = pattern.value.replace("_", " ") if pattern != NegotiationPattern.none else "Negotiation risk"
        summary = " — ".join(parts) if parts else "pricing integrity declining"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: NegotiationEffectivenessInput) -> NegotiationEffectivenessResult:
        discount   = round(self._discount_discipline_score(inp), 1)
        concession = round(self._concession_behavior_score(inp), 1)
        value      = round(self._value_defense_score(inp), 1)
        close_eff  = round(self._close_effectiveness_score(inp), 1)

        composite = round(
            discount * 0.30 + concession * 0.30 + value * 0.25 + close_eff * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, discount, concession, value, close_eff)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        pricing_risk = self._has_pricing_risk(composite, inp)
        coaching     = self._requires_negotiation_coaching(composite, inp)
        erosion      = self._estimated_margin_erosion(inp, composite)
        signal       = self._signal(inp, pattern, composite)

        result = NegotiationEffectivenessResult(
            rep_id=inp.rep_id,
            region=inp.region,
            negotiation_risk=risk,
            negotiation_pattern=pattern,
            negotiation_severity=severity,
            recommended_action=action,
            discount_discipline_score=discount,
            concession_behavior_score=concession,
            value_defense_score=value,
            close_effectiveness_score=close_eff,
            negotiation_composite=composite,
            has_pricing_risk=pricing_risk,
            requires_negotiation_coaching=coaching,
            estimated_margin_erosion_usd=erosion,
            negotiation_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[NegotiationEffectivenessInput]) -> list[NegotiationEffectivenessResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_negotiation_composite": 0.0,
                "pricing_risk_count": 0,
                "coaching_count": 0,
                "avg_discount_discipline_score": 0.0,
                "avg_concession_behavior_score": 0.0,
                "avg_value_defense_score": 0.0,
                "avg_close_effectiveness_score": 0.0,
                "total_estimated_margin_erosion_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_disc = total_conc = total_val = total_close = total_erosion = 0.0

        for r in self._results:
            risk_counts[r.negotiation_risk.value]       = risk_counts.get(r.negotiation_risk.value, 0) + 1
            pattern_counts[r.negotiation_pattern.value] = pattern_counts.get(r.negotiation_pattern.value, 0) + 1
            severity_counts[r.negotiation_severity.value] = severity_counts.get(r.negotiation_severity.value, 0) + 1
            action_counts[r.recommended_action.value]   = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp   += r.negotiation_composite
            total_disc   += r.discount_discipline_score
            total_conc   += r.concession_behavior_score
            total_val    += r.value_defense_score
            total_close  += r.close_effectiveness_score
            total_erosion += r.estimated_margin_erosion_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_negotiation_composite":            round(total_comp / n, 1),
            "pricing_risk_count":                   sum(1 for r in self._results if r.has_pricing_risk),
            "coaching_count":                       sum(1 for r in self._results if r.requires_negotiation_coaching),
            "avg_discount_discipline_score":        round(total_disc / n, 1),
            "avg_concession_behavior_score":        round(total_conc / n, 1),
            "avg_value_defense_score":              round(total_val / n, 1),
            "avg_close_effectiveness_score":        round(total_close / n, 1),
            "total_estimated_margin_erosion_usd":   round(total_erosion, 2),
        }
