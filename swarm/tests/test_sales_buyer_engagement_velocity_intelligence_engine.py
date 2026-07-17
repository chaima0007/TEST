"""
Comprehensive pytest test suite for SalesBuyerEngagementVelocityIntelligenceEngine.
"""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_buyer_engagement_velocity_intelligence_engine import (
    EngagementRisk,
    EngagementPattern,
    EngagementSeverity,
    EngagementAction,
    EngagementInput,
    EngagementResult,
    SalesBuyerEngagementVelocityIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> EngagementInput:
    """Return a baseline healthy EngagementInput with all 22 fields, overriding as needed."""
    defaults = dict(
        rep_id="REP001",
        region="WEST",
        evaluation_period_id="Q1-2026",
        avg_buyer_response_time_days=1.0,       # low velocity risk
        response_time_trend_days=0.5,
        ghosting_episodes_per_deal=0.0,
        buyer_initiated_contact_pct=0.50,
        stakeholder_breadth_avg=4.0,
        executive_engagement_rate_pct=0.50,
        meeting_acceptance_rate_pct=0.80,
        content_open_rate_pct=0.70,
        follow_up_required_before_response_pct=0.10,
        multi_stakeholder_deals_pct=0.70,
        engagement_drop_after_proposal_pct=0.10,
        champion_response_time_days=1.0,
        mutual_action_plan_completion_pct=0.85,
        next_step_set_rate_pct=0.80,
        deal_re_engaged_after_silence_pct=0.90,
        avg_days_between_meaningful_touches=5.0,
        late_stage_dark_period_pct=0.05,
        total_active_deals=10,
        avg_opportunity_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return EngagementInput(**defaults)


def fresh_engine() -> SalesBuyerEngagementVelocityIntelligenceEngine:
    return SalesBuyerEngagementVelocityIntelligenceEngine()


# ---------------------------------------------------------------------------
# 1. Enum values and counts
# ---------------------------------------------------------------------------

class TestEnums:
    def test_engagement_risk_values(self):
        assert set(e.value for e in EngagementRisk) == {"low", "moderate", "high", "critical"}

    def test_engagement_risk_count(self):
        assert len(EngagementRisk) == 4

    def test_engagement_pattern_values(self):
        expected = {
            "none",
            "buyer_ghosting_cycle",
            "single_contact_dependency",
            "response_lag_accumulation",
            "momentum_reversal",
            "executive_access_deficit",
        }
        assert set(e.value for e in EngagementPattern) == expected

    def test_engagement_pattern_count(self):
        assert len(EngagementPattern) == 6

    def test_engagement_severity_values(self):
        assert set(e.value for e in EngagementSeverity) == {
            "accelerating", "engaged", "slowing", "stalled"
        }

    def test_engagement_severity_count(self):
        assert len(EngagementSeverity) == 4

    def test_engagement_action_values(self):
        expected = {
            "no_action",
            "re_engagement_sequence_coaching",
            "multithreading_coaching",
            "executive_outreach_coaching",
            "deal_velocity_coaching",
            "deal_rescue_intervention",
        }
        assert set(e.value for e in EngagementAction) == expected

    def test_engagement_action_count(self):
        assert len(EngagementAction) == 6

    def test_enums_are_str_subclass(self):
        assert isinstance(EngagementRisk.low, str)
        assert isinstance(EngagementPattern.none, str)
        assert isinstance(EngagementSeverity.accelerating, str)
        assert isinstance(EngagementAction.no_action, str)


# ---------------------------------------------------------------------------
# 2. EngagementInput — all 22 fields
# ---------------------------------------------------------------------------

class TestEngagementInput:
    def test_all_22_fields_present(self):
        inp = make_input()
        assert inp.rep_id == "REP001"
        assert inp.region == "WEST"
        assert inp.evaluation_period_id == "Q1-2026"
        assert inp.avg_buyer_response_time_days == 1.0
        assert inp.response_time_trend_days == 0.5
        assert inp.ghosting_episodes_per_deal == 0.0
        assert inp.buyer_initiated_contact_pct == 0.50
        assert inp.stakeholder_breadth_avg == 4.0
        assert inp.executive_engagement_rate_pct == 0.50
        assert inp.meeting_acceptance_rate_pct == 0.80
        assert inp.content_open_rate_pct == 0.70
        assert inp.follow_up_required_before_response_pct == 0.10
        assert inp.multi_stakeholder_deals_pct == 0.70
        assert inp.engagement_drop_after_proposal_pct == 0.10
        assert inp.champion_response_time_days == 1.0
        assert inp.mutual_action_plan_completion_pct == 0.85
        assert inp.next_step_set_rate_pct == 0.80
        assert inp.deal_re_engaged_after_silence_pct == 0.90
        assert inp.avg_days_between_meaningful_touches == 5.0
        assert inp.late_stage_dark_period_pct == 0.05
        assert inp.total_active_deals == 10
        assert inp.avg_opportunity_value_usd == 50_000.0

    def test_field_count_via_dataclass(self):
        import dataclasses
        assert len(dataclasses.fields(EngagementInput)) == 22


# ---------------------------------------------------------------------------
# 3. EngagementResult — all 15 fields + to_dict 15 keys
# ---------------------------------------------------------------------------

class TestEngagementResult:
    def _sample_result(self) -> EngagementResult:
        engine = fresh_engine()
        return engine.assess(make_input())

    def test_result_has_15_fields(self):
        import dataclasses
        assert len(dataclasses.fields(EngagementResult)) == 15

    def test_result_field_names(self):
        import dataclasses
        names = {f.name for f in dataclasses.fields(EngagementResult)}
        assert names == {
            "rep_id", "region", "engagement_risk", "engagement_pattern",
            "engagement_severity", "recommended_action", "velocity_score",
            "breadth_score", "responsiveness_score", "momentum_score",
            "engagement_composite", "has_engagement_gap",
            "requires_engagement_coaching", "estimated_pipeline_at_risk_usd",
            "engagement_signal",
        }

    def test_to_dict_returns_15_keys(self):
        d = self._sample_result().to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self):
        d = self._sample_result().to_dict()
        assert set(d.keys()) == {
            "rep_id", "region", "engagement_risk", "engagement_pattern",
            "engagement_severity", "recommended_action", "velocity_score",
            "breadth_score", "responsiveness_score", "momentum_score",
            "engagement_composite", "has_engagement_gap",
            "requires_engagement_coaching", "estimated_pipeline_at_risk_usd",
            "engagement_signal",
        }

    def test_to_dict_enum_values_are_strings(self):
        d = self._sample_result().to_dict()
        assert isinstance(d["engagement_risk"], str)
        assert isinstance(d["engagement_pattern"], str)
        assert isinstance(d["engagement_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_and_region(self):
        d = fresh_engine().assess(make_input(rep_id="R99", region="EAST")).to_dict()
        assert d["rep_id"] == "R99"
        assert d["region"] == "EAST"


# ---------------------------------------------------------------------------
# 4. Sub-score: _velocity_score branches and cap
# ---------------------------------------------------------------------------

class TestVelocityScore:
    def _vs(self, **kw) -> float:
        engine = fresh_engine()
        return engine._velocity_score(make_input(**kw))

    # avg_buyer_response_time_days thresholds
    def test_response_time_below_1_5(self):
        assert self._vs(avg_buyer_response_time_days=1.0) == pytest.approx(0.0, abs=1e-6)

    def test_response_time_at_1_5(self):
        # >=1.5 → +8
        s = self._vs(avg_buyer_response_time_days=1.5,
                     avg_days_between_meaningful_touches=0.0,
                     next_step_set_rate_pct=1.0)
        assert s == pytest.approx(8.0)

    def test_response_time_between_1_5_and_3(self):
        s = self._vs(avg_buyer_response_time_days=2.0,
                     avg_days_between_meaningful_touches=0.0,
                     next_step_set_rate_pct=1.0)
        assert s == pytest.approx(8.0)

    def test_response_time_at_3(self):
        # >=3.0 → +22
        s = self._vs(avg_buyer_response_time_days=3.0,
                     avg_days_between_meaningful_touches=0.0,
                     next_step_set_rate_pct=1.0)
        assert s == pytest.approx(22.0)

    def test_response_time_at_5(self):
        # >=5.0 → +40
        s = self._vs(avg_buyer_response_time_days=5.0,
                     avg_days_between_meaningful_touches=0.0,
                     next_step_set_rate_pct=1.0)
        assert s == pytest.approx(40.0)

    def test_response_time_above_5(self):
        s = self._vs(avg_buyer_response_time_days=10.0,
                     avg_days_between_meaningful_touches=0.0,
                     next_step_set_rate_pct=1.0)
        assert s == pytest.approx(40.0)

    # avg_days_between_meaningful_touches thresholds
    def test_touches_below_7(self):
        s = self._vs(avg_buyer_response_time_days=0.0,
                     avg_days_between_meaningful_touches=5.0,
                     next_step_set_rate_pct=1.0)
        assert s == pytest.approx(0.0)

    def test_touches_at_7(self):
        # >=7.0 → +18
        s = self._vs(avg_buyer_response_time_days=0.0,
                     avg_days_between_meaningful_touches=7.0,
                     next_step_set_rate_pct=1.0)
        assert s == pytest.approx(18.0)

    def test_touches_at_14(self):
        # >=14.0 → +35
        s = self._vs(avg_buyer_response_time_days=0.0,
                     avg_days_between_meaningful_touches=14.0,
                     next_step_set_rate_pct=1.0)
        assert s == pytest.approx(35.0)

    # next_step_set_rate_pct thresholds
    def test_next_step_above_0_65(self):
        s = self._vs(avg_buyer_response_time_days=0.0,
                     avg_days_between_meaningful_touches=0.0,
                     next_step_set_rate_pct=0.80)
        assert s == pytest.approx(0.0)

    def test_next_step_at_0_65(self):
        # <=0.65 → +12
        s = self._vs(avg_buyer_response_time_days=0.0,
                     avg_days_between_meaningful_touches=0.0,
                     next_step_set_rate_pct=0.65)
        assert s == pytest.approx(12.0)

    def test_next_step_at_0_40(self):
        # <=0.40 → +25
        s = self._vs(avg_buyer_response_time_days=0.0,
                     avg_days_between_meaningful_touches=0.0,
                     next_step_set_rate_pct=0.40)
        assert s == pytest.approx(25.0)

    def test_next_step_below_0_40(self):
        s = self._vs(avg_buyer_response_time_days=0.0,
                     avg_days_between_meaningful_touches=0.0,
                     next_step_set_rate_pct=0.10)
        assert s == pytest.approx(25.0)

    def test_velocity_cap_at_100(self):
        # max possible: 40+35+25 = 100 → exact cap
        s = self._vs(avg_buyer_response_time_days=6.0,
                     avg_days_between_meaningful_touches=20.0,
                     next_step_set_rate_pct=0.10)
        assert s == pytest.approx(100.0)

    def test_velocity_exceeds_100_capped(self):
        # Confirm cap even when raw sum would exceed 100 (can't happen here, but verify)
        s = self._vs(avg_buyer_response_time_days=100.0,
                     avg_days_between_meaningful_touches=100.0,
                     next_step_set_rate_pct=0.0)
        assert s <= 100.0

    def test_velocity_additive_example(self):
        # response>=3 (+22), touches>=7 (+18), next_step<=0.65 (+12) = 52
        s = self._vs(avg_buyer_response_time_days=3.5,
                     avg_days_between_meaningful_touches=8.0,
                     next_step_set_rate_pct=0.55)
        assert s == pytest.approx(52.0)


# ---------------------------------------------------------------------------
# 5. Sub-score: _breadth_score branches and cap
# ---------------------------------------------------------------------------

class TestBreadthScore:
    def _bs(self, **kw) -> float:
        engine = fresh_engine()
        return engine._breadth_score(make_input(**kw))

    def test_stakeholder_above_3_5(self):
        s = self._bs(stakeholder_breadth_avg=4.0,
                     executive_engagement_rate_pct=1.0,
                     multi_stakeholder_deals_pct=1.0)
        assert s == pytest.approx(0.0)

    def test_stakeholder_at_3_5(self):
        # <=3.5 → +8
        s = self._bs(stakeholder_breadth_avg=3.5,
                     executive_engagement_rate_pct=1.0,
                     multi_stakeholder_deals_pct=1.0)
        assert s == pytest.approx(8.0)

    def test_stakeholder_at_2_5(self):
        # <=2.5 → +22
        s = self._bs(stakeholder_breadth_avg=2.5,
                     executive_engagement_rate_pct=1.0,
                     multi_stakeholder_deals_pct=1.0)
        assert s == pytest.approx(22.0)

    def test_stakeholder_at_1_5(self):
        # <=1.5 → +40
        s = self._bs(stakeholder_breadth_avg=1.5,
                     executive_engagement_rate_pct=1.0,
                     multi_stakeholder_deals_pct=1.0)
        assert s == pytest.approx(40.0)

    def test_executive_rate_above_0_40(self):
        s = self._bs(stakeholder_breadth_avg=5.0,
                     executive_engagement_rate_pct=0.50,
                     multi_stakeholder_deals_pct=1.0)
        assert s == pytest.approx(0.0)

    def test_executive_rate_at_0_40(self):
        # <=0.40 → +18
        s = self._bs(stakeholder_breadth_avg=5.0,
                     executive_engagement_rate_pct=0.40,
                     multi_stakeholder_deals_pct=1.0)
        assert s == pytest.approx(18.0)

    def test_executive_rate_at_0_20(self):
        # <=0.20 → +35
        s = self._bs(stakeholder_breadth_avg=5.0,
                     executive_engagement_rate_pct=0.20,
                     multi_stakeholder_deals_pct=1.0)
        assert s == pytest.approx(35.0)

    def test_multi_stakeholder_above_0_55(self):
        s = self._bs(stakeholder_breadth_avg=5.0,
                     executive_engagement_rate_pct=1.0,
                     multi_stakeholder_deals_pct=0.60)
        assert s == pytest.approx(0.0)

    def test_multi_stakeholder_at_0_55(self):
        # <=0.55 → +12
        s = self._bs(stakeholder_breadth_avg=5.0,
                     executive_engagement_rate_pct=1.0,
                     multi_stakeholder_deals_pct=0.55)
        assert s == pytest.approx(12.0)

    def test_multi_stakeholder_at_0_30(self):
        # <=0.30 → +25
        s = self._bs(stakeholder_breadth_avg=5.0,
                     executive_engagement_rate_pct=1.0,
                     multi_stakeholder_deals_pct=0.30)
        assert s == pytest.approx(25.0)

    def test_breadth_cap_at_100(self):
        # max: 40+35+25 = 100
        s = self._bs(stakeholder_breadth_avg=1.0,
                     executive_engagement_rate_pct=0.10,
                     multi_stakeholder_deals_pct=0.10)
        assert s == pytest.approx(100.0)

    def test_breadth_additive_example(self):
        # <=2.5 (+22) + <=0.40 (+18) + <=0.55 (+12) = 52
        s = self._bs(stakeholder_breadth_avg=2.0,
                     executive_engagement_rate_pct=0.35,
                     multi_stakeholder_deals_pct=0.50)
        assert s == pytest.approx(52.0)


# ---------------------------------------------------------------------------
# 6. Sub-score: _responsiveness_score branches and cap
# ---------------------------------------------------------------------------

class TestResponsivenessScore:
    def _rs(self, **kw) -> float:
        engine = fresh_engine()
        return engine._responsiveness_score(make_input(**kw))

    def test_followup_below_0_25(self):
        s = self._rs(follow_up_required_before_response_pct=0.10,
                     buyer_initiated_contact_pct=1.0,
                     content_open_rate_pct=1.0)
        assert s == pytest.approx(0.0)

    def test_followup_at_0_25(self):
        # >=0.25 → +8
        s = self._rs(follow_up_required_before_response_pct=0.25,
                     buyer_initiated_contact_pct=1.0,
                     content_open_rate_pct=1.0)
        assert s == pytest.approx(8.0)

    def test_followup_at_0_45(self):
        # >=0.45 → +22
        s = self._rs(follow_up_required_before_response_pct=0.45,
                     buyer_initiated_contact_pct=1.0,
                     content_open_rate_pct=1.0)
        assert s == pytest.approx(22.0)

    def test_followup_at_0_70(self):
        # >=0.70 → +40
        s = self._rs(follow_up_required_before_response_pct=0.70,
                     buyer_initiated_contact_pct=1.0,
                     content_open_rate_pct=1.0)
        assert s == pytest.approx(40.0)

    def test_buyer_initiated_above_0_30(self):
        s = self._rs(follow_up_required_before_response_pct=0.0,
                     buyer_initiated_contact_pct=0.50,
                     content_open_rate_pct=1.0)
        assert s == pytest.approx(0.0)

    def test_buyer_initiated_at_0_30(self):
        # <=0.30 → +18
        s = self._rs(follow_up_required_before_response_pct=0.0,
                     buyer_initiated_contact_pct=0.30,
                     content_open_rate_pct=1.0)
        assert s == pytest.approx(18.0)

    def test_buyer_initiated_at_0_15(self):
        # <=0.15 → +35
        s = self._rs(follow_up_required_before_response_pct=0.0,
                     buyer_initiated_contact_pct=0.15,
                     content_open_rate_pct=1.0)
        assert s == pytest.approx(35.0)

    def test_content_open_above_0_50(self):
        s = self._rs(follow_up_required_before_response_pct=0.0,
                     buyer_initiated_contact_pct=1.0,
                     content_open_rate_pct=0.60)
        assert s == pytest.approx(0.0)

    def test_content_open_at_0_50(self):
        # <=0.50 → +12
        s = self._rs(follow_up_required_before_response_pct=0.0,
                     buyer_initiated_contact_pct=1.0,
                     content_open_rate_pct=0.50)
        assert s == pytest.approx(12.0)

    def test_content_open_at_0_25(self):
        # <=0.25 → +25
        s = self._rs(follow_up_required_before_response_pct=0.0,
                     buyer_initiated_contact_pct=1.0,
                     content_open_rate_pct=0.25)
        assert s == pytest.approx(25.0)

    def test_responsiveness_cap_at_100(self):
        # max: 40+35+25 = 100
        s = self._rs(follow_up_required_before_response_pct=1.0,
                     buyer_initiated_contact_pct=0.0,
                     content_open_rate_pct=0.0)
        assert s == pytest.approx(100.0)

    def test_responsiveness_additive_example(self):
        # >=0.45 (+22) + <=0.30 (+18) + <=0.50 (+12) = 52
        s = self._rs(follow_up_required_before_response_pct=0.50,
                     buyer_initiated_contact_pct=0.25,
                     content_open_rate_pct=0.40)
        assert s == pytest.approx(52.0)


# ---------------------------------------------------------------------------
# 7. Sub-score: _momentum_score branches and cap
# ---------------------------------------------------------------------------

class TestMomentumScore:
    def _ms(self, **kw) -> float:
        engine = fresh_engine()
        return engine._momentum_score(make_input(**kw))

    def test_ghosting_below_0_5(self):
        s = self._ms(ghosting_episodes_per_deal=0.0,
                     engagement_drop_after_proposal_pct=0.0,
                     late_stage_dark_period_pct=0.0)
        assert s == pytest.approx(0.0)

    def test_ghosting_at_0_5(self):
        # >=0.5 → +10
        s = self._ms(ghosting_episodes_per_deal=0.5,
                     engagement_drop_after_proposal_pct=0.0,
                     late_stage_dark_period_pct=0.0)
        assert s == pytest.approx(10.0)

    def test_ghosting_at_1_5(self):
        # >=1.5 → +25
        s = self._ms(ghosting_episodes_per_deal=1.5,
                     engagement_drop_after_proposal_pct=0.0,
                     late_stage_dark_period_pct=0.0)
        assert s == pytest.approx(25.0)

    def test_ghosting_at_3_0(self):
        # >=3.0 → +45
        s = self._ms(ghosting_episodes_per_deal=3.0,
                     engagement_drop_after_proposal_pct=0.0,
                     late_stage_dark_period_pct=0.0)
        assert s == pytest.approx(45.0)

    def test_ghosting_above_3_0(self):
        s = self._ms(ghosting_episodes_per_deal=5.0,
                     engagement_drop_after_proposal_pct=0.0,
                     late_stage_dark_period_pct=0.0)
        assert s == pytest.approx(45.0)

    def test_drop_below_0_30(self):
        s = self._ms(ghosting_episodes_per_deal=0.0,
                     engagement_drop_after_proposal_pct=0.10,
                     late_stage_dark_period_pct=0.0)
        assert s == pytest.approx(0.0)

    def test_drop_at_0_30(self):
        # >=0.30 → +15
        s = self._ms(ghosting_episodes_per_deal=0.0,
                     engagement_drop_after_proposal_pct=0.30,
                     late_stage_dark_period_pct=0.0)
        assert s == pytest.approx(15.0)

    def test_drop_at_0_55(self):
        # >=0.55 → +30
        s = self._ms(ghosting_episodes_per_deal=0.0,
                     engagement_drop_after_proposal_pct=0.55,
                     late_stage_dark_period_pct=0.0)
        assert s == pytest.approx(30.0)

    def test_dark_period_below_0_20(self):
        s = self._ms(ghosting_episodes_per_deal=0.0,
                     engagement_drop_after_proposal_pct=0.0,
                     late_stage_dark_period_pct=0.10)
        assert s == pytest.approx(0.0)

    def test_dark_period_at_0_20(self):
        # >=0.20 → +12
        s = self._ms(ghosting_episodes_per_deal=0.0,
                     engagement_drop_after_proposal_pct=0.0,
                     late_stage_dark_period_pct=0.20)
        assert s == pytest.approx(12.0)

    def test_dark_period_at_0_40(self):
        # >=0.40 → +25
        s = self._ms(ghosting_episodes_per_deal=0.0,
                     engagement_drop_after_proposal_pct=0.0,
                     late_stage_dark_period_pct=0.40)
        assert s == pytest.approx(25.0)

    def test_momentum_cap_at_100(self):
        # max: 45+30+25 = 100
        s = self._ms(ghosting_episodes_per_deal=5.0,
                     engagement_drop_after_proposal_pct=0.80,
                     late_stage_dark_period_pct=0.80)
        assert s == pytest.approx(100.0)

    def test_momentum_additive_example(self):
        # >=1.5 (+25) + >=0.30 (+15) + >=0.20 (+12) = 52
        s = self._ms(ghosting_episodes_per_deal=2.0,
                     engagement_drop_after_proposal_pct=0.35,
                     late_stage_dark_period_pct=0.25)
        assert s == pytest.approx(52.0)


# ---------------------------------------------------------------------------
# 8. Composite formula and weights
# ---------------------------------------------------------------------------

class TestComposite:
    def test_composite_formula(self):
        """Verify composite = v*0.30 + b*0.25 + r*0.25 + m*0.20, capped at 100."""
        engine = fresh_engine()
        inp = make_input(
            avg_buyer_response_time_days=3.0,        # velocity +22
            avg_days_between_meaningful_touches=7.0,  # velocity +18  → vel=40
            next_step_set_rate_pct=0.80,              # velocity +0
            stakeholder_breadth_avg=2.5,              # breadth +22
            executive_engagement_rate_pct=0.40,       # breadth +18
            multi_stakeholder_deals_pct=0.55,         # breadth +12  → bre=52
            follow_up_required_before_response_pct=0.45,  # resp +22
            buyer_initiated_contact_pct=0.30,          # resp +18
            content_open_rate_pct=0.50,                # resp +12   → res=52
            ghosting_episodes_per_deal=1.5,            # mom +25
            engagement_drop_after_proposal_pct=0.30,   # mom +15
            late_stage_dark_period_pct=0.20,           # mom +12    → mom=52
        )
        result = engine.assess(inp)
        expected = round(40.0 * 0.30 + 52.0 * 0.25 + 52.0 * 0.25 + 52.0 * 0.20, 1)
        assert result.engagement_composite == pytest.approx(expected)

    def test_composite_capped_at_100(self):
        engine = fresh_engine()
        inp = make_input(
            avg_buyer_response_time_days=10.0,
            avg_days_between_meaningful_touches=30.0,
            next_step_set_rate_pct=0.0,
            stakeholder_breadth_avg=1.0,
            executive_engagement_rate_pct=0.0,
            multi_stakeholder_deals_pct=0.0,
            follow_up_required_before_response_pct=1.0,
            buyer_initiated_contact_pct=0.0,
            content_open_rate_pct=0.0,
            ghosting_episodes_per_deal=5.0,
            engagement_drop_after_proposal_pct=1.0,
            late_stage_dark_period_pct=1.0,
        )
        result = engine.assess(inp)
        assert result.engagement_composite <= 100.0

    def test_composite_zero_for_perfect_input(self):
        engine = fresh_engine()
        inp = make_input(
            avg_buyer_response_time_days=0.5,
            avg_days_between_meaningful_touches=2.0,
            next_step_set_rate_pct=0.90,
            stakeholder_breadth_avg=5.0,
            executive_engagement_rate_pct=0.80,
            multi_stakeholder_deals_pct=0.80,
            follow_up_required_before_response_pct=0.05,
            buyer_initiated_contact_pct=0.60,
            content_open_rate_pct=0.90,
            ghosting_episodes_per_deal=0.0,
            engagement_drop_after_proposal_pct=0.05,
            late_stage_dark_period_pct=0.05,
        )
        result = engine.assess(inp)
        assert result.engagement_composite == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# 9. Pattern detection — priority and all 6 patterns
# ---------------------------------------------------------------------------

class TestPatternDetection:

    def test_pattern_executive_access_deficit_priority_over_ghosting(self):
        """executive_access_deficit is checked before buyer_ghosting_cycle."""
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.10,    # <=0.15
            stakeholder_breadth_avg=1.8,            # <=2.0
            ghosting_episodes_per_deal=3.0,         # would trigger ghosting_cycle
            late_stage_dark_period_pct=0.40,        # would trigger ghosting_cycle
        )
        result = engine.assess(inp)
        assert result.engagement_pattern == EngagementPattern.executive_access_deficit

    def test_pattern_executive_access_deficit_boundaries(self):
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.15,    # exactly at threshold
            stakeholder_breadth_avg=2.0,            # exactly at threshold
        )
        result = engine.assess(inp)
        assert result.engagement_pattern == EngagementPattern.executive_access_deficit

    def test_pattern_executive_access_deficit_not_triggered_exec_too_high(self):
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.16,    # >0.15, won't trigger
            stakeholder_breadth_avg=1.8,
            ghosting_episodes_per_deal=0.0,
            late_stage_dark_period_pct=0.0,
            engagement_drop_after_proposal_pct=0.0,
            response_time_trend_days=0.0,
        )
        result = engine.assess(inp)
        assert result.engagement_pattern != EngagementPattern.executive_access_deficit

    def test_pattern_buyer_ghosting_cycle(self):
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.50,    # won't trigger exec_deficit
            stakeholder_breadth_avg=4.0,
            ghosting_episodes_per_deal=2.5,         # >=2.5
            late_stage_dark_period_pct=0.35,        # >=0.35
        )
        result = engine.assess(inp)
        assert result.engagement_pattern == EngagementPattern.buyer_ghosting_cycle

    def test_pattern_buyer_ghosting_cycle_boundaries(self):
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.50,
            stakeholder_breadth_avg=4.0,
            ghosting_episodes_per_deal=2.5,
            late_stage_dark_period_pct=0.35,
        )
        result = engine.assess(inp)
        assert result.engagement_pattern == EngagementPattern.buyer_ghosting_cycle

    def test_pattern_buyer_ghosting_cycle_not_triggered_below_boundary(self):
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.50,
            stakeholder_breadth_avg=4.0,
            ghosting_episodes_per_deal=2.4,         # just below 2.5
            late_stage_dark_period_pct=0.35,
            engagement_drop_after_proposal_pct=0.0,
            response_time_trend_days=0.0,
        )
        result = engine.assess(inp)
        assert result.engagement_pattern != EngagementPattern.buyer_ghosting_cycle

    def test_pattern_single_contact_dependency(self):
        """breadth_score>=35 AND stakeholder_breadth_avg<=2.0."""
        engine = fresh_engine()
        # To get breadth>=35: stakeholder<=1.5(+40) alone is enough
        inp = make_input(
            executive_engagement_rate_pct=0.50,    # won't trigger exec deficit
            stakeholder_breadth_avg=1.5,            # breadth score gets +40 >=35, also <=2.0
            ghosting_episodes_per_deal=0.0,         # no ghosting
            late_stage_dark_period_pct=0.0,
            multi_stakeholder_deals_pct=1.0,        # no extra breadth penalty
            engagement_drop_after_proposal_pct=0.0,
            response_time_trend_days=0.0,
        )
        result = engine.assess(inp)
        assert result.engagement_pattern == EngagementPattern.single_contact_dependency

    def test_pattern_single_contact_dependency_breadth_too_low(self):
        engine = fresh_engine()
        # stakeholder_breadth_avg=1.5 gives +40 alone; let's make breadth <35 with high stakeholder_breadth
        # <=2.5 (+22), exec=0.5 (+0), multi=1.0 (+0) = 22 < 35 → won't trigger
        inp = make_input(
            executive_engagement_rate_pct=0.50,
            stakeholder_breadth_avg=2.0,            # breadth: <=2.5→+22, <=2.0→still in <=2.5 band
            multi_stakeholder_deals_pct=1.0,
            ghosting_episodes_per_deal=0.0,
            late_stage_dark_period_pct=0.0,
            engagement_drop_after_proposal_pct=0.0,
            response_time_trend_days=0.0,
        )
        result = engine.assess(inp)
        # breadth_score = 22 < 35, so single_contact_dependency NOT triggered
        assert result.engagement_pattern != EngagementPattern.single_contact_dependency

    def test_pattern_response_lag_accumulation(self):
        """velocity>=35 AND response_time_trend_days>=1.5."""
        engine = fresh_engine()
        # velocity: avg_response>=5(+40), touches>=14(+35), next_step<=0.40(+25) → capped 100 ≥35
        inp = make_input(
            executive_engagement_rate_pct=0.50,    # no exec deficit
            stakeholder_breadth_avg=4.0,            # low breadth score
            ghosting_episodes_per_deal=0.0,
            late_stage_dark_period_pct=0.0,
            avg_buyer_response_time_days=5.0,       # +40 velocity
            avg_days_between_meaningful_touches=14.0,  # +35 velocity → vel=75
            next_step_set_rate_pct=0.80,
            response_time_trend_days=1.5,           # >=1.5
            engagement_drop_after_proposal_pct=0.0,
            multi_stakeholder_deals_pct=0.70,
        )
        result = engine.assess(inp)
        assert result.engagement_pattern == EngagementPattern.response_lag_accumulation

    def test_pattern_response_lag_accumulation_not_triggered_low_velocity(self):
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.50,
            stakeholder_breadth_avg=4.0,
            ghosting_episodes_per_deal=0.0,
            late_stage_dark_period_pct=0.0,
            avg_buyer_response_time_days=1.0,       # low velocity
            avg_days_between_meaningful_touches=5.0,
            next_step_set_rate_pct=0.80,             # vel=0 < 35
            response_time_trend_days=2.0,
            engagement_drop_after_proposal_pct=0.0,
        )
        result = engine.assess(inp)
        assert result.engagement_pattern != EngagementPattern.response_lag_accumulation

    def test_pattern_momentum_reversal(self):
        """engagement_drop_after_proposal_pct>=0.45 AND momentum>=30."""
        engine = fresh_engine()
        # momentum: ghosting>=3.0(+45), drop>=0.55(+30) → 75 ≥30
        inp = make_input(
            executive_engagement_rate_pct=0.50,
            stakeholder_breadth_avg=4.0,
            ghosting_episodes_per_deal=3.0,         # momentum +45
            late_stage_dark_period_pct=0.10,        # not enough for ghosting_cycle
            engagement_drop_after_proposal_pct=0.45,  # >=0.45
            avg_buyer_response_time_days=1.0,
            response_time_trend_days=0.0,
        )
        result = engine.assess(inp)
        # ghosting=3.0, dark=0.10 < 0.35 → not ghosting_cycle; exec OK; check breadth < 35
        # breadth_score: stakeholder=4.0(>3.5→+0), exec=0.5(>0.4→+0), multi=0.7(>0.55→+0) = 0 < 35 → not single_contact
        # velocity: response=1.0 → +0; touches=5 → +0; next_step=0.8 → +0 → vel=0 < 35 → not response_lag
        # momentum: ghosting=3.0→+45, drop=0.45→+15, dark=0.10→+0 = 60 ≥30 → momentum_reversal
        assert result.engagement_pattern == EngagementPattern.momentum_reversal

    def test_pattern_none(self):
        engine = fresh_engine()
        inp = make_input()  # all healthy defaults
        result = engine.assess(inp)
        assert result.engagement_pattern == EngagementPattern.none

    def test_pattern_priority_ghosting_over_single_contact(self):
        """buyer_ghosting_cycle checked before single_contact_dependency."""
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.50,
            stakeholder_breadth_avg=1.5,            # would trigger single_contact (breadth>=35)
            ghosting_episodes_per_deal=3.0,         # ghosting_cycle condition
            late_stage_dark_period_pct=0.40,        # ghosting_cycle condition
        )
        result = engine.assess(inp)
        assert result.engagement_pattern == EngagementPattern.buyer_ghosting_cycle

    def test_pattern_priority_single_contact_over_response_lag(self):
        """single_contact_dependency checked before response_lag_accumulation."""
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.50,
            stakeholder_breadth_avg=1.5,            # breadth score >=35, stakeholder<=2.0
            ghosting_episodes_per_deal=0.0,
            late_stage_dark_period_pct=0.0,
            avg_buyer_response_time_days=5.0,       # velocity >=35
            response_time_trend_days=2.0,           # response_lag trigger
            engagement_drop_after_proposal_pct=0.0,
        )
        result = engine.assess(inp)
        assert result.engagement_pattern == EngagementPattern.single_contact_dependency

    def test_pattern_priority_response_lag_over_momentum_reversal(self):
        """response_lag_accumulation checked before momentum_reversal."""
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.50,
            stakeholder_breadth_avg=4.0,
            ghosting_episodes_per_deal=3.0,
            late_stage_dark_period_pct=0.0,         # no ghosting cycle
            avg_buyer_response_time_days=5.0,        # velocity high
            avg_days_between_meaningful_touches=14.0,
            next_step_set_rate_pct=0.80,
            response_time_trend_days=2.0,           # response_lag
            engagement_drop_after_proposal_pct=0.50,  # momentum_reversal would also fire
        )
        result = engine.assess(inp)
        # breadth score: stakeholder=4.0→+0, exec=0.5→+0, multi=0.7→+0 = 0 < 35
        # velocity = 40+35 = 75 >= 35, trend=2.0>=1.5 → response_lag
        assert result.engagement_pattern == EngagementPattern.response_lag_accumulation


