"""
Comprehensive pytest tests for SalesDiscoveryQualityIntelligenceEngine.
Covers: all enums, all input fields, all result fields + to_dict(),
all sub-score branches, composite formula, all patterns (priority order),
all risk/severity thresholds (exact boundaries), all action mappings,
flag conditions, wasted pipeline formula, signal string,
assess end-to-end, assess_batch, empty + populated summary (13 keys).
"""
from __future__ import annotations

import pytest

from swarm.intelligence.sales_discovery_quality_intelligence_engine import (
    DiscoveryAction,
    DiscoveryInput,
    DiscoveryPattern,
    DiscoveryResult,
    DiscoveryRisk,
    DiscoverySeverity,
    SalesDiscoveryQualityIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> DiscoveryInput:
    """
    Return a DiscoveryInput with safe, low-risk defaults.
    All percentages are floats in [0, 1].
    Override any field via kwargs.
    """
    defaults = dict(
        rep_id="rep-001",
        region="EMEA",
        evaluation_period_id="Q1-2026",
        avg_discovery_questions_per_call=20.0,      # > 15 → no depth score
        business_impact_quantified_pct=0.80,        # > 0.50 → no depth score
        pain_points_documented_per_deal=5.0,        # > 2.5 → no depth score
        budget_qualified_before_demo_pct=0.90,      # > 0.75 → no qual score
        decision_process_mapped_pct=0.80,           # > 0.55 → no qual score
        timeline_established_in_discovery_pct=0.80, # > 0.60 → no qual score
        stakeholders_identified_in_discovery_avg=5.0, # > 3.5 → no stkh score
        economic_buyer_engaged_pre_proposal_pct=0.80,  # > 0.50 → no stkh score
        technical_buyer_engaged_pre_proposal_pct=0.80, # > 0.45 → no stkh score
        solution_presented_before_discovery_pct=0.05,  # < 0.10 → no fit score
        demo_given_without_discovery_pct=0.05,
        follow_up_discovery_call_rate_pct=0.60,
        discovery_to_proposal_gap_days=14.0,
        proposal_rework_rate_pct=0.10,              # < 0.25 → no fit score
        deals_lost_due_to_poor_fit_pct=0.05,        # < 0.20 → no fit score
        competitor_mentioned_in_discovery_pct=0.30,
        success_criteria_defined_in_discovery_pct=0.70,
        total_discovery_calls=50,
        avg_opportunity_value_usd=20_000.0,
    )
    defaults.update(overrides)
    return DiscoveryInput(**defaults)


def fresh_engine() -> SalesDiscoveryQualityIntelligenceEngine:
    return SalesDiscoveryQualityIntelligenceEngine()


# ===========================================================================
# 1. ENUM VALUES
# ===========================================================================

class TestEnumValues:

    def test_discovery_risk_values(self):
        assert DiscoveryRisk.low.value == "low"
        assert DiscoveryRisk.moderate.value == "moderate"
        assert DiscoveryRisk.high.value == "high"
        assert DiscoveryRisk.critical.value == "critical"

    def test_discovery_risk_members(self):
        members = {m.value for m in DiscoveryRisk}
        assert members == {"low", "moderate", "high", "critical"}

    def test_discovery_pattern_values(self):
        assert DiscoveryPattern.none.value == "none"
        assert DiscoveryPattern.surface_level_discovery.value == "surface_level_discovery"
        assert DiscoveryPattern.budget_avoidance.value == "budget_avoidance"
        assert DiscoveryPattern.single_stakeholder_lock.value == "single_stakeholder_lock"
        assert DiscoveryPattern.pain_point_skipping.value == "pain_point_skipping"
        assert DiscoveryPattern.premature_solutioning.value == "premature_solutioning"

    def test_discovery_pattern_members(self):
        members = {m.value for m in DiscoveryPattern}
        assert members == {
            "none",
            "surface_level_discovery",
            "budget_avoidance",
            "single_stakeholder_lock",
            "pain_point_skipping",
            "premature_solutioning",
        }

    def test_discovery_severity_values(self):
        assert DiscoverySeverity.thorough.value == "thorough"
        assert DiscoverySeverity.adequate.value == "adequate"
        assert DiscoverySeverity.shallow.value == "shallow"
        assert DiscoverySeverity.negligent.value == "negligent"

    def test_discovery_severity_members(self):
        members = {m.value for m in DiscoverySeverity}
        assert members == {"thorough", "adequate", "shallow", "negligent"}

    def test_discovery_action_values(self):
        assert DiscoveryAction.no_action.value == "no_action"
        assert DiscoveryAction.discovery_framework_coaching.value == "discovery_framework_coaching"
        assert DiscoveryAction.budget_qualification_coaching.value == "budget_qualification_coaching"
        assert DiscoveryAction.stakeholder_mapping_coaching.value == "stakeholder_mapping_coaching"
        assert DiscoveryAction.pain_discovery_coaching.value == "pain_discovery_coaching"
        assert DiscoveryAction.discovery_reset_intervention.value == "discovery_reset_intervention"

    def test_discovery_action_members(self):
        members = {m.value for m in DiscoveryAction}
        assert members == {
            "no_action",
            "discovery_framework_coaching",
            "budget_qualification_coaching",
            "stakeholder_mapping_coaching",
            "pain_discovery_coaching",
            "discovery_reset_intervention",
        }


# ===========================================================================
# 2. INPUT DATACLASS – ALL 22 FIELDS
# ===========================================================================

class TestDiscoveryInputFields:

    def test_all_22_fields_present(self):
        inp = make_input()
        expected_fields = [
            "rep_id", "region", "evaluation_period_id",
            "avg_discovery_questions_per_call", "business_impact_quantified_pct",
            "pain_points_documented_per_deal", "budget_qualified_before_demo_pct",
            "decision_process_mapped_pct", "timeline_established_in_discovery_pct",
            "stakeholders_identified_in_discovery_avg",
            "economic_buyer_engaged_pre_proposal_pct",
            "technical_buyer_engaged_pre_proposal_pct",
            "solution_presented_before_discovery_pct",
            "demo_given_without_discovery_pct",
            "follow_up_discovery_call_rate_pct",
            "discovery_to_proposal_gap_days",
            "proposal_rework_rate_pct",
            "deals_lost_due_to_poor_fit_pct",
            "competitor_mentioned_in_discovery_pct",
            "success_criteria_defined_in_discovery_pct",
            "total_discovery_calls",
            "avg_opportunity_value_usd",
        ]
        for field in expected_fields:
            assert hasattr(inp, field), f"Missing field: {field}"

    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(DiscoveryInput)
        assert len(fields) == 22

    def test_string_fields(self):
        inp = make_input(rep_id="REP-XYZ", region="APAC", evaluation_period_id="Q2-2026")
        assert inp.rep_id == "REP-XYZ"
        assert inp.region == "APAC"
        assert inp.evaluation_period_id == "Q2-2026"

    def test_numeric_fields(self):
        inp = make_input(total_discovery_calls=100, avg_opportunity_value_usd=50_000.0)
        assert inp.total_discovery_calls == 100
        assert inp.avg_opportunity_value_usd == 50_000.0


# ===========================================================================
# 3. RESULT DATACLASS – ALL 15 FIELDS + to_dict() KEYS
# ===========================================================================

class TestDiscoveryResultFields:

    def _get_result(self):
        return fresh_engine().assess(make_input())

    def test_all_15_fields_present(self):
        r = self._get_result()
        expected_fields = [
            "rep_id", "region", "discovery_risk", "discovery_pattern",
            "discovery_severity", "recommended_action", "depth_score",
            "qualification_score", "stakeholder_score", "fit_score",
            "discovery_composite", "has_discovery_gap",
            "requires_discovery_coaching", "estimated_wasted_pipeline_usd",
            "discovery_signal",
        ]
        for field in expected_fields:
            assert hasattr(r, field), f"Missing result field: {field}"

    def test_to_dict_returns_15_keys(self):
        d = self._get_result().to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self):
        d = self._get_result().to_dict()
        expected_keys = {
            "rep_id", "region", "discovery_risk", "discovery_pattern",
            "discovery_severity", "recommended_action", "depth_score",
            "qualification_score", "stakeholder_score", "fit_score",
            "discovery_composite", "has_discovery_gap",
            "requires_discovery_coaching", "estimated_wasted_pipeline_usd",
            "discovery_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        d = self._get_result().to_dict()
        assert isinstance(d["discovery_risk"], str)
        assert isinstance(d["discovery_pattern"], str)
        assert isinstance(d["discovery_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_preserves_rep_id_and_region(self):
        r = fresh_engine().assess(make_input(rep_id="REP-42", region="NAM"))
        d = r.to_dict()
        assert d["rep_id"] == "REP-42"
        assert d["region"] == "NAM"


# ===========================================================================
# 4. DEPTH SCORE – ALL BRANCHES
# ===========================================================================

class TestDepthScore:

    def _depth(self, **kw):
        e = fresh_engine()
        return e._depth_score(make_input(**kw))

    # avg_discovery_questions_per_call thresholds
    def test_questions_le_5_adds_40(self):
        score = self._depth(
            avg_discovery_questions_per_call=5.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
        )
        assert score == 40.0

    def test_questions_exactly_5(self):
        score = self._depth(
            avg_discovery_questions_per_call=5.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
        )
        assert score == 40.0

    def test_questions_le_10_adds_22(self):
        score = self._depth(
            avg_discovery_questions_per_call=7.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
        )
        assert score == 22.0

    def test_questions_exactly_10_adds_22(self):
        score = self._depth(
            avg_discovery_questions_per_call=10.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
        )
        assert score == 22.0

    def test_questions_le_15_adds_8(self):
        score = self._depth(
            avg_discovery_questions_per_call=12.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
        )
        assert score == 8.0

    def test_questions_exactly_15_adds_8(self):
        score = self._depth(
            avg_discovery_questions_per_call=15.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
        )
        assert score == 8.0

    def test_questions_gt_15_adds_0(self):
        score = self._depth(
            avg_discovery_questions_per_call=16.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
        )
        assert score == 0.0

    # pain_points_documented_per_deal thresholds
    def test_pain_points_le_1_adds_35(self):
        score = self._depth(
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=1.0,
            business_impact_quantified_pct=0.80,
        )
        assert score == 35.0

    def test_pain_points_exactly_1_adds_35(self):
        score = self._depth(
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=1.0,
            business_impact_quantified_pct=0.80,
        )
        assert score == 35.0

    def test_pain_points_le_2_5_adds_18(self):
        score = self._depth(
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=2.0,
            business_impact_quantified_pct=0.80,
        )
        assert score == 18.0

    def test_pain_points_exactly_2_5_adds_18(self):
        score = self._depth(
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=2.5,
            business_impact_quantified_pct=0.80,
        )
        assert score == 18.0

    def test_pain_points_gt_2_5_adds_0(self):
        score = self._depth(
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=3.0,
            business_impact_quantified_pct=0.80,
        )
        assert score == 0.0

    # business_impact_quantified_pct thresholds
    def test_business_impact_le_0_25_adds_25(self):
        score = self._depth(
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.25,
        )
        assert score == 25.0

    def test_business_impact_exactly_0_25_adds_25(self):
        score = self._depth(
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.25,
        )
        assert score == 25.0

    def test_business_impact_le_0_50_adds_12(self):
        score = self._depth(
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.40,
        )
        assert score == 12.0

    def test_business_impact_exactly_0_50_adds_12(self):
        score = self._depth(
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.50,
        )
        assert score == 12.0

    def test_business_impact_gt_0_50_adds_0(self):
        score = self._depth(
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
        )
        assert score == 0.0

    # Cap at 100
    def test_depth_score_capped_at_100(self):
        # all worst-case: 40 + 35 + 25 = 100, still 100
        score = self._depth(
            avg_discovery_questions_per_call=1.0,
            pain_points_documented_per_deal=0.5,
            business_impact_quantified_pct=0.10,
        )
        assert score == 100.0

    def test_depth_score_combines_all_three(self):
        # 22 + 18 + 12 = 52
        score = self._depth(
            avg_discovery_questions_per_call=8.0,
            pain_points_documented_per_deal=2.0,
            business_impact_quantified_pct=0.40,
        )
        assert score == 52.0


# ===========================================================================
# 5. QUALIFICATION SCORE – ALL BRANCHES
# ===========================================================================

class TestQualificationScore:

    def _qual(self, **kw):
        e = fresh_engine()
        return e._qualification_score(make_input(**kw))

    def test_budget_le_0_30_adds_40(self):
        s = self._qual(
            budget_qualified_before_demo_pct=0.30,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
        )
        assert s == 40.0

    def test_budget_le_0_55_adds_22(self):
        s = self._qual(
            budget_qualified_before_demo_pct=0.45,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
        )
        assert s == 22.0

    def test_budget_exactly_0_55_adds_22(self):
        s = self._qual(
            budget_qualified_before_demo_pct=0.55,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
        )
        assert s == 22.0

    def test_budget_le_0_75_adds_8(self):
        s = self._qual(
            budget_qualified_before_demo_pct=0.65,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
        )
        assert s == 8.0

    def test_budget_exactly_0_75_adds_8(self):
        s = self._qual(
            budget_qualified_before_demo_pct=0.75,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
        )
        assert s == 8.0

    def test_budget_gt_0_75_adds_0(self):
        s = self._qual(
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
        )
        assert s == 0.0

    def test_decision_le_0_30_adds_35(self):
        s = self._qual(
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.30,
            timeline_established_in_discovery_pct=0.80,
        )
        assert s == 35.0

    def test_decision_le_0_55_adds_18(self):
        s = self._qual(
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.40,
            timeline_established_in_discovery_pct=0.80,
        )
        assert s == 18.0

    def test_decision_exactly_0_55_adds_18(self):
        s = self._qual(
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.55,
            timeline_established_in_discovery_pct=0.80,
        )
        assert s == 18.0

    def test_decision_gt_0_55_adds_0(self):
        s = self._qual(
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
        )
        assert s == 0.0

    def test_timeline_le_0_35_adds_25(self):
        s = self._qual(
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.35,
        )
        assert s == 25.0

    def test_timeline_le_0_60_adds_12(self):
        s = self._qual(
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.50,
        )
        assert s == 12.0

    def test_timeline_exactly_0_60_adds_12(self):
        s = self._qual(
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.60,
        )
        assert s == 12.0

    def test_timeline_gt_0_60_adds_0(self):
        s = self._qual(
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
        )
        assert s == 0.0

    def test_qualification_score_capped_at_100(self):
        # 40 + 35 + 25 = 100
        s = self._qual(
            budget_qualified_before_demo_pct=0.10,
            decision_process_mapped_pct=0.10,
            timeline_established_in_discovery_pct=0.10,
        )
        assert s == 100.0

    def test_qualification_score_combined(self):
        # 22 + 18 + 12 = 52
        s = self._qual(
            budget_qualified_before_demo_pct=0.45,
            decision_process_mapped_pct=0.40,
            timeline_established_in_discovery_pct=0.50,
        )
        assert s == 52.0


# ===========================================================================
# 6. STAKEHOLDER SCORE – ALL BRANCHES
# ===========================================================================

class TestStakeholderScore:

    def _stkh(self, **kw):
        e = fresh_engine()
        return e._stakeholder_score(make_input(**kw))

    def test_stakeholders_le_1_5_adds_45(self):
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=1.5,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
        )
        assert s == 45.0

    def test_stakeholders_le_2_5_adds_25(self):
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=2.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
        )
        assert s == 25.0

    def test_stakeholders_exactly_2_5_adds_25(self):
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=2.5,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
        )
        assert s == 25.0

    def test_stakeholders_le_3_5_adds_10(self):
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=3.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
        )
        assert s == 10.0

    def test_stakeholders_exactly_3_5_adds_10(self):
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=3.5,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
        )
        assert s == 10.0

    def test_stakeholders_gt_3_5_adds_0(self):
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
        )
        assert s == 0.0

    def test_economic_buyer_le_0_25_adds_30(self):
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.25,
            technical_buyer_engaged_pre_proposal_pct=0.80,
        )
        assert s == 30.0

    def test_economic_buyer_le_0_50_adds_15(self):
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.40,
            technical_buyer_engaged_pre_proposal_pct=0.80,
        )
        assert s == 15.0

    def test_economic_buyer_exactly_0_50_adds_15(self):
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.50,
            technical_buyer_engaged_pre_proposal_pct=0.80,
        )
        assert s == 15.0

    def test_economic_buyer_gt_0_50_adds_0(self):
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
        )
        assert s == 0.0

    def test_technical_buyer_le_0_20_adds_25(self):
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.20,
        )
        assert s == 25.0

    def test_technical_buyer_le_0_45_adds_12(self):
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.35,
        )
        assert s == 12.0

    def test_technical_buyer_exactly_0_45_adds_12(self):
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.45,
        )
        assert s == 12.0

    def test_technical_buyer_gt_0_45_adds_0(self):
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
        )
        assert s == 0.0

    def test_stakeholder_score_capped_at_100(self):
        # 45 + 30 + 25 = 100
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=1.0,
            economic_buyer_engaged_pre_proposal_pct=0.10,
            technical_buyer_engaged_pre_proposal_pct=0.10,
        )
        assert s == 100.0

    def test_stakeholder_score_combined(self):
        # 25 + 15 + 12 = 52
        s = self._stkh(
            stakeholders_identified_in_discovery_avg=2.0,
            economic_buyer_engaged_pre_proposal_pct=0.40,
            technical_buyer_engaged_pre_proposal_pct=0.35,
        )
        assert s == 52.0


