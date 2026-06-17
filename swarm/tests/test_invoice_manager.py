"""Tests for InvoiceManager."""

from datetime import datetime, timedelta

import pytest

from swarm.intelligence.invoice_manager import (
    Invoice,
    InvoiceManager,
    InvoiceStatus,
    Payment,
    PaymentMethod,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture()
def mgr():
    return InvoiceManager()


def _create(mgr: InvoiceManager, n: int = 1, amount_ht: float = 499.0):
    result = []
    for i in range(n):
        result.append(mgr.create(f"p{i+1:03d}", f"Company {i+1}", "artisan", amount_ht=amount_ht))
    return result if n > 1 else result[0]


# ── create ────────────────────────────────────────────────────────────────────

class TestCreate:
    def test_creates_invoice(self, mgr):
        inv = mgr.create("p001", "ACME", "tech", amount_ht=499.0)
        assert inv.invoice_id.startswith("INV-")
        assert inv.prospect_id == "p001"
        assert inv.company_name == "ACME"
        assert inv.amount_ht == 499.0
        assert inv.status == InvoiceStatus.DRAFT

    def test_ids_unique(self, mgr):
        i1, i2 = _create(mgr, 2)
        assert i1.invoice_id != i2.invoice_id

    def test_amount_ttc_default_20pct(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)
        assert inv.amount_ttc == 120.0

    def test_amount_ttc_custom_tva(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0, tva_pct=10.0)
        assert inv.amount_ttc == 110.0

    def test_tva_amount(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)
        assert inv.tva_amount == 20.0

    def test_initial_amount_paid_zero(self, mgr):
        inv = _create(mgr)
        assert inv.amount_paid == 0.0

    def test_initial_amount_remaining_equals_ttc(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)
        assert inv.amount_remaining == 120.0

    def test_custom_timestamp(self, mgr):
        ts = datetime(2024, 1, 1)
        inv = mgr.create("p001", "A", ts=ts)
        assert inv.created_at == ts

    def test_notes_stored(self, mgr):
        inv = mgr.create("p001", "A", notes="Payable en 3x")
        assert inv.notes == "Payable en 3x"

    def test_stored_in_manager(self, mgr):
        inv = _create(mgr)
        assert mgr.get(inv.invoice_id) is inv


# ── send ──────────────────────────────────────────────────────────────────────

class TestSend:
    def test_send_draft(self, mgr):
        inv = _create(mgr)
        assert mgr.send(inv.invoice_id)
        assert inv.status == InvoiceStatus.SENT
        assert inv.sent_at is not None
        assert inv.due_at is not None

    def test_send_sets_due_at(self, mgr):
        ts = datetime(2024, 1, 1)
        inv = mgr.create("p001", "A", due_days=30)
        mgr.send(inv.invoice_id, ts=ts)
        assert inv.due_at == ts + timedelta(days=30)

    def test_send_already_sent_returns_false(self, mgr):
        inv = _create(mgr)
        mgr.send(inv.invoice_id)
        assert not mgr.send(inv.invoice_id)

    def test_send_missing_returns_false(self, mgr):
        assert not mgr.send("INV-9999")

    def test_send_custom_timestamp(self, mgr):
        ts = datetime(2024, 3, 15)
        inv = _create(mgr)
        mgr.send(inv.invoice_id, ts=ts)
        assert inv.sent_at == ts


# ── cancel ────────────────────────────────────────────────────────────────────

class TestCancel:
    def test_cancel_draft(self, mgr):
        inv = _create(mgr)
        assert mgr.cancel(inv.invoice_id)
        assert inv.status == InvoiceStatus.CANCELLED
        assert inv.cancelled_at is not None

    def test_cancel_sent(self, mgr):
        inv = _create(mgr)
        mgr.send(inv.invoice_id)
        assert mgr.cancel(inv.invoice_id)
        assert inv.status == InvoiceStatus.CANCELLED

    def test_cancel_paid_returns_false(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)
        mgr.send(inv.invoice_id)
        mgr.record_payment(inv.invoice_id, 120.0)
        assert not mgr.cancel(inv.invoice_id)

    def test_cancel_already_cancelled_returns_false(self, mgr):
        inv = _create(mgr)
        mgr.cancel(inv.invoice_id)
        assert not mgr.cancel(inv.invoice_id)


# ── record_payment ────────────────────────────────────────────────────────────

class TestRecordPayment:
    def test_full_payment_marks_paid(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)  # TTC = 120
        mgr.send(inv.invoice_id)
        pay = mgr.record_payment(inv.invoice_id, 120.0)
        assert pay is not None
        assert inv.status == InvoiceStatus.PAID
        assert inv.paid_at is not None

    def test_partial_payment_marks_partially_paid(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)
        mgr.send(inv.invoice_id)
        mgr.record_payment(inv.invoice_id, 60.0)
        assert inv.status == InvoiceStatus.PARTIALLY_PAID
        assert inv.amount_paid == 60.0
        assert inv.amount_remaining == 60.0

    def test_two_partial_payments_complete(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)
        mgr.send(inv.invoice_id)
        mgr.record_payment(inv.invoice_id, 60.0)
        mgr.record_payment(inv.invoice_id, 60.0)
        assert inv.status == InvoiceStatus.PAID
        assert inv.amount_paid == 120.0
        assert inv.amount_remaining == 0.0

    def test_payment_on_paid_invoice_returns_none(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)
        mgr.send(inv.invoice_id)
        mgr.record_payment(inv.invoice_id, 120.0)
        result = mgr.record_payment(inv.invoice_id, 10.0)
        assert result is None

    def test_payment_on_cancelled_returns_none(self, mgr):
        inv = _create(mgr)
        mgr.cancel(inv.invoice_id)
        result = mgr.record_payment(inv.invoice_id, 100.0)
        assert result is None

    def test_payment_missing_invoice_returns_none(self, mgr):
        assert mgr.record_payment("INV-9999", 100.0) is None

    def test_payment_method_stored(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)
        mgr.send(inv.invoice_id)
        pay = mgr.record_payment(inv.invoice_id, 120.0, method=PaymentMethod.BANK_TRANSFER)
        assert pay.method == PaymentMethod.BANK_TRANSFER

    def test_payment_reference_stored(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)
        mgr.send(inv.invoice_id)
        pay = mgr.record_payment(inv.invoice_id, 120.0, reference="ch_123")
        assert pay.reference == "ch_123"

    def test_payment_counter_increments(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)
        mgr.send(inv.invoice_id)
        p1 = mgr.record_payment(inv.invoice_id, 60.0)
        p2 = mgr.record_payment(inv.invoice_id, 60.0)
        assert p1.payment_id != p2.payment_id

    def test_rounding_tolerance(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)  # TTC=120.0
        mgr.send(inv.invoice_id)
        mgr.record_payment(inv.invoice_id, 119.997)
        assert inv.status == InvoiceStatus.PAID


# ── refresh_overdue ────────────────────────────────────────────────────────────

class TestRefreshOverdue:
    def test_marks_past_due_as_overdue(self, mgr):
        ts_sent = datetime(2024, 1, 1)
        inv = mgr.create("p001", "A", amount_ht=100.0, due_days=30)
        mgr.send(inv.invoice_id, ts=ts_sent)
        # advance 31 days
        count = mgr.refresh_overdue(as_of=ts_sent + timedelta(days=31))
        assert count == 1
        assert inv.status == InvoiceStatus.OVERDUE

    def test_not_yet_due_not_marked(self, mgr):
        ts_sent = datetime(2024, 1, 1)
        inv = mgr.create("p001", "A", amount_ht=100.0, due_days=30)
        mgr.send(inv.invoice_id, ts=ts_sent)
        count = mgr.refresh_overdue(as_of=ts_sent + timedelta(days=15))
        assert count == 0
        assert inv.status == InvoiceStatus.SENT

    def test_paid_not_marked_overdue(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0, due_days=1)
        ts = datetime(2024, 1, 1)
        mgr.send(inv.invoice_id, ts=ts)
        mgr.record_payment(inv.invoice_id, 120.0)
        mgr.refresh_overdue(as_of=ts + timedelta(days=5))
        assert inv.status == InvoiceStatus.PAID

    def test_partially_paid_can_become_overdue(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0, due_days=10)
        ts = datetime(2024, 1, 1)
        mgr.send(inv.invoice_id, ts=ts)
        mgr.record_payment(inv.invoice_id, 60.0)
        mgr.refresh_overdue(as_of=ts + timedelta(days=11))
        assert inv.status == InvoiceStatus.OVERDUE


# ── Queries ───────────────────────────────────────────────────────────────────

class TestQueries:
    def test_get_existing(self, mgr):
        inv = _create(mgr)
        assert mgr.get(inv.invoice_id) is inv

    def test_get_missing(self, mgr):
        assert mgr.get("INV-0000") is None

    def test_get_by_prospect(self, mgr):
        i1 = mgr.create("p001", "A")
        i2 = mgr.create("p001", "A")
        mgr.create("p002", "B")
        results = mgr.get_by_prospect("p001")
        assert len(results) == 2
        assert i1 in results and i2 in results

    def test_by_status(self, mgr):
        i1 = _create(mgr)
        i2 = mgr.create("p002", "B")
        mgr.send(i1.invoice_id)
        sent = mgr.by_status(InvoiceStatus.SENT)
        assert i1 in sent and i2 not in sent

    def test_overdue_query(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0, due_days=1)
        ts = datetime(2024, 1, 1)
        mgr.send(inv.invoice_id, ts=ts)
        mgr.refresh_overdue(as_of=ts + timedelta(days=2))
        assert inv in mgr.overdue()

    def test_unpaid(self, mgr):
        i1 = mgr.create("p001", "A", amount_ht=100.0)
        i2 = mgr.create("p002", "B", amount_ht=100.0)
        mgr.send(i1.invoice_id)
        mgr.send(i2.invoice_id)
        mgr.record_payment(i2.invoice_id, 120.0)
        unpaid = mgr.unpaid()
        assert i1 in unpaid and i2 not in unpaid

    def test_by_sector(self, mgr):
        mgr.create("p001", "A", sector="artisan")
        mgr.create("p002", "B", sector="juridique")
        mgr.create("p003", "C", sector="artisan spécialisé")
        results = mgr.by_sector("artisan")
        assert len(results) == 2


# ── Analytics ─────────────────────────────────────────────────────────────────

class TestAnalytics:
    def test_total_invoiced_excludes_cancelled(self, mgr):
        i1 = mgr.create("p001", "A", amount_ht=100.0)  # TTC 120
        i2 = mgr.create("p002", "B", amount_ht=100.0)  # TTC 120 (cancelled)
        mgr.cancel(i2.invoice_id)
        assert mgr.total_invoiced_ttc() == 120.0

    def test_total_collected(self, mgr):
        i1 = mgr.create("p001", "A", amount_ht=100.0)
        i2 = mgr.create("p002", "B", amount_ht=50.0)
        mgr.send(i1.invoice_id)
        mgr.send(i2.invoice_id)
        mgr.record_payment(i1.invoice_id, 120.0)
        mgr.record_payment(i2.invoice_id, 30.0)
        assert mgr.total_collected_ttc() == 150.0

    def test_total_outstanding(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)  # TTC 120
        mgr.send(inv.invoice_id)
        mgr.record_payment(inv.invoice_id, 60.0)
        assert mgr.total_outstanding_ttc() == 60.0

    def test_collection_rate_zero_when_nothing_invoiced(self, mgr):
        assert mgr.collection_rate() == 0.0

    def test_collection_rate_100(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)
        mgr.send(inv.invoice_id)
        mgr.record_payment(inv.invoice_id, 120.0)
        assert mgr.collection_rate() == 100.0

    def test_collection_rate_partial(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)  # TTC 120
        mgr.send(inv.invoice_id)
        mgr.record_payment(inv.invoice_id, 60.0)
        assert mgr.collection_rate() == 50.0

    def test_avg_days_to_pay_none_when_no_paid(self, mgr):
        assert mgr.average_days_to_pay() is None

    def test_avg_days_to_pay(self, mgr):
        ts = datetime(2024, 1, 1)
        i1 = mgr.create("p001", "A", amount_ht=100.0)
        mgr.send(i1.invoice_id, ts=ts)
        mgr.record_payment(i1.invoice_id, 120.0, ts=ts + timedelta(days=10))
        i2 = mgr.create("p002", "B", amount_ht=100.0)
        mgr.send(i2.invoice_id, ts=ts)
        mgr.record_payment(i2.invoice_id, 120.0, ts=ts + timedelta(days=20))
        assert mgr.average_days_to_pay() == 15.0

    def test_sector_summary(self, mgr):
        i1 = mgr.create("p001", "A", sector="artisan", amount_ht=100.0)
        i2 = mgr.create("p002", "B", sector="artisan", amount_ht=200.0)
        mgr.send(i1.invoice_id)
        mgr.record_payment(i1.invoice_id, 120.0)
        result = mgr.sector_summary()
        assert "artisan" in result
        assert result["artisan"]["count"] == 2
        assert result["artisan"]["collected"] == 120.0

    def test_payment_method_breakdown(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)
        mgr.send(inv.invoice_id)
        mgr.record_payment(inv.invoice_id, 60.0, method=PaymentMethod.STRIPE)
        mgr.record_payment(inv.invoice_id, 60.0, method=PaymentMethod.BANK_TRANSFER)
        breakdown = mgr.payment_method_breakdown()
        assert breakdown["stripe"]["count"] == 1
        assert breakdown["bank_transfer"]["count"] == 1


# ── summary() ─────────────────────────────────────────────────────────────────

class TestSummary:
    def test_empty_summary(self, mgr):
        s = mgr.summary()
        assert s["total"] == 0
        assert s["collection_rate_pct"] == 0.0

    def test_summary_keys(self, mgr):
        s = mgr.summary()
        for key in ["total", "draft", "sent", "partially_paid", "paid", "overdue", "cancelled",
                    "total_invoiced_ttc", "total_collected_ttc", "total_outstanding_ttc",
                    "total_overdue_ttc", "collection_rate_pct", "avg_days_to_pay"]:
            assert key in s

    def test_summary_counts(self, mgr):
        i1 = _create(mgr, amount_ht=100.0)
        i2 = mgr.create("p002", "B", amount_ht=100.0, due_days=1)
        i3 = mgr.create("p003", "C", amount_ht=100.0)
        mgr.send(i2.invoice_id, ts=datetime(2024, 1, 1))
        mgr.cancel(i3.invoice_id)
        mgr.refresh_overdue(as_of=datetime(2024, 1, 5))
        s = mgr.summary()
        assert s["total"] == 3
        assert s["draft"] == 1
        assert s["overdue"] == 1
        assert s["cancelled"] == 1


# ── to_dict ───────────────────────────────────────────────────────────────────

class TestToDict:
    def test_invoice_to_dict(self, mgr):
        inv = mgr.create("p001", "ACME", "tech", amount_ht=100.0)
        mgr.send(inv.invoice_id)
        mgr.record_payment(inv.invoice_id, 60.0, method=PaymentMethod.STRIPE, reference="ch_x")
        d = inv.to_dict()
        assert d["invoice_id"] == inv.invoice_id
        assert d["amount_ht"] == 100.0
        assert d["amount_ttc"] == 120.0
        assert d["amount_paid"] == 60.0
        assert d["amount_remaining"] == 60.0
        assert d["status"] == "partially_paid"
        assert len(d["payments"]) == 1
        assert d["payments"][0]["method"] == "stripe"

    def test_payment_to_dict_keys(self, mgr):
        inv = mgr.create("p001", "A", amount_ht=100.0)
        mgr.send(inv.invoice_id)
        pay = mgr.record_payment(inv.invoice_id, 120.0)
        d = pay.to_dict()
        for key in ["payment_id", "amount", "method", "received_at", "reference"]:
            assert key in d


# ── reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_all(self, mgr):
        _create(mgr, 3)
        mgr.reset()
        assert len(mgr.all_invoices()) == 0

    def test_reset_resets_counter(self, mgr):
        _create(mgr, 2)
        mgr.reset()
        inv = _create(mgr)
        assert inv.invoice_id == "INV-0001"
