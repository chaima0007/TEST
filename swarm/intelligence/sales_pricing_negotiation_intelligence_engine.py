from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class NegotiationRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class NegotiationPattern(str, Enum):
    none                  = "none"
    chronic_discounting   = "chronic_discounting"
    value_erosion         = "value_erosion"
    margin_collapse       = "margin_collapse"
    price_concession_habit = "price_concession_habit"
    competitive_surrender = "competitive_surrender"


class NegotiationSeverity(str, Enum):
    disciplined  = "disciplined"
    lenient      = "lenient"
    compromised  = "compromised"
    collapsing   = "collapsing"


class NegotiationAction(str, Enum):
    no_action                  = "no_action"
    discount_discipline_review = "discount_discipline_review"
    value_messaging_training   = "value_messaging_training"
    pricing_floor_enforcement  = "pricing_floor_enforcement"
    negotiation_coaching       = "negotiation_coaching"
    deal_desk_escalation       = "deal_desk_escalation"


@dataclass
class PricingNegotiationInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_deals_negotiated: int
    deals_with_discount_applied: int
    avg_discount_pct: float
    max_discount_applied_pct: float
    deals_below_floor_price: int
    discounts_approved_by_manager: int
    discounts_self_approved: int
    list_price_deals_closed: int
    value_add_instead_of_discount_count: int
    multi_year_deals_closed: int
    avg_deal_size_negotiated_usd: float
    avg_deal_size_post_negotiation_usd: float
    competitive_deals_price_matched: int
    prospects_rejected_due_to_price: int
    deals_lost_on_price_alone: int
    negotiation_cycle_avg_days: float
    concession_rounds_avg: float
    gross_margin_avg_pct: float
    repeat_buyer_discount_rate_pct: float


@dataclass
class PricingNegotiationResult:
    rep_id: str
    region: str
    negotiation_risk: NegotiationRisk
    negotiation_pattern: NegotiationPattern
    negotiation_severity: NegotiationSeverity
    recommended_action: NegotiationAction
    discount_discipline_score: float
    value_retention_score: float
    margin_protection_score: float
    negotiation_efficiency_score: float
    negotiation_effectiveness_composite: float
    is_margin_at_risk: bool
    requires_pricing_intervention: bool
    estimated_margin_loss_usd: float
    negotiation_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                               self.rep_id,
            "region":                               self.region,
            "negotiation_risk":                     self.negotiation_risk.value,
            "negotiation_pattern":                  self.negotiation_pattern.value,
            "negotiation_severity":                 self.negotiation_severity.value,
            "recommended_action":                   self.recommended_action.value,
            "discount_discipline_score":            self.discount_discipline_score,
            "value_retention_score":                self.value_retention_score,
            "margin_protection_score":              self.margin_protection_score,
            "negotiation_efficiency_score":         self.negotiation_efficiency_score,
            "negotiation_effectiveness_composite":  self.negotiation_effectiveness_composite,
            "is_margin_at_risk":                    self.is_margin_at_risk,
            "requires_pricing_intervention":        self.requires_pricing_intervention,
            "estimated_margin_loss_usd":            self.estimated_margin_loss_usd,
            "negotiation_signal":                   self.negotiation_signal,
        }


class SalesPricingNegotiationIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[PricingNegotiationResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _discount_discipline_score(self, inp: PricingNegotiationInput) -> float:
        score = 0.0
        total = max(inp.total_deals_negotiated, 1)

        discount_rate = inp.deals_with_discount_applied / total
        if discount_rate >= 0.70:
            score += 40.0
        elif discount_rate >= 0.50:
            score += 22.0
        elif discount_rate >= 0.35:
            score += 8.0

        if inp.avg_discount_pct >= 25.0:
            score += 30.0
        elif inp.avg_discount_pct >= 15.0:
            score += 18.0
        elif inp.avg_discount_pct >= 8.0:
            score += 7.0

        self_approved_denom = max(inp.discounts_approved_by_manager + inp.discounts_self_approved, 1)
        self_rate = inp.discounts_self_approved / self_approved_denom
        if self_rate >= 0.60:
            score += 20.0
        elif self_rate >= 0.40:
            score += 10.0

        return min(score, 100.0)

    def _value_retention_score(self, inp: PricingNegotiationInput) -> float:
        score = 0.0
        total = max(inp.total_deals_negotiated, 1)

        if inp.avg_deal_size_negotiated_usd > 0:
            erosion_pct = 1.0 - (inp.avg_deal_size_post_negotiation_usd / inp.avg_deal_size_negotiated_usd)
            if erosion_pct >= 0.20:
                score += 40.0
            elif erosion_pct >= 0.12:
                score += 22.0
            elif erosion_pct >= 0.06:
                score += 8.0

        value_add_rate = inp.value_add_instead_of_discount_count / total
        if value_add_rate < 0.10:
            score += 30.0
        elif value_add_rate < 0.25:
            score += 15.0

        list_price_rate = inp.list_price_deals_closed / total
        if list_price_rate < 0.10:
            score += 20.0
        elif list_price_rate < 0.25:
            score += 10.0

        return min(score, 100.0)

    def _margin_protection_score(self, inp: PricingNegotiationInput) -> float:
        score = 0.0
        total = max(inp.total_deals_negotiated, 1)

        if inp.gross_margin_avg_pct < 0.30:
            score += 40.0
        elif inp.gross_margin_avg_pct < 0.45:
            score += 22.0
        elif inp.gross_margin_avg_pct < 0.55:
            score += 8.0

        floor_rate = inp.deals_below_floor_price / total
        if floor_rate >= 0.20:
            score += 30.0
        elif floor_rate >= 0.10:
            score += 15.0
        elif floor_rate >= 0.05:
            score += 5.0

        if inp.max_discount_applied_pct >= 40.0:
            score += 20.0
        elif inp.max_discount_applied_pct >= 30.0:
            score += 10.0

        return min(score, 100.0)

    def _negotiation_efficiency_score(self, inp: PricingNegotiationInput) -> float:
        score = 0.0

        if inp.concession_rounds_avg >= 4.0:
            score += 35.0
        elif inp.concession_rounds_avg >= 2.5:
            score += 18.0
        elif inp.concession_rounds_avg >= 1.5:
            score += 7.0

        if inp.negotiation_cycle_avg_days >= 30:
            score += 30.0
        elif inp.negotiation_cycle_avg_days >= 18:
            score += 15.0
        elif inp.negotiation_cycle_avg_days >= 10:
            score += 5.0

        total = max(inp.total_deals_negotiated, 1)
        competitive_price_match_rate = inp.competitive_deals_price_matched / total
        if competitive_price_match_rate >= 0.40:
            score += 25.0
        elif competitive_price_match_rate >= 0.25:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: PricingNegotiationInput,
                          discipline: float, value: float,
                          margin: float, efficiency: float) -> NegotiationPattern:
        # Priority: margin_collapse > chronic_discounting > competitive_surrender
        #           > value_erosion > price_concession_habit > none
        total = max(inp.total_deals_negotiated, 1)

        if margin >= 40 and inp.gross_margin_avg_pct < 0.35:
            return NegotiationPattern.margin_collapse

        discount_rate = inp.deals_with_discount_applied / total
        if discipline >= 35 and discount_rate >= 0.60 and inp.avg_discount_pct >= 15.0:
            return NegotiationPattern.chronic_discounting

        comp_rate = inp.competitive_deals_price_matched / total
        if efficiency >= 30 and comp_rate >= 0.35:
            return NegotiationPattern.competitive_surrender

        if value >= 30 and inp.value_add_instead_of_discount_count < 3:
            return NegotiationPattern.value_erosion

        if inp.concession_rounds_avg >= 3.0 and inp.deals_lost_on_price_alone <= 1:
            return NegotiationPattern.price_concession_habit

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
            return NegotiationSeverity.compromised
        if composite >= 20:
            return NegotiationSeverity.lenient
        return NegotiationSeverity.disciplined

    def _action(self, risk: NegotiationRisk, pattern: NegotiationPattern) -> NegotiationAction:
        if risk == NegotiationRisk.critical:
            if pattern == NegotiationPattern.margin_collapse:
                return NegotiationAction.deal_desk_escalation
            if pattern == NegotiationPattern.chronic_discounting:
                return NegotiationAction.pricing_floor_enforcement
            return NegotiationAction.negotiation_coaching
        if risk == NegotiationRisk.high:
            if pattern == NegotiationPattern.value_erosion:
                return NegotiationAction.value_messaging_training
            if pattern == NegotiationPattern.competitive_surrender:
                return NegotiationAction.negotiation_coaching
            return NegotiationAction.discount_discipline_review
        if risk == NegotiationRisk.moderate:
            return NegotiationAction.discount_discipline_review
        return NegotiationAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _is_margin_at_risk(self, composite: float,
                            inp: PricingNegotiationInput) -> bool:
        total = max(inp.total_deals_negotiated, 1)
        floor_rate = inp.deals_below_floor_price / total
        return (
            composite >= 40
            or inp.gross_margin_avg_pct < 0.35
            or floor_rate >= 0.15
        )

    def _requires_pricing_intervention(self, composite: float,
                                        inp: PricingNegotiationInput) -> bool:
        return (
            composite >= 30
            or inp.avg_discount_pct >= 20.0
            or inp.concession_rounds_avg >= 3.0
        )

    # ------------------------------------------------------------------
    # Margin loss
    # ------------------------------------------------------------------

    def _estimated_margin_loss(self, inp: PricingNegotiationInput,
                                composite: float) -> float:
        if inp.avg_deal_size_negotiated_usd <= 0:
            return 0.0
        erosion = max(inp.avg_deal_size_negotiated_usd - inp.avg_deal_size_post_negotiation_usd, 0.0)
        return round(erosion * inp.deals_with_discount_applied * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: PricingNegotiationInput,
                 pattern: NegotiationPattern, composite: float) -> str:
        if pattern == NegotiationPattern.none and composite < 20:
            return "Pricing discipline maintained across negotiations"
        parts: list[str] = []
        if inp.avg_discount_pct >= 8.0:
            parts.append(f"{inp.avg_discount_pct:.0f}% avg discount")
        if inp.deals_below_floor_price >= 1:
            parts.append(f"{inp.deals_below_floor_price} below-floor deals")
        if inp.concession_rounds_avg >= 2.0:
            parts.append(f"{inp.concession_rounds_avg:.1f} avg concession rounds")
        if inp.deals_lost_on_price_alone >= 1:
            parts.append(f"{inp.deals_lost_on_price_alone} lost on price alone")
        label = pattern.value.replace("_", " ") if pattern != NegotiationPattern.none else "Negotiation risk"
        summary = " — ".join(parts) if parts else "pricing discipline degrading"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: PricingNegotiationInput) -> PricingNegotiationResult:
        discipline  = round(self._discount_discipline_score(inp), 1)
        value       = round(self._value_retention_score(inp), 1)
        margin      = round(self._margin_protection_score(inp), 1)
        efficiency  = round(self._negotiation_efficiency_score(inp), 1)

        composite = round(discipline * 0.30 + value * 0.25 + margin * 0.30 + efficiency * 0.15, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, discipline, value, margin, efficiency)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        at_risk    = self._is_margin_at_risk(composite, inp)
        interv     = self._requires_pricing_intervention(composite, inp)
        loss       = self._estimated_margin_loss(inp, composite)
        signal     = self._signal(inp, pattern, composite)

        result = PricingNegotiationResult(
            rep_id=inp.rep_id,
            region=inp.region,
            negotiation_risk=risk,
            negotiation_pattern=pattern,
            negotiation_severity=severity,
            recommended_action=action,
            discount_discipline_score=discipline,
            value_retention_score=value,
            margin_protection_score=margin,
            negotiation_efficiency_score=efficiency,
            negotiation_effectiveness_composite=composite,
            is_margin_at_risk=at_risk,
            requires_pricing_intervention=interv,
            estimated_margin_loss_usd=loss,
            negotiation_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[PricingNegotiationInput]) -> list[PricingNegotiationResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_negotiation_effectiveness_composite": 0.0,
                "margin_at_risk_count": 0,
                "pricing_intervention_count": 0,
                "avg_discount_discipline_score": 0.0,
                "avg_value_retention_score": 0.0,
                "avg_margin_protection_score": 0.0,
                "avg_negotiation_efficiency_score": 0.0,
                "total_estimated_margin_loss_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_disc = total_val = total_mar = total_eff = total_loss = 0.0

        for r in self._results:
            risk_counts[r.negotiation_risk.value]       = risk_counts.get(r.negotiation_risk.value, 0) + 1
            pattern_counts[r.negotiation_pattern.value] = pattern_counts.get(r.negotiation_pattern.value, 0) + 1
            severity_counts[r.negotiation_severity.value] = severity_counts.get(r.negotiation_severity.value, 0) + 1
            action_counts[r.recommended_action.value]     = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.negotiation_effectiveness_composite
            total_disc += r.discount_discipline_score
            total_val  += r.value_retention_score
            total_mar  += r.margin_protection_score
            total_eff  += r.negotiation_efficiency_score
            total_loss += r.estimated_margin_loss_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_negotiation_effectiveness_composite":  round(total_comp / n, 1),
            "margin_at_risk_count":                     sum(1 for r in self._results if r.is_margin_at_risk),
            "pricing_intervention_count":               sum(1 for r in self._results if r.requires_pricing_intervention),
            "avg_discount_discipline_score":            round(total_disc / n, 1),
            "avg_value_retention_score":                round(total_val / n, 1),
            "avg_margin_protection_score":              round(total_mar / n, 1),
            "avg_negotiation_efficiency_score":         round(total_eff / n, 1),
            "total_estimated_margin_loss_usd":          round(total_loss, 2),
        }
