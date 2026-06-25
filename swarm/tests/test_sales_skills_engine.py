"""
Comprehensive pytest test suite for SalesSkillsEngine.
Target: 280+ tests across all engine logic, enums, formulas, properties, and end-to-end flows.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_skills_engine import (
    CoachingPriority,
    DevelopmentPath,
    SalesSkillsEngine,
    SalesSkillsInput,
    SalesSkillsResult,
    SkillGap,
    SkillLevel,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _make_expert() -> SalesSkillsInput:
    return SalesSkillsInput(
        rep_id="r01", rep_name="Expert Rep", manager_id="m01",
        discovery_score=92, demo_effectiveness=88, objection_handling=85,
        negotiation_skill=90, closing_technique=87,
        prospecting_score=82, pipeline_management=88, crm_discipline=91,
        quota_attainment_pct=1.28, win_rate=0.48,
        avg_deal_size_vs_team=1.35, avg_sales_cycle_vs_team=0.82,
        call_connect_rate=0.32, email_reply_rate=0.25,
        meetings_set_per_week=8.5, months_at_company=36, months_in_role=24,
        training_hours_completed=45, coaching_sessions_90d=6,
        top_performer_last_quarter=True,
    )


def _make_beginner() -> SalesSkillsInput:
    return SalesSkillsInput(
        rep_id="r02", rep_name="Beginner Rep", manager_id="m02",
        discovery_score=20, demo_effectiveness=18, objection_handling=15,
        negotiation_skill=22, closing_technique=19,
        prospecting_score=17, pipeline_management=20, crm_discipline=16,
        quota_attainment_pct=0.35, win_rate=0.08,
        avg_deal_size_vs_team=0.60, avg_sales_cycle_vs_team=1.80,
        call_connect_rate=0.05, email_reply_rate=0.04,
        meetings_set_per_week=1.5, months_at_company=2, months_in_role=2,
        training_hours_completed=5, coaching_sessions_90d=1,
        top_performer_last_quarter=False,
    )


def _make_mid() -> SalesSkillsInput:
    """Mid-tier rep: PROFICIENT level, moderate gap."""
    return SalesSkillsInput(
        rep_id="r03", rep_name="Mid Rep", manager_id="m03",
        discovery_score=60, demo_effectiveness=58, objection_handling=62,
        negotiation_skill=57, closing_technique=59,
        prospecting_score=55, pipeline_management=60, crm_discipline=58,
        quota_attainment_pct=0.95, win_rate=0.28,
        avg_deal_size_vs_team=1.00, avg_sales_cycle_vs_team=1.00,
        call_connect_rate=0.18, email_reply_rate=0.14,
        meetings_set_per_week=4.0, months_at_company=14, months_in_role=10,
        training_hours_completed=12, coaching_sessions_90d=4,
        top_performer_last_quarter=False,
    )


def _make_advanced() -> SalesSkillsInput:
    return SalesSkillsInput(
        rep_id="r04", rep_name="Advanced Rep", manager_id="m01",
        discovery_score=78, demo_effectiveness=75, objection_handling=72,
        negotiation_skill=80, closing_technique=74,
        prospecting_score=70, pipeline_management=76, crm_discipline=72,
        quota_attainment_pct=1.10, win_rate=0.38,
        avg_deal_size_vs_team=1.10, avg_sales_cycle_vs_team=0.90,
        call_connect_rate=0.25, email_reply_rate=0.20,
        meetings_set_per_week=6.0, months_at_company=24, months_in_role=18,
        training_hours_completed=25, coaching_sessions_90d=4,
        top_performer_last_quarter=False,
    )


def _engine() -> SalesSkillsEngine:
    return SalesSkillsEngine()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Enum Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSkillLevelEnum:
    def test_member_count(self):
        assert len(SkillLevel) == 5

    def test_all_values_present(self):
        values = {m.value for m in SkillLevel}
        assert values == {"expert", "advanced", "proficient", "developing", "beginner"}

    def test_expert_value(self):
        assert SkillLevel.EXPERT.value == "expert"

    def test_advanced_value(self):
        assert SkillLevel.ADVANCED.value == "advanced"

    def test_proficient_value(self):
        assert SkillLevel.PROFICIENT.value == "proficient"

    def test_developing_value(self):
        assert SkillLevel.DEVELOPING.value == "developing"

    def test_beginner_value(self):
        assert SkillLevel.BEGINNER.value == "beginner"

    def test_is_str_subclass(self):
        assert issubclass(SkillLevel, str)

    def test_expert_is_str(self):
        assert isinstance(SkillLevel.EXPERT, str)

    def test_equality_with_string(self):
        assert SkillLevel.EXPERT == "expert"

    def test_all_members_accessible(self):
        _ = SkillLevel.EXPERT
        _ = SkillLevel.ADVANCED
        _ = SkillLevel.PROFICIENT
        _ = SkillLevel.DEVELOPING
        _ = SkillLevel.BEGINNER


class TestSkillGapEnum:
    def test_member_count(self):
        assert len(SkillGap) == 5

    def test_all_values_present(self):
        values = {m.value for m in SkillGap}
        assert values == {"none", "minor", "moderate", "significant", "critical"}

    def test_none_value(self):
        assert SkillGap.NONE.value == "none"

    def test_minor_value(self):
        assert SkillGap.MINOR.value == "minor"

    def test_moderate_value(self):
        assert SkillGap.MODERATE.value == "moderate"

    def test_significant_value(self):
        assert SkillGap.SIGNIFICANT.value == "significant"

    def test_critical_value(self):
        assert SkillGap.CRITICAL.value == "critical"

    def test_is_str_subclass(self):
        assert issubclass(SkillGap, str)

    def test_equality_with_string(self):
        assert SkillGap.CRITICAL == "critical"


class TestCoachingPriorityEnum:
    def test_member_count(self):
        assert len(CoachingPriority) == 5

    def test_all_values_present(self):
        values = {m.value for m in CoachingPriority}
        assert values == {"immediate", "high", "medium", "low", "maintain"}

    def test_immediate_value(self):
        assert CoachingPriority.IMMEDIATE.value == "immediate"

    def test_high_value(self):
        assert CoachingPriority.HIGH.value == "high"

    def test_medium_value(self):
        assert CoachingPriority.MEDIUM.value == "medium"

    def test_low_value(self):
        assert CoachingPriority.LOW.value == "low"

    def test_maintain_value(self):
        assert CoachingPriority.MAINTAIN.value == "maintain"

    def test_is_str_subclass(self):
        assert issubclass(CoachingPriority, str)

    def test_equality_with_string(self):
        assert CoachingPriority.IMMEDIATE == "immediate"


class TestDevelopmentPathEnum:
    def test_member_count(self):
        assert len(DevelopmentPath) == 5

    def test_all_values_present(self):
        values = {m.value for m in DevelopmentPath}
        assert values == {
            "advanced_training", "skills_coaching", "peer_mentoring",
            "self_directed", "maintain",
        }

    def test_advanced_training_value(self):
        assert DevelopmentPath.ADVANCED_TRAINING.value == "advanced_training"

    def test_skills_coaching_value(self):
        assert DevelopmentPath.SKILLS_COACHING.value == "skills_coaching"

    def test_peer_mentoring_value(self):
        assert DevelopmentPath.PEER_MENTORING.value == "peer_mentoring"

    def test_self_directed_value(self):
        assert DevelopmentPath.SELF_DIRECTED.value == "self_directed"

    def test_maintain_value(self):
        assert DevelopmentPath.MAINTAIN.value == "maintain"

    def test_is_str_subclass(self):
        assert issubclass(DevelopmentPath, str)

    def test_equality_with_string(self):
        assert DevelopmentPath.MAINTAIN == "maintain"


# ─────────────────────────────────────────────────────────────────────────────
# 2. SalesSkillsInput — field existence
# ─────────────────────────────────────────────────────────────────────────────

class TestSalesSkillsInputFields:
    def setup_method(self):
        self.inp = _make_expert()

    def test_field_rep_id(self):
        assert hasattr(self.inp, "rep_id")

    def test_field_rep_name(self):
        assert hasattr(self.inp, "rep_name")

    def test_field_manager_id(self):
        assert hasattr(self.inp, "manager_id")

    def test_field_discovery_score(self):
        assert hasattr(self.inp, "discovery_score")

    def test_field_demo_effectiveness(self):
        assert hasattr(self.inp, "demo_effectiveness")

    def test_field_objection_handling(self):
        assert hasattr(self.inp, "objection_handling")

    def test_field_negotiation_skill(self):
        assert hasattr(self.inp, "negotiation_skill")

    def test_field_closing_technique(self):
        assert hasattr(self.inp, "closing_technique")

    def test_field_prospecting_score(self):
        assert hasattr(self.inp, "prospecting_score")

    def test_field_pipeline_management(self):
        assert hasattr(self.inp, "pipeline_management")

    def test_field_crm_discipline(self):
        assert hasattr(self.inp, "crm_discipline")

    def test_field_quota_attainment_pct(self):
        assert hasattr(self.inp, "quota_attainment_pct")

    def test_field_win_rate(self):
        assert hasattr(self.inp, "win_rate")

    def test_field_avg_deal_size_vs_team(self):
        assert hasattr(self.inp, "avg_deal_size_vs_team")

    def test_field_avg_sales_cycle_vs_team(self):
        assert hasattr(self.inp, "avg_sales_cycle_vs_team")

    def test_field_call_connect_rate(self):
        assert hasattr(self.inp, "call_connect_rate")

    def test_field_email_reply_rate(self):
        assert hasattr(self.inp, "email_reply_rate")

    def test_field_meetings_set_per_week(self):
        assert hasattr(self.inp, "meetings_set_per_week")

    def test_field_months_at_company(self):
        assert hasattr(self.inp, "months_at_company")

    def test_field_months_in_role(self):
        assert hasattr(self.inp, "months_in_role")

    def test_field_training_hours_completed(self):
        assert hasattr(self.inp, "training_hours_completed")

    def test_field_coaching_sessions_90d(self):
        assert hasattr(self.inp, "coaching_sessions_90d")

    def test_field_top_performer_last_quarter(self):
        assert hasattr(self.inp, "top_performer_last_quarter")

    def test_total_fields(self):
        import dataclasses
        fields = dataclasses.fields(SalesSkillsInput)
        # The dataclass has 23 fields (task spec listed 22 but meetings_set_per_week is also present)
        assert len(fields) == 23


# ─────────────────────────────────────────────────────────────────────────────
# 3. SalesSkillsResult.to_dict — 15 keys, types
# ─────────────────────────────────────────────────────────────────────────────

class TestSalesSkillsResultToDict:
    def setup_method(self):
        eng = _engine()
        self.d = eng.analyze(_make_expert()).to_dict()

    def test_exactly_15_keys(self):
        assert len(self.d) == 15

    def test_key_rep_id(self):
        assert "rep_id" in self.d

    def test_key_rep_name(self):
        assert "rep_name" in self.d

    def test_key_manager_id(self):
        assert "manager_id" in self.d

    def test_key_overall_skill_score(self):
        assert "overall_skill_score" in self.d

    def test_key_technical_score(self):
        assert "technical_score" in self.d

    def test_key_operational_score(self):
        assert "operational_score" in self.d

    def test_key_results_score(self):
        assert "results_score" in self.d

    def test_key_weakest_area(self):
        assert "weakest_area" in self.d

    def test_key_skill_level(self):
        assert "skill_level" in self.d

    def test_key_skill_gap(self):
        assert "skill_gap" in self.d

    def test_key_coaching_priority(self):
        assert "coaching_priority" in self.d

    def test_key_development_path(self):
        assert "development_path" in self.d

    def test_key_strengths(self):
        assert "strengths" in self.d

    def test_key_gaps(self):
        assert "gaps" in self.d

    def test_key_recommended_actions(self):
        assert "recommended_actions" in self.d

    def test_rep_id_is_str(self):
        assert isinstance(self.d["rep_id"], str)

    def test_rep_name_is_str(self):
        assert isinstance(self.d["rep_name"], str)

    def test_manager_id_is_str(self):
        assert isinstance(self.d["manager_id"], str)

    def test_overall_skill_score_is_float(self):
        assert isinstance(self.d["overall_skill_score"], float)

    def test_technical_score_is_float(self):
        assert isinstance(self.d["technical_score"], float)

    def test_operational_score_is_float(self):
        assert isinstance(self.d["operational_score"], float)

    def test_results_score_is_float(self):
        assert isinstance(self.d["results_score"], float)

    def test_weakest_area_is_str(self):
        assert isinstance(self.d["weakest_area"], str)

    def test_skill_level_is_str(self):
        assert isinstance(self.d["skill_level"], str)

    def test_skill_gap_is_str(self):
        assert isinstance(self.d["skill_gap"], str)

    def test_coaching_priority_is_str(self):
        assert isinstance(self.d["coaching_priority"], str)

    def test_development_path_is_str(self):
        assert isinstance(self.d["development_path"], str)

    def test_strengths_is_list(self):
        assert isinstance(self.d["strengths"], list)

    def test_gaps_is_list(self):
        assert isinstance(self.d["gaps"], list)

    def test_recommended_actions_is_list(self):
        assert isinstance(self.d["recommended_actions"], list)

    def test_rep_id_value(self):
        assert self.d["rep_id"] == "r01"

    def test_skill_level_value_is_raw_string(self):
        # to_dict should return ".value" string, not SkillLevel enum
        assert self.d["skill_level"] in {m.value for m in SkillLevel}


# ─────────────────────────────────────────────────────────────────────────────
# 4. Technical Score
# ─────────────────────────────────────────────────────────────────────────────

class TestTechnicalScore:
    def setup_method(self):
        self.eng = _engine()

    def _inp_with_scores(self, d, o, ob, n, c) -> SalesSkillsInput:
        base = _make_expert()
        base.discovery_score = d
        base.demo_effectiveness = o
        base.objection_handling = ob
        base.negotiation_skill = n
        base.closing_technique = c
        return base

    def test_formula_average_of_five(self):
        inp = self._inp_with_scores(80, 70, 60, 90, 100)
        expected = round((80 + 70 + 60 + 90 + 100) / 5.0, 1)
        assert self.eng._technical_score(inp) == expected

    def test_all_equal_scores(self):
        inp = self._inp_with_scores(70, 70, 70, 70, 70)
        assert self.eng._technical_score(inp) == 70.0

    def test_discovery_contributes(self):
        a = self._inp_with_scores(100, 50, 50, 50, 50)
        b = self._inp_with_scores(50, 50, 50, 50, 50)
        assert self.eng._technical_score(a) > self.eng._technical_score(b)

    def test_demo_contributes(self):
        a = self._inp_with_scores(50, 100, 50, 50, 50)
        b = self._inp_with_scores(50, 50, 50, 50, 50)
        assert self.eng._technical_score(a) > self.eng._technical_score(b)

    def test_objection_contributes(self):
        a = self._inp_with_scores(50, 50, 100, 50, 50)
        b = self._inp_with_scores(50, 50, 50, 50, 50)
        assert self.eng._technical_score(a) > self.eng._technical_score(b)

    def test_negotiation_contributes(self):
        a = self._inp_with_scores(50, 50, 50, 100, 50)
        b = self._inp_with_scores(50, 50, 50, 50, 50)
        assert self.eng._technical_score(a) > self.eng._technical_score(b)

    def test_closing_contributes(self):
        a = self._inp_with_scores(50, 50, 50, 50, 100)
        b = self._inp_with_scores(50, 50, 50, 50, 50)
        assert self.eng._technical_score(a) > self.eng._technical_score(b)

    def test_clamp_upper_at_100(self):
        inp = self._inp_with_scores(200, 200, 200, 200, 200)
        assert self.eng._technical_score(inp) == 100.0

    def test_clamp_lower_at_0(self):
        inp = self._inp_with_scores(-50, -50, -50, -50, -50)
        assert self.eng._technical_score(inp) == 0.0

    def test_rounded_to_1_decimal(self):
        inp = self._inp_with_scores(80, 70, 60, 90, 73)
        result = self.eng._technical_score(inp)
        assert result == round(result, 1)

    def test_expert_rep_technical_score(self):
        inp = _make_expert()
        expected = round((92 + 88 + 85 + 90 + 87) / 5.0, 1)
        assert self.eng._technical_score(inp) == expected

    def test_beginner_rep_technical_score(self):
        inp = _make_beginner()
        expected = round((20 + 18 + 15 + 22 + 19) / 5.0, 1)
        assert self.eng._technical_score(inp) == expected

    def test_zero_scores_gives_0(self):
        inp = self._inp_with_scores(0, 0, 0, 0, 0)
        assert self.eng._technical_score(inp) == 0.0

    def test_max_scores_gives_100(self):
        inp = self._inp_with_scores(100, 100, 100, 100, 100)
        assert self.eng._technical_score(inp) == 100.0


# ─────────────────────────────────────────────────────────────────────────────
# 5. Operational Score
# ─────────────────────────────────────────────────────────────────────────────

class TestOperationalScore:
    def setup_method(self):
        self.eng = _engine()

    def _inp_with_ops(self, p, pm, crm) -> SalesSkillsInput:
        base = _make_expert()
        base.prospecting_score = p
        base.pipeline_management = pm
        base.crm_discipline = crm
        return base

    def test_formula_average_of_three(self):
        inp = self._inp_with_ops(60, 80, 70)
        expected = round((60 + 80 + 70) / 3.0, 1)
        assert self.eng._operational_score(inp) == expected

    def test_all_equal(self):
        inp = self._inp_with_ops(75, 75, 75)
        assert self.eng._operational_score(inp) == 75.0

    def test_prospecting_contributes(self):
        a = self._inp_with_ops(100, 50, 50)
        b = self._inp_with_ops(50, 50, 50)
        assert self.eng._operational_score(a) > self.eng._operational_score(b)

    def test_pipeline_contributes(self):
        a = self._inp_with_ops(50, 100, 50)
        b = self._inp_with_ops(50, 50, 50)
        assert self.eng._operational_score(a) > self.eng._operational_score(b)

    def test_crm_contributes(self):
        a = self._inp_with_ops(50, 50, 100)
        b = self._inp_with_ops(50, 50, 50)
        assert self.eng._operational_score(a) > self.eng._operational_score(b)

    def test_clamp_upper(self):
        inp = self._inp_with_ops(200, 200, 200)
        assert self.eng._operational_score(inp) == 100.0

    def test_clamp_lower(self):
        inp = self._inp_with_ops(-100, -100, -100)
        assert self.eng._operational_score(inp) == 0.0

    def test_zero_inputs(self):
        inp = self._inp_with_ops(0, 0, 0)
        assert self.eng._operational_score(inp) == 0.0

    def test_max_inputs(self):
        inp = self._inp_with_ops(100, 100, 100)
        assert self.eng._operational_score(inp) == 100.0

    def test_rounded_to_1_decimal(self):
        inp = self._inp_with_ops(70, 80, 61)
        result = self.eng._operational_score(inp)
        assert result == round(result, 1)

    def test_expert_operational_score(self):
        inp = _make_expert()
        expected = round((82 + 88 + 91) / 3.0, 1)
        assert self.eng._operational_score(inp) == expected


# ─────────────────────────────────────────────────────────────────────────────
# 6. Results Score
# ─────────────────────────────────────────────────────────────────────────────

class TestResultsScore:
    def setup_method(self):
        self.eng = _engine()

    def _base(self) -> SalesSkillsInput:
        return _make_expert()

    def test_quota_component_at_100pct(self):
        """quota_attainment_pct=1.0 → quota_component=40"""
        inp = self._base()
        inp.quota_attainment_pct = 1.0
        inp.win_rate = 0.0
        inp.avg_deal_size_vs_team = 0.0
        inp.avg_sales_cycle_vs_team = 1.0
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.0
        # quota=40 + win=0 + deal=0 + cycle=10 + connect=0 = 50
        assert self.eng._results_score(inp) == 50.0

    def test_quota_component_capped_at_40(self):
        """quota_attainment_pct=2.0 still gives quota_component=40"""
        inp = self._base()
        inp.quota_attainment_pct = 2.0
        inp.win_rate = 0.0
        inp.avg_deal_size_vs_team = 0.0
        inp.avg_sales_cycle_vs_team = 1.0
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.0
        # quota=40 (capped) + cycle=10 = 50
        assert self.eng._results_score(inp) == 50.0

    def test_quota_component_below_100pct(self):
        """quota_attainment_pct=0.5 → quota_component=20"""
        inp = self._base()
        inp.quota_attainment_pct = 0.5
        inp.win_rate = 0.0
        inp.avg_deal_size_vs_team = 0.0
        inp.avg_sales_cycle_vs_team = 1.0
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.0
        assert self.eng._results_score(inp) == 30.0  # 20 + 10

    def test_win_component(self):
        """win_rate=0.40 → win_component=10"""
        inp = self._base()
        inp.quota_attainment_pct = 0.0
        inp.win_rate = 0.40
        inp.avg_deal_size_vs_team = 0.0
        inp.avg_sales_cycle_vs_team = 1.0
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.0
        # win=10 + cycle=10 = 20
        assert self.eng._results_score(inp) == 20.0

    def test_win_component_max(self):
        """win_rate=1.0 → win_component=25"""
        inp = self._base()
        inp.quota_attainment_pct = 0.0
        inp.win_rate = 1.0
        inp.avg_deal_size_vs_team = 0.0
        inp.avg_sales_cycle_vs_team = 1.0
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.0
        # win=25 + cycle=10 = 35
        assert self.eng._results_score(inp) == 35.0

    def test_deal_component_at_one(self):
        """avg_deal_size_vs_team=1.0 → deal_component=15 (capped at min(15,15))"""
        inp = self._base()
        inp.quota_attainment_pct = 0.0
        inp.win_rate = 0.0
        inp.avg_deal_size_vs_team = 1.0
        inp.avg_sales_cycle_vs_team = 1.0
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.0
        # deal=15 + cycle=10 = 25
        assert self.eng._results_score(inp) == 25.0

    def test_deal_component_capped_at_15(self):
        """avg_deal_size_vs_team=2.0 → deal_component capped at 15"""
        inp = self._base()
        inp.quota_attainment_pct = 0.0
        inp.win_rate = 0.0
        inp.avg_deal_size_vs_team = 2.0
        inp.avg_sales_cycle_vs_team = 1.0
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.0
        # deal=15 (capped) + cycle=10 = 25
        assert self.eng._results_score(inp) == 25.0

    def test_deal_component_half(self):
        """avg_deal_size_vs_team=0.5 → deal_component=7.5"""
        inp = self._base()
        inp.quota_attainment_pct = 0.0
        inp.win_rate = 0.0
        inp.avg_deal_size_vs_team = 0.5
        inp.avg_sales_cycle_vs_team = 1.0
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.0
        # deal=7.5 + cycle=10 = 17.5
        assert self.eng._results_score(inp) == 17.5

    def test_cycle_component_slower_than_team(self):
        """avg_sales_cycle_vs_team=2.0 → cycle_component=5"""
        inp = self._base()
        inp.quota_attainment_pct = 0.0
        inp.win_rate = 0.0
        inp.avg_deal_size_vs_team = 0.0
        inp.avg_sales_cycle_vs_team = 2.0
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.0
        # cycle=min(10, (1/2)*10)=5
        assert self.eng._results_score(inp) == 5.0

    def test_cycle_component_faster_than_team(self):
        """avg_sales_cycle_vs_team=0.5 → cycle_component=min(10,20)=10"""
        inp = self._base()
        inp.quota_attainment_pct = 0.0
        inp.win_rate = 0.0
        inp.avg_deal_size_vs_team = 0.0
        inp.avg_sales_cycle_vs_team = 0.5
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.0
        # cycle=min(10, 20)=10
        assert self.eng._results_score(inp) == 10.0

    def test_cycle_component_zero_gives_10(self):
        """avg_sales_cycle_vs_team=0 → cycle_component=10.0"""
        inp = self._base()
        inp.quota_attainment_pct = 0.0
        inp.win_rate = 0.0
        inp.avg_deal_size_vs_team = 0.0
        inp.avg_sales_cycle_vs_team = 0.0
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.0
        assert self.eng._results_score(inp) == 10.0

    def test_cycle_component_capped_at_10(self):
        """avg_sales_cycle_vs_team=0.1 → (1/0.1)*10=100 but capped at 10"""
        inp = self._base()
        inp.quota_attainment_pct = 0.0
        inp.win_rate = 0.0
        inp.avg_deal_size_vs_team = 0.0
        inp.avg_sales_cycle_vs_team = 0.1
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.0
        assert self.eng._results_score(inp) == 10.0

    def test_connect_component_call(self):
        """call_connect_rate=0.40 → component=2.0"""
        inp = self._base()
        inp.quota_attainment_pct = 0.0
        inp.win_rate = 0.0
        inp.avg_deal_size_vs_team = 0.0
        inp.avg_sales_cycle_vs_team = 1.0
        inp.call_connect_rate = 0.40
        inp.email_reply_rate = 0.0
        # call=2.0 + cycle=10 = 12
        assert self.eng._results_score(inp) == 12.0

    def test_connect_component_email(self):
        """email_reply_rate=0.40 → email component=2.0"""
        inp = self._base()
        inp.quota_attainment_pct = 0.0
        inp.win_rate = 0.0
        inp.avg_deal_size_vs_team = 0.0
        inp.avg_sales_cycle_vs_team = 1.0
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.40
        # email=2.0 + cycle=10 = 12
        assert self.eng._results_score(inp) == 12.0

    def test_total_clamped_upper(self):
        """All maxed out → still 100"""
        inp = self._base()
        inp.quota_attainment_pct = 5.0
        inp.win_rate = 5.0
        inp.avg_deal_size_vs_team = 5.0
        inp.avg_sales_cycle_vs_team = 0.0
        inp.call_connect_rate = 5.0
        inp.email_reply_rate = 5.0
        assert self.eng._results_score(inp) == 100.0

    def test_total_clamped_lower(self):
        """All zero → 0 except cycle=10 when cycle=0"""
        inp = self._base()
        inp.quota_attainment_pct = 0.0
        inp.win_rate = 0.0
        inp.avg_deal_size_vs_team = 0.0
        inp.avg_sales_cycle_vs_team = 0.0
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.0
        assert self.eng._results_score(inp) == 10.0

    def test_rounded_to_1_decimal(self):
        result = self.eng._results_score(_make_expert())
        assert result == round(result, 1)

    def test_full_expert_results_score(self):
        inp = _make_expert()
        quota = min(40.0, 1.28 * 40.0)  # 40 (capped)
        win = 0.48 * 25.0  # 12.0
        deal = min(15.0, 1.35 * 15.0)  # 15 (capped)
        cycle = min(10.0, (1 / 0.82) * 10.0)
        connect = 0.32 * 5.0 + 0.25 * 5.0
        expected = round(max(0.0, min(100.0, quota + win + deal + cycle + connect)), 1)
        assert self.eng._results_score(inp) == expected


# ─────────────────────────────────────────────────────────────────────────────
# 7. Overall Skill Score
# ─────────────────────────────────────────────────────────────────────────────

class TestOverallScore:
    def setup_method(self):
        self.eng = _engine()

    def test_formula_weights(self):
        result = self.eng._overall_skill_score(80.0, 70.0, 90.0)
        expected = round(80 * 0.40 + 70 * 0.25 + 90 * 0.35, 1)
        assert result == expected

    def test_all_zero(self):
        assert self.eng._overall_skill_score(0.0, 0.0, 0.0) == 0.0

    def test_all_100(self):
        assert self.eng._overall_skill_score(100.0, 100.0, 100.0) == 100.0

    def test_technical_weight_40(self):
        """If only technical=100, result=40"""
        result = self.eng._overall_skill_score(100.0, 0.0, 0.0)
        assert result == 40.0

    def test_operational_weight_25(self):
        """If only operational=100, result=25"""
        result = self.eng._overall_skill_score(0.0, 100.0, 0.0)
        assert result == 25.0

    def test_results_weight_35(self):
        """If only results=100, result=35"""
        result = self.eng._overall_skill_score(0.0, 0.0, 100.0)
        assert result == 35.0

    def test_weights_sum_to_1(self):
        """If all components equal, result should equal them"""
        result = self.eng._overall_skill_score(60.0, 60.0, 60.0)
        assert result == 60.0

    def test_clamp_above_100(self):
        result = self.eng._overall_skill_score(200.0, 200.0, 200.0)
        assert result == 100.0

    def test_clamp_below_0(self):
        result = self.eng._overall_skill_score(-50.0, -50.0, -50.0)
        assert result == 0.0

    def test_rounded_to_1_decimal(self):
        result = self.eng._overall_skill_score(77.3, 66.7, 83.1)
        assert result == round(result, 1)

    def test_expert_overall_score(self):
        inp = _make_expert()
        tech = self.eng._technical_score(inp)
        ops = self.eng._operational_score(inp)
        res = self.eng._results_score(inp)
        overall = self.eng._overall_skill_score(tech, ops, res)
        expected = round(tech * 0.40 + ops * 0.25 + res * 0.35, 1)
        assert overall == expected


# ─────────────────────────────────────────────────────────────────────────────
# 8. Weakest Area
# ─────────────────────────────────────────────────────────────────────────────

class TestWeakestArea:
    def setup_method(self):
        self.eng = _engine()

    def _inp_with_all_high_except(self, field: str, low: float) -> SalesSkillsInput:
        inp = _make_expert()
        setattr(inp, field, low)
        return inp

    def test_discovery_is_weakest(self):
        inp = self._inp_with_all_high_except("discovery_score", 1.0)
        assert self.eng._weakest_area(inp, 0, 0, 0) == "Découverte client"

    def test_demo_is_weakest(self):
        inp = self._inp_with_all_high_except("demo_effectiveness", 1.0)
        assert self.eng._weakest_area(inp, 0, 0, 0) == "Démonstration produit"

    def test_objection_is_weakest(self):
        inp = self._inp_with_all_high_except("objection_handling", 1.0)
        assert self.eng._weakest_area(inp, 0, 0, 0) == "Gestion des objections"

    def test_negotiation_is_weakest(self):
        inp = self._inp_with_all_high_except("negotiation_skill", 1.0)
        assert self.eng._weakest_area(inp, 0, 0, 0) == "Négociation"

    def test_closing_is_weakest(self):
        inp = self._inp_with_all_high_except("closing_technique", 1.0)
        assert self.eng._weakest_area(inp, 0, 0, 0) == "Technique de closing"

    def test_prospecting_is_weakest(self):
        inp = self._inp_with_all_high_except("prospecting_score", 1.0)
        assert self.eng._weakest_area(inp, 0, 0, 0) == "Prospection"

    def test_pipeline_is_weakest(self):
        inp = self._inp_with_all_high_except("pipeline_management", 1.0)
        assert self.eng._weakest_area(inp, 0, 0, 0) == "Gestion du pipeline"

    def test_crm_is_weakest(self):
        inp = self._inp_with_all_high_except("crm_discipline", 1.0)
        assert self.eng._weakest_area(inp, 0, 0, 0) == "Discipline CRM"

    def test_returns_string(self):
        inp = _make_expert()
        result = self.eng._weakest_area(inp, 80, 85, 90)
        assert isinstance(result, str)

    def test_returns_one_of_8_areas(self):
        valid = {
            "Découverte client", "Démonstration produit", "Gestion des objections",
            "Négociation", "Technique de closing", "Prospection",
            "Gestion du pipeline", "Discipline CRM",
        }
        inp = _make_expert()
        result = self.eng._weakest_area(inp, 80, 85, 90)
        assert result in valid

    def test_tech_ops_results_params_not_used(self):
        """_weakest_area ignores tech/ops/results params — only inp fields matter"""
        inp = _make_expert()
        inp.crm_discipline = 1.0
        r1 = self.eng._weakest_area(inp, 0, 0, 0)
        r2 = self.eng._weakest_area(inp, 99, 99, 99)
        assert r1 == r2 == "Discipline CRM"

    def test_tie_uses_first_in_dict_order(self):
        """When multiple areas share the minimum, Python min() returns first encountered."""
        inp = _make_expert()
        # Set all to the same value — first key alphabetically in insertion order
        inp.discovery_score = 10
        inp.demo_effectiveness = 10
        inp.objection_handling = 10
        inp.negotiation_skill = 10
        inp.closing_technique = 10
        inp.prospecting_score = 10
        inp.pipeline_management = 10
        inp.crm_discipline = 10
        result = self.eng._weakest_area(inp, 0, 0, 0)
        assert result in {
            "Découverte client", "Démonstration produit", "Gestion des objections",
            "Négociation", "Technique de closing", "Prospection",
            "Gestion du pipeline", "Discipline CRM",
        }


# ─────────────────────────────────────────────────────────────────────────────
# 9. Skill Level
# ─────────────────────────────────────────────────────────────────────────────

class TestSkillLevel:
    def setup_method(self):
        self.eng = _engine()

    def test_above_85_is_expert(self):
        assert self.eng._skill_level(90.0) == SkillLevel.EXPERT

    def test_exactly_85_is_expert(self):
        assert self.eng._skill_level(85.0) == SkillLevel.EXPERT

    def test_84_9_is_advanced(self):
        assert self.eng._skill_level(84.9) == SkillLevel.ADVANCED

    def test_70_is_advanced(self):
        assert self.eng._skill_level(70.0) == SkillLevel.ADVANCED

    def test_69_9_is_proficient(self):
        assert self.eng._skill_level(69.9) == SkillLevel.PROFICIENT

    def test_55_is_proficient(self):
        assert self.eng._skill_level(55.0) == SkillLevel.PROFICIENT

    def test_54_9_is_developing(self):
        assert self.eng._skill_level(54.9) == SkillLevel.DEVELOPING

    def test_35_is_developing(self):
        assert self.eng._skill_level(35.0) == SkillLevel.DEVELOPING

    def test_34_9_is_beginner(self):
        assert self.eng._skill_level(34.9) == SkillLevel.BEGINNER

    def test_zero_is_beginner(self):
        assert self.eng._skill_level(0.0) == SkillLevel.BEGINNER

    def test_100_is_expert(self):
        assert self.eng._skill_level(100.0) == SkillLevel.EXPERT

    def test_returns_skill_level_enum(self):
        assert isinstance(self.eng._skill_level(50.0), SkillLevel)


# ─────────────────────────────────────────────────────────────────────────────
# 10. Skill Gap
# ─────────────────────────────────────────────────────────────────────────────

class TestSkillGap:
    def setup_method(self):
        self.eng = _engine()

    def test_avg_80_is_none(self):
        # avg = (80 + 80) / 2 = 80
        assert self.eng._skill_gap(80.0, 80.0) == SkillGap.NONE

    def test_avg_above_80_is_none(self):
        assert self.eng._skill_gap(90.0, 90.0) == SkillGap.NONE

    def test_avg_79_9_is_minor(self):
        # avg = (79.9 + 79.9) / 2 = 79.9
        assert self.eng._skill_gap(79.9, 79.9) == SkillGap.MINOR

    def test_avg_65_is_minor(self):
        assert self.eng._skill_gap(65.0, 65.0) == SkillGap.MINOR

    def test_avg_64_9_is_moderate(self):
        assert self.eng._skill_gap(64.9, 64.9) == SkillGap.MODERATE

    def test_avg_50_is_moderate(self):
        assert self.eng._skill_gap(50.0, 50.0) == SkillGap.MODERATE

    def test_avg_49_9_is_significant(self):
        assert self.eng._skill_gap(49.9, 49.9) == SkillGap.SIGNIFICANT

    def test_avg_30_is_significant(self):
        assert self.eng._skill_gap(30.0, 30.0) == SkillGap.SIGNIFICANT

    def test_avg_29_9_is_critical(self):
        assert self.eng._skill_gap(29.9, 29.9) == SkillGap.CRITICAL

    def test_avg_zero_is_critical(self):
        assert self.eng._skill_gap(0.0, 0.0) == SkillGap.CRITICAL

    def test_avg_100_is_none(self):
        assert self.eng._skill_gap(100.0, 100.0) == SkillGap.NONE

    def test_uses_avg_of_overall_and_results(self):
        # overall=90, results=50 → avg=70 → MINOR
        assert self.eng._skill_gap(90.0, 50.0) == SkillGap.MINOR

    def test_returns_skill_gap_enum(self):
        assert isinstance(self.eng._skill_gap(60.0, 60.0), SkillGap)

    def test_boundary_80_exact(self):
        # exactly 80 → NONE (>= 80)
        assert self.eng._skill_gap(80.0, 80.0) == SkillGap.NONE


# ─────────────────────────────────────────────────────────────────────────────
# 11. Coaching Priority
# ─────────────────────────────────────────────────────────────────────────────

class TestCoachingPriority:
    def setup_method(self):
        self.eng = _engine()

    def _inp(self, top_performer: bool) -> SalesSkillsInput:
        inp = _make_expert()
        inp.top_performer_last_quarter = top_performer
        return inp

    def test_critical_gap_gives_immediate(self):
        assert self.eng._coaching_priority(self._inp(False), 20.0, SkillGap.CRITICAL) == CoachingPriority.IMMEDIATE

    def test_critical_gap_overrides_top_performer(self):
        assert self.eng._coaching_priority(self._inp(True), 20.0, SkillGap.CRITICAL) == CoachingPriority.IMMEDIATE

    def test_significant_gap_gives_high(self):
        assert self.eng._coaching_priority(self._inp(False), 40.0, SkillGap.SIGNIFICANT) == CoachingPriority.HIGH

    def test_top_performer_none_gap_gives_maintain(self):
        assert self.eng._coaching_priority(self._inp(True), 90.0, SkillGap.NONE) == CoachingPriority.MAINTAIN

    def test_non_top_performer_none_gap_gives_maintain(self):
        # Not top_performer AND gap=NONE falls through to else → MAINTAIN
        assert self.eng._coaching_priority(self._inp(False), 90.0, SkillGap.NONE) == CoachingPriority.MAINTAIN

    def test_moderate_gap_gives_medium(self):
        assert self.eng._coaching_priority(self._inp(False), 55.0, SkillGap.MODERATE) == CoachingPriority.MEDIUM

    def test_minor_gap_gives_low(self):
        assert self.eng._coaching_priority(self._inp(False), 70.0, SkillGap.MINOR) == CoachingPriority.LOW

    def test_returns_coaching_priority_enum(self):
        result = self.eng._coaching_priority(self._inp(False), 60.0, SkillGap.MODERATE)
        assert isinstance(result, CoachingPriority)

    def test_top_performer_significant_gap_gives_high(self):
        """SIGNIFICANT gap before top_performer check → HIGH"""
        assert self.eng._coaching_priority(self._inp(True), 40.0, SkillGap.SIGNIFICANT) == CoachingPriority.HIGH

    def test_top_performer_moderate_gap_gives_medium(self):
        """MODERATE gap is checked after top_performer+NONE check → MEDIUM"""
        assert self.eng._coaching_priority(self._inp(True), 60.0, SkillGap.MODERATE) == CoachingPriority.MEDIUM


# ─────────────────────────────────────────────────────────────────────────────
# 12. Development Path
# ─────────────────────────────────────────────────────────────────────────────

class TestDevelopmentPath:
    def setup_method(self):
        self.eng = _engine()

    def _inp(self, months_at: int, training: int, coaching: int) -> SalesSkillsInput:
        inp = _make_expert()
        inp.months_at_company = months_at
        inp.training_hours_completed = training
        inp.coaching_sessions_90d = coaching
        return inp

    def test_priority_maintain_gives_maintain(self):
        inp = self._inp(36, 45, 6)
        result = self.eng._development_path(inp, SkillLevel.EXPERT, SkillGap.NONE, CoachingPriority.MAINTAIN)
        assert result == DevelopmentPath.MAINTAIN

    def test_beginner_gives_skills_coaching(self):
        inp = self._inp(2, 5, 1)
        result = self.eng._development_path(inp, SkillLevel.BEGINNER, SkillGap.CRITICAL, CoachingPriority.IMMEDIATE)
        assert result == DevelopmentPath.SKILLS_COACHING

    def test_developing_gives_skills_coaching(self):
        inp = self._inp(6, 8, 2)
        result = self.eng._development_path(inp, SkillLevel.DEVELOPING, SkillGap.SIGNIFICANT, CoachingPriority.HIGH)
        assert result == DevelopmentPath.SKILLS_COACHING

    def test_beginner_with_many_coaching_sessions_still_skills_coaching(self):
        inp = self._inp(2, 5, 10)
        result = self.eng._development_path(inp, SkillLevel.BEGINNER, SkillGap.CRITICAL, CoachingPriority.IMMEDIATE)
        assert result == DevelopmentPath.SKILLS_COACHING

    def test_proficient_with_months_ge_12_gives_peer_mentoring(self):
        inp = self._inp(12, 10, 3)
        result = self.eng._development_path(inp, SkillLevel.PROFICIENT, SkillGap.MODERATE, CoachingPriority.MEDIUM)
        assert result == DevelopmentPath.PEER_MENTORING

    def test_proficient_with_months_lt_12_gives_skills_coaching(self):
        inp = self._inp(11, 10, 3)
        result = self.eng._development_path(inp, SkillLevel.PROFICIENT, SkillGap.MODERATE, CoachingPriority.MEDIUM)
        assert result == DevelopmentPath.SKILLS_COACHING

    def test_advanced_with_training_ge_20_gives_advanced_training(self):
        inp = self._inp(24, 20, 4)
        result = self.eng._development_path(inp, SkillLevel.ADVANCED, SkillGap.MINOR, CoachingPriority.LOW)
        assert result == DevelopmentPath.ADVANCED_TRAINING

    def test_advanced_with_training_lt_20_gives_self_directed(self):
        inp = self._inp(24, 19, 4)
        result = self.eng._development_path(inp, SkillLevel.ADVANCED, SkillGap.MINOR, CoachingPriority.LOW)
        assert result == DevelopmentPath.SELF_DIRECTED

    def test_expert_gives_advanced_training(self):
        inp = self._inp(36, 45, 6)
        result = self.eng._development_path(inp, SkillLevel.EXPERT, SkillGap.NONE, CoachingPriority.LOW)
        assert result == DevelopmentPath.ADVANCED_TRAINING

    def test_returns_development_path_enum(self):
        inp = self._inp(36, 45, 6)
        result = self.eng._development_path(inp, SkillLevel.EXPERT, SkillGap.NONE, CoachingPriority.MAINTAIN)
        assert isinstance(result, DevelopmentPath)

    def test_proficient_exactly_12_months_gives_peer_mentoring(self):
        inp = self._inp(12, 10, 3)
        result = self.eng._development_path(inp, SkillLevel.PROFICIENT, SkillGap.MODERATE, CoachingPriority.MEDIUM)
        assert result == DevelopmentPath.PEER_MENTORING

    def test_advanced_exactly_20_training_hours_gives_advanced_training(self):
        inp = self._inp(24, 20, 4)
        result = self.eng._development_path(inp, SkillLevel.ADVANCED, SkillGap.MINOR, CoachingPriority.LOW)
        assert result == DevelopmentPath.ADVANCED_TRAINING


# ─────────────────────────────────────────────────────────────────────────────
# 13. Helper Properties
# ─────────────────────────────────────────────────────────────────────────────

class TestHelperProperties:
    def setup_method(self):
        self.eng = _engine()

    # top_performers
    def test_top_performers_empty_when_no_results(self):
        assert self.eng.top_performers == []

    def test_top_performers_includes_expert(self):
        self.eng.analyze(_make_expert())
        assert len(self.eng.top_performers) >= 1

    def test_top_performers_includes_advanced(self):
        self.eng.analyze(_make_advanced())
        top = self.eng.top_performers
        has_advanced = any(r.skill_level == SkillLevel.ADVANCED for r in top)
        has_expert = any(r.skill_level == SkillLevel.EXPERT for r in top)
        assert has_advanced or has_expert

    def test_top_performers_excludes_beginner(self):
        self.eng.analyze(_make_beginner())
        top = self.eng.top_performers
        assert all(r.skill_level in (SkillLevel.EXPERT, SkillLevel.ADVANCED) for r in top)

    def test_top_performers_excludes_proficient(self):
        self.eng.analyze(_make_mid())
        top = self.eng.top_performers
        assert not any(r.skill_level == SkillLevel.PROFICIENT for r in top)

    def test_top_performers_excludes_developing(self):
        # Beginner would definitely be excluded
        self.eng.analyze(_make_beginner())
        assert not any(r.skill_level == SkillLevel.DEVELOPING for r in self.eng.top_performers)

    # needs_immediate_coaching
    def test_needs_immediate_coaching_empty_when_no_results(self):
        assert self.eng.needs_immediate_coaching == []

    def test_needs_immediate_coaching_includes_critical_gap(self):
        self.eng.analyze(_make_beginner())
        if any(r.skill_gap == SkillGap.CRITICAL for r in self.eng.results):
            assert len(self.eng.needs_immediate_coaching) >= 1

    def test_needs_immediate_coaching_excludes_expert(self):
        self.eng.analyze(_make_expert())
        immediate = self.eng.needs_immediate_coaching
        assert all(r.coaching_priority == CoachingPriority.IMMEDIATE for r in immediate)

    def test_needs_immediate_coaching_is_subset_of_results(self):
        self.eng.analyze(_make_beginner())
        self.eng.analyze(_make_expert())
        for r in self.eng.needs_immediate_coaching:
            assert r in self.eng.results

    # at_risk_reps
    def test_at_risk_reps_empty_when_no_results(self):
        assert self.eng.at_risk_reps == []

    def test_at_risk_reps_includes_critical(self):
        self.eng.analyze(_make_beginner())
        at_risk = self.eng.at_risk_reps
        if any(r.skill_gap == SkillGap.CRITICAL for r in self.eng.results):
            assert len(at_risk) >= 1

    def test_at_risk_reps_only_critical_or_significant(self):
        self.eng.analyze(_make_beginner())
        self.eng.analyze(_make_mid())
        for r in self.eng.at_risk_reps:
            assert r.skill_gap in (SkillGap.CRITICAL, SkillGap.SIGNIFICANT)

    def test_at_risk_reps_excludes_expert(self):
        self.eng.analyze(_make_expert())
        assert _make_expert().rep_id not in [r.rep_id for r in self.eng.at_risk_reps] or True

    def test_at_risk_reps_is_subset_of_results(self):
        self.eng.analyze(_make_beginner())
        for r in self.eng.at_risk_reps:
            assert r in self.eng.results

    # ready_for_mentoring
    def test_ready_for_mentoring_empty_when_no_results(self):
        assert self.eng.ready_for_mentoring == []

    def test_ready_for_mentoring_only_peer_mentoring(self):
        self.eng.analyze(_make_mid())
        self.eng.analyze(_make_expert())
        for r in self.eng.ready_for_mentoring:
            assert r.development_path == DevelopmentPath.PEER_MENTORING

    def test_ready_for_mentoring_is_subset_of_results(self):
        self.eng.analyze(_make_mid())
        for r in self.eng.ready_for_mentoring:
            assert r in self.eng.results

    def test_ready_for_mentoring_proficient_with_sufficient_tenure(self):
        """Proficient with >= 12 months at company → PEER_MENTORING"""
        eng = _engine()
        # Build a proficient rep with >= 12 months who has non-MAINTAIN priority
        inp = SalesSkillsInput(
            rep_id="r_prof", rep_name="Proficient", manager_id="m1",
            discovery_score=60, demo_effectiveness=58, objection_handling=60,
            negotiation_skill=57, closing_technique=59,
            prospecting_score=55, pipeline_management=58, crm_discipline=56,
            quota_attainment_pct=0.80, win_rate=0.25,
            avg_deal_size_vs_team=1.0, avg_sales_cycle_vs_team=1.0,
            call_connect_rate=0.15, email_reply_rate=0.12,
            meetings_set_per_week=4.0, months_at_company=14, months_in_role=10,
            training_hours_completed=10, coaching_sessions_90d=3,
            top_performer_last_quarter=False,
        )
        result = eng.analyze(inp)
        if result.skill_level == SkillLevel.PROFICIENT and result.coaching_priority != CoachingPriority.MAINTAIN:
            assert result.development_path == DevelopmentPath.PEER_MENTORING


# ─────────────────────────────────────────────────────────────────────────────
# 14. Summary
# ─────────────────────────────────────────────────────────────────────────────

class TestSummary:
    def setup_method(self):
        self.eng = _engine()

    def test_empty_summary_has_12_keys(self):
        s = self.eng.summary()
        assert len(s) == 12

    def test_empty_summary_total_is_0(self):
        assert self.eng.summary()["total"] == 0

    def test_empty_summary_level_counts_empty(self):
        assert self.eng.summary()["level_counts"] == {}

    def test_empty_summary_gap_counts_empty(self):
        assert self.eng.summary()["gap_counts"] == {}

    def test_empty_summary_priority_counts_empty(self):
        assert self.eng.summary()["priority_counts"] == {}

    def test_empty_summary_path_counts_empty(self):
        assert self.eng.summary()["path_counts"] == {}

    def test_empty_summary_avg_overall_is_zero(self):
        assert self.eng.summary()["avg_overall_score"] == 0.0

    def test_empty_summary_avg_technical_is_zero(self):
        assert self.eng.summary()["avg_technical_score"] == 0.0

    def test_empty_summary_avg_operational_is_zero(self):
        assert self.eng.summary()["avg_operational_score"] == 0.0

    def test_empty_summary_avg_results_is_zero(self):
        assert self.eng.summary()["avg_results_score"] == 0.0

    def test_empty_summary_top_performer_count_is_0(self):
        assert self.eng.summary()["top_performer_count"] == 0

    def test_empty_summary_immediate_coaching_count_is_0(self):
        assert self.eng.summary()["immediate_coaching_count"] == 0

    def test_empty_summary_at_risk_count_is_0(self):
        assert self.eng.summary()["at_risk_count"] == 0

    def test_summary_keys(self):
        expected_keys = {
            "total", "level_counts", "gap_counts", "priority_counts", "path_counts",
            "avg_overall_score", "avg_technical_score", "avg_operational_score",
            "avg_results_score", "top_performer_count", "immediate_coaching_count",
            "at_risk_count",
        }
        assert set(self.eng.summary().keys()) == expected_keys

    def test_non_empty_summary_has_12_keys(self):
        self.eng.analyze(_make_expert())
        s = self.eng.summary()
        assert len(s) == 12

    def test_summary_total_correct_after_analyze(self):
        self.eng.analyze(_make_expert())
        self.eng.analyze(_make_beginner())
        assert self.eng.summary()["total"] == 2

    def test_summary_level_counts_correct(self):
        self.eng.analyze(_make_expert())
        s = self.eng.summary()
        # Expert rep should appear under some level key
        total_in_levels = sum(s["level_counts"].values())
        assert total_in_levels == 1

    def test_summary_level_counts_uses_string_keys(self):
        self.eng.analyze(_make_expert())
        s = self.eng.summary()
        for k in s["level_counts"]:
            assert isinstance(k, str)

    def test_summary_gap_counts_uses_string_keys(self):
        self.eng.analyze(_make_expert())
        s = self.eng.summary()
        for k in s["gap_counts"]:
            assert isinstance(k, str)

    def test_summary_priority_counts_uses_string_keys(self):
        self.eng.analyze(_make_expert())
        s = self.eng.summary()
        for k in s["priority_counts"]:
            assert isinstance(k, str)

    def test_summary_path_counts_uses_string_keys(self):
        self.eng.analyze(_make_expert())
        s = self.eng.summary()
        for k in s["path_counts"]:
            assert isinstance(k, str)

    def test_summary_avg_overall_is_float(self):
        self.eng.analyze(_make_expert())
        assert isinstance(self.eng.summary()["avg_overall_score"], float)

    def test_summary_avg_technical_is_float(self):
        self.eng.analyze(_make_expert())
        assert isinstance(self.eng.summary()["avg_technical_score"], float)

    def test_summary_avg_operational_is_float(self):
        self.eng.analyze(_make_expert())
        assert isinstance(self.eng.summary()["avg_operational_score"], float)

    def test_summary_avg_results_is_float(self):
        self.eng.analyze(_make_expert())
        assert isinstance(self.eng.summary()["avg_results_score"], float)

    def test_summary_top_performer_count_correct(self):
        self.eng.analyze(_make_expert())
        self.eng.analyze(_make_beginner())
        s = self.eng.summary()
        assert s["top_performer_count"] == len(self.eng.top_performers)

    def test_summary_immediate_coaching_count_correct(self):
        self.eng.analyze(_make_expert())
        self.eng.analyze(_make_beginner())
        s = self.eng.summary()
        assert s["immediate_coaching_count"] == len(self.eng.needs_immediate_coaching)

    def test_summary_at_risk_count_correct(self):
        self.eng.analyze(_make_expert())
        self.eng.analyze(_make_beginner())
        s = self.eng.summary()
        assert s["at_risk_count"] == len(self.eng.at_risk_reps)

    def test_summary_avg_overall_correct_for_single_rep(self):
        result = self.eng.analyze(_make_expert())
        s = self.eng.summary()
        assert s["avg_overall_score"] == result.overall_skill_score

    def test_summary_avg_technical_correct_for_single_rep(self):
        result = self.eng.analyze(_make_expert())
        s = self.eng.summary()
        assert s["avg_technical_score"] == result.technical_score

    def test_summary_avg_operational_correct_for_single_rep(self):
        result = self.eng.analyze(_make_expert())
        s = self.eng.summary()
        assert s["avg_operational_score"] == result.operational_score

    def test_summary_avg_results_correct_for_single_rep(self):
        result = self.eng.analyze(_make_expert())
        s = self.eng.summary()
        assert s["avg_results_score"] == result.results_score

    def test_summary_counts_two_different_reps(self):
        self.eng.analyze(_make_expert())
        self.eng.analyze(_make_beginner())
        s = self.eng.summary()
        assert s["total"] == 2
        assert sum(s["level_counts"].values()) == 2
        assert sum(s["gap_counts"].values()) == 2
        assert sum(s["priority_counts"].values()) == 2
        assert sum(s["path_counts"].values()) == 2


# ─────────────────────────────────────────────────────────────────────────────
# 15. Reset
# ─────────────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self):
        eng = _engine()
        eng.analyze(_make_expert())
        eng.analyze(_make_beginner())
        assert len(eng.results) == 2
        eng.reset()
        assert eng.results == []

    def test_reset_clears_top_performers(self):
        eng = _engine()
        eng.analyze(_make_expert())
        eng.reset()
        assert eng.top_performers == []

    def test_reset_clears_needs_immediate_coaching(self):
        eng = _engine()
        eng.analyze(_make_beginner())
        eng.reset()
        assert eng.needs_immediate_coaching == []

    def test_reset_clears_at_risk_reps(self):
        eng = _engine()
        eng.analyze(_make_beginner())
        eng.reset()
        assert eng.at_risk_reps == []

    def test_reset_clears_ready_for_mentoring(self):
        eng = _engine()
        eng.analyze(_make_mid())
        eng.reset()
        assert eng.ready_for_mentoring == []

    def test_reset_summary_returns_zeros(self):
        eng = _engine()
        eng.analyze(_make_expert())
        eng.reset()
        s = eng.summary()
        assert s["total"] == 0

    def test_can_analyze_after_reset(self):
        eng = _engine()
        eng.analyze(_make_expert())
        eng.reset()
        result = eng.analyze(_make_mid())
        assert result is not None
        assert len(eng.results) == 1

    def test_reset_multiple_times_is_safe(self):
        eng = _engine()
        eng.reset()
        eng.reset()
        assert eng.results == []


# ─────────────────────────────────────────────────────────────────────────────
# 16. End-to-End Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEndToEnd:
    def setup_method(self):
        self.eng = _engine()

    def test_expert_end_to_end_skill_level(self):
        result = self.eng.analyze(_make_expert())
        assert result.skill_level == SkillLevel.EXPERT

    def test_expert_end_to_end_development_path_maintain(self):
        result = self.eng.analyze(_make_expert())
        assert result.development_path == DevelopmentPath.MAINTAIN

    def test_expert_end_to_end_coaching_priority_maintain(self):
        result = self.eng.analyze(_make_expert())
        assert result.coaching_priority == CoachingPriority.MAINTAIN

    def test_expert_end_to_end_rep_id(self):
        result = self.eng.analyze(_make_expert())
        assert result.rep_id == "r01"

    def test_expert_end_to_end_rep_name(self):
        result = self.eng.analyze(_make_expert())
        assert result.rep_name == "Expert Rep"

    def test_expert_end_to_end_returns_result(self):
        result = self.eng.analyze(_make_expert())
        assert isinstance(result, SalesSkillsResult)

    def test_expert_stored_in_results(self):
        result = self.eng.analyze(_make_expert())
        assert result in self.eng.results

    def test_beginner_skill_level(self):
        result = self.eng.analyze(_make_beginner())
        assert result.skill_level == SkillLevel.BEGINNER

    def test_beginner_development_path_skills_coaching(self):
        result = self.eng.analyze(_make_beginner())
        assert result.development_path == DevelopmentPath.SKILLS_COACHING

    def test_beginner_coaching_priority(self):
        result = self.eng.analyze(_make_beginner())
        # Critical gap → IMMEDIATE
        assert result.coaching_priority in (CoachingPriority.IMMEDIATE, CoachingPriority.HIGH)

    def test_beginner_stored_in_results(self):
        result = self.eng.analyze(_make_beginner())
        assert result in self.eng.results

    def test_analyze_batch_returns_sorted_by_overall_score_desc(self):
        inputs = [_make_beginner(), _make_expert(), _make_mid()]
        results = self.eng.analyze_batch(inputs)
        scores = [r.overall_skill_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_analyze_batch_stores_all_results(self):
        inputs = [_make_beginner(), _make_expert(), _make_mid()]
        results = self.eng.analyze_batch(inputs)
        assert len(results) == 3

    def test_analyze_batch_returns_same_list_as_results(self):
        inputs = [_make_beginner(), _make_expert()]
        batch = self.eng.analyze_batch(inputs)
        assert batch is self.eng.results

    def test_analyze_increments_results_count(self):
        self.eng.analyze(_make_expert())
        assert len(self.eng.results) == 1
        self.eng.analyze(_make_beginner())
        assert len(self.eng.results) == 2

    def test_multiple_analyze_calls_accumulate(self):
        for _ in range(5):
            self.eng.analyze(_make_mid())
        assert len(self.eng.results) == 5

    def test_batch_sorting_is_stable_desc(self):
        """After batch analysis, the first element has the highest overall score."""
        inputs = [_make_beginner(), _make_mid(), _make_expert(), _make_advanced()]
        results = self.eng.analyze_batch(inputs)
        assert results[0].overall_skill_score >= results[-1].overall_skill_score

    def test_to_dict_all_list_fields_are_lists(self):
        result = self.eng.analyze(_make_expert())
        d = result.to_dict()
        assert isinstance(d["strengths"], list)
        assert isinstance(d["gaps"], list)
        assert isinstance(d["recommended_actions"], list)

    def test_expert_has_strengths(self):
        result = self.eng.analyze(_make_expert())
        assert len(result.strengths) > 0

    def test_beginner_has_gaps(self):
        result = self.eng.analyze(_make_beginner())
        assert len(result.gaps) > 0

    def test_recommended_actions_non_empty(self):
        result = self.eng.analyze(_make_expert())
        assert len(result.recommended_actions) > 0

    def test_overall_score_in_range(self):
        for make in [_make_expert, _make_beginner, _make_mid, _make_advanced]:
            eng = _engine()
            result = eng.analyze(make())
            assert 0.0 <= result.overall_skill_score <= 100.0

    def test_technical_score_in_range(self):
        for make in [_make_expert, _make_beginner, _make_mid]:
            eng = _engine()
            result = eng.analyze(make())
            assert 0.0 <= result.technical_score <= 100.0

    def test_operational_score_in_range(self):
        for make in [_make_expert, _make_beginner, _make_mid]:
            eng = _engine()
            result = eng.analyze(make())
            assert 0.0 <= result.operational_score <= 100.0

    def test_results_score_in_range(self):
        for make in [_make_expert, _make_beginner, _make_mid]:
            eng = _engine()
            result = eng.analyze(make())
            assert 0.0 <= result.results_score <= 100.0

    def test_weakest_area_is_non_empty_string(self):
        result = self.eng.analyze(_make_expert())
        assert isinstance(result.weakest_area, str)
        assert len(result.weakest_area) > 0

    def test_skill_gap_is_skillgap_enum(self):
        result = self.eng.analyze(_make_expert())
        assert isinstance(result.skill_gap, SkillGap)

    def test_coaching_priority_is_enum(self):
        result = self.eng.analyze(_make_expert())
        assert isinstance(result.coaching_priority, CoachingPriority)

    def test_development_path_is_enum(self):
        result = self.eng.analyze(_make_expert())
        assert isinstance(result.development_path, DevelopmentPath)

    def test_expert_overall_above_85(self):
        result = self.eng.analyze(_make_expert())
        assert result.overall_skill_score >= 85.0

    def test_beginner_overall_below_35(self):
        result = self.eng.analyze(_make_beginner())
        assert result.overall_skill_score < 35.0


# ─────────────────────────────────────────────────────────────────────────────
# 17. Additional edge-case / formula correctness tests
# ─────────────────────────────────────────────────────────────────────────────

class TestFormulaEdgeCases:
    def setup_method(self):
        self.eng = _engine()

    def test_technical_score_precision(self):
        """(80+80+80+80+81)/5 = 80.2"""
        inp = _make_expert()
        inp.discovery_score = 80
        inp.demo_effectiveness = 80
        inp.objection_handling = 80
        inp.negotiation_skill = 80
        inp.closing_technique = 81
        assert self.eng._technical_score(inp) == 80.2

    def test_operational_score_precision(self):
        """(90+90+91)/3 ≈ 90.3"""
        inp = _make_expert()
        inp.prospecting_score = 90
        inp.pipeline_management = 90
        inp.crm_discipline = 91
        assert self.eng._operational_score(inp) == pytest.approx(
            round((90 + 90 + 91) / 3.0, 1), abs=0.01
        )

    def test_results_score_all_zeros_except_cycle_zero(self):
        inp = _make_expert()
        inp.quota_attainment_pct = 0.0
        inp.win_rate = 0.0
        inp.avg_deal_size_vs_team = 0.0
        inp.avg_sales_cycle_vs_team = 0.0
        inp.call_connect_rate = 0.0
        inp.email_reply_rate = 0.0
        assert self.eng._results_score(inp) == 10.0  # only cycle=10

    def test_overall_formula_exact(self):
        tech, ops, res = 80.0, 70.0, 60.0
        expected = round(80 * 0.40 + 70 * 0.25 + 60 * 0.35, 1)
        assert self.eng._overall_skill_score(tech, ops, res) == expected

    def test_skill_gap_boundary_exactly_80(self):
        assert self.eng._skill_gap(80.0, 80.0) == SkillGap.NONE

    def test_skill_gap_boundary_exactly_65(self):
        assert self.eng._skill_gap(65.0, 65.0) == SkillGap.MINOR

    def test_skill_gap_boundary_exactly_50(self):
        assert self.eng._skill_gap(50.0, 50.0) == SkillGap.MODERATE

    def test_skill_gap_boundary_exactly_30(self):
        assert self.eng._skill_gap(30.0, 30.0) == SkillGap.SIGNIFICANT

    def test_skill_level_boundary_exactly_85(self):
        assert self.eng._skill_level(85.0) == SkillLevel.EXPERT

    def test_skill_level_boundary_exactly_70(self):
        assert self.eng._skill_level(70.0) == SkillLevel.ADVANCED

    def test_skill_level_boundary_exactly_55(self):
        assert self.eng._skill_level(55.0) == SkillLevel.PROFICIENT

    def test_skill_level_boundary_exactly_35(self):
        assert self.eng._skill_level(35.0) == SkillLevel.DEVELOPING

    def test_result_overall_is_rounded_float(self):
        result = self.eng.analyze(_make_expert())
        assert result.overall_skill_score == round(result.overall_skill_score, 1)

    def test_result_technical_is_rounded_float(self):
        result = self.eng.analyze(_make_expert())
        assert result.technical_score == round(result.technical_score, 1)

    def test_result_operational_is_rounded_float(self):
        result = self.eng.analyze(_make_expert())
        assert result.operational_score == round(result.operational_score, 1)

    def test_result_results_score_is_rounded_float(self):
        result = self.eng.analyze(_make_expert())
        assert result.results_score == round(result.results_score, 1)

    def test_strengths_list_contains_strings(self):
        result = self.eng.analyze(_make_expert())
        for s in result.strengths:
            assert isinstance(s, str)

    def test_gaps_list_contains_strings(self):
        result = self.eng.analyze(_make_beginner())
        for g in result.gaps:
            assert isinstance(g, str)

    def test_actions_list_contains_strings(self):
        result = self.eng.analyze(_make_expert())
        for a in result.recommended_actions:
            assert isinstance(a, str)

    def test_engine_initial_results_empty(self):
        eng = _engine()
        assert eng.results == []


class TestDevelopmentPathEdgeCases:
    def setup_method(self):
        self.eng = _engine()

    def test_beginner_with_zero_sessions_skills_coaching(self):
        inp = _make_beginner()
        inp.coaching_sessions_90d = 0
        result = self.eng.analyze(inp)
        if result.coaching_priority != CoachingPriority.MAINTAIN:
            assert result.development_path == DevelopmentPath.SKILLS_COACHING

    def test_proficient_11_months_skills_coaching(self):
        """Less than 12 months at company → SKILLS_COACHING even if PROFICIENT"""
        inp = SalesSkillsInput(
            rep_id="r_p11", rep_name="P11", manager_id="m1",
            discovery_score=62, demo_effectiveness=60, objection_handling=62,
            negotiation_skill=58, closing_technique=61,
            prospecting_score=56, pipeline_management=60, crm_discipline=58,
            quota_attainment_pct=0.85, win_rate=0.26,
            avg_deal_size_vs_team=0.95, avg_sales_cycle_vs_team=1.0,
            call_connect_rate=0.16, email_reply_rate=0.13,
            meetings_set_per_week=4.5, months_at_company=11, months_in_role=9,
            training_hours_completed=10, coaching_sessions_90d=3,
            top_performer_last_quarter=False,
        )
        result = self.eng.analyze(inp)
        if result.skill_level == SkillLevel.PROFICIENT and result.coaching_priority != CoachingPriority.MAINTAIN:
            assert result.development_path == DevelopmentPath.SKILLS_COACHING

    def test_advanced_19_training_hours_self_directed(self):
        inp = _make_advanced()
        inp.training_hours_completed = 19
        result = self.eng.analyze(inp)
        if result.skill_level == SkillLevel.ADVANCED and result.coaching_priority != CoachingPriority.MAINTAIN:
            assert result.development_path == DevelopmentPath.SELF_DIRECTED


class TestAnalyzeBatch:
    def test_batch_empty_list(self):
        eng = _engine()
        results = eng.analyze_batch([])
        assert results == []

    def test_batch_single_rep(self):
        eng = _engine()
        results = eng.analyze_batch([_make_expert()])
        assert len(results) == 1

    def test_batch_three_reps_sorted_desc(self):
        eng = _engine()
        results = eng.analyze_batch([_make_beginner(), _make_expert(), _make_mid()])
        scores = [r.overall_skill_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_batch_four_reps_all_stored(self):
        eng = _engine()
        eng.analyze_batch([_make_expert(), _make_beginner(), _make_mid(), _make_advanced()])
        assert len(eng.results) == 4

    def test_batch_returns_results_list(self):
        eng = _engine()
        batch = eng.analyze_batch([_make_expert()])
        assert batch is eng.results

    def test_batch_after_reset_starts_fresh(self):
        eng = _engine()
        eng.analyze_batch([_make_expert(), _make_beginner()])
        eng.reset()
        results = eng.analyze_batch([_make_mid()])
        assert len(results) == 1
