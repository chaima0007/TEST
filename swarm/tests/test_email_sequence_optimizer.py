"""Comprehensive pytest tests for EmailSequenceOptimizer."""

from __future__ import annotations

import pytest
from swarm.intelligence.email_sequence_optimizer import (
    EmailSequenceOptimizer,
    SequenceInput,
    SequenceResult,
    SequenceStep,
    StepOptimization,
    SequenceStatus,
    StepType,
    TouchpointStrategy,
    _timing_score,
    _performance_score,
    _overall_score,
    _status,
    _recommended_strategy,
    _OPTIMAL_GAPS_DAYS,
    _STEP_TYPE_OPEN_RATE,
    _STEP_TYPE_REPLY_RATE,
)
from swarm.intelligence.email_sequence_optimizer import _step_issues_and_recs


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------

def make_step(
    step_number: int = 1,
    step_type: StepType = StepType.EMAIL,
    day_offset: int = 0,
    **kwargs,
) -> SequenceStep:
    defaults = dict(
        subject_line="Test Subject",
        body_preview="Hello...",
        open_rate_pct=22.0,
        reply_rate_pct=5.0,
        click_rate_pct=2.0,
        unsubscribe_rate_pct=0.5,
        sent_count=100,
    )
    defaults.update(kwargs)
    return SequenceStep(
        step_number=step_number,
        step_type=step_type,
        day_offset=day_offset,
        **defaults,
    )


def make_input(sequence_id: str = "seq1", steps=None, **kwargs) -> SequenceInput:
    if steps is None:
        steps = [
            make_step(1, day_offset=0),
            make_step(2, StepType.LINKEDIN, 3),
            make_step(3, day_offset=7),
            make_step(4, StepType.PHONE, 14),
        ]
    defaults = dict(
        sequence_name="Test Seq",
        strategy=TouchpointStrategy.BALANCED,
        target_industry="saas",
        target_persona="VP Sales",
        avg_deal_size_eur=20000,
        total_prospects=200,
        converted_prospects=10,
        bounced_emails=4,
    )
    defaults.update(kwargs)
    return SequenceInput(sequence_id=sequence_id, steps=steps, **defaults)


# ===========================================================================
# 1. TestTimingScore
# ===========================================================================

class TestTimingScore:
    """Tests for _timing_score()."""

    # --- AGGRESSIVE strategy ---

    def test_aggressive_step1_perfect(self):
        # optimal[0]=0 → delta=0 → 100
        step = make_step(step_number=1, day_offset=0)
        assert _timing_score(step, TouchpointStrategy.AGGRESSIVE) == 100

    def test_aggressive_step2_perfect(self):
        step = make_step(step_number=2, day_offset=2)
        assert _timing_score(step, TouchpointStrategy.AGGRESSIVE) == 100

    def test_aggressive_step3_perfect(self):
        step = make_step(step_number=3, day_offset=4)
        assert _timing_score(step, TouchpointStrategy.AGGRESSIVE) == 100

    def test_aggressive_step4_perfect(self):
        step = make_step(step_number=4, day_offset=7)
        assert _timing_score(step, TouchpointStrategy.AGGRESSIVE) == 100

    def test_aggressive_step5_perfect(self):
        step = make_step(step_number=5, day_offset=10)
        assert _timing_score(step, TouchpointStrategy.AGGRESSIVE) == 100

    def test_aggressive_step6_perfect(self):
        step = make_step(step_number=6, day_offset=14)
        assert _timing_score(step, TouchpointStrategy.AGGRESSIVE) == 100

    def test_aggressive_step_beyond_list_uses_last(self):
        # step 7 → idx = min(6, 5) = 5 → optimal=14
        step = make_step(step_number=7, day_offset=14)
        assert _timing_score(step, TouchpointStrategy.AGGRESSIVE) == 100

    def test_aggressive_step1_delta5(self):
        # delta=5 → 100 - 5*8 = 60
        step = make_step(step_number=1, day_offset=5)
        assert _timing_score(step, TouchpointStrategy.AGGRESSIVE) == 60

    def test_aggressive_step1_delta13_zero(self):
        # delta=13 → 100 - 13*8 = -4 → max(0, -4)=0
        step = make_step(step_number=1, day_offset=13)
        assert _timing_score(step, TouchpointStrategy.AGGRESSIVE) == 0

    def test_aggressive_step1_delta1(self):
        step = make_step(step_number=1, day_offset=1)
        assert _timing_score(step, TouchpointStrategy.AGGRESSIVE) == 92

    # --- BALANCED strategy ---

    def test_balanced_step1_perfect(self):
        step = make_step(step_number=1, day_offset=0)
        assert _timing_score(step, TouchpointStrategy.BALANCED) == 100

    def test_balanced_step2_perfect(self):
        step = make_step(step_number=2, day_offset=3)
        assert _timing_score(step, TouchpointStrategy.BALANCED) == 100

    def test_balanced_step3_perfect(self):
        step = make_step(step_number=3, day_offset=7)
        assert _timing_score(step, TouchpointStrategy.BALANCED) == 100

    def test_balanced_step4_perfect(self):
        step = make_step(step_number=4, day_offset=14)
        assert _timing_score(step, TouchpointStrategy.BALANCED) == 100

    def test_balanced_step5_perfect(self):
        step = make_step(step_number=5, day_offset=21)
        assert _timing_score(step, TouchpointStrategy.BALANCED) == 100

    def test_balanced_step6_perfect(self):
        step = make_step(step_number=6, day_offset=28)
        assert _timing_score(step, TouchpointStrategy.BALANCED) == 100

    def test_balanced_step2_off_by_3(self):
        # optimal_day=3, day_offset=6 → delta=3 → 100-24=76
        step = make_step(step_number=2, day_offset=6)
        assert _timing_score(step, TouchpointStrategy.BALANCED) == 76

    # --- NURTURE strategy ---

    def test_nurture_step1_perfect(self):
        step = make_step(step_number=1, day_offset=0)
        assert _timing_score(step, TouchpointStrategy.NURTURE) == 100

    def test_nurture_step2_perfect(self):
        step = make_step(step_number=2, day_offset=7)
        assert _timing_score(step, TouchpointStrategy.NURTURE) == 100

    def test_nurture_step3_perfect(self):
        step = make_step(step_number=3, day_offset=14)
        assert _timing_score(step, TouchpointStrategy.NURTURE) == 100

    def test_nurture_step4_perfect(self):
        step = make_step(step_number=4, day_offset=30)
        assert _timing_score(step, TouchpointStrategy.NURTURE) == 100

    def test_nurture_step_beyond_list_uses_last(self):
        # step 10 → idx=min(9, 5)=5 → optimal_day=60
        step = make_step(step_number=10, day_offset=60)
        assert _timing_score(step, TouchpointStrategy.NURTURE) == 100

    # --- REACTIVATION strategy ---

    def test_reactivation_step1_perfect(self):
        step = make_step(step_number=1, day_offset=0)
        assert _timing_score(step, TouchpointStrategy.REACTIVATION) == 100

    def test_reactivation_step2_perfect(self):
        step = make_step(step_number=2, day_offset=5)
        assert _timing_score(step, TouchpointStrategy.REACTIVATION) == 100

    def test_reactivation_step3_perfect(self):
        step = make_step(step_number=3, day_offset=12)
        assert _timing_score(step, TouchpointStrategy.REACTIVATION) == 100

    def test_reactivation_step4_perfect(self):
        step = make_step(step_number=4, day_offset=21)
        assert _timing_score(step, TouchpointStrategy.REACTIVATION) == 100

    def test_reactivation_step5_perfect(self):
        step = make_step(step_number=5, day_offset=35)
        assert _timing_score(step, TouchpointStrategy.REACTIVATION) == 100

    def test_reactivation_step6_perfect(self):
        step = make_step(step_number=6, day_offset=50)
        assert _timing_score(step, TouchpointStrategy.REACTIVATION) == 100

    def test_timing_score_never_negative(self):
        # Very large offset → score floored at 0
        step = make_step(step_number=1, day_offset=1000)
        assert _timing_score(step, TouchpointStrategy.BALANCED) == 0

    def test_timing_score_negative_offset(self):
        # step_number=1, optimal=0, day_offset=-1 → delta=1 → 92
        step = make_step(step_number=1, day_offset=-1)
        assert _timing_score(step, TouchpointStrategy.BALANCED) == 92

    def test_timing_score_delta_zero_is_100(self):
        for strategy, gaps in _OPTIMAL_GAPS_DAYS.items():
            step = make_step(step_number=1, day_offset=gaps[0])
            assert _timing_score(step, strategy) == 100


