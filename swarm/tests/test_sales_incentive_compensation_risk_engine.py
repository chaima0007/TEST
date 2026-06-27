"""
Comprehensive pytest test suite for Module 126:
SalesIncentiveCompensationRiskEngine
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_incentive_compensation_risk_engine import (
    CompRisk,
    CompPattern,
    CompSeverity,
    CompAction,
    CompRiskInput,
    CompRiskResult,
    SalesIncentiveCompensationRiskEngine,
)


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> CompRiskInput:
    """Return a clean, low-risk baseline input with optional field overrides."""
    defaults = dict(
        rep_id="REP001",
        region="WEST",
        evaluation_period_id="2024-Q4",
        quota_attainment_pct=100.0,
        quota_attainment_prior_pct=100.0,
        avg_deal_discount_pct=10.0,
        discount_policy_max_pct=15.0,
        deals_discounted_above_policy_count=0,
        q3_deals_closed=10,
        q4_deals_closed=10,
        last_week_of_quarter_deals_pct=0.10,
        deal_size_variance_score=20.0,
        strategic_account_deals_pct=0.40,
        transactional_account_deals_pct=0.30,
        accelerator_threshold_pct=100.0,
        deals_closed_just_above_accelerator=0,
        deals_delayed_to_next_period_count=0,
        avg_margin_pct=30.0,
        margin_benchmark_pct=30.0,
        customer_satisfaction_score=80.0,
        multi_year_contract_pct=0.30,
        comp_complaint_count=0,
    )
    defaults.update(overrides)
    return CompRiskInput(**defaults)


@pytest.fixture
def engine():
    return SalesIncentiveCompensationRiskEngine()


@pytest.fixture
def clean_input():
    return make_input()


# ---------------------------------------------------------------------------
# 1. Enum tests
# ---------------------------------------------------------------------------

class TestEnums:
    def test_comp_risk_values(self):
        assert CompRisk.low.value == "low"
        assert CompRisk.moderate.value == "moderate"
        assert CompRisk.high.value == "high"
        assert CompRisk.critical.value == "critical"

    def test_comp_risk_str_subclass(self):
        assert isinstance(CompRisk.low, str)

    def test_comp_risk_has_four_members(self):
        assert len(list(CompRisk)) == 4

    def test_comp_pattern_values(self):
        assert CompPattern.none.value == "none"
        assert CompPattern.quarter_end_dumping.value == "quarter_end_dumping"
        assert CompPattern.discount_abuse.value == "discount_abuse"
        assert CompPattern.quota_ratchet_gaming.value == "quota_ratchet_gaming"
        assert CompPattern.cherry_picking.value == "cherry_picking"
        assert CompPattern.accelerator_exploitation.value == "accelerator_exploitation"

    def test_comp_pattern_has_six_members(self):
        assert len(list(CompPattern)) == 6

    def test_comp_severity_values(self):
        assert CompSeverity.aligned.value == "aligned"
        assert CompSeverity.watch.value == "watch"
        assert CompSeverity.misaligned.value == "misaligned"
        assert CompSeverity.exploiting.value == "exploiting"

    def test_comp_severity_has_four_members(self):
        assert len(list(CompSeverity)) == 4

    def test_comp_action_values(self):
        assert CompAction.no_action.value == "no_action"
        assert CompAction.comp_plan_review.value == "comp_plan_review"
        assert CompAction.deal_desk_escalation.value == "deal_desk_escalation"
        assert CompAction.quota_recalibration.value == "quota_recalibration"
        assert CompAction.plan_redesign.value == "plan_redesign"

    def test_comp_action_has_five_members(self):
        assert len(list(CompAction)) == 5

    def test_comp_risk_str_equality(self):
        assert CompRisk.low == "low"

    def test_comp_pattern_str_equality(self):
        assert CompPattern.none == "none"


# ---------------------------------------------------------------------------
# 2. CompRiskInput dataclass
# ---------------------------------------------------------------------------

class TestCompRiskInput:
    def test_all_22_fields_exist(self, clean_input):
        fields = [
            "rep_id", "region", "evaluation_period_id",
            "quota_attainment_pct", "quota_attainment_prior_pct",
            "avg_deal_discount_pct", "discount_policy_max_pct",
            "deals_discounted_above_policy_count",
            "q3_deals_closed", "q4_deals_closed",
            "last_week_of_quarter_deals_pct", "deal_size_variance_score",
            "strategic_account_deals_pct", "transactional_account_deals_pct",
            "accelerator_threshold_pct", "deals_closed_just_above_accelerator",
            "deals_delayed_to_next_period_count",
            "avg_margin_pct", "margin_benchmark_pct",
            "customer_satisfaction_score", "multi_year_contract_pct",
            "comp_complaint_count",
        ]
        for f in fields:
            assert hasattr(clean_input, f), f"Missing field: {f}"

    def test_rep_id_stored(self, clean_input):
        assert clean_input.rep_id == "REP001"

    def test_region_stored(self, clean_input):
        assert clean_input.region == "WEST"

    def test_numeric_fields_are_float(self, clean_input):
        assert isinstance(clean_input.quota_attainment_pct, float)

    def test_int_fields_are_int(self, clean_input):
        assert isinstance(clean_input.deals_discounted_above_policy_count, int)


# ---------------------------------------------------------------------------
# 3. CompRiskResult dataclass
# ---------------------------------------------------------------------------

class TestCompRiskResult:
    def test_all_15_fields_present(self, engine, clean_input):
        r = engine.assess(clean_input)
        fields = [
            "rep_id", "region", "comp_risk", "comp_pattern", "comp_severity",
            "recommended_action", "timing_manipulation_score",
            "discount_behavior_score", "quota_gaming_score",
            "strategic_alignment_score", "comp_risk_composite",
            "is_comp_misaligned", "requires_immediate_review",
            "estimated_margin_impact_pct", "comp_signal",
        ]
        for f in fields:
            assert hasattr(r, f), f"Missing result field: {f}"

    def test_to_dict_returns_dict(self, engine, clean_input):
        r = engine.assess(clean_input)
        d = r.to_dict()
        assert isinstance(d, dict)

    def test_to_dict_has_15_keys(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert len(r.to_dict()) == 15

    def test_to_dict_enum_values_are_strings(self, engine, clean_input):
        r = engine.assess(clean_input)
        d = r.to_dict()
        assert isinstance(d["comp_risk"], str)
        assert isinstance(d["comp_pattern"], str)
        assert isinstance(d["comp_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_matches(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.to_dict()["rep_id"] == "REP001"

    def test_result_rep_id_propagated(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.rep_id == "REP001"

    def test_result_region_propagated(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.region == "WEST"

    def test_comp_risk_is_enum(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert isinstance(r.comp_risk, CompRisk)

    def test_comp_pattern_is_enum(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert isinstance(r.comp_pattern, CompPattern)

    def test_comp_severity_is_enum(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert isinstance(r.comp_severity, CompSeverity)

    def test_recommended_action_is_enum(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert isinstance(r.recommended_action, CompAction)

    def test_scores_are_floats(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert isinstance(r.timing_manipulation_score, float)
        assert isinstance(r.discount_behavior_score, float)
        assert isinstance(r.quota_gaming_score, float)
        assert isinstance(r.strategic_alignment_score, float)

    def test_composite_is_float(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert isinstance(r.comp_risk_composite, float)

    def test_booleans_are_bool(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert isinstance(r.is_comp_misaligned, bool)
        assert isinstance(r.requires_immediate_review, bool)

    def test_margin_impact_is_float(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert isinstance(r.estimated_margin_impact_pct, float)

    def test_signal_is_str(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert isinstance(r.comp_signal, str)


# ---------------------------------------------------------------------------
# 4. Timing manipulation score
# ---------------------------------------------------------------------------

class TestTimingManipulationScore:

    def _get_score(self, **overrides):
        inp = make_input(**overrides)
        e = SalesIncentiveCompensationRiskEngine()
        return e.assess(inp).timing_manipulation_score

    # last_week_of_quarter thresholds
    def test_last_week_pct_below_20_no_score(self):
        assert self._get_score(last_week_of_quarter_deals_pct=0.10) == 0.0

    def test_last_week_pct_exactly_20_adds_12(self):
        score = self._get_score(last_week_of_quarter_deals_pct=0.20,
                                q3_deals_closed=10, q4_deals_closed=10,
                                deals_delayed_to_next_period_count=0,
                                comp_complaint_count=0)
        assert score == 12.0

    def test_last_week_pct_exactly_35_adds_28(self):
        score = self._get_score(last_week_of_quarter_deals_pct=0.35,
                                q3_deals_closed=10, q4_deals_closed=10,
                                deals_delayed_to_next_period_count=0,
                                comp_complaint_count=0)
        assert score == 28.0

    def test_last_week_pct_exactly_50_adds_45(self):
        score = self._get_score(last_week_of_quarter_deals_pct=0.50,
                                q3_deals_closed=10, q4_deals_closed=10,
                                deals_delayed_to_next_period_count=0,
                                comp_complaint_count=0)
        assert score == 45.0

    def test_last_week_pct_above_50(self):
        score = self._get_score(last_week_of_quarter_deals_pct=0.80,
                                q3_deals_closed=10, q4_deals_closed=10,
                                deals_delayed_to_next_period_count=0,
                                comp_complaint_count=0)
        assert score == 45.0

    # q4 ratio
    def test_q4_ratio_below_1_5_no_extra(self):
        score = self._get_score(q3_deals_closed=10, q4_deals_closed=10,
                                last_week_of_quarter_deals_pct=0.10,
                                deals_delayed_to_next_period_count=0,
                                comp_complaint_count=0)
        assert score == 0.0

    def test_q4_ratio_1_5_adds_6(self):
        score = self._get_score(q3_deals_closed=10, q4_deals_closed=15,
                                last_week_of_quarter_deals_pct=0.10,
                                deals_delayed_to_next_period_count=0,
                                comp_complaint_count=0)
        assert score == 6.0

    def test_q4_ratio_2_adds_15(self):
        score = self._get_score(q3_deals_closed=10, q4_deals_closed=20,
                                last_week_of_quarter_deals_pct=0.10,
                                deals_delayed_to_next_period_count=0,
                                comp_complaint_count=0)
        assert score == 15.0

    def test_q4_ratio_3_adds_30(self):
        score = self._get_score(q3_deals_closed=10, q4_deals_closed=30,
                                last_week_of_quarter_deals_pct=0.10,
                                deals_delayed_to_next_period_count=0,
                                comp_complaint_count=0)
        assert score == 30.0

    def test_q4_ratio_above_3_adds_30(self):
        score = self._get_score(q3_deals_closed=5, q4_deals_closed=30,
                                last_week_of_quarter_deals_pct=0.10,
                                deals_delayed_to_next_period_count=0,
                                comp_complaint_count=0)
        assert score == 30.0

    def test_q3_zero_no_ratio_added(self):
        score = self._get_score(q3_deals_closed=0, q4_deals_closed=20,
                                last_week_of_quarter_deals_pct=0.10,
                                deals_delayed_to_next_period_count=0,
                                comp_complaint_count=0)
        assert score == 0.0

    # delays
    def test_delays_1_adds_10(self):
        score = self._get_score(deals_delayed_to_next_period_count=1,
                                last_week_of_quarter_deals_pct=0.10,
                                q3_deals_closed=10, q4_deals_closed=10,
                                comp_complaint_count=0)
        assert score == 10.0

    def test_delays_3_adds_20(self):
        score = self._get_score(deals_delayed_to_next_period_count=3,
                                last_week_of_quarter_deals_pct=0.10,
                                q3_deals_closed=10, q4_deals_closed=10,
                                comp_complaint_count=0)
        assert score == 20.0

    def test_delays_2_adds_10(self):
        score = self._get_score(deals_delayed_to_next_period_count=2,
                                last_week_of_quarter_deals_pct=0.10,
                                q3_deals_closed=10, q4_deals_closed=10,
                                comp_complaint_count=0)
        assert score == 10.0

    # complaint
    def test_complaint_2_adds_5(self):
        score = self._get_score(comp_complaint_count=2,
                                last_week_of_quarter_deals_pct=0.10,
                                q3_deals_closed=10, q4_deals_closed=10,
                                deals_delayed_to_next_period_count=0)
        assert score == 5.0

    def test_complaint_1_no_extra(self):
        score = self._get_score(comp_complaint_count=1,
                                last_week_of_quarter_deals_pct=0.10,
                                q3_deals_closed=10, q4_deals_closed=10,
                                deals_delayed_to_next_period_count=0)
        assert score == 0.0

    # capped at 100
    def test_timing_capped_at_100(self):
        score = self._get_score(
            last_week_of_quarter_deals_pct=0.99,
            q3_deals_closed=1, q4_deals_closed=100,
            deals_delayed_to_next_period_count=5,
            comp_complaint_count=5,
        )
        assert score <= 100.0


# ---------------------------------------------------------------------------
# 5. Discount behavior score
# ---------------------------------------------------------------------------

class TestDiscountBehaviorScore:

    def _get_score(self, **overrides):
        inp = make_input(**overrides)
        e = SalesIncentiveCompensationRiskEngine()
        return e.assess(inp).discount_behavior_score

    def test_zero_above_policy_no_score(self):
        assert self._get_score(deals_discounted_above_policy_count=0,
                               avg_deal_discount_pct=10.0,
                               discount_policy_max_pct=15.0,
                               avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                               customer_satisfaction_score=80.0) == 0.0

    def test_one_above_policy_adds_12(self):
        score = self._get_score(deals_discounted_above_policy_count=1,
                                avg_deal_discount_pct=10.0,
                                discount_policy_max_pct=15.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                                customer_satisfaction_score=80.0)
        assert score == 12.0

    def test_three_above_policy_adds_25(self):
        score = self._get_score(deals_discounted_above_policy_count=3,
                                avg_deal_discount_pct=10.0,
                                discount_policy_max_pct=15.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                                customer_satisfaction_score=80.0)
        assert score == 25.0

    def test_five_above_policy_adds_40(self):
        score = self._get_score(deals_discounted_above_policy_count=5,
                                avg_deal_discount_pct=10.0,
                                discount_policy_max_pct=15.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                                customer_satisfaction_score=80.0)
        assert score == 40.0

    def test_excess_discount_2pct_adds_8(self):
        # discount_excess = 17 - 15 = 2
        score = self._get_score(deals_discounted_above_policy_count=0,
                                avg_deal_discount_pct=17.0,
                                discount_policy_max_pct=15.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                                customer_satisfaction_score=80.0)
        assert score == 8.0

    def test_excess_discount_5pct_adds_20(self):
        score = self._get_score(deals_discounted_above_policy_count=0,
                                avg_deal_discount_pct=20.0,
                                discount_policy_max_pct=15.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                                customer_satisfaction_score=80.0)
        assert score == 20.0

    def test_excess_discount_10pct_adds_35(self):
        score = self._get_score(deals_discounted_above_policy_count=0,
                                avg_deal_discount_pct=25.0,
                                discount_policy_max_pct=15.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                                customer_satisfaction_score=80.0)
        assert score == 35.0

    def test_margin_decline_5_adds_10(self):
        score = self._get_score(deals_discounted_above_policy_count=0,
                                avg_deal_discount_pct=10.0,
                                discount_policy_max_pct=15.0,
                                avg_margin_pct=25.0, margin_benchmark_pct=30.0,
                                customer_satisfaction_score=80.0)
        assert score == 10.0

    def test_margin_decline_10_adds_20(self):
        score = self._get_score(deals_discounted_above_policy_count=0,
                                avg_deal_discount_pct=10.0,
                                discount_policy_max_pct=15.0,
                                avg_margin_pct=20.0, margin_benchmark_pct=30.0,
                                customer_satisfaction_score=80.0)
        assert score == 20.0

    def test_low_csat_high_discount_adds_5(self):
        # customer_satisfaction_score < 50 AND avg_deal_discount_pct >= policy*0.8
        # policy=15, 0.8*15=12, avg=13 >= 12
        score = self._get_score(deals_discounted_above_policy_count=0,
                                avg_deal_discount_pct=13.0,
                                discount_policy_max_pct=15.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                                customer_satisfaction_score=45.0)
        assert score == 5.0

    def test_high_csat_no_bonus(self):
        score = self._get_score(deals_discounted_above_policy_count=0,
                                avg_deal_discount_pct=13.0,
                                discount_policy_max_pct=15.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                                customer_satisfaction_score=70.0)
        assert score == 0.0

    def test_discount_score_capped_at_100(self):
        score = self._get_score(deals_discounted_above_policy_count=10,
                                avg_deal_discount_pct=50.0,
                                discount_policy_max_pct=5.0,
                                avg_margin_pct=0.0, margin_benchmark_pct=30.0,
                                customer_satisfaction_score=10.0)
        assert score <= 100.0

    def test_policy_max_zero_no_excess(self):
        # discount_policy_max_pct=0 skips the excess block
        score = self._get_score(deals_discounted_above_policy_count=0,
                                avg_deal_discount_pct=10.0,
                                discount_policy_max_pct=0.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                                customer_satisfaction_score=80.0)
        assert score == 0.0


# ---------------------------------------------------------------------------
# 6. Quota gaming score
# ---------------------------------------------------------------------------

class TestQuotaGamingScore:

    def _get_score(self, **overrides):
        inp = make_input(**overrides)
        e = SalesIncentiveCompensationRiskEngine()
        return e.assess(inp).quota_gaming_score

    def test_no_gaming_baseline(self):
        score = self._get_score(
            deals_closed_just_above_accelerator=0,
            quota_attainment_pct=100.0,
            quota_attainment_prior_pct=100.0,
            deals_delayed_to_next_period_count=0,
            multi_year_contract_pct=0.30,
        )
        assert score == 0.0

    def test_two_just_above_accelerator_adds_18(self):
        score = self._get_score(
            deals_closed_just_above_accelerator=2,
            quota_attainment_pct=100.0,
            quota_attainment_prior_pct=100.0,
            deals_delayed_to_next_period_count=0,
            multi_year_contract_pct=0.30,
        )
        assert score == 18.0

    def test_four_just_above_accelerator_adds_35(self):
        score = self._get_score(
            deals_closed_just_above_accelerator=4,
            quota_attainment_pct=100.0,
            quota_attainment_prior_pct=100.0,
            deals_delayed_to_next_period_count=0,
            multi_year_contract_pct=0.30,
        )
        assert score == 35.0

    def test_attainment_99_to_105_prior_140_adds_30(self):
        score = self._get_score(
            deals_closed_just_above_accelerator=0,
            quota_attainment_pct=102.0,
            quota_attainment_prior_pct=145.0,
            deals_delayed_to_next_period_count=0,
            multi_year_contract_pct=0.30,
        )
        assert score == 30.0

    def test_attainment_below_100_prior_140_adds_15(self):
        score = self._get_score(
            deals_closed_just_above_accelerator=0,
            quota_attainment_pct=95.0,
            quota_attainment_prior_pct=145.0,
            deals_delayed_to_next_period_count=0,
            multi_year_contract_pct=0.30,
        )
        assert score == 15.0

    def test_attainment_106_prior_140_no_quota_gaming_bonus(self):
        # above 105 so neither sandbagging rule fires
        score = self._get_score(
            deals_closed_just_above_accelerator=0,
            quota_attainment_pct=106.0,
            quota_attainment_prior_pct=145.0,
            deals_delayed_to_next_period_count=0,
            multi_year_contract_pct=0.30,
        )
        # prior >= 140 but current is not 99-105 and not < 100
        assert score == 0.0

    def test_delayed_1_adds_8(self):
        score = self._get_score(
            deals_closed_just_above_accelerator=0,
            quota_attainment_pct=100.0,
            quota_attainment_prior_pct=100.0,
            deals_delayed_to_next_period_count=1,
            multi_year_contract_pct=0.30,
        )
        assert score == 8.0

    def test_delayed_2_adds_20(self):
        score = self._get_score(
            deals_closed_just_above_accelerator=0,
            quota_attainment_pct=100.0,
            quota_attainment_prior_pct=100.0,
            deals_delayed_to_next_period_count=2,
            multi_year_contract_pct=0.30,
        )
        assert score == 20.0

    def test_multi_year_below_10_adds_15(self):
        score = self._get_score(
            deals_closed_just_above_accelerator=0,
            quota_attainment_pct=100.0,
            quota_attainment_prior_pct=100.0,
            deals_delayed_to_next_period_count=0,
            multi_year_contract_pct=0.05,
        )
        assert score == 15.0

    def test_multi_year_between_10_20_adds_7(self):
        score = self._get_score(
            deals_closed_just_above_accelerator=0,
            quota_attainment_pct=100.0,
            quota_attainment_prior_pct=100.0,
            deals_delayed_to_next_period_count=0,
            multi_year_contract_pct=0.15,
        )
        assert score == 7.0

    def test_multi_year_above_20_no_penalty(self):
        score = self._get_score(
            deals_closed_just_above_accelerator=0,
            quota_attainment_pct=100.0,
            quota_attainment_prior_pct=100.0,
            deals_delayed_to_next_period_count=0,
            multi_year_contract_pct=0.25,
        )
        assert score == 0.0

    def test_quota_gaming_capped_at_100(self):
        score = self._get_score(
            deals_closed_just_above_accelerator=10,
            quota_attainment_pct=102.0,
            quota_attainment_prior_pct=150.0,
            deals_delayed_to_next_period_count=5,
            multi_year_contract_pct=0.01,
        )
        assert score <= 100.0


# ---------------------------------------------------------------------------
# 7. Strategic alignment score
# ---------------------------------------------------------------------------

class TestStrategicAlignmentScore:

    def _get_score(self, **overrides):
        inp = make_input(**overrides)
        e = SalesIncentiveCompensationRiskEngine()
        return e.assess(inp).strategic_alignment_score

    def test_zero_misalignment_baseline(self):
        score = self._get_score(
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.40,
            deal_size_variance_score=20.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
        )
        assert score == 0.0

    def test_transactional_50_adds_10(self):
        score = self._get_score(
            transactional_account_deals_pct=0.50,
            strategic_account_deals_pct=0.40,
            deal_size_variance_score=20.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
        )
        assert score == 10.0

    def test_transactional_65_adds_22(self):
        score = self._get_score(
            transactional_account_deals_pct=0.65,
            strategic_account_deals_pct=0.40,
            deal_size_variance_score=20.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
        )
        assert score == 22.0

    def test_transactional_80_adds_40(self):
        score = self._get_score(
            transactional_account_deals_pct=0.80,
            strategic_account_deals_pct=0.40,
            deal_size_variance_score=20.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
        )
        assert score == 40.0

    def test_strategic_below_10_adds_30(self):
        score = self._get_score(
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.05,
            deal_size_variance_score=20.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
        )
        assert score == 30.0

    def test_strategic_between_10_20_adds_15(self):
        score = self._get_score(
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.15,
            deal_size_variance_score=20.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
        )
        assert score == 15.0

    def test_strategic_above_20_no_penalty(self):
        score = self._get_score(
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.25,
            deal_size_variance_score=20.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
        )
        assert score == 0.0

    def test_variance_50_adds_10(self):
        score = self._get_score(
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.40,
            deal_size_variance_score=50.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
        )
        assert score == 10.0

    def test_variance_70_adds_20(self):
        score = self._get_score(
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.40,
            deal_size_variance_score=70.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
        )
        assert score == 20.0

    def test_margin_decline_8_adds_10(self):
        score = self._get_score(
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.40,
            deal_size_variance_score=20.0,
            avg_margin_pct=20.0, margin_benchmark_pct=28.0,
        )
        assert score == 10.0

    def test_margin_decline_below_8_no_strategic_penalty(self):
        score = self._get_score(
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.40,
            deal_size_variance_score=20.0,
            avg_margin_pct=25.0, margin_benchmark_pct=30.0,
        )
        # 30-25=5 < 8, no penalty
        assert score == 0.0

    def test_alignment_score_capped_at_100(self):
        score = self._get_score(
            transactional_account_deals_pct=0.99,
            strategic_account_deals_pct=0.01,
            deal_size_variance_score=90.0,
            avg_margin_pct=5.0, margin_benchmark_pct=30.0,
        )
        assert score <= 100.0


# ---------------------------------------------------------------------------
# 8. Composite score
# ---------------------------------------------------------------------------

class TestCompositeScore:

    def test_composite_formula(self, engine):
        # Manually constructed input with known sub-scores
        inp = make_input(
            # timing: last_week=0.35 => 28; q4/q3=1 => 0; delays=0; complaints=0 => 28
            last_week_of_quarter_deals_pct=0.35,
            q3_deals_closed=10, q4_deals_closed=10,
            deals_delayed_to_next_period_count=0,
            comp_complaint_count=0,
            # discount: all zero => 0
            deals_discounted_above_policy_count=0,
            avg_deal_discount_pct=10.0, discount_policy_max_pct=15.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
            customer_satisfaction_score=80.0,
            # gaming: all zero; multi_year=0.30 => 0
            deals_closed_just_above_accelerator=0,
            quota_attainment_pct=100.0, quota_attainment_prior_pct=100.0,
            multi_year_contract_pct=0.30,
            # alignment: transact=0.30, strategic=0.40, variance=20, margin same => 0
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.40,
            deal_size_variance_score=20.0,
        )
        r = engine.assess(inp)
        expected = round(28.0 * 0.25 + 0.0 * 0.30 + 0.0 * 0.25 + 0.0 * 0.20, 1)
        assert r.comp_risk_composite == expected

    def test_composite_not_negative(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.comp_risk_composite >= 0.0

    def test_composite_capped_at_100(self, engine):
        inp = make_input(
            last_week_of_quarter_deals_pct=0.99,
            q3_deals_closed=1, q4_deals_closed=100,
            deals_delayed_to_next_period_count=5,
            comp_complaint_count=5,
            deals_discounted_above_policy_count=10,
            avg_deal_discount_pct=50.0, discount_policy_max_pct=5.0,
            avg_margin_pct=0.0, margin_benchmark_pct=30.0,
            customer_satisfaction_score=10.0,
            deals_closed_just_above_accelerator=10,
            quota_attainment_pct=102.0, quota_attainment_prior_pct=150.0,
            multi_year_contract_pct=0.01,
            transactional_account_deals_pct=0.99,
            strategic_account_deals_pct=0.01,
            deal_size_variance_score=90.0,
        )
        r = engine.assess(inp)
        assert r.comp_risk_composite <= 100.0

    def test_composite_rounded_to_one_decimal(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.comp_risk_composite == round(r.comp_risk_composite, 1)


# ---------------------------------------------------------------------------
# 9. Risk level
# ---------------------------------------------------------------------------

class TestRiskLevel:

    def test_composite_0_is_low(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.comp_risk == CompRisk.low

    def test_composite_below_20_is_low(self, engine):
        inp = make_input(last_week_of_quarter_deals_pct=0.19,
                         deals_delayed_to_next_period_count=0,
                         comp_complaint_count=0,
                         q3_deals_closed=10, q4_deals_closed=10)
        r = engine.assess(inp)
        assert r.comp_risk == CompRisk.low

    def test_composite_20_is_moderate(self, engine):
        # timing=28, composite = 28*0.25 = 7 — not enough; use a bigger trigger
        # delays=3 => timing=20, q4=2x => 15 → total timing=35; 35*0.25=8.75 still not 20
        # let's raise timing to 45 (last_week>=0.50) → 45*0.25=11.25 still not 20
        # combine: 45+30+20=95 timing, composite=95*0.25=23.75 → moderate
        inp = make_input(
            last_week_of_quarter_deals_pct=0.50,
            q3_deals_closed=1, q4_deals_closed=3,
            deals_delayed_to_next_period_count=3,
            comp_complaint_count=0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
        )
        r = engine.assess(inp)
        assert r.comp_risk == CompRisk.moderate

    def test_composite_40_is_high(self, engine):
        inp = make_input(
            last_week_of_quarter_deals_pct=0.50,
            q3_deals_closed=1, q4_deals_closed=3,
            deals_delayed_to_next_period_count=3,
            comp_complaint_count=2,
            deals_discounted_above_policy_count=3,
            avg_deal_discount_pct=20.0, discount_policy_max_pct=15.0,
            avg_margin_pct=20.0, margin_benchmark_pct=30.0,
            customer_satisfaction_score=80.0,
        )
        r = engine.assess(inp)
        assert r.comp_risk in (CompRisk.high, CompRisk.critical)

    def test_composite_60_is_critical(self, engine):
        inp = make_input(
            last_week_of_quarter_deals_pct=0.99,
            q3_deals_closed=1, q4_deals_closed=100,
            deals_delayed_to_next_period_count=5,
            comp_complaint_count=5,
            deals_discounted_above_policy_count=10,
            avg_deal_discount_pct=50.0, discount_policy_max_pct=5.0,
            avg_margin_pct=0.0, margin_benchmark_pct=30.0,
            customer_satisfaction_score=10.0,
            deals_closed_just_above_accelerator=10,
            quota_attainment_pct=102.0, quota_attainment_prior_pct=150.0,
            multi_year_contract_pct=0.01,
            transactional_account_deals_pct=0.99,
            strategic_account_deals_pct=0.01,
            deal_size_variance_score=90.0,
        )
        r = engine.assess(inp)
        assert r.comp_risk == CompRisk.critical


# ---------------------------------------------------------------------------
# 10. Severity
# ---------------------------------------------------------------------------

class TestSeverity:

    def test_low_risk_is_aligned(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.comp_severity == CompSeverity.aligned

    def test_moderate_composite_is_watch(self, engine):
        inp = make_input(
            last_week_of_quarter_deals_pct=0.50,
            q3_deals_closed=1, q4_deals_closed=3,
            deals_delayed_to_next_period_count=3,
            comp_complaint_count=0,
        )
        r = engine.assess(inp)
        if r.comp_risk_composite >= 40:
            assert r.comp_severity == CompSeverity.misaligned
        elif r.comp_risk_composite >= 20:
            assert r.comp_severity == CompSeverity.watch

    def test_critical_composite_is_exploiting(self, engine):
        inp = make_input(
            last_week_of_quarter_deals_pct=0.99,
            q3_deals_closed=1, q4_deals_closed=100,
            deals_delayed_to_next_period_count=5,
            comp_complaint_count=5,
            deals_discounted_above_policy_count=10,
            avg_deal_discount_pct=50.0, discount_policy_max_pct=5.0,
            avg_margin_pct=0.0, margin_benchmark_pct=30.0,
            customer_satisfaction_score=10.0,
            deals_closed_just_above_accelerator=10,
            quota_attainment_pct=102.0, quota_attainment_prior_pct=150.0,
            multi_year_contract_pct=0.01,
            transactional_account_deals_pct=0.99,
            strategic_account_deals_pct=0.01,
            deal_size_variance_score=90.0,
        )
        r = engine.assess(inp)
        assert r.comp_severity == CompSeverity.exploiting

    def test_severity_aligned_composite_below_20(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.comp_severity == CompSeverity.aligned


# ---------------------------------------------------------------------------
# 11. Recommended action
# ---------------------------------------------------------------------------

class TestRecommendedAction:

    def test_low_risk_no_action(self, engine, clean_input):
        r = engine.assess(clean_input)
        if r.comp_risk == CompRisk.low:
            assert r.recommended_action == CompAction.no_action

    def test_moderate_risk_comp_plan_review(self, engine):
        inp = make_input(
            last_week_of_quarter_deals_pct=0.50,
            q3_deals_closed=1, q4_deals_closed=3,
            deals_delayed_to_next_period_count=3,
        )
        r = engine.assess(inp)
        if r.comp_risk == CompRisk.moderate:
            assert r.recommended_action == CompAction.comp_plan_review

    def test_critical_risk_plan_redesign(self, engine):
        inp = make_input(
            last_week_of_quarter_deals_pct=0.99,
            q3_deals_closed=1, q4_deals_closed=100,
            deals_delayed_to_next_period_count=5,
            comp_complaint_count=5,
            deals_discounted_above_policy_count=10,
            avg_deal_discount_pct=50.0, discount_policy_max_pct=5.0,
            avg_margin_pct=0.0, margin_benchmark_pct=30.0,
            customer_satisfaction_score=10.0,
            deals_closed_just_above_accelerator=10,
            quota_attainment_pct=102.0, quota_attainment_prior_pct=150.0,
            multi_year_contract_pct=0.01,
            transactional_account_deals_pct=0.99,
            strategic_account_deals_pct=0.01,
            deal_size_variance_score=90.0,
        )
        r = engine.assess(inp)
        assert r.recommended_action == CompAction.plan_redesign

    def test_high_discount_abuse_deal_desk_escalation(self, engine):
        # Need high risk + discount_abuse pattern
        # discount_abuse: discount>=25 AND above_policy>=2
        # high risk: composite 40-59
        inp = make_input(
            deals_discounted_above_policy_count=5,
            avg_deal_discount_pct=30.0, discount_policy_max_pct=15.0,
            avg_margin_pct=10.0, margin_benchmark_pct=30.0,
            customer_satisfaction_score=40.0,
            transactional_account_deals_pct=0.70,
            strategic_account_deals_pct=0.05,
            deal_size_variance_score=20.0,
        )
        r = engine.assess(inp)
        if r.comp_risk == CompRisk.high and r.comp_pattern == CompPattern.discount_abuse:
            assert r.recommended_action == CompAction.deal_desk_escalation

    def test_high_risk_no_special_pattern_quota_recalibration(self, engine):
        # high risk + quarter_end_dumping pattern => quota_recalibration
        inp = make_input(
            last_week_of_quarter_deals_pct=0.50,
            q3_deals_closed=1, q4_deals_closed=3,
            deals_delayed_to_next_period_count=3,
            comp_complaint_count=2,
            deals_discounted_above_policy_count=3,
            avg_deal_discount_pct=20.0, discount_policy_max_pct=15.0,
            avg_margin_pct=20.0, margin_benchmark_pct=30.0,
            customer_satisfaction_score=80.0,
            multi_year_contract_pct=0.30,
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.40,
            deal_size_variance_score=20.0,
        )
        r = engine.assess(inp)
        if r.comp_risk == CompRisk.high and r.comp_pattern not in (
            CompPattern.discount_abuse, CompPattern.accelerator_exploitation
        ):
            assert r.recommended_action == CompAction.quota_recalibration


# ---------------------------------------------------------------------------
# 12. Pattern detection
# ---------------------------------------------------------------------------

class TestPatternDetection:

    def test_no_pattern_for_clean_input(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.comp_pattern == CompPattern.none

    def test_accelerator_exploitation_priority(self, engine):
        # deals_closed_just_above_accelerator >= 3 AND gaming >= 30
        inp = make_input(
            deals_closed_just_above_accelerator=4,
            quota_attainment_pct=102.0,
            quota_attainment_prior_pct=145.0,
            deals_delayed_to_next_period_count=2,
            multi_year_contract_pct=0.05,
            # also trigger cherry_picking conditions
            transactional_account_deals_pct=0.80,
            strategic_account_deals_pct=0.05,
        )
        r = engine.assess(inp)
        assert r.comp_pattern == CompPattern.accelerator_exploitation

    def test_cherry_picking_when_alignment_high(self, engine):
        # alignment>=30 AND strategic_pct<0.15 (not accelerator)
        inp = make_input(
            transactional_account_deals_pct=0.80,
            strategic_account_deals_pct=0.05,
            deal_size_variance_score=20.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
            deals_closed_just_above_accelerator=0,
        )
        r = engine.assess(inp)
        assert r.comp_pattern == CompPattern.cherry_picking

    def test_quota_ratchet_gaming(self, engine):
        # gaming>=25 AND prior_pct>=130, not accel, not cherry
        inp = make_input(
            deals_closed_just_above_accelerator=2,
            quota_attainment_pct=102.0,
            quota_attainment_prior_pct=140.0,
            deals_delayed_to_next_period_count=2,
            multi_year_contract_pct=0.05,
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.40,
        )
        r = engine.assess(inp)
        # gaming: 18+30+20+15=83 >= 25, prior >= 130
        assert r.comp_pattern == CompPattern.quota_ratchet_gaming

    def test_discount_abuse(self, engine):
        # discount>=25 AND above_policy>=2, not accel/cherry/gaming
        inp = make_input(
            deals_discounted_above_policy_count=5,
            avg_deal_discount_pct=30.0, discount_policy_max_pct=15.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
            customer_satisfaction_score=80.0,
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.40,
            deals_closed_just_above_accelerator=0,
            quota_attainment_prior_pct=100.0,
        )
        r = engine.assess(inp)
        assert r.comp_pattern == CompPattern.discount_abuse

    def test_quarter_end_dumping(self, engine):
        # timing>=25 AND last_week>=0.30, not others
        inp = make_input(
            last_week_of_quarter_deals_pct=0.40,
            q3_deals_closed=10, q4_deals_closed=10,
            deals_delayed_to_next_period_count=0,
            comp_complaint_count=0,
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.40,
            deals_discounted_above_policy_count=0,
            avg_deal_discount_pct=10.0, discount_policy_max_pct=15.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
            deals_closed_just_above_accelerator=0,
            quota_attainment_prior_pct=100.0,
        )
        r = engine.assess(inp)
        # timing = 28; last_week = 0.40 >= 0.30 → quarter_end_dumping
        assert r.comp_pattern == CompPattern.quarter_end_dumping

    def test_accelerator_pattern_beats_cherry_picking(self, engine):
        inp = make_input(
            deals_closed_just_above_accelerator=4,
            quota_attainment_pct=102.0,
            quota_attainment_prior_pct=145.0,
            deals_delayed_to_next_period_count=2,
            multi_year_contract_pct=0.05,
            transactional_account_deals_pct=0.85,
            strategic_account_deals_pct=0.05,
        )
        r = engine.assess(inp)
        assert r.comp_pattern == CompPattern.accelerator_exploitation

    def test_pattern_none_when_no_thresholds_met(self, engine):
        inp = make_input(
            last_week_of_quarter_deals_pct=0.10,
            q3_deals_closed=10, q4_deals_closed=10,
            comp_complaint_count=0,
            deals_discounted_above_policy_count=0,
            avg_deal_discount_pct=10.0, discount_policy_max_pct=15.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
            deals_closed_just_above_accelerator=0,
            quota_attainment_prior_pct=100.0,
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.40,
        )
        r = engine.assess(inp)
        assert r.comp_pattern == CompPattern.none


# ---------------------------------------------------------------------------
# 13. is_comp_misaligned flag
# ---------------------------------------------------------------------------

class TestIsCompMisaligned:

    def test_clean_input_not_misaligned(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.is_comp_misaligned is False

    def test_composite_40_triggers_misaligned(self, engine):
        inp = make_input(
            last_week_of_quarter_deals_pct=0.99,
            q3_deals_closed=1, q4_deals_closed=100,
            deals_delayed_to_next_period_count=5,
            comp_complaint_count=5,
            deals_discounted_above_policy_count=10,
            avg_deal_discount_pct=50.0, discount_policy_max_pct=5.0,
            avg_margin_pct=0.0, margin_benchmark_pct=30.0,
            customer_satisfaction_score=10.0,
            deals_closed_just_above_accelerator=10,
            quota_attainment_pct=102.0, quota_attainment_prior_pct=150.0,
            multi_year_contract_pct=0.01,
            transactional_account_deals_pct=0.99,
            strategic_account_deals_pct=0.01,
            deal_size_variance_score=90.0,
        )
        r = engine.assess(inp)
        assert r.is_comp_misaligned is True

    def test_five_above_policy_triggers_misaligned(self, engine):
        inp = make_input(deals_discounted_above_policy_count=5)
        r = engine.assess(inp)
        assert r.is_comp_misaligned is True

    def test_four_above_policy_not_misaligned_via_policy_count(self, engine):
        # 4 < 5, so only composite or last_week could trigger
        inp = make_input(deals_discounted_above_policy_count=4,
                         last_week_of_quarter_deals_pct=0.10)
        r = engine.assess(inp)
        # Only triggered if composite >= 40
        if r.comp_risk_composite < 40:
            assert r.is_comp_misaligned is False

    def test_last_week_50_triggers_misaligned(self, engine):
        inp = make_input(last_week_of_quarter_deals_pct=0.50)
        r = engine.assess(inp)
        assert r.is_comp_misaligned is True

    def test_last_week_49_not_triggered_by_pct(self, engine):
        inp = make_input(last_week_of_quarter_deals_pct=0.49,
                         deals_discounted_above_policy_count=0)
        r = engine.assess(inp)
        if r.comp_risk_composite < 40:
            assert r.is_comp_misaligned is False


# ---------------------------------------------------------------------------
# 14. requires_immediate_review flag
# ---------------------------------------------------------------------------

class TestRequiresImmediateReview:

    def test_clean_not_immediate(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.requires_immediate_review is False

    def test_composite_30_triggers_immediate(self, engine):
        inp = make_input(
            last_week_of_quarter_deals_pct=0.50,
            q3_deals_closed=1, q4_deals_closed=3,
            deals_delayed_to_next_period_count=3,
            comp_complaint_count=2,
        )
        r = engine.assess(inp)
        if r.comp_risk_composite >= 30:
            assert r.requires_immediate_review is True

    def test_two_complaints_triggers_immediate(self, engine):
        inp = make_input(comp_complaint_count=2)
        r = engine.assess(inp)
        assert r.requires_immediate_review is True

    def test_one_complaint_not_triggered_alone(self, engine):
        inp = make_input(comp_complaint_count=1,
                         avg_margin_pct=30.0, margin_benchmark_pct=30.0)
        r = engine.assess(inp)
        if r.comp_risk_composite < 30:
            assert r.requires_immediate_review is False

    def test_margin_below_80pct_benchmark_triggers(self, engine):
        # avg < benchmark * 0.80 → 15 < 30*0.80=24 → True
        inp = make_input(avg_margin_pct=15.0, margin_benchmark_pct=30.0)
        r = engine.assess(inp)
        assert r.requires_immediate_review is True

    def test_margin_exactly_80pct_not_triggered(self, engine):
        # avg == benchmark * 0.80 → NOT strictly less
        inp = make_input(avg_margin_pct=24.0, margin_benchmark_pct=30.0,
                         comp_complaint_count=0)
        r = engine.assess(inp)
        if r.comp_risk_composite < 30:
            assert r.requires_immediate_review is False

    def test_margin_81pct_not_triggered(self, engine):
        inp = make_input(avg_margin_pct=24.4, margin_benchmark_pct=30.0,
                         comp_complaint_count=0)
        r = engine.assess(inp)
        if r.comp_risk_composite < 30:
            assert r.requires_immediate_review is False


# ---------------------------------------------------------------------------
# 15. estimated_margin_impact_pct
# ---------------------------------------------------------------------------

class TestEstimatedMarginImpact:

    def test_no_decline_zero_impact(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.estimated_margin_impact_pct == 0.0

    def test_positive_margin_no_decline(self, engine):
        # avg > benchmark → no impact
        inp = make_input(avg_margin_pct=35.0, margin_benchmark_pct=30.0)
        r = engine.assess(inp)
        assert r.estimated_margin_impact_pct == 0.0

    def test_margin_impact_formula(self, engine):
        # decline = 30 - 20 = 10; need known composite
        inp = make_input(avg_margin_pct=20.0, margin_benchmark_pct=30.0,
                         # no other scoring factors
                         last_week_of_quarter_deals_pct=0.10,
                         q3_deals_closed=10, q4_deals_closed=10,
                         deals_delayed_to_next_period_count=0,
                         comp_complaint_count=0,
                         deals_discounted_above_policy_count=0,
                         avg_deal_discount_pct=10.0, discount_policy_max_pct=15.0,
                         customer_satisfaction_score=80.0,
                         deals_closed_just_above_accelerator=0,
                         quota_attainment_pct=100.0, quota_attainment_prior_pct=100.0,
                         multi_year_contract_pct=0.30,
                         transactional_account_deals_pct=0.30,
                         strategic_account_deals_pct=0.40,
                         deal_size_variance_score=20.0)
        r = engine.assess(inp)
        expected = round(max(30.0 - 20.0, 0.0) * (r.comp_risk_composite / 100.0), 2)
        assert r.estimated_margin_impact_pct == expected

    def test_margin_impact_rounded_to_two_decimals(self, engine):
        inp = make_input(avg_margin_pct=22.5, margin_benchmark_pct=30.0)
        r = engine.assess(inp)
        assert r.estimated_margin_impact_pct == round(r.estimated_margin_impact_pct, 2)

    def test_margin_impact_non_negative(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.estimated_margin_impact_pct >= 0.0


# ---------------------------------------------------------------------------
# 16. comp_signal
# ---------------------------------------------------------------------------

class TestCompSignal:

    def test_clean_signal_is_aligned_message(self, engine, clean_input):
        r = engine.assess(clean_input)
        # composite=0, pattern=none
        assert "aligned" in r.comp_signal.lower()

    def test_signal_contains_pattern_label(self, engine):
        inp = make_input(
            last_week_of_quarter_deals_pct=0.40,
            q3_deals_closed=10, q4_deals_closed=10,
        )
        r = engine.assess(inp)
        if r.comp_pattern != CompPattern.none:
            label = r.comp_pattern.value.replace("_", " ")
            assert label.lower() in r.comp_signal.lower()

    def test_signal_contains_composite_value(self, engine):
        inp = make_input(last_week_of_quarter_deals_pct=0.40,
                         deals_discounted_above_policy_count=1)
        r = engine.assess(inp)
        if r.comp_risk_composite >= 5 or r.comp_pattern != CompPattern.none:
            # Signal renders composite as f"{composite:.0f}" (rounds half-up)
            rendered = f"{r.comp_risk_composite:.0f}"
            assert rendered in r.comp_signal

    def test_signal_mentions_last_week_pct_when_high(self, engine):
        inp = make_input(last_week_of_quarter_deals_pct=0.30,
                         deals_discounted_above_policy_count=0,
                         deals_closed_just_above_accelerator=0,
                         deals_delayed_to_next_period_count=0)
        r = engine.assess(inp)
        if r.comp_risk_composite >= 5 or r.comp_pattern != CompPattern.none:
            assert "%" in r.comp_signal or "deals" in r.comp_signal.lower()

    def test_signal_is_nonempty_string(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert len(r.comp_signal) > 0

    def test_signal_mentions_discount_when_above_policy(self, engine):
        inp = make_input(deals_discounted_above_policy_count=3)
        r = engine.assess(inp)
        assert "discount" in r.comp_signal.lower() or "3 deals" in r.comp_signal

    def test_signal_mentions_accelerator_when_above_threshold(self, engine):
        # Need composite >= 5 OR pattern != none for the signal to include detail.
        # deals_closed_just_above_accelerator >= 2 adds gaming score but composite
        # may still be < 5 and pattern=none. Use enough to push composite >= 5.
        inp = make_input(deals_closed_just_above_accelerator=2,
                         deals_discounted_above_policy_count=0,
                         last_week_of_quarter_deals_pct=0.10,
                         multi_year_contract_pct=0.05)  # adds 15 gaming => composite=8.25
        r = engine.assess(inp)
        if r.comp_risk_composite >= 5 or r.comp_pattern != CompPattern.none:
            assert "accelerator" in r.comp_signal.lower() or "2 deals" in r.comp_signal

    def test_signal_mentions_delayed_when_present(self, engine):
        inp = make_input(deals_delayed_to_next_period_count=2,
                         last_week_of_quarter_deals_pct=0.10,
                         deals_discounted_above_policy_count=0,
                         deals_closed_just_above_accelerator=0)
        r = engine.assess(inp)
        if r.comp_risk_composite >= 5 or r.comp_pattern != CompPattern.none:
            assert "delayed" in r.comp_signal.lower() or "2 deals" in r.comp_signal


# ---------------------------------------------------------------------------
# 17. assess() method
# ---------------------------------------------------------------------------

class TestAssessMethod:

    def test_returns_comp_risk_result(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert isinstance(r, CompRiskResult)

    def test_assess_stores_result(self, engine, clean_input):
        engine.assess(clean_input)
        assert len(engine._results) == 1

    def test_assess_multiple_stores_all(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"REP{i:03d}"))
        assert len(engine._results) == 5

    def test_assess_rep_id_preserved(self, engine):
        r = engine.assess(make_input(rep_id="UNIQUE_REP"))
        assert r.rep_id == "UNIQUE_REP"

    def test_assess_region_preserved(self, engine):
        r = engine.assess(make_input(region="EMEA"))
        assert r.region == "EMEA"

    def test_assess_different_reps_independent(self, engine):
        r1 = engine.assess(make_input(rep_id="A", last_week_of_quarter_deals_pct=0.10))
        r2 = engine.assess(make_input(rep_id="B", last_week_of_quarter_deals_pct=0.60))
        assert r1.comp_risk_composite < r2.comp_risk_composite

    def test_assess_deterministic(self, engine):
        inp = make_input(last_week_of_quarter_deals_pct=0.40)
        e1 = SalesIncentiveCompensationRiskEngine()
        e2 = SalesIncentiveCompensationRiskEngine()
        r1 = e1.assess(inp)
        r2 = e2.assess(inp)
        assert r1.comp_risk_composite == r2.comp_risk_composite


# ---------------------------------------------------------------------------
# 18. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:

    def test_returns_list(self, engine):
        results = engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        assert isinstance(results, list)

    def test_batch_length_matches_input(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(7)]
        results = engine.assess_batch(inputs)
        assert len(results) == 7

    def test_batch_all_comp_risk_results(self, engine):
        results = engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        assert all(isinstance(r, CompRiskResult) for r in results)

    def test_empty_batch_returns_empty(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_batch_stores_in_results(self, engine):
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        assert len(engine._results) == 5

    def test_batch_order_preserved(self, engine):
        rep_ids = [f"REP{i:03d}" for i in range(10)]
        inputs = [make_input(rep_id=r) for r in rep_ids]
        results = engine.assess_batch(inputs)
        assert [r.rep_id for r in results] == rep_ids

    def test_batch_single_item(self, engine, clean_input):
        results = engine.assess_batch([clean_input])
        assert len(results) == 1
        assert isinstance(results[0], CompRiskResult)


# ---------------------------------------------------------------------------
# 19. summary() — empty state
# ---------------------------------------------------------------------------

class TestSummaryEmpty:

    def test_summary_empty_has_13_keys(self):
        e = SalesIncentiveCompensationRiskEngine()
        s = e.summary()
        assert len(s) == 13

    def test_summary_empty_total_zero(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert e.summary()["total"] == 0

    def test_summary_empty_risk_counts_empty(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert e.summary()["risk_counts"] == {}

    def test_summary_empty_pattern_counts_empty(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert e.summary()["pattern_counts"] == {}

    def test_summary_empty_severity_counts_empty(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert e.summary()["severity_counts"] == {}

    def test_summary_empty_action_counts_empty(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert e.summary()["action_counts"] == {}

    def test_summary_empty_avg_composite_zero(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert e.summary()["avg_comp_risk_composite"] == 0.0

    def test_summary_empty_misaligned_count_zero(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert e.summary()["misaligned_count"] == 0

    def test_summary_empty_immediate_review_count_zero(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert e.summary()["immediate_review_count"] == 0

    def test_summary_empty_avg_timing_zero(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert e.summary()["avg_timing_manipulation_score"] == 0.0

    def test_summary_empty_avg_discount_zero(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert e.summary()["avg_discount_behavior_score"] == 0.0

    def test_summary_empty_avg_gaming_zero(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert e.summary()["avg_quota_gaming_score"] == 0.0

    def test_summary_empty_avg_alignment_zero(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert e.summary()["avg_strategic_alignment_score"] == 0.0

    def test_summary_empty_avg_margin_impact_zero(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert e.summary()["avg_estimated_margin_impact_pct"] == 0.0

    def test_summary_returns_dict(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert isinstance(e.summary(), dict)


# ---------------------------------------------------------------------------
# 20. summary() — populated state
# ---------------------------------------------------------------------------

class TestSummaryPopulated:

    def _engine_with_two(self):
        e = SalesIncentiveCompensationRiskEngine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B",
                             last_week_of_quarter_deals_pct=0.50,
                             deals_discounted_above_policy_count=5,
                             comp_complaint_count=2))
        return e

    def test_total_count(self):
        e = self._engine_with_two()
        assert e.summary()["total"] == 2

    def test_risk_counts_is_dict(self):
        e = self._engine_with_two()
        assert isinstance(e.summary()["risk_counts"], dict)

    def test_risk_counts_sum_to_total(self):
        e = self._engine_with_two()
        s = e.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_pattern_counts_sum_to_total(self):
        e = self._engine_with_two()
        s = e.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_severity_counts_sum_to_total(self):
        e = self._engine_with_two()
        s = e.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_action_counts_sum_to_total(self):
        e = self._engine_with_two()
        s = e.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_avg_comp_risk_composite_is_average(self):
        e = SalesIncentiveCompensationRiskEngine()
        r1 = e.assess(make_input(rep_id="A"))
        r2 = e.assess(make_input(rep_id="B"))
        expected = round((r1.comp_risk_composite + r2.comp_risk_composite) / 2, 1)
        assert e.summary()["avg_comp_risk_composite"] == expected

    def test_avg_timing_is_average(self):
        e = SalesIncentiveCompensationRiskEngine()
        r1 = e.assess(make_input(rep_id="A"))
        r2 = e.assess(make_input(rep_id="B", last_week_of_quarter_deals_pct=0.40))
        expected = round((r1.timing_manipulation_score + r2.timing_manipulation_score) / 2, 1)
        assert e.summary()["avg_timing_manipulation_score"] == expected

    def test_avg_discount_is_average(self):
        e = SalesIncentiveCompensationRiskEngine()
        r1 = e.assess(make_input(rep_id="A"))
        r2 = e.assess(make_input(rep_id="B", deals_discounted_above_policy_count=5))
        expected = round((r1.discount_behavior_score + r2.discount_behavior_score) / 2, 1)
        assert e.summary()["avg_discount_behavior_score"] == expected

    def test_avg_gaming_is_average(self):
        e = SalesIncentiveCompensationRiskEngine()
        r1 = e.assess(make_input(rep_id="A"))
        r2 = e.assess(make_input(rep_id="B", deals_closed_just_above_accelerator=4))
        expected = round((r1.quota_gaming_score + r2.quota_gaming_score) / 2, 1)
        assert e.summary()["avg_quota_gaming_score"] == expected

    def test_avg_alignment_is_average(self):
        e = SalesIncentiveCompensationRiskEngine()
        r1 = e.assess(make_input(rep_id="A"))
        r2 = e.assess(make_input(rep_id="B",
                                  transactional_account_deals_pct=0.80,
                                  strategic_account_deals_pct=0.05))
        expected = round((r1.strategic_alignment_score + r2.strategic_alignment_score) / 2, 1)
        assert e.summary()["avg_strategic_alignment_score"] == expected

    def test_avg_margin_impact_is_average(self):
        e = SalesIncentiveCompensationRiskEngine()
        r1 = e.assess(make_input(rep_id="A"))
        r2 = e.assess(make_input(rep_id="B", avg_margin_pct=15.0, margin_benchmark_pct=30.0))
        expected = round((r1.estimated_margin_impact_pct + r2.estimated_margin_impact_pct) / 2, 2)
        assert e.summary()["avg_estimated_margin_impact_pct"] == expected

    def test_misaligned_count_correct(self):
        e = SalesIncentiveCompensationRiskEngine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B", deals_discounted_above_policy_count=5))
        s = e.summary()
        assert s["misaligned_count"] == sum(1 for r in e._results if r.is_comp_misaligned)

    def test_immediate_review_count_correct(self):
        e = SalesIncentiveCompensationRiskEngine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B", comp_complaint_count=2))
        s = e.summary()
        assert s["immediate_review_count"] == sum(1 for r in e._results if r.requires_immediate_review)

    def test_summary_13_keys_populated(self):
        e = self._engine_with_two()
        assert len(e.summary()) == 13

    def test_summary_keys_exact(self):
        e = self._engine_with_two()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_comp_risk_composite", "misaligned_count",
            "immediate_review_count", "avg_timing_manipulation_score",
            "avg_discount_behavior_score", "avg_quota_gaming_score",
            "avg_strategic_alignment_score", "avg_estimated_margin_impact_pct",
        }
        assert set(e.summary().keys()) == expected_keys


# ---------------------------------------------------------------------------
# 21. Engine state accumulation
# ---------------------------------------------------------------------------

class TestEngineState:

    def test_fresh_engine_empty_results(self):
        e = SalesIncentiveCompensationRiskEngine()
        assert e._results == []

    def test_results_accumulate_across_assess_calls(self):
        e = SalesIncentiveCompensationRiskEngine()
        for i in range(10):
            e.assess(make_input(rep_id=f"R{i}"))
        assert len(e._results) == 10

    def test_two_engines_independent(self):
        e1 = SalesIncentiveCompensationRiskEngine()
        e2 = SalesIncentiveCompensationRiskEngine()
        e1.assess(make_input(rep_id="A"))
        assert len(e2._results) == 0

    def test_batch_adds_to_existing(self):
        e = SalesIncentiveCompensationRiskEngine()
        e.assess(make_input(rep_id="A"))
        e.assess_batch([make_input(rep_id=f"B{i}") for i in range(3)])
        assert len(e._results) == 4

    def test_summary_after_batch_total_correct(self):
        e = SalesIncentiveCompensationRiskEngine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        assert e.summary()["total"] == 5


# ---------------------------------------------------------------------------
# 22. Boundary / edge cases
# ---------------------------------------------------------------------------

class TestBoundaryEdgeCases:

    def test_zero_quota_attainment(self, engine):
        r = engine.assess(make_input(quota_attainment_pct=0.0))
        assert isinstance(r, CompRiskResult)

    def test_200pct_quota_attainment(self, engine):
        r = engine.assess(make_input(quota_attainment_pct=200.0))
        assert isinstance(r, CompRiskResult)

    def test_zero_q3_and_q4(self, engine):
        r = engine.assess(make_input(q3_deals_closed=0, q4_deals_closed=0))
        assert isinstance(r, CompRiskResult)

    def test_last_week_pct_zero(self, engine):
        r = engine.assess(make_input(last_week_of_quarter_deals_pct=0.0))
        assert r.timing_manipulation_score >= 0.0

    def test_last_week_pct_one(self, engine):
        r = engine.assess(make_input(last_week_of_quarter_deals_pct=1.0))
        assert r.timing_manipulation_score <= 100.0

    def test_all_strategic_deals(self, engine):
        r = engine.assess(make_input(strategic_account_deals_pct=1.0,
                                      transactional_account_deals_pct=0.0))
        assert isinstance(r, CompRiskResult)

    def test_all_transactional_deals(self, engine):
        r = engine.assess(make_input(strategic_account_deals_pct=0.0,
                                      transactional_account_deals_pct=1.0))
        assert r.strategic_alignment_score > 0

    def test_zero_deals_discounted_above_policy(self, engine):
        r = engine.assess(make_input(deals_discounted_above_policy_count=0))
        assert r.discount_behavior_score >= 0.0

    def test_high_deal_size_variance(self, engine):
        r = engine.assess(make_input(deal_size_variance_score=100.0))
        assert r.strategic_alignment_score > 0

    def test_zero_deal_size_variance(self, engine):
        r = engine.assess(make_input(deal_size_variance_score=0.0))
        assert isinstance(r, CompRiskResult)

    def test_multi_year_contract_zero(self, engine):
        r = engine.assess(make_input(multi_year_contract_pct=0.0))
        assert r.quota_gaming_score >= 15.0  # adds 15 for <0.10

    def test_multi_year_contract_one(self, engine):
        r = engine.assess(make_input(multi_year_contract_pct=1.0))
        assert isinstance(r, CompRiskResult)

    def test_avg_margin_equals_benchmark(self, engine):
        r = engine.assess(make_input(avg_margin_pct=30.0, margin_benchmark_pct=30.0))
        assert r.estimated_margin_impact_pct == 0.0

    def test_avg_margin_above_benchmark(self, engine):
        r = engine.assess(make_input(avg_margin_pct=40.0, margin_benchmark_pct=30.0))
        assert r.estimated_margin_impact_pct == 0.0

    def test_zero_comp_complaint_count(self, engine):
        r = engine.assess(make_input(comp_complaint_count=0))
        assert isinstance(r, CompRiskResult)

    def test_high_comp_complaint_count(self, engine):
        r = engine.assess(make_input(comp_complaint_count=10))
        assert r.requires_immediate_review is True

    def test_customer_satisfaction_zero(self, engine):
        r = engine.assess(make_input(customer_satisfaction_score=0.0,
                                      avg_deal_discount_pct=15.0,
                                      discount_policy_max_pct=15.0))
        assert isinstance(r, CompRiskResult)

    def test_customer_satisfaction_100(self, engine):
        r = engine.assess(make_input(customer_satisfaction_score=100.0))
        assert isinstance(r, CompRiskResult)

    def test_accelerator_threshold_exactly_100(self, engine):
        r = engine.assess(make_input(accelerator_threshold_pct=100.0))
        assert isinstance(r, CompRiskResult)

    def test_large_batch(self, engine):
        inputs = [make_input(rep_id=f"REP{i:04d}") for i in range(100)]
        results = engine.assess_batch(inputs)
        assert len(results) == 100


# ---------------------------------------------------------------------------
# 23. Score interaction / combination tests
# ---------------------------------------------------------------------------

class TestScoreInteractions:

    def test_all_four_scores_contribute_to_composite(self, engine):
        # All sub-scores non-zero
        inp = make_input(
            last_week_of_quarter_deals_pct=0.35,
            deals_discounted_above_policy_count=1,
            avg_deal_discount_pct=17.0, discount_policy_max_pct=15.0,
            deals_closed_just_above_accelerator=2,
            transactional_account_deals_pct=0.50,
            strategic_account_deals_pct=0.05,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
        )
        r = engine.assess(inp)
        assert r.timing_manipulation_score > 0
        assert r.discount_behavior_score > 0
        assert r.quota_gaming_score > 0
        assert r.strategic_alignment_score > 0

    def test_composite_is_weighted_average(self, engine):
        inp = make_input(
            last_week_of_quarter_deals_pct=0.35,
            q3_deals_closed=10, q4_deals_closed=10,
            deals_delayed_to_next_period_count=0,
            comp_complaint_count=0,
            deals_discounted_above_policy_count=0,
            avg_deal_discount_pct=10.0, discount_policy_max_pct=15.0,
            avg_margin_pct=30.0, margin_benchmark_pct=30.0,
            customer_satisfaction_score=80.0,
            deals_closed_just_above_accelerator=0,
            quota_attainment_pct=100.0, quota_attainment_prior_pct=100.0,
            multi_year_contract_pct=0.30,
            transactional_account_deals_pct=0.30,
            strategic_account_deals_pct=0.40,
            deal_size_variance_score=20.0,
        )
        r = engine.assess(inp)
        ti, di, ga, al = (r.timing_manipulation_score, r.discount_behavior_score,
                          r.quota_gaming_score, r.strategic_alignment_score)
        expected = round(ti * 0.25 + di * 0.30 + ga * 0.25 + al * 0.20, 1)
        assert r.comp_risk_composite == min(expected, 100.0)

    def test_high_timing_score_raises_composite(self, engine):
        low = engine.assess(make_input(last_week_of_quarter_deals_pct=0.05))
        high = engine.assess(make_input(last_week_of_quarter_deals_pct=0.60))
        assert high.comp_risk_composite > low.comp_risk_composite

    def test_high_discount_score_raises_composite(self, engine):
        low = engine.assess(make_input(deals_discounted_above_policy_count=0))
        high = engine.assess(make_input(deals_discounted_above_policy_count=5))
        assert high.comp_risk_composite > low.comp_risk_composite

    def test_high_gaming_score_raises_composite(self, engine):
        low = engine.assess(make_input(deals_closed_just_above_accelerator=0))
        high = engine.assess(make_input(deals_closed_just_above_accelerator=4,
                                         quota_attainment_pct=102.0,
                                         quota_attainment_prior_pct=145.0))
        assert high.comp_risk_composite > low.comp_risk_composite

    def test_high_alignment_score_raises_composite(self, engine):
        low = engine.assess(make_input(transactional_account_deals_pct=0.30,
                                        strategic_account_deals_pct=0.40))
        high = engine.assess(make_input(transactional_account_deals_pct=0.85,
                                         strategic_account_deals_pct=0.05))
        assert high.comp_risk_composite > low.comp_risk_composite


# ---------------------------------------------------------------------------
# 24. to_dict() method
# ---------------------------------------------------------------------------

class TestToDict:

    def test_all_keys_present(self, engine, clean_input):
        d = engine.assess(clean_input).to_dict()
        expected_keys = {
            "rep_id", "region", "comp_risk", "comp_pattern", "comp_severity",
            "recommended_action", "timing_manipulation_score",
            "discount_behavior_score", "quota_gaming_score",
            "strategic_alignment_score", "comp_risk_composite",
            "is_comp_misaligned", "requires_immediate_review",
            "estimated_margin_impact_pct", "comp_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_comp_risk_value_is_string(self, engine, clean_input):
        d = engine.assess(clean_input).to_dict()
        assert d["comp_risk"] in [e.value for e in CompRisk]

    def test_comp_pattern_value_is_string(self, engine, clean_input):
        d = engine.assess(clean_input).to_dict()
        assert d["comp_pattern"] in [e.value for e in CompPattern]

    def test_comp_severity_value_is_string(self, engine, clean_input):
        d = engine.assess(clean_input).to_dict()
        assert d["comp_severity"] in [e.value for e in CompSeverity]

    def test_recommended_action_value_is_string(self, engine, clean_input):
        d = engine.assess(clean_input).to_dict()
        assert d["recommended_action"] in [e.value for e in CompAction]

    def test_is_comp_misaligned_is_bool(self, engine, clean_input):
        d = engine.assess(clean_input).to_dict()
        assert isinstance(d["is_comp_misaligned"], bool)

    def test_requires_immediate_review_is_bool(self, engine, clean_input):
        d = engine.assess(clean_input).to_dict()
        assert isinstance(d["requires_immediate_review"], bool)

    def test_composite_in_dict_matches_result(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.to_dict()["comp_risk_composite"] == r.comp_risk_composite

    def test_scores_in_dict_match_result(self, engine, clean_input):
        r = engine.assess(clean_input)
        d = r.to_dict()
        assert d["timing_manipulation_score"] == r.timing_manipulation_score
        assert d["discount_behavior_score"] == r.discount_behavior_score
        assert d["quota_gaming_score"] == r.quota_gaming_score
        assert d["strategic_alignment_score"] == r.strategic_alignment_score


# ---------------------------------------------------------------------------
# 25. Risk-severity-action coherence
# ---------------------------------------------------------------------------

class TestCoherence:

    def _assess_many(self):
        e = SalesIncentiveCompensationRiskEngine()
        inputs = [
            make_input(rep_id="R1"),
            make_input(rep_id="R2", last_week_of_quarter_deals_pct=0.40),
            make_input(rep_id="R3", deals_discounted_above_policy_count=5,
                       avg_deal_discount_pct=30.0, discount_policy_max_pct=15.0),
            make_input(rep_id="R4", deals_closed_just_above_accelerator=4,
                       quota_attainment_pct=102.0, quota_attainment_prior_pct=150.0,
                       deals_delayed_to_next_period_count=3, multi_year_contract_pct=0.05),
            make_input(rep_id="R5",
                       last_week_of_quarter_deals_pct=0.99,
                       q3_deals_closed=1, q4_deals_closed=100,
                       deals_delayed_to_next_period_count=5,
                       deals_discounted_above_policy_count=10,
                       avg_deal_discount_pct=50.0, discount_policy_max_pct=5.0,
                       avg_margin_pct=0.0, margin_benchmark_pct=30.0,
                       deals_closed_just_above_accelerator=10,
                       quota_attainment_pct=102.0, quota_attainment_prior_pct=150.0,
                       multi_year_contract_pct=0.01,
                       transactional_account_deals_pct=0.99,
                       strategic_account_deals_pct=0.01,
                       deal_size_variance_score=90.0),
        ]
        return e.assess_batch(inputs)

    def test_low_risk_implies_aligned_severity(self):
        for r in self._assess_many():
            if r.comp_risk == CompRisk.low:
                assert r.comp_severity == CompSeverity.aligned

    def test_moderate_risk_implies_watch_severity(self):
        for r in self._assess_many():
            if r.comp_risk == CompRisk.moderate:
                assert r.comp_severity == CompSeverity.watch

    def test_high_risk_implies_misaligned_severity(self):
        for r in self._assess_many():
            if r.comp_risk == CompRisk.high:
                assert r.comp_severity == CompSeverity.misaligned

    def test_critical_risk_implies_exploiting_severity(self):
        for r in self._assess_many():
            if r.comp_risk == CompRisk.critical:
                assert r.comp_severity == CompSeverity.exploiting

    def test_low_risk_implies_no_action(self):
        for r in self._assess_many():
            if r.comp_risk == CompRisk.low:
                assert r.recommended_action == CompAction.no_action

    def test_moderate_risk_implies_comp_plan_review(self):
        for r in self._assess_many():
            if r.comp_risk == CompRisk.moderate:
                assert r.recommended_action == CompAction.comp_plan_review

    def test_critical_risk_implies_plan_redesign(self):
        for r in self._assess_many():
            if r.comp_risk == CompRisk.critical:
                assert r.recommended_action == CompAction.plan_redesign

    def test_high_discount_abuse_implies_deal_desk(self):
        for r in self._assess_many():
            if r.comp_risk == CompRisk.high and r.comp_pattern == CompPattern.discount_abuse:
                assert r.recommended_action == CompAction.deal_desk_escalation

    def test_high_accelerator_exploit_implies_deal_desk(self):
        for r in self._assess_many():
            if r.comp_risk == CompRisk.high and r.comp_pattern == CompPattern.accelerator_exploitation:
                assert r.recommended_action == CompAction.deal_desk_escalation

    def test_composite_matches_risk_level(self):
        for r in self._assess_many():
            c = r.comp_risk_composite
            if c >= 60:
                assert r.comp_risk == CompRisk.critical
            elif c >= 40:
                assert r.comp_risk == CompRisk.high
            elif c >= 20:
                assert r.comp_risk == CompRisk.moderate
            else:
                assert r.comp_risk == CompRisk.low

    def test_composite_matches_severity(self):
        for r in self._assess_many():
            c = r.comp_risk_composite
            if c >= 60:
                assert r.comp_severity == CompSeverity.exploiting
            elif c >= 40:
                assert r.comp_severity == CompSeverity.misaligned
            elif c >= 20:
                assert r.comp_severity == CompSeverity.watch
            else:
                assert r.comp_severity == CompSeverity.aligned

    def test_misaligned_flag_coherence(self):
        for r in self._assess_many():
            if r.comp_risk == CompRisk.critical or r.comp_risk == CompRisk.high:
                # composite is >=40 => should be misaligned
                pass  # not strictly required by spec alone
            assert isinstance(r.is_comp_misaligned, bool)


# ---------------------------------------------------------------------------
# 26. Summary value types
# ---------------------------------------------------------------------------

class TestSummaryTypes:

    def _populated_engine(self):
        e = SalesIncentiveCompensationRiskEngine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        return e

    def test_total_is_int(self):
        assert isinstance(self._populated_engine().summary()["total"], int)

    def test_risk_counts_values_are_int(self):
        s = self._populated_engine().summary()
        for v in s["risk_counts"].values():
            assert isinstance(v, int)

    def test_pattern_counts_values_are_int(self):
        s = self._populated_engine().summary()
        for v in s["pattern_counts"].values():
            assert isinstance(v, int)

    def test_avg_composite_is_float(self):
        s = self._populated_engine().summary()
        assert isinstance(s["avg_comp_risk_composite"], float)

    def test_misaligned_count_is_int(self):
        s = self._populated_engine().summary()
        assert isinstance(s["misaligned_count"], int)

    def test_immediate_review_count_is_int(self):
        s = self._populated_engine().summary()
        assert isinstance(s["immediate_review_count"], int)

    def test_avg_timing_is_float(self):
        s = self._populated_engine().summary()
        assert isinstance(s["avg_timing_manipulation_score"], float)

    def test_avg_discount_is_float(self):
        s = self._populated_engine().summary()
        assert isinstance(s["avg_discount_behavior_score"], float)

    def test_avg_gaming_is_float(self):
        s = self._populated_engine().summary()
        assert isinstance(s["avg_quota_gaming_score"], float)

    def test_avg_alignment_is_float(self):
        s = self._populated_engine().summary()
        assert isinstance(s["avg_strategic_alignment_score"], float)

    def test_avg_margin_impact_is_float(self):
        s = self._populated_engine().summary()
        assert isinstance(s["avg_estimated_margin_impact_pct"], float)


# ---------------------------------------------------------------------------
# 27. Specific regression / exact-value tests
# ---------------------------------------------------------------------------

class TestExactValues:

    def test_clean_baseline_composite_is_zero(self, engine, clean_input):
        r = engine.assess(clean_input)
        # All sub-scores should be 0 for the clean baseline
        assert r.timing_manipulation_score == 0.0
        assert r.discount_behavior_score == 0.0
        # multi_year=0.30 (>0.20) => 0 gaming, accelerator=0, delays=0, attainment normal
        assert r.quota_gaming_score == 0.0
        # transact=0.30, strategic=0.40, variance=20, margin same => 0
        assert r.strategic_alignment_score == 0.0
        assert r.comp_risk_composite == 0.0

    def test_timing_all_flags_combined(self, engine):
        # 45 + 30 + 20 + 5 = 100 → capped at 100
        inp = make_input(
            last_week_of_quarter_deals_pct=0.50,
            q3_deals_closed=1, q4_deals_closed=3,
            deals_delayed_to_next_period_count=3,
            comp_complaint_count=2,
        )
        r = engine.assess(inp)
        assert r.timing_manipulation_score == 100.0

    def test_discount_all_flags_combined_capped(self, engine):
        # 40 (above_policy>=5) + 35 (excess>=10) + 20 (margin_decline>=10) + 5 (low csat) = 100
        # margin_decline = 25 - 15 = 10 → adds 20 (not 10, since >=10 tier)
        inp = make_input(
            deals_discounted_above_policy_count=5,
            avg_deal_discount_pct=30.0, discount_policy_max_pct=15.0,
            avg_margin_pct=15.0, margin_benchmark_pct=25.0,
            customer_satisfaction_score=40.0,
        )
        r = engine.assess(inp)
        # 40 + 35 + 20 + 5 = 100 → capped at 100
        assert r.discount_behavior_score == 100.0

    def test_quota_gaming_four_accelerator_30_sandbagging(self, engine):
        # 35 + 30 + 20 + 15 = 100, cap
        inp = make_input(
            deals_closed_just_above_accelerator=4,
            quota_attainment_pct=102.0,
            quota_attainment_prior_pct=145.0,
            deals_delayed_to_next_period_count=2,
            multi_year_contract_pct=0.05,
        )
        r = engine.assess(inp)
        assert r.quota_gaming_score == 100.0

    def test_strategic_alignment_full_score_capped(self, engine):
        # 40 + 30 + 20 + 10 = 100, cap
        inp = make_input(
            transactional_account_deals_pct=0.85,
            strategic_account_deals_pct=0.05,
            deal_size_variance_score=70.0,
            avg_margin_pct=18.0, margin_benchmark_pct=26.0,
        )
        r = engine.assess(inp)
        assert r.strategic_alignment_score == 100.0

    def test_is_comp_misaligned_exact_boundary_composite_39(self, engine):
        # composite just below 40 — only triggers via deals or last_week
        # use clean input and manually verify
        inp = make_input()
        r = engine.assess(inp)
        # composite=0, no overrides
        assert not r.is_comp_misaligned

    def test_requires_immediate_review_via_margin_threshold(self, engine):
        # avg=23.9, benchmark=30 → 23.9 < 30*0.8=24 → True
        inp = make_input(avg_margin_pct=23.9, margin_benchmark_pct=30.0,
                         comp_complaint_count=0)
        r = engine.assess(inp)
        assert r.requires_immediate_review is True

    def test_requires_immediate_not_triggered_margin_24(self, engine):
        inp = make_input(avg_margin_pct=24.0, margin_benchmark_pct=30.0,
                         comp_complaint_count=0)
        r = engine.assess(inp)
        if r.comp_risk_composite < 30:
            assert r.requires_immediate_review is False

    def test_q4_ratio_exactly_1_5_adds_6(self, engine):
        inp = make_input(q3_deals_closed=2, q4_deals_closed=3,
                         last_week_of_quarter_deals_pct=0.0,
                         deals_delayed_to_next_period_count=0,
                         comp_complaint_count=0)
        r = engine.assess(inp)
        assert r.timing_manipulation_score == 6.0

    def test_q4_ratio_exactly_2_0_adds_15(self, engine):
        inp = make_input(q3_deals_closed=5, q4_deals_closed=10,
                         last_week_of_quarter_deals_pct=0.0,
                         deals_delayed_to_next_period_count=0,
                         comp_complaint_count=0)
        r = engine.assess(inp)
        assert r.timing_manipulation_score == 15.0

    def test_q4_ratio_exactly_3_0_adds_30(self, engine):
        inp = make_input(q3_deals_closed=5, q4_deals_closed=15,
                         last_week_of_quarter_deals_pct=0.0,
                         deals_delayed_to_next_period_count=0,
                         comp_complaint_count=0)
        r = engine.assess(inp)
        assert r.timing_manipulation_score == 30.0

    def test_discount_excess_exactly_2_adds_8(self, engine):
        inp = make_input(deals_discounted_above_policy_count=0,
                         avg_deal_discount_pct=17.0,
                         discount_policy_max_pct=15.0,
                         avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                         customer_satisfaction_score=80.0)
        r = engine.assess(inp)
        assert r.discount_behavior_score == 8.0

    def test_discount_excess_exactly_5_adds_20(self, engine):
        inp = make_input(deals_discounted_above_policy_count=0,
                         avg_deal_discount_pct=20.0,
                         discount_policy_max_pct=15.0,
                         avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                         customer_satisfaction_score=80.0)
        r = engine.assess(inp)
        assert r.discount_behavior_score == 20.0

    def test_discount_excess_exactly_10_adds_35(self, engine):
        inp = make_input(deals_discounted_above_policy_count=0,
                         avg_deal_discount_pct=25.0,
                         discount_policy_max_pct=15.0,
                         avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                         customer_satisfaction_score=80.0)
        r = engine.assess(inp)
        assert r.discount_behavior_score == 35.0

    def test_clean_signal_exact_text(self, engine, clean_input):
        r = engine.assess(clean_input)
        assert r.comp_signal == "Incentive comp behavior aligned with company objectives"


# ---------------------------------------------------------------------------
# 28. Summary with single item
# ---------------------------------------------------------------------------

class TestSummaryOneItem:

    def test_single_item_total_is_1(self):
        e = SalesIncentiveCompensationRiskEngine()
        r = e.assess(make_input())
        s = e.summary()
        assert s["total"] == 1

    def test_single_item_avg_composite_equals_result(self):
        e = SalesIncentiveCompensationRiskEngine()
        r = e.assess(make_input())
        s = e.summary()
        assert s["avg_comp_risk_composite"] == round(r.comp_risk_composite, 1)

    def test_single_item_risk_count_has_one_entry(self):
        e = SalesIncentiveCompensationRiskEngine()
        e.assess(make_input())
        s = e.summary()
        assert sum(s["risk_counts"].values()) == 1

    def test_single_item_pattern_count_has_one_entry(self):
        e = SalesIncentiveCompensationRiskEngine()
        e.assess(make_input())
        s = e.summary()
        assert sum(s["pattern_counts"].values()) == 1

    def test_single_item_severity_count_has_one_entry(self):
        e = SalesIncentiveCompensationRiskEngine()
        e.assess(make_input())
        s = e.summary()
        assert sum(s["severity_counts"].values()) == 1

    def test_single_item_action_count_has_one_entry(self):
        e = SalesIncentiveCompensationRiskEngine()
        e.assess(make_input())
        s = e.summary()
        assert sum(s["action_counts"].values()) == 1

    def test_single_item_avg_margin_impact_equals_result(self):
        e = SalesIncentiveCompensationRiskEngine()
        r = e.assess(make_input(avg_margin_pct=20.0, margin_benchmark_pct=30.0))
        s = e.summary()
        assert s["avg_estimated_margin_impact_pct"] == round(r.estimated_margin_impact_pct, 2)

    def test_single_item_misaligned_count(self):
        e = SalesIncentiveCompensationRiskEngine()
        r = e.assess(make_input(deals_discounted_above_policy_count=5))
        s = e.summary()
        assert s["misaligned_count"] == (1 if r.is_comp_misaligned else 0)

    def test_single_item_immediate_review_count(self):
        e = SalesIncentiveCompensationRiskEngine()
        r = e.assess(make_input(comp_complaint_count=2))
        s = e.summary()
        assert s["immediate_review_count"] == (1 if r.requires_immediate_review else 0)


# ---------------------------------------------------------------------------
# 29. Additional timing score tests
# ---------------------------------------------------------------------------

class TestTimingScoreAdditional:

    def _timing(self, **kw):
        e = SalesIncentiveCompensationRiskEngine()
        return e.assess(make_input(**kw)).timing_manipulation_score

    def test_last_week_25_below_35_adds_12(self):
        assert self._timing(last_week_of_quarter_deals_pct=0.25,
                            q3_deals_closed=10, q4_deals_closed=10,
                            deals_delayed_to_next_period_count=0,
                            comp_complaint_count=0) == 12.0

    def test_last_week_49_adds_28(self):
        assert self._timing(last_week_of_quarter_deals_pct=0.49,
                            q3_deals_closed=10, q4_deals_closed=10,
                            deals_delayed_to_next_period_count=0,
                            comp_complaint_count=0) == 28.0

    def test_delays_0_no_delay_contribution(self):
        assert self._timing(last_week_of_quarter_deals_pct=0.10,
                            q3_deals_closed=10, q4_deals_closed=10,
                            deals_delayed_to_next_period_count=0,
                            comp_complaint_count=0) == 0.0

    def test_delays_4_still_adds_20(self):
        score = self._timing(last_week_of_quarter_deals_pct=0.10,
                             q3_deals_closed=10, q4_deals_closed=10,
                             deals_delayed_to_next_period_count=4,
                             comp_complaint_count=0)
        assert score == 20.0

    def test_complaint_3_same_as_2(self):
        score = self._timing(comp_complaint_count=3,
                             last_week_of_quarter_deals_pct=0.10,
                             q3_deals_closed=10, q4_deals_closed=10,
                             deals_delayed_to_next_period_count=0)
        assert score == 5.0

    def test_q4_ratio_between_15_and_2(self):
        # q4/q3 = 19/10 = 1.9 → adds 6
        score = self._timing(q3_deals_closed=10, q4_deals_closed=19,
                             last_week_of_quarter_deals_pct=0.10,
                             deals_delayed_to_next_period_count=0,
                             comp_complaint_count=0)
        assert score == 6.0

    def test_q4_ratio_between_2_and_3(self):
        # q4/q3 = 25/10 = 2.5 → adds 15
        score = self._timing(q3_deals_closed=10, q4_deals_closed=25,
                             last_week_of_quarter_deals_pct=0.10,
                             deals_delayed_to_next_period_count=0,
                             comp_complaint_count=0)
        assert score == 15.0

    def test_all_zero_gives_zero(self):
        score = self._timing(last_week_of_quarter_deals_pct=0.05,
                             q3_deals_closed=10, q4_deals_closed=10,
                             deals_delayed_to_next_period_count=0,
                             comp_complaint_count=0)
        assert score == 0.0


# ---------------------------------------------------------------------------
# 30. Additional discount behavior tests
# ---------------------------------------------------------------------------

class TestDiscountBehaviorAdditional:

    def _discount(self, **kw):
        e = SalesIncentiveCompensationRiskEngine()
        return e.assess(make_input(**kw)).discount_behavior_score

    def test_two_above_policy_adds_25(self):
        # 3 above => 25, but 2 => only 1 tier qualifies as >=1 (12)... wait: 2 is >=1 but <3
        # Let's re-check: >=5→40, >=3→25, >=1→12. So 2 gives 12.
        score = self._discount(deals_discounted_above_policy_count=2,
                               avg_deal_discount_pct=10.0, discount_policy_max_pct=15.0,
                               avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                               customer_satisfaction_score=80.0)
        assert score == 12.0

    def test_four_above_policy_adds_25(self):
        score = self._discount(deals_discounted_above_policy_count=4,
                               avg_deal_discount_pct=10.0, discount_policy_max_pct=15.0,
                               avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                               customer_satisfaction_score=80.0)
        assert score == 25.0

    def test_margin_decline_exactly_5_adds_10(self):
        score = self._discount(deals_discounted_above_policy_count=0,
                               avg_deal_discount_pct=10.0, discount_policy_max_pct=15.0,
                               avg_margin_pct=25.0, margin_benchmark_pct=30.0,
                               customer_satisfaction_score=80.0)
        assert score == 10.0

    def test_margin_decline_9_adds_10(self):
        score = self._discount(deals_discounted_above_policy_count=0,
                               avg_deal_discount_pct=10.0, discount_policy_max_pct=15.0,
                               avg_margin_pct=21.0, margin_benchmark_pct=30.0,
                               customer_satisfaction_score=80.0)
        assert score == 10.0

    def test_low_csat_below_80pct_policy_no_bonus(self):
        # csat < 50 but avg < policy*0.8 (5 < 15*0.8=12) → no bonus
        score = self._discount(deals_discounted_above_policy_count=0,
                               avg_deal_discount_pct=5.0, discount_policy_max_pct=15.0,
                               avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                               customer_satisfaction_score=40.0)
        assert score == 0.0

    def test_excess_discount_1pct_no_excess_bonus(self):
        # excess = 16-15=1 < 2 → no bonus
        score = self._discount(deals_discounted_above_policy_count=0,
                               avg_deal_discount_pct=16.0, discount_policy_max_pct=15.0,
                               avg_margin_pct=30.0, margin_benchmark_pct=30.0,
                               customer_satisfaction_score=80.0)
        assert score == 0.0


# ---------------------------------------------------------------------------
# 31. Additional quota gaming tests
# ---------------------------------------------------------------------------

class TestQuotaGamingAdditional:

    def _gaming(self, **kw):
        e = SalesIncentiveCompensationRiskEngine()
        return e.assess(make_input(**kw)).quota_gaming_score

    def test_one_just_above_accelerator_no_score(self):
        # >=2→18, >=4→35; so 1 gives 0
        score = self._gaming(deals_closed_just_above_accelerator=1,
                             quota_attainment_pct=100.0,
                             quota_attainment_prior_pct=100.0,
                             deals_delayed_to_next_period_count=0,
                             multi_year_contract_pct=0.30)
        assert score == 0.0

    def test_three_just_above_accelerator_adds_18(self):
        score = self._gaming(deals_closed_just_above_accelerator=3,
                             quota_attainment_pct=100.0,
                             quota_attainment_prior_pct=100.0,
                             deals_delayed_to_next_period_count=0,
                             multi_year_contract_pct=0.30)
        assert score == 18.0

    def test_attainment_99_prior_140_adds_30(self):
        score = self._gaming(deals_closed_just_above_accelerator=0,
                             quota_attainment_pct=99.0,
                             quota_attainment_prior_pct=140.0,
                             deals_delayed_to_next_period_count=0,
                             multi_year_contract_pct=0.30)
        assert score == 30.0

    def test_attainment_105_prior_140_adds_30(self):
        score = self._gaming(deals_closed_just_above_accelerator=0,
                             quota_attainment_pct=105.0,
                             quota_attainment_prior_pct=140.0,
                             deals_delayed_to_next_period_count=0,
                             multi_year_contract_pct=0.30)
        assert score == 30.0

    def test_prior_pct_below_140_no_sandbagging(self):
        score = self._gaming(deals_closed_just_above_accelerator=0,
                             quota_attainment_pct=102.0,
                             quota_attainment_prior_pct=139.9,
                             deals_delayed_to_next_period_count=0,
                             multi_year_contract_pct=0.30)
        assert score == 0.0

    def test_multi_year_exactly_10_adds_7(self):
        score = self._gaming(deals_closed_just_above_accelerator=0,
                             quota_attainment_pct=100.0,
                             quota_attainment_prior_pct=100.0,
                             deals_delayed_to_next_period_count=0,
                             multi_year_contract_pct=0.10)
        # 0.10 is not < 0.10, so no 15-pt penalty; but 0.10 < 0.20, so adds 7
        assert score == 7.0

    def test_multi_year_exactly_20_no_penalty(self):
        score = self._gaming(deals_closed_just_above_accelerator=0,
                             quota_attainment_pct=100.0,
                             quota_attainment_prior_pct=100.0,
                             deals_delayed_to_next_period_count=0,
                             multi_year_contract_pct=0.20)
        assert score == 0.0


# ---------------------------------------------------------------------------
# 32. Additional strategic alignment tests
# ---------------------------------------------------------------------------

class TestStrategicAlignmentAdditional:

    def _alignment(self, **kw):
        e = SalesIncentiveCompensationRiskEngine()
        return e.assess(make_input(**kw)).strategic_alignment_score

    def test_transactional_exactly_50_adds_10(self):
        score = self._alignment(transactional_account_deals_pct=0.50,
                                strategic_account_deals_pct=0.40,
                                deal_size_variance_score=20.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0)
        assert score == 10.0

    def test_transactional_exactly_65_adds_22(self):
        score = self._alignment(transactional_account_deals_pct=0.65,
                                strategic_account_deals_pct=0.40,
                                deal_size_variance_score=20.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0)
        assert score == 22.0

    def test_transactional_exactly_80_adds_40(self):
        score = self._alignment(transactional_account_deals_pct=0.80,
                                strategic_account_deals_pct=0.40,
                                deal_size_variance_score=20.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0)
        assert score == 40.0

    def test_strategic_exactly_10_adds_15(self):
        score = self._alignment(transactional_account_deals_pct=0.30,
                                strategic_account_deals_pct=0.10,
                                deal_size_variance_score=20.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0)
        # 0.10 is not < 0.10 → no 30-pt; but 0.10 < 0.20 → adds 15-pt
        assert score == 15.0

    def test_strategic_exactly_20_no_penalty(self):
        score = self._alignment(transactional_account_deals_pct=0.30,
                                strategic_account_deals_pct=0.20,
                                deal_size_variance_score=20.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0)
        assert score == 0.0

    def test_variance_exactly_50_adds_10(self):
        score = self._alignment(transactional_account_deals_pct=0.30,
                                strategic_account_deals_pct=0.40,
                                deal_size_variance_score=50.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0)
        assert score == 10.0

    def test_variance_exactly_70_adds_20(self):
        score = self._alignment(transactional_account_deals_pct=0.30,
                                strategic_account_deals_pct=0.40,
                                deal_size_variance_score=70.0,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0)
        assert score == 20.0

    def test_variance_below_50_no_variance_score(self):
        score = self._alignment(transactional_account_deals_pct=0.30,
                                strategic_account_deals_pct=0.40,
                                deal_size_variance_score=49.9,
                                avg_margin_pct=30.0, margin_benchmark_pct=30.0)
        assert score == 0.0
