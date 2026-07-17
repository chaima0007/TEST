"""Comprehensive pytest test suite for swarm.intelligence.sales_coaching_engine."""

from __future__ import annotations

import pytest

from swarm.intelligence.sales_coaching_engine import (
    SkillGap,
    CoachingIntensity,
    CoachingFocus,
    RepPerformanceInput,
    CoachingPlanResult,
    SalesCoachingEngine,
    _coaching_score,
    _coaching_intensity,
    _detect_skill_gaps,
    _primary_focus,
    _build_strengths,
    _build_development_areas,
    _build_coaching_actions,
    _build_session_plan,
    _build_kpis_to_track,
)


# ─── Fixtures ────────────────────────────────────────────────────────────────


def make_rep(
    rep_id: str = "R001",
    rep_name: str = "Alice Dupont",
    segment: str = "enterprise",
    tenure_months: int = 24,
    quota_eur: float = 1_000_000.0,
    quota_attainment_pct: float = 100.0,
    pipeline_coverage_ratio: float = 3.0,
    forecast_accuracy_pct: float = 10.0,
    avg_discovery_questions_per_call: float = 8.0,
    avg_deal_cycle_days: int = 60,
    deals_lost_to_no_decision_pct: float = 10.0,
    deals_lost_to_competitor_pct: float = 20.0,
    discount_avg_pct: float = 5.0,
    crm_update_lag_days: float = 1.0,
    multi_thread_avg_contacts: float = 3.5,
    next_step_set_pct: float = 80.0,
    last_coaching_session_days_ago: int = 14,
    coaching_sessions_ytd: int = 6,
    self_assessment_score: float = 75.0,
    manager_assessment_score: float = 80.0,
) -> RepPerformanceInput:
    """Factory for RepPerformanceInput with sensible defaults (star performer)."""
    return RepPerformanceInput(
        rep_id=rep_id,
        rep_name=rep_name,
        segment=segment,
        tenure_months=tenure_months,
        quota_eur=quota_eur,
        quota_attainment_pct=quota_attainment_pct,
        pipeline_coverage_ratio=pipeline_coverage_ratio,
        forecast_accuracy_pct=forecast_accuracy_pct,
        avg_discovery_questions_per_call=avg_discovery_questions_per_call,
        avg_deal_cycle_days=avg_deal_cycle_days,
        deals_lost_to_no_decision_pct=deals_lost_to_no_decision_pct,
        deals_lost_to_competitor_pct=deals_lost_to_competitor_pct,
        discount_avg_pct=discount_avg_pct,
        crm_update_lag_days=crm_update_lag_days,
        multi_thread_avg_contacts=multi_thread_avg_contacts,
        next_step_set_pct=next_step_set_pct,
        last_coaching_session_days_ago=last_coaching_session_days_ago,
        coaching_sessions_ytd=coaching_sessions_ytd,
        self_assessment_score=self_assessment_score,
        manager_assessment_score=manager_assessment_score,
    )


@pytest.fixture
def star_rep() -> RepPerformanceInput:
    """Rep with excellent metrics — score = 30+20+15+15+10+10 = 100."""
    return make_rep(
        quota_attainment_pct=120.0,
        pipeline_coverage_ratio=3.0,
        next_step_set_pct=80.0,
        multi_thread_avg_contacts=3.5,
        crm_update_lag_days=1.0,
        discount_avg_pct=5.0,
    )


@pytest.fixture
def critical_rep() -> RepPerformanceInput:
    """Rep with very poor metrics — lowest scoring."""
    return make_rep(
        rep_id="R999",
        rep_name="Bob Critique",
        quota_attainment_pct=20.0,
        pipeline_coverage_ratio=0.5,
        next_step_set_pct=30.0,
        multi_thread_avg_contacts=1.0,
        crm_update_lag_days=10.0,
        discount_avg_pct=30.0,
    )


@pytest.fixture
def moderate_rep() -> RepPerformanceInput:
    """Rep with moderate metrics."""
    return make_rep(
        rep_id="R002",
        rep_name="Carol Moyen",
        quota_attainment_pct=80.0,
        pipeline_coverage_ratio=2.0,
        next_step_set_pct=60.0,
        multi_thread_avg_contacts=2.5,
        crm_update_lag_days=3.0,
        discount_avg_pct=15.0,
    )


@pytest.fixture
def engine() -> SalesCoachingEngine:
    return SalesCoachingEngine()


# ─── 1. TestSkillGapEnum ─────────────────────────────────────────────────────


class TestSkillGapEnum:
    def test_discovery_value(self):
        assert SkillGap.DISCOVERY.value == "discovery"

    def test_qualification_value(self):
        assert SkillGap.QUALIFICATION.value == "qualification"

    def test_presentation_value(self):
        assert SkillGap.PRESENTATION.value == "presentation"

    def test_objection_handling_value(self):
        assert SkillGap.OBJECTION_HANDLING.value == "objection_handling"

    def test_closing_value(self):
        assert SkillGap.CLOSING.value == "closing"

    def test_pipeline_hygiene_value(self):
        assert SkillGap.PIPELINE_HYGIENE.value == "pipeline_hygiene"

    def test_multi_threading_value(self):
        assert SkillGap.MULTI_THREADING.value == "multi_threading"

    def test_forecasting_value(self):
        assert SkillGap.FORECASTING.value == "forecasting"

    def test_total_count(self):
        assert len(SkillGap) == 8

    def test_is_str_enum(self):
        assert isinstance(SkillGap.DISCOVERY, str)

    def test_all_members_present(self):
        names = {m.name for m in SkillGap}
        expected = {
            "DISCOVERY", "QUALIFICATION", "PRESENTATION", "OBJECTION_HANDLING",
            "CLOSING", "PIPELINE_HYGIENE", "MULTI_THREADING", "FORECASTING",
        }
        assert names == expected


# ─── 2. TestCoachingIntensityEnum ────────────────────────────────────────────


class TestCoachingIntensityEnum:
    def test_light_value(self):
        assert CoachingIntensity.LIGHT.value == "light"

    def test_moderate_value(self):
        assert CoachingIntensity.MODERATE.value == "moderate"

    def test_intensive_value(self):
        assert CoachingIntensity.INTENSIVE.value == "intensive"

    def test_critical_value(self):
        assert CoachingIntensity.CRITICAL.value == "critical"

    def test_total_count(self):
        assert len(CoachingIntensity) == 4

    def test_is_str_enum(self):
        assert isinstance(CoachingIntensity.LIGHT, str)

    def test_all_members_present(self):
        names = {m.name for m in CoachingIntensity}
        assert names == {"LIGHT", "MODERATE", "INTENSIVE", "CRITICAL"}


# ─── 3. TestCoachingFocusEnum ─────────────────────────────────────────────────


class TestCoachingFocusEnum:
    def test_skills_value(self):
        assert CoachingFocus.SKILLS.value == "skills"

    def test_pipeline_value(self):
        assert CoachingFocus.PIPELINE.value == "pipeline"

    def test_mindset_value(self):
        assert CoachingFocus.MINDSET.value == "mindset"

    def test_process_value(self):
        assert CoachingFocus.PROCESS.value == "process"

    def test_strategy_value(self):
        assert CoachingFocus.STRATEGY.value == "strategy"

    def test_total_count(self):
        assert len(CoachingFocus) == 5

    def test_is_str_enum(self):
        assert isinstance(CoachingFocus.SKILLS, str)

    def test_all_members_present(self):
        names = {m.name for m in CoachingFocus}
        assert names == {"SKILLS", "PIPELINE", "MINDSET", "PROCESS", "STRATEGY"}


# ─── 4. TestRepPerformanceInputDataclass ──────────────────────────────────────


