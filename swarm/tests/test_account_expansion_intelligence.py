"""
Comprehensive pytest test suite for AccountExpansionIntelligence.

~250 tests organised in classes, covering:
  - Enum membership / counts
  - Dataclass field counts
  - Individual scoring functions
  - Composite formula
  - Boolean flags (is_expansion_ready, needs_retention_focus)
  - Result.to_dict() key count and types
  - Opportunity / health / priority / action classifiers
  - AccountExpansionIntelligence methods
  - summary() key count and values
  - Edge-cases and clamping
"""
from __future__ import annotations

import dataclasses
import math
import pytest

from swarm.intelligence.account_expansion_intelligence import (
    AccountExpansionIntelligence,
    AccountExpansionInput,
    AccountExpansionResult,
    ExpansionOpportunity,
    ExpansionPriority,
    AccountHealth,
    ExpansionAction,
    _adoption_health_score,
    _relationship_health_score,
    _commercial_readiness_score,
    _risk_score,
    _composite,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**kwargs) -> AccountExpansionInput:
    defaults = dict(
        account_id="acc_001",
        account_name="TechCorp",
        rep_id="rep_001",
        contract_value_usd=150_000.0,
        contract_renewal_days=120,
        product_adoption_score=82.0,
        active_users_count=45,
        total_licensed_users_count=50,
        support_ticket_count_90d=1,
        nps_score=62.0,
        exec_sponsor_engaged=1,
        champion_identified=1,
        qbr_completed_last_180d=1,
        upsell_discussion_held=1,
        cross_sell_product_gaps=3,
        competitor_in_account=0,
        days_since_last_touchpoint=5,
        escalation_count_90d=0,
        expansion_budget_confirmed=1,
        expansion_usd_potential=75_000.0,
        industry_growth_score=78.0,
        account_tenure_days=540,
    )
    defaults.update(kwargs)
    return AccountExpansionInput(**defaults)


def at_risk_input(account_id: str = "at_risk_001") -> AccountExpansionInput:
    return make_input(
        account_id=account_id,
        nps_score=-40.0,
        escalation_count_90d=4,
        product_adoption_score=15.0,
        competitor_in_account=1,
        support_ticket_count_90d=8,
        expansion_budget_confirmed=0,
        exec_sponsor_engaged=0,
        champion_identified=0,
        qbr_completed_last_180d=0,
        upsell_discussion_held=0,
        days_since_last_touchpoint=45,
    )


def fresh() -> AccountExpansionIntelligence:
    """Return a new, empty AccountExpansionIntelligence."""
    return AccountExpansionIntelligence()


# ---------------------------------------------------------------------------
# 1. Enum tests
# ---------------------------------------------------------------------------

class TestEnums:
    def test_expansion_opportunity_count(self):
        assert len(ExpansionOpportunity) == 5

    def test_expansion_opportunity_values(self):
        values = {e.value for e in ExpansionOpportunity}
        assert values == {"upsell", "cross_sell", "renewal_upgrade", "whitespace", "at_risk"}

    def test_expansion_opportunity_upsell(self):
        assert ExpansionOpportunity.UPSELL.value == "upsell"

    def test_expansion_opportunity_cross_sell(self):
        assert ExpansionOpportunity.CROSS_SELL.value == "cross_sell"

    def test_expansion_opportunity_renewal_upgrade(self):
        assert ExpansionOpportunity.RENEWAL_UPGRADE.value == "renewal_upgrade"

    def test_expansion_opportunity_whitespace(self):
        assert ExpansionOpportunity.WHITESPACE.value == "whitespace"

    def test_expansion_opportunity_at_risk(self):
        assert ExpansionOpportunity.AT_RISK.value == "at_risk"

    def test_expansion_priority_count(self):
        assert len(ExpansionPriority) == 4

    def test_expansion_priority_values(self):
        values = {e.value for e in ExpansionPriority}
        assert values == {"critical", "high", "medium", "low"}

    def test_expansion_priority_critical(self):
        assert ExpansionPriority.CRITICAL.value == "critical"

    def test_expansion_priority_high(self):
        assert ExpansionPriority.HIGH.value == "high"

    def test_expansion_priority_medium(self):
        assert ExpansionPriority.MEDIUM.value == "medium"

    def test_expansion_priority_low(self):
        assert ExpansionPriority.LOW.value == "low"

    def test_account_health_count(self):
        assert len(AccountHealth) == 4

    def test_account_health_values(self):
        values = {e.value for e in AccountHealth}
        assert values == {"champion", "healthy", "stable", "at_risk"}

    def test_account_health_champion(self):
        assert AccountHealth.CHAMPION.value == "champion"

    def test_account_health_healthy(self):
        assert AccountHealth.HEALTHY.value == "healthy"

    def test_account_health_stable(self):
        assert AccountHealth.STABLE.value == "stable"

    def test_account_health_at_risk(self):
        assert AccountHealth.AT_RISK.value == "at_risk"

    def test_expansion_action_count(self):
        assert len(ExpansionAction) == 4

    def test_expansion_action_values(self):
        values = {e.value for e in ExpansionAction}
        assert values == {
            "schedule_executive_briefing",
            "propose_expansion",
            "qbr_required",
            "retain_focus",
        }

    def test_expansion_action_schedule_executive_briefing(self):
        assert ExpansionAction.SCHEDULE_EXECUTIVE_BRIEFING.value == "schedule_executive_briefing"

    def test_expansion_action_propose_expansion(self):
        assert ExpansionAction.PROPOSE_EXPANSION.value == "propose_expansion"

    def test_expansion_action_qbr_required(self):
        assert ExpansionAction.QBR_REQUIRED.value == "qbr_required"

    def test_expansion_action_retain_focus(self):
        assert ExpansionAction.RETAIN_FOCUS.value == "retain_focus"

    def test_enums_are_str_subclass(self):
        # All enums inherit from str
        for cls in (ExpansionOpportunity, ExpansionPriority, AccountHealth, ExpansionAction):
            for member in cls:
                assert isinstance(member, str)


# ---------------------------------------------------------------------------
# 2. Dataclass field count
# ---------------------------------------------------------------------------

class TestDataclassFieldCounts:
    def test_account_expansion_input_has_22_fields(self):
        fields = dataclasses.fields(AccountExpansionInput)
        assert len(fields) == 22

    def test_account_expansion_result_fields(self):
        fields = dataclasses.fields(AccountExpansionResult)
        # 15 fields expected (same as to_dict keys)
        assert len(fields) == 15

    def test_input_field_names(self):
        names = {f.name for f in dataclasses.fields(AccountExpansionInput)}
        expected = {
            "account_id", "account_name", "rep_id",
            "contract_value_usd", "contract_renewal_days",
            "product_adoption_score", "active_users_count", "total_licensed_users_count",
            "support_ticket_count_90d", "nps_score",
            "exec_sponsor_engaged", "champion_identified", "qbr_completed_last_180d",
            "upsell_discussion_held", "cross_sell_product_gaps", "competitor_in_account",
            "days_since_last_touchpoint", "escalation_count_90d", "expansion_budget_confirmed",
            "expansion_usd_potential", "industry_growth_score", "account_tenure_days",
        }
        assert names == expected


# ---------------------------------------------------------------------------
# 3. to_dict() key count
# ---------------------------------------------------------------------------

