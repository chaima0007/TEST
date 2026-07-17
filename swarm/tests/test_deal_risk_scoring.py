"""Tests for DealRiskScoringEngine"""
import pytest
from dataclasses import fields as dc_fields
from intelligence.deal_risk_scoring_engine import (
    DealRiskScoringEngine, DealRiskInput, DealRiskResult,
    DealRisk, DealRiskPattern, DealRiskSeverity, DealRiskAction,
)


@pytest.fixture
def engine():
    return DealRiskScoringEngine()


@pytest.fixture
def healthy_deal():
    return DealRiskInput(
        deal_value=60000.0, deal_stage=3,
        days_in_current_stage=10.0, avg_days_in_stage_benchmark=15.0,
        days_since_last_contact=3.0, last_contact_was_outbound=False,
        competitor_mentioned=False, num_competitors_mentioned=0,
        budget_confirmed=True, budget_at_risk=False,
        champion_active=True, champion_seniority=3,
        executive_engaged=True, close_date_slipped_count=0,
        close_date_days_remaining=30.0, mutual_close_plan=True,
        next_step_defined=True, stakeholder_count=4,
        last_meeting_outcome="positive", multi_threaded=True,
        internal_priority_score=85.0, days_in_pipeline_total=40.0,
    )


@pytest.fixture
def ghost_deal():
    return DealRiskInput(
        deal_value=50000.0, deal_stage=3,
        days_in_current_stage=30.0, avg_days_in_stage_benchmark=15.0,
        days_since_last_contact=20.0, last_contact_was_outbound=True,
        competitor_mentioned=False, num_competitors_mentioned=0,
        budget_confirmed=True, budget_at_risk=False,
        champion_active=True, champion_seniority=2,
        executive_engaged=False, close_date_slipped_count=2,
        close_date_days_remaining=5.0, mutual_close_plan=False,
        next_step_defined=False, stakeholder_count=1,
        last_meeting_outcome="neutral", multi_threaded=False,
        internal_priority_score=40.0, days_in_pipeline_total=90.0,
    )


class TestResultStructure:
    def test_result_has_15_fields(self):
        assert len(dc_fields(DealRiskResult)) == 15

    def test_to_dict_has_15_keys(self, engine, healthy_deal):
        assert len(engine.assess(healthy_deal).to_dict()) == 15

    def test_to_dict_keys(self, engine, healthy_deal):
        d = engine.assess(healthy_deal).to_dict()
        expected = {
            "composite_score", "risk", "pattern", "severity", "action",
            "engagement_score", "relationship_strength_score",
            "process_health_score", "competitive_exposure_score",
            "slip_probability_pct", "ghost_probability_pct",
            "days_overdue_in_stage", "signal", "recommended_next_step",
            "revenue_at_risk",
        }
        assert set(d.keys()) == expected


class TestHealthyDeal:
    def test_healthy_low_risk(self, engine, healthy_deal):
        r = engine.assess(healthy_deal)
        assert r.risk == DealRisk.low

    def test_healthy_healthy_severity(self, engine, healthy_deal):
        r = engine.assess(healthy_deal)
        assert r.severity == DealRiskSeverity.healthy

    def test_healthy_no_pattern(self, engine, healthy_deal):
        r = engine.assess(healthy_deal)
        assert r.pattern == DealRiskPattern.none

    def test_healthy_action_maintain(self, engine, healthy_deal):
        r = engine.assess(healthy_deal)
        assert r.action == DealRiskAction.maintain

    def test_healthy_no_overdue(self, engine, healthy_deal):
        r = engine.assess(healthy_deal)
        assert r.days_overdue_in_stage == 0.0

    def test_healthy_signal_contains_healthy(self, engine, healthy_deal):
        r = engine.assess(healthy_deal)
        assert "healthy" in r.signal.lower()


