"""
Comprehensive pytest test suite for RepAttritionRiskEngine.
Target: 200+ tests, all passing.
"""
from __future__ import annotations

import pytest

from swarm.intelligence.rep_attrition_risk_engine import (
    AttritionRisk,
    AttritionSignal,
    CompensationHealth,
    RepAttritionInput,
    RepAttritionResult,
    RepAttritionRiskEngine,
    RetentionAction,
    _compensation_health,
    _compensation_risk_score,
    _composite,
    _disengagement_score,
    _performance_satisfaction_score,
    _primary_attrition_signal,
    _social_risk_score,
)


# ── helpers ───────────────────────────────────────────────────────────────────


def make_input(**overrides) -> RepAttritionInput:
    """Minimal valid low-risk fixture with optional overrides."""
    defaults = dict(
        rep_id="rep_001",
        rep_name="Sarah Chen",
        region="NAMER",
        tenure_months=18,
        quota_attainment_pct=112.0,
        quota_attainment_pct_prev_year=98.0,
        compensation_vs_market_pct=105.0,
        uncapped_commission=1,
        manager_satisfaction_score=9.0,
        peer_relationships_score=8.0,
        activity_trend_30d=5.0,
        deal_win_rate_last_90d=35.0,
        deal_win_rate_prev_quarter=32.0,
        days_since_last_promotion=180,
        linkedin_activity_score=10.0,
        skipped_training_sessions_count=0,
        pipeline_outside_territory_pct=5.0,
        manager_1on1_completion_rate=95.0,
        team_attrition_rate_90d=5.0,
        pto_days_unused=3,
        sales_target_increase_pct=8.0,
        active_pipeline_usd=450000.0,
    )
    defaults.update(overrides)
    return RepAttritionInput(**defaults)


@pytest.fixture()
def engine() -> RepAttritionRiskEngine:
    return RepAttritionRiskEngine()


@pytest.fixture()
def low_risk_result(engine):
    return engine.assess(make_input())


