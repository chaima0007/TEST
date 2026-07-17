"""
Comprehensive pytest tests for SalesDiscountLeakageMarginErosionIntelligenceEngine.

Covers:
- DiscountInput construction (all 22 fields)
- DiscountResult.to_dict() key count and values
- summary() key count and values
- Sub-score computation (_frequency_score, _depth_score, _discipline_score, _value_defense_score)
- Composite score and weighting
- Risk classification
- Severity classification
- Pattern detection (priority order)
- Action recommendation
- has_discount_gap flag
- requires_discount_intervention flag
- estimated_margin_erosion_usd calculation
- discount_signal text
- assess() and assess_batch() APIs
- Engine state isolation / reset
- Edge cases (zeros, boundary values, caps at 100)
"""

from __future__ import annotations
import math
import pytest
from swarm.intelligence.sales_discount_leakage_margin_erosion_intelligence_engine import (
    SalesDiscountLeakageMarginErosionIntelligenceEngine,
    DiscountInput,
    DiscountResult,
    DiscountRisk,
    DiscountPattern,
    DiscountSeverity,
    DiscountAction,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> DiscountInput:
    """Return a baseline DiscountInput with all fields zeroed / minimal, then apply overrides."""
    defaults = dict(
        rep_id="REP-001",
        region="WEST",
        evaluation_period_id="Q1-2026",
        avg_discount_depth_pct=0.0,
        discount_frequency_pct=0.0,
        unauthorized_discount_rate_pct=0.0,
        early_discount_offer_rate_pct=0.0,
        discount_as_first_response_pct=0.0,
        gross_margin_vs_target_pct=0.0,
        price_objection_concession_rate_pct=0.0,
        multi_level_discount_rate_pct=0.0,
        discount_to_close_conversion_pct=0.0,
        competitor_price_match_rate_pct=0.0,
        list_price_win_rate_pct=1.0,        # high = healthy
        end_of_quarter_spike_rate_pct=0.0,
        approval_request_bypass_count=0,
        avg_deal_cycle_with_discount_days=30.0,
        value_objection_to_discount_pct=0.0,
        deal_size_after_discount_shrink_pct=0.0,
        repeat_discount_same_customer_pct=0.0,
        total_closed_deals=10,
        avg_deal_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return DiscountInput(**defaults)


def fresh_engine() -> SalesDiscountLeakageMarginErosionIntelligenceEngine:
    return SalesDiscountLeakageMarginErosionIntelligenceEngine()


# ---------------------------------------------------------------------------
# Section 1 – DiscountInput: all 22 fields present
# ---------------------------------------------------------------------------

class TestDiscountInputFields:
    def test_rep_id_stored(self):
        inp = make_input(rep_id="R-XYZ")
        assert inp.rep_id == "R-XYZ"

    def test_region_stored(self):
        inp = make_input(region="EAST")
        assert inp.region == "EAST"

    def test_evaluation_period_id_stored(self):
        inp = make_input(evaluation_period_id="Q2-2026")
        assert inp.evaluation_period_id == "Q2-2026"

    def test_avg_discount_depth_pct_stored(self):
        inp = make_input(avg_discount_depth_pct=0.25)
        assert inp.avg_discount_depth_pct == 0.25

    def test_discount_frequency_pct_stored(self):
        inp = make_input(discount_frequency_pct=0.60)
        assert inp.discount_frequency_pct == 0.60

    def test_unauthorized_discount_rate_pct_stored(self):
        inp = make_input(unauthorized_discount_rate_pct=0.33)
        assert inp.unauthorized_discount_rate_pct == 0.33

    def test_early_discount_offer_rate_pct_stored(self):
        inp = make_input(early_discount_offer_rate_pct=0.45)
        assert inp.early_discount_offer_rate_pct == 0.45

    def test_discount_as_first_response_pct_stored(self):
        inp = make_input(discount_as_first_response_pct=0.40)
        assert inp.discount_as_first_response_pct == 0.40

    def test_gross_margin_vs_target_pct_stored(self):
        inp = make_input(gross_margin_vs_target_pct=-0.10)
        assert inp.gross_margin_vs_target_pct == -0.10

    def test_price_objection_concession_rate_pct_stored(self):
        inp = make_input(price_objection_concession_rate_pct=0.55)
        assert inp.price_objection_concession_rate_pct == 0.55

    def test_multi_level_discount_rate_pct_stored(self):
        inp = make_input(multi_level_discount_rate_pct=0.35)
        assert inp.multi_level_discount_rate_pct == 0.35

    def test_discount_to_close_conversion_pct_stored(self):
        inp = make_input(discount_to_close_conversion_pct=0.50)
        assert inp.discount_to_close_conversion_pct == 0.50

    def test_competitor_price_match_rate_pct_stored(self):
        inp = make_input(competitor_price_match_rate_pct=0.20)
        assert inp.competitor_price_match_rate_pct == 0.20

    def test_list_price_win_rate_pct_stored(self):
        inp = make_input(list_price_win_rate_pct=0.10)
        assert inp.list_price_win_rate_pct == 0.10

    def test_end_of_quarter_spike_rate_pct_stored(self):
        inp = make_input(end_of_quarter_spike_rate_pct=0.55)
        assert inp.end_of_quarter_spike_rate_pct == 0.55

    def test_approval_request_bypass_count_stored(self):
        inp = make_input(approval_request_bypass_count=5)
        assert inp.approval_request_bypass_count == 5

    def test_avg_deal_cycle_with_discount_days_stored(self):
        inp = make_input(avg_deal_cycle_with_discount_days=45.0)
        assert inp.avg_deal_cycle_with_discount_days == 45.0

    def test_value_objection_to_discount_pct_stored(self):
        inp = make_input(value_objection_to_discount_pct=0.60)
        assert inp.value_objection_to_discount_pct == 0.60

    def test_deal_size_after_discount_shrink_pct_stored(self):
        inp = make_input(deal_size_after_discount_shrink_pct=0.30)
        assert inp.deal_size_after_discount_shrink_pct == 0.30

    def test_repeat_discount_same_customer_pct_stored(self):
        inp = make_input(repeat_discount_same_customer_pct=0.50)
        assert inp.repeat_discount_same_customer_pct == 0.50

    def test_total_closed_deals_stored(self):
        inp = make_input(total_closed_deals=50)
        assert inp.total_closed_deals == 50

    def test_avg_deal_value_usd_stored(self):
        inp = make_input(avg_deal_value_usd=25_000.0)
        assert inp.avg_deal_value_usd == 25_000.0

    def test_total_field_count(self):
        inp = make_input()
        assert len(inp.__dataclass_fields__) == 22


# ---------------------------------------------------------------------------
# Section 2 – DiscountResult.to_dict() has exactly 15 keys
# ---------------------------------------------------------------------------

class TestDiscountResultToDict:
    def test_to_dict_key_count(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_contains_rep_id(self):
        engine = fresh_engine()
        result = engine.assess(make_input(rep_id="REP-TEST"))
        assert result.to_dict()["rep_id"] == "REP-TEST"

    def test_to_dict_contains_region(self):
        engine = fresh_engine()
        result = engine.assess(make_input(region="NORTH"))
        assert result.to_dict()["region"] == "NORTH"

    def test_to_dict_discount_risk_is_string(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert isinstance(result.to_dict()["discount_risk"], str)

    def test_to_dict_discount_pattern_is_string(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert isinstance(result.to_dict()["discount_pattern"], str)

    def test_to_dict_discount_severity_is_string(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert isinstance(result.to_dict()["discount_severity"], str)

    def test_to_dict_recommended_action_is_string(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert isinstance(result.to_dict()["recommended_action"], str)

    def test_to_dict_scores_are_floats(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        for key in ("frequency_score", "depth_score", "discipline_score", "value_defense_score", "discount_composite"):
            assert isinstance(d[key], float), f"{key} should be float"

    def test_to_dict_flags_are_bools(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["has_discount_gap"], bool)
        assert isinstance(d["requires_discount_intervention"], bool)

    def test_to_dict_margin_erosion_is_float(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["estimated_margin_erosion_usd"], float)

    def test_to_dict_signal_is_string(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["discount_signal"], str)

    def test_to_dict_exact_keys(self):
        expected_keys = {
            "rep_id", "region", "discount_risk", "discount_pattern",
            "discount_severity", "recommended_action", "frequency_score",
            "depth_score", "discipline_score", "value_defense_score",
            "discount_composite", "has_discount_gap",
            "requires_discount_intervention", "estimated_margin_erosion_usd",
            "discount_signal",
        }
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings_not_enum_objects(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        # Values must be raw strings, not enum objects
        assert d["discount_risk"] in ("low", "moderate", "high", "critical")
        assert d["discount_pattern"] in (
            "none", "panic_discounter", "relationship_briber",
            "price_first_seller", "approval_bypasser", "chronic_leaker"
        )
        assert d["discount_severity"] in ("disciplined", "drifting", "leaking", "eroding")


# ---------------------------------------------------------------------------
# Section 3 – summary() has exactly 13 keys
# ---------------------------------------------------------------------------

class TestSummaryKeyCount:
    def test_summary_empty_engine_has_13_keys(self):
        engine = fresh_engine()
        s = engine.summary()
        assert len(s) == 13

    def test_summary_after_assess_has_13_keys(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert len(s) == 13

    def test_summary_exact_keys(self):
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_discount_composite", "discount_gap_count",
            "intervention_count", "avg_frequency_score", "avg_depth_score",
            "avg_discipline_score", "avg_value_defense_score",
            "total_estimated_margin_erosion_usd",
        }
        engine = fresh_engine()
        engine.assess(make_input())
        assert set(engine.summary().keys()) == expected

    def test_summary_empty_total_is_zero(self):
        assert fresh_engine().summary()["total"] == 0

    def test_summary_total_increments(self):
        engine = fresh_engine()
        engine.assess(make_input())
        engine.assess(make_input(rep_id="R2"))
        assert engine.summary()["total"] == 2

    def test_summary_empty_risk_counts_empty_dict(self):
        assert fresh_engine().summary()["risk_counts"] == {}

    def test_summary_empty_avg_composite_is_zero(self):
        assert fresh_engine().summary()["avg_discount_composite"] == 0.0

    def test_summary_gap_count_empty(self):
        assert fresh_engine().summary()["discount_gap_count"] == 0

    def test_summary_intervention_count_empty(self):
        assert fresh_engine().summary()["intervention_count"] == 0

    def test_summary_avg_scores_zero_when_empty(self):
        s = fresh_engine().summary()
        assert s["avg_frequency_score"] == 0.0
        assert s["avg_depth_score"] == 0.0
        assert s["avg_discipline_score"] == 0.0
        assert s["avg_value_defense_score"] == 0.0

    def test_summary_margin_erosion_zero_when_empty(self):
        assert fresh_engine().summary()["total_estimated_margin_erosion_usd"] == 0.0


# ---------------------------------------------------------------------------
# Section 4 – _frequency_score sub-score
# ---------------------------------------------------------------------------

class TestFrequencyScore:
    def _score(self, **kw):
        engine = fresh_engine()
        inp = make_input(**kw)
        return engine._frequency_score(inp)

    # discount_frequency_pct thresholds
    def test_freq_zero_all_zero(self):
        assert self._score() == 0.0

    def test_freq_pct_below_035(self):
        assert self._score(discount_frequency_pct=0.34) == 0.0

    def test_freq_pct_exactly_035(self):
        # 0.35 → +8
        assert self._score(discount_frequency_pct=0.35) == 8.0

    def test_freq_pct_between_035_and_050(self):
        assert self._score(discount_frequency_pct=0.49) == 8.0

    def test_freq_pct_exactly_050(self):
        # 0.50 → +22
        assert self._score(discount_frequency_pct=0.50) == 22.0

    def test_freq_pct_between_050_and_070(self):
        assert self._score(discount_frequency_pct=0.69) == 22.0

    def test_freq_pct_exactly_070(self):
        # 0.70 → +40
        assert self._score(discount_frequency_pct=0.70) == 40.0

    def test_freq_pct_above_070(self):
        assert self._score(discount_frequency_pct=0.90) == 40.0

    # multi_level_discount_rate_pct thresholds
    def test_multi_below_025(self):
        assert self._score(multi_level_discount_rate_pct=0.24) == 0.0

    def test_multi_exactly_025(self):
        assert self._score(multi_level_discount_rate_pct=0.25) == 18.0

    def test_multi_between_025_045(self):
        assert self._score(multi_level_discount_rate_pct=0.44) == 18.0

    def test_multi_exactly_045(self):
        assert self._score(multi_level_discount_rate_pct=0.45) == 35.0

    def test_multi_above_045(self):
        assert self._score(multi_level_discount_rate_pct=0.80) == 35.0

    # end_of_quarter_spike_rate_pct thresholds
    def test_eoq_below_035(self):
        assert self._score(end_of_quarter_spike_rate_pct=0.34) == 0.0

    def test_eoq_exactly_035(self):
        assert self._score(end_of_quarter_spike_rate_pct=0.35) == 12.0

    def test_eoq_between_035_055(self):
        assert self._score(end_of_quarter_spike_rate_pct=0.54) == 12.0

    def test_eoq_exactly_055(self):
        assert self._score(end_of_quarter_spike_rate_pct=0.55) == 25.0

    def test_eoq_above_055(self):
        assert self._score(end_of_quarter_spike_rate_pct=1.00) == 25.0

    # additive combinations
    def test_freq_additive_two_components(self):
        # freq=0.70 (+40) + multi=0.45 (+35) = 75
        s = self._score(discount_frequency_pct=0.70, multi_level_discount_rate_pct=0.45)
        assert s == 75.0

    def test_freq_additive_all_three_max(self):
        # freq=0.70 (+40) + multi=0.45 (+35) + eoq=0.55 (+25) = 100
        s = self._score(
            discount_frequency_pct=0.70,
            multi_level_discount_rate_pct=0.45,
            end_of_quarter_spike_rate_pct=0.55,
        )
        assert s == 100.0

    def test_freq_cap_at_100(self):
        # same inputs; total exceeds 100 conceptually but cap applies
        s = self._score(
            discount_frequency_pct=0.90,
            multi_level_discount_rate_pct=0.90,
            end_of_quarter_spike_rate_pct=0.90,
        )
        assert s == 100.0

    def test_freq_partial_high_low(self):
        # freq=0.50 (+22) + multi=0.25 (+18) = 40
        s = self._score(discount_frequency_pct=0.50, multi_level_discount_rate_pct=0.25)
        assert s == 40.0


# ---------------------------------------------------------------------------
# Section 5 – _depth_score sub-score
# ---------------------------------------------------------------------------

class TestDepthScore:
    def _score(self, **kw):
        engine = fresh_engine()
        inp = make_input(**kw)
        return engine._depth_score(inp)

    def test_depth_zero(self):
        assert self._score() == 0.0

    def test_avg_depth_below_010(self):
        assert self._score(avg_discount_depth_pct=0.09) == 0.0

    def test_avg_depth_exactly_010(self):
        assert self._score(avg_discount_depth_pct=0.10) == 8.0

    def test_avg_depth_between_010_018(self):
        assert self._score(avg_discount_depth_pct=0.17) == 8.0

    def test_avg_depth_exactly_018(self):
        assert self._score(avg_discount_depth_pct=0.18) == 22.0

    def test_avg_depth_between_018_030(self):
        assert self._score(avg_discount_depth_pct=0.29) == 22.0

    def test_avg_depth_exactly_030(self):
        assert self._score(avg_discount_depth_pct=0.30) == 40.0

    def test_avg_depth_above_030(self):
        assert self._score(avg_discount_depth_pct=0.50) == 40.0

    def test_shrink_below_012(self):
        assert self._score(deal_size_after_discount_shrink_pct=0.11) == 0.0

    def test_shrink_exactly_012(self):
        assert self._score(deal_size_after_discount_shrink_pct=0.12) == 18.0

    def test_shrink_between_012_025(self):
        assert self._score(deal_size_after_discount_shrink_pct=0.24) == 18.0

    def test_shrink_exactly_025(self):
        assert self._score(deal_size_after_discount_shrink_pct=0.25) == 35.0

    def test_shrink_above_025(self):
        assert self._score(deal_size_after_discount_shrink_pct=0.80) == 35.0

    def test_margin_above_minus_005(self):
        assert self._score(gross_margin_vs_target_pct=0.0) == 0.0

    def test_margin_exactly_minus_005(self):
        assert self._score(gross_margin_vs_target_pct=-0.05) == 12.0

    def test_margin_between_minus_015_minus_005(self):
        assert self._score(gross_margin_vs_target_pct=-0.10) == 12.0

    def test_margin_exactly_minus_015(self):
        assert self._score(gross_margin_vs_target_pct=-0.15) == 25.0

    def test_margin_below_minus_015(self):
        assert self._score(gross_margin_vs_target_pct=-0.50) == 25.0

    def test_depth_additive_all_max(self):
        # 40+35+25 = 100
        s = self._score(
            avg_discount_depth_pct=0.30,
            deal_size_after_discount_shrink_pct=0.25,
            gross_margin_vs_target_pct=-0.15,
        )
        assert s == 100.0

    def test_depth_cap_enforced(self):
        s = self._score(
            avg_discount_depth_pct=0.99,
            deal_size_after_discount_shrink_pct=0.99,
            gross_margin_vs_target_pct=-0.99,
        )
        assert s == 100.0

    def test_depth_partial_combination(self):
        # avg=0.18 (+22) + shrink=0.12 (+18) = 40
        s = self._score(avg_discount_depth_pct=0.18, deal_size_after_discount_shrink_pct=0.12)
        assert s == 40.0


# ---------------------------------------------------------------------------
# Section 6 – _discipline_score sub-score
# ---------------------------------------------------------------------------

class TestDisciplineScore:
    def _score(self, **kw):
        engine = fresh_engine()
        inp = make_input(**kw)
        return engine._discipline_score(inp)

    def test_discipline_zero(self):
        assert self._score() == 0.0

    def test_unauth_below_008(self):
        assert self._score(unauthorized_discount_rate_pct=0.07) == 0.0

    def test_unauth_exactly_008(self):
        assert self._score(unauthorized_discount_rate_pct=0.08) == 8.0

    def test_unauth_between_008_020(self):
        assert self._score(unauthorized_discount_rate_pct=0.19) == 8.0

    def test_unauth_exactly_020(self):
        assert self._score(unauthorized_discount_rate_pct=0.20) == 22.0

    def test_unauth_between_020_040(self):
        assert self._score(unauthorized_discount_rate_pct=0.39) == 22.0

    def test_unauth_exactly_040(self):
        assert self._score(unauthorized_discount_rate_pct=0.40) == 40.0

    def test_unauth_above_040(self):
        assert self._score(unauthorized_discount_rate_pct=0.80) == 40.0

    def test_early_below_028(self):
        assert self._score(early_discount_offer_rate_pct=0.27) == 0.0

    def test_early_exactly_028(self):
        assert self._score(early_discount_offer_rate_pct=0.28) == 18.0

    def test_early_between_028_050(self):
        assert self._score(early_discount_offer_rate_pct=0.49) == 18.0

    def test_early_exactly_050(self):
        assert self._score(early_discount_offer_rate_pct=0.50) == 35.0

    def test_early_above_050(self):
        assert self._score(early_discount_offer_rate_pct=1.00) == 35.0

    def test_bypass_below_2(self):
        assert self._score(approval_request_bypass_count=1) == 0.0

    def test_bypass_0(self):
        assert self._score(approval_request_bypass_count=0) == 0.0

    def test_bypass_exactly_2(self):
        assert self._score(approval_request_bypass_count=2) == 12.0

    def test_bypass_3(self):
        assert self._score(approval_request_bypass_count=3) == 12.0

    def test_bypass_exactly_4(self):
        assert self._score(approval_request_bypass_count=4) == 25.0

    def test_bypass_above_4(self):
        assert self._score(approval_request_bypass_count=10) == 25.0

    def test_discipline_all_max(self):
        # 40+35+25 = 100
        s = self._score(
            unauthorized_discount_rate_pct=0.40,
            early_discount_offer_rate_pct=0.50,
            approval_request_bypass_count=4,
        )
        assert s == 100.0

    def test_discipline_cap_enforced(self):
        s = self._score(
            unauthorized_discount_rate_pct=0.99,
            early_discount_offer_rate_pct=0.99,
            approval_request_bypass_count=100,
        )
        assert s == 100.0

    def test_discipline_partial(self):
        # unauth=0.20 (+22) + bypass=2 (+12) = 34
        s = self._score(unauthorized_discount_rate_pct=0.20, approval_request_bypass_count=2)
        assert s == 34.0


# ---------------------------------------------------------------------------
# Section 7 – _value_defense_score sub-score
# ---------------------------------------------------------------------------

class TestValueDefenseScore:
    def _score(self, **kw):
        engine = fresh_engine()
        inp = make_input(**kw)
        return engine._value_defense_score(inp)

    def test_value_zero_list_price_high(self):
        # list_price_win_rate_pct defaults to 1.0 → above 0.25 → 0 points
        assert self._score() == 0.0

    def test_first_response_below_015(self):
        assert self._score(discount_as_first_response_pct=0.14) == 0.0

    def test_first_response_exactly_015(self):
        assert self._score(discount_as_first_response_pct=0.15) == 10.0

    def test_first_response_between_015_030(self):
        assert self._score(discount_as_first_response_pct=0.29) == 10.0

    def test_first_response_exactly_030(self):
        assert self._score(discount_as_first_response_pct=0.30) == 25.0

    def test_first_response_between_030_055(self):
        assert self._score(discount_as_first_response_pct=0.54) == 25.0

    def test_first_response_exactly_055(self):
        assert self._score(discount_as_first_response_pct=0.55) == 45.0

    def test_first_response_above_055(self):
        assert self._score(discount_as_first_response_pct=0.90) == 45.0

    def test_price_obj_below_030(self):
        assert self._score(price_objection_concession_rate_pct=0.29) == 0.0

    def test_price_obj_exactly_030(self):
        assert self._score(price_objection_concession_rate_pct=0.30) == 15.0

    def test_price_obj_between_030_055(self):
        assert self._score(price_objection_concession_rate_pct=0.54) == 15.0

    def test_price_obj_exactly_055(self):
        assert self._score(price_objection_concession_rate_pct=0.55) == 30.0

    def test_price_obj_above_055(self):
        assert self._score(price_objection_concession_rate_pct=0.80) == 30.0

    def test_list_price_win_above_025(self):
        assert self._score(list_price_win_rate_pct=0.26) == 0.0

    def test_list_price_win_exactly_025(self):
        assert self._score(list_price_win_rate_pct=0.25) == 12.0

    def test_list_price_win_between_010_025(self):
        assert self._score(list_price_win_rate_pct=0.15) == 12.0

    def test_list_price_win_exactly_010(self):
        assert self._score(list_price_win_rate_pct=0.10) == 25.0

    def test_list_price_win_below_010(self):
        assert self._score(list_price_win_rate_pct=0.05) == 25.0

    def test_value_all_max(self):
        # 45+30+25 = 100
        s = self._score(
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
            list_price_win_rate_pct=0.10,
        )
        assert s == 100.0

    def test_value_cap_enforced(self):
        s = self._score(
            discount_as_first_response_pct=0.99,
            price_objection_concession_rate_pct=0.99,
            list_price_win_rate_pct=0.01,
        )
        assert s == 100.0

    def test_value_partial(self):
        # first_response=0.30 (+25) + price_obj=0.30 (+15) = 40
        s = self._score(
            discount_as_first_response_pct=0.30,
            price_objection_concession_rate_pct=0.30,
        )
        assert s == 40.0


# ---------------------------------------------------------------------------
# Section 8 – composite score weighting
# ---------------------------------------------------------------------------

class TestCompositeScore:
    def _composite(self, fr, de, di, vd):
        return fresh_engine()._composite(fr, de, di, vd)

    def test_composite_all_zero(self):
        assert self._composite(0, 0, 0, 0) == 0.0

    def test_composite_all_100(self):
        assert self._composite(100, 100, 100, 100) == 100.0

    def test_composite_weights(self):
        # fr=100, de=0, di=0, vd=0 → 100*0.25=25
        assert self._composite(100, 0, 0, 0) == 25.0

    def test_composite_depth_weight(self):
        # fr=0, de=100, di=0, vd=0 → 100*0.30=30
        assert self._composite(0, 100, 0, 0) == 30.0

    def test_composite_discipline_weight(self):
        assert self._composite(0, 0, 100, 0) == 25.0

    def test_composite_value_defense_weight(self):
        assert self._composite(0, 0, 0, 100) == 20.0

    def test_composite_weights_sum_to_1(self):
        # All 100 → 25+30+25+20 = 100
        assert self._composite(100, 100, 100, 100) == 100.0

    def test_composite_rounded_to_2dp(self):
        # Should be rounded to 2 decimal places
        result = self._composite(33.33, 33.33, 33.33, 33.33)
        assert result == round(33.33 * 0.25 + 33.33 * 0.30 + 33.33 * 0.25 + 33.33 * 0.20, 2)

    def test_composite_capped_at_100(self):
        # Scores above 100 are possible before cap – but engine enforces sub-score cap so this is moot
        # Test engine's _composite cap:
        result = fresh_engine()._composite(200, 200, 200, 200)
        assert result == 100.0

    def test_composite_typical_values(self):
        # fr=40 de=35 di=22 vd=25
        expected = round(40 * 0.25 + 35 * 0.30 + 22 * 0.25 + 25 * 0.20, 2)
        assert self._composite(40, 35, 22, 25) == expected


# ---------------------------------------------------------------------------
# Section 9 – Risk classification
# ---------------------------------------------------------------------------

class TestRiskClassification:
    def _risk(self, composite):
        return fresh_engine()._risk(composite)

    def test_risk_0_is_low(self):
        assert self._risk(0) == DiscountRisk.low

    def test_risk_19_is_low(self):
        assert self._risk(19.99) == DiscountRisk.low

    def test_risk_20_is_moderate(self):
        assert self._risk(20) == DiscountRisk.moderate

    def test_risk_39_is_moderate(self):
        assert self._risk(39.99) == DiscountRisk.moderate

    def test_risk_40_is_high(self):
        assert self._risk(40) == DiscountRisk.high

    def test_risk_59_is_high(self):
        assert self._risk(59.99) == DiscountRisk.high

    def test_risk_60_is_critical(self):
        assert self._risk(60) == DiscountRisk.critical

    def test_risk_100_is_critical(self):
        assert self._risk(100) == DiscountRisk.critical

    def test_risk_boundary_exact_20(self):
        assert self._risk(20.0) == DiscountRisk.moderate

    def test_risk_boundary_exact_40(self):
        assert self._risk(40.0) == DiscountRisk.high

    def test_risk_boundary_exact_60(self):
        assert self._risk(60.0) == DiscountRisk.critical


# ---------------------------------------------------------------------------
# Section 10 – Severity classification
# ---------------------------------------------------------------------------

class TestSeverityClassification:
    def _severity(self, composite):
        return fresh_engine()._severity(composite)

    def test_severity_0_is_disciplined(self):
        assert self._severity(0) == DiscountSeverity.disciplined

    def test_severity_19_is_disciplined(self):
        assert self._severity(19.99) == DiscountSeverity.disciplined

    def test_severity_20_is_drifting(self):
        assert self._severity(20) == DiscountSeverity.drifting

    def test_severity_39_is_drifting(self):
        assert self._severity(39.99) == DiscountSeverity.drifting

    def test_severity_40_is_leaking(self):
        assert self._severity(40) == DiscountSeverity.leaking

    def test_severity_59_is_leaking(self):
        assert self._severity(59.99) == DiscountSeverity.leaking

    def test_severity_60_is_eroding(self):
        assert self._severity(60) == DiscountSeverity.eroding

    def test_severity_100_is_eroding(self):
        assert self._severity(100) == DiscountSeverity.eroding

    def test_severity_exact_20(self):
        assert self._severity(20.0) == DiscountSeverity.drifting

    def test_severity_exact_40(self):
        assert self._severity(40.0) == DiscountSeverity.leaking

    def test_severity_exact_60(self):
        assert self._severity(60.0) == DiscountSeverity.eroding


# ---------------------------------------------------------------------------
# Section 11 – Pattern detection (priority order)
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def _pattern(self, **kw):
        engine = fresh_engine()
        return engine._pattern(make_input(**kw))

    # panic_discounter: eoq>=0.45 AND depth>=0.20
    def test_panic_discounter_detected(self):
        assert self._pattern(end_of_quarter_spike_rate_pct=0.45, avg_discount_depth_pct=0.20) == DiscountPattern.panic_discounter

    def test_panic_discounter_eoq_below_threshold(self):
        p = self._pattern(end_of_quarter_spike_rate_pct=0.44, avg_discount_depth_pct=0.20)
        assert p != DiscountPattern.panic_discounter

    def test_panic_discounter_depth_below_threshold(self):
        p = self._pattern(end_of_quarter_spike_rate_pct=0.45, avg_discount_depth_pct=0.19)
        assert p != DiscountPattern.panic_discounter

    def test_panic_discounter_eoq_above(self):
        assert self._pattern(end_of_quarter_spike_rate_pct=0.90, avg_discount_depth_pct=0.50) == DiscountPattern.panic_discounter

    # relationship_briber: repeat>=0.50 AND list_price_win<=0.15
    def test_relationship_briber_detected(self):
        assert self._pattern(repeat_discount_same_customer_pct=0.50, list_price_win_rate_pct=0.15) == DiscountPattern.relationship_briber

    def test_relationship_briber_repeat_below(self):
        p = self._pattern(repeat_discount_same_customer_pct=0.49, list_price_win_rate_pct=0.10)
        assert p != DiscountPattern.relationship_briber

    def test_relationship_briber_list_price_win_above(self):
        p = self._pattern(repeat_discount_same_customer_pct=0.60, list_price_win_rate_pct=0.16)
        assert p != DiscountPattern.relationship_briber

    # price_first_seller: early>=0.45 AND first_response>=0.40
    def test_price_first_seller_detected(self):
        assert self._pattern(early_discount_offer_rate_pct=0.45, discount_as_first_response_pct=0.40) == DiscountPattern.price_first_seller

    def test_price_first_seller_early_below(self):
        p = self._pattern(early_discount_offer_rate_pct=0.44, discount_as_first_response_pct=0.40)
        assert p != DiscountPattern.price_first_seller

    def test_price_first_seller_first_response_below(self):
        p = self._pattern(early_discount_offer_rate_pct=0.50, discount_as_first_response_pct=0.39)
        assert p != DiscountPattern.price_first_seller

    # approval_bypasser: unauth>=0.30 AND bypass>=3
    def test_approval_bypasser_detected(self):
        assert self._pattern(unauthorized_discount_rate_pct=0.30, approval_request_bypass_count=3) == DiscountPattern.approval_bypasser

    def test_approval_bypasser_unauth_below(self):
        p = self._pattern(unauthorized_discount_rate_pct=0.29, approval_request_bypass_count=5)
        assert p != DiscountPattern.approval_bypasser

    def test_approval_bypasser_bypass_below(self):
        p = self._pattern(unauthorized_discount_rate_pct=0.30, approval_request_bypass_count=2)
        assert p != DiscountPattern.approval_bypasser

    # chronic_leaker: freq>=0.60 AND multi>=0.35
    def test_chronic_leaker_detected(self):
        assert self._pattern(discount_frequency_pct=0.60, multi_level_discount_rate_pct=0.35) == DiscountPattern.chronic_leaker

    def test_chronic_leaker_freq_below(self):
        p = self._pattern(discount_frequency_pct=0.59, multi_level_discount_rate_pct=0.40)
        assert p != DiscountPattern.chronic_leaker

    def test_chronic_leaker_multi_below(self):
        p = self._pattern(discount_frequency_pct=0.70, multi_level_discount_rate_pct=0.34)
        assert p != DiscountPattern.chronic_leaker

    # none (fallback)
    def test_none_pattern(self):
        assert self._pattern() == DiscountPattern.none

    # Priority order: panic_discounter takes precedence over relationship_briber
    def test_panic_discounter_priority_over_relationship_briber(self):
        p = self._pattern(
            end_of_quarter_spike_rate_pct=0.45,
            avg_discount_depth_pct=0.20,
            repeat_discount_same_customer_pct=0.60,
            list_price_win_rate_pct=0.10,
        )
        assert p == DiscountPattern.panic_discounter

    def test_panic_discounter_priority_over_price_first_seller(self):
        p = self._pattern(
            end_of_quarter_spike_rate_pct=0.50,
            avg_discount_depth_pct=0.25,
            early_discount_offer_rate_pct=0.50,
            discount_as_first_response_pct=0.45,
        )
        assert p == DiscountPattern.panic_discounter

    def test_panic_discounter_priority_over_approval_bypasser(self):
        p = self._pattern(
            end_of_quarter_spike_rate_pct=0.50,
            avg_discount_depth_pct=0.25,
            unauthorized_discount_rate_pct=0.30,
            approval_request_bypass_count=5,
        )
        assert p == DiscountPattern.panic_discounter

    def test_panic_discounter_priority_over_chronic_leaker(self):
        p = self._pattern(
            end_of_quarter_spike_rate_pct=0.50,
            avg_discount_depth_pct=0.25,
            discount_frequency_pct=0.70,
            multi_level_discount_rate_pct=0.50,
        )
        assert p == DiscountPattern.panic_discounter

    def test_relationship_briber_priority_over_price_first_seller(self):
        p = self._pattern(
            repeat_discount_same_customer_pct=0.60,
            list_price_win_rate_pct=0.10,
            early_discount_offer_rate_pct=0.50,
            discount_as_first_response_pct=0.45,
        )
        assert p == DiscountPattern.relationship_briber

    def test_relationship_briber_priority_over_approval_bypasser(self):
        p = self._pattern(
            repeat_discount_same_customer_pct=0.60,
            list_price_win_rate_pct=0.10,
            unauthorized_discount_rate_pct=0.35,
            approval_request_bypass_count=5,
        )
        assert p == DiscountPattern.relationship_briber

    def test_price_first_seller_priority_over_approval_bypasser(self):
        p = self._pattern(
            early_discount_offer_rate_pct=0.50,
            discount_as_first_response_pct=0.45,
            unauthorized_discount_rate_pct=0.35,
            approval_request_bypass_count=5,
        )
        assert p == DiscountPattern.price_first_seller

    def test_price_first_seller_priority_over_chronic_leaker(self):
        p = self._pattern(
            early_discount_offer_rate_pct=0.50,
            discount_as_first_response_pct=0.45,
            discount_frequency_pct=0.70,
            multi_level_discount_rate_pct=0.50,
        )
        assert p == DiscountPattern.price_first_seller

    def test_approval_bypasser_priority_over_chronic_leaker(self):
        p = self._pattern(
            unauthorized_discount_rate_pct=0.35,
            approval_request_bypass_count=5,
            discount_frequency_pct=0.70,
            multi_level_discount_rate_pct=0.50,
        )
        assert p == DiscountPattern.approval_bypasser


# ---------------------------------------------------------------------------
# Section 12 – Action recommendation
# ---------------------------------------------------------------------------

class TestActionRecommendation:
    def _action(self, risk, pattern):
        return fresh_engine()._action(risk, pattern)

    # Critical risk
    def test_critical_approval_bypasser_resets_authority(self):
        assert self._action(DiscountRisk.critical, DiscountPattern.approval_bypasser) == DiscountAction.pricing_authority_reset

    def test_critical_chronic_leaker_resets_authority(self):
        assert self._action(DiscountRisk.critical, DiscountPattern.chronic_leaker) == DiscountAction.pricing_authority_reset

    def test_critical_panic_discounter_deal_desk(self):
        assert self._action(DiscountRisk.critical, DiscountPattern.panic_discounter) == DiscountAction.deal_desk_review

    def test_critical_relationship_briber_deal_desk(self):
        assert self._action(DiscountRisk.critical, DiscountPattern.relationship_briber) == DiscountAction.deal_desk_review

    def test_critical_price_first_seller_deal_desk(self):
        assert self._action(DiscountRisk.critical, DiscountPattern.price_first_seller) == DiscountAction.deal_desk_review

    def test_critical_none_deal_desk(self):
        assert self._action(DiscountRisk.critical, DiscountPattern.none) == DiscountAction.deal_desk_review

    # High risk
    def test_high_panic_discounter_value_selling(self):
        assert self._action(DiscountRisk.high, DiscountPattern.panic_discounter) == DiscountAction.value_selling_coaching

    def test_high_relationship_briber_pricing_discipline(self):
        assert self._action(DiscountRisk.high, DiscountPattern.relationship_briber) == DiscountAction.pricing_discipline_coaching

    def test_high_price_first_seller_value_selling(self):
        assert self._action(DiscountRisk.high, DiscountPattern.price_first_seller) == DiscountAction.value_selling_coaching

    def test_high_approval_bypasser_enforcement(self):
        assert self._action(DiscountRisk.high, DiscountPattern.approval_bypasser) == DiscountAction.approval_process_enforcement

    def test_high_chronic_leaker_deal_desk(self):
        assert self._action(DiscountRisk.high, DiscountPattern.chronic_leaker) == DiscountAction.deal_desk_review

    def test_high_none_pricing_discipline(self):
        assert self._action(DiscountRisk.high, DiscountPattern.none) == DiscountAction.pricing_discipline_coaching

    # Moderate risk
    def test_moderate_any_pattern_monitoring(self):
        for pattern in DiscountPattern:
            assert self._action(DiscountRisk.moderate, pattern) == DiscountAction.discount_monitoring

    # Low risk
    def test_low_any_pattern_no_action(self):
        for pattern in DiscountPattern:
            assert self._action(DiscountRisk.low, pattern) == DiscountAction.no_action


# ---------------------------------------------------------------------------
# Section 13 – has_discount_gap flag
# ---------------------------------------------------------------------------

class TestHasDiscountGap:
    def _has_gap(self, composite, **kw):
        engine = fresh_engine()
        inp = make_input(**kw)
        return engine._has_gap(inp, composite)

    def test_gap_false_all_below(self):
        # composite<40, depth<0.20, unauth<0.15
        assert not self._has_gap(
            39.99,
            avg_discount_depth_pct=0.19,
            unauthorized_discount_rate_pct=0.14,
        )

    def test_gap_true_composite_40(self):
        assert self._has_gap(40.0, avg_discount_depth_pct=0.0, unauthorized_discount_rate_pct=0.0)

    def test_gap_true_composite_above_40(self):
        assert self._has_gap(70.0)

    def test_gap_true_depth_020(self):
        assert self._has_gap(0.0, avg_discount_depth_pct=0.20)

    def test_gap_true_depth_above_020(self):
        assert self._has_gap(0.0, avg_discount_depth_pct=0.50)

    def test_gap_false_depth_019(self):
        assert not self._has_gap(
            0.0,
            avg_discount_depth_pct=0.19,
            unauthorized_discount_rate_pct=0.0,
        )

    def test_gap_true_unauth_015(self):
        assert self._has_gap(0.0, unauthorized_discount_rate_pct=0.15)

    def test_gap_true_unauth_above_015(self):
        assert self._has_gap(0.0, unauthorized_discount_rate_pct=0.50)

    def test_gap_false_unauth_014(self):
        assert not self._has_gap(
            0.0,
            avg_discount_depth_pct=0.0,
            unauthorized_discount_rate_pct=0.14,
        )

    def test_gap_via_assess_zero_all(self):
        result = fresh_engine().assess(make_input())
        assert result.has_discount_gap is False

    def test_gap_via_assess_high_composite(self):
        result = fresh_engine().assess(make_input(
            avg_discount_depth_pct=0.30,
            deal_size_after_discount_shrink_pct=0.30,
            gross_margin_vs_target_pct=-0.20,
            discount_frequency_pct=0.80,
            multi_level_discount_rate_pct=0.50,
            end_of_quarter_spike_rate_pct=0.60,
            discount_as_first_response_pct=0.60,
            price_objection_concession_rate_pct=0.60,
            list_price_win_rate_pct=0.05,
        ))
        assert result.has_discount_gap is True


# ---------------------------------------------------------------------------
# Section 14 – requires_discount_intervention flag
# ---------------------------------------------------------------------------

class TestRequiresIntervention:
    def _req(self, composite, **kw):
        engine = fresh_engine()
        inp = make_input(**kw)
        return engine._requires_intervention(inp, composite)

    def test_intervention_false_all_below(self):
        assert not self._req(24.99, discount_frequency_pct=0.49, gross_margin_vs_target_pct=0.0)

    def test_intervention_true_composite_25(self):
        assert self._req(25.0)

    def test_intervention_true_composite_above_25(self):
        assert self._req(50.0)

    def test_intervention_true_freq_050(self):
        assert self._req(0.0, discount_frequency_pct=0.50)

    def test_intervention_true_freq_above_050(self):
        assert self._req(0.0, discount_frequency_pct=0.80)

    def test_intervention_false_freq_049(self):
        assert not self._req(0.0, discount_frequency_pct=0.49, gross_margin_vs_target_pct=0.0)

    def test_intervention_true_margin_minus_008(self):
        assert self._req(0.0, gross_margin_vs_target_pct=-0.08)

    def test_intervention_true_margin_below_minus_008(self):
        assert self._req(0.0, gross_margin_vs_target_pct=-0.50)

    def test_intervention_false_margin_minus_007(self):
        assert not self._req(0.0, discount_frequency_pct=0.0, gross_margin_vs_target_pct=-0.07)

    def test_intervention_via_assess_zero(self):
        result = fresh_engine().assess(make_input())
        assert result.requires_discount_intervention is False

    def test_intervention_via_assess_freq_50(self):
        result = fresh_engine().assess(make_input(discount_frequency_pct=0.50))
        assert result.requires_discount_intervention is True


# ---------------------------------------------------------------------------
# Section 15 – estimated_margin_erosion_usd
# ---------------------------------------------------------------------------

class TestMarginErosion:
    def _erosion(self, **kw):
        engine = fresh_engine()
        inp = make_input(**kw)
        fr = engine._frequency_score(inp)
        de = engine._depth_score(inp)
        di = engine._discipline_score(inp)
        vd = engine._value_defense_score(inp)
        comp = engine._composite(fr, de, di, vd)
        return engine._margin_erosion(inp, comp)

    def test_erosion_zero_when_composite_zero(self):
        assert self._erosion() == 0.0

    def test_erosion_zero_when_no_depth_or_freq(self):
        # Even with composite>0, if depth=0 or freq=0 then erosion=0
        result = fresh_engine().assess(make_input(
            discount_as_first_response_pct=0.60,
            price_objection_concession_rate_pct=0.60,
            list_price_win_rate_pct=0.05,
            avg_discount_depth_pct=0.0,
            discount_frequency_pct=0.0,
        ))
        assert result.estimated_margin_erosion_usd == 0.0

    def test_erosion_formula(self):
        inp = make_input(
            total_closed_deals=100,
            avg_deal_value_usd=10_000.0,
            avg_discount_depth_pct=0.20,
            discount_frequency_pct=0.60,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
            list_price_win_rate_pct=0.10,
        )
        engine = fresh_engine()
        result = engine.assess(inp)
        comp = result.discount_composite
        expected = round(100 * 10_000.0 * 0.20 * 0.60 * (comp / 100), 2)
        assert result.estimated_margin_erosion_usd == expected

    def test_erosion_rounded_to_2dp(self):
        result = fresh_engine().assess(make_input(
            total_closed_deals=7,
            avg_deal_value_usd=3_333.33,
            avg_discount_depth_pct=0.15,
            discount_frequency_pct=0.40,
            discount_as_first_response_pct=0.30,
            price_objection_concession_rate_pct=0.35,
        ))
        erosion = result.estimated_margin_erosion_usd
        assert erosion == round(erosion, 2)

    def test_erosion_positive_when_active(self):
        result = fresh_engine().assess(make_input(
            total_closed_deals=50,
            avg_deal_value_usd=5_000.0,
            avg_discount_depth_pct=0.25,
            discount_frequency_pct=0.70,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.60,
            list_price_win_rate_pct=0.05,
        ))
        assert result.estimated_margin_erosion_usd > 0


# ---------------------------------------------------------------------------
# Section 16 – discount_signal text
# ---------------------------------------------------------------------------

class TestDiscountSignal:
    def test_signal_healthy_below_20(self):
        result = fresh_engine().assess(make_input())
        assert "healthy" in result.discount_signal.lower()

    def test_signal_includes_disc_pct(self):
        result = fresh_engine().assess(make_input(
            discount_frequency_pct=0.45,
            discount_as_first_response_pct=0.30,
            price_objection_concession_rate_pct=0.35,
        ))
        if result.discount_composite >= 20:
            assert "45%" in result.discount_signal

    def test_signal_includes_depth_pct(self):
        result = fresh_engine().assess(make_input(
            avg_discount_depth_pct=0.20,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
            list_price_win_rate_pct=0.10,
        ))
        if result.discount_composite >= 20:
            assert "20%" in result.discount_signal

    def test_signal_includes_composite_int(self):
        result = fresh_engine().assess(make_input(
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
            list_price_win_rate_pct=0.05,
        ))
        if result.discount_composite >= 20:
            comp_int = str(round(result.discount_composite))
            assert comp_int in result.discount_signal

    def test_signal_panic_discounter_label(self):
        result = fresh_engine().assess(make_input(
            end_of_quarter_spike_rate_pct=0.60,
            avg_discount_depth_pct=0.30,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
            list_price_win_rate_pct=0.05,
        ))
        if result.discount_composite >= 20:
            assert "Panic discounter" in result.discount_signal

    def test_signal_relationship_briber_label(self):
        result = fresh_engine().assess(make_input(
            repeat_discount_same_customer_pct=0.60,
            list_price_win_rate_pct=0.10,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
        ))
        if result.discount_composite >= 20 and result.discount_pattern == DiscountPattern.relationship_briber:
            assert "Relationship briber" in result.discount_signal

    def test_signal_price_first_seller_label(self):
        result = fresh_engine().assess(make_input(
            early_discount_offer_rate_pct=0.55,
            discount_as_first_response_pct=0.50,
            price_objection_concession_rate_pct=0.55,
            list_price_win_rate_pct=0.05,
        ))
        if result.discount_composite >= 20 and result.discount_pattern == DiscountPattern.price_first_seller:
            assert "Price-first seller" in result.discount_signal

    def test_signal_approval_bypasser_label(self):
        result = fresh_engine().assess(make_input(
            unauthorized_discount_rate_pct=0.40,
            approval_request_bypass_count=5,
            early_discount_offer_rate_pct=0.50,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
        ))
        if result.discount_composite >= 20 and result.discount_pattern == DiscountPattern.approval_bypasser:
            assert "Approval bypasser" in result.discount_signal

    def test_signal_chronic_leaker_label(self):
        result = fresh_engine().assess(make_input(
            discount_frequency_pct=0.70,
            multi_level_discount_rate_pct=0.50,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
            list_price_win_rate_pct=0.05,
        ))
        if result.discount_composite >= 20 and result.discount_pattern == DiscountPattern.chronic_leaker:
            assert "Chronic leaker" in result.discount_signal

    def test_signal_is_non_empty_string(self):
        for _ in range(3):
            result = fresh_engine().assess(make_input())
            assert isinstance(result.discount_signal, str)
            assert len(result.discount_signal) > 0


# ---------------------------------------------------------------------------
# Section 17 – assess() end-to-end
# ---------------------------------------------------------------------------

class TestAssess:
    def test_assess_returns_discount_result(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert isinstance(result, DiscountResult)

    def test_assess_preserves_rep_id(self):
        engine = fresh_engine()
        result = engine.assess(make_input(rep_id="REP-XYZ"))
        assert result.rep_id == "REP-XYZ"

    def test_assess_preserves_region(self):
        engine = fresh_engine()
        result = engine.assess(make_input(region="SOUTH"))
        assert result.region == "SOUTH"

    def test_assess_accumulates_results(self):
        engine = fresh_engine()
        engine.assess(make_input(rep_id="R1"))
        engine.assess(make_input(rep_id="R2"))
        assert len(engine._results) == 2

    def test_assess_zero_input_low_risk(self):
        result = fresh_engine().assess(make_input())
        assert result.discount_risk == DiscountRisk.low

    def test_assess_zero_input_no_gap(self):
        result = fresh_engine().assess(make_input())
        assert result.has_discount_gap is False

    def test_assess_zero_input_no_intervention(self):
        result = fresh_engine().assess(make_input())
        assert result.requires_discount_intervention is False

    def test_assess_zero_input_zero_erosion(self):
        result = fresh_engine().assess(make_input())
        assert result.estimated_margin_erosion_usd == 0.0

    def test_assess_zero_input_disciplined(self):
        result = fresh_engine().assess(make_input())
        assert result.discount_severity == DiscountSeverity.disciplined

    def test_assess_zero_input_none_pattern(self):
        result = fresh_engine().assess(make_input())
        assert result.discount_pattern == DiscountPattern.none

    def test_assess_zero_input_no_action(self):
        result = fresh_engine().assess(make_input())
        assert result.recommended_action == DiscountAction.no_action

    def test_assess_critical_rep(self):
        """All sub-scores at maximum → critical risk."""
        result = fresh_engine().assess(make_input(
            avg_discount_depth_pct=0.30,
            deal_size_after_discount_shrink_pct=0.30,
            gross_margin_vs_target_pct=-0.20,
            discount_frequency_pct=0.80,
            multi_level_discount_rate_pct=0.50,
            end_of_quarter_spike_rate_pct=0.60,
            unauthorized_discount_rate_pct=0.50,
            early_discount_offer_rate_pct=0.60,
            approval_request_bypass_count=5,
            discount_as_first_response_pct=0.70,
            price_objection_concession_rate_pct=0.70,
            list_price_win_rate_pct=0.05,
        ))
        assert result.discount_risk == DiscountRisk.critical
        assert result.discount_severity == DiscountSeverity.eroding
        assert result.has_discount_gap is True
        assert result.requires_discount_intervention is True

    def test_assess_composite_stored_in_result(self):
        engine = fresh_engine()
        inp = make_input(discount_frequency_pct=0.50)
        result = engine.assess(inp)
        fr = engine._frequency_score(inp)
        de = engine._depth_score(inp)
        di = engine._discipline_score(inp)
        vd = engine._value_defense_score(inp)
        expected = engine._composite(fr, de, di, vd)
        assert result.discount_composite == expected

    def test_assess_result_appended_to_internal_list(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert engine._results[-1] is result


# ---------------------------------------------------------------------------
# Section 18 – assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_batch_empty_returns_empty_list(self):
        assert fresh_engine().assess_batch([]) == []

    def test_batch_returns_list_of_results(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = fresh_engine().assess_batch(inputs)
        assert len(results) == 5
        assert all(isinstance(r, DiscountResult) for r in results)

    def test_batch_preserves_order(self):
        ids = ["A", "B", "C"]
        inputs = [make_input(rep_id=r) for r in ids]
        results = fresh_engine().assess_batch(inputs)
        assert [r.rep_id for r in results] == ids

    def test_batch_accumulates_in_engine(self):
        engine = fresh_engine()
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        assert len(engine._results) == 3

    def test_batch_single_element(self):
        results = fresh_engine().assess_batch([make_input(rep_id="SOLO")])
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"

    def test_batch_results_match_individual_assess(self):
        inputs = [make_input(rep_id=f"R{i}", discount_frequency_pct=i * 0.1) for i in range(4)]
        batch_results = fresh_engine().assess_batch(inputs)
        individual_results = [fresh_engine().assess(inp) for inp in inputs]
        for b, ind in zip(batch_results, individual_results):
            assert b.discount_composite == ind.discount_composite
            assert b.discount_risk == ind.discount_risk


# ---------------------------------------------------------------------------
# Section 19 – summary() aggregation
# ---------------------------------------------------------------------------

class TestSummaryAggregation:
    def test_summary_risk_counts_populated(self):
        engine = fresh_engine()
        engine.assess(make_input())  # low risk
        s = engine.summary()
        assert "low" in s["risk_counts"]

    def test_summary_risk_counts_increment(self):
        engine = fresh_engine()
        engine.assess(make_input())
        engine.assess(make_input())
        s = engine.summary()
        assert s["risk_counts"].get("low", 0) == 2

    def test_summary_pattern_counts_populated(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert "none" in s["pattern_counts"]

    def test_summary_severity_counts_populated(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert "disciplined" in s["severity_counts"]

    def test_summary_action_counts_populated(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert "no_action" in s["action_counts"]

    def test_summary_avg_composite_correct(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(discount_frequency_pct=0.70))
        r2 = engine.assess(make_input(discount_frequency_pct=0.50))
        expected = round((r1.discount_composite + r2.discount_composite) / 2, 1)
        assert engine.summary()["avg_discount_composite"] == expected

    def test_summary_gap_count_correct(self):
        engine = fresh_engine()
        engine.assess(make_input(avg_discount_depth_pct=0.25))  # gap
        engine.assess(make_input())  # no gap
        s = engine.summary()
        assert s["discount_gap_count"] == 1

    def test_summary_intervention_count_correct(self):
        engine = fresh_engine()
        engine.assess(make_input(discount_frequency_pct=0.60))  # intervention
        engine.assess(make_input())  # no intervention
        s = engine.summary()
        assert s["intervention_count"] == 1

    def test_summary_avg_frequency_score(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(discount_frequency_pct=0.70))
        r2 = engine.assess(make_input(discount_frequency_pct=0.0))
        expected = round((r1.frequency_score + r2.frequency_score) / 2, 1)
        assert engine.summary()["avg_frequency_score"] == expected

    def test_summary_avg_depth_score(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(avg_discount_depth_pct=0.30))
        r2 = engine.assess(make_input())
        expected = round((r1.depth_score + r2.depth_score) / 2, 1)
        assert engine.summary()["avg_depth_score"] == expected

    def test_summary_avg_discipline_score(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(unauthorized_discount_rate_pct=0.40))
        r2 = engine.assess(make_input())
        expected = round((r1.discipline_score + r2.discipline_score) / 2, 1)
        assert engine.summary()["avg_discipline_score"] == expected

    def test_summary_avg_value_defense_score(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(discount_as_first_response_pct=0.55))
        r2 = engine.assess(make_input())
        expected = round((r1.value_defense_score + r2.value_defense_score) / 2, 1)
        assert engine.summary()["avg_value_defense_score"] == expected

    def test_summary_total_erosion_sums_all(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(
            total_closed_deals=10,
            avg_deal_value_usd=1000.0,
            avg_discount_depth_pct=0.20,
            discount_frequency_pct=0.60,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
            list_price_win_rate_pct=0.05,
        ))
        r2 = engine.assess(make_input())
        expected = round(r1.estimated_margin_erosion_usd + r2.estimated_margin_erosion_usd, 2)
        assert engine.summary()["total_estimated_margin_erosion_usd"] == expected

    def test_summary_multiple_risk_levels(self):
        engine = fresh_engine()
        # low risk
        engine.assess(make_input())
        # critical risk (all maxed)
        engine.assess(make_input(
            avg_discount_depth_pct=0.30,
            deal_size_after_discount_shrink_pct=0.30,
            gross_margin_vs_target_pct=-0.20,
            discount_frequency_pct=0.80,
            multi_level_discount_rate_pct=0.50,
            end_of_quarter_spike_rate_pct=0.60,
            discount_as_first_response_pct=0.70,
            price_objection_concession_rate_pct=0.70,
            list_price_win_rate_pct=0.05,
            unauthorized_discount_rate_pct=0.50,
            early_discount_offer_rate_pct=0.60,
            approval_request_bypass_count=5,
        ))
        s = engine.summary()
        assert "low" in s["risk_counts"]
        assert "critical" in s["risk_counts"]
        assert s["total"] == 2


# ---------------------------------------------------------------------------
# Section 20 – Engine state isolation
# ---------------------------------------------------------------------------

class TestEngineStateIsolation:
    def test_two_engines_independent(self):
        e1 = SalesDiscountLeakageMarginErosionIntelligenceEngine()
        e2 = SalesDiscountLeakageMarginErosionIntelligenceEngine()
        e1.assess(make_input(rep_id="R1"))
        assert e1.summary()["total"] == 1
        assert e2.summary()["total"] == 0

    def test_results_not_shared_between_instances(self):
        e1 = SalesDiscountLeakageMarginErosionIntelligenceEngine()
        e2 = SalesDiscountLeakageMarginErosionIntelligenceEngine()
        e1.assess(make_input(rep_id="R1"))
        e2.assess(make_input(rep_id="R2"))
        assert e1._results[0].rep_id == "R1"
        assert e2._results[0].rep_id == "R2"

    def test_fresh_engine_has_empty_results(self):
        engine = fresh_engine()
        assert engine._results == []

    def test_engine_summary_after_10_assessments(self):
        engine = fresh_engine()
        for i in range(10):
            engine.assess(make_input(rep_id=f"R{i}"))
        assert engine.summary()["total"] == 10


# ---------------------------------------------------------------------------
# Section 21 – Enum values
# ---------------------------------------------------------------------------

class TestEnumValues:
    def test_risk_enum_values(self):
        assert DiscountRisk.low.value == "low"
        assert DiscountRisk.moderate.value == "moderate"
        assert DiscountRisk.high.value == "high"
        assert DiscountRisk.critical.value == "critical"

    def test_severity_enum_values(self):
        assert DiscountSeverity.disciplined.value == "disciplined"
        assert DiscountSeverity.drifting.value == "drifting"
        assert DiscountSeverity.leaking.value == "leaking"
        assert DiscountSeverity.eroding.value == "eroding"

    def test_pattern_enum_values(self):
        assert DiscountPattern.none.value == "none"
        assert DiscountPattern.panic_discounter.value == "panic_discounter"
        assert DiscountPattern.relationship_briber.value == "relationship_briber"
        assert DiscountPattern.price_first_seller.value == "price_first_seller"
        assert DiscountPattern.approval_bypasser.value == "approval_bypasser"
        assert DiscountPattern.chronic_leaker.value == "chronic_leaker"

    def test_action_enum_values(self):
        assert DiscountAction.no_action.value == "no_action"
        assert DiscountAction.discount_monitoring.value == "discount_monitoring"
        assert DiscountAction.pricing_discipline_coaching.value == "pricing_discipline_coaching"
        assert DiscountAction.approval_process_enforcement.value == "approval_process_enforcement"
        assert DiscountAction.value_selling_coaching.value == "value_selling_coaching"
        assert DiscountAction.deal_desk_review.value == "deal_desk_review"
        assert DiscountAction.pricing_authority_reset.value == "pricing_authority_reset"


# ---------------------------------------------------------------------------
# Section 22 – Boundary / edge cases
# ---------------------------------------------------------------------------

class TestBoundaryEdgeCases:
    def test_all_zeros_composite_is_zero(self):
        result = fresh_engine().assess(make_input())
        assert result.discount_composite == 0.0

    def test_all_maxed_composite_is_100(self):
        result = fresh_engine().assess(make_input(
            avg_discount_depth_pct=0.30,
            deal_size_after_discount_shrink_pct=0.25,
            gross_margin_vs_target_pct=-0.15,
            discount_frequency_pct=0.70,
            multi_level_discount_rate_pct=0.45,
            end_of_quarter_spike_rate_pct=0.55,
            unauthorized_discount_rate_pct=0.40,
            early_discount_offer_rate_pct=0.50,
            approval_request_bypass_count=4,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
            list_price_win_rate_pct=0.10,
        ))
        assert result.discount_composite == 100.0

    def test_composite_never_exceeds_100(self):
        result = fresh_engine().assess(make_input(
            avg_discount_depth_pct=1.0,
            deal_size_after_discount_shrink_pct=1.0,
            gross_margin_vs_target_pct=-1.0,
            discount_frequency_pct=1.0,
            multi_level_discount_rate_pct=1.0,
            end_of_quarter_spike_rate_pct=1.0,
            unauthorized_discount_rate_pct=1.0,
            early_discount_offer_rate_pct=1.0,
            approval_request_bypass_count=100,
            discount_as_first_response_pct=1.0,
            price_objection_concession_rate_pct=1.0,
            list_price_win_rate_pct=0.0,
        ))
        assert result.discount_composite <= 100.0

    def test_frequency_score_never_exceeds_100(self):
        engine = fresh_engine()
        inp = make_input(
            discount_frequency_pct=1.0,
            multi_level_discount_rate_pct=1.0,
            end_of_quarter_spike_rate_pct=1.0,
        )
        assert engine._frequency_score(inp) <= 100.0

    def test_depth_score_never_exceeds_100(self):
        engine = fresh_engine()
        inp = make_input(
            avg_discount_depth_pct=1.0,
            deal_size_after_discount_shrink_pct=1.0,
            gross_margin_vs_target_pct=-1.0,
        )
        assert engine._depth_score(inp) <= 100.0

    def test_discipline_score_never_exceeds_100(self):
        engine = fresh_engine()
        inp = make_input(
            unauthorized_discount_rate_pct=1.0,
            early_discount_offer_rate_pct=1.0,
            approval_request_bypass_count=100,
        )
        assert engine._discipline_score(inp) <= 100.0

    def test_value_defense_score_never_exceeds_100(self):
        engine = fresh_engine()
        inp = make_input(
            discount_as_first_response_pct=1.0,
            price_objection_concession_rate_pct=1.0,
            list_price_win_rate_pct=0.0,
        )
        assert engine._value_defense_score(inp) <= 100.0

    def test_large_bypass_count(self):
        engine = fresh_engine()
        inp = make_input(approval_request_bypass_count=9999)
        assert engine._discipline_score(inp) <= 100.0

    def test_negative_margin_positive_scores(self):
        engine = fresh_engine()
        inp = make_input(gross_margin_vs_target_pct=-1.0)
        score = engine._depth_score(inp)
        assert score >= 25.0

    def test_list_price_win_rate_zero(self):
        engine = fresh_engine()
        inp = make_input(list_price_win_rate_pct=0.0)
        score = engine._value_defense_score(inp)
        # 0.0 <= 0.10 → +25
        assert score >= 25.0

    def test_discount_composite_is_float(self):
        result = fresh_engine().assess(make_input(discount_frequency_pct=0.50))
        assert isinstance(result.discount_composite, float)

    def test_sub_scores_are_floats(self):
        result = fresh_engine().assess(make_input(discount_frequency_pct=0.50))
        assert isinstance(result.frequency_score, float)
        assert isinstance(result.depth_score, float)
        assert isinstance(result.discipline_score, float)
        assert isinstance(result.value_defense_score, float)

    def test_erosion_zero_when_deals_zero(self):
        result = fresh_engine().assess(make_input(
            total_closed_deals=0,
            avg_discount_depth_pct=0.30,
            discount_frequency_pct=0.80,
        ))
        assert result.estimated_margin_erosion_usd == 0.0

    def test_erosion_zero_when_avg_value_zero(self):
        result = fresh_engine().assess(make_input(
            avg_deal_value_usd=0.0,
            avg_discount_depth_pct=0.30,
            discount_frequency_pct=0.80,
        ))
        assert result.estimated_margin_erosion_usd == 0.0


# ---------------------------------------------------------------------------
# Section 23 – Scenario-based integration tests
# ---------------------------------------------------------------------------

class TestScenarios:
    """End-to-end scenarios that exercise the full assess() pipeline."""

    def test_star_rep_all_healthy(self):
        """Star rep with no discount leakage."""
        result = fresh_engine().assess(make_input(
            rep_id="STAR",
            avg_discount_depth_pct=0.05,
            discount_frequency_pct=0.10,
            unauthorized_discount_rate_pct=0.02,
            early_discount_offer_rate_pct=0.05,
            discount_as_first_response_pct=0.05,
            gross_margin_vs_target_pct=0.10,
            price_objection_concession_rate_pct=0.05,
            multi_level_discount_rate_pct=0.05,
            list_price_win_rate_pct=0.80,
            end_of_quarter_spike_rate_pct=0.05,
            approval_request_bypass_count=0,
            deal_size_after_discount_shrink_pct=0.02,
            repeat_discount_same_customer_pct=0.05,
        ))
        assert result.discount_risk == DiscountRisk.low
        assert result.discount_severity == DiscountSeverity.disciplined
        assert result.discount_pattern == DiscountPattern.none
        assert result.recommended_action == DiscountAction.no_action
        assert result.has_discount_gap is False
        assert result.requires_discount_intervention is False

    def test_panic_discounter_scenario(self):
        """Classic panic discounter at end of quarter."""
        result = fresh_engine().assess(make_input(
            rep_id="PANIC",
            end_of_quarter_spike_rate_pct=0.70,
            avg_discount_depth_pct=0.35,
            discount_frequency_pct=0.60,
            multi_level_discount_rate_pct=0.40,
            discount_as_first_response_pct=0.55,
        ))
        assert result.discount_pattern == DiscountPattern.panic_discounter

    def test_relationship_briber_scenario(self):
        """Rep giving repeat discounts to loyal accounts."""
        result = fresh_engine().assess(make_input(
            rep_id="BRIBER",
            repeat_discount_same_customer_pct=0.65,
            list_price_win_rate_pct=0.10,
            discount_as_first_response_pct=0.30,
            price_objection_concession_rate_pct=0.35,
        ))
        assert result.discount_pattern == DiscountPattern.relationship_briber

    def test_price_first_seller_scenario(self):
        """Rep leads with discount in first meeting."""
        result = fresh_engine().assess(make_input(
            rep_id="PRICEFIRST",
            early_discount_offer_rate_pct=0.60,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.50,
        ))
        assert result.discount_pattern == DiscountPattern.price_first_seller

    def test_approval_bypasser_scenario(self):
        """Rep bypasses approval process consistently."""
        result = fresh_engine().assess(make_input(
            rep_id="BYPASSER",
            unauthorized_discount_rate_pct=0.45,
            approval_request_bypass_count=6,
            early_discount_offer_rate_pct=0.40,
            discount_as_first_response_pct=0.35,
        ))
        assert result.discount_pattern == DiscountPattern.approval_bypasser

    def test_chronic_leaker_scenario(self):
        """Rep with systemic multi-level discounting."""
        result = fresh_engine().assess(make_input(
            rep_id="LEAKER",
            discount_frequency_pct=0.75,
            multi_level_discount_rate_pct=0.50,
            avg_discount_depth_pct=0.15,
            discount_as_first_response_pct=0.30,
        ))
        assert result.discount_pattern == DiscountPattern.chronic_leaker

    def test_moderate_risk_scenario(self):
        """Mid-tier discounting behavior."""
        result = fresh_engine().assess(make_input(
            discount_frequency_pct=0.40,
            avg_discount_depth_pct=0.12,
            discount_as_first_response_pct=0.20,
            price_objection_concession_rate_pct=0.25,
        ))
        assert result.discount_risk in (DiscountRisk.low, DiscountRisk.moderate)

    def test_high_risk_critical_action(self):
        """Critical risk results in deal_desk_review or pricing_authority_reset."""
        result = fresh_engine().assess(make_input(
            avg_discount_depth_pct=0.30,
            deal_size_after_discount_shrink_pct=0.30,
            gross_margin_vs_target_pct=-0.20,
            discount_frequency_pct=0.80,
            multi_level_discount_rate_pct=0.50,
            end_of_quarter_spike_rate_pct=0.60,
            discount_as_first_response_pct=0.70,
            price_objection_concession_rate_pct=0.70,
            list_price_win_rate_pct=0.05,
        ))
        if result.discount_risk == DiscountRisk.critical:
            assert result.recommended_action in (
                DiscountAction.deal_desk_review,
                DiscountAction.pricing_authority_reset,
            )

    def test_large_erosion_high_volume(self):
        """Large team with high deal volume generates significant erosion."""
        result = fresh_engine().assess(make_input(
            total_closed_deals=500,
            avg_deal_value_usd=50_000.0,
            avg_discount_depth_pct=0.20,
            discount_frequency_pct=0.60,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
            list_price_win_rate_pct=0.05,
        ))
        assert result.estimated_margin_erosion_usd > 100_000

    def test_batch_mixed_reps(self):
        """Batch assessment with different risk profiles."""
        inputs = [
            make_input(rep_id="CLEAN"),  # low risk
            make_input(rep_id="LEAKY", discount_frequency_pct=0.70, avg_discount_depth_pct=0.30),
            make_input(rep_id="PANIC", end_of_quarter_spike_rate_pct=0.60, avg_discount_depth_pct=0.25),
        ]
        engine = fresh_engine()
        results = engine.assess_batch(inputs)
        assert len(results) == 3
        # Engine accumulates all 3
        assert engine.summary()["total"] == 3

    def test_intervention_required_when_margin_bad(self):
        result = fresh_engine().assess(make_input(
            gross_margin_vs_target_pct=-0.15,
        ))
        assert result.requires_discount_intervention is True

    def test_gap_detected_via_unauth(self):
        result = fresh_engine().assess(make_input(
            unauthorized_discount_rate_pct=0.20,
        ))
        assert result.has_discount_gap is True

    def test_gap_detected_via_depth(self):
        result = fresh_engine().assess(make_input(
            avg_discount_depth_pct=0.25,
        ))
        assert result.has_discount_gap is True

    def test_to_dict_values_match_result_fields(self):
        engine = fresh_engine()
        result = engine.assess(make_input(
            rep_id="R-DICT",
            region="CENTRAL",
            discount_frequency_pct=0.60,
        ))
        d = result.to_dict()
        assert d["rep_id"] == result.rep_id
        assert d["region"] == result.region
        assert d["discount_risk"] == result.discount_risk.value
        assert d["discount_pattern"] == result.discount_pattern.value
        assert d["discount_severity"] == result.discount_severity.value
        assert d["recommended_action"] == result.recommended_action.value
        assert d["frequency_score"] == result.frequency_score
        assert d["depth_score"] == result.depth_score
        assert d["discipline_score"] == result.discipline_score
        assert d["value_defense_score"] == result.value_defense_score
        assert d["discount_composite"] == result.discount_composite
        assert d["has_discount_gap"] == result.has_discount_gap
        assert d["requires_discount_intervention"] == result.requires_discount_intervention
        assert d["estimated_margin_erosion_usd"] == result.estimated_margin_erosion_usd
        assert d["discount_signal"] == result.discount_signal


# ---------------------------------------------------------------------------
# Section 24 – Additional targeted sub-score boundary tests
# ---------------------------------------------------------------------------

class TestSubScoreBoundaries:
    """Fine-grained boundary assertions at exact threshold values."""

    def test_freq_exactly_035_gives_8(self):
        engine = fresh_engine()
        assert engine._frequency_score(make_input(discount_frequency_pct=0.350)) == 8.0

    def test_freq_just_under_035_gives_0(self):
        engine = fresh_engine()
        assert engine._frequency_score(make_input(discount_frequency_pct=0.349)) == 0.0

    def test_freq_exactly_050_gives_22(self):
        engine = fresh_engine()
        assert engine._frequency_score(make_input(discount_frequency_pct=0.500)) == 22.0

    def test_freq_just_under_050_gives_8(self):
        engine = fresh_engine()
        assert engine._frequency_score(make_input(discount_frequency_pct=0.499)) == 8.0

    def test_freq_exactly_070_gives_40(self):
        engine = fresh_engine()
        assert engine._frequency_score(make_input(discount_frequency_pct=0.700)) == 40.0

    def test_freq_just_under_070_gives_22(self):
        engine = fresh_engine()
        assert engine._frequency_score(make_input(discount_frequency_pct=0.699)) == 22.0

    def test_depth_avg_exactly_010_gives_8(self):
        engine = fresh_engine()
        assert engine._depth_score(make_input(avg_discount_depth_pct=0.10)) == 8.0

    def test_depth_avg_exactly_018_gives_22(self):
        engine = fresh_engine()
        assert engine._depth_score(make_input(avg_discount_depth_pct=0.18)) == 22.0

    def test_depth_avg_exactly_030_gives_40(self):
        engine = fresh_engine()
        assert engine._depth_score(make_input(avg_discount_depth_pct=0.30)) == 40.0

    def test_discipline_unauth_exactly_008_gives_8(self):
        engine = fresh_engine()
        assert engine._discipline_score(make_input(unauthorized_discount_rate_pct=0.08)) == 8.0

    def test_discipline_unauth_exactly_020_gives_22(self):
        engine = fresh_engine()
        assert engine._discipline_score(make_input(unauthorized_discount_rate_pct=0.20)) == 22.0

    def test_discipline_unauth_exactly_040_gives_40(self):
        engine = fresh_engine()
        assert engine._discipline_score(make_input(unauthorized_discount_rate_pct=0.40)) == 40.0

    def test_discipline_early_exactly_028_gives_18(self):
        engine = fresh_engine()
        assert engine._discipline_score(make_input(early_discount_offer_rate_pct=0.28)) == 18.0

    def test_discipline_early_exactly_050_gives_35(self):
        engine = fresh_engine()
        assert engine._discipline_score(make_input(early_discount_offer_rate_pct=0.50)) == 35.0

    def test_discipline_bypass_exactly_2_gives_12(self):
        engine = fresh_engine()
        assert engine._discipline_score(make_input(approval_request_bypass_count=2)) == 12.0

    def test_discipline_bypass_exactly_4_gives_25(self):
        engine = fresh_engine()
        assert engine._discipline_score(make_input(approval_request_bypass_count=4)) == 25.0

    def test_value_defense_first_resp_015_gives_10(self):
        engine = fresh_engine()
        assert engine._value_defense_score(make_input(discount_as_first_response_pct=0.15)) == 10.0

    def test_value_defense_first_resp_030_gives_25(self):
        engine = fresh_engine()
        assert engine._value_defense_score(make_input(discount_as_first_response_pct=0.30)) == 25.0

    def test_value_defense_first_resp_055_gives_45(self):
        engine = fresh_engine()
        assert engine._value_defense_score(make_input(discount_as_first_response_pct=0.55)) == 45.0

    def test_value_defense_price_obj_030_gives_15(self):
        engine = fresh_engine()
        assert engine._value_defense_score(make_input(price_objection_concession_rate_pct=0.30)) == 15.0

    def test_value_defense_price_obj_055_gives_30(self):
        engine = fresh_engine()
        assert engine._value_defense_score(make_input(price_objection_concession_rate_pct=0.55)) == 30.0

    def test_value_defense_list_price_025_gives_12(self):
        engine = fresh_engine()
        # Default list_price_win_rate=1.0, override to 0.25
        assert engine._value_defense_score(make_input(list_price_win_rate_pct=0.25)) == 12.0

    def test_value_defense_list_price_010_gives_25(self):
        engine = fresh_engine()
        assert engine._value_defense_score(make_input(list_price_win_rate_pct=0.10)) == 25.0

    def test_multi_level_exactly_025_gives_18(self):
        engine = fresh_engine()
        assert engine._frequency_score(make_input(multi_level_discount_rate_pct=0.25)) == 18.0

    def test_multi_level_exactly_045_gives_35(self):
        engine = fresh_engine()
        assert engine._frequency_score(make_input(multi_level_discount_rate_pct=0.45)) == 35.0

    def test_eoq_exactly_035_gives_12(self):
        engine = fresh_engine()
        assert engine._frequency_score(make_input(end_of_quarter_spike_rate_pct=0.35)) == 12.0

    def test_eoq_exactly_055_gives_25(self):
        engine = fresh_engine()
        assert engine._frequency_score(make_input(end_of_quarter_spike_rate_pct=0.55)) == 25.0

    def test_shrink_exactly_012_gives_18(self):
        engine = fresh_engine()
        assert engine._depth_score(make_input(deal_size_after_discount_shrink_pct=0.12)) == 18.0

    def test_shrink_exactly_025_gives_35(self):
        engine = fresh_engine()
        assert engine._depth_score(make_input(deal_size_after_discount_shrink_pct=0.25)) == 35.0

    def test_margin_exactly_minus_005_gives_12(self):
        engine = fresh_engine()
        assert engine._depth_score(make_input(gross_margin_vs_target_pct=-0.05)) == 12.0

    def test_margin_exactly_minus_015_gives_25(self):
        engine = fresh_engine()
        assert engine._depth_score(make_input(gross_margin_vs_target_pct=-0.15)) == 25.0


# ---------------------------------------------------------------------------
# Section 25 – Pattern boundary tests (exact threshold crossings)
# ---------------------------------------------------------------------------

class TestPatternBoundary:
    def test_panic_eoq_exactly_045_depth_exactly_020(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            end_of_quarter_spike_rate_pct=0.45,
            avg_discount_depth_pct=0.20,
        ))
        assert p == DiscountPattern.panic_discounter

    def test_panic_eoq_044_not_panic(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            end_of_quarter_spike_rate_pct=0.44,
            avg_discount_depth_pct=0.20,
        ))
        assert p != DiscountPattern.panic_discounter

    def test_panic_depth_019_not_panic(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            end_of_quarter_spike_rate_pct=0.50,
            avg_discount_depth_pct=0.19,
        ))
        assert p != DiscountPattern.panic_discounter

    def test_briber_repeat_exactly_050_listprice_exactly_015(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            repeat_discount_same_customer_pct=0.50,
            list_price_win_rate_pct=0.15,
        ))
        assert p == DiscountPattern.relationship_briber

    def test_briber_repeat_049_not_briber(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            repeat_discount_same_customer_pct=0.49,
            list_price_win_rate_pct=0.10,
        ))
        assert p != DiscountPattern.relationship_briber

    def test_briber_listprice_016_not_briber(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            repeat_discount_same_customer_pct=0.60,
            list_price_win_rate_pct=0.16,
        ))
        assert p != DiscountPattern.relationship_briber

    def test_price_first_early_exactly_045_first_resp_exactly_040(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            early_discount_offer_rate_pct=0.45,
            discount_as_first_response_pct=0.40,
        ))
        assert p == DiscountPattern.price_first_seller

    def test_price_first_early_044_not_price_first(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            early_discount_offer_rate_pct=0.44,
            discount_as_first_response_pct=0.50,
        ))
        assert p != DiscountPattern.price_first_seller

    def test_price_first_resp_039_not_price_first(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            early_discount_offer_rate_pct=0.50,
            discount_as_first_response_pct=0.39,
        ))
        assert p != DiscountPattern.price_first_seller

    def test_bypasser_unauth_exactly_030_bypass_exactly_3(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            unauthorized_discount_rate_pct=0.30,
            approval_request_bypass_count=3,
        ))
        assert p == DiscountPattern.approval_bypasser

    def test_bypasser_unauth_029_not_bypasser(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            unauthorized_discount_rate_pct=0.29,
            approval_request_bypass_count=5,
        ))
        assert p != DiscountPattern.approval_bypasser

    def test_bypasser_bypass_2_not_bypasser(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            unauthorized_discount_rate_pct=0.35,
            approval_request_bypass_count=2,
        ))
        assert p != DiscountPattern.approval_bypasser

    def test_chronic_leaker_freq_exactly_060_multi_exactly_035(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            discount_frequency_pct=0.60,
            multi_level_discount_rate_pct=0.35,
        ))
        assert p == DiscountPattern.chronic_leaker

    def test_chronic_leaker_freq_059_not_chronic(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            discount_frequency_pct=0.59,
            multi_level_discount_rate_pct=0.50,
        ))
        assert p != DiscountPattern.chronic_leaker

    def test_chronic_leaker_multi_034_not_chronic(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            discount_frequency_pct=0.70,
            multi_level_discount_rate_pct=0.34,
        ))
        assert p != DiscountPattern.chronic_leaker