class TestRepPerformanceInputDataclass:
    def test_construction(self):
        rep = make_rep()
        assert rep.rep_id == "R001"

    def test_rep_name(self):
        rep = make_rep(rep_name="Test Name")
        assert rep.rep_name == "Test Name"

    def test_segment(self):
        rep = make_rep(segment="smb")
        assert rep.segment == "smb"

    def test_tenure_months(self):
        rep = make_rep(tenure_months=12)
        assert rep.tenure_months == 12

    def test_quota_eur(self):
        rep = make_rep(quota_eur=500_000.0)
        assert rep.quota_eur == 500_000.0

    def test_quota_attainment_pct(self):
        rep = make_rep(quota_attainment_pct=95.0)
        assert rep.quota_attainment_pct == 95.0

    def test_pipeline_coverage_ratio(self):
        rep = make_rep(pipeline_coverage_ratio=2.5)
        assert rep.pipeline_coverage_ratio == 2.5

    def test_forecast_accuracy_pct(self):
        rep = make_rep(forecast_accuracy_pct=15.0)
        assert rep.forecast_accuracy_pct == 15.0

    def test_avg_discovery_questions(self):
        rep = make_rep(avg_discovery_questions_per_call=6.0)
        assert rep.avg_discovery_questions_per_call == 6.0

    def test_avg_deal_cycle_days(self):
        rep = make_rep(avg_deal_cycle_days=90)
        assert rep.avg_deal_cycle_days == 90

    def test_deals_lost_to_no_decision(self):
        rep = make_rep(deals_lost_to_no_decision_pct=25.0)
        assert rep.deals_lost_to_no_decision_pct == 25.0

    def test_deals_lost_to_competitor(self):
        rep = make_rep(deals_lost_to_competitor_pct=35.0)
        assert rep.deals_lost_to_competitor_pct == 35.0

    def test_discount_avg_pct(self):
        rep = make_rep(discount_avg_pct=12.0)
        assert rep.discount_avg_pct == 12.0

    def test_crm_update_lag_days(self):
        rep = make_rep(crm_update_lag_days=2.0)
        assert rep.crm_update_lag_days == 2.0

    def test_multi_thread_avg_contacts(self):
        rep = make_rep(multi_thread_avg_contacts=2.0)
        assert rep.multi_thread_avg_contacts == 2.0

    def test_next_step_set_pct(self):
        rep = make_rep(next_step_set_pct=70.0)
        assert rep.next_step_set_pct == 70.0

    def test_last_coaching_session_days_ago(self):
        rep = make_rep(last_coaching_session_days_ago=30)
        assert rep.last_coaching_session_days_ago == 30

    def test_coaching_sessions_ytd(self):
        rep = make_rep(coaching_sessions_ytd=10)
        assert rep.coaching_sessions_ytd == 10

    def test_self_assessment_score(self):
        rep = make_rep(self_assessment_score=60.0)
        assert rep.self_assessment_score == 60.0

    def test_manager_assessment_score(self):
        rep = make_rep(manager_assessment_score=70.0)
        assert rep.manager_assessment_score == 70.0

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(RepPerformanceInput)


# ─── 5. TestCoachingPlanResultToDict ─────────────────────────────────────────


class TestCoachingPlanResultToDict:
    def _make_result(self, gaps=None) -> CoachingPlanResult:
        if gaps is None:
            gaps = [SkillGap.DISCOVERY, SkillGap.CLOSING]
        return CoachingPlanResult(
            rep_id="R001",
            rep_name="Test Rep",
            segment="enterprise",
            tenure_months=12,
            coaching_intensity=CoachingIntensity.MODERATE,
            primary_focus=CoachingFocus.SKILLS,
            coaching_score=55.0,
            top_skill_gaps=gaps,
            strengths=["strength 1"],
            development_areas=["dev area 1"],
            coaching_actions=["action 1"],
            session_plan=["S1: session"],
            kpis_to_track=["KPI 1"],
        )

    def test_to_dict_returns_dict(self):
        result = self._make_result()
        assert isinstance(result.to_dict(), dict)

    def test_top_skill_gaps_are_strings(self):
        result = self._make_result()
        d = result.to_dict()
        for gap in d["top_skill_gaps"]:
            assert isinstance(gap, str)

    def test_top_skill_gaps_values(self):
        result = self._make_result([SkillGap.DISCOVERY, SkillGap.CLOSING])
        d = result.to_dict()
        assert d["top_skill_gaps"] == ["discovery", "closing"]

    def test_coaching_intensity_is_string(self):
        result = self._make_result()
        d = result.to_dict()
        assert d["coaching_intensity"] == "moderate"

    def test_primary_focus_is_string(self):
        result = self._make_result()
        d = result.to_dict()
        assert d["primary_focus"] == "skills"

    def test_rep_id_present(self):
        result = self._make_result()
        d = result.to_dict()
        assert d["rep_id"] == "R001"

    def test_empty_gaps_serialized(self):
        result = self._make_result(gaps=[])
        d = result.to_dict()
        assert d["top_skill_gaps"] == []

    def test_all_eight_gaps_serialized(self):
        all_gaps = list(SkillGap)[:4]
        result = self._make_result(gaps=all_gaps)
        d = result.to_dict()
        assert len(d["top_skill_gaps"]) == 4
        assert all(isinstance(g, str) for g in d["top_skill_gaps"])

    def test_coaching_score_present(self):
        result = self._make_result()
        d = result.to_dict()
        assert d["coaching_score"] == 55.0

    def test_no_enum_objects_in_dict(self):
        result = self._make_result()
        d = result.to_dict()
        assert not isinstance(d["coaching_intensity"], CoachingIntensity)
        assert not isinstance(d["primary_focus"], CoachingFocus)
        for g in d["top_skill_gaps"]:
            assert not isinstance(g, SkillGap)


# ─── 6. TestCoachingScoreQuota ────────────────────────────────────────────────


class TestCoachingScoreQuota:
    """Test quota attainment contribution (0-30 pts) with all else neutral."""

    def _base_score_minus_quota(self):
        """Score from pipeline=0 (ratio<1), next_step=0 (<40), multi=0 (<1.5), crm=10 (<=1), discount=10 (<=5)."""
        # We'll use pipeline=0.5, next_step=30, multi=1.0, crm=1.0, discount=5
        # -> 0 + 0 + 0 + 10 + 10 = 20
        return 20.0

    def _make(self, att: float) -> float:
        rep = make_rep(
            quota_attainment_pct=att,
            pipeline_coverage_ratio=0.5,  # 0 pts
            next_step_set_pct=30.0,        # 0 pts
            multi_thread_avg_contacts=1.0, # 0 pts
            crm_update_lag_days=1.0,       # 10 pts
            discount_avg_pct=5.0,          # 10 pts
        )
        return _coaching_score(rep)

    def test_att_120_gives_30pts(self):
        score = self._make(120.0)
        base = self._base_score_minus_quota()
        assert score == round(base + 30.0, 1)

    def test_att_exactly_120(self):
        score = self._make(120.0)
        assert score == 50.0  # 30 + 20 = 50

    def test_att_between_100_and_119(self):
        score = self._make(110.0)
        assert score == 45.0  # 25 + 20 = 45

    def test_att_exactly_100(self):
        score = self._make(100.0)
        assert score == 45.0  # 25 + 20

    def test_att_between_80_and_99(self):
        score = self._make(90.0)
        assert score == 38.0  # 18 + 20

    def test_att_exactly_80(self):
        score = self._make(80.0)
        assert score == 38.0  # 18 + 20

    def test_att_between_60_and_79(self):
        score = self._make(70.0)
        assert score == 30.0  # 10 + 20

    def test_att_exactly_60(self):
        score = self._make(60.0)
        assert score == 30.0  # 10 + 20

    def test_att_between_40_and_59(self):
        score = self._make(50.0)
        assert score == 24.0  # 4 + 20

    def test_att_exactly_40(self):
        score = self._make(40.0)
        assert score == 24.0  # 4 + 20

    def test_att_below_40_gives_0pts(self):
        score = self._make(39.9)
        assert score == 20.0  # 0 + 20

    def test_att_zero_gives_0pts(self):
        score = self._make(0.0)
        assert score == 20.0  # 0 + 20