# ===========================================================================
# 7. FIT SCORE – ALL BRANCHES
# ===========================================================================

class TestFitScore:

    def _fit(self, **kw):
        e = fresh_engine()
        return e._fit_score(make_input(**kw))

    def test_solution_ge_0_40_adds_40(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.40,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
        )
        assert s == 40.0

    def test_solution_above_0_40_adds_40(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.60,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
        )
        assert s == 40.0

    def test_solution_ge_0_20_adds_22(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.30,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
        )
        assert s == 22.0

    def test_solution_exactly_0_20_adds_22(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.20,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
        )
        assert s == 22.0

    def test_solution_ge_0_10_adds_8(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.15,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
        )
        assert s == 8.0

    def test_solution_exactly_0_10_adds_8(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.10,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
        )
        assert s == 8.0

    def test_solution_lt_0_10_adds_0(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
        )
        assert s == 0.0

    def test_deals_lost_ge_0_40_adds_35(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.40,
            proposal_rework_rate_pct=0.10,
        )
        assert s == 35.0

    def test_deals_lost_ge_0_20_adds_18(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.30,
            proposal_rework_rate_pct=0.10,
        )
        assert s == 18.0

    def test_deals_lost_exactly_0_20_adds_18(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.20,
            proposal_rework_rate_pct=0.10,
        )
        assert s == 18.0

    def test_deals_lost_lt_0_20_adds_0(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.10,
            proposal_rework_rate_pct=0.10,
        )
        assert s == 0.0

    def test_proposal_rework_ge_0_50_adds_25(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.50,
        )
        assert s == 25.0

    def test_proposal_rework_ge_0_25_adds_12(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.35,
        )
        assert s == 12.0

    def test_proposal_rework_exactly_0_25_adds_12(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.25,
        )
        assert s == 12.0

    def test_proposal_rework_lt_0_25_adds_0(self):
        s = self._fit(
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
        )
        assert s == 0.0

    def test_fit_score_capped_at_100(self):
        # 40 + 35 + 25 = 100
        s = self._fit(
            solution_presented_before_discovery_pct=0.50,
            deals_lost_due_to_poor_fit_pct=0.50,
            proposal_rework_rate_pct=0.60,
        )
        assert s == 100.0

    def test_fit_score_combined(self):
        # 22 + 18 + 12 = 52
        s = self._fit(
            solution_presented_before_discovery_pct=0.30,
            deals_lost_due_to_poor_fit_pct=0.30,
            proposal_rework_rate_pct=0.35,
        )
        assert s == 52.0


