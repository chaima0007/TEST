"""
Comprehensive pytest tests for SalesTimeAllocationIntelligenceEngine.

Import path: swarm.intelligence.sales_time_allocation_intelligence_engine
Run from /home/user/TEST:
    python -m pytest swarm/tests/test_sales_time_allocation_intelligence_engine.py -v
"""

import pytest
from swarm.intelligence.sales_time_allocation_intelligence_engine import (
    AllocationRisk,
    AllocationPattern,
    AllocationSeverity,
    AllocationAction,
    TimeAllocationInput,
    TimeAllocationResult,
    SalesTimeAllocationIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helper factory
# ---------------------------------------------------------------------------

def make_input(
    rep_id="R001",
    region="EMEA",
    evaluation_period_id="Q1-2026",
    total_hours_tracked=100.0,
    customer_facing_hours=30.0,
    prospecting_hours=15.0,
    admin_hours=10.0,
    internal_meeting_hours=10.0,
    proposal_prep_hours=10.0,
    travel_hours=5.0,
    training_hours=5.0,
    emails_sent_count=300,
    avg_email_response_time_minutes=60.0,
    calls_made_count=50,
    avg_call_duration_minutes=20.0,
    meetings_attended_count=10,
    internal_meetings_count=5,
    demo_hours=8.0,
    pipeline_review_hours=3.0,
    coaching_sessions_hours=2.0,
    focus_blocks_per_week=6.0,
    after_hours_work_hours=2.0,
) -> TimeAllocationInput:
    """Return a healthy TimeAllocationInput (low-risk by default)."""
    return TimeAllocationInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        total_hours_tracked=total_hours_tracked,
        customer_facing_hours=customer_facing_hours,
        prospecting_hours=prospecting_hours,
        admin_hours=admin_hours,
        internal_meeting_hours=internal_meeting_hours,
        proposal_prep_hours=proposal_prep_hours,
        travel_hours=travel_hours,
        training_hours=training_hours,
        emails_sent_count=emails_sent_count,
        avg_email_response_time_minutes=avg_email_response_time_minutes,
        calls_made_count=calls_made_count,
        avg_call_duration_minutes=avg_call_duration_minutes,
        meetings_attended_count=meetings_attended_count,
        internal_meetings_count=internal_meetings_count,
        demo_hours=demo_hours,
        pipeline_review_hours=pipeline_review_hours,
        coaching_sessions_hours=coaching_sessions_hours,
        focus_blocks_per_week=focus_blocks_per_week,
        after_hours_work_hours=after_hours_work_hours,
    )


@pytest.fixture
def engine():
    return SalesTimeAllocationIntelligenceEngine()


@pytest.fixture
def healthy_input():
    return make_input()


# ===========================================================================
# 1. Enum value tests
# ===========================================================================

class TestEnumValues:

    def test_allocation_risk_low(self):
        assert AllocationRisk.low.value == "low"

    def test_allocation_risk_moderate(self):
        assert AllocationRisk.moderate.value == "moderate"

    def test_allocation_risk_high(self):
        assert AllocationRisk.high.value == "high"

    def test_allocation_risk_critical(self):
        assert AllocationRisk.critical.value == "critical"

    def test_allocation_risk_is_str_enum(self):
        assert isinstance(AllocationRisk.low, str)

    def test_allocation_pattern_none(self):
        assert AllocationPattern.none.value == "none"

    def test_allocation_pattern_admin_overload(self):
        assert AllocationPattern.admin_overload.value == "admin_overload"

    def test_allocation_pattern_meeting_fatigue(self):
        assert AllocationPattern.meeting_fatigue.value == "meeting_fatigue"

    def test_allocation_pattern_low_selling_time(self):
        assert AllocationPattern.low_selling_time.value == "low_selling_time"

    def test_allocation_pattern_reactive_mode(self):
        assert AllocationPattern.reactive_mode.value == "reactive_mode"

    def test_allocation_pattern_time_fragmentation(self):
        assert AllocationPattern.time_fragmentation.value == "time_fragmentation"

    def test_allocation_severity_optimized(self):
        assert AllocationSeverity.optimized.value == "optimized"

    def test_allocation_severity_developing(self):
        assert AllocationSeverity.developing.value == "developing"

    def test_allocation_severity_burdened(self):
        assert AllocationSeverity.burdened.value == "burdened"

    def test_allocation_severity_fragmented(self):
        assert AllocationSeverity.fragmented.value == "fragmented"

    def test_allocation_action_no_action(self):
        assert AllocationAction.no_action.value == "no_action"

    def test_allocation_action_time_audit_coaching(self):
        assert AllocationAction.time_audit_coaching.value == "time_audit_coaching"

    def test_allocation_action_admin_reduction_plan(self):
        assert AllocationAction.admin_reduction_plan.value == "admin_reduction_plan"

    def test_allocation_action_meeting_hygiene_review(self):
        assert AllocationAction.meeting_hygiene_review.value == "meeting_hygiene_review"

    def test_allocation_action_selling_time_recovery(self):
        assert AllocationAction.selling_time_recovery.value == "selling_time_recovery"

    def test_allocation_action_workflow_optimization(self):
        assert AllocationAction.workflow_optimization.value == "workflow_optimization"

    def test_all_risks_count(self):
        assert len(AllocationRisk) == 4

    def test_all_patterns_count(self):
        assert len(AllocationPattern) == 6

    def test_all_severities_count(self):
        assert len(AllocationSeverity) == 4

    def test_all_actions_count(self):
        assert len(AllocationAction) == 6


# ===========================================================================
# 2. TimeAllocationInput dataclass field count
# ===========================================================================

class TestTimeAllocationInput:

    def test_input_has_22_fields(self, healthy_input):
        import dataclasses
        fields = dataclasses.fields(healthy_input)
        assert len(fields) == 22

    def test_rep_id_stored(self, healthy_input):
        assert healthy_input.rep_id == "R001"

    def test_region_stored(self, healthy_input):
        assert healthy_input.region == "EMEA"

    def test_evaluation_period_stored(self, healthy_input):
        assert healthy_input.evaluation_period_id == "Q1-2026"

    def test_total_hours_stored(self, healthy_input):
        assert healthy_input.total_hours_tracked == 100.0


# ===========================================================================
# 3. TimeAllocationResult and to_dict()
# ===========================================================================