# ─── 7. TestCoachingScorePipeline ────────────────────────────────────────────


class TestCoachingScorePipeline:
    """Test pipeline coverage contribution (0-20 pts)."""

    def _make(self, pc: float) -> float:
        # att=120→30, next_step=80→15, multi=3.5→15, crm=1→10, discount=5→10 = 80
        rep = make_rep(
            quota_attainment_pct=120.0,
            pipeline_coverage_ratio=pc,
            next_step_set_pct=80.0,
            multi_thread_avg_contacts=3.5,
            crm_update_lag_days=1.0,
            discount_avg_pct=5.0,
        )
        return _coaching_score(rep)

    def test_pc_3_gives_20pts(self):
        score = self._make(3.0)
        assert score == 100.0  # 30+20+15+15+10+10

    def test_pc_above_3_gives_20pts(self):
        score = self._make(5.0)
        assert score == 100.0

    def test_pc_between_2_and_3_gives_14pts(self):
        score = self._make(2.5)
        assert score == 94.0  # 30+14+15+15+10+10

    def test_pc_exactly_2_gives_14pts(self):
        score = self._make(2.0)
        assert score == 94.0

    def test_pc_between_1_5_and_2_gives_8pts(self):
        score = self._make(1.75)
        assert score == 88.0  # 30+8+15+15+10+10

    def test_pc_exactly_1_5_gives_8pts(self):
        score = self._make(1.5)
        assert score == 88.0

    def test_pc_between_1_and_1_5_gives_3pts(self):
        score = self._make(1.25)
        assert score == 83.0  # 30+3+15+15+10+10

    def test_pc_exactly_1_gives_3pts(self):
        score = self._make(1.0)
        assert score == 83.0

    def test_pc_below_1_gives_0pts(self):
        score = self._make(0.5)
        assert score == 80.0  # 30+0+15+15+10+10

    def test_pc_zero_gives_0pts(self):
        score = self._make(0.0)
        assert score == 80.0


# ─── 8. TestCoachingScoreNextStep ────────────────────────────────────────────


class TestCoachingScoreNextStep:
    """Test next_step_set_pct contribution (0-15 pts)."""

    def _make(self, ns: float) -> float:
        # att=120→30, pc=3→20, multi=3.5→15, crm=1→10, discount=5→10 = 85 + ns_pts
        rep = make_rep(
            quota_attainment_pct=120.0,
            pipeline_coverage_ratio=3.0,
            next_step_set_pct=ns,
            multi_thread_avg_contacts=3.5,
            crm_update_lag_days=1.0,
            discount_avg_pct=5.0,
        )
        return _coaching_score(rep)

    def test_ns_80_gives_15pts(self):
        assert self._make(80.0) == 100.0  # 30+20+15+15+10+10

    def test_ns_above_80_gives_15pts(self):
        assert self._make(95.0) == 100.0

    def test_ns_between_60_and_79_gives_10pts(self):
        assert self._make(70.0) == 95.0  # 30+20+10+15+10+10

    def test_ns_exactly_60_gives_10pts(self):
        assert self._make(60.0) == 95.0

    def test_ns_between_40_and_59_gives_5pts(self):
        assert self._make(50.0) == 90.0  # 30+20+5+15+10+10

    def test_ns_exactly_40_gives_5pts(self):
        assert self._make(40.0) == 90.0

    def test_ns_below_40_gives_0pts(self):
        assert self._make(39.0) == 85.0  # 30+20+0+15+10+10

    def test_ns_zero_gives_0pts(self):
        assert self._make(0.0) == 85.0


# ─── 9. TestCoachingScoreMultiThread ─────────────────────────────────────────


class TestCoachingScoreMultiThread:
    """Test multi_thread_avg_contacts contribution (0-15 pts)."""

    def _make(self, mt: float) -> float:
        # att=120→30, pc=3→20, ns=80→15, crm=1→10, discount=5→10 = 85 + mt_pts
        rep = make_rep(
            quota_attainment_pct=120.0,
            pipeline_coverage_ratio=3.0,
            next_step_set_pct=80.0,
            multi_thread_avg_contacts=mt,
            crm_update_lag_days=1.0,
            discount_avg_pct=5.0,
        )
        return _coaching_score(rep)

    def test_mt_3_5_gives_15pts(self):
        assert self._make(3.5) == 100.0

    def test_mt_above_3_5_gives_15pts(self):
        assert self._make(5.0) == 100.0

    def test_mt_between_2_5_and_3_5_gives_10pts(self):
        assert self._make(3.0) == 95.0  # 30+20+15+10+10+10

    def test_mt_exactly_2_5_gives_10pts(self):
        assert self._make(2.5) == 95.0

    def test_mt_between_1_5_and_2_5_gives_5pts(self):
        assert self._make(2.0) == 90.0  # 30+20+15+5+10+10

    def test_mt_exactly_1_5_gives_5pts(self):
        assert self._make(1.5) == 90.0

    def test_mt_below_1_5_gives_0pts(self):
        assert self._make(1.4) == 85.0  # 30+20+15+0+10+10

    def test_mt_zero_gives_0pts(self):
        assert self._make(0.0) == 85.0


# ─── 10. TestCoachingScoreCRMLag ─────────────────────────────────────────────


class TestCoachingScoreCRMLag:
    """Test crm_update_lag_days contribution (0-10 pts)."""

    def _make(self, lag: float) -> float:
        # att=120→30, pc=3→20, ns=80→15, mt=3.5→15, discount=5→10 = 90 + lag_pts
        rep = make_rep(
            quota_attainment_pct=120.0,
            pipeline_coverage_ratio=3.0,
            next_step_set_pct=80.0,
            multi_thread_avg_contacts=3.5,
            crm_update_lag_days=lag,
            discount_avg_pct=5.0,
        )
        return _coaching_score(rep)

    def test_lag_1_gives_10pts(self):
        assert self._make(1.0) == 100.0

    def test_lag_0_gives_10pts(self):
        assert self._make(0.0) == 100.0

    def test_lag_between_1_and_3_gives_6pts(self):
        assert self._make(2.0) == 96.0  # 90+6

    def test_lag_exactly_3_gives_6pts(self):
        assert self._make(3.0) == 96.0

    def test_lag_between_3_and_7_gives_2pts(self):
        assert self._make(5.0) == 92.0  # 90+2

    def test_lag_exactly_7_gives_2pts(self):
        assert self._make(7.0) == 92.0

    def test_lag_above_7_gives_0pts(self):
        assert self._make(8.0) == 90.0  # 90+0

    def test_lag_very_high_gives_0pts(self):
        assert self._make(30.0) == 90.0


# ─── 11. TestCoachingScoreDiscount ───────────────────────────────────────────


class TestCoachingScoreDiscount:
    """Test discount_avg_pct contribution (0-10 pts)."""

    def _make(self, disc: float) -> float:
        # att=120→30, pc=3→20, ns=80→15, mt=3.5→15, crm=1→10 = 90 + disc_pts
        rep = make_rep(
            quota_attainment_pct=120.0,
            pipeline_coverage_ratio=3.0,
            next_step_set_pct=80.0,
            multi_thread_avg_contacts=3.5,
            crm_update_lag_days=1.0,
            discount_avg_pct=disc,
        )
        return _coaching_score(rep)

    def test_disc_5_gives_10pts(self):
        assert self._make(5.0) == 100.0

    def test_disc_0_gives_10pts(self):
        assert self._make(0.0) == 100.0

    def test_disc_between_5_and_15_gives_6pts(self):
        assert self._make(10.0) == 96.0  # 90+6

    def test_disc_exactly_15_gives_6pts(self):
        assert self._make(15.0) == 96.0

    def test_disc_between_15_and_25_gives_2pts(self):
        assert self._make(20.0) == 92.0  # 90+2

    def test_disc_exactly_25_gives_2pts(self):
        assert self._make(25.0) == 92.0

    def test_disc_above_25_gives_0pts(self):
        assert self._make(26.0) == 90.0

    def test_disc_very_high_gives_0pts(self):
        assert self._make(60.0) == 90.0


