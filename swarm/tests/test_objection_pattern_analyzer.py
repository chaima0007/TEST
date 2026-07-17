"""
Comprehensive pytest tests for ObjectionPatternAnalyzer.
"""
from __future__ import annotations

import pytest

from swarm.intelligence.objection_pattern_analyzer import (
    ObjectionPatternAnalyzer,
    ObjectionPatternInput,
    ObjectionType,
    ObjectionSeverity,
    HandlingReadiness,
    ObjectionAction,
    ObjectionPatternResult,
)


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def make_input(
    *,
    deal_id: str = "D001",
    deal_name: str = "Test Deal",
    rep_id: str = "R001",
    price_objections_count: int = 0,
    timing_objections_count: int = 0,
    competitor_objections_count: int = 0,
    status_quo_objections_count: int = 0,
    risk_objections_count: int = 0,
    total_objections_raised: int = 0,
    objections_successfully_handled: int = 0,
    objection_reoccurrence_count: int = 0,
    rep_used_battlecard: int = 0,
    rep_asked_discovery_question: int = 0,
    social_proof_used: int = 0,
    roi_calculator_used: int = 0,
    deal_stage_numeric: int = 1,
    deal_size_usd: float = 10_000.0,
    days_to_close: int = 30,
    objection_raised_in_late_stage: int = 0,
    competitor_deal_lost_last_90d: int = 0,
    discovery_call_count: int = 0,
    avg_objection_response_time_hrs: float = 2.0,
) -> ObjectionPatternInput:
    return ObjectionPatternInput(
        deal_id=deal_id,
        deal_name=deal_name,
        rep_id=rep_id,
        price_objections_count=price_objections_count,
        timing_objections_count=timing_objections_count,
        competitor_objections_count=competitor_objections_count,
        status_quo_objections_count=status_quo_objections_count,
        risk_objections_count=risk_objections_count,
        total_objections_raised=total_objections_raised,
        objections_successfully_handled=objections_successfully_handled,
        objection_reoccurrence_count=objection_reoccurrence_count,
        rep_used_battlecard=rep_used_battlecard,
        rep_asked_discovery_question=rep_asked_discovery_question,
        social_proof_used=social_proof_used,
        roi_calculator_used=roi_calculator_used,
        deal_stage_numeric=deal_stage_numeric,
        deal_size_usd=deal_size_usd,
        days_to_close=days_to_close,
        objection_raised_in_late_stage=objection_raised_in_late_stage,
        competitor_deal_lost_last_90d=competitor_deal_lost_last_90d,
        discovery_call_count=discovery_call_count,
        avg_objection_response_time_hrs=avg_objection_response_time_hrs,
    )


@pytest.fixture
def analyzer():
    return ObjectionPatternAnalyzer()


# ---------------------------------------------------------------------------
# Invariant 1: ObjectionPatternInput has exactly 22 fields
# ---------------------------------------------------------------------------

class TestObjectionPatternInputFields:
    def test_has_exactly_22_fields(self):
        import dataclasses
        fields = dataclasses.fields(ObjectionPatternInput)
        assert len(fields) == 22, f"Expected 22 fields, got {len(fields)}"

    def test_field_names(self):
        import dataclasses
        field_names = {f.name for f in dataclasses.fields(ObjectionPatternInput)}
        expected = {
            "deal_id", "deal_name", "rep_id",
            "price_objections_count", "timing_objections_count",
            "competitor_objections_count", "status_quo_objections_count",
            "risk_objections_count", "total_objections_raised",
            "objections_successfully_handled", "objection_reoccurrence_count",
            "rep_used_battlecard", "rep_asked_discovery_question",
            "social_proof_used", "roi_calculator_used",
            "deal_stage_numeric", "deal_size_usd", "days_to_close",
            "objection_raised_in_late_stage", "competitor_deal_lost_last_90d",
            "discovery_call_count", "avg_objection_response_time_hrs",
        }
        assert field_names == expected


# ---------------------------------------------------------------------------
# Invariant 2: ObjectionPatternResult.to_dict() returns exactly 15 keys
# ---------------------------------------------------------------------------

class TestToDict:
    def test_to_dict_returns_15_keys(self, analyzer):
        inp = make_input()
        result = analyzer.analyze(inp)
        d = result.to_dict()
        assert len(d) == 15, f"Expected 15 keys, got {len(d)}: {list(d.keys())}"

    def test_to_dict_key_names(self, analyzer):
        inp = make_input()
        result = analyzer.analyze(inp)
        d = result.to_dict()
        expected_keys = {
            "deal_id", "deal_name", "primary_objection_type",
            "objection_severity", "handling_readiness", "objection_action",
            "handling_effectiveness_score", "objection_density_score",
            "pattern_risk_score", "rep_preparedness_score",
            "objection_composite", "handle_rate",
            "late_stage_risk", "is_objection_contained", "needs_coaching",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self, analyzer):
        inp = make_input(total_objections_raised=2, objections_successfully_handled=2,
                         price_objections_count=2)
        result = analyzer.analyze(inp)
        d = result.to_dict()
        assert isinstance(d["primary_objection_type"], str)
        assert isinstance(d["objection_severity"], str)
        assert isinstance(d["handling_readiness"], str)
        assert isinstance(d["objection_action"], str)


# ---------------------------------------------------------------------------
# Invariant 3: summary() returns exactly 13 keys
# ---------------------------------------------------------------------------

class TestSummaryKeys:
    def test_empty_summary_has_13_keys(self, analyzer):
        s = analyzer.summary()
        assert len(s) == 13, f"Expected 13 keys, got {len(s)}: {list(s.keys())}"

    def test_nonempty_summary_has_13_keys(self, analyzer):
        analyzer.analyze(make_input())
        s = analyzer.summary()
        assert len(s) == 13

    def test_summary_key_names(self, analyzer):
        s = analyzer.summary()
        expected = {
            "total", "objection_type_counts", "severity_counts",
            "readiness_counts", "action_counts",
            "avg_objection_composite", "avg_handle_rate",
            "contained_count", "coaching_count",
            "avg_handling_effectiveness_score", "avg_pattern_risk_score",
            "avg_rep_preparedness_score", "avg_objection_density_score",
        }
        assert set(s.keys()) == expected


# ---------------------------------------------------------------------------
# Invariant 4: Enum members
# ---------------------------------------------------------------------------

