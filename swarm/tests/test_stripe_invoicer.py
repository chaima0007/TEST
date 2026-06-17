"""
Tests for exporters/stripe_invoicer.py
"""

import pytest
from exporters.stripe_invoicer import StripeInvoicer, InvoiceRecord, InvoiceItem, PRICING_GRID


# ── Helpers ───────────────────────────────────────────────────────────────────

def invoicer() -> StripeInvoicer:
    inv = StripeInvoicer()
    inv.reset()
    return inv


def create(inv: StripeInvoicer, company_id="co_001", filenames=None, discount=0.0) -> InvoiceRecord:
    return inv.create_invoice(
        company_id=company_id,
        company_name="Plomberie Martin SARL",
        contact_email="contact@plomberie.fr",
        deliverable_filenames=filenames or ["responsive_fix.html", "ssl_headers.nginx"],
        discount_pct=discount,
    )


# ── create_invoice ────────────────────────────────────────────────────────────

class TestCreateInvoice:
    def test_returns_invoice_record(self):
        inv = invoicer()
        record = create(inv)
        assert isinstance(record, InvoiceRecord)

    def test_invoice_id_starts_with_inv(self):
        record = create(invoicer())
        assert record.invoice_id.startswith("inv_")

    def test_company_id_preserved(self):
        inv = invoicer()
        record = create(inv, company_id="xyz_99")
        assert record.company_id == "xyz_99"

    def test_initial_status_is_draft(self):
        record = create(invoicer())
        assert record.status == "draft"

    def test_items_populated(self):
        record = create(invoicer())
        assert len(record.items) == 2

    def test_items_are_invoice_items(self):
        record = create(invoicer())
        assert all(isinstance(i, InvoiceItem) for i in record.items)

    def test_known_filename_uses_pricing_grid(self):
        inv = invoicer()
        record = create(inv, filenames=["responsive_fix.html"])
        assert record.items[0].unit_price_eur == PRICING_GRID["responsive_fix.html"]

    def test_unknown_filename_uses_default_price(self):
        from exporters.stripe_invoicer import DEFAULT_UNIT_PRICE
        inv = invoicer()
        record = create(inv, filenames=["mystery_file.docx"])
        assert record.items[0].unit_price_eur == DEFAULT_UNIT_PRICE

    def test_total_eur_sum_of_items(self):
        record = create(invoicer(), filenames=["responsive_fix.html", "ssl_headers.nginx"])
        expected = PRICING_GRID["responsive_fix.html"] + PRICING_GRID["ssl_headers.nginx"]
        assert abs(record.total_eur - expected) < 0.01

    def test_total_with_tax_is_20_pct_more(self):
        record = create(invoicer())
        assert abs(record.total_eur_with_tax - record.total_eur * 1.20) < 0.01

    def test_stripe_fields_none_initially(self):
        record = create(invoicer())
        assert record.stripe_invoice_id is None
        assert record.stripe_payment_url is None

    def test_dry_run_flag_is_true_without_key(self):
        record = create(invoicer())
        assert record.dry_run is True

    def test_empty_filenames_creates_empty_items(self):
        inv = invoicer()
        record = inv.create_invoice("c1", "Co", "e@c.fr", [])
        assert record.items == []
        assert record.total_eur == 0.0


# ── Discount ──────────────────────────────────────────────────────────────────

class TestDiscount:
    def test_zero_discount_no_change(self):
        inv = invoicer()
        record_full = create(inv, discount=0.0)
        record_zero = create(inv, discount=0.0)
        assert abs(record_full.total_eur - record_zero.total_eur) < 0.01

    def test_15_pct_discount_reduces_price(self):
        inv = invoicer()
        full = create(inv, filenames=["responsive_fix.html"], discount=0.0)
        disc = create(inv, filenames=["responsive_fix.html"], discount=15.0)
        assert disc.total_eur < full.total_eur
        assert abs(disc.total_eur - full.total_eur * 0.85) < 0.05

    def test_100_pct_discount_gives_zero(self):
        inv = invoicer()
        record = create(inv, filenames=["responsive_fix.html"], discount=100.0)
        assert record.total_eur == pytest.approx(0.0, abs=0.01)


# ── send_invoice (dry-run) ────────────────────────────────────────────────────