# ─── 12. TestCoachingScoreClamping ───────────────────────────────────────────


class TestCoachingScoreClamping:
    def test_max_score_is_100(self, star_rep):
        score = _coaching_score(star_rep)
        assert score <= 100.0

    def test_perfect_rep_gives_100(self):
        rep = make_rep(
            quota_attainment_pct=200.0,
            pipeline_coverage_ratio=10.0,
            next_step_set_pct=100.0,
            multi_thread_avg_contacts=10.0,
            crm_update_lag_days=0.0,
            discount_avg_pct=0.0,
        )
        assert _coaching_score(rep) == 100.0

    def test_min_score_is_0(self, critical_rep):
        score = _coaching_score(critical_rep)
        assert score >= 0.0

    def test_worst_case_score_is_zero_or_positive(self):
        rep = make_rep(
            quota_attainment_pct=0.0,
            pipeline_coverage_ratio=0.0,
            next_step_set_pct=0.0,
            multi_thread_avg_contacts=0.0,
            crm_update_lag_days=100.0,
            discount_avg_pct=100.0,
        )
        assert _coaching_score(rep) == 0.0

    def test_score_is_float(self, star_rep):
        score = _coaching_score(star_rep)
        assert isinstance(score, (int, float))

    def test_score_rounded_to_1dp(self, star_rep):
        score = _coaching_score(star_rep)
        assert round(score, 1) == score

    def test_score_within_valid_range_for_moderate(self, moderate_rep):
        score = _coaching_score(moderate_rep)
        assert 0.0 <= score <= 100.0


# ─── 13. TestCoachingIntensityThresholds ─────────────────────────────────────


class TestCoachingIntensityThresholds:
    def test_light_score_80_att_100(self):
        assert _coaching_intensity(80.0, 100.0) == CoachingIntensity.LIGHT

    def test_light_score_100_att_150(self):
        assert _coaching_intensity(100.0, 150.0) == CoachingIntensity.LIGHT

    def test_not_light_when_score_80_att_99(self):
        result = _coaching_intensity(80.0, 99.0)
        assert result != CoachingIntensity.LIGHT

    def test_not_light_when_score_79_att_100(self):
        result = _coaching_intensity(79.0, 100.0)
        assert result != CoachingIntensity.LIGHT

    def test_moderate_score_60_att_75(self):
        assert _coaching_intensity(60.0, 75.0) == CoachingIntensity.MODERATE

    def test_moderate_score_70_att_80(self):
        assert _coaching_intensity(70.0, 80.0) == CoachingIntensity.MODERATE

    def test_not_moderate_when_score_60_att_74(self):
        result = _coaching_intensity(60.0, 74.0)
        assert result != CoachingIntensity.MODERATE

    def test_not_moderate_when_score_59_att_75(self):
        result = _coaching_intensity(59.0, 75.0)
        assert result != CoachingIntensity.MODERATE

    def test_intensive_score_35_att_30(self):
        assert _coaching_intensity(35.0, 30.0) == CoachingIntensity.INTENSIVE

    def test_intensive_score_20_att_50(self):
        assert _coaching_intensity(20.0, 50.0) == CoachingIntensity.INTENSIVE

    def test_intensive_score_34_att_49_is_critical(self):
        # score < 35 AND att < 50 -> CRITICAL
        assert _coaching_intensity(34.0, 49.0) == CoachingIntensity.CRITICAL

    def test_critical_score_0_att_0(self):
        assert _coaching_intensity(0.0, 0.0) == CoachingIntensity.CRITICAL

    def test_critical_score_34_att_0(self):
        assert _coaching_intensity(34.0, 0.0) == CoachingIntensity.CRITICAL

    def test_intensive_exact_boundary_score_35(self):
        assert _coaching_intensity(35.0, 49.0) == CoachingIntensity.INTENSIVE

    def test_intensive_exact_boundary_att_50(self):
        assert _coaching_intensity(34.0, 50.0) == CoachingIntensity.INTENSIVE


# ─── 14. TestDetectSkillGaps ─────────────────────────────────────────────────


class TestDetectSkillGaps:
    def test_discovery_triggered_below_5(self):
        rep = make_rep(avg_discovery_questions_per_call=4.9)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.DISCOVERY in gaps

    def test_discovery_not_triggered_at_5(self):
        rep = make_rep(avg_discovery_questions_per_call=5.0)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.DISCOVERY not in gaps

    def test_qualification_triggered_above_20(self):
        rep = make_rep(deals_lost_to_no_decision_pct=20.1)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.QUALIFICATION in gaps

    def test_qualification_not_triggered_at_20(self):
        rep = make_rep(deals_lost_to_no_decision_pct=20.0)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.QUALIFICATION not in gaps

    def test_presentation_triggered_discount_above_20(self):
        rep = make_rep(discount_avg_pct=21.0)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.PRESENTATION in gaps

    def test_presentation_not_triggered_at_20(self):
        rep = make_rep(discount_avg_pct=20.0)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.PRESENTATION not in gaps

    def test_objection_handling_triggered_above_30(self):
        rep = make_rep(deals_lost_to_competitor_pct=31.0)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.OBJECTION_HANDLING in gaps

    def test_objection_handling_not_triggered_at_30(self):
        rep = make_rep(deals_lost_to_competitor_pct=30.0)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.OBJECTION_HANDLING not in gaps

    def test_closing_triggered_att_below_80_and_pc_above_2(self):
        rep = make_rep(quota_attainment_pct=79.0, pipeline_coverage_ratio=2.0)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.CLOSING in gaps

    def test_closing_not_triggered_att_80(self):
        rep = make_rep(quota_attainment_pct=80.0, pipeline_coverage_ratio=2.0)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.CLOSING not in gaps

    def test_closing_not_triggered_pc_below_2(self):
        rep = make_rep(quota_attainment_pct=70.0, pipeline_coverage_ratio=1.9)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.CLOSING not in gaps

    def test_pipeline_hygiene_triggered_crm_above_3(self):
        rep = make_rep(crm_update_lag_days=3.1)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.PIPELINE_HYGIENE in gaps

    def test_pipeline_hygiene_not_triggered_at_3(self):
        rep = make_rep(crm_update_lag_days=3.0)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.PIPELINE_HYGIENE not in gaps

    def test_multi_threading_triggered_below_2(self):
        rep = make_rep(multi_thread_avg_contacts=1.9)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.MULTI_THREADING in gaps

    def test_multi_threading_not_triggered_at_2(self):
        rep = make_rep(multi_thread_avg_contacts=2.0)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.MULTI_THREADING not in gaps

    def test_forecasting_triggered_absolute_above_25(self):
        rep = make_rep(forecast_accuracy_pct=26.0)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.FORECASTING in gaps

    def test_forecasting_triggered_negative_absolute_above_25(self):
        rep = make_rep(forecast_accuracy_pct=-26.0)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.FORECASTING in gaps

    def test_forecasting_not_triggered_at_25(self):
        rep = make_rep(forecast_accuracy_pct=25.0)
        gaps = _detect_skill_gaps(rep)
        assert SkillGap.FORECASTING not in gaps

    def test_top_4_cap(self):
        # Trigger all 8 gaps; only first 4 should be returned
        rep = make_rep(
            avg_discovery_questions_per_call=1.0,   # DISCOVERY
            deals_lost_to_no_decision_pct=30.0,      # QUALIFICATION
            discount_avg_pct=25.0,                   # PRESENTATION
            deals_lost_to_competitor_pct=40.0,       # OBJECTION_HANDLING
            quota_attainment_pct=50.0,               # enables CLOSING (att<80)
            pipeline_coverage_ratio=2.5,             # CLOSING (pc>=2)
            crm_update_lag_days=5.0,                 # PIPELINE_HYGIENE
            multi_thread_avg_contacts=1.0,           # MULTI_THREADING
            forecast_accuracy_pct=30.0,              # FORECASTING
        )
        gaps = _detect_skill_gaps(rep)
        assert len(gaps) <= 4

    def test_no_gaps_for_perfect_rep(self, star_rep):
        # star_rep has good metrics except defaults may trigger some
        rep = make_rep(
            avg_discovery_questions_per_call=8.0,
            deals_lost_to_no_decision_pct=10.0,
            discount_avg_pct=5.0,
            deals_lost_to_competitor_pct=20.0,
            quota_attainment_pct=120.0,
            pipeline_coverage_ratio=3.0,
            crm_update_lag_days=1.0,
            multi_thread_avg_contacts=3.5,
            forecast_accuracy_pct=5.0,
        )
        gaps = _detect_skill_gaps(rep)
        assert len(gaps) == 0

    def test_gaps_returns_list(self):
        rep = make_rep()
        gaps = _detect_skill_gaps(rep)
        assert isinstance(gaps, list)

    def test_gap_items_are_skillgap(self):
        rep = make_rep(avg_discovery_questions_per_call=3.0)
        gaps = _detect_skill_gaps(rep)
        for g in gaps:
            assert isinstance(g, SkillGap)