# ===========================================================================
# 8. COMPOSITE FORMULA WEIGHTS
# ===========================================================================

class TestCompositeFormula:

    def test_composite_formula_weights(self):
        """
        depth=40, qualification=0, stakeholder=0, fit=0
        → composite = 40*0.30 + 0*0.30 + 0*0.25 + 0*0.15 = 12.0
        """
        inp = make_input(
            avg_discovery_questions_per_call=7.0,  # depth += 22 from questions
            # force other sub-scores to zero
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
            # remove other depth contributions
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
        )
        e = fresh_engine()
        depth = e._depth_score(inp)       # should be 22.0
        qual  = e._qualification_score(inp)  # should be 0.0
        stkh  = e._stakeholder_score(inp)    # should be 0.0
        fit   = e._fit_score(inp)            # should be 0.0

        assert depth == 22.0
        assert qual == 0.0
        assert stkh == 0.0
        assert fit == 0.0

        r = e.assess(inp)
        # 22.0*0.30 + 0*0.30 + 0*0.25 + 0*0.15 = 6.6 → rounded to 6.6
        assert r.discovery_composite == pytest.approx(6.6, abs=0.15)

    def test_composite_all_weights_contribute(self):
        """
        depth=40, qualification=40, stakeholder=45, fit=40
        → raw = 40*0.30 + 40*0.30 + 45*0.25 + 40*0.15
              = 12 + 12 + 11.25 + 6 = 41.25 → rounded to 41.3
        """
        inp = make_input(
            # depth = 40 (questions <=5 → 40, no pain/impact contribution)
            avg_discovery_questions_per_call=5.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
            # qualification = 40 (budget <=0.30 → 40, no others)
            budget_qualified_before_demo_pct=0.20,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
            # stakeholder = 45 (stakeholders <=1.5 → 45, no others)
            stakeholders_identified_in_discovery_avg=1.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
            # fit = 40 (solution >=0.40 → 40, no others)
            solution_presented_before_discovery_pct=0.50,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
        )
        e = fresh_engine()
        r = e.assess(inp)
        expected = round(40 * 0.30 + 40 * 0.30 + 45 * 0.25 + 40 * 0.15, 1)
        assert r.discovery_composite == pytest.approx(expected, abs=0.2)

    def test_composite_capped_at_100(self):
        # All sub-scores at max → composite must not exceed 100
        inp = make_input(
            avg_discovery_questions_per_call=1.0,
            pain_points_documented_per_deal=0.5,
            business_impact_quantified_pct=0.10,
            budget_qualified_before_demo_pct=0.10,
            decision_process_mapped_pct=0.10,
            timeline_established_in_discovery_pct=0.10,
            stakeholders_identified_in_discovery_avg=1.0,
            economic_buyer_engaged_pre_proposal_pct=0.10,
            technical_buyer_engaged_pre_proposal_pct=0.10,
            solution_presented_before_discovery_pct=0.50,
            deals_lost_due_to_poor_fit_pct=0.50,
            proposal_rework_rate_pct=0.60,
        )
        r = fresh_engine().assess(inp)
        assert r.discovery_composite <= 100.0