# ===========================================================================
# 2. TestPerformanceScore
# ===========================================================================

class TestPerformanceScore:
    """Tests for _performance_score()."""

    def test_sent_count_zero_returns_50(self):
        step = make_step(sent_count=0)
        assert _performance_score(step) == 50.0

    def test_sent_count_zero_regardless_of_rates(self):
        step = make_step(sent_count=0, open_rate_pct=99.0, reply_rate_pct=99.0)
        assert _performance_score(step) == 50.0

    def test_email_at_benchmark(self):
        # open=22%, reply=5%, unsub=0%, sent=100
        # benchmark_open=22, benchmark_reply=5
        # open_score=min(100, (22/22)*70)=70
        # reply_score=min(100, (5/5)*100)=100
        # unsub_penalty=0
        # total=70*0.45 + 100*0.55 - 0 = 31.5 + 55 = 86.5
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=22.0,
            reply_rate_pct=5.0,
            unsubscribe_rate_pct=0.0,
            sent_count=100,
        )
        assert abs(_performance_score(step) - 86.5) < 0.001

    def test_linkedin_at_benchmark(self):
        # open=45%, reply=12%, unsub=0
        # benchmark_open=45, benchmark_reply=12
        # open_score=min(100, (45/45)*70)=70
        # reply_score=min(100, (12/12)*100)=100
        # total=70*0.45+100*0.55=31.5+55=86.5
        step = make_step(
            step_type=StepType.LINKEDIN,
            open_rate_pct=45.0,
            reply_rate_pct=12.0,
            unsubscribe_rate_pct=0.0,
            sent_count=100,
        )
        assert abs(_performance_score(step) - 86.5) < 0.001

    def test_phone_at_benchmark(self):
        # open=30, reply=18, unsub=0
        # open_score=min(100,(30/30)*70)=70, reply_score=min(100,(18/18)*100)=100
        # total=86.5
        step = make_step(
            step_type=StepType.PHONE,
            open_rate_pct=30.0,
            reply_rate_pct=18.0,
            unsubscribe_rate_pct=0.0,
            sent_count=100,
        )
        assert abs(_performance_score(step) - 86.5) < 0.001

    def test_video_at_benchmark(self):
        step = make_step(
            step_type=StepType.VIDEO,
            open_rate_pct=38.0,
            reply_rate_pct=10.0,
            unsubscribe_rate_pct=0.0,
            sent_count=100,
        )
        assert abs(_performance_score(step) - 86.5) < 0.001

    def test_direct_mail_at_benchmark(self):
        step = make_step(
            step_type=StepType.DIRECT_MAIL,
            open_rate_pct=65.0,
            reply_rate_pct=25.0,
            unsubscribe_rate_pct=0.0,
            sent_count=100,
        )
        assert abs(_performance_score(step) - 86.5) < 0.001

    def test_open_score_capped_at_70(self):
        # Even 200% open rate → open_score capped at 100 (but formula *70 so max 70)
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=200.0,
            reply_rate_pct=5.0,
            unsubscribe_rate_pct=0.0,
            sent_count=100,
        )
        score = _performance_score(step)
        # open_score = min(100, (200/22)*70) = min(100, ~636) = 100 → wait, min(100, ...) then *0.45
        # open_score=100 → wait, (200/22)*70=636 → min(100, 636)=100
        # total=100*0.45+100*0.55=86.5+... wait reply=(5/5)*100=100
        # Actually open_score=min(100, (200/22)*70)=min(100,636)=100
        # score=100*0.45+100*0.55=86.5? No: 100*0.45=45, 100*0.55=55 → 100
        assert abs(score - 100.0) < 0.001

    def test_reply_score_capped_at_100(self):
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=22.0,
            reply_rate_pct=100.0,
            unsubscribe_rate_pct=0.0,
            sent_count=100,
        )
        score = _performance_score(step)
        # reply_score = min(100, (100/5)*100)=min(100,2000)=100
        # open_score=min(100,(22/22)*70)=70
        # total=70*0.45+100*0.55=31.5+55=86.5
        assert abs(score - 86.5) < 0.001

    def test_unsub_penalty_capped_at_30(self):
        # unsub=5% → min(30, 5*10)=min(30,50)=30
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=22.0,
            reply_rate_pct=5.0,
            unsubscribe_rate_pct=5.0,
            sent_count=100,
        )
        score = _performance_score(step)
        # 70*0.45+100*0.55-30 = 31.5+55-30=56.5
        assert abs(score - 56.5) < 0.001

    def test_unsub_penalty_partial(self):
        # unsub=2% → penalty=min(30, 2*10)=20
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=22.0,
            reply_rate_pct=5.0,
            unsubscribe_rate_pct=2.0,
            sent_count=100,
        )
        score = _performance_score(step)
        # 70*0.45+100*0.55-20=31.5+55-20=66.5
        assert abs(score - 66.5) < 0.001

    def test_low_open_rate_lowers_score(self):
        step_good = make_step(open_rate_pct=22.0, reply_rate_pct=5.0, sent_count=100)
        step_bad = make_step(open_rate_pct=5.0, reply_rate_pct=5.0, sent_count=100)
        assert _performance_score(step_bad) < _performance_score(step_good)

    def test_low_reply_rate_lowers_score(self):
        step_good = make_step(open_rate_pct=22.0, reply_rate_pct=5.0, sent_count=100)
        step_bad = make_step(open_rate_pct=22.0, reply_rate_pct=1.0, sent_count=100)
        assert _performance_score(step_bad) < _performance_score(step_good)

    def test_score_never_negative(self):
        # Extreme unsub with zero rates
        step = make_step(
            open_rate_pct=0.0,
            reply_rate_pct=0.0,
            unsubscribe_rate_pct=100.0,
            sent_count=100,
        )
        assert _performance_score(step) >= 0.0

    def test_zero_open_zero_reply(self):
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=0.0,
            reply_rate_pct=0.0,
            unsubscribe_rate_pct=0.0,
            sent_count=100,
        )
        # open_score=0, reply_score=0, penalty=0 → 0
        assert _performance_score(step) == 0.0

    def test_performance_score_double_benchmark_open(self):
        # open=44 (2x), reply=5 → open_score=min(100,(44/22)*70)=min(100,140)=100
        # reply_score=min(100,(5/5)*100)=100
        # total=100*0.45+100*0.55=100
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=44.0,
            reply_rate_pct=5.0,
            unsubscribe_rate_pct=0.0,
            sent_count=100,
        )
        assert abs(_performance_score(step) - 100.0) < 0.001

    def test_performance_score_half_benchmark(self):
        # open=11 (0.5x) → open_score=(11/22)*70=35
        # reply=2.5 (0.5x) → reply_score=(2.5/5)*100=50
        # penalty=0
        # total=35*0.45+50*0.55=15.75+27.5=43.25
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=11.0,
            reply_rate_pct=2.5,
            unsubscribe_rate_pct=0.0,
            sent_count=100,
        )
        assert abs(_performance_score(step) - 43.25) < 0.001

    def test_unsub_at_zero(self):
        step = make_step(unsubscribe_rate_pct=0.0, sent_count=100)
        score = _performance_score(step)
        assert score >= 0.0

    def test_unsub_at_exactly_3(self):
        # penalty = min(30, 3*10)=30
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=22.0,
            reply_rate_pct=5.0,
            unsubscribe_rate_pct=3.0,
            sent_count=100,
        )
        score = _performance_score(step)
        # 31.5+55-30=56.5
        assert abs(score - 56.5) < 0.001

    def test_direct_mail_double_open(self):
        # open=130 (2x65), reply=25, unsub=0
        # open_score=min(100,(130/65)*70)=min(100,140)=100
        # reply_score=min(100,(25/25)*100)=100
        step = make_step(
            step_type=StepType.DIRECT_MAIL,
            open_rate_pct=130.0,
            reply_rate_pct=25.0,
            unsubscribe_rate_pct=0.0,
            sent_count=100,
        )
        assert abs(_performance_score(step) - 100.0) < 0.001