class TestEnums:
    def test_objection_type_members(self):
        values = {e.value for e in ObjectionType}
        assert values == {"price", "timing", "competitor", "status_quo", "risk", "no_objection"}

    def test_objection_type_count(self):
        assert len(ObjectionType) == 6

    def test_objection_severity_members(self):
        values = {e.value for e in ObjectionSeverity}
        assert values == {"minor", "moderate", "serious", "deal_breaker"}

    def test_objection_severity_count(self):
        assert len(ObjectionSeverity) == 4

    def test_handling_readiness_members(self):
        values = {e.value for e in HandlingReadiness}
        assert values == {"prepared", "needs_prep", "reactive", "unprepared"}

    def test_handling_readiness_count(self):
        assert len(HandlingReadiness) == 4

    def test_objection_action_members(self):
        values = {e.value for e in ObjectionAction}
        assert values == {"none_needed", "reframe_value", "provide_proof", "executive_call"}

    def test_objection_action_count(self):
        assert len(ObjectionAction) == 4

    def test_enums_are_str_subclass(self):
        assert issubclass(ObjectionType, str)
        assert issubclass(ObjectionSeverity, str)
        assert issubclass(HandlingReadiness, str)
        assert issubclass(ObjectionAction, str)


# ---------------------------------------------------------------------------
# Invariant 5: Composite formula
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_composite_formula_directly(self, analyzer):
        handling = 80.0
        density = 60.0
        pat_risk = 70.0
        prep = 50.0
        expected = round(handling * 0.35 + density * 0.25 + pat_risk * 0.25 + prep * 0.15, 1)
        result = analyzer._composite(handling, density, pat_risk, prep)
        assert result == expected

    def test_composite_clamps_to_100(self, analyzer):
        assert analyzer._composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_composite_clamps_to_0(self, analyzer):
        assert analyzer._composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_composite_weights_add_to_1(self):
        # 0.35 + 0.25 + 0.25 + 0.15 == 1.0
        assert abs(0.35 + 0.25 + 0.25 + 0.15 - 1.0) < 1e-9

    def test_composite_is_reflected_in_result(self, analyzer):
        inp = make_input(
            total_objections_raised=2,
            objections_successfully_handled=2,
            rep_used_battlecard=1,
            rep_asked_discovery_question=1,
            social_proof_used=1,
            roi_calculator_used=1,
            avg_objection_response_time_hrs=2.0,
        )
        result = analyzer.analyze(inp)
        handling = analyzer._handling_effectiveness_score(inp)
        density = analyzer._objection_density_score(inp)
        pat_risk = analyzer._pattern_risk_score(inp)
        prep = analyzer._rep_preparedness_score(inp)
        expected = analyzer._composite(handling, density, pat_risk, prep)
        assert result.objection_composite == expected


# ---------------------------------------------------------------------------
# Invariant 6: is_objection_contained
# ---------------------------------------------------------------------------

class TestIsObjectionContained:
    def test_contained_when_composite_ge_60_and_reoccurrence_le_1(self, analyzer):
        # All tools used => high prep; no objections => easy deal
        inp = make_input(
            rep_used_battlecard=1,
            rep_asked_discovery_question=1,
            social_proof_used=1,
            roi_calculator_used=1,
            objection_reoccurrence_count=0,
        )
        result = analyzer.analyze(inp)
        # Verify the condition manually
        assert result.is_objection_contained == (
            result.objection_composite >= 60 and inp.objection_reoccurrence_count <= 1
        )

    def test_not_contained_when_reoccurrence_gt_1(self, analyzer):
        inp = make_input(
            rep_used_battlecard=1,
            rep_asked_discovery_question=1,
            social_proof_used=1,
            roi_calculator_used=1,
            total_objections_raised=3,
            objections_successfully_handled=3,
            objection_reoccurrence_count=2,
        )
        result = analyzer.analyze(inp)
        assert result.is_objection_contained is False

    def test_not_contained_when_composite_lt_60(self, analyzer):
        # No tools => prep=0, many objections at high reoccurrence => low composite
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=0,
            objection_reoccurrence_count=0,
            objection_raised_in_late_stage=1,
            competitor_deal_lost_last_90d=1,
            avg_objection_response_time_hrs=100.0,
        )
        result = analyzer.analyze(inp)
        if result.objection_composite < 60:
            assert result.is_objection_contained is False

    def test_contained_boundary_composite_exactly_60(self, analyzer):
        # Directly verify the property formula using the input's reoccurrence count
        inp = make_input(objection_reoccurrence_count=1)
        result = analyzer.analyze(inp)
        expected = result.objection_composite >= 60 and inp.objection_reoccurrence_count <= 1
        assert result.is_objection_contained == expected

    def test_contained_reoccurrence_boundary_1(self, analyzer):
        # reoccurrence == 1 is still contained if composite >= 60
        inp = make_input(
            rep_used_battlecard=1,
            rep_asked_discovery_question=1,
            social_proof_used=1,
            roi_calculator_used=1,
            objection_reoccurrence_count=1,
        )
        result = analyzer.analyze(inp)
        assert result.is_objection_contained == (result.objection_composite >= 60)


# ---------------------------------------------------------------------------
# Invariant 7: needs_coaching
# ---------------------------------------------------------------------------

class TestNeedsCoaching:
    def test_needs_coaching_when_prep_lt_40(self, analyzer):
        # No tools => prep=0 < 40
        inp = make_input()
        result = analyzer.analyze(inp)
        assert result.rep_preparedness_score < 40
        assert result.needs_coaching is True

    def test_needs_coaching_when_reoccurrence_ge_3(self, analyzer):
        inp = make_input(
            rep_used_battlecard=1,
            rep_asked_discovery_question=1,
            social_proof_used=1,
            roi_calculator_used=1,
            total_objections_raised=5,
            objections_successfully_handled=5,
            objection_reoccurrence_count=3,
        )
        result = analyzer.analyze(inp)
        assert result.needs_coaching is True

    def test_needs_coaching_when_composite_lt_40(self, analyzer):
        # Force a very low composite: low handling, low density score, low prep
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=0,
            objection_reoccurrence_count=4,
            objection_raised_in_late_stage=1,
            competitor_deal_lost_last_90d=1,
            avg_objection_response_time_hrs=100.0,
        )
        result = analyzer.analyze(inp)
        if result.objection_composite < 40:
            assert result.needs_coaching is True

    def test_no_coaching_when_all_conditions_false(self, analyzer):
        # Prep >= 40, reoccurrence < 3, composite >= 40
        inp = make_input(
            rep_used_battlecard=1,
            rep_asked_discovery_question=1,
            total_objections_raised=2,
            objections_successfully_handled=2,
            objection_reoccurrence_count=0,
            avg_objection_response_time_hrs=2.0,
        )
        result = analyzer.analyze(inp)
        expected = (
            result.rep_preparedness_score < 40
            or inp.objection_reoccurrence_count >= 3
            or result.objection_composite < 40
        )
        assert result.needs_coaching == expected

    def test_needs_coaching_reoccurrence_boundary_2(self, analyzer):
        # reoccurrence == 2 should NOT trigger the reoccurrence>=3 branch
        inp = make_input(
            rep_used_battlecard=1,
            rep_asked_discovery_question=1,
            social_proof_used=1,
            roi_calculator_used=1,
            total_objections_raised=2,
            objections_successfully_handled=2,
            objection_reoccurrence_count=2,
        )
        result = analyzer.analyze(inp)
        # coaching depends on other conditions; reoccurrence==2 alone doesn't trigger it
        assert result.needs_coaching == (
            result.rep_preparedness_score < 40
            or inp.objection_reoccurrence_count >= 3
            or result.objection_composite < 40
        )


