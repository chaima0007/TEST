from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class DealDeskRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class DealDeskPattern(str, Enum):
    none                        = "none"
    deal_desk_dependent         = "deal_desk_dependent"
    discount_authority_abuse    = "discount_authority_abuse"
    last_minute_escalation      = "last_minute_escalation"
    legal_escalation_pattern    = "legal_escalation_pattern"
    competitive_capitulation    = "competitive_capitulation"


class DealDeskSeverity(str, Enum):
    autonomous  = "autonomous"
    developing  = "developing"
    dependent   = "dependent"
    entrenched  = "entrenched"


class DealDeskAction(str, Enum):
    no_action                   = "no_action"
    pricing_authority_coaching  = "pricing_authority_coaching"
    deal_desk_training          = "deal_desk_training"
    discount_discipline_review  = "discount_discipline_review"
    legal_escalation_reduction  = "legal_escalation_reduction"
    deal_desk_intervention      = "deal_desk_intervention"


@dataclass
class DealDeskInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_deals_closed: int
    deals_requiring_approval_pct: float
    avg_discount_override_depth_pct: float
    custom_terms_request_count: int
    legal_review_escalation_count: int
    executive_sponsor_required_count: int
    avg_days_in_deal_desk_review: float
    deal_desk_rejection_rate_pct: float
    standard_terms_win_rate_pct: float
    custom_terms_win_rate_pct: float
    avg_deal_desk_cycles_per_deal: float
    exceptions_by_competitor_loss_count: int
    late_stage_escalation_rate_pct: float
    pricing_authority_exceeded_count: int
    multi_product_bundle_exception_count: int
    customer_success_concession_count: int
    avg_exception_value_usd: float
    deal_desk_approval_rate_pct: float
    avg_opportunity_value_usd: float


@dataclass
class DealDeskResult:
    rep_id: str
    region: str
    deal_desk_risk: DealDeskRisk
    deal_desk_pattern: DealDeskPattern
    deal_desk_severity: DealDeskSeverity
    recommended_action: DealDeskAction
    approval_dependency_score: float
    exception_complexity_score: float
    exception_urgency_score: float
    exception_impact_score: float
    deal_desk_composite: float
    has_deal_desk_gap: bool
    requires_deal_desk_coaching: bool
    estimated_margin_risk_usd: float
    deal_desk_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "deal_desk_risk":                   self.deal_desk_risk.value,
            "deal_desk_pattern":                self.deal_desk_pattern.value,
            "deal_desk_severity":               self.deal_desk_severity.value,
            "recommended_action":               self.recommended_action.value,
            "approval_dependency_score":        self.approval_dependency_score,
            "exception_complexity_score":       self.exception_complexity_score,
            "exception_urgency_score":          self.exception_urgency_score,
            "exception_impact_score":           self.exception_impact_score,
            "deal_desk_composite":              self.deal_desk_composite,
            "has_deal_desk_gap":                self.has_deal_desk_gap,
            "requires_deal_desk_coaching":      self.requires_deal_desk_coaching,
            "estimated_margin_risk_usd":        self.estimated_margin_risk_usd,
            "deal_desk_signal":                 self.deal_desk_signal,
        }


class SalesDealDeskIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[DealDeskResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _approval_dependency_score(self, inp: DealDeskInput) -> float:
        score = 0.0

        if inp.deals_requiring_approval_pct >= 0.60:
            score += 45.0
        elif inp.deals_requiring_approval_pct >= 0.40:
            score += 25.0
        elif inp.deals_requiring_approval_pct >= 0.20:
            score += 10.0

        if inp.avg_discount_override_depth_pct >= 0.15:
            score += 30.0
        elif inp.avg_discount_override_depth_pct >= 0.08:
            score += 15.0

        if inp.pricing_authority_exceeded_count >= 5:
            score += 25.0
        elif inp.pricing_authority_exceeded_count >= 2:
            score += 12.0

        return min(score, 100.0)

    def _exception_complexity_score(self, inp: DealDeskInput) -> float:
        score = 0.0

        if inp.legal_review_escalation_count >= 5:
            score += 40.0
        elif inp.legal_review_escalation_count >= 3:
            score += 22.0
        elif inp.legal_review_escalation_count >= 1:
            score += 8.0

        if inp.avg_deal_desk_cycles_per_deal >= 3.0:
            score += 35.0
        elif inp.avg_deal_desk_cycles_per_deal >= 2.0:
            score += 18.0

        if inp.executive_sponsor_required_count >= 4:
            score += 25.0
        elif inp.executive_sponsor_required_count >= 2:
            score += 12.0

        return min(score, 100.0)

    def _exception_urgency_score(self, inp: DealDeskInput) -> float:
        score = 0.0

        if inp.late_stage_escalation_rate_pct >= 0.60:
            score += 40.0
        elif inp.late_stage_escalation_rate_pct >= 0.40:
            score += 22.0
        elif inp.late_stage_escalation_rate_pct >= 0.20:
            score += 8.0

        if inp.deal_desk_rejection_rate_pct >= 0.30:
            score += 35.0
        elif inp.deal_desk_rejection_rate_pct >= 0.15:
            score += 18.0

        if inp.exceptions_by_competitor_loss_count >= 4:
            score += 25.0
        elif inp.exceptions_by_competitor_loss_count >= 2:
            score += 12.0

        return min(score, 100.0)

    def _exception_impact_score(self, inp: DealDeskInput) -> float:
        score = 0.0

        if inp.avg_exception_value_usd >= 20000.0:
            score += 45.0
        elif inp.avg_exception_value_usd >= 10000.0:
            score += 25.0
        elif inp.avg_exception_value_usd >= 5000.0:
            score += 10.0

        if inp.customer_success_concession_count >= 5:
            score += 30.0
        elif inp.customer_success_concession_count >= 2:
            score += 15.0

        if inp.multi_product_bundle_exception_count >= 4:
            score += 25.0
        elif inp.multi_product_bundle_exception_count >= 2:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: DealDeskInput,
                          approval: float, complexity: float,
                          urgency: float, impact: float) -> DealDeskPattern:
        if approval >= 40 and inp.deals_requiring_approval_pct >= 0.50:
            return DealDeskPattern.deal_desk_dependent

        if approval >= 30 and inp.avg_discount_override_depth_pct >= 0.10:
            return DealDeskPattern.discount_authority_abuse

        if urgency >= 30 and inp.late_stage_escalation_rate_pct >= 0.45:
            return DealDeskPattern.last_minute_escalation

        if complexity >= 30 and inp.legal_review_escalation_count >= 4:
            return DealDeskPattern.legal_escalation_pattern

        if urgency >= 20 and inp.exceptions_by_competitor_loss_count >= 3:
            return DealDeskPattern.competitive_capitulation

        return DealDeskPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> DealDeskRisk:
        if composite >= 60:
            return DealDeskRisk.critical
        if composite >= 40:
            return DealDeskRisk.high
        if composite >= 20:
            return DealDeskRisk.moderate
        return DealDeskRisk.low

    def _severity(self, composite: float) -> DealDeskSeverity:
        if composite >= 60:
            return DealDeskSeverity.entrenched
        if composite >= 40:
            return DealDeskSeverity.dependent
        if composite >= 20:
            return DealDeskSeverity.developing
        return DealDeskSeverity.autonomous

    def _action(self, risk: DealDeskRisk,
                 pattern: DealDeskPattern) -> DealDeskAction:
        if risk == DealDeskRisk.critical:
            if pattern == DealDeskPattern.discount_authority_abuse:
                return DealDeskAction.discount_discipline_review
            if pattern == DealDeskPattern.legal_escalation_pattern:
                return DealDeskAction.legal_escalation_reduction
            return DealDeskAction.deal_desk_intervention
        if risk == DealDeskRisk.high:
            if pattern == DealDeskPattern.last_minute_escalation:
                return DealDeskAction.deal_desk_training
            if pattern == DealDeskPattern.competitive_capitulation:
                return DealDeskAction.pricing_authority_coaching
            return DealDeskAction.deal_desk_training
        if risk == DealDeskRisk.moderate:
            return DealDeskAction.pricing_authority_coaching
        return DealDeskAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_deal_desk_gap(self, composite: float,
                            inp: DealDeskInput) -> bool:
        return (
            composite >= 40
            or inp.deals_requiring_approval_pct >= 0.50
            or inp.late_stage_escalation_rate_pct >= 0.50
        )

    def _requires_deal_desk_coaching(self, composite: float,
                                      inp: DealDeskInput) -> bool:
        return (
            composite >= 30
            or inp.pricing_authority_exceeded_count >= 3
            or inp.avg_discount_override_depth_pct >= 0.10
        )

    # ------------------------------------------------------------------
    # Margin risk estimate
    # ------------------------------------------------------------------

    def _estimated_margin_risk(self, inp: DealDeskInput,
                                composite: float) -> float:
        exception_deals = round(inp.total_deals_closed * inp.deals_requiring_approval_pct)
        return round(exception_deals * inp.avg_exception_value_usd * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: DealDeskInput,
                 pattern: DealDeskPattern, composite: float) -> str:
        if pattern == DealDeskPattern.none and composite < 20:
            return "Deal desk utilization healthy — pricing discipline and exception management within benchmarks"
        parts: list[str] = []
        if inp.deals_requiring_approval_pct < 1.0:
            parts.append(f"{inp.deals_requiring_approval_pct*100:.0f}% deals need approval")
        if inp.late_stage_escalation_rate_pct < 1.0:
            parts.append(f"{inp.late_stage_escalation_rate_pct*100:.0f}% late-stage escalations")
        parts.append(f"{inp.avg_deal_desk_cycles_per_deal:.1f} avg desk cycles")
        label = pattern.value.replace("_", " ") if pattern != DealDeskPattern.none else "Deal desk risk"
        summary = " — ".join(parts) if parts else "exception dependency elevated"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: DealDeskInput) -> DealDeskResult:
        approval    = round(self._approval_dependency_score(inp), 1)
        complexity  = round(self._exception_complexity_score(inp), 1)
        urgency     = round(self._exception_urgency_score(inp), 1)
        impact      = round(self._exception_impact_score(inp), 1)

        composite = round(
            approval * 0.30 + complexity * 0.30 + urgency * 0.25 + impact * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, approval, complexity, urgency, impact)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_deal_desk_gap(composite, inp)
        coach  = self._requires_deal_desk_coaching(composite, inp)
        impact_ = self._estimated_margin_risk(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = DealDeskResult(
            rep_id=inp.rep_id,
            region=inp.region,
            deal_desk_risk=risk,
            deal_desk_pattern=pattern,
            deal_desk_severity=severity,
            recommended_action=action,
            approval_dependency_score=approval,
            exception_complexity_score=complexity,
            exception_urgency_score=urgency,
            exception_impact_score=impact,
            deal_desk_composite=composite,
            has_deal_desk_gap=gap,
            requires_deal_desk_coaching=coach,
            estimated_margin_risk_usd=impact_,
            deal_desk_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[DealDeskInput]) -> list[DealDeskResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_deal_desk_composite": 0.0,
                "deal_desk_gap_count": 0,
                "coaching_count": 0,
                "avg_approval_dependency_score": 0.0,
                "avg_exception_complexity_score": 0.0,
                "avg_exception_urgency_score": 0.0,
                "avg_exception_impact_score": 0.0,
                "total_estimated_margin_risk_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_app = total_cpx = total_urg = total_imp = total_impact = 0.0

        for r in self._results:
            risk_counts[r.deal_desk_risk.value]       = risk_counts.get(r.deal_desk_risk.value, 0) + 1
            pattern_counts[r.deal_desk_pattern.value] = pattern_counts.get(r.deal_desk_pattern.value, 0) + 1
            severity_counts[r.deal_desk_severity.value] = severity_counts.get(r.deal_desk_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp   += r.deal_desk_composite
            total_app    += r.approval_dependency_score
            total_cpx    += r.exception_complexity_score
            total_urg    += r.exception_urgency_score
            total_imp    += r.exception_impact_score
            total_impact += r.estimated_margin_risk_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_deal_desk_composite":                  round(total_comp / n, 1),
            "deal_desk_gap_count":                      sum(1 for r in self._results if r.has_deal_desk_gap),
            "coaching_count":                           sum(1 for r in self._results if r.requires_deal_desk_coaching),
            "avg_approval_dependency_score":            round(total_app / n, 1),
            "avg_exception_complexity_score":           round(total_cpx / n, 1),
            "avg_exception_urgency_score":              round(total_urg / n, 1),
            "avg_exception_impact_score":               round(total_imp / n, 1),
            "total_estimated_margin_risk_usd":          round(total_impact, 2),
        }