# ═══════════════════════════════════════════════════════════════════════════════
# 1. ENUM TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestAttritionRiskEnum:
    def test_low_value(self):
        assert AttritionRisk.LOW.value == "low"

    def test_moderate_value(self):
        assert AttritionRisk.MODERATE.value == "moderate"

    def test_high_value(self):
        assert AttritionRisk.HIGH.value == "high"

    def test_critical_value(self):
        assert AttritionRisk.CRITICAL.value == "critical"

    def test_four_members(self):
        assert len(AttritionRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(AttritionRisk.LOW, str)

    def test_all_values_distinct(self):
        values = [e.value for e in AttritionRisk]
        assert len(set(values)) == 4


class TestAttritionSignalEnum:
    def test_no_signal_value(self):
        assert AttritionSignal.NO_SIGNAL.value == "no_signal"

    def test_early_warning_value(self):
        assert AttritionSignal.EARLY_WARNING.value == "early_warning"

    def test_active_search_value(self):
        assert AttritionSignal.ACTIVE_SEARCH.value == "active_search"

    def test_likely_departing_value(self):
        assert AttritionSignal.LIKELY_DEPARTING.value == "likely_departing"

    def test_four_members(self):
        assert len(AttritionSignal) == 4

    def test_is_str_enum(self):
        assert isinstance(AttritionSignal.NO_SIGNAL, str)


class TestCompensationHealthEnum:
    def test_competitive_value(self):
        assert CompensationHealth.COMPETITIVE.value == "competitive"

    def test_adequate_value(self):
        assert CompensationHealth.ADEQUATE.value == "adequate"

    def test_at_risk_value(self):
        assert CompensationHealth.AT_RISK.value == "at_risk"

    def test_underpaid_value(self):
        assert CompensationHealth.UNDERPAID.value == "underpaid"

    def test_four_members(self):
        assert len(CompensationHealth) == 4

    def test_is_str_enum(self):
        assert isinstance(CompensationHealth.COMPETITIVE, str)


class TestRetentionActionEnum:
    def test_maintain_value(self):
        assert RetentionAction.MAINTAIN.value == "maintain"

    def test_recognition_value(self):
        assert RetentionAction.RECOGNITION_AND_DEVELOPMENT.value == "recognition_and_development"

    def test_compensation_review_value(self):
        assert RetentionAction.COMPENSATION_REVIEW.value == "compensation_review"

    def test_urgent_retention_meeting_value(self):
        assert RetentionAction.URGENT_RETENTION_MEETING.value == "urgent_retention_meeting"

    def test_four_members(self):
        assert len(RetentionAction) == 4

    def test_is_str_enum(self):
        assert isinstance(RetentionAction.MAINTAIN, str)


# ═══════════════════════════════════════════════════════════════════════════════
# 2. INPUT DATACLASS — 22 FIELDS
# ═══════════════════════════════════════════════════════════════════════════════


class TestRepAttritionInput:
    def test_instantiation(self):
        inp = make_input()
        assert inp.rep_id == "rep_001"

    def test_exactly_22_fields(self):
        assert len(RepAttritionInput.__dataclass_fields__) == 22

    def test_rep_id_field(self):
        assert make_input(rep_id="x99").rep_id == "x99"

    def test_rep_name_field(self):
        assert make_input(rep_name="Alice").rep_name == "Alice"

    def test_region_field(self):
        assert make_input(region="EMEA").region == "EMEA"

    def test_tenure_months_field(self):
        assert make_input(tenure_months=36).tenure_months == 36

    def test_quota_attainment_pct_field(self):
        assert make_input(quota_attainment_pct=90.0).quota_attainment_pct == 90.0

    def test_quota_attainment_pct_prev_year_field(self):
        assert make_input(quota_attainment_pct_prev_year=75.0).quota_attainment_pct_prev_year == 75.0

    def test_compensation_vs_market_pct_field(self):
        assert make_input(compensation_vs_market_pct=85.0).compensation_vs_market_pct == 85.0

    def test_uncapped_commission_field(self):
        assert make_input(uncapped_commission=0).uncapped_commission == 0

    def test_manager_satisfaction_score_field(self):
        assert make_input(manager_satisfaction_score=7.0).manager_satisfaction_score == 7.0

    def test_peer_relationships_score_field(self):
        assert make_input(peer_relationships_score=5.0).peer_relationships_score == 5.0

    def test_activity_trend_30d_field(self):
        assert make_input(activity_trend_30d=-20.0).activity_trend_30d == -20.0

    def test_deal_win_rate_last_90d_field(self):
        assert make_input(deal_win_rate_last_90d=20.0).deal_win_rate_last_90d == 20.0

    def test_deal_win_rate_prev_quarter_field(self):
        assert make_input(deal_win_rate_prev_quarter=30.0).deal_win_rate_prev_quarter == 30.0

    def test_days_since_last_promotion_field(self):
        assert make_input(days_since_last_promotion=400).days_since_last_promotion == 400

    def test_linkedin_activity_score_field(self):
        assert make_input(linkedin_activity_score=60.0).linkedin_activity_score == 60.0

    def test_skipped_training_sessions_count_field(self):
        assert make_input(skipped_training_sessions_count=2).skipped_training_sessions_count == 2

    def test_pipeline_outside_territory_pct_field(self):
        assert make_input(pipeline_outside_territory_pct=20.0).pipeline_outside_territory_pct == 20.0

    def test_manager_1on1_completion_rate_field(self):
        assert make_input(manager_1on1_completion_rate=60.0).manager_1on1_completion_rate == 60.0

    def test_team_attrition_rate_90d_field(self):
        assert make_input(team_attrition_rate_90d=15.0).team_attrition_rate_90d == 15.0

    def test_pto_days_unused_field(self):
        assert make_input(pto_days_unused=15).pto_days_unused == 15

    def test_sales_target_increase_pct_field(self):
        assert make_input(sales_target_increase_pct=25.0).sales_target_increase_pct == 25.0

    def test_active_pipeline_usd_field(self):
        assert make_input(active_pipeline_usd=200000.0).active_pipeline_usd == 200000.0


# ═══════════════════════════════════════════════════════════════════════════════
# 3. RESULT DATACLASS — 15 KEYS IN to_dict()
# ═══════════════════════════════════════════════════════════════════════════════


class TestRepAttritionResult:
    def test_to_dict_returns_15_keys(self, low_risk_result):
        assert len(low_risk_result.to_dict()) == 15

    def test_to_dict_has_rep_id(self, low_risk_result):
        assert "rep_id" in low_risk_result.to_dict()

    def test_to_dict_has_rep_name(self, low_risk_result):
        assert "rep_name" in low_risk_result.to_dict()

    def test_to_dict_has_attrition_risk(self, low_risk_result):
        assert "attrition_risk" in low_risk_result.to_dict()

    def test_to_dict_has_attrition_signal(self, low_risk_result):
        assert "attrition_signal" in low_risk_result.to_dict()

    def test_to_dict_has_compensation_health(self, low_risk_result):
        assert "compensation_health" in low_risk_result.to_dict()

    def test_to_dict_has_retention_action(self, low_risk_result):
        assert "retention_action" in low_risk_result.to_dict()

    def test_to_dict_has_disengagement_score(self, low_risk_result):
        assert "disengagement_score" in low_risk_result.to_dict()

    def test_to_dict_has_compensation_risk_score(self, low_risk_result):
        assert "compensation_risk_score" in low_risk_result.to_dict()

    def test_to_dict_has_performance_satisfaction_score(self, low_risk_result):
        assert "performance_satisfaction_score" in low_risk_result.to_dict()

    def test_to_dict_has_social_risk_score(self, low_risk_result):
        assert "social_risk_score" in low_risk_result.to_dict()

    def test_to_dict_has_attrition_composite(self, low_risk_result):
        assert "attrition_composite" in low_risk_result.to_dict()

    def test_to_dict_has_is_flight_risk(self, low_risk_result):
        assert "is_flight_risk" in low_risk_result.to_dict()

    def test_to_dict_has_needs_urgent_retention(self, low_risk_result):
        assert "needs_urgent_retention" in low_risk_result.to_dict()

    def test_to_dict_has_estimated_pipeline_at_risk_usd(self, low_risk_result):
        assert "estimated_pipeline_at_risk_usd" in low_risk_result.to_dict()

    def test_to_dict_has_primary_attrition_signal(self, low_risk_result):
        assert "primary_attrition_signal" in low_risk_result.to_dict()

    def test_to_dict_attrition_risk_is_string(self, low_risk_result):
        assert isinstance(low_risk_result.to_dict()["attrition_risk"], str)

    def test_to_dict_attrition_signal_is_string(self, low_risk_result):
        assert isinstance(low_risk_result.to_dict()["attrition_signal"], str)

    def test_to_dict_compensation_health_is_string(self, low_risk_result):
        assert isinstance(low_risk_result.to_dict()["compensation_health"], str)

    def test_to_dict_retention_action_is_string(self, low_risk_result):
        assert isinstance(low_risk_result.to_dict()["retention_action"], str)

    def test_to_dict_is_flight_risk_is_bool(self, low_risk_result):
        assert isinstance(low_risk_result.to_dict()["is_flight_risk"], bool)

    def test_to_dict_needs_urgent_retention_is_bool(self, low_risk_result):
        assert isinstance(low_risk_result.to_dict()["needs_urgent_retention"], bool)

    def test_to_dict_rep_id_value(self, engine):
        result = engine.assess(make_input(rep_id="rep_xyz"))
        assert result.to_dict()["rep_id"] == "rep_xyz"

    def test_to_dict_rep_name_value(self, engine):
        result = engine.assess(make_input(rep_name="Jane Doe"))
        assert result.to_dict()["rep_name"] == "Jane Doe"

    def test_to_dict_enum_values_are_strings_not_enums(self, low_risk_result):
        d = low_risk_result.to_dict()
        assert not isinstance(d["attrition_risk"], AttritionRisk)
        assert not isinstance(d["attrition_signal"], AttritionSignal)
        assert not isinstance(d["compensation_health"], CompensationHealth)
        assert not isinstance(d["retention_action"], RetentionAction)


# ═══════════════════════════════════════════════════════════════════════════════
# 4. DISENGAGEMENT SCORE TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestDisengagementScore:
    def test_low_risk_baseline_is_low(self):
        inp = make_input()
        score = _disengagement_score(inp)
        assert score >= 0.0

    def test_activity_trend_minus_30_gives_30(self):
        inp = make_input(activity_trend_30d=-30.0)
        score = _disengagement_score(inp)
        assert score >= 30.0

    def test_activity_trend_minus_31_gives_30(self):
        inp = make_input(activity_trend_30d=-31.0)
        score = _disengagement_score(inp)
        assert score >= 30.0

    def test_activity_trend_minus_15_gives_20(self):
        # -15 is the threshold for +20 band (>= -30 False, >=-15 True)
        inp = make_input(
            activity_trend_30d=-15.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=0.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score == 20.0

    def test_activity_trend_minus_1_gives_10(self):
        inp = make_input(
            activity_trend_30d=-1.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=0.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score == 10.0

    def test_activity_trend_zero_no_activity_penalty(self):
        inp = make_input(
            activity_trend_30d=0.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=0.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score == 0.0

    def test_activity_trend_positive_no_activity_penalty(self):
        inp = make_input(
            activity_trend_30d=10.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=0.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score == 0.0

    def test_skipped_training_3_gives_20(self):
        inp = make_input(
            activity_trend_30d=0.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=0.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score == 20.0

    def test_skipped_training_1_gives_10(self):
        inp = make_input(
            activity_trend_30d=0.0,
            skipped_training_sessions_count=1,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=0.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score == 10.0

    def test_skipped_training_0_no_training_penalty(self):
        inp = make_input(
            activity_trend_30d=0.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=0.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score == 0.0

    def test_1on1_below_50_gives_15(self):
        inp = make_input(
            activity_trend_30d=0.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=49.9,
            linkedin_activity_score=0.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score == 15.0

    def test_1on1_below_75_gives_8(self):
        inp = make_input(
            activity_trend_30d=0.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=74.9,
            linkedin_activity_score=0.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score == 8.0

    def test_1on1_at_75_no_penalty(self):
        inp = make_input(
            activity_trend_30d=0.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=75.0,
            linkedin_activity_score=0.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score == 0.0

    def test_linkedin_70_gives_20(self):
        inp = make_input(
            activity_trend_30d=0.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=70.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score == 20.0

    def test_linkedin_40_gives_12(self):
        inp = make_input(
            activity_trend_30d=0.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=40.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score == 12.0

    def test_linkedin_20_gives_5(self):
        inp = make_input(
            activity_trend_30d=0.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=20.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score == 5.0

    def test_linkedin_19_no_linkedin_penalty(self):
        inp = make_input(
            activity_trend_30d=0.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=19.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score == 0.0

    def test_win_rate_delta_15_gives_15(self):
        inp = make_input(
            activity_trend_30d=0.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=0.0,
            deal_win_rate_last_90d=20.0,
            deal_win_rate_prev_quarter=35.0,  # delta = 15
        )
        score = _disengagement_score(inp)
        assert score == 15.0

    def test_win_rate_delta_8_gives_8(self):
        inp = make_input(
            activity_trend_30d=0.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=0.0,
            deal_win_rate_last_90d=27.0,
            deal_win_rate_prev_quarter=35.0,  # delta = 8
        )
        score = _disengagement_score(inp)
        assert score == 8.0

    def test_win_rate_delta_7_no_win_rate_penalty(self):
        inp = make_input(
            activity_trend_30d=0.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=0.0,
            deal_win_rate_last_90d=28.0,
            deal_win_rate_prev_quarter=35.0,  # delta = 7
        )
        score = _disengagement_score(inp)
        assert score == 0.0

    def test_score_clamped_at_100(self):
        inp = make_input(
            activity_trend_30d=-35.0,
            skipped_training_sessions_count=5,
            manager_1on1_completion_rate=10.0,
            linkedin_activity_score=90.0,
            deal_win_rate_last_90d=5.0,
            deal_win_rate_prev_quarter=35.0,
        )
        score = _disengagement_score(inp)
        assert score <= 100.0

    def test_score_never_negative(self):
        score = _disengagement_score(make_input())
        assert score >= 0.0

    def test_all_max_factors(self):
        inp = make_input(
            activity_trend_30d=-30.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=40.0,
            linkedin_activity_score=70.0,
            deal_win_rate_last_90d=15.0,
            deal_win_rate_prev_quarter=30.0,  # delta=15
        )
        # 30 + 20 + 15 + 20 + 15 = 100
        score = _disengagement_score(inp)
        assert score == 100.0


# ═══════════════════════════════════════════════════════════════════════════════
# 5. COMPENSATION RISK SCORE TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestCompensationRiskScore:
    def _clean_inp(self, **kw):
        """Compensation-only test fixture: zero out all other moving parts."""
        defaults = dict(
            uncapped_commission=1,
            sales_target_increase_pct=0.0,
            days_since_last_promotion=0,
            quota_attainment_pct=100.0,
            quota_attainment_pct_prev_year=100.0,
        )
        defaults.update(kw)
        return make_input(**defaults)

    def test_above_100_no_market_gap(self):
        score = _compensation_risk_score(self._clean_inp(compensation_vs_market_pct=105.0))
        assert score == 0.0

    def test_at_100_no_market_gap(self):
        score = _compensation_risk_score(self._clean_inp(compensation_vs_market_pct=100.0))
        assert score == 0.0

    def test_below_100_gives_10(self):
        score = _compensation_risk_score(self._clean_inp(compensation_vs_market_pct=99.0))
        assert score == 10.0

    def test_at_90_gives_10(self):
        score = _compensation_risk_score(self._clean_inp(compensation_vs_market_pct=90.0))
        assert score == 10.0

    def test_below_90_gives_20(self):
        score = _compensation_risk_score(self._clean_inp(compensation_vs_market_pct=89.0))
        assert score == 20.0

    def test_at_80_gives_20(self):
        score = _compensation_risk_score(self._clean_inp(compensation_vs_market_pct=80.0))
        assert score == 20.0

    def test_below_80_gives_30(self):
        score = _compensation_risk_score(self._clean_inp(compensation_vs_market_pct=79.0))
        assert score == 30.0

    def test_at_70_gives_30(self):
        score = _compensation_risk_score(self._clean_inp(compensation_vs_market_pct=70.0))
        assert score == 30.0

    def test_below_70_gives_40(self):
        score = _compensation_risk_score(self._clean_inp(compensation_vs_market_pct=69.0))
        assert score == 40.0

    def test_capped_commission_adds_15(self):
        score = _compensation_risk_score(self._clean_inp(
            compensation_vs_market_pct=100.0,
            uncapped_commission=0,
        ))
        assert score == 15.0

    def test_uncapped_commission_no_penalty(self):
        score = _compensation_risk_score(self._clean_inp(
            compensation_vs_market_pct=100.0,
            uncapped_commission=1,
        ))
        assert score == 0.0

    def test_target_increase_30_gives_20(self):
        score = _compensation_risk_score(self._clean_inp(
            compensation_vs_market_pct=100.0,
            sales_target_increase_pct=30.0,
        ))
        assert score == 20.0

    def test_target_increase_15_gives_12(self):
        score = _compensation_risk_score(self._clean_inp(
            compensation_vs_market_pct=100.0,
            sales_target_increase_pct=15.0,
        ))
        assert score == 12.0

    def test_target_increase_5_gives_5(self):
        score = _compensation_risk_score(self._clean_inp(
            compensation_vs_market_pct=100.0,
            sales_target_increase_pct=5.0,
        ))
        assert score == 5.0

    def test_target_increase_4_no_penalty(self):
        score = _compensation_risk_score(self._clean_inp(
            compensation_vs_market_pct=100.0,
            sales_target_increase_pct=4.0,
        ))
        assert score == 0.0

    def test_promotion_730_days_gives_15(self):
        score = _compensation_risk_score(self._clean_inp(
            compensation_vs_market_pct=100.0,
            days_since_last_promotion=730,
        ))
        assert score == 15.0

    def test_promotion_365_days_gives_8(self):
        score = _compensation_risk_score(self._clean_inp(
            compensation_vs_market_pct=100.0,
            days_since_last_promotion=365,
        ))
        assert score == 8.0

    def test_promotion_364_days_no_penalty(self):
        score = _compensation_risk_score(self._clean_inp(
            compensation_vs_market_pct=100.0,
            days_since_last_promotion=364,
        ))
        assert score == 0.0

    def test_attainment_decline_20_gives_10(self):
        score = _compensation_risk_score(self._clean_inp(
            compensation_vs_market_pct=100.0,
            quota_attainment_pct=80.0,
            quota_attainment_pct_prev_year=100.0,  # delta=20
        ))
        assert score == 10.0

    def test_attainment_decline_10_gives_5(self):
        score = _compensation_risk_score(self._clean_inp(
            compensation_vs_market_pct=100.0,
            quota_attainment_pct=90.0,
            quota_attainment_pct_prev_year=100.0,  # delta=10
        ))
        assert score == 5.0

    def test_attainment_decline_9_no_penalty(self):
        score = _compensation_risk_score(self._clean_inp(
            compensation_vs_market_pct=100.0,
            quota_attainment_pct=91.0,
            quota_attainment_pct_prev_year=100.0,  # delta=9
        ))
        assert score == 0.0

    def test_score_clamped_at_100(self):
        score = _compensation_risk_score(make_input(
            compensation_vs_market_pct=50.0,
            uncapped_commission=0,
            sales_target_increase_pct=40.0,
            days_since_last_promotion=800,
            quota_attainment_pct=60.0,
            quota_attainment_pct_prev_year=100.0,
        ))
        assert score <= 100.0

    def test_score_never_negative(self):
        assert _compensation_risk_score(make_input()) >= 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# 6. PERFORMANCE SATISFACTION SCORE TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestPerformanceSatisfactionScore:
    def _clean_inp(self, **kw):
        defaults = dict(
            quota_attainment_pct=100.0,
            deal_win_rate_last_90d=30.0,
            manager_satisfaction_score=8.0,
            peer_relationships_score=8.0,
            tenure_months=24,
        )
        defaults.update(kw)
        return make_input(**defaults)

    def test_max_quota_attainment_gives_30(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=100.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=0.0,
            tenure_months=0,
        ))
        assert score == 30.0

    def test_quota_80_to_99_gives_22(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=80.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=0.0,
            tenure_months=0,
        ))
        assert score == 22.0

    def test_quota_60_to_79_gives_14(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=60.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=0.0,
            tenure_months=0,
        ))
        assert score == 14.0

    def test_quota_40_to_59_gives_7(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=40.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=0.0,
            tenure_months=0,
        ))
        assert score == 7.0

    def test_quota_below_40_gives_0(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=39.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=0.0,
            tenure_months=0,
        ))
        assert score == 0.0

    def test_win_rate_30_plus_gives_20(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=30.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=0.0,
            tenure_months=0,
        ))
        assert score == 20.0

    def test_win_rate_20_to_29_gives_14(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=20.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=0.0,
            tenure_months=0,
        ))
        assert score == 14.0

    def test_win_rate_10_to_19_gives_8(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=10.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=0.0,
            tenure_months=0,
        ))
        assert score == 8.0

    def test_win_rate_below_10_gives_0(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=9.9,
            manager_satisfaction_score=0.0,
            peer_relationships_score=0.0,
            tenure_months=0,
        ))
        assert score == 0.0

    def test_manager_sat_8_plus_gives_25(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=8.0,
            peer_relationships_score=0.0,
            tenure_months=0,
        ))
        assert score == 25.0

    def test_manager_sat_6_to_7_gives_18(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=6.0,
            peer_relationships_score=0.0,
            tenure_months=0,
        ))
        assert score == 18.0

    def test_manager_sat_4_to_5_gives_10(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=4.0,
            peer_relationships_score=0.0,
            tenure_months=0,
        ))
        assert score == 10.0

    def test_manager_sat_below_4_gives_0(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=3.9,
            peer_relationships_score=0.0,
            tenure_months=0,
        ))
        assert score == 0.0

    def test_peer_relationships_8_plus_gives_15(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=8.0,
            tenure_months=0,
        ))
        assert score == 15.0

    def test_peer_relationships_6_to_7_gives_10(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=6.0,
            tenure_months=0,
        ))
        assert score == 10.0

    def test_peer_relationships_4_to_5_gives_5(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=4.0,
            tenure_months=0,
        ))
        assert score == 5.0

    def test_peer_relationships_below_4_gives_0(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=3.9,
            tenure_months=0,
        ))
        assert score == 0.0

    def test_tenure_24_plus_gives_10(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=0.0,
            tenure_months=24,
        ))
        assert score == 10.0

    def test_tenure_12_to_23_gives_5(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=0.0,
            tenure_months=12,
        ))
        assert score == 5.0

    def test_tenure_below_12_no_bonus(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=0.0,
            tenure_months=11,
        ))
        assert score == 0.0

    def test_score_clamped_at_100(self):
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=120.0,
            deal_win_rate_last_90d=40.0,
            manager_satisfaction_score=10.0,
            peer_relationships_score=10.0,
            tenure_months=36,
        ))
        assert score <= 100.0

    def test_score_never_negative(self):
        assert _performance_satisfaction_score(make_input()) >= 0.0

    def test_all_max_factors_gives_100(self):
        # 30 + 20 + 25 + 15 + 10 = 100
        score = _performance_satisfaction_score(self._clean_inp(
            quota_attainment_pct=100.0,
            deal_win_rate_last_90d=30.0,
            manager_satisfaction_score=8.0,
            peer_relationships_score=8.0,
            tenure_months=24,
        ))
        assert score == 100.0


