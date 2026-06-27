"""Comprehensive pytest test suite for SalesForecastSandbaggingDetector.

Covers:
- Enum values and membership
- Input dataclass field count (22 fields)
- Result dataclass field count and to_dict() key count (15 keys)
- Sub-score computation (_forecast_accuracy_score, _pattern_consistency_score,
  _deal_manipulation_score, _over_attainment_score)
- Composite formula: accuracy*0.30 + pattern*0.25 + deal*0.25 + over_attainment*0.20
- Risk / severity / pattern / action classification
- is_sandbagging invariants
- requires_quota_review invariants
- estimated_hidden_pipeline_usd formula
- signal text generation
- assess() integration paths
- assess_batch()
- summary() with 13 keys, empty and populated states
- Edge and boundary cases
"""

from __future__ import annotations

import dataclasses
import math

import pytest

from swarm.intelligence.sales_forecast_sandbagging_detector import (
    SalesForecastSandbaggingDetector,
    SalesForecastSandbaggingInput,
    SandbaggingAction,
    SandbaggingPattern,
    SandbaggingRisk,
    SandbaggingSeverity,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_input(**overrides) -> SalesForecastSandbaggingInput:
    """Return a baseline clean input; override any field via kwargs."""
    defaults = dict(
        rep_id="REP-001",
        region="West",
        forecast_period_id="Q1-2026",
        committed_forecast_usd=100_000.0,
        actual_attained_usd=105_000.0,
        prior_period_over_attainment_pct=105.0,
        avg_quarter_over_attainment_pct=105.0,
        deals_held_from_forecast_count=0,
        late_stage_deals_not_committed_count=0,
        close_date_pushed_past_period_count=0,
        pipeline_coverage_ratio=1.5,
        forecast_submission_days_late=0,
        forecast_change_count=0,
        sandbagged_deal_value_usd=50_000.0,
        avg_deal_size_usd=25_000.0,
        peer_avg_over_attainment_pct=105.0,
        rep_tenure_years=2.0,
        quota_usd=100_000.0,
        manager_override_count=0,
        deal_pull_forward_count=0,
        historical_accuracy_pct=90.0,
        deals_pulled_from_next_period_count=0,
    )
    defaults.update(overrides)
    return SalesForecastSandbaggingInput(**defaults)


def _detector() -> SalesForecastSandbaggingDetector:
    return SalesForecastSandbaggingDetector()


# ---------------------------------------------------------------------------
# 1. Enum: SandbaggingRisk
# ---------------------------------------------------------------------------

class TestSandbaggingRiskEnum:
    def test_low_value(self):
        assert SandbaggingRisk.low.value == "low"

    def test_moderate_value(self):
        assert SandbaggingRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert SandbaggingRisk.high.value == "high"

    def test_critical_value(self):
        assert SandbaggingRisk.critical.value == "critical"

    def test_member_count(self):
        assert len(SandbaggingRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(SandbaggingRisk.low, str)

    def test_str_equality(self):
        assert SandbaggingRisk.moderate == "moderate"


# ---------------------------------------------------------------------------
# 2. Enum: SandbaggingPattern
# ---------------------------------------------------------------------------

class TestSandbaggingPatternEnum:
    def test_none_value(self):
        assert SandbaggingPattern.none.value == "none"

    def test_consistent_low_value(self):
        assert SandbaggingPattern.consistent_low.value == "consistent_low"

    def test_deal_hoarding_value(self):
        assert SandbaggingPattern.deal_hoarding.value == "deal_hoarding"

    def test_late_pushes_value(self):
        assert SandbaggingPattern.late_pushes.value == "late_pushes"

    def test_forecast_delay_value(self):
        assert SandbaggingPattern.forecast_delay.value == "forecast_delay"

    def test_pull_forward_abuse_value(self):
        assert SandbaggingPattern.pull_forward_abuse.value == "pull_forward_abuse"

    def test_member_count(self):
        assert len(SandbaggingPattern) == 6


# ---------------------------------------------------------------------------
# 3. Enum: SandbaggingSeverity
# ---------------------------------------------------------------------------

class TestSandbaggingSeverityEnum:
    def test_clean_value(self):
        assert SandbaggingSeverity.clean.value == "clean"

    def test_watch_value(self):
        assert SandbaggingSeverity.watch.value == "watch"

    def test_suspicious_value(self):
        assert SandbaggingSeverity.suspicious.value == "suspicious"

    def test_confirmed_value(self):
        assert SandbaggingSeverity.confirmed.value == "confirmed"

    def test_member_count(self):
        assert len(SandbaggingSeverity) == 4


# ---------------------------------------------------------------------------
# 4. Enum: SandbaggingAction
# ---------------------------------------------------------------------------

class TestSandbaggingActionEnum:
    def test_no_action_value(self):
        assert SandbaggingAction.no_action.value == "no_action"

    def test_monitor_value(self):
        assert SandbaggingAction.monitor.value == "monitor"

    def test_manager_review_value(self):
        assert SandbaggingAction.manager_review.value == "manager_review"

    def test_quota_recalibrate_value(self):
        assert SandbaggingAction.quota_recalibrate.value == "quota_recalibrate"

    def test_compensation_audit_value(self):
        assert SandbaggingAction.compensation_audit.value == "compensation_audit"

    def test_member_count(self):
        assert len(SandbaggingAction) == 5


# ---------------------------------------------------------------------------
# 5. Input dataclass: exactly 22 fields
# ---------------------------------------------------------------------------

class TestInputDataclass:
    def test_field_count(self):
        fields = dataclasses.fields(SalesForecastSandbaggingInput)
        assert len(fields) == 22

    def test_field_names(self):
        field_names = {f.name for f in dataclasses.fields(SalesForecastSandbaggingInput)}
        expected = {
            "rep_id", "region", "forecast_period_id", "committed_forecast_usd",
            "actual_attained_usd", "prior_period_over_attainment_pct",
            "avg_quarter_over_attainment_pct", "deals_held_from_forecast_count",
            "late_stage_deals_not_committed_count", "close_date_pushed_past_period_count",
            "pipeline_coverage_ratio", "forecast_submission_days_late",
            "forecast_change_count", "sandbagged_deal_value_usd", "avg_deal_size_usd",
            "peer_avg_over_attainment_pct", "rep_tenure_years", "quota_usd",
            "manager_override_count", "deal_pull_forward_count",
            "historical_accuracy_pct", "deals_pulled_from_next_period_count",
        }
        assert field_names == expected

    def test_instantiation(self):
        inp = _make_input()
        assert inp.rep_id == "REP-001"

    def test_rep_id_field(self):
        inp = _make_input(rep_id="REP-999")
        assert inp.rep_id == "REP-999"

    def test_region_field(self):
        inp = _make_input(region="East")
        assert inp.region == "East"

    def test_committed_forecast_usd_field(self):
        inp = _make_input(committed_forecast_usd=200_000.0)
        assert inp.committed_forecast_usd == 200_000.0

    def test_deals_held_from_forecast_count_field(self):
        inp = _make_input(deals_held_from_forecast_count=5)
        assert inp.deals_held_from_forecast_count == 5

    def test_historical_accuracy_pct_field(self):
        inp = _make_input(historical_accuracy_pct=65.0)
        assert inp.historical_accuracy_pct == 65.0


# ---------------------------------------------------------------------------
# 6. to_dict() — exactly 15 keys
# ---------------------------------------------------------------------------

class TestToDict:
    EXPECTED_KEYS = {
        "rep_id", "region", "sandbagging_risk", "sandbagging_pattern",
        "sandbagging_severity", "recommended_action", "forecast_accuracy_score",
        "pattern_consistency_score", "deal_manipulation_score", "over_attainment_score",
        "sandbagging_composite", "is_sandbagging", "requires_quota_review",
        "estimated_hidden_pipeline_usd", "sandbagging_signal",
    }

    def test_key_count(self):
        result = _detector().assess(_make_input())
        assert len(result.to_dict()) == 15

    def test_exact_key_names(self):
        result = _detector().assess(_make_input())
        assert set(result.to_dict().keys()) == self.EXPECTED_KEYS

    def test_rep_id_propagated(self):
        result = _detector().assess(_make_input(rep_id="REP-XYZ"))
        assert result.to_dict()["rep_id"] == "REP-XYZ"

    def test_region_propagated(self):
        result = _detector().assess(_make_input(region="EMEA"))
        assert result.to_dict()["region"] == "EMEA"

    def test_risk_is_string(self):
        d = _detector().assess(_make_input()).to_dict()
        assert isinstance(d["sandbagging_risk"], str)

    def test_pattern_is_string(self):
        d = _detector().assess(_make_input()).to_dict()
        assert isinstance(d["sandbagging_pattern"], str)

    def test_severity_is_string(self):
        d = _detector().assess(_make_input()).to_dict()
        assert isinstance(d["sandbagging_severity"], str)

    def test_action_is_string(self):
        d = _detector().assess(_make_input()).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_is_sandbagging_is_bool(self):
        d = _detector().assess(_make_input()).to_dict()
        assert isinstance(d["is_sandbagging"], bool)

    def test_requires_quota_review_is_bool(self):
        d = _detector().assess(_make_input()).to_dict()
        assert isinstance(d["requires_quota_review"], bool)

    def test_scores_rounded_to_1dp(self):
        d = _detector().assess(_make_input()).to_dict()
        for key in ("forecast_accuracy_score", "pattern_consistency_score",
                    "deal_manipulation_score", "over_attainment_score",
                    "sandbagging_composite"):
            val = d[key]
            assert round(val, 1) == val

    def test_estimated_hidden_pipeline_rounded_to_2dp(self):
        d = _detector().assess(_make_input()).to_dict()
        val = d["estimated_hidden_pipeline_usd"]
        assert round(val, 2) == val

    def test_sandbagging_signal_is_str(self):
        d = _detector().assess(_make_input()).to_dict()
        assert isinstance(d["sandbagging_signal"], str)


# ---------------------------------------------------------------------------
# 7. _forecast_accuracy_score
# ---------------------------------------------------------------------------

class TestForecastAccuracyScore:
    """Test each branch of the accuracy sub-score."""

    def _score(self, **kw) -> float:
        det = _detector()
        return det._forecast_accuracy_score(_make_input(**kw))

    # attainment ratio branches
    def test_ratio_below_125_no_attainment_points(self):
        s = self._score(committed_forecast_usd=100_000, actual_attained_usd=110_000,
                        historical_accuracy_pct=90, forecast_submission_days_late=0)
        assert s == 0.0

    def test_ratio_exactly_125_gives_12(self):
        s = self._score(committed_forecast_usd=100_000, actual_attained_usd=125_000,
                        historical_accuracy_pct=90, forecast_submission_days_late=0)
        assert s == 12.0

    def test_ratio_between_125_and_150_gives_12(self):
        s = self._score(committed_forecast_usd=100_000, actual_attained_usd=140_000,
                        historical_accuracy_pct=90, forecast_submission_days_late=0)
        assert s == 12.0

    def test_ratio_exactly_150_gives_25(self):
        s = self._score(committed_forecast_usd=100_000, actual_attained_usd=150_000,
                        historical_accuracy_pct=90, forecast_submission_days_late=0)
        assert s == 25.0

    def test_ratio_between_150_and_175_gives_25(self):
        s = self._score(committed_forecast_usd=100_000, actual_attained_usd=160_000,
                        historical_accuracy_pct=90, forecast_submission_days_late=0)
        assert s == 25.0

    def test_ratio_exactly_175_gives_38(self):
        s = self._score(committed_forecast_usd=100_000, actual_attained_usd=175_000,
                        historical_accuracy_pct=90, forecast_submission_days_late=0)
        assert s == 38.0

    def test_ratio_between_175_and_200_gives_38(self):
        s = self._score(committed_forecast_usd=100_000, actual_attained_usd=190_000,
                        historical_accuracy_pct=90, forecast_submission_days_late=0)
        assert s == 38.0

    def test_ratio_exactly_200_gives_50(self):
        s = self._score(committed_forecast_usd=100_000, actual_attained_usd=200_000,
                        historical_accuracy_pct=90, forecast_submission_days_late=0)
        assert s == 50.0

    def test_ratio_above_200_gives_50(self):
        s = self._score(committed_forecast_usd=100_000, actual_attained_usd=300_000,
                        historical_accuracy_pct=90, forecast_submission_days_late=0)
        assert s == 50.0

    def test_zero_committed_no_attainment_points(self):
        s = self._score(committed_forecast_usd=0, actual_attained_usd=200_000,
                        historical_accuracy_pct=90, forecast_submission_days_late=0)
        assert s == 0.0

    # historical accuracy branches
    def test_historical_accuracy_below_70_adds_10(self):
        s = self._score(committed_forecast_usd=0, actual_attained_usd=0,
                        historical_accuracy_pct=65, forecast_submission_days_late=0)
        assert s == 10.0

    def test_historical_accuracy_exactly_70_adds_5(self):
        s = self._score(committed_forecast_usd=0, actual_attained_usd=0,
                        historical_accuracy_pct=70, forecast_submission_days_late=0)
        assert s == 5.0

    def test_historical_accuracy_between_70_and_80_adds_5(self):
        s = self._score(committed_forecast_usd=0, actual_attained_usd=0,
                        historical_accuracy_pct=75, forecast_submission_days_late=0)
        assert s == 5.0

    def test_historical_accuracy_80_and_above_adds_0(self):
        s = self._score(committed_forecast_usd=0, actual_attained_usd=0,
                        historical_accuracy_pct=80, forecast_submission_days_late=0)
        assert s == 0.0

    def test_historical_accuracy_100_adds_0(self):
        s = self._score(committed_forecast_usd=0, actual_attained_usd=0,
                        historical_accuracy_pct=100, forecast_submission_days_late=0)
        assert s == 0.0

    # submission days late branches
    def test_days_late_0_adds_0(self):
        s = self._score(committed_forecast_usd=0, actual_attained_usd=0,
                        historical_accuracy_pct=90, forecast_submission_days_late=0)
        assert s == 0.0

    def test_days_late_1_adds_0(self):
        s = self._score(committed_forecast_usd=0, actual_attained_usd=0,
                        historical_accuracy_pct=90, forecast_submission_days_late=1)
        assert s == 0.0

    def test_days_late_exactly_2_adds_10(self):
        s = self._score(committed_forecast_usd=0, actual_attained_usd=0,
                        historical_accuracy_pct=90, forecast_submission_days_late=2)
        assert s == 10.0

    def test_days_late_4_adds_10(self):
        s = self._score(committed_forecast_usd=0, actual_attained_usd=0,
                        historical_accuracy_pct=90, forecast_submission_days_late=4)
        assert s == 10.0

    def test_days_late_exactly_5_adds_20(self):
        s = self._score(committed_forecast_usd=0, actual_attained_usd=0,
                        historical_accuracy_pct=90, forecast_submission_days_late=5)
        assert s == 20.0

    def test_days_late_10_adds_20(self):
        s = self._score(committed_forecast_usd=0, actual_attained_usd=0,
                        historical_accuracy_pct=90, forecast_submission_days_late=10)
        assert s == 20.0

    def test_score_clamped_at_100(self):
        s = self._score(committed_forecast_usd=100_000, actual_attained_usd=300_000,
                        historical_accuracy_pct=65, forecast_submission_days_late=10)
        assert s == 80.0

    def test_score_never_negative(self):
        s = self._score(committed_forecast_usd=0, actual_attained_usd=0,
                        historical_accuracy_pct=100, forecast_submission_days_late=0)
        assert s >= 0.0

    def test_combined_max_without_clamping(self):
        # 50 + 10 + 20 = 80 < 100 so not clamped
        s = self._score(committed_forecast_usd=100_000, actual_attained_usd=300_000,
                        historical_accuracy_pct=65, forecast_submission_days_late=10)
        assert s == 80.0


# ---------------------------------------------------------------------------
# 8. _pattern_consistency_score
# ---------------------------------------------------------------------------

class TestPatternConsistencyScore:
    def _score(self, **kw) -> float:
        return _detector()._pattern_consistency_score(_make_input(**kw))

    def test_avg_overattainment_below_120_no_points(self):
        s = self._score(avg_quarter_over_attainment_pct=100,
                        peer_avg_over_attainment_pct=100, manager_override_count=0)
        assert s == 0.0

    def test_avg_overattainment_exactly_120_gives_18(self):
        s = self._score(avg_quarter_over_attainment_pct=120,
                        peer_avg_over_attainment_pct=0, manager_override_count=0)
        assert s == 18.0

    def test_avg_overattainment_130_gives_18(self):
        s = self._score(avg_quarter_over_attainment_pct=130,
                        peer_avg_over_attainment_pct=0, manager_override_count=0)
        assert s == 18.0

    def test_avg_overattainment_exactly_140_gives_32(self):
        s = self._score(avg_quarter_over_attainment_pct=140,
                        peer_avg_over_attainment_pct=0, manager_override_count=0)
        assert s == 32.0

    def test_avg_overattainment_150_gives_32(self):
        s = self._score(avg_quarter_over_attainment_pct=150,
                        peer_avg_over_attainment_pct=0, manager_override_count=0)
        assert s == 32.0

    def test_avg_overattainment_exactly_160_gives_45(self):
        s = self._score(avg_quarter_over_attainment_pct=160,
                        peer_avg_over_attainment_pct=0, manager_override_count=0)
        assert s == 45.0

    def test_avg_overattainment_200_gives_45(self):
        s = self._score(avg_quarter_over_attainment_pct=200,
                        peer_avg_over_attainment_pct=0, manager_override_count=0)
        assert s == 45.0

    # peer outperformance branches
    def test_delta_below_15_no_peer_points(self):
        s = self._score(avg_quarter_over_attainment_pct=100,
                        peer_avg_over_attainment_pct=90, manager_override_count=0)
        assert s == 0.0

    def test_delta_exactly_15_adds_8(self):
        s = self._score(avg_quarter_over_attainment_pct=115,
                        peer_avg_over_attainment_pct=100, manager_override_count=0)
        assert s == 8.0

    def test_delta_20_adds_8(self):
        s = self._score(avg_quarter_over_attainment_pct=120,
                        peer_avg_over_attainment_pct=100, manager_override_count=0)
        # 18 (from avg tier) + 8 (from delta)
        assert s == 26.0

    def test_delta_exactly_30_adds_18(self):
        s = self._score(avg_quarter_over_attainment_pct=130,
                        peer_avg_over_attainment_pct=100, manager_override_count=0)
        # 18 (avg tier) + 18 (delta)
        assert s == 36.0

    def test_delta_exactly_50_adds_30(self):
        s = self._score(avg_quarter_over_attainment_pct=150,
                        peer_avg_over_attainment_pct=100, manager_override_count=0)
        # 32 (avg tier) + 30 (delta)
        assert s == 62.0

    def test_zero_peer_avg_no_peer_points(self):
        s = self._score(avg_quarter_over_attainment_pct=200,
                        peer_avg_over_attainment_pct=0, manager_override_count=0)
        assert s == 45.0

    # manager override branches
    def test_override_0_no_points(self):
        s = self._score(avg_quarter_over_attainment_pct=100,
                        peer_avg_over_attainment_pct=0, manager_override_count=0)
        assert s == 0.0

    def test_override_1_adds_12(self):
        s = self._score(avg_quarter_over_attainment_pct=100,
                        peer_avg_over_attainment_pct=0, manager_override_count=1)
        assert s == 12.0

    def test_override_2_adds_12(self):
        s = self._score(avg_quarter_over_attainment_pct=100,
                        peer_avg_over_attainment_pct=0, manager_override_count=2)
        assert s == 12.0

    def test_override_3_adds_25(self):
        s = self._score(avg_quarter_over_attainment_pct=100,
                        peer_avg_over_attainment_pct=0, manager_override_count=3)
        assert s == 25.0

    def test_override_5_adds_25(self):
        s = self._score(avg_quarter_over_attainment_pct=100,
                        peer_avg_over_attainment_pct=0, manager_override_count=5)
        assert s == 25.0

    def test_score_clamped_at_100(self):
        s = self._score(avg_quarter_over_attainment_pct=200,
                        peer_avg_over_attainment_pct=100, manager_override_count=5)
        # 45 + 30 + 25 = 100 → clamped at 100
        assert s == 100.0

    def test_score_never_negative(self):
        s = self._score(avg_quarter_over_attainment_pct=50,
                        peer_avg_over_attainment_pct=200, manager_override_count=0)
        assert s >= 0.0


# ---------------------------------------------------------------------------
# 9. _deal_manipulation_score
# ---------------------------------------------------------------------------

class TestDealManipulationScore:
    def _score(self, **kw) -> float:
        return _detector()._deal_manipulation_score(_make_input(**kw))

    # deals_held branches
    def test_held_0_no_points(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s == 0.0

    def test_held_1_adds_15(self):
        s = self._score(deals_held_from_forecast_count=1,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s == 15.0

    def test_held_2_adds_15(self):
        s = self._score(deals_held_from_forecast_count=2,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s == 15.0

    def test_held_3_adds_30(self):
        s = self._score(deals_held_from_forecast_count=3,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s == 30.0

    def test_held_4_adds_30(self):
        s = self._score(deals_held_from_forecast_count=4,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s == 30.0

    def test_held_5_adds_45(self):
        s = self._score(deals_held_from_forecast_count=5,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s == 45.0

    def test_held_10_adds_45(self):
        s = self._score(deals_held_from_forecast_count=10,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s == 45.0

    # late_stage branches
    def test_late_stage_0_no_points(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s == 0.0

    def test_late_stage_1_adds_8(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=1,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s == 8.0

    def test_late_stage_2_adds_18(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=2,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s == 18.0

    def test_late_stage_3_adds_18(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=3,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s == 18.0

    def test_late_stage_4_adds_30(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=4,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s == 30.0

    def test_late_stage_10_adds_30(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=10,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s == 30.0

    # close date pushed branches
    def test_pushed_0_no_points(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s == 0.0

    def test_pushed_1_adds_10(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=1,
                        deal_pull_forward_count=0)
        assert s == 10.0

    def test_pushed_2_adds_10(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=2,
                        deal_pull_forward_count=0)
        assert s == 10.0

    def test_pushed_3_adds_20(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=3,
                        deal_pull_forward_count=0)
        assert s == 20.0

    def test_pushed_10_adds_20(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=10,
                        deal_pull_forward_count=0)
        assert s == 20.0

    # pull_forward branches
    def test_pull_forward_below_3_no_points(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=2)
        assert s == 0.0

    def test_pull_forward_3_adds_10(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=3)
        assert s == 10.0

    def test_pull_forward_10_adds_10(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=10)
        assert s == 10.0

    def test_score_clamped_at_100(self):
        s = self._score(deals_held_from_forecast_count=5,
                        late_stage_deals_not_committed_count=4,
                        close_date_pushed_past_period_count=3,
                        deal_pull_forward_count=3)
        # 45 + 30 + 20 + 10 = 105 → clamped to 100
        assert s == 100.0

    def test_score_never_negative(self):
        s = self._score(deals_held_from_forecast_count=0,
                        late_stage_deals_not_committed_count=0,
                        close_date_pushed_past_period_count=0,
                        deal_pull_forward_count=0)
        assert s >= 0.0


# ---------------------------------------------------------------------------
# 10. _over_attainment_score
# ---------------------------------------------------------------------------

class TestOverAttainmentScore:
    def _score(self, **kw) -> float:
        return _detector()._over_attainment_score(_make_input(**kw))

    # prior_period branches
    def test_prior_below_125_no_points(self):
        s = self._score(prior_period_over_attainment_pct=100,
                        pipeline_coverage_ratio=1.0, quota_usd=100_000,
                        committed_forecast_usd=100_000,
                        deals_pulled_from_next_period_count=0)
        assert s == 0.0

    def test_prior_exactly_125_adds_12(self):
        s = self._score(prior_period_over_attainment_pct=125,
                        pipeline_coverage_ratio=1.0, quota_usd=100_000,
                        committed_forecast_usd=100_000,
                        deals_pulled_from_next_period_count=0)
        assert s == 12.0

    def test_prior_140_adds_12(self):
        s = self._score(prior_period_over_attainment_pct=140,
                        pipeline_coverage_ratio=1.0, quota_usd=100_000,
                        committed_forecast_usd=100_000,
                        deals_pulled_from_next_period_count=0)
        assert s == 12.0

    def test_prior_exactly_150_adds_25(self):
        s = self._score(prior_period_over_attainment_pct=150,
                        pipeline_coverage_ratio=1.0, quota_usd=100_000,
                        committed_forecast_usd=100_000,
                        deals_pulled_from_next_period_count=0)
        assert s == 25.0

    def test_prior_160_adds_25(self):
        s = self._score(prior_period_over_attainment_pct=160,
                        pipeline_coverage_ratio=1.0, quota_usd=100_000,
                        committed_forecast_usd=100_000,
                        deals_pulled_from_next_period_count=0)
        assert s == 25.0

    def test_prior_exactly_175_adds_38(self):
        s = self._score(prior_period_over_attainment_pct=175,
                        pipeline_coverage_ratio=1.0, quota_usd=100_000,
                        committed_forecast_usd=100_000,
                        deals_pulled_from_next_period_count=0)
        assert s == 38.0

    def test_prior_190_adds_38(self):
        s = self._score(prior_period_over_attainment_pct=190,
                        pipeline_coverage_ratio=1.0, quota_usd=100_000,
                        committed_forecast_usd=100_000,
                        deals_pulled_from_next_period_count=0)
        assert s == 38.0

    def test_prior_exactly_200_adds_50(self):
        s = self._score(prior_period_over_attainment_pct=200,
                        pipeline_coverage_ratio=1.0, quota_usd=100_000,
                        committed_forecast_usd=100_000,
                        deals_pulled_from_next_period_count=0)
        assert s == 50.0

    def test_prior_250_adds_50(self):
        s = self._score(prior_period_over_attainment_pct=250,
                        pipeline_coverage_ratio=1.0, quota_usd=100_000,
                        committed_forecast_usd=100_000,
                        deals_pulled_from_next_period_count=0)
        assert s == 50.0

    # pipeline coverage + commitment branches
    def test_high_coverage_low_commitment_adds_30(self):
        # coverage >= 4.0 and coverage_vs_commitment < 0.8
        s = self._score(prior_period_over_attainment_pct=100,
                        pipeline_coverage_ratio=4.0, quota_usd=100_000,
                        committed_forecast_usd=70_000,  # 0.7 < 0.8
                        deals_pulled_from_next_period_count=0)
        assert s == 30.0

    def test_moderate_coverage_low_commitment_adds_18(self):
        # coverage >= 3.0 and coverage_vs_commitment < 0.9
        s = self._score(prior_period_over_attainment_pct=100,
                        pipeline_coverage_ratio=3.0, quota_usd=100_000,
                        committed_forecast_usd=80_000,  # 0.8 < 0.9
                        deals_pulled_from_next_period_count=0)
        assert s == 18.0

    def test_high_coverage_high_commitment_no_extra_points(self):
        # coverage >= 4.0 but commitment >= 0.8 so no bonus
        s = self._score(prior_period_over_attainment_pct=100,
                        pipeline_coverage_ratio=4.0, quota_usd=100_000,
                        committed_forecast_usd=90_000,  # 0.9 >= 0.8
                        deals_pulled_from_next_period_count=0)
        assert s == 0.0

    def test_zero_quota_no_coverage_points(self):
        s = self._score(prior_period_over_attainment_pct=100,
                        pipeline_coverage_ratio=5.0, quota_usd=0,
                        committed_forecast_usd=0,
                        deals_pulled_from_next_period_count=0)
        assert s == 0.0

    # deals_pulled_from_next_period branches
    def test_pulled_next_0_no_points(self):
        s = self._score(prior_period_over_attainment_pct=100,
                        pipeline_coverage_ratio=1.0, quota_usd=100_000,
                        committed_forecast_usd=100_000,
                        deals_pulled_from_next_period_count=0)
        assert s == 0.0

    def test_pulled_next_1_adds_10(self):
        s = self._score(prior_period_over_attainment_pct=100,
                        pipeline_coverage_ratio=1.0, quota_usd=100_000,
                        committed_forecast_usd=100_000,
                        deals_pulled_from_next_period_count=1)
        assert s == 10.0

    def test_pulled_next_2_adds_10(self):
        s = self._score(prior_period_over_attainment_pct=100,
                        pipeline_coverage_ratio=1.0, quota_usd=100_000,
                        committed_forecast_usd=100_000,
                        deals_pulled_from_next_period_count=2)
        assert s == 10.0

    def test_pulled_next_3_adds_20(self):
        s = self._score(prior_period_over_attainment_pct=100,
                        pipeline_coverage_ratio=1.0, quota_usd=100_000,
                        committed_forecast_usd=100_000,
                        deals_pulled_from_next_period_count=3)
        assert s == 20.0

    def test_score_clamped_at_100(self):
        s = self._score(prior_period_over_attainment_pct=200,
                        pipeline_coverage_ratio=4.0, quota_usd=100_000,
                        committed_forecast_usd=50_000,
                        deals_pulled_from_next_period_count=3)
        # 50 + 30 + 20 = 100 → exactly 100
        assert s == 100.0

    def test_score_never_negative(self):
        s = self._score(prior_period_over_attainment_pct=50,
                        pipeline_coverage_ratio=0.5, quota_usd=100_000,
                        committed_forecast_usd=100_000,
                        deals_pulled_from_next_period_count=0)
        assert s >= 0.0


# ---------------------------------------------------------------------------
# 11. Composite formula
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_composite_formula_exact(self):
        det = _detector()
        inp = _make_input()
        acc = det._forecast_accuracy_score(inp)
        pat = det._pattern_consistency_score(inp)
        deal = det._deal_manipulation_score(inp)
        over = det._over_attainment_score(inp)
        expected = round(min(100.0, max(0.0, acc * 0.30 + pat * 0.25 + deal * 0.25 + over * 0.20)), 1)
        result = det.assess(inp)
        assert result.sandbagging_composite == expected

    def test_composite_weights_sum_to_1(self):
        # verify weights: 0.30 + 0.25 + 0.25 + 0.20 == 1.00
        assert math.isclose(0.30 + 0.25 + 0.25 + 0.20, 1.0)

    def test_composite_zero_inputs_is_zero(self):
        inp = _make_input(
            committed_forecast_usd=0, actual_attained_usd=0,
            historical_accuracy_pct=90, forecast_submission_days_late=0,
            avg_quarter_over_attainment_pct=100, peer_avg_over_attainment_pct=0,
            manager_override_count=0, deals_held_from_forecast_count=0,
            late_stage_deals_not_committed_count=0, close_date_pushed_past_period_count=0,
            deal_pull_forward_count=0, prior_period_over_attainment_pct=100,
            pipeline_coverage_ratio=1.0, quota_usd=100_000,
            deals_pulled_from_next_period_count=0,
        )
        result = _detector().assess(inp)
        assert result.sandbagging_composite == 0.0

    def test_composite_clamped_to_100(self):
        # All sub-scores maxed
        inp = _make_input(
            committed_forecast_usd=50_000, actual_attained_usd=300_000,
            historical_accuracy_pct=60, forecast_submission_days_late=10,
            avg_quarter_over_attainment_pct=200, peer_avg_over_attainment_pct=100,
            manager_override_count=5,
            deals_held_from_forecast_count=10, late_stage_deals_not_committed_count=10,
            close_date_pushed_past_period_count=10, deal_pull_forward_count=10,
            prior_period_over_attainment_pct=250,
            pipeline_coverage_ratio=5.0, quota_usd=100_000,
            deals_pulled_from_next_period_count=10,
        )
        result = _detector().assess(inp)
        assert result.sandbagging_composite <= 100.0

    def test_composite_never_negative(self):
        result = _detector().assess(_make_input())
        assert result.sandbagging_composite >= 0.0

    def test_composite_reflects_all_four_sub_scores(self):
        det = _detector()
        inp = _make_input(
            committed_forecast_usd=100_000, actual_attained_usd=200_000,  # +50 acc
            historical_accuracy_pct=90, forecast_submission_days_late=0,
            avg_quarter_over_attainment_pct=100, peer_avg_over_attainment_pct=0,
            manager_override_count=0, deals_held_from_forecast_count=0,
            late_stage_deals_not_committed_count=0, close_date_pushed_past_period_count=0,
            deal_pull_forward_count=0, prior_period_over_attainment_pct=100,
            pipeline_coverage_ratio=1.0, quota_usd=100_000,
            deals_pulled_from_next_period_count=0,
        )
        result = det.assess(inp)
        # accuracy=50, pattern=0, deal=0, over=0 → composite = 50*0.30 = 15
        assert result.sandbagging_composite == 15.0


# ---------------------------------------------------------------------------
# 12. Risk classification
# ---------------------------------------------------------------------------

class TestClassifyRisk:
    def _risk(self, composite: float) -> SandbaggingRisk:
        det = _detector()
        return det._classify_risk(composite)

    def test_below_20_is_low(self):
        assert self._risk(0.0) == SandbaggingRisk.low

    def test_exactly_0_is_low(self):
        assert self._risk(0.0) == SandbaggingRisk.low

    def test_19_is_low(self):
        assert self._risk(19.9) == SandbaggingRisk.low

    def test_exactly_20_is_moderate(self):
        assert self._risk(20.0) == SandbaggingRisk.moderate

    def test_30_is_moderate(self):
        assert self._risk(30.0) == SandbaggingRisk.moderate

    def test_39_is_moderate(self):
        assert self._risk(39.9) == SandbaggingRisk.moderate

    def test_exactly_40_is_high(self):
        assert self._risk(40.0) == SandbaggingRisk.high

    def test_50_is_high(self):
        assert self._risk(50.0) == SandbaggingRisk.high

    def test_59_is_high(self):
        assert self._risk(59.9) == SandbaggingRisk.high

    def test_exactly_60_is_critical(self):
        assert self._risk(60.0) == SandbaggingRisk.critical

    def test_100_is_critical(self):
        assert self._risk(100.0) == SandbaggingRisk.critical


# ---------------------------------------------------------------------------
# 13. Severity classification
# ---------------------------------------------------------------------------

class TestClassifySeverity:
    def _sev(self, composite: float) -> SandbaggingSeverity:
        return _detector()._classify_severity(composite)

    def test_below_20_is_clean(self):
        assert self._sev(0.0) == SandbaggingSeverity.clean

    def test_19_is_clean(self):
        assert self._sev(19.9) == SandbaggingSeverity.clean

    def test_exactly_20_is_watch(self):
        assert self._sev(20.0) == SandbaggingSeverity.watch

    def test_30_is_watch(self):
        assert self._sev(30.0) == SandbaggingSeverity.watch

    def test_39_is_watch(self):
        assert self._sev(39.9) == SandbaggingSeverity.watch

    def test_exactly_40_is_suspicious(self):
        assert self._sev(40.0) == SandbaggingSeverity.suspicious

    def test_50_is_suspicious(self):
        assert self._sev(50.0) == SandbaggingSeverity.suspicious

    def test_59_is_suspicious(self):
        assert self._sev(59.9) == SandbaggingSeverity.suspicious

    def test_exactly_60_is_confirmed(self):
        assert self._sev(60.0) == SandbaggingSeverity.confirmed

    def test_100_is_confirmed(self):
        assert self._sev(100.0) == SandbaggingSeverity.confirmed


# ---------------------------------------------------------------------------
# 14. Pattern classification
# ---------------------------------------------------------------------------

class TestClassifyPattern:
    def _pattern(self, **kw) -> SandbaggingPattern:
        det = _detector()
        inp = _make_input(**kw)
        acc = det._forecast_accuracy_score(inp)
        pat = det._pattern_consistency_score(inp)
        deal = det._deal_manipulation_score(inp)
        return det._classify_pattern(inp, acc, pat, deal)

    def test_all_zeros_is_none(self):
        p = self._pattern(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=0,
            deal_pull_forward_count=0,
            avg_quarter_over_attainment_pct=100,
        )
        assert p == SandbaggingPattern.none

    def test_3_held_deals_is_deal_hoarding(self):
        p = self._pattern(deals_held_from_forecast_count=3)
        assert p == SandbaggingPattern.deal_hoarding

    def test_5_held_deals_is_deal_hoarding(self):
        p = self._pattern(deals_held_from_forecast_count=5)
        assert p == SandbaggingPattern.deal_hoarding

    def test_deal_hoarding_takes_priority_over_late_pushes(self):
        p = self._pattern(
            deals_held_from_forecast_count=3,
            close_date_pushed_past_period_count=3,
        )
        assert p == SandbaggingPattern.deal_hoarding

    def test_3_close_pushed_is_late_pushes(self):
        p = self._pattern(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=3,
        )
        assert p == SandbaggingPattern.late_pushes

    def test_late_pushes_takes_priority_over_forecast_delay(self):
        p = self._pattern(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=3,
            forecast_submission_days_late=5,
        )
        assert p == SandbaggingPattern.late_pushes

    def test_3_days_late_is_forecast_delay(self):
        p = self._pattern(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=3,
        )
        assert p == SandbaggingPattern.forecast_delay

    def test_5_days_late_is_forecast_delay(self):
        p = self._pattern(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=5,
        )
        assert p == SandbaggingPattern.forecast_delay

    def test_forecast_delay_takes_priority_over_pull_forward(self):
        p = self._pattern(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=3,
            deal_pull_forward_count=3,
        )
        assert p == SandbaggingPattern.forecast_delay

    def test_3_pull_forward_is_pull_forward_abuse(self):
        p = self._pattern(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=0,
            deal_pull_forward_count=3,
        )
        assert p == SandbaggingPattern.pull_forward_abuse

    def test_pull_forward_takes_priority_over_consistent_low(self):
        p = self._pattern(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=0,
            deal_pull_forward_count=3,
            avg_quarter_over_attainment_pct=200,
        )
        assert p == SandbaggingPattern.pull_forward_abuse

    def test_avg_overattainment_140_is_consistent_low(self):
        p = self._pattern(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=0,
            deal_pull_forward_count=0,
            avg_quarter_over_attainment_pct=140,
        )
        assert p == SandbaggingPattern.consistent_low

    def test_avg_overattainment_139_is_none(self):
        p = self._pattern(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=0,
            deal_pull_forward_count=0,
            avg_quarter_over_attainment_pct=139,
        )
        assert p == SandbaggingPattern.none

    def test_2_held_deals_is_not_deal_hoarding(self):
        p = self._pattern(deals_held_from_forecast_count=2)
        assert p != SandbaggingPattern.deal_hoarding

    def test_2_pushed_is_not_late_pushes(self):
        p = self._pattern(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=2,
        )
        assert p != SandbaggingPattern.late_pushes

    def test_2_days_late_is_not_forecast_delay(self):
        p = self._pattern(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=2,
        )
        assert p != SandbaggingPattern.forecast_delay

    def test_2_pull_forward_is_not_pull_forward_abuse(self):
        p = self._pattern(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=0,
            deal_pull_forward_count=2,
        )
        assert p != SandbaggingPattern.pull_forward_abuse


# ---------------------------------------------------------------------------
# 15. Recommended action
# ---------------------------------------------------------------------------

class TestRecommendedAction:
    def _action(self, risk: SandbaggingRisk, composite: float) -> SandbaggingAction:
        return _detector()._recommended_action(risk, composite)

    def test_composite_60_gives_compensation_audit(self):
        assert self._action(SandbaggingRisk.critical, 60.0) == SandbaggingAction.compensation_audit

    def test_composite_80_gives_compensation_audit(self):
        assert self._action(SandbaggingRisk.high, 80.0) == SandbaggingAction.compensation_audit

    def test_composite_100_gives_compensation_audit(self):
        assert self._action(SandbaggingRisk.critical, 100.0) == SandbaggingAction.compensation_audit

    def test_high_risk_below_60_gives_quota_recalibrate(self):
        assert self._action(SandbaggingRisk.high, 55.0) == SandbaggingAction.quota_recalibrate

    def test_high_risk_40_gives_quota_recalibrate(self):
        assert self._action(SandbaggingRisk.high, 40.0) == SandbaggingAction.quota_recalibrate

    def test_moderate_risk_gives_manager_review(self):
        assert self._action(SandbaggingRisk.moderate, 30.0) == SandbaggingAction.manager_review

    def test_moderate_risk_20_gives_manager_review(self):
        assert self._action(SandbaggingRisk.moderate, 20.0) == SandbaggingAction.manager_review

    def test_low_risk_composite_10_gives_monitor(self):
        assert self._action(SandbaggingRisk.low, 10.0) == SandbaggingAction.monitor

    def test_low_risk_composite_15_gives_monitor(self):
        assert self._action(SandbaggingRisk.low, 15.0) == SandbaggingAction.monitor

    def test_low_risk_composite_below_10_gives_no_action(self):
        assert self._action(SandbaggingRisk.low, 0.0) == SandbaggingAction.no_action

    def test_low_risk_composite_9_gives_no_action(self):
        assert self._action(SandbaggingRisk.low, 9.9) == SandbaggingAction.no_action

    def test_critical_risk_below_60_gives_quota_recalibrate(self):
        # critical risk is composite >= 60, so shouldn't arise < 60; but classification
        # takes composite >= 60 first anyway
        assert self._action(SandbaggingRisk.high, 59.9) == SandbaggingAction.quota_recalibrate


# ---------------------------------------------------------------------------
# 16. is_sandbagging invariant
# ---------------------------------------------------------------------------

class TestIsSandbagging:
    def test_composite_40_triggers_sandbagging(self):
        # Build input that gives composite >= 40
        inp = _make_input(
            committed_forecast_usd=100_000, actual_attained_usd=200_000,
            historical_accuracy_pct=60, forecast_submission_days_late=10,
            avg_quarter_over_attainment_pct=160, peer_avg_over_attainment_pct=100,
            manager_override_count=3,
        )
        result = _detector().assess(inp)
        if result.sandbagging_composite >= 40:
            assert result.is_sandbagging is True

    def test_prior_period_150_triggers_sandbagging(self):
        inp = _make_input(prior_period_over_attainment_pct=150)
        result = _detector().assess(inp)
        assert result.is_sandbagging is True

    def test_prior_period_200_triggers_sandbagging(self):
        inp = _make_input(prior_period_over_attainment_pct=200)
        result = _detector().assess(inp)
        assert result.is_sandbagging is True

    def test_deals_held_3_triggers_sandbagging(self):
        inp = _make_input(deals_held_from_forecast_count=3)
        result = _detector().assess(inp)
        assert result.is_sandbagging is True

    def test_deals_held_10_triggers_sandbagging(self):
        inp = _make_input(deals_held_from_forecast_count=10)
        result = _detector().assess(inp)
        assert result.is_sandbagging is True

    def test_clean_rep_not_sandbagging(self):
        inp = _make_input(
            committed_forecast_usd=100_000, actual_attained_usd=105_000,
            prior_period_over_attainment_pct=105, avg_quarter_over_attainment_pct=105,
            deals_held_from_forecast_count=0, historical_accuracy_pct=90,
            forecast_submission_days_late=0, manager_override_count=0,
            late_stage_deals_not_committed_count=0, close_date_pushed_past_period_count=0,
            deal_pull_forward_count=0, pipeline_coverage_ratio=1.5, quota_usd=100_000,
            deals_pulled_from_next_period_count=0, peer_avg_over_attainment_pct=105,
        )
        result = _detector().assess(inp)
        assert result.is_sandbagging is False

    def test_prior_149_does_not_trigger_by_prior_period_alone(self):
        inp = _make_input(prior_period_over_attainment_pct=149)
        result = _detector().assess(inp)
        # May or may not be sandbagging via composite — just verify prior_period alone is not enough
        # If composite < 40 and held < 3, must be False
        det = _detector()
        res = det.assess(inp)
        if res.sandbagging_composite < 40 and inp.deals_held_from_forecast_count < 3:
            assert res.is_sandbagging is False

    def test_deals_held_2_does_not_trigger_alone(self):
        inp = _make_input(deals_held_from_forecast_count=2,
                          prior_period_over_attainment_pct=100)
        result = _detector().assess(inp)
        # composite with 2 held = 15*0.25=3.75. Must check composite < 40
        if result.sandbagging_composite < 40 and inp.prior_period_over_attainment_pct < 150:
            assert result.is_sandbagging is False


# ---------------------------------------------------------------------------
# 17. requires_quota_review invariant
# ---------------------------------------------------------------------------

class TestRequiresQuotaReview:
    def test_composite_30_triggers_quota_review(self):
        inp = _make_input(
            committed_forecast_usd=100_000, actual_attained_usd=200_000,
            historical_accuracy_pct=60, forecast_submission_days_late=5,
        )
        result = _detector().assess(inp)
        if result.sandbagging_composite >= 30:
            assert result.requires_quota_review is True

    def test_avg_overattainment_130_triggers_quota_review(self):
        inp = _make_input(avg_quarter_over_attainment_pct=130)
        result = _detector().assess(inp)
        assert result.requires_quota_review is True

    def test_avg_overattainment_200_triggers_quota_review(self):
        inp = _make_input(avg_quarter_over_attainment_pct=200)
        result = _detector().assess(inp)
        assert result.requires_quota_review is True

    def test_deals_held_2_and_change_3_triggers_quota_review(self):
        inp = _make_input(deals_held_from_forecast_count=2, forecast_change_count=3)
        result = _detector().assess(inp)
        assert result.requires_quota_review is True

    def test_deals_held_2_and_change_2_not_triggered_alone(self):
        inp = _make_input(
            deals_held_from_forecast_count=2, forecast_change_count=2,
            avg_quarter_over_attainment_pct=100,
        )
        result = _detector().assess(inp)
        # Only triggered if composite >= 30 or avg >= 130 or (held>=2 and change>=3)
        if result.sandbagging_composite < 30 and inp.avg_quarter_over_attainment_pct < 130:
            assert result.requires_quota_review is False

    def test_avg_overattainment_129_not_triggered_by_avg_alone(self):
        inp = _make_input(avg_quarter_over_attainment_pct=129,
                          deals_held_from_forecast_count=0)
        result = _detector().assess(inp)
        if result.sandbagging_composite < 30:
            assert result.requires_quota_review is False

    def test_deals_held_1_and_change_10_not_triggered_alone(self):
        inp = _make_input(deals_held_from_forecast_count=1, forecast_change_count=10,
                          avg_quarter_over_attainment_pct=100)
        result = _detector().assess(inp)
        if result.sandbagging_composite < 30:
            assert result.requires_quota_review is False


# ---------------------------------------------------------------------------
# 18. estimated_hidden_pipeline_usd formula
# ---------------------------------------------------------------------------

class TestEstimatedHiddenPipeline:
    def test_formula_exact(self):
        inp = _make_input(sandbagged_deal_value_usd=100_000.0)
        result = _detector().assess(inp)
        expected = inp.sandbagged_deal_value_usd * (result.sandbagging_composite / 100.0)
        assert math.isclose(result.estimated_hidden_pipeline_usd, expected, rel_tol=1e-6)

    def test_zero_sandbagged_value_gives_zero_hidden(self):
        inp = _make_input(sandbagged_deal_value_usd=0.0)
        result = _detector().assess(inp)
        assert result.estimated_hidden_pipeline_usd == 0.0

    def test_zero_composite_gives_zero_hidden(self):
        inp = _make_input(
            sandbagged_deal_value_usd=500_000.0,
            committed_forecast_usd=0, actual_attained_usd=0,
            historical_accuracy_pct=90, forecast_submission_days_late=0,
            avg_quarter_over_attainment_pct=100, peer_avg_over_attainment_pct=0,
            manager_override_count=0, deals_held_from_forecast_count=0,
            late_stage_deals_not_committed_count=0, close_date_pushed_past_period_count=0,
            deal_pull_forward_count=0, prior_period_over_attainment_pct=100,
            pipeline_coverage_ratio=1.0, quota_usd=100_000,
            deals_pulled_from_next_period_count=0,
        )
        result = _detector().assess(inp)
        assert result.estimated_hidden_pipeline_usd == 0.0

    def test_hidden_pipeline_in_to_dict(self):
        inp = _make_input(sandbagged_deal_value_usd=200_000.0)
        result = _detector().assess(inp)
        d = result.to_dict()
        assert d["estimated_hidden_pipeline_usd"] == round(result.estimated_hidden_pipeline_usd, 2)

    def test_hidden_pipeline_scales_with_composite(self):
        det = _detector()
        inp_low = _make_input(sandbagged_deal_value_usd=100_000.0,
                              committed_forecast_usd=0, actual_attained_usd=0,
                              historical_accuracy_pct=90, forecast_submission_days_late=0,
                              avg_quarter_over_attainment_pct=100, peer_avg_over_attainment_pct=0,
                              manager_override_count=0, deals_held_from_forecast_count=0,
                              late_stage_deals_not_committed_count=0,
                              close_date_pushed_past_period_count=0,
                              deal_pull_forward_count=0, prior_period_over_attainment_pct=100,
                              pipeline_coverage_ratio=1.0, quota_usd=100_000,
                              deals_pulled_from_next_period_count=0)
        inp_high = _make_input(sandbagged_deal_value_usd=100_000.0,
                               committed_forecast_usd=100_000, actual_attained_usd=300_000,
                               historical_accuracy_pct=60, forecast_submission_days_late=10,
                               avg_quarter_over_attainment_pct=160,
                               peer_avg_over_attainment_pct=100, manager_override_count=5,
                               deals_held_from_forecast_count=0,
                               late_stage_deals_not_committed_count=0,
                               close_date_pushed_past_period_count=0,
                               deal_pull_forward_count=0, prior_period_over_attainment_pct=100,
                               pipeline_coverage_ratio=1.0, quota_usd=100_000,
                               deals_pulled_from_next_period_count=0)
        r_low = det.assess(inp_low)
        det2 = _detector()
        r_high = det2.assess(inp_high)
        assert r_high.estimated_hidden_pipeline_usd >= r_low.estimated_hidden_pipeline_usd


# ---------------------------------------------------------------------------
# 19. Signal text
# ---------------------------------------------------------------------------

class TestSignalText:
    def test_pattern_none_gives_normal_signal(self):
        inp = _make_input()
        result = _detector().assess(inp)
        if result.sandbagging_pattern == SandbaggingPattern.none:
            assert "normal parameters" in result.sandbagging_signal

    def test_deal_hoarding_signal_contains_held_count(self):
        inp = _make_input(deals_held_from_forecast_count=3)
        result = _detector().assess(inp)
        assert "3" in result.sandbagging_signal
        assert "composite" in result.sandbagging_signal

    def test_late_pushes_signal_contains_pushed_count(self):
        inp = _make_input(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=3,
        )
        result = _detector().assess(inp)
        assert "3" in result.sandbagging_signal

    def test_forecast_delay_signal_contains_days(self):
        inp = _make_input(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=5,
        )
        result = _detector().assess(inp)
        assert "5" in result.sandbagging_signal
        assert "days late" in result.sandbagging_signal

    def test_pull_forward_signal_contains_count(self):
        inp = _make_input(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=0,
            deal_pull_forward_count=3,
        )
        result = _detector().assess(inp)
        assert "3" in result.sandbagging_signal

    def test_consistent_low_signal_contains_overattainment(self):
        inp = _make_input(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=0,
            deal_pull_forward_count=0,
            avg_quarter_over_attainment_pct=140,
        )
        result = _detector().assess(inp)
        assert "140" in result.sandbagging_signal

    def test_non_none_signal_always_contains_composite(self):
        inp = _make_input(deals_held_from_forecast_count=3)
        result = _detector().assess(inp)
        if result.sandbagging_pattern != SandbaggingPattern.none:
            assert "composite" in result.sandbagging_signal

    def test_signal_is_non_empty_string(self):
        result = _detector().assess(_make_input())
        assert len(result.sandbagging_signal) > 0


# ---------------------------------------------------------------------------
# 20. assess() integration: result fields
# ---------------------------------------------------------------------------

class TestAssessIntegration:
    def test_rep_id_stored(self):
        inp = _make_input(rep_id="SALES-007")
        assert _detector().assess(inp).rep_id == "SALES-007"

    def test_region_stored(self):
        inp = _make_input(region="APAC")
        assert _detector().assess(inp).region == "APAC"

    def test_result_has_correct_type(self):
        from swarm.intelligence.sales_forecast_sandbagging_detector import SalesForecastSandbaggingResult
        result = _detector().assess(_make_input())
        assert isinstance(result, SalesForecastSandbaggingResult)

    def test_risk_is_enum(self):
        result = _detector().assess(_make_input())
        assert isinstance(result.sandbagging_risk, SandbaggingRisk)

    def test_pattern_is_enum(self):
        result = _detector().assess(_make_input())
        assert isinstance(result.sandbagging_pattern, SandbaggingPattern)

    def test_severity_is_enum(self):
        result = _detector().assess(_make_input())
        assert isinstance(result.sandbagging_severity, SandbaggingSeverity)

    def test_action_is_enum(self):
        result = _detector().assess(_make_input())
        assert isinstance(result.recommended_action, SandbaggingAction)

    def test_all_scores_non_negative(self):
        result = _detector().assess(_make_input())
        assert result.forecast_accuracy_score >= 0
        assert result.pattern_consistency_score >= 0
        assert result.deal_manipulation_score >= 0
        assert result.over_attainment_score >= 0

    def test_all_scores_at_most_100(self):
        result = _detector().assess(_make_input())
        assert result.forecast_accuracy_score <= 100
        assert result.pattern_consistency_score <= 100
        assert result.deal_manipulation_score <= 100
        assert result.over_attainment_score <= 100

    def test_composite_range(self):
        result = _detector().assess(_make_input())
        assert 0.0 <= result.sandbagging_composite <= 100.0

    def test_result_stored_internally(self):
        det = _detector()
        det.assess(_make_input())
        assert len(det._results) == 1

    def test_each_assess_appends_result(self):
        det = _detector()
        det.assess(_make_input())
        det.assess(_make_input(rep_id="R2"))
        assert len(det._results) == 2

    def test_risk_severity_consistency(self):
        # risk and severity should be consistent with composite
        result = _detector().assess(_make_input(deals_held_from_forecast_count=5,
                                                committed_forecast_usd=100_000,
                                                actual_attained_usd=300_000))
        composite = result.sandbagging_composite
        if composite < 20:
            assert result.sandbagging_risk == SandbaggingRisk.low
            assert result.sandbagging_severity == SandbaggingSeverity.clean
        elif composite < 40:
            assert result.sandbagging_risk == SandbaggingRisk.moderate
            assert result.sandbagging_severity == SandbaggingSeverity.watch
        elif composite < 60:
            assert result.sandbagging_risk == SandbaggingRisk.high
            assert result.sandbagging_severity == SandbaggingSeverity.suspicious
        else:
            assert result.sandbagging_risk == SandbaggingRisk.critical
            assert result.sandbagging_severity == SandbaggingSeverity.confirmed

    def test_compensation_audit_requires_composite_60_plus(self):
        result = _detector().assess(_make_input(
            committed_forecast_usd=100_000, actual_attained_usd=300_000,
            historical_accuracy_pct=60, forecast_submission_days_late=10,
            avg_quarter_over_attainment_pct=200, peer_avg_over_attainment_pct=100,
            manager_override_count=5,
        ))
        if result.recommended_action == SandbaggingAction.compensation_audit:
            assert result.sandbagging_composite >= 60.0


# ---------------------------------------------------------------------------
# 21. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_empty_list_returns_empty(self):
        assert _detector().assess_batch([]) == []

    def test_single_input_returns_single_result(self):
        results = _detector().assess_batch([_make_input()])
        assert len(results) == 1

    def test_batch_returns_correct_count(self):
        inputs = [_make_input(rep_id=f"R{i}") for i in range(5)]
        results = _detector().assess_batch(inputs)
        assert len(results) == 5

    def test_batch_preserves_order(self):
        inputs = [_make_input(rep_id=f"REP-{i:03d}") for i in range(10)]
        results = _detector().assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"REP-{i:03d}"

    def test_batch_appends_to_internal_results(self):
        det = _detector()
        inputs = [_make_input(rep_id=f"R{i}") for i in range(3)]
        det.assess_batch(inputs)
        assert len(det._results) == 3

    def test_batch_mixed_risk_levels(self):
        inputs = [
            _make_input(rep_id="LOW"),
            _make_input(rep_id="HIGH", deals_held_from_forecast_count=5,
                        committed_forecast_usd=100_000, actual_attained_usd=300_000),
        ]
        results = _detector().assess_batch(inputs)
        assert results[0].rep_id == "LOW"
        assert results[1].rep_id == "HIGH"

    def test_batch_result_types(self):
        from swarm.intelligence.sales_forecast_sandbagging_detector import SalesForecastSandbaggingResult
        inputs = [_make_input() for _ in range(3)]
        for r in _detector().assess_batch(inputs):
            assert isinstance(r, SalesForecastSandbaggingResult)

    def test_batch_then_summary_totals(self):
        det = _detector()
        inputs = [_make_input(rep_id=f"R{i}") for i in range(4)]
        det.assess_batch(inputs)
        s = det.summary()
        assert s["total"] == 4


# ---------------------------------------------------------------------------
# 22. summary() — exactly 13 keys
# ---------------------------------------------------------------------------

class TestSummaryKeys:
    EXPECTED_KEYS = {
        "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
        "avg_sandbagging_composite", "sandbagging_count", "quota_review_count",
        "avg_forecast_accuracy_score", "avg_pattern_consistency_score",
        "avg_deal_manipulation_score", "avg_over_attainment_score",
        "total_estimated_hidden_pipeline_usd",
    }

    def test_empty_summary_key_count(self):
        s = _detector().summary()
        assert len(s) == 13

    def test_empty_summary_exact_keys(self):
        s = _detector().summary()
        assert set(s.keys()) == self.EXPECTED_KEYS

    def test_populated_summary_key_count(self):
        det = _detector()
        det.assess(_make_input())
        assert len(det.summary()) == 13

    def test_populated_summary_exact_keys(self):
        det = _detector()
        det.assess(_make_input())
        assert set(det.summary().keys()) == self.EXPECTED_KEYS


class TestSummaryEmpty:
    def test_total_is_zero(self):
        assert _detector().summary()["total"] == 0

    def test_risk_counts_is_empty_dict(self):
        assert _detector().summary()["risk_counts"] == {}

    def test_pattern_counts_is_empty_dict(self):
        assert _detector().summary()["pattern_counts"] == {}

    def test_severity_counts_is_empty_dict(self):
        assert _detector().summary()["severity_counts"] == {}

    def test_action_counts_is_empty_dict(self):
        assert _detector().summary()["action_counts"] == {}

    def test_avg_composite_is_zero(self):
        assert _detector().summary()["avg_sandbagging_composite"] == 0.0

    def test_sandbagging_count_is_zero(self):
        assert _detector().summary()["sandbagging_count"] == 0

    def test_quota_review_count_is_zero(self):
        assert _detector().summary()["quota_review_count"] == 0

    def test_avg_accuracy_is_zero(self):
        assert _detector().summary()["avg_forecast_accuracy_score"] == 0.0

    def test_avg_pattern_is_zero(self):
        assert _detector().summary()["avg_pattern_consistency_score"] == 0.0

    def test_avg_deal_is_zero(self):
        assert _detector().summary()["avg_deal_manipulation_score"] == 0.0

    def test_avg_over_attainment_is_zero(self):
        assert _detector().summary()["avg_over_attainment_score"] == 0.0

    def test_total_hidden_pipeline_is_zero(self):
        assert _detector().summary()["total_estimated_hidden_pipeline_usd"] == 0.0


class TestSummaryPopulated:
    def _det_with_one_clean(self) -> SalesForecastSandbaggingDetector:
        det = _detector()
        det.assess(_make_input())
        return det

    def test_total_is_one(self):
        assert self._det_with_one_clean().summary()["total"] == 1

    def test_sandbagging_count_type(self):
        assert isinstance(self._det_with_one_clean().summary()["sandbagging_count"], int)

    def test_quota_review_count_type(self):
        assert isinstance(self._det_with_one_clean().summary()["quota_review_count"], int)

    def test_avg_composite_is_float(self):
        s = self._det_with_one_clean().summary()
        assert isinstance(s["avg_sandbagging_composite"], float)

    def test_risk_counts_sums_to_total(self):
        det = _detector()
        inputs = [_make_input(rep_id=f"R{i}") for i in range(5)]
        det.assess_batch(inputs)
        s = det.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_pattern_counts_sums_to_total(self):
        det = _detector()
        inputs = [_make_input(rep_id=f"R{i}") for i in range(5)]
        det.assess_batch(inputs)
        s = det.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_severity_counts_sums_to_total(self):
        det = _detector()
        inputs = [_make_input(rep_id=f"R{i}") for i in range(5)]
        det.assess_batch(inputs)
        s = det.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_action_counts_sums_to_total(self):
        det = _detector()
        inputs = [_make_input(rep_id=f"R{i}") for i in range(5)]
        det.assess_batch(inputs)
        s = det.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_sandbagging_count_le_total(self):
        det = _detector()
        det.assess_batch([_make_input(rep_id=f"R{i}") for i in range(5)])
        s = det.summary()
        assert s["sandbagging_count"] <= s["total"]

    def test_quota_review_count_le_total(self):
        det = _detector()
        det.assess_batch([_make_input(rep_id=f"R{i}") for i in range(5)])
        s = det.summary()
        assert s["quota_review_count"] <= s["total"]

    def test_total_hidden_pipeline_non_negative(self):
        det = _detector()
        det.assess(_make_input())
        assert det.summary()["total_estimated_hidden_pipeline_usd"] >= 0.0

    def test_sandbagging_count_with_explicit_sandbagging(self):
        det = _detector()
        det.assess(_make_input(deals_held_from_forecast_count=3))
        det.assess(_make_input())
        s = det.summary()
        assert s["sandbagging_count"] >= 1

    def test_quota_review_count_with_high_avg(self):
        det = _detector()
        det.assess(_make_input(avg_quarter_over_attainment_pct=150))
        s = det.summary()
        assert s["quota_review_count"] >= 1

    def test_avg_composite_within_range(self):
        det = _detector()
        det.assess_batch([_make_input(rep_id=f"R{i}") for i in range(3)])
        s = det.summary()
        assert 0.0 <= s["avg_sandbagging_composite"] <= 100.0

    def test_avg_scores_within_range(self):
        det = _detector()
        det.assess_batch([_make_input(rep_id=f"R{i}") for i in range(3)])
        s = det.summary()
        for k in ("avg_forecast_accuracy_score", "avg_pattern_consistency_score",
                  "avg_deal_manipulation_score", "avg_over_attainment_score"):
            assert 0.0 <= s[k] <= 100.0

    def test_total_hidden_pipeline_is_sum(self):
        det = _detector()
        inp1 = _make_input(rep_id="R1", sandbagged_deal_value_usd=100_000.0)
        inp2 = _make_input(rep_id="R2", sandbagged_deal_value_usd=200_000.0)
        r1 = det.assess(inp1)
        r2 = det.assess(inp2)
        s = det.summary()
        expected = round(r1.estimated_hidden_pipeline_usd + r2.estimated_hidden_pipeline_usd, 2)
        assert math.isclose(s["total_estimated_hidden_pipeline_usd"], expected, rel_tol=1e-6)

    def test_avg_composite_one_result_matches_that_result(self):
        det = _detector()
        result = det.assess(_make_input())
        s = det.summary()
        assert s["avg_sandbagging_composite"] == result.sandbagging_composite

    def test_summary_total_matches_assess_count(self):
        det = _detector()
        for i in range(7):
            det.assess(_make_input(rep_id=f"R{i}"))
        assert det.summary()["total"] == 7

    def test_multiple_calls_accumulate(self):
        det = _detector()
        det.assess(_make_input(rep_id="A"))
        det.assess(_make_input(rep_id="B"))
        det.assess(_make_input(rep_id="C"))
        assert det.summary()["total"] == 3

    def test_avg_scores_rounded_to_1dp(self):
        det = _detector()
        det.assess(_make_input())
        s = det.summary()
        for k in ("avg_sandbagging_composite", "avg_forecast_accuracy_score",
                  "avg_pattern_consistency_score", "avg_deal_manipulation_score",
                  "avg_over_attainment_score"):
            val = s[k]
            assert round(val, 1) == val

    def test_total_hidden_rounded_to_2dp(self):
        det = _detector()
        det.assess(_make_input())
        val = det.summary()["total_estimated_hidden_pipeline_usd"]
        assert round(val, 2) == val


# ---------------------------------------------------------------------------
# 23. Edge cases and boundary values
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_very_large_forecast_value(self):
        inp = _make_input(committed_forecast_usd=1e9, actual_attained_usd=1e9)
        result = _detector().assess(inp)
        assert 0.0 <= result.sandbagging_composite <= 100.0

    def test_zero_committed_and_zero_attained(self):
        inp = _make_input(committed_forecast_usd=0.0, actual_attained_usd=0.0)
        result = _detector().assess(inp)
        assert result.sandbagging_composite >= 0.0

    def test_negative_overrides_are_handled(self):
        # Negative peer avg -> outperform delta could be huge, score clamped
        inp = _make_input(avg_quarter_over_attainment_pct=160, peer_avg_over_attainment_pct=0.0)
        result = _detector().assess(inp)
        assert result.pattern_consistency_score <= 100.0

    def test_all_zero_inputs_result(self):
        inp = _make_input(
            committed_forecast_usd=0, actual_attained_usd=0,
            prior_period_over_attainment_pct=0, avg_quarter_over_attainment_pct=0,
            deals_held_from_forecast_count=0, late_stage_deals_not_committed_count=0,
            close_date_pushed_past_period_count=0, pipeline_coverage_ratio=0,
            forecast_submission_days_late=0, forecast_change_count=0,
            sandbagged_deal_value_usd=0, avg_deal_size_usd=0,
            peer_avg_over_attainment_pct=0, rep_tenure_years=0, quota_usd=0,
            manager_override_count=0, deal_pull_forward_count=0,
            historical_accuracy_pct=100, deals_pulled_from_next_period_count=0,
        )
        result = _detector().assess(inp)
        assert result.sandbagging_composite == 0.0
        assert result.is_sandbagging is False

    def test_all_max_sandbagging_inputs(self):
        inp = _make_input(
            committed_forecast_usd=100_000, actual_attained_usd=500_000,
            prior_period_over_attainment_pct=300, avg_quarter_over_attainment_pct=300,
            deals_held_from_forecast_count=10, late_stage_deals_not_committed_count=10,
            close_date_pushed_past_period_count=10, pipeline_coverage_ratio=5.0,
            forecast_submission_days_late=10, forecast_change_count=10,
            sandbagged_deal_value_usd=1_000_000, avg_deal_size_usd=100_000,
            peer_avg_over_attainment_pct=100, rep_tenure_years=10, quota_usd=100_000,
            manager_override_count=10, deal_pull_forward_count=10,
            historical_accuracy_pct=50, deals_pulled_from_next_period_count=10,
        )
        result = _detector().assess(inp)
        assert result.sandbagging_composite >= 60.0
        assert result.is_sandbagging is True
        assert result.requires_quota_review is True
        assert result.recommended_action == SandbaggingAction.compensation_audit

    def test_boundary_composite_exactly_40_is_high_risk(self):
        det = _detector()
        assert det._classify_risk(40.0) == SandbaggingRisk.high

    def test_boundary_composite_exactly_60_is_critical(self):
        det = _detector()
        assert det._classify_risk(60.0) == SandbaggingRisk.critical

    def test_boundary_composite_exactly_20_is_moderate(self):
        det = _detector()
        assert det._classify_risk(20.0) == SandbaggingRisk.moderate

    def test_clamp_function_at_zero(self):
        from swarm.intelligence.sales_forecast_sandbagging_detector import _clamp
        assert _clamp(-1.0) == 0.0

    def test_clamp_function_at_100(self):
        from swarm.intelligence.sales_forecast_sandbagging_detector import _clamp
        assert _clamp(101.0) == 100.0

    def test_clamp_function_midpoint(self):
        from swarm.intelligence.sales_forecast_sandbagging_detector import _clamp
        assert _clamp(50.0) == 50.0

    def test_forecast_period_id_stored_in_input(self):
        inp = _make_input(forecast_period_id="Q3-2025")
        assert inp.forecast_period_id == "Q3-2025"

    def test_rep_tenure_years_does_not_affect_scores(self):
        det1 = _detector()
        det2 = _detector()
        inp1 = _make_input(rep_tenure_years=1.0)
        inp2 = _make_input(rep_tenure_years=20.0)
        r1 = det1.assess(inp1)
        r2 = det2.assess(inp2)
        assert r1.sandbagging_composite == r2.sandbagging_composite

    def test_avg_deal_size_does_not_affect_scores(self):
        det1 = _detector()
        det2 = _detector()
        r1 = det1.assess(_make_input(avg_deal_size_usd=10_000))
        r2 = det2.assess(_make_input(avg_deal_size_usd=1_000_000))
        assert r1.sandbagging_composite == r2.sandbagging_composite

    def test_single_detect_does_not_carry_state_to_new_detector(self):
        det1 = _detector()
        det1.assess(_make_input(rep_id="R1"))
        det2 = _detector()
        assert det2.summary()["total"] == 0

    def test_assess_returns_result_directly(self):
        from swarm.intelligence.sales_forecast_sandbagging_detector import SalesForecastSandbaggingResult
        result = _detector().assess(_make_input())
        assert isinstance(result, SalesForecastSandbaggingResult)

    def test_batch_empty_does_not_affect_summary(self):
        det = _detector()
        det.assess_batch([])
        assert det.summary()["total"] == 0

    def test_to_dict_risk_is_valid_enum_value(self):
        d = _detector().assess(_make_input()).to_dict()
        assert d["sandbagging_risk"] in {r.value for r in SandbaggingRisk}

    def test_to_dict_pattern_is_valid_enum_value(self):
        d = _detector().assess(_make_input()).to_dict()
        assert d["sandbagging_pattern"] in {p.value for p in SandbaggingPattern}

    def test_to_dict_severity_is_valid_enum_value(self):
        d = _detector().assess(_make_input()).to_dict()
        assert d["sandbagging_severity"] in {s.value for s in SandbaggingSeverity}

    def test_to_dict_action_is_valid_enum_value(self):
        d = _detector().assess(_make_input()).to_dict()
        assert d["recommended_action"] in {a.value for a in SandbaggingAction}


# ---------------------------------------------------------------------------
# 24. Full end-to-end scenario tests
# ---------------------------------------------------------------------------

class TestScenarios:
    def test_clean_rep_scenario(self):
        """Rep with perfect behavior: low risk, clean, no_action."""
        inp = _make_input(
            committed_forecast_usd=100_000, actual_attained_usd=103_000,
            prior_period_over_attainment_pct=103, avg_quarter_over_attainment_pct=103,
            deals_held_from_forecast_count=0, historical_accuracy_pct=95,
            forecast_submission_days_late=0, manager_override_count=0,
            late_stage_deals_not_committed_count=0, close_date_pushed_past_period_count=0,
            deal_pull_forward_count=0, pipeline_coverage_ratio=1.5,
            quota_usd=100_000, deals_pulled_from_next_period_count=0,
            peer_avg_over_attainment_pct=103,
        )
        result = _detector().assess(inp)
        assert result.sandbagging_risk == SandbaggingRisk.low
        assert result.sandbagging_severity == SandbaggingSeverity.clean
        assert result.is_sandbagging is False
        assert result.sandbagging_pattern == SandbaggingPattern.none

    def test_deal_hoarder_scenario(self):
        """Rep hoarding deals: deal_hoarding pattern, is_sandbagging, review needed."""
        inp = _make_input(
            deals_held_from_forecast_count=5,
            late_stage_deals_not_committed_count=4,
            forecast_change_count=3,  # triggers requires_quota_review via (held>=2 AND change>=3)
        )
        result = _detector().assess(inp)
        assert result.sandbagging_pattern == SandbaggingPattern.deal_hoarding
        assert result.is_sandbagging is True
        assert result.requires_quota_review is True

    def test_late_submitter_scenario(self):
        """Rep who always submits late: forecast_delay pattern."""
        inp = _make_input(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=7,
        )
        result = _detector().assess(inp)
        assert result.sandbagging_pattern == SandbaggingPattern.forecast_delay

    def test_consistent_over_attainer_scenario(self):
        """Rep consistently over-attaining: consistent_low pattern."""
        inp = _make_input(
            avg_quarter_over_attainment_pct=155,
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=0,
            deal_pull_forward_count=0,
        )
        result = _detector().assess(inp)
        assert result.sandbagging_pattern == SandbaggingPattern.consistent_low
        assert result.requires_quota_review is True

    def test_pull_forward_abuser_scenario(self):
        """Rep pulling deals from future periods: pull_forward_abuse pattern."""
        inp = _make_input(
            deals_held_from_forecast_count=0,
            close_date_pushed_past_period_count=0,
            forecast_submission_days_late=0,
            deal_pull_forward_count=5,
        )
        result = _detector().assess(inp)
        assert result.sandbagging_pattern == SandbaggingPattern.pull_forward_abuse

    def test_high_composite_gets_compensation_audit(self):
        """Rep with composite >= 60 should get compensation_audit."""
        inp = _make_input(
            committed_forecast_usd=100_000, actual_attained_usd=300_000,
            historical_accuracy_pct=60, forecast_submission_days_late=10,
            avg_quarter_over_attainment_pct=200, peer_avg_over_attainment_pct=100,
            manager_override_count=5,
            deals_held_from_forecast_count=0,
            late_stage_deals_not_committed_count=0,
            close_date_pushed_past_period_count=0,
            deal_pull_forward_count=0,
            prior_period_over_attainment_pct=100,
            pipeline_coverage_ratio=1.0, quota_usd=100_000,
            deals_pulled_from_next_period_count=0,
        )
        result = _detector().assess(inp)
        if result.sandbagging_composite >= 60:
            assert result.recommended_action == SandbaggingAction.compensation_audit

    def test_moderate_risk_gets_manager_review(self):
        """Rep with moderate risk gets manager_review action."""
        inp = _make_input(
            committed_forecast_usd=100_000, actual_attained_usd=130_000,
            historical_accuracy_pct=75, forecast_submission_days_late=2,
        )
        result = _detector().assess(inp)
        if result.sandbagging_risk == SandbaggingRisk.moderate:
            assert result.recommended_action == SandbaggingAction.manager_review

    def test_batch_summary_sandbagging_count(self):
        """Batch with known sandbagging reps; count should match."""
        det = _detector()
        clean = _make_input(rep_id="CLEAN")
        sbag = _make_input(rep_id="SBAG", deals_held_from_forecast_count=3)
        det.assess_batch([clean, sbag])
        s = det.summary()
        assert s["sandbagging_count"] >= 1

    def test_multiple_regions_tracked(self):
        det = _detector()
        det.assess(_make_input(rep_id="W1", region="West"))
        det.assess(_make_input(rep_id="E1", region="East"))
        s = det.summary()
        assert s["total"] == 2

    def test_detector_accumulates_across_calls(self):
        det = _detector()
        for _ in range(10):
            det.assess(_make_input())
        assert det.summary()["total"] == 10

    def test_all_sandbagging_triggers_combine(self):
        """Prior period >= 150 AND deals_held >= 3 AND composite >= 40."""
        inp = _make_input(
            prior_period_over_attainment_pct=200,
            deals_held_from_forecast_count=5,
            committed_forecast_usd=100_000, actual_attained_usd=300_000,
            historical_accuracy_pct=60, forecast_submission_days_late=10,
        )
        result = _detector().assess(inp)
        assert result.is_sandbagging is True

    def test_quota_review_via_avg_over_attainment(self):
        inp = _make_input(avg_quarter_over_attainment_pct=130,
                          deals_held_from_forecast_count=0, forecast_change_count=0)
        result = _detector().assess(inp)
        assert result.requires_quota_review is True

    def test_quota_review_via_held_and_change(self):
        inp = _make_input(deals_held_from_forecast_count=2, forecast_change_count=3,
                          avg_quarter_over_attainment_pct=100)
        result = _detector().assess(inp)
        assert result.requires_quota_review is True

    def test_late_pushes_pattern_with_3_pushed(self):
        inp = _make_input(close_date_pushed_past_period_count=5,
                          deals_held_from_forecast_count=0)
        result = _detector().assess(inp)
        assert result.sandbagging_pattern == SandbaggingPattern.late_pushes

    def test_no_action_for_very_clean_rep(self):
        inp = _make_input(
            committed_forecast_usd=100_000, actual_attained_usd=100_500,
            prior_period_over_attainment_pct=100, avg_quarter_over_attainment_pct=100,
            deals_held_from_forecast_count=0, historical_accuracy_pct=98,
            forecast_submission_days_late=0, manager_override_count=0,
            late_stage_deals_not_committed_count=0, close_date_pushed_past_period_count=0,
            deal_pull_forward_count=0, pipeline_coverage_ratio=1.2, quota_usd=100_000,
            deals_pulled_from_next_period_count=0, peer_avg_over_attainment_pct=100,
            sandbagged_deal_value_usd=0,
        )
        result = _detector().assess(inp)
        assert result.recommended_action == SandbaggingAction.no_action

    def test_hidden_pipeline_is_zero_for_zero_sandbagged_value(self):
        inp = _make_input(sandbagged_deal_value_usd=0.0,
                          deals_held_from_forecast_count=5,
                          committed_forecast_usd=100_000, actual_attained_usd=300_000)
        result = _detector().assess(inp)
        assert result.estimated_hidden_pipeline_usd == 0.0

    def test_risk_counts_reflect_actual_risks(self):
        det = _detector()
        det.assess(_make_input(rep_id="L"))  # likely low
        s = det.summary()
        all_risk_values = {r.value for r in SandbaggingRisk}
        for key in s["risk_counts"].keys():
            assert key in all_risk_values

    def test_pattern_counts_reflect_actual_patterns(self):
        det = _detector()
        det.assess(_make_input(rep_id="P"))
        s = det.summary()
        all_pattern_values = {p.value for p in SandbaggingPattern}
        for key in s["pattern_counts"].keys():
            assert key in all_pattern_values

    def test_severity_counts_reflect_actual_severities(self):
        det = _detector()
        det.assess(_make_input(rep_id="S"))
        s = det.summary()
        all_sev_values = {sev.value for sev in SandbaggingSeverity}
        for key in s["severity_counts"].keys():
            assert key in all_sev_values

    def test_action_counts_reflect_actual_actions(self):
        det = _detector()
        det.assess(_make_input(rep_id="A"))
        s = det.summary()
        all_action_values = {a.value for a in SandbaggingAction}
        for key in s["action_counts"].keys():
            assert key in all_action_values


# ---------------------------------------------------------------------------
# 25. Additional boundary and regression tests
# ---------------------------------------------------------------------------

class TestAdditionalBoundaries:
    def test_forecast_accuracy_score_exactly_50_plus_0_plus_0(self):
        # ratio = 2.0 → 50 pts, accuracy >= 80, days_late=0
        s = _detector()._forecast_accuracy_score(
            _make_input(committed_forecast_usd=100_000, actual_attained_usd=200_000,
                        historical_accuracy_pct=85, forecast_submission_days_late=0))
        assert s == 50.0

    def test_forecast_accuracy_score_12_plus_0_plus_10(self):
        # ratio 1.25 → 12, days_late=2 → 10
        s = _detector()._forecast_accuracy_score(
            _make_input(committed_forecast_usd=100_000, actual_attained_usd=125_000,
                        historical_accuracy_pct=85, forecast_submission_days_late=2))
        assert s == 22.0

    def test_pattern_consistency_score_with_both_avg_and_delta(self):
        # avg=160 → 45, peer=0 so no delta, override=0
        s = _detector()._pattern_consistency_score(
            _make_input(avg_quarter_over_attainment_pct=160,
                        peer_avg_over_attainment_pct=0, manager_override_count=0))
        assert s == 45.0

    def test_deal_manipulation_score_5_held_plus_4_late_plus_3_pushed(self):
        # 45 + 30 + 20 = 95
        s = _detector()._deal_manipulation_score(
            _make_input(deals_held_from_forecast_count=5,
                        late_stage_deals_not_committed_count=4,
                        close_date_pushed_past_period_count=3,
                        deal_pull_forward_count=0))
        assert s == 95.0

    def test_over_attainment_score_200_prior_plus_30_coverage_plus_20_pulled(self):
        # 50 + 30 + 20 = 100 (clamped)
        s = _detector()._over_attainment_score(
            _make_input(prior_period_over_attainment_pct=200,
                        pipeline_coverage_ratio=4.0, quota_usd=100_000,
                        committed_forecast_usd=50_000,
                        deals_pulled_from_next_period_count=3))
        assert s == 100.0

    def test_classify_risk_thresholds_boundary_table(self):
        det = _detector()
        # (composite, expected_risk)
        cases = [
            (0.0, SandbaggingRisk.low),
            (19.9, SandbaggingRisk.low),
            (20.0, SandbaggingRisk.moderate),
            (39.9, SandbaggingRisk.moderate),
            (40.0, SandbaggingRisk.high),
            (59.9, SandbaggingRisk.high),
            (60.0, SandbaggingRisk.critical),
            (100.0, SandbaggingRisk.critical),
        ]
        for composite, expected in cases:
            assert det._classify_risk(composite) == expected, f"composite={composite}"

    def test_classify_severity_thresholds_boundary_table(self):
        det = _detector()
        cases = [
            (0.0, SandbaggingSeverity.clean),
            (19.9, SandbaggingSeverity.clean),
            (20.0, SandbaggingSeverity.watch),
            (39.9, SandbaggingSeverity.watch),
            (40.0, SandbaggingSeverity.suspicious),
            (59.9, SandbaggingSeverity.suspicious),
            (60.0, SandbaggingSeverity.confirmed),
            (100.0, SandbaggingSeverity.confirmed),
        ]
        for composite, expected in cases:
            assert det._classify_severity(composite) == expected, f"composite={composite}"

    def test_recommended_action_boundary_table(self):
        det = _detector()
        # (risk, composite, expected)
        cases = [
            (SandbaggingRisk.low, 0.0, SandbaggingAction.no_action),
            (SandbaggingRisk.low, 9.9, SandbaggingAction.no_action),
            (SandbaggingRisk.low, 10.0, SandbaggingAction.monitor),
            (SandbaggingRisk.low, 19.9, SandbaggingAction.monitor),
            (SandbaggingRisk.moderate, 20.0, SandbaggingAction.manager_review),
            (SandbaggingRisk.moderate, 39.9, SandbaggingAction.manager_review),
            (SandbaggingRisk.high, 40.0, SandbaggingAction.quota_recalibrate),
            (SandbaggingRisk.high, 59.9, SandbaggingAction.quota_recalibrate),
            (SandbaggingRisk.critical, 60.0, SandbaggingAction.compensation_audit),
            (SandbaggingRisk.critical, 100.0, SandbaggingAction.compensation_audit),
        ]
        for risk, composite, expected in cases:
            assert det._recommended_action(risk, composite) == expected

    def test_to_dict_returns_new_dict_each_call(self):
        result = _detector().assess(_make_input())
        d1 = result.to_dict()
        d2 = result.to_dict()
        assert d1 == d2
        assert d1 is not d2

    def test_summary_called_twice_returns_same(self):
        det = _detector()
        det.assess(_make_input())
        s1 = det.summary()
        s2 = det.summary()
        assert s1 == s2

    def test_composite_formula_with_known_sub_scores(self):
        # Pure accuracy=50, pattern=0, deal=0, over=0 → 15.0
        inp = _make_input(
            committed_forecast_usd=100_000, actual_attained_usd=200_000,
            historical_accuracy_pct=90, forecast_submission_days_late=0,
            avg_quarter_over_attainment_pct=100, peer_avg_over_attainment_pct=0,
            manager_override_count=0, deals_held_from_forecast_count=0,
            late_stage_deals_not_committed_count=0, close_date_pushed_past_period_count=0,
            deal_pull_forward_count=0, prior_period_over_attainment_pct=100,
            pipeline_coverage_ratio=1.0, quota_usd=100_000,
            deals_pulled_from_next_period_count=0,
        )
        result = _detector().assess(inp)
        assert result.sandbagging_composite == 15.0  # 50*0.30=15

    def test_pattern_consistency_delta_exactly_50_from_peer(self):
        # avg=150, peer=100, delta=50 → adds 30
        s = _detector()._pattern_consistency_score(
            _make_input(avg_quarter_over_attainment_pct=150,
                        peer_avg_over_attainment_pct=100, manager_override_count=0))
        # 32 (avg tier) + 30 (delta) = 62
        assert s == 62.0

    def test_over_attainment_score_exactly_3_coverage_80_pct_commitment(self):
        # coverage=3.0, commitment/quota=80/100=0.8 → < 0.9 → adds 18
        s = _detector()._over_attainment_score(
            _make_input(prior_period_over_attainment_pct=100,
                        pipeline_coverage_ratio=3.0, quota_usd=100_000,
                        committed_forecast_usd=80_000,
                        deals_pulled_from_next_period_count=0))
        assert s == 18.0

    def test_over_attainment_score_exactly_4_coverage_80_pct_commitment(self):
        # coverage=4.0, commitment/quota=0.8 → exactly 0.8, which is NOT < 0.8
        s = _detector()._over_attainment_score(
            _make_input(prior_period_over_attainment_pct=100,
                        pipeline_coverage_ratio=4.0, quota_usd=100_000,
                        committed_forecast_usd=80_000,  # 0.80, NOT < 0.8
                        deals_pulled_from_next_period_count=0))
        # Should fall to moderate coverage check: coverage >= 3.0 and commitment < 0.9 → 18
        assert s == 18.0

    def test_over_attainment_score_coverage_4_commitment_70_pct(self):
        # coverage=4.0, commitment/quota=0.70 < 0.8 → adds 30
        s = _detector()._over_attainment_score(
            _make_input(prior_period_over_attainment_pct=100,
                        pipeline_coverage_ratio=4.0, quota_usd=100_000,
                        committed_forecast_usd=70_000,
                        deals_pulled_from_next_period_count=0))
        assert s == 30.0

    def test_forecast_accuracy_score_ratio_1_24_no_points(self):
        # ratio = 124000/100000 = 1.24 → below 1.25 threshold
        s = _detector()._forecast_accuracy_score(
            _make_input(committed_forecast_usd=100_000, actual_attained_usd=124_000,
                        historical_accuracy_pct=90, forecast_submission_days_late=0))
        assert s == 0.0

    def test_pattern_classify_order_deals_first(self):
        # Both deal_hoarding and late_pushes conditions met → deal_hoarding wins
        det = _detector()
        inp = _make_input(
            deals_held_from_forecast_count=4,  # >= 3
            close_date_pushed_past_period_count=5,  # >= 3
        )
        result = det.assess(inp)
        assert result.sandbagging_pattern == SandbaggingPattern.deal_hoarding

    def test_avg_composite_sum_divided_by_n(self):
        det = _detector()
        r1 = det.assess(_make_input(rep_id="R1"))
        r2 = det.assess(_make_input(rep_id="R2"))
        expected_avg = round((r1.sandbagging_composite + r2.sandbagging_composite) / 2, 1)
        assert det.summary()["avg_sandbagging_composite"] == expected_avg

    def test_risk_keys_in_summary_are_valid(self):
        det = _detector()
        det.assess(_make_input(deals_held_from_forecast_count=5,
                               committed_forecast_usd=100_000, actual_attained_usd=250_000))
        s = det.summary()
        for key in s["risk_counts"]:
            assert key in {r.value for r in SandbaggingRisk}

    def test_summary_avg_accuracy_matches_single_result(self):
        det = _detector()
        result = det.assess(_make_input())
        s = det.summary()
        assert s["avg_forecast_accuracy_score"] == result.forecast_accuracy_score

    def test_summary_avg_pattern_matches_single_result(self):
        det = _detector()
        result = det.assess(_make_input())
        s = det.summary()
        assert s["avg_pattern_consistency_score"] == result.pattern_consistency_score

    def test_summary_avg_deal_matches_single_result(self):
        det = _detector()
        result = det.assess(_make_input())
        s = det.summary()
        assert s["avg_deal_manipulation_score"] == result.deal_manipulation_score

    def test_summary_avg_over_attainment_matches_single_result(self):
        det = _detector()
        result = det.assess(_make_input())
        s = det.summary()
        assert s["avg_over_attainment_score"] == result.over_attainment_score

    def test_result_dataclass_field_count(self):
        from swarm.intelligence.sales_forecast_sandbagging_detector import SalesForecastSandbaggingResult
        fields = dataclasses.fields(SalesForecastSandbaggingResult)
        assert len(fields) == 15

    def test_result_field_names(self):
        from swarm.intelligence.sales_forecast_sandbagging_detector import SalesForecastSandbaggingResult
        field_names = {f.name for f in dataclasses.fields(SalesForecastSandbaggingResult)}
        expected = {
            "rep_id", "region", "sandbagging_risk", "sandbagging_pattern",
            "sandbagging_severity", "recommended_action", "forecast_accuracy_score",
            "pattern_consistency_score", "deal_manipulation_score", "over_attainment_score",
            "sandbagging_composite", "is_sandbagging", "requires_quota_review",
            "estimated_hidden_pipeline_usd", "sandbagging_signal",
        }
        assert field_names == expected