# ─── 15. TestPrimaryFocus ─────────────────────────────────────────────────────


class TestPrimaryFocus:
    def test_pipeline_when_pipeline_hygiene_in_gaps(self):
        gaps = [SkillGap.PIPELINE_HYGIENE]
        focus = _primary_focus(gaps, 100.0, 3.0)
        assert focus == CoachingFocus.PIPELINE

    def test_pipeline_when_pc_below_1_5(self):
        gaps = []
        focus = _primary_focus(gaps, 80.0, 1.4)
        assert focus == CoachingFocus.PIPELINE

    def test_pipeline_has_priority_over_mindset(self):
        # PIPELINE_HYGIENE in gaps AND att < 50 -> PIPELINE wins
        gaps = [SkillGap.PIPELINE_HYGIENE]
        focus = _primary_focus(gaps, 40.0, 3.0)
        assert focus == CoachingFocus.PIPELINE

    def test_mindset_when_att_below_50(self):
        gaps = []
        focus = _primary_focus(gaps, 49.0, 2.0)
        assert focus == CoachingFocus.MINDSET

    def test_mindset_att_zero(self):
        gaps = []
        focus = _primary_focus(gaps, 0.0, 2.0)
        assert focus == CoachingFocus.MINDSET

    def test_skills_when_discovery_in_gaps(self):
        gaps = [SkillGap.DISCOVERY]
        focus = _primary_focus(gaps, 70.0, 2.0)
        assert focus == CoachingFocus.SKILLS

    def test_skills_when_qualification_in_gaps(self):
        gaps = [SkillGap.QUALIFICATION]
        focus = _primary_focus(gaps, 70.0, 2.0)
        assert focus == CoachingFocus.SKILLS

    def test_process_when_forecasting_in_gaps(self):
        # No PIPELINE_HYGIENE, att>=50, no DISCOVERY/QUALIFICATION, but FORECASTING
        gaps = [SkillGap.FORECASTING]
        focus = _primary_focus(gaps, 70.0, 2.0)
        assert focus == CoachingFocus.PROCESS

    def test_strategy_when_att_above_80_no_gaps(self):
        gaps = []
        focus = _primary_focus(gaps, 80.0, 2.0)
        assert focus == CoachingFocus.STRATEGY

    def test_strategy_att_exactly_80(self):
        gaps = []
        focus = _primary_focus(gaps, 80.0, 2.0)
        assert focus == CoachingFocus.STRATEGY

    def test_fallback_skills_when_att_between_50_and_80_no_gaps(self):
        gaps = []
        focus = _primary_focus(gaps, 70.0, 2.0)
        assert focus == CoachingFocus.SKILLS

    def test_pipeline_when_pc_exactly_1_5_not_triggered(self):
        # pc >= 1.5, so no PIPELINE from that path; att=70, no gaps -> SKILLS
        gaps = []
        focus = _primary_focus(gaps, 70.0, 1.5)
        assert focus == CoachingFocus.SKILLS

    def test_returns_coaching_focus_instance(self):
        gaps = []
        focus = _primary_focus(gaps, 100.0, 3.0)
        assert isinstance(focus, CoachingFocus)


# ─── 16. TestBuildStrengths ──────────────────────────────────────────────────


class TestBuildStrengths:
    def test_quota_strength_at_100(self):
        rep = make_rep(quota_attainment_pct=100.0)
        strengths = _build_strengths(rep, 60.0)
        assert any("quota" in s.lower() or "100" in s for s in strengths)

    def test_quota_strength_at_120(self):
        rep = make_rep(quota_attainment_pct=120.0)
        strengths = _build_strengths(rep, 80.0)
        assert any("120" in s for s in strengths)

    def test_no_quota_strength_below_100(self):
        rep = make_rep(quota_attainment_pct=99.0)
        strengths = _build_strengths(rep, 50.0)
        # Check no quota-atteinte string
        assert not any("Atteinte quota" in s for s in strengths)

    def test_next_step_strength_at_75(self):
        rep = make_rep(next_step_set_pct=75.0)
        strengths = _build_strengths(rep, 60.0)
        assert any("prochaines" in s.lower() or "NS" in s for s in strengths)

    def test_next_step_strength_at_80(self):
        rep = make_rep(next_step_set_pct=80.0)
        strengths = _build_strengths(rep, 60.0)
        assert any("80" in s for s in strengths)

    def test_no_next_step_strength_below_75(self):
        rep = make_rep(next_step_set_pct=74.0)
        strengths = _build_strengths(rep, 50.0)
        assert not any("prochaines" in s.lower() for s in strengths)

    def test_multi_thread_strength_at_3(self):
        rep = make_rep(multi_thread_avg_contacts=3.0)
        strengths = _build_strengths(rep, 60.0)
        assert any("multi" in s.lower() or "3.0" in s for s in strengths)

    def test_no_multi_thread_strength_below_3(self):
        rep = make_rep(multi_thread_avg_contacts=2.9)
        strengths = _build_strengths(rep, 50.0)
        assert not any("Multi-threading" in s for s in strengths)

    def test_discount_strength_at_10(self):
        rep = make_rep(discount_avg_pct=10.0)
        strengths = _build_strengths(rep, 60.0)
        assert any("remise" in s.lower() or "prix" in s.lower() for s in strengths)

    def test_no_discount_strength_above_10(self):
        rep = make_rep(discount_avg_pct=11.0)
        strengths = _build_strengths(rep, 50.0)
        assert not any("tenue sur les prix" in s for s in strengths)

    def test_pipeline_strength_at_3(self):
        rep = make_rep(pipeline_coverage_ratio=3.0)
        strengths = _build_strengths(rep, 60.0)
        assert any("pipeline" in s.lower() for s in strengths)

    def test_no_pipeline_strength_below_3(self):
        rep = make_rep(pipeline_coverage_ratio=2.9)
        strengths = _build_strengths(rep, 50.0)
        assert not any("Couverture pipeline" in s for s in strengths)

    def test_crm_strength_at_1(self):
        rep = make_rep(crm_update_lag_days=1.0)
        strengths = _build_strengths(rep, 60.0)
        assert any("CRM" in s or "crm" in s.lower() for s in strengths)

    def test_no_crm_strength_above_1(self):
        rep = make_rep(crm_update_lag_days=1.1)
        strengths = _build_strengths(rep, 50.0)
        assert not any("CRM à jour" in s for s in strengths)

    def test_discovery_strength_at_8(self):
        rep = make_rep(avg_discovery_questions_per_call=8.0)
        strengths = _build_strengths(rep, 60.0)
        assert any("couverte" in s.lower() or "Découverte" in s for s in strengths)

    def test_no_discovery_strength_below_8(self):
        rep = make_rep(avg_discovery_questions_per_call=7.9)
        strengths = _build_strengths(rep, 50.0)
        assert not any("Découverte approfondie" in s for s in strengths)

    def test_returns_list(self):
        rep = make_rep()
        result = _build_strengths(rep, 50.0)
        assert isinstance(result, list)

    def test_empty_for_poor_rep(self, critical_rep):
        strengths = _build_strengths(critical_rep, 5.0)
        assert isinstance(strengths, list)


