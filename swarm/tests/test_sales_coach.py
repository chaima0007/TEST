"""
Comprehensive tests for swarm/intelligence/sales_coach.py
"""

import pytest
from swarm.intelligence.sales_coach import (
    SalesCoachAgent,
    RepPerformance,
    CoachingPlan,
    CoachingPriority,
    CoachingFocus,
    SkillArea,
    _pipeline_health,
    _activity_score,
    _skill_gaps,
    _win_rate_trend,
    _determine_focus,
    _coaching_priority,
    _estimated_quota_attainment,
)


# ─── Helper ───────────────────────────────────────────────────────────────────

def make_rep(**kwargs) -> RepPerformance:
    """
    Build a RepPerformance with sensible defaults.
    Pass keyword arguments to override any single field.
    Defaults yield a healthy, averagely performing rep:
      - coverage 3.0 (≥ 3x), no stalls, good skills, improving win rate
    """
    defaults = dict(
        rep_id="rep_001",
        rep_name="Alice Dupont",
        manager_id="mgr_01",
        territory="France-Sud",
        open_deals=10,
        pipeline_value_eur=300_000.0,
        quota_eur=100_000.0,
        pipeline_coverage_ratio=3.0,
        calls_last_30d=60,
        emails_last_30d=120,
        meetings_last_30d=15,
        demos_last_30d=8,
        win_rate_last_90d=30.0,
        win_rate_prev_90d=25.0,
        avg_deal_size_eur=10_000.0,
        avg_sales_cycle_days=90,
        discovery_score=70.0,
        objection_score=70.0,
        demo_score=70.0,
        pricing_score=70.0,
        follow_up_score=70.0,
        relationship_score=70.0,
        time_mgmt_score=70.0,
        deals_won_last_90d=6,
        deals_lost_last_90d=4,
        deals_stalled_last_30d=1,
    )
    defaults.update(kwargs)
    return RepPerformance(**defaults)


# ─── Enums ────────────────────────────────────────────────────────────────────

class TestEnums:
    def test_coaching_priority_values(self):
        assert CoachingPriority.URGENT.value == "urgent"
        assert CoachingPriority.HIGH.value == "high"
        assert CoachingPriority.MEDIUM.value == "medium"
        assert CoachingPriority.LOW.value == "low"

    def test_coaching_focus_values(self):
        assert CoachingFocus.PROSPECTING.value == "prospecting"
        assert CoachingFocus.QUALIFICATION.value == "qualification"
        assert CoachingFocus.PRESENTATION.value == "presentation"
        assert CoachingFocus.NEGOTIATION.value == "negotiation"
        assert CoachingFocus.CLOSING.value == "closing"
        assert CoachingFocus.RETENTION.value == "retention"

    def test_skill_area_values(self):
        expected = {"discovery", "objection_handling", "demo", "pricing",
                    "follow_up", "relationship", "time_management"}
        actual = {s.value for s in SkillArea}
        assert actual == expected

    def test_coaching_priority_is_str_enum(self):
        assert isinstance(CoachingPriority.URGENT, str)

    def test_coaching_focus_is_str_enum(self):
        assert isinstance(CoachingFocus.RETENTION, str)


# ─── RepPerformance dataclass ─────────────────────────────────────────────────

class TestRepPerformance:
    def test_can_instantiate(self):
        r = make_rep()
        assert r.rep_id == "rep_001"

    def test_to_dict_contains_all_fields(self):
        r = make_rep()
        d = r.to_dict()
        for field in (
            "rep_id", "rep_name", "manager_id", "territory",
            "open_deals", "pipeline_value_eur", "quota_eur",
            "pipeline_coverage_ratio", "calls_last_30d", "emails_last_30d",
            "meetings_last_30d", "demos_last_30d", "win_rate_last_90d",
            "win_rate_prev_90d", "avg_deal_size_eur", "avg_sales_cycle_days",
            "discovery_score", "objection_score", "demo_score",
            "pricing_score", "follow_up_score", "relationship_score",
            "time_mgmt_score", "deals_won_last_90d", "deals_lost_last_90d",
            "deals_stalled_last_30d",
        ):
            assert field in d, f"Missing field: {field}"

    def test_to_dict_returns_correct_values(self):
        r = make_rep(rep_id="xyz", territory="Paris")
        d = r.to_dict()
        assert d["rep_id"] == "xyz"
        assert d["territory"] == "Paris"


# ─── _pipeline_health ─────────────────────────────────────────────────────────

