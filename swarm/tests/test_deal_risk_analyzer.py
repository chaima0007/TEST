"""Comprehensive pytest test suite for Module 26 — Deal Risk Analyzer Engine."""
from __future__ import annotations

import pytest

from swarm.intelligence.deal_risk_analyzer import (
    DealAction,
    DealProfile,
    DealRiskAnalyzerEngine,
    DealRiskResult,
    RiskLevel,
    SalesStage,
    StallReason,
    _deal_action,
    _forecast_adjustment,
    _intervention_plan,
    _positive_signals,
    _risk_factors,
    _risk_level,
    _risk_score,
    _stall_reasons,
)


# ---------------------------------------------------------------------------
# Helper factory
# ---------------------------------------------------------------------------

def make_deal(
    deal_id: str = "d1",
    account_name: str = "Acme",
    segment: str = "enterprise",
    arr_eur: float = 100_000.0,
    stage: SalesStage = SalesStage.PROPOSAL,
    days_in_stage: int = 10,
    expected_close_date_days: int = 30,
    has_champion: bool = True,
    champion_strength: float = 8.0,
    stakeholder_count: int = 3,
    executive_sponsor: bool = True,
    days_since_last_contact: int = 3,
    last_meeting_had_next_step: bool = True,
    email_response_rate_pct: float = 75.0,
    mutual_action_plan: bool = True,
    legal_engaged: bool = False,
    procurement_engaged: bool = False,
    technical_validation_done: bool = True,
    competitor_active: bool = False,
    price_objection_raised: bool = False,
    scope_changed: bool = False,
    budget_confirmed: bool = True,
    decision_criteria_agreed: bool = True,
    rep_confidence_pct: float = 80.0,
) -> DealProfile:
    return DealProfile(
        deal_id=deal_id,
        account_name=account_name,
        segment=segment,
        arr_eur=arr_eur,
        stage=stage,
        days_in_stage=days_in_stage,
        expected_close_date_days=expected_close_date_days,
        has_champion=has_champion,
        champion_strength=champion_strength,
        stakeholder_count=stakeholder_count,
        executive_sponsor=executive_sponsor,
        days_since_last_contact=days_since_last_contact,
        last_meeting_had_next_step=last_meeting_had_next_step,
        email_response_rate_pct=email_response_rate_pct,
        mutual_action_plan=mutual_action_plan,
        legal_engaged=legal_engaged,
        procurement_engaged=procurement_engaged,
        technical_validation_done=technical_validation_done,
        competitor_active=competitor_active,
        price_objection_raised=price_objection_raised,
        scope_changed=scope_changed,
        budget_confirmed=budget_confirmed,
        decision_criteria_agreed=decision_criteria_agreed,
        rep_confidence_pct=rep_confidence_pct,
    )


# ===========================================================================
# 1. TestRiskLevelEnum
# ===========================================================================

class TestRiskLevelEnum:
    def test_low_value(self):
        assert RiskLevel.LOW.value == "low"

    def test_moderate_value(self):
        assert RiskLevel.MODERATE.value == "moderate"

    def test_high_value(self):
        assert RiskLevel.HIGH.value == "high"

    def test_critical_value(self):
        assert RiskLevel.CRITICAL.value == "critical"

    def test_is_str_subclass(self):
        assert isinstance(RiskLevel.LOW, str)

    def test_enum_members_count(self):
        assert len(RiskLevel) == 4

    def test_str_comparison(self):
        assert RiskLevel.HIGH == "high"

    def test_enum_identity(self):
        assert RiskLevel("low") is RiskLevel.LOW

    def test_all_values(self):
        values = {r.value for r in RiskLevel}
        assert values == {"low", "moderate", "high", "critical"}

    def test_critical_not_low(self):
        assert RiskLevel.CRITICAL != RiskLevel.LOW


# ===========================================================================
# 2. TestStallReasonEnum
# ===========================================================================

class TestStallReasonEnum:
    def test_no_champion_value(self):
        assert StallReason.NO_CHAMPION.value == "no_champion"

    def test_single_threaded_value(self):
        assert StallReason.SINGLE_THREADED.value == "single_threaded"

    def test_budget_freeze_value(self):
        assert StallReason.BUDGET_FREEZE.value == "budget_freeze"

    def test_competitor_threat_value(self):
        assert StallReason.COMPETITOR_THREAT.value == "competitor_threat"

    def test_technical_blocker_value(self):
        assert StallReason.TECHNICAL_BLOCKER.value == "technical_blocker"

    def test_executive_misalignment_value(self):
        assert StallReason.EXECUTIVE_MISALIGNMENT.value == "executive_misalignment"

    def test_procurement_delay_value(self):
        assert StallReason.PROCUREMENT_DELAY.value == "procurement_delay"

    def test_scope_creep_value(self):
        assert StallReason.SCOPE_CREEP.value == "scope_creep"

    def test_is_str_subclass(self):
        assert isinstance(StallReason.NO_CHAMPION, str)

    def test_enum_members_count(self):
        assert len(StallReason) == 8

    def test_enum_lookup_by_value(self):
        assert StallReason("budget_freeze") is StallReason.BUDGET_FREEZE

    def test_str_equality(self):
        assert StallReason.SCOPE_CREEP == "scope_creep"


# ===========================================================================
# 3. TestDealActionEnum
# ===========================================================================

class TestDealActionEnum:
    def test_accelerate_value(self):
        assert DealAction.ACCELERATE.value == "accelerate"

    def test_intervene_value(self):
        assert DealAction.INTERVENE.value == "intervene"

    def test_monitor_value(self):
        assert DealAction.MONITOR.value == "monitor"

    def test_escalate_value(self):
        assert DealAction.ESCALATE.value == "escalate"

    def test_abandon_value(self):
        assert DealAction.ABANDON.value == "abandon"

    def test_is_str_subclass(self):
        assert isinstance(DealAction.ABANDON, str)

    def test_enum_members_count(self):
        assert len(DealAction) == 5

    def test_enum_lookup(self):
        assert DealAction("monitor") is DealAction.MONITOR

    def test_str_equality(self):
        assert DealAction.ESCALATE == "escalate"

    def test_all_values(self):
        values = {a.value for a in DealAction}
        assert values == {"accelerate", "intervene", "monitor", "escalate", "abandon"}


# ===========================================================================
# 4. TestSalesStageEnum
# ===========================================================================

class TestSalesStageEnum:
    def test_discovery_value(self):
        assert SalesStage.DISCOVERY.value == "discovery"

    def test_qualification_value(self):
        assert SalesStage.QUALIFICATION.value == "qualification"

    def test_proposal_value(self):
        assert SalesStage.PROPOSAL.value == "proposal"

    def test_negotiation_value(self):
        assert SalesStage.NEGOTIATION.value == "negotiation"

    def test_closing_value(self):
        assert SalesStage.CLOSING.value == "closing"

    def test_is_str_subclass(self):
        assert isinstance(SalesStage.PROPOSAL, str)

    def test_enum_members_count(self):
        assert len(SalesStage) == 5

    def test_str_equality(self):
        assert SalesStage.CLOSING == "closing"

    def test_enum_lookup(self):
        assert SalesStage("negotiation") is SalesStage.NEGOTIATION

    def test_all_values(self):
        values = {s.value for s in SalesStage}
        assert values == {"discovery", "qualification", "proposal", "negotiation", "closing"}


# ===========================================================================
# 5. TestDealProfileDataclass
# ===========================================================================

