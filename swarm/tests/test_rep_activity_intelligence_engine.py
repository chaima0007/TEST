"""
Comprehensive pytest tests for RepActivityIntelligenceEngine (Module 37).

Import path: swarm.intelligence.rep_activity_intelligence_engine
Run from /home/user/TEST:
    python -m pytest swarm/tests/test_rep_activity_intelligence_engine.py -v
"""

import pytest
from swarm.intelligence.rep_activity_intelligence_engine import (
    ActivityTier,
    ActivityTrend,
    CoachingFocus,
    ActivityAction,
    RepActivityInput,
    RepActivityResult,
    RepActivityIntelligenceEngine,
)


# ─── Helper ───────────────────────────────────────────────────────────────────

def make_input(
    rep_id="R001",
    rep_name="Alice",
    region="EMEA",
    segment="Enterprise",
    calls_30d=100,
    emails_30d=200,
    meetings_booked_30d=20,
    proposals_30d=10,
    linkedin_touches_30d=50,
    follow_ups_30d=30,
    calls_7d=25,
    emails_7d=50,
    meetings_7d=5,
    benchmark_calls_30d=100,
    benchmark_emails_30d=200,
    benchmark_meetings_30d=20,
    benchmark_proposals_30d=10,
    connect_rate_pct=20.0,
    email_reply_rate_pct=15.0,
    meeting_show_rate_pct=80.0,
    deals_created_30d=5,
    pipeline_generated_eur=100000.0,
    quota_attainment_pct=80.0,
) -> RepActivityInput:
    """Return a RepActivityInput with all benchmarks met by default (score ~100)."""
    return RepActivityInput(
        rep_id=rep_id,
        rep_name=rep_name,
        region=region,
        segment=segment,
        calls_30d=calls_30d,
        emails_30d=emails_30d,
        meetings_booked_30d=meetings_booked_30d,
        proposals_30d=proposals_30d,
        linkedin_touches_30d=linkedin_touches_30d,
        follow_ups_30d=follow_ups_30d,
        calls_7d=calls_7d,
        emails_7d=emails_7d,
        meetings_7d=meetings_7d,
        benchmark_calls_30d=benchmark_calls_30d,
        benchmark_emails_30d=benchmark_emails_30d,
        benchmark_meetings_30d=benchmark_meetings_30d,
        benchmark_proposals_30d=benchmark_proposals_30d,
        connect_rate_pct=connect_rate_pct,
        email_reply_rate_pct=email_reply_rate_pct,
        meeting_show_rate_pct=meeting_show_rate_pct,
        deals_created_30d=deals_created_30d,
        pipeline_generated_eur=pipeline_generated_eur,
        quota_attainment_pct=quota_attainment_pct,
    )


@pytest.fixture
def engine():
    return RepActivityIntelligenceEngine()


# ═══════════════════════════════════════════════════════════════════════════════
# 1. Enum values and str inheritance
# ═══════════════════════════════════════════════════════════════════════════════

class TestActivityTierEnum:
    def test_elite_value(self):
        assert ActivityTier.ELITE == "elite"

    def test_high_value(self):
        assert ActivityTier.HIGH == "high"

    def test_average_value(self):
        assert ActivityTier.AVERAGE == "average"

    def test_low_value(self):
        assert ActivityTier.LOW == "low"

    def test_inactive_value(self):
        assert ActivityTier.INACTIVE == "inactive"

    def test_is_str(self):
        assert isinstance(ActivityTier.ELITE, str)

    def test_all_five_members(self):
        assert len(ActivityTier) == 5


class TestActivityTrendEnum:
    def test_accelerating_value(self):
        assert ActivityTrend.ACCELERATING == "accelerating"

    def test_stable_value(self):
        assert ActivityTrend.STABLE == "stable"

    def test_declining_value(self):
        assert ActivityTrend.DECLINING == "declining"

    def test_stalled_value(self):
        assert ActivityTrend.STALLED == "stalled"

    def test_is_str(self):
        assert isinstance(ActivityTrend.STALLED, str)

    def test_all_four_members(self):
        assert len(ActivityTrend) == 4


class TestCoachingFocusEnum:
    def test_calls_value(self):
        assert CoachingFocus.CALLS == "calls"

    def test_emails_value(self):
        assert CoachingFocus.EMAILS == "emails"

    def test_meetings_value(self):
        assert CoachingFocus.MEETINGS == "meetings"

    def test_prospecting_value(self):
        assert CoachingFocus.PROSPECTING == "prospecting"

    def test_follow_up_value(self):
        assert CoachingFocus.FOLLOW_UP == "follow_up"

    def test_quality_value(self):
        assert CoachingFocus.QUALITY == "quality"

    def test_on_track_value(self):
        assert CoachingFocus.ON_TRACK == "on_track"

    def test_is_str(self):
        assert isinstance(CoachingFocus.ON_TRACK, str)

    def test_all_seven_members(self):
        assert len(CoachingFocus) == 7


class TestActivityActionEnum:
    def test_celebrate_value(self):
        assert ActivityAction.CELEBRATE == "celebrate"

    def test_maintain_value(self):
        assert ActivityAction.MAINTAIN == "maintain"

    def test_nudge_value(self):
        assert ActivityAction.NUDGE == "nudge"

    def test_coach_value(self):
        assert ActivityAction.COACH == "coach"

    def test_intervene_value(self):
        assert ActivityAction.INTERVENE == "intervene"

    def test_is_str(self):
        assert isinstance(ActivityAction.CELEBRATE, str)

    def test_all_five_members(self):
        assert len(ActivityAction) == 5


# ═══════════════════════════════════════════════════════════════════════════════
# 2. RepActivityInput field count
# ═══════════════════════════════════════════════════════════════════════════════