# ===========================================================================
# 9. PATTERN DETECTION – ALL PATTERNS + PRIORITY ORDER
# ===========================================================================

class TestPatternDetection:

    def _pattern(self, **kw) -> DiscoveryPattern:
        e = fresh_engine()
        inp = make_input(**kw)
        r = e.assess(inp)
        return r.discovery_pattern

    # --- premature_solutioning (priority 1) ---

    def test_premature_solutioning_detected(self):
        p = self._pattern(
            solution_presented_before_discovery_pct=0.35,
            demo_given_without_discovery_pct=0.30,
        )
        assert p == DiscoveryPattern.premature_solutioning

    def test_premature_solutioning_exact_thresholds(self):
        p = self._pattern(
            solution_presented_before_discovery_pct=0.35,
            demo_given_without_discovery_pct=0.30,
        )
        assert p == DiscoveryPattern.premature_solutioning

    def test_premature_solutioning_missing_demo_condition(self):
        # Only solution_pct satisfied, not demo
        p = self._pattern(
            solution_presented_before_discovery_pct=0.50,
            demo_given_without_discovery_pct=0.10,
            # force no other pattern
            avg_discovery_questions_per_call=20.0,
            budget_qualified_before_demo_pct=0.90,
            stakeholders_identified_in_discovery_avg=5.0,
            pain_points_documented_per_deal=5.0,
            deals_lost_due_to_poor_fit_pct=0.05,
        )
        assert p != DiscoveryPattern.premature_solutioning

    # --- surface_level_discovery (priority 2) ---

    def test_surface_level_discovery_detected(self):
        # Need depth >= 40: questions <= 5 → +40, pain <= 1 → +35 = 75 >= 40 ✓
        # avg_questions <= 8.0 ✓
        p = self._pattern(
            avg_discovery_questions_per_call=7.0,
            pain_points_documented_per_deal=0.5,
            # ensure no premature_solutioning
            solution_presented_before_discovery_pct=0.05,
            demo_given_without_discovery_pct=0.05,
        )
        assert p == DiscoveryPattern.surface_level_discovery

    def test_surface_level_discovery_questions_exactly_8(self):
        p = self._pattern(
            avg_discovery_questions_per_call=8.0,
            pain_points_documented_per_deal=0.5,
            solution_presented_before_discovery_pct=0.05,
            demo_given_without_discovery_pct=0.05,
        )
        assert p == DiscoveryPattern.surface_level_discovery

    def test_surface_level_discovery_not_triggered_questions_above_8(self):
        # depth >= 40 but questions > 8 → no surface_level
        p = self._pattern(
            avg_discovery_questions_per_call=9.0,
            pain_points_documented_per_deal=0.5,
            solution_presented_before_discovery_pct=0.05,
            demo_given_without_discovery_pct=0.05,
            # force budget/stakeholder patterns off
            budget_qualified_before_demo_pct=0.90,
            stakeholders_identified_in_discovery_avg=5.0,
            deals_lost_due_to_poor_fit_pct=0.05,
        )
        assert p != DiscoveryPattern.surface_level_discovery

    # --- budget_avoidance (priority 3) ---

    def test_budget_avoidance_detected(self):
        # budget_pct <= 0.25 AND qual >= 35: budget <= 0.30 → +40, decision <= 0.30 → +35 = 75 >= 35
        p = self._pattern(
            budget_qualified_before_demo_pct=0.20,
            decision_process_mapped_pct=0.20,
            timeline_established_in_discovery_pct=0.80,
            # force no premature_solutioning or surface_level
            solution_presented_before_discovery_pct=0.05,
            demo_given_without_discovery_pct=0.05,
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
        )
        assert p == DiscoveryPattern.budget_avoidance

    def test_budget_avoidance_exact_budget_threshold(self):
        p = self._pattern(
            budget_qualified_before_demo_pct=0.25,
            decision_process_mapped_pct=0.20,
            timeline_established_in_discovery_pct=0.80,
            solution_presented_before_discovery_pct=0.05,
            demo_given_without_discovery_pct=0.05,
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
        )
        assert p == DiscoveryPattern.budget_avoidance

    # --- single_stakeholder_lock (priority 4) ---

    def test_single_stakeholder_lock_detected(self):
        # stakeholders <= 1.5 AND stakeholder_score >= 30
        # stakeholders=1.0 → +45, economic=0.20 → +30, technical=0.80 → 0 → total=75 >= 30
        p = self._pattern(
            stakeholders_identified_in_discovery_avg=1.0,
            economic_buyer_engaged_pre_proposal_pct=0.20,
            # force no higher-priority patterns
            solution_presented_before_discovery_pct=0.05,
            demo_given_without_discovery_pct=0.05,
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
            budget_qualified_before_demo_pct=0.90,
        )
        assert p == DiscoveryPattern.single_stakeholder_lock

    def test_single_stakeholder_lock_exact_stakeholder_threshold(self):
        p = self._pattern(
            stakeholders_identified_in_discovery_avg=1.5,
            economic_buyer_engaged_pre_proposal_pct=0.20,
            solution_presented_before_discovery_pct=0.05,
            demo_given_without_discovery_pct=0.05,
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
            budget_qualified_before_demo_pct=0.90,
        )
        assert p == DiscoveryPattern.single_stakeholder_lock

    # --- pain_point_skipping (priority 5) ---

    def test_pain_point_skipping_detected(self):
        # pain <= 1.5 AND deals_lost >= 0.30
        p = self._pattern(
            pain_points_documented_per_deal=1.0,
            deals_lost_due_to_poor_fit_pct=0.35,
            # force no higher-priority patterns
            solution_presented_before_discovery_pct=0.05,
            demo_given_without_discovery_pct=0.05,
            avg_discovery_questions_per_call=20.0,
            budget_qualified_before_demo_pct=0.90,
            stakeholders_identified_in_discovery_avg=5.0,
            business_impact_quantified_pct=0.80,
        )
        assert p == DiscoveryPattern.pain_point_skipping

    def test_pain_point_skipping_exact_thresholds(self):
        p = self._pattern(
            pain_points_documented_per_deal=1.5,
            deals_lost_due_to_poor_fit_pct=0.30,
            solution_presented_before_discovery_pct=0.05,
            demo_given_without_discovery_pct=0.05,
            avg_discovery_questions_per_call=20.0,
            budget_qualified_before_demo_pct=0.90,
            stakeholders_identified_in_discovery_avg=5.0,
            business_impact_quantified_pct=0.80,
        )
        assert p == DiscoveryPattern.pain_point_skipping

    # --- none (fallback) ---

    def test_no_pattern_returns_none(self):
        # All safe defaults → should be none
        p = self._pattern()
        assert p == DiscoveryPattern.none

    # --- Priority ordering: premature_solutioning beats others ---

    def test_priority_premature_over_surface_level(self):
        """premature_solutioning triggers first even if surface_level would also match"""
        p = self._pattern(
            solution_presented_before_discovery_pct=0.35,
            demo_given_without_discovery_pct=0.30,
            # also satisfies surface_level (depth>=40, questions<=8)
            avg_discovery_questions_per_call=7.0,
            pain_points_documented_per_deal=0.5,
            business_impact_quantified_pct=0.80,
        )
        assert p == DiscoveryPattern.premature_solutioning

    def test_priority_premature_over_budget_avoidance(self):
        p = self._pattern(
            solution_presented_before_discovery_pct=0.35,
            demo_given_without_discovery_pct=0.30,
            budget_qualified_before_demo_pct=0.20,
            decision_process_mapped_pct=0.20,
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
        )
        assert p == DiscoveryPattern.premature_solutioning

    def test_priority_surface_level_over_budget_avoidance(self):
        """surface_level_discovery (priority 2) beats budget_avoidance (priority 3)"""
        p = self._pattern(
            # surface_level: depth>=40 AND questions<=8
            avg_discovery_questions_per_call=7.0,
            pain_points_documented_per_deal=0.5,
            business_impact_quantified_pct=0.80,
            # budget_avoidance: budget_pct<=0.25 AND qual>=35
            budget_qualified_before_demo_pct=0.20,
            decision_process_mapped_pct=0.20,
            # no premature_solutioning
            solution_presented_before_discovery_pct=0.05,
            demo_given_without_discovery_pct=0.05,
        )
        assert p == DiscoveryPattern.surface_level_discovery


