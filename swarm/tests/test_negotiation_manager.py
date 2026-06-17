"""Tests for NegotiationManager."""

from datetime import datetime, timedelta

import pytest

from swarm.intelligence.negotiation_manager import (
    ConcessionType,
    NegotiationManager,
    NegotiationStatus,
    OfferParty,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture()
def mgr():
    return NegotiationManager()


def _open(mgr: NegotiationManager, n: int = 1):
    """Open n negotiations and return them."""
    result = []
    for i in range(n):
        result.append(mgr.open(f"p{i+1:03d}", f"Company {i+1}", "artisan", asking_price=1000.0))
    return result if n > 1 else result[0]


# ── open ──────────────────────────────────────────────────────────────────────

class TestOpen:
    def test_creates_negotiation(self, mgr):
        neg = mgr.open("p001", "ACME", "tech", asking_price=500.0)
        assert neg is not None
        assert neg.negotiation_id.startswith("neg_")
        assert neg.prospect_id == "p001"
        assert neg.company_name == "ACME"
        assert neg.sector == "tech"
        assert neg.asking_price == 500.0
        assert neg.status == NegotiationStatus.OPENED

    def test_ids_are_unique(self, mgr):
        n1, n2, n3 = _open(mgr, 3)
        assert n1.negotiation_id != n2.negotiation_id
        assert n2.negotiation_id != n3.negotiation_id

    def test_counter_increments(self, mgr):
        n1 = mgr.open("p1", "A", asking_price=100)
        n2 = mgr.open("p2", "B", asking_price=200)
        assert n2.negotiation_id > n1.negotiation_id

    def test_custom_timestamp(self, mgr):
        ts = datetime(2024, 1, 15, 10, 0)
        neg = mgr.open("p001", "ACME", ts=ts)
        assert neg.opened_at == ts

    def test_default_sector_empty(self, mgr):
        neg = mgr.open("p001", "ACME")
        assert neg.sector == ""

    def test_no_offers_initially(self, mgr):
        neg = _open(mgr)
        assert neg.rounds == 0
        assert neg.offers == []

    def test_current_amount_is_asking_price_when_no_offers(self, mgr):
        neg = mgr.open("p001", "A", asking_price=750.0)
        assert neg.current_amount == 750.0


# ── get / get_by_prospect ─────────────────────────────────────────────────────

class TestGet:
    def test_get_existing(self, mgr):
        neg = _open(mgr)
        assert mgr.get(neg.negotiation_id) is neg

    def test_get_missing(self, mgr):
        assert mgr.get("neg_99999") is None

    def test_get_by_prospect(self, mgr):
        neg1 = mgr.open("p001", "A", asking_price=100)
        neg2 = mgr.open("p001", "A", asking_price=200)
        mgr.open("p002", "B", asking_price=300)
        results = mgr.get_by_prospect("p001")
        assert len(results) == 2
        assert neg1 in results
        assert neg2 in results

    def test_get_by_prospect_missing(self, mgr):
        assert mgr.get_by_prospect("p999") == []


# ── add_offer ─────────────────────────────────────────────────────────────────

class TestAddOffer:
    def test_add_offer_returns_offer(self, mgr):
        neg = _open(mgr)
        offer = mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 850.0)
        assert offer is not None
        assert offer.amount == 850.0
        assert offer.party == OfferParty.PROSPECT
        assert offer.round_number == 1

    def test_add_offer_increments_rounds(self, mgr):
        neg = _open(mgr)
        mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 900.0)
        mgr.add_offer(neg.negotiation_id, OfferParty.US, 950.0)
        assert neg.rounds == 2

    def test_add_offer_updates_status_to_in_progress(self, mgr):
        neg = _open(mgr)
        assert neg.status == NegotiationStatus.OPENED
        mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 900.0)
        assert neg.status == NegotiationStatus.IN_PROGRESS

    def test_add_offer_missing_neg_returns_none(self, mgr):
        result = mgr.add_offer("neg_99999", OfferParty.US, 100.0)
        assert result is None

    def test_offer_round_numbers_sequential(self, mgr):
        neg = _open(mgr)
        for i, amount in enumerate([900, 920, 950], start=1):
            offer = mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, amount)
            assert offer.round_number == i

    def test_concession_type_default_is_price(self, mgr):
        neg = _open(mgr)
        offer = mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 800.0)
        assert offer.concession_type == ConcessionType.PRICE

    def test_concession_type_custom(self, mgr):
        neg = _open(mgr)
        offer = mgr.add_offer(neg.negotiation_id, OfferParty.US, 1000.0, ConcessionType.PAYMENT)
        assert offer.concession_type == ConcessionType.PAYMENT

    def test_offer_note_stored(self, mgr):
        neg = _open(mgr)
        offer = mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 800.0, note="Budget limité")
        assert offer.note == "Budget limité"

    def test_current_amount_updates(self, mgr):
        neg = mgr.open("p001", "A", asking_price=1000.0)
        mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 850.0)
        assert neg.current_amount == 850.0
        mgr.add_offer(neg.negotiation_id, OfferParty.US, 900.0)
        assert neg.current_amount == 900.0

    def test_custom_timestamp(self, mgr):
        neg = _open(mgr)
        ts = datetime(2024, 3, 1, 9, 0)
        offer = mgr.add_offer(neg.negotiation_id, OfferParty.US, 950.0, ts=ts)
        assert offer.proposed_at == ts


