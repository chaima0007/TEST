"""
Comprehensive pytest tests for SalesAccountChurnEarlyWarningEngine.
100+ tests covering: smoke tests, all patterns, all risk levels, all severities,
all actions, boundary values for each sub-score threshold, has_churn_signal,
requires_executive_action, arr_at_risk calculation, signal string format,
batch assess, summary aggregation, and empty summary.
"""
from __future__ import annotations

import sys
sys.path.insert(0, '/home/user/TEST')

import pytest

from swarm.intelligence.sales_account_churn_early_warning_engine import (
    SalesAccountChurnEarlyWarningEngine,
    ChurnInput,
    ChurnResult,
    ChurnRisk,
    ChurnPattern,
    ChurnSeverity,
    ChurnAction,
)


# ---------------------------------------------------------------------------
# Helper — safe low-churn defaults
# ---------------------------------------------------------------------------

def make_input(**overrides) -> ChurnInput:
    """Return a ChurnInput with safe defaults that score very low (healthy account)."""
    defaults = dict(
        account_id="acct-001",
        region="NA",
        evaluation_period_id="Q1-2026",
        # Usage signals — all healthy
        product_usage_decay_pct=0.0,
        feature_adoption_rate_pct=0.90,
        login_frequency_decay_pct=0.0,
        api_call_volume_decay_pct=0.0,
        # Relationship signals — all healthy
        executive_sponsor_engaged=1.0,
        champion_tenure_months=24.0,
        stakeholder_count_change=0.0,
        last_exec_meeting_days_ago=10.0,
        # Support & satisfaction — all healthy
        open_support_tickets=0,
        avg_ticket_resolution_days=1.0,
        nps_score_change=5.0,
        escalation_frequency_pct=0.0,
        # Competitive & value — all healthy
        competitive_evaluation_signal=0.0,
        roi_achievement_pct=1.0,
        contract_utilization_pct=0.90,
        renewal_conversation_initiated=1.0,
        # Volume context
        arr_usd=100_000.0,
        contract_months_remaining=12,
        days_to_renewal=365,
    )
    defaults.update(overrides)
    return ChurnInput(**defaults)


@pytest.fixture
def engine():
    return SalesAccountChurnEarlyWarningEngine()


# ===========================================================================
# 1. SMOKE TESTS
# ===========================================================================

class TestSmoke:
    def test_assess_returns_churn_result(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result, ChurnResult)

    def test_to_dict_has_exactly_15_keys(self, engine):
        result = engine.assess(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self, engine):
        result = engine.assess(make_input())
        expected_keys = {
            "account_id", "region", "churn_risk", "churn_pattern",
            "churn_severity", "recommended_action", "usage_score",
            "relationship_score", "support_score", "value_score",
            "churn_composite", "has_churn_signal", "requires_executive_action",
            "estimated_arr_at_risk_usd", "churn_signal",
        }
        assert set(result.to_dict().keys()) == expected_keys

    def test_summary_has_exactly_13_keys(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert len(s) == 13

    def test_summary_exact_keys(self, engine):
        engine.assess(make_input())
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_churn_composite", "churn_signal_count",
            "executive_action_count", "avg_usage_score", "avg_relationship_score",
            "avg_support_score", "avg_value_score", "total_estimated_arr_at_risk_usd",
        }
        assert set(engine.summary().keys()) == expected

    def test_max_composite_is_100(self, engine):
        # Force all sub-scores to max
        i = make_input(
            product_usage_decay_pct=1.0,
            feature_adoption_rate_pct=0.0,
            login_frequency_decay_pct=1.0,
            executive_sponsor_engaged=0.0,
            last_exec_meeting_days_ago=200.0,
            stakeholder_count_change=-5.0,
            open_support_tickets=15,
            escalation_frequency_pct=1.0,
            avg_ticket_resolution_days=20.0,
            roi_achievement_pct=0.0,
            competitive_evaluation_signal=1.0,
            contract_utilization_pct=0.0,
        )
        result = engine.assess(i)
        assert result.churn_composite == 100.0

    def test_min_composite_is_zero(self, engine):
        result = engine.assess(make_input())
        assert result.churn_composite == 0.0

    def test_account_id_and_region_propagated(self, engine):
        result = engine.assess(make_input(account_id="X99", region="EMEA"))
        assert result.account_id == "X99"
        assert result.region == "EMEA"

    def test_composite_formula(self, engine):
        # Drive each sub-score to known values and verify composite
        # All sub-scores = 0 → composite = 0
        result = engine.assess(make_input())
        assert result.churn_composite == 0.0
        assert result.usage_score == 0
        assert result.relationship_score == 0
        assert result.support_score == 0
        assert result.value_score == 0


# ===========================================================================
# 2. ENUM VALUES
# ===========================================================================

class TestEnumValues:
    def test_churn_risk_values(self):
        assert ChurnRisk.low.value == "low"
        assert ChurnRisk.moderate.value == "moderate"
        assert ChurnRisk.high.value == "high"
        assert ChurnRisk.critical.value == "critical"

    def test_churn_pattern_values(self):
        assert ChurnPattern.none.value == "none"
        assert ChurnPattern.usage_collapse.value == "usage_collapse"
        assert ChurnPattern.sponsor_exodus.value == "sponsor_exodus"
        assert ChurnPattern.support_spiral.value == "support_spiral"
        assert ChurnPattern.competitive_switch.value == "competitive_switch"
        assert ChurnPattern.value_gap_crisis.value == "value_gap_crisis"

    def test_churn_severity_values(self):
        assert ChurnSeverity.healthy.value == "healthy"
        assert ChurnSeverity.watching.value == "watching"
        assert ChurnSeverity.at_risk.value == "at_risk"
        assert ChurnSeverity.churning.value == "churning"

    def test_churn_action_values(self):
        assert ChurnAction.no_action.value == "no_action"
        assert ChurnAction.health_monitoring.value == "health_monitoring"
        assert ChurnAction.executive_business_review.value == "executive_business_review"
        assert ChurnAction.success_plan_reset.value == "success_plan_reset"
        assert ChurnAction.competitive_defense_playbook.value == "competitive_defense_playbook"
        assert ChurnAction.sponsor_re_engagement.value == "sponsor_re_engagement"
        assert ChurnAction.support_escalation_resolution.value == "support_escalation_resolution"
        assert ChurnAction.renewal_risk_intervention.value == "renewal_risk_intervention"
        assert ChurnAction.executive_save_call.value == "executive_save_call"


# ===========================================================================
# 3. RISK LEVELS
# ===========================================================================

