"""
Tests for intelligence/conversion_funnel.py
"""

import pytest
from datetime import datetime, timedelta
from intelligence.conversion_funnel import (
    ConversionFunnelTracker, FunnelRecord, FunnelStage, StageEntry,
    TransitionStats, STAGE_ORDER, TERMINAL_STAGES,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

T0 = datetime(2025, 3, 1, 9, 0, 0)


def tracker() -> ConversionFunnelTracker:
    return ConversionFunnelTracker()


def add(t: ConversionFunnelTracker, pid="p001", name="Acme", sector="artisan", ts=None):
    return t.add_prospect(pid, name, sector, ts=ts or T0)


def full_journey(t: ConversionFunnelTracker, pid="p001", quote=598.80):
    """Takes a prospect all the way to WON."""
    add(t, pid, ts=T0)
    for i, stage in enumerate([
        FunnelStage.CONTACTED,
        FunnelStage.OPENED,
        FunnelStage.REPLIED,
        FunnelStage.DEMO,
        FunnelStage.QUOTED,
        FunnelStage.NEGOTIATING,
        FunnelStage.WON,
    ]):
        ts_i = T0 + timedelta(days=i + 1)
        kw = {"quote_value": quote} if stage == FunnelStage.QUOTED else {}
        t.advance(pid, stage, ts=ts_i, **kw)


# ── Stage constants ───────────────────────────────────────────────────────────

class TestStageConstants:
    def test_stage_order_starts_with_lead(self):
        assert STAGE_ORDER[0] == FunnelStage.LEAD

    def test_stage_order_ends_with_won(self):
        assert STAGE_ORDER[-1] == FunnelStage.WON

    def test_terminal_stages_contain_won_lost(self):
        assert FunnelStage.WON  in TERMINAL_STAGES
        assert FunnelStage.LOST in TERMINAL_STAGES

    def test_lost_not_in_stage_order(self):
        assert FunnelStage.LOST not in STAGE_ORDER


# ── Add prospect ──────────────────────────────────────────────────────────────

class TestAddProspect:
    def test_add_returns_record(self):
        t = tracker()
        r = add(t)
        assert isinstance(r, FunnelRecord)

    def test_initial_stage_is_lead(self):
        t = tracker()
        r = add(t)
        assert r.current_stage == FunnelStage.LEAD

    def test_company_name_preserved(self):
        t = tracker()
        r = add(t, name="Garage Dupont")
        assert r.company_name == "Garage Dupont"

    def test_sector_preserved(self):
        t = tracker()
        r = add(t, sector="médical")
        assert r.sector == "médical"

    def test_get_returns_record(self):
        t = tracker()
        add(t, "p1")
        assert t.get("p1") is not None

    def test_get_unknown_returns_none(self):
        assert tracker().get("nope") is None

    def test_get_or_add_creates(self):
        t = tracker()
        r = t.get_or_add("p1", "Test Co")
        assert r.prospect_id == "p1"

    def test_get_or_add_returns_existing(self):
        t = tracker()
        r1 = add(t, "p1")
        r2 = t.get_or_add("p1")
        assert r1 is r2

    def test_initial_entries_has_lead(self):
        t = tracker()
        r = add(t)
        assert r.entries[0].stage == FunnelStage.LEAD


# ── Stage advancement ─────────────────────────────────────────────────────────

class TestAdvance:
    def test_advance_returns_true(self):
        t = tracker()
        add(t, "p1")
        assert t.advance("p1", FunnelStage.CONTACTED) is True

    def test_advance_updates_stage(self):
        t = tracker()
        add(t, "p1")
        t.advance("p1", FunnelStage.CONTACTED)
        assert t.get("p1").current_stage == FunnelStage.CONTACTED

    def test_advance_unknown_prospect(self):
        assert tracker().advance("nope", FunnelStage.CONTACTED) is False

    def test_advance_sets_quote_value(self):
        t = tracker()
        add(t, "p1")
        t.advance("p1", FunnelStage.QUOTED, quote_value=1199.0)
        assert t.get("p1").quote_value == pytest.approx(1199.0)

    def test_advance_creates_entry(self):
        t = tracker()
        add(t, "p1")
        t.advance("p1", FunnelStage.CONTACTED)
        rec = t.get("p1")
        assert len(rec.entries) == 2
        assert rec.entries[-1].stage == FunnelStage.CONTACTED

    def test_advance_closes_previous_entry(self):
        t = tracker()
        add(t, "p1", ts=T0)
        t.advance("p1", FunnelStage.CONTACTED, ts=T0 + timedelta(hours=2))
        rec = t.get("p1")
        assert rec.entries[0].exited_at is not None

    def test_mark_won(self):
        t = tracker()
        add(t, "p1")
        t.mark_won("p1", quote_value=799.0)
        assert t.get("p1").is_won

    def test_mark_lost(self):
        t = tracker()
        add(t, "p1")
        t.mark_lost("p1")
        assert t.get("p1").is_lost

    def test_is_active_after_advance(self):
        t = tracker()
        add(t, "p1")
        t.advance("p1", FunnelStage.QUOTED)
        assert t.get("p1").is_active

    def test_is_not_active_after_won(self):
        t = tracker()
        add(t, "p1")
        t.mark_won("p1")
        assert not t.get("p1").is_active


# ── Stage queries ─────────────────────────────────────────────────────────────

class TestStageQueries:
    def test_by_stage(self):
        t = tracker()
        add(t, "p1")
        add(t, "p2")
        t.advance("p1", FunnelStage.CONTACTED)
        assert len(t.by_stage(FunnelStage.LEAD)) == 1
        assert len(t.by_stage(FunnelStage.CONTACTED)) == 1

    def test_active_excludes_terminal(self):
        t = tracker()
        add(t, "p1")
        add(t, "p2")
        t.mark_won("p1")
        t.mark_lost("p2")
        assert len(t.active()) == 0

    def test_won_returns_correct(self):
        t = tracker()
        add(t, "p1")
        add(t, "p2")
        t.mark_won("p1")
        assert len(t.won()) == 1
        assert t.won()[0].prospect_id == "p1"

    def test_lost_returns_correct(self):
        t = tracker()
        add(t, "p1")
        t.mark_lost("p1")
        assert len(t.lost()) == 1

    def test_by_sector(self):
        t = tracker()
        add(t, "p1", sector="restaurant gastronomique")
        add(t, "p2", sector="artisan")
        assert len(t.by_sector("restaurant")) == 1
        assert len(t.by_sector("artisan")) == 1

    def test_all_records(self):
        t = tracker()
        add(t, "p1")
        add(t, "p2")
        assert len(t.all_records()) == 2


# ── Stage entry duration ──────────────────────────────────────────────────────

class TestStageDuration:
    def test_duration_hours_after_exit(self):
        t = tracker()
        add(t, "p1", ts=T0)
        t.advance("p1", FunnelStage.CONTACTED, ts=T0 + timedelta(hours=48))
        rec = t.get("p1")
        assert rec.entries[0].duration_hours == pytest.approx(48.0)

    def test_duration_none_while_in_stage(self):
        t = tracker()
        add(t, "p1", ts=T0)
        rec = t.get("p1")
        assert rec.entries[0].duration_hours is None

    def test_time_in_stage(self):
        t = tracker()
        add(t, "p1", ts=T0)
        t.advance("p1", FunnelStage.CONTACTED, ts=T0 + timedelta(hours=24))
        rec = t.get("p1")
        hours = rec.time_in_stage(FunnelStage.LEAD)
        assert hours == pytest.approx(24.0)

    def test_time_in_stage_not_reached(self):
        t = tracker()
        add(t, "p1")
        assert t.get("p1").time_in_stage(FunnelStage.QUOTED) is None

    def test_days_in_funnel(self):
        t = tracker()
        add(t, "p1", ts=T0)
        t.mark_won("p1", ts=T0 + timedelta(days=14))
        assert t.get("p1").days_in_funnel == pytest.approx(14.0, abs=0.1)

    def test_stage_entry_to_dict(self):
        t = tracker()
        add(t, "p1", ts=T0)
        t.advance("p1", FunnelStage.CONTACTED, ts=T0 + timedelta(hours=2))
        d = t.get("p1").entries[0].to_dict()
        for key in ("stage", "entered_at", "exited_at", "duration_hours"):
            assert key in d


# ── Stages reached ────────────────────────────────────────────────────────────

class TestStagesReached:
    def test_stages_reached_after_journey(self):
        t = tracker()
        full_journey(t)
        reached = t.get("p001").stages_reached
        assert FunnelStage.LEAD in reached
        assert FunnelStage.WON  in reached

    def test_stages_reached_only_lead_at_start(self):
        t = tracker()
        add(t, "p1")
        assert t.get("p1").stages_reached == [FunnelStage.LEAD]


# ── Analytics ─────────────────────────────────────────────────────────────────

class TestAnalytics:
    def test_stage_counts(self):
        t = tracker()
        add(t, "p1")
        add(t, "p2")
        t.advance("p1", FunnelStage.CONTACTED)
        counts = t.stage_counts()
        assert counts.get("lead", 0) == 1
        assert counts.get("contacted", 0) == 1

    def test_stage_report_length(self):
        t = tracker()
        add(t, "p1")
        report = t.stage_report()
        assert len(report) == len(STAGE_ORDER) - 1

    def test_stage_report_has_transition_stats(self):
        t = tracker()
        full_journey(t)
        report = t.stage_report()
        lead_to_contacted = next(r for r in report if r.from_stage == FunnelStage.LEAD)
        assert lead_to_contacted.prospects_entered == 1
        assert lead_to_contacted.prospects_converted == 1
        assert lead_to_contacted.conversion_rate == pytest.approx(1.0)

    def test_overall_conversion_rate_zero(self):
        t = tracker()
        add(t, "p1")
        assert t.overall_conversion_rate() == pytest.approx(0.0)

    def test_overall_conversion_rate_full(self):
        t = tracker()
        full_journey(t)
        assert t.overall_conversion_rate() == pytest.approx(1.0)

    def test_total_pipeline_value(self):
        t = tracker()
        add(t, "p1")
        add(t, "p2")
        t.advance("p1", FunnelStage.QUOTED, quote_value=1000.0)
        t.advance("p2", FunnelStage.QUOTED, quote_value=500.0)
        assert t.total_pipeline_value() == pytest.approx(1500.0)

    def test_won_not_in_pipeline(self):
        t = tracker()
        add(t, "p1")
        t.mark_won("p1", quote_value=1000.0)
        assert t.total_pipeline_value() == pytest.approx(0.0)

    def test_total_won_revenue(self):
        t = tracker()
        full_journey(t, "p001", quote=598.80)
        full_journey(t, "p002", quote=958.80)
        assert t.total_won_revenue() == pytest.approx(598.80 + 958.80, abs=0.01)

    def test_average_deal_size(self):
        t = tracker()
        full_journey(t, "p001", quote=600.0)
        full_journey(t, "p002", quote=400.0)
        assert t.average_deal_size() == pytest.approx(500.0)

    def test_average_days_to_close(self):
        t = tracker()
        full_journey(t, "p001")  # closes in 7 days (7 advances after T0)
        days = t.average_days_to_close()
        assert days > 0

    def test_top_prospects(self):
        t = tracker()
        add(t, "p1")
        add(t, "p2")
        t.advance("p1", FunnelStage.QUOTED, quote_value=2000.0)
        t.advance("p2", FunnelStage.QUOTED, quote_value=1000.0)
        top = t.top_prospects(n=2)
        assert top[0].prospect_id == "p1"

    def test_sector_summary(self):
        t = tracker()
        add(t, "p1", sector="artisan")
        add(t, "p2", sector="artisan")
        t.mark_won("p1", quote_value=500.0)
        s = t.sector_summary()
        assert s["artisan"]["count"] == 2
        assert s["artisan"]["won"] == 1
        assert s["artisan"]["revenue"] == pytest.approx(500.0)

    def test_average_time_per_stage(self):
        t = tracker()
        add(t, "p1", ts=T0)
        t.advance("p1", FunnelStage.CONTACTED, ts=T0 + timedelta(hours=24))
        avg = t.average_time_per_stage()
        assert avg.get("lead") == pytest.approx(24.0)


# ── Summary ───────────────────────────────────────────────────────────────────

class TestSummary:
    def test_empty_summary(self):
        s = tracker().summary()
        assert s["total_prospects"] == 0
        assert s["overall_cvr_pct"] == 0.0

    def test_summary_after_won(self):
        t = tracker()
        full_journey(t, "p001", quote=1000.0)
        add(t, "p002")
        s = t.summary()
        assert s["total_prospects"] == 2
        assert s["won"] == 1
        assert s["active"] == 1
        assert s["total_won_eur"] == pytest.approx(1000.0)
        assert s["overall_cvr_pct"] == pytest.approx(50.0)

    def test_summary_has_keys(self):
        s = tracker().summary()
        for key in ("total_prospects", "active", "won", "lost",
                    "overall_cvr_pct", "total_pipeline_eur",
                    "total_won_eur", "avg_deal_size_eur",
                    "avg_days_to_close", "stage_counts"):
            assert key in s

    def test_funnel_record_to_dict(self):
        t = tracker()
        add(t, "p1")
        d = t.get("p1").to_dict()
        for key in ("prospect_id", "company_name", "sector", "current_stage",
                    "quote_value", "is_active", "days_in_funnel",
                    "stages_reached", "entries"):
            assert key in d

    def test_transition_stats_to_dict(self):
        t = tracker()
        full_journey(t)
        report = t.stage_report()
        d = report[0].to_dict()
        for key in ("from_stage", "to_stage", "prospects_entered",
                    "prospects_converted", "conversion_rate_pct",
                    "drop_off_rate_pct"):
            assert key in d


# ── Reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_records(self):
        t = tracker()
        add(t, "p1")
        t.reset()
        assert t.get("p1") is None

    def test_reset_allows_fresh_start(self):
        t = tracker()
        full_journey(t)
        t.reset()
        add(t, "p1")
        assert t.summary()["total_prospects"] == 1
        assert t.summary()["won"] == 0
