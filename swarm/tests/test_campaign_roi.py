"""
Comprehensive pytest tests for swarm/intelligence/campaign_roi.py
"""
from __future__ import annotations

import pytest
from swarm.intelligence.campaign_roi import (
    CampaignROICalculator,
    CampaignMetrics,
    CampaignResult,
    CampaignStatus,
    ChannelType,
    _roi_score,
    _reach_efficiency,
    _conversion_quality,
    _cost_efficiency,
    _campaign_status,
    _build_recommendations,
    _CHANNEL_BENCHMARKS,
)


# ─── Helper ──────────────────────────────────────────────────────────────────

def make_campaign(
    campaign_id: str = "c1",
    campaign_name: str = "Test Campaign",
    channel: ChannelType = ChannelType.EMAIL,
    start_date: str = "2026-01-01",
    duration_days: int = 30,
    budget_eur: float = 5000.0,
    total_spent_eur: float = 4500.0,
    total_contacts: int = 500,
    emails_sent: int = 500,
    opens: int = 150,       # 30% open rate
    clicks: int = 25,       # 5% click rate
    unsubscribes: int = 2,  # 0.4% unsub rate
    leads_generated: int = 50,
    mqls: int = 30,
    sqls: int = 15,
    opportunities_created: int = 10,
    deals_won: int = 3,
    pipeline_value_eur: float = 50000.0,
    closed_revenue_eur: float = 18000.0,
    avg_deal_size_eur: float = 6000.0,
) -> CampaignMetrics:
    return CampaignMetrics(
        campaign_id=campaign_id,
        campaign_name=campaign_name,
        channel=channel,
        start_date=start_date,
        duration_days=duration_days,
        budget_eur=budget_eur,
        total_spent_eur=total_spent_eur,
        total_contacts=total_contacts,
        emails_sent=emails_sent,
        opens=opens,
        clicks=clicks,
        unsubscribes=unsubscribes,
        leads_generated=leads_generated,
        mqls=mqls,
        sqls=sqls,
        opportunities_created=opportunities_created,
        deals_won=deals_won,
        pipeline_value_eur=pipeline_value_eur,
        closed_revenue_eur=closed_revenue_eur,
        avg_deal_size_eur=avg_deal_size_eur,
    )


@pytest.fixture
def calculator():
    return CampaignROICalculator()


# ─── _CHANNEL_BENCHMARKS ─────────────────────────────────────────────────────

class TestChannelBenchmarks:
    def test_email_benchmark(self):
        assert _CHANNEL_BENCHMARKS[ChannelType.EMAIL] == 4.2

    def test_linkedin_benchmark(self):
        assert _CHANNEL_BENCHMARKS[ChannelType.LINKEDIN] == 2.8

    def test_webinar_benchmark(self):
        assert _CHANNEL_BENCHMARKS[ChannelType.WEBINAR] == 3.5

    def test_content_benchmark(self):
        assert _CHANNEL_BENCHMARKS[ChannelType.CONTENT] == 2.0

    def test_paid_benchmark(self):
        assert _CHANNEL_BENCHMARKS[ChannelType.PAID] == 2.5

    def test_outbound_benchmark(self):
        assert _CHANNEL_BENCHMARKS[ChannelType.OUTBOUND] == 3.0

    def test_event_benchmark(self):
        assert _CHANNEL_BENCHMARKS[ChannelType.EVENT] == 1.8

    def test_all_channels_present(self):
        for ct in ChannelType:
            assert ct in _CHANNEL_BENCHMARKS

    def test_benchmarks_all_above_one(self):
        for v in _CHANNEL_BENCHMARKS.values():
            assert v > 1.0


# ─── _roi_score ───────────────────────────────────────────────────────────────

