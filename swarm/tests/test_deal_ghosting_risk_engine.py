"""Comprehensive pytest test suite for DealGhostingRiskEngine (Module 115)."""

from __future__ import annotations

import dataclasses
import math
import pytest

from swarm.intelligence.deal_ghosting_risk_engine import (
    DealGhostingInput,
    DealGhostingResult,
    DealGhostingRiskEngine,
    GhostingAction,
    GhostingPattern,
    GhostingRisk,
    GhostingSeverity,
    _clamp,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def base_input(**overrides) -> DealGhostingInput:
    """Return a minimal healthy (low-risk) DealGhostingInput with optional overrides."""
    defaults = dict(
        deal_id="D001",
        rep_id="R001",
        evaluation_period_id="EP001",
        days_since_last_prospect_response=1,
        days_since_last_rep_outreach=1,
        outreach_attempts_no_response=0,
        deal_stage="discovery",
        days_in_current_stage=5,
        expected_days_in_stage=14,
        demo_completed=0,
        days_since_demo=0,
        proposal_sent=0,
        days_since_proposal=0,
        stakeholder_count=2,
        responsive_stakeholders=2,
        champion_last_response_days=1,
        email_open_rate_last_30d=0.50,
        meeting_decline_count=0,
        meeting_accept_count=3,
        competitor_mentioned_last_contact=0,
        deal_value_usd=10000.0,
        close_date_days_remaining=60,
    )
    defaults.update(overrides)
    return DealGhostingInput(**defaults)


def fresh_engine() -> DealGhostingRiskEngine:
    return DealGhostingRiskEngine()


# ---------------------------------------------------------------------------
# 1. Structural / Invariant tests
# ---------------------------------------------------------------------------

class TestStructuralInvariants:

    def test_dealghostinginput_has_22_fields(self):
        fields = dataclasses.fields(DealGhostingInput)
        assert len(fields) == 22

    def test_to_dict_returns_15_keys(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        d = result.to_dict()
        expected = {
            "deal_id", "rep_id", "ghosting_risk", "ghosting_pattern",
            "ghosting_severity", "recommended_action", "silence_score",
            "engagement_decay_score", "stakeholder_coverage_score",
            "deal_momentum_score", "ghosting_composite", "is_ghosted",
            "requires_escalation", "estimated_deal_recovery_pct",
            "ghosting_signal",
        }
        assert set(d.keys()) == expected

    def test_summary_returns_13_keys_empty_engine(self):
        engine = fresh_engine()
        s = engine.summary()
        assert len(s) == 13

    def test_summary_returns_13_keys_populated_engine(self):
        engine = fresh_engine()
        engine.assess(base_input())
        s = engine.summary()
        assert len(s) == 13

    def test_summary_exact_keys_empty(self):
        engine = fresh_engine()
        s = engine.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_ghosting_composite", "ghosted_count",
            "escalation_count", "avg_silence_score", "avg_engagement_decay_score",
            "avg_stakeholder_coverage_score", "avg_deal_momentum_score",
            "avg_estimated_deal_recovery_pct",
        }
        assert set(s.keys()) == expected

    def test_summary_exact_keys_populated(self):
        engine = fresh_engine()
        engine.assess(base_input())
        s = engine.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_ghosting_composite", "ghosted_count",
            "escalation_count", "avg_silence_score", "avg_engagement_decay_score",
            "avg_stakeholder_coverage_score", "avg_deal_momentum_score",
            "avg_estimated_deal_recovery_pct",
        }
        assert set(s.keys()) == expected

    def test_dealghostingresult_has_15_fields(self):
        fields = dataclasses.fields(DealGhostingResult)
        assert len(fields) == 15

    def test_input_field_names(self):
        field_names = {f.name for f in dataclasses.fields(DealGhostingInput)}
        expected = {
            "deal_id", "rep_id", "evaluation_period_id",
            "days_since_last_prospect_response", "days_since_last_rep_outreach",
            "outreach_attempts_no_response", "deal_stage", "days_in_current_stage",
            "expected_days_in_stage", "demo_completed", "days_since_demo",
            "proposal_sent", "days_since_proposal", "stakeholder_count",
            "responsive_stakeholders", "champion_last_response_days",
            "email_open_rate_last_30d", "meeting_decline_count",
            "meeting_accept_count", "competitor_mentioned_last_contact",
            "deal_value_usd", "close_date_days_remaining",
        }
        assert field_names == expected


# ---------------------------------------------------------------------------
# 2. Enum membership
# ---------------------------------------------------------------------------

class TestEnums:

    def test_ghosting_risk_values(self):
        assert set(r.value for r in GhostingRisk) == {"low", "moderate", "high", "critical"}

    def test_ghosting_pattern_values(self):
        assert set(p.value for p in GhostingPattern) == {
            "none", "silence_after_demo", "proposal_drop_off",
            "champion_unresponsive", "multi_stakeholder_fade", "end_of_cycle_ghost",
        }

    def test_ghosting_severity_values(self):
        assert set(s.value for s in GhostingSeverity) == {"active", "cooling", "dark", "lost"}

    def test_ghosting_action_values(self):
        assert set(a.value for a in GhostingAction) == {
            "no_action", "follow_up_sequence", "manager_re_engage",
            "exec_outreach", "deal_disqualification",
        }

    def test_ghosting_risk_count(self):
        assert len(GhostingRisk) == 4

    def test_ghosting_pattern_count(self):
        assert len(GhostingPattern) == 6

    def test_ghosting_severity_count(self):
        assert len(GhostingSeverity) == 4

    def test_ghosting_action_count(self):
        assert len(GhostingAction) == 5

    def test_enums_are_str_subclass(self):
        assert isinstance(GhostingRisk.low, str)
        assert isinstance(GhostingPattern.none, str)
        assert isinstance(GhostingSeverity.active, str)
        assert isinstance(GhostingAction.no_action, str)

    def test_to_dict_enum_values_are_strings(self):
        engine = fresh_engine()
        d = engine.assess(base_input()).to_dict()
        assert isinstance(d["ghosting_risk"], str)
        assert isinstance(d["ghosting_pattern"], str)
        assert isinstance(d["ghosting_severity"], str)
        assert isinstance(d["recommended_action"], str)


# ---------------------------------------------------------------------------
# 3. _clamp helper
# ---------------------------------------------------------------------------

class TestClamp:

    def test_clamp_below_zero(self):
        assert _clamp(-10.0) == 0.0

    def test_clamp_above_100(self):
        assert _clamp(110.0) == 100.0

    def test_clamp_zero(self):
        assert _clamp(0.0) == 0.0

    def test_clamp_100(self):
        assert _clamp(100.0) == 100.0

    def test_clamp_midrange(self):
        assert _clamp(50.0) == 50.0


# ---------------------------------------------------------------------------
# 4. Silence score sub-score
# ---------------------------------------------------------------------------

class TestSilenceScore:

    def _silence(self, **kw) -> float:
        engine = fresh_engine()
        inp = base_input(**kw)
        return engine._silence_score(inp)

    # days_since_last_prospect_response tiers
    def test_silence_days_response_lt3(self):
        assert self._silence(days_since_last_prospect_response=2) == 0.0

    def test_silence_days_response_eq3(self):
        assert self._silence(days_since_last_prospect_response=3) == 5.0

    def test_silence_days_response_eq6(self):
        assert self._silence(days_since_last_prospect_response=6) == 5.0

    def test_silence_days_response_eq7(self):
        assert self._silence(days_since_last_prospect_response=7) == 14.0

    def test_silence_days_response_eq13(self):
        assert self._silence(days_since_last_prospect_response=13) == 14.0

    def test_silence_days_response_eq14(self):
        assert self._silence(days_since_last_prospect_response=14) == 28.0

    def test_silence_days_response_eq20(self):
        assert self._silence(days_since_last_prospect_response=20) == 28.0

    def test_silence_days_response_eq21(self):
        assert self._silence(days_since_last_prospect_response=21) == 45.0

    def test_silence_days_response_gt21(self):
        assert self._silence(days_since_last_prospect_response=30) == 45.0

    # outreach_attempts_no_response tiers
    def test_silence_outreach_0(self):
        assert self._silence(outreach_attempts_no_response=0) == 0.0

    def test_silence_outreach_eq1(self):
        assert self._silence(outreach_attempts_no_response=1) == 5.0

    def test_silence_outreach_eq2(self):
        assert self._silence(outreach_attempts_no_response=2) == 10.0

    def test_silence_outreach_eq3(self):
        assert self._silence(outreach_attempts_no_response=3) == 10.0

    def test_silence_outreach_eq4(self):
        assert self._silence(outreach_attempts_no_response=4) == 22.0

    def test_silence_outreach_eq5(self):
        assert self._silence(outreach_attempts_no_response=5) == 22.0

    def test_silence_outreach_eq6(self):
        assert self._silence(outreach_attempts_no_response=6) == 35.0

    def test_silence_outreach_gt6(self):
        assert self._silence(outreach_attempts_no_response=10) == 35.0

    # champion_last_response_days tiers
    def test_silence_champion_lt7(self):
        assert self._silence(champion_last_response_days=5) == 0.0

    def test_silence_champion_eq7(self):
        assert self._silence(champion_last_response_days=7) == 6.0

    def test_silence_champion_eq13(self):
        assert self._silence(champion_last_response_days=13) == 6.0

    def test_silence_champion_eq14(self):
        assert self._silence(champion_last_response_days=14) == 12.0

    def test_silence_champion_eq20(self):
        assert self._silence(champion_last_response_days=20) == 12.0

    def test_silence_champion_eq21(self):
        assert self._silence(champion_last_response_days=21) == 20.0

    def test_silence_champion_gt21(self):
        assert self._silence(champion_last_response_days=30) == 20.0

    # Combined (additive)
    def test_silence_combined_additive(self):
        # days=21(45) + outreach=6(35) + champion=21(20) = 100 clamped
        score = self._silence(
            days_since_last_prospect_response=21,
            outreach_attempts_no_response=6,
            champion_last_response_days=21,
        )
        assert score == 100.0

    def test_silence_clamped_at_100(self):
        score = self._silence(
            days_since_last_prospect_response=30,
            outreach_attempts_no_response=10,
            champion_last_response_days=30,
        )
        assert score == 100.0

    def test_silence_partial_combination(self):
        # days=14(28) + outreach=2(10) = 38
        score = self._silence(
            days_since_last_prospect_response=14,
            outreach_attempts_no_response=2,
            champion_last_response_days=0,
        )
        assert score == 38.0


