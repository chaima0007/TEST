"""
Comprehensive pytest test suite for SalesProposalConversionIntelligenceEngine.
~300 tests covering all enums, sub-scores, pattern detection, risk/severity/action,
flags, revenue calculation, signal string, to_dict, summary, and batch assess.
"""
import pytest
from swarm.intelligence.sales_proposal_conversion_intelligence_engine import (
    SalesProposalConversionIntelligenceEngine,
    ProposalConversionInput,
    ProposalConversionResult,
    ProposalRisk,
    ProposalPattern,
    ProposalSeverity,
    ProposalAction,
)


# ---------------------------------------------------------------------------
# Helper fixture
# ---------------------------------------------------------------------------

def make_input(**kwargs):
    defaults = dict(
        rep_id="rep_test",
        region="West",
        evaluation_period_id="Q1-2026",
        proposals_sent_count=10,
        proposals_won_count=5,
        proposals_lost_count=3,
        proposals_pending_count=2,
        avg_proposal_size_usd=50_000.0,
        avg_days_proposal_to_decision=30.0,
        proposals_stale_count=0,
        proposal_revision_avg_count=1.0,
        proposals_lost_to_price_count=0,
        proposals_lost_to_competitor_count=0,
        proposals_lost_no_decision_count=1,
        executive_sponsor_rate_pct=0.60,
        value_prop_alignment_score=0.75,
        avg_discount_pct=8.0,
        discount_applied_count=2,
        competitive_deals_pct=0.25,
        prior_period_win_rate_pct=0.50,
        current_period_win_rate_pct=0.50,
        multi_stakeholder_proposals_pct=0.65,
    )
    defaults.update(kwargs)
    return ProposalConversionInput(**defaults)


@pytest.fixture
def engine():
    return SalesProposalConversionIntelligenceEngine()


# ===========================================================================
# 1. ENUM VALUES
# ===========================================================================

class TestProposalRiskEnum:
    def test_low_value(self):
        assert ProposalRisk.low.value == "low"

    def test_moderate_value(self):
        assert ProposalRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert ProposalRisk.high.value == "high"

    def test_critical_value(self):
        assert ProposalRisk.critical.value == "critical"

    def test_all_members(self):
        members = {m.value for m in ProposalRisk}
        assert members == {"low", "moderate", "high", "critical"}

    def test_is_str(self):
        assert isinstance(ProposalRisk.low, str)

    def test_str_comparison(self):
        assert ProposalRisk.high == "high"


class TestProposalPatternEnum:
    def test_none_value(self):
        assert ProposalPattern.none.value == "none"

    def test_poor_win_rate_value(self):
        assert ProposalPattern.poor_win_rate.value == "poor_win_rate"

    def test_proposal_staleness_value(self):
        assert ProposalPattern.proposal_staleness.value == "proposal_staleness"

    def test_value_misalignment_value(self):
        assert ProposalPattern.value_misalignment.value == "value_misalignment"

    def test_competitive_loss_value(self):
        assert ProposalPattern.competitive_loss.value == "competitive_loss"

    def test_budget_friction_value(self):
        assert ProposalPattern.budget_friction.value == "budget_friction"

    def test_all_members(self):
        members = {m.value for m in ProposalPattern}
        assert members == {
            "none", "poor_win_rate", "proposal_staleness",
            "value_misalignment", "competitive_loss", "budget_friction",
        }

    def test_is_str(self):
        assert isinstance(ProposalPattern.competitive_loss, str)


class TestProposalSeverityEnum:
    def test_healthy_value(self):
        assert ProposalSeverity.healthy.value == "healthy"

    def test_declining_value(self):
        assert ProposalSeverity.declining.value == "declining"

    def test_stalled_value(self):
        assert ProposalSeverity.stalled.value == "stalled"

    def test_critical_value(self):
        assert ProposalSeverity.critical.value == "critical"

    def test_all_members(self):
        members = {m.value for m in ProposalSeverity}
        assert members == {"healthy", "declining", "stalled", "critical"}

    def test_is_str(self):
        assert isinstance(ProposalSeverity.stalled, str)


class TestProposalActionEnum:
    def test_no_action_value(self):
        assert ProposalAction.no_action.value == "no_action"

    def test_proposal_coaching_value(self):
        assert ProposalAction.proposal_coaching.value == "proposal_coaching"

    def test_value_messaging_update_value(self):
        assert ProposalAction.value_messaging_update.value == "value_messaging_update"

    def test_competitive_repositioning_value(self):
        assert ProposalAction.competitive_repositioning.value == "competitive_repositioning"

    def test_pricing_optimization_value(self):
        assert ProposalAction.pricing_optimization.value == "pricing_optimization"

    def test_executive_escalation_value(self):
        assert ProposalAction.executive_escalation.value == "executive_escalation"

    def test_all_members(self):
        members = {m.value for m in ProposalAction}
        assert members == {
            "no_action", "proposal_coaching", "value_messaging_update",
            "competitive_repositioning", "pricing_optimization", "executive_escalation",
        }

    def test_is_str(self):
        assert isinstance(ProposalAction.no_action, str)


# ===========================================================================
# 2. SUB-SCORE: _proposal_win_rate_score
# ===========================================================================