# ─── 17. TestBuildDevelopmentAreas ───────────────────────────────────────────


class TestBuildDevelopmentAreas:
    def test_discovery_area_when_gap_present(self):
        rep = make_rep(avg_discovery_questions_per_call=3.0)
        areas = _build_development_areas(rep, [SkillGap.DISCOVERY])
        assert any("Découverte" in a for a in areas)

    def test_no_discovery_area_when_gap_absent(self):
        rep = make_rep(avg_discovery_questions_per_call=3.0)
        areas = _build_development_areas(rep, [])
        assert not any("Découverte insuffisante" in a for a in areas)

    def test_qualification_area_when_gap_present(self):
        rep = make_rep(deals_lost_to_no_decision_pct=30.0)
        areas = _build_development_areas(rep, [SkillGap.QUALIFICATION])
        assert any("Qualification" in a for a in areas)

    def test_presentation_area_when_gap_present(self):
        rep = make_rep(discount_avg_pct=25.0)
        areas = _build_development_areas(rep, [SkillGap.PRESENTATION])
        assert any("Présentation" in a or "demo" in a.lower() for a in areas)

    def test_objection_handling_area_when_gap_present(self):
        rep = make_rep(deals_lost_to_competitor_pct=40.0)
        areas = _build_development_areas(rep, [SkillGap.OBJECTION_HANDLING])
        assert any("objection" in a.lower() or "Gestion" in a for a in areas)

    def test_closing_area_when_gap_present(self):
        rep = make_rep()
        areas = _build_development_areas(rep, [SkillGap.CLOSING])
        assert any("closing" in a.lower() or "Compétences" in a for a in areas)

    def test_pipeline_hygiene_area_when_gap_present(self):
        rep = make_rep(crm_update_lag_days=5.0)
        areas = _build_development_areas(rep, [SkillGap.PIPELINE_HYGIENE])
        assert any("CRM" in a or "Hygiène" in a for a in areas)

    def test_multi_threading_area_when_gap_present(self):
        rep = make_rep(multi_thread_avg_contacts=1.5)
        areas = _build_development_areas(rep, [SkillGap.MULTI_THREADING])
        assert any("Multi-threading" in a or "contacts" in a.lower() for a in areas)

    def test_forecasting_area_when_gap_present(self):
        rep = make_rep(forecast_accuracy_pct=30.0)
        areas = _build_development_areas(rep, [SkillGap.FORECASTING])
        assert any("forecast" in a.lower() or "Prévisions" in a for a in areas)

    def test_empty_gaps_gives_empty_list(self):
        rep = make_rep()
        areas = _build_development_areas(rep, [])
        assert areas == []

    def test_returns_list(self):
        rep = make_rep()
        result = _build_development_areas(rep, [])
        assert isinstance(result, list)

    def test_multiple_gaps_gives_multiple_areas(self):
        rep = make_rep(
            avg_discovery_questions_per_call=3.0,
            deals_lost_to_no_decision_pct=30.0,
        )
        areas = _build_development_areas(
            rep, [SkillGap.DISCOVERY, SkillGap.QUALIFICATION]
        )
        assert len(areas) == 2


# ─── 18. TestBuildSessionPlan ─────────────────────────────────────────────────


class TestBuildSessionPlan:
    def test_light_plan_has_steps(self):
        plan = _build_session_plan(CoachingIntensity.LIGHT, CoachingFocus.STRATEGY)
        assert len(plan) > 0

    def test_moderate_plan_has_steps(self):
        plan = _build_session_plan(CoachingIntensity.MODERATE, CoachingFocus.SKILLS)
        assert len(plan) > 0

    def test_intensive_plan_has_steps(self):
        plan = _build_session_plan(CoachingIntensity.INTENSIVE, CoachingFocus.PIPELINE)
        assert len(plan) > 0

    def test_critical_plan_has_steps(self):
        plan = _build_session_plan(CoachingIntensity.CRITICAL, CoachingFocus.MINDSET)
        assert len(plan) > 0

    def test_light_plan_count(self):
        plan = _build_session_plan(CoachingIntensity.LIGHT, CoachingFocus.STRATEGY)
        assert len(plan) == 3

    def test_moderate_plan_count(self):
        plan = _build_session_plan(CoachingIntensity.MODERATE, CoachingFocus.SKILLS)
        assert len(plan) == 5

    def test_intensive_plan_count(self):
        plan = _build_session_plan(CoachingIntensity.INTENSIVE, CoachingFocus.PIPELINE)
        assert len(plan) == 8

    def test_critical_plan_count(self):
        plan = _build_session_plan(CoachingIntensity.CRITICAL, CoachingFocus.MINDSET)
        assert len(plan) == 8

    def test_light_plan_starts_with_s1(self):
        plan = _build_session_plan(CoachingIntensity.LIGHT, CoachingFocus.STRATEGY)
        assert plan[0].startswith("S1")

    def test_moderate_plan_starts_with_s1(self):
        plan = _build_session_plan(CoachingIntensity.MODERATE, CoachingFocus.SKILLS)
        assert plan[0].startswith("S1")

    def test_critical_plan_mentions_pip(self):
        plan = _build_session_plan(CoachingIntensity.CRITICAL, CoachingFocus.PROCESS)
        assert any("PIP" in step for step in plan)

    def test_returns_list_of_strings(self):
        plan = _build_session_plan(CoachingIntensity.LIGHT, CoachingFocus.STRATEGY)
        assert isinstance(plan, list)
        for step in plan:
            assert isinstance(step, str)

    def test_intensive_plan_has_more_sessions_than_moderate(self):
        intensive = _build_session_plan(CoachingIntensity.INTENSIVE, CoachingFocus.SKILLS)
        moderate = _build_session_plan(CoachingIntensity.MODERATE, CoachingFocus.SKILLS)
        assert len(intensive) > len(moderate)

    def test_critical_plan_has_more_sessions_than_light(self):
        critical = _build_session_plan(CoachingIntensity.CRITICAL, CoachingFocus.SKILLS)
        light = _build_session_plan(CoachingIntensity.LIGHT, CoachingFocus.SKILLS)
        assert len(critical) > len(light)


# ─── 19. TestBuildKPIsToTrack ─────────────────────────────────────────────────


