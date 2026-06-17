"""
Tests for intelligence/objection_handler.py
"""

import pytest
from intelligence.objection_handler import (
    ObjectionHandler, ObjectionType, RebuttalOutcome,
    Rebuttal, OutcomeRecord, _REBUTTALS, _BY_OBJECTION, _REBUTTAL_INDEX,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def handler() -> ObjectionHandler:
    return ObjectionHandler()


def record(h: ObjectionHandler, rebuttal_id: str, prospect_id: str, objection: str,
           outcome: str, sector: str = "") -> OutcomeRecord:
    return h.record_outcome(rebuttal_id, prospect_id, objection, outcome, sector=sector)


# ── Rebuttal catalogue ────────────────────────────────────────────────────────

class TestRebuttalCatalogue:
    def test_at_least_12_rebuttals(self):
        assert len(_REBUTTALS) >= 12

    def test_all_objection_types_covered(self):
        covered = {r.objection for r in _REBUTTALS}
        for obj_type in ObjectionType:
            assert obj_type in covered, f"{obj_type} has no rebuttal"

    def test_rebuttal_index_complete(self):
        for r in _REBUTTALS:
            assert r.rebuttal_id in _REBUTTAL_INDEX

    def test_by_objection_grouping(self):
        for obj_type, rebuttals in _BY_OBJECTION.items():
            assert all(r.objection == obj_type for r in rebuttals)

    def test_price_has_multiple_rebuttals(self):
        assert len(_BY_OBJECTION.get(ObjectionType.PRICE, [])) >= 2

    def test_trust_has_multiple_rebuttals(self):
        assert len(_BY_OBJECTION.get(ObjectionType.TRUST, [])) >= 2

    def test_rebuttal_has_talking_points(self):
        for r in _REBUTTALS:
            assert len(r.talking_points) >= 1

    def test_rebuttal_to_dict_has_keys(self):
        r = _REBUTTALS[0]
        d = r.to_dict()
        for key in ("rebuttal_id", "objection", "name", "template_id",
                    "talking_points", "urgency_angle", "social_proof"):
            assert key in d


# ── Catalogue access ──────────────────────────────────────────────────────────

class TestCatalogueAccess:
    def test_get_rebuttal_by_id(self):
        h = handler()
        r = h.get_rebuttal("price_roi")
        assert r is not None
        assert r.rebuttal_id == "price_roi"

    def test_get_unknown_rebuttal_none(self):
        assert handler().get_rebuttal("nonexistent") is None

    def test_rebuttals_for_price(self):
        rebuttals = handler().rebuttals_for(ObjectionType.PRICE)
        assert len(rebuttals) >= 2
        assert all(r.objection == ObjectionType.PRICE for r in rebuttals)

    def test_rebuttals_for_unknown_type(self):
        rebuttals = handler().rebuttals_for(ObjectionType.UNKNOWN)
        assert len(rebuttals) >= 1

    def test_all_rebuttals_returns_full_list(self):
        assert len(handler().all_rebuttals()) == len(_REBUTTALS)


# ── Recommendation (no history) ───────────────────────────────────────────────

class TestRecommendationNoHistory:
    def test_recommend_price_returns_rebuttal(self):
        r = handler().recommend("price")
        assert r is not None
        assert r.objection == ObjectionType.PRICE

    def test_recommend_timing_returns_rebuttal(self):
        r = handler().recommend("timing")
        assert r is not None
        assert r.objection == ObjectionType.TIMING

    def test_recommend_unknown_string_returns_unknown_rebuttal(self):
        r = handler().recommend("zorgblorf")
        assert r is not None
        assert r.objection == ObjectionType.UNKNOWN

    def test_recommend_enum_value(self):
        r = handler().recommend(ObjectionType.TRUST)
        assert r is not None
        assert r.objection == ObjectionType.TRUST

    def test_recommend_with_exclude(self):
        h = handler()
        first = h.recommend("price")
        second = h.recommend("price", exclude_ids=[first.rebuttal_id])
        assert second is None or second.rebuttal_id != first.rebuttal_id

    def test_recommend_sequence_returns_list(self):
        h = handler()
        seq = h.recommend_sequence("price")
        assert isinstance(seq, list)
        assert len(seq) >= 2
        assert all(r.objection == ObjectionType.PRICE for r in seq)


# ── Recommendation (with history) ────────────────────────────────────────────

class TestRecommendationWithHistory:
    def test_winning_rebuttal_ranked_first(self):
        h = handler()
        # Record many wins for price_roi
        for i in range(5):
            record(h, "price_roi", f"p{i}", "price", "positive")
        # Record losses for price_payment_plan
        for i in range(5, 10):
            record(h, "price_payment_plan", f"p{i}", "price", "negative")

        recommended = h.recommend("price")
        assert recommended.rebuttal_id == "price_roi"

    def test_sector_specific_wins_preferred(self):
        h = handler()
        # Many wins for price_roi in restaurant sector
        for i in range(4):
            record(h, "price_roi", f"p{i}", "price", "positive", sector="restaurant")
        # Global wins for price_payment_plan
        for i in range(4, 10):
            record(h, "price_payment_plan", f"p{i}", "price", "positive")

        # In restaurant context, price_roi should still win
        recommended = h.recommend("price", sector="restaurant")
        assert recommended.rebuttal_id == "price_roi"

    def test_converted_counts_as_win(self):
        h = handler()
        record(h, "price_roi", "p1", "price", "converted")
        report = h.effectiveness_report()
        roi_row = next(r for r in report if r["rebuttal_id"] == "price_roi")
        assert roi_row["wins"] == 1

    def test_negative_does_not_count_as_win(self):
        h = handler()
        record(h, "price_roi", "p1", "price", "negative")
        report = h.effectiveness_report()
        roi_row = next(r for r in report if r["rebuttal_id"] == "price_roi")
        assert roi_row["wins"] == 0


# ── Record outcome ────────────────────────────────────────────────────────────

class TestRecordOutcome:
    def test_returns_outcome_record(self):
        h = handler()
        rec = record(h, "price_roi", "p1", "price", "positive")
        assert isinstance(rec, OutcomeRecord)

    def test_outcome_stored(self):
        h = handler()
        record(h, "price_roi", "p1", "price", "positive")
        assert len(h.outcomes_for("price_roi")) == 1

    def test_invalid_outcome_defaults_to_neutral(self):
        h = handler()
        rec = record(h, "price_roi", "p1", "price", "zorg_blorf")
        assert rec.outcome == RebuttalOutcome.NEUTRAL

    def test_invalid_objection_defaults_to_unknown(self):
        h = handler()
        rec = record(h, "unknown_open_question", "p1", "zorgblorf", "positive")
        assert rec.objection == ObjectionType.UNKNOWN

    def test_sector_preserved(self):
        h = handler()
        rec = record(h, "price_roi", "p1", "price", "positive", sector="médical")
        assert rec.sector == "médical"

    def test_multiple_records(self):
        h = handler()
        record(h, "price_roi", "p1", "price", "positive")
        record(h, "price_roi", "p2", "price", "negative")
        record(h, "price_roi", "p3", "price", "neutral")
        assert len(h.outcomes_for("price_roi")) == 3

    def test_outcomes_for_unknown_rebuttal_empty(self):
        assert handler().outcomes_for("nonexistent") == []

    def test_to_dict_has_keys(self):
        h = handler()
        rec = record(h, "price_roi", "p1", "price", "positive", sector="restaurant")
        d = rec.to_dict()
        for key in ("rebuttal_id", "prospect_id", "objection", "outcome", "sector"):
            assert key in d


# ── Effectiveness report ──────────────────────────────────────────────────────

class TestEffectivenessReport:
    def test_report_covers_all_rebuttals(self):
        h = handler()
        report = h.effectiveness_report()
        assert len(report) == len(_REBUTTALS)

    def test_report_sorted_by_win_rate_desc(self):
        h = handler()
        record(h, "price_roi", "p1", "price", "positive")
        record(h, "price_roi", "p2", "price", "positive")
        record(h, "price_payment_plan", "p3", "price", "negative")
        report = h.effectiveness_report()
        rates = [r["win_rate_pct"] for r in report]
        assert rates == sorted(rates, reverse=True)

    def test_no_history_all_zeros(self):
        h = handler()
        report = h.effectiveness_report()
        assert all(r["win_rate_pct"] == 0.0 for r in report)

    def test_report_has_required_keys(self):
        h = handler()
        record(h, "price_roi", "p1", "price", "positive")
        row = next(r for r in h.effectiveness_report() if r["rebuttal_id"] == "price_roi")
        for key in ("rebuttal_id", "objection", "name", "total", "wins", "win_rate_pct"):
            assert key in row

    def test_win_rate_calculation(self):
        h = handler()
        record(h, "price_roi", "p1", "price", "positive")
        record(h, "price_roi", "p2", "price", "positive")
        record(h, "price_roi", "p3", "price", "negative")
        record(h, "price_roi", "p4", "price", "neutral")
        row = next(r for r in h.effectiveness_report() if r["rebuttal_id"] == "price_roi")
        assert row["total"] == 4
        assert row["wins"] == 2
        assert row["win_rate_pct"] == pytest.approx(50.0)


# ── Summary ───────────────────────────────────────────────────────────────────

class TestSummary:
    def test_empty_summary(self):
        s = handler().summary()
        assert s["total_outcomes"] == 0
        assert s["win_rate_pct"] == 0.0

    def test_summary_after_outcomes(self):
        h = handler()
        record(h, "price_roi", "p1", "price", "positive")
        record(h, "trust_free_audit", "p2", "trust", "converted")
        record(h, "timing_now_or_never", "p3", "timing", "negative")
        s = h.summary()
        assert s["total_outcomes"] == 3
        assert s["wins"] == 2

    def test_summary_win_rate(self):
        h = handler()
        for _ in range(3):
            record(h, "price_roi", "p1", "price", "positive")
        record(h, "price_roi", "p2", "price", "negative")
        s = h.summary()
        assert s["win_rate_pct"] == pytest.approx(75.0)

    def test_summary_by_objection(self):
        h = handler()
        record(h, "price_roi", "p1", "price", "positive")
        record(h, "price_roi", "p2", "price", "positive")
        record(h, "trust_free_audit", "p3", "trust", "neutral")
        s = h.summary()
        assert s["by_objection"].get("price", 0) == 2
        assert s["by_objection"].get("trust", 0) == 1

    def test_summary_by_outcome(self):
        h = handler()
        record(h, "price_roi", "p1", "price", "positive")
        record(h, "price_roi", "p2", "price", "negative")
        record(h, "trust_free_audit", "p3", "trust", "converted")
        s = h.summary()
        assert s["by_outcome"].get("positive", 0) == 1
        assert s["by_outcome"].get("negative", 0) == 1
        assert s["by_outcome"].get("converted", 0) == 1

    def test_summary_has_keys(self):
        s = handler().summary()
        for key in ("total_outcomes", "wins", "win_rate_pct",
                    "by_objection", "by_outcome", "rebuttals_count"):
            assert key in s

    def test_rebuttals_count_in_summary(self):
        assert handler().summary()["rebuttals_count"] == len(_REBUTTALS)


# ── Reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_outcomes(self):
        h = handler()
        record(h, "price_roi", "p1", "price", "positive")
        h.reset()
        assert len(h.outcomes_for("price_roi")) == 0

    def test_reset_clears_summary(self):
        h = handler()
        record(h, "price_roi", "p1", "price", "positive")
        h.reset()
        assert h.summary()["total_outcomes"] == 0

    def test_reset_preserves_catalogue(self):
        h = handler()
        h.reset()
        assert h.get_rebuttal("price_roi") is not None
        assert len(h.all_rebuttals()) == len(_REBUTTALS)

    def test_reset_allows_fresh_history(self):
        h = handler()
        record(h, "price_roi", "p1", "price", "negative")
        h.reset()
        record(h, "price_roi", "p2", "price", "positive")
        s = h.summary()
        assert s["total_outcomes"] == 1
        assert s["wins"] == 1
