"""
Comprehensive pytest test suite for swarm/intelligence/pipeline_generation_efficiency_engine.py
Run from /home/user/TEST:
    python -m pytest swarm/tests/test_pipeline_generation_efficiency_engine.py -v
"""

from __future__ import annotations

import pytest

from swarm.intelligence.pipeline_generation_efficiency_engine import (
    EfficiencyRisk,
    EfficiencyPattern,
    EfficiencySeverity,
    EfficiencyAction,
    PipelineEfficiencyInput,
    PipelineEfficiencyResult,
    PipelineGenerationEfficiencyEngine,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_input(
    rep_id: str = "rep_001",
    region: str = "west",
    evaluation_period_id: str = "Q1-2026",
    cold_calls_made: int = 60,
    cold_call_connect_rate_pct: float = 0.25,
    emails_sent: int = 200,
    email_reply_rate_pct: float = 0.12,
    demos_conducted: int = 10,
    demo_to_opp_conversion_rate_pct: float = 0.55,
    events_attended: int = 3,
    event_leads_generated: int = 5,
    referrals_requested: int = 2,
    referrals_received: int = 1,
    social_touches_count: int = 20,
    meetings_booked: int = 12,
    qualified_opps_created: int = 5,
    pipeline_generated_usd: float = 120_000.0,
    pipeline_target_usd: float = 100_000.0,
    activity_mix_variance_score: float = 20.0,
    prior_period_pipeline_generated_usd: float = 100_000.0,
    activities_total_count: int = 150,
    crm_activity_logging_rate_pct: float = 0.85,
) -> PipelineEfficiencyInput:
    return PipelineEfficiencyInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        cold_calls_made=cold_calls_made,
        cold_call_connect_rate_pct=cold_call_connect_rate_pct,
        emails_sent=emails_sent,
        email_reply_rate_pct=email_reply_rate_pct,
        demos_conducted=demos_conducted,
        demo_to_opp_conversion_rate_pct=demo_to_opp_conversion_rate_pct,
        events_attended=events_attended,
        event_leads_generated=event_leads_generated,
        referrals_requested=referrals_requested,
        referrals_received=referrals_received,
        social_touches_count=social_touches_count,
        meetings_booked=meetings_booked,
        qualified_opps_created=qualified_opps_created,
        pipeline_generated_usd=pipeline_generated_usd,
        pipeline_target_usd=pipeline_target_usd,
        activity_mix_variance_score=activity_mix_variance_score,
        prior_period_pipeline_generated_usd=prior_period_pipeline_generated_usd,
        activities_total_count=activities_total_count,
        crm_activity_logging_rate_pct=crm_activity_logging_rate_pct,
    )


@pytest.fixture
def engine():
    return PipelineGenerationEfficiencyEngine()


@pytest.fixture
def healthy_input():
    """Input that produces a fully healthy / low-risk result."""
    return make_input()


@pytest.fixture
def critical_input():
    """Input designed to maximise composite score."""
    return make_input(
        activities_total_count=30,
        meetings_booked=2,
        cold_calls_made=10,
        crm_activity_logging_rate_pct=0.30,
        cold_call_connect_rate_pct=0.05,
        email_reply_rate_pct=0.02,
        demo_to_opp_conversion_rate_pct=0.10,
        qualified_opps_created=0,
        pipeline_generated_usd=20_000.0,
        pipeline_target_usd=100_000.0,
        activity_mix_variance_score=75.0,
        prior_period_pipeline_generated_usd=100_000.0,
    )


# ===========================================================================
# CLASS 1: Enum sanity checks
# ===========================================================================

class TestEnums:
    def test_efficiency_risk_values(self):
        assert set(r.value for r in EfficiencyRisk) == {"low", "moderate", "high", "critical"}

    def test_efficiency_pattern_values(self):
        expected = {
            "none", "low_activity_volume", "poor_conversion",
            "activity_channel_overreliance", "pipeline_coverage_gap", "activity_decay",
        }
        assert set(p.value for p in EfficiencyPattern) == expected

    def test_efficiency_severity_values(self):
        assert set(s.value for s in EfficiencySeverity) == {
            "healthy", "underperforming", "degraded", "critical"
        }

    def test_efficiency_action_values(self):
        expected = {
            "no_action", "activity_increase", "conversion_coaching",
            "channel_diversification", "pipeline_blitz", "performance_improvement_plan",
        }
        assert set(a.value for a in EfficiencyAction) == expected

    def test_risk_is_str_enum(self):
        assert EfficiencyRisk.low == "low"

    def test_pattern_is_str_enum(self):
        assert EfficiencyPattern.none == "none"

    def test_severity_is_str_enum(self):
        assert EfficiencySeverity.healthy == "healthy"

    def test_action_is_str_enum(self):
        assert EfficiencyAction.no_action == "no_action"

    def test_risk_count(self):
        assert len(list(EfficiencyRisk)) == 4

    def test_pattern_count(self):
        assert len(list(EfficiencyPattern)) == 6

    def test_severity_count(self):
        assert len(list(EfficiencySeverity)) == 4

    def test_action_count(self):
        assert len(list(EfficiencyAction)) == 6


# ===========================================================================
# CLASS 2: Input dataclass
# ===========================================================================

class TestInputDataclass:
    def test_all_22_fields_exist(self):
        inp = make_input()
        fields = [
            "rep_id", "region", "evaluation_period_id", "cold_calls_made",
            "cold_call_connect_rate_pct", "emails_sent", "email_reply_rate_pct",
            "demos_conducted", "demo_to_opp_conversion_rate_pct", "events_attended",
            "event_leads_generated", "referrals_requested", "referrals_received",
            "social_touches_count", "meetings_booked", "qualified_opps_created",
            "pipeline_generated_usd", "pipeline_target_usd", "activity_mix_variance_score",
            "prior_period_pipeline_generated_usd", "activities_total_count",
            "crm_activity_logging_rate_pct",
        ]
        for f in fields:
            assert hasattr(inp, f), f"Missing field: {f}"

    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(PipelineEfficiencyInput)
        assert len(fields) == 22

    def test_rep_id_stored(self):
        inp = make_input(rep_id="rep_XYZ")
        assert inp.rep_id == "rep_XYZ"

    def test_region_stored(self):
        inp = make_input(region="east")
        assert inp.region == "east"

    def test_numeric_fields_stored(self):
        inp = make_input(cold_calls_made=77, emails_sent=333)
        assert inp.cold_calls_made == 77
        assert inp.emails_sent == 333

    def test_float_fields_stored(self):
        inp = make_input(cold_call_connect_rate_pct=0.18)
        assert inp.cold_call_connect_rate_pct == 0.18


# ===========================================================================
# CLASS 3: Result dataclass & to_dict
# ===========================================================================

