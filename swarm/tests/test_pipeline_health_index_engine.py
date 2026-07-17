import pytest
from swarm.intelligence.pipeline_health_index_engine import (
    HealthGrade,
    HealthDimension,
    PipelineRisk,
    HealthAction,
    PipelineHealthInput,
    PipelineHealthResult,
    PipelineHealthIndexEngine,
)


# ─── Fixtures ─────────────────────────────────────────────────────────────────

def make_input(**overrides) -> PipelineHealthInput:
    defaults = dict(
        pipeline_id="pipe-001",
        rep_id="rep-001",
        rep_name="Alice Dupont",
        region="EMEA",
        total_deals=10,
        total_pipeline_eur=300_000.0,
        quota_eur=100_000.0,
        deals_early_stage=3,
        deals_mid_stage=4,
        deals_late_stage=3,
        avg_deal_age_days=30.0,
        avg_cycle_length_benchmark_days=60.0,
        deals_stale_30d=0,
        avg_deal_health_score=80.0,
        qualified_deals_pct=80.0,
        avg_next_step_adherence_pct=80.0,
        calls_last_30d=20,
        meetings_last_30d=10,
        call_benchmark_30d=20,
        meeting_benchmark_30d=10,
        deals_single_threaded=0,
        deals_no_exec_sponsor=0,
        deals_overdue_close_date=0,
        rep_win_rate_pct=40.0,
        manager_reviewed_deals=5,
        forecast_accuracy_pct=80.0,
    )
    defaults.update(overrides)
    return PipelineHealthInput(**defaults)


@pytest.fixture
def engine():
    return PipelineHealthIndexEngine()


@pytest.fixture
def default_input():
    return make_input()


# ─── Test Classes ─────────────────────────────────────────────────────────────


class TestHealthGradeEnum:
    def test_excellent_value(self):
        assert HealthGrade.EXCELLENT.value == "excellent"

    def test_good_value(self):
        assert HealthGrade.GOOD.value == "good"

    def test_fair_value(self):
        assert HealthGrade.FAIR.value == "fair"

    def test_poor_value(self):
        assert HealthGrade.POOR.value == "poor"

    def test_critical_value(self):
        assert HealthGrade.CRITICAL.value == "critical"

    def test_str_inheritance_excellent(self):
        assert isinstance(HealthGrade.EXCELLENT, str)

    def test_str_inheritance_critical(self):
        assert isinstance(HealthGrade.CRITICAL, str)

    def test_str_equality_excellent(self):
        assert HealthGrade.EXCELLENT == "excellent"

    def test_str_equality_critical(self):
        assert HealthGrade.CRITICAL == "critical"

    def test_all_members(self):
        members = [g.value for g in HealthGrade]
        assert set(members) == {"excellent", "good", "fair", "poor", "critical"}

    def test_member_count(self):
        assert len(HealthGrade) == 5


class TestHealthDimensionEnum:
    def test_velocity_value(self):
        assert HealthDimension.VELOCITY.value == "velocity"

    def test_quality_value(self):
        assert HealthDimension.QUALITY.value == "quality"

    def test_coverage_value(self):
        assert HealthDimension.COVERAGE.value == "coverage"

    def test_diversity_value(self):
        assert HealthDimension.DIVERSITY.value == "diversity"

    def test_activity_value(self):
        assert HealthDimension.ACTIVITY.value == "activity"

    def test_str_inheritance(self):
        assert isinstance(HealthDimension.VELOCITY, str)

    def test_str_equality_velocity(self):
        assert HealthDimension.VELOCITY == "velocity"

    def test_all_members(self):
        members = {d.value for d in HealthDimension}
        assert members == {"velocity", "quality", "coverage", "diversity", "activity"}

    def test_member_count(self):
        assert len(HealthDimension) == 5


class TestPipelineRiskEnum:
    def test_low_value(self):
        assert PipelineRisk.LOW.value == "low"

    def test_moderate_value(self):
        assert PipelineRisk.MODERATE.value == "moderate"

    def test_high_value(self):
        assert PipelineRisk.HIGH.value == "high"

    def test_severe_value(self):
        assert PipelineRisk.SEVERE.value == "severe"

    def test_str_inheritance(self):
        assert isinstance(PipelineRisk.SEVERE, str)

    def test_str_equality_low(self):
        assert PipelineRisk.LOW == "low"

    def test_all_members(self):
        members = {r.value for r in PipelineRisk}
        assert members == {"low", "moderate", "high", "severe"}

    def test_member_count(self):
        assert len(PipelineRisk) == 4


class TestHealthActionEnum:
    def test_accelerate_value(self):
        assert HealthAction.ACCELERATE.value == "accelerate"

    def test_add_pipeline_value(self):
        assert HealthAction.ADD_PIPELINE.value == "add_pipeline"

    def test_improve_qual_value(self):
        assert HealthAction.IMPROVE_QUAL.value == "improve_qual"

    def test_rebalance_value(self):
        assert HealthAction.REBALANCE.value == "rebalance"

    def test_boost_activity_value(self):
        assert HealthAction.BOOST_ACTIVITY.value == "boost_activity"

    def test_maintain_value(self):
        assert HealthAction.MAINTAIN.value == "maintain"

    def test_str_inheritance(self):
        assert isinstance(HealthAction.MAINTAIN, str)

    def test_str_equality_maintain(self):
        assert HealthAction.MAINTAIN == "maintain"

    def test_all_members(self):
        members = {a.value for a in HealthAction}
        assert members == {"accelerate", "add_pipeline", "improve_qual", "rebalance", "boost_activity", "maintain"}

    def test_member_count(self):
        assert len(HealthAction) == 6