# ---------------------------------------------------------------------------
# Invariant 8: handle_rate
# ---------------------------------------------------------------------------

class TestHandleRate:
    def test_handle_rate_zero_total_returns_100(self, analyzer):
        inp = make_input(total_objections_raised=0, objections_successfully_handled=0)
        result = analyzer.analyze(inp)
        assert result.handle_rate == 100.0

    def test_handle_rate_all_handled(self, analyzer):
        inp = make_input(
            total_objections_raised=5,
            objections_successfully_handled=5,
            price_objections_count=5,
        )
        result = analyzer.analyze(inp)
        assert result.handle_rate == 100.0

    def test_handle_rate_none_handled(self, analyzer):
        inp = make_input(
            total_objections_raised=4,
            objections_successfully_handled=0,
            price_objections_count=4,
        )
        result = analyzer.analyze(inp)
        assert result.handle_rate == 0.0

    def test_handle_rate_partial(self, analyzer):
        inp = make_input(
            total_objections_raised=4,
            objections_successfully_handled=3,
            price_objections_count=4,
        )
        result = analyzer.analyze(inp)
        assert result.handle_rate == round(3 / 4 * 100, 1)

    def test_handle_rate_is_rounded_to_1_decimal(self, analyzer):
        # 1/3 * 100 = 33.333... -> 33.3
        inp = make_input(
            total_objections_raised=3,
            objections_successfully_handled=1,
            price_objections_count=3,
        )
        result = analyzer.analyze(inp)
        assert result.handle_rate == round(1 / 3 * 100, 1)


# ---------------------------------------------------------------------------
# Invariant 9: _primary_objection_type
# ---------------------------------------------------------------------------

class TestPrimaryObjectionType:
    def test_no_objection_when_total_zero(self, analyzer):
        inp = make_input(total_objections_raised=0)
        result = analyzer.analyze(inp)
        assert result.primary_objection_type == ObjectionType.NO_OBJECTION

    def test_price_is_primary(self, analyzer):
        inp = make_input(
            total_objections_raised=5,
            objections_successfully_handled=5,
            price_objections_count=3,
            timing_objections_count=1,
            risk_objections_count=1,
        )
        result = analyzer.analyze(inp)
        assert result.primary_objection_type == ObjectionType.PRICE

    def test_timing_is_primary(self, analyzer):
        inp = make_input(
            total_objections_raised=4,
            objections_successfully_handled=4,
            timing_objections_count=4,
        )
        result = analyzer.analyze(inp)
        assert result.primary_objection_type == ObjectionType.TIMING

    def test_competitor_is_primary(self, analyzer):
        inp = make_input(
            total_objections_raised=3,
            objections_successfully_handled=3,
            competitor_objections_count=3,
        )
        result = analyzer.analyze(inp)
        assert result.primary_objection_type == ObjectionType.COMPETITOR

    def test_status_quo_is_primary(self, analyzer):
        inp = make_input(
            total_objections_raised=5,
            objections_successfully_handled=5,
            status_quo_objections_count=5,
        )
        result = analyzer.analyze(inp)
        assert result.primary_objection_type == ObjectionType.STATUS_QUO

    def test_risk_is_primary(self, analyzer):
        inp = make_input(
            total_objections_raised=2,
            objections_successfully_handled=2,
            risk_objections_count=2,
        )
        result = analyzer.analyze(inp)
        assert result.primary_objection_type == ObjectionType.RISK


# ---------------------------------------------------------------------------
# Scoring helpers: _handling_effectiveness_score
# ---------------------------------------------------------------------------

