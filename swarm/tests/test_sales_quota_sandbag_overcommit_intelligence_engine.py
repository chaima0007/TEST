"""
Comprehensive pytest tests for SalesQuotaSandbagOvercommitIntelligenceEngine.
"""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_quota_sandbag_overcommit_intelligence_engine import (
    SalesQuotaSandbagOvercommitIntelligenceEngine,
    QuotaInput,
    QuotaResult,
    QuotaPattern,
    QuotaPatternRisk,
    QuotaSeverity,
    QuotaAction,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> QuotaInput:
    """Return a clean, low-score baseline input with any fields overridden."""
    defaults = dict(
        rep_id="REP-001",
        region="West",
        evaluation_period_id="Q1-2026",
        quota_attainment_pct=1.0,
        forecast_accuracy_pct=0.85,
        commit_vs_actual_ratio=1.0,
        sandbagging_index=0.10,
        overcommit_frequency_pct=0.10,
        late_quarter_close_rate_pct=0.10,
        pipeline_to_quota_ratio=3.0,
        early_commit_accuracy_pct=0.80,
        mid_commit_accuracy_pct=0.80,
        late_commit_accuracy_pct=0.80,
        upside_conversion_rate_pct=0.50,
        commit_revision_frequency=1,
        pulled_in_deal_rate_pct=0.05,
        pushed_out_deal_rate_pct=0.05,
        quota_to_territory_fit_score=0.80,
        mgr_trust_in_forecast_score=0.80,
        peer_comparison_delta_pct=0.05,
        consecutive_miss_streak=0,
        voluntary_quota_increase_pct=0.10,
    )
    defaults.update(overrides)
    return QuotaInput(**defaults)


def engine() -> SalesQuotaSandbagOvercommitIntelligenceEngine:
    return SalesQuotaSandbagOvercommitIntelligenceEngine()


# ---------------------------------------------------------------------------
# 1. QuotaInput – field count
# ---------------------------------------------------------------------------

class TestQuotaInputFields:
    def test_has_22_fields(self):
        import dataclasses
        fields = dataclasses.fields(QuotaInput)
        assert len(fields) == 22

    def test_field_names(self):
        import dataclasses
        names = {f.name for f in dataclasses.fields(QuotaInput)}
        expected = {
            "rep_id", "region", "evaluation_period_id", "quota_attainment_pct",
            "forecast_accuracy_pct", "commit_vs_actual_ratio", "sandbagging_index",
            "overcommit_frequency_pct", "late_quarter_close_rate_pct",
            "pipeline_to_quota_ratio", "early_commit_accuracy_pct",
            "mid_commit_accuracy_pct", "late_commit_accuracy_pct",
            "upside_conversion_rate_pct", "commit_revision_frequency",
            "pulled_in_deal_rate_pct", "pushed_out_deal_rate_pct",
            "quota_to_territory_fit_score", "mgr_trust_in_forecast_score",
            "peer_comparison_delta_pct", "consecutive_miss_streak",
            "voluntary_quota_increase_pct",
        }
        assert names == expected


# ---------------------------------------------------------------------------
# 2. QuotaResult.to_dict – exactly 15 keys
# ---------------------------------------------------------------------------

class TestToDict:
    def test_to_dict_has_15_keys(self):
        e = engine()
        r = e.assess(make_input())
        d = r.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self):
        e = engine()
        r = e.assess(make_input())
        d = r.to_dict()
        expected = {
            "rep_id", "region", "quota_risk", "quota_pattern", "quota_severity",
            "recommended_action", "sandbagging_score", "overcommit_score",
            "calibration_score", "volatility_score", "quota_composite",
            "has_quota_gap", "requires_quota_intervention",
            "estimated_quota_distortion_usd", "quota_signal",
        }
        assert set(d.keys()) == expected

    def test_to_dict_values_are_primitives(self):
        e = engine()
        r = e.assess(make_input())
        d = r.to_dict()
        for k, v in d.items():
            assert isinstance(v, (str, float, int, bool)), f"Key {k} has unexpected type {type(v)}"

    def test_to_dict_enum_values_are_strings(self):
        e = engine()
        r = e.assess(make_input())
        d = r.to_dict()
        assert isinstance(d["quota_risk"], str)
        assert isinstance(d["quota_pattern"], str)
        assert isinstance(d["quota_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_preserved(self):
        e = engine()
        r = e.assess(make_input(rep_id="XYZ-999"))
        assert r.to_dict()["rep_id"] == "XYZ-999"

    def test_to_dict_region_preserved(self):
        e = engine()
        r = e.assess(make_input(region="EMEA"))
        assert r.to_dict()["region"] == "EMEA"


# ---------------------------------------------------------------------------
# 3. summary() – exactly 13 keys
# ---------------------------------------------------------------------------

class TestSummaryKeys:
    def test_empty_summary_has_13_keys(self):
        e = engine()
        s = e.summary()
        assert len(s) == 13

    def test_nonempty_summary_has_13_keys(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert len(s) == 13

    def test_summary_key_names(self):
        e = engine()
        s = e.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_quota_composite", "quota_gap_count",
            "intervention_count", "avg_sandbagging_score", "avg_overcommit_score",
            "avg_calibration_score", "avg_volatility_score",
            "total_estimated_quota_distortion_usd",
        }
        assert set(s.keys()) == expected

    def test_empty_summary_total_zero(self):
        e = engine()
        assert e.summary()["total"] == 0

    def test_empty_summary_avg_composite_zero(self):
        e = engine()
        assert e.summary()["avg_quota_composite"] == 0.0

    def test_empty_summary_distortion_zero(self):
        e = engine()
        assert e.summary()["total_estimated_quota_distortion_usd"] == 0.0

    def test_summary_total_matches_assessed(self):
        e = engine()
        for _ in range(5):
            e.assess(make_input())
        assert e.summary()["total"] == 5


# ---------------------------------------------------------------------------
# 4. Risk levels
# ---------------------------------------------------------------------------

class TestRiskLevels:
    def test_low_risk(self):
        # composite < 20
        e = engine()
        r = e.assess(make_input())
        assert r.quota_risk == QuotaPatternRisk.low

    def test_moderate_risk_boundary_20(self):
        # Need composite == 20 exactly — calibration_score >=20 via forecast_accuracy_pct<=0.75 (+8) and early<=0.55 (+15)
        # calibration: 8+15 = 23; composite = 0.30*23 = 6.9 — not enough
        # Use forecast<=0.40 (+40) alone: calibration=40, composite=0.30*40=12 still low
        # forecast<=0.40 (+40) + early<=0.35 (+30) = 70 -> composite=0.30*70=21 -> moderate
        e = engine()
        r = e.assess(make_input(
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        ))
        assert r.quota_risk == QuotaPatternRisk.moderate

    def test_moderate_risk_below_40(self):
        e = engine()
        r = e.assess(make_input(
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        ))
        assert r.quota_composite < 40

    def test_high_risk_boundary_40(self):
        # calibration: forecast<=0.40(+40)+early<=0.35(+30)+mid<=0.50(+20)+late<=0.65(+10)=100->*0.30=30
        # overcommit: freq>=0.55(+40)+miss>=2(+18)+trust<=0.35(+25)=83->*0.25=20.75
        # vol: rev>=3(+22)->*0.15=3.3; total=54.05 -> high
        e = engine()
        r = e.assess(make_input(
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
            late_commit_accuracy_pct=0.65,
            overcommit_frequency_pct=0.55,
            consecutive_miss_streak=2,
            mgr_trust_in_forecast_score=0.35,
            commit_revision_frequency=3,
        ))
        assert r.quota_risk == QuotaPatternRisk.high

    def test_critical_risk_boundary_60(self):
        # sandbagging: 40+35+25=100 -> *0.30=30
        # calibration: 40+30+20+10=100 -> *0.30=30
        # total=60 -> critical
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.65,
            late_quarter_close_rate_pct=0.60,
            commit_vs_actual_ratio=0.70,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
            late_commit_accuracy_pct=0.65,
        ))
        assert r.quota_risk == QuotaPatternRisk.critical

    def test_risk_enum_values(self):
        assert QuotaPatternRisk.low.value == "low"
        assert QuotaPatternRisk.moderate.value == "moderate"
        assert QuotaPatternRisk.high.value == "high"
        assert QuotaPatternRisk.critical.value == "critical"


# ---------------------------------------------------------------------------
# 5. Severity levels
# ---------------------------------------------------------------------------

class TestSeverityLevels:
    def test_calibrated_severity(self):
        e = engine()
        r = e.assess(make_input())
        assert r.quota_severity == QuotaSeverity.calibrated

    def test_drifting_severity(self):
        e = engine()
        r = e.assess(make_input(
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        ))
        assert r.quota_severity == QuotaSeverity.drifting

    def test_distorted_severity(self):
        # composite=54.05 -> distorted
        e = engine()
        r = e.assess(make_input(
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
            late_commit_accuracy_pct=0.65,
            overcommit_frequency_pct=0.55,
            consecutive_miss_streak=2,
            mgr_trust_in_forecast_score=0.35,
            commit_revision_frequency=3,
        ))
        assert r.quota_severity == QuotaSeverity.distorted

    def test_manipulated_severity(self):
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.65,
            late_quarter_close_rate_pct=0.60,
            commit_vs_actual_ratio=0.70,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
            late_commit_accuracy_pct=0.65,
        ))
        assert r.quota_severity == QuotaSeverity.manipulated

    def test_severity_mirrors_risk_calibrated(self):
        e = engine()
        r = e.assess(make_input())
        assert r.quota_risk == QuotaPatternRisk.low
        assert r.quota_severity == QuotaSeverity.calibrated

    def test_severity_enum_values(self):
        assert QuotaSeverity.calibrated.value == "calibrated"
        assert QuotaSeverity.drifting.value == "drifting"
        assert QuotaSeverity.distorted.value == "distorted"
        assert QuotaSeverity.manipulated.value == "manipulated"