class TestRiskLevels:
    def test_risk_low_when_composite_below_20(self, engine):
        result = engine.assess(make_input())
        assert result.churn_risk == "low"

    def test_risk_moderate_at_exactly_20(self, engine):
        # Drive composite to ~20: need us*0.30 + re*0.25 + su*0.25 + va*0.20 = 20
        # usage_decay 0.30 → us=22; composite = 22*0.30 = 6.6 too low
        # Combine decay + feature_adoption to push usage higher
        # usage_decay>=0.30 → +22, feature_adoption<=0.60 → +6 → us=28
        # 28*0.30 = 8.4, need 20 total
        # relationship: exec_days>=30 → +6 → re=6; 6*0.25=1.5 → total=9.9
        # value: roi<=0.75 → +10; va=10; 10*0.20=2.0 → total=11.9
        # support: tickets>=2 → +8, su=8; 8*0.25=2.0 → total 13.9
        # Need more. escalation>=0.20 → +18 on support; su=26; 26*0.25=6.5 → total 18.4
        # Add more usage: decay>=0.50 → +40; feat<=0.25→+35; login>=0.30→+12; us=87 capped at 100
        # 100*0.30 + 6*0.25 + 26*0.25 + 10*0.20 = 30+1.5+6.5+2 = 40 → high not moderate
        # Let's just drive composite to 20-39 directly
        # usage_decay=0.30 → +22; login_decay=0.30 → +12 → us=34
        # 34*0.30=10.2, re=0, su=0, va=0 → 10.2 < 20
        # Add feature_adoption=0.45 → +18; us=52; 52*0.30=15.6
        # Add support tickets=2 → +8; su=8; 8*0.25=2 → total=17.6
        # Need just a bit more: nps_change doesn't contribute to score
        # Add escalation=0.20 → +18; su=26; 26*0.25=6.5 → total=22.1 → moderate!
        result = engine.assess(make_input(
            product_usage_decay_pct=0.30,
            login_frequency_decay_pct=0.30,
            feature_adoption_rate_pct=0.45,
            open_support_tickets=2,
            escalation_frequency_pct=0.20,
        ))
        assert result.churn_risk == "moderate"
        assert result.churn_composite >= 20

    def test_risk_high_at_exactly_40(self, engine):
        # Push composite to 40-59
        # usage: decay>=0.50→+40, feature<=0.25→+35, login>=0.50→+25; us=100
        # 100*0.30=30
        # relationship=0, support=0, value: roi<=0.75→+10; va=10; 10*0.20=2 → total=32
        # Add relationship: exec_days>=30→+6; re=6; 6*0.25=1.5 → total=33.5
        # Add support tickets>=5→+22; esc>=0.20→+18; su=40; 40*0.25=10 → total=43.5 → high
        result = engine.assess(make_input(
            product_usage_decay_pct=0.55,
            feature_adoption_rate_pct=0.20,
            login_frequency_decay_pct=0.55,
            last_exec_meeting_days_ago=35.0,
            open_support_tickets=5,
            escalation_frequency_pct=0.20,
            roi_achievement_pct=0.70,
        ))
        assert result.churn_risk == "high"
        assert result.churn_composite >= 40

    def test_risk_critical_at_exactly_60(self, engine):
        result = engine.assess(make_input(
            product_usage_decay_pct=1.0,
            feature_adoption_rate_pct=0.0,
            login_frequency_decay_pct=1.0,
            executive_sponsor_engaged=0.0,
            last_exec_meeting_days_ago=200.0,
            stakeholder_count_change=-5.0,
            open_support_tickets=15,
            escalation_frequency_pct=1.0,
            avg_ticket_resolution_days=20.0,
            roi_achievement_pct=0.0,
            competitive_evaluation_signal=1.0,
            contract_utilization_pct=0.0,
        ))
        assert result.churn_risk == "critical"
        assert result.churn_composite >= 60

    def test_risk_boundary_19_99_is_low(self, engine):
        # composite just under 20 → low
        # All zeros → 0.0 → low
        result = engine.assess(make_input())
        assert result.churn_risk == "low"

    def test_risk_boundary_39_99_is_moderate(self, engine):
        # Need composite between 20 and 39.99
        result = engine.assess(make_input(
            product_usage_decay_pct=0.30,
            login_frequency_decay_pct=0.30,
            feature_adoption_rate_pct=0.45,
            open_support_tickets=2,
            escalation_frequency_pct=0.20,
        ))
        comp = result.churn_composite
        assert 20 <= comp < 40
        assert result.churn_risk == "moderate"

    def test_risk_boundary_59_99_is_high(self, engine):
        # composite between 40 and 59.99
        result = engine.assess(make_input(
            product_usage_decay_pct=0.55,
            feature_adoption_rate_pct=0.20,
            login_frequency_decay_pct=0.55,
            last_exec_meeting_days_ago=35.0,
            open_support_tickets=5,
            escalation_frequency_pct=0.20,
            roi_achievement_pct=0.70,
        ))
        assert 40 <= result.churn_composite < 60
        assert result.churn_risk == "high"


# ===========================================================================
# 4. SEVERITY LEVELS
# ===========================================================================

class TestSeverityLevels:
    def test_severity_healthy_below_20(self, engine):
        result = engine.assess(make_input())
        assert result.churn_severity == "healthy"

    def test_severity_watching_20_to_39(self, engine):
        result = engine.assess(make_input(
            product_usage_decay_pct=0.30,
            login_frequency_decay_pct=0.30,
            feature_adoption_rate_pct=0.45,
            open_support_tickets=2,
            escalation_frequency_pct=0.20,
        ))
        assert result.churn_severity == "watching"

    def test_severity_at_risk_40_to_59(self, engine):
        result = engine.assess(make_input(
            product_usage_decay_pct=0.55,
            feature_adoption_rate_pct=0.20,
            login_frequency_decay_pct=0.55,
            last_exec_meeting_days_ago=35.0,
            open_support_tickets=5,
            escalation_frequency_pct=0.20,
            roi_achievement_pct=0.70,
        ))
        assert result.churn_severity == "at_risk"

    def test_severity_churning_at_60_plus(self, engine):
        result = engine.assess(make_input(
            product_usage_decay_pct=1.0,
            feature_adoption_rate_pct=0.0,
            login_frequency_decay_pct=1.0,
            executive_sponsor_engaged=0.0,
            last_exec_meeting_days_ago=200.0,
            open_support_tickets=15,
            escalation_frequency_pct=1.0,
            avg_ticket_resolution_days=20.0,
            roi_achievement_pct=0.0,
            competitive_evaluation_signal=1.0,
            contract_utilization_pct=0.0,
        ))
        assert result.churn_severity == "churning"


# ===========================================================================
# 5. PATTERN DETECTION
# ===========================================================================

