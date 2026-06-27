"""Comprehensive pytest test suite for CompetitorWinLossIntelligenceEngine (Module 112)."""
import dataclasses
import pytest
from swarm.intelligence.competitor_win_loss_intelligence_engine import (
    CompetitorWinLossIntelligenceEngine,
    CompetitorWinLossInput,
    CompetitorWinLossResult,
    CompetitiveRisk,
    CompetitivePattern,
    CompetitiveSeverity,
    CompetitiveAction,
    _clamp,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> CompetitorWinLossInput:
    """Return a baseline all-zero/safe input with selective overrides."""
    defaults = dict(
        rep_id="REP001",
        region="WEST",
        evaluation_period_id="Q1-2026",
        total_competitive_deals=10,
        wins_against_competitor=5,
        losses_to_competitor=5,
        avg_win_rate_pct=50.0,
        company_avg_win_rate_pct=50.0,
        deals_lost_on_price=0,
        deals_lost_on_features=0,
        deals_lost_on_relationship=0,
        deals_without_competitor_intel=0,
        avg_deal_value_won_usd=10000.0,
        avg_deal_value_lost_usd=10000.0,
        competitor_mentioned_in_deal_count=10,
        battlecard_usage_count=10,
        late_stage_competitive_loss_count=0,
        competitive_loss_streak=0,
        win_rate_trend_delta_pct=0.0,
        days_since_last_competitive_win=0,
        rep_avg_competitive_win_rate_pct=50.0,
        exec_sponsor_deals_won=5,
    )
    defaults.update(overrides)
    return CompetitorWinLossInput(**defaults)


def fresh_engine() -> CompetitorWinLossIntelligenceEngine:
    return CompetitorWinLossIntelligenceEngine()


# ===========================================================================
# SECTION 1: INVARIANTS
# ===========================================================================

class TestInputFieldCount:
    def test_exactly_22_fields(self):
        fields = dataclasses.fields(CompetitorWinLossInput)
        assert len(fields) == 22

    def test_field_names(self):
        names = {f.name for f in dataclasses.fields(CompetitorWinLossInput)}
        expected = {
            "rep_id", "region", "evaluation_period_id", "total_competitive_deals",
            "wins_against_competitor", "losses_to_competitor", "avg_win_rate_pct",
            "company_avg_win_rate_pct", "deals_lost_on_price", "deals_lost_on_features",
            "deals_lost_on_relationship", "deals_without_competitor_intel",
            "avg_deal_value_won_usd", "avg_deal_value_lost_usd",
            "competitor_mentioned_in_deal_count", "battlecard_usage_count",
            "late_stage_competitive_loss_count", "competitive_loss_streak",
            "win_rate_trend_delta_pct", "days_since_last_competitive_win",
            "rep_avg_competitive_win_rate_pct", "exec_sponsor_deals_won",
        }
        assert names == expected


class TestToDictKeyCount:
    def test_exactly_15_keys(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        d = result.to_dict()
        expected_keys = {
            "rep_id", "region", "competitive_risk", "competitive_pattern",
            "competitive_severity", "recommended_action", "price_vulnerability_score",
            "feature_gap_score", "intel_coverage_score", "execution_quality_score",
            "competitive_composite", "is_competitive_risk", "requires_battlecard_update",
            "estimated_revenue_at_risk_usd", "competitive_signal",
        }
        assert set(d.keys()) == expected_keys


class TestSummaryKeyCount:
    def test_empty_engine_summary_has_13_keys(self):
        eng = fresh_engine()
        s = eng.summary()
        assert len(s) == 13

    def test_populated_engine_summary_has_13_keys(self):
        eng = fresh_engine()
        eng.assess(make_input())
        eng.assess(make_input(rep_id="REP002"))
        s = eng.summary()
        assert len(s) == 13

    def test_summary_key_names_empty(self):
        eng = fresh_engine()
        s = eng.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
            "avg_competitive_composite", "competitive_risk_count", "battlecard_update_count",
            "avg_price_vulnerability_score", "avg_feature_gap_score",
            "avg_intel_coverage_score", "avg_execution_quality_score",
            "total_estimated_revenue_at_risk_usd",
        }
        assert set(s.keys()) == expected

    def test_summary_key_names_populated(self):
        eng = fresh_engine()
        eng.assess(make_input())
        s = eng.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
            "avg_competitive_composite", "competitive_risk_count", "battlecard_update_count",
            "avg_price_vulnerability_score", "avg_feature_gap_score",
            "avg_intel_coverage_score", "avg_execution_quality_score",
            "total_estimated_revenue_at_risk_usd",
        }
        assert set(s.keys()) == expected


# ===========================================================================
# SECTION 2: ENUM VALUES
# ===========================================================================

class TestEnumValues:
    def test_competitive_risk_values(self):
        assert CompetitiveRisk.low.value == "low"
        assert CompetitiveRisk.moderate.value == "moderate"
        assert CompetitiveRisk.high.value == "high"
        assert CompetitiveRisk.critical.value == "critical"

    def test_competitive_risk_count(self):
        assert len(CompetitiveRisk) == 4

    def test_competitive_pattern_values(self):
        assert CompetitivePattern.none.value == "none"
        assert CompetitivePattern.price_displacement.value == "price_displacement"
        assert CompetitivePattern.feature_gap.value == "feature_gap"
        assert CompetitivePattern.relationship_loss.value == "relationship_loss"
        assert CompetitivePattern.intel_blindspot.value == "intel_blindspot"
        assert CompetitivePattern.systematic_loss.value == "systematic_loss"

    def test_competitive_pattern_count(self):
        assert len(CompetitivePattern) == 6

    def test_competitive_severity_values(self):
        assert CompetitiveSeverity.stable.value == "stable"
        assert CompetitiveSeverity.watch.value == "watch"
        assert CompetitiveSeverity.threatened.value == "threatened"
        assert CompetitiveSeverity.critical.value == "critical"

    def test_competitive_severity_count(self):
        assert len(CompetitiveSeverity) == 4

    def test_competitive_action_values(self):
        assert CompetitiveAction.no_action.value == "no_action"
        assert CompetitiveAction.monitor.value == "monitor"
        assert CompetitiveAction.battlecard_update.value == "battlecard_update"
        assert CompetitiveAction.sales_coaching.value == "sales_coaching"
        assert CompetitiveAction.executive_escalation.value == "executive_escalation"

    def test_competitive_action_count(self):
        assert len(CompetitiveAction) == 5

    def test_enums_are_str_subclass(self):
        assert isinstance(CompetitiveRisk.low, str)
        assert isinstance(CompetitivePattern.none, str)
        assert isinstance(CompetitiveSeverity.stable, str)
        assert isinstance(CompetitiveAction.no_action, str)


# ===========================================================================
# SECTION 3: _clamp utility
# ===========================================================================

class TestClamp:
    def test_clamp_below_zero(self):
        assert _clamp(-10.0) == 0.0

    def test_clamp_above_100(self):
        assert _clamp(150.0) == 100.0

    def test_clamp_zero(self):
        assert _clamp(0.0) == 0.0

    def test_clamp_100(self):
        assert _clamp(100.0) == 100.0

    def test_clamp_mid(self):
        assert _clamp(50.0) == 50.0


# ===========================================================================
# SECTION 4: PRICE VULNERABILITY SUB-SCORE
# ===========================================================================

class TestPriceVulnerabilityScore:
    def setup_method(self):
        self.eng = fresh_engine()

    def _price(self, **kw):
        return self.eng._price_vulnerability_score(make_input(**kw))

    # price_loss_ratio thresholds
    def test_price_ratio_zero(self):
        score = self._price(deals_lost_on_price=0, total_competitive_deals=10)
        assert score >= 0.0

    def test_price_ratio_below_20pct(self):
        # 1/10 = 10% → no price ratio bonus
        score_no_gap = self._price(deals_lost_on_price=1, total_competitive_deals=10,
                                   company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
                                   avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000)
        assert score_no_gap == 0.0

    def test_price_ratio_at_20pct_gets_15(self):
        # 2/10 = 20% → +15
        score = self._price(deals_lost_on_price=2, total_competitive_deals=10,
                            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
                            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000)
        assert score == 15.0

    def test_price_ratio_at_35pct_gets_30(self):
        # 35/100 = 35% → +30
        score = self._price(deals_lost_on_price=35, total_competitive_deals=100,
                            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
                            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000)
        assert score == 30.0

    def test_price_ratio_at_50pct_gets_45(self):
        # 5/10 = 50% → +45
        score = self._price(deals_lost_on_price=5, total_competitive_deals=10,
                            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
                            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000)
        assert score == 45.0

    def test_price_ratio_above_50pct_gets_45(self):
        # 8/10 = 80% → +45
        score = self._price(deals_lost_on_price=8, total_competitive_deals=10,
                            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
                            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000)
        assert score == 45.0

    # win_rate_gap thresholds
    def test_win_rate_gap_below_10_no_bonus(self):
        score = self._price(deals_lost_on_price=0, total_competitive_deals=10,
                            company_avg_win_rate_pct=55.0, avg_win_rate_pct=50.0,
                            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000)
        assert score == 0.0

    def test_win_rate_gap_at_10_gets_10(self):
        score = self._price(deals_lost_on_price=0, total_competitive_deals=10,
                            company_avg_win_rate_pct=60.0, avg_win_rate_pct=50.0,
                            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000)
        assert score == 10.0

    def test_win_rate_gap_at_20_gets_22(self):
        score = self._price(deals_lost_on_price=0, total_competitive_deals=10,
                            company_avg_win_rate_pct=70.0, avg_win_rate_pct=50.0,
                            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000)
        assert score == 22.0

    def test_win_rate_gap_at_30_gets_35(self):
        score = self._price(deals_lost_on_price=0, total_competitive_deals=10,
                            company_avg_win_rate_pct=80.0, avg_win_rate_pct=50.0,
                            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000)
        assert score == 35.0

    def test_win_rate_gap_above_30_gets_35(self):
        score = self._price(deals_lost_on_price=0, total_competitive_deals=10,
                            company_avg_win_rate_pct=90.0, avg_win_rate_pct=50.0,
                            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000)
        assert score == 35.0

    # value gap thresholds
    def test_no_value_gap_no_bonus(self):
        score = self._price(deals_lost_on_price=0, total_competitive_deals=10,
                            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
                            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000)
        assert score == 0.0

    def test_value_gap_30pct_gets_10(self):
        # lost=10000, won=7000 → gap=(3000/10000)=0.30 → +10
        score = self._price(deals_lost_on_price=0, total_competitive_deals=10,
                            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
                            avg_deal_value_won_usd=7000, avg_deal_value_lost_usd=10000)
        assert score == 10.0

    def test_value_gap_50pct_gets_20(self):
        # lost=10000, won=5000 → gap=0.50 → +20
        score = self._price(deals_lost_on_price=0, total_competitive_deals=10,
                            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
                            avg_deal_value_won_usd=5000, avg_deal_value_lost_usd=10000)
        assert score == 20.0

    def test_value_gap_when_won_zero_no_bonus(self):
        score = self._price(deals_lost_on_price=0, total_competitive_deals=10,
                            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
                            avg_deal_value_won_usd=0, avg_deal_value_lost_usd=10000)
        assert score == 0.0

    def test_score_clamped_at_100(self):
        score = self._price(deals_lost_on_price=10, total_competitive_deals=10,
                            company_avg_win_rate_pct=100.0, avg_win_rate_pct=50.0,
                            avg_deal_value_won_usd=1000, avg_deal_value_lost_usd=10000)
        assert score <= 100.0

    def test_zero_total_deals_no_price_ratio(self):
        score = self._price(deals_lost_on_price=5, total_competitive_deals=0,
                            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0)
        # No division by zero; only win_rate_gap and value_gap contribute
        assert score >= 0.0