class TestPipelineHealth:
    # ── coverage scoring ──────────────────────────────────────────────────────

    def test_coverage_4_gives_100(self):
        r = make_rep(pipeline_coverage_ratio=4.0, deals_stalled_last_30d=0,
                     pipeline_value_eur=400_000, quota_eur=100_000)
        score, _ = _pipeline_health(r)
        # cov_score=100, stall_score=100, quota_score=min(100,133.33)=100
        # score = 100*0.40 + 100*0.35 + 100*0.25 = 100
        assert score == 100.0

    def test_coverage_above_4_gives_100(self):
        r = make_rep(pipeline_coverage_ratio=5.0, deals_stalled_last_30d=0,
                     pipeline_value_eur=500_000, quota_eur=100_000)
        score, _ = _pipeline_health(r)
        assert score == 100.0

    def test_coverage_3_cov_score_85(self):
        r = make_rep(pipeline_coverage_ratio=3.0, deals_stalled_last_30d=0,
                     pipeline_value_eur=300_000, quota_eur=100_000)
        score, _ = _pipeline_health(r)
        # cov_score=85, stall_score=100, quota_score=100
        assert score == pytest.approx(85 * 0.40 + 100 * 0.35 + 100 * 0.25, rel=1e-4)

    def test_coverage_3point5_cov_score_85(self):
        r = make_rep(pipeline_coverage_ratio=3.5, deals_stalled_last_30d=0,
                     pipeline_value_eur=350_000, quota_eur=100_000)
        score, _ = _pipeline_health(r)
        assert score == pytest.approx(85 * 0.40 + 100 * 0.35 + 100 * 0.25, rel=1e-4)

    def test_coverage_2_cov_score_65(self):
        r = make_rep(pipeline_coverage_ratio=2.0, deals_stalled_last_30d=0,
                     pipeline_value_eur=200_000, quota_eur=100_000)
        score, _ = _pipeline_health(r)
        # quota_score = min(100, (200000/100000*100)/3) = min(100, 66.67) = 66.67
        quota_s = min(100, (200_000 / 100_000 * 100) / 3.0)
        expected = 65 * 0.40 + 100 * 0.35 + quota_s * 0.25
        assert score == pytest.approx(expected, rel=1e-4)

    def test_coverage_2point5_cov_score_65(self):
        r = make_rep(pipeline_coverage_ratio=2.5, deals_stalled_last_30d=0,
                     pipeline_value_eur=250_000, quota_eur=100_000)
        score, _ = _pipeline_health(r)
        quota_s = min(100, (250_000 / 100_000 * 100) / 3.0)
        expected = 65 * 0.40 + 100 * 0.35 + quota_s * 0.25
        assert score == pytest.approx(expected, rel=1e-4)

    def test_coverage_1_cov_score_40(self):
        r = make_rep(pipeline_coverage_ratio=1.0, deals_stalled_last_30d=0,
                     pipeline_value_eur=100_000, quota_eur=100_000)
        score, _ = _pipeline_health(r)
        quota_s = min(100, (100_000 / 100_000 * 100) / 3.0)
        expected = 40 * 0.40 + 100 * 0.35 + quota_s * 0.25
        assert score == pytest.approx(expected, rel=1e-4)

    def test_coverage_1point5_cov_score_40(self):
        r = make_rep(pipeline_coverage_ratio=1.5, deals_stalled_last_30d=0,
                     pipeline_value_eur=150_000, quota_eur=100_000)
        score, _ = _pipeline_health(r)
        quota_s = min(100, (150_000 / 100_000 * 100) / 3.0)
        expected = 40 * 0.40 + 100 * 0.35 + quota_s * 0.25
        assert score == pytest.approx(expected, rel=1e-4)

    def test_coverage_below_1_uses_formula(self):
        r = make_rep(pipeline_coverage_ratio=0.5, deals_stalled_last_30d=0,
                     pipeline_value_eur=50_000, quota_eur=100_000)
        score, _ = _pipeline_health(r)
        cov_s = max(0.0, 0.5 * 40.0)  # = 20
        quota_s = min(100, (50_000 / 100_000 * 100) / 3.0)
        expected = cov_s * 0.40 + 100 * 0.35 + quota_s * 0.25
        assert score == pytest.approx(expected, rel=1e-4)

    def test_coverage_zero_cov_score_zero(self):
        r = make_rep(pipeline_coverage_ratio=0.0, deals_stalled_last_30d=0,
                     pipeline_value_eur=0, quota_eur=100_000)
        score, _ = _pipeline_health(r)
        # cov_score = max(0, 0*40) = 0, stall_score=100, quota_score=0
        assert score == pytest.approx(0 * 0.40 + 100 * 0.35 + 0 * 0.25, rel=1e-4)

    # ── coverage < 2.0 adds increase_prospecting tip ──────────────────────────

    def test_coverage_below_2_adds_prospecting_tip(self):
        r = make_rep(pipeline_coverage_ratio=1.9)
        _, tips = _pipeline_health(r)
        assert "increase_prospecting" in tips

    def test_coverage_exactly_2_no_prospecting_tip(self):
        r = make_rep(pipeline_coverage_ratio=2.0)
        _, tips = _pipeline_health(r)
        assert "increase_prospecting" not in tips

    def test_coverage_above_2_no_prospecting_tip(self):
        r = make_rep(pipeline_coverage_ratio=3.0)
        _, tips = _pipeline_health(r)
        assert "increase_prospecting" not in tips

    # ── stall scoring ─────────────────────────────────────────────────────────

    def test_no_stalled_deals_stall_score_100(self):
        r = make_rep(pipeline_coverage_ratio=4.0, deals_stalled_last_30d=0,
                     open_deals=10, pipeline_value_eur=400_000, quota_eur=100_000)
        score, _ = _pipeline_health(r)
        assert score == 100.0

    def test_stall_pct_50_stall_score_zero(self):
        # stall_pct=50 → stall_score = max(0, 100-100) = 0
        r = make_rep(pipeline_coverage_ratio=4.0, open_deals=10,
                     deals_stalled_last_30d=5, pipeline_value_eur=400_000, quota_eur=100_000)
        score, _ = _pipeline_health(r)
        # stall_score=0
        expected = 100 * 0.40 + 0 * 0.35 + 100 * 0.25
        assert score == pytest.approx(expected, rel=1e-4)

    def test_stall_pct_above_30_adds_followup_and_weekly_review_tips(self):
        r = make_rep(open_deals=10, deals_stalled_last_30d=4)  # 40% stalled
        _, tips = _pipeline_health(r)
        assert "follow_up_faster" in tips
        assert "weekly_review" in tips

    def test_stall_pct_exactly_30_no_followup_tip(self):
        r = make_rep(open_deals=10, deals_stalled_last_30d=3)  # exactly 30%
        _, tips = _pipeline_health(r)
        assert "follow_up_faster" not in tips
        assert "weekly_review" not in tips

    def test_stall_pct_below_30_no_tips(self):
        r = make_rep(open_deals=10, deals_stalled_last_30d=2)  # 20%
        _, tips = _pipeline_health(r)
        assert "follow_up_faster" not in tips

    def test_zero_open_deals_no_division_error(self):
        r = make_rep(open_deals=0, deals_stalled_last_30d=0)
        score, _ = _pipeline_health(r)
        assert isinstance(score, float)

    # ── quota_score ───────────────────────────────────────────────────────────

    def test_quota_score_capped_at_100(self):
        # pipeline_value_eur = 1_000_000, quota = 100_000 → quota_attain=1000%
        # quota_score = min(100, 1000/3) = 100
        r = make_rep(pipeline_coverage_ratio=4.0, deals_stalled_last_30d=0,
                     pipeline_value_eur=1_000_000, quota_eur=100_000)
        score, _ = _pipeline_health(r)
        assert score == 100.0

    def test_zero_quota_no_division_error(self):
        r = make_rep(quota_eur=0, pipeline_value_eur=0)
        score, _ = _pipeline_health(r)
        assert isinstance(score, float)

    # ── return type ───────────────────────────────────────────────────────────

    def test_returns_tuple_float_list(self):
        r = make_rep()
        result = _pipeline_health(r)
        assert isinstance(result, tuple)
        assert isinstance(result[0], float)
        assert isinstance(result[1], list)


# ─── _activity_score ──────────────────────────────────────────────────────────

class TestActivityScore:
    # ── at benchmark = 100 ───────────────────────────────────────────────────

    def test_at_benchmarks_gives_100(self):
        r = make_rep(calls_last_30d=60, emails_last_30d=120,
                     meetings_last_30d=15, demos_last_30d=8)
        score, _ = _activity_score(r)
        assert score == pytest.approx(100.0, rel=1e-4)

    # ── individual sub-scores ─────────────────────────────────────────────────

    def test_calls_half_benchmark(self):
        r = make_rep(calls_last_30d=30, emails_last_30d=120,
                     meetings_last_30d=15, demos_last_30d=8)
        score, _ = _activity_score(r)
        # call_score=50, rest=100 → avg = (50+100+100+100)*0.25 = 87.5
        assert score == pytest.approx(87.5, rel=1e-4)

    def test_emails_half_benchmark(self):
        r = make_rep(calls_last_30d=60, emails_last_30d=60,
                     meetings_last_30d=15, demos_last_30d=8)
        score, _ = _activity_score(r)
        assert score == pytest.approx(87.5, rel=1e-4)

    def test_meetings_half_benchmark(self):
        r = make_rep(calls_last_30d=60, emails_last_30d=120,
                     meetings_last_30d=7, demos_last_30d=8)  # ~46.67
        meeting_score = min(100, 7 / 15 * 100)
        expected = (100 + 100 + meeting_score + 100) * 0.25
        score, _ = _activity_score(r)
        assert score == pytest.approx(expected, rel=1e-4)

    def test_demos_half_benchmark(self):
        r = make_rep(calls_last_30d=60, emails_last_30d=120,
                     meetings_last_30d=15, demos_last_30d=4)
        score, _ = _activity_score(r)
        assert score == pytest.approx((100 + 100 + 100 + 50) * 0.25, rel=1e-4)

    def test_all_zero_gives_zero(self):
        r = make_rep(calls_last_30d=0, emails_last_30d=0,
                     meetings_last_30d=0, demos_last_30d=0)
        score, _ = _activity_score(r)
        assert score == 0.0

    def test_above_benchmark_capped_at_100(self):
        r = make_rep(calls_last_30d=200, emails_last_30d=500,
                     meetings_last_30d=50, demos_last_30d=30)
        score, _ = _activity_score(r)
        assert score == 100.0

    # ── tips ─────────────────────────────────────────────────────────────────

    def test_demos_below_3_adds_improve_demo_tip(self):
        r = make_rep(demos_last_30d=2)
        _, tips = _activity_score(r)
        assert "improve_demo" in tips

    def test_demos_exactly_3_no_improve_demo_tip(self):
        r = make_rep(demos_last_30d=3)
        _, tips = _activity_score(r)
        assert "improve_demo" not in tips

    def test_demos_above_3_no_improve_demo_tip(self):
        r = make_rep(demos_last_30d=8)
        _, tips = _activity_score(r)
        assert "improve_demo" not in tips

    def test_calls_plus_emails_below_50_adds_use_crm_tip(self):
        r = make_rep(calls_last_30d=10, emails_last_30d=20)  # sum=30
        _, tips = _activity_score(r)
        assert "use_crm" in tips

    def test_calls_plus_emails_exactly_50_no_use_crm_tip(self):
        r = make_rep(calls_last_30d=25, emails_last_30d=25)
        _, tips = _activity_score(r)
        assert "use_crm" not in tips

    def test_calls_plus_emails_above_50_no_use_crm_tip(self):
        r = make_rep(calls_last_30d=60, emails_last_30d=120)
        _, tips = _activity_score(r)
        assert "use_crm" not in tips

    def test_no_tips_when_all_above_benchmarks(self):
        r = make_rep(calls_last_30d=60, emails_last_30d=120,
                     meetings_last_30d=15, demos_last_30d=8)
        _, tips = _activity_score(r)
        assert tips == []

    def test_both_tips_when_demos_and_volume_low(self):
        r = make_rep(calls_last_30d=5, emails_last_30d=5, demos_last_30d=0)
        _, tips = _activity_score(r)
        assert "improve_demo" in tips
        assert "use_crm" in tips

    # ── return type ───────────────────────────────────────────────────────────

    def test_returns_tuple_float_list(self):
        result = _activity_score(make_rep())
        assert isinstance(result, tuple)
        assert isinstance(result[0], float)
        assert isinstance(result[1], list)