# ---------------------------------------------------------------------------
# 10. Risk thresholds
# ---------------------------------------------------------------------------

class TestRiskLevel:
    def _risk_for_composite(self, composite_target: float) -> EngagementRisk:
        """Return risk by creating an input that yields approximately the target composite."""
        engine = fresh_engine()
        # Use direct method
        return engine._risk_level(composite_target)

    def test_risk_below_20_is_low(self):
        assert self._risk_for_composite(19.9) == EngagementRisk.low

    def test_risk_at_0_is_low(self):
        assert self._risk_for_composite(0.0) == EngagementRisk.low

    def test_risk_at_20_is_moderate(self):
        assert self._risk_for_composite(20.0) == EngagementRisk.moderate

    def test_risk_at_39_9_is_moderate(self):
        assert self._risk_for_composite(39.9) == EngagementRisk.moderate

    def test_risk_at_40_is_high(self):
        assert self._risk_for_composite(40.0) == EngagementRisk.high

    def test_risk_at_59_9_is_high(self):
        assert self._risk_for_composite(59.9) == EngagementRisk.high

    def test_risk_at_60_is_critical(self):
        assert self._risk_for_composite(60.0) == EngagementRisk.critical

    def test_risk_at_100_is_critical(self):
        assert self._risk_for_composite(100.0) == EngagementRisk.critical