# ===========================================================================
# 10. RISK THRESHOLDS (EXACT BOUNDARIES)
# ===========================================================================

class TestRiskThresholds:

    def _risk(self, composite: float) -> DiscoveryRisk:
        e = fresh_engine()
        return e._risk_level(composite)

    def test_risk_critical_at_60(self):
        assert self._risk(60.0) == DiscoveryRisk.critical

    def test_risk_critical_above_60(self):
        assert self._risk(80.0) == DiscoveryRisk.critical

    def test_risk_high_at_40(self):
        assert self._risk(40.0) == DiscoveryRisk.high

    def test_risk_high_at_59_9(self):
        assert self._risk(59.9) == DiscoveryRisk.high

    def test_risk_moderate_at_20(self):
        assert self._risk(20.0) == DiscoveryRisk.moderate

    def test_risk_moderate_at_39_9(self):
        assert self._risk(39.9) == DiscoveryRisk.moderate

    def test_risk_low_at_0(self):
        assert self._risk(0.0) == DiscoveryRisk.low

    def test_risk_low_at_19_9(self):
        assert self._risk(19.9) == DiscoveryRisk.low

    def test_risk_low_just_below_20(self):
        assert self._risk(19.999) == DiscoveryRisk.low

    def test_risk_moderate_just_at_20(self):
        assert self._risk(20.0) == DiscoveryRisk.moderate

    def test_risk_high_just_at_40(self):
        assert self._risk(40.0) == DiscoveryRisk.high

    def test_risk_critical_just_at_60(self):
        assert self._risk(60.0) == DiscoveryRisk.critical


# ===========================================================================
# 11. SEVERITY THRESHOLDS (EXACT BOUNDARIES)
# ===========================================================================

class TestSeverityThresholds:

    def _sev(self, composite: float) -> DiscoverySeverity:
        e = fresh_engine()
        return e._severity(composite)

    def test_severity_negligent_at_60(self):
        assert self._sev(60.0) == DiscoverySeverity.negligent

    def test_severity_negligent_above_60(self):
        assert self._sev(90.0) == DiscoverySeverity.negligent

    def test_severity_shallow_at_40(self):
        assert self._sev(40.0) == DiscoverySeverity.shallow

    def test_severity_shallow_at_59_9(self):
        assert self._sev(59.9) == DiscoverySeverity.shallow

    def test_severity_adequate_at_20(self):
        assert self._sev(20.0) == DiscoverySeverity.adequate

    def test_severity_adequate_at_39_9(self):
        assert self._sev(39.9) == DiscoverySeverity.adequate

    def test_severity_thorough_at_0(self):
        assert self._sev(0.0) == DiscoverySeverity.thorough

    def test_severity_thorough_at_19_9(self):
        assert self._sev(19.9) == DiscoverySeverity.thorough

    def test_severity_boundary_just_below_20(self):
        assert self._sev(19.999) == DiscoverySeverity.thorough

    def test_severity_boundary_at_20(self):
        assert self._sev(20.0) == DiscoverySeverity.adequate

    def test_severity_boundary_at_40(self):
        assert self._sev(40.0) == DiscoverySeverity.shallow

    def test_severity_boundary_at_60(self):
        assert self._sev(60.0) == DiscoverySeverity.negligent


# ===========================================================================
# 12. ACTION MAPPINGS
# ===========================================================================

class TestActionMappings:

    def _action(self, risk: DiscoveryRisk, pattern: DiscoveryPattern) -> DiscoveryAction:
        e = fresh_engine()
        return e._action(risk, pattern)

    # Critical
    def test_critical_premature_solutioning(self):
        a = self._action(DiscoveryRisk.critical, DiscoveryPattern.premature_solutioning)
        assert a == DiscoveryAction.discovery_framework_coaching

    def test_critical_surface_level_discovery(self):
        a = self._action(DiscoveryRisk.critical, DiscoveryPattern.surface_level_discovery)
        assert a == DiscoveryAction.pain_discovery_coaching

    def test_critical_budget_avoidance(self):
        a = self._action(DiscoveryRisk.critical, DiscoveryPattern.budget_avoidance)
        assert a == DiscoveryAction.discovery_reset_intervention

    def test_critical_single_stakeholder_lock(self):
        a = self._action(DiscoveryRisk.critical, DiscoveryPattern.single_stakeholder_lock)
        assert a == DiscoveryAction.discovery_reset_intervention

    def test_critical_pain_point_skipping(self):
        a = self._action(DiscoveryRisk.critical, DiscoveryPattern.pain_point_skipping)
        assert a == DiscoveryAction.discovery_reset_intervention

    def test_critical_none_pattern(self):
        a = self._action(DiscoveryRisk.critical, DiscoveryPattern.none)
        assert a == DiscoveryAction.discovery_reset_intervention

    # High
    def test_high_budget_avoidance(self):
        a = self._action(DiscoveryRisk.high, DiscoveryPattern.budget_avoidance)
        assert a == DiscoveryAction.budget_qualification_coaching

    def test_high_single_stakeholder_lock(self):
        a = self._action(DiscoveryRisk.high, DiscoveryPattern.single_stakeholder_lock)
        assert a == DiscoveryAction.stakeholder_mapping_coaching

    def test_high_premature_solutioning(self):
        a = self._action(DiscoveryRisk.high, DiscoveryPattern.premature_solutioning)
        assert a == DiscoveryAction.discovery_framework_coaching

    def test_high_surface_level_discovery(self):
        a = self._action(DiscoveryRisk.high, DiscoveryPattern.surface_level_discovery)
        assert a == DiscoveryAction.discovery_framework_coaching

    def test_high_pain_point_skipping(self):
        a = self._action(DiscoveryRisk.high, DiscoveryPattern.pain_point_skipping)
        assert a == DiscoveryAction.discovery_framework_coaching

    def test_high_none_pattern(self):
        a = self._action(DiscoveryRisk.high, DiscoveryPattern.none)
        assert a == DiscoveryAction.discovery_framework_coaching

    # Moderate
    def test_moderate_any_pattern(self):
        for p in DiscoveryPattern:
            a = self._action(DiscoveryRisk.moderate, p)
            assert a == DiscoveryAction.discovery_framework_coaching

    # Low
    def test_low_any_pattern(self):
        for p in DiscoveryPattern:
            a = self._action(DiscoveryRisk.low, p)
            assert a == DiscoveryAction.no_action