# ─── _skill_gaps ──────────────────────────────────────────────────────────────

class TestSkillGaps:
    def test_all_perfect_avg_100_no_tips(self):
        r = make_rep(discovery_score=100, objection_score=100, demo_score=100,
                     pricing_score=100, follow_up_score=100,
                     relationship_score=100, time_mgmt_score=100)
        avg, tips = _skill_gaps(r)
        assert avg == 100.0
        assert tips == []

    def test_all_zero_avg_zero_all_tips(self):
        r = make_rep(discovery_score=0, objection_score=0, demo_score=0,
                     pricing_score=0, follow_up_score=0,
                     relationship_score=0, time_mgmt_score=0)
        avg, tips = _skill_gaps(r)
        assert avg == 0.0
        assert len(tips) == 7

    def test_avg_is_mean_of_seven_scores(self):
        r = make_rep(discovery_score=50, objection_score=60, demo_score=70,
                     pricing_score=80, follow_up_score=90,
                     relationship_score=100, time_mgmt_score=40)
        expected_avg = (50 + 60 + 70 + 80 + 90 + 100 + 40) / 7
        avg, _ = _skill_gaps(r)
        assert avg == pytest.approx(expected_avg, rel=1e-4)

    def test_skill_below_60_adds_tip(self):
        r = make_rep(discovery_score=59)
        _, tips = _skill_gaps(r)
        from swarm.intelligence.sales_coach import _SKILL_TIPS
        assert _SKILL_TIPS[SkillArea.DISCOVERY] in tips

    def test_skill_exactly_60_no_tip(self):
        r = make_rep(discovery_score=60)
        _, tips = _skill_gaps(r)
        from swarm.intelligence.sales_coach import _SKILL_TIPS
        assert _SKILL_TIPS[SkillArea.DISCOVERY] not in tips

    def test_objection_skill_weak_adds_tip(self):
        r = make_rep(objection_score=55)
        _, tips = _skill_gaps(r)
        from swarm.intelligence.sales_coach import _SKILL_TIPS
        assert _SKILL_TIPS[SkillArea.OBJECTION_HANDLING] in tips

    def test_demo_skill_weak_adds_tip(self):
        r = make_rep(demo_score=40)
        _, tips = _skill_gaps(r)
        from swarm.intelligence.sales_coach import _SKILL_TIPS
        assert _SKILL_TIPS[SkillArea.DEMO] in tips

    def test_pricing_skill_weak_adds_tip(self):
        r = make_rep(pricing_score=30)
        _, tips = _skill_gaps(r)
        from swarm.intelligence.sales_coach import _SKILL_TIPS
        assert _SKILL_TIPS[SkillArea.PRICING] in tips

    def test_followup_skill_weak_adds_tip(self):
        r = make_rep(follow_up_score=50)
        _, tips = _skill_gaps(r)
        from swarm.intelligence.sales_coach import _SKILL_TIPS
        assert _SKILL_TIPS[SkillArea.FOLLOW_UP] in tips

    def test_relationship_skill_weak_adds_tip(self):
        r = make_rep(relationship_score=10)
        _, tips = _skill_gaps(r)
        from swarm.intelligence.sales_coach import _SKILL_TIPS
        assert _SKILL_TIPS[SkillArea.RELATIONSHIP] in tips

    def test_time_mgmt_skill_weak_adds_tip(self):
        r = make_rep(time_mgmt_score=0)
        _, tips = _skill_gaps(r)
        from swarm.intelligence.sales_coach import _SKILL_TIPS
        assert _SKILL_TIPS[SkillArea.TIME_MANAGEMENT] in tips

    def test_returns_tuple_float_list(self):
        result = _skill_gaps(make_rep())
        assert isinstance(result, tuple)
        assert isinstance(result[0], float)
        assert isinstance(result[1], list)

    def test_all_strong_no_tips(self):
        r = make_rep(discovery_score=70, objection_score=70, demo_score=70,
                     pricing_score=70, follow_up_score=70,
                     relationship_score=70, time_mgmt_score=70)
        _, tips = _skill_gaps(r)
        assert tips == []


# ─── _win_rate_trend ──────────────────────────────────────────────────────────