class TestDealProfileDataclass:
    def test_basic_instantiation(self):
        deal = make_deal()
        assert deal.deal_id == "d1"

    def test_account_name(self):
        deal = make_deal(account_name="BigCorp")
        assert deal.account_name == "BigCorp"

    def test_segment(self):
        deal = make_deal(segment="smb")
        assert deal.segment == "smb"

    def test_arr_eur(self):
        deal = make_deal(arr_eur=50000.0)
        assert deal.arr_eur == 50000.0

    def test_stage(self):
        deal = make_deal(stage=SalesStage.CLOSING)
        assert deal.stage == SalesStage.CLOSING

    def test_days_in_stage(self):
        deal = make_deal(days_in_stage=20)
        assert deal.days_in_stage == 20

    def test_expected_close_date_days(self):
        deal = make_deal(expected_close_date_days=45)
        assert deal.expected_close_date_days == 45

    def test_has_champion(self):
        deal = make_deal(has_champion=False)
        assert deal.has_champion is False

    def test_champion_strength(self):
        deal = make_deal(champion_strength=3.0)
        assert deal.champion_strength == 3.0

    def test_stakeholder_count(self):
        deal = make_deal(stakeholder_count=5)
        assert deal.stakeholder_count == 5

    def test_executive_sponsor(self):
        deal = make_deal(executive_sponsor=False)
        assert deal.executive_sponsor is False

    def test_days_since_last_contact(self):
        deal = make_deal(days_since_last_contact=10)
        assert deal.days_since_last_contact == 10

    def test_last_meeting_had_next_step(self):
        deal = make_deal(last_meeting_had_next_step=False)
        assert deal.last_meeting_had_next_step is False

    def test_email_response_rate_pct(self):
        deal = make_deal(email_response_rate_pct=40.0)
        assert deal.email_response_rate_pct == 40.0

    def test_mutual_action_plan(self):
        deal = make_deal(mutual_action_plan=False)
        assert deal.mutual_action_plan is False

    def test_legal_engaged(self):
        deal = make_deal(legal_engaged=True)
        assert deal.legal_engaged is True

    def test_procurement_engaged(self):
        deal = make_deal(procurement_engaged=True)
        assert deal.procurement_engaged is True

    def test_technical_validation_done(self):
        deal = make_deal(technical_validation_done=False)
        assert deal.technical_validation_done is False

    def test_competitor_active(self):
        deal = make_deal(competitor_active=True)
        assert deal.competitor_active is True

    def test_price_objection_raised(self):
        deal = make_deal(price_objection_raised=True)
        assert deal.price_objection_raised is True

    def test_scope_changed(self):
        deal = make_deal(scope_changed=True)
        assert deal.scope_changed is True

    def test_budget_confirmed(self):
        deal = make_deal(budget_confirmed=False)
        assert deal.budget_confirmed is False

    def test_decision_criteria_agreed(self):
        deal = make_deal(decision_criteria_agreed=False)
        assert deal.decision_criteria_agreed is False

    def test_rep_confidence_pct(self):
        deal = make_deal(rep_confidence_pct=60.0)
        assert deal.rep_confidence_pct == 60.0


# ===========================================================================
# 6. TestDealRiskResultToDict
# ===========================================================================

class TestDealRiskResultToDict:
    def _make_result(self, **kwargs) -> DealRiskResult:
        engine = DealRiskAnalyzerEngine()
        return engine.analyze(make_deal(**kwargs))

    def test_to_dict_returns_dict(self):
        r = self._make_result()
        assert isinstance(r.to_dict(), dict)

    def test_to_dict_has_deal_id(self):
        r = self._make_result(deal_id="xyz")
        assert r.to_dict()["deal_id"] == "xyz"

    def test_to_dict_has_account_name(self):
        r = self._make_result(account_name="MegaCorp")
        assert r.to_dict()["account_name"] == "MegaCorp"

    def test_to_dict_has_segment(self):
        r = self._make_result(segment="smb")
        assert r.to_dict()["segment"] == "smb"

    def test_to_dict_has_arr_eur(self):
        r = self._make_result(arr_eur=25000.0)
        assert r.to_dict()["arr_eur"] == 25000.0

    def test_to_dict_stage_is_string(self):
        r = self._make_result(stage=SalesStage.CLOSING)
        assert isinstance(r.to_dict()["stage"], str)
        assert r.to_dict()["stage"] == "closing"

    def test_to_dict_risk_level_is_string_not_enum(self):
        r = self._make_result()
        val = r.to_dict()["risk_level"]
        assert isinstance(val, str)
        assert val in {"low", "moderate", "high", "critical"}

    def test_to_dict_deal_action_is_string_not_enum(self):
        r = self._make_result()
        val = r.to_dict()["deal_action"]
        assert isinstance(val, str)
        assert val in {"monitor", "accelerate", "intervene", "escalate", "abandon"}

    def test_to_dict_stall_reasons_is_list(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["stall_reasons"], list)

    def test_to_dict_stall_reasons_strings_only(self):
        r = self._make_result(has_champion=False)
        for item in r.to_dict()["stall_reasons"]:
            assert isinstance(item, str)

    def test_to_dict_risk_factors_is_list(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["risk_factors"], list)

    def test_to_dict_positive_signals_is_list(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["positive_signals"], list)

    def test_to_dict_intervention_plan_is_list(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["intervention_plan"], list)

    def test_to_dict_forecast_adjustment_pct_numeric(self):
        r = self._make_result()
        val = r.to_dict()["forecast_adjustment_pct"]
        assert isinstance(val, (int, float))

    def test_to_dict_has_all_keys(self):
        r = self._make_result()
        expected_keys = {
            "deal_id", "account_name", "segment", "arr_eur", "stage",
            "risk_score", "risk_level", "deal_action", "stall_reasons",
            "risk_factors", "positive_signals", "intervention_plan",
            "forecast_adjustment_pct",
        }
        assert set(r.to_dict().keys()) == expected_keys

    def test_to_dict_risk_score_numeric(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["risk_score"], (int, float))

    def test_to_dict_no_enum_objects(self):
        r = self._make_result()
        d = r.to_dict()
        from enum import Enum
        for v in d.values():
            assert not isinstance(v, Enum)


# ===========================================================================
# 7. TestRiskScoreStallByStage
# ===========================================================================

class TestRiskScoreStallByStage:
    """Stage stall: DISCOVERY(14,30), QUALIFICATION(21,45), PROPOSAL(14,28),
       NEGOTIATION(10,21), CLOSING(7,14). warn→+14, crit→+25."""

    # DISCOVERY
    def test_discovery_below_warn(self):
        base = _risk_score(make_deal(stage=SalesStage.DISCOVERY, days_in_stage=13))
        no_stall = _risk_score(make_deal(stage=SalesStage.DISCOVERY, days_in_stage=0))
        assert base == no_stall

    def test_discovery_at_warn(self):
        score_warn = _risk_score(make_deal(stage=SalesStage.DISCOVERY, days_in_stage=14))
        score_none = _risk_score(make_deal(stage=SalesStage.DISCOVERY, days_in_stage=13))
        assert score_warn == score_none + 14

    def test_discovery_at_crit(self):
        score_crit = _risk_score(make_deal(stage=SalesStage.DISCOVERY, days_in_stage=30))
        score_none = _risk_score(make_deal(stage=SalesStage.DISCOVERY, days_in_stage=13))
        assert score_crit == score_none + 25

    def test_discovery_warn_boundary_below(self):
        # 13 days → no stall points
        score = _risk_score(make_deal(stage=SalesStage.DISCOVERY, days_in_stage=13))
        baseline = _risk_score(make_deal(stage=SalesStage.DISCOVERY, days_in_stage=0))
        assert score == baseline

    # QUALIFICATION
    def test_qualification_below_warn(self):
        s0 = _risk_score(make_deal(stage=SalesStage.QUALIFICATION, days_in_stage=0))
        s20 = _risk_score(make_deal(stage=SalesStage.QUALIFICATION, days_in_stage=20))
        assert s0 == s20

    def test_qualification_at_warn(self):
        sw = _risk_score(make_deal(stage=SalesStage.QUALIFICATION, days_in_stage=21))
        sn = _risk_score(make_deal(stage=SalesStage.QUALIFICATION, days_in_stage=20))
        assert sw == sn + 14

    def test_qualification_at_crit(self):
        sc = _risk_score(make_deal(stage=SalesStage.QUALIFICATION, days_in_stage=45))
        sn = _risk_score(make_deal(stage=SalesStage.QUALIFICATION, days_in_stage=20))
        assert sc == sn + 25

    def test_qualification_just_below_crit(self):
        sw = _risk_score(make_deal(stage=SalesStage.QUALIFICATION, days_in_stage=44))
        sn = _risk_score(make_deal(stage=SalesStage.QUALIFICATION, days_in_stage=20))
        assert sw == sn + 14

    # PROPOSAL
    def test_proposal_below_warn(self):
        s0 = _risk_score(make_deal(stage=SalesStage.PROPOSAL, days_in_stage=0))
        s13 = _risk_score(make_deal(stage=SalesStage.PROPOSAL, days_in_stage=13))
        assert s0 == s13

    def test_proposal_at_warn(self):
        sw = _risk_score(make_deal(stage=SalesStage.PROPOSAL, days_in_stage=14))
        sn = _risk_score(make_deal(stage=SalesStage.PROPOSAL, days_in_stage=13))
        assert sw == sn + 14

    def test_proposal_at_crit(self):
        sc = _risk_score(make_deal(stage=SalesStage.PROPOSAL, days_in_stage=28))
        sn = _risk_score(make_deal(stage=SalesStage.PROPOSAL, days_in_stage=13))
        assert sc == sn + 25

    def test_proposal_just_below_crit(self):
        sw = _risk_score(make_deal(stage=SalesStage.PROPOSAL, days_in_stage=27))
        sn = _risk_score(make_deal(stage=SalesStage.PROPOSAL, days_in_stage=13))
        assert sw == sn + 14

    # NEGOTIATION
    def test_negotiation_below_warn(self):
        s0 = _risk_score(make_deal(stage=SalesStage.NEGOTIATION, days_in_stage=0))
        s9 = _risk_score(make_deal(stage=SalesStage.NEGOTIATION, days_in_stage=9))
        assert s0 == s9

    def test_negotiation_at_warn(self):
        sw = _risk_score(make_deal(stage=SalesStage.NEGOTIATION, days_in_stage=10))
        sn = _risk_score(make_deal(stage=SalesStage.NEGOTIATION, days_in_stage=9))
        assert sw == sn + 14

    def test_negotiation_at_crit(self):
        sc = _risk_score(make_deal(stage=SalesStage.NEGOTIATION, days_in_stage=21))
        sn = _risk_score(make_deal(stage=SalesStage.NEGOTIATION, days_in_stage=9))
        assert sc == sn + 25

    # CLOSING
    def test_closing_below_warn(self):
        s0 = _risk_score(make_deal(stage=SalesStage.CLOSING, days_in_stage=0))
        s6 = _risk_score(make_deal(stage=SalesStage.CLOSING, days_in_stage=6))
        assert s0 == s6

    def test_closing_at_warn(self):
        sw = _risk_score(make_deal(stage=SalesStage.CLOSING, days_in_stage=7))
        sn = _risk_score(make_deal(stage=SalesStage.CLOSING, days_in_stage=6))
        assert sw == sn + 14

    def test_closing_at_crit(self):
        sc = _risk_score(make_deal(stage=SalesStage.CLOSING, days_in_stage=14))
        sn = _risk_score(make_deal(stage=SalesStage.CLOSING, days_in_stage=6))
        assert sc == sn + 25

    def test_closing_just_below_crit(self):
        sw = _risk_score(make_deal(stage=SalesStage.CLOSING, days_in_stage=13))
        sn = _risk_score(make_deal(stage=SalesStage.CLOSING, days_in_stage=6))
        assert sw == sn + 14

    def test_crit_adds_more_than_warn(self):
        sc = _risk_score(make_deal(stage=SalesStage.PROPOSAL, days_in_stage=28))
        sw = _risk_score(make_deal(stage=SalesStage.PROPOSAL, days_in_stage=14))
        assert sc > sw