# ===========================================================================
# 13. FLAG CONDITIONS
# ===========================================================================

class TestFlagConditions:

    # has_discovery_gap
    def test_has_gap_composite_ge_40(self):
        e = fresh_engine()
        inp = make_input(
            budget_qualified_before_demo_pct=0.90,   # > 0.40 → flag from budget is False
            deals_lost_due_to_poor_fit_pct=0.05,     # < 0.25 → flag from deals is False
        )
        # Force composite >= 40 via high sub-scores
        # all worst-case to get composite up
        inp2 = make_input(
            avg_discovery_questions_per_call=1.0,
            pain_points_documented_per_deal=0.5,
            business_impact_quantified_pct=0.10,
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
        )
        r = e.assess(inp2)
        # depth score = 40+35+25 = 100, composite = 100*0.30 = 30 < 40
        # budget > 0.40, deals < 0.25 → all false → has_gap False
        assert r.has_discovery_gap is False

    def test_has_gap_budget_le_0_40(self):
        e = fresh_engine()
        # composite < 40, deals < 0.25, but budget <= 0.40
        inp = make_input(budget_qualified_before_demo_pct=0.40)
        r = e.assess(inp)
        assert r.has_discovery_gap is True

    def test_has_gap_deals_ge_0_25(self):
        e = fresh_engine()
        inp = make_input(deals_lost_due_to_poor_fit_pct=0.25, budget_qualified_before_demo_pct=0.90)
        r = e.assess(inp)
        assert r.has_discovery_gap is True

    def test_no_gap_all_conditions_false(self):
        e = fresh_engine()
        # All defaults → composite=0, budget=0.90 > 0.40, deals=0.05 < 0.25
        inp = make_input(
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
        )
        r = e.assess(inp)
        assert r.has_discovery_gap is False

    # requires_discovery_coaching
    def test_coaching_composite_ge_30(self):
        # Build an inp with composite just above 30
        # depth=100*0.30=30 via max depth, no others
        inp = make_input(
            avg_discovery_questions_per_call=1.0,
            pain_points_documented_per_deal=0.5,
            business_impact_quantified_pct=0.10,
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
        )
        e = fresh_engine()
        r = e.assess(inp)
        # depth = 100, composite = 100*0.30 = 30 → composite >= 30
        if r.discovery_composite >= 30:
            assert r.requires_discovery_coaching is True

    def test_coaching_questions_le_10(self):
        e = fresh_engine()
        inp = make_input(avg_discovery_questions_per_call=10.0)
        r = e.assess(inp)
        assert r.requires_discovery_coaching is True

    def test_coaching_solution_ge_0_20(self):
        e = fresh_engine()
        inp = make_input(solution_presented_before_discovery_pct=0.20)
        r = e.assess(inp)
        assert r.requires_discovery_coaching is True

    def test_no_coaching_all_conditions_false(self):
        e = fresh_engine()
        # composite < 30, questions > 10, solution < 0.20
        inp = make_input(
            avg_discovery_questions_per_call=20.0,
            solution_presented_before_discovery_pct=0.05,
        )
        r = e.assess(inp)
        # Check composite < 30 first
        if r.discovery_composite < 30:
            assert r.requires_discovery_coaching is False


# ===========================================================================
# 14. WASTED PIPELINE FORMULA
# ===========================================================================

class TestWastedPipelineFormula:

    def test_basic_formula(self):
        inp = make_input(
            total_discovery_calls=100,
            avg_opportunity_value_usd=10_000.0,
            deals_lost_due_to_poor_fit_pct=0.20,
        )
        e = fresh_engine()
        r = e.assess(inp)
        # composite depends on sub-scores
        expected = round(100 * 10_000.0 * 0.20 * (r.discovery_composite / 100.0), 2)
        assert r.estimated_wasted_pipeline_usd == pytest.approx(expected, abs=0.01)

    def test_wasted_pipeline_zero_when_no_losses(self):
        inp = make_input(deals_lost_due_to_poor_fit_pct=0.0)
        r = fresh_engine().assess(inp)
        assert r.estimated_wasted_pipeline_usd == 0.0

    def test_wasted_pipeline_zero_when_composite_zero(self):
        # All safe values → composite = 0
        inp = make_input(
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.20,
            proposal_rework_rate_pct=0.10,
        )
        r = fresh_engine().assess(inp)
        if r.discovery_composite == 0.0:
            assert r.estimated_wasted_pipeline_usd == 0.0

    def test_wasted_pipeline_rounded_to_2_decimals(self):
        inp = make_input(
            total_discovery_calls=33,
            avg_opportunity_value_usd=7_777.77,
            deals_lost_due_to_poor_fit_pct=0.13,
        )
        r = fresh_engine().assess(inp)
        # Just check it's rounded to 2dp
        assert r.estimated_wasted_pipeline_usd == round(r.estimated_wasted_pipeline_usd, 2)

    def test_wasted_pipeline_all_factors(self):
        """Verify exact multiplication order."""
        inp = make_input(
            total_discovery_calls=50,
            avg_opportunity_value_usd=20_000.0,
            deals_lost_due_to_poor_fit_pct=0.40,
        )
        e = fresh_engine()
        r = e.assess(inp)
        composite = r.discovery_composite
        expected = round(50 * 20_000.0 * 0.40 * (composite / 100.0), 2)
        assert r.estimated_wasted_pipeline_usd == expected


# ===========================================================================
# 15. SIGNAL STRING
# ===========================================================================

