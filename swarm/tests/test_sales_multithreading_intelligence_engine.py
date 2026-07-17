"""
Comprehensive pytest test suite for SalesMultithreadingIntelligenceEngine.
Covers all enums, dataclasses, sub-score methods, pattern detection,
risk/severity/action mapping, flag methods, revenue at risk, signal
generation, assess(), assess_batch(), summary(), edge cases, and E2E scenarios.
"""
from __future__ import annotations

import pytest
from dataclasses import fields

from swarm.intelligence.sales_multithreading_intelligence_engine import (
    MultithreadAction,
    MultithreadInput,
    MultithreadPattern,
    MultithreadResult,
    MultithreadRisk,
    MultithreadSeverity,
    SalesMultithreadingIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers / Fixtures
# ---------------------------------------------------------------------------

def make_input(**overrides) -> MultithreadInput:
    """Return a healthy (low-risk) baseline input with any field overridden."""
    defaults = dict(
        rep_id="rep-001",
        region="West",
        evaluation_period_id="Q2-2026",
        total_active_deals=20,
        avg_stakeholders_per_deal=4.0,
        single_threaded_deals_pct=0.10,
        executive_sponsor_engaged_pct=0.60,
        champion_identified_pct=0.80,
        economic_buyer_engaged_pct=0.75,
        user_buyer_engaged_pct=0.70,
        technical_buyer_engaged_pct=0.65,
        avg_days_since_secondary_contact=5.0,
        deals_with_decision_maker_pct=0.80,
        deal_reviews_with_multi_contacts_pct=0.75,
        avg_contacts_added_per_month=4.0,
        internal_champion_strength_score=0.80,
        champion_last_active_days_avg=3.0,
        deals_at_risk_from_champion_loss_pct=0.10,
        multi_site_deals_pct=0.30,
        stakeholder_map_completion_pct=0.85,
        referrals_from_existing_contacts_count=5,
        avg_opportunity_value_usd=50000.0,
    )
    defaults.update(overrides)
    return MultithreadInput(**defaults)


def make_engine() -> SalesMultithreadingIntelligenceEngine:
    return SalesMultithreadingIntelligenceEngine()


@pytest.fixture
def engine():
    return make_engine()


@pytest.fixture
def healthy_input():
    return make_input()


# ---------------------------------------------------------------------------
# 1. Enum tests
# ---------------------------------------------------------------------------

class TestMultithreadRiskEnum:
    def test_values_exist(self):
        assert MultithreadRisk.low.value == "low"
        assert MultithreadRisk.moderate.value == "moderate"
        assert MultithreadRisk.high.value == "high"
        assert MultithreadRisk.critical.value == "critical"

    def test_count(self):
        assert len(MultithreadRisk) == 4

    def test_is_str(self):
        assert isinstance(MultithreadRisk.low, str)

    def test_str_comparison(self):
        assert MultithreadRisk.low == "low"
        assert MultithreadRisk.critical == "critical"

    def test_members_are_distinct(self):
        values = [m.value for m in MultithreadRisk]
        assert len(values) == len(set(values))


class TestMultithreadPatternEnum:
    def test_values_exist(self):
        assert MultithreadPattern.none.value == "none"
        assert MultithreadPattern.single_threading.value == "single_threading"
        assert MultithreadPattern.champion_dependency.value == "champion_dependency"
        assert MultithreadPattern.executive_blind_spot.value == "executive_blind_spot"
        assert MultithreadPattern.stakeholder_map_gap.value == "stakeholder_map_gap"
        assert MultithreadPattern.relationship_stagnation.value == "relationship_stagnation"

    def test_count(self):
        assert len(MultithreadPattern) == 6

    def test_is_str(self):
        assert isinstance(MultithreadPattern.none, str)

    def test_members_are_distinct(self):
        values = [m.value for m in MultithreadPattern]
        assert len(values) == len(set(values))


class TestMultithreadSeverityEnum:
    def test_values_exist(self):
        assert MultithreadSeverity.networked.value == "networked"
        assert MultithreadSeverity.developing.value == "developing"
        assert MultithreadSeverity.exposed.value == "exposed"
        assert MultithreadSeverity.fragile.value == "fragile"

    def test_count(self):
        assert len(MultithreadSeverity) == 4

    def test_is_str(self):
        assert isinstance(MultithreadSeverity.networked, str)

    def test_members_are_distinct(self):
        values = [m.value for m in MultithreadSeverity]
        assert len(values) == len(set(values))


class TestMultithreadActionEnum:
    def test_values_exist(self):
        assert MultithreadAction.no_action.value == "no_action"
        assert MultithreadAction.multithread_coaching.value == "multithread_coaching"
        assert MultithreadAction.champion_backup_strategy.value == "champion_backup_strategy"
        assert MultithreadAction.executive_outreach_plan.value == "executive_outreach_plan"
        assert MultithreadAction.stakeholder_mapping_session.value == "stakeholder_mapping_session"
        assert MultithreadAction.relationship_expansion_sprint.value == "relationship_expansion_sprint"

    def test_count(self):
        assert len(MultithreadAction) == 6

    def test_is_str(self):
        assert isinstance(MultithreadAction.no_action, str)

    def test_members_are_distinct(self):
        values = [m.value for m in MultithreadAction]
        assert len(values) == len(set(values))


# ---------------------------------------------------------------------------
# 2. MultithreadInput dataclass tests
# ---------------------------------------------------------------------------

class TestMultithreadInput:
    def test_field_count(self):
        assert len(fields(MultithreadInput)) == 22

    def test_instantiation(self, healthy_input):
        assert healthy_input.rep_id == "rep-001"
        assert healthy_input.region == "West"
        assert healthy_input.evaluation_period_id == "Q2-2026"

    def test_int_fields(self, healthy_input):
        assert isinstance(healthy_input.total_active_deals, int)
        assert isinstance(healthy_input.referrals_from_existing_contacts_count, int)

    def test_float_fields(self, healthy_input):
        float_fields = [
            "avg_stakeholders_per_deal",
            "single_threaded_deals_pct",
            "executive_sponsor_engaged_pct",
            "champion_identified_pct",
            "economic_buyer_engaged_pct",
            "user_buyer_engaged_pct",
            "technical_buyer_engaged_pct",
            "avg_days_since_secondary_contact",
            "deals_with_decision_maker_pct",
            "deal_reviews_with_multi_contacts_pct",
            "avg_contacts_added_per_month",
            "internal_champion_strength_score",
            "champion_last_active_days_avg",
            "deals_at_risk_from_champion_loss_pct",
            "multi_site_deals_pct",
            "stakeholder_map_completion_pct",
            "avg_opportunity_value_usd",
        ]
        for fname in float_fields:
            assert isinstance(getattr(healthy_input, fname), float), fname

    def test_field_names(self):
        field_names = {f.name for f in fields(MultithreadInput)}
        expected = {
            "rep_id", "region", "evaluation_period_id", "total_active_deals",
            "avg_stakeholders_per_deal", "single_threaded_deals_pct",
            "executive_sponsor_engaged_pct", "champion_identified_pct",
            "economic_buyer_engaged_pct", "user_buyer_engaged_pct",
            "technical_buyer_engaged_pct", "avg_days_since_secondary_contact",
            "deals_with_decision_maker_pct", "deal_reviews_with_multi_contacts_pct",
            "avg_contacts_added_per_month", "internal_champion_strength_score",
            "champion_last_active_days_avg", "deals_at_risk_from_champion_loss_pct",
            "multi_site_deals_pct", "stakeholder_map_completion_pct",
            "referrals_from_existing_contacts_count", "avg_opportunity_value_usd",
        }
        assert field_names == expected

    def test_override_works(self):
        inp = make_input(rep_id="rep-999", region="East")
        assert inp.rep_id == "rep-999"
        assert inp.region == "East"


# ---------------------------------------------------------------------------
# 3. MultithreadResult dataclass tests
# ---------------------------------------------------------------------------

class TestMultithreadResult:
    def _make_result(self) -> MultithreadResult:
        eng = make_engine()
        return eng.assess(make_input())

    def test_field_count(self):
        assert len(fields(MultithreadResult)) == 15

    def test_field_names(self):
        field_names = {f.name for f in fields(MultithreadResult)}
        expected = {
            "rep_id", "region", "multithread_risk", "multithread_pattern",
            "multithread_severity", "recommended_action", "threading_breadth_score",
            "champion_dependency_score", "decision_maker_coverage_score",
            "relationship_map_score", "multithread_composite", "has_threading_gap",
            "requires_multithread_coaching", "estimated_at_risk_usd", "multithread_signal",
        }
        assert field_names == expected

    def test_to_dict_returns_15_keys(self):
        r = self._make_result()
        d = r.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self):
        r = self._make_result()
        d = r.to_dict()
        expected_keys = {
            "rep_id", "region", "multithread_risk", "multithread_pattern",
            "multithread_severity", "recommended_action", "threading_breadth_score",
            "champion_dependency_score", "decision_maker_coverage_score",
            "relationship_map_score", "multithread_composite", "has_threading_gap",
            "requires_multithread_coaching", "estimated_at_risk_usd", "multithread_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        r = self._make_result()
        d = r.to_dict()
        assert isinstance(d["multithread_risk"], str)
        assert isinstance(d["multithread_pattern"], str)
        assert isinstance(d["multithread_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_numeric_fields(self):
        r = self._make_result()
        d = r.to_dict()
        for key in ["threading_breadth_score", "champion_dependency_score",
                    "decision_maker_coverage_score", "relationship_map_score",
                    "multithread_composite", "estimated_at_risk_usd"]:
            assert isinstance(d[key], float), key

    def test_to_dict_bool_fields(self):
        r = self._make_result()
        d = r.to_dict()
        assert isinstance(d["has_threading_gap"], bool)
        assert isinstance(d["requires_multithread_coaching"], bool)

    def test_to_dict_signal_is_str(self):
        r = self._make_result()
        d = r.to_dict()
        assert isinstance(d["multithread_signal"], str)

    def test_to_dict_rep_id_matches(self):
        r = self._make_result()
        d = r.to_dict()
        assert d["rep_id"] == "rep-001"

    def test_to_dict_region_matches(self):
        r = self._make_result()
        d = r.to_dict()
        assert d["region"] == "West"


# ---------------------------------------------------------------------------
# 4. _threading_breadth_score tests
# ---------------------------------------------------------------------------

class TestThreadingBreadthScore:
    def _score(self, **kw):
        eng = make_engine()
        return eng._threading_breadth_score(make_input(**kw))

    # single_threaded_deals_pct tiers
    def test_single_threaded_below_30(self):
        s = self._score(single_threaded_deals_pct=0.10)
        assert s == 0.0  # no contribution from that tier

    def test_single_threaded_30_to_49(self):
        s = self._score(single_threaded_deals_pct=0.30,
                        avg_stakeholders_per_deal=5.0,
                        executive_sponsor_engaged_pct=0.80)
        assert s == 10.0

    def test_single_threaded_50_to_69(self):
        s = self._score(single_threaded_deals_pct=0.50,
                        avg_stakeholders_per_deal=5.0,
                        executive_sponsor_engaged_pct=0.80)
        assert s == 25.0

    def test_single_threaded_70_plus(self):
        s = self._score(single_threaded_deals_pct=0.70,
                        avg_stakeholders_per_deal=5.0,
                        executive_sponsor_engaged_pct=0.80)
        assert s == 45.0

    def test_single_threaded_exact_0_69(self):
        # 0.69 is in the 0.50-0.70 bucket
        s = self._score(single_threaded_deals_pct=0.69,
                        avg_stakeholders_per_deal=5.0,
                        executive_sponsor_engaged_pct=0.80)
        assert s == 25.0

    # avg_stakeholders_per_deal tiers
    def test_stakeholders_below_2(self):
        s = self._score(single_threaded_deals_pct=0.0,
                        avg_stakeholders_per_deal=1.5,
                        executive_sponsor_engaged_pct=0.80)
        assert s == 30.0

    def test_stakeholders_2_to_3(self):
        s = self._score(single_threaded_deals_pct=0.0,
                        avg_stakeholders_per_deal=2.0,
                        executive_sponsor_engaged_pct=0.80)
        assert s == 15.0

    def test_stakeholders_3_to_4(self):
        s = self._score(single_threaded_deals_pct=0.0,
                        avg_stakeholders_per_deal=3.0,
                        executive_sponsor_engaged_pct=0.80)
        assert s == 5.0

    def test_stakeholders_4_plus(self):
        s = self._score(single_threaded_deals_pct=0.0,
                        avg_stakeholders_per_deal=4.0,
                        executive_sponsor_engaged_pct=0.80)
        assert s == 0.0

    # executive_sponsor_engaged_pct tiers
    def test_exec_sponsor_below_20(self):
        s = self._score(single_threaded_deals_pct=0.0,
                        avg_stakeholders_per_deal=5.0,
                        executive_sponsor_engaged_pct=0.10)
        assert s == 25.0

    def test_exec_sponsor_20_to_39(self):
        s = self._score(single_threaded_deals_pct=0.0,
                        avg_stakeholders_per_deal=5.0,
                        executive_sponsor_engaged_pct=0.20)
        assert s == 12.0

    def test_exec_sponsor_40_plus(self):
        s = self._score(single_threaded_deals_pct=0.0,
                        avg_stakeholders_per_deal=5.0,
                        executive_sponsor_engaged_pct=0.40)
        assert s == 0.0

    # max cap
    def test_capped_at_100(self):
        s = self._score(single_threaded_deals_pct=1.0,
                        avg_stakeholders_per_deal=1.0,
                        executive_sponsor_engaged_pct=0.0)
        assert s <= 100.0

    def test_max_possible_is_100(self):
        # 45 + 30 + 25 = 100, already capped
        s = self._score(single_threaded_deals_pct=0.70,
                        avg_stakeholders_per_deal=1.5,
                        executive_sponsor_engaged_pct=0.10)
        assert s == 100.0

    def test_zero_risk_case(self):
        s = self._score(single_threaded_deals_pct=0.0,
                        avg_stakeholders_per_deal=5.0,
                        executive_sponsor_engaged_pct=0.80)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 5. _champion_dependency_score tests
# ---------------------------------------------------------------------------

class TestChampionDependencyScore:
    def _score(self, **kw):
        eng = make_engine()
        return eng._champion_dependency_score(make_input(**kw))

    # champion_last_active_days_avg tiers
    def test_champion_active_below_7(self):
        s = self._score(champion_last_active_days_avg=3.0,
                        deals_at_risk_from_champion_loss_pct=0.0,
                        internal_champion_strength_score=0.90)
        assert s == 0.0

    def test_champion_active_7_to_13(self):
        s = self._score(champion_last_active_days_avg=7.0,
                        deals_at_risk_from_champion_loss_pct=0.0,
                        internal_champion_strength_score=0.90)
        assert s == 8.0

    def test_champion_active_14_to_20(self):
        s = self._score(champion_last_active_days_avg=14.0,
                        deals_at_risk_from_champion_loss_pct=0.0,
                        internal_champion_strength_score=0.90)
        assert s == 22.0

    def test_champion_active_21_plus(self):
        s = self._score(champion_last_active_days_avg=21.0,
                        deals_at_risk_from_champion_loss_pct=0.0,
                        internal_champion_strength_score=0.90)
        assert s == 40.0

    # deals_at_risk_from_champion_loss_pct tiers
    def test_champion_loss_below_30(self):
        s = self._score(champion_last_active_days_avg=1.0,
                        deals_at_risk_from_champion_loss_pct=0.10,
                        internal_champion_strength_score=0.90)
        assert s == 0.0

    def test_champion_loss_30_to_49(self):
        s = self._score(champion_last_active_days_avg=1.0,
                        deals_at_risk_from_champion_loss_pct=0.30,
                        internal_champion_strength_score=0.90)
        assert s == 18.0

    def test_champion_loss_50_plus(self):
        s = self._score(champion_last_active_days_avg=1.0,
                        deals_at_risk_from_champion_loss_pct=0.50,
                        internal_champion_strength_score=0.90)
        assert s == 35.0

    # internal_champion_strength_score tiers
    def test_champion_strength_below_40(self):
        s = self._score(champion_last_active_days_avg=1.0,
                        deals_at_risk_from_champion_loss_pct=0.0,
                        internal_champion_strength_score=0.30)
        assert s == 25.0

    def test_champion_strength_40_to_59(self):
        s = self._score(champion_last_active_days_avg=1.0,
                        deals_at_risk_from_champion_loss_pct=0.0,
                        internal_champion_strength_score=0.40)
        assert s == 12.0

    def test_champion_strength_60_plus(self):
        s = self._score(champion_last_active_days_avg=1.0,
                        deals_at_risk_from_champion_loss_pct=0.0,
                        internal_champion_strength_score=0.60)
        assert s == 0.0

    def test_capped_at_100(self):
        s = self._score(champion_last_active_days_avg=30.0,
                        deals_at_risk_from_champion_loss_pct=1.0,
                        internal_champion_strength_score=0.0)
        assert s <= 100.0

    def test_max_case(self):
        s = self._score(champion_last_active_days_avg=30.0,
                        deals_at_risk_from_champion_loss_pct=1.0,
                        internal_champion_strength_score=0.0)
        assert s == 100.0

    def test_zero_risk(self):
        s = self._score(champion_last_active_days_avg=1.0,
                        deals_at_risk_from_champion_loss_pct=0.0,
                        internal_champion_strength_score=0.90)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 6. _decision_maker_coverage_score tests
# ---------------------------------------------------------------------------

class TestDecisionMakerCoverageScore:
    def _score(self, **kw):
        eng = make_engine()
        return eng._decision_maker_coverage_score(make_input(**kw))

    # economic_buyer_engaged_pct tiers
    def test_economic_below_30(self):
        s = self._score(economic_buyer_engaged_pct=0.10,
                        deals_with_decision_maker_pct=0.90,
                        technical_buyer_engaged_pct=0.90)
        assert s == 40.0

    def test_economic_30_to_49(self):
        s = self._score(economic_buyer_engaged_pct=0.30,
                        deals_with_decision_maker_pct=0.90,
                        technical_buyer_engaged_pct=0.90)
        assert s == 20.0

    def test_economic_50_to_69(self):
        s = self._score(economic_buyer_engaged_pct=0.50,
                        deals_with_decision_maker_pct=0.90,
                        technical_buyer_engaged_pct=0.90)
        assert s == 8.0

    def test_economic_70_plus(self):
        s = self._score(economic_buyer_engaged_pct=0.70,
                        deals_with_decision_maker_pct=0.90,
                        technical_buyer_engaged_pct=0.90)
        assert s == 0.0

    # deals_with_decision_maker_pct tiers
    def test_dm_below_30(self):
        s = self._score(economic_buyer_engaged_pct=0.90,
                        deals_with_decision_maker_pct=0.10,
                        technical_buyer_engaged_pct=0.90)
        assert s == 35.0

    def test_dm_30_to_49(self):
        s = self._score(economic_buyer_engaged_pct=0.90,
                        deals_with_decision_maker_pct=0.30,
                        technical_buyer_engaged_pct=0.90)
        assert s == 18.0

    def test_dm_50_plus(self):
        s = self._score(economic_buyer_engaged_pct=0.90,
                        deals_with_decision_maker_pct=0.50,
                        technical_buyer_engaged_pct=0.90)
        assert s == 0.0

    # technical_buyer_engaged_pct tiers
    def test_technical_below_20(self):
        s = self._score(economic_buyer_engaged_pct=0.90,
                        deals_with_decision_maker_pct=0.90,
                        technical_buyer_engaged_pct=0.10)
        assert s == 25.0

    def test_technical_20_to_39(self):
        s = self._score(economic_buyer_engaged_pct=0.90,
                        deals_with_decision_maker_pct=0.90,
                        technical_buyer_engaged_pct=0.20)
        assert s == 12.0

    def test_technical_40_plus(self):
        s = self._score(economic_buyer_engaged_pct=0.90,
                        deals_with_decision_maker_pct=0.90,
                        technical_buyer_engaged_pct=0.40)
        assert s == 0.0

    def test_capped_at_100(self):
        s = self._score(economic_buyer_engaged_pct=0.0,
                        deals_with_decision_maker_pct=0.0,
                        technical_buyer_engaged_pct=0.0)
        assert s <= 100.0

    def test_max_case(self):
        s = self._score(economic_buyer_engaged_pct=0.0,
                        deals_with_decision_maker_pct=0.0,
                        technical_buyer_engaged_pct=0.0)
        assert s == 100.0

    def test_zero_risk(self):
        s = self._score(economic_buyer_engaged_pct=0.90,
                        deals_with_decision_maker_pct=0.90,
                        technical_buyer_engaged_pct=0.90)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 7. _relationship_map_score tests
# ---------------------------------------------------------------------------

class TestRelationshipMapScore:
    def _score(self, **kw):
        eng = make_engine()
        return eng._relationship_map_score(make_input(**kw))

    # stakeholder_map_completion_pct tiers
    def test_map_below_25(self):
        s = self._score(stakeholder_map_completion_pct=0.10,
                        avg_contacts_added_per_month=5.0,
                        avg_days_since_secondary_contact=3.0)
        assert s == 40.0

    def test_map_25_to_49(self):
        s = self._score(stakeholder_map_completion_pct=0.25,
                        avg_contacts_added_per_month=5.0,
                        avg_days_since_secondary_contact=3.0)
        assert s == 20.0

    def test_map_50_to_74(self):
        s = self._score(stakeholder_map_completion_pct=0.50,
                        avg_contacts_added_per_month=5.0,
                        avg_days_since_secondary_contact=3.0)
        assert s == 8.0

    def test_map_75_plus(self):
        s = self._score(stakeholder_map_completion_pct=0.75,
                        avg_contacts_added_per_month=5.0,
                        avg_days_since_secondary_contact=3.0)
        assert s == 0.0

    # avg_contacts_added_per_month tiers
    def test_contacts_below_1(self):
        s = self._score(stakeholder_map_completion_pct=1.0,
                        avg_contacts_added_per_month=0.5,
                        avg_days_since_secondary_contact=3.0)
        assert s == 35.0

    def test_contacts_1_to_2(self):
        s = self._score(stakeholder_map_completion_pct=1.0,
                        avg_contacts_added_per_month=1.0,
                        avg_days_since_secondary_contact=3.0)
        assert s == 18.0

    def test_contacts_3_plus(self):
        s = self._score(stakeholder_map_completion_pct=1.0,
                        avg_contacts_added_per_month=3.0,
                        avg_days_since_secondary_contact=3.0)
        assert s == 0.0

    # avg_days_since_secondary_contact tiers
    def test_secondary_contact_below_14(self):
        s = self._score(stakeholder_map_completion_pct=1.0,
                        avg_contacts_added_per_month=5.0,
                        avg_days_since_secondary_contact=5.0)
        assert s == 0.0

    def test_secondary_contact_14_to_29(self):
        s = self._score(stakeholder_map_completion_pct=1.0,
                        avg_contacts_added_per_month=5.0,
                        avg_days_since_secondary_contact=14.0)
        assert s == 12.0

    def test_secondary_contact_30_plus(self):
        s = self._score(stakeholder_map_completion_pct=1.0,
                        avg_contacts_added_per_month=5.0,
                        avg_days_since_secondary_contact=30.0)
        assert s == 25.0

    def test_capped_at_100(self):
        s = self._score(stakeholder_map_completion_pct=0.0,
                        avg_contacts_added_per_month=0.0,
                        avg_days_since_secondary_contact=100.0)
        assert s <= 100.0

    def test_max_case(self):
        s = self._score(stakeholder_map_completion_pct=0.0,
                        avg_contacts_added_per_month=0.0,
                        avg_days_since_secondary_contact=100.0)
        assert s == 100.0

    def test_zero_risk(self):
        s = self._score(stakeholder_map_completion_pct=1.0,
                        avg_contacts_added_per_month=5.0,
                        avg_days_since_secondary_contact=5.0)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 8. _detect_pattern tests
# ---------------------------------------------------------------------------

class TestDetectPattern:
    def _pattern(self, inp, breadth, champion, decision, relationship):
        return make_engine()._detect_pattern(inp, breadth, champion, decision, relationship)

    def test_none_pattern(self):
        inp = make_input()
        p = self._pattern(inp, 5.0, 5.0, 5.0, 5.0)
        assert p == MultithreadPattern.none

    def test_single_threading_pattern(self):
        inp = make_input(single_threaded_deals_pct=0.60)
        p = self._pattern(inp, 40.0, 10.0, 10.0, 10.0)
        assert p == MultithreadPattern.single_threading

    def test_single_threading_requires_breadth_ge_35(self):
        inp = make_input(single_threaded_deals_pct=0.60)
        p = self._pattern(inp, 34.9, 10.0, 10.0, 10.0)
        assert p != MultithreadPattern.single_threading

    def test_single_threading_requires_pct_ge_50(self):
        inp = make_input(single_threaded_deals_pct=0.49)
        p = self._pattern(inp, 40.0, 10.0, 10.0, 10.0)
        assert p != MultithreadPattern.single_threading

    def test_champion_dependency_pattern(self):
        inp = make_input(deals_at_risk_from_champion_loss_pct=0.50)
        p = self._pattern(inp, 10.0, 40.0, 10.0, 10.0)
        assert p == MultithreadPattern.champion_dependency

    def test_champion_dependency_requires_champion_ge_35(self):
        inp = make_input(deals_at_risk_from_champion_loss_pct=0.50)
        p = self._pattern(inp, 10.0, 34.9, 10.0, 10.0)
        assert p != MultithreadPattern.champion_dependency

    def test_champion_dependency_requires_at_risk_ge_40(self):
        inp = make_input(deals_at_risk_from_champion_loss_pct=0.39)
        p = self._pattern(inp, 10.0, 40.0, 10.0, 10.0)
        assert p != MultithreadPattern.champion_dependency

    def test_executive_blind_spot_pattern(self):
        inp = make_input(executive_sponsor_engaged_pct=0.20)
        p = self._pattern(inp, 10.0, 10.0, 35.0, 10.0)
        assert p == MultithreadPattern.executive_blind_spot

    def test_executive_blind_spot_requires_decision_ge_30(self):
        inp = make_input(executive_sponsor_engaged_pct=0.20)
        p = self._pattern(inp, 10.0, 10.0, 29.9, 10.0)
        assert p != MultithreadPattern.executive_blind_spot

    def test_executive_blind_spot_requires_exec_pct_lt_25(self):
        inp = make_input(executive_sponsor_engaged_pct=0.25)
        p = self._pattern(inp, 10.0, 10.0, 35.0, 10.0)
        assert p != MultithreadPattern.executive_blind_spot

    def test_stakeholder_map_gap_pattern(self):
        inp = make_input(stakeholder_map_completion_pct=0.30)
        p = self._pattern(inp, 10.0, 10.0, 10.0, 35.0)
        assert p == MultithreadPattern.stakeholder_map_gap

    def test_stakeholder_map_gap_requires_rel_ge_30(self):
        inp = make_input(stakeholder_map_completion_pct=0.30)
        p = self._pattern(inp, 10.0, 10.0, 10.0, 29.9)
        assert p != MultithreadPattern.stakeholder_map_gap

    def test_stakeholder_map_gap_requires_map_lt_40(self):
        inp = make_input(stakeholder_map_completion_pct=0.40)
        p = self._pattern(inp, 10.0, 10.0, 10.0, 35.0)
        assert p != MultithreadPattern.stakeholder_map_gap

    def test_relationship_stagnation_pattern(self):
        inp = make_input(avg_contacts_added_per_month=1.0)
        p = self._pattern(inp, 10.0, 10.0, 10.0, 25.0)
        assert p == MultithreadPattern.relationship_stagnation

    def test_relationship_stagnation_requires_rel_ge_20(self):
        inp = make_input(avg_contacts_added_per_month=1.0)
        p = self._pattern(inp, 10.0, 10.0, 10.0, 19.9)
        assert p != MultithreadPattern.relationship_stagnation

    def test_relationship_stagnation_requires_contacts_lt_1_5(self):
        inp = make_input(avg_contacts_added_per_month=1.5)
        p = self._pattern(inp, 10.0, 10.0, 10.0, 25.0)
        assert p != MultithreadPattern.relationship_stagnation

    def test_single_threading_takes_priority_over_champion(self):
        # breadth >= 35 + pct >= 50 should win over champion
        inp = make_input(single_threaded_deals_pct=0.60,
                         deals_at_risk_from_champion_loss_pct=0.50)
        p = self._pattern(inp, 40.0, 40.0, 10.0, 10.0)
        assert p == MultithreadPattern.single_threading


# ---------------------------------------------------------------------------
# 9. _risk_level tests
# ---------------------------------------------------------------------------

class TestRiskLevel:
    def _risk(self, composite):
        return make_engine()._risk_level(composite)

    def test_below_20_is_low(self):
        assert self._risk(0.0) == MultithreadRisk.low
        assert self._risk(19.9) == MultithreadRisk.low

    def test_exactly_20_is_moderate(self):
        assert self._risk(20.0) == MultithreadRisk.moderate

    def test_20_to_39_is_moderate(self):
        assert self._risk(39.9) == MultithreadRisk.moderate

    def test_exactly_40_is_high(self):
        assert self._risk(40.0) == MultithreadRisk.high

    def test_40_to_59_is_high(self):
        assert self._risk(59.9) == MultithreadRisk.high

    def test_exactly_60_is_critical(self):
        assert self._risk(60.0) == MultithreadRisk.critical

    def test_above_60_is_critical(self):
        assert self._risk(100.0) == MultithreadRisk.critical


# ---------------------------------------------------------------------------
# 10. _severity tests
# ---------------------------------------------------------------------------

class TestSeverity:
    def _sev(self, composite):
        return make_engine()._severity(composite)

    def test_below_20_is_networked(self):
        assert self._sev(0.0) == MultithreadSeverity.networked
        assert self._sev(19.9) == MultithreadSeverity.networked

    def test_exactly_20_is_developing(self):
        assert self._sev(20.0) == MultithreadSeverity.developing

    def test_20_to_39_is_developing(self):
        assert self._sev(39.9) == MultithreadSeverity.developing

    def test_exactly_40_is_exposed(self):
        assert self._sev(40.0) == MultithreadSeverity.exposed

    def test_40_to_59_is_exposed(self):
        assert self._sev(59.9) == MultithreadSeverity.exposed

    def test_exactly_60_is_fragile(self):
        assert self._sev(60.0) == MultithreadSeverity.fragile

    def test_above_60_is_fragile(self):
        assert self._sev(100.0) == MultithreadSeverity.fragile


# ---------------------------------------------------------------------------
# 11. _action tests
# ---------------------------------------------------------------------------

class TestAction:
    def _action(self, risk, pattern):
        return make_engine()._action(risk, pattern)

    def test_low_risk_no_action(self):
        assert self._action(MultithreadRisk.low, MultithreadPattern.none) == MultithreadAction.no_action

    def test_low_risk_any_pattern_no_action(self):
        for p in MultithreadPattern:
            assert self._action(MultithreadRisk.low, p) == MultithreadAction.no_action

    def test_moderate_risk_coaching(self):
        assert self._action(MultithreadRisk.moderate, MultithreadPattern.none) == MultithreadAction.multithread_coaching

    def test_moderate_risk_any_pattern_coaching(self):
        for p in MultithreadPattern:
            assert self._action(MultithreadRisk.moderate, p) == MultithreadAction.multithread_coaching

    def test_high_risk_stakeholder_map_gap(self):
        assert self._action(MultithreadRisk.high, MultithreadPattern.stakeholder_map_gap) == MultithreadAction.stakeholder_mapping_session

    def test_high_risk_relationship_stagnation(self):
        assert self._action(MultithreadRisk.high, MultithreadPattern.relationship_stagnation) == MultithreadAction.relationship_expansion_sprint

    def test_high_risk_other_patterns_coaching(self):
        other_patterns = [
            MultithreadPattern.none,
            MultithreadPattern.single_threading,
            MultithreadPattern.champion_dependency,
            MultithreadPattern.executive_blind_spot,
        ]
        for p in other_patterns:
            assert self._action(MultithreadRisk.high, p) == MultithreadAction.multithread_coaching

    def test_critical_champion_dependency(self):
        assert self._action(MultithreadRisk.critical, MultithreadPattern.champion_dependency) == MultithreadAction.champion_backup_strategy

    def test_critical_executive_blind_spot(self):
        assert self._action(MultithreadRisk.critical, MultithreadPattern.executive_blind_spot) == MultithreadAction.executive_outreach_plan

    def test_critical_other_patterns_coaching(self):
        other_patterns = [
            MultithreadPattern.none,
            MultithreadPattern.single_threading,
            MultithreadPattern.stakeholder_map_gap,
            MultithreadPattern.relationship_stagnation,
        ]
        for p in other_patterns:
            assert self._action(MultithreadRisk.critical, p) == MultithreadAction.multithread_coaching


# ---------------------------------------------------------------------------
# 12. _has_threading_gap tests
# ---------------------------------------------------------------------------

class TestHasThreadingGap:
    def _gap(self, composite, **kw):
        return make_engine()._has_threading_gap(composite, make_input(**kw))

    def test_composite_40_triggers_gap(self):
        assert self._gap(40.0) is True

    def test_composite_39_no_gap_from_composite(self):
        # Only composite check — other defaults are safe
        assert self._gap(39.9,
                         single_threaded_deals_pct=0.10,
                         deals_at_risk_from_champion_loss_pct=0.10) is False

    def test_single_threaded_60_triggers_gap(self):
        assert self._gap(10.0, single_threaded_deals_pct=0.60) is True

    def test_single_threaded_59_no_gap(self):
        assert self._gap(10.0,
                         single_threaded_deals_pct=0.59,
                         deals_at_risk_from_champion_loss_pct=0.10) is False

    def test_at_risk_50_triggers_gap(self):
        assert self._gap(10.0, deals_at_risk_from_champion_loss_pct=0.50) is True

    def test_at_risk_49_no_gap(self):
        assert self._gap(10.0,
                         single_threaded_deals_pct=0.10,
                         deals_at_risk_from_champion_loss_pct=0.49) is False

    def test_all_conditions_false(self):
        assert self._gap(10.0,
                         single_threaded_deals_pct=0.10,
                         deals_at_risk_from_champion_loss_pct=0.10) is False

    def test_composite_exactly_40(self):
        assert self._gap(40.0) is True


# ---------------------------------------------------------------------------
# 13. _requires_multithread_coaching tests
# ---------------------------------------------------------------------------

class TestRequiresMultithreadCoaching:
    def _coach(self, composite, **kw):
        return make_engine()._requires_multithread_coaching(composite, make_input(**kw))

    def test_composite_30_triggers(self):
        assert self._coach(30.0) is True

    def test_composite_29_no_trigger_alone(self):
        assert self._coach(29.9,
                           avg_stakeholders_per_deal=4.0,
                           economic_buyer_engaged_pct=0.80) is False

    def test_avg_stakeholders_below_2_triggers(self):
        assert self._coach(10.0, avg_stakeholders_per_deal=1.5) is True

    def test_avg_stakeholders_exactly_2_no_trigger(self):
        assert self._coach(10.0,
                           avg_stakeholders_per_deal=2.0,
                           economic_buyer_engaged_pct=0.80) is False

    def test_economic_buyer_below_30_triggers(self):
        assert self._coach(10.0, economic_buyer_engaged_pct=0.29) is True

    def test_economic_buyer_exactly_30_no_trigger(self):
        assert self._coach(10.0,
                           avg_stakeholders_per_deal=4.0,
                           economic_buyer_engaged_pct=0.30) is False

    def test_all_false(self):
        assert self._coach(10.0,
                           avg_stakeholders_per_deal=4.0,
                           economic_buyer_engaged_pct=0.80) is False


# ---------------------------------------------------------------------------
# 14. _estimated_at_risk tests
# ---------------------------------------------------------------------------

class TestEstimatedAtRisk:
    def _risk_usd(self, **kw):
        eng = make_engine()
        inp = make_input(**kw)
        composite = eng._threading_breadth_score(inp) * 0.30 \
                  + eng._champion_dependency_score(inp) * 0.30 \
                  + eng._decision_maker_coverage_score(inp) * 0.25 \
                  + eng._relationship_map_score(inp) * 0.15
        return eng._estimated_at_risk(inp, composite)

    def test_zero_single_threaded(self):
        eng = make_engine()
        inp = make_input(total_active_deals=10, single_threaded_deals_pct=0.0,
                         avg_opportunity_value_usd=100000.0)
        assert eng._estimated_at_risk(inp, 50.0) == 0.0

    def test_formula_correctness(self):
        eng = make_engine()
        inp = make_input(total_active_deals=10, single_threaded_deals_pct=0.50,
                         avg_opportunity_value_usd=100000.0)
        # single_threaded = round(10 * 0.50) = 5
        # risk = 5 * 100000 * (50/100) * 0.20 = 50000.0
        result = eng._estimated_at_risk(inp, 50.0)
        assert result == 50000.0

    def test_formula_rounding(self):
        eng = make_engine()
        inp = make_input(total_active_deals=3, single_threaded_deals_pct=0.33,
                         avg_opportunity_value_usd=10000.0)
        # single_threaded = round(3 * 0.33) = round(0.99) = 1
        # risk = 1 * 10000 * (40/100) * 0.20 = 800.0
        result = eng._estimated_at_risk(inp, 40.0)
        assert result == 800.0

    def test_zero_composite(self):
        eng = make_engine()
        inp = make_input(total_active_deals=20, single_threaded_deals_pct=0.50,
                         avg_opportunity_value_usd=50000.0)
        assert eng._estimated_at_risk(inp, 0.0) == 0.0

    def test_returns_float(self):
        eng = make_engine()
        inp = make_input()
        result = eng._estimated_at_risk(inp, 50.0)
        assert isinstance(result, float)


# ---------------------------------------------------------------------------
# 15. _signal tests
# ---------------------------------------------------------------------------

class TestSignal:
    def _signal(self, pattern, composite, **kw):
        eng = make_engine()
        inp = make_input(**kw)
        return eng._signal(inp, pattern, composite)

    def test_healthy_benchmark_signal(self):
        sig = self._signal(MultithreadPattern.none, 10.0,
                           single_threaded_deals_pct=0.10,
                           executive_sponsor_engaged_pct=0.80,
                           deals_at_risk_from_champion_loss_pct=0.05)
        assert sig == "Stakeholder coverage healthy — multi-threading, champion strength, and executive access within benchmarks"

    def test_healthy_benchmark_exact_boundary(self):
        sig = self._signal(MultithreadPattern.none, 19.9)
        assert "healthy" in sig

    def test_not_healthy_when_composite_ge_20(self):
        sig = self._signal(MultithreadPattern.none, 20.0)
        assert "healthy" not in sig

    def test_not_healthy_when_pattern_not_none(self):
        sig = self._signal(MultithreadPattern.single_threading, 10.0)
        assert "healthy" not in sig

    def test_signal_contains_composite(self):
        sig = self._signal(MultithreadPattern.single_threading, 45.0,
                           single_threaded_deals_pct=0.60,
                           executive_sponsor_engaged_pct=0.30,
                           deals_at_risk_from_champion_loss_pct=0.20)
        assert "45" in sig

    def test_signal_contains_single_threaded_pct(self):
        sig = self._signal(MultithreadPattern.single_threading, 45.0,
                           single_threaded_deals_pct=0.60,
                           executive_sponsor_engaged_pct=0.30,
                           deals_at_risk_from_champion_loss_pct=0.20)
        assert "60%" in sig

    def test_signal_contains_executive_pct(self):
        sig = self._signal(MultithreadPattern.single_threading, 45.0,
                           single_threaded_deals_pct=0.60,
                           executive_sponsor_engaged_pct=0.30,
                           deals_at_risk_from_champion_loss_pct=0.20)
        assert "30%" in sig

    def test_signal_contains_champion_risk_pct(self):
        sig = self._signal(MultithreadPattern.single_threading, 45.0,
                           single_threaded_deals_pct=0.60,
                           executive_sponsor_engaged_pct=0.30,
                           deals_at_risk_from_champion_loss_pct=0.20)
        assert "20%" in sig

    def test_signal_label_from_pattern(self):
        sig = self._signal(MultithreadPattern.champion_dependency, 50.0,
                           single_threaded_deals_pct=0.30,
                           executive_sponsor_engaged_pct=0.30,
                           deals_at_risk_from_champion_loss_pct=0.30)
        assert "Champion dependency" in sig

    def test_signal_threading_risk_label_when_no_pattern(self):
        sig = self._signal(MultithreadPattern.none, 25.0,
                           single_threaded_deals_pct=0.30,
                           executive_sponsor_engaged_pct=0.30,
                           deals_at_risk_from_champion_loss_pct=0.10)
        assert "Threading risk" in sig

    def test_signal_stakeholder_coverage_declining_when_all_at_1(self):
        sig = self._signal(MultithreadPattern.none, 25.0,
                           single_threaded_deals_pct=1.0,
                           executive_sponsor_engaged_pct=1.0,
                           deals_at_risk_from_champion_loss_pct=1.0)
        assert "stakeholder coverage declining" in sig


# ---------------------------------------------------------------------------
# 16. assess() end-to-end tests
# ---------------------------------------------------------------------------

class TestAssess:
    def test_returns_multithread_result(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result, MultithreadResult)

    def test_rep_id_propagated(self, engine):
        result = engine.assess(make_input(rep_id="X-42"))
        assert result.rep_id == "X-42"

    def test_region_propagated(self, engine):
        result = engine.assess(make_input(region="APAC"))
        assert result.region == "APAC"

    def test_healthy_is_low_risk(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.multithread_risk == MultithreadRisk.low

    def test_healthy_is_networked(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.multithread_severity == MultithreadSeverity.networked

    def test_healthy_no_action(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.recommended_action == MultithreadAction.no_action

    def test_healthy_no_gap(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.has_threading_gap is False

    def test_scores_are_floats(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert all(isinstance(v, float) for v in [
            r.threading_breadth_score, r.champion_dependency_score,
            r.decision_maker_coverage_score, r.relationship_map_score,
            r.multithread_composite,
        ])

    def test_composite_formula(self, engine):
        """composite = breadth*0.30 + champion*0.30 + decision*0.25 + rel*0.15"""
        inp = make_input()
        r = engine.assess(inp)
        expected = round(
            r.threading_breadth_score * 0.30
            + r.champion_dependency_score * 0.30
            + r.decision_maker_coverage_score * 0.25
            + r.relationship_map_score * 0.15, 1
        )
        assert r.multithread_composite == min(expected, 100.0)

    def test_composite_capped_at_100(self, engine):
        # Maximize all sub-scores
        inp = make_input(
            single_threaded_deals_pct=1.0,
            avg_stakeholders_per_deal=1.0,
            executive_sponsor_engaged_pct=0.0,
            champion_last_active_days_avg=30.0,
            deals_at_risk_from_champion_loss_pct=1.0,
            internal_champion_strength_score=0.0,
            economic_buyer_engaged_pct=0.0,
            deals_with_decision_maker_pct=0.0,
            technical_buyer_engaged_pct=0.0,
            stakeholder_map_completion_pct=0.0,
            avg_contacts_added_per_month=0.0,
            avg_days_since_secondary_contact=100.0,
        )
        r = engine.assess(inp)
        assert r.multithread_composite <= 100.0

    def test_critical_risk_scenario(self, engine):
        inp = make_input(
            single_threaded_deals_pct=0.80,
            avg_stakeholders_per_deal=1.5,
            executive_sponsor_engaged_pct=0.05,
            champion_last_active_days_avg=30.0,
            deals_at_risk_from_champion_loss_pct=0.70,
            internal_champion_strength_score=0.20,
            economic_buyer_engaged_pct=0.10,
            deals_with_decision_maker_pct=0.10,
            technical_buyer_engaged_pct=0.05,
            stakeholder_map_completion_pct=0.10,
            avg_contacts_added_per_month=0.3,
            avg_days_since_secondary_contact=45.0,
        )
        r = engine.assess(inp)
        assert r.multithread_risk == MultithreadRisk.critical
        assert r.multithread_severity == MultithreadSeverity.fragile

    def test_result_stored_in_engine(self, engine, healthy_input):
        engine.assess(healthy_input)
        assert len(engine._results) == 1

    def test_multiple_results_stored(self, engine):
        engine.assess(make_input(rep_id="A"))
        engine.assess(make_input(rep_id="B"))
        assert len(engine._results) == 2

    def test_healthy_signal_benchmark(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.multithread_signal == (
            "Stakeholder coverage healthy — multi-threading, champion strength, "
            "and executive access within benchmarks"
        )

    def test_at_risk_usd_is_nonnegative(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.estimated_at_risk_usd >= 0.0

    def test_pattern_is_multithread_pattern(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.multithread_pattern, MultithreadPattern)


# ---------------------------------------------------------------------------
# 17. assess_batch() tests
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self, engine):
        results = engine.assess_batch([make_input(rep_id="A"), make_input(rep_id="B")])
        assert isinstance(results, list)

    def test_length_matches_input(self, engine):
        inputs = [make_input(rep_id=str(i)) for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_empty_batch(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_all_results_stored(self, engine):
        engine.assess_batch([make_input(rep_id=str(i)) for i in range(3)])
        assert len(engine._results) == 3

    def test_order_preserved(self, engine):
        rep_ids = ["r1", "r2", "r3"]
        inputs = [make_input(rep_id=r) for r in rep_ids]
        results = engine.assess_batch(inputs)
        assert [r.rep_id for r in results] == rep_ids

    def test_each_result_is_multithread_result(self, engine):
        results = engine.assess_batch([make_input(), make_input()])
        for r in results:
            assert isinstance(r, MultithreadResult)

    def test_single_item_batch(self, engine):
        results = engine.assess_batch([make_input(rep_id="solo")])
        assert len(results) == 1
        assert results[0].rep_id == "solo"


# ---------------------------------------------------------------------------
# 18. summary() tests
# ---------------------------------------------------------------------------

class TestSummary:
    def test_empty_engine_summary(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_multithread_composite"] == 0.0
        assert s["threading_gap_count"] == 0
        assert s["coaching_count"] == 0
        assert s["avg_threading_breadth_score"] == 0.0
        assert s["avg_champion_dependency_score"] == 0.0
        assert s["avg_decision_maker_coverage_score"] == 0.0
        assert s["avg_relationship_map_score"] == 0.0
        assert s["total_estimated_at_risk_usd"] == 0.0

    def test_empty_summary_has_13_keys(self, engine):
        assert len(engine.summary()) == 13

    def test_summary_13_keys_after_assess(self, engine):
        engine.assess(make_input())
        assert len(engine.summary()) == 13

    def test_total_count(self, engine):
        engine.assess_batch([make_input(rep_id=str(i)) for i in range(4)])
        assert engine.summary()["total"] == 4

    def test_risk_counts_keys(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert "risk_counts" in s
        # Each key is a valid risk value
        for k in s["risk_counts"]:
            assert k in [r.value for r in MultithreadRisk]

    def test_pattern_counts_keys(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        for k in s["pattern_counts"]:
            assert k in [p.value for p in MultithreadPattern]

    def test_severity_counts_keys(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        for k in s["severity_counts"]:
            assert k in [sv.value for sv in MultithreadSeverity]

    def test_action_counts_keys(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        for k in s["action_counts"]:
            assert k in [a.value for a in MultithreadAction]

    def test_threading_gap_count(self, engine):
        # create one with gap and one without
        engine.assess(make_input(single_threaded_deals_pct=0.70))  # gap
        engine.assess(make_input())  # no gap
        s = engine.summary()
        assert s["threading_gap_count"] >= 1

    def test_coaching_count(self, engine):
        engine.assess(make_input(avg_stakeholders_per_deal=1.5))  # triggers coaching
        engine.assess(make_input())
        s = engine.summary()
        assert s["coaching_count"] >= 1

    def test_avg_composite_is_float(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["avg_multithread_composite"], float)

    def test_total_at_risk_usd_is_float(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["total_estimated_at_risk_usd"], float)

    def test_risk_counts_sum_equals_total(self, engine):
        engine.assess_batch([make_input(rep_id=str(i)) for i in range(5)])
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_severity_counts_sum_equals_total(self, engine):
        engine.assess_batch([make_input(rep_id=str(i)) for i in range(5)])
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_pattern_counts_sum_equals_total(self, engine):
        engine.assess_batch([make_input(rep_id=str(i)) for i in range(5)])
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_action_counts_sum_equals_total(self, engine):
        engine.assess_batch([make_input(rep_id=str(i)) for i in range(5)])
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_single_rep_avg_equals_that_rep(self, engine):
        r = engine.assess(make_input())
        s = engine.summary()
        assert s["avg_multithread_composite"] == r.multithread_composite
        assert s["avg_threading_breadth_score"] == r.threading_breadth_score
        assert s["avg_champion_dependency_score"] == r.champion_dependency_score
        assert s["avg_decision_maker_coverage_score"] == r.decision_maker_coverage_score
        assert s["avg_relationship_map_score"] == r.relationship_map_score

    def test_total_at_risk_sums_correctly(self, engine):
        r1 = engine.assess(make_input(rep_id="A"))
        r2 = engine.assess(make_input(rep_id="B"))
        s = engine.summary()
        assert round(s["total_estimated_at_risk_usd"], 2) == round(r1.estimated_at_risk_usd + r2.estimated_at_risk_usd, 2)

    def test_summary_key_names(self, engine):
        engine.assess(make_input())
        keys = set(engine.summary().keys())
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_multithread_composite", "threading_gap_count",
            "coaching_count", "avg_threading_breadth_score",
            "avg_champion_dependency_score", "avg_decision_maker_coverage_score",
            "avg_relationship_map_score", "total_estimated_at_risk_usd",
        }
        assert keys == expected


# ---------------------------------------------------------------------------
# 19. Composite formula precision tests
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_weights_sum_to_1(self):
        assert abs(0.30 + 0.30 + 0.25 + 0.15 - 1.0) < 1e-9

    def test_zero_composite_when_all_zero(self):
        eng = make_engine()
        inp = make_input(
            single_threaded_deals_pct=0.0,
            avg_stakeholders_per_deal=5.0,
            executive_sponsor_engaged_pct=0.80,
            champion_last_active_days_avg=1.0,
            deals_at_risk_from_champion_loss_pct=0.0,
            internal_champion_strength_score=0.90,
            economic_buyer_engaged_pct=0.90,
            deals_with_decision_maker_pct=0.90,
            technical_buyer_engaged_pct=0.90,
            stakeholder_map_completion_pct=1.0,
            avg_contacts_added_per_month=5.0,
            avg_days_since_secondary_contact=3.0,
        )
        r = eng.assess(inp)
        assert r.multithread_composite == 0.0

    def test_composite_rounded_to_one_decimal(self):
        eng = make_engine()
        r = eng.assess(make_input())
        # result should have at most 1 decimal
        assert r.multithread_composite == round(r.multithread_composite, 1)

    def test_sub_scores_rounded_to_one_decimal(self):
        eng = make_engine()
        r = eng.assess(make_input())
        for score in [r.threading_breadth_score, r.champion_dependency_score,
                      r.decision_maker_coverage_score, r.relationship_map_score]:
            assert score == round(score, 1)


# ---------------------------------------------------------------------------
# 20. Edge case and boundary tests
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_total_deals(self):
        eng = make_engine()
        r = eng.assess(make_input(total_active_deals=0))
        assert r.estimated_at_risk_usd == 0.0

    def test_zero_opportunity_value(self):
        eng = make_engine()
        r = eng.assess(make_input(avg_opportunity_value_usd=0.0))
        assert r.estimated_at_risk_usd == 0.0

    def test_single_active_deal(self):
        eng = make_engine()
        r = eng.assess(make_input(total_active_deals=1))
        assert isinstance(r, MultithreadResult)

    def test_pct_values_at_exact_thresholds(self):
        # single_threaded_deals_pct = 0.30 hits the lowest bucket
        eng = make_engine()
        score = eng._threading_breadth_score(make_input(
            single_threaded_deals_pct=0.30,
            avg_stakeholders_per_deal=5.0,
            executive_sponsor_engaged_pct=0.80,
        ))
        assert score == 10.0

    def test_champion_strength_exact_boundary_40(self):
        eng = make_engine()
        score = eng._champion_dependency_score(make_input(
            champion_last_active_days_avg=1.0,
            deals_at_risk_from_champion_loss_pct=0.0,
            internal_champion_strength_score=0.40,
        ))
        assert score == 12.0

    def test_economic_buyer_exact_boundary_50(self):
        eng = make_engine()
        score = eng._decision_maker_coverage_score(make_input(
            economic_buyer_engaged_pct=0.50,
            deals_with_decision_maker_pct=0.90,
            technical_buyer_engaged_pct=0.90,
        ))
        assert score == 8.0

    def test_stakeholder_map_exact_boundary_50(self):
        eng = make_engine()
        score = eng._relationship_map_score(make_input(
            stakeholder_map_completion_pct=0.50,
            avg_contacts_added_per_month=5.0,
            avg_days_since_secondary_contact=3.0,
        ))
        assert score == 8.0

    def test_all_sub_scores_nonnegative(self):
        eng = make_engine()
        for inp_kwargs in [
            {},
            {"single_threaded_deals_pct": 0.0},
            {"single_threaded_deals_pct": 1.0},
        ]:
            inp = make_input(**inp_kwargs)
            assert eng._threading_breadth_score(inp) >= 0.0
            assert eng._champion_dependency_score(inp) >= 0.0
            assert eng._decision_maker_coverage_score(inp) >= 0.0
            assert eng._relationship_map_score(inp) >= 0.0

    def test_all_sub_scores_at_most_100(self):
        for kwargs in [
            {},
            {"single_threaded_deals_pct": 1.0, "avg_stakeholders_per_deal": 0.5, "executive_sponsor_engaged_pct": 0.0},
        ]:
            eng = make_engine()
            inp = make_input(**kwargs)
            assert eng._threading_breadth_score(inp) <= 100.0
            assert eng._champion_dependency_score(inp) <= 100.0
            assert eng._decision_maker_coverage_score(inp) <= 100.0
            assert eng._relationship_map_score(inp) <= 100.0

    def test_fresh_engine_empty_results(self):
        eng = make_engine()
        assert eng._results == []

    def test_multiple_engines_independent(self):
        eng1 = make_engine()
        eng2 = make_engine()
        eng1.assess(make_input(rep_id="A"))
        assert len(eng2._results) == 0

    def test_assess_accumulates_across_calls(self):
        eng = make_engine()
        for i in range(10):
            eng.assess(make_input(rep_id=str(i)))
        assert len(eng._results) == 10


# ---------------------------------------------------------------------------
# 21. End-to-end scenario tests
# ---------------------------------------------------------------------------

class TestEndToEndScenarios:
    def test_scenario_single_threading_pattern(self):
        """High single-threading should trigger single_threading pattern and coaching."""
        eng = make_engine()
        r = eng.assess(make_input(
            single_threaded_deals_pct=0.75,
            avg_stakeholders_per_deal=1.5,
            executive_sponsor_engaged_pct=0.10,
            champion_last_active_days_avg=5.0,
            deals_at_risk_from_champion_loss_pct=0.20,
            internal_champion_strength_score=0.80,
            economic_buyer_engaged_pct=0.80,
            deals_with_decision_maker_pct=0.80,
            technical_buyer_engaged_pct=0.80,
            stakeholder_map_completion_pct=0.80,
            avg_contacts_added_per_month=3.0,
            avg_days_since_secondary_contact=5.0,
        ))
        assert r.multithread_pattern == MultithreadPattern.single_threading
        assert r.recommended_action != MultithreadAction.no_action

    def test_scenario_champion_dependency_critical(self):
        """Extreme champion risk + other high scores should produce champion_dependency + backup strategy."""
        eng = make_engine()
        # Champion score: 40+35+25=100 -> contributes 30
        # Breadth: 45+30+25=100 -> contributes 30
        # Decision: 40+35+25=100 -> contributes 25
        # Rel: 40+35+25=100 -> contributes 15
        # Composite = 100 -> critical
        r = eng.assess(make_input(
            single_threaded_deals_pct=0.80,        # +45 breadth
            avg_stakeholders_per_deal=1.5,          # +30 breadth
            executive_sponsor_engaged_pct=0.10,     # +25 breadth
            champion_last_active_days_avg=30.0,     # +40 champion
            deals_at_risk_from_champion_loss_pct=0.80,  # +35 champion (>= 0.40 for pattern)
            internal_champion_strength_score=0.10,  # +25 champion
            economic_buyer_engaged_pct=0.10,        # +40 decision
            deals_with_decision_maker_pct=0.10,     # +35 decision
            technical_buyer_engaged_pct=0.10,       # +25 decision
            stakeholder_map_completion_pct=0.10,    # +40 rel
            avg_contacts_added_per_month=0.3,       # +35 rel
            avg_days_since_secondary_contact=40.0,  # +25 rel
        ))
        # single_threading pattern fires first (breadth >= 35 AND pct >= 0.50)
        # but champion_dep fires if breadth check doesn't. Here breadth IS >= 35
        # so single_threading fires. Test that critical risk + champion_dep pattern
        # gives backup strategy by using a scenario that avoids single_threading trigger.
        # Instead boost champion scores only to hit critical composite.
        eng2 = make_engine()
        r = eng2.assess(make_input(
            single_threaded_deals_pct=0.10,         # breadth low
            avg_stakeholders_per_deal=1.5,           # +30 breadth
            executive_sponsor_engaged_pct=0.10,      # +25 breadth -> breadth=55
            champion_last_active_days_avg=30.0,      # +40
            deals_at_risk_from_champion_loss_pct=0.80,  # +35, >=0.40 triggers pattern
            internal_champion_strength_score=0.10,   # +25 -> champion=100
            economic_buyer_engaged_pct=0.10,         # +40
            deals_with_decision_maker_pct=0.10,      # +35
            technical_buyer_engaged_pct=0.10,        # +25 -> decision=100
            stakeholder_map_completion_pct=0.10,     # +40
            avg_contacts_added_per_month=0.3,        # +35
            avg_days_since_secondary_contact=40.0,   # +25 -> rel=100
        ))
        # breadth = 0+30+25=55 (single_threaded=0.10 < 0.30 -> 0, stakeholders <2 -> 30, exec <0.20 -> 25)
        # champion=100, decision=100, rel=100
        # composite = 55*0.30 + 100*0.30 + 100*0.25 + 100*0.15 = 16.5+30+25+15=86.5 -> critical
        # pattern: breadth=55 >= 35 but pct=0.10 < 0.50 -> no single_threading
        # champion=100 >= 35 AND at_risk=0.80 >= 0.40 -> champion_dependency
        assert r.multithread_pattern == MultithreadPattern.champion_dependency
        assert r.multithread_risk == MultithreadRisk.critical
        assert r.recommended_action == MultithreadAction.champion_backup_strategy

    def test_scenario_executive_blind_spot(self):
        """Low executive access + high decision score + critical composite -> exec outreach plan."""
        eng = make_engine()
        # Need: decision >= 30, exec_pct < 0.25, composite >= 60
        # Breadth: pct=0.10 -> 0, stakeholders=4.0 -> 0, exec=0.10 -> 25 => breadth=25
        # Champion: active=7 -> 8, at_risk=0.10 -> 0, strength=0.80 -> 0 => champion=8
        # Decision: economic=0.10 -> 40, dm=0.10 -> 35, tech=0.10 -> 25 => decision=100
        # Rel: map=0.80 -> 0, contacts=3.0 -> 0, days=5.0 -> 0 => rel=0
        # composite = 25*0.30 + 8*0.30 + 100*0.25 + 0*0.15 = 7.5+2.4+25+0 = 34.9 -> high, not critical
        # Boost to get critical: increase breadth and champion too
        r = eng.assess(make_input(
            single_threaded_deals_pct=0.10,         # no single_threading pattern (< 0.50)
            avg_stakeholders_per_deal=1.5,           # +30 breadth
            executive_sponsor_engaged_pct=0.10,      # +25 breadth, < 0.25 for pattern
            champion_last_active_days_avg=25.0,      # +40 champion
            deals_at_risk_from_champion_loss_pct=0.10, # champion_dep needs >= 0.40, keep low
            internal_champion_strength_score=0.30,   # +25 champion -> champion=65
            economic_buyer_engaged_pct=0.10,         # +40 decision
            deals_with_decision_maker_pct=0.10,      # +35 decision
            technical_buyer_engaged_pct=0.10,        # +25 decision -> decision=100
            stakeholder_map_completion_pct=0.80,     # rel low
            avg_contacts_added_per_month=3.0,
            avg_days_since_secondary_contact=5.0,    # rel=0
        ))
        # breadth = 0+30+25=55, champion=65, decision=100, rel=0
        # composite = 55*0.30 + 65*0.30 + 100*0.25 + 0*0.15 = 16.5+19.5+25+0=61 -> critical
        # pattern: breadth=55>=35 but pct=0.10<0.50 -> no single_threading
        # champion=65>=35 but at_risk=0.10<0.40 -> no champion_dep
        # decision=100>=30 and exec=0.10<0.25 -> executive_blind_spot
        assert r.multithread_pattern == MultithreadPattern.executive_blind_spot
        assert r.multithread_risk == MultithreadRisk.critical
        assert r.recommended_action == MultithreadAction.executive_outreach_plan

    def test_scenario_stakeholder_map_gap_high_risk(self):
        """Relationship score >= 30 + map < 0.40 + high composite -> map gap + mapping session."""
        eng = make_engine()
        # Need: relationship >= 30, map < 0.40, composite >= 40 (high risk)
        # Need to avoid single_threading (pct < 0.50) and champion_dep (at_risk < 0.40)
        # and executive_blind_spot (exec >= 0.25 or decision < 30)
        # Rel: map=0.10 -> 40, contacts=0.3 -> 35, days=40 -> 25 = 100
        # Breadth: pct=0.10->0, stakeholders=1.5->30, exec=0.30->12 = 42
        # Champion: active=5->0, at_risk=0.10->0, strength=0.80->0 = 0
        # Decision: economic=0.80->0, dm=0.80->0, tech=0.80->0 = 0
        # composite = 42*0.30 + 0*0.30 + 0*0.25 + 100*0.15 = 12.6+0+0+15=27.6 -> moderate
        # Need higher — boost breadth or champion more
        # Use: pct=0.10->0, stakeholders=1.5->30, exec=0.10->25 = 55 breadth
        # champion: active=15->22, at_risk=0.10->0, strength=0.45->12 = 34
        # decision: all good -> 0
        # rel: 40+35+25=100
        # composite = 55*0.30+34*0.30+0*0.25+100*0.15=16.5+10.2+0+15=41.7 -> high
        # pattern: breadth=55>=35, pct=0.10<0.50 -> no single_threading
        # champion=34<35 -> no champion_dep
        # decision=0<30 -> no exec_blind_spot
        # rel=100>=30, map=0.10<0.40 -> stakeholder_map_gap
        r = eng.assess(make_input(
            single_threaded_deals_pct=0.10,
            avg_stakeholders_per_deal=1.5,
            executive_sponsor_engaged_pct=0.10,
            champion_last_active_days_avg=15.0,
            deals_at_risk_from_champion_loss_pct=0.10,
            internal_champion_strength_score=0.45,
            economic_buyer_engaged_pct=0.80,
            deals_with_decision_maker_pct=0.80,
            technical_buyer_engaged_pct=0.80,
            stakeholder_map_completion_pct=0.10,
            avg_contacts_added_per_month=0.3,
            avg_days_since_secondary_contact=40.0,
        ))
        assert r.multithread_pattern == MultithreadPattern.stakeholder_map_gap
        assert r.multithread_risk == MultithreadRisk.high
        assert r.recommended_action == MultithreadAction.stakeholder_mapping_session

    def test_scenario_relationship_stagnation_high_risk(self):
        """Relationship stagnation pattern + high composite -> relationship_expansion_sprint."""
        eng = make_engine()
        # Need: rel >= 20, contacts < 1.5, composite >= 40 (high risk)
        # Avoid other patterns: pct<0.50, at_risk<0.40, exec>=0.25 or decision<30, map>=0.40
        # rel: map=0.55 -> 8, contacts=1.0 -> 18, days=20 -> 12 = 38 (>= 20, contacts < 1.5)
        # Boost breadth and champion to reach composite >= 40
        # Breadth: pct=0.10->0, stakeholders=1.5->30, exec=0.10->25 = 55
        # Champion: active=15->22, at_risk=0.10->0, strength=0.45->12 = 34
        # Decision: all good -> 0
        # composite = 55*0.30+34*0.30+0*0.25+38*0.15=16.5+10.2+0+5.7=32.4 -> moderate
        # need higher: boost champion a bit more
        # champion: active=15->22, at_risk=0.29->0 (still<0.30), strength=0.35->25=47
        # composite = 55*0.30+47*0.30+0*0.25+38*0.15=16.5+14.1+0+5.7=36.3 -> moderate
        # still not high. Add decision score contribution:
        # decision: economic=0.40->20, dm=0.40->18, tech=0.30->12=50
        # composite = 55*0.30+47*0.30+50*0.25+38*0.15=16.5+14.1+12.5+5.7=48.8 -> high
        # pattern: breadth=55>=35, pct=0.10<0.50 -> no single_threading
        # champion=47>=35, at_risk=0.29<0.40 -> no champion_dep
        # decision=50>=30, exec=0.10<0.25 -> executive_blind_spot fires BEFORE stagnation
        # Avoid blind spot: keep exec >= 0.25
        # exec=0.25 -> breadth: pct=0.10->0, stakeholders=1.5->30, exec=0.25->12=42
        # composite = 42*0.30+47*0.30+50*0.25+38*0.15=12.6+14.1+12.5+5.7=44.9 -> high
        # pattern: breadth=42>=35, pct<0.50 -> no single_threading
        # champion=47>=35, at_risk<0.40 -> no champion_dep
        # decision=50>=30, exec=0.25 (NOT < 0.25) -> no exec_blind_spot
        # rel=38>=30, map=0.55>=0.40 -> no stakeholder_map_gap
        # rel=38>=20, contacts=1.0<1.5 -> relationship_stagnation ✓
        r = eng.assess(make_input(
            single_threaded_deals_pct=0.10,
            avg_stakeholders_per_deal=1.5,
            executive_sponsor_engaged_pct=0.25,
            champion_last_active_days_avg=15.0,
            deals_at_risk_from_champion_loss_pct=0.29,
            internal_champion_strength_score=0.35,
            economic_buyer_engaged_pct=0.40,
            deals_with_decision_maker_pct=0.40,
            technical_buyer_engaged_pct=0.30,
            stakeholder_map_completion_pct=0.55,
            avg_contacts_added_per_month=1.0,
            avg_days_since_secondary_contact=20.0,
        ))
        assert r.multithread_pattern == MultithreadPattern.relationship_stagnation
        assert r.multithread_risk == MultithreadRisk.high
        assert r.recommended_action == MultithreadAction.relationship_expansion_sprint

    def test_scenario_batch_summary_consistency(self):
        eng = make_engine()
        inputs = [
            make_input(rep_id="A", single_threaded_deals_pct=0.80),
            make_input(rep_id="B"),
            make_input(rep_id="C", champion_last_active_days_avg=30.0,
                       deals_at_risk_from_champion_loss_pct=0.70,
                       internal_champion_strength_score=0.20),
        ]
        results = eng.assess_batch(inputs)
        s = eng.summary()
        assert s["total"] == 3
        assert sum(s["risk_counts"].values()) == 3
        assert s["total_estimated_at_risk_usd"] == round(
            sum(r.estimated_at_risk_usd for r in results), 2
        )

    def test_to_dict_round_trip(self):
        eng = make_engine()
        r = eng.assess(make_input())
        d = r.to_dict()
        assert d["rep_id"] == r.rep_id
        assert d["region"] == r.region
        assert d["multithread_risk"] == r.multithread_risk.value
        assert d["multithread_pattern"] == r.multithread_pattern.value
        assert d["multithread_severity"] == r.multithread_severity.value
        assert d["recommended_action"] == r.recommended_action.value
        assert d["threading_breadth_score"] == r.threading_breadth_score
        assert d["champion_dependency_score"] == r.champion_dependency_score
        assert d["decision_maker_coverage_score"] == r.decision_maker_coverage_score
        assert d["relationship_map_score"] == r.relationship_map_score
        assert d["multithread_composite"] == r.multithread_composite
        assert d["has_threading_gap"] == r.has_threading_gap
        assert d["requires_multithread_coaching"] == r.requires_multithread_coaching
        assert d["estimated_at_risk_usd"] == r.estimated_at_risk_usd
        assert d["multithread_signal"] == r.multithread_signal

    def test_high_value_deal_large_at_risk(self):
        eng = make_engine()
        r = eng.assess(make_input(
            total_active_deals=50,
            single_threaded_deals_pct=0.80,
            avg_opportunity_value_usd=500000.0,
            avg_stakeholders_per_deal=1.5,
            executive_sponsor_engaged_pct=0.05,
        ))
        assert r.estimated_at_risk_usd > 0.0

    def test_multiple_regions(self):
        eng = make_engine()
        for region in ["North", "South", "East", "West"]:
            eng.assess(make_input(region=region))
        s = eng.summary()
        assert s["total"] == 4

    def test_coaching_count_increments_correctly(self):
        eng = make_engine()
        eng.assess(make_input(avg_stakeholders_per_deal=1.5))  # should coach
        eng.assess(make_input())  # healthy, depends on composite
        s = eng.summary()
        # The first one definitely should require coaching
        assert s["coaching_count"] >= 1
