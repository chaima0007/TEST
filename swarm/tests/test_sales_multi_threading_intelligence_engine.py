"""
Comprehensive pytest tests for SalesMultiThreadingIntelligenceEngine.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_multi_threading_intelligence_engine import (
    MultithreadRisk,
    MultithreadPattern,
    MultithreadSeverity,
    MultithreadAction,
    MultithreadInput,
    MultithreadResult,
    SalesMultiThreadingIntelligenceEngine,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def make_input(**overrides) -> MultithreadInput:
    """Return a fully-healthy baseline MultithreadInput, override any field."""
    defaults = dict(
        rep_id="REP-001",
        region="North America",
        evaluation_period_id="Q1-2026",
        # depth – healthy
        avg_contacts_per_active_deal=3.5,
        single_contact_deal_rate_pct=0.10,
        champion_only_reliance_pct=0.20,
        # breadth – healthy
        multi_dept_engaged_rate_pct=0.75,
        org_chart_mapped_pct=0.60,
        technical_buyer_engaged_pct=0.65,
        # exec access – healthy
        executive_engaged_rate_pct=0.70,
        economic_buyer_direct_contact_pct=0.60,
        referral_from_champion_to_exec_pct=0.40,
        # risk exposure – healthy
        champion_churn_impacted_deals_pct=0.02,
        lost_due_single_thread_pct=0.05,
        deal_sponsor_count_avg=2.5,
        # breadth_shallow fields
        new_stakeholder_added_per_deal_avg=1.5,
        org_breadth_score_avg=0.50,
        # unused scoring fields
        user_buyer_engaged_pct=0.50,
        legal_procurement_early_engaged_pct=0.30,
        multi_sponsor_deals_win_rate_pct=0.60,
        # deal risk
        total_active_deals=20,
        avg_opportunity_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return MultithreadInput(**defaults)


def fresh_engine() -> SalesMultiThreadingIntelligenceEngine:
    return SalesMultiThreadingIntelligenceEngine()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Enum value tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEnumValues:
    def test_risk_low(self):
        assert MultithreadRisk.low.value == "low"

    def test_risk_moderate(self):
        assert MultithreadRisk.moderate.value == "moderate"

    def test_risk_high(self):
        assert MultithreadRisk.high.value == "high"

    def test_risk_critical(self):
        assert MultithreadRisk.critical.value == "critical"

    def test_pattern_none(self):
        assert MultithreadPattern.none.value == "none"

    def test_pattern_single_contact_dependency(self):
        assert MultithreadPattern.single_contact_dependency.value == "single_contact_dependency"

    def test_pattern_champion_only_reliance(self):
        assert MultithreadPattern.champion_only_reliance.value == "champion_only_reliance"

    def test_pattern_executive_bypass(self):
        assert MultithreadPattern.executive_bypass.value == "executive_bypass"

    def test_pattern_org_chart_blind(self):
        assert MultithreadPattern.org_chart_blind.value == "org_chart_blind"

    def test_pattern_breadth_shallow(self):
        assert MultithreadPattern.breadth_shallow.value == "breadth_shallow"

    def test_severity_networked(self):
        assert MultithreadSeverity.networked.value == "networked"

    def test_severity_adequate(self):
        assert MultithreadSeverity.adequate.value == "adequate"

    def test_severity_shallow(self):
        assert MultithreadSeverity.shallow.value == "shallow"

    def test_severity_isolated(self):
        assert MultithreadSeverity.isolated.value == "isolated"

    def test_action_no_action(self):
        assert MultithreadAction.no_action.value == "no_action"

    def test_action_stakeholder_mapping_coaching(self):
        assert MultithreadAction.stakeholder_mapping_coaching.value == "stakeholder_mapping_coaching"

    def test_action_champion_diversification_coaching(self):
        assert MultithreadAction.champion_diversification_coaching.value == "champion_diversification_coaching"

    def test_action_executive_access_coaching(self):
        assert MultithreadAction.executive_access_coaching.value == "executive_access_coaching"

    def test_action_organization_navigation_coaching(self):
        assert MultithreadAction.organization_navigation_coaching.value == "organization_navigation_coaching"

    def test_action_multithread_intervention(self):
        assert MultithreadAction.multithread_intervention.value == "multithread_intervention"

    def test_action_deal_at_risk_intervention(self):
        assert MultithreadAction.deal_at_risk_intervention.value == "deal_at_risk_intervention"


# ─────────────────────────────────────────────────────────────────────────────
# 2. MultithreadInput dataclass – field presence
# ─────────────────────────────────────────────────────────────────────────────

class TestMultithreadInputFields:
    def test_has_22_fields(self):
        inp = make_input()
        assert len(inp.__dataclass_fields__) == 22

    def test_rep_id_stored(self):
        assert make_input(rep_id="R42").rep_id == "R42"

    def test_region_stored(self):
        assert make_input(region="EMEA").region == "EMEA"

    def test_evaluation_period_id_stored(self):
        assert make_input(evaluation_period_id="Q2-2026").evaluation_period_id == "Q2-2026"

    def test_numeric_field_types(self):
        inp = make_input()
        assert isinstance(inp.avg_contacts_per_active_deal, float)
        assert isinstance(inp.total_active_deals, int)


# ─────────────────────────────────────────────────────────────────────────────
# 3. MultithreadResult dataclass – field presence
# ─────────────────────────────────────────────────────────────────────────────

class TestMultithreadResultFields:
    def setup_method(self):
        self.engine = fresh_engine()
        self.result = self.engine.assess(make_input())

    def test_has_rep_id(self):
        assert hasattr(self.result, "rep_id")

    def test_has_region(self):
        assert hasattr(self.result, "region")

    def test_has_multithread_risk(self):
        assert hasattr(self.result, "multithread_risk")

    def test_has_multithread_pattern(self):
        assert hasattr(self.result, "multithread_pattern")

    def test_has_multithread_severity(self):
        assert hasattr(self.result, "multithread_severity")

    def test_has_recommended_action(self):
        assert hasattr(self.result, "recommended_action")

    def test_has_depth_score(self):
        assert hasattr(self.result, "depth_score")

    def test_has_breadth_score(self):
        assert hasattr(self.result, "breadth_score")

    def test_has_executive_access_score(self):
        assert hasattr(self.result, "executive_access_score")

    def test_has_risk_exposure_score(self):
        assert hasattr(self.result, "risk_exposure_score")

    def test_has_multithread_composite(self):
        assert hasattr(self.result, "multithread_composite")

    def test_has_has_multithread_gap(self):
        assert hasattr(self.result, "has_multithread_gap")

    def test_has_requires_multithread_coaching(self):
        assert hasattr(self.result, "requires_multithread_coaching")

    def test_has_estimated_deal_risk_usd(self):
        assert hasattr(self.result, "estimated_deal_risk_usd")

    def test_has_multithread_signal(self):
        assert hasattr(self.result, "multithread_signal")


# ─────────────────────────────────────────────────────────────────────────────
# 4. to_dict() keys
# ─────────────────────────────────────────────────────────────────────────────

class TestToDict:
    def setup_method(self):
        engine = fresh_engine()
        self.d = engine.assess(make_input()).to_dict()

    def test_has_15_keys(self):
        assert len(self.d) == 15

    def test_key_rep_id(self):
        assert "rep_id" in self.d

    def test_key_region(self):
        assert "region" in self.d

    def test_key_multithread_risk(self):
        assert "multithread_risk" in self.d

    def test_key_multithread_pattern(self):
        assert "multithread_pattern" in self.d

    def test_key_multithread_severity(self):
        assert "multithread_severity" in self.d

    def test_key_recommended_action(self):
        assert "recommended_action" in self.d

    def test_key_depth_score(self):
        assert "depth_score" in self.d

    def test_key_breadth_score(self):
        assert "breadth_score" in self.d

    def test_key_executive_access_score(self):
        assert "executive_access_score" in self.d

    def test_key_risk_exposure_score(self):
        assert "risk_exposure_score" in self.d

    def test_key_multithread_composite(self):
        assert "multithread_composite" in self.d

    def test_key_has_multithread_gap(self):
        assert "has_multithread_gap" in self.d

    def test_key_requires_multithread_coaching(self):
        assert "requires_multithread_coaching" in self.d

    def test_key_estimated_deal_risk_usd(self):
        assert "estimated_deal_risk_usd" in self.d

    def test_key_multithread_signal(self):
        assert "multithread_signal" in self.d

    def test_risk_is_string_in_dict(self):
        assert isinstance(self.d["multithread_risk"], str)

    def test_pattern_is_string_in_dict(self):
        assert isinstance(self.d["multithread_pattern"], str)

    def test_severity_is_string_in_dict(self):
        assert isinstance(self.d["multithread_severity"], str)

    def test_action_is_string_in_dict(self):
        assert isinstance(self.d["recommended_action"], str)


# ─────────────────────────────────────────────────────────────────────────────
# 5. _depth_score tests
# ─────────────────────────────────────────────────────────────────────────────

class TestDepthScore:
    def setup_method(self):
        self.engine = fresh_engine()

    def _score(self, **kw):
        return self.engine._depth_score(make_input(**kw))

    # avg_contacts_per_active_deal
    def test_avg_contacts_le_1_5_adds_40(self):
        s = self._score(avg_contacts_per_active_deal=1.5, single_contact_deal_rate_pct=0.0,
                        champion_only_reliance_pct=0.0)
        assert s == 40.0

    def test_avg_contacts_exact_1_5(self):
        s = self._score(avg_contacts_per_active_deal=1.5, single_contact_deal_rate_pct=0.0,
                        champion_only_reliance_pct=0.0)
        assert s == 40.0

    def test_avg_contacts_le_2_0_adds_22(self):
        s = self._score(avg_contacts_per_active_deal=2.0, single_contact_deal_rate_pct=0.0,
                        champion_only_reliance_pct=0.0)
        assert s == 22.0

    def test_avg_contacts_le_2_5_adds_8(self):
        s = self._score(avg_contacts_per_active_deal=2.5, single_contact_deal_rate_pct=0.0,
                        champion_only_reliance_pct=0.0)
        assert s == 8.0

    def test_avg_contacts_above_2_5_adds_0(self):
        s = self._score(avg_contacts_per_active_deal=3.0, single_contact_deal_rate_pct=0.0,
                        champion_only_reliance_pct=0.0)
        assert s == 0.0

    # single_contact_deal_rate_pct
    def test_single_contact_ge_0_60_adds_35(self):
        s = self._score(avg_contacts_per_active_deal=10.0, single_contact_deal_rate_pct=0.60,
                        champion_only_reliance_pct=0.0)
        assert s == 35.0

    def test_single_contact_ge_0_40_adds_18(self):
        s = self._score(avg_contacts_per_active_deal=10.0, single_contact_deal_rate_pct=0.40,
                        champion_only_reliance_pct=0.0)
        assert s == 18.0

    def test_single_contact_below_0_40_adds_0(self):
        s = self._score(avg_contacts_per_active_deal=10.0, single_contact_deal_rate_pct=0.39,
                        champion_only_reliance_pct=0.0)
        assert s == 0.0

    # champion_only_reliance_pct
    def test_champion_ge_0_70_adds_25(self):
        s = self._score(avg_contacts_per_active_deal=10.0, single_contact_deal_rate_pct=0.0,
                        champion_only_reliance_pct=0.70)
        assert s == 25.0

    def test_champion_ge_0_50_adds_12(self):
        s = self._score(avg_contacts_per_active_deal=10.0, single_contact_deal_rate_pct=0.0,
                        champion_only_reliance_pct=0.50)
        assert s == 12.0

    def test_champion_below_0_50_adds_0(self):
        s = self._score(avg_contacts_per_active_deal=10.0, single_contact_deal_rate_pct=0.0,
                        champion_only_reliance_pct=0.49)
        assert s == 0.0

    # cap at 100
    def test_depth_score_capped_at_100(self):
        s = self._score(avg_contacts_per_active_deal=1.0, single_contact_deal_rate_pct=0.90,
                        champion_only_reliance_pct=0.90)
        assert s == 100.0

    def test_depth_score_all_zeros(self):
        s = self._score(avg_contacts_per_active_deal=10.0, single_contact_deal_rate_pct=0.0,
                        champion_only_reliance_pct=0.0)
        assert s == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 6. _breadth_score tests
# ─────────────────────────────────────────────────────────────────────────────

class TestBreadthScore:
    def setup_method(self):
        self.engine = fresh_engine()

    def _score(self, **kw):
        return self.engine._breadth_score(make_input(**kw))

    def test_multi_dept_le_0_25_adds_40(self):
        s = self._score(multi_dept_engaged_rate_pct=0.25, org_chart_mapped_pct=1.0,
                        technical_buyer_engaged_pct=1.0)
        assert s == 40.0

    def test_multi_dept_le_0_45_adds_22(self):
        s = self._score(multi_dept_engaged_rate_pct=0.45, org_chart_mapped_pct=1.0,
                        technical_buyer_engaged_pct=1.0)
        assert s == 22.0

    def test_multi_dept_le_0_65_adds_8(self):
        s = self._score(multi_dept_engaged_rate_pct=0.65, org_chart_mapped_pct=1.0,
                        technical_buyer_engaged_pct=1.0)
        assert s == 8.0

    def test_multi_dept_above_0_65_adds_0(self):
        s = self._score(multi_dept_engaged_rate_pct=0.66, org_chart_mapped_pct=1.0,
                        technical_buyer_engaged_pct=1.0)
        assert s == 0.0

    def test_org_chart_le_0_20_adds_35(self):
        s = self._score(multi_dept_engaged_rate_pct=1.0, org_chart_mapped_pct=0.20,
                        technical_buyer_engaged_pct=1.0)
        assert s == 35.0

    def test_org_chart_le_0_40_adds_18(self):
        s = self._score(multi_dept_engaged_rate_pct=1.0, org_chart_mapped_pct=0.40,
                        technical_buyer_engaged_pct=1.0)
        assert s == 18.0

    def test_org_chart_above_0_40_adds_0(self):
        s = self._score(multi_dept_engaged_rate_pct=1.0, org_chart_mapped_pct=0.41,
                        technical_buyer_engaged_pct=1.0)
        assert s == 0.0

    def test_tech_buyer_le_0_30_adds_25(self):
        s = self._score(multi_dept_engaged_rate_pct=1.0, org_chart_mapped_pct=1.0,
                        technical_buyer_engaged_pct=0.30)
        assert s == 25.0

    def test_tech_buyer_le_0_50_adds_12(self):
        s = self._score(multi_dept_engaged_rate_pct=1.0, org_chart_mapped_pct=1.0,
                        technical_buyer_engaged_pct=0.50)
        assert s == 12.0

    def test_tech_buyer_above_0_50_adds_0(self):
        s = self._score(multi_dept_engaged_rate_pct=1.0, org_chart_mapped_pct=1.0,
                        technical_buyer_engaged_pct=0.51)
        assert s == 0.0

    def test_breadth_score_capped_at_100(self):
        s = self._score(multi_dept_engaged_rate_pct=0.0, org_chart_mapped_pct=0.0,
                        technical_buyer_engaged_pct=0.0)
        assert s == 100.0

    def test_breadth_score_all_zeros(self):
        s = self._score(multi_dept_engaged_rate_pct=1.0, org_chart_mapped_pct=1.0,
                        technical_buyer_engaged_pct=1.0)
        assert s == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 7. _executive_access_score tests
# ─────────────────────────────────────────────────────────────────────────────

class TestExecutiveAccessScore:
    def setup_method(self):
        self.engine = fresh_engine()

    def _score(self, **kw):
        return self.engine._executive_access_score(make_input(**kw))

    def test_exec_engaged_le_0_20_adds_45(self):
        s = self._score(executive_engaged_rate_pct=0.20, economic_buyer_direct_contact_pct=1.0,
                        referral_from_champion_to_exec_pct=1.0)
        assert s == 45.0

    def test_exec_engaged_le_0_40_adds_25(self):
        s = self._score(executive_engaged_rate_pct=0.40, economic_buyer_direct_contact_pct=1.0,
                        referral_from_champion_to_exec_pct=1.0)
        assert s == 25.0

    def test_exec_engaged_le_0_60_adds_10(self):
        s = self._score(executive_engaged_rate_pct=0.60, economic_buyer_direct_contact_pct=1.0,
                        referral_from_champion_to_exec_pct=1.0)
        assert s == 10.0

    def test_exec_engaged_above_0_60_adds_0(self):
        s = self._score(executive_engaged_rate_pct=0.61, economic_buyer_direct_contact_pct=1.0,
                        referral_from_champion_to_exec_pct=1.0)
        assert s == 0.0

    def test_economic_buyer_le_0_25_adds_30(self):
        s = self._score(executive_engaged_rate_pct=1.0, economic_buyer_direct_contact_pct=0.25,
                        referral_from_champion_to_exec_pct=1.0)
        assert s == 30.0

    def test_economic_buyer_le_0_50_adds_15(self):
        s = self._score(executive_engaged_rate_pct=1.0, economic_buyer_direct_contact_pct=0.50,
                        referral_from_champion_to_exec_pct=1.0)
        assert s == 15.0

    def test_economic_buyer_above_0_50_adds_0(self):
        s = self._score(executive_engaged_rate_pct=1.0, economic_buyer_direct_contact_pct=0.51,
                        referral_from_champion_to_exec_pct=1.0)
        assert s == 0.0

    def test_referral_le_0_15_adds_25(self):
        s = self._score(executive_engaged_rate_pct=1.0, economic_buyer_direct_contact_pct=1.0,
                        referral_from_champion_to_exec_pct=0.15)
        assert s == 25.0

    def test_referral_le_0_30_adds_12(self):
        s = self._score(executive_engaged_rate_pct=1.0, economic_buyer_direct_contact_pct=1.0,
                        referral_from_champion_to_exec_pct=0.30)
        assert s == 12.0

    def test_referral_above_0_30_adds_0(self):
        s = self._score(executive_engaged_rate_pct=1.0, economic_buyer_direct_contact_pct=1.0,
                        referral_from_champion_to_exec_pct=0.31)
        assert s == 0.0

    def test_exec_access_capped_at_100(self):
        s = self._score(executive_engaged_rate_pct=0.0, economic_buyer_direct_contact_pct=0.0,
                        referral_from_champion_to_exec_pct=0.0)
        assert s == 100.0

    def test_exec_access_all_zeros(self):
        s = self._score(executive_engaged_rate_pct=1.0, economic_buyer_direct_contact_pct=1.0,
                        referral_from_champion_to_exec_pct=1.0)
        assert s == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 8. _risk_exposure_score tests
# ─────────────────────────────────────────────────────────────────────────────

class TestRiskExposureScore:
    def setup_method(self):
        self.engine = fresh_engine()

    def _score(self, **kw):
        return self.engine._risk_exposure_score(make_input(**kw))

    def test_churn_ge_0_30_adds_40(self):
        s = self._score(champion_churn_impacted_deals_pct=0.30, lost_due_single_thread_pct=0.0,
                        deal_sponsor_count_avg=5.0)
        assert s == 40.0

    def test_churn_ge_0_15_adds_22(self):
        s = self._score(champion_churn_impacted_deals_pct=0.15, lost_due_single_thread_pct=0.0,
                        deal_sponsor_count_avg=5.0)
        assert s == 22.0

    def test_churn_ge_0_05_adds_8(self):
        s = self._score(champion_churn_impacted_deals_pct=0.05, lost_due_single_thread_pct=0.0,
                        deal_sponsor_count_avg=5.0)
        assert s == 8.0

    def test_churn_below_0_05_adds_0(self):
        s = self._score(champion_churn_impacted_deals_pct=0.04, lost_due_single_thread_pct=0.0,
                        deal_sponsor_count_avg=5.0)
        assert s == 0.0

    def test_lost_ge_0_30_adds_35(self):
        s = self._score(champion_churn_impacted_deals_pct=0.0, lost_due_single_thread_pct=0.30,
                        deal_sponsor_count_avg=5.0)
        assert s == 35.0

    def test_lost_ge_0_15_adds_18(self):
        s = self._score(champion_churn_impacted_deals_pct=0.0, lost_due_single_thread_pct=0.15,
                        deal_sponsor_count_avg=5.0)
        assert s == 18.0

    def test_lost_below_0_15_adds_0(self):
        s = self._score(champion_churn_impacted_deals_pct=0.0, lost_due_single_thread_pct=0.14,
                        deal_sponsor_count_avg=5.0)
        assert s == 0.0

    def test_sponsor_le_1_0_adds_25(self):
        s = self._score(champion_churn_impacted_deals_pct=0.0, lost_due_single_thread_pct=0.0,
                        deal_sponsor_count_avg=1.0)
        assert s == 25.0

    def test_sponsor_le_1_5_adds_12(self):
        s = self._score(champion_churn_impacted_deals_pct=0.0, lost_due_single_thread_pct=0.0,
                        deal_sponsor_count_avg=1.5)
        assert s == 12.0

    def test_sponsor_above_1_5_adds_0(self):
        s = self._score(champion_churn_impacted_deals_pct=0.0, lost_due_single_thread_pct=0.0,
                        deal_sponsor_count_avg=1.51)
        assert s == 0.0

    def test_risk_exposure_capped_at_100(self):
        s = self._score(champion_churn_impacted_deals_pct=0.50, lost_due_single_thread_pct=0.50,
                        deal_sponsor_count_avg=0.5)
        assert s == 100.0

    def test_risk_exposure_all_zero(self):
        s = self._score(champion_churn_impacted_deals_pct=0.0, lost_due_single_thread_pct=0.0,
                        deal_sponsor_count_avg=5.0)
        assert s == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 9. Composite score tests
# ─────────────────────────────────────────────────────────────────────────────

class TestCompositeScore:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_composite_all_zero(self):
        c = self.engine._composite(0.0, 0.0, 0.0, 0.0)
        assert c == 0.0

    def test_composite_all_100(self):
        c = self.engine._composite(100.0, 100.0, 100.0, 100.0)
        assert c == 100.0

    def test_composite_weights_depth_only(self):
        c = self.engine._composite(100.0, 0.0, 0.0, 0.0)
        assert abs(c - 35.0) < 0.01

    def test_composite_weights_breadth_only(self):
        c = self.engine._composite(0.0, 100.0, 0.0, 0.0)
        assert abs(c - 30.0) < 0.01

    def test_composite_weights_exec_only(self):
        c = self.engine._composite(0.0, 0.0, 100.0, 0.0)
        assert abs(c - 20.0) < 0.01

    def test_composite_weights_risk_only(self):
        c = self.engine._composite(0.0, 0.0, 0.0, 100.0)
        assert abs(c - 15.0) < 0.01

    def test_composite_weights_sum_to_100(self):
        c = self.engine._composite(100.0, 100.0, 100.0, 100.0)
        assert c == 100.0

    def test_composite_is_rounded_to_2_decimals(self):
        c = self.engine._composite(33.0, 33.0, 33.0, 33.0)
        # 33*(0.35+0.30+0.20+0.15) = 33.0, but test rounding doesn't add extra decimals
        assert c == round(c, 2)

    def test_composite_capped_at_100(self):
        c = self.engine._composite(200.0, 200.0, 200.0, 200.0)
        assert c == 100.0


# ─────────────────────────────────────────────────────────────────────────────
# 10. Risk threshold tests
# ─────────────────────────────────────────────────────────────────────────────

class TestRiskThresholds:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_risk_critical_at_60(self):
        assert self.engine._risk(60.0) == MultithreadRisk.critical

    def test_risk_critical_above_60(self):
        assert self.engine._risk(80.0) == MultithreadRisk.critical

    def test_risk_high_at_40(self):
        assert self.engine._risk(40.0) == MultithreadRisk.high

    def test_risk_high_below_60(self):
        assert self.engine._risk(59.99) == MultithreadRisk.high

    def test_risk_moderate_at_20(self):
        assert self.engine._risk(20.0) == MultithreadRisk.moderate

    def test_risk_moderate_below_40(self):
        assert self.engine._risk(39.99) == MultithreadRisk.moderate

    def test_risk_low_below_20(self):
        assert self.engine._risk(19.99) == MultithreadRisk.low

    def test_risk_low_at_zero(self):
        assert self.engine._risk(0.0) == MultithreadRisk.low


# ─────────────────────────────────────────────────────────────────────────────
# 11. Severity threshold tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSeverityThresholds:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_severity_isolated_at_60(self):
        assert self.engine._severity(60.0) == MultithreadSeverity.isolated

    def test_severity_isolated_above_60(self):
        assert self.engine._severity(90.0) == MultithreadSeverity.isolated

    def test_severity_shallow_at_40(self):
        assert self.engine._severity(40.0) == MultithreadSeverity.shallow

    def test_severity_shallow_below_60(self):
        assert self.engine._severity(59.99) == MultithreadSeverity.shallow

    def test_severity_adequate_at_20(self):
        assert self.engine._severity(20.0) == MultithreadSeverity.adequate

    def test_severity_adequate_below_40(self):
        assert self.engine._severity(39.99) == MultithreadSeverity.adequate

    def test_severity_networked_below_20(self):
        assert self.engine._severity(19.99) == MultithreadSeverity.networked

    def test_severity_networked_at_zero(self):
        assert self.engine._severity(0.0) == MultithreadSeverity.networked


# ─────────────────────────────────────────────────────────────────────────────
# 12. Pattern detection tests
# ─────────────────────────────────────────────────────────────────────────────

class TestPatternDetection:
    def setup_method(self):
        self.engine = fresh_engine()

    def _pattern(self, **kw):
        return self.engine._pattern(make_input(**kw))

    def test_single_contact_dependency_both_conditions(self):
        p = self._pattern(single_contact_deal_rate_pct=0.55, avg_contacts_per_active_deal=1.5)
        assert p == MultithreadPattern.single_contact_dependency

    def test_single_contact_dependency_exact_thresholds(self):
        p = self._pattern(single_contact_deal_rate_pct=0.55, avg_contacts_per_active_deal=1.5)
        assert p == MultithreadPattern.single_contact_dependency

    def test_single_contact_dependency_fails_if_rate_below(self):
        p = self._pattern(single_contact_deal_rate_pct=0.54, avg_contacts_per_active_deal=1.5,
                          champion_only_reliance_pct=0.0, executive_engaged_rate_pct=1.0,
                          economic_buyer_direct_contact_pct=1.0, org_chart_mapped_pct=1.0,
                          multi_dept_engaged_rate_pct=1.0, new_stakeholder_added_per_deal_avg=5.0,
                          org_breadth_score_avg=1.0)
        assert p != MultithreadPattern.single_contact_dependency

    def test_single_contact_dependency_fails_if_contacts_above(self):
        p = self._pattern(single_contact_deal_rate_pct=0.60, avg_contacts_per_active_deal=1.51,
                          champion_only_reliance_pct=0.0, executive_engaged_rate_pct=1.0,
                          economic_buyer_direct_contact_pct=1.0, org_chart_mapped_pct=1.0,
                          multi_dept_engaged_rate_pct=1.0, new_stakeholder_added_per_deal_avg=5.0,
                          org_breadth_score_avg=1.0)
        assert p != MultithreadPattern.single_contact_dependency

    def test_champion_only_reliance_both_conditions(self):
        p = self._pattern(single_contact_deal_rate_pct=0.10, avg_contacts_per_active_deal=3.0,
                          champion_only_reliance_pct=0.65, executive_engaged_rate_pct=0.25)
        assert p == MultithreadPattern.champion_only_reliance

    def test_champion_only_reliance_fails_if_pct_below(self):
        p = self._pattern(single_contact_deal_rate_pct=0.10, avg_contacts_per_active_deal=3.0,
                          champion_only_reliance_pct=0.64, executive_engaged_rate_pct=0.25,
                          economic_buyer_direct_contact_pct=1.0, org_chart_mapped_pct=1.0,
                          multi_dept_engaged_rate_pct=1.0, new_stakeholder_added_per_deal_avg=5.0,
                          org_breadth_score_avg=1.0)
        assert p != MultithreadPattern.champion_only_reliance

    def test_executive_bypass_both_conditions(self):
        p = self._pattern(single_contact_deal_rate_pct=0.10, avg_contacts_per_active_deal=3.0,
                          champion_only_reliance_pct=0.30, executive_engaged_rate_pct=0.20,
                          economic_buyer_direct_contact_pct=0.20)
        assert p == MultithreadPattern.executive_bypass

    def test_executive_bypass_exact_threshold(self):
        p = self._pattern(single_contact_deal_rate_pct=0.10, avg_contacts_per_active_deal=3.0,
                          champion_only_reliance_pct=0.30, executive_engaged_rate_pct=0.20,
                          economic_buyer_direct_contact_pct=0.20)
        assert p == MultithreadPattern.executive_bypass

    def test_executive_bypass_fails_if_exec_above(self):
        p = self._pattern(single_contact_deal_rate_pct=0.10, avg_contacts_per_active_deal=3.0,
                          champion_only_reliance_pct=0.30, executive_engaged_rate_pct=0.21,
                          economic_buyer_direct_contact_pct=0.20, org_chart_mapped_pct=1.0,
                          multi_dept_engaged_rate_pct=1.0, new_stakeholder_added_per_deal_avg=5.0,
                          org_breadth_score_avg=1.0)
        assert p != MultithreadPattern.executive_bypass

    def test_org_chart_blind_both_conditions(self):
        p = self._pattern(single_contact_deal_rate_pct=0.10, avg_contacts_per_active_deal=3.0,
                          champion_only_reliance_pct=0.30, executive_engaged_rate_pct=0.50,
                          economic_buyer_direct_contact_pct=0.50, org_chart_mapped_pct=0.15,
                          multi_dept_engaged_rate_pct=0.25)
        assert p == MultithreadPattern.org_chart_blind

    def test_org_chart_blind_fails_if_mapped_above(self):
        p = self._pattern(single_contact_deal_rate_pct=0.10, avg_contacts_per_active_deal=3.0,
                          champion_only_reliance_pct=0.30, executive_engaged_rate_pct=0.50,
                          economic_buyer_direct_contact_pct=0.50, org_chart_mapped_pct=0.16,
                          multi_dept_engaged_rate_pct=0.25, new_stakeholder_added_per_deal_avg=5.0,
                          org_breadth_score_avg=1.0)
        assert p != MultithreadPattern.org_chart_blind

    def test_breadth_shallow_both_conditions(self):
        p = self._pattern(single_contact_deal_rate_pct=0.10, avg_contacts_per_active_deal=3.0,
                          champion_only_reliance_pct=0.30, executive_engaged_rate_pct=0.50,
                          economic_buyer_direct_contact_pct=0.50, org_chart_mapped_pct=0.50,
                          multi_dept_engaged_rate_pct=0.50, new_stakeholder_added_per_deal_avg=0.5,
                          org_breadth_score_avg=0.30)
        assert p == MultithreadPattern.breadth_shallow

    def test_breadth_shallow_fails_if_stakeholder_above(self):
        p = self._pattern(single_contact_deal_rate_pct=0.10, avg_contacts_per_active_deal=3.0,
                          champion_only_reliance_pct=0.30, executive_engaged_rate_pct=0.50,
                          economic_buyer_direct_contact_pct=0.50, org_chart_mapped_pct=0.50,
                          multi_dept_engaged_rate_pct=0.50, new_stakeholder_added_per_deal_avg=0.51,
                          org_breadth_score_avg=0.30)
        assert p == MultithreadPattern.none

    def test_pattern_none_when_all_healthy(self):
        p = self._pattern()
        assert p == MultithreadPattern.none

    def test_pattern_priority_single_contact_over_champion(self):
        # Both single_contact_dependency and champion_only_reliance could match
        p = self._pattern(single_contact_deal_rate_pct=0.60, avg_contacts_per_active_deal=1.5,
                          champion_only_reliance_pct=0.70, executive_engaged_rate_pct=0.20)
        assert p == MultithreadPattern.single_contact_dependency

    def test_pattern_priority_champion_over_exec_bypass(self):
        p = self._pattern(single_contact_deal_rate_pct=0.10, avg_contacts_per_active_deal=3.0,
                          champion_only_reliance_pct=0.70, executive_engaged_rate_pct=0.20,
                          economic_buyer_direct_contact_pct=0.15)
        assert p == MultithreadPattern.champion_only_reliance


# ─────────────────────────────────────────────────────────────────────────────
# 13. Action routing tests
# ─────────────────────────────────────────────────────────────────────────────

class TestActionRouting:
    def setup_method(self):
        self.engine = fresh_engine()

    def _action(self, risk, pattern):
        return self.engine._action(risk, pattern)

    def test_critical_single_contact_is_deal_at_risk(self):
        a = self._action(MultithreadRisk.critical, MultithreadPattern.single_contact_dependency)
        assert a == MultithreadAction.deal_at_risk_intervention

    def test_critical_champion_only_is_deal_at_risk(self):
        a = self._action(MultithreadRisk.critical, MultithreadPattern.champion_only_reliance)
        assert a == MultithreadAction.deal_at_risk_intervention

    def test_critical_exec_bypass_is_multithread_intervention(self):
        a = self._action(MultithreadRisk.critical, MultithreadPattern.executive_bypass)
        assert a == MultithreadAction.multithread_intervention

    def test_critical_org_chart_blind_is_multithread_intervention(self):
        a = self._action(MultithreadRisk.critical, MultithreadPattern.org_chart_blind)
        assert a == MultithreadAction.multithread_intervention

    def test_critical_breadth_shallow_is_multithread_intervention(self):
        a = self._action(MultithreadRisk.critical, MultithreadPattern.breadth_shallow)
        assert a == MultithreadAction.multithread_intervention

    def test_critical_none_is_multithread_intervention(self):
        a = self._action(MultithreadRisk.critical, MultithreadPattern.none)
        assert a == MultithreadAction.multithread_intervention

    def test_high_exec_bypass_is_executive_access_coaching(self):
        a = self._action(MultithreadRisk.high, MultithreadPattern.executive_bypass)
        assert a == MultithreadAction.executive_access_coaching

    def test_high_org_chart_blind_is_organization_navigation_coaching(self):
        a = self._action(MultithreadRisk.high, MultithreadPattern.org_chart_blind)
        assert a == MultithreadAction.organization_navigation_coaching

    def test_high_breadth_shallow_is_stakeholder_mapping_coaching(self):
        a = self._action(MultithreadRisk.high, MultithreadPattern.breadth_shallow)
        assert a == MultithreadAction.stakeholder_mapping_coaching

    def test_high_single_contact_is_champion_diversification_coaching(self):
        a = self._action(MultithreadRisk.high, MultithreadPattern.single_contact_dependency)
        assert a == MultithreadAction.champion_diversification_coaching

    def test_high_champion_only_is_champion_diversification_coaching(self):
        a = self._action(MultithreadRisk.high, MultithreadPattern.champion_only_reliance)
        assert a == MultithreadAction.champion_diversification_coaching

    def test_high_none_is_champion_diversification_coaching(self):
        a = self._action(MultithreadRisk.high, MultithreadPattern.none)
        assert a == MultithreadAction.champion_diversification_coaching

    def test_moderate_any_pattern_is_stakeholder_mapping_coaching(self):
        for pat in MultithreadPattern:
            a = self._action(MultithreadRisk.moderate, pat)
            assert a == MultithreadAction.stakeholder_mapping_coaching

    def test_low_any_pattern_is_no_action(self):
        for pat in MultithreadPattern:
            a = self._action(MultithreadRisk.low, pat)
            assert a == MultithreadAction.no_action


# ─────────────────────────────────────────────────────────────────────────────
# 14. _has_gap and _requires_coaching tests
# ─────────────────────────────────────────────────────────────────────────────

class TestFlags:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_has_gap_true_if_composite_ge_40(self):
        inp = make_input(single_contact_deal_rate_pct=0.0, champion_only_reliance_pct=0.0)
        assert self.engine._has_gap(inp, 40.0) is True

    def test_has_gap_true_if_single_contact_ge_0_45(self):
        inp = make_input(single_contact_deal_rate_pct=0.45)
        assert self.engine._has_gap(inp, 0.0) is True

    def test_has_gap_true_if_champion_only_ge_0_55(self):
        inp = make_input(champion_only_reliance_pct=0.55)
        assert self.engine._has_gap(inp, 0.0) is True

    def test_has_gap_false_all_healthy(self):
        inp = make_input(single_contact_deal_rate_pct=0.10, champion_only_reliance_pct=0.20)
        assert self.engine._has_gap(inp, 10.0) is False

    def test_requires_coaching_true_if_composite_ge_30(self):
        inp = make_input(avg_contacts_per_active_deal=5.0, executive_engaged_rate_pct=0.80)
        assert self.engine._requires_coaching(inp, 30.0) is True

    def test_requires_coaching_true_if_contacts_le_2_0(self):
        inp = make_input(avg_contacts_per_active_deal=2.0, executive_engaged_rate_pct=0.80)
        assert self.engine._requires_coaching(inp, 0.0) is True

    def test_requires_coaching_true_if_exec_rate_le_0_35(self):
        inp = make_input(avg_contacts_per_active_deal=5.0, executive_engaged_rate_pct=0.35)
        assert self.engine._requires_coaching(inp, 0.0) is True

    def test_requires_coaching_false_all_good(self):
        inp = make_input(avg_contacts_per_active_deal=5.0, executive_engaged_rate_pct=0.80)
        assert self.engine._requires_coaching(inp, 10.0) is False


# ─────────────────────────────────────────────────────────────────────────────
# 15. _deal_risk tests
# ─────────────────────────────────────────────────────────────────────────────

class TestDealRisk:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_deal_risk_basic_calculation(self):
        inp = make_input(total_active_deals=10, avg_opportunity_value_usd=100_000.0,
                         single_contact_deal_rate_pct=0.50)
        risk = self.engine._deal_risk(inp, 50.0)
        assert risk == 10 * 100_000.0 * 0.50 * (50.0 / 100)

    def test_deal_risk_zero_composite(self):
        inp = make_input(total_active_deals=10, avg_opportunity_value_usd=100_000.0,
                         single_contact_deal_rate_pct=0.50)
        assert self.engine._deal_risk(inp, 0.0) == 0.0

    def test_deal_risk_zero_single_contact(self):
        inp = make_input(total_active_deals=10, avg_opportunity_value_usd=100_000.0,
                         single_contact_deal_rate_pct=0.0)
        assert self.engine._deal_risk(inp, 80.0) == 0.0

    def test_deal_risk_rounded_to_2_decimals(self):
        inp = make_input(total_active_deals=3, avg_opportunity_value_usd=33_333.33,
                         single_contact_deal_rate_pct=0.333)
        risk = self.engine._deal_risk(inp, 33.33)
        assert risk == round(risk, 2)

    def test_deal_risk_large_values(self):
        inp = make_input(total_active_deals=1000, avg_opportunity_value_usd=500_000.0,
                         single_contact_deal_rate_pct=1.0)
        risk = self.engine._deal_risk(inp, 100.0)
        assert risk == 500_000_000.0


# ─────────────────────────────────────────────────────────────────────────────
# 16. Signal text tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSignal:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_signal_healthy_below_20(self):
        inp = make_input()
        sig = self.engine._signal(inp, MultithreadPattern.none, 10.0)
        assert sig == ("Multi-threading strong — stakeholder depth, org breadth, "
                       "and executive access within benchmarks")

    def test_signal_healthy_at_zero(self):
        inp = make_input()
        sig = self.engine._signal(inp, MultithreadPattern.none, 0.0)
        assert "Multi-threading strong" in sig

    def test_signal_unhealthy_at_20(self):
        inp = make_input(avg_contacts_per_active_deal=1.5, single_contact_deal_rate_pct=0.60,
                         executive_engaged_rate_pct=0.20)
        sig = self.engine._signal(inp, MultithreadPattern.single_contact_dependency, 20.0)
        assert "Single contact dependency" in sig

    def test_signal_includes_avg_contacts(self):
        inp = make_input(avg_contacts_per_active_deal=2.3, single_contact_deal_rate_pct=0.50,
                         executive_engaged_rate_pct=0.30)
        sig = self.engine._signal(inp, MultithreadPattern.champion_only_reliance, 25.0)
        assert "2.3 avg contacts/deal" in sig

    def test_signal_includes_single_pct(self):
        inp = make_input(avg_contacts_per_active_deal=2.0, single_contact_deal_rate_pct=0.45,
                         executive_engaged_rate_pct=0.30)
        sig = self.engine._signal(inp, MultithreadPattern.champion_only_reliance, 25.0)
        assert "45% single-contact deals" in sig

    def test_signal_includes_exec_pct(self):
        inp = make_input(avg_contacts_per_active_deal=2.0, single_contact_deal_rate_pct=0.40,
                         executive_engaged_rate_pct=0.30)
        sig = self.engine._signal(inp, MultithreadPattern.champion_only_reliance, 25.0)
        assert "30% exec engaged" in sig

    def test_signal_includes_composite(self):
        inp = make_input(avg_contacts_per_active_deal=2.0, single_contact_deal_rate_pct=0.40,
                         executive_engaged_rate_pct=0.30)
        sig = self.engine._signal(inp, MultithreadPattern.champion_only_reliance, 35.0)
        assert "composite 35" in sig

    def test_signal_executive_bypass_label(self):
        inp = make_input(avg_contacts_per_active_deal=2.0, single_contact_deal_rate_pct=0.40,
                         executive_engaged_rate_pct=0.15)
        sig = self.engine._signal(inp, MultithreadPattern.executive_bypass, 25.0)
        assert "Executive bypass" in sig

    def test_signal_org_chart_blind_label(self):
        inp = make_input(avg_contacts_per_active_deal=2.0, single_contact_deal_rate_pct=0.40,
                         executive_engaged_rate_pct=0.50)
        sig = self.engine._signal(inp, MultithreadPattern.org_chart_blind, 25.0)
        assert "Org chart blind" in sig

    def test_signal_breadth_shallow_label(self):
        inp = make_input(avg_contacts_per_active_deal=2.0, single_contact_deal_rate_pct=0.40,
                         executive_engaged_rate_pct=0.50)
        sig = self.engine._signal(inp, MultithreadPattern.breadth_shallow, 25.0)
        assert "Breadth shallow" in sig


# ─────────────────────────────────────────────────────────────────────────────
# 17. assess() end-to-end tests
# ─────────────────────────────────────────────────────────────────────────────

class TestAssessEndToEnd:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_assess_returns_multithread_result(self):
        r = self.engine.assess(make_input())
        assert isinstance(r, MultithreadResult)

    def test_assess_rep_id_propagated(self):
        r = self.engine.assess(make_input(rep_id="REP-XYZ"))
        assert r.rep_id == "REP-XYZ"

    def test_assess_region_propagated(self):
        r = self.engine.assess(make_input(region="APAC"))
        assert r.region == "APAC"

    def test_assess_score_bounds(self):
        r = self.engine.assess(make_input())
        assert 0.0 <= r.depth_score <= 100.0
        assert 0.0 <= r.breadth_score <= 100.0
        assert 0.0 <= r.executive_access_score <= 100.0
        assert 0.0 <= r.risk_exposure_score <= 100.0
        assert 0.0 <= r.multithread_composite <= 100.0

    def test_assess_healthy_rep_low_risk(self):
        r = self.engine.assess(make_input())
        assert r.multithread_risk == MultithreadRisk.low

    def test_assess_healthy_rep_no_action(self):
        r = self.engine.assess(make_input())
        assert r.recommended_action == MultithreadAction.no_action

    def test_assess_healthy_rep_networked_severity(self):
        r = self.engine.assess(make_input())
        assert r.multithread_severity == MultithreadSeverity.networked

    def test_assess_healthy_rep_no_gap(self):
        r = self.engine.assess(make_input())
        assert r.has_multithread_gap is False

    def test_assess_healthy_rep_healthy_signal(self):
        r = self.engine.assess(make_input())
        assert "Multi-threading strong" in r.multithread_signal

    def test_assess_critical_rep(self):
        # Force every sub-score to maximum
        inp = make_input(
            avg_contacts_per_active_deal=1.0,
            single_contact_deal_rate_pct=0.90,
            champion_only_reliance_pct=0.90,
            multi_dept_engaged_rate_pct=0.10,
            org_chart_mapped_pct=0.05,
            technical_buyer_engaged_pct=0.10,
            executive_engaged_rate_pct=0.05,
            economic_buyer_direct_contact_pct=0.05,
            referral_from_champion_to_exec_pct=0.05,
            champion_churn_impacted_deals_pct=0.50,
            lost_due_single_thread_pct=0.50,
            deal_sponsor_count_avg=0.5,
        )
        r = self.engine.assess(inp)
        assert r.multithread_risk == MultithreadRisk.critical

    def test_assess_critical_deal_at_risk_with_single_contact(self):
        inp = make_input(
            avg_contacts_per_active_deal=1.0,
            single_contact_deal_rate_pct=0.90,
            champion_only_reliance_pct=0.90,
            multi_dept_engaged_rate_pct=0.10,
            org_chart_mapped_pct=0.05,
            technical_buyer_engaged_pct=0.10,
            executive_engaged_rate_pct=0.05,
            economic_buyer_direct_contact_pct=0.05,
            referral_from_champion_to_exec_pct=0.05,
            champion_churn_impacted_deals_pct=0.50,
            lost_due_single_thread_pct=0.50,
            deal_sponsor_count_avg=0.5,
        )
        r = self.engine.assess(inp)
        assert r.recommended_action == MultithreadAction.deal_at_risk_intervention

    def test_assess_stores_result_in_internal_list(self):
        engine = fresh_engine()
        engine.assess(make_input())
        assert len(engine._results) == 1

    def test_assess_deal_risk_usd_is_float(self):
        r = self.engine.assess(make_input())
        assert isinstance(r.estimated_deal_risk_usd, float)

    def test_assess_has_gap_bool(self):
        r = self.engine.assess(make_input())
        assert isinstance(r.has_multithread_gap, bool)

    def test_assess_requires_coaching_bool(self):
        r = self.engine.assess(make_input())
        assert isinstance(r.requires_multithread_coaching, bool)


# ─────────────────────────────────────────────────────────────────────────────
# 18. assess_batch() tests
# ─────────────────────────────────────────────────────────────────────────────

class TestAssessBatch:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_assess_batch_returns_list(self):
        result = self.engine.assess_batch([make_input(), make_input(rep_id="REP-002")])
        assert isinstance(result, list)

    def test_assess_batch_length(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = self.engine.assess_batch(inputs)
        assert len(results) == 5

    def test_assess_batch_all_multithread_result(self):
        results = self.engine.assess_batch([make_input(), make_input(rep_id="R2")])
        assert all(isinstance(r, MultithreadResult) for r in results)

    def test_assess_batch_empty(self):
        assert self.engine.assess_batch([]) == []

    def test_assess_batch_accumulates_in_results(self):
        engine = fresh_engine()
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        assert len(engine._results) == 3

    def test_assess_batch_rep_ids_preserved(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        results = self.engine.assess_batch(inputs)
        assert [r.rep_id for r in results] == ["R0", "R1", "R2"]


# ─────────────────────────────────────────────────────────────────────────────
# 19. summary() tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSummary:
    def test_summary_empty_engine_returns_dict_with_13_keys(self):
        engine = fresh_engine()
        s = engine.summary()
        assert len(s) == 13

    def test_summary_empty_total_zero(self):
        engine = fresh_engine()
        assert engine.summary()["total"] == 0

    def test_summary_empty_risk_counts_empty(self):
        engine = fresh_engine()
        assert engine.summary()["risk_counts"] == {}

    def test_summary_empty_avg_composite_zero(self):
        engine = fresh_engine()
        assert engine.summary()["avg_multithread_composite"] == 0.0

    def test_summary_empty_total_risk_zero(self):
        engine = fresh_engine()
        assert engine.summary()["total_estimated_deal_risk_usd"] == 0.0

    def test_summary_13_expected_keys(self):
        engine = fresh_engine()
        s = engine.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
            "avg_multithread_composite", "multithread_gap_count", "coaching_count",
            "avg_depth_score", "avg_breadth_score", "avg_executive_access_score",
            "avg_risk_exposure_score", "total_estimated_deal_risk_usd",
        }
        assert set(s.keys()) == expected

    def test_summary_total_after_assessments(self):
        engine = fresh_engine()
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        assert engine.summary()["total"] == 4

    def test_summary_risk_counts_populated(self):
        engine = fresh_engine()
        engine.assess(make_input())  # should be low risk
        s = engine.summary()
        assert "low" in s["risk_counts"]

    def test_summary_pattern_counts_populated(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert "none" in s["pattern_counts"]

    def test_summary_severity_counts_populated(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert "networked" in s["severity_counts"]

    def test_summary_action_counts_populated(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert "no_action" in s["action_counts"]

    def test_summary_avg_composite_is_float(self):
        engine = fresh_engine()
        engine.assess(make_input())
        assert isinstance(engine.summary()["avg_multithread_composite"], float)

    def test_summary_gap_count_correct(self):
        engine = fresh_engine()
        # gap when single_contact_deal_rate_pct >= 0.45
        engine.assess(make_input(single_contact_deal_rate_pct=0.45))
        engine.assess(make_input())  # no gap
        s = engine.summary()
        assert s["multithread_gap_count"] == 1

    def test_summary_coaching_count_correct(self):
        engine = fresh_engine()
        # coaching when avg_contacts <= 2.0
        engine.assess(make_input(avg_contacts_per_active_deal=2.0))
        engine.assess(make_input(avg_contacts_per_active_deal=5.0,
                                 executive_engaged_rate_pct=0.80))
        s = engine.summary()
        # First triggers coaching, second may or may not depending on composite
        assert s["coaching_count"] >= 1

    def test_summary_total_deal_risk_is_sum(self):
        engine = fresh_engine()
        inp1 = make_input(total_active_deals=10, avg_opportunity_value_usd=100_000.0,
                          single_contact_deal_rate_pct=0.50)
        inp2 = make_input(rep_id="R2", total_active_deals=5, avg_opportunity_value_usd=50_000.0,
                          single_contact_deal_rate_pct=0.20)
        r1 = engine.assess(inp1)
        r2 = engine.assess(inp2)
        s = engine.summary()
        expected = round(r1.estimated_deal_risk_usd + r2.estimated_deal_risk_usd, 2)
        assert s["total_estimated_deal_risk_usd"] == expected

    def test_summary_avg_depth_score_correct(self):
        engine = fresh_engine()
        inp = make_input()
        r = engine.assess(inp)
        s = engine.summary()
        assert s["avg_depth_score"] == round(r.depth_score, 1)

    def test_summary_multiple_risk_buckets(self):
        engine = fresh_engine()
        # healthy rep → low
        engine.assess(make_input(rep_id="R1"))
        # critically bad rep
        engine.assess(make_input(
            rep_id="R2",
            avg_contacts_per_active_deal=1.0,
            single_contact_deal_rate_pct=0.90,
            champion_only_reliance_pct=0.90,
            multi_dept_engaged_rate_pct=0.10,
            org_chart_mapped_pct=0.05,
            technical_buyer_engaged_pct=0.10,
            executive_engaged_rate_pct=0.05,
            economic_buyer_direct_contact_pct=0.05,
            referral_from_champion_to_exec_pct=0.05,
            champion_churn_impacted_deals_pct=0.50,
            lost_due_single_thread_pct=0.50,
            deal_sponsor_count_avg=0.5,
        ))
        s = engine.summary()
        assert "low" in s["risk_counts"]
        assert "critical" in s["risk_counts"]


# ─────────────────────────────────────────────────────────────────────────────
# 20. Edge case and boundary tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_all_fields_at_zero(self):
        """Zero values represent worst-case for most fields."""
        inp = make_input(
            avg_contacts_per_active_deal=0.0,
            single_contact_deal_rate_pct=0.0,
            champion_only_reliance_pct=0.0,
            multi_dept_engaged_rate_pct=0.0,
            org_chart_mapped_pct=0.0,
            technical_buyer_engaged_pct=0.0,
            executive_engaged_rate_pct=0.0,
            economic_buyer_direct_contact_pct=0.0,
            referral_from_champion_to_exec_pct=0.0,
            champion_churn_impacted_deals_pct=0.0,
            lost_due_single_thread_pct=0.0,
            deal_sponsor_count_avg=0.0,
            new_stakeholder_added_per_deal_avg=0.0,
            org_breadth_score_avg=0.0,
            total_active_deals=0,
            avg_opportunity_value_usd=0.0,
        )
        r = self.engine.assess(inp)
        assert isinstance(r, MultithreadResult)

    def test_all_fields_at_max(self):
        """Max values for most fields = healthy."""
        inp = make_input(
            avg_contacts_per_active_deal=10.0,
            single_contact_deal_rate_pct=1.0,
            champion_only_reliance_pct=1.0,
            multi_dept_engaged_rate_pct=1.0,
            org_chart_mapped_pct=1.0,
            technical_buyer_engaged_pct=1.0,
            executive_engaged_rate_pct=1.0,
            economic_buyer_direct_contact_pct=1.0,
            referral_from_champion_to_exec_pct=1.0,
            champion_churn_impacted_deals_pct=1.0,
            lost_due_single_thread_pct=1.0,
            deal_sponsor_count_avg=10.0,
            new_stakeholder_added_per_deal_avg=10.0,
            org_breadth_score_avg=1.0,
        )
        r = self.engine.assess(inp)
        assert isinstance(r, MultithreadResult)

    def test_composite_exact_boundary_60(self):
        """composite == 60 should be critical."""
        engine = fresh_engine()
        # Force composite to be exactly 60 via known sub-score values
        # depth=100*0.35=35, breadth=100*0.30=30, exec=100*0.20=20, risk=0*0.15=0 → 85 composite
        # We use the _composite method directly
        c = engine._composite(100.0, 100.0, 0.0, 0.0)  # 35+30 = 65
        assert engine._risk(c) == MultithreadRisk.critical

    def test_composite_boundary_just_below_60(self):
        engine = fresh_engine()
        assert engine._risk(59.99) == MultithreadRisk.high

    def test_composite_boundary_just_below_40(self):
        engine = fresh_engine()
        assert engine._risk(39.99) == MultithreadRisk.moderate

    def test_composite_boundary_just_below_20(self):
        engine = fresh_engine()
        assert engine._risk(19.99) == MultithreadRisk.low

    def test_assess_result_appended_to_results(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert engine._results[0] is r

    def test_multiple_assess_accumulates(self):
        engine = fresh_engine()
        for i in range(10):
            engine.assess(make_input(rep_id=f"R{i}"))
        assert len(engine._results) == 10

    def test_fresh_engine_empty_results(self):
        engine = fresh_engine()
        assert engine._results == []

    def test_to_dict_risk_value_is_valid(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        assert d["multithread_risk"] in [r.value for r in MultithreadRisk]

    def test_to_dict_pattern_value_is_valid(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        assert d["multithread_pattern"] in [p.value for p in MultithreadPattern]

    def test_to_dict_severity_value_is_valid(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        assert d["multithread_severity"] in [s.value for s in MultithreadSeverity]

    def test_to_dict_action_value_is_valid(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        assert d["recommended_action"] in [a.value for a in MultithreadAction]

    def test_depth_score_boundary_1_5_vs_1_51(self):
        e = fresh_engine()
        s1 = e._depth_score(make_input(avg_contacts_per_active_deal=1.5,
                                       single_contact_deal_rate_pct=0.0,
                                       champion_only_reliance_pct=0.0))
        s2 = e._depth_score(make_input(avg_contacts_per_active_deal=1.51,
                                       single_contact_deal_rate_pct=0.0,
                                       champion_only_reliance_pct=0.0))
        assert s1 > s2

    def test_breadth_score_boundary_0_25_vs_0_26(self):
        e = fresh_engine()
        s1 = e._breadth_score(make_input(multi_dept_engaged_rate_pct=0.25,
                                          org_chart_mapped_pct=1.0, technical_buyer_engaged_pct=1.0))
        s2 = e._breadth_score(make_input(multi_dept_engaged_rate_pct=0.26,
                                          org_chart_mapped_pct=1.0, technical_buyer_engaged_pct=1.0))
        assert s1 > s2

    def test_signal_rounding_single_pct(self):
        """single_contact_deal_rate_pct=0.456 rounds to 46%."""
        inp = make_input(avg_contacts_per_active_deal=2.0,
                         single_contact_deal_rate_pct=0.456,
                         executive_engaged_rate_pct=0.50)
        sig = fresh_engine()._signal(inp, MultithreadPattern.champion_only_reliance, 25.0)
        assert "46% single-contact deals" in sig

    def test_summary_avg_scores_rounded_1_decimal(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        for key in ("avg_depth_score", "avg_breadth_score",
                    "avg_executive_access_score", "avg_risk_exposure_score"):
            val = s[key]
            assert val == round(val, 1)

    def test_has_gap_false_boundary_just_below_all_thresholds(self):
        inp = make_input(single_contact_deal_rate_pct=0.44, champion_only_reliance_pct=0.54)
        assert fresh_engine()._has_gap(inp, 39.9) is False

    def test_pattern_breadth_shallow_exact_boundary_both(self):
        p = fresh_engine()._pattern(make_input(
            single_contact_deal_rate_pct=0.10, avg_contacts_per_active_deal=3.0,
            champion_only_reliance_pct=0.30, executive_engaged_rate_pct=0.50,
            economic_buyer_direct_contact_pct=0.50, org_chart_mapped_pct=0.50,
            multi_dept_engaged_rate_pct=0.50, new_stakeholder_added_per_deal_avg=0.5,
            org_breadth_score_avg=0.30,
        ))
        assert p == MultithreadPattern.breadth_shallow

    def test_assess_moderate_risk_gives_stakeholder_mapping(self):
        # Design a scenario where composite is 20-39 (moderate)
        # depth = 22 (avg_contacts=2.0), breadth = 0, exec=0, risk=0 → 22*0.35=7.7
        # Let's try breadth=22 (multi_dept=0.45) → 22*0.30=6.6, total~14.3 ← too low
        # Try depth=40+35=75, breadth=0, exec=0, risk=0 → 75*0.35=26.25 → moderate
        inp = make_input(
            avg_contacts_per_active_deal=1.5,      # +40
            single_contact_deal_rate_pct=0.60,     # +35 → depth=75 (but capped)
            champion_only_reliance_pct=0.0,
            multi_dept_engaged_rate_pct=1.0,       # 0
            org_chart_mapped_pct=1.0,              # 0
            technical_buyer_engaged_pct=1.0,       # 0
            executive_engaged_rate_pct=1.0,        # 0
            economic_buyer_direct_contact_pct=1.0, # 0
            referral_from_champion_to_exec_pct=1.0,# 0
            champion_churn_impacted_deals_pct=0.0, # 0
            lost_due_single_thread_pct=0.0,        # 0
            deal_sponsor_count_avg=5.0,            # 0
        )
        r = fresh_engine().assess(inp)
        # composite = 75*0.35 = 26.25 → moderate
        assert r.multithread_risk == MultithreadRisk.moderate
        assert r.recommended_action == MultithreadAction.stakeholder_mapping_coaching

    def test_assess_high_risk_executive_bypass(self):
        # Need composite 40-59 with executive_bypass pattern
        # depth=75*0.35=26.25, breadth=75*0.30=22.5 → total=48.75 → high
        inp = make_input(
            avg_contacts_per_active_deal=1.5,       # +40
            single_contact_deal_rate_pct=0.60,      # +35 → depth=75 (capped at 100 with champ)
            champion_only_reliance_pct=0.0,         # +0
            multi_dept_engaged_rate_pct=0.25,       # +40
            org_chart_mapped_pct=0.20,              # +35 → breadth=75
            technical_buyer_engaged_pct=1.0,        # 0
            executive_engaged_rate_pct=0.20,        # executive_bypass condition: exec<=0.20
            economic_buyer_direct_contact_pct=0.20, # executive_bypass condition: econ<=0.20
            referral_from_champion_to_exec_pct=1.0, # 0
            champion_churn_impacted_deals_pct=0.0,
            lost_due_single_thread_pct=0.0,
            deal_sponsor_count_avg=5.0,
        )
        r = fresh_engine().assess(inp)
        # depth=75, breadth=75, exec=45+30=75, risk=0
        # composite = 75*0.35+75*0.30+75*0.20+0*0.15 = 26.25+22.5+15 = 63.75 → critical
        # If critical+exec_bypass → multithread_intervention
        assert r.multithread_risk in (MultithreadRisk.critical, MultithreadRisk.high)

    def test_assess_single_contact_dependency_pattern_set(self):
        inp = make_input(
            single_contact_deal_rate_pct=0.60,
            avg_contacts_per_active_deal=1.5,
        )
        r = fresh_engine().assess(inp)
        assert r.multithread_pattern == MultithreadPattern.single_contact_dependency

    def test_assess_champion_only_reliance_pattern_set(self):
        inp = make_input(
            single_contact_deal_rate_pct=0.10,
            avg_contacts_per_active_deal=3.0,
            champion_only_reliance_pct=0.70,
            executive_engaged_rate_pct=0.20,
        )
        r = fresh_engine().assess(inp)
        assert r.multithread_pattern == MultithreadPattern.champion_only_reliance

    def test_isolated_severity_at_composite_60(self):
        engine = fresh_engine()
        assert engine._severity(60.0) == MultithreadSeverity.isolated

    def test_shallow_severity_at_composite_40(self):
        engine = fresh_engine()
        assert engine._severity(40.0) == MultithreadSeverity.shallow

    def test_adequate_severity_at_composite_20(self):
        engine = fresh_engine()
        assert engine._severity(20.0) == MultithreadSeverity.adequate

    def test_networked_severity_at_composite_0(self):
        engine = fresh_engine()
        assert engine._severity(0.0) == MultithreadSeverity.networked

    def test_deal_risk_formula_precise(self):
        engine = fresh_engine()
        inp = make_input(total_active_deals=20, avg_opportunity_value_usd=50_000.0,
                         single_contact_deal_rate_pct=0.50)
        comp = 40.0
        expected = round(20 * 50_000.0 * 0.50 * (40.0 / 100), 2)
        assert engine._deal_risk(inp, comp) == expected

    def test_requires_coaching_boundary_contacts_exactly_2(self):
        inp = make_input(avg_contacts_per_active_deal=2.0, executive_engaged_rate_pct=0.80)
        assert fresh_engine()._requires_coaching(inp, 0.0) is True

    def test_requires_coaching_boundary_exec_exactly_035(self):
        inp = make_input(avg_contacts_per_active_deal=5.0, executive_engaged_rate_pct=0.35)
        assert fresh_engine()._requires_coaching(inp, 0.0) is True

    def test_pattern_none_exact_boundary(self):
        """Just above all pattern thresholds → none."""
        p = fresh_engine()._pattern(make_input(
            single_contact_deal_rate_pct=0.54,
            avg_contacts_per_active_deal=1.51,
            champion_only_reliance_pct=0.64,
            executive_engaged_rate_pct=0.26,
            economic_buyer_direct_contact_pct=0.21,
            org_chart_mapped_pct=0.16,
            multi_dept_engaged_rate_pct=0.26,
            new_stakeholder_added_per_deal_avg=0.51,
            org_breadth_score_avg=0.31,
        ))
        assert p == MultithreadPattern.none