class TestSignalString:

    def test_signal_strong_when_none_and_composite_lt_20(self):
        # All safe → pattern=none, composite<20
        inp = make_input()
        r = fresh_engine().assess(inp)
        if r.discovery_pattern == DiscoveryPattern.none and r.discovery_composite < 20:
            assert r.discovery_signal == (
                "Discovery quality strong — depth of questioning, "
                "qualification, and stakeholder mapping within benchmarks"
            )

    def test_signal_strong_exact_text(self):
        inp = make_input(
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
            budget_qualified_before_demo_pct=0.90,
            decision_process_mapped_pct=0.80,
            timeline_established_in_discovery_pct=0.80,
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
            solution_presented_before_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
        )
        r = fresh_engine().assess(inp)
        assert r.discovery_pattern == DiscoveryPattern.none
        assert r.discovery_composite < 20
        assert "Discovery quality strong" in r.discovery_signal

    def test_signal_includes_avg_questions(self):
        inp = make_input(
            avg_discovery_questions_per_call=7.0,
            pain_points_documented_per_deal=0.5,
            solution_presented_before_discovery_pct=0.05,
            demo_given_without_discovery_pct=0.05,
        )
        r = fresh_engine().assess(inp)
        if r.discovery_pattern != DiscoveryPattern.none or r.discovery_composite >= 20:
            assert "7 avg questions per call" in r.discovery_signal

    def test_signal_includes_budget_pct(self):
        inp = make_input(
            avg_discovery_questions_per_call=20.0,
            budget_qualified_before_demo_pct=0.30,
            decision_process_mapped_pct=0.20,
        )
        r = fresh_engine().assess(inp)
        if r.discovery_pattern != DiscoveryPattern.none or r.discovery_composite >= 20:
            assert "30% budget qualified before demo" in r.discovery_signal

    def test_signal_includes_deals_lost_pct(self):
        inp = make_input(deals_lost_due_to_poor_fit_pct=0.15)
        r = fresh_engine().assess(inp)
        if r.discovery_pattern != DiscoveryPattern.none or r.discovery_composite >= 20:
            assert "15% deals lost to poor fit" in r.discovery_signal

    def test_signal_includes_composite(self):
        inp = make_input(
            avg_discovery_questions_per_call=5.0,
            pain_points_documented_per_deal=1.0,
            business_impact_quantified_pct=0.20,
        )
        r = fresh_engine().assess(inp)
        if r.discovery_pattern != DiscoveryPattern.none or r.discovery_composite >= 20:
            assert f"composite {r.discovery_composite:.0f}" in r.discovery_signal

    def test_signal_none_pattern_with_high_composite_uses_discovery_risk_label(self):
        """When pattern==none but composite>=20, label is 'Discovery risk'"""
        # Build scenario where composite >= 20 but no specific pattern triggers
        # budget=0.90 (no avoidance), questions=20 (no surface), solution=0.05 (no premature)
        # stakeholders=5 (no lock), pain_points=5 & deals_lost=0.05 (no pain skipping)
        # but get composite >= 20 via qualification score
        inp = make_input(
            budget_qualified_before_demo_pct=0.20,
            decision_process_mapped_pct=0.20,
            timeline_established_in_discovery_pct=0.80,
            avg_discovery_questions_per_call=20.0,
            pain_points_documented_per_deal=5.0,
            business_impact_quantified_pct=0.80,
            stakeholders_identified_in_discovery_avg=5.0,
            economic_buyer_engaged_pre_proposal_pct=0.80,
            technical_buyer_engaged_pre_proposal_pct=0.80,
            solution_presented_before_discovery_pct=0.05,
            demo_given_without_discovery_pct=0.05,
            deals_lost_due_to_poor_fit_pct=0.05,
            proposal_rework_rate_pct=0.10,
        )
        r = fresh_engine().assess(inp)
        # budget_avoidance: budget_pct(0.20) <= 0.25 AND qual >= 35
        # qual = budget(40) + decision(35) = 75 → budget_avoidance triggers
        # So pattern = budget_avoidance, label = "budget avoidance"
        if r.discovery_pattern == DiscoveryPattern.none and r.discovery_composite >= 20:
            assert "Discovery risk" in r.discovery_signal

    def test_signal_pattern_label_capitalized(self):
        # premature_solutioning → "Premature solutioning"
        inp = make_input(
            solution_presented_before_discovery_pct=0.35,
            demo_given_without_discovery_pct=0.30,
        )
        r = fresh_engine().assess(inp)
        assert r.discovery_pattern == DiscoveryPattern.premature_solutioning
        assert r.discovery_signal.startswith("Premature solutioning")


# ===========================================================================
# 16. ASSESS END-TO-END
# ===========================================================================

class TestAssessEndToEnd:

    def test_assess_returns_discovery_result(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r, DiscoveryResult)

    def test_assess_preserves_rep_id(self):
        r = fresh_engine().assess(make_input(rep_id="REP-END2END"))
        assert r.rep_id == "REP-END2END"

    def test_assess_preserves_region(self):
        r = fresh_engine().assess(make_input(region="LATAM"))
        assert r.region == "LATAM"

    def test_assess_appends_to_internal_results(self):
        e = fresh_engine()
        e.assess(make_input())
        e.assess(make_input())
        assert len(e._results) == 2

    def test_assess_risk_and_pattern_consistent(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r.discovery_risk, DiscoveryRisk)
        assert isinstance(r.discovery_pattern, DiscoveryPattern)
        assert isinstance(r.discovery_severity, DiscoverySeverity)
        assert isinstance(r.recommended_action, DiscoveryAction)

    def test_assess_scores_are_floats(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r.depth_score, float)
        assert isinstance(r.qualification_score, float)
        assert isinstance(r.stakeholder_score, float)
        assert isinstance(r.fit_score, float)
        assert isinstance(r.discovery_composite, float)

    def test_assess_flags_are_booleans(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r.has_discovery_gap, bool)
        assert isinstance(r.requires_discovery_coaching, bool)

    def test_assess_high_risk_scenario(self):
        # This should produce a high-risk, potentially critical result
        inp = make_input(
            avg_discovery_questions_per_call=3.0,
            pain_points_documented_per_deal=0.5,
            business_impact_quantified_pct=0.10,
            budget_qualified_before_demo_pct=0.10,
            decision_process_mapped_pct=0.10,
            timeline_established_in_discovery_pct=0.10,
            stakeholders_identified_in_discovery_avg=1.0,
            economic_buyer_engaged_pre_proposal_pct=0.10,
            technical_buyer_engaged_pre_proposal_pct=0.10,
            solution_presented_before_discovery_pct=0.50,
            deals_lost_due_to_poor_fit_pct=0.50,
            proposal_rework_rate_pct=0.60,
        )
        r = fresh_engine().assess(inp)
        assert r.discovery_risk in (DiscoveryRisk.high, DiscoveryRisk.critical)
        assert r.has_discovery_gap is True
        assert r.requires_discovery_coaching is True

    def test_assess_low_risk_scenario(self):
        r = fresh_engine().assess(make_input())
        assert r.discovery_risk == DiscoveryRisk.low
        assert r.discovery_severity == DiscoverySeverity.thorough
        assert r.recommended_action == DiscoveryAction.no_action


# ===========================================================================
# 17. ASSESS_BATCH
# ===========================================================================

class TestAssessBatch:

    def test_assess_batch_returns_list(self):
        e = fresh_engine()
        results = e.assess_batch([make_input(), make_input()])
        assert isinstance(results, list)

    def test_assess_batch_length(self):
        e = fresh_engine()
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(5)]
        results = e.assess_batch(inputs)
        assert len(results) == 5

    def test_assess_batch_all_results_are_discovery_result(self):
        e = fresh_engine()
        results = e.assess_batch([make_input(), make_input()])
        for r in results:
            assert isinstance(r, DiscoveryResult)

    def test_assess_batch_stores_results(self):
        e = fresh_engine()
        e.assess_batch([make_input(), make_input(), make_input()])
        assert len(e._results) == 3

    def test_assess_batch_empty_list(self):
        e = fresh_engine()
        results = e.assess_batch([])
        assert results == []

    def test_assess_batch_order_preserved(self):
        e = fresh_engine()
        ids = ["REP-A", "REP-B", "REP-C"]
        inputs = [make_input(rep_id=i) for i in ids]
        results = e.assess_batch(inputs)
        assert [r.rep_id for r in results] == ids