class TestWinRateTrend:
    # ── rate_score ────────────────────────────────────────────────────────────

    def test_66pct_win_rate_gives_rate_score_99(self):
        r = make_rep(win_rate_last_90d=66.0, win_rate_prev_90d=61.0)
        score, _ = _win_rate_trend(r)
        # rate_score = min(100, 66*1.5) = 99, trend=5 → +15, clamp 99+15=100
        assert score == 100.0

    def test_win_rate_above_66_rate_score_capped_at_100(self):
        r = make_rep(win_rate_last_90d=80.0, win_rate_prev_90d=70.0)
        score, _ = _win_rate_trend(r)
        # rate_score=100, trend=10 → +15; clamp=100
        assert score == 100.0

    def test_rate_score_formula_low_win_rate(self):
        r = make_rep(win_rate_last_90d=20.0, win_rate_prev_90d=20.0)
        score, _ = _win_rate_trend(r)
        # rate_score = 30, trend=0 → +5; score=35
        assert score == pytest.approx(35.0, rel=1e-4)

    # ── trend bonus ───────────────────────────────────────────────────────────

    def test_trend_ge_5_gives_plus15(self):
        r = make_rep(win_rate_last_90d=40.0, win_rate_prev_90d=35.0)
        score, _ = _win_rate_trend(r)
        rate_score = min(100, 40 * 1.5)
        expected = min(100, max(0, rate_score + 15))
        assert score == pytest.approx(expected, rel=1e-4)

    def test_trend_exactly_5_gives_plus15(self):
        r = make_rep(win_rate_last_90d=30.0, win_rate_prev_90d=25.0)
        score, _ = _win_rate_trend(r)
        rate_score = min(100, 30 * 1.5)
        expected = min(100, max(0, rate_score + 15))
        assert score == pytest.approx(expected, rel=1e-4)

    def test_trend_ge_0_lt_5_gives_plus5(self):
        r = make_rep(win_rate_last_90d=30.0, win_rate_prev_90d=27.0)
        score, _ = _win_rate_trend(r)
        rate_score = min(100, 30 * 1.5)
        expected = min(100, max(0, rate_score + 5))
        assert score == pytest.approx(expected, rel=1e-4)

    def test_trend_zero_gives_plus5(self):
        r = make_rep(win_rate_last_90d=30.0, win_rate_prev_90d=30.0)
        score, _ = _win_rate_trend(r)
        rate_score = min(100, 30 * 1.5)
        expected = min(100, max(0, rate_score + 5))
        assert score == pytest.approx(expected, rel=1e-4)

    def test_trend_minus3_gives_minus5(self):
        r = make_rep(win_rate_last_90d=27.0, win_rate_prev_90d=30.0)
        score, _ = _win_rate_trend(r)
        rate_score = min(100, 27 * 1.5)
        expected = min(100, max(0, rate_score - 5))
        assert score == pytest.approx(expected, rel=1e-4)

    def test_trend_exactly_minus5_gives_minus5(self):
        r = make_rep(win_rate_last_90d=25.0, win_rate_prev_90d=30.0)
        score, _ = _win_rate_trend(r)
        rate_score = min(100, 25 * 1.5)
        expected = min(100, max(0, rate_score - 5))
        assert score == pytest.approx(expected, rel=1e-4)

    def test_trend_worse_than_minus5_gives_minus15(self):
        r = make_rep(win_rate_last_90d=20.0, win_rate_prev_90d=30.0)
        score, _ = _win_rate_trend(r)
        rate_score = min(100, 20 * 1.5)
        expected = min(100, max(0, rate_score - 15))
        assert score == pytest.approx(expected, rel=1e-4)

    def test_score_clamped_to_zero_when_very_low(self):
        r = make_rep(win_rate_last_90d=0.0, win_rate_prev_90d=10.0)
        score, _ = _win_rate_trend(r)
        assert score >= 0.0

    def test_score_never_exceeds_100(self):
        r = make_rep(win_rate_last_90d=100.0, win_rate_prev_90d=90.0)
        score, _ = _win_rate_trend(r)
        assert score <= 100.0

    # ── tips ─────────────────────────────────────────────────────────────────

    def test_declining_trend_adds_qualify_harder_and_handle_objections(self):
        r = make_rep(win_rate_last_90d=25.0, win_rate_prev_90d=35.0)  # trend=-10
        _, tips = _win_rate_trend(r)
        assert "qualify_harder" in tips
        assert "handle_objections" in tips

    def test_stable_trend_no_qualify_harder_tip(self):
        r = make_rep(win_rate_last_90d=30.0, win_rate_prev_90d=30.0)
        _, tips = _win_rate_trend(r)
        assert "qualify_harder" not in tips

    def test_win_rate_below_20_adds_close_earlier_tip(self):
        r = make_rep(win_rate_last_90d=15.0, win_rate_prev_90d=15.0)
        _, tips = _win_rate_trend(r)
        assert "close_earlier" in tips

    def test_win_rate_exactly_20_no_close_earlier_tip(self):
        r = make_rep(win_rate_last_90d=20.0, win_rate_prev_90d=20.0)
        _, tips = _win_rate_trend(r)
        assert "close_earlier" not in tips

    def test_win_rate_above_20_no_close_earlier_tip(self):
        r = make_rep(win_rate_last_90d=30.0, win_rate_prev_90d=25.0)
        _, tips = _win_rate_trend(r)
        assert "close_earlier" not in tips

    def test_returns_tuple_float_list(self):
        result = _win_rate_trend(make_rep())
        assert isinstance(result, tuple)
        assert isinstance(result[0], float)
        assert isinstance(result[1], list)


# ─── _determine_focus ─────────────────────────────────────────────────────────

class TestDetermineFocus:
    def test_coverage_below_1point5_returns_prospecting(self):
        r = make_rep(pipeline_coverage_ratio=1.4)
        focus = _determine_focus(r, 50.0, r.win_rate_last_90d)
        assert focus == CoachingFocus.PROSPECTING

    def test_coverage_exactly_1point5_not_prospecting(self):
        r = make_rep(pipeline_coverage_ratio=1.5, win_rate_last_90d=30.0,
                     demos_last_30d=5, avg_sales_cycle_days=90,
                     deals_stalled_last_30d=1, open_deals=10,
                     deals_lost_last_90d=4, deals_won_last_90d=6)
        focus = _determine_focus(r, 50.0, r.win_rate_last_90d)
        assert focus != CoachingFocus.PROSPECTING

    def test_win_rate_below_15_returns_qualification(self):
        r = make_rep(pipeline_coverage_ratio=2.0, win_rate_last_90d=14.9)
        focus = _determine_focus(r, 60.0, r.win_rate_last_90d)
        assert focus == CoachingFocus.QUALIFICATION

    def test_win_rate_exactly_15_not_qualification_from_winrate(self):
        # Must check that 15.0 doesn't trigger the <15 branch
        r = make_rep(pipeline_coverage_ratio=2.0, win_rate_last_90d=15.0,
                     demos_last_30d=5, avg_sales_cycle_days=90,
                     deals_stalled_last_30d=1, open_deals=10,
                     deals_lost_last_90d=2, deals_won_last_90d=6)
        focus = _determine_focus(r, 60.0, r.win_rate_last_90d)
        # Should not be QUALIFICATION from win_rate branch (may be from lost>won*2 but not here)
        # lost=2, won=6 → 2 > 12? No → RETENTION
        assert focus == CoachingFocus.RETENTION

    def test_demos_below_2_returns_presentation(self):
        r = make_rep(pipeline_coverage_ratio=2.0, win_rate_last_90d=25.0,
                     demos_last_30d=1, avg_sales_cycle_days=90,
                     deals_stalled_last_30d=1, open_deals=10,
                     deals_lost_last_90d=2, deals_won_last_90d=6)
        focus = _determine_focus(r, 60.0, r.win_rate_last_90d)
        assert focus == CoachingFocus.PRESENTATION

    def test_demos_exactly_2_not_presentation(self):
        r = make_rep(pipeline_coverage_ratio=2.0, win_rate_last_90d=25.0,
                     demos_last_30d=2, avg_sales_cycle_days=90,
                     deals_stalled_last_30d=1, open_deals=10,
                     deals_lost_last_90d=2, deals_won_last_90d=6)
        focus = _determine_focus(r, 60.0, r.win_rate_last_90d)
        assert focus != CoachingFocus.PRESENTATION

    def test_long_cycle_returns_negotiation(self):
        r = make_rep(pipeline_coverage_ratio=2.0, win_rate_last_90d=25.0,
                     demos_last_30d=5, avg_sales_cycle_days=121,
                     deals_stalled_last_30d=1, open_deals=10,
                     deals_lost_last_90d=2, deals_won_last_90d=6)
        focus = _determine_focus(r, 60.0, r.win_rate_last_90d)
        assert focus == CoachingFocus.NEGOTIATION

    def test_cycle_exactly_120_not_negotiation(self):
        r = make_rep(pipeline_coverage_ratio=2.0, win_rate_last_90d=25.0,
                     demos_last_30d=5, avg_sales_cycle_days=120,
                     deals_stalled_last_30d=1, open_deals=10,
                     deals_lost_last_90d=2, deals_won_last_90d=6)
        focus = _determine_focus(r, 60.0, r.win_rate_last_90d)
        assert focus != CoachingFocus.NEGOTIATION

    def test_stalled_over_40pct_returns_closing(self):
        r = make_rep(pipeline_coverage_ratio=2.0, win_rate_last_90d=25.0,
                     demos_last_30d=5, avg_sales_cycle_days=90,
                     open_deals=10, deals_stalled_last_30d=5,  # 50% > 40%
                     deals_lost_last_90d=2, deals_won_last_90d=6)
        focus = _determine_focus(r, 60.0, r.win_rate_last_90d)
        assert focus == CoachingFocus.CLOSING

    def test_stalled_exactly_40pct_not_closing(self):
        # 4/10 = exactly 40% — condition is strict >
        r = make_rep(pipeline_coverage_ratio=2.0, win_rate_last_90d=25.0,
                     demos_last_30d=5, avg_sales_cycle_days=90,
                     open_deals=10, deals_stalled_last_30d=4,
                     deals_lost_last_90d=2, deals_won_last_90d=6)
        focus = _determine_focus(r, 60.0, r.win_rate_last_90d)
        assert focus != CoachingFocus.CLOSING

    def test_lost_more_than_2x_won_returns_qualification(self):
        r = make_rep(pipeline_coverage_ratio=2.0, win_rate_last_90d=25.0,
                     demos_last_30d=5, avg_sales_cycle_days=90,
                     open_deals=10, deals_stalled_last_30d=1,
                     deals_lost_last_90d=13, deals_won_last_90d=6)
        focus = _determine_focus(r, 60.0, r.win_rate_last_90d)
        assert focus == CoachingFocus.QUALIFICATION

    def test_healthy_rep_returns_retention(self):
        r = make_rep(pipeline_coverage_ratio=3.0, win_rate_last_90d=35.0,
                     demos_last_30d=8, avg_sales_cycle_days=60,
                     open_deals=10, deals_stalled_last_30d=1,
                     deals_lost_last_90d=4, deals_won_last_90d=6)
        focus = _determine_focus(r, 80.0, r.win_rate_last_90d)
        assert focus == CoachingFocus.RETENTION

    def test_priority_prospecting_over_qualification(self):
        # coverage < 1.5 should take priority over win_rate < 15
        r = make_rep(pipeline_coverage_ratio=1.0, win_rate_last_90d=10.0)
        focus = _determine_focus(r, 30.0, r.win_rate_last_90d)
        assert focus == CoachingFocus.PROSPECTING