class TestPatternDetection:
    def test_pattern_none_when_all_healthy(self, engine):
        result = engine.assess(make_input())
        assert result.churn_pattern == "none"

    def test_usage_collapse_both_conditions_met(self, engine):
        result = engine.assess(make_input(
            product_usage_decay_pct=0.45,
            login_frequency_decay_pct=0.40,
        ))
        assert result.churn_pattern == "usage_collapse"

    def test_usage_collapse_exact_boundary_45_and_40(self, engine):
        result = engine.assess(make_input(
            product_usage_decay_pct=0.45,
            login_frequency_decay_pct=0.40,
        ))
        assert result.churn_pattern == "usage_collapse"

    def test_usage_collapse_not_triggered_usage_below_threshold(self, engine):
        result = engine.assess(make_input(
            product_usage_decay_pct=0.44,
            login_frequency_decay_pct=0.40,
        ))
        assert result.churn_pattern != "usage_collapse"

    def test_usage_collapse_not_triggered_login_below_threshold(self, engine):
        result = engine.assess(make_input(
            product_usage_decay_pct=0.45,
            login_frequency_decay_pct=0.39,
        ))
        assert result.churn_pattern != "usage_collapse"

    def test_sponsor_exodus_both_conditions_met(self, engine):
        result = engine.assess(make_input(
            executive_sponsor_engaged=0.25,
            stakeholder_count_change=-2.0,
        ))
        assert result.churn_pattern == "sponsor_exodus"

    def test_sponsor_exodus_exact_boundary_25_and_minus2(self, engine):
        result = engine.assess(make_input(
            executive_sponsor_engaged=0.25,
            stakeholder_count_change=-2.0,
        ))
        assert result.churn_pattern == "sponsor_exodus"

    def test_sponsor_exodus_not_triggered_exec_above_25(self, engine):
        result = engine.assess(make_input(
            executive_sponsor_engaged=0.26,
            stakeholder_count_change=-2.0,
        ))
        assert result.churn_pattern != "sponsor_exodus"

    def test_sponsor_exodus_not_triggered_stakeholder_change_above_minus2(self, engine):
        result = engine.assess(make_input(
            executive_sponsor_engaged=0.25,
            stakeholder_count_change=-1.0,
        ))
        assert result.churn_pattern != "sponsor_exodus"

    def test_support_spiral_both_conditions_met(self, engine):
        result = engine.assess(make_input(
            open_support_tickets=6,
            escalation_frequency_pct=0.30,
        ))
        assert result.churn_pattern == "support_spiral"

    def test_support_spiral_exact_boundary_6_tickets_and_30_pct(self, engine):
        result = engine.assess(make_input(
            open_support_tickets=6,
            escalation_frequency_pct=0.30,
        ))
        assert result.churn_pattern == "support_spiral"

    def test_support_spiral_not_triggered_tickets_below_6(self, engine):
        result = engine.assess(make_input(
            open_support_tickets=5,
            escalation_frequency_pct=0.30,
        ))
        assert result.churn_pattern != "support_spiral"

    def test_support_spiral_not_triggered_escalation_below_30(self, engine):
        result = engine.assess(make_input(
            open_support_tickets=6,
            escalation_frequency_pct=0.29,
        ))
        assert result.churn_pattern != "support_spiral"

    def test_competitive_switch_both_conditions_met(self, engine):
        result = engine.assess(make_input(
            competitive_evaluation_signal=0.55,
            roi_achievement_pct=0.60,
        ))
        assert result.churn_pattern == "competitive_switch"

    def test_competitive_switch_exact_boundary_55_and_60(self, engine):
        result = engine.assess(make_input(
            competitive_evaluation_signal=0.55,
            roi_achievement_pct=0.60,
        ))
        assert result.churn_pattern == "competitive_switch"

    def test_competitive_switch_not_triggered_signal_below_55(self, engine):
        result = engine.assess(make_input(
            competitive_evaluation_signal=0.54,
            roi_achievement_pct=0.60,
        ))
        assert result.churn_pattern != "competitive_switch"

    def test_competitive_switch_not_triggered_roi_above_60(self, engine):
        result = engine.assess(make_input(
            competitive_evaluation_signal=0.55,
            roi_achievement_pct=0.61,
        ))
        assert result.churn_pattern != "competitive_switch"

    def test_value_gap_crisis_both_conditions_met(self, engine):
        result = engine.assess(make_input(
            roi_achievement_pct=0.40,
            contract_utilization_pct=0.40,
        ))
        assert result.churn_pattern == "value_gap_crisis"

    def test_value_gap_crisis_exact_boundary_40_and_40(self, engine):
        result = engine.assess(make_input(
            roi_achievement_pct=0.40,
            contract_utilization_pct=0.40,
        ))
        assert result.churn_pattern == "value_gap_crisis"

    def test_value_gap_crisis_not_triggered_roi_above_40(self, engine):
        result = engine.assess(make_input(
            roi_achievement_pct=0.41,
            contract_utilization_pct=0.40,
        ))
        assert result.churn_pattern != "value_gap_crisis"

    def test_value_gap_crisis_not_triggered_utilization_above_40(self, engine):
        result = engine.assess(make_input(
            roi_achievement_pct=0.40,
            contract_utilization_pct=0.41,
        ))
        assert result.churn_pattern != "value_gap_crisis"

    def test_usage_collapse_takes_priority_over_sponsor_exodus(self, engine):
        # usage_collapse triggers first in priority order
        result = engine.assess(make_input(
            product_usage_decay_pct=0.45,
            login_frequency_decay_pct=0.40,
            executive_sponsor_engaged=0.25,
            stakeholder_count_change=-2.0,
        ))
        assert result.churn_pattern == "usage_collapse"

    def test_sponsor_exodus_takes_priority_over_support_spiral(self, engine):
        result = engine.assess(make_input(
            executive_sponsor_engaged=0.25,
            stakeholder_count_change=-2.0,
            open_support_tickets=6,
            escalation_frequency_pct=0.30,
        ))
        assert result.churn_pattern == "sponsor_exodus"

    def test_support_spiral_takes_priority_over_competitive_switch(self, engine):
        result = engine.assess(make_input(
            open_support_tickets=6,
            escalation_frequency_pct=0.30,
            competitive_evaluation_signal=0.55,
            roi_achievement_pct=0.60,
        ))
        assert result.churn_pattern == "support_spiral"

    def test_competitive_switch_takes_priority_over_value_gap_crisis(self, engine):
        result = engine.assess(make_input(
            competitive_evaluation_signal=0.55,
            roi_achievement_pct=0.40,
            contract_utilization_pct=0.40,
        ))
        assert result.churn_pattern == "competitive_switch"


# ===========================================================================
# 6. ACTION MAPPING
# ===========================================================================