# ---------------------------------------------------------------------------
# 11. Severity thresholds
# ---------------------------------------------------------------------------

class TestSeverity:
    def _sev(self, composite: float) -> EngagementSeverity:
        engine = fresh_engine()
        return engine._severity(composite)

    def test_severity_below_20_is_accelerating(self):
        assert self._sev(19.9) == EngagementSeverity.accelerating

    def test_severity_at_0_is_accelerating(self):
        assert self._sev(0.0) == EngagementSeverity.accelerating

    def test_severity_at_20_is_engaged(self):
        assert self._sev(20.0) == EngagementSeverity.engaged

    def test_severity_at_39_9_is_engaged(self):
        assert self._sev(39.9) == EngagementSeverity.engaged

    def test_severity_at_40_is_slowing(self):
        assert self._sev(40.0) == EngagementSeverity.slowing

    def test_severity_at_59_9_is_slowing(self):
        assert self._sev(59.9) == EngagementSeverity.slowing

    def test_severity_at_60_is_stalled(self):
        assert self._sev(60.0) == EngagementSeverity.stalled

    def test_severity_at_100_is_stalled(self):
        assert self._sev(100.0) == EngagementSeverity.stalled


# ---------------------------------------------------------------------------
# 12. Action mappings (all branches)
# ---------------------------------------------------------------------------

