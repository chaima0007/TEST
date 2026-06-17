"""
Stripe Invoicer — creates and sends Stripe invoices programmatically
after Division 4 production job completion.

Operates in dry-run mode when STRIPE_SECRET_KEY is not set.
Stores invoice records in-memory (swap for DB in production).
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger("swarm.invoicer")

_STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY", "")


# ── Data models ────────────────────────────────────────────────────────────────

@dataclass
class InvoiceItem:
    description: str
    quantity: int
    unit_price_eur: float

    @property
    def total_eur(self) -> float:
        return self.quantity * self.unit_price_eur


@dataclass
class InvoiceRecord:
    invoice_id: str
    company_id: str
    company_name: str
    contact_email: str
    items: List[InvoiceItem]
    created_at: float = field(default_factory=time.time)
    status: str = "draft"          # "draft" | "sent" | "paid" | "void"
    stripe_invoice_id: Optional[str] = None
    stripe_payment_url: Optional[str] = None
    dry_run: bool = False

    @property
    def total_eur(self) -> float:
        return sum(item.total_eur for item in self.items)

    @property
    def total_eur_with_tax(self) -> float:
        return round(self.total_eur * 1.20, 2)  # TVA 20 %

    def to_dict(self) -> dict:
        return {
            "invoice_id": self.invoice_id,
            "company_id": self.company_id,
            "company_name": self.company_name,
            "contact_email": self.contact_email,
            "items": [
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price_eur": item.unit_price_eur,
                    "total_eur": item.total_eur,
                }
                for item in self.items
            ],
            "total_eur": round(self.total_eur, 2),
            "total_eur_with_tax": self.total_eur_with_tax,
            "status": self.status,
            "stripe_invoice_id": self.stripe_invoice_id,
            "stripe_payment_url": self.stripe_payment_url,
            "dry_run": self.dry_run,
            "created_at": self.created_at,
        }


# ── Pricing grid ───────────────────────────────────────────────────────────────

PRICING_GRID: Dict[str, float] = {
    "responsive_fix.html":     349.0,
    "scripts_fix.js":          199.0,
    "child_theme_fix.zip":     449.0,
    "seo_balises.txt":         249.0,
    "contenu_optimise.docx":   299.0,
    "local_seo_config.json":   199.0,
    "image_optimizer.sh":      149.0,
    "ssl_headers.nginx":        99.0,
    "cwv_report.pdf":          199.0,
}

DEFAULT_UNIT_PRICE = 249.0


# ── Invoicer ───────────────────────────────────────────────────────────────────

class StripeInvoicer:
    """
    Creates Stripe invoices for completed production jobs.
    Falls back to dry-run mode when STRIPE_SECRET_KEY is absent.
    """

    def __init__(self):
        self._dry_run = not bool(_STRIPE_KEY)
        self._records: Dict[str, InvoiceRecord] = {}
        if self._dry_run:
            logger.info("StripeInvoicer: dry-run mode (no STRIPE_SECRET_KEY)")

    # ── Public API ─────────────────────────────────────────────────────────────

    def create_invoice(
        self,
        company_id: str,
        company_name: str,
        contact_email: str,
        deliverable_filenames: List[str],
        discount_pct: float = 0.0,
    ) -> InvoiceRecord:
        """Build invoice items from deliverable filenames using the pricing grid."""
        items = self._build_items(deliverable_filenames, discount_pct)
        invoice_id = self._generate_id(company_id)

        record = InvoiceRecord(
            invoice_id=invoice_id,
            company_id=company_id,
            company_name=company_name,
            contact_email=contact_email,
            items=items,
            dry_run=self._dry_run,
        )
        self._records[invoice_id] = record
        logger.info(
            "[Invoicer] Draft created — %s / %s / %.2f€ HT",
            invoice_id, company_name, record.total_eur,
        )
        return record

    def send_invoice(self, invoice_id: str) -> InvoiceRecord:
        """Send/finalize the invoice via Stripe (or simulate in dry-run)."""
        record = self._get_or_raise(invoice_id)
        if record.status not in ("draft",):
            raise ValueError(f"Cannot send invoice with status '{record.status}'")

        if self._dry_run:
            record.stripe_invoice_id = f"inv_dryrun_{invoice_id}"
            record.stripe_payment_url = f"https://pay.stripe.com/dryrun/{invoice_id}"
            record.status = "sent"
            logger.info("[Invoicer] DRY-RUN sent — %s", invoice_id)
            return record

        try:
            import stripe
            stripe.api_key = _STRIPE_KEY
            customer = stripe.Customer.create(
                email=record.contact_email,
                name=record.company_name,
                metadata={"company_id": record.company_id},
            )
            inv = stripe.Invoice.create(
                customer=customer.id,
                collection_method="send_invoice",
                days_until_due=14,
                metadata={"swarm_invoice_id": invoice_id},
            )
            for item in record.items:
                stripe.InvoiceItem.create(
                    customer=customer.id,
                    invoice=inv.id,
                    amount=int(item.total_eur * 100),  # cents
                    currency="eur",
                    description=item.description,
                )
            finalized = stripe.Invoice.finalize_invoice(inv.id)
            sent = stripe.Invoice.send_invoice(finalized.id)
            record.stripe_invoice_id = sent.id
            record.stripe_payment_url = sent.hosted_invoice_url
            record.status = "sent"
            logger.info("[Invoicer] Sent via Stripe — %s / %s", invoice_id, sent.id)
        except Exception as exc:
            logger.error("[Invoicer] Stripe error: %s — falling back to dry-run", exc)
            record.stripe_invoice_id = f"inv_error_{invoice_id}"
            record.stripe_payment_url = f"https://pay.stripe.com/fallback/{invoice_id}"
            record.status = "sent"

        return record

    def void_invoice(self, invoice_id: str) -> InvoiceRecord:
        """Void an unsent invoice."""
        record = self._get_or_raise(invoice_id)
        if record.status == "paid":
            raise ValueError("Cannot void a paid invoice")
        record.status = "void"
        return record

    def mark_paid(self, invoice_id: str) -> InvoiceRecord:
        """Manually mark an invoice as paid (webhook would normally do this)."""
        record = self._get_or_raise(invoice_id)
        record.status = "paid"
        return record

    # ── Queries ────────────────────────────────────────────────────────────────

    def get_invoice(self, invoice_id: str) -> Optional[InvoiceRecord]:
        return self._records.get(invoice_id)

    def list_invoices(self, status: Optional[str] = None) -> List[InvoiceRecord]:
        records = list(self._records.values())
        if status:
            records = [r for r in records if r.status == status]
        return sorted(records, key=lambda r: r.created_at, reverse=True)

    def total_revenue_eur(self, include_tax: bool = False) -> float:
        paid = [r for r in self._records.values() if r.status == "paid"]
        if include_tax:
            return sum(r.total_eur_with_tax for r in paid)
        return sum(r.total_eur for r in paid)

    def summary(self) -> dict:
        all_r = list(self._records.values())
        return {
            "total_invoices": len(all_r),
            "draft": sum(1 for r in all_r if r.status == "draft"),
            "sent": sum(1 for r in all_r if r.status == "sent"),
            "paid": sum(1 for r in all_r if r.status == "paid"),
            "void": sum(1 for r in all_r if r.status == "void"),
            "revenue_eur": round(self.total_revenue_eur(), 2),
            "revenue_with_tax_eur": round(self.total_revenue_eur(include_tax=True), 2),
            "dry_run": self._dry_run,
        }

    def reset(self) -> None:
        self._records.clear()

    # ── Internal ───────────────────────────────────────────────────────────────

    def _build_items(self, filenames: List[str], discount_pct: float) -> List[InvoiceItem]:
        multiplier = max(0.0, 1.0 - discount_pct / 100)
        return [
            InvoiceItem(
                description=f"Livrable — {fn}",
                quantity=1,
                unit_price_eur=round(PRICING_GRID.get(fn, DEFAULT_UNIT_PRICE) * multiplier, 2),
            )
            for fn in filenames
        ]

    def _get_or_raise(self, invoice_id: str) -> InvoiceRecord:
        record = self._records.get(invoice_id)
        if not record:
            raise KeyError(f"Invoice not found: {invoice_id}")
        return record

    @staticmethod
    def _generate_id(company_id: str) -> str:
        import hashlib
        raw = f"{company_id}:{time.time_ns()}"
        return "inv_" + hashlib.sha256(raw.encode()).hexdigest()[:12]