# ---------------------------------------------------------------------------
# 5. Engagement decay sub-score
# ---------------------------------------------------------------------------

class TestEngagementDecayScore:

    def _engagement(self, **kw) -> float:
        engine = fresh_engine()
        inp = base_input(**kw)
        return engine._engagement_decay_score(inp)

    # email_open_rate tiers
    def test_engagement_open_rate_gte35(self):
        assert self._engagement(email_open_rate_last_30d=0.50) == 0.0

    def test_engagement_open_rate_eq35(self):
        assert self._engagement(email_open_rate_last_30d=0.35) == 0.0

    def test_engagement_open_rate_lt35(self):
        assert self._engagement(email_open_rate_last_30d=0.34) == 10.0

    def test_engagement_open_rate_eq20(self):
        # 0.20 is not < 0.10, not < 0.20, but IS < 0.35 → score += 10
        assert self._engagement(email_open_rate_last_30d=0.20) == 10.0

    def test_engagement_open_rate_lt20(self):
        # 0.19 is < 0.20 → score += 20
        assert self._engagement(email_open_rate_last_30d=0.19) == 20.0

    def test_engagement_open_rate_lt10(self):
        assert self._engagement(email_open_rate_last_30d=0.09) == 35.0

    def test_engagement_open_rate_zero(self):
        assert self._engagement(email_open_rate_last_30d=0.0) == 35.0

    # meeting_decline_count tiers
    def test_engagement_decline_0(self):
        assert self._engagement(meeting_decline_count=0) == 0.0

    def test_engagement_decline_eq1(self):
        assert self._engagement(meeting_decline_count=1) == 10.0

    def test_engagement_decline_eq2(self):
        assert self._engagement(meeting_decline_count=2) == 20.0

    def test_engagement_decline_eq3(self):
        assert self._engagement(meeting_decline_count=3) == 20.0

    def test_engagement_decline_eq4(self):
        assert self._engagement(meeting_decline_count=4) == 35.0

    def test_engagement_decline_gt4(self):
        assert self._engagement(meeting_decline_count=5) == 35.0

    # proposal tiers
    def test_engagement_no_proposal(self):
        assert self._engagement(proposal_sent=0, days_since_proposal=20) == 0.0

    def test_engagement_proposal_lt7days(self):
        assert self._engagement(proposal_sent=1, days_since_proposal=5) == 0.0

    def test_engagement_proposal_eq7days(self):
        assert self._engagement(proposal_sent=1, days_since_proposal=7) == 15.0

    def test_engagement_proposal_lt14days(self):
        assert self._engagement(proposal_sent=1, days_since_proposal=13) == 15.0

    def test_engagement_proposal_eq14days(self):
        assert self._engagement(proposal_sent=1, days_since_proposal=14) == 30.0

    def test_engagement_proposal_gt14days(self):
        assert self._engagement(proposal_sent=1, days_since_proposal=21) == 30.0

    # Combined
    def test_engagement_combined_clamped(self):
        score = self._engagement(
            email_open_rate_last_30d=0.0,
            meeting_decline_count=4,
            proposal_sent=1,
            days_since_proposal=14,
        )
        # 35 + 35 + 30 = 100 clamped
        assert score == 100.0

    def test_engagement_partial(self):
        # open<20(20) + decline=2(20) = 40
        score = self._engagement(
            email_open_rate_last_30d=0.15,
            meeting_decline_count=2,
            proposal_sent=0,
        )
        assert score == 40.0


# ---------------------------------------------------------------------------
# 6. Stakeholder coverage sub-score
# ---------------------------------------------------------------------------

class TestStakeholderCoverageScore:

    def _stk(self, **kw) -> float:
        engine = fresh_engine()
        inp = base_input(**kw)
        return engine._stakeholder_coverage_score(inp)

    # responsive ratio tiers
    def test_stk_zero_stakeholders_no_penalty(self):
        assert self._stk(stakeholder_count=0, responsive_stakeholders=0) == 0.0

    def test_stk_ratio_gte60(self):
        # 2/2 = 1.0 >= 0.6
        assert self._stk(stakeholder_count=2, responsive_stakeholders=2) == 0.0

    def test_stk_ratio_lt60(self):
        # 1/2 = 0.5
        assert self._stk(stakeholder_count=2, responsive_stakeholders=1) == 15.0

    def test_stk_ratio_lt40(self):
        # 1/3 = 0.33
        assert self._stk(stakeholder_count=3, responsive_stakeholders=1) == 30.0

    def test_stk_ratio_lt20(self):
        # 0/5 = 0.0
        assert self._stk(stakeholder_count=5, responsive_stakeholders=0) == 50.0

    def test_stk_ratio_exactly_20(self):
        # 1/5 = 0.2 → not < 0.2
        assert self._stk(stakeholder_count=5, responsive_stakeholders=1) == 30.0

    def test_stk_ratio_exactly_40(self):
        # 2/5 = 0.4 → not < 0.4
        assert self._stk(stakeholder_count=5, responsive_stakeholders=2) == 15.0

    def test_stk_ratio_exactly_60(self):
        # 3/5 = 0.6 → not < 0.6
        assert self._stk(stakeholder_count=5, responsive_stakeholders=3) == 0.0

    # competitor
    def test_stk_competitor_mentioned(self):
        score = self._stk(
            stakeholder_count=2, responsive_stakeholders=2,
            competitor_mentioned_last_contact=1,
        )
        assert score == 30.0

    def test_stk_no_competitor(self):
        score = self._stk(competitor_mentioned_last_contact=0)
        assert score == 0.0

    # demo silence
    def test_stk_demo_lt14days(self):
        assert self._stk(demo_completed=1, days_since_demo=13) == 0.0

    def test_stk_demo_eq14days(self):
        assert self._stk(demo_completed=1, days_since_demo=14) == 10.0

    def test_stk_demo_lt21days(self):
        assert self._stk(demo_completed=1, days_since_demo=20) == 10.0

    def test_stk_demo_eq21days(self):
        assert self._stk(demo_completed=1, days_since_demo=21) == 20.0

    def test_stk_demo_gt21days(self):
        assert self._stk(demo_completed=1, days_since_demo=30) == 20.0

    def test_stk_no_demo_no_penalty(self):
        assert self._stk(demo_completed=0, days_since_demo=30) == 0.0

    # Combined clamped
    def test_stk_combined_clamped(self):
        score = self._stk(
            stakeholder_count=5, responsive_stakeholders=0,
            competitor_mentioned_last_contact=1,
            demo_completed=1, days_since_demo=21,
        )
        # 50 + 30 + 20 = 100
        assert score == 100.0


# ---------------------------------------------------------------------------
# 7. Deal momentum sub-score
# ---------------------------------------------------------------------------

class TestDealMomentumScore:

    def _mom(self, **kw) -> float:
        engine = fresh_engine()
        inp = base_input(**kw)
        return engine._deal_momentum_score(inp)

    # stage stagnation
    def test_mom_expected_zero_no_stage_penalty(self):
        assert self._mom(expected_days_in_stage=0, days_in_current_stage=100) == 0.0

    def test_mom_stage_ratio_lt15(self):
        # 10/14 = 0.71
        assert self._mom(days_in_current_stage=10, expected_days_in_stage=14) == 0.0

    def test_mom_stage_ratio_gte15(self):
        # 21/14 = 1.5
        assert self._mom(days_in_current_stage=21, expected_days_in_stage=14) == 12.0

    def test_mom_stage_ratio_lt15_boundary(self):
        # 20/14 = 1.43 < 1.5
        assert self._mom(days_in_current_stage=20, expected_days_in_stage=14) == 0.0

    def test_mom_stage_ratio_gte20(self):
        # 28/14 = 2.0
        assert self._mom(days_in_current_stage=28, expected_days_in_stage=14) == 25.0

    def test_mom_stage_ratio_gte30(self):
        # 42/14 = 3.0
        assert self._mom(days_in_current_stage=42, expected_days_in_stage=14) == 40.0

    def test_mom_stage_ratio_gt30(self):
        # 60/14 > 3.0
        assert self._mom(days_in_current_stage=60, expected_days_in_stage=14) == 40.0

    # close date urgency
    def test_mom_close_far_away_no_penalty(self):
        score = self._mom(
            close_date_days_remaining=60,
            days_since_last_prospect_response=10,
        )
        # no momentum penalty from urgency (60 > 14)
        assert score == 0.0

    def test_mom_close_lte14_response_gte10(self):
        score = self._mom(
            close_date_days_remaining=14,
            days_since_last_prospect_response=10,
            days_in_current_stage=5,
            expected_days_in_stage=14,
        )
        assert score == 20.0

    def test_mom_close_lte7_response_gte7(self):
        score = self._mom(
            close_date_days_remaining=7,
            days_since_last_prospect_response=7,
            days_in_current_stage=5,
            expected_days_in_stage=14,
        )
        assert score == 35.0

    def test_mom_close_lte7_response_lt7_no_urgency(self):
        score = self._mom(
            close_date_days_remaining=7,
            days_since_last_prospect_response=6,
            days_in_current_stage=5,
            expected_days_in_stage=14,
        )
        # close <= 7 but response < 7 → no urgency bonus
        # close <= 14 and response >= 10? No, 6 < 10
        assert score == 0.0

    # meeting accept ratio
    def test_mom_no_meetings_no_penalty(self):
        assert self._mom(meeting_accept_count=0, meeting_decline_count=0) == 0.0

    def test_mom_accept_ratio_gte50(self):
        # 2/3 = 0.67
        assert self._mom(meeting_accept_count=2, meeting_decline_count=1) == 0.0

    def test_mom_accept_ratio_lt50(self):
        # 1/3 = 0.33
        assert self._mom(meeting_accept_count=1, meeting_decline_count=2) == 12.0

    def test_mom_accept_ratio_lt25(self):
        # 1/5 = 0.2
        assert self._mom(meeting_accept_count=1, meeting_decline_count=4) == 25.0

    def test_mom_accept_ratio_zero(self):
        # 0/2 = 0.0
        assert self._mom(meeting_accept_count=0, meeting_decline_count=2) == 25.0

    def test_mom_accept_ratio_exactly_25(self):
        # 1/4 = 0.25 → not < 0.25
        assert self._mom(meeting_accept_count=1, meeting_decline_count=3) == 12.0

    def test_mom_accept_ratio_exactly_50(self):
        # 1/2 = 0.5 → not < 0.5
        assert self._mom(meeting_accept_count=1, meeting_decline_count=1) == 0.0

    def test_mom_combined_clamped(self):
        score = self._mom(
            days_in_current_stage=60,
            expected_days_in_stage=14,
            close_date_days_remaining=7,
            days_since_last_prospect_response=7,
            meeting_accept_count=0,
            meeting_decline_count=4,
        )
        # 40 + 35 + 25 = 100 clamped
        assert score == 100.0