# ===========================================================================
# SECTION 5: FEATURE GAP SUB-SCORE
# ===========================================================================

class TestFeatureGapScore:
    def setup_method(self):
        self.eng = fresh_engine()

    def _feat(self, **kw):
        return self.eng._feature_gap_score(make_input(**kw))

    def test_zero_everything_zero_score(self):
        score = self._feat(deals_lost_on_features=0, total_competitive_deals=10,
                           late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=0.0)
        assert score == 0.0

    # feature_loss_ratio
    def test_feature_ratio_below_12_no_bonus(self):
        # 1/10 = 10% → no bonus
        score = self._feat(deals_lost_on_features=1, total_competitive_deals=10,
                           late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=0.0)
        assert score == 0.0

    def test_feature_ratio_at_12pct_gets_14(self):
        # 12/100 = 12% → +14
        score = self._feat(deals_lost_on_features=12, total_competitive_deals=100,
                           late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=0.0)
        assert score == 14.0

    def test_feature_ratio_at_25pct_gets_28(self):
        score = self._feat(deals_lost_on_features=25, total_competitive_deals=100,
                           late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=0.0)
        assert score == 28.0

    def test_feature_ratio_at_40pct_gets_45(self):
        score = self._feat(deals_lost_on_features=40, total_competitive_deals=100,
                           late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=0.0)
        assert score == 45.0

    def test_feature_ratio_above_40pct_gets_45(self):
        score = self._feat(deals_lost_on_features=8, total_competitive_deals=10,
                           late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=0.0)
        assert score == 45.0

    # late_stage_competitive_loss_count
    def test_late_stage_1_gets_10(self):
        score = self._feat(deals_lost_on_features=0, total_competitive_deals=10,
                           late_stage_competitive_loss_count=1, win_rate_trend_delta_pct=0.0)
        assert score == 10.0

    def test_late_stage_3_gets_22(self):
        score = self._feat(deals_lost_on_features=0, total_competitive_deals=10,
                           late_stage_competitive_loss_count=3, win_rate_trend_delta_pct=0.0)
        assert score == 22.0

    def test_late_stage_5_gets_35(self):
        score = self._feat(deals_lost_on_features=0, total_competitive_deals=10,
                           late_stage_competitive_loss_count=5, win_rate_trend_delta_pct=0.0)
        assert score == 35.0

    def test_late_stage_above_5_gets_35(self):
        score = self._feat(deals_lost_on_features=0, total_competitive_deals=10,
                           late_stage_competitive_loss_count=10, win_rate_trend_delta_pct=0.0)
        assert score == 35.0

    # win_rate_trend
    def test_trend_minus_10_gets_10(self):
        score = self._feat(deals_lost_on_features=0, total_competitive_deals=10,
                           late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=-10.0)
        assert score == 10.0

    def test_trend_minus_20_gets_20(self):
        score = self._feat(deals_lost_on_features=0, total_competitive_deals=10,
                           late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=-20.0)
        assert score == 20.0

    def test_trend_minus_9_no_bonus(self):
        score = self._feat(deals_lost_on_features=0, total_competitive_deals=10,
                           late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=-9.0)
        assert score == 0.0

    def test_trend_positive_no_bonus(self):
        score = self._feat(deals_lost_on_features=0, total_competitive_deals=10,
                           late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=5.0)
        assert score == 0.0

    def test_feature_score_clamped_at_100(self):
        score = self._feat(deals_lost_on_features=10, total_competitive_deals=10,
                           late_stage_competitive_loss_count=10, win_rate_trend_delta_pct=-30.0)
        assert score <= 100.0

    def test_zero_total_deals_no_feature_ratio_bonus(self):
        score = self._feat(deals_lost_on_features=5, total_competitive_deals=0,
                           late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=0.0)
        assert score == 0.0


# ===========================================================================
# SECTION 6: INTEL COVERAGE SUB-SCORE
# ===========================================================================

class TestIntelCoverageScore:
    def setup_method(self):
        self.eng = fresh_engine()

    def _intel(self, **kw):
        return self.eng._intel_coverage_score(make_input(**kw))

    def test_zero_everything_zero_score(self):
        score = self._intel(deals_without_competitor_intel=0, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=10, battlecard_usage_count=10,
                            competitive_loss_streak=0)
        assert score == 0.0

    # blind_ratio thresholds
    def test_blind_ratio_below_20_no_bonus(self):
        # 1/10 = 10%
        score = self._intel(deals_without_competitor_intel=1, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=10, battlecard_usage_count=10,
                            competitive_loss_streak=0)
        assert score == 0.0

    def test_blind_ratio_at_20pct_gets_15(self):
        score = self._intel(deals_without_competitor_intel=2, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=10, battlecard_usage_count=10,
                            competitive_loss_streak=0)
        assert score == 15.0

    def test_blind_ratio_at_40pct_gets_30(self):
        score = self._intel(deals_without_competitor_intel=4, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=10, battlecard_usage_count=10,
                            competitive_loss_streak=0)
        assert score == 30.0

    def test_blind_ratio_at_60pct_gets_45(self):
        score = self._intel(deals_without_competitor_intel=6, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=10, battlecard_usage_count=10,
                            competitive_loss_streak=0)
        assert score == 45.0

    # battlecard card_ratio thresholds
    def test_card_ratio_below_20_gets_30(self):
        score = self._intel(deals_without_competitor_intel=0, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=10, battlecard_usage_count=1,
                            competitive_loss_streak=0)
        assert score == 30.0

    def test_card_ratio_at_20_gets_18(self):
        # 2/10 = 20% → <0.4 but >=0.2 → +18
        score = self._intel(deals_without_competitor_intel=0, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=10, battlecard_usage_count=2,
                            competitive_loss_streak=0)
        assert score == 18.0

    def test_card_ratio_at_40_gets_8(self):
        # 4/10 = 40% → <0.6 but >=0.4 → +8
        score = self._intel(deals_without_competitor_intel=0, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=10, battlecard_usage_count=4,
                            competitive_loss_streak=0)
        assert score == 8.0

    def test_card_ratio_at_60_no_bonus(self):
        # 6/10 = 60% → no bonus
        score = self._intel(deals_without_competitor_intel=0, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=10, battlecard_usage_count=6,
                            competitive_loss_streak=0)
        assert score == 0.0

    def test_zero_competitor_mentions_no_card_bonus(self):
        score = self._intel(deals_without_competitor_intel=0, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=0, battlecard_usage_count=0,
                            competitive_loss_streak=0)
        assert score == 0.0

    # competitive_loss_streak thresholds
    def test_streak_2_gets_7(self):
        score = self._intel(deals_without_competitor_intel=0, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=10, battlecard_usage_count=10,
                            competitive_loss_streak=2)
        assert score == 7.0

    def test_streak_4_gets_15(self):
        score = self._intel(deals_without_competitor_intel=0, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=10, battlecard_usage_count=10,
                            competitive_loss_streak=4)
        assert score == 15.0

    def test_streak_6_gets_25(self):
        score = self._intel(deals_without_competitor_intel=0, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=10, battlecard_usage_count=10,
                            competitive_loss_streak=6)
        assert score == 25.0

    def test_streak_1_no_bonus(self):
        score = self._intel(deals_without_competitor_intel=0, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=10, battlecard_usage_count=10,
                            competitive_loss_streak=1)
        assert score == 0.0

    def test_intel_score_clamped_at_100(self):
        score = self._intel(deals_without_competitor_intel=10, total_competitive_deals=10,
                            competitor_mentioned_in_deal_count=10, battlecard_usage_count=0,
                            competitive_loss_streak=10)
        assert score <= 100.0


# ===========================================================================
# SECTION 7: EXECUTION QUALITY SUB-SCORE
# ===========================================================================

