"""
Invoice Manager — creates, tracks, and reconciles invoices for
all prospects who have reached the WON stage.

Invoice lifecycle:
  DRAFT → SENT → PARTIALLY_PAID → PAID   (happy path)
                → OVERDUE                 (payment deadline missed)
                → CANCELLED               (voided before payment)

Each invoice can record multiple payment events (partial payments),
allowing tracking of instalment plans.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional


# ── Enums ─────────────────────────────────────────────────────────────────────

class InvoiceStatus(str, Enum):
    DRAFT           = "draft"
    SENT            = "sent"
    PARTIALLY_PAID  = "partially_paid"
    PAID            = "paid"
    OVERDUE         = "overdue"
    CANCELLED       = "cancelled"


class PaymentMethod(str, Enum):
    STRIPE      = "stripe"
    BANK_TRANSFER = "bank_transfer"
    CHEQUE      = "cheque"
    CASH        = "cash"
    OTHER       = "other"


# ── Payment record ────────────────────────────────────────────────────────────

@dataclass
class Payment:
    payment_id:    str
    amount:        float
    method:        PaymentMethod
    received_at:   datetime
    reference:     str = ""          # e.g. Stripe charge ID or bank ref

    def to_dict(self) -> dict:
        return {
            "payment_id":   self.payment_id,
            "amount":       self.amount,
            "method":       self.method.value,
            "received_at":  self.received_at.isoformat(),
            "reference":    self.reference,
        }


# ── Invoice ───────────────────────────────────────────────────────────────────

@dataclass
class Invoice:
    invoice_id:    str
    prospect_id:   str
    company_name:  str
    sector:        str
    amount_ht:     float             # HT (excl. VAT)
    tva_pct:       float = 20.0
    due_days:      int = 30          # payment deadline in days from sent_at
    status:        InvoiceStatus = InvoiceStatus.DRAFT
    created_at:    datetime = field(default_factory=datetime.utcnow)
    sent_at:       Optional[datetime] = None
    due_at:        Optional[datetime] = None
    paid_at:       Optional[datetime] = None
    cancelled_at:  Optional[datetime] = None
    payments:      List[Payment] = field(default_factory=list)
    notes:         str = ""

    # ── Derived financials ─────────────────────────────────────────────────────

    @property
    def amount_ttc(self) -> float:
        return round(self.amount_ht * (1 + self.tva_pct / 100), 2)

    @property
    def tva_amount(self) -> float:
        return round(self.amount_ttc - self.amount_ht, 2)

    @property
    def amount_paid(self) -> float:
        return round(sum(p.amount for p in self.payments), 2)

    @property
    def amount_remaining(self) -> float:
        return round(max(0.0, self.amount_ttc - self.amount_paid), 2)

    @property
    def is_overdue(self) -> bool:
        if self.due_at is None or self.status in (InvoiceStatus.PAID, InvoiceStatus.CANCELLED):
            return False
        return datetime.utcnow() > self.due_at

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def send(self, ts: Optional[datetime] = None) -> bool:
        if self.status != InvoiceStatus.DRAFT:
            return False
        now = ts or datetime.utcnow()
        self.sent_at = now
        self.due_at = now + timedelta(days=self.due_days)
        self.status = InvoiceStatus.SENT
        return True

    def cancel(self, ts: Optional[datetime] = None) -> bool:
        if self.status in (InvoiceStatus.PAID, InvoiceStatus.CANCELLED):
            return False
        self.cancelled_at = ts or datetime.utcnow()
        self.status = InvoiceStatus.CANCELLED
        return True

    def mark_overdue(self, ts: Optional[datetime] = None) -> bool:
        if self.status not in (InvoiceStatus.SENT, InvoiceStatus.PARTIALLY_PAID):
            return False
        self.status = InvoiceStatus.OVERDUE
        return True

    def to_dict(self) -> dict:
        return {
            "invoice_id":      self.invoice_id,
            "prospect_id":     self.prospect_id,
            "company_name":    self.company_name,
            "sector":          self.sector,
            "amount_ht":       self.amount_ht,
            "tva_pct":         self.tva_pct,
            "amount_ttc":      self.amount_ttc,
            "tva_amount":      self.tva_amount,
            "amount_paid":     self.amount_paid,
            "amount_remaining": self.amount_remaining,
            "status":          self.status.value,
            "due_days":        self.due_days,
            "created_at":      self.created_at.isoformat(),
            "sent_at":         self.sent_at.isoformat() if self.sent_at else None,
            "due_at":          self.due_at.isoformat() if self.due_at else None,
            "paid_at":         self.paid_at.isoformat() if self.paid_at else None,
            "cancelled_at":    self.cancelled_at.isoformat() if self.cancelled_at else None,
            "notes":           self.notes,
            "payments":        [p.to_dict() for p in self.payments],
        }


# ── Invoice Manager ───────────────────────────────────────────────────────────

class InvoiceManager:
    """
    Creates and tracks invoices for all closed (WON) prospects.

    Usage::
        mgr = InvoiceManager()
        inv = mgr.create("p001", "Plomberie Martin", "artisan", amount_ht=499.0)
        mgr.send(inv.invoice_id)
        mgr.record_payment(inv.invoice_id, 249.50, PaymentMethod.STRIPE, ref="ch_abc")
        mgr.record_payment(inv.invoice_id, 249.50, PaymentMethod.STRIPE, ref="ch_def")
        assert inv.status == InvoiceStatus.PAID
    """

    def __init__(self) -> None:
        self._records: Dict[str, Invoice] = {}
        self._invoice_counter = 0
        self._payment_counter = 0

    def _next_invoice_id(self) -> str:
        self._invoice_counter += 1
        return f"INV-{self._invoice_counter:04d}"

    def _next_payment_id(self) -> str:
        self._payment_counter += 1
        return f"PAY-{self._payment_counter:05d}"

    # ── Create ─────────────────────────────────────────────────────────────────

    def create(
        self,
        prospect_id: str,
        company_name: str,
        sector: str = "",
        amount_ht: float = 0.0,
        tva_pct: float = 20.0,
        due_days: int = 30,
        notes: str = "",
        ts: Optional[datetime] = None,
    ) -> Invoice:
        inv = Invoice(
            invoice_id=self._next_invoice_id(),
            prospect_id=prospect_id,
            company_name=company_name,
            sector=sector,
            amount_ht=amount_ht,
            tva_pct=tva_pct,
            due_days=due_days,
            notes=notes,
            created_at=ts or datetime.utcnow(),
        )
        self._records[inv.invoice_id] = inv
        return inv

    # ── Get ────────────────────────────────────────────────────────────────────

    def get(self, invoice_id: str) -> Optional[Invoice]:
        return self._records.get(invoice_id)

    def get_by_prospect(self, prospect_id: str) -> List[Invoice]:
        return [i for i in self._records.values() if i.prospect_id == prospect_id]

    def all_invoices(self) -> List[Invoice]:
        return list(self._records.values())

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def send(self, invoice_id: str, ts: Optional[datetime] = None) -> bool:
        inv = self._records.get(invoice_id)
        return inv.send(ts) if inv else False

    def cancel(self, invoice_id: str, ts: Optional[datetime] = None) -> bool:
        inv = self._records.get(invoice_id)
        return inv.cancel(ts) if inv else False

    def refresh_overdue(self, as_of: Optional[datetime] = None) -> int:
        """Mark all sent/partially_paid invoices past due_at as OVERDUE. Returns count updated."""
        now = as_of or datetime.utcnow()
        updated = 0
        for inv in self._records.values():
            if inv.status in (InvoiceStatus.SENT, InvoiceStatus.PARTIALLY_PAID):
                if inv.due_at and now > inv.due_at:
                    inv.mark_overdue()
                    updated += 1
        return updated

    # ── Payment recording ──────────────────────────────────────────────────────

    def record_payment(
        self,
        invoice_id: str,
        amount: float,
        method: PaymentMethod = PaymentMethod.STRIPE,
        reference: str = "",
        ts: Optional[datetime] = None,
    ) -> Optional[Payment]:
        inv = self._records.get(invoice_id)
        if not inv:
            return None
        if inv.status in (InvoiceStatus.PAID, InvoiceStatus.CANCELLED):
            return None

        pay = Payment(
            payment_id=self._next_payment_id(),
            amount=amount,
            method=method,
            received_at=ts or datetime.utcnow(),
            reference=reference,
        )
        inv.payments.append(pay)

        if inv.amount_remaining <= 0.005:  # within rounding tolerance
            inv.status = InvoiceStatus.PAID
            inv.paid_at = pay.received_at
        else:
            inv.status = InvoiceStatus.PARTIALLY_PAID

        return pay

    # ── Queries ────────────────────────────────────────────────────────────────

    def by_status(self, status: InvoiceStatus) -> List[Invoice]:
        return [i for i in self._records.values() if i.status == status]

    def overdue(self) -> List[Invoice]:
        return self.by_status(InvoiceStatus.OVERDUE)

    def paid(self) -> List[Invoice]:
        return self.by_status(InvoiceStatus.PAID)

    def unpaid(self) -> List[Invoice]:
        return [i for i in self._records.values()
                if i.status in (InvoiceStatus.SENT, InvoiceStatus.PARTIALLY_PAID, InvoiceStatus.OVERDUE)]

    def by_sector(self, sector: str) -> List[Invoice]:
        return [i for i in self._records.values() if sector.lower() in i.sector.lower()]

    # ── Analytics ──────────────────────────────────────────────────────────────

    def total_invoiced_ttc(self) -> float:
        return round(sum(i.amount_ttc for i in self._records.values()
                         if i.status != InvoiceStatus.CANCELLED), 2)

    def total_collected_ttc(self) -> float:
        return round(sum(i.amount_paid for i in self._records.values()), 2)

    def total_outstanding_ttc(self) -> float:
        return round(sum(i.amount_remaining for i in self._records.values()
                         if i.status not in (InvoiceStatus.PAID, InvoiceStatus.CANCELLED)), 2)

    def total_overdue_ttc(self) -> float:
        return round(sum(i.amount_remaining for i in self.overdue()), 2)

    def collection_rate(self) -> float:
        invoiced = self.total_invoiced_ttc()
        if invoiced == 0:
            return 0.0
        return round(self.total_collected_ttc() / invoiced * 100, 1)

    def average_days_to_pay(self) -> Optional[float]:
        paid_invoices = [i for i in self.paid() if i.sent_at and i.paid_at]
        if not paid_invoices:
            return None
        avg = sum((i.paid_at - i.sent_at).total_seconds() / 86400 for i in paid_invoices) / len(paid_invoices)
        return round(avg, 1)

    def sector_summary(self) -> Dict[str, dict]:
        result: Dict[str, dict] = {}
        for inv in self._records.values():
            if inv.status == InvoiceStatus.CANCELLED:
                continue
            s = inv.sector or "unknown"
            if s not in result:
                result[s] = {"count": 0, "invoiced": 0.0, "collected": 0.0, "outstanding": 0.0}
            result[s]["count"] += 1
            result[s]["invoiced"] = round(result[s]["invoiced"] + inv.amount_ttc, 2)
            result[s]["collected"] = round(result[s]["collected"] + inv.amount_paid, 2)
            result[s]["outstanding"] = round(result[s]["outstanding"] + inv.amount_remaining, 2)
        return result

    def payment_method_breakdown(self) -> Dict[str, dict]:
        counts: Dict[str, dict] = {}
        for inv in self._records.values():
            for pay in inv.payments:
                m = pay.method.value
                if m not in counts:
                    counts[m] = {"count": 0, "total": 0.0}
                counts[m]["count"] += 1
                counts[m]["total"] = round(counts[m]["total"] + pay.amount, 2)
        return counts

    def summary(self) -> dict:
        total = len(self._records)
        paid_n = self.paid()
        overdue_n = self.overdue()
        draft_n = self.by_status(InvoiceStatus.DRAFT)
        cancelled_n = self.by_status(InvoiceStatus.CANCELLED)
        return {
            "total":                total,
            "draft":                len(draft_n),
            "sent":                 len(self.by_status(InvoiceStatus.SENT)),
            "partially_paid":       len(self.by_status(InvoiceStatus.PARTIALLY_PAID)),
            "paid":                 len(paid_n),
            "overdue":              len(overdue_n),
            "cancelled":            len(cancelled_n),
            "total_invoiced_ttc":   self.total_invoiced_ttc(),
            "total_collected_ttc":  self.total_collected_ttc(),
            "total_outstanding_ttc": self.total_outstanding_ttc(),
            "total_overdue_ttc":    self.total_overdue_ttc(),
            "collection_rate_pct":  self.collection_rate(),
            "avg_days_to_pay":      self.average_days_to_pay(),
        }

    # ── Reset ──────────────────────────────────────────────────────────────────

    def reset(self) -> None:
        self._records.clear()
        self._invoice_counter = 0
        self._payment_counter = 0