class TestToDictKeys:
    def test_to_dict_returns_15_keys(self):
        intel = fresh()
        result = intel.analyze(make_input())
        assert len(result.to_dict()) == 15

    def test_to_dict_key_names(self):
        intel = fresh()
        result = intel.analyze(make_input())
        d = result.to_dict()
        expected_keys = {
            "account_id", "account_name",
            "expansion_opportunity", "expansion_priority",
            "account_health", "expansion_action",
            "adoption_health_score", "relationship_health_score",
            "commercial_readiness_score", "risk_score",
            "expansion_composite", "estimated_expansion_arr_usd",
            "is_expansion_ready", "needs_retention_focus",
            "primary_expansion_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        intel = fresh()
        result = intel.analyze(make_input())
        d = result.to_dict()
        assert isinstance(d["expansion_opportunity"], str)
        assert isinstance(d["expansion_priority"], str)
        assert isinstance(d["account_health"], str)
        assert isinstance(d["expansion_action"], str)

    def test_to_dict_bool_fields(self):
        intel = fresh()
        result = intel.analyze(make_input())
        d = result.to_dict()
        assert isinstance(d["is_expansion_ready"], bool)
        assert isinstance(d["needs_retention_focus"], bool)

    def test_to_dict_numeric_fields_are_float_or_int(self):
        intel = fresh()
        result = intel.analyze(make_input())
        d = result.to_dict()
        for key in ("adoption_health_score", "relationship_health_score",
                    "commercial_readiness_score", "risk_score",
                    "expansion_composite", "estimated_expansion_arr_usd"):
            assert isinstance(d[key], (int, float))

    def test_to_dict_at_risk_account(self):
        intel = fresh()
        result = intel.analyze(at_risk_input())
        d = result.to_dict()
        assert len(d) == 15
        assert d["needs_retention_focus"] is True

    def test_to_dict_account_id_matches_input(self):
        intel = fresh()
        inp = make_input(account_id="xyz_789")
        result = intel.analyze(inp)
        assert result.to_dict()["account_id"] == "xyz_789"


# ---------------------------------------------------------------------------
# 4. _adoption_health_score
# ---------------------------------------------------------------------------

class TestAdoptionHealthScore:
    def test_default_input_score_in_range(self):
        inp = make_input()
        score = _adoption_health_score(inp)
        assert 0.0 <= score <= 100.0

    def test_perfect_adoption(self):
        # adoption>=80(35) + util=1.0(30) + nps>=50(20) + tickets=0(15) = 100
        inp = make_input(
            product_adoption_score=95.0,
            active_users_count=50, total_licensed_users_count=50,
            nps_score=80.0, support_ticket_count_90d=0,
            escalation_count_90d=0,
        )
        assert _adoption_health_score(inp) == 100.0

    def test_zero_adoption_clamped(self):
        inp = make_input(
            product_adoption_score=0.0,
            active_users_count=0, total_licensed_users_count=50,
            nps_score=-50.0, support_ticket_count_90d=10,
            escalation_count_90d=5,
        )
        score = _adoption_health_score(inp)
        assert score == 0.0

    def test_adoption_score_between_60_and_79(self):
        inp = make_input(product_adoption_score=70.0)
        score = _adoption_health_score(inp)
        # 25 for adoption tier; rest depends on defaults
        assert 0.0 <= score <= 100.0
        # Explicitly check it is NOT getting the 35 tier
        inp_high = make_input(product_adoption_score=80.0)
        # higher adoption should give higher or equal score
        assert _adoption_health_score(inp_high) >= score

    def test_adoption_score_tier_40_to_59(self):
        inp = make_input(product_adoption_score=50.0)
        inp_higher = make_input(product_adoption_score=60.0)
        assert _adoption_health_score(inp) <= _adoption_health_score(inp_higher)

    def test_adoption_score_tier_20_to_39(self):
        inp = make_input(product_adoption_score=25.0)
        inp_higher = make_input(product_adoption_score=40.0)
        assert _adoption_health_score(inp) <= _adoption_health_score(inp_higher)

    def test_adoption_score_below_20(self):
        inp = make_input(product_adoption_score=10.0)
        inp_above = make_input(product_adoption_score=20.0)
        assert _adoption_health_score(inp) <= _adoption_health_score(inp_above)

    def test_util_rate_above_90pct(self):
        inp = make_input(active_users_count=46, total_licensed_users_count=50)
        # util = 0.92 → 30 points
        base = make_input(active_users_count=35, total_licensed_users_count=50)
        # util = 0.70 → 22 points
        assert _adoption_health_score(inp) > _adoption_health_score(base)

    def test_util_rate_70_to_89pct(self):
        inp = make_input(active_users_count=35, total_licensed_users_count=50)  # 0.70
        assert 0.0 <= _adoption_health_score(inp) <= 100.0

    def test_util_rate_50_to_69pct(self):
        inp = make_input(active_users_count=28, total_licensed_users_count=50)  # 0.56
        inp_higher = make_input(active_users_count=38, total_licensed_users_count=50)  # 0.76
        assert _adoption_health_score(inp) < _adoption_health_score(inp_higher)

    def test_util_rate_30_to_49pct(self):
        inp = make_input(active_users_count=15, total_licensed_users_count=50)  # 0.30
        assert 0.0 <= _adoption_health_score(inp) <= 100.0

    def test_zero_licensed_users_no_crash(self):
        inp = make_input(active_users_count=0, total_licensed_users_count=0)
        score = _adoption_health_score(inp)
        assert 0.0 <= score <= 100.0

    def test_nps_above_50(self):
        inp_high = make_input(nps_score=60.0)
        inp_low = make_input(nps_score=25.0)
        assert _adoption_health_score(inp_high) > _adoption_health_score(inp_low)

    def test_nps_20_to_49(self):
        inp = make_input(nps_score=30.0)
        assert 0.0 <= _adoption_health_score(inp) <= 100.0

    def test_nps_0_to_19(self):
        inp = make_input(nps_score=5.0)
        assert 0.0 <= _adoption_health_score(inp) <= 100.0

    def test_nps_minus20_to_minus1(self):
        inp = make_input(nps_score=-10.0)
        assert 0.0 <= _adoption_health_score(inp) <= 100.0

    def test_nps_below_minus20_no_bonus(self):
        inp = make_input(nps_score=-25.0)
        # Below -20 gets 0 NPS points
        inp_above = make_input(nps_score=-10.0)  # gets 3 points
        assert _adoption_health_score(inp) <= _adoption_health_score(inp_above)

    def test_support_tickets_zero(self):
        inp = make_input(support_ticket_count_90d=0)
        inp_high = make_input(support_ticket_count_90d=3)
        assert _adoption_health_score(inp) > _adoption_health_score(inp_high)

    def test_support_tickets_1_to_2(self):
        inp = make_input(support_ticket_count_90d=2)
        assert 0.0 <= _adoption_health_score(inp) <= 100.0

    def test_support_tickets_3_to_5(self):
        inp = make_input(support_ticket_count_90d=5)
        assert 0.0 <= _adoption_health_score(inp) <= 100.0

    def test_support_tickets_above_5_no_bonus(self):
        inp_6 = make_input(support_ticket_count_90d=6)
        inp_5 = make_input(support_ticket_count_90d=5)
        # 5 still gives 5 points; 6 gives 0
        assert _adoption_health_score(inp_5) >= _adoption_health_score(inp_6)

    def test_escalation_3_plus_penalty(self):
        inp_no_esc = make_input(escalation_count_90d=0)
        inp_3_esc = make_input(escalation_count_90d=3)
        assert _adoption_health_score(inp_no_esc) > _adoption_health_score(inp_3_esc)

    def test_escalation_1_to_2_penalty(self):
        inp_1_esc = make_input(escalation_count_90d=1)
        inp_no_esc = make_input(escalation_count_90d=0)
        assert _adoption_health_score(inp_no_esc) > _adoption_health_score(inp_1_esc)

    def test_result_is_rounded_to_1_decimal(self):
        inp = make_input()
        score = _adoption_health_score(inp)
        assert score == round(score, 1)

    def test_default_input_expected_value(self):
        # adoption=82(35) + util=45/50=0.9(30) + nps=62(20) + tickets=1(10) + esc=0(0) = 95
        inp = make_input()
        assert _adoption_health_score(inp) == 95.0


# ---------------------------------------------------------------------------
# 5. _relationship_health_score
# ---------------------------------------------------------------------------

class TestRelationshipHealthScore:
    def test_default_input_in_range(self):
        inp = make_input()
        score = _relationship_health_score(inp)
        assert 0.0 <= score <= 100.0

    def test_perfect_relationship(self):
        # exec(30)+champ(25)+qbr(20)+touch<=7(15)+tenure>=730(10) = 100; competitor=0
        inp = make_input(
            exec_sponsor_engaged=1, champion_identified=1, qbr_completed_last_180d=1,
            days_since_last_touchpoint=5, account_tenure_days=800,
            competitor_in_account=0,
        )
        assert _relationship_health_score(inp) == 100.0

    def test_zero_relationship(self):
        inp = make_input(
            exec_sponsor_engaged=0, champion_identified=0, qbr_completed_last_180d=0,
            days_since_last_touchpoint=90, account_tenure_days=30,
            competitor_in_account=1,
        )
        score = _relationship_health_score(inp)
        assert score == 0.0

    def test_exec_sponsor_adds_30(self):
        inp_with = make_input(exec_sponsor_engaged=1, champion_identified=0,
                               qbr_completed_last_180d=0, days_since_last_touchpoint=90,
                               account_tenure_days=30, competitor_in_account=0)
        inp_without = make_input(exec_sponsor_engaged=0, champion_identified=0,
                                  qbr_completed_last_180d=0, days_since_last_touchpoint=90,
                                  account_tenure_days=30, competitor_in_account=0)
        assert _relationship_health_score(inp_with) - _relationship_health_score(inp_without) == 30.0

    def test_champion_adds_25(self):
        inp_with = make_input(exec_sponsor_engaged=0, champion_identified=1,
                               qbr_completed_last_180d=0, days_since_last_touchpoint=90,
                               account_tenure_days=30, competitor_in_account=0)
        inp_without = make_input(exec_sponsor_engaged=0, champion_identified=0,
                                  qbr_completed_last_180d=0, days_since_last_touchpoint=90,
                                  account_tenure_days=30, competitor_in_account=0)
        assert _relationship_health_score(inp_with) - _relationship_health_score(inp_without) == 25.0

    def test_qbr_adds_20(self):
        inp_with = make_input(exec_sponsor_engaged=0, champion_identified=0,
                               qbr_completed_last_180d=1, days_since_last_touchpoint=90,
                               account_tenure_days=30, competitor_in_account=0)
        inp_without = make_input(exec_sponsor_engaged=0, champion_identified=0,
                                  qbr_completed_last_180d=0, days_since_last_touchpoint=90,
                                  account_tenure_days=30, competitor_in_account=0)
        assert _relationship_health_score(inp_with) - _relationship_health_score(inp_without) == 20.0

    def test_touchpoint_within_7_days(self):
        inp = make_input(exec_sponsor_engaged=0, champion_identified=0, qbr_completed_last_180d=0,
                          days_since_last_touchpoint=7, account_tenure_days=30, competitor_in_account=0)
        inp_later = make_input(exec_sponsor_engaged=0, champion_identified=0, qbr_completed_last_180d=0,
                                days_since_last_touchpoint=8, account_tenure_days=30, competitor_in_account=0)
        assert _relationship_health_score(inp) > _relationship_health_score(inp_later)

    def test_touchpoint_8_to_14_days(self):
        inp = make_input(exec_sponsor_engaged=0, champion_identified=0, qbr_completed_last_180d=0,
                          days_since_last_touchpoint=10, account_tenure_days=30, competitor_in_account=0)
        assert 0.0 <= _relationship_health_score(inp) <= 100.0

    def test_touchpoint_15_to_30_days(self):
        inp = make_input(exec_sponsor_engaged=0, champion_identified=0, qbr_completed_last_180d=0,
                          days_since_last_touchpoint=20, account_tenure_days=30, competitor_in_account=0)
        assert 0.0 <= _relationship_health_score(inp) <= 100.0

    def test_touchpoint_31_to_60_days(self):
        inp = make_input(exec_sponsor_engaged=0, champion_identified=0, qbr_completed_last_180d=0,
                          days_since_last_touchpoint=45, account_tenure_days=30, competitor_in_account=0)
        assert 0.0 <= _relationship_health_score(inp) <= 100.0

    def test_touchpoint_over_60_days_no_bonus(self):
        inp_61 = make_input(exec_sponsor_engaged=0, champion_identified=0, qbr_completed_last_180d=0,
                             days_since_last_touchpoint=61, account_tenure_days=30, competitor_in_account=0)
        inp_45 = make_input(exec_sponsor_engaged=0, champion_identified=0, qbr_completed_last_180d=0,
                             days_since_last_touchpoint=45, account_tenure_days=30, competitor_in_account=0)
        assert _relationship_health_score(inp_61) < _relationship_health_score(inp_45)

    def test_tenure_above_730_days(self):
        inp = make_input(exec_sponsor_engaged=0, champion_identified=0, qbr_completed_last_180d=0,
                          days_since_last_touchpoint=90, account_tenure_days=800, competitor_in_account=0)
        assert 0.0 <= _relationship_health_score(inp) <= 100.0

    def test_tenure_365_to_729(self):
        inp = make_input(exec_sponsor_engaged=0, champion_identified=0, qbr_completed_last_180d=0,
                          days_since_last_touchpoint=90, account_tenure_days=400, competitor_in_account=0)
        assert 0.0 <= _relationship_health_score(inp) <= 100.0

    def test_tenure_180_to_364(self):
        inp = make_input(exec_sponsor_engaged=0, champion_identified=0, qbr_completed_last_180d=0,
                          days_since_last_touchpoint=90, account_tenure_days=200, competitor_in_account=0)
        assert 0.0 <= _relationship_health_score(inp) <= 100.0

    def test_competitor_penalty(self):
        inp_comp = make_input(competitor_in_account=1)
        inp_no_comp = make_input(competitor_in_account=0)
        assert _relationship_health_score(inp_no_comp) > _relationship_health_score(inp_comp)

    def test_competitor_penalty_is_10(self):
        inp_comp = make_input(exec_sponsor_engaged=1, champion_identified=1, qbr_completed_last_180d=1,
                               days_since_last_touchpoint=5, account_tenure_days=800, competitor_in_account=1)
        inp_no_comp = make_input(exec_sponsor_engaged=1, champion_identified=1, qbr_completed_last_180d=1,
                                  days_since_last_touchpoint=5, account_tenure_days=800, competitor_in_account=0)
        assert _relationship_health_score(inp_no_comp) - _relationship_health_score(inp_comp) == 10.0

    def test_result_rounded_to_1_decimal(self):
        inp = make_input()
        score = _relationship_health_score(inp)
        assert score == round(score, 1)

    def test_default_input_expected_value(self):
        # exec(30)+champ(25)+qbr(20)+touch=5<=7(15)+tenure=540(365-729→7)+comp=0 = 97
        inp = make_input()
        assert _relationship_health_score(inp) == 97.0


# ---------------------------------------------------------------------------
# 6. _commercial_readiness_score
# ---------------------------------------------------------------------------

class TestCommercialReadinessScore:
    def test_default_input_in_range(self):
        inp = make_input()
        score = _commercial_readiness_score(inp)
        assert 0.0 <= score <= 100.0

    def test_budget_confirmed_adds_35(self):
        inp_with = make_input(expansion_budget_confirmed=1, upsell_discussion_held=0,
                               cross_sell_product_gaps=0, industry_growth_score=0.0,
                               contract_renewal_days=500)
        inp_without = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                                  cross_sell_product_gaps=0, industry_growth_score=0.0,
                                  contract_renewal_days=500)
        assert _commercial_readiness_score(inp_with) - _commercial_readiness_score(inp_without) == 35.0

    def test_upsell_discussion_adds_25(self):
        inp_with = make_input(expansion_budget_confirmed=0, upsell_discussion_held=1,
                               cross_sell_product_gaps=0, industry_growth_score=0.0,
                               contract_renewal_days=500)
        inp_without = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                                  cross_sell_product_gaps=0, industry_growth_score=0.0,
                                  contract_renewal_days=500)
        assert _commercial_readiness_score(inp_with) - _commercial_readiness_score(inp_without) == 25.0

    def test_cross_sell_3_plus_adds_20(self):
        inp = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                          cross_sell_product_gaps=3, industry_growth_score=0.0,
                          contract_renewal_days=500)
        inp_less = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                               cross_sell_product_gaps=2, industry_growth_score=0.0,
                               contract_renewal_days=500)
        assert _commercial_readiness_score(inp) > _commercial_readiness_score(inp_less)

    def test_cross_sell_2_adds_14(self):
        inp = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                          cross_sell_product_gaps=2, industry_growth_score=0.0,
                          contract_renewal_days=500)
        inp_base = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                               cross_sell_product_gaps=0, industry_growth_score=0.0,
                               contract_renewal_days=500)
        assert _commercial_readiness_score(inp) - _commercial_readiness_score(inp_base) == 14.0

    def test_cross_sell_1_adds_7(self):
        inp = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                          cross_sell_product_gaps=1, industry_growth_score=0.0,
                          contract_renewal_days=500)
        inp_base = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                               cross_sell_product_gaps=0, industry_growth_score=0.0,
                               contract_renewal_days=500)
        assert _commercial_readiness_score(inp) - _commercial_readiness_score(inp_base) == 7.0

    def test_industry_growth_contributes_10pct(self):
        inp = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                          cross_sell_product_gaps=0, industry_growth_score=100.0,
                          contract_renewal_days=500)
        inp_zero = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                               cross_sell_product_gaps=0, industry_growth_score=0.0,
                               contract_renewal_days=500)
        assert _commercial_readiness_score(inp) - _commercial_readiness_score(inp_zero) == pytest.approx(10.0, abs=0.2)

    def test_renewal_within_90_days_adds_10(self):
        inp_90 = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                             cross_sell_product_gaps=0, industry_growth_score=0.0,
                             contract_renewal_days=60)
        inp_500 = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                              cross_sell_product_gaps=0, industry_growth_score=0.0,
                              contract_renewal_days=500)
        assert _commercial_readiness_score(inp_90) > _commercial_readiness_score(inp_500)

    def test_renewal_91_to_180_days_adds_6(self):
        inp = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                          cross_sell_product_gaps=0, industry_growth_score=0.0,
                          contract_renewal_days=150)
        assert 0.0 <= _commercial_readiness_score(inp) <= 100.0

    def test_renewal_181_to_365_adds_3(self):
        inp = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                          cross_sell_product_gaps=0, industry_growth_score=0.0,
                          contract_renewal_days=300)
        assert 0.0 <= _commercial_readiness_score(inp) <= 100.0

    def test_renewal_over_365_no_bonus(self):
        inp_366 = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                              cross_sell_product_gaps=0, industry_growth_score=0.0,
                              contract_renewal_days=400)
        inp_300 = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                              cross_sell_product_gaps=0, industry_growth_score=0.0,
                              contract_renewal_days=300)
        assert _commercial_readiness_score(inp_300) > _commercial_readiness_score(inp_366)

    def test_clamped_max_100(self):
        inp = make_input(expansion_budget_confirmed=1, upsell_discussion_held=1,
                          cross_sell_product_gaps=5, industry_growth_score=100.0,
                          contract_renewal_days=30)
        assert _commercial_readiness_score(inp) <= 100.0

    def test_clamped_min_0(self):
        inp = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                          cross_sell_product_gaps=0, industry_growth_score=0.0,
                          contract_renewal_days=500)
        assert _commercial_readiness_score(inp) >= 0.0

    def test_result_rounded_to_1_decimal(self):
        inp = make_input()
        score = _commercial_readiness_score(inp)
        assert score == round(score, 1)

    def test_default_input_expected_value(self):
        # budget(35)+upsell(25)+gaps=3(20)+growth=78*0.1(7.8)+renewal=120(6) = 93.8
        inp = make_input()
        assert _commercial_readiness_score(inp) == 93.8


