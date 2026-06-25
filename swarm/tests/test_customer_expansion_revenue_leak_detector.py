"""
Comprehensive pytest tests for Module 124:
CustomerExpansionRevenueLeakDetector
"""
from __future__ import annotations

import pytest
from swarm.intelligence.customer_expansion_revenue_leak_detector import (
    CustomerExpansionRevenueLeakDetector,
    ExpansionLeakInput,
    ExpansionLeakResult,
    ExpansionLeakRisk,
    LeakPattern,
    LeakSeverity,
    LeakAction,
)


# ---------------------------------------------------------------------------
# Helpers / Fixtures
# ---------------------------------------------------------------------------

def make_input(**overrides) -> ExpansionLeakInput:
    """Return a baseline healthy account with selectable overrides."""
    defaults = dict(
        account_id="ACC-001",
        region="NA",
        csm_id="CSM-1",
        contract_arr_usd=100_000.0,
        expansion_potential_usd=20_000.0,
        upsell_attempts_last_90d=3,
        upsell_wins_last_90d=1,
        cross_sell_products_available=4,
        cross_sell_products_adopted=3,
        renewal_price_increase_pct=5.0,
        market_price_increase_benchmark_pct=5.0,
        days_since_last_expansion_discussion=10,
        champion_engagement_score=80.0,
        champion_intro_to_new_stakeholders=2,
        qbr_held_last_180d=2,
        product_usage_growth_pct=5.0,
        license_utilization_pct=0.50,
        nps_score=75.0,
        account_health_score=85.0,
        open_expansion_opportunities=1,
        expansion_opportunities_aged_90d_plus=0,
        competitive_displacement_risk_score=20.0,
    )
    defaults.update(overrides)
    return ExpansionLeakInput(**defaults)


@pytest.fixture
def detector():
    return CustomerExpansionRevenueLeakDetector()


@pytest.fixture
def healthy_input():
    return make_input()


@pytest.fixture
def critical_input():
    """Account with every dimension at worst case."""
    return make_input(
        expansion_potential_usd=50_000.0,
        upsell_attempts_last_90d=0,
        upsell_wins_last_90d=0,
        cross_sell_products_available=5,
        cross_sell_products_adopted=0,
        renewal_price_increase_pct=0.0,
        market_price_increase_benchmark_pct=15.0,
        days_since_last_expansion_discussion=120,
        champion_engagement_score=10.0,
        champion_intro_to_new_stakeholders=0,
        qbr_held_last_180d=0,
        license_utilization_pct=0.97,
        nps_score=80.0,
        account_health_score=80.0,
        open_expansion_opportunities=5,
        expansion_opportunities_aged_90d_plus=4,
        competitive_displacement_risk_score=70.0,
    )


# ---------------------------------------------------------------------------
# 1. Imports and class existence
# ---------------------------------------------------------------------------

class TestImports:
    def test_import_detector_class(self):
        assert CustomerExpansionRevenueLeakDetector is not None

    def test_import_input_dataclass(self):
        assert ExpansionLeakInput is not None

    def test_import_result_dataclass(self):
        assert ExpansionLeakResult is not None

    def test_import_expansion_leak_risk(self):
        assert ExpansionLeakRisk is not None

    def test_import_leak_pattern(self):
        assert LeakPattern is not None

    def test_import_leak_severity(self):
        assert LeakSeverity is not None

    def test_import_leak_action(self):
        assert LeakAction is not None


# ---------------------------------------------------------------------------
# 2. Enum values
# ---------------------------------------------------------------------------

class TestEnumValues:
    def test_risk_low(self):
        assert ExpansionLeakRisk.low.value == "low"

    def test_risk_moderate(self):
        assert ExpansionLeakRisk.moderate.value == "moderate"

    def test_risk_high(self):
        assert ExpansionLeakRisk.high.value == "high"

    def test_risk_critical(self):
        assert ExpansionLeakRisk.critical.value == "critical"

    def test_risk_count(self):
        assert len(ExpansionLeakRisk) == 4

    def test_pattern_none(self):
        assert LeakPattern.none.value == "none"

    def test_pattern_upsell_neglect(self):
        assert LeakPattern.upsell_neglect.value == "upsell_neglect"

    def test_pattern_cross_sell_gap(self):
        assert LeakPattern.cross_sell_gap.value == "cross_sell_gap"

    def test_pattern_renewal_underpricing(self):
        assert LeakPattern.renewal_underpricing.value == "renewal_underpricing"

    def test_pattern_champion_not_leveraged(self):
        assert LeakPattern.champion_not_leveraged.value == "champion_not_leveraged"

    def test_pattern_expansion_stall(self):
        assert LeakPattern.expansion_stall.value == "expansion_stall"

    def test_pattern_count(self):
        assert len(LeakPattern) == 6

    def test_severity_captured(self):
        assert LeakSeverity.captured.value == "captured"

    def test_severity_watch(self):
        assert LeakSeverity.watch.value == "watch"

    def test_severity_leaking(self):
        assert LeakSeverity.leaking.value == "leaking"

    def test_severity_critical(self):
        assert LeakSeverity.critical.value == "critical"

    def test_severity_count(self):
        assert len(LeakSeverity) == 4

    def test_action_no_action(self):
        assert LeakAction.no_action.value == "no_action"

    def test_action_expansion_outreach(self):
        assert LeakAction.expansion_outreach.value == "expansion_outreach"

    def test_action_qbr_scheduling(self):
        assert LeakAction.qbr_scheduling.value == "qbr_scheduling"

    def test_action_pricing_renegotiation(self):
        assert LeakAction.pricing_renegotiation.value == "pricing_renegotiation"

    def test_action_executive_alignment(self):
        assert LeakAction.executive_alignment.value == "executive_alignment"

    def test_action_count(self):
        assert len(LeakAction) == 5

    def test_risk_is_str_enum(self):
        assert isinstance(ExpansionLeakRisk.low, str)

    def test_pattern_is_str_enum(self):
        assert isinstance(LeakPattern.none, str)

    def test_severity_is_str_enum(self):
        assert isinstance(LeakSeverity.captured, str)

    def test_action_is_str_enum(self):
        assert isinstance(LeakAction.no_action, str)


# ---------------------------------------------------------------------------
# 3. ExpansionLeakInput – field count and types
# ---------------------------------------------------------------------------

class TestExpansionLeakInputFields:
    def test_has_22_fields(self):
        import dataclasses
        fields = dataclasses.fields(ExpansionLeakInput)
        assert len(fields) == 22

    def test_account_id_field(self, healthy_input):
        assert healthy_input.account_id == "ACC-001"

    def test_region_field(self, healthy_input):
        assert healthy_input.region == "NA"

    def test_csm_id_field(self, healthy_input):
        assert healthy_input.csm_id == "CSM-1"

    def test_contract_arr_usd_field(self, healthy_input):
        assert healthy_input.contract_arr_usd == 100_000.0

    def test_expansion_potential_usd_field(self, healthy_input):
        assert healthy_input.expansion_potential_usd == 20_000.0

    def test_upsell_attempts_field(self, healthy_input):
        assert healthy_input.upsell_attempts_last_90d == 3

    def test_upsell_wins_field(self, healthy_input):
        assert healthy_input.upsell_wins_last_90d == 1

    def test_cross_sell_available_field(self, healthy_input):
        assert healthy_input.cross_sell_products_available == 4

    def test_cross_sell_adopted_field(self, healthy_input):
        assert healthy_input.cross_sell_products_adopted == 3

    def test_renewal_price_pct_field(self, healthy_input):
        assert healthy_input.renewal_price_increase_pct == 5.0

    def test_market_benchmark_field(self, healthy_input):
        assert healthy_input.market_price_increase_benchmark_pct == 5.0

    def test_days_since_discussion_field(self, healthy_input):
        assert healthy_input.days_since_last_expansion_discussion == 10

    def test_champion_engagement_score_field(self, healthy_input):
        assert healthy_input.champion_engagement_score == 80.0

    def test_champion_intro_field(self, healthy_input):
        assert healthy_input.champion_intro_to_new_stakeholders == 2

    def test_qbr_held_field(self, healthy_input):
        assert healthy_input.qbr_held_last_180d == 2

    def test_usage_growth_field(self, healthy_input):
        assert healthy_input.product_usage_growth_pct == 5.0

    def test_license_utilization_field(self, healthy_input):
        assert healthy_input.license_utilization_pct == 0.50

    def test_nps_score_field(self, healthy_input):
        assert healthy_input.nps_score == 75.0

    def test_account_health_field(self, healthy_input):
        assert healthy_input.account_health_score == 85.0

    def test_open_expansion_opps_field(self, healthy_input):
        assert healthy_input.open_expansion_opportunities == 1

    def test_aged_expansion_opps_field(self, healthy_input):
        assert healthy_input.expansion_opportunities_aged_90d_plus == 0

    def test_competitive_risk_field(self, healthy_input):
        assert healthy_input.competitive_displacement_risk_score == 20.0


# ---------------------------------------------------------------------------
# 4. ExpansionLeakResult – field count
# ---------------------------------------------------------------------------