class TestProposalWinRateScore:
    def test_zero_proposals_no_crash(self, engine):
        inp = make_input(proposals_won_count=0, proposals_lost_count=0,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert 0.0 <= score <= 100.0

    def test_perfect_win_rate_zero_delta_zero_no_decision(self, engine):
        # win_rate=1.0 (none of the <0.15, <0.25, <0.40 bands), delta=0, no_decision=0
        inp = make_input(proposals_won_count=10, proposals_lost_count=0,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert score == 0.0

    def test_win_rate_below_15_adds_40(self, engine):
        # won=1, lost=9 => 10% win rate < 0.15
        inp = make_input(proposals_won_count=1, proposals_lost_count=9,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert score >= 40.0

    def test_win_rate_below_25_adds_25(self, engine):
        # won=2, lost=9 => ~18.2% win rate (0.15 <= x < 0.25)
        inp = make_input(proposals_won_count=2, proposals_lost_count=9,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert score >= 25.0

    def test_win_rate_below_40_adds_10(self, engine):
        # won=3, lost=9 => 25% win rate (0.25 <= x < 0.40)
        inp = make_input(proposals_won_count=3, proposals_lost_count=9,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert score >= 10.0

    def test_win_rate_at_40_no_band_added(self, engine):
        # won=4, lost=6 => 40% win rate (not < 0.40 so no band)
        inp = make_input(proposals_won_count=4, proposals_lost_count=6,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert score == 0.0

    def test_delta_below_minus_10_adds_30(self, engine):
        # delta = 0.20 - 0.35 = -0.15 < -0.10 => +30
        inp = make_input(proposals_won_count=10, proposals_lost_count=0,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.20,
                         prior_period_win_rate_pct=0.35)
        score = engine._proposal_win_rate_score(inp)
        assert score >= 30.0

    def test_delta_between_minus_10_and_minus_5_adds_15(self, engine):
        # delta = 0.40 - 0.47 = -0.07 => -0.10 < delta < -0.05 => +15
        inp = make_input(proposals_won_count=10, proposals_lost_count=0,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.40,
                         prior_period_win_rate_pct=0.47)
        score = engine._proposal_win_rate_score(inp)
        assert score >= 15.0

    def test_delta_between_minus_5_and_zero_adds_8(self, engine):
        # delta = 0.48 - 0.50 = -0.02 => -0.05 < delta < 0 => +8
        inp = make_input(proposals_won_count=10, proposals_lost_count=0,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.48,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert score >= 8.0

    def test_delta_positive_no_delta_penalty(self, engine):
        inp = make_input(proposals_won_count=10, proposals_lost_count=0,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.55,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert score == 0.0

    def test_no_decision_1_adds_5(self, engine):
        inp = make_input(proposals_won_count=10, proposals_lost_count=0,
                         proposals_lost_no_decision_count=1,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert score >= 5.0

    def test_no_decision_2_adds_10(self, engine):
        inp = make_input(proposals_won_count=10, proposals_lost_count=0,
                         proposals_lost_no_decision_count=2,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert score >= 10.0

    def test_no_decision_3_adds_20(self, engine):
        inp = make_input(proposals_won_count=10, proposals_lost_count=0,
                         proposals_lost_no_decision_count=3,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert score >= 20.0

    def test_no_decision_at_2_boundary(self, engine):
        # exactly 2 => +10 (not >=3 branch)
        inp = make_input(proposals_won_count=10, proposals_lost_count=0,
                         proposals_lost_no_decision_count=2,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert score == 10.0

    def test_capped_at_100(self, engine):
        # Max possible: 40 + 30 + 20 = 90 ... add more to push over
        inp = make_input(proposals_won_count=0, proposals_lost_count=10,
                         proposals_lost_no_decision_count=5,
                         current_period_win_rate_pct=0.10,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert score <= 100.0

    def test_score_is_float(self, engine):
        inp = make_input()
        score = engine._proposal_win_rate_score(inp)
        assert isinstance(score, float)

    def test_exactly_15_percent_win_rate(self, engine):
        # won=3, lost=17 => 15% => NOT < 0.15 so no 40 penalty
        inp = make_input(proposals_won_count=3, proposals_lost_count=17,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        # 15% is not < 0.15 so only gets +25 (< 0.25)
        assert score == 25.0

    def test_exactly_25_percent_win_rate(self, engine):
        # won=1, lost=3 => 25% => not < 0.25
        inp = make_input(proposals_won_count=1, proposals_lost_count=3,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        # 25% is >= 0.25 but < 0.40 => +10
        assert score == 10.0

    def test_delta_exactly_minus_10(self, engine):
        # delta = -0.10, NOT < -0.10, but < -0.05 => +15
        inp = make_input(proposals_won_count=10, proposals_lost_count=0,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.40,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert score == 15.0

    def test_delta_exactly_minus_05(self, engine):
        # delta = -0.05, NOT < -0.05, but < 0 => +8
        inp = make_input(proposals_won_count=10, proposals_lost_count=0,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.45,
                         prior_period_win_rate_pct=0.50)
        score = engine._proposal_win_rate_score(inp)
        assert score == 8.0


# ===========================================================================
# 3. SUB-SCORE: _proposal_velocity_score
# ===========================================================================

class TestProposalVelocityScore:
    def test_zero_everything(self, engine):
        inp = make_input(avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=0.0)
        score = engine._proposal_velocity_score(inp)
        assert score == 0.0

    def test_days_below_30_no_penalty(self, engine):
        inp = make_input(avg_days_proposal_to_decision=29.9,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=0.0)
        score = engine._proposal_velocity_score(inp)
        assert score == 0.0

    def test_days_at_30_adds_8(self, engine):
        inp = make_input(avg_days_proposal_to_decision=30.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=0.0)
        score = engine._proposal_velocity_score(inp)
        assert score == 8.0

    def test_days_at_60_adds_20(self, engine):
        inp = make_input(avg_days_proposal_to_decision=60.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=0.0)
        score = engine._proposal_velocity_score(inp)
        assert score == 20.0

    def test_days_at_90_adds_35(self, engine):
        inp = make_input(avg_days_proposal_to_decision=90.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=0.0)
        score = engine._proposal_velocity_score(inp)
        assert score == 35.0

    def test_days_above_90_adds_35(self, engine):
        inp = make_input(avg_days_proposal_to_decision=120.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=0.0)
        score = engine._proposal_velocity_score(inp)
        assert score == 35.0

    def test_stale_0_no_penalty(self, engine):
        inp = make_input(avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=0.0)
        assert engine._proposal_velocity_score(inp) == 0.0

    def test_stale_1_adds_8(self, engine):
        inp = make_input(avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=1,
                         proposal_revision_avg_count=0.0)
        assert engine._proposal_velocity_score(inp) == 8.0

    def test_stale_2_adds_18(self, engine):
        inp = make_input(avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=2,
                         proposal_revision_avg_count=0.0)
        assert engine._proposal_velocity_score(inp) == 18.0

    def test_stale_3_adds_18(self, engine):
        # 3 is >=2 but not >=4 => +18
        inp = make_input(avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=3,
                         proposal_revision_avg_count=0.0)
        assert engine._proposal_velocity_score(inp) == 18.0

    def test_stale_4_adds_30(self, engine):
        inp = make_input(avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=4,
                         proposal_revision_avg_count=0.0)
        assert engine._proposal_velocity_score(inp) == 30.0

    def test_revision_below_15_no_penalty(self, engine):
        inp = make_input(avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=1.4)
        assert engine._proposal_velocity_score(inp) == 0.0

    def test_revision_at_15_adds_5(self, engine):
        inp = make_input(avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=1.5)
        assert engine._proposal_velocity_score(inp) == 5.0

    def test_revision_at_25_adds_10(self, engine):
        inp = make_input(avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=2.5)
        assert engine._proposal_velocity_score(inp) == 10.0

    def test_revision_at_4_adds_20(self, engine):
        inp = make_input(avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=4.0)
        assert engine._proposal_velocity_score(inp) == 20.0

    def test_capped_at_100(self, engine):
        inp = make_input(avg_days_proposal_to_decision=120.0,
                         proposals_stale_count=10,
                         proposal_revision_avg_count=10.0)
        score = engine._proposal_velocity_score(inp)
        assert score <= 100.0

    def test_score_is_float(self, engine):
        inp = make_input()
        score = engine._proposal_velocity_score(inp)
        assert isinstance(score, float)

    def test_combined_all_high(self, engine):
        inp = make_input(avg_days_proposal_to_decision=100.0,
                         proposals_stale_count=5,
                         proposal_revision_avg_count=5.0)
        # 35 + 30 + 20 = 85
        assert engine._proposal_velocity_score(inp) == 85.0


# ===========================================================================
# 4. SUB-SCORE: _value_alignment_score
# ===========================================================================

class TestValueAlignmentScore:
    def test_all_good_no_penalty(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=5.0)
        assert engine._value_alignment_score(inp) == 0.0

    def test_value_prop_below_35_adds_40(self, engine):
        inp = make_input(value_prop_alignment_score=0.30,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=5.0)
        assert engine._value_alignment_score(inp) >= 40.0

    def test_value_prop_at_35_uses_25_band(self, engine):
        # 0.35 is NOT < 0.35, goes to < 0.55 band => +25
        inp = make_input(value_prop_alignment_score=0.35,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=5.0)
        assert engine._value_alignment_score(inp) == 25.0

    def test_value_prop_below_55_adds_25(self, engine):
        inp = make_input(value_prop_alignment_score=0.45,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=5.0)
        assert engine._value_alignment_score(inp) == 25.0

    def test_value_prop_below_70_adds_10(self, engine):
        inp = make_input(value_prop_alignment_score=0.60,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=5.0)
        assert engine._value_alignment_score(inp) == 10.0

    def test_value_prop_at_70_no_penalty(self, engine):
        inp = make_input(value_prop_alignment_score=0.70,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=5.0)
        assert engine._value_alignment_score(inp) == 0.0

    def test_exec_sponsor_below_25_adds_30(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.20,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=5.0)
        assert engine._value_alignment_score(inp) == 30.0

    def test_exec_sponsor_at_25_uses_15_band(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.25,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=5.0)
        assert engine._value_alignment_score(inp) == 15.0

    def test_exec_sponsor_below_45_adds_15(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.35,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=5.0)
        assert engine._value_alignment_score(inp) == 15.0

    def test_exec_sponsor_at_45_no_penalty(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.45,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=5.0)
        assert engine._value_alignment_score(inp) == 0.0

    def test_multi_stakeholder_below_30_adds_20(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.20,
                         avg_discount_pct=5.0)
        assert engine._value_alignment_score(inp) == 20.0

    def test_multi_stakeholder_at_30_uses_10_band(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.30,
                         avg_discount_pct=5.0)
        assert engine._value_alignment_score(inp) == 10.0

    def test_multi_stakeholder_below_50_adds_10(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.40,
                         avg_discount_pct=5.0)
        assert engine._value_alignment_score(inp) == 10.0

    def test_multi_stakeholder_at_50_no_penalty(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.50,
                         avg_discount_pct=5.0)
        assert engine._value_alignment_score(inp) == 0.0

    def test_discount_at_15_adds_8(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=15.0)
        assert engine._value_alignment_score(inp) == 8.0

    def test_discount_at_25_adds_15(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=25.0)
        assert engine._value_alignment_score(inp) == 15.0

    def test_discount_below_15_no_penalty(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=14.9)
        assert engine._value_alignment_score(inp) == 0.0

    def test_capped_at_100(self, engine):
        inp = make_input(value_prop_alignment_score=0.10,
                         executive_sponsor_rate_pct=0.10,
                         multi_stakeholder_proposals_pct=0.10,
                         avg_discount_pct=30.0)
        # 40 + 30 + 20 + 15 = 105 => capped
        assert engine._value_alignment_score(inp) == 100.0

    def test_score_is_float(self, engine):
        inp = make_input()
        assert isinstance(engine._value_alignment_score(inp), float)


# ===========================================================================
# 5. SUB-SCORE: _competitive_exposure_score
# ===========================================================================

class TestCompetitiveExposureScore:
    def test_all_zero(self, engine):
        inp = make_input(competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=0,
                         proposals_lost_count=0,
                         discount_applied_count=0)
        assert engine._competitive_exposure_score(inp) == 0.0

    def test_competitive_deals_below_20_no_penalty(self, engine):
        inp = make_input(competitive_deals_pct=0.10,
                         proposals_lost_to_competitor_count=0,
                         proposals_lost_count=0,
                         discount_applied_count=0)
        assert engine._competitive_exposure_score(inp) == 0.0

    def test_competitive_deals_at_20_adds_8(self, engine):
        inp = make_input(competitive_deals_pct=0.20,
                         proposals_lost_to_competitor_count=0,
                         proposals_lost_count=0,
                         discount_applied_count=0)
        assert engine._competitive_exposure_score(inp) == 8.0

    def test_competitive_deals_at_40_adds_20(self, engine):
        inp = make_input(competitive_deals_pct=0.40,
                         proposals_lost_to_competitor_count=0,
                         proposals_lost_count=0,
                         discount_applied_count=0)
        assert engine._competitive_exposure_score(inp) == 20.0

    def test_competitive_deals_at_60_adds_35(self, engine):
        inp = make_input(competitive_deals_pct=0.60,
                         proposals_lost_to_competitor_count=0,
                         proposals_lost_count=0,
                         discount_applied_count=0)
        assert engine._competitive_exposure_score(inp) == 35.0

    def test_competitive_deals_above_60_adds_35(self, engine):
        inp = make_input(competitive_deals_pct=0.80,
                         proposals_lost_to_competitor_count=0,
                         proposals_lost_count=0,
                         discount_applied_count=0)
        assert engine._competitive_exposure_score(inp) == 35.0

    def test_competitor_lost_0_no_penalty(self, engine):
        inp = make_input(competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=0,
                         proposals_lost_count=0,
                         discount_applied_count=0)
        assert engine._competitive_exposure_score(inp) == 0.0

    def test_competitor_lost_1_adds_10(self, engine):
        inp = make_input(competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=1,
                         proposals_lost_count=5,
                         discount_applied_count=0)
        # 10 (count) + comp_loss_rate = 1/5=20% (< 0.40) => no extra
        assert engine._competitive_exposure_score(inp) == 10.0

    def test_competitor_lost_2_adds_20(self, engine):
        inp = make_input(competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=2,
                         proposals_lost_count=10,
                         discount_applied_count=0)
        # 20 (count) + comp_loss_rate=20% => no extra
        assert engine._competitive_exposure_score(inp) == 20.0

    def test_competitor_lost_4_adds_35(self, engine):
        inp = make_input(competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=4,
                         proposals_lost_count=20,
                         discount_applied_count=0)
        # 35 (count) + comp_loss_rate=20% => no extra
        assert engine._competitive_exposure_score(inp) == 35.0

    def test_comp_loss_rate_above_60_adds_20(self, engine):
        # lost_to_comp=6, total_lost=9 => 66.7% >= 0.60 => +20
        inp = make_input(competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=6,
                         proposals_lost_count=9,
                         discount_applied_count=0)
        # count: >=4 => 35; rate: 66.7% => +20 => 55
        assert engine._competitive_exposure_score(inp) == 55.0

    def test_comp_loss_rate_between_40_60_adds_10(self, engine):
        # lost_to_comp=2, total_lost=4 => 50% in [0.40, 0.60)
        inp = make_input(competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=2,
                         proposals_lost_count=4,
                         discount_applied_count=0)
        # count: >=2 => 20; rate: 50% => +10 => 30
        assert engine._competitive_exposure_score(inp) == 30.0

    def test_discount_applied_5_adds_10(self, engine):
        inp = make_input(competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=0,
                         proposals_lost_count=0,
                         discount_applied_count=5)
        assert engine._competitive_exposure_score(inp) == 10.0

    def test_discount_applied_4_no_penalty(self, engine):
        inp = make_input(competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=0,
                         proposals_lost_count=0,
                         discount_applied_count=4)
        assert engine._competitive_exposure_score(inp) == 0.0

    def test_capped_at_100(self, engine):
        inp = make_input(competitive_deals_pct=0.80,
                         proposals_lost_to_competitor_count=10,
                         proposals_lost_count=10,
                         discount_applied_count=10)
        assert engine._competitive_exposure_score(inp) <= 100.0

    def test_zero_lost_no_comp_loss_rate(self, engine):
        # proposals_lost_count=0 => skip comp_loss_rate block
        inp = make_input(competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=0,
                         proposals_lost_count=0,
                         discount_applied_count=0)
        assert engine._competitive_exposure_score(inp) == 0.0

    def test_score_is_float(self, engine):
        inp = make_input()
        assert isinstance(engine._competitive_exposure_score(inp), float)


# ===========================================================================
# 6. PATTERN DETECTION
# ===========================================================================

class TestDetectPattern:
    def _scores(self, engine, inp):
        wr = engine._proposal_win_rate_score(inp)
        vel = engine._proposal_velocity_score(inp)
        val = engine._value_alignment_score(inp)
        comp = engine._competitive_exposure_score(inp)
        return wr, vel, val, comp

    def test_competitive_loss_pattern(self, engine):
        # Need competitive >= 35 AND lost_to_competitor >= 2
        # competitive_deals_pct=0.60 => +35, lost_to_competitor=3 => +35; total=70 (capped?)
        inp = make_input(competitive_deals_pct=0.60,
                         proposals_lost_to_competitor_count=3,
                         proposals_lost_count=5,
                         discount_applied_count=0,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        wr, vel, val, comp = self._scores(engine, inp)
        pattern = engine._detect_pattern(inp, wr, vel, val, comp)
        assert pattern == ProposalPattern.competitive_loss

    def test_competitive_loss_requires_count_ge_2(self, engine):
        # competitive=35 but only 1 lost to competitor => should NOT trigger competitive_loss
        inp = make_input(competitive_deals_pct=0.60,
                         proposals_lost_to_competitor_count=1,
                         proposals_lost_count=5,
                         discount_applied_count=0,
                         proposals_won_count=10,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50,
                         avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=0.0,
                         value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=0.0)
        wr, vel, val, comp = self._scores(engine, inp)
        pattern = engine._detect_pattern(inp, wr, vel, val, comp)
        assert pattern != ProposalPattern.competitive_loss

    def test_poor_win_rate_pattern(self, engine):
        # win_rate_score >= 35 AND current_period_win_rate_pct < 0.30
        # won=1, lost=9 => 10% win rate => +40; current=0.20 < 0.30
        inp = make_input(proposals_won_count=1,
                         proposals_lost_count=9,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.20,
                         prior_period_win_rate_pct=0.20,
                         competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=0,
                         discount_applied_count=0,
                         avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=0.0,
                         value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=0.0)
        wr, vel, val, comp = self._scores(engine, inp)
        pattern = engine._detect_pattern(inp, wr, vel, val, comp)
        assert pattern == ProposalPattern.poor_win_rate

    def test_proposal_staleness_pattern(self, engine):
        # velocity >= 30 AND stale >= 2; use stale=4 => +30 velocity
        inp = make_input(avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=4,
                         proposal_revision_avg_count=0.0,
                         proposals_won_count=10,
                         proposals_lost_count=0,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50,
                         competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=0,
                         discount_applied_count=0,
                         value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=0.0)
        wr, vel, val, comp = self._scores(engine, inp)
        pattern = engine._detect_pattern(inp, wr, vel, val, comp)
        assert pattern == ProposalPattern.proposal_staleness

    def test_value_misalignment_pattern(self, engine):
        # value >= 30 AND value_prop_alignment_score < 0.50
        # exec_sponsor < 0.25 => +30 value_alignment
        inp = make_input(value_prop_alignment_score=0.40,
                         executive_sponsor_rate_pct=0.10,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=0.0,
                         proposals_won_count=10,
                         proposals_lost_count=0,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50,
                         competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=0,
                         discount_applied_count=0,
                         avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=0.0)
        wr, vel, val, comp = self._scores(engine, inp)
        pattern = engine._detect_pattern(inp, wr, vel, val, comp)
        assert pattern == ProposalPattern.value_misalignment

    def test_budget_friction_pattern(self, engine):
        inp = make_input(avg_discount_pct=20.0,
                         proposals_lost_to_price_count=3,
                         proposals_won_count=10,
                         proposals_lost_count=3,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50,
                         competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=0,
                         discount_applied_count=0,
                         avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=0.0,
                         value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80)
        wr, vel, val, comp = self._scores(engine, inp)
        pattern = engine._detect_pattern(inp, wr, vel, val, comp)
        assert pattern == ProposalPattern.budget_friction

    def test_none_pattern(self, engine):
        inp = make_input()
        wr, vel, val, comp = self._scores(engine, inp)
        pattern = engine._detect_pattern(inp, wr, vel, val, comp)
        assert pattern == ProposalPattern.none

    def test_competitive_loss_takes_priority_over_poor_win_rate(self, engine):
        # Both conditions met: competitive_loss should win
        inp = make_input(competitive_deals_pct=0.60,
                         proposals_lost_to_competitor_count=3,
                         proposals_lost_count=9,
                         proposals_won_count=1,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.10,
                         prior_period_win_rate_pct=0.10,
                         discount_applied_count=0,
                         avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=0.0,
                         value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80,
                         avg_discount_pct=0.0)
        wr, vel, val, comp = self._scores(engine, inp)
        pattern = engine._detect_pattern(inp, wr, vel, val, comp)
        assert pattern == ProposalPattern.competitive_loss

    def test_budget_friction_requires_price_count_ge_2(self, engine):
        # avg_discount>=15 but only 1 lost to price
        inp = make_input(avg_discount_pct=20.0,
                         proposals_lost_to_price_count=1,
                         proposals_won_count=10,
                         proposals_lost_count=1,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50,
                         competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=0,
                         discount_applied_count=0,
                         avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=0.0,
                         value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80)
        wr, vel, val, comp = self._scores(engine, inp)
        pattern = engine._detect_pattern(inp, wr, vel, val, comp)
        assert pattern == ProposalPattern.none


# ===========================================================================
# 7. RISK LEVEL
# ===========================================================================

class TestRiskLevel:
    def test_low_below_20(self, engine):
        assert engine._risk_level(0.0) == ProposalRisk.low
        assert engine._risk_level(19.9) == ProposalRisk.low

    def test_moderate_at_20(self, engine):
        assert engine._risk_level(20.0) == ProposalRisk.moderate

    def test_moderate_below_40(self, engine):
        assert engine._risk_level(39.9) == ProposalRisk.moderate

    def test_high_at_40(self, engine):
        assert engine._risk_level(40.0) == ProposalRisk.high

    def test_high_below_60(self, engine):
        assert engine._risk_level(59.9) == ProposalRisk.high

    def test_critical_at_60(self, engine):
        assert engine._risk_level(60.0) == ProposalRisk.critical

    def test_critical_above_60(self, engine):
        assert engine._risk_level(100.0) == ProposalRisk.critical

    def test_boundary_exactly_20(self, engine):
        assert engine._risk_level(20.0) == ProposalRisk.moderate

    def test_boundary_exactly_40(self, engine):
        assert engine._risk_level(40.0) == ProposalRisk.high

    def test_boundary_exactly_60(self, engine):
        assert engine._risk_level(60.0) == ProposalRisk.critical


# ===========================================================================
# 8. SEVERITY LEVEL
# ===========================================================================

class TestSeverityLevel:
    def test_healthy_below_20(self, engine):
        assert engine._severity(0.0) == ProposalSeverity.healthy
        assert engine._severity(19.9) == ProposalSeverity.healthy

    def test_declining_at_20(self, engine):
        assert engine._severity(20.0) == ProposalSeverity.declining

    def test_declining_below_40(self, engine):
        assert engine._severity(39.9) == ProposalSeverity.declining

    def test_stalled_at_40(self, engine):
        assert engine._severity(40.0) == ProposalSeverity.stalled

    def test_stalled_below_60(self, engine):
        assert engine._severity(59.9) == ProposalSeverity.stalled

    def test_critical_at_60(self, engine):
        assert engine._severity(60.0) == ProposalSeverity.critical

    def test_critical_above_60(self, engine):
        assert engine._severity(100.0) == ProposalSeverity.critical

    def test_boundary_exactly_20(self, engine):
        assert engine._severity(20.0) == ProposalSeverity.declining

    def test_boundary_exactly_40(self, engine):
        assert engine._severity(40.0) == ProposalSeverity.stalled

    def test_boundary_exactly_60(self, engine):
        assert engine._severity(60.0) == ProposalSeverity.critical


# ===========================================================================
# 9. ACTION LOGIC
# ===========================================================================

class TestActionLogic:
    def test_critical_competitive_loss(self, engine):
        action = engine._action(ProposalRisk.critical, ProposalPattern.competitive_loss)
        assert action == ProposalAction.competitive_repositioning

    def test_critical_poor_win_rate(self, engine):
        action = engine._action(ProposalRisk.critical, ProposalPattern.poor_win_rate)
        assert action == ProposalAction.executive_escalation

    def test_critical_proposal_staleness(self, engine):
        action = engine._action(ProposalRisk.critical, ProposalPattern.proposal_staleness)
        assert action == ProposalAction.executive_escalation

    def test_critical_value_misalignment(self, engine):
        action = engine._action(ProposalRisk.critical, ProposalPattern.value_misalignment)
        assert action == ProposalAction.executive_escalation

    def test_critical_budget_friction(self, engine):
        action = engine._action(ProposalRisk.critical, ProposalPattern.budget_friction)
        assert action == ProposalAction.executive_escalation

    def test_critical_none(self, engine):
        action = engine._action(ProposalRisk.critical, ProposalPattern.none)
        assert action == ProposalAction.executive_escalation

    def test_high_competitive_loss(self, engine):
        action = engine._action(ProposalRisk.high, ProposalPattern.competitive_loss)
        assert action == ProposalAction.competitive_repositioning

    def test_high_value_misalignment(self, engine):
        action = engine._action(ProposalRisk.high, ProposalPattern.value_misalignment)
        assert action == ProposalAction.value_messaging_update

    def test_high_poor_win_rate(self, engine):
        action = engine._action(ProposalRisk.high, ProposalPattern.poor_win_rate)
        assert action == ProposalAction.proposal_coaching

    def test_high_proposal_staleness(self, engine):
        action = engine._action(ProposalRisk.high, ProposalPattern.proposal_staleness)
        assert action == ProposalAction.proposal_coaching

    def test_high_budget_friction(self, engine):
        action = engine._action(ProposalRisk.high, ProposalPattern.budget_friction)
        assert action == ProposalAction.proposal_coaching

    def test_high_none(self, engine):
        action = engine._action(ProposalRisk.high, ProposalPattern.none)
        assert action == ProposalAction.proposal_coaching

    def test_moderate_budget_friction(self, engine):
        action = engine._action(ProposalRisk.moderate, ProposalPattern.budget_friction)
        assert action == ProposalAction.pricing_optimization

    def test_moderate_competitive_loss(self, engine):
        action = engine._action(ProposalRisk.moderate, ProposalPattern.competitive_loss)
        assert action == ProposalAction.proposal_coaching

    def test_moderate_poor_win_rate(self, engine):
        action = engine._action(ProposalRisk.moderate, ProposalPattern.poor_win_rate)
        assert action == ProposalAction.proposal_coaching

    def test_moderate_none(self, engine):
        action = engine._action(ProposalRisk.moderate, ProposalPattern.none)
        assert action == ProposalAction.proposal_coaching

    def test_low_all_patterns(self, engine):
        for pattern in ProposalPattern:
            action = engine._action(ProposalRisk.low, pattern)
            assert action == ProposalAction.no_action


# ===========================================================================
# 10. IS_WIN_RATE_DECLINING FLAG
# ===========================================================================

class TestIsWinRateDeclining:
    def test_current_below_prior_minus_5_pct(self, engine):
        inp = make_input(current_period_win_rate_pct=0.40,
                         prior_period_win_rate_pct=0.50)
        assert engine._is_win_rate_declining(inp, 0.0) is True

    def test_current_exactly_prior_minus_5_pct(self, engine):
        # 0.45 = 0.50 - 0.05 => NOT < (prior - 0.05), not triggered
        inp = make_input(current_period_win_rate_pct=0.45,
                         prior_period_win_rate_pct=0.50)
        assert engine._is_win_rate_declining(inp, 0.0) is False

    def test_current_above_prior_minus_5_pct(self, engine):
        inp = make_input(current_period_win_rate_pct=0.47,
                         prior_period_win_rate_pct=0.50)
        assert engine._is_win_rate_declining(inp, 0.0) is False

    def test_win_rate_score_ge_40_triggers(self, engine):
        inp = make_input(current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        assert engine._is_win_rate_declining(inp, 40.0) is True

    def test_win_rate_score_exactly_40(self, engine):
        inp = make_input(current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        assert engine._is_win_rate_declining(inp, 40.0) is True

    def test_win_rate_score_39_no_trigger(self, engine):
        inp = make_input(current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        assert engine._is_win_rate_declining(inp, 39.9) is False

    def test_both_conditions_true(self, engine):
        inp = make_input(current_period_win_rate_pct=0.30,
                         prior_period_win_rate_pct=0.50)
        assert engine._is_win_rate_declining(inp, 50.0) is True

    def test_neither_condition_false(self, engine):
        inp = make_input(current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50)
        assert engine._is_win_rate_declining(inp, 10.0) is False

    def test_improving_win_rate_no_score_trigger(self, engine):
        inp = make_input(current_period_win_rate_pct=0.60,
                         prior_period_win_rate_pct=0.50)
        assert engine._is_win_rate_declining(inp, 5.0) is False

    def test_returns_bool(self, engine):
        inp = make_input()
        result = engine._is_win_rate_declining(inp, 0.0)
        assert isinstance(result, bool)


# ===========================================================================
# 11. REQUIRES_PROPOSAL_REDESIGN FLAG
# ===========================================================================

class TestRequiresProposalRedesign:
    def test_composite_ge_30_triggers(self, engine):
        inp = make_input(value_prop_alignment_score=0.90)
        assert engine._requires_proposal_redesign(30.0, inp) is True

    def test_composite_29_no_trigger_alone(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         proposals_stale_count=0)
        assert engine._requires_proposal_redesign(29.0, inp) is False

    def test_value_prop_below_35_triggers(self, engine):
        inp = make_input(value_prop_alignment_score=0.30,
                         proposals_stale_count=0)
        assert engine._requires_proposal_redesign(0.0, inp) is True

    def test_value_prop_at_35_no_trigger_alone(self, engine):
        inp = make_input(value_prop_alignment_score=0.35,
                         proposals_stale_count=0)
        assert engine._requires_proposal_redesign(0.0, inp) is False

    def test_stale_ge_3_and_composite_ge_25_triggers(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         proposals_stale_count=3)
        assert engine._requires_proposal_redesign(25.0, inp) is True

    def test_stale_ge_3_but_composite_24_no_trigger(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         proposals_stale_count=3)
        assert engine._requires_proposal_redesign(24.0, inp) is False

    def test_stale_2_and_composite_25_no_stale_trigger(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         proposals_stale_count=2)
        assert engine._requires_proposal_redesign(25.0, inp) is False

    def test_all_false_no_trigger(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         proposals_stale_count=0)
        assert engine._requires_proposal_redesign(10.0, inp) is False

    def test_returns_bool(self, engine):
        inp = make_input()
        result = engine._requires_proposal_redesign(10.0, inp)
        assert isinstance(result, bool)

    def test_composite_exactly_30(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         proposals_stale_count=0)
        assert engine._requires_proposal_redesign(30.0, inp) is True

    def test_composite_exactly_25_with_stale_3(self, engine):
        inp = make_input(value_prop_alignment_score=0.90,
                         proposals_stale_count=3)
        assert engine._requires_proposal_redesign(25.0, inp) is True


# ===========================================================================
# 12. ESTIMATED LOST REVENUE
# ===========================================================================

class TestEstimatedLostRevenue:
    def test_zero_lost_count(self, engine):
        inp = make_input(proposals_lost_count=0, avg_proposal_size_usd=100_000.0)
        rev = engine._estimated_lost_revenue(inp, 50.0)
        assert rev == 0.0

    def test_zero_composite(self, engine):
        inp = make_input(proposals_lost_count=5, avg_proposal_size_usd=50_000.0)
        rev = engine._estimated_lost_revenue(inp, 0.0)
        assert rev == 0.0

    def test_basic_calculation(self, engine):
        inp = make_input(proposals_lost_count=3, avg_proposal_size_usd=50_000.0)
        rev = engine._estimated_lost_revenue(inp, 50.0)
        assert rev == 75_000.0

    def test_calculation_rounded_to_2_decimals(self, engine):
        inp = make_input(proposals_lost_count=1, avg_proposal_size_usd=33_333.33)
        rev = engine._estimated_lost_revenue(inp, 33.3)
        assert rev == round(33_333.33 * 0.333, 2)

    def test_100_composite(self, engine):
        inp = make_input(proposals_lost_count=2, avg_proposal_size_usd=100_000.0)
        rev = engine._estimated_lost_revenue(inp, 100.0)
        assert rev == 200_000.0

    def test_returns_float(self, engine):
        inp = make_input()
        rev = engine._estimated_lost_revenue(inp, 30.0)
        assert isinstance(rev, float)

    def test_large_values(self, engine):
        inp = make_input(proposals_lost_count=100, avg_proposal_size_usd=1_000_000.0)
        rev = engine._estimated_lost_revenue(inp, 75.0)
        assert rev == 75_000_000.0


# ===========================================================================
# 13. SIGNAL STRING
# ===========================================================================

class TestSignalString:
    def test_none_pattern_below_20_returns_benchmark_string(self, engine):
        inp = make_input(current_period_win_rate_pct=0.50,
                         proposals_stale_count=0,
                         value_prop_alignment_score=0.90,
                         proposals_lost_to_competitor_count=0)
        signal = engine._signal(inp, ProposalPattern.none, 15.0)
        assert signal == "Proposal conversion rate within benchmarks"

    def test_none_pattern_at_20_not_benchmark(self, engine):
        inp = make_input(current_period_win_rate_pct=0.50,
                         proposals_stale_count=0,
                         value_prop_alignment_score=0.90,
                         proposals_lost_to_competitor_count=0)
        signal = engine._signal(inp, ProposalPattern.none, 20.0)
        assert signal != "Proposal conversion rate within benchmarks"

    def test_non_none_pattern_below_20_not_benchmark(self, engine):
        inp = make_input(current_period_win_rate_pct=0.50,
                         proposals_stale_count=0,
                         value_prop_alignment_score=0.90,
                         proposals_lost_to_competitor_count=0)
        signal = engine._signal(inp, ProposalPattern.poor_win_rate, 10.0)
        assert signal != "Proposal conversion rate within benchmarks"

    def test_signal_includes_pattern_label(self, engine):
        inp = make_input(current_period_win_rate_pct=0.50,
                         proposals_stale_count=0,
                         value_prop_alignment_score=0.90,
                         proposals_lost_to_competitor_count=0)
        signal = engine._signal(inp, ProposalPattern.competitive_loss, 50.0)
        assert "competitive loss" in signal.lower()

    def test_signal_includes_win_rate_when_low(self, engine):
        inp = make_input(current_period_win_rate_pct=0.20,
                         proposals_stale_count=0,
                         value_prop_alignment_score=0.90,
                         proposals_lost_to_competitor_count=0)
        signal = engine._signal(inp, ProposalPattern.poor_win_rate, 40.0)
        assert "20% win rate" in signal

    def test_signal_includes_stale_count(self, engine):
        inp = make_input(current_period_win_rate_pct=0.50,
                         proposals_stale_count=3,
                         value_prop_alignment_score=0.90,
                         proposals_lost_to_competitor_count=0)
        signal = engine._signal(inp, ProposalPattern.proposal_staleness, 40.0)
        assert "3 stale proposals" in signal

    def test_signal_includes_value_alignment_when_low(self, engine):
        inp = make_input(current_period_win_rate_pct=0.50,
                         proposals_stale_count=0,
                         value_prop_alignment_score=0.40,
                         proposals_lost_to_competitor_count=0)
        signal = engine._signal(inp, ProposalPattern.value_misalignment, 40.0)
        assert "40% value alignment" in signal

    def test_signal_includes_competitor_count(self, engine):
        inp = make_input(current_period_win_rate_pct=0.50,
                         proposals_stale_count=0,
                         value_prop_alignment_score=0.90,
                         proposals_lost_to_competitor_count=3)
        signal = engine._signal(inp, ProposalPattern.competitive_loss, 50.0)
        assert "3 lost to competition" in signal

    def test_signal_fallback_when_no_parts(self, engine):
        inp = make_input(current_period_win_rate_pct=0.50,
                         proposals_stale_count=0,
                         value_prop_alignment_score=0.90,
                         proposals_lost_to_competitor_count=0)
        signal = engine._signal(inp, ProposalPattern.budget_friction, 25.0)
        assert "conversion efficiency degraded" in signal

    def test_signal_includes_composite(self, engine):
        inp = make_input(current_period_win_rate_pct=0.50,
                         proposals_stale_count=0,
                         value_prop_alignment_score=0.90,
                         proposals_lost_to_competitor_count=0)
        signal = engine._signal(inp, ProposalPattern.budget_friction, 42.0)
        assert "composite 42" in signal

    def test_signal_none_pattern_capitalizes_proposal_risk(self, engine):
        inp = make_input(current_period_win_rate_pct=0.20,
                         proposals_stale_count=0,
                         value_prop_alignment_score=0.90,
                         proposals_lost_to_competitor_count=0)
        signal = engine._signal(inp, ProposalPattern.none, 25.0)
        assert signal.startswith("Proposal risk")

    def test_signal_is_string(self, engine):
        inp = make_input()
        signal = engine._signal(inp, ProposalPattern.none, 15.0)
        assert isinstance(signal, str)


# ===========================================================================
# 14. TO_DICT() — exactly 15 keys
# ===========================================================================

class TestToDict:
    def test_returns_dict(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.to_dict(), dict)

    def test_exactly_15_keys(self, engine):
        result = engine.assess(make_input())
        assert len(result.to_dict()) == 15

    def test_key_rep_id(self, engine):
        result = engine.assess(make_input(rep_id="xyz"))
        assert result.to_dict()["rep_id"] == "xyz"

    def test_key_region(self, engine):
        result = engine.assess(make_input(region="East"))
        assert result.to_dict()["region"] == "East"

    def test_key_proposal_risk_is_string(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.to_dict()["proposal_risk"], str)

    def test_key_proposal_pattern_is_string(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.to_dict()["proposal_pattern"], str)

    def test_key_proposal_severity_is_string(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.to_dict()["proposal_severity"], str)

    def test_key_recommended_action_is_string(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.to_dict()["recommended_action"], str)

    def test_key_proposal_win_rate_score(self, engine):
        result = engine.assess(make_input())
        assert "proposal_win_rate_score" in result.to_dict()

    def test_key_proposal_velocity_score(self, engine):
        result = engine.assess(make_input())
        assert "proposal_velocity_score" in result.to_dict()

    def test_key_value_alignment_score(self, engine):
        result = engine.assess(make_input())
        assert "value_alignment_score" in result.to_dict()

    def test_key_competitive_exposure_score(self, engine):
        result = engine.assess(make_input())
        assert "competitive_exposure_score" in result.to_dict()

    def test_key_proposal_effectiveness_composite(self, engine):
        result = engine.assess(make_input())
        assert "proposal_effectiveness_composite" in result.to_dict()

    def test_key_is_win_rate_declining_is_bool(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.to_dict()["is_win_rate_declining"], bool)

    def test_key_requires_proposal_redesign_is_bool(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.to_dict()["requires_proposal_redesign"], bool)

    def test_key_estimated_lost_revenue_usd(self, engine):
        result = engine.assess(make_input())
        assert "estimated_lost_revenue_usd" in result.to_dict()

    def test_key_proposal_signal_is_string(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.to_dict()["proposal_signal"], str)

    def test_enum_values_are_strings_not_enum_objects(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert d["proposal_risk"] in {"low", "moderate", "high", "critical"}
        assert d["proposal_pattern"] in {
            "none", "poor_win_rate", "proposal_staleness",
            "value_misalignment", "competitive_loss", "budget_friction",
        }

    def test_all_expected_keys_present(self, engine):
        expected_keys = {
            "rep_id", "region", "proposal_risk", "proposal_pattern",
            "proposal_severity", "recommended_action",
            "proposal_win_rate_score", "proposal_velocity_score",
            "value_alignment_score", "competitive_exposure_score",
            "proposal_effectiveness_composite", "is_win_rate_declining",
            "requires_proposal_redesign", "estimated_lost_revenue_usd",
            "proposal_signal",
        }
        assert set(engine.assess(make_input()).to_dict().keys()) == expected_keys


# ===========================================================================
# 15. SUMMARY() — exactly 13 keys
# ===========================================================================

class TestSummary:
    def test_empty_summary_has_13_keys(self, engine):
        assert len(engine.summary()) == 13

    def test_empty_summary_total_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_summary_all_zero_averages(self, engine):
        s = engine.summary()
        assert s["avg_proposal_effectiveness_composite"] == 0.0
        assert s["declining_win_rate_count"] == 0
        assert s["proposal_redesign_count"] == 0
        assert s["avg_proposal_win_rate_score"] == 0.0
        assert s["avg_proposal_velocity_score"] == 0.0
        assert s["avg_value_alignment_score"] == 0.0
        assert s["avg_competitive_exposure_score"] == 0.0
        assert s["total_estimated_lost_revenue_usd"] == 0.0

    def test_summary_after_one_assess_has_13_keys(self, engine):
        engine.assess(make_input())
        assert len(engine.summary()) == 13

    def test_summary_total_reflects_count(self, engine):
        engine.assess(make_input())
        engine.assess(make_input())
        assert engine.summary()["total"] == 2

    def test_summary_risk_counts_populated(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == 1

    def test_summary_pattern_counts_populated(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == 1

    def test_summary_severity_counts_populated(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == 1

    def test_summary_action_counts_populated(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert sum(s["action_counts"].values()) == 1

    def test_summary_avg_composite_is_float(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.summary()["avg_proposal_effectiveness_composite"], float)

    def test_summary_total_revenue_is_float(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.summary()["total_estimated_lost_revenue_usd"], float)

    def test_summary_keys(self, engine):
        engine.assess(make_input())
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_proposal_effectiveness_composite",
            "declining_win_rate_count", "proposal_redesign_count",
            "avg_proposal_win_rate_score", "avg_proposal_velocity_score",
            "avg_value_alignment_score", "avg_competitive_exposure_score",
            "total_estimated_lost_revenue_usd",
        }
        assert set(engine.summary().keys()) == expected

    def test_summary_declining_count_accurate(self, engine):
        engine.assess(make_input(current_period_win_rate_pct=0.30,
                                  prior_period_win_rate_pct=0.50))
        engine.assess(make_input(current_period_win_rate_pct=0.50,
                                  prior_period_win_rate_pct=0.50))
        s = engine.summary()
        assert s["declining_win_rate_count"] >= 1


# ===========================================================================
# 16. ASSESS_BATCH
# ===========================================================================

class TestAssessBatch:
    def test_empty_batch(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_single_item_batch(self, engine):
        results = engine.assess_batch([make_input()])
        assert len(results) == 1

    def test_multiple_items_batch(self, engine):
        inputs = [make_input(rep_id=f"rep_{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_results_are_proposal_conversion_result(self, engine):
        results = engine.assess_batch([make_input()])
        assert isinstance(results[0], ProposalConversionResult)

    def test_batch_accumulates_in_results(self, engine):
        engine.assess_batch([make_input(), make_input()])
        assert engine.summary()["total"] == 2

    def test_batch_preserves_rep_ids(self, engine):
        inputs = [make_input(rep_id=f"rep_{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        rep_ids = [r.rep_id for r in results]
        assert rep_ids == ["rep_0", "rep_1", "rep_2"]

    def test_batch_returns_list(self, engine):
        results = engine.assess_batch([make_input()])
        assert isinstance(results, list)

    def test_batch_handles_diverse_inputs(self, engine):
        inputs = [
            make_input(proposals_won_count=0, proposals_lost_count=10),
            make_input(proposals_won_count=10, proposals_lost_count=0),
            make_input(competitive_deals_pct=0.90, proposals_lost_to_competitor_count=5),
        ]
        results = engine.assess_batch(inputs)
        assert len(results) == 3


# ===========================================================================
# 17. FULL ASSESS INTEGRATION
# ===========================================================================

class TestAssessIntegration:
    def test_assess_returns_proposal_conversion_result(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result, ProposalConversionResult)

    def test_assess_rep_id_passthrough(self, engine):
        result = engine.assess(make_input(rep_id="test_rep"))
        assert result.rep_id == "test_rep"

    def test_assess_region_passthrough(self, engine):
        result = engine.assess(make_input(region="North"))
        assert result.region == "North"

    def test_composite_between_0_and_100(self, engine):
        result = engine.assess(make_input())
        assert 0.0 <= result.proposal_effectiveness_composite <= 100.0

    def test_composite_capped_at_100_with_max_inputs(self, engine):
        inp = make_input(
            proposals_won_count=0, proposals_lost_count=10,
            proposals_lost_no_decision_count=5,
            current_period_win_rate_pct=0.05, prior_period_win_rate_pct=0.50,
            avg_days_proposal_to_decision=120.0, proposals_stale_count=10,
            proposal_revision_avg_count=10.0, value_prop_alignment_score=0.10,
            executive_sponsor_rate_pct=0.10, multi_stakeholder_proposals_pct=0.10,
            avg_discount_pct=30.0, competitive_deals_pct=0.90,
            proposals_lost_to_competitor_count=10, discount_applied_count=10,
        )
        result = engine.assess(inp)
        assert result.proposal_effectiveness_composite <= 100.0

    def test_assess_risk_type(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.proposal_risk, ProposalRisk)

    def test_assess_pattern_type(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.proposal_pattern, ProposalPattern)

    def test_assess_severity_type(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.proposal_severity, ProposalSeverity)

    def test_assess_action_type(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.recommended_action, ProposalAction)

    def test_assess_accumulates_results(self, engine):
        engine.assess(make_input())
        engine.assess(make_input())
        assert len(engine._results) == 2

    def test_low_risk_scenario(self, engine):
        # All perfect conditions
        inp = make_input(
            proposals_won_count=10, proposals_lost_count=0,
            proposals_lost_no_decision_count=0,
            current_period_win_rate_pct=0.60, prior_period_win_rate_pct=0.55,
            avg_days_proposal_to_decision=10.0, proposals_stale_count=0,
            proposal_revision_avg_count=1.0, value_prop_alignment_score=0.90,
            executive_sponsor_rate_pct=0.70, multi_stakeholder_proposals_pct=0.80,
            avg_discount_pct=5.0, competitive_deals_pct=0.10,
            proposals_lost_to_competitor_count=0, discount_applied_count=0,
        )
        result = engine.assess(inp)
        assert result.proposal_risk == ProposalRisk.low
        assert result.proposal_severity == ProposalSeverity.healthy

    def test_critical_risk_scenario(self, engine):
        inp = make_input(
            proposals_won_count=0, proposals_lost_count=10,
            proposals_lost_no_decision_count=5,
            current_period_win_rate_pct=0.05, prior_period_win_rate_pct=0.50,
            avg_days_proposal_to_decision=120.0, proposals_stale_count=6,
            proposal_revision_avg_count=6.0, value_prop_alignment_score=0.20,
            executive_sponsor_rate_pct=0.10, multi_stakeholder_proposals_pct=0.10,
            avg_discount_pct=30.0, competitive_deals_pct=0.80,
            proposals_lost_to_competitor_count=8, discount_applied_count=8,
        )
        result = engine.assess(inp)
        assert result.proposal_risk == ProposalRisk.critical
        assert result.proposal_severity == ProposalSeverity.critical

    def test_zero_proposals_sent(self, engine):
        inp = make_input(proposals_sent_count=0, proposals_won_count=0,
                         proposals_lost_count=0, proposals_pending_count=0)
        result = engine.assess(inp)
        assert isinstance(result, ProposalConversionResult)

    def test_100_percent_win_rate(self, engine):
        inp = make_input(proposals_won_count=10, proposals_lost_count=0,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=1.0,
                         prior_period_win_rate_pct=0.90)
        result = engine.assess(inp)
        assert result.proposal_win_rate_score == 0.0

    def test_estimated_lost_revenue_zero_when_no_losses(self, engine):
        inp = make_input(proposals_lost_count=0)
        result = engine.assess(inp)
        assert result.estimated_lost_revenue_usd == 0.0

    def test_estimated_lost_revenue_positive_with_losses(self, engine):
        inp = make_input(proposals_lost_count=5, avg_proposal_size_usd=100_000.0)
        result = engine.assess(inp)
        if result.proposal_effectiveness_composite > 0:
            assert result.estimated_lost_revenue_usd > 0.0

    def test_default_input_signal_within_benchmarks(self, engine):
        # Default input should have low composite => "within benchmarks"
        inp = make_input(
            proposals_won_count=10, proposals_lost_count=0,
            proposals_lost_no_decision_count=0,
            current_period_win_rate_pct=0.60, prior_period_win_rate_pct=0.55,
            avg_days_proposal_to_decision=10.0, proposals_stale_count=0,
            proposal_revision_avg_count=1.0, value_prop_alignment_score=0.90,
            executive_sponsor_rate_pct=0.70, multi_stakeholder_proposals_pct=0.80,
            avg_discount_pct=5.0, competitive_deals_pct=0.10,
            proposals_lost_to_competitor_count=0, discount_applied_count=0,
        )
        result = engine.assess(inp)
        assert result.proposal_signal == "Proposal conversion rate within benchmarks"

    def test_composite_weights_correct(self, engine):
        # Manually force sub-scores to known values and check composite
        # Use a pristine input with known score contributions
        # win_rate=0, velocity=0, value=0, competitive=0 => composite=0
        inp = make_input(
            proposals_won_count=10, proposals_lost_count=0,
            proposals_lost_no_decision_count=0,
            current_period_win_rate_pct=0.60, prior_period_win_rate_pct=0.55,
            avg_days_proposal_to_decision=0.0, proposals_stale_count=0,
            proposal_revision_avg_count=0.0, value_prop_alignment_score=0.90,
            executive_sponsor_rate_pct=0.70, multi_stakeholder_proposals_pct=0.80,
            avg_discount_pct=0.0, competitive_deals_pct=0.0,
            proposals_lost_to_competitor_count=0, discount_applied_count=0,
        )
        result = engine.assess(inp)
        assert result.proposal_effectiveness_composite == 0.0


# ===========================================================================
# 18. EDGE CASES & BOUNDARY CONDITIONS
# ===========================================================================

class TestEdgeCases:
    def test_zero_proposals_all_zeros(self, engine):
        # When won=0, lost=0 => decided=0 => win_rate=0/max(0,1)=0 < 0.15 => +40 win_rate score
        # So composite will be > 0; just verify it doesn't crash and returns a valid result
        inp = make_input(
            proposals_sent_count=0, proposals_won_count=0, proposals_lost_count=0,
            proposals_pending_count=0, proposals_stale_count=0,
            proposals_lost_to_price_count=0, proposals_lost_to_competitor_count=0,
            proposals_lost_no_decision_count=0,
            avg_days_proposal_to_decision=0.0,
            proposal_revision_avg_count=0.0,
            avg_discount_pct=0.0, discount_applied_count=0,
            competitive_deals_pct=0.0,
            executive_sponsor_rate_pct=0.70, value_prop_alignment_score=0.90,
            multi_stakeholder_proposals_pct=0.80,
            current_period_win_rate_pct=0.50, prior_period_win_rate_pct=0.50,
        )
        result = engine.assess(inp)
        # won=0, lost=0 => computed win_rate=0/1=0 < 0.15 => win_rate_score=40 => composite=12
        assert result.proposal_effectiveness_composite == 12.0

    def test_all_proposals_lost(self, engine):
        inp = make_input(proposals_won_count=0, proposals_lost_count=10)
        result = engine.assess(inp)
        assert result.estimated_lost_revenue_usd > 0

    def test_very_large_proposal_size(self, engine):
        inp = make_input(avg_proposal_size_usd=10_000_000.0)
        result = engine.assess(inp)
        assert isinstance(result, ProposalConversionResult)

    def test_very_small_win_rate(self, engine):
        inp = make_input(proposals_won_count=0, proposals_lost_count=100,
                         current_period_win_rate_pct=0.01,
                         prior_period_win_rate_pct=0.50)
        result = engine.assess(inp)
        assert result.is_win_rate_declining is True

    def test_max_discount(self, engine):
        inp = make_input(avg_discount_pct=100.0)
        result = engine.assess(inp)
        assert isinstance(result, ProposalConversionResult)

    def test_min_value_prop_alignment(self, engine):
        inp = make_input(value_prop_alignment_score=0.0)
        result = engine.assess(inp)
        assert result.requires_proposal_redesign is True

    def test_max_value_prop_alignment(self, engine):
        inp = make_input(value_prop_alignment_score=1.0)
        result = engine.assess(inp)
        assert isinstance(result, ProposalConversionResult)

    def test_stale_count_exactly_1(self, engine):
        inp = make_input(proposals_stale_count=1, avg_days_proposal_to_decision=0.0,
                         proposal_revision_avg_count=0.0)
        score = engine._proposal_velocity_score(inp)
        assert score == 8.0

    def test_new_engine_empty_results(self, engine):
        assert engine._results == []

    def test_multiple_engines_independent(self):
        e1 = SalesProposalConversionIntelligenceEngine()
        e2 = SalesProposalConversionIntelligenceEngine()
        e1.assess(make_input())
        assert e2.summary()["total"] == 0

    def test_assess_batch_then_summary_consistent(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(10)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 10

    def test_win_rate_score_rounded_to_1_decimal(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        # Check that sub-scores are rounded to 1 decimal
        wr = result.proposal_win_rate_score
        assert wr == round(wr, 1)

    def test_composite_rounded_to_1_decimal(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        composite = result.proposal_effectiveness_composite
        assert composite == round(composite, 1)

    def test_revenue_rounded_to_2_decimals(self, engine):
        inp = make_input(proposals_lost_count=3, avg_proposal_size_usd=33_333.33)
        result = engine.assess(inp)
        rev = result.estimated_lost_revenue_usd
        assert rev == round(rev, 2)

    def test_proposal_conversion_input_is_dataclass(self):
        inp = make_input()
        assert isinstance(inp, ProposalConversionInput)

    def test_proposal_conversion_result_is_dataclass(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result, ProposalConversionResult)

    def test_high_stale_triggers_redesign_with_composite_25(self, engine):
        # stale=3, need composite>=25 to trigger the stale+composite redesign condition.
        # Use _requires_proposal_redesign directly with stale=3 and composite=25.
        inp = make_input(proposals_stale_count=3, value_prop_alignment_score=0.90)
        assert engine._requires_proposal_redesign(25.0, inp) is True

    def test_budget_friction_requires_discount_ge_15(self, engine):
        # avg_discount=14.9 < 15 => no budget_friction even with price losses
        inp = make_input(avg_discount_pct=14.9,
                         proposals_lost_to_price_count=5,
                         proposals_won_count=10, proposals_lost_count=5,
                         proposals_lost_no_decision_count=0,
                         current_period_win_rate_pct=0.50,
                         prior_period_win_rate_pct=0.50,
                         competitive_deals_pct=0.0,
                         proposals_lost_to_competitor_count=0,
                         discount_applied_count=0,
                         avg_days_proposal_to_decision=0.0,
                         proposals_stale_count=0,
                         proposal_revision_avg_count=0.0,
                         value_prop_alignment_score=0.90,
                         executive_sponsor_rate_pct=0.70,
                         multi_stakeholder_proposals_pct=0.80)
        result = engine.assess(inp)
        assert result.proposal_pattern != ProposalPattern.budget_friction

    def test_competitive_loss_priority_over_all_others(self, engine):
        # Force all patterns to be eligible; competitive_loss should win
        inp = make_input(
            competitive_deals_pct=0.60,
            proposals_lost_to_competitor_count=3,
            proposals_lost_count=3,
            proposals_won_count=0,
            proposals_lost_no_decision_count=5,
            current_period_win_rate_pct=0.05,
            prior_period_win_rate_pct=0.50,
            avg_days_proposal_to_decision=120.0,
            proposals_stale_count=5,
            proposal_revision_avg_count=5.0,
            value_prop_alignment_score=0.20,
            executive_sponsor_rate_pct=0.10,
            multi_stakeholder_proposals_pct=0.10,
            avg_discount_pct=30.0,
            proposals_lost_to_price_count=3,
            discount_applied_count=10,
        )
        result = engine.assess(inp)
        assert result.proposal_pattern == ProposalPattern.competitive_loss

    def test_action_consistent_with_risk_and_pattern(self, engine):
        result = engine.assess(make_input())
        expected = engine._action(result.proposal_risk, result.proposal_pattern)
        assert result.recommended_action == expected