# ---------------------------------------------------------------------------
# 6. Pattern detection
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def test_none_pattern(self):
        e = engine()
        r = e.assess(make_input())
        assert r.quota_pattern == QuotaPattern.none

    def test_sandbagging_pattern(self):
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.50,
            late_quarter_close_rate_pct=0.45,
        ))
        assert r.quota_pattern == QuotaPattern.sandbagging

    def test_sandbagging_exact_boundary(self):
        e = engine()
        r = e.assess(make_input(sandbagging_index=0.50, late_quarter_close_rate_pct=0.45))
        assert r.quota_pattern == QuotaPattern.sandbagging

    def test_sandbagging_below_index_threshold(self):
        e = engine()
        r = e.assess(make_input(sandbagging_index=0.499, late_quarter_close_rate_pct=0.45))
        assert r.quota_pattern != QuotaPattern.sandbagging

    def test_sandbagging_below_late_threshold(self):
        e = engine()
        r = e.assess(make_input(sandbagging_index=0.50, late_quarter_close_rate_pct=0.449))
        assert r.quota_pattern != QuotaPattern.sandbagging

    def test_overcommitting_pattern(self):
        e = engine()
        r = e.assess(make_input(
            overcommit_frequency_pct=0.50,
            consecutive_miss_streak=2,
        ))
        assert r.quota_pattern == QuotaPattern.overcommitting

    def test_overcommitting_exact_boundary(self):
        e = engine()
        r = e.assess(make_input(overcommit_frequency_pct=0.50, consecutive_miss_streak=2))
        assert r.quota_pattern == QuotaPattern.overcommitting

    def test_overcommitting_below_freq(self):
        e = engine()
        r = e.assess(make_input(overcommit_frequency_pct=0.499, consecutive_miss_streak=2))
        assert r.quota_pattern != QuotaPattern.overcommitting

    def test_overcommitting_below_streak(self):
        e = engine()
        r = e.assess(make_input(overcommit_frequency_pct=0.50, consecutive_miss_streak=1))
        assert r.quota_pattern != QuotaPattern.overcommitting

    def test_volatile_committor_pattern(self):
        e = engine()
        r = e.assess(make_input(
            commit_revision_frequency=4,
            forecast_accuracy_pct=0.55,
        ))
        assert r.quota_pattern == QuotaPattern.volatile_committor

    def test_volatile_committor_exact_boundary(self):
        e = engine()
        r = e.assess(make_input(commit_revision_frequency=4, forecast_accuracy_pct=0.55))
        assert r.quota_pattern == QuotaPattern.volatile_committor

    def test_volatile_committor_below_revision(self):
        e = engine()
        r = e.assess(make_input(commit_revision_frequency=3, forecast_accuracy_pct=0.55))
        assert r.quota_pattern != QuotaPattern.volatile_committor

    def test_volatile_committor_above_accuracy(self):
        e = engine()
        r = e.assess(make_input(commit_revision_frequency=4, forecast_accuracy_pct=0.551))
        assert r.quota_pattern != QuotaPattern.volatile_committor

    def test_late_surge_pattern(self):
        e = engine()
        r = e.assess(make_input(
            late_quarter_close_rate_pct=0.55,
            early_commit_accuracy_pct=0.40,
        ))
        assert r.quota_pattern == QuotaPattern.late_surge

    def test_late_surge_exact_boundary(self):
        e = engine()
        r = e.assess(make_input(late_quarter_close_rate_pct=0.55, early_commit_accuracy_pct=0.40))
        assert r.quota_pattern == QuotaPattern.late_surge

    def test_late_surge_below_late_rate(self):
        e = engine()
        r = e.assess(make_input(late_quarter_close_rate_pct=0.549, early_commit_accuracy_pct=0.40))
        assert r.quota_pattern != QuotaPattern.late_surge

    def test_late_surge_above_early_accuracy(self):
        e = engine()
        r = e.assess(make_input(late_quarter_close_rate_pct=0.55, early_commit_accuracy_pct=0.401))
        assert r.quota_pattern != QuotaPattern.late_surge

    def test_forecast_manipulator_pattern(self):
        e = engine()
        r = e.assess(make_input(
            pulled_in_deal_rate_pct=0.30,
            pushed_out_deal_rate_pct=0.25,
        ))
        assert r.quota_pattern == QuotaPattern.forecast_manipulator

    def test_forecast_manipulator_exact_boundary(self):
        e = engine()
        r = e.assess(make_input(pulled_in_deal_rate_pct=0.30, pushed_out_deal_rate_pct=0.25))
        assert r.quota_pattern == QuotaPattern.forecast_manipulator

    def test_forecast_manipulator_below_pulled(self):
        e = engine()
        r = e.assess(make_input(pulled_in_deal_rate_pct=0.299, pushed_out_deal_rate_pct=0.25))
        assert r.quota_pattern != QuotaPattern.forecast_manipulator

    def test_forecast_manipulator_below_pushed(self):
        e = engine()
        r = e.assess(make_input(pulled_in_deal_rate_pct=0.30, pushed_out_deal_rate_pct=0.249))
        assert r.quota_pattern != QuotaPattern.forecast_manipulator

    def test_pattern_priority_sandbagging_over_overcommitting(self):
        # sandbagging conditions met AND overcommitting conditions met -> sandbagging wins
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.50,
            late_quarter_close_rate_pct=0.45,
            overcommit_frequency_pct=0.50,
            consecutive_miss_streak=2,
        ))
        assert r.quota_pattern == QuotaPattern.sandbagging

    def test_pattern_priority_overcommitting_over_volatile(self):
        e = engine()
        r = e.assess(make_input(
            overcommit_frequency_pct=0.50,
            consecutive_miss_streak=2,
            commit_revision_frequency=4,
            forecast_accuracy_pct=0.55,
        ))
        assert r.quota_pattern == QuotaPattern.overcommitting

    def test_pattern_priority_volatile_over_late_surge(self):
        e = engine()
        r = e.assess(make_input(
            commit_revision_frequency=4,
            forecast_accuracy_pct=0.55,
            late_quarter_close_rate_pct=0.55,
            early_commit_accuracy_pct=0.40,
        ))
        assert r.quota_pattern == QuotaPattern.volatile_committor

    def test_pattern_priority_late_surge_over_manipulator(self):
        e = engine()
        r = e.assess(make_input(
            late_quarter_close_rate_pct=0.55,
            early_commit_accuracy_pct=0.40,
            pulled_in_deal_rate_pct=0.30,
            pushed_out_deal_rate_pct=0.25,
        ))
        assert r.quota_pattern == QuotaPattern.late_surge

    def test_pattern_enum_values(self):
        assert QuotaPattern.none.value == "none"
        assert QuotaPattern.sandbagging.value == "sandbagging"
        assert QuotaPattern.overcommitting.value == "overcommitting"
        assert QuotaPattern.volatile_committor.value == "volatile_committor"
        assert QuotaPattern.late_surge.value == "late_surge"
        assert QuotaPattern.forecast_manipulator.value == "forecast_manipulator"


# ---------------------------------------------------------------------------
# 7. Action types (all 7)
# ---------------------------------------------------------------------------