class TestRepActivityInputFields:
    def test_field_count(self):
        inp = make_input()
        import dataclasses
        fields = dataclasses.fields(inp)
        # The dataclass defines 23 fields (22 documented + quota_attainment_pct)
        assert len(fields) == 23

    def test_identity_fields(self):
        inp = make_input(rep_id="X1", rep_name="Bob", region="APAC", segment="SMB")
        assert inp.rep_id == "X1"
        assert inp.rep_name == "Bob"
        assert inp.region == "APAC"
        assert inp.segment == "SMB"

    def test_activity_30d_fields(self):
        inp = make_input(
            calls_30d=10, emails_30d=20, meetings_booked_30d=3,
            proposals_30d=2, linkedin_touches_30d=5, follow_ups_30d=7,
        )
        assert inp.calls_30d == 10
        assert inp.emails_30d == 20
        assert inp.meetings_booked_30d == 3
        assert inp.proposals_30d == 2
        assert inp.linkedin_touches_30d == 5
        assert inp.follow_ups_30d == 7

    def test_activity_7d_fields(self):
        inp = make_input(calls_7d=3, emails_7d=8, meetings_7d=1)
        assert inp.calls_7d == 3
        assert inp.emails_7d == 8
        assert inp.meetings_7d == 1

    def test_benchmark_fields(self):
        inp = make_input(
            benchmark_calls_30d=80, benchmark_emails_30d=160,
            benchmark_meetings_30d=16, benchmark_proposals_30d=8,
        )
        assert inp.benchmark_calls_30d == 80
        assert inp.benchmark_emails_30d == 160
        assert inp.benchmark_meetings_30d == 16
        assert inp.benchmark_proposals_30d == 8

    def test_conversion_fields(self):
        inp = make_input(connect_rate_pct=22.5, email_reply_rate_pct=12.0, meeting_show_rate_pct=90.0)
        assert inp.connect_rate_pct == 22.5
        assert inp.email_reply_rate_pct == 12.0
        assert inp.meeting_show_rate_pct == 90.0

    def test_output_fields(self):
        inp = make_input(deals_created_30d=7, pipeline_generated_eur=250000.0, quota_attainment_pct=110.0)
        assert inp.deals_created_30d == 7
        assert inp.pipeline_generated_eur == 250000.0
        assert inp.quota_attainment_pct == 110.0


# ═══════════════════════════════════════════════════════════════════════════════
# 3. _index() helper
# ═══════════════════════════════════════════════════════════════════════════════

class TestIndexHelper:
    def test_normal_equal(self, engine):
        assert engine._index(100, 100) == 1.0

    def test_normal_above(self, engine):
        assert engine._index(150, 100) == 1.5

    def test_normal_below(self, engine):
        assert engine._index(50, 100) == 0.5

    def test_zero_benchmark_returns_one(self, engine):
        assert engine._index(50, 0) == 1.0

    def test_negative_benchmark_returns_one(self, engine):
        assert engine._index(50, -5) == 1.0

    def test_zero_actual(self, engine):
        assert engine._index(0, 100) == 0.0

    def test_rounding_two_decimals(self, engine):
        # 1/3 rounds to 0.33
        result = engine._index(1, 3)
        assert result == 0.33

    def test_exact_fraction(self, engine):
        assert engine._index(25, 100) == 0.25

    def test_zero_both(self, engine):
        assert engine._index(0, 0) == 1.0


# ═══════════════════════════════════════════════════════════════════════════════
# 4. _activity_score — each component, capping, clamping
# ═══════════════════════════════════════════════════════════════════════════════

class TestActivityScore:
    def test_perfect_score(self, engine):
        # All at benchmark, conversion maxed
        inp = make_input(
            connect_rate_pct=100.0, email_reply_rate_pct=100.0, meeting_show_rate_pct=100.0
        )
        score = engine._activity_score(inp)
        assert score == 100.0

    def test_zero_score(self, engine):
        inp = make_input(
            calls_30d=0, emails_30d=0, meetings_booked_30d=0, proposals_30d=0,
            connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
            benchmark_calls_30d=100, benchmark_emails_30d=200,
            benchmark_meetings_30d=20, benchmark_proposals_30d=10,
        )
        score = engine._activity_score(inp)
        assert score == 0.0

    def test_call_pts_cap_at_25(self, engine):
        # calls 200% of benchmark => index=2, raw call_pts=50 => capped at 25
        inp = make_input(
            calls_30d=200, benchmark_calls_30d=100,
            emails_30d=0, benchmark_emails_30d=200,
            meetings_booked_30d=0, benchmark_meetings_30d=20,
            proposals_30d=0, benchmark_proposals_30d=10,
            connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
        )
        score = engine._activity_score(inp)
        assert score == 25.0

    def test_email_pts_cap_at_20(self, engine):
        inp = make_input(
            calls_30d=0, benchmark_calls_30d=100,
            emails_30d=400, benchmark_emails_30d=200,
            meetings_booked_30d=0, benchmark_meetings_30d=20,
            proposals_30d=0, benchmark_proposals_30d=10,
            connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
        )
        score = engine._activity_score(inp)
        assert score == 20.0

    def test_meeting_pts_cap_at_20(self, engine):
        inp = make_input(
            calls_30d=0, benchmark_calls_30d=100,
            emails_30d=0, benchmark_emails_30d=200,
            meetings_booked_30d=40, benchmark_meetings_30d=20,
            proposals_30d=0, benchmark_proposals_30d=10,
            connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
        )
        score = engine._activity_score(inp)
        assert score == 20.0

    def test_proposal_pts_cap_at_15(self, engine):
        inp = make_input(
            calls_30d=0, benchmark_calls_30d=100,
            emails_30d=0, benchmark_emails_30d=200,
            meetings_booked_30d=0, benchmark_meetings_30d=20,
            proposals_30d=20, benchmark_proposals_30d=10,
            connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
        )
        score = engine._activity_score(inp)
        assert score == 15.0

    def test_connect_pts_cap_at_10(self, engine):
        inp = make_input(
            calls_30d=0, benchmark_calls_30d=100,
            emails_30d=0, benchmark_emails_30d=200,
            meetings_booked_30d=0, benchmark_meetings_30d=20,
            proposals_30d=0, benchmark_proposals_30d=10,
            connect_rate_pct=200.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
        )
        score = engine._activity_score(inp)
        assert score == 10.0

    def test_reply_pts_cap_at_5(self, engine):
        inp = make_input(
            calls_30d=0, benchmark_calls_30d=100,
            emails_30d=0, benchmark_emails_30d=200,
            meetings_booked_30d=0, benchmark_meetings_30d=20,
            proposals_30d=0, benchmark_proposals_30d=10,
            connect_rate_pct=0.0, email_reply_rate_pct=200.0, meeting_show_rate_pct=0.0,
        )
        score = engine._activity_score(inp)
        assert score == 5.0

    def test_show_pts_cap_at_5(self, engine):
        inp = make_input(
            calls_30d=0, benchmark_calls_30d=100,
            emails_30d=0, benchmark_emails_30d=200,
            meetings_booked_30d=0, benchmark_meetings_30d=20,
            proposals_30d=0, benchmark_proposals_30d=10,
            connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=200.0,
        )
        score = engine._activity_score(inp)
        assert score == 5.0

    def test_partial_connect_pts(self, engine):
        # connect_rate_pct=50 => 50/10=5 pts
        inp = make_input(
            calls_30d=0, benchmark_calls_30d=100,
            emails_30d=0, benchmark_emails_30d=200,
            meetings_booked_30d=0, benchmark_meetings_30d=20,
            proposals_30d=0, benchmark_proposals_30d=10,
            connect_rate_pct=50.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
        )
        score = engine._activity_score(inp)
        assert score == 5.0

    def test_score_is_numeric(self, engine):
        inp = make_input()
        score = engine._activity_score(inp)
        assert isinstance(score, (int, float))

    def test_score_clamped_below_100(self, engine):
        inp = make_input(
            connect_rate_pct=1000.0, email_reply_rate_pct=1000.0, meeting_show_rate_pct=1000.0,
            calls_30d=10000, emails_30d=10000, meetings_booked_30d=10000, proposals_30d=10000,
        )
        assert engine._activity_score(inp) <= 100.0

    def test_score_nonnegative(self, engine):
        inp = make_input(
            calls_30d=0, emails_30d=0, meetings_booked_30d=0, proposals_30d=0,
            connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
        )
        assert engine._activity_score(inp) >= 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# 5. _activity_tier — all 5 thresholds (both sides)