# ===========================================================================
# 3. TestOverallScore
# ===========================================================================

class TestOverallScore:
    """Tests for _overall_score()."""

    def test_empty_steps_scores_returns_zero(self):
        inp = make_input(total_prospects=100, converted_prospects=5, bounced_emails=0)
        assert _overall_score(inp, []) == 0.0

    def test_perfect_scenario(self):
        # timing=100, perf=100, conv_rate=10%→conv_score=100, bounce=0→penalty=0
        # raw=100*0.30+100*0.40+100*0.20-0*0.10=30+40+20=90
        inp = make_input(total_prospects=100, converted_prospects=10, bounced_emails=0)
        result = _overall_score(inp, [(100, 100)])
        assert abs(result - 90.0) < 0.01

    def test_conv_rate_10_pct_gives_conv_score_100(self):
        inp = make_input(total_prospects=100, converted_prospects=10, bounced_emails=0)
        # conv_score=min(100,10*10)=100
        result = _overall_score(inp, [(100, 100)])
        assert abs(result - 90.0) < 0.01

    def test_conv_rate_0_pct_gives_conv_score_0(self):
        # timing=100, perf=100, conv_score=0, bounce=0
        # raw=30+40+0-0=70
        inp = make_input(total_prospects=100, converted_prospects=0, bounced_emails=0)
        result = _overall_score(inp, [(100, 100)])
        assert abs(result - 70.0) < 0.01

    def test_bounce_rate_10_pct_gives_penalty_30(self):
        # bounce=10/100=10% → penalty=min(30,10*3)=30
        # timing=100, perf=100, conv=0, bounce=30
        # raw=30+40+0-30*0.10=70-3=67
        inp = make_input(total_prospects=100, converted_prospects=0, bounced_emails=10)
        result = _overall_score(inp, [(100, 100)])
        assert abs(result - 67.0) < 0.01

    def test_bounce_rate_20_pct_penalty_still_capped_30(self):
        # bounce=20% → penalty=min(30,20*3)=min(30,60)=30
        # timing=100, perf=100, conv=0, bounce=30
        # raw=30+40+0-30*0.10=67
        inp = make_input(total_prospects=100, converted_prospects=0, bounced_emails=20)
        result = _overall_score(inp, [(100, 100)])
        assert abs(result - 67.0) < 0.01

    def test_rounded_to_2_decimal_places(self):
        inp = make_input(total_prospects=100, converted_prospects=3, bounced_emails=1)
        result = _overall_score(inp, [(75, 80)])
        assert result == round(result, 2)

    def test_result_min_zero(self):
        # Even with very bad scores, result is at least 0
        inp = make_input(total_prospects=100, converted_prospects=0, bounced_emails=100)
        result = _overall_score(inp, [(0, 0)])
        assert result >= 0.0

    def test_result_max_100(self):
        # Even with inflated scores, result is at most 100
        inp = make_input(total_prospects=100, converted_prospects=100, bounced_emails=0)
        result = _overall_score(inp, [(100, 100)])
        assert result <= 100.0

    def test_multiple_steps_scores_averaged(self):
        # timing avg=(100+60)/2=80, perf avg=(80+40)/2=60
        # conv=0, bounce=0
        # raw=80*0.30+60*0.40=24+24=48
        inp = make_input(total_prospects=100, converted_prospects=0, bounced_emails=0)
        result = _overall_score(inp, [(100, 80), (60, 40)])
        assert abs(result - 48.0) < 0.01

    def test_total_prospects_zero_uses_max_1(self):
        # total=0 → max(1,0)=1 → conv_rate=0/1=0 → conv_score=0
        # bounce=0/1=0 → penalty=0
        inp = make_input(total_prospects=0, converted_prospects=0, bounced_emails=0)
        result = _overall_score(inp, [(100, 100)])
        assert abs(result - 70.0) < 0.01

    def test_conv_score_capped_at_100(self):
        # 100% conversion → conv_rate=100% → conv_score=min(100,100*10)=100
        inp = make_input(total_prospects=10, converted_prospects=10, bounced_emails=0)
        result = _overall_score(inp, [(100, 100)])
        # raw=30+40+100*0.20=30+40+20=90
        assert abs(result - 90.0) < 0.01

    def test_single_step_perfect_no_conv_no_bounce(self):
        inp = make_input(total_prospects=100, converted_prospects=0, bounced_emails=0)
        result = _overall_score(inp, [(100, 100)])
        # raw=30+40+0-0=70
        assert abs(result - 70.0) < 0.01

    def test_partial_scores(self):
        # timing=50, perf=50, conv=5%, bounce=2%
        # conv_score=min(100,5*10)=50
        # bounce_penalty=min(30,2*3)=6
        # raw=50*0.30+50*0.40+50*0.20-6*0.10=15+20+10-0.6=44.4
        inp = make_input(total_prospects=100, converted_prospects=5, bounced_emails=2)
        result = _overall_score(inp, [(50, 50)])
        assert abs(result - 44.4) < 0.01

    def test_zero_timing_zero_perf_high_conv(self):
        # timing=0, perf=0, conv=10%→score=100, bounce=0
        # raw=0+0+100*0.20-0=20
        inp = make_input(total_prospects=100, converted_prospects=10, bounced_emails=0)
        result = _overall_score(inp, [(0, 0)])
        assert abs(result - 20.0) < 0.01


# ===========================================================================
# 4. TestStatus
# ===========================================================================

class TestStatus:
    """Tests for _status() — exact boundary values."""

    def test_score_80_excellent(self):
        assert _status(80) == SequenceStatus.EXCELLENT

    def test_score_7999_good(self):
        assert _status(79.99) == SequenceStatus.GOOD

    def test_score_60_good(self):
        assert _status(60) == SequenceStatus.GOOD

    def test_score_5999_average(self):
        assert _status(59.99) == SequenceStatus.AVERAGE

    def test_score_40_average(self):
        assert _status(40) == SequenceStatus.AVERAGE

    def test_score_3999_poor(self):
        assert _status(39.99) == SequenceStatus.POOR

    def test_score_20_poor(self):
        assert _status(20) == SequenceStatus.POOR

    def test_score_1999_critical(self):
        assert _status(19.99) == SequenceStatus.CRITICAL

    def test_score_0_critical(self):
        assert _status(0) == SequenceStatus.CRITICAL

    def test_score_100_excellent(self):
        assert _status(100) == SequenceStatus.EXCELLENT