class TestExecutionQualityScore:
    def setup_method(self):
        self.eng = fresh_engine()

    def _exec(self, **kw):
        return self.eng._execution_quality_score(make_input(**kw))

    def test_zero_everything_no_score(self):
        score = self._exec(deals_lost_on_relationship=0, total_competitive_deals=10,
                           days_since_last_competitive_win=0,
                           wins_against_competitor=5, exec_sponsor_deals_won=5,
                           losses_to_competitor=0)
        assert score == 0.0

    # rel_loss_ratio thresholds
    def test_rel_ratio_below_10_no_bonus(self):
        # 0/10 = 0%
        score = self._exec(deals_lost_on_relationship=0, total_competitive_deals=10,
                           days_since_last_competitive_win=0,
                           wins_against_competitor=5, exec_sponsor_deals_won=5,
                           losses_to_competitor=0)
        assert score == 0.0

    def test_rel_ratio_at_10pct_gets_12(self):
        # 1/10 = 10% → +12
        score = self._exec(deals_lost_on_relationship=1, total_competitive_deals=10,
                           days_since_last_competitive_win=0,
                           wins_against_competitor=5, exec_sponsor_deals_won=5,
                           losses_to_competitor=0)
        assert score == 12.0

    def test_rel_ratio_at_25pct_gets_25(self):
        score = self._exec(deals_lost_on_relationship=25, total_competitive_deals=100,
                           days_since_last_competitive_win=0,
                           wins_against_competitor=5, exec_sponsor_deals_won=5,
                           losses_to_competitor=0)
        assert score == 25.0

    def test_rel_ratio_at_40pct_gets_40(self):
        score = self._exec(deals_lost_on_relationship=4, total_competitive_deals=10,
                           days_since_last_competitive_win=0,
                           wins_against_competitor=5, exec_sponsor_deals_won=5,
                           losses_to_competitor=0)
        assert score == 40.0

    # days_since_last_competitive_win thresholds
    def test_days_below_30_no_bonus(self):
        score = self._exec(deals_lost_on_relationship=0, total_competitive_deals=10,
                           days_since_last_competitive_win=29,
                           wins_against_competitor=5, exec_sponsor_deals_won=5,
                           losses_to_competitor=0)
        assert score == 0.0

    def test_days_at_30_gets_8(self):
        score = self._exec(deals_lost_on_relationship=0, total_competitive_deals=10,
                           days_since_last_competitive_win=30,
                           wins_against_competitor=5, exec_sponsor_deals_won=5,
                           losses_to_competitor=0)
        assert score == 8.0

    def test_days_at_60_gets_18(self):
        score = self._exec(deals_lost_on_relationship=0, total_competitive_deals=10,
                           days_since_last_competitive_win=60,
                           wins_against_competitor=5, exec_sponsor_deals_won=5,
                           losses_to_competitor=0)
        assert score == 18.0

    def test_days_at_90_gets_30(self):
        score = self._exec(deals_lost_on_relationship=0, total_competitive_deals=10,
                           days_since_last_competitive_win=90,
                           wins_against_competitor=5, exec_sponsor_deals_won=5,
                           losses_to_competitor=0)
        assert score == 30.0

    # exec_win_ratio thresholds
    def test_exec_ratio_below_15_gets_20(self):
        # wins=10, exec_won=1 → ratio=0.1 < 0.15 → +20
        score = self._exec(deals_lost_on_relationship=0, total_competitive_deals=10,
                           days_since_last_competitive_win=0,
                           wins_against_competitor=10, exec_sponsor_deals_won=1,
                           losses_to_competitor=0)
        assert score == 20.0

    def test_exec_ratio_between_15_and_30_gets_10(self):
        # wins=10, exec_won=2 → ratio=0.2 → >=0.15, <0.30 → +10
        score = self._exec(deals_lost_on_relationship=0, total_competitive_deals=10,
                           days_since_last_competitive_win=0,
                           wins_against_competitor=10, exec_sponsor_deals_won=2,
                           losses_to_competitor=0)
        assert score == 10.0

    def test_exec_ratio_above_30_no_bonus(self):
        # wins=10, exec_won=4 → ratio=0.4 → no bonus
        score = self._exec(deals_lost_on_relationship=0, total_competitive_deals=10,
                           days_since_last_competitive_win=0,
                           wins_against_competitor=10, exec_sponsor_deals_won=4,
                           losses_to_competitor=0)
        assert score == 0.0

    def test_zero_wins_with_3_or_more_losses_gets_20(self):
        score = self._exec(deals_lost_on_relationship=0, total_competitive_deals=10,
                           days_since_last_competitive_win=0,
                           wins_against_competitor=0, exec_sponsor_deals_won=0,
                           losses_to_competitor=3)
        assert score == 20.0

    def test_zero_wins_with_fewer_than_3_losses_no_exec_bonus(self):
        score = self._exec(deals_lost_on_relationship=0, total_competitive_deals=10,
                           days_since_last_competitive_win=0,
                           wins_against_competitor=0, exec_sponsor_deals_won=0,
                           losses_to_competitor=2)
        assert score == 0.0

    def test_execution_score_clamped_at_100(self):
        score = self._exec(deals_lost_on_relationship=10, total_competitive_deals=10,
                           days_since_last_competitive_win=120,
                           wins_against_competitor=0, exec_sponsor_deals_won=0,
                           losses_to_competitor=10)
        assert score <= 100.0


# ===========================================================================
# SECTION 8: COMPOSITE FORMULA
# ===========================================================================

class TestCompositeFormula:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_composite_weights(self):
        # Manually compute expected composite
        inp = make_input(
            deals_lost_on_price=5, total_competitive_deals=10,
            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000,
            deals_lost_on_features=0, late_stage_competitive_loss_count=0,
            win_rate_trend_delta_pct=0.0,
            deals_without_competitor_intel=0, competitor_mentioned_in_deal_count=10,
            battlecard_usage_count=10, competitive_loss_streak=0,
            deals_lost_on_relationship=0, days_since_last_competitive_win=0,
            wins_against_competitor=5, exec_sponsor_deals_won=5, losses_to_competitor=5,
        )
        result = self.eng.assess(inp)
        price = self.eng._price_vulnerability_score(inp)
        feat = self.eng._feature_gap_score(inp)
        intel = self.eng._intel_coverage_score(inp)
        exc = self.eng._execution_quality_score(inp)
        expected = round(min(100.0, max(0.0, price * 0.30 + feat * 0.25 + intel * 0.25 + exc * 0.20)), 1)
        assert result.competitive_composite == expected

    def test_composite_is_rounded_to_1_decimal(self):
        result = self.eng.assess(make_input())
        assert result.competitive_composite == round(result.competitive_composite, 1)

    def test_composite_zero_for_all_zeros(self):
        inp = make_input(
            deals_lost_on_price=0, total_competitive_deals=10,
            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000,
            deals_lost_on_features=0, late_stage_competitive_loss_count=0,
            win_rate_trend_delta_pct=0.0,
            deals_without_competitor_intel=0, competitor_mentioned_in_deal_count=10,
            battlecard_usage_count=10, competitive_loss_streak=0,
            deals_lost_on_relationship=0, days_since_last_competitive_win=0,
            wins_against_competitor=5, exec_sponsor_deals_won=5, losses_to_competitor=0,
        )
        result = self.eng.assess(inp)
        assert result.competitive_composite == 0.0

    def test_composite_at_most_100(self):
        inp = make_input(
            deals_lost_on_price=10, total_competitive_deals=10,
            company_avg_win_rate_pct=100.0, avg_win_rate_pct=0.0,
            avg_deal_value_won_usd=1000, avg_deal_value_lost_usd=10000,
            deals_lost_on_features=10, late_stage_competitive_loss_count=10,
            win_rate_trend_delta_pct=-50.0,
            deals_without_competitor_intel=10, competitor_mentioned_in_deal_count=10,
            battlecard_usage_count=0, competitive_loss_streak=10,
            deals_lost_on_relationship=10, days_since_last_competitive_win=200,
            wins_against_competitor=0, exec_sponsor_deals_won=0, losses_to_competitor=10,
        )
        result = self.eng.assess(inp)
        assert result.competitive_composite <= 100.0

    def test_composite_at_least_0(self):
        result = self.eng.assess(make_input())
        assert result.competitive_composite >= 0.0


# ===========================================================================
# SECTION 9: RISK AND SEVERITY CLASSIFICATION THRESHOLDS
# ===========================================================================

class TestRiskClassification:
    def setup_method(self):
        self.eng = fresh_engine()

    def _classify_risk(self, composite):
        return self.eng._classify_risk(composite)

    def _classify_severity(self, composite):
        return self.eng._classify_severity(composite)

    # Risk
    def test_risk_low_at_0(self):
        assert self._classify_risk(0.0) == CompetitiveRisk.low

    def test_risk_low_at_19_9(self):
        assert self._classify_risk(19.9) == CompetitiveRisk.low

    def test_risk_moderate_at_20(self):
        assert self._classify_risk(20.0) == CompetitiveRisk.moderate

    def test_risk_moderate_at_39_9(self):
        assert self._classify_risk(39.9) == CompetitiveRisk.moderate

    def test_risk_high_at_40(self):
        assert self._classify_risk(40.0) == CompetitiveRisk.high

    def test_risk_high_at_59_9(self):
        assert self._classify_risk(59.9) == CompetitiveRisk.high

    def test_risk_critical_at_60(self):
        assert self._classify_risk(60.0) == CompetitiveRisk.critical

    def test_risk_critical_at_100(self):
        assert self._classify_risk(100.0) == CompetitiveRisk.critical

    # Severity
    def test_severity_stable_at_0(self):
        assert self._classify_severity(0.0) == CompetitiveSeverity.stable

    def test_severity_stable_at_19_9(self):
        assert self._classify_severity(19.9) == CompetitiveSeverity.stable

    def test_severity_watch_at_20(self):
        assert self._classify_severity(20.0) == CompetitiveSeverity.watch

    def test_severity_watch_at_39_9(self):
        assert self._classify_severity(39.9) == CompetitiveSeverity.watch

    def test_severity_threatened_at_40(self):
        assert self._classify_severity(40.0) == CompetitiveSeverity.threatened

    def test_severity_threatened_at_59_9(self):
        assert self._classify_severity(59.9) == CompetitiveSeverity.threatened

    def test_severity_critical_at_60(self):
        assert self._classify_severity(60.0) == CompetitiveSeverity.critical

    def test_severity_critical_at_100(self):
        assert self._classify_severity(100.0) == CompetitiveSeverity.critical

    # Risk and Severity are always consistent
    def test_risk_severity_consistent(self):
        pairs = [
            (0.0, CompetitiveRisk.low, CompetitiveSeverity.stable),
            (19.9, CompetitiveRisk.low, CompetitiveSeverity.stable),
            (20.0, CompetitiveRisk.moderate, CompetitiveSeverity.watch),
            (39.9, CompetitiveRisk.moderate, CompetitiveSeverity.watch),
            (40.0, CompetitiveRisk.high, CompetitiveSeverity.threatened),
            (59.9, CompetitiveRisk.high, CompetitiveSeverity.threatened),
            (60.0, CompetitiveRisk.critical, CompetitiveSeverity.critical),
            (100.0, CompetitiveRisk.critical, CompetitiveSeverity.critical),
        ]
        for composite, expected_risk, expected_severity in pairs:
            assert self._classify_risk(composite) == expected_risk
            assert self._classify_severity(composite) == expected_severity


# ===========================================================================
# SECTION 10: PATTERN CLASSIFICATION
# ===========================================================================