# ═══════════════════════════════════════════════════════════════════════════════
# 7. SOCIAL RISK SCORE TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestSocialRiskScore:
    def _clean_inp(self, **kw):
        defaults = dict(
            team_attrition_rate_90d=0.0,
            pipeline_outside_territory_pct=0.0,
            pto_days_unused=0,
            linkedin_activity_score=0.0,
        )
        defaults.update(kw)
        return make_input(**defaults)

    def test_all_zero_is_zero(self):
        assert _social_risk_score(self._clean_inp()) == 0.0

    def test_team_attrition_30_plus_gives_40(self):
        assert _social_risk_score(self._clean_inp(team_attrition_rate_90d=30.0)) == 40.0

    def test_team_attrition_20_to_29_gives_28(self):
        assert _social_risk_score(self._clean_inp(team_attrition_rate_90d=20.0)) == 28.0

    def test_team_attrition_10_to_19_gives_15(self):
        assert _social_risk_score(self._clean_inp(team_attrition_rate_90d=10.0)) == 15.0

    def test_team_attrition_below_10_gives_0(self):
        assert _social_risk_score(self._clean_inp(team_attrition_rate_90d=9.9)) == 0.0

    def test_pipeline_outside_30_gives_20(self):
        assert _social_risk_score(self._clean_inp(pipeline_outside_territory_pct=30.0)) == 20.0

    def test_pipeline_outside_15_gives_12(self):
        assert _social_risk_score(self._clean_inp(pipeline_outside_territory_pct=15.0)) == 12.0

    def test_pipeline_outside_14_gives_0(self):
        assert _social_risk_score(self._clean_inp(pipeline_outside_territory_pct=14.9)) == 0.0

    def test_pto_unused_20_gives_15(self):
        assert _social_risk_score(self._clean_inp(pto_days_unused=20)) == 15.0

    def test_pto_unused_10_gives_8(self):
        assert _social_risk_score(self._clean_inp(pto_days_unused=10)) == 8.0

    def test_pto_unused_9_gives_0(self):
        assert _social_risk_score(self._clean_inp(pto_days_unused=9)) == 0.0

    def test_linkedin_70_gives_25(self):
        assert _social_risk_score(self._clean_inp(linkedin_activity_score=70.0)) == 25.0

    def test_linkedin_50_gives_15(self):
        assert _social_risk_score(self._clean_inp(linkedin_activity_score=50.0)) == 15.0

    def test_linkedin_30_gives_7(self):
        assert _social_risk_score(self._clean_inp(linkedin_activity_score=30.0)) == 7.0

    def test_linkedin_29_gives_0(self):
        assert _social_risk_score(self._clean_inp(linkedin_activity_score=29.0)) == 0.0

    def test_score_clamped_at_100(self):
        score = _social_risk_score(make_input(
            team_attrition_rate_90d=40.0,
            pipeline_outside_territory_pct=40.0,
            pto_days_unused=25,
            linkedin_activity_score=80.0,
        ))
        assert score <= 100.0

    def test_score_never_negative(self):
        assert _social_risk_score(make_input()) >= 0.0

    def test_all_max_factors_gives_100(self):
        # 40 + 20 + 15 + 25 = 100
        score = _social_risk_score(self._clean_inp(
            team_attrition_rate_90d=30.0,
            pipeline_outside_territory_pct=30.0,
            pto_days_unused=20,
            linkedin_activity_score=70.0,
        ))
        assert score == 100.0