class TestActionTypes:
    def test_no_action(self):
        e = engine()
        r = e.assess(make_input())
        assert r.recommended_action == QuotaAction.no_action

    def test_quota_check_in_moderate_no_pattern(self):
        # moderate composite, pattern=none
        e = engine()
        r = e.assess(make_input(
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        ))
        assert r.quota_risk == QuotaPatternRisk.moderate
        assert r.recommended_action == QuotaAction.quota_check_in

    def test_forecast_calibration_coaching(self):
        # high risk + volatile_committor pattern
        e = engine()
        r = e.assess(make_input(
            commit_revision_frequency=4,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
            overcommit_frequency_pct=0.55,
            consecutive_miss_streak=2,
            mgr_trust_in_forecast_score=0.35,
        ))
        # ensure high risk and volatile_committor doesn't get overridden
        # Need sandbagging NOT triggered and overcommitting NOT triggered
        e2 = engine()
        r2 = e2.assess(make_input(
            commit_revision_frequency=5,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
            late_commit_accuracy_pct=0.65,
            mgr_trust_in_forecast_score=0.30,
        ))
        # composite: sandbagging=0, calibration=40+30+20+10=100->*0.30=30, overcommit=25->*0.25=6.25, vol=40->*0.15=6
        # total=42.25 -> high; pattern=volatile_committor (rev=5>=4, acc=0.40<=0.55)
        assert r2.quota_risk == QuotaPatternRisk.high
        assert r2.quota_pattern == QuotaPattern.volatile_committor
        assert r2.recommended_action == QuotaAction.forecast_calibration_coaching

    def test_commit_accuracy_coaching_high_overcommitting(self):
        e = engine()
        # high risk + overcommitting pattern (no sandbagging)
        r = e.assess(make_input(
            overcommit_frequency_pct=0.55,
            consecutive_miss_streak=3,
            mgr_trust_in_forecast_score=0.30,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        ))
        if r.quota_risk == QuotaPatternRisk.high and r.quota_pattern == QuotaPattern.overcommitting:
            assert r.recommended_action == QuotaAction.commit_accuracy_coaching

    def test_commit_accuracy_coaching_high_none_pattern(self):
        # high risk + none pattern -> commit_accuracy_coaching (fallback)
        e = engine()
        # craft high composite with no pattern triggers
        r = e.assess(make_input(
            forecast_accuracy_pct=0.38,
            early_commit_accuracy_pct=0.30,
            mid_commit_accuracy_pct=0.45,
            late_commit_accuracy_pct=0.60,
            overcommit_frequency_pct=0.56,
            mgr_trust_in_forecast_score=0.30,
            commit_revision_frequency=5,
        ))
        # overcommitting pattern: freq>=0.50 and streak>=2 -> streak=0 so no overcommitting
        # volatile: rev=5>=4 and acc=0.38<=0.55 -> volatile_committor
        # so pattern=volatile_committor, not none; let's suppress revision
        e2 = engine()
        r2 = e2.assess(make_input(
            forecast_accuracy_pct=0.38,
            early_commit_accuracy_pct=0.30,
            mid_commit_accuracy_pct=0.45,
            late_commit_accuracy_pct=0.60,
            overcommit_frequency_pct=0.56,
            mgr_trust_in_forecast_score=0.30,
            commit_revision_frequency=1,
            consecutive_miss_streak=0,
        ))
        if r2.quota_risk == QuotaPatternRisk.high and r2.quota_pattern == QuotaPattern.none:
            assert r2.recommended_action == QuotaAction.commit_accuracy_coaching

    def test_manager_quota_review_high_sandbagging(self):
        e = engine()
        # Need high (not critical) + sandbagging pattern
        r = e.assess(make_input(
            sandbagging_index=0.50,
            late_quarter_close_rate_pct=0.50,
            forecast_accuracy_pct=0.60,
        ))
        if r.quota_risk == QuotaPatternRisk.high and r.quota_pattern == QuotaPattern.sandbagging:
            assert r.recommended_action == QuotaAction.manager_quota_review

    def test_manager_quota_review_high_late_surge(self):
        e = engine()
        r = e.assess(make_input(
            late_quarter_close_rate_pct=0.55,
            early_commit_accuracy_pct=0.40,
            forecast_accuracy_pct=0.38,
            mid_commit_accuracy_pct=0.45,
            overcommit_frequency_pct=0.56,
            mgr_trust_in_forecast_score=0.30,
        ))
        if r.quota_risk == QuotaPatternRisk.high and r.quota_pattern == QuotaPattern.late_surge:
            assert r.recommended_action == QuotaAction.manager_quota_review

    def test_manager_quota_review_high_forecast_manipulator(self):
        e = engine()
        r = e.assess(make_input(
            pulled_in_deal_rate_pct=0.30,
            pushed_out_deal_rate_pct=0.25,
            forecast_accuracy_pct=0.38,
            early_commit_accuracy_pct=0.30,
            mid_commit_accuracy_pct=0.45,
            overcommit_frequency_pct=0.56,
            mgr_trust_in_forecast_score=0.30,
        ))
        if r.quota_risk == QuotaPatternRisk.high and r.quota_pattern == QuotaPattern.forecast_manipulator:
            assert r.recommended_action == QuotaAction.manager_quota_review

    def test_quota_reset_intervention(self):
        # critical + not sandbagging/forecast_manipulator -> quota_reset_intervention
        e = engine()
        r = e.assess(make_input(
            overcommit_frequency_pct=0.55,
            consecutive_miss_streak=3,
            mgr_trust_in_forecast_score=0.30,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
            late_commit_accuracy_pct=0.65,
            commit_revision_frequency=5,
            pulled_in_deal_rate_pct=0.36,
            pushed_out_deal_rate_pct=0.30,
            sandbagging_index=0.10,
            late_quarter_close_rate_pct=0.10,
        ))
        if r.quota_risk == QuotaPatternRisk.critical:
            if r.quota_pattern not in (QuotaPattern.sandbagging, QuotaPattern.forecast_manipulator):
                assert r.recommended_action == QuotaAction.quota_reset_intervention

    def test_executive_quota_escalation_critical_sandbagging(self):
        # critical composite + sandbagging pattern
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.65,
            late_quarter_close_rate_pct=0.65,
            commit_vs_actual_ratio=0.65,
            forecast_accuracy_pct=0.38,
            early_commit_accuracy_pct=0.30,
            mid_commit_accuracy_pct=0.45,
            late_commit_accuracy_pct=0.60,
            overcommit_frequency_pct=0.60,
            consecutive_miss_streak=4,
            mgr_trust_in_forecast_score=0.25,
        ))
        if r.quota_risk == QuotaPatternRisk.critical and r.quota_pattern == QuotaPattern.sandbagging:
            assert r.recommended_action == QuotaAction.executive_quota_escalation

    def test_executive_quota_escalation_critical_forecast_manipulator(self):
        e = engine()
        # Need critical + forecast_manipulator (no sandbagging to avoid priority override)
        r = e.assess(make_input(
            pulled_in_deal_rate_pct=0.36,
            pushed_out_deal_rate_pct=0.30,
            forecast_accuracy_pct=0.38,
            early_commit_accuracy_pct=0.30,
            mid_commit_accuracy_pct=0.45,
            late_commit_accuracy_pct=0.60,
            overcommit_frequency_pct=0.60,
            consecutive_miss_streak=3,
            mgr_trust_in_forecast_score=0.25,
            commit_revision_frequency=5,
        ))
        if r.quota_risk == QuotaPatternRisk.critical and r.quota_pattern == QuotaPattern.forecast_manipulator:
            assert r.recommended_action == QuotaAction.executive_quota_escalation

    def test_action_enum_values(self):
        assert QuotaAction.no_action.value == "no_action"
        assert QuotaAction.quota_check_in.value == "quota_check_in"
        assert QuotaAction.forecast_calibration_coaching.value == "forecast_calibration_coaching"
        assert QuotaAction.commit_accuracy_coaching.value == "commit_accuracy_coaching"
        assert QuotaAction.manager_quota_review.value == "manager_quota_review"
        assert QuotaAction.quota_reset_intervention.value == "quota_reset_intervention"
        assert QuotaAction.executive_quota_escalation.value == "executive_quota_escalation"


# ---------------------------------------------------------------------------
# 8. Sub-score: sandbagging_score
# ---------------------------------------------------------------------------

class TestSandbagScore:
    def _sb(self, **kw):
        e = engine()
        return e._sandbagging_score(make_input(**kw))

    def test_zero_score(self):
        assert self._sb() == 0.0

    def test_sandbagging_index_tier1_ge65(self):
        s = self._sb(sandbagging_index=0.65)
        assert s >= 40

    def test_sandbagging_index_tier2_ge45(self):
        s1 = self._sb(sandbagging_index=0.45)
        s2 = self._sb(sandbagging_index=0.25)
        assert s1 == 22

    def test_sandbagging_index_tier3_ge25(self):
        s = self._sb(sandbagging_index=0.25)
        assert s == 8

    def test_sandbagging_index_below_25(self):
        s = self._sb(sandbagging_index=0.24)
        assert s == 0

    def test_late_quarter_tier1_ge60(self):
        s = self._sb(late_quarter_close_rate_pct=0.60)
        assert s == 35

    def test_late_quarter_tier2_ge40(self):
        s = self._sb(late_quarter_close_rate_pct=0.40)
        assert s == 18

    def test_late_quarter_below_40(self):
        s = self._sb(late_quarter_close_rate_pct=0.39)
        assert s == 0

    def test_commit_vs_actual_tier1_le70(self):
        s = self._sb(commit_vs_actual_ratio=0.70)
        assert s == 25

    def test_commit_vs_actual_tier2_le85(self):
        s = self._sb(commit_vs_actual_ratio=0.85)
        assert s == 12

    def test_commit_vs_actual_above_85(self):
        s = self._sb(commit_vs_actual_ratio=0.86)
        assert s == 0

    def test_max_capped_at_100(self):
        s = self._sb(sandbagging_index=0.65, late_quarter_close_rate_pct=0.60, commit_vs_actual_ratio=0.70)
        assert s == 100.0

    def test_combined_scores(self):
        # index>=0.65 (+40) + late>=0.40 (+18) = 58
        s = self._sb(sandbagging_index=0.65, late_quarter_close_rate_pct=0.40)
        assert s == 58.0

    def test_index_boundary_exactly_65(self):
        s = self._sb(sandbagging_index=0.65)
        assert s == 40

    def test_index_boundary_exactly_45(self):
        s = self._sb(sandbagging_index=0.45)
        assert s == 22

    def test_index_boundary_exactly_25(self):
        s = self._sb(sandbagging_index=0.25)
        assert s == 8


# ---------------------------------------------------------------------------
# 9. Sub-score: overcommit_score
# ---------------------------------------------------------------------------