class TestSendInvoiceDryRun:
    def test_sent_status_after_send(self):
        inv = invoicer()
        record = create(inv)
        sent = inv.send_invoice(record.invoice_id)
        assert sent.status == "sent"

    def test_stripe_invoice_id_set_after_send(self):
        inv = invoicer()
        record = create(inv)
        sent = inv.send_invoice(record.invoice_id)
        assert sent.stripe_invoice_id is not None

    def test_stripe_payment_url_set_after_send(self):
        inv = invoicer()
        record = create(inv)
        sent = inv.send_invoice(record.invoice_id)
        assert sent.stripe_payment_url is not None
        assert record.invoice_id in sent.stripe_payment_url

    def test_cannot_send_void_invoice(self):
        inv = invoicer()
        record = create(inv)
        inv.void_invoice(record.invoice_id)
        with pytest.raises(ValueError):
            inv.send_invoice(record.invoice_id)

    def test_cannot_send_unknown_invoice(self):
        with pytest.raises(KeyError):
            invoicer().send_invoice("inv_doesnotexist")


# ── void_invoice ──────────────────────────────────────────────────────────────

class TestVoidInvoice:
    def test_void_sets_status(self):
        inv = invoicer()
        record = create(inv)
        voided = inv.void_invoice(record.invoice_id)
        assert voided.status == "void"

    def test_cannot_void_paid_invoice(self):
        inv = invoicer()
        record = create(inv)
        inv.mark_paid(record.invoice_id)
        with pytest.raises(ValueError):
            inv.void_invoice(record.invoice_id)

    def test_cannot_void_unknown_invoice(self):
        with pytest.raises(KeyError):
            invoicer().void_invoice("inv_ghost")


# ── mark_paid ─────────────────────────────────────────────────────────────────

class TestMarkPaid:
    def test_mark_paid_sets_status(self):
        inv = invoicer()
        record = create(inv)
        paid = inv.mark_paid(record.invoice_id)
        assert paid.status == "paid"

    def test_cannot_mark_unknown_paid(self):
        with pytest.raises(KeyError):
            invoicer().mark_paid("inv_ghost")


# ── get / list ────────────────────────────────────────────────────────────────

class TestListAndGet:
    def test_get_invoice_returns_record(self):
        inv = invoicer()
        record = create(inv)
        fetched = inv.get_invoice(record.invoice_id)
        assert fetched is not None
        assert fetched.invoice_id == record.invoice_id

    def test_get_unknown_returns_none(self):
        assert invoicer().get_invoice("inv_ghost") is None

    def test_list_invoices_all(self):
        inv = invoicer()
        create(inv, company_id="c1")
        create(inv, company_id="c2")
        assert len(inv.list_invoices()) == 2

    def test_list_invoices_filtered_by_status(self):
        inv = invoicer()
        r1 = create(inv, company_id="c1")
        r2 = create(inv, company_id="c2")
        inv.send_invoice(r1.invoice_id)
        drafts = inv.list_invoices(status="draft")
        sent = inv.list_invoices(status="sent")
        assert len(drafts) == 1
        assert len(sent) == 1


# ── revenue / summary ─────────────────────────────────────────────────────────

class TestRevenue:
    def test_revenue_zero_when_none_paid(self):
        inv = invoicer()
        create(inv)
        assert inv.total_revenue_eur() == 0.0

    def test_revenue_counts_only_paid(self):
        inv = invoicer()
        r1 = create(inv, company_id="c1")
        r2 = create(inv, company_id="c2")
        inv.mark_paid(r1.invoice_id)
        assert abs(inv.total_revenue_eur() - r1.total_eur) < 0.01

    def test_revenue_with_tax_is_more(self):
        inv = invoicer()
        r = create(inv)
        inv.mark_paid(r.invoice_id)
        assert inv.total_revenue_eur(include_tax=True) > inv.total_revenue_eur()

    def test_summary_has_all_keys(self):
        s = invoicer().summary()
        for key in ("total_invoices", "draft", "sent", "paid", "void", "revenue_eur", "dry_run"):
            assert key in s

    def test_summary_dry_run_is_true(self):
        assert invoicer().summary()["dry_run"] is True


# ── to_dict ───────────────────────────────────────────────────────────────────

class TestToDict:
    def test_to_dict_returns_dict(self):
        d = create(invoicer()).to_dict()
        assert isinstance(d, dict)

    def test_to_dict_has_items(self):
        d = create(invoicer()).to_dict()
        assert isinstance(d["items"], list)
        assert len(d["items"]) == 2

    def test_to_dict_total_eur_present(self):
        d = create(invoicer()).to_dict()
        assert "total_eur" in d
        assert d["total_eur"] > 0

    def test_to_dict_has_tax(self):
        d = create(invoicer()).to_dict()
        assert "total_eur_with_tax" in d
        assert d["total_eur_with_tax"] > d["total_eur"]


# ── reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_records(self):
        inv = invoicer()
        create(inv)
        inv.reset()
        assert inv.list_invoices() == []

    def test_reset_allows_fresh_invoicing(self):
        inv = invoicer()
        create(inv, company_id="c1")
        inv.reset()
        create(inv, company_id="c2")
        assert len(inv.list_invoices()) == 1