# ── agree / fail / abandon ────────────────────────────────────────────────────

class TestClosing:
    def test_agree(self, mgr):
        neg = _open(mgr)
        assert mgr.agree(neg.negotiation_id)
        assert neg.status == NegotiationStatus.AGREED
        assert neg.closed_at is not None

    def test_agree_twice_returns_false(self, mgr):
        neg = _open(mgr)
        mgr.agree(neg.negotiation_id)
        assert not mgr.agree(neg.negotiation_id)

    def test_fail(self, mgr):
        neg = _open(mgr)
        assert mgr.fail(neg.negotiation_id, reason="Prix trop élevé")
        assert neg.status == NegotiationStatus.FAILED
        assert neg.failure_reason == "Prix trop élevé"
        assert neg.closed_at is not None

    def test_fail_twice_returns_false(self, mgr):
        neg = _open(mgr)
        mgr.fail(neg.negotiation_id)
        assert not mgr.fail(neg.negotiation_id)

    def test_abandon(self, mgr):
        neg = _open(mgr)
        assert mgr.abandon(neg.negotiation_id)
        assert neg.status == NegotiationStatus.ABANDONED
        assert neg.closed_at is not None

    def test_fail_after_agreed_returns_false(self, mgr):
        neg = _open(mgr)
        mgr.agree(neg.negotiation_id)
        assert not mgr.fail(neg.negotiation_id)

    def test_agree_missing_returns_false(self, mgr):
        assert not mgr.agree("neg_99999")

    def test_custom_timestamp_agree(self, mgr):
        neg = _open(mgr)
        ts = datetime(2024, 5, 20)
        mgr.agree(neg.negotiation_id, ts=ts)
        assert neg.closed_at == ts

    def test_final_amount_set_after_agree(self, mgr):
        neg = mgr.open("p001", "A", asking_price=1000.0)
        mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 900.0)
        mgr.agree(neg.negotiation_id)
        assert neg.final_amount == 900.0

    def test_final_amount_none_when_active(self, mgr):
        neg = _open(mgr)
        assert neg.final_amount is None


# ── Discount / concession analytics ──────────────────────────────────────────

class TestDiscountAnalytics:
    def test_discount_pct_zero_when_no_offers(self, mgr):
        neg = mgr.open("p001", "A", asking_price=1000.0)
        assert neg.discount_pct == 0.0

    def test_discount_pct_after_offer(self, mgr):
        neg = mgr.open("p001", "A", asking_price=1000.0)
        mgr.add_offer(neg.negotiation_id, OfferParty.US, 900.0)
        assert neg.discount_pct == 10.0

    def test_discount_pct_never_negative(self, mgr):
        neg = mgr.open("p001", "A", asking_price=1000.0)
        mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 1100.0)
        assert neg.discount_pct == 0.0

    def test_total_concession_eur(self, mgr):
        neg = mgr.open("p001", "A", asking_price=1000.0)
        mgr.add_offer(neg.negotiation_id, OfferParty.US, 850.0)
        assert neg.total_concession_eur == 150.0

    def test_our_last_offer(self, mgr):
        neg = _open(mgr)
        mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 800.0)
        mgr.add_offer(neg.negotiation_id, OfferParty.US, 920.0)
        mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 900.0)
        assert neg.our_last_offer.amount == 920.0

    def test_prospect_last_offer(self, mgr):
        neg = _open(mgr)
        mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 800.0)
        mgr.add_offer(neg.negotiation_id, OfferParty.US, 920.0)
        mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 900.0)
        assert neg.prospect_last_offer.amount == 900.0

    def test_our_last_offer_none_if_no_offers_from_us(self, mgr):
        neg = _open(mgr)
        mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 800.0)
        assert neg.our_last_offer is None

    def test_round_deltas(self, mgr):
        neg = mgr.open("p001", "A", asking_price=1000.0)
        mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 900.0)
        mgr.add_offer(neg.negotiation_id, OfferParty.US, 950.0)
        deltas = neg.round_deltas()
        assert len(deltas) == 2
        assert deltas[0]["delta"] == -100.0
        assert deltas[1]["delta"] == 50.0