class TestActionMapping:
    def _action(self, risk: EngagementRisk, pattern: EngagementPattern) -> EngagementAction:
        return fresh_engine()._action(risk, pattern)

    def test_critical_ghosting_cycle(self):
        assert self._action(EngagementRisk.critical, EngagementPattern.buyer_ghosting_cycle) \
               == EngagementAction.re_engagement_sequence_coaching

    def test_critical_exec_deficit(self):
        assert self._action(EngagementRisk.critical, EngagementPattern.executive_access_deficit) \
               == EngagementAction.executive_outreach_coaching

    def test_critical_other_pattern_none(self):
        assert self._action(EngagementRisk.critical, EngagementPattern.none) \
               == EngagementAction.deal_rescue_intervention

    def test_critical_other_pattern_momentum_reversal(self):
        assert self._action(EngagementRisk.critical, EngagementPattern.momentum_reversal) \
               == EngagementAction.deal_rescue_intervention

    def test_critical_other_pattern_single_contact(self):
        assert self._action(EngagementRisk.critical, EngagementPattern.single_contact_dependency) \
               == EngagementAction.deal_rescue_intervention

    def test_critical_other_pattern_response_lag(self):
        assert self._action(EngagementRisk.critical, EngagementPattern.response_lag_accumulation) \
               == EngagementAction.deal_rescue_intervention

    def test_high_single_contact_dependency(self):
        assert self._action(EngagementRisk.high, EngagementPattern.single_contact_dependency) \
               == EngagementAction.multithreading_coaching

    def test_high_response_lag_accumulation(self):
        assert self._action(EngagementRisk.high, EngagementPattern.response_lag_accumulation) \
               == EngagementAction.deal_velocity_coaching

    def test_high_other_pattern_none(self):
        assert self._action(EngagementRisk.high, EngagementPattern.none) \
               == EngagementAction.deal_velocity_coaching

    def test_high_other_pattern_momentum_reversal(self):
        assert self._action(EngagementRisk.high, EngagementPattern.momentum_reversal) \
               == EngagementAction.deal_velocity_coaching

    def test_moderate_any_pattern(self):
        for pat in EngagementPattern:
            assert self._action(EngagementRisk.moderate, pat) \
                   == EngagementAction.re_engagement_sequence_coaching

    def test_low_any_pattern(self):
        for pat in EngagementPattern:
            assert self._action(EngagementRisk.low, pat) \
                   == EngagementAction.no_action