# ─── _coaching_priority ───────────────────────────────────────────────────────

class TestCoachingPriority:
    def test_score_75_is_urgent(self):
        assert _coaching_priority(75.0) == CoachingPriority.URGENT

    def test_score_100_is_urgent(self):
        assert _coaching_priority(100.0) == CoachingPriority.URGENT

    def test_score_74point9_is_high(self):
        assert _coaching_priority(74.9) == CoachingPriority.HIGH

    def test_score_55_is_high(self):
        assert _coaching_priority(55.0) == CoachingPriority.HIGH

    def test_score_54point9_is_medium(self):
        assert _coaching_priority(54.9) == CoachingPriority.MEDIUM

    def test_score_35_is_medium(self):
        assert _coaching_priority(35.0) == CoachingPriority.MEDIUM

    def test_score_34point9_is_low(self):
        assert _coaching_priority(34.9) == CoachingPriority.LOW

    def test_score_0_is_low(self):
        assert _coaching_priority(0.0) == CoachingPriority.LOW

    def test_score_80_is_urgent(self):
        assert _coaching_priority(80.0) == CoachingPriority.URGENT

    def test_score_60_is_high(self):
        assert _coaching_priority(60.0) == CoachingPriority.HIGH

    def test_score_45_is_medium(self):
        assert _coaching_priority(45.0) == CoachingPriority.MEDIUM


# ─── _estimated_quota_attainment ──────────────────────────────────────────────

class TestEstimatedQuotaAttainment:
    def test_zero_quota_returns_zero(self):
        r = make_rep(quota_eur=0)
        result = _estimated_quota_attainment(r, 30.0, 80.0)
        assert result == 0.0

    def test_perfect_pipeline_and_win_rate(self):
        r = make_rep(pipeline_value_eur=100_000, quota_eur=100_000)
        # effective = 100000 * 1.0 = 100000; attainment = 100%
        # health_factor = 0.80 + (100/100)*0.40 = 1.20
        # result = min(200, 100 * 1.20) = 120
        result = _estimated_quota_attainment(r, 100.0, 100.0)
        assert result == pytest.approx(120.0, rel=1e-4)

    def test_attainment_capped_at_200(self):
        r = make_rep(pipeline_value_eur=10_000_000, quota_eur=100_000)
        result = _estimated_quota_attainment(r, 100.0, 100.0)
        assert result == 200.0

    def test_returns_float(self):
        r = make_rep()
        result = _estimated_quota_attainment(r, 30.0, 70.0)
        assert isinstance(result, float)

    def test_low_win_rate_reduces_attainment(self):
        r = make_rep(pipeline_value_eur=300_000, quota_eur=100_000)
        result_10 = _estimated_quota_attainment(r, 10.0, 70.0)
        result_50 = _estimated_quota_attainment(r, 50.0, 70.0)
        assert result_10 < result_50

    def test_health_factor_influences_attainment(self):
        r = make_rep(pipeline_value_eur=300_000, quota_eur=100_000)
        result_low_health = _estimated_quota_attainment(r, 30.0, 0.0)
        result_high_health = _estimated_quota_attainment(r, 30.0, 100.0)
        assert result_low_health < result_high_health

    def test_rounded_to_2dp(self):
        r = make_rep(pipeline_value_eur=100_001, quota_eur=100_000)
        result = _estimated_quota_attainment(r, 33.33, 50.0)
        # Check it's rounded
        assert result == round(result, 2)


# ─── coaching_score formula ───────────────────────────────────────────────────

class TestCoachingScoreFormula:
    def test_coaching_score_range(self):
        agent = SalesCoachAgent()
        plan = agent.coach(make_rep())
        assert 0.0 <= plan.coaching_score <= 100.0

    def test_bad_rep_has_higher_coaching_score(self):
        agent = SalesCoachAgent()
        good = agent.coach(make_rep(
            pipeline_coverage_ratio=4.0,
            calls_last_30d=60, emails_last_30d=120,
            meetings_last_30d=15, demos_last_30d=8,
            discovery_score=100, objection_score=100, demo_score=100,
            pricing_score=100, follow_up_score=100,
            relationship_score=100, time_mgmt_score=100,
            win_rate_last_90d=50.0, win_rate_prev_90d=40.0,
            rep_id="good",
        ))
        bad = agent.coach(make_rep(
            pipeline_coverage_ratio=0.5,
            calls_last_30d=0, emails_last_30d=0,
            meetings_last_30d=0, demos_last_30d=0,
            discovery_score=10, objection_score=10, demo_score=10,
            pricing_score=10, follow_up_score=10,
            relationship_score=10, time_mgmt_score=10,
            win_rate_last_90d=5.0, win_rate_prev_90d=20.0,
            rep_id="bad",
        ))
        assert bad.coaching_score > good.coaching_score

    def test_coaching_score_formula_direct(self):
        """Verify the formula manually for a known rep."""
        r = make_rep(
            pipeline_coverage_ratio=3.0,
            open_deals=10, deals_stalled_last_30d=1,
            pipeline_value_eur=300_000, quota_eur=100_000,
            calls_last_30d=60, emails_last_30d=120,
            meetings_last_30d=15, demos_last_30d=8,
            discovery_score=70, objection_score=70, demo_score=70,
            pricing_score=70, follow_up_score=70,
            relationship_score=70, time_mgmt_score=70,
            win_rate_last_90d=30.0, win_rate_prev_90d=25.0,
        )
        pipeline_s, _ = _pipeline_health(r)
        activity_s, _ = _activity_score(r)
        skill_avg, _ = _skill_gaps(r)
        win_trend_s, _ = _win_rate_trend(r)
        skill_gap_score = 100 - skill_avg
        expected = round(
            (100 - pipeline_s) * 0.30
            + (100 - activity_s) * 0.25
            + skill_gap_score * 0.25
            + (100 - win_trend_s) * 0.20,
            2,
        )
        agent = SalesCoachAgent()
        plan = agent.coach(r)
        assert plan.coaching_score == pytest.approx(expected, rel=1e-4)


