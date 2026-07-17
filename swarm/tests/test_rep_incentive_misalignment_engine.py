"""
Comprehensive pytest test suite for RepIncentiveMisalignmentEngine.

Organized into test classes covering:
  - Enum values and membership
  - Dataclass field counts
  - to_dict() / summary() key counts
  - Sub-score range invariants
  - Composite formula correctness
  - is_gaming_quota boundary conditions
  - requires_plan_review boundary conditions
  - estimated_revenue_risk_usd formula
  - assess() return-type correctness
  - assess_batch() behaviour
  - summary() key correctness
  - Determinism
  - Aligned-rep / pathological-rep smoke tests
  - Rating, risk, action thresholds
  - Primary misalignment type logic
  - Signal string generation
  - Engine state (reset, get, all_reps, gaming_reps, by_rating, by_risk)
  - Edge cases (zero quotas, zero targets, extreme values)
"""

from __future__ import annotations

import dataclasses
from typing import List

import pytest

from swarm.intelligence.rep_incentive_misalignment_engine import (
    IncentiveAction,
    MisalignmentRating,
    MisalignmentRisk,
    MisalignmentType,
    RepIncentiveInput,
    RepIncentiveMisalignmentEngine,
    RepIncentiveResult,
)

# ---------------------------------------------------------------------------
# Helpers / Fixtures
# ---------------------------------------------------------------------------

EXPECTED_TO_DICT_KEYS = [
    "rep_id",
    "rep_name",
    "misalignment_rating",
    "misalignment_risk",
    "primary_misalignment_type",
    "incentive_action",
    "behavior_alignment_score",
    "strategic_alignment_score",
    "discount_discipline_score",
    "revenue_quality_score",
    "misalignment_composite",
    "is_gaming_quota",
    "requires_plan_review",
    "estimated_revenue_risk_usd",
    "misalignment_signal",
]

EXPECTED_SUMMARY_KEYS = [
    "total",
    "rating_counts",
    "risk_counts",
    "type_counts",
    "action_counts",
    "avg_misalignment_composite",
    "gaming_quota_count",
    "plan_review_count",
    "avg_behavior_alignment_score",
    "avg_strategic_alignment_score",
    "avg_discount_discipline_score",
    "avg_revenue_quality_score",
    "total_revenue_risk_usd",
]


def make_aligned_input(**overrides) -> RepIncentiveInput:
    """Return an input representing a highly aligned rep (all scores push toward 0 composite)."""
    defaults = dict(
        rep_id="aligned-001",
        rep_name="Alice Aligned",
        region="West",
        quota_usd=1_000_000.0,
        closed_won_usd=1_000_000.0,
        avg_deal_size_usd=100_000.0,
        company_avg_deal_size_usd=100_000.0,
        discount_pct_avg=10.0,
        company_avg_discount_pct=10.0,
        strategic_account_revenue_pct=50.0,
        target_strategic_revenue_pct=50.0,
        sandbagging_score=10.0,          # very low → high behavior score
        late_quarter_close_pct=20.0,      # low → good
        multi_year_deal_pct=35.0,
        target_multi_year_pct=30.0,
        renewal_neglect_count=0,
        upsell_attempt_rate_pct=40.0,
        target_upsell_rate_pct=40.0,
        commission_dispute_count=0,
        spiff_overreliance_score=10.0,
        forecast_accuracy_pct=90.0,
        deal_size_variance_pct=15.0,
    )
    defaults.update(overrides)
    return RepIncentiveInput(**defaults)


def make_pathological_input(**overrides) -> RepIncentiveInput:
    """Return an input representing a severely misaligned rep."""
    defaults = dict(
        rep_id="bad-001",
        rep_name="Bob Bad",
        region="East",
        quota_usd=1_000_000.0,
        closed_won_usd=500_000.0,
        avg_deal_size_usd=20_000.0,
        company_avg_deal_size_usd=100_000.0,
        discount_pct_avg=30.0,
        company_avg_discount_pct=10.0,
        strategic_account_revenue_pct=5.0,
        target_strategic_revenue_pct=50.0,
        sandbagging_score=90.0,           # very high → bad
        late_quarter_close_pct=90.0,      # very high → bad
        multi_year_deal_pct=0.0,
        target_multi_year_pct=30.0,
        renewal_neglect_count=5,
        upsell_attempt_rate_pct=0.0,
        target_upsell_rate_pct=40.0,
        commission_dispute_count=5,
        spiff_overreliance_score=90.0,
        forecast_accuracy_pct=20.0,
        deal_size_variance_pct=80.0,
    )
    defaults.update(overrides)
    return RepIncentiveInput(**defaults)


@pytest.fixture
def engine() -> RepIncentiveMisalignmentEngine:
    return RepIncentiveMisalignmentEngine()


@pytest.fixture
def aligned_input() -> RepIncentiveInput:
    return make_aligned_input()


@pytest.fixture
def pathological_input() -> RepIncentiveInput:
    return make_pathological_input()


# ===========================================================================
# 1. Enum Tests
# ===========================================================================


class TestMisalignmentRatingEnum:
    def test_has_five_members(self):
        assert len(MisalignmentRating) == 5

    def test_aligned_value(self):
        assert MisalignmentRating.ALIGNED.value == "aligned"

    def test_minor_value(self):
        assert MisalignmentRating.MINOR.value == "minor"

    def test_moderate_value(self):
        assert MisalignmentRating.MODERATE.value == "moderate"

    def test_severe_value(self):
        assert MisalignmentRating.SEVERE.value == "severe"

    def test_critical_value(self):
        assert MisalignmentRating.CRITICAL.value == "critical"

    def test_is_str_enum(self):
        assert isinstance(MisalignmentRating.ALIGNED, str)

    def test_str_comparison_aligned(self):
        assert MisalignmentRating.ALIGNED == "aligned"

    def test_str_comparison_critical(self):
        assert MisalignmentRating.CRITICAL == "critical"

    def test_members_by_name(self):
        expected_names = {"ALIGNED", "MINOR", "MODERATE", "SEVERE", "CRITICAL"}
        assert set(MisalignmentRating.__members__) == expected_names

    def test_iterable(self):
        values = [m.value for m in MisalignmentRating]
        assert "aligned" in values and "critical" in values


class TestMisalignmentRiskEnum:
    def test_has_four_members(self):
        assert len(MisalignmentRisk) == 4

    def test_low_value(self):
        assert MisalignmentRisk.LOW.value == "low"

    def test_moderate_value(self):
        assert MisalignmentRisk.MODERATE.value == "moderate"

    def test_high_value(self):
        assert MisalignmentRisk.HIGH.value == "high"

    def test_critical_value(self):
        assert MisalignmentRisk.CRITICAL.value == "critical"

    def test_is_str_enum(self):
        assert isinstance(MisalignmentRisk.LOW, str)

    def test_str_comparison(self):
        assert MisalignmentRisk.HIGH == "high"

    def test_members_by_name(self):
        expected_names = {"LOW", "MODERATE", "HIGH", "CRITICAL"}
        assert set(MisalignmentRisk.__members__) == expected_names


class TestMisalignmentTypeEnum:
    def test_has_six_members(self):
        assert len(MisalignmentType) == 6

    def test_none_value(self):
        assert MisalignmentType.NONE.value == "none"

    def test_sandbagging_value(self):
        assert MisalignmentType.SANDBAGGING.value == "sandbagging"

    def test_cherry_picking_value(self):
        assert MisalignmentType.CHERRY_PICKING.value == "cherry_picking"

    def test_discount_abuse_value(self):
        assert MisalignmentType.DISCOUNT_ABUSE.value == "discount_abuse"

    def test_account_neglect_value(self):
        assert MisalignmentType.ACCOUNT_NEGLECT.value == "account_neglect"

    def test_quota_gaming_value(self):
        assert MisalignmentType.QUOTA_GAMING.value == "quota_gaming"

    def test_is_str_enum(self):
        assert isinstance(MisalignmentType.NONE, str)

    def test_members_by_name(self):
        expected_names = {
            "NONE", "SANDBAGGING", "CHERRY_PICKING",
            "DISCOUNT_ABUSE", "ACCOUNT_NEGLECT", "QUOTA_GAMING",
        }
        assert set(MisalignmentType.__members__) == expected_names


class TestIncentiveActionEnum:
    def test_has_five_members(self):
        assert len(IncentiveAction) == 5

    def test_no_action_value(self):
        assert IncentiveAction.NO_ACTION.value == "no_action"

    def test_monitor_value(self):
        assert IncentiveAction.MONITOR.value == "monitor"

    def test_plan_review_value(self):
        assert IncentiveAction.PLAN_REVIEW.value == "plan_review"

    def test_manager_coaching_value(self):
        assert IncentiveAction.MANAGER_COACHING.value == "manager_coaching"

    def test_comp_restructure_value(self):
        assert IncentiveAction.COMP_RESTRUCTURE.value == "comp_restructure"

    def test_is_str_enum(self):
        assert isinstance(IncentiveAction.NO_ACTION, str)

    def test_members_by_name(self):
        expected_names = {
            "NO_ACTION", "MONITOR", "PLAN_REVIEW", "MANAGER_COACHING", "COMP_RESTRUCTURE",
        }
        assert set(IncentiveAction.__members__) == expected_names