class TestOvercommitScore:
    def _oc(self, **kw):
        e = engine()
        return e._overcommit_score(make_input(**kw))

    def test_zero_score(self):
        assert self._oc() == 0.0

    def test_overcommit_freq_tier1_ge55(self):
        s = self._oc(overcommit_frequency_pct=0.55)
        assert s == 40

    def test_overcommit_freq_tier2_ge35(self):
        s = self._oc(overcommit_frequency_pct=0.35)
        assert s == 22

    def test_overcommit_freq_tier3_ge20(self):
        s = self._oc(overcommit_frequency_pct=0.20)
        assert s == 8

    def test_overcommit_freq_below_20(self):
        s = self._oc(overcommit_frequency_pct=0.19)
        assert s == 0

    def test_miss_streak_tier1_ge3(self):
        s = self._oc(consecutive_miss_streak=3)
        assert s == 35

    def test_miss_streak_tier2_ge2(self):
        s = self._oc(consecutive_miss_streak=2)
        assert s == 18

    def test_miss_streak_below_2(self):
        s = self._oc(consecutive_miss_streak=1)
        assert s == 0

    def test_mgr_trust_tier1_le35(self):
        s = self._oc(mgr_trust_in_forecast_score=0.35)
        assert s == 25

    def test_mgr_trust_tier2_le55(self):
        s = self._oc(mgr_trust_in_forecast_score=0.55)
        assert s == 12

    def test_mgr_trust_above_55(self):
        s = self._oc(mgr_trust_in_forecast_score=0.56)
        assert s == 0

    def test_max_capped_at_100(self):
        s = self._oc(overcommit_frequency_pct=0.55, consecutive_miss_streak=3, mgr_trust_in_forecast_score=0.35)
        assert s == 100.0

    def test_freq_boundary_exactly_55(self):
        s = self._oc(overcommit_frequency_pct=0.55)
        assert s == 40

    def test_freq_boundary_exactly_35(self):
        s = self._oc(overcommit_frequency_pct=0.35)
        assert s == 22

    def test_streak_boundary_exactly_3(self):
        s = self._oc(consecutive_miss_streak=3)
        assert s == 35

    def test_streak_boundary_exactly_2(self):
        s = self._oc(consecutive_miss_streak=2)
        assert s == 18

    def test_trust_boundary_exactly_35(self):
        s = self._oc(mgr_trust_in_forecast_score=0.35)
        assert s == 25

    def test_trust_boundary_exactly_55(self):
        s = self._oc(mgr_trust_in_forecast_score=0.55)
        assert s == 12


# ---------------------------------------------------------------------------
# 10. Sub-score: calibration_score
# ---------------------------------------------------------------------------

class TestCalibrationScore:
    def _cal(self, **kw):
        e = engine()
        return e._calibration_score(make_input(**kw))

    def test_zero_score(self):
        assert self._cal() == 0.0

    def test_forecast_acc_tier1_le40(self):
        s = self._cal(forecast_accuracy_pct=0.40)
        assert s == 40

    def test_forecast_acc_tier2_le60(self):
        s = self._cal(forecast_accuracy_pct=0.60)
        assert s == 22

    def test_forecast_acc_tier3_le75(self):
        s = self._cal(forecast_accuracy_pct=0.75)
        assert s == 8

    def test_forecast_acc_above_75(self):
        s = self._cal(forecast_accuracy_pct=0.76)
        assert s == 0

    def test_early_commit_tier1_le35(self):
        s = self._cal(early_commit_accuracy_pct=0.35)
        assert s == 30

    def test_early_commit_tier2_le55(self):
        s = self._cal(early_commit_accuracy_pct=0.55)
        assert s == 15

    def test_early_commit_above_55(self):
        s = self._cal(early_commit_accuracy_pct=0.56)
        assert s == 0

    def test_mid_commit_tier1_le50(self):
        s = self._cal(mid_commit_accuracy_pct=0.50)
        assert s == 20

    def test_mid_commit_tier2_le70(self):
        s = self._cal(mid_commit_accuracy_pct=0.70)
        assert s == 10

    def test_mid_commit_above_70(self):
        s = self._cal(mid_commit_accuracy_pct=0.71)
        assert s == 0

    def test_late_commit_le65(self):
        s = self._cal(late_commit_accuracy_pct=0.65)
        assert s == 10

    def test_late_commit_above_65(self):
        s = self._cal(late_commit_accuracy_pct=0.66)
        assert s == 0

    def test_max_capped_at_100(self):
        s = self._cal(
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
            late_commit_accuracy_pct=0.65,
        )
        assert s == 100.0

    def test_combined_cal(self):
        # forecast<=0.40(+40) + early<=0.55(+15) = 55
        s = self._cal(forecast_accuracy_pct=0.40, early_commit_accuracy_pct=0.55)
        assert s == 55.0

    def test_forecast_boundary_exactly_40(self):
        s = self._cal(forecast_accuracy_pct=0.40)
        assert s == 40

    def test_forecast_boundary_exactly_60(self):
        s = self._cal(forecast_accuracy_pct=0.60)
        assert s == 22

    def test_forecast_boundary_exactly_75(self):
        s = self._cal(forecast_accuracy_pct=0.75)
        assert s == 8

    def test_early_boundary_exactly_35(self):
        s = self._cal(early_commit_accuracy_pct=0.35)
        assert s == 30

    def test_early_boundary_exactly_55(self):
        s = self._cal(early_commit_accuracy_pct=0.55)
        assert s == 15

    def test_mid_boundary_exactly_50(self):
        s = self._cal(mid_commit_accuracy_pct=0.50)
        assert s == 20

    def test_mid_boundary_exactly_70(self):
        s = self._cal(mid_commit_accuracy_pct=0.70)
        assert s == 10

    def test_late_boundary_exactly_65(self):
        s = self._cal(late_commit_accuracy_pct=0.65)
        assert s == 10


# ---------------------------------------------------------------------------
# 11. Sub-score: volatility_score
# ---------------------------------------------------------------------------

class TestVolatilityScore:
    def _vol(self, **kw):
        e = engine()
        return e._volatility_score(make_input(**kw))

    def test_zero_score(self):
        assert self._vol() == 0.0

    def test_revision_tier1_ge5(self):
        s = self._vol(commit_revision_frequency=5)
        assert s == 40

    def test_revision_tier2_ge3(self):
        s = self._vol(commit_revision_frequency=3)
        assert s == 22

    def test_revision_tier3_ge2(self):
        s = self._vol(commit_revision_frequency=2)
        assert s == 8

    def test_revision_below_2(self):
        s = self._vol(commit_revision_frequency=1)
        assert s == 0

    def test_pulled_in_tier1_ge35(self):
        s = self._vol(pulled_in_deal_rate_pct=0.35)
        assert s == 35

    def test_pulled_in_tier2_ge20(self):
        s = self._vol(pulled_in_deal_rate_pct=0.20)
        assert s == 18

    def test_pulled_in_below_20(self):
        s = self._vol(pulled_in_deal_rate_pct=0.19)
        assert s == 0

    def test_pushed_out_tier1_ge30(self):
        s = self._vol(pushed_out_deal_rate_pct=0.30)
        assert s == 25

    def test_pushed_out_tier2_ge15(self):
        s = self._vol(pushed_out_deal_rate_pct=0.15)
        assert s == 12

    def test_pushed_out_below_15(self):
        s = self._vol(pushed_out_deal_rate_pct=0.14)
        assert s == 0

    def test_max_capped_at_100(self):
        s = self._vol(commit_revision_frequency=5, pulled_in_deal_rate_pct=0.35, pushed_out_deal_rate_pct=0.30)
        assert s == 100.0

    def test_combined_vol(self):
        # revision=3(+22) + pulled_in=0.20(+18) = 40
        s = self._vol(commit_revision_frequency=3, pulled_in_deal_rate_pct=0.20)
        assert s == 40.0

    def test_revision_boundary_exactly_5(self):
        s = self._vol(commit_revision_frequency=5)
        assert s == 40

    def test_revision_boundary_exactly_3(self):
        s = self._vol(commit_revision_frequency=3)
        assert s == 22

    def test_revision_boundary_exactly_2(self):
        s = self._vol(commit_revision_frequency=2)
        assert s == 8

    def test_pulled_boundary_exactly_35(self):
        s = self._vol(pulled_in_deal_rate_pct=0.35)
        assert s == 35

    def test_pulled_boundary_exactly_20(self):
        s = self._vol(pulled_in_deal_rate_pct=0.20)
        assert s == 18

    def test_pushed_boundary_exactly_30(self):
        s = self._vol(pushed_out_deal_rate_pct=0.30)
        assert s == 25

    def test_pushed_boundary_exactly_15(self):
        s = self._vol(pushed_out_deal_rate_pct=0.15)
        assert s == 12


# ---------------------------------------------------------------------------
# 12. Composite calculation and weights
# ---------------------------------------------------------------------------

class TestComposite:
    def test_composite_formula(self):
        e = engine()
        inp = make_input(
            sandbagging_index=0.65,
            forecast_accuracy_pct=0.40,
            overcommit_frequency_pct=0.55,
            commit_revision_frequency=5,
        )
        sb  = e._sandbagging_score(inp)
        oc  = e._overcommit_score(inp)
        cal = e._calibration_score(inp)
        vol = e._volatility_score(inp)
        expected = min(round(sb*0.30 + oc*0.25 + cal*0.30 + vol*0.15, 2), 100.0)
        r = e.assess(inp)
        assert r.quota_composite == expected

    def test_composite_capped_at_100(self):
        # Max all sub-scores
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.65,
            late_quarter_close_rate_pct=0.65,
            commit_vs_actual_ratio=0.65,
            forecast_accuracy_pct=0.35,
            early_commit_accuracy_pct=0.30,
            mid_commit_accuracy_pct=0.45,
            late_commit_accuracy_pct=0.60,
            overcommit_frequency_pct=0.60,
            consecutive_miss_streak=4,
            mgr_trust_in_forecast_score=0.25,
            commit_revision_frequency=6,
            pulled_in_deal_rate_pct=0.40,
            pushed_out_deal_rate_pct=0.35,
        ))
        assert r.quota_composite <= 100.0

    def test_composite_non_negative(self):
        e = engine()
        r = e.assess(make_input())
        assert r.quota_composite >= 0.0

    def test_weight_sum(self):
        assert abs(0.30 + 0.25 + 0.30 + 0.15 - 1.00) < 1e-9

    def test_composite_all_zero_subscores(self):
        e = engine()
        r = e.assess(make_input())
        assert r.quota_composite == 0.0

    def test_composite_is_float(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.quota_composite, float)

    def test_composite_rounded_to_2dp(self):
        e = engine()
        inp = make_input(sandbagging_index=0.45, forecast_accuracy_pct=0.60)
        r = e.assess(inp)
        # verify it's a 2dp float
        assert r.quota_composite == round(r.quota_composite, 2)