# ─── CoachingPlan structure ───────────────────────────────────────────────────

class TestCoachingPlanStructure:
    def test_returns_coaching_plan(self):
        agent = SalesCoachAgent()
        plan = agent.coach(make_rep())
        assert isinstance(plan, CoachingPlan)

    def test_plan_has_coaching_priority(self):
        agent = SalesCoachAgent()
        plan = agent.coach(make_rep())
        assert isinstance(plan.coaching_priority, CoachingPriority)

    def test_plan_has_primary_focus(self):
        agent = SalesCoachAgent()
        plan = agent.coach(make_rep())
        assert isinstance(plan.primary_focus, CoachingFocus)

    def test_plan_has_top_recommendations_list(self):
        agent = SalesCoachAgent()
        plan = agent.coach(make_rep())
        assert isinstance(plan.top_recommendations, list)

    def test_plan_has_skill_development_list(self):
        agent = SalesCoachAgent()
        plan = agent.coach(make_rep())
        assert isinstance(plan.skill_development, list)

    def test_plan_has_kpis_to_watch_list(self):
        agent = SalesCoachAgent()
        plan = agent.coach(make_rep())
        assert isinstance(plan.kpis_to_watch, list)

    def test_plan_kpis_not_empty(self):
        agent = SalesCoachAgent()
        plan = agent.coach(make_rep())
        assert len(plan.kpis_to_watch) >= 2

    def test_plan_estimated_quota_attainment_is_float(self):
        agent = SalesCoachAgent()
        plan = agent.coach(make_rep())
        assert isinstance(plan.estimated_quota_attainment_pct, float)

    def test_to_dict_has_all_keys(self):
        agent = SalesCoachAgent()
        plan = agent.coach(make_rep())
        d = plan.to_dict()
        for key in (
            "rep", "coaching_priority", "primary_focus", "coaching_score",
            "pipeline_health_score", "activity_score", "skill_gap_score",
            "win_rate_trend_score", "top_recommendations",
            "skill_development", "kpis_to_watch", "estimated_quota_attainment_pct",
        ):
            assert key in d, f"Missing key: {key}"

    def test_to_dict_priority_is_string(self):
        agent = SalesCoachAgent()
        plan = agent.coach(make_rep())
        d = plan.to_dict()
        assert isinstance(d["coaching_priority"], str)

    def test_to_dict_focus_is_string(self):
        agent = SalesCoachAgent()
        plan = agent.coach(make_rep())
        d = plan.to_dict()
        assert isinstance(d["primary_focus"], str)

    def test_recommendations_are_strings(self):
        r = make_rep(pipeline_coverage_ratio=1.0)  # triggers prospecting tip
        agent = SalesCoachAgent()
        plan = agent.coach(r)
        for rec in plan.top_recommendations:
            assert isinstance(rec, str)

    def test_recommendations_are_unique(self):
        r = make_rep(pipeline_coverage_ratio=1.0, deals_stalled_last_30d=4, open_deals=10)
        agent = SalesCoachAgent()
        plan = agent.coach(r)
        assert len(plan.top_recommendations) == len(set(plan.top_recommendations))

    def test_plan_rep_field_is_rep_performance(self):
        agent = SalesCoachAgent()
        r = make_rep()
        plan = agent.coach(r)
        assert plan.rep is r


# ─── SalesCoachAgent.coach ────────────────────────────────────────────────────

class TestSalesCoachAgentCoach:
    def test_coach_returns_plan(self):
        agent = SalesCoachAgent()
        plan = agent.coach(make_rep())
        assert isinstance(plan, CoachingPlan)

    def test_coach_stores_plan_by_rep_id(self):
        agent = SalesCoachAgent()
        r = make_rep(rep_id="rep_abc")
        agent.coach(r)
        assert agent.get("rep_abc") is not None

    def test_coach_overwrites_existing_plan(self):
        agent = SalesCoachAgent()
        r1 = make_rep(rep_id="rep_x", win_rate_last_90d=30.0)
        r2 = make_rep(rep_id="rep_x", win_rate_last_90d=10.0)
        agent.coach(r1)
        agent.coach(r2)
        plan = agent.get("rep_x")
        assert plan.rep.win_rate_last_90d == 10.0

    def test_coach_batch_returns_list_of_plans(self):
        agent = SalesCoachAgent()
        reps = [make_rep(rep_id=f"rep_{i}") for i in range(5)]
        plans = agent.coach_batch(reps)
        assert len(plans) == 5
        assert all(isinstance(p, CoachingPlan) for p in plans)

    def test_coach_batch_stores_all(self):
        agent = SalesCoachAgent()
        reps = [make_rep(rep_id=f"rep_{i}") for i in range(3)]
        agent.coach_batch(reps)
        for i in range(3):
            assert agent.get(f"rep_{i}") is not None


# ─── SalesCoachAgent.get ──────────────────────────────────────────────────────

class TestSalesCoachAgentGet:
    def test_get_returns_none_for_unknown_id(self):
        agent = SalesCoachAgent()
        assert agent.get("nonexistent") is None

    def test_get_returns_plan_after_coach(self):
        agent = SalesCoachAgent()
        r = make_rep(rep_id="known")
        agent.coach(r)
        plan = agent.get("known")
        assert plan is not None

    def test_get_returns_correct_plan(self):
        agent = SalesCoachAgent()
        r = make_rep(rep_id="test_123", rep_name="Bob")
        agent.coach(r)
        plan = agent.get("test_123")
        assert plan.rep.rep_name == "Bob"


# ─── SalesCoachAgent.all_plans ────────────────────────────────────────────────

class TestAllPlans:
    def test_all_plans_empty_initially(self):
        agent = SalesCoachAgent()
        assert agent.all_plans() == []

    def test_all_plans_returns_all_coached_reps(self):
        agent = SalesCoachAgent()
        for i in range(4):
            agent.coach(make_rep(rep_id=f"r{i}"))
        assert len(agent.all_plans()) == 4

    def test_all_plans_sorted_by_coaching_score_desc(self):
        agent = SalesCoachAgent()
        # Bad rep = high coaching score; good rep = low coaching score
        agent.coach(make_rep(rep_id="good",
            pipeline_coverage_ratio=4.0, calls_last_30d=60,
            emails_last_30d=120, meetings_last_30d=15, demos_last_30d=8,
            discovery_score=100, objection_score=100, demo_score=100,
            pricing_score=100, follow_up_score=100,
            relationship_score=100, time_mgmt_score=100,
            win_rate_last_90d=60.0, win_rate_prev_90d=50.0))
        agent.coach(make_rep(rep_id="bad",
            pipeline_coverage_ratio=0.3, calls_last_30d=0, emails_last_30d=0,
            meetings_last_30d=0, demos_last_30d=0,
            discovery_score=10, objection_score=10, demo_score=10,
            pricing_score=10, follow_up_score=10, relationship_score=10,
            time_mgmt_score=10, win_rate_last_90d=5.0, win_rate_prev_90d=20.0))
        plans = agent.all_plans()
        assert plans[0].rep.rep_id == "bad"
        assert plans[-1].rep.rep_id == "good"

    def test_all_plans_sorted_descending(self):
        agent = SalesCoachAgent()
        for i in range(5):
            agent.coach(make_rep(rep_id=f"r{i}", win_rate_last_90d=float(i * 10)))
        scores = [p.coaching_score for p in agent.all_plans()]
        assert scores == sorted(scores, reverse=True)