# ── Duration ──────────────────────────────────────────────────────────────────

class TestDuration:
    def test_duration_grows_when_active(self, mgr):
        ts_open = datetime(2024, 1, 1)
        neg = mgr.open("p001", "A", asking_price=1000.0, ts=ts_open)
        # Simulate 5 days later
        ts_close = datetime(2024, 1, 6)
        mgr.agree(neg.negotiation_id, ts=ts_close)
        assert neg.duration_days == 5.0

    def test_duration_freezes_after_close(self, mgr):
        ts = datetime(2024, 2, 1)
        neg = mgr.open("p001", "A", ts=ts)
        mgr.fail(neg.negotiation_id, ts=datetime(2024, 2, 4))
        d1 = neg.duration_days
        d2 = neg.duration_days
        assert d1 == d2 == 3.0


# ── Queries ───────────────────────────────────────────────────────────────────

class TestQueries:
    def test_active(self, mgr):
        n1 = _open(mgr)
        n2 = mgr.open("p002", "B", asking_price=500.0)
        mgr.agree(n2.negotiation_id)
        assert mgr.active() == [n1]

    def test_agreed(self, mgr):
        n1 = _open(mgr)
        mgr.agree(n1.negotiation_id)
        n2 = mgr.open("p002", "B", asking_price=500.0)
        assert mgr.agreed() == [n1]

    def test_failed_or_abandoned(self, mgr):
        n1 = _open(mgr)
        mgr.fail(n1.negotiation_id)
        n2 = mgr.open("p002", "B", asking_price=500.0)
        mgr.abandon(n2.negotiation_id)
        n3 = mgr.open("p003", "C", asking_price=200.0)
        results = mgr.failed_or_abandoned()
        assert n1 in results and n2 in results
        assert n3 not in results

    def test_by_status(self, mgr):
        n1 = _open(mgr)
        mgr.agree(n1.negotiation_id)
        n2 = mgr.open("p002", "B")
        assert mgr.by_status(NegotiationStatus.AGREED) == [n1]
        assert mgr.by_status(NegotiationStatus.OPENED) == [n2]

    def test_by_sector(self, mgr):
        mgr.open("p001", "A", sector="artisan")
        mgr.open("p002", "B", sector="juridique")
        mgr.open("p003", "C", sector="artisan spécialisé")
        results = mgr.by_sector("artisan")
        assert len(results) == 2

    def test_all_negotiations(self, mgr):
        _open(mgr, 3)
        assert len(mgr.all_negotiations()) == 3


# ── Aggregate analytics ───────────────────────────────────────────────────────

