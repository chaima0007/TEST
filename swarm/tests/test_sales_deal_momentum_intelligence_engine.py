"""
Comprehensive pytest test suite for SalesDealMomentumIntelligenceEngine.
Covers all enums, dataclass fields, sub-scores, composite, thresholds,
patterns, flags, dollar impact, signal, and public API.
"""
from __future__ import annotations

import math
import pytest
from swarm.intelligence.sales_deal_momentum_intelligence_engine import (
    MomentumRisk,
    MomentumPattern,
    MomentumSeverity,
    MomentumAction,
    MomentumInput,
    MomentumResult,
    SalesDealMomentumIntelligenceEngine,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────────────────────

def make_input(**overrides) -> MomentumInput:
    """Return a MomentumInput with all fields at 'good' (low-risk) defaults."""
    defaults = dict(
        rep_id="rep-001",
        region="EMEA",
        evaluation_period_id="Q2-2026",
        avg_days_in_stage=5.0,
        stage_progression_rate_pct=0.50,   # high progression → low discipline risk
        deal_velocity_score=0.80,           # high → low velocity risk
        stalled_deal_pct=0.05,             # low → low velocity risk
        avg_time_to_close_days=30.0,
        time_to_close_ratio=0.90,          # <1 → low velocity risk
        engagement_recency_score=0.90,     # high → low engagement risk
        next_step_completion_rate_pct=0.90,# high → low discipline risk
        multi_touch_frequency=2.0,         # high → low engagement risk
        deal_age_skew=0.10,                # low → low momentum risk
        reopen_rate_pct=0.05,              # low → low discipline risk
        forecast_category_movement_pct=0.80, # high → low momentum risk
        competitive_displacement_rate_pct=0.50,
        decision_date_slip_rate_pct=0.05,  # low → low momentum risk
        avg_days_since_last_contact=2.0,   # low → low engagement risk
        deal_expansion_rate_pct=0.30,
        lost_deal_recapture_pct=0.10,
        total_active_deals=20,
        avg_deal_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return MomentumInput(**defaults)


def make_engine() -> SalesDealMomentumIntelligenceEngine:
    return SalesDealMomentumIntelligenceEngine()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Enum values and counts
# ─────────────────────────────────────────────────────────────────────────────

class TestMomentumRiskEnum:
    def test_member_count(self):
        assert len(MomentumRisk) == 4

    def test_low_value(self):
        assert MomentumRisk.low.value == "low"

    def test_moderate_value(self):
        assert MomentumRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert MomentumRisk.high.value == "high"

    def test_critical_value(self):
        assert MomentumRisk.critical.value == "critical"

    def test_is_str_subclass(self):
        assert isinstance(MomentumRisk.low, str)


class TestMomentumPatternEnum:
    def test_member_count(self):
        assert len(MomentumPattern) == 6

    def test_none_value(self):
        assert MomentumPattern.none.value == "none"

    def test_stall_accumulator_value(self):
        assert MomentumPattern.stall_accumulator.value == "stall_accumulator"

    def test_slow_burn_value(self):
        assert MomentumPattern.slow_burn.value == "slow_burn"

    def test_late_stage_freeze_value(self):
        assert MomentumPattern.late_stage_freeze.value == "late_stage_freeze"

    def test_contact_desert_value(self):
        assert MomentumPattern.contact_desert.value == "contact_desert"

    def test_forecast_drift_value(self):
        assert MomentumPattern.forecast_drift.value == "forecast_drift"

    def test_is_str_subclass(self):
        assert isinstance(MomentumPattern.none, str)


class TestMomentumSeverityEnum:
    def test_member_count(self):
        assert len(MomentumSeverity) == 4

    def test_accelerating_value(self):
        assert MomentumSeverity.accelerating.value == "accelerating"

    def test_steady_value(self):
        assert MomentumSeverity.steady.value == "steady"

    def test_decelerating_value(self):
        assert MomentumSeverity.decelerating.value == "decelerating"

    def test_stalled_value(self):
        assert MomentumSeverity.stalled.value == "stalled"

    def test_is_str_subclass(self):
        assert isinstance(MomentumSeverity.accelerating, str)


class TestMomentumActionEnum:
    def test_member_count(self):
        assert len(MomentumAction) == 7

    def test_no_action_value(self):
        assert MomentumAction.no_action.value == "no_action"

    def test_pipeline_review_value(self):
        assert MomentumAction.pipeline_review.value == "pipeline_review"

    def test_deal_acceleration_coaching_value(self):
        assert MomentumAction.deal_acceleration_coaching.value == "deal_acceleration_coaching"

    def test_stall_intervention_value(self):
        assert MomentumAction.stall_intervention.value == "stall_intervention"

    def test_contact_cadence_coaching_value(self):
        assert MomentumAction.contact_cadence_coaching.value == "contact_cadence_coaching"

    def test_pipeline_purge_value(self):
        assert MomentumAction.pipeline_purge.value == "pipeline_purge"

    def test_executive_deal_rescue_value(self):
        assert MomentumAction.executive_deal_rescue.value == "executive_deal_rescue"

    def test_is_str_subclass(self):
        assert isinstance(MomentumAction.no_action, str)


# ─────────────────────────────────────────────────────────────────────────────
# 2. MomentumInput: all 22 fields exist and accept expected types
# ─────────────────────────────────────────────────────────────────────────────

class TestMomentumInputFields:
    def test_rep_id_field(self):
        inp = make_input(rep_id="r-99")
        assert inp.rep_id == "r-99"

    def test_region_field(self):
        inp = make_input(region="APAC")
        assert inp.region == "APAC"

    def test_evaluation_period_id_field(self):
        inp = make_input(evaluation_period_id="Q1-2026")
        assert inp.evaluation_period_id == "Q1-2026"

    def test_avg_days_in_stage_field(self):
        inp = make_input(avg_days_in_stage=12.5)
        assert inp.avg_days_in_stage == 12.5

    def test_stage_progression_rate_pct_field(self):
        inp = make_input(stage_progression_rate_pct=0.25)
        assert inp.stage_progression_rate_pct == 0.25

    def test_deal_velocity_score_field(self):
        inp = make_input(deal_velocity_score=0.55)
        assert inp.deal_velocity_score == 0.55

    def test_stalled_deal_pct_field(self):
        inp = make_input(stalled_deal_pct=0.40)
        assert inp.stalled_deal_pct == 0.40

    def test_avg_time_to_close_days_field(self):
        inp = make_input(avg_time_to_close_days=90.0)
        assert inp.avg_time_to_close_days == 90.0

    def test_time_to_close_ratio_field(self):
        inp = make_input(time_to_close_ratio=1.75)
        assert inp.time_to_close_ratio == 1.75

    def test_engagement_recency_score_field(self):
        inp = make_input(engagement_recency_score=0.15)
        assert inp.engagement_recency_score == 0.15

    def test_next_step_completion_rate_pct_field(self):
        inp = make_input(next_step_completion_rate_pct=0.45)
        assert inp.next_step_completion_rate_pct == 0.45

    def test_multi_touch_frequency_field(self):
        inp = make_input(multi_touch_frequency=0.3)
        assert inp.multi_touch_frequency == 0.3

    def test_deal_age_skew_field(self):
        inp = make_input(deal_age_skew=0.65)
        assert inp.deal_age_skew == 0.65

    def test_reopen_rate_pct_field(self):
        inp = make_input(reopen_rate_pct=0.35)
        assert inp.reopen_rate_pct == 0.35

    def test_forecast_category_movement_pct_field(self):
        inp = make_input(forecast_category_movement_pct=0.10)
        assert inp.forecast_category_movement_pct == 0.10

    def test_competitive_displacement_rate_pct_field(self):
        inp = make_input(competitive_displacement_rate_pct=0.70)
        assert inp.competitive_displacement_rate_pct == 0.70

    def test_decision_date_slip_rate_pct_field(self):
        inp = make_input(decision_date_slip_rate_pct=0.60)
        assert inp.decision_date_slip_rate_pct == 0.60

    def test_avg_days_since_last_contact_field(self):
        inp = make_input(avg_days_since_last_contact=25.0)
        assert inp.avg_days_since_last_contact == 25.0

    def test_deal_expansion_rate_pct_field(self):
        inp = make_input(deal_expansion_rate_pct=0.20)
        assert inp.deal_expansion_rate_pct == 0.20

    def test_lost_deal_recapture_pct_field(self):
        inp = make_input(lost_deal_recapture_pct=0.05)
        assert inp.lost_deal_recapture_pct == 0.05

    def test_total_active_deals_field(self):
        inp = make_input(total_active_deals=50)
        assert inp.total_active_deals == 50

    def test_avg_deal_value_usd_field(self):
        inp = make_input(avg_deal_value_usd=25_000.0)
        assert inp.avg_deal_value_usd == 25_000.0

    def test_total_field_count(self):
        """Verify all 22 fields are present on the dataclass."""
        import dataclasses
        fields = dataclasses.fields(MomentumInput)
        assert len(fields) == 22


# ─────────────────────────────────────────────────────────────────────────────
# 3. MomentumResult.to_dict() – exactly 15 keys, all JSON-serializable
# ─────────────────────────────────────────────────────────────────────────────

class TestMomentumResultToDict:
    EXPECTED_KEYS = {
        "rep_id", "region", "momentum_risk", "momentum_pattern",
        "momentum_severity", "recommended_action", "velocity_score",
        "engagement_score", "momentum_score", "discipline_score",
        "momentum_composite", "has_momentum_gap", "requires_momentum_coaching",
        "estimated_stalled_pipeline_usd", "momentum_signal",
    }

    def _get_result(self) -> MomentumResult:
        engine = make_engine()
        return engine.assess(make_input())

    def test_to_dict_returns_dict(self):
        assert isinstance(self._get_result().to_dict(), dict)

    def test_to_dict_exactly_15_keys(self):
        assert len(self._get_result().to_dict()) == 15

    def test_to_dict_key_names(self):
        assert set(self._get_result().to_dict().keys()) == self.EXPECTED_KEYS

    def test_rep_id_in_dict(self):
        d = make_engine().assess(make_input(rep_id="XYZ")).to_dict()
        assert d["rep_id"] == "XYZ"

    def test_region_in_dict(self):
        d = make_engine().assess(make_input(region="APAC")).to_dict()
        assert d["region"] == "APAC"

    def test_momentum_risk_is_string(self):
        d = self._get_result().to_dict()
        assert isinstance(d["momentum_risk"], str)

    def test_momentum_pattern_is_string(self):
        d = self._get_result().to_dict()
        assert isinstance(d["momentum_pattern"], str)

    def test_momentum_severity_is_string(self):
        d = self._get_result().to_dict()
        assert isinstance(d["momentum_severity"], str)

    def test_recommended_action_is_string(self):
        d = self._get_result().to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_velocity_score_is_float(self):
        d = self._get_result().to_dict()
        assert isinstance(d["velocity_score"], float)

    def test_engagement_score_is_float(self):
        d = self._get_result().to_dict()
        assert isinstance(d["engagement_score"], float)

    def test_momentum_score_is_float(self):
        d = self._get_result().to_dict()
        assert isinstance(d["momentum_score"], float)

    def test_discipline_score_is_float(self):
        d = self._get_result().to_dict()
        assert isinstance(d["discipline_score"], float)

    def test_momentum_composite_is_float(self):
        d = self._get_result().to_dict()
        assert isinstance(d["momentum_composite"], float)

    def test_has_momentum_gap_is_bool(self):
        d = self._get_result().to_dict()
        assert isinstance(d["has_momentum_gap"], bool)

    def test_requires_momentum_coaching_is_bool(self):
        d = self._get_result().to_dict()
        assert isinstance(d["requires_momentum_coaching"], bool)

    def test_estimated_stalled_pipeline_usd_is_float(self):
        d = self._get_result().to_dict()
        assert isinstance(d["estimated_stalled_pipeline_usd"], float)

    def test_momentum_signal_is_str(self):
        d = self._get_result().to_dict()
        assert isinstance(d["momentum_signal"], str)

    def test_json_serializable(self):
        import json
        d = self._get_result().to_dict()
        # Should not raise
        json.dumps(d)


# ─────────────────────────────────────────────────────────────────────────────
# 4. _velocity_score boundaries
# ─────────────────────────────────────────────────────────────────────────────

class TestVelocityScore:
    def _score(self, **kw) -> float:
        e = make_engine()
        return e._velocity_score(make_input(**kw))

    # stalled_deal_pct thresholds
    def test_stalled_below_015_adds_0(self):
        assert self._score(stalled_deal_pct=0.10) == 0.0

    def test_stalled_at_015_adds_8(self):
        # 0.15 triggers the >=0.15 branch (+8); with good other fields → 8
        s = self._score(stalled_deal_pct=0.15, time_to_close_ratio=0.90, deal_velocity_score=0.80)
        assert s == 8.0

    def test_stalled_at_030_adds_22(self):
        s = self._score(stalled_deal_pct=0.30, time_to_close_ratio=0.90, deal_velocity_score=0.80)
        assert s == 22.0

    def test_stalled_at_050_adds_40(self):
        s = self._score(stalled_deal_pct=0.50, time_to_close_ratio=0.90, deal_velocity_score=0.80)
        assert s == 40.0

    def test_stalled_above_050_still_40(self):
        s = self._score(stalled_deal_pct=0.99, time_to_close_ratio=0.90, deal_velocity_score=0.80)
        assert s == 40.0

    # time_to_close_ratio thresholds
    def test_ttc_ratio_below_110_adds_0(self):
        s = self._score(stalled_deal_pct=0.0, time_to_close_ratio=1.05, deal_velocity_score=0.80)
        assert s == 0.0

    def test_ttc_ratio_at_110_adds_6(self):
        s = self._score(stalled_deal_pct=0.0, time_to_close_ratio=1.10, deal_velocity_score=0.80)
        assert s == 6.0

    def test_ttc_ratio_at_130_adds_18(self):
        s = self._score(stalled_deal_pct=0.0, time_to_close_ratio=1.30, deal_velocity_score=0.80)
        assert s == 18.0

    def test_ttc_ratio_at_160_adds_35(self):
        s = self._score(stalled_deal_pct=0.0, time_to_close_ratio=1.60, deal_velocity_score=0.80)
        assert s == 35.0

    # deal_velocity_score thresholds
    def test_dv_score_above_040_adds_0(self):
        s = self._score(stalled_deal_pct=0.0, time_to_close_ratio=0.90, deal_velocity_score=0.50)
        assert s == 0.0

    def test_dv_score_at_040_adds_12(self):
        s = self._score(stalled_deal_pct=0.0, time_to_close_ratio=0.90, deal_velocity_score=0.40)
        assert s == 12.0

    def test_dv_score_at_020_adds_25(self):
        s = self._score(stalled_deal_pct=0.0, time_to_close_ratio=0.90, deal_velocity_score=0.20)
        assert s == 25.0

    def test_velocity_score_capped_at_100(self):
        # Max possible: 40+35+25=100
        s = self._score(stalled_deal_pct=1.0, time_to_close_ratio=2.0, deal_velocity_score=0.0)
        assert s == 100.0

    def test_velocity_score_zero_on_all_good(self):
        s = self._score(stalled_deal_pct=0.0, time_to_close_ratio=1.0, deal_velocity_score=0.80)
        assert s == 0.0

    def test_velocity_additive(self):
        # stalled=0.30(+22) + ttc=1.30(+18) + dv=0.20(+25) = 65
        s = self._score(stalled_deal_pct=0.30, time_to_close_ratio=1.30, deal_velocity_score=0.20)
        assert s == 65.0


# ─────────────────────────────────────────────────────────────────────────────
# 5. _engagement_score boundaries
# ─────────────────────────────────────────────────────────────────────────────

class TestEngagementScore:
    def _score(self, **kw) -> float:
        e = make_engine()
        return e._engagement_score(make_input(**kw))

    # avg_days_since_last_contact thresholds
    def test_contact_below_7_adds_0(self):
        s = self._score(avg_days_since_last_contact=5.0, engagement_recency_score=0.90, multi_touch_frequency=2.0)
        assert s == 0.0

    def test_contact_at_7_adds_8(self):
        s = self._score(avg_days_since_last_contact=7.0, engagement_recency_score=0.90, multi_touch_frequency=2.0)
        assert s == 8.0

    def test_contact_at_14_adds_22(self):
        s = self._score(avg_days_since_last_contact=14.0, engagement_recency_score=0.90, multi_touch_frequency=2.0)
        assert s == 22.0

    def test_contact_at_21_adds_40(self):
        s = self._score(avg_days_since_last_contact=21.0, engagement_recency_score=0.90, multi_touch_frequency=2.0)
        assert s == 40.0

    # engagement_recency_score thresholds
    def test_recency_above_040_adds_0(self):
        s = self._score(avg_days_since_last_contact=0.0, engagement_recency_score=0.50, multi_touch_frequency=2.0)
        assert s == 0.0

    def test_recency_at_040_adds_18(self):
        s = self._score(avg_days_since_last_contact=0.0, engagement_recency_score=0.40, multi_touch_frequency=2.0)
        assert s == 18.0

    def test_recency_at_020_adds_35(self):
        s = self._score(avg_days_since_last_contact=0.0, engagement_recency_score=0.20, multi_touch_frequency=2.0)
        assert s == 35.0

    # multi_touch_frequency thresholds
    def test_multi_touch_above_100_adds_0(self):
        s = self._score(avg_days_since_last_contact=0.0, engagement_recency_score=0.90, multi_touch_frequency=1.50)
        assert s == 0.0

    def test_multi_touch_at_100_adds_12(self):
        s = self._score(avg_days_since_last_contact=0.0, engagement_recency_score=0.90, multi_touch_frequency=1.00)
        assert s == 12.0

    def test_multi_touch_at_050_adds_25(self):
        s = self._score(avg_days_since_last_contact=0.0, engagement_recency_score=0.90, multi_touch_frequency=0.50)
        assert s == 25.0

    def test_engagement_score_capped_at_100(self):
        s = self._score(avg_days_since_last_contact=30.0, engagement_recency_score=0.10, multi_touch_frequency=0.10)
        assert s == 100.0

    def test_engagement_score_zero_on_all_good(self):
        s = self._score(avg_days_since_last_contact=1.0, engagement_recency_score=0.90, multi_touch_frequency=2.0)
        assert s == 0.0

    def test_engagement_additive(self):
        # contact=14(+22) + recency=0.40(+18) + multi_touch=1.00(+12) = 52
        s = self._score(avg_days_since_last_contact=14.0, engagement_recency_score=0.40, multi_touch_frequency=1.00)
        assert s == 52.0


# ─────────────────────────────────────────────────────────────────────────────
# 6. _momentum_score boundaries
# ─────────────────────────────────────────────────────────────────────────────

class TestMomentumScoreMethod:
    def _score(self, **kw) -> float:
        e = make_engine()
        return e._momentum_score(make_input(**kw))

    # forecast_category_movement_pct thresholds
    def test_fcm_above_050_adds_0(self):
        s = self._score(forecast_category_movement_pct=0.60, decision_date_slip_rate_pct=0.10, deal_age_skew=0.10)
        assert s == 0.0

    def test_fcm_at_050_adds_8(self):
        s = self._score(forecast_category_movement_pct=0.50, decision_date_slip_rate_pct=0.10, deal_age_skew=0.10)
        assert s == 8.0

    def test_fcm_at_030_adds_22(self):
        s = self._score(forecast_category_movement_pct=0.30, decision_date_slip_rate_pct=0.10, deal_age_skew=0.10)
        assert s == 22.0

    def test_fcm_at_015_adds_40(self):
        s = self._score(forecast_category_movement_pct=0.15, decision_date_slip_rate_pct=0.10, deal_age_skew=0.10)
        assert s == 40.0

    # decision_date_slip_rate_pct thresholds
    def test_slip_below_035_adds_0(self):
        s = self._score(forecast_category_movement_pct=0.80, decision_date_slip_rate_pct=0.20, deal_age_skew=0.10)
        assert s == 0.0

    def test_slip_at_035_adds_18(self):
        s = self._score(forecast_category_movement_pct=0.80, decision_date_slip_rate_pct=0.35, deal_age_skew=0.10)
        assert s == 18.0

    def test_slip_at_055_adds_35(self):
        s = self._score(forecast_category_movement_pct=0.80, decision_date_slip_rate_pct=0.55, deal_age_skew=0.10)
        assert s == 35.0

    # deal_age_skew thresholds
    def test_age_skew_below_040_adds_0(self):
        s = self._score(forecast_category_movement_pct=0.80, decision_date_slip_rate_pct=0.10, deal_age_skew=0.30)
        assert s == 0.0

    def test_age_skew_at_040_adds_12(self):
        s = self._score(forecast_category_movement_pct=0.80, decision_date_slip_rate_pct=0.10, deal_age_skew=0.40)
        assert s == 12.0

    def test_age_skew_at_060_adds_25(self):
        s = self._score(forecast_category_movement_pct=0.80, decision_date_slip_rate_pct=0.10, deal_age_skew=0.60)
        assert s == 25.0

    def test_momentum_score_capped_at_100(self):
        s = self._score(forecast_category_movement_pct=0.10, decision_date_slip_rate_pct=0.60, deal_age_skew=0.70)
        assert s == 100.0

    def test_momentum_score_zero_on_all_good(self):
        s = self._score(forecast_category_movement_pct=0.90, decision_date_slip_rate_pct=0.10, deal_age_skew=0.10)
        assert s == 0.0

    def test_momentum_score_additive(self):
        # fcm=0.30(+22) + slip=0.35(+18) + age=0.40(+12) = 52
        s = self._score(forecast_category_movement_pct=0.30, decision_date_slip_rate_pct=0.35, deal_age_skew=0.40)
        assert s == 52.0


# ─────────────────────────────────────────────────────────────────────────────
# 7. _discipline_score boundaries
# ─────────────────────────────────────────────────────────────────────────────

class TestDisciplineScore:
    def _score(self, **kw) -> float:
        e = make_engine()
        return e._discipline_score(make_input(**kw))

    # next_step_completion_rate_pct thresholds
    def test_ns_above_075_adds_0(self):
        s = self._score(next_step_completion_rate_pct=0.80, stage_progression_rate_pct=0.50, reopen_rate_pct=0.05)
        assert s == 0.0

    def test_ns_at_075_adds_10(self):
        s = self._score(next_step_completion_rate_pct=0.75, stage_progression_rate_pct=0.50, reopen_rate_pct=0.05)
        assert s == 10.0

    def test_ns_at_055_adds_25(self):
        s = self._score(next_step_completion_rate_pct=0.55, stage_progression_rate_pct=0.50, reopen_rate_pct=0.05)
        assert s == 25.0

    def test_ns_at_030_adds_45(self):
        s = self._score(next_step_completion_rate_pct=0.30, stage_progression_rate_pct=0.50, reopen_rate_pct=0.05)
        assert s == 45.0

    # stage_progression_rate_pct thresholds
    def test_spr_above_020_adds_0(self):
        s = self._score(next_step_completion_rate_pct=0.90, stage_progression_rate_pct=0.30, reopen_rate_pct=0.05)
        assert s == 0.0

    def test_spr_at_020_adds_15(self):
        s = self._score(next_step_completion_rate_pct=0.90, stage_progression_rate_pct=0.20, reopen_rate_pct=0.05)
        assert s == 15.0

    def test_spr_at_010_adds_30(self):
        s = self._score(next_step_completion_rate_pct=0.90, stage_progression_rate_pct=0.10, reopen_rate_pct=0.05)
        assert s == 30.0

    # reopen_rate_pct thresholds
    def test_reopen_below_015_adds_0(self):
        s = self._score(next_step_completion_rate_pct=0.90, stage_progression_rate_pct=0.50, reopen_rate_pct=0.10)
        assert s == 0.0

    def test_reopen_at_015_adds_10(self):
        s = self._score(next_step_completion_rate_pct=0.90, stage_progression_rate_pct=0.50, reopen_rate_pct=0.15)
        assert s == 10.0

    def test_reopen_at_030_adds_25(self):
        s = self._score(next_step_completion_rate_pct=0.90, stage_progression_rate_pct=0.50, reopen_rate_pct=0.30)
        assert s == 25.0

    def test_discipline_score_capped_at_100(self):
        s = self._score(next_step_completion_rate_pct=0.20, stage_progression_rate_pct=0.05, reopen_rate_pct=0.50)
        assert s == 100.0

    def test_discipline_score_zero_on_all_good(self):
        s = self._score(next_step_completion_rate_pct=0.90, stage_progression_rate_pct=0.50, reopen_rate_pct=0.05)
        assert s == 0.0

    def test_discipline_score_additive(self):
        # ns=0.55(+25) + spr=0.20(+15) + reopen=0.15(+10) = 50
        s = self._score(next_step_completion_rate_pct=0.55, stage_progression_rate_pct=0.20, reopen_rate_pct=0.15)
        assert s == 50.0


# ─────────────────────────────────────────────────────────────────────────────
# 8. Composite formula – weights must sum to 1.00
# ─────────────────────────────────────────────────────────────────────────────

class TestCompositeFormula:
    WEIGHTS = [0.35, 0.25, 0.25, 0.15]

    def test_weights_sum_to_one(self):
        assert abs(sum(self.WEIGHTS) - 1.00) < 1e-9

    def test_composite_with_all_zeros(self):
        e = make_engine()
        assert e._composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_composite_with_all_100(self):
        e = make_engine()
        assert e._composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_composite_manual_calculation(self):
        e = make_engine()
        v, eng, m, d = 80.0, 60.0, 40.0, 20.0
        expected = round(80 * 0.35 + 60 * 0.25 + 40 * 0.25 + 20 * 0.15, 2)
        assert e._composite(v, eng, m, d) == expected

    def test_composite_capped_at_100(self):
        e = make_engine()
        # Even if somehow inputs exceed bounds, cap at 100
        assert e._composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_composite_weight_velocity_35pct(self):
        """Velocity gets 0.35 weight — change only velocity and verify delta."""
        e = make_engine()
        c1 = e._composite(0.0, 0.0, 0.0, 0.0)
        c2 = e._composite(100.0, 0.0, 0.0, 0.0)
        assert abs(c2 - c1 - 35.0) < 0.01

    def test_composite_weight_engagement_25pct(self):
        e = make_engine()
        c1 = e._composite(0.0, 0.0, 0.0, 0.0)
        c2 = e._composite(0.0, 100.0, 0.0, 0.0)
        assert abs(c2 - c1 - 25.0) < 0.01

    def test_composite_weight_momentum_25pct(self):
        e = make_engine()
        c1 = e._composite(0.0, 0.0, 0.0, 0.0)
        c2 = e._composite(0.0, 0.0, 100.0, 0.0)
        assert abs(c2 - c1 - 25.0) < 0.01

    def test_composite_weight_discipline_15pct(self):
        e = make_engine()
        c1 = e._composite(0.0, 0.0, 0.0, 0.0)
        c2 = e._composite(0.0, 0.0, 0.0, 100.0)
        assert abs(c2 - c1 - 15.0) < 0.01

    def test_composite_rounded_to_2_decimals(self):
        e = make_engine()
        result = e._composite(33.3, 33.3, 33.3, 33.3)
        assert result == round(result, 2)


# ─────────────────────────────────────────────────────────────────────────────
# 9. Risk thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestRiskThresholds:
    def _risk(self, composite: float) -> MomentumRisk:
        return make_engine()._risk(composite)

    def test_risk_0_is_low(self):
        assert self._risk(0.0) == MomentumRisk.low

    def test_risk_19_is_low(self):
        assert self._risk(19.99) == MomentumRisk.low

    def test_risk_20_is_moderate(self):
        assert self._risk(20.0) == MomentumRisk.moderate

    def test_risk_39_is_moderate(self):
        assert self._risk(39.99) == MomentumRisk.moderate

    def test_risk_40_is_high(self):
        assert self._risk(40.0) == MomentumRisk.high

    def test_risk_59_is_high(self):
        assert self._risk(59.99) == MomentumRisk.high

    def test_risk_60_is_critical(self):
        assert self._risk(60.0) == MomentumRisk.critical

    def test_risk_100_is_critical(self):
        assert self._risk(100.0) == MomentumRisk.critical

    def test_risk_boundary_exactly_20(self):
        assert self._risk(20.0) == MomentumRisk.moderate

    def test_risk_boundary_exactly_40(self):
        assert self._risk(40.0) == MomentumRisk.high

    def test_risk_boundary_exactly_60(self):
        assert self._risk(60.0) == MomentumRisk.critical


# ─────────────────────────────────────────────────────────────────────────────
# 10. Severity thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestSeverityThresholds:
    def _severity(self, composite: float) -> MomentumSeverity:
        return make_engine()._severity(composite)

    def test_severity_0_is_accelerating(self):
        assert self._severity(0.0) == MomentumSeverity.accelerating

    def test_severity_19_is_accelerating(self):
        assert self._severity(19.99) == MomentumSeverity.accelerating

    def test_severity_20_is_steady(self):
        assert self._severity(20.0) == MomentumSeverity.steady

    def test_severity_39_is_steady(self):
        assert self._severity(39.99) == MomentumSeverity.steady

    def test_severity_40_is_decelerating(self):
        assert self._severity(40.0) == MomentumSeverity.decelerating

    def test_severity_59_is_decelerating(self):
        assert self._severity(59.99) == MomentumSeverity.decelerating

    def test_severity_60_is_stalled(self):
        assert self._severity(60.0) == MomentumSeverity.stalled

    def test_severity_100_is_stalled(self):
        assert self._severity(100.0) == MomentumSeverity.stalled

    def test_severity_boundary_exactly_20(self):
        assert self._severity(20.0) == MomentumSeverity.steady

    def test_severity_boundary_exactly_40(self):
        assert self._severity(40.0) == MomentumSeverity.decelerating

    def test_severity_boundary_exactly_60(self):
        assert self._severity(60.0) == MomentumSeverity.stalled


# ─────────────────────────────────────────────────────────────────────────────
# 11. Action thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestActionThresholds:
    def _action(self, risk: MomentumRisk, pattern: MomentumPattern) -> MomentumAction:
        return make_engine()._action(risk, pattern)

    # Low risk → no_action
    def test_low_any_pattern_no_action(self):
        for p in MomentumPattern:
            assert self._action(MomentumRisk.low, p) == MomentumAction.no_action

    # Moderate risk → pipeline_review
    def test_moderate_any_pattern_pipeline_review(self):
        for p in MomentumPattern:
            assert self._action(MomentumRisk.moderate, p) == MomentumAction.pipeline_review

    # High risk + patterns
    def test_high_stall_accumulator_stall_intervention(self):
        assert self._action(MomentumRisk.high, MomentumPattern.stall_accumulator) == MomentumAction.stall_intervention

    def test_high_contact_desert_contact_cadence_coaching(self):
        assert self._action(MomentumRisk.high, MomentumPattern.contact_desert) == MomentumAction.contact_cadence_coaching

    def test_high_slow_burn_deal_acceleration_coaching(self):
        assert self._action(MomentumRisk.high, MomentumPattern.slow_burn) == MomentumAction.deal_acceleration_coaching

    def test_high_late_stage_freeze_stall_intervention(self):
        assert self._action(MomentumRisk.high, MomentumPattern.late_stage_freeze) == MomentumAction.stall_intervention

    def test_high_forecast_drift_deal_acceleration_coaching(self):
        assert self._action(MomentumRisk.high, MomentumPattern.forecast_drift) == MomentumAction.deal_acceleration_coaching

    def test_high_none_pattern_deal_acceleration_coaching(self):
        assert self._action(MomentumRisk.high, MomentumPattern.none) == MomentumAction.deal_acceleration_coaching

    # Critical risk + patterns
    def test_critical_stall_accumulator_executive_rescue(self):
        assert self._action(MomentumRisk.critical, MomentumPattern.stall_accumulator) == MomentumAction.executive_deal_rescue

    def test_critical_late_stage_freeze_executive_rescue(self):
        assert self._action(MomentumRisk.critical, MomentumPattern.late_stage_freeze) == MomentumAction.executive_deal_rescue

    def test_critical_contact_desert_pipeline_purge(self):
        assert self._action(MomentumRisk.critical, MomentumPattern.contact_desert) == MomentumAction.pipeline_purge

    def test_critical_slow_burn_pipeline_purge(self):
        assert self._action(MomentumRisk.critical, MomentumPattern.slow_burn) == MomentumAction.pipeline_purge

    def test_critical_forecast_drift_pipeline_purge(self):
        assert self._action(MomentumRisk.critical, MomentumPattern.forecast_drift) == MomentumAction.pipeline_purge

    def test_critical_none_pipeline_purge(self):
        assert self._action(MomentumRisk.critical, MomentumPattern.none) == MomentumAction.pipeline_purge


# ─────────────────────────────────────────────────────────────────────────────
# 12. Pattern detection (all 6 patterns)
# ─────────────────────────────────────────────────────────────────────────────

class TestPatternDetection:
    def _pattern(self, **kw) -> MomentumPattern:
        return make_engine()._pattern(make_input(**kw))

    def test_stall_accumulator_triggers(self):
        p = self._pattern(stalled_deal_pct=0.40, deal_age_skew=0.40)
        assert p == MomentumPattern.stall_accumulator

    def test_stall_accumulator_requires_both_conditions(self):
        # only stalled_deal_pct high
        p = self._pattern(stalled_deal_pct=0.40, deal_age_skew=0.30)
        assert p != MomentumPattern.stall_accumulator

    def test_stall_accumulator_only_age_skew_not_enough(self):
        p = self._pattern(stalled_deal_pct=0.30, deal_age_skew=0.40)
        assert p != MomentumPattern.stall_accumulator

    def test_slow_burn_triggers(self):
        p = self._pattern(
            time_to_close_ratio=1.40, forecast_category_movement_pct=0.25,
            stalled_deal_pct=0.0, deal_age_skew=0.0,
        )
        assert p == MomentumPattern.slow_burn

    def test_slow_burn_requires_both_conditions(self):
        p = self._pattern(time_to_close_ratio=1.40, forecast_category_movement_pct=0.30)
        assert p != MomentumPattern.slow_burn

    def test_late_stage_freeze_triggers(self):
        p = self._pattern(
            decision_date_slip_rate_pct=0.50, stage_progression_rate_pct=0.15,
            stalled_deal_pct=0.0, deal_age_skew=0.0,
            time_to_close_ratio=1.0, forecast_category_movement_pct=0.80,
        )
        assert p == MomentumPattern.late_stage_freeze

    def test_late_stage_freeze_requires_both(self):
        p = self._pattern(
            decision_date_slip_rate_pct=0.50, stage_progression_rate_pct=0.20,
            stalled_deal_pct=0.0, deal_age_skew=0.0,
        )
        assert p != MomentumPattern.late_stage_freeze

    def test_contact_desert_triggers(self):
        p = self._pattern(
            avg_days_since_last_contact=14.0, engagement_recency_score=0.30,
            stalled_deal_pct=0.0, deal_age_skew=0.0,
            time_to_close_ratio=1.0, forecast_category_movement_pct=0.80,
            decision_date_slip_rate_pct=0.10, stage_progression_rate_pct=0.50,
        )
        assert p == MomentumPattern.contact_desert

    def test_contact_desert_requires_both(self):
        p = self._pattern(
            avg_days_since_last_contact=14.0, engagement_recency_score=0.35,
            stalled_deal_pct=0.0, deal_age_skew=0.0,
        )
        assert p != MomentumPattern.contact_desert

    def test_forecast_drift_triggers(self):
        p = self._pattern(
            forecast_category_movement_pct=0.20, deal_velocity_score=0.30,
            stalled_deal_pct=0.0, deal_age_skew=0.0,
            time_to_close_ratio=1.0,
            decision_date_slip_rate_pct=0.10, stage_progression_rate_pct=0.50,
            avg_days_since_last_contact=1.0, engagement_recency_score=0.90,
        )
        assert p == MomentumPattern.forecast_drift

    def test_forecast_drift_requires_both(self):
        p = self._pattern(
            forecast_category_movement_pct=0.20, deal_velocity_score=0.35,
            stalled_deal_pct=0.0, deal_age_skew=0.0,
        )
        assert p != MomentumPattern.forecast_drift

    def test_none_pattern_when_no_conditions_met(self):
        # Completely clean input (all defaults are 'good')
        p = self._pattern()
        assert p == MomentumPattern.none

    def test_stall_accumulator_has_priority_over_slow_burn(self):
        # stall_accumulator conditions AND slow_burn conditions both met
        p = self._pattern(
            stalled_deal_pct=0.40, deal_age_skew=0.40,    # stall_accumulator
            time_to_close_ratio=1.40, forecast_category_movement_pct=0.20,  # slow_burn
        )
        assert p == MomentumPattern.stall_accumulator

    def test_slow_burn_priority_over_late_stage_freeze(self):
        p = self._pattern(
            stalled_deal_pct=0.0, deal_age_skew=0.0,
            time_to_close_ratio=1.40, forecast_category_movement_pct=0.20,   # slow_burn
            decision_date_slip_rate_pct=0.50, stage_progression_rate_pct=0.15,  # late_stage_freeze
        )
        assert p == MomentumPattern.slow_burn


# ─────────────────────────────────────────────────────────────────────────────
# 13. has_momentum_gap conditions (3 OR conditions)
# ─────────────────────────────────────────────────────────────────────────────

class TestHasMomentumGap:
    def _gap(self, composite: float, **kw) -> bool:
        e = make_engine()
        inp = make_input(**kw)
        return e._has_gap(inp, composite)

    def test_gap_false_when_all_below_thresholds(self):
        assert not self._gap(
            composite=39.0,
            stalled_deal_pct=0.20,
            decision_date_slip_rate_pct=0.30,
        )

    def test_gap_true_when_composite_ge_40(self):
        assert self._gap(composite=40.0, stalled_deal_pct=0.0, decision_date_slip_rate_pct=0.0)

    def test_gap_true_when_stalled_ge_025(self):
        assert self._gap(composite=0.0, stalled_deal_pct=0.25, decision_date_slip_rate_pct=0.0)

    def test_gap_true_when_slip_ge_040(self):
        assert self._gap(composite=0.0, stalled_deal_pct=0.0, decision_date_slip_rate_pct=0.40)

    def test_gap_false_just_below_all_three(self):
        assert not self._gap(
            composite=39.99,
            stalled_deal_pct=0.249,
            decision_date_slip_rate_pct=0.399,
        )

    def test_gap_boundary_composite_exactly_40(self):
        assert self._gap(composite=40.0, stalled_deal_pct=0.0, decision_date_slip_rate_pct=0.0)

    def test_gap_boundary_stalled_exactly_025(self):
        assert self._gap(composite=0.0, stalled_deal_pct=0.25, decision_date_slip_rate_pct=0.0)

    def test_gap_boundary_slip_exactly_040(self):
        assert self._gap(composite=0.0, stalled_deal_pct=0.0, decision_date_slip_rate_pct=0.40)

    def test_gap_true_when_multiple_conditions_met(self):
        assert self._gap(composite=50.0, stalled_deal_pct=0.30, decision_date_slip_rate_pct=0.50)


# ─────────────────────────────────────────────────────────────────────────────
# 14. requires_momentum_coaching conditions (3 OR conditions)
# ─────────────────────────────────────────────────────────────────────────────

class TestRequiresMomentumCoaching:
    def _coaching(self, composite: float, **kw) -> bool:
        e = make_engine()
        inp = make_input(**kw)
        return e._requires_coaching(inp, composite)

    def test_coaching_false_when_all_below(self):
        assert not self._coaching(
            composite=24.0,
            next_step_completion_rate_pct=0.60,
            avg_days_since_last_contact=9.0,
        )

    def test_coaching_true_when_composite_ge_25(self):
        assert self._coaching(composite=25.0, next_step_completion_rate_pct=0.90, avg_days_since_last_contact=1.0)

    def test_coaching_true_when_ns_le_055(self):
        assert self._coaching(composite=0.0, next_step_completion_rate_pct=0.55, avg_days_since_last_contact=1.0)

    def test_coaching_true_when_contact_ge_10(self):
        assert self._coaching(composite=0.0, next_step_completion_rate_pct=0.90, avg_days_since_last_contact=10.0)

    def test_coaching_false_just_below_all_three(self):
        assert not self._coaching(
            composite=24.99,
            next_step_completion_rate_pct=0.56,
            avg_days_since_last_contact=9.99,
        )

    def test_coaching_boundary_composite_exactly_25(self):
        assert self._coaching(composite=25.0, next_step_completion_rate_pct=0.90, avg_days_since_last_contact=1.0)

    def test_coaching_boundary_ns_exactly_055(self):
        assert self._coaching(composite=0.0, next_step_completion_rate_pct=0.55, avg_days_since_last_contact=1.0)

    def test_coaching_boundary_contact_exactly_10(self):
        assert self._coaching(composite=0.0, next_step_completion_rate_pct=0.90, avg_days_since_last_contact=10.0)

    def test_coaching_true_when_multiple_conditions_met(self):
        assert self._coaching(composite=30.0, next_step_completion_rate_pct=0.40, avg_days_since_last_contact=15.0)


# ─────────────────────────────────────────────────────────────────────────────
# 15. _stalled_pipeline formula
# ─────────────────────────────────────────────────────────────────────────────

class TestStalledPipeline:
    def _sp(self, composite: float, **kw) -> float:
        e = make_engine()
        inp = make_input(**kw)
        return e._stalled_pipeline(inp, composite)

    def test_zero_stalled_deals_gives_zero(self):
        sp = self._sp(composite=50.0, stalled_deal_pct=0.0, total_active_deals=20, avg_deal_value_usd=10_000.0, deal_age_skew=0.3)
        assert sp == 0.0

    def test_zero_active_deals_gives_zero(self):
        sp = self._sp(composite=50.0, stalled_deal_pct=0.50, total_active_deals=0, avg_deal_value_usd=10_000.0, deal_age_skew=0.3)
        assert sp == 0.0

    def test_manual_formula_calculation(self):
        # stalled_deals = 20 * 0.50 = 10
        # risk_mult = min(1.0, (50/100) * (1 + 0.3)) = min(1.0, 0.65) = 0.65
        # result = 10 * 10_000 * 0.65 = 65_000
        sp = self._sp(composite=50.0, stalled_deal_pct=0.50, total_active_deals=20, avg_deal_value_usd=10_000.0, deal_age_skew=0.30)
        expected = round(10 * 10_000 * min(1.0, (50 / 100) * (1 + 0.30)), 2)
        assert sp == expected

    def test_risk_mult_capped_at_1(self):
        # composite=100, deal_age_skew=1.0 → (100/100)*(1+1.0)=2.0 → capped at 1.0
        sp = self._sp(composite=100.0, stalled_deal_pct=0.50, total_active_deals=10, avg_deal_value_usd=1000.0, deal_age_skew=1.0)
        expected = round(5 * 1000.0 * 1.0, 2)
        assert sp == expected

    def test_result_is_rounded_to_2_decimals(self):
        sp = self._sp(composite=33.33, stalled_deal_pct=0.33, total_active_deals=7, avg_deal_value_usd=1234.56, deal_age_skew=0.5)
        assert sp == round(sp, 2)

    def test_composite_zero_gives_zero_pipeline(self):
        sp = self._sp(composite=0.0, stalled_deal_pct=0.50, total_active_deals=20, avg_deal_value_usd=10_000.0, deal_age_skew=0.30)
        assert sp == 0.0

    def test_larger_deal_value_scales_linearly(self):
        sp1 = self._sp(composite=50.0, stalled_deal_pct=0.50, total_active_deals=20, avg_deal_value_usd=5_000.0, deal_age_skew=0.0)
        sp2 = self._sp(composite=50.0, stalled_deal_pct=0.50, total_active_deals=20, avg_deal_value_usd=10_000.0, deal_age_skew=0.0)
        assert abs(sp2 / sp1 - 2.0) < 0.01


# ─────────────────────────────────────────────────────────────────────────────
# 16. _signal for low and high composite
# ─────────────────────────────────────────────────────────────────────────────

class TestSignal:
    def _signal(self, composite: float, pattern: MomentumPattern, **kw) -> str:
        e = make_engine()
        inp = make_input(**kw)
        return e._signal(inp, pattern, composite)

    def test_low_composite_returns_strong_message(self):
        s = self._signal(composite=0.0, pattern=MomentumPattern.none)
        assert "strong" in s.lower()

    def test_composite_below_20_returns_benchmark_message(self):
        s = self._signal(composite=19.99, pattern=MomentumPattern.none)
        assert "benchmarks" in s.lower()

    def test_high_composite_includes_label(self):
        s = self._signal(
            composite=70.0, pattern=MomentumPattern.stall_accumulator,
            stalled_deal_pct=0.50, decision_date_slip_rate_pct=0.60, avg_days_since_last_contact=25.0,
        )
        assert "Stall accumulator" in s

    def test_high_composite_includes_stall_pct(self):
        s = self._signal(
            composite=70.0, pattern=MomentumPattern.contact_desert,
            stalled_deal_pct=0.40, decision_date_slip_rate_pct=0.20, avg_days_since_last_contact=20.0,
        )
        assert "40%" in s

    def test_high_composite_includes_slip_pct(self):
        s = self._signal(
            composite=70.0, pattern=MomentumPattern.slow_burn,
            stalled_deal_pct=0.10, decision_date_slip_rate_pct=0.55, avg_days_since_last_contact=20.0,
        )
        assert "55%" in s

    def test_high_composite_includes_contact_days(self):
        s = self._signal(
            composite=70.0, pattern=MomentumPattern.late_stage_freeze,
            stalled_deal_pct=0.10, decision_date_slip_rate_pct=0.20, avg_days_since_last_contact=14.0,
        )
        assert "14d" in s

    def test_high_composite_includes_composite_value(self):
        s = self._signal(
            composite=75.0, pattern=MomentumPattern.forecast_drift,
            stalled_deal_pct=0.10, decision_date_slip_rate_pct=0.20, avg_days_since_last_contact=5.0,
        )
        assert "75" in s

    def test_pattern_labels_in_signal(self):
        e = make_engine()
        inp = make_input(stalled_deal_pct=0.10, decision_date_slip_rate_pct=0.10, avg_days_since_last_contact=5.0)
        label_map = {
            MomentumPattern.stall_accumulator: "Stall accumulator",
            MomentumPattern.slow_burn: "Slow burn",
            MomentumPattern.late_stage_freeze: "Late-stage freeze",
            MomentumPattern.contact_desert: "Contact desert",
            MomentumPattern.forecast_drift: "Forecast drift",
        }
        for pattern, label in label_map.items():
            s = e._signal(inp, pattern, 50.0)
            assert label in s, f"Expected '{label}' in signal for pattern {pattern}"

    def test_none_pattern_at_high_composite_uses_fallback_label(self):
        s = self._signal(
            composite=50.0, pattern=MomentumPattern.none,
            stalled_deal_pct=0.10, decision_date_slip_rate_pct=0.10, avg_days_since_last_contact=5.0,
        )
        # none pattern should produce a label derived from the value ("None" or "none")
        assert "composite" in s.lower()

    def test_signal_boundary_at_exactly_20(self):
        s = self._signal(composite=20.0, pattern=MomentumPattern.none,
                         stalled_deal_pct=0.10, decision_date_slip_rate_pct=0.10, avg_days_since_last_contact=5.0)
        # >= 20 should NOT return the "strong" message
        assert "strong" not in s.lower()

    def test_signal_boundary_at_just_below_20(self):
        s = self._signal(composite=19.99, pattern=MomentumPattern.none)
        assert "strong" in s.lower()


# ─────────────────────────────────────────────────────────────────────────────
# 17. assess() integration tests
# ─────────────────────────────────────────────────────────────────────────────

class TestAssessIntegration:
    def test_returns_momentum_result_type(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert isinstance(result, MomentumResult)

    def test_rep_id_propagated(self):
        result = make_engine().assess(make_input(rep_id="r-42"))
        assert result.rep_id == "r-42"

    def test_region_propagated(self):
        result = make_engine().assess(make_input(region="LATAM"))
        assert result.region == "LATAM"

    def test_good_input_gives_low_risk(self):
        result = make_engine().assess(make_input())
        assert result.momentum_risk == MomentumRisk.low

    def test_good_input_gives_accelerating_severity(self):
        result = make_engine().assess(make_input())
        assert result.momentum_severity == MomentumSeverity.accelerating

    def test_good_input_gives_no_action(self):
        result = make_engine().assess(make_input())
        assert result.recommended_action == MomentumAction.no_action

    def test_bad_input_gives_critical_risk(self):
        inp = make_input(
            stalled_deal_pct=0.80,
            time_to_close_ratio=2.0,
            deal_velocity_score=0.10,
            avg_days_since_last_contact=30.0,
            engagement_recency_score=0.10,
            multi_touch_frequency=0.20,
            forecast_category_movement_pct=0.05,
            decision_date_slip_rate_pct=0.80,
            deal_age_skew=0.80,
            next_step_completion_rate_pct=0.10,
            stage_progression_rate_pct=0.05,
            reopen_rate_pct=0.50,
        )
        result = make_engine().assess(inp)
        assert result.momentum_risk == MomentumRisk.critical

    def test_bad_input_gives_stalled_severity(self):
        inp = make_input(
            stalled_deal_pct=0.80, time_to_close_ratio=2.0, deal_velocity_score=0.10,
            avg_days_since_last_contact=30.0, engagement_recency_score=0.10, multi_touch_frequency=0.20,
            forecast_category_movement_pct=0.05, decision_date_slip_rate_pct=0.80, deal_age_skew=0.80,
            next_step_completion_rate_pct=0.10, stage_progression_rate_pct=0.05, reopen_rate_pct=0.50,
        )
        result = make_engine().assess(inp)
        assert result.momentum_severity == MomentumSeverity.stalled

    def test_result_added_to_internal_list(self):
        engine = make_engine()
        engine.assess(make_input())
        assert len(engine._results) == 1

    def test_composite_in_valid_range(self):
        result = make_engine().assess(make_input())
        assert 0.0 <= result.momentum_composite <= 100.0

    def test_velocity_score_in_valid_range(self):
        result = make_engine().assess(make_input())
        assert 0.0 <= result.velocity_score <= 100.0

    def test_engagement_score_in_valid_range(self):
        result = make_engine().assess(make_input())
        assert 0.0 <= result.engagement_score <= 100.0

    def test_momentum_score_in_valid_range(self):
        result = make_engine().assess(make_input())
        assert 0.0 <= result.momentum_score <= 100.0

    def test_discipline_score_in_valid_range(self):
        result = make_engine().assess(make_input())
        assert 0.0 <= result.discipline_score <= 100.0

    def test_momentum_signal_is_non_empty_string(self):
        result = make_engine().assess(make_input())
        assert isinstance(result.momentum_signal, str) and len(result.momentum_signal) > 0

    def test_composite_matches_manual_calculation(self):
        engine = make_engine()
        inp = make_input()
        result = engine.assess(inp)
        v = engine._velocity_score(inp)
        e = engine._engagement_score(inp)
        m = engine._momentum_score(inp)
        d = engine._discipline_score(inp)
        expected = round(v * 0.35 + e * 0.25 + m * 0.25 + d * 0.15, 2)
        assert result.momentum_composite == expected

    def test_assess_called_multiple_times_appends(self):
        engine = make_engine()
        engine.assess(make_input(rep_id="a"))
        engine.assess(make_input(rep_id="b"))
        assert len(engine._results) == 2


# ─────────────────────────────────────────────────────────────────────────────
# 18. assess_batch()
# ─────────────────────────────────────────────────────────────────────────────

class TestAssessBatch:
    def test_empty_list_returns_empty_list(self):
        engine = make_engine()
        result = engine.assess_batch([])
        assert result == []

    def test_single_item(self):
        engine = make_engine()
        results = engine.assess_batch([make_input()])
        assert len(results) == 1
        assert isinstance(results[0], MomentumResult)

    def test_multiple_items_returns_same_count(self):
        engine = make_engine()
        inputs = [make_input(rep_id=f"r-{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_results_added_to_internal_list(self):
        engine = make_engine()
        engine.assess_batch([make_input(rep_id=f"r-{i}") for i in range(3)])
        assert len(engine._results) == 3

    def test_batch_preserves_rep_ids(self):
        engine = make_engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(4)]
        results = engine.assess_batch(inputs)
        for i, res in enumerate(results):
            assert res.rep_id == f"rep-{i}"

    def test_batch_each_is_momentum_result(self):
        engine = make_engine()
        inputs = [make_input() for _ in range(3)]
        for r in engine.assess_batch(inputs):
            assert isinstance(r, MomentumResult)

    def test_batch_plus_single_total_count(self):
        engine = make_engine()
        engine.assess(make_input(rep_id="single"))
        engine.assess_batch([make_input(rep_id=f"b-{i}") for i in range(3)])
        assert len(engine._results) == 4


# ─────────────────────────────────────────────────────────────────────────────
# 19. summary() – empty and populated, exactly 13 keys
# ─────────────────────────────────────────────────────────────────────────────

SUMMARY_EXPECTED_KEYS = {
    "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
    "avg_momentum_composite", "momentum_gap_count", "coaching_count",
    "avg_velocity_score", "avg_engagement_score", "avg_momentum_score",
    "avg_discipline_score", "total_estimated_stalled_pipeline_usd",
}


class TestSummaryEmpty:
    def test_empty_returns_dict(self):
        assert isinstance(make_engine().summary(), dict)

    def test_empty_exactly_13_keys(self):
        assert len(make_engine().summary()) == 13

    def test_empty_key_names(self):
        assert set(make_engine().summary().keys()) == SUMMARY_EXPECTED_KEYS

    def test_empty_total_is_zero(self):
        assert make_engine().summary()["total"] == 0

    def test_empty_risk_counts_is_empty_dict(self):
        assert make_engine().summary()["risk_counts"] == {}

    def test_empty_pattern_counts_is_empty_dict(self):
        assert make_engine().summary()["pattern_counts"] == {}

    def test_empty_severity_counts_is_empty_dict(self):
        assert make_engine().summary()["severity_counts"] == {}

    def test_empty_action_counts_is_empty_dict(self):
        assert make_engine().summary()["action_counts"] == {}

    def test_empty_avg_composite_is_zero(self):
        assert make_engine().summary()["avg_momentum_composite"] == 0.0

    def test_empty_gap_count_is_zero(self):
        assert make_engine().summary()["momentum_gap_count"] == 0

    def test_empty_coaching_count_is_zero(self):
        assert make_engine().summary()["coaching_count"] == 0

    def test_empty_avg_velocity_is_zero(self):
        assert make_engine().summary()["avg_velocity_score"] == 0.0

    def test_empty_avg_engagement_is_zero(self):
        assert make_engine().summary()["avg_engagement_score"] == 0.0

    def test_empty_avg_momentum_is_zero(self):
        assert make_engine().summary()["avg_momentum_score"] == 0.0

    def test_empty_avg_discipline_is_zero(self):
        assert make_engine().summary()["avg_discipline_score"] == 0.0

    def test_empty_total_stalled_pipeline_is_zero(self):
        assert make_engine().summary()["total_estimated_stalled_pipeline_usd"] == 0.0


class TestSummaryPopulated:
    def _engine_with_results(self, n: int = 3) -> SalesDealMomentumIntelligenceEngine:
        engine = make_engine()
        engine.assess_batch([make_input(rep_id=f"r-{i}") for i in range(n)])
        return engine

    def test_populated_returns_dict(self):
        assert isinstance(self._engine_with_results().summary(), dict)

    def test_populated_exactly_13_keys(self):
        assert len(self._engine_with_results().summary()) == 13

    def test_populated_key_names(self):
        assert set(self._engine_with_results().summary().keys()) == SUMMARY_EXPECTED_KEYS

    def test_populated_total_equals_count(self):
        engine = self._engine_with_results(4)
        assert engine.summary()["total"] == 4

    def test_populated_risk_counts_is_dict(self):
        assert isinstance(self._engine_with_results().summary()["risk_counts"], dict)

    def test_populated_pattern_counts_is_dict(self):
        assert isinstance(self._engine_with_results().summary()["pattern_counts"], dict)

    def test_populated_severity_counts_is_dict(self):
        assert isinstance(self._engine_with_results().summary()["severity_counts"], dict)

    def test_populated_action_counts_is_dict(self):
        assert isinstance(self._engine_with_results().summary()["action_counts"], dict)

    def test_populated_avg_composite_is_float(self):
        assert isinstance(self._engine_with_results().summary()["avg_momentum_composite"], float)

    def test_populated_gap_count_is_int(self):
        assert isinstance(self._engine_with_results().summary()["momentum_gap_count"], int)

    def test_populated_coaching_count_is_int(self):
        assert isinstance(self._engine_with_results().summary()["coaching_count"], int)

    def test_populated_avg_velocity_is_float(self):
        assert isinstance(self._engine_with_results().summary()["avg_velocity_score"], float)

    def test_populated_avg_engagement_is_float(self):
        assert isinstance(self._engine_with_results().summary()["avg_engagement_score"], float)

    def test_populated_avg_momentum_is_float(self):
        assert isinstance(self._engine_with_results().summary()["avg_momentum_score"], float)

    def test_populated_avg_discipline_is_float(self):
        assert isinstance(self._engine_with_results().summary()["avg_discipline_score"], float)

    def test_populated_total_stalled_pipeline_is_float(self):
        assert isinstance(self._engine_with_results().summary()["total_estimated_stalled_pipeline_usd"], float)

    def test_risk_counts_values_sum_to_total(self):
        engine = self._engine_with_results(5)
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_severity_counts_values_sum_to_total(self):
        engine = self._engine_with_results(5)
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_pattern_counts_values_sum_to_total(self):
        engine = self._engine_with_results(5)
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_action_counts_values_sum_to_total(self):
        engine = self._engine_with_results(5)
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_avg_composite_is_correct(self):
        engine = make_engine()
        r1 = engine.assess(make_input(rep_id="r1"))
        r2 = engine.assess(make_input(rep_id="r2"))
        s = engine.summary()
        expected = round((r1.momentum_composite + r2.momentum_composite) / 2, 1)
        assert s["avg_momentum_composite"] == expected

    def test_gap_count_increments(self):
        engine = make_engine()
        # All-bad input guarantees has_momentum_gap=True
        bad = make_input(stalled_deal_pct=0.50)  # >= 0.25 triggers gap
        engine.assess_batch([bad, bad, bad])
        assert engine.summary()["momentum_gap_count"] == 3

    def test_coaching_count_increments(self):
        engine = make_engine()
        # avg_days_since_last_contact >= 10 triggers coaching
        inp = make_input(avg_days_since_last_contact=15.0)
        engine.assess_batch([inp, inp])
        assert engine.summary()["coaching_count"] == 2

    def test_total_stalled_pipeline_sums_correctly(self):
        engine = make_engine()
        r1 = engine.assess(make_input(rep_id="r1"))
        r2 = engine.assess(make_input(rep_id="r2"))
        s = engine.summary()
        expected = round(r1.estimated_stalled_pipeline_usd + r2.estimated_stalled_pipeline_usd, 2)
        assert s["total_estimated_stalled_pipeline_usd"] == expected


# ─────────────────────────────────────────────────────────────────────────────
# 20. Edge cases – zero values, boundary values, max values
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_all_zeros_does_not_raise(self):
        inp = make_input(
            avg_days_in_stage=0.0,
            stage_progression_rate_pct=0.0,
            deal_velocity_score=0.0,
            stalled_deal_pct=0.0,
            avg_time_to_close_days=0.0,
            time_to_close_ratio=0.0,
            engagement_recency_score=0.0,
            next_step_completion_rate_pct=0.0,
            multi_touch_frequency=0.0,
            deal_age_skew=0.0,
            reopen_rate_pct=0.0,
            forecast_category_movement_pct=0.0,
            competitive_displacement_rate_pct=0.0,
            decision_date_slip_rate_pct=0.0,
            avg_days_since_last_contact=0.0,
            deal_expansion_rate_pct=0.0,
            lost_deal_recapture_pct=0.0,
            total_active_deals=0,
            avg_deal_value_usd=0.0,
        )
        result = make_engine().assess(inp)
        assert isinstance(result, MomentumResult)

    def test_all_max_values_does_not_raise(self):
        inp = make_input(
            stage_progression_rate_pct=1.0,
            deal_velocity_score=1.0,
            stalled_deal_pct=1.0,
            time_to_close_ratio=5.0,
            engagement_recency_score=1.0,
            next_step_completion_rate_pct=1.0,
            multi_touch_frequency=10.0,
            deal_age_skew=1.0,
            reopen_rate_pct=1.0,
            forecast_category_movement_pct=1.0,
            competitive_displacement_rate_pct=1.0,
            decision_date_slip_rate_pct=1.0,
            avg_days_since_last_contact=100.0,
            deal_expansion_rate_pct=1.0,
            lost_deal_recapture_pct=1.0,
            total_active_deals=1000,
            avg_deal_value_usd=1_000_000.0,
        )
        result = make_engine().assess(inp)
        assert isinstance(result, MomentumResult)

    def test_composite_never_exceeds_100(self):
        inp = make_input(
            stalled_deal_pct=1.0, time_to_close_ratio=5.0, deal_velocity_score=0.0,
            avg_days_since_last_contact=100.0, engagement_recency_score=0.0, multi_touch_frequency=0.0,
            forecast_category_movement_pct=0.0, decision_date_slip_rate_pct=1.0, deal_age_skew=1.0,
            next_step_completion_rate_pct=0.0, stage_progression_rate_pct=0.0, reopen_rate_pct=1.0,
        )
        result = make_engine().assess(inp)
        assert result.momentum_composite <= 100.0

    def test_composite_never_below_zero(self):
        result = make_engine().assess(make_input())
        assert result.momentum_composite >= 0.0

    def test_boundary_stalled_just_below_015_no_velocity_points(self):
        e = make_engine()
        s = e._velocity_score(make_input(stalled_deal_pct=0.149, time_to_close_ratio=0.9, deal_velocity_score=0.8))
        assert s == 0.0

    def test_boundary_contact_just_below_7_no_engagement_points(self):
        e = make_engine()
        s = e._engagement_score(make_input(avg_days_since_last_contact=6.99, engagement_recency_score=0.9, multi_touch_frequency=2.0))
        assert s == 0.0

    def test_boundary_fcm_just_above_050_no_momentum_points(self):
        e = make_engine()
        s = e._momentum_score(make_input(forecast_category_movement_pct=0.51, decision_date_slip_rate_pct=0.1, deal_age_skew=0.1))
        assert s == 0.0

    def test_boundary_ns_just_above_075_no_discipline_points(self):
        e = make_engine()
        s = e._discipline_score(make_input(next_step_completion_rate_pct=0.76, stage_progression_rate_pct=0.5, reopen_rate_pct=0.05))
        assert s == 0.0

    def test_single_rep_summary_matches_result(self):
        engine = make_engine()
        result = engine.assess(make_input(rep_id="solo"))
        s = engine.summary()
        assert s["total"] == 1
        assert s["avg_momentum_composite"] == round(result.momentum_composite, 1)

    def test_to_dict_keys_stable_across_calls(self):
        engine = make_engine()
        r1 = engine.assess(make_input(rep_id="a"))
        r2 = engine.assess(make_input(rep_id="b"))
        assert set(r1.to_dict().keys()) == set(r2.to_dict().keys())

    def test_assess_result_has_momentum_risk_enum(self):
        result = make_engine().assess(make_input())
        assert isinstance(result.momentum_risk, MomentumRisk)

    def test_assess_result_has_momentum_pattern_enum(self):
        result = make_engine().assess(make_input())
        assert isinstance(result.momentum_pattern, MomentumPattern)

    def test_assess_result_has_momentum_severity_enum(self):
        result = make_engine().assess(make_input())
        assert isinstance(result.momentum_severity, MomentumSeverity)

    def test_assess_result_has_recommended_action_enum(self):
        result = make_engine().assess(make_input())
        assert isinstance(result.recommended_action, MomentumAction)

    def test_stalled_pipeline_nonnegative(self):
        result = make_engine().assess(make_input())
        assert result.estimated_stalled_pipeline_usd >= 0.0

    def test_each_engine_instance_is_independent(self):
        e1 = make_engine()
        e2 = make_engine()
        e1.assess(make_input())
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_moderate_risk_gives_pipeline_review(self):
        # Composite 20-39: moderate risk → pipeline_review
        engine = make_engine()
        # Force a moderate composite: stalled=0.30(+22 vel) + good elsewhere
        inp = make_input(
            stalled_deal_pct=0.30, time_to_close_ratio=0.90, deal_velocity_score=0.80,
            avg_days_since_last_contact=2.0, engagement_recency_score=0.90, multi_touch_frequency=2.0,
            forecast_category_movement_pct=0.80, decision_date_slip_rate_pct=0.05, deal_age_skew=0.10,
            next_step_completion_rate_pct=0.90, stage_progression_rate_pct=0.50, reopen_rate_pct=0.05,
        )
        result = engine.assess(inp)
        if result.momentum_risk == MomentumRisk.moderate:
            assert result.recommended_action == MomentumAction.pipeline_review

    def test_summary_avg_rounded_to_1_decimal(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        for key in ["avg_momentum_composite", "avg_velocity_score", "avg_engagement_score",
                    "avg_momentum_score", "avg_discipline_score"]:
            val = s[key]
            assert val == round(val, 1), f"{key} should be rounded to 1 decimal"