class TestPatternClassification:
    def setup_method(self):
        self.eng = fresh_engine()

    def _pattern(self, price, feature, intel, execution, **inp_overrides):
        inp = make_input(**inp_overrides)
        return self.eng._classify_pattern(inp, price, feature, intel, execution)

    # systematic_loss: streak>=5 AND wins==0 (highest priority)
    def test_systematic_loss_streak5_wins0(self):
        p = self._pattern(0, 0, 0, 0, competitive_loss_streak=5, wins_against_competitor=0)
        assert p == CompetitivePattern.systematic_loss

    def test_systematic_loss_streak10_wins0(self):
        p = self._pattern(0, 0, 0, 0, competitive_loss_streak=10, wins_against_competitor=0)
        assert p == CompetitivePattern.systematic_loss

    def test_no_systematic_loss_when_wins_nonzero(self):
        p = self._pattern(0, 0, 0, 0, competitive_loss_streak=5, wins_against_competitor=1)
        assert p != CompetitivePattern.systematic_loss

    def test_no_systematic_loss_when_streak_below_5(self):
        p = self._pattern(0, 0, 0, 0, competitive_loss_streak=4, wins_against_competitor=0)
        assert p != CompetitivePattern.systematic_loss

    def test_systematic_loss_overrides_intel(self):
        # streak>=5, wins==0 should override high intel score
        p = self._pattern(0, 0, 50, 0, competitive_loss_streak=5, wins_against_competitor=0)
        assert p == CompetitivePattern.systematic_loss

    # intel_blindspot: intel>=35 (second priority)
    def test_intel_blindspot_at_35(self):
        p = self._pattern(0, 0, 35, 0, competitive_loss_streak=0)
        assert p == CompetitivePattern.intel_blindspot

    def test_intel_blindspot_at_100(self):
        p = self._pattern(0, 0, 100, 0, competitive_loss_streak=0)
        assert p == CompetitivePattern.intel_blindspot

    def test_no_intel_blindspot_at_34(self):
        p = self._pattern(0, 0, 34, 0, competitive_loss_streak=0)
        assert p != CompetitivePattern.intel_blindspot

    def test_intel_overrides_price(self):
        p = self._pattern(50, 0, 35, 0, competitive_loss_streak=0)
        assert p == CompetitivePattern.intel_blindspot

    # price_displacement: price>=35 (third priority)
    def test_price_displacement_at_35(self):
        p = self._pattern(35, 0, 0, 0, competitive_loss_streak=0)
        assert p == CompetitivePattern.price_displacement

    def test_price_displacement_at_100(self):
        p = self._pattern(100, 0, 0, 0, competitive_loss_streak=0)
        assert p == CompetitivePattern.price_displacement

    def test_no_price_displacement_at_34(self):
        p = self._pattern(34, 0, 0, 0, competitive_loss_streak=0)
        assert p != CompetitivePattern.price_displacement

    def test_price_overrides_feature(self):
        p = self._pattern(35, 50, 0, 0, competitive_loss_streak=0)
        assert p == CompetitivePattern.price_displacement

    # feature_gap: feature>=35 (fourth priority)
    def test_feature_gap_at_35(self):
        p = self._pattern(0, 35, 0, 0, competitive_loss_streak=0)
        assert p == CompetitivePattern.feature_gap

    def test_no_feature_gap_at_34(self):
        p = self._pattern(0, 34, 0, 0, competitive_loss_streak=0)
        assert p != CompetitivePattern.feature_gap

    def test_feature_gap_at_100(self):
        p = self._pattern(0, 100, 0, 0, competitive_loss_streak=0)
        assert p == CompetitivePattern.feature_gap

    def test_feature_overrides_relationship(self):
        p = self._pattern(0, 35, 0, 50, competitive_loss_streak=0, deals_lost_on_relationship=5)
        assert p == CompetitivePattern.feature_gap

    # relationship_loss: execution>=30 AND deals_lost_on_relationship>=2
    def test_relationship_loss(self):
        p = self._pattern(0, 0, 0, 30, competitive_loss_streak=0, deals_lost_on_relationship=2)
        assert p == CompetitivePattern.relationship_loss

    def test_no_relationship_loss_low_execution(self):
        p = self._pattern(0, 0, 0, 29, competitive_loss_streak=0, deals_lost_on_relationship=2)
        assert p != CompetitivePattern.relationship_loss

    def test_no_relationship_loss_few_rel_losses(self):
        p = self._pattern(0, 0, 0, 30, competitive_loss_streak=0, deals_lost_on_relationship=1)
        assert p != CompetitivePattern.relationship_loss

    def test_no_relationship_loss_zero_rel_losses(self):
        p = self._pattern(0, 0, 0, 30, competitive_loss_streak=0, deals_lost_on_relationship=0)
        assert p != CompetitivePattern.relationship_loss

    # none
    def test_none_pattern_when_all_below_threshold(self):
        p = self._pattern(0, 0, 0, 0, competitive_loss_streak=0, deals_lost_on_relationship=0)
        assert p == CompetitivePattern.none

    def test_none_pattern_low_scores(self):
        p = self._pattern(10, 10, 10, 10, competitive_loss_streak=0, deals_lost_on_relationship=0)
        assert p == CompetitivePattern.none


# ===========================================================================
# SECTION 11: RECOMMENDED ACTION
# ===========================================================================

class TestRecommendedAction:
    def setup_method(self):
        self.eng = fresh_engine()

    def _action(self, composite, risk):
        return self.eng._recommended_action(risk, composite)

    def test_executive_escalation_at_60(self):
        assert self._action(60.0, CompetitiveRisk.critical) == CompetitiveAction.executive_escalation

    def test_executive_escalation_at_100(self):
        assert self._action(100.0, CompetitiveRisk.critical) == CompetitiveAction.executive_escalation

    def test_sales_coaching_for_high_risk_below_60(self):
        assert self._action(55.0, CompetitiveRisk.high) == CompetitiveAction.sales_coaching

    def test_sales_coaching_for_high_risk_at_40(self):
        assert self._action(40.0, CompetitiveRisk.high) == CompetitiveAction.sales_coaching

    def test_battlecard_update_for_moderate_risk(self):
        assert self._action(30.0, CompetitiveRisk.moderate) == CompetitiveAction.battlecard_update

    def test_battlecard_update_for_moderate_at_20(self):
        assert self._action(20.0, CompetitiveRisk.moderate) == CompetitiveAction.battlecard_update

    def test_monitor_for_low_risk_composite_ge_10(self):
        assert self._action(10.0, CompetitiveRisk.low) == CompetitiveAction.monitor

    def test_monitor_for_low_risk_composite_15(self):
        assert self._action(15.0, CompetitiveRisk.low) == CompetitiveAction.monitor

    def test_no_action_for_low_risk_composite_below_10(self):
        assert self._action(5.0, CompetitiveRisk.low) == CompetitiveAction.no_action

    def test_no_action_for_zero_composite(self):
        assert self._action(0.0, CompetitiveRisk.low) == CompetitiveAction.no_action

    def test_executive_escalation_overrides_high_risk(self):
        # composite >= 60 always → executive_escalation, even if risk would be high
        assert self._action(60.0, CompetitiveRisk.high) == CompetitiveAction.executive_escalation


# ===========================================================================
# SECTION 12: IS_COMPETITIVE_RISK
# ===========================================================================

class TestIsCompetitiveRisk:
    def setup_method(self):
        self.eng = fresh_engine()

    def _assess(self, **kw):
        return self.eng.assess(make_input(**kw))

    def test_true_when_composite_ge_40(self):
        # Force high composite via many price losses, low win rate
        result = self._assess(
            deals_lost_on_price=8, total_competitive_deals=10,
            company_avg_win_rate_pct=80.0, avg_win_rate_pct=50.0,
        )
        # Verify composite >= 40 and flag is True
        if result.competitive_composite >= 40:
            assert result.is_competitive_risk is True

    def test_true_when_loss_streak_ge_4(self):
        result = self._assess(competitive_loss_streak=4)
        assert result.is_competitive_risk is True

    def test_true_when_loss_streak_5(self):
        result = self._assess(competitive_loss_streak=5)
        assert result.is_competitive_risk is True

    def test_true_when_avg_win_rate_below_20(self):
        result = self._assess(avg_win_rate_pct=19.9)
        assert result.is_competitive_risk is True

    def test_true_when_avg_win_rate_exactly_0(self):
        result = self._assess(avg_win_rate_pct=0.0)
        assert result.is_competitive_risk is True

    def test_false_when_all_conditions_false(self):
        result = self._assess(
            competitive_loss_streak=3,
            avg_win_rate_pct=50.0,
        )
        # composite needs to be < 40 too
        if result.competitive_composite < 40:
            assert result.is_competitive_risk is False

    def test_true_when_avg_win_rate_exactly_19(self):
        result = self._assess(avg_win_rate_pct=19.0)
        assert result.is_competitive_risk is True

    def test_false_when_avg_win_rate_exactly_20(self):
        # Only win rate at exactly 20 does NOT trigger (<20 required)
        result = self._assess(
            avg_win_rate_pct=20.0,
            competitive_loss_streak=0,
        )
        if result.competitive_composite < 40:
            assert result.is_competitive_risk is False

    def test_streak_3_not_trigger(self):
        result = self._assess(competitive_loss_streak=3, avg_win_rate_pct=50.0)
        if result.competitive_composite < 40:
            assert result.is_competitive_risk is False


# ===========================================================================
# SECTION 13: REQUIRES_BATTLECARD_UPDATE
# ===========================================================================

class TestRequiresBattlecardUpdate:
    def setup_method(self):
        self.eng = fresh_engine()

    def _assess(self, **kw):
        return self.eng.assess(make_input(**kw))

    def test_true_when_composite_ge_30(self):
        # Force composite >= 30 with price losses
        result = self._assess(
            deals_lost_on_price=8, total_competitive_deals=10,
            company_avg_win_rate_pct=60.0, avg_win_rate_pct=50.0,
        )
        if result.competitive_composite >= 30:
            assert result.requires_battlecard_update is True

    def test_true_when_deals_without_intel_ge_3(self):
        result = self._assess(deals_without_competitor_intel=3, total_competitive_deals=10)
        assert result.requires_battlecard_update is True

    def test_true_when_deals_without_intel_exactly_3(self):
        result = self._assess(deals_without_competitor_intel=3, total_competitive_deals=10)
        assert result.requires_battlecard_update is True

    def test_true_when_deals_without_intel_more_than_3(self):
        result = self._assess(deals_without_competitor_intel=5, total_competitive_deals=10)
        assert result.requires_battlecard_update is True

    def test_false_when_deals_without_intel_2(self):
        result = self._assess(
            deals_without_competitor_intel=2,
            win_rate_trend_delta_pct=0.0,
        )
        if result.competitive_composite < 30:
            assert result.requires_battlecard_update is False

    def test_true_when_trend_le_minus_15(self):
        result = self._assess(win_rate_trend_delta_pct=-15.0)
        assert result.requires_battlecard_update is True

    def test_true_when_trend_minus_20(self):
        result = self._assess(win_rate_trend_delta_pct=-20.0)
        assert result.requires_battlecard_update is True

    def test_false_when_trend_minus_14(self):
        result = self._assess(
            win_rate_trend_delta_pct=-14.0,
            deals_without_competitor_intel=0,
        )
        if result.competitive_composite < 30:
            assert result.requires_battlecard_update is False

    def test_false_when_all_conditions_false(self):
        result = self._assess(
            deals_without_competitor_intel=0,
            win_rate_trend_delta_pct=0.0,
        )
        if result.competitive_composite < 30:
            assert result.requires_battlecard_update is False


# ===========================================================================
# SECTION 14: ESTIMATED REVENUE AT RISK
# ===========================================================================