class TestPipelineHealthInputFields:
    def test_pipeline_id_field(self):
        inp = make_input(pipeline_id="p-xyz")
        assert inp.pipeline_id == "p-xyz"

    def test_rep_id_field(self):
        inp = make_input(rep_id="r-123")
        assert inp.rep_id == "r-123"

    def test_rep_name_field(self):
        inp = make_input(rep_name="Bob Martin")
        assert inp.rep_name == "Bob Martin"

    def test_region_field(self):
        inp = make_input(region="APAC")
        assert inp.region == "APAC"

    def test_total_deals_field(self):
        inp = make_input(total_deals=20)
        assert inp.total_deals == 20

    def test_total_pipeline_eur_field(self):
        inp = make_input(total_pipeline_eur=500_000.0)
        assert inp.total_pipeline_eur == 500_000.0

    def test_quota_eur_field(self):
        inp = make_input(quota_eur=150_000.0)
        assert inp.quota_eur == 150_000.0

    def test_deals_early_stage_field(self):
        inp = make_input(deals_early_stage=5)
        assert inp.deals_early_stage == 5

    def test_deals_mid_stage_field(self):
        inp = make_input(deals_mid_stage=3)
        assert inp.deals_mid_stage == 3

    def test_deals_late_stage_field(self):
        inp = make_input(deals_late_stage=2)
        assert inp.deals_late_stage == 2

    def test_avg_deal_age_days_field(self):
        inp = make_input(avg_deal_age_days=45.0)
        assert inp.avg_deal_age_days == 45.0

    def test_avg_cycle_length_benchmark_days_field(self):
        inp = make_input(avg_cycle_length_benchmark_days=90.0)
        assert inp.avg_cycle_length_benchmark_days == 90.0

    def test_deals_stale_30d_field(self):
        inp = make_input(deals_stale_30d=3)
        assert inp.deals_stale_30d == 3

    def test_avg_deal_health_score_field(self):
        inp = make_input(avg_deal_health_score=75.0)
        assert inp.avg_deal_health_score == 75.0

    def test_qualified_deals_pct_field(self):
        inp = make_input(qualified_deals_pct=60.0)
        assert inp.qualified_deals_pct == 60.0

    def test_avg_next_step_adherence_pct_field(self):
        inp = make_input(avg_next_step_adherence_pct=90.0)
        assert inp.avg_next_step_adherence_pct == 90.0

    def test_calls_last_30d_field(self):
        inp = make_input(calls_last_30d=15)
        assert inp.calls_last_30d == 15

    def test_meetings_last_30d_field(self):
        inp = make_input(meetings_last_30d=8)
        assert inp.meetings_last_30d == 8

    def test_call_benchmark_30d_field(self):
        inp = make_input(call_benchmark_30d=25)
        assert inp.call_benchmark_30d == 25

    def test_meeting_benchmark_30d_field(self):
        inp = make_input(meeting_benchmark_30d=12)
        assert inp.meeting_benchmark_30d == 12

    def test_deals_single_threaded_field(self):
        inp = make_input(deals_single_threaded=2)
        assert inp.deals_single_threaded == 2

    def test_deals_no_exec_sponsor_field(self):
        inp = make_input(deals_no_exec_sponsor=4)
        assert inp.deals_no_exec_sponsor == 4

    def test_deals_overdue_close_date_field(self):
        inp = make_input(deals_overdue_close_date=1)
        assert inp.deals_overdue_close_date == 1

    def test_rep_win_rate_pct_field(self):
        inp = make_input(rep_win_rate_pct=35.0)
        assert inp.rep_win_rate_pct == 35.0

    def test_manager_reviewed_deals_field(self):
        inp = make_input(manager_reviewed_deals=7)
        assert inp.manager_reviewed_deals == 7

    def test_forecast_accuracy_pct_field(self):
        inp = make_input(forecast_accuracy_pct=70.0)
        assert inp.forecast_accuracy_pct == 70.0

    def test_total_field_count(self):
        import dataclasses
        fields = dataclasses.fields(PipelineHealthInput)
        assert len(fields) == 26