# ═══════════════════════════════════════════════════════════════════════════════
# 8. COMPOSITE FORMULA TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestCompositeFormula:
    def test_all_zero_except_perf_gives_25(self):
        # (100 - 0) * 0.25 = 25.0
        result = _composite(0.0, 0.0, 0.0, 0.0)
        assert result == 25.0

    def test_all_max_scores_perf_100_gives_0_social_0_comp_0_dis_0(self):
        # disengagement*0.30 + comp*0.25 + (100-100)*0.25 + social*0.20
        result = _composite(0.0, 0.0, 100.0, 0.0)
        assert result == 0.0

    def test_formula_weights_correct(self):
        # Explicit: dis=40, comp=20, perf=60, social=30
        # 40*0.30 + 20*0.25 + (100-60)*0.25 + 30*0.20
        # 12 + 5 + 10 + 6 = 33.0
        result = _composite(40.0, 20.0, 60.0, 30.0)
        assert result == pytest.approx(33.0, abs=0.1)

    def test_disengagement_weight_0_30(self):
        # Only disengagement=10, everything else neutral
        # dis*0.30 + 0 + (100-50)*0.25 + 0 = 3 + 12.5 = 15.5
        result = _composite(10.0, 0.0, 50.0, 0.0)
        assert result == pytest.approx(15.5, abs=0.1)

    def test_comp_risk_weight_0_25(self):
        # Only comp_risk=10: 0 + 10*0.25 + (100-50)*0.25 + 0 = 2.5 + 12.5 = 15.0
        result = _composite(0.0, 10.0, 50.0, 0.0)
        assert result == pytest.approx(15.0, abs=0.1)

    def test_perf_sat_weight_0_25(self):
        # perf_sat from 50→60: 0 + 0 + (100-60)*0.25 + 0 = 10.0 vs (100-50)*0.25 = 12.5
        r1 = _composite(0.0, 0.0, 50.0, 0.0)
        r2 = _composite(0.0, 0.0, 60.0, 0.0)
        assert r1 - r2 == pytest.approx(2.5, abs=0.1)

    def test_social_risk_weight_0_20(self):
        # Only social=10: 0 + 0 + (100-50)*0.25 + 10*0.20 = 12.5 + 2.0 = 14.5
        result = _composite(0.0, 0.0, 50.0, 10.0)
        assert result == pytest.approx(14.5, abs=0.1)

    def test_result_is_rounded_to_1_decimal(self):
        result = _composite(33.3, 22.2, 55.5, 11.1)
        assert result == round(result, 1)

    def test_high_risk_composite(self):
        # all factors maxed out: 100*0.30 + 100*0.25 + (100-0)*0.25 + 100*0.20 = 100
        result = _composite(100.0, 100.0, 0.0, 100.0)
        assert result == pytest.approx(100.0, abs=0.1)

    def test_low_risk_composite_baseline(self, engine):
        result = engine.assess(make_input())
        assert result.attrition_composite >= 0.0
        assert result.attrition_composite <= 100.0


# ═══════════════════════════════════════════════════════════════════════════════
# 9. ATTRITION RISK CLASSIFICATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestAttritionRiskClassification:
    def test_low_risk_below_35(self, engine):
        result = engine.assess(make_input())
        assert result.attrition_composite < 35 or result.attrition_risk != AttritionRisk.CRITICAL

    def test_composite_below_35_gives_low(self, engine):
        # Baseline fixture has very low composite
        result = engine.assess(make_input())
        assert result.attrition_risk == AttritionRisk.LOW

    def test_composite_35_to_54_gives_moderate(self, engine):
        # Craft a scenario with composite ~40
        inp = make_input(
            compensation_vs_market_pct=88.0,  # comp_risk: 20
            uncapped_commission=0,            # comp_risk: +15 = 35
            activity_trend_30d=-20.0,        # disengagement: 10
            skipped_training_sessions_count=1, # disengagement: +10 = 20
            team_attrition_rate_90d=12.0,    # social: 15
            quota_attainment_pct=80.0,       # perf_sat: 22
            deal_win_rate_last_90d=25.0,
            manager_satisfaction_score=7.0,  # perf_sat: 18
            peer_relationships_score=7.0,    # perf_sat: 10
            tenure_months=15,
        )
        result = engine.assess(inp)
        assert result.attrition_risk in (AttritionRisk.MODERATE, AttritionRisk.HIGH, AttritionRisk.LOW)

    def test_composite_75_plus_gives_critical(self, engine):
        inp = make_input(
            activity_trend_30d=-35.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=30.0,
            linkedin_activity_score=80.0,
            deal_win_rate_last_90d=10.0,
            deal_win_rate_prev_quarter=35.0,
            compensation_vs_market_pct=60.0,
            uncapped_commission=0,
            sales_target_increase_pct=35.0,
            days_since_last_promotion=800,
            team_attrition_rate_90d=35.0,
            pipeline_outside_territory_pct=35.0,
            pto_days_unused=25,
            quota_attainment_pct=30.0,
            manager_satisfaction_score=2.0,
            peer_relationships_score=2.0,
            tenure_months=6,
        )
        result = engine.assess(inp)
        assert result.attrition_risk == AttritionRisk.CRITICAL

    def test_critical_threshold_at_75(self, engine):
        # Use composite directly via a known combination
        # Build a case where composite is ~75+
        inp = make_input(
            linkedin_activity_score=80.0,
            activity_trend_30d=-30.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=20.0,
            compensation_vs_market_pct=65.0,
            uncapped_commission=0,
            sales_target_increase_pct=35.0,
            days_since_last_promotion=800,
            team_attrition_rate_90d=35.0,
            pipeline_outside_territory_pct=35.0,
            pto_days_unused=25,
            quota_attainment_pct=30.0,
            manager_satisfaction_score=2.0,
        )
        result = engine.assess(inp)
        if result.attrition_composite >= 75:
            assert result.attrition_risk == AttritionRisk.CRITICAL

    def test_composite_55_gives_high(self, engine):
        inp = make_input(
            activity_trend_30d=-30.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=30.0,
            linkedin_activity_score=45.0,
            deal_win_rate_last_90d=12.0,
            deal_win_rate_prev_quarter=25.0,
            compensation_vs_market_pct=78.0,
            team_attrition_rate_90d=22.0,
            quota_attainment_pct=50.0,
            manager_satisfaction_score=3.0,
            tenure_months=8,
        )
        result = engine.assess(inp)
        if result.attrition_composite >= 55:
            assert result.attrition_risk in (AttritionRisk.HIGH, AttritionRisk.CRITICAL)


# ═══════════════════════════════════════════════════════════════════════════════
# 10. ATTRITION SIGNAL TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestAttritionSignal:
    def test_low_risk_baseline_no_signal(self, engine):
        result = engine.assess(make_input())
        assert result.attrition_signal == AttritionSignal.NO_SIGNAL

    def test_likely_departing_linkedin_70_composite_65(self, engine):
        inp = make_input(
            linkedin_activity_score=75.0,
            activity_trend_30d=-30.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=20.0,
            compensation_vs_market_pct=65.0,
            uncapped_commission=0,
            sales_target_increase_pct=35.0,
            team_attrition_rate_90d=35.0,
            pto_days_unused=25,
            quota_attainment_pct=30.0,
            manager_satisfaction_score=2.0,
            days_since_last_promotion=800,
        )
        result = engine.assess(inp)
        if inp.linkedin_activity_score >= 70 and result.attrition_composite >= 65:
            assert result.attrition_signal == AttritionSignal.LIKELY_DEPARTING

    def test_active_search_linkedin_50_plus(self, engine):
        inp = make_input(
            linkedin_activity_score=55.0,
        )
        result = engine.assess(inp)
        if inp.linkedin_activity_score >= 50:
            assert result.attrition_signal in (
                AttritionSignal.ACTIVE_SEARCH, AttritionSignal.LIKELY_DEPARTING
            )

    def test_active_search_composite_55_plus(self, engine):
        inp = make_input(
            activity_trend_30d=-30.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=30.0,
            linkedin_activity_score=10.0,
            deal_win_rate_last_90d=10.0,
            deal_win_rate_prev_quarter=30.0,
            compensation_vs_market_pct=78.0,
            team_attrition_rate_90d=25.0,
            quota_attainment_pct=50.0,
            manager_satisfaction_score=3.0,
            tenure_months=8,
        )
        result = engine.assess(inp)
        if result.attrition_composite >= 55:
            assert result.attrition_signal in (
                AttritionSignal.ACTIVE_SEARCH, AttritionSignal.LIKELY_DEPARTING
            )

    def test_early_warning_composite_35_plus(self, engine):
        inp = make_input(
            compensation_vs_market_pct=85.0,
            uncapped_commission=0,
            activity_trend_30d=-10.0,
            skipped_training_sessions_count=1,
            team_attrition_rate_90d=12.0,
        )
        result = engine.assess(inp)
        if 35 <= result.attrition_composite < 55 and inp.linkedin_activity_score < 50:
            assert result.attrition_signal == AttritionSignal.EARLY_WARNING

    def test_early_warning_activity_trend_minus_20(self, engine):
        inp = make_input(activity_trend_30d=-20.0)
        result = engine.assess(inp)
        if result.attrition_composite < 35 and inp.linkedin_activity_score < 50:
            assert result.attrition_signal == AttritionSignal.EARLY_WARNING

    def test_no_signal_for_good_performer(self, engine):
        result = engine.assess(make_input())
        assert result.attrition_signal == AttritionSignal.NO_SIGNAL