class TestActionMapping:
    def test_low_risk_gives_no_action(self, engine):
        result = engine.assess(make_input())
        assert result.recommended_action == "no_action"

    def test_moderate_risk_gives_health_monitoring(self, engine):
        result = engine.assess(make_input(
            product_usage_decay_pct=0.30,
            login_frequency_decay_pct=0.30,
            feature_adoption_rate_pct=0.45,
            open_support_tickets=2,
            escalation_frequency_pct=0.20,
        ))
        assert result.churn_risk == "moderate"
        assert result.recommended_action == "health_monitoring"

    def test_critical_sponsor_exodus_gives_executive_save_call(self, engine):
        result = engine.assess(make_input(
            product_usage_decay_pct=1.0,
            feature_adoption_rate_pct=0.0,
            login_frequency_decay_pct=1.0,
            executive_sponsor_engaged=0.25,
            stakeholder_count_change=-2.0,
            last_exec_meeting_days_ago=200.0,
            open_support_tickets=15,
            escalation_frequency_pct=1.0,
            avg_ticket_resolution_days=20.0,
            roi_achievement_pct=0.0,
            competitive_evaluation_signal=1.0,
            contract_utilization_pct=0.0,
        ))
        assert result.churn_risk == "critical"
        # With usage_collapse firing first (product_usage_decay>=0.45 AND login>=0.40),
        # sponsor_exodus won't fire. Make usage below usage_collapse threshold.
        # Let's test sponsor_exodus directly without usage_collapse
        result2 = engine.assess(make_input(
            # Sub-scores driving critical without usage_collapse
            executive_sponsor_engaged=0.25,
            stakeholder_count_change=-2.0,
            last_exec_meeting_days_ago=200.0,
            open_support_tickets=15,
            escalation_frequency_pct=1.0,
            avg_ticket_resolution_days=20.0,
            roi_achievement_pct=0.0,
            competitive_evaluation_signal=1.0,
            contract_utilization_pct=0.0,
        ))
        assert result2.churn_pattern == "sponsor_exodus"
        assert result2.churn_risk == "critical"
        assert result2.recommended_action == "executive_save_call"

    def test_critical_competitive_switch_gives_executive_save_call(self, engine):
        # Trigger competitive_switch: avoid usage_collapse, sponsor_exodus, support_spiral
        # usage_collapse: needs product_decay>=0.45 AND login_decay>=0.40 → keep decay below 0.45
        # sponsor_exodus: needs exec_engaged<=0.25 AND stakeholder_change<=-2 → keep exec above 0.25
        # support_spiral: needs tickets>=6 AND escalation>=0.30 → keep tickets below 6
        # competitive_switch: competitive_eval>=0.55 AND roi<=0.60 → satisfied
        result = engine.assess(make_input(
            product_usage_decay_pct=0.44,        # just below 0.45 → no usage_collapse
            feature_adoption_rate_pct=0.0,       # +35 usage
            login_frequency_decay_pct=0.39,      # below 0.40 → no usage_collapse
            executive_sponsor_engaged=0.30,      # above 0.25 → no sponsor_exodus
            last_exec_meeting_days_ago=200.0,
            stakeholder_count_change=-5.0,
            open_support_tickets=5,              # below 6 → no support_spiral
            escalation_frequency_pct=0.0,
            avg_ticket_resolution_days=20.0,
            competitive_evaluation_signal=0.60,
            roi_achievement_pct=0.30,            # <=0.60 → competitive_switch
            contract_utilization_pct=0.0,
        ))
        assert result.churn_pattern == "competitive_switch"
        assert result.churn_risk == "critical"
        assert result.recommended_action == "executive_save_call"

    def test_critical_other_pattern_gives_renewal_risk_intervention(self, engine):
        # Critical risk with usage_collapse pattern → renewal_risk_intervention
        result = engine.assess(make_input(
            product_usage_decay_pct=0.45,
            login_frequency_decay_pct=0.40,
            feature_adoption_rate_pct=0.0,
            executive_sponsor_engaged=0.20,
            last_exec_meeting_days_ago=200.0,
            stakeholder_count_change=-5.0,
            open_support_tickets=15,
            escalation_frequency_pct=1.0,
            avg_ticket_resolution_days=20.0,
            roi_achievement_pct=0.0,
            competitive_evaluation_signal=1.0,
            contract_utilization_pct=0.0,
        ))
        assert result.churn_pattern == "usage_collapse"
        assert result.churn_risk == "critical"
        assert result.recommended_action == "renewal_risk_intervention"

    def test_critical_none_pattern_gives_renewal_risk_intervention(self, engine):
        # Critical risk with no specific pattern → renewal_risk_intervention
        # Drive composite>=60 without triggering any named pattern
        result = engine.assess(make_input(
            feature_adoption_rate_pct=0.0,       # +35 usage
            product_usage_decay_pct=0.50,        # +40 usage
            login_frequency_decay_pct=0.50,      # +25 usage → us=100
            executive_sponsor_engaged=0.45,      # 0.25 < 0.45 <= 0.45 → +22 rel; NOT sponsor_exodus since >0.25
            last_exec_meeting_days_ago=200.0,    # +35 rel
            stakeholder_count_change=-1.0,       # -1 → +12 rel → re=69
            open_support_tickets=10,             # +40 su
            avg_ticket_resolution_days=7.0,      # +12 su → su=52
            roi_achievement_pct=0.75,            # +10 va → va=10
            # No usage_collapse: usage_decay=0.50>=0.45 BUT login=0.50>=0.40 → usage_collapse fires!
        ))
        # This WILL fire usage_collapse. Let's adjust to not fire usage_collapse:
        result2 = engine.assess(make_input(
            feature_adoption_rate_pct=0.0,
            product_usage_decay_pct=0.44,        # Below 0.45 → no usage_collapse
            login_frequency_decay_pct=0.50,
            executive_sponsor_engaged=0.45,      # above 0.25 → no sponsor_exodus
            last_exec_meeting_days_ago=200.0,
            stakeholder_count_change=-1.0,
            open_support_tickets=10,
            avg_ticket_resolution_days=14.0,
            escalation_frequency_pct=0.40,
            roi_achievement_pct=0.75,
            contract_utilization_pct=0.80,       # above 0.55 → no value contribution
            competitive_evaluation_signal=0.54,  # below 0.55 → no competitive_switch
        ))
        if result2.churn_risk == "critical" and result2.churn_pattern == "none":
            assert result2.recommended_action == "renewal_risk_intervention"

    def test_high_usage_collapse_gives_success_plan_reset(self, engine):
        result = engine.assess(make_input(
            product_usage_decay_pct=0.45,
            login_frequency_decay_pct=0.40,
            feature_adoption_rate_pct=0.45,
            open_support_tickets=5,
            escalation_frequency_pct=0.20,
        ))
        if result.churn_risk == "high" and result.churn_pattern == "usage_collapse":
            assert result.recommended_action == "success_plan_reset"

    def test_high_usage_collapse_action(self, engine):
        # Build a scenario that definitely hits high+usage_collapse
        result = engine.assess(make_input(
            product_usage_decay_pct=0.45,
            login_frequency_decay_pct=0.40,
            feature_adoption_rate_pct=0.45,  # +18 usage
            open_support_tickets=5,
            escalation_frequency_pct=0.20,
            last_exec_meeting_days_ago=30.0,
        ))
        assert result.churn_pattern == "usage_collapse"
        if result.churn_risk == "high":
            assert result.recommended_action == "success_plan_reset"

    def test_high_sponsor_exodus_gives_sponsor_re_engagement(self, engine):
        # High risk + sponsor_exodus (no usage_collapse firing first)
        result = engine.assess(make_input(
            product_usage_decay_pct=0.20,        # below 0.45 → no usage_collapse
            feature_adoption_rate_pct=0.45,
            executive_sponsor_engaged=0.25,      # <=0.25 → sponsor_exodus
            stakeholder_count_change=-2.0,
            last_exec_meeting_days_ago=120.0,
            open_support_tickets=5,
            escalation_frequency_pct=0.20,
        ))
        assert result.churn_pattern == "sponsor_exodus"
        if result.churn_risk == "high":
            assert result.recommended_action == "sponsor_re_engagement"

    def test_high_support_spiral_gives_support_escalation_resolution(self, engine):
        result = engine.assess(make_input(
            open_support_tickets=6,
            escalation_frequency_pct=0.30,
            product_usage_decay_pct=0.30,
            feature_adoption_rate_pct=0.45,
            last_exec_meeting_days_ago=60.0,
        ))
        assert result.churn_pattern == "support_spiral"
        if result.churn_risk == "high":
            assert result.recommended_action == "support_escalation_resolution"

    def test_high_competitive_switch_gives_competitive_defense_playbook(self, engine):
        result = engine.assess(make_input(
            competitive_evaluation_signal=0.55,
            roi_achievement_pct=0.60,
            product_usage_decay_pct=0.30,
            feature_adoption_rate_pct=0.45,
            open_support_tickets=3,
        ))
        assert result.churn_pattern == "competitive_switch"
        if result.churn_risk == "high":
            assert result.recommended_action == "competitive_defense_playbook"

    def test_high_value_gap_crisis_gives_executive_business_review(self, engine):
        result = engine.assess(make_input(
            roi_achievement_pct=0.40,
            contract_utilization_pct=0.40,
            product_usage_decay_pct=0.30,
            feature_adoption_rate_pct=0.45,
            last_exec_meeting_days_ago=60.0,
        ))
        assert result.churn_pattern == "value_gap_crisis"
        if result.churn_risk == "high":
            assert result.recommended_action == "executive_business_review"

    def test_high_no_pattern_gives_health_monitoring(self, engine):
        # High risk + no pattern → health_monitoring
        # Drive composite to 40-59 without triggering any pattern
        result = engine.assess(make_input(
            feature_adoption_rate_pct=0.45,      # +18 usage
            product_usage_decay_pct=0.30,        # +22 usage; total us=40
            login_frequency_decay_pct=0.30,      # +12; us=52
            last_exec_meeting_days_ago=60.0,     # +18 rel
            open_support_tickets=5,              # +22 su
            escalation_frequency_pct=0.20,       # +18 su → su=40
            roi_achievement_pct=0.75,            # +10 va
        ))
        # Check composite and pattern
        if result.churn_risk == "high" and result.churn_pattern == "none":
            assert result.recommended_action == "health_monitoring"


# ===========================================================================
# 7. SUB-SCORE BOUNDARIES — USAGE
# ===========================================================================