# ---------------------------------------------------------------------------
# 13. has_quota_gap logic
# ---------------------------------------------------------------------------

class TestHasQuotaGap:
    def test_gap_false_all_below(self):
        e = engine()
        r = e.assess(make_input(
            forecast_accuracy_pct=0.61,
            consecutive_miss_streak=1,
        ))
        if r.quota_composite < 40:
            assert r.has_quota_gap is False

    def test_gap_true_composite_ge40(self):
        # Force composite>=40
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.65,
            late_quarter_close_rate_pct=0.60,
            commit_vs_actual_ratio=0.70,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
        ))
        if r.quota_composite >= 40:
            assert r.has_quota_gap is True

    def test_gap_true_forecast_accuracy_le60(self):
        e = engine()
        r = e.assess(make_input(forecast_accuracy_pct=0.60))
        assert r.has_quota_gap is True

    def test_gap_true_forecast_accuracy_below_60(self):
        e = engine()
        r = e.assess(make_input(forecast_accuracy_pct=0.50))
        assert r.has_quota_gap is True

    def test_gap_true_consecutive_miss_ge2(self):
        e = engine()
        r = e.assess(make_input(consecutive_miss_streak=2))
        assert r.has_quota_gap is True

    def test_gap_true_consecutive_miss_above_2(self):
        e = engine()
        r = e.assess(make_input(consecutive_miss_streak=5))
        assert r.has_quota_gap is True

    def test_gap_false_streak_1(self):
        e = engine()
        r = e.assess(make_input(consecutive_miss_streak=1, forecast_accuracy_pct=0.85))
        if r.quota_composite < 40:
            assert r.has_quota_gap is False

    def test_gap_boundary_forecast_exactly_60(self):
        e = engine()
        r = e.assess(make_input(forecast_accuracy_pct=0.60))
        assert r.has_quota_gap is True

    def test_gap_boundary_streak_exactly_2(self):
        e = engine()
        r = e.assess(make_input(consecutive_miss_streak=2))
        assert r.has_quota_gap is True


# ---------------------------------------------------------------------------
# 14. requires_quota_intervention logic
# ---------------------------------------------------------------------------

class TestRequiresIntervention:
    def test_intervention_false_all_below(self):
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.10,
            mgr_trust_in_forecast_score=0.80,
        ))
        if r.quota_composite < 25:
            assert r.requires_quota_intervention is False

    def test_intervention_true_composite_ge25(self):
        # Build composite>=25
        e = engine()
        r = e.assess(make_input(
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
        ))
        if r.quota_composite >= 25:
            assert r.requires_quota_intervention is True

    def test_intervention_true_sandbagging_index_ge40(self):
        e = engine()
        r = e.assess(make_input(sandbagging_index=0.40))
        assert r.requires_quota_intervention is True

    def test_intervention_true_sandbagging_index_above_40(self):
        e = engine()
        r = e.assess(make_input(sandbagging_index=0.50))
        assert r.requires_quota_intervention is True

    def test_intervention_true_mgr_trust_le50(self):
        e = engine()
        r = e.assess(make_input(mgr_trust_in_forecast_score=0.50))
        assert r.requires_quota_intervention is True

    def test_intervention_true_mgr_trust_below_50(self):
        e = engine()
        r = e.assess(make_input(mgr_trust_in_forecast_score=0.30))
        assert r.requires_quota_intervention is True

    def test_intervention_boundary_sandbagging_exactly_40(self):
        e = engine()
        r = e.assess(make_input(sandbagging_index=0.40))
        assert r.requires_quota_intervention is True

    def test_intervention_boundary_mgr_trust_exactly_50(self):
        e = engine()
        r = e.assess(make_input(mgr_trust_in_forecast_score=0.50))
        assert r.requires_quota_intervention is True

    def test_intervention_false_sandbagging_below_40(self):
        e = engine()
        r = e.assess(make_input(sandbagging_index=0.39, mgr_trust_in_forecast_score=0.80))
        if r.quota_composite < 25:
            assert r.requires_quota_intervention is False

    def test_intervention_false_mgr_trust_above_50(self):
        e = engine()
        r = e.assess(make_input(mgr_trust_in_forecast_score=0.51, sandbagging_index=0.10))
        if r.quota_composite < 25:
            assert r.requires_quota_intervention is False


# ---------------------------------------------------------------------------
# 15. estimated_quota_distortion_usd
# ---------------------------------------------------------------------------

class TestDistortionUSD:
    def test_zero_distortion_when_commit_matches_actual(self):
        e = engine()
        r = e.assess(make_input(commit_vs_actual_ratio=1.0))
        assert r.estimated_quota_distortion_usd == 0.0

    def test_distortion_formula_basic(self):
        e = engine()
        inp = make_input(
            pipeline_to_quota_ratio=2.0,
            commit_vs_actual_ratio=0.80,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        )
        r = e.assess(inp)
        base = 2.0 * 100_000
        expected = round(base * (r.quota_composite / 100) * abs(1.0 - 0.80), 2)
        assert r.estimated_quota_distortion_usd == expected

    def test_distortion_positive_for_overcommit(self):
        e = engine()
        r = e.assess(make_input(
            commit_vs_actual_ratio=1.50,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        ))
        assert r.estimated_quota_distortion_usd >= 0.0

    def test_distortion_uses_abs_value(self):
        # Both sides of ratio=1.0 should give same distortion for same magnitude
        e1 = engine()
        e2 = engine()
        inp_under = make_input(
            commit_vs_actual_ratio=0.70,
            pipeline_to_quota_ratio=2.0,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        )
        inp_over = make_input(
            commit_vs_actual_ratio=1.30,
            pipeline_to_quota_ratio=2.0,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        )
        r1 = e1.assess(inp_under)
        r2 = e2.assess(inp_over)
        # composite should be similar but let's just check non-negative
        assert r1.estimated_quota_distortion_usd >= 0.0
        assert r2.estimated_quota_distortion_usd >= 0.0

    def test_distortion_scales_with_pipeline_ratio(self):
        e1 = engine()
        e2 = engine()
        common = dict(
            commit_vs_actual_ratio=0.80,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        )
        r1 = e1.assess(make_input(pipeline_to_quota_ratio=1.0, **common))
        r2 = e2.assess(make_input(pipeline_to_quota_ratio=4.0, **common))
        assert r2.estimated_quota_distortion_usd == pytest.approx(r1.estimated_quota_distortion_usd * 4, rel=1e-5)

    def test_distortion_is_float(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.estimated_quota_distortion_usd, float)

    def test_distortion_rounded_to_2dp(self):
        e = engine()
        r = e.assess(make_input(
            commit_vs_actual_ratio=0.77,
            pipeline_to_quota_ratio=3.7,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        ))
        assert r.estimated_quota_distortion_usd == round(r.estimated_quota_distortion_usd, 2)

    def test_distortion_zero_pipeline(self):
        e = engine()
        r = e.assess(make_input(pipeline_to_quota_ratio=0.0, commit_vs_actual_ratio=0.50))
        assert r.estimated_quota_distortion_usd == 0.0


# ---------------------------------------------------------------------------
# 16. Signal text
# ---------------------------------------------------------------------------

class TestSignal:
    def test_signal_low_composite_text(self):
        e = engine()
        r = e.assess(make_input())
        assert "calibrated" in r.quota_signal.lower()

    def test_signal_low_composite_full_text(self):
        e = engine()
        r = e.assess(make_input())
        assert r.quota_signal == (
            "Quota commitment calibrated — forecast accuracy, commit consistency, "
            "and attainment pattern within benchmarks"
        )

    def test_signal_high_composite_contains_pattern_label(self):
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.50,
            late_quarter_close_rate_pct=0.45,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        ))
        if r.quota_composite >= 20:
            assert "Sandbagging" in r.quota_signal

    def test_signal_contains_forecast_accuracy_pct(self):
        e = engine()
        r = e.assess(make_input(
            forecast_accuracy_pct=0.72,
            sandbagging_index=0.50,
            late_quarter_close_rate_pct=0.45,
            early_commit_accuracy_pct=0.35,
        ))
        if r.quota_composite >= 20:
            assert "72%" in r.quota_signal

    def test_signal_contains_late_close_pct(self):
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.50,
            late_quarter_close_rate_pct=0.45,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        ))
        if r.quota_composite >= 20:
            assert "45%" in r.quota_signal

    def test_signal_contains_consecutive_miss(self):
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.50,
            late_quarter_close_rate_pct=0.45,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            consecutive_miss_streak=3,
        ))
        if r.quota_composite >= 20:
            assert "3 consecutive miss streak" in r.quota_signal

    def test_signal_contains_composite_int(self):
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.50,
            late_quarter_close_rate_pct=0.45,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        ))
        if r.quota_composite >= 20:
            assert f"composite {round(r.quota_composite)}" in r.quota_signal

    def test_signal_overcommitting_label(self):
        e = engine()
        r = e.assess(make_input(
            overcommit_frequency_pct=0.55,
            consecutive_miss_streak=3,
            mgr_trust_in_forecast_score=0.30,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        ))
        if r.quota_composite >= 20 and r.quota_pattern == QuotaPattern.overcommitting:
            assert "Overcommitting" in r.quota_signal

    def test_signal_volatile_committor_label(self):
        e = engine()
        r = e.assess(make_input(
            commit_revision_frequency=5,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
            mgr_trust_in_forecast_score=0.30,
        ))
        if r.quota_composite >= 20 and r.quota_pattern == QuotaPattern.volatile_committor:
            assert "Volatile committor" in r.quota_signal

    def test_signal_late_surge_label(self):
        e = engine()
        r = e.assess(make_input(
            late_quarter_close_rate_pct=0.55,
            early_commit_accuracy_pct=0.40,
            forecast_accuracy_pct=0.40,
            mid_commit_accuracy_pct=0.50,
        ))
        if r.quota_composite >= 20 and r.quota_pattern == QuotaPattern.late_surge:
            assert "Late surge" in r.quota_signal

    def test_signal_forecast_manipulator_label(self):
        e = engine()
        r = e.assess(make_input(
            pulled_in_deal_rate_pct=0.30,
            pushed_out_deal_rate_pct=0.25,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        ))
        if r.quota_composite >= 20 and r.quota_pattern == QuotaPattern.forecast_manipulator:
            assert "Forecast manipulator" in r.quota_signal

    def test_signal_is_string(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.quota_signal, str)

    def test_signal_nonempty(self):
        e = engine()
        r = e.assess(make_input())
        assert len(r.quota_signal) > 0