# ═══════════════════════════════════════════════════════════════════════════════

class TestActivityTier:
    def test_elite_at_85(self, engine):
        assert engine._activity_tier(85.0) == ActivityTier.ELITE

    def test_elite_above_85(self, engine):
        assert engine._activity_tier(99.9) == ActivityTier.ELITE

    def test_elite_at_100(self, engine):
        assert engine._activity_tier(100.0) == ActivityTier.ELITE

    def test_high_just_below_85(self, engine):
        assert engine._activity_tier(84.9) == ActivityTier.HIGH

    def test_high_at_65(self, engine):
        assert engine._activity_tier(65.0) == ActivityTier.HIGH

    def test_high_midpoint(self, engine):
        assert engine._activity_tier(75.0) == ActivityTier.HIGH

    def test_average_just_below_65(self, engine):
        assert engine._activity_tier(64.9) == ActivityTier.AVERAGE

    def test_average_at_45(self, engine):
        assert engine._activity_tier(45.0) == ActivityTier.AVERAGE

    def test_average_midpoint(self, engine):
        assert engine._activity_tier(55.0) == ActivityTier.AVERAGE

    def test_low_just_below_45(self, engine):
        assert engine._activity_tier(44.9) == ActivityTier.LOW

    def test_low_at_20(self, engine):
        assert engine._activity_tier(20.0) == ActivityTier.LOW

    def test_low_midpoint(self, engine):
        assert engine._activity_tier(32.0) == ActivityTier.LOW

    def test_inactive_just_below_20(self, engine):
        assert engine._activity_tier(19.9) == ActivityTier.INACTIVE

    def test_inactive_at_zero(self, engine):
        assert engine._activity_tier(0.0) == ActivityTier.INACTIVE

    def test_inactive_midpoint(self, engine):
        assert engine._activity_tier(10.0) == ActivityTier.INACTIVE


# ═══════════════════════════════════════════════════════════════════════════════
# 6. _activity_trend — all 4 outcomes
# ═══════════════════════════════════════════════════════════════════════════════

class TestActivityTrend:
    def test_stable_at_benchmark(self, engine):
        # 7d pace = 30d/4 exactly => ratio=1.0 => STABLE
        inp = make_input(
            calls_30d=100, emails_30d=200, meetings_booked_30d=20,
            calls_7d=25, emails_7d=50, meetings_7d=5,
            benchmark_calls_30d=100, benchmark_emails_30d=200, benchmark_meetings_30d=20,
        )
        assert engine._activity_trend(inp) == ActivityTrend.STABLE

    def test_accelerating_ratio_ge_1_2(self, engine):
        # total_30=100, expected_7=25, total_7=30 => ratio=1.2 => ACCELERATING
        inp = make_input(
            calls_30d=100, emails_30d=0, meetings_booked_30d=0,
            calls_7d=30, emails_7d=0, meetings_7d=0,
            benchmark_calls_30d=100, benchmark_emails_30d=200, benchmark_meetings_30d=20,
        )
        assert engine._activity_trend(inp) == ActivityTrend.ACCELERATING

    def test_accelerating_well_above(self, engine):
        # total_30=40, expected_7=10, total_7=20 => ratio=2.0 => ACCELERATING
        inp = make_input(
            calls_30d=40, emails_30d=0, meetings_booked_30d=0,
            calls_7d=20, emails_7d=0, meetings_7d=0,
            benchmark_calls_30d=100, benchmark_emails_30d=200, benchmark_meetings_30d=20,
        )
        assert engine._activity_trend(inp) == ActivityTrend.ACCELERATING

    def test_declining_ratio_le_0_8(self, engine):
        # total_30=100, expected_7=25, total_7=20 => ratio=0.8 => DECLINING
        inp = make_input(
            calls_30d=100, emails_30d=0, meetings_booked_30d=0,
            calls_7d=20, emails_7d=0, meetings_7d=0,
            benchmark_calls_30d=100, benchmark_emails_30d=200, benchmark_meetings_30d=20,
        )
        assert engine._activity_trend(inp) == ActivityTrend.DECLINING

    def test_declining_well_below(self, engine):
        # total_30=100, expected_7=25, total_7=5 => ratio=0.2 => DECLINING
        # BUT also check STALLED: benchmark_weekly=(100+200+20)/4=80, total_7=5
        # 5 < 80*0.2=16 => STALLED wins first
        # Use low benchmark to avoid STALLED:
        inp = make_input(
            calls_30d=100, emails_30d=0, meetings_booked_30d=0,
            calls_7d=5, emails_7d=0, meetings_7d=0,
            benchmark_calls_30d=0, benchmark_emails_30d=0, benchmark_meetings_30d=0,
        )
        # benchmark_weekly=0 so STALLED won't trigger, expected_7=25, total_7=5, ratio=0.2 => DECLINING
        assert engine._activity_trend(inp) == ActivityTrend.DECLINING

    def test_stalled_below_20pct_benchmark(self, engine):
        # benchmark_weekly=(100+200+20)/4=80, need total_7 < 16
        inp = make_input(
            calls_30d=100, emails_30d=200, meetings_booked_30d=20,
            calls_7d=5, emails_7d=5, meetings_7d=1,  # total_7=11 < 16
            benchmark_calls_30d=100, benchmark_emails_30d=200, benchmark_meetings_30d=20,
        )
        assert engine._activity_trend(inp) == ActivityTrend.STALLED

    def test_stalled_boundary_exact_19pct(self, engine):
        # benchmark_weekly=80, 19.9% would be 15.9 => total_7=15 < 16 => STALLED
        inp = make_input(
            calls_30d=200, emails_30d=0, meetings_booked_30d=0,
            calls_7d=15, emails_7d=0, meetings_7d=0,
            benchmark_calls_30d=100, benchmark_emails_30d=200, benchmark_meetings_30d=20,
        )
        assert engine._activity_trend(inp) == ActivityTrend.STALLED

    def test_stalled_zero_benchmarks_no_trigger(self, engine):
        # benchmark_weekly=0 so STALLED doesn't trigger
        inp = make_input(
            calls_30d=0, emails_30d=0, meetings_booked_30d=0,
            calls_7d=0, emails_7d=0, meetings_7d=0,
            benchmark_calls_30d=0, benchmark_emails_30d=0, benchmark_meetings_30d=0,
        )
        # expected_7=0 => STABLE
        assert engine._activity_trend(inp) == ActivityTrend.STABLE

    def test_stable_when_expected7_zero_no_30d(self, engine):
        # total_30=0 => expected_7=0 => STABLE (after STALLED check)
        inp = make_input(
            calls_30d=0, emails_30d=0, meetings_booked_30d=0,
            calls_7d=0, emails_7d=0, meetings_7d=0,
            benchmark_calls_30d=0, benchmark_emails_30d=0, benchmark_meetings_30d=0,
        )
        assert engine._activity_trend(inp) == ActivityTrend.STABLE

    def test_ratio_exactly_1_2_accelerating(self, engine):
        # total_30=80, expected_7=20, total_7=24 => ratio=1.2 => ACCELERATING
        inp = make_input(
            calls_30d=80, emails_30d=0, meetings_booked_30d=0,
            calls_7d=24, emails_7d=0, meetings_7d=0,
            benchmark_calls_30d=0, benchmark_emails_30d=0, benchmark_meetings_30d=0,
        )
        assert engine._activity_trend(inp) == ActivityTrend.ACCELERATING

    def test_ratio_0_9_stable(self, engine):
        # total_30=100, expected_7=25, total_7=22 => ratio=0.88 > 0.8 and < 1.2 => STABLE
        inp = make_input(
            calls_30d=100, emails_30d=0, meetings_booked_30d=0,
            calls_7d=22, emails_7d=0, meetings_7d=0,
            benchmark_calls_30d=0, benchmark_emails_30d=0, benchmark_meetings_30d=0,
        )
        assert engine._activity_trend(inp) == ActivityTrend.STABLE