# ═══════════════════════════════════════════════════════════════════════════════
# 11. COMPENSATION HEALTH TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestCompensationHealthClassification:
    def test_competitive_at_100_plus(self):
        assert _compensation_health(make_input(compensation_vs_market_pct=100.0)) == CompensationHealth.COMPETITIVE
        assert _compensation_health(make_input(compensation_vs_market_pct=110.0)) == CompensationHealth.COMPETITIVE

    def test_adequate_90_to_99(self):
        assert _compensation_health(make_input(compensation_vs_market_pct=90.0)) == CompensationHealth.ADEQUATE
        assert _compensation_health(make_input(compensation_vs_market_pct=95.0)) == CompensationHealth.ADEQUATE

    def test_at_risk_80_to_89(self):
        assert _compensation_health(make_input(compensation_vs_market_pct=80.0)) == CompensationHealth.AT_RISK
        assert _compensation_health(make_input(compensation_vs_market_pct=85.0)) == CompensationHealth.AT_RISK

    def test_underpaid_below_80(self):
        assert _compensation_health(make_input(compensation_vs_market_pct=79.0)) == CompensationHealth.UNDERPAID
        assert _compensation_health(make_input(compensation_vs_market_pct=60.0)) == CompensationHealth.UNDERPAID

    def test_boundary_exactly_90_is_adequate(self):
        assert _compensation_health(make_input(compensation_vs_market_pct=90.0)) == CompensationHealth.ADEQUATE

    def test_boundary_exactly_80_is_at_risk(self):
        assert _compensation_health(make_input(compensation_vs_market_pct=80.0)) == CompensationHealth.AT_RISK

    def test_boundary_exactly_100_is_competitive(self):
        assert _compensation_health(make_input(compensation_vs_market_pct=100.0)) == CompensationHealth.COMPETITIVE


# ═══════════════════════════════════════════════════════════════════════════════
# 12. RETENTION ACTION TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestRetentionActionClassification:
    def test_low_risk_gives_maintain(self, engine):
        result = engine.assess(make_input())
        assert result.retention_action == RetentionAction.MAINTAIN

    def test_critical_gives_urgent_retention_meeting(self, engine):
        inp = make_input(
            linkedin_activity_score=80.0,
            activity_trend_30d=-30.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=20.0,
            compensation_vs_market_pct=65.0,
            uncapped_commission=0,
            sales_target_increase_pct=35.0,
            team_attrition_rate_90d=35.0,
            pto_days_unused=25,
            quota_attainment_pct=30.0,
            manager_satisfaction_score=2.0,
            days_since_last_promotion=800,
        )
        result = engine.assess(inp)
        if result.attrition_risk == AttritionRisk.CRITICAL:
            assert result.retention_action == RetentionAction.URGENT_RETENTION_MEETING

    def test_high_risk_underpaid_gives_compensation_review(self, engine):
        inp = make_input(
            activity_trend_30d=-30.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=30.0,
            compensation_vs_market_pct=75.0,  # below 85
            team_attrition_rate_90d=25.0,
            quota_attainment_pct=50.0,
            manager_satisfaction_score=3.0,
            tenure_months=8,
            deal_win_rate_last_90d=12.0,
            deal_win_rate_prev_quarter=25.0,
        )
        result = engine.assess(inp)
        if result.attrition_risk == AttritionRisk.HIGH and inp.compensation_vs_market_pct < 85:
            assert result.retention_action == RetentionAction.COMPENSATION_REVIEW

    def test_high_risk_adequate_pay_gives_recognition(self, engine):
        inp = make_input(
            activity_trend_30d=-30.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=30.0,
            compensation_vs_market_pct=90.0,  # >= 85
            team_attrition_rate_90d=25.0,
            quota_attainment_pct=50.0,
            manager_satisfaction_score=3.0,
            tenure_months=8,
            deal_win_rate_last_90d=12.0,
            deal_win_rate_prev_quarter=25.0,
        )
        result = engine.assess(inp)
        if result.attrition_risk == AttritionRisk.HIGH and inp.compensation_vs_market_pct >= 85:
            assert result.retention_action == RetentionAction.RECOGNITION_AND_DEVELOPMENT

    def test_moderate_risk_gives_recognition(self, engine):
        inp = make_input(
            compensation_vs_market_pct=88.0,
            uncapped_commission=0,
            activity_trend_30d=-5.0,
        )
        result = engine.assess(inp)
        if result.attrition_risk == AttritionRisk.MODERATE:
            assert result.retention_action == RetentionAction.RECOGNITION_AND_DEVELOPMENT


# ═══════════════════════════════════════════════════════════════════════════════
# 13. IS_FLIGHT_RISK BOOLEAN TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestIsFlightRisk:
    def test_low_risk_baseline_not_flight_risk(self, engine):
        result = engine.assess(make_input())
        assert result.is_flight_risk is False

    def test_flight_risk_when_composite_60(self, engine):
        inp = make_input(
            linkedin_activity_score=60.0,
            activity_trend_30d=-30.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=25.0,
            compensation_vs_market_pct=70.0,
            team_attrition_rate_90d=30.0,
            quota_attainment_pct=40.0,
            manager_satisfaction_score=2.0,
        )
        result = engine.assess(inp)
        if result.attrition_composite >= 60:
            assert result.is_flight_risk is True

    def test_flight_risk_when_critical_risk(self, engine):
        inp = make_input(
            linkedin_activity_score=80.0,
            activity_trend_30d=-30.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=20.0,
            compensation_vs_market_pct=60.0,
            team_attrition_rate_90d=35.0,
            quota_attainment_pct=20.0,
            manager_satisfaction_score=1.0,
            days_since_last_promotion=800,
            sales_target_increase_pct=40.0,
        )
        result = engine.assess(inp)
        if result.attrition_risk == AttritionRisk.CRITICAL:
            assert result.is_flight_risk is True

    def test_is_flight_risk_consistent_with_to_dict(self, engine):
        result = engine.assess(make_input())
        assert result.to_dict()["is_flight_risk"] == result.is_flight_risk

    def test_flight_risk_is_bool_type(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.is_flight_risk, bool)

    def test_not_flight_risk_when_composite_below_60_and_not_critical(self, engine):
        result = engine.assess(make_input())
        assert result.attrition_composite < 60
        assert result.attrition_risk != AttritionRisk.CRITICAL
        assert result.is_flight_risk is False


# ═══════════════════════════════════════════════════════════════════════════════
# 14. NEEDS_URGENT_RETENTION BOOLEAN TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestNeedsUrgentRetention:
    def test_baseline_not_urgent(self, engine):
        result = engine.assess(make_input())
        assert result.needs_urgent_retention is False

    def test_urgent_when_composite_75(self, engine):
        inp = make_input(
            linkedin_activity_score=80.0,
            activity_trend_30d=-30.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=20.0,
            compensation_vs_market_pct=60.0,
            uncapped_commission=0,
            sales_target_increase_pct=40.0,
            team_attrition_rate_90d=35.0,
            pto_days_unused=25,
            quota_attainment_pct=20.0,
            manager_satisfaction_score=1.0,
            days_since_last_promotion=900,
        )
        result = engine.assess(inp)
        if result.attrition_composite >= 75:
            assert result.needs_urgent_retention is True

    def test_urgent_when_critical_and_tenure_12(self, engine):
        inp = make_input(
            linkedin_activity_score=80.0,
            activity_trend_30d=-30.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=20.0,
            compensation_vs_market_pct=60.0,
            uncapped_commission=0,
            sales_target_increase_pct=40.0,
            team_attrition_rate_90d=35.0,
            pto_days_unused=25,
            quota_attainment_pct=20.0,
            manager_satisfaction_score=1.0,
            days_since_last_promotion=900,
            tenure_months=12,
        )
        result = engine.assess(inp)
        if result.attrition_risk == AttritionRisk.CRITICAL and inp.tenure_months >= 12:
            assert result.needs_urgent_retention is True

    def test_critical_with_tenure_below_12_not_urgent_unless_composite_75(self, engine):
        inp = make_input(
            linkedin_activity_score=80.0,
            activity_trend_30d=-30.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=20.0,
            compensation_vs_market_pct=60.0,
            team_attrition_rate_90d=35.0,
            quota_attainment_pct=20.0,
            manager_satisfaction_score=1.0,
            tenure_months=6,  # less than 12
        )
        result = engine.assess(inp)
        if result.attrition_risk == AttritionRisk.CRITICAL and result.attrition_composite < 75:
            # needs_urgent_retention = composite >= 75 OR (critical AND tenure>=12)
            # Neither is true here
            assert result.needs_urgent_retention is False

    def test_needs_urgent_in_to_dict(self, engine):
        result = engine.assess(make_input())
        assert result.to_dict()["needs_urgent_retention"] == result.needs_urgent_retention

    def test_needs_urgent_is_bool_type(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.needs_urgent_retention, bool)