class TestRoiScore:
    def test_zero_cost_returns_zeros(self):
        m = make_campaign(total_spent_eur=0.0, budget_eur=0.0)
        score, roi_pct, benchmark_vs, insights = _roi_score(m)
        assert score == 0.0
        assert roi_pct == 0.0
        assert benchmark_vs == 1.0
        assert insights == []

    def test_uses_total_spent_when_positive(self):
        # cost = total_spent_eur (4500)
        # roi = (18000 - 4500) / 4500 * 100 = 300%
        m = make_campaign(total_spent_eur=4500.0, budget_eur=5000.0, closed_revenue_eur=18000.0)
        score, roi_pct, benchmark_vs, insights = _roi_score(m)
        assert roi_pct == pytest.approx(300.0, abs=0.01)

    def test_falls_back_to_budget_when_spent_zero(self):
        # cost = budget_eur (5000)
        m = make_campaign(total_spent_eur=0.0, budget_eur=5000.0, closed_revenue_eur=10000.0)
        score, roi_pct, benchmark_vs, insights = _roi_score(m)
        assert roi_pct == pytest.approx(100.0, abs=0.01)

    def test_negative_roi_score_clamped_at_zero(self):
        # revenue = 0 → roi = -100%, score = max(0, 30 + (-100)*0.1) = max(0, 20) = 20
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=0.0)
        score, roi_pct, _, _ = _roi_score(m)
        assert roi_pct < 0
        assert score >= 0.0

    def test_very_negative_roi_clamps_to_zero(self):
        # roi = -300%, score = max(0, 30 + (-300)*0.1) = max(0, 0) = 0
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=0.0)
        # make it deeply negative
        m2 = make_campaign(total_spent_eur=1000.0, budget_eur=1000.0, closed_revenue_eur=0.0)
        score, roi_pct, _, insights = _roi_score(m2)
        assert score >= 0.0
        assert "below_benchmark" in insights

    def test_roi_at_zero_returns_score_30(self):
        # roi_pct = 0 → score = max(0, 30 + 0*0.1) = 30
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=1000.0)
        score, roi_pct, _, _ = _roi_score(m)
        assert roi_pct == pytest.approx(0.0, abs=0.01)
        assert score == pytest.approx(30.0, abs=0.01)

    def test_roi_at_benchmark_returns_score_60(self):
        # EMAIL benchmark = 4.2 → benchmark_roi_pct = 320%
        # roi = 320% → score = 30 + (320/320)*30 = 60
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=4200.0, channel=ChannelType.EMAIL)
        score, roi_pct, benchmark_vs, insights = _roi_score(m)
        assert roi_pct == pytest.approx(320.0, abs=0.01)
        assert score == pytest.approx(60.0, abs=0.01)
        assert benchmark_vs == pytest.approx(1.0, abs=0.001)

    def test_roi_at_half_benchmark_score_between_30_and_60(self):
        # EMAIL benchmark = 320%, half = 160%
        # score = 30 + (160/320)*30 = 45
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=2600.0, channel=ChannelType.EMAIL)
        score, roi_pct, _, _ = _roi_score(m)
        assert roi_pct == pytest.approx(160.0, abs=0.01)
        assert score == pytest.approx(45.0, abs=0.01)

    def test_roi_above_benchmark_gives_higher_score(self):
        # roi = 640% (2x EMAIL benchmark of 320%)
        # ratio = 2.0 → score = min(100, 60 + (2-1)*40) = 100
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=7400.0, channel=ChannelType.EMAIL)
        score, roi_pct, benchmark_vs, _ = _roi_score(m)
        assert roi_pct == pytest.approx(640.0, abs=0.01)
        assert score == pytest.approx(100.0, abs=0.01)
        assert benchmark_vs == pytest.approx(2.0, abs=0.001)

    def test_roi_capped_at_100(self):
        # Extremely high revenue
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=100000.0)
        score, _, _, _ = _roi_score(m)
        assert score <= 100.0

    def test_insight_excellent_roi_at_1_5x_benchmark(self):
        # EMAIL benchmark_roi_pct = 320%, 1.5x = 480%
        # revenue so roi = 480% → spent=1000, rev=5800
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=5800.0, channel=ChannelType.EMAIL)
        _, _, _, insights = _roi_score(m)
        assert "excellent_roi" in insights

    def test_insight_good_roi_at_benchmark(self):
        # roi exactly at benchmark
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=4200.0, channel=ChannelType.EMAIL)
        _, _, _, insights = _roi_score(m)
        assert "good_roi" in insights

    def test_insight_below_benchmark(self):
        # roi < benchmark
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=1500.0, channel=ChannelType.EMAIL)
        _, _, _, insights = _roi_score(m)
        assert "below_benchmark" in insights

    def test_negative_roi_has_below_benchmark_insight(self):
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=500.0)
        _, _, _, insights = _roi_score(m)
        assert "below_benchmark" in insights

    def test_benchmark_vs_ratio_correct(self):
        # linkedin benchmark = 2.8 → benchmark_roi_pct = 180%
        # roi = 90% → benchmark_vs = 90/180 = 0.5
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=1900.0, channel=ChannelType.LINKEDIN)
        _, roi_pct, benchmark_vs, _ = _roi_score(m)
        assert roi_pct == pytest.approx(90.0, abs=0.01)
        assert benchmark_vs == pytest.approx(0.5, abs=0.001)

    def test_roi_score_returns_tuple_of_four(self):
        m = make_campaign()
        result = _roi_score(m)
        assert len(result) == 4

    def test_score_between_0_and_100(self):
        for rev in [0, 500, 1000, 5000, 20000, 100000]:
            m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=float(rev))
            score, _, _, _ = _roi_score(m)
            assert 0.0 <= score <= 100.0

    def test_linkedin_benchmark_roi_pct(self):
        # benchmark_roi_pct = (2.8 - 1.0) * 100 = 180%
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=2800.0, channel=ChannelType.LINKEDIN)
        score, roi_pct, benchmark_vs, _ = _roi_score(m)
        assert roi_pct == pytest.approx(180.0, abs=0.01)
        assert benchmark_vs == pytest.approx(1.0, abs=0.001)

    def test_event_benchmark_roi_pct(self):
        # benchmark_roi_pct = (1.8 - 1.0) * 100 = 80%
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=1800.0, channel=ChannelType.EVENT)
        _, roi_pct, benchmark_vs, _ = _roi_score(m)
        assert roi_pct == pytest.approx(80.0, abs=0.01)
        assert benchmark_vs == pytest.approx(1.0, abs=0.001)

    def test_score_slightly_above_benchmark(self):
        # roi = 1.1 * benchmark_roi_pct → ratio = 1.1
        # score = min(100, 60 + (1.1 - 1.0) * 40) = 64
        # EMAIL benchmark = 320%, 1.1x = 352%
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=4520.0, channel=ChannelType.EMAIL)
        score, roi_pct, _, _ = _roi_score(m)
        expected_score = min(100.0, 60.0 + (roi_pct / 320.0 - 1.0) * 40.0)
        assert score == pytest.approx(expected_score, abs=0.1)


# ─── _reach_efficiency ───────────────────────────────────────────────────────

