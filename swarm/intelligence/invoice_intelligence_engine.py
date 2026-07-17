"""
Module 222 — Invoice Intelligence Engine
Detects billing anomalies, overdue risk, dispute likelihood and
revenue leakage across invoices before they become collection problems.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class InvoiceRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class InvoicePattern(str, Enum):
    none               = "none"
    chronic_late_payer = "chronic_late_payer"
    dispute_prone      = "dispute_prone"
    partial_payment    = "partial_payment"
    billing_anomaly    = "billing_anomaly"
    revenue_leakage    = "revenue_leakage"


class InvoiceSeverity(str, Enum):
    healthy    = "healthy"
    watchlist  = "watchlist"
    at_risk    = "at_risk"
    critical   = "critical"


class InvoiceAction(str, Enum):
    no_action                = "no_action"
    payment_monitoring       = "payment_monitoring"
    gentle_reminder          = "gentle_reminder"
    formal_collection_notice = "formal_collection_notice"
    dispute_resolution_call  = "dispute_resolution_call"
    billing_correction       = "billing_correction"
    executive_escalation     = "executive_escalation"
    payment_plan_negotiation = "payment_plan_negotiation"
    legal_review_trigger     = "legal_review_trigger"


@dataclass
class InvoiceInput:
    invoice_id: str
    client_id: str
    region: str
    # Payment behavior
    days_overdue: int                      # days past due date (0 = on time)
    payment_delay_avg_days: float          # avg days to pay in last 12 months
    late_payment_frequency_pct: float      # % of invoices paid late historically
    partial_payment_count: int             # times paid partially in last 6 months
    # Dispute signals
    dispute_history_count: int             # disputes raised in last 12 months
    billing_error_rate_pct: float          # % of invoices that had billing errors
    credit_note_frequency: int             # credit notes issued in last 12 months
    invoice_rejection_count: int           # invoices rejected by client AP
    # Financial exposure
    invoice_amount_usd: float              # current invoice amount
    total_outstanding_usd: float           # total AR outstanding for client
    credit_limit_utilization_pct: float    # % of credit limit used
    days_sales_outstanding: float          # DSO for this client
    # Relationship context
    contract_value_usd: float              # total contract value
    client_tenure_months: int             # months as client
    account_health_score: float           # 0-1 (1 = very healthy account)
    payment_terms_days: int               # contracted payment terms (e.g. 30)
    # Collection signals
    last_contact_days_ago: int            # days since last collection contact
    promise_to_pay_broken_count: int      # broken payment promises
    escalation_count: int                 # prior escalations this year


@dataclass
class InvoiceResult:
    invoice_id: str
    client_id: str
    region: str
    invoice_risk: str
    invoice_pattern: str
    invoice_severity: str
    recommended_action: str
    overdue_score: float
    dispute_score: float
    exposure_score: float
    behavior_score: float
    invoice_composite: float
    has_collection_signal: bool
    requires_escalation: bool
    estimated_bad_debt_usd: float
    invoice_signal: str

    def to_dict(self) -> Dict:
        return {
            "invoice_id":             self.invoice_id,
            "client_id":              self.client_id,
            "region":                 self.region,
            "invoice_risk":           self.invoice_risk,
            "invoice_pattern":        self.invoice_pattern,
            "invoice_severity":       self.invoice_severity,
            "recommended_action":     self.recommended_action,
            "overdue_score":          self.overdue_score,
            "dispute_score":          self.dispute_score,
            "exposure_score":         self.exposure_score,
            "behavior_score":         self.behavior_score,
            "invoice_composite":      self.invoice_composite,
            "has_collection_signal":  self.has_collection_signal,
            "requires_escalation":    self.requires_escalation,
            "estimated_bad_debt_usd": self.estimated_bad_debt_usd,
            "invoice_signal":         self.invoice_signal,
        }


class InvoiceIntelligenceEngine:
    def __init__(self) -> None:
        self._results: List[InvoiceResult] = []

    def _overdue_score(self, i: InvoiceInput) -> float:
        s = 0
        if   i.days_overdue >= 60:  s += 40
        elif i.days_overdue >= 30:  s += 22
        elif i.days_overdue >= 10:  s += 8

        if   i.payment_delay_avg_days >= 45: s += 35
        elif i.payment_delay_avg_days >= 25: s += 18
        elif i.payment_delay_avg_days >= 10: s += 6

        if   i.promise_to_pay_broken_count >= 3: s += 25
        elif i.promise_to_pay_broken_count >= 1: s += 12
        return min(s, 100)

    def _dispute_score(self, i: InvoiceInput) -> float:
        s = 0
        if   i.dispute_history_count  >= 4:    s += 40
        elif i.dispute_history_count  >= 2:    s += 22
        elif i.dispute_history_count  >= 1:    s += 8

        if   i.billing_error_rate_pct >= 0.20: s += 35
        elif i.billing_error_rate_pct >= 0.10: s += 18
        elif i.billing_error_rate_pct >= 0.05: s += 6

        if   i.invoice_rejection_count >= 3:   s += 25
        elif i.invoice_rejection_count >= 1:   s += 12
        return min(s, 100)

    def _exposure_score(self, i: InvoiceInput) -> float:
        s = 0
        if   i.credit_limit_utilization_pct >= 0.90: s += 40
        elif i.credit_limit_utilization_pct >= 0.70: s += 22
        elif i.credit_limit_utilization_pct >= 0.50: s += 8

        if   i.days_sales_outstanding >= 75:  s += 35
        elif i.days_sales_outstanding >= 50:  s += 18
        elif i.days_sales_outstanding >= 30:  s += 6

        if   i.escalation_count >= 3: s += 25
        elif i.escalation_count >= 1: s += 12
        return min(s, 100)

    def _behavior_score(self, i: InvoiceInput) -> float:
        s = 0
        if   i.late_payment_frequency_pct >= 0.60: s += 45
        elif i.late_payment_frequency_pct >= 0.35: s += 25
        elif i.late_payment_frequency_pct >= 0.15: s += 10

        if   i.partial_payment_count >= 3: s += 30
        elif i.partial_payment_count >= 1: s += 15

        if   i.credit_note_frequency >= 4: s += 25
        elif i.credit_note_frequency >= 2: s += 12
        return min(s, 100)

    def _composite(self, ov: float, di: float, ex: float, bh: float) -> float:
        return min(round(ov * 0.30 + di * 0.25 + ex * 0.25 + bh * 0.20, 2), 100.0)

    def _risk(self, c: float) -> InvoiceRisk:
        if c >= 60: return InvoiceRisk.critical
        if c >= 40: return InvoiceRisk.high
        if c >= 20: return InvoiceRisk.moderate
        return InvoiceRisk.low

    def _severity(self, c: float) -> InvoiceSeverity:
        if c >= 60: return InvoiceSeverity.critical
        if c >= 40: return InvoiceSeverity.at_risk
        if c >= 20: return InvoiceSeverity.watchlist
        return InvoiceSeverity.healthy

    def _pattern(self, i: InvoiceInput) -> InvoicePattern:
        if (i.late_payment_frequency_pct >= 0.50
                and i.payment_delay_avg_days >= 30):
            return InvoicePattern.chronic_late_payer
        if (i.dispute_history_count >= 3
                and i.billing_error_rate_pct >= 0.10):
            return InvoicePattern.dispute_prone
        if (i.partial_payment_count >= 2
                and i.promise_to_pay_broken_count >= 1):
            return InvoicePattern.partial_payment
        if (i.billing_error_rate_pct >= 0.15
                and i.credit_note_frequency >= 3):
            return InvoicePattern.billing_anomaly
        if (i.credit_limit_utilization_pct >= 0.80
                and i.days_sales_outstanding >= 60):
            return InvoicePattern.revenue_leakage
        return InvoicePattern.none

    def _action(self, risk: InvoiceRisk, pat: InvoicePattern) -> InvoiceAction:
        if risk == InvoiceRisk.critical:
            if pat in (InvoicePattern.chronic_late_payer, InvoicePattern.partial_payment):
                return InvoiceAction.legal_review_trigger
            return InvoiceAction.executive_escalation
        if risk == InvoiceRisk.high:
            if pat == InvoicePattern.chronic_late_payer:  return InvoiceAction.formal_collection_notice
            if pat == InvoicePattern.dispute_prone:       return InvoiceAction.dispute_resolution_call
            if pat == InvoicePattern.partial_payment:     return InvoiceAction.payment_plan_negotiation
            if pat == InvoicePattern.billing_anomaly:     return InvoiceAction.billing_correction
            if pat == InvoicePattern.revenue_leakage:     return InvoiceAction.executive_escalation
            return InvoiceAction.payment_monitoring
        if risk == InvoiceRisk.moderate:
            return InvoiceAction.gentle_reminder
        return InvoiceAction.no_action

    def _signal(self, i: InvoiceInput, pat: InvoicePattern, comp: float) -> str:
        if comp < 20:
            return "Invoice health normal — payment behaviour, dispute history and exposure within acceptable thresholds"
        labels = {
            InvoicePattern.chronic_late_payer: "Chronic late payer",
            InvoicePattern.dispute_prone:      "Dispute-prone",
            InvoicePattern.partial_payment:    "Partial payment pattern",
            InvoicePattern.billing_anomaly:    "Billing anomaly",
            InvoicePattern.revenue_leakage:    "Revenue leakage",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — {i.days_overdue}d overdue — "
            f"${round(i.invoice_amount_usd/1000)}k invoice — "
            f"${round(i.total_outstanding_usd/1000)}k total AR — "
            f"DSO {round(i.days_sales_outstanding)}d — "
            f"composite {round(comp)}"
        )

    def _has_collection_signal(self, i: InvoiceInput, comp: float) -> bool:
        return (comp >= 40
                or i.days_overdue >= 15
                or i.late_payment_frequency_pct >= 0.35)

    def _requires_escalation(self, i: InvoiceInput, comp: float) -> bool:
        return (comp >= 25
                or i.days_overdue >= 30
                or i.promise_to_pay_broken_count >= 1)

    def _bad_debt(self, i: InvoiceInput, comp: float) -> float:
        return round(i.total_outstanding_usd * (comp / 100), 2)

    def assess(self, i: InvoiceInput) -> InvoiceResult:
        ov   = self._overdue_score(i)
        di   = self._dispute_score(i)
        ex   = self._exposure_score(i)
        bh   = self._behavior_score(i)
        comp = self._composite(ov, di, ex, bh)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = InvoiceResult(
            invoice_id=i.invoice_id,
            client_id=i.client_id,
            region=i.region,
            invoice_risk=risk.value,
            invoice_pattern=pat.value,
            invoice_severity=sev.value,
            recommended_action=act.value,
            overdue_score=ov,
            dispute_score=di,
            exposure_score=ex,
            behavior_score=bh,
            invoice_composite=comp,
            has_collection_signal=self._has_collection_signal(i, comp),
            requires_escalation=self._requires_escalation(i, comp),
            estimated_bad_debt_usd=self._bad_debt(i, comp),
            invoice_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[InvoiceInput]) -> List[InvoiceResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_invoice_composite": 0.0,
                "collection_signal_count": 0,
                "escalation_count": 0,
                "avg_overdue_score": 0.0,
                "avg_dispute_score": 0.0,
                "avg_exposure_score": 0.0,
                "avg_behavior_score": 0.0,
                "total_estimated_bad_debt_usd": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tov = tdi = tex = tbh = tcomp = tbd = 0.0
        gc = ec = 0
        for r in self._results:
            rc[r.invoice_risk]      = rc.get(r.invoice_risk, 0)      + 1
            pc[r.invoice_pattern]   = pc.get(r.invoice_pattern, 0)   + 1
            sc[r.invoice_severity]  = sc.get(r.invoice_severity, 0)  + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            tov   += r.overdue_score
            tdi   += r.dispute_score
            tex   += r.exposure_score
            tbh   += r.behavior_score
            tcomp += r.invoice_composite
            tbd   += r.estimated_bad_debt_usd
            if r.has_collection_signal: gc += 1
            if r.requires_escalation:   ec += 1
        return {
            "total":                          n,
            "risk_counts":                    rc,
            "pattern_counts":                 pc,
            "severity_counts":                sc,
            "action_counts":                  ac,
            "avg_invoice_composite":          round(tcomp / n, 1),
            "collection_signal_count":        gc,
            "escalation_count":               ec,
            "avg_overdue_score":              round(tov / n, 1),
            "avg_dispute_score":              round(tdi / n, 1),
            "avg_exposure_score":             round(tex / n, 1),
            "avg_behavior_score":             round(tbh / n, 1),
            "total_estimated_bad_debt_usd":   round(tbd, 2),
        }
