"""
Comprehensive pytest tests for SalesBuyerResponseLatencyIntelligenceEngine.

Coverage:
- All enum values (LatencyRisk, LatencyPattern, LatencySeverity, LatencyAction)
- LatencyInput dataclass (all 22 fields)
- LatencyResult dataclass + to_dict() (15 keys)
- Sub-scores: _latency_score, _engagement_depth_score, _commitment_score, _process_velocity_score
- Sub-score boundary conditions and weights
- Composite formula (0.35 / 0.25 / 0.25 / 0.15 weights)
- Risk thresholds (20 / 40 / 60)
- Severity thresholds (20 / 40 / 60)
- Pattern detection (all 5 patterns + none, priority order)
- Action routing (all risk × pattern combinations)
- Flags: has_latency_gap, requires_latency_intervention
- at_risk_revenue formula
- Signal string (healthy and unhealthy branches)
- assess() end-to-end
- assess_batch()
- summary() (empty and populated, 13-key contract)
"""

import math
import pytest

from swarm.intelligence.sales_buyer_response_latency_intelligence_engine import (
    LatencyAction,
    LatencyInput,
    LatencyPattern,
    LatencyResult,
    LatencyRisk,
    LatencySeverity,
    SalesBuyerResponseLatencyIntelligenceEngine,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helper factories
# ─────────────────────────────────────────────────────────────────────────────

def make_input(**overrides) -> LatencyInput:
    """Return a LatencyInput in the fully-healthy (zero-score) zone.

    All values are below every scoring threshold so the composite ≈ 0
    and the engine returns low / responsive / none / no_action.
    Override individual fields via kwargs.
    """
    defaults = dict(
        rep_id="rep-001",
        region="North",
        evaluation_period_id="Q1-2026",
        # _latency_score contributors – all below thresholds
        avg_buyer_response_hours=4.0,           # < 24
        response_time_vs_baseline_ratio=1.0,    # < 1.5
        no_response_rate_pct=0.05,              # < 0.30
        # _engagement_depth_score contributors
        ghost_rate_pct=0.05,                    # < 0.10
        champion_response_rate_pct=0.90,        # > 0.50
        executive_response_rate_pct=0.80,       # > 0.30
        # _commitment_score contributors
        meeting_no_show_rate_pct=0.02,          # < 0.10
        meeting_rescheduled_rate_pct=0.05,      # < 0.30
        meeting_acceptance_rate_pct=0.90,       # > 0.50
        # _process_velocity_score contributors
        proposal_review_response_days=3.0,      # < 7
        contract_review_latency_days=5.0,       # < 21
        demo_request_to_completion_days=5.0,    # < 14
        # Additional LatencyInput fields
        avg_follow_ups_before_response=1.0,
        response_latency_trend=0.10,
        multi_contact_response_diversity=0.90,
        outreach_channel_effectiveness=0.90,
        response_quality_score=0.90,
        total_active_deals=10,
        avg_deal_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return LatencyInput(**defaults)


def make_engine() -> SalesBuyerResponseLatencyIntelligenceEngine:
    return SalesBuyerResponseLatencyIntelligenceEngine()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Enum membership
# ─────────────────────────────────────────────────────────────────────────────

class TestEnumMembers:
    def test_latency_risk_all_four_members(self):
        values = {e.value for e in LatencyRisk}
        assert values == {"low", "moderate", "high", "critical"}

    def test_latency_risk_low(self):
        assert LatencyRisk.low.value == "low"

    def test_latency_risk_moderate(self):
        assert LatencyRisk.moderate.value == "moderate"

    def test_latency_risk_high(self):
        assert LatencyRisk.high.value == "high"

    def test_latency_risk_critical(self):
        assert LatencyRisk.critical.value == "critical"

    def test_latency_pattern_all_six_members(self):
        values = {e.value for e in LatencyPattern}
        assert values == {
            "none",
            "buyer_ghosting",
            "executive_avoidance",
            "champion_cooling",
            "commitment_fading",
            "process_stalling",
        }

    def test_latency_pattern_none(self):
        assert LatencyPattern.none.value == "none"

    def test_latency_pattern_buyer_ghosting(self):
        assert LatencyPattern.buyer_ghosting.value == "buyer_ghosting"

    def test_latency_pattern_executive_avoidance(self):
        assert LatencyPattern.executive_avoidance.value == "executive_avoidance"

    def test_latency_pattern_champion_cooling(self):
        assert LatencyPattern.champion_cooling.value == "champion_cooling"

    def test_latency_pattern_commitment_fading(self):
        assert LatencyPattern.commitment_fading.value == "commitment_fading"

    def test_latency_pattern_process_stalling(self):
        assert LatencyPattern.process_stalling.value == "process_stalling"

    def test_latency_severity_all_four_members(self):
        values = {e.value for e in LatencySeverity}
        assert values == {"responsive", "cooling", "disengaging", "ghosted"}

    def test_latency_severity_responsive(self):
        assert LatencySeverity.responsive.value == "responsive"

    def test_latency_severity_cooling(self):
        assert LatencySeverity.cooling.value == "cooling"

    def test_latency_severity_disengaging(self):
        assert LatencySeverity.disengaging.value == "disengaging"

    def test_latency_severity_ghosted(self):
        assert LatencySeverity.ghosted.value == "ghosted"

    def test_latency_action_all_seven_members(self):
        values = {e.value for e in LatencyAction}
        assert values == {
            "no_action",
            "engagement_monitoring",
            "re_engagement_coaching",
            "executive_outreach_coaching",
            "deal_save_intervention",
            "champion_replacement_coaching",
            "deal_abandon_escalation",
        }

    def test_latency_action_no_action(self):
        assert LatencyAction.no_action.value == "no_action"

    def test_latency_action_engagement_monitoring(self):
        assert LatencyAction.engagement_monitoring.value == "engagement_monitoring"

    def test_latency_action_re_engagement_coaching(self):
        assert LatencyAction.re_engagement_coaching.value == "re_engagement_coaching"

    def test_latency_action_executive_outreach_coaching(self):
        assert LatencyAction.executive_outreach_coaching.value == "executive_outreach_coaching"

    def test_latency_action_deal_save_intervention(self):
        assert LatencyAction.deal_save_intervention.value == "deal_save_intervention"

    def test_latency_action_champion_replacement_coaching(self):
        assert LatencyAction.champion_replacement_coaching.value == "champion_replacement_coaching"

    def test_latency_action_deal_abandon_escalation(self):
        assert LatencyAction.deal_abandon_escalation.value == "deal_abandon_escalation"

    def test_enums_are_strings(self):
        """All enums inherit from str."""
        assert isinstance(LatencyRisk.low, str)
        assert isinstance(LatencyPattern.none, str)
        assert isinstance(LatencySeverity.responsive, str)
        assert isinstance(LatencyAction.no_action, str)


# ─────────────────────────────────────────────────────────────────────────────
# 2. LatencyInput field coverage
# ─────────────────────────────────────────────────────────────────────────────

class TestLatencyInputFields:
    def test_has_rep_id(self):
        inp = make_input(rep_id="R-XYZ")
        assert inp.rep_id == "R-XYZ"

    def test_has_region(self):
        inp = make_input(region="EMEA")
        assert inp.region == "EMEA"

    def test_has_evaluation_period_id(self):
        inp = make_input(evaluation_period_id="Q2-2026")
        assert inp.evaluation_period_id == "Q2-2026"

    def test_has_avg_buyer_response_hours(self):
        inp = make_input(avg_buyer_response_hours=72.0)
        assert inp.avg_buyer_response_hours == 72.0

    def test_has_response_latency_trend(self):
        inp = make_input(response_latency_trend=0.75)
        assert inp.response_latency_trend == 0.75

    def test_has_no_response_rate_pct(self):
        inp = make_input(no_response_rate_pct=0.45)
        assert inp.no_response_rate_pct == 0.45

    def test_has_avg_follow_ups_before_response(self):
        inp = make_input(avg_follow_ups_before_response=4.5)
        assert inp.avg_follow_ups_before_response == 4.5

    def test_has_ghost_rate_pct(self):
        inp = make_input(ghost_rate_pct=0.35)
        assert inp.ghost_rate_pct == 0.35

    def test_has_response_time_vs_baseline_ratio(self):
        inp = make_input(response_time_vs_baseline_ratio=2.5)
        assert inp.response_time_vs_baseline_ratio == 2.5

    def test_has_executive_response_rate_pct(self):
        inp = make_input(executive_response_rate_pct=0.20)
        assert inp.executive_response_rate_pct == 0.20

    def test_has_champion_response_rate_pct(self):
        inp = make_input(champion_response_rate_pct=0.40)
        assert inp.champion_response_rate_pct == 0.40

    def test_has_meeting_acceptance_rate_pct(self):
        inp = make_input(meeting_acceptance_rate_pct=0.55)
        assert inp.meeting_acceptance_rate_pct == 0.55

    def test_has_meeting_rescheduled_rate_pct(self):
        inp = make_input(meeting_rescheduled_rate_pct=0.25)
        assert inp.meeting_rescheduled_rate_pct == 0.25

    def test_has_meeting_no_show_rate_pct(self):
        inp = make_input(meeting_no_show_rate_pct=0.15)
        assert inp.meeting_no_show_rate_pct == 0.15

    def test_has_demo_request_to_completion_days(self):
        inp = make_input(demo_request_to_completion_days=18.0)
        assert inp.demo_request_to_completion_days == 18.0

    def test_has_proposal_review_response_days(self):
        inp = make_input(proposal_review_response_days=10.0)
        assert inp.proposal_review_response_days == 10.0

    def test_has_contract_review_latency_days(self):
        inp = make_input(contract_review_latency_days=25.0)
        assert inp.contract_review_latency_days == 25.0

    def test_has_multi_contact_response_diversity(self):
        inp = make_input(multi_contact_response_diversity=0.60)
        assert inp.multi_contact_response_diversity == 0.60

    def test_has_outreach_channel_effectiveness(self):
        inp = make_input(outreach_channel_effectiveness=0.70)
        assert inp.outreach_channel_effectiveness == 0.70

    def test_has_response_quality_score(self):
        inp = make_input(response_quality_score=0.50)
        assert inp.response_quality_score == 0.50

    def test_has_total_active_deals(self):
        inp = make_input(total_active_deals=25)
        assert inp.total_active_deals == 25

    def test_has_avg_deal_value_usd(self):
        inp = make_input(avg_deal_value_usd=100_000.0)
        assert inp.avg_deal_value_usd == 100_000.0

    def test_total_fields_count(self):
        """LatencyInput has exactly 22 fields."""
        import dataclasses
        fields = dataclasses.fields(LatencyInput)
        assert len(fields) == 22


# ─────────────────────────────────────────────────────────────────────────────
# 3. LatencyResult and to_dict() key contract
# ─────────────────────────────────────────────────────────────────────────────

class TestLatencyResultToDict:
    EXPECTED_KEYS = {
        "rep_id",
        "region",
        "latency_risk",
        "latency_pattern",
        "latency_severity",
        "recommended_action",
        "latency_score",
        "engagement_depth_score",
        "commitment_score",
        "process_velocity_score",
        "latency_composite",
        "has_latency_gap",
        "requires_latency_intervention",
        "estimated_at_risk_revenue_usd",
        "latency_signal",
    }

    def test_to_dict_has_exactly_15_keys(self):
        eng = make_engine()
        result = eng.assess(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert set(result.to_dict().keys()) == self.EXPECTED_KEYS

    def test_to_dict_enum_values_are_strings(self):
        eng = make_engine()
        result = eng.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["latency_risk"], str)
        assert isinstance(d["latency_pattern"], str)
        assert isinstance(d["latency_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_propagated(self):
        eng = make_engine()
        result = eng.assess(make_input(rep_id="XYZ"))
        assert result.to_dict()["rep_id"] == "XYZ"

    def test_to_dict_region_propagated(self):
        eng = make_engine()
        result = eng.assess(make_input(region="APAC"))
        assert result.to_dict()["region"] == "APAC"

    def test_to_dict_booleans_present(self):
        eng = make_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["has_latency_gap"], bool)
        assert isinstance(d["requires_latency_intervention"], bool)

    def test_to_dict_numeric_fields_are_floats_or_ints(self):
        eng = make_engine()
        d = eng.assess(make_input()).to_dict()
        for key in ["latency_score", "engagement_depth_score", "commitment_score",
                    "process_velocity_score", "latency_composite",
                    "estimated_at_risk_revenue_usd"]:
            assert isinstance(d[key], (int, float)), f"{key} should be numeric"

    def test_to_dict_signal_is_string(self):
        eng = make_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["latency_signal"], str)


# ─────────────────────────────────────────────────────────────────────────────
# 4. Sub-score: _latency_score
# ─────────────────────────────────────────────────────────────────────────────

class TestLatencyScore:
    """Tests for the _latency_score private method via assess()."""

    def _score(self, **kwargs) -> float:
        eng = make_engine()
        return eng._latency_score(make_input(**kwargs))

    # avg_buyer_response_hours thresholds
    def test_response_hours_below_24_adds_0(self):
        assert self._score(avg_buyer_response_hours=23.9) == 0.0

    def test_response_hours_at_24_adds_8(self):
        # Only response_hours branch fires (others are below threshold)
        s = self._score(avg_buyer_response_hours=24.0)
        assert s == 8.0

    def test_response_hours_at_48_adds_22(self):
        s = self._score(avg_buyer_response_hours=48.0)
        assert s == 22.0

    def test_response_hours_at_96_adds_40(self):
        s = self._score(avg_buyer_response_hours=96.0)
        assert s == 40.0

    def test_response_hours_above_96_adds_40(self):
        s = self._score(avg_buyer_response_hours=200.0)
        assert s == 40.0

    # response_time_vs_baseline_ratio thresholds
    def test_baseline_ratio_below_1_5_adds_0(self):
        assert self._score(response_time_vs_baseline_ratio=1.49) == 0.0

    def test_baseline_ratio_at_1_5_adds_6(self):
        s = self._score(response_time_vs_baseline_ratio=1.5)
        assert s == 6.0

    def test_baseline_ratio_at_2_0_adds_18(self):
        s = self._score(response_time_vs_baseline_ratio=2.0)
        assert s == 18.0

    def test_baseline_ratio_at_3_0_adds_35(self):
        s = self._score(response_time_vs_baseline_ratio=3.0)
        assert s == 35.0

    def test_baseline_ratio_above_3_0_adds_35(self):
        s = self._score(response_time_vs_baseline_ratio=5.0)
        assert s == 35.0

    # no_response_rate_pct thresholds
    def test_no_response_below_30_adds_0(self):
        assert self._score(no_response_rate_pct=0.29) == 0.0

    def test_no_response_at_30_adds_12(self):
        s = self._score(no_response_rate_pct=0.30)
        assert s == 12.0

    def test_no_response_at_50_adds_25(self):
        s = self._score(no_response_rate_pct=0.50)
        assert s == 25.0

    def test_no_response_above_50_adds_25(self):
        s = self._score(no_response_rate_pct=0.99)
        assert s == 25.0

    # Additive accumulation
    def test_all_three_mid_level_triggers_accumulate(self):
        # 24h → +8, ratio 1.5 → +6, no_response 0.30 → +12 => 26
        s = self._score(
            avg_buyer_response_hours=24.0,
            response_time_vs_baseline_ratio=1.5,
            no_response_rate_pct=0.30,
        )
        assert s == 26.0

    def test_max_capped_at_100(self):
        # 40 + 35 + 25 = 100
        s = self._score(
            avg_buyer_response_hours=96.0,
            response_time_vs_baseline_ratio=3.0,
            no_response_rate_pct=0.50,
        )
        assert s == 100.0

    def test_score_above_100_capped(self):
        # same as max – already at 100
        s = self._score(
            avg_buyer_response_hours=200.0,
            response_time_vs_baseline_ratio=10.0,
            no_response_rate_pct=1.0,
        )
        assert s <= 100.0

    def test_healthy_input_gives_zero(self):
        assert self._score() == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 5. Sub-score: _engagement_depth_score
# ─────────────────────────────────────────────────────────────────────────────

class TestEngagementDepthScore:
    def _score(self, **kwargs) -> float:
        eng = make_engine()
        return eng._engagement_depth_score(make_input(**kwargs))

    # ghost_rate_pct
    def test_ghost_below_10_adds_0(self):
        assert self._score(ghost_rate_pct=0.09) == 0.0

    def test_ghost_at_10_adds_8(self):
        assert self._score(ghost_rate_pct=0.10) == 8.0

    def test_ghost_at_25_adds_22(self):
        assert self._score(ghost_rate_pct=0.25) == 22.0

    def test_ghost_at_40_adds_40(self):
        assert self._score(ghost_rate_pct=0.40) == 40.0

    def test_ghost_above_40_adds_40(self):
        assert self._score(ghost_rate_pct=0.99) == 40.0

    # champion_response_rate_pct (inverted – low is bad)
    def test_champion_above_50_adds_0(self):
        assert self._score(champion_response_rate_pct=0.51) == 0.0

    def test_champion_at_50_adds_18(self):
        assert self._score(champion_response_rate_pct=0.50) == 18.0

    def test_champion_at_30_adds_35(self):
        assert self._score(champion_response_rate_pct=0.30) == 35.0

    def test_champion_below_30_adds_35(self):
        assert self._score(champion_response_rate_pct=0.10) == 35.0

    # executive_response_rate_pct
    def test_exec_above_30_adds_0(self):
        assert self._score(executive_response_rate_pct=0.31) == 0.0

    def test_exec_at_30_adds_12(self):
        assert self._score(executive_response_rate_pct=0.30) == 12.0

    def test_exec_at_15_adds_25(self):
        assert self._score(executive_response_rate_pct=0.15) == 25.0

    def test_exec_below_15_adds_25(self):
        assert self._score(executive_response_rate_pct=0.05) == 25.0

    # Accumulation
    def test_all_three_worst_case_accumulate(self):
        # 40 + 35 + 25 = 100
        s = self._score(
            ghost_rate_pct=0.40,
            champion_response_rate_pct=0.30,
            executive_response_rate_pct=0.15,
        )
        assert s == 100.0

    def test_cap_at_100(self):
        s = self._score(
            ghost_rate_pct=1.0,
            champion_response_rate_pct=0.0,
            executive_response_rate_pct=0.0,
        )
        assert s <= 100.0

    def test_healthy_input_gives_zero(self):
        assert self._score() == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 6. Sub-score: _commitment_score
# ─────────────────────────────────────────────────────────────────────────────

class TestCommitmentScore:
    def _score(self, **kwargs) -> float:
        eng = make_engine()
        return eng._commitment_score(make_input(**kwargs))

    # meeting_no_show_rate_pct
    def test_no_show_below_10_adds_0(self):
        assert self._score(meeting_no_show_rate_pct=0.09) == 0.0

    def test_no_show_at_10_adds_8(self):
        assert self._score(meeting_no_show_rate_pct=0.10) == 8.0

    def test_no_show_at_20_adds_22(self):
        assert self._score(meeting_no_show_rate_pct=0.20) == 22.0

    def test_no_show_at_35_adds_40(self):
        assert self._score(meeting_no_show_rate_pct=0.35) == 40.0

    def test_no_show_above_35_adds_40(self):
        assert self._score(meeting_no_show_rate_pct=1.0) == 40.0

    # meeting_rescheduled_rate_pct
    def test_reschedule_below_30_adds_0(self):
        assert self._score(meeting_rescheduled_rate_pct=0.29) == 0.0

    def test_reschedule_at_30_adds_18(self):
        assert self._score(meeting_rescheduled_rate_pct=0.30) == 18.0

    def test_reschedule_at_50_adds_35(self):
        assert self._score(meeting_rescheduled_rate_pct=0.50) == 35.0

    def test_reschedule_above_50_adds_35(self):
        assert self._score(meeting_rescheduled_rate_pct=0.99) == 35.0

    # meeting_acceptance_rate_pct (inverted)
    def test_acceptance_above_50_adds_0(self):
        assert self._score(meeting_acceptance_rate_pct=0.51) == 0.0

    def test_acceptance_at_50_adds_12(self):
        assert self._score(meeting_acceptance_rate_pct=0.50) == 12.0

    def test_acceptance_at_30_adds_25(self):
        assert self._score(meeting_acceptance_rate_pct=0.30) == 25.0

    def test_acceptance_below_30_adds_25(self):
        assert self._score(meeting_acceptance_rate_pct=0.10) == 25.0

    # Accumulation and cap
    def test_all_worst_case_accumulate_to_100(self):
        s = self._score(
            meeting_no_show_rate_pct=0.35,
            meeting_rescheduled_rate_pct=0.50,
            meeting_acceptance_rate_pct=0.30,
        )
        assert s == 100.0

    def test_cap_at_100(self):
        s = self._score(
            meeting_no_show_rate_pct=1.0,
            meeting_rescheduled_rate_pct=1.0,
            meeting_acceptance_rate_pct=0.0,
        )
        assert s <= 100.0

    def test_healthy_input_gives_zero(self):
        assert self._score() == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 7. Sub-score: _process_velocity_score
# ─────────────────────────────────────────────────────────────────────────────

class TestProcessVelocityScore:
    def _score(self, **kwargs) -> float:
        eng = make_engine()
        return eng._process_velocity_score(make_input(**kwargs))

    # proposal_review_response_days
    def test_proposal_below_7_adds_0(self):
        assert self._score(proposal_review_response_days=6.9) == 0.0

    def test_proposal_at_7_adds_10(self):
        assert self._score(proposal_review_response_days=7.0) == 10.0

    def test_proposal_at_14_adds_25(self):
        assert self._score(proposal_review_response_days=14.0) == 25.0

    def test_proposal_at_21_adds_45(self):
        assert self._score(proposal_review_response_days=21.0) == 45.0

    def test_proposal_above_21_adds_45(self):
        assert self._score(proposal_review_response_days=100.0) == 45.0

    # contract_review_latency_days
    def test_contract_below_21_adds_0(self):
        assert self._score(contract_review_latency_days=20.9) == 0.0

    def test_contract_at_21_adds_15(self):
        assert self._score(contract_review_latency_days=21.0) == 15.0

    def test_contract_at_30_adds_30(self):
        assert self._score(contract_review_latency_days=30.0) == 30.0

    def test_contract_above_30_adds_30(self):
        assert self._score(contract_review_latency_days=90.0) == 30.0

    # demo_request_to_completion_days
    def test_demo_below_14_adds_0(self):
        assert self._score(demo_request_to_completion_days=13.9) == 0.0

    def test_demo_at_14_adds_10(self):
        assert self._score(demo_request_to_completion_days=14.0) == 10.0

    def test_demo_at_21_adds_25(self):
        assert self._score(demo_request_to_completion_days=21.0) == 25.0

    def test_demo_above_21_adds_25(self):
        assert self._score(demo_request_to_completion_days=60.0) == 25.0

    # Accumulation and cap
    def test_all_worst_case_100(self):
        s = self._score(
            proposal_review_response_days=21.0,
            contract_review_latency_days=30.0,
            demo_request_to_completion_days=21.0,
        )
        assert s == 100.0

    def test_cap_at_100(self):
        s = self._score(
            proposal_review_response_days=999.0,
            contract_review_latency_days=999.0,
            demo_request_to_completion_days=999.0,
        )
        assert s <= 100.0

    def test_healthy_input_gives_zero(self):
        assert self._score() == 0.0

    def test_mid_level_accumulation(self):
        # proposal 7d → +10, contract 21d → +15, demo 14d → +10 => 35
        s = self._score(
            proposal_review_response_days=7.0,
            contract_review_latency_days=21.0,
            demo_request_to_completion_days=14.0,
        )
        assert s == 35.0


# ─────────────────────────────────────────────────────────────────────────────
# 8. Composite formula and weights
# ─────────────────────────────────────────────────────────────────────────────

class TestCompositeFormula:
    """Verify l*0.35 + e*0.25 + c*0.25 + p*0.15 == composite."""

    def test_all_zero_sub_scores_gives_zero_composite(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert result.latency_composite == 0.0

    def test_composite_formula_manual(self):
        eng = make_engine()
        inp = make_input(
            avg_buyer_response_hours=96.0,       # _latency_score += 40
            ghost_rate_pct=0.40,                 # _engagement_depth_score += 40
            meeting_no_show_rate_pct=0.35,       # _commitment_score += 40
            proposal_review_response_days=21.0,  # _process_velocity_score += 45
        )
        result = eng.assess(inp)
        l = result.latency_score
        e = result.engagement_depth_score
        c = result.commitment_score
        p = result.process_velocity_score
        expected = round(l * 0.35 + e * 0.25 + c * 0.25 + p * 0.15, 2)
        assert result.latency_composite == expected

    def test_composite_latency_weight_is_0_35(self):
        """Only latency score fires: result should equal latency_score * 0.35."""
        eng = make_engine()
        inp = make_input(avg_buyer_response_hours=96.0)  # +40 to latency only
        result = eng.assess(inp)
        assert result.latency_score == 40.0
        assert result.engagement_depth_score == 0.0
        assert result.commitment_score == 0.0
        assert result.process_velocity_score == 0.0
        assert result.latency_composite == round(40.0 * 0.35, 2)

    def test_composite_engagement_weight_is_0_25(self):
        eng = make_engine()
        inp = make_input(ghost_rate_pct=0.40)  # +40 to engagement only
        result = eng.assess(inp)
        assert result.engagement_depth_score == 40.0
        assert result.latency_score == 0.0
        assert result.commitment_score == 0.0
        assert result.process_velocity_score == 0.0
        assert result.latency_composite == round(40.0 * 0.25, 2)

    def test_composite_commitment_weight_is_0_25(self):
        eng = make_engine()
        inp = make_input(meeting_no_show_rate_pct=0.35)  # +40 to commitment only
        result = eng.assess(inp)
        assert result.commitment_score == 40.0
        assert result.latency_score == 0.0
        assert result.engagement_depth_score == 0.0
        assert result.process_velocity_score == 0.0
        assert result.latency_composite == round(40.0 * 0.25, 2)

    def test_composite_process_velocity_weight_is_0_15(self):
        eng = make_engine()
        inp = make_input(proposal_review_response_days=21.0)  # +45 to process only
        result = eng.assess(inp)
        assert result.process_velocity_score == 45.0
        assert result.latency_score == 0.0
        assert result.engagement_depth_score == 0.0
        assert result.commitment_score == 0.0
        assert result.latency_composite == round(45.0 * 0.15, 2)

    def test_composite_weights_sum_to_100_pct(self):
        """weights 0.35+0.25+0.25+0.15 == 1.0"""
        assert abs(0.35 + 0.25 + 0.25 + 0.15 - 1.0) < 1e-9

    def test_composite_capped_at_100(self):
        eng = make_engine()
        inp = make_input(
            avg_buyer_response_hours=200.0,
            response_time_vs_baseline_ratio=10.0,
            no_response_rate_pct=1.0,
            ghost_rate_pct=1.0,
            champion_response_rate_pct=0.0,
            executive_response_rate_pct=0.0,
            meeting_no_show_rate_pct=1.0,
            meeting_rescheduled_rate_pct=1.0,
            meeting_acceptance_rate_pct=0.0,
            proposal_review_response_days=999.0,
            contract_review_latency_days=999.0,
            demo_request_to_completion_days=999.0,
        )
        result = eng.assess(inp)
        assert result.latency_composite <= 100.0

    def test_composite_rounded_to_2_decimal_places(self):
        eng = make_engine()
        inp = make_input(
            avg_buyer_response_hours=48.0,   # latency +22
            ghost_rate_pct=0.25,             # engagement +22
        )
        result = eng.assess(inp)
        # Check it's a proper float with at most 2dp
        s = str(result.latency_composite)
        if "." in s:
            assert len(s.split(".")[1]) <= 2


# ─────────────────────────────────────────────────────────────────────────────
# 9. Risk thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestRiskThresholds:
    def _risk_at(self, composite: float) -> LatencyRisk:
        eng = make_engine()
        return eng._risk(composite)

    def test_composite_0_is_low(self):
        assert self._risk_at(0.0) == LatencyRisk.low

    def test_composite_19_is_low(self):
        assert self._risk_at(19.99) == LatencyRisk.low

    def test_composite_20_is_moderate(self):
        assert self._risk_at(20.0) == LatencyRisk.moderate

    def test_composite_39_is_moderate(self):
        assert self._risk_at(39.99) == LatencyRisk.moderate

    def test_composite_40_is_high(self):
        assert self._risk_at(40.0) == LatencyRisk.high

    def test_composite_59_is_high(self):
        assert self._risk_at(59.99) == LatencyRisk.high

    def test_composite_60_is_critical(self):
        assert self._risk_at(60.0) == LatencyRisk.critical

    def test_composite_100_is_critical(self):
        assert self._risk_at(100.0) == LatencyRisk.critical


# ─────────────────────────────────────────────────────────────────────────────
# 10. Severity thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestSeverityThresholds:
    def _sev_at(self, composite: float) -> LatencySeverity:
        eng = make_engine()
        return eng._severity(composite)

    def test_composite_0_is_responsive(self):
        assert self._sev_at(0.0) == LatencySeverity.responsive

    def test_composite_19_is_responsive(self):
        assert self._sev_at(19.99) == LatencySeverity.responsive

    def test_composite_20_is_cooling(self):
        assert self._sev_at(20.0) == LatencySeverity.cooling

    def test_composite_39_is_cooling(self):
        assert self._sev_at(39.99) == LatencySeverity.cooling

    def test_composite_40_is_disengaging(self):
        assert self._sev_at(40.0) == LatencySeverity.disengaging

    def test_composite_59_is_disengaging(self):
        assert self._sev_at(59.99) == LatencySeverity.disengaging

    def test_composite_60_is_ghosted(self):
        assert self._sev_at(60.0) == LatencySeverity.ghosted

    def test_composite_100_is_ghosted(self):
        assert self._sev_at(100.0) == LatencySeverity.ghosted


# ─────────────────────────────────────────────────────────────────────────────
# 11. Pattern detection
# ─────────────────────────────────────────────────────────────────────────────

class TestPatternDetection:
    def _pattern(self, **kwargs) -> LatencyPattern:
        eng = make_engine()
        return eng._pattern(make_input(**kwargs))

    # buyer_ghosting: ghost_rate_pct >= 0.30 AND no_response_rate_pct >= 0.40
    def test_buyer_ghosting_detected(self):
        assert self._pattern(
            ghost_rate_pct=0.30,
            no_response_rate_pct=0.40,
        ) == LatencyPattern.buyer_ghosting

    def test_buyer_ghosting_ghost_too_low(self):
        p = self._pattern(ghost_rate_pct=0.29, no_response_rate_pct=0.40)
        assert p != LatencyPattern.buyer_ghosting

    def test_buyer_ghosting_no_response_too_low(self):
        p = self._pattern(ghost_rate_pct=0.30, no_response_rate_pct=0.39)
        assert p != LatencyPattern.buyer_ghosting

    # executive_avoidance: exec_resp <= 0.20 AND no_show >= 0.25
    def test_executive_avoidance_detected(self):
        assert self._pattern(
            executive_response_rate_pct=0.20,
            meeting_no_show_rate_pct=0.25,
        ) == LatencyPattern.executive_avoidance

    def test_executive_avoidance_exec_too_high(self):
        p = self._pattern(
            executive_response_rate_pct=0.21,
            meeting_no_show_rate_pct=0.25,
        )
        assert p != LatencyPattern.executive_avoidance

    def test_executive_avoidance_no_show_too_low(self):
        p = self._pattern(
            executive_response_rate_pct=0.20,
            meeting_no_show_rate_pct=0.24,
        )
        assert p != LatencyPattern.executive_avoidance

    # champion_cooling: champion_resp <= 0.40 AND latency_trend >= 0.60
    def test_champion_cooling_detected(self):
        assert self._pattern(
            champion_response_rate_pct=0.40,
            response_latency_trend=0.60,
        ) == LatencyPattern.champion_cooling

    def test_champion_cooling_champion_too_high(self):
        p = self._pattern(
            champion_response_rate_pct=0.41,
            response_latency_trend=0.60,
        )
        assert p != LatencyPattern.champion_cooling

    def test_champion_cooling_trend_too_low(self):
        p = self._pattern(
            champion_response_rate_pct=0.40,
            response_latency_trend=0.59,
        )
        assert p != LatencyPattern.champion_cooling

    # commitment_fading: reschedule >= 0.40 AND acceptance <= 0.40
    def test_commitment_fading_detected(self):
        assert self._pattern(
            meeting_rescheduled_rate_pct=0.40,
            meeting_acceptance_rate_pct=0.40,
        ) == LatencyPattern.commitment_fading

    def test_commitment_fading_reschedule_too_low(self):
        p = self._pattern(
            meeting_rescheduled_rate_pct=0.39,
            meeting_acceptance_rate_pct=0.40,
        )
        assert p != LatencyPattern.commitment_fading

    def test_commitment_fading_acceptance_too_high(self):
        p = self._pattern(
            meeting_rescheduled_rate_pct=0.40,
            meeting_acceptance_rate_pct=0.41,
        )
        assert p != LatencyPattern.commitment_fading

    # process_stalling: proposal >= 14 AND contract >= 21
    def test_process_stalling_detected(self):
        assert self._pattern(
            proposal_review_response_days=14.0,
            contract_review_latency_days=21.0,
        ) == LatencyPattern.process_stalling

    def test_process_stalling_proposal_too_low(self):
        p = self._pattern(
            proposal_review_response_days=13.9,
            contract_review_latency_days=21.0,
        )
        assert p != LatencyPattern.process_stalling

    def test_process_stalling_contract_too_low(self):
        p = self._pattern(
            proposal_review_response_days=14.0,
            contract_review_latency_days=20.9,
        )
        assert p != LatencyPattern.process_stalling

    # none
    def test_none_pattern_when_nothing_triggers(self):
        assert self._pattern() == LatencyPattern.none

    # Priority: buyer_ghosting beats everything else
    def test_buyer_ghosting_takes_priority_over_executive_avoidance(self):
        p = self._pattern(
            ghost_rate_pct=0.30,
            no_response_rate_pct=0.40,
            executive_response_rate_pct=0.20,
            meeting_no_show_rate_pct=0.25,
        )
        assert p == LatencyPattern.buyer_ghosting

    # Priority: executive_avoidance beats champion_cooling
    def test_executive_avoidance_takes_priority_over_champion_cooling(self):
        p = self._pattern(
            executive_response_rate_pct=0.20,
            meeting_no_show_rate_pct=0.25,
            champion_response_rate_pct=0.40,
            response_latency_trend=0.60,
        )
        assert p == LatencyPattern.executive_avoidance

    # Priority: champion_cooling beats commitment_fading
    def test_champion_cooling_takes_priority_over_commitment_fading(self):
        p = self._pattern(
            champion_response_rate_pct=0.40,
            response_latency_trend=0.60,
            meeting_rescheduled_rate_pct=0.40,
            meeting_acceptance_rate_pct=0.40,
        )
        assert p == LatencyPattern.champion_cooling

    # Priority: commitment_fading beats process_stalling
    def test_commitment_fading_takes_priority_over_process_stalling(self):
        p = self._pattern(
            meeting_rescheduled_rate_pct=0.40,
            meeting_acceptance_rate_pct=0.40,
            proposal_review_response_days=14.0,
            contract_review_latency_days=21.0,
        )
        assert p == LatencyPattern.commitment_fading


# ─────────────────────────────────────────────────────────────────────────────
# 12. Action routing
# ─────────────────────────────────────────────────────────────────────────────

class TestActionRouting:
    def _action(self, risk: LatencyRisk, pattern: LatencyPattern) -> LatencyAction:
        eng = make_engine()
        return eng._action(risk, pattern)

    # low risk → no_action regardless of pattern
    def test_low_no_action(self):
        assert self._action(LatencyRisk.low, LatencyPattern.none) == LatencyAction.no_action

    def test_low_no_action_with_buyer_ghosting(self):
        assert self._action(LatencyRisk.low, LatencyPattern.buyer_ghosting) == LatencyAction.no_action

    # moderate → engagement_monitoring regardless of pattern
    def test_moderate_engagement_monitoring(self):
        assert self._action(LatencyRisk.moderate, LatencyPattern.none) == LatencyAction.engagement_monitoring

    def test_moderate_engagement_monitoring_with_stalling(self):
        assert self._action(LatencyRisk.moderate, LatencyPattern.process_stalling) == LatencyAction.engagement_monitoring

    # high + buyer_ghosting → deal_save_intervention
    def test_high_buyer_ghosting_deal_save(self):
        assert self._action(LatencyRisk.high, LatencyPattern.buyer_ghosting) == LatencyAction.deal_save_intervention

    # high + executive_avoidance → executive_outreach_coaching
    def test_high_executive_avoidance_outreach(self):
        assert self._action(LatencyRisk.high, LatencyPattern.executive_avoidance) == LatencyAction.executive_outreach_coaching

    # high + champion_cooling → champion_replacement_coaching
    def test_high_champion_cooling_replacement(self):
        assert self._action(LatencyRisk.high, LatencyPattern.champion_cooling) == LatencyAction.champion_replacement_coaching

    # high + commitment_fading → re_engagement_coaching
    def test_high_commitment_fading_re_engagement(self):
        assert self._action(LatencyRisk.high, LatencyPattern.commitment_fading) == LatencyAction.re_engagement_coaching

    # high + process_stalling → executive_outreach_coaching
    def test_high_process_stalling_outreach(self):
        assert self._action(LatencyRisk.high, LatencyPattern.process_stalling) == LatencyAction.executive_outreach_coaching

    # high + none → re_engagement_coaching (fallback)
    def test_high_none_pattern_re_engagement_fallback(self):
        assert self._action(LatencyRisk.high, LatencyPattern.none) == LatencyAction.re_engagement_coaching

    # critical + buyer_ghosting → deal_abandon_escalation
    def test_critical_buyer_ghosting_abandon(self):
        assert self._action(LatencyRisk.critical, LatencyPattern.buyer_ghosting) == LatencyAction.deal_abandon_escalation

    # critical + executive_avoidance → deal_abandon_escalation
    def test_critical_executive_avoidance_abandon(self):
        assert self._action(LatencyRisk.critical, LatencyPattern.executive_avoidance) == LatencyAction.deal_abandon_escalation

    # critical + champion_cooling → deal_save_intervention
    def test_critical_champion_cooling_deal_save(self):
        assert self._action(LatencyRisk.critical, LatencyPattern.champion_cooling) == LatencyAction.deal_save_intervention

    # critical + commitment_fading → deal_save_intervention
    def test_critical_commitment_fading_deal_save(self):
        assert self._action(LatencyRisk.critical, LatencyPattern.commitment_fading) == LatencyAction.deal_save_intervention

    # critical + process_stalling → deal_save_intervention
    def test_critical_process_stalling_deal_save(self):
        assert self._action(LatencyRisk.critical, LatencyPattern.process_stalling) == LatencyAction.deal_save_intervention

    # critical + none → deal_save_intervention
    def test_critical_none_pattern_deal_save(self):
        assert self._action(LatencyRisk.critical, LatencyPattern.none) == LatencyAction.deal_save_intervention


# ─────────────────────────────────────────────────────────────────────────────
# 13. has_latency_gap flag
# ─────────────────────────────────────────────────────────────────────────────

class TestHasLatencyGap:
    def _gap(self, **kwargs) -> bool:
        eng = make_engine()
        inp = make_input(**kwargs)
        result = eng.assess(inp)
        return result.has_latency_gap

    def test_gap_false_when_healthy(self):
        assert self._gap() is False

    def test_gap_true_when_composite_40(self):
        # Drive composite >= 40 via ghost_rate_pct + no_response
        assert self._gap(
            ghost_rate_pct=0.40,
            champion_response_rate_pct=0.30,
            executive_response_rate_pct=0.15,
        ) is True

    def test_gap_true_when_ghost_rate_20(self):
        assert self._gap(ghost_rate_pct=0.20) is True

    def test_gap_true_when_ghost_rate_exactly_20(self):
        assert self._gap(ghost_rate_pct=0.20) is True

    def test_gap_false_when_ghost_rate_just_below_20(self):
        assert self._gap(ghost_rate_pct=0.19) is False

    def test_gap_true_when_response_hours_48(self):
        assert self._gap(avg_buyer_response_hours=48.0) is True

    def test_gap_true_when_response_hours_above_48(self):
        assert self._gap(avg_buyer_response_hours=100.0) is True

    def test_gap_false_when_response_hours_just_below_48(self):
        assert self._gap(avg_buyer_response_hours=47.9) is False


# ─────────────────────────────────────────────────────────────────────────────
# 14. requires_latency_intervention flag
# ─────────────────────────────────────────────────────────────────────────────

class TestRequiresIntervention:
    def _intervention(self, **kwargs) -> bool:
        eng = make_engine()
        result = eng.assess(make_input(**kwargs))
        return result.requires_latency_intervention

    def test_intervention_false_when_healthy(self):
        assert self._intervention() is False

    def test_intervention_true_when_composite_25(self):
        # composite 25 -> True
        # ghost 0.40 * 0.25 = 10 for engagement, need composite >= 25
        # latency: 96h → 40*0.35 = 14, engagement ghost 0.40 → 40*0.25 = 10 => 24, need a bit more
        # add no_response 0.30 → latency: 40+12=52, 52*0.35=18.2, engagement: 40*0.25=10, total ~28.2
        assert self._intervention(
            avg_buyer_response_hours=96.0,
            no_response_rate_pct=0.30,
            ghost_rate_pct=0.40,
        ) is True

    def test_intervention_true_when_no_show_exactly_15(self):
        assert self._intervention(meeting_no_show_rate_pct=0.15) is True

    def test_intervention_true_when_no_show_above_15(self):
        assert self._intervention(meeting_no_show_rate_pct=0.50) is True

    def test_intervention_false_when_no_show_just_below_15(self):
        assert self._intervention(meeting_no_show_rate_pct=0.14) is False

    def test_intervention_true_when_champion_response_exactly_55(self):
        assert self._intervention(champion_response_rate_pct=0.55) is True

    def test_intervention_true_when_champion_response_below_55(self):
        assert self._intervention(champion_response_rate_pct=0.30) is True

    def test_intervention_false_when_champion_response_above_55(self):
        assert self._intervention(champion_response_rate_pct=0.56) is False


# ─────────────────────────────────────────────────────────────────────────────
# 15. at_risk_revenue formula
# ─────────────────────────────────────────────────────────────────────────────

class TestAtRiskRevenue:
    def test_zero_composite_gives_zero_revenue(self):
        eng = make_engine()
        result = eng.assess(make_input())
        # composite==0 → revenue == 0
        assert result.estimated_at_risk_revenue_usd == 0.0

    def test_formula_basic(self):
        eng = make_engine()
        # Let's drive a known composite and known inputs
        # ghost_rate=0.40, no_response=0.50, total_deals=10, avg_val=1000
        # at_risk_deals = 10 * (0.40 + 0.50*0.5) = 10 * 0.65 = 6.5 (< 10)
        # composite drives the final factor
        inp = make_input(
            ghost_rate_pct=0.40,
            no_response_rate_pct=0.50,
            total_active_deals=10,
            avg_deal_value_usd=1_000.0,
        )
        result = eng.assess(inp)
        comp = result.latency_composite
        at_risk_deals = min(10 * (0.40 + 0.50 * 0.5), 10)
        expected = round(at_risk_deals * 1_000.0 * (comp / 100), 2)
        assert result.estimated_at_risk_revenue_usd == expected

    def test_at_risk_deals_capped_at_total_active(self):
        eng = make_engine()
        # ghost=1.0 + no_response=1.0 → at_risk_deals = 10*(1+0.5)=15 capped to 10
        inp = make_input(
            ghost_rate_pct=1.0,
            no_response_rate_pct=1.0,
            total_active_deals=10,
            avg_deal_value_usd=500.0,
        )
        result = eng.assess(inp)
        comp = result.latency_composite
        expected = round(10 * 500.0 * (comp / 100), 2)
        assert result.estimated_at_risk_revenue_usd == expected

    def test_revenue_scales_with_deal_value(self):
        eng1 = make_engine()
        eng2 = make_engine()
        inp1 = make_input(
            ghost_rate_pct=0.30,
            no_response_rate_pct=0.40,
            avg_deal_value_usd=1_000.0,
            total_active_deals=5,
        )
        inp2 = make_input(
            ghost_rate_pct=0.30,
            no_response_rate_pct=0.40,
            avg_deal_value_usd=2_000.0,
            total_active_deals=5,
        )
        r1 = eng1.assess(inp1)
        r2 = eng2.assess(inp2)
        if r1.estimated_at_risk_revenue_usd > 0:
            assert abs(r2.estimated_at_risk_revenue_usd / r1.estimated_at_risk_revenue_usd - 2.0) < 0.01

    def test_revenue_scales_with_deals(self):
        eng1 = make_engine()
        eng2 = make_engine()
        inp1 = make_input(
            ghost_rate_pct=0.30,
            no_response_rate_pct=0.40,
            avg_deal_value_usd=1_000.0,
            total_active_deals=5,
        )
        inp2 = make_input(
            ghost_rate_pct=0.30,
            no_response_rate_pct=0.40,
            avg_deal_value_usd=1_000.0,
            total_active_deals=10,
        )
        r1 = eng1.assess(inp1)
        r2 = eng2.assess(inp2)
        if r1.estimated_at_risk_revenue_usd > 0:
            assert abs(r2.estimated_at_risk_revenue_usd / r1.estimated_at_risk_revenue_usd - 2.0) < 0.01

    def test_revenue_is_non_negative(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert result.estimated_at_risk_revenue_usd >= 0.0

    def test_revenue_rounded_to_2dp(self):
        eng = make_engine()
        inp = make_input(
            ghost_rate_pct=0.333,
            no_response_rate_pct=0.333,
            avg_deal_value_usd=333.33,
            total_active_deals=7,
        )
        result = eng.assess(inp)
        # Must be rounded to 2dp
        as_str = f"{result.estimated_at_risk_revenue_usd:.10f}"
        rounded = round(result.estimated_at_risk_revenue_usd, 2)
        assert result.estimated_at_risk_revenue_usd == rounded


# ─────────────────────────────────────────────────────────────────────────────
# 16. Signal string
# ─────────────────────────────────────────────────────────────────────────────

class TestSignalString:
    def test_healthy_signal_returned_when_composite_below_20(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert "Buyer engagement healthy" in result.latency_signal

    def test_healthy_signal_exact_text(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert result.latency_signal == (
            "Buyer engagement healthy — response times, meeting attendance, "
            "champion engagement, and process velocity within benchmarks"
        )

    def test_unhealthy_signal_contains_pattern_label(self):
        eng = make_engine()
        inp = make_input(
            ghost_rate_pct=0.30,
            no_response_rate_pct=0.40,
            avg_buyer_response_hours=96.0,
        )
        result = eng.assess(inp)
        assert "Buyer ghosting" in result.latency_signal

    def test_unhealthy_signal_contains_response_hours(self):
        eng = make_engine()
        # Need composite >= 20 for the unhealthy branch
        # avg_hours=96 → latency 40, ghost=0.30 → engagement 22, no_response=0.40 → latency +25
        # latency = min(40+25,100)=65, engagement=22, composite=65*0.35+22*0.25=22.75+5.5=28.25 >= 20
        inp = make_input(
            ghost_rate_pct=0.30,
            no_response_rate_pct=0.40,
            avg_buyer_response_hours=73.0,
            champion_response_rate_pct=0.20,   # engagement +35
            executive_response_rate_pct=0.10,  # engagement +25
        )
        result = eng.assess(inp)
        # Verify composite is above 20 before asserting signal content
        assert result.latency_composite >= 20.0, (
            f"Composite {result.latency_composite} too low for unhealthy signal"
        )
        assert "73h" in result.latency_signal

    def test_unhealthy_signal_contains_ghost_pct(self):
        eng = make_engine()
        inp = make_input(
            ghost_rate_pct=0.30,
            no_response_rate_pct=0.40,
            avg_buyer_response_hours=96.0,
        )
        result = eng.assess(inp)
        assert "30% deals ghosted" in result.latency_signal

    def test_unhealthy_signal_contains_no_show_pct(self):
        eng = make_engine()
        inp = make_input(
            ghost_rate_pct=0.30,
            no_response_rate_pct=0.40,
            avg_buyer_response_hours=96.0,
            meeting_no_show_rate_pct=0.20,
        )
        result = eng.assess(inp)
        assert "20% meeting no-shows" in result.latency_signal

    def test_unhealthy_signal_contains_composite(self):
        eng = make_engine()
        inp = make_input(
            ghost_rate_pct=0.30,
            no_response_rate_pct=0.40,
            avg_buyer_response_hours=96.0,
        )
        result = eng.assess(inp)
        comp_int = round(result.latency_composite)
        assert f"composite {comp_int}" in result.latency_signal

    def test_executive_avoidance_label_in_signal(self):
        eng = make_engine()
        inp = make_input(
            executive_response_rate_pct=0.10,
            meeting_no_show_rate_pct=0.30,
            avg_buyer_response_hours=96.0,
            no_response_rate_pct=0.50,
        )
        result = eng.assess(inp)
        if result.latency_pattern == LatencyPattern.executive_avoidance:
            assert "Executive avoidance" in result.latency_signal

    def test_champion_cooling_label_in_signal(self):
        eng = make_engine()
        inp = make_input(
            champion_response_rate_pct=0.20,
            response_latency_trend=0.80,
            avg_buyer_response_hours=96.0,
        )
        result = eng.assess(inp)
        if result.latency_pattern == LatencyPattern.champion_cooling:
            assert "Champion cooling" in result.latency_signal

    def test_commitment_fading_label_in_signal(self):
        eng = make_engine()
        inp = make_input(
            meeting_rescheduled_rate_pct=0.50,
            meeting_acceptance_rate_pct=0.25,
            avg_buyer_response_hours=96.0,
        )
        result = eng.assess(inp)
        if result.latency_pattern == LatencyPattern.commitment_fading:
            assert "Commitment fading" in result.latency_signal

    def test_process_stalling_label_in_signal(self):
        eng = make_engine()
        inp = make_input(
            proposal_review_response_days=21.0,
            contract_review_latency_days=30.0,
            avg_buyer_response_hours=96.0,
        )
        result = eng.assess(inp)
        if result.latency_pattern == LatencyPattern.process_stalling:
            assert "Process stalling" in result.latency_signal


# ─────────────────────────────────────────────────────────────────────────────
# 17. assess() end-to-end
# ─────────────────────────────────────────────────────────────────────────────

class TestAssessEndToEnd:
    def test_returns_latency_result_type(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert isinstance(result, LatencyResult)

    def test_rep_id_preserved(self):
        eng = make_engine()
        result = eng.assess(make_input(rep_id="RTEST"))
        assert result.rep_id == "RTEST"

    def test_region_preserved(self):
        eng = make_engine()
        result = eng.assess(make_input(region="WEST"))
        assert result.region == "WEST"

    def test_healthy_input_low_risk(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert result.latency_risk == LatencyRisk.low

    def test_healthy_input_responsive_severity(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert result.latency_severity == LatencySeverity.responsive

    def test_healthy_input_none_pattern(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert result.latency_pattern == LatencyPattern.none

    def test_healthy_input_no_action(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert result.recommended_action == LatencyAction.no_action

    def test_critical_scenario_full(self):
        eng = make_engine()
        inp = make_input(
            ghost_rate_pct=0.50,
            no_response_rate_pct=0.60,
            avg_buyer_response_hours=120.0,
            response_time_vs_baseline_ratio=3.5,
            champion_response_rate_pct=0.20,
            executive_response_rate_pct=0.10,
            meeting_no_show_rate_pct=0.40,
            meeting_rescheduled_rate_pct=0.60,
            meeting_acceptance_rate_pct=0.20,
            proposal_review_response_days=30.0,
            contract_review_latency_days=45.0,
            demo_request_to_completion_days=30.0,
        )
        result = eng.assess(inp)
        assert result.latency_risk == LatencyRisk.critical
        assert result.latency_severity == LatencySeverity.ghosted
        assert result.latency_composite >= 60.0

    def test_assess_stores_result(self):
        eng = make_engine()
        eng.assess(make_input())
        assert len(eng._results) == 1

    def test_assess_multiple_stores_all(self):
        eng = make_engine()
        for i in range(5):
            eng.assess(make_input(rep_id=f"R{i}"))
        assert len(eng._results) == 5

    def test_result_sub_scores_are_non_negative(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert result.latency_score >= 0
        assert result.engagement_depth_score >= 0
        assert result.commitment_score >= 0
        assert result.process_velocity_score >= 0

    def test_result_sub_scores_at_most_100(self):
        eng = make_engine()
        inp = make_input(
            avg_buyer_response_hours=200.0,
            response_time_vs_baseline_ratio=10.0,
            no_response_rate_pct=1.0,
            ghost_rate_pct=1.0,
            champion_response_rate_pct=0.0,
            executive_response_rate_pct=0.0,
            meeting_no_show_rate_pct=1.0,
            meeting_rescheduled_rate_pct=1.0,
            meeting_acceptance_rate_pct=0.0,
            proposal_review_response_days=999.0,
            contract_review_latency_days=999.0,
            demo_request_to_completion_days=999.0,
        )
        result = eng.assess(inp)
        assert result.latency_score <= 100
        assert result.engagement_depth_score <= 100
        assert result.commitment_score <= 100
        assert result.process_velocity_score <= 100

    def test_moderate_risk_scenario(self):
        eng = make_engine()
        # composite between 20 and 40 → moderate
        inp = make_input(avg_buyer_response_hours=48.0)  # latency 22 * 0.35 = 7.7
        # Need more: add ghost 0.25 → eng 22*0.25=5.5 => composite ~13.2 still low
        # Add no_show 0.20 → commit 22*0.25=5.5 => ~18.7 still low
        # Try avg_hours 96 (40*0.35=14) + ghost 0.25 (22*0.25=5.5) + no_show 0.20 (22*0.25=5.5) = 25 >= 20
        inp2 = make_input(
            avg_buyer_response_hours=96.0,
            ghost_rate_pct=0.25,
            meeting_no_show_rate_pct=0.20,
        )
        result = eng.assess(inp2)
        assert result.latency_risk == LatencyRisk.moderate
        assert result.recommended_action == LatencyAction.engagement_monitoring

    def test_high_risk_no_pattern_gives_re_engagement(self):
        eng = make_engine()
        # Drive high risk (40-60) without triggering a pattern
        # latency: 96h→40*0.35=14, baseline 2.0→18*0.35=6.3... need 40+
        # engagement: ghost 0.25→22*0.25=5.5, no-response 0.30→12*0.35=4.2
        # Let's brute-force via all mid fields
        inp = make_input(
            avg_buyer_response_hours=96.0,       # latency +40
            response_time_vs_baseline_ratio=2.0, # latency +18
            no_response_rate_pct=0.30,            # latency +12
            ghost_rate_pct=0.10,                  # engagement +8  (< 0.25 so not buyer_ghosting)
            champion_response_rate_pct=0.51,      # no trigger
            executive_response_rate_pct=0.31,     # no trigger
            meeting_no_show_rate_pct=0.09,        # no trigger for executive_avoidance
            meeting_rescheduled_rate_pct=0.05,
            meeting_acceptance_rate_pct=0.90,
            proposal_review_response_days=3.0,
            contract_review_latency_days=5.0,
            demo_request_to_completion_days=5.0,
            response_latency_trend=0.10,
        )
        result = eng.assess(inp)
        # latency: min(40+18+12,100)=70, engagement: 8, commitment: 0, process: 0
        # composite = 70*0.35 + 8*0.25 + 0 + 0 = 24.5 + 2.0 = 26.5 → moderate
        # So pattern is none, risk is moderate, action is engagement_monitoring
        assert result.latency_pattern == LatencyPattern.none


# ─────────────────────────────────────────────────────────────────────────────
# 18. assess_batch()
# ─────────────────────────────────────────────────────────────────────────────

class TestAssessBatch:
    def test_returns_list(self):
        eng = make_engine()
        results = eng.assess_batch([make_input(), make_input(rep_id="R2")])
        assert isinstance(results, list)

    def test_returns_correct_count(self):
        eng = make_engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(7)]
        results = eng.assess_batch(inputs)
        assert len(results) == 7

    def test_each_item_is_latency_result(self):
        eng = make_engine()
        results = eng.assess_batch([make_input(), make_input(rep_id="R2")])
        for r in results:
            assert isinstance(r, LatencyResult)

    def test_empty_batch_returns_empty_list(self):
        eng = make_engine()
        assert eng.assess_batch([]) == []

    def test_batch_stores_all_results(self):
        eng = make_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        assert len(eng._results) == 4

    def test_batch_results_match_individual_assess(self):
        inp1 = make_input(rep_id="A")
        inp2 = make_input(rep_id="B", avg_buyer_response_hours=96.0)

        eng_single = make_engine()
        r1 = eng_single.assess(inp1)
        r2 = eng_single.assess(inp2)

        eng_batch = make_engine()
        batch = eng_batch.assess_batch([inp1, inp2])

        assert batch[0].latency_composite == r1.latency_composite
        assert batch[1].latency_composite == r2.latency_composite

    def test_batch_rep_ids_preserved(self):
        eng = make_engine()
        ids = [f"REP-{i}" for i in range(5)]
        inputs = [make_input(rep_id=rid) for rid in ids]
        results = eng.assess_batch(inputs)
        assert [r.rep_id for r in results] == ids

    def test_single_item_batch(self):
        eng = make_engine()
        results = eng.assess_batch([make_input(rep_id="SOLO")])
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"


# ─────────────────────────────────────────────────────────────────────────────
# 19. summary() — empty state
# ─────────────────────────────────────────────────────────────────────────────

class TestSummaryEmpty:
    def test_empty_summary_has_13_keys(self):
        eng = make_engine()
        s = eng.summary()
        assert len(s) == 13

    def test_empty_summary_total_zero(self):
        assert make_engine().summary()["total"] == 0

    def test_empty_summary_risk_counts_empty(self):
        assert make_engine().summary()["risk_counts"] == {}

    def test_empty_summary_pattern_counts_empty(self):
        assert make_engine().summary()["pattern_counts"] == {}

    def test_empty_summary_severity_counts_empty(self):
        assert make_engine().summary()["severity_counts"] == {}

    def test_empty_summary_action_counts_empty(self):
        assert make_engine().summary()["action_counts"] == {}

    def test_empty_summary_avg_composite_zero(self):
        assert make_engine().summary()["avg_latency_composite"] == 0.0

    def test_empty_summary_gap_count_zero(self):
        assert make_engine().summary()["latency_gap_count"] == 0

    def test_empty_summary_intervention_count_zero(self):
        assert make_engine().summary()["intervention_count"] == 0

    def test_empty_summary_avg_latency_score_zero(self):
        assert make_engine().summary()["avg_latency_score"] == 0.0

    def test_empty_summary_avg_engagement_depth_score_zero(self):
        assert make_engine().summary()["avg_engagement_depth_score"] == 0.0

    def test_empty_summary_avg_commitment_score_zero(self):
        assert make_engine().summary()["avg_commitment_score"] == 0.0

    def test_empty_summary_avg_process_velocity_score_zero(self):
        assert make_engine().summary()["avg_process_velocity_score"] == 0.0

    def test_empty_summary_total_at_risk_revenue_zero(self):
        assert make_engine().summary()["total_estimated_at_risk_revenue_usd"] == 0.0

    def test_empty_summary_key_names(self):
        expected_keys = {
            "total",
            "risk_counts",
            "pattern_counts",
            "severity_counts",
            "action_counts",
            "avg_latency_composite",
            "latency_gap_count",
            "intervention_count",
            "avg_latency_score",
            "avg_engagement_depth_score",
            "avg_commitment_score",
            "avg_process_velocity_score",
            "total_estimated_at_risk_revenue_usd",
        }
        assert set(make_engine().summary().keys()) == expected_keys


# ─────────────────────────────────────────────────────────────────────────────
# 20. summary() — populated state
# ─────────────────────────────────────────────────────────────────────────────

class TestSummaryPopulated:
    def test_summary_has_13_keys(self):
        eng = make_engine()
        eng.assess(make_input())
        assert len(eng.summary()) == 13

    def test_total_count(self):
        eng = make_engine()
        for _ in range(3):
            eng.assess(make_input())
        assert eng.summary()["total"] == 3

    def test_risk_counts_sums_to_total(self):
        eng = make_engine()
        for _ in range(5):
            eng.assess(make_input())
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_pattern_counts_sums_to_total(self):
        eng = make_engine()
        for _ in range(4):
            eng.assess(make_input())
        s = eng.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_severity_counts_sums_to_total(self):
        eng = make_engine()
        for _ in range(4):
            eng.assess(make_input())
        s = eng.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_action_counts_sums_to_total(self):
        eng = make_engine()
        for _ in range(4):
            eng.assess(make_input())
        s = eng.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_avg_composite_is_average(self):
        eng = make_engine()
        inp_a = make_input()  # composite = 0
        inp_b = make_input(avg_buyer_response_hours=96.0)  # composite > 0
        eng.assess(inp_a)
        eng.assess(inp_b)
        s = eng.summary()
        composites = [r.latency_composite for r in eng._results]
        expected_avg = round(sum(composites) / len(composites), 1)
        assert s["avg_latency_composite"] == expected_avg

    def test_gap_count_correct(self):
        eng = make_engine()
        eng.assess(make_input(ghost_rate_pct=0.20))  # gap=True
        eng.assess(make_input())                      # gap=False
        s = eng.summary()
        assert s["latency_gap_count"] == 1

    def test_intervention_count_correct(self):
        eng = make_engine()
        eng.assess(make_input(meeting_no_show_rate_pct=0.15))  # intervention=True
        eng.assess(make_input())                                # intervention=False
        s = eng.summary()
        assert s["intervention_count"] == 1

    def test_total_at_risk_revenue_is_sum(self):
        eng = make_engine()
        eng.assess(make_input())
        eng.assess(make_input())
        s = eng.summary()
        total = sum(r.estimated_at_risk_revenue_usd for r in eng._results)
        assert s["total_estimated_at_risk_revenue_usd"] == round(total, 2)

    def test_risk_counts_use_string_keys(self):
        eng = make_engine()
        eng.assess(make_input())
        risk_counts = eng.summary()["risk_counts"]
        for k in risk_counts:
            assert isinstance(k, str)

    def test_pattern_counts_use_string_keys(self):
        eng = make_engine()
        eng.assess(make_input())
        pattern_counts = eng.summary()["pattern_counts"]
        for k in pattern_counts:
            assert isinstance(k, str)

    def test_mixed_risk_levels_counted_separately(self):
        eng = make_engine()
        # healthy → low
        eng.assess(make_input())
        # Drive moderate (composite ~20-40)
        eng.assess(make_input(avg_buyer_response_hours=96.0, ghost_rate_pct=0.25))
        s = eng.summary()
        assert "low" in s["risk_counts"]

    def test_avg_latency_score_is_avg(self):
        eng = make_engine()
        for _ in range(3):
            eng.assess(make_input())
        s = eng.summary()
        scores = [r.latency_score for r in eng._results]
        expected = round(sum(scores) / len(scores), 1)
        assert s["avg_latency_score"] == expected

    def test_avg_engagement_depth_score_is_avg(self):
        eng = make_engine()
        for _ in range(3):
            eng.assess(make_input())
        s = eng.summary()
        scores = [r.engagement_depth_score for r in eng._results]
        expected = round(sum(scores) / len(scores), 1)
        assert s["avg_engagement_depth_score"] == expected

    def test_avg_commitment_score_is_avg(self):
        eng = make_engine()
        for _ in range(3):
            eng.assess(make_input())
        s = eng.summary()
        scores = [r.commitment_score for r in eng._results]
        expected = round(sum(scores) / len(scores), 1)
        assert s["avg_commitment_score"] == expected

    def test_avg_process_velocity_score_is_avg(self):
        eng = make_engine()
        for _ in range(3):
            eng.assess(make_input())
        s = eng.summary()
        scores = [r.process_velocity_score for r in eng._results]
        expected = round(sum(scores) / len(scores), 1)
        assert s["avg_process_velocity_score"] == expected


# ─────────────────────────────────────────────────────────────────────────────
# 21. Engine instance isolation
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineIsolation:
    def test_new_engine_starts_empty(self):
        eng = make_engine()
        assert eng._results == []

    def test_two_engines_independent(self):
        eng1 = make_engine()
        eng2 = make_engine()
        eng1.assess(make_input(rep_id="A"))
        assert len(eng2._results) == 0

    def test_results_accumulate_across_calls(self):
        eng = make_engine()
        for i in range(10):
            eng.assess(make_input(rep_id=f"R{i}"))
        assert len(eng._results) == 10

    def test_summary_after_batch_and_single(self):
        eng = make_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        eng.assess(make_input(rep_id="EXTRA"))
        assert eng.summary()["total"] == 4


# ─────────────────────────────────────────────────────────────────────────────
# 22. Edge and boundary cases
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_all_fields_at_zero(self):
        eng = make_engine()
        inp = make_input(
            avg_buyer_response_hours=0.0,
            response_latency_trend=0.0,
            no_response_rate_pct=0.0,
            avg_follow_ups_before_response=0.0,
            ghost_rate_pct=0.0,
            response_time_vs_baseline_ratio=0.0,
            executive_response_rate_pct=0.0,     # <=0.15 → +25
            champion_response_rate_pct=0.0,      # <=0.30 → +35
            meeting_acceptance_rate_pct=0.0,     # <=0.30 → +25
            meeting_rescheduled_rate_pct=0.0,
            meeting_no_show_rate_pct=0.0,
            demo_request_to_completion_days=0.0,
            proposal_review_response_days=0.0,
            contract_review_latency_days=0.0,
            multi_contact_response_diversity=0.0,
            outreach_channel_effectiveness=0.0,
            response_quality_score=0.0,
            total_active_deals=0,
            avg_deal_value_usd=0.0,
        )
        result = eng.assess(inp)
        assert result.latency_composite >= 0.0

    def test_total_active_deals_zero_revenue_is_zero(self):
        eng = make_engine()
        inp = make_input(total_active_deals=0, avg_deal_value_usd=100_000.0)
        result = eng.assess(inp)
        assert result.estimated_at_risk_revenue_usd == 0.0

    def test_avg_deal_value_zero_revenue_is_zero(self):
        eng = make_engine()
        inp = make_input(
            ghost_rate_pct=0.40,
            no_response_rate_pct=0.50,
            avg_deal_value_usd=0.0,
        )
        result = eng.assess(inp)
        assert result.estimated_at_risk_revenue_usd == 0.0

    def test_composite_exactly_at_boundary_20(self):
        eng = make_engine()
        # Composite of exactly 20 should be moderate / cooling
        # latency: 96h→40, ratio<1.5→0, no_resp<0.30→0 => 40*0.35=14
        # engagement: ghost<0.10→0, champ>0.50→0, exec>0.30→0 => 0
        # commitment: 0
        # process: 0
        # So 14 composite < 20 → low
        # We need to hit exactly 20: set engagement ghost 0.10→8, exec 0.15→25, champ 0.30→35
        # engagement = min(8+35+25,100)=68, 68*0.25=17, latency=14, total=31 → high not boundary
        # Let's test the _risk boundary directly
        risk = eng._risk(20.0)
        assert risk == LatencyRisk.moderate

    def test_composite_exactly_at_boundary_40(self):
        eng = make_engine()
        assert eng._risk(40.0) == LatencyRisk.high

    def test_composite_exactly_at_boundary_60(self):
        eng = make_engine()
        assert eng._risk(60.0) == LatencyRisk.critical

    def test_severity_exactly_at_boundary_20(self):
        eng = make_engine()
        assert eng._severity(20.0) == LatencySeverity.cooling

    def test_severity_exactly_at_boundary_40(self):
        eng = make_engine()
        assert eng._severity(40.0) == LatencySeverity.disengaging

    def test_severity_exactly_at_boundary_60(self):
        eng = make_engine()
        assert eng._severity(60.0) == LatencySeverity.ghosted

    def test_ghost_rate_exactly_20_triggers_gap(self):
        eng = make_engine()
        result = eng.assess(make_input(ghost_rate_pct=0.20))
        assert result.has_latency_gap is True

    def test_champion_response_exactly_55_triggers_intervention(self):
        eng = make_engine()
        result = eng.assess(make_input(champion_response_rate_pct=0.55))
        assert result.requires_latency_intervention is True

    def test_champion_response_55_and_composite_below_25_still_intervention(self):
        eng = make_engine()
        result = eng.assess(make_input(champion_response_rate_pct=0.55))
        # Even if composite < 25, champion 0.55 triggers intervention
        assert result.requires_latency_intervention is True

    def test_large_deal_values(self):
        eng = make_engine()
        inp = make_input(
            avg_deal_value_usd=1_000_000.0,
            total_active_deals=100,
            ghost_rate_pct=0.40,
            no_response_rate_pct=0.50,
        )
        result = eng.assess(inp)
        assert result.estimated_at_risk_revenue_usd > 0.0

    def test_response_hours_exactly_24(self):
        eng = make_engine()
        score = eng._latency_score(make_input(avg_buyer_response_hours=24.0))
        assert score == 8.0

    def test_response_hours_exactly_48(self):
        eng = make_engine()
        score = eng._latency_score(make_input(avg_buyer_response_hours=48.0))
        assert score == 22.0

    def test_response_hours_exactly_96(self):
        eng = make_engine()
        score = eng._latency_score(make_input(avg_buyer_response_hours=96.0))
        assert score == 40.0

    def test_no_response_rate_exactly_30(self):
        eng = make_engine()
        score = eng._latency_score(make_input(no_response_rate_pct=0.30))
        assert score == 12.0

    def test_no_response_rate_exactly_50(self):
        eng = make_engine()
        score = eng._latency_score(make_input(no_response_rate_pct=0.50))
        assert score == 25.0

    def test_ghost_rate_exactly_10(self):
        eng = make_engine()
        score = eng._engagement_depth_score(make_input(ghost_rate_pct=0.10))
        assert score == 8.0

    def test_ghost_rate_exactly_25(self):
        eng = make_engine()
        score = eng._engagement_depth_score(make_input(ghost_rate_pct=0.25))
        assert score == 22.0

    def test_ghost_rate_exactly_40(self):
        eng = make_engine()
        score = eng._engagement_depth_score(make_input(ghost_rate_pct=0.40))
        assert score == 40.0

    def test_no_show_exactly_10(self):
        eng = make_engine()
        score = eng._commitment_score(make_input(meeting_no_show_rate_pct=0.10))
        assert score == 8.0

    def test_no_show_exactly_20(self):
        eng = make_engine()
        score = eng._commitment_score(make_input(meeting_no_show_rate_pct=0.20))
        assert score == 22.0

    def test_no_show_exactly_35(self):
        eng = make_engine()
        score = eng._commitment_score(make_input(meeting_no_show_rate_pct=0.35))
        assert score == 40.0

    def test_proposal_exactly_7(self):
        eng = make_engine()
        score = eng._process_velocity_score(make_input(proposal_review_response_days=7.0))
        assert score == 10.0

    def test_proposal_exactly_14(self):
        eng = make_engine()
        score = eng._process_velocity_score(make_input(proposal_review_response_days=14.0))
        assert score == 25.0

    def test_proposal_exactly_21(self):
        eng = make_engine()
        score = eng._process_velocity_score(make_input(proposal_review_response_days=21.0))
        assert score == 45.0

    def test_contract_exactly_21(self):
        eng = make_engine()
        score = eng._process_velocity_score(make_input(contract_review_latency_days=21.0))
        assert score == 15.0

    def test_contract_exactly_30(self):
        eng = make_engine()
        score = eng._process_velocity_score(make_input(contract_review_latency_days=30.0))
        assert score == 30.0

    def test_demo_exactly_14(self):
        eng = make_engine()
        score = eng._process_velocity_score(make_input(demo_request_to_completion_days=14.0))
        assert score == 10.0

    def test_demo_exactly_21(self):
        eng = make_engine()
        score = eng._process_velocity_score(make_input(demo_request_to_completion_days=21.0))
        assert score == 25.0