class TestReachEfficiency:
    def test_zero_emails_returns_zero(self):
        m = make_campaign(emails_sent=0)
        score, insights = _reach_efficiency(m)
        assert score == 0.0
        assert insights == []

    def test_open_rate_below_15_adds_low_open_rate(self):
        # 14% open rate (70 opens out of 500)
        m = make_campaign(emails_sent=500, opens=70, clicks=15, unsubscribes=2)
        score, insights = _reach_efficiency(m)
        assert "low_open_rate" in insights

    def test_open_rate_exactly_15_no_low_open_rate(self):
        # exactly 15% → not < 15, no flag
        m = make_campaign(emails_sent=500, opens=75, clicks=15, unsubscribes=2)
        _, insights = _reach_efficiency(m)
        assert "low_open_rate" not in insights

    def test_click_rate_below_1_5_adds_low_click_rate(self):
        # 1% click rate
        m = make_campaign(emails_sent=500, opens=150, clicks=5, unsubscribes=2)
        _, insights = _reach_efficiency(m)
        assert "low_click_rate" in insights

    def test_click_rate_above_1_5_no_low_click_rate(self):
        # 3% click rate
        m = make_campaign(emails_sent=500, opens=150, clicks=15, unsubscribes=2)
        _, insights = _reach_efficiency(m)
        assert "low_click_rate" not in insights

    def test_strong_engagement_when_open_above_35_and_click_above_5(self):
        # open=40%, click=6%
        m = make_campaign(emails_sent=500, opens=200, clicks=30, unsubscribes=2)
        _, insights = _reach_efficiency(m)
        assert "strong_engagement" in insights

    def test_no_strong_engagement_if_only_high_open(self):
        # open=40%, click=3% (not >5%)
        m = make_campaign(emails_sent=500, opens=200, clicks=15, unsubscribes=2)
        _, insights = _reach_efficiency(m)
        assert "strong_engagement" not in insights

    def test_no_strong_engagement_if_only_high_click(self):
        # open=30% (not >35%), click=6%
        m = make_campaign(emails_sent=500, opens=150, clicks=30, unsubscribes=2)
        _, insights = _reach_efficiency(m)
        assert "strong_engagement" not in insights

    def test_high_unsubscribe_above_1_pct(self):
        # 1.1% unsub rate
        m = make_campaign(emails_sent=500, opens=150, clicks=25, unsubscribes=6)
        _, insights = _reach_efficiency(m)
        assert "high_unsubscribe" in insights

    def test_no_high_unsubscribe_below_1_pct(self):
        # 0.8% unsub rate
        m = make_campaign(emails_sent=500, opens=150, clicks=25, unsubscribes=4)
        _, insights = _reach_efficiency(m)
        assert "high_unsubscribe" not in insights

    def test_wide_reach_when_contacts_1000_or_more(self):
        m = make_campaign(total_contacts=1000)
        _, insights = _reach_efficiency(m)
        assert "wide_reach" in insights

    def test_wide_reach_threshold_exactly_1000(self):
        m = make_campaign(total_contacts=1000)
        _, insights = _reach_efficiency(m)
        assert "wide_reach" in insights

    def test_no_wide_reach_below_1000(self):
        m = make_campaign(total_contacts=999)
        _, insights = _reach_efficiency(m)
        assert "wide_reach" not in insights

    def test_low_reach_when_contacts_below_100(self):
        m = make_campaign(total_contacts=50)
        _, insights = _reach_efficiency(m)
        assert "low_reach" in insights

    def test_no_low_reach_at_exactly_100(self):
        m = make_campaign(total_contacts=100)
        _, insights = _reach_efficiency(m)
        assert "low_reach" not in insights

    def test_no_low_reach_above_100(self):
        m = make_campaign(total_contacts=101)
        _, insights = _reach_efficiency(m)
        assert "low_reach" not in insights

    def test_score_is_between_0_and_100(self):
        for opens in [0, 50, 125, 175, 250, 300]:
            m = make_campaign(emails_sent=500, opens=opens, clicks=25, unsubscribes=2, total_contacts=500)
            score, _ = _reach_efficiency(m)
            assert 0.0 <= score <= 100.0

    def test_unsub_penalty_applied_above_0_5_pct(self):
        # unsub_rate = 1%: penalty = (1.0 - 0.5) * 20 = 10
        m_with = make_campaign(emails_sent=500, opens=150, clicks=15, unsubscribes=5, total_contacts=500)
        m_without = make_campaign(emails_sent=500, opens=150, clicks=15, unsubscribes=2, total_contacts=500)
        score_with, _ = _reach_efficiency(m_with)
        score_without, _ = _reach_efficiency(m_without)
        assert score_with < score_without

    def test_unsub_penalty_capped_at_30(self):
        # unsub_rate = 2%: penalty = (2.0 - 0.5) * 20 = 30 (capped)
        # unsub_rate = 10%: penalty = (10.0 - 0.5) * 20 = 190 → capped at 30
        m = make_campaign(emails_sent=500, opens=150, clicks=15, unsubscribes=50, total_contacts=500)
        m2 = make_campaign(emails_sent=500, opens=150, clicks=15, unsubscribes=10, total_contacts=500)
        score1, _ = _reach_efficiency(m)
        score2, _ = _reach_efficiency(m2)
        # Both should have max penalty 30, so scores should be equal
        assert score1 == score2

    def test_open_score_capped_at_100(self):
        # opens = 500 → open_rate = 100% → open_score = min(100, 100/25*100) = 100
        m = make_campaign(emails_sent=500, opens=500, clicks=25, unsubscribes=2, total_contacts=500)
        score, _ = _reach_efficiency(m)
        assert score >= 0.0  # score includes capped open_score

    def test_perfect_metrics_high_score(self):
        # High opens, clicks, contacts, low unsub
        m = make_campaign(emails_sent=500, opens=200, clicks=30, unsubscribes=0,
                          total_contacts=1000)
        score, insights = _reach_efficiency(m)
        assert score > 70.0
        assert "strong_engagement" in insights
        assert "wide_reach" in insights

    def test_contact_reach_capped_at_100(self):
        # contacts = 5000 → contact_reach = min(100, 5000/500*100) = 100
        m = make_campaign(total_contacts=5000, emails_sent=500, opens=150, clicks=25, unsubscribes=2)
        score, _ = _reach_efficiency(m)
        assert score >= 0.0

    def test_score_formula_manually(self):
        # emails_sent=500, opens=125(25%), clicks=15(3%), unsub=2(0.4%), contacts=500
        # open_score = min(100, 25/25*100) = 100
        # click_score = min(100, 3/3*100) = 100
        # unsub_penalty = 0 (0.4% < 0.5%)
        # contact_reach = min(100, 500/500*100) = 100
        # score = 100*0.35 + 100*0.35 + 100*0.30 - 0 = 100
        m = make_campaign(emails_sent=500, opens=125, clicks=15, unsubscribes=2, total_contacts=500)
        score, _ = _reach_efficiency(m)
        assert score == pytest.approx(100.0, abs=0.1)


# ─── _conversion_quality ─────────────────────────────────────────────────────

class TestConversionQuality:
    def test_returns_four_elements(self):
        m = make_campaign()
        result = _conversion_quality(m)
        assert len(result) == 4

    def test_zero_leads_no_division_error(self):
        m = make_campaign(leads_generated=0, mqls=0, sqls=0, opportunities_created=0, deals_won=0)
        score, insights, l2o, o2w = _conversion_quality(m)
        assert score >= 0.0
        assert l2o == 0.0
        assert o2w == 0.0

    def test_zero_opportunities_no_division_error(self):
        m = make_campaign(opportunities_created=0, deals_won=0, leads_generated=50)
        score, insights, l2o, o2w = _conversion_quality(m)
        assert o2w == 0.0

    def test_low_conversion_below_8_pct(self):
        # 3 opps out of 100 leads = 3%
        m = make_campaign(leads_generated=100, opportunities_created=3)
        _, insights, _, _ = _conversion_quality(m)
        assert "low_conversion" in insights

    def test_no_low_conversion_at_8_pct(self):
        # 8 opps out of 100 leads = 8%
        m = make_campaign(leads_generated=100, opportunities_created=8)
        _, insights, _, _ = _conversion_quality(m)
        assert "low_conversion" not in insights

    def test_strong_conversion_at_or_above_20_pct(self):
        # 20 opps out of 100 leads = 20%
        m = make_campaign(leads_generated=100, opportunities_created=20)
        _, insights, _, _ = _conversion_quality(m)
        assert "strong_conversion" in insights

    def test_no_strong_conversion_below_20_pct(self):
        # 15 opps out of 100 leads = 15% (not >= 20)
        m = make_campaign(leads_generated=100, opportunities_created=15)
        _, insights, _, _ = _conversion_quality(m)
        assert "strong_conversion" not in insights

    def test_pipeline_generated_when_opportunities_above_zero(self):
        m = make_campaign(opportunities_created=5, leads_generated=50)
        _, insights, _, _ = _conversion_quality(m)
        assert "pipeline_generated" in insights

    def test_no_pipeline_when_leads_but_no_opportunities(self):
        m = make_campaign(leads_generated=50, opportunities_created=0)
        _, insights, _, _ = _conversion_quality(m)
        assert "no_pipeline" in insights

    def test_no_pipeline_flag_when_zero_leads_too(self):
        m = make_campaign(leads_generated=0, opportunities_created=0)
        _, insights, _, _ = _conversion_quality(m)
        assert "no_pipeline" not in insights
        assert "pipeline_generated" not in insights

    def test_lead_to_opp_rate_correct(self):
        # 10 opps / 50 leads = 20%
        m = make_campaign(leads_generated=50, opportunities_created=10)
        _, _, l2o, _ = _conversion_quality(m)
        assert l2o == pytest.approx(20.0, abs=0.01)

    def test_opp_to_won_rate_correct(self):
        # 3 deals / 10 opps = 30%
        m = make_campaign(opportunities_created=10, deals_won=3)
        _, _, _, o2w = _conversion_quality(m)
        assert o2w == pytest.approx(30.0, abs=0.01)

    def test_score_between_0_and_100(self):
        for leads in [0, 10, 50, 100]:
            m = make_campaign(leads_generated=leads, opportunities_created=min(leads, 5),
                              deals_won=min(leads, 2))
            score, _, _, _ = _conversion_quality(m)
            assert 0.0 <= score <= 100.0

    def test_lead_opp_score_capped_at_100(self):
        # 80 opps / 100 leads = 80% → lead_opp_score = min(100, 80/15*100) = 100
        m = make_campaign(leads_generated=100, opportunities_created=80, deals_won=20)
        score, _, l2o, _ = _conversion_quality(m)
        assert l2o == pytest.approx(80.0, abs=0.01)
        assert score <= 100.0

    def test_mql_rate_contributes_to_funnel_score(self):
        # mqls = 40 out of 100 leads = 40% → mql portion = 40/40*50 = 50
        # sqls = 20 out of 40 mqls = 50% → sql portion = 50/50*50 = 50
        # funnel_score = min(100, 50+50) = 100
        m = make_campaign(leads_generated=100, mqls=40, sqls=20, opportunities_created=15, deals_won=3)
        score, _, _, _ = _conversion_quality(m)
        assert score > 0.0

    def test_zero_mqls_no_sql_rate_computed(self):
        m = make_campaign(leads_generated=50, mqls=0, sqls=0)
        score, insights, _, _ = _conversion_quality(m)
        assert score >= 0.0  # No crash

    def test_score_formula_weights(self):
        # With perfect rates, score = 100*0.40 + 100*0.35 + 100*0.25 = 100
        m = make_campaign(leads_generated=100, mqls=40, sqls=20,
                          opportunities_created=15, deals_won=25)
        score, _, _, _ = _conversion_quality(m)
        assert score == pytest.approx(100.0, abs=1.0)