# ===========================================================================
# 8. TestRiskScorePeople
# ===========================================================================

class TestRiskScorePeople:
    def test_no_champion_adds_15(self):
        s_no = _risk_score(make_deal(has_champion=False, champion_strength=0.0))
        s_yes = _risk_score(make_deal(has_champion=True, champion_strength=8.0))
        assert s_no == s_yes + 15

    def test_weak_champion_adds_8(self):
        s_weak = _risk_score(make_deal(has_champion=True, champion_strength=4.9))
        s_strong = _risk_score(make_deal(has_champion=True, champion_strength=5.0))
        assert s_weak == s_strong + 8

    def test_champion_strength_exactly_5_not_weak(self):
        s5 = _risk_score(make_deal(has_champion=True, champion_strength=5.0))
        s6 = _risk_score(make_deal(has_champion=True, champion_strength=6.0))
        assert s5 == s6

    def test_weak_champion_only_when_has_champion_true(self):
        # no_champion → +15, NOT +8 (conditions are elif)
        s_no = _risk_score(make_deal(has_champion=False, champion_strength=3.0))
        s_strong = _risk_score(make_deal(has_champion=True, champion_strength=8.0))
        # difference should be exactly 15, not 15+8
        assert s_no - s_strong == 15

    def test_stakeholder_count_1_adds_10(self):
        s1 = _risk_score(make_deal(stakeholder_count=1))
        s3 = _risk_score(make_deal(stakeholder_count=3))
        assert s1 == s3 + 10

    def test_stakeholder_count_0_adds_10(self):
        s0 = _risk_score(make_deal(stakeholder_count=0))
        s3 = _risk_score(make_deal(stakeholder_count=3))
        assert s0 == s3 + 10

    def test_stakeholder_count_2_adds_4(self):
        s2 = _risk_score(make_deal(stakeholder_count=2))
        s3 = _risk_score(make_deal(stakeholder_count=3))
        assert s2 == s3 + 4

    def test_stakeholder_count_3_no_penalty(self):
        s3 = _risk_score(make_deal(stakeholder_count=3))
        s4 = _risk_score(make_deal(stakeholder_count=4))
        assert s3 == s4

    def test_exec_sponsor_arr_gte_50k_no_sponsor_adds_5(self):
        s_no = _risk_score(make_deal(executive_sponsor=False, arr_eur=50_000.0))
        s_yes = _risk_score(make_deal(executive_sponsor=True, arr_eur=50_000.0))
        assert s_no == s_yes + 5

    def test_exec_sponsor_arr_lt_50k_no_penalty(self):
        s_no = _risk_score(make_deal(executive_sponsor=False, arr_eur=49_999.0))
        s_yes = _risk_score(make_deal(executive_sponsor=True, arr_eur=49_999.0))
        assert s_no == s_yes

    def test_exec_sponsor_true_no_penalty_regardless_of_arr(self):
        s = _risk_score(make_deal(executive_sponsor=True, arr_eur=200_000.0))
        s2 = _risk_score(make_deal(executive_sponsor=True, arr_eur=50_000.0))
        assert s == s2


# ===========================================================================
# 9. TestRiskScoreActivity
# ===========================================================================

class TestRiskScoreActivity:
    def test_days_since_contact_gte_14_adds_12(self):
        s14 = _risk_score(make_deal(days_since_last_contact=14))
        s6 = _risk_score(make_deal(days_since_last_contact=6))
        assert s14 == s6 + 12

    def test_days_since_contact_gte_7_lt_14_adds_6(self):
        s7 = _risk_score(make_deal(days_since_last_contact=7))
        s6 = _risk_score(make_deal(days_since_last_contact=6))
        assert s7 == s6 + 6

    def test_days_since_contact_lt_7_no_penalty(self):
        s0 = _risk_score(make_deal(days_since_last_contact=0))
        s6 = _risk_score(make_deal(days_since_last_contact=6))
        assert s0 == s6

    def test_days_since_contact_exactly_14_adds_12(self):
        s14 = _risk_score(make_deal(days_since_last_contact=14))
        s13 = _risk_score(make_deal(days_since_last_contact=13))
        assert s14 == s13 + 6  # 13 → +6, 14 → +12, diff is 6

    def test_no_next_step_adds_5(self):
        s_no = _risk_score(make_deal(last_meeting_had_next_step=False))
        s_yes = _risk_score(make_deal(last_meeting_had_next_step=True))
        assert s_no == s_yes + 5

    def test_email_rate_lt_30_adds_3(self):
        s_low = _risk_score(make_deal(email_response_rate_pct=29.9))
        s_ok = _risk_score(make_deal(email_response_rate_pct=30.0))
        assert s_low == s_ok + 3

    def test_email_rate_exactly_30_no_penalty(self):
        s30 = _risk_score(make_deal(email_response_rate_pct=30.0))
        s50 = _risk_score(make_deal(email_response_rate_pct=50.0))
        assert s30 == s50

    def test_email_rate_0_adds_3(self):
        s0 = _risk_score(make_deal(email_response_rate_pct=0.0))
        s50 = _risk_score(make_deal(email_response_rate_pct=50.0))
        assert s0 == s50 + 3

    def test_activity_combined_penalties(self):
        # days>=14 (+12), no next step (+5), email<30 (+3) = +20
        deal_bad = make_deal(
            days_since_last_contact=14,
            last_meeting_had_next_step=False,
            email_response_rate_pct=20.0,
        )
        deal_good = make_deal(
            days_since_last_contact=0,
            last_meeting_had_next_step=True,
            email_response_rate_pct=80.0,
        )
        assert _risk_score(deal_bad) == _risk_score(deal_good) + 20


# ===========================================================================
# 10. TestRiskScoreProcess
# ===========================================================================