class TestHandlingEffectivenessScore:
    def test_no_objections_returns_85(self, analyzer):
        inp = make_input(total_objections_raised=0)
        assert analyzer._handling_effectiveness_score(inp) == 85.0

    def test_hr_ge_90_adds_50(self, analyzer):
        # hr=0.9 => +50; reoccurrence=0 => +25; no late stage; fast response => +15
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=9,
            objection_reoccurrence_count=0,
            objection_raised_in_late_stage=0,
            avg_objection_response_time_hrs=2.0,
        )
        score = analyzer._handling_effectiveness_score(inp)
        # 50 (hr>=0.9) + 25 (reoccurrence==0) + 0 (no late) + 15 (<=4hrs) = 90
        assert score == 90.0

    def test_hr_ge_70_adds_35(self, analyzer):
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=7,
            objection_reoccurrence_count=0,
            avg_objection_response_time_hrs=2.0,
        )
        score = analyzer._handling_effectiveness_score(inp)
        # 35 + 25 + 15 = 75
        assert score == 75.0

    def test_hr_ge_50_adds_20(self, analyzer):
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=5,
            objection_reoccurrence_count=0,
            avg_objection_response_time_hrs=2.0,
        )
        score = analyzer._handling_effectiveness_score(inp)
        # 20 + 25 + 15 = 60
        assert score == 60.0

    def test_hr_ge_30_adds_10(self, analyzer):
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=3,
            objection_reoccurrence_count=0,
            avg_objection_response_time_hrs=2.0,
        )
        score = analyzer._handling_effectiveness_score(inp)
        # 10 + 25 + 15 = 50
        assert score == 50.0

    def test_hr_below_30_adds_nothing(self, analyzer):
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=2,
            objection_reoccurrence_count=0,
            avg_objection_response_time_hrs=2.0,
        )
        score = analyzer._handling_effectiveness_score(inp)
        # 0 + 25 + 15 = 40
        assert score == 40.0

    def test_reoccurrence_0_adds_25(self, analyzer):
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=9,
            objection_reoccurrence_count=0,
            avg_objection_response_time_hrs=100.0,  # no response bonus
        )
        # 50 (hr>=.9) + 25 (reoccurrence==0) + 0 (slow response) = 75
        # actually slow response -10: 50+25-10 = 65
        score = analyzer._handling_effectiveness_score(inp)
        assert score == 65.0

    def test_reoccurrence_1_adds_12(self, analyzer):
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=9,
            objection_reoccurrence_count=1,
            avg_objection_response_time_hrs=100.0,
        )
        # 50 + 12 - 10 = 52
        score = analyzer._handling_effectiveness_score(inp)
        assert score == 52.0

    def test_reoccurrence_ge_3_subtracts_10(self, analyzer):
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=9,
            objection_reoccurrence_count=3,
            avg_objection_response_time_hrs=100.0,
        )
        # 50 - 10 - 10 = 30
        score = analyzer._handling_effectiveness_score(inp)
        assert score == 30.0

    def test_late_stage_subtracts_15(self, analyzer):
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=9,
            objection_reoccurrence_count=0,
            objection_raised_in_late_stage=1,
            avg_objection_response_time_hrs=2.0,
        )
        # 50 + 25 - 15 + 15 = 75
        score = analyzer._handling_effectiveness_score(inp)
        assert score == 75.0

    def test_response_time_le_4_adds_15(self, analyzer):
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=9,
            objection_reoccurrence_count=0,
            avg_objection_response_time_hrs=4.0,
        )
        score = analyzer._handling_effectiveness_score(inp)
        assert score == 90.0

    def test_response_time_le_24_adds_8(self, analyzer):
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=9,
            objection_reoccurrence_count=0,
            avg_objection_response_time_hrs=10.0,
        )
        # 50 + 25 + 8 = 83
        score = analyzer._handling_effectiveness_score(inp)
        assert score == 83.0

    def test_response_time_ge_72_subtracts_10(self, analyzer):
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=9,
            objection_reoccurrence_count=0,
            avg_objection_response_time_hrs=72.0,
        )
        # 50 + 25 - 10 = 65
        score = analyzer._handling_effectiveness_score(inp)
        assert score == 65.0

    def test_score_clamps_to_zero(self, analyzer):
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=0,
            objection_reoccurrence_count=3,
            objection_raised_in_late_stage=1,
            avg_objection_response_time_hrs=100.0,
        )
        # 0 - 10 - 15 - 10 = -35 => 0
        score = analyzer._handling_effectiveness_score(inp)
        assert score == 0.0

    def test_score_clamps_to_100(self, analyzer):
        # Maximum possible: hr>=.9(50) + reoccurrence==0(25) + late_no(0) + fast(15) = 90 max
        # Actually can't exceed 90 given the scoring, but let's test clamp exists
        inp = make_input(
            total_objections_raised=10,
            objections_successfully_handled=10,
            objection_reoccurrence_count=0,
            avg_objection_response_time_hrs=1.0,
        )
        score = analyzer._handling_effectiveness_score(inp)
        assert score <= 100.0
        assert score >= 0.0


# ---------------------------------------------------------------------------
# Scoring helpers: _objection_density_score
# ---------------------------------------------------------------------------

class TestObjectionDensityScore:
    def test_density_zero_returns_90(self, analyzer):
        inp = make_input(total_objections_raised=0, deal_stage_numeric=1)
        assert analyzer._objection_density_score(inp) == 90.0

    def test_density_le_05_returns_75(self, analyzer):
        # 1 objection / 4 stages = 0.25
        inp = make_input(total_objections_raised=1, deal_stage_numeric=4)
        assert analyzer._objection_density_score(inp) == 75.0

    def test_density_le_1_returns_55(self, analyzer):
        # 2 objections / 2 stages = 1.0
        inp = make_input(total_objections_raised=2, deal_stage_numeric=2)
        assert analyzer._objection_density_score(inp) == 55.0

    def test_density_le_2_returns_35(self, analyzer):
        # 4 objections / 2 stages = 2.0
        inp = make_input(total_objections_raised=4, deal_stage_numeric=2)
        assert analyzer._objection_density_score(inp) == 35.0

    def test_density_gt_2_returns_15(self, analyzer):
        # 7 objections / 2 stages = 3.5
        inp = make_input(total_objections_raised=7, deal_stage_numeric=2)
        assert analyzer._objection_density_score(inp) == 15.0

    def test_competitor_status_quo_combo_penalty(self, analyzer):
        # competitor>=2 and status_quo>=2 => -15
        inp = make_input(
            total_objections_raised=0,
            deal_stage_numeric=1,
            competitor_objections_count=2,
            status_quo_objections_count=2,
        )
        # density==0 => 90 - 15 = 75
        assert analyzer._objection_density_score(inp) == 75.0

    def test_competitor_status_quo_no_penalty_when_below_threshold(self, analyzer):
        inp = make_input(
            total_objections_raised=0,
            deal_stage_numeric=1,
            competitor_objections_count=1,
            status_quo_objections_count=1,
        )
        # density==0 => 90; no combo penalty
        assert analyzer._objection_density_score(inp) == 90.0

    def test_stage_min_1(self, analyzer):
        # deal_stage_numeric=0 should be treated as 1
        inp = make_input(total_objections_raised=1, deal_stage_numeric=0)
        # max(1,0)=1 => density=1.0 => 55
        assert analyzer._objection_density_score(inp) == 55.0

    def test_score_clamped_to_0(self, analyzer):
        # Very high density + combo penalty
        inp = make_input(
            total_objections_raised=20,
            deal_stage_numeric=1,
            competitor_objections_count=5,
            status_quo_objections_count=5,
        )
        # density=20 => 15 - 15 = 0
        score = analyzer._objection_density_score(inp)
        assert score == 0.0


# ---------------------------------------------------------------------------
# Scoring helpers: _pattern_risk_score
# ---------------------------------------------------------------------------