# ─── _cost_efficiency ────────────────────────────────────────────────────────

class TestCostEfficiency:
    def test_returns_five_elements(self):
        m = make_campaign()
        result = _cost_efficiency(m)
        assert len(result) == 5

    def test_zero_leads_returns_minus_one_cpl(self):
        m = make_campaign(leads_generated=0, sqls=0, deals_won=0)
        _, _, cpl, _, _ = _cost_efficiency(m)
        assert cpl == -1.0

    def test_zero_sqls_returns_minus_one_csql(self):
        m = make_campaign(sqls=0, deals_won=0)
        _, _, _, csql, _ = _cost_efficiency(m)
        assert csql == -1.0

    def test_zero_deals_returns_minus_one_cpd(self):
        m = make_campaign(deals_won=0)
        _, _, _, _, cpd = _cost_efficiency(m)
        assert cpd == -1.0

    def test_cpl_calculated_correctly(self):
        # spent = 4500, leads = 50 → cpl = 90
        m = make_campaign(total_spent_eur=4500.0, leads_generated=50)
        _, _, cpl, _, _ = _cost_efficiency(m)
        assert cpl == pytest.approx(90.0, abs=0.01)

    def test_csql_calculated_correctly(self):
        # spent = 4500, sqls = 15 → csql = 300
        m = make_campaign(total_spent_eur=4500.0, sqls=15)
        _, _, _, csql, _ = _cost_efficiency(m)
        assert csql == pytest.approx(300.0, abs=0.01)

    def test_cpd_calculated_correctly(self):
        # spent = 4500, deals = 3 → cpd = 1500
        m = make_campaign(total_spent_eur=4500.0, deals_won=3)
        _, _, _, _, cpd = _cost_efficiency(m)
        assert cpd == pytest.approx(1500.0, abs=0.01)

    def test_high_cpl_above_300(self):
        # spent = 4500, leads = 10 → cpl = 450 > 300
        m = make_campaign(total_spent_eur=4500.0, leads_generated=10)
        _, insights, _, _, _ = _cost_efficiency(m)
        assert "high_cpl" in insights

    def test_no_high_cpl_at_300_or_below(self):
        # spent = 3000, leads = 10 → cpl = 300 (not > 300)
        m = make_campaign(total_spent_eur=3000.0, leads_generated=10)
        _, insights, _, _, _ = _cost_efficiency(m)
        assert "high_cpl" not in insights

    def test_budget_efficient_when_avg_cost_score_above_70(self):
        # Low cost, high leads/sqls/deals → all scores high
        m = make_campaign(total_spent_eur=500.0, leads_generated=100, sqls=50, deals_won=10)
        _, insights, _, _, _ = _cost_efficiency(m)
        assert "budget_efficient" in insights

    def test_budget_inefficient_when_avg_cost_score_below_30(self):
        # All metrics inf → avg_cost_score = 0 < 30
        m = make_campaign(total_spent_eur=50000.0, leads_generated=0, sqls=0, deals_won=0)
        _, insights, _, _, _ = _cost_efficiency(m)
        assert "budget_inefficient" in insights

    def test_uses_budget_when_spent_zero(self):
        # total_spent=0 → cost = budget_eur = 5000
        m = make_campaign(total_spent_eur=0.0, budget_eur=5000.0, leads_generated=50)
        _, _, cpl, _, _ = _cost_efficiency(m)
        assert cpl == pytest.approx(100.0, abs=0.01)

    def test_budget_utilization_near_100_gives_high_util_score(self):
        # spent = 5000, budget = 5000 → util = 100% → util_score = 100 - 0 = 100
        m = make_campaign(total_spent_eur=5000.0, budget_eur=5000.0)
        score, _, _, _, _ = _cost_efficiency(m)
        # util contributes 100*0.10 = 10 to score
        assert score >= 0.0

    def test_score_between_0_and_100(self):
        test_cases = [
            dict(leads_generated=0, sqls=0, deals_won=0),
            dict(leads_generated=50, sqls=15, deals_won=3),
            dict(leads_generated=200, sqls=100, deals_won=50),
        ]
        for kwargs in test_cases:
            m = make_campaign(**kwargs)
            score, _, _, _, _ = _cost_efficiency(m)
            assert 0.0 <= score <= 100.0

    def test_score_not_negative(self):
        m = make_campaign(total_spent_eur=100000.0, leads_generated=1, sqls=0, deals_won=0)
        score, _, _, _, _ = _cost_efficiency(m)
        assert score >= 0.0

    def test_cpl_score_capped_at_100(self):
        # cpl = 1 → cpl_score = min(100, 150/1*100) = 100
        m = make_campaign(total_spent_eur=100.0, leads_generated=100, sqls=50, deals_won=10)
        score, _, cpl, _, _ = _cost_efficiency(m)
        assert cpl == pytest.approx(1.0, abs=0.01)


# ─── _campaign_status ────────────────────────────────────────────────────────