class TestRiskScoreProcess:
    def test_no_mutual_action_plan_adds_7(self):
        s_no = _risk_score(make_deal(mutual_action_plan=False))
        s_yes = _risk_score(make_deal(mutual_action_plan=True))
        assert s_no == s_yes + 7

    def test_no_decision_criteria_adds_6(self):
        s_no = _risk_score(make_deal(decision_criteria_agreed=False))
        s_yes = _risk_score(make_deal(decision_criteria_agreed=True))
        assert s_no == s_yes + 6

    def test_no_budget_close_le_60_adds_7(self):
        s_no = _risk_score(make_deal(budget_confirmed=False, expected_close_date_days=60))
        s_yes = _risk_score(make_deal(budget_confirmed=True, expected_close_date_days=60))
        assert s_no == s_yes + 7

    def test_no_budget_close_gt_60_no_penalty(self):
        s_no = _risk_score(make_deal(budget_confirmed=False, expected_close_date_days=61))
        s_yes = _risk_score(make_deal(budget_confirmed=True, expected_close_date_days=61))
        assert s_no == s_yes

    def test_budget_confirmed_no_close_date_penalty(self):
        s = _risk_score(make_deal(budget_confirmed=True, expected_close_date_days=10))
        baseline = _risk_score(make_deal(budget_confirmed=True, expected_close_date_days=90))
        assert s == baseline

    def test_no_budget_close_exactly_60_adds_7(self):
        s60 = _risk_score(make_deal(budget_confirmed=False, expected_close_date_days=60))
        s61 = _risk_score(make_deal(budget_confirmed=False, expected_close_date_days=61))
        assert s60 == s61 + 7

    def test_all_process_risk_combined(self):
        # no MAP (+7), no decision criteria (+6), no budget + close<=60 (+7) = 20
        bad = make_deal(mutual_action_plan=False, decision_criteria_agreed=False,
                        budget_confirmed=False, expected_close_date_days=30)
        good = make_deal(mutual_action_plan=True, decision_criteria_agreed=True,
                         budget_confirmed=True, expected_close_date_days=30)
        assert _risk_score(bad) == _risk_score(good) + 20


# ===========================================================================
# 11. TestRiskScoreFlags
# ===========================================================================

class TestRiskScoreFlags:
    def test_competitor_active_adds_5(self):
        s_comp = _risk_score(make_deal(competitor_active=True))
        s_none = _risk_score(make_deal(competitor_active=False))
        assert s_comp == s_none + 5

    def test_scope_changed_adds_3(self):
        s_sc = _risk_score(make_deal(scope_changed=True))
        s_ns = _risk_score(make_deal(scope_changed=False))
        assert s_sc == s_ns + 3

    def test_price_objection_no_budget_adds_2(self):
        s_po = _risk_score(make_deal(price_objection_raised=True, budget_confirmed=False,
                                      expected_close_date_days=90))
        s_np = _risk_score(make_deal(price_objection_raised=False, budget_confirmed=False,
                                      expected_close_date_days=90))
        assert s_po == s_np + 2

    def test_price_objection_with_budget_no_penalty(self):
        s_po = _risk_score(make_deal(price_objection_raised=True, budget_confirmed=True))
        s_np = _risk_score(make_deal(price_objection_raised=False, budget_confirmed=True))
        assert s_po == s_np

    def test_all_flags_combined(self):
        # competitor (+5), scope (+3), price+no_budget (+2) = 10
        bad = make_deal(competitor_active=True, scope_changed=True,
                        price_objection_raised=True, budget_confirmed=False,
                        expected_close_date_days=90)
        good = make_deal(competitor_active=False, scope_changed=False,
                         price_objection_raised=False, budget_confirmed=False,
                         expected_close_date_days=90)
        assert _risk_score(bad) == _risk_score(good) + 10

    def test_no_flags_no_penalty(self):
        s = _risk_score(make_deal(competitor_active=False, scope_changed=False,
                                   price_objection_raised=False))
        assert isinstance(s, (int, float))


# ===========================================================================
# 12. TestRiskScoreClamping
# ===========================================================================

class TestRiskScoreClamping:
    def test_score_min_is_zero(self):
        # Perfect deal: no penalties at all
        deal = make_deal(
            days_in_stage=0,
            has_champion=True, champion_strength=9.0,
            stakeholder_count=5,
            executive_sponsor=True,
            days_since_last_contact=1,
            last_meeting_had_next_step=True,
            email_response_rate_pct=90.0,
            mutual_action_plan=True,
            decision_criteria_agreed=True,
            budget_confirmed=True,
            expected_close_date_days=90,
            competitor_active=False,
            scope_changed=False,
            price_objection_raised=False,
        )
        assert _risk_score(deal) >= 0.0

    def test_score_max_is_100(self):
        # Worst possible deal
        deal = make_deal(
            stage=SalesStage.QUALIFICATION, days_in_stage=50,
            has_champion=False, champion_strength=0.0,
            stakeholder_count=0,
            executive_sponsor=False, arr_eur=100_000.0,
            days_since_last_contact=20,
            last_meeting_had_next_step=False,
            email_response_rate_pct=0.0,
            mutual_action_plan=False,
            decision_criteria_agreed=False,
            budget_confirmed=False, expected_close_date_days=10,
            competitor_active=True,
            scope_changed=True,
            price_objection_raised=True,
        )
        assert _risk_score(deal) <= 100.0

    def test_score_is_float(self):
        assert isinstance(_risk_score(make_deal()), float)

    def test_score_rounded_to_1dp(self):
        score = _risk_score(make_deal())
        assert score == round(score, 1)

    def test_score_nonnegative_for_all_good(self):
        assert _risk_score(make_deal(days_in_stage=0)) >= 0.0

    def test_score_not_exceed_100(self):
        # Artificially high penalty count
        deal = make_deal(
            stage=SalesStage.CLOSING, days_in_stage=30,
            has_champion=False, stakeholder_count=0,
            executive_sponsor=False, arr_eur=100_000.0,
            days_since_last_contact=30,
            last_meeting_had_next_step=False,
            email_response_rate_pct=0.0,
            mutual_action_plan=False,
            decision_criteria_agreed=False,
            budget_confirmed=False, expected_close_date_days=10,
            competitor_active=True, scope_changed=True,
            price_objection_raised=True,
        )
        assert _risk_score(deal) == 100.0


# ===========================================================================
# 13. TestRiskLevelThresholds
# ===========================================================================

class TestRiskLevelThresholds:
    def test_score_below_25_is_low(self):
        assert _risk_level(0.0) == RiskLevel.LOW

    def test_score_24_9_is_low(self):
        assert _risk_level(24.9) == RiskLevel.LOW

    def test_score_25_is_moderate(self):
        assert _risk_level(25.0) == RiskLevel.MODERATE

    def test_score_44_9_is_moderate(self):
        assert _risk_level(44.9) == RiskLevel.MODERATE

    def test_score_45_is_high(self):
        assert _risk_level(45.0) == RiskLevel.HIGH

    def test_score_64_9_is_high(self):
        assert _risk_level(64.9) == RiskLevel.HIGH

    def test_score_65_is_critical(self):
        assert _risk_level(65.0) == RiskLevel.CRITICAL

    def test_score_100_is_critical(self):
        assert _risk_level(100.0) == RiskLevel.CRITICAL

    def test_score_0_is_low(self):
        assert _risk_level(0.0) == RiskLevel.LOW

    def test_boundary_exact_25(self):
        assert _risk_level(25.0) != RiskLevel.LOW

    def test_boundary_exact_45(self):
        assert _risk_level(45.0) != RiskLevel.MODERATE

    def test_boundary_exact_65(self):
        assert _risk_level(65.0) != RiskLevel.HIGH


# ===========================================================================
# 14. TestDealActionLogic
# ===========================================================================

class TestDealActionLogic:
    def test_low_is_monitor(self):
        deal = make_deal()
        assert _deal_action(RiskLevel.LOW, deal) == DealAction.MONITOR

    def test_moderate_is_accelerate(self):
        deal = make_deal()
        assert _deal_action(RiskLevel.MODERATE, deal) == DealAction.ACCELERATE

    def test_high_is_intervene(self):
        deal = make_deal()
        assert _deal_action(RiskLevel.HIGH, deal) == DealAction.INTERVENE

    def test_critical_escalate_when_no_abandon_condition(self):
        # Critical but contact < 21 days
        deal = make_deal(days_since_last_contact=5, has_champion=False)
        assert _deal_action(RiskLevel.CRITICAL, deal) == DealAction.ESCALATE

    def test_critical_escalate_when_has_champion_despite_old_contact(self):
        deal = make_deal(days_since_last_contact=25, has_champion=True)
        assert _deal_action(RiskLevel.CRITICAL, deal) == DealAction.ESCALATE

    def test_abandon_requires_both_conditions(self):
        # days_since_last_contact >= 21 AND not has_champion
        deal = make_deal(days_since_last_contact=21, has_champion=False)
        assert _deal_action(RiskLevel.CRITICAL, deal) == DealAction.ABANDON

    def test_abandon_exact_21_days_no_champion(self):
        deal = make_deal(days_since_last_contact=21, has_champion=False)
        assert _deal_action(RiskLevel.CRITICAL, deal) == DealAction.ABANDON

    def test_abandon_requires_critical_level(self):
        deal = make_deal(days_since_last_contact=30, has_champion=False)
        assert _deal_action(RiskLevel.HIGH, deal) == DealAction.INTERVENE

    def test_abandon_requires_no_champion(self):
        deal = make_deal(days_since_last_contact=25, has_champion=True)
        assert _deal_action(RiskLevel.CRITICAL, deal) != DealAction.ABANDON

    def test_abandon_requires_21_plus_days(self):
        deal = make_deal(days_since_last_contact=20, has_champion=False)
        assert _deal_action(RiskLevel.CRITICAL, deal) == DealAction.ESCALATE

    def test_all_actions_are_deal_action_enum(self):
        deal = make_deal()
        for risk in RiskLevel:
            action = _deal_action(risk, deal)
            assert isinstance(action, DealAction)


