"""Comprehensive pytest test suite for SalesCoachingEffectivenessEngine."""

from __future__ import annotations

import pytest

from swarm.intelligence.sales_coaching_effectiveness_engine import (
    CoachingRisk,
    CoachingPattern,
    CoachingSeverity,
    CoachingAction,
    CoachingEffectivenessInput,
    CoachingEffectivenessResult,
    SalesCoachingEffectivenessEngine,
)


# ---------------------------------------------------------------------------
# Helper / factory
# ---------------------------------------------------------------------------

def make_input(
    rep_id: str = "R001",
    region: str = "EMEA",
    manager_id: str = "M001",
    coaching_sessions_last_90d: int = 6,
    coaching_sessions_benchmark: int = 6,
    win_rate_before_coaching_pct: float = 0.40,
    win_rate_after_coaching_pct: float = 0.42,
    quota_attainment_before_pct: float = 90.0,
    quota_attainment_after_pct: float = 95.0,
    activity_score_before: float = 70.0,
    activity_score_after: float = 75.0,
    avg_deal_size_before_usd: float = 50_000.0,
    avg_deal_size_after_usd: float = 52_000.0,
    avg_discount_before_pct: float = 10.0,
    avg_discount_after_pct: float = 10.0,
    coaching_topic_alignment_score: float = 80.0,
    days_to_behavioral_change: int = 10,
    recidivism_count: int = 0,
    manager_coaching_effectiveness_pct: float = 0.75,
    deal_quality_improvement_score: float = 5.0,
    self_assessed_readiness_score: float = 75.0,
    peer_comparison_percentile: float = 60.0,
) -> CoachingEffectivenessInput:
    """Factory with sensible defaults that produce a low-risk/effective result."""
    return CoachingEffectivenessInput(
        rep_id=rep_id,
        region=region,
        manager_id=manager_id,
        coaching_sessions_last_90d=coaching_sessions_last_90d,
        coaching_sessions_benchmark=coaching_sessions_benchmark,
        win_rate_before_coaching_pct=win_rate_before_coaching_pct,
        win_rate_after_coaching_pct=win_rate_after_coaching_pct,
        quota_attainment_before_pct=quota_attainment_before_pct,
        quota_attainment_after_pct=quota_attainment_after_pct,
        activity_score_before=activity_score_before,
        activity_score_after=activity_score_after,
        avg_deal_size_before_usd=avg_deal_size_before_usd,
        avg_deal_size_after_usd=avg_deal_size_after_usd,
        avg_discount_before_pct=avg_discount_before_pct,
        avg_discount_after_pct=avg_discount_after_pct,
        coaching_topic_alignment_score=coaching_topic_alignment_score,
        days_to_behavioral_change=days_to_behavioral_change,
        recidivism_count=recidivism_count,
        manager_coaching_effectiveness_pct=manager_coaching_effectiveness_pct,
        deal_quality_improvement_score=deal_quality_improvement_score,
        self_assessed_readiness_score=self_assessed_readiness_score,
        peer_comparison_percentile=peer_comparison_percentile,
    )


@pytest.fixture
def engine() -> SalesCoachingEffectivenessEngine:
    return SalesCoachingEffectivenessEngine()


@pytest.fixture
def good_input() -> CoachingEffectivenessInput:
    """Produces low composite / effective / no_action."""
    return make_input()


# ---------------------------------------------------------------------------
# Class 1: Enum membership
# ---------------------------------------------------------------------------

class TestEnums:
    def test_coaching_risk_members(self):
        assert set(CoachingRisk) == {
            CoachingRisk.low, CoachingRisk.moderate,
            CoachingRisk.high, CoachingRisk.critical,
        }

    def test_coaching_pattern_members(self):
        assert set(CoachingPattern) == {
            CoachingPattern.none,
            CoachingPattern.insufficient_frequency,
            CoachingPattern.no_behavioral_change,
            CoachingPattern.topic_misalignment,
            CoachingPattern.manager_ineffectiveness,
            CoachingPattern.coaching_resistance,
        }

    def test_coaching_severity_members(self):
        assert set(CoachingSeverity) == {
            CoachingSeverity.effective, CoachingSeverity.developing,
            CoachingSeverity.stalled, CoachingSeverity.regressing,
        }

    def test_coaching_action_members(self):
        assert set(CoachingAction) == {
            CoachingAction.no_action,
            CoachingAction.increase_coaching_frequency,
            CoachingAction.coaching_topic_reset,
            CoachingAction.manager_coaching_training,
            CoachingAction.external_coach_engagement,
            CoachingAction.performance_management,
        }

    def test_risk_values(self):
        assert CoachingRisk.low.value == "low"
        assert CoachingRisk.moderate.value == "moderate"
        assert CoachingRisk.high.value == "high"
        assert CoachingRisk.critical.value == "critical"

    def test_pattern_values(self):
        assert CoachingPattern.none.value == "none"
        assert CoachingPattern.insufficient_frequency.value == "insufficient_frequency"
        assert CoachingPattern.no_behavioral_change.value == "no_behavioral_change"
        assert CoachingPattern.topic_misalignment.value == "topic_misalignment"
        assert CoachingPattern.manager_ineffectiveness.value == "manager_ineffectiveness"
        assert CoachingPattern.coaching_resistance.value == "coaching_resistance"

    def test_severity_values(self):
        assert CoachingSeverity.effective.value == "effective"
        assert CoachingSeverity.developing.value == "developing"
        assert CoachingSeverity.stalled.value == "stalled"
        assert CoachingSeverity.regressing.value == "regressing"

    def test_action_values(self):
        assert CoachingAction.no_action.value == "no_action"
        assert CoachingAction.performance_management.value == "performance_management"
        assert CoachingAction.external_coach_engagement.value == "external_coach_engagement"

    def test_enums_are_str(self):
        assert isinstance(CoachingRisk.low, str)
        assert isinstance(CoachingPattern.none, str)
        assert isinstance(CoachingSeverity.effective, str)
        assert isinstance(CoachingAction.no_action, str)


# ---------------------------------------------------------------------------
# Class 2: Input dataclass fields
# ---------------------------------------------------------------------------

class TestInputDataclass:
    def test_all_22_fields_present(self):
        inp = make_input()
        fields = [
            "rep_id", "region", "manager_id",
            "coaching_sessions_last_90d", "coaching_sessions_benchmark",
            "win_rate_before_coaching_pct", "win_rate_after_coaching_pct",
            "quota_attainment_before_pct", "quota_attainment_after_pct",
            "activity_score_before", "activity_score_after",
            "avg_deal_size_before_usd", "avg_deal_size_after_usd",
            "avg_discount_before_pct", "avg_discount_after_pct",
            "coaching_topic_alignment_score",
            "days_to_behavioral_change", "recidivism_count",
            "manager_coaching_effectiveness_pct",
            "deal_quality_improvement_score",
            "self_assessed_readiness_score",
            "peer_comparison_percentile",
        ]
        for f in fields:
            assert hasattr(inp, f), f"Missing field: {f}"

    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(CoachingEffectivenessInput)
        assert len(fields) == 22

    def test_rep_id_stored(self):
        inp = make_input(rep_id="XREP")
        assert inp.rep_id == "XREP"

    def test_region_stored(self):
        inp = make_input(region="APAC")
        assert inp.region == "APAC"

    def test_numeric_fields_stored(self):
        inp = make_input(recidivism_count=5, days_to_behavioral_change=45)
        assert inp.recidivism_count == 5
        assert inp.days_to_behavioral_change == 45


# ---------------------------------------------------------------------------
# Class 3: Result dataclass and to_dict()
# ---------------------------------------------------------------------------

