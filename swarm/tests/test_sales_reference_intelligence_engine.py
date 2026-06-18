"""
Comprehensive pytest test suite for SalesReferenceIntelligenceEngine.
Covers: enums, dataclasses, sub-score methods, pattern detection,
risk/severity/action mapping, flag methods, win-rate impact, signal
generation, assess(), assess_batch(), summary(), edge cases, and
end-to-end scenarios.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_reference_intelligence_engine import (
    ReferenceAction,
    ReferenceInput,
    ReferencePattern,
    ReferenceResult,
    ReferenceRisk,
    ReferenceSeverity,
    SalesReferenceIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> ReferenceInput:
    """Return a low-risk, healthy baseline ReferenceInput with optional overrides."""
    defaults = dict(
        rep_id="REP-001",
        region="EMEA",
        evaluation_period_id="2024-Q1",
        total_deals_active=20,
        deals_with_reference_deployed_pct=0.80,
        avg_references_per_deal=2.5,
        unique_references_used_count=8,
        reference_call_conversion_lift_pct=0.10,
        avg_days_to_first_reference=10.0,
        late_stage_reference_rate_pct=0.20,
        deals_with_no_evidence_pct=0.10,
        case_study_deployment_rate_pct=0.70,
        roi_document_shared_pct=0.70,
        testimonial_used_pct=0.60,
        peer_review_site_share_rate_pct=0.50,
        reference_repeat_use_count=1,
        reference_burnout_signals_count=0,
        analyst_report_leveraged_pct=0.50,
        competitive_displacement_story_used_pct=0.50,
        win_stories_shared_in_pipeline_pct=0.50,
        avg_evidence_assets_per_deal=3.0,
        avg_opportunity_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return ReferenceInput(**defaults)


def make_engine() -> SalesReferenceIntelligenceEngine:
    return SalesReferenceIntelligenceEngine()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestReferenceRiskEnum:
    def test_values(self):
        assert ReferenceRisk.low.value == "low"
        assert ReferenceRisk.moderate.value == "moderate"
        assert ReferenceRisk.high.value == "high"
        assert ReferenceRisk.critical.value == "critical"

    def test_members(self):
        members = [m.value for m in ReferenceRisk]
        assert set(members) == {"low", "moderate", "high", "critical"}

    def test_str_enum_behavior(self):
        assert ReferenceRisk.low == "low"
        assert ReferenceRisk.critical == "critical"

    def test_is_str_subclass(self):
        assert isinstance(ReferenceRisk.low, str)

    def test_count(self):
        assert len(ReferenceRisk) == 4


class TestReferencePatternEnum:
    def test_none_value(self):
        assert ReferencePattern.none.value == "none"

    def test_reference_avoidance_value(self):
        assert ReferencePattern.reference_avoidance.value == "reference_avoidance"

    def test_reference_fatigue_value(self):
        assert ReferencePattern.reference_fatigue.value == "reference_fatigue"

    def test_single_reference_overuse_value(self):
        assert ReferencePattern.single_reference_overuse.value == "single_reference_overuse"

    def test_no_case_study_usage_value(self):
        assert ReferencePattern.no_case_study_usage.value == "no_case_study_usage"

    def test_late_stage_evidence_gap_value(self):
        assert ReferencePattern.late_stage_evidence_gap.value == "late_stage_evidence_gap"

    def test_count(self):
        assert len(ReferencePattern) == 6

    def test_str_enum_behavior(self):
        assert ReferencePattern.none == "none"

    def test_is_str_subclass(self):
        assert isinstance(ReferencePattern.reference_avoidance, str)


class TestReferenceSeverityEnum:
    def test_evidence_led_value(self):
        assert ReferenceSeverity.evidence_led.value == "evidence_led"

    def test_developing_value(self):
        assert ReferenceSeverity.developing.value == "developing"

    def test_anecdotal_value(self):
        assert ReferenceSeverity.anecdotal.value == "anecdotal"

    def test_blind_value(self):
        assert ReferenceSeverity.blind.value == "blind"

    def test_count(self):
        assert len(ReferenceSeverity) == 4

    def test_str_enum_behavior(self):
        assert ReferenceSeverity.blind == "blind"

    def test_is_str_subclass(self):
        assert isinstance(ReferenceSeverity.developing, str)


class TestReferenceActionEnum:
    def test_no_action_value(self):
        assert ReferenceAction.no_action.value == "no_action"

    def test_reference_program_onboarding_value(self):
        assert ReferenceAction.reference_program_onboarding.value == "reference_program_onboarding"

    def test_evidence_library_training_value(self):
        assert ReferenceAction.evidence_library_training.value == "evidence_library_training"

    def test_reference_rotation_coaching_value(self):
        assert ReferenceAction.reference_rotation_coaching.value == "reference_rotation_coaching"

    def test_case_study_deployment_plan_value(self):
        assert ReferenceAction.case_study_deployment_plan.value == "case_study_deployment_plan"

    def test_late_stage_evidence_sprint_value(self):
        assert ReferenceAction.late_stage_evidence_sprint.value == "late_stage_evidence_sprint"

    def test_count(self):
        assert len(ReferenceAction) == 6

    def test_str_enum_behavior(self):
        assert ReferenceAction.no_action == "no_action"

    def test_is_str_subclass(self):
        assert isinstance(ReferenceAction.late_stage_evidence_sprint, str)


# ===========================================================================
# 2. REFERENCEINPUT DATACLASS TESTS
# ===========================================================================

class TestReferenceInput:
    def test_all_22_fields_present(self):
        inp = make_input()
        assert hasattr(inp, "rep_id")
        assert hasattr(inp, "region")
        assert hasattr(inp, "evaluation_period_id")
        assert hasattr(inp, "total_deals_active")
        assert hasattr(inp, "deals_with_reference_deployed_pct")
        assert hasattr(inp, "avg_references_per_deal")
        assert hasattr(inp, "unique_references_used_count")
        assert hasattr(inp, "reference_call_conversion_lift_pct")
        assert hasattr(inp, "avg_days_to_first_reference")
        assert hasattr(inp, "late_stage_reference_rate_pct")
        assert hasattr(inp, "deals_with_no_evidence_pct")
        assert hasattr(inp, "case_study_deployment_rate_pct")
        assert hasattr(inp, "roi_document_shared_pct")
        assert hasattr(inp, "testimonial_used_pct")
        assert hasattr(inp, "peer_review_site_share_rate_pct")
        assert hasattr(inp, "reference_repeat_use_count")
        assert hasattr(inp, "reference_burnout_signals_count")
        assert hasattr(inp, "analyst_report_leveraged_pct")
        assert hasattr(inp, "competitive_displacement_story_used_pct")
        assert hasattr(inp, "win_stories_shared_in_pipeline_pct")
        assert hasattr(inp, "avg_evidence_assets_per_deal")
        assert hasattr(inp, "avg_opportunity_value_usd")

    def test_rep_id_stored(self):
        inp = make_input(rep_id="X99")
        assert inp.rep_id == "X99"

    def test_region_stored(self):
        inp = make_input(region="APAC")
        assert inp.region == "APAC"

    def test_evaluation_period_id_stored(self):
        inp = make_input(evaluation_period_id="2024-Q4")
        assert inp.evaluation_period_id == "2024-Q4"

    def test_total_deals_active_stored(self):
        inp = make_input(total_deals_active=100)
        assert inp.total_deals_active == 100

    def test_deals_with_reference_deployed_pct_stored(self):
        inp = make_input(deals_with_reference_deployed_pct=0.55)
        assert inp.deals_with_reference_deployed_pct == pytest.approx(0.55)

    def test_avg_references_per_deal_stored(self):
        inp = make_input(avg_references_per_deal=1.5)
        assert inp.avg_references_per_deal == pytest.approx(1.5)

    def test_unique_references_used_count_stored(self):
        inp = make_input(unique_references_used_count=4)
        assert inp.unique_references_used_count == 4

    def test_reference_call_conversion_lift_pct_stored(self):
        inp = make_input(reference_call_conversion_lift_pct=0.25)
        assert inp.reference_call_conversion_lift_pct == pytest.approx(0.25)

    def test_avg_days_to_first_reference_stored(self):
        inp = make_input(avg_days_to_first_reference=45.0)
        assert inp.avg_days_to_first_reference == pytest.approx(45.0)

    def test_late_stage_reference_rate_pct_stored(self):
        inp = make_input(late_stage_reference_rate_pct=0.65)
        assert inp.late_stage_reference_rate_pct == pytest.approx(0.65)

    def test_deals_with_no_evidence_pct_stored(self):
        inp = make_input(deals_with_no_evidence_pct=0.30)
        assert inp.deals_with_no_evidence_pct == pytest.approx(0.30)

    def test_case_study_deployment_rate_pct_stored(self):
        inp = make_input(case_study_deployment_rate_pct=0.40)
        assert inp.case_study_deployment_rate_pct == pytest.approx(0.40)

    def test_roi_document_shared_pct_stored(self):
        inp = make_input(roi_document_shared_pct=0.10)
        assert inp.roi_document_shared_pct == pytest.approx(0.10)

    def test_testimonial_used_pct_stored(self):
        inp = make_input(testimonial_used_pct=0.75)
        assert inp.testimonial_used_pct == pytest.approx(0.75)

    def test_peer_review_site_share_rate_pct_stored(self):
        inp = make_input(peer_review_site_share_rate_pct=0.33)
        assert inp.peer_review_site_share_rate_pct == pytest.approx(0.33)

    def test_reference_repeat_use_count_stored(self):
        inp = make_input(reference_repeat_use_count=7)
        assert inp.reference_repeat_use_count == 7

    def test_reference_burnout_signals_count_stored(self):
        inp = make_input(reference_burnout_signals_count=3)
        assert inp.reference_burnout_signals_count == 3

    def test_analyst_report_leveraged_pct_stored(self):
        inp = make_input(analyst_report_leveraged_pct=0.20)
        assert inp.analyst_report_leveraged_pct == pytest.approx(0.20)

    def test_competitive_displacement_story_used_pct_stored(self):
        inp = make_input(competitive_displacement_story_used_pct=0.12)
        assert inp.competitive_displacement_story_used_pct == pytest.approx(0.12)

    def test_win_stories_shared_in_pipeline_pct_stored(self):
        inp = make_input(win_stories_shared_in_pipeline_pct=0.90)
        assert inp.win_stories_shared_in_pipeline_pct == pytest.approx(0.90)

    def test_avg_evidence_assets_per_deal_stored(self):
        inp = make_input(avg_evidence_assets_per_deal=1.5)
        assert inp.avg_evidence_assets_per_deal == pytest.approx(1.5)

    def test_avg_opportunity_value_usd_stored(self):
        inp = make_input(avg_opportunity_value_usd=100_000.0)
        assert inp.avg_opportunity_value_usd == pytest.approx(100_000.0)


# ===========================================================================
# 3. REFERENCERESULT DATACLASS TESTS
# ===========================================================================

class TestReferenceResult:
    def _make_result(self):
        return ReferenceResult(
            rep_id="R1",
            region="NA",
            reference_risk=ReferenceRisk.low,
            reference_pattern=ReferencePattern.none,
            reference_severity=ReferenceSeverity.evidence_led,
            recommended_action=ReferenceAction.no_action,
            reference_utilization_score=5.0,
            evidence_diversity_score=5.0,
            reference_timing_score=5.0,
            evidence_depth_score=5.0,
            reference_composite=5.0,
            has_reference_gap=False,
            requires_reference_coaching=False,
            estimated_win_rate_impact_usd=0.0,
            reference_signal="healthy",
        )

    def test_all_15_fields_present(self):
        r = self._make_result()
        assert hasattr(r, "rep_id")
        assert hasattr(r, "region")
        assert hasattr(r, "reference_risk")
        assert hasattr(r, "reference_pattern")
        assert hasattr(r, "reference_severity")
        assert hasattr(r, "recommended_action")
        assert hasattr(r, "reference_utilization_score")
        assert hasattr(r, "evidence_diversity_score")
        assert hasattr(r, "reference_timing_score")
        assert hasattr(r, "evidence_depth_score")
        assert hasattr(r, "reference_composite")
        assert hasattr(r, "has_reference_gap")
        assert hasattr(r, "requires_reference_coaching")
        assert hasattr(r, "estimated_win_rate_impact_usd")
        assert hasattr(r, "reference_signal")

    def test_to_dict_returns_dict(self):
        r = self._make_result()
        assert isinstance(r.to_dict(), dict)

    def test_to_dict_has_15_keys(self):
        r = self._make_result()
        assert len(r.to_dict()) == 15

    def test_to_dict_expected_keys(self):
        r = self._make_result()
        d = r.to_dict()
        expected_keys = {
            "rep_id", "region", "reference_risk", "reference_pattern",
            "reference_severity", "recommended_action",
            "reference_utilization_score", "evidence_diversity_score",
            "reference_timing_score", "evidence_depth_score",
            "reference_composite", "has_reference_gap",
            "requires_reference_coaching", "estimated_win_rate_impact_usd",
            "reference_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        r = self._make_result()
        d = r.to_dict()
        assert d["reference_risk"] == "low"
        assert d["reference_pattern"] == "none"
        assert d["reference_severity"] == "evidence_led"
        assert d["recommended_action"] == "no_action"

    def test_to_dict_rep_id(self):
        r = self._make_result()
        assert r.to_dict()["rep_id"] == "R1"

    def test_to_dict_region(self):
        r = self._make_result()
        assert r.to_dict()["region"] == "NA"

    def test_to_dict_scores_present(self):
        r = self._make_result()
        d = r.to_dict()
        assert d["reference_utilization_score"] == pytest.approx(5.0)
        assert d["evidence_diversity_score"] == pytest.approx(5.0)
        assert d["reference_timing_score"] == pytest.approx(5.0)
        assert d["evidence_depth_score"] == pytest.approx(5.0)
        assert d["reference_composite"] == pytest.approx(5.0)

    def test_to_dict_flags(self):
        r = self._make_result()
        d = r.to_dict()
        assert d["has_reference_gap"] is False
        assert d["requires_reference_coaching"] is False

    def test_to_dict_impact(self):
        r = self._make_result()
        assert r.to_dict()["estimated_win_rate_impact_usd"] == pytest.approx(0.0)

    def test_to_dict_signal(self):
        r = self._make_result()
        assert r.to_dict()["reference_signal"] == "healthy"


# ===========================================================================
# 4. SUB-SCORE: _reference_utilization_score
# ===========================================================================

class TestReferenceUtilizationScore:
    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kw) -> float:
        return self.engine._reference_utilization_score(make_input(**kw))

    # deals_with_reference_deployed_pct branches
    def test_deployed_pct_le_020_adds_40(self):
        s = self._score(
            deals_with_reference_deployed_pct=0.10,
            avg_references_per_deal=2.0,
            deals_with_no_evidence_pct=0.05,
        )
        assert s >= 40.0

    def test_deployed_pct_exactly_020_adds_40(self):
        s = self._score(
            deals_with_reference_deployed_pct=0.20,
            avg_references_per_deal=2.0,
            deals_with_no_evidence_pct=0.05,
        )
        assert s >= 40.0

    def test_deployed_pct_021_no_40_bonus(self):
        s_low = self._score(
            deals_with_reference_deployed_pct=0.20,
            avg_references_per_deal=2.0,
            deals_with_no_evidence_pct=0.05,
        )
        s_high = self._score(
            deals_with_reference_deployed_pct=0.21,
            avg_references_per_deal=2.0,
            deals_with_no_evidence_pct=0.05,
        )
        assert s_high < s_low

    def test_deployed_pct_le_050_adds_22(self):
        s = self._score(
            deals_with_reference_deployed_pct=0.40,
            avg_references_per_deal=2.0,
            deals_with_no_evidence_pct=0.05,
        )
        # Should add 22, not 40
        assert 20.0 <= s <= 30.0

    def test_deployed_pct_le_070_adds_8(self):
        s = self._score(
            deals_with_reference_deployed_pct=0.60,
            avg_references_per_deal=2.0,
            deals_with_no_evidence_pct=0.05,
        )
        assert 6.0 <= s <= 14.0

    def test_deployed_pct_above_070_adds_0(self):
        s = self._score(
            deals_with_reference_deployed_pct=0.80,
            avg_references_per_deal=2.0,
            deals_with_no_evidence_pct=0.05,
        )
        assert s == 0.0

    # avg_references_per_deal branches
    def test_avg_refs_le_05_adds_35(self):
        s = self._score(
            deals_with_reference_deployed_pct=0.80,
            avg_references_per_deal=0.5,
            deals_with_no_evidence_pct=0.05,
        )
        assert s >= 35.0

    def test_avg_refs_le_10_adds_18(self):
        s = self._score(
            deals_with_reference_deployed_pct=0.80,
            avg_references_per_deal=0.8,
            deals_with_no_evidence_pct=0.05,
        )
        assert s >= 18.0

    def test_avg_refs_above_10_adds_0(self):
        s = self._score(
            deals_with_reference_deployed_pct=0.80,
            avg_references_per_deal=1.5,
            deals_with_no_evidence_pct=0.05,
        )
        assert s == 0.0

    # deals_with_no_evidence_pct branches
    def test_no_evidence_ge_050_adds_25(self):
        s = self._score(
            deals_with_reference_deployed_pct=0.80,
            avg_references_per_deal=2.0,
            deals_with_no_evidence_pct=0.60,
        )
        assert s >= 25.0

    def test_no_evidence_ge_025_adds_12(self):
        s = self._score(
            deals_with_reference_deployed_pct=0.80,
            avg_references_per_deal=2.0,
            deals_with_no_evidence_pct=0.30,
        )
        assert s >= 12.0

    def test_no_evidence_below_025_adds_0(self):
        s = self._score(
            deals_with_reference_deployed_pct=0.80,
            avg_references_per_deal=2.0,
            deals_with_no_evidence_pct=0.10,
        )
        assert s == 0.0

    def test_capped_at_100(self):
        # Worst case: everything maximally bad
        s = self._score(
            deals_with_reference_deployed_pct=0.0,
            avg_references_per_deal=0.0,
            deals_with_no_evidence_pct=1.0,
        )
        assert s == 100.0

    def test_zero_score_healthy_input(self):
        s = self._score(
            deals_with_reference_deployed_pct=0.90,
            avg_references_per_deal=3.0,
            deals_with_no_evidence_pct=0.05,
        )
        assert s == 0.0

    def test_boundary_050(self):
        s = self._score(
            deals_with_reference_deployed_pct=0.50,
            avg_references_per_deal=2.0,
            deals_with_no_evidence_pct=0.05,
        )
        assert s >= 22.0

    def test_boundary_070(self):
        s = self._score(
            deals_with_reference_deployed_pct=0.70,
            avg_references_per_deal=2.0,
            deals_with_no_evidence_pct=0.05,
        )
        assert s >= 8.0


# ===========================================================================
# 5. SUB-SCORE: _evidence_diversity_score
# ===========================================================================

class TestEvidenceDiversityScore:
    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kw) -> float:
        return self.engine._evidence_diversity_score(make_input(**kw))

    # unique_references_used_count branches
    def test_unique_refs_le_1_adds_40(self):
        s = self._score(
            unique_references_used_count=1,
            case_study_deployment_rate_pct=0.70,
            avg_evidence_assets_per_deal=3.0,
        )
        assert s >= 40.0

    def test_unique_refs_le_3_adds_22(self):
        s = self._score(
            unique_references_used_count=3,
            case_study_deployment_rate_pct=0.70,
            avg_evidence_assets_per_deal=3.0,
        )
        assert s >= 22.0

    def test_unique_refs_le_5_adds_8(self):
        s = self._score(
            unique_references_used_count=5,
            case_study_deployment_rate_pct=0.70,
            avg_evidence_assets_per_deal=3.0,
        )
        assert s >= 8.0

    def test_unique_refs_above_5_adds_0(self):
        s = self._score(
            unique_references_used_count=6,
            case_study_deployment_rate_pct=0.70,
            avg_evidence_assets_per_deal=3.0,
        )
        assert s == 0.0

    # case_study_deployment_rate_pct branches
    def test_case_study_le_020_adds_35(self):
        s = self._score(
            unique_references_used_count=6,
            case_study_deployment_rate_pct=0.10,
            avg_evidence_assets_per_deal=3.0,
        )
        assert s >= 35.0

    def test_case_study_le_050_adds_18(self):
        s = self._score(
            unique_references_used_count=6,
            case_study_deployment_rate_pct=0.40,
            avg_evidence_assets_per_deal=3.0,
        )
        assert s >= 18.0

    def test_case_study_above_050_adds_0(self):
        s = self._score(
            unique_references_used_count=6,
            case_study_deployment_rate_pct=0.60,
            avg_evidence_assets_per_deal=3.0,
        )
        assert s == 0.0

    # avg_evidence_assets_per_deal branches
    def test_assets_le_1_adds_25(self):
        s = self._score(
            unique_references_used_count=6,
            case_study_deployment_rate_pct=0.70,
            avg_evidence_assets_per_deal=1.0,
        )
        assert s >= 25.0

    def test_assets_le_2_adds_12(self):
        s = self._score(
            unique_references_used_count=6,
            case_study_deployment_rate_pct=0.70,
            avg_evidence_assets_per_deal=1.5,
        )
        assert s >= 12.0

    def test_assets_above_2_adds_0(self):
        s = self._score(
            unique_references_used_count=6,
            case_study_deployment_rate_pct=0.70,
            avg_evidence_assets_per_deal=2.5,
        )
        assert s == 0.0

    def test_capped_at_100(self):
        s = self._score(
            unique_references_used_count=0,
            case_study_deployment_rate_pct=0.0,
            avg_evidence_assets_per_deal=0.0,
        )
        assert s == 100.0

    def test_zero_score_healthy(self):
        s = self._score(
            unique_references_used_count=10,
            case_study_deployment_rate_pct=0.80,
            avg_evidence_assets_per_deal=4.0,
        )
        assert s == 0.0

    def test_boundary_unique_refs_2(self):
        s = self._score(
            unique_references_used_count=2,
            case_study_deployment_rate_pct=0.70,
            avg_evidence_assets_per_deal=3.0,
        )
        assert s >= 22.0

    def test_boundary_case_study_020(self):
        s = self._score(
            unique_references_used_count=6,
            case_study_deployment_rate_pct=0.20,
            avg_evidence_assets_per_deal=3.0,
        )
        assert s >= 35.0


# ===========================================================================
# 6. SUB-SCORE: _reference_timing_score
# ===========================================================================

class TestReferenceTimingScore:
    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kw) -> float:
        return self.engine._reference_timing_score(make_input(**kw))

    # avg_days_to_first_reference branches
    def test_days_ge_60_adds_40(self):
        s = self._score(
            avg_days_to_first_reference=60.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=0,
        )
        assert s >= 40.0

    def test_days_ge_30_adds_22(self):
        s = self._score(
            avg_days_to_first_reference=45.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=0,
        )
        assert s >= 22.0

    def test_days_ge_14_adds_8(self):
        s = self._score(
            avg_days_to_first_reference=20.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=0,
        )
        assert s >= 8.0

    def test_days_below_14_adds_0(self):
        s = self._score(
            avg_days_to_first_reference=10.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=0,
        )
        assert s == 0.0

    # late_stage_reference_rate_pct branches
    def test_late_stage_ge_060_adds_35(self):
        s = self._score(
            avg_days_to_first_reference=5.0,
            late_stage_reference_rate_pct=0.70,
            reference_repeat_use_count=0,
        )
        assert s >= 35.0

    def test_late_stage_ge_040_adds_18(self):
        s = self._score(
            avg_days_to_first_reference=5.0,
            late_stage_reference_rate_pct=0.50,
            reference_repeat_use_count=0,
        )
        assert s >= 18.0

    def test_late_stage_below_040_adds_0(self):
        s = self._score(
            avg_days_to_first_reference=5.0,
            late_stage_reference_rate_pct=0.20,
            reference_repeat_use_count=0,
        )
        assert s == 0.0

    # reference_repeat_use_count branches
    def test_repeat_ge_6_adds_25(self):
        s = self._score(
            avg_days_to_first_reference=5.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=6,
        )
        assert s >= 25.0

    def test_repeat_ge_3_adds_12(self):
        s = self._score(
            avg_days_to_first_reference=5.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=4,
        )
        assert s >= 12.0

    def test_repeat_below_3_adds_0(self):
        s = self._score(
            avg_days_to_first_reference=5.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=2,
        )
        assert s == 0.0

    def test_capped_at_100(self):
        s = self._score(
            avg_days_to_first_reference=90.0,
            late_stage_reference_rate_pct=1.0,
            reference_repeat_use_count=10,
        )
        assert s == 100.0

    def test_zero_score_healthy(self):
        s = self._score(
            avg_days_to_first_reference=5.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=0,
        )
        assert s == 0.0

    def test_boundary_exactly_30_days(self):
        s = self._score(
            avg_days_to_first_reference=30.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=0,
        )
        assert s >= 22.0

    def test_boundary_exactly_14_days(self):
        s = self._score(
            avg_days_to_first_reference=14.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=0,
        )
        assert s >= 8.0

    def test_boundary_repeat_exactly_3(self):
        s = self._score(
            avg_days_to_first_reference=5.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=3,
        )
        assert s >= 12.0

    def test_boundary_repeat_exactly_6(self):
        s = self._score(
            avg_days_to_first_reference=5.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=6,
        )
        assert s >= 25.0


# ===========================================================================
# 7. SUB-SCORE: _evidence_depth_score
# ===========================================================================

class TestEvidenceDepthScore:
    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kw) -> float:
        return self.engine._evidence_depth_score(make_input(**kw))

    # roi_document_shared_pct branches
    def test_roi_le_015_adds_45(self):
        s = self._score(
            roi_document_shared_pct=0.10,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.50,
        )
        assert s >= 45.0

    def test_roi_le_040_adds_25(self):
        s = self._score(
            roi_document_shared_pct=0.30,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.50,
        )
        assert s >= 25.0

    def test_roi_le_065_adds_10(self):
        s = self._score(
            roi_document_shared_pct=0.50,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.50,
        )
        assert s >= 10.0

    def test_roi_above_065_adds_0(self):
        s = self._score(
            roi_document_shared_pct=0.70,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.50,
        )
        assert s == 0.0

    # analyst_report_leveraged_pct branches
    def test_analyst_le_010_adds_30(self):
        s = self._score(
            roi_document_shared_pct=0.70,
            analyst_report_leveraged_pct=0.05,
            competitive_displacement_story_used_pct=0.50,
        )
        assert s >= 30.0

    def test_analyst_le_030_adds_15(self):
        s = self._score(
            roi_document_shared_pct=0.70,
            analyst_report_leveraged_pct=0.20,
            competitive_displacement_story_used_pct=0.50,
        )
        assert s >= 15.0

    def test_analyst_above_030_adds_0(self):
        s = self._score(
            roi_document_shared_pct=0.70,
            analyst_report_leveraged_pct=0.40,
            competitive_displacement_story_used_pct=0.50,
        )
        assert s == 0.0

    # competitive_displacement_story_used_pct branches
    def test_competitive_le_015_adds_25(self):
        s = self._score(
            roi_document_shared_pct=0.70,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.10,
        )
        assert s >= 25.0

    def test_competitive_le_035_adds_12(self):
        s = self._score(
            roi_document_shared_pct=0.70,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.25,
        )
        assert s >= 12.0

    def test_competitive_above_035_adds_0(self):
        s = self._score(
            roi_document_shared_pct=0.70,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.40,
        )
        assert s == 0.0

    def test_zero_score_healthy(self):
        s = self._score(
            roi_document_shared_pct=0.80,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.50,
        )
        assert s == 0.0

    def test_capped_at_100(self):
        s = self._score(
            roi_document_shared_pct=0.0,
            analyst_report_leveraged_pct=0.0,
            competitive_displacement_story_used_pct=0.0,
        )
        assert s == 100.0

    def test_boundary_roi_exactly_015(self):
        s = self._score(
            roi_document_shared_pct=0.15,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.50,
        )
        assert s >= 45.0

    def test_boundary_roi_exactly_040(self):
        s = self._score(
            roi_document_shared_pct=0.40,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.50,
        )
        assert s >= 25.0

    def test_boundary_roi_exactly_065(self):
        s = self._score(
            roi_document_shared_pct=0.65,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.50,
        )
        assert s >= 10.0

    def test_boundary_analyst_exactly_010(self):
        s = self._score(
            roi_document_shared_pct=0.70,
            analyst_report_leveraged_pct=0.10,
            competitive_displacement_story_used_pct=0.50,
        )
        assert s >= 30.0

    def test_boundary_analyst_exactly_030(self):
        s = self._score(
            roi_document_shared_pct=0.70,
            analyst_report_leveraged_pct=0.30,
            competitive_displacement_story_used_pct=0.50,
        )
        assert s >= 15.0

    def test_boundary_competitive_exactly_015(self):
        s = self._score(
            roi_document_shared_pct=0.70,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.15,
        )
        assert s >= 25.0

    def test_boundary_competitive_exactly_035(self):
        s = self._score(
            roi_document_shared_pct=0.70,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.35,
        )
        assert s >= 12.0


# ===========================================================================
# 8. COMPOSITE SCORE FORMULA
# ===========================================================================

class TestCompositeFormula:
    def setup_method(self):
        self.engine = make_engine()

    def test_composite_formula_weights(self):
        """Composite = utilization*0.30 + diversity*0.30 + timing*0.25 + depth*0.15"""
        inp = make_input()
        result = self.engine.assess(inp)
        u = result.reference_utilization_score
        d = result.evidence_diversity_score
        t = result.reference_timing_score
        dp = result.evidence_depth_score
        expected = round(u * 0.30 + d * 0.30 + t * 0.25 + dp * 0.15, 1)
        assert result.reference_composite == pytest.approx(expected)

    def test_composite_capped_at_100(self):
        """All sub-scores at max → composite stays <=100."""
        inp = make_input(
            deals_with_reference_deployed_pct=0.0,
            avg_references_per_deal=0.0,
            deals_with_no_evidence_pct=1.0,
            unique_references_used_count=0,
            case_study_deployment_rate_pct=0.0,
            avg_evidence_assets_per_deal=0.0,
            avg_days_to_first_reference=90.0,
            late_stage_reference_rate_pct=1.0,
            reference_repeat_use_count=10,
            roi_document_shared_pct=0.0,
            analyst_report_leveraged_pct=0.0,
            competitive_displacement_story_used_pct=0.0,
        )
        result = self.engine.assess(inp)
        assert result.reference_composite <= 100.0

    def test_composite_non_negative(self):
        result = self.engine.assess(make_input())
        assert result.reference_composite >= 0.0


# ===========================================================================
# 9. PATTERN DETECTION
# ===========================================================================

class TestDetectPattern:
    def setup_method(self):
        self.engine = make_engine()

    def _pattern(self, **kw) -> ReferencePattern:
        inp = make_input(**kw)
        u = self.engine._reference_utilization_score(inp)
        d = self.engine._evidence_diversity_score(inp)
        t = self.engine._reference_timing_score(inp)
        dp = self.engine._evidence_depth_score(inp)
        return self.engine._detect_pattern(inp, u, d, t, dp)

    def test_reference_avoidance_detected(self):
        # utilization >= 40 (very low deployed pct adds 40+) and deployed pct <= 0.20
        p = self._pattern(
            deals_with_reference_deployed_pct=0.10,
            avg_references_per_deal=0.3,
            deals_with_no_evidence_pct=0.60,
        )
        assert p == ReferencePattern.reference_avoidance

    def test_reference_fatigue_detected(self):
        # timing >= 30 and repeat_use_count >= 4
        p = self._pattern(
            # Ensure utilization < 40 so avoidance not triggered first
            deals_with_reference_deployed_pct=0.80,
            avg_references_per_deal=3.0,
            deals_with_no_evidence_pct=0.05,
            # timing >= 30 — days >= 60 adds 40
            avg_days_to_first_reference=65.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=5,
        )
        assert p == ReferencePattern.reference_fatigue

    def test_single_reference_overuse_detected(self):
        # diversity >= 30, unique_refs <= 2
        # utilization must be < 40 to avoid avoidance
        # timing must be < 30 to avoid fatigue
        p = self._pattern(
            deals_with_reference_deployed_pct=0.80,
            avg_references_per_deal=3.0,
            deals_with_no_evidence_pct=0.05,
            avg_days_to_first_reference=5.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=0,
            unique_references_used_count=1,
            case_study_deployment_rate_pct=0.70,
            avg_evidence_assets_per_deal=3.0,
        )
        assert p == ReferencePattern.single_reference_overuse

    def test_no_case_study_usage_detected(self):
        # depth >= 30, case_study_deployment_rate_pct <= 0.20
        # Earlier conditions must not trigger
        p = self._pattern(
            deals_with_reference_deployed_pct=0.80,
            avg_references_per_deal=3.0,
            deals_with_no_evidence_pct=0.05,
            avg_days_to_first_reference=5.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=0,
            unique_references_used_count=8,
            case_study_deployment_rate_pct=0.10,
            avg_evidence_assets_per_deal=3.0,
            roi_document_shared_pct=0.0,
            analyst_report_leveraged_pct=0.0,
            competitive_displacement_story_used_pct=0.0,
        )
        assert p == ReferencePattern.no_case_study_usage

    def test_late_stage_evidence_gap_detected(self):
        # timing >= 20, late_stage_reference_rate_pct >= 0.50
        # Must not trigger avoidance, fatigue, single_overuse, or no_case_study
        p = self._pattern(
            deals_with_reference_deployed_pct=0.80,
            avg_references_per_deal=3.0,
            deals_with_no_evidence_pct=0.05,
            avg_days_to_first_reference=14.0,   # adds 8 to timing
            late_stage_reference_rate_pct=0.50,  # adds 18 → timing >= 26
            reference_repeat_use_count=2,        # adds 0 → total ~26
            unique_references_used_count=8,
            case_study_deployment_rate_pct=0.70,
            avg_evidence_assets_per_deal=3.0,
            roi_document_shared_pct=0.80,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.50,
        )
        assert p == ReferencePattern.late_stage_evidence_gap

    def test_none_pattern_healthy(self):
        p = self._pattern(
            deals_with_reference_deployed_pct=0.90,
            avg_references_per_deal=3.0,
            deals_with_no_evidence_pct=0.05,
            avg_days_to_first_reference=5.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=0,
            unique_references_used_count=10,
            case_study_deployment_rate_pct=0.80,
            avg_evidence_assets_per_deal=4.0,
            roi_document_shared_pct=0.80,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.50,
        )
        assert p == ReferencePattern.none

    def test_avoidance_takes_priority_over_fatigue(self):
        # Both avoidance and fatigue conditions met — avoidance checked first
        p = self._pattern(
            deals_with_reference_deployed_pct=0.10,  # avoidance trigger
            avg_references_per_deal=0.3,
            deals_with_no_evidence_pct=0.60,
            avg_days_to_first_reference=65.0,
            reference_repeat_use_count=6,            # fatigue trigger too
        )
        assert p == ReferencePattern.reference_avoidance


# ===========================================================================
# 10. RISK LEVEL
# ===========================================================================

class TestRiskLevel:
    def setup_method(self):
        self.engine = make_engine()

    def test_critical_at_60(self):
        assert self.engine._risk_level(60.0) == ReferenceRisk.critical

    def test_critical_above_60(self):
        assert self.engine._risk_level(90.0) == ReferenceRisk.critical

    def test_high_at_40(self):
        assert self.engine._risk_level(40.0) == ReferenceRisk.high

    def test_high_below_60(self):
        assert self.engine._risk_level(59.9) == ReferenceRisk.high

    def test_moderate_at_20(self):
        assert self.engine._risk_level(20.0) == ReferenceRisk.moderate

    def test_moderate_below_40(self):
        assert self.engine._risk_level(39.9) == ReferenceRisk.moderate

    def test_low_below_20(self):
        assert self.engine._risk_level(19.9) == ReferenceRisk.low

    def test_low_at_zero(self):
        assert self.engine._risk_level(0.0) == ReferenceRisk.low

    def test_boundary_exactly_60(self):
        assert self.engine._risk_level(60.0) == ReferenceRisk.critical

    def test_boundary_just_under_60(self):
        assert self.engine._risk_level(59.9) == ReferenceRisk.high

    def test_boundary_exactly_40(self):
        assert self.engine._risk_level(40.0) == ReferenceRisk.high

    def test_boundary_just_under_40(self):
        assert self.engine._risk_level(39.9) == ReferenceRisk.moderate

    def test_boundary_exactly_20(self):
        assert self.engine._risk_level(20.0) == ReferenceRisk.moderate

    def test_boundary_just_under_20(self):
        assert self.engine._risk_level(19.9) == ReferenceRisk.low


# ===========================================================================
# 11. SEVERITY
# ===========================================================================

class TestSeverity:
    def setup_method(self):
        self.engine = make_engine()

    def test_blind_at_60(self):
        assert self.engine._severity(60.0) == ReferenceSeverity.blind

    def test_blind_above_60(self):
        assert self.engine._severity(80.0) == ReferenceSeverity.blind

    def test_anecdotal_at_40(self):
        assert self.engine._severity(40.0) == ReferenceSeverity.anecdotal

    def test_anecdotal_below_60(self):
        assert self.engine._severity(59.9) == ReferenceSeverity.anecdotal

    def test_developing_at_20(self):
        assert self.engine._severity(20.0) == ReferenceSeverity.developing

    def test_developing_below_40(self):
        assert self.engine._severity(39.9) == ReferenceSeverity.developing

    def test_evidence_led_below_20(self):
        assert self.engine._severity(19.9) == ReferenceSeverity.evidence_led

    def test_evidence_led_at_zero(self):
        assert self.engine._severity(0.0) == ReferenceSeverity.evidence_led

    def test_boundary_exactly_60(self):
        assert self.engine._severity(60.0) == ReferenceSeverity.blind

    def test_boundary_just_under_60(self):
        assert self.engine._severity(59.9) == ReferenceSeverity.anecdotal

    def test_boundary_exactly_40(self):
        assert self.engine._severity(40.0) == ReferenceSeverity.anecdotal

    def test_boundary_just_under_40(self):
        assert self.engine._severity(39.9) == ReferenceSeverity.developing

    def test_boundary_exactly_20(self):
        assert self.engine._severity(20.0) == ReferenceSeverity.developing

    def test_boundary_just_under_20(self):
        assert self.engine._severity(19.9) == ReferenceSeverity.evidence_led


# ===========================================================================
# 12. ACTION MAPPING
# ===========================================================================

class TestAction:
    def setup_method(self):
        self.engine = make_engine()

    def _action(self, risk, pattern):
        return self.engine._action(risk, pattern)

    # Critical risk branch
    def test_critical_fatigue_returns_rotation_coaching(self):
        a = self._action(ReferenceRisk.critical, ReferencePattern.reference_fatigue)
        assert a == ReferenceAction.reference_rotation_coaching

    def test_critical_no_case_study_returns_case_study_plan(self):
        a = self._action(ReferenceRisk.critical, ReferencePattern.no_case_study_usage)
        assert a == ReferenceAction.case_study_deployment_plan

    def test_critical_avoidance_returns_onboarding(self):
        a = self._action(ReferenceRisk.critical, ReferencePattern.reference_avoidance)
        assert a == ReferenceAction.reference_program_onboarding

    def test_critical_none_returns_onboarding(self):
        a = self._action(ReferenceRisk.critical, ReferencePattern.none)
        assert a == ReferenceAction.reference_program_onboarding

    def test_critical_single_overuse_returns_onboarding(self):
        a = self._action(ReferenceRisk.critical, ReferencePattern.single_reference_overuse)
        assert a == ReferenceAction.reference_program_onboarding

    def test_critical_late_stage_returns_onboarding(self):
        a = self._action(ReferenceRisk.critical, ReferencePattern.late_stage_evidence_gap)
        assert a == ReferenceAction.reference_program_onboarding

    # High risk branch
    def test_high_late_stage_returns_sprint(self):
        a = self._action(ReferenceRisk.high, ReferencePattern.late_stage_evidence_gap)
        assert a == ReferenceAction.late_stage_evidence_sprint

    def test_high_single_overuse_returns_rotation_coaching(self):
        a = self._action(ReferenceRisk.high, ReferencePattern.single_reference_overuse)
        assert a == ReferenceAction.reference_rotation_coaching

    def test_high_none_returns_evidence_library_training(self):
        a = self._action(ReferenceRisk.high, ReferencePattern.none)
        assert a == ReferenceAction.evidence_library_training

    def test_high_avoidance_returns_evidence_library_training(self):
        a = self._action(ReferenceRisk.high, ReferencePattern.reference_avoidance)
        assert a == ReferenceAction.evidence_library_training

    def test_high_fatigue_returns_evidence_library_training(self):
        a = self._action(ReferenceRisk.high, ReferencePattern.reference_fatigue)
        assert a == ReferenceAction.evidence_library_training

    def test_high_no_case_study_returns_evidence_library_training(self):
        a = self._action(ReferenceRisk.high, ReferencePattern.no_case_study_usage)
        assert a == ReferenceAction.evidence_library_training

    # Moderate risk branch
    def test_moderate_any_pattern_returns_evidence_library_training(self):
        for pattern in ReferencePattern:
            a = self._action(ReferenceRisk.moderate, pattern)
            assert a == ReferenceAction.evidence_library_training

    # Low risk branch
    def test_low_any_pattern_returns_no_action(self):
        for pattern in ReferencePattern:
            a = self._action(ReferenceRisk.low, pattern)
            assert a == ReferenceAction.no_action


# ===========================================================================
# 13. FLAGS
# ===========================================================================

class TestFlags:
    def setup_method(self):
        self.engine = make_engine()

    # _has_reference_gap
    def test_gap_true_when_composite_ge_40(self):
        inp = make_input(deals_with_reference_deployed_pct=0.80, deals_with_no_evidence_pct=0.05)
        assert self.engine._has_reference_gap(40.0, inp) is True

    def test_gap_true_when_deployed_pct_le_020(self):
        inp = make_input(deals_with_reference_deployed_pct=0.15, deals_with_no_evidence_pct=0.05)
        assert self.engine._has_reference_gap(0.0, inp) is True

    def test_gap_true_when_no_evidence_ge_040(self):
        inp = make_input(deals_with_reference_deployed_pct=0.90, deals_with_no_evidence_pct=0.40)
        assert self.engine._has_reference_gap(0.0, inp) is True

    def test_gap_false_healthy(self):
        inp = make_input(deals_with_reference_deployed_pct=0.90, deals_with_no_evidence_pct=0.05)
        assert self.engine._has_reference_gap(10.0, inp) is False

    def test_gap_boundary_composite_exactly_40(self):
        inp = make_input(deals_with_reference_deployed_pct=0.90, deals_with_no_evidence_pct=0.05)
        assert self.engine._has_reference_gap(40.0, inp) is True

    def test_gap_boundary_deployed_exactly_020(self):
        inp = make_input(deals_with_reference_deployed_pct=0.20, deals_with_no_evidence_pct=0.05)
        assert self.engine._has_reference_gap(0.0, inp) is True

    def test_gap_boundary_no_evidence_exactly_040(self):
        inp = make_input(deals_with_reference_deployed_pct=0.90, deals_with_no_evidence_pct=0.40)
        assert self.engine._has_reference_gap(0.0, inp) is True

    def test_gap_false_composite_39(self):
        inp = make_input(deals_with_reference_deployed_pct=0.90, deals_with_no_evidence_pct=0.05)
        assert self.engine._has_reference_gap(39.0, inp) is False

    # _requires_reference_coaching
    def test_coaching_true_when_composite_ge_30(self):
        inp = make_input(case_study_deployment_rate_pct=0.80, unique_references_used_count=8)
        assert self.engine._requires_reference_coaching(30.0, inp) is True

    def test_coaching_true_when_case_study_le_025(self):
        inp = make_input(case_study_deployment_rate_pct=0.20, unique_references_used_count=8)
        assert self.engine._requires_reference_coaching(0.0, inp) is True

    def test_coaching_true_when_unique_refs_le_2(self):
        inp = make_input(case_study_deployment_rate_pct=0.80, unique_references_used_count=2)
        assert self.engine._requires_reference_coaching(0.0, inp) is True

    def test_coaching_false_healthy(self):
        inp = make_input(case_study_deployment_rate_pct=0.80, unique_references_used_count=8)
        assert self.engine._requires_reference_coaching(10.0, inp) is False

    def test_coaching_boundary_composite_exactly_30(self):
        inp = make_input(case_study_deployment_rate_pct=0.80, unique_references_used_count=8)
        assert self.engine._requires_reference_coaching(30.0, inp) is True

    def test_coaching_boundary_case_study_exactly_025(self):
        inp = make_input(case_study_deployment_rate_pct=0.25, unique_references_used_count=8)
        assert self.engine._requires_reference_coaching(0.0, inp) is True

    def test_coaching_boundary_unique_refs_exactly_2(self):
        inp = make_input(case_study_deployment_rate_pct=0.80, unique_references_used_count=2)
        assert self.engine._requires_reference_coaching(0.0, inp) is True

    def test_coaching_false_composite_29(self):
        inp = make_input(case_study_deployment_rate_pct=0.80, unique_references_used_count=8)
        assert self.engine._requires_reference_coaching(29.0, inp) is False


# ===========================================================================
# 14. WIN RATE IMPACT
# ===========================================================================

class TestWinRateImpact:
    def setup_method(self):
        self.engine = make_engine()

    def _impact(self, **kw) -> float:
        return self.engine._estimated_win_rate_impact(make_input(**kw), kw.pop("composite", 50.0))

    def test_basic_calculation(self):
        inp = make_input(
            total_deals_active=100,
            deals_with_no_evidence_pct=0.50,
            avg_opportunity_value_usd=10_000.0,
            reference_call_conversion_lift_pct=0.20,
        )
        composite = 80.0
        impact = self.engine._estimated_win_rate_impact(inp, composite)
        # evidence_free_deals = round(100 * 0.50) = 50
        # lift_gap = 0.20
        # result = 50 * 10000 * 0.20 * (80/100) = 80000.0
        assert impact == pytest.approx(80_000.0)

    def test_zero_when_no_evidence_free_deals(self):
        inp = make_input(
            total_deals_active=10,
            deals_with_no_evidence_pct=0.0,
            avg_opportunity_value_usd=10_000.0,
            reference_call_conversion_lift_pct=0.20,
        )
        assert self.engine._estimated_win_rate_impact(inp, 50.0) == 0.0

    def test_zero_when_lift_is_zero(self):
        inp = make_input(
            total_deals_active=10,
            deals_with_no_evidence_pct=0.50,
            avg_opportunity_value_usd=10_000.0,
            reference_call_conversion_lift_pct=0.0,
        )
        assert self.engine._estimated_win_rate_impact(inp, 50.0) == 0.0

    def test_zero_when_composite_zero(self):
        inp = make_input(
            total_deals_active=10,
            deals_with_no_evidence_pct=0.50,
            avg_opportunity_value_usd=10_000.0,
            reference_call_conversion_lift_pct=0.20,
        )
        assert self.engine._estimated_win_rate_impact(inp, 0.0) == 0.0

    def test_negative_lift_clamped_to_zero(self):
        inp = make_input(
            total_deals_active=10,
            deals_with_no_evidence_pct=0.50,
            avg_opportunity_value_usd=10_000.0,
            reference_call_conversion_lift_pct=-0.10,
        )
        assert self.engine._estimated_win_rate_impact(inp, 50.0) == 0.0

    def test_result_is_rounded_to_2dp(self):
        inp = make_input(
            total_deals_active=3,
            deals_with_no_evidence_pct=1.0 / 3.0,
            avg_opportunity_value_usd=10_000.0,
            reference_call_conversion_lift_pct=0.10,
        )
        impact = self.engine._estimated_win_rate_impact(inp, 33.0)
        # Check it has at most 2 decimal places
        assert impact == round(impact, 2)

    def test_impact_scales_with_composite(self):
        inp = make_input(
            total_deals_active=10,
            deals_with_no_evidence_pct=0.50,
            avg_opportunity_value_usd=10_000.0,
            reference_call_conversion_lift_pct=0.10,
        )
        impact_low = self.engine._estimated_win_rate_impact(inp, 20.0)
        impact_high = self.engine._estimated_win_rate_impact(inp, 80.0)
        assert impact_high > impact_low


# ===========================================================================
# 15. SIGNAL STRING
# ===========================================================================

class TestSignal:
    def setup_method(self):
        self.engine = make_engine()

    def test_healthy_signal_when_no_pattern_and_composite_below_20(self):
        inp = make_input()
        sig = self.engine._signal(inp, ReferencePattern.none, 10.0)
        assert sig == "Reference usage healthy — customer evidence, case studies, and ROI assets deployed within benchmarks"

    def test_unhealthy_signal_when_no_pattern_but_composite_ge_20(self):
        inp = make_input(
            deals_with_reference_deployed_pct=0.70,
            deals_with_no_evidence_pct=0.20,
        )
        sig = self.engine._signal(inp, ReferencePattern.none, 25.0)
        assert sig != "Reference usage healthy — customer evidence, case studies, and ROI assets deployed within benchmarks"
        assert "Reference gap" in sig

    def test_signal_includes_pattern_name_capitalized(self):
        inp = make_input(deals_with_reference_deployed_pct=0.30, deals_with_no_evidence_pct=0.30)
        sig = self.engine._signal(inp, ReferencePattern.reference_avoidance, 50.0)
        assert "Reference avoidance" in sig

    def test_signal_includes_composite(self):
        inp = make_input(deals_with_reference_deployed_pct=0.30, deals_with_no_evidence_pct=0.30)
        sig = self.engine._signal(inp, ReferencePattern.reference_avoidance, 55.0)
        assert "composite 55" in sig

    def test_signal_includes_deals_with_reference_pct(self):
        inp = make_input(deals_with_reference_deployed_pct=0.45, deals_with_no_evidence_pct=0.30)
        sig = self.engine._signal(inp, ReferencePattern.reference_avoidance, 55.0)
        assert "45% deals with reference" in sig

    def test_signal_includes_no_evidence_pct(self):
        inp = make_input(deals_with_reference_deployed_pct=0.45, deals_with_no_evidence_pct=0.30)
        sig = self.engine._signal(inp, ReferencePattern.reference_avoidance, 55.0)
        assert "30% deals without evidence" in sig

    def test_signal_includes_unique_refs_count(self):
        inp = make_input(unique_references_used_count=7)
        sig = self.engine._signal(inp, ReferencePattern.reference_fatigue, 50.0)
        assert "7 unique refs" in sig

    def test_signal_not_healthy_when_pattern_set(self):
        inp = make_input()
        sig = self.engine._signal(inp, ReferencePattern.reference_fatigue, 10.0)
        # pattern != none means NOT healthy signal
        assert "healthy" not in sig.lower() or "Reference fatigue" in sig

    def test_signal_late_stage_pattern_capitalized(self):
        inp = make_input(deals_with_reference_deployed_pct=0.30, deals_with_no_evidence_pct=0.20)
        sig = self.engine._signal(inp, ReferencePattern.late_stage_evidence_gap, 30.0)
        assert "Late stage evidence gap" in sig

    def test_signal_single_reference_overuse_capitalized(self):
        inp = make_input(deals_with_reference_deployed_pct=0.30, deals_with_no_evidence_pct=0.20)
        sig = self.engine._signal(inp, ReferencePattern.single_reference_overuse, 30.0)
        assert "Single reference overuse" in sig

    def test_signal_no_case_study_capitalized(self):
        inp = make_input(deals_with_reference_deployed_pct=0.30, deals_with_no_evidence_pct=0.20)
        sig = self.engine._signal(inp, ReferencePattern.no_case_study_usage, 30.0)
        assert "No case study usage" in sig


# ===========================================================================
# 16. ASSESS() — INTEGRATION
# ===========================================================================

class TestAssess:
    def setup_method(self):
        self.engine = make_engine()

    def test_returns_reference_result(self):
        r = self.engine.assess(make_input())
        assert isinstance(r, ReferenceResult)

    def test_rep_id_propagated(self):
        r = self.engine.assess(make_input(rep_id="ZREP"))
        assert r.rep_id == "ZREP"

    def test_region_propagated(self):
        r = self.engine.assess(make_input(region="LATAM"))
        assert r.region == "LATAM"

    def test_result_stored_in_internal_list(self):
        e = make_engine()
        r = e.assess(make_input())
        assert r in e._results

    def test_multiple_assess_accumulate_results(self):
        e = make_engine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B"))
        assert len(e._results) == 2

    def test_healthy_input_produces_low_risk(self):
        r = self.engine.assess(make_input())
        assert r.reference_risk == ReferenceRisk.low

    def test_healthy_input_produces_evidence_led(self):
        r = self.engine.assess(make_input())
        assert r.reference_severity == ReferenceSeverity.evidence_led

    def test_healthy_input_produces_no_action(self):
        r = self.engine.assess(make_input())
        assert r.recommended_action == ReferenceAction.no_action

    def test_healthy_input_produces_none_pattern(self):
        r = self.engine.assess(make_input())
        assert r.reference_pattern == ReferencePattern.none

    def test_healthy_input_produces_healthy_signal(self):
        r = self.engine.assess(make_input())
        assert "healthy" in r.reference_signal.lower()

    def test_worst_case_input_produces_critical_risk(self):
        inp = make_input(
            deals_with_reference_deployed_pct=0.0,
            avg_references_per_deal=0.0,
            deals_with_no_evidence_pct=1.0,
            unique_references_used_count=0,
            case_study_deployment_rate_pct=0.0,
            avg_evidence_assets_per_deal=0.0,
            avg_days_to_first_reference=90.0,
            late_stage_reference_rate_pct=1.0,
            reference_repeat_use_count=10,
            roi_document_shared_pct=0.0,
            analyst_report_leveraged_pct=0.0,
            competitive_displacement_story_used_pct=0.0,
        )
        r = self.engine.assess(inp)
        assert r.reference_risk == ReferenceRisk.critical

    def test_worst_case_produces_blind_severity(self):
        inp = make_input(
            deals_with_reference_deployed_pct=0.0,
            avg_references_per_deal=0.0,
            deals_with_no_evidence_pct=1.0,
            unique_references_used_count=0,
            case_study_deployment_rate_pct=0.0,
            avg_evidence_assets_per_deal=0.0,
            avg_days_to_first_reference=90.0,
            late_stage_reference_rate_pct=1.0,
            reference_repeat_use_count=10,
            roi_document_shared_pct=0.0,
            analyst_report_leveraged_pct=0.0,
            competitive_displacement_story_used_pct=0.0,
        )
        r = self.engine.assess(inp)
        assert r.reference_severity == ReferenceSeverity.blind

    def test_sub_scores_are_between_0_and_100(self):
        r = self.engine.assess(make_input())
        assert 0.0 <= r.reference_utilization_score <= 100.0
        assert 0.0 <= r.evidence_diversity_score <= 100.0
        assert 0.0 <= r.reference_timing_score <= 100.0
        assert 0.0 <= r.evidence_depth_score <= 100.0

    def test_composite_between_0_and_100(self):
        r = self.engine.assess(make_input())
        assert 0.0 <= r.reference_composite <= 100.0

    def test_scores_are_rounded_to_1dp(self):
        r = self.engine.assess(make_input())
        assert r.reference_utilization_score == round(r.reference_utilization_score, 1)
        assert r.evidence_diversity_score == round(r.evidence_diversity_score, 1)
        assert r.reference_timing_score == round(r.reference_timing_score, 1)
        assert r.evidence_depth_score == round(r.evidence_depth_score, 1)
        assert r.reference_composite == round(r.reference_composite, 1)

    def test_impact_is_non_negative(self):
        r = self.engine.assess(make_input())
        assert r.estimated_win_rate_impact_usd >= 0.0

    def test_has_reference_gap_is_bool(self):
        r = self.engine.assess(make_input())
        assert isinstance(r.has_reference_gap, bool)

    def test_requires_reference_coaching_is_bool(self):
        r = self.engine.assess(make_input())
        assert isinstance(r.requires_reference_coaching, bool)


# ===========================================================================
# 17. ASSESS_BATCH()
# ===========================================================================

class TestAssessBatch:
    def setup_method(self):
        self.engine = make_engine()

    def test_returns_list(self):
        result = self.engine.assess_batch([make_input()])
        assert isinstance(result, list)

    def test_returns_correct_count(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = self.engine.assess_batch(inputs)
        assert len(results) == 5

    def test_each_result_is_reference_result(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        for r in self.engine.assess_batch(inputs):
            assert isinstance(r, ReferenceResult)

    def test_empty_batch_returns_empty_list(self):
        assert self.engine.assess_batch([]) == []

    def test_batch_results_stored_internally(self):
        e = make_engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(4)]
        e.assess_batch(inputs)
        assert len(e._results) == 4

    def test_batch_rep_ids_match_inputs(self):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(3)]
        results = self.engine.assess_batch(inputs)
        assert [r.rep_id for r in results] == [f"REP-{i}" for i in range(3)]

    def test_single_item_batch(self):
        inputs = [make_input(rep_id="SOLO")]
        results = self.engine.assess_batch(inputs)
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"

    def test_batch_after_assess_accumulates(self):
        e = make_engine()
        e.assess(make_input(rep_id="FIRST"))
        e.assess_batch([make_input(rep_id="B1"), make_input(rep_id="B2")])
        assert len(e._results) == 3


# ===========================================================================
# 18. SUMMARY()
# ===========================================================================

class TestSummary:
    def _engine_with_results(self, count=3) -> SalesReferenceIntelligenceEngine:
        e = make_engine()
        for i in range(count):
            e.assess(make_input(rep_id=f"R{i}"))
        return e

    def test_empty_summary_has_13_keys(self):
        e = make_engine()
        s = e.summary()
        assert len(s) == 13

    def test_empty_summary_total_zero(self):
        e = make_engine()
        assert e.summary()["total"] == 0

    def test_empty_summary_avg_composite_zero(self):
        e = make_engine()
        assert e.summary()["avg_reference_composite"] == 0.0

    def test_empty_summary_gap_count_zero(self):
        e = make_engine()
        assert e.summary()["reference_gap_count"] == 0

    def test_empty_summary_coaching_count_zero(self):
        e = make_engine()
        assert e.summary()["coaching_count"] == 0

    def test_empty_summary_total_impact_zero(self):
        e = make_engine()
        assert e.summary()["total_estimated_win_rate_impact_usd"] == 0.0

    def test_empty_summary_risk_counts_empty(self):
        e = make_engine()
        assert e.summary()["risk_counts"] == {}

    def test_empty_summary_pattern_counts_empty(self):
        e = make_engine()
        assert e.summary()["pattern_counts"] == {}

    def test_empty_summary_severity_counts_empty(self):
        e = make_engine()
        assert e.summary()["severity_counts"] == {}

    def test_empty_summary_action_counts_empty(self):
        e = make_engine()
        assert e.summary()["action_counts"] == {}

    def test_non_empty_summary_has_13_keys(self):
        e = self._engine_with_results()
        assert len(e.summary()) == 13

    def test_total_matches_assessed_count(self):
        e = self._engine_with_results(5)
        assert e.summary()["total"] == 5

    def test_risk_counts_values_sum_to_total(self):
        e = self._engine_with_results(4)
        s = e.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_pattern_counts_values_sum_to_total(self):
        e = self._engine_with_results(4)
        s = e.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_severity_counts_values_sum_to_total(self):
        e = self._engine_with_results(4)
        s = e.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_action_counts_values_sum_to_total(self):
        e = self._engine_with_results(4)
        s = e.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_avg_reference_composite_range(self):
        e = self._engine_with_results(3)
        avg = e.summary()["avg_reference_composite"]
        assert 0.0 <= avg <= 100.0

    def test_avg_utilization_range(self):
        e = self._engine_with_results(3)
        avg = e.summary()["avg_reference_utilization_score"]
        assert 0.0 <= avg <= 100.0

    def test_avg_diversity_range(self):
        e = self._engine_with_results(3)
        avg = e.summary()["avg_evidence_diversity_score"]
        assert 0.0 <= avg <= 100.0

    def test_avg_timing_range(self):
        e = self._engine_with_results(3)
        avg = e.summary()["avg_reference_timing_score"]
        assert 0.0 <= avg <= 100.0

    def test_avg_depth_range(self):
        e = self._engine_with_results(3)
        avg = e.summary()["avg_evidence_depth_score"]
        assert 0.0 <= avg <= 100.0

    def test_gap_count_lte_total(self):
        e = self._engine_with_results(4)
        s = e.summary()
        assert s["reference_gap_count"] <= s["total"]

    def test_coaching_count_lte_total(self):
        e = self._engine_with_results(4)
        s = e.summary()
        assert s["coaching_count"] <= s["total"]

    def test_total_impact_non_negative(self):
        e = self._engine_with_results(3)
        assert e.summary()["total_estimated_win_rate_impact_usd"] >= 0.0

    def test_summary_expected_keys(self):
        e = make_engine()
        s = e.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_reference_composite", "reference_gap_count",
            "coaching_count", "avg_reference_utilization_score",
            "avg_evidence_diversity_score", "avg_reference_timing_score",
            "avg_evidence_depth_score", "total_estimated_win_rate_impact_usd",
        }
        assert set(s.keys()) == expected

    def test_summary_avgs_rounded_to_1dp(self):
        e = self._engine_with_results(3)
        s = e.summary()
        for key in ["avg_reference_composite", "avg_reference_utilization_score",
                    "avg_evidence_diversity_score", "avg_reference_timing_score",
                    "avg_evidence_depth_score"]:
            v = s[key]
            assert v == round(v, 1)

    def test_summary_with_single_result(self):
        e = make_engine()
        r = e.assess(make_input())
        s = e.summary()
        assert s["total"] == 1
        assert s["avg_reference_composite"] == pytest.approx(r.reference_composite, abs=0.1)

    def test_summary_impact_is_sum_of_individual_impacts(self):
        e = make_engine()
        inputs = [make_input(rep_id=f"R{i}", total_deals_active=10,
                              deals_with_no_evidence_pct=0.50,
                              avg_opportunity_value_usd=10_000.0,
                              reference_call_conversion_lift_pct=0.10)
                  for i in range(3)]
        results = e.assess_batch(inputs)
        expected_total = round(sum(r.estimated_win_rate_impact_usd for r in results), 2)
        assert e.summary()["total_estimated_win_rate_impact_usd"] == pytest.approx(expected_total)

    def test_summary_risk_counts_keys_are_strings(self):
        e = self._engine_with_results(2)
        for k in e.summary()["risk_counts"]:
            assert isinstance(k, str)

    def test_summary_pattern_counts_keys_are_strings(self):
        e = self._engine_with_results(2)
        for k in e.summary()["pattern_counts"]:
            assert isinstance(k, str)

    def test_summary_severity_counts_keys_are_strings(self):
        e = self._engine_with_results(2)
        for k in e.summary()["severity_counts"]:
            assert isinstance(k, str)

    def test_summary_action_counts_keys_are_strings(self):
        e = self._engine_with_results(2)
        for k in e.summary()["action_counts"]:
            assert isinstance(k, str)


# ===========================================================================
# 19. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def setup_method(self):
        self.engine = make_engine()

    def test_zero_total_deals_produces_zero_impact(self):
        inp = make_input(total_deals_active=0, deals_with_no_evidence_pct=0.50)
        r = self.engine.assess(inp)
        assert r.estimated_win_rate_impact_usd == 0.0

    def test_pct_exactly_100_boundary_for_deployed(self):
        inp = make_input(deals_with_reference_deployed_pct=1.0)
        r = self.engine.assess(inp)
        assert r.reference_utilization_score >= 0.0

    def test_pct_zero_boundary_for_deployed(self):
        inp = make_input(deals_with_reference_deployed_pct=0.0)
        r = self.engine.assess(inp)
        assert r.reference_utilization_score >= 40.0

    def test_single_active_deal(self):
        inp = make_input(total_deals_active=1)
        r = self.engine.assess(inp)
        assert r is not None

    def test_large_opportunity_value(self):
        inp = make_input(
            avg_opportunity_value_usd=1_000_000.0,
            total_deals_active=100,
            deals_with_no_evidence_pct=0.50,
            reference_call_conversion_lift_pct=0.10,
        )
        r = self.engine.assess(inp)
        assert r.estimated_win_rate_impact_usd > 0.0

    def test_string_enum_comparison_for_risk(self):
        r = self.engine.assess(make_input())
        assert r.reference_risk == r.reference_risk.value

    def test_string_enum_comparison_for_pattern(self):
        r = self.engine.assess(make_input())
        assert r.reference_pattern == r.reference_pattern.value

    def test_string_enum_comparison_for_severity(self):
        r = self.engine.assess(make_input())
        assert r.reference_severity == r.reference_severity.value

    def test_string_enum_comparison_for_action(self):
        r = self.engine.assess(make_input())
        assert r.recommended_action == r.recommended_action.value

    def test_different_rep_ids_produce_independent_results(self):
        e = make_engine()
        r1 = e.assess(make_input(rep_id="A"))
        r2 = e.assess(make_input(rep_id="B"))
        assert r1.rep_id != r2.rep_id

    def test_engine_state_accumulates_across_assessments(self):
        e = make_engine()
        for i in range(10):
            e.assess(make_input(rep_id=f"R{i}"))
        assert len(e._results) == 10

    def test_all_score_methods_return_float(self):
        inp = make_input()
        e = make_engine()
        assert isinstance(e._reference_utilization_score(inp), float)
        assert isinstance(e._evidence_diversity_score(inp), float)
        assert isinstance(e._reference_timing_score(inp), float)
        assert isinstance(e._evidence_depth_score(inp), float)

    def test_to_dict_round_trip_rep_id(self):
        inp = make_input(rep_id="ROUND_TRIP")
        r = self.engine.assess(inp)
        assert r.to_dict()["rep_id"] == "ROUND_TRIP"

    def test_fresh_engine_has_no_results(self):
        e = make_engine()
        assert e._results == []

    def test_utilization_boundary_025(self):
        # deals_with_no_evidence_pct exactly 0.25 should add 12
        inp = make_input(
            deals_with_reference_deployed_pct=0.90,
            avg_references_per_deal=3.0,
            deals_with_no_evidence_pct=0.25,
        )
        s = self.engine._reference_utilization_score(inp)
        assert s >= 12.0


# ===========================================================================
# 20. END-TO-END SCENARIOS
# ===========================================================================

class TestEndToEndScenarios:
    """Full pipeline tests for representative rep profiles."""

    def test_star_rep_all_healthy(self):
        e = make_engine()
        inp = make_input(
            rep_id="STAR",
            deals_with_reference_deployed_pct=0.95,
            avg_references_per_deal=3.0,
            deals_with_no_evidence_pct=0.05,
            unique_references_used_count=12,
            case_study_deployment_rate_pct=0.90,
            avg_evidence_assets_per_deal=4.0,
            avg_days_to_first_reference=7.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=1,
            roi_document_shared_pct=0.80,
            analyst_report_leveraged_pct=0.60,
            competitive_displacement_story_used_pct=0.60,
        )
        r = e.assess(inp)
        assert r.reference_risk == ReferenceRisk.low
        assert r.reference_severity == ReferenceSeverity.evidence_led
        assert r.recommended_action == ReferenceAction.no_action
        assert r.has_reference_gap is False
        assert "healthy" in r.reference_signal.lower()

    def test_struggling_rep_critical_risk(self):
        e = make_engine()
        inp = make_input(
            rep_id="STRUGGLING",
            deals_with_reference_deployed_pct=0.05,
            avg_references_per_deal=0.2,
            deals_with_no_evidence_pct=0.80,
            unique_references_used_count=1,
            case_study_deployment_rate_pct=0.05,
            avg_evidence_assets_per_deal=0.5,
            avg_days_to_first_reference=70.0,
            late_stage_reference_rate_pct=0.80,
            reference_repeat_use_count=8,
            roi_document_shared_pct=0.05,
            analyst_report_leveraged_pct=0.05,
            competitive_displacement_story_used_pct=0.05,
        )
        r = e.assess(inp)
        assert r.reference_risk == ReferenceRisk.critical
        assert r.reference_severity == ReferenceSeverity.blind
        assert r.has_reference_gap is True
        assert r.requires_reference_coaching is True

    def test_batch_mixed_reps(self):
        e = make_engine()
        inputs = [
            make_input(rep_id="HEALTHY",
                       deals_with_reference_deployed_pct=0.90,
                       avg_references_per_deal=3.0,
                       deals_with_no_evidence_pct=0.05),
            make_input(rep_id="CRITICAL",
                       deals_with_reference_deployed_pct=0.05,
                       avg_references_per_deal=0.2,
                       deals_with_no_evidence_pct=0.80,
                       avg_days_to_first_reference=70.0,
                       reference_repeat_use_count=8),
        ]
        results = e.assess_batch(inputs)
        assert results[0].reference_risk == ReferenceRisk.low
        assert results[1].reference_risk in (ReferenceRisk.critical, ReferenceRisk.high)

    def test_summary_after_batch(self):
        e = make_engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(6)]
        e.assess_batch(inputs)
        s = e.summary()
        assert s["total"] == 6
        assert sum(s["risk_counts"].values()) == 6

    def test_avoidance_pattern_triggers_onboarding_when_critical(self):
        e = make_engine()
        inp = make_input(
            deals_with_reference_deployed_pct=0.05,
            avg_references_per_deal=0.1,
            deals_with_no_evidence_pct=0.90,
            unique_references_used_count=1,
            case_study_deployment_rate_pct=0.05,
            avg_evidence_assets_per_deal=0.5,
            avg_days_to_first_reference=5.0,
            late_stage_reference_rate_pct=0.10,
            reference_repeat_use_count=1,
            roi_document_shared_pct=0.80,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.50,
        )
        r = e.assess(inp)
        if r.reference_risk == ReferenceRisk.critical:
            assert r.reference_pattern == ReferencePattern.reference_avoidance
            assert r.recommended_action == ReferenceAction.reference_program_onboarding

    def test_to_dict_on_assessed_result(self):
        e = make_engine()
        r = e.assess(make_input(rep_id="DICT_TEST", region="TEST"))
        d = r.to_dict()
        assert d["rep_id"] == "DICT_TEST"
        assert d["region"] == "TEST"
        assert isinstance(d["reference_risk"], str)
        assert isinstance(d["has_reference_gap"], bool)

    def test_summary_risk_counts_contain_only_valid_risk_values(self):
        e = make_engine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        valid = {r.value for r in ReferenceRisk}
        for key in e.summary()["risk_counts"]:
            assert key in valid

    def test_summary_pattern_counts_contain_only_valid_pattern_values(self):
        e = make_engine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        valid = {p.value for p in ReferencePattern}
        for key in e.summary()["pattern_counts"]:
            assert key in valid

    def test_summary_severity_counts_contain_only_valid_severity_values(self):
        e = make_engine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        valid = {s.value for s in ReferenceSeverity}
        for key in e.summary()["severity_counts"]:
            assert key in valid

    def test_summary_action_counts_contain_only_valid_action_values(self):
        e = make_engine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        valid = {a.value for a in ReferenceAction}
        for key in e.summary()["action_counts"]:
            assert key in valid

    def test_moderate_risk_always_evidence_library_training(self):
        """Any moderate-risk scenario → evidence_library_training regardless of pattern."""
        e = make_engine()
        # Build an input that reliably lands in moderate risk band (composite ~20-39)
        inp = make_input(
            deals_with_reference_deployed_pct=0.60,  # +8 to utilization
            avg_references_per_deal=1.5,
            deals_with_no_evidence_pct=0.15,
            unique_references_used_count=8,
            case_study_deployment_rate_pct=0.70,
            avg_evidence_assets_per_deal=3.0,
            avg_days_to_first_reference=14.0,         # +8 to timing
            late_stage_reference_rate_pct=0.25,
            reference_repeat_use_count=2,
            roi_document_shared_pct=0.70,
            analyst_report_leveraged_pct=0.50,
            competitive_displacement_story_used_pct=0.50,
        )
        r = e.assess(inp)
        if r.reference_risk == ReferenceRisk.moderate:
            assert r.recommended_action == ReferenceAction.evidence_library_training

    def test_composite_formula_consistent_with_assessed_result(self):
        e = make_engine()
        inp = make_input()
        r = e.assess(inp)
        expected_composite = round(
            r.reference_utilization_score * 0.30
            + r.evidence_diversity_score * 0.30
            + r.reference_timing_score * 0.25
            + r.evidence_depth_score * 0.15,
            1,
        )
        expected_composite = min(expected_composite, 100.0)
        assert r.reference_composite == pytest.approx(expected_composite)
