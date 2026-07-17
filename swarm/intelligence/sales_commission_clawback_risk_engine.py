"""Sales Commission Clawback Risk Engine — predicts which closed deals are at risk
of triggering commission clawbacks due to early cancellation, payment failure,
deal revision, or contract disputes."""

from __future__ import annotations

import dataclasses
from enum import Enum


class ClawbackRisk(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class ClawbackLikelihood(str, Enum):
    unlikely = "unlikely"
    possible = "possible"
    probable = "probable"
    imminent = "imminent"


class ClawbackReason(str, Enum):
    none = "none"
    early_cancellation = "early_cancellation"
    payment_failure = "payment_failure"
    contract_dispute = "contract_dispute"
    deal_revision = "deal_revision"
    customer_bankruptcy = "customer_bankruptcy"


class ClawbackAction(str, Enum):
    no_action = "no_action"
    flag_for_review = "flag_for_review"
    hold_commission = "hold_commission"
    partial_clawback = "partial_clawback"
    full_clawback = "full_clawback"


@dataclasses.dataclass
class SalesCommissionClawbackInput:
    deal_id: str
    rep_id: str
    rep_name: str
    region: str
    deal_value_usd: float
    commission_paid_usd: float
    deal_close_date_days_ago: int
    contract_length_months: int
    payment_terms_days: int
    first_payment_received: int
    payment_failure_count: int
    customer_health_score: float
    customer_payment_history_score: float
    discount_pct: float
    company_avg_discount_pct: float
    customer_cancellation_request: int
    contract_dispute_flag: int
    legal_hold_flag: int
    customer_churn_risk_score: float
    competitor_displacement_flag: int
    deal_size_vs_avg_ratio: float
    rep_clawback_history_count: int


@dataclasses.dataclass
class SalesCommissionClawbackResult:
    deal_id: str
    rep_id: str
    clawback_risk: ClawbackRisk
    clawback_likelihood: ClawbackLikelihood
    primary_clawback_reason: ClawbackReason
    recommended_action: ClawbackAction
    payment_risk_score: float
    customer_stability_score: float
    deal_integrity_score: float
    rep_risk_score: float
    clawback_composite: float
    is_clawback_likely: bool
    requires_commission_hold: bool
    estimated_clawback_usd: float
    clawback_signal: str

    def to_dict(self) -> dict:
        return {
            "deal_id":                  self.deal_id,
            "rep_id":                   self.rep_id,
            "clawback_risk":            self.clawback_risk.value,
            "clawback_likelihood":      self.clawback_likelihood.value,
            "primary_clawback_reason":  self.primary_clawback_reason.value,
            "recommended_action":       self.recommended_action.value,
            "payment_risk_score":       round(self.payment_risk_score, 1),
            "customer_stability_score": round(self.customer_stability_score, 1),
            "deal_integrity_score":     round(self.deal_integrity_score, 1),
            "rep_risk_score":           round(self.rep_risk_score, 1),
            "clawback_composite":       round(self.clawback_composite, 1),
            "is_clawback_likely":       self.is_clawback_likely,
            "requires_commission_hold": self.requires_commission_hold,
            "estimated_clawback_usd":   round(self.estimated_clawback_usd, 2),
            "clawback_signal":          self.clawback_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class SalesCommissionClawbackRiskEngine:
    """Predicts commission clawback risk for closed deals."""

    def __init__(self) -> None:
        self._results: list[SalesCommissionClawbackResult] = []

    # ── sub-scores ──────────────────────────────────────────────────────────

    def _payment_risk(self, inp: SalesCommissionClawbackInput) -> float:
        """Higher = more payment risk."""
        score = 0.0
        # First payment not received yet
        if not inp.first_payment_received:
            score += 35.0
        # Payment failures
        if inp.payment_failure_count >= 3:
            score += 35.0
        elif inp.payment_failure_count >= 2:
            score += 24.0
        elif inp.payment_failure_count >= 1:
            score += 12.0
        # Long payment terms
        if inp.payment_terms_days > 90:
            score += 15.0
        elif inp.payment_terms_days > 60:
            score += 8.0
        # Customer payment history
        score += (1.0 - inp.customer_payment_history_score / 100.0) * 15.0
        return _clamp(score)

    def _customer_stability(self, inp: SalesCommissionClawbackInput) -> float:
        """Higher = more customer instability."""
        score = 0.0
        # Customer health
        score += (1.0 - inp.customer_health_score / 100.0) * 35.0
        # Churn risk
        score += (inp.customer_churn_risk_score / 100.0) * 35.0
        # Cancellation request active
        if inp.customer_cancellation_request:
            score += 25.0
        # Competitor trying to displace
        if inp.competitor_displacement_flag:
            score += 5.0
        return _clamp(score)

    def _deal_integrity(self, inp: SalesCommissionClawbackInput) -> float:
        """Higher = more deal integrity concern."""
        score = 0.0
        # Legal hold or contract dispute
        if inp.legal_hold_flag:
            score += 40.0
        if inp.contract_dispute_flag:
            score += 30.0
        # Aggressive discounting
        excess_discount = inp.discount_pct - inp.company_avg_discount_pct
        if excess_discount > 15:
            score += 20.0
        elif excess_discount > 10:
            score += 12.0
        elif excess_discount > 5:
            score += 6.0
        # Unusually large deal
        if inp.deal_size_vs_avg_ratio > 5.0:
            score += 10.0
        elif inp.deal_size_vs_avg_ratio > 3.0:
            score += 5.0
        return _clamp(score)

    def _rep_risk(self, inp: SalesCommissionClawbackInput) -> float:
        """Higher = rep has more clawback history."""
        score = 0.0
        if inp.rep_clawback_history_count >= 4:
            score += 60.0
        elif inp.rep_clawback_history_count >= 2:
            score += 35.0
        elif inp.rep_clawback_history_count >= 1:
            score += 15.0
        # Very short contract with high value
        if inp.contract_length_months <= 1 and inp.deal_value_usd > 100_000:
            score += 25.0
        elif inp.contract_length_months <= 3 and inp.deal_value_usd > 500_000:
            score += 15.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> ClawbackRisk:
        if composite < 20:
            return ClawbackRisk.low
        if composite < 45:
            return ClawbackRisk.moderate
        if composite < 65:
            return ClawbackRisk.high
        return ClawbackRisk.critical

    def _classify_likelihood(self, composite: float, inp: SalesCommissionClawbackInput) -> ClawbackLikelihood:
        if inp.legal_hold_flag and inp.customer_cancellation_request:
            return ClawbackLikelihood.imminent
        if composite >= 65:
            return ClawbackLikelihood.imminent
        if composite >= 45:
            return ClawbackLikelihood.probable
        if composite >= 20:
            return ClawbackLikelihood.possible
        return ClawbackLikelihood.unlikely

    def _primary_reason(
        self,
        inp: SalesCommissionClawbackInput,
        payment: float,
        stability: float,
        integrity: float,
        rep: float,
    ) -> ClawbackReason:
        if inp.customer_cancellation_request:
            return ClawbackReason.early_cancellation
        if inp.legal_hold_flag or inp.contract_dispute_flag:
            return ClawbackReason.contract_dispute
        scores = {
            ClawbackReason.payment_failure:    payment    if inp.payment_failure_count > 0 else 0,
            ClawbackReason.customer_bankruptcy: stability if inp.customer_health_score < 30 else 0,
            ClawbackReason.deal_revision:      integrity  if inp.discount_pct > inp.company_avg_discount_pct + 10 else 0,
        }
        best = max(scores, key=lambda k: scores[k])
        if scores[best] == 0:
            return ClawbackReason.none
        return best

    def _recommended_action(
        self, risk: ClawbackRisk, inp: SalesCommissionClawbackInput
    ) -> ClawbackAction:
        if inp.legal_hold_flag or (inp.customer_cancellation_request and risk in (ClawbackRisk.high, ClawbackRisk.critical)):
            return ClawbackAction.full_clawback
        if risk == ClawbackRisk.critical:
            return ClawbackAction.full_clawback
        if risk == ClawbackRisk.high:
            return ClawbackAction.partial_clawback
        if risk == ClawbackRisk.moderate:
            return ClawbackAction.hold_commission
        if inp.rep_clawback_history_count >= 1:
            return ClawbackAction.flag_for_review
        return ClawbackAction.no_action

    def _signal(
        self,
        risk: ClawbackRisk,
        reason: ClawbackReason,
        composite: float,
        inp: SalesCommissionClawbackInput,
    ) -> str:
        if risk == ClawbackRisk.low:
            return "deal appears stable — low clawback risk"
        msgs = {
            ClawbackReason.early_cancellation: (
                f"cancellation request active — deal at high clawback risk"
            ),
            ClawbackReason.contract_dispute: (
                f"legal hold or contract dispute — commission at risk"
            ),
            ClawbackReason.payment_failure: (
                f"{inp.payment_failure_count} payment failure(s) — first payment {'received' if inp.first_payment_received else 'not yet received'}"
            ),
            ClawbackReason.customer_bankruptcy: (
                f"customer health score {inp.customer_health_score:.0f}/100 — high churn risk"
            ),
            ClawbackReason.deal_revision: (
                f"discount {inp.discount_pct:.1f}% vs avg {inp.company_avg_discount_pct:.1f}% — deal may require revision"
            ),
        }
        base = msgs.get(reason, f"elevated clawback risk composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: SalesCommissionClawbackInput) -> SalesCommissionClawbackResult:
        payment   = self._payment_risk(inp)
        stability = self._customer_stability(inp)
        integrity = self._deal_integrity(inp)
        rep       = self._rep_risk(inp)

        composite = _clamp(
            payment * 0.35
            + stability * 0.30
            + integrity * 0.25
            + rep * 0.10
        )
        composite = round(composite, 1)

        risk        = self._classify_risk(composite)
        likelihood  = self._classify_likelihood(composite, inp)
        reason      = self._primary_reason(inp, payment, stability, integrity, rep)
        action      = self._recommended_action(risk, inp)

        is_clawback_likely = (
            composite >= 40
            or inp.customer_cancellation_request == 1
            or inp.legal_hold_flag == 1
        )
        requires_commission_hold = (
            composite >= 30
            or inp.payment_failure_count >= 2
            or inp.contract_dispute_flag == 1
        )

        estimated_clawback_usd = inp.commission_paid_usd * (composite / 100.0)

        result = SalesCommissionClawbackResult(
            deal_id=inp.deal_id,
            rep_id=inp.rep_id,
            clawback_risk=risk,
            clawback_likelihood=likelihood,
            primary_clawback_reason=reason,
            recommended_action=action,
            payment_risk_score=payment,
            customer_stability_score=stability,
            deal_integrity_score=integrity,
            rep_risk_score=rep,
            clawback_composite=composite,
            is_clawback_likely=is_clawback_likely,
            requires_commission_hold=requires_commission_hold,
            estimated_clawback_usd=estimated_clawback_usd,
            clawback_signal=self._signal(risk, reason, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[SalesCommissionClawbackInput]
    ) -> list[SalesCommissionClawbackResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "likelihood_counts": {},
                "reason_counts": {},
                "action_counts": {},
                "avg_clawback_composite": 0.0,
                "clawback_likely_count": 0,
                "commission_hold_count": 0,
                "avg_payment_risk_score": 0.0,
                "avg_customer_stability_score": 0.0,
                "avg_deal_integrity_score": 0.0,
                "avg_rep_risk_score": 0.0,
                "total_estimated_clawback_usd": 0.0,
            }

        risk_counts:       dict[str, int] = {}
        likelihood_counts: dict[str, int] = {}
        reason_counts:     dict[str, int] = {}
        action_counts:     dict[str, int] = {}
        total_comp = total_pay = total_stab = total_int = total_rep = total_claw = 0.0
        likely = hold = 0

        for r in self._results:
            risk_counts[r.clawback_risk.value]              = risk_counts.get(r.clawback_risk.value, 0) + 1
            likelihood_counts[r.clawback_likelihood.value]  = likelihood_counts.get(r.clawback_likelihood.value, 0) + 1
            reason_counts[r.primary_clawback_reason.value]  = reason_counts.get(r.primary_clawback_reason.value, 0) + 1
            action_counts[r.recommended_action.value]       = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.clawback_composite
            total_pay  += r.payment_risk_score
            total_stab += r.customer_stability_score
            total_int  += r.deal_integrity_score
            total_rep  += r.rep_risk_score
            total_claw += r.estimated_clawback_usd
            if r.is_clawback_likely:
                likely += 1
            if r.requires_commission_hold:
                hold += 1

        n = len(self._results)
        return {
            "total":                        n,
            "risk_counts":                  risk_counts,
            "likelihood_counts":            likelihood_counts,
            "reason_counts":                reason_counts,
            "action_counts":                action_counts,
            "avg_clawback_composite":       round(total_comp / n, 1),
            "clawback_likely_count":        likely,
            "commission_hold_count":        hold,
            "avg_payment_risk_score":       round(total_pay  / n, 1),
            "avg_customer_stability_score": round(total_stab / n, 1),
            "avg_deal_integrity_score":     round(total_int  / n, 1),
            "avg_rep_risk_score":           round(total_rep  / n, 1),
            "total_estimated_clawback_usd": round(total_claw, 2),
        }