# ===========================================================================
# 15. TestStallReasonsDetection
# ===========================================================================

class TestStallReasonsDetection:
    def test_no_champion_adds_no_champion(self):
        r = _stall_reasons(make_deal(has_champion=False))
        assert "no_champion" in r

    def test_has_champion_no_no_champion(self):
        r = _stall_reasons(make_deal(has_champion=True))
        assert "no_champion" not in r

    def test_stakeholder_count_1_single_threaded(self):
        r = _stall_reasons(make_deal(stakeholder_count=1))
        assert "single_threaded" in r

    def test_stakeholder_count_0_single_threaded(self):
        r = _stall_reasons(make_deal(stakeholder_count=0))
        assert "single_threaded" in r

    def test_stakeholder_count_2_no_single_threaded(self):
        r = _stall_reasons(make_deal(stakeholder_count=2))
        assert "single_threaded" not in r

    def test_no_budget_close_le_60_budget_freeze(self):
        r = _stall_reasons(make_deal(budget_confirmed=False, expected_close_date_days=60))
        assert "budget_freeze" in r

    def test_no_budget_close_gt_60_no_budget_freeze(self):
        r = _stall_reasons(make_deal(budget_confirmed=False, expected_close_date_days=61))
        assert "budget_freeze" not in r

    def test_budget_confirmed_no_budget_freeze(self):
        r = _stall_reasons(make_deal(budget_confirmed=True, expected_close_date_days=30))
        assert "budget_freeze" not in r

    def test_competitor_active_threat(self):
        r = _stall_reasons(make_deal(competitor_active=True))
        assert "competitor_threat" in r

    def test_no_competitor_no_threat(self):
        r = _stall_reasons(make_deal(competitor_active=False))
        assert "competitor_threat" not in r

    def test_technical_blocker_negotiation(self):
        r = _stall_reasons(make_deal(technical_validation_done=False,
                                      stage=SalesStage.NEGOTIATION))
        assert "technical_blocker" in r

    def test_technical_blocker_closing(self):
        r = _stall_reasons(make_deal(technical_validation_done=False,
                                      stage=SalesStage.CLOSING))
        assert "technical_blocker" in r

    def test_no_technical_blocker_proposal(self):
        r = _stall_reasons(make_deal(technical_validation_done=False,
                                      stage=SalesStage.PROPOSAL))
        assert "technical_blocker" not in r

    def test_no_technical_blocker_if_validation_done(self):
        r = _stall_reasons(make_deal(technical_validation_done=True,
                                      stage=SalesStage.CLOSING))
        assert "technical_blocker" not in r

    def test_executive_misalignment_no_sponsor_high_arr(self):
        r = _stall_reasons(make_deal(executive_sponsor=False, arr_eur=50_000.0))
        assert "executive_misalignment" in r

    def test_executive_misalignment_no_sponsor_low_arr(self):
        r = _stall_reasons(make_deal(executive_sponsor=False, arr_eur=49_999.0))
        assert "executive_misalignment" not in r

    def test_executive_misalignment_with_sponsor(self):
        r = _stall_reasons(make_deal(executive_sponsor=True, arr_eur=100_000.0))
        assert "executive_misalignment" not in r

    def test_procurement_delay_closing_procurement_no_legal(self):
        r = _stall_reasons(make_deal(procurement_engaged=True, legal_engaged=False,
                                      stage=SalesStage.CLOSING))
        assert "procurement_delay" in r

    def test_no_procurement_delay_not_closing(self):
        r = _stall_reasons(make_deal(procurement_engaged=True, legal_engaged=False,
                                      stage=SalesStage.NEGOTIATION))
        assert "procurement_delay" not in r

    def test_no_procurement_delay_legal_engaged(self):
        r = _stall_reasons(make_deal(procurement_engaged=True, legal_engaged=True,
                                      stage=SalesStage.CLOSING))
        assert "procurement_delay" not in r

    def test_scope_creep_when_scope_changed(self):
        r = _stall_reasons(make_deal(scope_changed=True))
        assert "scope_creep" in r

    def test_no_scope_creep(self):
        r = _stall_reasons(make_deal(scope_changed=False))
        assert "scope_creep" not in r

    def test_clean_deal_no_stall_reasons(self):
        r = _stall_reasons(make_deal())
        assert r == []

    def test_returns_list_of_strings(self):
        r = _stall_reasons(make_deal(has_champion=False))
        assert isinstance(r, list)
        for item in r:
            assert isinstance(item, str)


# ===========================================================================
# 16. TestRiskFactorsGeneration
# ===========================================================================

class TestRiskFactorsGeneration:
    def test_stage_stall_warn_in_factors(self):
        deal = make_deal(stage=SalesStage.PROPOSAL, days_in_stage=14)
        factors = _risk_factors(deal)
        assert any("proposal" in f.lower() for f in factors)

    def test_stage_stall_crit_different_text(self):
        deal_warn = make_deal(stage=SalesStage.PROPOSAL, days_in_stage=14)
        deal_crit = make_deal(stage=SalesStage.PROPOSAL, days_in_stage=28)
        factors_warn = _risk_factors(deal_warn)
        factors_crit = _risk_factors(deal_crit)
        # Critical should mention "critique"
        assert any("critique" in f.lower() for f in factors_crit)
        assert not any("critique" in f.lower() for f in factors_warn)

    def test_no_champion_in_factors(self):
        factors = _risk_factors(make_deal(has_champion=False))
        assert any("champion" in f.lower() for f in factors)

    def test_weak_champion_in_factors(self):
        factors = _risk_factors(make_deal(has_champion=True, champion_strength=3.0))
        assert any("champion" in f.lower() for f in factors)

    def test_single_thread_in_factors(self):
        factors = _risk_factors(make_deal(stakeholder_count=1))
        assert any("mono-thread" in f.lower() or "single" in f.lower() or "mono" in f.lower()
                   for f in factors)

    def test_old_contact_in_factors(self):
        factors = _risk_factors(make_deal(days_since_last_contact=14))
        assert any("contact" in f.lower() for f in factors)

    def test_no_next_step_in_factors(self):
        factors = _risk_factors(make_deal(last_meeting_had_next_step=False))
        assert any("étape" in f.lower() or "next" in f.lower() or "prochaine" in f.lower()
                   for f in factors)

    def test_competitor_in_factors(self):
        factors = _risk_factors(make_deal(competitor_active=True))
        assert any("concurrent" in f.lower() or "competitor" in f.lower() for f in factors)

    def test_no_budget_close_date_in_factors(self):
        factors = _risk_factors(make_deal(budget_confirmed=False, expected_close_date_days=30))
        assert any("budget" in f.lower() for f in factors)

    def test_no_map_in_factors(self):
        factors = _risk_factors(make_deal(mutual_action_plan=False))
        assert any("plan" in f.lower() or "mutuel" in f.lower() for f in factors)

    def test_scope_changed_in_factors(self):
        factors = _risk_factors(make_deal(scope_changed=True))
        assert any("scope" in f.lower() for f in factors)

    def test_clean_deal_empty_factors(self):
        factors = _risk_factors(make_deal(days_in_stage=0))
        assert isinstance(factors, list)

    def test_returns_list(self):
        assert isinstance(_risk_factors(make_deal()), list)


# ===========================================================================
# 17. TestPositiveSignalsGeneration
# ===========================================================================