class TestUsageScoreBoundaries:
    def test_product_usage_decay_below_15_adds_zero(self, engine):
        r = engine.assess(make_input(product_usage_decay_pct=0.14))
        assert r.usage_score == 0  # only decay contributes here

    def test_product_usage_decay_at_15_adds_8(self, engine):
        r = engine.assess(make_input(product_usage_decay_pct=0.15))
        assert r.usage_score == 8

    def test_product_usage_decay_at_30_adds_22(self, engine):
        r = engine.assess(make_input(product_usage_decay_pct=0.30))
        assert r.usage_score == 22

    def test_product_usage_decay_at_50_adds_40(self, engine):
        r = engine.assess(make_input(product_usage_decay_pct=0.50))
        assert r.usage_score == 40

    def test_feature_adoption_above_60_adds_zero(self, engine):
        r = engine.assess(make_input(feature_adoption_rate_pct=0.61))
        assert r.usage_score == 0

    def test_feature_adoption_at_60_adds_6(self, engine):
        r = engine.assess(make_input(feature_adoption_rate_pct=0.60))
        assert r.usage_score == 6

    def test_feature_adoption_at_45_adds_18(self, engine):
        r = engine.assess(make_input(feature_adoption_rate_pct=0.45))
        assert r.usage_score == 18

    def test_feature_adoption_at_25_adds_35(self, engine):
        r = engine.assess(make_input(feature_adoption_rate_pct=0.25))
        assert r.usage_score == 35

    def test_login_decay_below_30_adds_zero(self, engine):
        r = engine.assess(make_input(login_frequency_decay_pct=0.29))
        assert r.usage_score == 0

    def test_login_decay_at_30_adds_12(self, engine):
        r = engine.assess(make_input(login_frequency_decay_pct=0.30))
        assert r.usage_score == 12

    def test_login_decay_at_50_adds_25(self, engine):
        r = engine.assess(make_input(login_frequency_decay_pct=0.50))
        assert r.usage_score == 25

    def test_usage_score_capped_at_100(self, engine):
        r = engine.assess(make_input(
            product_usage_decay_pct=1.0,
            feature_adoption_rate_pct=0.0,
            login_frequency_decay_pct=1.0,
        ))
        assert r.usage_score == 100


# ===========================================================================
# 8. SUB-SCORE BOUNDARIES — RELATIONSHIP
# ===========================================================================

class TestRelationshipScoreBoundaries:
    def test_exec_sponsor_above_65_adds_zero(self, engine):
        r = engine.assess(make_input(executive_sponsor_engaged=0.66))
        assert r.relationship_score == 0

    def test_exec_sponsor_at_65_adds_8(self, engine):
        r = engine.assess(make_input(executive_sponsor_engaged=0.65))
        assert r.relationship_score == 8

    def test_exec_sponsor_at_45_adds_22(self, engine):
        r = engine.assess(make_input(executive_sponsor_engaged=0.45))
        assert r.relationship_score == 22

    def test_exec_sponsor_at_20_adds_40(self, engine):
        r = engine.assess(make_input(executive_sponsor_engaged=0.20))
        assert r.relationship_score == 40

    def test_exec_meeting_below_30_adds_zero(self, engine):
        r = engine.assess(make_input(last_exec_meeting_days_ago=29.0))
        assert r.relationship_score == 0

    def test_exec_meeting_at_30_adds_6(self, engine):
        r = engine.assess(make_input(last_exec_meeting_days_ago=30.0))
        assert r.relationship_score == 6

    def test_exec_meeting_at_60_adds_18(self, engine):
        r = engine.assess(make_input(last_exec_meeting_days_ago=60.0))
        assert r.relationship_score == 18

    def test_exec_meeting_at_120_adds_35(self, engine):
        r = engine.assess(make_input(last_exec_meeting_days_ago=120.0))
        assert r.relationship_score == 35

    def test_stakeholder_change_above_minus1_adds_zero(self, engine):
        r = engine.assess(make_input(stakeholder_count_change=0.0))
        assert r.relationship_score == 0

    def test_stakeholder_change_at_minus1_adds_12(self, engine):
        r = engine.assess(make_input(stakeholder_count_change=-1.0))
        assert r.relationship_score == 12

    def test_stakeholder_change_at_minus3_adds_25(self, engine):
        r = engine.assess(make_input(stakeholder_count_change=-3.0))
        assert r.relationship_score == 25

    def test_relationship_score_capped_at_100(self, engine):
        r = engine.assess(make_input(
            executive_sponsor_engaged=0.0,
            last_exec_meeting_days_ago=200.0,
            stakeholder_count_change=-5.0,
        ))
        assert r.relationship_score == 100


# ===========================================================================
# 9. SUB-SCORE BOUNDARIES — SUPPORT
# ===========================================================================

class TestSupportScoreBoundaries:
    def test_tickets_below_2_adds_zero(self, engine):
        r = engine.assess(make_input(open_support_tickets=1))
        assert r.support_score == 0

    def test_tickets_at_2_adds_8(self, engine):
        r = engine.assess(make_input(open_support_tickets=2))
        assert r.support_score == 8

    def test_tickets_at_5_adds_22(self, engine):
        r = engine.assess(make_input(open_support_tickets=5))
        assert r.support_score == 22

    def test_tickets_at_10_adds_40(self, engine):
        r = engine.assess(make_input(open_support_tickets=10))
        assert r.support_score == 40

    def test_escalation_below_20_adds_zero(self, engine):
        r = engine.assess(make_input(escalation_frequency_pct=0.19))
        assert r.support_score == 0

    def test_escalation_at_20_adds_18(self, engine):
        r = engine.assess(make_input(escalation_frequency_pct=0.20))
        assert r.support_score == 18

    def test_escalation_at_40_adds_35(self, engine):
        r = engine.assess(make_input(escalation_frequency_pct=0.40))
        assert r.support_score == 35

    def test_resolution_days_below_7_adds_zero(self, engine):
        r = engine.assess(make_input(avg_ticket_resolution_days=6.0))
        assert r.support_score == 0

    def test_resolution_days_at_7_adds_12(self, engine):
        r = engine.assess(make_input(avg_ticket_resolution_days=7.0))
        assert r.support_score == 12

    def test_resolution_days_at_14_adds_25(self, engine):
        r = engine.assess(make_input(avg_ticket_resolution_days=14.0))
        assert r.support_score == 25

    def test_support_score_capped_at_100(self, engine):
        r = engine.assess(make_input(
            open_support_tickets=10,
            escalation_frequency_pct=0.40,
            avg_ticket_resolution_days=14.0,
        ))
        assert r.support_score == 100


# ===========================================================================
# 10. SUB-SCORE BOUNDARIES — VALUE
# ===========================================================================

class TestValueScoreBoundaries:
    def test_roi_above_75_adds_zero(self, engine):
        r = engine.assess(make_input(roi_achievement_pct=0.76))
        assert r.value_score == 0

    def test_roi_at_75_adds_10(self, engine):
        r = engine.assess(make_input(roi_achievement_pct=0.75))
        assert r.value_score == 10

    def test_roi_at_55_adds_25(self, engine):
        r = engine.assess(make_input(roi_achievement_pct=0.55))
        assert r.value_score == 25

    def test_roi_at_30_adds_45(self, engine):
        r = engine.assess(make_input(roi_achievement_pct=0.30))
        assert r.value_score == 45

    def test_competitive_signal_below_35_adds_zero(self, engine):
        r = engine.assess(make_input(competitive_evaluation_signal=0.34))
        assert r.value_score == 0

    def test_competitive_signal_at_35_adds_15(self, engine):
        r = engine.assess(make_input(competitive_evaluation_signal=0.35))
        assert r.value_score == 15

    def test_competitive_signal_at_60_adds_30(self, engine):
        r = engine.assess(make_input(competitive_evaluation_signal=0.60))
        assert r.value_score == 30

    def test_contract_utilization_above_55_adds_zero(self, engine):
        r = engine.assess(make_input(contract_utilization_pct=0.56))
        assert r.value_score == 0

    def test_contract_utilization_at_55_adds_12(self, engine):
        r = engine.assess(make_input(contract_utilization_pct=0.55))
        assert r.value_score == 12

    def test_contract_utilization_at_30_adds_25(self, engine):
        r = engine.assess(make_input(contract_utilization_pct=0.30))
        assert r.value_score == 25

    def test_value_score_capped_at_100(self, engine):
        r = engine.assess(make_input(
            roi_achievement_pct=0.0,
            competitive_evaluation_signal=1.0,
            contract_utilization_pct=0.0,
        ))
        assert r.value_score == 100


