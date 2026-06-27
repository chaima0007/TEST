"""
Comprehensive pytest tests for TerritoryWhitespaceAnalyzer.

Covers:
- Dataclass field counts
- to_dict() key counts and values
- summary() key counts and values
- All enum values
- All scoring branches (opportunity_density, market_timing, territory_coverage,
  icp_alignment, composite, whitespace_priority, whitespace_type,
  territory_health, territory_penetration_pct, estimated_whitespace_arr,
  whitespace_action)
- is_high_potential_territory and needs_immediate_prospecting flags
- analyze() and analyze_batch() public API
- Properties: high_potential_territories, immediate_prospecting_queue,
  total_estimated_whitespace_arr, avg_whitespace_composite
- reset()
- Edge cases (zero accounts, boundary values, signal combinations)
"""

from __future__ import annotations

import dataclasses
import math
import pytest

from swarm.intelligence.territory_whitespace_analyzer import (
    TerritoryWhitespaceAnalyzer,
    TerritoryWhitespaceInput,
    TerritoryWhitespaceResult,
    WhitespacePriority,
    WhitespaceType,
    TerritoryHealth,
    WhitespaceAction,
)


# ---------------------------------------------------------------------------
# Helpers / factories
# ---------------------------------------------------------------------------

def make_input(**overrides) -> TerritoryWhitespaceInput:
    """Return a baseline TerritoryWhitespaceInput with all fields populated.

    The baseline is deliberately modest so individual tests can tweak specific
    fields to exercise branches without unintended side-effects.
    """
    defaults = dict(
        territory_id="T001",
        territory_name="West Region",
        rep_id="R001",
        total_accounts_in_territory=100,
        accounts_with_active_deals=5,
        accounts_with_customers=5,
        accounts_never_contacted=40,
        icp_match_score_avg=50.0,
        avg_company_size_employees=500,
        industry_growth_rate_pct=3.0,
        competitor_present_pct=30.0,
        buying_trigger_signal_count=2,
        lookalike_customer_match_count=3,
        avg_deal_size_similar_accounts=40_000.0,
        territory_quota_attainment_pct=60.0,
        months_rep_in_territory=6,
        outreach_coverage_pct=60.0,
        territory_revenue_potential=500_000.0,
        current_territory_revenue=100_000.0,
        conference_event_signal=0,
        seasonal_buying_signal=0,
        executive_referral_count=2,
    )
    defaults.update(overrides)
    return TerritoryWhitespaceInput(**defaults)


def make_analyzer() -> TerritoryWhitespaceAnalyzer:
    return TerritoryWhitespaceAnalyzer()


# ---------------------------------------------------------------------------
# 1. Enum tests
# ---------------------------------------------------------------------------

class TestEnums:
    def test_whitespace_priority_values(self):
        assert WhitespacePriority.LOW.value == "low"
        assert WhitespacePriority.MEDIUM.value == "medium"
        assert WhitespacePriority.HIGH.value == "high"
        assert WhitespacePriority.URGENT.value == "urgent"

    def test_whitespace_priority_count(self):
        assert len(WhitespacePriority) == 4

    def test_whitespace_type_values(self):
        assert WhitespaceType.NEW_LOGO.value == "new_logo"
        assert WhitespaceType.PRODUCT_EXPAND.value == "product_expand"
        assert WhitespaceType.GEO_EXPAND.value == "geo_expand"
        assert WhitespaceType.SEGMENT_EXPAND.value == "segment_expand"
        assert WhitespaceType.DORMANT_REACTIVATE.value == "dormant_reactivate"

    def test_whitespace_type_count(self):
        assert len(WhitespaceType) == 5

    def test_territory_health_values(self):
        assert TerritoryHealth.UNDERPENETRATED.value == "underpenetrated"
        assert TerritoryHealth.DEVELOPING.value == "developing"
        assert TerritoryHealth.OPTIMIZED.value == "optimized"
        assert TerritoryHealth.SATURATED.value == "saturated"

    def test_territory_health_count(self):
        assert len(TerritoryHealth) == 4

    def test_whitespace_action_values(self):
        assert WhitespaceAction.NURTURE.value == "nurture"
        assert WhitespaceAction.PROSPECT.value == "prospect"
        assert WhitespaceAction.PRIORITIZE.value == "prioritize"
        assert WhitespaceAction.IMMEDIATE_FOCUS.value == "immediate_focus"

    def test_whitespace_action_count(self):
        assert len(WhitespaceAction) == 4

    def test_enums_are_str_subclass(self):
        assert isinstance(WhitespacePriority.LOW, str)
        assert isinstance(WhitespaceType.NEW_LOGO, str)
        assert isinstance(TerritoryHealth.DEVELOPING, str)
        assert isinstance(WhitespaceAction.NURTURE, str)


# ---------------------------------------------------------------------------
# 2. TerritoryWhitespaceInput field count
# ---------------------------------------------------------------------------

class TestTerritoryWhitespaceInputFields:
    def test_exactly_22_fields(self):
        fields = dataclasses.fields(TerritoryWhitespaceInput)
        assert len(fields) == 22

    def test_field_names(self):
        field_names = {f.name for f in dataclasses.fields(TerritoryWhitespaceInput)}
        expected = {
            "territory_id",
            "territory_name",
            "rep_id",
            "total_accounts_in_territory",
            "accounts_with_active_deals",
            "accounts_with_customers",
            "accounts_never_contacted",
            "icp_match_score_avg",
            "avg_company_size_employees",
            "industry_growth_rate_pct",
            "competitor_present_pct",
            "buying_trigger_signal_count",
            "lookalike_customer_match_count",
            "avg_deal_size_similar_accounts",
            "territory_quota_attainment_pct",
            "months_rep_in_territory",
            "outreach_coverage_pct",
            "territory_revenue_potential",
            "current_territory_revenue",
            "conference_event_signal",
            "seasonal_buying_signal",
            "executive_referral_count",
        }
        assert field_names == expected

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(TerritoryWhitespaceInput)

    def test_instantiation(self):
        inp = make_input()
        assert inp.territory_id == "T001"


# ---------------------------------------------------------------------------
# 3. TerritoryWhitespaceResult.to_dict() key count and values
# ---------------------------------------------------------------------------

class TestTerritoryWhitespaceResultToDict:
    def setup_method(self):
        self.analyzer = make_analyzer()
        self.result = self.analyzer.analyze(make_input())
        self.d = self.result.to_dict()

    def test_exactly_15_keys(self):
        assert len(self.d) == 15

    def test_key_names(self):
        expected_keys = {
            "territory_id",
            "territory_name",
            "whitespace_priority",
            "whitespace_type",
            "territory_health",
            "whitespace_action",
            "opportunity_density_score",
            "market_timing_score",
            "territory_coverage_score",
            "icp_alignment_score",
            "whitespace_composite",
            "estimated_whitespace_arr",
            "territory_penetration_pct",
            "is_high_potential_territory",
            "needs_immediate_prospecting",
        }
        assert set(self.d.keys()) == expected_keys

    def test_priority_is_string_value(self):
        assert isinstance(self.d["whitespace_priority"], str)
        assert self.d["whitespace_priority"] in {"low", "medium", "high", "urgent"}

    def test_type_is_string_value(self):
        assert isinstance(self.d["whitespace_type"], str)

    def test_health_is_string_value(self):
        assert isinstance(self.d["territory_health"], str)

    def test_action_is_string_value(self):
        assert isinstance(self.d["whitespace_action"], str)

    def test_scores_are_floats(self):
        for key in ("opportunity_density_score", "market_timing_score",
                    "territory_coverage_score", "icp_alignment_score",
                    "whitespace_composite", "estimated_whitespace_arr",
                    "territory_penetration_pct"):
            assert isinstance(self.d[key], float), f"{key} should be float"

    def test_booleans(self):
        assert isinstance(self.d["is_high_potential_territory"], bool)
        assert isinstance(self.d["needs_immediate_prospecting"], bool)

    def test_territory_id_matches(self):
        assert self.d["territory_id"] == "T001"

    def test_territory_name_matches(self):
        assert self.d["territory_name"] == "West Region"


# ---------------------------------------------------------------------------
# 4. summary() key count and empty-state
# ---------------------------------------------------------------------------

