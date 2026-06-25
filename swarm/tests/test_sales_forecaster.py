"""Tests for SalesForecaster."""

import pytest
from intelligence.sales_forecaster import (
    SalesForecaster,
    Deal,
    PipelineStage,
    ForecastScenario,
    ForecastResult,
)


@pytest.fixture()
def fc():
    return SalesForecaster()


@pytest.fixture()
def fc_with_deals(fc):
    fc.add_deal(Deal("d1", "avocat", PipelineStage.PROPOSAL, 890))
    fc.add_deal(Deal("d2", "artisan", PipelineStage.NEGOTIATION, 340))
    fc.add_deal(Deal("d3", "pme", PipelineStage.QUALIFIED, 1200))
    fc.add_deal(Deal("d4", "médecin", PipelineStage.VERBAL_CLOSE, 650))
    fc.add_deal(Deal("d5", "restaurant", PipelineStage.CONTACTED, 480))
    return fc


# ── Deal ──────────────────────────────────────────────────────────────────────

class TestDeal:
    def test_close_probability_at_proposal(self):
        d = Deal("x", "pme", PipelineStage.PROPOSAL, 1000)
        assert abs(d.close_probability - 0.45) < 0.01

    def test_close_probability_at_closed_won(self):
        d = Deal("x", "pme", PipelineStage.CLOSED_WON, 1000)
        assert d.close_probability == 1.0

    def test_close_probability_at_prospected(self):
        d = Deal("x", "pme", PipelineStage.PROSPECTED, 1000)
        assert abs(d.close_probability - 0.05) < 0.01

    def test_stale_deal_has_lower_probability(self):
        fresh = Deal("a", "pme", PipelineStage.PROPOSAL, 1000, days_in_stage=0)
        stale = Deal("b", "pme", PipelineStage.PROPOSAL, 1000, days_in_stage=30)
        assert stale.close_probability < fresh.close_probability

    def test_probability_never_below_0_01(self):
        d = Deal("x", "pme", PipelineStage.PROSPECTED, 1000, days_in_stage=999)
        assert d.close_probability >= 0.01

    def test_probability_never_above_1(self):
        d = Deal("x", "pme", PipelineStage.CLOSED_WON, 1000, days_in_stage=0)
        assert d.close_probability <= 1.0

    def test_avocat_multiplier_above_1(self):
        d = Deal("x", "avocat", PipelineStage.PROPOSAL, 1000)
        assert d.sector_multiplier > 1.0

    def test_artisan_multiplier_below_1(self):
        d = Deal("x", "artisan", PipelineStage.PROPOSAL, 1000)
        assert d.sector_multiplier < 1.0

    def test_pme_multiplier_is_1(self):
        d = Deal("x", "pme", PipelineStage.PROPOSAL, 1000)
        assert d.sector_multiplier == 1.0

    def test_unknown_sector_defaults(self):
        d = Deal("x", "unknown_xyz", PipelineStage.PROPOSAL, 1000)
        assert d.sector_multiplier == 1.0

    def test_weighted_value_is_product(self):
        d = Deal("x", "pme", PipelineStage.PROPOSAL, 1000)
        expected = 1000 * d.close_probability * d.sector_multiplier
        assert abs(d.weighted_value - expected) < 0.01

    def test_to_dict_has_required_keys(self):
        d = Deal("d1", "pme", PipelineStage.PROPOSAL, 500)
        result = d.to_dict()
        for key in ["deal_id", "sector", "stage", "value_eur", "close_probability", "weighted_value"]:
            assert key in result


# ── SalesForecaster — pipeline management ─────────────────────────────────────

class TestPipelineManagement:
    def test_add_and_retrieve_deal(self, fc):
        deal = Deal("d1", "pme", PipelineStage.PROPOSAL, 500)
        fc.add_deal(deal)
        assert fc.get_deal("d1") is deal

    def test_all_deals_returns_list(self, fc_with_deals):
        assert len(fc_with_deals.all_deals()) == 5

    def test_update_stage(self, fc_with_deals):
        fc_with_deals.update_stage("d1", PipelineStage.NEGOTIATION)
        assert fc_with_deals.get_deal("d1").stage == PipelineStage.NEGOTIATION

    def test_remove_deal(self, fc_with_deals):
        fc_with_deals.remove_deal("d1")
        assert fc_with_deals.get_deal("d1") is None
        assert len(fc_with_deals.all_deals()) == 4

    def test_close_won_removes_from_pipeline(self, fc_with_deals):
        val = fc_with_deals.close_won("d1")
        assert val == 890
        assert fc_with_deals.get_deal("d1") is None

    def test_close_won_returns_none_for_unknown(self, fc):
        assert fc.close_won("nonexistent") is None

    def test_deals_by_stage(self, fc_with_deals):
        proposals = fc_with_deals.deals_by_stage(PipelineStage.PROPOSAL)
        assert all(d.stage == PipelineStage.PROPOSAL for d in proposals)

    def test_reset_clears_pipeline(self, fc_with_deals):
        fc_with_deals.reset()
        assert len(fc_with_deals.all_deals()) == 0