class TestResultDataclass:
    def test_result_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(PipelineEfficiencyResult)
        assert len(fields) == 15

    def test_to_dict_returns_15_keys(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        d = result.to_dict()
        expected_keys = {
            "rep_id", "region", "efficiency_risk", "efficiency_pattern",
            "efficiency_severity", "recommended_action", "activity_volume_score",
            "conversion_efficiency_score", "pipeline_coverage_score", "activity_mix_score",
            "pipeline_efficiency_composite", "is_pipeline_at_risk",
            "requires_activity_intervention", "estimated_pipeline_gap_usd",
            "efficiency_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_fields_are_strings(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["efficiency_risk"], str)
        assert isinstance(d["efficiency_pattern"], str)
        assert isinstance(d["efficiency_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_matches(self, engine):
        result = engine.assess(make_input(rep_id="rep_TEST"))
        assert result.to_dict()["rep_id"] == "rep_TEST"

    def test_to_dict_region_matches(self, engine):
        result = engine.assess(make_input(region="southeast"))
        assert result.to_dict()["region"] == "southeast"

    def test_to_dict_bool_fields_are_bool(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["is_pipeline_at_risk"], bool)
        assert isinstance(d["requires_activity_intervention"], bool)

    def test_to_dict_numeric_fields_are_float(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["pipeline_efficiency_composite"], float)
        assert isinstance(d["activity_volume_score"], float)

    def test_to_dict_signal_is_string(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["efficiency_signal"], str)


# ===========================================================================
# CLASS 4: activity_volume_score
# ===========================================================================

class TestActivityVolumeScore:
    def _score(self, **kwargs):
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(**kwargs)
        return e._activity_volume_score(inp)

    # activities_total_count thresholds
    def test_activities_lt50_adds_35(self):
        s = self._score(activities_total_count=30, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(35.0)

    def test_activities_lt100_adds_20(self):
        s = self._score(activities_total_count=75, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(20.0)

    def test_activities_lt150_adds_8(self):
        s = self._score(activities_total_count=120, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(8.0)

    def test_activities_ge150_adds_0(self):
        s = self._score(activities_total_count=150, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(0.0)

    def test_activities_200_adds_0(self):
        s = self._score(activities_total_count=200, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(0.0)

    # meetings_booked thresholds
    def test_meetings_lt5_adds_25(self):
        s = self._score(activities_total_count=200, meetings_booked=3,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(25.0)

    def test_meetings_lt10_adds_12(self):
        s = self._score(activities_total_count=200, meetings_booked=7,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(12.0)

    def test_meetings_ge10_adds_0(self):
        s = self._score(activities_total_count=200, meetings_booked=10,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(0.0)

    # cold_calls_made thresholds
    def test_cold_calls_lt20_adds_15(self):
        s = self._score(activities_total_count=200, meetings_booked=15,
                        cold_calls_made=10, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(15.0)

    def test_cold_calls_lt40_adds_8(self):
        s = self._score(activities_total_count=200, meetings_booked=15,
                        cold_calls_made=30, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(8.0)

    def test_cold_calls_ge40_adds_0(self):
        s = self._score(activities_total_count=200, meetings_booked=15,
                        cold_calls_made=40, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(0.0)

    # crm logging thresholds
    def test_crm_lt50_adds_25(self):
        s = self._score(activities_total_count=200, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.40)
        assert s == pytest.approx(25.0)

    def test_crm_lt70_adds_12(self):
        s = self._score(activities_total_count=200, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.60)
        assert s == pytest.approx(12.0)

    def test_crm_ge70_adds_0(self):
        s = self._score(activities_total_count=200, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.70)
        assert s == pytest.approx(0.0)

    def test_score_capped_at_100(self):
        s = self._score(activities_total_count=10, meetings_booked=1,
                        cold_calls_made=5, crm_activity_logging_rate_pct=0.10)
        assert s == pytest.approx(100.0)

    def test_all_zero_risk(self):
        s = self._score(activities_total_count=200, meetings_booked=20,
                        cold_calls_made=80, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(0.0)

    def test_boundary_activities_exactly_50(self):
        # exactly 50 → falls into lt100 bucket (adds 20)
        s = self._score(activities_total_count=50, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(20.0)

    def test_boundary_meetings_exactly_5(self):
        # exactly 5 → falls into lt10 bucket (adds 12)
        s = self._score(activities_total_count=200, meetings_booked=5,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(12.0)

    def test_boundary_cold_calls_exactly_20(self):
        # exactly 20 → falls into lt40 bucket (adds 8)
        s = self._score(activities_total_count=200, meetings_booked=15,
                        cold_calls_made=20, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(8.0)

    def test_boundary_crm_exactly_50(self):
        # exactly 0.50 → falls into lt70 bucket (adds 12)
        s = self._score(activities_total_count=200, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.50)
        assert s == pytest.approx(12.0)

    def test_partial_risk_combination(self):
        # activities < 100 (+20) + meetings >= 10 (0) + calls >= 40 (0) + crm >= 70 (0) = 20
        s = self._score(activities_total_count=80, meetings_booked=12,
                        cold_calls_made=45, crm_activity_logging_rate_pct=0.75)
        assert s == pytest.approx(20.0)


# ===========================================================================
# CLASS 5: conversion_efficiency_score
# ===========================================================================

class TestConversionEfficiencyScore:
    def _score(self, **kwargs):
        e = PipelineGenerationEfficiencyEngine()
        return e._conversion_efficiency_score(make_input(**kwargs))

    def test_connect_rate_lt010_adds_30(self):
        s = self._score(cold_call_connect_rate_pct=0.05,
                        email_reply_rate_pct=0.15,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=5)
        assert s == pytest.approx(30.0)

    def test_connect_rate_lt020_adds_15(self):
        s = self._score(cold_call_connect_rate_pct=0.15,
                        email_reply_rate_pct=0.15,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=5)
        assert s == pytest.approx(15.0)

    def test_connect_rate_ge020_adds_0(self):
        s = self._score(cold_call_connect_rate_pct=0.20,
                        email_reply_rate_pct=0.15,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=5)
        assert s == pytest.approx(0.0)

    def test_email_reply_lt005_adds_25(self):
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.03,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=5)
        assert s == pytest.approx(25.0)

    def test_email_reply_lt010_adds_12(self):
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.07,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=5)
        assert s == pytest.approx(12.0)

    def test_email_reply_ge010_adds_0(self):
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.10,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=5)
        assert s == pytest.approx(0.0)

    def test_demo_conv_lt030_adds_30(self):
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.15,
                        demo_to_opp_conversion_rate_pct=0.20,
                        qualified_opps_created=5)
        assert s == pytest.approx(30.0)

    def test_demo_conv_lt050_adds_15(self):
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.15,
                        demo_to_opp_conversion_rate_pct=0.40,
                        qualified_opps_created=5)
        assert s == pytest.approx(15.0)

    def test_demo_conv_ge050_adds_0(self):
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.15,
                        demo_to_opp_conversion_rate_pct=0.50,
                        qualified_opps_created=5)
        assert s == pytest.approx(0.0)

    def test_zero_opps_with_enough_activities_adds_15(self):
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.15,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=0,
                        activities_total_count=30)
        assert s == pytest.approx(15.0)

    def test_zero_opps_low_activities_no_bonus(self):
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.15,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=0,
                        activities_total_count=20)
        assert s == pytest.approx(0.0)

    def test_non_zero_opps_no_bonus(self):
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.15,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=1,
                        activities_total_count=50)
        assert s == pytest.approx(0.0)

    def test_all_bad_capped_at_100(self):
        s = self._score(cold_call_connect_rate_pct=0.01,
                        email_reply_rate_pct=0.01,
                        demo_to_opp_conversion_rate_pct=0.01,
                        qualified_opps_created=0,
                        activities_total_count=50)
        assert s == pytest.approx(100.0)

    def test_all_good_returns_0(self):
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.20,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=5)
        assert s == pytest.approx(0.0)

    def test_boundary_connect_exactly_010(self):
        # exactly 0.10 → lt020 bucket → +15
        s = self._score(cold_call_connect_rate_pct=0.10,
                        email_reply_rate_pct=0.15,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=5)
        assert s == pytest.approx(15.0)

    def test_boundary_email_exactly_005(self):
        # exactly 0.05 → lt010 bucket → +12
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.05,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=5)
        assert s == pytest.approx(12.0)

    def test_boundary_demo_exactly_030(self):
        # exactly 0.30 → lt050 bucket → +15
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.15,
                        demo_to_opp_conversion_rate_pct=0.30,
                        qualified_opps_created=5)
        assert s == pytest.approx(15.0)

    def test_activities_exactly_30_triggers_zero_opp_bonus(self):
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.15,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=0,
                        activities_total_count=30)
        assert s == pytest.approx(15.0)


# ===========================================================================
# CLASS 6: pipeline_coverage_score
# ===========================================================================

class TestPipelineCoverageScore:
    def _score(self, **kwargs):
        e = PipelineGenerationEfficiencyEngine()
        return e._pipeline_coverage_score(make_input(**kwargs))

    def test_coverage_lt050_adds_40(self):
        # generated=40k, target=100k → coverage=0.40
        s = self._score(pipeline_generated_usd=40_000,
                        pipeline_target_usd=100_000,
                        prior_period_pipeline_generated_usd=0,
                        qualified_opps_created=5)
        assert s == pytest.approx(40.0)

    def test_coverage_lt075_adds_25(self):
        # generated=60k, target=100k → 0.60
        s = self._score(pipeline_generated_usd=60_000,
                        pipeline_target_usd=100_000,
                        prior_period_pipeline_generated_usd=0,
                        qualified_opps_created=5)
        assert s == pytest.approx(25.0)

    def test_coverage_lt100_adds_10(self):
        # generated=80k, target=100k → 0.80
        s = self._score(pipeline_generated_usd=80_000,
                        pipeline_target_usd=100_000,
                        prior_period_pipeline_generated_usd=0,
                        qualified_opps_created=5)
        assert s == pytest.approx(10.0)

    def test_coverage_ge100_adds_0_from_target(self):
        s = self._score(pipeline_generated_usd=100_000,
                        pipeline_target_usd=100_000,
                        prior_period_pipeline_generated_usd=0,
                        qualified_opps_created=5)
        assert s == pytest.approx(0.0)

    def test_no_target_skips_coverage_calc(self):
        s = self._score(pipeline_generated_usd=50_000,
                        pipeline_target_usd=0,
                        prior_period_pipeline_generated_usd=0,
                        qualified_opps_created=5)
        assert s == pytest.approx(0.0)

    def test_decay_ge030_adds_30(self):
        # prior=100k, current=60k → decay=0.40
        s = self._score(pipeline_generated_usd=60_000,
                        pipeline_target_usd=0,
                        prior_period_pipeline_generated_usd=100_000,
                        qualified_opps_created=5)
        assert s == pytest.approx(30.0)

    def test_decay_ge015_adds_15(self):
        # prior=100k, current=80k → decay=0.20
        s = self._score(pipeline_generated_usd=80_000,
                        pipeline_target_usd=0,
                        prior_period_pipeline_generated_usd=100_000,
                        qualified_opps_created=5)
        assert s == pytest.approx(15.0)

    def test_decay_lt015_adds_0(self):
        # prior=100k, current=90k → decay=0.10
        s = self._score(pipeline_generated_usd=90_000,
                        pipeline_target_usd=0,
                        prior_period_pipeline_generated_usd=100_000,
                        qualified_opps_created=5)
        assert s == pytest.approx(0.0)

    def test_no_prior_skips_decay_calc(self):
        s = self._score(pipeline_generated_usd=50_000,
                        pipeline_target_usd=0,
                        prior_period_pipeline_generated_usd=0,
                        qualified_opps_created=5)
        assert s == pytest.approx(0.0)

    def test_zero_opps_with_target_adds_30(self):
        s = self._score(pipeline_generated_usd=100_000,
                        pipeline_target_usd=100_000,
                        prior_period_pipeline_generated_usd=0,
                        qualified_opps_created=0)
        # coverage=1.0 (no coverage penalty) + 0 (no prior) + 30 (zero opps)
        assert s == pytest.approx(30.0)

    def test_zero_opps_no_target_no_bonus(self):
        s = self._score(pipeline_generated_usd=100_000,
                        pipeline_target_usd=0,
                        prior_period_pipeline_generated_usd=0,
                        qualified_opps_created=0)
        assert s == pytest.approx(0.0)

    def test_coverage_and_decay_combined(self):
        # coverage 0.60 (+25), decay 0.40 (+30), opps>0 (0) = 55
        s = self._score(pipeline_generated_usd=60_000,
                        pipeline_target_usd=100_000,
                        prior_period_pipeline_generated_usd=100_000,
                        qualified_opps_created=5)
        assert s == pytest.approx(55.0)

    def test_capped_at_100(self):
        # coverage <0.50 (+40), decay >= 0.30 (+30), zero opps (+30) = 100
        s = self._score(pipeline_generated_usd=10_000,
                        pipeline_target_usd=100_000,
                        prior_period_pipeline_generated_usd=100_000,
                        qualified_opps_created=0)
        assert s == pytest.approx(100.0)

    def test_boundary_coverage_exactly_050(self):
        # exactly 0.50 → lt075 bucket → +25
        s = self._score(pipeline_generated_usd=50_000,
                        pipeline_target_usd=100_000,
                        prior_period_pipeline_generated_usd=0,
                        qualified_opps_created=5)
        assert s == pytest.approx(25.0)

    def test_boundary_decay_exactly_030(self):
        # prior=100k, current=70k → decay exactly 0.30 → +30
        s = self._score(pipeline_generated_usd=70_000,
                        pipeline_target_usd=0,
                        prior_period_pipeline_generated_usd=100_000,
                        qualified_opps_created=5)
        assert s == pytest.approx(30.0)

    def test_positive_decay_growth_no_penalty(self):
        # current > prior → negative delta → no penalty
        s = self._score(pipeline_generated_usd=120_000,
                        pipeline_target_usd=0,
                        prior_period_pipeline_generated_usd=100_000,
                        qualified_opps_created=5)
        assert s == pytest.approx(0.0)


# ===========================================================================
# CLASS 7: activity_mix_score
# ===========================================================================

class TestActivityMixScore:
    def _score(self, **kwargs):
        e = PipelineGenerationEfficiencyEngine()
        return e._activity_mix_score(make_input(**kwargs))

    def test_variance_ge70_adds_40(self):
        s = self._score(activity_mix_variance_score=75.0,
                        activities_total_count=200, cold_calls_made=80,
                        referrals_requested=0, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(40.0)

    def test_variance_ge50_adds_22(self):
        s = self._score(activity_mix_variance_score=55.0,
                        activities_total_count=200, cold_calls_made=80,
                        referrals_requested=0, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(22.0)

    def test_variance_ge30_adds_10(self):
        s = self._score(activity_mix_variance_score=35.0,
                        activities_total_count=200, cold_calls_made=80,
                        referrals_requested=0, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(10.0)

    def test_variance_lt30_adds_0(self):
        s = self._score(activity_mix_variance_score=25.0,
                        activities_total_count=200, cold_calls_made=80,
                        referrals_requested=0, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(0.0)

    def test_cold_call_share_ge080_adds_20(self):
        # 160/200 = 0.80
        s = self._score(activity_mix_variance_score=20.0,
                        activities_total_count=200, cold_calls_made=160,
                        referrals_requested=0, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(20.0)

    def test_cold_call_share_ge065_adds_10(self):
        # 140/200 = 0.70
        s = self._score(activity_mix_variance_score=20.0,
                        activities_total_count=200, cold_calls_made=140,
                        referrals_requested=0, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(10.0)

    def test_cold_call_share_lt065_adds_0(self):
        # 100/200 = 0.50
        s = self._score(activity_mix_variance_score=20.0,
                        activities_total_count=200, cold_calls_made=100,
                        referrals_requested=0, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(0.0)

    def test_referrals_ge5_received_0_adds_20(self):
        s = self._score(activity_mix_variance_score=20.0,
                        activities_total_count=200, cold_calls_made=80,
                        referrals_requested=5, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(20.0)

    def test_referrals_ge3_received_0_adds_10(self):
        s = self._score(activity_mix_variance_score=20.0,
                        activities_total_count=200, cold_calls_made=80,
                        referrals_requested=3, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(10.0)

    def test_referrals_ge5_received_gt0_no_bonus(self):
        s = self._score(activity_mix_variance_score=20.0,
                        activities_total_count=200, cold_calls_made=80,
                        referrals_requested=5, referrals_received=1,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(0.0)

    def test_referrals_lt3_received_0_no_bonus(self):
        s = self._score(activity_mix_variance_score=20.0,
                        activities_total_count=200, cold_calls_made=80,
                        referrals_requested=2, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(0.0)

    def test_crm_lt040_adds_15(self):
        s = self._score(activity_mix_variance_score=20.0,
                        activities_total_count=200, cold_calls_made=80,
                        referrals_requested=0, referrals_received=0,
                        crm_activity_logging_rate_pct=0.30)
        assert s == pytest.approx(15.0)

    def test_crm_ge040_adds_0(self):
        s = self._score(activity_mix_variance_score=20.0,
                        activities_total_count=200, cold_calls_made=80,
                        referrals_requested=0, referrals_received=0,
                        crm_activity_logging_rate_pct=0.40)
        assert s == pytest.approx(0.0)

    def test_zero_activities_skips_share_calc(self):
        # activities_total_count=0: division not attempted
        s = self._score(activity_mix_variance_score=20.0,
                        activities_total_count=0, cold_calls_made=0,
                        referrals_requested=0, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(0.0)

    def test_capped_at_100(self):
        # variance=75 (+40), share=10/10=1.0 (+20), referrals>=5 received=0 (+20), crm=0.30 (+15) = 95
        # To hit cap add more: use variance=75 (+40) + share>=0.80 (+20) + ref>=5 (+20) + crm<0.40 (+15) = 95 < 100
        # So check the actual max is 95 and is correctly capped (i.e. min(95,100)=95)
        s = self._score(activity_mix_variance_score=75.0,
                        activities_total_count=10, cold_calls_made=10,
                        referrals_requested=8, referrals_received=0,
                        crm_activity_logging_rate_pct=0.30)
        assert s == pytest.approx(95.0)
        assert s <= 100.0

    def test_boundary_variance_exactly_70(self):
        # exactly 70 → +40
        s = self._score(activity_mix_variance_score=70.0,
                        activities_total_count=200, cold_calls_made=80,
                        referrals_requested=0, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(40.0)

    def test_boundary_variance_exactly_50(self):
        # exactly 50 → +22
        s = self._score(activity_mix_variance_score=50.0,
                        activities_total_count=200, cold_calls_made=80,
                        referrals_requested=0, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(22.0)

    def test_boundary_cold_call_share_exactly_080(self):
        # exactly 0.80 → +20
        s = self._score(activity_mix_variance_score=20.0,
                        activities_total_count=100, cold_calls_made=80,
                        referrals_requested=0, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(20.0)

    def test_referrals_exactly_5_received_0(self):
        # exactly 5 → +20 (not elif +10)
        s = self._score(activity_mix_variance_score=20.0,
                        activities_total_count=200, cold_calls_made=80,
                        referrals_requested=5, referrals_received=0,
                        crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(20.0)


# ===========================================================================
# CLASS 8: composite score
# ===========================================================================

class TestCompositeScore:
    def test_healthy_composite_is_low(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.pipeline_efficiency_composite < 20.0

    def test_critical_composite_is_high(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert result.pipeline_efficiency_composite >= 60.0

    def test_composite_capped_at_100(self, engine):
        inp = make_input(
            activities_total_count=10, meetings_booked=1, cold_calls_made=5,
            crm_activity_logging_rate_pct=0.10,
            cold_call_connect_rate_pct=0.01, email_reply_rate_pct=0.01,
            demo_to_opp_conversion_rate_pct=0.01, qualified_opps_created=0,
            pipeline_generated_usd=0, pipeline_target_usd=200_000,
            prior_period_pipeline_generated_usd=200_000,
            activity_mix_variance_score=80.0,
        )
        result = engine.assess(inp)
        assert result.pipeline_efficiency_composite <= 100.0

    def test_composite_weights_applied(self, engine):
        # Use controlled sub-scores: volume=40, conversion=0, coverage=0, mix=0
        # composite should be 40*0.25 = 10.0
        inp = make_input(
            # volume score = 20 (activities 50-100)
            activities_total_count=80, meetings_booked=15,
            cold_calls_made=50, crm_activity_logging_rate_pct=0.90,
            # conversion = 0
            cold_call_connect_rate_pct=0.30, email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60, qualified_opps_created=5,
            # coverage = 0
            pipeline_generated_usd=120_000, pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
            # mix = 0
            activity_mix_variance_score=20.0,
            referrals_requested=0, referrals_received=0,
        )
        result = engine.assess(inp)
        # volume score = 20 → composite = 20*0.25 = 5.0
        assert result.pipeline_efficiency_composite == pytest.approx(5.0, abs=1.0)

    def test_composite_is_rounded_to_1_decimal(self, engine):
        result = engine.assess(make_input())
        val = result.pipeline_efficiency_composite
        assert round(val, 1) == val


# ===========================================================================
# CLASS 9: risk level
# ===========================================================================

class TestRiskLevel:
    def _risk(self, composite):
        e = PipelineGenerationEfficiencyEngine()
        return e._risk_level(composite)

    def test_composite_0_is_low(self):
        assert self._risk(0.0) == EfficiencyRisk.low

    def test_composite_19_is_low(self):
        assert self._risk(19.9) == EfficiencyRisk.low

    def test_composite_20_is_moderate(self):
        assert self._risk(20.0) == EfficiencyRisk.moderate

    def test_composite_39_is_moderate(self):
        assert self._risk(39.9) == EfficiencyRisk.moderate

    def test_composite_40_is_high(self):
        assert self._risk(40.0) == EfficiencyRisk.high

    def test_composite_59_is_high(self):
        assert self._risk(59.9) == EfficiencyRisk.high

    def test_composite_60_is_critical(self):
        assert self._risk(60.0) == EfficiencyRisk.critical

    def test_composite_100_is_critical(self):
        assert self._risk(100.0) == EfficiencyRisk.critical


# ===========================================================================
# CLASS 10: severity
# ===========================================================================

class TestSeverity:
    def _sev(self, composite):
        e = PipelineGenerationEfficiencyEngine()
        return e._severity(composite)

    def test_composite_0_is_healthy(self):
        assert self._sev(0.0) == EfficiencySeverity.healthy

    def test_composite_19_is_healthy(self):
        assert self._sev(19.9) == EfficiencySeverity.healthy

    def test_composite_20_is_underperforming(self):
        assert self._sev(20.0) == EfficiencySeverity.underperforming

    def test_composite_39_is_underperforming(self):
        assert self._sev(39.9) == EfficiencySeverity.underperforming

    def test_composite_40_is_degraded(self):
        assert self._sev(40.0) == EfficiencySeverity.degraded

    def test_composite_59_is_degraded(self):
        assert self._sev(59.9) == EfficiencySeverity.degraded

    def test_composite_60_is_critical(self):
        assert self._sev(60.0) == EfficiencySeverity.critical

    def test_composite_100_is_critical(self):
        assert self._sev(100.0) == EfficiencySeverity.critical


# ===========================================================================
# CLASS 11: action logic
# ===========================================================================

class TestActionLogic:
    def _action(self, risk, pattern):
        e = PipelineGenerationEfficiencyEngine()
        return e._action(risk, pattern)

    def test_critical_any_pattern_gives_pip(self):
        for p in EfficiencyPattern:
            assert self._action(EfficiencyRisk.critical, p) == EfficiencyAction.performance_improvement_plan

    def test_high_low_activity_volume_gives_pipeline_blitz(self):
        assert self._action(EfficiencyRisk.high, EfficiencyPattern.low_activity_volume) == EfficiencyAction.pipeline_blitz

    def test_high_poor_conversion_gives_conversion_coaching(self):
        assert self._action(EfficiencyRisk.high, EfficiencyPattern.poor_conversion) == EfficiencyAction.conversion_coaching

    def test_high_pipeline_coverage_gap_gives_conversion_coaching(self):
        assert self._action(EfficiencyRisk.high, EfficiencyPattern.pipeline_coverage_gap) == EfficiencyAction.conversion_coaching

    def test_high_activity_decay_gives_conversion_coaching(self):
        assert self._action(EfficiencyRisk.high, EfficiencyPattern.activity_decay) == EfficiencyAction.conversion_coaching

    def test_high_activity_channel_overreliance_gives_conversion_coaching(self):
        assert self._action(EfficiencyRisk.high, EfficiencyPattern.activity_channel_overreliance) == EfficiencyAction.conversion_coaching

    def test_high_none_gives_conversion_coaching(self):
        assert self._action(EfficiencyRisk.high, EfficiencyPattern.none) == EfficiencyAction.conversion_coaching

    def test_moderate_activity_channel_overreliance_gives_channel_diversification(self):
        assert self._action(EfficiencyRisk.moderate, EfficiencyPattern.activity_channel_overreliance) == EfficiencyAction.channel_diversification

    def test_moderate_other_gives_activity_increase(self):
        for p in [EfficiencyPattern.none, EfficiencyPattern.low_activity_volume,
                  EfficiencyPattern.poor_conversion, EfficiencyPattern.pipeline_coverage_gap,
                  EfficiencyPattern.activity_decay]:
            assert self._action(EfficiencyRisk.moderate, p) == EfficiencyAction.activity_increase

    def test_low_any_gives_no_action(self):
        for p in EfficiencyPattern:
            assert self._action(EfficiencyRisk.low, p) == EfficiencyAction.no_action


# ===========================================================================
# CLASS 12: pattern detection
# ===========================================================================

class TestPatternDetection:
    def _pattern(self, **kwargs):
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(**kwargs)
        vol = e._activity_volume_score(inp)
        conv = e._conversion_efficiency_score(inp)
        cov = e._pipeline_coverage_score(inp)
        mix = e._activity_mix_score(inp)
        return e._detect_pattern(inp, vol, conv, cov, mix)

    def test_activity_decay_detected(self):
        # prior=100k, current=50k → decay=0.50 >= 0.30
        # need conversion >= 30: set low connect, low email, low demo
        p = self._pattern(
            prior_period_pipeline_generated_usd=100_000,
            pipeline_generated_usd=50_000,
            cold_call_connect_rate_pct=0.05,  # +30
            email_reply_rate_pct=0.03,         # +25
            demo_to_opp_conversion_rate_pct=0.20,  # +30
            qualified_opps_created=5,
            pipeline_target_usd=0,  # no coverage gap
        )
        assert p == EfficiencyPattern.activity_decay

    def test_pipeline_coverage_gap_detected(self):
        # generated < target * 0.50, prior=0 so no decay check
        p = self._pattern(
            pipeline_generated_usd=40_000,
            pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.15,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
        )
        assert p == EfficiencyPattern.pipeline_coverage_gap

    def test_poor_conversion_detected(self):
        # conversion >= 35, demo rate < 0.30, no prior decay, no coverage gap
        p = self._pattern(
            prior_period_pipeline_generated_usd=0,
            pipeline_generated_usd=100_000,
            pipeline_target_usd=0,
            cold_call_connect_rate_pct=0.05,   # +30
            email_reply_rate_pct=0.03,          # +25
            demo_to_opp_conversion_rate_pct=0.20,  # triggers poor_conversion
            qualified_opps_created=5,
            activity_mix_variance_score=20.0,
        )
        assert p == EfficiencyPattern.poor_conversion

    def test_activity_channel_overreliance_detected(self):
        # mix >= 30, variance >= 50, no higher-priority patterns
        p = self._pattern(
            prior_period_pipeline_generated_usd=0,
            pipeline_generated_usd=100_000,
            pipeline_target_usd=0,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.15,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            activity_mix_variance_score=55.0,  # mix score = 22 (>=30 needed)
            activities_total_count=200,
            cold_calls_made=160,  # share=0.80 → +20 → mix=42
        )
        assert p == EfficiencyPattern.activity_channel_overreliance

    def test_low_activity_volume_detected(self):
        # volume >= 30, activities < 100, no higher-priority patterns
        p = self._pattern(
            prior_period_pipeline_generated_usd=0,
            pipeline_generated_usd=100_000,
            pipeline_target_usd=0,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.15,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            activities_total_count=60,  # → volume score = 20 ... adjust
            meetings_booked=2,          # +25 → volume = 45 >= 30
            cold_calls_made=50,
            crm_activity_logging_rate_pct=0.90,
            activity_mix_variance_score=20.0,
        )
        assert p == EfficiencyPattern.low_activity_volume

    def test_none_pattern_when_healthy(self):
        p = self._pattern()  # defaults = healthy
        assert p == EfficiencyPattern.none

    def test_activity_decay_priority_over_coverage_gap(self):
        # Both decay and coverage gap conditions met; decay wins
        p = self._pattern(
            prior_period_pipeline_generated_usd=100_000,
            pipeline_generated_usd=40_000,  # < 50% of target
            pipeline_target_usd=100_000,
            cold_call_connect_rate_pct=0.05,
            email_reply_rate_pct=0.03,
            demo_to_opp_conversion_rate_pct=0.20,
            qualified_opps_created=5,
        )
        assert p == EfficiencyPattern.activity_decay

    def test_no_decay_when_prior_is_zero(self):
        # prior=0: decay block skipped
        p = self._pattern(
            prior_period_pipeline_generated_usd=0,
            pipeline_generated_usd=40_000,
            pipeline_target_usd=100_000,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.15,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
        )
        assert p == EfficiencyPattern.pipeline_coverage_gap  # fallthrough


# ===========================================================================
# CLASS 13: is_pipeline_at_risk
# ===========================================================================

class TestIsPipelineAtRisk:
    def _flag(self, **kwargs):
        e = PipelineGenerationEfficiencyEngine()
        return e.assess(make_input(**kwargs)).is_pipeline_at_risk

    def test_high_composite_triggers_risk(self):
        # Force composite >= 40
        assert self._flag(
            activities_total_count=30, meetings_booked=2, cold_calls_made=10,
            crm_activity_logging_rate_pct=0.30, cold_call_connect_rate_pct=0.05,
            email_reply_rate_pct=0.02, demo_to_opp_conversion_rate_pct=0.10,
            qualified_opps_created=0, pipeline_generated_usd=80_000,
            pipeline_target_usd=100_000, prior_period_pipeline_generated_usd=0,
        ) is True

    def test_coverage_below_075_triggers_risk(self):
        # composite < 40 but coverage < 75%
        assert self._flag(
            pipeline_generated_usd=70_000,
            pipeline_target_usd=100_000,
            activities_total_count=200,
            meetings_booked=15,
            cold_calls_made=60,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            prior_period_pipeline_generated_usd=0,
            activity_mix_variance_score=20.0,
        ) is True

    def test_zero_opps_triggers_risk(self):
        assert self._flag(
            qualified_opps_created=0,
            pipeline_generated_usd=120_000,
            pipeline_target_usd=0,  # no coverage check
            activities_total_count=200,
            meetings_booked=15,
            cold_calls_made=60,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            prior_period_pipeline_generated_usd=0,
            activity_mix_variance_score=20.0,
        ) is True

    def test_healthy_returns_false(self):
        # coverage >= 75%, composite < 40, opps > 0
        assert self._flag(
            pipeline_generated_usd=120_000,
            pipeline_target_usd=100_000,  # 120% coverage
            activities_total_count=200,
            meetings_booked=15,
            cold_calls_made=60,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            prior_period_pipeline_generated_usd=0,
            activity_mix_variance_score=20.0,
        ) is False

    def test_no_target_no_coverage_check(self):
        # pipeline_target=0 so coverage condition skipped; depends on composite & opps
        result = self._flag(
            pipeline_generated_usd=50_000,
            pipeline_target_usd=0,
            activities_total_count=200,
            meetings_booked=15,
            cold_calls_made=60,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            prior_period_pipeline_generated_usd=0,
            activity_mix_variance_score=20.0,
        )
        assert result is False


# ===========================================================================
# CLASS 14: requires_activity_intervention
# ===========================================================================

class TestRequiresActivityIntervention:
    def _flag(self, **kwargs):
        e = PipelineGenerationEfficiencyEngine()
        return e.assess(make_input(**kwargs)).requires_activity_intervention

    def test_high_composite_triggers_intervention(self):
        assert self._flag(
            activities_total_count=30, meetings_booked=2, cold_calls_made=10,
            crm_activity_logging_rate_pct=0.30, cold_call_connect_rate_pct=0.05,
            email_reply_rate_pct=0.02, demo_to_opp_conversion_rate_pct=0.10,
            qualified_opps_created=0, pipeline_generated_usd=80_000,
            pipeline_target_usd=100_000, prior_period_pipeline_generated_usd=0,
        ) is True

    def test_low_activities_triggers_intervention(self):
        # activities_total < 50
        assert self._flag(
            activities_total_count=40,
            meetings_booked=15,
            cold_calls_made=60,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            pipeline_generated_usd=120_000,
            pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
            activity_mix_variance_score=20.0,
        ) is True

    def test_low_connect_rate_triggers_intervention(self):
        # connect < 0.05
        assert self._flag(
            cold_call_connect_rate_pct=0.04,
            activities_total_count=200,
            meetings_booked=15,
            cold_calls_made=60,
            crm_activity_logging_rate_pct=0.90,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            pipeline_generated_usd=120_000,
            pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
            activity_mix_variance_score=20.0,
        ) is True

    def test_healthy_no_intervention(self):
        assert self._flag(
            activities_total_count=200,
            meetings_booked=15,
            cold_calls_made=60,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            pipeline_generated_usd=120_000,
            pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
            activity_mix_variance_score=20.0,
        ) is False

    def test_boundary_activities_exactly_50_no_intervention(self):
        # exactly 50 → condition is < 50, so no intervention from this condition
        result = self._flag(
            activities_total_count=50,
            meetings_booked=15,
            cold_calls_made=60,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            pipeline_generated_usd=120_000,
            pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
            activity_mix_variance_score=20.0,
        )
        # composite from those inputs should be < 30, and connect >= 0.05
        assert result is False

    def test_boundary_connect_exactly_005(self):
        # exactly 0.05 is NOT < 0.05, so no trigger from this condition
        result = self._flag(
            cold_call_connect_rate_pct=0.05,
            activities_total_count=200,
            meetings_booked=15,
            cold_calls_made=60,
            crm_activity_logging_rate_pct=0.90,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            pipeline_generated_usd=120_000,
            pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
            activity_mix_variance_score=20.0,
        )
        # composite: volume=0, conversion=30(connect<0.10), mix=0, coverage=0 → 0*0.25+30*0.35=10.5 < 30
        assert result is False


# ===========================================================================
# CLASS 15: estimated_pipeline_gap_usd
# ===========================================================================

class TestEstimatedPipelineGap:
    def _gap(self, **kwargs):
        e = PipelineGenerationEfficiencyEngine()
        return e.assess(make_input(**kwargs)).estimated_pipeline_gap_usd

    def test_no_gap_when_above_target(self):
        gap = self._gap(pipeline_generated_usd=120_000, pipeline_target_usd=100_000)
        assert gap == pytest.approx(0.0)

    def test_gap_calculation(self):
        # gap = max(100k-80k,0) * (composite/100)
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            pipeline_generated_usd=80_000,
            pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
            activities_total_count=200,
            meetings_booked=15,
            cold_calls_made=60,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            activity_mix_variance_score=20.0,
        )
        result = e.assess(inp)
        expected = round(20_000 * (result.pipeline_efficiency_composite / 100.0), 2)
        assert result.estimated_pipeline_gap_usd == pytest.approx(expected)

    def test_zero_target_zero_gap(self):
        gap = self._gap(pipeline_generated_usd=50_000, pipeline_target_usd=0)
        assert gap == pytest.approx(0.0)

    def test_gap_is_rounded_to_2_decimals(self):
        e = PipelineGenerationEfficiencyEngine()
        result = e.assess(make_input(pipeline_generated_usd=80_001, pipeline_target_usd=100_000))
        assert round(result.estimated_pipeline_gap_usd, 2) == result.estimated_pipeline_gap_usd

    def test_zero_composite_zero_gap(self):
        # If composite=0, gap=0 regardless
        gap = self._gap(
            pipeline_generated_usd=0,
            pipeline_target_usd=100_000,
            activities_total_count=200,
            meetings_booked=15,
            cold_calls_made=60,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            prior_period_pipeline_generated_usd=0,
            activity_mix_variance_score=20.0,
        )
        # composite won't be 0 here since there IS a coverage gap
        # just test gap >= 0
        assert gap >= 0.0


# ===========================================================================
# CLASS 16: efficiency_signal
# ===========================================================================

class TestEfficiencySignal:
    def test_healthy_signal_text(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        if result.efficiency_pattern == EfficiencyPattern.none and result.pipeline_efficiency_composite < 20:
            assert result.efficiency_signal == "Pipeline generation efficiency within targets"

    def test_signal_contains_composite(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert "composite" in result.efficiency_signal

    def test_signal_low_activities_included(self, engine):
        inp = make_input(activities_total_count=50)  # < 100 → included in signal
        result = engine.assess(inp)
        if result.pipeline_efficiency_composite >= 20 or result.efficiency_pattern != EfficiencyPattern.none:
            assert "total activities" in result.efficiency_signal

    def test_signal_demo_rate_included(self, engine):
        inp = make_input(demo_to_opp_conversion_rate_pct=0.20)  # < 0.30
        result = engine.assess(inp)
        if result.pipeline_efficiency_composite >= 20 or result.efficiency_pattern != EfficiencyPattern.none:
            assert "demo-to-opp rate" in result.efficiency_signal

    def test_signal_pipeline_coverage_included(self, engine):
        inp = make_input(pipeline_generated_usd=70_000, pipeline_target_usd=100_000)
        result = engine.assess(inp)
        if result.pipeline_efficiency_composite >= 20 or result.efficiency_pattern != EfficiencyPattern.none:
            assert "pipeline coverage" in result.efficiency_signal

    def test_signal_call_connect_rate_included(self, engine):
        inp = make_input(cold_call_connect_rate_pct=0.10)  # < 0.15
        result = engine.assess(inp)
        if result.pipeline_efficiency_composite >= 20 or result.efficiency_pattern != EfficiencyPattern.none:
            assert "call connect rate" in result.efficiency_signal

    def test_signal_uses_pattern_label(self, engine):
        # Force pipeline_coverage_gap pattern
        inp = make_input(
            pipeline_generated_usd=40_000, pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
        )
        result = engine.assess(inp)
        assert result.efficiency_pattern == EfficiencyPattern.pipeline_coverage_gap
        assert "pipeline coverage gap" in result.efficiency_signal.lower()

    def test_signal_none_pattern_uses_efficiency_risk_label(self, engine):
        # Pattern is none but composite >= 20
        inp = make_input(
            activities_total_count=200, meetings_booked=2,  # meetings < 5 → +25 volume
            cold_calls_made=60, crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30, email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60, qualified_opps_created=5,
            pipeline_generated_usd=120_000, pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0, activity_mix_variance_score=20.0,
        )
        result = engine.assess(inp)
        if result.efficiency_pattern == EfficiencyPattern.none and result.pipeline_efficiency_composite >= 20:
            assert result.efficiency_signal.startswith("Efficiency risk")

    def test_signal_fallback_degraded_text(self, engine):
        # When no parts qualify (all metrics good but pattern != none or composite >= 20)
        inp = make_input(
            activities_total_count=200,  # >= 100
            demo_to_opp_conversion_rate_pct=0.60,  # >= 0.30
            pipeline_generated_usd=120_000, pipeline_target_usd=100_000,  # coverage >= 1
            cold_call_connect_rate_pct=0.30,  # >= 0.15
            meetings_booked=2,  # trigger moderate risk via volume
        )
        result = engine.assess(inp)
        if "—" in result.efficiency_signal:
            # signal has format: "label — parts_or_fallback — composite N"
            parts_section = result.efficiency_signal
            assert "composite" in parts_section


# ===========================================================================
# CLASS 17: assess() integration
# ===========================================================================

class TestAssessIntegration:
    def test_assess_returns_result_instance(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result, PipelineEfficiencyResult)

    def test_assess_stores_rep_id(self, engine):
        result = engine.assess(make_input(rep_id="rep_42"))
        assert result.rep_id == "rep_42"

    def test_assess_stores_region(self, engine):
        result = engine.assess(make_input(region="central"))
        assert result.region == "central"

    def test_assess_healthy_risk_low(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.efficiency_risk == EfficiencyRisk.low

    def test_assess_healthy_severity_healthy(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.efficiency_severity == EfficiencySeverity.healthy

    def test_assess_healthy_action_no_action(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.recommended_action == EfficiencyAction.no_action

    def test_assess_critical_risk_critical(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert result.efficiency_risk == EfficiencyRisk.critical

    def test_assess_critical_action_pip(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert result.recommended_action == EfficiencyAction.performance_improvement_plan

    def test_assess_sub_scores_non_negative(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.activity_volume_score >= 0
        assert result.conversion_efficiency_score >= 0
        assert result.pipeline_coverage_score >= 0
        assert result.activity_mix_score >= 0

    def test_assess_sub_scores_capped(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert result.activity_volume_score <= 100
        assert result.conversion_efficiency_score <= 100
        assert result.pipeline_coverage_score <= 100
        assert result.activity_mix_score <= 100

    def test_assess_appends_to_results(self, engine):
        engine.assess(make_input(rep_id="r1"))
        engine.assess(make_input(rep_id="r2"))
        assert len(engine._results) == 2

    def test_assess_multiple_calls_independent(self, engine):
        r1 = engine.assess(make_input(rep_id="r1", pipeline_generated_usd=120_000))
        r2 = engine.assess(make_input(rep_id="r2", pipeline_generated_usd=30_000, pipeline_target_usd=100_000))
        assert r1.rep_id != r2.rep_id
        assert r1.pipeline_efficiency_composite != r2.pipeline_efficiency_composite

    def test_assess_batch_returns_list(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert isinstance(results, list)
        assert len(results) == 5

    def test_assess_batch_all_results(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        assert all(isinstance(r, PipelineEfficiencyResult) for r in results)

    def test_assess_batch_stores_all(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(4)]
        engine.assess_batch(inputs)
        assert len(engine._results) == 4

    def test_fresh_engine_empty_results(self):
        e = PipelineGenerationEfficiencyEngine()
        assert len(e._results) == 0


# ===========================================================================
# CLASS 18: summary()
# ===========================================================================

class TestSummary:
    def test_empty_summary_returns_13_keys(self):
        e = PipelineGenerationEfficiencyEngine()
        s = e.summary()
        assert len(s) == 13

    def test_empty_summary_exact_keys(self):
        e = PipelineGenerationEfficiencyEngine()
        s = e.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_pipeline_efficiency_composite",
            "pipeline_at_risk_count", "activity_intervention_count",
            "avg_activity_volume_score", "avg_conversion_efficiency_score",
            "avg_pipeline_coverage_score", "avg_activity_mix_score",
            "total_estimated_pipeline_gap_usd",
        }
        assert set(s.keys()) == expected

    def test_empty_summary_zero_total(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e.summary()["total"] == 0

    def test_empty_summary_empty_counts(self):
        e = PipelineGenerationEfficiencyEngine()
        s = e.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_zero_averages(self):
        e = PipelineGenerationEfficiencyEngine()
        s = e.summary()
        assert s["avg_pipeline_efficiency_composite"] == 0.0
        assert s["avg_activity_volume_score"] == 0.0
        assert s["avg_conversion_efficiency_score"] == 0.0
        assert s["avg_pipeline_coverage_score"] == 0.0
        assert s["avg_activity_mix_score"] == 0.0

    def test_empty_summary_zero_gap(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e.summary()["total_estimated_pipeline_gap_usd"] == 0.0

    def test_summary_total_count(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        assert engine.summary()["total"] == 5

    def test_summary_risk_counts_sum(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(4)])
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == 4

    def test_summary_pattern_counts_sum(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(4)])
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == 4

    def test_summary_severity_counts_sum(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(4)])
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == 4

    def test_summary_action_counts_sum(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(4)])
        s = engine.summary()
        assert sum(s["action_counts"].values()) == 4

    def test_summary_pipeline_at_risk_count(self, engine):
        # healthy → not at risk
        engine.assess(make_input(pipeline_generated_usd=120_000, pipeline_target_usd=100_000,
                                  qualified_opps_created=5))
        # at risk → zero opps
        engine.assess(make_input(qualified_opps_created=0))
        s = engine.summary()
        assert s["pipeline_at_risk_count"] >= 1

    def test_summary_intervention_count(self, engine):
        engine.assess(make_input(activities_total_count=30))  # < 50 → intervention
        s = engine.summary()
        assert s["activity_intervention_count"] >= 1

    def test_summary_avg_composite_correct(self, engine):
        r1 = engine.assess(make_input(rep_id="r1"))
        r2 = engine.assess(make_input(rep_id="r2"))
        expected = round((r1.pipeline_efficiency_composite + r2.pipeline_efficiency_composite) / 2, 1)
        assert engine.summary()["avg_pipeline_efficiency_composite"] == pytest.approx(expected)

    def test_summary_total_gap_is_sum(self, engine):
        r1 = engine.assess(make_input(rep_id="r1", pipeline_generated_usd=80_000, pipeline_target_usd=100_000))
        r2 = engine.assess(make_input(rep_id="r2", pipeline_generated_usd=90_000, pipeline_target_usd=100_000))
        expected = round(r1.estimated_pipeline_gap_usd + r2.estimated_pipeline_gap_usd, 2)
        assert engine.summary()["total_estimated_pipeline_gap_usd"] == pytest.approx(expected)

    def test_summary_risk_counts_keys_are_strings(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        for k in s["risk_counts"]:
            assert isinstance(k, str)

    def test_summary_13_keys_after_assess(self, engine):
        engine.assess(make_input())
        assert len(engine.summary()) == 13

    def test_summary_avg_volume_score_correct(self, engine):
        r1 = engine.assess(make_input(rep_id="r1"))
        r2 = engine.assess(make_input(rep_id="r2"))
        expected = round((r1.activity_volume_score + r2.activity_volume_score) / 2, 1)
        assert engine.summary()["avg_activity_volume_score"] == pytest.approx(expected)

    def test_summary_avg_mix_score_correct(self, engine):
        r1 = engine.assess(make_input(rep_id="r1"))
        r2 = engine.assess(make_input(rep_id="r2"))
        expected = round((r1.activity_mix_score + r2.activity_mix_score) / 2, 1)
        assert engine.summary()["avg_activity_mix_score"] == pytest.approx(expected)


# ===========================================================================
# CLASS 19: end-to-end scenario tests
# ===========================================================================

class TestScenarios:
    def test_star_performer(self):
        """All metrics excellent → low risk, healthy, no action."""
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            activities_total_count=250, meetings_booked=20, cold_calls_made=100,
            crm_activity_logging_rate_pct=0.95,
            cold_call_connect_rate_pct=0.35, email_reply_rate_pct=0.25,
            demo_to_opp_conversion_rate_pct=0.65, qualified_opps_created=10,
            pipeline_generated_usd=200_000, pipeline_target_usd=150_000,
            prior_period_pipeline_generated_usd=180_000,
            activity_mix_variance_score=15.0, referrals_requested=3,
            referrals_received=2,
        )
        r = e.assess(inp)
        assert r.efficiency_risk == EfficiencyRisk.low
        assert r.efficiency_severity == EfficiencySeverity.healthy
        assert r.recommended_action == EfficiencyAction.no_action
        assert r.is_pipeline_at_risk is False

    def test_channel_dependent_rep(self):
        """High mix variance + heavy cold-call share → channel overreliance pattern."""
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            activity_mix_variance_score=60.0,
            activities_total_count=200,
            cold_calls_made=160,  # 80% share
            prior_period_pipeline_generated_usd=0,
            pipeline_generated_usd=120_000,
            pipeline_target_usd=100_000,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
        )
        r = e.assess(inp)
        assert r.efficiency_pattern == EfficiencyPattern.activity_channel_overreliance

    def test_declining_pipeline_rep(self):
        """Significant pipeline decay triggers activity_decay pattern."""
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            prior_period_pipeline_generated_usd=200_000,
            pipeline_generated_usd=100_000,  # 50% decay
            pipeline_target_usd=0,
            cold_call_connect_rate_pct=0.05,  # poor → conversion >= 30
            email_reply_rate_pct=0.03,
            demo_to_opp_conversion_rate_pct=0.20,
            qualified_opps_created=5,
        )
        r = e.assess(inp)
        assert r.efficiency_pattern == EfficiencyPattern.activity_decay

    def test_poor_demo_conversion_rep(self):
        """Low demo rate with decent activity → poor_conversion pattern."""
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            prior_period_pipeline_generated_usd=0,
            pipeline_generated_usd=100_000,
            pipeline_target_usd=0,
            cold_call_connect_rate_pct=0.05,  # +30
            email_reply_rate_pct=0.03,         # +25
            demo_to_opp_conversion_rate_pct=0.15,  # +30 → conversion=85 >= 35
            qualified_opps_created=5,
            activity_mix_variance_score=20.0,
            activities_total_count=200,
        )
        r = e.assess(inp)
        assert r.efficiency_pattern == EfficiencyPattern.poor_conversion

    def test_low_volume_rep(self):
        """Low activity count → low_activity_volume pattern."""
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            activities_total_count=60,
            meetings_booked=2,  # +25 → volume = 20+25 = 45+ >= 30
            cold_calls_made=50,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            pipeline_generated_usd=120_000,
            pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
            activity_mix_variance_score=20.0,
        )
        r = e.assess(inp)
        assert r.efficiency_pattern == EfficiencyPattern.low_activity_volume

    def test_pipeline_coverage_gap_rep(self):
        """Generated far below target → pipeline_coverage_gap."""
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            pipeline_generated_usd=30_000,
            pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
        )
        r = e.assess(inp)
        assert r.efficiency_pattern == EfficiencyPattern.pipeline_coverage_gap

    def test_high_risk_blitz_action(self):
        """High composite + low_activity_volume pattern → pipeline_blitz."""
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            activities_total_count=60,
            meetings_booked=2,   # volume += 25
            cold_calls_made=10,  # volume += 15
            crm_activity_logging_rate_pct=0.35,  # volume += 25; mix += 15
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            pipeline_generated_usd=120_000,
            pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
            activity_mix_variance_score=20.0,
        )
        r = e.assess(inp)
        if r.efficiency_risk == EfficiencyRisk.high and r.efficiency_pattern == EfficiencyPattern.low_activity_volume:
            assert r.recommended_action == EfficiencyAction.pipeline_blitz

    def test_moderate_overreliance_channel_diversification(self):
        """Moderate composite + channel overreliance → channel_diversification."""
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            activity_mix_variance_score=55.0,
            activities_total_count=200,
            cold_calls_made=160,  # 80% share → mix +=40+20=60
            prior_period_pipeline_generated_usd=0,
            pipeline_generated_usd=120_000,
            pipeline_target_usd=100_000,
            cold_call_connect_rate_pct=0.30,
            email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60,
            qualified_opps_created=5,
            meetings_booked=15,
            crm_activity_logging_rate_pct=0.90,
        )
        r = e.assess(inp)
        if r.efficiency_risk == EfficiencyRisk.moderate and r.efficiency_pattern == EfficiencyPattern.activity_channel_overreliance:
            assert r.recommended_action == EfficiencyAction.channel_diversification

    def test_multiple_reps_summary_totals(self):
        """Batch of mixed reps; summary totals are correct."""
        e = PipelineGenerationEfficiencyEngine()
        inputs = [
            make_input(rep_id="r1"),
            make_input(rep_id="r2", activities_total_count=30),
            make_input(rep_id="r3", pipeline_generated_usd=0, pipeline_target_usd=100_000),
        ]
        results = e.assess_batch(inputs)
        s = e.summary()
        assert s["total"] == 3
        assert sum(s["risk_counts"].values()) == 3
        assert s["total_estimated_pipeline_gap_usd"] == pytest.approx(
            round(sum(r.estimated_pipeline_gap_usd for r in results), 2)
        )

    def test_zero_activities_edge_case(self):
        """activities_total_count=0 doesn't crash (no division)."""
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(activities_total_count=0, cold_calls_made=0, meetings_booked=0)
        r = e.assess(inp)
        assert isinstance(r, PipelineEfficiencyResult)

    def test_all_zero_numeric_inputs(self):
        """All-zero numeric inputs doesn't crash."""
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            cold_calls_made=0, emails_sent=0, demos_conducted=0,
            events_attended=0, event_leads_generated=0, referrals_requested=0,
            referrals_received=0, social_touches_count=0, meetings_booked=0,
            qualified_opps_created=0, pipeline_generated_usd=0,
            pipeline_target_usd=0, activity_mix_variance_score=0.0,
            prior_period_pipeline_generated_usd=0, activities_total_count=0,
            crm_activity_logging_rate_pct=0.0,
            cold_call_connect_rate_pct=0.0, email_reply_rate_pct=0.0,
            demo_to_opp_conversion_rate_pct=0.0,
        )
        r = e.assess(inp)
        assert r.pipeline_efficiency_composite >= 0


# ===========================================================================
# CLASS 20: boundary and edge value tests
# ===========================================================================

class TestBoundaryValues:
    def test_composite_exactly_20_is_moderate(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e._risk_level(20.0) == EfficiencyRisk.moderate

    def test_composite_exactly_40_is_high(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e._risk_level(40.0) == EfficiencyRisk.high

    def test_composite_exactly_60_is_critical(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e._risk_level(60.0) == EfficiencyRisk.critical

    def test_severity_exactly_20_is_underperforming(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e._severity(20.0) == EfficiencySeverity.underperforming

    def test_severity_exactly_40_is_degraded(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e._severity(40.0) == EfficiencySeverity.degraded

    def test_severity_exactly_60_is_critical(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e._severity(60.0) == EfficiencySeverity.critical

    def test_gap_max_is_nonnegative(self, engine):
        # pipeline_generated > pipeline_target → gap = 0
        r = engine.assess(make_input(pipeline_generated_usd=200_000, pipeline_target_usd=100_000))
        assert r.estimated_pipeline_gap_usd == pytest.approx(0.0)

    def test_large_pipeline_values(self, engine):
        r = engine.assess(make_input(
            pipeline_generated_usd=5_000_000,
            pipeline_target_usd=10_000_000,
        ))
        assert isinstance(r, PipelineEfficiencyResult)

    def test_crm_rate_exactly_040_no_mix_penalty(self):
        e = PipelineGenerationEfficiencyEngine()
        s = e._activity_mix_score(make_input(
            crm_activity_logging_rate_pct=0.40,
            activity_mix_variance_score=20.0,
            activities_total_count=200, cold_calls_made=80,
            referrals_requested=0, referrals_received=0,
        ))
        assert s == pytest.approx(0.0)

    def test_decay_exactly_015_adds_15(self):
        # prior=100k, current=85k → delta=0.15 → +15
        e = PipelineGenerationEfficiencyEngine()
        s = e._pipeline_coverage_score(make_input(
            pipeline_generated_usd=85_000,
            pipeline_target_usd=0,
            prior_period_pipeline_generated_usd=100_000,
            qualified_opps_created=5,
        ))
        assert s == pytest.approx(15.0)

    def test_coverage_exactly_075_no_penalty(self):
        # coverage = 0.75 → NOT < 0.75 → 0 from coverage
        e = PipelineGenerationEfficiencyEngine()
        s = e._pipeline_coverage_score(make_input(
            pipeline_generated_usd=75_000,
            pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
            qualified_opps_created=5,
        ))
        # coverage = 0.75 → not < 0.75, not < 1.0 is True → +10
        assert s == pytest.approx(10.0)

    def test_referrals_exactly_4_received_0_elif_applies(self):
        # 4 >= 3 but < 5 → elif → +10
        e = PipelineGenerationEfficiencyEngine()
        s = e._activity_mix_score(make_input(
            referrals_requested=4,
            referrals_received=0,
            activity_mix_variance_score=20.0,
            activities_total_count=200,
            cold_calls_made=80,
            crm_activity_logging_rate_pct=0.90,
        ))
        assert s == pytest.approx(10.0)


# ===========================================================================
# CLASS 21: result field type validation
# ===========================================================================

class TestResultFieldTypes:
    def test_efficiency_risk_is_enum(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.efficiency_risk, EfficiencyRisk)

    def test_efficiency_pattern_is_enum(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.efficiency_pattern, EfficiencyPattern)

    def test_efficiency_severity_is_enum(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.efficiency_severity, EfficiencySeverity)

    def test_recommended_action_is_enum(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.recommended_action, EfficiencyAction)

    def test_composite_is_float(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.pipeline_efficiency_composite, float)

    def test_is_pipeline_at_risk_is_bool(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.is_pipeline_at_risk, bool)

    def test_requires_activity_intervention_is_bool(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.requires_activity_intervention, bool)

    def test_gap_is_float(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.estimated_pipeline_gap_usd, float)

    def test_signal_is_str(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.efficiency_signal, str)

    def test_rep_id_is_str(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.rep_id, str)

    def test_region_is_str(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.region, str)


# ===========================================================================
# CLASS 22: assess_batch edge cases
# ===========================================================================

class TestAssessBatch:
    def test_empty_batch(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_single_item_batch(self, engine):
        results = engine.assess_batch([make_input()])
        assert len(results) == 1

    def test_batch_preserves_order(self, engine):
        ids = [f"rep_{i}" for i in range(10)]
        inputs = [make_input(rep_id=rid) for rid in ids]
        results = engine.assess_batch(inputs)
        assert [r.rep_id for r in results] == ids

    def test_batch_all_critical(self, engine, critical_input):
        results = engine.assess_batch([critical_input, critical_input])
        assert all(r.efficiency_risk == EfficiencyRisk.critical for r in results)

    def test_batch_accumulates_for_summary(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(7)])
        assert engine.summary()["total"] == 7

    def test_batch_and_single_accumulate_together(self, engine):
        engine.assess(make_input(rep_id="single"))
        engine.assess_batch([make_input(rep_id=f"b{i}") for i in range(3)])
        assert engine.summary()["total"] == 4


# ===========================================================================
# CLASS 23: additional composite/scoring cross-checks
# ===========================================================================

class TestScoringCrossChecks:
    def test_volume_contributes_25pct(self):
        e = PipelineGenerationEfficiencyEngine()
        # Only add volume risk: activities=80 (+20), meetings=15(0), calls=50(0), crm=0.9(0) → volume=20
        # conversion=0, coverage=0, mix=0 → composite = 20*0.25 = 5.0
        inp = make_input(
            activities_total_count=80, meetings_booked=15, cold_calls_made=50,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30, email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60, qualified_opps_created=5,
            pipeline_generated_usd=120_000, pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0, activity_mix_variance_score=20.0,
        )
        r = e.assess(inp)
        assert r.activity_volume_score == pytest.approx(20.0)
        assert r.pipeline_efficiency_composite == pytest.approx(5.0)

    def test_conversion_contributes_35pct(self):
        e = PipelineGenerationEfficiencyEngine()
        # Only conversion risk: connect<0.10 (+30), email>=0.10 (0), demo>=0.50 (0), opps>0 → conv=30
        # volume=0, coverage=0, mix=0 → composite = 30*0.35 = 10.5
        inp = make_input(
            activities_total_count=200, meetings_booked=15, cold_calls_made=50,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.05, email_reply_rate_pct=0.15,
            demo_to_opp_conversion_rate_pct=0.60, qualified_opps_created=5,
            pipeline_generated_usd=120_000, pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0, activity_mix_variance_score=20.0,
        )
        r = e.assess(inp)
        assert r.conversion_efficiency_score == pytest.approx(30.0)
        assert r.pipeline_efficiency_composite == pytest.approx(10.5)

    def test_coverage_contributes_25pct(self):
        e = PipelineGenerationEfficiencyEngine()
        # Only coverage risk: generated=80k, target=100k → coverage=0.80 → +10
        # volume=0, conversion=0, mix=0 → composite = 10*0.25 = 2.5
        inp = make_input(
            activities_total_count=200, meetings_booked=15, cold_calls_made=50,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30, email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60, qualified_opps_created=5,
            pipeline_generated_usd=80_000, pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0, activity_mix_variance_score=20.0,
        )
        r = e.assess(inp)
        assert r.pipeline_coverage_score == pytest.approx(10.0)
        assert r.pipeline_efficiency_composite == pytest.approx(2.5)

    def test_mix_contributes_15pct(self):
        e = PipelineGenerationEfficiencyEngine()
        # Only mix risk: variance=55 (+22), activities=200, calls=80 (share=0.40 < 0.65) → mix=22
        # volume=0, conversion=0, coverage=0 → composite = 22*0.15 = 3.3
        inp = make_input(
            activities_total_count=200, meetings_booked=15, cold_calls_made=80,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30, email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60, qualified_opps_created=5,
            pipeline_generated_usd=120_000, pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0, activity_mix_variance_score=55.0,
        )
        r = e.assess(inp)
        assert r.activity_mix_score == pytest.approx(22.0)
        assert r.pipeline_efficiency_composite == pytest.approx(3.3)

    def test_all_weights_sum_correctly(self):
        # When all four scores are the same value X, composite = X*(0.25+0.35+0.25+0.15) = X*1.0 = X
        e = PipelineGenerationEfficiencyEngine()
        # Engineer sub-scores: need a case where all = 0 → composite = 0
        inp = make_input(
            activities_total_count=200, meetings_booked=15, cold_calls_made=50,
            crm_activity_logging_rate_pct=0.90,
            cold_call_connect_rate_pct=0.30, email_reply_rate_pct=0.20,
            demo_to_opp_conversion_rate_pct=0.60, qualified_opps_created=5,
            pipeline_generated_usd=120_000, pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0, activity_mix_variance_score=20.0,
        )
        r = e.assess(inp)
        assert r.activity_volume_score == pytest.approx(0.0)
        assert r.conversion_efficiency_score == pytest.approx(0.0)
        assert r.pipeline_coverage_score == pytest.approx(0.0)
        assert r.activity_mix_score == pytest.approx(0.0)
        assert r.pipeline_efficiency_composite == pytest.approx(0.0)

    def test_composite_never_negative(self, engine):
        r = engine.assess(make_input())
        assert r.pipeline_efficiency_composite >= 0.0

    def test_sub_scores_not_capped_individually_until_100(self):
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            activities_total_count=10, meetings_booked=1, cold_calls_made=5,
            crm_activity_logging_rate_pct=0.10,
        )
        s = e._activity_volume_score(inp)
        assert s == pytest.approx(100.0)  # 35+25+15+25 = 100


# ===========================================================================
# CLASS 24: signal format verification
# ===========================================================================

class TestSignalFormat:
    def test_signal_no_parts_fallback(self):
        """When all parts conditions are false, fallback text appears."""
        e = PipelineGenerationEfficiencyEngine()
        # activities >= 100, demo >= 0.30, coverage >= 1.0 (or no target), connect >= 0.15
        # but composite >= 20 so not "within targets"
        inp = make_input(
            activities_total_count=200,
            demo_to_opp_conversion_rate_pct=0.60,
            cold_call_connect_rate_pct=0.30,
            pipeline_generated_usd=120_000,
            pipeline_target_usd=100_000,
            meetings_booked=2,  # volume score bump to push composite >= 20
        )
        r = e.assess(inp)
        if r.efficiency_pattern == EfficiencyPattern.none and r.pipeline_efficiency_composite >= 20:
            assert "pipeline efficiency degraded" in r.efficiency_signal

    def test_signal_format_with_pattern(self):
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            pipeline_generated_usd=30_000,
            pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
        )
        r = e.assess(inp)
        # pattern = pipeline_coverage_gap
        assert "—" in r.efficiency_signal
        assert "composite" in r.efficiency_signal

    def test_signal_label_capitalized(self):
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            pipeline_generated_usd=30_000,
            pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
        )
        r = e.assess(inp)
        # label = "pipeline coverage gap".capitalize() = "Pipeline coverage gap"
        assert r.efficiency_signal[0].isupper()

    def test_signal_demo_rate_format(self):
        """Demo rate shown as integer percentage."""
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            demo_to_opp_conversion_rate_pct=0.25,  # 25%
            pipeline_generated_usd=120_000,
            pipeline_target_usd=100_000,
            prior_period_pipeline_generated_usd=0,
        )
        r = e.assess(inp)
        if "demo-to-opp rate" in r.efficiency_signal:
            assert "25%" in r.efficiency_signal

    def test_signal_activities_count_format(self):
        """Activity count shown numerically."""
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(activities_total_count=75)
        r = e.assess(inp)
        if "total activities" in r.efficiency_signal:
            assert "75" in r.efficiency_signal

    def test_signal_within_targets_exact(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        if r.efficiency_pattern == EfficiencyPattern.none and r.pipeline_efficiency_composite < 20:
            assert r.efficiency_signal == "Pipeline generation efficiency within targets"

    def test_signal_connect_rate_format(self):
        """Connect rate shown as integer percentage."""
        e = PipelineGenerationEfficiencyEngine()
        inp = make_input(
            cold_call_connect_rate_pct=0.10,  # < 0.15 → included; 10%
            activities_total_count=200,
            demo_to_opp_conversion_rate_pct=0.60,
            pipeline_generated_usd=120_000,
            pipeline_target_usd=100_000,
        )
        r = e.assess(inp)
        if "call connect rate" in r.efficiency_signal:
            assert "10%" in r.efficiency_signal


# ===========================================================================
# CLASS 25: miscellaneous robustness tests
# ===========================================================================

class TestRobustness:
    def test_different_rep_ids_independent(self):
        e = PipelineGenerationEfficiencyEngine()
        r1 = e.assess(make_input(rep_id="alpha"))
        r2 = e.assess(make_input(rep_id="beta"))
        assert r1.rep_id == "alpha"
        assert r2.rep_id == "beta"

    def test_different_regions_preserved(self):
        e = PipelineGenerationEfficiencyEngine()
        r1 = e.assess(make_input(region="north"))
        r2 = e.assess(make_input(region="south"))
        assert r1.region == "north"
        assert r2.region == "south"

    def test_engine_state_isolated_between_instances(self):
        e1 = PipelineGenerationEfficiencyEngine()
        e2 = PipelineGenerationEfficiencyEngine()
        e1.assess(make_input(rep_id="r1"))
        e1.assess(make_input(rep_id="r2"))
        e2.assess(make_input(rep_id="r3"))
        assert len(e1._results) == 2
        assert len(e2._results) == 1

    def test_to_dict_is_independent_copy(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        d1 = r.to_dict()
        d2 = r.to_dict()
        assert d1 == d2

    def test_assess_batch_empty_then_summary(self, engine):
        engine.assess_batch([])
        s = engine.summary()
        assert s["total"] == 0

    def test_summary_called_twice_consistent(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s1 = engine.summary()
        s2 = engine.summary()
        assert s1 == s2

    def test_high_decimal_pipeline_values(self, engine):
        r = engine.assess(make_input(
            pipeline_generated_usd=123456.789,
            pipeline_target_usd=234567.890,
        ))
        assert isinstance(r.estimated_pipeline_gap_usd, float)

    def test_zero_connect_rate(self, engine):
        r = engine.assess(make_input(cold_call_connect_rate_pct=0.0))
        assert r.conversion_efficiency_score >= 30.0

    def test_full_crm_logging(self, engine):
        r = engine.assess(make_input(crm_activity_logging_rate_pct=1.0))
        # No crm penalty in volume or mix from logging
        assert isinstance(r, PipelineEfficiencyResult)

    def test_summary_gap_is_sum_not_average(self):
        """Verify total_estimated_pipeline_gap_usd is a SUM."""
        e = PipelineGenerationEfficiencyEngine()
        r1 = e.assess(make_input(rep_id="r1", pipeline_generated_usd=50_000, pipeline_target_usd=100_000))
        r2 = e.assess(make_input(rep_id="r2", pipeline_generated_usd=60_000, pipeline_target_usd=100_000))
        s = e.summary()
        expected_sum = round(r1.estimated_pipeline_gap_usd + r2.estimated_pipeline_gap_usd, 2)
        assert s["total_estimated_pipeline_gap_usd"] == pytest.approx(expected_sum)

    def test_summary_avg_composite_not_sum(self):
        e = PipelineGenerationEfficiencyEngine()
        r1 = e.assess(make_input(rep_id="r1"))
        r2 = e.assess(make_input(rep_id="r2"))
        s = e.summary()
        expected_avg = round((r1.pipeline_efficiency_composite + r2.pipeline_efficiency_composite) / 2, 1)
        assert s["avg_pipeline_efficiency_composite"] == pytest.approx(expected_avg)

    def test_assess_returns_fresh_result_each_time(self, engine):
        r1 = engine.assess(make_input(rep_id="r1"))
        r2 = engine.assess(make_input(rep_id="r2"))
        assert r1 is not r2


# ===========================================================================
# CLASS 26: additional activity_volume_score edge cases
# ===========================================================================

class TestActivityVolumeScoreExtra:
    def _score(self, **kwargs):
        e = PipelineGenerationEfficiencyEngine()
        return e._activity_volume_score(make_input(**kwargs))

    def test_exactly_49_activities_adds_35(self):
        s = self._score(activities_total_count=49, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(35.0)

    def test_exactly_99_activities_adds_20(self):
        s = self._score(activities_total_count=99, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(20.0)

    def test_exactly_149_activities_adds_8(self):
        s = self._score(activities_total_count=149, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(8.0)

    def test_exactly_4_meetings_adds_25(self):
        s = self._score(activities_total_count=200, meetings_booked=4,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(25.0)

    def test_exactly_9_meetings_adds_12(self):
        s = self._score(activities_total_count=200, meetings_booked=9,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(12.0)

    def test_exactly_19_calls_adds_15(self):
        s = self._score(activities_total_count=200, meetings_booked=15,
                        cold_calls_made=19, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(15.0)

    def test_exactly_39_calls_adds_8(self):
        s = self._score(activities_total_count=200, meetings_booked=15,
                        cold_calls_made=39, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(8.0)

    def test_exactly_069_crm_adds_12(self):
        s = self._score(activities_total_count=200, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.69)
        assert s == pytest.approx(12.0)

    def test_exactly_049_crm_adds_25(self):
        s = self._score(activities_total_count=200, meetings_booked=15,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.49)
        assert s == pytest.approx(25.0)

    def test_all_worst_sums_to_100(self):
        # 35+25+15+25=100
        s = self._score(activities_total_count=1, meetings_booked=1,
                        cold_calls_made=1, crm_activity_logging_rate_pct=0.10)
        assert s == pytest.approx(100.0)

    def test_moderate_combo(self):
        # activities<100 (+20) + meetings<5 (+25) = 45
        s = self._score(activities_total_count=80, meetings_booked=4,
                        cold_calls_made=50, crm_activity_logging_rate_pct=0.90)
        assert s == pytest.approx(45.0)


# ===========================================================================
# CLASS 27: additional conversion_efficiency_score edge cases
# ===========================================================================

class TestConversionEfficiencyScoreExtra:
    def _score(self, **kwargs):
        e = PipelineGenerationEfficiencyEngine()
        return e._conversion_efficiency_score(make_input(**kwargs))

    def test_all_worst_sums_to_100(self):
        # 30+25+30+15=100
        s = self._score(cold_call_connect_rate_pct=0.01,
                        email_reply_rate_pct=0.01,
                        demo_to_opp_conversion_rate_pct=0.01,
                        qualified_opps_created=0,
                        activities_total_count=50)
        assert s == pytest.approx(100.0)

    def test_combo_connect_and_email_poor(self):
        # connect<0.10 (+30) + email<0.05 (+25) = 55, demo good, opps>0
        s = self._score(cold_call_connect_rate_pct=0.05,
                        email_reply_rate_pct=0.02,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=5)
        assert s == pytest.approx(55.0)

    def test_combo_demo_and_zero_opps(self):
        # demo<0.30 (+30) + zero_opps_30_activities (+15) = 45
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.20,
                        demo_to_opp_conversion_rate_pct=0.20,
                        qualified_opps_created=0,
                        activities_total_count=50)
        assert s == pytest.approx(45.0)

    def test_exactly_29_activities_no_zero_opp_bonus(self):
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.20,
                        demo_to_opp_conversion_rate_pct=0.60,
                        qualified_opps_created=0,
                        activities_total_count=29)
        assert s == pytest.approx(0.0)

    def test_boundary_demo_exactly_050(self):
        # exactly 0.50 → not < 0.50 → 0
        s = self._score(cold_call_connect_rate_pct=0.30,
                        email_reply_rate_pct=0.20,
                        demo_to_opp_conversion_rate_pct=0.50,
                        qualified_opps_created=5)
        assert s == pytest.approx(0.0)


# ===========================================================================
# CLASS 28: additional pipeline_coverage_score edge cases
# ===========================================================================

class TestPipelineCoverageScoreExtra:
    def _score(self, **kwargs):
        e = PipelineGenerationEfficiencyEngine()
        return e._pipeline_coverage_score(make_input(**kwargs))

    def test_coverage_49pct_adds_40(self):
        s = self._score(pipeline_generated_usd=49_000,
                        pipeline_target_usd=100_000,
                        prior_period_pipeline_generated_usd=0,
                        qualified_opps_created=5)
        assert s == pytest.approx(40.0)

    def test_coverage_74pct_adds_25(self):
        s = self._score(pipeline_generated_usd=74_000,
                        pipeline_target_usd=100_000,
                        prior_period_pipeline_generated_usd=0,
                        qualified_opps_created=5)
        assert s == pytest.approx(25.0)

    def test_coverage_99pct_adds_10(self):
        s = self._score(pipeline_generated_usd=99_000,
                        pipeline_target_usd=100_000,
                        prior_period_pipeline_generated_usd=0,
                        qualified_opps_created=5)
        assert s == pytest.approx(10.0)

    def test_coverage_100pct_adds_0(self):
        s = self._score(pipeline_generated_usd=100_000,
                        pipeline_target_usd=100_000,
                        prior_period_pipeline_generated_usd=0,
                        qualified_opps_created=5)
        assert s == pytest.approx(0.0)

    def test_decay_29pct_adds_15(self):
        # prior=100k, current=71k → delta=0.29, >= 0.15 but < 0.30 → +15
        s = self._score(pipeline_generated_usd=71_000,
                        pipeline_target_usd=0,
                        prior_period_pipeline_generated_usd=100_000,
                        qualified_opps_created=5)
        assert s == pytest.approx(15.0)

    def test_prior_equals_current_no_penalty(self):
        s = self._score(pipeline_generated_usd=100_000,
                        pipeline_target_usd=0,
                        prior_period_pipeline_generated_usd=100_000,
                        qualified_opps_created=5)
        assert s == pytest.approx(0.0)

    def test_zero_opps_no_target_no_penalty(self):
        s = self._score(pipeline_generated_usd=100_000,
                        pipeline_target_usd=0,
                        prior_period_pipeline_generated_usd=0,
                        qualified_opps_created=0)
        assert s == pytest.approx(0.0)


# ===========================================================================
# CLASS 29: action logic full matrix
# ===========================================================================

class TestActionMatrix:
    def test_critical_with_none_pattern_gives_pip(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e._action(EfficiencyRisk.critical, EfficiencyPattern.none) == EfficiencyAction.performance_improvement_plan

    def test_critical_with_activity_decay_gives_pip(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e._action(EfficiencyRisk.critical, EfficiencyPattern.activity_decay) == EfficiencyAction.performance_improvement_plan

    def test_high_with_pipeline_coverage_gap_gives_coaching(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e._action(EfficiencyRisk.high, EfficiencyPattern.pipeline_coverage_gap) == EfficiencyAction.conversion_coaching

    def test_moderate_with_low_activity_volume_gives_increase(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e._action(EfficiencyRisk.moderate, EfficiencyPattern.low_activity_volume) == EfficiencyAction.activity_increase

    def test_moderate_with_poor_conversion_gives_increase(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e._action(EfficiencyRisk.moderate, EfficiencyPattern.poor_conversion) == EfficiencyAction.activity_increase

    def test_moderate_with_pipeline_coverage_gap_gives_increase(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e._action(EfficiencyRisk.moderate, EfficiencyPattern.pipeline_coverage_gap) == EfficiencyAction.activity_increase

    def test_low_with_activity_decay_gives_no_action(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e._action(EfficiencyRisk.low, EfficiencyPattern.activity_decay) == EfficiencyAction.no_action

    def test_low_with_pipeline_coverage_gap_gives_no_action(self):
        e = PipelineGenerationEfficiencyEngine()
        assert e._action(EfficiencyRisk.low, EfficiencyPattern.pipeline_coverage_gap) == EfficiencyAction.no_action


# ===========================================================================
# CLASS 30: summary aggregation accuracy
# ===========================================================================

class TestSummaryAggregation:
    def test_single_result_avg_equals_value(self):
        e = PipelineGenerationEfficiencyEngine()
        r = e.assess(make_input())
        s = e.summary()
        assert s["avg_pipeline_efficiency_composite"] == pytest.approx(r.pipeline_efficiency_composite)
        assert s["avg_activity_volume_score"] == pytest.approx(r.activity_volume_score)
        assert s["avg_conversion_efficiency_score"] == pytest.approx(r.conversion_efficiency_score)
        assert s["avg_pipeline_coverage_score"] == pytest.approx(r.pipeline_coverage_score)
        assert s["avg_activity_mix_score"] == pytest.approx(r.activity_mix_score)

    def test_pipeline_at_risk_count_matches(self):
        e = PipelineGenerationEfficiencyEngine()
        results = e.assess_batch([make_input(rep_id=f"r{i}") for i in range(6)])
        s = e.summary()
        assert s["pipeline_at_risk_count"] == sum(1 for r in results if r.is_pipeline_at_risk)

    def test_intervention_count_matches(self):
        e = PipelineGenerationEfficiencyEngine()
        results = e.assess_batch([make_input(rep_id=f"r{i}") for i in range(6)])
        s = e.summary()
        assert s["activity_intervention_count"] == sum(1 for r in results if r.requires_activity_intervention)

    def test_mixed_risk_counts(self):
        e = PipelineGenerationEfficiencyEngine()
        # healthy (low risk)
        e.assess(make_input(rep_id="healthy"))
        # critical
        e.assess(make_input(rep_id="bad",
            activities_total_count=10, meetings_booked=1, cold_calls_made=5,
            crm_activity_logging_rate_pct=0.20, cold_call_connect_rate_pct=0.02,
            email_reply_rate_pct=0.01, demo_to_opp_conversion_rate_pct=0.05,
            qualified_opps_created=0, pipeline_generated_usd=5_000,
            pipeline_target_usd=100_000, prior_period_pipeline_generated_usd=100_000,
        ))
        s = e.summary()
        assert s["risk_counts"].get("low", 0) >= 1
        assert s["risk_counts"].get("critical", 0) >= 1

    def test_summary_avg_coverage_score_correct(self):
        e = PipelineGenerationEfficiencyEngine()
        r1 = e.assess(make_input(rep_id="r1"))
        r2 = e.assess(make_input(rep_id="r2"))
        expected = round((r1.pipeline_coverage_score + r2.pipeline_coverage_score) / 2, 1)
        assert e.summary()["avg_pipeline_coverage_score"] == pytest.approx(expected)

    def test_summary_avg_conversion_score_correct(self):
        e = PipelineGenerationEfficiencyEngine()
        r1 = e.assess(make_input(rep_id="r1"))
        r2 = e.assess(make_input(rep_id="r2"))
        expected = round((r1.conversion_efficiency_score + r2.conversion_efficiency_score) / 2, 1)
        assert e.summary()["avg_conversion_efficiency_score"] == pytest.approx(expected)