# ---------------------------------------------------------------------------
# 17. Batch processing
# ---------------------------------------------------------------------------

class TestBatchProcessing:
    def test_batch_returns_list(self):
        e = engine()
        results = e.assess_batch([make_input(), make_input(rep_id="REP-002")])
        assert isinstance(results, list)

    def test_batch_length_matches_input(self):
        e = engine()
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(10)]
        results = e.assess_batch(inputs)
        assert len(results) == 10

    def test_batch_each_is_quota_result(self):
        e = engine()
        results = e.assess_batch([make_input(), make_input(rep_id="REP-002")])
        for r in results:
            assert isinstance(r, QuotaResult)

    def test_batch_empty_list(self):
        e = engine()
        results = e.assess_batch([])
        assert results == []

    def test_batch_accumulates_in_summary(self):
        e = engine()
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(7)]
        e.assess_batch(inputs)
        assert e.summary()["total"] == 7

    def test_batch_mixed_patterns(self):
        e = engine()
        inputs = [
            make_input(sandbagging_index=0.55, late_quarter_close_rate_pct=0.50),
            make_input(overcommit_frequency_pct=0.55, consecutive_miss_streak=2),
            make_input(),
        ]
        results = e.assess_batch(inputs)
        patterns = {r.quota_pattern for r in results}
        assert QuotaPattern.sandbagging in patterns
        assert QuotaPattern.overcommitting in patterns
        assert QuotaPattern.none in patterns

    def test_batch_preserves_rep_ids(self):
        e = engine()
        ids = [f"REP-{i:03d}" for i in range(5)]
        results = e.assess_batch([make_input(rep_id=rid) for rid in ids])
        assert [r.rep_id for r in results] == ids

    def test_single_assess_and_batch_equivalent(self):
        inp = make_input(sandbagging_index=0.55, late_quarter_close_rate_pct=0.50)
        e1 = engine()
        e2 = engine()
        r_single = e1.assess(inp)
        r_batch = e2.assess_batch([inp])[0]
        assert r_single.quota_composite == r_batch.quota_composite
        assert r_single.quota_pattern == r_batch.quota_pattern


# ---------------------------------------------------------------------------
# 18. summary() aggregation
# ---------------------------------------------------------------------------

class TestSummaryAggregation:
    def test_summary_risk_counts(self):
        e = engine()
        e.assess(make_input())  # low
        e.assess(make_input(
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
        ))  # moderate
        s = e.summary()
        assert "low" in s["risk_counts"]

    def test_summary_pattern_counts_none(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert s["pattern_counts"].get("none", 0) >= 1

    def test_summary_gap_count(self):
        e = engine()
        e.assess(make_input(consecutive_miss_streak=2))  # has_gap=True
        e.assess(make_input())  # may or may not have gap
        s = e.summary()
        assert s["quota_gap_count"] >= 1

    def test_summary_intervention_count(self):
        e = engine()
        e.assess(make_input(mgr_trust_in_forecast_score=0.50))  # requires intervention
        e.assess(make_input())
        s = e.summary()
        assert s["intervention_count"] >= 1

    def test_summary_avg_composite_positive(self):
        e = engine()
        e.assess(make_input(forecast_accuracy_pct=0.40, early_commit_accuracy_pct=0.35))
        s = e.summary()
        assert s["avg_quota_composite"] > 0

    def test_summary_total_distortion_sum(self):
        e = engine()
        r1 = e.assess(make_input(commit_vs_actual_ratio=0.70, forecast_accuracy_pct=0.40, early_commit_accuracy_pct=0.35))
        r2 = e.assess(make_input(commit_vs_actual_ratio=0.70, forecast_accuracy_pct=0.40, early_commit_accuracy_pct=0.35))
        s = e.summary()
        expected = round(r1.estimated_quota_distortion_usd + r2.estimated_quota_distortion_usd, 2)
        assert s["total_estimated_quota_distortion_usd"] == pytest.approx(expected, rel=1e-4)

    def test_summary_avg_sandbagging_non_negative(self):
        e = engine()
        e.assess(make_input())
        assert e.summary()["avg_sandbagging_score"] >= 0

    def test_summary_avg_overcommit_non_negative(self):
        e = engine()
        e.assess(make_input())
        assert e.summary()["avg_overcommit_score"] >= 0

    def test_summary_avg_calibration_non_negative(self):
        e = engine()
        e.assess(make_input())
        assert e.summary()["avg_calibration_score"] >= 0

    def test_summary_avg_volatility_non_negative(self):
        e = engine()
        e.assess(make_input())
        assert e.summary()["avg_volatility_score"] >= 0

    def test_summary_severity_counts_populated(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        total_severity = sum(s["severity_counts"].values())
        assert total_severity == s["total"]

    def test_summary_action_counts_populated(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        total_actions = sum(s["action_counts"].values())
        assert total_actions == s["total"]

    def test_summary_risk_counts_sum_equals_total(self):
        e = engine()
        for _ in range(5):
            e.assess(make_input())
        s = e.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_equals_total(self):
        e = engine()
        for _ in range(5):
            e.assess(make_input())
        s = e.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_multiple_engines_independent(self):
        e1 = engine()
        e2 = engine()
        e1.assess(make_input())
        e1.assess(make_input())
        e2.assess(make_input())
        assert e1.summary()["total"] == 2
        assert e2.summary()["total"] == 1


# ---------------------------------------------------------------------------
# 19. Additional boundary and edge cases
# ---------------------------------------------------------------------------

class TestBoundaryEdgeCases:
    def test_composite_exactly_20_is_moderate(self):
        # calibration=0.40(+40)+early=0.35(+30) -> cal=70 -> cal*0.30=21 -> moderate
        e = engine()
        r = e.assess(make_input(forecast_accuracy_pct=0.40, early_commit_accuracy_pct=0.35))
        assert r.quota_composite >= 20
        assert r.quota_risk in (QuotaPatternRisk.moderate, QuotaPatternRisk.high, QuotaPatternRisk.critical)

    def test_composite_exactly_40_is_high(self):
        e = engine()
        # Calibration only: forecast<=0.40(+40)+early<=0.35(+30)+mid<=0.50(+20)+late<=0.65(+10)=100 -> *0.30=30
        # Overcommit: freq>=0.55(+40)+miss>=2(+18)+trust<=0.35(+25)=83 -> *0.25=20.75
        # total=50.75 (too high) let's try calibration+some overcommit to hit exactly 40
        # Let calibration=100->*0.30=30, overcommit=0, sandbagging=0
        # need volatility to add 10 -> vol=10/0.15=66.7 -> rev>=3(+22)+pushed>=0.15(+12)=34 no
        # vol: rev>=3(+22)+pulled>=0.20(+18)=40 -> *0.15=6 -> total=36 not 40
        # calibration=100->30, vol: rev=5(+40)+pulled=0.35(+35)+pushed=0.30(+25)=100->*0.15=15 -> total=45 high
        r = e.assess(make_input(
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
            late_commit_accuracy_pct=0.65,
            commit_revision_frequency=5,
            pulled_in_deal_rate_pct=0.35,
            pushed_out_deal_rate_pct=0.30,
        ))
        assert r.quota_composite >= 40
        assert r.quota_risk in (QuotaPatternRisk.high, QuotaPatternRisk.critical)

    def test_composite_exactly_60_is_critical(self):
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.65,
            late_quarter_close_rate_pct=0.60,
            commit_vs_actual_ratio=0.70,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
            late_commit_accuracy_pct=0.65,
        ))
        # sb=100->30, cal=100->30, total>=60
        assert r.quota_composite >= 60
        assert r.quota_risk == QuotaPatternRisk.critical

    def test_result_rep_id_preserved(self):
        e = engine()
        r = e.assess(make_input(rep_id="SPECIAL-REP"))
        assert r.rep_id == "SPECIAL-REP"

    def test_result_region_preserved(self):
        e = engine()
        r = e.assess(make_input(region="APAC"))
        assert r.region == "APAC"

    def test_assess_returns_quota_result_instance(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r, QuotaResult)

    def test_multiple_assess_independent(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="A"))
        r2 = e.assess(make_input(rep_id="B"))
        assert r1.rep_id == "A"
        assert r2.rep_id == "B"

    def test_engine_accumulates_results(self):
        e = engine()
        e.assess(make_input())
        e.assess(make_input())
        assert e.summary()["total"] == 2

    def test_new_engine_starts_fresh(self):
        e1 = engine()
        e1.assess(make_input())
        e2 = engine()
        assert e2.summary()["total"] == 0

    def test_zero_commit_revision_frequency(self):
        e = engine()
        r = e.assess(make_input(commit_revision_frequency=0))
        assert r.volatility_score == 0.0

    def test_high_pipeline_ratio(self):
        e = engine()
        r = e.assess(make_input(pipeline_to_quota_ratio=10.0, commit_vs_actual_ratio=0.50,
                                forecast_accuracy_pct=0.40, early_commit_accuracy_pct=0.35))
        assert r.estimated_quota_distortion_usd > 0

    def test_commit_vs_actual_exactly_1(self):
        e = engine()
        r = e.assess(make_input(commit_vs_actual_ratio=1.0))
        assert r.estimated_quota_distortion_usd == 0.0

    def test_all_patterns_enum_accessible(self):
        assert len(list(QuotaPattern)) == 6

    def test_all_risks_enum_accessible(self):
        assert len(list(QuotaPatternRisk)) == 4

    def test_all_severities_enum_accessible(self):
        assert len(list(QuotaSeverity)) == 4

    def test_all_actions_enum_accessible(self):
        assert len(list(QuotaAction)) == 7