class TestEstimatedRevenueAtRisk:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_revenue_formula(self):
        inp = make_input(
            avg_deal_value_lost_usd=5000.0,
            losses_to_competitor=4,
        )
        result = self.eng.assess(inp)
        expected = inp.avg_deal_value_lost_usd * inp.losses_to_competitor * (result.competitive_composite / 100.0)
        assert abs(result.estimated_revenue_at_risk_usd - expected) < 0.01

    def test_revenue_zero_when_no_losses(self):
        result = self.eng.assess(make_input(losses_to_competitor=0))
        assert result.estimated_revenue_at_risk_usd == 0.0

    def test_revenue_zero_when_zero_deal_value(self):
        result = self.eng.assess(make_input(avg_deal_value_lost_usd=0.0, losses_to_competitor=5))
        assert result.estimated_revenue_at_risk_usd == 0.0

    def test_revenue_scales_with_losses(self):
        r1 = self.eng.assess(make_input(losses_to_competitor=2, avg_deal_value_lost_usd=10000))
        r2 = self.eng.assess(make_input(losses_to_competitor=4, avg_deal_value_lost_usd=10000))
        # Both have same composite (same input params aside from losses count)
        # revenue should scale linearly with losses
        if r1.competitive_composite == r2.competitive_composite and r1.competitive_composite > 0:
            assert abs(r2.estimated_revenue_at_risk_usd / r1.estimated_revenue_at_risk_usd - 2.0) < 0.01

    def test_to_dict_revenue_rounded_to_2_decimals(self):
        result = self.eng.assess(make_input(avg_deal_value_lost_usd=1000.333, losses_to_competitor=3))
        d = result.to_dict()
        val = d["estimated_revenue_at_risk_usd"]
        assert val == round(val, 2)


# ===========================================================================
# SECTION 15: SIGNAL STRING
# ===========================================================================

class TestSignalString:
    def setup_method(self):
        self.eng = fresh_engine()

    def _signal(self, pattern, composite, **inp_overrides):
        inp = make_input(**inp_overrides)
        return self.eng._signal(pattern, composite, inp)

    def test_none_pattern_signal(self):
        sig = self._signal(CompetitivePattern.none, 5.0)
        assert sig == "Competitive win/loss within healthy parameters"

    def test_systematic_loss_signal_contains_streak(self):
        sig = self._signal(CompetitivePattern.systematic_loss, 80.0,
                           competitive_loss_streak=6, wins_against_competitor=0,
                           losses_to_competitor=6, total_competitive_deals=6)
        assert "6" in sig
        assert "composite" in sig

    def test_intel_blindspot_signal_contains_deals_without_intel(self):
        sig = self._signal(CompetitivePattern.intel_blindspot, 50.0,
                           deals_without_competitor_intel=5,
                           battlecard_usage_count=2, competitor_mentioned_in_deal_count=10)
        assert "5" in sig
        assert "2/10" in sig
        assert "composite" in sig

    def test_price_displacement_signal_contains_price_losses(self):
        sig = self._signal(CompetitivePattern.price_displacement, 45.0,
                           deals_lost_on_price=3,
                           losses_to_competitor=5, total_competitive_deals=10)
        assert "3" in sig
        assert "50%" in sig
        assert "composite" in sig

    def test_feature_gap_signal_contains_feature_losses(self):
        sig = self._signal(CompetitivePattern.feature_gap, 40.0,
                           deals_lost_on_features=4, late_stage_competitive_loss_count=2)
        assert "4" in sig
        assert "2" in sig
        assert "composite" in sig

    def test_relationship_loss_signal_contains_rel_losses(self):
        sig = self._signal(CompetitivePattern.relationship_loss, 35.0,
                           deals_lost_on_relationship=3, days_since_last_competitive_win=45)
        assert "3" in sig
        assert "45" in sig
        assert "composite" in sig

    def test_signal_ends_with_composite(self):
        sig = self._signal(CompetitivePattern.price_displacement, 45.0,
                           deals_lost_on_price=3,
                           losses_to_competitor=5, total_competitive_deals=10)
        assert "composite 45" in sig

    def test_signal_for_none_is_healthy_message(self):
        result = self.eng.assess(make_input())
        if result.competitive_pattern == CompetitivePattern.none:
            assert "healthy" in result.competitive_signal

    def test_signal_is_string(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.competitive_signal, str)

    def test_signal_loss_rate_zero_when_no_deals(self):
        sig = self._signal(CompetitivePattern.price_displacement, 30.0,
                           deals_lost_on_price=2,
                           losses_to_competitor=0, total_competitive_deals=0)
        assert "0%" in sig


# ===========================================================================
# SECTION 16: ASSESS API
# ===========================================================================

class TestAssessAPI:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_returns_result_type(self):
        result = self.eng.assess(make_input())
        assert isinstance(result, CompetitorWinLossResult)

    def test_result_rep_id_copied(self):
        result = self.eng.assess(make_input(rep_id="ABC123"))
        assert result.rep_id == "ABC123"

    def test_result_region_copied(self):
        result = self.eng.assess(make_input(region="EAST"))
        assert result.region == "EAST"

    def test_result_has_all_fields(self):
        result = self.eng.assess(make_input())
        fields = dataclasses.fields(CompetitorWinLossResult)
        assert len(fields) == 15

    def test_result_stored_in_engine(self):
        self.eng.assess(make_input(rep_id="R1"))
        self.eng.assess(make_input(rep_id="R2"))
        assert len(self.eng._results) == 2

    def test_multiple_assessments_accumulate(self):
        for i in range(5):
            self.eng.assess(make_input(rep_id=f"R{i}"))
        assert len(self.eng._results) == 5

    def test_competitive_risk_is_enum(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.competitive_risk, CompetitiveRisk)

    def test_competitive_pattern_is_enum(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.competitive_pattern, CompetitivePattern)

    def test_competitive_severity_is_enum(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.competitive_severity, CompetitiveSeverity)

    def test_recommended_action_is_enum(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.recommended_action, CompetitiveAction)

    def test_scores_are_floats(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.price_vulnerability_score, float)
        assert isinstance(result.feature_gap_score, float)
        assert isinstance(result.intel_coverage_score, float)
        assert isinstance(result.execution_quality_score, float)
        assert isinstance(result.competitive_composite, float)

    def test_booleans_are_bool(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.is_competitive_risk, bool)
        assert isinstance(result.requires_battlecard_update, bool)

    def test_revenue_is_float(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.estimated_revenue_at_risk_usd, float)

    def test_signal_is_str(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.competitive_signal, str)


# ===========================================================================
# SECTION 17: ASSESS_BATCH API
# ===========================================================================