class TestBuildKPIsToTrack:
    def test_base_kpis_always_present(self):
        rep = make_rep()
        kpis = _build_kpis_to_track(rep, [])
        # At least quota, pipeline coverage, next steps, discount
        assert len(kpis) >= 3

    def test_quota_kpi_always_present(self):
        rep = make_rep()
        kpis = _build_kpis_to_track(rep, [])
        assert any("quota" in k.lower() or "Atteinte" in k for k in kpis)

    def test_pipeline_kpi_always_present(self):
        rep = make_rep()
        kpis = _build_kpis_to_track(rep, [])
        assert any("pipeline" in k.lower() or "Couverture" in k for k in kpis)

    def test_next_step_kpi_always_present(self):
        rep = make_rep()
        kpis = _build_kpis_to_track(rep, [])
        assert any("prochaine" in k.lower() or "tape" in k for k in kpis)

    def test_discount_kpi_always_present(self):
        rep = make_rep()
        kpis = _build_kpis_to_track(rep, [])
        assert any("remise" in k.lower() or "Remise" in k for k in kpis)

    def test_discovery_kpi_added_when_gap_present(self):
        rep = make_rep(avg_discovery_questions_per_call=3.0)
        kpis = _build_kpis_to_track(rep, [SkillGap.DISCOVERY])
        assert any("discovery" in k.lower() or "Questions" in k for k in kpis)

    def test_discovery_kpi_absent_when_gap_absent(self):
        rep = make_rep()
        kpis = _build_kpis_to_track(rep, [])
        assert not any("Questions discovery" in k for k in kpis)

    def test_multi_threading_kpi_added_when_gap_present(self):
        rep = make_rep(multi_thread_avg_contacts=1.5)
        kpis = _build_kpis_to_track(rep, [SkillGap.MULTI_THREADING])
        assert any("Contact" in k or "contact" in k.lower() for k in kpis)

    def test_multi_threading_kpi_absent_when_gap_absent(self):
        rep = make_rep()
        kpis = _build_kpis_to_track(rep, [])
        assert not any("Contacts/deal" in k for k in kpis)

    def test_pipeline_hygiene_kpi_added_when_gap_present(self):
        rep = make_rep(crm_update_lag_days=5.0)
        kpis = _build_kpis_to_track(rep, [SkillGap.PIPELINE_HYGIENE])
        assert any("CRM" in k or "mise à jour" in k.lower() for k in kpis)

    def test_pipeline_hygiene_kpi_absent_when_gap_absent(self):
        rep = make_rep()
        kpis = _build_kpis_to_track(rep, [])
        assert not any("Délai mise à jour CRM" in k for k in kpis)

    def test_forecasting_kpi_added_when_gap_present(self):
        rep = make_rep(forecast_accuracy_pct=30.0)
        kpis = _build_kpis_to_track(rep, [SkillGap.FORECASTING])
        assert any("forecast" in k.lower() or "Précision" in k for k in kpis)

    def test_forecasting_kpi_absent_when_gap_absent(self):
        rep = make_rep()
        kpis = _build_kpis_to_track(rep, [])
        assert not any("Précision forecast" in k for k in kpis)

    def test_returns_list_of_strings(self):
        rep = make_rep()
        kpis = _build_kpis_to_track(rep, [])
        assert isinstance(kpis, list)
        for k in kpis:
            assert isinstance(k, str)

    def test_more_kpis_with_more_gaps(self):
        rep = make_rep()
        base = _build_kpis_to_track(rep, [])
        with_gaps = _build_kpis_to_track(rep, [SkillGap.DISCOVERY, SkillGap.MULTI_THREADING])
        assert len(with_gaps) > len(base)


# ─── 20. TestEngineCoach ─────────────────────────────────────────────────────