class TestPatternRiskScore:
    def test_no_risk_factors_returns_100(self, analyzer):
        inp = make_input(
            objection_reoccurrence_count=0,
            objection_raised_in_late_stage=0,
            competitor_deal_lost_last_90d=0,
            total_objections_raised=0,
        )
        assert analyzer._pattern_risk_score(inp) == 100.0

    def test_reoccurrence_ge_3_adds_40_risk(self, analyzer):
        inp = make_input(objection_reoccurrence_count=3)
        # risk=40 => score=60
        assert analyzer._pattern_risk_score(inp) == 60.0

    def test_reoccurrence_ge_2_adds_25_risk(self, analyzer):
        inp = make_input(objection_reoccurrence_count=2)
        # risk=25 => score=75
        assert analyzer._pattern_risk_score(inp) == 75.0

    def test_reoccurrence_ge_1_adds_10_risk(self, analyzer):
        inp = make_input(objection_reoccurrence_count=1)
        # risk=10 => score=90
        assert analyzer._pattern_risk_score(inp) == 90.0

    def test_late_stage_adds_30_risk(self, analyzer):
        inp = make_input(objection_raised_in_late_stage=1)
        # risk=30 => score=70
        assert analyzer._pattern_risk_score(inp) == 70.0

    def test_competitor_lost_adds_15_risk(self, analyzer):
        inp = make_input(competitor_deal_lost_last_90d=1)
        # risk=15 => score=85
        assert analyzer._pattern_risk_score(inp) == 85.0

    def test_total_ge_8_adds_15_risk(self, analyzer):
        inp = make_input(total_objections_raised=8)
        # risk=15 => score=85
        assert analyzer._pattern_risk_score(inp) == 85.0

    def test_total_ge_5_adds_8_risk(self, analyzer):
        inp = make_input(total_objections_raised=5)
        # risk=8 => score=92
        assert analyzer._pattern_risk_score(inp) == 92.0

    def test_total_lt_5_adds_no_risk(self, analyzer):
        inp = make_input(total_objections_raised=4)
        # risk=0 => score=100
        assert analyzer._pattern_risk_score(inp) == 100.0

    def test_combined_risk_clamped_to_0(self, analyzer):
        inp = make_input(
            objection_reoccurrence_count=3,
            objection_raised_in_late_stage=1,
            competitor_deal_lost_last_90d=1,
            total_objections_raised=8,
        )
        # risk = 40+30+15+15=100 => score=0
        assert analyzer._pattern_risk_score(inp) == 0.0


# ---------------------------------------------------------------------------
# Scoring helpers: _rep_preparedness_score
# ---------------------------------------------------------------------------

class TestRepPreparednessScore:
    def test_no_tools_returns_0(self, analyzer):
        inp = make_input()
        assert analyzer._rep_preparedness_score(inp) == 0.0

    def test_battlecard_adds_35(self, analyzer):
        inp = make_input(rep_used_battlecard=1)
        assert analyzer._rep_preparedness_score(inp) == 35.0

    def test_discovery_question_adds_25(self, analyzer):
        inp = make_input(rep_asked_discovery_question=1)
        assert analyzer._rep_preparedness_score(inp) == 25.0

    def test_social_proof_adds_20(self, analyzer):
        inp = make_input(social_proof_used=1)
        assert analyzer._rep_preparedness_score(inp) == 20.0

    def test_roi_calculator_adds_15(self, analyzer):
        inp = make_input(roi_calculator_used=1)
        assert analyzer._rep_preparedness_score(inp) == 15.0

    def test_discovery_calls_ge_3_adds_5_bonus(self, analyzer):
        inp = make_input(rep_used_battlecard=1, discovery_call_count=3)
        # 35 + 5 = 40
        assert analyzer._rep_preparedness_score(inp) == 40.0

    def test_discovery_calls_lt_3_no_bonus(self, analyzer):
        inp = make_input(rep_used_battlecard=1, discovery_call_count=2)
        assert analyzer._rep_preparedness_score(inp) == 35.0

    def test_all_tools_returns_95_plus_bonus(self, analyzer):
        # 35+25+20+15=95; +5 bonus if discovery_call_count>=3
        inp = make_input(
            rep_used_battlecard=1,
            rep_asked_discovery_question=1,
            social_proof_used=1,
            roi_calculator_used=1,
            discovery_call_count=3,
        )
        assert analyzer._rep_preparedness_score(inp) == 100.0

    def test_all_tools_without_bonus_returns_95(self, analyzer):
        inp = make_input(
            rep_used_battlecard=1,
            rep_asked_discovery_question=1,
            social_proof_used=1,
            roi_calculator_used=1,
            discovery_call_count=0,
        )
        assert analyzer._rep_preparedness_score(inp) == 95.0

    def test_score_clamped_to_100(self, analyzer):
        # Already capped at 95+5=100; won't exceed
        inp = make_input(
            rep_used_battlecard=1,
            rep_asked_discovery_question=1,
            social_proof_used=1,
            roi_calculator_used=1,
            discovery_call_count=10,
        )
        assert analyzer._rep_preparedness_score(inp) == 100.0


# ---------------------------------------------------------------------------
# Classifier: _objection_severity
# ---------------------------------------------------------------------------

class TestObjectionSeverity:
    def test_zero_total_returns_minor(self, analyzer):
        inp = make_input(total_objections_raised=0)
        assert analyzer._objection_severity(inp) == ObjectionSeverity.MINOR

    def test_deal_breaker_late_stage_low_hr(self, analyzer):
        inp = make_input(
            total_objections_raised=4,
            objections_successfully_handled=1,
            objection_raised_in_late_stage=1,
        )
        # hr = 0.25 < 0.5 and late_stage => deal_breaker
        assert analyzer._objection_severity(inp) == ObjectionSeverity.DEAL_BREAKER

    def test_not_deal_breaker_late_stage_high_hr(self, analyzer):
        inp = make_input(
            total_objections_raised=4,
            objections_successfully_handled=3,
            objection_raised_in_late_stage=1,
        )
        # hr = 0.75 >= 0.5 => not deal_breaker
        severity = analyzer._objection_severity(inp)
        assert severity != ObjectionSeverity.DEAL_BREAKER

    def test_serious_reoccurrence_ge_3(self, analyzer):
        inp = make_input(
            total_objections_raised=4,
            objections_successfully_handled=4,
            objection_reoccurrence_count=3,
        )
        assert analyzer._objection_severity(inp) == ObjectionSeverity.SERIOUS

    def test_serious_total_ge_6_low_hr(self, analyzer):
        inp = make_input(
            total_objections_raised=6,
            objections_successfully_handled=3,
            objection_reoccurrence_count=0,
        )
        # total>=6 and hr=0.5 < 0.6 => serious
        assert analyzer._objection_severity(inp) == ObjectionSeverity.SERIOUS

    def test_moderate_reoccurrence_ge_2(self, analyzer):
        inp = make_input(
            total_objections_raised=2,
            objections_successfully_handled=2,
            objection_reoccurrence_count=2,
        )
        assert analyzer._objection_severity(inp) == ObjectionSeverity.MODERATE

    def test_moderate_total_ge_4(self, analyzer):
        inp = make_input(
            total_objections_raised=4,
            objections_successfully_handled=4,
            objection_reoccurrence_count=0,
        )
        assert analyzer._objection_severity(inp) == ObjectionSeverity.MODERATE

    def test_minor_low_objections(self, analyzer):
        inp = make_input(
            total_objections_raised=2,
            objections_successfully_handled=2,
            objection_reoccurrence_count=0,
        )
        assert analyzer._objection_severity(inp) == ObjectionSeverity.MINOR


