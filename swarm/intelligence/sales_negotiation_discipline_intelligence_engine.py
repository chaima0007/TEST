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
    chronic_discounter    = "chronic_discounter"
    value_cave            = "value_cave"
    competitor_price_match = "competitor_price_match"
    single_threaded_close = "single_threaded_close"
    late_stage_collapse   = "late_stage_collapse"


class NegotiationSeverity(str, Enum):
    clean      = "clean"
    managing   = "managing"
    struggling = "struggling"
    collapsing = "collapsing"


class NegotiationAction(str, Enum):
    no_action                       = "no_action"
    negotiation_process_coaching    = "negotiation_process_coaching"
    stakeholder_expansion_coaching  = "stakeholder_expansion_coaching"
    close_technique_coaching        = "close_technique_coaching"
    discount_defense_intervention   = "discount_defense_intervention"
    value_based_negotiation_reset   = "value_based_negotiation_reset"
    negotiation_reset_intervention  = "negotiation_reset_intervention"


@dataclass
class NegotiationInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    initial_discount_offered_pct: float
    avg_total_discount_given_pct: float
    avg_selling_price_vs_list_pct: float
    price_concession_without_value_exchange_pct: float
    multi_concession_in_single_negotiation_pct: float
    final_ask_for_extras_rate_pct: float
    champion_deal_only_rate_pct: float
    procurement_escalation_rate_pct: float
    contract_redline_rounds_avg: float
    late_stage_deal_loss_rate_pct: float
    decision_deadline_driven_by_rep_pct: float
    multi_year_deal_rate_pct: float
    negotiation_rounds_before_close_avg: float
    deal_closed_at_list_price_pct: float
    competitor_discount_match_rate_pct: float
    payment_terms_extension_rate_pct: float
    legal_review_delay_days_avg: float
    total_late_stage_deals: int
    avg_opportunity_value_usd: float


@dataclass
class NegotiationResult:
    rep_id: str
    region: str
    negotiation_risk: NegotiationRisk
    negotiation_pattern: NegotiationPattern
    negotiation_severity: NegotiationSeverity
    recommended_action: NegotiationAction
    discount_discipline_score: float
    concession_behavior_score: float
    deal_construction_score: float
    close_effectiveness_score: float
    negotiation_composite: float
    has_negotiation_gap: bool
    requires_negotiation_coaching: bool
    estimated_revenue_dilution_usd: float
    negotiation_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                         self.rep_id,
            "region":                         self.region,
            "negotiation_risk":               self.negotiation_risk.value,
            "negotiation_pattern":            self.negotiation_pattern.value,
            "negotiation_severity":           self.negotiation_severity.value,
            "recommended_action":             self.recommended_action.value,
            "discount_discipline_score":      self.discount_discipline_score,
            "concession_behavior_score":      self.concession_behavior_score,
            "deal_construction_score":        self.deal_construction_score,
            "close_effectiveness_score":      self.close_effectiveness_score,
            "negotiation_composite":          self.negotiation_composite,
            "has_negotiation_gap":            self.has_negotiation_gap,
            "requires_negotiation_coaching":  self.requires_negotiation_coaching,
            "estimated_revenue_dilution_usd": self.estimated_revenue_dilution_usd,
            "negotiation_signal":             self.negotiation_signal,
        }


class SalesNegotiationDisciplineIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[NegotiationResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _discount_discipline_score(self, inp: NegotiationInput) -> float:
        score = 0.0

        if inp.initial_discount_offered_pct >= 0.25:
            score += 40.0
        elif inp.initial_discount_offered_pct >= 0.15:
            score += 22.0
        elif inp.initial_discount_offered_pct >= 0.05:
            score += 8.0

        if inp.avg_total_discount_given_pct >= 0.30:
            score += 35.0
        elif inp.avg_total_discount_given_pct >= 0.20:
            score += 18.0

        if inp.avg_selling_price_vs_list_pct <= 0.70:
            score += 25.0
        elif inp.avg_selling_price_vs_list_pct <= 0.85:
            score += 12.0

        return min(score, 100.0)

    def _concession_behavior_score(self, inp: NegotiationInput) -> float:
        score = 0.0

        if inp.price_concession_without_value_exchange_pct >= 0.60:
            score += 40.0
        elif inp.price_concession_without_value_exchange_pct >= 0.40:
            score += 22.0
        elif inp.price_concession_without_value_exchange_pct >= 0.20:
            score += 8.0

        if inp.multi_concession_in_single_negotiation_pct >= 0.50:
            score += 35.0
        elif inp.multi_concession_in_single_negotiation_pct >= 0.30:
            score += 18.0

        if inp.final_ask_for_extras_rate_pct >= 0.40:
            score += 25.0
        elif inp.final_ask_for_extras_rate_pct >= 0.20:
            score += 12.0

        return min(score, 100.0)

    def _deal_construction_score(self, inp: NegotiationInput) -> float:
        score = 0.0

        if inp.champion_deal_only_rate_pct >= 0.65:
            score += 45.0
        elif inp.champion_deal_only_rate_pct >= 0.45:
            score += 25.0
        elif inp.champion_deal_only_rate_pct >= 0.25:
            score += 10.0

        if inp.procurement_escalation_rate_pct >= 0.40:
            score += 30.0
        elif inp.procurement_escalation_rate_pct >= 0.20:
            score += 15.0

        if inp.contract_redline_rounds_avg >= 4.0:
            score += 25.0
        elif inp.contract_redline_rounds_avg >= 2.5:
            score += 12.0

        return min(score, 100.0)

    def _close_effectiveness_score(self, inp: NegotiationInput) -> float:
        score = 0.0

        if inp.late_stage_deal_loss_rate_pct >= 0.45:
            score += 40.0
        elif inp.late_stage_deal_loss_rate_pct >= 0.25:
            score += 22.0
        elif inp.late_stage_deal_loss_rate_pct >= 0.10:
            score += 8.0

        if inp.decision_deadline_driven_by_rep_pct <= 0.25:
            score += 35.0
        elif inp.decision_deadline_driven_by_rep_pct <= 0.50:
            score += 18.0

        if inp.multi_year_deal_rate_pct <= 0.10:
            score += 25.0
        elif inp.multi_year_deal_rate_pct <= 0.25:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: NegotiationInput,
                         discount: float, concession: float,
                         construction: float, close: float) -> NegotiationPattern:
        # Chronic discounter: habitually cuts price to close
        if inp.avg_total_discount_given_pct >= 0.25 and discount >= 40:
            return NegotiationPattern.chronic_discounter

        # Value cave: gives concessions without receiving anything in return
        if inp.price_concession_without_value_exchange_pct >= 0.50 and concession >= 40:
            return NegotiationPattern.value_cave

        # Competitor price match: caves to unverified competitor price claims
        if inp.competitor_discount_match_rate_pct >= 0.50 and inp.negotiation_rounds_before_close_avg >= 3.0:
            return NegotiationPattern.competitor_price_match

        # Single-threaded close: only engages one stakeholder in negotiation
        if inp.champion_deal_only_rate_pct >= 0.60 and construction >= 35:
            return NegotiationPattern.single_threaded_close

        # Late-stage collapse: loses deals that should be won at proposal stage
        if inp.late_stage_deal_loss_rate_pct >= 0.40 and close >= 30:
            return NegotiationPattern.late_stage_collapse

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
            return NegotiationSeverity.struggling
        if composite >= 20:
            return NegotiationSeverity.managing
        return NegotiationSeverity.clean

    def _action(self, risk: NegotiationRisk, pattern: NegotiationPattern) -> NegotiationAction:
        if risk == NegotiationRisk.critical:
            if pattern == NegotiationPattern.chronic_discounter:
                return NegotiationAction.discount_defense_intervention
            if pattern == NegotiationPattern.value_cave:
                return NegotiationAction.value_based_negotiation_reset
            return NegotiationAction.negotiation_reset_intervention
        if risk == NegotiationRisk.high:
            if pattern == NegotiationPattern.single_threaded_close:
                return NegotiationAction.stakeholder_expansion_coaching
            if pattern == NegotiationPattern.late_stage_collapse:
                return NegotiationAction.close_technique_coaching
            return NegotiationAction.negotiation_process_coaching
        if risk == NegotiationRisk.moderate:
            return NegotiationAction.negotiation_process_coaching
        return NegotiationAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_negotiation_gap(self, composite: float, inp: NegotiationInput) -> bool:
        return (
            composite >= 40
            or inp.avg_total_discount_given_pct >= 0.20
            or inp.late_stage_deal_loss_rate_pct >= 0.30
        )

    def _requires_negotiation_coaching(self, composite: float, inp: NegotiationInput) -> bool:
        return (
            composite >= 30
            or inp.price_concession_without_value_exchange_pct >= 0.40
            or inp.multi_concession_in_single_negotiation_pct >= 0.40
        )

    # ------------------------------------------------------------------
    # Revenue dilution estimate
    # ------------------------------------------------------------------

    def _estimated_revenue_dilution(self, inp: NegotiationInput, composite: float) -> float:
        return round(
            inp.total_late_stage_deals
            * inp.avg_opportunity_value_usd
            * inp.avg_total_discount_given_pct
            * (composite / 100.0),
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: NegotiationInput,
                pattern: NegotiationPattern, composite: float) -> str:
        if pattern == NegotiationPattern.none and composite < 20:
            return "Negotiation discipline strong — discount defense, concession sequencing, and deal construction within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.avg_total_discount_given_pct * 100:.0f}% avg discount given")
        parts.append(f"{inp.price_concession_without_value_exchange_pct * 100:.0f}% concessions without value exchange")
        parts.append(f"{inp.deal_closed_at_list_price_pct * 100:.0f}% closed at list price")
        label = pattern.value.replace("_", " ") if pattern != NegotiationPattern.none else "Negotiation risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: NegotiationInput) -> NegotiationResult:
        discount     = round(self._discount_discipline_score(inp), 1)
        concession   = round(self._concession_behavior_score(inp), 1)
        construction = round(self._deal_construction_score(inp), 1)
        close        = round(self._close_effectiveness_score(inp), 1)

        composite = round(
            discount * 0.30 + concession * 0.30 + construction * 0.25 + close * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, discount, concession, construction, close)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_negotiation_gap(composite, inp)
        coach  = self._requires_negotiation_coaching(composite, inp)
        loss   = self._estimated_revenue_dilution(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = NegotiationResult(
            rep_id=inp.rep_id,
            region=inp.region,
            negotiation_risk=risk,
            negotiation_pattern=pattern,
            negotiation_severity=severity,
            recommended_action=action,
            discount_discipline_score=discount,
            concession_behavior_score=concession,
            deal_construction_score=construction,
            close_effectiveness_score=close,
            negotiation_composite=composite,
            has_negotiation_gap=gap,
            requires_negotiation_coaching=coach,
            estimated_revenue_dilution_usd=loss,
            negotiation_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[NegotiationInput]) -> list[NegotiationResult]:
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
                "negotiation_gap_count": 0,
                "coaching_count": 0,
                "avg_discount_discipline_score": 0.0,
                "avg_concession_behavior_score": 0.0,
                "avg_deal_construction_score": 0.0,
                "avg_close_effectiveness_score": 0.0,
                "total_estimated_revenue_dilution_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_dis = total_con = total_con2 = total_clo = total_loss = 0.0

        for r in self._results:
            risk_counts[r.negotiation_risk.value]         = risk_counts.get(r.negotiation_risk.value, 0) + 1
            pattern_counts[r.negotiation_pattern.value]   = pattern_counts.get(r.negotiation_pattern.value, 0) + 1
            severity_counts[r.negotiation_severity.value] = severity_counts.get(r.negotiation_severity.value, 0) + 1
            action_counts[r.recommended_action.value]     = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.negotiation_composite
            total_dis  += r.discount_discipline_score
            total_con  += r.concession_behavior_score
            total_con2 += r.deal_construction_score
            total_clo  += r.close_effectiveness_score
            total_loss += r.estimated_revenue_dilution_usd

        n = len(self._results)

        return {
            "total":                                  n,
            "risk_counts":                            risk_counts,
            "pattern_counts":                         pattern_counts,
            "severity_counts":                        severity_counts,
            "action_counts":                          action_counts,
            "avg_negotiation_composite":              round(total_comp / n, 1),
            "negotiation_gap_count":                  sum(1 for r in self._results if r.has_negotiation_gap),
            "coaching_count":                         sum(1 for r in self._results if r.requires_negotiation_coaching),
            "avg_discount_discipline_score":          round(total_dis / n, 1),
            "avg_concession_behavior_score":          round(total_con / n, 1),
            "avg_deal_construction_score":            round(total_con2 / n, 1),
            "avg_close_effectiveness_score":          round(total_clo / n, 1),
            "total_estimated_revenue_dilution_usd":   round(total_loss, 2),
        }