class TestGhostDeal:
    def test_ghost_high_or_critical_risk(self, engine, ghost_deal):
        r = engine.assess(ghost_deal)
        assert r.risk in (DealRisk.high, DealRisk.critical)

    def test_ghost_pattern_detected(self, engine, ghost_deal):
        r = engine.assess(ghost_deal)
        assert r.pattern == DealRiskPattern.ghost_risk

    def test_ghost_action_re_engage(self, engine, ghost_deal):
        r = engine.assess(ghost_deal)
        assert r.action == DealRiskAction.re_engage

    def test_ghost_probability_elevated(self, engine, ghost_deal):
        r = engine.assess(ghost_deal)
        assert r.ghost_probability_pct > 30

    def test_ghost_overdue_in_stage(self, engine, ghost_deal):
        r = engine.assess(ghost_deal)
        assert r.days_overdue_in_stage > 0


class TestScoreBoundaries:
    def test_composite_bounded(self, engine):
        for inp in [DealRiskInput(), DealRiskInput(deal_value=0.0),
                    DealRiskInput(days_since_last_contact=60.0)]:
            r = engine.assess(inp)
            assert 0 <= r.composite_score <= 100

    def test_sub_scores_bounded(self, engine, healthy_deal):
        r = engine.assess(healthy_deal)
        for s in [r.engagement_score, r.relationship_strength_score,
                  r.process_health_score, r.competitive_exposure_score]:
            assert 0 <= s <= 100

    def test_probabilities_bounded(self, engine, ghost_deal):
        r = engine.assess(ghost_deal)
        assert 0 <= r.slip_probability_pct <= 100
        assert 0 <= r.ghost_probability_pct <= 100


class TestPatternDetection:
    def test_competitive_loss_risk_detected(self, engine):
        inp = DealRiskInput(
            competitor_mentioned=True, num_competitors_mentioned=3,
            days_since_last_contact=5.0, last_contact_was_outbound=False,
            close_date_slipped_count=0,
        )
        r = engine.assess(inp)
        assert r.pattern == DealRiskPattern.competitive_loss_risk

    def test_budget_freeze_detected(self, engine):
        inp = DealRiskInput(
            budget_confirmed=False, budget_at_risk=True,
            days_since_last_contact=5.0, last_contact_was_outbound=False,
            competitor_mentioned=False,
        )
        r = engine.assess(inp)
        assert r.pattern == DealRiskPattern.budget_freeze_risk

    def test_champion_attrition_detected(self, engine):
        inp = DealRiskInput(
            champion_active=False,
            days_since_last_contact=5.0, last_contact_was_outbound=False,
            competitor_mentioned=False, budget_confirmed=True,
        )
        r = engine.assess(inp)
        assert r.pattern == DealRiskPattern.champion_attrition_risk

    def test_slip_risk_detected(self, engine):
        inp = DealRiskInput(
            close_date_slipped_count=3,
            days_since_last_contact=3.0, last_contact_was_outbound=False,
            competitor_mentioned=False, budget_confirmed=True,
            champion_active=True,
        )
        r = engine.assess(inp)
        assert r.pattern == DealRiskPattern.slip_risk


class TestRevenueAtRisk:
    def test_healthy_revenue_at_risk_low(self, engine, healthy_deal):
        r = engine.assess(healthy_deal)
        assert r.revenue_at_risk < healthy_deal.deal_value * 0.4

    def test_ghost_revenue_at_risk_high(self, engine, ghost_deal):
        r = engine.assess(ghost_deal)
        assert r.revenue_at_risk > ghost_deal.deal_value * 0.4


class TestBatchSummary:
    def test_batch_length(self, engine, healthy_deal, ghost_deal):
        assert len(engine.batch([healthy_deal, ghost_deal])) == 2

    def test_summary_13_keys(self, engine, healthy_deal, ghost_deal):
        results = engine.batch([healthy_deal, ghost_deal])
        assert len(engine.summary(results)) == 13

    def test_summary_empty(self, engine):
        assert engine.summary([]) == {}

    def test_summary_total_deals(self, engine, healthy_deal, ghost_deal):
        results = engine.batch([healthy_deal, ghost_deal])
        assert engine.summary(results)["total_deals"] == 2

    def test_recommended_next_step_non_empty(self, engine, ghost_deal):
        r = engine.assess(ghost_deal)
        assert len(r.recommended_next_step) > 10