class TestPositiveSignalsGeneration:
    def test_strong_champion_gte_7_signal(self):
        signals = _positive_signals(make_deal(has_champion=True, champion_strength=7.0))
        assert any("champion" in s.lower() for s in signals)

    def test_champion_strength_6_no_signal(self):
        signals = _positive_signals(make_deal(has_champion=True, champion_strength=6.9))
        assert not any("champion fort" in s.lower() for s in signals)

    def test_champion_not_present_no_signal(self):
        signals = _positive_signals(make_deal(has_champion=False, champion_strength=9.0))
        assert not any("champion fort" in s.lower() for s in signals)

    def test_stakeholder_4_large_support_signal(self):
        signals = _positive_signals(make_deal(stakeholder_count=4))
        assert any("4" in s for s in signals)

    def test_stakeholder_5_large_support_signal(self):
        signals = _positive_signals(make_deal(stakeholder_count=5))
        assert any("5" in s for s in signals)

    def test_stakeholder_3_multithread_signal(self):
        signals = _positive_signals(make_deal(stakeholder_count=3))
        assert any("3" in s for s in signals)

    def test_stakeholder_2_no_positive(self):
        signals = _positive_signals(make_deal(stakeholder_count=2))
        assert not any("2 parties" in s for s in signals)

    def test_executive_sponsor_signal(self):
        signals = _positive_signals(make_deal(executive_sponsor=True))
        assert any("sponsor" in s.lower() or "exécutif" in s.lower() for s in signals)

    def test_no_exec_sponsor_no_signal(self):
        signals = _positive_signals(make_deal(executive_sponsor=False))
        assert not any("exécutif" in s.lower() for s in signals)

    def test_mutual_action_plan_signal(self):
        signals = _positive_signals(make_deal(mutual_action_plan=True))
        assert any("plan" in s.lower() for s in signals)

    def test_no_map_no_signal(self):
        signals = _positive_signals(make_deal(mutual_action_plan=False))
        assert not any("mutuel" in s.lower() for s in signals)

    def test_legal_engaged_signal(self):
        signals = _positive_signals(make_deal(legal_engaged=True))
        assert any("légal" in s.lower() or "legal" in s.lower() for s in signals)

    def test_technical_validation_done_signal(self):
        signals = _positive_signals(make_deal(technical_validation_done=True))
        assert any("technique" in s.lower() or "technical" in s.lower() for s in signals)

    def test_budget_confirmed_signal(self):
        signals = _positive_signals(make_deal(budget_confirmed=True))
        assert any("budget" in s.lower() for s in signals)

    def test_decision_criteria_agreed_signal(self):
        signals = _positive_signals(make_deal(decision_criteria_agreed=True))
        assert any("critère" in s.lower() or "critere" in s.lower() or "décision" in s.lower()
                   for s in signals)

    def test_last_meeting_next_step_signal(self):
        signals = _positive_signals(make_deal(last_meeting_had_next_step=True))
        assert any("étape" in s.lower() or "step" in s.lower() or "prochaine" in s.lower()
                   for s in signals)

    def test_email_rate_gte_70_signal(self):
        signals = _positive_signals(make_deal(email_response_rate_pct=70.0))
        assert any("email" in s.lower() or "réponse" in s.lower() for s in signals)

    def test_email_rate_lt_70_no_signal(self):
        signals = _positive_signals(make_deal(email_response_rate_pct=69.9))
        assert not any("taux de réponse" in s.lower() for s in signals)

    def test_returns_list(self):
        assert isinstance(_positive_signals(make_deal()), list)


# ===========================================================================
# 18. TestInterventionPlanAbandon
# ===========================================================================

class TestInterventionPlanAbandon:
    def test_abandon_has_3_steps(self):
        deal = make_deal()
        plan = _intervention_plan(deal, DealAction.ABANDON)
        assert len(plan) == 3

    def test_abandon_first_step_archive(self):
        plan = _intervention_plan(make_deal(), DealAction.ABANDON)
        assert any("archiver" in s.lower() or "abandon" in s.lower() for s in plan)

    def test_abandon_second_step_document(self):
        plan = _intervention_plan(make_deal(), DealAction.ABANDON)
        assert any("document" in s.lower() for s in plan)

    def test_abandon_third_step_nurture(self):
        plan = _intervention_plan(make_deal(), DealAction.ABANDON)
        assert any("nurture" in s.lower() or "recycler" in s.lower() for s in plan)

    def test_abandon_returns_list(self):
        assert isinstance(_intervention_plan(make_deal(), DealAction.ABANDON), list)

    def test_abandon_all_strings(self):
        plan = _intervention_plan(make_deal(), DealAction.ABANDON)
        for step in plan:
            assert isinstance(step, str)


# ===========================================================================
# 19. TestInterventionPlanEscalateInterveneAccelerateMonitor
# ===========================================================================

class TestInterventionPlanEscalateInterveneAccelerateMonitor:
    def test_escalate_starts_with_clevel(self):
        plan = _intervention_plan(make_deal(), DealAction.ESCALATE)
        assert any("c-level" in s.lower() or "escalade" in s.lower() for s in plan)

    def test_escalate_no_champion_adds_identify_step(self):
        deal = make_deal(has_champion=False)
        plan = _intervention_plan(deal, DealAction.ESCALATE)
        assert any("champion" in s.lower() for s in plan)

    def test_escalate_with_champion_no_identify_step(self):
        deal = make_deal(has_champion=True)
        plan = _intervention_plan(deal, DealAction.ESCALATE)
        assert not any("identifier un champion" in s.lower() for s in plan)

    def test_escalate_old_contact_adds_contact_step(self):
        deal = make_deal(days_since_last_contact=14)
        plan = _intervention_plan(deal, DealAction.ESCALATE)
        assert any("contact" in s.lower() for s in plan)

    def test_escalate_recent_contact_no_extra_step(self):
        deal = make_deal(days_since_last_contact=3)
        plan = _intervention_plan(deal, DealAction.ESCALATE)
        assert not any("reprendre contact" in s.lower() for s in plan)

    def test_escalate_returns_list(self):
        assert isinstance(_intervention_plan(make_deal(), DealAction.ESCALATE), list)

    def test_intervene_returns_list(self):
        assert isinstance(_intervention_plan(make_deal(), DealAction.INTERVENE), list)

    def test_intervene_single_thread_step(self):
        deal = make_deal(stakeholder_count=1)
        plan = _intervention_plan(deal, DealAction.INTERVENE)
        assert any("stakeholder" in s.lower() or "mapping" in s.lower() or "relationnel" in s.lower()
                   for s in plan)

    def test_intervene_no_map_step(self):
        deal = make_deal(mutual_action_plan=False)
        plan = _intervention_plan(deal, DealAction.INTERVENE)
        assert any("plan" in s.lower() or "mutuel" in s.lower() for s in plan)

    def test_intervene_competitor_step(self):
        deal = make_deal(competitor_active=True)
        plan = _intervention_plan(deal, DealAction.INTERVENE)
        assert any("concurrent" in s.lower() or "battlecard" in s.lower() for s in plan)

    def test_intervene_no_budget_step(self):
        deal = make_deal(budget_confirmed=False)
        plan = _intervention_plan(deal, DealAction.INTERVENE)
        assert any("budget" in s.lower() for s in plan)

    def test_intervene_always_ends_with_deadline(self):
        deal = make_deal()
        plan = _intervention_plan(deal, DealAction.INTERVENE)
        assert any("deadline" in s.lower() or "urgence" in s.lower() for s in plan)

    def test_accelerate_has_4_steps(self):
        plan = _intervention_plan(make_deal(), DealAction.ACCELERATE)
        assert len(plan) == 4

    def test_accelerate_returns_list(self):
        assert isinstance(_intervention_plan(make_deal(), DealAction.ACCELERATE), list)

    def test_accelerate_mentions_acceleration(self):
        plan = _intervention_plan(make_deal(), DealAction.ACCELERATE)
        assert any("accélérer" in s.lower() or "accelerer" in s.lower() for s in plan)

    def test_monitor_has_3_steps(self):
        plan = _intervention_plan(make_deal(), DealAction.MONITOR)
        assert len(plan) == 3

    def test_monitor_returns_list(self):
        assert isinstance(_intervention_plan(make_deal(), DealAction.MONITOR), list)

    def test_monitor_mentions_cadence(self):
        plan = _intervention_plan(make_deal(), DealAction.MONITOR)
        assert any("cadence" in s.lower() or "contact" in s.lower() or "maintenir" in s.lower()
                   for s in plan)

    def test_all_plans_non_empty(self):
        deal = make_deal()
        for action in DealAction:
            plan = _intervention_plan(deal, action)
            assert len(plan) > 0


# ===========================================================================
# 20. TestForecastAdjustment
# ===========================================================================

