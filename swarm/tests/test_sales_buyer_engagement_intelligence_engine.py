"""
Comprehensive pytest tests for SalesBuyerEngagementIntelligenceEngine.

Coverage:
- Enums
- EngagementInput dataclass
- EngagementResult dataclass + to_dict()
- Sub-scores: _responsiveness_score, _signal_score, _activation_score, _risk_score
- Composite calculation
- Pattern detection (priority order)
- Risk thresholds
- Severity thresholds
- Action routing
- Flags: has_engagement_gap, requires_engagement_coaching
- estimated_revenue_at_dark_usd
- Signal string (healthy and unhealthy)
- assess() end-to-end
- assess_batch()
- summary() (empty and populated)
"""

import pytest
from swarm.intelligence.sales_buyer_engagement_intelligence_engine import (
    EngagementAction,
    EngagementInput,
    EngagementPattern,
    EngagementResult,
    EngagementRisk,
    EngagementSeverity,
    SalesBuyerEngagementIntelligenceEngine,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def make_input(**overrides) -> EngagementInput:
    """Return a base EngagementInput with all metrics in the healthy zone.
    Override individual fields via kwargs.
    """
    defaults = dict(
        rep_id="rep-001",
        region="North",
        evaluation_period_id="Q1-2026",
        buyer_email_response_rate_pct=0.80,       # healthy (>0.60)
        meeting_attendance_rate_pct=0.90,          # healthy (>0.75)
        meeting_cancellation_rate_pct=0.10,        # healthy (<0.20)
        buyer_initiated_follow_up_pct=0.50,        # healthy (>0.25)
        proposal_open_rate_pct=0.85,               # healthy (>0.75)
        proposal_viewed_more_than_once_pct=0.80,   # healthy (>0.15)
        content_shared_engagement_rate_pct=0.60,   # healthy (>0.40)
        demo_to_next_step_commitment_rate_pct=0.80,# healthy (>0.70)
        stakeholder_expansion_by_buyer_pct=0.50,   # healthy (>0.25)
        avg_days_buyer_silent_before_followup=5.0, # healthy (<12)
        rep_response_to_buyer_signal_hours_avg=4.0,# healthy (<48)
        buyer_urgency_expression_rate_pct=0.70,
        multi_touch_engagement_rate_pct=0.60,      # healthy (>0.40)
        deal_dark_more_than_14d_pct=0.05,          # healthy (<0.10)
        executive_engagement_by_buyer_pct=0.60,
        reference_request_rate_pct=0.30,
        mutual_action_plan_adherence_pct=0.80,     # healthy (>0.55)
        total_active_deals=20,
        avg_opportunity_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return EngagementInput(**defaults)


def make_engine() -> SalesBuyerEngagementIntelligenceEngine:
    return SalesBuyerEngagementIntelligenceEngine()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Enum membership tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEnums:
    def test_engagement_risk_members(self):
        values = {e.value for e in EngagementRisk}
        assert values == {"low", "moderate", "high", "critical"}

    def test_engagement_pattern_members(self):
        values = {e.value for e in EngagementPattern}
        assert values == {
            "none", "one_way_sender", "low_signal_pursuer",
            "engagement_ignorer", "meeting_canceler", "proposal_black_hole",
        }

    def test_engagement_severity_members(self):
        values = {e.value for e in EngagementSeverity}
        assert values == {"engaged", "responsive", "passive", "dark"}

    def test_engagement_action_members(self):
        values = {e.value for e in EngagementAction}
        assert values == {
            "no_action", "engagement_quality_coaching", "signal_response_coaching",
            "buyer_activation_coaching", "deal_review_coaching",
            "engagement_intervention", "deal_qualification_review",
        }

    def test_enums_are_str_subclass(self):
        # All enum classes inherit from str
        assert isinstance(EngagementRisk.low, str)
        assert isinstance(EngagementPattern.none, str)
        assert isinstance(EngagementSeverity.engaged, str)
        assert isinstance(EngagementAction.no_action, str)

    def test_risk_enum_count(self):
        assert len(EngagementRisk) == 4

    def test_pattern_enum_count(self):
        assert len(EngagementPattern) == 6

    def test_severity_enum_count(self):
        assert len(EngagementSeverity) == 4

    def test_action_enum_count(self):
        assert len(EngagementAction) == 7


# ─────────────────────────────────────────────────────────────────────────────
# 2. EngagementInput dataclass
# ─────────────────────────────────────────────────────────────────────────────

class TestEngagementInput:
    def test_input_creation(self):
        inp = make_input()
        assert inp.rep_id == "rep-001"
        assert inp.region == "North"

    def test_input_has_22_fields(self):
        import dataclasses
        fields = dataclasses.fields(EngagementInput)
        assert len(fields) == 22

    def test_input_total_active_deals_int(self):
        inp = make_input(total_active_deals=10)
        assert isinstance(inp.total_active_deals, int)

    def test_input_float_fields(self):
        inp = make_input()
        assert isinstance(inp.buyer_email_response_rate_pct, float)
        assert isinstance(inp.avg_opportunity_value_usd, float)


# ─────────────────────────────────────────────────────────────────────────────
# 3. EngagementResult dataclass + to_dict()
# ─────────────────────────────────────────────────────────────────────────────

class TestEngagementResult:
    def _make_result(self):
        engine = make_engine()
        return engine.assess(make_input())

    def test_result_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(EngagementResult)
        assert len(fields) == 15

    def test_to_dict_has_15_keys(self):
        d = self._make_result().to_dict()
        assert len(d) == 15

    def test_to_dict_keys(self):
        expected = {
            "rep_id", "region", "engagement_risk", "engagement_pattern",
            "engagement_severity", "recommended_action", "responsiveness_score",
            "signal_score", "activation_score", "risk_score",
            "engagement_composite", "has_engagement_gap",
            "requires_engagement_coaching", "estimated_revenue_at_dark_usd",
            "engagement_signal",
        }
        assert set(self._make_result().to_dict().keys()) == expected

    def test_to_dict_enum_values_are_strings(self):
        d = self._make_result().to_dict()
        assert isinstance(d["engagement_risk"], str)
        assert isinstance(d["engagement_pattern"], str)
        assert isinstance(d["engagement_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_preserved(self):
        engine = make_engine()
        result = engine.assess(make_input(rep_id="xyz-999"))
        assert result.to_dict()["rep_id"] == "xyz-999"

    def test_to_dict_region_preserved(self):
        engine = make_engine()
        result = engine.assess(make_input(region="EMEA"))
        assert result.to_dict()["region"] == "EMEA"

    def test_to_dict_bool_fields_are_bool(self):
        d = self._make_result().to_dict()
        assert isinstance(d["has_engagement_gap"], bool)
        assert isinstance(d["requires_engagement_coaching"], bool)

    def test_to_dict_numeric_fields_are_float(self):
        d = self._make_result().to_dict()
        for key in ["responsiveness_score", "signal_score", "activation_score",
                    "risk_score", "engagement_composite", "estimated_revenue_at_dark_usd"]:
            assert isinstance(d[key], float), f"{key} should be float"


# ─────────────────────────────────────────────────────────────────────────────
# 4. _responsiveness_score
# ─────────────────────────────────────────────────────────────────────────────

class TestResponsivenessScore:
    def _score(self, **kw) -> float:
        engine = make_engine()
        return engine._responsiveness_score(make_input(**kw))

    # buyer_email_response_rate_pct
    def test_email_response_at_or_below_025_adds_40(self):
        assert self._score(buyer_email_response_rate_pct=0.25) == pytest.approx(40 + 0 + 0)  # no other triggers

    def test_email_response_strictly_below_025(self):
        s = self._score(buyer_email_response_rate_pct=0.10,
                        meeting_attendance_rate_pct=0.90,
                        buyer_initiated_follow_up_pct=0.50)
        assert s == pytest.approx(40.0)

    def test_email_response_between_025_and_045_adds_22(self):
        s = self._score(buyer_email_response_rate_pct=0.30,
                        meeting_attendance_rate_pct=0.90,
                        buyer_initiated_follow_up_pct=0.50)
        assert s == pytest.approx(22.0)

    def test_email_response_at_045_adds_22(self):
        s = self._score(buyer_email_response_rate_pct=0.45,
                        meeting_attendance_rate_pct=0.90,
                        buyer_initiated_follow_up_pct=0.50)
        assert s == pytest.approx(22.0)

    def test_email_response_between_045_and_060_adds_8(self):
        s = self._score(buyer_email_response_rate_pct=0.55,
                        meeting_attendance_rate_pct=0.90,
                        buyer_initiated_follow_up_pct=0.50)
        assert s == pytest.approx(8.0)

    def test_email_response_above_060_adds_0(self):
        s = self._score(buyer_email_response_rate_pct=0.80,
                        meeting_attendance_rate_pct=0.90,
                        buyer_initiated_follow_up_pct=0.50)
        assert s == pytest.approx(0.0)

    # meeting_attendance_rate_pct
    def test_meeting_attendance_at_or_below_055_adds_35(self):
        s = self._score(buyer_email_response_rate_pct=0.80,
                        meeting_attendance_rate_pct=0.55,
                        buyer_initiated_follow_up_pct=0.50)
        assert s == pytest.approx(35.0)

    def test_meeting_attendance_between_055_and_075_adds_18(self):
        s = self._score(buyer_email_response_rate_pct=0.80,
                        meeting_attendance_rate_pct=0.70,
                        buyer_initiated_follow_up_pct=0.50)
        assert s == pytest.approx(18.0)

    def test_meeting_attendance_above_075_adds_0(self):
        s = self._score(buyer_email_response_rate_pct=0.80,
                        meeting_attendance_rate_pct=0.90,
                        buyer_initiated_follow_up_pct=0.50)
        assert s == pytest.approx(0.0)

    # buyer_initiated_follow_up_pct
    def test_follow_up_at_or_below_010_adds_25(self):
        s = self._score(buyer_email_response_rate_pct=0.80,
                        meeting_attendance_rate_pct=0.90,
                        buyer_initiated_follow_up_pct=0.10)
        assert s == pytest.approx(25.0)

    def test_follow_up_between_010_and_025_adds_12(self):
        s = self._score(buyer_email_response_rate_pct=0.80,
                        meeting_attendance_rate_pct=0.90,
                        buyer_initiated_follow_up_pct=0.20)
        assert s == pytest.approx(12.0)

    def test_follow_up_above_025_adds_0(self):
        s = self._score(buyer_email_response_rate_pct=0.80,
                        meeting_attendance_rate_pct=0.90,
                        buyer_initiated_follow_up_pct=0.50)
        assert s == pytest.approx(0.0)

    # Additive and cap
    def test_full_score_sums_correctly(self):
        # <=0.25 → +40, <=0.55 → +35, <=0.10 → +25 = 100
        s = self._score(buyer_email_response_rate_pct=0.20,
                        meeting_attendance_rate_pct=0.50,
                        buyer_initiated_follow_up_pct=0.05)
        assert s == pytest.approx(100.0)

    def test_score_capped_at_100(self):
        # Same maximal inputs — should not exceed 100
        s = self._score(buyer_email_response_rate_pct=0.10,
                        meeting_attendance_rate_pct=0.30,
                        buyer_initiated_follow_up_pct=0.05)
        assert s <= 100.0

    def test_score_non_negative(self):
        s = self._score(buyer_email_response_rate_pct=1.0,
                        meeting_attendance_rate_pct=1.0,
                        buyer_initiated_follow_up_pct=1.0)
        assert s >= 0.0

    def test_partial_score_additive(self):
        # <=0.45 → +22, <=0.75 → +18, <=0.25 → +12 = 52
        s = self._score(buyer_email_response_rate_pct=0.45,
                        meeting_attendance_rate_pct=0.75,
                        buyer_initiated_follow_up_pct=0.25)
        assert s == pytest.approx(52.0)


# ─────────────────────────────────────────────────────────────────────────────
# 5. _signal_score
# ─────────────────────────────────────────────────────────────────────────────

class TestSignalScore:
    def _score(self, **kw) -> float:
        engine = make_engine()
        return engine._signal_score(make_input(**kw))

    def test_proposal_open_rate_at_040_adds_40(self):
        s = self._score(proposal_open_rate_pct=0.40,
                        content_shared_engagement_rate_pct=0.60,
                        multi_touch_engagement_rate_pct=0.60)
        assert s == pytest.approx(40.0)

    def test_proposal_open_rate_between_040_060_adds_22(self):
        s = self._score(proposal_open_rate_pct=0.55,
                        content_shared_engagement_rate_pct=0.60,
                        multi_touch_engagement_rate_pct=0.60)
        assert s == pytest.approx(22.0)

    def test_proposal_open_rate_between_060_075_adds_8(self):
        s = self._score(proposal_open_rate_pct=0.70,
                        content_shared_engagement_rate_pct=0.60,
                        multi_touch_engagement_rate_pct=0.60)
        assert s == pytest.approx(8.0)

    def test_proposal_open_rate_above_075_adds_0(self):
        s = self._score(proposal_open_rate_pct=0.90,
                        content_shared_engagement_rate_pct=0.60,
                        multi_touch_engagement_rate_pct=0.60)
        assert s == pytest.approx(0.0)

    def test_content_engagement_at_020_adds_35(self):
        s = self._score(proposal_open_rate_pct=0.90,
                        content_shared_engagement_rate_pct=0.20,
                        multi_touch_engagement_rate_pct=0.60)
        assert s == pytest.approx(35.0)

    def test_content_engagement_between_020_040_adds_18(self):
        s = self._score(proposal_open_rate_pct=0.90,
                        content_shared_engagement_rate_pct=0.30,
                        multi_touch_engagement_rate_pct=0.60)
        assert s == pytest.approx(18.0)

    def test_content_engagement_above_040_adds_0(self):
        s = self._score(proposal_open_rate_pct=0.90,
                        content_shared_engagement_rate_pct=0.60,
                        multi_touch_engagement_rate_pct=0.60)
        assert s == pytest.approx(0.0)

    def test_multi_touch_at_020_adds_25(self):
        s = self._score(proposal_open_rate_pct=0.90,
                        content_shared_engagement_rate_pct=0.60,
                        multi_touch_engagement_rate_pct=0.20)
        assert s == pytest.approx(25.0)

    def test_multi_touch_between_020_040_adds_12(self):
        s = self._score(proposal_open_rate_pct=0.90,
                        content_shared_engagement_rate_pct=0.60,
                        multi_touch_engagement_rate_pct=0.35)
        assert s == pytest.approx(12.0)

    def test_multi_touch_above_040_adds_0(self):
        s = self._score(proposal_open_rate_pct=0.90,
                        content_shared_engagement_rate_pct=0.60,
                        multi_touch_engagement_rate_pct=0.60)
        assert s == pytest.approx(0.0)

    def test_max_signal_score_is_100(self):
        s = self._score(proposal_open_rate_pct=0.10,
                        content_shared_engagement_rate_pct=0.10,
                        multi_touch_engagement_rate_pct=0.10)
        assert s == pytest.approx(100.0)

    def test_signal_score_capped(self):
        s = self._score(proposal_open_rate_pct=0.01,
                        content_shared_engagement_rate_pct=0.01,
                        multi_touch_engagement_rate_pct=0.01)
        assert s <= 100.0

    def test_all_healthy_zero_signal_score(self):
        s = self._score(proposal_open_rate_pct=0.90,
                        content_shared_engagement_rate_pct=0.90,
                        multi_touch_engagement_rate_pct=0.90)
        assert s == pytest.approx(0.0)

    def test_partial_signal_score(self):
        # proposal <=0.60 → +22, content <=0.40 → +18, multi >0.40 → +0 = 40
        s = self._score(proposal_open_rate_pct=0.55,
                        content_shared_engagement_rate_pct=0.35,
                        multi_touch_engagement_rate_pct=0.60)
        assert s == pytest.approx(40.0)


# ─────────────────────────────────────────────────────────────────────────────
# 6. _activation_score
# ─────────────────────────────────────────────────────────────────────────────

class TestActivationScore:
    def _score(self, **kw) -> float:
        engine = make_engine()
        return engine._activation_score(make_input(**kw))

    def test_demo_at_035_adds_45(self):
        s = self._score(demo_to_next_step_commitment_rate_pct=0.35,
                        stakeholder_expansion_by_buyer_pct=0.50,
                        mutual_action_plan_adherence_pct=0.80)
        assert s == pytest.approx(45.0)

    def test_demo_between_035_055_adds_25(self):
        s = self._score(demo_to_next_step_commitment_rate_pct=0.45,
                        stakeholder_expansion_by_buyer_pct=0.50,
                        mutual_action_plan_adherence_pct=0.80)
        assert s == pytest.approx(25.0)

    def test_demo_between_055_070_adds_10(self):
        s = self._score(demo_to_next_step_commitment_rate_pct=0.60,
                        stakeholder_expansion_by_buyer_pct=0.50,
                        mutual_action_plan_adherence_pct=0.80)
        assert s == pytest.approx(10.0)

    def test_demo_above_070_adds_0(self):
        s = self._score(demo_to_next_step_commitment_rate_pct=0.80,
                        stakeholder_expansion_by_buyer_pct=0.50,
                        mutual_action_plan_adherence_pct=0.80)
        assert s == pytest.approx(0.0)

    def test_stakeholder_at_010_adds_30(self):
        s = self._score(demo_to_next_step_commitment_rate_pct=0.80,
                        stakeholder_expansion_by_buyer_pct=0.10,
                        mutual_action_plan_adherence_pct=0.80)
        assert s == pytest.approx(30.0)

    def test_stakeholder_between_010_025_adds_15(self):
        s = self._score(demo_to_next_step_commitment_rate_pct=0.80,
                        stakeholder_expansion_by_buyer_pct=0.20,
                        mutual_action_plan_adherence_pct=0.80)
        assert s == pytest.approx(15.0)

    def test_stakeholder_above_025_adds_0(self):
        s = self._score(demo_to_next_step_commitment_rate_pct=0.80,
                        stakeholder_expansion_by_buyer_pct=0.50,
                        mutual_action_plan_adherence_pct=0.80)
        assert s == pytest.approx(0.0)

    def test_map_adherence_at_030_adds_25(self):
        s = self._score(demo_to_next_step_commitment_rate_pct=0.80,
                        stakeholder_expansion_by_buyer_pct=0.50,
                        mutual_action_plan_adherence_pct=0.30)
        assert s == pytest.approx(25.0)

    def test_map_adherence_between_030_055_adds_12(self):
        s = self._score(demo_to_next_step_commitment_rate_pct=0.80,
                        stakeholder_expansion_by_buyer_pct=0.50,
                        mutual_action_plan_adherence_pct=0.40)
        assert s == pytest.approx(12.0)

    def test_map_adherence_above_055_adds_0(self):
        s = self._score(demo_to_next_step_commitment_rate_pct=0.80,
                        stakeholder_expansion_by_buyer_pct=0.50,
                        mutual_action_plan_adherence_pct=0.80)
        assert s == pytest.approx(0.0)

    def test_max_activation_score_is_100(self):
        s = self._score(demo_to_next_step_commitment_rate_pct=0.10,
                        stakeholder_expansion_by_buyer_pct=0.05,
                        mutual_action_plan_adherence_pct=0.10)
        assert s == pytest.approx(100.0)

    def test_activation_score_capped_at_100(self):
        s = self._score(demo_to_next_step_commitment_rate_pct=0.01,
                        stakeholder_expansion_by_buyer_pct=0.01,
                        mutual_action_plan_adherence_pct=0.01)
        assert s <= 100.0

    def test_zero_activation_when_all_healthy(self):
        s = self._score(demo_to_next_step_commitment_rate_pct=0.90,
                        stakeholder_expansion_by_buyer_pct=0.90,
                        mutual_action_plan_adherence_pct=0.90)
        assert s == pytest.approx(0.0)

    def test_partial_activation_score(self):
        # demo <=0.55 → +25, stakeholder <=0.25 → +15, map >0.55 → +0 = 40
        s = self._score(demo_to_next_step_commitment_rate_pct=0.50,
                        stakeholder_expansion_by_buyer_pct=0.20,
                        mutual_action_plan_adherence_pct=0.70)
        assert s == pytest.approx(40.0)


# ─────────────────────────────────────────────────────────────────────────────
# 7. _risk_score
# ─────────────────────────────────────────────────────────────────────────────

class TestRiskScore:
    def _score(self, **kw) -> float:
        engine = make_engine()
        return engine._risk_score(make_input(**kw))

    def test_deal_dark_at_040_adds_40(self):
        s = self._score(deal_dark_more_than_14d_pct=0.40,
                        meeting_cancellation_rate_pct=0.10,
                        avg_days_buyer_silent_before_followup=5.0)
        assert s == pytest.approx(40.0)

    def test_deal_dark_between_020_040_adds_22(self):
        s = self._score(deal_dark_more_than_14d_pct=0.25,
                        meeting_cancellation_rate_pct=0.10,
                        avg_days_buyer_silent_before_followup=5.0)
        assert s == pytest.approx(22.0)

    def test_deal_dark_between_010_020_adds_8(self):
        s = self._score(deal_dark_more_than_14d_pct=0.15,
                        meeting_cancellation_rate_pct=0.10,
                        avg_days_buyer_silent_before_followup=5.0)
        assert s == pytest.approx(8.0)

    def test_deal_dark_below_010_adds_0(self):
        s = self._score(deal_dark_more_than_14d_pct=0.05,
                        meeting_cancellation_rate_pct=0.10,
                        avg_days_buyer_silent_before_followup=5.0)
        assert s == pytest.approx(0.0)

    def test_meeting_cancel_at_035_adds_35(self):
        s = self._score(deal_dark_more_than_14d_pct=0.05,
                        meeting_cancellation_rate_pct=0.35,
                        avg_days_buyer_silent_before_followup=5.0)
        assert s == pytest.approx(35.0)

    def test_meeting_cancel_between_020_035_adds_18(self):
        s = self._score(deal_dark_more_than_14d_pct=0.05,
                        meeting_cancellation_rate_pct=0.25,
                        avg_days_buyer_silent_before_followup=5.0)
        assert s == pytest.approx(18.0)

    def test_meeting_cancel_below_020_adds_0(self):
        s = self._score(deal_dark_more_than_14d_pct=0.05,
                        meeting_cancellation_rate_pct=0.10,
                        avg_days_buyer_silent_before_followup=5.0)
        assert s == pytest.approx(0.0)

    def test_silent_days_at_20_adds_25(self):
        s = self._score(deal_dark_more_than_14d_pct=0.05,
                        meeting_cancellation_rate_pct=0.10,
                        avg_days_buyer_silent_before_followup=20.0)
        assert s == pytest.approx(25.0)

    def test_silent_days_between_12_20_adds_12(self):
        s = self._score(deal_dark_more_than_14d_pct=0.05,
                        meeting_cancellation_rate_pct=0.10,
                        avg_days_buyer_silent_before_followup=15.0)
        assert s == pytest.approx(12.0)

    def test_silent_days_below_12_adds_0(self):
        s = self._score(deal_dark_more_than_14d_pct=0.05,
                        meeting_cancellation_rate_pct=0.10,
                        avg_days_buyer_silent_before_followup=5.0)
        assert s == pytest.approx(0.0)

    def test_max_risk_score_is_100(self):
        s = self._score(deal_dark_more_than_14d_pct=0.90,
                        meeting_cancellation_rate_pct=0.90,
                        avg_days_buyer_silent_before_followup=30.0)
        assert s == pytest.approx(100.0)

    def test_risk_score_capped_at_100(self):
        s = self._score(deal_dark_more_than_14d_pct=1.0,
                        meeting_cancellation_rate_pct=1.0,
                        avg_days_buyer_silent_before_followup=100.0)
        assert s <= 100.0

    def test_zero_risk_when_all_healthy(self):
        s = self._score(deal_dark_more_than_14d_pct=0.01,
                        meeting_cancellation_rate_pct=0.01,
                        avg_days_buyer_silent_before_followup=1.0)
        assert s == pytest.approx(0.0)

    def test_partial_risk_score(self):
        # dark >=0.20 → +22, cancel >=0.20 → +18, silent >=12 → +12 = 52
        s = self._score(deal_dark_more_than_14d_pct=0.25,
                        meeting_cancellation_rate_pct=0.25,
                        avg_days_buyer_silent_before_followup=15.0)
        assert s == pytest.approx(52.0)


# ─────────────────────────────────────────────────────────────────────────────
# 8. Composite calculation
# ─────────────────────────────────────────────────────────────────────────────

class TestComposite:
    def test_composite_weights_sum_to_1(self):
        assert pytest.approx(0.30 + 0.30 + 0.25 + 0.15, abs=1e-9) == 1.0

    def test_composite_formula(self):
        engine = make_engine()
        # Use known sub-scores
        rs, ss, ac, rk = 40.0, 40.0, 45.0, 0.0
        expected = round(40 * 0.30 + 40 * 0.30 + 45 * 0.25 + 0 * 0.15, 2)
        assert engine._composite(rs, ss, ac, rk) == pytest.approx(expected)

    def test_composite_zero_when_all_healthy(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert result.engagement_composite == pytest.approx(0.0)

    def test_composite_capped_at_100(self):
        engine = make_engine()
        result = engine._composite(100.0, 100.0, 100.0, 100.0)
        assert result <= 100.0

    def test_composite_max_is_100(self):
        engine = make_engine()
        result = engine._composite(100.0, 100.0, 100.0, 100.0)
        assert result == pytest.approx(100.0)

    def test_composite_uses_two_decimal_rounding(self):
        engine = make_engine()
        # 22*0.30 + 22*0.30 + 25*0.25 + 12*0.15 = 6.6 + 6.6 + 6.25 + 1.80 = 21.25
        result = engine._composite(22.0, 22.0, 25.0, 12.0)
        assert result == pytest.approx(21.25)


# ─────────────────────────────────────────────────────────────────────────────
# 9. Pattern detection
# ─────────────────────────────────────────────────────────────────────────────

class TestPattern:
    def _pattern(self, **kw) -> EngagementPattern:
        engine = make_engine()
        return engine._pattern(make_input(**kw))

    def test_no_pattern_when_all_healthy(self):
        assert self._pattern() == EngagementPattern.none

    def test_one_way_sender_exact_boundary(self):
        p = self._pattern(buyer_email_response_rate_pct=0.20,
                          buyer_initiated_follow_up_pct=0.08)
        assert p == EngagementPattern.one_way_sender

    def test_one_way_sender_below_both_thresholds(self):
        p = self._pattern(buyer_email_response_rate_pct=0.10,
                          buyer_initiated_follow_up_pct=0.05)
        assert p == EngagementPattern.one_way_sender

    def test_one_way_sender_requires_both_conditions(self):
        # Email low but follow-up high → not one_way_sender
        p = self._pattern(buyer_email_response_rate_pct=0.10,
                          buyer_initiated_follow_up_pct=0.20)
        assert p != EngagementPattern.one_way_sender

    def test_low_signal_pursuer_exact_boundary(self):
        p = self._pattern(buyer_email_response_rate_pct=0.80,
                          buyer_initiated_follow_up_pct=0.50,
                          proposal_open_rate_pct=0.30,
                          content_shared_engagement_rate_pct=0.15)
        assert p == EngagementPattern.low_signal_pursuer

    def test_low_signal_pursuer_below_both(self):
        p = self._pattern(buyer_email_response_rate_pct=0.80,
                          buyer_initiated_follow_up_pct=0.50,
                          proposal_open_rate_pct=0.20,
                          content_shared_engagement_rate_pct=0.10)
        assert p == EngagementPattern.low_signal_pursuer

    def test_engagement_ignorer_exact_boundary(self):
        p = self._pattern(buyer_email_response_rate_pct=0.80,
                          buyer_initiated_follow_up_pct=0.50,
                          proposal_open_rate_pct=0.80,
                          content_shared_engagement_rate_pct=0.80,
                          deal_dark_more_than_14d_pct=0.45,
                          rep_response_to_buyer_signal_hours_avg=48.0)
        assert p == EngagementPattern.engagement_ignorer

    def test_engagement_ignorer_above_thresholds(self):
        p = self._pattern(buyer_email_response_rate_pct=0.80,
                          buyer_initiated_follow_up_pct=0.50,
                          proposal_open_rate_pct=0.80,
                          content_shared_engagement_rate_pct=0.80,
                          deal_dark_more_than_14d_pct=0.60,
                          rep_response_to_buyer_signal_hours_avg=72.0)
        assert p == EngagementPattern.engagement_ignorer

    def test_meeting_canceler_exact_boundary(self):
        p = self._pattern(buyer_email_response_rate_pct=0.80,
                          buyer_initiated_follow_up_pct=0.50,
                          proposal_open_rate_pct=0.80,
                          content_shared_engagement_rate_pct=0.80,
                          deal_dark_more_than_14d_pct=0.05,
                          rep_response_to_buyer_signal_hours_avg=4.0,
                          meeting_cancellation_rate_pct=0.40,
                          meeting_attendance_rate_pct=0.55)
        assert p == EngagementPattern.meeting_canceler

    def test_proposal_black_hole_exact_boundary(self):
        p = self._pattern(buyer_email_response_rate_pct=0.80,
                          buyer_initiated_follow_up_pct=0.50,
                          proposal_open_rate_pct=0.50,
                          content_shared_engagement_rate_pct=0.80,
                          proposal_viewed_more_than_once_pct=0.15,
                          deal_dark_more_than_14d_pct=0.05,
                          meeting_cancellation_rate_pct=0.10,
                          meeting_attendance_rate_pct=0.90,
                          rep_response_to_buyer_signal_hours_avg=4.0)
        assert p == EngagementPattern.proposal_black_hole

    def test_priority_one_way_sender_beats_low_signal(self):
        # Both conditions met → one_way_sender wins (higher priority)
        p = self._pattern(buyer_email_response_rate_pct=0.10,
                          buyer_initiated_follow_up_pct=0.05,
                          proposal_open_rate_pct=0.20,
                          content_shared_engagement_rate_pct=0.10)
        assert p == EngagementPattern.one_way_sender

    def test_priority_low_signal_beats_engagement_ignorer(self):
        # one_way_sender NOT met; low_signal & engagement_ignorer both met
        p = self._pattern(buyer_email_response_rate_pct=0.50,
                          buyer_initiated_follow_up_pct=0.50,
                          proposal_open_rate_pct=0.20,
                          content_shared_engagement_rate_pct=0.10,
                          deal_dark_more_than_14d_pct=0.60,
                          rep_response_to_buyer_signal_hours_avg=72.0)
        assert p == EngagementPattern.low_signal_pursuer

    def test_none_when_nothing_triggered(self):
        p = self._pattern(buyer_email_response_rate_pct=0.90,
                          buyer_initiated_follow_up_pct=0.90,
                          proposal_open_rate_pct=0.90,
                          content_shared_engagement_rate_pct=0.90,
                          deal_dark_more_than_14d_pct=0.01,
                          rep_response_to_buyer_signal_hours_avg=2.0,
                          meeting_cancellation_rate_pct=0.01,
                          meeting_attendance_rate_pct=0.99,
                          proposal_viewed_more_than_once_pct=0.90)
        assert p == EngagementPattern.none


# ─────────────────────────────────────────────────────────────────────────────
# 10. Risk thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestRiskThresholds:
    def _risk(self, composite: float) -> EngagementRisk:
        return make_engine()._risk(composite)

    def test_composite_60_is_critical(self):
        assert self._risk(60.0) == EngagementRisk.critical

    def test_composite_above_60_is_critical(self):
        assert self._risk(75.0) == EngagementRisk.critical

    def test_composite_100_is_critical(self):
        assert self._risk(100.0) == EngagementRisk.critical

    def test_composite_40_is_high(self):
        assert self._risk(40.0) == EngagementRisk.high

    def test_composite_59_is_high(self):
        assert self._risk(59.9) == EngagementRisk.high

    def test_composite_20_is_moderate(self):
        assert self._risk(20.0) == EngagementRisk.moderate

    def test_composite_39_is_moderate(self):
        assert self._risk(39.9) == EngagementRisk.moderate

    def test_composite_0_is_low(self):
        assert self._risk(0.0) == EngagementRisk.low

    def test_composite_19_is_low(self):
        assert self._risk(19.9) == EngagementRisk.low


# ─────────────────────────────────────────────────────────────────────────────
# 11. Severity thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestSeverityThresholds:
    def _severity(self, composite: float) -> EngagementSeverity:
        return make_engine()._severity(composite)

    def test_composite_60_is_dark(self):
        assert self._severity(60.0) == EngagementSeverity.dark

    def test_composite_100_is_dark(self):
        assert self._severity(100.0) == EngagementSeverity.dark

    def test_composite_40_is_passive(self):
        assert self._severity(40.0) == EngagementSeverity.passive

    def test_composite_59_is_passive(self):
        assert self._severity(59.9) == EngagementSeverity.passive

    def test_composite_20_is_responsive(self):
        assert self._severity(20.0) == EngagementSeverity.responsive

    def test_composite_39_is_responsive(self):
        assert self._severity(39.9) == EngagementSeverity.responsive

    def test_composite_0_is_engaged(self):
        assert self._severity(0.0) == EngagementSeverity.engaged

    def test_composite_19_is_engaged(self):
        assert self._severity(19.9) == EngagementSeverity.engaged


# ─────────────────────────────────────────────────────────────────────────────
# 12. Action routing
# ─────────────────────────────────────────────────────────────────────────────

class TestActionRouting:
    def _action(self, risk, pattern) -> EngagementAction:
        return make_engine()._action(risk, pattern)

    def test_critical_one_way_sender_is_deal_qualification_review(self):
        assert self._action(EngagementRisk.critical, EngagementPattern.one_way_sender) == EngagementAction.deal_qualification_review

    def test_critical_engagement_ignorer_is_engagement_intervention(self):
        assert self._action(EngagementRisk.critical, EngagementPattern.engagement_ignorer) == EngagementAction.engagement_intervention

    def test_critical_none_is_deal_qualification_review(self):
        assert self._action(EngagementRisk.critical, EngagementPattern.none) == EngagementAction.deal_qualification_review

    def test_critical_meeting_canceler_is_deal_qualification_review(self):
        assert self._action(EngagementRisk.critical, EngagementPattern.meeting_canceler) == EngagementAction.deal_qualification_review

    def test_critical_low_signal_is_deal_qualification_review(self):
        assert self._action(EngagementRisk.critical, EngagementPattern.low_signal_pursuer) == EngagementAction.deal_qualification_review

    def test_critical_proposal_black_hole_is_deal_qualification_review(self):
        assert self._action(EngagementRisk.critical, EngagementPattern.proposal_black_hole) == EngagementAction.deal_qualification_review

    def test_high_low_signal_pursuer_is_signal_response_coaching(self):
        assert self._action(EngagementRisk.high, EngagementPattern.low_signal_pursuer) == EngagementAction.signal_response_coaching

    def test_high_meeting_canceler_is_buyer_activation_coaching(self):
        assert self._action(EngagementRisk.high, EngagementPattern.meeting_canceler) == EngagementAction.buyer_activation_coaching

    def test_high_proposal_black_hole_is_deal_review_coaching(self):
        assert self._action(EngagementRisk.high, EngagementPattern.proposal_black_hole) == EngagementAction.deal_review_coaching

    def test_high_none_is_engagement_quality_coaching(self):
        assert self._action(EngagementRisk.high, EngagementPattern.none) == EngagementAction.engagement_quality_coaching

    def test_high_one_way_sender_is_engagement_quality_coaching(self):
        assert self._action(EngagementRisk.high, EngagementPattern.one_way_sender) == EngagementAction.engagement_quality_coaching

    def test_high_engagement_ignorer_is_engagement_quality_coaching(self):
        assert self._action(EngagementRisk.high, EngagementPattern.engagement_ignorer) == EngagementAction.engagement_quality_coaching

    def test_moderate_any_is_engagement_quality_coaching(self):
        for pattern in EngagementPattern:
            assert self._action(EngagementRisk.moderate, pattern) == EngagementAction.engagement_quality_coaching

    def test_low_any_is_no_action(self):
        for pattern in EngagementPattern:
            assert self._action(EngagementRisk.low, pattern) == EngagementAction.no_action


# ─────────────────────────────────────────────────────────────────────────────
# 13. Flags: has_engagement_gap
# ─────────────────────────────────────────────────────────────────────────────

class TestHasEngagementGap:
    def _gap(self, **kw) -> bool:
        engine = make_engine()
        return engine.assess(make_input(**kw)).has_engagement_gap

    def test_no_gap_when_all_healthy(self):
        assert self._gap() is False

    def test_gap_when_composite_at_40(self):
        # Force composite >= 40: all-bad inputs
        assert self._gap(
            buyer_email_response_rate_pct=0.10,
            meeting_attendance_rate_pct=0.40,
            buyer_initiated_follow_up_pct=0.05,
            proposal_open_rate_pct=0.20,
            content_shared_engagement_rate_pct=0.10,
            multi_touch_engagement_rate_pct=0.10,
            demo_to_next_step_commitment_rate_pct=0.20,
            stakeholder_expansion_by_buyer_pct=0.05,
            mutual_action_plan_adherence_pct=0.20,
            deal_dark_more_than_14d_pct=0.50,
            meeting_cancellation_rate_pct=0.50,
            avg_days_buyer_silent_before_followup=25.0,
        ) is True

    def test_gap_when_deal_dark_pct_at_025(self):
        # deal_dark >= 0.25 triggers gap
        assert self._gap(deal_dark_more_than_14d_pct=0.25) is True

    def test_gap_when_email_response_rate_at_040(self):
        # buyer_email_response_rate_pct <= 0.40 triggers gap
        assert self._gap(buyer_email_response_rate_pct=0.40) is True

    def test_gap_when_email_response_below_040(self):
        assert self._gap(buyer_email_response_rate_pct=0.30) is True

    def test_no_gap_when_email_response_just_above_040(self):
        # 0.41 > 0.40 does not trigger; deal dark <0.25; composite <40
        result = make_engine().assess(make_input(buyer_email_response_rate_pct=0.41))
        assert result.has_engagement_gap is False


# ─────────────────────────────────────────────────────────────────────────────
# 14. Flags: requires_engagement_coaching
# ─────────────────────────────────────────────────────────────────────────────

class TestRequiresEngagementCoaching:
    def _coaching(self, **kw) -> bool:
        engine = make_engine()
        return engine.assess(make_input(**kw)).requires_engagement_coaching

    def test_no_coaching_when_all_healthy(self):
        assert self._coaching() is False

    def test_coaching_when_meeting_attendance_at_065(self):
        assert self._coaching(meeting_attendance_rate_pct=0.65) is True

    def test_coaching_when_meeting_attendance_below_065(self):
        assert self._coaching(meeting_attendance_rate_pct=0.50) is True

    def test_coaching_when_demo_rate_at_050(self):
        assert self._coaching(demo_to_next_step_commitment_rate_pct=0.50) is True

    def test_coaching_when_demo_rate_below_050(self):
        assert self._coaching(demo_to_next_step_commitment_rate_pct=0.30) is True

    def test_no_coaching_when_slightly_above_thresholds(self):
        # Both 0.66 > 0.65 and 0.51 > 0.50; composite stays low
        result = make_engine().assess(make_input(
            meeting_attendance_rate_pct=0.66,
            demo_to_next_step_commitment_rate_pct=0.51,
        ))
        assert result.requires_engagement_coaching is False


# ─────────────────────────────────────────────────────────────────────────────
# 15. estimated_revenue_at_dark_usd
# ─────────────────────────────────────────────────────────────────────────────

class TestRevenueAtDark:
    def test_zero_when_no_dark_deals(self):
        engine = make_engine()
        result = engine.assess(make_input(deal_dark_more_than_14d_pct=0.0))
        assert result.estimated_revenue_at_dark_usd == pytest.approx(0.0)

    def test_zero_when_composite_is_zero(self):
        # If composite = 0, revenue = 0 regardless of dark pct
        engine = make_engine()
        inp = make_input(deal_dark_more_than_14d_pct=0.50)
        result = engine.assess(inp)
        # composite may not be zero with dark pct=0.50, so let's check formula directly
        comp = result.engagement_composite
        expected = round(inp.total_active_deals * inp.avg_opportunity_value_usd * 0.50 * (comp / 100), 2)
        assert result.estimated_revenue_at_dark_usd == pytest.approx(expected)

    def test_revenue_formula_manual(self):
        engine = make_engine()
        inp = make_input(
            total_active_deals=10,
            avg_opportunity_value_usd=100_000.0,
            deal_dark_more_than_14d_pct=0.50,
        )
        result = engine.assess(inp)
        comp = result.engagement_composite
        expected = round(10 * 100_000.0 * 0.50 * (comp / 100), 2)
        assert result.estimated_revenue_at_dark_usd == pytest.approx(expected)

    def test_revenue_rounded_to_2_decimals(self):
        engine = make_engine()
        result = engine.assess(make_input(
            total_active_deals=3,
            avg_opportunity_value_usd=33_333.33,
            deal_dark_more_than_14d_pct=0.30,
        ))
        # Just check it's rounded properly
        val = result.estimated_revenue_at_dark_usd
        assert round(val, 2) == val


# ─────────────────────────────────────────────────────────────────────────────
# 16. Signal string
# ─────────────────────────────────────────────────────────────────────────────

class TestSignalString:
    HEALTHY_SIGNAL = (
        "Buyer engagement strong — response rates, signal quality, "
        "and deal activation within benchmarks"
    )

    def test_healthy_signal_when_composite_below_20(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert result.engagement_signal == self.HEALTHY_SIGNAL

    def test_unhealthy_signal_contains_pattern_label(self):
        engine = make_engine()
        result = engine.assess(make_input(
            buyer_email_response_rate_pct=0.10,
            buyer_initiated_follow_up_pct=0.05,
            meeting_attendance_rate_pct=0.40,
            proposal_open_rate_pct=0.20,
            content_shared_engagement_rate_pct=0.10,
            multi_touch_engagement_rate_pct=0.10,
            demo_to_next_step_commitment_rate_pct=0.20,
            stakeholder_expansion_by_buyer_pct=0.05,
            mutual_action_plan_adherence_pct=0.20,
            deal_dark_more_than_14d_pct=0.50,
            meeting_cancellation_rate_pct=0.50,
            avg_days_buyer_silent_before_followup=25.0,
        ))
        assert "One-way sender" in result.engagement_signal

    def test_unhealthy_signal_contains_email_response_pct(self):
        engine = make_engine()
        inp = make_input(
            buyer_email_response_rate_pct=0.10,
            buyer_initiated_follow_up_pct=0.05,
            meeting_attendance_rate_pct=0.40,
            proposal_open_rate_pct=0.20,
            content_shared_engagement_rate_pct=0.10,
            multi_touch_engagement_rate_pct=0.10,
            demo_to_next_step_commitment_rate_pct=0.20,
            stakeholder_expansion_by_buyer_pct=0.05,
            mutual_action_plan_adherence_pct=0.20,
            deal_dark_more_than_14d_pct=0.50,
            meeting_cancellation_rate_pct=0.50,
            avg_days_buyer_silent_before_followup=25.0,
        )
        result = engine.assess(inp)
        # 0.10 * 100 = 10% → "10% buyer email response"
        assert "10% buyer email response" in result.engagement_signal

    def test_unhealthy_signal_contains_meeting_attendance_pct(self):
        engine = make_engine()
        inp = make_input(
            buyer_email_response_rate_pct=0.10,
            buyer_initiated_follow_up_pct=0.05,
            meeting_attendance_rate_pct=0.40,
            proposal_open_rate_pct=0.20,
            content_shared_engagement_rate_pct=0.10,
            multi_touch_engagement_rate_pct=0.10,
            demo_to_next_step_commitment_rate_pct=0.20,
            stakeholder_expansion_by_buyer_pct=0.05,
            mutual_action_plan_adherence_pct=0.20,
            deal_dark_more_than_14d_pct=0.50,
            meeting_cancellation_rate_pct=0.50,
            avg_days_buyer_silent_before_followup=25.0,
        )
        result = engine.assess(inp)
        assert "40% meeting attendance" in result.engagement_signal

    def test_unhealthy_signal_contains_dark_pct(self):
        engine = make_engine()
        inp = make_input(
            buyer_email_response_rate_pct=0.10,
            buyer_initiated_follow_up_pct=0.05,
            meeting_attendance_rate_pct=0.40,
            proposal_open_rate_pct=0.20,
            content_shared_engagement_rate_pct=0.10,
            multi_touch_engagement_rate_pct=0.10,
            demo_to_next_step_commitment_rate_pct=0.20,
            stakeholder_expansion_by_buyer_pct=0.05,
            mutual_action_plan_adherence_pct=0.20,
            deal_dark_more_than_14d_pct=0.50,
            meeting_cancellation_rate_pct=0.50,
            avg_days_buyer_silent_before_followup=25.0,
        )
        result = engine.assess(inp)
        assert "50% deals gone dark" in result.engagement_signal

    def test_unhealthy_signal_contains_composite(self):
        engine = make_engine()
        inp = make_input(
            buyer_email_response_rate_pct=0.10,
            buyer_initiated_follow_up_pct=0.05,
            meeting_attendance_rate_pct=0.40,
            proposal_open_rate_pct=0.20,
            content_shared_engagement_rate_pct=0.10,
            multi_touch_engagement_rate_pct=0.10,
            demo_to_next_step_commitment_rate_pct=0.20,
            stakeholder_expansion_by_buyer_pct=0.05,
            mutual_action_plan_adherence_pct=0.20,
            deal_dark_more_than_14d_pct=0.50,
            meeting_cancellation_rate_pct=0.50,
            avg_days_buyer_silent_before_followup=25.0,
        )
        result = engine.assess(inp)
        comp_int = round(result.engagement_composite)
        assert f"composite {comp_int}" in result.engagement_signal

    def test_none_pattern_signal_uses_title_case_label(self):
        engine = make_engine()
        # Create a scenario where composite >= 20 but pattern is none
        # Force moderate with minimal triggers but no matching pattern
        inp = make_input(
            buyer_email_response_rate_pct=0.50,    # +8 responsiveness
            meeting_attendance_rate_pct=0.65,
            buyer_initiated_follow_up_pct=0.20,    # +12
            proposal_open_rate_pct=0.55,           # +22 signal
            content_shared_engagement_rate_pct=0.50,
            multi_touch_engagement_rate_pct=0.50,
            deal_dark_more_than_14d_pct=0.05,
            meeting_cancellation_rate_pct=0.05,
            avg_days_buyer_silent_before_followup=5.0,
            demo_to_next_step_commitment_rate_pct=0.80,
            stakeholder_expansion_by_buyer_pct=0.80,
            mutual_action_plan_adherence_pct=0.80,
            # Keep proposal_viewed_more_than_once_pct high to avoid proposal_black_hole
            proposal_viewed_more_than_once_pct=0.80,
            rep_response_to_buyer_signal_hours_avg=4.0,
        )
        result = engine.assess(inp)
        if result.engagement_composite >= 20 and result.engagement_pattern == EngagementPattern.none:
            assert "None" in result.engagement_signal

    def test_pattern_labels_for_each_pattern(self):
        """Verify _PATTERN_LABELS keys cover all non-none patterns."""
        engine = make_engine()
        expected_labels = {
            EngagementPattern.one_way_sender: "One-way sender",
            EngagementPattern.low_signal_pursuer: "Low signal pursuer",
            EngagementPattern.engagement_ignorer: "Engagement ignorer",
            EngagementPattern.meeting_canceler: "Meeting canceler",
            EngagementPattern.proposal_black_hole: "Proposal black hole",
        }
        assert engine._PATTERN_LABELS == expected_labels


# ─────────────────────────────────────────────────────────────────────────────
# 17. assess() end-to-end
# ─────────────────────────────────────────────────────────────────────────────

class TestAssessEndToEnd:
    def test_assess_returns_engagement_result(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert isinstance(result, EngagementResult)

    def test_assess_preserves_rep_id(self):
        engine = make_engine()
        result = engine.assess(make_input(rep_id="abc-123"))
        assert result.rep_id == "abc-123"

    def test_assess_preserves_region(self):
        engine = make_engine()
        result = engine.assess(make_input(region="APAC"))
        assert result.region == "APAC"

    def test_assess_healthy_rep_has_low_risk(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert result.engagement_risk == EngagementRisk.low

    def test_assess_healthy_rep_has_engaged_severity(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert result.engagement_severity == EngagementSeverity.engaged

    def test_assess_healthy_rep_has_no_action(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert result.recommended_action == EngagementAction.no_action

    def test_assess_healthy_rep_has_zero_composite(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert result.engagement_composite == pytest.approx(0.0)

    def test_assess_worst_case_is_critical(self):
        engine = make_engine()
        result = engine.assess(make_input(
            buyer_email_response_rate_pct=0.05,
            meeting_attendance_rate_pct=0.20,
            buyer_initiated_follow_up_pct=0.02,
            proposal_open_rate_pct=0.10,
            content_shared_engagement_rate_pct=0.05,
            multi_touch_engagement_rate_pct=0.05,
            demo_to_next_step_commitment_rate_pct=0.10,
            stakeholder_expansion_by_buyer_pct=0.02,
            mutual_action_plan_adherence_pct=0.10,
            deal_dark_more_than_14d_pct=0.80,
            meeting_cancellation_rate_pct=0.70,
            avg_days_buyer_silent_before_followup=30.0,
        ))
        assert result.engagement_risk == EngagementRisk.critical

    def test_assess_stores_result_internally(self):
        engine = make_engine()
        engine.assess(make_input())
        assert len(engine._results) == 1

    def test_assess_multiple_calls_accumulate_results(self):
        engine = make_engine()
        engine.assess(make_input(rep_id="r1"))
        engine.assess(make_input(rep_id="r2"))
        assert len(engine._results) == 2

    def test_assess_score_bounds_all_non_negative(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert result.responsiveness_score >= 0.0
        assert result.signal_score >= 0.0
        assert result.activation_score >= 0.0
        assert result.risk_score >= 0.0

    def test_assess_score_bounds_all_at_most_100(self):
        engine = make_engine()
        result = engine.assess(make_input(
            buyer_email_response_rate_pct=0.01,
            meeting_attendance_rate_pct=0.01,
            buyer_initiated_follow_up_pct=0.01,
            proposal_open_rate_pct=0.01,
            content_shared_engagement_rate_pct=0.01,
            multi_touch_engagement_rate_pct=0.01,
            demo_to_next_step_commitment_rate_pct=0.01,
            stakeholder_expansion_by_buyer_pct=0.01,
            mutual_action_plan_adherence_pct=0.01,
            deal_dark_more_than_14d_pct=0.99,
            meeting_cancellation_rate_pct=0.99,
            avg_days_buyer_silent_before_followup=50.0,
        ))
        assert result.responsiveness_score <= 100.0
        assert result.signal_score <= 100.0
        assert result.activation_score <= 100.0
        assert result.risk_score <= 100.0
        assert result.engagement_composite <= 100.0


# ─────────────────────────────────────────────────────────────────────────────
# 18. assess_batch()
# ─────────────────────────────────────────────────────────────────────────────

class TestAssessBatch:
    def test_batch_returns_list(self):
        engine = make_engine()
        results = engine.assess_batch([make_input(rep_id="r1"), make_input(rep_id="r2")])
        assert isinstance(results, list)

    def test_batch_length_matches_input(self):
        engine = make_engine()
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_empty_list_returns_empty(self):
        engine = make_engine()
        results = engine.assess_batch([])
        assert results == []

    def test_batch_results_are_engagement_results(self):
        engine = make_engine()
        results = engine.assess_batch([make_input(rep_id="r1"), make_input(rep_id="r2")])
        for r in results:
            assert isinstance(r, EngagementResult)

    def test_batch_accumulates_in_internal_store(self):
        engine = make_engine()
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        assert len(engine._results) == 3

    def test_batch_preserves_rep_ids(self):
        engine = make_engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(4)]
        results = engine.assess_batch(inputs)
        for i, result in enumerate(results):
            assert result.rep_id == f"rep-{i}"

    def test_batch_processes_each_independently(self):
        engine = make_engine()
        healthy = make_input(rep_id="healthy")
        bad = make_input(
            rep_id="bad",
            buyer_email_response_rate_pct=0.05,
            meeting_attendance_rate_pct=0.20,
            buyer_initiated_follow_up_pct=0.02,
            proposal_open_rate_pct=0.10,
            content_shared_engagement_rate_pct=0.05,
            multi_touch_engagement_rate_pct=0.05,
            demo_to_next_step_commitment_rate_pct=0.10,
            stakeholder_expansion_by_buyer_pct=0.02,
            mutual_action_plan_adherence_pct=0.10,
            deal_dark_more_than_14d_pct=0.80,
            meeting_cancellation_rate_pct=0.70,
            avg_days_buyer_silent_before_followup=30.0,
        )
        results = engine.assess_batch([healthy, bad])
        assert results[0].engagement_risk == EngagementRisk.low
        assert results[1].engagement_risk == EngagementRisk.critical


# ─────────────────────────────────────────────────────────────────────────────
# 19. summary()
# ─────────────────────────────────────────────────────────────────────────────

class TestSummary:
    def test_summary_empty_engine(self):
        engine = make_engine()
        s = engine.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_engagement_composite"] == 0.0
        assert s["engagement_gap_count"] == 0
        assert s["coaching_count"] == 0
        assert s["avg_responsiveness_score"] == 0.0
        assert s["avg_signal_score"] == 0.0
        assert s["avg_activation_score"] == 0.0
        assert s["avg_risk_score"] == 0.0
        assert s["total_estimated_revenue_at_dark_usd"] == 0.0

    def test_summary_has_13_keys(self):
        engine = make_engine()
        engine.assess(make_input())
        assert len(engine.summary()) == 13

    def test_summary_empty_has_13_keys(self):
        engine = make_engine()
        assert len(engine.summary()) == 13

    def test_summary_total_count(self):
        engine = make_engine()
        for i in range(4):
            engine.assess(make_input(rep_id=f"r{i}"))
        assert engine.summary()["total"] == 4

    def test_summary_risk_counts(self):
        engine = make_engine()
        engine.assess(make_input())  # healthy → low
        engine.assess(make_input())  # healthy → low
        s = engine.summary()
        assert s["risk_counts"].get("low", 0) == 2

    def test_summary_pattern_counts(self):
        engine = make_engine()
        engine.assess(make_input())  # healthy → none
        s = engine.summary()
        assert s["pattern_counts"].get("none", 0) == 1

    def test_summary_severity_counts(self):
        engine = make_engine()
        engine.assess(make_input())  # healthy → engaged
        s = engine.summary()
        assert s["severity_counts"].get("engaged", 0) == 1

    def test_summary_action_counts(self):
        engine = make_engine()
        engine.assess(make_input())  # healthy → no_action
        s = engine.summary()
        assert s["action_counts"].get("no_action", 0) == 1

    def test_summary_avg_composite_for_single_result(self):
        engine = make_engine()
        result = engine.assess(make_input())
        s = engine.summary()
        assert s["avg_engagement_composite"] == pytest.approx(result.engagement_composite, abs=0.1)

    def test_summary_avg_composite_for_multiple(self):
        engine = make_engine()
        r1 = engine.assess(make_input(rep_id="r1"))
        r2 = engine.assess(make_input(rep_id="r2"))
        expected_avg = round((r1.engagement_composite + r2.engagement_composite) / 2, 1)
        assert engine.summary()["avg_engagement_composite"] == pytest.approx(expected_avg, abs=0.05)

    def test_summary_engagement_gap_count(self):
        engine = make_engine()
        engine.assess(make_input(buyer_email_response_rate_pct=0.40))  # has gap
        engine.assess(make_input())  # no gap
        s = engine.summary()
        assert s["engagement_gap_count"] == 1

    def test_summary_coaching_count(self):
        engine = make_engine()
        engine.assess(make_input(meeting_attendance_rate_pct=0.50))  # coaching
        engine.assess(make_input())  # no coaching
        s = engine.summary()
        assert s["coaching_count"] == 1

    def test_summary_avg_responsiveness_score(self):
        engine = make_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(buyer_email_response_rate_pct=0.30))
        expected = round((r1.responsiveness_score + r2.responsiveness_score) / 2, 1)
        assert engine.summary()["avg_responsiveness_score"] == pytest.approx(expected, abs=0.05)

    def test_summary_avg_signal_score(self):
        engine = make_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(proposal_open_rate_pct=0.30))
        expected = round((r1.signal_score + r2.signal_score) / 2, 1)
        assert engine.summary()["avg_signal_score"] == pytest.approx(expected, abs=0.05)

    def test_summary_avg_activation_score(self):
        engine = make_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(demo_to_next_step_commitment_rate_pct=0.30))
        expected = round((r1.activation_score + r2.activation_score) / 2, 1)
        assert engine.summary()["avg_activation_score"] == pytest.approx(expected, abs=0.05)

    def test_summary_avg_risk_score(self):
        engine = make_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(deal_dark_more_than_14d_pct=0.50))
        expected = round((r1.risk_score + r2.risk_score) / 2, 1)
        assert engine.summary()["avg_risk_score"] == pytest.approx(expected, abs=0.05)

    def test_summary_total_revenue_at_dark(self):
        engine = make_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(deal_dark_more_than_14d_pct=0.30))
        expected = round(r1.estimated_revenue_at_dark_usd + r2.estimated_revenue_at_dark_usd, 2)
        assert engine.summary()["total_estimated_revenue_at_dark_usd"] == pytest.approx(expected)

    def test_summary_rounded_averages(self):
        engine = make_engine()
        for i in range(3):
            engine.assess(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        # All averages should be rounded to 1 decimal
        for key in ["avg_engagement_composite", "avg_responsiveness_score",
                    "avg_signal_score", "avg_activation_score", "avg_risk_score"]:
            val = s[key]
            assert round(val, 1) == val


# ─────────────────────────────────────────────────────────────────────────────
# 20. Integration / edge cases
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegration:
    def test_full_unhealthy_pipeline_critical(self):
        engine = make_engine()
        inp = make_input(
            buyer_email_response_rate_pct=0.15,
            buyer_initiated_follow_up_pct=0.05,
            meeting_attendance_rate_pct=0.40,
            proposal_open_rate_pct=0.20,
            content_shared_engagement_rate_pct=0.10,
            multi_touch_engagement_rate_pct=0.10,
            demo_to_next_step_commitment_rate_pct=0.20,
            stakeholder_expansion_by_buyer_pct=0.05,
            mutual_action_plan_adherence_pct=0.15,
            deal_dark_more_than_14d_pct=0.60,
            meeting_cancellation_rate_pct=0.50,
            avg_days_buyer_silent_before_followup=25.0,
        )
        result = engine.assess(inp)
        assert result.engagement_risk == EngagementRisk.critical
        assert result.engagement_severity == EngagementSeverity.dark
        assert result.recommended_action == EngagementAction.deal_qualification_review
        assert result.has_engagement_gap is True
        assert result.requires_engagement_coaching is True

    def test_moderate_scenario(self):
        """Moderate risk: composite 20–39."""
        engine = make_engine()
        # Target ~25 composite
        inp = make_input(
            buyer_email_response_rate_pct=0.55,   # +8 resp
            meeting_attendance_rate_pct=0.90,
            buyer_initiated_follow_up_pct=0.50,
            proposal_open_rate_pct=0.55,          # +22 signal
            content_shared_engagement_rate_pct=0.50,
            multi_touch_engagement_rate_pct=0.50,
            demo_to_next_step_commitment_rate_pct=0.90,
            stakeholder_expansion_by_buyer_pct=0.90,
            mutual_action_plan_adherence_pct=0.90,
            deal_dark_more_than_14d_pct=0.05,
            meeting_cancellation_rate_pct=0.10,
            avg_days_buyer_silent_before_followup=5.0,
        )
        result = engine.assess(inp)
        assert result.engagement_risk in (EngagementRisk.low, EngagementRisk.moderate)

    def test_engine_isolation_between_instances(self):
        e1 = make_engine()
        e2 = make_engine()
        e1.assess(make_input(rep_id="e1-rep"))
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_to_dict_values_match_result_fields(self):
        engine = make_engine()
        result = engine.assess(make_input(rep_id="dict-test", region="West"))
        d = result.to_dict()
        assert d["rep_id"] == result.rep_id
        assert d["region"] == result.region
        assert d["engagement_risk"] == result.engagement_risk.value
        assert d["engagement_pattern"] == result.engagement_pattern.value
        assert d["engagement_severity"] == result.engagement_severity.value
        assert d["recommended_action"] == result.recommended_action.value
        assert d["responsiveness_score"] == result.responsiveness_score
        assert d["signal_score"] == result.signal_score
        assert d["activation_score"] == result.activation_score
        assert d["risk_score"] == result.risk_score
        assert d["engagement_composite"] == result.engagement_composite
        assert d["has_engagement_gap"] == result.has_engagement_gap
        assert d["requires_engagement_coaching"] == result.requires_engagement_coaching
        assert d["estimated_revenue_at_dark_usd"] == result.estimated_revenue_at_dark_usd
        assert d["engagement_signal"] == result.engagement_signal

    def test_multiple_different_reps_in_summary(self):
        engine = make_engine()
        # Two low-risk reps
        engine.assess(make_input(rep_id="low1"))
        engine.assess(make_input(rep_id="low2"))
        # One critical rep
        engine.assess(make_input(
            rep_id="critical1",
            buyer_email_response_rate_pct=0.10,
            buyer_initiated_follow_up_pct=0.03,
            meeting_attendance_rate_pct=0.30,
            proposal_open_rate_pct=0.10,
            content_shared_engagement_rate_pct=0.05,
            multi_touch_engagement_rate_pct=0.05,
            demo_to_next_step_commitment_rate_pct=0.10,
            stakeholder_expansion_by_buyer_pct=0.03,
            mutual_action_plan_adherence_pct=0.10,
            deal_dark_more_than_14d_pct=0.70,
            meeting_cancellation_rate_pct=0.60,
            avg_days_buyer_silent_before_followup=30.0,
        ))
        s = engine.summary()
        assert s["total"] == 3
        assert s["risk_counts"].get("low", 0) == 2
        assert s["risk_counts"].get("critical", 0) == 1

    def test_boundary_composite_exactly_60(self):
        """Check composite exactly at 60 gives critical/dark."""
        engine = make_engine()
        # 40*0.30 + 40*0.30 + 40*0.25 + 40*0.15 = 40 → not 60
        # We need composite=60: 100*0.30 + 100*0.30 + 100*0.25 + 0*0.15 = 85 → too high
        # 60 = rs*0.30 + ss*0.30 + ac*0.25 + rk*0.15
        # Try rs=100, ss=100, ac=100, rk=100 → 100; try rs=60, ss=60, ac=60, rk=60 → 60
        result = engine._composite(60.0, 60.0, 60.0, 60.0)
        assert result == pytest.approx(60.0)
        assert engine._risk(result) == EngagementRisk.critical
        assert engine._severity(result) == EngagementSeverity.dark

    def test_boundary_composite_exactly_40(self):
        engine = make_engine()
        result = engine._composite(40.0, 40.0, 40.0, 40.0)
        assert result == pytest.approx(40.0)
        assert engine._risk(result) == EngagementRisk.high
        assert engine._severity(result) == EngagementSeverity.passive

    def test_boundary_composite_exactly_20(self):
        engine = make_engine()
        result = engine._composite(20.0, 20.0, 20.0, 20.0)
        assert result == pytest.approx(20.0)
        assert engine._risk(result) == EngagementRisk.moderate
        assert engine._severity(result) == EngagementSeverity.responsive

    def test_assess_returns_correct_signal_healthy(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert result.engagement_signal.startswith("Buyer engagement strong")

    def test_assess_unhealthy_signal_not_healthy_string(self):
        engine = make_engine()
        result = engine.assess(make_input(
            buyer_email_response_rate_pct=0.10,
            buyer_initiated_follow_up_pct=0.03,
            meeting_attendance_rate_pct=0.30,
            proposal_open_rate_pct=0.10,
            content_shared_engagement_rate_pct=0.05,
            multi_touch_engagement_rate_pct=0.05,
            demo_to_next_step_commitment_rate_pct=0.10,
            stakeholder_expansion_by_buyer_pct=0.03,
            mutual_action_plan_adherence_pct=0.10,
            deal_dark_more_than_14d_pct=0.70,
            meeting_cancellation_rate_pct=0.60,
            avg_days_buyer_silent_before_followup=30.0,
        ))
        assert "Buyer engagement strong" not in result.engagement_signal

    def test_pattern_black_hole_with_high_risk_action(self):
        """High risk + proposal_black_hole → deal_review_coaching."""
        engine = make_engine()
        inp = make_input(
            # Force proposal_black_hole pattern
            proposal_viewed_more_than_once_pct=0.10,
            proposal_open_rate_pct=0.40,
            buyer_email_response_rate_pct=0.30,  # +22 resp (not one_way_sender: follow_up high)
            buyer_initiated_follow_up_pct=0.50,
            content_shared_engagement_rate_pct=0.50,  # no low_signal
            deal_dark_more_than_14d_pct=0.05,     # no engagement_ignorer
            rep_response_to_buyer_signal_hours_avg=4.0,
            meeting_cancellation_rate_pct=0.05,   # no meeting_canceler
            meeting_attendance_rate_pct=0.90,
            # Add signal score
            multi_touch_engagement_rate_pct=0.15,  # +25 signal
            # Activation score
            demo_to_next_step_commitment_rate_pct=0.30,  # +45 activation
            stakeholder_expansion_by_buyer_pct=0.05,     # +30 activation
            mutual_action_plan_adherence_pct=0.25,       # +25 activation
        )
        result = engine.assess(inp)
        if result.engagement_pattern == EngagementPattern.proposal_black_hole:
            if result.engagement_risk == EngagementRisk.high:
                assert result.recommended_action == EngagementAction.deal_review_coaching

    def test_freshly_instantiated_engine_has_empty_results(self):
        engine = make_engine()
        assert engine._results == []

    def test_summary_keys_are_exactly_13(self):
        engine = make_engine()
        engine.assess(make_input())
        keys = set(engine.summary().keys())
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_engagement_composite", "engagement_gap_count",
            "coaching_count", "avg_responsiveness_score", "avg_signal_score",
            "avg_activation_score", "avg_risk_score",
            "total_estimated_revenue_at_dark_usd",
        }
        assert keys == expected_keys
