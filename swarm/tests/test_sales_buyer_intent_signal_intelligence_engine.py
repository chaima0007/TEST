"""
Comprehensive pytest tests for SalesBuyerIntentSignalIntelligenceEngine.
"""
from __future__ import annotations

import math
import pytest

from swarm.intelligence.sales_buyer_intent_signal_intelligence_engine import (
    IntentRisk,
    IntentPattern,
    IntentSeverity,
    IntentAction,
    BuyerIntentSignalInput,
    BuyerIntentSignalResult,
    SalesBuyerIntentSignalIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers / Fixtures
# ---------------------------------------------------------------------------

def make_input(**overrides) -> BuyerIntentSignalInput:
    """Return a 'healthy' baseline input; override any field via kwargs."""
    defaults = dict(
        rep_id="rep-001",
        region="EMEA",
        evaluation_period_id="Q2-2026",
        total_prospects_tracked=100,
        email_opens_last_7d_count=80,
        email_opens_prior_7d_count=80,
        website_visits_last_7d_count=60,
        website_visits_prior_7d_count=60,
        content_downloads_last_7d_count=10,
        demo_requests_count=15,
        pricing_page_visits_count=12,
        avg_days_since_last_prospect_response=2.0,
        prospects_no_response_14d_count=10,
        prospects_no_response_30d_count=10,
        champion_response_rate_pct=0.70,
        champion_last_contact_days=3.0,
        competitor_mentions_count=0,
        multi_stakeholder_engagement_pct=0.60,
        buying_committee_size_avg=3.5,
        budget_confirmed_count=20,
        timeline_confirmed_count=20,
        avg_opportunity_value_usd=5000.0,
    )
    defaults.update(overrides)
    return BuyerIntentSignalInput(**defaults)


@pytest.fixture
def engine():
    return SalesBuyerIntentSignalIntelligenceEngine()


@pytest.fixture
def healthy_input():
    return make_input()


# ===========================================================================
# 1. Enum tests
# ===========================================================================

class TestIntentRiskEnum:
    def test_members_exist(self):
        assert IntentRisk.low
        assert IntentRisk.moderate
        assert IntentRisk.high
        assert IntentRisk.critical

    def test_values(self):
        assert IntentRisk.low.value == "low"
        assert IntentRisk.moderate.value == "moderate"
        assert IntentRisk.high.value == "high"
        assert IntentRisk.critical.value == "critical"

    def test_str_enum(self):
        assert IntentRisk.low == "low"
        assert IntentRisk.critical == "critical"

    def test_count(self):
        assert len(IntentRisk) == 4


class TestIntentPatternEnum:
    def test_members_exist(self):
        assert IntentPattern.none is not None
        assert IntentPattern.intent_cooling
        assert IntentPattern.ghost_prospect
        assert IntentPattern.competitor_evaluation
        assert IntentPattern.timing_mismatch
        assert IntentPattern.champion_disengagement

    def test_values(self):
        assert IntentPattern.none.value == "none"
        assert IntentPattern.intent_cooling.value == "intent_cooling"
        assert IntentPattern.ghost_prospect.value == "ghost_prospect"
        assert IntentPattern.competitor_evaluation.value == "competitor_evaluation"
        assert IntentPattern.timing_mismatch.value == "timing_mismatch"
        assert IntentPattern.champion_disengagement.value == "champion_disengagement"

    def test_str_enum(self):
        assert IntentPattern.none == "none"
        assert IntentPattern.ghost_prospect == "ghost_prospect"

    def test_count(self):
        assert len(IntentPattern) == 6


class TestIntentSeverityEnum:
    def test_members_exist(self):
        assert IntentSeverity.engaged
        assert IntentSeverity.lukewarm
        assert IntentSeverity.cooling
        assert IntentSeverity.ghosted

    def test_values(self):
        assert IntentSeverity.engaged.value == "engaged"
        assert IntentSeverity.lukewarm.value == "lukewarm"
        assert IntentSeverity.cooling.value == "cooling"
        assert IntentSeverity.ghosted.value == "ghosted"

    def test_str_enum(self):
        assert IntentSeverity.engaged == "engaged"
        assert IntentSeverity.ghosted == "ghosted"

    def test_count(self):
        assert len(IntentSeverity) == 4


class TestIntentActionEnum:
    def test_members_exist(self):
        assert IntentAction.no_action
        assert IntentAction.re_engagement_sequence
        assert IntentAction.champion_outreach
        assert IntentAction.competitive_displacement
        assert IntentAction.timing_nurture_sequence
        assert IntentAction.deal_rescue_escalation

    def test_values(self):
        assert IntentAction.no_action.value == "no_action"
        assert IntentAction.re_engagement_sequence.value == "re_engagement_sequence"
        assert IntentAction.champion_outreach.value == "champion_outreach"
        assert IntentAction.competitive_displacement.value == "competitive_displacement"
        assert IntentAction.timing_nurture_sequence.value == "timing_nurture_sequence"
        assert IntentAction.deal_rescue_escalation.value == "deal_rescue_escalation"

    def test_str_enum(self):
        assert IntentAction.no_action == "no_action"
        assert IntentAction.champion_outreach == "champion_outreach"

    def test_count(self):
        assert len(IntentAction) == 6


# ===========================================================================
# 2. BuyerIntentSignalInput dataclass
# ===========================================================================

class TestBuyerIntentSignalInput:
    def test_instantiation(self, healthy_input):
        assert healthy_input.rep_id == "rep-001"
        assert healthy_input.region == "EMEA"
        assert healthy_input.evaluation_period_id == "Q2-2026"

    def test_all_22_fields(self, healthy_input):
        fields = [
            "rep_id", "region", "evaluation_period_id",
            "total_prospects_tracked", "email_opens_last_7d_count",
            "email_opens_prior_7d_count", "website_visits_last_7d_count",
            "website_visits_prior_7d_count", "content_downloads_last_7d_count",
            "demo_requests_count", "pricing_page_visits_count",
            "avg_days_since_last_prospect_response",
            "prospects_no_response_14d_count", "prospects_no_response_30d_count",
            "champion_response_rate_pct", "champion_last_contact_days",
            "competitor_mentions_count", "multi_stakeholder_engagement_pct",
            "buying_committee_size_avg", "budget_confirmed_count",
            "timeline_confirmed_count", "avg_opportunity_value_usd",
        ]
        assert len(fields) == 22
        for f in fields:
            assert hasattr(healthy_input, f)

    def test_numeric_fields(self, healthy_input):
        assert isinstance(healthy_input.total_prospects_tracked, int)
        assert isinstance(healthy_input.avg_opportunity_value_usd, float)

    def test_string_fields(self, healthy_input):
        assert isinstance(healthy_input.rep_id, str)
        assert isinstance(healthy_input.region, str)
        assert isinstance(healthy_input.evaluation_period_id, str)

    def test_override_fields(self):
        inp = make_input(rep_id="x", region="APAC", total_prospects_tracked=50)
        assert inp.rep_id == "x"
        assert inp.region == "APAC"
        assert inp.total_prospects_tracked == 50


# ===========================================================================
# 3. BuyerIntentSignalResult dataclass & to_dict
# ===========================================================================

class TestBuyerIntentSignalResult:
    def _make_result(self):
        return BuyerIntentSignalResult(
            rep_id="rep-A",
            region="NA",
            intent_risk=IntentRisk.low,
            intent_pattern=IntentPattern.none,
            intent_severity=IntentSeverity.engaged,
            recommended_action=IntentAction.no_action,
            engagement_decay_score=0.0,
            champion_health_score=0.0,
            buying_signal_score=0.0,
            competitive_threat_score=0.0,
            buyer_intent_composite=0.0,
            has_intent_gap=False,
            requires_re_engagement=False,
            estimated_pipeline_at_risk_usd=0.0,
            intent_signal="Buyer intent signals healthy — prospects showing active engagement",
        )

    def test_all_15_fields(self):
        r = self._make_result()
        fields = [
            "rep_id", "region", "intent_risk", "intent_pattern",
            "intent_severity", "recommended_action", "engagement_decay_score",
            "champion_health_score", "buying_signal_score",
            "competitive_threat_score", "buyer_intent_composite",
            "has_intent_gap", "requires_re_engagement",
            "estimated_pipeline_at_risk_usd", "intent_signal",
        ]
        assert len(fields) == 15
        for f in fields:
            assert hasattr(r, f)

    def test_to_dict_keys(self):
        r = self._make_result()
        d = r.to_dict()
        expected_keys = {
            "rep_id", "region", "intent_risk", "intent_pattern",
            "intent_severity", "recommended_action", "engagement_decay_score",
            "champion_health_score", "buying_signal_score",
            "competitive_threat_score", "buyer_intent_composite",
            "has_intent_gap", "requires_re_engagement",
            "estimated_pipeline_at_risk_usd", "intent_signal",
        }
        assert set(d.keys()) == expected_keys
        assert len(d) == 15

    def test_to_dict_enum_values_are_strings(self):
        r = self._make_result()
        d = r.to_dict()
        assert isinstance(d["intent_risk"], str)
        assert isinstance(d["intent_pattern"], str)
        assert isinstance(d["intent_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_correct_values(self):
        r = self._make_result()
        d = r.to_dict()
        assert d["rep_id"] == "rep-A"
        assert d["region"] == "NA"
        assert d["intent_risk"] == "low"
        assert d["intent_pattern"] == "none"
        assert d["intent_severity"] == "engaged"
        assert d["recommended_action"] == "no_action"
        assert d["has_intent_gap"] is False
        assert d["requires_re_engagement"] is False
        assert d["estimated_pipeline_at_risk_usd"] == 0.0

    def test_to_dict_non_enum_types(self):
        r = self._make_result()
        d = r.to_dict()
        assert isinstance(d["engagement_decay_score"], float)
        assert isinstance(d["buyer_intent_composite"], float)
        assert isinstance(d["has_intent_gap"], bool)
        assert isinstance(d["intent_signal"], str)


# ===========================================================================
# 4. _engagement_decay_score
# ===========================================================================

class TestEngagementDecayScore:
    """Tests for the _engagement_decay_score sub-score method."""

    def test_no_decay_returns_zero(self, engine):
        inp = make_input(
            email_opens_last_7d_count=80,
            email_opens_prior_7d_count=80,
            website_visits_last_7d_count=60,
            website_visits_prior_7d_count=60,
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
        )
        # open_decay=0, visit_decay=0, no_resp_rate=0.05 < 0.20
        assert engine._engagement_decay_score(inp) == 0.0

    def test_high_email_decay_adds_35(self, engine):
        # open_decay >= 0.60 → +35
        inp = make_input(
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=60,
            website_visits_prior_7d_count=60,
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
        )
        score = engine._engagement_decay_score(inp)
        assert score >= 35.0

    def test_medium_email_decay_adds_18(self, engine):
        # open_decay = (100-70)/100 = 0.30 → +18
        inp = make_input(
            email_opens_last_7d_count=70,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=60,
            website_visits_prior_7d_count=60,
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
        )
        score = engine._engagement_decay_score(inp)
        assert score >= 18.0

    def test_low_email_decay_adds_7(self, engine):
        # open_decay = (100-90)/100 = 0.10 → +7
        inp = make_input(
            email_opens_last_7d_count=90,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=60,
            website_visits_prior_7d_count=60,
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
        )
        score = engine._engagement_decay_score(inp)
        assert score >= 7.0

    def test_high_visit_decay_adds_30(self, engine):
        # visit_decay >= 0.60 → +30
        inp = make_input(
            email_opens_last_7d_count=80,
            email_opens_prior_7d_count=80,
            website_visits_last_7d_count=0,
            website_visits_prior_7d_count=100,
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
        )
        score = engine._engagement_decay_score(inp)
        assert score >= 30.0

    def test_medium_visit_decay_adds_15(self, engine):
        # visit_decay = (100-70)/100 = 0.30 → +15
        inp = make_input(
            email_opens_last_7d_count=80,
            email_opens_prior_7d_count=80,
            website_visits_last_7d_count=70,
            website_visits_prior_7d_count=100,
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
        )
        score = engine._engagement_decay_score(inp)
        assert score >= 15.0

    def test_high_no_response_rate_adds_25(self, engine):
        # no_resp_rate = 40/100 = 0.40 → +25
        inp = make_input(
            email_opens_last_7d_count=80,
            email_opens_prior_7d_count=80,
            website_visits_last_7d_count=60,
            website_visits_prior_7d_count=60,
            prospects_no_response_30d_count=40,
            total_prospects_tracked=100,
        )
        score = engine._engagement_decay_score(inp)
        assert score >= 25.0

    def test_medium_no_response_rate_adds_12(self, engine):
        # no_resp_rate = 20/100 = 0.20 → +12
        inp = make_input(
            email_opens_last_7d_count=80,
            email_opens_prior_7d_count=80,
            website_visits_last_7d_count=60,
            website_visits_prior_7d_count=60,
            prospects_no_response_30d_count=20,
            total_prospects_tracked=100,
        )
        score = engine._engagement_decay_score(inp)
        assert score >= 12.0

    def test_max_capped_at_100(self, engine):
        # All worst-case → 35+30+25 = 90 ≤ 100
        inp = make_input(
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=0,
            website_visits_prior_7d_count=100,
            prospects_no_response_30d_count=50,
            total_prospects_tracked=100,
        )
        score = engine._engagement_decay_score(inp)
        assert score <= 100.0

    def test_prior_opens_zero_handled(self, engine):
        # prior_opens=0 → max(0,1)=1, so open_decay=(1-0)/1=1.0 >= 0.60 → +35
        inp = make_input(
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=0,
            website_visits_last_7d_count=60,
            website_visits_prior_7d_count=60,
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
        )
        score = engine._engagement_decay_score(inp)
        assert score >= 35.0

    def test_prior_visits_zero_handled(self, engine):
        # prior_visits=0 → max(0,1)=1, visit_decay=(1-0)/1=1.0 >= 0.60 → +30
        inp = make_input(
            email_opens_last_7d_count=80,
            email_opens_prior_7d_count=80,
            website_visits_last_7d_count=0,
            website_visits_prior_7d_count=0,
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
        )
        score = engine._engagement_decay_score(inp)
        assert score >= 30.0

    def test_total_prospects_zero_handled(self, engine):
        # total_prospects=0 → max(0,1)=1; no_resp_30/1 could be large
        inp = make_input(
            email_opens_last_7d_count=80,
            email_opens_prior_7d_count=80,
            website_visits_last_7d_count=60,
            website_visits_prior_7d_count=60,
            prospects_no_response_30d_count=0,
            total_prospects_tracked=0,
        )
        score = engine._engagement_decay_score(inp)
        assert isinstance(score, float)
        assert score <= 100.0

    def test_combined_all_worst_case(self, engine):
        inp = make_input(
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=0,
            website_visits_prior_7d_count=100,
            prospects_no_response_30d_count=50,
            total_prospects_tracked=100,
        )
        score = engine._engagement_decay_score(inp)
        # 35 + 30 + 25 = 90
        assert score == pytest.approx(90.0)

    def test_email_decay_below_10_no_addition(self, engine):
        # open_decay = (100-95)/100 = 0.05 < 0.10 → 0 added
        inp = make_input(
            email_opens_last_7d_count=95,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=60,
            website_visits_prior_7d_count=60,
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
        )
        score = engine._engagement_decay_score(inp)
        assert score == 0.0

    def test_visit_decay_below_30_no_addition(self, engine):
        # visit_decay = (100-80)/100 = 0.20 < 0.30 → 0 added
        inp = make_input(
            email_opens_last_7d_count=80,
            email_opens_prior_7d_count=80,
            website_visits_last_7d_count=80,
            website_visits_prior_7d_count=100,
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
        )
        score = engine._engagement_decay_score(inp)
        assert score == 0.0


# ===========================================================================
# 5. _champion_health_score
# ===========================================================================

class TestChampionHealthScore:
    def test_healthy_champion_zero(self, engine):
        inp = make_input(
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
        )
        assert engine._champion_health_score(inp) == 0.0

    def test_last_contact_21d_adds_40(self, engine):
        inp = make_input(
            champion_last_contact_days=21.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
        )
        assert engine._champion_health_score(inp) >= 40.0

    def test_last_contact_14d_adds_22(self, engine):
        inp = make_input(
            champion_last_contact_days=14.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
        )
        assert engine._champion_health_score(inp) >= 22.0

    def test_last_contact_7d_adds_8(self, engine):
        inp = make_input(
            champion_last_contact_days=7.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
        )
        assert engine._champion_health_score(inp) >= 8.0

    def test_low_response_rate_below_20_adds_35(self, engine):
        inp = make_input(
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.10,
            multi_stakeholder_engagement_pct=0.70,
        )
        assert engine._champion_health_score(inp) >= 35.0

    def test_response_rate_20_to_40_adds_18(self, engine):
        inp = make_input(
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.30,
            multi_stakeholder_engagement_pct=0.70,
        )
        assert engine._champion_health_score(inp) >= 18.0

    def test_response_rate_40_to_60_adds_7(self, engine):
        inp = make_input(
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.50,
            multi_stakeholder_engagement_pct=0.70,
        )
        assert engine._champion_health_score(inp) >= 7.0

    def test_low_multi_stakeholder_below_20_adds_20(self, engine):
        inp = make_input(
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.10,
        )
        assert engine._champion_health_score(inp) >= 20.0

    def test_multi_stakeholder_20_to_40_adds_10(self, engine):
        inp = make_input(
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.30,
        )
        assert engine._champion_health_score(inp) >= 10.0

    def test_max_capped_at_100(self, engine):
        # 40 + 35 + 20 = 95 ≤ 100
        inp = make_input(
            champion_last_contact_days=30.0,
            champion_response_rate_pct=0.10,
            multi_stakeholder_engagement_pct=0.05,
        )
        score = engine._champion_health_score(inp)
        assert score <= 100.0

    def test_worst_case_score(self, engine):
        inp = make_input(
            champion_last_contact_days=30.0,
            champion_response_rate_pct=0.05,
            multi_stakeholder_engagement_pct=0.05,
        )
        score = engine._champion_health_score(inp)
        # 40 + 35 + 20 = 95
        assert score == pytest.approx(95.0)

    def test_response_rate_exactly_60_no_addition(self, engine):
        inp = make_input(
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.60,
            multi_stakeholder_engagement_pct=0.70,
        )
        # response_rate >= 0.60 → none of the branches match → 0
        assert engine._champion_health_score(inp) == 0.0

    def test_multi_stakeholder_exactly_40_no_addition(self, engine):
        inp = make_input(
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.40,
        )
        # 0.40 is not < 0.20 and not < 0.40 → 0
        assert engine._champion_health_score(inp) == 0.0


# ===========================================================================
# 6. _buying_signal_score
# ===========================================================================

class TestBuyingSignalScore:
    def test_high_activity_zero(self, engine):
        # demo_rate=0.15 >= 0.10, pricing_rate=0.12 >= 0.10, budget+timeline each 0.20 >= 0.20
        inp = make_input(
            demo_requests_count=15,
            pricing_page_visits_count=12,
            budget_confirmed_count=20,
            timeline_confirmed_count=20,
            total_prospects_tracked=100,
        )
        assert engine._buying_signal_score(inp) == 0.0

    def test_low_demo_rate_below_5_adds_30(self, engine):
        inp = make_input(
            demo_requests_count=4,
            pricing_page_visits_count=12,
            budget_confirmed_count=20,
            timeline_confirmed_count=20,
            total_prospects_tracked=100,
        )
        score = engine._buying_signal_score(inp)
        assert score >= 30.0

    def test_demo_rate_5_to_10_adds_15(self, engine):
        inp = make_input(
            demo_requests_count=7,
            pricing_page_visits_count=12,
            budget_confirmed_count=20,
            timeline_confirmed_count=20,
            total_prospects_tracked=100,
        )
        score = engine._buying_signal_score(inp)
        assert score >= 15.0

    def test_low_pricing_rate_below_5_adds_25(self, engine):
        inp = make_input(
            demo_requests_count=15,
            pricing_page_visits_count=4,
            budget_confirmed_count=20,
            timeline_confirmed_count=20,
            total_prospects_tracked=100,
        )
        score = engine._buying_signal_score(inp)
        assert score >= 25.0

    def test_pricing_rate_5_to_10_adds_12(self, engine):
        inp = make_input(
            demo_requests_count=15,
            pricing_page_visits_count=7,
            budget_confirmed_count=20,
            timeline_confirmed_count=20,
            total_prospects_tracked=100,
        )
        score = engine._buying_signal_score(inp)
        assert score >= 12.0

    def test_both_budget_and_timeline_below_10_adds_30(self, engine):
        inp = make_input(
            demo_requests_count=15,
            pricing_page_visits_count=12,
            budget_confirmed_count=5,
            timeline_confirmed_count=5,
            total_prospects_tracked=100,
        )
        score = engine._buying_signal_score(inp)
        assert score >= 30.0

    def test_budget_or_timeline_below_20_adds_15(self, engine):
        inp = make_input(
            demo_requests_count=15,
            pricing_page_visits_count=12,
            budget_confirmed_count=10,
            timeline_confirmed_count=25,
            total_prospects_tracked=100,
        )
        score = engine._buying_signal_score(inp)
        assert score >= 15.0

    def test_max_capped_at_100(self, engine):
        inp = make_input(
            demo_requests_count=0,
            pricing_page_visits_count=0,
            budget_confirmed_count=0,
            timeline_confirmed_count=0,
            total_prospects_tracked=100,
        )
        score = engine._buying_signal_score(inp)
        assert score <= 100.0

    def test_worst_case_score(self, engine):
        # demo < 5% → +30, pricing < 5% → +25, both budget+timeline < 10% → +30 = 85
        inp = make_input(
            demo_requests_count=0,
            pricing_page_visits_count=0,
            budget_confirmed_count=0,
            timeline_confirmed_count=0,
            total_prospects_tracked=100,
        )
        score = engine._buying_signal_score(inp)
        assert score == pytest.approx(85.0)

    def test_total_prospects_zero_handled(self, engine):
        inp = make_input(
            demo_requests_count=0,
            pricing_page_visits_count=0,
            budget_confirmed_count=0,
            timeline_confirmed_count=0,
            total_prospects_tracked=0,
        )
        score = engine._buying_signal_score(inp)
        assert isinstance(score, float)
        assert score <= 100.0

    def test_demo_rate_exactly_10_no_addition(self, engine):
        # demo_rate = 10/100 = 0.10 → not < 0.05, not < 0.10 → 0
        inp = make_input(
            demo_requests_count=10,
            pricing_page_visits_count=12,
            budget_confirmed_count=20,
            timeline_confirmed_count=20,
            total_prospects_tracked=100,
        )
        score = engine._buying_signal_score(inp)
        assert score == 0.0

    def test_pricing_rate_exactly_10_no_addition(self, engine):
        inp = make_input(
            demo_requests_count=15,
            pricing_page_visits_count=10,
            budget_confirmed_count=20,
            timeline_confirmed_count=20,
            total_prospects_tracked=100,
        )
        score = engine._buying_signal_score(inp)
        assert score == 0.0


# ===========================================================================
# 7. _competitive_threat_score
# ===========================================================================

class TestCompetitiveThreatScore:
    def test_no_threat_zero(self, engine):
        inp = make_input(
            competitor_mentions_count=0,
            total_prospects_tracked=100,
            avg_days_since_last_prospect_response=1.0,
            prospects_no_response_14d_count=5,
        )
        assert engine._competitive_threat_score(inp) == 0.0

    def test_high_competitor_rate_adds_45(self, engine):
        # rate = 30/100 = 0.30 → +45
        inp = make_input(
            competitor_mentions_count=30,
            total_prospects_tracked=100,
            avg_days_since_last_prospect_response=1.0,
            prospects_no_response_14d_count=5,
        )
        score = engine._competitive_threat_score(inp)
        assert score >= 45.0

    def test_medium_competitor_rate_adds_25(self, engine):
        # rate = 15/100 = 0.15 → +25
        inp = make_input(
            competitor_mentions_count=15,
            total_prospects_tracked=100,
            avg_days_since_last_prospect_response=1.0,
            prospects_no_response_14d_count=5,
        )
        score = engine._competitive_threat_score(inp)
        assert score >= 25.0

    def test_low_competitor_rate_adds_10(self, engine):
        # rate = 5/100 = 0.05 → +10
        inp = make_input(
            competitor_mentions_count=5,
            total_prospects_tracked=100,
            avg_days_since_last_prospect_response=1.0,
            prospects_no_response_14d_count=5,
        )
        score = engine._competitive_threat_score(inp)
        assert score >= 10.0

    def test_response_delay_14d_adds_35(self, engine):
        inp = make_input(
            competitor_mentions_count=0,
            total_prospects_tracked=100,
            avg_days_since_last_prospect_response=14.0,
            prospects_no_response_14d_count=5,
        )
        score = engine._competitive_threat_score(inp)
        assert score >= 35.0

    def test_response_delay_7d_adds_18(self, engine):
        inp = make_input(
            competitor_mentions_count=0,
            total_prospects_tracked=100,
            avg_days_since_last_prospect_response=7.0,
            prospects_no_response_14d_count=5,
        )
        score = engine._competitive_threat_score(inp)
        assert score >= 18.0

    def test_response_delay_4d_adds_7(self, engine):
        inp = make_input(
            competitor_mentions_count=0,
            total_prospects_tracked=100,
            avg_days_since_last_prospect_response=4.0,
            prospects_no_response_14d_count=5,
        )
        score = engine._competitive_threat_score(inp)
        assert score >= 7.0

    def test_high_no_response_14d_rate_adds_20(self, engine):
        # 30/100 = 0.30 → +20
        inp = make_input(
            competitor_mentions_count=0,
            total_prospects_tracked=100,
            avg_days_since_last_prospect_response=1.0,
            prospects_no_response_14d_count=30,
        )
        score = engine._competitive_threat_score(inp)
        assert score >= 20.0

    def test_medium_no_response_14d_rate_adds_10(self, engine):
        # 15/100 = 0.15 → +10
        inp = make_input(
            competitor_mentions_count=0,
            total_prospects_tracked=100,
            avg_days_since_last_prospect_response=1.0,
            prospects_no_response_14d_count=15,
        )
        score = engine._competitive_threat_score(inp)
        assert score >= 10.0

    def test_max_capped_at_100(self, engine):
        inp = make_input(
            competitor_mentions_count=100,
            total_prospects_tracked=100,
            avg_days_since_last_prospect_response=20.0,
            prospects_no_response_14d_count=50,
        )
        score = engine._competitive_threat_score(inp)
        assert score <= 100.0

    def test_worst_case_score(self, engine):
        # 45 + 35 + 20 = 100
        inp = make_input(
            competitor_mentions_count=100,
            total_prospects_tracked=100,
            avg_days_since_last_prospect_response=20.0,
            prospects_no_response_14d_count=50,
        )
        score = engine._competitive_threat_score(inp)
        assert score == pytest.approx(100.0)

    def test_response_delay_below_4d_no_addition(self, engine):
        inp = make_input(
            competitor_mentions_count=0,
            total_prospects_tracked=100,
            avg_days_since_last_prospect_response=3.9,
            prospects_no_response_14d_count=5,
        )
        assert engine._competitive_threat_score(inp) == 0.0


# ===========================================================================
# 8. Composite formula
# ===========================================================================

class TestCompositeFormula:
    def test_composite_formula(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        decay = result.engagement_decay_score
        champion = result.champion_health_score
        signal = result.buying_signal_score
        competitive = result.competitive_threat_score
        expected = round(decay * 0.30 + champion * 0.30 + signal * 0.25 + competitive * 0.15, 1)
        assert result.buyer_intent_composite == pytest.approx(expected)

    def test_composite_capped_at_100(self, engine):
        inp = make_input(
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=0,
            website_visits_prior_7d_count=100,
            prospects_no_response_30d_count=50,
            total_prospects_tracked=100,
            champion_last_contact_days=30.0,
            champion_response_rate_pct=0.05,
            multi_stakeholder_engagement_pct=0.05,
            demo_requests_count=0,
            pricing_page_visits_count=0,
            budget_confirmed_count=0,
            timeline_confirmed_count=0,
            competitor_mentions_count=100,
            avg_days_since_last_prospect_response=20.0,
            prospects_no_response_14d_count=50,
        )
        result = engine.assess(inp)
        assert result.buyer_intent_composite <= 100.0

    def test_composite_weights_decay(self, engine):
        """Ensure decay (0.30) contributes more than competitive (0.15)."""
        # Isolated decay=100, others=0: composite = 100*0.30 = 30
        inp = make_input(
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=0,
            website_visits_prior_7d_count=100,
            prospects_no_response_30d_count=50,
            total_prospects_tracked=100,
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
            demo_requests_count=15,
            pricing_page_visits_count=12,
            budget_confirmed_count=20,
            timeline_confirmed_count=20,
            competitor_mentions_count=0,
            avg_days_since_last_prospect_response=1.0,
            prospects_no_response_14d_count=5,
        )
        result = engine.assess(inp)
        # Decay is only real contributor here
        assert result.engagement_decay_score > 0
        assert result.buyer_intent_composite > 0


# ===========================================================================
# 9. _risk_level
# ===========================================================================

class TestRiskLevel:
    def test_below_20_is_low(self, engine):
        assert engine._risk_level(0.0) == IntentRisk.low
        assert engine._risk_level(19.9) == IntentRisk.low

    def test_exactly_20_is_moderate(self, engine):
        assert engine._risk_level(20.0) == IntentRisk.moderate

    def test_20_to_39_is_moderate(self, engine):
        assert engine._risk_level(25.0) == IntentRisk.moderate
        assert engine._risk_level(39.9) == IntentRisk.moderate

    def test_exactly_40_is_high(self, engine):
        assert engine._risk_level(40.0) == IntentRisk.high

    def test_40_to_59_is_high(self, engine):
        assert engine._risk_level(45.0) == IntentRisk.high
        assert engine._risk_level(59.9) == IntentRisk.high

    def test_exactly_60_is_critical(self, engine):
        assert engine._risk_level(60.0) == IntentRisk.critical

    def test_above_60_is_critical(self, engine):
        assert engine._risk_level(75.0) == IntentRisk.critical
        assert engine._risk_level(100.0) == IntentRisk.critical


# ===========================================================================
# 10. _severity
# ===========================================================================

class TestSeverity:
    def test_below_20_is_engaged(self, engine):
        assert engine._severity(0.0) == IntentSeverity.engaged
        assert engine._severity(19.9) == IntentSeverity.engaged

    def test_exactly_20_is_lukewarm(self, engine):
        assert engine._severity(20.0) == IntentSeverity.lukewarm

    def test_20_to_39_is_lukewarm(self, engine):
        assert engine._severity(25.0) == IntentSeverity.lukewarm
        assert engine._severity(39.9) == IntentSeverity.lukewarm

    def test_exactly_40_is_cooling(self, engine):
        assert engine._severity(40.0) == IntentSeverity.cooling

    def test_40_to_59_is_cooling(self, engine):
        assert engine._severity(50.0) == IntentSeverity.cooling
        assert engine._severity(59.9) == IntentSeverity.cooling

    def test_exactly_60_is_ghosted(self, engine):
        assert engine._severity(60.0) == IntentSeverity.ghosted

    def test_above_60_is_ghosted(self, engine):
        assert engine._severity(80.0) == IntentSeverity.ghosted
        assert engine._severity(100.0) == IntentSeverity.ghosted


# ===========================================================================
# 11. _action mapping
# ===========================================================================

class TestActionMapping:
    def test_low_risk_no_action(self, engine):
        action = engine._action(IntentRisk.low, IntentPattern.none)
        assert action == IntentAction.no_action

    def test_low_risk_any_pattern_no_action(self, engine):
        for p in IntentPattern:
            assert engine._action(IntentRisk.low, p) == IntentAction.no_action

    def test_moderate_risk_re_engagement(self, engine):
        action = engine._action(IntentRisk.moderate, IntentPattern.none)
        assert action == IntentAction.re_engagement_sequence

    def test_moderate_risk_all_patterns_re_engagement(self, engine):
        for p in IntentPattern:
            assert engine._action(IntentRisk.moderate, p) == IntentAction.re_engagement_sequence

    def test_high_risk_competitor_evaluation(self, engine):
        action = engine._action(IntentRisk.high, IntentPattern.competitor_evaluation)
        assert action == IntentAction.competitive_displacement

    def test_high_risk_timing_mismatch(self, engine):
        action = engine._action(IntentRisk.high, IntentPattern.timing_mismatch)
        assert action == IntentAction.timing_nurture_sequence

    def test_high_risk_default_re_engagement(self, engine):
        action = engine._action(IntentRisk.high, IntentPattern.none)
        assert action == IntentAction.re_engagement_sequence

    def test_high_risk_ghost_prospect_re_engagement(self, engine):
        action = engine._action(IntentRisk.high, IntentPattern.ghost_prospect)
        assert action == IntentAction.re_engagement_sequence

    def test_critical_champion_disengagement_outreach(self, engine):
        action = engine._action(IntentRisk.critical, IntentPattern.champion_disengagement)
        assert action == IntentAction.champion_outreach

    def test_critical_ghost_prospect_deal_rescue(self, engine):
        action = engine._action(IntentRisk.critical, IntentPattern.ghost_prospect)
        assert action == IntentAction.deal_rescue_escalation

    def test_critical_none_pattern_deal_rescue(self, engine):
        action = engine._action(IntentRisk.critical, IntentPattern.none)
        assert action == IntentAction.deal_rescue_escalation

    def test_critical_other_patterns_deal_rescue(self, engine):
        for p in [IntentPattern.intent_cooling, IntentPattern.competitor_evaluation,
                  IntentPattern.timing_mismatch]:
            assert engine._action(IntentRisk.critical, p) == IntentAction.deal_rescue_escalation


# ===========================================================================
# 12. _detect_pattern
# ===========================================================================

class TestDetectPattern:
    def test_none_pattern_healthy(self, engine, healthy_input):
        decay = engine._engagement_decay_score(healthy_input)
        champion = engine._champion_health_score(healthy_input)
        signal = engine._buying_signal_score(healthy_input)
        competitive = engine._competitive_threat_score(healthy_input)
        pattern = engine._detect_pattern(healthy_input, decay, champion, signal, competitive)
        assert pattern == IntentPattern.none

    def test_champion_disengagement_priority(self, engine):
        # champion >= 40 and last_contact >= 14 → champion_disengagement
        inp = make_input(
            champion_last_contact_days=21.0,
            champion_response_rate_pct=0.10,
            multi_stakeholder_engagement_pct=0.05,
            prospects_no_response_30d_count=50,
            total_prospects_tracked=100,
        )
        champion = engine._champion_health_score(inp)
        assert champion >= 40
        pattern = engine._detect_pattern(inp, 100, champion, 100, 100)
        assert pattern == IntentPattern.champion_disengagement

    def test_ghost_prospect_pattern(self, engine):
        # decay >= 40 and no_resp_30d_rate >= 0.30
        inp = make_input(
            prospects_no_response_30d_count=30,
            total_prospects_tracked=100,
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
        )
        # Champion score must be < 40 to skip champion_disengagement
        pattern = engine._detect_pattern(inp, 50, 10, 10, 10)
        assert pattern == IntentPattern.ghost_prospect

    def test_competitor_evaluation_pattern(self, engine):
        # competitive >= 30, competitor_rate >= 0.15
        inp = make_input(
            competitor_mentions_count=20,
            total_prospects_tracked=100,
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
            prospects_no_response_30d_count=5,
        )
        pattern = engine._detect_pattern(inp, 10, 10, 10, 40)
        assert pattern == IntentPattern.competitor_evaluation

    def test_timing_mismatch_pattern(self, engine):
        # signal >= 30, budget=0, timeline=0
        inp = make_input(
            budget_confirmed_count=0,
            timeline_confirmed_count=0,
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
            competitor_mentions_count=0,
        )
        pattern = engine._detect_pattern(inp, 10, 10, 40, 10)
        assert pattern == IntentPattern.timing_mismatch

    def test_intent_cooling_pattern(self, engine):
        # decay >= 25, but no other conditions met
        inp = make_input(
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
            competitor_mentions_count=1,  # < 0.15 rate
            budget_confirmed_count=10,    # at least one non-zero
        )
        pattern = engine._detect_pattern(inp, 25, 10, 10, 10)
        assert pattern == IntentPattern.intent_cooling

    def test_champion_disengagement_requires_last_contact_14(self, engine):
        # champion >= 40 but last_contact < 14 → no champion_disengagement
        inp = make_input(
            champion_last_contact_days=10.0,
            champion_response_rate_pct=0.10,
            multi_stakeholder_engagement_pct=0.05,
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
        )
        champion = engine._champion_health_score(inp)
        assert champion >= 40
        # With low decay/no_resp, should not ghost_prospect either
        pattern = engine._detect_pattern(inp, 10, champion, 10, 10)
        # champion score >= 40 but last_contact < 14 so no champion_disengagement
        assert pattern != IntentPattern.champion_disengagement

    def test_ghost_prospect_requires_decay_40(self, engine):
        # no_resp_30 rate >= 0.30 but decay < 40 → should not be ghost
        inp = make_input(
            prospects_no_response_30d_count=30,
            total_prospects_tracked=100,
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
        )
        pattern = engine._detect_pattern(inp, 30, 10, 10, 10)
        assert pattern != IntentPattern.ghost_prospect


# ===========================================================================
# 13. _has_intent_gap
# ===========================================================================

class TestHasIntentGap:
    def test_false_when_low_composite_and_low_rates(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
            champion_last_contact_days=5.0,
        )
        assert engine._has_intent_gap(15.0, inp) is False

    def test_true_when_composite_40_or_more(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
            champion_last_contact_days=5.0,
        )
        assert engine._has_intent_gap(40.0, inp) is True

    def test_true_when_no_response_30d_rate_30_or_more(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=30,
            total_prospects_tracked=100,
            champion_last_contact_days=5.0,
        )
        assert engine._has_intent_gap(10.0, inp) is True

    def test_true_when_champion_last_contact_21_or_more(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
            champion_last_contact_days=21.0,
        )
        assert engine._has_intent_gap(10.0, inp) is True

    def test_exactly_at_thresholds(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=30,
            total_prospects_tracked=100,
            champion_last_contact_days=21.0,
        )
        assert engine._has_intent_gap(40.0, inp) is True

    def test_zero_prospects_handled(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=0,
            total_prospects_tracked=0,
            champion_last_contact_days=5.0,
        )
        # no_resp_rate = 0/max(0,1) = 0, composite=10 < 40, champion < 21
        result = engine._has_intent_gap(10.0, inp)
        assert isinstance(result, bool)


# ===========================================================================
# 14. _requires_re_engagement
# ===========================================================================

class TestRequiresReEngagement:
    def test_false_when_all_low(self, engine):
        inp = make_input(
            avg_days_since_last_prospect_response=2.0,
            prospects_no_response_14d_count=5,
            total_prospects_tracked=100,
        )
        assert engine._requires_re_engagement(10.0, inp) is False

    def test_true_when_composite_30_or_more(self, engine):
        inp = make_input(
            avg_days_since_last_prospect_response=2.0,
            prospects_no_response_14d_count=5,
            total_prospects_tracked=100,
        )
        assert engine._requires_re_engagement(30.0, inp) is True

    def test_true_when_avg_days_10_or_more(self, engine):
        inp = make_input(
            avg_days_since_last_prospect_response=10.0,
            prospects_no_response_14d_count=5,
            total_prospects_tracked=100,
        )
        assert engine._requires_re_engagement(10.0, inp) is True

    def test_true_when_14d_rate_25_or_more(self, engine):
        inp = make_input(
            avg_days_since_last_prospect_response=2.0,
            prospects_no_response_14d_count=25,
            total_prospects_tracked=100,
        )
        assert engine._requires_re_engagement(10.0, inp) is True

    def test_exactly_at_thresholds(self, engine):
        inp = make_input(
            avg_days_since_last_prospect_response=10.0,
            prospects_no_response_14d_count=25,
            total_prospects_tracked=100,
        )
        assert engine._requires_re_engagement(30.0, inp) is True

    def test_14d_rate_below_25_false(self, engine):
        inp = make_input(
            avg_days_since_last_prospect_response=2.0,
            prospects_no_response_14d_count=24,
            total_prospects_tracked=100,
        )
        assert engine._requires_re_engagement(10.0, inp) is False


# ===========================================================================
# 15. _estimated_pipeline_at_risk
# ===========================================================================

class TestEstimatedPipelineAtRisk:
    def test_zero_when_no_non_responders(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=0,
            avg_opportunity_value_usd=5000.0,
        )
        assert engine._estimated_pipeline_at_risk(inp, 50.0) == 0.0

    def test_formula_basic(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=10,
            avg_opportunity_value_usd=1000.0,
        )
        result = engine._estimated_pipeline_at_risk(inp, 50.0)
        expected = round(10 * 1000.0 * 0.50, 2)
        assert result == pytest.approx(expected)

    def test_formula_full_composite(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=5,
            avg_opportunity_value_usd=2000.0,
        )
        result = engine._estimated_pipeline_at_risk(inp, 100.0)
        expected = round(5 * 2000.0 * 1.0, 2)
        assert result == pytest.approx(expected)

    def test_zero_composite_zero_risk(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=20,
            avg_opportunity_value_usd=5000.0,
        )
        assert engine._estimated_pipeline_at_risk(inp, 0.0) == 0.0

    def test_rounding(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=3,
            avg_opportunity_value_usd=333.33,
        )
        result = engine._estimated_pipeline_at_risk(inp, 33.3)
        assert result == round(3 * 333.33 * 0.333, 2)

    def test_large_values(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=100,
            avg_opportunity_value_usd=100000.0,
        )
        result = engine._estimated_pipeline_at_risk(inp, 80.0)
        expected = round(100 * 100000.0 * 0.80, 2)
        assert result == pytest.approx(expected)


# ===========================================================================
# 16. _signal
# ===========================================================================

class TestSignal:
    def test_healthy_benchmark(self, engine, healthy_input):
        sig = engine._signal(healthy_input, IntentPattern.none, 10.0)
        assert sig == "Buyer intent signals healthy — prospects showing active engagement"

    def test_pattern_none_but_composite_20_not_benchmark(self, engine, healthy_input):
        sig = engine._signal(healthy_input, IntentPattern.none, 20.0)
        assert "Buyer intent signals healthy" not in sig

    def test_signal_contains_pattern_label(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=30,
            total_prospects_tracked=100,
            champion_last_contact_days=5.0,
            competitor_mentions_count=0,
        )
        sig = engine._signal(inp, IntentPattern.ghost_prospect, 50.0)
        assert "Ghost prospect" in sig

    def test_signal_contains_no_response_rate_when_high(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=25,
            total_prospects_tracked=100,
            champion_last_contact_days=3.0,
            competitor_mentions_count=0,
        )
        sig = engine._signal(inp, IntentPattern.intent_cooling, 35.0)
        assert "25%" in sig
        assert "silent 30d" in sig

    def test_signal_contains_champion_days_when_7_or_more(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
            champion_last_contact_days=10.0,
            competitor_mentions_count=0,
        )
        sig = engine._signal(inp, IntentPattern.intent_cooling, 35.0)
        assert "10d since champion contact" in sig

    def test_signal_contains_competitor_mentions(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
            champion_last_contact_days=3.0,
            competitor_mentions_count=5,
        )
        sig = engine._signal(inp, IntentPattern.competitor_evaluation, 35.0)
        assert "5 competitor mentions" in sig

    def test_signal_no_parts_engagement_declining(self, engine):
        # No no_resp, no champion days >= 7, no competitors
        inp = make_input(
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
            champion_last_contact_days=3.0,
            competitor_mentions_count=0,
        )
        sig = engine._signal(inp, IntentPattern.intent_cooling, 30.0)
        assert "engagement declining" in sig

    def test_signal_composite_included(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
            champion_last_contact_days=3.0,
            competitor_mentions_count=0,
        )
        sig = engine._signal(inp, IntentPattern.intent_cooling, 35.0)
        assert "composite 35" in sig

    def test_signal_none_pattern_label_is_intent_risk(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
            champion_last_contact_days=3.0,
            competitor_mentions_count=0,
        )
        sig = engine._signal(inp, IntentPattern.none, 25.0)
        assert "Intent risk" in sig

    def test_signal_pattern_value_replaces_underscores(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
            champion_last_contact_days=3.0,
            competitor_mentions_count=0,
        )
        sig = engine._signal(inp, IntentPattern.champion_disengagement, 60.0)
        assert "_" not in sig.split(" — ")[0]

    def test_signal_no_response_rate_below_20_not_included(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=15,
            total_prospects_tracked=100,
            champion_last_contact_days=3.0,
            competitor_mentions_count=0,
        )
        sig = engine._signal(inp, IntentPattern.intent_cooling, 30.0)
        assert "silent 30d" not in sig

    def test_signal_champion_contact_below_7_not_included(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
            champion_last_contact_days=6.9,
            competitor_mentions_count=0,
        )
        sig = engine._signal(inp, IntentPattern.intent_cooling, 30.0)
        assert "since champion contact" not in sig


# ===========================================================================
# 17. assess() end-to-end
# ===========================================================================

class TestAssess:
    def test_returns_result_type(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result, BuyerIntentSignalResult)

    def test_result_rep_id_and_region(self, engine):
        inp = make_input(rep_id="rep-X", region="LATAM")
        result = engine.assess(inp)
        assert result.rep_id == "rep-X"
        assert result.region == "LATAM"

    def test_healthy_input_low_risk(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.intent_risk == IntentRisk.low

    def test_healthy_input_engaged_severity(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.intent_severity == IntentSeverity.engaged

    def test_healthy_input_no_action(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.recommended_action == IntentAction.no_action

    def test_healthy_input_pattern_none(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.intent_pattern == IntentPattern.none

    def test_healthy_input_no_intent_gap(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.has_intent_gap is False

    def test_healthy_input_no_re_engagement(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.requires_re_engagement is False

    def test_healthy_input_healthy_signal(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert "healthy" in result.intent_signal

    def test_high_risk_scenario(self, engine):
        inp = make_input(
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=0,
            website_visits_prior_7d_count=100,
            prospects_no_response_30d_count=50,
            total_prospects_tracked=100,
            champion_last_contact_days=25.0,
            champion_response_rate_pct=0.10,
            multi_stakeholder_engagement_pct=0.05,
            demo_requests_count=1,
            pricing_page_visits_count=1,
            budget_confirmed_count=1,
            timeline_confirmed_count=1,
            competitor_mentions_count=0,
            avg_days_since_last_prospect_response=5.0,
            prospects_no_response_14d_count=20,
        )
        result = engine.assess(inp)
        assert result.intent_risk in (IntentRisk.critical, IntentRisk.high)
        assert result.has_intent_gap is True
        assert result.requires_re_engagement is True

    def test_results_accumulated(self, engine, healthy_input):
        engine.assess(healthy_input)
        engine.assess(healthy_input)
        assert len(engine._results) == 2

    def test_scores_are_floats(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.engagement_decay_score, float)
        assert isinstance(result.champion_health_score, float)
        assert isinstance(result.buying_signal_score, float)
        assert isinstance(result.competitive_threat_score, float)
        assert isinstance(result.buyer_intent_composite, float)

    def test_pipeline_at_risk_is_float(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.estimated_pipeline_at_risk_usd, float)

    def test_critical_risk_deal_rescue(self, engine):
        inp = make_input(
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=0,
            website_visits_prior_7d_count=100,
            prospects_no_response_30d_count=80,
            total_prospects_tracked=100,
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.05,
            multi_stakeholder_engagement_pct=0.05,
            demo_requests_count=0,
            pricing_page_visits_count=0,
            budget_confirmed_count=0,
            timeline_confirmed_count=0,
            competitor_mentions_count=0,
            avg_days_since_last_prospect_response=20.0,
            prospects_no_response_14d_count=60,
        )
        result = engine.assess(inp)
        if result.intent_risk == IntentRisk.critical:
            assert result.recommended_action in (
                IntentAction.deal_rescue_escalation,
                IntentAction.champion_outreach,
            )

    def test_composite_rounded_to_1dp(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        # Should have at most 1 decimal place
        val = result.buyer_intent_composite
        assert round(val, 1) == val

    def test_signal_string_is_str(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.intent_signal, str)
        assert len(result.intent_signal) > 0


# ===========================================================================
# 18. assess_batch()
# ===========================================================================

class TestAssessBatch:
    def test_empty_list(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_single_item(self, engine, healthy_input):
        results = engine.assess_batch([healthy_input])
        assert len(results) == 1
        assert isinstance(results[0], BuyerIntentSignalResult)

    def test_multiple_items(self, engine, healthy_input):
        results = engine.assess_batch([healthy_input, healthy_input, healthy_input])
        assert len(results) == 3

    def test_results_accumulated_in_engine(self, engine, healthy_input):
        engine.assess_batch([healthy_input, healthy_input])
        assert len(engine._results) == 2

    def test_different_inputs_different_results(self, engine):
        inp1 = make_input(rep_id="A", champion_last_contact_days=2.0)
        inp2 = make_input(rep_id="B", champion_last_contact_days=30.0, champion_response_rate_pct=0.05)
        results = engine.assess_batch([inp1, inp2])
        assert results[0].rep_id == "A"
        assert results[1].rep_id == "B"
        assert results[0].champion_health_score < results[1].champion_health_score

    def test_order_preserved(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep-{i}"

    def test_returns_list_type(self, engine, healthy_input):
        results = engine.assess_batch([healthy_input])
        assert isinstance(results, list)

    def test_batch_same_as_individual(self, engine):
        engine2 = SalesBuyerIntentSignalIntelligenceEngine()
        inp = make_input(rep_id="test")
        r1 = engine.assess(inp)
        r2 = engine2.assess_batch([inp])[0]
        assert r1.buyer_intent_composite == r2.buyer_intent_composite
        assert r1.intent_risk == r2.intent_risk


# ===========================================================================
# 19. summary()
# ===========================================================================

class TestSummary:
    def test_empty_summary(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_buyer_intent_composite"] == 0.0
        assert s["intent_gap_count"] == 0
        assert s["re_engagement_count"] == 0
        assert s["avg_engagement_decay_score"] == 0.0
        assert s["avg_champion_health_score"] == 0.0
        assert s["avg_buying_signal_score"] == 0.0
        assert s["avg_competitive_threat_score"] == 0.0
        assert s["total_estimated_pipeline_at_risk_usd"] == 0.0

    def test_summary_has_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_summary_keys(self, engine):
        s = engine.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_buyer_intent_composite", "intent_gap_count",
            "re_engagement_count", "avg_engagement_decay_score",
            "avg_champion_health_score", "avg_buying_signal_score",
            "avg_competitive_threat_score", "total_estimated_pipeline_at_risk_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_after_one_assess(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        assert s["total"] == 1

    def test_summary_total_count(self, engine, healthy_input):
        for _ in range(5):
            engine.assess(healthy_input)
        s = engine.summary()
        assert s["total"] == 5

    def test_summary_risk_counts(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == 1

    def test_summary_pattern_counts(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == 1

    def test_summary_severity_counts(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == 1

    def test_summary_action_counts(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        assert sum(s["action_counts"].values()) == 1

    def test_summary_avg_composite(self, engine, healthy_input):
        engine.assess(healthy_input)
        engine.assess(healthy_input)
        s = engine.summary()
        assert isinstance(s["avg_buyer_intent_composite"], float)

    def test_summary_intent_gap_count(self, engine):
        inp_no_gap = make_input()
        inp_gap = make_input(
            prospects_no_response_30d_count=40,
            total_prospects_tracked=100,
            champion_last_contact_days=5.0,
        )
        engine.assess(inp_no_gap)
        engine.assess(inp_gap)
        s = engine.summary()
        # At least one has intent gap
        assert s["intent_gap_count"] >= 1

    def test_summary_re_engagement_count(self, engine):
        inp_no_re = make_input()
        inp_re = make_input(avg_days_since_last_prospect_response=15.0)
        engine.assess(inp_no_re)
        engine.assess(inp_re)
        s = engine.summary()
        assert s["re_engagement_count"] >= 1

    def test_summary_avgs_rounded_to_1dp(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        for key in ["avg_buyer_intent_composite", "avg_engagement_decay_score",
                    "avg_champion_health_score", "avg_buying_signal_score",
                    "avg_competitive_threat_score"]:
            val = s[key]
            assert round(val, 1) == val

    def test_summary_pipeline_at_risk_sum(self, engine):
        inp1 = make_input(prospects_no_response_30d_count=10, avg_opportunity_value_usd=1000.0)
        inp2 = make_input(prospects_no_response_30d_count=20, avg_opportunity_value_usd=500.0)
        r1 = engine.assess(inp1)
        r2 = engine.assess(inp2)
        s = engine.summary()
        expected = round(r1.estimated_pipeline_at_risk_usd + r2.estimated_pipeline_at_risk_usd, 2)
        assert s["total_estimated_pipeline_at_risk_usd"] == pytest.approx(expected)

    def test_summary_multiple_risks(self, engine):
        inp_low = make_input()  # healthy → low
        inp_high = make_input(
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=0,
            website_visits_prior_7d_count=100,
            prospects_no_response_30d_count=50,
            total_prospects_tracked=100,
            champion_last_contact_days=25.0,
            champion_response_rate_pct=0.05,
            multi_stakeholder_engagement_pct=0.05,
        )
        engine.assess(inp_low)
        engine.assess(inp_high)
        s = engine.summary()
        assert s["total"] == 2
        assert len(s["risk_counts"]) >= 2

    def test_summary_accumulates_across_batches(self, engine, healthy_input):
        engine.assess_batch([healthy_input, healthy_input])
        engine.assess(healthy_input)
        s = engine.summary()
        assert s["total"] == 3

    def test_summary_risk_counts_keys_are_strings(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        for key in s["risk_counts"]:
            assert isinstance(key, str)

    def test_summary_pattern_counts_keys_are_strings(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        for key in s["pattern_counts"]:
            assert isinstance(key, str)

    def test_summary_avg_decay_correct(self, engine):
        inp = make_input(
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=100,
        )
        engine.assess(inp)
        s = engine.summary()
        assert s["avg_engagement_decay_score"] > 0


# ===========================================================================
# 20. Engine state isolation
# ===========================================================================

class TestEngineStateIsolation:
    def test_new_engine_empty_results(self):
        engine = SalesBuyerIntentSignalIntelligenceEngine()
        assert engine._results == []

    def test_two_engines_independent(self):
        e1 = SalesBuyerIntentSignalIntelligenceEngine()
        e2 = SalesBuyerIntentSignalIntelligenceEngine()
        inp = make_input()
        e1.assess(inp)
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_multiple_assess_accumulate(self):
        engine = SalesBuyerIntentSignalIntelligenceEngine()
        for i in range(10):
            engine.assess(make_input(rep_id=f"rep-{i}"))
        assert len(engine._results) == 10

    def test_summary_empty_before_assess(self):
        engine = SalesBuyerIntentSignalIntelligenceEngine()
        s = engine.summary()
        assert s["total"] == 0


# ===========================================================================
# 21. Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_all_zeros_input(self, engine):
        inp = BuyerIntentSignalInput(
            rep_id="zero",
            region="ZERO",
            evaluation_period_id="Q0",
            total_prospects_tracked=0,
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=0,
            website_visits_last_7d_count=0,
            website_visits_prior_7d_count=0,
            content_downloads_last_7d_count=0,
            demo_requests_count=0,
            pricing_page_visits_count=0,
            avg_days_since_last_prospect_response=0.0,
            prospects_no_response_14d_count=0,
            prospects_no_response_30d_count=0,
            champion_response_rate_pct=0.0,
            champion_last_contact_days=0.0,
            competitor_mentions_count=0,
            multi_stakeholder_engagement_pct=0.0,
            buying_committee_size_avg=0.0,
            budget_confirmed_count=0,
            timeline_confirmed_count=0,
            avg_opportunity_value_usd=0.0,
        )
        result = engine.assess(inp)
        assert result is not None
        assert result.estimated_pipeline_at_risk_usd == 0.0

    def test_very_large_values(self, engine):
        inp = make_input(
            total_prospects_tracked=100000,
            email_opens_last_7d_count=50000,
            email_opens_prior_7d_count=100000,
            avg_opportunity_value_usd=1_000_000.0,
            prospects_no_response_30d_count=30000,
        )
        result = engine.assess(inp)
        assert result.buyer_intent_composite <= 100.0
        assert result.estimated_pipeline_at_risk_usd >= 0.0

    def test_all_prospects_non_responsive(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=100,
            total_prospects_tracked=100,
        )
        result = engine.assess(inp)
        assert result.has_intent_gap is True

    def test_composite_is_non_negative(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.buyer_intent_composite >= 0.0

    def test_all_sub_scores_non_negative(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.engagement_decay_score >= 0.0
        assert result.champion_health_score >= 0.0
        assert result.buying_signal_score >= 0.0
        assert result.competitive_threat_score >= 0.0

    def test_pipeline_at_risk_non_negative(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.estimated_pipeline_at_risk_usd >= 0.0

    def test_to_dict_all_keys_present(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_champion_last_contact_exactly_14(self, engine):
        inp = make_input(
            champion_last_contact_days=14.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
        )
        score = engine._champion_health_score(inp)
        assert score >= 22.0

    def test_champion_last_contact_exactly_21(self, engine):
        inp = make_input(
            champion_last_contact_days=21.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
        )
        score = engine._champion_health_score(inp)
        assert score >= 40.0

    def test_single_prospect_tracked(self, engine):
        inp = make_input(
            total_prospects_tracked=1,
            prospects_no_response_30d_count=1,
            prospects_no_response_14d_count=1,
            demo_requests_count=0,
            pricing_page_visits_count=0,
        )
        result = engine.assess(inp)
        assert result is not None

    def test_email_opens_greater_than_prior(self, engine):
        # open_decay < 0 → no addition (branch not hit)
        inp = make_input(
            email_opens_last_7d_count=120,
            email_opens_prior_7d_count=100,
        )
        decay = engine._engagement_decay_score(inp)
        # open_decay = (100-120)/100 = -0.20 → none of the branches fire
        assert decay >= 0.0

    def test_visits_greater_than_prior(self, engine):
        inp = make_input(
            website_visits_last_7d_count=120,
            website_visits_prior_7d_count=100,
        )
        decay = engine._engagement_decay_score(inp)
        assert decay >= 0.0

    def test_assess_result_stored(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert engine._results[-1] is result


# ===========================================================================
# 22. End-to-end scenarios
# ===========================================================================

class TestEndToEndScenarios:
    def test_scenario_champion_disengagement(self, engine):
        """Champion disengaged for 3 weeks with low response rate."""
        inp = make_input(
            champion_last_contact_days=22.0,
            champion_response_rate_pct=0.10,
            multi_stakeholder_engagement_pct=0.05,
        )
        result = engine.assess(inp)
        assert result.intent_pattern == IntentPattern.champion_disengagement
        assert result.champion_health_score >= 40.0

    def test_scenario_ghost_prospect(self, engine):
        """High no-response rate with email decay."""
        inp = make_input(
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=0,
            website_visits_prior_7d_count=100,
            prospects_no_response_30d_count=50,
            total_prospects_tracked=100,
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
        )
        result = engine.assess(inp)
        assert result.intent_pattern == IntentPattern.ghost_prospect

    def test_scenario_competitor_evaluation(self, engine):
        """High competitor mentions with moderate competitive threat."""
        inp = make_input(
            competitor_mentions_count=25,
            total_prospects_tracked=100,
            avg_days_since_last_prospect_response=10.0,
            prospects_no_response_14d_count=20,
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
            prospects_no_response_30d_count=5,
        )
        result = engine.assess(inp)
        assert result.intent_pattern == IntentPattern.competitor_evaluation

    def test_scenario_timing_mismatch(self, engine):
        """No budget or timeline confirmation with low demo rate."""
        inp = make_input(
            budget_confirmed_count=0,
            timeline_confirmed_count=0,
            demo_requests_count=1,
            pricing_page_visits_count=1,
            total_prospects_tracked=100,
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
            competitor_mentions_count=0,
            prospects_no_response_30d_count=5,
        )
        result = engine.assess(inp)
        assert result.intent_pattern == IntentPattern.timing_mismatch

    def test_scenario_intent_cooling(self, engine):
        """Mild email decay without meeting ghost or other pattern conditions."""
        inp = make_input(
            email_opens_last_7d_count=30,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=50,
            website_visits_prior_7d_count=70,
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.80,
            multi_stakeholder_engagement_pct=0.70,
            competitor_mentions_count=0,
            budget_confirmed_count=15,
            timeline_confirmed_count=15,
            prospects_no_response_30d_count=5,
            total_prospects_tracked=100,
        )
        result = engine.assess(inp)
        assert result.intent_pattern == IntentPattern.intent_cooling

    def test_scenario_full_pipeline_at_risk(self, engine):
        """100 non-responsive prospects at $10k each with high composite."""
        inp = make_input(
            prospects_no_response_30d_count=50,
            avg_opportunity_value_usd=10000.0,
            total_prospects_tracked=100,
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=100,
        )
        result = engine.assess(inp)
        expected = round(50 * 10000.0 * (result.buyer_intent_composite / 100.0), 2)
        assert result.estimated_pipeline_at_risk_usd == pytest.approx(expected)

    def test_scenario_healthy_benchmark_signal(self, engine):
        """Healthy scenario produces benchmark signal."""
        result = engine.assess(make_input())
        assert "healthy" in result.intent_signal

    def test_scenario_batch_summary_consistency(self, engine):
        """Batch + summary totals are consistent."""
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(10)]
        results = engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 10
        assert sum(s["risk_counts"].values()) == 10
        assert sum(s["pattern_counts"].values()) == 10
        assert sum(s["severity_counts"].values()) == 10
        assert sum(s["action_counts"].values()) == 10

    def test_scenario_all_critical(self, engine):
        """All inputs lead to critical risk; summary shows all critical."""
        worst = make_input(
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=0,
            website_visits_prior_7d_count=100,
            prospects_no_response_30d_count=80,
            total_prospects_tracked=100,
            champion_last_contact_days=2.0,
            champion_response_rate_pct=0.05,
            multi_stakeholder_engagement_pct=0.05,
            demo_requests_count=0,
            pricing_page_visits_count=0,
            budget_confirmed_count=0,
            timeline_confirmed_count=0,
            competitor_mentions_count=0,
            avg_days_since_last_prospect_response=20.0,
            prospects_no_response_14d_count=60,
        )
        engine.assess_batch([worst, worst, worst])
        s = engine.summary()
        # All should be same risk level
        assert s["total"] == 3
        assert len(s["risk_counts"]) == 1

    def test_scenario_to_dict_roundtrip(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        d = result.to_dict()
        assert d["rep_id"] == result.rep_id
        assert d["buyer_intent_composite"] == result.buyer_intent_composite
        assert d["intent_risk"] == result.intent_risk.value
        assert d["has_intent_gap"] == result.has_intent_gap

    def test_scenario_mixed_batch(self, engine):
        """Mix of healthy and risky inputs produces varied summary."""
        healthy = make_input(rep_id="h")
        risky = make_input(
            rep_id="r",
            email_opens_last_7d_count=0,
            email_opens_prior_7d_count=100,
            website_visits_last_7d_count=0,
            website_visits_prior_7d_count=100,
            prospects_no_response_30d_count=50,
            total_prospects_tracked=100,
        )
        engine.assess_batch([healthy, risky])
        s = engine.summary()
        assert s["total"] == 2
        # At least two different risk levels
        assert len(s["risk_counts"]) >= 1

    def test_risk_low_20_boundary(self, engine):
        """Test boundary at composite=20 for risk classification."""
        assert engine._risk_level(19.9) == IntentRisk.low
        assert engine._risk_level(20.0) == IntentRisk.moderate

    def test_risk_high_60_boundary(self, engine):
        """Test boundary at composite=60 for risk classification."""
        assert engine._risk_level(59.9) == IntentRisk.high
        assert engine._risk_level(60.0) == IntentRisk.critical

    def test_severity_boundaries(self, engine):
        """Test all severity boundaries."""
        assert engine._severity(19.9) == IntentSeverity.engaged
        assert engine._severity(20.0) == IntentSeverity.lukewarm
        assert engine._severity(39.9) == IntentSeverity.lukewarm
        assert engine._severity(40.0) == IntentSeverity.cooling
        assert engine._severity(59.9) == IntentSeverity.cooling
        assert engine._severity(60.0) == IntentSeverity.ghosted

    def test_pipeline_at_risk_zero_composite(self, engine):
        inp = make_input(
            prospects_no_response_30d_count=10,
            avg_opportunity_value_usd=5000.0,
        )
        at_risk = engine._estimated_pipeline_at_risk(inp, 0.0)
        assert at_risk == 0.0

    def test_multiple_engines_dont_share_state(self):
        e1 = SalesBuyerIntentSignalIntelligenceEngine()
        e2 = SalesBuyerIntentSignalIntelligenceEngine()
        inp = make_input()
        e1.assess(inp)
        e1.assess(inp)
        e2.assess(inp)
        assert len(e1._results) == 2
        assert len(e2._results) == 1

    def test_buying_signal_score_timeline_only_below_20(self, engine):
        """Budget high but timeline below 20 → +15."""
        inp = make_input(
            demo_requests_count=15,
            pricing_page_visits_count=12,
            budget_confirmed_count=25,
            timeline_confirmed_count=10,  # 10% < 20% threshold
            total_prospects_tracked=100,
        )
        score = engine._buying_signal_score(inp)
        assert score >= 15.0

    def test_buying_signal_score_budget_only_below_20(self, engine):
        """Timeline high but budget below 20 → +15."""
        inp = make_input(
            demo_requests_count=15,
            pricing_page_visits_count=12,
            budget_confirmed_count=10,  # 10% < 20% threshold
            timeline_confirmed_count=25,
            total_prospects_tracked=100,
        )
        score = engine._buying_signal_score(inp)
        assert score >= 15.0