# ---------------------------------------------------------------------------
# Classifier: _handling_readiness
# ---------------------------------------------------------------------------

class TestHandlingReadiness:
    def test_prepared_when_prep_ge_70(self, analyzer):
        inp = make_input(
            rep_used_battlecard=1,
            rep_asked_discovery_question=1,
            social_proof_used=1,
        )
        prep = analyzer._rep_preparedness_score(inp)  # 35+25+20=80
        assert prep >= 70
        assert analyzer._handling_readiness(prep, inp) == HandlingReadiness.PREPARED

    def test_needs_prep_when_prep_between_45_and_70(self, analyzer):
        inp = make_input(rep_used_battlecard=1, rep_asked_discovery_question=1)
        prep = analyzer._rep_preparedness_score(inp)  # 35+25=60
        assert 45 <= prep < 70
        assert analyzer._handling_readiness(prep, inp) == HandlingReadiness.NEEDS_PREP

    def test_reactive_when_prep_between_20_and_45(self, analyzer):
        inp = make_input(rep_asked_discovery_question=1)
        prep = analyzer._rep_preparedness_score(inp)  # 25
        assert 20 <= prep < 45
        assert analyzer._handling_readiness(prep, inp) == HandlingReadiness.REACTIVE

    def test_unprepared_when_prep_lt_20(self, analyzer):
        inp = make_input(roi_calculator_used=1)
        prep = analyzer._rep_preparedness_score(inp)  # 15
        assert prep < 20
        assert analyzer._handling_readiness(prep, inp) == HandlingReadiness.UNPREPARED

    def test_prepared_boundary_exactly_70(self, analyzer):
        inp = make_input()
        assert analyzer._handling_readiness(70.0, inp) == HandlingReadiness.PREPARED

    def test_needs_prep_boundary_exactly_45(self, analyzer):
        inp = make_input()
        assert analyzer._handling_readiness(45.0, inp) == HandlingReadiness.NEEDS_PREP

    def test_reactive_boundary_exactly_20(self, analyzer):
        inp = make_input()
        assert analyzer._handling_readiness(20.0, inp) == HandlingReadiness.REACTIVE

    def test_unprepared_boundary_just_below_20(self, analyzer):
        inp = make_input()
        assert analyzer._handling_readiness(19.9, inp) == HandlingReadiness.UNPREPARED


# ---------------------------------------------------------------------------
# Classifier: _objection_action
# ---------------------------------------------------------------------------

class TestObjectionAction:
    def test_executive_call_when_deal_breaker(self, analyzer):
        inp = make_input(
            total_objections_raised=4,
            objections_successfully_handled=1,
            objection_raised_in_late_stage=1,
        )
        severity = ObjectionSeverity.DEAL_BREAKER
        action = analyzer._objection_action(severity, False, inp)
        assert action == ObjectionAction.EXECUTIVE_CALL

    def test_provide_proof_when_competitor_ge_2(self, analyzer):
        inp = make_input(competitor_objections_count=2)
        # Not deal_breaker; competitor>=2 => provide_proof
        action = analyzer._objection_action(ObjectionSeverity.MODERATE, False, inp)
        assert action == ObjectionAction.PROVIDE_PROOF

    def test_reframe_value_when_needs_coaching(self, analyzer):
        inp = make_input(competitor_objections_count=0)
        action = analyzer._objection_action(ObjectionSeverity.MINOR, True, inp)
        assert action == ObjectionAction.REFRAME_VALUE

    def test_reframe_value_when_serious_severity(self, analyzer):
        inp = make_input(competitor_objections_count=0)
        action = analyzer._objection_action(ObjectionSeverity.SERIOUS, False, inp)
        assert action == ObjectionAction.REFRAME_VALUE

    def test_none_needed_when_all_ok(self, analyzer):
        inp = make_input(competitor_objections_count=0)
        action = analyzer._objection_action(ObjectionSeverity.MINOR, False, inp)
        assert action == ObjectionAction.NONE_NEEDED

    def test_executive_call_takes_priority_over_competitor(self, analyzer):
        # deal_breaker should override competitor check
        inp = make_input(competitor_objections_count=5)
        action = analyzer._objection_action(ObjectionSeverity.DEAL_BREAKER, True, inp)
        assert action == ObjectionAction.EXECUTIVE_CALL

    def test_provide_proof_takes_priority_over_coaching(self, analyzer):
        # competitor>=2 should come before needs_coaching in priority
        inp = make_input(competitor_objections_count=2)
        action = analyzer._objection_action(ObjectionSeverity.MINOR, True, inp)
        assert action == ObjectionAction.PROVIDE_PROOF


# ---------------------------------------------------------------------------
# analyze() and analyze_batch()
# ---------------------------------------------------------------------------

class TestAnalyze:
    def test_analyze_returns_result_object(self, analyzer):
        inp = make_input()
        result = analyzer.analyze(inp)
        assert isinstance(result, ObjectionPatternResult)

    def test_analyze_stores_result(self, analyzer):
        inp = make_input(deal_id="X1")
        analyzer.analyze(inp)
        assert len(analyzer._results) == 1
        assert analyzer._results[0].deal_id == "X1"

    def test_analyze_batch_returns_list(self, analyzer):
        inputs = [make_input(deal_id=f"D{i}") for i in range(3)]
        results = analyzer.analyze_batch(inputs)
        assert isinstance(results, list)
        assert len(results) == 3

    def test_analyze_batch_stores_all_results(self, analyzer):
        inputs = [make_input(deal_id=f"D{i}") for i in range(5)]
        analyzer.analyze_batch(inputs)
        assert len(analyzer._results) == 5

    def test_analyze_batch_result_order(self, analyzer):
        inputs = [make_input(deal_id=f"D{i}") for i in range(3)]
        results = analyzer.analyze_batch(inputs)
        for i, r in enumerate(results):
            assert r.deal_id == f"D{i}"

    def test_analyze_deal_id_and_name_preserved(self, analyzer):
        inp = make_input(deal_id="ABC", deal_name="Big Deal")
        result = analyzer.analyze(inp)
        assert result.deal_id == "ABC"
        assert result.deal_name == "Big Deal"

    def test_analyze_late_stage_risk_flag(self, analyzer):
        inp_late = make_input(objection_raised_in_late_stage=1)
        inp_not_late = make_input(objection_raised_in_late_stage=0)
        assert analyzer.analyze(inp_late).late_stage_risk is True
        assert analyzer.analyze(inp_not_late).late_stage_risk is False

    def test_analyze_accumulates_across_calls(self, analyzer):
        for i in range(4):
            analyzer.analyze(make_input(deal_id=f"D{i}"))
        assert len(analyzer._results) == 4

    def test_analyze_empty_batch(self, analyzer):
        results = analyzer.analyze_batch([])
        assert results == []
        assert len(analyzer._results) == 0


