"""
Tests for intelligence/campaign_scheduler.py
"""

import datetime
import pytest
from intelligence.campaign_scheduler import (
    CampaignScheduler, CampaignWave, CampaignPlan,
    MAX_PER_HOUR, MAX_PER_SECTOR_PER_WAVE, MIN_HOURS_BETWEEN_WAVES,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def sched() -> CampaignScheduler:
    s = CampaignScheduler()
    s.reset()
    return s


FIXED_START = datetime.datetime(2026, 1, 5, 8, 0, 0)  # Monday 08:00


# ── Constants ─────────────────────────────────────────────────────────────────

class TestConstants:
    def test_max_per_hour(self):
        assert MAX_PER_HOUR == 150

    def test_max_per_wave(self):
        assert MAX_PER_SECTOR_PER_WAVE == 50

    def test_min_hours_between_waves(self):
        assert MIN_HOURS_BETWEEN_WAVES == 4


# ── CampaignWave ──────────────────────────────────────────────────────────────

class TestCampaignWave:
    def _wave(self):
        return CampaignWave(
            wave_id="plan_abc_w1",
            sector="artisan",
            agent_id="2.1",
            email_count=30,
            scheduled_at=FIXED_START,
            priority="high",
            tier_filter="A",
        )

    def test_default_status_pending(self):
        assert self._wave().status == "pending"

    def test_to_dict_keys(self):
        d = self._wave().to_dict()
        for key in ("wave_id", "sector", "agent_id", "email_count",
                    "scheduled_at", "priority", "tier_filter", "status"):
            assert key in d

    def test_to_dict_scheduled_at_isoformat(self):
        d = self._wave().to_dict()
        assert "T" in d["scheduled_at"]  # ISO 8601

    def test_to_dict_email_count(self):
        assert self._wave().to_dict()["email_count"] == 30


# ── CampaignPlan ──────────────────────────────────────────────────────────────

class TestCampaignPlan:
    def _plan(self):
        wave = CampaignWave("p_w1", "restaurant", "2.1", 20, FIXED_START, "normal", "A")
        return CampaignPlan(
            plan_id="plan_test",
            created_at=FIXED_START,
            total_emails=20,
            total_waves=1,
            waves=[wave],
        )

    def test_to_dict_keys(self):
        d = self._plan().to_dict()
        for key in ("plan_id", "created_at", "total_emails", "total_waves", "waves"):
            assert key in d

    def test_to_dict_waves_list(self):
        d = self._plan().to_dict()
        assert isinstance(d["waves"], list)
        assert len(d["waves"]) == 1

    def test_to_dict_waves_are_dicts(self):
        d = self._plan().to_dict()
        assert isinstance(d["waves"][0], dict)


# ── plan() — basic ────────────────────────────────────────────────────────────

class TestPlanBasic:
    def test_returns_campaign_plan(self):
        s = sched()
        plan = s.plan("artisan", 30, "2.1", start_from=FIXED_START)
        assert isinstance(plan, CampaignPlan)

    def test_single_wave_for_small_volume(self):
        plan = sched().plan("artisan", 20, "2.1", start_from=FIXED_START)
        assert plan.total_waves == 1
        assert len(plan.waves) == 1

    def test_total_emails_matches_request(self):
        plan = sched().plan("artisan", 45, "2.1", start_from=FIXED_START)
        assert plan.total_emails == 45

    def test_wave_email_count_correct(self):
        plan = sched().plan("artisan", 30, "2.1", start_from=FIXED_START)
        assert plan.waves[0].email_count == 30

    def test_wave_sector_assigned(self):
        plan = sched().plan("artisan", 10, "2.1", start_from=FIXED_START)
        assert plan.waves[0].sector == "artisan"

    def test_wave_agent_id_assigned(self):
        plan = sched().plan("restaurant", 10, "3.2", start_from=FIXED_START)
        assert plan.waves[0].agent_id == "3.2"

    def test_plan_stored_in_scheduler(self):
        s = sched()
        plan = s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        assert s.get_plan(plan.plan_id) is not None

    def test_plan_id_starts_with_plan(self):
        plan = sched().plan("artisan", 10, "2.1", start_from=FIXED_START)
        assert plan.plan_id.startswith("plan_")

    def test_default_tier_filter_is_A(self):
        plan = sched().plan("artisan", 10, "2.1", start_from=FIXED_START)
        assert plan.waves[0].tier_filter == "A"

    def test_custom_tier_filter(self):
        plan = sched().plan("artisan", 10, "2.1", tier_filter="B", start_from=FIXED_START)
        assert plan.waves[0].tier_filter == "B"

    def test_default_priority_normal(self):
        plan = sched().plan("artisan", 10, "2.1", start_from=FIXED_START)
        assert plan.waves[0].priority == "normal"

    def test_custom_priority_urgent(self):
        plan = sched().plan("artisan", 10, "2.1", priority="urgent", start_from=FIXED_START)
        assert plan.waves[0].priority == "urgent"


# ── plan() — multi-wave batching ──────────────────────────────────────────────

class TestPlanMultiWave:
    def test_two_waves_for_51_leads(self):
        plan = sched().plan("artisan", 51, "2.1", start_from=FIXED_START)
        assert plan.total_waves == 2
        assert len(plan.waves) == 2

    def test_first_wave_full_batch(self):
        plan = sched().plan("artisan", 51, "2.1", start_from=FIXED_START)
        assert plan.waves[0].email_count == 50

    def test_second_wave_remainder(self):
        plan = sched().plan("artisan", 51, "2.1", start_from=FIXED_START)
        assert plan.waves[1].email_count == 1

    def test_three_waves_for_120_leads(self):
        plan = sched().plan("restaurant", 120, "2.1", start_from=FIXED_START)
        assert plan.total_waves == 3

    def test_wave_counts_sum_to_total(self):
        plan = sched().plan("restaurant", 130, "2.1", start_from=FIXED_START)
        total = sum(w.email_count for w in plan.waves)
        assert total == 130

    def test_wave_ids_sequential(self):
        plan = sched().plan("artisan", 60, "2.1", start_from=FIXED_START)
        assert plan.waves[0].wave_id.endswith("_w1")
        assert plan.waves[1].wave_id.endswith("_w2")

    def test_second_wave_later_than_first(self):
        plan = sched().plan("artisan", 60, "2.1", start_from=FIXED_START)
        assert plan.waves[1].scheduled_at > plan.waves[0].scheduled_at

    def test_min_gap_between_waves(self):
        s = CampaignScheduler(min_gap_hours=4)
        plan = s.plan("artisan", 60, "2.1", start_from=FIXED_START)
        gap = (plan.waves[1].scheduled_at - plan.waves[0].scheduled_at).total_seconds() / 3600
        assert gap >= 4


# ── plan() — send window logic ────────────────────────────────────────────────

class TestSendWindowLogic:
    def test_scheduled_time_is_datetime(self):
        plan = sched().plan("artisan", 10, "2.1", start_from=FIXED_START)
        assert isinstance(plan.waves[0].scheduled_at, datetime.datetime)

    def test_default_start_from_is_utcnow(self):
        before = datetime.datetime.utcnow()
        plan = sched().plan("artisan", 10, "2.1")
        after = datetime.datetime.utcnow()
        assert before <= plan.waves[0].scheduled_at <= after + datetime.timedelta(days=7)

    def test_unknown_sector_uses_default_window(self):
        plan = sched().plan("unknown_xyz", 10, "2.1", start_from=FIXED_START)
        assert isinstance(plan.waves[0].scheduled_at, datetime.datetime)

    def test_sector_window_respected_hour(self):
        # Artisan windows: [(1, 7), (2, 7), (3, 8)] — Tue-Thu
        # FIXED_START is Monday 08:00 → next artisan window should be Tue at 07:00
        plan = sched().plan("artisan", 10, "2.1", start_from=FIXED_START)
        scheduled = plan.waves[0].scheduled_at
        assert scheduled.weekday() in {1, 2, 3}  # Tue, Wed, Thu

    def test_restaurant_sector_window(self):
        # restaurant: [(1, 9), (2, 9), (0, 8)] — Mon/Tue/Wed
        plan = sched().plan("restaurant", 10, "2.1", start_from=FIXED_START)
        scheduled = plan.waves[0].scheduled_at
        assert scheduled.weekday() in {0, 1, 2}

    def test_minutes_zeroed_in_window(self):
        plan = sched().plan("artisan", 10, "2.1", start_from=FIXED_START)
        assert plan.waves[0].scheduled_at.minute == 0
        assert plan.waves[0].scheduled_at.second == 0


# ── get_plan / list_plans ─────────────────────────────────────────────────────

class TestGetListPlans:
    def test_get_plan_returns_plan(self):
        s = sched()
        plan = s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        assert s.get_plan(plan.plan_id) is plan

    def test_get_plan_unknown_returns_none(self):
        assert sched().get_plan("nonexistent") is None

    def test_list_plans_empty_initially(self):
        assert sched().list_plans() == []

    def test_list_plans_returns_all(self):
        s = sched()
        s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        s.plan("restaurant", 20, "2.2", start_from=FIXED_START)
        assert len(s.list_plans()) == 2


# ── cancel_wave / mark_wave_done ──────────────────────────────────────────────

class TestWaveStatusManagement:
    def test_cancel_wave_returns_true(self):
        s = sched()
        plan = s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        wave = plan.waves[0]
        assert s.cancel_wave(plan.plan_id, wave.wave_id) is True

    def test_cancel_wave_sets_status(self):
        s = sched()
        plan = s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        wave = plan.waves[0]
        s.cancel_wave(plan.plan_id, wave.wave_id)
        assert wave.status == "cancelled"

    def test_cancel_wave_unknown_plan_false(self):
        assert sched().cancel_wave("bad_plan", "bad_wave") is False

    def test_cancel_wave_unknown_wave_false(self):
        s = sched()
        plan = s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        assert s.cancel_wave(plan.plan_id, "bad_wave") is False

    def test_mark_wave_done_returns_true(self):
        s = sched()
        plan = s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        wave = plan.waves[0]
        assert s.mark_wave_done(plan.plan_id, wave.wave_id) is True

    def test_mark_wave_done_sets_status(self):
        s = sched()
        plan = s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        wave = plan.waves[0]
        s.mark_wave_done(plan.plan_id, wave.wave_id)
        assert wave.status == "done"

    def test_mark_wave_done_unknown_plan_false(self):
        assert sched().mark_wave_done("bad_plan", "bad_wave") is False


# ── pending_waves ─────────────────────────────────────────────────────────────

class TestPendingWaves:
    def test_no_pending_waves_before_schedule(self):
        s = sched()
        future = FIXED_START + datetime.timedelta(days=30)
        s.plan("artisan", 10, "2.1", start_from=future)
        now = FIXED_START
        assert s.pending_waves(as_of=now) == []

    def test_pending_waves_returns_due(self):
        s = sched()
        plan = s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        # scheduled_at is some time after FIXED_START — check far future
        far_future = FIXED_START + datetime.timedelta(days=100)
        pending = s.pending_waves(as_of=far_future)
        assert len(pending) == 1

    def test_pending_waves_excludes_done(self):
        s = sched()
        plan = s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        wave = plan.waves[0]
        s.mark_wave_done(plan.plan_id, wave.wave_id)
        far_future = FIXED_START + datetime.timedelta(days=100)
        assert s.pending_waves(as_of=far_future) == []

    def test_pending_waves_excludes_cancelled(self):
        s = sched()
        plan = s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        wave = plan.waves[0]
        s.cancel_wave(plan.plan_id, wave.wave_id)
        far_future = FIXED_START + datetime.timedelta(days=100)
        assert s.pending_waves(as_of=far_future) == []

    def test_pending_waves_sorted_by_scheduled_at(self):
        s = sched()
        s.plan("artisan", 60, "2.1", start_from=FIXED_START)
        far_future = FIXED_START + datetime.timedelta(days=100)
        pending = s.pending_waves(as_of=far_future)
        times = [w.scheduled_at for w in pending]
        assert times == sorted(times)

    def test_pending_waves_uses_utcnow_default(self):
        s = sched()
        s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        # should not raise
        _ = s.pending_waves()


# ── plan_multi_sector ─────────────────────────────────────────────────────────

class TestPlanMultiSector:
    def test_returns_list_of_plans(self):
        s = sched()
        plans = s.plan_multi_sector(
            {"artisan": 30, "restaurant": 20},
            start_from=FIXED_START,
        )
        assert isinstance(plans, list)
        assert len(plans) == 2

    def test_plan_count_matches_sectors(self):
        s = sched()
        plans = s.plan_multi_sector(
            {"artisan": 30, "restaurant": 20, "médical": 10},
            start_from=FIXED_START,
        )
        assert len(plans) == 3

    def test_higher_volume_scheduled_first(self):
        s = sched()
        plans = s.plan_multi_sector(
            {"artisan": 80, "restaurant": 10},
            start_from=FIXED_START,
        )
        # Artisan has higher volume → first plan
        assert plans[0].total_emails == 80

    def test_agent_assignment_respected(self):
        s = sched()
        plans = s.plan_multi_sector(
            {"artisan": 20},
            agent_assignments={"artisan": "3.7"},
            start_from=FIXED_START,
        )
        assert plans[0].waves[0].agent_id == "3.7"

    def test_default_agent_when_no_assignment(self):
        s = sched()
        plans = s.plan_multi_sector(
            {"artisan": 20},
            start_from=FIXED_START,
        )
        assert plans[0].waves[0].agent_id == "2.1"

    def test_all_plans_stored(self):
        s = sched()
        plans = s.plan_multi_sector(
            {"artisan": 30, "restaurant": 20},
            start_from=FIXED_START,
        )
        for plan in plans:
            assert s.get_plan(plan.plan_id) is not None

    def test_empty_sector_volumes(self):
        s = sched()
        plans = s.plan_multi_sector({}, start_from=FIXED_START)
        assert plans == []


# ── summary ───────────────────────────────────────────────────────────────────

class TestSummary:
    def test_summary_keys(self):
        s = sched()
        s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        summary = s.summary()
        for key in ("total_plans", "total_waves", "total_emails_planned",
                    "pending", "done", "cancelled"):
            assert key in summary

    def test_summary_empty_scheduler(self):
        summary = sched().summary()
        assert summary["total_plans"] == 0
        assert summary["total_waves"] == 0
        assert summary["total_emails_planned"] == 0

    def test_summary_counts_plans(self):
        s = sched()
        s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        s.plan("restaurant", 20, "2.2", start_from=FIXED_START)
        assert s.summary()["total_plans"] == 2

    def test_summary_total_emails(self):
        s = sched()
        s.plan("artisan", 30, "2.1", start_from=FIXED_START)
        s.plan("restaurant", 20, "2.2", start_from=FIXED_START)
        assert s.summary()["total_emails_planned"] == 50

    def test_summary_pending_count(self):
        s = sched()
        s.plan("artisan", 30, "2.1", start_from=FIXED_START)
        assert s.summary()["pending"] == 1

    def test_summary_done_count_after_mark(self):
        s = sched()
        plan = s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        s.mark_wave_done(plan.plan_id, plan.waves[0].wave_id)
        assert s.summary()["done"] == 1
        assert s.summary()["pending"] == 0

    def test_summary_cancelled_count(self):
        s = sched()
        plan = s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        s.cancel_wave(plan.plan_id, plan.waves[0].wave_id)
        assert s.summary()["cancelled"] == 1


# ── reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_plans(self):
        s = sched()
        s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        s.reset()
        assert s.list_plans() == []

    def test_reset_allows_fresh_start(self):
        s = sched()
        s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        s.reset()
        s.plan("restaurant", 20, "2.2", start_from=FIXED_START)
        assert len(s.list_plans()) == 1

    def test_reset_clears_pending_waves(self):
        s = sched()
        s.plan("artisan", 10, "2.1", start_from=FIXED_START)
        s.reset()
        far_future = FIXED_START + datetime.timedelta(days=100)
        assert s.pending_waves(as_of=far_future) == []


# ── custom constructor ────────────────────────────────────────────────────────

class TestCustomConstructor:
    def test_custom_max_per_hour(self):
        s = CampaignScheduler(max_per_hour=50)
        assert s.max_per_hour == 50

    def test_custom_max_per_wave(self):
        s = CampaignScheduler(max_per_wave=10)
        plan = s.plan("artisan", 25, "2.1", start_from=FIXED_START)
        assert plan.total_waves == 3

    def test_custom_min_gap_hours(self):
        s = CampaignScheduler(max_per_wave=50, min_gap_hours=8)
        plan = s.plan("artisan", 60, "2.1", start_from=FIXED_START)
        gap_h = (plan.waves[1].scheduled_at - plan.waves[0].scheduled_at).total_seconds() / 3600
        assert gap_h >= 8


# ── _best_windows internal ────────────────────────────────────────────────────

class TestBestWindows:
    def test_exact_sector_match(self):
        s = sched()
        windows = s._best_windows("artisan")
        assert len(windows) > 0

    def test_partial_sector_match(self):
        s = sched()
        windows = s._best_windows("artisan bâtiment")
        assert len(windows) > 0

    def test_unknown_sector_returns_default(self):
        s = sched()
        windows = s._best_windows("zorgblorf")
        assert windows is not None
        assert len(windows) > 0

    def test_case_insensitive(self):
        s = sched()
        windows_lower = s._best_windows("restaurant")
        windows_upper = s._best_windows("RESTAURANT")
        assert windows_lower == windows_upper