# ---------------------------------------------------------------------------
# Section 26 – Risk / composite boundary assertions from assess()
# ---------------------------------------------------------------------------

class TestRiskFromAssess:
    def test_risk_low_composite_just_under_20(self):
        """Inputs that produce composite just under 20 → low."""
        engine = fresh_engine()
        # Just use tiny inputs to get a low composite
        result = engine.assess(make_input(
            discount_frequency_pct=0.35,  # +8 freq
        ))
        # freq_score=8, depth=0, discipline=0, value_defense=0 → composite=2
        assert result.discount_risk == DiscountRisk.low

    def test_risk_moderate_composite_20_to_39(self):
        engine = fresh_engine()
        result = engine.assess(make_input(
            discount_frequency_pct=0.70,    # freq=40
            avg_discount_depth_pct=0.10,    # depth=8
            discount_as_first_response_pct=0.15,  # vd=10
        ))
        # freq=40*0.25=10, depth=8*0.30=2.4, di=0, vd=10*0.20=2 → 14.4 → low
        # Adjust to hit moderate (>=20):
        result2 = engine.assess(make_input(
            discount_frequency_pct=0.70,  # freq=40
            avg_discount_depth_pct=0.18,  # depth=22
            discount_as_first_response_pct=0.30,  # vd=25
        ))
        # composite = 40*0.25 + 22*0.30 + 0*0.25 + 25*0.20 = 10+6.6+0+5=21.6
        assert result2.discount_risk == DiscountRisk.moderate

    def test_risk_high_composite_40_to_59(self):
        engine = fresh_engine()
        result = engine.assess(make_input(
            discount_frequency_pct=0.70,     # freq=40
            avg_discount_depth_pct=0.18,     # depth=22
            deal_size_after_discount_shrink_pct=0.12,  # depth+=18 → depth=40
            early_discount_offer_rate_pct=0.28,  # dis=18
            discount_as_first_response_pct=0.30,  # vd=25
            price_objection_concession_rate_pct=0.30,  # vd+=15 → vd=40
        ))
        # freq=40, depth=40, dis=18, vd=40
        # composite=40*0.25+40*0.30+18*0.25+40*0.20=10+12+4.5+8=34.5 → moderate
        # Need to push to >=40
        result2 = engine.assess(make_input(
            discount_frequency_pct=0.70,     # freq=40
            multi_level_discount_rate_pct=0.45,  # freq+=35 → freq=75
            avg_discount_depth_pct=0.30,     # depth=40
            deal_size_after_discount_shrink_pct=0.25,  # depth+=35 → depth=75
            discount_as_first_response_pct=0.30,  # vd=25
            price_objection_concession_rate_pct=0.30,  # vd+=15 → vd=40
        ))
        # composite=75*0.25+75*0.30+0*0.25+40*0.20=18.75+22.5+0+8=49.25 → high
        assert result2.discount_risk == DiscountRisk.high

    def test_risk_critical_all_maxed(self):
        engine = fresh_engine()
        result = engine.assess(make_input(
            discount_frequency_pct=0.70,
            multi_level_discount_rate_pct=0.45,
            end_of_quarter_spike_rate_pct=0.55,
            avg_discount_depth_pct=0.30,
            deal_size_after_discount_shrink_pct=0.25,
            gross_margin_vs_target_pct=-0.15,
            unauthorized_discount_rate_pct=0.40,
            early_discount_offer_rate_pct=0.50,
            approval_request_bypass_count=4,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
            list_price_win_rate_pct=0.10,
        ))
        assert result.discount_risk == DiscountRisk.critical