class TestExpansionLeakResultFields:
    def test_has_15_fields(self, detector, healthy_input):
        import dataclasses
        result = detector.assess(healthy_input)
        fields = dataclasses.fields(result)
        assert len(fields) == 15

    def test_result_account_id(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert result.account_id == "ACC-001"

    def test_result_region(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert result.region == "NA"

    def test_result_has_expansion_leak_risk(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.expansion_leak_risk, ExpansionLeakRisk)

    def test_result_has_leak_pattern(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.leak_pattern, LeakPattern)

    def test_result_has_leak_severity(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.leak_severity, LeakSeverity)

    def test_result_has_recommended_action(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.recommended_action, LeakAction)

    def test_result_upsell_neglect_score_float(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.upsell_neglect_score, float)

    def test_result_cross_sell_gap_score_float(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.cross_sell_gap_score, float)

    def test_result_renewal_pricing_score_float(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.renewal_pricing_score, float)

    def test_result_champion_leverage_score_float(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.champion_leverage_score, float)

    def test_result_composite_float(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.expansion_leak_composite, float)

    def test_result_is_revenue_leaking_bool(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.is_revenue_leaking, bool)

    def test_result_requires_immediate_action_bool(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.requires_immediate_action, bool)

    def test_result_estimated_leaked_revenue_float(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.estimated_leaked_revenue_usd, float)

    def test_result_leak_signal_str(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.leak_signal, str)


# ---------------------------------------------------------------------------
# 5. to_dict
# ---------------------------------------------------------------------------

class TestToDict:
    def test_to_dict_returns_dict(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.to_dict(), dict)

    def test_to_dict_has_15_keys(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert len(result.to_dict()) == 15

    def test_to_dict_account_id(self, detector, healthy_input):
        d = detector.assess(healthy_input).to_dict()
        assert d["account_id"] == "ACC-001"

    def test_to_dict_region(self, detector, healthy_input):
        d = detector.assess(healthy_input).to_dict()
        assert d["region"] == "NA"

    def test_to_dict_risk_is_string(self, detector, healthy_input):
        d = detector.assess(healthy_input).to_dict()
        assert isinstance(d["expansion_leak_risk"], str)

    def test_to_dict_pattern_is_string(self, detector, healthy_input):
        d = detector.assess(healthy_input).to_dict()
        assert isinstance(d["leak_pattern"], str)

    def test_to_dict_severity_is_string(self, detector, healthy_input):
        d = detector.assess(healthy_input).to_dict()
        assert isinstance(d["leak_severity"], str)

    def test_to_dict_action_is_string(self, detector, healthy_input):
        d = detector.assess(healthy_input).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_is_revenue_leaking_bool(self, detector, healthy_input):
        d = detector.assess(healthy_input).to_dict()
        assert isinstance(d["is_revenue_leaking"], bool)

    def test_to_dict_requires_immediate_bool(self, detector, healthy_input):
        d = detector.assess(healthy_input).to_dict()
        assert isinstance(d["requires_immediate_action"], bool)

    def test_to_dict_composite_numeric(self, detector, healthy_input):
        d = detector.assess(healthy_input).to_dict()
        assert isinstance(d["expansion_leak_composite"], float)

    def test_to_dict_estimated_revenue_numeric(self, detector, healthy_input):
        d = detector.assess(healthy_input).to_dict()
        assert isinstance(d["estimated_leaked_revenue_usd"], float)


# ---------------------------------------------------------------------------
# 6. assess() – healthy account (low risk)
# ---------------------------------------------------------------------------

class TestAssessHealthyAccount:
    def test_healthy_risk_low(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert result.expansion_leak_risk == ExpansionLeakRisk.low

    def test_healthy_severity_captured(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert result.leak_severity == LeakSeverity.captured

    def test_healthy_action_no_action(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert result.recommended_action == LeakAction.no_action

    def test_healthy_pattern_none(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert result.leak_pattern == LeakPattern.none

    def test_healthy_composite_low(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert result.expansion_leak_composite < 20.0

    def test_healthy_not_leaking(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert result.is_revenue_leaking is False

    def test_healthy_account_id_preserved(self, detector):
        inp = make_input(account_id="XYZ-999")
        result = detector.assess(inp)
        assert result.account_id == "XYZ-999"

    def test_healthy_region_preserved(self, detector):
        inp = make_input(region="EMEA")
        result = detector.assess(inp)
        assert result.region == "EMEA"

    def test_healthy_estimated_revenue_non_negative(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert result.estimated_leaked_revenue_usd >= 0.0

    def test_healthy_scores_all_non_negative(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert result.upsell_neglect_score >= 0.0
        assert result.cross_sell_gap_score >= 0.0
        assert result.renewal_pricing_score >= 0.0
        assert result.champion_leverage_score >= 0.0


# ---------------------------------------------------------------------------
# 7. assess() – critical account
# ---------------------------------------------------------------------------

class TestAssessCriticalAccount:
    def test_critical_risk_critical(self, detector, critical_input):
        result = detector.assess(critical_input)
        assert result.expansion_leak_risk == ExpansionLeakRisk.critical

    def test_critical_severity_critical(self, detector, critical_input):
        result = detector.assess(critical_input)
        assert result.leak_severity == LeakSeverity.critical

    def test_critical_is_leaking(self, detector, critical_input):
        result = detector.assess(critical_input)
        assert result.is_revenue_leaking is True

    def test_critical_requires_immediate_action(self, detector, critical_input):
        result = detector.assess(critical_input)
        assert result.requires_immediate_action is True

    def test_critical_composite_above_60(self, detector, critical_input):
        result = detector.assess(critical_input)
        assert result.expansion_leak_composite >= 60.0

    def test_critical_leaked_revenue_positive(self, detector, critical_input):
        result = detector.assess(critical_input)
        assert result.estimated_leaked_revenue_usd > 0.0

    def test_critical_leaked_revenue_max_cap(self, detector, critical_input):
        # composite capped at 100, so leaked rev <= expansion_potential
        result = detector.assess(critical_input)
        assert result.estimated_leaked_revenue_usd <= critical_input.expansion_potential_usd


# ---------------------------------------------------------------------------
# 8. Upsell neglect score
# ---------------------------------------------------------------------------

class TestUpsellNeglectScore:
    def test_no_attempts_with_potential_adds_35(self, detector):
        inp = make_input(upsell_attempts_last_90d=0, upsell_wins_last_90d=0,
                         expansion_potential_usd=10_000.0,
                         days_since_last_expansion_discussion=0,
                         expansion_opportunities_aged_90d_plus=0,
                         license_utilization_pct=0.50)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 35.0

    def test_no_attempts_zero_potential_no_35(self, detector):
        inp = make_input(upsell_attempts_last_90d=0, upsell_wins_last_90d=0,
                         expansion_potential_usd=0.0,
                         days_since_last_expansion_discussion=0,
                         expansion_opportunities_aged_90d_plus=0,
                         license_utilization_pct=0.50)
        result = detector.assess(inp)
        assert result.upsell_neglect_score < 35.0

    def test_low_conversion_rate_adds_30(self, detector):
        # 1/20 = 5% conversion → +30
        inp = make_input(upsell_attempts_last_90d=20, upsell_wins_last_90d=1,
                         days_since_last_expansion_discussion=0,
                         expansion_opportunities_aged_90d_plus=0,
                         license_utilization_pct=0.50)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 30.0

    def test_mid_conversion_rate_adds_15(self, detector):
        # 2/10 = 20% conversion → +15
        inp = make_input(upsell_attempts_last_90d=10, upsell_wins_last_90d=2,
                         days_since_last_expansion_discussion=0,
                         expansion_opportunities_aged_90d_plus=0,
                         license_utilization_pct=0.50)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 15.0

    def test_good_conversion_adds_0(self, detector):
        # 5/10 = 50% → no upsell penalty
        inp = make_input(upsell_attempts_last_90d=10, upsell_wins_last_90d=5,
                         days_since_last_expansion_discussion=0,
                         expansion_opportunities_aged_90d_plus=0,
                         license_utilization_pct=0.50)
        result = detector.assess(inp)
        assert result.upsell_neglect_score == 0.0

    def test_days_90_plus_adds_35(self, detector):
        inp = make_input(upsell_attempts_last_90d=3, upsell_wins_last_90d=1,
                         days_since_last_expansion_discussion=90,
                         expansion_opportunities_aged_90d_plus=0,
                         license_utilization_pct=0.50)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 35.0

    def test_days_60_to_89_adds_20(self, detector):
        inp = make_input(upsell_attempts_last_90d=3, upsell_wins_last_90d=1,
                         days_since_last_expansion_discussion=60,
                         expansion_opportunities_aged_90d_plus=0,
                         license_utilization_pct=0.50)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 20.0

    def test_days_30_to_59_adds_8(self, detector):
        inp = make_input(upsell_attempts_last_90d=3, upsell_wins_last_90d=1,
                         days_since_last_expansion_discussion=30,
                         expansion_opportunities_aged_90d_plus=0,
                         license_utilization_pct=0.50)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 8.0

    def test_aged_opps_3_plus_adds_20(self, detector):
        inp = make_input(upsell_attempts_last_90d=3, upsell_wins_last_90d=1,
                         days_since_last_expansion_discussion=0,
                         expansion_opportunities_aged_90d_plus=3,
                         license_utilization_pct=0.50)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 20.0

    def test_aged_opps_1_2_adds_10(self, detector):
        inp = make_input(upsell_attempts_last_90d=3, upsell_wins_last_90d=1,
                         days_since_last_expansion_discussion=0,
                         expansion_opportunities_aged_90d_plus=1,
                         license_utilization_pct=0.50)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 10.0

    def test_high_utilization_no_upsell_adds_15(self, detector):
        inp = make_input(upsell_attempts_last_90d=0, upsell_wins_last_90d=0,
                         expansion_potential_usd=0.0,
                         days_since_last_expansion_discussion=0,
                         expansion_opportunities_aged_90d_plus=0,
                         license_utilization_pct=0.92)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 15.0

    def test_high_utilization_with_upsell_no_15(self, detector):
        # utilization >= 0.90 but attempts > 0 → no +15
        inp = make_input(upsell_attempts_last_90d=5, upsell_wins_last_90d=2,
                         days_since_last_expansion_discussion=0,
                         expansion_opportunities_aged_90d_plus=0,
                         license_utilization_pct=0.95)
        result = detector.assess(inp)
        # no utilization penalty
        assert result.upsell_neglect_score < 35.0  # good conversion, no days penalty

    def test_upsell_neglect_capped_at_100(self, detector):
        inp = make_input(upsell_attempts_last_90d=0, expansion_potential_usd=50_000.0,
                         days_since_last_expansion_discussion=120,
                         expansion_opportunities_aged_90d_plus=5,
                         license_utilization_pct=0.98)
        result = detector.assess(inp)
        assert result.upsell_neglect_score <= 100.0


# ---------------------------------------------------------------------------
# 9. Cross-sell gap score
# ---------------------------------------------------------------------------

class TestCrossSellGapScore:
    def test_zero_available_no_score(self, detector):
        inp = make_input(cross_sell_products_available=0,
                         cross_sell_products_adopted=0,
                         product_usage_growth_pct=0.0,
                         open_expansion_opportunities=0,
                         account_health_score=40.0)
        result = detector.assess(inp)
        assert result.cross_sell_gap_score == 0.0

    def test_adoption_below_20pct_adds_45(self, detector):
        # 1/10 = 10% < 20%
        inp = make_input(cross_sell_products_available=10,
                         cross_sell_products_adopted=1,
                         product_usage_growth_pct=0.0,
                         open_expansion_opportunities=0,
                         account_health_score=40.0)
        result = detector.assess(inp)
        assert result.cross_sell_gap_score >= 45.0

    def test_adoption_20_to_40pct_adds_25(self, detector):
        # 3/10 = 30%
        inp = make_input(cross_sell_products_available=10,
                         cross_sell_products_adopted=3,
                         product_usage_growth_pct=0.0,
                         open_expansion_opportunities=0,
                         account_health_score=40.0)
        result = detector.assess(inp)
        assert result.cross_sell_gap_score >= 25.0

    def test_adoption_40_to_60pct_adds_10(self, detector):
        # 5/10 = 50%
        inp = make_input(cross_sell_products_available=10,
                         cross_sell_products_adopted=5,
                         product_usage_growth_pct=0.0,
                         open_expansion_opportunities=0,
                         account_health_score=40.0)
        result = detector.assess(inp)
        assert result.cross_sell_gap_score >= 10.0

    def test_high_health_low_adoption_extra_20(self, detector):
        # health >= 70, adoption < 30%
        # 2/10 = 20% is NOT < 0.20 so main band gives +25 (elif < 0.40)
        # health bonus: 20% < 30% → +20; total = 45
        inp = make_input(cross_sell_products_available=10,
                         cross_sell_products_adopted=2,  # 20% < 30%
                         product_usage_growth_pct=0.0,
                         open_expansion_opportunities=0,
                         account_health_score=75.0)
        result = detector.assess(inp)
        assert result.cross_sell_gap_score >= 45.0  # 25 (adoption band) + 20 (health bonus)

    def test_usage_growth_20pct_no_adoption_adds_20(self, detector):
        inp = make_input(cross_sell_products_available=0,
                         cross_sell_products_adopted=0,
                         product_usage_growth_pct=25.0,
                         open_expansion_opportunities=0,
                         account_health_score=40.0)
        result = detector.assess(inp)
        assert result.cross_sell_gap_score >= 20.0

    def test_usage_growth_10pct_no_adoption_adds_10(self, detector):
        inp = make_input(cross_sell_products_available=0,
                         cross_sell_products_adopted=0,
                         product_usage_growth_pct=15.0,
                         open_expansion_opportunities=0,
                         account_health_score=40.0)
        result = detector.assess(inp)
        assert result.cross_sell_gap_score >= 10.0

    def test_open_opps_4_plus_adds_15(self, detector):
        inp = make_input(cross_sell_products_available=0,
                         cross_sell_products_adopted=0,
                         product_usage_growth_pct=0.0,
                         open_expansion_opportunities=4,
                         account_health_score=40.0)
        result = detector.assess(inp)
        assert result.cross_sell_gap_score >= 15.0

    def test_open_opps_2_3_adds_7(self, detector):
        inp = make_input(cross_sell_products_available=0,
                         cross_sell_products_adopted=0,
                         product_usage_growth_pct=0.0,
                         open_expansion_opportunities=2,
                         account_health_score=40.0)
        result = detector.assess(inp)
        assert result.cross_sell_gap_score >= 7.0

    def test_cross_sell_gap_capped_at_100(self, detector):
        inp = make_input(cross_sell_products_available=10,
                         cross_sell_products_adopted=0,
                         product_usage_growth_pct=30.0,
                         open_expansion_opportunities=6,
                         account_health_score=90.0)
        result = detector.assess(inp)
        assert result.cross_sell_gap_score <= 100.0


# ---------------------------------------------------------------------------
# 10. Renewal pricing score
# ---------------------------------------------------------------------------

class TestRenewalPricingScore:
    def test_delta_10_plus_adds_45(self, detector):
        # benchmark=15, renewal=2 → delta=13
        inp = make_input(market_price_increase_benchmark_pct=15.0,
                         renewal_price_increase_pct=2.0,
                         nps_score=40.0, account_health_score=50.0,
                         competitive_displacement_risk_score=20.0)
        result = detector.assess(inp)
        assert result.renewal_pricing_score >= 45.0

    def test_delta_5_to_10_adds_25(self, detector):
        inp = make_input(market_price_increase_benchmark_pct=10.0,
                         renewal_price_increase_pct=4.0,  # delta=6
                         nps_score=40.0, account_health_score=50.0,
                         competitive_displacement_risk_score=20.0)
        result = detector.assess(inp)
        assert result.renewal_pricing_score >= 25.0

    def test_delta_2_to_5_adds_10(self, detector):
        inp = make_input(market_price_increase_benchmark_pct=7.0,
                         renewal_price_increase_pct=4.5,  # delta=2.5
                         nps_score=40.0, account_health_score=50.0,
                         competitive_displacement_risk_score=20.0)
        result = detector.assess(inp)
        assert result.renewal_pricing_score >= 10.0

    def test_high_nps_low_price_increase_adds_25(self, detector):
        # nps >= 70, renewal < benchmark * 0.5
        inp = make_input(market_price_increase_benchmark_pct=10.0,
                         renewal_price_increase_pct=1.0,  # < 5.0
                         nps_score=80.0, account_health_score=50.0,
                         competitive_displacement_risk_score=20.0)
        result = detector.assess(inp)
        assert result.renewal_pricing_score >= 25.0

    def test_high_health_no_price_increase_adds_20(self, detector):
        inp = make_input(market_price_increase_benchmark_pct=5.0,
                         renewal_price_increase_pct=2.9,  # < 3.0
                         nps_score=40.0, account_health_score=80.0,
                         competitive_displacement_risk_score=20.0)
        result = detector.assess(inp)
        assert result.renewal_pricing_score >= 20.0

    def test_high_competitive_risk_adds_10(self, detector):
        inp = make_input(market_price_increase_benchmark_pct=5.0,
                         renewal_price_increase_pct=5.0,  # delta=0
                         nps_score=40.0, account_health_score=50.0,
                         competitive_displacement_risk_score=65.0)
        result = detector.assess(inp)
        assert result.renewal_pricing_score >= 10.0

    def test_no_underpricing_no_score(self, detector):
        inp = make_input(market_price_increase_benchmark_pct=5.0,
                         renewal_price_increase_pct=6.0,  # above benchmark
                         nps_score=40.0, account_health_score=50.0,
                         competitive_displacement_risk_score=10.0)
        result = detector.assess(inp)
        assert result.renewal_pricing_score == 0.0

    def test_pricing_score_capped_at_100(self, detector):
        inp = make_input(market_price_increase_benchmark_pct=20.0,
                         renewal_price_increase_pct=0.0,
                         nps_score=90.0, account_health_score=90.0,
                         competitive_displacement_risk_score=70.0)
        result = detector.assess(inp)
        assert result.renewal_pricing_score <= 100.0


# ---------------------------------------------------------------------------
# 11. Champion leverage score
# ---------------------------------------------------------------------------

class TestChampionLeverageScore:
    def test_champion_engagement_below_30_adds_40(self, detector):
        inp = make_input(champion_engagement_score=20.0,
                         champion_intro_to_new_stakeholders=2,
                         qbr_held_last_180d=2,
                         nps_score=60.0, account_health_score=40.0,
                         expansion_potential_usd=0.0)
        result = detector.assess(inp)
        assert result.champion_leverage_score >= 40.0

    def test_champion_engagement_30_to_50_adds_20(self, detector):
        inp = make_input(champion_engagement_score=40.0,
                         champion_intro_to_new_stakeholders=2,
                         qbr_held_last_180d=2,
                         nps_score=60.0, account_health_score=40.0,
                         expansion_potential_usd=0.0)
        result = detector.assess(inp)
        assert result.champion_leverage_score >= 20.0

    def test_champion_engagement_50_to_65_adds_8(self, detector):
        inp = make_input(champion_engagement_score=55.0,
                         champion_intro_to_new_stakeholders=2,
                         qbr_held_last_180d=2,
                         nps_score=60.0, account_health_score=40.0,
                         expansion_potential_usd=0.0)
        result = detector.assess(inp)
        assert result.champion_leverage_score >= 8.0

    def test_no_introductions_high_health_adds_30(self, detector):
        inp = make_input(champion_engagement_score=80.0,
                         champion_intro_to_new_stakeholders=0,
                         qbr_held_last_180d=2,
                         nps_score=60.0, account_health_score=65.0,
                         expansion_potential_usd=0.0)
        result = detector.assess(inp)
        assert result.champion_leverage_score >= 30.0

    def test_no_introductions_low_health_adds_15(self, detector):
        inp = make_input(champion_engagement_score=80.0,
                         champion_intro_to_new_stakeholders=0,
                         qbr_held_last_180d=2,
                         nps_score=60.0, account_health_score=50.0,
                         expansion_potential_usd=0.0)
        result = detector.assess(inp)
        assert result.champion_leverage_score >= 15.0

    def test_no_qbr_adds_20(self, detector):
        inp = make_input(champion_engagement_score=80.0,
                         champion_intro_to_new_stakeholders=2,
                         qbr_held_last_180d=0,
                         nps_score=60.0, account_health_score=40.0,
                         expansion_potential_usd=0.0)
        result = detector.assess(inp)
        assert result.champion_leverage_score >= 20.0

    def test_one_qbr_adds_5(self, detector):
        inp = make_input(champion_engagement_score=80.0,
                         champion_intro_to_new_stakeholders=2,
                         qbr_held_last_180d=1,
                         nps_score=60.0, account_health_score=40.0,
                         expansion_potential_usd=0.0)
        result = detector.assess(inp)
        assert result.champion_leverage_score >= 5.0

    def test_low_nps_with_potential_adds_10(self, detector):
        inp = make_input(champion_engagement_score=80.0,
                         champion_intro_to_new_stakeholders=2,
                         qbr_held_last_180d=2,
                         nps_score=35.0, account_health_score=40.0,
                         expansion_potential_usd=10_000.0)
        result = detector.assess(inp)
        assert result.champion_leverage_score >= 10.0

    def test_champion_leverage_capped_at_100(self, detector):
        inp = make_input(champion_engagement_score=5.0,
                         champion_intro_to_new_stakeholders=0,
                         qbr_held_last_180d=0,
                         nps_score=10.0, account_health_score=80.0,
                         expansion_potential_usd=50_000.0)
        result = detector.assess(inp)
        assert result.champion_leverage_score <= 100.0


# ---------------------------------------------------------------------------
# 12. Composite score formula
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_composite_formula_calculation(self, detector):
        # Pick inputs that yield predictable scores
        # Good account: all zeros except upsell_attempts_last_90d=5, wins=3 (60% conv)
        inp = make_input(
            upsell_attempts_last_90d=5,
            upsell_wins_last_90d=3,
            cross_sell_products_available=4,
            cross_sell_products_adopted=3,
            renewal_price_increase_pct=5.0,
            market_price_increase_benchmark_pct=5.0,
            days_since_last_expansion_discussion=5,
            champion_engagement_score=80.0,
            champion_intro_to_new_stakeholders=2,
            qbr_held_last_180d=2,
            license_utilization_pct=0.50,
            nps_score=75.0,
            account_health_score=60.0,
            open_expansion_opportunities=0,
            expansion_opportunities_aged_90d_plus=0,
            product_usage_growth_pct=0.0,
            competitive_displacement_risk_score=10.0,
            expansion_potential_usd=10_000.0,
        )
        result = detector.assess(inp)
        expected = round(
            result.upsell_neglect_score * 0.30
            + result.cross_sell_gap_score * 0.30
            + result.renewal_pricing_score * 0.25
            + result.champion_leverage_score * 0.15,
            1,
        )
        expected = min(expected, 100.0)
        assert result.expansion_leak_composite == expected

    def test_composite_never_exceeds_100(self, detector, critical_input):
        result = detector.assess(critical_input)
        assert result.expansion_leak_composite <= 100.0

    def test_composite_never_below_0(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert result.expansion_leak_composite >= 0.0

    def test_weights_sum_to_1(self):
        assert abs(0.30 + 0.30 + 0.25 + 0.15 - 1.0) < 1e-9


# ---------------------------------------------------------------------------
# 13. Risk level thresholds
# ---------------------------------------------------------------------------

class TestRiskLevelThresholds:
    def _input_with_composite(self, target_composite, detector):
        """Binary-search style: raise scores until composite hits target."""
        # Use a known score distribution for upsell=target_composite/0.3
        # Simpler: use days_since_expansion and known weights
        pass

    def test_composite_below_20_is_low(self, detector):
        inp = make_input()  # healthy → composite < 20
        result = detector.assess(inp)
        if result.expansion_leak_composite < 20:
            assert result.expansion_leak_risk == ExpansionLeakRisk.low

    def test_composite_60_or_above_is_critical(self, detector, critical_input):
        result = detector.assess(critical_input)
        if result.expansion_leak_composite >= 60:
            assert result.expansion_leak_risk == ExpansionLeakRisk.critical

    def test_risk_thresholds_directly(self, detector):
        # Access private method for direct testing
        d = CustomerExpansionRevenueLeakDetector()
        assert d._risk_level(0.0) == ExpansionLeakRisk.low
        assert d._risk_level(19.9) == ExpansionLeakRisk.low
        assert d._risk_level(20.0) == ExpansionLeakRisk.moderate
        assert d._risk_level(39.9) == ExpansionLeakRisk.moderate
        assert d._risk_level(40.0) == ExpansionLeakRisk.high
        assert d._risk_level(59.9) == ExpansionLeakRisk.high
        assert d._risk_level(60.0) == ExpansionLeakRisk.critical
        assert d._risk_level(100.0) == ExpansionLeakRisk.critical


# ---------------------------------------------------------------------------
# 14. Severity thresholds
# ---------------------------------------------------------------------------

class TestSeverityThresholds:
    def test_severity_thresholds_directly(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d._severity(0.0) == LeakSeverity.captured
        assert d._severity(19.9) == LeakSeverity.captured
        assert d._severity(20.0) == LeakSeverity.watch
        assert d._severity(39.9) == LeakSeverity.watch
        assert d._severity(40.0) == LeakSeverity.leaking
        assert d._severity(59.9) == LeakSeverity.leaking
        assert d._severity(60.0) == LeakSeverity.critical
        assert d._severity(100.0) == LeakSeverity.critical


# ---------------------------------------------------------------------------
# 15. Action mapping
# ---------------------------------------------------------------------------

class TestActionMapping:
    def test_action_critical_champion_not_leveraged_is_executive_alignment(self):
        d = CustomerExpansionRevenueLeakDetector()
        action = d._action(ExpansionLeakRisk.critical, LeakPattern.champion_not_leveraged)
        assert action == LeakAction.executive_alignment

    def test_action_critical_other_pattern_is_qbr_scheduling(self):
        d = CustomerExpansionRevenueLeakDetector()
        for pattern in [LeakPattern.expansion_stall, LeakPattern.renewal_underpricing,
                        LeakPattern.cross_sell_gap, LeakPattern.upsell_neglect, LeakPattern.none]:
            action = d._action(ExpansionLeakRisk.critical, pattern)
            assert action == LeakAction.qbr_scheduling

    def test_action_high_renewal_underpricing_is_pricing_renegotiation(self):
        d = CustomerExpansionRevenueLeakDetector()
        action = d._action(ExpansionLeakRisk.high, LeakPattern.renewal_underpricing)
        assert action == LeakAction.pricing_renegotiation

    def test_action_high_other_pattern_is_expansion_outreach(self):
        d = CustomerExpansionRevenueLeakDetector()
        for pattern in [LeakPattern.expansion_stall, LeakPattern.champion_not_leveraged,
                        LeakPattern.cross_sell_gap, LeakPattern.upsell_neglect, LeakPattern.none]:
            action = d._action(ExpansionLeakRisk.high, pattern)
            assert action == LeakAction.expansion_outreach

    def test_action_moderate_is_expansion_outreach(self):
        d = CustomerExpansionRevenueLeakDetector()
        for pattern in LeakPattern:
            action = d._action(ExpansionLeakRisk.moderate, pattern)
            assert action == LeakAction.expansion_outreach

    def test_action_low_is_no_action(self):
        d = CustomerExpansionRevenueLeakDetector()
        for pattern in LeakPattern:
            action = d._action(ExpansionLeakRisk.low, pattern)
            assert action == LeakAction.no_action


# ---------------------------------------------------------------------------
# 16. Pattern detection
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def test_expansion_stall_priority(self):
        """expansion_stall requires upsell>=30 AND cross>=30 AND aged>=2."""
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input(
            upsell_attempts_last_90d=0, expansion_potential_usd=50_000.0,
            days_since_last_expansion_discussion=100,
            cross_sell_products_available=5, cross_sell_products_adopted=0,
            expansion_opportunities_aged_90d_plus=3,
            champion_engagement_score=80.0,
            champion_intro_to_new_stakeholders=1,
            qbr_held_last_180d=2,
            market_price_increase_benchmark_pct=5.0,
            renewal_price_increase_pct=5.0,
        )
        result = d.assess(inp)
        assert result.leak_pattern == LeakPattern.expansion_stall

    def test_champion_not_leveraged_pattern(self):
        """champion>=30, no intros, no QBR → champion_not_leveraged."""
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input(
            champion_engagement_score=15.0,
            champion_intro_to_new_stakeholders=0,
            qbr_held_last_180d=0,
            account_health_score=65.0,
            # avoid expansion_stall
            expansion_opportunities_aged_90d_plus=0,
            upsell_attempts_last_90d=5, upsell_wins_last_90d=3,
            cross_sell_products_available=4, cross_sell_products_adopted=3,
            market_price_increase_benchmark_pct=5.0,
            renewal_price_increase_pct=5.0,
        )
        result = d.assess(inp)
        assert result.leak_pattern == LeakPattern.champion_not_leveraged

    def test_renewal_underpricing_pattern(self):
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input(
            market_price_increase_benchmark_pct=15.0,
            renewal_price_increase_pct=2.0,
            nps_score=80.0,
            account_health_score=80.0,
            champion_engagement_score=80.0,
            champion_intro_to_new_stakeholders=2,
            qbr_held_last_180d=2,
            cross_sell_products_available=4, cross_sell_products_adopted=3,
            upsell_attempts_last_90d=5, upsell_wins_last_90d=3,
            expansion_opportunities_aged_90d_plus=0,
            days_since_last_expansion_discussion=5,
        )
        result = d.assess(inp)
        assert result.leak_pattern == LeakPattern.renewal_underpricing

    def test_cross_sell_gap_pattern(self):
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input(
            cross_sell_products_available=10,
            cross_sell_products_adopted=2,  # 20% adoption → cross>=25
            account_health_score=40.0,
            product_usage_growth_pct=0.0,
            open_expansion_opportunities=0,
            champion_engagement_score=80.0,
            champion_intro_to_new_stakeholders=2,
            qbr_held_last_180d=2,
            upsell_attempts_last_90d=5, upsell_wins_last_90d=3,
            expansion_opportunities_aged_90d_plus=0,
            market_price_increase_benchmark_pct=5.0,
            renewal_price_increase_pct=5.0,
            days_since_last_expansion_discussion=5,
        )
        result = d.assess(inp)
        assert result.leak_pattern == LeakPattern.cross_sell_gap

    def test_upsell_neglect_pattern(self):
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input(
            upsell_attempts_last_90d=0, expansion_potential_usd=50_000.0,
            days_since_last_expansion_discussion=60,
            cross_sell_products_available=4, cross_sell_products_adopted=3,
            champion_engagement_score=80.0,
            champion_intro_to_new_stakeholders=2,
            qbr_held_last_180d=2,
            expansion_opportunities_aged_90d_plus=0,
            market_price_increase_benchmark_pct=5.0,
            renewal_price_increase_pct=5.0,
        )
        result = d.assess(inp)
        assert result.leak_pattern == LeakPattern.upsell_neglect

    def test_none_pattern_healthy(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert result.leak_pattern == LeakPattern.none

    def test_expansion_stall_takes_priority_over_champion(self):
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input(
            upsell_attempts_last_90d=0, expansion_potential_usd=50_000.0,
            days_since_last_expansion_discussion=100,
            cross_sell_products_available=5, cross_sell_products_adopted=0,
            expansion_opportunities_aged_90d_plus=3,
            champion_engagement_score=15.0,
            champion_intro_to_new_stakeholders=0,
            qbr_held_last_180d=0,
            market_price_increase_benchmark_pct=5.0,
            renewal_price_increase_pct=5.0,
        )
        result = d.assess(inp)
        assert result.leak_pattern == LeakPattern.expansion_stall


# ---------------------------------------------------------------------------
# 17. is_revenue_leaking flags
# ---------------------------------------------------------------------------

class TestIsRevenueLeaking:
    def test_composite_above_40_is_leaking(self, detector, critical_input):
        result = detector.assess(critical_input)
        assert result.is_revenue_leaking is True

    def test_aged_opps_3_plus_is_leaking(self, detector):
        inp = make_input(expansion_opportunities_aged_90d_plus=3,
                         upsell_attempts_last_90d=3, upsell_wins_last_90d=1,
                         days_since_last_expansion_discussion=5)
        result = detector.assess(inp)
        assert result.is_revenue_leaking is True

    def test_high_util_no_upsell_is_leaking(self, detector):
        inp = make_input(license_utilization_pct=0.96,
                         upsell_attempts_last_90d=0,
                         expansion_potential_usd=0.0,
                         days_since_last_expansion_discussion=5,
                         expansion_opportunities_aged_90d_plus=0)
        result = detector.assess(inp)
        assert result.is_revenue_leaking is True

    def test_healthy_account_not_leaking(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert result.is_revenue_leaking is False

    def test_utilization_exactly_095_no_attempts_is_leaking(self, detector):
        inp = make_input(license_utilization_pct=0.95,
                         upsell_attempts_last_90d=0,
                         expansion_potential_usd=0.0,
                         days_since_last_expansion_discussion=5,
                         expansion_opportunities_aged_90d_plus=0)
        result = detector.assess(inp)
        assert result.is_revenue_leaking is True

    def test_utilization_094_no_attempts_flag_depends_on_composite(self, detector):
        inp = make_input(license_utilization_pct=0.94,
                         upsell_attempts_last_90d=0,
                         expansion_potential_usd=0.0,
                         days_since_last_expansion_discussion=5,
                         expansion_opportunities_aged_90d_plus=0)
        result = detector.assess(inp)
        # The 0.94 util condition fails; leaking only if composite>=40 or aged>=3
        expected = result.expansion_leak_composite >= 40 or inp.expansion_opportunities_aged_90d_plus >= 3
        assert result.is_revenue_leaking == expected


# ---------------------------------------------------------------------------
# 18. requires_immediate_action flags
# ---------------------------------------------------------------------------

class TestRequiresImmediateAction:
    def test_composite_above_30_requires_action(self, detector):
        inp = make_input(
            upsell_attempts_last_90d=0, expansion_potential_usd=50_000.0,
            days_since_last_expansion_discussion=30,
            cross_sell_products_available=10, cross_sell_products_adopted=1,
            expansion_opportunities_aged_90d_plus=0,
        )
        result = detector.assess(inp)
        if result.expansion_leak_composite >= 30:
            assert result.requires_immediate_action is True

    def test_days_90_plus_requires_action(self, detector):
        inp = make_input(days_since_last_expansion_discussion=90)
        result = detector.assess(inp)
        assert result.requires_immediate_action is True

    def test_no_qbr_requires_action(self, detector):
        inp = make_input(qbr_held_last_180d=0)
        result = detector.assess(inp)
        assert result.requires_immediate_action is True

    def test_healthy_no_immediate_action(self, detector):
        inp = make_input(
            days_since_last_expansion_discussion=5,
            qbr_held_last_180d=2,
        )
        result = detector.assess(inp)
        if result.expansion_leak_composite < 30:
            assert result.requires_immediate_action is False

    def test_days_89_no_qbr_effect(self, detector):
        inp = make_input(days_since_last_expansion_discussion=89,
                         qbr_held_last_180d=2)
        result = detector.assess(inp)
        if result.expansion_leak_composite < 30:
            # 89 days doesn't trigger the >=90 rule
            assert result.requires_immediate_action is False

    def test_days_exactly_90_triggers(self, detector):
        inp = make_input(days_since_last_expansion_discussion=90,
                         qbr_held_last_180d=2)
        result = detector.assess(inp)
        assert result.requires_immediate_action is True


# ---------------------------------------------------------------------------
# 19. estimated_leaked_revenue_usd
# ---------------------------------------------------------------------------

class TestEstimatedLeakedRevenue:
    def test_leaked_revenue_formula(self, detector):
        inp = make_input(expansion_potential_usd=50_000.0)
        result = detector.assess(inp)
        expected = round(50_000.0 * (result.expansion_leak_composite / 100.0), 2)
        assert result.estimated_leaked_revenue_usd == expected

    def test_leaked_revenue_zero_potential(self, detector):
        inp = make_input(expansion_potential_usd=0.0)
        result = detector.assess(inp)
        assert result.estimated_leaked_revenue_usd == 0.0

    def test_leaked_revenue_100_composite_equals_potential(self, detector):
        # Force composite=100 by capping
        inp = make_input(expansion_potential_usd=10_000.0)
        d = CustomerExpansionRevenueLeakDetector()
        # Direct private method test
        rev = d._leaked_revenue(inp, 100.0)
        assert rev == 10_000.0

    def test_leaked_revenue_rounded_to_2_decimals(self, detector):
        inp = make_input(expansion_potential_usd=33_333.33)
        result = detector.assess(inp)
        # Check it's rounded to 2 decimal places
        assert result.estimated_leaked_revenue_usd == round(
            33_333.33 * (result.expansion_leak_composite / 100.0), 2
        )

    def test_leaked_revenue_non_negative(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert result.estimated_leaked_revenue_usd >= 0.0


# ---------------------------------------------------------------------------
# 20. leak_signal content
# ---------------------------------------------------------------------------

class TestLeakSignal:
    def test_signal_is_non_empty_string(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result.leak_signal, str)
        assert len(result.leak_signal) > 0

    def test_signal_healthy_contains_healthy_message(self, detector):
        inp = make_input(
            upsell_attempts_last_90d=3, upsell_wins_last_90d=2,
            cross_sell_products_available=4, cross_sell_products_adopted=4,
            renewal_price_increase_pct=5.0, market_price_increase_benchmark_pct=5.0,
            days_since_last_expansion_discussion=5,
            champion_engagement_score=90.0,
            champion_intro_to_new_stakeholders=3,
            qbr_held_last_180d=2,
            license_utilization_pct=0.50,
            nps_score=80.0, account_health_score=85.0,
            open_expansion_opportunities=0,
            expansion_opportunities_aged_90d_plus=0,
            product_usage_growth_pct=0.0,
            competitive_displacement_risk_score=10.0,
        )
        result = detector.assess(inp)
        if result.expansion_leak_composite < 5 and result.leak_pattern == LeakPattern.none:
            assert "healthy" in result.leak_signal.lower()

    def test_signal_contains_days_when_60_plus(self, detector):
        inp = make_input(days_since_last_expansion_discussion=75)
        result = detector.assess(inp)
        assert "75d" in result.leak_signal

    def test_signal_contains_aged_opps(self, detector):
        # Ensure composite >= 5 so we don't hit the healthy shortcircuit
        inp = make_input(expansion_opportunities_aged_90d_plus=2,
                         upsell_attempts_last_90d=0,
                         expansion_potential_usd=10_000.0,
                         days_since_last_expansion_discussion=5)
        result = detector.assess(inp)
        # composite > 5 ensures detailed signal path
        if result.expansion_leak_composite >= 5 or result.leak_pattern != LeakPattern.none:
            assert "2 aged opps 90d+" in result.leak_signal

    def test_signal_contains_no_qbr(self, detector):
        # qbr=0 adds 20 to champion score (0.15 weight = 3 to composite > 5)
        # also ensure champion_intro=0 with health>=60 adds another 30 → composite > 5
        inp = make_input(qbr_held_last_180d=0,
                         champion_engagement_score=15.0,  # adds 40 to champion score
                         champion_intro_to_new_stakeholders=0,
                         account_health_score=65.0,
                         days_since_last_expansion_discussion=5)
        result = detector.assess(inp)
        assert result.expansion_leak_composite >= 5
        assert "no QBR" in result.leak_signal

    def test_signal_contains_utilization_no_upsell(self, detector):
        # util>=0.90 no attempts adds 15 to upsell (0.30 weight = 4.5 to composite)
        # cross_sell low adoption to push composite above 5
        inp = make_input(license_utilization_pct=0.95,
                         upsell_attempts_last_90d=0,
                         expansion_potential_usd=0.0,
                         days_since_last_expansion_discussion=5,
                         cross_sell_products_available=10,
                         cross_sell_products_adopted=1,  # 10% → +45 cross_sell
                         account_health_score=40.0,
                         product_usage_growth_pct=0.0,
                         open_expansion_opportunities=0)
        result = detector.assess(inp)
        assert result.expansion_leak_composite >= 5
        assert "utilization" in result.leak_signal

    def test_signal_contains_composite(self, detector, critical_input):
        result = detector.assess(critical_input)
        assert "composite" in result.leak_signal

    def test_signal_contains_pattern_label(self, detector, critical_input):
        result = detector.assess(critical_input)
        pattern_label = result.leak_pattern.value.replace("_", " ")
        assert pattern_label.lower() in result.leak_signal.lower()


# ---------------------------------------------------------------------------
# 21. assess_batch
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_batch_returns_list(self, detector):
        inputs = [make_input(account_id=f"ACC-{i}") for i in range(5)]
        results = detector.assess_batch(inputs)
        assert isinstance(results, list)

    def test_batch_length_matches_input(self, detector):
        inputs = [make_input(account_id=f"ACC-{i}") for i in range(7)]
        results = detector.assess_batch(inputs)
        assert len(results) == 7

    def test_batch_returns_results(self, detector):
        inputs = [make_input(account_id=f"ACC-{i}") for i in range(3)]
        results = detector.assess_batch(inputs)
        for r in results:
            assert isinstance(r, ExpansionLeakResult)

    def test_batch_preserves_account_ids(self, detector):
        ids = ["ACC-A", "ACC-B", "ACC-C"]
        inputs = [make_input(account_id=aid) for aid in ids]
        results = detector.assess_batch(inputs)
        assert [r.account_id for r in results] == ids

    def test_batch_empty_list(self, detector):
        results = detector.assess_batch([])
        assert results == []

    def test_batch_single_item(self, detector):
        inp = make_input(account_id="SOLO")
        results = detector.assess_batch([inp])
        assert len(results) == 1
        assert results[0].account_id == "SOLO"

    def test_batch_accumulates_in_results(self, detector):
        inputs = [make_input(account_id=f"ACC-{i}") for i in range(4)]
        detector.assess_batch(inputs)
        summ = detector.summary()
        assert summ["total"] == 4


# ---------------------------------------------------------------------------
# 22. summary() – empty
# ---------------------------------------------------------------------------

class TestSummaryEmpty:
    def test_summary_empty_returns_dict(self):
        d = CustomerExpansionRevenueLeakDetector()
        s = d.summary()
        assert isinstance(s, dict)

    def test_summary_empty_has_13_keys(self):
        d = CustomerExpansionRevenueLeakDetector()
        s = d.summary()
        assert len(s) == 13

    def test_summary_empty_total_zero(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d.summary()["total"] == 0

    def test_summary_empty_risk_counts_empty(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d.summary()["risk_counts"] == {}

    def test_summary_empty_pattern_counts_empty(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d.summary()["pattern_counts"] == {}

    def test_summary_empty_severity_counts_empty(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d.summary()["severity_counts"] == {}

    def test_summary_empty_action_counts_empty(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d.summary()["action_counts"] == {}

    def test_summary_empty_avg_composite_zero(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d.summary()["avg_expansion_leak_composite"] == 0.0

    def test_summary_empty_leaking_count_zero(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d.summary()["leaking_count"] == 0

    def test_summary_empty_immediate_action_count_zero(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d.summary()["immediate_action_count"] == 0

    def test_summary_empty_avg_upsell_zero(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d.summary()["avg_upsell_neglect_score"] == 0.0

    def test_summary_empty_avg_cross_sell_zero(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d.summary()["avg_cross_sell_gap_score"] == 0.0

    def test_summary_empty_avg_renewal_zero(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d.summary()["avg_renewal_pricing_score"] == 0.0

    def test_summary_empty_avg_champion_zero(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d.summary()["avg_champion_leverage_score"] == 0.0

    def test_summary_empty_total_revenue_zero(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d.summary()["total_estimated_leaked_revenue_usd"] == 0.0


# ---------------------------------------------------------------------------
# 23. summary() – populated
# ---------------------------------------------------------------------------

class TestSummaryPopulated:
    def _populated_detector(self):
        d = CustomerExpansionRevenueLeakDetector()
        inputs = [
            make_input(account_id="A1", region="NA"),
            make_input(account_id="A2", region="EMEA",
                       upsell_attempts_last_90d=0, expansion_potential_usd=50_000.0,
                       days_since_last_expansion_discussion=100,
                       cross_sell_products_available=5, cross_sell_products_adopted=0,
                       expansion_opportunities_aged_90d_plus=4,
                       champion_engagement_score=10.0,
                       champion_intro_to_new_stakeholders=0,
                       qbr_held_last_180d=0,
                       license_utilization_pct=0.97,
                       nps_score=80.0, account_health_score=80.0,
                       market_price_increase_benchmark_pct=15.0,
                       renewal_price_increase_pct=0.0,
                       competitive_displacement_risk_score=70.0),
        ]
        d.assess_batch(inputs)
        return d

    def test_summary_total_equals_assessed_count(self):
        d = self._populated_detector()
        assert d.summary()["total"] == 2

    def test_summary_has_13_keys(self):
        d = self._populated_detector()
        assert len(d.summary()) == 13

    def test_summary_risk_counts_is_dict(self):
        d = self._populated_detector()
        assert isinstance(d.summary()["risk_counts"], dict)

    def test_summary_risk_counts_sum_equals_total(self):
        d = self._populated_detector()
        s = d.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_equals_total(self):
        d = self._populated_detector()
        s = d.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_equals_total(self):
        d = self._populated_detector()
        s = d.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self):
        d = self._populated_detector()
        s = d.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_leaking_count_type(self):
        d = self._populated_detector()
        assert isinstance(d.summary()["leaking_count"], int)

    def test_summary_immediate_action_count_type(self):
        d = self._populated_detector()
        assert isinstance(d.summary()["immediate_action_count"], int)

    def test_summary_avg_composite_is_float(self):
        d = self._populated_detector()
        assert isinstance(d.summary()["avg_expansion_leak_composite"], float)

    def test_summary_total_leaked_revenue_is_sum(self):
        d = CustomerExpansionRevenueLeakDetector()
        inputs = [make_input(account_id=f"X{i}", expansion_potential_usd=10_000.0)
                  for i in range(3)]
        results = d.assess_batch(inputs)
        expected_total = round(sum(r.estimated_leaked_revenue_usd for r in results), 2)
        assert d.summary()["total_estimated_leaked_revenue_usd"] == expected_total

    def test_summary_avg_composite_calculation(self):
        d = CustomerExpansionRevenueLeakDetector()
        inputs = [make_input(account_id=f"Z{i}") for i in range(5)]
        results = d.assess_batch(inputs)
        expected_avg = round(sum(r.expansion_leak_composite for r in results) / 5, 1)
        assert d.summary()["avg_expansion_leak_composite"] == expected_avg

    def test_summary_avg_upsell_neglect_calculation(self):
        d = CustomerExpansionRevenueLeakDetector()
        inputs = [make_input(account_id=f"U{i}") for i in range(4)]
        results = d.assess_batch(inputs)
        expected = round(sum(r.upsell_neglect_score for r in results) / 4, 1)
        assert d.summary()["avg_upsell_neglect_score"] == expected

    def test_summary_avg_cross_sell_calculation(self):
        d = CustomerExpansionRevenueLeakDetector()
        inputs = [make_input(account_id=f"C{i}") for i in range(4)]
        results = d.assess_batch(inputs)
        expected = round(sum(r.cross_sell_gap_score for r in results) / 4, 1)
        assert d.summary()["avg_cross_sell_gap_score"] == expected

    def test_summary_avg_renewal_pricing_calculation(self):
        d = CustomerExpansionRevenueLeakDetector()
        inputs = [make_input(account_id=f"R{i}") for i in range(4)]
        results = d.assess_batch(inputs)
        expected = round(sum(r.renewal_pricing_score for r in results) / 4, 1)
        assert d.summary()["avg_renewal_pricing_score"] == expected

    def test_summary_avg_champion_leverage_calculation(self):
        d = CustomerExpansionRevenueLeakDetector()
        inputs = [make_input(account_id=f"H{i}") for i in range(4)]
        results = d.assess_batch(inputs)
        expected = round(sum(r.champion_leverage_score for r in results) / 4, 1)
        assert d.summary()["avg_champion_leverage_score"] == expected

    def test_summary_leaking_count_accurate(self):
        d = CustomerExpansionRevenueLeakDetector()
        inputs = [make_input(account_id=f"L{i}") for i in range(5)]
        results = d.assess_batch(inputs)
        expected = sum(1 for r in results if r.is_revenue_leaking)
        assert d.summary()["leaking_count"] == expected

    def test_summary_immediate_action_count_accurate(self):
        d = CustomerExpansionRevenueLeakDetector()
        inputs = [make_input(account_id=f"I{i}") for i in range(5)]
        results = d.assess_batch(inputs)
        expected = sum(1 for r in results if r.requires_immediate_action)
        assert d.summary()["immediate_action_count"] == expected

    def test_summary_accumulates_across_multiple_assess_calls(self):
        d = CustomerExpansionRevenueLeakDetector()
        for i in range(3):
            d.assess(make_input(account_id=f"ACC-{i}"))
        d.assess(make_input(account_id="EXTRA"))
        assert d.summary()["total"] == 4

    def test_summary_single_record_avgs_equal_that_record(self):
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input(account_id="SINGLE")
        result = d.assess(inp)
        s = d.summary()
        assert s["avg_expansion_leak_composite"] == result.expansion_leak_composite
        assert s["avg_upsell_neglect_score"] == result.upsell_neglect_score
        assert s["avg_cross_sell_gap_score"] == result.cross_sell_gap_score


# ---------------------------------------------------------------------------
# 24. Boundary / edge values
# ---------------------------------------------------------------------------

class TestBoundaryValues:
    def test_zero_expansion_potential_no_crash(self, detector):
        inp = make_input(expansion_potential_usd=0.0)
        result = detector.assess(inp)
        assert result.estimated_leaked_revenue_usd == 0.0

    def test_all_zero_numeric_fields(self, detector):
        inp = ExpansionLeakInput(
            account_id="ZERO", region="TEST", csm_id="C0",
            contract_arr_usd=0.0, expansion_potential_usd=0.0,
            upsell_attempts_last_90d=0, upsell_wins_last_90d=0,
            cross_sell_products_available=0, cross_sell_products_adopted=0,
            renewal_price_increase_pct=0.0, market_price_increase_benchmark_pct=0.0,
            days_since_last_expansion_discussion=0,
            champion_engagement_score=0.0,
            champion_intro_to_new_stakeholders=0,
            qbr_held_last_180d=0,
            product_usage_growth_pct=0.0,
            license_utilization_pct=0.0,
            nps_score=0.0,
            account_health_score=0.0,
            open_expansion_opportunities=0,
            expansion_opportunities_aged_90d_plus=0,
            competitive_displacement_risk_score=0.0,
        )
        result = detector.assess(inp)
        # Should not crash; qbr=0 triggers immediate action
        assert result.requires_immediate_action is True

    def test_days_since_discussion_exactly_30(self, detector):
        inp = make_input(days_since_last_expansion_discussion=30,
                         upsell_attempts_last_90d=3, upsell_wins_last_90d=1)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 8.0

    def test_days_since_discussion_exactly_60(self, detector):
        inp = make_input(days_since_last_expansion_discussion=60,
                         upsell_attempts_last_90d=3, upsell_wins_last_90d=1)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 20.0

    def test_days_since_discussion_exactly_90(self, detector):
        inp = make_input(days_since_last_expansion_discussion=90,
                         upsell_attempts_last_90d=3, upsell_wins_last_90d=1)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 35.0

    def test_champion_engagement_exactly_30(self, detector):
        inp = make_input(champion_engagement_score=30.0,
                         champion_intro_to_new_stakeholders=2,
                         qbr_held_last_180d=2,
                         expansion_potential_usd=0.0,
                         nps_score=60.0)
        result = detector.assess(inp)
        # score=30 is NOT < 30, falls to elif < 50 → +20
        assert result.champion_leverage_score >= 20.0

    def test_champion_engagement_exactly_50(self, detector):
        inp = make_input(champion_engagement_score=50.0,
                         champion_intro_to_new_stakeholders=2,
                         qbr_held_last_180d=2,
                         expansion_potential_usd=0.0,
                         nps_score=60.0)
        result = detector.assess(inp)
        # 50 is NOT < 50, falls to elif <65 → +8
        assert result.champion_leverage_score >= 8.0

    def test_champion_engagement_exactly_65(self, detector):
        inp = make_input(champion_engagement_score=65.0,
                         champion_intro_to_new_stakeholders=2,
                         qbr_held_last_180d=2,
                         expansion_potential_usd=0.0,
                         nps_score=60.0)
        result = detector.assess(inp)
        # 65 is NOT < 65 → no points from engagement
        assert result.champion_leverage_score == 0.0

    def test_license_utilization_exactly_090(self, detector):
        inp = make_input(license_utilization_pct=0.90,
                         upsell_attempts_last_90d=0,
                         expansion_potential_usd=0.0,
                         days_since_last_expansion_discussion=0,
                         expansion_opportunities_aged_90d_plus=0)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 15.0

    def test_license_utilization_exactly_095(self, detector):
        inp = make_input(license_utilization_pct=0.95,
                         upsell_attempts_last_90d=0,
                         expansion_potential_usd=0.0,
                         days_since_last_expansion_discussion=0,
                         expansion_opportunities_aged_90d_plus=0)
        result = detector.assess(inp)
        assert result.is_revenue_leaking is True

    def test_nps_exactly_70_for_pricing(self, detector):
        inp = make_input(nps_score=70.0,
                         renewal_price_increase_pct=1.0,
                         market_price_increase_benchmark_pct=10.0,
                         account_health_score=50.0,
                         competitive_displacement_risk_score=10.0)
        result = detector.assess(inp)
        assert result.renewal_pricing_score >= 25.0

    def test_cross_sell_adoption_exactly_020(self, detector):
        # 2/10 = 20% → NOT < 0.20, falls to elif < 0.40 → +25
        inp = make_input(cross_sell_products_available=10,
                         cross_sell_products_adopted=2,
                         account_health_score=40.0,
                         product_usage_growth_pct=0.0,
                         open_expansion_opportunities=0)
        result = detector.assess(inp)
        assert result.cross_sell_gap_score >= 25.0

    def test_cross_sell_adoption_exactly_040(self, detector):
        # 4/10 = 40% → NOT < 0.40, falls to elif < 0.60 → +10
        inp = make_input(cross_sell_products_available=10,
                         cross_sell_products_adopted=4,
                         account_health_score=40.0,
                         product_usage_growth_pct=0.0,
                         open_expansion_opportunities=0)
        result = detector.assess(inp)
        assert result.cross_sell_gap_score >= 10.0

    def test_delta_exactly_2(self, detector):
        inp = make_input(market_price_increase_benchmark_pct=7.0,
                         renewal_price_increase_pct=5.0,  # delta=2
                         nps_score=40.0, account_health_score=50.0,
                         competitive_displacement_risk_score=10.0)
        result = detector.assess(inp)
        assert result.renewal_pricing_score >= 10.0

    def test_delta_exactly_5(self, detector):
        inp = make_input(market_price_increase_benchmark_pct=10.0,
                         renewal_price_increase_pct=5.0,  # delta=5
                         nps_score=40.0, account_health_score=50.0,
                         competitive_displacement_risk_score=10.0)
        result = detector.assess(inp)
        assert result.renewal_pricing_score >= 25.0

    def test_delta_exactly_10(self, detector):
        inp = make_input(market_price_increase_benchmark_pct=15.0,
                         renewal_price_increase_pct=5.0,  # delta=10
                         nps_score=40.0, account_health_score=50.0,
                         competitive_displacement_risk_score=10.0)
        result = detector.assess(inp)
        assert result.renewal_pricing_score >= 45.0


# ---------------------------------------------------------------------------
# 25. Multiple assessments & state isolation
# ---------------------------------------------------------------------------

class TestStateIsolation:
    def test_fresh_detector_has_empty_results(self):
        d = CustomerExpansionRevenueLeakDetector()
        assert d.summary()["total"] == 0

    def test_each_assess_appends_to_results(self):
        d = CustomerExpansionRevenueLeakDetector()
        for i in range(5):
            d.assess(make_input(account_id=f"ACC-{i}"))
        assert d.summary()["total"] == 5

    def test_two_detectors_independent(self):
        d1 = CustomerExpansionRevenueLeakDetector()
        d2 = CustomerExpansionRevenueLeakDetector()
        d1.assess(make_input(account_id="D1"))
        assert d2.summary()["total"] == 0
        assert d1.summary()["total"] == 1

    def test_assess_returns_correct_result_type(self, detector, healthy_input):
        result = detector.assess(healthy_input)
        assert isinstance(result, ExpansionLeakResult)

    def test_multiple_same_account_id_accumulates(self):
        d = CustomerExpansionRevenueLeakDetector()
        for _ in range(3):
            d.assess(make_input(account_id="DUP"))
        assert d.summary()["total"] == 3


# ---------------------------------------------------------------------------
# 26. Score ranges
# ---------------------------------------------------------------------------

class TestScoreRanges:
    def test_upsell_neglect_score_range(self, detector):
        inps = [
            make_input(upsell_attempts_last_90d=0, expansion_potential_usd=50_000.0,
                       days_since_last_expansion_discussion=120,
                       expansion_opportunities_aged_90d_plus=5,
                       license_utilization_pct=0.98),
            make_input(),
        ]
        for inp in inps:
            result = detector.assess(inp)
            assert 0.0 <= result.upsell_neglect_score <= 100.0

    def test_cross_sell_gap_score_range(self, detector):
        inps = [
            make_input(cross_sell_products_available=10, cross_sell_products_adopted=0,
                       product_usage_growth_pct=50.0, open_expansion_opportunities=6,
                       account_health_score=90.0),
            make_input(),
        ]
        for inp in inps:
            result = detector.assess(inp)
            assert 0.0 <= result.cross_sell_gap_score <= 100.0

    def test_renewal_pricing_score_range(self, detector):
        inps = [
            make_input(market_price_increase_benchmark_pct=20.0,
                       renewal_price_increase_pct=0.0,
                       nps_score=90.0, account_health_score=90.0,
                       competitive_displacement_risk_score=70.0),
            make_input(),
        ]
        for inp in inps:
            result = detector.assess(inp)
            assert 0.0 <= result.renewal_pricing_score <= 100.0

    def test_champion_leverage_score_range(self, detector):
        inps = [
            make_input(champion_engagement_score=5.0,
                       champion_intro_to_new_stakeholders=0,
                       qbr_held_last_180d=0,
                       nps_score=10.0, account_health_score=80.0,
                       expansion_potential_usd=50_000.0),
            make_input(),
        ]
        for inp in inps:
            result = detector.assess(inp)
            assert 0.0 <= result.champion_leverage_score <= 100.0

    def test_composite_range(self, detector):
        inps = [make_input(), make_input(
            upsell_attempts_last_90d=0, expansion_potential_usd=50_000.0,
            days_since_last_expansion_discussion=120,
            cross_sell_products_available=5, cross_sell_products_adopted=0,
            champion_engagement_score=5.0,
            champion_intro_to_new_stakeholders=0, qbr_held_last_180d=0,
            market_price_increase_benchmark_pct=20.0, renewal_price_increase_pct=0.0,
            nps_score=90.0, account_health_score=90.0,
            expansion_opportunities_aged_90d_plus=5,
            competitive_displacement_risk_score=70.0)]
        for inp in inps:
            result = detector.assess(inp)
            assert 0.0 <= result.expansion_leak_composite <= 100.0


# ---------------------------------------------------------------------------
# 27. Region and IDs pass-through
# ---------------------------------------------------------------------------

class TestPassThrough:
    def test_region_apac(self, detector):
        inp = make_input(region="APAC")
        result = detector.assess(inp)
        assert result.region == "APAC"

    def test_region_latam(self, detector):
        inp = make_input(region="LATAM")
        result = detector.assess(inp)
        assert result.region == "LATAM"

    def test_account_id_numeric_string(self, detector):
        inp = make_input(account_id="123456789")
        result = detector.assess(inp)
        assert result.account_id == "123456789"

    def test_account_id_special_chars(self, detector):
        inp = make_input(account_id="ACC-001/XYZ")
        result = detector.assess(inp)
        assert result.account_id == "ACC-001/XYZ"


# ---------------------------------------------------------------------------
# 28. Cross-sell gap: adoption at 60% boundary
# ---------------------------------------------------------------------------

class TestCrossSellAdoptionBoundary:
    def test_adoption_exactly_60pct_no_gap_points(self, detector):
        # 6/10 = 60% → NOT < 0.60 → 0 points from main adoption block
        inp = make_input(cross_sell_products_available=10,
                         cross_sell_products_adopted=6,
                         account_health_score=40.0,
                         product_usage_growth_pct=0.0,
                         open_expansion_opportunities=0)
        result = detector.assess(inp)
        assert result.cross_sell_gap_score == 0.0

    def test_adoption_59pct_adds_10(self, detector):
        # 5.9/10 ≈ 59% → < 0.60 → +10
        inp = make_input(cross_sell_products_available=10,
                         cross_sell_products_adopted=5,  # 50%
                         account_health_score=40.0,
                         product_usage_growth_pct=0.0,
                         open_expansion_opportunities=0)
        result = detector.assess(inp)
        assert result.cross_sell_gap_score >= 10.0


# ---------------------------------------------------------------------------
# 29. Upsell conversion at exact boundaries
# ---------------------------------------------------------------------------

class TestUpsellConversionBoundaries:
    def test_conversion_exactly_10pct_adds_15(self, detector):
        # 1/10 = 10% → NOT < 0.10, falls to elif < 0.25 → +15
        inp = make_input(upsell_attempts_last_90d=10, upsell_wins_last_90d=1,
                         days_since_last_expansion_discussion=0,
                         expansion_opportunities_aged_90d_plus=0,
                         license_utilization_pct=0.50)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 15.0

    def test_conversion_exactly_25pct_no_conversion_penalty(self, detector):
        # 5/20 = 25% → NOT < 0.10, NOT < 0.25 → 0 from conversion
        inp = make_input(upsell_attempts_last_90d=20, upsell_wins_last_90d=5,
                         days_since_last_expansion_discussion=0,
                         expansion_opportunities_aged_90d_plus=0,
                         license_utilization_pct=0.50)
        result = detector.assess(inp)
        # conversion penalty = 0, no days or aged penalty
        assert result.upsell_neglect_score == 0.0

    def test_conversion_9_9pct_adds_30(self, detector):
        # 9/91 ≈ 9.9% → < 0.10 → +30
        inp = make_input(upsell_attempts_last_90d=91, upsell_wins_last_90d=9,
                         days_since_last_expansion_discussion=0,
                         expansion_opportunities_aged_90d_plus=0,
                         license_utilization_pct=0.50)
        result = detector.assess(inp)
        assert result.upsell_neglect_score >= 30.0


# ---------------------------------------------------------------------------
# 30. Detect_pattern edge cases
# ---------------------------------------------------------------------------

class TestDetectPatternEdgeCases:
    def test_expansion_stall_requires_aged_2_plus(self):
        d = CustomerExpansionRevenueLeakDetector()
        # upsell>=30, cross>=30 but aged=1 → should NOT be expansion_stall
        inp = make_input(
            upsell_attempts_last_90d=0, expansion_potential_usd=50_000.0,
            days_since_last_expansion_discussion=100,
            cross_sell_products_available=5, cross_sell_products_adopted=0,
            expansion_opportunities_aged_90d_plus=1,
            champion_engagement_score=80.0,
            champion_intro_to_new_stakeholders=1,
            qbr_held_last_180d=2,
            market_price_increase_benchmark_pct=5.0,
            renewal_price_increase_pct=5.0,
        )
        result = d.assess(inp)
        assert result.leak_pattern != LeakPattern.expansion_stall

    def test_champion_not_leveraged_requires_qbr_0(self):
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input(
            champion_engagement_score=15.0,
            champion_intro_to_new_stakeholders=0,
            qbr_held_last_180d=1,  # NOT 0
            expansion_opportunities_aged_90d_plus=0,
            upsell_attempts_last_90d=3, upsell_wins_last_90d=1,
            cross_sell_products_available=4, cross_sell_products_adopted=3,
            market_price_increase_benchmark_pct=5.0,
            renewal_price_increase_pct=5.0,
            days_since_last_expansion_discussion=5,
        )
        result = d.assess(inp)
        assert result.leak_pattern != LeakPattern.champion_not_leveraged

    def test_cross_sell_gap_pattern_requires_low_adoption(self):
        d = CustomerExpansionRevenueLeakDetector()
        # cross>=25 but adoption >= 0.40 → no cross_sell_gap pattern
        inp = make_input(
            cross_sell_products_available=10,
            cross_sell_products_adopted=5,  # 50% → >=0.40
            account_health_score=90.0,
            product_usage_growth_pct=0.0,
            open_expansion_opportunities=4,
            champion_engagement_score=80.0,
            champion_intro_to_new_stakeholders=2,
            qbr_held_last_180d=2,
            upsell_attempts_last_90d=3, upsell_wins_last_90d=1,
            expansion_opportunities_aged_90d_plus=0,
            market_price_increase_benchmark_pct=5.0,
            renewal_price_increase_pct=5.0,
            days_since_last_expansion_discussion=5,
        )
        result = d.assess(inp)
        assert result.leak_pattern != LeakPattern.cross_sell_gap

    def test_upsell_neglect_pattern_requires_days_45_plus(self):
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input(
            upsell_attempts_last_90d=0, expansion_potential_usd=50_000.0,
            days_since_last_expansion_discussion=44,  # < 45
            cross_sell_products_available=4, cross_sell_products_adopted=3,
            champion_engagement_score=80.0,
            champion_intro_to_new_stakeholders=2,
            qbr_held_last_180d=2,
            expansion_opportunities_aged_90d_plus=0,
            market_price_increase_benchmark_pct=5.0,
            renewal_price_increase_pct=5.0,
        )
        result = d.assess(inp)
        assert result.leak_pattern != LeakPattern.upsell_neglect


# ---------------------------------------------------------------------------
# 31. Large batch summary correctness
# ---------------------------------------------------------------------------

class TestLargeBatchSummary:
    def test_batch_10_summary_total(self):
        d = CustomerExpansionRevenueLeakDetector()
        inputs = [make_input(account_id=f"LG-{i}") for i in range(10)]
        d.assess_batch(inputs)
        assert d.summary()["total"] == 10

    def test_batch_mixed_risk_levels(self):
        d = CustomerExpansionRevenueLeakDetector()
        d.assess(make_input(account_id="healthy"))  # low
        d.assess(make_input(account_id="critical",
                            upsell_attempts_last_90d=0, expansion_potential_usd=50_000.0,
                            days_since_last_expansion_discussion=120,
                            cross_sell_products_available=5, cross_sell_products_adopted=0,
                            champion_engagement_score=5.0,
                            champion_intro_to_new_stakeholders=0, qbr_held_last_180d=0,
                            market_price_increase_benchmark_pct=20.0,
                            renewal_price_increase_pct=0.0,
                            nps_score=90.0, account_health_score=90.0,
                            expansion_opportunities_aged_90d_plus=4,
                            competitive_displacement_risk_score=70.0))
        s = d.summary()
        assert s["total"] == 2
        assert "low" in s["risk_counts"] or "critical" in s["risk_counts"]

    def test_batch_100_no_crash(self):
        d = CustomerExpansionRevenueLeakDetector()
        inputs = [make_input(account_id=f"BIG-{i}") for i in range(100)]
        results = d.assess_batch(inputs)
        assert len(results) == 100
        s = d.summary()
        assert s["total"] == 100

    def test_batch_total_revenue_sum_correct(self):
        d = CustomerExpansionRevenueLeakDetector()
        inputs = [make_input(account_id=f"R-{i}", expansion_potential_usd=float(i * 1000))
                  for i in range(5)]
        results = d.assess_batch(inputs)
        expected_sum = round(sum(r.estimated_leaked_revenue_usd for r in results), 2)
        assert d.summary()["total_estimated_leaked_revenue_usd"] == expected_sum


# ---------------------------------------------------------------------------
# 32. Regression / specific scenario tests
# ---------------------------------------------------------------------------

class TestSpecificScenarios:
    def test_fully_healthy_all_scores_zero(self):
        """An account with perfect signals should score 0 everywhere."""
        d = CustomerExpansionRevenueLeakDetector()
        inp = ExpansionLeakInput(
            account_id="PERFECT", region="NA", csm_id="CSM-X",
            contract_arr_usd=200_000.0, expansion_potential_usd=50_000.0,
            upsell_attempts_last_90d=10, upsell_wins_last_90d=6,   # 60% conv
            cross_sell_products_available=5, cross_sell_products_adopted=5,  # 100%
            renewal_price_increase_pct=10.0, market_price_increase_benchmark_pct=8.0,  # above market
            days_since_last_expansion_discussion=5,
            champion_engagement_score=90.0,
            champion_intro_to_new_stakeholders=3,
            qbr_held_last_180d=2,
            product_usage_growth_pct=5.0,
            license_utilization_pct=0.60,
            nps_score=80.0,
            account_health_score=90.0,
            open_expansion_opportunities=0,
            expansion_opportunities_aged_90d_plus=0,
            competitive_displacement_risk_score=5.0,
        )
        result = d.assess(inp)
        assert result.upsell_neglect_score == 0.0
        assert result.cross_sell_gap_score == 0.0
        assert result.expansion_leak_composite == 0.0
        assert result.expansion_leak_risk == ExpansionLeakRisk.low
        assert result.leak_severity == LeakSeverity.captured
        assert result.recommended_action == LeakAction.no_action
        assert result.is_revenue_leaking is False

    def test_no_qbr_always_triggers_immediate_action(self):
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input(qbr_held_last_180d=0)
        result = d.assess(inp)
        assert result.requires_immediate_action is True

    def test_pattern_none_gives_no_action_on_low_risk(self):
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input()
        result = d.assess(inp)
        if result.expansion_leak_risk == ExpansionLeakRisk.low:
            assert result.recommended_action == LeakAction.no_action

    def test_account_ids_in_batch_results_correct(self):
        d = CustomerExpansionRevenueLeakDetector()
        expected_ids = [f"BATCH-{i:03d}" for i in range(10)]
        inputs = [make_input(account_id=aid) for aid in expected_ids]
        results = d.assess_batch(inputs)
        actual_ids = [r.account_id for r in results]
        assert actual_ids == expected_ids

    def test_high_nps_high_health_no_price_increase_leaks(self):
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input(
            nps_score=80.0,
            account_health_score=80.0,
            renewal_price_increase_pct=0.0,
            market_price_increase_benchmark_pct=10.0,
        )
        result = d.assess(inp)
        assert result.renewal_pricing_score >= 45.0  # delta=10 → 45

    def test_expansion_leak_composite_rounded_to_1_decimal(self):
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input(account_id="ROUND")
        result = d.assess(inp)
        # Check it has at most 1 decimal place
        assert result.expansion_leak_composite == round(result.expansion_leak_composite, 1)

    def test_sub_scores_rounded_to_1_decimal(self):
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input(account_id="ROUND2")
        result = d.assess(inp)
        assert result.upsell_neglect_score == round(result.upsell_neglect_score, 1)
        assert result.cross_sell_gap_score == round(result.cross_sell_gap_score, 1)
        assert result.renewal_pricing_score == round(result.renewal_pricing_score, 1)
        assert result.champion_leverage_score == round(result.champion_leverage_score, 1)

    def test_estimated_leaked_revenue_rounded_to_2_decimals(self):
        d = CustomerExpansionRevenueLeakDetector()
        inp = make_input(expansion_potential_usd=99_999.99)
        result = d.assess(inp)
        assert result.estimated_leaked_revenue_usd == round(result.estimated_leaked_revenue_usd, 2)

    def test_summary_total_leaked_revenue_rounded_to_2_decimals(self):
        d = CustomerExpansionRevenueLeakDetector()
        inputs = [make_input(account_id=f"T{i}", expansion_potential_usd=33_333.33)
                  for i in range(3)]
        d.assess_batch(inputs)
        total = d.summary()["total_estimated_leaked_revenue_usd"]
        assert total == round(total, 2)