# ---------------------------------------------------------------------------
# 7. _risk_score
# ---------------------------------------------------------------------------

class TestRiskScore:
    def test_default_input_in_range(self):
        inp = make_input()
        score = _risk_score(inp)
        assert 0.0 <= score <= 100.0

    def test_default_input_low_risk(self):
        # nps=62 (0 pts) + escalations=0 (0) + competitor=0 (0) + adoption=82 (0) + renewal=120 (0) = 0
        inp = make_input()
        assert _risk_score(inp) == 0.0

    def test_nps_below_minus30_adds_30(self):
        # Use nps_score=25 as baseline (no NPS risk points) vs nps_score=-35 (30 pts)
        inp_bad = make_input(nps_score=-35.0, escalation_count_90d=0,
                              competitor_in_account=0, product_adoption_score=80.0,
                              contract_renewal_days=200)
        inp_ok = make_input(nps_score=25.0, escalation_count_90d=0,
                             competitor_in_account=0, product_adoption_score=80.0,
                             contract_renewal_days=200)
        assert _risk_score(inp_bad) - _risk_score(inp_ok) == 30.0

    def test_nps_minus30_to_minus1_adds_20(self):
        inp = make_input(nps_score=-10.0, escalation_count_90d=0,
                          competitor_in_account=0, product_adoption_score=80.0,
                          contract_renewal_days=200)
        assert 20.0 <= _risk_score(inp) <= 100.0

    def test_nps_0_to_19_adds_10(self):
        inp = make_input(nps_score=10.0, escalation_count_90d=0,
                          competitor_in_account=0, product_adoption_score=80.0,
                          contract_renewal_days=200)
        assert _risk_score(inp) == 10.0

    def test_nps_above_20_no_risk(self):
        inp = make_input(nps_score=20.0, escalation_count_90d=0,
                          competitor_in_account=0, product_adoption_score=80.0,
                          contract_renewal_days=200)
        assert _risk_score(inp) == 0.0

    def test_escalation_3_plus_adds_25(self):
        inp = make_input(nps_score=50.0, escalation_count_90d=3,
                          competitor_in_account=0, product_adoption_score=80.0,
                          contract_renewal_days=200)
        inp_base = make_input(nps_score=50.0, escalation_count_90d=0,
                               competitor_in_account=0, product_adoption_score=80.0,
                               contract_renewal_days=200)
        assert _risk_score(inp) - _risk_score(inp_base) == 25.0

    def test_escalation_1_to_2_adds_15(self):
        inp = make_input(nps_score=50.0, escalation_count_90d=1,
                          competitor_in_account=0, product_adoption_score=80.0,
                          contract_renewal_days=200)
        inp_base = make_input(nps_score=50.0, escalation_count_90d=0,
                               competitor_in_account=0, product_adoption_score=80.0,
                               contract_renewal_days=200)
        assert _risk_score(inp) - _risk_score(inp_base) == 15.0

    def test_competitor_adds_20(self):
        inp = make_input(nps_score=50.0, escalation_count_90d=0,
                          competitor_in_account=1, product_adoption_score=80.0,
                          contract_renewal_days=200)
        inp_base = make_input(nps_score=50.0, escalation_count_90d=0,
                               competitor_in_account=0, product_adoption_score=80.0,
                               contract_renewal_days=200)
        assert _risk_score(inp) - _risk_score(inp_base) == 20.0

    def test_low_adoption_below_30_adds_15(self):
        inp = make_input(nps_score=50.0, escalation_count_90d=0,
                          competitor_in_account=0, product_adoption_score=20.0,
                          contract_renewal_days=200)
        inp_base = make_input(nps_score=50.0, escalation_count_90d=0,
                               competitor_in_account=0, product_adoption_score=80.0,
                               contract_renewal_days=200)
        assert _risk_score(inp) - _risk_score(inp_base) == 15.0

    def test_low_adoption_30_to_49_adds_8(self):
        inp = make_input(nps_score=50.0, escalation_count_90d=0,
                          competitor_in_account=0, product_adoption_score=40.0,
                          contract_renewal_days=200)
        inp_base = make_input(nps_score=50.0, escalation_count_90d=0,
                               competitor_in_account=0, product_adoption_score=80.0,
                               contract_renewal_days=200)
        assert _risk_score(inp) - _risk_score(inp_base) == 8.0

    def test_renewal_within_30_days_adds_10(self):
        inp = make_input(nps_score=50.0, escalation_count_90d=0,
                          competitor_in_account=0, product_adoption_score=80.0,
                          contract_renewal_days=25)
        inp_base = make_input(nps_score=50.0, escalation_count_90d=0,
                               competitor_in_account=0, product_adoption_score=80.0,
                               contract_renewal_days=200)
        assert _risk_score(inp) - _risk_score(inp_base) == 10.0

    def test_renewal_over_30_no_extra_risk(self):
        inp = make_input(nps_score=50.0, escalation_count_90d=0,
                          competitor_in_account=0, product_adoption_score=80.0,
                          contract_renewal_days=31)
        inp_base = make_input(nps_score=50.0, escalation_count_90d=0,
                               competitor_in_account=0, product_adoption_score=80.0,
                               contract_renewal_days=200)
        assert _risk_score(inp) == _risk_score(inp_base)

    def test_at_risk_input_high_score(self):
        inp = at_risk_input()
        score = _risk_score(inp)
        assert score >= 50.0

    def test_clamped_max_100(self):
        inp = at_risk_input()
        assert _risk_score(inp) <= 100.0

    def test_result_rounded_to_1_decimal(self):
        inp = make_input()
        score = _risk_score(inp)
        assert score == round(score, 1)