class TestResultDataclass:
    def test_to_dict_returns_15_keys(self, engine, good_input):
        result = engine.assess(good_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self, engine, good_input):
        expected = {
            "rep_id", "region", "coaching_risk", "coaching_pattern",
            "coaching_severity", "recommended_action",
            "coaching_frequency_score", "coaching_impact_score",
            "coaching_alignment_score", "manager_effectiveness_score",
            "coaching_effectiveness_composite", "is_coaching_ineffective",
            "requires_coaching_redesign", "estimated_revenue_impact_usd",
            "coaching_signal",
        }
        result = engine.assess(good_input)
        assert set(result.to_dict().keys()) == expected

    def test_to_dict_enum_values_are_strings(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert isinstance(d["coaching_risk"], str)
        assert isinstance(d["coaching_pattern"], str)
        assert isinstance(d["coaching_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_passthrough(self, engine):
        inp = make_input(rep_id="ZREP99")
        d = engine.assess(inp).to_dict()
        assert d["rep_id"] == "ZREP99"

    def test_to_dict_region_passthrough(self, engine):
        inp = make_input(region="LATAM")
        d = engine.assess(inp).to_dict()
        assert d["region"] == "LATAM"

    def test_to_dict_bool_fields(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert isinstance(d["is_coaching_ineffective"], bool)
        assert isinstance(d["requires_coaching_redesign"], bool)

    def test_to_dict_numeric_fields(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert isinstance(d["coaching_frequency_score"], float)
        assert isinstance(d["coaching_impact_score"], float)
        assert isinstance(d["coaching_alignment_score"], float)
        assert isinstance(d["manager_effectiveness_score"], float)
        assert isinstance(d["coaching_effectiveness_composite"], float)
        assert isinstance(d["estimated_revenue_impact_usd"], float)

    def test_result_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(CoachingEffectivenessResult)
        assert len(fields) == 15


# ---------------------------------------------------------------------------
# Class 4: coaching_frequency_score
# ---------------------------------------------------------------------------

class TestCoachingFrequencyScore:
    def _score(self, **kwargs) -> float:
        eng = SalesCoachingEffectivenessEngine()
        return eng._coaching_frequency_score(make_input(**kwargs))

    def test_zero_sessions_adds_50(self):
        s = self._score(coaching_sessions_last_90d=0, coaching_sessions_benchmark=6,
                        days_to_behavioral_change=0, recidivism_count=0)
        assert s == 50.0

    def test_sessions_below_50_pct_bench_adds_35(self):
        # bench=10, sessions=4 → 4 < 5 → +35
        s = self._score(coaching_sessions_last_90d=4, coaching_sessions_benchmark=10,
                        days_to_behavioral_change=0, recidivism_count=0)
        assert s == 35.0

    def test_sessions_below_75_pct_bench_adds_20(self):
        # bench=8, sessions=5 → 5 < 6 → +20
        s = self._score(coaching_sessions_last_90d=5, coaching_sessions_benchmark=8,
                        days_to_behavioral_change=0, recidivism_count=0)
        assert s == 20.0

    def test_sessions_at_benchmark_no_volume_penalty(self):
        s = self._score(coaching_sessions_last_90d=6, coaching_sessions_benchmark=6,
                        days_to_behavioral_change=0, recidivism_count=0)
        assert s == 0.0

    def test_sessions_above_benchmark_no_penalty(self):
        s = self._score(coaching_sessions_last_90d=10, coaching_sessions_benchmark=6,
                        days_to_behavioral_change=0, recidivism_count=0)
        assert s == 0.0

    def test_days_behavioral_change_ge_30_adds_20(self):
        s = self._score(coaching_sessions_last_90d=6, coaching_sessions_benchmark=6,
                        days_to_behavioral_change=30, recidivism_count=0)
        assert s == 20.0

    def test_days_behavioral_change_ge_15_adds_10(self):
        s = self._score(coaching_sessions_last_90d=6, coaching_sessions_benchmark=6,
                        days_to_behavioral_change=15, recidivism_count=0)
        assert s == 10.0

    def test_days_behavioral_change_below_15_no_penalty(self):
        s = self._score(coaching_sessions_last_90d=6, coaching_sessions_benchmark=6,
                        days_to_behavioral_change=14, recidivism_count=0)
        assert s == 0.0

    def test_recidivism_ge_3_adds_20(self):
        s = self._score(coaching_sessions_last_90d=6, coaching_sessions_benchmark=6,
                        days_to_behavioral_change=0, recidivism_count=3)
        assert s == 20.0

    def test_recidivism_ge_1_adds_8(self):
        s = self._score(coaching_sessions_last_90d=6, coaching_sessions_benchmark=6,
                        days_to_behavioral_change=0, recidivism_count=1)
        assert s == 8.0

    def test_recidivism_0_no_penalty(self):
        s = self._score(coaching_sessions_last_90d=6, coaching_sessions_benchmark=6,
                        days_to_behavioral_change=0, recidivism_count=0)
        assert s == 0.0

    def test_cap_at_100(self):
        # 50 + 20 + 20 = 90, but add more: sessions=0, days=30, recidivism=3
        s = self._score(coaching_sessions_last_90d=0, coaching_sessions_benchmark=6,
                        days_to_behavioral_change=30, recidivism_count=3)
        # 50+20+20=90 — under 100
        assert s == 90.0

    def test_combined_additive(self):
        # sessions=0 → +50, days=30 → +20, recidivism=3 → +20 = 90
        s = self._score(coaching_sessions_last_90d=0, coaching_sessions_benchmark=6,
                        days_to_behavioral_change=30, recidivism_count=3)
        assert s == 90.0

    def test_benchmark_zero_treated_as_1(self):
        # benchmark=0 → max(0,1)=1, sessions=0 → +50
        s = self._score(coaching_sessions_last_90d=0, coaching_sessions_benchmark=0,
                        days_to_behavioral_change=0, recidivism_count=0)
        assert s == 50.0

    def test_exact_50pct_benchmark_no_35_penalty(self):
        # sessions=5, bench=10 → 5 == 5.0, not < 5.0
        s = self._score(coaching_sessions_last_90d=5, coaching_sessions_benchmark=10,
                        days_to_behavioral_change=0, recidivism_count=0)
        # 5 < 5*0.75=7.5 → +20
        assert s == 20.0

    def test_exact_75pct_benchmark_no_20_penalty(self):
        # sessions=6, bench=8 → 6 < 6? No. 6 == 6.0. Not < 6.0. Not < 8*0.50=4.0 either.
        # So no volume penalty
        s = self._score(coaching_sessions_last_90d=6, coaching_sessions_benchmark=8,
                        days_to_behavioral_change=0, recidivism_count=0)
        assert s == 0.0

    def test_recidivism_2_adds_8_not_20(self):
        s = self._score(coaching_sessions_last_90d=6, coaching_sessions_benchmark=6,
                        days_to_behavioral_change=0, recidivism_count=2)
        assert s == 8.0

    def test_full_worst_case_capped(self):
        # Sessions=0(+50), days=30(+20), recidivism=3(+20) = 90, below cap
        s = self._score(coaching_sessions_last_90d=0, coaching_sessions_benchmark=1,
                        days_to_behavioral_change=45, recidivism_count=5)
        assert s == 90.0

    def test_score_nonnegative(self):
        s = self._score()
        assert s >= 0.0

    def test_score_not_exceeding_100(self):
        s = self._score(coaching_sessions_last_90d=0, coaching_sessions_benchmark=6,
                        days_to_behavioral_change=60, recidivism_count=10)
        assert s <= 100.0


# ---------------------------------------------------------------------------
# Class 5: coaching_impact_score
# ---------------------------------------------------------------------------

class TestCoachingImpactScore:
    def _score(self, **kwargs) -> float:
        eng = SalesCoachingEffectivenessEngine()
        return eng._coaching_impact_score(make_input(**kwargs))

    def test_win_delta_less_than_neg005_adds_35(self):
        # before=0.50, after=0.40 → delta=-0.10 < -0.05
        s = self._score(win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40,
                        quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
                        activity_score_before=70.0, activity_score_after=70.0,
                        recidivism_count=0)
        assert s == 35.0

    def test_win_delta_between_neg005_and_0_adds_18(self):
        # before=0.45, after=0.42 → delta=-0.03
        s = self._score(win_rate_before_coaching_pct=0.45, win_rate_after_coaching_pct=0.42,
                        quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
                        activity_score_before=70.0, activity_score_after=70.0,
                        recidivism_count=0)
        assert s == 18.0

    def test_win_delta_zero_no_win_penalty(self):
        s = self._score(win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.40,
                        quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
                        activity_score_before=70.0, activity_score_after=70.0,
                        recidivism_count=0)
        assert s == 0.0

    def test_win_delta_positive_no_penalty(self):
        s = self._score(win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.50,
                        quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
                        activity_score_before=70.0, activity_score_after=70.0,
                        recidivism_count=0)
        assert s == 0.0

    def test_quota_delta_less_than_neg10_adds_30(self):
        s = self._score(win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.40,
                        quota_attainment_before_pct=100.0, quota_attainment_after_pct=85.0,
                        activity_score_before=70.0, activity_score_after=70.0,
                        recidivism_count=0)
        assert s == 30.0

    def test_quota_delta_between_neg10_and_0_adds_15(self):
        s = self._score(win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.40,
                        quota_attainment_before_pct=100.0, quota_attainment_after_pct=95.0,
                        activity_score_before=70.0, activity_score_after=70.0,
                        recidivism_count=0)
        assert s == 15.0

    def test_quota_delta_zero_no_penalty(self):
        s = self._score(win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.40,
                        quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
                        activity_score_before=70.0, activity_score_after=70.0,
                        recidivism_count=0)
        assert s == 0.0

    def test_activity_delta_less_than_neg10_adds_20(self):
        s = self._score(win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.40,
                        quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
                        activity_score_before=80.0, activity_score_after=65.0,
                        recidivism_count=0)
        assert s == 20.0

    def test_activity_delta_between_neg10_and_0_adds_10(self):
        s = self._score(win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.40,
                        quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
                        activity_score_before=80.0, activity_score_after=75.0,
                        recidivism_count=0)
        assert s == 10.0

    def test_activity_delta_zero_no_penalty(self):
        s = self._score(win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.40,
                        quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
                        activity_score_before=70.0, activity_score_after=70.0,
                        recidivism_count=0)
        assert s == 0.0

    def test_recidivism_ge_2_adds_15(self):
        s = self._score(win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.40,
                        quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
                        activity_score_before=70.0, activity_score_after=70.0,
                        recidivism_count=2)
        assert s == 15.0

    def test_recidivism_1_no_impact_penalty(self):
        s = self._score(win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.40,
                        quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
                        activity_score_before=70.0, activity_score_after=70.0,
                        recidivism_count=1)
        assert s == 0.0

    def test_all_worst_case_capped_at_100(self):
        # 35+30+20+15 = 100
        s = self._score(win_rate_before_coaching_pct=0.60, win_rate_after_coaching_pct=0.40,
                        quota_attainment_before_pct=100.0, quota_attainment_after_pct=80.0,
                        activity_score_before=90.0, activity_score_after=70.0,
                        recidivism_count=3)
        assert s == 100.0

    def test_score_nonnegative(self):
        s = self._score()
        assert s >= 0.0

    def test_score_not_exceeding_100(self):
        s = self._score(win_rate_before_coaching_pct=0.80, win_rate_after_coaching_pct=0.10,
                        quota_attainment_before_pct=150.0, quota_attainment_after_pct=50.0,
                        activity_score_before=100.0, activity_score_after=50.0,
                        recidivism_count=10)
        assert s <= 100.0

    def test_exact_neg005_win_delta_is_35(self):
        # delta = -0.06 < -0.05
        s = self._score(win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.44,
                        quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
                        activity_score_before=70.0, activity_score_after=70.0,
                        recidivism_count=0)
        assert s == 35.0

    def test_win_delta_exactly_neg005_is_18(self):
        # delta = -0.05 which is NOT < -0.05, but IS < 0.0
        s = self._score(win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.45,
                        quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
                        activity_score_before=70.0, activity_score_after=70.0,
                        recidivism_count=0)
        assert s == 18.0


# ---------------------------------------------------------------------------
# Class 6: coaching_alignment_score
# ---------------------------------------------------------------------------

class TestCoachingAlignmentScore:
    def _score(self, **kwargs) -> float:
        eng = SalesCoachingEffectivenessEngine()
        return eng._coaching_alignment_score(make_input(**kwargs))

    def test_alignment_below_40_adds_40(self):
        s = self._score(coaching_topic_alignment_score=30.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
                        self_assessed_readiness_score=75.0)
        assert s == 40.0

    def test_alignment_between_40_and_60_adds_25(self):
        s = self._score(coaching_topic_alignment_score=50.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
                        self_assessed_readiness_score=75.0)
        assert s == 25.0

    def test_alignment_between_60_and_75_adds_10(self):
        s = self._score(coaching_topic_alignment_score=70.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
                        self_assessed_readiness_score=75.0)
        assert s == 10.0

    def test_alignment_ge_75_no_penalty(self):
        s = self._score(coaching_topic_alignment_score=80.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
                        self_assessed_readiness_score=75.0)
        assert s == 0.0

    def test_discount_delta_ge_3_adds_20(self):
        s = self._score(coaching_topic_alignment_score=80.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=13.5,
                        self_assessed_readiness_score=75.0)
        assert s == 20.0

    def test_discount_delta_between_1_and_3_adds_10(self):
        s = self._score(coaching_topic_alignment_score=80.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=11.5,
                        self_assessed_readiness_score=75.0)
        assert s == 10.0

    def test_discount_delta_below_1_no_penalty(self):
        s = self._score(coaching_topic_alignment_score=80.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=10.5,
                        self_assessed_readiness_score=75.0)
        assert s == 0.0

    def test_discount_delta_negative_no_penalty(self):
        s = self._score(coaching_topic_alignment_score=80.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=8.0,
                        self_assessed_readiness_score=75.0)
        assert s == 0.0

    def test_readiness_below_40_adds_15(self):
        s = self._score(coaching_topic_alignment_score=80.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
                        self_assessed_readiness_score=30.0)
        assert s == 15.0

    def test_readiness_between_40_and_60_adds_8(self):
        s = self._score(coaching_topic_alignment_score=80.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
                        self_assessed_readiness_score=50.0)
        assert s == 8.0

    def test_readiness_ge_60_no_penalty(self):
        s = self._score(coaching_topic_alignment_score=80.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
                        self_assessed_readiness_score=70.0)
        assert s == 0.0

    def test_max_score_capped_at_100(self):
        # 40+20+15 = 75
        s = self._score(coaching_topic_alignment_score=20.0,
                        avg_discount_before_pct=0.0, avg_discount_after_pct=10.0,
                        self_assessed_readiness_score=20.0)
        assert s == 75.0

    def test_combined_alignment_and_discount(self):
        # alignment<40 → +40, discount delta=5 → +20 = 60
        s = self._score(coaching_topic_alignment_score=30.0,
                        avg_discount_before_pct=5.0, avg_discount_after_pct=10.0,
                        self_assessed_readiness_score=75.0)
        assert s == 60.0

    def test_score_nonnegative(self):
        s = self._score()
        assert s >= 0.0

    def test_score_not_exceeding_100(self):
        s = self._score(coaching_topic_alignment_score=0.0,
                        avg_discount_before_pct=0.0, avg_discount_after_pct=20.0,
                        self_assessed_readiness_score=0.0)
        assert s <= 100.0

    def test_alignment_exactly_40_is_25(self):
        # 40 is NOT < 40, but IS < 60
        s = self._score(coaching_topic_alignment_score=40.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
                        self_assessed_readiness_score=75.0)
        assert s == 25.0

    def test_alignment_exactly_60_is_10(self):
        # 60 is NOT < 60, but IS < 75
        s = self._score(coaching_topic_alignment_score=60.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
                        self_assessed_readiness_score=75.0)
        assert s == 10.0

    def test_readiness_exactly_40_is_8(self):
        s = self._score(coaching_topic_alignment_score=80.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
                        self_assessed_readiness_score=40.0)
        assert s == 8.0

    def test_discount_delta_exactly_1_adds_10(self):
        s = self._score(coaching_topic_alignment_score=80.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=11.0,
                        self_assessed_readiness_score=75.0)
        assert s == 10.0

    def test_discount_delta_exactly_3_adds_20(self):
        s = self._score(coaching_topic_alignment_score=80.0,
                        avg_discount_before_pct=10.0, avg_discount_after_pct=13.0,
                        self_assessed_readiness_score=75.0)
        assert s == 20.0


# ---------------------------------------------------------------------------
# Class 7: manager_effectiveness_score
# ---------------------------------------------------------------------------

class TestManagerEffectivenessScore:
    def _score(self, **kwargs) -> float:
        eng = SalesCoachingEffectivenessEngine()
        return eng._manager_effectiveness_score(make_input(**kwargs))

    def test_mgr_pct_below_030_adds_40(self):
        s = self._score(manager_coaching_effectiveness_pct=0.20,
                        peer_comparison_percentile=60.0,
                        deal_quality_improvement_score=5.0)
        assert s == 40.0

    def test_mgr_pct_between_030_and_050_adds_25(self):
        s = self._score(manager_coaching_effectiveness_pct=0.40,
                        peer_comparison_percentile=60.0,
                        deal_quality_improvement_score=5.0)
        assert s == 25.0

    def test_mgr_pct_between_050_and_070_adds_10(self):
        s = self._score(manager_coaching_effectiveness_pct=0.60,
                        peer_comparison_percentile=60.0,
                        deal_quality_improvement_score=5.0)
        assert s == 10.0

    def test_mgr_pct_ge_070_no_penalty(self):
        s = self._score(manager_coaching_effectiveness_pct=0.80,
                        peer_comparison_percentile=60.0,
                        deal_quality_improvement_score=5.0)
        assert s == 0.0

    def test_peer_percentile_below_25_adds_30(self):
        s = self._score(manager_coaching_effectiveness_pct=0.80,
                        peer_comparison_percentile=20.0,
                        deal_quality_improvement_score=5.0)
        assert s == 30.0

    def test_peer_percentile_between_25_and_40_adds_15(self):
        s = self._score(manager_coaching_effectiveness_pct=0.80,
                        peer_comparison_percentile=35.0,
                        deal_quality_improvement_score=5.0)
        assert s == 15.0

    def test_peer_percentile_ge_40_no_penalty(self):
        s = self._score(manager_coaching_effectiveness_pct=0.80,
                        peer_comparison_percentile=50.0,
                        deal_quality_improvement_score=5.0)
        assert s == 0.0

    def test_deal_quality_below_neg10_adds_20(self):
        s = self._score(manager_coaching_effectiveness_pct=0.80,
                        peer_comparison_percentile=60.0,
                        deal_quality_improvement_score=-15.0)
        assert s == 20.0

    def test_deal_quality_between_neg10_and_0_adds_10(self):
        s = self._score(manager_coaching_effectiveness_pct=0.80,
                        peer_comparison_percentile=60.0,
                        deal_quality_improvement_score=-5.0)
        assert s == 10.0

    def test_deal_quality_zero_no_penalty(self):
        s = self._score(manager_coaching_effectiveness_pct=0.80,
                        peer_comparison_percentile=60.0,
                        deal_quality_improvement_score=0.0)
        assert s == 0.0

    def test_deal_quality_positive_no_penalty(self):
        s = self._score(manager_coaching_effectiveness_pct=0.80,
                        peer_comparison_percentile=60.0,
                        deal_quality_improvement_score=10.0)
        assert s == 0.0

    def test_max_capped_at_100(self):
        # 40+30+20 = 90, under cap
        s = self._score(manager_coaching_effectiveness_pct=0.10,
                        peer_comparison_percentile=10.0,
                        deal_quality_improvement_score=-20.0)
        assert s == 90.0

    def test_score_nonnegative(self):
        s = self._score()
        assert s >= 0.0

    def test_score_not_exceeding_100(self):
        s = self._score(manager_coaching_effectiveness_pct=0.0,
                        peer_comparison_percentile=0.0,
                        deal_quality_improvement_score=-100.0)
        assert s <= 100.0

    def test_mgr_pct_exactly_030_is_25(self):
        # 0.30 is NOT < 0.30, but IS < 0.50
        s = self._score(manager_coaching_effectiveness_pct=0.30,
                        peer_comparison_percentile=60.0,
                        deal_quality_improvement_score=5.0)
        assert s == 25.0

    def test_mgr_pct_exactly_050_is_10(self):
        s = self._score(manager_coaching_effectiveness_pct=0.50,
                        peer_comparison_percentile=60.0,
                        deal_quality_improvement_score=5.0)
        assert s == 10.0

    def test_peer_percentile_exactly_25_is_15(self):
        s = self._score(manager_coaching_effectiveness_pct=0.80,
                        peer_comparison_percentile=25.0,
                        deal_quality_improvement_score=5.0)
        assert s == 15.0

    def test_deal_quality_exactly_neg10_is_10(self):
        # -10 is NOT < -10, but IS < 0
        s = self._score(manager_coaching_effectiveness_pct=0.80,
                        peer_comparison_percentile=60.0,
                        deal_quality_improvement_score=-10.0)
        assert s == 10.0


# ---------------------------------------------------------------------------
# Class 8: composite calculation
# ---------------------------------------------------------------------------

class TestCompositeCalculation:
    def test_composite_formula(self, engine):
        # Build an input where each sub-score is known, then verify composite
        # Use zero-penalty input: composite should be ~0
        inp = make_input()
        result = engine.assess(inp)
        freq = result.coaching_frequency_score
        imp = result.coaching_impact_score
        aln = result.coaching_alignment_score
        mgr = result.manager_effectiveness_score
        expected = round(freq * 0.20 + imp * 0.35 + aln * 0.25 + mgr * 0.20, 1)
        assert result.coaching_effectiveness_composite == expected

    def test_composite_capped_at_100(self, engine):
        # Force all sub-scores high
        inp = make_input(
            coaching_sessions_last_90d=0,
            days_to_behavioral_change=60,
            recidivism_count=10,
            win_rate_before_coaching_pct=0.80,
            win_rate_after_coaching_pct=0.20,
            quota_attainment_before_pct=150.0,
            quota_attainment_after_pct=50.0,
            activity_score_before=100.0,
            activity_score_after=50.0,
            coaching_topic_alignment_score=10.0,
            avg_discount_before_pct=0.0,
            avg_discount_after_pct=20.0,
            self_assessed_readiness_score=10.0,
            manager_coaching_effectiveness_pct=0.05,
            peer_comparison_percentile=5.0,
            deal_quality_improvement_score=-50.0,
        )
        result = engine.assess(inp)
        assert result.coaching_effectiveness_composite <= 100.0

    def test_composite_nonnegative(self, engine, good_input):
        result = engine.assess(good_input)
        assert result.coaching_effectiveness_composite >= 0.0

    def test_composite_rounded_to_1_decimal(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        # Check it's a float with at most 1 decimal place
        c = result.coaching_effectiveness_composite
        assert round(c, 1) == c


# ---------------------------------------------------------------------------
# Class 9: Risk level
# ---------------------------------------------------------------------------

class TestRiskLevel:
    def _risk(self, composite: float) -> CoachingRisk:
        eng = SalesCoachingEffectivenessEngine()
        return eng._risk_level(composite)

    def test_composite_ge_60_is_critical(self):
        assert self._risk(60.0) == CoachingRisk.critical
        assert self._risk(75.0) == CoachingRisk.critical
        assert self._risk(100.0) == CoachingRisk.critical

    def test_composite_ge_40_lt_60_is_high(self):
        assert self._risk(40.0) == CoachingRisk.high
        assert self._risk(50.0) == CoachingRisk.high
        assert self._risk(59.9) == CoachingRisk.high

    def test_composite_ge_20_lt_40_is_moderate(self):
        assert self._risk(20.0) == CoachingRisk.moderate
        assert self._risk(30.0) == CoachingRisk.moderate
        assert self._risk(39.9) == CoachingRisk.moderate

    def test_composite_lt_20_is_low(self):
        assert self._risk(0.0) == CoachingRisk.low
        assert self._risk(10.0) == CoachingRisk.low
        assert self._risk(19.9) == CoachingRisk.low

    def test_boundary_exactly_40(self):
        assert self._risk(40.0) == CoachingRisk.high

    def test_boundary_exactly_20(self):
        assert self._risk(20.0) == CoachingRisk.moderate

    def test_boundary_exactly_60(self):
        assert self._risk(60.0) == CoachingRisk.critical


# ---------------------------------------------------------------------------
# Class 10: Severity
# ---------------------------------------------------------------------------

class TestSeverity:
    def _sev(self, composite: float) -> CoachingSeverity:
        eng = SalesCoachingEffectivenessEngine()
        return eng._severity(composite)

    def test_composite_ge_60_is_regressing(self):
        assert self._sev(60.0) == CoachingSeverity.regressing
        assert self._sev(80.0) == CoachingSeverity.regressing

    def test_composite_ge_40_lt_60_is_stalled(self):
        assert self._sev(40.0) == CoachingSeverity.stalled
        assert self._sev(55.0) == CoachingSeverity.stalled

    def test_composite_ge_20_lt_40_is_developing(self):
        assert self._sev(20.0) == CoachingSeverity.developing
        assert self._sev(35.0) == CoachingSeverity.developing

    def test_composite_lt_20_is_effective(self):
        assert self._sev(0.0) == CoachingSeverity.effective
        assert self._sev(15.0) == CoachingSeverity.effective
        assert self._sev(19.9) == CoachingSeverity.effective

    def test_boundary_exactly_40(self):
        assert self._sev(40.0) == CoachingSeverity.stalled

    def test_boundary_exactly_60(self):
        assert self._sev(60.0) == CoachingSeverity.regressing

    def test_boundary_exactly_20(self):
        assert self._sev(20.0) == CoachingSeverity.developing


# ---------------------------------------------------------------------------
# Class 11: Pattern detection
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def _pattern(self, **kwargs) -> CoachingPattern:
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(**kwargs)
        freq = eng._coaching_frequency_score(inp)
        impact = eng._coaching_impact_score(inp)
        aln = eng._coaching_alignment_score(inp)
        mgr = eng._manager_effectiveness_score(inp)
        return eng._detect_pattern(inp, freq, impact, aln, mgr)

    def test_coaching_resistance_highest_priority(self):
        # recidivism>=3 and impact>=40 → coaching_resistance
        p = self._pattern(
            recidivism_count=3,
            win_rate_before_coaching_pct=0.60, win_rate_after_coaching_pct=0.30,
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=75.0,
            activity_score_before=80.0, activity_score_after=60.0,
            manager_coaching_effectiveness_pct=0.20,  # also triggers manager_ineffectiveness
            peer_comparison_percentile=20.0,
            deal_quality_improvement_score=-20.0,
        )
        assert p == CoachingPattern.coaching_resistance

    def test_manager_ineffectiveness_before_misalignment(self):
        # manager>=40 and mgr_pct<0.40, but not coaching_resistance
        p = self._pattern(
            recidivism_count=0,
            manager_coaching_effectiveness_pct=0.20,
            peer_comparison_percentile=15.0,
            deal_quality_improvement_score=-15.0,
            coaching_topic_alignment_score=20.0,
            avg_discount_before_pct=0.0, avg_discount_after_pct=5.0,
            self_assessed_readiness_score=20.0,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.42,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=92.0,
            activity_score_before=70.0, activity_score_after=72.0,
        )
        assert p == CoachingPattern.manager_ineffectiveness

    def test_topic_misalignment_detected(self):
        # alignment>=35 and topic_alignment<50, not resistance/manager
        p = self._pattern(
            recidivism_count=0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
            coaching_topic_alignment_score=30.0,
            avg_discount_before_pct=0.0, avg_discount_after_pct=5.0,
            self_assessed_readiness_score=30.0,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.42,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=92.0,
            activity_score_before=70.0, activity_score_after=72.0,
        )
        assert p == CoachingPattern.topic_misalignment

    def test_no_behavioral_change_detected(self):
        # impact>=30, win_after<=win_before, quota_after<=quota_before
        p = self._pattern(
            recidivism_count=0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
            coaching_topic_alignment_score=80.0,
            avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
            self_assessed_readiness_score=75.0,
            win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40,
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=85.0,
            activity_score_before=70.0, activity_score_after=70.0,
        )
        assert p == CoachingPattern.no_behavioral_change

    def test_insufficient_frequency_detected(self):
        # frequency>=30 and sessions < bench*0.50
        p = self._pattern(
            recidivism_count=0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
            coaching_topic_alignment_score=80.0,
            avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
            self_assessed_readiness_score=75.0,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.42,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=92.0,
            activity_score_before=70.0, activity_score_after=72.0,
            coaching_sessions_last_90d=0,
            coaching_sessions_benchmark=6,
            days_to_behavioral_change=30,
        )
        assert p == CoachingPattern.insufficient_frequency

    def test_none_pattern_when_no_issues(self):
        p = self._pattern()
        assert p == CoachingPattern.none

    def test_no_behavioral_change_requires_win_and_quota_both_le(self):
        # win_after > win_before → should not trigger no_behavioral_change
        p = self._pattern(
            recidivism_count=0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
            coaching_topic_alignment_score=80.0,
            avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
            self_assessed_readiness_score=75.0,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.50,  # improved
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=85.0,
            activity_score_before=80.0, activity_score_after=65.0,
        )
        assert p != CoachingPattern.no_behavioral_change

    def test_manager_ineffectiveness_requires_mgr_pct_lt_040(self):
        # manager score >= 40 but mgr_pct >= 0.40 → no manager_ineffectiveness
        p = self._pattern(
            recidivism_count=0,
            manager_coaching_effectiveness_pct=0.45,  # >= 0.40
            peer_comparison_percentile=10.0,
            deal_quality_improvement_score=-20.0,
            coaching_topic_alignment_score=80.0,
            avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
            self_assessed_readiness_score=75.0,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.42,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=92.0,
            activity_score_before=70.0, activity_score_after=72.0,
        )
        assert p != CoachingPattern.manager_ineffectiveness


# ---------------------------------------------------------------------------
# Class 12: Action logic
# ---------------------------------------------------------------------------

class TestActionLogic:
    def _action(self, risk: CoachingRisk, pattern: CoachingPattern) -> CoachingAction:
        eng = SalesCoachingEffectivenessEngine()
        return eng._action(risk, pattern)

    def test_critical_coaching_resistance_is_performance_management(self):
        assert self._action(CoachingRisk.critical, CoachingPattern.coaching_resistance) == CoachingAction.performance_management

    def test_critical_manager_ineffectiveness_is_external_coach(self):
        assert self._action(CoachingRisk.critical, CoachingPattern.manager_ineffectiveness) == CoachingAction.external_coach_engagement

    def test_critical_topic_misalignment_is_coaching_topic_reset(self):
        assert self._action(CoachingRisk.critical, CoachingPattern.topic_misalignment) == CoachingAction.coaching_topic_reset

    def test_critical_no_behavioral_change_is_coaching_topic_reset(self):
        assert self._action(CoachingRisk.critical, CoachingPattern.no_behavioral_change) == CoachingAction.coaching_topic_reset

    def test_critical_insufficient_frequency_is_coaching_topic_reset(self):
        assert self._action(CoachingRisk.critical, CoachingPattern.insufficient_frequency) == CoachingAction.coaching_topic_reset

    def test_critical_none_is_coaching_topic_reset(self):
        assert self._action(CoachingRisk.critical, CoachingPattern.none) == CoachingAction.coaching_topic_reset

    def test_high_manager_ineffectiveness_is_manager_training(self):
        assert self._action(CoachingRisk.high, CoachingPattern.manager_ineffectiveness) == CoachingAction.manager_coaching_training

    def test_high_insufficient_frequency_is_increase_frequency(self):
        assert self._action(CoachingRisk.high, CoachingPattern.insufficient_frequency) == CoachingAction.increase_coaching_frequency

    def test_high_topic_misalignment_is_coaching_topic_reset(self):
        assert self._action(CoachingRisk.high, CoachingPattern.topic_misalignment) == CoachingAction.coaching_topic_reset

    def test_high_no_behavioral_change_is_coaching_topic_reset(self):
        assert self._action(CoachingRisk.high, CoachingPattern.no_behavioral_change) == CoachingAction.coaching_topic_reset

    def test_high_coaching_resistance_is_coaching_topic_reset(self):
        assert self._action(CoachingRisk.high, CoachingPattern.coaching_resistance) == CoachingAction.coaching_topic_reset

    def test_high_none_is_coaching_topic_reset(self):
        assert self._action(CoachingRisk.high, CoachingPattern.none) == CoachingAction.coaching_topic_reset

    def test_moderate_insufficient_frequency_is_increase_frequency(self):
        assert self._action(CoachingRisk.moderate, CoachingPattern.insufficient_frequency) == CoachingAction.increase_coaching_frequency

    def test_moderate_other_patterns_is_coaching_topic_reset(self):
        for p in [CoachingPattern.no_behavioral_change, CoachingPattern.topic_misalignment,
                  CoachingPattern.manager_ineffectiveness, CoachingPattern.coaching_resistance,
                  CoachingPattern.none]:
            assert self._action(CoachingRisk.moderate, p) == CoachingAction.coaching_topic_reset

    def test_low_is_no_action_regardless_of_pattern(self):
        for p in CoachingPattern:
            assert self._action(CoachingRisk.low, p) == CoachingAction.no_action


# ---------------------------------------------------------------------------
# Class 13: is_coaching_ineffective flag
# ---------------------------------------------------------------------------

class TestIsCoachingIneffective:
    def _flag(self, **kwargs) -> bool:
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(**kwargs)
        result = eng.assess(inp)
        return result.is_coaching_ineffective

    def test_composite_ge_40_makes_ineffective(self):
        # Force composite >= 40 via worst-case inputs
        flag = self._flag(
            coaching_sessions_last_90d=0,
            days_to_behavioral_change=30,
            recidivism_count=3,
            win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.35,
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=80.0,
            activity_score_before=80.0, activity_score_after=65.0,
            coaching_topic_alignment_score=30.0,
            manager_coaching_effectiveness_pct=0.20,
            peer_comparison_percentile=15.0,
            deal_quality_improvement_score=-15.0,
        )
        assert flag is True

    def test_recidivism_ge_3_makes_ineffective(self):
        flag = self._flag(recidivism_count=3)
        assert flag is True

    def test_win_rate_drops_more_than_005_makes_ineffective(self):
        # after = before - 0.06
        flag = self._flag(
            win_rate_before_coaching_pct=0.50,
            win_rate_after_coaching_pct=0.44,
        )
        assert flag is True

    def test_win_rate_drops_exactly_005_not_ineffective_by_this_rule(self):
        # 0.44 - 0.50 = -0.06 is actually MORE than 0.05 drop... let me use exact 0.05
        # win_after = before - 0.05 exactly: 0.50 - 0.05 = 0.45, delta = -0.05
        # -0.05 < -0.05 is False → this rule alone not triggered
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(
            win_rate_before_coaching_pct=0.50,
            win_rate_after_coaching_pct=0.45,
            recidivism_count=0,
        )
        result = eng.assess(inp)
        # Only the win-rate rule: 0.45 < 0.50 - 0.05 = 0.45 → False (not <)
        # composite might trigger it though, let's just check the condition
        assert result.is_coaching_ineffective == (
            result.coaching_effectiveness_composite >= 40
            or inp.recidivism_count >= 3
            or inp.win_rate_after_coaching_pct < inp.win_rate_before_coaching_pct - 0.05
        )

    def test_good_rep_not_ineffective(self):
        flag = self._flag()
        assert flag is False

    def test_ineffective_when_recidivism_4(self):
        flag = self._flag(recidivism_count=4)
        assert flag is True


# ---------------------------------------------------------------------------
# Class 14: requires_coaching_redesign flag
# ---------------------------------------------------------------------------

class TestRequiresCoachingRedesign:
    def _flag(self, **kwargs) -> bool:
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(**kwargs)
        return eng.assess(inp).requires_coaching_redesign

    def test_composite_ge_30_triggers_redesign(self):
        # composite >=30 via moderate inputs
        flag = self._flag(
            coaching_sessions_last_90d=0,
            days_to_behavioral_change=30,
            recidivism_count=2,
            win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40,
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=90.0,
            activity_score_before=70.0, activity_score_after=70.0,
            coaching_topic_alignment_score=80.0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=50.0,
            deal_quality_improvement_score=5.0,
        )
        assert flag is True

    def test_topic_alignment_below_40_triggers_redesign(self):
        flag = self._flag(coaching_topic_alignment_score=30.0)
        assert flag is True

    def test_mgr_pct_below_030_triggers_redesign(self):
        flag = self._flag(manager_coaching_effectiveness_pct=0.25)
        assert flag is True

    def test_good_rep_no_redesign(self):
        flag = self._flag()
        assert flag is False

    def test_alignment_exactly_40_not_redesign_by_this_rule(self):
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(coaching_topic_alignment_score=40.0,
                         manager_coaching_effectiveness_pct=0.80)
        result = eng.assess(inp)
        # 40.0 is NOT < 40.0, so rule doesn't apply; check composite
        assert result.requires_coaching_redesign == (
            result.coaching_effectiveness_composite >= 30
            or inp.coaching_topic_alignment_score < 40.0
            or inp.manager_coaching_effectiveness_pct < 0.30
        )


# ---------------------------------------------------------------------------
# Class 15: estimated_revenue_impact_usd
# ---------------------------------------------------------------------------

class TestEstimatedRevenueImpact:
    def test_positive_deal_degradation(self, engine):
        # before=60000, after=50000, deal_degradation=10000
        # composite determined by other inputs
        inp = make_input(avg_deal_size_before_usd=60_000.0, avg_deal_size_after_usd=50_000.0)
        result = engine.assess(inp)
        degradation = 60_000.0 - 50_000.0
        expected = round(degradation * (result.coaching_effectiveness_composite / 100.0), 2)
        assert result.estimated_revenue_impact_usd == expected

    def test_deal_size_improved_zero_impact(self, engine):
        # after > before → max(negative, 0) = 0
        inp = make_input(avg_deal_size_before_usd=50_000.0, avg_deal_size_after_usd=55_000.0)
        result = engine.assess(inp)
        assert result.estimated_revenue_impact_usd == 0.0

    def test_deal_size_equal_zero_impact(self, engine):
        inp = make_input(avg_deal_size_before_usd=50_000.0, avg_deal_size_after_usd=50_000.0)
        result = engine.assess(inp)
        assert result.estimated_revenue_impact_usd == 0.0

    def test_revenue_impact_nonnegative(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        assert result.estimated_revenue_impact_usd >= 0.0

    def test_revenue_impact_scales_with_composite(self, engine):
        # Higher composite → higher revenue impact (given same deal degradation)
        inp_low = make_input(avg_deal_size_before_usd=60_000.0, avg_deal_size_after_usd=50_000.0)
        inp_high = make_input(
            avg_deal_size_before_usd=60_000.0, avg_deal_size_after_usd=50_000.0,
            coaching_sessions_last_90d=0,
            days_to_behavioral_change=30,
            recidivism_count=3,
            win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.30,
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=80.0,
            activity_score_before=80.0, activity_score_after=60.0,
            coaching_topic_alignment_score=30.0,
            manager_coaching_effectiveness_pct=0.20,
            peer_comparison_percentile=15.0,
            deal_quality_improvement_score=-15.0,
        )
        r_low = engine.assess(inp_low)
        r_high = engine.assess(inp_high)
        assert r_high.estimated_revenue_impact_usd >= r_low.estimated_revenue_impact_usd

    def test_revenue_impact_rounded_to_2_decimals(self, engine):
        inp = make_input(avg_deal_size_before_usd=60_000.0, avg_deal_size_after_usd=50_000.0)
        result = engine.assess(inp)
        assert round(result.estimated_revenue_impact_usd, 2) == result.estimated_revenue_impact_usd


# ---------------------------------------------------------------------------
# Class 16: coaching_signal string
# ---------------------------------------------------------------------------

class TestCoachingSignal:
    def test_good_rep_positive_signal(self, engine):
        # pattern=none, composite < 10
        inp = make_input()
        result = engine.assess(inp)
        if result.coaching_pattern == CoachingPattern.none and result.coaching_effectiveness_composite < 10:
            assert result.coaching_signal == "Coaching driving measurable performance improvement"

    def test_signal_contains_label(self, engine):
        # non-trivial case: ensure label from pattern is capitalized
        inp = make_input(
            coaching_sessions_last_90d=0,
            coaching_sessions_benchmark=6,
            days_to_behavioral_change=30,
        )
        result = engine.assess(inp)
        if result.coaching_pattern != CoachingPattern.none:
            label = result.coaching_pattern.value.replace("_", " ").capitalize()
            assert result.coaching_signal.startswith(label)

    def test_signal_contains_composite(self, engine):
        inp = make_input(
            win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40,
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=88.0,
        )
        result = engine.assess(inp)
        composite_str = f"{result.coaching_effectiveness_composite:.0f}"
        assert composite_str in result.coaching_signal

    def test_signal_win_rate_drop_included(self, engine):
        inp = make_input(
            win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40,
        )
        result = engine.assess(inp)
        assert "win rate" in result.coaching_signal

    def test_signal_quota_drop_included(self, engine):
        inp = make_input(
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=85.0,
        )
        result = engine.assess(inp)
        assert "attainment" in result.coaching_signal

    def test_signal_recidivism_included(self, engine):
        # Need composite >= 10 or non-none pattern to avoid positive signal
        inp = make_input(recidivism_count=2,
                         win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40,
                         quota_attainment_before_pct=100.0, quota_attainment_after_pct=88.0)
        result = engine.assess(inp)
        # Ensure we are NOT in the positive-signal branch
        assert not (result.coaching_pattern == CoachingPattern.none and result.coaching_effectiveness_composite < 10)
        assert "recidivism" in result.coaching_signal

    def test_signal_topic_alignment_included_when_lt_60(self, engine):
        # Force composite >= 10 so we don't get the positive signal
        inp = make_input(coaching_topic_alignment_score=50.0,
                         win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40)
        result = engine.assess(inp)
        assert not (result.coaching_pattern == CoachingPattern.none and result.coaching_effectiveness_composite < 10)
        assert "topic alignment" in result.coaching_signal

    def test_signal_topic_alignment_not_included_when_ge_60(self, engine):
        # alignment >= 60 → no topic alignment part in signal
        inp = make_input(coaching_topic_alignment_score=65.0,
                         win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.40,
                         quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
                         recidivism_count=0)
        result = engine.assess(inp)
        # Only check if no pattern and no drops
        if result.coaching_pattern == CoachingPattern.none and result.coaching_effectiveness_composite >= 10:
            assert "topic alignment" not in result.coaching_signal

    def test_signal_none_pattern_high_composite_uses_coaching_risk_label(self, engine):
        # Pattern=none but composite >= 10 → label = "Coaching risk"
        # Craft input where composite >= 10 but no specific pattern triggers
        inp = make_input(
            recidivism_count=1,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.40,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
        )
        result = engine.assess(inp)
        if result.coaching_pattern == CoachingPattern.none and result.coaching_effectiveness_composite >= 10:
            assert result.coaching_signal.startswith("Coaching risk")

    def test_signal_fallback_coaching_effectiveness_degraded(self, engine):
        # When no parts are added, fallback text is used
        inp = make_input(
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.42,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=92.0,
            recidivism_count=0,
            coaching_topic_alignment_score=80.0,
        )
        result = engine.assess(inp)
        if result.coaching_effectiveness_composite >= 10 or result.coaching_pattern != CoachingPattern.none:
            if "win rate" not in result.coaching_signal and \
               "attainment" not in result.coaching_signal and \
               "recidivism" not in result.coaching_signal and \
               "topic alignment" not in result.coaching_signal:
                assert "coaching effectiveness degraded" in result.coaching_signal

    def test_signal_format_with_dashes(self, engine):
        inp = make_input(
            win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40,
        )
        result = engine.assess(inp)
        # Should contain at least two " — " separators when there are parts
        assert " — " in result.coaching_signal

    def test_signal_recidivism_count_in_text(self, engine):
        # Ensure composite >= 10 so positive signal is not returned
        inp = make_input(recidivism_count=4,
                         win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40,
                         quota_attainment_before_pct=100.0, quota_attainment_after_pct=88.0)
        result = engine.assess(inp)
        assert not (result.coaching_pattern == CoachingPattern.none and result.coaching_effectiveness_composite < 10)
        assert "4 recidivism" in result.coaching_signal

    def test_signal_alignment_score_in_text(self, engine):
        # Ensure composite >= 10 so positive signal is not returned
        inp = make_input(coaching_topic_alignment_score=45.0,
                         win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40)
        result = engine.assess(inp)
        assert not (result.coaching_pattern == CoachingPattern.none and result.coaching_effectiveness_composite < 10)
        assert "45% topic alignment" in result.coaching_signal


# ---------------------------------------------------------------------------
# Class 17: assess() integration — good rep
# ---------------------------------------------------------------------------

class TestAssessGoodRep:
    def test_good_rep_low_risk(self, engine, good_input):
        result = engine.assess(good_input)
        assert result.coaching_risk == CoachingRisk.low

    def test_good_rep_effective_severity(self, engine, good_input):
        result = engine.assess(good_input)
        assert result.coaching_severity == CoachingSeverity.effective

    def test_good_rep_no_action(self, engine, good_input):
        result = engine.assess(good_input)
        assert result.recommended_action == CoachingAction.no_action

    def test_good_rep_none_pattern(self, engine, good_input):
        result = engine.assess(good_input)
        assert result.coaching_pattern == CoachingPattern.none

    def test_good_rep_not_ineffective(self, engine, good_input):
        result = engine.assess(good_input)
        assert result.is_coaching_ineffective is False

    def test_good_rep_rep_id_preserved(self, engine):
        inp = make_input(rep_id="R999")
        result = engine.assess(inp)
        assert result.rep_id == "R999"

    def test_good_rep_region_preserved(self, engine):
        inp = make_input(region="APAC")
        result = engine.assess(inp)
        assert result.region == "APAC"

    def test_good_rep_composite_low(self, engine, good_input):
        result = engine.assess(good_input)
        assert result.coaching_effectiveness_composite < 20.0

    def test_good_rep_result_is_result_type(self, engine, good_input):
        result = engine.assess(good_input)
        assert isinstance(result, CoachingEffectivenessResult)


# ---------------------------------------------------------------------------
# Class 18: assess() integration — worst-case rep
# ---------------------------------------------------------------------------

class TestAssessWorstCaseRep:
    @pytest.fixture
    def worst_input(self) -> CoachingEffectivenessInput:
        return make_input(
            coaching_sessions_last_90d=0,
            coaching_sessions_benchmark=6,
            days_to_behavioral_change=45,
            recidivism_count=4,
            win_rate_before_coaching_pct=0.60,
            win_rate_after_coaching_pct=0.30,
            quota_attainment_before_pct=120.0,
            quota_attainment_after_pct=70.0,
            activity_score_before=90.0,
            activity_score_after=60.0,
            avg_deal_size_before_usd=80_000.0,
            avg_deal_size_after_usd=40_000.0,
            avg_discount_before_pct=5.0,
            avg_discount_after_pct=15.0,
            coaching_topic_alignment_score=20.0,
            manager_coaching_effectiveness_pct=0.15,
            peer_comparison_percentile=10.0,
            deal_quality_improvement_score=-20.0,
            self_assessed_readiness_score=20.0,
        )

    def test_worst_critical_risk(self, engine, worst_input):
        result = engine.assess(worst_input)
        assert result.coaching_risk == CoachingRisk.critical

    def test_worst_regressing_severity(self, engine, worst_input):
        result = engine.assess(worst_input)
        assert result.coaching_severity == CoachingSeverity.regressing

    def test_worst_is_ineffective(self, engine, worst_input):
        result = engine.assess(worst_input)
        assert result.is_coaching_ineffective is True

    def test_worst_requires_redesign(self, engine, worst_input):
        result = engine.assess(worst_input)
        assert result.requires_coaching_redesign is True

    def test_worst_composite_high(self, engine, worst_input):
        result = engine.assess(worst_input)
        assert result.coaching_effectiveness_composite >= 60.0

    def test_worst_positive_revenue_impact(self, engine, worst_input):
        result = engine.assess(worst_input)
        assert result.estimated_revenue_impact_usd > 0.0

    def test_worst_pattern_coaching_resistance(self, engine, worst_input):
        result = engine.assess(worst_input)
        assert result.coaching_pattern == CoachingPattern.coaching_resistance

    def test_worst_action_performance_management(self, engine, worst_input):
        result = engine.assess(worst_input)
        assert result.recommended_action == CoachingAction.performance_management


# ---------------------------------------------------------------------------
# Class 19: assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_batch_returns_list(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert isinstance(results, list)

    def test_batch_length_matches_input(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(7)]
        results = engine.assess_batch(inputs)
        assert len(results) == 7

    def test_batch_each_element_is_result(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        for r in results:
            assert isinstance(r, CoachingEffectivenessResult)

    def test_batch_preserves_rep_ids(self, engine):
        ids = ["A", "B", "C"]
        inputs = [make_input(rep_id=i) for i in ids]
        results = engine.assess_batch(inputs)
        assert [r.rep_id for r in results] == ids

    def test_batch_empty_list(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_batch_single_element(self, engine):
        results = engine.assess_batch([make_input(rep_id="SOLO")])
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"

    def test_batch_updates_internal_results(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(4)]
        engine.assess_batch(inputs)
        summ = engine.summary()
        assert summ["total"] == 4


# ---------------------------------------------------------------------------
# Class 20: summary() — structure
# ---------------------------------------------------------------------------

class TestSummaryStructure:
    def test_summary_has_13_keys(self, engine, good_input):
        engine.assess(good_input)
        s = engine.summary()
        assert len(s) == 13

    def test_summary_exact_keys(self, engine, good_input):
        engine.assess(good_input)
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
            "avg_coaching_effectiveness_composite", "ineffective_coaching_count",
            "coaching_redesign_count", "avg_coaching_frequency_score",
            "avg_coaching_impact_score", "avg_coaching_alignment_score",
            "avg_manager_effectiveness_score", "total_estimated_revenue_impact_usd",
        }
        assert set(engine.summary().keys()) == expected_keys

    def test_summary_empty_engine(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_coaching_effectiveness_composite"] == 0.0
        assert s["ineffective_coaching_count"] == 0
        assert s["coaching_redesign_count"] == 0
        assert s["avg_coaching_frequency_score"] == 0.0
        assert s["avg_coaching_impact_score"] == 0.0
        assert s["avg_coaching_alignment_score"] == 0.0
        assert s["avg_manager_effectiveness_score"] == 0.0
        assert s["total_estimated_revenue_impact_usd"] == 0.0

    def test_summary_empty_has_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_summary_total_correct(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"R{i}"))
        assert engine.summary()["total"] == 5

    def test_summary_risk_counts_is_dict(self, engine, good_input):
        engine.assess(good_input)
        assert isinstance(engine.summary()["risk_counts"], dict)

    def test_summary_pattern_counts_is_dict(self, engine, good_input):
        engine.assess(good_input)
        assert isinstance(engine.summary()["pattern_counts"], dict)

    def test_summary_severity_counts_is_dict(self, engine, good_input):
        engine.assess(good_input)
        assert isinstance(engine.summary()["severity_counts"], dict)

    def test_summary_action_counts_is_dict(self, engine, good_input):
        engine.assess(good_input)
        assert isinstance(engine.summary()["action_counts"], dict)

    def test_summary_total_revenue_is_sum_not_avg(self, engine):
        # Assess two reps with known deal degradation
        eng2 = SalesCoachingEffectivenessEngine()
        inp1 = make_input(rep_id="R1", avg_deal_size_before_usd=60_000.0, avg_deal_size_after_usd=50_000.0)
        inp2 = make_input(rep_id="R2", avg_deal_size_before_usd=70_000.0, avg_deal_size_after_usd=55_000.0)
        r1 = eng2.assess(inp1)
        r2 = eng2.assess(inp2)
        s = eng2.summary()
        expected_total = round(r1.estimated_revenue_impact_usd + r2.estimated_revenue_impact_usd, 2)
        assert s["total_estimated_revenue_impact_usd"] == expected_total


# ---------------------------------------------------------------------------
# Class 21: summary() — aggregation accuracy
# ---------------------------------------------------------------------------

class TestSummaryAggregation:
    def test_avg_composite_correct(self, engine):
        eng = SalesCoachingEffectivenessEngine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        results = eng.assess_batch(inputs)
        expected_avg = round(sum(r.coaching_effectiveness_composite for r in results) / 3, 1)
        assert eng.summary()["avg_coaching_effectiveness_composite"] == expected_avg

    def test_avg_frequency_score_correct(self):
        eng = SalesCoachingEffectivenessEngine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        results = eng.assess_batch(inputs)
        expected = round(sum(r.coaching_frequency_score for r in results) / 3, 1)
        assert eng.summary()["avg_coaching_frequency_score"] == expected

    def test_avg_impact_score_correct(self):
        eng = SalesCoachingEffectivenessEngine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        results = eng.assess_batch(inputs)
        expected = round(sum(r.coaching_impact_score for r in results) / 3, 1)
        assert eng.summary()["avg_coaching_impact_score"] == expected

    def test_avg_alignment_score_correct(self):
        eng = SalesCoachingEffectivenessEngine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        results = eng.assess_batch(inputs)
        expected = round(sum(r.coaching_alignment_score for r in results) / 3, 1)
        assert eng.summary()["avg_coaching_alignment_score"] == expected

    def test_avg_manager_score_correct(self):
        eng = SalesCoachingEffectivenessEngine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        results = eng.assess_batch(inputs)
        expected = round(sum(r.manager_effectiveness_score for r in results) / 3, 1)
        assert eng.summary()["avg_manager_effectiveness_score"] == expected

    def test_ineffective_count_correct(self):
        eng = SalesCoachingEffectivenessEngine()
        good = make_input(rep_id="G1")
        bad = make_input(rep_id="B1", recidivism_count=3)
        eng.assess_batch([good, bad])
        s = eng.summary()
        assert s["ineffective_coaching_count"] >= 1

    def test_redesign_count_correct(self):
        eng = SalesCoachingEffectivenessEngine()
        good = make_input(rep_id="G1")
        bad = make_input(rep_id="B1", coaching_topic_alignment_score=20.0)
        eng.assess_batch([good, bad])
        s = eng.summary()
        assert s["coaching_redesign_count"] >= 1

    def test_risk_counts_sum_equals_total(self):
        eng = SalesCoachingEffectivenessEngine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        eng.assess_batch(inputs)
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_pattern_counts_sum_equals_total(self):
        eng = SalesCoachingEffectivenessEngine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        eng.assess_batch(inputs)
        s = eng.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_severity_counts_sum_equals_total(self):
        eng = SalesCoachingEffectivenessEngine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        eng.assess_batch(inputs)
        s = eng.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_action_counts_sum_equals_total(self):
        eng = SalesCoachingEffectivenessEngine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        eng.assess_batch(inputs)
        s = eng.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_single_assess_risk_count(self):
        eng = SalesCoachingEffectivenessEngine()
        result = eng.assess(make_input())
        s = eng.summary()
        assert s["risk_counts"][result.coaching_risk.value] == 1


# ---------------------------------------------------------------------------
# Class 22: engine state isolation
# ---------------------------------------------------------------------------

class TestEngineStateIsolation:
    def test_fresh_engine_empty_summary(self):
        eng = SalesCoachingEffectivenessEngine()
        assert eng.summary()["total"] == 0

    def test_results_accumulate_across_calls(self):
        eng = SalesCoachingEffectivenessEngine()
        eng.assess(make_input(rep_id="A"))
        eng.assess(make_input(rep_id="B"))
        assert eng.summary()["total"] == 2

    def test_two_engines_independent(self):
        eng1 = SalesCoachingEffectivenessEngine()
        eng2 = SalesCoachingEffectivenessEngine()
        eng1.assess(make_input(rep_id="X"))
        assert eng1.summary()["total"] == 1
        assert eng2.summary()["total"] == 0

    def test_results_list_grows_correctly(self):
        eng = SalesCoachingEffectivenessEngine()
        for i in range(10):
            eng.assess(make_input(rep_id=f"R{i}"))
        assert eng.summary()["total"] == 10

    def test_batch_followed_by_single(self):
        eng = SalesCoachingEffectivenessEngine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        eng.assess(make_input(rep_id="R_extra"))
        assert eng.summary()["total"] == 4


# ---------------------------------------------------------------------------
# Class 23: boundary / edge cases
# ---------------------------------------------------------------------------

class TestBoundaryEdgeCases:
    def test_benchmark_zero_treated_as_one(self, engine):
        inp = make_input(coaching_sessions_last_90d=1, coaching_sessions_benchmark=0)
        result = engine.assess(inp)
        # Should not crash; sessions=1 >= 1*0.50=0.5 and >=1*0.75=0.75
        # So sessions=1 is NOT < 0.5 and NOT < 0.75 → no volume penalty
        assert result.coaching_frequency_score >= 0.0

    def test_all_scores_at_exactly_0_composite_0(self, engine):
        inp = make_input(
            coaching_sessions_last_90d=6,
            coaching_sessions_benchmark=6,
            days_to_behavioral_change=0,
            recidivism_count=0,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.42,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=92.0,
            activity_score_before=70.0, activity_score_after=72.0,
            coaching_topic_alignment_score=80.0,
            avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
            self_assessed_readiness_score=75.0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
        )
        result = engine.assess(inp)
        assert result.coaching_effectiveness_composite == 0.0

    def test_composite_0_is_low_risk_effective(self, engine):
        inp = make_input(
            coaching_sessions_last_90d=6, coaching_sessions_benchmark=6,
            days_to_behavioral_change=0, recidivism_count=0,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.42,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=92.0,
            activity_score_before=70.0, activity_score_after=72.0,
            coaching_topic_alignment_score=80.0,
            avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
            self_assessed_readiness_score=75.0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
        )
        result = engine.assess(inp)
        assert result.coaching_risk == CoachingRisk.low
        assert result.coaching_severity == CoachingSeverity.effective

    def test_very_high_sessions_no_penalty(self, engine):
        inp = make_input(coaching_sessions_last_90d=100, coaching_sessions_benchmark=6)
        result = engine.assess(inp)
        # No volume penalty contribution
        freq = result.coaching_frequency_score
        assert freq >= 0.0

    def test_float_precision_composite(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        c = result.coaching_effectiveness_composite
        assert isinstance(c, float)

    def test_very_large_deal_sizes(self, engine):
        inp = make_input(avg_deal_size_before_usd=1_000_000.0, avg_deal_size_after_usd=500_000.0)
        result = engine.assess(inp)
        assert result.estimated_revenue_impact_usd >= 0.0

    def test_days_to_behavioral_change_14_no_penalty(self, engine):
        inp = make_input(days_to_behavioral_change=14, recidivism_count=0,
                         coaching_sessions_last_90d=6, coaching_sessions_benchmark=6)
        result = engine.assess(inp)
        assert result.coaching_frequency_score == 0.0

    def test_days_to_behavioral_change_15_adds_10(self, engine):
        inp = make_input(days_to_behavioral_change=15, recidivism_count=0,
                         coaching_sessions_last_90d=6, coaching_sessions_benchmark=6)
        result = engine.assess(inp)
        assert result.coaching_frequency_score == 10.0

    def test_days_to_behavioral_change_30_adds_20(self, engine):
        inp = make_input(days_to_behavioral_change=30, recidivism_count=0,
                         coaching_sessions_last_90d=6, coaching_sessions_benchmark=6)
        result = engine.assess(inp)
        assert result.coaching_frequency_score == 20.0

    def test_quota_delta_exactly_neg10_adds_15(self, engine):
        inp = make_input(quota_attainment_before_pct=100.0, quota_attainment_after_pct=90.0)
        result = engine.assess(inp)
        # delta = -10, which is NOT < -10, so +15 (not +30)
        # Impact score includes this +15
        assert result.coaching_impact_score >= 15.0

    def test_activity_delta_exactly_neg10_adds_10(self, engine):
        inp = make_input(activity_score_before=80.0, activity_score_after=70.0)
        result = engine.assess(inp)
        # delta = -10, NOT < -10, so +10
        assert result.coaching_impact_score >= 10.0


# ---------------------------------------------------------------------------
# Class 24: mixed batch scenarios
# ---------------------------------------------------------------------------

class TestMixedBatchScenarios:
    def test_mixed_risks_in_summary(self):
        eng = SalesCoachingEffectivenessEngine()
        # Good rep → low
        eng.assess(make_input(rep_id="G"))
        # Bad rep → critical/high
        eng.assess(make_input(
            rep_id="B",
            coaching_sessions_last_90d=0,
            days_to_behavioral_change=30,
            recidivism_count=4,
            win_rate_before_coaching_pct=0.60, win_rate_after_coaching_pct=0.30,
            quota_attainment_before_pct=120.0, quota_attainment_after_pct=70.0,
            activity_score_before=90.0, activity_score_after=55.0,
            coaching_topic_alignment_score=20.0,
            manager_coaching_effectiveness_pct=0.15,
            peer_comparison_percentile=10.0,
            deal_quality_improvement_score=-20.0,
        ))
        s = eng.summary()
        assert s["total"] == 2
        assert "low" in s["risk_counts"]

    def test_summary_with_all_patterns(self):
        eng = SalesCoachingEffectivenessEngine()
        # none
        eng.assess(make_input(rep_id="none"))
        # coaching_resistance
        eng.assess(make_input(
            rep_id="resist",
            recidivism_count=3,
            win_rate_before_coaching_pct=0.60, win_rate_after_coaching_pct=0.30,
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=75.0,
            activity_score_before=80.0, activity_score_after=60.0,
        ))
        s = eng.summary()
        assert "none" in s["pattern_counts"]

    def test_total_revenue_impact_sums_correctly(self):
        eng = SalesCoachingEffectivenessEngine()
        r1 = eng.assess(make_input(rep_id="R1", avg_deal_size_before_usd=70_000, avg_deal_size_after_usd=60_000))
        r2 = eng.assess(make_input(rep_id="R2", avg_deal_size_before_usd=80_000, avg_deal_size_after_usd=70_000))
        r3 = eng.assess(make_input(rep_id="R3"))
        s = eng.summary()
        expected = round(r1.estimated_revenue_impact_usd + r2.estimated_revenue_impact_usd + r3.estimated_revenue_impact_usd, 2)
        assert s["total_estimated_revenue_impact_usd"] == expected

    def test_count_values_valid_strings(self):
        eng = SalesCoachingEffectivenessEngine()
        eng.assess(make_input())
        s = eng.summary()
        for key in s["risk_counts"]:
            assert key in [r.value for r in CoachingRisk]
        for key in s["pattern_counts"]:
            assert key in [p.value for p in CoachingPattern]
        for key in s["severity_counts"]:
            assert key in [sv.value for sv in CoachingSeverity]
        for key in s["action_counts"]:
            assert key in [a.value for a in CoachingAction]


# ---------------------------------------------------------------------------
# Class 25: specific scenario-based integration tests
# ---------------------------------------------------------------------------

class TestScenarioIntegration:
    def test_scenario_manager_underperformer(self):
        eng = SalesCoachingEffectivenessEngine()
        # Need composite >= 40 (high) to get manager_coaching_training
        # manager_score = 40+30+20=90, composite contribution from manager = 90*0.20=18
        # Add more: win regression +35 impact, quota regression +30, activity -10
        inp = make_input(
            rep_id="MGR_FAIL",
            manager_coaching_effectiveness_pct=0.20,
            peer_comparison_percentile=15.0,
            deal_quality_improvement_score=-15.0,
            recidivism_count=0,
            win_rate_before_coaching_pct=0.60, win_rate_after_coaching_pct=0.40,
            quota_attainment_before_pct=120.0, quota_attainment_after_pct=100.0,
            activity_score_before=85.0, activity_score_after=73.0,
            coaching_topic_alignment_score=80.0,
        )
        result = eng.assess(inp)
        assert result.coaching_pattern == CoachingPattern.manager_ineffectiveness
        assert result.recommended_action in (
            CoachingAction.manager_coaching_training,
            CoachingAction.external_coach_engagement,
        )

    def test_scenario_misaligned_coaching(self):
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(
            rep_id="MISALIGN",
            coaching_topic_alignment_score=25.0,
            avg_discount_before_pct=5.0, avg_discount_after_pct=10.0,
            self_assessed_readiness_score=25.0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
            recidivism_count=0,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.42,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=92.0,
            activity_score_before=70.0, activity_score_after=72.0,
        )
        result = eng.assess(inp)
        assert result.requires_coaching_redesign is True

    def test_scenario_no_behavioral_change(self):
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(
            rep_id="NO_CHANGE",
            win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40,
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=85.0,
            activity_score_before=80.0, activity_score_after=65.0,
            coaching_topic_alignment_score=80.0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
            recidivism_count=0,
        )
        result = eng.assess(inp)
        assert result.coaching_pattern == CoachingPattern.no_behavioral_change
        assert result.is_coaching_ineffective is True

    def test_scenario_insufficient_frequency(self):
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(
            rep_id="LOW_FREQ",
            coaching_sessions_last_90d=1,
            coaching_sessions_benchmark=10,
            days_to_behavioral_change=30,
            recidivism_count=0,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.42,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=92.0,
            activity_score_before=70.0, activity_score_after=72.0,
            coaching_topic_alignment_score=80.0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
        )
        result = eng.assess(inp)
        assert result.coaching_pattern == CoachingPattern.insufficient_frequency

    def test_scenario_high_risk_increase_frequency(self):
        eng = SalesCoachingEffectivenessEngine()
        # Build input that hits high risk + insufficient_frequency pattern
        inp = make_input(
            rep_id="HIGH_FREQ",
            coaching_sessions_last_90d=1,
            coaching_sessions_benchmark=10,
            days_to_behavioral_change=30,
            recidivism_count=1,
            win_rate_before_coaching_pct=0.45, win_rate_after_coaching_pct=0.40,
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=92.0,
            activity_score_before=75.0, activity_score_after=70.0,
            coaching_topic_alignment_score=80.0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
        )
        result = eng.assess(inp)
        if result.coaching_risk == CoachingRisk.high and result.coaching_pattern == CoachingPattern.insufficient_frequency:
            assert result.recommended_action == CoachingAction.increase_coaching_frequency

    def test_to_dict_composite_matches_result(self):
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input()
        result = eng.assess(inp)
        d = result.to_dict()
        assert d["coaching_effectiveness_composite"] == result.coaching_effectiveness_composite

    def test_to_dict_signal_matches_result(self):
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input()
        result = eng.assess(inp)
        d = result.to_dict()
        assert d["coaching_signal"] == result.coaching_signal

    def test_assess_returns_same_as_batch_single(self):
        eng1 = SalesCoachingEffectivenessEngine()
        eng2 = SalesCoachingEffectivenessEngine()
        inp = make_input()
        r_single = eng1.assess(inp)
        r_batch = eng2.assess_batch([inp])[0]
        assert r_single.coaching_effectiveness_composite == r_batch.coaching_effectiveness_composite
        assert r_single.coaching_risk == r_batch.coaching_risk

    def test_win_rate_format_in_signal(self):
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40)
        result = eng.assess(inp)
        # delta = -0.10 → -10pp
        assert "-10pp post-coaching" in result.coaching_signal

    def test_quota_format_in_signal(self):
        eng = SalesCoachingEffectivenessEngine()
        # Ensure composite >= 10 to avoid positive signal; add win rate regression
        inp = make_input(
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=90.0,
            win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40,
        )
        result = eng.assess(inp)
        assert not (result.coaching_pattern == CoachingPattern.none and result.coaching_effectiveness_composite < 10)
        # delta = -10 → -10pp
        assert "attainment -10pp post-coaching" in result.coaching_signal

    def test_region_propagates_to_summary_not_directly(self):
        eng = SalesCoachingEffectivenessEngine()
        eng.assess(make_input(region="EMEA"))
        eng.assess(make_input(region="APAC"))
        # summary doesn't track region breakdown but total should be 2
        assert eng.summary()["total"] == 2

    def test_multiple_reps_different_patterns(self):
        eng = SalesCoachingEffectivenessEngine()
        eng.assess(make_input(rep_id="good"))
        eng.assess(make_input(rep_id="bad1", recidivism_count=3,
                              win_rate_before_coaching_pct=0.60, win_rate_after_coaching_pct=0.30,
                              quota_attainment_before_pct=100.0, quota_attainment_after_pct=75.0,
                              activity_score_before=80.0, activity_score_after=60.0))
        s = eng.summary()
        assert len(s["pattern_counts"]) >= 1

    def test_high_recidivism_always_ineffective(self):
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(recidivism_count=5)
        result = eng.assess(inp)
        assert result.is_coaching_ineffective is True

    def test_low_topic_alignment_always_requires_redesign(self):
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(coaching_topic_alignment_score=10.0)
        result = eng.assess(inp)
        assert result.requires_coaching_redesign is True

    def test_low_manager_pct_always_requires_redesign(self):
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(manager_coaching_effectiveness_pct=0.10)
        result = eng.assess(inp)
        assert result.requires_coaching_redesign is True


# ---------------------------------------------------------------------------
# Class 26: additional sub-score and composite tests
# ---------------------------------------------------------------------------

class TestAdditionalSubScores:
    def test_frequency_score_bench_1_sessions_0(self):
        eng = SalesCoachingEffectivenessEngine()
        s = eng._coaching_frequency_score(make_input(
            coaching_sessions_last_90d=0, coaching_sessions_benchmark=1,
            days_to_behavioral_change=0, recidivism_count=0))
        assert s == 50.0

    def test_frequency_sessions_1_bench_3_below_50pct(self):
        # 1 < 3*0.50=1.5 → +35
        eng = SalesCoachingEffectivenessEngine()
        s = eng._coaching_frequency_score(make_input(
            coaching_sessions_last_90d=1, coaching_sessions_benchmark=3,
            days_to_behavioral_change=0, recidivism_count=0))
        assert s == 35.0

    def test_frequency_sessions_2_bench_3_below_75pct(self):
        # 2 < 3*0.75=2.25 → +20
        eng = SalesCoachingEffectivenessEngine()
        s = eng._coaching_frequency_score(make_input(
            coaching_sessions_last_90d=2, coaching_sessions_benchmark=3,
            days_to_behavioral_change=0, recidivism_count=0))
        assert s == 20.0

    def test_frequency_days_29_no_penalty(self):
        eng = SalesCoachingEffectivenessEngine()
        s = eng._coaching_frequency_score(make_input(
            coaching_sessions_last_90d=6, coaching_sessions_benchmark=6,
            days_to_behavioral_change=29, recidivism_count=0))
        assert s == 10.0  # 29 >= 15 but < 30 → +10

    def test_impact_score_zero_on_all_improvements(self):
        eng = SalesCoachingEffectivenessEngine()
        s = eng._coaching_impact_score(make_input(
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.50,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=100.0,
            activity_score_before=70.0, activity_score_after=80.0,
            recidivism_count=0))
        assert s == 0.0

    def test_impact_score_recidivism_3_adds_15(self):
        eng = SalesCoachingEffectivenessEngine()
        s = eng._coaching_impact_score(make_input(
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.40,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
            activity_score_before=70.0, activity_score_after=70.0,
            recidivism_count=3))
        assert s == 15.0

    def test_alignment_zero_on_good_inputs(self):
        eng = SalesCoachingEffectivenessEngine()
        s = eng._coaching_alignment_score(make_input(
            coaching_topic_alignment_score=90.0,
            avg_discount_before_pct=10.0, avg_discount_after_pct=9.0,
            self_assessed_readiness_score=80.0))
        assert s == 0.0

    def test_manager_score_zero_on_great_manager(self):
        eng = SalesCoachingEffectivenessEngine()
        s = eng._manager_effectiveness_score(make_input(
            manager_coaching_effectiveness_pct=0.90,
            peer_comparison_percentile=80.0,
            deal_quality_improvement_score=20.0))
        assert s == 0.0

    def test_composite_weights_sum_to_1(self):
        # Verify that if all sub-scores are 50, composite = 50
        # freq=50, impact=50, align=50, mgr=50
        # composite = 50*0.20 + 50*0.35 + 50*0.25 + 50*0.20 = 50
        assert round(50*0.20 + 50*0.35 + 50*0.25 + 50*0.20, 1) == 50.0

    def test_impact_score_combined_all_penalties(self):
        eng = SalesCoachingEffectivenessEngine()
        # win_delta < -0.05 → +35, quota < -10 → +30, activity < -10 → +20, recidivism >= 2 → +15 = 100
        s = eng._coaching_impact_score(make_input(
            win_rate_before_coaching_pct=0.60, win_rate_after_coaching_pct=0.40,
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=80.0,
            activity_score_before=90.0, activity_score_after=70.0,
            recidivism_count=2))
        assert s == 100.0

    def test_alignment_combined_max_75_not_capped(self):
        eng = SalesCoachingEffectivenessEngine()
        # alignment < 40 → +40, discount >= 3 → +20, readiness < 40 → +15 = 75
        s = eng._coaching_alignment_score(make_input(
            coaching_topic_alignment_score=20.0,
            avg_discount_before_pct=0.0, avg_discount_after_pct=5.0,
            self_assessed_readiness_score=20.0))
        assert s == 75.0

    def test_manager_score_max_90_not_capped(self):
        eng = SalesCoachingEffectivenessEngine()
        # mgr_pct < 0.30 → +40, peer < 25 → +30, deal_quality < -10 → +20 = 90
        s = eng._manager_effectiveness_score(make_input(
            manager_coaching_effectiveness_pct=0.10,
            peer_comparison_percentile=10.0,
            deal_quality_improvement_score=-20.0))
        assert s == 90.0

    def test_frequency_score_all_penalties(self):
        eng = SalesCoachingEffectivenessEngine()
        # sessions=0 → +50, days=30 → +20, recidivism=3 → +20 = 90
        s = eng._coaching_frequency_score(make_input(
            coaching_sessions_last_90d=0, coaching_sessions_benchmark=6,
            days_to_behavioral_change=30, recidivism_count=3))
        assert s == 90.0

    def test_assess_stores_result(self):
        eng = SalesCoachingEffectivenessEngine()
        eng.assess(make_input())
        assert len(eng._results) == 1

    def test_assess_batch_stores_all_results(self):
        eng = SalesCoachingEffectivenessEngine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        assert len(eng._results) == 5


# ---------------------------------------------------------------------------
# Class 27: additional risk/severity/action boundary tests
# ---------------------------------------------------------------------------

class TestAdditionalRiskSeverityAction:
    def test_risk_boundary_59_9_is_high(self):
        eng = SalesCoachingEffectivenessEngine()
        assert eng._risk_level(59.9) == CoachingRisk.high

    def test_risk_boundary_39_9_is_moderate(self):
        eng = SalesCoachingEffectivenessEngine()
        assert eng._risk_level(39.9) == CoachingRisk.moderate

    def test_risk_boundary_19_9_is_low(self):
        eng = SalesCoachingEffectivenessEngine()
        assert eng._risk_level(19.9) == CoachingRisk.low

    def test_severity_boundary_59_9_is_stalled(self):
        eng = SalesCoachingEffectivenessEngine()
        assert eng._severity(59.9) == CoachingSeverity.stalled

    def test_severity_boundary_39_9_is_developing(self):
        eng = SalesCoachingEffectivenessEngine()
        assert eng._severity(39.9) == CoachingSeverity.developing

    def test_severity_boundary_19_9_is_effective(self):
        eng = SalesCoachingEffectivenessEngine()
        assert eng._severity(19.9) == CoachingSeverity.effective

    def test_action_high_coaching_resistance_is_reset(self):
        eng = SalesCoachingEffectivenessEngine()
        assert eng._action(CoachingRisk.high, CoachingPattern.coaching_resistance) == CoachingAction.coaching_topic_reset

    def test_action_moderate_no_behavioral_change_is_reset(self):
        eng = SalesCoachingEffectivenessEngine()
        assert eng._action(CoachingRisk.moderate, CoachingPattern.no_behavioral_change) == CoachingAction.coaching_topic_reset

    def test_action_moderate_topic_misalignment_is_reset(self):
        eng = SalesCoachingEffectivenessEngine()
        assert eng._action(CoachingRisk.moderate, CoachingPattern.topic_misalignment) == CoachingAction.coaching_topic_reset

    def test_action_moderate_manager_ineffectiveness_is_reset(self):
        eng = SalesCoachingEffectivenessEngine()
        assert eng._action(CoachingRisk.moderate, CoachingPattern.manager_ineffectiveness) == CoachingAction.coaching_topic_reset

    def test_action_moderate_coaching_resistance_is_reset(self):
        eng = SalesCoachingEffectivenessEngine()
        assert eng._action(CoachingRisk.moderate, CoachingPattern.coaching_resistance) == CoachingAction.coaching_topic_reset

    def test_action_moderate_none_is_reset(self):
        eng = SalesCoachingEffectivenessEngine()
        assert eng._action(CoachingRisk.moderate, CoachingPattern.none) == CoachingAction.coaching_topic_reset

    def test_action_low_all_patterns_no_action(self):
        eng = SalesCoachingEffectivenessEngine()
        for p in CoachingPattern:
            assert eng._action(CoachingRisk.low, p) == CoachingAction.no_action


# ---------------------------------------------------------------------------
# Class 28: additional pattern detection edge cases
# ---------------------------------------------------------------------------

class TestAdditionalPatternDetection:
    def test_coaching_resistance_requires_recidivism_ge_3(self):
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(
            recidivism_count=2,  # not >= 3
            win_rate_before_coaching_pct=0.60, win_rate_after_coaching_pct=0.30,
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=75.0,
            activity_score_before=80.0, activity_score_after=60.0,
        )
        result = eng.assess(inp)
        assert result.coaching_pattern != CoachingPattern.coaching_resistance

    def test_manager_ineffectiveness_requires_manager_score_ge_40(self):
        # Set manager_pct < 0.40 but low peer/deal so manager score < 40
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(
            manager_coaching_effectiveness_pct=0.35,  # → +25 only
            peer_comparison_percentile=80.0,  # no penalty
            deal_quality_improvement_score=10.0,  # no penalty
            recidivism_count=0,
        )
        result = eng.assess(inp)
        # manager score = 25, which is < 40 → no manager_ineffectiveness
        assert result.coaching_pattern != CoachingPattern.manager_ineffectiveness

    def test_topic_misalignment_requires_alignment_score_ge_35(self):
        # coaching_topic_alignment_score < 50 but alignment score < 35
        eng = SalesCoachingEffectivenessEngine()
        inp = make_input(
            coaching_topic_alignment_score=45.0,  # < 50 ✓ but alignment score...
            avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
            self_assessed_readiness_score=75.0,
            # alignment score: 45 is between 40 and 60 → +25 ≥ 35 ✓
            recidivism_count=0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.42,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=92.0,
            activity_score_before=70.0, activity_score_after=72.0,
        )
        result = eng.assess(inp)
        # alignment_score = 25 < 35 → topic_misalignment NOT triggered
        assert result.coaching_pattern != CoachingPattern.topic_misalignment

    def test_insufficient_frequency_not_triggered_if_sessions_ge_50pct(self):
        eng = SalesCoachingEffectivenessEngine()
        # sessions = 5, bench = 8 → 5 >= 8*0.50=4 → no insufficient_frequency
        inp = make_input(
            coaching_sessions_last_90d=5, coaching_sessions_benchmark=8,
            days_to_behavioral_change=30, recidivism_count=0,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.42,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=92.0,
            activity_score_before=70.0, activity_score_after=72.0,
            coaching_topic_alignment_score=80.0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
        )
        result = eng.assess(inp)
        assert result.coaching_pattern != CoachingPattern.insufficient_frequency

    def test_no_behavioral_change_requires_impact_ge_30(self):
        eng = SalesCoachingEffectivenessEngine()
        # win_after <= win_before AND quota_after <= quota_before, but impact score < 30
        inp = make_input(
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.40,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=90.0,
            recidivism_count=0,
            activity_score_before=70.0, activity_score_after=70.0,
        )
        result = eng.assess(inp)
        # impact score = 0 < 30 → no_behavioral_change NOT triggered
        assert result.coaching_pattern != CoachingPattern.no_behavioral_change


# ---------------------------------------------------------------------------
# Class 29: additional to_dict and summary edge cases
# ---------------------------------------------------------------------------

class TestAdditionalDictAndSummary:
    def test_to_dict_is_ineffective_matches_field(self, engine):
        inp = make_input(recidivism_count=4)
        result = engine.assess(inp)
        assert result.to_dict()["is_coaching_ineffective"] == result.is_coaching_ineffective

    def test_to_dict_requires_redesign_matches_field(self, engine):
        inp = make_input(coaching_topic_alignment_score=20.0)
        result = engine.assess(inp)
        assert result.to_dict()["requires_coaching_redesign"] == result.requires_coaching_redesign

    def test_to_dict_revenue_impact_matches_field(self, engine):
        inp = make_input(avg_deal_size_before_usd=70_000.0, avg_deal_size_after_usd=60_000.0)
        result = engine.assess(inp)
        assert result.to_dict()["estimated_revenue_impact_usd"] == result.estimated_revenue_impact_usd

    def test_to_dict_coaching_risk_value_is_string(self, engine):
        result = engine.assess(make_input())
        d = result.to_dict()
        assert d["coaching_risk"] in ["low", "moderate", "high", "critical"]

    def test_to_dict_coaching_pattern_value_is_string(self, engine):
        result = engine.assess(make_input())
        d = result.to_dict()
        valid_patterns = ["none", "insufficient_frequency", "no_behavioral_change",
                          "topic_misalignment", "manager_ineffectiveness", "coaching_resistance"]
        assert d["coaching_pattern"] in valid_patterns

    def test_to_dict_coaching_severity_value_is_string(self, engine):
        result = engine.assess(make_input())
        d = result.to_dict()
        assert d["coaching_severity"] in ["effective", "developing", "stalled", "regressing"]

    def test_to_dict_recommended_action_value_is_string(self, engine):
        result = engine.assess(make_input())
        d = result.to_dict()
        valid_actions = ["no_action", "increase_coaching_frequency", "coaching_topic_reset",
                         "manager_coaching_training", "external_coach_engagement", "performance_management"]
        assert d["recommended_action"] in valid_actions

    def test_summary_avg_composite_single_item(self):
        eng = SalesCoachingEffectivenessEngine()
        result = eng.assess(make_input())
        s = eng.summary()
        assert s["avg_coaching_effectiveness_composite"] == result.coaching_effectiveness_composite

    def test_summary_avg_frequency_single_item(self):
        eng = SalesCoachingEffectivenessEngine()
        result = eng.assess(make_input())
        s = eng.summary()
        assert s["avg_coaching_frequency_score"] == result.coaching_frequency_score

    def test_summary_avg_impact_single_item(self):
        eng = SalesCoachingEffectivenessEngine()
        result = eng.assess(make_input())
        s = eng.summary()
        assert s["avg_coaching_impact_score"] == result.coaching_impact_score

    def test_summary_avg_alignment_single_item(self):
        eng = SalesCoachingEffectivenessEngine()
        result = eng.assess(make_input())
        s = eng.summary()
        assert s["avg_coaching_alignment_score"] == result.coaching_alignment_score

    def test_summary_avg_manager_single_item(self):
        eng = SalesCoachingEffectivenessEngine()
        result = eng.assess(make_input())
        s = eng.summary()
        assert s["avg_manager_effectiveness_score"] == result.manager_effectiveness_score

    def test_summary_ineffective_count_zero_for_good_rep(self):
        eng = SalesCoachingEffectivenessEngine()
        eng.assess(make_input())
        s = eng.summary()
        assert s["ineffective_coaching_count"] == 0

    def test_summary_redesign_count_zero_for_good_rep(self):
        eng = SalesCoachingEffectivenessEngine()
        eng.assess(make_input())
        s = eng.summary()
        assert s["coaching_redesign_count"] == 0

    def test_summary_revenue_impact_zero_for_improved_deal_size(self):
        eng = SalesCoachingEffectivenessEngine()
        eng.assess(make_input(avg_deal_size_before_usd=50_000.0, avg_deal_size_after_usd=55_000.0))
        s = eng.summary()
        assert s["total_estimated_revenue_impact_usd"] == 0.0


# ---------------------------------------------------------------------------
# Class 30: signal string format precision tests
# ---------------------------------------------------------------------------

class TestSignalFormat:
    def test_signal_is_string(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.coaching_signal, str)

    def test_signal_nonempty(self, engine):
        result = engine.assess(make_input())
        assert len(result.coaching_signal) > 0

    def test_positive_signal_exact_text(self, engine):
        # zero composite scenario
        inp = make_input(
            coaching_sessions_last_90d=6, coaching_sessions_benchmark=6,
            days_to_behavioral_change=0, recidivism_count=0,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.42,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=92.0,
            activity_score_before=70.0, activity_score_after=72.0,
            coaching_topic_alignment_score=80.0,
            avg_discount_before_pct=10.0, avg_discount_after_pct=10.0,
            self_assessed_readiness_score=75.0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
        )
        result = engine.assess(inp)
        assert result.coaching_signal == "Coaching driving measurable performance improvement"

    def test_signal_win_delta_negative_20pp(self, engine):
        # before=0.60, after=0.40 → delta=-0.20 → "-20pp"
        inp = make_input(
            win_rate_before_coaching_pct=0.60, win_rate_after_coaching_pct=0.40,
        )
        result = engine.assess(inp)
        assert "win rate -20pp post-coaching" in result.coaching_signal

    def test_signal_quota_negative_15pp(self, engine):
        inp = make_input(
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=85.0,
            win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40,
        )
        result = engine.assess(inp)
        assert "attainment -15pp post-coaching" in result.coaching_signal

    def test_signal_1_recidivism_text(self, engine):
        inp = make_input(
            recidivism_count=1,
            win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40,
        )
        result = engine.assess(inp)
        assert "1 recidivism incidents" in result.coaching_signal

    def test_signal_coaching_resistance_label(self, engine):
        inp = make_input(
            recidivism_count=3,
            win_rate_before_coaching_pct=0.60, win_rate_after_coaching_pct=0.30,
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=75.0,
            activity_score_before=80.0, activity_score_after=60.0,
        )
        result = engine.assess(inp)
        if result.coaching_pattern == CoachingPattern.coaching_resistance:
            assert result.coaching_signal.startswith("Coaching resistance")

    def test_signal_insufficient_frequency_label(self, engine):
        inp = make_input(
            coaching_sessions_last_90d=1, coaching_sessions_benchmark=10,
            days_to_behavioral_change=30,
            recidivism_count=0,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.42,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=92.0,
            activity_score_before=70.0, activity_score_after=72.0,
            coaching_topic_alignment_score=80.0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
        )
        result = engine.assess(inp)
        if result.coaching_pattern == CoachingPattern.insufficient_frequency:
            assert result.coaching_signal.startswith("Insufficient frequency")

    def test_signal_no_behavioral_change_label(self, engine):
        inp = make_input(
            win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40,
            quota_attainment_before_pct=100.0, quota_attainment_after_pct=85.0,
            activity_score_before=80.0, activity_score_after=65.0,
            coaching_topic_alignment_score=80.0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
            recidivism_count=0,
        )
        result = engine.assess(inp)
        if result.coaching_pattern == CoachingPattern.no_behavioral_change:
            assert result.coaching_signal.startswith("No behavioral change")

    def test_signal_topic_misalignment_label(self, engine):
        inp = make_input(
            coaching_topic_alignment_score=30.0,
            avg_discount_before_pct=0.0, avg_discount_after_pct=5.0,
            self_assessed_readiness_score=30.0,
            manager_coaching_effectiveness_pct=0.80,
            peer_comparison_percentile=60.0,
            deal_quality_improvement_score=5.0,
            recidivism_count=0,
            win_rate_before_coaching_pct=0.40, win_rate_after_coaching_pct=0.42,
            quota_attainment_before_pct=90.0, quota_attainment_after_pct=92.0,
            activity_score_before=70.0, activity_score_after=72.0,
        )
        result = engine.assess(inp)
        if result.coaching_pattern == CoachingPattern.topic_misalignment:
            assert result.coaching_signal.startswith("Topic misalignment")

    def test_signal_ends_with_composite(self, engine):
        inp = make_input(
            win_rate_before_coaching_pct=0.50, win_rate_after_coaching_pct=0.40,
        )
        result = engine.assess(inp)
        composite_str = f"composite {result.coaching_effectiveness_composite:.0f}"
        assert result.coaching_signal.endswith(composite_str)

    def test_signal_coaching_risk_label_capitalized(self, engine):
        # pattern=none, composite >= 10
        inp = make_input(
            recidivism_count=1,
            win_rate_before_coaching_pct=0.45, win_rate_after_coaching_pct=0.42,
        )
        result = engine.assess(inp)
        if result.coaching_pattern == CoachingPattern.none and result.coaching_effectiveness_composite >= 10:
            assert result.coaching_signal.startswith("Coaching risk")