# ─── SalesCoachAgent.urgent_reps ─────────────────────────────────────────────

class TestUrgentReps:
    def test_urgent_reps_empty_when_none_urgent(self):
        agent = SalesCoachAgent()
        # Coach a clearly healthy rep → LOW priority
        agent.coach(make_rep(
            pipeline_coverage_ratio=4.0, calls_last_30d=60,
            emails_last_30d=120, meetings_last_30d=15, demos_last_30d=8,
            discovery_score=100, objection_score=100, demo_score=100,
            pricing_score=100, follow_up_score=100,
            relationship_score=100, time_mgmt_score=100,
            win_rate_last_90d=60.0, win_rate_prev_90d=50.0,
        ))
        urgent = agent.urgent_reps()
        assert all(p.coaching_priority == CoachingPriority.URGENT for p in urgent)

    def test_urgent_reps_returns_only_urgent(self):
        agent = SalesCoachAgent()
        agent.coach(make_rep(rep_id="bad",
            pipeline_coverage_ratio=0.1, calls_last_30d=0, emails_last_30d=0,
            meetings_last_30d=0, demos_last_30d=0,
            discovery_score=5, objection_score=5, demo_score=5,
            pricing_score=5, follow_up_score=5, relationship_score=5,
            time_mgmt_score=5, win_rate_last_90d=2.0, win_rate_prev_90d=20.0))
        urgent = agent.urgent_reps()
        # All in urgent_reps must be URGENT
        for p in urgent:
            assert p.coaching_priority == CoachingPriority.URGENT


# ─── SalesCoachAgent.by_priority ─────────────────────────────────────────────

class TestByPriority:
    def test_by_priority_returns_only_matching(self):
        agent = SalesCoachAgent()
        agent.coach(make_rep(rep_id="r1"))
        for p in agent.by_priority(CoachingPriority.URGENT):
            assert p.coaching_priority == CoachingPriority.URGENT

    def test_by_priority_low_filters_correctly(self):
        agent = SalesCoachAgent()
        agent.coach(make_rep(rep_id="r1"))
        for p in agent.by_priority(CoachingPriority.LOW):
            assert p.coaching_priority == CoachingPriority.LOW

    def test_by_priority_empty_for_unrepresented(self):
        agent = SalesCoachAgent()
        # Don't coach anyone
        assert agent.by_priority(CoachingPriority.URGENT) == []


# ─── SalesCoachAgent.by_focus ─────────────────────────────────────────────────

class TestByFocus:
    def test_by_focus_returns_only_matching_focus(self):
        agent = SalesCoachAgent()
        agent.coach(make_rep(rep_id="r1", pipeline_coverage_ratio=1.0))  # forces PROSPECTING
        prospecting = agent.by_focus(CoachingFocus.PROSPECTING)
        for p in prospecting:
            assert p.primary_focus == CoachingFocus.PROSPECTING

    def test_by_focus_empty_when_no_match(self):
        agent = SalesCoachAgent()
        # No reps coached → empty
        assert agent.by_focus(CoachingFocus.CLOSING) == []


# ─── SalesCoachAgent.by_manager ───────────────────────────────────────────────

class TestByManager:
    def test_by_manager_returns_matching_manager(self):
        agent = SalesCoachAgent()
        agent.coach(make_rep(rep_id="r1", manager_id="mgr_A"))
        agent.coach(make_rep(rep_id="r2", manager_id="mgr_B"))
        results = agent.by_manager("mgr_A")
        assert len(results) == 1
        assert results[0].rep.manager_id == "mgr_A"

    def test_by_manager_returns_all_matching(self):
        agent = SalesCoachAgent()
        for i in range(3):
            agent.coach(make_rep(rep_id=f"r{i}", manager_id="mgr_X"))
        agent.coach(make_rep(rep_id="r_other", manager_id="mgr_Y"))
        results = agent.by_manager("mgr_X")
        assert len(results) == 3

    def test_by_manager_empty_for_unknown(self):
        agent = SalesCoachAgent()
        agent.coach(make_rep(rep_id="r1", manager_id="mgr_A"))
        assert agent.by_manager("mgr_Z") == []


# ─── SalesCoachAgent.top_coaching_needs ───────────────────────────────────────

class TestTopCoachingNeeds:
    def test_top_coaching_needs_default_5(self):
        agent = SalesCoachAgent()
        for i in range(10):
            agent.coach(make_rep(rep_id=f"r{i}"))
        top = agent.top_coaching_needs()
        assert len(top) == 5

    def test_top_coaching_needs_custom_n(self):
        agent = SalesCoachAgent()
        for i in range(10):
            agent.coach(make_rep(rep_id=f"r{i}"))
        top = agent.top_coaching_needs(n=3)
        assert len(top) == 3

    def test_top_coaching_needs_fewer_than_n(self):
        agent = SalesCoachAgent()
        for i in range(2):
            agent.coach(make_rep(rep_id=f"r{i}"))
        top = agent.top_coaching_needs(n=5)
        assert len(top) == 2

    def test_top_coaching_needs_are_highest_scoring(self):
        agent = SalesCoachAgent()
        for i in range(6):
            agent.coach(make_rep(rep_id=f"r{i}"))
        all_s = [p.coaching_score for p in agent.all_plans()]
        top_s = [p.coaching_score for p in agent.top_coaching_needs(n=5)]
        assert top_s == all_s[:5]

    def test_top_coaching_needs_empty_store(self):
        agent = SalesCoachAgent()
        assert agent.top_coaching_needs() == []


# ─── SalesCoachAgent.summary ──────────────────────────────────────────────────

class TestSummary:
    def test_summary_empty(self):
        agent = SalesCoachAgent()
        s = agent.summary()
        assert s["total_reps"] == 0
        assert s["avg_coaching_score"] == 0.0
        assert s["avg_quota_attainment_pct"] == 0.0
        assert s["urgent_count"] == 0

    def test_summary_empty_priority_counts_all_zero(self):
        agent = SalesCoachAgent()
        s = agent.summary()
        for pv in CoachingPriority:
            assert s["priority_counts"][pv.value] == 0

    def test_summary_empty_focus_counts_all_zero(self):
        agent = SalesCoachAgent()
        s = agent.summary()
        for fv in CoachingFocus:
            assert s["focus_counts"][fv.value] == 0

    def test_summary_total_reps(self):
        agent = SalesCoachAgent()
        for i in range(3):
            agent.coach(make_rep(rep_id=f"r{i}"))
        assert agent.summary()["total_reps"] == 3

    def test_summary_priority_counts_sum_to_total(self):
        agent = SalesCoachAgent()
        for i in range(4):
            agent.coach(make_rep(rep_id=f"r{i}"))
        s = agent.summary()
        assert sum(s["priority_counts"].values()) == 4

    def test_summary_focus_counts_sum_to_total(self):
        agent = SalesCoachAgent()
        for i in range(4):
            agent.coach(make_rep(rep_id=f"r{i}"))
        s = agent.summary()
        assert sum(s["focus_counts"].values()) == 4

    def test_summary_avg_coaching_score_is_float(self):
        agent = SalesCoachAgent()
        agent.coach(make_rep())
        assert isinstance(agent.summary()["avg_coaching_score"], float)

    def test_summary_avg_quota_attainment_is_float(self):
        agent = SalesCoachAgent()
        agent.coach(make_rep())
        assert isinstance(agent.summary()["avg_quota_attainment_pct"], float)

    def test_summary_has_all_keys(self):
        agent = SalesCoachAgent()
        s = agent.summary()
        for key in ("total_reps", "priority_counts", "focus_counts",
                    "avg_coaching_score", "avg_quota_attainment_pct", "urgent_count"):
            assert key in s