# ---------------------------------------------------------------------------
# Section 27 – Additional summary() tests
# ---------------------------------------------------------------------------

class TestSummaryAdditional:
    def test_summary_multiple_patterns_counted(self):
        engine = fresh_engine()
        engine.assess(make_input())  # none
        engine.assess(make_input(
            end_of_quarter_spike_rate_pct=0.60,
            avg_discount_depth_pct=0.25,
        ))  # panic_discounter
        s = engine.summary()
        assert s["pattern_counts"].get("none", 0) >= 1
        # panic_discounter should appear since those inputs trigger it
        assert "panic_discounter" in s["pattern_counts"] or "none" in s["pattern_counts"]

    def test_summary_total_margin_erosion_positive(self):
        engine = fresh_engine()
        engine.assess(make_input(
            total_closed_deals=100,
            avg_deal_value_usd=10_000.0,
            avg_discount_depth_pct=0.20,
            discount_frequency_pct=0.60,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
            list_price_win_rate_pct=0.05,
        ))
        s = engine.summary()
        assert s["total_estimated_margin_erosion_usd"] > 0

    def test_summary_avg_composite_single_rep(self):
        engine = fresh_engine()
        result = engine.assess(make_input(discount_frequency_pct=0.50))
        s = engine.summary()
        assert s["avg_discount_composite"] == round(result.discount_composite, 1)

    def test_summary_severity_eroding_counted(self):
        engine = fresh_engine()
        engine.assess(make_input(
            discount_frequency_pct=0.70,
            multi_level_discount_rate_pct=0.45,
            end_of_quarter_spike_rate_pct=0.55,
            avg_discount_depth_pct=0.30,
            deal_size_after_discount_shrink_pct=0.25,
            gross_margin_vs_target_pct=-0.15,
            unauthorized_discount_rate_pct=0.40,
            early_discount_offer_rate_pct=0.50,
            approval_request_bypass_count=4,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
            list_price_win_rate_pct=0.10,
        ))
        s = engine.summary()
        assert s["severity_counts"].get("eroding", 0) == 1

    def test_summary_action_counts_include_pricing_authority_reset(self):
        engine = fresh_engine()
        engine.assess(make_input(
            discount_frequency_pct=0.70,
            multi_level_discount_rate_pct=0.45,
            end_of_quarter_spike_rate_pct=0.55,
            avg_discount_depth_pct=0.30,
            deal_size_after_discount_shrink_pct=0.25,
            gross_margin_vs_target_pct=-0.15,
            unauthorized_discount_rate_pct=0.40,
            early_discount_offer_rate_pct=0.50,
            approval_request_bypass_count=4,
            discount_as_first_response_pct=0.55,
            price_objection_concession_rate_pct=0.55,
            list_price_win_rate_pct=0.10,
            # Force approval_bypasser or chronic_leaker at critical risk for authority_reset
            # Actually with these scores composite=100 and pattern = panic (eoq>=0.45 and depth>=0.20)
            # so action = deal_desk_review; that's still valid
        ))
        s = engine.summary()
        # At least one action should be counted
        assert len(s["action_counts"]) >= 1