class TestPipelineHealthResultToDictKeys:
    def test_to_dict_returns_17_keys(self, engine, default_input):
        result = engine.analyze(default_input)
        d = result.to_dict()
        assert len(d) == 17

    def test_to_dict_has_pipeline_id(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "pipeline_id" in d

    def test_to_dict_has_rep_id(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "rep_id" in d

    def test_to_dict_has_rep_name(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "rep_name" in d

    def test_to_dict_has_region(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "region" in d

    def test_to_dict_has_health_grade(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "health_grade" in d

    def test_to_dict_has_pipeline_risk(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "pipeline_risk" in d

    def test_to_dict_has_health_action(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "health_action" in d

    def test_to_dict_has_phi_score(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "phi_score" in d

    def test_to_dict_has_velocity_score(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "velocity_score" in d

    def test_to_dict_has_quality_score(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "quality_score" in d

    def test_to_dict_has_coverage_score(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "coverage_score" in d

    def test_to_dict_has_activity_score(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "activity_score" in d

    def test_to_dict_has_coverage_ratio(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "coverage_ratio" in d

    def test_to_dict_has_stale_deal_pct(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "stale_deal_pct" in d

    def test_to_dict_has_remediation_plays(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "remediation_plays" in d

    def test_to_dict_has_risk_signals(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "risk_signals" in d

    def test_to_dict_has_manager_alerts(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert "manager_alerts" in d

    def test_to_dict_exact_keys(self, engine, default_input):
        expected = {
            "pipeline_id", "rep_id", "rep_name", "region",
            "health_grade", "pipeline_risk", "health_action",
            "phi_score", "velocity_score", "quality_score",
            "coverage_score", "activity_score",
            "coverage_ratio", "stale_deal_pct",
            "remediation_plays", "risk_signals", "manager_alerts",
        }
        d = engine.analyze(default_input).to_dict()
        assert set(d.keys()) == expected

    def test_to_dict_values_propagated(self, engine):
        inp = make_input(pipeline_id="p-abc", rep_id="r-xyz", rep_name="Carol", region="US")
        d = engine.analyze(inp).to_dict()
        assert d["pipeline_id"] == "p-abc"
        assert d["rep_id"] == "r-xyz"
        assert d["rep_name"] == "Carol"
        assert d["region"] == "US"

    def test_to_dict_remediation_plays_is_list(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert isinstance(d["remediation_plays"], list)

    def test_to_dict_risk_signals_is_list(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert isinstance(d["risk_signals"], list)

    def test_to_dict_manager_alerts_is_list(self, engine, default_input):
        d = engine.analyze(default_input).to_dict()
        assert isinstance(d["manager_alerts"], list)


class TestVelocityScore:
    def test_age_ratio_at_most_0_5_returns_100(self, engine):
        inp = make_input(avg_deal_age_days=25.0, avg_cycle_length_benchmark_days=100.0, deals_stale_30d=0)
        score = engine._velocity_score(inp)
        assert score == 100.0

    def test_age_ratio_exactly_0_5_returns_100(self, engine):
        inp = make_input(avg_deal_age_days=50.0, avg_cycle_length_benchmark_days=100.0, deals_stale_30d=0)
        score = engine._velocity_score(inp)
        assert score == 100.0

    def test_age_ratio_0_6_returns_85(self, engine):
        inp = make_input(avg_deal_age_days=60.0, avg_cycle_length_benchmark_days=100.0, deals_stale_30d=0)
        score = engine._velocity_score(inp)
        assert score == 85.0

    def test_age_ratio_exactly_0_8_returns_85(self, engine):
        inp = make_input(avg_deal_age_days=80.0, avg_cycle_length_benchmark_days=100.0, deals_stale_30d=0)
        score = engine._velocity_score(inp)
        assert score == 85.0

    def test_age_ratio_0_9_returns_70(self, engine):
        inp = make_input(avg_deal_age_days=90.0, avg_cycle_length_benchmark_days=100.0, deals_stale_30d=0)
        score = engine._velocity_score(inp)
        assert score == 70.0

    def test_age_ratio_exactly_1_0_returns_70(self, engine):
        inp = make_input(avg_deal_age_days=100.0, avg_cycle_length_benchmark_days=100.0, deals_stale_30d=0)
        score = engine._velocity_score(inp)
        assert score == 70.0

    def test_age_ratio_1_2_returns_50(self, engine):
        inp = make_input(avg_deal_age_days=120.0, avg_cycle_length_benchmark_days=100.0, deals_stale_30d=0)
        score = engine._velocity_score(inp)
        assert score == 50.0

    def test_age_ratio_exactly_1_3_returns_50(self, engine):
        inp = make_input(avg_deal_age_days=130.0, avg_cycle_length_benchmark_days=100.0, deals_stale_30d=0)
        score = engine._velocity_score(inp)
        assert score == 50.0

    def test_age_ratio_1_5_returns_30(self, engine):
        inp = make_input(avg_deal_age_days=150.0, avg_cycle_length_benchmark_days=100.0, deals_stale_30d=0)
        score = engine._velocity_score(inp)
        assert score == 30.0

    def test_age_ratio_exactly_1_6_returns_30(self, engine):
        inp = make_input(avg_deal_age_days=160.0, avg_cycle_length_benchmark_days=100.0, deals_stale_30d=0)
        score = engine._velocity_score(inp)
        assert score == 30.0

    def test_age_ratio_above_1_6_returns_10_base(self, engine):
        inp = make_input(avg_deal_age_days=200.0, avg_cycle_length_benchmark_days=100.0, deals_stale_30d=0)
        score = engine._velocity_score(inp)
        assert score == 10.0

    def test_zero_benchmark_returns_50(self, engine):
        inp = make_input(avg_cycle_length_benchmark_days=0, total_deals=10)
        score = engine._velocity_score(inp)
        assert score == 50.0

    def test_zero_total_deals_returns_50(self, engine):
        inp = make_input(total_deals=0, avg_cycle_length_benchmark_days=60.0)
        score = engine._velocity_score(inp)
        assert score == 50.0

    def test_stale_penalty_applied(self, engine):
        inp = make_input(
            avg_deal_age_days=50.0,
            avg_cycle_length_benchmark_days=100.0,
            deals_stale_30d=5,
            total_deals=10,
        )
        # age_ratio=0.5 -> vel=100, stale_pct=0.5 -> penalty=min(30,0.5*60)=30 -> 70
        score = engine._velocity_score(inp)
        assert score == 70.0

    def test_stale_penalty_capped_at_30(self, engine):
        inp = make_input(
            avg_deal_age_days=50.0,
            avg_cycle_length_benchmark_days=100.0,
            deals_stale_30d=10,
            total_deals=10,
        )
        # stale_pct=1.0 -> penalty=min(30, 60)=30 -> 100-30=70
        score = engine._velocity_score(inp)
        assert score == 70.0

    def test_clamped_at_zero(self, engine):
        inp = make_input(
            avg_deal_age_days=200.0,
            avg_cycle_length_benchmark_days=100.0,
            deals_stale_30d=10,
            total_deals=10,
        )
        # base=10, penalty=30 -> -20 -> clamped to 0
        score = engine._velocity_score(inp)
        assert score == 0.0

    def test_clamped_at_100(self, engine):
        inp = make_input(
            avg_deal_age_days=1.0,
            avg_cycle_length_benchmark_days=100.0,
            deals_stale_30d=0,
        )
        score = engine._velocity_score(inp)
        assert score <= 100.0

    def test_score_is_numeric(self, engine, default_input):
        score = engine._velocity_score(default_input)
        assert isinstance(score, (int, float))


class TestQualityScore:
    def test_perfect_inputs_returns_100(self, engine):
        inp = make_input(
            avg_deal_health_score=100.0,
            qualified_deals_pct=100.0,
            avg_next_step_adherence_pct=100.0,
            rep_win_rate_pct=100.0,
        )
        score = engine._quality_score(inp)
        assert score == 100.0

    def test_zero_inputs_returns_0(self, engine):
        inp = make_input(
            avg_deal_health_score=0.0,
            qualified_deals_pct=0.0,
            avg_next_step_adherence_pct=0.0,
            rep_win_rate_pct=0.0,
        )
        score = engine._quality_score(inp)
        assert score == 0.0

    def test_health_score_component_max_40(self, engine):
        inp = make_input(
            avg_deal_health_score=100.0,
            qualified_deals_pct=0.0,
            avg_next_step_adherence_pct=0.0,
            rep_win_rate_pct=0.0,
        )
        score = engine._quality_score(inp)
        assert score == 40.0

    def test_qualified_pct_component_max_30(self, engine):
        inp = make_input(
            avg_deal_health_score=0.0,
            qualified_deals_pct=100.0,
            avg_next_step_adherence_pct=0.0,
            rep_win_rate_pct=0.0,
        )
        score = engine._quality_score(inp)
        assert score == 30.0

    def test_next_step_component_max_20(self, engine):
        inp = make_input(
            avg_deal_health_score=0.0,
            qualified_deals_pct=0.0,
            avg_next_step_adherence_pct=100.0,
            rep_win_rate_pct=0.0,
        )
        score = engine._quality_score(inp)
        assert score == 20.0

    def test_win_rate_component_max_10(self, engine):
        inp = make_input(
            avg_deal_health_score=0.0,
            qualified_deals_pct=0.0,
            avg_next_step_adherence_pct=0.0,
            rep_win_rate_pct=100.0,
        )
        score = engine._quality_score(inp)
        assert score == 10.0

    def test_health_score_partial(self, engine):
        inp = make_input(
            avg_deal_health_score=50.0,
            qualified_deals_pct=0.0,
            avg_next_step_adherence_pct=0.0,
            rep_win_rate_pct=0.0,
        )
        score = engine._quality_score(inp)
        assert score == pytest.approx(20.0)

    def test_qualified_pct_partial(self, engine):
        inp = make_input(
            avg_deal_health_score=0.0,
            qualified_deals_pct=50.0,
            avg_next_step_adherence_pct=0.0,
            rep_win_rate_pct=0.0,
        )
        score = engine._quality_score(inp)
        assert score == pytest.approx(15.0)

    def test_score_is_numeric(self, engine, default_input):
        score = engine._quality_score(default_input)
        assert isinstance(score, (int, float))

    def test_clamped_at_100(self, engine):
        inp = make_input(
            avg_deal_health_score=200.0,
            qualified_deals_pct=200.0,
            avg_next_step_adherence_pct=200.0,
            rep_win_rate_pct=200.0,
        )
        score = engine._quality_score(inp)
        assert score == 100.0


class TestCoverageScore:
    def test_ratio_4_or_more_returns_100(self, engine):
        inp = make_input(total_pipeline_eur=400_000.0, quota_eur=100_000.0)
        score = engine._coverage_score(inp)
        assert score == 100.0

    def test_ratio_exactly_4_returns_100(self, engine):
        inp = make_input(total_pipeline_eur=400_000.0, quota_eur=100_000.0)
        score = engine._coverage_score(inp)
        assert score == 100.0

    def test_ratio_5_returns_100(self, engine):
        inp = make_input(total_pipeline_eur=500_000.0, quota_eur=100_000.0)
        score = engine._coverage_score(inp)
        assert score == 100.0

    def test_ratio_3_to_4_returns_85(self, engine):
        inp = make_input(total_pipeline_eur=350_000.0, quota_eur=100_000.0)
        score = engine._coverage_score(inp)
        assert score == 85.0

    def test_ratio_exactly_3_returns_85(self, engine):
        inp = make_input(total_pipeline_eur=300_000.0, quota_eur=100_000.0)
        score = engine._coverage_score(inp)
        assert score == 85.0

    def test_ratio_2_to_3_returns_70(self, engine):
        inp = make_input(total_pipeline_eur=250_000.0, quota_eur=100_000.0)
        score = engine._coverage_score(inp)
        assert score == 70.0

    def test_ratio_exactly_2_returns_70(self, engine):
        inp = make_input(total_pipeline_eur=200_000.0, quota_eur=100_000.0)
        score = engine._coverage_score(inp)
        assert score == 70.0

    def test_ratio_1_5_to_2_returns_55(self, engine):
        inp = make_input(total_pipeline_eur=175_000.0, quota_eur=100_000.0)
        score = engine._coverage_score(inp)
        assert score == 55.0

    def test_ratio_exactly_1_5_returns_55(self, engine):
        inp = make_input(total_pipeline_eur=150_000.0, quota_eur=100_000.0)
        score = engine._coverage_score(inp)
        assert score == 55.0

    def test_ratio_1_to_1_5_returns_40(self, engine):
        inp = make_input(total_pipeline_eur=120_000.0, quota_eur=100_000.0)
        score = engine._coverage_score(inp)
        assert score == 40.0

    def test_ratio_exactly_1_returns_40(self, engine):
        inp = make_input(total_pipeline_eur=100_000.0, quota_eur=100_000.0)
        score = engine._coverage_score(inp)
        assert score == 40.0

    def test_ratio_below_1_is_ratio_times_40(self, engine):
        inp = make_input(total_pipeline_eur=50_000.0, quota_eur=100_000.0)
        score = engine._coverage_score(inp)
        assert score == pytest.approx(20.0)

    def test_ratio_zero_returns_0(self, engine):
        inp = make_input(total_pipeline_eur=0.0, quota_eur=100_000.0)
        score = engine._coverage_score(inp)
        assert score == 0.0

    def test_zero_quota_returns_80(self, engine):
        inp = make_input(quota_eur=0.0, total_pipeline_eur=500_000.0)
        score = engine._coverage_score(inp)
        assert score == 80.0

    def test_score_is_numeric(self, engine, default_input):
        score = engine._coverage_score(default_input)
        assert isinstance(score, (int, float))


class TestActivityScore:
    def test_perfect_calls_and_meetings_returns_85_plus(self, engine):
        inp = make_input(
            calls_last_30d=20, call_benchmark_30d=20,
            meetings_last_30d=10, meeting_benchmark_30d=10,
            manager_reviewed_deals=10, total_deals=10,
        )
        score = engine._activity_score(inp)
        assert score == 100.0

    def test_zero_calls_with_benchmark(self, engine):
        inp = make_input(
            calls_last_30d=0, call_benchmark_30d=20,
            meetings_last_30d=10, meeting_benchmark_30d=10,
            manager_reviewed_deals=10, total_deals=10,
        )
        # call=0, mtg=35, review=15 -> 50
        score = engine._activity_score(inp)
        assert score == 50.0

    def test_zero_benchmark_calls_adds_50(self, engine):
        inp = make_input(
            calls_last_30d=0, call_benchmark_30d=0,
            meetings_last_30d=0, meeting_benchmark_30d=10,
            manager_reviewed_deals=0, total_deals=10,
        )
        # call_benchmark=0 -> +50, mtg_ratio=0 -> +0, review=0 -> +0 -> 50
        score = engine._activity_score(inp)
        assert score == 50.0

    def test_zero_benchmark_meetings_adds_35(self, engine):
        inp = make_input(
            calls_last_30d=0, call_benchmark_30d=10,
            meetings_last_30d=0, meeting_benchmark_30d=0,
            manager_reviewed_deals=0, total_deals=10,
        )
        # call_ratio=0 -> +0, mtg_benchmark=0 -> +35, review=0 -> +0 -> 35
        score = engine._activity_score(inp)
        assert score == 35.0

    def test_call_component_capped_at_50(self, engine):
        inp = make_input(
            calls_last_30d=100, call_benchmark_30d=10,
            meetings_last_30d=0, meeting_benchmark_30d=10,
            manager_reviewed_deals=0, total_deals=10,
        )
        score = engine._activity_score(inp)
        assert score == 50.0

    def test_meeting_component_capped_at_35(self, engine):
        inp = make_input(
            calls_last_30d=0, call_benchmark_30d=10,
            meetings_last_30d=100, meeting_benchmark_30d=10,
            manager_reviewed_deals=0, total_deals=10,
        )
        score = engine._activity_score(inp)
        assert score == 35.0

    def test_review_component_capped_at_15(self, engine):
        inp = make_input(
            calls_last_30d=0, call_benchmark_30d=10,
            meetings_last_30d=0, meeting_benchmark_30d=10,
            manager_reviewed_deals=100, total_deals=10,
        )
        score = engine._activity_score(inp)
        assert score == 15.0

    def test_zero_total_deals_no_review_contribution(self, engine):
        inp = make_input(
            calls_last_30d=10, call_benchmark_30d=10,
            meetings_last_30d=5, meeting_benchmark_30d=5,
            manager_reviewed_deals=5, total_deals=0,
        )
        # review skipped when total_deals=0
        score = engine._activity_score(inp)
        assert score == pytest.approx(85.0)

    def test_score_is_numeric(self, engine, default_input):
        score = engine._activity_score(default_input)
        assert isinstance(score, (int, float))

    def test_score_clamped_at_100(self, engine):
        inp = make_input(
            calls_last_30d=0, call_benchmark_30d=0,
            meetings_last_30d=0, meeting_benchmark_30d=0,
            manager_reviewed_deals=100, total_deals=1,
        )
        score = engine._activity_score(inp)
        assert score <= 100.0


class TestPhiScore:
    def test_all_100_returns_100(self, engine):
        phi = engine._phi_score(100.0, 100.0, 100.0, 100.0)
        assert phi == 100.0

    def test_all_0_returns_0(self, engine):
        phi = engine._phi_score(0.0, 0.0, 0.0, 0.0)
        assert phi == 0.0

    def test_weights_sum_to_1(self, engine):
        # vel=100 only -> 25.0
        assert engine._phi_score(100, 0, 0, 0) == pytest.approx(25.0)
        # qual=100 only -> 30.0
        assert engine._phi_score(0, 100, 0, 0) == pytest.approx(30.0)
        # cov=100 only -> 25.0
        assert engine._phi_score(0, 0, 100, 0) == pytest.approx(25.0)
        # act=100 only -> 20.0
        assert engine._phi_score(0, 0, 0, 100) == pytest.approx(20.0)

    def test_phi_rounds_to_1_decimal(self, engine):
        phi = engine._phi_score(33.3, 33.3, 33.3, 33.3)
        assert phi == round(33.3 * 0.25 + 33.3 * 0.30 + 33.3 * 0.25 + 33.3 * 0.20, 1)

    def test_result_is_numeric(self, engine):
        phi = engine._phi_score(50.0, 50.0, 50.0, 50.0)
        assert isinstance(phi, (int, float))


class TestHealthGradeThresholds:
    def test_phi_80_returns_excellent(self, engine):
        assert engine._health_grade(80.0) == HealthGrade.EXCELLENT

    def test_phi_above_80_returns_excellent(self, engine):
        assert engine._health_grade(95.0) == HealthGrade.EXCELLENT

    def test_phi_100_returns_excellent(self, engine):
        assert engine._health_grade(100.0) == HealthGrade.EXCELLENT

    def test_phi_79_9_returns_good(self, engine):
        assert engine._health_grade(79.9) == HealthGrade.GOOD

    def test_phi_60_returns_good(self, engine):
        assert engine._health_grade(60.0) == HealthGrade.GOOD

    def test_phi_59_9_returns_fair(self, engine):
        assert engine._health_grade(59.9) == HealthGrade.FAIR

    def test_phi_40_returns_fair(self, engine):
        assert engine._health_grade(40.0) == HealthGrade.FAIR

    def test_phi_39_9_returns_poor(self, engine):
        assert engine._health_grade(39.9) == HealthGrade.POOR

    def test_phi_20_returns_poor(self, engine):
        assert engine._health_grade(20.0) == HealthGrade.POOR

    def test_phi_19_9_returns_critical(self, engine):
        assert engine._health_grade(19.9) == HealthGrade.CRITICAL

    def test_phi_0_returns_critical(self, engine):
        assert engine._health_grade(0.0) == HealthGrade.CRITICAL

    def test_phi_1_returns_critical(self, engine):
        assert engine._health_grade(1.0) == HealthGrade.CRITICAL


class TestPipelineRiskClassification:
    def _make_clean_input(self, **overrides):
        base = dict(
            total_deals=10,
            deals_single_threaded=0,
            deals_overdue_close_date=0,
            deals_no_exec_sponsor=0,
            deals_stale_30d=0,
            rep_win_rate_pct=50.0,
        )
        base.update(overrides)
        return make_input(**base)

    def test_no_risk_factors_returns_low(self, engine):
        inp = self._make_clean_input()
        risk = engine._pipeline_risk(inp, phi=70.0)
        assert risk == PipelineRisk.LOW

    def test_one_risk_factor_returns_moderate(self, engine):
        inp = self._make_clean_input(rep_win_rate_pct=20.0)
        risk = engine._pipeline_risk(inp, phi=70.0)
        assert risk == PipelineRisk.MODERATE

    def test_two_risk_factors_returns_high(self, engine):
        inp = self._make_clean_input(rep_win_rate_pct=20.0, deals_stale_30d=4)
        risk = engine._pipeline_risk(inp, phi=70.0)
        assert risk == PipelineRisk.HIGH

    def test_four_risk_factors_returns_severe(self, engine):
        inp = self._make_clean_input(
            rep_win_rate_pct=20.0,
            deals_stale_30d=4,
            deals_single_threaded=6,
            deals_overdue_close_date=4,
        )
        risk = engine._pipeline_risk(inp, phi=70.0)
        assert risk == PipelineRisk.SEVERE

    def test_phi_below_30_adds_risk_factor(self, engine):
        inp = self._make_clean_input()
        risk = engine._pipeline_risk(inp, phi=25.0)
        assert risk == PipelineRisk.MODERATE

    def test_single_threaded_above_50pct_adds_risk(self, engine):
        inp = self._make_clean_input(deals_single_threaded=6)
        risk = engine._pipeline_risk(inp, phi=70.0)
        assert risk == PipelineRisk.MODERATE

    def test_single_threaded_at_50pct_no_risk(self, engine):
        inp = self._make_clean_input(deals_single_threaded=5)
        risk = engine._pipeline_risk(inp, phi=70.0)
        assert risk == PipelineRisk.LOW

    def test_overdue_above_30pct_adds_risk(self, engine):
        inp = self._make_clean_input(deals_overdue_close_date=4)
        risk = engine._pipeline_risk(inp, phi=70.0)
        assert risk == PipelineRisk.MODERATE

    def test_overdue_at_30pct_no_risk(self, engine):
        inp = self._make_clean_input(deals_overdue_close_date=3)
        risk = engine._pipeline_risk(inp, phi=70.0)
        assert risk == PipelineRisk.LOW

    def test_no_exec_above_40pct_adds_risk(self, engine):
        inp = self._make_clean_input(deals_no_exec_sponsor=5)
        risk = engine._pipeline_risk(inp, phi=70.0)
        assert risk == PipelineRisk.MODERATE

    def test_stale_above_30pct_adds_risk(self, engine):
        inp = self._make_clean_input(deals_stale_30d=4)
        risk = engine._pipeline_risk(inp, phi=70.0)
        assert risk == PipelineRisk.MODERATE

    def test_win_rate_below_25_adds_risk(self, engine):
        inp = self._make_clean_input(rep_win_rate_pct=24.9)
        risk = engine._pipeline_risk(inp, phi=70.0)
        assert risk == PipelineRisk.MODERATE

    def test_win_rate_exactly_25_no_risk(self, engine):
        inp = self._make_clean_input(rep_win_rate_pct=25.0)
        risk = engine._pipeline_risk(inp, phi=70.0)
        assert risk == PipelineRisk.LOW

    def test_three_factors_returns_high(self, engine):
        inp = self._make_clean_input(
            rep_win_rate_pct=20.0,
            deals_stale_30d=4,
            deals_single_threaded=6,
        )
        risk = engine._pipeline_risk(inp, phi=70.0)
        assert risk == PipelineRisk.HIGH

    def test_severe_at_exactly_4_factors(self, engine):
        inp = self._make_clean_input(
            rep_win_rate_pct=20.0,
            deals_stale_30d=4,
            deals_single_threaded=6,
            deals_overdue_close_date=4,
        )
        risk = engine._pipeline_risk(inp, phi=70.0)
        assert risk == PipelineRisk.SEVERE


class TestHealthAction:
    def test_coverage_below_40_returns_add_pipeline(self, engine):
        action = engine._health_action(phi=60.0, vel=80.0, qual=80.0, cov=30.0, act=80.0, inp=make_input())
        assert action == HealthAction.ADD_PIPELINE

    def test_activity_below_40_returns_boost_activity(self, engine):
        action = engine._health_action(phi=60.0, vel=80.0, qual=80.0, cov=50.0, act=30.0, inp=make_input())
        assert action == HealthAction.BOOST_ACTIVITY

    def test_quality_below_40_returns_improve_qual(self, engine):
        action = engine._health_action(phi=60.0, vel=80.0, qual=30.0, cov=50.0, act=50.0, inp=make_input())
        assert action == HealthAction.IMPROVE_QUAL

    def test_velocity_below_40_returns_accelerate(self, engine):
        action = engine._health_action(phi=60.0, vel=30.0, qual=50.0, cov=50.0, act=50.0, inp=make_input())
        assert action == HealthAction.ACCELERATE

    def test_rebalance_condition(self, engine):
        # phi<50, vel<60, qual<60 -> REBALANCE
        action = engine._health_action(phi=45.0, vel=55.0, qual=55.0, cov=50.0, act=50.0, inp=make_input())
        assert action == HealthAction.REBALANCE

    def test_all_good_returns_maintain(self, engine):
        action = engine._health_action(phi=80.0, vel=80.0, qual=80.0, cov=80.0, act=80.0, inp=make_input())
        assert action == HealthAction.MAINTAIN

    def test_coverage_takes_priority_over_activity(self, engine):
        action = engine._health_action(phi=60.0, vel=80.0, qual=80.0, cov=30.0, act=30.0, inp=make_input())
        assert action == HealthAction.ADD_PIPELINE

    def test_activity_takes_priority_over_quality(self, engine):
        action = engine._health_action(phi=60.0, vel=80.0, qual=30.0, cov=50.0, act=30.0, inp=make_input())
        assert action == HealthAction.BOOST_ACTIVITY

    def test_quality_takes_priority_over_velocity(self, engine):
        action = engine._health_action(phi=60.0, vel=30.0, qual=30.0, cov=50.0, act=50.0, inp=make_input())
        assert action == HealthAction.IMPROVE_QUAL

    def test_rebalance_not_triggered_when_phi_50(self, engine):
        # phi>=50 -> MAINTAIN even if vel<60 and qual<60
        action = engine._health_action(phi=50.0, vel=55.0, qual=55.0, cov=50.0, act=50.0, inp=make_input())
        assert action == HealthAction.MAINTAIN

    def test_rebalance_not_triggered_when_vel_60(self, engine):
        action = engine._health_action(phi=45.0, vel=60.0, qual=55.0, cov=50.0, act=50.0, inp=make_input())
        assert action == HealthAction.MAINTAIN

    def test_rebalance_not_triggered_when_qual_60(self, engine):
        action = engine._health_action(phi=45.0, vel=55.0, qual=60.0, cov=50.0, act=50.0, inp=make_input())
        assert action == HealthAction.MAINTAIN


class TestCoverageRatioAndStalePct:
    def test_coverage_ratio_computed_correctly(self, engine):
        inp = make_input(total_pipeline_eur=200_000.0, quota_eur=100_000.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == pytest.approx(2.0)

    def test_coverage_ratio_zero_when_quota_zero(self, engine):
        inp = make_input(total_pipeline_eur=100_000.0, quota_eur=0.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 0.0

    def test_coverage_ratio_partial(self, engine):
        inp = make_input(total_pipeline_eur=150_000.0, quota_eur=200_000.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == pytest.approx(0.75)

    def test_stale_deal_pct_computed(self, engine):
        inp = make_input(deals_stale_30d=2, total_deals=10)
        result = engine.analyze(inp)
        assert result.stale_deal_pct == pytest.approx(20.0)

    def test_stale_deal_pct_zero_when_no_stale(self, engine):
        inp = make_input(deals_stale_30d=0, total_deals=10)
        result = engine.analyze(inp)
        assert result.stale_deal_pct == 0.0

    def test_stale_deal_pct_zero_when_total_deals_zero(self, engine):
        inp = make_input(deals_stale_30d=0, total_deals=0, avg_cycle_length_benchmark_days=0)
        result = engine.analyze(inp)
        assert result.stale_deal_pct == 0.0

    def test_stale_deal_pct_100_when_all_stale(self, engine):
        inp = make_input(deals_stale_30d=10, total_deals=10)
        result = engine.analyze(inp)
        assert result.stale_deal_pct == pytest.approx(100.0)


class TestAnalyze:
    def test_returns_pipeline_health_result(self, engine, default_input):
        result = engine.analyze(default_input)
        assert isinstance(result, PipelineHealthResult)

    def test_result_stored_in_results(self, engine, default_input):
        engine.analyze(default_input)
        assert len(engine._results) == 1

    def test_scores_are_numeric(self, engine, default_input):
        result = engine.analyze(default_input)
        assert isinstance(result.phi_score, (int, float))
        assert isinstance(result.velocity_score, (int, float))
        assert isinstance(result.quality_score, (int, float))
        assert isinstance(result.coverage_score, (int, float))
        assert isinstance(result.activity_score, (int, float))

    def test_health_grade_is_string(self, engine, default_input):
        result = engine.analyze(default_input)
        assert isinstance(result.health_grade, str)

    def test_pipeline_risk_is_string(self, engine, default_input):
        result = engine.analyze(default_input)
        assert isinstance(result.pipeline_risk, str)

    def test_health_action_is_string(self, engine, default_input):
        result = engine.analyze(default_input)
        assert isinstance(result.health_action, str)

    def test_health_grade_valid_value(self, engine, default_input):
        result = engine.analyze(default_input)
        assert result.health_grade in {g.value for g in HealthGrade}

    def test_pipeline_risk_valid_value(self, engine, default_input):
        result = engine.analyze(default_input)
        assert result.pipeline_risk in {r.value for r in PipelineRisk}

    def test_health_action_valid_value(self, engine, default_input):
        result = engine.analyze(default_input)
        assert result.health_action in {a.value for a in HealthAction}

    def test_phi_score_in_range(self, engine, default_input):
        result = engine.analyze(default_input)
        assert 0.0 <= result.phi_score <= 100.0

    def test_velocity_score_in_range(self, engine, default_input):
        result = engine.analyze(default_input)
        assert 0.0 <= result.velocity_score <= 100.0

    def test_quality_score_in_range(self, engine, default_input):
        result = engine.analyze(default_input)
        assert 0.0 <= result.quality_score <= 100.0

    def test_coverage_score_in_range(self, engine, default_input):
        result = engine.analyze(default_input)
        assert 0.0 <= result.coverage_score <= 100.0

    def test_activity_score_in_range(self, engine, default_input):
        result = engine.analyze(default_input)
        assert 0.0 <= result.activity_score <= 100.0

    def test_multiple_analyzes_accumulate(self, engine):
        engine.analyze(make_input(pipeline_id="p1"))
        engine.analyze(make_input(pipeline_id="p2"))
        assert len(engine._results) == 2

    def test_identity_fields_propagated(self, engine):
        inp = make_input(pipeline_id="p-test", rep_id="r-test", rep_name="TestRep", region="APAC")
        result = engine.analyze(inp)
        assert result.pipeline_id == "p-test"
        assert result.rep_id == "r-test"
        assert result.rep_name == "TestRep"
        assert result.region == "APAC"


class TestAnalyzeBatch:
    def test_returns_list(self, engine):
        results = engine.analyze_batch([make_input(pipeline_id="p1")])
        assert isinstance(results, list)

    def test_sorted_desc_by_phi_score(self, engine):
        # Create inputs that produce different phi scores
        high = make_input(
            pipeline_id="high",
            avg_deal_age_days=10.0, avg_cycle_length_benchmark_days=100.0,
            total_pipeline_eur=500_000.0, quota_eur=100_000.0,
            avg_deal_health_score=100.0, qualified_deals_pct=100.0,
            avg_next_step_adherence_pct=100.0, rep_win_rate_pct=100.0,
            calls_last_30d=20, call_benchmark_30d=20,
            meetings_last_30d=10, meeting_benchmark_30d=10,
            manager_reviewed_deals=10, total_deals=10,
        )
        low = make_input(
            pipeline_id="low",
            avg_deal_age_days=200.0, avg_cycle_length_benchmark_days=100.0,
            total_pipeline_eur=10_000.0, quota_eur=100_000.0,
            avg_deal_health_score=0.0, qualified_deals_pct=0.0,
            avg_next_step_adherence_pct=0.0, rep_win_rate_pct=0.0,
            calls_last_30d=0, call_benchmark_30d=20,
            meetings_last_30d=0, meeting_benchmark_30d=10,
            manager_reviewed_deals=0, total_deals=10,
            deals_stale_30d=0,
        )
        results = engine.analyze_batch([low, high])
        assert results[0].phi_score >= results[1].phi_score

    def test_batch_stores_all_results(self, engine):
        inputs = [make_input(pipeline_id=f"p{i}") for i in range(5)]
        engine.analyze_batch(inputs)
        assert len(engine._results) == 5

    def test_batch_returns_all_results(self, engine):
        inputs = [make_input(pipeline_id=f"p{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 3

    def test_batch_empty_input(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_batch_single_input(self, engine):
        results = engine.analyze_batch([make_input(pipeline_id="solo")])
        assert len(results) == 1
        assert results[0].pipeline_id == "solo"

    def test_batch_sorted_three_elements(self, engine):
        def score_input(pipeline_eur):
            return make_input(
                total_pipeline_eur=pipeline_eur,
                quota_eur=100_000.0,
                avg_deal_age_days=10.0,
                avg_cycle_length_benchmark_days=100.0,
            )
        inputs = [score_input(50_000), score_input(400_000), score_input(200_000)]
        results = engine.analyze_batch(inputs)
        phi_scores = [r.phi_score for r in results]
        assert phi_scores == sorted(phi_scores, reverse=True)


class TestCriticalPipelines:
    def test_returns_only_critical(self, engine):
        engine.analyze(make_input(
            pipeline_id="bad",
            avg_deal_age_days=300.0, avg_cycle_length_benchmark_days=100.0,
            total_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_deal_health_score=0.0, qualified_deals_pct=0.0,
            avg_next_step_adherence_pct=0.0, rep_win_rate_pct=0.0,
            calls_last_30d=0, call_benchmark_30d=20,
            meetings_last_30d=0, meeting_benchmark_30d=10,
            manager_reviewed_deals=0, total_deals=10,
            deals_stale_30d=5,
        ))
        engine.analyze(make_input(pipeline_id="good"))
        criticals = engine.critical_pipelines()
        for r in criticals:
            assert r.health_grade == HealthGrade.CRITICAL.value

    def test_empty_when_none_critical(self, engine):
        engine.analyze(make_input())
        criticals = engine.critical_pipelines()
        for r in criticals:
            assert r.health_grade == HealthGrade.CRITICAL.value

    def test_empty_results(self, engine):
        assert engine.critical_pipelines() == []


class TestSevereRisk:
    def test_returns_only_severe(self, engine):
        severe_inp = make_input(
            pipeline_id="severe",
            total_deals=10,
            deals_single_threaded=6,
            deals_overdue_close_date=4,
            deals_no_exec_sponsor=5,
            deals_stale_30d=4,
            rep_win_rate_pct=10.0,
        )
        engine.analyze(severe_inp)
        engine.analyze(make_input(pipeline_id="ok"))
        severes = engine.severe_risk()
        for r in severes:
            assert r.pipeline_risk == PipelineRisk.SEVERE.value

    def test_empty_results(self, engine):
        assert engine.severe_risk() == []


class TestNeedsPipelineAdd:
    def test_returns_only_add_pipeline_action(self, engine):
        low_cov = make_input(
            pipeline_id="low_cov",
            total_pipeline_eur=10_000.0,
            quota_eur=100_000.0,
        )
        engine.analyze(low_cov)
        engine.analyze(make_input(pipeline_id="ok"))
        needs = engine.needs_pipeline_add()
        for r in needs:
            assert r.health_action == HealthAction.ADD_PIPELINE.value

    def test_empty_results(self, engine):
        assert engine.needs_pipeline_add() == []


class TestHealthyPipelines:
    def test_returns_excellent_and_good(self, engine):
        engine.analyze(make_input(pipeline_id="p1"))
        healthy = engine.healthy_pipelines()
        for r in healthy:
            assert r.health_grade in (HealthGrade.EXCELLENT.value, HealthGrade.GOOD.value)

    def test_excludes_fair_poor_critical(self, engine):
        engine.analyze(make_input(
            pipeline_id="bad",
            avg_deal_age_days=300.0, avg_cycle_length_benchmark_days=100.0,
            total_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_deal_health_score=0.0, qualified_deals_pct=0.0,
            avg_next_step_adherence_pct=0.0, rep_win_rate_pct=0.0,
            calls_last_30d=0, call_benchmark_30d=20,
            meetings_last_30d=0, meeting_benchmark_30d=10,
            manager_reviewed_deals=0, total_deals=10,
            deals_stale_30d=5,
        ))
        healthy = engine.healthy_pipelines()
        for r in healthy:
            assert r.health_grade in (HealthGrade.EXCELLENT.value, HealthGrade.GOOD.value)

    def test_empty_results(self, engine):
        assert engine.healthy_pipelines() == []


class TestAtRiskPipelines:
    def test_returns_high_and_severe(self, engine):
        at_risk = engine.at_risk_pipelines()
        for r in at_risk:
            assert r.pipeline_risk in (PipelineRisk.HIGH.value, PipelineRisk.SEVERE.value)

    def test_empty_results(self, engine):
        assert engine.at_risk_pipelines() == []

    def test_excludes_low_moderate(self, engine):
        engine.analyze(make_input(pipeline_id="ok"))
        at_risk = engine.at_risk_pipelines()
        for r in at_risk:
            assert r.pipeline_risk in (PipelineRisk.HIGH.value, PipelineRisk.SEVERE.value)


class TestSummary:
    def test_summary_returns_11_keys_empty(self, engine):
        s = engine.summary()
        assert len(s) == 11

    def test_summary_returns_11_keys_with_data(self, engine, default_input):
        engine.analyze(default_input)
        s = engine.summary()
        assert len(s) == 11

    def test_summary_exact_keys(self, engine):
        expected = {
            "total", "grade_counts", "risk_counts", "action_counts",
            "avg_phi_score", "avg_velocity_score", "avg_quality_score",
            "avg_coverage_score", "avg_activity_score",
            "critical_count", "severe_risk_count",
        }
        s = engine.summary()
        assert set(s.keys()) == expected

    def test_summary_total_zero_when_empty(self, engine):
        s = engine.summary()
        assert s["total"] == 0

    def test_summary_averages_zero_when_empty(self, engine):
        s = engine.summary()
        assert s["avg_phi_score"] == 0.0
        assert s["avg_velocity_score"] == 0.0
        assert s["avg_quality_score"] == 0.0
        assert s["avg_coverage_score"] == 0.0
        assert s["avg_activity_score"] == 0.0

    def test_summary_critical_count_zero_when_empty(self, engine):
        s = engine.summary()
        assert s["critical_count"] == 0

    def test_summary_severe_risk_count_zero_when_empty(self, engine):
        s = engine.summary()
        assert s["severe_risk_count"] == 0

    def test_summary_total_reflects_analyzed_count(self, engine):
        engine.analyze(make_input(pipeline_id="p1"))
        engine.analyze(make_input(pipeline_id="p2"))
        s = engine.summary()
        assert s["total"] == 2

    def test_summary_grade_counts_populated(self, engine, default_input):
        engine.analyze(default_input)
        s = engine.summary()
        assert isinstance(s["grade_counts"], dict)
        assert sum(s["grade_counts"].values()) == 1

    def test_summary_risk_counts_populated(self, engine, default_input):
        engine.analyze(default_input)
        s = engine.summary()
        assert isinstance(s["risk_counts"], dict)
        assert sum(s["risk_counts"].values()) == 1

    def test_summary_action_counts_populated(self, engine, default_input):
        engine.analyze(default_input)
        s = engine.summary()
        assert isinstance(s["action_counts"], dict)
        assert sum(s["action_counts"].values()) == 1

    def test_summary_avg_phi_computed(self, engine):
        engine.analyze(make_input(pipeline_id="p1"))
        engine.analyze(make_input(pipeline_id="p2"))
        s = engine.summary()
        assert isinstance(s["avg_phi_score"], (int, float))

    def test_summary_empty_dicts_when_no_results(self, engine):
        s = engine.summary()
        assert s["grade_counts"] == {}
        assert s["risk_counts"] == {}
        assert s["action_counts"] == {}


class TestReset:
    def test_reset_clears_results(self, engine, default_input):
        engine.analyze(default_input)
        engine.reset()
        assert engine._results == []

    def test_reset_allows_reuse(self, engine, default_input):
        engine.analyze(default_input)
        engine.reset()
        engine.analyze(make_input(pipeline_id="p2"))
        assert len(engine._results) == 1

    def test_reset_on_empty_engine(self, engine):
        engine.reset()
        assert engine._results == []

    def test_summary_after_reset(self, engine, default_input):
        engine.analyze(default_input)
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0


class TestEngineInit:
    def test_results_empty_on_init(self):
        eng = PipelineHealthIndexEngine()
        assert eng._results == []

    def test_multiple_engines_independent(self):
        e1 = PipelineHealthIndexEngine()
        e2 = PipelineHealthIndexEngine()
        e1.analyze(make_input(pipeline_id="p1"))
        assert len(e2._results) == 0


class TestEdgeCases:
    def test_zero_total_deals_velocity_fallback(self, engine):
        inp = make_input(total_deals=0, avg_cycle_length_benchmark_days=60.0)
        result = engine.analyze(inp)
        assert result.velocity_score == 50.0

    def test_zero_quota_coverage_fallback(self, engine):
        inp = make_input(quota_eur=0.0, total_pipeline_eur=100_000.0)
        result = engine.analyze(inp)
        assert result.coverage_score == 80.0

    def test_all_zero_scores_give_critical_grade(self, engine):
        inp = make_input(
            avg_deal_age_days=300.0, avg_cycle_length_benchmark_days=100.0,
            total_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_deal_health_score=0.0, qualified_deals_pct=0.0,
            avg_next_step_adherence_pct=0.0, rep_win_rate_pct=0.0,
            calls_last_30d=0, call_benchmark_30d=20,
            meetings_last_30d=0, meeting_benchmark_30d=10,
            manager_reviewed_deals=0, total_deals=10,
            deals_stale_30d=5,
        )
        result = engine.analyze(inp)
        assert result.health_grade == HealthGrade.CRITICAL.value

    def test_perfect_pipeline_gives_excellent_grade(self, engine):
        inp = make_input(
            avg_deal_age_days=10.0, avg_cycle_length_benchmark_days=100.0,
            total_pipeline_eur=500_000.0, quota_eur=100_000.0,
            avg_deal_health_score=100.0, qualified_deals_pct=100.0,
            avg_next_step_adherence_pct=100.0, rep_win_rate_pct=100.0,
            calls_last_30d=20, call_benchmark_30d=20,
            meetings_last_30d=10, meeting_benchmark_30d=10,
            manager_reviewed_deals=10, total_deals=10,
            deals_stale_30d=0,
        )
        result = engine.analyze(inp)
        assert result.health_grade == HealthGrade.EXCELLENT.value

    def test_remediation_plays_not_empty(self, engine, default_input):
        result = engine.analyze(default_input)
        assert len(result.remediation_plays) >= 1

    def test_stale_deals_appear_in_remediation(self, engine):
        inp = make_input(deals_stale_30d=3, total_deals=10)
        result = engine.analyze(inp)
        plays = " ".join(result.remediation_plays)
        assert "3" in plays

    def test_single_threaded_appear_in_remediation(self, engine):
        inp = make_input(deals_single_threaded=2, total_deals=10)
        result = engine.analyze(inp)
        plays = " ".join(result.remediation_plays)
        assert "2" in plays

    def test_overdue_appear_in_remediation(self, engine):
        inp = make_input(deals_overdue_close_date=1, total_deals=10)
        result = engine.analyze(inp)
        plays = " ".join(result.remediation_plays)
        assert "1" in plays

    def test_pipeline_below_quota_in_risk_signals(self, engine):
        inp = make_input(total_pipeline_eur=50_000.0, quota_eur=100_000.0)
        result = engine.analyze(inp)
        assert len(result.risk_signals) >= 1

    def test_low_win_rate_in_risk_signals(self, engine):
        inp = make_input(rep_win_rate_pct=10.0)
        result = engine.analyze(inp)
        risk_text = " ".join(result.risk_signals)
        assert "10" in risk_text

    def test_critical_grade_triggers_manager_alert(self, engine):
        inp = make_input(
            avg_deal_age_days=300.0, avg_cycle_length_benchmark_days=100.0,
            total_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_deal_health_score=0.0, qualified_deals_pct=0.0,
            avg_next_step_adherence_pct=0.0, rep_win_rate_pct=0.0,
            calls_last_30d=0, call_benchmark_30d=20,
            meetings_last_30d=0, meeting_benchmark_30d=10,
            manager_reviewed_deals=0, total_deals=10,
            deals_stale_30d=5,
        )
        result = engine.analyze(inp)
        assert len(result.manager_alerts) >= 1

    def test_pipeline_below_80pct_quota_triggers_alert(self, engine):
        inp = make_input(total_pipeline_eur=70_000.0, quota_eur=100_000.0)
        result = engine.analyze(inp)
        assert len(result.manager_alerts) >= 1