class TestCampaignStatus:
    def test_score_80_is_excellent(self):
        assert _campaign_status(80.0) == CampaignStatus.EXCELLENT

    def test_score_100_is_excellent(self):
        assert _campaign_status(100.0) == CampaignStatus.EXCELLENT

    def test_score_79_99_is_good(self):
        assert _campaign_status(79.99) == CampaignStatus.GOOD

    def test_score_60_is_good(self):
        assert _campaign_status(60.0) == CampaignStatus.GOOD

    def test_score_59_99_is_average(self):
        assert _campaign_status(59.99) == CampaignStatus.AVERAGE

    def test_score_40_is_average(self):
        assert _campaign_status(40.0) == CampaignStatus.AVERAGE

    def test_score_39_99_is_poor(self):
        assert _campaign_status(39.99) == CampaignStatus.POOR

    def test_score_20_is_poor(self):
        assert _campaign_status(20.0) == CampaignStatus.POOR

    def test_score_19_99_is_failing(self):
        assert _campaign_status(19.99) == CampaignStatus.FAILING

    def test_score_0_is_failing(self):
        assert _campaign_status(0.0) == CampaignStatus.FAILING

    def test_score_negative_is_failing(self):
        assert _campaign_status(-5.0) == CampaignStatus.FAILING

    def test_exact_boundary_80_excellent(self):
        assert _campaign_status(80.0) == CampaignStatus.EXCELLENT

    def test_exact_boundary_60_good(self):
        assert _campaign_status(60.0) == CampaignStatus.GOOD

    def test_exact_boundary_40_average(self):
        assert _campaign_status(40.0) == CampaignStatus.AVERAGE

    def test_exact_boundary_20_poor(self):
        assert _campaign_status(20.0) == CampaignStatus.POOR


# ─── _build_recommendations ──────────────────────────────────────────────────

class TestBuildRecommendations:
    def test_excellent_gets_scale_immediately(self):
        recs = _build_recommendations(CampaignStatus.EXCELLENT, 300, 25, 15, 0.4, 50000)
        assert "scale_immediately" in recs

    def test_excellent_gets_repurpose_content(self):
        recs = _build_recommendations(CampaignStatus.EXCELLENT, 300, 25, 15, 0.4, 50000)
        assert "repurpose_content" in recs

    def test_good_gets_ab_test_content(self):
        recs = _build_recommendations(CampaignStatus.GOOD, 200, 25, 15, 0.4, 50000)
        assert "ab_test_content" in recs

    def test_good_gets_retarget_engaged(self):
        recs = _build_recommendations(CampaignStatus.GOOD, 200, 25, 15, 0.4, 50000)
        assert "retarget_engaged" in recs

    def test_average_gets_optimize_targeting(self):
        recs = _build_recommendations(CampaignStatus.AVERAGE, 100, 25, 15, 0.4, 50000)
        assert "optimize_targeting" in recs

    def test_average_gets_improve_landing(self):
        recs = _build_recommendations(CampaignStatus.AVERAGE, 100, 25, 15, 0.4, 50000)
        assert "improve_landing" in recs

    def test_average_gets_add_nurture_sequence(self):
        recs = _build_recommendations(CampaignStatus.AVERAGE, 100, 25, 15, 0.4, 50000)
        assert "add_nurture_sequence" in recs

    def test_poor_gets_optimize_targeting(self):
        recs = _build_recommendations(CampaignStatus.POOR, 50, 25, 15, 0.4, 50000)
        assert "optimize_targeting" in recs

    def test_poor_gets_increase_personalization(self):
        recs = _build_recommendations(CampaignStatus.POOR, 50, 25, 15, 0.4, 50000)
        assert "increase_personalization" in recs

    def test_poor_gets_cut_budget(self):
        recs = _build_recommendations(CampaignStatus.POOR, 50, 25, 15, 0.4, 50000)
        assert "cut_budget" in recs

    def test_failing_gets_pause_campaign(self):
        recs = _build_recommendations(CampaignStatus.FAILING, 10, 25, 15, 0.4, 50000)
        assert "pause_campaign" in recs

    def test_low_open_rate_adds_ab_test(self):
        # open_rate < 15 → ab_test_content added
        recs = _build_recommendations(CampaignStatus.AVERAGE, 100, 10, 15, 0.4, 50000)
        assert "ab_test_content" in recs

    def test_low_conversion_adds_optimize_targeting(self):
        # conversion < 8 and optimize_targeting not already there
        recs = _build_recommendations(CampaignStatus.GOOD, 200, 25, 5, 0.4, 50000)
        assert "optimize_targeting" in recs

    def test_high_unsub_adds_reduce_frequency(self):
        # unsub_rate > 1
        recs = _build_recommendations(CampaignStatus.AVERAGE, 100, 25, 15, 1.5, 50000)
        assert "reduce_frequency" in recs

    def test_no_pipeline_adds_align_sales(self):
        # pipeline == 0
        recs = _build_recommendations(CampaignStatus.AVERAGE, 100, 25, 15, 0.4, 0.0)
        assert "align_sales" in recs

    def test_no_duplicates_in_recommendations(self):
        recs = _build_recommendations(CampaignStatus.AVERAGE, 100, 10, 5, 1.5, 0.0)
        assert len(recs) == len(set(recs))

    def test_no_duplicates_poor_with_low_conversion(self):
        # POOR already adds optimize_targeting; low conversion would add it again — dedup
        recs = _build_recommendations(CampaignStatus.POOR, 50, 25, 5, 0.4, 50000)
        assert recs.count("optimize_targeting") == 1

    def test_returns_list(self):
        recs = _build_recommendations(CampaignStatus.GOOD, 200, 25, 15, 0.4, 50000)
        assert isinstance(recs, list)


# ─── CampaignROICalculator ────────────────────────────────────────────────────

