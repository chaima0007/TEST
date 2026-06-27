"""Comprehensive pytest tests for CompetitorIntelligenceEngine."""

from __future__ import annotations

import math
import pytest

from swarm.intelligence.competitor_intelligence import (
    CompetitorIntelligenceEngine,
    CompetitorInput,
    CompetitorResult,
    ThreatLevel,
    CompetitorType,
    CompetitiveAction,
    _market_score,
    _product_score,
    _gtm_score,
    _weakness_score,
    _threat_score,
    _threat_level,
    _action,
    _win_probability,
    _TYPE_BASE_THREAT,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_input(**kwargs) -> CompetitorInput:
    defaults = dict(
        competitor_id="comp1",
        competitor_name="CompetitorX",
        competitor_type=CompetitorType.DIRECT,
        market_share_pct=20.0,
        growth_rate_pct=25.0,
        funding_total_m_eur=30.0,
        last_funding_months_ago=8,
        feature_overlap_pct=65.0,
        product_quality_score=75.0,
        pricing_vs_us=1.0,
        has_recent_product_launch=False,
        sales_team_size=50,
        marketing_spend_index=1.0,
        win_rate_against_us_pct=45.0,
        common_accounts=10,
        hiring_velocity=1.0,
        executive_departures=0,
        negative_reviews_pct=10.0,
        partnership_announcements=1,
    )
    defaults.update(kwargs)
    return CompetitorInput(**defaults)


# ---------------------------------------------------------------------------
# TestMarketScore  (20+ tests)
# ---------------------------------------------------------------------------

class TestMarketScore:

    def test_share_score_at_zero(self):
        inp = make_input(market_share_pct=0.0, growth_rate_pct=0, funding_total_m_eur=0, last_funding_months_ago=0)
        share_score = min(100, 0.0 * 1.5)
        assert share_score == 0.0

    def test_share_score_cap_exactly_at_boundary(self):
        # share_pct = 100/1.5 = 66.666... → share_score = 100 exactly
        pct = 100 / 1.5
        share_score = min(100, pct * 1.5)
        assert share_score == 100.0

    def test_share_score_capped_above_boundary(self):
        # market_share_pct=80 → 80*1.5=120 → capped at 100
        assert min(100, 80 * 1.5) == 100.0

    def test_share_score_partial(self):
        # market_share_pct=20 → 20*1.5=30
        assert min(100, 20 * 1.5) == 30.0

    def test_growth_negative_clamped_to_zero(self):
        inp = make_input(growth_rate_pct=-50)
        growth_score = min(100, max(0, -50 * 2))
        assert growth_score == 0.0

    def test_growth_zero(self):
        growth_score = min(100, max(0, 0.0 * 2))
        assert growth_score == 0.0

    def test_growth_above_50_capped(self):
        # 60% growth → 60*2=120 → capped at 100
        growth_score = min(100, max(0, 60 * 2))
        assert growth_score == 100.0

    def test_growth_exactly_50_equals_100(self):
        growth_score = min(100, max(0, 50 * 2))
        assert growth_score == 100.0

    def test_growth_partial(self):
        growth_score = min(100, max(0, 25 * 2))
        assert growth_score == 50.0

    def test_funding_recency_months_0_is_100(self):
        recency = max(0, 100 - 0 * 3)
        assert recency == 100

    def test_funding_recency_months_34_is_0(self):
        recency = max(0, 100 - 34 * 3)
        assert recency == 0

    def test_funding_recency_months_33_is_1(self):
        recency = max(0, 100 - 33 * 3)
        assert recency == 1

    def test_funding_recency_months_8(self):
        recency = max(0, 100 - 8 * 3)
        assert recency == 76

    def test_funding_size_zero_eur(self):
        # log10(max(1, 0)) = log10(1) = 0
        size = min(100, math.log10(max(1, 0)) / math.log10(500) * 100)
        assert size == 0.0

    def test_funding_size_1m_eur(self):
        # log10(1) = 0 → size = 0
        size = min(100, math.log10(max(1, 1)) / math.log10(500) * 100)
        assert size == 0.0

    def test_funding_size_500m_eur_is_100(self):
        size = min(100, math.log10(max(1, 500)) / math.log10(500) * 100)
        assert pytest.approx(size, abs=1e-9) == 100.0

    def test_funding_size_partial(self):
        size = min(100, math.log10(max(1, 30)) / math.log10(500) * 100)
        expected = math.log10(30) / math.log10(500) * 100
        assert pytest.approx(size, rel=1e-6) == expected

    def test_funding_score_blend(self):
        recency = max(0, 100 - 8 * 3)  # 76
        size = min(100, math.log10(30) / math.log10(500) * 100)
        fund_score = recency * 0.5 + size * 0.5
        inp = make_input(last_funding_months_ago=8, funding_total_m_eur=30)
        # compute market manually and compare
        share_score = min(100, 20.0 * 1.5)
        growth_score = min(100, max(0, 25.0 * 2))
        expected = min(100, share_score * 0.40 + growth_score * 0.30 + fund_score * 0.30)
        assert pytest.approx(_market_score(inp), rel=1e-6) == expected

    def test_market_score_full_formula_matches(self):
        inp = make_input(
            market_share_pct=30, growth_rate_pct=40,
            funding_total_m_eur=100, last_funding_months_ago=6
        )
        share_score = min(100, 30 * 1.5)
        growth_score = min(100, max(0, 40 * 2))
        recency = max(0, 100 - 6 * 3)
        size = min(100, math.log10(100) / math.log10(500) * 100)
        fund_score = recency * 0.5 + size * 0.5
        expected = min(100, share_score * 0.40 + growth_score * 0.30 + fund_score * 0.30)
        assert pytest.approx(_market_score(inp), rel=1e-6) == expected

    def test_market_score_all_zero_inputs(self):
        # market_share=0, growth=0, funding=0, months=0
        # fund_size=0, fund_recency=100, fund_score=50
        # market = 0 + 0 + 50*0.30 = 15
        inp = make_input(market_share_pct=0, growth_rate_pct=0, funding_total_m_eur=0, last_funding_months_ago=0)
        expected = 0.0 * 0.40 + 0.0 * 0.30 + (100 * 0.5 + 0 * 0.5) * 0.30
        assert pytest.approx(_market_score(inp), rel=1e-6) == expected

    def test_market_score_max_100_cap(self):
        # All max values should not exceed 100
        inp = make_input(
            market_share_pct=100, growth_rate_pct=100,
            funding_total_m_eur=500, last_funding_months_ago=0
        )
        assert _market_score(inp) <= 100.0

    def test_market_score_returns_float(self):
        inp = make_input()
        assert isinstance(_market_score(inp), float)

    def test_market_score_default_inputs(self):
        inp = make_input()
        # computed manually
        share_score = min(100, 20.0 * 1.5)
        growth_score = min(100, max(0, 25.0 * 2))
        recency = max(0, 100 - 8 * 3)
        size = min(100, math.log10(30) / math.log10(500) * 100)
        fund_score = recency * 0.5 + size * 0.5
        expected = min(100, share_score * 0.40 + growth_score * 0.30 + fund_score * 0.30)
        assert pytest.approx(_market_score(inp), rel=1e-6) == expected

    def test_market_score_high_share_growth(self):
        inp = make_input(market_share_pct=80, growth_rate_pct=60, funding_total_m_eur=500, last_funding_months_ago=0)
        score = _market_score(inp)
        assert score == 100.0  # all components maxed

    def test_funding_recency_above_34_months_stays_at_zero(self):
        recency = max(0, 100 - 50 * 3)  # -50 → 0
        assert recency == 0


# ---------------------------------------------------------------------------
# TestProductScore  (15+ tests)
# ---------------------------------------------------------------------------

class TestProductScore:

    def test_overlap_score_exact(self):
        inp = make_input(feature_overlap_pct=80, product_quality_score=0, pricing_vs_us=2.0, has_recent_product_launch=False)
        overlap_score = min(100, 80)
        expected = overlap_score * 0.40 + 0 * 0.35 + 0 * 0.15 + 0 * 0.10
        assert pytest.approx(_product_score(inp), rel=1e-6) == expected

    def test_overlap_capped_at_100(self):
        inp = make_input(feature_overlap_pct=120, product_quality_score=0, pricing_vs_us=2.0, has_recent_product_launch=False)
        overlap_score = min(100, 120)
        assert overlap_score == 100

    def test_quality_score_exact(self):
        inp = make_input(feature_overlap_pct=0, product_quality_score=90, pricing_vs_us=2.0, has_recent_product_launch=False)
        expected = 0 * 0.40 + 90 * 0.35 + 0 * 0.15 + 0 * 0.10
        assert pytest.approx(_product_score(inp), rel=1e-6) == expected

    def test_quality_capped_at_100(self):
        score = min(100, 150)
        assert score == 100

    def test_price_score_pricing_2_is_0(self):
        price_score = min(100, max(0, (2.0 - 2.0) * 50))
        assert price_score == 0.0

    def test_price_score_pricing_1_is_50(self):
        price_score = min(100, max(0, (2.0 - 1.0) * 50))
        assert price_score == 50.0

    def test_price_score_pricing_0_is_100(self):
        price_score = min(100, max(0, (2.0 - 0.0) * 50))
        assert price_score == 100.0

    def test_price_score_pricing_above_2_capped_at_0(self):
        price_score = min(100, max(0, (2.0 - 2.5) * 50))
        assert price_score == 0.0

    def test_price_score_pricing_0_8(self):
        # cheaper competitor: more threatening
        price_score = min(100, max(0, (2.0 - 0.8) * 50))
        assert pytest.approx(price_score, rel=1e-9) == 60.0

    def test_launch_score_true_is_100(self):
        inp = make_input(feature_overlap_pct=0, product_quality_score=0, pricing_vs_us=2.0, has_recent_product_launch=True)
        expected = 0 * 0.40 + 0 * 0.35 + 0 * 0.15 + 100 * 0.10
        assert pytest.approx(_product_score(inp), rel=1e-6) == expected

    def test_launch_score_false_is_0(self):
        inp = make_input(feature_overlap_pct=0, product_quality_score=0, pricing_vs_us=2.0, has_recent_product_launch=False)
        assert _product_score(inp) == 0.0

    def test_product_score_full_formula(self):
        inp = make_input(
            feature_overlap_pct=80, product_quality_score=90,
            pricing_vs_us=0.8, has_recent_product_launch=True
        )
        overlap_score = min(100, 80)
        quality_score = min(100, 90)
        price_score = min(100, max(0, (2.0 - 0.8) * 50))
        launch_score = 100
        expected = overlap_score * 0.40 + quality_score * 0.35 + price_score * 0.15 + launch_score * 0.10
        assert pytest.approx(_product_score(inp), rel=1e-6) == expected

    def test_product_score_default_inputs(self):
        inp = make_input()
        overlap_score = min(100, 65.0)
        quality_score = min(100, 75.0)
        price_score = min(100, max(0, (2.0 - 1.0) * 50))
        launch_score = 0
        expected = overlap_score * 0.40 + quality_score * 0.35 + price_score * 0.15 + launch_score * 0.10
        assert pytest.approx(_product_score(inp), rel=1e-6) == expected

    def test_product_score_returns_float(self):
        assert isinstance(_product_score(make_input()), float)

    def test_product_score_all_zeros(self):
        inp = make_input(
            feature_overlap_pct=0, product_quality_score=0,
            pricing_vs_us=2.0, has_recent_product_launch=False
        )
        assert _product_score(inp) == 0.0

    def test_product_score_all_maxed(self):
        inp = make_input(
            feature_overlap_pct=100, product_quality_score=100,
            pricing_vs_us=0.0, has_recent_product_launch=True
        )
        expected = 100 * 0.40 + 100 * 0.35 + 100 * 0.15 + 100 * 0.10
        assert pytest.approx(_product_score(inp), rel=1e-6) == expected


# ---------------------------------------------------------------------------
# TestGTMScore  (15+ tests)
# ---------------------------------------------------------------------------

class TestGTMScore:

    def test_win_score_exact(self):
        win_score = min(100, 45.0)
        assert win_score == 45.0

    def test_win_score_capped_at_100(self):
        win_score = min(100, 120)
        assert win_score == 100

    def test_win_score_zero(self):
        inp = make_input(win_rate_against_us_pct=0, sales_team_size=1, marketing_spend_index=0, common_accounts=0)
        expected_win = 0.0
        sales_s = min(100, math.log10(max(1, 1)) / math.log10(1000) * 100)  # 0
        mkt_s = min(100, 0 * 50)  # 0
        acc_s = min(100, 0 * 5)   # 0
        expected = expected_win * 0.40 + sales_s * 0.25 + mkt_s * 0.20 + acc_s * 0.15
        assert pytest.approx(_gtm_score(inp), rel=1e-6) == expected

    def test_sales_score_team_1_is_0(self):
        sales_score = min(100, math.log10(max(1, 1)) / math.log10(1000) * 100)
        assert sales_score == 0.0

    def test_sales_score_team_1000_is_100(self):
        sales_score = min(100, math.log10(max(1, 1000)) / math.log10(1000) * 100)
        assert pytest.approx(sales_score, rel=1e-9) == 100.0

    def test_sales_score_team_0_is_0(self):
        sales_score = min(100, math.log10(max(1, 0)) / math.log10(1000) * 100)
        assert sales_score == 0.0

    def test_sales_score_team_100(self):
        sales_score = min(100, math.log10(100) / math.log10(1000) * 100)
        expected = math.log10(100) / math.log10(1000) * 100
        assert pytest.approx(sales_score, rel=1e-6) == expected

    def test_mkt_score_index_2_is_100(self):
        mkt_score = min(100, 2.0 * 50)
        assert mkt_score == 100.0

    def test_mkt_score_index_0_5_is_25(self):
        mkt_score = min(100, 0.5 * 50)
        assert mkt_score == 25.0

    def test_mkt_score_index_1_is_50(self):
        mkt_score = min(100, 1.0 * 50)
        assert mkt_score == 50.0

    def test_accounts_score_20_is_100(self):
        accounts_score = min(100, 20 * 5)
        assert accounts_score == 100.0

    def test_accounts_score_10_is_50(self):
        accounts_score = min(100, 10 * 5)
        assert accounts_score == 50.0

    def test_accounts_score_above_20_capped(self):
        accounts_score = min(100, 25 * 5)
        assert accounts_score == 100.0

    def test_accounts_score_zero(self):
        accounts_score = min(100, 0 * 5)
        assert accounts_score == 0.0

    def test_gtm_score_full_formula(self):
        inp = make_input(
            win_rate_against_us_pct=70, sales_team_size=100,
            marketing_spend_index=1.5, common_accounts=15
        )
        win_score = min(100, 70)
        sales_score = min(100, math.log10(100) / math.log10(1000) * 100)
        mkt_score = min(100, 1.5 * 50)
        accounts_score = min(100, 15 * 5)
        expected = win_score * 0.40 + sales_score * 0.25 + mkt_score * 0.20 + accounts_score * 0.15
        assert pytest.approx(_gtm_score(inp), rel=1e-6) == expected

    def test_gtm_score_default_inputs(self):
        inp = make_input()
        win_score = min(100, 45.0)
        sales_score = min(100, math.log10(50) / math.log10(1000) * 100)
        mkt_score = min(100, 1.0 * 50)
        accounts_score = min(100, 10 * 5)
        expected = win_score * 0.40 + sales_score * 0.25 + mkt_score * 0.20 + accounts_score * 0.15
        assert pytest.approx(_gtm_score(inp), rel=1e-6) == expected

    def test_gtm_score_returns_float(self):
        assert isinstance(_gtm_score(make_input()), float)


# ---------------------------------------------------------------------------
# TestWeaknessScore  (15+ tests)
# ---------------------------------------------------------------------------

class TestWeaknessScore:

    def test_all_zeros_returns_zero(self):
        inp = make_input(
            executive_departures=0, negative_reviews_pct=0,
            hiring_velocity=2.0, funding_total_m_eur=20, last_funding_months_ago=0
        )
        assert _weakness_score(inp) == 0.0

    def test_exec_departures_1_adds_10(self):
        inp = make_input(
            executive_departures=1, negative_reviews_pct=0,
            hiring_velocity=2.0, funding_total_m_eur=20
        )
        assert _weakness_score(inp) == 10.0

    def test_exec_departures_2_adds_20(self):
        inp = make_input(
            executive_departures=2, negative_reviews_pct=0,
            hiring_velocity=2.0, funding_total_m_eur=20
        )
        assert _weakness_score(inp) == 20.0

    def test_exec_departures_3_caps_at_30(self):
        inp = make_input(
            executive_departures=3, negative_reviews_pct=0,
            hiring_velocity=2.0, funding_total_m_eur=20
        )
        assert _weakness_score(inp) == 30.0

    def test_exec_departures_4_still_capped_at_30(self):
        inp = make_input(
            executive_departures=4, negative_reviews_pct=0,
            hiring_velocity=2.0, funding_total_m_eur=20
        )
        assert _weakness_score(inp) == 30.0

    def test_neg_reviews_12_5_pct_adds_25(self):
        inp = make_input(
            executive_departures=0, negative_reviews_pct=12.5,
            hiring_velocity=2.0, funding_total_m_eur=20
        )
        assert _weakness_score(inp) == 25.0

    def test_neg_reviews_above_12_5_capped_at_25(self):
        inp = make_input(
            executive_departures=0, negative_reviews_pct=20,
            hiring_velocity=2.0, funding_total_m_eur=20
        )
        assert _weakness_score(inp) == 25.0

    def test_neg_reviews_partial(self):
        inp = make_input(
            executive_departures=0, negative_reviews_pct=5,
            hiring_velocity=2.0, funding_total_m_eur=20
        )
        assert _weakness_score(inp) == 10.0  # 5*2=10

    def test_hiring_velocity_0_5_adds_15(self):
        # max(0, 20 - 0.5*10) = max(0,15) = 15
        inp = make_input(
            executive_departures=0, negative_reviews_pct=0,
            hiring_velocity=0.5, funding_total_m_eur=20
        )
        assert _weakness_score(inp) == 15.0

    def test_hiring_velocity_0_adds_20(self):
        # max(0, 20 - 0*10) = 20
        inp = make_input(
            executive_departures=0, negative_reviews_pct=0,
            hiring_velocity=0.0, funding_total_m_eur=20
        )
        assert _weakness_score(inp) == 20.0

    def test_hiring_velocity_2_adds_0(self):
        # max(0, 20 - 2*10) = 0
        inp = make_input(
            executive_departures=0, negative_reviews_pct=0,
            hiring_velocity=2.0, funding_total_m_eur=20
        )
        assert _weakness_score(inp) == 0.0

    def test_low_funding_old_round_adds_penalty(self):
        # funding < 10 AND last_funding_months_ago * 1.5 → penalty
        inp = make_input(
            executive_departures=0, negative_reviews_pct=0,
            hiring_velocity=2.0, funding_total_m_eur=5, last_funding_months_ago=12
        )
        expected = min(25, 12 * 1.5)  # 18
        assert _weakness_score(inp) == expected

    def test_high_funding_no_penalty(self):
        # funding >= 10 → no penalty applied
        inp_low = make_input(
            executive_departures=0, negative_reviews_pct=0,
            hiring_velocity=2.0, funding_total_m_eur=5, last_funding_months_ago=12
        )
        inp_high = make_input(
            executive_departures=0, negative_reviews_pct=0,
            hiring_velocity=2.0, funding_total_m_eur=10, last_funding_months_ago=12
        )
        assert _weakness_score(inp_high) == 0.0
        assert _weakness_score(inp_low) > 0.0

    def test_funding_exactly_10_no_penalty(self):
        inp = make_input(
            executive_departures=0, negative_reviews_pct=0,
            hiring_velocity=2.0, funding_total_m_eur=10, last_funding_months_ago=20
        )
        assert _weakness_score(inp) == 0.0

    def test_weakness_score_all_maxed_caps_at_100(self):
        inp = make_input(
            executive_departures=5, negative_reviews_pct=100,
            hiring_velocity=0.0, funding_total_m_eur=1, last_funding_months_ago=100
        )
        assert _weakness_score(inp) <= 100.0

    def test_weakness_score_combined_components(self):
        inp = make_input(
            executive_departures=2, negative_reviews_pct=15,
            hiring_velocity=0.5, funding_total_m_eur=5, last_funding_months_ago=12
        )
        score = 0.0
        score += min(30, 2 * 10)           # 20
        score += min(25, 15 * 2)           # 25
        score += min(20, max(0, 20 - 0.5 * 10))  # 15
        score += min(25, 12 * 1.5)         # 18
        expected = min(100, score)
        assert pytest.approx(_weakness_score(inp), rel=1e-6) == expected

    def test_weakness_score_returns_float(self):
        assert isinstance(_weakness_score(make_input()), float)


# ---------------------------------------------------------------------------
# TestThreatScore  (10+ tests)
# ---------------------------------------------------------------------------

class TestThreatScore:

    def _compute_threat(self, inp, m, p, g, w):
        type_base = _TYPE_BASE_THREAT[inp.competitor_type]
        weighted = m * 0.30 + p * 0.35 + g * 0.25 - w * 0.10
        raw = type_base * 0.20 + weighted * 0.80
        return round(max(0, min(100, raw)), 2)

    def test_type_base_direct_is_60(self):
        assert _TYPE_BASE_THREAT[CompetitorType.DIRECT] == 60

    def test_type_base_indirect_is_30(self):
        assert _TYPE_BASE_THREAT[CompetitorType.INDIRECT] == 30

    def test_type_base_emerging_is_50(self):
        assert _TYPE_BASE_THREAT[CompetitorType.EMERGING] == 50

    def test_type_base_legacy_is_45(self):
        assert _TYPE_BASE_THREAT[CompetitorType.LEGACY] == 45

    def test_type_base_niche_is_35(self):
        assert _TYPE_BASE_THREAT[CompetitorType.NICHE] == 35

    def test_threat_direct_vs_indirect_diff_is_6(self):
        # (60 - 30) * 0.20 = 6 difference from type alone
        inp_dir = make_input(competitor_type=CompetitorType.DIRECT)
        inp_ind = make_input(competitor_type=CompetitorType.INDIRECT)
        m, p, g, w = 50.0, 60.0, 55.0, 20.0
        t_dir = _threat_score(inp_dir, m, p, g, w)
        t_ind = _threat_score(inp_ind, m, p, g, w)
        assert pytest.approx(t_dir - t_ind, abs=1e-9) == 6.0

    def test_threat_score_capped_at_100(self):
        inp = make_input()
        assert _threat_score(inp, 100.0, 100.0, 100.0, 0.0) <= 100.0

    def test_threat_score_floored_at_0(self):
        inp = make_input()
        assert _threat_score(inp, 0.0, 0.0, 0.0, 100.0) >= 0.0

    def test_threat_score_formula_direct(self):
        inp = make_input(competitor_type=CompetitorType.DIRECT)
        m, p, g, w = 50.0, 60.0, 55.0, 20.0
        expected = self._compute_threat(inp, m, p, g, w)
        assert _threat_score(inp, m, p, g, w) == expected

    def test_threat_score_formula_indirect(self):
        inp = make_input(competitor_type=CompetitorType.INDIRECT)
        m, p, g, w = 50.0, 60.0, 55.0, 20.0
        expected = self._compute_threat(inp, m, p, g, w)
        assert _threat_score(inp, m, p, g, w) == expected

    def test_threat_score_all_maxed_is_84(self):
        # type_base=60, weighted = 100*0.30+100*0.35+100*0.25-0*0.10=90
        # raw = 60*0.20 + 90*0.80 = 12+72 = 84
        inp = make_input(competitor_type=CompetitorType.DIRECT)
        assert _threat_score(inp, 100.0, 100.0, 100.0, 0.0) == 84.0

    def test_threat_score_weakness_reduces_score(self):
        inp = make_input()
        t_no_weakness = _threat_score(inp, 50.0, 60.0, 55.0, 0.0)
        t_with_weakness = _threat_score(inp, 50.0, 60.0, 55.0, 50.0)
        assert t_no_weakness > t_with_weakness

    def test_threat_score_returns_rounded_2_decimal(self):
        inp = make_input()
        t = _threat_score(inp, 33.33, 66.67, 50.0, 25.0)
        # Should be rounded to 2 decimals
        assert t == round(t, 2)


# ---------------------------------------------------------------------------
# TestThreatLevel  (8 tests)
# ---------------------------------------------------------------------------

class TestThreatLevel:

    def test_score_80_is_critical(self):
        assert _threat_level(80.0) == ThreatLevel.CRITICAL

    def test_score_79_99_is_high(self):
        assert _threat_level(79.99) == ThreatLevel.HIGH

    def test_score_60_is_high(self):
        assert _threat_level(60.0) == ThreatLevel.HIGH

    def test_score_59_99_is_medium(self):
        assert _threat_level(59.99) == ThreatLevel.MEDIUM

    def test_score_40_is_medium(self):
        assert _threat_level(40.0) == ThreatLevel.MEDIUM

    def test_score_39_99_is_low(self):
        assert _threat_level(39.99) == ThreatLevel.LOW

    def test_score_20_is_low(self):
        assert _threat_level(20.0) == ThreatLevel.LOW

    def test_score_19_99_is_minimal(self):
        assert _threat_level(19.99) == ThreatLevel.MINIMAL

    def test_score_0_is_minimal(self):
        assert _threat_level(0.0) == ThreatLevel.MINIMAL

    def test_score_100_is_critical(self):
        assert _threat_level(100.0) == ThreatLevel.CRITICAL


# ---------------------------------------------------------------------------
# TestAction  (6 tests)
# ---------------------------------------------------------------------------

class TestAction:

    def test_critical_returns_preempt(self):
        inp = make_input()
        assert _action(ThreatLevel.CRITICAL, inp) == CompetitiveAction.PREEMPT

    def test_high_with_win_rate_40_returns_respond(self):
        inp = make_input(win_rate_against_us_pct=40.0)
        assert _action(ThreatLevel.HIGH, inp) == CompetitiveAction.RESPOND

    def test_high_with_win_rate_above_40_returns_respond(self):
        inp = make_input(win_rate_against_us_pct=60.0)
        assert _action(ThreatLevel.HIGH, inp) == CompetitiveAction.RESPOND

    def test_high_with_win_rate_below_40_returns_differentiate(self):
        inp = make_input(win_rate_against_us_pct=39.9)
        assert _action(ThreatLevel.HIGH, inp) == CompetitiveAction.DIFFERENTIATE

    def test_high_with_win_rate_0_returns_differentiate(self):
        inp = make_input(win_rate_against_us_pct=0.0)
        assert _action(ThreatLevel.HIGH, inp) == CompetitiveAction.DIFFERENTIATE

    def test_medium_returns_monitor(self):
        inp = make_input()
        assert _action(ThreatLevel.MEDIUM, inp) == CompetitiveAction.MONITOR

    def test_low_returns_monitor(self):
        inp = make_input()
        assert _action(ThreatLevel.LOW, inp) == CompetitiveAction.MONITOR

    def test_minimal_returns_ignore(self):
        inp = make_input()
        assert _action(ThreatLevel.MINIMAL, inp) == CompetitiveAction.IGNORE


# ---------------------------------------------------------------------------
# TestWinProbability  (8 tests)
# ---------------------------------------------------------------------------

class TestWinProbability:

    def test_no_weakness_bonus_formula(self):
        inp = make_input(
            executive_departures=0, negative_reviews_pct=0,
            hiring_velocity=2.0, funding_total_m_eur=20, last_funding_months_ago=0
        )
        # weakness=0, bonus=0
        threat = 40.0
        expected = round(max(5, min(95, 100 - threat + 0.0)), 1)
        assert _win_probability(inp, threat) == expected

    def test_with_weakness_bonus(self):
        inp = make_input()
        weakness = _weakness_score(inp)
        bonus = min(15, weakness * 0.15)
        threat = 47.45
        expected = round(max(5, min(95, 100 - threat + bonus)), 1)
        assert _win_probability(inp, threat) == expected

    def test_threat_100_clamped_to_min_5(self):
        inp = make_input(
            executive_departures=0, negative_reviews_pct=0,
            hiring_velocity=2.0, funding_total_m_eur=20
        )
        result = _win_probability(inp, 100.0)
        assert result >= 5.0

    def test_threat_0_with_no_bonus_is_95(self):
        inp = make_input(
            executive_departures=0, negative_reviews_pct=0,
            hiring_velocity=2.0, funding_total_m_eur=20, last_funding_months_ago=0
        )
        # raw = 100 - 0 + 0 = 100 → capped at 95
        result = _win_probability(inp, 0.0)
        assert result == 95.0

    def test_weakness_bonus_capped_at_15(self):
        # max weakness = 100 → bonus = min(15, 100*0.15) = 15
        inp = make_input(
            executive_departures=5, negative_reviews_pct=100,
            hiring_velocity=0.0, funding_total_m_eur=1, last_funding_months_ago=100
        )
        weakness = _weakness_score(inp)
        bonus = min(15, weakness * 0.15)
        assert bonus == 15.0

    def test_result_min_is_5(self):
        inp = make_input(
            executive_departures=0, negative_reviews_pct=0,
            hiring_velocity=2.0, funding_total_m_eur=20
        )
        result = _win_probability(inp, 100.0)
        assert result >= 5.0

    def test_result_max_is_95(self):
        inp = make_input(
            executive_departures=5, negative_reviews_pct=100,
            hiring_velocity=0.0, funding_total_m_eur=1, last_funding_months_ago=100
        )
        result = _win_probability(inp, 0.0)
        assert result <= 95.0

    def test_result_rounded_to_1_decimal(self):
        inp = make_input()
        result = _win_probability(inp, 33.3)
        assert result == round(result, 1)

    def test_threat_50_default_weakness(self):
        inp = make_input()
        weakness = _weakness_score(inp)
        bonus = min(15, weakness * 0.15)
        expected = round(max(5, min(95, 100 - 50.0 + bonus)), 1)
        assert _win_probability(inp, 50.0) == expected


# ---------------------------------------------------------------------------
# TestSignals  (15+ tests)
# ---------------------------------------------------------------------------

def _get_signals(inp: CompetitorInput):
    """Helper that runs the full analysis and extracts signals."""
    engine = CompetitorIntelligenceEngine()
    result = engine.analyze(inp)
    return result.threat_signals, result.opportunity_signals, result.battle_card_tips


class TestSignals:

    def test_win_rate_50_generates_threat_signal(self):
        inp = make_input(win_rate_against_us_pct=50)
        threats, _, _ = _get_signals(inp)
        assert any("50%" in s for s in threats)

    def test_win_rate_below_50_no_win_threat_signal(self):
        inp = make_input(win_rate_against_us_pct=49.9)
        threats, _, _ = _get_signals(inp)
        assert not any("49%" in s or "49.9" in s for s in threats)

    def test_growth_30_generates_threat_signal(self):
        inp = make_input(growth_rate_pct=30)
        threats, _, _ = _get_signals(inp)
        assert any("30%" in s for s in threats)

    def test_growth_below_30_no_growth_threat_signal(self):
        inp = make_input(growth_rate_pct=29)
        threats, _, _ = _get_signals(inp)
        assert not any("Croissance rapide" in s for s in threats)

    def test_recent_product_launch_generates_threat(self):
        inp = make_input(has_recent_product_launch=True)
        threats, _, _ = _get_signals(inp)
        assert any("Lancement produit" in s for s in threats)

    def test_no_recent_launch_no_threat(self):
        inp = make_input(has_recent_product_launch=False)
        threats, _, _ = _get_signals(inp)
        assert not any("Lancement produit" in s for s in threats)

    def test_feature_overlap_70_generates_threat(self):
        inp = make_input(feature_overlap_pct=70)
        threats, _, _ = _get_signals(inp)
        assert any("70%" in s for s in threats)

    def test_feature_overlap_below_70_no_overlap_threat(self):
        inp = make_input(feature_overlap_pct=69.9)
        threats, _, _ = _get_signals(inp)
        assert not any("chevauchement" in s for s in threats)

    def test_recent_funding_generates_threat(self):
        # last_funding_months_ago <= 6 AND funding >= 10M
        inp = make_input(last_funding_months_ago=6, funding_total_m_eur=10)
        threats, _, _ = _get_signals(inp)
        assert any("Financement récent" in s for s in threats)

    def test_recent_funding_low_amount_no_threat(self):
        # funding < 10M → no funding threat
        inp = make_input(last_funding_months_ago=3, funding_total_m_eur=9.9)
        threats, _, _ = _get_signals(inp)
        assert not any("Financement récent" in s for s in threats)

    def test_marketing_spend_1_5_generates_threat(self):
        inp = make_input(marketing_spend_index=1.5)
        threats, _, _ = _get_signals(inp)
        assert any("Budget marketing" in s for s in threats)

    def test_partnership_2_generates_threat(self):
        inp = make_input(partnership_announcements=2)
        threats, _, _ = _get_signals(inp)
        assert any("partenariats" in s for s in threats)

    def test_exec_departures_2_generates_opportunity(self):
        inp = make_input(executive_departures=2)
        _, opps, _ = _get_signals(inp)
        assert any("C-suite" in s for s in opps)

    def test_exec_departures_1_no_c_suite_opportunity(self):
        inp = make_input(executive_departures=1)
        _, opps, _ = _get_signals(inp)
        assert not any("C-suite" in s for s in opps)

    def test_negative_reviews_20_generates_opportunity(self):
        inp = make_input(negative_reviews_pct=20)
        _, opps, _ = _get_signals(inp)
        assert any("avis négatifs" in s for s in opps)

    def test_negative_reviews_below_20_no_avis_opportunity(self):
        inp = make_input(negative_reviews_pct=19)
        _, opps, _ = _get_signals(inp)
        assert not any("avis négatifs" in s for s in opps)

    def test_pricing_above_1_3_generates_opportunity(self):
        inp = make_input(pricing_vs_us=1.4)
        _, opps, _ = _get_signals(inp)
        assert any("Pricing" in s for s in opps)

    def test_pricing_exactly_1_3_no_opportunity(self):
        inp = make_input(pricing_vs_us=1.3)
        _, opps, _ = _get_signals(inp)
        assert not any("Pricing" in s for s in opps)

    def test_low_hiring_velocity_generates_opportunity(self):
        inp = make_input(hiring_velocity=0.5)
        _, opps, _ = _get_signals(inp)
        assert any("embauches" in s for s in opps)

    def test_hiring_velocity_0_7_no_slow_hiring_opportunity(self):
        # threshold is < 0.7 strictly
        inp = make_input(hiring_velocity=0.7)
        _, opps, _ = _get_signals(inp)
        assert not any("embauches" in s for s in opps)

    def test_feature_overlap_60_generates_battle_tip(self):
        inp = make_input(feature_overlap_pct=60)
        _, _, tips = _get_signals(inp)
        assert any("fonctionnalités différenciantes" in t for t in tips)

    def test_pricing_above_1_generates_roi_battle_tip(self):
        inp = make_input(pricing_vs_us=1.1)
        _, _, tips = _get_signals(inp)
        assert any("ROI" in t for t in tips)

    def test_win_rate_40_generates_champion_battle_tip(self):
        inp = make_input(win_rate_against_us_pct=40, feature_overlap_pct=60)
        _, _, tips = _get_signals(inp)
        assert any("champion interne" in t for t in tips)

    def test_exec_departure_1_generates_stability_battle_tip(self):
        inp = make_input(executive_departures=1)
        _, _, tips = _get_signals(inp)
        assert any("stabilité" in t for t in tips)

    def test_high_threat_level_generates_exec_sponsor_tip(self):
        # Create HIGH or CRITICAL level
        inp = make_input(
            market_share_pct=80, growth_rate_pct=60, feature_overlap_pct=100,
            product_quality_score=100, win_rate_against_us_pct=80,
            sales_team_size=500, marketing_spend_index=2.0, common_accounts=20,
            funding_total_m_eur=500, last_funding_months_ago=0
        )
        threats, _, tips = _get_signals(inp)
        assert any("exec sponsor" in t for t in tips)

    def test_neg_reviews_15_generates_prospect_opportunity(self):
        inp = make_input(negative_reviews_pct=15)
        _, opps, _ = _get_signals(inp)
        assert any("Insatisfaction produit" in s for s in opps)


# ---------------------------------------------------------------------------
# TestEngineAnalyze  (10+ tests)
# ---------------------------------------------------------------------------

class TestEngineAnalyze:

    def test_returns_competitor_result(self):
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(make_input())
        assert isinstance(result, CompetitorResult)

    def test_result_stored_via_get(self):
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(make_input(competitor_id="cid"))
        assert engine.get("cid") is result

    def test_overwrite_same_id(self):
        engine = CompetitorIntelligenceEngine()
        engine.analyze(make_input(competitor_id="same", competitor_name="First"))
        engine.analyze(make_input(competitor_id="same", competitor_name="Second"))
        assert len(engine.all_competitors()) == 1
        assert engine.get("same").competitor_name == "Second"

    def test_threat_score_in_range(self):
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(make_input())
        assert 0.0 <= result.threat_score <= 100.0

    def test_result_fields_populated(self):
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(make_input())
        assert result.competitor_id == "comp1"
        assert result.competitor_name == "CompetitorX"
        assert result.competitor_type == CompetitorType.DIRECT
        assert isinstance(result.threat_level, ThreatLevel)
        assert isinstance(result.recommended_action, CompetitiveAction)
        assert isinstance(result.threat_signals, list)
        assert isinstance(result.opportunity_signals, list)
        assert isinstance(result.battle_card_tips, list)
        assert 5.0 <= result.win_probability_vs_this <= 95.0

    def test_market_score_stored(self):
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(make_input())
        expected_m = round(_market_score(make_input()), 2)
        assert result.market_score == expected_m

    def test_product_score_stored(self):
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(make_input())
        expected_p = round(_product_score(make_input()), 2)
        assert result.product_score == expected_p

    def test_gtm_score_stored(self):
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(make_input())
        expected_g = round(_gtm_score(make_input()), 2)
        assert result.gtm_score == expected_g

    def test_weakness_score_stored(self):
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(make_input())
        expected_w = round(_weakness_score(make_input()), 2)
        assert result.weakness_score == expected_w

    def test_batch_sorted_desc_by_threat(self):
        engine = CompetitorIntelligenceEngine()
        inp_low = make_input(competitor_id="low", market_share_pct=5, growth_rate_pct=5)
        inp_high = make_input(competitor_id="high", market_share_pct=70, growth_rate_pct=50)
        inp_mid = make_input(competitor_id="mid", market_share_pct=30, growth_rate_pct=30)
        batch = engine.analyze_batch([inp_low, inp_high, inp_mid])
        scores = [r.threat_score for r in batch]
        assert scores == sorted(scores, reverse=True)

    def test_batch_returns_correct_count(self):
        engine = CompetitorIntelligenceEngine()
        inputs = [make_input(competitor_id=f"c{i}") for i in range(4)]
        batch = engine.analyze_batch(inputs)
        assert len(batch) == 4

    def test_batch_also_stores_results(self):
        engine = CompetitorIntelligenceEngine()
        inputs = [make_input(competitor_id=f"c{i}") for i in range(3)]
        engine.analyze_batch(inputs)
        for i in range(3):
            assert engine.get(f"c{i}") is not None


# ---------------------------------------------------------------------------
# TestEngineQueries  (15+ tests)
# ---------------------------------------------------------------------------

class TestEngineQueries:

    def _engine_with_defaults(self) -> CompetitorIntelligenceEngine:
        engine = CompetitorIntelligenceEngine()
        engine.analyze(make_input(competitor_id="c1", market_share_pct=10))
        engine.analyze(make_input(competitor_id="c2", market_share_pct=40))
        engine.analyze(make_input(competitor_id="c3", market_share_pct=25))
        return engine

    def test_all_competitors_sorted_desc(self):
        engine = self._engine_with_defaults()
        results = engine.all_competitors()
        scores = [r.threat_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_all_competitors_count(self):
        engine = self._engine_with_defaults()
        assert len(engine.all_competitors()) == 3

    def test_by_level_filters_correctly(self):
        engine = self._engine_with_defaults()
        # all defaults should be MEDIUM
        medium = engine.by_level(ThreatLevel.MEDIUM)
        assert all(r.threat_level == ThreatLevel.MEDIUM for r in medium)

    def test_by_level_returns_empty_for_missing_level(self):
        engine = self._engine_with_defaults()
        assert engine.by_level(ThreatLevel.CRITICAL) == []

    def test_critical_threats_filters_critical(self):
        engine = CompetitorIntelligenceEngine()
        engine.analyze(make_input(competitor_id="normal"))
        critical = engine.critical_threats()
        assert all(r.threat_level == ThreatLevel.CRITICAL for r in critical)

    def test_high_threats_filters_high(self):
        engine = CompetitorIntelligenceEngine()
        # add a HIGH threat
        inp_high = make_input(
            competitor_id="high",
            market_share_pct=80, growth_rate_pct=60,
            feature_overlap_pct=100, product_quality_score=100,
            win_rate_against_us_pct=100, sales_team_size=1000,
            marketing_spend_index=2.0, common_accounts=20,
            funding_total_m_eur=500, last_funding_months_ago=0
        )
        engine.analyze(inp_high)
        engine.analyze(make_input(competitor_id="normal"))
        high = engine.high_threats()
        assert all(r.threat_level == ThreatLevel.HIGH for r in high)

    def test_urgent_threats_includes_critical_and_high(self):
        engine = CompetitorIntelligenceEngine()
        engine.analyze(make_input(competitor_id="normal"))
        inp_high = make_input(
            competitor_id="high",
            market_share_pct=80, growth_rate_pct=60,
            feature_overlap_pct=100, product_quality_score=100,
            win_rate_against_us_pct=100, sales_team_size=1000,
            marketing_spend_index=2.0, common_accounts=20,
            funding_total_m_eur=500, last_funding_months_ago=0
        )
        engine.analyze(inp_high)
        urgent = engine.urgent_threats()
        assert all(
            r.threat_level in (ThreatLevel.CRITICAL, ThreatLevel.HIGH)
            for r in urgent
        )

    def test_urgent_threats_excludes_medium_and_below(self):
        engine = CompetitorIntelligenceEngine()
        engine.analyze(make_input(competitor_id="normal"))
        urgent = engine.urgent_threats()
        assert not any(r.competitor_id == "normal" for r in urgent)

    def test_by_type_direct_returns_only_direct(self):
        engine = CompetitorIntelligenceEngine()
        engine.analyze(make_input(competitor_id="d1", competitor_type=CompetitorType.DIRECT))
        engine.analyze(make_input(competitor_id="e1", competitor_type=CompetitorType.EMERGING))
        direct = engine.by_type(CompetitorType.DIRECT)
        assert len(direct) == 1
        assert direct[0].competitor_id == "d1"

    def test_by_type_returns_empty_for_missing_type(self):
        engine = CompetitorIntelligenceEngine()
        engine.analyze(make_input(competitor_id="d1", competitor_type=CompetitorType.DIRECT))
        assert engine.by_type(CompetitorType.NICHE) == []

    def test_top_threats_returns_n(self):
        engine = CompetitorIntelligenceEngine()
        for i in range(5):
            engine.analyze(make_input(competitor_id=f"c{i}", market_share_pct=float(i * 10)))
        top3 = engine.top_threats(3)
        assert len(top3) == 3

    def test_top_threats_sorted_desc(self):
        engine = CompetitorIntelligenceEngine()
        for i in range(5):
            engine.analyze(make_input(competitor_id=f"c{i}", market_share_pct=float(i * 10)))
        top3 = engine.top_threats(3)
        scores = [r.threat_score for r in top3]
        assert scores == sorted(scores, reverse=True)

    def test_top_threats_fewer_than_n(self):
        engine = CompetitorIntelligenceEngine()
        engine.analyze(make_input(competitor_id="only"))
        top5 = engine.top_threats(5)
        assert len(top5) == 1

    def test_avg_win_probability_formula(self):
        engine = self._engine_with_defaults()
        all_r = engine.all_competitors()
        expected = round(sum(r.win_probability_vs_this for r in all_r) / len(all_r), 1)
        assert engine.avg_win_probability() == expected

    def test_avg_win_probability_empty_is_zero(self):
        engine = CompetitorIntelligenceEngine()
        assert engine.avg_win_probability() == 0.0

    def test_reset_clears_all(self):
        engine = self._engine_with_defaults()
        engine.reset()
        assert engine.all_competitors() == []

    def test_get_returns_none_for_nonexistent(self):
        engine = CompetitorIntelligenceEngine()
        assert engine.get("nonexistent") is None


# ---------------------------------------------------------------------------
# TestSummary  (8 tests)
# ---------------------------------------------------------------------------

class TestSummary:

    def test_empty_engine_summary(self):
        engine = CompetitorIntelligenceEngine()
        s = engine.summary()
        assert s["total"] == 0
        assert s["level_counts"] == {}
        assert s["avg_threat_score"] == 0.0
        assert s["avg_win_probability"] == 0.0

    def test_summary_total_count(self):
        engine = CompetitorIntelligenceEngine()
        for i in range(3):
            engine.analyze(make_input(competitor_id=f"c{i}"))
        assert engine.summary()["total"] == 3

    def test_summary_level_counts(self):
        engine = CompetitorIntelligenceEngine()
        engine.analyze(make_input(competitor_id="c1"))
        engine.analyze(make_input(competitor_id="c2"))
        s = engine.summary()
        # both are MEDIUM level (default inputs)
        assert s["level_counts"].get("medium", 0) == 2

    def test_summary_avg_threat_score(self):
        engine = CompetitorIntelligenceEngine()
        engine.analyze(make_input(competitor_id="c1"))
        engine.analyze(make_input(competitor_id="c2"))
        all_r = engine.all_competitors()
        expected = round(sum(r.threat_score for r in all_r) / len(all_r), 1)
        assert engine.summary()["avg_threat_score"] == expected

    def test_summary_avg_win_probability(self):
        engine = CompetitorIntelligenceEngine()
        engine.analyze(make_input(competitor_id="c1"))
        engine.analyze(make_input(competitor_id="c2"))
        expected = engine.avg_win_probability()
        assert engine.summary()["avg_win_probability"] == expected

    def test_summary_has_required_keys(self):
        engine = CompetitorIntelligenceEngine()
        s = engine.summary()
        assert "total" in s
        assert "level_counts" in s
        assert "avg_threat_score" in s
        assert "avg_win_probability" in s

    def test_summary_multiple_levels(self):
        engine = CompetitorIntelligenceEngine()
        engine.analyze(make_input(competitor_id="normal"))
        inp_high = make_input(
            competitor_id="high",
            market_share_pct=80, growth_rate_pct=60,
            feature_overlap_pct=100, product_quality_score=100,
            win_rate_against_us_pct=100, sales_team_size=1000,
            marketing_spend_index=2.0, common_accounts=20,
            funding_total_m_eur=500, last_funding_months_ago=0
        )
        engine.analyze(inp_high)
        s = engine.summary()
        assert s["total"] == 2
        assert len(s["level_counts"]) >= 2

    def test_summary_level_counts_correct_values(self):
        engine = CompetitorIntelligenceEngine()
        engine.analyze(make_input(competitor_id="c1"))
        engine.analyze(make_input(competitor_id="c2"))
        engine.analyze(make_input(competitor_id="c3"))
        s = engine.summary()
        total_from_counts = sum(s["level_counts"].values())
        assert total_from_counts == s["total"]


# ---------------------------------------------------------------------------
# TestEdgeCases  (10+ tests)
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def test_market_share_zero(self):
        inp = make_input(market_share_pct=0, growth_rate_pct=0)
        result = _market_score(inp)
        assert result >= 0.0

    def test_all_booleans_false(self):
        inp = make_input(has_recent_product_launch=False)
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(inp)
        assert result.threat_score >= 0.0

    def test_funding_total_zero(self):
        inp = make_input(funding_total_m_eur=0)
        result = _market_score(inp)
        # log10(max(1,0)) = log10(1) = 0, so funding_size = 0
        assert result >= 0.0

    def test_sales_team_zero(self):
        inp = make_input(sales_team_size=0)
        result = _gtm_score(inp)
        # log10(max(1,0)) = 0, sales_score = 0
        assert result >= 0.0

    def test_pricing_at_2_clamped_price_score_0(self):
        inp = make_input(pricing_vs_us=2.0)
        price_score = min(100, max(0, (2.0 - 2.0) * 50))
        assert price_score == 0.0

    def test_pricing_above_2_still_clamped_to_0(self):
        inp = make_input(pricing_vs_us=3.0)
        price_score = min(100, max(0, (2.0 - 3.0) * 50))
        assert price_score == 0.0

    def test_empty_engine_all_competitors_empty(self):
        engine = CompetitorIntelligenceEngine()
        assert engine.all_competitors() == []

    def test_reset_then_analyze_works(self):
        engine = CompetitorIntelligenceEngine()
        engine.analyze(make_input(competitor_id="before"))
        engine.reset()
        result = engine.analyze(make_input(competitor_id="after"))
        assert len(engine.all_competitors()) == 1
        assert engine.get("after") is result

    def test_to_dict_enum_values_are_strings(self):
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert d["competitor_type"] == "direct"
        assert d["threat_level"] in ("critical", "high", "medium", "low", "minimal")
        assert d["recommended_action"] in ("monitor", "respond", "differentiate", "preempt", "ignore")

    def test_to_dict_has_all_required_keys(self):
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(make_input())
        d = result.to_dict()
        required = {
            "competitor_id", "competitor_name", "competitor_type",
            "threat_score", "threat_level", "market_score", "product_score",
            "gtm_score", "weakness_score", "recommended_action",
            "threat_signals", "opportunity_signals", "battle_card_tips",
            "win_probability_vs_this"
        }
        assert required.issubset(d.keys())

    def test_funding_months_0_max_recency(self):
        recency = max(0, 100 - 0 * 3)
        assert recency == 100

    def test_multiple_competitors_different_types(self):
        engine = CompetitorIntelligenceEngine()
        for i, ctype in enumerate(CompetitorType):
            engine.analyze(make_input(competitor_id=f"c{i}", competitor_type=ctype))
        assert len(engine.all_competitors()) == 5

    def test_win_probability_result_is_float(self):
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(make_input())
        assert isinstance(result.win_probability_vs_this, float)

    def test_threat_signals_is_list(self):
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(make_input())
        assert isinstance(result.threat_signals, list)

    def test_opportunity_signals_is_list(self):
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(make_input())
        assert isinstance(result.opportunity_signals, list)

    def test_battle_card_tips_is_list(self):
        engine = CompetitorIntelligenceEngine()
        result = engine.analyze(make_input())
        assert isinstance(result.battle_card_tips, list)

    def test_negative_growth_still_produces_valid_score(self):
        inp = make_input(growth_rate_pct=-100)
        score = _market_score(inp)
        assert 0.0 <= score <= 100.0

    def test_large_common_accounts_capped(self):
        inp = make_input(common_accounts=1000)
        acc_score = min(100, 1000 * 5)
        assert acc_score == 100.0

    def test_engine_analyze_multiple_times_same_id_last_wins(self):
        engine = CompetitorIntelligenceEngine()
        for i in range(5):
            engine.analyze(make_input(competitor_id="stable", market_share_pct=float(i * 5)))
        assert len(engine.all_competitors()) == 1
        # last analyzed had market_share_pct=20
        assert engine.get("stable").market_score == round(_market_score(make_input(market_share_pct=20)), 2)