# ── SalesForecaster — forecasting ─────────────────────────────────────────────

class TestForecasting:
    def test_empty_pipeline_returns_zero(self, fc):
        r = fc.forecast()
        assert r.expected_revenue == 0.0
        assert r.deals_count == 0

    def test_returns_forecast_result(self, fc_with_deals):
        r = fc_with_deals.forecast()
        assert isinstance(r, ForecastResult)

    def test_base_scenario_positive(self, fc_with_deals):
        r = fc_with_deals.forecast(ForecastScenario.BASE)
        assert r.expected_revenue > 0

    def test_optimistic_greater_than_base(self, fc_with_deals):
        base = fc_with_deals.forecast(ForecastScenario.BASE)
        opt  = fc_with_deals.forecast(ForecastScenario.OPTIMISTIC)
        assert opt.expected_revenue > base.expected_revenue

    def test_pessimistic_less_than_base(self, fc_with_deals):
        base = fc_with_deals.forecast(ForecastScenario.BASE)
        pess = fc_with_deals.forecast(ForecastScenario.PESSIMISTIC)
        assert pess.expected_revenue < base.expected_revenue

    def test_pipeline_value_is_raw_sum(self, fc_with_deals):
        r = fc_with_deals.forecast()
        raw = sum(d.value_eur for d in fc_with_deals.all_deals())
        assert abs(r.pipeline_value - raw) < 0.01

    def test_by_stage_keys_are_stage_values(self, fc_with_deals):
        r = fc_with_deals.forecast()
        valid_stages = {s.value for s in PipelineStage}
        for k in r.by_stage:
            assert k in valid_stages

    def test_by_sector_populated(self, fc_with_deals):
        r = fc_with_deals.forecast()
        assert len(r.by_sector) > 0

    def test_confidence_between_0_and_1(self, fc_with_deals):
        r = fc_with_deals.forecast()
        assert 0.0 <= r.confidence <= 1.0

    def test_confidence_zero_for_empty(self, fc):
        r = fc.forecast()
        assert r.confidence == 0.0

    def test_rationale_is_nonempty_string(self, fc_with_deals):
        r = fc_with_deals.forecast()
        assert isinstance(r.rationale, str) and len(r.rationale) > 10

    def test_all_scenarios_returns_three(self, fc_with_deals):
        results = fc_with_deals.all_scenarios()
        assert len(results) == 3

    def test_all_scenarios_ordered_pess_base_opt(self, fc_with_deals):
        results = fc_with_deals.all_scenarios()
        revenues = [r.expected_revenue for r in results]
        assert revenues == sorted(revenues)

    def test_to_dict_has_required_keys(self, fc_with_deals):
        r = fc_with_deals.forecast()
        d = r.to_dict()
        for key in ["scenario", "expected_revenue", "deals_count", "pipeline_value", "confidence"]:
            assert key in d


# ── SalesForecaster — pipeline summary ────────────────────────────────────────

class TestPipelineSummary:
    def test_summary_keys(self, fc_with_deals):
        s = fc_with_deals.pipeline_summary()
        for key in ["total_deals", "pipeline_value_eur", "weighted_pipeline", "base_forecast", "confidence"]:
            assert key in s

    def test_total_deals_matches(self, fc_with_deals):
        s = fc_with_deals.pipeline_summary()
        assert s["total_deals"] == 5

    def test_top_deals_sorted_descending(self, fc_with_deals):
        top = fc_with_deals.top_deals(n=3)
        assert len(top) == 3
        vals = [d.weighted_value for d in top]
        assert vals == sorted(vals, reverse=True)

    def test_top_deals_respects_n(self, fc_with_deals):
        assert len(fc_with_deals.top_deals(n=2)) == 2

    def test_stale_deals_filter(self, fc):
        fc.add_deal(Deal("fresh", "pme", PipelineStage.PROPOSAL, 500, days_in_stage=3))
        fc.add_deal(Deal("stale", "pme", PipelineStage.PROPOSAL, 500, days_in_stage=20))
        assert len(fc.stale_deals(threshold_days=14)) == 1

    def test_closed_won_updates_history(self, fc_with_deals):
        fc_with_deals.close_won("d1")
        s = fc_with_deals.pipeline_summary()
        assert 890.0 in s["closed_won_history"]