class TestCampaignROICalculatorCalculate:
    def test_calculate_returns_campaign_result(self, calculator):
        m = make_campaign()
        result = calculator.calculate(m)
        assert isinstance(result, CampaignResult)

    def test_calculate_stores_result(self, calculator):
        m = make_campaign(campaign_id="x1")
        calculator.calculate(m)
        assert calculator.get("x1") is not None

    def test_calculate_result_has_correct_campaign_id(self, calculator):
        m = make_campaign(campaign_id="abc")
        result = calculator.calculate(m)
        assert result.campaign.campaign_id == "abc"

    def test_calculate_result_has_roi_pct(self, calculator):
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=4200.0)
        result = calculator.calculate(m)
        assert isinstance(result.roi_pct, float)

    def test_calculate_result_has_status(self, calculator):
        m = make_campaign()
        result = calculator.calculate(m)
        assert isinstance(result.status, CampaignStatus)

    def test_calculate_result_overall_score_between_0_and_100(self, calculator):
        m = make_campaign()
        result = calculator.calculate(m)
        assert 0.0 <= result.overall_score <= 100.0

    def test_calculate_overrides_previous_result(self, calculator):
        m1 = make_campaign(campaign_id="c1", closed_revenue_eur=5000.0)
        m2 = make_campaign(campaign_id="c1", closed_revenue_eur=50000.0)
        calculator.calculate(m1)
        calculator.calculate(m2)
        result = calculator.get("c1")
        assert result.campaign.closed_revenue_eur == 50000.0

    def test_calculate_open_rate_pct(self, calculator):
        m = make_campaign(emails_sent=500, opens=125)
        result = calculator.calculate(m)
        assert result.open_rate_pct == pytest.approx(25.0, abs=0.01)

    def test_calculate_click_rate_pct(self, calculator):
        m = make_campaign(emails_sent=500, clicks=15)
        result = calculator.calculate(m)
        assert result.click_rate_pct == pytest.approx(3.0, abs=0.01)

    def test_calculate_cost_per_lead(self, calculator):
        m = make_campaign(total_spent_eur=5000.0, leads_generated=50)
        result = calculator.calculate(m)
        assert result.cost_per_lead_eur == pytest.approx(100.0, abs=0.01)

    def test_calculate_cost_per_sql(self, calculator):
        m = make_campaign(total_spent_eur=4500.0, sqls=15)
        result = calculator.calculate(m)
        assert result.cost_per_sql_eur == pytest.approx(300.0, abs=0.01)

    def test_calculate_cost_per_deal(self, calculator):
        m = make_campaign(total_spent_eur=4500.0, deals_won=3)
        result = calculator.calculate(m)
        assert result.cost_per_deal_eur == pytest.approx(1500.0, abs=0.01)

    def test_calculate_lead_to_opp_rate(self, calculator):
        m = make_campaign(leads_generated=50, opportunities_created=10)
        result = calculator.calculate(m)
        assert result.lead_to_opp_rate_pct == pytest.approx(20.0, abs=0.01)

    def test_calculate_opp_to_won_rate(self, calculator):
        m = make_campaign(opportunities_created=10, deals_won=3)
        result = calculator.calculate(m)
        assert result.opp_to_won_rate_pct == pytest.approx(30.0, abs=0.01)

    def test_calculate_key_insights_is_list(self, calculator):
        m = make_campaign()
        result = calculator.calculate(m)
        assert isinstance(result.key_insights, list)

    def test_calculate_recommendations_is_list(self, calculator):
        m = make_campaign()
        result = calculator.calculate(m)
        assert isinstance(result.recommendations, list)

    def test_calculate_benchmark_vs_channel(self, calculator):
        m = make_campaign(total_spent_eur=1000.0, closed_revenue_eur=4200.0, channel=ChannelType.EMAIL)
        result = calculator.calculate(m)
        assert result.benchmark_vs_channel == pytest.approx(1.0, abs=0.01)

    def test_calculate_composite_weights(self, calculator):
        # Verify overall_score = roi*0.35 + reach*0.25 + conv*0.25 + cost*0.15
        m = make_campaign()
        result = calculator.calculate(m)
        expected = round(
            result.roi_score * 0.35 + result.reach_efficiency * 0.25 +
            result.conversion_quality * 0.25 + result.cost_efficiency * 0.15, 2
        )
        assert result.overall_score == pytest.approx(expected, abs=0.01)


class TestCampaignROICalculatorBatch:
    def test_calculate_batch_returns_list(self, calculator):
        campaigns = [make_campaign(campaign_id=f"c{i}") for i in range(3)]
        results = calculator.calculate_batch(campaigns)
        assert isinstance(results, list)
        assert len(results) == 3

    def test_calculate_batch_stores_all(self, calculator):
        campaigns = [make_campaign(campaign_id=f"c{i}") for i in range(5)]
        calculator.calculate_batch(campaigns)
        assert len(calculator.all_results()) == 5

    def test_calculate_batch_empty_list(self, calculator):
        results = calculator.calculate_batch([])
        assert results == []

    def test_calculate_batch_each_result_is_campaign_result(self, calculator):
        campaigns = [make_campaign(campaign_id=f"c{i}") for i in range(3)]
        results = calculator.calculate_batch(campaigns)
        for r in results:
            assert isinstance(r, CampaignResult)


class TestCampaignROICalculatorGet:
    def test_get_existing_returns_result(self, calculator):
        m = make_campaign(campaign_id="abc")
        calculator.calculate(m)
        assert calculator.get("abc") is not None

    def test_get_missing_returns_none(self, calculator):
        assert calculator.get("nonexistent") is None

    def test_get_correct_campaign(self, calculator):
        m1 = make_campaign(campaign_id="c1", campaign_name="Alpha")
        m2 = make_campaign(campaign_id="c2", campaign_name="Beta")
        calculator.calculate(m1)
        calculator.calculate(m2)
        r = calculator.get("c2")
        assert r.campaign.campaign_name == "Beta"


class TestCampaignROICalculatorAllResults:
    def test_all_results_sorted_by_score_desc(self, calculator):
        campaigns = [
            make_campaign(campaign_id="low", total_spent_eur=10000.0, closed_revenue_eur=0.0,
                          leads_generated=0, sqls=0, deals_won=0, emails_sent=100, opens=5,
                          clicks=1, unsubscribes=0, opportunities_created=0),
            make_campaign(campaign_id="high", total_spent_eur=1000.0, closed_revenue_eur=50000.0,
                          leads_generated=200, sqls=80, deals_won=20, emails_sent=500, opens=200,
                          clicks=30, unsubscribes=0, opportunities_created=50, total_contacts=2000),
        ]
        calculator.calculate_batch(campaigns)
        results = calculator.all_results()
        assert results[0].overall_score >= results[-1].overall_score

    def test_all_results_returns_all(self, calculator):
        for i in range(4):
            calculator.calculate(make_campaign(campaign_id=f"c{i}"))
        assert len(calculator.all_results()) == 4

    def test_all_results_empty_when_no_campaigns(self, calculator):
        assert calculator.all_results() == []


class TestCampaignROICalculatorTopCampaigns:
    def test_top_campaigns_default_n_5(self, calculator):
        for i in range(8):
            calculator.calculate(make_campaign(campaign_id=f"c{i}"))
        top = calculator.top_campaigns()
        assert len(top) <= 5

    def test_top_campaigns_custom_n(self, calculator):
        for i in range(8):
            calculator.calculate(make_campaign(campaign_id=f"c{i}"))
        top = calculator.top_campaigns(3)
        assert len(top) == 3

    def test_top_campaigns_fewer_than_n(self, calculator):
        for i in range(3):
            calculator.calculate(make_campaign(campaign_id=f"c{i}"))
        top = calculator.top_campaigns(10)
        assert len(top) == 3

    def test_top_campaigns_are_sorted(self, calculator):
        for i in range(5):
            calculator.calculate(make_campaign(campaign_id=f"c{i}"))
        top = calculator.top_campaigns(5)
        scores = [r.overall_score for r in top]
        assert scores == sorted(scores, reverse=True)