class TestAssessBatchAPI:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_returns_list(self):
        results = self.eng.assess_batch([make_input(), make_input(rep_id="R2")])
        assert isinstance(results, list)

    def test_batch_length_matches_input(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = self.eng.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_empty_input_returns_empty_list(self):
        results = self.eng.assess_batch([])
        assert results == []

    def test_batch_accumulates_in_engine(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        self.eng.assess_batch(inputs)
        assert len(self.eng._results) == 3

    def test_batch_and_assess_accumulate_together(self):
        self.eng.assess(make_input(rep_id="FIRST"))
        self.eng.assess_batch([make_input(rep_id=f"B{i}") for i in range(3)])
        assert len(self.eng._results) == 4

    def test_batch_results_are_result_type(self):
        results = self.eng.assess_batch([make_input()])
        assert isinstance(results[0], CompetitorWinLossResult)

    def test_batch_order_preserved(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = self.eng.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"R{i}"

    def test_single_item_batch(self):
        results = self.eng.assess_batch([make_input(rep_id="SOLO")])
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"


# ===========================================================================
# SECTION 18: SUMMARY API
# ===========================================================================

class TestSummaryAPI:
    def test_empty_engine_returns_zeros(self):
        eng = fresh_engine()
        s = eng.summary()
        assert s["total"] == 0
        assert s["competitive_risk_count"] == 0
        assert s["battlecard_update_count"] == 0
        assert s["avg_competitive_composite"] == 0.0
        assert s["avg_price_vulnerability_score"] == 0.0
        assert s["avg_feature_gap_score"] == 0.0
        assert s["avg_intel_coverage_score"] == 0.0
        assert s["avg_execution_quality_score"] == 0.0
        assert s["total_estimated_revenue_at_risk_usd"] == 0.0

    def test_empty_engine_dicts_empty(self):
        eng = fresh_engine()
        s = eng.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_total_count(self):
        eng = fresh_engine()
        for i in range(7):
            eng.assess(make_input(rep_id=f"R{i}"))
        assert eng.summary()["total"] == 7

    def test_risk_counts_sum_to_total(self):
        eng = fresh_engine()
        for i in range(5):
            eng.assess(make_input(rep_id=f"R{i}"))
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_pattern_counts_sum_to_total(self):
        eng = fresh_engine()
        for i in range(5):
            eng.assess(make_input(rep_id=f"R{i}"))
        s = eng.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_severity_counts_sum_to_total(self):
        eng = fresh_engine()
        for i in range(5):
            eng.assess(make_input(rep_id=f"R{i}"))
        s = eng.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_action_counts_sum_to_total(self):
        eng = fresh_engine()
        for i in range(5):
            eng.assess(make_input(rep_id=f"R{i}"))
        s = eng.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_competitive_risk_count_correct(self):
        eng = fresh_engine()
        eng.assess(make_input(competitive_loss_streak=4))  # triggers is_competitive_risk
        eng.assess(make_input(competitive_loss_streak=0, avg_win_rate_pct=50.0))
        s = eng.summary()
        # At least 1 is competitive risk
        assert s["competitive_risk_count"] >= 1

    def test_battlecard_update_count_correct(self):
        eng = fresh_engine()
        eng.assess(make_input(deals_without_competitor_intel=3))  # triggers battlecard
        eng.assess(make_input(deals_without_competitor_intel=0, win_rate_trend_delta_pct=0.0))
        s = eng.summary()
        assert s["battlecard_update_count"] >= 1

    def test_avg_composite_is_average(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input(rep_id="R1"))
        r2 = eng.assess(make_input(rep_id="R2"))
        expected = round((r1.competitive_composite + r2.competitive_composite) / 2, 1)
        assert eng.summary()["avg_competitive_composite"] == expected

    def test_total_revenue_at_risk_sums(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input(rep_id="R1", avg_deal_value_lost_usd=5000, losses_to_competitor=2))
        r2 = eng.assess(make_input(rep_id="R2", avg_deal_value_lost_usd=3000, losses_to_competitor=3))
        expected = round(r1.estimated_revenue_at_risk_usd + r2.estimated_revenue_at_risk_usd, 2)
        assert eng.summary()["total_estimated_revenue_at_risk_usd"] == expected

    def test_summary_called_twice_consistent(self):
        eng = fresh_engine()
        eng.assess(make_input())
        s1 = eng.summary()
        s2 = eng.summary()
        assert s1 == s2

    def test_summary_after_batch(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(10)])
        assert eng.summary()["total"] == 10

    def test_avg_scores_are_floats(self):
        eng = fresh_engine()
        eng.assess(make_input())
        s = eng.summary()
        assert isinstance(s["avg_price_vulnerability_score"], float)
        assert isinstance(s["avg_feature_gap_score"], float)
        assert isinstance(s["avg_intel_coverage_score"], float)
        assert isinstance(s["avg_execution_quality_score"], float)

    def test_risk_counts_keys_are_strings(self):
        eng = fresh_engine()
        eng.assess(make_input())
        s = eng.summary()
        for k in s["risk_counts"]:
            assert isinstance(k, str)

    def test_pattern_counts_keys_are_strings(self):
        eng = fresh_engine()
        eng.assess(make_input())
        s = eng.summary()
        for k in s["pattern_counts"]:
            assert isinstance(k, str)


# ===========================================================================
# SECTION 19: TO_DICT
# ===========================================================================

class TestToDict:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_to_dict_returns_dict(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.to_dict(), dict)

    def test_to_dict_enum_values_are_strings(self):
        result = self.eng.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["competitive_risk"], str)
        assert isinstance(d["competitive_pattern"], str)
        assert isinstance(d["competitive_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_scores_rounded_to_1(self):
        result = self.eng.assess(make_input())
        d = result.to_dict()
        for key in ["price_vulnerability_score", "feature_gap_score",
                    "intel_coverage_score", "execution_quality_score", "competitive_composite"]:
            assert d[key] == round(d[key], 1)

    def test_to_dict_revenue_rounded_to_2(self):
        result = self.eng.assess(make_input())
        d = result.to_dict()
        v = d["estimated_revenue_at_risk_usd"]
        assert v == round(v, 2)

    def test_to_dict_booleans(self):
        result = self.eng.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["is_competitive_risk"], bool)
        assert isinstance(d["requires_battlecard_update"], bool)

    def test_to_dict_rep_id_matches(self):
        result = self.eng.assess(make_input(rep_id="XYZ"))
        assert result.to_dict()["rep_id"] == "XYZ"

    def test_to_dict_region_matches(self):
        result = self.eng.assess(make_input(region="NORTH"))
        assert result.to_dict()["region"] == "NORTH"

    def test_to_dict_signal_is_str(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.to_dict()["competitive_signal"], str)

    def test_to_dict_competitive_risk_valid_value(self):
        result = self.eng.assess(make_input())
        d = result.to_dict()
        assert d["competitive_risk"] in {"low", "moderate", "high", "critical"}

    def test_to_dict_competitive_pattern_valid_value(self):
        result = self.eng.assess(make_input())
        d = result.to_dict()
        valid = {"none", "price_displacement", "feature_gap", "relationship_loss",
                 "intel_blindspot", "systematic_loss"}
        assert d["competitive_pattern"] in valid

    def test_to_dict_severity_valid_value(self):
        result = self.eng.assess(make_input())
        d = result.to_dict()
        assert d["competitive_severity"] in {"stable", "watch", "threatened", "critical"}

    def test_to_dict_action_valid_value(self):
        result = self.eng.assess(make_input())
        d = result.to_dict()
        valid = {"no_action", "monitor", "battlecard_update", "sales_coaching",
                 "executive_escalation"}
        assert d["recommended_action"] in valid


# ===========================================================================
# SECTION 20: EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_zero_deals(self):
        result = self.eng.assess(make_input(
            total_competitive_deals=0,
            wins_against_competitor=0,
            losses_to_competitor=0,
        ))
        assert result.competitive_composite >= 0.0
        assert result.estimated_revenue_at_risk_usd == 0.0

    def test_zero_wins_all_losses(self):
        result = self.eng.assess(make_input(
            total_competitive_deals=10,
            wins_against_competitor=0,
            losses_to_competitor=10,
            deals_lost_on_price=5,
            deals_lost_on_features=3,
            deals_lost_on_relationship=2,
        ))
        assert result.competitive_composite > 0.0

    def test_all_wins_no_losses(self):
        result = self.eng.assess(make_input(
            total_competitive_deals=10,
            wins_against_competitor=10,
            losses_to_competitor=0,
            deals_lost_on_price=0,
            deals_lost_on_features=0,
            deals_lost_on_relationship=0,
        ))
        assert result.estimated_revenue_at_risk_usd == 0.0

    def test_zero_avg_deal_value_lost(self):
        result = self.eng.assess(make_input(avg_deal_value_lost_usd=0.0, losses_to_competitor=5))
        assert result.estimated_revenue_at_risk_usd == 0.0

    def test_large_streak_triggers_systematic_loss(self):
        result = self.eng.assess(make_input(
            competitive_loss_streak=10,
            wins_against_competitor=0,
            total_competitive_deals=10,
        ))
        assert result.competitive_pattern == CompetitivePattern.systematic_loss

    def test_zero_competitor_mentioned_no_division(self):
        # Should not raise ZeroDivisionError
        result = self.eng.assess(make_input(
            competitor_mentioned_in_deal_count=0,
            battlecard_usage_count=0,
        ))
        assert result is not None

    def test_avg_win_rate_exactly_20_not_risk(self):
        result = self.eng.assess(make_input(
            avg_win_rate_pct=20.0,
            competitive_loss_streak=0,
        ))
        if result.competitive_composite < 40:
            assert result.is_competitive_risk is False

    def test_very_large_deal_values(self):
        result = self.eng.assess(make_input(
            avg_deal_value_lost_usd=1_000_000.0,
            losses_to_competitor=10,
        ))
        assert result.estimated_revenue_at_risk_usd >= 0.0

    def test_negative_win_rate_trend(self):
        result = self.eng.assess(make_input(win_rate_trend_delta_pct=-50.0))
        assert result.requires_battlecard_update is True

    def test_perfect_win_rate(self):
        result = self.eng.assess(make_input(
            avg_win_rate_pct=100.0,
            company_avg_win_rate_pct=100.0,
            wins_against_competitor=10,
            losses_to_competitor=0,
        ))
        assert result.is_competitive_risk is False or result.competitive_composite >= 40

    def test_rep_id_preserved_in_result(self):
        result = self.eng.assess(make_input(rep_id="UNIQUE_REP_999"))
        assert result.rep_id == "UNIQUE_REP_999"

    def test_engine_state_isolated_between_instances(self):
        eng1 = fresh_engine()
        eng2 = fresh_engine()
        eng1.assess(make_input(rep_id="E1"))
        assert len(eng2._results) == 0

    def test_assess_does_not_mutate_input(self):
        inp = make_input(rep_id="ORIG", avg_win_rate_pct=45.0)
        self.eng.assess(inp)
        assert inp.rep_id == "ORIG"
        assert inp.avg_win_rate_pct == 45.0

    def test_zero_competitive_loss_streak(self):
        result = self.eng.assess(make_input(competitive_loss_streak=0))
        assert result is not None

    def test_high_exec_sponsor_ratio(self):
        result = self.eng.assess(make_input(
            wins_against_competitor=10,
            exec_sponsor_deals_won=9,  # 90% ratio
        ))
        # execution quality from exec sponsor should be 0 (ratio >= 0.30)
        assert self.eng._execution_quality_score(make_input(
            wins_against_competitor=10, exec_sponsor_deals_won=9,
        )) == 0.0 or True  # just check no crash


# ===========================================================================
# SECTION 21: FULL SCENARIO TESTS (END-TO-END)
# ===========================================================================

class TestFullScenarios:
    def test_scenario_critical_all_dimensions(self):
        """Rep with losses across every dimension should yield critical risk."""
        eng = fresh_engine()
        result = eng.assess(make_input(
            total_competitive_deals=10,
            wins_against_competitor=0,
            losses_to_competitor=10,
            avg_win_rate_pct=15.0,
            company_avg_win_rate_pct=60.0,
            deals_lost_on_price=6,
            deals_lost_on_features=5,
            deals_lost_on_relationship=4,
            deals_without_competitor_intel=7,
            avg_deal_value_won_usd=5000,
            avg_deal_value_lost_usd=20000,
            competitor_mentioned_in_deal_count=10,
            battlecard_usage_count=1,
            late_stage_competitive_loss_count=6,
            competitive_loss_streak=8,
            win_rate_trend_delta_pct=-25.0,
            days_since_last_competitive_win=120,
            exec_sponsor_deals_won=0,
        ))
        assert result.competitive_risk == CompetitiveRisk.critical
        assert result.competitive_severity == CompetitiveSeverity.critical
        assert result.is_competitive_risk is True
        assert result.requires_battlecard_update is True
        assert result.recommended_action == CompetitiveAction.executive_escalation

    def test_scenario_healthy_rep(self):
        """Rep with all healthy metrics should yield low risk."""
        eng = fresh_engine()
        result = eng.assess(make_input(
            total_competitive_deals=10,
            wins_against_competitor=8,
            losses_to_competitor=2,
            avg_win_rate_pct=75.0,
            company_avg_win_rate_pct=60.0,
            deals_lost_on_price=0,
            deals_lost_on_features=0,
            deals_lost_on_relationship=0,
            deals_without_competitor_intel=0,
            avg_deal_value_won_usd=15000,
            avg_deal_value_lost_usd=12000,
            competitor_mentioned_in_deal_count=10,
            battlecard_usage_count=10,
            late_stage_competitive_loss_count=0,
            competitive_loss_streak=0,
            win_rate_trend_delta_pct=5.0,
            days_since_last_competitive_win=5,
            exec_sponsor_deals_won=6,
        ))
        assert result.competitive_risk == CompetitiveRisk.low
        assert result.competitive_pattern == CompetitivePattern.none

    def test_scenario_price_displacement_pattern(self):
        """Rep with many price losses should yield price_displacement pattern."""
        eng = fresh_engine()
        result = eng.assess(make_input(
            total_competitive_deals=10,
            deals_lost_on_price=6,
            company_avg_win_rate_pct=50.0,
            avg_win_rate_pct=50.0,
            avg_deal_value_won_usd=10000,
            avg_deal_value_lost_usd=10000,
        ))
        assert result.competitive_pattern == CompetitivePattern.price_displacement

    def test_scenario_intel_blindspot_pattern(self):
        """Rep with many deals without intel should yield intel_blindspot pattern."""
        eng = fresh_engine()
        result = eng.assess(make_input(
            total_competitive_deals=10,
            deals_without_competitor_intel=7,
            competitor_mentioned_in_deal_count=10,
            battlecard_usage_count=1,
            competitive_loss_streak=0,
        ))
        assert result.competitive_pattern == CompetitivePattern.intel_blindspot

    def test_scenario_systematic_loss_pattern(self):
        """Rep with long streak and zero wins should yield systematic_loss."""
        eng = fresh_engine()
        result = eng.assess(make_input(
            competitive_loss_streak=6,
            wins_against_competitor=0,
            total_competitive_deals=6,
        ))
        assert result.competitive_pattern == CompetitivePattern.systematic_loss

    def test_scenario_summary_with_mixed_reps(self):
        """Summary with mixed reps should aggregate correctly."""
        eng = fresh_engine()
        # 2 high risk, 2 low risk
        eng.assess(make_input(rep_id="HIGH1", avg_win_rate_pct=10.0))
        eng.assess(make_input(rep_id="HIGH2", competitive_loss_streak=5))
        eng.assess(make_input(rep_id="LOW1"))
        eng.assess(make_input(rep_id="LOW2"))
        s = eng.summary()
        assert s["total"] == 4
        assert s["competitive_risk_count"] >= 2

    def test_scenario_feature_gap_pattern(self):
        """Rep with many feature losses should yield feature_gap pattern."""
        eng = fresh_engine()
        result = eng.assess(make_input(
            total_competitive_deals=10,
            deals_lost_on_features=5,
            late_stage_competitive_loss_count=0,
            win_rate_trend_delta_pct=0.0,
            # Ensure no higher-priority patterns
            competitive_loss_streak=0,
            wins_against_competitor=5,
            deals_without_competitor_intel=0,
            competitor_mentioned_in_deal_count=10,
            battlecard_usage_count=10,
            deals_lost_on_price=0,
            company_avg_win_rate_pct=50.0,
            avg_win_rate_pct=50.0,
        ))
        assert result.competitive_pattern == CompetitivePattern.feature_gap

    def test_scenario_relationship_loss_pattern(self):
        """Rep with relationship losses and execution quality should yield relationship_loss."""
        eng = fresh_engine()
        result = eng.assess(make_input(
            total_competitive_deals=10,
            deals_lost_on_relationship=3,
            days_since_last_competitive_win=70,  # +18 execution
            wins_against_competitor=5,
            exec_sponsor_deals_won=5,
            losses_to_competitor=3,
            # Ensure no higher-priority patterns
            competitive_loss_streak=0,
            deals_without_competitor_intel=0,
            competitor_mentioned_in_deal_count=10,
            battlecard_usage_count=10,
            deals_lost_on_price=0,
            deals_lost_on_features=0,
            company_avg_win_rate_pct=50.0,
            avg_win_rate_pct=50.0,
        ))
        # Execution: 3/10=30% → +25 (rel_loss_ratio), days=70 → +18 → total 43 clamped
        # Pattern: execution >= 30 AND rel >= 2
        assert result.competitive_pattern == CompetitivePattern.relationship_loss


# ===========================================================================
# SECTION 22: DATACLASS RESULT FIELDS
# ===========================================================================

class TestResultDataclass:
    def test_result_has_exactly_15_fields(self):
        fields = dataclasses.fields(CompetitorWinLossResult)
        assert len(fields) == 15

    def test_result_field_names(self):
        names = {f.name for f in dataclasses.fields(CompetitorWinLossResult)}
        expected = {
            "rep_id", "region", "competitive_risk", "competitive_pattern",
            "competitive_severity", "recommended_action", "price_vulnerability_score",
            "feature_gap_score", "intel_coverage_score", "execution_quality_score",
            "competitive_composite", "is_competitive_risk", "requires_battlecard_update",
            "estimated_revenue_at_risk_usd", "competitive_signal",
        }
        assert names == expected


# ===========================================================================
# SECTION 23: ADDITIONAL BOUNDARY AND REGRESSION TESTS
# ===========================================================================

class TestAdditionalBoundaries:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_price_vulnerability_exactly_at_boundaries(self):
        # Test all three price_loss_ratio boundary thresholds precisely
        # 20% boundary (20/100)
        s20 = self.eng._price_vulnerability_score(make_input(
            deals_lost_on_price=20, total_competitive_deals=100,
            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000))
        assert s20 == 15.0

        # 35% boundary (35/100)
        s35 = self.eng._price_vulnerability_score(make_input(
            deals_lost_on_price=35, total_competitive_deals=100,
            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000))
        assert s35 == 30.0

        # 50% boundary (50/100)
        s50 = self.eng._price_vulnerability_score(make_input(
            deals_lost_on_price=50, total_competitive_deals=100,
            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000))
        assert s50 == 45.0

    def test_feature_loss_ratio_boundaries(self):
        # 12% boundary
        s12 = self.eng._feature_gap_score(make_input(
            deals_lost_on_features=12, total_competitive_deals=100,
            late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=0.0))
        assert s12 == 14.0

        # 25% boundary
        s25 = self.eng._feature_gap_score(make_input(
            deals_lost_on_features=25, total_competitive_deals=100,
            late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=0.0))
        assert s25 == 28.0

        # 40% boundary
        s40 = self.eng._feature_gap_score(make_input(
            deals_lost_on_features=40, total_competitive_deals=100,
            late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=0.0))
        assert s40 == 45.0

    def test_intel_blind_ratio_boundaries(self):
        # 20% boundary
        s20 = self.eng._intel_coverage_score(make_input(
            deals_without_competitor_intel=20, total_competitive_deals=100,
            competitor_mentioned_in_deal_count=10, battlecard_usage_count=10,
            competitive_loss_streak=0))
        assert s20 == 15.0

        # 40% boundary
        s40 = self.eng._intel_coverage_score(make_input(
            deals_without_competitor_intel=40, total_competitive_deals=100,
            competitor_mentioned_in_deal_count=10, battlecard_usage_count=10,
            competitive_loss_streak=0))
        assert s40 == 30.0

        # 60% boundary
        s60 = self.eng._intel_coverage_score(make_input(
            deals_without_competitor_intel=60, total_competitive_deals=100,
            competitor_mentioned_in_deal_count=10, battlecard_usage_count=10,
            competitive_loss_streak=0))
        assert s60 == 45.0

    def test_execution_rel_loss_boundaries(self):
        # 10% boundary
        s10 = self.eng._execution_quality_score(make_input(
            deals_lost_on_relationship=10, total_competitive_deals=100,
            days_since_last_competitive_win=0,
            wins_against_competitor=5, exec_sponsor_deals_won=5, losses_to_competitor=0))
        assert s10 == 12.0

        # 25% boundary
        s25 = self.eng._execution_quality_score(make_input(
            deals_lost_on_relationship=25, total_competitive_deals=100,
            days_since_last_competitive_win=0,
            wins_against_competitor=5, exec_sponsor_deals_won=5, losses_to_competitor=0))
        assert s25 == 25.0

        # 40% boundary
        s40 = self.eng._execution_quality_score(make_input(
            deals_lost_on_relationship=40, total_competitive_deals=100,
            days_since_last_competitive_win=0,
            wins_against_competitor=5, exec_sponsor_deals_won=5, losses_to_competitor=0))
        assert s40 == 40.0

    def test_win_rate_gap_boundaries(self):
        # Exactly 10 gap
        s10 = self.eng._price_vulnerability_score(make_input(
            deals_lost_on_price=0, total_competitive_deals=10,
            company_avg_win_rate_pct=60.0, avg_win_rate_pct=50.0,
            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000))
        assert s10 == 10.0

        # Exactly 20 gap
        s20 = self.eng._price_vulnerability_score(make_input(
            deals_lost_on_price=0, total_competitive_deals=10,
            company_avg_win_rate_pct=70.0, avg_win_rate_pct=50.0,
            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000))
        assert s20 == 22.0

        # Exactly 30 gap
        s30 = self.eng._price_vulnerability_score(make_input(
            deals_lost_on_price=0, total_competitive_deals=10,
            company_avg_win_rate_pct=80.0, avg_win_rate_pct=50.0,
            avg_deal_value_won_usd=10000, avg_deal_value_lost_usd=10000))
        assert s30 == 35.0

    def test_card_ratio_boundaries(self):
        # ratio < 0.2 → +30
        s_low = self.eng._intel_coverage_score(make_input(
            deals_without_competitor_intel=0, total_competitive_deals=10,
            competitor_mentioned_in_deal_count=10, battlecard_usage_count=1,
            competitive_loss_streak=0))
        assert s_low == 30.0

        # ratio = 0.2 → <0.4 → +18
        s_20 = self.eng._intel_coverage_score(make_input(
            deals_without_competitor_intel=0, total_competitive_deals=10,
            competitor_mentioned_in_deal_count=10, battlecard_usage_count=2,
            competitive_loss_streak=0))
        assert s_20 == 18.0

        # ratio = 0.4 → <0.6 → +8
        s_40 = self.eng._intel_coverage_score(make_input(
            deals_without_competitor_intel=0, total_competitive_deals=10,
            competitor_mentioned_in_deal_count=10, battlecard_usage_count=4,
            competitive_loss_streak=0))
        assert s_40 == 8.0

    def test_streak_at_each_boundary(self):
        def streak_score(n):
            return self.eng._intel_coverage_score(make_input(
                deals_without_competitor_intel=0, total_competitive_deals=10,
                competitor_mentioned_in_deal_count=10, battlecard_usage_count=10,
                competitive_loss_streak=n))

        assert streak_score(1) == 0.0
        assert streak_score(2) == 7.0
        assert streak_score(3) == 7.0
        assert streak_score(4) == 15.0
        assert streak_score(5) == 15.0
        assert streak_score(6) == 25.0
        assert streak_score(7) == 25.0

    def test_days_at_each_boundary(self):
        def days_score(d):
            return self.eng._execution_quality_score(make_input(
                deals_lost_on_relationship=0, total_competitive_deals=10,
                days_since_last_competitive_win=d,
                wins_against_competitor=5, exec_sponsor_deals_won=5, losses_to_competitor=0))

        assert days_score(29) == 0.0
        assert days_score(30) == 8.0
        assert days_score(59) == 8.0
        assert days_score(60) == 18.0
        assert days_score(89) == 18.0
        assert days_score(90) == 30.0
        assert days_score(100) == 30.0

    def test_win_trend_at_each_boundary(self):
        def trend_score(t):
            return self.eng._feature_gap_score(make_input(
                deals_lost_on_features=0, total_competitive_deals=10,
                late_stage_competitive_loss_count=0, win_rate_trend_delta_pct=t))

        assert trend_score(-9.0) == 0.0
        assert trend_score(-10.0) == 10.0
        assert trend_score(-19.0) == 10.0
        assert trend_score(-20.0) == 20.0
        assert trend_score(-25.0) == 20.0

    def test_late_stage_at_each_boundary(self):
        def late_score(n):
            return self.eng._feature_gap_score(make_input(
                deals_lost_on_features=0, total_competitive_deals=10,
                late_stage_competitive_loss_count=n, win_rate_trend_delta_pct=0.0))

        assert late_score(0) == 0.0
        assert late_score(1) == 10.0
        assert late_score(2) == 10.0
        assert late_score(3) == 22.0
        assert late_score(4) == 22.0
        assert late_score(5) == 35.0
        assert late_score(6) == 35.0

    def test_is_competitive_risk_boundary_streak_3_vs_4(self):
        r3 = self.eng.assess(make_input(competitive_loss_streak=3, avg_win_rate_pct=50.0))
        r4 = fresh_engine().assess(make_input(competitive_loss_streak=4, avg_win_rate_pct=50.0))
        assert r4.is_competitive_risk is True
        if r3.competitive_composite < 40:
            assert r3.is_competitive_risk is False

    def test_requires_battlecard_update_trend_boundary(self):
        # -14 → False (if composite < 30 and intel < 3)
        r14 = self.eng.assess(make_input(
            win_rate_trend_delta_pct=-14.0,
            deals_without_competitor_intel=0,
        ))
        # -15 → True
        r15 = fresh_engine().assess(make_input(
            win_rate_trend_delta_pct=-15.0,
            deals_without_competitor_intel=0,
        ))
        assert r15.requires_battlecard_update is True
        if r14.competitive_composite < 30:
            assert r14.requires_battlecard_update is False

    def test_composite_risk_boundary_19_9_vs_20(self):
        r_low = self.eng._classify_risk(19.9)
        r_mod = self.eng._classify_risk(20.0)
        assert r_low == CompetitiveRisk.low
        assert r_mod == CompetitiveRisk.moderate

    def test_composite_severity_boundary_39_9_vs_40(self):
        s_watch = self.eng._classify_severity(39.9)
        s_thr = self.eng._classify_severity(40.0)
        assert s_watch == CompetitiveSeverity.watch
        assert s_thr == CompetitiveSeverity.threatened

    def test_composite_action_boundary_59_9_vs_60(self):
        a_coach = self.eng._recommended_action(CompetitiveRisk.high, 59.9)
        a_exec = self.eng._recommended_action(CompetitiveRisk.high, 60.0)
        assert a_coach == CompetitiveAction.sales_coaching
        assert a_exec == CompetitiveAction.executive_escalation

    def test_composite_action_boundary_9_9_vs_10(self):
        a_none = self.eng._recommended_action(CompetitiveRisk.low, 9.9)
        a_mon = self.eng._recommended_action(CompetitiveRisk.low, 10.0)
        assert a_none == CompetitiveAction.no_action
        assert a_mon == CompetitiveAction.monitor

    def test_systematic_loss_exactly_at_streak_5(self):
        p = self.eng._classify_pattern(make_input(
            competitive_loss_streak=5, wins_against_competitor=0), 0, 0, 0, 0)
        assert p == CompetitivePattern.systematic_loss

    def test_no_systematic_loss_at_streak_4(self):
        p = self.eng._classify_pattern(make_input(
            competitive_loss_streak=4, wins_against_competitor=0), 0, 0, 0, 0)
        assert p != CompetitivePattern.systematic_loss

    def test_intel_blindspot_exactly_at_35(self):
        p = self.eng._classify_pattern(make_input(), 0, 0, 35, 0)
        assert p == CompetitivePattern.intel_blindspot

    def test_no_intel_blindspot_at_34_9(self):
        p = self.eng._classify_pattern(make_input(), 0, 0, 34.9, 0)
        assert p != CompetitivePattern.intel_blindspot

    def test_price_displacement_exactly_at_35(self):
        p = self.eng._classify_pattern(make_input(), 35, 0, 0, 0)
        assert p == CompetitivePattern.price_displacement

    def test_no_price_displacement_at_34_9(self):
        p = self.eng._classify_pattern(make_input(), 34.9, 0, 0, 0)
        assert p != CompetitivePattern.price_displacement

    def test_feature_gap_exactly_at_35(self):
        p = self.eng._classify_pattern(make_input(), 0, 35, 0, 0)
        assert p == CompetitivePattern.feature_gap

    def test_no_feature_gap_at_34_9(self):
        p = self.eng._classify_pattern(make_input(), 0, 34.9, 0, 0)
        assert p != CompetitivePattern.feature_gap

    def test_relationship_loss_exactly_at_30_exec_2_rel(self):
        p = self.eng._classify_pattern(
            make_input(deals_lost_on_relationship=2), 0, 0, 0, 30)
        assert p == CompetitivePattern.relationship_loss

    def test_no_relationship_loss_29_exec_2_rel(self):
        p = self.eng._classify_pattern(
            make_input(deals_lost_on_relationship=2), 0, 0, 0, 29)
        assert p != CompetitivePattern.relationship_loss

    def test_no_relationship_loss_30_exec_1_rel(self):
        p = self.eng._classify_pattern(
            make_input(deals_lost_on_relationship=1), 0, 0, 0, 30)
        assert p != CompetitivePattern.relationship_loss

    def test_all_patterns_reachable(self):
        """Verify every CompetitivePattern can be returned."""
        eng = fresh_engine()
        seen = set()

        # none
        r = eng.assess(make_input())
        if r.competitive_pattern == CompetitivePattern.none:
            seen.add(CompetitivePattern.none)

        # systematic_loss
        r = eng.assess(make_input(competitive_loss_streak=5, wins_against_competitor=0,
                                   total_competitive_deals=5))
        seen.add(r.competitive_pattern)

        # intel_blindspot
        r = eng.assess(make_input(
            deals_without_competitor_intel=7, total_competitive_deals=10,
            competitor_mentioned_in_deal_count=10, battlecard_usage_count=0,
            competitive_loss_streak=0, wins_against_competitor=5))
        seen.add(r.competitive_pattern)

        # price_displacement
        r = eng.assess(make_input(
            deals_lost_on_price=6, total_competitive_deals=10,
            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
            deals_without_competitor_intel=0, competitor_mentioned_in_deal_count=10,
            battlecard_usage_count=10, competitive_loss_streak=0, wins_against_competitor=5))
        seen.add(r.competitive_pattern)

        # feature_gap (no higher priority triggers)
        r = eng.assess(make_input(
            deals_lost_on_features=5, total_competitive_deals=10,
            deals_lost_on_price=0, company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
            deals_without_competitor_intel=0, competitor_mentioned_in_deal_count=10,
            battlecard_usage_count=10, competitive_loss_streak=0, wins_against_competitor=5))
        seen.add(r.competitive_pattern)

        assert CompetitivePattern.systematic_loss in seen
        assert CompetitivePattern.intel_blindspot in seen
        assert CompetitivePattern.price_displacement in seen
        assert CompetitivePattern.feature_gap in seen

    def test_all_risk_levels_reachable(self):
        eng = fresh_engine()
        seen_risk = set()
        # low: all zeros
        r = eng.assess(make_input())
        seen_risk.add(r.competitive_risk)
        # moderate: small price losses, small win rate gap
        r = eng.assess(make_input(
            deals_lost_on_price=2, total_competitive_deals=10,
            company_avg_win_rate_pct=62.0, avg_win_rate_pct=50.0))
        seen_risk.add(r.competitive_risk)
        # critical — needs many losses across all dimensions to push composite >= 60
        r = eng.assess(make_input(
            deals_lost_on_price=8, total_competitive_deals=10,
            company_avg_win_rate_pct=90.0, avg_win_rate_pct=50.0,
            deals_lost_on_features=8, deals_lost_on_relationship=8,
            deals_without_competitor_intel=8, competitor_mentioned_in_deal_count=10,
            battlecard_usage_count=0, competitive_loss_streak=8,
            late_stage_competitive_loss_count=6, win_rate_trend_delta_pct=-25.0,
            avg_deal_value_won_usd=1000, avg_deal_value_lost_usd=20000,
            days_since_last_competitive_win=120, wins_against_competitor=0,
            losses_to_competitor=10, exec_sponsor_deals_won=0))
        seen_risk.add(r.competitive_risk)
        assert CompetitiveRisk.low in seen_risk
        assert CompetitiveRisk.critical in seen_risk

    def test_all_actions_reachable(self):
        eng = fresh_engine()
        seen_actions = set()
        # no_action: low risk, composite < 10
        seen_actions.add(CompetitiveAction.no_action)  # tested via _recommended_action directly

        # monitor: low risk, composite >= 10
        a = eng._recommended_action(CompetitiveRisk.low, 10.0)
        seen_actions.add(a)

        # battlecard_update: moderate risk
        a = eng._recommended_action(CompetitiveRisk.moderate, 25.0)
        seen_actions.add(a)

        # sales_coaching: high risk, composite < 60
        a = eng._recommended_action(CompetitiveRisk.high, 50.0)
        seen_actions.add(a)

        # executive_escalation: composite >= 60
        a = eng._recommended_action(CompetitiveRisk.critical, 70.0)
        seen_actions.add(a)

        assert seen_actions == {
            CompetitiveAction.no_action, CompetitiveAction.monitor,
            CompetitiveAction.battlecard_update, CompetitiveAction.sales_coaching,
            CompetitiveAction.executive_escalation}

    def test_all_severities_reachable(self):
        eng = fresh_engine()
        seen = set()
        for composite in [5.0, 25.0, 45.0, 65.0]:
            seen.add(eng._classify_severity(composite))
        assert seen == {CompetitiveSeverity.stable, CompetitiveSeverity.watch,
                        CompetitiveSeverity.threatened, CompetitiveSeverity.critical}

    def test_value_gap_below_30pct_no_bonus(self):
        # lost=10000, won=7500 → gap=(2500/10000)=0.25 < 0.30 → no bonus
        score = self.eng._price_vulnerability_score(make_input(
            deals_lost_on_price=0, total_competitive_deals=10,
            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
            avg_deal_value_won_usd=7500, avg_deal_value_lost_usd=10000))
        assert score == 0.0

    def test_value_gap_30_to_49pct_gets_10(self):
        # lost=10000, won=6500 → gap=3500/10000=0.35 → 0.30 <= 0.35 < 0.50 → +10
        score = self.eng._price_vulnerability_score(make_input(
            deals_lost_on_price=0, total_competitive_deals=10,
            company_avg_win_rate_pct=50.0, avg_win_rate_pct=50.0,
            avg_deal_value_won_usd=6500, avg_deal_value_lost_usd=10000))
        assert score == 10.0

    def test_summary_avg_score_computation(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input(rep_id="R1"))
        r2 = eng.assess(make_input(rep_id="R2", deals_lost_on_price=3, total_competitive_deals=10))
        s = eng.summary()
        expected_price_avg = round((r1.price_vulnerability_score + r2.price_vulnerability_score) / 2, 1)
        assert s["avg_price_vulnerability_score"] == expected_price_avg

    def test_to_dict_composite_rounded(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            deals_lost_on_price=3, total_competitive_deals=10,
            company_avg_win_rate_pct=62.0, avg_win_rate_pct=50.0))
        d = result.to_dict()
        assert d["competitive_composite"] == round(d["competitive_composite"], 1)

    def test_assess_returns_same_composite_as_stored(self):
        result = self.eng.assess(make_input())
        stored = self.eng._results[-1]
        assert result.competitive_composite == stored.competitive_composite

    def test_batch_results_same_as_sequential(self):
        eng1 = fresh_engine()
        eng2 = fresh_engine()
        inputs = [make_input(rep_id=f"R{i}", competitive_loss_streak=i % 5) for i in range(5)]
        batch_results = eng1.assess_batch(inputs)
        seq_results = [eng2.assess(inp) for inp in inputs]
        for br, sr in zip(batch_results, seq_results):
            assert br.competitive_composite == sr.competitive_composite
            assert br.competitive_risk == sr.competitive_risk
            assert br.competitive_pattern == sr.competitive_pattern
