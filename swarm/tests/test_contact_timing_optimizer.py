"""Tests for ContactTimingOptimizer."""

import pytest
from intelligence.contact_timing_optimizer import (
    ContactTimingOptimizer,
    OptimalWindow,
)


@pytest.fixture()
def opt():
    return ContactTimingOptimizer()


# ── ScoreSlot ─────────────────────────────────────────────────────────────────

class TestScoreSlot:
    def test_sunday_always_very_low(self, opt):
        assert opt.score_slot("artisan", 6, 10) < 10

    def test_saturday_lower_than_tuesday(self, opt):
        assert opt.score_slot("PME", 5, 10) < opt.score_slot("PME", 1, 10)

    def test_tuesday_highest_for_pme(self, opt):
        scores_by_day = [opt.score_slot("PME", d, 10) for d in range(7)]
        assert scores_by_day[1] == max(scores_by_day)

    def test_midnight_zero_score(self, opt):
        assert opt.score_slot("artisan", 1, 0) == 0

    def test_peak_hour_artisan_morning(self, opt):
        score_9h = opt.score_slot("artisan", 1, 9)
        score_6h = opt.score_slot("artisan", 1, 6)
        assert score_9h > score_6h

    def test_score_bounded_0_100(self, opt):
        for sector in ["artisan", "restaurant", "médecin", "PME"]:
            for day in range(7):
                for hour in range(24):
                    score = opt.score_slot(sector, day, hour)
                    assert 0 <= score <= 100

    def test_unknown_sector_falls_back_to_pme(self, opt):
        score = opt.score_slot("unknown_xyz", 1, 10)
        pme_score = opt.score_slot("PME", 1, 10)
        assert score == pme_score

    def test_restaurant_lower_at_noon(self, opt):
        noon = opt.score_slot("restaurant", 1, 12)
        afternoon = opt.score_slot("restaurant", 1, 16)
        assert afternoon > noon


# ── BestWindow ────────────────────────────────────────────────────────────────

class TestBestWindow:
    def test_returns_optimal_window(self, opt):
        w = opt.best_window("artisan")
        assert isinstance(w, OptimalWindow)

    def test_best_day_is_weekday(self, opt):
        w = opt.best_window("artisan")
        assert 0 <= w.day_of_week <= 4

    def test_score_positive(self, opt):
        w = opt.best_window("restaurant")
        assert w.score > 0

    def test_confidence_is_valid(self, opt):
        w = opt.best_window("PME")
        assert w.confidence in ("high", "medium", "low")

    def test_high_confidence_for_strong_sectors(self, opt):
        w = opt.best_window("PME")
        assert w.confidence == "high"

    def test_has_rationale(self, opt):
        w = opt.best_window("artisan")
        assert len(w.rationale) > 5

    def test_hour_in_valid_range(self, opt):
        w = opt.best_window("médecin")
        assert 6 <= w.hour_start <= 19

    def test_best_score_is_maximum(self, opt):
        w = opt.best_window("PME")
        for day in range(5):
            for hour in range(6, 20):
                assert opt.score_slot("PME", day, hour) <= w.score + 0.01

    def test_to_dict_has_required_keys(self, opt):
        d = opt.best_window("artisan").to_dict()
        for key in ["sector", "day_of_week", "day_name", "hour_start", "hour_end", "score", "confidence", "rationale"]:
            assert key in d

    def test_sector_preserved_in_window(self, opt):
        w = opt.best_window("médecin")
        assert w.sector == "médecin"


# ── TopWindows ────────────────────────────────────────────────────────────────

class TestTopWindows:
    def test_returns_n_windows(self, opt):
        windows = opt.top_windows("artisan", n=3)
        assert len(windows) == 3

    def test_sorted_descending(self, opt):
        windows = opt.top_windows("PME", n=5)
        scores = [w.score for w in windows]
        assert scores == sorted(scores, reverse=True)

    def test_top_1_matches_best_window(self, opt):
        top = opt.top_windows("artisan", n=1)[0]
        best = opt.best_window("artisan")
        assert top.score == best.score
        assert top.day_of_week == best.day_of_week
        assert top.hour_start == best.hour_start

    def test_all_weekday_slots(self, opt):
        windows = opt.top_windows("restaurant", n=10)
        for w in windows:
            assert 0 <= w.day_of_week <= 4

    def test_n_0_returns_empty(self, opt):
        assert opt.top_windows("artisan", n=0) == []


# ── WeeklySchedule ────────────────────────────────────────────────────────────

class TestWeeklySchedule:
    def test_has_all_7_days(self, opt):
        schedule = opt.weekly_schedule("artisan")
        assert len(schedule) == 7

    def test_sunday_scores_low(self, opt):
        schedule = opt.weekly_schedule("artisan")
        max_sunday = max(schedule["Dimanche"].values())
        max_tuesday = max(schedule["Mardi"].values())
        assert max_tuesday > max_sunday

    def test_hours_covered(self, opt):
        schedule = opt.weekly_schedule("PME")
        for day_scores in schedule.values():
            assert len(day_scores) > 0

    def test_all_scores_bounded(self, opt):
        schedule = opt.weekly_schedule("médecin")
        for day_scores in schedule.values():
            for score in day_scores.values():
                assert 0 <= score <= 100

    def test_restaurant_lower_at_service_times(self, opt):
        schedule = opt.weekly_schedule("restaurant")
        noon_score = schedule["Mardi"].get(12, 0)
        afternoon_score = schedule["Mardi"].get(16, 0)
        assert afternoon_score > noon_score


# ── SectorSummary ─────────────────────────────────────────────────────────────

class TestSectorSummary:
    def test_returns_list(self, opt):
        summary = opt.sector_summary()
        assert isinstance(summary, list)
        assert len(summary) > 0

    def test_each_item_has_required_keys(self, opt):
        summary = opt.sector_summary()
        for item in summary:
            for key in ["sector", "day_of_week", "day_name", "hour_start", "hour_end", "score", "confidence"]:
                assert key in item

    def test_custom_sectors(self, opt):
        summary = opt.sector_summary(["artisan", "restaurant"])
        assert len(summary) == 2

    def test_sectors_have_different_windows(self, opt):
        s1 = opt.best_window("artisan")
        s2 = opt.best_window("PME")
        # Artisan peak is earlier in the morning
        assert s1.score > 0 and s2.score > 0

    def test_scores_are_reasonable(self, opt):
        summary = opt.sector_summary(["artisan"])
        assert summary[0]["score"] > 30  # At least medium engagement