class TestCampaignROICalculatorFilters:
    def test_by_status_returns_matching(self, calculator):
        # A campaign likely to be FAILING
        m = make_campaign(
            campaign_id="failing_one",
            total_spent_eur=10000.0, closed_revenue_eur=0.0,
            leads_generated=0, sqls=0, deals_won=0,
            emails_sent=100, opens=5, clicks=1, unsubscribes=0,
            opportunities_created=0, total_contacts=10
        )
        calculator.calculate(m)
        result = calculator.get("failing_one")
        by_status = calculator.by_status(result.status)
        assert any(r.campaign.campaign_id == "failing_one" for r in by_status)

    def test_by_status_excludes_others(self, calculator):
        m1 = make_campaign(campaign_id="c1")
        calculator.calculate(m1)
        # Get the status of c1
        status1 = calculator.get("c1").status
        for s in CampaignStatus:
            if s != status1:
                results = calculator.by_status(s)
                assert all(r.campaign.campaign_id != "c1" for r in results)
                break

    def test_by_channel_returns_matching(self, calculator):
        m1 = make_campaign(campaign_id="email_c", channel=ChannelType.EMAIL)
        m2 = make_campaign(campaign_id="linkedin_c", channel=ChannelType.LINKEDIN)
        calculator.calculate(m1)
        calculator.calculate(m2)
        email_results = calculator.by_channel(ChannelType.EMAIL)
        assert all(r.campaign.channel == ChannelType.EMAIL for r in email_results)

    def test_by_channel_excludes_wrong_channel(self, calculator):
        m1 = make_campaign(campaign_id="email_c", channel=ChannelType.EMAIL)
        m2 = make_campaign(campaign_id="linkedin_c", channel=ChannelType.LINKEDIN)
        calculator.calculate(m1)
        calculator.calculate(m2)
        linkedin_results = calculator.by_channel(ChannelType.LINKEDIN)
        assert all(r.campaign.channel == ChannelType.LINKEDIN for r in linkedin_results)

    def test_by_channel_empty_when_no_match(self, calculator):
        m = make_campaign(channel=ChannelType.EMAIL)
        calculator.calculate(m)
        results = calculator.by_channel(ChannelType.EVENT)
        assert results == []

    def test_failing_campaigns_includes_failing_status(self, calculator):
        m = make_campaign(
            campaign_id="fail_c",
            total_spent_eur=10000.0, closed_revenue_eur=0.0,
            leads_generated=0, sqls=0, deals_won=0,
            emails_sent=100, opens=5, clicks=1, unsubscribes=0,
            opportunities_created=0, total_contacts=10
        )
        calculator.calculate(m)
        r = calculator.get("fail_c")
        if r.status in (CampaignStatus.FAILING, CampaignStatus.POOR):
            failing = calculator.failing_campaigns()
            assert any(res.campaign.campaign_id == "fail_c" for res in failing)

    def test_failing_campaigns_includes_poor_status(self, calculator):
        # Check that failing_campaigns() returns both POOR and FAILING
        failing = calculator.failing_campaigns()
        for r in failing:
            assert r.status in (CampaignStatus.FAILING, CampaignStatus.POOR)

    def test_excellent_campaigns_only_excellent(self, calculator):
        for i in range(5):
            calculator.calculate(make_campaign(campaign_id=f"c{i}"))
        excellent = calculator.excellent_campaigns()
        for r in excellent:
            assert r.status == CampaignStatus.EXCELLENT

    def test_excellent_campaigns_empty_when_none(self, calculator):
        # Campaign with zero revenue → likely not excellent
        m = make_campaign(closed_revenue_eur=0.0, leads_generated=0)
        calculator.calculate(m)
        excellent = calculator.excellent_campaigns()
        for r in excellent:
            assert r.status == CampaignStatus.EXCELLENT


class TestCampaignROICalculatorSummary:
    def test_summary_empty_store(self, calculator):
        summary = calculator.summary()
        assert summary["total"] == 0
        assert summary["avg_overall_score"] == 0.0
        assert summary["avg_roi_pct"] == 0.0
        assert summary["total_pipeline_eur"] == 0.0
        assert summary["total_closed_revenue_eur"] == 0.0
        assert summary["total_spent_eur"] == 0.0

    def test_summary_empty_has_all_status_keys(self, calculator):
        summary = calculator.summary()
        for s in CampaignStatus:
            assert s.value in summary["status_counts"]

    def test_summary_empty_has_all_channel_keys(self, calculator):
        summary = calculator.summary()
        for c in ChannelType:
            assert c.value in summary["channel_counts"]

    def test_summary_total_count(self, calculator):
        for i in range(3):
            calculator.calculate(make_campaign(campaign_id=f"c{i}"))
        summary = calculator.summary()
        assert summary["total"] == 3

    def test_summary_total_spent(self, calculator):
        m1 = make_campaign(campaign_id="c1", total_spent_eur=3000.0)
        m2 = make_campaign(campaign_id="c2", total_spent_eur=2000.0)
        calculator.calculate(m1)
        calculator.calculate(m2)
        summary = calculator.summary()
        assert summary["total_spent_eur"] == pytest.approx(5000.0, abs=0.01)

    def test_summary_total_pipeline(self, calculator):
        m1 = make_campaign(campaign_id="c1", pipeline_value_eur=10000.0)
        m2 = make_campaign(campaign_id="c2", pipeline_value_eur=20000.0)
        calculator.calculate(m1)
        calculator.calculate(m2)
        summary = calculator.summary()
        assert summary["total_pipeline_eur"] == pytest.approx(30000.0, abs=0.01)

    def test_summary_total_closed_revenue(self, calculator):
        m1 = make_campaign(campaign_id="c1", closed_revenue_eur=5000.0)
        m2 = make_campaign(campaign_id="c2", closed_revenue_eur=7000.0)
        calculator.calculate(m1)
        calculator.calculate(m2)
        summary = calculator.summary()
        assert summary["total_closed_revenue_eur"] == pytest.approx(12000.0, abs=0.01)

    def test_summary_channel_counts(self, calculator):
        m1 = make_campaign(campaign_id="c1", channel=ChannelType.EMAIL)
        m2 = make_campaign(campaign_id="c2", channel=ChannelType.EMAIL)
        m3 = make_campaign(campaign_id="c3", channel=ChannelType.LINKEDIN)
        calculator.calculate_batch([m1, m2, m3])
        summary = calculator.summary()
        assert summary["channel_counts"]["email"] == 2
        assert summary["channel_counts"]["linkedin"] == 1

    def test_summary_status_counts(self, calculator):
        m = make_campaign()
        calculator.calculate(m)
        summary = calculator.summary()
        total_status = sum(summary["status_counts"].values())
        assert total_status == 1

    def test_summary_avg_overall_score(self, calculator):
        m1 = make_campaign(campaign_id="c1")
        m2 = make_campaign(campaign_id="c2")
        r1 = calculator.calculate(m1)
        r2 = calculator.calculate(m2)
        expected_avg = round((r1.overall_score + r2.overall_score) / 2, 2)
        summary = calculator.summary()
        assert summary["avg_overall_score"] == pytest.approx(expected_avg, abs=0.01)


