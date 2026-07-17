from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class NegotiationRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class NegotiationPattern(str, Enum):
    none                          = "none"
    early_capitulation            = "early_capitulation"
    manager_escalation_dependency = "manager_escalation_dependency"
    price_anchoring_failure       = "price_anchoring_failure"
    concession_cascade            = "concession_cascade"
    urgency_creation_gap          = "urgency_creation_gap"


class NegotiationSeverity(str, Enum):
    disciplined = "disciplined"
    developing  = "developing"
    reactive    = "reactive"
    erosive     = "erosive"


class NegotiationAction(str, Enum):
    no_action                     = "no_action"
    negotiation_skills_coaching   = "negotiation_skills_coaching"
    value_anchoring_training      = "value_anchoring_training"
    concession_management_review  = "concession_management_review"
    manager_escalation_reduction  = "manager_escalation_reduction"
    urgency_creation_training     = "urgency_creation_training"


@dataclass
class NegotiationInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_negotiations_conducted: int
    avg_negotiation_rounds_per_deal: float
    first_concession_timing_pct: float
    avg_discount_concession_pct: float
    deals_won_without_discount_pct: float
    manager_escalation_in_negotiation_pct: float
    value_vs_price_conversation_ratio: float
    avg_days_from_proposal_to_close: float
    deals_with_no_negotiation_pct: float
    multi_item_negotiation_rate_pct: float
    urgency_trigger_used_pct: float
    competitive_counteroffer_handled_pct: float
    contract_term_concession_pct: float
    payment_term_concession_pct: float
    scope_expansion_during_negotiation_pct: float
    negotiation_stall_rate_pct: float
    deal_desk_referral_in_negotiation_pct: float
    avg_final_margin_vs_list_pct: float
    avg_opportunity_value_usd: float


@dataclass
class NegotiationResult:
    rep_id: str
    region: str
    negotiation_risk: NegotiationRisk
    negotiation_pattern: NegotiationPattern
    negotiation_severity: NegotiationSeverity
    recommended_action: NegotiationAction
    concession_discipline_score: float
    negotiation_process_score: float
    negotiation_urgency_score: float
    value_articulation_score: float
    negotiation_composite: float
    has_negotiation_gap: bool
    requires_negotiation_coaching: bool
    estimated_margin_erosion_usd: float
    negotiation_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "negotiation_risk":                 self.negotiation_risk.value,
            "negotiation_pattern":              self.negotiation_pattern.value,
            "negotiation_severity":             self.negotiation_severity.value,
            "recommended_action":               self.recommended_action.value,
            "concession_discipline_score":      self.concession_discipline_score,
            "negotiation_process_score":        self.negotiation_process_score,
            "negotiation_urgency_score":        self.negotiation_urgency_score,
            "value_articulation_score":         self.value_articulation_score,
            "negotiation_composite":            self.negotiation_composite,
            "has_negotiation_gap":              self.has_negotiation_gap,
            "requires_negotiation_coaching":    self.requires_negotiation_coaching,
            "estimated_margin_erosion_usd":     self.estimated_margin_erosion_usd,
            "negotiation_signal":               self.negotiation_signal,
        }


class SalesNegotiationIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[NegotiationResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _concession_discipline_score(self, inp: NegotiationInput) -> float:
        score = 0.0

        if inp.first_concession_timing_pct >= 0.80:
            score += 40.0
        elif inp.first_concession_timing_pct >= 0.55:
            score += 22.0
        elif inp.first_concession_timing_pct >= 0.35:
            score += 8.0

        if inp.avg_discount_concession_pct >= 0.20:
            score += 35.0
        elif inp.avg_discount_concession_pct >= 0.10:
            score += 18.0

        if inp.deals_won_without_discount_pct <= 0.10:
            score += 25.0
        elif inp.deals_won_without_discount_pct <= 0.30:
            score += 12.0

        return min(score, 100.0)

    def _negotiation_process_score(self, inp: NegotiationInput) -> float:
        score = 0.0

        if inp.manager_escalation_in_negotiation_pct >= 0.60:
            score += 40.0
        elif inp.manager_escalation_in_negotiation_pct >= 0.35:
            score += 22.0
        elif inp.manager_escalation_in_negotiation_pct >= 0.15:
            score += 8.0

        if inp.multi_item_negotiation_rate_pct <= 0.15:
            score += 35.0
        elif inp.multi_item_negotiation_rate_pct <= 0.35:
            score += 18.0

        if inp.deal_desk_referral_in_negotiation_pct >= 0.40:
            score += 25.0
        elif inp.deal_desk_referral_in_negotiation_pct >= 0.20:
            score += 12.0

        return min(score, 100.0)

    def _negotiation_urgency_score(self, inp: NegotiationInput) -> float:
        score = 0.0

        if inp.urgency_trigger_used_pct <= 0.10:
            score += 40.0
        elif inp.urgency_trigger_used_pct <= 0.30:
            score += 22.0
        elif inp.urgency_trigger_used_pct <= 0.50:
            score += 8.0

        if inp.negotiation_stall_rate_pct >= 0.40:
            score += 35.0
        elif inp.negotiation_stall_rate_pct >= 0.20:
            score += 18.0

        if inp.competitive_counteroffer_handled_pct <= 0.20:
            score += 25.0
        elif inp.competitive_counteroffer_handled_pct <= 0.50:
            score += 12.0

        return min(score, 100.0)

    def _value_articulation_score(self, inp: NegotiationInput) -> float:
        score = 0.0

        if inp.value_vs_price_conversation_ratio <= 0.20:
            score += 45.0
        elif inp.value_vs_price_conversation_ratio <= 0.40:
            score += 25.0
        elif inp.value_vs_price_conversation_ratio <= 0.60:
            score += 10.0

        if inp.scope_expansion_during_negotiation_pct <= 0.10:
            score += 30.0
        elif inp.scope_expansion_during_negotiation_pct <= 0.30:
            score += 15.0

        if inp.deals_with_no_negotiation_pct >= 0.40:
            score += 25.0
        elif inp.deals_with_no_negotiation_pct >= 0.20:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: NegotiationInput,
                          concession: float, process: float,
                          urgency: float, value: float) -> NegotiationPattern:
        if concession >= 40 and inp.first_concession_timing_pct >= 0.70:
            return NegotiationPattern.early_capitulation

        if process >= 40 and inp.manager_escalation_in_negotiation_pct >= 0.50:
            return NegotiationPattern.manager_escalation_dependency

        if value >= 30 and inp.value_vs_price_conversation_ratio <= 0.30:
            return NegotiationPattern.price_anchoring_failure

        if concession >= 30 and inp.avg_negotiation_rounds_per_deal >= 3.0:
            return NegotiationPattern.concession_cascade

        if urgency >= 30 and inp.urgency_trigger_used_pct <= 0.20:
            return NegotiationPattern.urgency_creation_gap

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
            return NegotiationSeverity.erosive
        if composite >= 40:
            return NegotiationSeverity.reactive
        if composite >= 20:
            return NegotiationSeverity.developing
        return NegotiationSeverity.disciplined

    def _action(self, risk: NegotiationRisk,
                 pattern: NegotiationPattern) -> NegotiationAction:
        if risk == NegotiationRisk.critical:
            if pattern == NegotiationPattern.manager_escalation_dependency:
                return NegotiationAction.manager_escalation_reduction
            if pattern == NegotiationPattern.price_anchoring_failure:
                return NegotiationAction.value_anchoring_training
            return NegotiationAction.concession_management_review
        if risk == NegotiationRisk.high:
            if pattern == NegotiationPattern.urgency_creation_gap:
                return NegotiationAction.urgency_creation_training
            if pattern == NegotiationPattern.concession_cascade:
                return NegotiationAction.concession_management_review
            return NegotiationAction.negotiation_skills_coaching
        if risk == NegotiationRisk.moderate:
            return NegotiationAction.negotiation_skills_coaching
        return NegotiationAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_negotiation_gap(self, composite: float, inp: NegotiationInput) -> bool:
        return (
            composite >= 40
            or inp.avg_discount_concession_pct >= 0.20
            or inp.manager_escalation_in_negotiation_pct >= 0.50
        )

    def _requires_negotiation_coaching(self, composite: float, inp: NegotiationInput) -> bool:
        return (
            composite >= 30
            or inp.first_concession_timing_pct >= 0.60
            or inp.deals_won_without_discount_pct <= 0.15
        )

    # ------------------------------------------------------------------
    # Margin erosion estimate
    # ------------------------------------------------------------------

    def _estimated_margin_erosion(self, inp: NegotiationInput, composite: float) -> float:
        total_revenue_base = inp.total_negotiations_conducted * inp.avg_opportunity_value_usd
        return round(total_revenue_base * inp.avg_discount_concession_pct * (composite / 100.0) * 0.50, 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: NegotiationInput,
                 pattern: NegotiationPattern, composite: float) -> str:
        if pattern == NegotiationPattern.none and composite < 20:
            return "Negotiation discipline healthy — concession management, value anchoring, and urgency creation within benchmarks"
        parts: list[str] = []
        if inp.first_concession_timing_pct < 1.0:
            parts.append(f"{inp.first_concession_timing_pct*100:.0f}% give first concession immediately")
        if inp.deals_won_without_discount_pct < 1.0:
            parts.append(f"{inp.deals_won_without_discount_pct*100:.0f}% deals won without discount")
        parts.append(f"{inp.avg_negotiation_rounds_per_deal:.1f} avg rounds")
        label = pattern.value.replace("_", " ") if pattern != NegotiationPattern.none else "Negotiation risk"
        summary = " — ".join(parts) if parts else "negotiation discipline gap"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: NegotiationInput) -> NegotiationResult:
        concession = round(self._concession_discipline_score(inp), 1)
        process    = round(self._negotiation_process_score(inp), 1)
        urgency    = round(self._negotiation_urgency_score(inp), 1)
        value      = round(self._value_articulation_score(inp), 1)

        composite = round(
            concession * 0.35 + process * 0.30 + urgency * 0.20 + value * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, concession, process, urgency, value)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_negotiation_gap(composite, inp)
        coach  = self._requires_negotiation_coaching(composite, inp)
        erosion = self._estimated_margin_erosion(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = NegotiationResult(
            rep_id=inp.rep_id,
            region=inp.region,
            negotiation_risk=risk,
            negotiation_pattern=pattern,
            negotiation_severity=severity,
            recommended_action=action,
            concession_discipline_score=concession,
            negotiation_process_score=process,
            negotiation_urgency_score=urgency,
            value_articulation_score=value,
            negotiation_composite=composite,
            has_negotiation_gap=gap,
            requires_negotiation_coaching=coach,
            estimated_margin_erosion_usd=erosion,
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
                "avg_concession_discipline_score": 0.0,
                "avg_negotiation_process_score": 0.0,
                "avg_negotiation_urgency_score": 0.0,
                "avg_value_articulation_score": 0.0,
                "total_estimated_margin_erosion_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_con = total_pro = total_urg = total_val = total_erosion = 0.0

        for r in self._results:
            risk_counts[r.negotiation_risk.value]       = risk_counts.get(r.negotiation_risk.value, 0) + 1
            pattern_counts[r.negotiation_pattern.value] = pattern_counts.get(r.negotiation_pattern.value, 0) + 1
            severity_counts[r.negotiation_severity.value] = severity_counts.get(r.negotiation_severity.value, 0) + 1
            action_counts[r.recommended_action.value]   = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp    += r.negotiation_composite
            total_con     += r.concession_discipline_score
            total_pro     += r.negotiation_process_score
            total_urg     += r.negotiation_urgency_score
            total_val     += r.value_articulation_score
            total_erosion += r.estimated_margin_erosion_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_negotiation_composite":                round(total_comp / n, 1),
            "negotiation_gap_count":                    sum(1 for r in self._results if r.has_negotiation_gap),
            "coaching_count":                           sum(1 for r in self._results if r.requires_negotiation_coaching),
            "avg_concession_discipline_score":          round(total_con / n, 1),
            "avg_negotiation_process_score":            round(total_pro / n, 1),
            "avg_negotiation_urgency_score":            round(total_urg / n, 1),
            "avg_value_articulation_score":             round(total_val / n, 1),
            "total_estimated_margin_erosion_usd":       round(total_erosion, 2),
        }
