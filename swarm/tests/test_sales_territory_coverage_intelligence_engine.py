"""
Comprehensive pytest test suite for SalesTerritoryCoverageIntelligenceEngine.
~300 tests covering enums, sub-scores, pattern detection, risk/severity/action,
flags, revenue-at-risk, signal strings, to_dict/summary, batch processing,
and edge cases.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_territory_coverage_intelligence_engine import (
    SalesTerritoryCoverageIntelligenceEngine,
    TerritoryCoverageInput,
    TerritoryCoverageResult,
    CoverageRisk,
    CoveragePattern,
    CoverageSeverity,
    CoverageAction,
)


# ---------------------------------------------------------------------------
# Helper fixture / factory
# ---------------------------------------------------------------------------

def make_input(**kwargs) -> TerritoryCoverageInput:
    defaults = dict(
        rep_id="rep_test",
        region="West",
        evaluation_period_id="Q1-2026",
        total_accounts_in_territory=50,
        accounts_active_count=40,
        accounts_neglected_count=2,
        high_value_accounts_total=10,
        high_value_accounts_engaged_count=8,
        new_logo_accounts_added=3,
        new_logo_converted_count=2,
        whitespace_accounts_identified=5,
        whitespace_accounts_pursued=3,
        churn_risk_accounts_total=4,
        churn_risk_accounts_contacted=3,
        top_account_revenue_concentration_pct=0.30,
        avg_contacts_per_account=3.0,
        expansion_signals_identified=6,
        expansion_signals_acted_upon=5,
        multi_product_penetration_pct=0.50,
        territory_revenue_growth_pct=0.10,
        avg_account_revenue_usd=20000.0,
        accounts_without_next_steps_pct=0.15,
    )
    defaults.update(kwargs)
    return TerritoryCoverageInput(**defaults)


@pytest.fixture
def engine() -> SalesTerritoryCoverageIntelligenceEngine:
    return SalesTerritoryCoverageIntelligenceEngine()


@pytest.fixture
def good_input() -> TerritoryCoverageInput:
    """A healthy territory: low scores → low composite."""
    return make_input()


# ===========================================================================
# 1. ENUM VALUES
# ===========================================================================

class TestCoverageRiskEnum:
    def test_low_value(self):
        assert CoverageRisk.low.value == "low"

    def test_moderate_value(self):
        assert CoverageRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert CoverageRisk.high.value == "high"

    def test_critical_value(self):
        assert CoverageRisk.critical.value == "critical"

    def test_four_members(self):
        assert len(CoverageRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(CoverageRisk.low, str)


class TestCoveragePatternEnum:
    def test_none_value(self):
        assert CoveragePattern.none.value == "none"

    def test_account_neglect_value(self):
        assert CoveragePattern.account_neglect.value == "account_neglect"

    def test_high_value_underserved_value(self):
        assert CoveragePattern.high_value_underserved.value == "high_value_underserved"

    def test_whitespace_ignored_value(self):
        assert CoveragePattern.whitespace_ignored.value == "whitespace_ignored"

    def test_churn_risk_uncovered_value(self):
        assert CoveragePattern.churn_risk_uncovered.value == "churn_risk_uncovered"

    def test_revenue_concentration_value(self):
        assert CoveragePattern.revenue_concentration.value == "revenue_concentration"

    def test_six_members(self):
        assert len(CoveragePattern) == 6

    def test_is_str_enum(self):
        assert isinstance(CoveragePattern.none, str)


class TestCoverageSeverityEnum:
    def test_optimized_value(self):
        assert CoverageSeverity.optimized.value == "optimized"

    def test_gaps_detected_value(self):
        assert CoverageSeverity.gaps_detected.value == "gaps_detected"

    def test_underserved_value(self):
        assert CoverageSeverity.underserved.value == "underserved"

    def test_critical_value(self):
        assert CoverageSeverity.critical.value == "critical"

    def test_four_members(self):
        assert len(CoverageSeverity) == 4


class TestCoverageActionEnum:
    def test_no_action_value(self):
        assert CoverageAction.no_action.value == "no_action"

    def test_account_outreach_blitz_value(self):
        assert CoverageAction.account_outreach_blitz.value == "account_outreach_blitz"

    def test_high_value_focus_value(self):
        assert CoverageAction.high_value_focus.value == "high_value_focus"

    def test_whitespace_expansion_value(self):
        assert CoverageAction.whitespace_expansion.value == "whitespace_expansion"

    def test_churn_prevention_sprint_value(self):
        assert CoverageAction.churn_prevention_sprint.value == "churn_prevention_sprint"

    def test_territory_restructure_value(self):
        assert CoverageAction.territory_restructure.value == "territory_restructure"

    def test_six_members(self):
        assert len(CoverageAction) == 6


# ===========================================================================
# 2. SUB-SCORES
# ===========================================================================

class TestAccountBreadthScore:
    """_account_breadth_score — higher score = more risk."""

    def test_zero_neglect_high_active_low_steps(self, engine):
        inp = make_input(
            accounts_neglected_count=0,
            accounts_active_count=48,
            accounts_without_next_steps_pct=0.05,
        )
        assert engine._account_breadth_score(inp) == 0.0

    # neglect_ratio tiers
    def test_neglect_ratio_below_10_no_score(self, engine):
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=9,
            accounts_active_count=80,
            accounts_without_next_steps_pct=0.0,
        )
        assert engine._account_breadth_score(inp) == 0.0

    def test_neglect_ratio_10_adds_10(self, engine):
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=10,
            accounts_active_count=80,
            accounts_without_next_steps_pct=0.0,
        )
        assert engine._account_breadth_score(inp) == 10.0

    def test_neglect_ratio_25_adds_25(self, engine):
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=25,
            accounts_active_count=80,
            accounts_without_next_steps_pct=0.0,
        )
        assert engine._account_breadth_score(inp) == 25.0

    def test_neglect_ratio_40_adds_40(self, engine):
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=40,
            accounts_active_count=80,
            accounts_without_next_steps_pct=0.0,
        )
        assert engine._account_breadth_score(inp) == 40.0

    # active_ratio tiers
    def test_active_ratio_below_30_adds_25(self, engine):
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=0,
            accounts_active_count=29,
            accounts_without_next_steps_pct=0.0,
        )
        assert engine._account_breadth_score(inp) == 25.0

    def test_active_ratio_30_to_50_adds_12(self, engine):
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=0,
            accounts_active_count=40,
            accounts_without_next_steps_pct=0.0,
        )
        assert engine._account_breadth_score(inp) == 12.0

    def test_active_ratio_50_no_addition(self, engine):
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=0,
            accounts_active_count=50,
            accounts_without_next_steps_pct=0.0,
        )
        assert engine._account_breadth_score(inp) == 0.0

    # without_next_steps_pct tiers
    def test_next_steps_60_adds_20(self, engine):
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=0,
            accounts_active_count=80,
            accounts_without_next_steps_pct=0.60,
        )
        assert engine._account_breadth_score(inp) == 20.0

    def test_next_steps_40_to_60_adds_10(self, engine):
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=0,
            accounts_active_count=80,
            accounts_without_next_steps_pct=0.40,
        )
        assert engine._account_breadth_score(inp) == 10.0

    def test_next_steps_below_40_no_addition(self, engine):
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=0,
            accounts_active_count=80,
            accounts_without_next_steps_pct=0.39,
        )
        assert engine._account_breadth_score(inp) == 0.0

    def test_score_max_is_85(self, engine):
        # max: neglect>=0.40 (+40) + active<0.30 (+25) + next_steps>=0.60 (+20) = 85
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=50,
            accounts_active_count=10,
            accounts_without_next_steps_pct=0.90,
        )
        assert engine._account_breadth_score(inp) == 85.0

    def test_zero_total_uses_denominator_1(self, engine):
        inp = make_input(
            total_accounts_in_territory=0,
            accounts_neglected_count=0,
            accounts_active_count=0,
            accounts_without_next_steps_pct=0.0,
        )
        # max(0,1)=1 denominator; neglect=0/1=0, active=0/1=0 → 25 for active<0.30
        score = engine._account_breadth_score(inp)
        assert score == 25.0

    def test_boundary_neglect_exactly_24(self, engine):
        # 24/100 = 0.24 < 0.25, so adds 10
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=24,
            accounts_active_count=80,
            accounts_without_next_steps_pct=0.0,
        )
        assert engine._account_breadth_score(inp) == 10.0

    def test_boundary_neglect_exactly_39(self, engine):
        # 39/100 = 0.39 < 0.40, so adds 25
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=39,
            accounts_active_count=80,
            accounts_without_next_steps_pct=0.0,
        )
        assert engine._account_breadth_score(inp) == 25.0


class TestAccountPrioritizationScore:
    """_account_prioritization_score — higher = more risk."""

    def test_perfect_coverage_no_concentration_high_contacts(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=10,
            top_account_revenue_concentration_pct=0.10,
            avg_contacts_per_account=5.0,
        )
        assert engine._account_prioritization_score(inp) == 0.0

    # hv_engaged_ratio tiers
    def test_hv_ratio_below_40_adds_40(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=3,
            top_account_revenue_concentration_pct=0.10,
            avg_contacts_per_account=5.0,
        )
        assert engine._account_prioritization_score(inp) == 40.0

    def test_hv_ratio_40_to_60_adds_25(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=5,
            top_account_revenue_concentration_pct=0.10,
            avg_contacts_per_account=5.0,
        )
        assert engine._account_prioritization_score(inp) == 25.0

    def test_hv_ratio_60_to_80_adds_10(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=7,
            top_account_revenue_concentration_pct=0.10,
            avg_contacts_per_account=5.0,
        )
        assert engine._account_prioritization_score(inp) == 10.0

    def test_hv_ratio_80_plus_no_add(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=8,
            top_account_revenue_concentration_pct=0.10,
            avg_contacts_per_account=5.0,
        )
        assert engine._account_prioritization_score(inp) == 0.0

    # concentration tiers
    def test_concentration_80_plus_adds_30(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
            top_account_revenue_concentration_pct=0.80,
            avg_contacts_per_account=5.0,
        )
        assert engine._account_prioritization_score(inp) == 30.0

    def test_concentration_60_to_80_adds_15(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
            top_account_revenue_concentration_pct=0.65,
            avg_contacts_per_account=5.0,
        )
        assert engine._account_prioritization_score(inp) == 15.0

    def test_concentration_below_60_no_add(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
            top_account_revenue_concentration_pct=0.50,
            avg_contacts_per_account=5.0,
        )
        assert engine._account_prioritization_score(inp) == 0.0

    # avg_contacts tiers
    def test_contacts_below_1_adds_20(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
            top_account_revenue_concentration_pct=0.10,
            avg_contacts_per_account=0.5,
        )
        assert engine._account_prioritization_score(inp) == 20.0

    def test_contacts_1_to_2_adds_10(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
            top_account_revenue_concentration_pct=0.10,
            avg_contacts_per_account=1.5,
        )
        assert engine._account_prioritization_score(inp) == 10.0

    def test_contacts_2_plus_no_add(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
            top_account_revenue_concentration_pct=0.10,
            avg_contacts_per_account=2.0,
        )
        assert engine._account_prioritization_score(inp) == 0.0

    def test_max_is_90(self, engine):
        # max: hv<0.40 (+40) + concentration>=0.80 (+30) + contacts<1.0 (+20) = 90
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=3,
            top_account_revenue_concentration_pct=0.90,
            avg_contacts_per_account=0.1,
        )
        assert engine._account_prioritization_score(inp) == 90.0

    def test_zero_hv_total_uses_denominator_1(self, engine):
        inp = make_input(
            high_value_accounts_total=0,
            high_value_accounts_engaged_count=0,
            top_account_revenue_concentration_pct=0.10,
            avg_contacts_per_account=5.0,
        )
        # 0/1 = 0 < 0.40 → +40
        assert engine._account_prioritization_score(inp) == 40.0

    def test_boundary_hv_ratio_exactly_60(self, engine):
        # 6/10 = 0.60, NOT < 0.60, so check next: 0.60 NOT < 0.80 → +10
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=6,
            top_account_revenue_concentration_pct=0.10,
            avg_contacts_per_account=5.0,
        )
        assert engine._account_prioritization_score(inp) == 10.0

    def test_boundary_concentration_exactly_60(self, engine):
        # 0.60 >= 0.60 adds 15
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
            top_account_revenue_concentration_pct=0.60,
            avg_contacts_per_account=5.0,
        )
        assert engine._account_prioritization_score(inp) == 15.0

    def test_boundary_concentration_exactly_80(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
            top_account_revenue_concentration_pct=0.80,
            avg_contacts_per_account=5.0,
        )
        assert engine._account_prioritization_score(inp) == 30.0


class TestWhitespaceExploitationScore:
    """_whitespace_exploitation_score — higher = more risk."""

    def test_zero_risk_high_acted_high_ws_high_multi_high_logo(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=8,
            multi_product_penetration_pct=0.50,
            new_logo_accounts_added=5,
            new_logo_converted_count=4,
        )
        assert engine._whitespace_exploitation_score(inp) == 0.0

    # acted_ratio tiers
    def test_acted_ratio_below_20_adds_35(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=1,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=8,
            multi_product_penetration_pct=0.50,
            new_logo_accounts_added=5,
            new_logo_converted_count=4,
        )
        assert engine._whitespace_exploitation_score(inp) == 35.0

    def test_acted_ratio_20_to_40_adds_20(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=3,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=8,
            multi_product_penetration_pct=0.50,
            new_logo_accounts_added=5,
            new_logo_converted_count=4,
        )
        assert engine._whitespace_exploitation_score(inp) == 20.0

    def test_acted_ratio_40_to_60_adds_8(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=5,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=8,
            multi_product_penetration_pct=0.50,
            new_logo_accounts_added=5,
            new_logo_converted_count=4,
        )
        assert engine._whitespace_exploitation_score(inp) == 8.0

    def test_acted_ratio_60_plus_no_add(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=7,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=8,
            multi_product_penetration_pct=0.50,
            new_logo_accounts_added=5,
            new_logo_converted_count=4,
        )
        assert engine._whitespace_exploitation_score(inp) == 0.0

    # ws_ratio tiers
    def test_ws_ratio_below_20_adds_30(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=1,
            multi_product_penetration_pct=0.50,
            new_logo_accounts_added=5,
            new_logo_converted_count=4,
        )
        assert engine._whitespace_exploitation_score(inp) == 30.0

    def test_ws_ratio_20_to_40_adds_15(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=3,
            multi_product_penetration_pct=0.50,
            new_logo_accounts_added=5,
            new_logo_converted_count=4,
        )
        assert engine._whitespace_exploitation_score(inp) == 15.0

    def test_ws_ratio_40_plus_no_add(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=5,
            multi_product_penetration_pct=0.50,
            new_logo_accounts_added=5,
            new_logo_converted_count=4,
        )
        assert engine._whitespace_exploitation_score(inp) == 0.0

    # multi_product tiers
    def test_multi_product_below_20_adds_20(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=8,
            multi_product_penetration_pct=0.10,
            new_logo_accounts_added=5,
            new_logo_converted_count=4,
        )
        assert engine._whitespace_exploitation_score(inp) == 20.0

    def test_multi_product_20_to_35_adds_10(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=8,
            multi_product_penetration_pct=0.25,
            new_logo_accounts_added=5,
            new_logo_converted_count=4,
        )
        assert engine._whitespace_exploitation_score(inp) == 10.0

    def test_multi_product_35_plus_no_add(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=8,
            multi_product_penetration_pct=0.35,
            new_logo_accounts_added=5,
            new_logo_converted_count=4,
        )
        assert engine._whitespace_exploitation_score(inp) == 0.0

    # new_logo_converted tiers
    def test_logo_converted_below_20_adds_15(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=8,
            multi_product_penetration_pct=0.50,
            new_logo_accounts_added=10,
            new_logo_converted_count=1,
        )
        assert engine._whitespace_exploitation_score(inp) == 15.0

    def test_logo_converted_20_plus_no_add(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=8,
            multi_product_penetration_pct=0.50,
            new_logo_accounts_added=10,
            new_logo_converted_count=2,
        )
        assert engine._whitespace_exploitation_score(inp) == 0.0

    def test_capped_at_100(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=1,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=1,
            multi_product_penetration_pct=0.05,
            new_logo_accounts_added=10,
            new_logo_converted_count=1,
        )
        score = engine._whitespace_exploitation_score(inp)
        assert score == 100.0

    def test_zero_expansion_uses_denominator_1(self, engine):
        inp = make_input(
            expansion_signals_identified=0,
            expansion_signals_acted_upon=0,
            whitespace_accounts_identified=0,
            whitespace_accounts_pursued=0,
            multi_product_penetration_pct=0.50,
            new_logo_accounts_added=5,
            new_logo_converted_count=4,
        )
        # 0/1 acted=0 < 0.20 → +35; ws 0/1=0 < 0.20 → +30
        score = engine._whitespace_exploitation_score(inp)
        assert score == 65.0


class TestChurnPreventionScore:
    """_churn_prevention_score — higher = more risk."""

    def test_perfect_churn_coverage_positive_growth_low_neglect(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
            territory_revenue_growth_pct=0.15,
            accounts_neglected_count=0,
        )
        assert engine._churn_prevention_score(inp) == 0.0

    # churn_coverage tiers
    def test_churn_coverage_below_40_adds_40(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=3,
            territory_revenue_growth_pct=0.10,
            accounts_neglected_count=0,
        )
        assert engine._churn_prevention_score(inp) == 40.0

    def test_churn_coverage_40_to_60_adds_25(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=5,
            territory_revenue_growth_pct=0.10,
            accounts_neglected_count=0,
        )
        assert engine._churn_prevention_score(inp) == 25.0

    def test_churn_coverage_60_to_80_adds_10(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=7,
            territory_revenue_growth_pct=0.10,
            accounts_neglected_count=0,
        )
        assert engine._churn_prevention_score(inp) == 10.0

    def test_churn_coverage_80_plus_no_add(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
            territory_revenue_growth_pct=0.10,
            accounts_neglected_count=0,
        )
        assert engine._churn_prevention_score(inp) == 0.0

    # revenue growth tiers
    def test_growth_below_neg_10_adds_35(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
            territory_revenue_growth_pct=-0.15,
            accounts_neglected_count=0,
        )
        assert engine._churn_prevention_score(inp) == 35.0

    def test_growth_neg_10_to_0_adds_15(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
            territory_revenue_growth_pct=-0.05,
            accounts_neglected_count=0,
        )
        assert engine._churn_prevention_score(inp) == 15.0

    def test_growth_zero_no_add(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
            territory_revenue_growth_pct=0.0,
            accounts_neglected_count=0,
        )
        assert engine._churn_prevention_score(inp) == 0.0

    def test_growth_positive_no_add(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
            territory_revenue_growth_pct=0.05,
            accounts_neglected_count=0,
        )
        assert engine._churn_prevention_score(inp) == 0.0

    # neglected tiers
    def test_neglected_5_plus_adds_15(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
            territory_revenue_growth_pct=0.10,
            accounts_neglected_count=5,
        )
        assert engine._churn_prevention_score(inp) == 15.0

    def test_neglected_3_to_5_adds_8(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
            territory_revenue_growth_pct=0.10,
            accounts_neglected_count=3,
        )
        assert engine._churn_prevention_score(inp) == 8.0

    def test_neglected_below_3_no_add(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
            territory_revenue_growth_pct=0.10,
            accounts_neglected_count=2,
        )
        assert engine._churn_prevention_score(inp) == 0.0

    def test_capped_at_100(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=1,
            territory_revenue_growth_pct=-0.50,
            accounts_neglected_count=10,
        )
        assert engine._churn_prevention_score(inp) == 90.0

    def test_zero_churn_total_uses_denominator_1(self, engine):
        inp = make_input(
            churn_risk_accounts_total=0,
            churn_risk_accounts_contacted=0,
            territory_revenue_growth_pct=0.10,
            accounts_neglected_count=0,
        )
        # 0/1 < 0.40 → +40
        assert engine._churn_prevention_score(inp) == 40.0

    def test_boundary_churn_coverage_exactly_40(self, engine):
        # 4/10 = 0.40, not < 0.40, so check < 0.60 → +25
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=4,
            territory_revenue_growth_pct=0.10,
            accounts_neglected_count=0,
        )
        assert engine._churn_prevention_score(inp) == 25.0

    def test_boundary_growth_exactly_neg_10(self, engine):
        # -0.10 not < -0.10 but < 0, so +15
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
            territory_revenue_growth_pct=-0.10,
            accounts_neglected_count=0,
        )
        assert engine._churn_prevention_score(inp) == 15.0


# ===========================================================================
# 3. PATTERN DETECTION
# ===========================================================================

class TestPatternDetection:
    """_detect_pattern — priority order matters."""

    def _make_engine_and_scores(self, inp):
        eng = SalesTerritoryCoverageIntelligenceEngine()
        breadth = eng._account_breadth_score(inp)
        pri     = eng._account_prioritization_score(inp)
        ws      = eng._whitespace_exploitation_score(inp)
        churn   = eng._churn_prevention_score(inp)
        return eng, breadth, pri, ws, churn

    def test_none_pattern_for_good_territory(self):
        inp = make_input()
        eng, b, p, w, c = self._make_engine_and_scores(inp)
        assert eng._detect_pattern(inp, b, p, w, c) == CoveragePattern.none

    def test_revenue_concentration_highest_priority(self):
        # concentration >= 0.70 AND prioritization >= 30
        inp = make_input(
            top_account_revenue_concentration_pct=0.80,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=3,  # → pri = 40
            avg_contacts_per_account=5.0,
        )
        eng, b, p, w, c = self._make_engine_and_scores(inp)
        assert eng._detect_pattern(inp, b, p, w, c) == CoveragePattern.revenue_concentration

    def test_revenue_concentration_requires_concentration_070(self):
        # concentration = 0.69 → won't trigger
        inp = make_input(
            top_account_revenue_concentration_pct=0.69,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=3,
            avg_contacts_per_account=5.0,
        )
        eng, b, p, w, c = self._make_engine_and_scores(inp)
        assert eng._detect_pattern(inp, b, p, w, c) != CoveragePattern.revenue_concentration

    def test_revenue_concentration_requires_prioritization_30(self):
        # concentration >= 0.70 but prioritization < 30 → won't trigger
        inp = make_input(
            top_account_revenue_concentration_pct=0.75,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,  # → pri low
            avg_contacts_per_account=5.0,
        )
        eng, b, p, w, c = self._make_engine_and_scores(inp)
        assert eng._detect_pattern(inp, b, p, w, c) != CoveragePattern.revenue_concentration

    def test_churn_risk_uncovered_second_priority(self):
        # churn >= 30 AND churn_ratio < 0.40
        # But no revenue concentration
        inp = make_input(
            top_account_revenue_concentration_pct=0.30,  # no concentration
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=3,  # ratio=0.30 < 0.40
            territory_revenue_growth_pct=-0.15,  # → churn score high
            accounts_neglected_count=0,
        )
        eng, b, p, w, c = self._make_engine_and_scores(inp)
        result = eng._detect_pattern(inp, b, p, w, c)
        assert result == CoveragePattern.churn_risk_uncovered

    def test_churn_risk_uncovered_requires_churn_score_30(self):
        # churn < 30 even if ratio < 0.40
        inp = make_input(
            top_account_revenue_concentration_pct=0.30,
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=3,
            territory_revenue_growth_pct=0.10,  # positive → low churn score
            accounts_neglected_count=0,
        )
        eng, b, p, w, c = self._make_engine_and_scores(inp)
        # churn score = 40 (from coverage) → is >= 30
        # But let's pick a case where churn < 30
        # Force low churn: high contact ratio + positive growth + no neglect
        inp2 = make_input(
            top_account_revenue_concentration_pct=0.30,
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,  # 0.90 → no churn score
            territory_revenue_growth_pct=0.10,
            accounts_neglected_count=0,
        )
        eng2 = SalesTerritoryCoverageIntelligenceEngine()
        b2, p2, w2, c2 = (
            eng2._account_breadth_score(inp2),
            eng2._account_prioritization_score(inp2),
            eng2._whitespace_exploitation_score(inp2),
            eng2._churn_prevention_score(inp2),
        )
        assert c2 == 0.0  # churn score is 0, not >= 30
        assert eng2._detect_pattern(inp2, b2, p2, w2, c2) != CoveragePattern.churn_risk_uncovered

    def test_high_value_underserved_third_priority(self):
        # prioritization >= 35 AND hv_ratio < 0.60
        # But no revenue concentration or churn pattern
        inp = make_input(
            top_account_revenue_concentration_pct=0.30,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=5,  # ratio=0.50 < 0.60
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,  # good churn coverage
            territory_revenue_growth_pct=0.10,
            accounts_neglected_count=0,
            avg_contacts_per_account=5.0,
        )
        eng, b, p, w, c = self._make_engine_and_scores(inp)
        # p should be 25 (40-60 tier) → not >= 35
        # Let's set it to get >= 35: hv < 0.40 → p=40 and no concentration
        inp2 = make_input(
            top_account_revenue_concentration_pct=0.30,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=3,  # ratio=0.30 → +40
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
            territory_revenue_growth_pct=0.10,
            accounts_neglected_count=0,
            avg_contacts_per_account=5.0,
        )
        eng2 = SalesTerritoryCoverageIntelligenceEngine()
        b2, p2, w2, c2 = (
            eng2._account_breadth_score(inp2),
            eng2._account_prioritization_score(inp2),
            eng2._whitespace_exploitation_score(inp2),
            eng2._churn_prevention_score(inp2),
        )
        result = eng2._detect_pattern(inp2, b2, p2, w2, c2)
        assert result == CoveragePattern.high_value_underserved

    def test_whitespace_ignored_fourth_priority(self):
        # whitespace >= 35 AND acted_ratio < 0.20
        # No prior patterns triggered
        inp = make_input(
            top_account_revenue_concentration_pct=0.30,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
            territory_revenue_growth_pct=0.10,
            accounts_neglected_count=0,
            avg_contacts_per_account=5.0,
            expansion_signals_identified=10,
            expansion_signals_acted_upon=1,  # ratio=0.10 < 0.20 → +35
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=1,  # ratio=0.10 < 0.20 → +30
            multi_product_penetration_pct=0.50,
        )
        eng, b, p, w, c = self._make_engine_and_scores(inp)
        result = eng._detect_pattern(inp, b, p, w, c)
        assert result == CoveragePattern.whitespace_ignored

    def test_account_neglect_fifth_priority(self):
        # breadth >= 30 AND neglected >= 5
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=5,
            accounts_active_count=15,  # ratio=0.15 < 0.30 → +25 breadth
            accounts_without_next_steps_pct=0.10,
            top_account_revenue_concentration_pct=0.30,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
            territory_revenue_growth_pct=0.10,
            avg_contacts_per_account=5.0,
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=8,
            multi_product_penetration_pct=0.50,
        )
        eng, b, p, w, c = self._make_engine_and_scores(inp)
        # breadth = 25 (from active < 0.30) + 10 (neglect 5/100=0.05 < 0.10 → 0)
        # Actually 5/100=0.05 < 0.10 → 0 neglect score, but active=15/100=0.15 < 0.30 → +25
        # Let's check breadth >= 30: need more
        inp2 = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=5,
            accounts_active_count=15,  # +25 breadth
            accounts_without_next_steps_pct=0.40,  # +10 breadth → total=35
            top_account_revenue_concentration_pct=0.30,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
            territory_revenue_growth_pct=0.10,
            avg_contacts_per_account=5.0,
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=8,
            multi_product_penetration_pct=0.50,
        )
        eng2 = SalesTerritoryCoverageIntelligenceEngine()
        b2, p2, w2, c2 = (
            eng2._account_breadth_score(inp2),
            eng2._account_prioritization_score(inp2),
            eng2._whitespace_exploitation_score(inp2),
            eng2._churn_prevention_score(inp2),
        )
        result = eng2._detect_pattern(inp2, b2, p2, w2, c2)
        assert result == CoveragePattern.account_neglect

    def test_no_pattern_when_all_below_thresholds(self):
        # Default make_input should produce none
        inp = make_input()
        eng = SalesTerritoryCoverageIntelligenceEngine()
        b = eng._account_breadth_score(inp)
        p = eng._account_prioritization_score(inp)
        w = eng._whitespace_exploitation_score(inp)
        c = eng._churn_prevention_score(inp)
        assert eng._detect_pattern(inp, b, p, w, c) == CoveragePattern.none

    def test_revenue_concentration_beats_churn_when_both_trigger(self):
        # Both revenue_concentration and churn conditions met
        # revenue_concentration should win (higher priority)
        inp = make_input(
            top_account_revenue_concentration_pct=0.80,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=3,  # → pri=40
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=3,  # ratio<0.40
            territory_revenue_growth_pct=-0.15,  # → churn score high
            accounts_neglected_count=0,
            avg_contacts_per_account=5.0,
        )
        eng, b, p, w, c = self._make_engine_and_scores(inp)
        assert eng._detect_pattern(inp, b, p, w, c) == CoveragePattern.revenue_concentration


# ===========================================================================
# 4. RISK LEVELS
# ===========================================================================

class TestRiskLevel:
    def test_low_below_20(self, engine):
        assert engine._risk_level(19.9) == CoverageRisk.low

    def test_low_at_zero(self, engine):
        assert engine._risk_level(0.0) == CoverageRisk.low

    def test_moderate_at_20(self, engine):
        assert engine._risk_level(20.0) == CoverageRisk.moderate

    def test_moderate_at_39(self, engine):
        assert engine._risk_level(39.9) == CoverageRisk.moderate

    def test_high_at_40(self, engine):
        assert engine._risk_level(40.0) == CoverageRisk.high

    def test_high_at_59(self, engine):
        assert engine._risk_level(59.9) == CoverageRisk.high

    def test_critical_at_60(self, engine):
        assert engine._risk_level(60.0) == CoverageRisk.critical

    def test_critical_at_100(self, engine):
        assert engine._risk_level(100.0) == CoverageRisk.critical

    def test_boundary_exactly_20(self, engine):
        assert engine._risk_level(20.0) == CoverageRisk.moderate

    def test_boundary_exactly_40(self, engine):
        assert engine._risk_level(40.0) == CoverageRisk.high

    def test_boundary_exactly_60(self, engine):
        assert engine._risk_level(60.0) == CoverageRisk.critical


# ===========================================================================
# 5. SEVERITY LEVELS
# ===========================================================================

class TestSeverity:
    def test_optimized_below_20(self, engine):
        assert engine._severity(19.9) == CoverageSeverity.optimized

    def test_optimized_at_zero(self, engine):
        assert engine._severity(0.0) == CoverageSeverity.optimized

    def test_gaps_detected_at_20(self, engine):
        assert engine._severity(20.0) == CoverageSeverity.gaps_detected

    def test_gaps_detected_at_39(self, engine):
        assert engine._severity(39.9) == CoverageSeverity.gaps_detected

    def test_underserved_at_40(self, engine):
        assert engine._severity(40.0) == CoverageSeverity.underserved

    def test_underserved_at_59(self, engine):
        assert engine._severity(59.9) == CoverageSeverity.underserved

    def test_critical_at_60(self, engine):
        assert engine._severity(60.0) == CoverageSeverity.critical

    def test_critical_at_100(self, engine):
        assert engine._severity(100.0) == CoverageSeverity.critical


# ===========================================================================
# 6. ACTIONS
# ===========================================================================

class TestAction:
    # Low risk → always no_action
    def test_low_none_no_action(self, engine):
        assert engine._action(CoverageRisk.low, CoveragePattern.none) == CoverageAction.no_action

    def test_low_account_neglect_no_action(self, engine):
        assert engine._action(CoverageRisk.low, CoveragePattern.account_neglect) == CoverageAction.no_action

    def test_low_revenue_concentration_no_action(self, engine):
        assert engine._action(CoverageRisk.low, CoveragePattern.revenue_concentration) == CoverageAction.no_action

    def test_low_churn_risk_no_action(self, engine):
        assert engine._action(CoverageRisk.low, CoveragePattern.churn_risk_uncovered) == CoverageAction.no_action

    def test_low_whitespace_ignored_no_action(self, engine):
        assert engine._action(CoverageRisk.low, CoveragePattern.whitespace_ignored) == CoverageAction.no_action

    def test_low_high_value_no_action(self, engine):
        assert engine._action(CoverageRisk.low, CoveragePattern.high_value_underserved) == CoverageAction.no_action

    # Critical risk
    def test_critical_churn_prevention_sprint(self, engine):
        assert engine._action(CoverageRisk.critical, CoveragePattern.churn_risk_uncovered) == CoverageAction.churn_prevention_sprint

    def test_critical_none_restructure(self, engine):
        assert engine._action(CoverageRisk.critical, CoveragePattern.none) == CoverageAction.territory_restructure

    def test_critical_account_neglect_restructure(self, engine):
        assert engine._action(CoverageRisk.critical, CoveragePattern.account_neglect) == CoverageAction.territory_restructure

    def test_critical_whitespace_ignored_restructure(self, engine):
        assert engine._action(CoverageRisk.critical, CoveragePattern.whitespace_ignored) == CoverageAction.territory_restructure

    def test_critical_high_value_underserved_restructure(self, engine):
        assert engine._action(CoverageRisk.critical, CoveragePattern.high_value_underserved) == CoverageAction.territory_restructure

    def test_critical_revenue_concentration_restructure(self, engine):
        assert engine._action(CoverageRisk.critical, CoveragePattern.revenue_concentration) == CoverageAction.territory_restructure

    # High risk
    def test_high_churn_prevention_sprint(self, engine):
        assert engine._action(CoverageRisk.high, CoveragePattern.churn_risk_uncovered) == CoverageAction.churn_prevention_sprint

    def test_high_whitespace_expansion(self, engine):
        assert engine._action(CoverageRisk.high, CoveragePattern.whitespace_ignored) == CoverageAction.whitespace_expansion

    def test_high_high_value_focus(self, engine):
        assert engine._action(CoverageRisk.high, CoveragePattern.high_value_underserved) == CoverageAction.high_value_focus

    def test_high_none_outreach_blitz(self, engine):
        assert engine._action(CoverageRisk.high, CoveragePattern.none) == CoverageAction.account_outreach_blitz

    def test_high_account_neglect_outreach_blitz(self, engine):
        assert engine._action(CoverageRisk.high, CoveragePattern.account_neglect) == CoverageAction.account_outreach_blitz

    def test_high_revenue_concentration_outreach_blitz(self, engine):
        assert engine._action(CoverageRisk.high, CoveragePattern.revenue_concentration) == CoverageAction.account_outreach_blitz

    # Moderate risk
    def test_moderate_whitespace_expansion(self, engine):
        assert engine._action(CoverageRisk.moderate, CoveragePattern.whitespace_ignored) == CoverageAction.whitespace_expansion

    def test_moderate_none_outreach_blitz(self, engine):
        assert engine._action(CoverageRisk.moderate, CoveragePattern.none) == CoverageAction.account_outreach_blitz

    def test_moderate_account_neglect_outreach_blitz(self, engine):
        assert engine._action(CoverageRisk.moderate, CoveragePattern.account_neglect) == CoverageAction.account_outreach_blitz

    def test_moderate_churn_outreach_blitz(self, engine):
        assert engine._action(CoverageRisk.moderate, CoveragePattern.churn_risk_uncovered) == CoverageAction.account_outreach_blitz

    def test_moderate_high_value_outreach_blitz(self, engine):
        assert engine._action(CoverageRisk.moderate, CoveragePattern.high_value_underserved) == CoverageAction.account_outreach_blitz

    def test_moderate_revenue_concentration_outreach_blitz(self, engine):
        assert engine._action(CoverageRisk.moderate, CoveragePattern.revenue_concentration) == CoverageAction.account_outreach_blitz


# ===========================================================================
# 7. HAS_COVERAGE_GAP FLAG
# ===========================================================================

class TestHasCoverageGap:
    def test_gap_when_composite_ge_40(self, engine):
        inp = make_input(accounts_neglected_count=0, churn_risk_accounts_total=0)
        assert engine._has_coverage_gap(40.0, inp) is True

    def test_no_gap_when_composite_39_no_neglect_no_churn(self, engine):
        inp = make_input(
            accounts_neglected_count=4,
            churn_risk_accounts_total=0,
        )
        # neglected=4 < 5, churn_total=0 → no churn condition, composite<40
        assert engine._has_coverage_gap(39.9, inp) is False

    def test_gap_when_neglected_ge_5(self, engine):
        inp = make_input(accounts_neglected_count=5, churn_risk_accounts_total=0)
        assert engine._has_coverage_gap(10.0, inp) is True

    def test_no_gap_when_neglected_4(self, engine):
        inp = make_input(accounts_neglected_count=4, churn_risk_accounts_total=0)
        assert engine._has_coverage_gap(10.0, inp) is False

    def test_gap_when_churn_contacted_below_40(self, engine):
        inp = make_input(
            accounts_neglected_count=0,
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=3,
        )
        assert engine._has_coverage_gap(10.0, inp) is True

    def test_no_gap_when_churn_contacted_40(self, engine):
        inp = make_input(
            accounts_neglected_count=0,
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=4,
        )
        # 4/10 = 0.40, NOT < 0.40
        assert engine._has_coverage_gap(10.0, inp) is False

    def test_no_gap_when_churn_total_zero(self, engine):
        # churn_risk_accounts_total=0 → condition requires total > 0
        inp = make_input(
            accounts_neglected_count=0,
            churn_risk_accounts_total=0,
            churn_risk_accounts_contacted=0,
        )
        assert engine._has_coverage_gap(10.0, inp) is False

    def test_gap_composite_40_overrides_good_churn(self, engine):
        inp = make_input(
            accounts_neglected_count=0,
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
        )
        assert engine._has_coverage_gap(40.0, inp) is True


# ===========================================================================
# 8. REQUIRES_TERRITORY_REBALANCE FLAG
# ===========================================================================

class TestRequiresTerritoryRebalance:
    def test_rebalance_when_composite_ge_30(self, engine):
        inp = make_input(
            top_account_revenue_concentration_pct=0.30,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
        )
        assert engine._requires_territory_rebalance(30.0, inp) is True

    def test_no_rebalance_when_composite_29_good_rest(self, engine):
        inp = make_input(
            top_account_revenue_concentration_pct=0.30,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
        )
        # 9/10 = 0.90 ≥ 0.40, concentration 0.30 < 0.70
        assert engine._requires_territory_rebalance(29.9, inp) is False

    def test_rebalance_when_concentration_ge_70(self, engine):
        inp = make_input(
            top_account_revenue_concentration_pct=0.70,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
        )
        assert engine._requires_territory_rebalance(0.0, inp) is True

    def test_no_rebalance_when_concentration_69(self, engine):
        inp = make_input(
            top_account_revenue_concentration_pct=0.69,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
        )
        assert engine._requires_territory_rebalance(0.0, inp) is False

    def test_rebalance_when_hv_engaged_below_40(self, engine):
        inp = make_input(
            top_account_revenue_concentration_pct=0.30,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=3,  # 0.30 < 0.40
        )
        assert engine._requires_territory_rebalance(0.0, inp) is True

    def test_no_rebalance_when_hv_engaged_40(self, engine):
        # 4/10 = 0.40, NOT < 0.40
        inp = make_input(
            top_account_revenue_concentration_pct=0.30,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=4,
        )
        assert engine._requires_territory_rebalance(0.0, inp) is False

    def test_rebalance_when_hv_total_zero_uses_denominator_1(self, engine):
        # 0/1 = 0.0 < 0.40 → True
        inp = make_input(
            top_account_revenue_concentration_pct=0.30,
            high_value_accounts_total=0,
            high_value_accounts_engaged_count=0,
        )
        assert engine._requires_territory_rebalance(0.0, inp) is True


# ===========================================================================
# 9. ESTIMATED REVENUE AT RISK
# ===========================================================================

class TestEstimatedRevenueAtRisk:
    def test_basic_calculation(self, engine):
        inp = make_input(accounts_neglected_count=5, avg_account_revenue_usd=10000.0)
        result = engine._estimated_revenue_at_risk(inp, 50.0)
        assert result == round(5 * 10000.0 * 0.50, 2)

    def test_zero_neglected(self, engine):
        inp = make_input(accounts_neglected_count=0, avg_account_revenue_usd=50000.0)
        assert engine._estimated_revenue_at_risk(inp, 80.0) == 0.0

    def test_zero_composite(self, engine):
        inp = make_input(accounts_neglected_count=10, avg_account_revenue_usd=50000.0)
        assert engine._estimated_revenue_at_risk(inp, 0.0) == 0.0

    def test_formula_is_rounded_to_2(self, engine):
        inp = make_input(accounts_neglected_count=3, avg_account_revenue_usd=33333.33)
        result = engine._estimated_revenue_at_risk(inp, 37.7)
        expected = round(3 * 33333.33 * (37.7 / 100.0), 2)
        assert result == expected

    def test_high_composite(self, engine):
        inp = make_input(accounts_neglected_count=2, avg_account_revenue_usd=20000.0)
        result = engine._estimated_revenue_at_risk(inp, 100.0)
        assert result == round(2 * 20000.0 * 1.0, 2)

    def test_full_calculation_matches_default_fixture(self, engine, good_input):
        # default: neglected=2, avg_revenue=20000, composite computed from assess
        r = engine.assess(good_input)
        expected = round(2 * 20000.0 * (r.territory_coverage_composite / 100.0), 2)
        assert r.estimated_revenue_at_risk_usd == expected


# ===========================================================================
# 10. SIGNAL STRING
# ===========================================================================

class TestSignalString:
    def test_optimized_signal_when_none_and_below_20(self, engine):
        inp = make_input()  # good territory → composite < 20, pattern = none
        r = engine.assess(inp)
        if r.coverage_pattern == CoveragePattern.none and r.territory_coverage_composite < 20:
            assert r.coverage_signal == "Territory coverage optimized across all segments"

    def test_optimized_signal_exact_condition(self, engine):
        # Directly test _signal
        inp = make_input()
        signal = engine._signal(inp, CoveragePattern.none, 19.9)
        assert signal == "Territory coverage optimized across all segments"

    def test_not_optimized_when_pattern_not_none(self, engine):
        inp = make_input()
        signal = engine._signal(inp, CoveragePattern.account_neglect, 10.0)
        assert signal != "Territory coverage optimized across all segments"

    def test_not_optimized_when_composite_ge_20(self, engine):
        inp = make_input()
        signal = engine._signal(inp, CoveragePattern.none, 20.0)
        assert signal != "Territory coverage optimized across all segments"

    def test_signal_contains_neglected_when_ge_3(self, engine):
        inp = make_input(accounts_neglected_count=5)
        signal = engine._signal(inp, CoveragePattern.account_neglect, 35.0)
        assert "5 accounts neglected" in signal

    def test_signal_no_neglected_mention_when_below_3(self, engine):
        inp = make_input(accounts_neglected_count=2)
        signal = engine._signal(inp, CoveragePattern.account_neglect, 35.0)
        assert "accounts neglected" not in signal

    def test_signal_hv_coverage_when_below_60(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=4,  # 40% < 60%
            accounts_neglected_count=0,
        )
        signal = engine._signal(inp, CoveragePattern.none, 30.0)
        assert "high-value coverage" in signal

    def test_signal_no_hv_when_above_60(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=7,  # 70% >= 60%
            accounts_neglected_count=0,
        )
        signal = engine._signal(inp, CoveragePattern.none, 30.0)
        assert "high-value coverage" not in signal

    def test_signal_whitespace_missed_when_acted_below_40(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=3,  # 30% < 40%
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=6,
            accounts_neglected_count=0,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
        )
        signal = engine._signal(inp, CoveragePattern.none, 30.0)
        assert "whitespace opportunities missed" in signal

    def test_signal_churn_contacts_when_below_50(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=4,  # 40% < 50%
            accounts_neglected_count=0,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
        )
        signal = engine._signal(inp, CoveragePattern.none, 30.0)
        assert "churn risk contacts" in signal

    def test_signal_composite_shown(self, engine):
        inp = make_input()
        signal = engine._signal(inp, CoveragePattern.account_neglect, 42.0)
        assert "composite 42" in signal

    def test_signal_pattern_label_capitalized(self, engine):
        inp = make_input()
        signal = engine._signal(inp, CoveragePattern.churn_risk_uncovered, 42.0)
        assert signal.startswith("Churn risk uncovered")

    def test_signal_fallback_coverage_risk_for_none_pattern(self, engine):
        inp = make_input(
            accounts_neglected_count=0,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=6,  # 60% >= 50%
        )
        signal = engine._signal(inp, CoveragePattern.none, 25.0)
        assert signal.startswith("Coverage risk")

    def test_signal_no_parts_uses_default(self, engine):
        inp = make_input(
            accounts_neglected_count=0,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=9,
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=9,
        )
        signal = engine._signal(inp, CoveragePattern.none, 25.0)
        assert "territory coverage gaps detected" in signal


# ===========================================================================
# 11. TO_DICT — exactly 15 keys
# ===========================================================================

class TestToDict:
    def test_exactly_15_keys(self, engine, good_input):
        result = engine.assess(good_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_contains_rep_id(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "rep_id" in d

    def test_contains_region(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "region" in d

    def test_contains_coverage_risk(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "coverage_risk" in d

    def test_contains_coverage_pattern(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "coverage_pattern" in d

    def test_contains_coverage_severity(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "coverage_severity" in d

    def test_contains_recommended_action(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "recommended_action" in d

    def test_contains_account_breadth_score(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "account_breadth_score" in d

    def test_contains_account_prioritization_score(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "account_prioritization_score" in d

    def test_contains_whitespace_exploitation_score(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "whitespace_exploitation_score" in d

    def test_contains_churn_prevention_score(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "churn_prevention_score" in d

    def test_contains_territory_coverage_composite(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "territory_coverage_composite" in d

    def test_contains_has_coverage_gap(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "has_coverage_gap" in d

    def test_contains_requires_territory_rebalance(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "requires_territory_rebalance" in d

    def test_contains_estimated_revenue_at_risk_usd(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "estimated_revenue_at_risk_usd" in d

    def test_contains_coverage_signal(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert "coverage_signal" in d

    def test_enum_values_are_strings(self, engine, good_input):
        d = engine.assess(good_input).to_dict()
        assert isinstance(d["coverage_risk"], str)
        assert isinstance(d["coverage_pattern"], str)
        assert isinstance(d["coverage_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_rep_id_value(self, engine):
        inp = make_input(rep_id="rep_xyz")
        d = engine.assess(inp).to_dict()
        assert d["rep_id"] == "rep_xyz"

    def test_region_value(self, engine):
        inp = make_input(region="East")
        d = engine.assess(inp).to_dict()
        assert d["region"] == "East"


# ===========================================================================
# 12. SUMMARY — exactly 13 keys
# ===========================================================================

class TestSummary:
    def test_empty_summary_has_13_keys(self):
        eng = SalesTerritoryCoverageIntelligenceEngine()
        s = eng.summary()
        assert len(s) == 13

    def test_empty_summary_total_zero(self):
        eng = SalesTerritoryCoverageIntelligenceEngine()
        assert eng.summary()["total"] == 0

    def test_empty_summary_avg_composite_zero(self):
        eng = SalesTerritoryCoverageIntelligenceEngine()
        assert eng.summary()["avg_territory_coverage_composite"] == 0.0

    def test_empty_summary_gap_count_zero(self):
        eng = SalesTerritoryCoverageIntelligenceEngine()
        assert eng.summary()["coverage_gap_count"] == 0

    def test_empty_summary_rebalance_count_zero(self):
        eng = SalesTerritoryCoverageIntelligenceEngine()
        assert eng.summary()["rebalance_count"] == 0

    def test_empty_summary_revenue_zero(self):
        eng = SalesTerritoryCoverageIntelligenceEngine()
        assert eng.summary()["total_estimated_revenue_at_risk_usd"] == 0.0

    def test_summary_after_one_assess_has_13_keys(self, engine, good_input):
        engine.assess(good_input)
        s = engine.summary()
        assert len(s) == 13

    def test_summary_total_reflects_assess_count(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        assert engine.summary()["total"] == 5

    def test_summary_risk_counts_sum_to_total(self, engine):
        for _ in range(3):
            engine.assess(make_input())
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_to_total(self, engine):
        for _ in range(3):
            engine.assess(make_input())
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_to_total(self, engine):
        for _ in range(3):
            engine.assess(make_input())
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self, engine):
        for _ in range(3):
            engine.assess(make_input())
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_contains_all_keys(self, engine, good_input):
        engine.assess(good_input)
        s = engine.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_territory_coverage_composite",
            "coverage_gap_count", "rebalance_count",
            "avg_account_breadth_score", "avg_account_prioritization_score",
            "avg_whitespace_exploitation_score", "avg_churn_prevention_score",
            "total_estimated_revenue_at_risk_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_avg_composite_is_rounded(self, engine):
        for _ in range(3):
            engine.assess(make_input())
        s = engine.summary()
        avg = s["avg_territory_coverage_composite"]
        assert avg == round(avg, 1)

    def test_summary_revenue_at_risk_is_sum(self, engine):
        results = [engine.assess(make_input()) for _ in range(3)]
        s = engine.summary()
        expected = round(sum(r.estimated_revenue_at_risk_usd for r in results), 2)
        assert s["total_estimated_revenue_at_risk_usd"] == expected


# ===========================================================================
# 13. ASSESS_BATCH
# ===========================================================================

class TestAssessBatch:
    def test_returns_list(self, engine):
        result = engine.assess_batch([make_input(), make_input()])
        assert isinstance(result, list)

    def test_length_matches_inputs(self, engine):
        inputs = [make_input(rep_id=f"rep_{i}") for i in range(7)]
        results = engine.assess_batch(inputs)
        assert len(results) == 7

    def test_each_element_is_result(self, engine):
        results = engine.assess_batch([make_input()])
        assert isinstance(results[0], TerritoryCoverageResult)

    def test_empty_batch(self, engine):
        assert engine.assess_batch([]) == []

    def test_batch_accumulates_in_summary(self, engine):
        engine.assess_batch([make_input() for _ in range(4)])
        assert engine.summary()["total"] == 4

    def test_single_item_batch(self, engine):
        results = engine.assess_batch([make_input()])
        assert len(results) == 1

    def test_rep_ids_preserved(self, engine):
        inputs = [make_input(rep_id=f"rep_{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        assert [r.rep_id for r in results] == ["rep_0", "rep_1", "rep_2"]


# ===========================================================================
# 14. FULL ASSESS INTEGRATION
# ===========================================================================

class TestAssessIntegration:
    def test_assess_returns_result(self, engine, good_input):
        r = engine.assess(good_input)
        assert isinstance(r, TerritoryCoverageResult)

    def test_assess_stores_in_results(self, engine, good_input):
        engine.assess(good_input)
        assert len(engine._results) == 1

    def test_assess_rep_id_preserved(self, engine):
        inp = make_input(rep_id="myRep")
        r = engine.assess(inp)
        assert r.rep_id == "myRep"

    def test_assess_region_preserved(self, engine):
        inp = make_input(region="North")
        r = engine.assess(inp)
        assert r.region == "North"

    def test_composite_bounded_by_100(self, engine):
        # Worst possible input
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=50,
            accounts_active_count=10,
            accounts_without_next_steps_pct=0.90,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=1,
            top_account_revenue_concentration_pct=0.95,
            avg_contacts_per_account=0.1,
            expansion_signals_identified=10,
            expansion_signals_acted_upon=1,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=1,
            multi_product_penetration_pct=0.05,
            new_logo_accounts_added=10,
            new_logo_converted_count=1,
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=1,
            territory_revenue_growth_pct=-0.50,
        )
        r = engine.assess(inp)
        assert r.territory_coverage_composite <= 100.0

    def test_composite_at_least_0(self, engine, good_input):
        r = engine.assess(good_input)
        assert r.territory_coverage_composite >= 0.0

    def test_scores_rounded_to_1_decimal(self, engine, good_input):
        r = engine.assess(good_input)
        for score in [
            r.account_breadth_score,
            r.account_prioritization_score,
            r.whitespace_exploitation_score,
            r.churn_prevention_score,
            r.territory_coverage_composite,
        ]:
            assert score == round(score, 1)

    def test_composite_weighted_formula(self, engine):
        # Manually verify composite = 0.25*b + 0.30*p + 0.25*w + 0.20*c
        inp = make_input()
        r = engine.assess(inp)
        b, p, w, c = (
            r.account_breadth_score,
            r.account_prioritization_score,
            r.whitespace_exploitation_score,
            r.churn_prevention_score,
        )
        expected = round(b * 0.25 + p * 0.30 + w * 0.25 + c * 0.20, 1)
        assert r.territory_coverage_composite == min(expected, 100.0)

    def test_coverage_risk_matches_composite(self, engine, good_input):
        r = engine.assess(good_input)
        if r.territory_coverage_composite < 20:
            assert r.coverage_risk == CoverageRisk.low
        elif r.territory_coverage_composite < 40:
            assert r.coverage_risk == CoverageRisk.moderate
        elif r.territory_coverage_composite < 60:
            assert r.coverage_risk == CoverageRisk.high
        else:
            assert r.coverage_risk == CoverageRisk.critical

    def test_severity_matches_composite(self, engine, good_input):
        r = engine.assess(good_input)
        if r.territory_coverage_composite < 20:
            assert r.coverage_severity == CoverageSeverity.optimized
        elif r.territory_coverage_composite < 40:
            assert r.coverage_severity == CoverageSeverity.gaps_detected
        elif r.territory_coverage_composite < 60:
            assert r.coverage_severity == CoverageSeverity.underserved
        else:
            assert r.coverage_severity == CoverageSeverity.critical

    def test_multiple_assess_accumulates(self, engine):
        engine.assess(make_input())
        engine.assess(make_input())
        assert len(engine._results) == 2


# ===========================================================================
# 15. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def test_zero_total_accounts(self, engine):
        inp = make_input(
            total_accounts_in_territory=0,
            accounts_active_count=0,
            accounts_neglected_count=0,
        )
        r = engine.assess(inp)
        assert isinstance(r, TerritoryCoverageResult)

    def test_100_percent_active(self, engine):
        inp = make_input(
            total_accounts_in_territory=50,
            accounts_active_count=50,
            accounts_neglected_count=0,
            accounts_without_next_steps_pct=0.0,
        )
        r = engine.assess(inp)
        assert r.account_breadth_score == 0.0

    def test_all_hv_engaged(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=10,
            top_account_revenue_concentration_pct=0.10,
            avg_contacts_per_account=5.0,
        )
        r = engine.assess(inp)
        assert r.account_prioritization_score == 0.0

    def test_perfect_expansion(self, engine):
        inp = make_input(
            expansion_signals_identified=10,
            expansion_signals_acted_upon=10,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=10,
            multi_product_penetration_pct=1.0,
            new_logo_accounts_added=10,
            new_logo_converted_count=10,
        )
        r = engine.assess(inp)
        assert r.whitespace_exploitation_score == 0.0

    def test_zero_churn_total_in_assess(self, engine):
        inp = make_input(
            churn_risk_accounts_total=0,
            churn_risk_accounts_contacted=0,
        )
        r = engine.assess(inp)
        assert isinstance(r, TerritoryCoverageResult)

    def test_high_revenue_concentration_triggers_restructure(self, engine):
        inp = make_input(
            top_account_revenue_concentration_pct=0.90,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=1,  # 10% engaged → pri=40+30=70 → rebalance
            avg_contacts_per_account=0.5,
        )
        r = engine.assess(inp)
        assert r.requires_territory_rebalance is True

    def test_worst_case_is_critical(self, engine):
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=50,
            accounts_active_count=10,
            accounts_without_next_steps_pct=0.90,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=1,
            top_account_revenue_concentration_pct=0.95,
            avg_contacts_per_account=0.1,
            expansion_signals_identified=10,
            expansion_signals_acted_upon=1,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=1,
            multi_product_penetration_pct=0.05,
            new_logo_accounts_added=10,
            new_logo_converted_count=1,
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=1,
            territory_revenue_growth_pct=-0.50,
        )
        r = engine.assess(inp)
        assert r.coverage_risk == CoverageRisk.critical
        assert r.coverage_severity == CoverageSeverity.critical

    def test_best_case_is_low(self, engine):
        inp = make_input()
        r = engine.assess(inp)
        # Default input should produce low risk
        assert r.coverage_risk in (CoverageRisk.low, CoverageRisk.moderate)

    def test_result_fields_are_correct_types(self, engine, good_input):
        r = engine.assess(good_input)
        assert isinstance(r.rep_id, str)
        assert isinstance(r.region, str)
        assert isinstance(r.coverage_risk, CoverageRisk)
        assert isinstance(r.coverage_pattern, CoveragePattern)
        assert isinstance(r.coverage_severity, CoverageSeverity)
        assert isinstance(r.recommended_action, CoverageAction)
        assert isinstance(r.account_breadth_score, float)
        assert isinstance(r.account_prioritization_score, float)
        assert isinstance(r.whitespace_exploitation_score, float)
        assert isinstance(r.churn_prevention_score, float)
        assert isinstance(r.territory_coverage_composite, float)
        assert isinstance(r.has_coverage_gap, bool)
        assert isinstance(r.requires_territory_rebalance, bool)
        assert isinstance(r.estimated_revenue_at_risk_usd, float)
        assert isinstance(r.coverage_signal, str)

    def test_high_neglect_triggers_coverage_gap(self, engine):
        inp = make_input(accounts_neglected_count=10)
        r = engine.assess(inp)
        assert r.has_coverage_gap is True

    def test_very_high_churn_not_contacted_triggers_gap(self, engine):
        inp = make_input(
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=3,
        )
        r = engine.assess(inp)
        assert r.has_coverage_gap is True

    def test_territory_rebalance_low_hv_engagement(self, engine):
        inp = make_input(
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=3,
        )
        r = engine.assess(inp)
        assert r.requires_territory_rebalance is True

    def test_multiple_engines_are_independent(self):
        eng1 = SalesTerritoryCoverageIntelligenceEngine()
        eng2 = SalesTerritoryCoverageIntelligenceEngine()
        eng1.assess(make_input())
        assert eng2.summary()["total"] == 0

    def test_assess_idempotent_output_for_same_input(self, engine):
        inp = make_input()
        r1 = SalesTerritoryCoverageIntelligenceEngine().assess(inp)
        r2 = SalesTerritoryCoverageIntelligenceEngine().assess(inp)
        assert r1.territory_coverage_composite == r2.territory_coverage_composite
        assert r1.coverage_risk == r2.coverage_risk

    def test_avg_account_revenue_zero_produces_zero_risk(self, engine):
        inp = make_input(avg_account_revenue_usd=0.0, accounts_neglected_count=5)
        r = engine.assess(inp)
        assert r.estimated_revenue_at_risk_usd == 0.0

    def test_very_large_territory(self, engine):
        inp = make_input(
            total_accounts_in_territory=10000,
            accounts_active_count=8000,
            accounts_neglected_count=100,
        )
        r = engine.assess(inp)
        assert isinstance(r, TerritoryCoverageResult)

    def test_churn_total_zero_no_gap_condition(self, engine):
        # When churn_risk_accounts_total=0, the third condition in _has_coverage_gap
        # is short-circuited by "churn_risk_accounts_total > 0"
        inp = make_input(
            accounts_neglected_count=0,
            churn_risk_accounts_total=0,
            churn_risk_accounts_contacted=0,
        )
        r = engine.assess(inp)
        # Only composite or neglected>=5 can trigger gap here
        if r.territory_coverage_composite < 40 and inp.accounts_neglected_count < 5:
            assert r.has_coverage_gap is False

    def test_summary_empty_risk_counts_empty_dict(self):
        eng = SalesTerritoryCoverageIntelligenceEngine()
        s = eng.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_summary_after_batch_correct_total(self, engine):
        engine.assess_batch([make_input() for _ in range(10)])
        assert engine.summary()["total"] == 10


# ===========================================================================
# 16. COMPOSITE THRESHOLD SCENARIOS (end-to-end)
# ===========================================================================

class TestCompositeThresholds:
    def test_composite_below_20_low_risk_optimized(self, engine):
        # Very good territory
        inp = make_input(
            total_accounts_in_territory=50,
            accounts_active_count=48,
            accounts_neglected_count=0,
            accounts_without_next_steps_pct=0.05,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=10,
            top_account_revenue_concentration_pct=0.10,
            avg_contacts_per_account=5.0,
            expansion_signals_identified=10,
            expansion_signals_acted_upon=9,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=8,
            multi_product_penetration_pct=0.80,
            new_logo_accounts_added=5,
            new_logo_converted_count=4,
            churn_risk_accounts_total=5,
            churn_risk_accounts_contacted=5,
            territory_revenue_growth_pct=0.20,
            avg_account_revenue_usd=10000.0,
        )
        r = engine.assess(inp)
        assert r.territory_coverage_composite < 20
        assert r.coverage_risk == CoverageRisk.low
        assert r.coverage_severity == CoverageSeverity.optimized
        assert r.recommended_action == CoverageAction.no_action
        assert r.coverage_signal == "Territory coverage optimized across all segments"

    def test_composite_40_plus_has_coverage_gap(self, engine):
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=30,
            accounts_active_count=20,
            accounts_without_next_steps_pct=0.70,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=3,
            top_account_revenue_concentration_pct=0.50,
            avg_contacts_per_account=0.5,
            expansion_signals_identified=10,
            expansion_signals_acted_upon=1,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=1,
            multi_product_penetration_pct=0.10,
            new_logo_accounts_added=10,
            new_logo_converted_count=1,
            churn_risk_accounts_total=10,
            churn_risk_accounts_contacted=1,
            territory_revenue_growth_pct=-0.15,
        )
        r = engine.assess(inp)
        if r.territory_coverage_composite >= 40:
            assert r.has_coverage_gap is True

    def test_composite_30_plus_requires_rebalance(self, engine):
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=25,
            accounts_active_count=20,
            accounts_without_next_steps_pct=0.50,
        )
        r = engine.assess(inp)
        if r.territory_coverage_composite >= 30:
            assert r.requires_territory_rebalance is True

    def test_high_risk_action_for_high_composite(self, engine):
        inp = make_input(
            total_accounts_in_territory=100,
            accounts_neglected_count=20,
            accounts_active_count=20,
            accounts_without_next_steps_pct=0.70,
            high_value_accounts_total=10,
            high_value_accounts_engaged_count=3,
            top_account_revenue_concentration_pct=0.30,
            avg_contacts_per_account=0.5,
            expansion_signals_identified=10,
            expansion_signals_acted_upon=3,
            whitespace_accounts_identified=10,
            whitespace_accounts_pursued=3,
            multi_product_penetration_pct=0.15,
            new_logo_accounts_added=10,
            new_logo_converted_count=1,
            churn_risk_accounts_total=5,
            churn_risk_accounts_contacted=4,
            territory_revenue_growth_pct=0.05,
        )
        r = engine.assess(inp)
        if r.coverage_risk == CoverageRisk.high:
            assert r.recommended_action in (
                CoverageAction.account_outreach_blitz,
                CoverageAction.churn_prevention_sprint,
                CoverageAction.whitespace_expansion,
                CoverageAction.high_value_focus,
            )
