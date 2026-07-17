from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class LeverageRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class LeveragePattern(str, Enum):
    none                           = "none"
    deadline_blind_negotiator      = "deadline_blind_negotiator"
    single_lever_dependency        = "single_lever_dependency"
    urgency_manufacturing_failure  = "urgency_manufacturing_failure"
    competitive_leverage_avoidance = "competitive_leverage_avoidance"
    concession_without_ask         = "concession_without_ask"


class LeverageSeverity(str, Enum):
    commanding = "commanding"
    balanced   = "balanced"
    reactive   = "reactive"
    powerless  = "powerless"


class LeverageAction(str, Enum):
    no_action                       = "no_action"
    leverage_awareness_coaching     = "leverage_awareness_coaching"
    deadline_framing_coaching       = "deadline_framing_coaching"
    competitive_leverage_coaching   = "competitive_leverage_coaching"
    concession_discipline_coaching  = "concession_discipline_coaching"
    negotiation_strategy_overhaul   = "negotiation_strategy_overhaul"


@dataclass
class LeverageInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    deals_with_competitive_pressure_used_pct: float
    urgency_event_cited_in_negotiation_pct: float
    deadline_anchored_close_rate_pct: float
    concession_without_counter_ask_pct: float
    value_anchor_set_before_price_pct: float
    executive_sponsor_engaged_in_negotiation_pct: float
    walk_away_threat_used_pct: float
    walk_away_actually_executed_pct: float
    multi_option_pricing_presented_pct: float
    deal_restructured_to_preserve_margin_pct: float
    procurement_engaged_early_pct: float
    legal_used_as_delay_tactic_pct: float
    negotiation_extended_beyond_target_days: float
    last_minute_concession_rate_pct: float
    price_reduction_without_scope_change_pct: float
    batch_deal_packaging_rate_pct: float
    renewal_leverage_used_pct: float
    total_deals_negotiated: int
    avg_opportunity_value_usd: float


@dataclass
class LeverageResult:
    rep_id: str
    region: str
    leverage_risk: LeverageRisk
    leverage_pattern: LeveragePattern
    leverage_severity: LeverageSeverity
    recommended_action: LeverageAction
    tactical_score: float
    urgency_score: float
    discipline_score: float
    positioning_score: float
    leverage_composite: float
    has_leverage_gap: bool
    requires_leverage_coaching: bool
    estimated_margin_conceded_usd: float
    leverage_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "leverage_risk":                self.leverage_risk.value,
            "leverage_pattern":             self.leverage_pattern.value,
            "leverage_severity":            self.leverage_severity.value,
            "recommended_action":           self.recommended_action.value,
            "tactical_score":               self.tactical_score,
            "urgency_score":                self.urgency_score,
            "discipline_score":             self.discipline_score,
            "positioning_score":            self.positioning_score,
            "leverage_composite":           self.leverage_composite,
            "has_leverage_gap":             self.has_leverage_gap,
            "requires_leverage_coaching":   self.requires_leverage_coaching,
            "estimated_margin_conceded_usd":self.estimated_margin_conceded_usd,
            "leverage_signal":              self.leverage_signal,
        }


class SalesNegotiationLeverageIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[LeverageResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _tactical_score(self, inp: LeverageInput) -> float:
        score = 0.0

        if inp.deals_with_competitive_pressure_used_pct <= 0.20:
            score += 40.0
        elif inp.deals_with_competitive_pressure_used_pct <= 0.40:
            score += 22.0
        elif inp.deals_with_competitive_pressure_used_pct <= 0.60:
            score += 8.0

        if inp.walk_away_threat_used_pct <= 0.10:
            score += 35.0
        elif inp.walk_away_threat_used_pct <= 0.25:
            score += 18.0

        if inp.multi_option_pricing_presented_pct <= 0.20:
            score += 25.0
        elif inp.multi_option_pricing_presented_pct <= 0.45:
            score += 12.0

        return min(score, 100.0)

    def _urgency_score(self, inp: LeverageInput) -> float:
        score = 0.0

        if inp.urgency_event_cited_in_negotiation_pct <= 0.20:
            score += 40.0
        elif inp.urgency_event_cited_in_negotiation_pct <= 0.40:
            score += 22.0
        elif inp.urgency_event_cited_in_negotiation_pct <= 0.60:
            score += 8.0

        if inp.deadline_anchored_close_rate_pct <= 0.25:
            score += 35.0
        elif inp.deadline_anchored_close_rate_pct <= 0.50:
            score += 18.0

        if inp.negotiation_extended_beyond_target_days >= 21.0:
            score += 25.0
        elif inp.negotiation_extended_beyond_target_days >= 10.0:
            score += 12.0

        return min(score, 100.0)

    def _discipline_score(self, inp: LeverageInput) -> float:
        score = 0.0

        if inp.concession_without_counter_ask_pct >= 0.60:
            score += 40.0
        elif inp.concession_without_counter_ask_pct >= 0.40:
            score += 22.0
        elif inp.concession_without_counter_ask_pct >= 0.20:
            score += 8.0

        if inp.price_reduction_without_scope_change_pct >= 0.50:
            score += 35.0
        elif inp.price_reduction_without_scope_change_pct >= 0.30:
            score += 18.0

        if inp.last_minute_concession_rate_pct >= 0.45:
            score += 25.0
        elif inp.last_minute_concession_rate_pct >= 0.25:
            score += 12.0

        return min(score, 100.0)

    def _positioning_score(self, inp: LeverageInput) -> float:
        score = 0.0

        if inp.value_anchor_set_before_price_pct <= 0.30:
            score += 45.0
        elif inp.value_anchor_set_before_price_pct <= 0.55:
            score += 25.0
        elif inp.value_anchor_set_before_price_pct <= 0.75:
            score += 10.0

        if inp.executive_sponsor_engaged_in_negotiation_pct <= 0.20:
            score += 30.0
        elif inp.executive_sponsor_engaged_in_negotiation_pct <= 0.40:
            score += 15.0

        if inp.deal_restructured_to_preserve_margin_pct <= 0.15:
            score += 25.0
        elif inp.deal_restructured_to_preserve_margin_pct <= 0.35:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: LeverageInput,
                          tactical: float, urgency: float,
                          discipline: float, positioning: float) -> LeveragePattern:
        # Concession without ask: giving things away without extracting anything
        if inp.concession_without_counter_ask_pct >= 0.55 and inp.price_reduction_without_scope_change_pct >= 0.40:
            return LeveragePattern.concession_without_ask

        # Competitive leverage avoidance: not using competitors as pressure
        if tactical >= 40 and inp.deals_with_competitive_pressure_used_pct <= 0.25:
            return LeveragePattern.competitive_leverage_avoidance

        # Deadline blind negotiator: no urgency framing, deals drag on
        if urgency >= 40 and inp.negotiation_extended_beyond_target_days >= 14.0:
            return LeveragePattern.deadline_blind_negotiator

        # Urgency manufacturing failure: can't create urgency events
        if inp.urgency_event_cited_in_negotiation_pct <= 0.15 and discipline >= 30:
            return LeveragePattern.urgency_manufacturing_failure

        # Single lever dependency: relies only on price as lever
        if positioning >= 30 and inp.value_anchor_set_before_price_pct <= 0.25:
            return LeveragePattern.single_lever_dependency

        return LeveragePattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> LeverageRisk:
        if composite >= 60:
            return LeverageRisk.critical
        if composite >= 40:
            return LeverageRisk.high
        if composite >= 20:
            return LeverageRisk.moderate
        return LeverageRisk.low

    def _severity(self, composite: float) -> LeverageSeverity:
        if composite >= 60:
            return LeverageSeverity.powerless
        if composite >= 40:
            return LeverageSeverity.reactive
        if composite >= 20:
            return LeverageSeverity.balanced
        return LeverageSeverity.commanding

    def _action(self, risk: LeverageRisk, pattern: LeveragePattern) -> LeverageAction:
        if risk == LeverageRisk.critical:
            if pattern == LeveragePattern.concession_without_ask:
                return LeverageAction.concession_discipline_coaching
            if pattern == LeveragePattern.competitive_leverage_avoidance:
                return LeverageAction.competitive_leverage_coaching
            return LeverageAction.negotiation_strategy_overhaul
        if risk == LeverageRisk.high:
            if pattern == LeveragePattern.deadline_blind_negotiator:
                return LeverageAction.deadline_framing_coaching
            if pattern == LeveragePattern.urgency_manufacturing_failure:
                return LeverageAction.deadline_framing_coaching
            return LeverageAction.leverage_awareness_coaching
        if risk == LeverageRisk.moderate:
            return LeverageAction.leverage_awareness_coaching
        return LeverageAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_leverage_gap(self, composite: float, inp: LeverageInput) -> bool:
        return (
            composite >= 40
            or inp.concession_without_counter_ask_pct >= 0.45
            or inp.value_anchor_set_before_price_pct <= 0.35
        )

    def _requires_leverage_coaching(self, composite: float, inp: LeverageInput) -> bool:
        return (
            composite >= 30
            or inp.deals_with_competitive_pressure_used_pct <= 0.30
            or inp.price_reduction_without_scope_change_pct >= 0.25
        )

    # ------------------------------------------------------------------
    # Margin conceded estimate
    # ------------------------------------------------------------------

    def _estimated_margin_conceded(self, inp: LeverageInput, composite: float) -> float:
        return round(
            inp.total_deals_negotiated
            * inp.avg_opportunity_value_usd
            * inp.price_reduction_without_scope_change_pct
            * (composite / 100.0),
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: LeverageInput,
                 pattern: LeveragePattern, composite: float) -> str:
        if pattern == LeveragePattern.none and composite < 20:
            return "Negotiation leverage healthy — tactical use, urgency framing, and concession discipline within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.concession_without_counter_ask_pct * 100:.0f}% concessions without counter-ask")
        parts.append(f"{inp.deals_with_competitive_pressure_used_pct * 100:.0f}% competitive pressure used")
        parts.append(f"{inp.value_anchor_set_before_price_pct * 100:.0f}% value-anchored before price")
        label = pattern.value.replace("_", " ") if pattern != LeveragePattern.none else "Leverage risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: LeverageInput) -> LeverageResult:
        tactical    = round(self._tactical_score(inp), 1)
        urgency     = round(self._urgency_score(inp), 1)
        discipline  = round(self._discipline_score(inp), 1)
        positioning = round(self._positioning_score(inp), 1)

        composite = round(
            tactical * 0.30 + urgency * 0.25 + discipline * 0.25 + positioning * 0.20, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, tactical, urgency, discipline, positioning)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_leverage_gap(composite, inp)
        coach  = self._requires_leverage_coaching(composite, inp)
        loss   = self._estimated_margin_conceded(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = LeverageResult(
            rep_id=inp.rep_id,
            region=inp.region,
            leverage_risk=risk,
            leverage_pattern=pattern,
            leverage_severity=severity,
            recommended_action=action,
            tactical_score=tactical,
            urgency_score=urgency,
            discipline_score=discipline,
            positioning_score=positioning,
            leverage_composite=composite,
            has_leverage_gap=gap,
            requires_leverage_coaching=coach,
            estimated_margin_conceded_usd=loss,
            leverage_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[LeverageInput]) -> list[LeverageResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_leverage_composite": 0.0,
                "leverage_gap_count": 0,
                "coaching_count": 0,
                "avg_tactical_score": 0.0,
                "avg_urgency_score": 0.0,
                "avg_discipline_score": 0.0,
                "avg_positioning_score": 0.0,
                "total_estimated_margin_conceded_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_tac = total_urg = total_dis = total_pos = total_loss = 0.0

        for r in self._results:
            risk_counts[r.leverage_risk.value]         = risk_counts.get(r.leverage_risk.value, 0) + 1
            pattern_counts[r.leverage_pattern.value]   = pattern_counts.get(r.leverage_pattern.value, 0) + 1
            severity_counts[r.leverage_severity.value] = severity_counts.get(r.leverage_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.leverage_composite
            total_tac  += r.tactical_score
            total_urg  += r.urgency_score
            total_dis  += r.discipline_score
            total_pos  += r.positioning_score
            total_loss += r.estimated_margin_conceded_usd

        n = len(self._results)

        return {
            "total":                                     n,
            "risk_counts":                               risk_counts,
            "pattern_counts":                            pattern_counts,
            "severity_counts":                           severity_counts,
            "action_counts":                             action_counts,
            "avg_leverage_composite":                    round(total_comp / n, 1),
            "leverage_gap_count":                        sum(1 for r in self._results if r.has_leverage_gap),
            "coaching_count":                            sum(1 for r in self._results if r.requires_leverage_coaching),
            "avg_tactical_score":                        round(total_tac / n, 1),
            "avg_urgency_score":                         round(total_urg / n, 1),
            "avg_discipline_score":                      round(total_dis / n, 1),
            "avg_positioning_score":                     round(total_pos / n, 1),
            "total_estimated_margin_conceded_usd":       round(total_loss, 2),
        }
