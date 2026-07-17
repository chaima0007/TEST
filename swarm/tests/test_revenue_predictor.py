"""
Comprehensive tests for swarm/intelligence/revenue_predictor.py

Covers:
  - Enum values (RevenuePeriod, ConfidenceLevel)
  - Factor helpers: _lead_factor, _churn_factor, _stage_factor
  - adjusted_probability composition and clamping
  - Confidence level classification (all boundaries)
  - Risk factors (each trigger condition)
  - Upside factors (each trigger condition)
  - weighted_value_eur = deal_value * adjusted_prob
  - forecast_period filtering by expected_close_days
  - PeriodForecast: conservative/optimistic multipliers
  - by_stage and by_sector aggregation
  - RevenuePredictor CRUD methods
  - predict / predict_batch / get / all_predictions
  - top_opportunities / at_risk_deals / by_confidence
  - summary() with zero and non-zero predictions
  - reset()
  - to_dict() on RevenuePrediction and PeriodForecast
"""

import pytest
from swarm.intelligence.revenue_predictor import (
    RevenuePeriod,
    ConfidenceLevel,
    DealSignals,
    RevenuePrediction,
    PeriodForecast,
    RevenuePredictor,
    _lead_factor,
    _churn_factor,
    _stage_factor,
    _adjusted_probability,
    _confidence,
    _risk_factors,
    _upside_factors,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_deal(
    deal_id="D1",
    name="Test Deal",
    company="Acme",
    sector="Tech",
    stage="negotiation",
    deal_value_eur=10_000.0,
    probability=0.80,
    expected_close_days=30,
    lead_score=80.0,
    churn_risk_score=10.0,
    months_in_pipeline=2,
) -> DealSignals:
    return DealSignals(
        deal_id=deal_id,
        name=name,
        company=company,
        sector=sector,
        stage=stage,
        deal_value_eur=deal_value_eur,
        probability=probability,
        expected_close_days=expected_close_days,
        lead_score=lead_score,
        churn_risk_score=churn_risk_score,
        months_in_pipeline=months_in_pipeline,
    )


@pytest.fixture
def predictor():
    return RevenuePredictor()


@pytest.fixture
def clean_deal():
    """A deal with no risk factors and several upside factors."""
    return make_deal()


# ===========================================================================
# 1. Enum values
# ===========================================================================

class TestRevenuePeriodEnum:
    def test_monthly_value(self):
        assert RevenuePeriod.MONTHLY.value == "monthly"

    def test_quarterly_value(self):
        assert RevenuePeriod.QUARTERLY.value == "quarterly"

    def test_annual_value(self):
        assert RevenuePeriod.ANNUAL.value == "annual"

    def test_period_count(self):
        assert len(RevenuePeriod) == 3

    def test_period_is_string_enum(self):
        assert isinstance(RevenuePeriod.MONTHLY, str)


class TestConfidenceLevelEnum:
    def test_low_value(self):
        assert ConfidenceLevel.LOW.value == "low"

    def test_medium_value(self):
        assert ConfidenceLevel.MEDIUM.value == "medium"

    def test_high_value(self):
        assert ConfidenceLevel.HIGH.value == "high"

    def test_very_high_value(self):
        assert ConfidenceLevel.VERY_HIGH.value == "very_high"

    def test_confidence_count(self):
        assert len(ConfidenceLevel) == 4

    def test_confidence_is_string_enum(self):
        assert isinstance(ConfidenceLevel.HIGH, str)


# ===========================================================================
# 2. Factor helpers – boundary values
# ===========================================================================

class TestLeadFactor:
    def test_zero_lead_score(self):
        assert _lead_factor(0) == pytest.approx(0.50)

    def test_full_lead_score(self):
        assert _lead_factor(100) == pytest.approx(1.00)

    def test_mid_lead_score(self):
        # 0.50 + (50/100)*0.50 = 0.75
        assert _lead_factor(50) == pytest.approx(0.75)

    def test_lead_score_clamped_below(self):
        assert _lead_factor(-10) == pytest.approx(0.50)

    def test_lead_score_clamped_above(self):
        assert _lead_factor(150) == pytest.approx(1.00)

    def test_lead_score_75(self):
        # 0.50 + (75/100)*0.50 = 0.875
        assert _lead_factor(75) == pytest.approx(0.875)


class TestChurnFactor:
    def test_zero_churn(self):
        assert _churn_factor(0) == pytest.approx(1.00)

    def test_max_churn(self):
        assert _churn_factor(100) == pytest.approx(0.50)

    def test_mid_churn(self):
        # 1.0 - 50/200 = 0.75
        assert _churn_factor(50) == pytest.approx(0.75)

    def test_churn_clamped_below(self):
        assert _churn_factor(-20) == pytest.approx(1.00)

    def test_churn_clamped_above(self):
        assert _churn_factor(200) == pytest.approx(0.50)

    def test_churn_25(self):
        # 1.0 - 25/200 = 0.875
        assert _churn_factor(25) == pytest.approx(0.875)


class TestStageFactor:
    def test_prospecting(self):
        assert _stage_factor("prospecting") == pytest.approx(0.70)

    def test_qualified(self):
        assert _stage_factor("qualified") == pytest.approx(0.85)

    def test_proposal(self):
        assert _stage_factor("proposal") == pytest.approx(0.95)

    def test_negotiation(self):
        assert _stage_factor("negotiation") == pytest.approx(1.00)

    def test_closing(self):
        assert _stage_factor("closing") == pytest.approx(1.05)

    def test_unknown_stage_default(self):
        # Unknown stage → default 0.80
        assert _stage_factor("unknown") == pytest.approx(0.80)

    def test_stage_case_insensitive(self):
        assert _stage_factor("CLOSING") == pytest.approx(1.05)
        assert _stage_factor("Negotiation") == pytest.approx(1.00)


# ===========================================================================
# 3. adjusted_probability – composition and clamping
# ===========================================================================

class TestAdjustedProbability:
    def test_basic_combination(self):
        deal = make_deal(probability=0.80, lead_score=80, churn_risk_score=10, stage="negotiation")
        lf = _lead_factor(80)     # 0.90
        cf = _churn_factor(10)    # 0.95
        sf = _stage_factor("negotiation")  # 1.00
        expected = round(min(1.0, 0.80 * lf * cf * sf), 4)
        assert _adjusted_probability(deal) == pytest.approx(expected)

    def test_clamped_to_one(self):
        # All maximal factors: closing stage, lead=100, churn=0, prob=1.0
        deal = make_deal(probability=1.0, lead_score=100, churn_risk_score=0, stage="closing")
        adj = _adjusted_probability(deal)
        assert adj <= 1.0

    def test_clamped_to_zero(self):
        deal = make_deal(probability=0.0, lead_score=0, churn_risk_score=100, stage="prospecting")
        adj = _adjusted_probability(deal)
        assert adj >= 0.0

    def test_probability_zero_gives_zero(self):
        deal = make_deal(probability=0.0, lead_score=80, churn_risk_score=10, stage="closing")
        assert _adjusted_probability(deal) == pytest.approx(0.0)

    def test_prospecting_reduces_probability(self):
        deal_neg = make_deal(probability=0.50, lead_score=50, churn_risk_score=0, stage="negotiation")
        deal_pro = make_deal(probability=0.50, lead_score=50, churn_risk_score=0, stage="prospecting")
        assert _adjusted_probability(deal_pro) < _adjusted_probability(deal_neg)

    def test_high_churn_reduces_probability(self):
        deal_low = make_deal(probability=0.80, lead_score=80, churn_risk_score=10, stage="negotiation")
        deal_high = make_deal(probability=0.80, lead_score=80, churn_risk_score=90, stage="negotiation")
        assert _adjusted_probability(deal_high) < _adjusted_probability(deal_low)

    def test_result_is_rounded_to_4_decimals(self):
        deal = make_deal(probability=0.333, lead_score=33, churn_risk_score=33, stage="proposal")
        adj = _adjusted_probability(deal)
        assert adj == round(adj, 4)


# ===========================================================================
# 4. Confidence level classification – each boundary
# ===========================================================================

class TestConfidenceClassification:
    def test_very_high(self):
        # adj >= 0.70, late stage, lead >= 60
        conf = _confidence(0.70, "negotiation", 60)
        assert conf == ConfidenceLevel.VERY_HIGH

    def test_very_high_closing(self):
        conf = _confidence(0.75, "closing", 80)
        assert conf == ConfidenceLevel.VERY_HIGH

    def test_not_very_high_low_lead(self):
        # adj >= 0.70 and late stage but lead < 60 → HIGH
        conf = _confidence(0.75, "negotiation", 59)
        assert conf == ConfidenceLevel.HIGH

    def test_not_very_high_low_adj_prob(self):
        # adj < 0.70 even on late stage with high lead → HIGH
        conf = _confidence(0.65, "negotiation", 80)
        assert conf == ConfidenceLevel.HIGH

    def test_not_very_high_early_stage(self):
        # adj >= 0.70 but prospecting stage → not late stage → MEDIUM
        conf = _confidence(0.75, "prospecting", 80)
        assert conf == ConfidenceLevel.MEDIUM

    def test_high_on_proposal(self):
        conf = _confidence(0.55, "proposal", 50)
        assert conf == ConfidenceLevel.HIGH

    def test_high_on_negotiation_mid_adj(self):
        conf = _confidence(0.55, "negotiation", 40)
        assert conf == ConfidenceLevel.HIGH

    def test_not_high_early_stage_mid_adj(self):
        conf = _confidence(0.55, "qualified", 80)
        assert conf == ConfidenceLevel.MEDIUM

    def test_medium(self):
        conf = _confidence(0.30, "qualified", 20)
        assert conf == ConfidenceLevel.MEDIUM

    def test_medium_boundary(self):
        conf = _confidence(0.30, "prospecting", 10)
        assert conf == ConfidenceLevel.MEDIUM

    def test_low_below_medium_threshold(self):
        conf = _confidence(0.29, "prospecting", 10)
        assert conf == ConfidenceLevel.LOW

    def test_low_zero_prob(self):
        conf = _confidence(0.0, "prospecting", 0)
        assert conf == ConfidenceLevel.LOW


# ===========================================================================
# 5. Risk factors – each trigger condition
# ===========================================================================

class TestRiskFactors:
    def test_no_risk_factors_clean_deal(self):
        deal = make_deal(
            churn_risk_score=20, months_in_pipeline=2,
            lead_score=80, expected_close_days=30, probability=0.80
        )
        assert _risk_factors(deal) == []

    def test_high_churn_risk(self):
        deal = make_deal(churn_risk_score=61)
        risks = _risk_factors(deal)
        assert "Haut risque de churn client" in risks

    def test_churn_at_boundary_60_not_triggered(self):
        deal = make_deal(churn_risk_score=60)
        risks = _risk_factors(deal)
        assert "Haut risque de churn client" not in risks

    def test_long_pipeline(self):
        deal = make_deal(months_in_pipeline=7)
        risks = _risk_factors(deal)
        assert "Pipeline trop long (>6 mois)" in risks

    def test_pipeline_exactly_6_not_triggered(self):
        deal = make_deal(months_in_pipeline=6)
        risks = _risk_factors(deal)
        assert "Pipeline trop long (>6 mois)" not in risks

    def test_low_lead_score(self):
        deal = make_deal(lead_score=39)
        risks = _risk_factors(deal)
        assert "Score lead faible (<40)" in risks

    def test_lead_score_exactly_40_not_triggered(self):
        deal = make_deal(lead_score=40)
        risks = _risk_factors(deal)
        assert "Score lead faible (<40)" not in risks

    def test_high_close_days(self):
        deal = make_deal(expected_close_days=91)
        risks = _risk_factors(deal)
        assert "Délai de clôture élevé (>90 jours)" in risks

    def test_close_days_exactly_90_not_triggered(self):
        deal = make_deal(expected_close_days=90)
        risks = _risk_factors(deal)
        assert "Délai de clôture élevé (>90 jours)" not in risks

    def test_low_base_probability(self):
        deal = make_deal(probability=0.29)
        risks = _risk_factors(deal)
        assert "Probabilité de base insuffisante" in risks

    def test_probability_exactly_030_not_triggered(self):
        deal = make_deal(probability=0.30)
        risks = _risk_factors(deal)
        assert "Probabilité de base insuffisante" not in risks

    def test_multiple_risk_factors(self):
        deal = make_deal(
            churn_risk_score=70, months_in_pipeline=8,
            lead_score=30, expected_close_days=100, probability=0.10
        )
        risks = _risk_factors(deal)
        assert len(risks) == 5


# ===========================================================================
# 6. Upside factors – each trigger condition
# ===========================================================================

class TestUpsideFactors:
    def test_no_upside_factors_baseline(self):
        deal = make_deal(
            lead_score=50, churn_risk_score=50, stage="qualified",
            months_in_pipeline=5, deal_value_eur=10_000, probability=0.50
        )
        upsides = _upside_factors(deal)
        assert upsides == []

    def test_high_lead_score(self):
        deal = make_deal(lead_score=75)
        upsides = _upside_factors(deal)
        assert "Score lead élevé (≥75)" in upsides

    def test_lead_score_74_not_triggered(self):
        deal = make_deal(lead_score=74)
        upsides = _upside_factors(deal)
        assert "Score lead élevé (≥75)" not in upsides

    def test_low_churn_risk(self):
        deal = make_deal(churn_risk_score=25)
        upsides = _upside_factors(deal)
        assert "Faible risque de churn" in upsides

    def test_churn_26_not_triggered(self):
        deal = make_deal(churn_risk_score=26)
        upsides = _upside_factors(deal)
        assert "Faible risque de churn" not in upsides

    def test_fast_pipeline_negotiation(self):
        deal = make_deal(stage="negotiation", months_in_pipeline=3)
        upsides = _upside_factors(deal)
        assert "Progression pipeline rapide" in upsides

    def test_fast_pipeline_closing(self):
        deal = make_deal(stage="closing", months_in_pipeline=1)
        upsides = _upside_factors(deal)
        assert "Progression pipeline rapide" in upsides

    def test_fast_pipeline_not_late_stage(self):
        deal = make_deal(stage="proposal", months_in_pipeline=2)
        upsides = _upside_factors(deal)
        assert "Progression pipeline rapide" not in upsides

    def test_fast_pipeline_too_many_months(self):
        deal = make_deal(stage="negotiation", months_in_pipeline=4)
        upsides = _upside_factors(deal)
        assert "Progression pipeline rapide" not in upsides

    def test_high_value_opportunity(self):
        deal = make_deal(deal_value_eur=50_000)
        upsides = _upside_factors(deal)
        assert "Opportunité haute valeur (≥50k€)" in upsides

    def test_value_below_50k_not_triggered(self):
        deal = make_deal(deal_value_eur=49_999)
        upsides = _upside_factors(deal)
        assert "Opportunité haute valeur (≥50k€)" not in upsides

    def test_high_base_probability(self):
        deal = make_deal(probability=0.70)
        upsides = _upside_factors(deal)
        assert "Forte probabilité de base" in upsides

    def test_base_probability_069_not_triggered(self):
        deal = make_deal(probability=0.69)
        upsides = _upside_factors(deal)
        assert "Forte probabilité de base" not in upsides

    def test_all_upside_factors(self):
        deal = make_deal(
            lead_score=75, churn_risk_score=20, stage="closing",
            months_in_pipeline=2, deal_value_eur=60_000, probability=0.80
        )
        upsides = _upside_factors(deal)
        assert len(upsides) == 5


# ===========================================================================
# 7. weighted_value_eur = deal_value * adjusted_prob
# ===========================================================================

class TestWeightedValue:
    def test_weighted_value_calculation(self, predictor):
        deal = make_deal(deal_value_eur=20_000.0)
        pred = predictor.predict(deal)
        expected_weighted = round(deal.deal_value_eur * pred.adjusted_probability, 2)
        assert pred.weighted_value_eur == pytest.approx(expected_weighted)

    def test_weighted_value_zero_prob(self, predictor):
        deal = make_deal(probability=0.0, lead_score=0, churn_risk_score=100)
        pred = predictor.predict(deal)
        assert pred.weighted_value_eur == pytest.approx(0.0)

    def test_weighted_value_scales_with_deal_value(self, predictor):
        deal_small = make_deal(deal_id="D1", deal_value_eur=10_000)
        deal_large = make_deal(deal_id="D2", deal_value_eur=100_000)
        pred_small = predictor.predict(deal_small)
        pred_large = predictor.predict(deal_large)
        # Same factors, so ratio should be 10x
        ratio = pred_large.weighted_value_eur / pred_small.weighted_value_eur
        assert ratio == pytest.approx(10.0)


# ===========================================================================
# 8. forecast_period – filtering by expected_close_days
# ===========================================================================

class TestForecastPeriodFiltering:
    def test_monthly_limit_30_days(self, predictor):
        deals = [
            make_deal(deal_id="D1", expected_close_days=30),   # exactly 30 → included
            make_deal(deal_id="D2", expected_close_days=31),   # just over → excluded
            make_deal(deal_id="D3", expected_close_days=15),   # well within → included
        ]
        forecast = predictor.forecast_period(deals, RevenuePeriod.MONTHLY)
        included_ids = {p.deal.deal_id for p in forecast.predictions}
        assert "D1" in included_ids
        assert "D3" in included_ids
        assert "D2" not in included_ids

    def test_quarterly_limit_90_days(self, predictor):
        deals = [
            make_deal(deal_id="D1", expected_close_days=90),
            make_deal(deal_id="D2", expected_close_days=91),
        ]
        forecast = predictor.forecast_period(deals, RevenuePeriod.QUARTERLY)
        included_ids = {p.deal.deal_id for p in forecast.predictions}
        assert "D1" in included_ids
        assert "D2" not in included_ids

    def test_annual_limit_360_days(self, predictor):
        deals = [
            make_deal(deal_id="D1", expected_close_days=360),
            make_deal(deal_id="D2", expected_close_days=361),
        ]
        forecast = predictor.forecast_period(deals, RevenuePeriod.ANNUAL)
        included_ids = {p.deal.deal_id for p in forecast.predictions}
        assert "D1" in included_ids
        assert "D2" not in included_ids

    def test_empty_result_when_all_excluded(self, predictor):
        deals = [make_deal(deal_id="D1", expected_close_days=500)]
        forecast = predictor.forecast_period(deals, RevenuePeriod.MONTHLY)
        assert len(forecast.predictions) == 0
        assert forecast.expected_revenue_eur == pytest.approx(0.0)


# ===========================================================================
# 9. PeriodForecast: conservative = expected*0.75, optimistic = expected*1.25
# ===========================================================================

class TestPeriodForecastMultipliers:
    def test_conservative_is_75_percent(self, predictor):
        deals = [make_deal(deal_id="D1", expected_close_days=10)]
        forecast = predictor.forecast_period(deals, RevenuePeriod.MONTHLY)
        assert forecast.conservative_eur == pytest.approx(forecast.expected_revenue_eur * 0.75, rel=1e-4)

    def test_optimistic_is_125_percent(self, predictor):
        deals = [make_deal(deal_id="D1", expected_close_days=10)]
        forecast = predictor.forecast_period(deals, RevenuePeriod.MONTHLY)
        assert forecast.optimistic_eur == pytest.approx(forecast.expected_revenue_eur * 1.25, rel=1e-4)

    def test_empty_forecast_zeros(self, predictor):
        forecast = predictor.forecast_period([], RevenuePeriod.QUARTERLY)
        assert forecast.conservative_eur == pytest.approx(0.0)
        assert forecast.optimistic_eur == pytest.approx(0.0)
        assert forecast.expected_revenue_eur == pytest.approx(0.0)
        assert forecast.total_pipeline_eur == pytest.approx(0.0)

    def test_period_is_set_correctly(self, predictor):
        forecast = predictor.forecast_period([], RevenuePeriod.ANNUAL)
        assert forecast.period == RevenuePeriod.ANNUAL


# ===========================================================================
# 10. by_stage and by_sector aggregation in PeriodForecast
# ===========================================================================

class TestForecastAggregation:
    def test_by_stage_keys(self, predictor):
        deals = [
            make_deal(deal_id="D1", stage="proposal", expected_close_days=20),
            make_deal(deal_id="D2", stage="proposal", expected_close_days=20),
            make_deal(deal_id="D3", stage="negotiation", expected_close_days=20),
        ]
        forecast = predictor.forecast_period(deals, RevenuePeriod.MONTHLY)
        assert "proposal" in forecast.by_stage
        assert "negotiation" in forecast.by_stage

    def test_by_stage_count(self, predictor):
        deals = [
            make_deal(deal_id="D1", stage="closing", expected_close_days=10),
            make_deal(deal_id="D2", stage="closing", expected_close_days=10),
        ]
        forecast = predictor.forecast_period(deals, RevenuePeriod.MONTHLY)
        assert forecast.by_stage["closing"]["count"] == 2

    def test_by_stage_pipeline_eur(self, predictor):
        deals = [
            make_deal(deal_id="D1", stage="closing", deal_value_eur=10_000, expected_close_days=10),
            make_deal(deal_id="D2", stage="closing", deal_value_eur=20_000, expected_close_days=10),
        ]
        forecast = predictor.forecast_period(deals, RevenuePeriod.MONTHLY)
        assert forecast.by_stage["closing"]["pipeline_eur"] == pytest.approx(30_000.0)

    def test_by_sector_aggregation(self, predictor):
        deals = [
            make_deal(deal_id="D1", sector="SaaS", expected_close_days=10),
            make_deal(deal_id="D2", sector="SaaS", expected_close_days=10),
            make_deal(deal_id="D3", sector="Finance", expected_close_days=10),
        ]
        forecast = predictor.forecast_period(deals, RevenuePeriod.MONTHLY)
        assert "SaaS" in forecast.by_sector
        assert "Finance" in forecast.by_sector
        # SaaS should have 2x Finance's weighted value (same deal params)
        assert forecast.by_sector["SaaS"] == pytest.approx(2 * forecast.by_sector["Finance"], rel=1e-4)

    def test_confidence_distribution_keys(self, predictor):
        deals = [make_deal(deal_id="D1", expected_close_days=10)]
        forecast = predictor.forecast_period(deals, RevenuePeriod.MONTHLY)
        for level in ConfidenceLevel:
            assert level.value in forecast.confidence_distribution

    def test_confidence_distribution_sum(self, predictor):
        deals = [
            make_deal(deal_id="D1", expected_close_days=10),
            make_deal(deal_id="D2", expected_close_days=10),
        ]
        forecast = predictor.forecast_period(deals, RevenuePeriod.MONTHLY)
        total = sum(forecast.confidence_distribution.values())
        assert total == 2


# ===========================================================================
# 11 & 12. predict / predict_batch
# ===========================================================================

class TestPredictMethods:
    def test_predict_returns_revenue_prediction(self, predictor, clean_deal):
        result = predictor.predict(clean_deal)
        assert isinstance(result, RevenuePrediction)

    def test_predict_stores_result(self, predictor, clean_deal):
        predictor.predict(clean_deal)
        assert predictor.get(clean_deal.deal_id) is not None

    def test_predict_stores_correct_deal_id(self, predictor, clean_deal):
        pred = predictor.predict(clean_deal)
        assert pred.deal.deal_id == clean_deal.deal_id

    def test_predict_overwrites_on_same_id(self, predictor):
        deal_v1 = make_deal(deal_id="D1", deal_value_eur=1_000)
        deal_v2 = make_deal(deal_id="D1", deal_value_eur=99_000)
        predictor.predict(deal_v1)
        predictor.predict(deal_v2)
        assert predictor.get("D1").deal.deal_value_eur == 99_000

    def test_predict_batch_returns_all(self, predictor):
        deals = [make_deal(deal_id=f"D{i}") for i in range(5)]
        results = predictor.predict_batch(deals)
        assert len(results) == 5

    def test_predict_batch_stores_all(self, predictor):
        deals = [make_deal(deal_id=f"D{i}") for i in range(3)]
        predictor.predict_batch(deals)
        for d in deals:
            assert predictor.get(d.deal_id) is not None

    def test_predict_batch_returns_list_of_revenue_predictions(self, predictor):
        deals = [make_deal(deal_id="D1"), make_deal(deal_id="D2")]
        results = predictor.predict_batch(deals)
        assert all(isinstance(r, RevenuePrediction) for r in results)

    def test_get_nonexistent_returns_none(self, predictor):
        assert predictor.get("nonexistent") is None

    def test_all_predictions_sorted_descending(self, predictor):
        deals = [
            make_deal(deal_id="D1", deal_value_eur=5_000),
            make_deal(deal_id="D2", deal_value_eur=100_000),
            make_deal(deal_id="D3", deal_value_eur=20_000),
        ]
        predictor.predict_batch(deals)
        preds = predictor.all_predictions()
        values = [p.weighted_value_eur for p in preds]
        assert values == sorted(values, reverse=True)


# ===========================================================================
# 13. top_opportunities
# ===========================================================================

class TestTopOpportunities:
    def test_default_top_5(self, predictor):
        deals = [make_deal(deal_id=f"D{i}", deal_value_eur=float(i * 1000)) for i in range(1, 11)]
        predictor.predict_batch(deals)
        top = predictor.top_opportunities()
        assert len(top) == 5

    def test_top_n_respects_n(self, predictor):
        deals = [make_deal(deal_id=f"D{i}") for i in range(10)]
        predictor.predict_batch(deals)
        top = predictor.top_opportunities(3)
        assert len(top) == 3

    def test_top_opportunities_are_highest_weighted(self, predictor):
        deals = [
            make_deal(deal_id="D1", deal_value_eur=1_000),
            make_deal(deal_id="D2", deal_value_eur=50_000),
            make_deal(deal_id="D3", deal_value_eur=100_000),
        ]
        predictor.predict_batch(deals)
        top = predictor.top_opportunities(2)
        top_ids = {p.deal.deal_id for p in top}
        assert "D3" in top_ids
        assert "D2" in top_ids

    def test_top_n_larger_than_available(self, predictor):
        deals = [make_deal(deal_id="D1")]
        predictor.predict_batch(deals)
        top = predictor.top_opportunities(10)
        assert len(top) == 1


# ===========================================================================
# 14. at_risk_deals
# ===========================================================================

class TestAtRiskDeals:
    def test_returns_only_deals_with_risks(self, predictor):
        safe = make_deal(deal_id="SAFE", churn_risk_score=5, lead_score=80, probability=0.80,
                         months_in_pipeline=2, expected_close_days=30)
        risky = make_deal(deal_id="RISKY", churn_risk_score=90)
        predictor.predict_batch([safe, risky])
        at_risk = predictor.at_risk_deals()
        ids = {p.deal.deal_id for p in at_risk}
        assert "RISKY" in ids
        assert "SAFE" not in ids

    def test_no_risks_returns_empty(self, predictor):
        clean = make_deal(churn_risk_score=5, lead_score=80, probability=0.80,
                          months_in_pipeline=2, expected_close_days=30)
        predictor.predict(clean)
        assert predictor.at_risk_deals() == []


# ===========================================================================
# 15. by_confidence filter
# ===========================================================================

class TestByConfidence:
    def test_filters_by_low(self, predictor):
        low_deal = make_deal(deal_id="LOW", probability=0.05, lead_score=0,
                             churn_risk_score=100, stage="prospecting")
        predictor.predict(low_deal)
        lows = predictor.by_confidence(ConfidenceLevel.LOW)
        assert any(p.deal.deal_id == "LOW" for p in lows)

    def test_filters_by_very_high(self, predictor):
        vh_deal = make_deal(deal_id="VH", probability=0.90, lead_score=90,
                            churn_risk_score=0, stage="closing")
        predictor.predict(vh_deal)
        vhs = predictor.by_confidence(ConfidenceLevel.VERY_HIGH)
        assert any(p.deal.deal_id == "VH" for p in vhs)

    def test_only_matching_confidence_returned(self, predictor):
        vh_deal = make_deal(deal_id="VH", probability=0.90, lead_score=90,
                            churn_risk_score=0, stage="closing")
        low_deal = make_deal(deal_id="LOW", probability=0.05, lead_score=0,
                             churn_risk_score=100, stage="prospecting")
        predictor.predict_batch([vh_deal, low_deal])
        vhs = predictor.by_confidence(ConfidenceLevel.VERY_HIGH)
        assert all(p.confidence == ConfidenceLevel.VERY_HIGH for p in vhs)


# ===========================================================================
# 16 & 17. summary()
# ===========================================================================

class TestSummary:
    def test_summary_zero_deals(self, predictor):
        s = predictor.summary()
        assert s["total_deals"] == 0
        assert s["total_pipeline_eur"] == pytest.approx(0.0)
        assert s["expected_revenue_eur"] == pytest.approx(0.0)
        assert s["conservative_eur"] == pytest.approx(0.0)
        assert s["optimistic_eur"] == pytest.approx(0.0)
        assert s["avg_adjusted_probability"] == pytest.approx(0.0)
        assert s["at_risk_count"] == 0
        for level in ConfidenceLevel:
            assert s["confidence_distribution"][level.value] == 0

    def test_summary_total_deals(self, predictor):
        deals = [make_deal(deal_id=f"D{i}") for i in range(3)]
        predictor.predict_batch(deals)
        assert predictor.summary()["total_deals"] == 3

    def test_summary_total_pipeline(self, predictor):
        deals = [
            make_deal(deal_id="D1", deal_value_eur=10_000),
            make_deal(deal_id="D2", deal_value_eur=20_000),
        ]
        predictor.predict_batch(deals)
        assert predictor.summary()["total_pipeline_eur"] == pytest.approx(30_000.0)

    def test_summary_expected_revenue(self, predictor):
        deals = [make_deal(deal_id="D1"), make_deal(deal_id="D2")]
        preds = predictor.predict_batch(deals)
        expected = sum(p.weighted_value_eur for p in preds)
        assert predictor.summary()["expected_revenue_eur"] == pytest.approx(expected, rel=1e-4)

    def test_summary_conservative(self, predictor):
        predictor.predict(make_deal(deal_id="D1"))
        s = predictor.summary()
        assert s["conservative_eur"] == pytest.approx(s["expected_revenue_eur"] * 0.75, rel=1e-4)

    def test_summary_optimistic(self, predictor):
        predictor.predict(make_deal(deal_id="D1"))
        s = predictor.summary()
        assert s["optimistic_eur"] == pytest.approx(s["expected_revenue_eur"] * 1.25, rel=1e-4)

    def test_summary_avg_adjusted_probability(self, predictor):
        deals = [make_deal(deal_id=f"D{i}") for i in range(4)]
        preds = predictor.predict_batch(deals)
        expected_avg = sum(p.adjusted_probability for p in preds) / 4
        assert predictor.summary()["avg_adjusted_probability"] == pytest.approx(expected_avg, rel=1e-4)

    def test_summary_at_risk_count(self, predictor):
        risky = make_deal(deal_id="R1", churn_risk_score=90)
        clean = make_deal(deal_id="C1")
        predictor.predict_batch([risky, clean])
        s = predictor.summary()
        assert s["at_risk_count"] == 1

    def test_summary_confidence_distribution_sums_to_total(self, predictor):
        deals = [make_deal(deal_id=f"D{i}") for i in range(5)]
        predictor.predict_batch(deals)
        s = predictor.summary()
        dist_total = sum(s["confidence_distribution"].values())
        assert dist_total == 5


# ===========================================================================
# 18. reset()
# ===========================================================================

class TestReset:
    def test_reset_clears_predictions(self, predictor):
        predictor.predict(make_deal(deal_id="D1"))
        predictor.reset()
        assert predictor.get("D1") is None

    def test_reset_clears_all(self, predictor):
        deals = [make_deal(deal_id=f"D{i}") for i in range(5)]
        predictor.predict_batch(deals)
        predictor.reset()
        assert predictor.all_predictions() == []

    def test_reset_allows_fresh_start(self, predictor):
        predictor.predict(make_deal(deal_id="D1"))
        predictor.reset()
        predictor.predict(make_deal(deal_id="D2"))
        assert predictor.get("D1") is None
        assert predictor.get("D2") is not None

    def test_summary_after_reset_is_zero(self, predictor):
        predictor.predict(make_deal(deal_id="D1"))
        predictor.reset()
        s = predictor.summary()
        assert s["total_deals"] == 0


# ===========================================================================
# 19. to_dict() on RevenuePrediction and PeriodForecast
# ===========================================================================

class TestToDictMethods:
    def test_revenue_prediction_to_dict_keys(self, predictor, clean_deal):
        pred = predictor.predict(clean_deal)
        d = pred.to_dict()
        expected_keys = {
            "deal", "adjusted_probability", "weighted_value_eur",
            "confidence", "expected_close_date_offset_days",
            "risk_factors", "upside_factors",
        }
        assert set(d.keys()) == expected_keys

    def test_revenue_prediction_to_dict_confidence_is_string(self, predictor, clean_deal):
        pred = predictor.predict(clean_deal)
        d = pred.to_dict()
        assert isinstance(d["confidence"], str)

    def test_revenue_prediction_to_dict_deal_is_dict(self, predictor, clean_deal):
        pred = predictor.predict(clean_deal)
        d = pred.to_dict()
        assert isinstance(d["deal"], dict)

    def test_revenue_prediction_to_dict_values_match(self, predictor, clean_deal):
        pred = predictor.predict(clean_deal)
        d = pred.to_dict()
        assert d["adjusted_probability"] == pred.adjusted_probability
        assert d["weighted_value_eur"] == pred.weighted_value_eur
        assert d["confidence"] == pred.confidence.value
        assert d["risk_factors"] == pred.risk_factors
        assert d["upside_factors"] == pred.upside_factors

    def test_period_forecast_to_dict_keys(self, predictor):
        forecast = predictor.forecast_period(
            [make_deal(deal_id="D1", expected_close_days=10)],
            RevenuePeriod.MONTHLY,
        )
        d = forecast.to_dict()
        expected_keys = {
            "period", "predictions", "total_pipeline_eur",
            "expected_revenue_eur", "conservative_eur", "optimistic_eur",
            "by_stage", "by_sector", "confidence_distribution",
        }
        assert set(d.keys()) == expected_keys

    def test_period_forecast_to_dict_period_is_string(self, predictor):
        forecast = predictor.forecast_period([], RevenuePeriod.QUARTERLY)
        d = forecast.to_dict()
        assert d["period"] == "quarterly"

    def test_period_forecast_to_dict_predictions_are_dicts(self, predictor):
        forecast = predictor.forecast_period(
            [make_deal(deal_id="D1", expected_close_days=10)],
            RevenuePeriod.MONTHLY,
        )
        d = forecast.to_dict()
        assert all(isinstance(p, dict) for p in d["predictions"])

    def test_period_forecast_to_dict_values_match(self, predictor):
        deals = [make_deal(deal_id="D1", expected_close_days=10)]
        forecast = predictor.forecast_period(deals, RevenuePeriod.MONTHLY)
        d = forecast.to_dict()
        assert d["total_pipeline_eur"] == forecast.total_pipeline_eur
        assert d["expected_revenue_eur"] == forecast.expected_revenue_eur
        assert d["conservative_eur"] == forecast.conservative_eur
        assert d["optimistic_eur"] == forecast.optimistic_eur

    def test_deal_signals_to_dict(self, clean_deal):
        d = clean_deal.to_dict()
        assert d["deal_id"] == clean_deal.deal_id
        assert d["deal_value_eur"] == clean_deal.deal_value_eur
        assert d["stage"] == clean_deal.stage