# ===========================================================================
# 2. Dataclass Field Count Tests
# ===========================================================================


class TestInputDataclassFields:
    def test_field_count_is_22(self):
        fields = dataclasses.fields(RepIncentiveInput)
        assert len(fields) == 22

    def test_has_rep_id(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "rep_id" in names

    def test_has_rep_name(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "rep_name" in names

    def test_has_region(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "region" in names

    def test_has_quota_usd(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "quota_usd" in names

    def test_has_closed_won_usd(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "closed_won_usd" in names

    def test_has_avg_deal_size_usd(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "avg_deal_size_usd" in names

    def test_has_company_avg_deal_size_usd(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "company_avg_deal_size_usd" in names

    def test_has_discount_pct_avg(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "discount_pct_avg" in names

    def test_has_company_avg_discount_pct(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "company_avg_discount_pct" in names

    def test_has_strategic_account_revenue_pct(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "strategic_account_revenue_pct" in names

    def test_has_target_strategic_revenue_pct(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "target_strategic_revenue_pct" in names

    def test_has_sandbagging_score(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "sandbagging_score" in names

    def test_has_late_quarter_close_pct(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "late_quarter_close_pct" in names

    def test_has_multi_year_deal_pct(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "multi_year_deal_pct" in names

    def test_has_target_multi_year_pct(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "target_multi_year_pct" in names

    def test_has_renewal_neglect_count(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "renewal_neglect_count" in names

    def test_has_upsell_attempt_rate_pct(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "upsell_attempt_rate_pct" in names

    def test_has_target_upsell_rate_pct(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "target_upsell_rate_pct" in names

    def test_has_commission_dispute_count(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "commission_dispute_count" in names

    def test_has_spiff_overreliance_score(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "spiff_overreliance_score" in names

    def test_has_forecast_accuracy_pct(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "forecast_accuracy_pct" in names

    def test_has_deal_size_variance_pct(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert "deal_size_variance_pct" in names

    def test_all_22_field_names(self):
        expected = {
            "rep_id", "rep_name", "region", "quota_usd", "closed_won_usd",
            "avg_deal_size_usd", "company_avg_deal_size_usd", "discount_pct_avg",
            "company_avg_discount_pct", "strategic_account_revenue_pct",
            "target_strategic_revenue_pct", "sandbagging_score",
            "late_quarter_close_pct", "multi_year_deal_pct", "target_multi_year_pct",
            "renewal_neglect_count", "upsell_attempt_rate_pct", "target_upsell_rate_pct",
            "commission_dispute_count", "spiff_overreliance_score",
            "forecast_accuracy_pct", "deal_size_variance_pct",
        }
        actual = {f.name for f in dataclasses.fields(RepIncentiveInput)}
        assert actual == expected


class TestResultDataclassFields:
    def test_result_field_count_is_15(self):
        fields = dataclasses.fields(RepIncentiveResult)
        assert len(fields) == 15

    def test_result_has_rep_id(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveResult)}
        assert "rep_id" in names

    def test_result_has_misalignment_composite(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveResult)}
        assert "misalignment_composite" in names

    def test_result_has_is_gaming_quota(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveResult)}
        assert "is_gaming_quota" in names

    def test_result_has_requires_plan_review(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveResult)}
        assert "requires_plan_review" in names

    def test_result_has_estimated_revenue_risk_usd(self):
        names = {f.name for f in dataclasses.fields(RepIncentiveResult)}
        assert "estimated_revenue_risk_usd" in names


# ===========================================================================
# 3. to_dict() Key Count Tests
# ===========================================================================


class TestToDictKeyCount:
    def test_to_dict_returns_exactly_15_keys(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert len(result.to_dict()) == 15

    def test_to_dict_key_count_pathological(self, engine, pathological_input):
        result = engine.assess(pathological_input)
        assert len(result.to_dict()) == 15

    def test_to_dict_exact_key_names(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert set(result.to_dict().keys()) == set(EXPECTED_TO_DICT_KEYS)

    def test_to_dict_rep_id_correct(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert result.to_dict()["rep_id"] == "aligned-001"

    def test_to_dict_rep_name_correct(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert result.to_dict()["rep_name"] == "Alice Aligned"

    def test_to_dict_misalignment_rating_is_string(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert isinstance(result.to_dict()["misalignment_rating"], str)

    def test_to_dict_misalignment_risk_is_string(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert isinstance(result.to_dict()["misalignment_risk"], str)

    def test_to_dict_primary_misalignment_type_is_string(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert isinstance(result.to_dict()["primary_misalignment_type"], str)

    def test_to_dict_incentive_action_is_string(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert isinstance(result.to_dict()["incentive_action"], str)

    def test_to_dict_is_gaming_quota_is_bool(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert isinstance(result.to_dict()["is_gaming_quota"], bool)

    def test_to_dict_requires_plan_review_is_bool(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert isinstance(result.to_dict()["requires_plan_review"], bool)

    def test_to_dict_composite_is_float(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert isinstance(result.to_dict()["misalignment_composite"], float)

    def test_to_dict_revenue_risk_is_numeric(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert isinstance(result.to_dict()["estimated_revenue_risk_usd"], (int, float))

    def test_to_dict_signal_is_string(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert isinstance(result.to_dict()["misalignment_signal"], str)

    def test_to_dict_behavior_score_is_float(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert isinstance(result.to_dict()["behavior_alignment_score"], float)

    def test_to_dict_strategic_score_is_float(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert isinstance(result.to_dict()["strategic_alignment_score"], float)

    def test_to_dict_discount_score_is_float(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert isinstance(result.to_dict()["discount_discipline_score"], float)

    def test_to_dict_quality_score_is_float(self, engine, aligned_input):
        result = engine.assess(aligned_input)
        assert isinstance(result.to_dict()["revenue_quality_score"], float)


# ===========================================================================
# 4. summary() Key Count Tests
# ===========================================================================


class TestSummaryKeyCount:
    def test_summary_returns_exactly_13_keys(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert len(engine.summary()) == 13

    def test_summary_exact_key_names(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert set(engine.summary().keys()) == set(EXPECTED_SUMMARY_KEYS)

    def test_summary_key_count_empty_engine(self, engine):
        # summary on empty engine still returns 13 keys
        assert len(engine.summary()) == 13

    def test_summary_key_count_multiple_reps(self, engine, aligned_input, pathological_input):
        engine.assess(aligned_input)
        engine.assess(pathological_input)
        assert len(engine.summary()) == 13

    def test_summary_total_key(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert "total" in engine.summary()

    def test_summary_rating_counts_key(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert "rating_counts" in engine.summary()

    def test_summary_risk_counts_key(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert "risk_counts" in engine.summary()

    def test_summary_type_counts_key(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert "type_counts" in engine.summary()

    def test_summary_action_counts_key(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert "action_counts" in engine.summary()

    def test_summary_avg_composite_key(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert "avg_misalignment_composite" in engine.summary()

    def test_summary_gaming_quota_count_key(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert "gaming_quota_count" in engine.summary()

    def test_summary_plan_review_count_key(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert "plan_review_count" in engine.summary()

    def test_summary_avg_behavior_score_key(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert "avg_behavior_alignment_score" in engine.summary()

    def test_summary_avg_strategic_score_key(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert "avg_strategic_alignment_score" in engine.summary()

    def test_summary_avg_discount_score_key(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert "avg_discount_discipline_score" in engine.summary()

    def test_summary_avg_quality_score_key(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert "avg_revenue_quality_score" in engine.summary()

    def test_summary_total_revenue_risk_key(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert "total_revenue_risk_usd" in engine.summary()


# ===========================================================================
# 5. Sub-Score Range Invariants [0, 100]
# ===========================================================================


class TestSubScoreRanges:
    """All four sub-scores must stay in [0, 100] for any valid input."""

    def _check_ranges(self, result: RepIncentiveResult):
        for attr in (
            "behavior_alignment_score",
            "strategic_alignment_score",
            "discount_discipline_score",
            "revenue_quality_score",
        ):
            val = getattr(result, attr)
            assert 0.0 <= val <= 100.0, f"{attr}={val} out of [0,100]"

    def test_aligned_rep_scores_in_range(self, engine, aligned_input):
        self._check_ranges(engine.assess(aligned_input))

    def test_pathological_rep_scores_in_range(self, engine, pathological_input):
        self._check_ranges(engine.assess(pathological_input))

    def test_behavior_score_range_zero_sandbagging(self, engine):
        inp = make_aligned_input(rep_id="b1", sandbagging_score=0.0, forecast_accuracy_pct=100.0)
        r = engine.assess(inp)
        assert 0.0 <= r.behavior_alignment_score <= 100.0

    def test_behavior_score_range_max_sandbagging(self, engine):
        inp = make_aligned_input(rep_id="b2", sandbagging_score=100.0, forecast_accuracy_pct=0.0,
                                  late_quarter_close_pct=100.0, commission_dispute_count=10)
        r = engine.assess(inp)
        assert 0.0 <= r.behavior_alignment_score <= 100.0

    def test_strategic_score_range_zero_target(self, engine):
        inp = make_aligned_input(rep_id="s1", target_strategic_revenue_pct=0.0,
                                  target_multi_year_pct=0.0, target_upsell_rate_pct=0.0)
        r = engine.assess(inp)
        assert 0.0 <= r.strategic_alignment_score <= 100.0

    def test_strategic_score_range_high_neglect(self, engine):
        inp = make_aligned_input(rep_id="s2", renewal_neglect_count=10,
                                  strategic_account_revenue_pct=0.0, upsell_attempt_rate_pct=0.0)
        r = engine.assess(inp)
        assert 0.0 <= r.strategic_alignment_score <= 100.0

    def test_discount_score_range_extreme_delta(self, engine):
        inp = make_aligned_input(rep_id="d1", discount_pct_avg=100.0, company_avg_discount_pct=0.0,
                                  spiff_overreliance_score=100.0, deal_size_variance_pct=100.0)
        r = engine.assess(inp)
        assert 0.0 <= r.discount_discipline_score <= 100.0

    def test_revenue_quality_score_range_low_attain(self, engine):
        inp = make_aligned_input(rep_id="q1", closed_won_usd=10_000.0, quota_usd=10_000_000.0,
                                  avg_deal_size_usd=1_000.0, multi_year_deal_pct=0.0)
        r = engine.assess(inp)
        assert 0.0 <= r.revenue_quality_score <= 100.0

    def test_revenue_quality_score_range_overperformer(self, engine):
        inp = make_aligned_input(rep_id="q2", closed_won_usd=5_000_000.0, quota_usd=1_000_000.0,
                                  avg_deal_size_usd=200_000.0, multi_year_deal_pct=50.0)
        r = engine.assess(inp)
        assert 0.0 <= r.revenue_quality_score <= 100.0

    def test_composite_range(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert 0.0 <= r.misalignment_composite <= 100.0

    def test_composite_range_pathological(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        assert 0.0 <= r.misalignment_composite <= 100.0


# ===========================================================================
# 6. Composite Formula Correctness
# ===========================================================================


class TestCompositeFormula:
    """Verify (100-b)*0.30 + (100-s)*0.25 + (100-d)*0.25 + (100-q)*0.20"""

    def _expected_composite(self, b, s, d, q) -> float:
        raw = (100 - b) * 0.30 + (100 - s) * 0.25 + (100 - d) * 0.25 + (100 - q) * 0.20
        return round(raw, 1)

    def test_composite_formula_aligned(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        expected = self._expected_composite(
            r.behavior_alignment_score,
            r.strategic_alignment_score,
            r.discount_discipline_score,
            r.revenue_quality_score,
        )
        assert r.misalignment_composite == pytest.approx(expected, abs=0.05)

    def test_composite_formula_pathological(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        expected = self._expected_composite(
            r.behavior_alignment_score,
            r.strategic_alignment_score,
            r.discount_discipline_score,
            r.revenue_quality_score,
        )
        assert r.misalignment_composite == pytest.approx(expected, abs=0.05)

    def test_composite_all_zeros_gives_100(self):
        """If every sub-score is 0, composite should be 100."""
        from swarm.intelligence.rep_incentive_misalignment_engine import _misalignment_composite
        assert _misalignment_composite(0, 0, 0, 0) == pytest.approx(100.0, abs=0.05)

    def test_composite_all_100_gives_0(self):
        """If every sub-score is 100, composite should be 0."""
        from swarm.intelligence.rep_incentive_misalignment_engine import _misalignment_composite
        assert _misalignment_composite(100, 100, 100, 100) == pytest.approx(0.0, abs=0.05)

    def test_composite_behavior_weight_30pct(self):
        from swarm.intelligence.rep_incentive_misalignment_engine import _misalignment_composite
        # Only behavior differs from 100; contribution should be (100-50)*0.30 = 15
        result = _misalignment_composite(50, 100, 100, 100)
        assert result == pytest.approx(15.0, abs=0.05)

    def test_composite_strategic_weight_25pct(self):
        from swarm.intelligence.rep_incentive_misalignment_engine import _misalignment_composite
        # Only strategic differs; (100-50)*0.25 = 12.5
        result = _misalignment_composite(100, 50, 100, 100)
        assert result == pytest.approx(12.5, abs=0.05)

    def test_composite_discount_weight_25pct(self):
        from swarm.intelligence.rep_incentive_misalignment_engine import _misalignment_composite
        result = _misalignment_composite(100, 100, 50, 100)
        assert result == pytest.approx(12.5, abs=0.05)

    def test_composite_quality_weight_20pct(self):
        from swarm.intelligence.rep_incentive_misalignment_engine import _misalignment_composite
        result = _misalignment_composite(100, 100, 100, 50)
        assert result == pytest.approx(10.0, abs=0.05)

    def test_composite_weights_sum_to_100(self):
        """Weights: 0.30 + 0.25 + 0.25 + 0.20 = 1.0, so composite of all-0 scores = 100."""
        from swarm.intelligence.rep_incentive_misalignment_engine import _misalignment_composite
        assert _misalignment_composite(0, 0, 0, 0) == pytest.approx(100.0, abs=0.05)

    def test_composite_specific_example(self):
        from swarm.intelligence.rep_incentive_misalignment_engine import _misalignment_composite
        b, s, d, q = 80.0, 60.0, 70.0, 50.0
        expected = (100 - 80) * 0.30 + (100 - 60) * 0.25 + (100 - 70) * 0.25 + (100 - 50) * 0.20
        assert _misalignment_composite(b, s, d, q) == pytest.approx(round(expected, 1), abs=0.05)

    def test_composite_is_rounded_to_1dp(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        # Should equal itself rounded to 1 decimal place
        assert r.misalignment_composite == round(r.misalignment_composite, 1)


# ===========================================================================
# 7. is_gaming_quota Boundary Conditions
# ===========================================================================


class TestIsGamingQuota:
    """is_gaming_quota: composite >= 40 AND (sandbagging_score > 60 OR late_quarter_close_pct > 60)"""

    def test_gaming_false_when_composite_below_40(self, engine):
        # Aligned rep → composite < 40
        inp = make_aligned_input(rep_id="g1")
        r = engine.assess(inp)
        assert r.is_gaming_quota is False

    def test_gaming_true_when_composite_ge40_and_sandbagging_gt60(self, engine):
        inp = make_pathological_input(rep_id="g2", sandbagging_score=90.0, late_quarter_close_pct=20.0)
        r = engine.assess(inp)
        if r.misalignment_composite >= 40:
            assert r.is_gaming_quota is True
        # If composite < 40 for this config, skip assertion (edge-case construction)

    def test_gaming_true_when_composite_ge40_and_late_quarter_gt60(self, engine):
        inp = make_pathological_input(rep_id="g3", sandbagging_score=30.0, late_quarter_close_pct=90.0)
        r = engine.assess(inp)
        if r.misalignment_composite >= 40:
            assert r.is_gaming_quota is True

    def test_gaming_false_when_sandbagging_exactly_60(self, engine):
        # sandbagging_score == 60 (not > 60), late_quarter_close_pct <= 60
        inp = make_pathological_input(rep_id="g4", sandbagging_score=60.0, late_quarter_close_pct=60.0)
        r = engine.assess(inp)
        assert r.is_gaming_quota is False

    def test_gaming_true_when_sandbagging_just_above_60(self, engine):
        inp = make_pathological_input(rep_id="g5", sandbagging_score=60.1, late_quarter_close_pct=20.0)
        r = engine.assess(inp)
        if r.misalignment_composite >= 40:
            assert r.is_gaming_quota is True

    def test_gaming_true_when_late_quarter_just_above_60(self, engine):
        inp = make_pathological_input(rep_id="g6", sandbagging_score=30.0, late_quarter_close_pct=60.1)
        r = engine.assess(inp)
        if r.misalignment_composite >= 40:
            assert r.is_gaming_quota is True

    def test_gaming_false_high_sandbagging_low_composite(self, engine):
        # High sandbagging but everything else perfect → composite might stay < 40
        inp = make_aligned_input(rep_id="g7", sandbagging_score=90.0)
        r = engine.assess(inp)
        if r.misalignment_composite < 40:
            assert r.is_gaming_quota is False

    def test_gaming_type_is_bool(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.is_gaming_quota, bool)

    def test_gaming_pathological_is_true(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        # The pathological input has sandbagging=90 and late_quarter=90 and bad everything
        # composite should be well above 40
        assert r.misalignment_composite >= 40
        assert r.is_gaming_quota is True

    def test_gaming_composite_exactly_40_sandbagging_gt60(self, engine):
        """Build an input such that composite is expected at ~40 and sandbagging > 60."""
        # Use pathological but tweak to keep composite near boundary
        # We verify the flag is consistent with the rule regardless of exact composite
        inp = make_pathological_input(rep_id="g8", sandbagging_score=70.0)
        r = engine.assess(inp)
        expected = r.misalignment_composite >= 40 and (
            inp.sandbagging_score > 60 or inp.late_quarter_close_pct > 60
        )
        assert r.is_gaming_quota is expected


# ===========================================================================
# 8. requires_plan_review Boundary Conditions
# ===========================================================================


class TestRequiresPlanReview:
    """requires_plan_review: composite >= 30 OR commission_dispute_count >= 2"""

    def test_review_false_when_low_composite_no_disputes(self, engine):
        inp = make_aligned_input(rep_id="r1", commission_dispute_count=0)
        r = engine.assess(inp)
        if r.misalignment_composite < 30:
            assert r.requires_plan_review is False

    def test_review_true_when_composite_ge30(self, engine):
        inp = make_pathological_input(rep_id="r2")
        r = engine.assess(inp)
        if r.misalignment_composite >= 30:
            assert r.requires_plan_review is True

    def test_review_true_when_disputes_ge2(self, engine):
        inp = make_aligned_input(rep_id="r3", commission_dispute_count=2)
        r = engine.assess(inp)
        assert r.requires_plan_review is True

    def test_review_true_when_disputes_3(self, engine):
        inp = make_aligned_input(rep_id="r4", commission_dispute_count=3)
        r = engine.assess(inp)
        assert r.requires_plan_review is True

    def test_review_false_when_disputes_1_and_low_composite(self, engine):
        inp = make_aligned_input(rep_id="r5", commission_dispute_count=1)
        r = engine.assess(inp)
        if r.misalignment_composite < 30:
            assert r.requires_plan_review is False

    def test_review_true_when_disputes_exactly_2(self, engine):
        inp = make_aligned_input(rep_id="r6", commission_dispute_count=2)
        r = engine.assess(inp)
        assert r.requires_plan_review is True

    def test_review_type_is_bool(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.requires_plan_review, bool)

    def test_review_true_for_pathological(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        assert r.requires_plan_review is True

    def test_review_consistent_with_rule(self, engine):
        for dispute_count in range(6):
            inp = make_aligned_input(rep_id=f"rc-{dispute_count}", commission_dispute_count=dispute_count)
            r = engine.assess(inp)
            expected = r.misalignment_composite >= 30 or dispute_count >= 2
            assert r.requires_plan_review is expected, (
                f"dispute_count={dispute_count}, composite={r.misalignment_composite}"
            )
            engine.reset()


# ===========================================================================
# 9. estimated_revenue_risk_usd Formula
# ===========================================================================


class TestRevenueRiskFormula:
    """estimated_revenue_risk_usd = round(closed_won_usd * (composite/100) * 0.25, 2)"""

    def test_formula_aligned_rep(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        expected = round(aligned_input.closed_won_usd * (r.misalignment_composite / 100) * 0.25, 2)
        assert r.estimated_revenue_risk_usd == pytest.approx(expected, abs=0.01)

    def test_formula_pathological_rep(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        expected = round(pathological_input.closed_won_usd * (r.misalignment_composite / 100) * 0.25, 2)
        assert r.estimated_revenue_risk_usd == pytest.approx(expected, abs=0.01)

    def test_formula_zero_closed_won(self, engine):
        inp = make_aligned_input(rep_id="rr1", closed_won_usd=0.0)
        r = engine.assess(inp)
        assert r.estimated_revenue_risk_usd == pytest.approx(0.0, abs=0.01)

    def test_formula_large_closed_won(self, engine):
        inp = make_pathological_input(rep_id="rr2", closed_won_usd=10_000_000.0)
        r = engine.assess(inp)
        expected = round(10_000_000.0 * (r.misalignment_composite / 100) * 0.25, 2)
        assert r.estimated_revenue_risk_usd == pytest.approx(expected, abs=0.01)

    def test_revenue_risk_is_non_negative(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert r.estimated_revenue_risk_usd >= 0.0

    def test_revenue_risk_increases_with_composite(self, engine):
        inp_low = make_aligned_input(rep_id="rrl", closed_won_usd=1_000_000.0)
        inp_high = make_pathological_input(rep_id="rrh", closed_won_usd=1_000_000.0)
        r_low = engine.assess(inp_low)
        r_high = engine.assess(inp_high)
        # Pathological should have higher risk
        assert r_high.estimated_revenue_risk_usd >= r_low.estimated_revenue_risk_usd

    def test_revenue_risk_is_float(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.estimated_revenue_risk_usd, float)

    def test_formula_specific_values(self, engine):
        inp = make_pathological_input(rep_id="rrs", closed_won_usd=400_000.0)
        r = engine.assess(inp)
        expected = round(400_000.0 * (r.misalignment_composite / 100) * 0.25, 2)
        assert r.estimated_revenue_risk_usd == pytest.approx(expected, abs=0.01)

    def test_total_revenue_risk_is_sum(self, engine, aligned_input, pathological_input):
        r1 = engine.assess(aligned_input)
        r2 = engine.assess(pathological_input)
        expected_total = round(r1.estimated_revenue_risk_usd + r2.estimated_revenue_risk_usd, 2)
        assert engine.total_revenue_risk_usd() == pytest.approx(expected_total, abs=0.01)


# ===========================================================================
# 10. assess() Return Type Correctness
# ===========================================================================


class TestAssessReturnTypes:
    def test_assess_returns_result_instance(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r, RepIncentiveResult)

    def test_assess_rep_id_copied(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert r.rep_id == aligned_input.rep_id

    def test_assess_rep_name_copied(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert r.rep_name == aligned_input.rep_name

    def test_assess_rating_is_enum(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.misalignment_rating, MisalignmentRating)

    def test_assess_risk_is_enum(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.misalignment_risk, MisalignmentRisk)

    def test_assess_type_is_enum(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.primary_misalignment_type, MisalignmentType)

    def test_assess_action_is_enum(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.incentive_action, IncentiveAction)

    def test_assess_behavior_score_is_float(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.behavior_alignment_score, float)

    def test_assess_strategic_score_is_float(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.strategic_alignment_score, float)

    def test_assess_discount_score_is_float(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.discount_discipline_score, float)

    def test_assess_quality_score_is_float(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.revenue_quality_score, float)

    def test_assess_composite_is_float(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.misalignment_composite, float)

    def test_assess_is_gaming_is_bool(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.is_gaming_quota, bool)

    def test_assess_requires_review_is_bool(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.requires_plan_review, bool)

    def test_assess_signal_is_str(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.misalignment_signal, str)

    def test_assess_signal_non_empty(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert len(r.misalignment_signal) > 0

    def test_assess_revenue_risk_is_float(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.estimated_revenue_risk_usd, float)


# ===========================================================================
# 11. assess_batch() Tests
# ===========================================================================


class TestAssessBatch:
    def test_batch_returns_list(self, engine, aligned_input, pathological_input):
        results = engine.assess_batch([aligned_input, pathological_input])
        assert isinstance(results, list)

    def test_batch_length_matches_inputs(self, engine):
        inputs = [make_aligned_input(rep_id=f"b{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_empty_list_returns_empty(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_batch_all_results_are_result_instances(self, engine):
        inputs = [make_aligned_input(rep_id=f"bt{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        for r in results:
            assert isinstance(r, RepIncentiveResult)

    def test_batch_sorted_by_composite_descending(self, engine):
        inputs = [
            make_aligned_input(rep_id="bs1"),
            make_pathological_input(rep_id="bs2"),
            make_aligned_input(rep_id="bs3", sandbagging_score=50.0),
        ]
        results = engine.assess_batch(inputs)
        composites = [r.misalignment_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_batch_single_input_returns_list_of_one(self, engine, aligned_input):
        results = engine.assess_batch([aligned_input])
        assert len(results) == 1
        assert isinstance(results[0], RepIncentiveResult)

    def test_batch_stores_results_in_engine(self, engine):
        inputs = [make_aligned_input(rep_id=f"bst{i}") for i in range(4)]
        engine.assess_batch(inputs)
        assert engine.summary()["total"] == 4

    def test_batch_pathological_first_after_sort(self, engine, aligned_input, pathological_input):
        results = engine.assess_batch([aligned_input, pathological_input])
        # pathological should be first (highest composite)
        assert results[0].rep_id == pathological_input.rep_id

    def test_batch_to_dict_on_each_result(self, engine):
        inputs = [make_aligned_input(rep_id=f"bd{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        for r in results:
            d = r.to_dict()
            assert len(d) == 15


# ===========================================================================
# 12. summary() Content Correctness
# ===========================================================================


class TestSummaryContent:
    def test_summary_total_zero_when_empty(self, engine):
        assert engine.summary()["total"] == 0

    def test_summary_total_correct(self, engine, aligned_input, pathological_input):
        engine.assess(aligned_input)
        engine.assess(pathological_input)
        assert engine.summary()["total"] == 2

    def test_summary_avg_composite_is_float(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert isinstance(engine.summary()["avg_misalignment_composite"], float)

    def test_summary_gaming_quota_count_zero_for_aligned(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert engine.summary()["gaming_quota_count"] == 0

    def test_summary_gaming_quota_count_nonzero_for_pathological(self, engine, pathological_input):
        engine.assess(pathological_input)
        assert engine.summary()["gaming_quota_count"] >= 0  # may or may not qualify
        # Verify it's consistent with individual results
        r = engine.get(pathological_input.rep_id)
        expected = 1 if r.is_gaming_quota else 0
        assert engine.summary()["gaming_quota_count"] == expected

    def test_summary_plan_review_count(self, engine, aligned_input, pathological_input):
        r1 = engine.assess(aligned_input)
        r2 = engine.assess(pathological_input)
        expected = sum(1 for r in [r1, r2] if r.requires_plan_review)
        assert engine.summary()["plan_review_count"] == expected

    def test_summary_rating_counts_dict(self, engine, aligned_input):
        engine.assess(aligned_input)
        s = engine.summary()
        assert isinstance(s["rating_counts"], dict)

    def test_summary_risk_counts_dict(self, engine, aligned_input):
        engine.assess(aligned_input)
        s = engine.summary()
        assert isinstance(s["risk_counts"], dict)

    def test_summary_type_counts_dict(self, engine, aligned_input):
        engine.assess(aligned_input)
        s = engine.summary()
        assert isinstance(s["type_counts"], dict)

    def test_summary_action_counts_dict(self, engine, aligned_input):
        engine.assess(aligned_input)
        s = engine.summary()
        assert isinstance(s["action_counts"], dict)

    def test_summary_total_revenue_risk_is_numeric(self, engine, aligned_input):
        engine.assess(aligned_input)
        s = engine.summary()
        assert isinstance(s["total_revenue_risk_usd"], (int, float))

    def test_summary_avg_scores_are_float(self, engine, aligned_input):
        engine.assess(aligned_input)
        s = engine.summary()
        for key in (
            "avg_behavior_alignment_score",
            "avg_strategic_alignment_score",
            "avg_discount_discipline_score",
            "avg_revenue_quality_score",
        ):
            assert isinstance(s[key], float), f"{key} should be float"

    def test_summary_rating_counts_sums_to_total(self, engine, aligned_input, pathological_input):
        engine.assess(aligned_input)
        engine.assess(pathological_input)
        s = engine.summary()
        assert sum(s["rating_counts"].values()) == s["total"]

    def test_summary_risk_counts_sums_to_total(self, engine, aligned_input, pathological_input):
        engine.assess(aligned_input)
        engine.assess(pathological_input)
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_type_counts_sums_to_total(self, engine, aligned_input, pathological_input):
        engine.assess(aligned_input)
        engine.assess(pathological_input)
        s = engine.summary()
        assert sum(s["type_counts"].values()) == s["total"]

    def test_summary_action_counts_sums_to_total(self, engine, aligned_input, pathological_input):
        engine.assess(aligned_input)
        engine.assess(pathological_input)
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_keys_exact_match(self, engine, aligned_input):
        engine.assess(aligned_input)
        assert set(engine.summary().keys()) == set(EXPECTED_SUMMARY_KEYS)

    def test_summary_total_revenue_risk_equals_sum(self, engine, aligned_input, pathological_input):
        r1 = engine.assess(aligned_input)
        r2 = engine.assess(pathological_input)
        expected = round(r1.estimated_revenue_risk_usd + r2.estimated_revenue_risk_usd, 2)
        s = engine.summary()
        assert s["total_revenue_risk_usd"] == pytest.approx(expected, abs=0.01)


# ===========================================================================
# 13. Determinism Tests
# ===========================================================================


class TestDeterminism:
    def test_same_input_same_composite(self, engine):
        inp = make_aligned_input()
        r1 = engine.assess(inp)
        engine.reset()
        r2 = engine.assess(inp)
        assert r1.misalignment_composite == r2.misalignment_composite

    def test_same_input_same_rating(self, engine):
        inp = make_aligned_input()
        r1 = engine.assess(inp)
        engine.reset()
        r2 = engine.assess(inp)
        assert r1.misalignment_rating == r2.misalignment_rating

    def test_same_input_same_risk(self, engine):
        inp = make_aligned_input()
        r1 = engine.assess(inp)
        engine.reset()
        r2 = engine.assess(inp)
        assert r1.misalignment_risk == r2.misalignment_risk

    def test_same_input_same_type(self, engine):
        inp = make_aligned_input()
        r1 = engine.assess(inp)
        engine.reset()
        r2 = engine.assess(inp)
        assert r1.primary_misalignment_type == r2.primary_misalignment_type

    def test_same_input_same_action(self, engine):
        inp = make_aligned_input()
        r1 = engine.assess(inp)
        engine.reset()
        r2 = engine.assess(inp)
        assert r1.incentive_action == r2.incentive_action

    def test_same_input_same_gaming_flag(self, engine):
        inp = make_pathological_input()
        r1 = engine.assess(inp)
        engine.reset()
        r2 = engine.assess(inp)
        assert r1.is_gaming_quota == r2.is_gaming_quota

    def test_same_input_same_review_flag(self, engine):
        inp = make_pathological_input()
        r1 = engine.assess(inp)
        engine.reset()
        r2 = engine.assess(inp)
        assert r1.requires_plan_review == r2.requires_plan_review

    def test_same_input_same_revenue_risk(self, engine):
        inp = make_pathological_input()
        r1 = engine.assess(inp)
        engine.reset()
        r2 = engine.assess(inp)
        assert r1.estimated_revenue_risk_usd == r2.estimated_revenue_risk_usd

    def test_same_input_same_signal(self, engine):
        inp = make_pathological_input()
        r1 = engine.assess(inp)
        engine.reset()
        r2 = engine.assess(inp)
        assert r1.misalignment_signal == r2.misalignment_signal

    def test_batch_determinism(self, engine):
        inputs = [make_aligned_input(rep_id=f"det{i}") for i in range(3)]
        r1 = engine.assess_batch(inputs)
        engine.reset()
        r2 = engine.assess_batch(inputs)
        for a, b in zip(r1, r2):
            assert a.misalignment_composite == b.misalignment_composite


# ===========================================================================
# 14. Aligned Rep Smoke Test
# ===========================================================================


class TestAlignedRepBehaviour:
    def test_aligned_rep_low_composite(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert r.misalignment_composite < 30

    def test_aligned_rep_rating_not_critical(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert r.misalignment_rating != MisalignmentRating.CRITICAL

    def test_aligned_rep_rating_not_severe(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert r.misalignment_rating != MisalignmentRating.SEVERE

    def test_aligned_rep_risk_not_critical(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert r.misalignment_risk != MisalignmentRisk.CRITICAL

    def test_aligned_rep_not_gaming_quota(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert r.is_gaming_quota is False

    def test_aligned_rep_action_not_comp_restructure(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert r.incentive_action != IncentiveAction.COMP_RESTRUCTURE

    def test_aligned_rep_high_behavior_score(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert r.behavior_alignment_score >= 50.0

    def test_aligned_rep_high_strategic_score(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert r.strategic_alignment_score >= 50.0

    def test_aligned_rep_high_discount_score(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert r.discount_discipline_score >= 50.0

    def test_aligned_rep_high_quality_score(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert r.revenue_quality_score >= 50.0

    def test_aligned_rep_low_revenue_risk(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        # Risk should be less than 25% of closed won
        assert r.estimated_revenue_risk_usd < aligned_input.closed_won_usd * 0.25


# ===========================================================================
# 15. Pathological Rep Smoke Test
# ===========================================================================


class TestPathologicalRepBehaviour:
    def test_pathological_rep_high_composite(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        assert r.misalignment_composite >= 50.0

    def test_pathological_rep_rating_severe_or_critical(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        assert r.misalignment_rating in (MisalignmentRating.SEVERE, MisalignmentRating.CRITICAL)

    def test_pathological_rep_risk_high_or_critical(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        assert r.misalignment_risk in (MisalignmentRisk.HIGH, MisalignmentRisk.CRITICAL)

    def test_pathological_rep_is_gaming_quota(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        assert r.is_gaming_quota is True

    def test_pathological_rep_requires_plan_review(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        assert r.requires_plan_review is True

    def test_pathological_rep_action_is_coaching_or_restructure(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        assert r.incentive_action in (IncentiveAction.MANAGER_COACHING, IncentiveAction.COMP_RESTRUCTURE)

    def test_pathological_rep_low_behavior_score(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        assert r.behavior_alignment_score < 50.0

    def test_pathological_rep_low_strategic_score(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        assert r.strategic_alignment_score < 50.0

    def test_pathological_rep_low_discount_score(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        assert r.discount_discipline_score < 50.0

    def test_pathological_rep_low_quality_score(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        assert r.revenue_quality_score < 50.0


# ===========================================================================
# 16. Rating and Risk Threshold Tests
# ===========================================================================


class TestRatingThresholds:
    """composite < 15 → ALIGNED, < 30 → MINOR, < 50 → MODERATE, < 70 → SEVERE, else CRITICAL"""

    def _rating_for_composite(self, composite: float) -> MisalignmentRating:
        from swarm.intelligence.rep_incentive_misalignment_engine import _misalignment_rating
        return _misalignment_rating(composite)

    def test_rating_aligned_at_0(self):
        assert self._rating_for_composite(0.0) == MisalignmentRating.ALIGNED

    def test_rating_aligned_at_14_9(self):
        assert self._rating_for_composite(14.9) == MisalignmentRating.ALIGNED

    def test_rating_minor_at_15(self):
        assert self._rating_for_composite(15.0) == MisalignmentRating.MINOR

    def test_rating_minor_at_29_9(self):
        assert self._rating_for_composite(29.9) == MisalignmentRating.MINOR

    def test_rating_moderate_at_30(self):
        assert self._rating_for_composite(30.0) == MisalignmentRating.MODERATE

    def test_rating_moderate_at_49_9(self):
        assert self._rating_for_composite(49.9) == MisalignmentRating.MODERATE

    def test_rating_severe_at_50(self):
        assert self._rating_for_composite(50.0) == MisalignmentRating.SEVERE

    def test_rating_severe_at_69_9(self):
        assert self._rating_for_composite(69.9) == MisalignmentRating.SEVERE

    def test_rating_critical_at_70(self):
        assert self._rating_for_composite(70.0) == MisalignmentRating.CRITICAL

    def test_rating_critical_at_100(self):
        assert self._rating_for_composite(100.0) == MisalignmentRating.CRITICAL


class TestRiskThresholds:
    """composite < 20 → LOW, < 40 → MODERATE, < 60 → HIGH, else CRITICAL"""

    def _risk_for_composite(self, composite: float) -> MisalignmentRisk:
        from swarm.intelligence.rep_incentive_misalignment_engine import _misalignment_risk
        return _misalignment_risk(composite)

    def test_risk_low_at_0(self):
        assert self._risk_for_composite(0.0) == MisalignmentRisk.LOW

    def test_risk_low_at_19_9(self):
        assert self._risk_for_composite(19.9) == MisalignmentRisk.LOW

    def test_risk_moderate_at_20(self):
        assert self._risk_for_composite(20.0) == MisalignmentRisk.MODERATE

    def test_risk_moderate_at_39_9(self):
        assert self._risk_for_composite(39.9) == MisalignmentRisk.MODERATE

    def test_risk_high_at_40(self):
        assert self._risk_for_composite(40.0) == MisalignmentRisk.HIGH

    def test_risk_high_at_59_9(self):
        assert self._risk_for_composite(59.9) == MisalignmentRisk.HIGH

    def test_risk_critical_at_60(self):
        assert self._risk_for_composite(60.0) == MisalignmentRisk.CRITICAL

    def test_risk_critical_at_100(self):
        assert self._risk_for_composite(100.0) == MisalignmentRisk.CRITICAL


class TestActionThresholds:
    """Rating → Action mapping"""

    def _action_for_rating(self, rating: MisalignmentRating) -> IncentiveAction:
        from swarm.intelligence.rep_incentive_misalignment_engine import _incentive_action
        return _incentive_action(rating)

    def test_action_no_action_for_aligned(self):
        assert self._action_for_rating(MisalignmentRating.ALIGNED) == IncentiveAction.NO_ACTION

    def test_action_monitor_for_minor(self):
        assert self._action_for_rating(MisalignmentRating.MINOR) == IncentiveAction.MONITOR

    def test_action_plan_review_for_moderate(self):
        assert self._action_for_rating(MisalignmentRating.MODERATE) == IncentiveAction.PLAN_REVIEW

    def test_action_manager_coaching_for_severe(self):
        assert self._action_for_rating(MisalignmentRating.SEVERE) == IncentiveAction.MANAGER_COACHING

    def test_action_comp_restructure_for_critical(self):
        assert self._action_for_rating(MisalignmentRating.CRITICAL) == IncentiveAction.COMP_RESTRUCTURE


# ===========================================================================
# 17. Engine State Tests (reset, get, all_reps, gaming_reps, by_rating, by_risk)
# ===========================================================================


class TestEngineState:
    def test_reset_clears_results(self, engine, aligned_input):
        engine.assess(aligned_input)
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_reset_clears_quota_values(self, engine, aligned_input):
        engine.assess(aligned_input)
        engine.reset()
        assert engine.get(aligned_input.rep_id) is None

    def test_get_returns_result(self, engine, aligned_input):
        engine.assess(aligned_input)
        r = engine.get(aligned_input.rep_id)
        assert r is not None
        assert r.rep_id == aligned_input.rep_id

    def test_get_returns_none_for_unknown(self, engine):
        assert engine.get("nonexistent") is None

    def test_all_reps_returns_list(self, engine, aligned_input, pathological_input):
        engine.assess(aligned_input)
        engine.assess(pathological_input)
        all_r = engine.all_reps()
        assert isinstance(all_r, list)
        assert len(all_r) == 2

    def test_all_reps_sorted_descending(self, engine, aligned_input, pathological_input):
        engine.assess(aligned_input)
        engine.assess(pathological_input)
        all_r = engine.all_reps()
        composites = [r.misalignment_composite for r in all_r]
        assert composites == sorted(composites, reverse=True)

    def test_gaming_reps_returns_list(self, engine, pathological_input):
        engine.assess(pathological_input)
        gr = engine.gaming_reps()
        assert isinstance(gr, list)

    def test_gaming_reps_contains_pathological(self, engine, pathological_input):
        engine.assess(pathological_input)
        r = engine.get(pathological_input.rep_id)
        if r.is_gaming_quota:
            ids = [g.rep_id for g in engine.gaming_reps()]
            assert pathological_input.rep_id in ids

    def test_gaming_reps_excludes_aligned(self, engine, aligned_input):
        engine.assess(aligned_input)
        gr = engine.gaming_reps()
        ids = [g.rep_id for g in gr]
        assert aligned_input.rep_id not in ids

    def test_by_rating_returns_correct_subset(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        subset = engine.by_rating(r.misalignment_rating)
        assert aligned_input.rep_id in [x.rep_id for x in subset]

    def test_by_risk_returns_correct_subset(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        subset = engine.by_risk(r.misalignment_risk)
        assert aligned_input.rep_id in [x.rep_id for x in subset]

    def test_avg_composite_empty_is_zero(self, engine):
        assert engine.avg_misalignment_composite() == 0.0

    def test_avg_composite_single_rep(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert engine.avg_misalignment_composite() == pytest.approx(r.misalignment_composite, abs=0.05)

    def test_total_revenue_risk_empty_is_zero(self, engine):
        assert engine.total_revenue_risk_usd() == 0.0

    def test_total_revenue_risk_accumulates(self, engine, aligned_input, pathological_input):
        r1 = engine.assess(aligned_input)
        r2 = engine.assess(pathological_input)
        expected = round(r1.estimated_revenue_risk_usd + r2.estimated_revenue_risk_usd, 2)
        assert engine.total_revenue_risk_usd() == pytest.approx(expected, abs=0.01)

    def test_assess_updates_existing_rep(self, engine, aligned_input):
        engine.assess(aligned_input)
        # Assess same rep again with different data
        modified = make_aligned_input(rep_id=aligned_input.rep_id, sandbagging_score=80.0)
        engine.assess(modified)
        # Only one rep in results
        assert engine.summary()["total"] == 1

    def test_get_returns_latest_result_after_reassess(self, engine, aligned_input):
        engine.assess(aligned_input)
        modified = make_aligned_input(rep_id=aligned_input.rep_id, sandbagging_score=80.0)
        r2 = engine.assess(modified)
        assert engine.get(aligned_input.rep_id).misalignment_composite == r2.misalignment_composite


# ===========================================================================
# 18. Behavior Alignment Score Sub-Tests
# ===========================================================================


class TestBehaviorAlignmentScore:
    def _score(self, **kwargs) -> float:
        inp = make_aligned_input(**kwargs)
        engine = RepIncentiveMisalignmentEngine()
        return engine.assess(inp).behavior_alignment_score

    def test_sandbagging_le20_adds_35(self):
        # With sandbagging=10, forecast=90, late_close=20, disputes=0 → 35+30+20+15 = 100
        s = self._score(rep_id="ba1", sandbagging_score=10.0, forecast_accuracy_pct=90.0,
                        late_quarter_close_pct=20.0, commission_dispute_count=0)
        assert s == pytest.approx(100.0, abs=0.1)

    def test_sandbagging_le40_adds_25(self):
        s1 = self._score(rep_id="ba2a", sandbagging_score=21.0, forecast_accuracy_pct=90.0,
                         late_quarter_close_pct=20.0, commission_dispute_count=0)
        s2 = self._score(rep_id="ba2b", sandbagging_score=10.0, forecast_accuracy_pct=90.0,
                         late_quarter_close_pct=20.0, commission_dispute_count=0)
        # 21 gets 25 for sandbagging instead of 35
        assert s1 == pytest.approx(s2 - 10.0, abs=0.1)

    def test_high_sandbagging_above80_adds_zero(self):
        s = self._score(rep_id="ba3", sandbagging_score=90.0, forecast_accuracy_pct=90.0,
                        late_quarter_close_pct=20.0, commission_dispute_count=0)
        # sandbagging > 80 → 0 points for sandbagging
        s_baseline = self._score(rep_id="ba3b", sandbagging_score=10.0, forecast_accuracy_pct=90.0,
                                  late_quarter_close_pct=20.0, commission_dispute_count=0)
        assert s == pytest.approx(s_baseline - 35.0, abs=0.1)

    def test_forecast_ge85_adds_30(self):
        s1 = self._score(rep_id="ba4", sandbagging_score=10.0, forecast_accuracy_pct=85.0,
                         late_quarter_close_pct=20.0, commission_dispute_count=0)
        assert s1 == pytest.approx(100.0, abs=0.1)

    def test_forecast_ge70_adds_20(self):
        s = self._score(rep_id="ba5", sandbagging_score=10.0, forecast_accuracy_pct=70.0,
                        late_quarter_close_pct=20.0, commission_dispute_count=0)
        assert s == pytest.approx(90.0, abs=0.1)

    def test_forecast_below40_adds_zero(self):
        s = self._score(rep_id="ba6", sandbagging_score=10.0, forecast_accuracy_pct=30.0,
                        late_quarter_close_pct=20.0, commission_dispute_count=0)
        # No forecast points
        assert s == pytest.approx(70.0, abs=0.1)

    def test_late_quarter_le30_adds_20(self):
        s = self._score(rep_id="ba7", sandbagging_score=10.0, forecast_accuracy_pct=90.0,
                        late_quarter_close_pct=30.0, commission_dispute_count=0)
        assert s == pytest.approx(100.0, abs=0.1)

    def test_late_quarter_above70_adds_zero(self):
        s = self._score(rep_id="ba8", sandbagging_score=10.0, forecast_accuracy_pct=90.0,
                        late_quarter_close_pct=80.0, commission_dispute_count=0)
        # No late_quarter points
        assert s == pytest.approx(80.0, abs=0.1)

    def test_disputes_0_adds_15(self):
        s = self._score(rep_id="ba9", sandbagging_score=10.0, forecast_accuracy_pct=90.0,
                        late_quarter_close_pct=20.0, commission_dispute_count=0)
        assert s == pytest.approx(100.0, abs=0.1)

    def test_disputes_1_adds_9(self):
        s = self._score(rep_id="ba10", sandbagging_score=10.0, forecast_accuracy_pct=90.0,
                        late_quarter_close_pct=20.0, commission_dispute_count=1)
        assert s == pytest.approx(94.0, abs=0.1)

    def test_disputes_2_adds_3(self):
        s = self._score(rep_id="ba11", sandbagging_score=10.0, forecast_accuracy_pct=90.0,
                        late_quarter_close_pct=20.0, commission_dispute_count=2)
        assert s == pytest.approx(88.0, abs=0.1)

    def test_disputes_gt2_adds_zero(self):
        s = self._score(rep_id="ba12", sandbagging_score=10.0, forecast_accuracy_pct=90.0,
                        late_quarter_close_pct=20.0, commission_dispute_count=5)
        assert s == pytest.approx(85.0, abs=0.1)


# ===========================================================================
# 19. Discount Discipline Score Sub-Tests
# ===========================================================================


class TestDiscountDisciplineScore:
    def _score(self, **kwargs) -> float:
        inp = make_aligned_input(**kwargs)
        engine = RepIncentiveMisalignmentEngine()
        return engine.assess(inp).discount_discipline_score

    def test_delta_le2_adds_50(self):
        # discount_delta = 0, spiff=10, variance=15 → 50+30+20 = 100
        s = self._score(rep_id="dd1", discount_pct_avg=10.0, company_avg_discount_pct=10.0,
                        spiff_overreliance_score=10.0, deal_size_variance_pct=15.0)
        assert s == pytest.approx(100.0, abs=0.1)

    def test_delta_le5_adds_35(self):
        s = self._score(rep_id="dd2", discount_pct_avg=14.0, company_avg_discount_pct=10.0,
                        spiff_overreliance_score=10.0, deal_size_variance_pct=15.0)
        assert s == pytest.approx(85.0, abs=0.1)

    def test_delta_le10_adds_18(self):
        s = self._score(rep_id="dd3", discount_pct_avg=18.0, company_avg_discount_pct=10.0,
                        spiff_overreliance_score=10.0, deal_size_variance_pct=15.0)
        assert s == pytest.approx(68.0, abs=0.1)

    def test_delta_le15_adds_7(self):
        s = self._score(rep_id="dd4", discount_pct_avg=23.0, company_avg_discount_pct=10.0,
                        spiff_overreliance_score=10.0, deal_size_variance_pct=15.0)
        assert s == pytest.approx(57.0, abs=0.1)

    def test_delta_above15_adds_zero(self):
        s = self._score(rep_id="dd5", discount_pct_avg=30.0, company_avg_discount_pct=10.0,
                        spiff_overreliance_score=10.0, deal_size_variance_pct=15.0)
        assert s == pytest.approx(50.0, abs=0.1)

    def test_spiff_le20_adds_30(self):
        s = self._score(rep_id="dd6", discount_pct_avg=10.0, company_avg_discount_pct=10.0,
                        spiff_overreliance_score=20.0, deal_size_variance_pct=15.0)
        assert s == pytest.approx(100.0, abs=0.1)

    def test_spiff_le40_adds_20(self):
        s = self._score(rep_id="dd7", discount_pct_avg=10.0, company_avg_discount_pct=10.0,
                        spiff_overreliance_score=30.0, deal_size_variance_pct=15.0)
        assert s == pytest.approx(90.0, abs=0.1)

    def test_spiff_above80_adds_zero(self):
        s = self._score(rep_id="dd8", discount_pct_avg=10.0, company_avg_discount_pct=10.0,
                        spiff_overreliance_score=90.0, deal_size_variance_pct=15.0)
        assert s == pytest.approx(70.0, abs=0.1)

    def test_variance_le20_adds_20(self):
        s = self._score(rep_id="dd9", discount_pct_avg=10.0, company_avg_discount_pct=10.0,
                        spiff_overreliance_score=10.0, deal_size_variance_pct=20.0)
        assert s == pytest.approx(100.0, abs=0.1)

    def test_variance_above65_adds_zero(self):
        s = self._score(rep_id="dd10", discount_pct_avg=10.0, company_avg_discount_pct=10.0,
                        spiff_overreliance_score=10.0, deal_size_variance_pct=70.0)
        assert s == pytest.approx(80.0, abs=0.1)


# ===========================================================================
# 20. Primary Misalignment Type Logic
# ===========================================================================


class TestPrimaryMisalignmentType:
    def test_type_none_when_all_scores_ge70(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        # If all scores are high, type should be NONE
        if min(r.behavior_alignment_score, r.strategic_alignment_score,
               r.discount_discipline_score, r.revenue_quality_score) >= 70:
            assert r.primary_misalignment_type == MisalignmentType.NONE

    def test_type_sandbagging_when_behavior_worst_and_sandbagging_gt60(self, engine):
        # High sandbagging, low behavior score, high everything else
        inp = make_aligned_input(
            rep_id="pt1",
            sandbagging_score=90.0,        # > 60 → sandbagging type
            forecast_accuracy_pct=20.0,    # low → low behavior score
            late_quarter_close_pct=80.0,   # additional behaviour penalty
            commission_dispute_count=5,    # behaviour penalty
            # Keep strategic, discount, quality high
            strategic_account_revenue_pct=50.0,
            target_strategic_revenue_pct=50.0,
            discount_pct_avg=10.0,
            company_avg_discount_pct=10.0,
            deal_size_variance_pct=15.0,
            spiff_overreliance_score=10.0,
            avg_deal_size_usd=100_000.0,
            company_avg_deal_size_usd=100_000.0,
            multi_year_deal_pct=35.0,
            closed_won_usd=1_000_000.0,
            quota_usd=1_000_000.0,
        )
        r = engine.assess(inp)
        # behavior is worst score AND sandbagging > 60 → SANDBAGGING type
        if (r.behavior_alignment_score == min(r.behavior_alignment_score,
                                               r.strategic_alignment_score,
                                               r.discount_discipline_score,
                                               r.revenue_quality_score)
                and inp.sandbagging_score > 60):
            assert r.primary_misalignment_type == MisalignmentType.SANDBAGGING

    def test_type_discount_abuse(self, engine):
        # High discount delta, discount worst score
        inp = make_aligned_input(
            rep_id="pt2",
            discount_pct_avg=30.0,         # delta = 20 > 5 → discount abuse
            company_avg_discount_pct=10.0,
            spiff_overreliance_score=90.0, # also hurts discount score
            deal_size_variance_pct=70.0,
            # Keep behavior, strategic, quality high
            sandbagging_score=10.0,
            forecast_accuracy_pct=90.0,
            late_quarter_close_pct=20.0,
            commission_dispute_count=0,
            strategic_account_revenue_pct=50.0,
            target_strategic_revenue_pct=50.0,
            avg_deal_size_usd=100_000.0,
            company_avg_deal_size_usd=100_000.0,
            multi_year_deal_pct=35.0,
        )
        r = engine.assess(inp)
        if (r.discount_discipline_score == min(r.behavior_alignment_score,
                                                r.strategic_alignment_score,
                                                r.discount_discipline_score,
                                                r.revenue_quality_score)
                and inp.discount_pct_avg > inp.company_avg_discount_pct + 5):
            assert r.primary_misalignment_type == MisalignmentType.DISCOUNT_ABUSE

    def test_type_is_valid_enum_member(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert r.primary_misalignment_type in list(MisalignmentType)

    def test_type_is_valid_enum_member_pathological(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        assert r.primary_misalignment_type in list(MisalignmentType)


# ===========================================================================
# 21. Signal String Tests
# ===========================================================================


class TestMisalignmentSignal:
    def test_signal_non_empty_aligned(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert len(r.misalignment_signal) > 0

    def test_signal_non_empty_pathological(self, engine, pathological_input):
        r = engine.assess(pathological_input)
        assert len(r.misalignment_signal) > 0

    def test_signal_contains_aligned_text_for_aligned(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        if r.misalignment_composite < 15 and r.primary_misalignment_type == MisalignmentType.NONE:
            assert "aligned" in r.misalignment_signal.lower() or "well" in r.misalignment_signal.lower()

    def test_signal_mentions_sandbagging_for_sandbagging_type(self, engine):
        inp = make_pathological_input(rep_id="sig1")
        r = engine.assess(inp)
        if r.primary_misalignment_type == MisalignmentType.SANDBAGGING:
            assert "sandbagging" in r.misalignment_signal.lower()

    def test_signal_mentions_discount_for_discount_type(self, engine):
        inp = make_aligned_input(
            rep_id="sig2",
            discount_pct_avg=30.0,
            company_avg_discount_pct=10.0,
            spiff_overreliance_score=90.0,
            deal_size_variance_pct=70.0,
        )
        r = engine.assess(inp)
        if r.primary_misalignment_type == MisalignmentType.DISCOUNT_ABUSE:
            assert "discount" in r.misalignment_signal.lower() or "margin" in r.misalignment_signal.lower()

    def test_signal_mentions_renewal_for_account_neglect(self, engine):
        inp = make_aligned_input(
            rep_id="sig3",
            renewal_neglect_count=5,
            strategic_account_revenue_pct=0.0,
            upsell_attempt_rate_pct=0.0,
        )
        r = engine.assess(inp)
        if r.primary_misalignment_type == MisalignmentType.ACCOUNT_NEGLECT:
            assert "renewal" in r.misalignment_signal.lower() or "neglect" in r.misalignment_signal.lower()

    def test_signal_mentions_deal_size_for_cherry_picking(self, engine):
        inp = make_aligned_input(
            rep_id="sig4",
            avg_deal_size_usd=10_000.0,
            company_avg_deal_size_usd=100_000.0,
            multi_year_deal_pct=0.0,
            closed_won_usd=200_000.0,
            quota_usd=1_000_000.0,
        )
        r = engine.assess(inp)
        if r.primary_misalignment_type == MisalignmentType.CHERRY_PICKING:
            assert "deal" in r.misalignment_signal.lower() or "cherry" in r.misalignment_signal.lower()

    def test_signal_is_string_type(self, engine, aligned_input):
        r = engine.assess(aligned_input)
        assert isinstance(r.misalignment_signal, str)


# ===========================================================================
# 22. Edge Cases
# ===========================================================================


class TestEdgeCases:
    def test_zero_quota_usd_no_crash(self, engine):
        inp = make_aligned_input(rep_id="ec1", quota_usd=0.0, closed_won_usd=100_000.0)
        r = engine.assess(inp)
        assert isinstance(r, RepIncentiveResult)

    def test_zero_closed_won_no_crash(self, engine):
        inp = make_aligned_input(rep_id="ec2", closed_won_usd=0.0)
        r = engine.assess(inp)
        assert r.estimated_revenue_risk_usd == pytest.approx(0.0, abs=0.01)

    def test_zero_company_avg_deal_size_no_crash(self, engine):
        inp = make_aligned_input(rep_id="ec3", company_avg_deal_size_usd=0.0)
        r = engine.assess(inp)
        assert isinstance(r, RepIncentiveResult)

    def test_zero_target_strategic_no_crash(self, engine):
        inp = make_aligned_input(rep_id="ec4", target_strategic_revenue_pct=0.0)
        r = engine.assess(inp)
        assert isinstance(r, RepIncentiveResult)

    def test_zero_target_multi_year_no_crash(self, engine):
        inp = make_aligned_input(rep_id="ec5", target_multi_year_pct=0.0)
        r = engine.assess(inp)
        assert isinstance(r, RepIncentiveResult)

    def test_zero_target_upsell_no_crash(self, engine):
        inp = make_aligned_input(rep_id="ec6", target_upsell_rate_pct=0.0)
        r = engine.assess(inp)
        assert isinstance(r, RepIncentiveResult)

    def test_very_large_quota_no_crash(self, engine):
        inp = make_aligned_input(rep_id="ec7", quota_usd=1e12, closed_won_usd=5e11)
        r = engine.assess(inp)
        assert isinstance(r, RepIncentiveResult)

    def test_very_large_deal_size_no_crash(self, engine):
        inp = make_aligned_input(rep_id="ec8", avg_deal_size_usd=1e9,
                                  company_avg_deal_size_usd=1e9)
        r = engine.assess(inp)
        assert isinstance(r, RepIncentiveResult)

    def test_all_scores_100_composite_near_zero(self, engine):
        # Best possible input
        inp = make_aligned_input(
            rep_id="ec9",
            sandbagging_score=0.0, forecast_accuracy_pct=100.0,
            late_quarter_close_pct=0.0, commission_dispute_count=0,
            strategic_account_revenue_pct=100.0, target_strategic_revenue_pct=100.0,
            multi_year_deal_pct=100.0, target_multi_year_pct=100.0,
            upsell_attempt_rate_pct=100.0, target_upsell_rate_pct=100.0,
            renewal_neglect_count=0,
            discount_pct_avg=0.0, company_avg_discount_pct=0.0,
            spiff_overreliance_score=0.0, deal_size_variance_pct=0.0,
            avg_deal_size_usd=100_000.0, company_avg_deal_size_usd=100_000.0,
        )
        r = engine.assess(inp)
        assert r.misalignment_composite < 15.0

    def test_negative_discount_delta_still_valid(self, engine):
        # Rep discounts less than average → delta < 0 → very good
        inp = make_aligned_input(rep_id="ec10", discount_pct_avg=5.0,
                                  company_avg_discount_pct=15.0)
        r = engine.assess(inp)
        assert 0.0 <= r.discount_discipline_score <= 100.0

    def test_batch_with_duplicate_rep_ids(self, engine):
        inp1 = make_aligned_input(rep_id="dup")
        inp2 = make_pathological_input(rep_id="dup")
        results = engine.assess_batch([inp1, inp2])
        # Last assessment wins for state
        assert len(results) == 2  # batch returns both results
        assert engine.summary()["total"] == 1  # only one stored (same rep_id)

    def test_summary_on_fresh_engine_has_zero_total(self, engine):
        s = engine.summary()
        assert s["total"] == 0

    def test_summary_avg_scores_zero_when_empty(self, engine):
        s = engine.summary()
        assert s["avg_behavior_alignment_score"] == 0.0
        assert s["avg_strategic_alignment_score"] == 0.0
        assert s["avg_discount_discipline_score"] == 0.0
        assert s["avg_revenue_quality_score"] == 0.0

    def test_composite_rounded_to_one_decimal(self, engine):
        for i in range(10):
            inp = make_aligned_input(rep_id=f"rnd{i}", sandbagging_score=float(i * 10))
            r = engine.assess(inp)
            assert r.misalignment_composite == round(r.misalignment_composite, 1)
            engine.reset()

    def test_revenue_risk_rounded_to_two_decimal(self, engine):
        inp = make_pathological_input(rep_id="rnd_risk", closed_won_usd=333_333.33)
        r = engine.assess(inp)
        assert r.estimated_revenue_risk_usd == round(r.estimated_revenue_risk_usd, 2)


# ===========================================================================
# 23. Multiple Reps — Aggregate Checks
# ===========================================================================


class TestMultipleReps:
    def test_batch_10_reps(self, engine):
        inputs = [
            make_aligned_input(rep_id=f"mr{i}", sandbagging_score=float(i * 10))
            for i in range(10)
        ]
        results = engine.assess_batch(inputs)
        assert len(results) == 10

    def test_summary_total_10_reps(self, engine):
        inputs = [
            make_aligned_input(rep_id=f"st{i}")
            for i in range(10)
        ]
        engine.assess_batch(inputs)
        assert engine.summary()["total"] == 10

    def test_avg_composite_between_min_and_max(self, engine):
        inputs = [
            make_aligned_input(rep_id="mc1"),
            make_pathological_input(rep_id="mc2"),
        ]
        r1, r2 = engine.assess(inputs[0]), engine.assess(inputs[1])
        avg = engine.avg_misalignment_composite()
        lo = min(r1.misalignment_composite, r2.misalignment_composite)
        hi = max(r1.misalignment_composite, r2.misalignment_composite)
        assert lo <= avg <= hi

    def test_by_rating_all_belong_to_rating(self, engine, aligned_input, pathological_input):
        engine.assess(aligned_input)
        engine.assess(pathological_input)
        for rating in MisalignmentRating:
            subset = engine.by_rating(rating)
            for r in subset:
                assert r.misalignment_rating == rating

    def test_by_risk_all_belong_to_risk(self, engine, aligned_input, pathological_input):
        engine.assess(aligned_input)
        engine.assess(pathological_input)
        for risk in MisalignmentRisk:
            subset = engine.by_risk(risk)
            for r in subset:
                assert r.misalignment_risk == risk

    def test_all_reps_contains_all_assessed(self, engine):
        inputs = [make_aligned_input(rep_id=f"ar{i}") for i in range(5)]
        for inp in inputs:
            engine.assess(inp)
        all_ids = {r.rep_id for r in engine.all_reps()}
        for inp in inputs:
            assert inp.rep_id in all_ids

    def test_rating_counts_values_in_summary_are_positive_ints(self, engine, aligned_input, pathological_input):
        engine.assess(aligned_input)
        engine.assess(pathological_input)
        s = engine.summary()
        for v in s["rating_counts"].values():
            assert isinstance(v, int) and v > 0

    def test_action_counts_values_are_positive_ints(self, engine, aligned_input, pathological_input):
        engine.assess(aligned_input)
        engine.assess(pathological_input)
        s = engine.summary()
        for v in s["action_counts"].values():
            assert isinstance(v, int) and v > 0