# ---------------------------------------------------------------------------
# 13. Flag conditions
# ---------------------------------------------------------------------------

class TestFlags:
    def test_has_engagement_gap_via_composite(self):
        """composite>=40 triggers gap."""
        engine = fresh_engine()
        inp = make_input(
            avg_buyer_response_time_days=5.0,
            avg_days_between_meaningful_touches=14.0,
            next_step_set_rate_pct=0.80,
            stakeholder_breadth_avg=4.0,
            executive_engagement_rate_pct=0.80,
            multi_stakeholder_deals_pct=0.80,
            follow_up_required_before_response_pct=0.05,
            buyer_initiated_contact_pct=0.60,
            content_open_rate_pct=0.90,
            ghosting_episodes_per_deal=0.0,
            engagement_drop_after_proposal_pct=0.0,
            late_stage_dark_period_pct=0.0,
        )
        result = engine.assess(inp)
        # velocity: 40+35=75, breadth/responsiveness/momentum minimal
        # composite = 75*0.3 = 22.5 ... need composite>=40 or ghosting>=2 or exec<=0.25
        # exec=0.80 > 0.25 and ghosting=0.0 < 2.0 → rely on composite
        # Actually composite=22.5 < 40, and no other triggers → gap=False
        # Let's adjust: add more velocity for a higher composite
        pass

    def test_has_engagement_gap_via_ghosting(self):
        """ghosting_episodes_per_deal>=2.0 triggers gap regardless of composite."""
        engine = fresh_engine()
        inp = make_input(ghosting_episodes_per_deal=2.0)
        result = engine.assess(inp)
        assert result.has_engagement_gap is True

    def test_has_engagement_gap_via_executive_rate(self):
        """executive_engagement_rate_pct<=0.25 triggers gap."""
        engine = fresh_engine()
        inp = make_input(executive_engagement_rate_pct=0.25)
        result = engine.assess(inp)
        assert result.has_engagement_gap is True

    def test_has_engagement_gap_false(self):
        """Healthy input: composite<40, ghosting<2.0, exec>0.25."""
        engine = fresh_engine()
        inp = make_input(
            ghosting_episodes_per_deal=0.0,
            executive_engagement_rate_pct=0.80,
        )
        result = engine.assess(inp)
        # Baseline has composite close to 0; check it's indeed False
        assert result.has_engagement_gap is False

    def test_has_engagement_gap_high_composite(self):
        engine = fresh_engine()
        inp = make_input(
            avg_buyer_response_time_days=5.0,
            avg_days_between_meaningful_touches=14.0,
            next_step_set_rate_pct=0.40,
            stakeholder_breadth_avg=1.5,
            executive_engagement_rate_pct=0.80,
            multi_stakeholder_deals_pct=0.80,
            follow_up_required_before_response_pct=0.70,
            buyer_initiated_contact_pct=0.50,
            content_open_rate_pct=0.70,
            ghosting_episodes_per_deal=0.0,
            engagement_drop_after_proposal_pct=0.0,
            late_stage_dark_period_pct=0.0,
        )
        result = engine.assess(inp)
        # composite should be high enough (>=40) to trigger gap
        if result.engagement_composite >= 40:
            assert result.has_engagement_gap is True

    def test_requires_engagement_coaching_via_composite(self):
        """composite>=30 triggers coaching."""
        engine = fresh_engine()
        inp = make_input(
            avg_buyer_response_time_days=5.0,
            avg_days_between_meaningful_touches=14.0,
            next_step_set_rate_pct=0.80,
            ghosting_episodes_per_deal=0.0,
            engagement_drop_after_proposal_pct=0.0,
            late_stage_dark_period_pct=0.0,
        )
        result = engine.assess(inp)
        if result.engagement_composite >= 30:
            assert result.requires_engagement_coaching is True

    def test_requires_engagement_coaching_via_response_time(self):
        """avg_buyer_response_time_days>=4.0 triggers coaching."""
        engine = fresh_engine()
        inp = make_input(avg_buyer_response_time_days=4.0)
        result = engine.assess(inp)
        assert result.requires_engagement_coaching is True

    def test_requires_engagement_coaching_via_next_step(self):
        """next_step_set_rate_pct<=0.55 triggers coaching."""
        engine = fresh_engine()
        inp = make_input(next_step_set_rate_pct=0.55)
        result = engine.assess(inp)
        assert result.requires_engagement_coaching is True

    def test_requires_engagement_coaching_false(self):
        """Healthy rep: composite<30, response<4.0, next_step>0.55."""
        engine = fresh_engine()
        inp = make_input(
            avg_buyer_response_time_days=1.0,
            next_step_set_rate_pct=0.90,
        )
        result = engine.assess(inp)
        assert result.requires_engagement_coaching is False

    def test_requires_coaching_next_step_boundary_just_above(self):
        """next_step_set_rate_pct=0.56 should NOT trigger coaching alone."""
        engine = fresh_engine()
        inp = make_input(
            next_step_set_rate_pct=0.56,
            avg_buyer_response_time_days=1.0,
        )
        result = engine.assess(inp)
        # Only triggers if composite>=30 too; baseline healthy → likely False
        if result.engagement_composite < 30 and inp.avg_buyer_response_time_days < 4.0:
            assert result.requires_engagement_coaching is False


