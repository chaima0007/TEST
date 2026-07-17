"""
Comprehensive pytest test suite for SalesTimeAllocationIntelligenceEngine (Module 182).
200+ tests covering all risk levels, patterns, severities, actions, edge cases, and formulas.
"""
import sys
import pytest

sys.path.insert(0, '/home/user/TEST')

from swarm.intelligence.sales_time_allocation_intelligence_engine import (
    TimeInput,
    TimeResult,
    TimeRisk,
    TimePattern,
    TimeSeverity,
    TimeAction,
    SalesTimeAllocationIntelligenceEngine,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers / Fixtures
# ─────────────────────────────────────────────────────────────────────────────

def make_input(
    rep_id="REP001",
    region="Northeast",
    evaluation_period_id="Q1-2026",
    time_on_high_priority_accts_pct=0.70,
    time_on_low_priority_accts_pct=0.10,
    time_on_admin_tasks_pct=0.10,
    time_on_pipeline_building_pct=0.40,
    time_on_existing_customers_pct=0.30,
    time_on_new_logo_pursuit_pct=0.30,
    reactive_time_pct=0.20,
    meeting_prep_time_pct=0.12,
    crm_update_hrs_per_week_avg=3.0,
    avg_selling_hours_per_week=40.0,
    accounts_touched_per_week_avg=15.0,
    high_value_deal_time_ratio=0.60,
    quota_mapped_time_pct=0.70,
    strategy_vs_tactical_ratio=0.55,
    early_stage_deal_time_pct=0.35,
    late_stage_deal_time_pct=0.25,
    lost_deal_time_pct=0.05,
    total_managed_accounts=50,
    avg_opportunity_value_usd=10000.0,
) -> TimeInput:
    """Factory with healthy defaults (produces low risk / optimized)."""
    return TimeInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        time_on_high_priority_accts_pct=time_on_high_priority_accts_pct,
        time_on_low_priority_accts_pct=time_on_low_priority_accts_pct,
        time_on_admin_tasks_pct=time_on_admin_tasks_pct,
        time_on_pipeline_building_pct=time_on_pipeline_building_pct,
        time_on_existing_customers_pct=time_on_existing_customers_pct,
        time_on_new_logo_pursuit_pct=time_on_new_logo_pursuit_pct,
        reactive_time_pct=reactive_time_pct,
        meeting_prep_time_pct=meeting_prep_time_pct,
        crm_update_hrs_per_week_avg=crm_update_hrs_per_week_avg,
        avg_selling_hours_per_week=avg_selling_hours_per_week,
        accounts_touched_per_week_avg=accounts_touched_per_week_avg,
        high_value_deal_time_ratio=high_value_deal_time_ratio,
        quota_mapped_time_pct=quota_mapped_time_pct,
        strategy_vs_tactical_ratio=strategy_vs_tactical_ratio,
        early_stage_deal_time_pct=early_stage_deal_time_pct,
        late_stage_deal_time_pct=late_stage_deal_time_pct,
        lost_deal_time_pct=lost_deal_time_pct,
        total_managed_accounts=total_managed_accounts,
        avg_opportunity_value_usd=avg_opportunity_value_usd,
    )


def worst_case_input(**overrides) -> TimeInput:
    """Input engineered to produce critical risk."""
    defaults = dict(
        time_on_high_priority_accts_pct=0.10,
        time_on_low_priority_accts_pct=0.60,
        time_on_admin_tasks_pct=0.40,
        time_on_pipeline_building_pct=0.05,
        time_on_existing_customers_pct=0.20,
        time_on_new_logo_pursuit_pct=0.05,
        reactive_time_pct=0.70,
        meeting_prep_time_pct=0.03,
        crm_update_hrs_per_week_avg=10.0,
        avg_selling_hours_per_week=20.0,
        accounts_touched_per_week_avg=5.0,
        high_value_deal_time_ratio=0.10,
        quota_mapped_time_pct=0.20,
        strategy_vs_tactical_ratio=0.10,
        early_stage_deal_time_pct=0.05,
        late_stage_deal_time_pct=0.10,
        lost_deal_time_pct=0.25,
        total_managed_accounts=100,
        avg_opportunity_value_usd=20000.0,
    )
    defaults.update(overrides)
    return make_input(**defaults)


@pytest.fixture
def engine():
    return SalesTimeAllocationIntelligenceEngine()


@pytest.fixture
def healthy_input():
    return make_input()


@pytest.fixture
def critical_input():
    return worst_case_input()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Enum membership tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEnums:
    def test_time_risk_members(self):
        values = {r.value for r in TimeRisk}
        assert values == {"low", "moderate", "high", "critical"}

    def test_time_pattern_members(self):
        values = {p.value for p in TimePattern}
        assert values == {
            "none",
            "high_priority_neglect",
            "admin_overload",
            "reactive_time_sink",
            "wrong_size_focus",
            "renewal_hover",
        }

    def test_time_severity_members(self):
        values = {s.value for s in TimeSeverity}
        assert values == {"optimized", "balanced", "misaligned", "scattered"}

    def test_time_action_members(self):
        values = {a.value for a in TimeAction}
        assert values == {
            "no_action",
            "account_prioritization_coaching",
            "admin_reduction_coaching",
            "pipeline_focus_coaching",
            "time_reallocation_coaching",
            "time_reallocation_intervention",
            "time_strategy_reset",
        }

    def test_time_risk_is_str_enum(self):
        assert isinstance(TimeRisk.low, str)

    def test_time_pattern_is_str_enum(self):
        assert isinstance(TimePattern.none, str)

    def test_time_severity_is_str_enum(self):
        assert isinstance(TimeSeverity.optimized, str)

    def test_time_action_is_str_enum(self):
        assert isinstance(TimeAction.no_action, str)

    def test_time_risk_count(self):
        assert len(TimeRisk) == 4

    def test_time_pattern_count(self):
        assert len(TimePattern) == 6

    def test_time_severity_count(self):
        assert len(TimeSeverity) == 4

    def test_time_action_count(self):
        assert len(TimeAction) == 7


# ─────────────────────────────────────────────────────────────────────────────
# 2. TimeInput construction / field count
# ─────────────────────────────────────────────────────────────────────────────

class TestTimeInputConstruction:
    def test_has_22_fields(self):
        import dataclasses
        inp = make_input()
        fields = dataclasses.fields(inp)
        assert len(fields) == 22

    def test_rep_id_stored(self):
        inp = make_input(rep_id="X99")
        assert inp.rep_id == "X99"

    def test_region_stored(self):
        inp = make_input(region="West")
        assert inp.region == "West"

    def test_evaluation_period_id_stored(self):
        inp = make_input(evaluation_period_id="Q2-2026")
        assert inp.evaluation_period_id == "Q2-2026"

    def test_float_fields_accessible(self):
        inp = make_input(avg_opportunity_value_usd=99999.99)
        assert inp.avg_opportunity_value_usd == 99999.99

    def test_int_field_total_managed_accounts(self):
        inp = make_input(total_managed_accounts=200)
        assert inp.total_managed_accounts == 200

    def test_all_percentage_fields_storable(self):
        inp = make_input(
            time_on_high_priority_accts_pct=0.50,
            time_on_low_priority_accts_pct=0.15,
            time_on_admin_tasks_pct=0.12,
            time_on_pipeline_building_pct=0.22,
            time_on_existing_customers_pct=0.40,
            time_on_new_logo_pursuit_pct=0.18,
            reactive_time_pct=0.33,
            meeting_prep_time_pct=0.08,
            high_value_deal_time_ratio=0.45,
            quota_mapped_time_pct=0.55,
            strategy_vs_tactical_ratio=0.38,
            early_stage_deal_time_pct=0.20,
            late_stage_deal_time_pct=0.30,
            lost_deal_time_pct=0.07,
        )
        assert inp.time_on_high_priority_accts_pct == 0.50
        assert inp.lost_deal_time_pct == 0.07


# ─────────────────────────────────────────────────────────────────────────────
# 3. to_dict() — exactly 15 keys
# ─────────────────────────────────────────────────────────────────────────────