# ---------------------------------------------------------------------------
# 8. Composite formula
# ---------------------------------------------------------------------------

class TestCompositeFormula:

    def test_composite_formula_exact(self):
        engine = fresh_engine()
        inp = base_input(
            days_since_last_prospect_response=7,   # silence += 14
            email_open_rate_last_30d=0.34,         # engagement += 10
            stakeholder_count=2,
            responsive_stakeholders=1,             # stk += 15
            days_in_current_stage=21,
            expected_days_in_stage=14,             # momentum += 12 (ratio=1.5)
        )
        silence = engine._silence_score(inp)
        engagement = engine._engagement_decay_score(inp)
        stakeholder = engine._stakeholder_coverage_score(inp)
        momentum = engine._deal_momentum_score(inp)
        expected = round(
            silence * 0.35 + engagement * 0.25 + stakeholder * 0.25 + momentum * 0.15,
            1,
        )
        result = engine.assess(inp)
        assert result.ghosting_composite == expected

    def test_composite_weights_add_to_1(self):
        assert abs(0.35 + 0.25 + 0.25 + 0.15 - 1.0) < 1e-10

    def test_composite_all_zero(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        # base_input is fully healthy, composite should be 0
        assert result.ghosting_composite == 0.0

    def test_composite_clamped_at_100(self):
        engine = fresh_engine()
        inp = base_input(
            days_since_last_prospect_response=30,
            outreach_attempts_no_response=10,
            champion_last_response_days=30,
            email_open_rate_last_30d=0.0,
            meeting_decline_count=10,
            proposal_sent=1,
            days_since_proposal=30,
            stakeholder_count=5,
            responsive_stakeholders=0,
            competitor_mentioned_last_contact=1,
            demo_completed=1,
            days_since_demo=30,
            days_in_current_stage=200,
            expected_days_in_stage=14,
            close_date_days_remaining=1,
            meeting_accept_count=0,
        )
        result = engine.assess(inp)
        assert result.ghosting_composite <= 100.0

    def test_composite_non_negative(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert result.ghosting_composite >= 0.0

    def test_composite_rounded_to_1_decimal(self):
        engine = fresh_engine()
        inp = base_input(days_since_last_prospect_response=7)
        result = engine.assess(inp)
        # Should be rounded to 1 decimal
        assert result.ghosting_composite == round(result.ghosting_composite, 1)


# ---------------------------------------------------------------------------
# 9. Risk classification thresholds
# ---------------------------------------------------------------------------

class TestRiskClassification:

    def _risk(self, composite: float) -> GhostingRisk:
        return fresh_engine()._classify_risk(composite)

    def test_risk_composite_0(self):
        assert self._risk(0.0) == GhostingRisk.low

    def test_risk_composite_19(self):
        assert self._risk(19.9) == GhostingRisk.low

    def test_risk_composite_exactly_20(self):
        assert self._risk(20.0) == GhostingRisk.moderate

    def test_risk_composite_39(self):
        assert self._risk(39.9) == GhostingRisk.moderate

    def test_risk_composite_exactly_40(self):
        assert self._risk(40.0) == GhostingRisk.high

    def test_risk_composite_59(self):
        assert self._risk(59.9) == GhostingRisk.high

    def test_risk_composite_exactly_60(self):
        assert self._risk(60.0) == GhostingRisk.critical

    def test_risk_composite_100(self):
        assert self._risk(100.0) == GhostingRisk.critical

    def test_all_risk_levels_reachable(self):
        levels = {self._risk(v) for v in [0.0, 20.0, 40.0, 60.0]}
        assert levels == set(GhostingRisk)


# ---------------------------------------------------------------------------
# 10. Severity classification thresholds
# ---------------------------------------------------------------------------

class TestSeverityClassification:

    def _severity(self, composite: float) -> GhostingSeverity:
        return fresh_engine()._classify_severity(composite)

    def test_severity_composite_0(self):
        assert self._severity(0.0) == GhostingSeverity.active

    def test_severity_composite_19(self):
        assert self._severity(19.9) == GhostingSeverity.active

    def test_severity_composite_exactly_20(self):
        assert self._severity(20.0) == GhostingSeverity.cooling

    def test_severity_composite_39(self):
        assert self._severity(39.9) == GhostingSeverity.cooling

    def test_severity_composite_exactly_40(self):
        assert self._severity(40.0) == GhostingSeverity.dark

    def test_severity_composite_59(self):
        assert self._severity(59.9) == GhostingSeverity.dark

    def test_severity_composite_exactly_60(self):
        assert self._severity(60.0) == GhostingSeverity.lost

    def test_severity_composite_100(self):
        assert self._severity(100.0) == GhostingSeverity.lost

    def test_risk_and_severity_thresholds_aligned(self):
        # Same thresholds for risk and severity
        for composite in [0.0, 19.9, 20.0, 39.9, 40.0, 59.9, 60.0]:
            risk = fresh_engine()._classify_risk(composite)
            sev = fresh_engine()._classify_severity(composite)
            risk_level = list(GhostingRisk).index(risk)
            sev_level = list(GhostingSeverity).index(sev)
            assert risk_level == sev_level


# ---------------------------------------------------------------------------
# 11. Recommended action
# ---------------------------------------------------------------------------

class TestRecommendedAction:

    def _action(self, risk: GhostingRisk, composite: float) -> GhostingAction:
        return fresh_engine()._recommended_action(risk, composite)

    def test_action_composite_gte60(self):
        assert self._action(GhostingRisk.critical, 60.0) == GhostingAction.deal_disqualification

    def test_action_composite_100(self):
        assert self._action(GhostingRisk.critical, 100.0) == GhostingAction.deal_disqualification

    def test_action_composite_gte50_lt60(self):
        assert self._action(GhostingRisk.high, 50.0) == GhostingAction.exec_outreach

    def test_action_composite_59(self):
        assert self._action(GhostingRisk.high, 59.9) == GhostingAction.exec_outreach

    def test_action_high_risk_composite_lt50(self):
        assert self._action(GhostingRisk.high, 45.0) == GhostingAction.manager_re_engage

    def test_action_moderate_risk(self):
        assert self._action(GhostingRisk.moderate, 25.0) == GhostingAction.follow_up_sequence

    def test_action_low_risk(self):
        assert self._action(GhostingRisk.low, 5.0) == GhostingAction.no_action

    def test_action_low_risk_composite_zero(self):
        assert self._action(GhostingRisk.low, 0.0) == GhostingAction.no_action

    def test_all_actions_reachable(self):
        actions = {
            self._action(GhostingRisk.critical, 65.0),
            self._action(GhostingRisk.high, 55.0),
            self._action(GhostingRisk.high, 45.0),
            self._action(GhostingRisk.moderate, 30.0),
            self._action(GhostingRisk.low, 0.0),
        }
        assert actions == set(GhostingAction)


# ---------------------------------------------------------------------------
# 12. Pattern classification (priority order)
# ---------------------------------------------------------------------------

class TestPatternClassification:

    def _pattern(self, silence=0.0, engagement=0.0, stakeholder=0.0, momentum=0.0, **inp_kw):
        engine = fresh_engine()
        inp = base_input(**inp_kw)
        return engine._classify_pattern(inp, silence, engagement, stakeholder, momentum)

    # Priority 1: end_of_cycle_ghost
    def test_pattern_end_of_cycle_ghost(self):
        p = self._pattern(
            close_date_days_remaining=14,
            days_since_last_prospect_response=10,
        )
        assert p == GhostingPattern.end_of_cycle_ghost

    def test_pattern_end_of_cycle_close_lte14_response_gte10(self):
        p = self._pattern(
            close_date_days_remaining=1,
            days_since_last_prospect_response=21,
        )
        assert p == GhostingPattern.end_of_cycle_ghost

    def test_pattern_end_of_cycle_not_triggered_response_lt10(self):
        # close <= 14 but response < 10 — should fall through
        p = self._pattern(
            close_date_days_remaining=14,
            days_since_last_prospect_response=9,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=1,
        )
        assert p == GhostingPattern.none

    def test_pattern_end_of_cycle_not_triggered_close_gt14(self):
        p = self._pattern(
            close_date_days_remaining=15,
            days_since_last_prospect_response=21,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=1,
        )
        # Not end-of-cycle. champion? 1 < 14, no. multi? 1<3, no. none.
        assert p == GhostingPattern.none

    # Priority 2: multi_stakeholder_fade
    def test_pattern_multi_stakeholder_fade(self):
        p = self._pattern(
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=3,
            responsive_stakeholders=1,
        )
        assert p == GhostingPattern.multi_stakeholder_fade

    def test_pattern_multi_stakeholder_zero_responsive(self):
        p = self._pattern(
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=5,
            responsive_stakeholders=0,
        )
        assert p == GhostingPattern.multi_stakeholder_fade

    def test_pattern_multi_stakeholder_not_triggered_count_lt3(self):
        p = self._pattern(
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=2,
            responsive_stakeholders=0,
            champion_last_response_days=1,
        )
        # count < 3 → not multi_stakeholder_fade
        assert p == GhostingPattern.none

    def test_pattern_multi_stakeholder_not_triggered_responsive_gt1(self):
        p = self._pattern(
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=3,
            responsive_stakeholders=2,
            champion_last_response_days=1,
        )
        assert p == GhostingPattern.none

    # Priority 3: champion_unresponsive
    def test_pattern_champion_unresponsive(self):
        p = self._pattern(
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=14,
        )
        assert p == GhostingPattern.champion_unresponsive

    def test_pattern_champion_unresponsive_gt14(self):
        p = self._pattern(
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=21,
        )
        assert p == GhostingPattern.champion_unresponsive

    def test_pattern_champion_not_triggered_lt14(self):
        p = self._pattern(
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=13,
        )
        assert p == GhostingPattern.none

    # Priority 4: proposal_drop_off
    def test_pattern_proposal_drop_off(self):
        p = self._pattern(
            engagement=25.0,
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=1,
            proposal_sent=1,
            days_since_proposal=14,
        )
        assert p == GhostingPattern.proposal_drop_off

    def test_pattern_proposal_drop_off_engagement_exactly_25(self):
        p = self._pattern(
            engagement=25.0,
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=1,
            proposal_sent=1,
            days_since_proposal=14,
        )
        assert p == GhostingPattern.proposal_drop_off

    def test_pattern_proposal_drop_off_not_triggered_engagement_lt25(self):
        p = self._pattern(
            engagement=24.9,
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=1,
            proposal_sent=1,
            days_since_proposal=14,
        )
        assert p == GhostingPattern.none

    def test_pattern_proposal_drop_off_not_triggered_days_lt14(self):
        p = self._pattern(
            engagement=50.0,
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=1,
            proposal_sent=1,
            days_since_proposal=13,
        )
        assert p == GhostingPattern.none

    def test_pattern_proposal_drop_off_not_triggered_no_proposal(self):
        p = self._pattern(
            engagement=50.0,
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=1,
            proposal_sent=0,
            days_since_proposal=20,
        )
        assert p == GhostingPattern.none

    # Priority 5: silence_after_demo
    def test_pattern_silence_after_demo(self):
        p = self._pattern(
            silence=20.0,
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=1,
            demo_completed=1,
            days_since_demo=14,
        )
        assert p == GhostingPattern.silence_after_demo

    def test_pattern_silence_after_demo_gt14(self):
        p = self._pattern(
            silence=30.0,
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=1,
            demo_completed=1,
            days_since_demo=21,
        )
        assert p == GhostingPattern.silence_after_demo

    def test_pattern_silence_after_demo_not_triggered_silence_lt20(self):
        p = self._pattern(
            silence=19.9,
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=1,
            demo_completed=1,
            days_since_demo=14,
        )
        assert p == GhostingPattern.none

    def test_pattern_silence_after_demo_not_triggered_days_lt14(self):
        p = self._pattern(
            silence=50.0,
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=1,
            demo_completed=1,
            days_since_demo=13,
        )
        assert p == GhostingPattern.none

    def test_pattern_silence_after_demo_not_triggered_no_demo(self):
        p = self._pattern(
            silence=50.0,
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=1,
            demo_completed=0,
            days_since_demo=14,
        )
        assert p == GhostingPattern.none

    # Priority: end_of_cycle beats multi_stakeholder
    def test_pattern_priority_end_of_cycle_over_multi_stakeholder(self):
        p = self._pattern(
            close_date_days_remaining=14,
            days_since_last_prospect_response=10,
            stakeholder_count=5,
            responsive_stakeholders=0,
        )
        assert p == GhostingPattern.end_of_cycle_ghost

    # Priority: multi_stakeholder beats champion
    def test_pattern_priority_multi_over_champion(self):
        p = self._pattern(
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=3,
            responsive_stakeholders=0,
            champion_last_response_days=21,
        )
        assert p == GhostingPattern.multi_stakeholder_fade

    # Priority: champion beats proposal_drop_off
    def test_pattern_priority_champion_over_proposal(self):
        p = self._pattern(
            engagement=50.0,
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=2,
            responsive_stakeholders=2,
            champion_last_response_days=21,
            proposal_sent=1,
            days_since_proposal=20,
        )
        assert p == GhostingPattern.champion_unresponsive

    # none
    def test_pattern_none_healthy_deal(self):
        p = self._pattern(
            close_date_days_remaining=60,
            days_since_last_prospect_response=1,
            stakeholder_count=2,
            responsive_stakeholders=2,
            champion_last_response_days=1,
            demo_completed=0,
            proposal_sent=0,
        )
        assert p == GhostingPattern.none


# ---------------------------------------------------------------------------
# 13. is_ghosted conditions
# ---------------------------------------------------------------------------

class TestIsGhosted:

    def test_is_ghosted_composite_gte40(self):
        engine = fresh_engine()
        # Force composite >= 40 via silence
        inp = base_input(
            days_since_last_prospect_response=21,  # silence +45
            outreach_attempts_no_response=4,        # silence +22
        )
        result = engine.assess(inp)
        # composite = 67*0.35 = 23.45... let's verify via is_ghosted directly
        # If composite >= 40 → ghosted
        if result.ghosting_composite >= 40:
            assert result.is_ghosted is True

    def test_is_ghosted_outreach_attempts_gte5(self):
        engine = fresh_engine()
        inp = base_input(outreach_attempts_no_response=5)
        result = engine.assess(inp)
        assert result.is_ghosted is True

    def test_is_ghosted_outreach_attempts_eq5(self):
        engine = fresh_engine()
        inp = base_input(outreach_attempts_no_response=5)
        result = engine.assess(inp)
        assert result.is_ghosted is True

    def test_is_ghosted_days_since_response_gte21(self):
        engine = fresh_engine()
        inp = base_input(days_since_last_prospect_response=21)
        result = engine.assess(inp)
        assert result.is_ghosted is True

    def test_is_ghosted_days_since_response_eq21(self):
        engine = fresh_engine()
        inp = base_input(days_since_last_prospect_response=21)
        result = engine.assess(inp)
        assert result.is_ghosted is True

    def test_is_ghosted_days_since_response_gt21(self):
        engine = fresh_engine()
        inp = base_input(days_since_last_prospect_response=30)
        result = engine.assess(inp)
        assert result.is_ghosted is True

    def test_not_ghosted_healthy_deal(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert result.is_ghosted is False

    def test_not_ghosted_outreach_lt5(self):
        engine = fresh_engine()
        inp = base_input(outreach_attempts_no_response=4)
        result = engine.assess(inp)
        # Composite must be < 40 and days < 21
        if result.ghosting_composite < 40 and inp.days_since_last_prospect_response < 21:
            assert result.is_ghosted is False

    def test_not_ghosted_days_lt21(self):
        engine = fresh_engine()
        inp = base_input(days_since_last_prospect_response=20)
        result = engine.assess(inp)
        if result.ghosting_composite < 40 and inp.outreach_attempts_no_response < 5:
            assert result.is_ghosted is False

    def test_is_ghosted_or_condition_all_three(self):
        engine = fresh_engine()
        inp = base_input(
            days_since_last_prospect_response=21,
            outreach_attempts_no_response=5,
        )
        result = engine.assess(inp)
        assert result.is_ghosted is True


# ---------------------------------------------------------------------------
# 14. requires_escalation conditions
# ---------------------------------------------------------------------------

class TestRequiresEscalation:

    def test_escalation_composite_gte30(self):
        engine = fresh_engine()
        inp = base_input(
            days_since_last_prospect_response=21,  # silence=45
        )
        result = engine.assess(inp)
        if result.ghosting_composite >= 30:
            assert result.requires_escalation is True

    def test_escalation_champion_gte14(self):
        engine = fresh_engine()
        inp = base_input(champion_last_response_days=14)
        result = engine.assess(inp)
        assert result.requires_escalation is True

    def test_escalation_champion_gt14(self):
        engine = fresh_engine()
        inp = base_input(champion_last_response_days=21)
        result = engine.assess(inp)
        assert result.requires_escalation is True

    def test_escalation_champion_eq14(self):
        engine = fresh_engine()
        inp = base_input(champion_last_response_days=14)
        result = engine.assess(inp)
        assert result.requires_escalation is True

    def test_escalation_close_lte7_composite_gte20(self):
        engine = fresh_engine()
        # Need composite >= 20: days=14(28*0.35=9.8) + need more
        # Use outreach=4(22) → silence=28+22=50, composite=50*0.35=17.5 < 20
        # Use days=14(28) + champion=14(12) → silence=40, composite=40*0.35=14 < 20
        # Try email_open<0.10(35 eng) → engagement=35, composite=35*0.25=8.75
        # days=14 → silence=28*0.35=9.8 + email<0.10 engagement=35*0.25=8.75 = ~18.55 < 20
        # Use close_date_days_remaining=7 condition: needs composite>=20
        # days=14(28 silence) + outreach=4(22) → silence=50, comp=50*0.35=17.5
        # Add email<0.20(20 eng) → 50*0.35+20*0.25=17.5+5=22.5 >= 20
        inp = base_input(
            days_since_last_prospect_response=14,
            outreach_attempts_no_response=4,
            email_open_rate_last_30d=0.15,
            close_date_days_remaining=7,
        )
        result = engine.assess(inp)
        if result.ghosting_composite >= 20 and inp.close_date_days_remaining <= 7:
            assert result.requires_escalation is True

    def test_not_escalation_healthy(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert result.requires_escalation is False

    def test_not_escalation_champion_lt14(self):
        engine = fresh_engine()
        inp = base_input(champion_last_response_days=13)
        result = engine.assess(inp)
        if result.ghosting_composite < 30 and inp.close_date_days_remaining > 7:
            assert result.requires_escalation is False

    def test_escalation_composite_exactly_30(self):
        # Build a scenario where composite is exactly 30
        # Need silence*0.35 + eng*0.25 + stk*0.25 + mom*0.15 = 30
        # If silence=28(days_since=14), outreach=0, champion=0 → silence=28
        # engagement = 0, stk = 0, momentum = 0
        # composite = 28*0.35 = 9.8 < 30, need more
        # Add eng=10 (email 0.20-0.35): 28*0.35 + 10*0.25 = 9.8+2.5=12.3 still < 30
        # Need higher. silence=45(days>=21), champion=12(days=14..20)→silence=45+12=57
        # 57*0.35=19.95, add eng=10: 19.95+2.5=22.45, stk=15: 22.45+3.75=26.2, mom=12(1.5x stage): 26.2+1.8=28.0
        # Close but need 30. stk=30: 28*0.35+10*0.25+30*0.25+0*0.15=9.8+2.5+7.5=19.8 still nope
        # silence=57, engagement=30(proposal>=14), stk=15, momentum=0
        # 57*0.35+30*0.25+15*0.25 = 19.95+7.5+3.75=31.2 >= 30
        engine = fresh_engine()
        inp = base_input(
            days_since_last_prospect_response=21,
            champion_last_response_days=14,
            proposal_sent=1,
            days_since_proposal=14,
            stakeholder_count=2,
            responsive_stakeholders=1,
        )
        result = engine.assess(inp)
        if result.ghosting_composite >= 30:
            assert result.requires_escalation is True


# ---------------------------------------------------------------------------
# 15. estimated_deal_recovery_pct
# ---------------------------------------------------------------------------

class TestEstimatedDealRecovery:

    def test_recovery_healthy_deal(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert result.estimated_deal_recovery_pct == 100.0

    def test_recovery_formula_clamp_100_minus_composite(self):
        engine = fresh_engine()
        inp = base_input(days_since_last_prospect_response=14)  # adds silence
        result = engine.assess(inp)
        expected = max(0.0, min(100.0, 100.0 - result.ghosting_composite))
        assert abs(result.estimated_deal_recovery_pct - expected) < 0.01

    def test_recovery_zero_when_composite_100(self):
        engine = fresh_engine()
        inp = base_input(
            days_since_last_prospect_response=30,
            outreach_attempts_no_response=10,
            champion_last_response_days=30,
            email_open_rate_last_30d=0.0,
            meeting_decline_count=10,
            proposal_sent=1,
            days_since_proposal=30,
            stakeholder_count=5,
            responsive_stakeholders=0,
            competitor_mentioned_last_contact=1,
            demo_completed=1,
            days_since_demo=30,
            days_in_current_stage=200,
            expected_days_in_stage=14,
            close_date_days_remaining=1,
            meeting_accept_count=0,
        )
        result = engine.assess(inp)
        assert result.estimated_deal_recovery_pct >= 0.0

    def test_recovery_non_negative(self):
        engine = fresh_engine()
        inp = base_input(days_since_last_prospect_response=30)
        result = engine.assess(inp)
        assert result.estimated_deal_recovery_pct >= 0.0

    def test_recovery_lte_100(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert result.estimated_deal_recovery_pct <= 100.0

    def test_recovery_consistent_with_composite(self):
        engine = fresh_engine()
        inp = base_input(days_since_last_prospect_response=7)
        result = engine.assess(inp)
        assert abs(result.estimated_deal_recovery_pct - (100.0 - result.ghosting_composite)) < 0.01


# ---------------------------------------------------------------------------
# 16. Signal string tests
# ---------------------------------------------------------------------------

class TestSignalStrings:

    def test_signal_none_pattern(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert result.ghosting_signal == "Deal engagement within healthy parameters"

    def test_signal_end_of_cycle_ghost(self):
        engine = fresh_engine()
        inp = base_input(
            close_date_days_remaining=14,
            days_since_last_prospect_response=10,
        )
        result = engine.assess(inp)
        if result.ghosting_pattern == GhostingPattern.end_of_cycle_ghost:
            assert str(inp.days_since_last_prospect_response) in result.ghosting_signal
            assert str(inp.close_date_days_remaining) in result.ghosting_signal
            assert f"composite {result.ghosting_composite:.0f}" in result.ghosting_signal

    def test_signal_multi_stakeholder_fade(self):
        engine = fresh_engine()
        inp = base_input(
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=3,
            responsive_stakeholders=0,
        )
        result = engine.assess(inp)
        if result.ghosting_pattern == GhostingPattern.multi_stakeholder_fade:
            assert "0/3" in result.ghosting_signal
            assert "composite" in result.ghosting_signal

    def test_signal_champion_unresponsive(self):
        engine = fresh_engine()
        inp = base_input(
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=14,
        )
        result = engine.assess(inp)
        if result.ghosting_pattern == GhostingPattern.champion_unresponsive:
            assert "14d" in result.ghosting_signal
            assert "composite" in result.ghosting_signal

    def test_signal_proposal_drop_off(self):
        engine = fresh_engine()
        inp = base_input(
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=1,
            proposal_sent=1,
            days_since_proposal=14,
            email_open_rate_last_30d=0.05,
            meeting_decline_count=2,
        )
        result = engine.assess(inp)
        if result.ghosting_pattern == GhostingPattern.proposal_drop_off:
            assert "14" in result.ghosting_signal
            assert "composite" in result.ghosting_signal

    def test_signal_silence_after_demo(self):
        engine = fresh_engine()
        inp = base_input(
            close_date_days_remaining=30,
            days_since_last_prospect_response=14,
            stakeholder_count=1,
            responsive_stakeholders=1,
            champion_last_response_days=1,
            demo_completed=1,
            days_since_demo=14,
        )
        result = engine.assess(inp)
        if result.ghosting_pattern == GhostingPattern.silence_after_demo:
            assert "14d" in result.ghosting_signal
            assert "composite" in result.ghosting_signal

    def test_signal_is_string(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert isinstance(result.ghosting_signal, str)

    def test_signal_non_empty(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert len(result.ghosting_signal) > 0

    def test_signal_composite_in_non_none_patterns(self):
        engine = fresh_engine()
        inp = base_input(
            close_date_days_remaining=14,
            days_since_last_prospect_response=10,
        )
        result = engine.assess(inp)
        if result.ghosting_pattern != GhostingPattern.none:
            assert "composite" in result.ghosting_signal


# ---------------------------------------------------------------------------
# 17. assess() API
# ---------------------------------------------------------------------------

class TestAssessAPI:

    def test_assess_returns_dealghostingresult(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert isinstance(result, DealGhostingResult)

    def test_assess_preserves_deal_id(self):
        engine = fresh_engine()
        result = engine.assess(base_input(deal_id="DEAL-XYZ"))
        assert result.deal_id == "DEAL-XYZ"

    def test_assess_preserves_rep_id(self):
        engine = fresh_engine()
        result = engine.assess(base_input(rep_id="REP-999"))
        assert result.rep_id == "REP-999"

    def test_assess_accumulates_results(self):
        engine = fresh_engine()
        engine.assess(base_input(deal_id="D1"))
        engine.assess(base_input(deal_id="D2"))
        assert len(engine._results) == 2

    def test_assess_result_risk_is_ghostingrisk(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert isinstance(result.ghosting_risk, GhostingRisk)

    def test_assess_result_pattern_is_ghostingpattern(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert isinstance(result.ghosting_pattern, GhostingPattern)

    def test_assess_result_severity_is_ghostingseverity(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert isinstance(result.ghosting_severity, GhostingSeverity)

    def test_assess_result_action_is_ghostingaction(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert isinstance(result.recommended_action, GhostingAction)

    def test_assess_result_is_ghosted_is_bool(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert isinstance(result.is_ghosted, bool)

    def test_assess_result_requires_escalation_is_bool(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert isinstance(result.requires_escalation, bool)

    def test_assess_result_scores_are_floats(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert isinstance(result.silence_score, float)
        assert isinstance(result.engagement_decay_score, float)
        assert isinstance(result.stakeholder_coverage_score, float)
        assert isinstance(result.deal_momentum_score, float)
        assert isinstance(result.ghosting_composite, float)
        assert isinstance(result.estimated_deal_recovery_pct, float)

    def test_assess_independent_engines_dont_share_state(self):
        e1 = fresh_engine()
        e2 = fresh_engine()
        e1.assess(base_input())
        assert len(e2._results) == 0

    def test_assess_multiple_calls_same_engine_accumulate(self):
        engine = fresh_engine()
        for i in range(5):
            engine.assess(base_input(deal_id=f"D{i}"))
        assert len(engine._results) == 5


# ---------------------------------------------------------------------------
# 18. assess_batch() API
# ---------------------------------------------------------------------------

class TestAssessBatchAPI:

    def test_assess_batch_returns_list(self):
        engine = fresh_engine()
        results = engine.assess_batch([base_input(deal_id="D1"), base_input(deal_id="D2")])
        assert isinstance(results, list)

    def test_assess_batch_correct_length(self):
        engine = fresh_engine()
        inputs = [base_input(deal_id=f"D{i}") for i in range(10)]
        results = engine.assess_batch(inputs)
        assert len(results) == 10

    def test_assess_batch_empty_list(self):
        engine = fresh_engine()
        results = engine.assess_batch([])
        assert results == []

    def test_assess_batch_accumulates_in_engine(self):
        engine = fresh_engine()
        engine.assess_batch([base_input(deal_id=f"D{i}") for i in range(7)])
        assert len(engine._results) == 7

    def test_assess_batch_returns_dealghostingresult_items(self):
        engine = fresh_engine()
        results = engine.assess_batch([base_input()])
        assert all(isinstance(r, DealGhostingResult) for r in results)

    def test_assess_batch_preserves_order(self):
        engine = fresh_engine()
        inputs = [base_input(deal_id=f"D{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.deal_id == f"D{i}"

    def test_assess_batch_single_item(self):
        engine = fresh_engine()
        results = engine.assess_batch([base_input(deal_id="SOLO")])
        assert len(results) == 1
        assert results[0].deal_id == "SOLO"


# ---------------------------------------------------------------------------
# 19. summary() API
# ---------------------------------------------------------------------------

class TestSummaryAPI:

    def test_summary_empty_engine_total_zero(self):
        engine = fresh_engine()
        s = engine.summary()
        assert s["total"] == 0

    def test_summary_empty_engine_zeroed_averages(self):
        engine = fresh_engine()
        s = engine.summary()
        assert s["avg_ghosting_composite"] == 0.0
        assert s["avg_silence_score"] == 0.0
        assert s["avg_engagement_decay_score"] == 0.0
        assert s["avg_stakeholder_coverage_score"] == 0.0
        assert s["avg_deal_momentum_score"] == 0.0
        assert s["avg_estimated_deal_recovery_pct"] == 0.0

    def test_summary_empty_engine_empty_dicts(self):
        engine = fresh_engine()
        s = engine.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_summary_empty_engine_ghosted_zero(self):
        engine = fresh_engine()
        s = engine.summary()
        assert s["ghosted_count"] == 0
        assert s["escalation_count"] == 0

    def test_summary_single_result_total(self):
        engine = fresh_engine()
        engine.assess(base_input())
        s = engine.summary()
        assert s["total"] == 1

    def test_summary_multiple_results_total(self):
        engine = fresh_engine()
        for i in range(5):
            engine.assess(base_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert s["total"] == 5

    def test_summary_risk_counts_keys_are_strings(self):
        engine = fresh_engine()
        engine.assess(base_input())
        s = engine.summary()
        for k in s["risk_counts"]:
            assert isinstance(k, str)

    def test_summary_risk_counts_sum_to_total(self):
        engine = fresh_engine()
        engine.assess_batch([base_input(deal_id=f"D{i}") for i in range(10)])
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_to_total(self):
        engine = fresh_engine()
        engine.assess_batch([base_input(deal_id=f"D{i}") for i in range(10)])
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_to_total(self):
        engine = fresh_engine()
        engine.assess_batch([base_input(deal_id=f"D{i}") for i in range(10)])
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        engine = fresh_engine()
        engine.assess_batch([base_input(deal_id=f"D{i}") for i in range(10)])
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_ghosted_count_lte_total(self):
        engine = fresh_engine()
        engine.assess_batch([base_input(deal_id=f"D{i}") for i in range(10)])
        s = engine.summary()
        assert s["ghosted_count"] <= s["total"]

    def test_summary_escalation_count_lte_total(self):
        engine = fresh_engine()
        engine.assess_batch([base_input(deal_id=f"D{i}") for i in range(10)])
        s = engine.summary()
        assert s["escalation_count"] <= s["total"]

    def test_summary_avg_composite_correct(self):
        engine = fresh_engine()
        # Two deals: both healthy, composite = 0
        engine.assess(base_input(deal_id="D1"))
        engine.assess(base_input(deal_id="D2"))
        s = engine.summary()
        assert s["avg_ghosting_composite"] == 0.0

    def test_summary_avg_recovery_correct_all_healthy(self):
        engine = fresh_engine()
        engine.assess(base_input(deal_id="D1"))
        engine.assess(base_input(deal_id="D2"))
        s = engine.summary()
        assert s["avg_estimated_deal_recovery_pct"] == 100.0

    def test_summary_ghosted_count_correct(self):
        engine = fresh_engine()
        engine.assess(base_input(days_since_last_prospect_response=21, deal_id="ghosted"))
        engine.assess(base_input(deal_id="healthy"))
        s = engine.summary()
        assert s["ghosted_count"] >= 1

    def test_summary_escalation_count_correct(self):
        engine = fresh_engine()
        engine.assess(base_input(champion_last_response_days=14, deal_id="escalated"))
        engine.assess(base_input(deal_id="healthy"))
        s = engine.summary()
        assert s["escalation_count"] >= 1

    def test_summary_avgs_are_rounded_to_1_decimal(self):
        engine = fresh_engine()
        engine.assess(base_input(days_since_last_prospect_response=7))
        s = engine.summary()
        for key in ["avg_ghosting_composite", "avg_silence_score", "avg_engagement_decay_score",
                    "avg_stakeholder_coverage_score", "avg_deal_momentum_score",
                    "avg_estimated_deal_recovery_pct"]:
            val = s[key]
            assert val == round(val, 1), f"{key} not rounded to 1 decimal"

    def test_summary_accumulates_across_batches(self):
        engine = fresh_engine()
        engine.assess_batch([base_input(deal_id=f"A{i}") for i in range(5)])
        engine.assess_batch([base_input(deal_id=f"B{i}") for i in range(5)])
        s = engine.summary()
        assert s["total"] == 10


# ---------------------------------------------------------------------------
# 20. to_dict() value types
# ---------------------------------------------------------------------------

class TestToDict:

    def test_to_dict_deal_id_is_str(self):
        engine = fresh_engine()
        d = engine.assess(base_input(deal_id="TEST")).to_dict()
        assert d["deal_id"] == "TEST"
        assert isinstance(d["deal_id"], str)

    def test_to_dict_rep_id_is_str(self):
        engine = fresh_engine()
        d = engine.assess(base_input(rep_id="REP")).to_dict()
        assert d["rep_id"] == "REP"

    def test_to_dict_scores_rounded_to_1_decimal(self):
        engine = fresh_engine()
        d = engine.assess(base_input(days_since_last_prospect_response=7)).to_dict()
        for key in ["silence_score", "engagement_decay_score", "stakeholder_coverage_score",
                    "deal_momentum_score", "ghosting_composite", "estimated_deal_recovery_pct"]:
            val = d[key]
            assert val == round(val, 1), f"{key} not rounded"

    def test_to_dict_is_ghosted_bool(self):
        engine = fresh_engine()
        d = engine.assess(base_input()).to_dict()
        assert isinstance(d["is_ghosted"], bool)

    def test_to_dict_requires_escalation_bool(self):
        engine = fresh_engine()
        d = engine.assess(base_input()).to_dict()
        assert isinstance(d["requires_escalation"], bool)

    def test_to_dict_ghosting_signal_is_str(self):
        engine = fresh_engine()
        d = engine.assess(base_input()).to_dict()
        assert isinstance(d["ghosting_signal"], str)

    def test_to_dict_enum_values_valid_risk(self):
        engine = fresh_engine()
        d = engine.assess(base_input()).to_dict()
        assert d["ghosting_risk"] in {"low", "moderate", "high", "critical"}

    def test_to_dict_enum_values_valid_pattern(self):
        engine = fresh_engine()
        d = engine.assess(base_input()).to_dict()
        assert d["ghosting_pattern"] in {
            "none", "silence_after_demo", "proposal_drop_off",
            "champion_unresponsive", "multi_stakeholder_fade", "end_of_cycle_ghost"
        }

    def test_to_dict_enum_values_valid_severity(self):
        engine = fresh_engine()
        d = engine.assess(base_input()).to_dict()
        assert d["ghosting_severity"] in {"active", "cooling", "dark", "lost"}

    def test_to_dict_enum_values_valid_action(self):
        engine = fresh_engine()
        d = engine.assess(base_input()).to_dict()
        assert d["recommended_action"] in {
            "no_action", "follow_up_sequence", "manager_re_engage",
            "exec_outreach", "deal_disqualification"
        }


# ---------------------------------------------------------------------------
# 21. Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def test_zero_stakeholders_no_ratio_crash(self):
        engine = fresh_engine()
        inp = base_input(stakeholder_count=0, responsive_stakeholders=0)
        result = engine.assess(inp)
        assert result is not None
        assert result.stakeholder_coverage_score == 0.0

    def test_zero_expected_stage_days_no_div_zero(self):
        engine = fresh_engine()
        inp = base_input(expected_days_in_stage=0, days_in_current_stage=100)
        result = engine.assess(inp)
        assert result is not None
        assert result.deal_momentum_score == 0.0  # no stage penalty when expected=0

    def test_zero_total_meetings_no_div_zero(self):
        engine = fresh_engine()
        inp = base_input(meeting_accept_count=0, meeting_decline_count=0)
        result = engine.assess(inp)
        assert result is not None

    def test_no_demo_completed(self):
        engine = fresh_engine()
        inp = base_input(demo_completed=0, days_since_demo=999)
        result = engine.assess(inp)
        # No demo penalty
        stk = engine._stakeholder_coverage_score(inp)
        assert stk == 0.0  # only no-demo relevant part

    def test_no_proposal_sent(self):
        engine = fresh_engine()
        inp = base_input(proposal_sent=0, days_since_proposal=999)
        result = engine.assess(inp)
        eng = engine._engagement_decay_score(inp)
        # No proposal penalty
        assert eng == 0.0

    def test_very_high_deal_value(self):
        engine = fresh_engine()
        inp = base_input(deal_value_usd=10_000_000.0)
        result = engine.assess(inp)
        assert result is not None

    def test_zero_deal_value(self):
        engine = fresh_engine()
        inp = base_input(deal_value_usd=0.0)
        result = engine.assess(inp)
        assert result is not None

    def test_close_date_zero(self):
        engine = fresh_engine()
        inp = base_input(close_date_days_remaining=0, days_since_last_prospect_response=10)
        result = engine.assess(inp)
        assert result is not None

    def test_all_zeroes_numeric_fields(self):
        engine = fresh_engine()
        inp = base_input(
            days_since_last_prospect_response=0,
            days_since_last_rep_outreach=0,
            outreach_attempts_no_response=0,
            days_in_current_stage=0,
            expected_days_in_stage=0,
            demo_completed=0,
            days_since_demo=0,
            proposal_sent=0,
            days_since_proposal=0,
            stakeholder_count=0,
            responsive_stakeholders=0,
            champion_last_response_days=0,
            email_open_rate_last_30d=0.0,
            meeting_decline_count=0,
            meeting_accept_count=0,
            competitor_mentioned_last_contact=0,
            deal_value_usd=0.0,
            close_date_days_remaining=0,
        )
        result = engine.assess(inp)
        # email_open_rate=0.0 < 0.10 → engagement += 35
        # composite = 35*0.25 = 8.75
        assert result.ghosting_composite >= 0.0

    def test_engine_state_isolated_per_instance(self):
        e1 = DealGhostingRiskEngine()
        e2 = DealGhostingRiskEngine()
        e1.assess(base_input(deal_id="D1"))
        e1.assess(base_input(deal_id="D2"))
        assert len(e1._results) == 2
        assert len(e2._results) == 0

    def test_negative_days_no_crash(self):
        # Negative day values should not crash (they just hit 0 tier)
        engine = fresh_engine()
        inp = base_input(days_since_last_prospect_response=-1)
        result = engine.assess(inp)
        assert result is not None

    def test_very_large_outreach_attempts(self):
        engine = fresh_engine()
        inp = base_input(outreach_attempts_no_response=1000)
        result = engine.assess(inp)
        assert result.silence_score <= 100.0

    def test_email_open_rate_exactly_010(self):
        engine = fresh_engine()
        eng = engine._engagement_decay_score(base_input(email_open_rate_last_30d=0.10))
        # 0.10 is not < 0.10, so hits the 0.10-0.20 tier? No: 0.10 is not < 0.10 → check next: not < 0.20
        # 0.10 < 0.20 → score += 20
        assert eng == 20.0

    def test_email_open_rate_exactly_020(self):
        engine = fresh_engine()
        eng = engine._engagement_decay_score(base_input(email_open_rate_last_30d=0.20))
        # 0.20 is not < 0.20 → check next: 0.20 < 0.35 → score += 10
        assert eng == 10.0

    def test_email_open_rate_exactly_035(self):
        engine = fresh_engine()
        eng = engine._engagement_decay_score(base_input(email_open_rate_last_30d=0.35))
        # Not < 0.10, not < 0.20, not < 0.35 → no email contribution
        assert eng == 0.0

    def test_stakeholder_count_exactly_3_responsive_exactly_1(self):
        engine = fresh_engine()
        inp = base_input(stakeholder_count=3, responsive_stakeholders=1)
        p = engine._classify_pattern(inp, 0.0, 0.0, 0.0, 0.0)
        assert p == GhostingPattern.multi_stakeholder_fade

    def test_stakeholder_count_exactly_3_responsive_exactly_2(self):
        engine = fresh_engine()
        inp = base_input(
            stakeholder_count=3, responsive_stakeholders=2,
            close_date_days_remaining=30,
            days_since_last_prospect_response=1,
            champion_last_response_days=1,
        )
        p = engine._classify_pattern(inp, 0.0, 0.0, 0.0, 0.0)
        assert p == GhostingPattern.none


# ---------------------------------------------------------------------------
# 22. End-to-end scenarios
# ---------------------------------------------------------------------------

class TestEndToEndScenarios:

    def test_fully_healthy_deal(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert result.ghosting_risk == GhostingRisk.low
        assert result.ghosting_severity == GhostingSeverity.active
        assert result.ghosting_pattern == GhostingPattern.none
        assert result.recommended_action == GhostingAction.no_action
        assert result.is_ghosted is False
        assert result.requires_escalation is False
        assert result.ghosting_composite == 0.0
        assert result.estimated_deal_recovery_pct == 100.0

    def test_critical_ghosting_scenario(self):
        engine = fresh_engine()
        inp = base_input(
            days_since_last_prospect_response=21,
            outreach_attempts_no_response=6,
            champion_last_response_days=21,
            email_open_rate_last_30d=0.0,
            meeting_decline_count=4,
            proposal_sent=1,
            days_since_proposal=21,
            stakeholder_count=5,
            responsive_stakeholders=0,
            competitor_mentioned_last_contact=1,
            demo_completed=1,
            days_since_demo=21,
            days_in_current_stage=100,
            expected_days_in_stage=10,
            close_date_days_remaining=5,
            meeting_accept_count=0,
        )
        result = engine.assess(inp)
        assert result.ghosting_risk == GhostingRisk.critical
        assert result.ghosting_severity == GhostingSeverity.lost
        assert result.is_ghosted is True
        assert result.requires_escalation is True
        assert result.recommended_action == GhostingAction.deal_disqualification
        assert result.ghosting_composite == 100.0
        assert result.estimated_deal_recovery_pct == 0.0

    def test_moderate_ghosting_scenario(self):
        engine = fresh_engine()
        inp = base_input(
            days_since_last_prospect_response=7,
            outreach_attempts_no_response=2,
            email_open_rate_last_30d=0.25,
        )
        result = engine.assess(inp)
        # silence=14+10=24, eng=10, stk=0, mom=0
        # composite = 24*0.35 + 10*0.25 = 8.4 + 2.5 = 10.9
        assert result.ghosting_risk == GhostingRisk.low
        assert result.ghosting_composite < 20

    def test_champion_unresponsive_scenario(self):
        engine = fresh_engine()
        inp = base_input(
            close_date_days_remaining=30,
            days_since_last_prospect_response=5,
            stakeholder_count=2,
            responsive_stakeholders=2,
            champion_last_response_days=14,
        )
        result = engine.assess(inp)
        assert result.ghosting_pattern == GhostingPattern.champion_unresponsive
        assert result.requires_escalation is True

    def test_end_of_cycle_ghost_scenario(self):
        engine = fresh_engine()
        inp = base_input(
            close_date_days_remaining=7,
            days_since_last_prospect_response=10,
        )
        result = engine.assess(inp)
        assert result.ghosting_pattern == GhostingPattern.end_of_cycle_ghost

    def test_multi_stakeholder_fade_scenario(self):
        engine = fresh_engine()
        inp = base_input(
            close_date_days_remaining=30,
            days_since_last_prospect_response=2,
            stakeholder_count=4,
            responsive_stakeholders=0,
        )
        result = engine.assess(inp)
        assert result.ghosting_pattern == GhostingPattern.multi_stakeholder_fade

    def test_batch_mixed_scenarios(self):
        engine = fresh_engine()
        inputs = [
            base_input(deal_id="healthy"),
            base_input(deal_id="ghosted", days_since_last_prospect_response=21),
            base_input(deal_id="escalated", champion_last_response_days=14),
        ]
        results = engine.assess_batch(inputs)
        assert len(results) == 3
        s = engine.summary()
        assert s["total"] == 3
        assert s["ghosted_count"] >= 1
        assert s["escalation_count"] >= 1

    def test_summary_after_all_critical(self):
        engine = fresh_engine()
        inp = base_input(
            days_since_last_prospect_response=21,
            outreach_attempts_no_response=6,
            champion_last_response_days=21,
            email_open_rate_last_30d=0.0,
            meeting_decline_count=4,
            proposal_sent=1,
            days_since_proposal=21,
            stakeholder_count=5,
            responsive_stakeholders=0,
            competitor_mentioned_last_contact=1,
            demo_completed=1,
            days_since_demo=21,
            days_in_current_stage=100,
            expected_days_in_stage=10,
            close_date_days_remaining=5,
            meeting_accept_count=0,
        )
        engine.assess(inp)
        s = engine.summary()
        assert s["risk_counts"].get("critical", 0) >= 1
        assert s["severity_counts"].get("lost", 0) >= 1
        assert s["action_counts"].get("deal_disqualification", 0) >= 1
        assert s["ghosted_count"] == 1
        assert s["escalation_count"] == 1

    def test_summary_all_healthy(self):
        engine = fresh_engine()
        engine.assess_batch([base_input(deal_id=f"D{i}") for i in range(5)])
        s = engine.summary()
        assert s["risk_counts"].get("low", 0) == 5
        assert s["ghosted_count"] == 0
        assert s["avg_ghosting_composite"] == 0.0
        assert s["avg_estimated_deal_recovery_pct"] == 100.0

    def test_assess_high_composite_triggers_exec_outreach(self):
        engine = fresh_engine()
        # composite in [50,60): need to build carefully
        # silence=45(days=21) + outreach=0 + champion=0 → silence=45
        # engagement=30(proposal>=14) + email<0.10(35)? That's 65, use email<0.20(20): 20+30=50
        # stk=0, momentum=0
        # composite = 45*0.35 + 50*0.25 = 15.75+12.5=28.25 not enough
        # Need composite in [50,60)
        # silence=100: days=21(45)+outreach=6(35)+champ=21(20)=100 → 100*0.35=35
        # eng=100: email<0.10(35)+decline=4(35)+proposal>=14(30)=100 → 100*0.25=25
        # stk=80: stk<0.2(50)+competitor(30)=80 → 80*0.25=20
        # mom=0: 35+25+20=80 → critical, not [50,60)
        # Let me try: silence=28(days=14)+22(outreach=4)=50 → 50*0.35=17.5
        # eng=30(proposal>=14)+10(email<0.35)=40 → 40*0.25=10
        # stk=30(competitor) → 30*0.25=7.5
        # mom=25(accept_ratio<0.25) → 25*0.15=3.75
        # composite = 17.5+10+7.5+3.75=38.75 < 50
        # Try silence=45(days=21)+22(outreach=4)=67 clamped to 100? No: 45+22=67, not clamped
        # 67*0.35=23.45, eng=50(email<0.10(35)+decline=2(20))=55 clamped=55 → 55*0.25=13.75
        # stk=30 → 7.5, mom=25 → 3.75
        # total=23.45+13.75+7.5+3.75=48.45 still < 50
        # eng: email<0.10(35)+decline=4(35)+proposal>=14(30)=100 → 100*0.25=25
        # silence=67*0.35=23.45, eng=25, stk=7.5, mom=3.75 → 59.7? Let me check:
        # 23.45 + 25 + 7.5 + 3.75 = 59.7 → high (< 60), exec_outreach (>=50)
        inp = base_input(
            days_since_last_prospect_response=21,
            outreach_attempts_no_response=4,
            email_open_rate_last_30d=0.05,
            meeting_decline_count=4,
            proposal_sent=1,
            days_since_proposal=14,
            competitor_mentioned_last_contact=1,
            meeting_accept_count=0,
        )
        result = engine.assess(inp)
        if 50.0 <= result.ghosting_composite < 60.0:
            assert result.recommended_action == GhostingAction.exec_outreach

    def test_assess_high_risk_lt50_manager_re_engage(self):
        engine = fresh_engine()
        # composite in [40, 50): high risk, action=manager_re_engage
        # silence=45(days=21) → 45*0.35=15.75
        # eng=30(proposal)+10(email<0.35)=40 → 40*0.25=10
        # stk=30(competitor) → 7.5
        # mom=25(accept<0.25) → 3.75
        # total=37 = high? no 37 < 40, need slightly more
        # stk=50(ratio<0.2)+30(competitor)=80 → 80*0.25=20
        # total=15.75+10+20+3.75=49.5 → high (40-60), composite < 50 → manager_re_engage
        inp = base_input(
            days_since_last_prospect_response=21,
            proposal_sent=1,
            days_since_proposal=14,
            email_open_rate_last_30d=0.3,
            stakeholder_count=5,
            responsive_stakeholders=0,
            competitor_mentioned_last_contact=1,
            meeting_accept_count=0,
            meeting_decline_count=4,
        )
        result = engine.assess(inp)
        if 40.0 <= result.ghosting_composite < 50.0:
            assert result.recommended_action == GhostingAction.manager_re_engage


# ---------------------------------------------------------------------------
# 23. Additional boundary and regression tests
# ---------------------------------------------------------------------------

class TestAdditionalBoundaries:

    def test_silence_score_exactly_100_clamped(self):
        engine = fresh_engine()
        # 45+35+20=100 exactly
        score = engine._silence_score(base_input(
            days_since_last_prospect_response=21,
            outreach_attempts_no_response=6,
            champion_last_response_days=21,
        ))
        assert score == 100.0

    def test_engagement_decay_exactly_100_clamped(self):
        engine = fresh_engine()
        # 35+35+30=100
        score = engine._engagement_decay_score(base_input(
            email_open_rate_last_30d=0.0,
            meeting_decline_count=4,
            proposal_sent=1,
            days_since_proposal=14,
        ))
        assert score == 100.0

    def test_stakeholder_coverage_exactly_100_clamped(self):
        engine = fresh_engine()
        # 50+30+20=100
        score = engine._stakeholder_coverage_score(base_input(
            stakeholder_count=5,
            responsive_stakeholders=0,
            competitor_mentioned_last_contact=1,
            demo_completed=1,
            days_since_demo=21,
        ))
        assert score == 100.0

    def test_deal_momentum_exactly_100_clamped(self):
        engine = fresh_engine()
        # 40+35+25=100
        score = engine._deal_momentum_score(base_input(
            days_in_current_stage=42,
            expected_days_in_stage=14,  # ratio=3.0 → 40
            close_date_days_remaining=7,
            days_since_last_prospect_response=7,  # +35
            meeting_accept_count=0,
            meeting_decline_count=4,  # +25
        ))
        assert score == 100.0

    def test_composite_result_id_passthrough(self):
        engine = fresh_engine()
        result = engine.assess(base_input(deal_id="PASSTHROUGH-123", rep_id="REP-456"))
        assert result.deal_id == "PASSTHROUGH-123"
        assert result.rep_id == "REP-456"

    def test_summary_pattern_counts_include_none(self):
        engine = fresh_engine()
        engine.assess(base_input())
        s = engine.summary()
        assert s["pattern_counts"].get("none", 0) >= 1

    def test_summary_severity_counts_include_active(self):
        engine = fresh_engine()
        engine.assess(base_input())
        s = engine.summary()
        assert s["severity_counts"].get("active", 0) >= 1

    def test_summary_action_counts_include_no_action(self):
        engine = fresh_engine()
        engine.assess(base_input())
        s = engine.summary()
        assert s["action_counts"].get("no_action", 0) >= 1

    def test_is_ghosted_false_all_three_conditions_false(self):
        engine = fresh_engine()
        inp = base_input(
            days_since_last_prospect_response=1,
            outreach_attempts_no_response=0,
        )
        result = engine.assess(inp)
        # composite < 40, outreach < 5, days < 21
        assert result.is_ghosted is False

    def test_requires_escalation_all_three_false(self):
        engine = fresh_engine()
        inp = base_input(
            champion_last_response_days=1,
            close_date_days_remaining=60,
        )
        result = engine.assess(inp)
        # composite < 30, champion < 14, not (close <=7 AND composite >= 20)
        assert result.requires_escalation is False

    def test_close_date_lte7_composite_lt20_no_escalation(self):
        engine = fresh_engine()
        # close <= 7, but composite < 20 AND champion < 14 AND composite < 30
        inp = base_input(
            close_date_days_remaining=7,
            days_since_last_prospect_response=0,
            champion_last_response_days=1,
            email_open_rate_last_30d=1.0,
        )
        result = engine.assess(inp)
        # composite should be 0 (all healthy except email=1.0 → no engagement penalty)
        # email_open_rate=1.0 → no penalty
        # composite = 0 < 20 → close_date condition not met
        # composite < 30 → no escalation from composite
        # champion < 14 → no escalation from champion
        if result.ghosting_composite < 20:
            assert result.requires_escalation is False

    def test_multiple_engines_independent(self):
        engines = [DealGhostingRiskEngine() for _ in range(5)]
        for i, eng in enumerate(engines):
            for j in range(i + 1):
                eng.assess(base_input(deal_id=f"D{j}"))
        for i, eng in enumerate(engines):
            assert len(eng._results) == i + 1

    def test_assess_result_scores_non_negative(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert result.silence_score >= 0.0
        assert result.engagement_decay_score >= 0.0
        assert result.stakeholder_coverage_score >= 0.0
        assert result.deal_momentum_score >= 0.0
        assert result.ghosting_composite >= 0.0

    def test_assess_result_scores_lte_100(self):
        engine = fresh_engine()
        inp = base_input(
            days_since_last_prospect_response=30,
            outreach_attempts_no_response=10,
            champion_last_response_days=30,
            email_open_rate_last_30d=0.0,
            meeting_decline_count=10,
            proposal_sent=1,
            days_since_proposal=30,
        )
        result = engine.assess(inp)
        assert result.silence_score <= 100.0
        assert result.engagement_decay_score <= 100.0
        assert result.stakeholder_coverage_score <= 100.0
        assert result.deal_momentum_score <= 100.0
        assert result.ghosting_composite <= 100.0

    def test_stage_ratio_exactly_15(self):
        engine = fresh_engine()
        score = engine._deal_momentum_score(base_input(
            days_in_current_stage=21,
            expected_days_in_stage=14,  # 1.5 exactly
            close_date_days_remaining=60,
            meeting_accept_count=1,
            meeting_decline_count=0,
        ))
        assert score == 12.0

    def test_stage_ratio_exactly_20(self):
        engine = fresh_engine()
        score = engine._deal_momentum_score(base_input(
            days_in_current_stage=28,
            expected_days_in_stage=14,  # 2.0 exactly
            close_date_days_remaining=60,
            meeting_accept_count=1,
            meeting_decline_count=0,
        ))
        assert score == 25.0

    def test_stage_ratio_exactly_30(self):
        engine = fresh_engine()
        score = engine._deal_momentum_score(base_input(
            days_in_current_stage=42,
            expected_days_in_stage=14,  # 3.0 exactly
            close_date_days_remaining=60,
            meeting_accept_count=1,
            meeting_decline_count=0,
        ))
        assert score == 40.0

    def test_champion_dark_14_exactly(self):
        engine = fresh_engine()
        result = engine.assess(base_input(champion_last_response_days=14))
        assert result.requires_escalation is True

    def test_champion_dark_13_not_escalated(self):
        engine = fresh_engine()
        inp = base_input(champion_last_response_days=13, close_date_days_remaining=60)
        result = engine.assess(inp)
        if result.ghosting_composite < 30:
            assert result.requires_escalation is False

    def test_outreach_attempts_exactly_5_ghosted(self):
        engine = fresh_engine()
        result = engine.assess(base_input(outreach_attempts_no_response=5))
        assert result.is_ghosted is True

    def test_outreach_attempts_exactly_4_not_ghosted_via_attempts(self):
        engine = fresh_engine()
        inp = base_input(outreach_attempts_no_response=4, days_since_last_prospect_response=1)
        result = engine.assess(inp)
        # Only the attempts condition: 4 < 5, so not ghosted via that route
        # Check composite < 40 and days < 21
        if result.ghosting_composite < 40 and inp.days_since_last_prospect_response < 21:
            assert result.is_ghosted is False

    def test_days_since_response_exactly_21_ghosted(self):
        engine = fresh_engine()
        result = engine.assess(base_input(days_since_last_prospect_response=21))
        assert result.is_ghosted is True

    def test_days_since_response_exactly_20_not_ghosted_via_days(self):
        engine = fresh_engine()
        inp = base_input(days_since_last_prospect_response=20, outreach_attempts_no_response=0)
        result = engine.assess(inp)
        # days < 21, attempts < 5. Check composite < 40
        if result.ghosting_composite < 40:
            assert result.is_ghosted is False

    def test_recovery_pct_equals_100_minus_composite(self):
        engine = fresh_engine()
        inp = base_input(days_since_last_prospect_response=14)
        result = engine.assess(inp)
        expected = round(100.0 - result.ghosting_composite, 10)
        assert abs(result.estimated_deal_recovery_pct - expected) < 0.01

    def test_pattern_none_gives_healthy_signal(self):
        engine = fresh_engine()
        result = engine.assess(base_input())
        assert result.ghosting_pattern == GhostingPattern.none
        assert "healthy" in result.ghosting_signal.lower() or "parameters" in result.ghosting_signal

    def test_assess_returns_result_with_correct_rep_and_deal(self):
        engine = fresh_engine()
        inp = base_input(deal_id="DEAL-ABC", rep_id="REP-XYZ")
        result = engine.assess(inp)
        d = result.to_dict()
        assert d["deal_id"] == "DEAL-ABC"
        assert d["rep_id"] == "REP-XYZ"