class TestSummary:
    def test_empty_summary_has_13_keys(self):
        analyzer = make_analyzer()
        s = analyzer.summary()
        assert len(s) == 13

    def test_empty_summary_key_names(self):
        analyzer = make_analyzer()
        s = analyzer.summary()
        expected = {
            "total",
            "priority_counts",
            "type_counts",
            "health_counts",
            "action_counts",
            "avg_whitespace_composite",
            "total_estimated_whitespace_arr",
            "high_potential_count",
            "immediate_prospecting_count",
            "avg_opportunity_density_score",
            "avg_market_timing_score",
            "avg_territory_coverage_score",
            "avg_icp_alignment_score",
        }
        assert set(s.keys()) == expected

    def test_empty_summary_total_zero(self):
        s = make_analyzer().summary()
        assert s["total"] == 0

    def test_empty_summary_counts_empty_dicts(self):
        s = make_analyzer().summary()
        assert s["priority_counts"] == {}
        assert s["type_counts"] == {}
        assert s["health_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_numeric_zeros(self):
        s = make_analyzer().summary()
        assert s["avg_whitespace_composite"] == 0.0
        assert s["total_estimated_whitespace_arr"] == 0.0
        assert s["high_potential_count"] == 0
        assert s["immediate_prospecting_count"] == 0
        assert s["avg_opportunity_density_score"] == 0.0
        assert s["avg_market_timing_score"] == 0.0
        assert s["avg_territory_coverage_score"] == 0.0
        assert s["avg_icp_alignment_score"] == 0.0

    def test_summary_after_single_analyze_has_13_keys(self):
        a = make_analyzer()
        a.analyze(make_input())
        s = a.summary()
        assert len(s) == 13

    def test_summary_total_matches_analyzed_count(self):
        a = make_analyzer()
        for i in range(5):
            a.analyze(make_input(territory_id=f"T{i}"))
        assert a.summary()["total"] == 5

    def test_summary_priority_counts_sums_to_total(self):
        a = make_analyzer()
        for i in range(4):
            a.analyze(make_input(territory_id=f"T{i}"))
        s = a.summary()
        assert sum(s["priority_counts"].values()) == s["total"]

    def test_summary_type_counts_sums_to_total(self):
        a = make_analyzer()
        for i in range(3):
            a.analyze(make_input(territory_id=f"T{i}"))
        s = a.summary()
        assert sum(s["type_counts"].values()) == s["total"]

    def test_summary_health_counts_sums_to_total(self):
        a = make_analyzer()
        for i in range(3):
            a.analyze(make_input(territory_id=f"T{i}"))
        s = a.summary()
        assert sum(s["health_counts"].values()) == s["total"]

    def test_summary_action_counts_sums_to_total(self):
        a = make_analyzer()
        for i in range(3):
            a.analyze(make_input(territory_id=f"T{i}"))
        s = a.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_high_potential_count_correct(self):
        a = make_analyzer()
        # high composite
        a.analyze(make_input(territory_id="T1", buying_trigger_signal_count=10,
                              lookalike_customer_match_count=6, industry_growth_rate_pct=25,
                              seasonal_buying_signal=1, conference_event_signal=1,
                              outreach_coverage_pct=10, accounts_never_contacted=80))
        # low composite
        a.analyze(make_input(territory_id="T2", buying_trigger_signal_count=0,
                              lookalike_customer_match_count=0, industry_growth_rate_pct=1,
                              outreach_coverage_pct=90, accounts_never_contacted=5,
                              executive_referral_count=0, avg_deal_size_similar_accounts=1000))
        s = a.summary()
        assert s["high_potential_count"] == len(a.high_potential_territories)


# ---------------------------------------------------------------------------
# 5. _opportunity_density_score branches
# ---------------------------------------------------------------------------

class TestOpportunityDensityScore:
    def setup_method(self):
        self.a = make_analyzer()

    def _score(self, **kw):
        return self.a._opportunity_density_score(make_input(**kw))

    def test_zero_total_accounts_contributes_zero_untouched(self):
        score = self._score(total_accounts_in_territory=0,
                            accounts_never_contacted=0,
                            lookalike_customer_match_count=0,
                            buying_trigger_signal_count=0,
                            executive_referral_count=0)
        assert score == 0.0

    def test_untouched_pct_contributes_up_to_35(self):
        # 100% never contacted → untouched_pct=1 → 1*50=50, capped 35
        score = self._score(total_accounts_in_territory=100,
                            accounts_never_contacted=100,
                            lookalike_customer_match_count=0,
                            buying_trigger_signal_count=0,
                            executive_referral_count=0)
        assert score == 35.0

    def test_untouched_pct_partial(self):
        # 40% never contacted → 0.4*50=20, not capped
        score = self._score(total_accounts_in_territory=100,
                            accounts_never_contacted=40,
                            lookalike_customer_match_count=0,
                            buying_trigger_signal_count=0,
                            executive_referral_count=0)
        assert score == pytest.approx(20.0, abs=0.15)

    def test_lookalike_capped_at_30(self):
        # 10 lookalike * 5 = 50, capped 30
        score = self._score(total_accounts_in_territory=0,
                            accounts_never_contacted=0,
                            lookalike_customer_match_count=10,
                            buying_trigger_signal_count=0,
                            executive_referral_count=0)
        assert score == 30.0

    def test_lookalike_partial(self):
        # 3 lookalike * 5 = 15
        score = self._score(total_accounts_in_territory=0,
                            accounts_never_contacted=0,
                            lookalike_customer_match_count=3,
                            buying_trigger_signal_count=0,
                            executive_referral_count=0)
        assert score == pytest.approx(15.0, abs=0.15)

    def test_trigger_signals_capped_at_25(self):
        # 10 signals * 3 = 30, capped 25
        score = self._score(total_accounts_in_territory=0,
                            accounts_never_contacted=0,
                            lookalike_customer_match_count=0,
                            buying_trigger_signal_count=10,
                            executive_referral_count=0)
        assert score == 25.0

    def test_trigger_signals_partial(self):
        # 2 signals * 3 = 6
        score = self._score(total_accounts_in_territory=0,
                            accounts_never_contacted=0,
                            lookalike_customer_match_count=0,
                            buying_trigger_signal_count=2,
                            executive_referral_count=0)
        assert score == pytest.approx(6.0, abs=0.15)

    def test_executive_referrals_capped_at_10(self):
        # 6 referrals * 2 = 12, capped 10
        score = self._score(total_accounts_in_territory=0,
                            accounts_never_contacted=0,
                            lookalike_customer_match_count=0,
                            buying_trigger_signal_count=0,
                            executive_referral_count=6)
        assert score == 10.0

    def test_executive_referrals_partial(self):
        # 2 referrals * 2 = 4
        score = self._score(total_accounts_in_territory=0,
                            accounts_never_contacted=0,
                            lookalike_customer_match_count=0,
                            buying_trigger_signal_count=0,
                            executive_referral_count=2)
        assert score == pytest.approx(4.0, abs=0.15)

    def test_max_possible_score_is_100(self):
        # All components capped: 35+30+25+10=100
        score = self._score(total_accounts_in_territory=100,
                            accounts_never_contacted=100,
                            lookalike_customer_match_count=10,
                            buying_trigger_signal_count=10,
                            executive_referral_count=6)
        assert score == 100.0

    def test_all_zero_returns_zero(self):
        score = self._score(total_accounts_in_territory=0,
                            accounts_never_contacted=0,
                            lookalike_customer_match_count=0,
                            buying_trigger_signal_count=0,
                            executive_referral_count=0)
        assert score == 0.0

    def test_score_never_exceeds_100(self):
        score = self._score(total_accounts_in_territory=1,
                            accounts_never_contacted=1,
                            lookalike_customer_match_count=100,
                            buying_trigger_signal_count=100,
                            executive_referral_count=100)
        assert score <= 100.0

    def test_score_never_below_zero(self):
        score = self._score(total_accounts_in_territory=0,
                            accounts_never_contacted=0,
                            lookalike_customer_match_count=0,
                            buying_trigger_signal_count=0,
                            executive_referral_count=0)
        assert score >= 0.0

    def test_combined_components_sum_correctly(self):
        # 40/100 never contacted → 20, lookalike=3 → 15, triggers=2 → 6, referrals=2 → 4 → total 45
        score = self._score(total_accounts_in_territory=100,
                            accounts_never_contacted=40,
                            lookalike_customer_match_count=3,
                            buying_trigger_signal_count=2,
                            executive_referral_count=2)
        assert score == pytest.approx(45.0, abs=0.15)

    def test_untouched_pct_exactly_at_cap_boundary(self):
        # 70/100 = 0.7; 0.7*50=35 exactly at cap
        score = self._score(total_accounts_in_territory=100,
                            accounts_never_contacted=70,
                            lookalike_customer_match_count=0,
                            buying_trigger_signal_count=0,
                            executive_referral_count=0)
        assert score == pytest.approx(35.0, abs=0.15)

    def test_lookalike_at_exactly_cap_boundary(self):
        # 6 * 5 = 30 exactly at cap
        score = self._score(total_accounts_in_territory=0,
                            accounts_never_contacted=0,
                            lookalike_customer_match_count=6,
                            buying_trigger_signal_count=0,
                            executive_referral_count=0)
        assert score == 30.0

    def test_trigger_at_exactly_cap_boundary(self):
        # ceil(25/3) = ~9; 8*3=24, 9*3=27 > 25 so cap is at 9 signals
        # At exactly 25/3 ≈ 8.33 signals → use 9 (integer) → 27 capped to 25
        score = self._score(total_accounts_in_territory=0,
                            accounts_never_contacted=0,
                            lookalike_customer_match_count=0,
                            buying_trigger_signal_count=9,
                            executive_referral_count=0)
        assert score == 25.0

    def test_referrals_at_exactly_cap_boundary(self):
        # 5 * 2 = 10 exactly
        score = self._score(total_accounts_in_territory=0,
                            accounts_never_contacted=0,
                            lookalike_customer_match_count=0,
                            buying_trigger_signal_count=0,
                            executive_referral_count=5)
        assert score == 10.0

    def test_result_is_rounded_to_1_decimal(self):
        score = self._score(total_accounts_in_territory=3,
                            accounts_never_contacted=1,
                            lookalike_customer_match_count=0,
                            buying_trigger_signal_count=0,
                            executive_referral_count=0)
        # 1/3 * 50 = 16.666... → rounded to 16.7
        assert score == pytest.approx(16.7, abs=0.05)


# ---------------------------------------------------------------------------
# 6. _market_timing_score branches
# ---------------------------------------------------------------------------

class TestMarketTimingScore:
    def setup_method(self):
        self.a = make_analyzer()

    def _score(self, **kw):
        return self.a._market_timing_score(make_input(**kw))

    def test_base_score_30(self):
        score = self._score(industry_growth_rate_pct=0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=30.0)
        assert score == 30.0

    def test_growth_below_5_no_bonus(self):
        score = self._score(industry_growth_rate_pct=4.9,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=30.0)
        assert score == 30.0

    def test_growth_exactly_5_adds_10(self):
        score = self._score(industry_growth_rate_pct=5.0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=30.0)
        assert score == 40.0

    def test_growth_between_5_and_10(self):
        score = self._score(industry_growth_rate_pct=7.0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=30.0)
        assert score == 40.0

    def test_growth_exactly_10_adds_20(self):
        score = self._score(industry_growth_rate_pct=10.0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=30.0)
        assert score == 50.0

    def test_growth_between_10_and_20(self):
        score = self._score(industry_growth_rate_pct=15.0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=30.0)
        assert score == 50.0

    def test_growth_exactly_20_adds_30(self):
        score = self._score(industry_growth_rate_pct=20.0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=30.0)
        assert score == 60.0

    def test_growth_above_20_adds_30(self):
        score = self._score(industry_growth_rate_pct=50.0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=30.0)
        assert score == 60.0

    def test_seasonal_adds_20(self):
        score = self._score(industry_growth_rate_pct=0,
                            seasonal_buying_signal=1,
                            conference_event_signal=0,
                            competitor_present_pct=30.0)
        assert score == 50.0

    def test_no_seasonal_no_addition(self):
        score = self._score(industry_growth_rate_pct=0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=30.0)
        assert score == 30.0

    def test_conference_adds_15(self):
        score = self._score(industry_growth_rate_pct=0,
                            seasonal_buying_signal=0,
                            conference_event_signal=1,
                            competitor_present_pct=30.0)
        assert score == 45.0

    def test_no_conference_no_addition(self):
        score = self._score(industry_growth_rate_pct=0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=30.0)
        assert score == 30.0

    def test_competitor_le_20_adds_5(self):
        score = self._score(industry_growth_rate_pct=0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=20.0)
        assert score == 35.0

    def test_competitor_below_20_adds_5(self):
        score = self._score(industry_growth_rate_pct=0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=10.0)
        assert score == 35.0

    def test_competitor_0_adds_5(self):
        score = self._score(industry_growth_rate_pct=0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=0.0)
        assert score == 35.0

    def test_competitor_between_20_and_60_neutral(self):
        score = self._score(industry_growth_rate_pct=0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=40.0)
        assert score == 30.0

    def test_competitor_ge_60_subtracts_10(self):
        score = self._score(industry_growth_rate_pct=0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=60.0)
        assert score == 20.0

    def test_competitor_above_60_subtracts_10(self):
        score = self._score(industry_growth_rate_pct=0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=80.0)
        assert score == 20.0

    def test_score_capped_at_100(self):
        score = self._score(industry_growth_rate_pct=50,
                            seasonal_buying_signal=1,
                            conference_event_signal=1,
                            competitor_present_pct=10.0)
        # 30+30+20+15+5 = 100
        assert score == 100.0

    def test_score_never_below_zero(self):
        # base=30 - 10 (comp>=60) = 20, no negatives possible really
        score = self._score(industry_growth_rate_pct=-100,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=100.0)
        assert score >= 0.0

    def test_all_signals_combined(self):
        score = self._score(industry_growth_rate_pct=20,
                            seasonal_buying_signal=1,
                            conference_event_signal=1,
                            competitor_present_pct=15.0)
        # 30 + 30 + 20 + 15 + 5 = 100
        assert score == 100.0

    def test_competitor_exactly_21_no_bonus_no_penalty(self):
        score = self._score(industry_growth_rate_pct=0,
                            seasonal_buying_signal=0,
                            conference_event_signal=0,
                            competitor_present_pct=21.0)
        assert score == 30.0


# ---------------------------------------------------------------------------
# 7. _territory_coverage_score branches
# ---------------------------------------------------------------------------

class TestTerritoryCoverageScore:
    def setup_method(self):
        self.a = make_analyzer()

    def _score(self, **kw):
        return self.a._territory_coverage_score(make_input(**kw))

    def test_base_is_100_minus_coverage(self):
        score = self._score(outreach_coverage_pct=60.0,
                            months_rep_in_territory=6,
                            territory_quota_attainment_pct=60.0)
        # 100-60=40, tenure neutral, attainment>=50 no bonus → 40
        assert score == pytest.approx(40.0, abs=0.15)

    def test_0_coverage_gives_100_base(self):
        score = self._score(outreach_coverage_pct=0.0,
                            months_rep_in_territory=6,
                            territory_quota_attainment_pct=60.0)
        assert score == 100.0

    def test_100_coverage_gives_0_base(self):
        score = self._score(outreach_coverage_pct=100.0,
                            months_rep_in_territory=6,
                            territory_quota_attainment_pct=60.0)
        assert score == 0.0

    def test_tenure_le_3_adds_10(self):
        score = self._score(outreach_coverage_pct=60.0,
                            months_rep_in_territory=3,
                            territory_quota_attainment_pct=60.0)
        # 40 + 10 = 50
        assert score == pytest.approx(50.0, abs=0.15)

    def test_tenure_1_adds_10(self):
        score = self._score(outreach_coverage_pct=60.0,
                            months_rep_in_territory=1,
                            territory_quota_attainment_pct=60.0)
        assert score == pytest.approx(50.0, abs=0.15)

    def test_tenure_4_neutral(self):
        score = self._score(outreach_coverage_pct=60.0,
                            months_rep_in_territory=4,
                            territory_quota_attainment_pct=60.0)
        assert score == pytest.approx(40.0, abs=0.15)

    def test_tenure_12_neutral(self):
        score = self._score(outreach_coverage_pct=60.0,
                            months_rep_in_territory=12,
                            territory_quota_attainment_pct=60.0)
        assert score == pytest.approx(40.0, abs=0.15)

    def test_tenure_gt_12_adds_5(self):
        score = self._score(outreach_coverage_pct=60.0,
                            months_rep_in_territory=13,
                            territory_quota_attainment_pct=60.0)
        # 40 + 5 = 45
        assert score == pytest.approx(45.0, abs=0.15)

    def test_tenure_24_adds_5(self):
        score = self._score(outreach_coverage_pct=60.0,
                            months_rep_in_territory=24,
                            territory_quota_attainment_pct=60.0)
        assert score == pytest.approx(45.0, abs=0.15)

    def test_attainment_lt_50_adds_10(self):
        score = self._score(outreach_coverage_pct=60.0,
                            months_rep_in_territory=6,
                            territory_quota_attainment_pct=49.9)
        # 40 + 10 = 50
        assert score == pytest.approx(50.0, abs=0.15)

    def test_attainment_0_adds_10(self):
        score = self._score(outreach_coverage_pct=60.0,
                            months_rep_in_territory=6,
                            territory_quota_attainment_pct=0.0)
        assert score == pytest.approx(50.0, abs=0.15)

    def test_attainment_exactly_50_no_bonus(self):
        score = self._score(outreach_coverage_pct=60.0,
                            months_rep_in_territory=6,
                            territory_quota_attainment_pct=50.0)
        assert score == pytest.approx(40.0, abs=0.15)

    def test_attainment_100_no_bonus(self):
        score = self._score(outreach_coverage_pct=60.0,
                            months_rep_in_territory=6,
                            territory_quota_attainment_pct=100.0)
        assert score == pytest.approx(40.0, abs=0.15)

    def test_score_capped_at_100(self):
        score = self._score(outreach_coverage_pct=0.0,
                            months_rep_in_territory=1,
                            territory_quota_attainment_pct=0.0)
        # 100 + 10 + 10 would be 120, capped at 100
        assert score == 100.0

    def test_score_never_below_zero(self):
        score = self._score(outreach_coverage_pct=100.0,
                            months_rep_in_territory=6,
                            territory_quota_attainment_pct=60.0)
        assert score >= 0.0

    def test_all_bonuses_applied_together(self):
        score = self._score(outreach_coverage_pct=70.0,
                            months_rep_in_territory=2,
                            territory_quota_attainment_pct=30.0)
        # 100-70=30, +10 (tenure<=3), +10 (attainment<50) = 50
        assert score == pytest.approx(50.0, abs=0.15)

    def test_experienced_rep_low_attainment(self):
        score = self._score(outreach_coverage_pct=60.0,
                            months_rep_in_territory=18,
                            territory_quota_attainment_pct=20.0)
        # 40 + 5 (tenure>12) + 10 (attainment<50) = 55
        assert score == pytest.approx(55.0, abs=0.15)


# ---------------------------------------------------------------------------
# 8. _icp_alignment_score branches
# ---------------------------------------------------------------------------

class TestIcpAlignmentScore:
    def setup_method(self):
        self.a = make_analyzer()

    def _score(self, **kw):
        return self.a._icp_alignment_score(make_input(**kw))

    def test_base_is_icp_match_times_0_6(self):
        score = self._score(icp_match_score_avg=50.0,
                            avg_company_size_employees=10,
                            avg_deal_size_similar_accounts=10_000.0)
        # 50*0.60=30, size<50 → no bonus, deal<50k → no bonus
        assert score == pytest.approx(30.0, abs=0.15)

    def test_size_100_to_2000_adds_25(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=500,
                            avg_deal_size_similar_accounts=0.0)
        assert score == pytest.approx(25.0, abs=0.15)

    def test_size_100_boundary_adds_25(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=100,
                            avg_deal_size_similar_accounts=0.0)
        assert score == pytest.approx(25.0, abs=0.15)

    def test_size_2000_boundary_adds_25(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=2000,
                            avg_deal_size_similar_accounts=0.0)
        assert score == pytest.approx(25.0, abs=0.15)

    def test_size_50_adds_15(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=50,
                            avg_deal_size_similar_accounts=0.0)
        assert score == pytest.approx(15.0, abs=0.15)

    def test_size_99_adds_15(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=99,
                            avg_deal_size_similar_accounts=0.0)
        assert score == pytest.approx(15.0, abs=0.15)

    def test_size_2001_adds_15(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=2001,
                            avg_deal_size_similar_accounts=0.0)
        assert score == pytest.approx(15.0, abs=0.15)

    def test_size_5000_adds_15(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=5000,
                            avg_deal_size_similar_accounts=0.0)
        assert score == pytest.approx(15.0, abs=0.15)

    def test_size_5001_adds_8(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=5001,
                            avg_deal_size_similar_accounts=0.0)
        assert score == pytest.approx(8.0, abs=0.15)

    def test_size_10000_adds_8(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=10000,
                            avg_deal_size_similar_accounts=0.0)
        assert score == pytest.approx(8.0, abs=0.15)

    def test_size_below_50_no_bonus(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=49,
                            avg_deal_size_similar_accounts=0.0)
        assert score == pytest.approx(0.0, abs=0.15)

    def test_deal_ge_100k_adds_15(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=10,
                            avg_deal_size_similar_accounts=100_000.0)
        assert score == pytest.approx(15.0, abs=0.15)

    def test_deal_above_100k_adds_15(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=10,
                            avg_deal_size_similar_accounts=200_000.0)
        assert score == pytest.approx(15.0, abs=0.15)

    def test_deal_50k_to_99k_adds_8(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=10,
                            avg_deal_size_similar_accounts=50_000.0)
        assert score == pytest.approx(8.0, abs=0.15)

    def test_deal_75k_adds_8(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=10,
                            avg_deal_size_similar_accounts=75_000.0)
        assert score == pytest.approx(8.0, abs=0.15)

    def test_deal_below_50k_no_bonus(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=10,
                            avg_deal_size_similar_accounts=49_999.0)
        assert score == pytest.approx(0.0, abs=0.15)

    def test_score_capped_at_100(self):
        score = self._score(icp_match_score_avg=100.0,
                            avg_company_size_employees=500,
                            avg_deal_size_similar_accounts=200_000.0)
        # 60 + 25 + 15 = 100
        assert score == 100.0

    def test_score_never_below_zero(self):
        score = self._score(icp_match_score_avg=0.0,
                            avg_company_size_employees=0,
                            avg_deal_size_similar_accounts=0.0)
        assert score >= 0.0

    def test_combined_icp_100_size_500_deal_100k(self):
        score = self._score(icp_match_score_avg=100.0,
                            avg_company_size_employees=500,
                            avg_deal_size_similar_accounts=100_000.0)
        # 60 + 25 + 15 = 100
        assert score == 100.0


# ---------------------------------------------------------------------------
# 9. _composite
# ---------------------------------------------------------------------------

class TestComposite:
    def setup_method(self):
        self.a = make_analyzer()

    def test_weights_sum_to_1(self):
        assert abs(0.30 + 0.25 + 0.25 + 0.20 - 1.0) < 1e-9

    def test_composite_formula(self):
        comp = self.a._composite(80.0, 60.0, 70.0, 50.0)
        expected = 80*0.30 + 60*0.25 + 70*0.25 + 50*0.20
        assert comp == pytest.approx(expected, abs=0.1)

    def test_composite_100_all(self):
        assert self.a._composite(100, 100, 100, 100) == 100.0

    def test_composite_0_all(self):
        assert self.a._composite(0, 0, 0, 0) == 0.0

    def test_composite_rounded_to_1_decimal(self):
        comp = self.a._composite(33.3, 33.3, 33.3, 33.3)
        # verify it has at most 1 decimal place
        assert comp == round(comp, 1)

    def test_composite_capped_at_100(self):
        comp = self.a._composite(110, 110, 110, 110)
        assert comp == 100.0

    def test_composite_floor_at_0(self):
        comp = self.a._composite(-10, -10, -10, -10)
        assert comp == 0.0


# ---------------------------------------------------------------------------
# 10. _whitespace_priority branches
# ---------------------------------------------------------------------------

class TestWhitespacePriority:
    def setup_method(self):
        self.a = make_analyzer()

    def _priority(self, composite, triggers=0):
        inp = make_input(buying_trigger_signal_count=triggers)
        return self.a._whitespace_priority(composite, inp)

    def test_low_below_35(self):
        assert self._priority(34.9) == WhitespacePriority.LOW

    def test_low_at_0(self):
        assert self._priority(0.0) == WhitespacePriority.LOW

    def test_medium_at_35(self):
        assert self._priority(35.0) == WhitespacePriority.MEDIUM

    def test_medium_below_55(self):
        assert self._priority(54.9) == WhitespacePriority.MEDIUM

    def test_high_at_55(self):
        assert self._priority(55.0) == WhitespacePriority.HIGH

    def test_high_below_75(self):
        assert self._priority(74.9) == WhitespacePriority.HIGH

    def test_urgent_at_75(self):
        assert self._priority(75.0) == WhitespacePriority.URGENT

    def test_urgent_at_100(self):
        assert self._priority(100.0) == WhitespacePriority.URGENT

    def test_urgent_via_triggers_ge_8(self):
        assert self._priority(0.0, triggers=8) == WhitespacePriority.URGENT

    def test_urgent_via_triggers_10(self):
        assert self._priority(0.0, triggers=10) == WhitespacePriority.URGENT

    def test_triggers_7_does_not_force_urgent(self):
        # triggers=7 < 8, composite=34 → LOW
        assert self._priority(34.0, triggers=7) == WhitespacePriority.LOW

    def test_triggers_8_overrides_low_composite(self):
        assert self._priority(10.0, triggers=8) == WhitespacePriority.URGENT


# ---------------------------------------------------------------------------
# 11. _whitespace_type branches
# ---------------------------------------------------------------------------

class TestWhitespaceType:
    def setup_method(self):
        self.a = make_analyzer()

    def _type(self, **kw):
        return self.a._whitespace_type(make_input(**kw))

    def test_dormant_reactivate_when_never_contacted_lt_30pct_and_tenure_ge_12(self):
        wt = self._type(total_accounts_in_territory=100,
                        accounts_never_contacted=20,   # < 30
                        months_rep_in_territory=12,
                        icp_match_score_avg=80.0,
                        accounts_with_customers=10,
                        accounts_with_active_deals=5,
                        lookalike_customer_match_count=10)
        assert wt == WhitespaceType.DORMANT_REACTIVATE

    def test_dormant_reactivate_tenure_exactly_12(self):
        wt = self._type(total_accounts_in_territory=100,
                        accounts_never_contacted=29,
                        months_rep_in_territory=12,
                        icp_match_score_avg=50.0,
                        accounts_with_customers=2,
                        accounts_with_active_deals=1,
                        lookalike_customer_match_count=2)
        assert wt == WhitespaceType.DORMANT_REACTIVATE

    def test_not_dormant_when_never_contacted_ge_30pct(self):
        wt = self._type(total_accounts_in_territory=100,
                        accounts_never_contacted=30,   # = 30%, not < 30%
                        months_rep_in_territory=12,
                        icp_match_score_avg=80.0,
                        accounts_with_customers=2,
                        accounts_with_active_deals=1,
                        lookalike_customer_match_count=2)
        # should not be dormant; with icp=80 and never_contacted=30≥20 → GEO_EXPAND
        assert wt == WhitespaceType.GEO_EXPAND

    def test_not_dormant_when_tenure_lt_12(self):
        wt = self._type(total_accounts_in_territory=100,
                        accounts_never_contacted=20,
                        months_rep_in_territory=11,
                        icp_match_score_avg=80.0,
                        accounts_with_customers=10,
                        accounts_with_active_deals=5,
                        lookalike_customer_match_count=10)
        # tenure < 12 → not dormant; icp>=70 and never_contacted=20≥20 → GEO_EXPAND
        assert wt == WhitespaceType.GEO_EXPAND

    def test_geo_expand_icp_ge_70_and_never_contacted_ge_20(self):
        wt = self._type(total_accounts_in_territory=100,
                        accounts_never_contacted=25,
                        months_rep_in_territory=6,
                        icp_match_score_avg=70.0,
                        accounts_with_customers=2,
                        accounts_with_active_deals=1,
                        lookalike_customer_match_count=2)
        assert wt == WhitespaceType.GEO_EXPAND

    def test_geo_expand_icp_above_70(self):
        wt = self._type(total_accounts_in_territory=100,
                        accounts_never_contacted=30,
                        months_rep_in_territory=6,
                        icp_match_score_avg=90.0,
                        accounts_with_customers=2,
                        accounts_with_active_deals=1,
                        lookalike_customer_match_count=2)
        assert wt == WhitespaceType.GEO_EXPAND

    def test_not_geo_expand_when_icp_below_70(self):
        # icp<70, never_contacted<20 → check product expand, then segment
        wt = self._type(total_accounts_in_territory=100,
                        accounts_never_contacted=10,
                        months_rep_in_territory=6,
                        icp_match_score_avg=60.0,
                        accounts_with_customers=10,
                        accounts_with_active_deals=5,
                        lookalike_customer_match_count=2)
        assert wt == WhitespaceType.PRODUCT_EXPAND

    def test_not_geo_expand_when_never_contacted_lt_20(self):
        wt = self._type(total_accounts_in_territory=100,
                        accounts_never_contacted=19,
                        months_rep_in_territory=6,
                        icp_match_score_avg=90.0,
                        accounts_with_customers=10,
                        accounts_with_active_deals=5,
                        lookalike_customer_match_count=2)
        # icp>=70, never_contacted<20 → not geo; customers>=5, deals<customers → PRODUCT_EXPAND
        assert wt == WhitespaceType.PRODUCT_EXPAND

    def test_product_expand_customers_ge_5_and_deals_lt_customers(self):
        wt = self._type(total_accounts_in_territory=100,
                        accounts_never_contacted=5,
                        months_rep_in_territory=6,
                        icp_match_score_avg=50.0,
                        accounts_with_customers=10,
                        accounts_with_active_deals=5,
                        lookalike_customer_match_count=2)
        assert wt == WhitespaceType.PRODUCT_EXPAND

    def test_product_expand_deals_equal_customers_not_triggered(self):
        # deals == customers → condition fails
        wt = self._type(total_accounts_in_territory=100,
                        accounts_never_contacted=5,
                        months_rep_in_territory=6,
                        icp_match_score_avg=50.0,
                        accounts_with_customers=5,
                        accounts_with_active_deals=5,
                        lookalike_customer_match_count=6)
        assert wt == WhitespaceType.SEGMENT_EXPAND

    def test_segment_expand_when_lookalike_ge_5(self):
        wt = self._type(total_accounts_in_territory=100,
                        accounts_never_contacted=5,
                        months_rep_in_territory=6,
                        icp_match_score_avg=50.0,
                        accounts_with_customers=2,
                        accounts_with_active_deals=1,
                        lookalike_customer_match_count=5)
        assert wt == WhitespaceType.SEGMENT_EXPAND

    def test_segment_expand_lookalike_above_5(self):
        wt = self._type(total_accounts_in_territory=100,
                        accounts_never_contacted=5,
                        months_rep_in_territory=6,
                        icp_match_score_avg=50.0,
                        accounts_with_customers=2,
                        accounts_with_active_deals=1,
                        lookalike_customer_match_count=10)
        assert wt == WhitespaceType.SEGMENT_EXPAND

    def test_new_logo_when_no_other_condition_met(self):
        wt = self._type(total_accounts_in_territory=100,
                        accounts_never_contacted=5,
                        months_rep_in_territory=6,
                        icp_match_score_avg=50.0,
                        accounts_with_customers=2,
                        accounts_with_active_deals=1,
                        lookalike_customer_match_count=3)
        assert wt == WhitespaceType.NEW_LOGO

    def test_new_logo_zero_everything(self):
        wt = self._type(total_accounts_in_territory=10,
                        accounts_never_contacted=2,
                        months_rep_in_territory=6,
                        icp_match_score_avg=30.0,
                        accounts_with_customers=0,
                        accounts_with_active_deals=0,
                        lookalike_customer_match_count=0)
        assert wt == WhitespaceType.NEW_LOGO


# ---------------------------------------------------------------------------
# 12. _territory_health branches
# ---------------------------------------------------------------------------

class TestTerritoryHealth:
    def setup_method(self):
        self.a = make_analyzer()

    def _health(self, **kw):
        return self.a._territory_health(make_input(**kw))

    def test_zero_total_accounts_underpenetrated(self):
        h = self._health(total_accounts_in_territory=0,
                         accounts_with_customers=0,
                         accounts_with_active_deals=0)
        assert h == TerritoryHealth.UNDERPENETRATED

    def test_underpenetrated_below_20pct(self):
        h = self._health(total_accounts_in_territory=100,
                         accounts_with_customers=10,
                         accounts_with_active_deals=9)  # 19/100 = 0.19
        assert h == TerritoryHealth.UNDERPENETRATED

    def test_underpenetrated_at_0(self):
        h = self._health(total_accounts_in_territory=100,
                         accounts_with_customers=0,
                         accounts_with_active_deals=0)
        assert h == TerritoryHealth.UNDERPENETRATED

    def test_developing_at_exactly_20pct(self):
        h = self._health(total_accounts_in_territory=100,
                         accounts_with_customers=10,
                         accounts_with_active_deals=10)  # 20/100 = 0.20
        assert h == TerritoryHealth.DEVELOPING

    def test_developing_between_20_40(self):
        h = self._health(total_accounts_in_territory=100,
                         accounts_with_customers=20,
                         accounts_with_active_deals=15)  # 35/100 = 0.35
        assert h == TerritoryHealth.DEVELOPING

    def test_optimized_at_exactly_40pct(self):
        h = self._health(total_accounts_in_territory=100,
                         accounts_with_customers=20,
                         accounts_with_active_deals=20)  # 40/100 = 0.40
        assert h == TerritoryHealth.OPTIMIZED

    def test_optimized_between_40_70(self):
        h = self._health(total_accounts_in_territory=100,
                         accounts_with_customers=30,
                         accounts_with_active_deals=30)  # 60/100 = 0.60
        assert h == TerritoryHealth.OPTIMIZED

    def test_saturated_at_exactly_70pct(self):
        h = self._health(total_accounts_in_territory=100,
                         accounts_with_customers=35,
                         accounts_with_active_deals=35)  # 70/100 = 0.70
        assert h == TerritoryHealth.SATURATED

    def test_saturated_above_70(self):
        h = self._health(total_accounts_in_territory=100,
                         accounts_with_customers=50,
                         accounts_with_active_deals=40)  # 90/100 = 0.90
        assert h == TerritoryHealth.SATURATED

    def test_saturated_at_100pct(self):
        h = self._health(total_accounts_in_territory=10,
                         accounts_with_customers=5,
                         accounts_with_active_deals=5)
        assert h == TerritoryHealth.SATURATED


# ---------------------------------------------------------------------------
# 13. _territory_penetration_pct
# ---------------------------------------------------------------------------

class TestTerritoryPenetrationPct:
    def setup_method(self):
        self.a = make_analyzer()

    def _pct(self, **kw):
        return self.a._territory_penetration_pct(make_input(**kw))

    def test_zero_total_returns_0(self):
        assert self._pct(total_accounts_in_territory=0,
                         accounts_with_customers=0,
                         accounts_with_active_deals=0) == 0.0

    def test_basic_penetration(self):
        pct = self._pct(total_accounts_in_territory=100,
                        accounts_with_customers=10,
                        accounts_with_active_deals=10)
        assert pct == pytest.approx(20.0, abs=0.15)

    def test_full_penetration_capped_at_100(self):
        pct = self._pct(total_accounts_in_territory=10,
                        accounts_with_customers=10,
                        accounts_with_active_deals=10)
        assert pct == 100.0

    def test_penetration_rounded_to_1_decimal(self):
        pct = self._pct(total_accounts_in_territory=3,
                        accounts_with_customers=1,
                        accounts_with_active_deals=0)
        assert pct == round(pct, 1)

    def test_zero_customers_zero_deals(self):
        pct = self._pct(total_accounts_in_territory=100,
                        accounts_with_customers=0,
                        accounts_with_active_deals=0)
        assert pct == 0.0


# ---------------------------------------------------------------------------
# 14. _estimated_whitespace_arr
# ---------------------------------------------------------------------------

class TestEstimatedWhitespaceArr:
    def setup_method(self):
        self.a = make_analyzer()

    def _arr(self, **kw):
        return self.a._estimated_whitespace_arr(make_input(**kw))

    def test_basic_whitespace_from_potential_minus_current(self):
        arr = self._arr(territory_revenue_potential=500_000.0,
                        current_territory_revenue=100_000.0,
                        lookalike_customer_match_count=0,
                        buying_trigger_signal_count=0,
                        avg_deal_size_similar_accounts=0.0)
        assert arr == pytest.approx(400_000.0, abs=1.0)

    def test_no_whitespace_when_current_exceeds_potential(self):
        arr = self._arr(territory_revenue_potential=100_000.0,
                        current_territory_revenue=200_000.0,
                        lookalike_customer_match_count=0,
                        buying_trigger_signal_count=0,
                        avg_deal_size_similar_accounts=0.0)
        assert arr == 0.0

    def test_signal_arr_used_when_larger(self):
        # potential-current = 0; signal_arr = (5+5)*50000*0.15 = 75000
        arr = self._arr(territory_revenue_potential=0.0,
                        current_territory_revenue=0.0,
                        lookalike_customer_match_count=5,
                        buying_trigger_signal_count=5,
                        avg_deal_size_similar_accounts=50_000.0)
        assert arr == pytest.approx(75_000.0, abs=1.0)

    def test_max_of_whitespace_and_signal_arr(self):
        # whitespace=400k, signal_arr=(3+2)*40000*0.15=30000 → max=400k
        arr = self._arr(territory_revenue_potential=500_000.0,
                        current_territory_revenue=100_000.0,
                        lookalike_customer_match_count=3,
                        buying_trigger_signal_count=2,
                        avg_deal_size_similar_accounts=40_000.0)
        assert arr == pytest.approx(400_000.0, abs=1.0)

    def test_zero_revenue_potential_uses_signal_arr(self):
        arr = self._arr(territory_revenue_potential=0.0,
                        current_territory_revenue=0.0,
                        lookalike_customer_match_count=10,
                        buying_trigger_signal_count=10,
                        avg_deal_size_similar_accounts=100_000.0)
        expected = 20 * 100_000 * 0.15
        assert arr == pytest.approx(expected, abs=1.0)

    def test_result_rounded_to_2_decimals(self):
        arr = self._arr(territory_revenue_potential=100_001.0,
                        current_territory_revenue=0.0,
                        lookalike_customer_match_count=0,
                        buying_trigger_signal_count=0,
                        avg_deal_size_similar_accounts=0.0)
        assert arr == round(arr, 2)

    def test_negative_potential_gives_zero(self):
        arr = self._arr(territory_revenue_potential=-100.0,
                        current_territory_revenue=0.0,
                        lookalike_customer_match_count=0,
                        buying_trigger_signal_count=0,
                        avg_deal_size_similar_accounts=0.0)
        assert arr == 0.0


# ---------------------------------------------------------------------------
# 15. _whitespace_action branches
# ---------------------------------------------------------------------------

class TestWhitespaceAction:
    def setup_method(self):
        self.a = make_analyzer()

    def _action(self, priority, needs_now):
        return self.a._whitespace_action(priority, needs_now)

    def test_needs_now_true_always_immediate_focus(self):
        for p in WhitespacePriority:
            assert self._action(p, True) == WhitespaceAction.IMMEDIATE_FOCUS

    def test_urgent_without_needs_now_immediate_focus(self):
        assert self._action(WhitespacePriority.URGENT, False) == WhitespaceAction.IMMEDIATE_FOCUS

    def test_high_without_needs_now_prioritize(self):
        assert self._action(WhitespacePriority.HIGH, False) == WhitespaceAction.PRIORITIZE

    def test_medium_without_needs_now_prospect(self):
        assert self._action(WhitespacePriority.MEDIUM, False) == WhitespaceAction.PROSPECT

    def test_low_without_needs_now_nurture(self):
        assert self._action(WhitespacePriority.LOW, False) == WhitespaceAction.NURTURE


# ---------------------------------------------------------------------------
# 16. is_high_potential_territory
# ---------------------------------------------------------------------------

class TestIsHighPotential:
    def setup_method(self):
        self.a = make_analyzer()

    def test_high_potential_via_composite_ge_60(self):
        # Force composite >= 60: high growth, seasonal, conference, no competition, lots of untouched
        result = self.a.analyze(make_input(
            territory_id="HP1",
            industry_growth_rate_pct=20,
            seasonal_buying_signal=1,
            conference_event_signal=1,
            competitor_present_pct=10,
            total_accounts_in_territory=100,
            accounts_never_contacted=80,
            lookalike_customer_match_count=6,
            buying_trigger_signal_count=4,  # < 5 so flag is from composite
            icp_match_score_avg=80,
            avg_company_size_employees=500,
            avg_deal_size_similar_accounts=100_000,
            outreach_coverage_pct=10,
            months_rep_in_territory=6,
            territory_quota_attainment_pct=40,
            executive_referral_count=5,
        ))
        assert result.whitespace_composite >= 60.0
        assert result.is_high_potential_territory is True

    def test_high_potential_via_triggers_ge_5(self):
        result = self.a.analyze(make_input(
            territory_id="HP2",
            buying_trigger_signal_count=5,
            # keep composite low
            industry_growth_rate_pct=0,
            seasonal_buying_signal=0,
            conference_event_signal=0,
            total_accounts_in_territory=100,
            accounts_never_contacted=5,
            lookalike_customer_match_count=0,
            icp_match_score_avg=0,
            avg_company_size_employees=10,
            avg_deal_size_similar_accounts=1000,
            outreach_coverage_pct=90,
            months_rep_in_territory=6,
            territory_quota_attainment_pct=80,
            executive_referral_count=0,
            competitor_present_pct=50,
        ))
        assert result.is_high_potential_territory is True

    def test_not_high_potential_low_composite_low_triggers(self):
        result = self.a.analyze(make_input(
            territory_id="LP1",
            buying_trigger_signal_count=0,
            industry_growth_rate_pct=0,
            seasonal_buying_signal=0,
            conference_event_signal=0,
            total_accounts_in_territory=100,
            accounts_never_contacted=5,
            lookalike_customer_match_count=0,
            icp_match_score_avg=0,
            avg_company_size_employees=10,
            avg_deal_size_similar_accounts=1000,
            outreach_coverage_pct=90,
            months_rep_in_territory=6,
            territory_quota_attainment_pct=80,
            executive_referral_count=0,
            competitor_present_pct=50,
        ))
        assert result.whitespace_composite < 60.0
        assert result.is_high_potential_territory is False

    def test_high_potential_triggers_exactly_5(self):
        result = self.a.analyze(make_input(
            territory_id="HP3",
            buying_trigger_signal_count=5,
            industry_growth_rate_pct=0,
            seasonal_buying_signal=0,
            conference_event_signal=0,
            total_accounts_in_territory=100,
            accounts_never_contacted=5,
            lookalike_customer_match_count=0,
            icp_match_score_avg=0,
            avg_company_size_employees=10,
            avg_deal_size_similar_accounts=1000,
            outreach_coverage_pct=90,
            months_rep_in_territory=6,
            territory_quota_attainment_pct=80,
            executive_referral_count=0,
            competitor_present_pct=50,
        ))
        assert result.is_high_potential_territory is True

    def test_triggers_4_composite_below_60_not_high_potential(self):
        result = self.a.analyze(make_input(
            territory_id="LP2",
            buying_trigger_signal_count=4,
            industry_growth_rate_pct=0,
            seasonal_buying_signal=0,
            conference_event_signal=0,
            total_accounts_in_territory=100,
            accounts_never_contacted=5,
            lookalike_customer_match_count=0,
            icp_match_score_avg=0,
            avg_company_size_employees=10,
            avg_deal_size_similar_accounts=1000,
            outreach_coverage_pct=90,
            months_rep_in_territory=6,
            territory_quota_attainment_pct=80,
            executive_referral_count=0,
            competitor_present_pct=50,
        ))
        assert result.is_high_potential_territory is False


# ---------------------------------------------------------------------------
# 17. needs_immediate_prospecting
# ---------------------------------------------------------------------------

class TestNeedsImmediateProspecting:
    def setup_method(self):
        self.a = make_analyzer()

    def _analyze_needs_now(self, **kw):
        return self.a.analyze(make_input(**kw)).needs_immediate_prospecting

    def test_composite_ge_75_triggers_immediate(self):
        # Build high composite
        result = self.a.analyze(make_input(
            territory_id="N1",
            industry_growth_rate_pct=20,
            seasonal_buying_signal=1,
            conference_event_signal=1,
            competitor_present_pct=10,
            total_accounts_in_territory=100,
            accounts_never_contacted=80,
            lookalike_customer_match_count=6,
            buying_trigger_signal_count=4,
            icp_match_score_avg=80,
            avg_company_size_employees=500,
            avg_deal_size_similar_accounts=100_000,
            outreach_coverage_pct=10,
            months_rep_in_territory=2,
            territory_quota_attainment_pct=40,
            executive_referral_count=5,
        ))
        if result.whitespace_composite >= 75.0:
            assert result.needs_immediate_prospecting is True

    def test_seasonal_and_composite_ge_55_triggers_immediate(self):
        # composite >= 55 (not >= 75) with seasonal=1
        result = self.a.analyze(make_input(
            territory_id="N2",
            industry_growth_rate_pct=10,
            seasonal_buying_signal=1,
            conference_event_signal=0,
            competitor_present_pct=40,
            total_accounts_in_territory=100,
            accounts_never_contacted=40,
            lookalike_customer_match_count=3,
            buying_trigger_signal_count=3,
            icp_match_score_avg=60,
            avg_company_size_employees=500,
            avg_deal_size_similar_accounts=60_000,
            outreach_coverage_pct=40,
            months_rep_in_territory=6,
            territory_quota_attainment_pct=60,
            executive_referral_count=2,
        ))
        if result.whitespace_composite >= 55.0 and not (result.whitespace_composite >= 75.0):
            assert result.needs_immediate_prospecting is True

    def test_buying_trigger_ge_8_triggers_immediate(self):
        result = self.a.analyze(make_input(
            territory_id="N3",
            buying_trigger_signal_count=8,
            industry_growth_rate_pct=0,
            seasonal_buying_signal=0,
            conference_event_signal=0,
            total_accounts_in_territory=100,
            accounts_never_contacted=5,
            lookalike_customer_match_count=0,
            icp_match_score_avg=0,
            avg_company_size_employees=10,
            avg_deal_size_similar_accounts=1000,
            outreach_coverage_pct=90,
            months_rep_in_territory=6,
            territory_quota_attainment_pct=80,
            executive_referral_count=0,
            competitor_present_pct=50,
        ))
        assert result.needs_immediate_prospecting is True

    def test_triggers_exactly_8_immediate(self):
        result = self.a.analyze(make_input(
            territory_id="N4",
            buying_trigger_signal_count=8,
        ))
        assert result.needs_immediate_prospecting is True

    def test_triggers_10_immediate(self):
        result = self.a.analyze(make_input(
            territory_id="N5",
            buying_trigger_signal_count=10,
        ))
        assert result.needs_immediate_prospecting is True

    def test_not_immediate_low_everything(self):
        result = self.a.analyze(make_input(
            territory_id="N6",
            buying_trigger_signal_count=0,
            industry_growth_rate_pct=0,
            seasonal_buying_signal=0,
            conference_event_signal=0,
            total_accounts_in_territory=100,
            accounts_never_contacted=5,
            lookalike_customer_match_count=0,
            icp_match_score_avg=0,
            avg_company_size_employees=10,
            avg_deal_size_similar_accounts=1000,
            outreach_coverage_pct=90,
            months_rep_in_territory=6,
            territory_quota_attainment_pct=80,
            executive_referral_count=0,
            competitor_present_pct=50,
        ))
        assert result.needs_immediate_prospecting is False

    def test_seasonal_with_composite_below_55_not_immediate(self):
        # seasonal=1 but composite < 55 → should NOT be immediate unless composite>=75 or triggers>=8
        result = self.a.analyze(make_input(
            territory_id="N7",
            buying_trigger_signal_count=0,
            industry_growth_rate_pct=0,
            seasonal_buying_signal=1,
            conference_event_signal=0,
            total_accounts_in_territory=100,
            accounts_never_contacted=5,
            lookalike_customer_match_count=0,
            icp_match_score_avg=0,
            avg_company_size_employees=10,
            avg_deal_size_similar_accounts=1000,
            outreach_coverage_pct=90,
            months_rep_in_territory=6,
            territory_quota_attainment_pct=80,
            executive_referral_count=0,
            competitor_present_pct=50,
        ))
        assert result.whitespace_composite < 55.0
        assert result.needs_immediate_prospecting is False

    def test_triggers_7_not_immediate_low_composite(self):
        result = self.a.analyze(make_input(
            territory_id="N8",
            buying_trigger_signal_count=7,
            industry_growth_rate_pct=0,
            seasonal_buying_signal=0,
            conference_event_signal=0,
            total_accounts_in_territory=100,
            accounts_never_contacted=5,
            lookalike_customer_match_count=0,
            icp_match_score_avg=0,
            avg_company_size_employees=10,
            avg_deal_size_similar_accounts=1000,
            outreach_coverage_pct=90,
            months_rep_in_territory=6,
            territory_quota_attainment_pct=80,
            executive_referral_count=0,
            competitor_present_pct=50,
        ))
        assert result.needs_immediate_prospecting is False


# ---------------------------------------------------------------------------
# 18. analyze() – public API
# ---------------------------------------------------------------------------

class TestAnalyze:
    def setup_method(self):
        self.a = make_analyzer()

    def test_returns_territory_whitespace_result(self):
        r = self.a.analyze(make_input())
        assert isinstance(r, TerritoryWhitespaceResult)

    def test_result_stored_in_internal_list(self):
        self.a.analyze(make_input(territory_id="T1"))
        assert len(self.a._results) == 1

    def test_multiple_analyze_cumulates(self):
        for i in range(5):
            self.a.analyze(make_input(territory_id=f"T{i}"))
        assert len(self.a._results) == 5

    def test_result_territory_id_preserved(self):
        r = self.a.analyze(make_input(territory_id="XYZ"))
        assert r.territory_id == "XYZ"

    def test_result_territory_name_preserved(self):
        r = self.a.analyze(make_input(territory_name="EMEA"))
        assert r.territory_name == "EMEA"

    def test_result_scores_in_valid_range(self):
        r = self.a.analyze(make_input())
        assert 0.0 <= r.opportunity_density_score <= 100.0
        assert 0.0 <= r.market_timing_score <= 100.0
        assert 0.0 <= r.territory_coverage_score <= 100.0
        assert 0.0 <= r.icp_alignment_score <= 100.0
        assert 0.0 <= r.whitespace_composite <= 100.0

    def test_result_composite_matches_formula(self):
        r = self.a.analyze(make_input())
        expected = (r.opportunity_density_score * 0.30
                    + r.market_timing_score * 0.25
                    + r.territory_coverage_score * 0.25
                    + r.icp_alignment_score * 0.20)
        assert r.whitespace_composite == pytest.approx(round(min(100.0, max(0.0, expected)), 1), abs=0.15)

    def test_result_penetration_pct_non_negative(self):
        r = self.a.analyze(make_input())
        assert r.territory_penetration_pct >= 0.0

    def test_result_estimated_arr_non_negative(self):
        r = self.a.analyze(make_input())
        assert r.estimated_whitespace_arr >= 0.0


# ---------------------------------------------------------------------------
# 19. analyze_batch() – batch API
# ---------------------------------------------------------------------------

class TestAnalyzeBatch:
    def setup_method(self):
        self.a = make_analyzer()

    def test_returns_list(self):
        results = self.a.analyze_batch([make_input(territory_id="T1"),
                                         make_input(territory_id="T2")])
        assert isinstance(results, list)

    def test_returns_correct_count(self):
        inputs = [make_input(territory_id=f"T{i}") for i in range(7)]
        results = self.a.analyze_batch(inputs)
        assert len(results) == 7

    def test_empty_batch_returns_empty_list(self):
        results = self.a.analyze_batch([])
        assert results == []

    def test_all_results_are_correct_type(self):
        results = self.a.analyze_batch([make_input(territory_id=f"T{i}") for i in range(3)])
        assert all(isinstance(r, TerritoryWhitespaceResult) for r in results)

    def test_batch_cumulates_in_internal_list(self):
        self.a.analyze_batch([make_input(territory_id=f"T{i}") for i in range(4)])
        assert len(self.a._results) == 4

    def test_batch_then_analyze_cumulates(self):
        self.a.analyze_batch([make_input(territory_id="T1"), make_input(territory_id="T2")])
        self.a.analyze(make_input(territory_id="T3"))
        assert len(self.a._results) == 3

    def test_single_item_batch(self):
        results = self.a.analyze_batch([make_input(territory_id="SOLO")])
        assert len(results) == 1
        assert results[0].territory_id == "SOLO"


# ---------------------------------------------------------------------------
# 20. reset()
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_clears_results(self):
        a = make_analyzer()
        for i in range(5):
            a.analyze(make_input(territory_id=f"T{i}"))
        a.reset()
        assert len(a._results) == 0

    def test_reset_then_analyze(self):
        a = make_analyzer()
        a.analyze(make_input(territory_id="T1"))
        a.reset()
        a.analyze(make_input(territory_id="T2"))
        assert len(a._results) == 1

    def test_reset_on_empty_is_no_op(self):
        a = make_analyzer()
        a.reset()
        assert len(a._results) == 0

    def test_summary_empty_after_reset(self):
        a = make_analyzer()
        a.analyze(make_input())
        a.reset()
        assert a.summary()["total"] == 0


# ---------------------------------------------------------------------------
# 21. Properties
# ---------------------------------------------------------------------------

class TestProperties:
    def setup_method(self):
        self.a = make_analyzer()

    def test_high_potential_territories_empty_initially(self):
        assert self.a.high_potential_territories == []

    def test_immediate_prospecting_queue_empty_initially(self):
        assert self.a.immediate_prospecting_queue == []

    def test_total_estimated_whitespace_arr_zero_initially(self):
        assert self.a.total_estimated_whitespace_arr == 0.0

    def test_avg_whitespace_composite_zero_initially(self):
        assert self.a.avg_whitespace_composite == 0.0

    def test_high_potential_territories_filtered(self):
        # low: triggers=0, low composite
        self.a.analyze(make_input(territory_id="LOW",
                                   buying_trigger_signal_count=0,
                                   industry_growth_rate_pct=0,
                                   seasonal_buying_signal=0,
                                   conference_event_signal=0,
                                   total_accounts_in_territory=100,
                                   accounts_never_contacted=5,
                                   lookalike_customer_match_count=0,
                                   icp_match_score_avg=0,
                                   avg_company_size_employees=10,
                                   avg_deal_size_similar_accounts=1000,
                                   outreach_coverage_pct=90,
                                   months_rep_in_territory=6,
                                   territory_quota_attainment_pct=80,
                                   executive_referral_count=0,
                                   competitor_present_pct=50))
        # high: triggers=5
        self.a.analyze(make_input(territory_id="HIGH", buying_trigger_signal_count=5))
        hp = self.a.high_potential_territories
        assert len(hp) == 1
        assert hp[0].territory_id == "HIGH"

    def test_immediate_prospecting_queue_filtered(self):
        self.a.analyze(make_input(territory_id="NO",
                                   buying_trigger_signal_count=0,
                                   industry_growth_rate_pct=0,
                                   seasonal_buying_signal=0,
                                   conference_event_signal=0,
                                   total_accounts_in_territory=100,
                                   accounts_never_contacted=5,
                                   lookalike_customer_match_count=0,
                                   icp_match_score_avg=0,
                                   avg_company_size_employees=10,
                                   avg_deal_size_similar_accounts=1000,
                                   outreach_coverage_pct=90,
                                   months_rep_in_territory=6,
                                   territory_quota_attainment_pct=80,
                                   executive_referral_count=0,
                                   competitor_present_pct=50))
        self.a.analyze(make_input(territory_id="YES", buying_trigger_signal_count=8))
        iq = self.a.immediate_prospecting_queue
        assert len(iq) == 1
        assert iq[0].territory_id == "YES"

    def test_total_estimated_whitespace_arr_sums(self):
        a = make_analyzer()
        a.analyze(make_input(territory_id="T1",
                              territory_revenue_potential=500_000.0,
                              current_territory_revenue=100_000.0,
                              lookalike_customer_match_count=0,
                              buying_trigger_signal_count=0,
                              avg_deal_size_similar_accounts=0.0))
        a.analyze(make_input(territory_id="T2",
                              territory_revenue_potential=300_000.0,
                              current_territory_revenue=50_000.0,
                              lookalike_customer_match_count=0,
                              buying_trigger_signal_count=0,
                              avg_deal_size_similar_accounts=0.0))
        total = a.total_estimated_whitespace_arr
        assert total == pytest.approx(650_000.0, abs=1.0)

    def test_avg_whitespace_composite_single(self):
        a = make_analyzer()
        r = a.analyze(make_input())
        assert a.avg_whitespace_composite == r.whitespace_composite

    def test_avg_whitespace_composite_multiple(self):
        a = make_analyzer()
        for i in range(3):
            a.analyze(make_input(territory_id=f"T{i}"))
        s = a.summary()
        assert a.avg_whitespace_composite == pytest.approx(s["avg_whitespace_composite"], abs=0.1)

    def test_total_arr_rounded_to_2_decimals(self):
        a = make_analyzer()
        a.analyze(make_input(territory_id="T1",
                              territory_revenue_potential=100_000.01,
                              current_territory_revenue=0.0,
                              lookalike_customer_match_count=0,
                              buying_trigger_signal_count=0,
                              avg_deal_size_similar_accounts=0.0))
        total = a.total_estimated_whitespace_arr
        assert total == round(total, 2)


# ---------------------------------------------------------------------------
# 22. Full integration / end-to-end tests
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_full_pipeline_no_exceptions(self):
        a = make_analyzer()
        inputs = [make_input(territory_id=f"T{i}", industry_growth_rate_pct=i * 5)
                  for i in range(6)]
        results = a.analyze_batch(inputs)
        summary = a.summary()
        assert summary["total"] == 6
        assert len(results) == 6

    def test_territory_result_has_valid_enum_values(self):
        a = make_analyzer()
        r = a.analyze(make_input())
        assert r.whitespace_priority in WhitespacePriority
        assert r.whitespace_type in WhitespaceType
        assert r.territory_health in TerritoryHealth
        assert r.whitespace_action in WhitespaceAction

    def test_urgent_action_when_urgent_priority_and_no_needs_now(self):
        a = make_analyzer()
        # Force urgent priority via composite >= 75
        r = a.analyze(make_input(
            territory_id="URG",
            industry_growth_rate_pct=20,
            seasonal_buying_signal=1,
            conference_event_signal=1,
            competitor_present_pct=10,
            total_accounts_in_territory=100,
            accounts_never_contacted=80,
            lookalike_customer_match_count=6,
            buying_trigger_signal_count=4,
            icp_match_score_avg=80,
            avg_company_size_employees=500,
            avg_deal_size_similar_accounts=100_000,
            outreach_coverage_pct=10,
            months_rep_in_territory=2,
            territory_quota_attainment_pct=40,
            executive_referral_count=5,
        ))
        if r.whitespace_priority == WhitespacePriority.URGENT:
            assert r.whitespace_action == WhitespaceAction.IMMEDIATE_FOCUS

    def test_summary_after_reset_is_empty(self):
        a = make_analyzer()
        a.analyze_batch([make_input(territory_id=f"T{i}") for i in range(5)])
        a.reset()
        s = a.summary()
        assert s["total"] == 0

    def test_diverse_batch_summary_sums_correct(self):
        a = make_analyzer()
        # high triggers → urgent
        a.analyze(make_input(territory_id="T1", buying_trigger_signal_count=10))
        # low everything → low priority
        a.analyze(make_input(territory_id="T2",
                              buying_trigger_signal_count=0,
                              industry_growth_rate_pct=0,
                              seasonal_buying_signal=0,
                              conference_event_signal=0,
                              total_accounts_in_territory=100,
                              accounts_never_contacted=5,
                              lookalike_customer_match_count=0,
                              icp_match_score_avg=0,
                              avg_company_size_employees=10,
                              avg_deal_size_similar_accounts=1000,
                              outreach_coverage_pct=90,
                              months_rep_in_territory=6,
                              territory_quota_attainment_pct=80,
                              executive_referral_count=0,
                              competitor_present_pct=50))
        s = a.summary()
        assert s["total"] == 2
        assert sum(s["priority_counts"].values()) == 2

    def test_to_dict_enum_values_are_strings(self):
        a = make_analyzer()
        d = a.analyze(make_input()).to_dict()
        for key in ("whitespace_priority", "whitespace_type", "territory_health", "whitespace_action"):
            assert isinstance(d[key], str), f"{key} should be a string in to_dict()"

    def test_to_dict_not_same_object_as_result(self):
        a = make_analyzer()
        r = a.analyze(make_input())
        d1 = r.to_dict()
        d2 = r.to_dict()
        assert d1 == d2  # idempotent

    def test_multiple_analyzers_independent(self):
        a1 = make_analyzer()
        a2 = make_analyzer()
        a1.analyze(make_input(territory_id="A1"))
        assert len(a2._results) == 0

    def test_penetration_pct_in_result(self):
        a = make_analyzer()
        r = a.analyze(make_input(total_accounts_in_territory=100,
                                  accounts_with_customers=10,
                                  accounts_with_active_deals=10))
        assert r.territory_penetration_pct == pytest.approx(20.0, abs=0.15)

    def test_whitespace_priority_values_in_summary_priority_counts(self):
        a = make_analyzer()
        a.analyze_batch([make_input(territory_id=f"T{i}") for i in range(3)])
        s = a.summary()
        for k in s["priority_counts"]:
            assert k in {p.value for p in WhitespacePriority}

    def test_summary_type_counts_valid_values(self):
        a = make_analyzer()
        a.analyze_batch([make_input(territory_id=f"T{i}") for i in range(3)])
        s = a.summary()
        valid_types = {t.value for t in WhitespaceType}
        for k in s["type_counts"]:
            assert k in valid_types

    def test_summary_health_counts_valid_values(self):
        a = make_analyzer()
        a.analyze_batch([make_input(territory_id=f"T{i}") for i in range(3)])
        s = a.summary()
        valid_health = {h.value for h in TerritoryHealth}
        for k in s["health_counts"]:
            assert k in valid_health

    def test_summary_action_counts_valid_values(self):
        a = make_analyzer()
        a.analyze_batch([make_input(territory_id=f"T{i}") for i in range(3)])
        s = a.summary()
        valid_actions = {ac.value for ac in WhitespaceAction}
        for k in s["action_counts"]:
            assert k in valid_actions

    def test_avg_scores_in_summary_are_floats(self):
        a = make_analyzer()
        a.analyze(make_input())
        s = a.summary()
        for key in ("avg_whitespace_composite", "avg_opportunity_density_score",
                    "avg_market_timing_score", "avg_territory_coverage_score",
                    "avg_icp_alignment_score"):
            assert isinstance(s[key], float), f"{key} should be float"


# ---------------------------------------------------------------------------
# 23. Boundary and edge-case tests
# ---------------------------------------------------------------------------

class TestBoundaryAndEdgeCases:
    def setup_method(self):
        self.a = make_analyzer()

    def test_zero_total_accounts_no_crash(self):
        r = self.a.analyze(make_input(total_accounts_in_territory=0,
                                       accounts_with_customers=0,
                                       accounts_with_active_deals=0,
                                       accounts_never_contacted=0))
        assert r is not None

    def test_very_large_inputs_no_crash(self):
        r = self.a.analyze(make_input(
            total_accounts_in_territory=1_000_000,
            accounts_with_active_deals=100_000,
            accounts_with_customers=100_000,
            accounts_never_contacted=800_000,
            lookalike_customer_match_count=50_000,
            buying_trigger_signal_count=100_000,
            executive_referral_count=10_000,
            territory_revenue_potential=1_000_000_000.0,
            current_territory_revenue=100_000_000.0,
        ))
        assert 0.0 <= r.whitespace_composite <= 100.0
        assert r.estimated_whitespace_arr >= 0.0

    def test_icp_match_score_100(self):
        r = self.a.analyze(make_input(icp_match_score_avg=100.0,
                                       avg_company_size_employees=500,
                                       avg_deal_size_similar_accounts=200_000))
        assert r.icp_alignment_score <= 100.0

    def test_icp_match_score_0(self):
        r = self.a.analyze(make_input(icp_match_score_avg=0.0,
                                       avg_company_size_employees=5,
                                       avg_deal_size_similar_accounts=0))
        assert r.icp_alignment_score >= 0.0

    def test_outreach_coverage_100_percent(self):
        r = self.a.analyze(make_input(outreach_coverage_pct=100.0))
        assert r.territory_coverage_score >= 0.0

    def test_outreach_coverage_0_percent(self):
        r = self.a.analyze(make_input(outreach_coverage_pct=0.0,
                                       months_rep_in_territory=6,
                                       territory_quota_attainment_pct=60.0))
        assert r.territory_coverage_score == pytest.approx(100.0, abs=0.15)

    def test_composite_always_in_0_100(self):
        for _ in range(20):
            r = self.a.analyze(make_input())
            assert 0.0 <= r.whitespace_composite <= 100.0

    def test_all_signals_on_maximum_score(self):
        r = self.a.analyze(make_input(
            total_accounts_in_territory=100,
            accounts_never_contacted=100,
            lookalike_customer_match_count=10,
            buying_trigger_signal_count=15,
            executive_referral_count=10,
            industry_growth_rate_pct=30,
            seasonal_buying_signal=1,
            conference_event_signal=1,
            competitor_present_pct=5,
            icp_match_score_avg=100,
            avg_company_size_employees=500,
            avg_deal_size_similar_accounts=200_000,
            outreach_coverage_pct=0,
            months_rep_in_territory=1,
            territory_quota_attainment_pct=0,
        ))
        assert r.whitespace_composite == 100.0
        assert r.whitespace_priority == WhitespacePriority.URGENT
        assert r.whitespace_action == WhitespaceAction.IMMEDIATE_FOCUS
        assert r.is_high_potential_territory is True
        assert r.needs_immediate_prospecting is True

    def test_all_signals_minimum_score(self):
        r = self.a.analyze(make_input(
            total_accounts_in_territory=100,
            accounts_never_contacted=0,
            lookalike_customer_match_count=0,
            buying_trigger_signal_count=0,
            executive_referral_count=0,
            industry_growth_rate_pct=0,
            seasonal_buying_signal=0,
            conference_event_signal=0,
            competitor_present_pct=100,
            icp_match_score_avg=0,
            avg_company_size_employees=5,
            avg_deal_size_similar_accounts=0,
            outreach_coverage_pct=100,
            months_rep_in_territory=6,
            territory_quota_attainment_pct=100,
        ))
        assert r.whitespace_composite >= 0.0
        assert r.whitespace_priority == WhitespacePriority.LOW
        assert r.whitespace_action == WhitespaceAction.NURTURE

    def test_summary_averages_computed_correctly(self):
        a = make_analyzer()
        # All identical inputs → averages equal individual scores
        r = a.analyze(make_input(territory_id="T1"))
        a.analyze(make_input(territory_id="T2"))  # same params
        s = a.summary()
        # With two identical inputs, averages should equal individual score
        assert s["avg_opportunity_density_score"] == pytest.approx(r.opportunity_density_score, abs=0.2)

    def test_competitor_exactly_20_adds_5(self):
        score = self.a._market_timing_score(make_input(
            industry_growth_rate_pct=0,
            seasonal_buying_signal=0,
            conference_event_signal=0,
            competitor_present_pct=20.0
        ))
        assert score == 35.0

    def test_competitor_exactly_60_subtracts_10(self):
        score = self.a._market_timing_score(make_input(
            industry_growth_rate_pct=0,
            seasonal_buying_signal=0,
            conference_event_signal=0,
            competitor_present_pct=60.0
        ))
        assert score == 20.0

    def test_tenure_exactly_3_adds_10(self):
        score = self.a._territory_coverage_score(make_input(
            outreach_coverage_pct=60.0,
            months_rep_in_territory=3,
            territory_quota_attainment_pct=60.0
        ))
        assert score == pytest.approx(50.0, abs=0.15)

    def test_tenure_exactly_4_neutral(self):
        score = self.a._territory_coverage_score(make_input(
            outreach_coverage_pct=60.0,
            months_rep_in_territory=4,
            territory_quota_attainment_pct=60.0
        ))
        assert score == pytest.approx(40.0, abs=0.15)

    def test_growth_exactly_19_9_adds_20(self):
        score = self.a._market_timing_score(make_input(
            industry_growth_rate_pct=19.9,
            seasonal_buying_signal=0,
            conference_event_signal=0,
            competitor_present_pct=30.0
        ))
        assert score == 50.0

    def test_product_expand_customers_exactly_5_and_deals_4(self):
        wt = self.a._whitespace_type(make_input(
            total_accounts_in_territory=100,
            accounts_never_contacted=5,
            months_rep_in_territory=6,
            icp_match_score_avg=50.0,
            accounts_with_customers=5,
            accounts_with_active_deals=4,
            lookalike_customer_match_count=2,
        ))
        assert wt == WhitespaceType.PRODUCT_EXPAND

    def test_product_expand_customers_4_not_triggered(self):
        # customers < 5 → not product expand; lookalike<5 → new_logo
        wt = self.a._whitespace_type(make_input(
            total_accounts_in_territory=100,
            accounts_never_contacted=5,
            months_rep_in_territory=6,
            icp_match_score_avg=50.0,
            accounts_with_customers=4,
            accounts_with_active_deals=2,
            lookalike_customer_match_count=2,
        ))
        assert wt == WhitespaceType.NEW_LOGO

    def test_dormant_boundary_never_contacted_exactly_29_pct_tenure_12(self):
        # 29% never contacted (strictly less than 30%) with tenure=12 → dormant
        wt = self.a._whitespace_type(make_input(
            total_accounts_in_territory=100,
            accounts_never_contacted=29,
            months_rep_in_territory=12,
            icp_match_score_avg=80.0,
            accounts_with_customers=1,
            accounts_with_active_deals=0,
            lookalike_customer_match_count=1,
        ))
        assert wt == WhitespaceType.DORMANT_REACTIVATE

    def test_deal_size_exactly_49999_no_bonus(self):
        score = self.a._icp_alignment_score(make_input(
            icp_match_score_avg=0.0,
            avg_company_size_employees=10,
            avg_deal_size_similar_accounts=49_999.0,
        ))
        assert score == pytest.approx(0.0, abs=0.15)

    def test_deal_size_exactly_50000_adds_8(self):
        score = self.a._icp_alignment_score(make_input(
            icp_match_score_avg=0.0,
            avg_company_size_employees=10,
            avg_deal_size_similar_accounts=50_000.0,
        ))
        assert score == pytest.approx(8.0, abs=0.15)

    def test_deal_size_exactly_99999_adds_8(self):
        score = self.a._icp_alignment_score(make_input(
            icp_match_score_avg=0.0,
            avg_company_size_employees=10,
            avg_deal_size_similar_accounts=99_999.0,
        ))
        assert score == pytest.approx(8.0, abs=0.15)

    def test_deal_size_exactly_100000_adds_15(self):
        score = self.a._icp_alignment_score(make_input(
            icp_match_score_avg=0.0,
            avg_company_size_employees=10,
            avg_deal_size_similar_accounts=100_000.0,
        ))
        assert score == pytest.approx(15.0, abs=0.15)