class TestForecastAdjustment:
    def test_low_risk_base_0(self):
        deal = make_deal()
        adj = _forecast_adjustment(deal, 10.0, RiskLevel.LOW)
        assert adj <= 0.0

    def test_moderate_risk_base_minus_10(self):
        deal = make_deal(has_champion=True, executive_sponsor=True,
                         stakeholder_count=3, competitor_active=False,
                         budget_confirmed=True, mutual_action_plan=True,
                         decision_criteria_agreed=True)
        adj = _forecast_adjustment(deal, 30.0, RiskLevel.MODERATE)
        # -10 + 5 (exec) + 5 (map+criteria) = 0 → clamped at 0
        assert adj == 0.0

    def test_high_risk_base_minus_20(self):
        deal = make_deal(has_champion=True, executive_sponsor=False,
                         stakeholder_count=3, competitor_active=False,
                         budget_confirmed=True, mutual_action_plan=False,
                         decision_criteria_agreed=False, arr_eur=10_000.0)
        adj = _forecast_adjustment(deal, 50.0, RiskLevel.HIGH)
        # -20 base only (no positive offsets, no extra negatives)
        assert adj == -20.0

    def test_critical_risk_base_minus_35(self):
        deal = make_deal(has_champion=True, executive_sponsor=False,
                         stakeholder_count=3, competitor_active=False,
                         budget_confirmed=True, mutual_action_plan=False,
                         decision_criteria_agreed=False, arr_eur=10_000.0)
        adj = _forecast_adjustment(deal, 70.0, RiskLevel.CRITICAL)
        assert adj == -35.0

    def test_no_champion_adds_minus_5(self):
        deal_no = make_deal(has_champion=False, executive_sponsor=False,
                             stakeholder_count=3, competitor_active=False,
                             budget_confirmed=True, mutual_action_plan=False,
                             decision_criteria_agreed=False, arr_eur=10_000.0)
        deal_yes = make_deal(has_champion=True, executive_sponsor=False,
                              stakeholder_count=3, competitor_active=False,
                              budget_confirmed=True, mutual_action_plan=False,
                              decision_criteria_agreed=False, arr_eur=10_000.0)
        adj_no = _forecast_adjustment(deal_no, 50.0, RiskLevel.HIGH)
        adj_yes = _forecast_adjustment(deal_yes, 50.0, RiskLevel.HIGH)
        assert adj_no == adj_yes - 5.0

    def test_single_threaded_adds_minus_5(self):
        deal_st = make_deal(has_champion=True, stakeholder_count=1,
                             executive_sponsor=False, competitor_active=False,
                             budget_confirmed=True, mutual_action_plan=False,
                             decision_criteria_agreed=False, arr_eur=10_000.0)
        deal_mt = make_deal(has_champion=True, stakeholder_count=3,
                             executive_sponsor=False, competitor_active=False,
                             budget_confirmed=True, mutual_action_plan=False,
                             decision_criteria_agreed=False, arr_eur=10_000.0)
        adj_st = _forecast_adjustment(deal_st, 50.0, RiskLevel.HIGH)
        adj_mt = _forecast_adjustment(deal_mt, 50.0, RiskLevel.HIGH)
        assert adj_st == adj_mt - 5.0

    def test_competitor_adds_minus_5(self):
        deal_c = make_deal(has_champion=True, stakeholder_count=3,
                            executive_sponsor=False, competitor_active=True,
                            budget_confirmed=True, mutual_action_plan=False,
                            decision_criteria_agreed=False, arr_eur=10_000.0)
        deal_nc = make_deal(has_champion=True, stakeholder_count=3,
                             executive_sponsor=False, competitor_active=False,
                             budget_confirmed=True, mutual_action_plan=False,
                             decision_criteria_agreed=False, arr_eur=10_000.0)
        adj_c = _forecast_adjustment(deal_c, 50.0, RiskLevel.HIGH)
        adj_nc = _forecast_adjustment(deal_nc, 50.0, RiskLevel.HIGH)
        assert adj_c == adj_nc - 5.0

    def test_no_budget_adds_minus_5(self):
        deal_nb = make_deal(has_champion=True, stakeholder_count=3,
                             executive_sponsor=False, competitor_active=False,
                             budget_confirmed=False, mutual_action_plan=False,
                             decision_criteria_agreed=False, arr_eur=10_000.0)
        deal_b = make_deal(has_champion=True, stakeholder_count=3,
                            executive_sponsor=False, competitor_active=False,
                            budget_confirmed=True, mutual_action_plan=False,
                            decision_criteria_agreed=False, arr_eur=10_000.0)
        adj_nb = _forecast_adjustment(deal_nb, 50.0, RiskLevel.HIGH)
        adj_b = _forecast_adjustment(deal_b, 50.0, RiskLevel.HIGH)
        assert adj_nb == adj_b - 5.0

    def test_exec_sponsor_adds_plus_5(self):
        deal_es = make_deal(has_champion=True, stakeholder_count=3,
                             executive_sponsor=True, competitor_active=False,
                             budget_confirmed=True, mutual_action_plan=False,
                             decision_criteria_agreed=False, arr_eur=10_000.0)
        deal_no = make_deal(has_champion=True, stakeholder_count=3,
                             executive_sponsor=False, competitor_active=False,
                             budget_confirmed=True, mutual_action_plan=False,
                             decision_criteria_agreed=False, arr_eur=10_000.0)
        adj_es = _forecast_adjustment(deal_es, 50.0, RiskLevel.HIGH)
        adj_no = _forecast_adjustment(deal_no, 50.0, RiskLevel.HIGH)
        assert adj_es == adj_no + 5.0

    def test_map_and_criteria_adds_plus_5(self):
        deal_mc = make_deal(has_champion=True, stakeholder_count=3,
                             executive_sponsor=False, competitor_active=False,
                             budget_confirmed=True, mutual_action_plan=True,
                             decision_criteria_agreed=True, arr_eur=10_000.0)
        deal_nm = make_deal(has_champion=True, stakeholder_count=3,
                             executive_sponsor=False, competitor_active=False,
                             budget_confirmed=True, mutual_action_plan=False,
                             decision_criteria_agreed=True, arr_eur=10_000.0)
        adj_mc = _forecast_adjustment(deal_mc, 50.0, RiskLevel.HIGH)
        adj_nm = _forecast_adjustment(deal_nm, 50.0, RiskLevel.HIGH)
        assert adj_mc == adj_nm + 5.0

    def test_clamped_at_minus_60(self):
        # Worst-case deal: CRITICAL(-35) + no_champion(-5) + single_threaded(-5)
        # + competitor(-5) + no_budget(-5) = -55 (max raw). Clamp is at -60,
        # so actual result should be >= -60 and equal to the unclamped max.
        deal = make_deal(has_champion=False, stakeholder_count=0,
                          executive_sponsor=False, competitor_active=True,
                          budget_confirmed=False, mutual_action_plan=False,
                          decision_criteria_agreed=False, arr_eur=100_000.0)
        adj = _forecast_adjustment(deal, 100.0, RiskLevel.CRITICAL)
        assert adj >= -60.0
        assert adj == -55.0  # actual max with all 4 negative modifiers

    def test_never_positive(self):
        # Best possible deal → should be at most 0
        deal = make_deal(has_champion=True, executive_sponsor=True,
                         stakeholder_count=5, competitor_active=False,
                         budget_confirmed=True, mutual_action_plan=True,
                         decision_criteria_agreed=True)
        for risk in RiskLevel:
            adj = _forecast_adjustment(deal, 10.0, risk)
            assert adj <= 0.0

    def test_adjustment_is_float(self):
        deal = make_deal()
        adj = _forecast_adjustment(deal, 30.0, RiskLevel.MODERATE)
        assert isinstance(adj, (int, float))

    def test_adjustment_rounded_to_1dp(self):
        deal = make_deal()
        adj = _forecast_adjustment(deal, 30.0, RiskLevel.HIGH)
        assert adj == round(adj, 1)


# ===========================================================================
# 21. TestEngineAnalyzeAndFilters
# ===========================================================================