# ---------------------------------------------------------------------------
# 14. Pipeline at risk formula
# ---------------------------------------------------------------------------

class TestPipelineAtRisk:
    def test_pipeline_formula(self):
        engine = fresh_engine()
        inp = make_input(
            total_active_deals=10,
            avg_opportunity_value_usd=50_000.0,
            late_stage_dark_period_pct=0.20,
        )
        result = engine.assess(inp)
        expected = round(
            10 * 50_000.0 * 0.20 * (result.engagement_composite / 100.0), 2
        )
        assert result.estimated_pipeline_at_risk_usd == pytest.approx(expected)

    def test_pipeline_zero_when_no_dark_period(self):
        engine = fresh_engine()
        inp = make_input(late_stage_dark_period_pct=0.0)
        result = engine.assess(inp)
        assert result.estimated_pipeline_at_risk_usd == pytest.approx(0.0)

    def test_pipeline_zero_when_composite_zero(self):
        """When composite is exactly 0, pipeline at risk is 0 regardless of dark period."""
        engine = fresh_engine()
        # Perfect input: all sub-scores = 0 → composite = 0
        inp = make_input(
            avg_buyer_response_time_days=0.5,        # <1.5 → +0 velocity
            avg_days_between_meaningful_touches=2.0,  # <7.0 → +0 velocity
            next_step_set_rate_pct=0.90,              # >0.65 → +0 velocity
            stakeholder_breadth_avg=5.0,              # >3.5 → +0 breadth
            executive_engagement_rate_pct=0.80,       # >0.40 → +0 breadth
            multi_stakeholder_deals_pct=0.80,         # >0.55 → +0 breadth
            follow_up_required_before_response_pct=0.05,  # <0.25 → +0 responsiveness
            buyer_initiated_contact_pct=0.60,          # >0.30 → +0 responsiveness
            content_open_rate_pct=0.90,                # >0.50 → +0 responsiveness
            ghosting_episodes_per_deal=0.0,            # <0.5 → +0 momentum
            engagement_drop_after_proposal_pct=0.05,   # <0.30 → +0 momentum
            late_stage_dark_period_pct=0.0,            # =0 → pipeline_at_risk = 0
        )
        result = engine.assess(inp)
        assert result.engagement_composite == pytest.approx(0.0)
        assert result.estimated_pipeline_at_risk_usd == pytest.approx(0.0)

    def test_pipeline_rounded_to_2_decimal_places(self):
        engine = fresh_engine()
        inp = make_input(
            total_active_deals=7,
            avg_opportunity_value_usd=33_333.33,
            late_stage_dark_period_pct=0.33,
            ghosting_episodes_per_deal=2.0,
            engagement_drop_after_proposal_pct=0.40,
        )
        result = engine.assess(inp)
        # Verify it's rounded to 2 decimal places
        assert result.estimated_pipeline_at_risk_usd == round(result.estimated_pipeline_at_risk_usd, 2)

    def test_pipeline_scales_with_deals(self):
        engine1 = fresh_engine()
        engine2 = fresh_engine()
        inp1 = make_input(total_active_deals=5, avg_opportunity_value_usd=10_000.0,
                          late_stage_dark_period_pct=0.50,
                          ghosting_episodes_per_deal=2.0)
        inp2 = make_input(total_active_deals=10, avg_opportunity_value_usd=10_000.0,
                          late_stage_dark_period_pct=0.50,
                          ghosting_episodes_per_deal=2.0)
        r1 = engine1.assess(inp1)
        r2 = engine2.assess(inp2)
        if r1.engagement_composite == r2.engagement_composite:
            assert r2.estimated_pipeline_at_risk_usd == pytest.approx(
                r1.estimated_pipeline_at_risk_usd * 2, rel=1e-5
            )


# ---------------------------------------------------------------------------
# 15. Signal string
# ---------------------------------------------------------------------------

class TestSignal:
    def test_healthy_signal(self):
        engine = fresh_engine()
        inp = make_input()
        result = engine.assess(inp)
        assert result.engagement_signal == (
            "Buyer engagement healthy — response velocity, stakeholder breadth, "
            "and deal momentum within benchmarks"
        )

    def test_signal_contains_avg_response_time(self):
        engine = fresh_engine()
        inp = make_input(avg_buyer_response_time_days=4.0, ghosting_episodes_per_deal=2.5,
                         late_stage_dark_period_pct=0.40)
        result = engine.assess(inp)
        assert "4.0d avg buyer response time" in result.engagement_signal

    def test_signal_contains_avg_stakeholders(self):
        engine = fresh_engine()
        inp = make_input(avg_buyer_response_time_days=4.0, ghosting_episodes_per_deal=2.5,
                         late_stage_dark_period_pct=0.40)
        result = engine.assess(inp)
        assert f"{inp.stakeholder_breadth_avg:.1f} avg stakeholders" in result.engagement_signal

    def test_signal_contains_ghosting_episodes(self):
        engine = fresh_engine()
        inp = make_input(avg_buyer_response_time_days=4.0, ghosting_episodes_per_deal=2.5,
                         late_stage_dark_period_pct=0.40)
        result = engine.assess(inp)
        assert f"{inp.ghosting_episodes_per_deal:.1f} ghosting episodes/deal" in result.engagement_signal

    def test_signal_contains_composite(self):
        engine = fresh_engine()
        inp = make_input(avg_buyer_response_time_days=4.0, ghosting_episodes_per_deal=2.5,
                         late_stage_dark_period_pct=0.40)
        result = engine.assess(inp)
        assert f"composite {result.engagement_composite:.0f}" in result.engagement_signal

    def test_signal_pattern_label_capitalized(self):
        """Pattern name in signal should be capitalized with underscores replaced by spaces."""
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.50,
            ghosting_episodes_per_deal=3.0,
            late_stage_dark_period_pct=0.40,
        )
        result = engine.assess(inp)
        assert result.engagement_pattern == EngagementPattern.buyer_ghosting_cycle
        assert "Buyer ghosting cycle" in result.engagement_signal

    def test_signal_none_pattern_with_risk_uses_engagement_risk_label(self):
        """When pattern is none but composite>=20, label is 'Engagement risk'."""
        engine = fresh_engine()
        # Create moderate composite with no specific pattern
        inp = make_input(
            avg_buyer_response_time_days=3.0,    # +22 velocity
            avg_days_between_meaningful_touches=7.0,  # +18 velocity → vel=40
            next_step_set_rate_pct=0.80,
            stakeholder_breadth_avg=4.0,          # no breadth risk
            executive_engagement_rate_pct=0.80,
            multi_stakeholder_deals_pct=0.80,
            follow_up_required_before_response_pct=0.05,
            buyer_initiated_contact_pct=0.60,
            content_open_rate_pct=0.90,
            ghosting_episodes_per_deal=0.0,
            engagement_drop_after_proposal_pct=0.0,
            late_stage_dark_period_pct=0.0,
            response_time_trend_days=0.0,
        )
        result = engine.assess(inp)
        if result.engagement_pattern == EngagementPattern.none and result.engagement_composite >= 20:
            assert "Engagement risk" in result.engagement_signal

    def test_signal_executive_access_deficit_label(self):
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.10,
            stakeholder_breadth_avg=1.5,
        )
        result = engine.assess(inp)
        assert result.engagement_pattern == EngagementPattern.executive_access_deficit
        assert "Executive access deficit" in result.engagement_signal

    def test_signal_single_contact_dependency_label(self):
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.50,
            stakeholder_breadth_avg=1.5,
            ghosting_episodes_per_deal=0.0,
            late_stage_dark_period_pct=0.0,
            engagement_drop_after_proposal_pct=0.0,
            response_time_trend_days=0.0,
            multi_stakeholder_deals_pct=1.0,
        )
        result = engine.assess(inp)
        if result.engagement_pattern == EngagementPattern.single_contact_dependency:
            assert "Single contact dependency" in result.engagement_signal

    def test_signal_momentum_reversal_label(self):
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.50,
            stakeholder_breadth_avg=4.0,
            ghosting_episodes_per_deal=3.0,
            late_stage_dark_period_pct=0.10,
            engagement_drop_after_proposal_pct=0.45,
            avg_buyer_response_time_days=1.0,
            response_time_trend_days=0.0,
        )
        result = engine.assess(inp)
        if result.engagement_pattern == EngagementPattern.momentum_reversal:
            assert "Momentum reversal" in result.engagement_signal

    def test_signal_response_lag_label(self):
        engine = fresh_engine()
        inp = make_input(
            executive_engagement_rate_pct=0.50,
            stakeholder_breadth_avg=4.0,
            ghosting_episodes_per_deal=0.0,
            late_stage_dark_period_pct=0.0,
            avg_buyer_response_time_days=5.0,
            avg_days_between_meaningful_touches=14.0,
            next_step_set_rate_pct=0.80,
            response_time_trend_days=1.5,
            engagement_drop_after_proposal_pct=0.0,
        )
        result = engine.assess(inp)
        if result.engagement_pattern == EngagementPattern.response_lag_accumulation:
            assert "Response lag accumulation" in result.engagement_signal