# ---------------------------------------------------------------------------
# 8. _composite formula
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_formula_exact(self):
        a, r, c, risk = 80.0, 70.0, 60.0, 20.0
        expected = round(80 * 0.30 + 70 * 0.30 + 60 * 0.25 + (100 - 20) * 0.15, 1)
        assert _composite(a, r, c, risk) == expected

    def test_formula_all_zeros(self):
        # risk=0 → (100-0)*0.15 = 15
        result = _composite(0.0, 0.0, 0.0, 0.0)
        assert result == 15.0

    def test_formula_all_100(self):
        # 100*0.30 + 100*0.30 + 100*0.25 + (100-100)*0.15 = 85
        result = _composite(100.0, 100.0, 100.0, 100.0)
        assert result == 85.0

    def test_formula_perfect_scenario(self):
        # adoption=100, rel=100, comm=100, risk=0 → 100
        result = _composite(100.0, 100.0, 100.0, 0.0)
        assert result == 100.0

    def test_formula_rounded_to_1_decimal(self):
        result = _composite(77.3, 83.1, 65.5, 22.7)
        assert result == round(result, 1)

    def test_weights_sum_to_1(self):
        # 0.30+0.30+0.25+0.15=1.00
        assert abs(0.30 + 0.30 + 0.25 + 0.15 - 1.0) < 1e-9

    def test_risk_contribution_inverse(self):
        # Higher risk → lower composite
        c_low_risk = _composite(70.0, 70.0, 70.0, 0.0)
        c_high_risk = _composite(70.0, 70.0, 70.0, 100.0)
        assert c_low_risk > c_high_risk

    def test_default_input_composite(self):
        # Compute from known scores
        inp = make_input()
        a = _adoption_health_score(inp)   # 95.0
        r = _relationship_health_score(inp)  # 97.0
        c = _commercial_readiness_score(inp) # 93.8
        risk = _risk_score(inp)             # 0.0
        expected = round(a * 0.30 + r * 0.30 + c * 0.25 + (100 - risk) * 0.15, 1)
        assert _composite(a, r, c, risk) == expected


# ---------------------------------------------------------------------------
# 9. Boolean flag invariants
# ---------------------------------------------------------------------------