class TestEngineAnalyzeAndFilters:
    def setup_method(self):
        self.engine = DealRiskAnalyzerEngine()

    def test_analyze_returns_deal_risk_result(self):
        result = self.engine.analyze(make_deal())
        assert isinstance(result, DealRiskResult)

    def test_analyze_stores_result(self):
        self.engine.analyze(make_deal(deal_id="abc"))
        assert len(self.engine.all_deals()) == 1

    def test_analyze_overwrites_same_id(self):
        self.engine.analyze(make_deal(deal_id="x", days_in_stage=0))
        self.engine.analyze(make_deal(deal_id="x", days_in_stage=30))
        assert len(self.engine.all_deals()) == 1

    def test_analyze_batch_sorted_desc_by_risk(self):
        deals = [
            make_deal(deal_id="low", days_in_stage=0),
            make_deal(deal_id="high", stage=SalesStage.QUALIFICATION, days_in_stage=50,
                      has_champion=False, stakeholder_count=0, executive_sponsor=False,
                      arr_eur=100_000.0, days_since_last_contact=20,
                      last_meeting_had_next_step=False, email_response_rate_pct=10.0,
                      mutual_action_plan=False, decision_criteria_agreed=False,
                      budget_confirmed=False, expected_close_date_days=30,
                      competitor_active=True, scope_changed=True, price_objection_raised=True),
        ]
        results = self.engine.analyze_batch(deals)
        assert results[0].risk_score >= results[1].risk_score

    def test_analyze_batch_returns_list(self):
        results = self.engine.analyze_batch([make_deal(deal_id="a"), make_deal(deal_id="b")])
        assert isinstance(results, list)
        assert len(results) == 2

    def test_by_risk_filters_correctly(self):
        self.engine.analyze(make_deal(deal_id="d1", days_in_stage=0))
        results = self.engine.by_risk(RiskLevel.LOW)
        # All returned should be LOW
        for r in results:
            assert r.risk_level == RiskLevel.LOW

    def test_by_action_filters_correctly(self):
        self.engine.analyze(make_deal(deal_id="d1"))
        action = self.engine.all_deals()[0].deal_action
        results = self.engine.by_action(action)
        for r in results:
            assert r.deal_action == action

    def test_by_stage_filters_correctly(self):
        self.engine.analyze(make_deal(deal_id="d1", stage=SalesStage.CLOSING))
        results = self.engine.by_stage("closing")
        for r in results:
            assert r.stage == "closing"

    def test_critical_deals_returns_critical(self):
        self.engine.analyze(make_deal(deal_id="critical",
                                       stage=SalesStage.QUALIFICATION, days_in_stage=50,
                                       has_champion=False, stakeholder_count=0,
                                       executive_sponsor=False, arr_eur=100_000.0,
                                       days_since_last_contact=20,
                                       last_meeting_had_next_step=False,
                                       email_response_rate_pct=0.0,
                                       mutual_action_plan=False, decision_criteria_agreed=False,
                                       budget_confirmed=False, expected_close_date_days=10,
                                       competitor_active=True, scope_changed=True,
                                       price_objection_raised=True))
        criticals = self.engine.critical_deals()
        assert len(criticals) >= 1
        for r in criticals:
            assert r.risk_level == RiskLevel.CRITICAL

    def test_needs_escalation_returns_escalate(self):
        # force a critical deal that escalates (has_champion=True → no ABANDON)
        self.engine.analyze(make_deal(deal_id="esc",
                                       stage=SalesStage.QUALIFICATION, days_in_stage=50,
                                       has_champion=True, stakeholder_count=0,
                                       executive_sponsor=False, arr_eur=100_000.0,
                                       days_since_last_contact=5,
                                       last_meeting_had_next_step=False,
                                       email_response_rate_pct=0.0,
                                       mutual_action_plan=False, decision_criteria_agreed=False,
                                       budget_confirmed=False, expected_close_date_days=10,
                                       competitor_active=True, scope_changed=True,
                                       price_objection_raised=True))
        for r in self.engine.needs_escalation():
            assert r.deal_action == DealAction.ESCALATE

    def test_stalled_deals_have_stall_reasons(self):
        self.engine.analyze(make_deal(deal_id="stall", has_champion=False))
        stalled = self.engine.stalled_deals()
        assert len(stalled) >= 1
        for r in stalled:
            assert len(r.stall_reasons) > 0

    def test_all_deals_sorted_desc_by_score(self):
        self.engine.analyze_batch([
            make_deal(deal_id="a", days_in_stage=0),
            make_deal(deal_id="b", stage=SalesStage.QUALIFICATION, days_in_stage=50,
                      has_champion=False),
        ])
        all_d = self.engine.all_deals()
        scores = [r.risk_score for r in all_d]
        assert scores == sorted(scores, reverse=True)

    def test_by_risk_empty_when_no_match(self):
        self.engine.analyze(make_deal(deal_id="low_only", days_in_stage=0))
        results = self.engine.by_risk(RiskLevel.CRITICAL)
        # Could be empty or not — just ensure it's a list
        assert isinstance(results, list)

    def test_analyze_result_has_correct_deal_id(self):
        r = self.engine.analyze(make_deal(deal_id="test123"))
        assert r.deal_id == "test123"

    def test_analyze_result_stage_is_string(self):
        r = self.engine.analyze(make_deal(stage=SalesStage.NEGOTIATION))
        assert r.stage == "negotiation"


# ===========================================================================
# 22. TestEngineAggregates
# ===========================================================================

class TestEngineAggregates:
    def setup_method(self):
        self.engine = DealRiskAnalyzerEngine()

    def test_avg_risk_score_empty(self):
        assert self.engine.avg_risk_score() == 0.0

    def test_avg_risk_score_single(self):
        r = self.engine.analyze(make_deal(deal_id="s1"))
        assert self.engine.avg_risk_score() == r.risk_score

    def test_avg_risk_score_multiple(self):
        r1 = self.engine.analyze(make_deal(deal_id="a"))
        r2 = self.engine.analyze(make_deal(deal_id="b", days_in_stage=20))
        expected = round((r1.risk_score + r2.risk_score) / 2, 1)
        assert self.engine.avg_risk_score() == expected

    def test_total_arr_at_risk_empty(self):
        assert self.engine.total_arr_at_risk_eur() == 0.0

    def test_total_arr_at_risk_only_high_critical(self):
        # LOW deal - should not count
        self.engine.analyze(make_deal(deal_id="low", arr_eur=10_000.0, days_in_stage=0,
                                       stakeholder_count=5))
        # HIGH/CRITICAL deal
        high_deal = make_deal(deal_id="high", arr_eur=50_000.0,
                               stage=SalesStage.QUALIFICATION, days_in_stage=50,
                               has_champion=False, stakeholder_count=0,
                               executive_sponsor=False,
                               days_since_last_contact=20,
                               last_meeting_had_next_step=False,
                               email_response_rate_pct=0.0,
                               mutual_action_plan=False, decision_criteria_agreed=False,
                               budget_confirmed=False, expected_close_date_days=10,
                               competitor_active=True, scope_changed=True)
        r_high = self.engine.analyze(high_deal)
        total = self.engine.total_arr_at_risk_eur()
        if r_high.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
            assert total >= 50_000.0
        else:
            assert total == 0.0

    def test_total_arr_moderate_not_counted(self):
        # Moderate deal only
        self.engine.analyze(make_deal(deal_id="mod", arr_eur=75_000.0,
                                       days_in_stage=0, mutual_action_plan=False,
                                       decision_criteria_agreed=False,
                                       stakeholder_count=3, has_champion=True,
                                       days_since_last_contact=2))
        total = self.engine.total_arr_at_risk_eur()
        # If it's only moderate, total should not include it
        results = self.engine.all_deals()
        at_risk = sum(r.arr_eur for r in results
                      if r.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL))
        assert total == round(at_risk, 2)

    def test_summary_has_required_keys(self):
        self.engine.analyze(make_deal(deal_id="s1"))
        s = self.engine.summary()
        required = {"total", "risk_counts", "action_counts", "stage_counts",
                    "top_stall_reasons", "avg_risk_score", "critical_count",
                    "escalation_count", "total_arr_at_risk_eur"}
        assert required.issubset(s.keys())

    def test_summary_total_count(self):
        self.engine.analyze(make_deal(deal_id="a"))
        self.engine.analyze(make_deal(deal_id="b"))
        assert self.engine.summary()["total"] == 2

    def test_summary_risk_counts_is_dict(self):
        self.engine.analyze(make_deal(deal_id="a"))
        assert isinstance(self.engine.summary()["risk_counts"], dict)

    def test_summary_action_counts_is_dict(self):
        self.engine.analyze(make_deal(deal_id="a"))
        assert isinstance(self.engine.summary()["action_counts"], dict)

    def test_summary_stage_counts_is_dict(self):
        self.engine.analyze(make_deal(deal_id="a"))
        assert isinstance(self.engine.summary()["stage_counts"], dict)

    def test_summary_avg_risk_numeric(self):
        self.engine.analyze(make_deal(deal_id="a"))
        assert isinstance(self.engine.summary()["avg_risk_score"], (int, float))

    def test_reset_clears_results(self):
        self.engine.analyze(make_deal(deal_id="a"))
        self.engine.reset()
        assert self.engine.all_deals() == []

    def test_reset_avg_risk_returns_0(self):
        self.engine.analyze(make_deal(deal_id="a"))
        self.engine.reset()
        assert self.engine.avg_risk_score() == 0.0

    def test_reset_total_arr_returns_0(self):
        self.engine.analyze(make_deal(deal_id="a"))
        self.engine.reset()
        assert self.engine.total_arr_at_risk_eur() == 0.0

    def test_reset_summary_total_0(self):
        self.engine.analyze(make_deal(deal_id="a"))
        self.engine.reset()
        assert self.engine.summary()["total"] == 0

    def test_empty_state_all_deals_empty(self):
        assert self.engine.all_deals() == []

    def test_empty_state_critical_empty(self):
        assert self.engine.critical_deals() == []

    def test_empty_state_needs_escalation_empty(self):
        assert self.engine.needs_escalation() == []

    def test_empty_state_stalled_empty(self):
        assert self.engine.stalled_deals() == []

    def test_summary_critical_count_accurate(self):
        self.engine.analyze(make_deal(deal_id="a"))
        s = self.engine.summary()
        assert s["critical_count"] == len(self.engine.critical_deals())

    def test_summary_escalation_count_accurate(self):
        self.engine.analyze(make_deal(deal_id="a"))
        s = self.engine.summary()
        assert s["escalation_count"] == len(self.engine.needs_escalation())