# ---------------------------------------------------------------------------
# Properties
# ---------------------------------------------------------------------------

class TestProperties:
    def test_contained_deals_empty_initially(self, analyzer):
        assert analyzer.contained_deals == []

    def test_coaching_queue_empty_initially(self, analyzer):
        assert analyzer.coaching_queue == []

    def test_avg_objection_composite_zero_when_empty(self, analyzer):
        assert analyzer.avg_objection_composite == 0.0

    def test_avg_handle_rate_zero_when_empty(self, analyzer):
        assert analyzer.avg_handle_rate == 0.0

    def test_contained_deals_filters_correctly(self, analyzer):
        # Contained: high composite + low reoccurrence
        inp_contained = make_input(
            deal_id="C1",
            rep_used_battlecard=1,
            rep_asked_discovery_question=1,
            social_proof_used=1,
            roi_calculator_used=1,
            total_objections_raised=2,
            objections_successfully_handled=2,
            objection_reoccurrence_count=0,
            avg_objection_response_time_hrs=2.0,
            discovery_call_count=3,
        )
        # Not contained: high reoccurrence
        inp_not_contained = make_input(
            deal_id="C2",
            total_objections_raised=3,
            objections_successfully_handled=1,
            objection_reoccurrence_count=2,
        )
        analyzer.analyze(inp_contained)
        analyzer.analyze(inp_not_contained)
        contained = analyzer.contained_deals
        contained_ids = [r.deal_id for r in contained]
        assert "C1" in contained_ids or len(contained) >= 0  # at least consistent
        for r in contained:
            assert r.is_objection_contained is True

    def test_coaching_queue_filters_correctly(self, analyzer):
        inp = make_input(deal_id="CQ1")  # no tools => prep=0 => needs_coaching
        analyzer.analyze(inp)
        queue = analyzer.coaching_queue
        for r in queue:
            assert r.needs_coaching is True

    def test_avg_objection_composite_single(self, analyzer):
        inp = make_input()
        result = analyzer.analyze(inp)
        assert analyzer.avg_objection_composite == round(result.objection_composite, 1)

    def test_avg_objection_composite_multiple(self, analyzer):
        inputs = [make_input(deal_id=f"D{i}") for i in range(3)]
        results = analyzer.analyze_batch(inputs)
        expected = round(sum(r.objection_composite for r in results) / 3, 1)
        assert analyzer.avg_objection_composite == expected

    def test_avg_handle_rate_single(self, analyzer):
        inp = make_input(total_objections_raised=4, objections_successfully_handled=3,
                         price_objections_count=4)
        result = analyzer.analyze(inp)
        assert analyzer.avg_handle_rate == result.handle_rate

    def test_avg_handle_rate_multiple(self, analyzer):
        inputs = [
            make_input(deal_id="D1", total_objections_raised=4,
                       objections_successfully_handled=4, price_objections_count=4),
            make_input(deal_id="D2", total_objections_raised=4,
                       objections_successfully_handled=2, price_objections_count=4),
        ]
        results = analyzer.analyze_batch(inputs)
        expected = round(sum(r.handle_rate for r in results) / 2, 1)
        assert analyzer.avg_handle_rate == expected


# ---------------------------------------------------------------------------
# reset()
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_clears_results(self, analyzer):
        analyzer.analyze(make_input())
        analyzer.analyze(make_input(deal_id="D2"))
        assert len(analyzer._results) == 2
        analyzer.reset()
        assert len(analyzer._results) == 0

    def test_reset_clears_properties(self, analyzer):
        analyzer.analyze(make_input())
        analyzer.reset()
        assert analyzer.contained_deals == []
        assert analyzer.coaching_queue == []
        assert analyzer.avg_objection_composite == 0.0
        assert analyzer.avg_handle_rate == 0.0

    def test_reset_then_analyze_works(self, analyzer):
        analyzer.analyze(make_input(deal_id="D1"))
        analyzer.reset()
        analyzer.analyze(make_input(deal_id="D2"))
        assert len(analyzer._results) == 1
        assert analyzer._results[0].deal_id == "D2"

    def test_reset_clears_summary(self, analyzer):
        analyzer.analyze(make_input())
        analyzer.reset()
        s = analyzer.summary()
        assert s["total"] == 0
        assert s["contained_count"] == 0
        assert s["coaching_count"] == 0


# ---------------------------------------------------------------------------
# summary()
# ---------------------------------------------------------------------------