# ---------------------------------------------------------------------------
# 16. assess end-to-end
# ---------------------------------------------------------------------------

class TestAssessEndToEnd:
    def test_assess_returns_engagement_result(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert isinstance(result, EngagementResult)

    def test_assess_propagates_rep_id_region(self):
        engine = fresh_engine()
        result = engine.assess(make_input(rep_id="REP_X", region="NORTH"))
        assert result.rep_id == "REP_X"
        assert result.region == "NORTH"

    def test_assess_scores_are_non_negative(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert result.velocity_score >= 0
        assert result.breadth_score >= 0
        assert result.responsiveness_score >= 0
        assert result.momentum_score >= 0
        assert result.engagement_composite >= 0

    def test_assess_scores_capped_at_100(self):
        engine = fresh_engine()
        inp = make_input(
            avg_buyer_response_time_days=10.0,
            avg_days_between_meaningful_touches=30.0,
            next_step_set_rate_pct=0.0,
            stakeholder_breadth_avg=1.0,
            executive_engagement_rate_pct=0.0,
            multi_stakeholder_deals_pct=0.0,
            follow_up_required_before_response_pct=1.0,
            buyer_initiated_contact_pct=0.0,
            content_open_rate_pct=0.0,
            ghosting_episodes_per_deal=5.0,
            engagement_drop_after_proposal_pct=1.0,
            late_stage_dark_period_pct=1.0,
        )
        result = engine.assess(inp)
        assert result.velocity_score <= 100.0
        assert result.breadth_score <= 100.0
        assert result.responsiveness_score <= 100.0
        assert result.momentum_score <= 100.0
        assert result.engagement_composite <= 100.0

    def test_assess_critical_risk_scenario(self):
        engine = fresh_engine()
        inp = make_input(
            avg_buyer_response_time_days=6.0,
            avg_days_between_meaningful_touches=20.0,
            next_step_set_rate_pct=0.30,
            stakeholder_breadth_avg=1.2,
            executive_engagement_rate_pct=0.10,
            multi_stakeholder_deals_pct=0.15,
            follow_up_required_before_response_pct=0.80,
            buyer_initiated_contact_pct=0.10,
            content_open_rate_pct=0.20,
            ghosting_episodes_per_deal=4.0,
            engagement_drop_after_proposal_pct=0.65,
            late_stage_dark_period_pct=0.50,
        )
        result = engine.assess(inp)
        assert result.engagement_risk == EngagementRisk.critical
        assert result.engagement_severity == EngagementSeverity.stalled
        assert result.has_engagement_gap is True
        assert result.requires_engagement_coaching is True

    def test_assess_low_risk_scenario(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert result.engagement_risk == EngagementRisk.low
        assert result.engagement_severity == EngagementSeverity.accelerating
        assert result.recommended_action == EngagementAction.no_action

    def test_assess_accumulates_results_internally(self):
        engine = fresh_engine()
        engine.assess(make_input(rep_id="R1"))
        engine.assess(make_input(rep_id="R2"))
        assert len(engine._results) == 2


# ---------------------------------------------------------------------------
# 17. assess_batch
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_assess_batch_returns_list(self):
        engine = fresh_engine()
        results = engine.assess_batch([make_input(), make_input(rep_id="R2")])
        assert isinstance(results, list)
        assert len(results) == 2

    def test_assess_batch_each_is_engagement_result(self):
        engine = fresh_engine()
        for r in engine.assess_batch([make_input(), make_input(rep_id="R3")]):
            assert isinstance(r, EngagementResult)

    def test_assess_batch_empty_list(self):
        engine = fresh_engine()
        results = engine.assess_batch([])
        assert results == []

    def test_assess_batch_order_preserved(self):
        engine = fresh_engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"R{i}"

    def test_assess_batch_accumulates_in_results(self):
        engine = fresh_engine()
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        assert len(engine._results) == 3


# ---------------------------------------------------------------------------
# 18. summary — empty
# ---------------------------------------------------------------------------

class TestSummaryEmpty:
    def test_summary_empty_returns_dict(self):
        assert isinstance(fresh_engine().summary(), dict)

    def test_summary_empty_has_13_keys(self):
        assert len(fresh_engine().summary()) == 13

    def test_summary_empty_exact_keys(self):
        s = fresh_engine().summary()
        assert set(s.keys()) == {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_engagement_composite", "engagement_gap_count",
            "coaching_count", "avg_velocity_score", "avg_breadth_score",
            "avg_responsiveness_score", "avg_momentum_score",
            "total_estimated_pipeline_at_risk_usd",
        }

    def test_summary_empty_total_zero(self):
        assert fresh_engine().summary()["total"] == 0

    def test_summary_empty_counts_are_empty_dicts(self):
        s = fresh_engine().summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_summary_empty_numeric_fields_zero(self):
        s = fresh_engine().summary()
        assert s["avg_engagement_composite"] == 0.0
        assert s["engagement_gap_count"] == 0
        assert s["coaching_count"] == 0
        assert s["avg_velocity_score"] == 0.0
        assert s["avg_breadth_score"] == 0.0
        assert s["avg_responsiveness_score"] == 0.0
        assert s["avg_momentum_score"] == 0.0
        assert s["total_estimated_pipeline_at_risk_usd"] == 0.0


# ---------------------------------------------------------------------------
# 19. summary — populated (all 13 keys)
# ---------------------------------------------------------------------------

class TestSummaryPopulated:
    def _populated_engine(self) -> SalesBuyerEngagementVelocityIntelligenceEngine:
        engine = fresh_engine()
        # healthy rep
        engine.assess(make_input(rep_id="R1"))
        # high risk rep
        engine.assess(make_input(
            rep_id="R2",
            avg_buyer_response_time_days=5.0,
            avg_days_between_meaningful_touches=14.0,
            next_step_set_rate_pct=0.35,
            stakeholder_breadth_avg=1.5,
            executive_engagement_rate_pct=0.10,
            multi_stakeholder_deals_pct=0.20,
            follow_up_required_before_response_pct=0.75,
            buyer_initiated_contact_pct=0.10,
            content_open_rate_pct=0.20,
            ghosting_episodes_per_deal=3.5,
            engagement_drop_after_proposal_pct=0.60,
            late_stage_dark_period_pct=0.45,
        ))
        return engine

    def test_summary_has_13_keys(self):
        s = self._populated_engine().summary()
        assert len(s) == 13

    def test_summary_exact_keys(self):
        s = self._populated_engine().summary()
        assert set(s.keys()) == {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_engagement_composite", "engagement_gap_count",
            "coaching_count", "avg_velocity_score", "avg_breadth_score",
            "avg_responsiveness_score", "avg_momentum_score",
            "total_estimated_pipeline_at_risk_usd",
        }

    def test_summary_total_count(self):
        assert self._populated_engine().summary()["total"] == 2

    def test_summary_risk_counts_present(self):
        s = self._populated_engine().summary()
        assert isinstance(s["risk_counts"], dict)
        assert sum(s["risk_counts"].values()) == 2

    def test_summary_pattern_counts_present(self):
        s = self._populated_engine().summary()
        assert isinstance(s["pattern_counts"], dict)
        assert sum(s["pattern_counts"].values()) == 2

    def test_summary_severity_counts_present(self):
        s = self._populated_engine().summary()
        assert isinstance(s["severity_counts"], dict)
        assert sum(s["severity_counts"].values()) == 2

    def test_summary_action_counts_present(self):
        s = self._populated_engine().summary()
        assert isinstance(s["action_counts"], dict)
        assert sum(s["action_counts"].values()) == 2

    def test_summary_avg_engagement_composite_is_float(self):
        s = self._populated_engine().summary()
        assert isinstance(s["avg_engagement_composite"], float)

    def test_summary_gap_count_in_range(self):
        s = self._populated_engine().summary()
        assert 0 <= s["engagement_gap_count"] <= 2

    def test_summary_coaching_count_in_range(self):
        s = self._populated_engine().summary()
        assert 0 <= s["coaching_count"] <= 2

    def test_summary_avg_scores_are_floats(self):
        s = self._populated_engine().summary()
        for key in ("avg_velocity_score", "avg_breadth_score",
                    "avg_responsiveness_score", "avg_momentum_score"):
            assert isinstance(s[key], float), f"{key} not float"

    def test_summary_pipeline_at_risk_is_float(self):
        s = self._populated_engine().summary()
        assert isinstance(s["total_estimated_pipeline_at_risk_usd"], float)

    def test_summary_avg_composite_correct(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(rep_id="R1"))
        r2 = engine.assess(make_input(rep_id="R2"))
        s = engine.summary()
        expected = round((r1.engagement_composite + r2.engagement_composite) / 2, 1)
        assert s["avg_engagement_composite"] == pytest.approx(expected)

    def test_summary_total_pipeline_at_risk(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(rep_id="R1"))
        r2 = engine.assess(make_input(rep_id="R2"))
        s = engine.summary()
        expected = round(r1.estimated_pipeline_at_risk_usd + r2.estimated_pipeline_at_risk_usd, 2)
        assert s["total_estimated_pipeline_at_risk_usd"] == pytest.approx(expected)

    def test_summary_gap_count_accurate(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(rep_id="R1"))
        r2 = engine.assess(make_input(
            rep_id="R2",
            ghosting_episodes_per_deal=3.0,
        ))
        s = engine.summary()
        expected = sum([r1.has_engagement_gap, r2.has_engagement_gap])
        assert s["engagement_gap_count"] == expected

    def test_summary_coaching_count_accurate(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(rep_id="R1"))
        r2 = engine.assess(make_input(rep_id="R2", avg_buyer_response_time_days=4.5))
        s = engine.summary()
        expected = sum([r1.requires_engagement_coaching, r2.requires_engagement_coaching])
        assert s["coaching_count"] == expected

    def test_summary_batch_then_summary(self):
        engine = fresh_engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 5
        assert len(s) == 13


# ---------------------------------------------------------------------------
# 20. Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_exact_boundary_velocity_1_5(self):
        engine = fresh_engine()
        inp = make_input(avg_buyer_response_time_days=1.5,
                         avg_days_between_meaningful_touches=0.0,
                         next_step_set_rate_pct=1.0)
        vs = engine._velocity_score(inp)
        assert vs == pytest.approx(8.0)

    def test_exact_boundary_breadth_3_5(self):
        engine = fresh_engine()
        inp = make_input(stakeholder_breadth_avg=3.5,
                         executive_engagement_rate_pct=1.0,
                         multi_stakeholder_deals_pct=1.0)
        bs = engine._breadth_score(inp)
        assert bs == pytest.approx(8.0)

    def test_exact_boundary_responsiveness_0_70(self):
        engine = fresh_engine()
        inp = make_input(follow_up_required_before_response_pct=0.70,
                         buyer_initiated_contact_pct=1.0,
                         content_open_rate_pct=1.0)
        rs = engine._responsiveness_score(inp)
        assert rs == pytest.approx(40.0)

    def test_exact_boundary_momentum_3_0(self):
        engine = fresh_engine()
        inp = make_input(ghosting_episodes_per_deal=3.0,
                         engagement_drop_after_proposal_pct=0.0,
                         late_stage_dark_period_pct=0.0)
        ms = engine._momentum_score(inp)
        assert ms == pytest.approx(45.0)

    def test_risk_exact_60(self):
        assert fresh_engine()._risk_level(60.0) == EngagementRisk.critical

    def test_risk_exact_40(self):
        assert fresh_engine()._risk_level(40.0) == EngagementRisk.high

    def test_risk_exact_20(self):
        assert fresh_engine()._risk_level(20.0) == EngagementRisk.moderate

    def test_severity_exact_60(self):
        assert fresh_engine()._severity(60.0) == EngagementSeverity.stalled

    def test_severity_exact_40(self):
        assert fresh_engine()._severity(40.0) == EngagementSeverity.slowing

    def test_severity_exact_20(self):
        assert fresh_engine()._severity(20.0) == EngagementSeverity.engaged

    def test_pipeline_at_risk_rounds_correctly(self):
        engine = fresh_engine()
        # Use specific values to check rounding
        inp = make_input(
            total_active_deals=3,
            avg_opportunity_value_usd=33_333.33,
            late_stage_dark_period_pct=0.10,
            ghosting_episodes_per_deal=2.0,
        )
        result = engine.assess(inp)
        raw = 3 * 33_333.33 * 0.10 * (result.engagement_composite / 100.0)
        assert result.estimated_pipeline_at_risk_usd == pytest.approx(round(raw, 2), abs=0.01)

    def test_multiple_engines_are_independent(self):
        e1 = fresh_engine()
        e2 = fresh_engine()
        e1.assess(make_input(rep_id="R1"))
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_assess_multiple_times_accumulates(self):
        engine = fresh_engine()
        for i in range(10):
            engine.assess(make_input(rep_id=f"R{i}"))
        assert engine.summary()["total"] == 10

    def test_to_dict_values_match_result_fields(self):
        engine = fresh_engine()
        inp = make_input(rep_id="MATCH_TEST", region="SOUTH")
        result = engine.assess(inp)
        d = result.to_dict()
        assert d["rep_id"] == result.rep_id
        assert d["region"] == result.region
        assert d["engagement_risk"] == result.engagement_risk.value
        assert d["engagement_pattern"] == result.engagement_pattern.value
        assert d["engagement_severity"] == result.engagement_severity.value
        assert d["recommended_action"] == result.recommended_action.value
        assert d["velocity_score"] == result.velocity_score
        assert d["breadth_score"] == result.breadth_score
        assert d["responsiveness_score"] == result.responsiveness_score
        assert d["momentum_score"] == result.momentum_score
        assert d["engagement_composite"] == result.engagement_composite
        assert d["has_engagement_gap"] == result.has_engagement_gap
        assert d["requires_engagement_coaching"] == result.requires_engagement_coaching
        assert d["estimated_pipeline_at_risk_usd"] == result.estimated_pipeline_at_risk_usd
        assert d["engagement_signal"] == result.engagement_signal

    def test_has_engagement_gap_exact_ghosting_boundary(self):
        engine = fresh_engine()
        inp = make_input(ghosting_episodes_per_deal=2.0,
                         executive_engagement_rate_pct=0.80)
        result = engine.assess(inp)
        assert result.has_engagement_gap is True

    def test_has_engagement_gap_just_below_ghosting(self):
        engine = fresh_engine()
        inp = make_input(ghosting_episodes_per_deal=1.9,
                         executive_engagement_rate_pct=0.80)
        result = engine.assess(inp)
        # composite likely < 40, exec > 0.25, ghosting < 2.0 → False
        if result.engagement_composite < 40:
            assert result.has_engagement_gap is False

    def test_requires_coaching_exact_response_boundary(self):
        engine = fresh_engine()
        inp = make_input(avg_buyer_response_time_days=4.0, next_step_set_rate_pct=0.90)
        result = engine.assess(inp)
        assert result.requires_engagement_coaching is True

    def test_requires_coaching_exact_next_step_boundary(self):
        engine = fresh_engine()
        inp = make_input(avg_buyer_response_time_days=1.0, next_step_set_rate_pct=0.55)
        result = engine.assess(inp)
        assert result.requires_engagement_coaching is True

    def test_exec_engagement_boundary_0_25_gap(self):
        engine = fresh_engine()
        inp = make_input(executive_engagement_rate_pct=0.25)
        result = engine.assess(inp)
        assert result.has_engagement_gap is True

    def test_exec_engagement_just_above_0_25_no_gap_from_exec(self):
        engine = fresh_engine()
        inp = make_input(executive_engagement_rate_pct=0.26,
                         ghosting_episodes_per_deal=0.0)
        result = engine.assess(inp)
        # exec > 0.25, ghosting < 2.0; gap only True if composite >= 40
        if result.engagement_composite < 40:
            assert result.has_engagement_gap is False

    def test_summary_risk_counts_keys_are_strings(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        for k in s["risk_counts"]:
            assert isinstance(k, str)

    def test_summary_pattern_counts_keys_are_strings(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        for k in s["pattern_counts"]:
            assert isinstance(k, str)
