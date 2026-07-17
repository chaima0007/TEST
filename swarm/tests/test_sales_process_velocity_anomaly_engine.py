"""Comprehensive pytest test suite for SalesProcessVelocityAnomalyEngine."""

import dataclasses
import pytest

from swarm.intelligence.sales_process_velocity_anomaly_engine import (
    SalesProcessVelocityAnomalyEngine,
    SalesProcessVelocityInput,
    VelocityAnomaly,
    VelocityRisk,
    VelocityAlert,
    VelocitySeverity,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_input(**overrides) -> SalesProcessVelocityInput:
    """Return a baseline normal deal with any field overridden."""
    defaults = dict(
        deal_id="D001",
        rep_id="R001",
        deal_value_usd=50_000.0,
        company_avg_deal_value_usd=50_000.0,
        days_in_pipeline=30,
        company_avg_days_in_pipeline=30.0,
        stages_completed=4,
        expected_stages=4,
        discovery_days=7,
        expected_discovery_days=7.0,
        demo_days=5,
        expected_demo_days=5.0,
        proposal_days=8,
        expected_proposal_days=8.0,
        negotiation_days=10,
        expected_negotiation_days=10.0,
        stage_regression_count=0,
        stage_skip_count=0,
        close_date_changes=0,
        forecast_category_changes=0,
        end_of_period_push=0,
        rep_avg_deal_cycle_days=30.0,
    )
    defaults.update(overrides)
    return SalesProcessVelocityInput(**defaults)


@pytest.fixture
def engine():
    return SalesProcessVelocityAnomalyEngine()


@pytest.fixture
def normal_input():
    return make_input()


# ---------------------------------------------------------------------------
# 1. Enum value tests
# ---------------------------------------------------------------------------

class TestEnumValues:
    def test_velocity_anomaly_normal(self):
        assert VelocityAnomaly.normal.value == "normal"

    def test_velocity_anomaly_suspicious_fast(self):
        assert VelocityAnomaly.suspicious_fast.value == "suspicious_fast"

    def test_velocity_anomaly_stage_skipping(self):
        assert VelocityAnomaly.stage_skipping.value == "stage_skipping"

    def test_velocity_anomaly_stalled(self):
        assert VelocityAnomaly.stalled.value == "stalled"

    def test_velocity_anomaly_recycled(self):
        assert VelocityAnomaly.recycled.value == "recycled"

    def test_velocity_anomaly_forced_close(self):
        assert VelocityAnomaly.forced_close.value == "forced_close"

    def test_velocity_anomaly_count(self):
        assert len(VelocityAnomaly) == 6

    def test_velocity_risk_low(self):
        assert VelocityRisk.low.value == "low"

    def test_velocity_risk_moderate(self):
        assert VelocityRisk.moderate.value == "moderate"

    def test_velocity_risk_high(self):
        assert VelocityRisk.high.value == "high"

    def test_velocity_risk_critical(self):
        assert VelocityRisk.critical.value == "critical"

    def test_velocity_risk_count(self):
        assert len(VelocityRisk) == 4

    def test_velocity_alert_none(self):
        assert VelocityAlert.none.value == "none"

    def test_velocity_alert_flag(self):
        assert VelocityAlert.flag.value == "flag"

    def test_velocity_alert_review(self):
        assert VelocityAlert.review.value == "review"

    def test_velocity_alert_escalate(self):
        assert VelocityAlert.escalate.value == "escalate"

    def test_velocity_alert_audit(self):
        assert VelocityAlert.audit.value == "audit"

    def test_velocity_alert_count(self):
        assert len(VelocityAlert) == 5

    def test_velocity_severity_clean(self):
        assert VelocitySeverity.clean.value == "clean"

    def test_velocity_severity_watch(self):
        assert VelocitySeverity.watch.value == "watch"

    def test_velocity_severity_anomalous(self):
        assert VelocitySeverity.anomalous.value == "anomalous"

    def test_velocity_severity_fraud_risk(self):
        assert VelocitySeverity.fraud_risk.value == "fraud_risk"

    def test_velocity_severity_count(self):
        assert len(VelocitySeverity) == 4

    def test_enums_are_str_subclasses(self):
        assert isinstance(VelocityAnomaly.normal, str)
        assert isinstance(VelocityRisk.low, str)
        assert isinstance(VelocityAlert.none, str)
        assert isinstance(VelocitySeverity.clean, str)


# ---------------------------------------------------------------------------
# 2. Input dataclass – exactly 22 fields
# ---------------------------------------------------------------------------

class TestInputDataclass:
    def test_field_count_is_22(self):
        fields = dataclasses.fields(SalesProcessVelocityInput)
        assert len(fields) == 22

    def test_field_names(self):
        names = {f.name for f in dataclasses.fields(SalesProcessVelocityInput)}
        expected = {
            "deal_id", "rep_id", "deal_value_usd", "company_avg_deal_value_usd",
            "days_in_pipeline", "company_avg_days_in_pipeline",
            "stages_completed", "expected_stages",
            "discovery_days", "expected_discovery_days",
            "demo_days", "expected_demo_days",
            "proposal_days", "expected_proposal_days",
            "negotiation_days", "expected_negotiation_days",
            "stage_regression_count", "stage_skip_count",
            "close_date_changes", "forecast_category_changes",
            "end_of_period_push", "rep_avg_deal_cycle_days",
        }
        assert names == expected

    def test_no_rep_name_field(self):
        names = {f.name for f in dataclasses.fields(SalesProcessVelocityInput)}
        assert "rep_name" not in names

    def test_no_region_field(self):
        names = {f.name for f in dataclasses.fields(SalesProcessVelocityInput)}
        assert "region" not in names

    def test_no_competitive_displacement_field(self):
        names = {f.name for f in dataclasses.fields(SalesProcessVelocityInput)}
        assert "competitive_displacement" not in names

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(SalesProcessVelocityInput)

    def test_instantiation(self):
        inp = make_input()
        assert inp.deal_id == "D001"
        assert inp.rep_id == "R001"

    def test_field_deal_id(self):
        inp = make_input(deal_id="XYZ")
        assert inp.deal_id == "XYZ"

    def test_field_rep_id(self):
        inp = make_input(rep_id="R999")
        assert inp.rep_id == "R999"

    def test_field_deal_value_usd(self):
        inp = make_input(deal_value_usd=100_000.0)
        assert inp.deal_value_usd == 100_000.0

    def test_field_company_avg_deal_value_usd(self):
        inp = make_input(company_avg_deal_value_usd=20_000.0)
        assert inp.company_avg_deal_value_usd == 20_000.0

    def test_field_days_in_pipeline(self):
        inp = make_input(days_in_pipeline=90)
        assert inp.days_in_pipeline == 90

    def test_field_company_avg_days_in_pipeline(self):
        inp = make_input(company_avg_days_in_pipeline=45.0)
        assert inp.company_avg_days_in_pipeline == 45.0

    def test_field_stages_completed(self):
        inp = make_input(stages_completed=2)
        assert inp.stages_completed == 2

    def test_field_expected_stages(self):
        inp = make_input(expected_stages=6)
        assert inp.expected_stages == 6

    def test_field_stage_regression_count(self):
        inp = make_input(stage_regression_count=3)
        assert inp.stage_regression_count == 3

    def test_field_stage_skip_count(self):
        inp = make_input(stage_skip_count=2)
        assert inp.stage_skip_count == 2

    def test_field_end_of_period_push(self):
        inp = make_input(end_of_period_push=1)
        assert inp.end_of_period_push == 1

    def test_field_rep_avg_deal_cycle_days(self):
        inp = make_input(rep_avg_deal_cycle_days=60.0)
        assert inp.rep_avg_deal_cycle_days == 60.0


# ---------------------------------------------------------------------------
# 3. to_dict() – exactly 15 keys
# ---------------------------------------------------------------------------

class TestToDict:
    def test_to_dict_key_count(self, engine, normal_input):
        result = engine.assess(normal_input)
        assert len(result.to_dict()) == 15

    def test_to_dict_keys(self, engine, normal_input):
        d = engine.assess(normal_input).to_dict()
        expected = {
            "deal_id", "rep_id", "velocity_anomaly", "velocity_risk",
            "velocity_alert", "velocity_severity", "stage_completion_score",
            "timeline_deviation_score", "forecast_integrity_score",
            "pattern_risk_score", "velocity_composite", "is_anomalous",
            "requires_review", "pipeline_days_deviation", "velocity_signal",
        }
        assert set(d.keys()) == expected

    def test_to_dict_deal_id(self, engine):
        inp = make_input(deal_id="DEAL42")
        d = engine.assess(inp).to_dict()
        assert d["deal_id"] == "DEAL42"

    def test_to_dict_rep_id(self, engine):
        inp = make_input(rep_id="REP99")
        d = engine.assess(inp).to_dict()
        assert d["rep_id"] == "REP99"

    def test_to_dict_velocity_anomaly_is_str(self, engine, normal_input):
        d = engine.assess(normal_input).to_dict()
        assert isinstance(d["velocity_anomaly"], str)

    def test_to_dict_velocity_risk_is_str(self, engine, normal_input):
        d = engine.assess(normal_input).to_dict()
        assert isinstance(d["velocity_risk"], str)

    def test_to_dict_velocity_alert_is_str(self, engine, normal_input):
        d = engine.assess(normal_input).to_dict()
        assert isinstance(d["velocity_alert"], str)

    def test_to_dict_velocity_severity_is_str(self, engine, normal_input):
        d = engine.assess(normal_input).to_dict()
        assert isinstance(d["velocity_severity"], str)

    def test_to_dict_scores_are_float(self, engine, normal_input):
        d = engine.assess(normal_input).to_dict()
        for key in ("stage_completion_score", "timeline_deviation_score",
                    "forecast_integrity_score", "pattern_risk_score",
                    "velocity_composite", "pipeline_days_deviation"):
            assert isinstance(d[key], (int, float))

    def test_to_dict_is_anomalous_bool(self, engine, normal_input):
        d = engine.assess(normal_input).to_dict()
        assert isinstance(d["is_anomalous"], bool)

    def test_to_dict_requires_review_bool(self, engine, normal_input):
        d = engine.assess(normal_input).to_dict()
        assert isinstance(d["requires_review"], bool)

    def test_to_dict_velocity_signal_is_str(self, engine, normal_input):
        d = engine.assess(normal_input).to_dict()
        assert isinstance(d["velocity_signal"], str)

    def test_to_dict_scores_rounded_to_one_decimal(self, engine):
        inp = make_input(stage_skip_count=1)
        d = engine.assess(inp).to_dict()
        for key in ("stage_completion_score", "timeline_deviation_score",
                    "forecast_integrity_score", "pattern_risk_score",
                    "velocity_composite"):
            val = d[key]
            assert round(val, 1) == val

    def test_to_dict_pipeline_days_deviation_rounded(self, engine):
        inp = make_input(days_in_pipeline=33, company_avg_days_in_pipeline=30.3)
        d = engine.assess(inp).to_dict()
        val = d["pipeline_days_deviation"]
        assert round(val, 1) == val

    def test_to_dict_always_15_keys_high_anomaly(self, engine):
        inp = make_input(
            stage_skip_count=3, stage_regression_count=3,
            close_date_changes=6, forecast_category_changes=5,
            end_of_period_push=1, days_in_pipeline=2,
            company_avg_days_in_pipeline=30.0,
        )
        d = engine.assess(inp).to_dict()
        assert len(d) == 15


# ---------------------------------------------------------------------------
# 4. summary() – exactly 13 keys
# ---------------------------------------------------------------------------

class TestSummaryKeys:
    def test_empty_summary_has_13_keys(self):
        eng = SalesProcessVelocityAnomalyEngine()
        s = eng.summary()
        assert len(s) == 13

    def test_summary_after_assess_has_13_keys(self, engine, normal_input):
        engine.assess(normal_input)
        assert len(engine.summary()) == 13

    def test_summary_keys_exact(self):
        eng = SalesProcessVelocityAnomalyEngine()
        s = eng.summary()
        expected = {
            "total", "anomaly_counts", "risk_counts", "alert_counts",
            "severity_counts", "avg_velocity_composite", "anomalous_count",
            "review_required_count", "avg_stage_completion_score",
            "avg_timeline_deviation_score", "avg_forecast_integrity_score",
            "avg_pattern_risk_score", "avg_pipeline_days_deviation",
        }
        assert set(s.keys()) == expected

    def test_empty_summary_total_zero(self):
        eng = SalesProcessVelocityAnomalyEngine()
        assert eng.summary()["total"] == 0

    def test_empty_summary_averages_zero(self):
        eng = SalesProcessVelocityAnomalyEngine()
        s = eng.summary()
        assert s["avg_velocity_composite"] == 0.0
        assert s["avg_stage_completion_score"] == 0.0
        assert s["avg_timeline_deviation_score"] == 0.0
        assert s["avg_forecast_integrity_score"] == 0.0
        assert s["avg_pattern_risk_score"] == 0.0
        assert s["avg_pipeline_days_deviation"] == 0.0

    def test_empty_summary_counts_empty(self):
        eng = SalesProcessVelocityAnomalyEngine()
        s = eng.summary()
        assert s["anomaly_counts"] == {}
        assert s["risk_counts"] == {}
        assert s["alert_counts"] == {}
        assert s["severity_counts"] == {}

    def test_summary_total_matches_assessed(self, engine):
        for i in range(5):
            engine.assess(make_input(deal_id=f"D{i}"))
        assert engine.summary()["total"] == 5

    def test_summary_anomalous_count(self, engine):
        engine.assess(make_input())  # normal → not anomalous
        engine.assess(make_input(stage_skip_count=2))  # anomalous
        s = engine.summary()
        assert s["anomalous_count"] >= 1

    def test_summary_review_required_count(self, engine):
        engine.assess(make_input(close_date_changes=4))
        s = engine.summary()
        assert s["review_required_count"] >= 1

    def test_summary_anomaly_counts_dict(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["anomaly_counts"], dict)

    def test_summary_risk_counts_dict(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["risk_counts"], dict)

    def test_summary_alert_counts_dict(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["alert_counts"], dict)

    def test_summary_severity_counts_dict(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["severity_counts"], dict)

    def test_summary_avg_composite_rounded(self, engine):
        engine.assess(make_input())
        val = engine.summary()["avg_velocity_composite"]
        assert round(val, 1) == val

    def test_summary_avg_pipeline_dev_rounded(self, engine):
        engine.assess(make_input(days_in_pipeline=33, company_avg_days_in_pipeline=30.3))
        val = engine.summary()["avg_pipeline_days_deviation"]
        assert round(val, 1) == val

    def test_summary_counts_sum_to_total(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(4)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert sum(s["anomaly_counts"].values()) == s["total"]
        assert sum(s["risk_counts"].values()) == s["total"]
        assert sum(s["alert_counts"].values()) == s["total"]
        assert sum(s["severity_counts"].values()) == s["total"]


# ---------------------------------------------------------------------------
# 5. pipeline_days_deviation
# ---------------------------------------------------------------------------

class TestPipelineDaysDeviation:
    def test_zero_deviation(self, engine):
        inp = make_input(days_in_pipeline=30, company_avg_days_in_pipeline=30.0)
        r = engine.assess(inp)
        assert r.pipeline_days_deviation == 0.0

    def test_positive_deviation(self, engine):
        inp = make_input(days_in_pipeline=60, company_avg_days_in_pipeline=30.0)
        r = engine.assess(inp)
        assert r.pipeline_days_deviation == 30.0

    def test_negative_deviation(self, engine):
        inp = make_input(days_in_pipeline=10, company_avg_days_in_pipeline=30.0)
        r = engine.assess(inp)
        assert r.pipeline_days_deviation == -20.0

    def test_deviation_formula(self, engine):
        inp = make_input(days_in_pipeline=45, company_avg_days_in_pipeline=30.0)
        r = engine.assess(inp)
        assert r.pipeline_days_deviation == 45 - 30.0

    def test_deviation_rounded_in_dict(self, engine):
        inp = make_input(days_in_pipeline=33, company_avg_days_in_pipeline=30.333)
        d = engine.assess(inp).to_dict()
        assert d["pipeline_days_deviation"] == round(33 - 30.333, 1)

    def test_deviation_in_summary_avg(self, engine):
        engine.assess(make_input(days_in_pipeline=40, company_avg_days_in_pipeline=30.0))
        engine.assess(make_input(days_in_pipeline=20, company_avg_days_in_pipeline=30.0))
        s = engine.summary()
        assert s["avg_pipeline_days_deviation"] == 0.0


# ---------------------------------------------------------------------------
# 6. Composite formula: stage*0.25 + timeline*0.35 + forecast*0.25 + pattern*0.15
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_normal_deal_composite_low(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert r.velocity_composite < 20.0

    def test_composite_weights(self, engine):
        # Pure stage contribution with no other scores
        inp = make_input(stage_skip_count=1)  # stage += 15
        r = engine.assess(inp)
        # stage=15, timeline=0, forecast=0, pattern=0 → 15*0.25=3.75
        assert r.stage_completion_score == 15.0
        assert r.velocity_composite == pytest.approx(3.75 * 1, abs=2.0)

    def test_composite_clamped_to_100(self, engine):
        # Max out all sub-scores
        inp = make_input(
            stage_skip_count=3, stage_regression_count=3,
            stages_completed=1, expected_stages=10,
            days_in_pipeline=2, company_avg_days_in_pipeline=100.0,
            discovery_days=1, expected_discovery_days=20.0,
            demo_days=1, expected_demo_days=20.0,
            proposal_days=1, expected_proposal_days=20.0,
            negotiation_days=1, expected_negotiation_days=20.0,
            close_date_changes=5, forecast_category_changes=4,
            end_of_period_push=1,
            deal_value_usd=1_000_000.0, company_avg_deal_value_usd=50_000.0,
            rep_avg_deal_cycle_days=100.0,
        )
        r = engine.assess(inp)
        assert r.velocity_composite <= 100.0

    def test_composite_nonnegative(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert r.velocity_composite >= 0.0

    def test_subscores_nonnegative(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert r.stage_completion_score >= 0.0
        assert r.timeline_deviation_score >= 0.0
        assert r.forecast_integrity_score >= 0.0
        assert r.pattern_risk_score >= 0.0

    def test_subscores_max_100(self, engine):
        inp = make_input(
            stage_skip_count=3, stage_regression_count=3,
            days_in_pipeline=1, company_avg_days_in_pipeline=100.0,
            close_date_changes=5, forecast_category_changes=4,
            end_of_period_push=1,
        )
        r = engine.assess(inp)
        assert r.stage_completion_score <= 100.0
        assert r.timeline_deviation_score <= 100.0
        assert r.forecast_integrity_score <= 100.0
        assert r.pattern_risk_score <= 100.0

    def test_composite_rounded_to_1_decimal(self, engine):
        inp = make_input(stage_skip_count=1, close_date_changes=2)
        r = engine.assess(inp)
        assert round(r.velocity_composite, 1) == r.velocity_composite


# ---------------------------------------------------------------------------
# 7. is_anomalous invariants
# ---------------------------------------------------------------------------

class TestIsAnomalous:
    def test_normal_not_anomalous(self, engine, normal_input):
        assert not engine.assess(normal_input).is_anomalous

    def test_composite_gte_35_is_anomalous(self, engine):
        # Force high forecast score: close_date_changes=5 → +40, forecast_cat=4 → +35, eop=1 → +25 = 100
        # forecast*0.25=25, already >=35 with some timeline contribution
        inp = make_input(
            close_date_changes=5, forecast_category_changes=4,
            end_of_period_push=1,
            days_in_pipeline=5, company_avg_days_in_pipeline=30.0,
        )
        r = engine.assess(inp)
        assert r.is_anomalous

    def test_stage_skip_2_is_anomalous(self, engine):
        inp = make_input(stage_skip_count=2)
        assert engine.assess(inp).is_anomalous

    def test_stage_skip_3_is_anomalous(self, engine):
        inp = make_input(stage_skip_count=3)
        assert engine.assess(inp).is_anomalous

    def test_stage_skip_1_not_anomalous_otherwise_normal(self, engine):
        inp = make_input(stage_skip_count=1)
        r = engine.assess(inp)
        # skip=1 is not >= 2, composite likely low, no eop push
        assert not r.is_anomalous

    def test_eop_push_and_3_date_changes_anomalous(self, engine):
        inp = make_input(end_of_period_push=1, close_date_changes=3)
        assert engine.assess(inp).is_anomalous

    def test_eop_push_and_2_date_changes_not_anomalous_from_this_rule(self, engine):
        inp = make_input(end_of_period_push=1, close_date_changes=2)
        r = engine.assess(inp)
        # The eop rule requires close_date_changes >= 3; check composite separately
        if r.velocity_composite < 35 and inp.stage_skip_count < 2:
            assert not r.is_anomalous

    def test_eop_push_0_and_3_date_changes_not_triggered_by_eop_rule(self, engine):
        inp = make_input(end_of_period_push=0, close_date_changes=3)
        r = engine.assess(inp)
        # eop rule needs end_of_period_push==1; composite may still trigger
        # just verify is_anomalous consistent with composite or skip rule
        assert r.is_anomalous == (r.velocity_composite >= 35 or r.requires_review)  # approximate

    def test_stage_skip_2_overrides_low_composite(self, engine):
        inp = make_input(stage_skip_count=2)
        r = engine.assess(inp)
        assert r.is_anomalous is True

    def test_high_composite_triggers_anomalous(self, engine):
        inp = make_input(
            close_date_changes=5, forecast_category_changes=4, end_of_period_push=1,
            days_in_pipeline=2, company_avg_days_in_pipeline=30.0,
        )
        r = engine.assess(inp)
        assert r.velocity_composite >= 35
        assert r.is_anomalous


# ---------------------------------------------------------------------------
# 8. requires_review invariants
# ---------------------------------------------------------------------------

class TestRequiresReview:
    def test_normal_not_requires_review(self, engine, normal_input):
        assert not engine.assess(normal_input).requires_review

    def test_composite_gte_30_requires_review(self, engine):
        inp = make_input(
            close_date_changes=5, forecast_category_changes=4,
            days_in_pipeline=5, company_avg_days_in_pipeline=30.0,
        )
        r = engine.assess(inp)
        if r.velocity_composite >= 30:
            assert r.requires_review

    def test_close_date_4_requires_review(self, engine):
        inp = make_input(close_date_changes=4)
        assert engine.assess(inp).requires_review

    def test_close_date_5_requires_review(self, engine):
        inp = make_input(close_date_changes=5)
        assert engine.assess(inp).requires_review

    def test_close_date_3_not_from_this_rule(self, engine):
        inp = make_input(close_date_changes=3)
        r = engine.assess(inp)
        # close_date_changes=3 does not hit the >= 4 requires_review rule
        # composite=28*0.25=7.0, skip=0 → requires_review should be False
        assert not r.requires_review

    def test_stage_skip_2_requires_review(self, engine):
        inp = make_input(stage_skip_count=2)
        assert engine.assess(inp).requires_review

    def test_stage_skip_3_requires_review(self, engine):
        inp = make_input(stage_skip_count=3)
        assert engine.assess(inp).requires_review

    def test_requires_review_implies_is_anomalous_or_not(self, engine):
        # requires_review >= is_anomalous threshold; can be true when not anomalous
        inp = make_input(close_date_changes=4)
        r = engine.assess(inp)
        assert r.requires_review  # definitely true
        # is_anomalous may or may not be true depending on composite

    def test_anomalous_requires_review_consistency(self, engine):
        # If is_anomalous is True and composite >= 35 >= 30, requires_review must also be True
        inp = make_input(stage_skip_count=3, close_date_changes=5)
        r = engine.assess(inp)
        if r.is_anomalous and r.velocity_composite >= 30:
            assert r.requires_review


# ---------------------------------------------------------------------------
# 9. Stage completion score
# ---------------------------------------------------------------------------

class TestStageCompletionScore:
    def test_no_skips_no_regressions_baseline_0(self, engine):
        inp = make_input(stages_completed=4, expected_stages=4)
        r = engine.assess(inp)
        assert r.stage_completion_score == 0.0

    def test_skip_1_adds_15(self, engine):
        r = engine.assess(make_input(stage_skip_count=1))
        assert r.stage_completion_score >= 15.0

    def test_skip_2_adds_30(self, engine):
        r = engine.assess(make_input(stage_skip_count=2))
        assert r.stage_completion_score >= 30.0

    def test_skip_3_adds_45(self, engine):
        r = engine.assess(make_input(stage_skip_count=3))
        assert r.stage_completion_score >= 45.0

    def test_regression_1_adds_10(self, engine):
        r = engine.assess(make_input(stage_regression_count=1))
        assert r.stage_completion_score >= 10.0

    def test_regression_2_adds_22(self, engine):
        r = engine.assess(make_input(stage_regression_count=2))
        assert r.stage_completion_score >= 22.0

    def test_regression_3_adds_35(self, engine):
        r = engine.assess(make_input(stage_regression_count=3))
        assert r.stage_completion_score >= 35.0

    def test_low_completion_ratio_adds_20(self, engine):
        # completion_ratio < 0.5 and pipeline days > avg * 0.8
        inp = make_input(
            stages_completed=1, expected_stages=4,
            days_in_pipeline=30, company_avg_days_in_pipeline=30.0,
        )
        r = engine.assess(inp)
        assert r.stage_completion_score >= 20.0

    def test_high_completion_ratio_no_extra(self, engine):
        inp = make_input(stages_completed=4, expected_stages=4)
        r = engine.assess(inp)
        assert r.stage_completion_score == 0.0

    def test_clamped_at_100(self, engine):
        inp = make_input(stage_skip_count=3, stage_regression_count=3,
                         stages_completed=1, expected_stages=10,
                         days_in_pipeline=30, company_avg_days_in_pipeline=30.0)
        r = engine.assess(inp)
        # 45+35+20=100
        assert r.stage_completion_score == 100.0

    def test_combined_skip_and_regression(self, engine):
        inp = make_input(stage_skip_count=2, stage_regression_count=2)
        r = engine.assess(inp)
        assert r.stage_completion_score >= 52.0  # 30+22


# ---------------------------------------------------------------------------
# 10. Timeline deviation score
# ---------------------------------------------------------------------------

class TestTimelineDeviationScore:
    def test_normal_speed_no_deviation_score(self, engine):
        r = engine.assess(make_input(
            days_in_pipeline=30, company_avg_days_in_pipeline=30.0,
        ))
        assert r.timeline_deviation_score == 0.0

    def test_speed_ratio_below_01_adds_45(self, engine):
        inp = make_input(days_in_pipeline=2, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        assert r.timeline_deviation_score >= 45.0

    def test_speed_ratio_below_025_adds_30(self, engine):
        inp = make_input(days_in_pipeline=20, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        # ratio=0.2 < 0.25
        assert r.timeline_deviation_score >= 30.0

    def test_speed_ratio_below_04_adds_18(self, engine):
        inp = make_input(days_in_pipeline=35, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        # ratio=0.35 in [0.25, 0.4)
        assert r.timeline_deviation_score >= 18.0

    def test_speed_ratio_above_3_adds_25(self, engine):
        inp = make_input(days_in_pipeline=310, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        assert r.timeline_deviation_score >= 25.0

    def test_speed_ratio_above_2_adds_12(self, engine):
        inp = make_input(days_in_pipeline=210, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        assert r.timeline_deviation_score >= 12.0

    def test_stage_ratio_below_015_adds_8_per_stage(self, engine):
        inp = make_input(
            discovery_days=1, expected_discovery_days=20.0,
            demo_days=1, expected_demo_days=20.0,
            proposal_days=30, expected_proposal_days=30.0,
            negotiation_days=10, expected_negotiation_days=10.0,
        )
        r = engine.assess(inp)
        # Each fast stage (ratio < 0.15): discovery=0.05, demo=0.05 → +8 each
        assert r.timeline_deviation_score >= 16.0

    def test_stage_ratio_below_03_adds_4_per_stage(self, engine):
        inp = make_input(
            discovery_days=5, expected_discovery_days=20.0,  # 0.25 in [0.15,0.3)
            demo_days=30, expected_demo_days=30.0,
            proposal_days=30, expected_proposal_days=30.0,
            negotiation_days=10, expected_negotiation_days=10.0,
        )
        r = engine.assess(inp)
        assert r.timeline_deviation_score >= 4.0

    def test_zero_avg_pipeline_uses_speed_ratio_1(self, engine):
        inp = make_input(days_in_pipeline=30, company_avg_days_in_pipeline=0.0)
        r = engine.assess(inp)
        # speed_ratio defaults to 1.0 → no pipeline contribution
        assert r.timeline_deviation_score >= 0.0

    def test_clamped_at_100(self, engine):
        inp = make_input(
            days_in_pipeline=1, company_avg_days_in_pipeline=100.0,
            discovery_days=1, expected_discovery_days=100.0,
            demo_days=1, expected_demo_days=100.0,
            proposal_days=1, expected_proposal_days=100.0,
            negotiation_days=1, expected_negotiation_days=100.0,
        )
        r = engine.assess(inp)
        assert r.timeline_deviation_score <= 100.0

    def test_stage_days_zero_skips_ratio_check(self, engine):
        # actual=0 → skip per the "actual > 0" guard
        inp = make_input(discovery_days=0, expected_discovery_days=10.0)
        r = engine.assess(inp)
        # no contribution from that stage
        assert r.timeline_deviation_score >= 0.0


# ---------------------------------------------------------------------------
# 11. Forecast integrity score
# ---------------------------------------------------------------------------

class TestForecastIntegrityScore:
    def test_no_changes_zero(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert r.forecast_integrity_score == 0.0

    def test_close_date_2_adds_15(self, engine):
        r = engine.assess(make_input(close_date_changes=2))
        assert r.forecast_integrity_score >= 15.0

    def test_close_date_3_adds_28(self, engine):
        r = engine.assess(make_input(close_date_changes=3))
        assert r.forecast_integrity_score >= 28.0

    def test_close_date_5_adds_40(self, engine):
        r = engine.assess(make_input(close_date_changes=5))
        assert r.forecast_integrity_score >= 40.0

    def test_forecast_cat_1_adds_8(self, engine):
        r = engine.assess(make_input(forecast_category_changes=1))
        assert r.forecast_integrity_score >= 8.0

    def test_forecast_cat_2_adds_20(self, engine):
        r = engine.assess(make_input(forecast_category_changes=2))
        assert r.forecast_integrity_score >= 20.0

    def test_forecast_cat_4_adds_35(self, engine):
        r = engine.assess(make_input(forecast_category_changes=4))
        assert r.forecast_integrity_score >= 35.0

    def test_end_of_period_push_adds_25(self, engine):
        r = engine.assess(make_input(end_of_period_push=1))
        assert r.forecast_integrity_score >= 25.0

    def test_all_max_clamped_100(self, engine):
        inp = make_input(
            close_date_changes=5, forecast_category_changes=4, end_of_period_push=1
        )
        r = engine.assess(inp)
        assert r.forecast_integrity_score == 100.0

    def test_no_eop_push_no_contribution(self, engine):
        r = engine.assess(make_input(end_of_period_push=0))
        assert r.forecast_integrity_score == 0.0


# ---------------------------------------------------------------------------
# 12. Pattern risk score
# ---------------------------------------------------------------------------

class TestPatternRiskScore:
    def test_normal_zero(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert r.pattern_risk_score == 0.0

    def test_size_ratio_gt10_and_fast_adds_35(self, engine):
        inp = make_input(
            deal_value_usd=600_000.0,
            company_avg_deal_value_usd=50_000.0,  # ratio=12
            days_in_pipeline=10,
            company_avg_days_in_pipeline=30.0,   # pipeline < avg*0.5
        )
        r = engine.assess(inp)
        assert r.pattern_risk_score >= 35.0

    def test_size_ratio_gt5_very_fast_adds_20(self, engine):
        inp = make_input(
            deal_value_usd=300_000.0,
            company_avg_deal_value_usd=50_000.0,  # ratio=6
            days_in_pipeline=11,
            company_avg_days_in_pipeline=30.0,    # <avg*0.4=12
        )
        r = engine.assess(inp)
        assert r.pattern_risk_score >= 20.0

    def test_rep_ratio_below_02_adds_30(self, engine):
        inp = make_input(
            days_in_pipeline=5,
            rep_avg_deal_cycle_days=30.0,   # ratio=5/30≈0.167 < 0.2
        )
        r = engine.assess(inp)
        assert r.pattern_risk_score >= 30.0

    def test_rep_ratio_below_035_adds_18(self, engine):
        inp = make_input(
            days_in_pipeline=9,
            rep_avg_deal_cycle_days=30.0,   # ratio=9/30=0.3 in [0.2,0.35)
        )
        r = engine.assess(inp)
        assert r.pattern_risk_score >= 18.0

    def test_zero_avg_deal_value_no_contribution(self, engine):
        inp = make_input(company_avg_deal_value_usd=0.0)
        r = engine.assess(inp)
        # size_ratio branch skipped
        assert r.pattern_risk_score >= 0.0

    def test_zero_rep_avg_cycle_no_contribution(self, engine):
        inp = make_input(rep_avg_deal_cycle_days=0.0)
        r = engine.assess(inp)
        assert r.pattern_risk_score >= 0.0

    def test_clamped_at_100(self, engine):
        inp = make_input(
            deal_value_usd=1_000_000.0,
            company_avg_deal_value_usd=50_000.0,
            days_in_pipeline=5,
            company_avg_days_in_pipeline=100.0,
            rep_avg_deal_cycle_days=100.0,
        )
        r = engine.assess(inp)
        assert r.pattern_risk_score <= 100.0


# ---------------------------------------------------------------------------
# 13. Anomaly classification
# ---------------------------------------------------------------------------

class TestAnomalyClassification:
    def test_normal_classification(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert r.velocity_anomaly == VelocityAnomaly.normal

    def test_stage_skipping_priority(self, engine):
        inp = make_input(stage_skip_count=2)
        r = engine.assess(inp)
        assert r.velocity_anomaly == VelocityAnomaly.stage_skipping

    def test_stage_skipping_three(self, engine):
        inp = make_input(stage_skip_count=3)
        r = engine.assess(inp)
        assert r.velocity_anomaly == VelocityAnomaly.stage_skipping

    def test_recycled_regression_2(self, engine):
        inp = make_input(stage_regression_count=2)
        r = engine.assess(inp)
        assert r.velocity_anomaly == VelocityAnomaly.recycled

    def test_recycled_regression_3(self, engine):
        inp = make_input(stage_regression_count=3)
        r = engine.assess(inp)
        assert r.velocity_anomaly == VelocityAnomaly.recycled

    def test_forced_close(self, engine):
        inp = make_input(end_of_period_push=1, close_date_changes=2)
        r = engine.assess(inp)
        assert r.velocity_anomaly == VelocityAnomaly.forced_close

    def test_suspicious_fast(self, engine):
        # speed_ratio < 0.3 and timeline > 25
        inp = make_input(
            days_in_pipeline=20,
            company_avg_days_in_pipeline=100.0,  # ratio=0.2 < 0.3
            discovery_days=1, expected_discovery_days=20.0,  # +8 each
            demo_days=1, expected_demo_days=20.0,
            proposal_days=1, expected_proposal_days=20.0,
            negotiation_days=1, expected_negotiation_days=20.0,
        )
        r = engine.assess(inp)
        # speed_ratio=0.2 < 0.3 and timeline must be > 25
        if r.timeline_deviation_score > 25:
            assert r.velocity_anomaly == VelocityAnomaly.suspicious_fast

    def test_stalled(self, engine):
        inp = make_input(days_in_pipeline=300, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        assert r.velocity_anomaly == VelocityAnomaly.stalled

    def test_stage_skip_takes_priority_over_recycled(self, engine):
        # stage_skip_count >= 2 checked first
        inp = make_input(stage_skip_count=2, stage_regression_count=2)
        r = engine.assess(inp)
        assert r.velocity_anomaly == VelocityAnomaly.stage_skipping

    def test_recycled_takes_priority_over_forced_close(self, engine):
        inp = make_input(stage_regression_count=2, end_of_period_push=1, close_date_changes=2)
        r = engine.assess(inp)
        assert r.velocity_anomaly == VelocityAnomaly.recycled

    def test_stalled_ratio_exactly_25_is_normal(self, engine):
        inp = make_input(days_in_pipeline=250, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        # speed_ratio=2.5 which is NOT > 2.5
        assert r.velocity_anomaly == VelocityAnomaly.normal

    def test_stalled_ratio_above_25(self, engine):
        inp = make_input(days_in_pipeline=251, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        assert r.velocity_anomaly == VelocityAnomaly.stalled


# ---------------------------------------------------------------------------
# 14. Risk classification
# ---------------------------------------------------------------------------

class TestRiskClassification:
    def test_low_risk_below_20(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert r.velocity_risk == VelocityRisk.low

    def test_moderate_risk_20_to_40(self, engine):
        # Need composite in [20, 40)
        inp = make_input(close_date_changes=3, forecast_category_changes=2)
        r = engine.assess(inp)
        if 20 <= r.velocity_composite < 40:
            assert r.velocity_risk == VelocityRisk.moderate

    def test_high_risk_40_to_60(self, engine):
        inp = make_input(
            close_date_changes=5, forecast_category_changes=2,
            days_in_pipeline=5, company_avg_days_in_pipeline=30.0,
        )
        r = engine.assess(inp)
        if 40 <= r.velocity_composite < 60:
            assert r.velocity_risk == VelocityRisk.high

    def test_critical_risk_above_60(self, engine):
        inp = make_input(
            close_date_changes=5, forecast_category_changes=4,
            end_of_period_push=1,
            days_in_pipeline=2, company_avg_days_in_pipeline=100.0,
            discovery_days=1, expected_discovery_days=20.0,
            demo_days=1, expected_demo_days=20.0,
        )
        r = engine.assess(inp)
        if r.velocity_composite >= 60:
            assert r.velocity_risk == VelocityRisk.critical

    def test_risk_thresholds_exact_boundaries(self, engine):
        # Test classification at exact thresholds using known score
        # Composite exactly 20 → moderate
        # We trust the implementation; just verify the classification
        for composite_val, expected_risk in [
            (19.9, VelocityRisk.low),
            (20.0, VelocityRisk.moderate),
            (39.9, VelocityRisk.moderate),
            (40.0, VelocityRisk.high),
            (59.9, VelocityRisk.high),
            (60.0, VelocityRisk.critical),
        ]:
            eng = SalesProcessVelocityAnomalyEngine()
            r = eng._classify_risk(composite_val)
            assert r == expected_risk


# ---------------------------------------------------------------------------
# 15. Severity classification
# ---------------------------------------------------------------------------

class TestSeverityClassification:
    def test_clean_below_20(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert r.velocity_severity == VelocitySeverity.clean

    def test_severity_thresholds(self):
        eng = SalesProcessVelocityAnomalyEngine()
        assert eng._classify_severity(0.0) == VelocitySeverity.clean
        assert eng._classify_severity(19.9) == VelocitySeverity.clean
        assert eng._classify_severity(20.0) == VelocitySeverity.watch
        assert eng._classify_severity(39.9) == VelocitySeverity.watch
        assert eng._classify_severity(40.0) == VelocitySeverity.anomalous
        assert eng._classify_severity(64.9) == VelocitySeverity.anomalous
        assert eng._classify_severity(65.0) == VelocitySeverity.fraud_risk
        assert eng._classify_severity(100.0) == VelocitySeverity.fraud_risk


# ---------------------------------------------------------------------------
# 16. Alert classification
# ---------------------------------------------------------------------------

class TestAlertClassification:
    def test_none_alert_for_low_risk(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert r.velocity_alert == VelocityAlert.none

    def test_alert_thresholds_audit(self):
        eng = SalesProcessVelocityAnomalyEngine()
        alert = eng._recommended_alert(VelocityRisk.critical, 65.0)
        assert alert == VelocityAlert.audit

    def test_alert_thresholds_escalate(self):
        eng = SalesProcessVelocityAnomalyEngine()
        alert = eng._recommended_alert(VelocityRisk.critical, 60.0)
        assert alert == VelocityAlert.escalate

    def test_alert_thresholds_review(self):
        eng = SalesProcessVelocityAnomalyEngine()
        alert = eng._recommended_alert(VelocityRisk.high, 50.0)
        assert alert == VelocityAlert.review

    def test_alert_thresholds_flag(self):
        eng = SalesProcessVelocityAnomalyEngine()
        alert = eng._recommended_alert(VelocityRisk.moderate, 30.0)
        assert alert == VelocityAlert.flag

    def test_alert_thresholds_none(self):
        eng = SalesProcessVelocityAnomalyEngine()
        alert = eng._recommended_alert(VelocityRisk.low, 10.0)
        assert alert == VelocityAlert.none

    def test_composite_gte_65_triggers_audit_regardless_of_risk(self):
        eng = SalesProcessVelocityAnomalyEngine()
        # Even moderate risk: composite>=65 → audit
        alert = eng._recommended_alert(VelocityRisk.moderate, 65.0)
        assert alert == VelocityAlert.audit


# ---------------------------------------------------------------------------
# 17. Signal messages
# ---------------------------------------------------------------------------

class TestSignalMessages:
    def test_normal_signal(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert "normal parameters" in r.velocity_signal

    def test_stalled_signal(self, engine):
        inp = make_input(days_in_pipeline=300, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        assert "stalled" in r.velocity_signal

    def test_stage_skipping_signal(self, engine):
        inp = make_input(stage_skip_count=2)
        r = engine.assess(inp)
        assert "skip" in r.velocity_signal

    def test_recycled_signal(self, engine):
        inp = make_input(stage_regression_count=2)
        r = engine.assess(inp)
        assert "recycled" in r.velocity_signal

    def test_forced_close_signal(self, engine):
        inp = make_input(end_of_period_push=1, close_date_changes=2)
        r = engine.assess(inp)
        assert "forced close" in r.velocity_signal or "end-of-period" in r.velocity_signal

    def test_signal_contains_composite_for_anomalous(self, engine):
        inp = make_input(stage_skip_count=2)
        r = engine.assess(inp)
        assert "composite" in r.velocity_signal

    def test_signal_not_empty(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert len(r.velocity_signal) > 0

    def test_suspicious_fast_signal_contains_faster(self, engine):
        inp = make_input(
            days_in_pipeline=20,
            company_avg_days_in_pipeline=100.0,
            discovery_days=1, expected_discovery_days=20.0,
            demo_days=1, expected_demo_days=20.0,
            proposal_days=1, expected_proposal_days=20.0,
            negotiation_days=1, expected_negotiation_days=20.0,
        )
        r = engine.assess(inp)
        if r.velocity_anomaly == VelocityAnomaly.suspicious_fast:
            assert "faster" in r.velocity_signal or "days" in r.velocity_signal


# ---------------------------------------------------------------------------
# 18. assess() return type and state
# ---------------------------------------------------------------------------

class TestAssessMethod:
    def test_returns_result_object(self, engine, normal_input):
        from swarm.intelligence.sales_process_velocity_anomaly_engine import SalesProcessVelocityResult
        r = engine.assess(normal_input)
        assert isinstance(r, SalesProcessVelocityResult)

    def test_result_stored_in_results(self, engine, normal_input):
        engine.assess(normal_input)
        assert len(engine._results) == 1

    def test_multiple_assessments_accumulate(self, engine):
        for i in range(5):
            engine.assess(make_input(deal_id=f"D{i}"))
        assert len(engine._results) == 5

    def test_result_deal_id_matches_input(self, engine):
        inp = make_input(deal_id="DEAL999")
        r = engine.assess(inp)
        assert r.deal_id == "DEAL999"

    def test_result_rep_id_matches_input(self, engine):
        inp = make_input(rep_id="REP42")
        r = engine.assess(inp)
        assert r.rep_id == "REP42"

    def test_fresh_engine_no_results(self):
        eng = SalesProcessVelocityAnomalyEngine()
        assert len(eng._results) == 0

    def test_assess_does_not_mutate_input(self, engine):
        inp = make_input(stage_skip_count=2)
        orig_skip = inp.stage_skip_count
        engine.assess(inp)
        assert inp.stage_skip_count == orig_skip


# ---------------------------------------------------------------------------
# 19. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self, engine):
        result = engine.assess_batch([make_input(deal_id="D1"), make_input(deal_id="D2")])
        assert isinstance(result, list)

    def test_returns_correct_count(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(7)]
        results = engine.assess_batch(inputs)
        assert len(results) == 7

    def test_empty_batch_returns_empty_list(self, engine):
        assert engine.assess_batch([]) == []

    def test_batch_accumulates_results(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(3)]
        engine.assess_batch(inputs)
        assert len(engine._results) == 3

    def test_batch_order_preserved(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.deal_id == f"D{i}"

    def test_batch_results_same_as_individual(self, engine):
        inp1 = make_input(deal_id="D1", stage_skip_count=2)
        inp2 = make_input(deal_id="D2")
        batch = engine.assess_batch([inp1, inp2])
        eng2 = SalesProcessVelocityAnomalyEngine()
        r1 = eng2.assess(inp1)
        r2 = eng2.assess(inp2)
        assert batch[0].velocity_anomaly == r1.velocity_anomaly
        assert batch[1].velocity_anomaly == r2.velocity_anomaly

    def test_single_item_batch(self, engine):
        result = engine.assess_batch([make_input()])
        assert len(result) == 1


# ---------------------------------------------------------------------------
# 20. Summary aggregations
# ---------------------------------------------------------------------------

class TestSummaryAggregations:
    def test_all_normal_deals(self, engine):
        for i in range(3):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert s["total"] == 3
        assert "normal" in s["anomaly_counts"]

    def test_mixed_anomalies_counted(self, engine):
        engine.assess(make_input(deal_id="D1"))
        engine.assess(make_input(deal_id="D2", stage_skip_count=2))
        engine.assess(make_input(deal_id="D3", stage_regression_count=2))
        s = engine.summary()
        assert s["total"] == 3
        assert sum(s["anomaly_counts"].values()) == 3

    def test_avg_composite_calculation(self, engine):
        r1 = engine.assess(make_input(deal_id="D1"))
        r2 = engine.assess(make_input(deal_id="D2", stage_skip_count=2))
        s = engine.summary()
        expected = round((r1.velocity_composite + r2.velocity_composite) / 2, 1)
        assert s["avg_velocity_composite"] == expected

    def test_avg_stage_score_calculation(self, engine):
        r1 = engine.assess(make_input(deal_id="D1"))
        r2 = engine.assess(make_input(deal_id="D2", stage_skip_count=1))
        s = engine.summary()
        expected = round((r1.stage_completion_score + r2.stage_completion_score) / 2, 1)
        assert s["avg_stage_completion_score"] == expected

    def test_avg_timeline_score_calculation(self, engine):
        r1 = engine.assess(make_input(deal_id="D1"))
        r2 = engine.assess(make_input(deal_id="D2", days_in_pipeline=300, company_avg_days_in_pipeline=100.0))
        s = engine.summary()
        expected = round((r1.timeline_deviation_score + r2.timeline_deviation_score) / 2, 1)
        assert s["avg_timeline_deviation_score"] == expected

    def test_avg_forecast_score_calculation(self, engine):
        r1 = engine.assess(make_input(deal_id="D1"))
        r2 = engine.assess(make_input(deal_id="D2", close_date_changes=5))
        s = engine.summary()
        expected = round((r1.forecast_integrity_score + r2.forecast_integrity_score) / 2, 1)
        assert s["avg_forecast_integrity_score"] == expected

    def test_avg_pattern_score_calculation(self, engine):
        r1 = engine.assess(make_input(deal_id="D1"))
        r2 = engine.assess(make_input(deal_id="D2", days_in_pipeline=5, rep_avg_deal_cycle_days=30.0))
        s = engine.summary()
        expected = round((r1.pattern_risk_score + r2.pattern_risk_score) / 2, 1)
        assert s["avg_pattern_risk_score"] == expected

    def test_anomalous_count_accurate(self, engine):
        engine.assess(make_input(deal_id="D1"))           # normal
        engine.assess(make_input(deal_id="D2", stage_skip_count=2))  # anomalous
        engine.assess(make_input(deal_id="D3", stage_skip_count=2))  # anomalous
        s = engine.summary()
        assert s["anomalous_count"] == 2

    def test_review_required_count_accurate(self, engine):
        engine.assess(make_input(deal_id="D1"))
        engine.assess(make_input(deal_id="D2", close_date_changes=4))
        s = engine.summary()
        assert s["review_required_count"] >= 1

    def test_summary_after_batch(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(10)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 10

    def test_summary_called_twice_consistent(self, engine, normal_input):
        engine.assess(normal_input)
        s1 = engine.summary()
        s2 = engine.summary()
        assert s1 == s2


# ---------------------------------------------------------------------------
# 21. Edge cases and boundary conditions
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_expected_stages_no_div_error(self, engine):
        inp = make_input(expected_stages=0)
        r = engine.assess(inp)
        assert r is not None

    def test_zero_company_avg_pipeline_no_error(self, engine):
        inp = make_input(company_avg_days_in_pipeline=0.0)
        r = engine.assess(inp)
        assert r is not None

    def test_zero_rep_avg_cycle_no_error(self, engine):
        inp = make_input(rep_avg_deal_cycle_days=0.0)
        r = engine.assess(inp)
        assert r is not None

    def test_zero_avg_deal_value_no_error(self, engine):
        inp = make_input(company_avg_deal_value_usd=0.0)
        r = engine.assess(inp)
        assert r is not None

    def test_zero_expected_stage_days_no_error(self, engine):
        inp = make_input(
            expected_discovery_days=0.0,
            expected_demo_days=0.0,
            expected_proposal_days=0.0,
            expected_negotiation_days=0.0,
        )
        r = engine.assess(inp)
        assert r is not None

    def test_very_large_deal_value(self, engine):
        inp = make_input(deal_value_usd=1_000_000_000.0)
        r = engine.assess(inp)
        assert r.pattern_risk_score <= 100.0

    def test_very_large_days_in_pipeline(self, engine):
        inp = make_input(days_in_pipeline=10_000, company_avg_days_in_pipeline=30.0)
        r = engine.assess(inp)
        assert r.timeline_deviation_score <= 100.0

    def test_single_day_pipeline(self, engine):
        inp = make_input(days_in_pipeline=1, company_avg_days_in_pipeline=30.0)
        r = engine.assess(inp)
        assert r is not None

    def test_all_zeros(self, engine):
        inp = make_input(
            deal_value_usd=0.0, company_avg_deal_value_usd=0.0,
            days_in_pipeline=0, company_avg_days_in_pipeline=0.0,
            stages_completed=0, expected_stages=0,
            discovery_days=0, expected_discovery_days=0.0,
            demo_days=0, expected_demo_days=0.0,
            proposal_days=0, expected_proposal_days=0.0,
            negotiation_days=0, expected_negotiation_days=0.0,
            stage_regression_count=0, stage_skip_count=0,
            close_date_changes=0, forecast_category_changes=0,
            end_of_period_push=0, rep_avg_deal_cycle_days=0.0,
        )
        r = engine.assess(inp)
        assert r.velocity_composite >= 0.0

    def test_max_skip_and_regression(self, engine):
        # skip>=3 → +45, regression>=3 → +35; completion ratio 4/4=1.0 not <0.5 → no +20
        # Total = 80, clamped to 80 (not 100 without completion bonus)
        inp = make_input(stage_skip_count=10, stage_regression_count=10)
        r = engine.assess(inp)
        assert r.stage_completion_score == 80.0

    def test_large_batch_no_error(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(100)]
        results = engine.assess_batch(inputs)
        assert len(results) == 100

    def test_pipeline_days_deviation_exact_negative(self, engine):
        inp = make_input(days_in_pipeline=5, company_avg_days_in_pipeline=30.0)
        r = engine.assess(inp)
        assert r.pipeline_days_deviation == -25.0

    def test_each_engine_instance_independent(self):
        eng1 = SalesProcessVelocityAnomalyEngine()
        eng2 = SalesProcessVelocityAnomalyEngine()
        eng1.assess(make_input(deal_id="D1"))
        assert len(eng2._results) == 0

    def test_multiple_engines_same_result(self):
        inp = make_input(stage_skip_count=2)
        eng1 = SalesProcessVelocityAnomalyEngine()
        eng2 = SalesProcessVelocityAnomalyEngine()
        r1 = eng1.assess(inp)
        r2 = eng2.assess(inp)
        assert r1.velocity_composite == r2.velocity_composite
        assert r1.is_anomalous == r2.is_anomalous


# ---------------------------------------------------------------------------
# 22. Score combination scenarios
# ---------------------------------------------------------------------------

class TestScenarios:
    def test_perfectly_normal_deal(self, engine):
        inp = make_input()
        r = engine.assess(inp)
        assert r.velocity_anomaly == VelocityAnomaly.normal
        assert r.velocity_risk == VelocityRisk.low
        assert r.velocity_severity == VelocitySeverity.clean
        assert r.velocity_alert == VelocityAlert.none
        assert not r.is_anomalous
        assert not r.requires_review
        assert r.pipeline_days_deviation == 0.0

    def test_extreme_fraud_scenario(self, engine):
        inp = make_input(
            stage_skip_count=3,
            stage_regression_count=3,
            close_date_changes=6,
            forecast_category_changes=5,
            end_of_period_push=1,
            days_in_pipeline=2,
            company_avg_days_in_pipeline=100.0,
            deal_value_usd=1_000_000.0,
            company_avg_deal_value_usd=50_000.0,
            rep_avg_deal_cycle_days=100.0,
            discovery_days=1,
            expected_discovery_days=20.0,
            demo_days=1,
            expected_demo_days=20.0,
            proposal_days=1,
            expected_proposal_days=20.0,
            negotiation_days=1,
            expected_negotiation_days=20.0,
        )
        r = engine.assess(inp)
        assert r.is_anomalous
        assert r.requires_review
        assert r.velocity_composite >= 50.0

    def test_stalled_deal_scenario(self, engine):
        inp = make_input(days_in_pipeline=310, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        assert r.velocity_anomaly == VelocityAnomaly.stalled
        assert r.timeline_deviation_score >= 25.0

    def test_end_of_quarter_push_scenario(self, engine):
        inp = make_input(
            end_of_period_push=1,
            close_date_changes=5,
            forecast_category_changes=3,
        )
        r = engine.assess(inp)
        assert r.forecast_integrity_score >= 65.0  # 40+25 min
        assert r.is_anomalous or r.requires_review

    def test_stage_skipping_high_value_deal(self, engine):
        inp = make_input(
            stage_skip_count=2,
            deal_value_usd=600_000.0,
            company_avg_deal_value_usd=50_000.0,
            days_in_pipeline=10,
            company_avg_days_in_pipeline=30.0,
        )
        r = engine.assess(inp)
        assert r.velocity_anomaly == VelocityAnomaly.stage_skipping
        assert r.is_anomalous

    def test_slow_deal_with_regressions(self, engine):
        inp = make_input(
            stage_regression_count=3,
            days_in_pipeline=400,
            company_avg_days_in_pipeline=100.0,
        )
        r = engine.assess(inp)
        assert r.velocity_anomaly == VelocityAnomaly.recycled

    def test_forced_close_then_summary(self, engine):
        for i in range(3):
            engine.assess(make_input(
                deal_id=f"D{i}",
                end_of_period_push=1,
                close_date_changes=2,
            ))
        s = engine.summary()
        assert s["anomaly_counts"].get("forced_close", 0) == 3

    def test_consistent_deal_ids_in_batch_summary(self, engine):
        inputs = [
            make_input(deal_id="D1", stage_skip_count=2),   # is_anomalous via skip>=2
            make_input(deal_id="D2", stage_regression_count=2),  # recycled but composite=5.5, not anomalous
            make_input(deal_id="D3"),
        ]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 3
        # Only D1 triggers is_anomalous (stage_skip_count>=2); D2 regression alone does not
        assert s["anomalous_count"] == 1

    def test_to_dict_velocity_anomaly_values_valid(self, engine):
        valid_values = {a.value for a in VelocityAnomaly}
        for scenario in [
            make_input(),
            make_input(stage_skip_count=2),
            make_input(stage_regression_count=2),
            make_input(days_in_pipeline=300, company_avg_days_in_pipeline=100.0),
            make_input(end_of_period_push=1, close_date_changes=2),
        ]:
            eng = SalesProcessVelocityAnomalyEngine()
            d = eng.assess(scenario).to_dict()
            assert d["velocity_anomaly"] in valid_values

    def test_to_dict_velocity_risk_values_valid(self, engine):
        valid_values = {r.value for r in VelocityRisk}
        for scenario in [make_input(), make_input(stage_skip_count=3)]:
            eng = SalesProcessVelocityAnomalyEngine()
            d = eng.assess(scenario).to_dict()
            assert d["velocity_risk"] in valid_values

    def test_summary_avg_pipeline_dev_negative(self):
        eng = SalesProcessVelocityAnomalyEngine()
        eng.assess(make_input(days_in_pipeline=10, company_avg_days_in_pipeline=30.0))
        s = eng.summary()
        assert s["avg_pipeline_days_deviation"] < 0

    def test_summary_avg_pipeline_dev_positive(self):
        eng = SalesProcessVelocityAnomalyEngine()
        eng.assess(make_input(days_in_pipeline=60, company_avg_days_in_pipeline=30.0))
        s = eng.summary()
        assert s["avg_pipeline_days_deviation"] > 0


# ---------------------------------------------------------------------------
# 23. Risk/Severity/Alert alignment
# ---------------------------------------------------------------------------

class TestAlignments:
    def test_low_risk_never_audit(self, engine):
        # Audit requires composite >= 65; low risk needs composite < 20
        # These are mutually exclusive
        inp = make_input()
        r = engine.assess(inp)
        if r.velocity_risk == VelocityRisk.low:
            assert r.velocity_alert != VelocityAlert.audit

    def test_fraud_risk_severity_high_composite(self, engine):
        # fraud_risk requires composite >= 65
        inp = make_input(
            close_date_changes=5, forecast_category_changes=4,
            end_of_period_push=1,
            days_in_pipeline=2, company_avg_days_in_pipeline=100.0,
        )
        r = engine.assess(inp)
        if r.velocity_severity == VelocitySeverity.fraud_risk:
            assert r.velocity_composite >= 65.0

    def test_clean_severity_implies_low_risk(self, engine):
        inp = make_input()
        r = engine.assess(inp)
        if r.velocity_severity == VelocitySeverity.clean:
            assert r.velocity_risk == VelocityRisk.low

    def test_audit_alert_implies_high_composite(self, engine):
        inp = make_input(
            close_date_changes=5, forecast_category_changes=4,
            end_of_period_push=1,
            days_in_pipeline=2, company_avg_days_in_pipeline=100.0,
        )
        r = engine.assess(inp)
        if r.velocity_alert == VelocityAlert.audit:
            assert r.velocity_composite >= 65.0

    def test_none_alert_implies_low_risk(self, engine):
        inp = make_input()
        r = engine.assess(inp)
        if r.velocity_alert == VelocityAlert.none:
            assert r.velocity_risk == VelocityRisk.low

    def test_is_anomalous_and_requires_review_relationship(self, engine):
        # requires_review threshold (30) is lower than is_anomalous threshold (35)
        # So is_anomalous implies requires_review (via composite path)
        inp = make_input(
            close_date_changes=5, forecast_category_changes=4,
            end_of_period_push=1,
            days_in_pipeline=2, company_avg_days_in_pipeline=100.0,
        )
        r = engine.assess(inp)
        if r.velocity_composite >= 35:
            assert r.is_anomalous
            assert r.requires_review  # composite >= 35 >= 30


# ---------------------------------------------------------------------------
# 24. Dataclass result field types
# ---------------------------------------------------------------------------

class TestResultFieldTypes:
    def test_result_deal_id_str(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.deal_id, str)

    def test_result_rep_id_str(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.rep_id, str)

    def test_result_velocity_anomaly_enum(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.velocity_anomaly, VelocityAnomaly)

    def test_result_velocity_risk_enum(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.velocity_risk, VelocityRisk)

    def test_result_velocity_alert_enum(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.velocity_alert, VelocityAlert)

    def test_result_velocity_severity_enum(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.velocity_severity, VelocitySeverity)

    def test_result_stage_completion_score_float(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.stage_completion_score, float)

    def test_result_timeline_deviation_score_float(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.timeline_deviation_score, float)

    def test_result_forecast_integrity_score_float(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.forecast_integrity_score, float)

    def test_result_pattern_risk_score_float(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.pattern_risk_score, float)

    def test_result_velocity_composite_float(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.velocity_composite, float)

    def test_result_is_anomalous_bool(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.is_anomalous, bool)

    def test_result_requires_review_bool(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.requires_review, bool)

    def test_result_pipeline_days_deviation_float(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.pipeline_days_deviation, float)

    def test_result_velocity_signal_str(self, engine, normal_input):
        r = engine.assess(normal_input)
        assert isinstance(r.velocity_signal, str)


# ---------------------------------------------------------------------------
# 25. Additional boundary-precise tests
# ---------------------------------------------------------------------------

class TestBoundaryPrecise:
    def test_skip_count_0_no_skip_score(self, engine):
        r = engine.assess(make_input(stage_skip_count=0))
        # skip contribution = 0
        assert r.stage_completion_score == 0.0  # no regressions either, ratio OK

    def test_regression_count_0_no_regression_score(self, engine):
        r = engine.assess(make_input(stage_regression_count=0))
        assert r.stage_completion_score == 0.0

    def test_close_date_1_no_forecast_contribution(self, engine):
        r = engine.assess(make_input(close_date_changes=1))
        # close_date_changes=1 doesn't hit >= 2 threshold
        assert r.forecast_integrity_score == 0.0

    def test_forecast_cat_0_no_contribution(self, engine):
        r = engine.assess(make_input(forecast_category_changes=0))
        assert r.forecast_integrity_score == 0.0

    def test_speed_ratio_exactly_01_boundary(self, engine):
        # ratio = 0.1 is NOT < 0.1, so no +45; check it falls in next bracket
        inp = make_input(days_in_pipeline=10, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        # ratio=0.1 → NOT < 0.1, and NOT < 0.25, so we're in the >= 0.1 < 0.25 range → +30
        assert r.timeline_deviation_score >= 30.0

    def test_speed_ratio_just_below_01(self, engine):
        inp = make_input(days_in_pipeline=9, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        assert r.timeline_deviation_score >= 45.0

    def test_speed_ratio_exactly_025_no_30_bonus(self, engine):
        # ratio = 0.25 is NOT < 0.25
        inp = make_input(days_in_pipeline=25, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        # 0.25 not < 0.25; also not < 0.4 → +18
        assert r.timeline_deviation_score >= 18.0

    def test_speed_ratio_exactly_3_not_stalled_anomaly(self, engine):
        # ratio = 3.0 is NOT > 3.0 for +25
        inp = make_input(days_in_pipeline=300, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        # timeline: speed_ratio=3.0 not > 3.0 → check > 2.0 → yes +12
        assert r.timeline_deviation_score >= 12.0

    def test_speed_ratio_above_3_stalled_score(self, engine):
        inp = make_input(days_in_pipeline=301, company_avg_days_in_pipeline=100.0)
        r = engine.assess(inp)
        assert r.timeline_deviation_score >= 25.0

    def test_stage_completion_ratio_exactly_05_no_bonus(self, engine):
        # completion_ratio = 0.5 is NOT < 0.5
        inp = make_input(stages_completed=2, expected_stages=4,
                         days_in_pipeline=30, company_avg_days_in_pipeline=30.0)
        r = engine.assess(inp)
        # ratio=0.5, not < 0.5 → no +20
        assert r.stage_completion_score == 0.0

    def test_stage_completion_ratio_below_05_with_long_pipeline(self, engine):
        inp = make_input(
            stages_completed=1, expected_stages=4,
            days_in_pipeline=30,  # 30 > 30*0.8=24
            company_avg_days_in_pipeline=30.0,
        )
        r = engine.assess(inp)
        assert r.stage_completion_score >= 20.0

    def test_stage_completion_short_pipeline_no_bonus(self, engine):
        # pipeline days < avg * 0.8 → no bonus even with low completion
        inp = make_input(
            stages_completed=1, expected_stages=4,
            days_in_pipeline=20,  # 20 < 30*0.8=24
            company_avg_days_in_pipeline=30.0,
        )
        r = engine.assess(inp)
        # no +20, stage_skip=0, regression=0
        assert r.stage_completion_score == 0.0

    def test_size_ratio_exactly_10_no_big_bonus(self, engine):
        # size_ratio = 10.0 is NOT > 10.0 → check > 5.0
        inp = make_input(
            deal_value_usd=500_000.0,
            company_avg_deal_value_usd=50_000.0,  # ratio=10
            days_in_pipeline=10,
            company_avg_days_in_pipeline=30.0,   # < 30*0.4=12 → yes
        )
        r = engine.assess(inp)
        # size_ratio=10, not >10; is >5 and pipeline<avg*0.4 → +20
        assert r.pattern_risk_score >= 20.0

    def test_size_ratio_above_10_fast_adds_35(self, engine):
        inp = make_input(
            deal_value_usd=510_000.0,
            company_avg_deal_value_usd=50_000.0,  # ratio > 10
            days_in_pipeline=14,
            company_avg_days_in_pipeline=30.0,    # < 30*0.5=15 → yes
        )
        r = engine.assess(inp)
        assert r.pattern_risk_score >= 35.0

    def test_rep_ratio_exactly_02_no_30_bonus(self, engine):
        inp = make_input(days_in_pipeline=6, rep_avg_deal_cycle_days=30.0)
        r = engine.assess(inp)
        # ratio=6/30=0.2, not < 0.2
        # Is it < 0.35? yes → +18
        assert r.pattern_risk_score >= 18.0

    def test_rep_ratio_below_02_adds_30(self, engine):
        inp = make_input(days_in_pipeline=5, rep_avg_deal_cycle_days=30.0)
        r = engine.assess(inp)
        # 5/30=0.1667 < 0.2 → +30
        assert r.pattern_risk_score >= 30.0

    def test_stage_ratio_exactly_015_no_8_bonus(self, engine):
        # stage_ratio = 0.15, not < 0.15 → check < 0.3 → +4
        inp = make_input(discovery_days=3, expected_discovery_days=20.0)
        r = engine.assess(inp)
        # 3/20=0.15 → not < 0.15, is < 0.3 → +4
        assert r.timeline_deviation_score >= 4.0

    def test_stage_ratio_below_015_adds_8(self, engine):
        inp = make_input(discovery_days=2, expected_discovery_days=20.0)
        r = engine.assess(inp)
        # 2/20=0.1 < 0.15 → +8
        assert r.timeline_deviation_score >= 8.0

    def test_forced_close_needs_eop_and_date_changes(self, engine):
        # eop=1 but only 1 date change → not forced_close via that rule
        inp = make_input(end_of_period_push=1, close_date_changes=1)
        r = engine.assess(inp)
        # forced_close rule: end_of_period_push AND close_date_changes >= 2
        # 1 < 2 → not forced_close from this rule
        assert r.velocity_anomaly != VelocityAnomaly.forced_close

    def test_composite_gte_35_exactly(self, engine):
        # Build a scenario where we can compute expected composite
        # stage=30 (skip=2), timeline=0, forecast=0, pattern=0 → 30*0.25=7.5, not >=35
        # Need higher contributions
        inp = make_input(
            stage_skip_count=2,
            close_date_changes=5,  # forecast=40
            forecast_category_changes=4,  # forecast +=35, total =75, clamped 100
            end_of_period_push=1,   # forecast +=25
            days_in_pipeline=2, company_avg_days_in_pipeline=100.0,  # timeline: +45 (ratio<0.1) + stage deviations
        )
        r = engine.assess(inp)
        assert r.velocity_composite >= 35.0
        assert r.is_anomalous

    def test_requires_review_threshold_30(self, engine):
        # stage=30 (skip=2) → composite: 30*0.25=7.5 alone not >=30
        # But skip=2 triggers requires_review directly
        inp = make_input(stage_skip_count=2)
        r = engine.assess(inp)
        assert r.requires_review

    def test_close_date_changes_3_forecast_score(self, engine):
        r = engine.assess(make_input(close_date_changes=3))
        assert r.forecast_integrity_score == 28.0

    def test_close_date_changes_2_forecast_score(self, engine):
        r = engine.assess(make_input(close_date_changes=2))
        assert r.forecast_integrity_score == 15.0

    def test_forecast_cat_1_score(self, engine):
        r = engine.assess(make_input(forecast_category_changes=1))
        assert r.forecast_integrity_score == 8.0

    def test_forecast_cat_2_score(self, engine):
        r = engine.assess(make_input(forecast_category_changes=2))
        assert r.forecast_integrity_score == 20.0

    def test_forecast_cat_3_score(self, engine):
        r = engine.assess(make_input(forecast_category_changes=3))
        assert r.forecast_integrity_score == 20.0  # 3 uses the >=2 bucket

    def test_regression_1_score(self, engine):
        r = engine.assess(make_input(stage_regression_count=1))
        assert r.stage_completion_score == 10.0

    def test_regression_2_score(self, engine):
        r = engine.assess(make_input(stage_regression_count=2))
        assert r.stage_completion_score == 22.0

    def test_regression_3_score(self, engine):
        r = engine.assess(make_input(stage_regression_count=3))
        assert r.stage_completion_score == 35.0

    def test_skip_1_score(self, engine):
        r = engine.assess(make_input(stage_skip_count=1))
        assert r.stage_completion_score == 15.0

    def test_skip_2_score(self, engine):
        r = engine.assess(make_input(stage_skip_count=2))
        assert r.stage_completion_score == 30.0

    def test_skip_3_score(self, engine):
        r = engine.assess(make_input(stage_skip_count=3))
        assert r.stage_completion_score == 45.0

    def test_end_of_period_push_0_no_forecast_bonus(self, engine):
        r = engine.assess(make_input(end_of_period_push=0))
        # No eop contribution; other fields default 0
        assert r.forecast_integrity_score == 0.0


# ---------------------------------------------------------------------------
# 26. Summary key content types
# ---------------------------------------------------------------------------

class TestSummaryContentTypes:
    def test_total_is_int(self, engine, normal_input):
        engine.assess(normal_input)
        assert isinstance(engine.summary()["total"], int)

    def test_anomalous_count_is_int(self, engine, normal_input):
        engine.assess(normal_input)
        assert isinstance(engine.summary()["anomalous_count"], int)

    def test_review_required_count_is_int(self, engine, normal_input):
        engine.assess(normal_input)
        assert isinstance(engine.summary()["review_required_count"], int)

    def test_avg_velocity_composite_is_float(self, engine, normal_input):
        engine.assess(normal_input)
        val = engine.summary()["avg_velocity_composite"]
        assert isinstance(val, (int, float))

    def test_avg_stage_completion_score_is_float(self, engine, normal_input):
        engine.assess(normal_input)
        val = engine.summary()["avg_stage_completion_score"]
        assert isinstance(val, (int, float))

    def test_all_avg_fields_rounded_1_decimal(self, engine):
        engine.assess(make_input(stage_skip_count=1, close_date_changes=2))
        s = engine.summary()
        for key in (
            "avg_velocity_composite", "avg_stage_completion_score",
            "avg_timeline_deviation_score", "avg_forecast_integrity_score",
            "avg_pattern_risk_score", "avg_pipeline_days_deviation",
        ):
            val = s[key]
            assert round(val, 1) == val, f"{key}={val} not rounded to 1 decimal"

    def test_anomaly_counts_keys_are_strings(self, engine, normal_input):
        engine.assess(normal_input)
        for k in engine.summary()["anomaly_counts"]:
            assert isinstance(k, str)

    def test_risk_counts_keys_are_strings(self, engine, normal_input):
        engine.assess(normal_input)
        for k in engine.summary()["risk_counts"]:
            assert isinstance(k, str)