class TestAnalytics:
    def test_win_rate_zero_no_closed(self, mgr):
        _open(mgr)
        assert mgr.win_rate() == 0.0

    def test_win_rate_100_all_agreed(self, mgr):
        n1, n2 = _open(mgr, 2)
        mgr.agree(n1.negotiation_id)
        mgr.agree(n2.negotiation_id)
        assert mgr.win_rate() == 100.0

    def test_win_rate_50(self, mgr):
        n1, n2 = _open(mgr, 2)
        mgr.agree(n1.negotiation_id)
        mgr.fail(n2.negotiation_id)
        assert mgr.win_rate() == 50.0

    def test_average_discount_pct(self, mgr):
        n1 = mgr.open("p001", "A", asking_price=1000.0)
        n2 = mgr.open("p002", "B", asking_price=1000.0)
        mgr.add_offer(n1.negotiation_id, OfferParty.US, 900.0)  # -10%
        mgr.add_offer(n2.negotiation_id, OfferParty.US, 800.0)  # -20%
        mgr.agree(n1.negotiation_id)
        mgr.agree(n2.negotiation_id)
        assert mgr.average_discount_pct() == 15.0

    def test_average_discount_pct_zero_no_agreed(self, mgr):
        _open(mgr)
        assert mgr.average_discount_pct() == 0.0

    def test_average_rounds(self, mgr):
        n1 = _open(mgr)
        mgr.add_offer(n1.negotiation_id, OfferParty.PROSPECT, 900.0)
        mgr.add_offer(n1.negotiation_id, OfferParty.US, 950.0)  # 2 rounds
        n2 = mgr.open("p002", "B", asking_price=500.0)
        mgr.add_offer(n2.negotiation_id, OfferParty.PROSPECT, 400.0)  # 1 round
        assert mgr.average_rounds() == 1.5

    def test_total_agreed_revenue(self, mgr):
        n1 = mgr.open("p001", "A", asking_price=1000.0)
        n2 = mgr.open("p002", "B", asking_price=500.0)
        mgr.add_offer(n1.negotiation_id, OfferParty.US, 900.0)
        mgr.add_offer(n2.negotiation_id, OfferParty.US, 450.0)
        mgr.agree(n1.negotiation_id)
        mgr.agree(n2.negotiation_id)
        assert mgr.total_agreed_revenue() == 1350.0

    def test_total_conceded_eur(self, mgr):
        n1 = mgr.open("p001", "A", asking_price=1000.0)
        n2 = mgr.open("p002", "B", asking_price=600.0)
        mgr.add_offer(n1.negotiation_id, OfferParty.US, 950.0)   # -50
        mgr.add_offer(n2.negotiation_id, OfferParty.US, 540.0)   # -60
        mgr.agree(n1.negotiation_id)
        mgr.agree(n2.negotiation_id)
        assert mgr.total_conceded_eur() == 110.0

    def test_average_duration_days(self, mgr):
        ts = datetime(2024, 1, 1)
        n1 = mgr.open("p001", "A", asking_price=1000.0, ts=ts)
        mgr.agree(n1.negotiation_id, ts=datetime(2024, 1, 6))  # 5 days
        n2 = mgr.open("p002", "B", asking_price=500.0, ts=ts)
        mgr.fail(n2.negotiation_id, ts=datetime(2024, 1, 4))   # 3 days
        assert mgr.average_duration_days() == 4.0

    def test_sector_summary(self, mgr):
        n1 = mgr.open("p001", "A", sector="artisan", asking_price=1000.0)
        n2 = mgr.open("p002", "B", sector="artisan", asking_price=800.0)
        mgr.add_offer(n1.negotiation_id, OfferParty.US, 900.0)
        mgr.agree(n1.negotiation_id)
        result = mgr.sector_summary()
        assert "artisan" in result
        assert result["artisan"]["count"] == 2
        assert result["artisan"]["agreed"] == 1

    def test_failure_reason_summary(self, mgr):
        n1, n2 = _open(mgr, 2)
        mgr.fail(n1.negotiation_id, reason="budget")
        mgr.fail(n2.negotiation_id, reason="budget")
        reasons = mgr.failure_reason_summary()
        assert reasons.get("budget") == 2

    def test_failure_reason_unspecified(self, mgr):
        neg = _open(mgr)
        mgr.fail(neg.negotiation_id)
        reasons = mgr.failure_reason_summary()
        assert reasons.get("unspecified") == 1


# ── summary() ─────────────────────────────────────────────────────────────────

class TestSummary:
    def test_empty_summary(self, mgr):
        s = mgr.summary()
        assert s["total"] == 0
        assert s["win_rate_pct"] == 0.0

    def test_summary_counts(self, mgr):
        n1 = _open(mgr)
        n2 = mgr.open("p002", "B", asking_price=500.0)
        n3 = mgr.open("p003", "C", asking_price=200.0)
        mgr.agree(n1.negotiation_id)
        mgr.fail(n2.negotiation_id)
        s = mgr.summary()
        assert s["total"] == 3
        assert s["agreed"] == 1
        assert s["failed_or_abandoned"] == 1
        assert s["active"] == 1

    def test_summary_keys(self, mgr):
        s = mgr.summary()
        for key in ["total", "active", "agreed", "failed_or_abandoned", "win_rate_pct",
                    "avg_discount_pct", "avg_rounds", "avg_duration_days",
                    "total_agreed_eur", "total_conceded_eur"]:
            assert key in s


# ── to_dict ───────────────────────────────────────────────────────────────────

class TestToDict:
    def test_negotiation_to_dict(self, mgr):
        neg = mgr.open("p001", "ACME", "tech", asking_price=750.0)
        mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 650.0, note="Trop cher")
        d = neg.to_dict()
        assert d["negotiation_id"] == neg.negotiation_id
        assert d["company_name"] == "ACME"
        assert d["asking_price"] == 750.0
        assert d["current_amount"] == 650.0
        assert d["discount_pct"] == 13.3
        assert d["rounds"] == 1
        assert len(d["offers"]) == 1
        assert d["offers"][0]["note"] == "Trop cher"
        assert d["status"] == "in_progress"

    def test_offer_to_dict_keys(self, mgr):
        neg = _open(mgr)
        offer = mgr.add_offer(neg.negotiation_id, OfferParty.US, 900.0)
        d = offer.to_dict()
        for key in ["round_number", "party", "amount", "concession_type", "note", "proposed_at"]:
            assert key in d


# ── reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_records(self, mgr):
        _open(mgr, 3)
        assert len(mgr.all_negotiations()) == 3
        mgr.reset()
        assert len(mgr.all_negotiations()) == 0

    def test_reset_resets_counter(self, mgr):
        _open(mgr, 2)
        mgr.reset()
        neg = mgr.open("p001", "A", asking_price=100.0)
        assert neg.negotiation_id == "neg_00001"