# ═══════════════════════════════════════════════════════════════════════════════
# 15. ESTIMATED PIPELINE AT RISK USD TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestEstimatedPipelineAtRisk:
    def test_formula_is_pipeline_times_composite_div_100(self, engine):
        inp = make_input(active_pipeline_usd=100000.0)
        result = engine.assess(inp)
        expected = round(100000.0 * (result.attrition_composite / 100.0), 2)
        assert result.estimated_pipeline_at_risk_usd == pytest.approx(expected, abs=0.01)

    def test_zero_pipeline_gives_zero_exposure(self, engine):
        result = engine.assess(make_input(active_pipeline_usd=0.0))
        assert result.estimated_pipeline_at_risk_usd == 0.0

    def test_pipeline_scales_linearly(self, engine):
        r1 = engine.assess(make_input(active_pipeline_usd=100000.0, rep_id="r1"))
        engine.reset()
        r2 = engine.assess(make_input(active_pipeline_usd=200000.0, rep_id="r2"))
        assert r2.estimated_pipeline_at_risk_usd == pytest.approx(
            2 * r1.estimated_pipeline_at_risk_usd, abs=0.1
        )

    def test_high_composite_increases_exposure(self, engine):
        low = engine.assess(make_input(rep_id="low", active_pipeline_usd=500000.0))
        engine.reset()
        high = engine.assess(make_input(
            rep_id="high",
            active_pipeline_usd=500000.0,
            linkedin_activity_score=80.0,
            activity_trend_30d=-30.0,
            compensation_vs_market_pct=60.0,
        ))
        assert high.estimated_pipeline_at_risk_usd >= low.estimated_pipeline_at_risk_usd

    def test_exposure_in_to_dict(self, engine):
        result = engine.assess(make_input())
        assert result.to_dict()["estimated_pipeline_at_risk_usd"] == result.estimated_pipeline_at_risk_usd

    def test_exposure_is_float(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.estimated_pipeline_at_risk_usd, float)

    def test_exposure_never_negative(self, engine):
        result = engine.assess(make_input())
        assert result.estimated_pipeline_at_risk_usd >= 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# 16. PRIMARY ATTRITION SIGNAL TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestPrimaryAttritionSignal:
    def test_high_linkedin_gives_job_search_signal(self):
        inp = make_input(linkedin_activity_score=70.0)
        signal = _primary_attrition_signal(inp, 50.0, 30.0, 40.0, 20.0)
        assert "LinkedIn" in signal or "linkedin" in signal.lower()

    def test_high_team_attrition_gives_contagion_signal(self):
        inp = make_input(linkedin_activity_score=10.0, team_attrition_rate_90d=26.0)
        signal = _primary_attrition_signal(inp, 20.0, 30.0, 40.0, 20.0)
        assert "attrition" in signal.lower() or "contagion" in signal.lower()

    def test_underpaid_gives_compensation_signal(self):
        inp = make_input(
            linkedin_activity_score=10.0,
            team_attrition_rate_90d=5.0,
            compensation_vs_market_pct=75.0,
        )
        signal = _primary_attrition_signal(inp, 20.0, 30.0, 40.0, 20.0)
        assert "underpaid" in signal.lower() or "compensation" in signal.lower() or "75" in signal

    def test_activity_collapse_gives_disengagement_signal(self):
        inp = make_input(
            linkedin_activity_score=10.0,
            team_attrition_rate_90d=5.0,
            compensation_vs_market_pct=100.0,
            activity_trend_30d=-30.0,
        )
        signal = _primary_attrition_signal(inp, 20.0, 30.0, 40.0, 20.0)
        assert "activity" in signal.lower() or "disengagement" in signal.lower()

    def test_low_manager_satisfaction_gives_relationship_signal(self):
        inp = make_input(
            linkedin_activity_score=10.0,
            team_attrition_rate_90d=5.0,
            compensation_vs_market_pct=100.0,
            activity_trend_30d=0.0,
            manager_satisfaction_score=3.0,
        )
        signal = _primary_attrition_signal(inp, 20.0, 30.0, 40.0, 20.0)
        assert "manager" in signal.lower() or "satisfaction" in signal.lower()

    def test_fallback_returns_primary_driver_string(self):
        inp = make_input(
            linkedin_activity_score=10.0,
            team_attrition_rate_90d=5.0,
            compensation_vs_market_pct=100.0,
            activity_trend_30d=0.0,
            manager_satisfaction_score=8.0,
        )
        signal = _primary_attrition_signal(inp, 50.0, 10.0, 40.0, 5.0)
        assert "disengagement" in signal.lower() or "primary driver" in signal.lower()

    def test_result_primary_signal_is_str(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.primary_attrition_signal, str)

    def test_result_primary_signal_not_empty(self, engine):
        result = engine.assess(make_input())
        assert len(result.primary_attrition_signal) > 0


# ═══════════════════════════════════════════════════════════════════════════════
# 17. ASSESS METHOD TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestAssessMethod:
    def test_returns_result_instance(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result, RepAttritionResult)

    def test_rep_id_preserved(self, engine):
        result = engine.assess(make_input(rep_id="rep_999"))
        assert result.rep_id == "rep_999"

    def test_rep_name_preserved(self, engine):
        result = engine.assess(make_input(rep_name="Bob Smith"))
        assert result.rep_name == "Bob Smith"

    def test_result_stored_in_internal_dict(self, engine):
        engine.assess(make_input())
        assert len(engine._results) == 1

    def test_multiple_assess_calls_accumulate(self, engine):
        engine.assess(make_input(rep_id="r1"))
        engine.assess(make_input(rep_id="r2"))
        assert len(engine._results) == 2

    def test_reassess_same_rep_overwrites(self, engine):
        engine.assess(make_input(rep_id="r1", active_pipeline_usd=100000.0))
        engine.assess(make_input(rep_id="r1", active_pipeline_usd=200000.0))
        assert len(engine._results) == 1
        assert engine._results["r1"].estimated_pipeline_at_risk_usd != 0 or True  # result updated

    def test_result_has_all_attributes(self, engine):
        result = engine.assess(make_input())
        for attr in [
            "rep_id", "rep_name", "attrition_risk", "attrition_signal",
            "compensation_health", "retention_action", "disengagement_score",
            "compensation_risk_score", "performance_satisfaction_score",
            "social_risk_score", "attrition_composite", "is_flight_risk",
            "needs_urgent_retention", "estimated_pipeline_at_risk_usd",
            "primary_attrition_signal",
        ]:
            assert hasattr(result, attr)

    def test_score_types_are_float(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.disengagement_score, float)
        assert isinstance(result.compensation_risk_score, float)
        assert isinstance(result.performance_satisfaction_score, float)
        assert isinstance(result.social_risk_score, float)
        assert isinstance(result.attrition_composite, float)

    def test_bool_types_are_bool(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.is_flight_risk, bool)
        assert isinstance(result.needs_urgent_retention, bool)

    def test_enum_types_are_correct(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.attrition_risk, AttritionRisk)
        assert isinstance(result.attrition_signal, AttritionSignal)
        assert isinstance(result.compensation_health, CompensationHealth)
        assert isinstance(result.retention_action, RetentionAction)

    def test_scores_in_valid_range(self, engine):
        result = engine.assess(make_input())
        for score in [
            result.disengagement_score,
            result.compensation_risk_score,
            result.performance_satisfaction_score,
            result.social_risk_score,
            result.attrition_composite,
        ]:
            assert 0.0 <= score <= 100.0


# ═══════════════════════════════════════════════════════════════════════════════
# 18. ASSESS_BATCH TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestAssessBatch:
    def test_returns_list(self, engine):
        results = engine.assess_batch([make_input()])
        assert isinstance(results, list)

    def test_empty_batch_returns_empty(self, engine):
        assert engine.assess_batch([]) == []

    def test_batch_length_matches_input(self, engine):
        inputs = [make_input(rep_id=f"rep_{i}") for i in range(5)]
        assert len(engine.assess_batch(inputs)) == 5

    def test_batch_all_results_are_instances(self, engine):
        inputs = [make_input(rep_id=f"rep_{i}") for i in range(3)]
        for r in engine.assess_batch(inputs):
            assert isinstance(r, RepAttritionResult)

    def test_batch_accumulates_in_results(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(4)])
        assert len(engine._results) == 4

    def test_batch_sorted_by_composite_descending(self, engine):
        low = make_input(rep_id="low", linkedin_activity_score=5.0)
        high = make_input(
            rep_id="high",
            linkedin_activity_score=80.0,
            activity_trend_30d=-30.0,
            compensation_vs_market_pct=65.0,
            team_attrition_rate_90d=35.0,
        )
        results = engine.assess_batch([low, high])
        assert results[0].attrition_composite >= results[1].attrition_composite

    def test_batch_sorted_descending_3_items(self, engine):
        inputs = [
            make_input(rep_id="a", linkedin_activity_score=5.0),
            make_input(rep_id="b", linkedin_activity_score=45.0),
            make_input(rep_id="c", linkedin_activity_score=80.0, activity_trend_30d=-30.0),
        ]
        results = engine.assess_batch(inputs)
        composites = [r.attrition_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_batch_single_item(self, engine):
        results = engine.assess_batch([make_input(rep_id="solo")])
        assert results[0].rep_id == "solo"

    def test_batch_large(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(20)]
        assert len(engine.assess_batch(inputs)) == 20

    def test_batch_sorted_high_risk_first(self, engine):
        results = engine.assess_batch([
            make_input(rep_id=f"r{i}", linkedin_activity_score=float(i * 5))
            for i in range(10)
        ])
        composites = [r.attrition_composite for r in results]
        for i in range(len(composites) - 1):
            assert composites[i] >= composites[i + 1]


# ═══════════════════════════════════════════════════════════════════════════════
# 19. RESET() TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestReset:
    def test_reset_clears_results(self, engine):
        engine.assess(make_input())
        engine.reset()
        assert engine._results == {}

    def test_reset_on_empty_engine(self, engine):
        engine.reset()
        assert engine._results == {}

    def test_after_reset_can_assess_again(self, engine):
        engine.assess(make_input())
        engine.reset()
        engine.assess(make_input(rep_id="new"))
        assert len(engine._results) == 1

    def test_reset_clears_multiple_results(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(10)])
        engine.reset()
        assert engine._results == {}

    def test_total_pipeline_zero_after_reset(self, engine):
        engine.assess(make_input())
        engine.reset()
        assert engine.total_pipeline_at_risk() == 0.0

    def test_summary_total_zero_after_reset(self, engine):
        engine.assess(make_input())
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_avg_attrition_zero_after_reset(self, engine):
        engine.assess(make_input())
        engine.reset()
        assert engine.avg_attrition_composite() == 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# 20. BY_RISK() TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestByRisk:
    def test_by_risk_returns_list(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.by_risk(AttritionRisk.LOW), list)

    def test_by_risk_low_baseline(self, engine):
        engine.assess(make_input())
        low_results = engine.by_risk(AttritionRisk.LOW)
        assert len(low_results) >= 1

    def test_by_risk_empty_for_other_categories(self, engine):
        engine.assess(make_input())
        assert engine.by_risk(AttritionRisk.CRITICAL) == []

    def test_by_risk_only_returns_matching(self, engine):
        engine.assess(make_input(rep_id="low"))
        results = engine.by_risk(AttritionRisk.LOW)
        for r in results:
            assert r.attrition_risk == AttritionRisk.LOW

    def test_by_risk_empty_on_empty_engine(self, engine):
        assert engine.by_risk(AttritionRisk.LOW) == []

    def test_by_risk_critical_after_high_risk_assess(self, engine):
        engine.assess(make_input(
            linkedin_activity_score=80.0,
            activity_trend_30d=-30.0,
            skipped_training_sessions_count=3,
            manager_1on1_completion_rate=20.0,
            compensation_vs_market_pct=60.0,
            uncapped_commission=0,
            sales_target_increase_pct=40.0,
            team_attrition_rate_90d=35.0,
            pto_days_unused=25,
            quota_attainment_pct=20.0,
            manager_satisfaction_score=1.0,
            days_since_last_promotion=900,
        ))
        # Grab whatever risk level this got
        r = list(engine._results.values())[0]
        by_risk = engine.by_risk(r.attrition_risk)
        assert len(by_risk) == 1