# ═══════════════════════════════════════════════════════════════════════════════
# 7. _coaching_focus — all 7 values
# ═══════════════════════════════════════════════════════════════════════════════

class TestCoachingFocus:
    def test_on_track_all_above_threshold(self, engine):
        # All indices >=0.8, connect>=15, reply>=10, follow_ups>=5
        inp = make_input(
            calls_30d=100, benchmark_calls_30d=100,
            emails_30d=200, benchmark_emails_30d=200,
            meetings_booked_30d=20, benchmark_meetings_30d=20,
            proposals_30d=10, benchmark_proposals_30d=10,
            connect_rate_pct=20.0,
            email_reply_rate_pct=15.0,
            follow_ups_30d=10,
        )
        assert engine._coaching_focus(inp) == CoachingFocus.ON_TRACK

    def test_quality_low_connect_rate(self, engine):
        # All indices >=0.8, connect_rate < 15
        inp = make_input(
            calls_30d=100, benchmark_calls_30d=100,
            emails_30d=200, benchmark_emails_30d=200,
            meetings_booked_30d=20, benchmark_meetings_30d=20,
            proposals_30d=10, benchmark_proposals_30d=10,
            connect_rate_pct=10.0,  # < 15
            email_reply_rate_pct=15.0,
            follow_ups_30d=10,
        )
        assert engine._coaching_focus(inp) == CoachingFocus.QUALITY

    def test_quality_low_email_reply_rate(self, engine):
        # All indices >=0.8, connect >=15, email_reply < 10
        inp = make_input(
            calls_30d=100, benchmark_calls_30d=100,
            emails_30d=200, benchmark_emails_30d=200,
            meetings_booked_30d=20, benchmark_meetings_30d=20,
            proposals_30d=10, benchmark_proposals_30d=10,
            connect_rate_pct=20.0,
            email_reply_rate_pct=8.0,  # < 10
            follow_ups_30d=10,
        )
        assert engine._coaching_focus(inp) == CoachingFocus.QUALITY

    def test_follow_up_below_5(self, engine):
        # All indices >=0.8, connect>=15, reply>=10, follow_ups < 5
        inp = make_input(
            calls_30d=100, benchmark_calls_30d=100,
            emails_30d=200, benchmark_emails_30d=200,
            meetings_booked_30d=20, benchmark_meetings_30d=20,
            proposals_30d=10, benchmark_proposals_30d=10,
            connect_rate_pct=20.0,
            email_reply_rate_pct=15.0,
            follow_ups_30d=4,  # < 5
        )
        assert engine._coaching_focus(inp) == CoachingFocus.FOLLOW_UP

    def test_calls_focus_min_index(self, engine):
        # calls index = 0.0, all others >=0.8 -> CALLS is worst
        inp = make_input(
            calls_30d=0, benchmark_calls_30d=100,      # index=0.0 (lowest)
            emails_30d=200, benchmark_emails_30d=200,  # index=1.0
            meetings_booked_30d=20, benchmark_meetings_30d=20,  # index=1.0
            proposals_30d=10, benchmark_proposals_30d=10,        # index=1.0
        )
        assert engine._coaching_focus(inp) == CoachingFocus.CALLS

    def test_emails_focus_min_index(self, engine):
        # emails index = 0.1, calls=1.0, meetings=1.0, proposals=1.0 => EMAILS worst
        inp = make_input(
            calls_30d=100, benchmark_calls_30d=100,
            emails_30d=20, benchmark_emails_30d=200,    # index=0.1
            meetings_booked_30d=20, benchmark_meetings_30d=20,
            proposals_30d=10, benchmark_proposals_30d=10,
        )
        assert engine._coaching_focus(inp) == CoachingFocus.EMAILS

    def test_meetings_focus_min_index(self, engine):
        # meetings index lowest
        inp = make_input(
            calls_30d=100, benchmark_calls_30d=100,
            emails_30d=200, benchmark_emails_30d=200,
            meetings_booked_30d=2, benchmark_meetings_30d=20,   # index=0.1
            proposals_30d=10, benchmark_proposals_30d=10,
        )
        assert engine._coaching_focus(inp) == CoachingFocus.MEETINGS

    def test_prospecting_focus_min_index(self, engine):
        # proposals index lowest (and <0.8)
        inp = make_input(
            calls_30d=100, benchmark_calls_30d=100,
            emails_30d=200, benchmark_emails_30d=200,
            meetings_booked_30d=20, benchmark_meetings_30d=20,
            proposals_30d=1, benchmark_proposals_30d=10,        # index=0.1
        )
        assert engine._coaching_focus(inp) == CoachingFocus.PROSPECTING

    def test_all_zero_benchmarks_on_track(self, engine):
        # All benchmarks=0 => all indices=1.0 >=0.8
        # connect=20, reply=15, follow_ups=10 => ON_TRACK
        inp = make_input(
            benchmark_calls_30d=0, benchmark_emails_30d=0,
            benchmark_meetings_30d=0, benchmark_proposals_30d=0,
            connect_rate_pct=20.0, email_reply_rate_pct=15.0, follow_ups_30d=10,
        )
        assert engine._coaching_focus(inp) == CoachingFocus.ON_TRACK