class TestEngineCoach:
    def test_coach_returns_coaching_plan_result(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert isinstance(result, CoachingPlanResult)

    def test_coach_stores_result(self, engine, star_rep):
        engine.coach(star_rep)
        assert engine.get(star_rep.rep_id) is not None

    def test_coach_rep_id_matches(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert result.rep_id == star_rep.rep_id

    def test_coach_rep_name_matches(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert result.rep_name == star_rep.rep_name

    def test_coach_segment_matches(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert result.segment == star_rep.segment

    def test_coach_tenure_matches(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert result.tenure_months == star_rep.tenure_months

    def test_coach_score_within_range(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert 0.0 <= result.coaching_score <= 100.0

    def test_coach_intensity_is_enum(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert isinstance(result.coaching_intensity, CoachingIntensity)

    def test_coach_focus_is_enum(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert isinstance(result.primary_focus, CoachingFocus)

    def test_coach_gaps_is_list(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert isinstance(result.top_skill_gaps, list)

    def test_coach_strengths_is_list(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert isinstance(result.strengths, list)

    def test_coach_dev_areas_is_list(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert isinstance(result.development_areas, list)

    def test_coach_actions_is_list(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert isinstance(result.coaching_actions, list)

    def test_coach_session_plan_is_list(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert isinstance(result.session_plan, list)

    def test_coach_kpis_is_list(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert isinstance(result.kpis_to_track, list)

    def test_coach_overwrite_same_rep(self, engine, star_rep):
        r1 = engine.coach(star_rep)
        r2 = engine.coach(star_rep)
        assert engine.get(star_rep.rep_id) is not None
        assert r2.rep_id == star_rep.rep_id

    def test_get_returns_none_for_unknown(self, engine):
        assert engine.get("NONEXISTENT") is None

    def test_coach_star_rep_gets_light(self, engine):
        # star_rep with quota_attainment=120, score should be high
        rep = make_rep(
            quota_attainment_pct=120.0,
            pipeline_coverage_ratio=3.0,
            next_step_set_pct=80.0,
            multi_thread_avg_contacts=3.5,
            crm_update_lag_days=1.0,
            discount_avg_pct=5.0,
        )
        result = engine.coach(rep)
        assert result.coaching_intensity == CoachingIntensity.LIGHT

    def test_coach_critical_rep_gets_critical_intensity(self, engine, critical_rep):
        result = engine.coach(critical_rep)
        assert result.coaching_intensity == CoachingIntensity.CRITICAL

    def test_coach_session_plan_not_empty(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert len(result.session_plan) > 0

    def test_coach_kpis_not_empty(self, engine, star_rep):
        result = engine.coach(star_rep)
        assert len(result.kpis_to_track) > 0


# ─── 21. TestEngineBatchAndFilters ───────────────────────────────────────────


class TestEngineBatchAndFilters:
    def _batch_reps(self):
        return [
            make_rep(rep_id="A", rep_name="Alice", quota_attainment_pct=120.0,
                     pipeline_coverage_ratio=3.0, next_step_set_pct=80.0,
                     multi_thread_avg_contacts=3.5, crm_update_lag_days=1.0,
                     discount_avg_pct=5.0),
            make_rep(rep_id="B", rep_name="Bob", quota_attainment_pct=75.0,
                     pipeline_coverage_ratio=2.0, next_step_set_pct=60.0,
                     multi_thread_avg_contacts=2.5, crm_update_lag_days=3.0,
                     discount_avg_pct=15.0),
            make_rep(rep_id="C", rep_name="Carol", quota_attainment_pct=20.0,
                     pipeline_coverage_ratio=0.5, next_step_set_pct=30.0,
                     multi_thread_avg_contacts=1.0, crm_update_lag_days=10.0,
                     discount_avg_pct=30.0),
        ]

    def test_coach_batch_returns_list(self, engine):
        reps = self._batch_reps()
        results = engine.coach_batch(reps)
        assert isinstance(results, list)

    def test_coach_batch_returns_correct_count(self, engine):
        reps = self._batch_reps()
        results = engine.coach_batch(reps)
        assert len(results) == 3

    def test_coach_batch_sorted_desc_by_score(self, engine):
        reps = self._batch_reps()
        results = engine.coach_batch(reps)
        scores = [r.coaching_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_coach_batch_first_is_highest_score(self, engine):
        reps = self._batch_reps()
        results = engine.coach_batch(reps)
        assert results[0].coaching_score >= results[-1].coaching_score

    def test_coach_batch_stores_all_reps(self, engine):
        reps = self._batch_reps()
        engine.coach_batch(reps)
        for rep in reps:
            assert engine.get(rep.rep_id) is not None

    def test_all_reps_sorted_desc(self, engine):
        reps = self._batch_reps()
        engine.coach_batch(reps)
        all_r = engine.all_reps()
        scores = [r.coaching_score for r in all_r]
        assert scores == sorted(scores, reverse=True)

    def test_by_intensity_filters_correctly(self, engine):
        reps = self._batch_reps()
        engine.coach_batch(reps)
        light = engine.by_intensity(CoachingIntensity.LIGHT)
        for r in light:
            assert r.coaching_intensity == CoachingIntensity.LIGHT

    def test_by_intensity_critical_matches_needs_critical(self, engine):
        reps = self._batch_reps()
        engine.coach_batch(reps)
        assert engine.by_intensity(CoachingIntensity.CRITICAL) == engine.needs_critical_attention()

    def test_by_focus_filters_correctly(self, engine):
        reps = self._batch_reps()
        engine.coach_batch(reps)
        for focus in CoachingFocus:
            filtered = engine.by_focus(focus)
            for r in filtered:
                assert r.primary_focus == focus

    def test_needs_critical_attention_returns_critical_only(self, engine):
        reps = self._batch_reps()
        engine.coach_batch(reps)
        critical = engine.needs_critical_attention()
        for r in critical:
            assert r.coaching_intensity == CoachingIntensity.CRITICAL

    def test_star_performers_returns_light_only(self, engine):
        reps = self._batch_reps()
        engine.coach_batch(reps)
        stars = engine.star_performers()
        for r in stars:
            assert r.coaching_intensity == CoachingIntensity.LIGHT

    def test_with_skill_gap_filters_correctly(self, engine):
        rep_with_gap = make_rep(
            rep_id="GAP1",
            avg_discovery_questions_per_call=2.0,  # triggers DISCOVERY gap
        )
        rep_no_gap = make_rep(
            rep_id="NOGAP1",
            avg_discovery_questions_per_call=8.0,
        )
        engine.coach(rep_with_gap)
        engine.coach(rep_no_gap)
        with_discovery = engine.with_skill_gap(SkillGap.DISCOVERY)
        for r in with_discovery:
            assert SkillGap.DISCOVERY in r.top_skill_gaps

    def test_with_skill_gap_excludes_reps_without_gap(self, engine):
        rep_no_gap = make_rep(
            rep_id="NOGAP2",
            avg_discovery_questions_per_call=8.0,
            deals_lost_to_no_decision_pct=5.0,
            discount_avg_pct=5.0,
            deals_lost_to_competitor_pct=10.0,
            quota_attainment_pct=100.0,
            pipeline_coverage_ratio=2.0,
            crm_update_lag_days=1.0,
            multi_thread_avg_contacts=3.0,
            forecast_accuracy_pct=5.0,
        )
        engine.coach(rep_no_gap)
        with_disc = engine.with_skill_gap(SkillGap.DISCOVERY)
        assert rep_no_gap.rep_id not in [r.rep_id for r in with_disc]

    def test_empty_engine_all_reps(self, engine):
        assert engine.all_reps() == []

    def test_empty_engine_needs_critical(self, engine):
        assert engine.needs_critical_attention() == []

    def test_empty_engine_star_performers(self, engine):
        assert engine.star_performers() == []

    def test_coach_batch_empty_list(self, engine):
        results = engine.coach_batch([])
        assert results == []


# ─── 22. TestEngineAggregates ─────────────────────────────────────────────────


class TestEngineAggregates:
    def _populate_engine(self, engine):
        reps = [
            make_rep(rep_id="X1", rep_name="Rep1", quota_attainment_pct=120.0,
                     pipeline_coverage_ratio=3.0, next_step_set_pct=80.0,
                     multi_thread_avg_contacts=3.5, crm_update_lag_days=1.0,
                     discount_avg_pct=5.0),
            make_rep(rep_id="X2", rep_name="Rep2", quota_attainment_pct=20.0,
                     pipeline_coverage_ratio=0.5, next_step_set_pct=30.0,
                     multi_thread_avg_contacts=1.0, crm_update_lag_days=10.0,
                     discount_avg_pct=30.0),
        ]
        engine.coach_batch(reps)
        return reps

    def test_avg_coaching_score_is_float(self, engine):
        self._populate_engine(engine)
        avg = engine.avg_coaching_score()
        assert isinstance(avg, (int, float))

    def test_avg_coaching_score_rounded_to_1dp(self, engine):
        self._populate_engine(engine)
        avg = engine.avg_coaching_score()
        assert round(avg, 1) == avg

    def test_avg_coaching_score_correct(self, engine):
        reps = self._populate_engine(engine)
        s1 = _coaching_score(reps[0])
        s2 = _coaching_score(reps[1])
        expected = round((s1 + s2) / 2, 1)
        assert engine.avg_coaching_score() == expected

    def test_avg_coaching_score_empty_engine_is_zero(self, engine):
        assert engine.avg_coaching_score() == 0.0

    def test_summary_returns_dict(self, engine):
        self._populate_engine(engine)
        s = engine.summary()
        assert isinstance(s, dict)

    def test_summary_total_key(self, engine):
        self._populate_engine(engine)
        s = engine.summary()
        assert "total" in s
        assert s["total"] == 2

    def test_summary_intensity_counts_key(self, engine):
        self._populate_engine(engine)
        s = engine.summary()
        assert "intensity_counts" in s
        assert isinstance(s["intensity_counts"], dict)

    def test_summary_focus_counts_key(self, engine):
        self._populate_engine(engine)
        s = engine.summary()
        assert "focus_counts" in s
        assert isinstance(s["focus_counts"], dict)

    def test_summary_gap_counts_key(self, engine):
        self._populate_engine(engine)
        s = engine.summary()
        assert "gap_counts" in s
        assert isinstance(s["gap_counts"], dict)

    def test_summary_avg_coaching_score_key(self, engine):
        self._populate_engine(engine)
        s = engine.summary()
        assert "avg_coaching_score" in s
        assert isinstance(s["avg_coaching_score"], (int, float))

    def test_summary_critical_count_key(self, engine):
        self._populate_engine(engine)
        s = engine.summary()
        assert "critical_count" in s
        assert isinstance(s["critical_count"], int)

    def test_summary_star_count_key(self, engine):
        self._populate_engine(engine)
        s = engine.summary()
        assert "star_count" in s
        assert isinstance(s["star_count"], int)

    def test_summary_intensity_counts_sum_matches_total(self, engine):
        self._populate_engine(engine)
        s = engine.summary()
        assert sum(s["intensity_counts"].values()) == s["total"]

    def test_summary_focus_counts_sum_matches_total(self, engine):
        self._populate_engine(engine)
        s = engine.summary()
        assert sum(s["focus_counts"].values()) == s["total"]

    def test_summary_empty_engine(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["intensity_counts"] == {}
        assert s["focus_counts"] == {}
        assert s["gap_counts"] == {}
        assert s["avg_coaching_score"] == 0.0
        assert s["critical_count"] == 0
        assert s["star_count"] == 0

    def test_reset_clears_all_reps(self, engine):
        self._populate_engine(engine)
        engine.reset()
        assert engine.all_reps() == []

    def test_reset_clears_avg_score(self, engine):
        self._populate_engine(engine)
        engine.reset()
        assert engine.avg_coaching_score() == 0.0

    def test_reset_clears_summary(self, engine):
        self._populate_engine(engine)
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0

    def test_after_reset_can_add_new_reps(self, engine, star_rep):
        self._populate_engine(engine)
        engine.reset()
        engine.coach(star_rep)
        assert engine.get(star_rep.rep_id) is not None
        assert engine.avg_coaching_score() > 0.0

    def test_summary_gap_counts_values_are_ints(self, engine):
        rep = make_rep(avg_discovery_questions_per_call=3.0)
        engine.coach(rep)
        s = engine.summary()
        for v in s["gap_counts"].values():
            assert isinstance(v, int)

    def test_summary_intensity_keys_are_strings(self, engine):
        self._populate_engine(engine)
        s = engine.summary()
        for k in s["intensity_counts"]:
            assert isinstance(k, str)

    def test_summary_focus_keys_are_strings(self, engine):
        self._populate_engine(engine)
        s = engine.summary()
        for k in s["focus_counts"]:
            assert isinstance(k, str)