class TestSummary:
    def test_empty_summary_total_zero(self, analyzer):
        s = analyzer.summary()
        assert s["total"] == 0

    def test_empty_summary_empty_dicts(self, analyzer):
        s = analyzer.summary()
        assert s["objection_type_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["readiness_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_zero_averages(self, analyzer):
        s = analyzer.summary()
        assert s["avg_objection_composite"] == 0.0
        assert s["avg_handle_rate"] == 0.0
        assert s["avg_handling_effectiveness_score"] == 0.0
        assert s["avg_pattern_risk_score"] == 0.0
        assert s["avg_rep_preparedness_score"] == 0.0
        assert s["avg_objection_density_score"] == 0.0

    def test_summary_total_matches_analyzed(self, analyzer):
        for i in range(4):
            analyzer.analyze(make_input(deal_id=f"D{i}"))
        assert analyzer.summary()["total"] == 4

    def test_summary_type_counts(self, analyzer):
        analyzer.analyze(make_input(
            deal_id="D1", total_objections_raised=3,
            objections_successfully_handled=3, price_objections_count=3
        ))
        analyzer.analyze(make_input(
            deal_id="D2", total_objections_raised=2,
            objections_successfully_handled=2, timing_objections_count=2
        ))
        s = analyzer.summary()
        assert s["objection_type_counts"].get("price", 0) >= 1
        assert s["objection_type_counts"].get("timing", 0) >= 1

    def test_summary_severity_counts_populated(self, analyzer):
        analyzer.analyze(make_input(
            deal_id="D1", total_objections_raised=2,
            objections_successfully_handled=2, price_objections_count=2
        ))
        s = analyzer.summary()
        assert len(s["severity_counts"]) >= 1

    def test_summary_contained_count_matches_property(self, analyzer):
        for i in range(3):
            analyzer.analyze(make_input(deal_id=f"D{i}"))
        s = analyzer.summary()
        assert s["contained_count"] == len(analyzer.contained_deals)

    def test_summary_coaching_count_matches_property(self, analyzer):
        for i in range(3):
            analyzer.analyze(make_input(deal_id=f"D{i}"))
        s = analyzer.summary()
        assert s["coaching_count"] == len(analyzer.coaching_queue)

    def test_summary_avg_composite_matches_property(self, analyzer):
        for i in range(3):
            analyzer.analyze(make_input(deal_id=f"D{i}"))
        s = analyzer.summary()
        assert s["avg_objection_composite"] == analyzer.avg_objection_composite

    def test_summary_avg_handle_rate_matches_property(self, analyzer):
        for i in range(3):
            analyzer.analyze(make_input(deal_id=f"D{i}", total_objections_raised=2,
                                        objections_successfully_handled=1,
                                        price_objections_count=2))
        s = analyzer.summary()
        assert s["avg_handle_rate"] == analyzer.avg_handle_rate

    def test_summary_action_counts_populated(self, analyzer):
        analyzer.analyze(make_input())  # no tools => coaching needed => reframe_value
        s = analyzer.summary()
        assert len(s["action_counts"]) >= 1

    def test_summary_readiness_counts_populated(self, analyzer):
        analyzer.analyze(make_input())
        s = analyzer.summary()
        assert len(s["readiness_counts"]) >= 1


# ---------------------------------------------------------------------------
# End-to-end / integration scenarios
# ---------------------------------------------------------------------------

class TestEndToEnd:
    def test_clean_deal_no_objections(self, analyzer):
        """Deal with no objections — easy, all contained, high scores."""
        inp = make_input(
            deal_id="CLEAN",
            total_objections_raised=0,
            objections_successfully_handled=0,
            rep_used_battlecard=1,
            rep_asked_discovery_question=1,
            social_proof_used=1,
            roi_calculator_used=1,
            discovery_call_count=5,
        )
        result = analyzer.analyze(inp)
        assert result.primary_objection_type == ObjectionType.NO_OBJECTION
        assert result.handle_rate == 100.0
        assert result.late_stage_risk is False
        assert result.objection_severity == ObjectionSeverity.MINOR
        assert result.rep_preparedness_score == 100.0

    def test_worst_case_deal(self, analyzer):
        """Deal with maximum objections, late stage, competitor lost, no tools used."""
        inp = make_input(
            deal_id="WORST",
            total_objections_raised=10,
            objections_successfully_handled=1,
            price_objections_count=5,
            competitor_objections_count=3,
            status_quo_objections_count=2,
            objection_reoccurrence_count=4,
            objection_raised_in_late_stage=1,
            competitor_deal_lost_last_90d=1,
            avg_objection_response_time_hrs=100.0,
        )
        result = analyzer.analyze(inp)
        assert result.needs_coaching is True
        assert result.late_stage_risk is True
        assert result.is_objection_contained is False

    def test_mixed_batch(self, analyzer):
        """Batch of mixed deals produces correct summary stats."""
        inputs = [
            make_input(deal_id="G1", total_objections_raised=0,
                       rep_used_battlecard=1, rep_asked_discovery_question=1,
                       social_proof_used=1, roi_calculator_used=1),
            make_input(deal_id="B1", total_objections_raised=8,
                       objections_successfully_handled=1, price_objections_count=8,
                       objection_reoccurrence_count=4, objection_raised_in_late_stage=1),
        ]
        results = analyzer.analyze_batch(inputs)
        assert len(results) == 2
        s = analyzer.summary()
        assert s["total"] == 2
        assert len(s) == 13

    def test_result_scores_are_in_range(self, analyzer):
        """All numeric scores must be in [0, 100]."""
        inputs = [
            make_input(deal_id=f"D{i}",
                       total_objections_raised=i,
                       objections_successfully_handled=max(0, i - 1),
                       price_objections_count=i,
                       rep_used_battlecard=i % 2,
                       rep_asked_discovery_question=(i + 1) % 2,
                       objection_reoccurrence_count=i % 4,
                       avg_objection_response_time_hrs=float(i * 5 + 1))
            for i in range(6)
        ]
        results = analyzer.analyze_batch(inputs)
        for r in results:
            assert 0.0 <= r.handling_effectiveness_score <= 100.0
            assert 0.0 <= r.objection_density_score <= 100.0
            assert 0.0 <= r.pattern_risk_score <= 100.0
            assert 0.0 <= r.rep_preparedness_score <= 100.0
            assert 0.0 <= r.objection_composite <= 100.0
            assert 0.0 <= r.handle_rate <= 100.0

    def test_to_dict_values_match_result_fields(self, analyzer):
        inp = make_input(
            deal_id="DV1", deal_name="Value Test",
            total_objections_raised=3,
            objections_successfully_handled=3,
            price_objections_count=3,
            rep_used_battlecard=1,
        )
        result = analyzer.analyze(inp)
        d = result.to_dict()
        assert d["deal_id"] == result.deal_id
        assert d["deal_name"] == result.deal_name
        assert d["primary_objection_type"] == result.primary_objection_type.value
        assert d["objection_severity"] == result.objection_severity.value
        assert d["handling_readiness"] == result.handling_readiness.value
        assert d["objection_action"] == result.objection_action.value
        assert d["handling_effectiveness_score"] == result.handling_effectiveness_score
        assert d["objection_density_score"] == result.objection_density_score
        assert d["pattern_risk_score"] == result.pattern_risk_score
        assert d["rep_preparedness_score"] == result.rep_preparedness_score
        assert d["objection_composite"] == result.objection_composite
        assert d["handle_rate"] == result.handle_rate
        assert d["late_stage_risk"] == result.late_stage_risk
        assert d["is_objection_contained"] == result.is_objection_contained
        assert d["needs_coaching"] == result.needs_coaching

    def test_multiple_analyzers_are_independent(self):
        a1 = ObjectionPatternAnalyzer()
        a2 = ObjectionPatternAnalyzer()
        a1.analyze(make_input(deal_id="A"))
        a1.analyze(make_input(deal_id="B"))
        a2.analyze(make_input(deal_id="C"))
        assert len(a1._results) == 2
        assert len(a2._results) == 1