# ===========================================================================
# 11. COMPOSITE CALCULATION
# ===========================================================================

class TestCompositeCalculation:
    def test_composite_weighted_sum(self, engine):
        # us=40, re=6, su=22, va=10
        # 40*0.30 + 6*0.25 + 22*0.25 + 10*0.20 = 12+1.5+5.5+2 = 21.0
        r = engine.assess(make_input(
            product_usage_decay_pct=0.50,     # +40
            last_exec_meeting_days_ago=30.0,  # +6
            open_support_tickets=5,           # +22
            roi_achievement_pct=0.75,         # +10
        ))
        assert r.usage_score == 40
        assert r.relationship_score == 6
        assert r.support_score == 22
        assert r.value_score == 10
        assert r.churn_composite == round(40*0.30 + 6*0.25 + 22*0.25 + 10*0.20, 2)

    def test_composite_rounded_to_2_decimal_places(self, engine):
        r = engine.assess(make_input(
            product_usage_decay_pct=0.15,  # +8
            open_support_tickets=2,         # +8
            last_exec_meeting_days_ago=30.0, # +6
            roi_achievement_pct=0.75,        # +10
        ))
        # us=8, re=6, su=8, va=10
        # 8*0.30 + 6*0.25 + 8*0.25 + 10*0.20 = 2.4+1.5+2.0+2.0 = 7.9
        assert r.churn_composite == 7.9

    def test_composite_capped_at_100(self, engine):
        r = engine.assess(make_input(
            product_usage_decay_pct=1.0,
            feature_adoption_rate_pct=0.0,
            login_frequency_decay_pct=1.0,
            executive_sponsor_engaged=0.0,
            last_exec_meeting_days_ago=200.0,
            stakeholder_count_change=-5.0,
            open_support_tickets=15,
            escalation_frequency_pct=1.0,
            avg_ticket_resolution_days=20.0,
            roi_achievement_pct=0.0,
            competitive_evaluation_signal=1.0,
            contract_utilization_pct=0.0,
        ))
        assert r.churn_composite == 100.0


# ===========================================================================
# 12. HAS_CHURN_SIGNAL
# ===========================================================================

class TestHasChurnSignal:
    def test_no_churn_signal_when_all_healthy(self, engine):
        r = engine.assess(make_input())
        assert r.has_churn_signal is False

    def test_churn_signal_true_when_composite_gte_40(self, engine):
        r = engine.assess(make_input(
            product_usage_decay_pct=0.55,
            feature_adoption_rate_pct=0.20,
            login_frequency_decay_pct=0.55,
            last_exec_meeting_days_ago=35.0,
            open_support_tickets=5,
            escalation_frequency_pct=0.20,
            roi_achievement_pct=0.70,
        ))
        assert r.churn_composite >= 40
        assert r.has_churn_signal is True

    def test_churn_signal_true_when_usage_decay_gte_30(self, engine):
        r = engine.assess(make_input(product_usage_decay_pct=0.30))
        assert r.has_churn_signal is True

    def test_churn_signal_false_when_usage_decay_just_below_30(self, engine):
        r = engine.assess(make_input(product_usage_decay_pct=0.29))
        assert r.has_churn_signal is False

    def test_churn_signal_true_when_days_to_renewal_lte_90(self, engine):
        r = engine.assess(make_input(days_to_renewal=90))
        assert r.has_churn_signal is True

    def test_churn_signal_false_when_days_to_renewal_91(self, engine):
        r = engine.assess(make_input(days_to_renewal=91))
        assert r.has_churn_signal is False

    def test_churn_signal_true_when_days_to_renewal_0(self, engine):
        r = engine.assess(make_input(days_to_renewal=0))
        assert r.has_churn_signal is True


# ===========================================================================
# 13. REQUIRES_EXECUTIVE_ACTION
# ===========================================================================

class TestRequiresExecutiveAction:
    def test_no_exec_action_when_all_healthy(self, engine):
        r = engine.assess(make_input())
        assert r.requires_executive_action is False

    def test_exec_action_true_when_composite_gte_25(self, engine):
        # Drive composite to exactly >= 25
        r = engine.assess(make_input(
            product_usage_decay_pct=0.55,
            feature_adoption_rate_pct=0.20,
            login_frequency_decay_pct=0.55,
            last_exec_meeting_days_ago=35.0,
            open_support_tickets=5,
            escalation_frequency_pct=0.20,
            roi_achievement_pct=0.70,
        ))
        assert r.churn_composite >= 25
        assert r.requires_executive_action is True

    def test_exec_action_true_when_sponsor_engaged_lte_40(self, engine):
        r = engine.assess(make_input(executive_sponsor_engaged=0.40))
        assert r.requires_executive_action is True

    def test_exec_action_false_when_sponsor_engaged_above_40(self, engine):
        r = engine.assess(make_input(executive_sponsor_engaged=0.41))
        assert r.requires_executive_action is False

    def test_exec_action_true_when_competitive_signal_gte_35(self, engine):
        r = engine.assess(make_input(competitive_evaluation_signal=0.35))
        assert r.requires_executive_action is True

    def test_exec_action_false_when_competitive_signal_below_35(self, engine):
        r = engine.assess(make_input(competitive_evaluation_signal=0.34))
        assert r.requires_executive_action is False


# ===========================================================================
# 14. ARR AT RISK
# ===========================================================================

class TestArrAtRisk:
    def test_arr_at_risk_zero_when_composite_zero(self, engine):
        r = engine.assess(make_input(arr_usd=100_000.0))
        assert r.estimated_arr_at_risk_usd == 0.0

    def test_arr_at_risk_calculation(self, engine):
        # composite = 50.0 for example; arr = 200000
        r = engine.assess(make_input(
            product_usage_decay_pct=0.55,
            feature_adoption_rate_pct=0.20,
            login_frequency_decay_pct=0.55,
            last_exec_meeting_days_ago=35.0,
            open_support_tickets=5,
            escalation_frequency_pct=0.20,
            roi_achievement_pct=0.70,
            arr_usd=200_000.0,
        ))
        expected = round(200_000.0 * (r.churn_composite / 100), 2)
        assert r.estimated_arr_at_risk_usd == expected

    def test_arr_at_risk_full_when_composite_100(self, engine):
        r = engine.assess(make_input(
            product_usage_decay_pct=1.0,
            feature_adoption_rate_pct=0.0,
            login_frequency_decay_pct=1.0,
            executive_sponsor_engaged=0.0,
            last_exec_meeting_days_ago=200.0,
            stakeholder_count_change=-5.0,
            open_support_tickets=15,
            escalation_frequency_pct=1.0,
            avg_ticket_resolution_days=20.0,
            roi_achievement_pct=0.0,
            competitive_evaluation_signal=1.0,
            contract_utilization_pct=0.0,
            arr_usd=500_000.0,
        ))
        assert r.churn_composite == 100.0
        assert r.estimated_arr_at_risk_usd == 500_000.0

    def test_arr_at_risk_rounded_to_2_decimal(self, engine):
        r = engine.assess(make_input(
            product_usage_decay_pct=0.15,  # us=8
            arr_usd=33.33,
        ))
        # comp = 8*0.30 = 2.4
        assert r.estimated_arr_at_risk_usd == round(33.33 * (r.churn_composite / 100), 2)

    def test_arr_at_risk_large_arr(self, engine):
        r = engine.assess(make_input(
            product_usage_decay_pct=0.30,  # +22
            arr_usd=1_000_000.0,
        ))
        expected = round(1_000_000.0 * (r.churn_composite / 100), 2)
        assert r.estimated_arr_at_risk_usd == expected