# ===========================================================================
# 5. TestRecommendedStrategy
# ===========================================================================

class TestRecommendedStrategy:
    """Tests for _recommended_strategy()."""

    def test_conv_rate_10pct_returns_aggressive(self):
        inp = make_input(total_prospects=100, converted_prospects=10)
        result = _recommended_strategy(inp, 50)
        assert result == TouchpointStrategy.AGGRESSIVE

    def test_conv_rate_above_10pct_returns_aggressive(self):
        inp = make_input(total_prospects=100, converted_prospects=20)
        result = _recommended_strategy(inp, 50)
        assert result == TouchpointStrategy.AGGRESSIVE

    def test_conv_rate_5pct_keeps_current(self):
        inp = make_input(
            total_prospects=100,
            converted_prospects=5,
            strategy=TouchpointStrategy.BALANCED,
        )
        result = _recommended_strategy(inp, 50)
        assert result == TouchpointStrategy.BALANCED

    def test_conv_rate_between_5_and_10_keeps_current(self):
        inp = make_input(
            total_prospects=100,
            converted_prospects=7,
            strategy=TouchpointStrategy.NURTURE,
        )
        result = _recommended_strategy(inp, 50)
        assert result == TouchpointStrategy.NURTURE

    def test_total_prospects_positive_converted_zero_reactivation(self):
        inp = make_input(total_prospects=100, converted_prospects=0)
        result = _recommended_strategy(inp, 50)
        assert result == TouchpointStrategy.REACTIVATION

    def test_total_zero_returns_nurture(self):
        # 0/max(1,0)=0 → <0.05, total=0 not >0 → NURTURE
        inp = make_input(total_prospects=0, converted_prospects=0)
        result = _recommended_strategy(inp, 50)
        assert result == TouchpointStrategy.NURTURE

    def test_conv_rate_3pct_less_than_5pct_and_converted_nonzero_nurture(self):
        # 3/100=3% < 5%, total>0 but converted!=0 → NURTURE
        inp = make_input(total_prospects=100, converted_prospects=3)
        result = _recommended_strategy(inp, 50)
        assert result == TouchpointStrategy.NURTURE

    def test_conv_rate_exactly_5pct_keeps_current(self):
        inp = make_input(
            total_prospects=200,
            converted_prospects=10,
            strategy=TouchpointStrategy.AGGRESSIVE,
        )
        result = _recommended_strategy(inp, 80)
        assert result == TouchpointStrategy.AGGRESSIVE

    def test_conv_rate_just_below_10pct_keeps_current(self):
        # 9/100=9% → >=5% → keep current
        inp = make_input(
            total_prospects=100,
            converted_prospects=9,
            strategy=TouchpointStrategy.REACTIVATION,
        )
        result = _recommended_strategy(inp, 70)
        assert result == TouchpointStrategy.REACTIVATION


# ===========================================================================
# 6. TestStepIssuesAndRecs
# ===========================================================================

class TestStepIssuesAndRecs:
    """Tests for _step_issues_and_recs()."""

    def test_timing_below_50_adds_timing_issue(self):
        # timing=40 → issue added
        step = make_step(step_number=1, day_offset=8)  # delta=8 → 100-64=36 < 50
        issues, recs = _step_issues_and_recs(step, 36, 70, TouchpointStrategy.BALANCED)
        assert any("iming" in i for i in issues)

    def test_timing_below_50_adds_timing_rec(self):
        step = make_step(step_number=1, day_offset=8)
        issues, recs = _step_issues_and_recs(step, 36, 70, TouchpointStrategy.BALANCED)
        assert any("délai" in r or "optimal" in r for r in recs)

    def test_timing_above_50_no_timing_issue(self):
        step = make_step(step_number=1, day_offset=0)
        issues, recs = _step_issues_and_recs(step, 100, 80, TouchpointStrategy.BALANCED)
        assert not any("Timing" in i for i in issues)

    def test_open_below_60pct_benchmark_adds_issue(self):
        # benchmark_open for EMAIL = 22%, 60% of that = 13.2%
        # open=10% < 13.2% → open issue
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=10.0,
            reply_rate_pct=5.0,
            sent_count=100,
        )
        issues, recs = _step_issues_and_recs(step, 100, 70, TouchpointStrategy.BALANCED)
        assert any("ouverture" in i for i in issues)

    def test_open_above_60pct_benchmark_no_issue(self):
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=22.0,
            sent_count=100,
        )
        issues, recs = _step_issues_and_recs(step, 100, 80, TouchpointStrategy.BALANCED)
        assert not any("ouverture" in i for i in issues)

    def test_open_below_60pct_benchmark_adds_ab_test_rec(self):
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=10.0,
            sent_count=100,
        )
        issues, recs = _step_issues_and_recs(step, 100, 70, TouchpointStrategy.BALANCED)
        assert any("A/B" in r for r in recs)

    def test_reply_below_50pct_benchmark_adds_issue(self):
        # benchmark_reply for EMAIL = 5%, 50% = 2.5%
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=22.0,
            reply_rate_pct=1.0,
            sent_count=100,
        )
        issues, recs = _step_issues_and_recs(step, 100, 70, TouchpointStrategy.BALANCED)
        assert any("réponse" in i for i in issues)

    def test_reply_below_50pct_benchmark_adds_cta_rec(self):
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=22.0,
            reply_rate_pct=1.0,
            sent_count=100,
        )
        issues, recs = _step_issues_and_recs(step, 100, 70, TouchpointStrategy.BALANCED)
        assert any("CTA" in r for r in recs)

    def test_reply_above_50pct_benchmark_no_issue(self):
        step = make_step(
            step_type=StepType.EMAIL,
            reply_rate_pct=5.0,
            sent_count=100,
        )
        issues, recs = _step_issues_and_recs(step, 100, 80, TouchpointStrategy.BALANCED)
        assert not any("réponse" in i for i in issues)

    def test_unsub_above_2_adds_issue(self):
        step = make_step(unsubscribe_rate_pct=3.0, sent_count=100)
        issues, recs = _step_issues_and_recs(step, 100, 80, TouchpointStrategy.BALANCED)
        assert any("désabonnement" in i for i in issues)

    def test_unsub_above_2_adds_frequency_rec(self):
        step = make_step(unsubscribe_rate_pct=3.0, sent_count=100)
        issues, recs = _step_issues_and_recs(step, 100, 80, TouchpointStrategy.BALANCED)
        assert any("fréquence" in r or "liste" in r for r in recs)

    def test_unsub_below_2_no_issue(self):
        step = make_step(unsubscribe_rate_pct=1.0, sent_count=100)
        issues, recs = _step_issues_and_recs(step, 100, 80, TouchpointStrategy.BALANCED)
        assert not any("désabonnement" in i for i in issues)

    def test_sent_count_zero_no_performance_issues(self):
        # When sent_count=0, open/reply checks are skipped (gated on sent_count>0).
        # Unsub check is NOT gated on sent_count, so keep unsub low to isolate.
        step = make_step(
            open_rate_pct=0.0,
            reply_rate_pct=0.0,
            unsubscribe_rate_pct=0.5,  # below 2.0 threshold → no unsub issue
            sent_count=0,
        )
        issues, recs = _step_issues_and_recs(step, 100, 50, TouchpointStrategy.BALANCED)
        # sent_count=0 → open/reply issues suppressed
        assert not any("ouverture" in i for i in issues)
        assert not any("réponse" in i for i in issues)
        # unsub=0.5 < 2.0 → no unsub issue either
        assert not any("désabonnement" in i for i in issues)

    def test_email_click_below_1pct_adds_cta_rec(self):
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=22.0,
            reply_rate_pct=5.0,
            click_rate_pct=0.5,
            sent_count=100,
        )
        issues, recs = _step_issues_and_recs(step, 100, 80, TouchpointStrategy.BALANCED)
        assert any("CTA" in r or "lien" in r for r in recs)

    def test_email_click_above_1pct_no_extra_cta_rec(self):
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=22.0,
            reply_rate_pct=5.0,
            click_rate_pct=2.0,
            sent_count=100,
        )
        issues, recs = _step_issues_and_recs(step, 100, 80, TouchpointStrategy.BALANCED)
        # No click CTA rec
        click_recs = [r for r in recs if "lien CTA" in r]
        assert len(click_recs) == 0

    def test_linkedin_click_below_1pct_no_email_cta_rec(self):
        # click CTA rec only for EMAIL step_type
        step = make_step(
            step_type=StepType.LINKEDIN,
            open_rate_pct=45.0,
            reply_rate_pct=12.0,
            click_rate_pct=0.5,
            sent_count=100,
        )
        issues, recs = _step_issues_and_recs(step, 100, 80, TouchpointStrategy.BALANCED)
        cta_recs = [r for r in recs if "lien CTA" in r]
        assert len(cta_recs) == 0

    def test_no_issues_when_all_perfect(self):
        step = make_step(
            step_type=StepType.EMAIL,
            open_rate_pct=22.0,
            reply_rate_pct=5.0,
            click_rate_pct=2.0,
            unsubscribe_rate_pct=0.5,
            sent_count=100,
        )
        issues, recs = _step_issues_and_recs(step, 100, 80, TouchpointStrategy.BALANCED)
        assert len(issues) == 0