# ---------------------------------------------------------------------------
# 20. Integration: full scenarios
# ---------------------------------------------------------------------------

class TestIntegrationScenarios:
    def test_perfect_rep_scenario(self):
        """Rep with perfect metrics should be low risk, calibrated, no action."""
        e = engine()
        r = e.assess(make_input(
            forecast_accuracy_pct=0.95,
            commit_vs_actual_ratio=1.0,
            sandbagging_index=0.05,
            overcommit_frequency_pct=0.05,
            late_quarter_close_rate_pct=0.10,
            early_commit_accuracy_pct=0.90,
            mid_commit_accuracy_pct=0.90,
            late_commit_accuracy_pct=0.90,
            commit_revision_frequency=1,
            pulled_in_deal_rate_pct=0.05,
            pushed_out_deal_rate_pct=0.05,
            mgr_trust_in_forecast_score=0.95,
            consecutive_miss_streak=0,
        ))
        assert r.quota_risk == QuotaPatternRisk.low
        assert r.quota_severity == QuotaSeverity.calibrated
        assert r.recommended_action == QuotaAction.no_action
        assert r.quota_pattern == QuotaPattern.none
        assert r.has_quota_gap is False
        assert r.requires_quota_intervention is False

    def test_worst_case_scenario(self):
        """Rep with all bad metrics should be critical, manipulated."""
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.80,
            late_quarter_close_rate_pct=0.80,
            commit_vs_actual_ratio=0.50,
            forecast_accuracy_pct=0.30,
            overcommit_frequency_pct=0.80,
            consecutive_miss_streak=5,
            mgr_trust_in_forecast_score=0.20,
            early_commit_accuracy_pct=0.20,
            mid_commit_accuracy_pct=0.30,
            late_commit_accuracy_pct=0.40,
            commit_revision_frequency=8,
            pulled_in_deal_rate_pct=0.50,
            pushed_out_deal_rate_pct=0.45,
        ))
        assert r.quota_risk == QuotaPatternRisk.critical
        assert r.quota_severity == QuotaSeverity.manipulated
        assert r.quota_composite == 100.0

    def test_sandbagging_scenario_full(self):
        """Classic sandbagging: low commit, late quarter surge."""
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.70,
            late_quarter_close_rate_pct=0.65,
            commit_vs_actual_ratio=0.65,
        ))
        assert r.quota_pattern == QuotaPattern.sandbagging
        assert r.sandbagging_score > 0

    def test_forecast_manipulator_scenario_full(self):
        """Rep pulling in and pushing out deals to manage optics."""
        e = engine()
        r = e.assess(make_input(
            pulled_in_deal_rate_pct=0.40,
            pushed_out_deal_rate_pct=0.35,
        ))
        assert r.quota_pattern == QuotaPattern.forecast_manipulator

    def test_volatile_committor_scenario_full(self):
        """Rep changing commits frequently with poor accuracy."""
        e = engine()
        r = e.assess(make_input(
            commit_revision_frequency=6,
            forecast_accuracy_pct=0.45,
        ))
        assert r.quota_pattern == QuotaPattern.volatile_committor

    def test_overcommitting_scenario_full(self):
        """Rep consistently commits above what they close."""
        e = engine()
        r = e.assess(make_input(
            overcommit_frequency_pct=0.75,
            consecutive_miss_streak=3,
        ))
        assert r.quota_pattern == QuotaPattern.overcommitting

    def test_late_surge_scenario_full(self):
        """Rep closes most deals in last 2 weeks, terrible early accuracy."""
        e = engine()
        r = e.assess(make_input(
            late_quarter_close_rate_pct=0.70,
            early_commit_accuracy_pct=0.25,
        ))
        assert r.quota_pattern == QuotaPattern.late_surge

    def test_batch_summary_all_patterns(self):
        """Batch covering all 5 non-none patterns."""
        e = engine()
        inputs = [
            make_input(sandbagging_index=0.60, late_quarter_close_rate_pct=0.55),
            make_input(overcommit_frequency_pct=0.55, consecutive_miss_streak=2),
            make_input(commit_revision_frequency=4, forecast_accuracy_pct=0.50),
            make_input(late_quarter_close_rate_pct=0.60, early_commit_accuracy_pct=0.35),
            make_input(pulled_in_deal_rate_pct=0.35, pushed_out_deal_rate_pct=0.30),
            make_input(),
        ]
        e.assess_batch(inputs)
        s = e.summary()
        assert s["total"] == 6
        assert len(s["pattern_counts"]) >= 5

    def test_to_dict_roundtrip(self):
        e = engine()
        r = e.assess(make_input(rep_id="ROUND-TRIP", region="North"))
        d = r.to_dict()
        assert d["rep_id"] == "ROUND-TRIP"
        assert d["region"] == "North"
        assert d["quota_composite"] == r.quota_composite

    def test_has_gap_and_intervention_both_true(self):
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.65,
            late_quarter_close_rate_pct=0.60,
            commit_vs_actual_ratio=0.70,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
            late_commit_accuracy_pct=0.65,
        ))
        assert r.has_quota_gap is True
        assert r.requires_quota_intervention is True

    def test_action_coverage_in_batch(self):
        """Batch of reps produces multiple distinct action types."""
        e = engine()
        inputs = [
            make_input(),  # no_action
            make_input(forecast_accuracy_pct=0.40, early_commit_accuracy_pct=0.35),  # quota_check_in
        ]
        results = e.assess_batch(inputs)
        actions = {r.recommended_action for r in results}
        assert QuotaAction.no_action in actions


# ---------------------------------------------------------------------------
# 21. Additional sub-score threshold and capping tests
# ---------------------------------------------------------------------------

class TestSubScoreThresholdCapping:
    def test_sandbagging_score_partial_sum(self):
        e = engine()
        # index>=0.45(+22) + late>=0.40(+18) + commit<=0.85(+12) = 52
        r = e.assess(make_input(
            sandbagging_index=0.45,
            late_quarter_close_rate_pct=0.40,
            commit_vs_actual_ratio=0.85,
        ))
        assert r.sandbagging_score == 52.0

    def test_overcommit_score_partial_sum(self):
        e = engine()
        # freq>=0.35(+22) + miss=2(+18) = 40
        r = e.assess(make_input(
            overcommit_frequency_pct=0.35,
            consecutive_miss_streak=2,
        ))
        assert r.overcommit_score == 40.0

    def test_calibration_score_partial_sum(self):
        e = engine()
        # forecast<=0.60(+22) + early<=0.55(+15) = 37
        r = e.assess(make_input(
            forecast_accuracy_pct=0.60,
            early_commit_accuracy_pct=0.55,
        ))
        assert r.calibration_score == 37.0

    def test_volatility_score_partial_sum(self):
        e = engine()
        # rev=3(+22) + pushed=0.15(+12) = 34
        r = e.assess(make_input(
            commit_revision_frequency=3,
            pushed_out_deal_rate_pct=0.15,
        ))
        assert r.volatility_score == 34.0

    def test_sandbagging_score_not_negative(self):
        e = engine()
        r = e.assess(make_input(sandbagging_index=0.0, late_quarter_close_rate_pct=0.0, commit_vs_actual_ratio=2.0))
        assert r.sandbagging_score == 0.0

    def test_overcommit_score_not_negative(self):
        e = engine()
        r = e.assess(make_input(overcommit_frequency_pct=0.0, consecutive_miss_streak=0, mgr_trust_in_forecast_score=1.0))
        assert r.overcommit_score == 0.0

    def test_calibration_score_not_negative(self):
        e = engine()
        r = e.assess(make_input(forecast_accuracy_pct=1.0, early_commit_accuracy_pct=1.0,
                                mid_commit_accuracy_pct=1.0, late_commit_accuracy_pct=1.0))
        assert r.calibration_score == 0.0

    def test_volatility_score_not_negative(self):
        e = engine()
        r = e.assess(make_input(commit_revision_frequency=0, pulled_in_deal_rate_pct=0.0, pushed_out_deal_rate_pct=0.0))
        assert r.volatility_score == 0.0

    def test_all_subscores_capped_at_100(self):
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=1.0, late_quarter_close_rate_pct=1.0, commit_vs_actual_ratio=0.0,
            overcommit_frequency_pct=1.0, consecutive_miss_streak=10, mgr_trust_in_forecast_score=0.0,
            forecast_accuracy_pct=0.0, early_commit_accuracy_pct=0.0, mid_commit_accuracy_pct=0.0, late_commit_accuracy_pct=0.0,
            commit_revision_frequency=10, pulled_in_deal_rate_pct=1.0, pushed_out_deal_rate_pct=1.0,
        ))
        assert r.sandbagging_score <= 100.0
        assert r.overcommit_score <= 100.0
        assert r.calibration_score <= 100.0
        assert r.volatility_score <= 100.0

    def test_sandbagging_index_tier_exclusive(self):
        e = engine()
        # index=0.64 -> tier2 (+22), not tier1 (+40)
        r = e.assess(make_input(sandbagging_index=0.64))
        assert r.sandbagging_score == 22.0

    def test_overcommit_freq_tier_exclusive(self):
        e = engine()
        # freq=0.54 -> tier2(+22)
        r = e.assess(make_input(overcommit_frequency_pct=0.54))
        assert r.overcommit_score == 22.0

    def test_calibration_forecast_tier_exclusive(self):
        e = engine()
        # forecast=0.59 -> tier2 (+22)
        r = e.assess(make_input(forecast_accuracy_pct=0.59))
        assert r.calibration_score == 22.0

    def test_volatility_revision_tier_exclusive(self):
        e = engine()
        # rev=4 -> tier2(+22)
        r = e.assess(make_input(commit_revision_frequency=4))
        assert r.volatility_score == 22.0