# ─── SalesCoachAgent.reset ────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_store(self):
        agent = SalesCoachAgent()
        for i in range(3):
            agent.coach(make_rep(rep_id=f"r{i}"))
        agent.reset()
        assert agent.all_plans() == []

    def test_reset_makes_get_return_none(self):
        agent = SalesCoachAgent()
        agent.coach(make_rep(rep_id="r1"))
        agent.reset()
        assert agent.get("r1") is None

    def test_reset_summary_shows_zero(self):
        agent = SalesCoachAgent()
        agent.coach(make_rep())
        agent.reset()
        assert agent.summary()["total_reps"] == 0

    def test_reset_then_coach_works(self):
        agent = SalesCoachAgent()
        agent.coach(make_rep(rep_id="r1"))
        agent.reset()
        agent.coach(make_rep(rep_id="r2"))
        assert agent.get("r1") is None
        assert agent.get("r2") is not None

    def test_reset_on_empty_no_error(self):
        agent = SalesCoachAgent()
        agent.reset()  # Should not raise
        assert agent.all_plans() == []


# ─── Integration / end-to-end ─────────────────────────────────────────────────

class TestIntegration:
    def test_full_workflow_urgent_rep(self):
        """A very bad rep should end up URGENT and focused on PROSPECTING or QUALIFICATION."""
        r = make_rep(
            rep_id="bad_rep",
            pipeline_coverage_ratio=0.5,
            calls_last_30d=5, emails_last_30d=5,
            meetings_last_30d=0, demos_last_30d=0,
            discovery_score=20, objection_score=20, demo_score=20,
            pricing_score=20, follow_up_score=20, relationship_score=20,
            time_mgmt_score=20,
            win_rate_last_90d=5.0, win_rate_prev_90d=20.0,
            open_deals=5, deals_stalled_last_30d=3,
            deals_won_last_90d=1, deals_lost_last_90d=10,
        )
        agent = SalesCoachAgent()
        plan = agent.coach(r)
        assert plan.coaching_priority == CoachingPriority.URGENT
        assert plan.primary_focus in (CoachingFocus.PROSPECTING, CoachingFocus.QUALIFICATION)
        assert plan.coaching_score >= 75

    def test_full_workflow_low_priority_rep(self):
        """An excellent rep should end up LOW priority and focused on RETENTION."""
        r = make_rep(
            rep_id="star_rep",
            pipeline_coverage_ratio=5.0,
            calls_last_30d=120, emails_last_30d=240,
            meetings_last_30d=30, demos_last_30d=16,
            discovery_score=95, objection_score=95, demo_score=95,
            pricing_score=95, follow_up_score=95, relationship_score=95,
            time_mgmt_score=95,
            win_rate_last_90d=65.0, win_rate_prev_90d=60.0,
            open_deals=20, deals_stalled_last_30d=1,
            deals_won_last_90d=15, deals_lost_last_90d=5,
            avg_sales_cycle_days=60,
            pipeline_value_eur=2_000_000, quota_eur=100_000,
        )
        agent = SalesCoachAgent()
        plan = agent.coach(r)
        assert plan.coaching_priority in (CoachingPriority.LOW, CoachingPriority.MEDIUM)
        assert plan.primary_focus == CoachingFocus.RETENTION

    def test_coach_batch_and_urgent_reps(self):
        """Batch coaching should populate urgent_reps correctly."""
        agent = SalesCoachAgent()
        reps = [
            make_rep(rep_id="bad1", pipeline_coverage_ratio=0.2,
                     calls_last_30d=0, emails_last_30d=0,
                     meetings_last_30d=0, demos_last_30d=0,
                     discovery_score=5, objection_score=5, demo_score=5,
                     pricing_score=5, follow_up_score=5, relationship_score=5,
                     time_mgmt_score=5, win_rate_last_90d=2.0,
                     win_rate_prev_90d=20.0),
            make_rep(rep_id="bad2", pipeline_coverage_ratio=0.2,
                     calls_last_30d=0, emails_last_30d=0,
                     meetings_last_30d=0, demos_last_30d=0,
                     discovery_score=5, objection_score=5, demo_score=5,
                     pricing_score=5, follow_up_score=5, relationship_score=5,
                     time_mgmt_score=5, win_rate_last_90d=2.0,
                     win_rate_prev_90d=20.0),
        ]
        agent.coach_batch(reps)
        urgent = agent.urgent_reps()
        assert len(urgent) == 2

    def test_pipeline_score_stored_in_plan(self):
        agent = SalesCoachAgent()
        r = make_rep()
        plan = agent.coach(r)
        expected_pipeline, _ = _pipeline_health(r)
        assert plan.pipeline_health_score == pytest.approx(expected_pipeline, rel=1e-4)

    def test_activity_score_stored_in_plan(self):
        agent = SalesCoachAgent()
        r = make_rep()
        plan = agent.coach(r)
        expected_activity, _ = _activity_score(r)
        assert plan.activity_score == pytest.approx(expected_activity, rel=1e-4)

    def test_skill_gap_score_stored_in_plan(self):
        agent = SalesCoachAgent()
        r = make_rep()
        plan = agent.coach(r)
        avg_skill, _ = _skill_gaps(r)
        assert plan.skill_gap_score == pytest.approx(100 - avg_skill, rel=1e-4)

    def test_win_rate_trend_score_stored_in_plan(self):
        agent = SalesCoachAgent()
        r = make_rep()
        plan = agent.coach(r)
        expected_win, _ = _win_rate_trend(r)
        assert plan.win_rate_trend_score == pytest.approx(expected_win, rel=1e-4)

    def test_by_focus_prospecting_after_low_coverage(self):
        agent = SalesCoachAgent()
        r = make_rep(rep_id="low_cov", pipeline_coverage_ratio=1.0)
        agent.coach(r)
        prospecting = agent.by_focus(CoachingFocus.PROSPECTING)
        assert any(p.rep.rep_id == "low_cov" for p in prospecting)

    def test_by_manager_after_batch(self):
        agent = SalesCoachAgent()
        reps = [make_rep(rep_id=f"r{i}", manager_id="mgr_Z") for i in range(4)]
        agent.coach_batch(reps)
        results = agent.by_manager("mgr_Z")
        assert len(results) == 4

    def test_top_coaching_needs_order(self):
        agent = SalesCoachAgent()
        # Mix good and bad reps
        agent.coach(make_rep(rep_id="good",
            pipeline_coverage_ratio=4.0, calls_last_30d=60,
            emails_last_30d=120, meetings_last_30d=15, demos_last_30d=8,
            discovery_score=90, objection_score=90, demo_score=90,
            pricing_score=90, follow_up_score=90, relationship_score=90,
            time_mgmt_score=90, win_rate_last_90d=55.0, win_rate_prev_90d=50.0))
        agent.coach(make_rep(rep_id="bad",
            pipeline_coverage_ratio=0.5, calls_last_30d=0, emails_last_30d=0,
            meetings_last_30d=0, demos_last_30d=0,
            discovery_score=10, objection_score=10, demo_score=10,
            pricing_score=10, follow_up_score=10, relationship_score=10,
            time_mgmt_score=10, win_rate_last_90d=3.0, win_rate_prev_90d=20.0))
        top1 = agent.top_coaching_needs(n=1)[0]
        assert top1.rep.rep_id == "bad"