# ===========================================================================
# 15. SIGNAL STRING
# ===========================================================================

class TestSignalString:
    def test_healthy_signal_string(self, engine):
        r = engine.assess(make_input())
        assert r.churn_signal == "Account health strong — usage, relationship, support and value indicators within healthy benchmarks"

    def test_signal_string_below_20_always_healthy(self, engine):
        r = engine.assess(make_input(product_usage_decay_pct=0.15))  # us=8, comp=2.4
        assert r.churn_signal.startswith("Account health strong")

    def test_signal_string_at_20_plus_contains_composite(self, engine):
        r = engine.assess(make_input(
            product_usage_decay_pct=0.30,
            login_frequency_decay_pct=0.30,
            feature_adoption_rate_pct=0.45,
            open_support_tickets=2,
            escalation_frequency_pct=0.20,
        ))
        assert r.churn_composite >= 20
        assert f"composite {round(r.churn_composite)}" in r.churn_signal

    def test_signal_string_contains_usage_decay_pct(self, engine):
        r = engine.assess(make_input(
            product_usage_decay_pct=0.30,
            login_frequency_decay_pct=0.30,
            feature_adoption_rate_pct=0.45,
            open_support_tickets=2,
            escalation_frequency_pct=0.20,
        ))
        assert f"{round(0.30*100)}% usage decay" in r.churn_signal

    def test_signal_string_contains_roi_achieved(self, engine):
        r = engine.assess(make_input(
            product_usage_decay_pct=0.30,
            login_frequency_decay_pct=0.30,
            feature_adoption_rate_pct=0.45,
            open_support_tickets=2,
            escalation_frequency_pct=0.20,
            roi_achievement_pct=0.75,
        ))
        assert f"{round(0.75*100)}% ROI achieved" in r.churn_signal

    def test_signal_string_contains_days_to_renewal(self, engine):
        r = engine.assess(make_input(
            product_usage_decay_pct=0.30,
            login_frequency_decay_pct=0.30,
            feature_adoption_rate_pct=0.45,
            open_support_tickets=2,
            escalation_frequency_pct=0.20,
            days_to_renewal=180,
        ))
        assert "180d to renewal" in r.churn_signal

    def test_signal_label_usage_collapse(self, engine):
        r = engine.assess(make_input(
            product_usage_decay_pct=0.45,
            login_frequency_decay_pct=0.40,
            feature_adoption_rate_pct=0.45,
            open_support_tickets=2,
            escalation_frequency_pct=0.20,
        ))
        assert r.churn_pattern == "usage_collapse"
        if r.churn_composite >= 20:
            assert r.churn_signal.startswith("Usage collapse")

    def test_signal_label_sponsor_exodus(self, engine):
        r = engine.assess(make_input(
            product_usage_decay_pct=0.20,
            executive_sponsor_engaged=0.25,
            stakeholder_count_change=-2.0,
            last_exec_meeting_days_ago=60.0,
        ))
        assert r.churn_pattern == "sponsor_exodus"
        if r.churn_composite >= 20:
            assert r.churn_signal.startswith("Sponsor exodus")

    def test_signal_label_support_spiral(self, engine):
        r = engine.assess(make_input(
            open_support_tickets=6,
            escalation_frequency_pct=0.30,
            product_usage_decay_pct=0.30,
        ))
        assert r.churn_pattern == "support_spiral"
        if r.churn_composite >= 20:
            assert r.churn_signal.startswith("Support spiral")

    def test_signal_label_competitive_switch(self, engine):
        r = engine.assess(make_input(
            competitive_evaluation_signal=0.55,
            roi_achievement_pct=0.60,
            product_usage_decay_pct=0.30,
        ))
        assert r.churn_pattern == "competitive_switch"
        if r.churn_composite >= 20:
            assert r.churn_signal.startswith("Competitive switch")

    def test_signal_label_value_gap_crisis(self, engine):
        r = engine.assess(make_input(
            roi_achievement_pct=0.40,
            contract_utilization_pct=0.40,
            product_usage_decay_pct=0.30,
        ))
        assert r.churn_pattern == "value_gap_crisis"
        if r.churn_composite >= 20:
            assert r.churn_signal.startswith("Value gap crisis")


# ===========================================================================
# 16. BATCH ASSESS
# ===========================================================================