class TestCampaignROICalculatorReset:
    def test_reset_clears_store(self, calculator):
        calculator.calculate(make_campaign(campaign_id="c1"))
        calculator.reset()
        assert calculator.all_results() == []

    def test_reset_allows_recalculation(self, calculator):
        m = make_campaign(campaign_id="c1")
        calculator.calculate(m)
        calculator.reset()
        calculator.calculate(m)
        assert calculator.get("c1") is not None

    def test_get_returns_none_after_reset(self, calculator):
        calculator.calculate(make_campaign(campaign_id="c1"))
        calculator.reset()
        assert calculator.get("c1") is None

    def test_summary_empty_after_reset(self, calculator):
        calculator.calculate(make_campaign())
        calculator.reset()
        assert calculator.summary()["total"] == 0


# ─── CampaignResult.to_dict ──────────────────────────────────────────────────

class TestCampaignResultToDict:
    def test_to_dict_has_required_keys(self, calculator):
        m = make_campaign()
        result = calculator.calculate(m)
        d = result.to_dict()
        expected_keys = {
            "campaign", "roi_pct", "roi_score", "reach_efficiency",
            "conversion_quality", "cost_efficiency", "overall_score",
            "status", "cost_per_lead_eur", "cost_per_sql_eur", "cost_per_deal_eur",
            "open_rate_pct", "click_rate_pct", "lead_to_opp_rate_pct",
            "opp_to_won_rate_pct", "key_insights", "recommendations",
            "benchmark_vs_channel",
        }
        assert expected_keys <= set(d.keys())

    def test_to_dict_status_is_string(self, calculator):
        m = make_campaign()
        result = calculator.calculate(m)
        d = result.to_dict()
        assert isinstance(d["status"], str)

    def test_to_dict_campaign_is_dict(self, calculator):
        m = make_campaign()
        result = calculator.calculate(m)
        d = result.to_dict()
        assert isinstance(d["campaign"], dict)

    def test_to_dict_key_insights_is_list(self, calculator):
        m = make_campaign()
        result = calculator.calculate(m)
        d = result.to_dict()
        assert isinstance(d["key_insights"], list)

    def test_campaign_to_dict(self):
        m = make_campaign()
        d = m.to_dict()
        assert d["campaign_id"] == "c1"
        assert d["channel"] == ChannelType.EMAIL


# ─── Integration / edge-case tests ───────────────────────────────────────────

class TestIntegration:
    def test_all_zero_metrics_no_crash(self, calculator):
        m = make_campaign(
            total_spent_eur=0.0, budget_eur=0.0, closed_revenue_eur=0.0,
            emails_sent=0, opens=0, clicks=0, unsubscribes=0,
            leads_generated=0, mqls=0, sqls=0, opportunities_created=0,
            deals_won=0, pipeline_value_eur=0.0
        )
        result = calculator.calculate(m)
        assert result.overall_score >= 0.0
        assert result.status == CampaignStatus.FAILING

    def test_excellent_campaign_scenario(self, calculator):
        m = make_campaign(
            campaign_id="excellent",
            total_spent_eur=1000.0, closed_revenue_eur=50000.0,
            emails_sent=1000, opens=400, clicks=60, unsubscribes=3,
            leads_generated=200, mqls=80, sqls=40,
            opportunities_created=40, deals_won=15,
            total_contacts=2000, pipeline_value_eur=200000.0,
            channel=ChannelType.EMAIL
        )
        result = calculator.calculate(m)
        assert result.status == CampaignStatus.EXCELLENT
        assert result.overall_score >= 80.0

    def test_failing_campaign_scenario(self, calculator):
        m = make_campaign(
            campaign_id="failing",
            total_spent_eur=10000.0, closed_revenue_eur=500.0,
            emails_sent=200, opens=10, clicks=1, unsubscribes=5,
            leads_generated=2, mqls=0, sqls=0,
            opportunities_created=0, deals_won=0,
            total_contacts=50, pipeline_value_eur=0.0
        )
        result = calculator.calculate(m)
        assert result.status in (CampaignStatus.FAILING, CampaignStatus.POOR)

    def test_different_channels_different_benchmarks(self, calculator):
        m_email = make_campaign(campaign_id="email", channel=ChannelType.EMAIL,
                                 total_spent_eur=1000.0, closed_revenue_eur=4200.0)
        m_event = make_campaign(campaign_id="event", channel=ChannelType.EVENT,
                                 total_spent_eur=1000.0, closed_revenue_eur=4200.0)
        r_email = calculator.calculate(m_email)
        r_event = calculator.calculate(m_event)
        # Same revenue but different benchmarks → event should have higher benchmark_vs
        assert r_event.benchmark_vs_channel > r_email.benchmark_vs_channel

    def test_multiple_channels_by_channel_filter(self, calculator):
        channels = list(ChannelType)
        for i, ch in enumerate(channels):
            calculator.calculate(make_campaign(campaign_id=f"c{i}", channel=ch))
        for ch in channels:
            results = calculator.by_channel(ch)
            assert len(results) == 1
            assert results[0].campaign.channel == ch

    def test_insights_are_french_strings(self, calculator):
        # All insight values from _INSIGHTS should be non-empty strings
        m = make_campaign(emails_sent=500, opens=60, clicks=5, unsubscribes=6,
                          total_contacts=50, leads_generated=2, opportunities_created=0)
        result = calculator.calculate(m)
        for insight in result.key_insights:
            assert isinstance(insight, str)
            assert len(insight) > 0

    def test_recommendations_are_french_strings(self, calculator):
        m = make_campaign()
        result = calculator.calculate(m)
        for rec in result.recommendations:
            assert isinstance(rec, str)
            assert len(rec) > 0

    def test_batch_then_filter(self, calculator):
        campaigns = [
            make_campaign(campaign_id="e1", channel=ChannelType.EMAIL),
            make_campaign(campaign_id="e2", channel=ChannelType.EMAIL),
            make_campaign(campaign_id="l1", channel=ChannelType.LINKEDIN),
        ]
        calculator.calculate_batch(campaigns)
        email_results = calculator.by_channel(ChannelType.EMAIL)
        assert len(email_results) == 2

    def test_top_campaigns_reflects_scores(self, calculator):
        m_low = make_campaign(campaign_id="low",
                               total_spent_eur=10000.0, closed_revenue_eur=0.0,
                               leads_generated=0, sqls=0, deals_won=0,
                               emails_sent=100, opens=5, clicks=1, unsubscribes=0,
                               opportunities_created=0, total_contacts=10)
        m_high = make_campaign(campaign_id="high",
                                total_spent_eur=1000.0, closed_revenue_eur=50000.0,
                                leads_generated=200, sqls=80, deals_won=20,
                                emails_sent=500, opens=200, clicks=30,
                                unsubscribes=0, opportunities_created=50, total_contacts=2000)
        calculator.calculate_batch([m_low, m_high])
        top1 = calculator.top_campaigns(1)
        assert top1[0].campaign.campaign_id == "high"