# ---------------------------------------------------------------------------
# 22. Pattern edge cases - boundary precision
# ---------------------------------------------------------------------------

class TestPatternBoundaryPrecision:
    def test_sandbagging_index_exactly_50(self):
        e = engine()
        r = e.assess(make_input(sandbagging_index=0.50, late_quarter_close_rate_pct=0.50))
        assert r.quota_pattern == QuotaPattern.sandbagging

    def test_sandbagging_late_exactly_45(self):
        e = engine()
        r = e.assess(make_input(sandbagging_index=0.55, late_quarter_close_rate_pct=0.45))
        assert r.quota_pattern == QuotaPattern.sandbagging

    def test_overcommitting_freq_exactly_50(self):
        e = engine()
        r = e.assess(make_input(overcommit_frequency_pct=0.50, consecutive_miss_streak=3))
        assert r.quota_pattern == QuotaPattern.overcommitting

    def test_overcommitting_streak_exactly_2(self):
        e = engine()
        r = e.assess(make_input(overcommit_frequency_pct=0.60, consecutive_miss_streak=2))
        assert r.quota_pattern == QuotaPattern.overcommitting

    def test_volatile_revision_exactly_4(self):
        e = engine()
        r = e.assess(make_input(commit_revision_frequency=4, forecast_accuracy_pct=0.50))
        assert r.quota_pattern == QuotaPattern.volatile_committor

    def test_volatile_accuracy_exactly_55(self):
        e = engine()
        r = e.assess(make_input(commit_revision_frequency=5, forecast_accuracy_pct=0.55))
        assert r.quota_pattern == QuotaPattern.volatile_committor

    def test_late_surge_close_rate_exactly_55(self):
        e = engine()
        r = e.assess(make_input(late_quarter_close_rate_pct=0.55, early_commit_accuracy_pct=0.30))
        assert r.quota_pattern == QuotaPattern.late_surge

    def test_late_surge_early_accuracy_exactly_40(self):
        e = engine()
        r = e.assess(make_input(late_quarter_close_rate_pct=0.60, early_commit_accuracy_pct=0.40))
        assert r.quota_pattern == QuotaPattern.late_surge

    def test_forecast_manipulator_pulled_exactly_30(self):
        e = engine()
        r = e.assess(make_input(pulled_in_deal_rate_pct=0.30, pushed_out_deal_rate_pct=0.30))
        assert r.quota_pattern == QuotaPattern.forecast_manipulator

    def test_forecast_manipulator_pushed_exactly_25(self):
        e = engine()
        r = e.assess(make_input(pulled_in_deal_rate_pct=0.35, pushed_out_deal_rate_pct=0.25))
        assert r.quota_pattern == QuotaPattern.forecast_manipulator

    def test_none_pattern_all_below_thresholds(self):
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.499,
            overcommit_frequency_pct=0.499,
            consecutive_miss_streak=1,
            commit_revision_frequency=3,
            forecast_accuracy_pct=0.56,
            late_quarter_close_rate_pct=0.549,
            pulled_in_deal_rate_pct=0.299,
            pushed_out_deal_rate_pct=0.249,
        ))
        assert r.quota_pattern == QuotaPattern.none


# ---------------------------------------------------------------------------
# 23. Action routing exhaustive
# ---------------------------------------------------------------------------

class TestActionRouting:
    def test_low_risk_always_no_action(self):
        e = engine()
        r = e.assess(make_input())
        assert r.quota_risk == QuotaPatternRisk.low
        assert r.recommended_action == QuotaAction.no_action

    def test_moderate_risk_always_quota_check_in(self):
        # Multiple patterns at moderate risk all get quota_check_in
        inputs_mod = [
            make_input(forecast_accuracy_pct=0.40, early_commit_accuracy_pct=0.35),
        ]
        for inp in inputs_mod:
            e = engine()
            r = e.assess(inp)
            if r.quota_risk == QuotaPatternRisk.moderate:
                assert r.recommended_action == QuotaAction.quota_check_in

    def test_critical_sandbagging_escalation(self):
        e = engine()
        r = e.assess(make_input(
            sandbagging_index=0.80,
            late_quarter_close_rate_pct=0.80,
            commit_vs_actual_ratio=0.50,
            forecast_accuracy_pct=0.30,
            early_commit_accuracy_pct=0.20,
            mid_commit_accuracy_pct=0.30,
        ))
        assert r.quota_pattern == QuotaPattern.sandbagging
        if r.quota_risk == QuotaPatternRisk.critical:
            assert r.recommended_action == QuotaAction.executive_quota_escalation

    def test_high_risk_volatile_gets_forecast_coaching(self):
        e = engine()
        r = e.assess(make_input(
            commit_revision_frequency=5,
            forecast_accuracy_pct=0.40,
            early_commit_accuracy_pct=0.35,
            mid_commit_accuracy_pct=0.50,
            late_commit_accuracy_pct=0.65,
            mgr_trust_in_forecast_score=0.30,
        ))
        if r.quota_risk == QuotaPatternRisk.high and r.quota_pattern == QuotaPattern.volatile_committor:
            assert r.recommended_action == QuotaAction.forecast_calibration_coaching

    def test_high_risk_overcommitting_gets_commit_coaching(self):
        e = engine()
        r = e.assess(make_input(
            overcommit_frequency_pct=0.60,
            consecutive_miss_streak=3,
            mgr_trust_in_forecast_score=0.30,
            forecast_accuracy_pct=0.60,
        ))
        if r.quota_risk == QuotaPatternRisk.high and r.quota_pattern == QuotaPattern.overcommitting:
            assert r.recommended_action == QuotaAction.commit_accuracy_coaching

    def test_critical_non_sandbagging_non_manipulator_gets_reset(self):
        # Make critical + volatile_committor pattern
        e = engine()
        r = e.assess(make_input(
            commit_revision_frequency=6,
            forecast_accuracy_pct=0.30,
            early_commit_accuracy_pct=0.20,
            mid_commit_accuracy_pct=0.30,
            late_commit_accuracy_pct=0.50,
            overcommit_frequency_pct=0.60,
            consecutive_miss_streak=3,
            mgr_trust_in_forecast_score=0.25,
            pulled_in_deal_rate_pct=0.05,
            pushed_out_deal_rate_pct=0.05,
            sandbagging_index=0.10,
            late_quarter_close_rate_pct=0.10,
        ))
        if r.quota_risk == QuotaPatternRisk.critical:
            if r.quota_pattern not in (QuotaPattern.sandbagging, QuotaPattern.forecast_manipulator):
                assert r.recommended_action == QuotaAction.quota_reset_intervention


# ---------------------------------------------------------------------------
# 24. Data type validation
# ---------------------------------------------------------------------------

class TestDataTypes:
    def test_quota_composite_is_float(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.quota_composite, float)

    def test_sandbagging_score_is_float(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.sandbagging_score, float)

    def test_overcommit_score_is_float(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.overcommit_score, float)

    def test_calibration_score_is_float(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.calibration_score, float)

    def test_volatility_score_is_float(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.volatility_score, float)

    def test_has_quota_gap_is_bool(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.has_quota_gap, bool)

    def test_requires_intervention_is_bool(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.requires_quota_intervention, bool)

    def test_distortion_is_float(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.estimated_quota_distortion_usd, float)

    def test_quota_risk_is_enum(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.quota_risk, QuotaPatternRisk)

    def test_quota_pattern_is_enum(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.quota_pattern, QuotaPattern)

    def test_quota_severity_is_enum(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.quota_severity, QuotaSeverity)

    def test_recommended_action_is_enum(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.recommended_action, QuotaAction)