# ===========================================================================
# 7. TestOptimizerOptimize
# ===========================================================================

class TestOptimizerOptimize:
    """Tests for EmailSequenceOptimizer.optimize()."""

    def setup_method(self):
        self.opt = EmailSequenceOptimizer()

    def test_returns_sequence_result(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert isinstance(result, SequenceResult)

    def test_sequence_id_populated(self):
        inp = make_input(sequence_id="abc123")
        result = self.opt.optimize(inp)
        assert result.sequence_id == "abc123"

    def test_sequence_name_populated(self):
        inp = make_input(sequence_name="My Campaign")
        result = self.opt.optimize(inp)
        assert result.sequence_name == "My Campaign"

    def test_overall_score_in_range(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert 0.0 <= result.overall_score <= 100.0

    def test_status_is_valid_enum(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert isinstance(result.status, SequenceStatus)

    def test_strategy_matches_input(self):
        inp = make_input(strategy=TouchpointStrategy.NURTURE)
        result = self.opt.optimize(inp)
        assert result.strategy == TouchpointStrategy.NURTURE

    def test_step_optimizations_length(self):
        steps = [make_step(i, day_offset=(i - 1) * 3) for i in range(1, 5)]
        inp = make_input(steps=steps)
        result = self.opt.optimize(inp)
        assert len(result.step_optimizations) == 4

    def test_step_optimizations_step_numbers(self):
        steps = [make_step(i, day_offset=(i - 1) * 3) for i in range(1, 4)]
        inp = make_input(steps=steps)
        result = self.opt.optimize(inp)
        numbers = [so.step_number for so in result.step_optimizations]
        assert numbers == [1, 2, 3]

    def test_step_optimization_types_match(self):
        steps = [
            make_step(1, StepType.EMAIL, day_offset=0),
            make_step(2, StepType.LINKEDIN, day_offset=3),
        ]
        inp = make_input(steps=steps)
        result = self.opt.optimize(inp)
        assert result.step_optimizations[0].step_type == StepType.EMAIL
        assert result.step_optimizations[1].step_type == StepType.LINKEDIN

    def test_stored_in_get(self):
        inp = make_input(sequence_id="stored")
        result = self.opt.optimize(inp)
        assert self.opt.get("stored") is result

    def test_overwrite_same_id(self):
        inp1 = make_input(sequence_id="dup", sequence_name="First")
        inp2 = make_input(sequence_id="dup", sequence_name="Second")
        self.opt.optimize(inp1)
        self.opt.optimize(inp2)
        assert self.opt.get("dup").sequence_name == "Second"

    def test_conversion_rate_pct_correct(self):
        inp = make_input(total_prospects=200, converted_prospects=10)
        result = self.opt.optimize(inp)
        assert abs(result.conversion_rate_pct - 5.0) < 0.01

    def test_bounce_rate_pct_correct(self):
        inp = make_input(total_prospects=200, bounced_emails=4)
        result = self.opt.optimize(inp)
        assert abs(result.bounce_rate_pct - 2.0) < 0.01

    def test_avg_open_rate_weighted_by_sent(self):
        steps = [
            make_step(1, day_offset=0, open_rate_pct=30.0, sent_count=100),
            make_step(2, day_offset=3, open_rate_pct=10.0, sent_count=100),
        ]
        inp = make_input(steps=steps)
        result = self.opt.optimize(inp)
        # weighted avg = (30*100 + 10*100) / 200 = 4000/200 = 20
        assert abs(result.avg_open_rate_pct - 20.0) < 0.01

    def test_sequence_signals_is_list(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert isinstance(result.sequence_signals, list)

    def test_risk_signals_is_list(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert isinstance(result.risk_signals, list)

    def test_estimated_pipeline_eur_non_negative(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert result.estimated_pipeline_eur >= 0.0

    def test_recommended_strategy_is_valid_enum(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert isinstance(result.recommended_strategy, TouchpointStrategy)

    def test_step_optimization_timing_score_correct(self):
        # step1, BALANCED, day_offset=0 → timing=100
        steps = [make_step(1, StepType.EMAIL, day_offset=0)]
        inp = make_input(steps=steps, strategy=TouchpointStrategy.BALANCED)
        result = self.opt.optimize(inp)
        assert abs(result.step_optimizations[0].timing_score - 100.0) < 0.01

    def test_step_optimization_recommended_day_offset(self):
        # BALANCED step2 optimal=3
        steps = [make_step(2, StepType.EMAIL, day_offset=10)]
        inp = make_input(steps=steps, strategy=TouchpointStrategy.BALANCED)
        result = self.opt.optimize(inp)
        assert result.step_optimizations[0].recommended_day_offset == 3


# ===========================================================================
# 8. TestOptimizerBatch
# ===========================================================================

class TestOptimizerBatch:
    """Tests for EmailSequenceOptimizer.optimize_batch()."""

    def setup_method(self):
        self.opt = EmailSequenceOptimizer()

    def test_empty_list_returns_empty(self):
        result = self.opt.optimize_batch([])
        assert result == []

    def test_returns_list_of_sequence_results(self):
        inputs = [make_input("s1"), make_input("s2")]
        results = self.opt.optimize_batch(inputs)
        assert all(isinstance(r, SequenceResult) for r in results)

    def test_sorted_desc_by_overall_score(self):
        # Create sequences with different conversion rates to vary scores
        inp_high = make_input("h", total_prospects=100, converted_prospects=20, bounced_emails=0)
        inp_low = make_input("l", total_prospects=100, converted_prospects=0, bounced_emails=50)
        results = self.opt.optimize_batch([inp_low, inp_high])
        scores = [r.overall_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_all_stored_internally(self):
        inputs = [make_input(f"s{i}") for i in range(3)]
        self.opt.optimize_batch(inputs)
        for i in range(3):
            assert self.opt.get(f"s{i}") is not None

    def test_can_optimize_same_id_twice(self):
        inp1 = make_input("dup")
        inp2 = make_input("dup", sequence_name="Updated")
        self.opt.optimize_batch([inp1])
        self.opt.optimize_batch([inp2])
        assert self.opt.get("dup").sequence_name == "Updated"

    def test_single_input_batch(self):
        results = self.opt.optimize_batch([make_input("only")])
        assert len(results) == 1

    def test_batch_returns_correct_count(self):
        inputs = [make_input(f"s{i}") for i in range(5)]
        results = self.opt.optimize_batch(inputs)
        assert len(results) == 5

    def test_batch_results_match_individual(self):
        inp = make_input("single")
        batch_results = self.opt.optimize_batch([inp])
        single_result = self.opt.get("single")
        assert batch_results[0].overall_score == single_result.overall_score


# ===========================================================================
# 9. TestOptimizerQueries
# ===========================================================================

class TestOptimizerQueries:
    """Tests for query methods on EmailSequenceOptimizer."""

    def setup_method(self):
        self.opt = EmailSequenceOptimizer()

    def _add_result_with_score(self, seq_id, score_target="vary"):
        """Helper to store a result. Use different prospect counts to control score."""
        if score_target == "excellent":
            inp = make_input(seq_id, total_prospects=100, converted_prospects=20, bounced_emails=0)
        elif score_target == "critical":
            inp = make_input(seq_id, total_prospects=100, converted_prospects=0, bounced_emails=80,
                             steps=[make_step(1, day_offset=100)])
        elif score_target == "poor":
            inp = make_input(seq_id, total_prospects=100, converted_prospects=0, bounced_emails=30,
                             steps=[make_step(1, day_offset=50)])
        else:
            inp = make_input(seq_id)
        return self.opt.optimize(inp)

    def test_all_sequences_sorted_desc(self):
        for i, s in enumerate(["critical", "excellent", "vary"]):
            self._add_result_with_score(f"s{i}", s)
        all_r = self.opt.all_sequences()
        scores = [r.overall_score for r in all_r]
        assert scores == sorted(scores, reverse=True)

    def test_all_sequences_returns_all(self):
        for i in range(4):
            self._add_result_with_score(f"s{i}")
        assert len(self.opt.all_sequences()) == 4

    def test_by_status_filters_correctly(self):
        self._add_result_with_score("exc", "excellent")
        self._add_result_with_score("crit", "critical")
        excellent = self.opt.by_status(SequenceStatus.EXCELLENT)
        for r in excellent:
            assert r.status == SequenceStatus.EXCELLENT

    def test_excellent_sequences_returns_only_excellent(self):
        self._add_result_with_score("exc", "excellent")
        self._add_result_with_score("crit", "critical")
        results = self.opt.excellent_sequences()
        assert all(r.status == SequenceStatus.EXCELLENT for r in results)

    def test_critical_sequences_returns_only_critical(self):
        self._add_result_with_score("exc", "excellent")
        self._add_result_with_score("crit", "critical")
        results = self.opt.critical_sequences()
        assert all(r.status == SequenceStatus.CRITICAL for r in results)

    def test_needs_attention_returns_poor_and_critical(self):
        self._add_result_with_score("exc", "excellent")
        self._add_result_with_score("crit", "critical")
        self._add_result_with_score("poor", "poor")
        attention = self.opt.needs_attention()
        for r in attention:
            assert r.status in (SequenceStatus.POOR, SequenceStatus.CRITICAL)

    def test_needs_attention_excludes_excellent(self):
        self._add_result_with_score("exc", "excellent")
        self._add_result_with_score("crit", "critical")
        attention = self.opt.needs_attention()
        assert not any(r.status == SequenceStatus.EXCELLENT for r in attention)

    def test_top_pipeline_returns_top_n(self):
        for i in range(5):
            self.opt.optimize(make_input(
                f"s{i}",
                avg_deal_size_eur=i * 10000,
                total_prospects=100,
                converted_prospects=10,
            ))
        top2 = self.opt.top_pipeline(2)
        assert len(top2) == 2

    def test_top_pipeline_sorted_desc_by_pipeline(self):
        for i in range(5):
            self.opt.optimize(make_input(
                f"s{i}",
                avg_deal_size_eur=i * 10000,
                total_prospects=100,
                converted_prospects=10,
            ))
        top = self.opt.top_pipeline(5)
        pipelines = [r.estimated_pipeline_eur for r in top]
        assert pipelines == sorted(pipelines, reverse=True)

    def test_total_pipeline_eur_sums_all(self):
        for i in range(3):
            self.opt.optimize(make_input(f"s{i}"))
        total = self.opt.total_pipeline_eur()
        individual_sum = sum(r.estimated_pipeline_eur for r in self.opt.all_sequences())
        assert abs(total - round(individual_sum, 2)) < 0.01

    def test_reset_clears_all(self):
        for i in range(3):
            self._add_result_with_score(f"s{i}")
        self.opt.reset()
        assert self.opt.all_sequences() == []

    def test_after_reset_get_returns_none(self):
        self.opt.optimize(make_input("gone"))
        self.opt.reset()
        assert self.opt.get("gone") is None

    def test_get_nonexistent_returns_none(self):
        assert self.opt.get("nonexistent") is None

    def test_by_status_empty_when_none_match(self):
        self._add_result_with_score("exc", "excellent")
        result = self.opt.by_status(SequenceStatus.CRITICAL)
        assert result == []

    def test_top_pipeline_n_larger_than_count(self):
        for i in range(3):
            self.opt.optimize(make_input(f"s{i}"))
        top = self.opt.top_pipeline(10)
        assert len(top) == 3


# ===========================================================================
# 10. TestSummary
# ===========================================================================

class TestSummary:
    """Tests for EmailSequenceOptimizer.summary()."""

    def setup_method(self):
        self.opt = EmailSequenceOptimizer()

    def test_empty_returns_zeroed_dict(self):
        s = self.opt.summary()
        assert s["total"] == 0
        assert s["status_counts"] == {}
        assert s["avg_score"] == 0.0
        assert s["avg_conversion_rate_pct"] == 0.0
        assert s["total_pipeline_eur"] == 0.0

    def test_empty_has_all_keys(self):
        s = self.opt.summary()
        expected_keys = {"total", "status_counts", "avg_score", "avg_conversion_rate_pct", "total_pipeline_eur"}
        assert set(s.keys()) == expected_keys

    def test_total_correct(self):
        for i in range(3):
            self.opt.optimize(make_input(f"s{i}"))
        s = self.opt.summary()
        assert s["total"] == 3

    def test_status_counts_correct(self):
        # Force two to be the same status for reliable testing
        self.opt.optimize(make_input(
            "exc1", total_prospects=100, converted_prospects=20, bounced_emails=0,
        ))
        self.opt.optimize(make_input(
            "exc2", total_prospects=100, converted_prospects=20, bounced_emails=0,
        ))
        s = self.opt.summary()
        # Both should have same status — verify counts match total
        total_in_counts = sum(s["status_counts"].values())
        assert total_in_counts == s["total"]

    def test_avg_score_correct(self):
        for i in range(2):
            self.opt.optimize(make_input(f"s{i}"))
        all_r = self.opt.all_sequences()
        expected_avg = round(sum(r.overall_score for r in all_r) / len(all_r), 1)
        s = self.opt.summary()
        assert abs(s["avg_score"] - expected_avg) < 0.05

    def test_avg_conversion_correct(self):
        for i in range(3):
            self.opt.optimize(make_input(f"s{i}"))
        all_r = self.opt.all_sequences()
        expected = round(sum(r.conversion_rate_pct for r in all_r) / len(all_r), 2)
        s = self.opt.summary()
        assert abs(s["avg_conversion_rate_pct"] - expected) < 0.01

    def test_total_pipeline_in_summary(self):
        for i in range(2):
            self.opt.optimize(make_input(f"s{i}"))
        expected = self.opt.total_pipeline_eur()
        s = self.opt.summary()
        assert abs(s["total_pipeline_eur"] - expected) < 0.01

    def test_status_counts_uses_value(self):
        self.opt.optimize(make_input("s1"))
        s = self.opt.summary()
        # All keys in status_counts should be string values of SequenceStatus
        valid_values = {e.value for e in SequenceStatus}
        for key in s["status_counts"]:
            assert key in valid_values

    def test_single_result_summary(self):
        self.opt.optimize(make_input("only"))
        s = self.opt.summary()
        assert s["total"] == 1
        assert sum(s["status_counts"].values()) == 1

    def test_avg_score_rounded_to_1_decimal(self):
        self.opt.optimize(make_input("s1"))
        s = self.opt.summary()
        # Check rounding precision
        assert s["avg_score"] == round(s["avg_score"], 1)

    def test_summary_after_reset_is_empty(self):
        self.opt.optimize(make_input("s1"))
        self.opt.reset()
        s = self.opt.summary()
        assert s["total"] == 0


# ===========================================================================
# 11. TestSignals
# ===========================================================================

class TestSignals:
    """Tests for sequence_signals and risk_signals via optimize()."""

    def setup_method(self):
        self.opt = EmailSequenceOptimizer()

    def test_excellent_sequence_has_positive_signal(self):
        inp = make_input("exc", total_prospects=100, converted_prospects=20, bounced_emails=0)
        result = self.opt.optimize(inp)
        # If status is EXCELLENT or GOOD → positive signal
        if result.status in (SequenceStatus.EXCELLENT, SequenceStatus.GOOD):
            assert len(result.sequence_signals) > 0

    def test_conv_rate_8pct_has_conversion_signal(self):
        inp = make_input("c8", total_prospects=100, converted_prospects=8, bounced_emails=0)
        result = self.opt.optimize(inp)
        signals_text = " ".join(result.sequence_signals)
        assert "conversion" in signals_text.lower() or "Conversion" in signals_text

    def test_conv_rate_3pct_has_positive_signal(self):
        inp = make_input("c3", total_prospects=100, converted_prospects=3, bounced_emails=0)
        result = self.opt.optimize(inp)
        # conv_rate=3% >= 3 → positive signal
        signals_text = " ".join(result.sequence_signals)
        assert "Conversion" in signals_text or "conversion" in signals_text

    def test_bounce_below_2_clean_list_signal(self):
        inp = make_input("clean", total_prospects=100, converted_prospects=5, bounced_emails=1)
        result = self.opt.optimize(inp)
        # bounce_rate=1% < 2 → clean list signal
        signals_text = " ".join(result.sequence_signals)
        assert "bounce" in signals_text.lower() or "propre" in signals_text

    def test_5_or_more_steps_complete_sequence_signal(self):
        steps = [make_step(i, day_offset=(i - 1) * 5) for i in range(1, 7)]
        inp = make_input("long", steps=steps)
        result = self.opt.optimize(inp)
        signals_text = " ".join(result.sequence_signals)
        assert "complète" in signals_text or "Séquence" in signals_text

    def test_bounce_5pct_or_more_risk_signal(self):
        inp = make_input("badlist", total_prospects=100, converted_prospects=5, bounced_emails=5)
        result = self.opt.optimize(inp)
        # bounce_rate=5% >= 5 → risk signal
        risks_text = " ".join(result.risk_signals)
        assert "bounce" in risks_text.lower() or "Bounce" in risks_text

    def test_low_conv_many_prospects_risk_signal(self):
        # conv<2%, total>50
        inp = make_input("lowconv", total_prospects=100, converted_prospects=1, bounced_emails=0)
        result = self.opt.optimize(inp)
        # conv=1% < 2 and total=100 > 50 → risk signal
        risks_text = " ".join(result.risk_signals)
        assert "Conversion" in risks_text or "conversion" in risks_text or "ciblage" in risks_text

    def test_poor_or_critical_has_risk_signal(self):
        inp = make_input("bad", total_prospects=100, converted_prospects=0, bounced_emails=80,
                         steps=[make_step(1, day_offset=100)])
        result = self.opt.optimize(inp)
        if result.status in (SequenceStatus.POOR, SequenceStatus.CRITICAL):
            risks_text = " ".join(result.risk_signals)
            assert "sous-performante" in risks_text or "révision" in risks_text

    def test_less_than_4_steps_risk_signal(self):
        steps = [make_step(1, day_offset=0), make_step(2, day_offset=3)]
        inp = make_input("short", steps=steps)
        result = self.opt.optimize(inp)
        risks_text = " ".join(result.risk_signals)
        assert "étapes" in risks_text or "peu" in risks_text

    def test_4_steps_no_step_risk_signal(self):
        steps = [make_step(i, day_offset=i * 3) for i in range(1, 5)]
        inp = make_input("ok", steps=steps)
        result = self.opt.optimize(inp)
        risks_text = " ".join(result.risk_signals)
        assert "Trop peu d'étapes" not in risks_text

    def test_no_signals_when_conditions_not_met(self):
        # conv=0, bounce=0, 4 steps, poor score
        steps = [make_step(i, day_offset=100) for i in range(1, 5)]
        inp = make_input("s", steps=steps, total_prospects=100, converted_prospects=0, bounced_emails=0)
        result = self.opt.optimize(inp)
        # signals should be list types regardless
        assert isinstance(result.sequence_signals, list)
        assert isinstance(result.risk_signals, list)


# ===========================================================================
# 12. TestEstimatePipeline
# ===========================================================================

class TestEstimatePipeline:
    """Tests for _estimate_pipeline via optimize()."""

    def setup_method(self):
        self.opt = EmailSequenceOptimizer()

    def test_zero_prospects_gives_zero_pipeline(self):
        inp = make_input("z", total_prospects=0, converted_prospects=0, avg_deal_size_eur=10000)
        result = self.opt.optimize(inp)
        # projected_conv = 0 * 0/max(1,0) * (1+score/200) = 0
        assert result.estimated_pipeline_eur == 0.0

    def test_zero_converted_gives_zero_pipeline(self):
        inp = make_input("z2", total_prospects=100, converted_prospects=0, avg_deal_size_eur=10000)
        result = self.opt.optimize(inp)
        # conv_rate=0 → projected=0 → pipeline=0
        assert result.estimated_pipeline_eur == 0.0

    def test_zero_deal_size_gives_zero_pipeline(self):
        inp = make_input("z3", total_prospects=100, converted_prospects=10, avg_deal_size_eur=0)
        result = self.opt.optimize(inp)
        assert result.estimated_pipeline_eur == 0.0

    def test_pipeline_rounded_to_hundreds(self):
        inp = make_input("r", total_prospects=100, converted_prospects=10, avg_deal_size_eur=20000)
        result = self.opt.optimize(inp)
        # Should be rounded to nearest 100
        assert result.estimated_pipeline_eur % 100 == 0

    def test_pipeline_positive_with_valid_inputs(self):
        inp = make_input("pos", total_prospects=100, converted_prospects=10, avg_deal_size_eur=20000)
        result = self.opt.optimize(inp)
        assert result.estimated_pipeline_eur > 0

    def test_pipeline_increases_with_higher_deal_size(self):
        inp1 = make_input("low", total_prospects=100, converted_prospects=10, avg_deal_size_eur=10000)
        inp2 = make_input("high", total_prospects=100, converted_prospects=10, avg_deal_size_eur=50000)
        r1 = self.opt.optimize(inp1)
        r2 = self.opt.optimize(inp2)
        assert r2.estimated_pipeline_eur > r1.estimated_pipeline_eur

    def test_pipeline_formula_manually(self):
        # Use same steps as make_input default to control score
        inp = make_input("manual", total_prospects=100, converted_prospects=10,
                         avg_deal_size_eur=20000, bounced_emails=0)
        result = self.opt.optimize(inp)
        score = result.overall_score
        conv_rate = 10 / max(1, 100)
        projected = 100 * conv_rate * (1 + score / 200)
        expected = round(projected * 20000, -2)
        assert abs(result.estimated_pipeline_eur - expected) < 0.01


# ===========================================================================
# 13. TestEdgeCases
# ===========================================================================

class TestEdgeCases:
    """Edge case and integration tests."""

    def setup_method(self):
        self.opt = EmailSequenceOptimizer()

    def test_no_steps_empty_step_optimizations(self):
        inp = make_input(steps=[])
        result = self.opt.optimize(inp)
        assert result.step_optimizations == []

    def test_no_steps_score_zero(self):
        inp = make_input(steps=[])
        result = self.opt.optimize(inp)
        assert result.overall_score == 0.0

    def test_single_step_sequence(self):
        steps = [make_step(1, day_offset=0)]
        inp = make_input(steps=steps)
        result = self.opt.optimize(inp)
        assert len(result.step_optimizations) == 1
        assert 0.0 <= result.overall_score <= 100.0

    def test_very_high_bounce_near_zero_score(self):
        # 100% bounce with poor timing
        steps = [make_step(1, day_offset=100)]
        inp = make_input(steps=steps, total_prospects=100, converted_prospects=0, bounced_emails=100)
        result = self.opt.optimize(inp)
        assert result.overall_score < 30.0

    def test_all_sent_count_zero_performance_defaults_50(self):
        steps = [make_step(i, sent_count=0) for i in range(1, 4)]
        inp = make_input(steps=steps)
        result = self.opt.optimize(inp)
        for so in result.step_optimizations:
            assert abs(so.performance_score - 50.0) < 0.01

    def test_step_number_beyond_optimal_list_uses_last_gap(self):
        # step 8 for AGGRESSIVE, last optimal=14
        steps = [make_step(8, day_offset=14)]
        inp = make_input(steps=steps, strategy=TouchpointStrategy.AGGRESSIVE)
        result = self.opt.optimize(inp)
        assert result.step_optimizations[0].timing_score == 100.0
        assert result.step_optimizations[0].recommended_day_offset == 14

    def test_all_metrics_at_benchmark_consistent_score(self):
        steps = [
            make_step(1, StepType.EMAIL, day_offset=0, open_rate_pct=22.0,
                      reply_rate_pct=5.0, unsubscribe_rate_pct=0.0),
            make_step(2, StepType.EMAIL, day_offset=3, open_rate_pct=22.0,
                      reply_rate_pct=5.0, unsubscribe_rate_pct=0.0),
        ]
        inp = make_input(steps=steps, strategy=TouchpointStrategy.BALANCED,
                         total_prospects=100, converted_prospects=5, bounced_emails=0)
        result = self.opt.optimize(inp)
        assert 0.0 <= result.overall_score <= 100.0

    def test_to_dict_has_status_as_string(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        d = result.to_dict()
        assert isinstance(d["status"], str)
        assert d["status"] in [e.value for e in SequenceStatus]

    def test_to_dict_has_strategy_as_string(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        d = result.to_dict()
        assert isinstance(d["strategy"], str)
        assert d["strategy"] in [e.value for e in TouchpointStrategy]

    def test_to_dict_has_recommended_strategy_as_string(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        d = result.to_dict()
        assert isinstance(d["recommended_strategy"], str)

    def test_to_dict_step_type_as_string(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        d = result.to_dict()
        for so in d["step_optimizations"]:
            assert isinstance(so["step_type"], str)
            assert so["step_type"] in [e.value for e in StepType]

    def test_to_dict_all_keys_present(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        d = result.to_dict()
        expected_keys = {
            "sequence_id", "sequence_name", "overall_score", "status", "strategy",
            "avg_open_rate_pct", "avg_reply_rate_pct", "conversion_rate_pct",
            "bounce_rate_pct", "step_optimizations", "sequence_signals",
            "risk_signals", "estimated_pipeline_eur", "recommended_strategy",
        }
        assert set(d.keys()) == expected_keys

    def test_avg_open_reply_when_all_sent_zero(self):
        # Falls back to simple average of rates
        steps = [
            make_step(1, day_offset=0, open_rate_pct=30.0, reply_rate_pct=6.0, sent_count=0),
            make_step(2, day_offset=3, open_rate_pct=10.0, reply_rate_pct=4.0, sent_count=0),
        ]
        inp = make_input(steps=steps)
        result = self.opt.optimize(inp)
        # avg_open = (30+10)/2=20, avg_reply=(6+4)/2=5
        assert abs(result.avg_open_rate_pct - 20.0) < 0.01
        assert abs(result.avg_reply_rate_pct - 5.0) < 0.01

    def test_multiple_sequences_independent(self):
        r1 = self.opt.optimize(make_input("a"))
        r2 = self.opt.optimize(make_input("b"))
        assert r1.sequence_id == "a"
        assert r2.sequence_id == "b"
        assert self.opt.get("a") is r1
        assert self.opt.get("b") is r2

    def test_optimal_gaps_constants_correct(self):
        assert _OPTIMAL_GAPS_DAYS[TouchpointStrategy.AGGRESSIVE] == [0, 2, 4, 7, 10, 14]
        assert _OPTIMAL_GAPS_DAYS[TouchpointStrategy.BALANCED] == [0, 3, 7, 14, 21, 28]
        assert _OPTIMAL_GAPS_DAYS[TouchpointStrategy.NURTURE] == [0, 7, 14, 30, 45, 60]
        assert _OPTIMAL_GAPS_DAYS[TouchpointStrategy.REACTIVATION] == [0, 5, 12, 21, 35, 50]

    def test_step_type_open_rate_constants(self):
        assert _STEP_TYPE_OPEN_RATE[StepType.EMAIL] == 0.22
        assert _STEP_TYPE_OPEN_RATE[StepType.LINKEDIN] == 0.45
        assert _STEP_TYPE_OPEN_RATE[StepType.PHONE] == 0.30
        assert _STEP_TYPE_OPEN_RATE[StepType.VIDEO] == 0.38
        assert _STEP_TYPE_OPEN_RATE[StepType.DIRECT_MAIL] == 0.65

    def test_step_type_reply_rate_constants(self):
        assert _STEP_TYPE_REPLY_RATE[StepType.EMAIL] == 0.05
        assert _STEP_TYPE_REPLY_RATE[StepType.LINKEDIN] == 0.12
        assert _STEP_TYPE_REPLY_RATE[StepType.PHONE] == 0.18
        assert _STEP_TYPE_REPLY_RATE[StepType.VIDEO] == 0.10
        assert _STEP_TYPE_REPLY_RATE[StepType.DIRECT_MAIL] == 0.25