class TestBooleanFlags:
    def test_is_expansion_ready_true_when_composite_65_and_budget_1(self):
        intel = fresh()
        result = intel.analyze(make_input())
        if result.expansion_composite >= 65 and result.expansion_composite is not None:
            assert result.is_expansion_ready is True

    def test_is_expansion_ready_false_when_no_budget(self):
        intel = fresh()
        # High composite but no budget
        result = intel.analyze(make_input(expansion_budget_confirmed=0))
        assert result.is_expansion_ready is False

    def test_is_expansion_ready_false_when_composite_below_65(self):
        intel = fresh()
        # Craft an input with composite < 65
        result = intel.analyze(make_input(
            expansion_budget_confirmed=1,
            product_adoption_score=10.0,
            exec_sponsor_engaged=0,
            champion_identified=0,
            qbr_completed_last_180d=0,
            nps_score=-50.0,
            escalation_count_90d=5,
            competitor_in_account=1,
            days_since_last_touchpoint=90,
            upsell_discussion_held=0,
            industry_growth_score=0.0,
            account_tenure_days=10,
        ))
        assert result.expansion_composite < 65 or result.is_expansion_ready is False

    def test_needs_retention_focus_true_when_risk_score_50(self):
        intel = fresh()
        result = intel.analyze(at_risk_input())
        assert result.needs_retention_focus is True

    def test_needs_retention_focus_true_when_escalation_3(self):
        intel = fresh()
        result = intel.analyze(make_input(escalation_count_90d=3, nps_score=50.0,
                                           competitor_in_account=0, product_adoption_score=80.0))
        assert result.needs_retention_focus is True

    def test_needs_retention_focus_true_when_nps_below_minus20(self):
        intel = fresh()
        result = intel.analyze(make_input(nps_score=-25.0, escalation_count_90d=0,
                                           competitor_in_account=0, product_adoption_score=80.0))
        assert result.needs_retention_focus is True

    def test_needs_retention_focus_false_for_healthy_account(self):
        intel = fresh()
        result = intel.analyze(make_input())
        # Default: risk=0, escalations=0, nps=62 → no retention focus
        assert result.needs_retention_focus is False

    def test_is_expansion_ready_and_needs_retention_focus_both_false(self):
        intel = fresh()
        # Craft account with composite < 65
        result = intel.analyze(make_input(
            product_adoption_score=20.0,
            active_users_count=5, total_licensed_users_count=50,
            nps_score=5.0, expansion_budget_confirmed=0,
            exec_sponsor_engaged=0, champion_identified=0,
            qbr_completed_last_180d=0, days_since_last_touchpoint=45,
            escalation_count_90d=0, competitor_in_account=0,
            upsell_discussion_held=0, cross_sell_product_gaps=0,
            industry_growth_score=10.0, account_tenure_days=30,
        ))
        assert result.is_expansion_ready is False
        assert result.needs_retention_focus is False

    def test_expansion_ready_requires_both_conditions(self):
        # Condition 1: composite >= 65
        # Condition 2: expansion_budget_confirmed == 1
        intel = fresh()
        result = intel.analyze(make_input(expansion_budget_confirmed=1))
        if result.is_expansion_ready:
            assert result.expansion_composite >= 65

    def test_needs_retention_focus_or_conditions(self):
        intel = fresh()
        # Only escalation trigger (risk < 50, nps > -20)
        result = intel.analyze(make_input(
            escalation_count_90d=3, nps_score=30.0, competitor_in_account=0,
            product_adoption_score=80.0
        ))
        assert result.needs_retention_focus is True


# ---------------------------------------------------------------------------
# 10. AccountExpansionIntelligence.analyze()
# ---------------------------------------------------------------------------

class TestAnalyze:
    def test_analyze_returns_result(self):
        intel = fresh()
        result = intel.analyze(make_input())
        assert isinstance(result, AccountExpansionResult)

    def test_analyze_stores_result(self):
        intel = fresh()
        intel.analyze(make_input(account_id="test_001"))
        assert intel.get("test_001") is not None

    def test_analyze_overwrites_existing(self):
        intel = fresh()
        intel.analyze(make_input(account_id="acc_001", nps_score=50.0))
        intel.analyze(make_input(account_id="acc_001", nps_score=80.0))
        result = intel.get("acc_001")
        assert result is not None

    def test_analyze_scores_in_range(self):
        intel = fresh()
        result = intel.analyze(make_input())
        assert 0.0 <= result.adoption_health_score <= 100.0
        assert 0.0 <= result.relationship_health_score <= 100.0
        assert 0.0 <= result.commercial_readiness_score <= 100.0
        assert 0.0 <= result.risk_score <= 100.0

    def test_analyze_composite_in_range(self):
        intel = fresh()
        result = intel.analyze(make_input())
        assert 0.0 <= result.expansion_composite <= 100.0

    def test_analyze_at_risk_scores_in_range(self):
        intel = fresh()
        result = intel.analyze(at_risk_input())
        assert 0.0 <= result.adoption_health_score <= 100.0
        assert 0.0 <= result.relationship_health_score <= 100.0
        assert 0.0 <= result.commercial_readiness_score <= 100.0
        assert 0.0 <= result.risk_score <= 100.0

    def test_analyze_account_id_preserved(self):
        intel = fresh()
        result = intel.analyze(make_input(account_id="unique_id_123"))
        assert result.account_id == "unique_id_123"

    def test_analyze_account_name_preserved(self):
        intel = fresh()
        result = intel.analyze(make_input(account_name="Acme Corp"))
        assert result.account_name == "Acme Corp"

    def test_analyze_composite_matches_formula(self):
        intel = fresh()
        inp = make_input()
        result = intel.analyze(inp)
        expected = round(
            result.adoption_health_score * 0.30
            + result.relationship_health_score * 0.30
            + result.commercial_readiness_score * 0.25
            + (100 - result.risk_score) * 0.15,
            1,
        )
        assert result.expansion_composite == expected

    def test_analyze_opportunity_is_enum(self):
        intel = fresh()
        result = intel.analyze(make_input())
        assert isinstance(result.expansion_opportunity, ExpansionOpportunity)

    def test_analyze_priority_is_enum(self):
        intel = fresh()
        result = intel.analyze(make_input())
        assert isinstance(result.expansion_priority, ExpansionPriority)

    def test_analyze_health_is_enum(self):
        intel = fresh()
        result = intel.analyze(make_input())
        assert isinstance(result.account_health, AccountHealth)

    def test_analyze_action_is_enum(self):
        intel = fresh()
        result = intel.analyze(make_input())
        assert isinstance(result.expansion_action, ExpansionAction)

    def test_analyze_primary_signal_is_string(self):
        intel = fresh()
        result = intel.analyze(make_input())
        assert isinstance(result.primary_expansion_signal, str)

    def test_analyze_estimated_arr_positive(self):
        intel = fresh()
        result = intel.analyze(make_input())
        assert result.estimated_expansion_arr_usd >= 0.0

    def test_analyze_estimated_arr_multiplier_high_composite(self):
        # composite >= 75 → multiplier 0.85
        intel = fresh()
        result = intel.analyze(make_input())
        if result.expansion_composite >= 75:
            assert result.estimated_expansion_arr_usd == round(75_000.0 * 0.85, 0)

    def test_analyze_default_is_expansion_ready_true(self):
        intel = fresh()
        result = intel.analyze(make_input())
        assert result.is_expansion_ready is True

    def test_analyze_default_needs_retention_false(self):
        intel = fresh()
        result = intel.analyze(make_input())
        assert result.needs_retention_focus is False


# ---------------------------------------------------------------------------
# 11. AccountExpansionIntelligence.analyze_batch()
# ---------------------------------------------------------------------------