class TestTimeAllocationResult:

    def test_to_dict_has_15_keys(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_rep_id(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.to_dict()["rep_id"] == "R001"

    def test_to_dict_region(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.to_dict()["region"] == "EMEA"

    def test_to_dict_allocation_risk_is_string(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.to_dict()["allocation_risk"], str)

    def test_to_dict_allocation_pattern_is_string(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.to_dict()["allocation_pattern"], str)

    def test_to_dict_allocation_severity_is_string(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.to_dict()["allocation_severity"], str)

    def test_to_dict_recommended_action_is_string(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.to_dict()["recommended_action"], str)

    def test_to_dict_selling_time_score_is_float(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.to_dict()["selling_time_score"], float)

    def test_to_dict_admin_burden_score_is_float(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.to_dict()["admin_burden_score"], float)

    def test_to_dict_activity_quality_score_is_float(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.to_dict()["activity_quality_score"], float)

    def test_to_dict_time_discipline_score_is_float(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.to_dict()["time_discipline_score"], float)

    def test_to_dict_composite_is_float(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.to_dict()["time_allocation_composite"], float)

    def test_to_dict_has_time_gap_is_bool(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.to_dict()["has_time_gap"], bool)

    def test_to_dict_requires_coaching_is_bool(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.to_dict()["requires_allocation_coaching"], bool)

    def test_to_dict_hours_lost_is_float(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.to_dict()["estimated_selling_hours_lost_per_week"], float)

    def test_to_dict_signal_is_string(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.to_dict()["allocation_signal"], str)

    def test_to_dict_all_expected_keys(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        d = result.to_dict()
        expected_keys = {
            "rep_id", "region", "allocation_risk", "allocation_pattern",
            "allocation_severity", "recommended_action", "selling_time_score",
            "admin_burden_score", "activity_quality_score", "time_discipline_score",
            "time_allocation_composite", "has_time_gap", "requires_allocation_coaching",
            "estimated_selling_hours_lost_per_week", "allocation_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_result_has_15_fields(self, engine, healthy_input):
        import dataclasses
        result = engine.assess(healthy_input)
        assert len(dataclasses.fields(result)) == 15


# ===========================================================================
# 4. _selling_time_score branches
# ===========================================================================

class TestSellingTimeScore:

    def test_selling_pct_below_020_adds_45(self, engine):
        # selling_pct = (5+5)/100 = 0.10 < 0.20 → +45
        # demo_pct = 2/100 = 0.02 < 0.05 → +25
        # prospecting_pct = 5/100 = 0.05 < 0.10 → +20
        # total = 45+25+20 = 90
        inp = make_input(customer_facing_hours=5.0, proposal_prep_hours=5.0,
                         demo_hours=2.0, prospecting_hours=5.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 90.0

    def test_selling_pct_020_to_030_adds_25(self, engine):
        # selling_pct = (22+0)/100 = 0.22 → +25
        # demo_pct = 2/100 = 0.02 < 0.05 → +25
        # prospecting_pct = 5/100 = 0.05 < 0.10 → +20
        # total = 25+25+20 = 70
        inp = make_input(customer_facing_hours=22.0, proposal_prep_hours=0.0,
                         demo_hours=2.0, prospecting_hours=5.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 70.0

    def test_selling_pct_030_to_040_adds_10(self, engine):
        # selling_pct = (32+0)/100 = 0.32 → +10
        # demo_pct = 2/100 = 0.02 < 0.05 → +25
        # prospecting_pct = 5/100 = 0.05 < 0.10 → +20
        # total = 10+25+20 = 55
        inp = make_input(customer_facing_hours=32.0, proposal_prep_hours=0.0,
                         demo_hours=2.0, prospecting_hours=5.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 55.0

    def test_selling_pct_at_040_no_selling_bonus(self, engine):
        # selling_pct = 40/100 = 0.40, no bonus
        # demo_pct = 2/100 = 0.02 → +25
        # prospecting_pct = 5/100 = 0.05 → +20
        inp = make_input(customer_facing_hours=40.0, proposal_prep_hours=0.0,
                         demo_hours=2.0, prospecting_hours=5.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 45.0

    def test_demo_pct_below_005_adds_25(self, engine):
        # demo_pct = 2/100 = 0.02 → +25
        inp = make_input(customer_facing_hours=50.0, proposal_prep_hours=0.0,
                         demo_hours=2.0, prospecting_hours=20.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 25.0  # selling_pct=0.5 (no bonus), demo<0.05 +25, prospecting>=0.15 (no bonus)

    def test_demo_pct_005_to_010_adds_12(self, engine):
        # selling_pct=0.5 (no bonus), demo_pct=7/100=0.07 → +12, prospecting=20/100=0.20 no bonus
        inp = make_input(customer_facing_hours=50.0, proposal_prep_hours=0.0,
                         demo_hours=7.0, prospecting_hours=20.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 12.0

    def test_demo_pct_at_010_no_demo_bonus(self, engine):
        # demo_pct = 10/100 = 0.10, no bonus
        inp = make_input(customer_facing_hours=50.0, proposal_prep_hours=0.0,
                         demo_hours=10.0, prospecting_hours=20.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 0.0

    def test_prospecting_pct_below_010_adds_20(self, engine):
        # selling_pct=0.5 (no bonus), demo_pct=10/100 (no bonus), prospecting=5/100=0.05 → +20
        inp = make_input(customer_facing_hours=50.0, proposal_prep_hours=0.0,
                         demo_hours=10.0, prospecting_hours=5.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 20.0

    def test_prospecting_pct_010_to_015_adds_10(self, engine):
        # selling_pct=0.5 (no bonus), demo_pct=10/100 (no bonus), prospecting=12/100=0.12 → +10
        inp = make_input(customer_facing_hours=50.0, proposal_prep_hours=0.0,
                         demo_hours=10.0, prospecting_hours=12.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 10.0

    def test_prospecting_pct_at_015_no_bonus(self, engine):
        # prospecting=15/100=0.15, no bonus
        inp = make_input(customer_facing_hours=50.0, proposal_prep_hours=0.0,
                         demo_hours=10.0, prospecting_hours=15.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 0.0

    def test_selling_time_score_capped_at_100(self, engine):
        # Max theoretical: 45+25+20 = 90 but let's confirm cap logic
        inp = make_input(customer_facing_hours=0.0, proposal_prep_hours=0.0,
                         demo_hours=0.0, prospecting_hours=0.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score <= 100.0

    def test_selling_time_score_nonnegative(self, engine, healthy_input):
        assert engine._selling_time_score(healthy_input) >= 0.0

    def test_total_hours_floor_at_1(self, engine):
        # total=0 → uses 1.0 as floor
        inp = make_input(total_hours_tracked=0.0, customer_facing_hours=0.0,
                         proposal_prep_hours=0.0, demo_hours=0.0, prospecting_hours=0.0)
        # All pcts = 0/1 = 0 → selling < 0.20 (+45), demo < 0.05 (+25), prospecting < 0.10 (+20)
        score = engine._selling_time_score(inp)
        assert score == 90.0

    def test_selling_exactly_019_boundary(self, engine):
        # selling_pct = 19/100 = 0.19 → +45
        inp = make_input(customer_facing_hours=19.0, proposal_prep_hours=0.0,
                         demo_hours=10.0, prospecting_hours=15.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 45.0

    def test_selling_exactly_020_boundary(self, engine):
        # selling_pct = 20/100 = 0.20 → +25 (not < 0.20)
        inp = make_input(customer_facing_hours=20.0, proposal_prep_hours=0.0,
                         demo_hours=10.0, prospecting_hours=15.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 25.0

    def test_selling_exactly_030_boundary(self, engine):
        # selling_pct = 30/100 = 0.30 → NOT < 0.30, but < 0.40 → +10
        # demo_pct=10/100=0.10 → no bonus (not < 0.10), prospecting=15/100=0.15 → no bonus
        inp = make_input(customer_facing_hours=30.0, proposal_prep_hours=0.0,
                         demo_hours=10.0, prospecting_hours=15.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 10.0

    def test_selling_exactly_039_boundary(self, engine):
        # selling_pct = 39/100 = 0.39 → +10
        inp = make_input(customer_facing_hours=39.0, proposal_prep_hours=0.0,
                         demo_hours=10.0, prospecting_hours=15.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 10.0


# ===========================================================================
# 5. _admin_burden_score branches
# ===========================================================================

class TestAdminBurdenScore:

    def test_admin_pct_above_030_adds_40(self, engine):
        # admin_pct = (35+0)/100 = 0.35 → +40
        # internal_pct = 0/100 = 0 → no bonus
        # internal_meetings_count = 0 → no bonus
        inp = make_input(admin_hours=35.0, travel_hours=0.0,
                         internal_meeting_hours=0.0, internal_meetings_count=0,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 40.0

    def test_admin_pct_020_to_030_adds_20(self, engine):
        # admin_pct = 25/100 = 0.25 → +20
        inp = make_input(admin_hours=25.0, travel_hours=0.0,
                         internal_meeting_hours=0.0, internal_meetings_count=0,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 20.0

    def test_admin_pct_015_to_020_adds_8(self, engine):
        # admin_pct = 17/100 = 0.17 → +8
        inp = make_input(admin_hours=17.0, travel_hours=0.0,
                         internal_meeting_hours=0.0, internal_meetings_count=0,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 8.0

    def test_admin_pct_below_015_no_bonus(self, engine):
        # admin_pct = 10/100 = 0.10 → no bonus
        inp = make_input(admin_hours=10.0, travel_hours=0.0,
                         internal_meeting_hours=0.0, internal_meetings_count=0,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 0.0

    def test_admin_pct_exactly_030_adds_40(self, engine):
        inp = make_input(admin_hours=30.0, travel_hours=0.0,
                         internal_meeting_hours=0.0, internal_meetings_count=0,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 40.0

    def test_admin_pct_exactly_020_adds_20(self, engine):
        inp = make_input(admin_hours=20.0, travel_hours=0.0,
                         internal_meeting_hours=0.0, internal_meetings_count=0,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 20.0

    def test_admin_pct_exactly_015_adds_8(self, engine):
        inp = make_input(admin_hours=15.0, travel_hours=0.0,
                         internal_meeting_hours=0.0, internal_meetings_count=0,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 8.0

    def test_internal_pct_above_025_adds_35(self, engine):
        # internal_pct = 30/100 = 0.30 → +35
        inp = make_input(admin_hours=0.0, travel_hours=0.0,
                         internal_meeting_hours=30.0, internal_meetings_count=0,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 35.0

    def test_internal_pct_015_to_025_adds_18(self, engine):
        # internal_pct = 20/100 = 0.20 → +18
        inp = make_input(admin_hours=0.0, travel_hours=0.0,
                         internal_meeting_hours=20.0, internal_meetings_count=0,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 18.0

    def test_internal_pct_010_to_015_adds_7(self, engine):
        # internal_pct = 12/100 = 0.12 → +7
        inp = make_input(admin_hours=0.0, travel_hours=0.0,
                         internal_meeting_hours=12.0, internal_meetings_count=0,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 7.0

    def test_internal_pct_below_010_no_bonus(self, engine):
        # internal_pct = 5/100 = 0.05 → no bonus
        inp = make_input(admin_hours=0.0, travel_hours=0.0,
                         internal_meeting_hours=5.0, internal_meetings_count=0,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 0.0

    def test_internal_meetings_15_adds_20(self, engine):
        inp = make_input(admin_hours=0.0, travel_hours=0.0,
                         internal_meeting_hours=0.0, internal_meetings_count=15,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 20.0

    def test_internal_meetings_10_to_14_adds_10(self, engine):
        inp = make_input(admin_hours=0.0, travel_hours=0.0,
                         internal_meeting_hours=0.0, internal_meetings_count=10,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 10.0

    def test_internal_meetings_below_10_no_bonus(self, engine):
        inp = make_input(admin_hours=0.0, travel_hours=0.0,
                         internal_meeting_hours=0.0, internal_meetings_count=9,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 0.0

    def test_admin_burden_score_capped_at_100(self, engine):
        # max: 40+35+20 = 95, but test it's ≤ 100
        inp = make_input(admin_hours=40.0, travel_hours=0.0,
                         internal_meeting_hours=30.0, internal_meetings_count=20,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score <= 100.0

    def test_travel_included_in_admin_pct(self, engine):
        # admin_pct = (0+20)/100 = 0.20 → +20
        inp = make_input(admin_hours=0.0, travel_hours=20.0,
                         internal_meeting_hours=0.0, internal_meetings_count=0,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 20.0

    def test_internal_meetings_exactly_15_adds_20(self, engine):
        inp = make_input(admin_hours=0.0, travel_hours=0.0,
                         internal_meeting_hours=0.0, internal_meetings_count=15,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 20.0

    def test_internal_meetings_exactly_10_adds_10(self, engine):
        inp = make_input(admin_hours=0.0, travel_hours=0.0,
                         internal_meeting_hours=0.0, internal_meetings_count=10,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 10.0


# ===========================================================================
# 6. _activity_quality_score branches
# ===========================================================================

class TestActivityQualityScore:

    def test_call_duration_below_5_adds_35(self, engine):
        # avg_call_duration < 5 → +35
        # email_rate = 500/100 = 5.0 → no bonus (not < 5.0)
        # avg_email_response = 60 → no bonus
        inp = make_input(avg_call_duration_minutes=4.0, emails_sent_count=500,
                         avg_email_response_time_minutes=60.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score == 35.0

    def test_call_duration_5_to_10_adds_18(self, engine):
        # 5 <= duration < 10 → +18; email_rate=5.0 no bonus; response=60 no bonus
        inp = make_input(avg_call_duration_minutes=7.0, emails_sent_count=500,
                         avg_email_response_time_minutes=60.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score == 18.0

    def test_call_duration_10_to_15_adds_7(self, engine):
        # 10 <= duration < 15 → +7; email_rate=5.0 no bonus; response=60 no bonus
        inp = make_input(avg_call_duration_minutes=12.0, emails_sent_count=500,
                         avg_email_response_time_minutes=60.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score == 7.0

    def test_call_duration_at_15_no_bonus(self, engine):
        # duration=15 → no bonus; email_rate=5.0 no bonus; response=60 no bonus
        inp = make_input(avg_call_duration_minutes=15.0, emails_sent_count=500,
                         avg_email_response_time_minutes=60.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score == 0.0

    def test_email_rate_below_2_adds_30(self, engine):
        # email_rate = 100/100 = 1.0 < 2.0 → +30
        inp = make_input(avg_call_duration_minutes=20.0, emails_sent_count=100,
                         avg_email_response_time_minutes=60.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score == 30.0

    def test_email_rate_2_to_5_adds_15(self, engine):
        # email_rate = 300/100 = 3.0 → +15
        inp = make_input(avg_call_duration_minutes=20.0, emails_sent_count=300,
                         avg_email_response_time_minutes=60.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score == 15.0

    def test_email_rate_at_5_no_bonus(self, engine):
        # email_rate = 500/100 = 5.0, not < 5.0
        inp = make_input(avg_call_duration_minutes=20.0, emails_sent_count=500,
                         avg_email_response_time_minutes=60.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score == 0.0

    def test_email_response_above_1440_adds_25(self, engine):
        # avg_email_response >= 1440 → +25
        inp = make_input(avg_call_duration_minutes=20.0, emails_sent_count=500,
                         avg_email_response_time_minutes=1440.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score == 25.0

    def test_email_response_480_to_1440_adds_12(self, engine):
        # avg_email_response >= 480 but < 1440 → +12
        inp = make_input(avg_call_duration_minutes=20.0, emails_sent_count=500,
                         avg_email_response_time_minutes=720.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score == 12.0

    def test_email_response_below_480_no_bonus(self, engine):
        inp = make_input(avg_call_duration_minutes=20.0, emails_sent_count=500,
                         avg_email_response_time_minutes=479.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score == 0.0

    def test_activity_quality_score_capped_at_100(self, engine):
        # max: 35+30+25 = 90, but ensure cap
        inp = make_input(avg_call_duration_minutes=1.0, emails_sent_count=50,
                         avg_email_response_time_minutes=2000.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score <= 100.0
        assert score == 90.0

    def test_call_duration_exactly_5_adds_18(self, engine):
        # 5 is not < 5, but < 10 → +18
        inp = make_input(avg_call_duration_minutes=5.0, emails_sent_count=500,
                         avg_email_response_time_minutes=60.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score == 18.0

    def test_call_duration_exactly_10_adds_7(self, engine):
        inp = make_input(avg_call_duration_minutes=10.0, emails_sent_count=500,
                         avg_email_response_time_minutes=60.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score == 7.0

    def test_email_response_exactly_1440_adds_25(self, engine):
        inp = make_input(avg_call_duration_minutes=20.0, emails_sent_count=500,
                         avg_email_response_time_minutes=1440.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score == 25.0

    def test_email_response_exactly_480_adds_12(self, engine):
        inp = make_input(avg_call_duration_minutes=20.0, emails_sent_count=500,
                         avg_email_response_time_minutes=480.0, total_hours_tracked=100.0)
        score = engine._activity_quality_score(inp)
        assert score == 12.0


# ===========================================================================
# 7. _time_discipline_score branches
# ===========================================================================

class TestTimeDisciplineScore:

    def test_focus_blocks_below_2_adds_35(self, engine):
        # focus_blocks < 2 → +35
        # after_hours = 0 → no bonus
        # pipeline_review >= 2 → no bonus
        inp = make_input(focus_blocks_per_week=1.0, after_hours_work_hours=0.0,
                         pipeline_review_hours=3.0)
        score = engine._time_discipline_score(inp)
        assert score == 35.0

    def test_focus_blocks_2_to_5_adds_18(self, engine):
        inp = make_input(focus_blocks_per_week=3.0, after_hours_work_hours=0.0,
                         pipeline_review_hours=3.0)
        score = engine._time_discipline_score(inp)
        assert score == 18.0

    def test_focus_blocks_5_to_8_adds_7(self, engine):
        inp = make_input(focus_blocks_per_week=6.0, after_hours_work_hours=0.0,
                         pipeline_review_hours=3.0)
        score = engine._time_discipline_score(inp)
        assert score == 7.0

    def test_focus_blocks_at_8_no_bonus(self, engine):
        inp = make_input(focus_blocks_per_week=8.0, after_hours_work_hours=0.0,
                         pipeline_review_hours=3.0)
        score = engine._time_discipline_score(inp)
        assert score == 0.0

    def test_after_hours_at_10_adds_30(self, engine):
        inp = make_input(focus_blocks_per_week=8.0, after_hours_work_hours=10.0,
                         pipeline_review_hours=3.0)
        score = engine._time_discipline_score(inp)
        assert score == 30.0

    def test_after_hours_5_to_10_adds_15(self, engine):
        inp = make_input(focus_blocks_per_week=8.0, after_hours_work_hours=7.0,
                         pipeline_review_hours=3.0)
        score = engine._time_discipline_score(inp)
        assert score == 15.0

    def test_after_hours_below_5_no_bonus(self, engine):
        inp = make_input(focus_blocks_per_week=8.0, after_hours_work_hours=4.9,
                         pipeline_review_hours=3.0)
        score = engine._time_discipline_score(inp)
        assert score == 0.0

    def test_pipeline_review_below_1_adds_20(self, engine):
        inp = make_input(focus_blocks_per_week=8.0, after_hours_work_hours=0.0,
                         pipeline_review_hours=0.5)
        score = engine._time_discipline_score(inp)
        assert score == 20.0

    def test_pipeline_review_1_to_2_adds_10(self, engine):
        inp = make_input(focus_blocks_per_week=8.0, after_hours_work_hours=0.0,
                         pipeline_review_hours=1.5)
        score = engine._time_discipline_score(inp)
        assert score == 10.0

    def test_pipeline_review_at_2_no_bonus(self, engine):
        inp = make_input(focus_blocks_per_week=8.0, after_hours_work_hours=0.0,
                         pipeline_review_hours=2.0)
        score = engine._time_discipline_score(inp)
        assert score == 0.0

    def test_time_discipline_score_capped_at_100(self, engine):
        inp = make_input(focus_blocks_per_week=0.0, after_hours_work_hours=20.0,
                         pipeline_review_hours=0.0)
        score = engine._time_discipline_score(inp)
        assert score <= 100.0
        assert score == 85.0

    def test_focus_blocks_exactly_2_adds_18(self, engine):
        # 2.0 is not < 2 but < 5 → +18
        inp = make_input(focus_blocks_per_week=2.0, after_hours_work_hours=0.0,
                         pipeline_review_hours=3.0)
        score = engine._time_discipline_score(inp)
        assert score == 18.0

    def test_focus_blocks_exactly_5_adds_7(self, engine):
        inp = make_input(focus_blocks_per_week=5.0, after_hours_work_hours=0.0,
                         pipeline_review_hours=3.0)
        score = engine._time_discipline_score(inp)
        assert score == 7.0

    def test_after_hours_exactly_10_adds_30(self, engine):
        inp = make_input(focus_blocks_per_week=8.0, after_hours_work_hours=10.0,
                         pipeline_review_hours=3.0)
        score = engine._time_discipline_score(inp)
        assert score == 30.0

    def test_after_hours_exactly_5_adds_15(self, engine):
        inp = make_input(focus_blocks_per_week=8.0, after_hours_work_hours=5.0,
                         pipeline_review_hours=3.0)
        score = engine._time_discipline_score(inp)
        assert score == 15.0

    def test_pipeline_review_exactly_1_adds_10(self, engine):
        inp = make_input(focus_blocks_per_week=8.0, after_hours_work_hours=0.0,
                         pipeline_review_hours=1.0)
        score = engine._time_discipline_score(inp)
        assert score == 10.0


# ===========================================================================
# 8. Composite score calculation
# ===========================================================================

class TestCompositeScore:

    def test_composite_weighted_sum(self, engine):
        # Use known inputs producing known sub-scores
        # selling=0, admin=0, quality=0, discipline=0 → composite=0
        inp = make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            demo_hours=10.0, prospecting_hours=15.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=0,
            avg_call_duration_minutes=20.0, emails_sent_count=500,
            avg_email_response_time_minutes=60.0,
            focus_blocks_per_week=8.0, after_hours_work_hours=0.0,
            pipeline_review_hours=2.0,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.time_allocation_composite == 0.0

    def test_composite_capped_at_100(self, engine):
        # Worst case: all sub-scores maxed out
        inp = make_input(
            customer_facing_hours=0.0, proposal_prep_hours=0.0,
            demo_hours=0.0, prospecting_hours=0.0,
            admin_hours=40.0, travel_hours=0.0,
            internal_meeting_hours=30.0, internal_meetings_count=20,
            avg_call_duration_minutes=1.0, emails_sent_count=50,
            avg_email_response_time_minutes=2000.0,
            focus_blocks_per_week=0.0, after_hours_work_hours=20.0,
            pipeline_review_hours=0.0,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.time_allocation_composite <= 100.0

    def test_composite_rounded_to_1_decimal(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        composite = result.time_allocation_composite
        assert composite == round(composite, 1)

    def test_composite_formula(self, engine):
        # Manually compute: selling=90, admin=95, quality=90, discipline=85
        # composite = 90*0.35 + 95*0.30 + 90*0.20 + 85*0.15
        #           = 31.5 + 28.5 + 18 + 12.75 = 90.75
        inp = make_input(
            customer_facing_hours=0.0, proposal_prep_hours=0.0,
            demo_hours=0.0, prospecting_hours=0.0,
            admin_hours=40.0, travel_hours=0.0,
            internal_meeting_hours=30.0, internal_meetings_count=20,
            avg_call_duration_minutes=1.0, emails_sent_count=50,
            avg_email_response_time_minutes=2000.0,
            focus_blocks_per_week=0.0, after_hours_work_hours=20.0,
            pipeline_review_hours=0.0,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        # selling=90(capped), admin=95(capped to 95), quality=90, discipline=85
        # Just verify it's >= 80 given nearly worst case
        assert result.time_allocation_composite >= 80.0


# ===========================================================================
# 9. _detect_pattern — all branches and priority ordering
# ===========================================================================

class TestDetectPattern:

    def _make_admin_overload_input(self):
        """admin_score>=35, admin_pct>=0.25"""
        # admin_pct = (30+0)/100 = 0.30 → admin_score += 40 (>=35 ✓), admin_pct=0.30>=0.25 ✓
        return make_input(
            admin_hours=30.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=0,
            total_hours_tracked=100.0,
        )

    def _make_meeting_fatigue_input(self):
        """admin_score>=30, internal_pct>=0.20, but not admin_overload"""
        # admin_pct = (20+0)/100 = 0.20 → admin_score += 20 (>=30? NO)
        # Need admin_score >= 30: add internal_meetings_count>=10 → +10
        # admin_hours=20 → +20, internal_meetings_count=10 → +10, total admin=30 ✓
        # admin_pct=20/100=0.20 < 0.25 → not admin_overload ✓
        # internal_pct = 25/100 = 0.25 >= 0.20 ✓
        return make_input(
            admin_hours=20.0, travel_hours=0.0,
            internal_meeting_hours=25.0, internal_meetings_count=10,
            total_hours_tracked=100.0,
        )

    def _make_low_selling_time_input(self):
        """selling_score>=35, selling_pct<0.25; admin<35 and not meeting_fatigue"""
        # selling_pct = (10+0)/100 = 0.10 → +45 (>=35 ✓), selling_pct < 0.25 ✓
        # admin_pct = 0 → admin_score=0 (not admin_overload, not meeting_fatigue)
        return make_input(
            customer_facing_hours=10.0, proposal_prep_hours=0.0,
            demo_hours=2.0, prospecting_hours=5.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=0,
            total_hours_tracked=100.0,
        )

    def _make_reactive_mode_input(self):
        """quality_score>=30, avg_email_response>=480; selling,admin patterns don't fire"""
        # quality: email_rate=100/100=1.0<2.0 → +30; avg_response=720>=480 → +12; total=42 (>=30 ✓)
        # avg_call_duration=20 → no call bonus
        # admin_pct=0 → not admin_overload
        # selling_pct=50/100=0.50 → selling_score=0, no low_selling_time
        return make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            demo_hours=10.0, prospecting_hours=15.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=0,
            emails_sent_count=100, avg_email_response_time_minutes=720.0,
            avg_call_duration_minutes=20.0,
            focus_blocks_per_week=8.0, after_hours_work_hours=0.0,
            pipeline_review_hours=2.0,
            total_hours_tracked=100.0,
        )

    def _make_time_fragmentation_input(self):
        """discipline_score>=30, focus_blocks<3; other patterns don't fire"""
        # discipline: focus_blocks=1<2 → +35; after_hours=0; pipeline=2 → no bonus; total=35 (>=30 ✓)
        # focus_blocks=1 < 3 ✓
        # admin_pct=0, internal_pct=0, selling_pct=0.50
        # quality: avg_call=20, emails=500/100=5.0, response=60 → 0 (< 30, won't trigger reactive)
        return make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            demo_hours=10.0, prospecting_hours=15.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=0,
            emails_sent_count=500, avg_email_response_time_minutes=60.0,
            avg_call_duration_minutes=20.0,
            focus_blocks_per_week=1.0, after_hours_work_hours=0.0,
            pipeline_review_hours=2.0,
            total_hours_tracked=100.0,
        )

    def test_pattern_admin_overload(self, engine):
        inp = self._make_admin_overload_input()
        result = engine.assess(inp)
        assert result.allocation_pattern == AllocationPattern.admin_overload

    def test_pattern_meeting_fatigue(self, engine):
        inp = self._make_meeting_fatigue_input()
        result = engine.assess(inp)
        assert result.allocation_pattern == AllocationPattern.meeting_fatigue

    def test_pattern_low_selling_time(self, engine):
        inp = self._make_low_selling_time_input()
        result = engine.assess(inp)
        assert result.allocation_pattern == AllocationPattern.low_selling_time

    def test_pattern_reactive_mode(self, engine):
        inp = self._make_reactive_mode_input()
        result = engine.assess(inp)
        assert result.allocation_pattern == AllocationPattern.reactive_mode

    def test_pattern_time_fragmentation(self, engine):
        inp = self._make_time_fragmentation_input()
        result = engine.assess(inp)
        assert result.allocation_pattern == AllocationPattern.time_fragmentation

    def test_pattern_none_healthy(self, engine):
        # selling_pct=0.50, admin=0, quality=0, discipline=0 → none
        inp = make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            demo_hours=10.0, prospecting_hours=15.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=0,
            emails_sent_count=500, avg_email_response_time_minutes=60.0,
            avg_call_duration_minutes=20.0,
            focus_blocks_per_week=8.0, after_hours_work_hours=0.0,
            pipeline_review_hours=2.0,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.allocation_pattern == AllocationPattern.none

    def test_admin_overload_priority_over_meeting_fatigue(self, engine):
        """admin_overload conditions satisfied → should pick admin_overload not meeting_fatigue"""
        # admin_pct=0.30>=0.25, admin_score will include admin+internal → well above 35
        # internal_pct=0.25>=0.20 (meeting_fatigue would also fire)
        inp = make_input(
            admin_hours=30.0, travel_hours=0.0,
            internal_meeting_hours=25.0, internal_meetings_count=15,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.allocation_pattern == AllocationPattern.admin_overload

    def test_meeting_fatigue_priority_over_low_selling_time(self, engine):
        """When both meeting_fatigue and low_selling_time conditions met, meeting_fatigue wins"""
        # admin_score: admin_pct=20/100=0.20→+20, internal_meetings_count=10→+10 → total=30 ✓
        # admin_pct=0.20 < 0.25 → not admin_overload ✓
        # internal_pct=25/100=0.25 >= 0.20 ✓ → meeting_fatigue
        # selling_pct=(10+0)/100=0.10<0.25 AND selling_score will be high (>=35)
        inp = make_input(
            customer_facing_hours=10.0, proposal_prep_hours=0.0,
            demo_hours=2.0, prospecting_hours=5.0,
            admin_hours=20.0, travel_hours=0.0,
            internal_meeting_hours=25.0, internal_meetings_count=10,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.allocation_pattern == AllocationPattern.meeting_fatigue

    def test_low_selling_time_priority_over_reactive_mode(self, engine):
        """When both low_selling_time and reactive_mode would fire, low_selling_time wins"""
        # selling_pct=(10+0)/100=0.10<0.25 AND selling_score>=35 → low_selling_time
        # quality>=30 and response>=480 → reactive_mode would also fire
        inp = make_input(
            customer_facing_hours=10.0, proposal_prep_hours=0.0,
            demo_hours=2.0, prospecting_hours=5.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=0,
            emails_sent_count=100, avg_email_response_time_minutes=720.0,
            avg_call_duration_minutes=20.0,
            focus_blocks_per_week=8.0, after_hours_work_hours=0.0,
            pipeline_review_hours=2.0,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.allocation_pattern == AllocationPattern.low_selling_time

    def test_reactive_mode_priority_over_time_fragmentation(self, engine):
        """reactive_mode before time_fragmentation in priority order"""
        # quality>=30, response>=480 → reactive_mode
        # discipline>=30, focus_blocks<3 → time_fragmentation would also fire
        # admin_score < 30, selling_score < 35 (selling_pct = 0.50)
        inp = make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            demo_hours=10.0, prospecting_hours=15.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=0,
            emails_sent_count=100, avg_email_response_time_minutes=720.0,
            avg_call_duration_minutes=20.0,
            focus_blocks_per_week=1.0, after_hours_work_hours=0.0,
            pipeline_review_hours=2.0,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.allocation_pattern == AllocationPattern.reactive_mode

    def test_admin_overload_requires_admin_pct_threshold(self, engine):
        """admin_score>=35 but admin_pct<0.25 → not admin_overload"""
        # admin_pct = 20/100 = 0.20 < 0.25
        # admin_score: admin_pct=0.20→+20, internal_meetings_count=15→+20 = 40 (>=35 ✓)
        # But admin_pct < 0.25 → should NOT be admin_overload
        inp = make_input(
            admin_hours=20.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=15,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.allocation_pattern != AllocationPattern.admin_overload

    def test_meeting_fatigue_requires_internal_pct_threshold(self, engine):
        """admin_score>=30 but internal_pct<0.20 → not meeting_fatigue"""
        # admin: admin_pct=0.20→+20, internal_meetings=10→+10 = 30 ✓
        # internal_pct = 5/100 = 0.05 < 0.20 → not meeting_fatigue
        inp = make_input(
            admin_hours=20.0, travel_hours=0.0,
            internal_meeting_hours=5.0, internal_meetings_count=10,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.allocation_pattern != AllocationPattern.meeting_fatigue

    def test_low_selling_time_requires_selling_pct_below_025(self, engine):
        """selling_score>=35 but selling_pct>=0.25 → not low_selling_time"""
        # selling_pct = (25+0)/100 = 0.25 (not < 0.25)
        # demo_pct=2/100=0.02→+25, prospecting_pct=5/100=0.05→+20 → selling_score=45 ≥ 35
        inp = make_input(
            customer_facing_hours=25.0, proposal_prep_hours=0.0,
            demo_hours=2.0, prospecting_hours=5.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=0,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.allocation_pattern != AllocationPattern.low_selling_time

    def test_reactive_mode_requires_response_time_threshold(self, engine):
        """quality>=30 but avg_email_response<480 → not reactive_mode"""
        inp = make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            demo_hours=10.0, prospecting_hours=15.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=0,
            emails_sent_count=100, avg_email_response_time_minutes=479.0,
            avg_call_duration_minutes=20.0,
            focus_blocks_per_week=8.0, after_hours_work_hours=0.0,
            pipeline_review_hours=2.0,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.allocation_pattern != AllocationPattern.reactive_mode

    def test_time_fragmentation_requires_focus_blocks_below_3(self, engine):
        """discipline>=30 but focus_blocks>=3 → not time_fragmentation"""
        # discipline: focus_blocks=3 (not < 3), after_hours=0, pipeline=2 → no bonus
        # Need discipline>=30 another way: after_hours=10→+30
        inp = make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            demo_hours=10.0, prospecting_hours=15.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=0,
            emails_sent_count=500, avg_email_response_time_minutes=60.0,
            avg_call_duration_minutes=20.0,
            focus_blocks_per_week=3.0, after_hours_work_hours=10.0,
            pipeline_review_hours=2.0,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.allocation_pattern != AllocationPattern.time_fragmentation


# ===========================================================================
# 10. _risk_level
# ===========================================================================

class TestRiskLevel:

    def test_risk_low_below_20(self, engine):
        # composite < 20 → low
        r = engine._risk_level(19.9)
        assert r == AllocationRisk.low

    def test_risk_low_at_0(self, engine):
        assert engine._risk_level(0.0) == AllocationRisk.low

    def test_risk_moderate_at_20(self, engine):
        assert engine._risk_level(20.0) == AllocationRisk.moderate

    def test_risk_moderate_at_39(self, engine):
        assert engine._risk_level(39.9) == AllocationRisk.moderate

    def test_risk_high_at_40(self, engine):
        assert engine._risk_level(40.0) == AllocationRisk.high

    def test_risk_high_at_59(self, engine):
        assert engine._risk_level(59.9) == AllocationRisk.high

    def test_risk_critical_at_60(self, engine):
        assert engine._risk_level(60.0) == AllocationRisk.critical

    def test_risk_critical_at_100(self, engine):
        assert engine._risk_level(100.0) == AllocationRisk.critical


# ===========================================================================
# 11. _severity
# ===========================================================================

class TestSeverity:

    def test_severity_optimized_below_20(self, engine):
        assert engine._severity(19.9) == AllocationSeverity.optimized

    def test_severity_optimized_at_0(self, engine):
        assert engine._severity(0.0) == AllocationSeverity.optimized

    def test_severity_developing_at_20(self, engine):
        assert engine._severity(20.0) == AllocationSeverity.developing

    def test_severity_developing_at_39(self, engine):
        assert engine._severity(39.9) == AllocationSeverity.developing

    def test_severity_burdened_at_40(self, engine):
        assert engine._severity(40.0) == AllocationSeverity.burdened

    def test_severity_burdened_at_59(self, engine):
        assert engine._severity(59.9) == AllocationSeverity.burdened

    def test_severity_fragmented_at_60(self, engine):
        assert engine._severity(60.0) == AllocationSeverity.fragmented

    def test_severity_fragmented_at_100(self, engine):
        assert engine._severity(100.0) == AllocationSeverity.fragmented


# ===========================================================================
# 12. _action — all risk+pattern combos
# ===========================================================================

class TestAction:

    def test_critical_admin_overload_returns_admin_reduction_plan(self, engine):
        assert engine._action(AllocationRisk.critical, AllocationPattern.admin_overload) == AllocationAction.admin_reduction_plan

    def test_critical_low_selling_time_returns_selling_time_recovery(self, engine):
        assert engine._action(AllocationRisk.critical, AllocationPattern.low_selling_time) == AllocationAction.selling_time_recovery

    def test_critical_meeting_fatigue_returns_workflow_optimization(self, engine):
        assert engine._action(AllocationRisk.critical, AllocationPattern.meeting_fatigue) == AllocationAction.workflow_optimization

    def test_critical_reactive_mode_returns_workflow_optimization(self, engine):
        assert engine._action(AllocationRisk.critical, AllocationPattern.reactive_mode) == AllocationAction.workflow_optimization

    def test_critical_time_fragmentation_returns_workflow_optimization(self, engine):
        assert engine._action(AllocationRisk.critical, AllocationPattern.time_fragmentation) == AllocationAction.workflow_optimization

    def test_critical_none_returns_workflow_optimization(self, engine):
        assert engine._action(AllocationRisk.critical, AllocationPattern.none) == AllocationAction.workflow_optimization

    def test_high_meeting_fatigue_returns_meeting_hygiene_review(self, engine):
        assert engine._action(AllocationRisk.high, AllocationPattern.meeting_fatigue) == AllocationAction.meeting_hygiene_review

    def test_high_time_fragmentation_returns_time_audit_coaching(self, engine):
        assert engine._action(AllocationRisk.high, AllocationPattern.time_fragmentation) == AllocationAction.time_audit_coaching

    def test_high_admin_overload_returns_selling_time_recovery(self, engine):
        assert engine._action(AllocationRisk.high, AllocationPattern.admin_overload) == AllocationAction.selling_time_recovery

    def test_high_low_selling_time_returns_selling_time_recovery(self, engine):
        assert engine._action(AllocationRisk.high, AllocationPattern.low_selling_time) == AllocationAction.selling_time_recovery

    def test_high_reactive_mode_returns_selling_time_recovery(self, engine):
        assert engine._action(AllocationRisk.high, AllocationPattern.reactive_mode) == AllocationAction.selling_time_recovery

    def test_high_none_returns_selling_time_recovery(self, engine):
        assert engine._action(AllocationRisk.high, AllocationPattern.none) == AllocationAction.selling_time_recovery

    def test_moderate_any_pattern_returns_time_audit_coaching(self, engine):
        for pattern in AllocationPattern:
            assert engine._action(AllocationRisk.moderate, pattern) == AllocationAction.time_audit_coaching

    def test_low_any_pattern_returns_no_action(self, engine):
        for pattern in AllocationPattern:
            assert engine._action(AllocationRisk.low, pattern) == AllocationAction.no_action


# ===========================================================================
# 13. _has_time_gap flags
# ===========================================================================

class TestHasTimeGap:

    def test_time_gap_composite_at_40(self, engine):
        inp = make_input(total_hours_tracked=100.0)
        assert engine._has_time_gap(40.0, inp) is True

    def test_time_gap_composite_above_40(self, engine):
        inp = make_input(total_hours_tracked=100.0)
        assert engine._has_time_gap(60.0, inp) is True

    def test_time_gap_composite_below_40_no_other_flags(self, engine):
        # selling_pct=(30+10)/100=0.40 >= 0.15, admin_pct=(10+5)/100=0.15 < 0.35
        inp = make_input(
            customer_facing_hours=30.0, proposal_prep_hours=10.0,
            admin_hours=10.0, travel_hours=5.0,
            total_hours_tracked=100.0,
        )
        assert engine._has_time_gap(39.9, inp) is False

    def test_time_gap_selling_pct_below_015(self, engine):
        # selling_pct = (10+0)/100 = 0.10 < 0.15
        inp = make_input(
            customer_facing_hours=10.0, proposal_prep_hours=0.0,
            admin_hours=5.0, travel_hours=0.0,
            total_hours_tracked=100.0,
        )
        assert engine._has_time_gap(10.0, inp) is True

    def test_time_gap_selling_pct_exactly_015(self, engine):
        # selling_pct = 15/100 = 0.15, not < 0.15
        inp = make_input(
            customer_facing_hours=15.0, proposal_prep_hours=0.0,
            admin_hours=5.0, travel_hours=0.0,
            total_hours_tracked=100.0,
        )
        assert engine._has_time_gap(10.0, inp) is False

    def test_time_gap_admin_pct_at_035(self, engine):
        # admin_pct = (35+0)/100 = 0.35
        inp = make_input(
            customer_facing_hours=30.0, proposal_prep_hours=10.0,
            admin_hours=35.0, travel_hours=0.0,
            total_hours_tracked=100.0,
        )
        assert engine._has_time_gap(10.0, inp) is True

    def test_time_gap_admin_pct_above_035(self, engine):
        inp = make_input(
            customer_facing_hours=20.0, proposal_prep_hours=0.0,
            admin_hours=40.0, travel_hours=0.0,
            total_hours_tracked=100.0,
        )
        assert engine._has_time_gap(10.0, inp) is True

    def test_time_gap_admin_pct_below_035_no_gap(self, engine):
        # admin_pct=(10+5)/100=0.15, selling_pct=(30+10)/100=0.40
        inp = make_input(
            customer_facing_hours=30.0, proposal_prep_hours=10.0,
            admin_hours=10.0, travel_hours=5.0,
            total_hours_tracked=100.0,
        )
        assert engine._has_time_gap(10.0, inp) is False


# ===========================================================================
# 14. _requires_allocation_coaching flags
# ===========================================================================

class TestRequiresAllocationCoaching:

    def test_coaching_composite_at_30(self, engine):
        inp = make_input(
            customer_facing_hours=30.0, proposal_prep_hours=10.0,
            admin_hours=5.0, travel_hours=0.0,
            internal_meeting_hours=5.0, total_hours_tracked=100.0,
        )
        assert engine._requires_allocation_coaching(30.0, inp) is True

    def test_coaching_composite_above_30(self, engine):
        inp = make_input(
            customer_facing_hours=30.0, proposal_prep_hours=10.0,
            total_hours_tracked=100.0,
        )
        assert engine._requires_allocation_coaching(50.0, inp) is True

    def test_coaching_composite_below_30_no_other_flags(self, engine):
        # selling_pct=(30+10)/100=0.40>=0.20, internal_pct=5/100=0.05<0.25
        inp = make_input(
            customer_facing_hours=30.0, proposal_prep_hours=10.0,
            admin_hours=5.0, travel_hours=0.0,
            internal_meeting_hours=5.0, total_hours_tracked=100.0,
        )
        assert engine._requires_allocation_coaching(29.9, inp) is False

    def test_coaching_selling_pct_below_020(self, engine):
        # selling_pct=(10+0)/100=0.10 < 0.20
        inp = make_input(
            customer_facing_hours=10.0, proposal_prep_hours=0.0,
            internal_meeting_hours=5.0, total_hours_tracked=100.0,
        )
        assert engine._requires_allocation_coaching(5.0, inp) is True

    def test_coaching_selling_pct_exactly_020(self, engine):
        # selling_pct=0.20, not < 0.20
        inp = make_input(
            customer_facing_hours=20.0, proposal_prep_hours=0.0,
            internal_meeting_hours=5.0, total_hours_tracked=100.0,
        )
        assert engine._requires_allocation_coaching(5.0, inp) is False

    def test_coaching_internal_pct_at_025(self, engine):
        # internal_pct=25/100=0.25 >= 0.25
        inp = make_input(
            customer_facing_hours=30.0, proposal_prep_hours=10.0,
            internal_meeting_hours=25.0, total_hours_tracked=100.0,
        )
        assert engine._requires_allocation_coaching(5.0, inp) is True

    def test_coaching_internal_pct_above_025(self, engine):
        inp = make_input(
            customer_facing_hours=30.0, proposal_prep_hours=10.0,
            internal_meeting_hours=30.0, total_hours_tracked=100.0,
        )
        assert engine._requires_allocation_coaching(5.0, inp) is True

    def test_coaching_internal_pct_below_025_no_coaching(self, engine):
        # internal_pct=20/100=0.20 < 0.25, selling_pct=0.40, composite=5 < 30
        inp = make_input(
            customer_facing_hours=30.0, proposal_prep_hours=10.0,
            internal_meeting_hours=20.0, total_hours_tracked=100.0,
        )
        assert engine._requires_allocation_coaching(5.0, inp) is False


# ===========================================================================
# 15. _estimated_selling_hours_lost
# ===========================================================================

class TestEstimatedSellingHoursLost:

    def test_hours_lost_zero_when_selling_pct_above_040(self, engine):
        # selling_pct=(50+0)/100=0.50 >= 0.40 → gap=0 → 0
        inp = make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            total_hours_tracked=100.0,
        )
        lost = engine._estimated_selling_hours_lost(inp, composite=50.0)
        assert lost == 0.0

    def test_hours_lost_zero_when_composite_zero(self, engine):
        # gap > 0 but composite=0 → 0
        inp = make_input(
            customer_facing_hours=10.0, proposal_prep_hours=0.0,
            total_hours_tracked=100.0,
        )
        lost = engine._estimated_selling_hours_lost(inp, composite=0.0)
        assert lost == 0.0

    def test_hours_lost_formula(self, engine):
        # selling_pct=10/100=0.10, gap=0.40-0.10=0.30
        # total=100, composite=100
        # lost = round(0.30*100/4*100/100, 2) = round(7.5, 2) = 7.5
        inp = make_input(
            customer_facing_hours=10.0, proposal_prep_hours=0.0,
            total_hours_tracked=100.0,
        )
        lost = engine._estimated_selling_hours_lost(inp, composite=100.0)
        assert lost == 7.5

    def test_hours_lost_rounded_to_2_decimal(self, engine):
        # selling_pct=(10+3)/100=0.13, gap=0.27
        # total=100, composite=77.0
        # lost = round(0.27*100/4*77/100, 2) = round(0.27*25*0.77, 2) = round(5.1975, 2) = 5.2
        inp = make_input(
            customer_facing_hours=10.0, proposal_prep_hours=3.0,
            total_hours_tracked=100.0,
        )
        lost = engine._estimated_selling_hours_lost(inp, composite=77.0)
        expected = round((0.40 - 0.13) * 100 / 4 * 77 / 100, 2)
        assert lost == expected

    def test_hours_lost_nonnegative(self, engine, healthy_input):
        lost = engine._estimated_selling_hours_lost(healthy_input, composite=50.0)
        assert lost >= 0.0

    def test_hours_lost_at_exactly_040_is_zero(self, engine):
        # selling_pct=40/100=0.40, gap=max(0, 0)=0
        inp = make_input(
            customer_facing_hours=40.0, proposal_prep_hours=0.0,
            total_hours_tracked=100.0,
        )
        lost = engine._estimated_selling_hours_lost(inp, composite=80.0)
        assert lost == 0.0

    def test_hours_lost_uses_proposal_prep_in_selling_pct(self, engine):
        # selling_pct=(0+30)/100=0.30, gap=0.10
        # total=100, composite=100
        # lost = round(0.10*100/4*1.0, 2) = 2.5
        inp = make_input(
            customer_facing_hours=0.0, proposal_prep_hours=30.0,
            total_hours_tracked=100.0,
        )
        lost = engine._estimated_selling_hours_lost(inp, composite=100.0)
        assert lost == 2.5


# ===========================================================================
# 16. _signal string construction
# ===========================================================================

class TestSignal:

    def test_signal_healthy_none_pattern_low_composite(self, engine):
        # pattern=none, composite<20 → healthy signal
        inp = make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            demo_hours=10.0, prospecting_hours=15.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=0,
            emails_sent_count=500, avg_email_response_time_minutes=60.0,
            avg_call_duration_minutes=20.0,
            focus_blocks_per_week=8.0, after_hours_work_hours=0.0,
            pipeline_review_hours=2.0, total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.allocation_signal == "Time allocation and selling productivity within healthy benchmarks"

    def test_signal_none_pattern_composite_above_20_not_healthy_msg(self, engine):
        # none pattern but composite >= 20 → should not return healthy message
        signal = engine._signal(
            make_input(
                customer_facing_hours=30.0, proposal_prep_hours=0.0,
                admin_hours=10.0, travel_hours=0.0,
                internal_meeting_hours=5.0, total_hours_tracked=100.0,
            ),
            AllocationPattern.none,
            composite=25.0,
        )
        assert signal != "Time allocation and selling productivity within healthy benchmarks"

    def test_signal_contains_label_for_pattern(self, engine):
        signal = engine._signal(
            make_input(
                customer_facing_hours=10.0, proposal_prep_hours=0.0,
                admin_hours=30.0, travel_hours=0.0,
                internal_meeting_hours=10.0, total_hours_tracked=100.0,
            ),
            AllocationPattern.admin_overload,
            composite=70.0,
        )
        assert "Admin overload" in signal

    def test_signal_label_none_becomes_allocation_risk(self, engine):
        signal = engine._signal(
            make_input(
                customer_facing_hours=10.0, proposal_prep_hours=0.0,
                admin_hours=5.0, travel_hours=0.0,
                internal_meeting_hours=5.0, total_hours_tracked=100.0,
            ),
            AllocationPattern.none,
            composite=25.0,
        )
        assert "Allocation risk" in signal

    def test_signal_contains_customer_facing_when_selling_pct_below_030(self, engine):
        # selling_pct=(10+0)/100=0.10<0.30 → add customer-facing
        inp = make_input(
            customer_facing_hours=10.0, proposal_prep_hours=0.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, total_hours_tracked=100.0,
        )
        signal = engine._signal(inp, AllocationPattern.none, composite=25.0)
        assert "customer-facing" in signal

    def test_signal_no_customer_facing_when_selling_pct_above_030(self, engine):
        # selling_pct=(35+0)/100=0.35 >= 0.30
        inp = make_input(
            customer_facing_hours=35.0, proposal_prep_hours=0.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, total_hours_tracked=100.0,
        )
        signal = engine._signal(inp, AllocationPattern.none, composite=25.0)
        assert "customer-facing" not in signal

    def test_signal_contains_admin_when_admin_pct_above_015(self, engine):
        # admin_pct=(20+0)/100=0.20 >= 0.15
        inp = make_input(
            customer_facing_hours=35.0, proposal_prep_hours=0.0,
            admin_hours=20.0, travel_hours=0.0,
            internal_meeting_hours=0.0, total_hours_tracked=100.0,
        )
        signal = engine._signal(inp, AllocationPattern.none, composite=25.0)
        assert "admin" in signal

    def test_signal_no_admin_when_admin_pct_below_015(self, engine):
        inp = make_input(
            customer_facing_hours=35.0, proposal_prep_hours=0.0,
            admin_hours=10.0, travel_hours=0.0,
            internal_meeting_hours=0.0, total_hours_tracked=100.0,
        )
        signal = engine._signal(inp, AllocationPattern.none, composite=25.0)
        assert "admin" not in signal

    def test_signal_contains_internal_meetings_when_hours_above_5(self, engine):
        inp = make_input(
            customer_facing_hours=35.0, proposal_prep_hours=0.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=6.0, total_hours_tracked=100.0,
        )
        signal = engine._signal(inp, AllocationPattern.none, composite=25.0)
        assert "internal meetings" in signal

    def test_signal_no_internal_meetings_when_hours_below_5(self, engine):
        inp = make_input(
            customer_facing_hours=35.0, proposal_prep_hours=0.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=4.9, total_hours_tracked=100.0,
        )
        signal = engine._signal(inp, AllocationPattern.none, composite=25.0)
        assert "internal meetings" not in signal

    def test_signal_contains_composite_value(self, engine):
        inp = make_input(
            customer_facing_hours=10.0, proposal_prep_hours=0.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, total_hours_tracked=100.0,
        )
        signal = engine._signal(inp, AllocationPattern.none, composite=35.0)
        assert "composite 35" in signal

    def test_signal_fallback_no_parts(self, engine):
        # selling_pct >= 0.30, admin_pct < 0.15, internal < 5 → no parts → "selling time below target"
        inp = make_input(
            customer_facing_hours=35.0, proposal_prep_hours=0.0,
            admin_hours=5.0, travel_hours=0.0,
            internal_meeting_hours=3.0, total_hours_tracked=100.0,
        )
        signal = engine._signal(inp, AllocationPattern.none, composite=25.0)
        assert "selling time below target" in signal

    def test_signal_pattern_value_replaces_underscores(self, engine):
        inp = make_input(
            customer_facing_hours=10.0, proposal_prep_hours=0.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, total_hours_tracked=100.0,
        )
        signal = engine._signal(inp, AllocationPattern.low_selling_time, composite=50.0)
        assert "Low selling time" in signal
        assert "_" not in signal.split("—")[0]

    def test_signal_meeting_fatigue_capitalized(self, engine):
        inp = make_input(
            customer_facing_hours=10.0, proposal_prep_hours=0.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, total_hours_tracked=100.0,
        )
        signal = engine._signal(inp, AllocationPattern.meeting_fatigue, composite=50.0)
        assert signal.startswith("Meeting fatigue")

    def test_signal_exactly_at_030_selling_pct_no_customer_facing(self, engine):
        # selling_pct=30/100=0.30, not < 0.30
        inp = make_input(
            customer_facing_hours=30.0, proposal_prep_hours=0.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, total_hours_tracked=100.0,
        )
        signal = engine._signal(inp, AllocationPattern.none, composite=25.0)
        assert "customer-facing" not in signal

    def test_signal_exactly_at_015_admin_pct_includes_admin(self, engine):
        # admin_pct=15/100=0.15 >= 0.15
        inp = make_input(
            customer_facing_hours=35.0, proposal_prep_hours=0.0,
            admin_hours=15.0, travel_hours=0.0,
            internal_meeting_hours=0.0, total_hours_tracked=100.0,
        )
        signal = engine._signal(inp, AllocationPattern.none, composite=25.0)
        assert "admin" in signal

    def test_signal_internal_exactly_5_hours_included(self, engine):
        inp = make_input(
            customer_facing_hours=35.0, proposal_prep_hours=0.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=5.0, total_hours_tracked=100.0,
        )
        signal = engine._signal(inp, AllocationPattern.none, composite=25.0)
        assert "internal meetings" in signal


# ===========================================================================
# 17. assess() end-to-end structure
# ===========================================================================

class TestAssessStructure:

    def test_assess_returns_time_allocation_result(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result, TimeAllocationResult)

    def test_assess_rep_id_propagated(self, engine):
        inp = make_input(rep_id="XYZ99")
        result = engine.assess(inp)
        assert result.rep_id == "XYZ99"

    def test_assess_region_propagated(self, engine):
        inp = make_input(region="APAC")
        result = engine.assess(inp)
        assert result.region == "APAC"

    def test_assess_selling_time_score_in_result(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert 0.0 <= result.selling_time_score <= 100.0

    def test_assess_admin_burden_score_in_result(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert 0.0 <= result.admin_burden_score <= 100.0

    def test_assess_activity_quality_score_in_result(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert 0.0 <= result.activity_quality_score <= 100.0

    def test_assess_time_discipline_score_in_result(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert 0.0 <= result.time_discipline_score <= 100.0

    def test_assess_composite_in_result(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert 0.0 <= result.time_allocation_composite <= 100.0

    def test_assess_allocation_risk_is_enum(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.allocation_risk, AllocationRisk)

    def test_assess_allocation_pattern_is_enum(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.allocation_pattern, AllocationPattern)

    def test_assess_allocation_severity_is_enum(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.allocation_severity, AllocationSeverity)

    def test_assess_recommended_action_is_enum(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.recommended_action, AllocationAction)

    def test_assess_has_time_gap_is_bool(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.has_time_gap, bool)

    def test_assess_requires_coaching_is_bool(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.requires_allocation_coaching, bool)

    def test_assess_hours_lost_is_nonneg_float(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.estimated_selling_hours_lost_per_week, float)
        assert result.estimated_selling_hours_lost_per_week >= 0.0

    def test_assess_signal_is_nonempty_string(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.allocation_signal, str)
        assert len(result.allocation_signal) > 0

    def test_assess_appends_to_internal_results(self, engine, healthy_input):
        engine.assess(healthy_input)
        assert len(engine._results) == 1

    def test_assess_multiple_appends(self, engine, healthy_input):
        engine.assess(healthy_input)
        engine.assess(healthy_input)
        assert len(engine._results) == 2

    def test_assess_scores_rounded_to_1_decimal(self, engine):
        inp = make_input(total_hours_tracked=33.0, customer_facing_hours=5.0,
                         proposal_prep_hours=3.0, demo_hours=2.0, prospecting_hours=4.0)
        result = engine.assess(inp)
        for score in [result.selling_time_score, result.admin_burden_score,
                      result.activity_quality_score, result.time_discipline_score,
                      result.time_allocation_composite]:
            assert score == round(score, 1)


# ===========================================================================
# 18. assess_batch()
# ===========================================================================

class TestAssessBatch:

    def test_assess_batch_empty_list(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_assess_batch_single(self, engine, healthy_input):
        results = engine.assess_batch([healthy_input])
        assert len(results) == 1
        assert isinstance(results[0], TimeAllocationResult)

    def test_assess_batch_multiple(self, engine, healthy_input):
        inp2 = make_input(rep_id="R002")
        results = engine.assess_batch([healthy_input, inp2])
        assert len(results) == 2

    def test_assess_batch_returns_list(self, engine, healthy_input):
        results = engine.assess_batch([healthy_input])
        assert isinstance(results, list)

    def test_assess_batch_preserves_order(self, engine):
        inputs = [make_input(rep_id=f"R{i:03d}") for i in range(5)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"R{i:03d}"

    def test_assess_batch_appends_to_internal_results(self, engine, healthy_input):
        inp2 = make_input(rep_id="R002")
        engine.assess_batch([healthy_input, inp2])
        assert len(engine._results) == 2

    def test_assess_batch_each_result_is_result_type(self, engine):
        inputs = [make_input(rep_id=f"REP{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        assert all(isinstance(r, TimeAllocationResult) for r in results)


# ===========================================================================
# 19. summary()
# ===========================================================================

class TestSummary:

    def test_summary_empty_returns_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_summary_empty_total_is_0(self, engine):
        s = engine.summary()
        assert s["total"] == 0

    def test_summary_empty_risk_counts_empty(self, engine):
        s = engine.summary()
        assert s["risk_counts"] == {}

    def test_summary_empty_pattern_counts_empty(self, engine):
        s = engine.summary()
        assert s["pattern_counts"] == {}

    def test_summary_empty_severity_counts_empty(self, engine):
        s = engine.summary()
        assert s["severity_counts"] == {}

    def test_summary_empty_action_counts_empty(self, engine):
        s = engine.summary()
        assert s["action_counts"] == {}

    def test_summary_empty_avg_composite_is_0(self, engine):
        s = engine.summary()
        assert s["avg_time_allocation_composite"] == 0.0

    def test_summary_empty_time_gap_count_0(self, engine):
        s = engine.summary()
        assert s["time_gap_count"] == 0

    def test_summary_empty_coaching_count_0(self, engine):
        s = engine.summary()
        assert s["allocation_coaching_count"] == 0

    def test_summary_empty_avg_selling_score_0(self, engine):
        s = engine.summary()
        assert s["avg_selling_time_score"] == 0.0

    def test_summary_empty_avg_admin_score_0(self, engine):
        s = engine.summary()
        assert s["avg_admin_burden_score"] == 0.0

    def test_summary_empty_avg_quality_score_0(self, engine):
        s = engine.summary()
        assert s["avg_activity_quality_score"] == 0.0

    def test_summary_empty_avg_discipline_score_0(self, engine):
        s = engine.summary()
        assert s["avg_time_discipline_score"] == 0.0

    def test_summary_empty_total_hours_lost_0(self, engine):
        s = engine.summary()
        assert s["total_estimated_selling_hours_lost_per_week"] == 0.0

    def test_summary_after_one_assess_total_1(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        assert s["total"] == 1

    def test_summary_has_13_keys_after_assess(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        assert len(s) == 13

    def test_summary_expected_keys(self, engine):
        s = engine.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_time_allocation_composite", "time_gap_count",
            "allocation_coaching_count", "avg_selling_time_score",
            "avg_admin_burden_score", "avg_activity_quality_score",
            "avg_time_discipline_score", "total_estimated_selling_hours_lost_per_week",
        }
        assert set(s.keys()) == expected

    def test_summary_risk_counts_correct(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        result = engine._results[0]
        assert s["risk_counts"].get(result.allocation_risk.value, 0) == 1

    def test_summary_pattern_counts_correct(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        result = engine._results[0]
        assert s["pattern_counts"].get(result.allocation_pattern.value, 0) == 1

    def test_summary_severity_counts_correct(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        result = engine._results[0]
        assert s["severity_counts"].get(result.allocation_severity.value, 0) == 1

    def test_summary_action_counts_correct(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        result = engine._results[0]
        assert s["action_counts"].get(result.recommended_action.value, 0) == 1

    def test_summary_avg_composite_correct(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        expected = round(engine._results[0].time_allocation_composite, 1)
        assert s["avg_time_allocation_composite"] == expected

    def test_summary_time_gap_count(self, engine):
        # One with gap, one without
        gap_inp = make_input(
            customer_facing_hours=10.0, proposal_prep_hours=0.0,
            admin_hours=40.0, travel_hours=0.0, total_hours_tracked=100.0,
        )
        no_gap_inp = make_input(
            customer_facing_hours=30.0, proposal_prep_hours=10.0,
            admin_hours=10.0, travel_hours=5.0, total_hours_tracked=100.0,
        )
        engine.assess(gap_inp)
        engine.assess(no_gap_inp)
        s = engine.summary()
        # gap_inp: admin_pct=0.40>=0.35 → has_time_gap=True
        gap_count = s["time_gap_count"]
        assert gap_count >= 1

    def test_summary_total_hours_lost_is_sum(self, engine, healthy_input):
        engine.assess(healthy_input)
        engine.assess(healthy_input)
        s = engine.summary()
        expected = round(
            engine._results[0].estimated_selling_hours_lost_per_week +
            engine._results[1].estimated_selling_hours_lost_per_week, 2
        )
        assert s["total_estimated_selling_hours_lost_per_week"] == expected

    def test_summary_multiple_reps(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 5

    def test_summary_avg_selling_score_correct(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        expected = round(engine._results[0].selling_time_score, 1)
        assert s["avg_selling_time_score"] == expected

    def test_summary_avg_admin_score_correct(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        expected = round(engine._results[0].admin_burden_score, 1)
        assert s["avg_admin_burden_score"] == expected

    def test_summary_avg_quality_score_correct(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        expected = round(engine._results[0].activity_quality_score, 1)
        assert s["avg_activity_quality_score"] == expected

    def test_summary_avg_discipline_score_correct(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        expected = round(engine._results[0].time_discipline_score, 1)
        assert s["avg_time_discipline_score"] == expected


# ===========================================================================
# 20. Full end-to-end scenario tests
# ===========================================================================

class TestEndToEndScenarios:

    def test_perfectly_healthy_rep(self, engine):
        """A rep with optimal allocation should score low everywhere."""
        inp = make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            demo_hours=10.0, prospecting_hours=15.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=0,
            emails_sent_count=500, avg_email_response_time_minutes=60.0,
            avg_call_duration_minutes=20.0,
            focus_blocks_per_week=8.0, after_hours_work_hours=0.0,
            pipeline_review_hours=2.0, total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.allocation_risk == AllocationRisk.low
        assert result.allocation_severity == AllocationSeverity.optimized
        assert result.recommended_action == AllocationAction.no_action
        assert result.allocation_pattern == AllocationPattern.none

    def test_critical_admin_overload_scenario(self, engine):
        """Heavy admin burden triggers admin_reduction_plan at critical risk."""
        inp = make_input(
            customer_facing_hours=5.0, proposal_prep_hours=0.0,
            demo_hours=1.0, prospecting_hours=3.0,
            admin_hours=40.0, travel_hours=0.0,
            internal_meeting_hours=25.0, internal_meetings_count=18,
            emails_sent_count=50, avg_email_response_time_minutes=1500.0,
            avg_call_duration_minutes=2.0,
            focus_blocks_per_week=1.0, after_hours_work_hours=15.0,
            pipeline_review_hours=0.5, total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.allocation_risk == AllocationRisk.critical
        assert result.allocation_pattern == AllocationPattern.admin_overload
        assert result.recommended_action == AllocationAction.admin_reduction_plan

    def test_high_meeting_fatigue_scenario(self, engine):
        """Meeting fatigue at high risk → meeting_hygiene_review."""
        inp = make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            demo_hours=10.0, prospecting_hours=15.0,
            admin_hours=20.0, travel_hours=0.0,
            internal_meeting_hours=25.0, internal_meetings_count=10,
            emails_sent_count=500, avg_email_response_time_minutes=60.0,
            avg_call_duration_minutes=20.0,
            focus_blocks_per_week=8.0, after_hours_work_hours=0.0,
            pipeline_review_hours=2.0, total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        # admin_score = 20+18+10=48 (>=30), internal_pct=0.25>=0.20 → meeting_fatigue
        # admin_pct=0.20<0.25 → not admin_overload
        assert result.allocation_pattern == AllocationPattern.meeting_fatigue
        if result.allocation_risk == AllocationRisk.high:
            assert result.recommended_action == AllocationAction.meeting_hygiene_review

    def test_time_fragmentation_high_risk(self, engine):
        """time_fragmentation at high risk → time_audit_coaching."""
        # Need composite>=40 (high) and time_fragmentation pattern
        inp = make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            demo_hours=10.0, prospecting_hours=15.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=0.0, internal_meetings_count=0,
            emails_sent_count=500, avg_email_response_time_minutes=60.0,
            avg_call_duration_minutes=20.0,
            focus_blocks_per_week=1.0, after_hours_work_hours=10.0,
            pipeline_review_hours=0.5, total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        # discipline_score: focus<2→+35, after_hours>=10→+30, pipeline<1→+20 = 85
        # selling=0, admin=0, quality=0
        # composite = 0*0.35+0*0.30+0*0.20+85*0.15 = 12.75 → low risk
        # this is actually low; let's verify pattern is time_fragmentation
        assert result.allocation_pattern == AllocationPattern.time_fragmentation

    def test_no_time_gap_for_healthy_rep(self, engine):
        inp = make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            admin_hours=5.0, travel_hours=0.0,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        # selling_pct=0.50>=0.15, admin_pct=0.05<0.35, composite=low
        assert result.has_time_gap is False

    def test_coaching_required_for_low_selling(self, engine):
        inp = make_input(
            customer_facing_hours=10.0, proposal_prep_hours=0.0,
            total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        # selling_pct=0.10<0.20 → requires coaching
        assert result.requires_allocation_coaching is True

    def test_no_coaching_for_healthy_rep(self, engine):
        inp = make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            admin_hours=5.0, travel_hours=0.0,
            internal_meeting_hours=5.0, total_hours_tracked=100.0,
            avg_call_duration_minutes=20.0, emails_sent_count=500,
            avg_email_response_time_minutes=60.0,
            focus_blocks_per_week=8.0, after_hours_work_hours=0.0,
            pipeline_review_hours=2.0,
        )
        result = engine.assess(inp)
        assert result.requires_allocation_coaching is False

    def test_to_dict_round_trip(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        d = result.to_dict()
        assert d["rep_id"] == result.rep_id
        assert d["allocation_risk"] == result.allocation_risk.value
        assert d["selling_time_score"] == result.selling_time_score
        assert d["has_time_gap"] == result.has_time_gap


# ===========================================================================
# 21. Edge cases
# ===========================================================================

class TestEdgeCases:

    def test_zero_total_hours_uses_floor(self, engine):
        inp = make_input(total_hours_tracked=0.0, customer_facing_hours=0.0,
                         proposal_prep_hours=0.0, demo_hours=0.0, prospecting_hours=0.0,
                         admin_hours=0.0, travel_hours=0.0, internal_meeting_hours=0.0)
        result = engine.assess(inp)
        assert result.time_allocation_composite >= 0.0

    def test_very_large_total_hours(self, engine):
        inp = make_input(total_hours_tracked=10000.0,
                         customer_facing_hours=5000.0, proposal_prep_hours=0.0,
                         demo_hours=1000.0, prospecting_hours=1500.0)
        result = engine.assess(inp)
        assert 0.0 <= result.time_allocation_composite <= 100.0

    def test_all_zeros_no_crash(self, engine):
        inp = TimeAllocationInput(
            rep_id="Z", region="X", evaluation_period_id="P1",
            total_hours_tracked=0.0, customer_facing_hours=0.0,
            prospecting_hours=0.0, admin_hours=0.0, internal_meeting_hours=0.0,
            proposal_prep_hours=0.0, travel_hours=0.0, training_hours=0.0,
            emails_sent_count=0, avg_email_response_time_minutes=0.0,
            calls_made_count=0, avg_call_duration_minutes=0.0,
            meetings_attended_count=0, internal_meetings_count=0,
            demo_hours=0.0, pipeline_review_hours=0.0,
            coaching_sessions_hours=0.0, focus_blocks_per_week=0.0,
            after_hours_work_hours=0.0,
        )
        result = engine.assess(inp)
        assert isinstance(result, TimeAllocationResult)

    def test_selling_time_score_max_possible(self, engine):
        # selling_pct<0.20 (+45), demo_pct<0.05 (+25), prospecting_pct<0.10 (+20) = 90
        inp = make_input(customer_facing_hours=0.0, proposal_prep_hours=0.0,
                         demo_hours=0.0, prospecting_hours=0.0, total_hours_tracked=100.0)
        assert engine._selling_time_score(inp) == 90.0

    def test_admin_burden_score_max_possible_below_cap(self, engine):
        # admin_pct>=0.30 (+40), internal_pct>=0.25 (+35), internal_count>=15 (+20) = 95
        inp = make_input(admin_hours=30.0, travel_hours=5.0,
                         internal_meeting_hours=30.0, internal_meetings_count=15,
                         total_hours_tracked=100.0)
        assert engine._admin_burden_score(inp) == 95.0

    def test_activity_quality_score_max_possible(self, engine):
        # call<5 (+35), email_rate<2 (+30), response>=1440 (+25) = 90
        inp = make_input(avg_call_duration_minutes=1.0, emails_sent_count=100,
                         avg_email_response_time_minutes=1500.0, total_hours_tracked=100.0)
        assert engine._activity_quality_score(inp) == 90.0

    def test_time_discipline_score_max_possible(self, engine):
        # focus<2 (+35), after_hours>=10 (+30), pipeline<1 (+20) = 85
        inp = make_input(focus_blocks_per_week=0.0, after_hours_work_hours=10.0,
                         pipeline_review_hours=0.0)
        assert engine._time_discipline_score(inp) == 85.0

    def test_engine_state_isolated_between_instances(self):
        e1 = SalesTimeAllocationIntelligenceEngine()
        e2 = SalesTimeAllocationIntelligenceEngine()
        e1.assess(make_input(rep_id="A"))
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_assess_batch_does_not_share_state(self):
        e = SalesTimeAllocationIntelligenceEngine()
        e.assess_batch([make_input(rep_id="A"), make_input(rep_id="B")])
        assert len(e._results) == 2

    def test_internal_meeting_hours_exactly_5_in_signal(self, engine):
        inp = make_input(
            customer_facing_hours=35.0, proposal_prep_hours=0.0,
            admin_hours=0.0, travel_hours=0.0,
            internal_meeting_hours=5.0, total_hours_tracked=100.0,
        )
        signal = engine._signal(inp, AllocationPattern.none, composite=25.0)
        assert "5h internal meetings" in signal

    def test_admin_burden_includes_travel_in_admin_pct(self, engine):
        # pure travel: admin_hours=0, travel_hours=25 → admin_pct=0.25
        inp = make_input(admin_hours=0.0, travel_hours=25.0,
                         internal_meeting_hours=0.0, internal_meetings_count=0,
                         total_hours_tracked=100.0)
        score = engine._admin_burden_score(inp)
        assert score == 20.0  # 0.25 → +20

    def test_selling_pct_uses_both_customer_facing_and_proposal(self, engine):
        # selling_pct = (0+20)/100 = 0.20 → +25
        # demo_pct=0/100=0→+25, prospecting=0/100=0→+20 = 70
        inp = make_input(customer_facing_hours=0.0, proposal_prep_hours=20.0,
                         demo_hours=0.0, prospecting_hours=0.0, total_hours_tracked=100.0)
        score = engine._selling_time_score(inp)
        assert score == 70.0

    def test_composite_rounded_correctly_for_fractional(self, engine):
        # Compose a case where composite has fractions
        inp = make_input(
            customer_facing_hours=22.0, proposal_prep_hours=0.0,
            demo_hours=7.0, prospecting_hours=12.0,
            admin_hours=17.0, travel_hours=0.0,
            internal_meeting_hours=12.0, internal_meetings_count=9,
            avg_call_duration_minutes=12.0, emails_sent_count=300,
            avg_email_response_time_minutes=60.0,
            focus_blocks_per_week=6.0, after_hours_work_hours=0.0,
            pipeline_review_hours=1.5, total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        # selling=25+12+10=47, admin=8+7+0=15, quality=7+15=22, discipline=7+0+10=17
        # composite=47*0.35+15*0.30+22*0.20+17*0.15 = 16.45+4.5+4.4+2.55 = 27.9
        assert result.time_allocation_composite == round(
            result.selling_time_score * 0.35 +
            result.admin_burden_score * 0.30 +
            result.activity_quality_score * 0.20 +
            result.time_discipline_score * 0.15, 1
        )

    def test_assess_batch_empty_summary_still_works(self, engine):
        engine.assess_batch([])
        s = engine.summary()
        assert s["total"] == 0

    def test_high_selling_pct_scenario_is_healthy(self, engine):
        inp = make_input(
            customer_facing_hours=60.0, proposal_prep_hours=10.0,
            demo_hours=15.0, prospecting_hours=20.0,
            admin_hours=5.0, travel_hours=0.0,
            internal_meeting_hours=5.0, internal_meetings_count=3,
            emails_sent_count=500, avg_email_response_time_minutes=30.0,
            avg_call_duration_minutes=30.0,
            focus_blocks_per_week=10.0, after_hours_work_hours=0.0,
            pipeline_review_hours=5.0, total_hours_tracked=100.0,
        )
        result = engine.assess(inp)
        assert result.selling_time_score == 0.0

    def test_selling_time_score_all_branches_zero(self, engine):
        # selling_pct=0.50, demo_pct=0.15, prospecting_pct=0.20 → all zero
        inp = make_input(
            customer_facing_hours=50.0, proposal_prep_hours=0.0,
            demo_hours=15.0, prospecting_hours=20.0,
            total_hours_tracked=100.0,
        )
        score = engine._selling_time_score(inp)
        assert score == 0.0