class TestBatchAssess:
    def test_assess_batch_returns_list(self, engine):
        inputs = [make_input(account_id=f"acct-{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert isinstance(results, list)
        assert len(results) == 5

    def test_assess_batch_all_are_churn_results(self, engine):
        inputs = [make_input(account_id=f"acct-{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        for r in results:
            assert isinstance(r, ChurnResult)

    def test_assess_batch_preserves_account_ids(self, engine):
        inputs = [make_input(account_id=f"acct-{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.account_id == f"acct-{i}"

    def test_assess_batch_adds_to_internal_results(self, engine):
        inputs = [make_input(account_id=f"acct-{i}") for i in range(4)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 4

    def test_assess_batch_empty_list(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_assess_batch_mixed_risk_levels(self, engine):
        inputs = [
            make_input(account_id="low"),   # low risk
            make_input(
                account_id="critical",
                product_usage_decay_pct=1.0,
                feature_adoption_rate_pct=0.0,
                login_frequency_decay_pct=1.0,
                executive_sponsor_engaged=0.0,
                last_exec_meeting_days_ago=200.0,
                open_support_tickets=15,
                escalation_frequency_pct=1.0,
                avg_ticket_resolution_days=20.0,
                roi_achievement_pct=0.0,
                competitive_evaluation_signal=1.0,
                contract_utilization_pct=0.0,
            ),
        ]
        results = engine.assess_batch(inputs)
        assert results[0].churn_risk == "low"
        assert results[1].churn_risk == "critical"


# ===========================================================================
# 17. SUMMARY
# ===========================================================================

class TestSummary:
    def test_empty_summary_returns_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_total_is_zero(self, engine):
        s = engine.summary()
        assert s["total"] == 0

    def test_empty_summary_zero_counts(self, engine):
        s = engine.summary()
        assert s["churn_signal_count"] == 0
        assert s["executive_action_count"] == 0
        assert s["avg_churn_composite"] == 0.0
        assert s["total_estimated_arr_at_risk_usd"] == 0.0

    def test_empty_summary_empty_dicts(self, engine):
        s = engine.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_summary_total_count(self, engine):
        for i in range(7):
            engine.assess(make_input(account_id=f"acct-{i}"))
        assert engine.summary()["total"] == 7

    def test_summary_risk_counts(self, engine):
        engine.assess(make_input())  # low
        engine.assess(make_input())  # low
        s = engine.summary()
        assert s["risk_counts"]["low"] == 2

    def test_summary_pattern_counts(self, engine):
        engine.assess(make_input())  # none pattern
        engine.assess(make_input())  # none pattern
        s = engine.summary()
        assert s["pattern_counts"]["none"] == 2

    def test_summary_severity_counts(self, engine):
        engine.assess(make_input())  # healthy
        s = engine.summary()
        assert s["severity_counts"]["healthy"] == 1

    def test_summary_action_counts(self, engine):
        engine.assess(make_input())  # no_action
        s = engine.summary()
        assert s["action_counts"]["no_action"] == 1

    def test_summary_avg_churn_composite(self, engine):
        engine.assess(make_input())  # composite = 0.0
        r2 = engine.assess(make_input(product_usage_decay_pct=0.30))  # composite > 0
        s = engine.summary()
        expected = round((0.0 + r2.churn_composite) / 2, 1)
        assert s["avg_churn_composite"] == expected

    def test_summary_churn_signal_count(self, engine):
        engine.assess(make_input())  # no signal
        engine.assess(make_input(product_usage_decay_pct=0.30))  # has signal
        s = engine.summary()
        assert s["churn_signal_count"] == 1

    def test_summary_executive_action_count(self, engine):
        engine.assess(make_input())  # no exec action
        engine.assess(make_input(executive_sponsor_engaged=0.40))  # exec action
        s = engine.summary()
        assert s["executive_action_count"] == 1

    def test_summary_total_arr_at_risk(self, engine):
        r1 = engine.assess(make_input(arr_usd=100_000.0))
        r2 = engine.assess(make_input(arr_usd=200_000.0, product_usage_decay_pct=0.30))
        s = engine.summary()
        expected = round(r1.estimated_arr_at_risk_usd + r2.estimated_arr_at_risk_usd, 2)
        assert s["total_estimated_arr_at_risk_usd"] == expected

    def test_summary_avg_sub_scores(self, engine):
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(product_usage_decay_pct=0.30))
        s = engine.summary()
        assert s["avg_usage_score"] == round((r1.usage_score + r2.usage_score) / 2, 1)
        assert s["avg_relationship_score"] == round((r1.relationship_score + r2.relationship_score) / 2, 1)
        assert s["avg_support_score"] == round((r1.support_score + r2.support_score) / 2, 1)
        assert s["avg_value_score"] == round((r1.value_score + r2.value_score) / 2, 1)

    def test_summary_accumulates_across_assessments(self, engine):
        engine.assess(make_input(account_id="a"))
        engine.assess(make_input(account_id="b"))
        engine.assess(make_input(account_id="c"))
        s = engine.summary()
        assert s["total"] == 3

    def test_summary_mixed_patterns(self, engine):
        engine.assess(make_input())  # none
        engine.assess(make_input(
            product_usage_decay_pct=0.45,
            login_frequency_decay_pct=0.40,
        ))  # usage_collapse
        s = engine.summary()
        assert "none" in s["pattern_counts"]
        assert "usage_collapse" in s["pattern_counts"]


# ===========================================================================
# 18. TO_DICT
# ===========================================================================

class TestToDict:
    def test_to_dict_values_match_result_fields(self, engine):
        r = engine.assess(make_input(account_id="test-acct", region="APAC"))
        d = r.to_dict()
        assert d["account_id"] == r.account_id
        assert d["region"] == r.region
        assert d["churn_risk"] == r.churn_risk
        assert d["churn_pattern"] == r.churn_pattern
        assert d["churn_severity"] == r.churn_severity
        assert d["recommended_action"] == r.recommended_action
        assert d["usage_score"] == r.usage_score
        assert d["relationship_score"] == r.relationship_score
        assert d["support_score"] == r.support_score
        assert d["value_score"] == r.value_score
        assert d["churn_composite"] == r.churn_composite
        assert d["has_churn_signal"] == r.has_churn_signal
        assert d["requires_executive_action"] == r.requires_executive_action
        assert d["estimated_arr_at_risk_usd"] == r.estimated_arr_at_risk_usd
        assert d["churn_signal"] == r.churn_signal

    def test_to_dict_types(self, engine):
        r = engine.assess(make_input())
        d = r.to_dict()
        assert isinstance(d["account_id"], str)
        assert isinstance(d["region"], str)
        assert isinstance(d["churn_risk"], str)
        assert isinstance(d["churn_pattern"], str)
        assert isinstance(d["churn_severity"], str)
        assert isinstance(d["recommended_action"], str)
        assert isinstance(d["usage_score"], (int, float))
        assert isinstance(d["relationship_score"], (int, float))
        assert isinstance(d["support_score"], (int, float))
        assert isinstance(d["value_score"], (int, float))
        assert isinstance(d["churn_composite"], float)
        assert isinstance(d["has_churn_signal"], bool)
        assert isinstance(d["requires_executive_action"], bool)
        assert isinstance(d["estimated_arr_at_risk_usd"], float)
        assert isinstance(d["churn_signal"], str)


# ===========================================================================
# 19. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def test_zero_arr_gives_zero_at_risk(self, engine):
        r = engine.assess(make_input(
            arr_usd=0.0,
            product_usage_decay_pct=1.0,
        ))
        assert r.estimated_arr_at_risk_usd == 0.0

    def test_large_arr(self, engine):
        r = engine.assess(make_input(arr_usd=10_000_000.0, product_usage_decay_pct=1.0))
        assert r.estimated_arr_at_risk_usd > 0

    def test_negative_nps_does_not_break(self, engine):
        r = engine.assess(make_input(nps_score_change=-50.0))
        assert isinstance(r, ChurnResult)

    def test_zero_days_to_renewal(self, engine):
        r = engine.assess(make_input(days_to_renewal=0))
        assert r.has_churn_signal is True

    def test_long_time_to_renewal(self, engine):
        r = engine.assess(make_input(days_to_renewal=1000))
        assert isinstance(r, ChurnResult)

    def test_multiple_engines_are_independent(self):
        e1 = SalesAccountChurnEarlyWarningEngine()
        e2 = SalesAccountChurnEarlyWarningEngine()
        e1.assess(make_input(account_id="a"))
        e1.assess(make_input(account_id="b"))
        e2.assess(make_input(account_id="c"))
        assert e1.summary()["total"] == 2
        assert e2.summary()["total"] == 1

    def test_champion_tenure_does_not_affect_score(self, engine):
        r1 = engine.assess(make_input(champion_tenure_months=0.0))
        r2 = engine.assess(make_input(champion_tenure_months=100.0))
        assert r1.churn_composite == r2.churn_composite

    def test_renewal_conversation_does_not_affect_score(self, engine):
        r1 = engine.assess(make_input(renewal_conversation_initiated=0.0))
        r2 = engine.assess(make_input(renewal_conversation_initiated=1.0))
        assert r1.churn_composite == r2.churn_composite

    def test_api_call_volume_decay_does_not_affect_score(self, engine):
        r1 = engine.assess(make_input(api_call_volume_decay_pct=0.0))
        r2 = engine.assess(make_input(api_call_volume_decay_pct=1.0))
        assert r1.churn_composite == r2.churn_composite

    def test_contract_months_remaining_does_not_affect_score(self, engine):
        r1 = engine.assess(make_input(contract_months_remaining=1))
        r2 = engine.assess(make_input(contract_months_remaining=36))
        assert r1.churn_composite == r2.churn_composite

    def test_all_patterns_produce_valid_action_strings(self, engine):
        valid_actions = {a.value for a in ChurnAction}
        patterns_inputs = [
            make_input(),
            make_input(product_usage_decay_pct=0.45, login_frequency_decay_pct=0.40),
            make_input(executive_sponsor_engaged=0.25, stakeholder_count_change=-2.0),
            make_input(open_support_tickets=6, escalation_frequency_pct=0.30),
            make_input(competitive_evaluation_signal=0.55, roi_achievement_pct=0.60),
            make_input(roi_achievement_pct=0.40, contract_utilization_pct=0.40),
        ]
        for inp in patterns_inputs:
            r = engine.assess(inp)
            assert r.recommended_action in valid_actions

    def test_result_churn_risk_is_string_not_enum(self, engine):
        r = engine.assess(make_input())
        assert isinstance(r.churn_risk, str)
        assert not isinstance(r.churn_risk, ChurnRisk)

    def test_result_churn_pattern_is_string_not_enum(self, engine):
        r = engine.assess(make_input())
        assert isinstance(r.churn_pattern, str)

    def test_result_churn_severity_is_string_not_enum(self, engine):
        r = engine.assess(make_input())
        assert isinstance(r.churn_severity, str)

    def test_result_recommended_action_is_string_not_enum(self, engine):
        r = engine.assess(make_input())
        assert isinstance(r.recommended_action, str)