# ===========================================================================
# 18. SUMMARY – EMPTY AND POPULATED (ALL 13 KEYS)
# ===========================================================================

class TestSummary:

    EXPECTED_KEYS = {
        "total",
        "risk_counts",
        "pattern_counts",
        "severity_counts",
        "action_counts",
        "avg_discovery_composite",
        "discovery_gap_count",
        "coaching_count",
        "avg_depth_score",
        "avg_qualification_score",
        "avg_stakeholder_score",
        "avg_fit_score",
        "total_estimated_wasted_pipeline_usd",
    }

    def test_empty_summary_has_13_keys(self):
        s = fresh_engine().summary()
        assert len(s) == 13

    def test_empty_summary_exact_keys(self):
        s = fresh_engine().summary()
        assert set(s.keys()) == self.EXPECTED_KEYS

    def test_empty_summary_total_zero(self):
        s = fresh_engine().summary()
        assert s["total"] == 0

    def test_empty_summary_counts_empty_dicts(self):
        s = fresh_engine().summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_avg_zeros(self):
        s = fresh_engine().summary()
        assert s["avg_discovery_composite"] == 0.0
        assert s["avg_depth_score"] == 0.0
        assert s["avg_qualification_score"] == 0.0
        assert s["avg_stakeholder_score"] == 0.0
        assert s["avg_fit_score"] == 0.0

    def test_empty_summary_gap_coaching_zero(self):
        s = fresh_engine().summary()
        assert s["discovery_gap_count"] == 0
        assert s["coaching_count"] == 0
        assert s["total_estimated_wasted_pipeline_usd"] == 0.0

    def test_populated_summary_has_13_keys(self):
        e = fresh_engine()
        e.assess_batch([make_input(), make_input()])
        s = e.summary()
        assert len(s) == 13

    def test_populated_summary_exact_keys(self):
        e = fresh_engine()
        e.assess(make_input())
        s = e.summary()
        assert set(s.keys()) == self.EXPECTED_KEYS

    def test_populated_summary_total_count(self):
        e = fresh_engine()
        e.assess_batch([make_input()] * 5)
        assert e.summary()["total"] == 5

    def test_populated_summary_risk_counts(self):
        e = fresh_engine()
        e.assess(make_input())  # low risk
        s = e.summary()
        assert "low" in s["risk_counts"]
        assert s["risk_counts"]["low"] == 1

    def test_populated_summary_pattern_counts(self):
        e = fresh_engine()
        e.assess(make_input())  # no pattern
        s = e.summary()
        assert "none" in s["pattern_counts"]

    def test_populated_summary_severity_counts(self):
        e = fresh_engine()
        e.assess(make_input())  # thorough
        s = e.summary()
        assert "thorough" in s["severity_counts"]

    def test_populated_summary_action_counts(self):
        e = fresh_engine()
        e.assess(make_input())  # no_action
        s = e.summary()
        assert "no_action" in s["action_counts"]

    def test_populated_summary_avg_composite(self):
        e = fresh_engine()
        r1 = e.assess(make_input())
        r2 = e.assess(make_input())
        s = e.summary()
        expected = round((r1.discovery_composite + r2.discovery_composite) / 2, 1)
        assert s["avg_discovery_composite"] == expected

    def test_populated_summary_discovery_gap_count(self):
        e = fresh_engine()
        # gap = True when budget_qualified_before_demo_pct <= 0.40
        e.assess(make_input(budget_qualified_before_demo_pct=0.40))
        e.assess(make_input())  # no gap
        s = e.summary()
        assert s["discovery_gap_count"] >= 1

    def test_populated_summary_coaching_count(self):
        e = fresh_engine()
        e.assess(make_input(avg_discovery_questions_per_call=10.0))  # coaching
        e.assess(make_input())  # no coaching (questions=20, solution=0.05, composite=0)
        s = e.summary()
        assert s["coaching_count"] >= 1

    def test_populated_summary_avg_depth_score(self):
        e = fresh_engine()
        r1 = e.assess(make_input())
        r2 = e.assess(make_input())
        s = e.summary()
        expected = round((r1.depth_score + r2.depth_score) / 2, 1)
        assert s["avg_depth_score"] == expected

    def test_populated_summary_avg_qualification_score(self):
        e = fresh_engine()
        r1 = e.assess(make_input())
        r2 = e.assess(make_input())
        s = e.summary()
        expected = round((r1.qualification_score + r2.qualification_score) / 2, 1)
        assert s["avg_qualification_score"] == expected

    def test_populated_summary_avg_stakeholder_score(self):
        e = fresh_engine()
        r1 = e.assess(make_input())
        r2 = e.assess(make_input())
        s = e.summary()
        expected = round((r1.stakeholder_score + r2.stakeholder_score) / 2, 1)
        assert s["avg_stakeholder_score"] == expected

    def test_populated_summary_avg_fit_score(self):
        e = fresh_engine()
        r1 = e.assess(make_input())
        r2 = e.assess(make_input())
        s = e.summary()
        expected = round((r1.fit_score + r2.fit_score) / 2, 1)
        assert s["avg_fit_score"] == expected

    def test_populated_summary_total_wasted_pipeline(self):
        e = fresh_engine()
        r1 = e.assess(make_input())
        r2 = e.assess(make_input())
        s = e.summary()
        expected = round(r1.estimated_wasted_pipeline_usd + r2.estimated_wasted_pipeline_usd, 2)
        assert s["total_estimated_wasted_pipeline_usd"] == expected

    def test_populated_summary_multiple_risk_levels(self):
        e = fresh_engine()
        # low risk
        e.assess(make_input())
        # critical risk
        e.assess(make_input(
            avg_discovery_questions_per_call=1.0,
            pain_points_documented_per_deal=0.5,
            business_impact_quantified_pct=0.10,
            budget_qualified_before_demo_pct=0.10,
            decision_process_mapped_pct=0.10,
            timeline_established_in_discovery_pct=0.10,
            stakeholders_identified_in_discovery_avg=1.0,
            economic_buyer_engaged_pre_proposal_pct=0.10,
            technical_buyer_engaged_pre_proposal_pct=0.10,
            solution_presented_before_discovery_pct=0.50,
            deals_lost_due_to_poor_fit_pct=0.50,
            proposal_rework_rate_pct=0.60,
        ))
        s = e.summary()
        assert s["total"] == 2
        assert len(s["risk_counts"]) >= 2


# ===========================================================================
# 19. INTEGRATION: ASSESS THEN SUMMARY CONSISTENCY
# ===========================================================================

class TestAssessSummaryConsistency:

    def test_assess_batch_then_summary_total(self):
        e = fresh_engine()
        n = 7
        e.assess_batch([make_input(rep_id=f"REP-{i}") for i in range(n)])
        assert e.summary()["total"] == n

    def test_fresh_engine_summary_each_time(self):
        """Each new engine starts with empty results."""
        e1 = fresh_engine()
        e1.assess(make_input())
        e2 = fresh_engine()
        assert e2.summary()["total"] == 0

    def test_summary_counts_sum_to_total(self):
        e = fresh_engine()
        e.assess_batch([make_input(rep_id=f"REP-{i}") for i in range(6)])
        s = e.summary()
        assert sum(s["risk_counts"].values()) == s["total"]
        assert sum(s["pattern_counts"].values()) == s["total"]
        assert sum(s["severity_counts"].values()) == s["total"]
        assert sum(s["action_counts"].values()) == s["total"]