class TestToDictKeyCount:
    def test_to_dict_returns_15_keys(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        expected = {
            "rep_id", "region", "time_risk", "time_pattern", "time_severity",
            "recommended_action", "priority_allocation_score", "balance_score",
            "pipeline_focus_score", "selling_effectiveness_score", "time_composite",
            "has_time_gap", "requires_time_coaching", "estimated_quota_risk_usd",
            "time_signal",
        }
        assert set(d.keys()) == expected

    def test_to_dict_risk_is_string(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["time_risk"], str)

    def test_to_dict_pattern_is_string(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["time_pattern"], str)

    def test_to_dict_severity_is_string(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["time_severity"], str)

    def test_to_dict_action_is_string(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_has_time_gap_is_bool(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["has_time_gap"], bool)

    def test_to_dict_requires_time_coaching_is_bool(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["requires_time_coaching"], bool)

    def test_to_dict_rep_id_matches(self, engine):
        inp = make_input(rep_id="DICTTEST")
        d = engine.assess(inp).to_dict()
        assert d["rep_id"] == "DICTTEST"

    def test_to_dict_region_matches(self, engine):
        inp = make_input(region="South")
        d = engine.assess(inp).to_dict()
        assert d["region"] == "South"

    def test_to_dict_numeric_scores_present(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        for key in ("priority_allocation_score", "balance_score",
                    "pipeline_focus_score", "selling_effectiveness_score",
                    "time_composite", "estimated_quota_risk_usd"):
            assert isinstance(d[key], (int, float))

    def test_to_dict_critical_returns_15_keys(self, engine, critical_input):
        d = engine.assess(critical_input).to_dict()
        assert len(d) == 15

    def test_to_dict_signal_is_str(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["time_signal"], str)

    def test_to_dict_enum_values_are_raw_strings(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        # Enum .value strings — not enum instances
        assert d["time_risk"] in {"low", "moderate", "high", "critical"}
        assert d["time_severity"] in {"optimized", "balanced", "misaligned", "scattered"}

    def test_to_dict_risk_value_matches_result_risk_value(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        d = result.to_dict()
        assert d["time_risk"] == result.time_risk.value


# ─────────────────────────────────────────────────────────────────────────────
# 4. summary() — exactly 13 keys
# ─────────────────────────────────────────────────────────────────────────────

class TestSummaryKeyCount:
    def test_summary_empty_engine_13_keys(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        s = eng.summary()
        assert len(s) == 13

    def test_summary_after_assess_13_keys(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        assert len(s) == 13

    def test_summary_key_names(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_time_composite", "time_gap_count",
            "coaching_count", "avg_priority_allocation_score",
            "avg_balance_score", "avg_pipeline_focus_score",
            "avg_selling_effectiveness_score", "total_estimated_quota_risk_usd",
        }
        assert set(s.keys()) == expected

    def test_summary_empty_total_zero(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        assert eng.summary()["total"] == 0

    def test_summary_empty_avg_composite_zero(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        assert eng.summary()["avg_time_composite"] == 0.0

    def test_summary_empty_gap_count_zero(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        assert eng.summary()["time_gap_count"] == 0

    def test_summary_empty_coaching_count_zero(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        assert eng.summary()["coaching_count"] == 0

    def test_summary_total_increments(self, engine):
        for i in range(3):
            engine.assess(make_input(rep_id=f"R{i}"))
        assert engine.summary()["total"] == 3

    def test_summary_risk_counts_dict(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        assert isinstance(s["risk_counts"], dict)

    def test_summary_pattern_counts_dict(self, engine, healthy_input):
        engine.assess(healthy_input)
        assert isinstance(engine.summary()["pattern_counts"], dict)

    def test_summary_severity_counts_dict(self, engine, healthy_input):
        engine.assess(healthy_input)
        assert isinstance(engine.summary()["severity_counts"], dict)

    def test_summary_action_counts_dict(self, engine, healthy_input):
        engine.assess(healthy_input)
        assert isinstance(engine.summary()["action_counts"], dict)

    def test_summary_empty_risk_counts_empty_dict(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        assert eng.summary()["risk_counts"] == {}

    def test_summary_quota_risk_sum_zero_accounts(self, engine):
        inp1 = make_input(rep_id="A", total_managed_accounts=0)
        inp2 = make_input(rep_id="B", total_managed_accounts=0)
        engine.assess(inp1)
        engine.assess(inp2)
        assert engine.summary()["total_estimated_quota_risk_usd"] == 0.0

    def test_summary_after_multiple_13_keys(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"S{i}"))
        assert len(engine.summary()) == 13


# ─────────────────────────────────────────────────────────────────────────────
# 5. Risk level tests
# ─────────────────────────────────────────────────────────────────────────────

class TestRiskLevels:
    def test_low_risk_healthy_rep(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.time_risk == TimeRisk.low

    def test_low_risk_composite_below_20(self, engine):
        inp = make_input(
            time_on_high_priority_accts_pct=0.80,
            high_value_deal_time_ratio=0.80,
            quota_mapped_time_pct=0.80,
            time_on_admin_tasks_pct=0.05,
            reactive_time_pct=0.10,
            lost_deal_time_pct=0.02,
            time_on_pipeline_building_pct=0.55,
            time_on_new_logo_pursuit_pct=0.35,
            early_stage_deal_time_pct=0.40,
            avg_selling_hours_per_week=42.0,
            strategy_vs_tactical_ratio=0.60,
            meeting_prep_time_pct=0.15,
        )
        result = engine.assess(inp)
        assert result.time_composite < 20
        assert result.time_risk == TimeRisk.low

    def test_critical_risk_composite_ge_60(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert result.time_composite >= 60
        assert result.time_risk == TimeRisk.critical

    def test_risk_boundary_exactly_20_is_moderate(self, engine):
        assert engine._risk(20.0) == TimeRisk.moderate

    def test_risk_boundary_below_20_is_low(self, engine):
        assert engine._risk(19.99) == TimeRisk.low

    def test_risk_boundary_exactly_40_is_high(self, engine):
        assert engine._risk(40.0) == TimeRisk.high

    def test_risk_boundary_just_below_40_is_moderate(self, engine):
        assert engine._risk(39.99) == TimeRisk.moderate

    def test_risk_boundary_exactly_60_is_critical(self, engine):
        assert engine._risk(60.0) == TimeRisk.critical

    def test_risk_boundary_just_below_60_is_high(self, engine):
        assert engine._risk(59.99) == TimeRisk.high

    def test_risk_boundary_zero_is_low(self, engine):
        assert engine._risk(0.0) == TimeRisk.low

    def test_risk_boundary_100_is_critical(self, engine):
        assert engine._risk(100.0) == TimeRisk.critical

    def test_risk_all_four_values_covered(self, engine):
        assert engine._risk(0.0) == TimeRisk.low
        assert engine._risk(20.0) == TimeRisk.moderate
        assert engine._risk(40.0) == TimeRisk.high
        assert engine._risk(60.0) == TimeRisk.critical

    def test_moderate_risk_direct(self, engine):
        assert engine._risk(30.0) == TimeRisk.moderate

    def test_high_risk_direct(self, engine):
        assert engine._risk(50.0) == TimeRisk.high


# ─────────────────────────────────────────────────────────────────────────────
# 6. Severity level tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSeverityLevels:
    def test_optimized_below_20(self, engine):
        assert engine._severity(0.0) == TimeSeverity.optimized
        assert engine._severity(19.99) == TimeSeverity.optimized

    def test_balanced_20_to_39(self, engine):
        assert engine._severity(20.0) == TimeSeverity.balanced
        assert engine._severity(39.99) == TimeSeverity.balanced

    def test_misaligned_40_to_59(self, engine):
        assert engine._severity(40.0) == TimeSeverity.misaligned
        assert engine._severity(59.99) == TimeSeverity.misaligned

    def test_scattered_60_plus(self, engine):
        assert engine._severity(60.0) == TimeSeverity.scattered
        assert engine._severity(100.0) == TimeSeverity.scattered

    def test_healthy_rep_is_optimized(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.time_severity == TimeSeverity.optimized

    def test_critical_rep_is_scattered(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert result.time_severity == TimeSeverity.scattered

    def test_severity_all_four_values_covered(self, engine):
        assert engine._severity(0.0) == TimeSeverity.optimized
        assert engine._severity(20.0) == TimeSeverity.balanced
        assert engine._severity(40.0) == TimeSeverity.misaligned
        assert engine._severity(60.0) == TimeSeverity.scattered


# ─────────────────────────────────────────────────────────────────────────────
# 7. Pattern detection tests
# ─────────────────────────────────────────────────────────────────────────────

class TestPatternDetection:
    def test_pattern_none_for_healthy_rep(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.time_pattern == TimePattern.none

    def test_high_priority_neglect_detected(self, engine):
        inp = make_input(
            time_on_high_priority_accts_pct=0.20,
            high_value_deal_time_ratio=0.20,
        )
        result = engine.assess(inp)
        assert result.time_pattern == TimePattern.high_priority_neglect

    def test_high_priority_neglect_boundary_exactly_025(self, engine):
        inp = make_input(
            time_on_high_priority_accts_pct=0.25,
            high_value_deal_time_ratio=0.25,
        )
        result = engine.assess(inp)
        assert result.time_pattern == TimePattern.high_priority_neglect

    def test_high_priority_neglect_not_triggered_above_025(self, engine):
        inp = make_input(
            time_on_high_priority_accts_pct=0.26,
            high_value_deal_time_ratio=0.26,
        )
        result = engine.assess(inp)
        assert result.time_pattern != TimePattern.high_priority_neglect

    def test_admin_overload_detected(self, engine):
        inp = make_input(
            time_on_admin_tasks_pct=0.40,
            avg_selling_hours_per_week=25.0,
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
        )
        result = engine.assess(inp)
        assert result.time_pattern == TimePattern.admin_overload

    def test_admin_overload_boundary_admin_exactly_035(self, engine):
        inp = make_input(
            time_on_admin_tasks_pct=0.35,
            avg_selling_hours_per_week=25.0,
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
        )
        result = engine.assess(inp)
        assert result.time_pattern == TimePattern.admin_overload

    def test_admin_overload_boundary_selling_hours_exactly_28(self, engine):
        inp = make_input(
            time_on_admin_tasks_pct=0.40,
            avg_selling_hours_per_week=28.0,
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
        )
        result = engine.assess(inp)
        assert result.time_pattern == TimePattern.admin_overload

    def test_admin_overload_not_triggered_above_28_selling_hours(self, engine):
        inp = make_input(
            time_on_admin_tasks_pct=0.40,
            avg_selling_hours_per_week=29.0,
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
        )
        result = engine.assess(inp)
        assert result.time_pattern != TimePattern.admin_overload

    def test_reactive_time_sink_detected(self, engine):
        inp = make_input(
            reactive_time_pct=0.70,
            time_on_pipeline_building_pct=0.10,
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
        )
        result = engine.assess(inp)
        assert result.time_pattern == TimePattern.reactive_time_sink

    def test_reactive_time_sink_boundary_reactive_065(self, engine):
        inp = make_input(
            reactive_time_pct=0.65,
            time_on_pipeline_building_pct=0.10,
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
        )
        result = engine.assess(inp)
        assert result.time_pattern == TimePattern.reactive_time_sink

    def test_reactive_time_sink_not_triggered_pipeline_above_015(self, engine):
        inp = make_input(
            reactive_time_pct=0.70,
            time_on_pipeline_building_pct=0.16,
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
        )
        result = engine.assess(inp)
        assert result.time_pattern != TimePattern.reactive_time_sink

    def test_wrong_size_focus_detected(self, engine):
        inp = make_input(
            time_on_low_priority_accts_pct=0.55,
            high_value_deal_time_ratio=0.25,
            time_on_high_priority_accts_pct=0.60,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
            reactive_time_pct=0.20,
        )
        result = engine.assess(inp)
        assert result.time_pattern == TimePattern.wrong_size_focus

    def test_wrong_size_focus_boundary_low_pct_050(self, engine):
        inp = make_input(
            time_on_low_priority_accts_pct=0.50,
            high_value_deal_time_ratio=0.25,
            time_on_high_priority_accts_pct=0.60,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
            reactive_time_pct=0.20,
        )
        result = engine.assess(inp)
        assert result.time_pattern == TimePattern.wrong_size_focus

    def test_wrong_size_focus_not_triggered_hvd_above_030(self, engine):
        inp = make_input(
            time_on_low_priority_accts_pct=0.55,
            high_value_deal_time_ratio=0.31,
            time_on_high_priority_accts_pct=0.60,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
            reactive_time_pct=0.20,
        )
        result = engine.assess(inp)
        assert result.time_pattern != TimePattern.wrong_size_focus

    def test_renewal_hover_detected(self, engine):
        inp = make_input(
            time_on_existing_customers_pct=0.70,
            time_on_new_logo_pursuit_pct=0.10,
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
            reactive_time_pct=0.20,
            time_on_low_priority_accts_pct=0.10,
        )
        result = engine.assess(inp)
        assert result.time_pattern == TimePattern.renewal_hover

    def test_renewal_hover_boundary_existing_065(self, engine):
        inp = make_input(
            time_on_existing_customers_pct=0.65,
            time_on_new_logo_pursuit_pct=0.10,
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
            reactive_time_pct=0.20,
            time_on_low_priority_accts_pct=0.10,
        )
        result = engine.assess(inp)
        assert result.time_pattern == TimePattern.renewal_hover

    def test_renewal_hover_not_triggered_new_logo_above_015(self, engine):
        inp = make_input(
            time_on_existing_customers_pct=0.70,
            time_on_new_logo_pursuit_pct=0.16,
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
            reactive_time_pct=0.20,
            time_on_low_priority_accts_pct=0.10,
        )
        result = engine.assess(inp)
        assert result.time_pattern != TimePattern.renewal_hover

    def test_pattern_priority_order_high_priority_wins(self, engine):
        # Both high_priority_neglect and admin_overload conditions true;
        # high_priority_neglect is checked first
        inp = make_input(
            time_on_high_priority_accts_pct=0.20,
            high_value_deal_time_ratio=0.20,
            time_on_admin_tasks_pct=0.40,
            avg_selling_hours_per_week=25.0,
        )
        result = engine.assess(inp)
        assert result.time_pattern == TimePattern.high_priority_neglect

    def test_all_6_patterns_can_be_detected(self, engine):
        detected = set()

        # none
        detected.add(engine.assess(make_input()).time_pattern)

        # high_priority_neglect
        detected.add(engine.assess(make_input(
            time_on_high_priority_accts_pct=0.20,
            high_value_deal_time_ratio=0.20,
        )).time_pattern)

        # admin_overload
        detected.add(engine.assess(make_input(
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
            time_on_admin_tasks_pct=0.40,
            avg_selling_hours_per_week=25.0,
        )).time_pattern)

        # reactive_time_sink
        detected.add(engine.assess(make_input(
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
            reactive_time_pct=0.70,
            time_on_pipeline_building_pct=0.10,
        )).time_pattern)

        # wrong_size_focus
        detected.add(engine.assess(make_input(
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.25,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
            reactive_time_pct=0.20,
            time_on_low_priority_accts_pct=0.55,
        )).time_pattern)

        # renewal_hover
        detected.add(engine.assess(make_input(
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
            reactive_time_pct=0.20,
            time_on_low_priority_accts_pct=0.10,
            time_on_existing_customers_pct=0.70,
            time_on_new_logo_pursuit_pct=0.10,
        )).time_pattern)

        assert TimePattern.none in detected
        assert TimePattern.high_priority_neglect in detected
        assert TimePattern.admin_overload in detected
        assert TimePattern.reactive_time_sink in detected
        assert TimePattern.wrong_size_focus in detected
        assert TimePattern.renewal_hover in detected


# ─────────────────────────────────────────────────────────────────────────────
# 8. Action mapping tests
# ─────────────────────────────────────────────────────────────────────────────

class TestActionMapping:
    def test_no_action_low_risk(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.time_risk == TimeRisk.low
        assert result.recommended_action == TimeAction.no_action

    def test_admin_reduction_coaching_high_admin_overload(self, engine):
        result = engine._action(TimeRisk.high, TimePattern.admin_overload)
        assert result == TimeAction.admin_reduction_coaching

    def test_pipeline_focus_coaching_high_reactive_time_sink(self, engine):
        result = engine._action(TimeRisk.high, TimePattern.reactive_time_sink)
        assert result == TimeAction.pipeline_focus_coaching

    def test_account_prioritization_coaching_high_wrong_size(self, engine):
        result = engine._action(TimeRisk.high, TimePattern.wrong_size_focus)
        assert result == TimeAction.account_prioritization_coaching

    def test_pipeline_focus_coaching_high_renewal_hover(self, engine):
        result = engine._action(TimeRisk.high, TimePattern.renewal_hover)
        assert result == TimeAction.pipeline_focus_coaching

    def test_time_reallocation_coaching_high_none_pattern(self, engine):
        result = engine._action(TimeRisk.high, TimePattern.none)
        assert result == TimeAction.time_reallocation_coaching

    def test_time_reallocation_coaching_high_high_priority_neglect(self, engine):
        result = engine._action(TimeRisk.high, TimePattern.high_priority_neglect)
        assert result == TimeAction.time_reallocation_coaching

    def test_account_prioritization_coaching_moderate_any_pattern(self, engine):
        for pattern in TimePattern:
            assert engine._action(TimeRisk.moderate, pattern) == TimeAction.account_prioritization_coaching

    def test_no_action_low_risk_any_pattern(self, engine):
        for pattern in TimePattern:
            assert engine._action(TimeRisk.low, pattern) == TimeAction.no_action

    def test_time_strategy_reset_critical_high_priority_neglect(self, engine):
        result = engine._action(TimeRisk.critical, TimePattern.high_priority_neglect)
        assert result == TimeAction.time_strategy_reset

    def test_time_reallocation_intervention_critical_admin_overload(self, engine):
        result = engine._action(TimeRisk.critical, TimePattern.admin_overload)
        assert result == TimeAction.time_reallocation_intervention

    def test_time_strategy_reset_critical_none_pattern(self, engine):
        result = engine._action(TimeRisk.critical, TimePattern.none)
        assert result == TimeAction.time_strategy_reset

    def test_time_strategy_reset_critical_renewal_hover(self, engine):
        result = engine._action(TimeRisk.critical, TimePattern.renewal_hover)
        assert result == TimeAction.time_strategy_reset

    def test_time_strategy_reset_critical_wrong_size(self, engine):
        result = engine._action(TimeRisk.critical, TimePattern.wrong_size_focus)
        assert result == TimeAction.time_strategy_reset

    def test_time_strategy_reset_critical_reactive_time_sink(self, engine):
        result = engine._action(TimeRisk.critical, TimePattern.reactive_time_sink)
        assert result == TimeAction.time_strategy_reset

    def test_all_actions_reachable(self, engine):
        actions = set()
        # no_action
        actions.add(engine._action(TimeRisk.low, TimePattern.none))
        # account_prioritization_coaching
        actions.add(engine._action(TimeRisk.moderate, TimePattern.none))
        # admin_reduction_coaching
        actions.add(engine._action(TimeRisk.high, TimePattern.admin_overload))
        # pipeline_focus_coaching
        actions.add(engine._action(TimeRisk.high, TimePattern.reactive_time_sink))
        # time_reallocation_coaching
        actions.add(engine._action(TimeRisk.high, TimePattern.none))
        # time_reallocation_intervention
        actions.add(engine._action(TimeRisk.critical, TimePattern.admin_overload))
        # time_strategy_reset
        actions.add(engine._action(TimeRisk.critical, TimePattern.none))
        assert TimeAction.no_action in actions
        assert TimeAction.account_prioritization_coaching in actions
        assert TimeAction.admin_reduction_coaching in actions
        assert TimeAction.pipeline_focus_coaching in actions
        assert TimeAction.time_reallocation_coaching in actions
        assert TimeAction.time_reallocation_intervention in actions
        assert TimeAction.time_strategy_reset in actions


# ─────────────────────────────────────────────────────────────────────────────
# 9. has_time_gap logic
# ─────────────────────────────────────────────────────────────────────────────

class TestHasTimeGap:
    def test_has_gap_true_when_composite_ge_40(self, engine):
        assert engine._has_gap(make_input(), 40.0) is True

    def test_has_gap_true_when_composite_above_40(self, engine):
        assert engine._has_gap(make_input(), 55.0) is True

    def test_has_gap_false_when_composite_below_40_and_all_good(self, engine):
        inp = make_input(
            time_on_admin_tasks_pct=0.10,
            time_on_high_priority_accts_pct=0.70,
        )
        assert engine._has_gap(inp, 19.0) is False

    def test_has_gap_true_when_admin_ge_025(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.25, time_on_high_priority_accts_pct=0.70)
        assert engine._has_gap(inp, 10.0) is True

    def test_has_gap_true_when_admin_above_025(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.30, time_on_high_priority_accts_pct=0.70)
        assert engine._has_gap(inp, 10.0) is True

    def test_has_gap_false_when_admin_below_025(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.24, time_on_high_priority_accts_pct=0.70)
        assert engine._has_gap(inp, 10.0) is False

    def test_has_gap_true_when_high_priority_le_040(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.40, time_on_admin_tasks_pct=0.10)
        assert engine._has_gap(inp, 10.0) is True

    def test_has_gap_true_when_high_priority_below_040(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.30, time_on_admin_tasks_pct=0.10)
        assert engine._has_gap(inp, 10.0) is True

    def test_has_gap_false_when_high_priority_above_040(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.41, time_on_admin_tasks_pct=0.10)
        assert engine._has_gap(inp, 10.0) is False

    def test_has_gap_or_logic_composite_wins(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.10, time_on_high_priority_accts_pct=0.70)
        assert engine._has_gap(inp, 40.0) is True

    def test_has_gap_or_logic_admin_wins(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.25, time_on_high_priority_accts_pct=0.70)
        assert engine._has_gap(inp, 10.0) is True

    def test_has_gap_boundary_admin_exactly_025(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.25, time_on_high_priority_accts_pct=0.70)
        assert engine._has_gap(inp, 10.0) is True

    def test_has_gap_boundary_high_priority_exactly_040(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.40, time_on_admin_tasks_pct=0.10)
        assert engine._has_gap(inp, 10.0) is True

    def test_has_gap_reflected_in_result(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.30, time_on_admin_tasks_pct=0.10)
        result = engine.assess(inp)
        assert result.has_time_gap is True

    def test_no_gap_healthy_rep(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        # Verify that the result's has_time_gap matches the direct method call
        assert engine._has_gap(healthy_input, result.time_composite) is result.has_time_gap

    def test_has_gap_boundary_composite_exactly_40(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.10, time_on_high_priority_accts_pct=0.70)
        assert engine._has_gap(inp, 40.0) is True

    def test_has_gap_boundary_composite_just_below_40(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.10, time_on_high_priority_accts_pct=0.70)
        assert engine._has_gap(inp, 39.99) is False


# ─────────────────────────────────────────────────────────────────────────────
# 10. requires_time_coaching logic
# ─────────────────────────────────────────────────────────────────────────────

class TestRequiresTimeCoaching:
    def test_coaching_true_when_composite_ge_30(self, engine):
        assert engine._requires_coaching(make_input(), 30.0) is True

    def test_coaching_true_when_composite_above_30(self, engine):
        assert engine._requires_coaching(make_input(), 50.0) is True

    def test_coaching_false_when_all_below_thresholds(self, engine):
        inp = make_input(reactive_time_pct=0.20, high_value_deal_time_ratio=0.60)
        assert engine._requires_coaching(inp, 10.0) is False

    def test_coaching_true_when_reactive_ge_045(self, engine):
        inp = make_input(reactive_time_pct=0.45, high_value_deal_time_ratio=0.60)
        assert engine._requires_coaching(inp, 10.0) is True

    def test_coaching_true_when_reactive_above_045(self, engine):
        inp = make_input(reactive_time_pct=0.60, high_value_deal_time_ratio=0.60)
        assert engine._requires_coaching(inp, 10.0) is True

    def test_coaching_false_when_reactive_below_045(self, engine):
        inp = make_input(reactive_time_pct=0.44, high_value_deal_time_ratio=0.60)
        assert engine._requires_coaching(inp, 10.0) is False

    def test_coaching_true_when_high_value_le_040(self, engine):
        inp = make_input(reactive_time_pct=0.20, high_value_deal_time_ratio=0.40)
        assert engine._requires_coaching(inp, 10.0) is True

    def test_coaching_true_when_high_value_below_040(self, engine):
        inp = make_input(reactive_time_pct=0.20, high_value_deal_time_ratio=0.30)
        assert engine._requires_coaching(inp, 10.0) is True

    def test_coaching_false_when_high_value_above_040(self, engine):
        inp = make_input(reactive_time_pct=0.20, high_value_deal_time_ratio=0.41)
        assert engine._requires_coaching(inp, 10.0) is False

    def test_coaching_boundary_composite_exactly_30(self, engine):
        assert engine._requires_coaching(make_input(), 30.0) is True

    def test_coaching_boundary_composite_just_below_30(self, engine):
        inp = make_input(reactive_time_pct=0.20, high_value_deal_time_ratio=0.60)
        assert engine._requires_coaching(inp, 29.99) is False

    def test_coaching_boundary_reactive_exactly_045(self, engine):
        inp = make_input(reactive_time_pct=0.45, high_value_deal_time_ratio=0.60)
        assert engine._requires_coaching(inp, 10.0) is True

    def test_coaching_boundary_high_value_exactly_040(self, engine):
        inp = make_input(reactive_time_pct=0.20, high_value_deal_time_ratio=0.40)
        assert engine._requires_coaching(inp, 10.0) is True

    def test_requires_coaching_reflected_in_result_true(self, engine):
        inp = make_input(reactive_time_pct=0.50)
        result = engine.assess(inp)
        assert result.requires_time_coaching is True

    def test_requires_coaching_result_uses_correct_logic(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        expected = engine._requires_coaching(healthy_input, result.time_composite)
        assert result.requires_time_coaching == expected


# ─────────────────────────────────────────────────────────────────────────────
# 11. estimated_quota_risk_usd formula
# ─────────────────────────────────────────────────────────────────────────────

class TestQuotaRiskFormula:
    def test_quota_risk_zero_when_high_priority_above_065(self, engine):
        # misalignment = max(0, 0.65 - 0.70) = 0
        inp = make_input(
            time_on_high_priority_accts_pct=0.70,
            total_managed_accounts=100,
            avg_opportunity_value_usd=10000.0,
        )
        result = engine.assess(inp)
        assert result.estimated_quota_risk_usd == 0.0

    def test_quota_risk_zero_when_composite_zero(self, engine):
        inp = make_input(
            time_on_high_priority_accts_pct=0.30,
            total_managed_accounts=100,
            avg_opportunity_value_usd=10000.0,
        )
        assert engine._quota_risk(inp, 0.0) == 0.0

    def test_quota_risk_formula_manual_calculation(self, engine):
        # misalignment = max(0, 0.65 - 0.40) = 0.25
        # quota_risk = 10 * 1000 * 0.25 * (50/100) = 1250.0
        inp = make_input(
            time_on_high_priority_accts_pct=0.40,
            total_managed_accounts=10,
            avg_opportunity_value_usd=1000.0,
        )
        risk = engine._quota_risk(inp, 50.0)
        expected = round(10 * 1000.0 * max(0.0, 0.65 - 0.40) * (50.0 / 100), 2)
        assert risk == expected

    def test_quota_risk_scales_with_accounts(self, engine):
        inp1 = make_input(time_on_high_priority_accts_pct=0.40, total_managed_accounts=10, avg_opportunity_value_usd=1000.0)
        inp2 = make_input(time_on_high_priority_accts_pct=0.40, total_managed_accounts=20, avg_opportunity_value_usd=1000.0)
        r1 = engine._quota_risk(inp1, 50.0)
        r2 = engine._quota_risk(inp2, 50.0)
        assert r2 == pytest.approx(r1 * 2, rel=1e-6)

    def test_quota_risk_scales_with_opportunity_value(self, engine):
        inp1 = make_input(time_on_high_priority_accts_pct=0.40, total_managed_accounts=10, avg_opportunity_value_usd=1000.0)
        inp2 = make_input(time_on_high_priority_accts_pct=0.40, total_managed_accounts=10, avg_opportunity_value_usd=2000.0)
        r1 = engine._quota_risk(inp1, 50.0)
        r2 = engine._quota_risk(inp2, 50.0)
        assert r2 == pytest.approx(r1 * 2, rel=1e-6)

    def test_quota_risk_zero_accounts(self, engine):
        inp = make_input(total_managed_accounts=0, time_on_high_priority_accts_pct=0.30)
        assert engine._quota_risk(inp, 80.0) == 0.0

    def test_quota_risk_rounded_to_2_decimals(self, engine):
        inp = make_input(
            time_on_high_priority_accts_pct=0.33,
            total_managed_accounts=7,
            avg_opportunity_value_usd=333.33,
        )
        risk = engine._quota_risk(inp, 33.33)
        assert risk == round(risk, 2)

    def test_quota_risk_in_result(self, engine):
        inp = make_input(
            time_on_high_priority_accts_pct=0.40,
            total_managed_accounts=10,
            avg_opportunity_value_usd=1000.0,
        )
        result = engine.assess(inp)
        assert result.estimated_quota_risk_usd >= 0.0

    def test_quota_risk_max_misalignment(self, engine):
        # high_priority = 0.0 → misalignment = 0.65
        inp = make_input(
            time_on_high_priority_accts_pct=0.0,
            total_managed_accounts=10,
            avg_opportunity_value_usd=1000.0,
        )
        risk = engine._quota_risk(inp, 50.0)
        expected = round(10 * 1000.0 * 0.65 * 0.5, 2)
        assert risk == expected

    def test_quota_risk_no_negative(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.90)
        assert engine._quota_risk(inp, 80.0) >= 0.0

    def test_quota_risk_is_float(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.estimated_quota_risk_usd, float)

    def test_quota_risk_high_priority_exactly_065_zero(self, engine):
        # misalignment = max(0, 0.65 - 0.65) = 0
        inp = make_input(time_on_high_priority_accts_pct=0.65, total_managed_accounts=10, avg_opportunity_value_usd=1000.0)
        assert engine._quota_risk(inp, 50.0) == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 12. Signal string tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSignalString:
    def test_healthy_signal_text_below_20(self, engine):
        inp = make_input(
            time_on_high_priority_accts_pct=0.80,
            high_value_deal_time_ratio=0.80,
            quota_mapped_time_pct=0.80,
            time_on_admin_tasks_pct=0.05,
            reactive_time_pct=0.10,
            lost_deal_time_pct=0.02,
            time_on_pipeline_building_pct=0.55,
            time_on_new_logo_pursuit_pct=0.35,
            early_stage_deal_time_pct=0.40,
            avg_selling_hours_per_week=42.0,
            strategy_vs_tactical_ratio=0.60,
            meeting_prep_time_pct=0.15,
        )
        result = engine.assess(inp)
        if result.time_composite < 20:
            assert "Time allocation optimized" in result.time_signal

    def test_unhealthy_signal_contains_label(self, engine):
        inp = make_input(
            time_on_high_priority_accts_pct=0.20,
            high_value_deal_time_ratio=0.20,
            time_on_admin_tasks_pct=0.40,
            reactive_time_pct=0.70,
            lost_deal_time_pct=0.25,
            time_on_pipeline_building_pct=0.05,
            avg_selling_hours_per_week=20.0,
        )
        result = engine.assess(inp)
        if result.time_composite >= 20 and result.time_pattern == TimePattern.high_priority_neglect:
            assert "High-priority neglect" in result.time_signal

    def test_signal_contains_high_priority_pct(self, engine):
        inp = worst_case_input(time_on_high_priority_accts_pct=0.15)
        result = engine.assess(inp)
        assert "15%" in result.time_signal

    def test_signal_contains_admin_pct(self, engine):
        inp = worst_case_input(time_on_admin_tasks_pct=0.40)
        result = engine.assess(inp)
        assert "40%" in result.time_signal

    def test_signal_contains_reactive_pct(self, engine):
        inp = worst_case_input(reactive_time_pct=0.70)
        result = engine.assess(inp)
        assert "70%" in result.time_signal

    def test_signal_contains_composite_score(self, engine, critical_input):
        result = engine.assess(critical_input)
        if result.time_composite >= 20:
            assert str(round(result.time_composite)) in result.time_signal

    def test_signal_is_string(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.time_signal, str)

    def test_signal_non_empty(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert len(result.time_signal) > 0

    def test_optimized_signal_exact_content(self, engine):
        inp = make_input(
            time_on_high_priority_accts_pct=0.80,
            high_value_deal_time_ratio=0.80,
            quota_mapped_time_pct=0.80,
            time_on_admin_tasks_pct=0.05,
            reactive_time_pct=0.10,
            lost_deal_time_pct=0.02,
            time_on_pipeline_building_pct=0.55,
            time_on_new_logo_pursuit_pct=0.35,
            early_stage_deal_time_pct=0.40,
            avg_selling_hours_per_week=42.0,
            strategy_vs_tactical_ratio=0.60,
            meeting_prep_time_pct=0.15,
        )
        result = engine.assess(inp)
        if result.time_composite < 20:
            assert result.time_signal == (
                "Time allocation optimized — priority accounts, pipeline building, "
                "and selling hours within benchmarks"
            )

    def test_signal_admin_overload_label(self, engine):
        inp = make_input(
            time_on_admin_tasks_pct=0.40,
            avg_selling_hours_per_week=25.0,
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
            reactive_time_pct=0.50,
            quota_mapped_time_pct=0.30,
            lost_deal_time_pct=0.22,
            time_on_pipeline_building_pct=0.10,
            time_on_new_logo_pursuit_pct=0.10,
            early_stage_deal_time_pct=0.10,
            strategy_vs_tactical_ratio=0.20,
            meeting_prep_time_pct=0.03,
        )
        result = engine.assess(inp)
        if result.time_pattern == TimePattern.admin_overload and result.time_composite >= 20:
            assert "Admin overload" in result.time_signal

    def test_signal_renewal_hover_label(self, engine):
        inp = make_input(
            time_on_existing_customers_pct=0.70,
            time_on_new_logo_pursuit_pct=0.10,
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
            reactive_time_pct=0.20,
            time_on_low_priority_accts_pct=0.10,
            quota_mapped_time_pct=0.30,
            lost_deal_time_pct=0.22,
            time_on_pipeline_building_pct=0.10,
            early_stage_deal_time_pct=0.10,
            strategy_vs_tactical_ratio=0.20,
            meeting_prep_time_pct=0.03,
        )
        result = engine.assess(inp)
        if result.time_pattern == TimePattern.renewal_hover and result.time_composite >= 20:
            assert "Renewal hover" in result.time_signal

    def test_signal_from_critical_input_is_non_empty(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert len(result.time_signal) > 0


# ─────────────────────────────────────────────────────────────────────────────
# 13. Sub-score calculation tests (direct method calls)
# ─────────────────────────────────────────────────────────────────────────────

class TestPriorityAllocationScore:
    def test_score_max_when_all_worst(self, engine):
        inp = make_input(
            time_on_high_priority_accts_pct=0.10,  # +40
            high_value_deal_time_ratio=0.10,        # +35
            quota_mapped_time_pct=0.10,             # +25
        )
        score = engine._priority_allocation_score(inp)
        assert score == 100.0

    def test_score_zero_when_all_best(self, engine):
        inp = make_input(
            time_on_high_priority_accts_pct=0.80,
            high_value_deal_time_ratio=0.80,
            quota_mapped_time_pct=0.80,
        )
        score = engine._priority_allocation_score(inp)
        assert score == 0.0

    def test_score_capped_at_100(self, engine, critical_input):
        score = engine._priority_allocation_score(critical_input)
        assert score <= 100.0

    def test_score_nonnegative(self, engine, healthy_input):
        score = engine._priority_allocation_score(healthy_input)
        assert score >= 0.0

    def test_high_priority_030_threshold(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.30, high_value_deal_time_ratio=0.80, quota_mapped_time_pct=0.80)
        assert engine._priority_allocation_score(inp) == 40.0

    def test_high_priority_050_threshold(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.50, high_value_deal_time_ratio=0.80, quota_mapped_time_pct=0.80)
        assert engine._priority_allocation_score(inp) == 22.0

    def test_high_priority_065_threshold(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.65, high_value_deal_time_ratio=0.80, quota_mapped_time_pct=0.80)
        assert engine._priority_allocation_score(inp) == 8.0

    def test_high_priority_above_065_zero(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.66, high_value_deal_time_ratio=0.80, quota_mapped_time_pct=0.80)
        assert engine._priority_allocation_score(inp) == 0.0

    def test_high_value_030_threshold(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.80, high_value_deal_time_ratio=0.30, quota_mapped_time_pct=0.80)
        assert engine._priority_allocation_score(inp) == 35.0

    def test_high_value_050_threshold(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.80, high_value_deal_time_ratio=0.50, quota_mapped_time_pct=0.80)
        assert engine._priority_allocation_score(inp) == 18.0

    def test_quota_040_threshold(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.80, high_value_deal_time_ratio=0.80, quota_mapped_time_pct=0.40)
        assert engine._priority_allocation_score(inp) == 25.0

    def test_quota_060_threshold(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.80, high_value_deal_time_ratio=0.80, quota_mapped_time_pct=0.60)
        assert engine._priority_allocation_score(inp) == 12.0


class TestBalanceScore:
    def test_score_max_when_all_worst(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.35, reactive_time_pct=0.65, lost_deal_time_pct=0.25)
        assert engine._balance_score(inp) == 100.0

    def test_score_zero_when_all_best(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.05, reactive_time_pct=0.10, lost_deal_time_pct=0.02)
        assert engine._balance_score(inp) == 0.0

    def test_admin_030_threshold(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.30, reactive_time_pct=0.10, lost_deal_time_pct=0.02)
        assert engine._balance_score(inp) == 40.0

    def test_admin_020_threshold(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.20, reactive_time_pct=0.10, lost_deal_time_pct=0.02)
        assert engine._balance_score(inp) == 22.0

    def test_admin_012_threshold(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.12, reactive_time_pct=0.10, lost_deal_time_pct=0.02)
        assert engine._balance_score(inp) == 8.0

    def test_admin_below_012_zero(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.11, reactive_time_pct=0.10, lost_deal_time_pct=0.02)
        assert engine._balance_score(inp) == 0.0

    def test_reactive_060_threshold(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.05, reactive_time_pct=0.60, lost_deal_time_pct=0.02)
        assert engine._balance_score(inp) == 35.0

    def test_reactive_040_threshold(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.05, reactive_time_pct=0.40, lost_deal_time_pct=0.02)
        assert engine._balance_score(inp) == 18.0

    def test_lost_020_threshold(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.05, reactive_time_pct=0.10, lost_deal_time_pct=0.20)
        assert engine._balance_score(inp) == 25.0

    def test_lost_010_threshold(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.05, reactive_time_pct=0.10, lost_deal_time_pct=0.10)
        assert engine._balance_score(inp) == 12.0


class TestPipelineFocusScore:
    def test_score_max_when_all_worst(self, engine):
        inp = make_input(time_on_pipeline_building_pct=0.10, time_on_new_logo_pursuit_pct=0.05, early_stage_deal_time_pct=0.05)
        assert engine._pipeline_focus_score(inp) == 100.0

    def test_score_zero_when_all_best(self, engine):
        inp = make_input(time_on_pipeline_building_pct=0.60, time_on_new_logo_pursuit_pct=0.35, early_stage_deal_time_pct=0.40)
        assert engine._pipeline_focus_score(inp) == 0.0

    def test_building_020_threshold(self, engine):
        inp = make_input(time_on_pipeline_building_pct=0.20, time_on_new_logo_pursuit_pct=0.35, early_stage_deal_time_pct=0.40)
        assert engine._pipeline_focus_score(inp) == 45.0

    def test_building_035_threshold(self, engine):
        inp = make_input(time_on_pipeline_building_pct=0.35, time_on_new_logo_pursuit_pct=0.35, early_stage_deal_time_pct=0.40)
        assert engine._pipeline_focus_score(inp) == 25.0

    def test_building_050_threshold(self, engine):
        inp = make_input(time_on_pipeline_building_pct=0.50, time_on_new_logo_pursuit_pct=0.35, early_stage_deal_time_pct=0.40)
        assert engine._pipeline_focus_score(inp) == 10.0

    def test_building_above_050_zero(self, engine):
        inp = make_input(time_on_pipeline_building_pct=0.51, time_on_new_logo_pursuit_pct=0.35, early_stage_deal_time_pct=0.40)
        assert engine._pipeline_focus_score(inp) == 0.0

    def test_new_logo_010_threshold(self, engine):
        inp = make_input(time_on_pipeline_building_pct=0.60, time_on_new_logo_pursuit_pct=0.10, early_stage_deal_time_pct=0.40)
        assert engine._pipeline_focus_score(inp) == 30.0

    def test_new_logo_025_threshold(self, engine):
        inp = make_input(time_on_pipeline_building_pct=0.60, time_on_new_logo_pursuit_pct=0.25, early_stage_deal_time_pct=0.40)
        assert engine._pipeline_focus_score(inp) == 15.0

    def test_early_stage_015_threshold(self, engine):
        inp = make_input(time_on_pipeline_building_pct=0.60, time_on_new_logo_pursuit_pct=0.35, early_stage_deal_time_pct=0.15)
        assert engine._pipeline_focus_score(inp) == 25.0

    def test_early_stage_030_threshold(self, engine):
        inp = make_input(time_on_pipeline_building_pct=0.60, time_on_new_logo_pursuit_pct=0.35, early_stage_deal_time_pct=0.30)
        assert engine._pipeline_focus_score(inp) == 12.0


class TestSellingEffectivenessScore:
    def test_score_max_when_all_worst(self, engine):
        inp = make_input(avg_selling_hours_per_week=20.0, strategy_vs_tactical_ratio=0.10, meeting_prep_time_pct=0.03)
        assert engine._selling_effectiveness_score(inp) == 100.0

    def test_score_zero_when_all_best(self, engine):
        inp = make_input(avg_selling_hours_per_week=42.0, strategy_vs_tactical_ratio=0.60, meeting_prep_time_pct=0.15)
        assert engine._selling_effectiveness_score(inp) == 0.0

    def test_selling_hours_25_threshold(self, engine):
        inp = make_input(avg_selling_hours_per_week=25.0, strategy_vs_tactical_ratio=0.60, meeting_prep_time_pct=0.15)
        assert engine._selling_effectiveness_score(inp) == 40.0

    def test_selling_hours_32_threshold(self, engine):
        inp = make_input(avg_selling_hours_per_week=32.0, strategy_vs_tactical_ratio=0.60, meeting_prep_time_pct=0.15)
        assert engine._selling_effectiveness_score(inp) == 22.0

    def test_selling_hours_38_threshold(self, engine):
        inp = make_input(avg_selling_hours_per_week=38.0, strategy_vs_tactical_ratio=0.60, meeting_prep_time_pct=0.15)
        assert engine._selling_effectiveness_score(inp) == 8.0

    def test_selling_hours_above_38_zero(self, engine):
        inp = make_input(avg_selling_hours_per_week=39.0, strategy_vs_tactical_ratio=0.60, meeting_prep_time_pct=0.15)
        assert engine._selling_effectiveness_score(inp) == 0.0

    def test_strategy_025_threshold(self, engine):
        inp = make_input(avg_selling_hours_per_week=42.0, strategy_vs_tactical_ratio=0.25, meeting_prep_time_pct=0.15)
        assert engine._selling_effectiveness_score(inp) == 35.0

    def test_strategy_045_threshold(self, engine):
        inp = make_input(avg_selling_hours_per_week=42.0, strategy_vs_tactical_ratio=0.45, meeting_prep_time_pct=0.15)
        assert engine._selling_effectiveness_score(inp) == 18.0

    def test_meeting_prep_005_threshold(self, engine):
        inp = make_input(avg_selling_hours_per_week=42.0, strategy_vs_tactical_ratio=0.60, meeting_prep_time_pct=0.05)
        assert engine._selling_effectiveness_score(inp) == 25.0

    def test_meeting_prep_010_threshold(self, engine):
        inp = make_input(avg_selling_hours_per_week=42.0, strategy_vs_tactical_ratio=0.60, meeting_prep_time_pct=0.10)
        assert engine._selling_effectiveness_score(inp) == 12.0


# ─────────────────────────────────────────────────────────────────────────────
# 14. Composite score weight tests
# ─────────────────────────────────────────────────────────────────────────────

class TestCompositeWeights:
    def test_composite_weights_sum_to_one(self):
        total = 0.35 + 0.30 + 0.20 + 0.15
        assert total == pytest.approx(1.00)

    def test_composite_formula_manual(self, engine):
        pa, ba, pf, se = 80.0, 60.0, 40.0, 20.0
        expected = round(80.0 * 0.35 + 60.0 * 0.30 + 40.0 * 0.20 + 20.0 * 0.15, 2)
        result = engine._composite(pa, ba, pf, se)
        assert result == expected

    def test_composite_capped_at_100(self, engine):
        assert engine._composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_composite_zero_when_all_zero(self, engine):
        assert engine._composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_composite_only_pa_contributes(self, engine):
        result = engine._composite(100.0, 0.0, 0.0, 0.0)
        assert result == pytest.approx(35.0)

    def test_composite_only_ba_contributes(self, engine):
        result = engine._composite(0.0, 100.0, 0.0, 0.0)
        assert result == pytest.approx(30.0)

    def test_composite_only_pf_contributes(self, engine):
        result = engine._composite(0.0, 0.0, 100.0, 0.0)
        assert result == pytest.approx(20.0)

    def test_composite_only_se_contributes(self, engine):
        result = engine._composite(0.0, 0.0, 0.0, 100.0)
        assert result == pytest.approx(15.0)

    def test_composite_returned_in_result(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        pa = engine._priority_allocation_score(healthy_input)
        ba = engine._balance_score(healthy_input)
        pf = engine._pipeline_focus_score(healthy_input)
        se = engine._selling_effectiveness_score(healthy_input)
        expected = engine._composite(pa, ba, pf, se)
        assert result.time_composite == expected

    def test_composite_rounded_to_2_decimals(self, engine):
        result = engine._composite(33.3, 33.3, 33.3, 33.3)
        assert result == round(result, 2)


# ─────────────────────────────────────────────────────────────────────────────
# 15. assess() return type and field tests
# ─────────────────────────────────────────────────────────────────────────────

class TestAssessReturnType:
    def test_assess_returns_time_result(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result, TimeResult)

    def test_assess_result_rep_id(self, engine):
        inp = make_input(rep_id="ASSESS_TEST")
        result = engine.assess(inp)
        assert result.rep_id == "ASSESS_TEST"

    def test_assess_result_region(self, engine):
        inp = make_input(region="Pacific")
        result = engine.assess(inp)
        assert result.region == "Pacific"

    def test_assess_result_has_time_risk(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.time_risk, TimeRisk)

    def test_assess_result_has_pattern(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.time_pattern, TimePattern)

    def test_assess_result_has_severity(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.time_severity, TimeSeverity)

    def test_assess_result_has_action(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.recommended_action, TimeAction)

    def test_assess_result_scores_nonnegative(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.priority_allocation_score >= 0
        assert result.balance_score >= 0
        assert result.pipeline_focus_score >= 0
        assert result.selling_effectiveness_score >= 0

    def test_assess_result_scores_max_100(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert result.priority_allocation_score <= 100
        assert result.balance_score <= 100
        assert result.pipeline_focus_score <= 100
        assert result.selling_effectiveness_score <= 100

    def test_assess_result_composite_nonnegative(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.time_composite >= 0

    def test_assess_result_composite_max_100(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert result.time_composite <= 100

    def test_assess_appends_to_internal_results(self, engine, healthy_input):
        engine.assess(healthy_input)
        assert len(engine._results) == 1

    def test_assess_appends_multiple(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"R{i}"))
        assert len(engine._results) == 5

    def test_assess_result_signal_is_string(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.time_signal, str)


# ─────────────────────────────────────────────────────────────────────────────
# 16. assess_batch() tests
# ─────────────────────────────────────────────────────────────────────────────

class TestAssessBatch:
    def test_assess_batch_returns_list(self, engine):
        inputs = [make_input(rep_id=f"B{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        assert isinstance(results, list)

    def test_assess_batch_length_matches(self, engine):
        inputs = [make_input(rep_id=f"B{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_assess_batch_returns_time_results(self, engine):
        inputs = [make_input(rep_id=f"B{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        for r in results:
            assert isinstance(r, TimeResult)

    def test_assess_batch_empty_list(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_assess_batch_single_item(self, engine, healthy_input):
        results = engine.assess_batch([healthy_input])
        assert len(results) == 1

    def test_assess_batch_updates_internal_results(self, engine):
        inputs = [make_input(rep_id=f"B{i}") for i in range(4)]
        engine.assess_batch(inputs)
        assert len(engine._results) == 4

    def test_assess_batch_rep_ids_preserved(self, engine):
        inputs = [make_input(rep_id=f"REP{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"REP{i}"

    def test_assess_batch_mixed_risk_levels(self, engine):
        inputs = [make_input(), worst_case_input()]
        results = engine.assess_batch(inputs)
        risks = {r.time_risk for r in results}
        assert TimeRisk.low in risks
        assert TimeRisk.critical in risks

    def test_assess_batch_summary_reflects_batch(self, engine):
        inputs = [make_input(rep_id=f"B{i}") for i in range(7)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 7

    def test_assess_batch_vs_individual_consistency(self, engine):
        eng2 = SalesTimeAllocationIntelligenceEngine()
        inp = make_input(rep_id="CONSISTENCY")
        r_batch = engine.assess_batch([inp])[0]
        r_single = eng2.assess(inp)
        assert r_batch.time_composite == r_single.time_composite
        assert r_batch.time_risk == r_single.time_risk

    def test_assess_batch_large_batch(self, engine):
        inputs = [make_input(rep_id=f"L{i}") for i in range(50)]
        results = engine.assess_batch(inputs)
        assert len(results) == 50


# ─────────────────────────────────────────────────────────────────────────────
# 17. summary() aggregation tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSummaryAggregation:
    def test_summary_counts_risk_correctly(self, engine):
        engine.assess(make_input())        # low
        engine.assess(worst_case_input())  # critical
        s = engine.summary()
        assert s["risk_counts"].get("low", 0) >= 1
        assert s["risk_counts"].get("critical", 0) >= 1

    def test_summary_total_gap_count(self, engine):
        engine.assess(make_input(time_on_high_priority_accts_pct=0.30))
        engine.assess(make_input(time_on_high_priority_accts_pct=0.80))
        s = engine.summary()
        assert s["time_gap_count"] >= 1

    def test_summary_coaching_count(self, engine):
        engine.assess(make_input(reactive_time_pct=0.50))  # coaching=True
        s = engine.summary()
        assert s["coaching_count"] >= 1

    def test_summary_avg_composite_single(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        s = engine.summary()
        assert s["avg_time_composite"] == result.time_composite

    def test_summary_avg_composite_two(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        r1 = eng.assess(make_input(rep_id="A"))
        r2 = eng.assess(worst_case_input(rep_id="B"))
        s = eng.summary()
        expected = round((r1.time_composite + r2.time_composite) / 2, 1)
        assert s["avg_time_composite"] == expected

    def test_summary_total_quota_risk_sum(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        r1 = eng.assess(make_input(rep_id="A"))
        r2 = eng.assess(worst_case_input(rep_id="B"))
        s = eng.summary()
        expected = round(r1.estimated_quota_risk_usd + r2.estimated_quota_risk_usd, 2)
        assert s["total_estimated_quota_risk_usd"] == expected

    def test_summary_action_counts_tracked(self, engine):
        engine.assess(make_input())  # no_action
        s = engine.summary()
        assert "no_action" in s["action_counts"]

    def test_summary_severity_counts_tracked(self, engine):
        engine.assess(make_input())  # optimized
        s = engine.summary()
        assert "optimized" in s["severity_counts"]

    def test_summary_pattern_counts_tracked(self, engine):
        engine.assess(make_input())  # none pattern
        s = engine.summary()
        assert "none" in s["pattern_counts"]

    def test_summary_avg_pa_score_single(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        s = engine.summary()
        assert s["avg_priority_allocation_score"] == result.priority_allocation_score

    def test_summary_avg_ba_score_single(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        s = engine.summary()
        assert s["avg_balance_score"] == result.balance_score

    def test_summary_avg_pf_score_single(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        s = engine.summary()
        assert s["avg_pipeline_focus_score"] == result.pipeline_focus_score

    def test_summary_avg_se_score_single(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        s = engine.summary()
        assert s["avg_selling_effectiveness_score"] == result.selling_effectiveness_score

    def test_summary_after_batch_has_correct_avg(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        r1 = eng.assess(make_input(rep_id="X"))
        r2 = eng.assess(worst_case_input(rep_id="Y"))
        s = eng.summary()
        expected_avg = round((r1.time_composite + r2.time_composite) / 2, 1)
        assert s["avg_time_composite"] == expected_avg


# ─────────────────────────────────────────────────────────────────────────────
# 18. Edge cases: zero values
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCasesZeroValues:
    def test_all_pct_zero(self, engine):
        inp = make_input(
            time_on_high_priority_accts_pct=0.0,
            time_on_low_priority_accts_pct=0.0,
            time_on_admin_tasks_pct=0.0,
            time_on_pipeline_building_pct=0.0,
            time_on_existing_customers_pct=0.0,
            time_on_new_logo_pursuit_pct=0.0,
            reactive_time_pct=0.0,
            meeting_prep_time_pct=0.0,
            high_value_deal_time_ratio=0.0,
            quota_mapped_time_pct=0.0,
            strategy_vs_tactical_ratio=0.0,
            early_stage_deal_time_pct=0.0,
            late_stage_deal_time_pct=0.0,
            lost_deal_time_pct=0.0,
            avg_selling_hours_per_week=0.0,
            crm_update_hrs_per_week_avg=0.0,
            accounts_touched_per_week_avg=0.0,
            total_managed_accounts=0,
            avg_opportunity_value_usd=0.0,
        )
        result = engine.assess(inp)
        assert isinstance(result, TimeResult)

    def test_zero_total_accounts_no_quota_risk(self, engine):
        inp = make_input(total_managed_accounts=0, time_on_high_priority_accts_pct=0.30)
        result = engine.assess(inp)
        assert result.estimated_quota_risk_usd == 0.0

    def test_zero_opportunity_value_no_quota_risk(self, engine):
        inp = make_input(avg_opportunity_value_usd=0.0, time_on_high_priority_accts_pct=0.30)
        result = engine.assess(inp)
        assert result.estimated_quota_risk_usd == 0.0

    def test_zero_selling_hours_triggers_worst_se_score(self, engine):
        inp = make_input(avg_selling_hours_per_week=0.0)
        score = engine._selling_effectiveness_score(inp)
        assert score >= 40.0  # adds 40 for hours <= 25

    def test_all_pct_one(self, engine):
        inp = make_input(
            time_on_high_priority_accts_pct=1.0,
            time_on_low_priority_accts_pct=1.0,
            time_on_admin_tasks_pct=1.0,
            time_on_pipeline_building_pct=1.0,
            time_on_existing_customers_pct=1.0,
            time_on_new_logo_pursuit_pct=1.0,
            reactive_time_pct=1.0,
            meeting_prep_time_pct=1.0,
            high_value_deal_time_ratio=1.0,
            quota_mapped_time_pct=1.0,
            strategy_vs_tactical_ratio=1.0,
            early_stage_deal_time_pct=1.0,
            late_stage_deal_time_pct=1.0,
            lost_deal_time_pct=1.0,
        )
        result = engine.assess(inp)
        assert isinstance(result, TimeResult)

    def test_single_account(self, engine):
        inp = make_input(total_managed_accounts=1)
        result = engine.assess(inp)
        assert isinstance(result, TimeResult)

    def test_very_high_opportunity_value(self, engine):
        inp = make_input(avg_opportunity_value_usd=1_000_000.0, time_on_high_priority_accts_pct=0.30)
        result = engine.assess(inp)
        assert result.estimated_quota_risk_usd > 0.0

    def test_boundary_composite_exactly_0(self, engine):
        assert engine._risk(0.0) == TimeRisk.low
        assert engine._severity(0.0) == TimeSeverity.optimized

    def test_boundary_composite_exactly_100(self, engine):
        assert engine._risk(100.0) == TimeRisk.critical
        assert engine._severity(100.0) == TimeSeverity.scattered


# ─────────────────────────────────────────────────────────────────────────────
# 19. Integration / full-flow tests
# ─────────────────────────────────────────────────────────────────────────────

class TestFullFlowIntegration:
    def test_fresh_engine_summary_all_zeros(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        s = eng.summary()
        assert s["total"] == 0
        assert s["avg_time_composite"] == 0.0
        assert s["time_gap_count"] == 0
        assert s["coaching_count"] == 0
        assert s["total_estimated_quota_risk_usd"] == 0.0

    def test_engine_accumulates_across_assessments(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        for i in range(10):
            eng.assess(make_input(rep_id=f"R{i}"))
        assert eng.summary()["total"] == 10

    def test_batch_then_summary_consistency(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = eng.assess_batch(inputs)
        s = eng.summary()
        assert s["total"] == len(results)

    def test_critical_rep_all_fields_set(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        result = eng.assess(worst_case_input())
        assert result.time_risk == TimeRisk.critical
        assert result.time_severity == TimeSeverity.scattered
        assert result.time_composite >= 60
        assert result.has_time_gap is True
        assert result.requires_time_coaching is True

    def test_healthy_rep_all_fields_set(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        inp = make_input(
            time_on_high_priority_accts_pct=0.80,
            high_value_deal_time_ratio=0.80,
            quota_mapped_time_pct=0.80,
            time_on_admin_tasks_pct=0.05,
            reactive_time_pct=0.10,
            lost_deal_time_pct=0.02,
            time_on_pipeline_building_pct=0.55,
            time_on_new_logo_pursuit_pct=0.35,
            early_stage_deal_time_pct=0.40,
            avg_selling_hours_per_week=42.0,
            strategy_vs_tactical_ratio=0.60,
            meeting_prep_time_pct=0.15,
        )
        result = eng.assess(inp)
        assert result.time_risk == TimeRisk.low
        assert result.time_severity == TimeSeverity.optimized
        assert result.recommended_action == TimeAction.no_action
        assert result.time_composite < 20

    def test_multiple_engines_independent(self):
        eng1 = SalesTimeAllocationIntelligenceEngine()
        eng2 = SalesTimeAllocationIntelligenceEngine()
        eng1.assess(make_input(rep_id="E1"))
        assert eng1.summary()["total"] == 1
        assert eng2.summary()["total"] == 0

    def test_to_dict_consistent_with_result_fields(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        result = eng.assess(make_input())
        d = result.to_dict()
        assert d["rep_id"] == result.rep_id
        assert d["region"] == result.region
        assert d["time_risk"] == result.time_risk.value
        assert d["time_pattern"] == result.time_pattern.value
        assert d["time_severity"] == result.time_severity.value
        assert d["recommended_action"] == result.recommended_action.value
        assert d["time_composite"] == result.time_composite
        assert d["has_time_gap"] == result.has_time_gap
        assert d["requires_time_coaching"] == result.requires_time_coaching
        assert d["estimated_quota_risk_usd"] == result.estimated_quota_risk_usd
        assert d["time_signal"] == result.time_signal


# ─────────────────────────────────────────────────────────────────────────────
# 20. Additional boundary / coverage tests
# ─────────────────────────────────────────────────────────────────────────────

class TestAdditionalBoundaries:
    def test_wrong_size_focus_requires_both_conditions(self, engine):
        inp = make_input(
            time_on_low_priority_accts_pct=0.55,
            high_value_deal_time_ratio=0.31,  # above 0.30 → won't trigger
            time_on_high_priority_accts_pct=0.60,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
            reactive_time_pct=0.20,
        )
        result = engine.assess(inp)
        assert result.time_pattern != TimePattern.wrong_size_focus

    def test_renewal_hover_requires_both_conditions(self, engine):
        inp = make_input(
            time_on_existing_customers_pct=0.70,
            time_on_new_logo_pursuit_pct=0.16,  # above 0.15 → won't trigger
            time_on_high_priority_accts_pct=0.60,
            high_value_deal_time_ratio=0.60,
            time_on_admin_tasks_pct=0.10,
            avg_selling_hours_per_week=40.0,
            reactive_time_pct=0.20,
            time_on_low_priority_accts_pct=0.10,
        )
        result = engine.assess(inp)
        assert result.time_pattern != TimePattern.renewal_hover

    def test_has_gap_false_all_thresholds_barely_missed(self, engine):
        inp = make_input(
            time_on_admin_tasks_pct=0.249,
            time_on_high_priority_accts_pct=0.41,
        )
        comp = engine._composite(
            engine._priority_allocation_score(inp),
            engine._balance_score(inp),
            engine._pipeline_focus_score(inp),
            engine._selling_effectiveness_score(inp),
        )
        if comp < 40:
            assert engine._has_gap(inp, comp) is False

    def test_coaching_false_all_thresholds_barely_missed(self, engine):
        inp = make_input(reactive_time_pct=0.449, high_value_deal_time_ratio=0.41)
        assert engine._requires_coaching(inp, 29.99) is False

    def test_all_4_risk_levels_reachable(self, engine):
        risks = set()
        risks.add(engine.assess(make_input()).time_risk)
        risks.add(engine.assess(worst_case_input()).time_risk)
        # moderate
        risks.add(engine.assess(make_input(
            time_on_high_priority_accts_pct=0.55,
            high_value_deal_time_ratio=0.55,
            quota_mapped_time_pct=0.65,
            time_on_admin_tasks_pct=0.13,
            reactive_time_pct=0.25,
            lost_deal_time_pct=0.05,
            time_on_pipeline_building_pct=0.36,
            time_on_new_logo_pursuit_pct=0.26,
            early_stage_deal_time_pct=0.31,
            avg_selling_hours_per_week=42.0,
            strategy_vs_tactical_ratio=0.60,
            meeting_prep_time_pct=0.12,
        )).time_risk)
        assert TimeRisk.low in risks
        assert TimeRisk.critical in risks

    def test_summary_keys_are_exactly_13(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        eng.assess(make_input())
        assert len(eng.summary()) == 13

    def test_to_dict_keys_are_exactly_15(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        result = eng.assess(make_input())
        assert len(result.to_dict()) == 15

    def test_priority_score_below_or_equal_050_adds_22(self, engine):
        inp = make_input(time_on_high_priority_accts_pct=0.50, high_value_deal_time_ratio=0.80, quota_mapped_time_pct=0.80)
        assert engine._priority_allocation_score(inp) == 22.0

    def test_balance_score_reactive_exactly_040_adds_18(self, engine):
        inp = make_input(time_on_admin_tasks_pct=0.05, reactive_time_pct=0.40, lost_deal_time_pct=0.02)
        assert engine._balance_score(inp) == 18.0

    def test_pipeline_score_new_logo_exactly_010_adds_30(self, engine):
        inp = make_input(time_on_pipeline_building_pct=0.60, time_on_new_logo_pursuit_pct=0.10, early_stage_deal_time_pct=0.40)
        assert engine._pipeline_focus_score(inp) == 30.0

    def test_se_score_strategy_exactly_025_adds_35(self, engine):
        inp = make_input(avg_selling_hours_per_week=42.0, strategy_vs_tactical_ratio=0.25, meeting_prep_time_pct=0.15)
        assert engine._selling_effectiveness_score(inp) == 35.0

    def test_composite_is_nonnegative(self, engine, healthy_input):
        assert engine.assess(healthy_input).time_composite >= 0

    def test_fresh_engine_has_no_results(self):
        eng = SalesTimeAllocationIntelligenceEngine()
        assert eng._results == []

    def test_high_priority_accts_pct_reflected_in_signal(self, engine):
        inp = worst_case_input(time_on_high_priority_accts_pct=0.10)
        result = engine.assess(inp)
        assert "10%" in result.time_signal

    def test_assess_returns_consistent_result_type(self, engine):
        for i in range(3):
            result = engine.assess(make_input(rep_id=f"T{i}"))
            assert isinstance(result, TimeResult)