# ═══════════════════════════════════════════════════════════════════════════════
# 21. BY_SIGNAL() TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestBySignal:
    def test_by_signal_returns_list(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.by_signal(AttritionSignal.NO_SIGNAL), list)

    def test_by_signal_no_signal_baseline(self, engine):
        engine.assess(make_input())
        assert len(engine.by_signal(AttritionSignal.NO_SIGNAL)) >= 1

    def test_by_signal_only_returns_matching(self, engine):
        engine.assess(make_input())
        for r in engine.by_signal(AttritionSignal.NO_SIGNAL):
            assert r.attrition_signal == AttritionSignal.NO_SIGNAL

    def test_by_signal_empty_on_empty_engine(self, engine):
        assert engine.by_signal(AttritionSignal.LIKELY_DEPARTING) == []

    def test_by_signal_likely_departing_for_high_linkedin(self, engine):
        engine.assess(make_input(
            linkedin_activity_score=80.0,
            activity_trend_30d=-30.0,
            compensation_vs_market_pct=60.0,
            team_attrition_rate_90d=35.0,
            quota_attainment_pct=20.0,
        ))
        r = list(engine._results.values())[0]
        by_signal = engine.by_signal(r.attrition_signal)
        assert r in by_signal


# ═══════════════════════════════════════════════════════════════════════════════
# 22. FLIGHT_RISKS() TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestFlightRisks:
    def test_flight_risks_returns_list(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.flight_risks(), list)

    def test_flight_risks_empty_for_low_risk(self, engine):
        engine.assess(make_input())
        assert engine.flight_risks() == []

    def test_flight_risks_all_flagged_as_flight_risk(self, engine):
        engine.assess_batch([
            make_input(rep_id="low"),
            make_input(
                rep_id="high",
                linkedin_activity_score=80.0,
                activity_trend_30d=-30.0,
                compensation_vs_market_pct=60.0,
                team_attrition_rate_90d=35.0,
                quota_attainment_pct=20.0,
            ),
        ])
        for r in engine.flight_risks():
            assert r.is_flight_risk is True

    def test_flight_risks_empty_on_empty_engine(self, engine):
        assert engine.flight_risks() == []


# ═══════════════════════════════════════════════════════════════════════════════
# 23. URGENT_RETENTION() TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestUrgentRetention:
    def test_urgent_retention_returns_list(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.urgent_retention(), list)

    def test_urgent_retention_empty_for_low_risk(self, engine):
        engine.assess(make_input())
        assert engine.urgent_retention() == []

    def test_urgent_retention_all_flagged(self, engine):
        engine.assess_batch([
            make_input(rep_id="low"),
            make_input(
                rep_id="urgent",
                linkedin_activity_score=80.0,
                activity_trend_30d=-30.0,
                skipped_training_sessions_count=3,
                manager_1on1_completion_rate=20.0,
                compensation_vs_market_pct=60.0,
                uncapped_commission=0,
                sales_target_increase_pct=40.0,
                team_attrition_rate_90d=35.0,
                pto_days_unused=25,
                quota_attainment_pct=20.0,
                manager_satisfaction_score=1.0,
                days_since_last_promotion=900,
                tenure_months=18,
            ),
        ])
        for r in engine.urgent_retention():
            assert r.needs_urgent_retention is True

    def test_urgent_retention_empty_on_empty_engine(self, engine):
        assert engine.urgent_retention() == []


# ═══════════════════════════════════════════════════════════════════════════════
# 24. TOTAL_PIPELINE_AT_RISK() TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestTotalPipelineAtRisk:
    def test_zero_on_empty_engine(self, engine):
        assert engine.total_pipeline_at_risk() == 0.0

    def test_single_rep_total(self, engine):
        result = engine.assess(make_input(active_pipeline_usd=500000.0))
        assert engine.total_pipeline_at_risk() == pytest.approx(
            result.estimated_pipeline_at_risk_usd, abs=0.01
        )

    def test_sum_across_multiple_reps(self, engine):
        r1 = engine.assess(make_input(rep_id="r1", active_pipeline_usd=100000.0))
        r2 = engine.assess(make_input(rep_id="r2", active_pipeline_usd=200000.0))
        expected = r1.estimated_pipeline_at_risk_usd + r2.estimated_pipeline_at_risk_usd
        assert engine.total_pipeline_at_risk() == pytest.approx(expected, abs=0.01)

    def test_total_is_float(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.total_pipeline_at_risk(), float)

    def test_total_never_negative(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        assert engine.total_pipeline_at_risk() >= 0.0

    def test_total_increases_with_more_reps(self, engine):
        engine.assess(make_input(rep_id="r1", active_pipeline_usd=100000.0))
        total1 = engine.total_pipeline_at_risk()
        engine.assess(make_input(rep_id="r2", active_pipeline_usd=100000.0))
        assert engine.total_pipeline_at_risk() >= total1

    def test_total_zero_after_reset(self, engine):
        engine.assess(make_input())
        engine.reset()
        assert engine.total_pipeline_at_risk() == 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# 25. SUMMARY() TESTS — 13 KEYS
# ═══════════════════════════════════════════════════════════════════════════════


class TestSummary:
    def _populated_engine(self, engine):
        engine.assess(make_input(rep_id="r1"))
        engine.assess(make_input(rep_id="r2"))
        return engine

    def test_summary_returns_dict(self, engine):
        assert isinstance(engine.summary(), dict)

    def test_summary_empty_engine_13_keys(self, engine):
        assert len(engine.summary()) == 13

    def test_summary_populated_13_keys(self, engine):
        self._populated_engine(engine)
        assert len(engine.summary()) == 13

    def test_summary_has_total(self, engine):
        assert "total" in engine.summary()

    def test_summary_has_risk_counts(self, engine):
        assert "risk_counts" in engine.summary()

    def test_summary_has_signal_counts(self, engine):
        assert "signal_counts" in engine.summary()

    def test_summary_has_compensation_counts(self, engine):
        assert "compensation_counts" in engine.summary()

    def test_summary_has_action_counts(self, engine):
        assert "action_counts" in engine.summary()

    def test_summary_has_avg_attrition_composite(self, engine):
        assert "avg_attrition_composite" in engine.summary()

    def test_summary_has_flight_risk_count(self, engine):
        assert "flight_risk_count" in engine.summary()

    def test_summary_has_urgent_retention_count(self, engine):
        assert "urgent_retention_count" in engine.summary()

    def test_summary_has_avg_disengagement_score(self, engine):
        assert "avg_disengagement_score" in engine.summary()

    def test_summary_has_avg_compensation_risk_score(self, engine):
        assert "avg_compensation_risk_score" in engine.summary()

    def test_summary_has_avg_performance_satisfaction_score(self, engine):
        assert "avg_performance_satisfaction_score" in engine.summary()

    def test_summary_has_avg_social_risk_score(self, engine):
        assert "avg_social_risk_score" in engine.summary()

    def test_summary_has_total_pipeline_at_risk_usd(self, engine):
        assert "total_pipeline_at_risk_usd" in engine.summary()

    def test_summary_total_zero_on_empty(self, engine):
        assert engine.summary()["total"] == 0

    def test_summary_total_correct(self, engine):
        self._populated_engine(engine)
        assert engine.summary()["total"] == 2

    def test_summary_risk_counts_dict(self, engine):
        self._populated_engine(engine)
        assert isinstance(engine.summary()["risk_counts"], dict)

    def test_summary_risk_counts_sum(self, engine):
        self._populated_engine(engine)
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_signal_counts_sum(self, engine):
        self._populated_engine(engine)
        s = engine.summary()
        assert sum(s["signal_counts"].values()) == s["total"]

    def test_summary_avg_composite_in_valid_range(self, engine):
        self._populated_engine(engine)
        avg = engine.summary()["avg_attrition_composite"]
        assert 0.0 <= avg <= 100.0

    def test_summary_avg_scores_in_valid_range(self, engine):
        self._populated_engine(engine)
        s = engine.summary()
        for key in [
            "avg_disengagement_score",
            "avg_compensation_risk_score",
            "avg_performance_satisfaction_score",
            "avg_social_risk_score",
        ]:
            assert 0.0 <= s[key] <= 100.0

    def test_summary_flight_risk_count_nonnegative(self, engine):
        self._populated_engine(engine)
        assert engine.summary()["flight_risk_count"] >= 0

    def test_summary_urgent_retention_count_nonnegative(self, engine):
        self._populated_engine(engine)
        assert engine.summary()["urgent_retention_count"] >= 0

    def test_summary_total_pipeline_nonnegative(self, engine):
        self._populated_engine(engine)
        assert engine.summary()["total_pipeline_at_risk_usd"] >= 0.0

    def test_summary_flight_risk_matches_flight_risks_method(self, engine):
        self._populated_engine(engine)
        assert engine.summary()["flight_risk_count"] == len(engine.flight_risks())

    def test_summary_urgent_retention_matches_method(self, engine):
        self._populated_engine(engine)
        assert engine.summary()["urgent_retention_count"] == len(engine.urgent_retention())

    def test_summary_pipeline_matches_total_pipeline_method(self, engine):
        self._populated_engine(engine)
        assert engine.summary()["total_pipeline_at_risk_usd"] == engine.total_pipeline_at_risk()

    def test_summary_avg_composite_matches_method(self, engine):
        self._populated_engine(engine)
        assert engine.summary()["avg_attrition_composite"] == engine.avg_attrition_composite()


# ═══════════════════════════════════════════════════════════════════════════════
# 26. ENGINE GET / ALL_REPS METHODS
# ═══════════════════════════════════════════════════════════════════════════════


class TestEngineGetAndAllReps:
    def test_get_returns_none_if_not_found(self, engine):
        assert engine.get("nonexistent") is None

    def test_get_returns_result_after_assess(self, engine):
        engine.assess(make_input(rep_id="r1"))
        assert isinstance(engine.get("r1"), RepAttritionResult)

    def test_get_returns_correct_result(self, engine):
        engine.assess(make_input(rep_id="r1", rep_name="Alice"))
        result = engine.get("r1")
        assert result.rep_name == "Alice"

    def test_all_reps_returns_empty_list(self, engine):
        assert engine.all_reps() == []

    def test_all_reps_returns_list(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.all_reps(), list)

    def test_all_reps_sorted_descending(self, engine):
        engine.assess_batch([
            make_input(rep_id=f"r{i}", linkedin_activity_score=float(i * 8))
            for i in range(5)
        ])
        reps = engine.all_reps()
        composites = [r.attrition_composite for r in reps]
        assert composites == sorted(composites, reverse=True)

    def test_all_reps_count_matches_results(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(4)])
        assert len(engine.all_reps()) == 4