# ═══════════════════════════════════════════════════════════════════════════════
# 8. _activity_action — all 5 outcomes
# ═══════════════════════════════════════════════════════════════════════════════

class TestActivityAction:
    def test_celebrate_for_elite(self, engine):
        assert engine._activity_action(ActivityTier.ELITE) == ActivityAction.CELEBRATE

    def test_maintain_for_high(self, engine):
        assert engine._activity_action(ActivityTier.HIGH) == ActivityAction.MAINTAIN

    def test_nudge_for_average(self, engine):
        assert engine._activity_action(ActivityTier.AVERAGE) == ActivityAction.NUDGE

    def test_coach_for_low(self, engine):
        assert engine._activity_action(ActivityTier.LOW) == ActivityAction.COACH

    def test_intervene_for_inactive(self, engine):
        assert engine._activity_action(ActivityTier.INACTIVE) == ActivityAction.INTERVENE


# ═══════════════════════════════════════════════════════════════════════════════
# 9. to_dict() — 20 keys, enum serialization, lists present
# ═══════════════════════════════════════════════════════════════════════════════

class TestToDict:
    def test_returns_dict(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict(), dict)

    def test_exactly_20_keys(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert len(d) == 20

    def test_all_expected_keys_present(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        expected_keys = {
            "rep_id", "rep_name", "region", "segment",
            "activity_tier", "activity_trend", "coaching_focus", "activity_action",
            "activity_score", "call_index", "email_index", "meeting_index", "proposal_index",
            "connect_rate_pct", "email_reply_rate_pct", "meeting_show_rate_pct",
            "deals_created_30d", "pipeline_generated_eur",
            "coaching_insights", "action_items",
        }
        assert set(d.keys()) == expected_keys

    def test_enum_values_are_strings(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert isinstance(d["activity_tier"], str)
        assert isinstance(d["activity_trend"], str)
        assert isinstance(d["coaching_focus"], str)
        assert isinstance(d["activity_action"], str)

    def test_enum_not_enum_objects(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert not isinstance(d["activity_tier"], ActivityTier)
        assert not isinstance(d["activity_trend"], ActivityTrend)

    def test_coaching_insights_is_list(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["coaching_insights"], list)

    def test_action_items_is_list(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["action_items"], list)

    def test_activity_score_numeric(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert isinstance(d["activity_score"], (int, float))

    def test_pipeline_numeric(self, engine):
        result = engine.analyze(make_input(pipeline_generated_eur=55000.0))
        d = result.to_dict()
        assert isinstance(d["pipeline_generated_eur"], (int, float))
        assert d["pipeline_generated_eur"] == 55000.0

    def test_rep_id_preserved(self, engine):
        result = engine.analyze(make_input(rep_id="XYZ99"))
        assert result.to_dict()["rep_id"] == "XYZ99"


# ═══════════════════════════════════════════════════════════════════════════════
# 10. analyze() — return type, stored, field preservation
# ═══════════════════════════════════════════════════════════════════════════════

class TestAnalyze:
    def test_returns_rep_activity_result(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result, RepActivityResult)

    def test_result_stored_in_engine(self, engine):
        engine.analyze(make_input())
        assert len(engine.all_reps()) == 1

    def test_multiple_analyze_all_stored(self, engine):
        engine.analyze(make_input(rep_id="R1"))
        engine.analyze(make_input(rep_id="R2"))
        engine.analyze(make_input(rep_id="R3"))
        assert len(engine.all_reps()) == 3

    def test_rep_id_preserved(self, engine):
        result = engine.analyze(make_input(rep_id="REP42"))
        assert result.rep_id == "REP42"

    def test_rep_name_preserved(self, engine):
        result = engine.analyze(make_input(rep_name="Charlie"))
        assert result.rep_name == "Charlie"

    def test_region_preserved(self, engine):
        result = engine.analyze(make_input(region="LATAM"))
        assert result.region == "LATAM"

    def test_segment_preserved(self, engine):
        result = engine.analyze(make_input(segment="SMB"))
        assert result.segment == "SMB"

    def test_activity_tier_is_enum(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.activity_tier, ActivityTier)

    def test_activity_trend_is_enum(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.activity_trend, ActivityTrend)

    def test_coaching_focus_is_enum(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.coaching_focus, CoachingFocus)

    def test_activity_action_is_enum(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.activity_action, ActivityAction)

    def test_deals_created_preserved(self, engine):
        result = engine.analyze(make_input(deals_created_30d=9))
        assert result.deals_created_30d == 9

    def test_pipeline_eur_preserved(self, engine):
        result = engine.analyze(make_input(pipeline_generated_eur=77777.0))
        assert result.pipeline_generated_eur == 77777.0

    def test_coaching_insights_nonempty(self, engine):
        result = engine.analyze(make_input())
        assert len(result.coaching_insights) >= 1

    def test_action_items_nonempty(self, engine):
        result = engine.analyze(make_input())
        assert len(result.action_items) >= 1


# ═══════════════════════════════════════════════════════════════════════════════
# 11. analyze_batch() — DESC sort, count, empty
# ═══════════════════════════════════════════════════════════════════════════════

class TestAnalyzeBatch:
    def test_returns_list(self, engine):
        results = engine.analyze_batch([make_input()])
        assert isinstance(results, list)

    def test_empty_input(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_count_matches_input(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_sorted_desc_by_activity_score(self, engine):
        # Rep A: all zeros (low score), Rep B: all max (high score)
        low = make_input(
            rep_id="LOW",
            calls_30d=0, emails_30d=0, meetings_booked_30d=0, proposals_30d=0,
            connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
        )
        high = make_input(
            rep_id="HIGH",
            connect_rate_pct=100.0, email_reply_rate_pct=100.0, meeting_show_rate_pct=100.0,
        )
        results = engine.analyze_batch([low, high])
        assert results[0].activity_score >= results[1].activity_score

    def test_sorted_desc_three_reps(self, engine):
        inputs = [
            make_input(rep_id="R1", calls_30d=10, benchmark_calls_30d=100,
                       emails_30d=10, benchmark_emails_30d=200,
                       meetings_booked_30d=1, benchmark_meetings_30d=20,
                       proposals_30d=1, benchmark_proposals_30d=10,
                       connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0),
            make_input(rep_id="R2", connect_rate_pct=100.0, email_reply_rate_pct=100.0,
                       meeting_show_rate_pct=100.0),
            make_input(rep_id="R3", calls_30d=50, benchmark_calls_30d=100,
                       emails_30d=100, benchmark_emails_30d=200,
                       meetings_booked_30d=10, benchmark_meetings_30d=20,
                       proposals_30d=5, benchmark_proposals_30d=10,
                       connect_rate_pct=50.0, email_reply_rate_pct=40.0, meeting_show_rate_pct=50.0),
        ]
        results = engine.analyze_batch(inputs)
        scores = [r.activity_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_batch_appended_to_engine(self, engine):
        engine.analyze_batch([make_input(rep_id="A"), make_input(rep_id="B")])
        assert len(engine.all_reps()) == 2

    def test_single_item_batch(self, engine):
        results = engine.analyze_batch([make_input()])
        assert len(results) == 1


# ═══════════════════════════════════════════════════════════════════════════════
# 12. Filter methods
# ═══════════════════════════════════════════════════════════════════════════════

class TestFilterMethods:
    def test_by_tier_elite(self, engine):
        # score at benchmark gives ~95 => ELITE
        engine.analyze(make_input(rep_id="E1",
                                   connect_rate_pct=100.0, email_reply_rate_pct=100.0,
                                   meeting_show_rate_pct=100.0))
        elites = engine.by_tier(ActivityTier.ELITE)
        assert all(r.activity_tier == ActivityTier.ELITE for r in elites)

    def test_by_tier_empty(self, engine):
        engine.analyze(make_input())
        low_reps = engine.by_tier(ActivityTier.INACTIVE)
        # default make_input should not be inactive
        # just test it returns a list
        assert isinstance(low_reps, list)

    def test_by_tier_multiple_matches(self, engine):
        for i in range(3):
            engine.analyze(make_input(rep_id=f"E{i}",
                                       connect_rate_pct=100.0, email_reply_rate_pct=100.0,
                                       meeting_show_rate_pct=100.0))
        elites = engine.by_tier(ActivityTier.ELITE)
        assert len(elites) == 3

    def test_by_trend_stable(self, engine):
        engine.analyze(make_input())
        stable = engine.by_trend(ActivityTrend.STABLE)
        assert isinstance(stable, list)

    def test_by_trend_filters_correctly(self, engine):
        # Create STALLED rep
        stalled_inp = make_input(
            rep_id="STALLED",
            calls_7d=0, emails_7d=0, meetings_7d=0,
            benchmark_calls_30d=100, benchmark_emails_30d=200, benchmark_meetings_30d=20,
        )
        engine.analyze(stalled_inp)
        stalled = engine.by_trend(ActivityTrend.STALLED)
        assert any(r.rep_id == "STALLED" for r in stalled)

    def test_by_action_returns_list(self, engine):
        engine.analyze(make_input())
        result = engine.by_action(ActivityAction.CELEBRATE)
        assert isinstance(result, list)

    def test_by_action_coach(self, engine):
        # Score ~30 => LOW => COACH
        inp = make_input(
            calls_30d=20, benchmark_calls_30d=100,
            emails_30d=40, benchmark_emails_30d=200,
            meetings_booked_30d=4, benchmark_meetings_30d=20,
            proposals_30d=2, benchmark_proposals_30d=10,
            connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
        )
        engine.analyze(inp)
        coached = engine.by_action(ActivityAction.COACH)
        assert isinstance(coached, list)


# ═══════════════════════════════════════════════════════════════════════════════
# 13. Convenience filter methods
# ═══════════════════════════════════════════════════════════════════════════════

class TestConvenienceMethods:
    def test_elite_reps_returns_list(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.elite_reps(), list)

    def test_elite_reps_only_elite(self, engine):
        engine.analyze(make_input(
            connect_rate_pct=100.0, email_reply_rate_pct=100.0, meeting_show_rate_pct=100.0
        ))
        for r in engine.elite_reps():
            assert r.activity_tier == ActivityTier.ELITE

    def test_inactive_reps_returns_list(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.inactive_reps(), list)

    def test_inactive_reps_all_inactive(self, engine):
        inp = make_input(
            calls_30d=0, emails_30d=0, meetings_booked_30d=0, proposals_30d=0,
            connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
        )
        engine.analyze(inp)
        for r in engine.inactive_reps():
            assert r.activity_tier == ActivityTier.INACTIVE

    def test_needs_intervention_includes_coach_and_intervene(self, engine):
        # inactive => INTERVENE
        inp_inactive = make_input(
            rep_id="INACTIVE",
            calls_30d=0, emails_30d=0, meetings_booked_30d=0, proposals_30d=0,
            connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
        )
        engine.analyze(inp_inactive)
        needs = engine.needs_intervention()
        assert any(r.rep_id == "INACTIVE" for r in needs)
        for r in needs:
            assert r.activity_action in (ActivityAction.INTERVENE, ActivityAction.COACH)

    def test_declining_reps_returns_list(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.declining_reps(), list)

    def test_declining_reps_includes_declining_and_stalled(self, engine):
        stalled_inp = make_input(
            rep_id="STALLED",
            calls_7d=0, emails_7d=0, meetings_7d=0,
        )
        engine.analyze(stalled_inp)
        declining = engine.declining_reps()
        for r in declining:
            assert r.activity_trend in (ActivityTrend.DECLINING, ActivityTrend.STALLED)


# ═══════════════════════════════════════════════════════════════════════════════
# 14. Aggregates
# ═══════════════════════════════════════════════════════════════════════════════

class TestAggregates:
    def test_avg_activity_score_empty(self, engine):
        assert engine.avg_activity_score() == 0.0

    def test_avg_activity_score_single(self, engine):
        result = engine.analyze(make_input())
        avg = engine.avg_activity_score()
        assert avg == result.activity_score

    def test_avg_activity_score_multiple(self, engine):
        engine.analyze(make_input(
            rep_id="R1",
            calls_30d=0, emails_30d=0, meetings_booked_30d=0, proposals_30d=0,
            connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
        ))
        engine.analyze(make_input(
            rep_id="R2",
            connect_rate_pct=100.0, email_reply_rate_pct=100.0, meeting_show_rate_pct=100.0,
        ))
        avg = engine.avg_activity_score()
        assert isinstance(avg, (int, float))
        assert 0 <= avg <= 100

    def test_total_pipeline_empty(self, engine):
        assert engine.total_pipeline_generated_eur() == 0.0

    def test_total_pipeline_single(self, engine):
        engine.analyze(make_input(pipeline_generated_eur=50000.0))
        assert engine.total_pipeline_generated_eur() == 50000.0

    def test_total_pipeline_sums(self, engine):
        engine.analyze(make_input(rep_id="R1", pipeline_generated_eur=30000.0))
        engine.analyze(make_input(rep_id="R2", pipeline_generated_eur=70000.0))
        assert engine.total_pipeline_generated_eur() == 100000.0

    def test_avg_call_index_empty(self, engine):
        assert engine.avg_call_index() == 0.0

    def test_avg_call_index_single(self, engine):
        engine.analyze(make_input(calls_30d=100, benchmark_calls_30d=100))
        assert engine.avg_call_index() == 1.0

    def test_avg_call_index_multiple(self, engine):
        engine.analyze(make_input(rep_id="R1", calls_30d=50, benchmark_calls_30d=100))
        engine.analyze(make_input(rep_id="R2", calls_30d=150, benchmark_calls_30d=100))
        avg = engine.avg_call_index()
        assert isinstance(avg, (int, float))
        assert avg == 1.0  # (0.5 + 1.5) / 2

    def test_coaching_focus_distribution_empty(self, engine):
        dist = engine.coaching_focus_distribution()
        assert isinstance(dist, dict)
        assert dist == {}

    def test_coaching_focus_distribution_single(self, engine):
        engine.analyze(make_input(
            connect_rate_pct=20.0, email_reply_rate_pct=15.0, follow_ups_30d=10
        ))
        dist = engine.coaching_focus_distribution()
        assert isinstance(dist, dict)
        total = sum(dist.values())
        assert total == 1

    def test_coaching_focus_distribution_multiple(self, engine):
        for i in range(3):
            engine.analyze(make_input(
                rep_id=f"R{i}",
                connect_rate_pct=20.0, email_reply_rate_pct=15.0, follow_ups_30d=10,
            ))
        dist = engine.coaching_focus_distribution()
        total = sum(dist.values())
        assert total == 3

    def test_coaching_focus_distribution_keys_are_strings(self, engine):
        engine.analyze(make_input())
        dist = engine.coaching_focus_distribution()
        for k in dist.keys():
            assert isinstance(k, str)


# ═══════════════════════════════════════════════════════════════════════════════
# 15. summary() — all 10 keys, counts sum, empty state
# ═══════════════════════════════════════════════════════════════════════════════

class TestSummary:
    def test_summary_empty_state(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["avg_activity_score"] == 0.0
        assert s["total_pipeline_generated_eur"] == 0.0
        assert s["elite_count"] == 0
        assert s["inactive_count"] == 0
        assert s["intervention_count"] == 0
        assert s["declining_count"] == 0

    def test_summary_has_10_keys(self, engine):
        s = engine.summary()
        assert len(s) == 10

    def test_summary_all_expected_keys(self, engine):
        s = engine.summary()
        expected = {
            "total", "tier_counts", "trend_counts", "action_counts",
            "avg_activity_score", "total_pipeline_generated_eur",
            "elite_count", "inactive_count", "intervention_count", "declining_count",
        }
        assert set(s.keys()) == expected

    def test_summary_total_matches_reps(self, engine):
        engine.analyze(make_input(rep_id="A"))
        engine.analyze(make_input(rep_id="B"))
        assert engine.summary()["total"] == 2

    def test_summary_tier_counts_sum_to_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["tier_counts"].values()) == s["total"]

    def test_summary_trend_counts_sum_to_total(self, engine):
        for i in range(3):
            engine.analyze(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["trend_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self, engine):
        for i in range(5):
            engine.analyze(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_score_is_numeric(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert isinstance(s["avg_activity_score"], (int, float))

    def test_summary_pipeline_is_numeric(self, engine):
        engine.analyze(make_input(pipeline_generated_eur=12345.0))
        s = engine.summary()
        assert isinstance(s["total_pipeline_generated_eur"], (int, float))

    def test_summary_tier_counts_dict(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert isinstance(s["tier_counts"], dict)

    def test_summary_trend_counts_dict(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert isinstance(s["trend_counts"], dict)

    def test_summary_action_counts_dict(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert isinstance(s["action_counts"], dict)


# ═══════════════════════════════════════════════════════════════════════════════
# 16. reset() — clears results and resets aggregates
# ═══════════════════════════════════════════════════════════════════════════════

class TestReset:
    def test_reset_clears_all_reps(self, engine):
        engine.analyze(make_input(rep_id="A"))
        engine.analyze(make_input(rep_id="B"))
        engine.reset()
        assert engine.all_reps() == []

    def test_reset_resets_avg_score(self, engine):
        engine.analyze(make_input())
        engine.reset()
        assert engine.avg_activity_score() == 0.0

    def test_reset_resets_total_pipeline(self, engine):
        engine.analyze(make_input(pipeline_generated_eur=99999.0))
        engine.reset()
        assert engine.total_pipeline_generated_eur() == 0.0

    def test_reset_resets_avg_call_index(self, engine):
        engine.analyze(make_input())
        engine.reset()
        assert engine.avg_call_index() == 0.0

    def test_reset_resets_summary_total(self, engine):
        engine.analyze(make_input())
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_reset_allows_new_analysis(self, engine):
        engine.analyze(make_input(rep_id="OLD"))
        engine.reset()
        engine.analyze(make_input(rep_id="NEW"))
        reps = engine.all_reps()
        assert len(reps) == 1
        assert reps[0].rep_id == "NEW"

    def test_reset_resets_coaching_focus_distribution(self, engine):
        engine.analyze(make_input())
        engine.reset()
        assert engine.coaching_focus_distribution() == {}

    def test_double_reset_safe(self, engine):
        engine.reset()
        engine.reset()
        assert engine.all_reps() == []


# ═══════════════════════════════════════════════════════════════════════════════
# 17. Edge cases
# ═══════════════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    def test_zero_everything(self, engine):
        inp = make_input(
            calls_30d=0, emails_30d=0, meetings_booked_30d=0, proposals_30d=0,
            linkedin_touches_30d=0, follow_ups_30d=0,
            calls_7d=0, emails_7d=0, meetings_7d=0,
            benchmark_calls_30d=100, benchmark_emails_30d=200,
            benchmark_meetings_30d=20, benchmark_proposals_30d=10,
            connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
            deals_created_30d=0, pipeline_generated_eur=0.0, quota_attainment_pct=0.0,
        )
        result = engine.analyze(inp)
        assert result.activity_score == 0.0
        assert result.activity_tier == ActivityTier.INACTIVE
        assert result.activity_action == ActivityAction.INTERVENE

    def test_max_everything(self, engine):
        inp = make_input(
            calls_30d=10000, emails_30d=10000, meetings_booked_30d=10000, proposals_30d=10000,
            connect_rate_pct=100.0, email_reply_rate_pct=100.0, meeting_show_rate_pct=100.0,
        )
        result = engine.analyze(inp)
        assert result.activity_score == 100.0
        assert result.activity_tier == ActivityTier.ELITE

    def test_single_rep_analysis(self, engine):
        result = engine.analyze(make_input(rep_id="SOLO"))
        assert result.rep_id == "SOLO"
        assert len(engine.all_reps()) == 1

    def test_pipeline_zero(self, engine):
        result = engine.analyze(make_input(pipeline_generated_eur=0.0))
        assert result.pipeline_generated_eur == 0.0
        assert engine.total_pipeline_generated_eur() == 0.0

    def test_all_zero_benchmarks(self, engine):
        inp = make_input(
            benchmark_calls_30d=0, benchmark_emails_30d=0,
            benchmark_meetings_30d=0, benchmark_proposals_30d=0,
        )
        result = engine.analyze(inp)
        # all indices=1.0 => max volume pts + conversion pts
        assert result.call_index == 1.0
        assert result.email_index == 1.0
        assert result.meeting_index == 1.0
        assert result.proposal_index == 1.0

    def test_very_large_pipeline(self, engine):
        engine.analyze(make_input(rep_id="A", pipeline_generated_eur=1_000_000.0))
        engine.analyze(make_input(rep_id="B", pipeline_generated_eur=2_000_000.0))
        assert engine.total_pipeline_generated_eur() == 3_000_000.0

    def test_quota_attainment_does_not_affect_score(self, engine):
        # quota_attainment_pct is not used in _activity_score
        inp_low = make_input(quota_attainment_pct=0.0)
        inp_high = make_input(quota_attainment_pct=200.0)
        score_low = engine._activity_score(inp_low)
        score_high = engine._activity_score(inp_high)
        assert score_low == score_high

    def test_linkedin_touches_does_not_affect_score(self, engine):
        # linkedin_touches_30d is stored but not used in score formula
        inp_low = make_input(linkedin_touches_30d=0)
        inp_high = make_input(linkedin_touches_30d=10000)
        assert engine._activity_score(inp_low) == engine._activity_score(inp_high)


# ═══════════════════════════════════════════════════════════════════════════════
# 18. Integration — 4+ reps with different tiers, sort order correct
# ═══════════════════════════════════════════════════════════════════════════════

class TestIntegration:
    def _make_elite_input(self, rep_id="ELITE"):
        return make_input(
            rep_id=rep_id,
            connect_rate_pct=100.0,
            email_reply_rate_pct=100.0,
            meeting_show_rate_pct=100.0,
        )

    def _make_inactive_input(self, rep_id="INACTIVE"):
        return make_input(
            rep_id=rep_id,
            calls_30d=0, emails_30d=0, meetings_booked_30d=0, proposals_30d=0,
            connect_rate_pct=0.0, email_reply_rate_pct=0.0, meeting_show_rate_pct=0.0,
        )

    def test_four_reps_batch_sorted(self, engine):
        inputs = [
            self._make_inactive_input("LAST"),
            self._make_elite_input("FIRST"),
            make_input(rep_id="MID2", calls_30d=50, benchmark_calls_30d=100,
                       emails_30d=100, benchmark_emails_30d=200,
                       meetings_booked_30d=10, benchmark_meetings_30d=20,
                       proposals_30d=5, benchmark_proposals_30d=10,
                       connect_rate_pct=30.0, email_reply_rate_pct=20.0,
                       meeting_show_rate_pct=50.0),
            make_input(rep_id="MID1", calls_30d=80, benchmark_calls_30d=100,
                       emails_30d=160, benchmark_emails_30d=200,
                       meetings_booked_30d=16, benchmark_meetings_30d=20,
                       proposals_30d=8, benchmark_proposals_30d=10,
                       connect_rate_pct=15.0, email_reply_rate_pct=12.0,
                       meeting_show_rate_pct=70.0),
        ]
        results = engine.analyze_batch(inputs)
        scores = [r.activity_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_all_tiers_present_in_summary(self, engine):
        engine.analyze(self._make_elite_input())
        engine.analyze(self._make_inactive_input())
        s = engine.summary()
        assert s["elite_count"] >= 1
        assert s["inactive_count"] >= 1
        assert s["total"] == 2

    def test_intervention_count_correct(self, engine):
        engine.analyze(self._make_inactive_input("I1"))
        engine.analyze(self._make_inactive_input("I2"))
        engine.analyze(self._make_elite_input("E1"))
        s = engine.summary()
        # Both inactive get INTERVENE => intervention_count >= 2
        assert s["intervention_count"] >= 2

    def test_declining_count_correct(self, engine):
        stalled_inp = make_input(
            rep_id="STALLED",
            calls_7d=0, emails_7d=0, meetings_7d=0,
            benchmark_calls_30d=100, benchmark_emails_30d=200, benchmark_meetings_30d=20,
        )
        engine.analyze(stalled_inp)
        engine.analyze(self._make_elite_input())
        s = engine.summary()
        assert s["declining_count"] >= 1

    def test_reset_between_batches(self, engine):
        engine.analyze_batch([make_input(rep_id="A"), make_input(rep_id="B")])
        assert len(engine.all_reps()) == 2
        engine.reset()
        engine.analyze_batch([make_input(rep_id="X")])
        assert len(engine.all_reps()) == 1

    def test_full_pipeline_after_batch(self, engine):
        inputs = [
            make_input(rep_id=f"R{i}", pipeline_generated_eur=10000.0 * (i + 1))
            for i in range(4)
        ]
        engine.analyze_batch(inputs)
        # 10000 + 20000 + 30000 + 40000 = 100000
        assert engine.total_pipeline_generated_eur() == 100000.0

    def test_by_tier_after_batch(self, engine):
        inputs = [
            self._make_elite_input("E1"),
            self._make_elite_input("E2"),
            self._make_inactive_input("I1"),
        ]
        engine.analyze_batch(inputs)
        elites = engine.by_tier(ActivityTier.ELITE)
        inactives = engine.by_tier(ActivityTier.INACTIVE)
        assert len(elites) == 2
        assert len(inactives) == 1

    def test_all_reps_returns_insertion_order(self, engine):
        ids = ["Z", "A", "M", "B"]
        for rid in ids:
            engine.analyze(make_input(rep_id=rid))
        returned_ids = [r.rep_id for r in engine.all_reps()]
        assert returned_ids == ids

    def test_needs_intervention_empty_when_all_elite(self, engine):
        engine.analyze(self._make_elite_input("E1"))
        engine.analyze(self._make_elite_input("E2"))
        needs = engine.needs_intervention()
        assert needs == []

    def test_coaching_focus_distribution_counts(self, engine):
        # 3 ON_TRACK reps
        for i in range(3):
            engine.analyze(make_input(
                rep_id=f"OT{i}",
                connect_rate_pct=20.0, email_reply_rate_pct=15.0, follow_ups_30d=10,
            ))
        dist = engine.coaching_focus_distribution()
        assert sum(dist.values()) == 3