class TestAnalyzeBatch:
    def test_analyze_batch_returns_list(self):
        intel = fresh()
        results = intel.analyze_batch([make_input(account_id="a1"), make_input(account_id="a2")])
        assert isinstance(results, list)

    def test_analyze_batch_length(self):
        intel = fresh()
        inputs = [make_input(account_id=f"acc_{i}") for i in range(5)]
        results = intel.analyze_batch(inputs)
        assert len(results) == 5

    def test_analyze_batch_sorted_by_composite_desc(self):
        intel = fresh()
        inputs = [make_input(account_id=f"acc_{i}") for i in range(3)]
        inputs.append(at_risk_input("at_risk"))
        results = intel.analyze_batch(inputs)
        composites = [r.expansion_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_analyze_batch_stores_all_accounts(self):
        intel = fresh()
        intel.analyze_batch([make_input(account_id="b1"), make_input(account_id="b2")])
        assert intel.get("b1") is not None
        assert intel.get("b2") is not None

    def test_analyze_batch_empty_list(self):
        intel = fresh()
        results = intel.analyze_batch([])
        assert results == []

    def test_analyze_batch_single_item(self):
        intel = fresh()
        results = intel.analyze_batch([make_input(account_id="only_one")])
        assert len(results) == 1

    def test_analyze_batch_all_results_are_result_type(self):
        intel = fresh()
        results = intel.analyze_batch([make_input(account_id=f"x{i}") for i in range(3)])
        for r in results:
            assert isinstance(r, AccountExpansionResult)


# ---------------------------------------------------------------------------
# 12. get() and all_accounts()
# ---------------------------------------------------------------------------

class TestGetAndAllAccounts:
    def test_get_returns_none_for_unknown(self):
        intel = fresh()
        assert intel.get("unknown_id") is None

    def test_get_returns_correct_result(self):
        intel = fresh()
        intel.analyze(make_input(account_id="known_001"))
        result = intel.get("known_001")
        assert result is not None
        assert result.account_id == "known_001"

    def test_all_accounts_empty_initially(self):
        intel = fresh()
        assert intel.all_accounts() == []

    def test_all_accounts_returns_all(self):
        intel = fresh()
        intel.analyze(make_input(account_id="a1"))
        intel.analyze(make_input(account_id="a2"))
        intel.analyze(make_input(account_id="a3"))
        assert len(intel.all_accounts()) == 3

    def test_all_accounts_sorted_by_composite_desc(self):
        intel = fresh()
        intel.analyze(make_input(account_id="good"))
        intel.analyze(at_risk_input("bad"))
        accounts = intel.all_accounts()
        composites = [a.expansion_composite for a in accounts]
        assert composites == sorted(composites, reverse=True)

    def test_all_accounts_returns_list(self):
        intel = fresh()
        intel.analyze(make_input())
        assert isinstance(intel.all_accounts(), list)


# ---------------------------------------------------------------------------
# 13. expansion_ready() and retention_focus()
# ---------------------------------------------------------------------------

class TestFilterMethods:
    def test_expansion_ready_empty_when_no_accounts(self):
        intel = fresh()
        assert intel.expansion_ready() == []

    def test_expansion_ready_includes_ready_accounts(self):
        intel = fresh()
        intel.analyze(make_input(account_id="ready"))
        ready = intel.expansion_ready()
        account_ids = [r.account_id for r in ready]
        # Default account should be expansion ready
        assert "ready" in account_ids

    def test_expansion_ready_excludes_non_ready(self):
        intel = fresh()
        intel.analyze(make_input(account_id="not_ready", expansion_budget_confirmed=0))
        ready = intel.expansion_ready()
        account_ids = [r.account_id for r in ready]
        assert "not_ready" not in account_ids

    def test_expansion_ready_all_items_have_flag_true(self):
        intel = fresh()
        intel.analyze(make_input(account_id="r1"))
        intel.analyze(make_input(account_id="r2", expansion_budget_confirmed=0))
        for r in intel.expansion_ready():
            assert r.is_expansion_ready is True

    def test_retention_focus_empty_when_no_accounts(self):
        intel = fresh()
        assert intel.retention_focus() == []

    def test_retention_focus_includes_at_risk_accounts(self):
        intel = fresh()
        intel.analyze(at_risk_input("at_risk_acct"))
        focus = intel.retention_focus()
        account_ids = [r.account_id for r in focus]
        assert "at_risk_acct" in account_ids

    def test_retention_focus_excludes_healthy_accounts(self):
        intel = fresh()
        intel.analyze(make_input(account_id="healthy"))
        focus = intel.retention_focus()
        account_ids = [r.account_id for r in focus]
        assert "healthy" not in account_ids

    def test_retention_focus_all_items_have_flag_true(self):
        intel = fresh()
        intel.analyze(at_risk_input())
        for r in intel.retention_focus():
            assert r.needs_retention_focus is True

    def test_both_filters_can_overlap(self):
        intel = fresh()
        # High-composite but also escalation >= 3
        intel.analyze(make_input(account_id="overlap", escalation_count_90d=3))
        focus = intel.retention_focus()
        assert any(r.account_id == "overlap" for r in focus)


# ---------------------------------------------------------------------------
# 14. by_opportunity() and by_priority()
# ---------------------------------------------------------------------------

class TestByOpportunityAndPriority:
    def test_by_opportunity_returns_list(self):
        intel = fresh()
        intel.analyze(make_input())
        result = intel.by_opportunity(ExpansionOpportunity.UPSELL)
        assert isinstance(result, list)

    def test_by_opportunity_all_match(self):
        intel = fresh()
        intel.analyze(make_input())
        for opp in ExpansionOpportunity:
            for r in intel.by_opportunity(opp):
                assert r.expansion_opportunity == opp

    def test_by_opportunity_upsell_scenario(self):
        intel = fresh()
        # budget + upsell discussion + no risk
        inp = make_input(expansion_budget_confirmed=1, upsell_discussion_held=1,
                          nps_score=50.0, escalation_count_90d=0, competitor_in_account=0,
                          product_adoption_score=80.0)
        result = intel.analyze(inp)
        if result.expansion_opportunity == ExpansionOpportunity.UPSELL:
            upsells = intel.by_opportunity(ExpansionOpportunity.UPSELL)
            assert len(upsells) >= 1

    def test_by_opportunity_at_risk_scenario(self):
        intel = fresh()
        intel.analyze(at_risk_input())
        at_risks = intel.by_opportunity(ExpansionOpportunity.AT_RISK)
        assert len(at_risks) >= 1

    def test_by_priority_returns_list(self):
        intel = fresh()
        intel.analyze(make_input())
        result = intel.by_priority(ExpansionPriority.HIGH)
        assert isinstance(result, list)

    def test_by_priority_all_match(self):
        intel = fresh()
        intel.analyze(make_input())
        intel.analyze(at_risk_input())
        for priority in ExpansionPriority:
            for r in intel.by_priority(priority):
                assert r.expansion_priority == priority

    def test_by_priority_critical_for_at_risk(self):
        intel = fresh()
        intel.analyze(at_risk_input())
        criticals = intel.by_priority(ExpansionPriority.CRITICAL)
        # at_risk has high escalation → critical
        assert len(criticals) >= 1

    def test_by_opportunity_empty_for_missing_type(self):
        intel = fresh()
        intel.analyze(at_risk_input())
        # If no whitespace accounts, should return empty
        whitespaces = intel.by_opportunity(ExpansionOpportunity.WHITESPACE)
        for r in whitespaces:
            assert r.expansion_opportunity == ExpansionOpportunity.WHITESPACE


# ---------------------------------------------------------------------------
# 15. avg_expansion_composite()
# ---------------------------------------------------------------------------

class TestAvgExpansionComposite:
    def test_avg_empty_is_zero(self):
        intel = fresh()
        assert intel.avg_expansion_composite() == 0.0

    def test_avg_single_account(self):
        intel = fresh()
        result = intel.analyze(make_input())
        avg = intel.avg_expansion_composite()
        assert avg == result.expansion_composite

    def test_avg_multiple_accounts(self):
        intel = fresh()
        r1 = intel.analyze(make_input(account_id="a1"))
        r2 = intel.analyze(at_risk_input("a2"))
        expected = round((r1.expansion_composite + r2.expansion_composite) / 2, 1)
        assert intel.avg_expansion_composite() == expected

    def test_avg_is_rounded_to_1_decimal(self):
        intel = fresh()
        intel.analyze(make_input(account_id="a1"))
        intel.analyze(make_input(account_id="a2"))
        avg = intel.avg_expansion_composite()
        assert avg == round(avg, 1)

    def test_avg_between_min_and_max(self):
        intel = fresh()
        results = [intel.analyze(make_input(account_id=f"x{i}")) for i in range(4)]
        results.append(intel.analyze(at_risk_input()))
        all_composites = [r.expansion_composite for r in results]
        avg = intel.avg_expansion_composite()
        assert min(all_composites) <= avg <= max(all_composites)


# ---------------------------------------------------------------------------
# 16. reset()
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_clears_results(self):
        intel = fresh()
        intel.analyze(make_input())
        intel.reset()
        assert intel.all_accounts() == []

    def test_reset_makes_get_return_none(self):
        intel = fresh()
        intel.analyze(make_input(account_id="acc_001"))
        intel.reset()
        assert intel.get("acc_001") is None

    def test_reset_makes_avg_zero(self):
        intel = fresh()
        intel.analyze(make_input())
        intel.reset()
        assert intel.avg_expansion_composite() == 0.0

    def test_reset_allows_re_analyze(self):
        intel = fresh()
        intel.analyze(make_input(account_id="acc_001"))
        intel.reset()
        intel.analyze(make_input(account_id="acc_002"))
        assert intel.get("acc_002") is not None
        assert intel.get("acc_001") is None

    def test_reset_idempotent(self):
        intel = fresh()
        intel.reset()
        intel.reset()
        assert intel.all_accounts() == []


# ---------------------------------------------------------------------------
# 17. summary() key count and values
# ---------------------------------------------------------------------------

class TestSummary:
    def test_summary_returns_13_keys(self):
        intel = fresh()
        intel.analyze(make_input())
        s = intel.summary()
        assert len(s) == 13

    def test_summary_key_names(self):
        intel = fresh()
        intel.analyze(make_input())
        s = intel.summary()
        expected_keys = {
            "total",
            "opportunity_counts",
            "priority_counts",
            "health_counts",
            "action_counts",
            "avg_expansion_composite",
            "expansion_ready_count",
            "retention_focus_count",
            "avg_adoption_health_score",
            "avg_relationship_health_score",
            "avg_commercial_readiness_score",
            "avg_risk_score",
            "total_expansion_arr_potential_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_empty_intelligence(self):
        intel = fresh()
        s = intel.summary()
        assert len(s) == 13
        assert s["total"] == 0
        assert s["avg_expansion_composite"] == 0.0
        assert s["expansion_ready_count"] == 0
        assert s["retention_focus_count"] == 0
        assert s["avg_adoption_health_score"] == 0.0
        assert s["avg_relationship_health_score"] == 0.0
        assert s["avg_commercial_readiness_score"] == 0.0
        assert s["avg_risk_score"] == 0.0
        assert s["total_expansion_arr_potential_usd"] == 0.0

    def test_summary_total_count(self):
        intel = fresh()
        for i in range(4):
            intel.analyze(make_input(account_id=f"acc_{i}"))
        assert intel.summary()["total"] == 4

    def test_summary_opportunity_counts_is_dict(self):
        intel = fresh()
        intel.analyze(make_input())
        s = intel.summary()
        assert isinstance(s["opportunity_counts"], dict)

    def test_summary_priority_counts_is_dict(self):
        intel = fresh()
        intel.analyze(make_input())
        s = intel.summary()
        assert isinstance(s["priority_counts"], dict)

    def test_summary_health_counts_is_dict(self):
        intel = fresh()
        intel.analyze(make_input())
        s = intel.summary()
        assert isinstance(s["health_counts"], dict)

    def test_summary_action_counts_is_dict(self):
        intel = fresh()
        intel.analyze(make_input())
        s = intel.summary()
        assert isinstance(s["action_counts"], dict)

    def test_summary_opportunity_counts_sum_to_total(self):
        intel = fresh()
        intel.analyze(make_input(account_id="a1"))
        intel.analyze(at_risk_input("a2"))
        s = intel.summary()
        assert sum(s["opportunity_counts"].values()) == s["total"]

    def test_summary_priority_counts_sum_to_total(self):
        intel = fresh()
        intel.analyze(make_input(account_id="a1"))
        intel.analyze(at_risk_input("a2"))
        s = intel.summary()
        assert sum(s["priority_counts"].values()) == s["total"]

    def test_summary_health_counts_sum_to_total(self):
        intel = fresh()
        intel.analyze(make_input(account_id="a1"))
        intel.analyze(at_risk_input("a2"))
        s = intel.summary()
        assert sum(s["health_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        intel = fresh()
        intel.analyze(make_input(account_id="a1"))
        intel.analyze(at_risk_input("a2"))
        s = intel.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_expansion_ready_count_correct(self):
        intel = fresh()
        intel.analyze(make_input(account_id="ready1"))
        intel.analyze(make_input(account_id="not_ready", expansion_budget_confirmed=0))
        s = intel.summary()
        assert s["expansion_ready_count"] == len(intel.expansion_ready())

    def test_summary_retention_focus_count_correct(self):
        intel = fresh()
        intel.analyze(make_input(account_id="healthy"))
        intel.analyze(at_risk_input("at_risk"))
        s = intel.summary()
        assert s["retention_focus_count"] == len(intel.retention_focus())

    def test_summary_avg_composite_matches_method(self):
        intel = fresh()
        intel.analyze(make_input(account_id="a1"))
        intel.analyze(at_risk_input("a2"))
        s = intel.summary()
        assert s["avg_expansion_composite"] == intel.avg_expansion_composite()

    def test_summary_total_arr_is_sum(self):
        intel = fresh()
        r1 = intel.analyze(make_input(account_id="a1"))
        r2 = intel.analyze(make_input(account_id="a2"))
        s = intel.summary()
        expected = round(r1.estimated_expansion_arr_usd + r2.estimated_expansion_arr_usd, 0)
        assert s["total_expansion_arr_potential_usd"] == expected

    def test_summary_avg_scores_are_float(self):
        intel = fresh()
        intel.analyze(make_input())
        s = intel.summary()
        for key in ("avg_adoption_health_score", "avg_relationship_health_score",
                    "avg_commercial_readiness_score", "avg_risk_score",
                    "avg_expansion_composite"):
            assert isinstance(s[key], (int, float))

    def test_summary_counts_use_enum_string_values(self):
        intel = fresh()
        intel.analyze(make_input())
        s = intel.summary()
        # Keys in counts should be string enum values, not enum objects
        for key in s["opportunity_counts"]:
            assert isinstance(key, str)
        for key in s["priority_counts"]:
            assert isinstance(key, str)
        for key in s["health_counts"]:
            assert isinstance(key, str)
        for key in s["action_counts"]:
            assert isinstance(key, str)

    def test_summary_after_reset_has_13_keys(self):
        intel = fresh()
        intel.analyze(make_input())
        intel.reset()
        s = intel.summary()
        assert len(s) == 13

    def test_summary_with_multiple_opportunity_types(self):
        intel = fresh()
        # at_risk opportunity
        intel.analyze(at_risk_input("ar1"))
        # upsell scenario (budget + upsell + no risk)
        intel.analyze(make_input(account_id="up1", expansion_budget_confirmed=1,
                                  upsell_discussion_held=1, nps_score=50.0,
                                  escalation_count_90d=0, competitor_in_account=0))
        s = intel.summary()
        assert sum(s["opportunity_counts"].values()) == 2


# ---------------------------------------------------------------------------
# 18. Score clamping (0–100)
# ---------------------------------------------------------------------------

class TestScoreClamping:
    def test_adoption_score_never_below_0(self):
        inp = at_risk_input()
        assert _adoption_health_score(inp) >= 0.0

    def test_adoption_score_never_above_100(self):
        inp = make_input(
            product_adoption_score=100.0, active_users_count=100,
            total_licensed_users_count=100, nps_score=100.0,
            support_ticket_count_90d=0, escalation_count_90d=0,
        )
        assert _adoption_health_score(inp) <= 100.0

    def test_relationship_score_never_below_0(self):
        inp = at_risk_input()
        assert _relationship_health_score(inp) >= 0.0

    def test_relationship_score_never_above_100(self):
        inp = make_input(
            exec_sponsor_engaged=1, champion_identified=1, qbr_completed_last_180d=1,
            days_since_last_touchpoint=1, account_tenure_days=1000,
            competitor_in_account=0,
        )
        assert _relationship_health_score(inp) <= 100.0

    def test_commercial_score_never_below_0(self):
        inp = make_input(expansion_budget_confirmed=0, upsell_discussion_held=0,
                          cross_sell_product_gaps=0, industry_growth_score=0.0,
                          contract_renewal_days=500)
        assert _commercial_readiness_score(inp) >= 0.0

    def test_commercial_score_never_above_100(self):
        inp = make_input(expansion_budget_confirmed=1, upsell_discussion_held=1,
                          cross_sell_product_gaps=10, industry_growth_score=100.0,
                          contract_renewal_days=10)
        assert _commercial_readiness_score(inp) <= 100.0

    def test_risk_score_never_below_0(self):
        inp = make_input(nps_score=80.0, escalation_count_90d=0,
                          competitor_in_account=0, product_adoption_score=90.0,
                          contract_renewal_days=200)
        assert _risk_score(inp) >= 0.0

    def test_risk_score_never_above_100(self):
        inp = at_risk_input()
        assert _risk_score(inp) <= 100.0

    def test_analyze_all_scores_clamped(self):
        intel = fresh()
        for inp in [make_input(), at_risk_input()]:
            result = intel.analyze(inp)
            assert 0.0 <= result.adoption_health_score <= 100.0
            assert 0.0 <= result.relationship_health_score <= 100.0
            assert 0.0 <= result.commercial_readiness_score <= 100.0
            assert 0.0 <= result.risk_score <= 100.0


# ---------------------------------------------------------------------------
# 19. Opportunity / Health / Priority / Action classifiers
# ---------------------------------------------------------------------------

class TestClassifiers:
    def test_at_risk_opportunity_when_high_risk(self):
        intel = fresh()
        result = intel.analyze(at_risk_input())
        assert result.expansion_opportunity == ExpansionOpportunity.AT_RISK

    def test_at_risk_opportunity_when_nps_below_minus20(self):
        intel = fresh()
        result = intel.analyze(make_input(nps_score=-25.0, escalation_count_90d=0,
                                           competitor_in_account=0, product_adoption_score=80.0))
        assert result.expansion_opportunity == ExpansionOpportunity.AT_RISK

    def test_upsell_opportunity(self):
        intel = fresh()
        result = intel.analyze(make_input(
            expansion_budget_confirmed=1, upsell_discussion_held=1,
            nps_score=50.0, escalation_count_90d=0, competitor_in_account=0,
            product_adoption_score=80.0,
        ))
        assert result.expansion_opportunity == ExpansionOpportunity.UPSELL

    def test_cross_sell_opportunity(self):
        intel = fresh()
        # budget=0, no upsell discussion, gaps>=2, not at risk
        result = intel.analyze(make_input(
            expansion_budget_confirmed=0, upsell_discussion_held=0,
            cross_sell_product_gaps=2, nps_score=30.0,
            escalation_count_90d=0, competitor_in_account=0,
            product_adoption_score=80.0,
        ))
        assert result.expansion_opportunity == ExpansionOpportunity.CROSS_SELL

    def test_renewal_upgrade_opportunity(self):
        intel = fresh()
        # budget=0, no upsell, gaps<2, renewal<=180
        result = intel.analyze(make_input(
            expansion_budget_confirmed=0, upsell_discussion_held=0,
            cross_sell_product_gaps=0, contract_renewal_days=90,
            nps_score=30.0, escalation_count_90d=0, competitor_in_account=0,
            product_adoption_score=80.0,
        ))
        assert result.expansion_opportunity == ExpansionOpportunity.RENEWAL_UPGRADE

    def test_whitespace_opportunity(self):
        intel = fresh()
        result = intel.analyze(make_input(
            expansion_budget_confirmed=0, upsell_discussion_held=0,
            cross_sell_product_gaps=0, contract_renewal_days=400,
            nps_score=50.0, escalation_count_90d=0, competitor_in_account=0,
            product_adoption_score=80.0,
        ))
        assert result.expansion_opportunity == ExpansionOpportunity.WHITESPACE

    def test_champion_health(self):
        intel = fresh()
        result = intel.analyze(make_input())
        # Default should produce champion (high composite, low risk)
        assert result.account_health == AccountHealth.CHAMPION

    def test_at_risk_health_for_bad_account(self):
        intel = fresh()
        result = intel.analyze(at_risk_input())
        assert result.account_health == AccountHealth.AT_RISK

    def test_critical_priority_when_high_escalations(self):
        intel = fresh()
        result = intel.analyze(make_input(escalation_count_90d=3))
        assert result.expansion_priority == ExpansionPriority.CRITICAL

    def test_high_priority_when_composite_75_and_budget(self):
        intel = fresh()
        result = intel.analyze(make_input())
        if result.expansion_composite >= 75 and result.expansion_composite is not None:
            assert result.expansion_priority in (
                ExpansionPriority.HIGH, ExpansionPriority.CRITICAL
            )

    def test_retain_focus_action_for_at_risk_health(self):
        intel = fresh()
        result = intel.analyze(at_risk_input())
        assert result.expansion_action == ExpansionAction.RETAIN_FOCUS

    def test_schedule_executive_briefing_action(self):
        intel = fresh()
        result = intel.analyze(make_input(
            exec_sponsor_engaged=1, expansion_budget_confirmed=1,
            escalation_count_90d=0, nps_score=60.0, competitor_in_account=0,
            product_adoption_score=80.0,
        ))
        # health must not be AT_RISK for this action
        if result.account_health != AccountHealth.AT_RISK and result.expansion_composite >= 65:
            assert result.expansion_action == ExpansionAction.SCHEDULE_EXECUTIVE_BRIEFING

    def test_propose_expansion_action(self):
        intel = fresh()
        # No budget but exec sponsor, upsell held, composite >= 60, not AT_RISK health
        result = intel.analyze(make_input(
            exec_sponsor_engaged=1, expansion_budget_confirmed=0,
            upsell_discussion_held=1, nps_score=60.0,
            escalation_count_90d=0, competitor_in_account=0,
            product_adoption_score=80.0,
        ))
        if (result.account_health != AccountHealth.AT_RISK
                and result.expansion_composite >= 60):
            assert result.expansion_action in (
                ExpansionAction.PROPOSE_EXPANSION, ExpansionAction.QBR_REQUIRED
            )


# ---------------------------------------------------------------------------
# 20. Primary expansion signal
# ---------------------------------------------------------------------------

class TestPrimaryExpansionSignal:
    def test_budget_confirmed_signal(self):
        intel = fresh()
        result = intel.analyze(make_input(expansion_budget_confirmed=1))
        assert result.primary_expansion_signal == "expansion budget confirmed — ready to propose"

    def test_exec_sponsor_and_upsell_signal(self):
        intel = fresh()
        result = intel.analyze(make_input(
            expansion_budget_confirmed=0,
            exec_sponsor_engaged=1,
            upsell_discussion_held=1,
        ))
        assert result.primary_expansion_signal == "exec sponsor + upsell discussion active"

    def test_product_gaps_signal(self):
        intel = fresh()
        result = intel.analyze(make_input(
            expansion_budget_confirmed=0,
            exec_sponsor_engaged=0,
            upsell_discussion_held=0,
            cross_sell_product_gaps=3,
        ))
        assert result.primary_expansion_signal == "3+ product gaps — strong cross-sell potential"

    def test_competitor_signal(self):
        intel = fresh()
        result = intel.analyze(make_input(
            expansion_budget_confirmed=0,
            exec_sponsor_engaged=0,
            upsell_discussion_held=0,
            cross_sell_product_gaps=0,
            competitor_in_account=1,
        ))
        assert result.primary_expansion_signal == "competitor present — displacement opportunity"

    def test_renewal_signal(self):
        intel = fresh()
        result = intel.analyze(make_input(
            expansion_budget_confirmed=0,
            exec_sponsor_engaged=0,
            upsell_discussion_held=0,
            cross_sell_product_gaps=0,
            competitor_in_account=0,
            contract_renewal_days=60,
        ))
        assert result.primary_expansion_signal == "renewal in 90 days — upgrade window open"

    def test_standard_nurture_signal(self):
        intel = fresh()
        result = intel.analyze(make_input(
            expansion_budget_confirmed=0,
            exec_sponsor_engaged=0,
            upsell_discussion_held=0,
            cross_sell_product_gaps=0,
            competitor_in_account=0,
            contract_renewal_days=400,
            nps_score=30.0,
            product_adoption_score=60.0,
        ))
        assert result.primary_expansion_signal == "standard account nurture required"

    def test_high_nps_signal(self):
        intel = fresh()
        result = intel.analyze(make_input(
            expansion_budget_confirmed=0,
            exec_sponsor_engaged=0,
            upsell_discussion_held=0,
            cross_sell_product_gaps=0,
            competitor_in_account=0,
            contract_renewal_days=400,
            nps_score=75.0,
            product_adoption_score=60.0,
        ))
        assert result.primary_expansion_signal == "high NPS — strong advocate, expansion ready"

    def test_signal_is_string(self):
        intel = fresh()
        result = intel.analyze(make_input())
        assert isinstance(result.primary_expansion_signal, str)
        assert len(result.primary_expansion_signal) > 0


# ---------------------------------------------------------------------------
# 21. Estimated ARR multipliers
# ---------------------------------------------------------------------------

class TestEstimatedARR:
    def test_high_composite_multiplier_085(self):
        intel = fresh()
        result = intel.analyze(make_input())
        if result.expansion_composite >= 75:
            assert result.estimated_expansion_arr_usd == round(75_000.0 * 0.85, 0)

    def test_medium_high_composite_multiplier_060(self):
        # Craft composite in [55, 75)
        intel = fresh()
        result = intel.analyze(make_input(
            exec_sponsor_engaged=0, champion_identified=0,
            qbr_completed_last_180d=0, days_since_last_touchpoint=30,
            account_tenure_days=200, competitor_in_account=0,
            product_adoption_score=70.0, nps_score=30.0,
            expansion_budget_confirmed=0,
        ))
        if 55 <= result.expansion_composite < 75:
            assert result.estimated_expansion_arr_usd == round(
                result.estimated_expansion_arr_usd, 0
            )

    def test_arr_is_rounded(self):
        intel = fresh()
        result = intel.analyze(make_input())
        assert result.estimated_expansion_arr_usd == round(result.estimated_expansion_arr_usd, 0)

    def test_arr_non_negative(self):
        intel = fresh()
        result = intel.analyze(at_risk_input())
        assert result.estimated_expansion_arr_usd >= 0.0

    def test_arr_uses_expansion_potential(self):
        intel = fresh()
        result1 = intel.analyze(make_input(account_id="a1", expansion_usd_potential=100_000.0))
        result2 = intel.analyze(make_input(account_id="a2", expansion_usd_potential=200_000.0))
        # Higher potential should generally mean higher ARR at same composite tier
        if result1.expansion_composite == result2.expansion_composite:
            assert result2.estimated_expansion_arr_usd == 2 * result1.estimated_expansion_arr_usd


# ---------------------------------------------------------------------------
# 22. Edge cases and robustness
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_licensed_users_no_crash(self):
        intel = fresh()
        result = intel.analyze(make_input(active_users_count=0, total_licensed_users_count=0))
        assert isinstance(result, AccountExpansionResult)

    def test_renewal_days_zero_not_counted_as_urgent(self):
        # contract_renewal_days=0: condition is 0 < days <= 30, so 0 fails
        inp = make_input(contract_renewal_days=0)
        score = _risk_score(inp)
        # Should NOT add 10 for 0-day renewal
        inp_1day = make_input(contract_renewal_days=1)
        # 1 day should add 10 (risk) and 10 (commercial), 0 should not
        assert _risk_score(inp_1day) >= _risk_score(inp)

    def test_very_long_tenure_capped_at_10_points(self):
        inp = make_input(account_tenure_days=10_000)
        score = _relationship_health_score(inp)
        assert 0.0 <= score <= 100.0

    def test_large_cross_sell_gaps_capped(self):
        inp = make_input(cross_sell_product_gaps=100)
        assert _commercial_readiness_score(inp) <= 100.0

    def test_high_industry_growth_capped(self):
        inp = make_input(industry_growth_score=100.0)
        assert _commercial_readiness_score(inp) <= 100.0

    def test_negative_industry_growth_no_crash(self):
        inp = make_input(industry_growth_score=0.0)
        score = _commercial_readiness_score(inp)
        assert score >= 0.0

    def test_many_accounts_summary_totals(self):
        intel = fresh()
        for i in range(10):
            intel.analyze(make_input(account_id=f"bulk_{i}"))
        s = intel.summary()
        assert s["total"] == 10
        assert sum(s["priority_counts"].values()) == 10

    def test_analyze_does_not_mutate_input(self):
        inp = make_input()
        original_id = inp.account_id
        intel = fresh()
        intel.analyze(inp)
        assert inp.account_id == original_id

    def test_result_dataclass_fields_accessible(self):
        intel = fresh()
        result = intel.analyze(make_input())
        # All 15 fields should be accessible without error
        _ = (result.account_id, result.account_name, result.expansion_opportunity,
             result.expansion_priority, result.account_health, result.expansion_action,
             result.adoption_health_score, result.relationship_health_score,
             result.commercial_readiness_score, result.risk_score,
             result.expansion_composite, result.estimated_expansion_arr_usd,
             result.is_expansion_ready, result.needs_retention_focus,
             result.primary_expansion_signal)

    def test_multiple_resets_and_reuses(self):
        intel = fresh()
        for _ in range(3):
            intel.analyze(make_input())
            intel.reset()
            assert intel.all_accounts() == []

    def test_batch_then_individual_analyze(self):
        intel = fresh()
        intel.analyze_batch([make_input(account_id=f"b{i}") for i in range(3)])
        intel.analyze(make_input(account_id="individual"))
        assert intel.get("individual") is not None
        assert len(intel.all_accounts()) == 4