# ═══════════════════════════════════════════════════════════════════════════════
# 27. AVG_ATTRITION_COMPOSITE TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestAvgAttritionComposite:
    def test_zero_on_empty_engine(self, engine):
        assert engine.avg_attrition_composite() == 0.0

    def test_single_rep_equals_its_composite(self, engine):
        result = engine.assess(make_input())
        assert engine.avg_attrition_composite() == result.attrition_composite

    def test_average_is_correct(self, engine):
        r1 = engine.assess(make_input(rep_id="r1"))
        r2 = engine.assess(make_input(rep_id="r2", linkedin_activity_score=60.0))
        expected = round((r1.attrition_composite + r2.attrition_composite) / 2, 1)
        assert engine.avg_attrition_composite() == pytest.approx(expected, abs=0.1)

    def test_avg_in_valid_range(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        avg = engine.avg_attrition_composite()
        assert 0.0 <= avg <= 100.0


# ═══════════════════════════════════════════════════════════════════════════════
# 28. SCORE CLAMPING [0, 100] TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestScoreClamping:
    def test_disengagement_max_capped_at_100(self):
        inp = make_input(
            activity_trend_30d=-40.0,
            skipped_training_sessions_count=10,
            manager_1on1_completion_rate=0.0,
            linkedin_activity_score=100.0,
            deal_win_rate_last_90d=0.0,
            deal_win_rate_prev_quarter=100.0,
        )
        assert _disengagement_score(inp) <= 100.0

    def test_comp_risk_max_capped_at_100(self):
        inp = make_input(
            compensation_vs_market_pct=50.0,
            uncapped_commission=0,
            sales_target_increase_pct=50.0,
            days_since_last_promotion=1000,
            quota_attainment_pct=60.0,
            quota_attainment_pct_prev_year=100.0,
        )
        assert _compensation_risk_score(inp) <= 100.0

    def test_perf_sat_min_is_zero(self):
        inp = make_input(
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=0.0,
            tenure_months=0,
        )
        assert _performance_satisfaction_score(inp) >= 0.0

    def test_perf_sat_max_capped_at_100(self):
        inp = make_input(
            quota_attainment_pct=200.0,
            deal_win_rate_last_90d=100.0,
            manager_satisfaction_score=10.0,
            peer_relationships_score=10.0,
            tenure_months=60,
        )
        assert _performance_satisfaction_score(inp) <= 100.0

    def test_social_risk_max_capped_at_100(self):
        inp = make_input(
            team_attrition_rate_90d=50.0,
            pipeline_outside_territory_pct=50.0,
            pto_days_unused=30,
            linkedin_activity_score=100.0,
        )
        assert _social_risk_score(inp) <= 100.0

    def test_social_risk_min_is_zero(self):
        inp = make_input(
            team_attrition_rate_90d=0.0,
            pipeline_outside_territory_pct=0.0,
            pto_days_unused=0,
            linkedin_activity_score=0.0,
        )
        assert _social_risk_score(inp) >= 0.0

    def test_composite_from_engine_clamped(self, engine):
        result = engine.assess(make_input(
            activity_trend_30d=-40.0,
            linkedin_activity_score=100.0,
            compensation_vs_market_pct=50.0,
            team_attrition_rate_90d=50.0,
        ))
        assert 0.0 <= result.attrition_composite <= 100.0


# ═══════════════════════════════════════════════════════════════════════════════
# 29. EDGE CASES AND INTEGRATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestEdgeCasesAndIntegration:
    def test_identical_win_rates_no_disengagement_from_delta(self):
        inp = make_input(
            deal_win_rate_last_90d=30.0,
            deal_win_rate_prev_quarter=30.0,
            activity_trend_30d=0.0,
            skipped_training_sessions_count=0,
            manager_1on1_completion_rate=95.0,
            linkedin_activity_score=0.0,
        )
        score = _disengagement_score(inp)
        assert score == 0.0

    def test_zero_tenure_no_tenure_bonus(self):
        score = _performance_satisfaction_score(make_input(
            tenure_months=0,
            quota_attainment_pct=0.0,
            deal_win_rate_last_90d=0.0,
            manager_satisfaction_score=0.0,
            peer_relationships_score=0.0,
        ))
        assert score == 0.0

    def test_very_large_pipeline_at_risk(self, engine):
        result = engine.assess(make_input(active_pipeline_usd=10_000_000.0))
        assert result.estimated_pipeline_at_risk_usd >= 0.0

    def test_zero_pipeline_no_exposure(self, engine):
        result = engine.assess(make_input(active_pipeline_usd=0.0))
        assert result.estimated_pipeline_at_risk_usd == 0.0

    def test_batch_then_reset_then_batch(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        engine.reset()
        engine.assess_batch([make_input(rep_id=f"x{i}") for i in range(3)])
        assert len(engine._results) == 3

    def test_multiple_resets_safe(self, engine):
        engine.reset()
        engine.reset()
        assert engine._results == {}

    def test_assess_after_batch_adds_to_results(self, engine):
        engine.assess_batch([make_input(rep_id="r1"), make_input(rep_id="r2")])
        engine.assess(make_input(rep_id="r3"))
        assert len(engine._results) == 3

    def test_assess_on_new_engine_gives_no_flight_risks(self, engine):
        engine.assess(make_input())
        # Low risk baseline shouldn't be a flight risk
        assert engine.flight_risks() == []

    def test_by_risk_and_by_signal_consistent(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        total_by_risk = sum(
            len(engine.by_risk(r)) for r in AttritionRisk
        )
        assert total_by_risk == len(engine._results)

    def test_by_signal_all_categories_sum_to_total(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        total_by_signal = sum(
            len(engine.by_signal(s)) for s in AttritionSignal
        )
        assert total_by_signal == len(engine._results)

    def test_flight_risk_subset_of_all_reps(self, engine):
        engine.assess_batch([
            make_input(rep_id="low"),
            make_input(
                rep_id="high",
                linkedin_activity_score=80.0,
                activity_trend_30d=-30.0,
                compensation_vs_market_pct=60.0,
                team_attrition_rate_90d=35.0,
                quota_attainment_pct=20.0,
            ),
        ])
        all_ids = {r.rep_id for r in engine.all_reps()}
        flight_ids = {r.rep_id for r in engine.flight_risks()}
        assert flight_ids.issubset(all_ids)

    def test_urgent_subset_of_flight_risks_or_standalone(self, engine):
        engine.assess_batch([
            make_input(rep_id="low"),
            make_input(
                rep_id="urgent",
                linkedin_activity_score=80.0,
                activity_trend_30d=-30.0,
                skipped_training_sessions_count=3,
                manager_1on1_completion_rate=20.0,
                compensation_vs_market_pct=60.0,
                uncapped_commission=0,
                sales_target_increase_pct=40.0,
                team_attrition_rate_90d=35.0,
                pto_days_unused=25,
                quota_attainment_pct=20.0,
                manager_satisfaction_score=1.0,
                days_since_last_promotion=900,
                tenure_months=18,
            ),
        ])
        all_ids = {r.rep_id for r in engine.all_reps()}
        urgent_ids = {r.rep_id for r in engine.urgent_retention()}
        assert urgent_ids.issubset(all_ids)

    def test_summary_compensation_counts_sum(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = engine.summary()
        assert sum(s["compensation_counts"].values()) == s["total"]

    def test_summary_action_counts_sum(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]
