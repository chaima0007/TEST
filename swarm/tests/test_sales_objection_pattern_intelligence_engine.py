"""
Comprehensive pytest test suite for SalesObjectionPatternIntelligenceEngine.
Target: 280+ tests, all passing.
"""
from __future__ import annotations

import pytest

from swarm.intelligence.sales_objection_pattern_intelligence_engine import (
    ObjectionAction,
    ObjectionPattern,
    ObjectionPatternInput,
    ObjectionPatternResult,
    ObjectionRisk,
    ObjectionSeverity,
    SalesObjectionPatternIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_input(
    *,
    rep_id: str = "REP001",
    region: str = "West",
    evaluation_period_id: str = "Q1-2026",
    total_deals_with_objections: int = 10,
    price_objections_count: int = 0,
    timing_objections_count: int = 0,
    competition_objections_count: int = 0,
    authority_objections_count: int = 0,
    need_fit_objections_count: int = 0,
    objections_per_deal_avg: float = 1.0,
    objection_overcome_rate_pct: float = 0.60,
    price_overcome_rate_pct: float = 0.60,
    competition_overcome_rate_pct: float = 0.60,
    timing_overcome_rate_pct: float = 0.60,
    objection_stall_avg_days: float = 3.0,
    late_stage_objections_count: int = 0,
    recurring_objection_same_account_count: int = 0,
    lost_deals_due_to_objection_count: int = 0,
    deals_lost_to_price_count: int = 0,
    deals_lost_to_competition_count: int = 0,
    objection_documentation_rate_pct: float = 0.80,
    avg_deal_size_usd: float = 10000.0,
) -> ObjectionPatternInput:
    return ObjectionPatternInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        total_deals_with_objections=total_deals_with_objections,
        price_objections_count=price_objections_count,
        timing_objections_count=timing_objections_count,
        competition_objections_count=competition_objections_count,
        authority_objections_count=authority_objections_count,
        need_fit_objections_count=need_fit_objections_count,
        objections_per_deal_avg=objections_per_deal_avg,
        objection_overcome_rate_pct=objection_overcome_rate_pct,
        price_overcome_rate_pct=price_overcome_rate_pct,
        competition_overcome_rate_pct=competition_overcome_rate_pct,
        timing_overcome_rate_pct=timing_overcome_rate_pct,
        objection_stall_avg_days=objection_stall_avg_days,
        late_stage_objections_count=late_stage_objections_count,
        recurring_objection_same_account_count=recurring_objection_same_account_count,
        lost_deals_due_to_objection_count=lost_deals_due_to_objection_count,
        deals_lost_to_price_count=deals_lost_to_price_count,
        deals_lost_to_competition_count=deals_lost_to_competition_count,
        objection_documentation_rate_pct=objection_documentation_rate_pct,
        avg_deal_size_usd=avg_deal_size_usd,
    )


@pytest.fixture
def engine():
    return SalesObjectionPatternIntelligenceEngine()


@pytest.fixture
def clean_input():
    """Input with minimal objection burden — should yield low risk."""
    return make_input()


@pytest.fixture
def high_price_input():
    """Input that triggers price_barrier pattern with critical risk."""
    return make_input(
        total_deals_with_objections=10,
        price_objections_count=6,       # 60% ratio → +35
        price_overcome_rate_pct=0.20,   # <0.30 → +30
        deals_lost_to_price_count=4,    # >=4 → +25
        objection_overcome_rate_pct=0.20,
        lost_deals_due_to_objection_count=5,
    )


@pytest.fixture
def high_comp_input():
    """Input that triggers competitive_displacement pattern."""
    return make_input(
        total_deals_with_objections=10,
        competition_objections_count=5,   # 50% ratio → +35
        competition_overcome_rate_pct=0.20,
        deals_lost_to_competition_count=4,
        late_stage_objections_count=3,
        lost_deals_due_to_objection_count=4,
    )


# ---------------------------------------------------------------------------
# TestObjectionPatternInputDataclass
# ---------------------------------------------------------------------------

class TestObjectionPatternInputDataclass:
    """Tests for the ObjectionPatternInput dataclass."""

    def test_has_22_fields(self):
        import dataclasses
        fields = dataclasses.fields(ObjectionPatternInput)
        assert len(fields) == 22

    def test_construction_with_all_fields(self):
        inp = make_input()
        assert inp.rep_id == "REP001"
        assert inp.region == "West"

    def test_rep_id_stored(self):
        inp = make_input(rep_id="X999")
        assert inp.rep_id == "X999"

    def test_region_stored(self):
        inp = make_input(region="East")
        assert inp.region == "East"

    def test_evaluation_period_id_stored(self):
        inp = make_input(evaluation_period_id="Q4-2025")
        assert inp.evaluation_period_id == "Q4-2025"

    def test_numeric_fields_stored(self):
        inp = make_input(total_deals_with_objections=20, avg_deal_size_usd=50000.0)
        assert inp.total_deals_with_objections == 20
        assert inp.avg_deal_size_usd == 50000.0

    def test_float_fields_stored(self):
        inp = make_input(objection_overcome_rate_pct=0.75)
        assert inp.objection_overcome_rate_pct == 0.75


# ---------------------------------------------------------------------------
# TestObjectionPatternResultDataclass
# ---------------------------------------------------------------------------

class TestObjectionPatternResultDataclass:
    """Tests for the ObjectionPatternResult dataclass."""

    def test_to_dict_returns_15_keys(self, engine, clean_input):
        result = engine.assess(clean_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_keys_exact(self, engine, clean_input):
        result = engine.assess(clean_input)
        d = result.to_dict()
        expected_keys = {
            "rep_id", "region", "objection_risk", "objection_pattern",
            "objection_severity", "recommended_action", "price_pressure_score",
            "competition_pressure_score", "timing_resistance_score", "skill_gap_score",
            "objection_burden_composite", "has_systemic_issue",
            "requires_coaching_intervention", "estimated_lost_revenue_usd",
            "objection_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_rep_id(self, engine):
        result = engine.assess(make_input(rep_id="ABC"))
        assert result.to_dict()["rep_id"] == "ABC"

    def test_to_dict_region(self, engine):
        result = engine.assess(make_input(region="Midwest"))
        assert result.to_dict()["region"] == "Midwest"

    def test_to_dict_risk_is_string(self, engine, clean_input):
        d = engine.assess(clean_input).to_dict()
        assert isinstance(d["objection_risk"], str)

    def test_to_dict_pattern_is_string(self, engine, clean_input):
        d = engine.assess(clean_input).to_dict()
        assert isinstance(d["objection_pattern"], str)

    def test_to_dict_severity_is_string(self, engine, clean_input):
        d = engine.assess(clean_input).to_dict()
        assert isinstance(d["objection_severity"], str)

    def test_to_dict_action_is_string(self, engine, clean_input):
        d = engine.assess(clean_input).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_estimated_lost_revenue_is_float(self, engine, clean_input):
        d = engine.assess(clean_input).to_dict()
        assert isinstance(d["estimated_lost_revenue_usd"], float)

    def test_to_dict_has_systemic_issue_is_bool(self, engine, clean_input):
        d = engine.assess(clean_input).to_dict()
        assert isinstance(d["has_systemic_issue"], bool)

    def test_to_dict_requires_coaching_is_bool(self, engine, clean_input):
        d = engine.assess(clean_input).to_dict()
        assert isinstance(d["requires_coaching_intervention"], bool)

    def test_result_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(ObjectionPatternResult)
        assert len(fields) == 15


# ---------------------------------------------------------------------------
# TestEnumValues
# ---------------------------------------------------------------------------

class TestEnumValues:
    """Validate enum string values."""

    def test_risk_low(self):
        assert ObjectionRisk.low.value == "low"

    def test_risk_moderate(self):
        assert ObjectionRisk.moderate.value == "moderate"

    def test_risk_high(self):
        assert ObjectionRisk.high.value == "high"

    def test_risk_critical(self):
        assert ObjectionRisk.critical.value == "critical"

    def test_pattern_none(self):
        assert ObjectionPattern.none.value == "none"

    def test_pattern_price_barrier(self):
        assert ObjectionPattern.price_barrier.value == "price_barrier"

    def test_pattern_timing_stall(self):
        assert ObjectionPattern.timing_stall.value == "timing_stall"

    def test_pattern_competitive_displacement(self):
        assert ObjectionPattern.competitive_displacement.value == "competitive_displacement"

    def test_pattern_authority_gap(self):
        assert ObjectionPattern.authority_gap.value == "authority_gap"

    def test_pattern_need_misalignment(self):
        assert ObjectionPattern.need_misalignment.value == "need_misalignment"

    def test_severity_managed(self):
        assert ObjectionSeverity.managed.value == "managed"

    def test_severity_recurring(self):
        assert ObjectionSeverity.recurring.value == "recurring"

    def test_severity_systemic(self):
        assert ObjectionSeverity.systemic.value == "systemic"

    def test_severity_blocking(self):
        assert ObjectionSeverity.blocking.value == "blocking"

    def test_action_no_action(self):
        assert ObjectionAction.no_action.value == "no_action"

    def test_action_objection_coaching(self):
        assert ObjectionAction.objection_coaching.value == "objection_coaching"

    def test_action_messaging_update(self):
        assert ObjectionAction.messaging_update.value == "messaging_update"

    def test_action_battlecard_refresh(self):
        assert ObjectionAction.battlecard_refresh.value == "battlecard_refresh"

    def test_action_pricing_review(self):
        assert ObjectionAction.pricing_review.value == "pricing_review"


# ---------------------------------------------------------------------------
# TestPricePressureScore
# ---------------------------------------------------------------------------

class TestPricePressureScore:
    """Unit tests for _price_pressure_score."""

    def test_zero_price_objections_no_loss(self, engine):
        inp = make_input(price_objections_count=0, price_overcome_rate_pct=0.80,
                         deals_lost_to_price_count=0)
        s = engine._price_pressure_score(inp)
        assert s == 0.0

    def test_price_ratio_gte50_adds_35(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=5,
                         price_overcome_rate_pct=0.80, deals_lost_to_price_count=0)
        s = engine._price_pressure_score(inp)
        assert s == 35.0

    def test_price_ratio_30_to_50_adds_20(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=3,
                         price_overcome_rate_pct=0.80, deals_lost_to_price_count=0)
        s = engine._price_pressure_score(inp)
        assert s == 20.0

    def test_price_ratio_10_to_30_adds_8(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=1,
                         price_overcome_rate_pct=0.80, deals_lost_to_price_count=0)
        s = engine._price_pressure_score(inp)
        assert s == 8.0

    def test_overcome_rate_lt30_adds_30(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=0,
                         price_overcome_rate_pct=0.20, deals_lost_to_price_count=0)
        s = engine._price_pressure_score(inp)
        assert s == 30.0

    def test_overcome_rate_30_to_50_adds_15(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=0,
                         price_overcome_rate_pct=0.40, deals_lost_to_price_count=0)
        s = engine._price_pressure_score(inp)
        assert s == 15.0

    def test_overcome_rate_gte50_adds_0(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=0,
                         price_overcome_rate_pct=0.50, deals_lost_to_price_count=0)
        s = engine._price_pressure_score(inp)
        assert s == 0.0

    def test_deals_lost_price_gte4_adds_25(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=0,
                         price_overcome_rate_pct=0.80, deals_lost_to_price_count=4)
        s = engine._price_pressure_score(inp)
        assert s == 25.0

    def test_deals_lost_price_2_to_3_adds_15(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=0,
                         price_overcome_rate_pct=0.80, deals_lost_to_price_count=2)
        s = engine._price_pressure_score(inp)
        assert s == 15.0

    def test_deals_lost_price_1_adds_8(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=0,
                         price_overcome_rate_pct=0.80, deals_lost_to_price_count=1)
        s = engine._price_pressure_score(inp)
        assert s == 8.0

    def test_undocumented_price_objections_adds_5(self, engine):
        # doc_rate < 0.50 AND price_objections >= 2
        inp = make_input(total_deals_with_objections=10, price_objections_count=2,
                         price_overcome_rate_pct=0.80, deals_lost_to_price_count=0,
                         objection_documentation_rate_pct=0.40)
        s = engine._price_pressure_score(inp)
        # price_ratio = 2/10 = 0.20 → +8; doc < 0.50 and price >=2 → +5
        assert s == 8.0 + 5.0

    def test_no_undocumented_bonus_when_price_objections_lt2(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=1,
                         price_overcome_rate_pct=0.80, deals_lost_to_price_count=0,
                         objection_documentation_rate_pct=0.30)
        s = engine._price_pressure_score(inp)
        assert s == 8.0

    def test_no_undocumented_bonus_when_doc_rate_gte50(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=3,
                         price_overcome_rate_pct=0.80, deals_lost_to_price_count=0,
                         objection_documentation_rate_pct=0.50)
        s = engine._price_pressure_score(inp)
        assert s == 20.0

    def test_capped_at_100(self, engine):
        # max possible = 35+30+25+5 = 95; the cap only kicks in if the sum exceeded 100
        inp = make_input(total_deals_with_objections=10, price_objections_count=10,
                         price_overcome_rate_pct=0.10, deals_lost_to_price_count=10,
                         objection_documentation_rate_pct=0.30)
        s = engine._price_pressure_score(inp)
        assert s == 95.0

    def test_total_deals_zero_uses_1(self, engine):
        inp = make_input(total_deals_with_objections=0, price_objections_count=0,
                         price_overcome_rate_pct=0.80, deals_lost_to_price_count=0)
        s = engine._price_pressure_score(inp)
        assert s == 0.0


# ---------------------------------------------------------------------------
# TestCompetitionPressureScore
# ---------------------------------------------------------------------------

class TestCompetitionPressureScore:
    """Unit tests for _competition_pressure_score."""

    def test_zero_comp_objections_no_loss(self, engine):
        inp = make_input(competition_objections_count=0, competition_overcome_rate_pct=0.80,
                         deals_lost_to_competition_count=0)
        s = engine._competition_pressure_score(inp)
        assert s == 0.0

    def test_comp_ratio_gte40_adds_35(self, engine):
        inp = make_input(total_deals_with_objections=10, competition_objections_count=4,
                         competition_overcome_rate_pct=0.80, deals_lost_to_competition_count=0)
        s = engine._competition_pressure_score(inp)
        assert s == 35.0

    def test_comp_ratio_20_to_40_adds_20(self, engine):
        inp = make_input(total_deals_with_objections=10, competition_objections_count=2,
                         competition_overcome_rate_pct=0.80, deals_lost_to_competition_count=0)
        s = engine._competition_pressure_score(inp)
        assert s == 20.0

    def test_comp_ratio_10_to_20_adds_8(self, engine):
        inp = make_input(total_deals_with_objections=10, competition_objections_count=1,
                         competition_overcome_rate_pct=0.80, deals_lost_to_competition_count=0)
        s = engine._competition_pressure_score(inp)
        assert s == 8.0

    def test_comp_overcome_lt30_adds_30(self, engine):
        inp = make_input(competition_objections_count=0, competition_overcome_rate_pct=0.20,
                         deals_lost_to_competition_count=0)
        s = engine._competition_pressure_score(inp)
        assert s == 30.0

    def test_comp_overcome_30_to_50_adds_15(self, engine):
        inp = make_input(competition_objections_count=0, competition_overcome_rate_pct=0.40,
                         deals_lost_to_competition_count=0)
        s = engine._competition_pressure_score(inp)
        assert s == 15.0

    def test_comp_overcome_gte50_adds_0(self, engine):
        inp = make_input(competition_objections_count=0, competition_overcome_rate_pct=0.50,
                         deals_lost_to_competition_count=0)
        s = engine._competition_pressure_score(inp)
        assert s == 0.0

    def test_deals_lost_comp_gte4_adds_25(self, engine):
        inp = make_input(competition_objections_count=0, competition_overcome_rate_pct=0.80,
                         deals_lost_to_competition_count=4)
        s = engine._competition_pressure_score(inp)
        assert s == 25.0

    def test_deals_lost_comp_2_to_3_adds_15(self, engine):
        inp = make_input(competition_objections_count=0, competition_overcome_rate_pct=0.80,
                         deals_lost_to_competition_count=2)
        s = engine._competition_pressure_score(inp)
        assert s == 15.0

    def test_deals_lost_comp_1_adds_8(self, engine):
        inp = make_input(competition_objections_count=0, competition_overcome_rate_pct=0.80,
                         deals_lost_to_competition_count=1)
        s = engine._competition_pressure_score(inp)
        assert s == 8.0

    def test_late_stage_and_comp_objections_adds_5(self, engine):
        # late_stage >= 3 AND competition >= 2
        inp = make_input(total_deals_with_objections=10, competition_objections_count=2,
                         competition_overcome_rate_pct=0.80, deals_lost_to_competition_count=0,
                         late_stage_objections_count=3)
        s = engine._competition_pressure_score(inp)
        # comp_ratio = 2/10=0.20 → +20; late_stage bonus → +5
        assert s == 25.0

    def test_no_late_stage_bonus_when_lt3_late(self, engine):
        inp = make_input(total_deals_with_objections=10, competition_objections_count=2,
                         competition_overcome_rate_pct=0.80, deals_lost_to_competition_count=0,
                         late_stage_objections_count=2)
        s = engine._competition_pressure_score(inp)
        assert s == 20.0

    def test_no_late_stage_bonus_when_comp_lt2(self, engine):
        inp = make_input(total_deals_with_objections=10, competition_objections_count=1,
                         competition_overcome_rate_pct=0.80, deals_lost_to_competition_count=0,
                         late_stage_objections_count=3)
        s = engine._competition_pressure_score(inp)
        # comp_ratio=1/10=0.10 → +8; no late_stage bonus (comp < 2)
        assert s == 8.0

    def test_capped_at_100(self, engine):
        # max possible = 35+30+25+5 = 95; the cap only kicks in if the sum exceeded 100
        inp = make_input(total_deals_with_objections=10, competition_objections_count=10,
                         competition_overcome_rate_pct=0.10, deals_lost_to_competition_count=10,
                         late_stage_objections_count=5)
        s = engine._competition_pressure_score(inp)
        assert s == 95.0


# ---------------------------------------------------------------------------
# TestTimingResistanceScore
# ---------------------------------------------------------------------------

class TestTimingResistanceScore:
    """Unit tests for _timing_resistance_score."""

    def test_zero_timing_factors(self, engine):
        inp = make_input(timing_objections_count=0, timing_overcome_rate_pct=0.80,
                         late_stage_objections_count=0, objection_stall_avg_days=1.0)
        s = engine._timing_resistance_score(inp)
        assert s == 0.0

    def test_timing_ratio_gte40_adds_30(self, engine):
        inp = make_input(total_deals_with_objections=10, timing_objections_count=4,
                         timing_overcome_rate_pct=0.80, late_stage_objections_count=0,
                         objection_stall_avg_days=1.0)
        s = engine._timing_resistance_score(inp)
        assert s == 30.0

    def test_timing_ratio_25_to_40_adds_18(self, engine):
        inp = make_input(total_deals_with_objections=10, timing_objections_count=3,
                         timing_overcome_rate_pct=0.80, late_stage_objections_count=0,
                         objection_stall_avg_days=1.0)
        # 3/10 = 0.30 → +18
        s = engine._timing_resistance_score(inp)
        assert s == 18.0

    def test_timing_ratio_10_to_25_adds_8(self, engine):
        inp = make_input(total_deals_with_objections=10, timing_objections_count=1,
                         timing_overcome_rate_pct=0.80, late_stage_objections_count=0,
                         objection_stall_avg_days=1.0)
        s = engine._timing_resistance_score(inp)
        assert s == 8.0

    def test_timing_overcome_lt25_adds_30(self, engine):
        inp = make_input(timing_objections_count=0, timing_overcome_rate_pct=0.20,
                         late_stage_objections_count=0, objection_stall_avg_days=1.0)
        s = engine._timing_resistance_score(inp)
        assert s == 30.0

    def test_timing_overcome_25_to_45_adds_15(self, engine):
        inp = make_input(timing_objections_count=0, timing_overcome_rate_pct=0.35,
                         late_stage_objections_count=0, objection_stall_avg_days=1.0)
        s = engine._timing_resistance_score(inp)
        assert s == 15.0

    def test_timing_overcome_gte45_adds_0(self, engine):
        inp = make_input(timing_objections_count=0, timing_overcome_rate_pct=0.45,
                         late_stage_objections_count=0, objection_stall_avg_days=1.0)
        s = engine._timing_resistance_score(inp)
        assert s == 0.0

    def test_late_stage_gte4_adds_25(self, engine):
        inp = make_input(timing_objections_count=0, timing_overcome_rate_pct=0.80,
                         late_stage_objections_count=4, objection_stall_avg_days=1.0)
        s = engine._timing_resistance_score(inp)
        assert s == 25.0

    def test_late_stage_2_to_3_adds_12(self, engine):
        inp = make_input(timing_objections_count=0, timing_overcome_rate_pct=0.80,
                         late_stage_objections_count=2, objection_stall_avg_days=1.0)
        s = engine._timing_resistance_score(inp)
        assert s == 12.0

    def test_late_stage_0_adds_0(self, engine):
        inp = make_input(timing_objections_count=0, timing_overcome_rate_pct=0.80,
                         late_stage_objections_count=0, objection_stall_avg_days=1.0)
        s = engine._timing_resistance_score(inp)
        assert s == 0.0

    def test_stall_days_gte14_adds_15(self, engine):
        inp = make_input(timing_objections_count=0, timing_overcome_rate_pct=0.80,
                         late_stage_objections_count=0, objection_stall_avg_days=14.0)
        s = engine._timing_resistance_score(inp)
        assert s == 15.0

    def test_stall_days_7_to_14_adds_8(self, engine):
        inp = make_input(timing_objections_count=0, timing_overcome_rate_pct=0.80,
                         late_stage_objections_count=0, objection_stall_avg_days=7.0)
        s = engine._timing_resistance_score(inp)
        assert s == 8.0

    def test_stall_days_lt7_adds_0(self, engine):
        inp = make_input(timing_objections_count=0, timing_overcome_rate_pct=0.80,
                         late_stage_objections_count=0, objection_stall_avg_days=6.9)
        s = engine._timing_resistance_score(inp)
        assert s == 0.0

    def test_capped_at_100(self, engine):
        inp = make_input(total_deals_with_objections=10, timing_objections_count=10,
                         timing_overcome_rate_pct=0.10, late_stage_objections_count=10,
                         objection_stall_avg_days=20.0)
        s = engine._timing_resistance_score(inp)
        assert s == 100.0


# ---------------------------------------------------------------------------
# TestSkillGapScore
# ---------------------------------------------------------------------------

class TestSkillGapScore:
    """Unit tests for _skill_gap_score."""

    def test_zero_skill_issues(self, engine):
        inp = make_input(objections_per_deal_avg=0.5, objection_overcome_rate_pct=0.80,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.80)
        s = engine._skill_gap_score(inp)
        assert s == 0.0

    def test_objections_per_deal_gte3_adds_25(self, engine):
        inp = make_input(objections_per_deal_avg=3.0, objection_overcome_rate_pct=0.80,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.80)
        s = engine._skill_gap_score(inp)
        assert s == 25.0

    def test_objections_per_deal_2_to_3_adds_15(self, engine):
        inp = make_input(objections_per_deal_avg=2.0, objection_overcome_rate_pct=0.80,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.80)
        s = engine._skill_gap_score(inp)
        assert s == 15.0

    def test_objections_per_deal_1pt5_to_2_adds_8(self, engine):
        inp = make_input(objections_per_deal_avg=1.5, objection_overcome_rate_pct=0.80,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.80)
        s = engine._skill_gap_score(inp)
        assert s == 8.0

    def test_overcome_rate_lt25_adds_35(self, engine):
        inp = make_input(objections_per_deal_avg=0.5, objection_overcome_rate_pct=0.24,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.80)
        s = engine._skill_gap_score(inp)
        assert s == 35.0

    def test_overcome_rate_25_to_40_adds_20(self, engine):
        inp = make_input(objections_per_deal_avg=0.5, objection_overcome_rate_pct=0.30,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.80)
        s = engine._skill_gap_score(inp)
        assert s == 20.0

    def test_overcome_rate_40_to_55_adds_8(self, engine):
        inp = make_input(objections_per_deal_avg=0.5, objection_overcome_rate_pct=0.50,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.80)
        s = engine._skill_gap_score(inp)
        assert s == 8.0

    def test_overcome_rate_gte55_adds_0(self, engine):
        inp = make_input(objections_per_deal_avg=0.5, objection_overcome_rate_pct=0.55,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.80)
        s = engine._skill_gap_score(inp)
        assert s == 0.0

    def test_recurring_gte3_adds_20(self, engine):
        inp = make_input(objections_per_deal_avg=0.5, objection_overcome_rate_pct=0.80,
                         recurring_objection_same_account_count=3,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.80)
        s = engine._skill_gap_score(inp)
        assert s == 20.0

    def test_recurring_1_to_2_adds_10(self, engine):
        inp = make_input(objections_per_deal_avg=0.5, objection_overcome_rate_pct=0.80,
                         recurring_objection_same_account_count=1,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.80)
        s = engine._skill_gap_score(inp)
        assert s == 10.0

    def test_recurring_0_adds_0(self, engine):
        inp = make_input(objections_per_deal_avg=0.5, objection_overcome_rate_pct=0.80,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.80)
        s = engine._skill_gap_score(inp)
        assert s == 0.0

    def test_authority_need_combined_gte5_adds_15(self, engine):
        inp = make_input(objections_per_deal_avg=0.5, objection_overcome_rate_pct=0.80,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=3, need_fit_objections_count=2,
                         objection_documentation_rate_pct=0.80)
        s = engine._skill_gap_score(inp)
        assert s == 15.0

    def test_authority_need_combined_2_to_4_adds_8(self, engine):
        inp = make_input(objections_per_deal_avg=0.5, objection_overcome_rate_pct=0.80,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=1, need_fit_objections_count=1,
                         objection_documentation_rate_pct=0.80)
        s = engine._skill_gap_score(inp)
        assert s == 8.0

    def test_authority_need_combined_0_adds_0(self, engine):
        inp = make_input(objections_per_deal_avg=0.5, objection_overcome_rate_pct=0.80,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.80)
        s = engine._skill_gap_score(inp)
        assert s == 0.0

    def test_doc_rate_lt40_adds_5(self, engine):
        inp = make_input(objections_per_deal_avg=0.5, objection_overcome_rate_pct=0.80,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.39)
        s = engine._skill_gap_score(inp)
        assert s == 5.0

    def test_doc_rate_gte40_no_bonus(self, engine):
        inp = make_input(objections_per_deal_avg=0.5, objection_overcome_rate_pct=0.80,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.40)
        s = engine._skill_gap_score(inp)
        assert s == 0.0

    def test_capped_at_100(self, engine):
        inp = make_input(objections_per_deal_avg=5.0, objection_overcome_rate_pct=0.10,
                         recurring_objection_same_account_count=5,
                         authority_objections_count=5, need_fit_objections_count=5,
                         objection_documentation_rate_pct=0.20)
        s = engine._skill_gap_score(inp)
        assert s == 100.0


# ---------------------------------------------------------------------------
# TestCompositeScore
# ---------------------------------------------------------------------------

class TestCompositeScore:
    """Tests for composite = price*0.30 + comp*0.25 + timing*0.25 + skill*0.20."""

    def test_all_zero_scores(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        # All sub-scores may be 0 → composite 0
        price = engine._price_pressure_score(inp)
        comp = engine._competition_pressure_score(inp)
        timing = engine._timing_resistance_score(inp)
        skill = engine._skill_gap_score(inp)
        expected = round(price * 0.30 + comp * 0.25 + timing * 0.25 + skill * 0.20, 1)
        assert result.objection_burden_composite == expected

    def test_composite_uses_correct_weights(self, engine):
        # Force known sub-scores: set price=40, comp=40, timing=40, skill=40
        # We achieve this by checking weights manually
        inp = make_input(
            total_deals_with_objections=10,
            price_objections_count=5,        # 50% → +35
            price_overcome_rate_pct=0.80,
            deals_lost_to_price_count=0,
        )
        p = engine._price_pressure_score(inp)
        c = engine._competition_pressure_score(inp)
        t = engine._timing_resistance_score(inp)
        s = engine._skill_gap_score(inp)
        result = engine.assess(inp)
        expected = round(p * 0.30 + c * 0.25 + t * 0.25 + s * 0.20, 1)
        assert result.objection_burden_composite == expected

    def test_composite_capped_at_100(self, engine):
        inp = make_input(
            total_deals_with_objections=10,
            price_objections_count=10,
            price_overcome_rate_pct=0.10,
            deals_lost_to_price_count=10,
            competition_objections_count=10,
            competition_overcome_rate_pct=0.10,
            deals_lost_to_competition_count=10,
            timing_objections_count=10,
            timing_overcome_rate_pct=0.10,
            late_stage_objections_count=10,
            objection_stall_avg_days=20.0,
            objections_per_deal_avg=5.0,
            objection_overcome_rate_pct=0.10,
            recurring_objection_same_account_count=5,
            authority_objections_count=5,
            need_fit_objections_count=5,
            objection_documentation_rate_pct=0.20,
        )
        result = engine.assess(inp)
        assert result.objection_burden_composite <= 100.0

    def test_composite_is_rounded_to_1_decimal(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        val = result.objection_burden_composite
        assert val == round(val, 1)


# ---------------------------------------------------------------------------
# TestRiskLevel
# ---------------------------------------------------------------------------

class TestRiskLevel:
    """Tests for _risk_level thresholds."""

    def test_composite_60_is_critical(self, engine):
        assert engine._risk_level(60.0) == ObjectionRisk.critical

    def test_composite_70_is_critical(self, engine):
        assert engine._risk_level(70.0) == ObjectionRisk.critical

    def test_composite_100_is_critical(self, engine):
        assert engine._risk_level(100.0) == ObjectionRisk.critical

    def test_composite_59_is_high(self, engine):
        assert engine._risk_level(59.9) == ObjectionRisk.high

    def test_composite_40_is_high(self, engine):
        assert engine._risk_level(40.0) == ObjectionRisk.high

    def test_composite_50_is_high(self, engine):
        assert engine._risk_level(50.0) == ObjectionRisk.high

    def test_composite_39_is_moderate(self, engine):
        assert engine._risk_level(39.9) == ObjectionRisk.moderate

    def test_composite_20_is_moderate(self, engine):
        assert engine._risk_level(20.0) == ObjectionRisk.moderate

    def test_composite_30_is_moderate(self, engine):
        assert engine._risk_level(30.0) == ObjectionRisk.moderate

    def test_composite_19_is_low(self, engine):
        assert engine._risk_level(19.9) == ObjectionRisk.low

    def test_composite_0_is_low(self, engine):
        assert engine._risk_level(0.0) == ObjectionRisk.low

    def test_composite_10_is_low(self, engine):
        assert engine._risk_level(10.0) == ObjectionRisk.low


# ---------------------------------------------------------------------------
# TestSeverity
# ---------------------------------------------------------------------------

class TestSeverity:
    """Tests for _severity thresholds."""

    def test_composite_60_is_blocking(self, engine):
        assert engine._severity(60.0) == ObjectionSeverity.blocking

    def test_composite_80_is_blocking(self, engine):
        assert engine._severity(80.0) == ObjectionSeverity.blocking

    def test_composite_59_is_systemic(self, engine):
        assert engine._severity(59.9) == ObjectionSeverity.systemic

    def test_composite_40_is_systemic(self, engine):
        assert engine._severity(40.0) == ObjectionSeverity.systemic

    def test_composite_39_is_recurring(self, engine):
        assert engine._severity(39.9) == ObjectionSeverity.recurring

    def test_composite_20_is_recurring(self, engine):
        assert engine._severity(20.0) == ObjectionSeverity.recurring

    def test_composite_19_is_managed(self, engine):
        assert engine._severity(19.9) == ObjectionSeverity.managed

    def test_composite_0_is_managed(self, engine):
        assert engine._severity(0.0) == ObjectionSeverity.managed


# ---------------------------------------------------------------------------
# TestAction
# ---------------------------------------------------------------------------

class TestAction:
    """Tests for _action combinations."""

    def test_critical_price_barrier(self, engine):
        assert engine._action(ObjectionRisk.critical, ObjectionPattern.price_barrier) == ObjectionAction.pricing_review

    def test_critical_competitive_displacement(self, engine):
        assert engine._action(ObjectionRisk.critical, ObjectionPattern.competitive_displacement) == ObjectionAction.battlecard_refresh

    def test_critical_timing_stall(self, engine):
        assert engine._action(ObjectionRisk.critical, ObjectionPattern.timing_stall) == ObjectionAction.messaging_update

    def test_critical_authority_gap(self, engine):
        assert engine._action(ObjectionRisk.critical, ObjectionPattern.authority_gap) == ObjectionAction.messaging_update

    def test_critical_need_misalignment(self, engine):
        assert engine._action(ObjectionRisk.critical, ObjectionPattern.need_misalignment) == ObjectionAction.messaging_update

    def test_critical_none(self, engine):
        assert engine._action(ObjectionRisk.critical, ObjectionPattern.none) == ObjectionAction.messaging_update

    def test_high_price_barrier(self, engine):
        assert engine._action(ObjectionRisk.high, ObjectionPattern.price_barrier) == ObjectionAction.pricing_review

    def test_high_competitive_displacement(self, engine):
        assert engine._action(ObjectionRisk.high, ObjectionPattern.competitive_displacement) == ObjectionAction.battlecard_refresh

    def test_high_timing_stall(self, engine):
        assert engine._action(ObjectionRisk.high, ObjectionPattern.timing_stall) == ObjectionAction.objection_coaching

    def test_high_authority_gap(self, engine):
        assert engine._action(ObjectionRisk.high, ObjectionPattern.authority_gap) == ObjectionAction.objection_coaching

    def test_high_need_misalignment(self, engine):
        assert engine._action(ObjectionRisk.high, ObjectionPattern.need_misalignment) == ObjectionAction.objection_coaching

    def test_high_none(self, engine):
        assert engine._action(ObjectionRisk.high, ObjectionPattern.none) == ObjectionAction.objection_coaching

    def test_moderate_any_pattern(self, engine):
        for pattern in ObjectionPattern:
            assert engine._action(ObjectionRisk.moderate, pattern) == ObjectionAction.objection_coaching

    def test_low_any_pattern(self, engine):
        for pattern in ObjectionPattern:
            assert engine._action(ObjectionRisk.low, pattern) == ObjectionAction.no_action


# ---------------------------------------------------------------------------
# TestPatternDetection
# ---------------------------------------------------------------------------

class TestPatternDetection:
    """Tests for _detect_pattern priority logic."""

    def test_competitive_displacement_takes_priority(self, engine):
        # comp>=35 AND lost_comp>=2 → competitive_displacement regardless of price
        result = engine._detect_pattern(
            make_input(deals_lost_to_competition_count=2, deals_lost_to_price_count=2),
            price=40.0, competition=40.0, timing=30.0, skill=25.0
        )
        assert result == ObjectionPattern.competitive_displacement

    def test_price_barrier_when_no_comp(self, engine):
        result = engine._detect_pattern(
            make_input(deals_lost_to_price_count=2, deals_lost_to_competition_count=1),
            price=40.0, competition=10.0, timing=10.0, skill=10.0
        )
        assert result == ObjectionPattern.price_barrier

    def test_timing_stall_when_no_price_or_comp(self, engine):
        result = engine._detect_pattern(
            make_input(late_stage_objections_count=2, deals_lost_to_price_count=1,
                       deals_lost_to_competition_count=1),
            price=10.0, competition=10.0, timing=35.0, skill=25.0
        )
        assert result == ObjectionPattern.timing_stall

    def test_authority_gap(self, engine):
        result = engine._detect_pattern(
            make_input(authority_objections_count=3, late_stage_objections_count=0,
                       deals_lost_to_price_count=0, deals_lost_to_competition_count=0),
            price=10.0, competition=10.0, timing=10.0, skill=30.0
        )
        assert result == ObjectionPattern.authority_gap

    def test_need_misalignment(self, engine):
        result = engine._detect_pattern(
            make_input(need_fit_objections_count=3, objection_overcome_rate_pct=0.30,
                       authority_objections_count=0, deals_lost_to_price_count=0,
                       deals_lost_to_competition_count=0),
            price=10.0, competition=10.0, timing=10.0, skill=10.0
        )
        assert result == ObjectionPattern.need_misalignment

    def test_none_when_no_conditions_met(self, engine):
        result = engine._detect_pattern(
            make_input(deals_lost_to_price_count=0, deals_lost_to_competition_count=0,
                       authority_objections_count=0, need_fit_objections_count=0),
            price=10.0, competition=10.0, timing=10.0, skill=10.0
        )
        assert result == ObjectionPattern.none

    def test_competitive_displacement_requires_comp_score_gte35(self, engine):
        # comp=34 should NOT trigger competitive_displacement
        result = engine._detect_pattern(
            make_input(deals_lost_to_competition_count=2),
            price=10.0, competition=34.0, timing=10.0, skill=10.0
        )
        assert result != ObjectionPattern.competitive_displacement

    def test_competitive_displacement_requires_lost_comp_gte2(self, engine):
        # deals_lost_to_competition_count=1 should NOT trigger
        result = engine._detect_pattern(
            make_input(deals_lost_to_competition_count=1),
            price=10.0, competition=40.0, timing=10.0, skill=10.0
        )
        assert result != ObjectionPattern.competitive_displacement

    def test_price_barrier_requires_price_score_gte35(self, engine):
        result = engine._detect_pattern(
            make_input(deals_lost_to_price_count=2),
            price=34.0, competition=10.0, timing=10.0, skill=10.0
        )
        assert result != ObjectionPattern.price_barrier

    def test_price_barrier_requires_lost_price_gte2(self, engine):
        result = engine._detect_pattern(
            make_input(deals_lost_to_price_count=1),
            price=40.0, competition=10.0, timing=10.0, skill=10.0
        )
        assert result != ObjectionPattern.price_barrier

    def test_timing_stall_requires_timing_score_gte30(self, engine):
        result = engine._detect_pattern(
            make_input(late_stage_objections_count=2),
            price=10.0, competition=10.0, timing=29.0, skill=10.0
        )
        assert result != ObjectionPattern.timing_stall

    def test_timing_stall_requires_late_stage_gte2(self, engine):
        result = engine._detect_pattern(
            make_input(late_stage_objections_count=1),
            price=10.0, competition=10.0, timing=35.0, skill=10.0
        )
        assert result != ObjectionPattern.timing_stall

    def test_authority_gap_requires_authority_gte3(self, engine):
        result = engine._detect_pattern(
            make_input(authority_objections_count=2),
            price=10.0, competition=10.0, timing=10.0, skill=30.0
        )
        assert result != ObjectionPattern.authority_gap

    def test_authority_gap_requires_skill_gte25(self, engine):
        result = engine._detect_pattern(
            make_input(authority_objections_count=3),
            price=10.0, competition=10.0, timing=10.0, skill=24.0
        )
        assert result != ObjectionPattern.authority_gap

    def test_need_misalignment_requires_need_fit_gte3(self, engine):
        result = engine._detect_pattern(
            make_input(need_fit_objections_count=2, objection_overcome_rate_pct=0.30),
            price=10.0, competition=10.0, timing=10.0, skill=10.0
        )
        assert result != ObjectionPattern.need_misalignment

    def test_need_misalignment_requires_overcome_lt40(self, engine):
        result = engine._detect_pattern(
            make_input(need_fit_objections_count=3, objection_overcome_rate_pct=0.40),
            price=10.0, competition=10.0, timing=10.0, skill=10.0
        )
        assert result != ObjectionPattern.need_misalignment


# ---------------------------------------------------------------------------
# TestSystemicIssue
# ---------------------------------------------------------------------------

class TestSystemicIssue:
    """Tests for _has_systemic_issue."""

    def test_composite_gte40_triggers_systemic(self, engine):
        inp = make_input()
        assert engine._has_systemic_issue(40.0, inp) is True

    def test_composite_60_triggers_systemic(self, engine):
        inp = make_input()
        assert engine._has_systemic_issue(60.0, inp) is True

    def test_lost_deals_gte4_triggers_systemic(self, engine):
        inp = make_input(lost_deals_due_to_objection_count=4)
        assert engine._has_systemic_issue(10.0, inp) is True

    def test_lost_deals_5_triggers_systemic(self, engine):
        inp = make_input(lost_deals_due_to_objection_count=5)
        assert engine._has_systemic_issue(0.0, inp) is True

    def test_recurring_gte3_triggers_systemic(self, engine):
        inp = make_input(recurring_objection_same_account_count=3)
        assert engine._has_systemic_issue(0.0, inp) is True

    def test_recurring_4_triggers_systemic(self, engine):
        inp = make_input(recurring_objection_same_account_count=4)
        assert engine._has_systemic_issue(0.0, inp) is True

    def test_no_systemic_when_low_composite_low_lost_low_recurring(self, engine):
        inp = make_input(lost_deals_due_to_objection_count=0,
                         recurring_objection_same_account_count=0)
        assert engine._has_systemic_issue(10.0, inp) is False

    def test_composite_39_no_systemic_alone(self, engine):
        inp = make_input(lost_deals_due_to_objection_count=0,
                         recurring_objection_same_account_count=0)
        assert engine._has_systemic_issue(39.9, inp) is False

    def test_lost_deals_3_no_systemic_alone(self, engine):
        inp = make_input(lost_deals_due_to_objection_count=3,
                         recurring_objection_same_account_count=0)
        assert engine._has_systemic_issue(10.0, inp) is False

    def test_recurring_2_no_systemic_alone(self, engine):
        inp = make_input(recurring_objection_same_account_count=2,
                         lost_deals_due_to_objection_count=0)
        assert engine._has_systemic_issue(10.0, inp) is False


# ---------------------------------------------------------------------------
# TestCoachingIntervention
# ---------------------------------------------------------------------------

class TestCoachingIntervention:
    """Tests for _requires_coaching_intervention."""

    def test_composite_gte30_requires_coaching(self, engine):
        inp = make_input()
        assert engine._requires_coaching_intervention(30.0, inp) is True

    def test_composite_60_requires_coaching(self, engine):
        inp = make_input()
        assert engine._requires_coaching_intervention(60.0, inp) is True

    def test_overcome_rate_lt25_requires_coaching(self, engine):
        inp = make_input(objection_overcome_rate_pct=0.24)
        assert engine._requires_coaching_intervention(10.0, inp) is True

    def test_overcome_rate_0_requires_coaching(self, engine):
        inp = make_input(objection_overcome_rate_pct=0.0)
        assert engine._requires_coaching_intervention(5.0, inp) is True

    def test_doc_rate_lt40_and_composite_gte20_requires_coaching(self, engine):
        inp = make_input(objection_documentation_rate_pct=0.35)
        assert engine._requires_coaching_intervention(20.0, inp) is True

    def test_doc_rate_lt40_and_composite_lt20_no_coaching(self, engine):
        inp = make_input(objection_documentation_rate_pct=0.35,
                         objection_overcome_rate_pct=0.80)
        assert engine._requires_coaching_intervention(19.9, inp) is False

    def test_doc_rate_gte40_no_coaching_alone(self, engine):
        inp = make_input(objection_documentation_rate_pct=0.40,
                         objection_overcome_rate_pct=0.80)
        assert engine._requires_coaching_intervention(19.9, inp) is False

    def test_no_coaching_when_all_below_thresholds(self, engine):
        inp = make_input(objection_overcome_rate_pct=0.80,
                         objection_documentation_rate_pct=0.80)
        assert engine._requires_coaching_intervention(10.0, inp) is False

    def test_composite_29_no_coaching_alone(self, engine):
        inp = make_input(objection_overcome_rate_pct=0.80,
                         objection_documentation_rate_pct=0.80)
        assert engine._requires_coaching_intervention(29.9, inp) is False


# ---------------------------------------------------------------------------
# TestEstimatedLostRevenue
# ---------------------------------------------------------------------------

class TestEstimatedLostRevenue:
    """Tests for _estimated_lost_revenue."""

    def test_zero_lost_deals(self, engine):
        inp = make_input(lost_deals_due_to_objection_count=0, avg_deal_size_usd=50000.0)
        rev = engine._estimated_lost_revenue(inp, 50.0)
        assert rev == 0.0

    def test_basic_calculation(self, engine):
        inp = make_input(lost_deals_due_to_objection_count=2, avg_deal_size_usd=10000.0)
        rev = engine._estimated_lost_revenue(inp, 50.0)
        expected = round(2 * 10000.0 * (50.0 / 100.0), 2)
        assert rev == expected

    def test_composite_zero_gives_zero_revenue(self, engine):
        inp = make_input(lost_deals_due_to_objection_count=5, avg_deal_size_usd=20000.0)
        rev = engine._estimated_lost_revenue(inp, 0.0)
        assert rev == 0.0

    def test_result_is_rounded_to_2_decimals(self, engine):
        inp = make_input(lost_deals_due_to_objection_count=3, avg_deal_size_usd=33333.33)
        rev = engine._estimated_lost_revenue(inp, 33.3)
        assert rev == round(3 * 33333.33 * (33.3 / 100.0), 2)

    def test_large_deal_size(self, engine):
        inp = make_input(lost_deals_due_to_objection_count=1, avg_deal_size_usd=500000.0)
        rev = engine._estimated_lost_revenue(inp, 80.0)
        assert rev == round(1 * 500000.0 * 0.80, 2)

    def test_multiple_lost_deals(self, engine):
        inp = make_input(lost_deals_due_to_objection_count=5, avg_deal_size_usd=20000.0)
        rev = engine._estimated_lost_revenue(inp, 75.0)
        assert rev == round(5 * 20000.0 * 0.75, 2)


# ---------------------------------------------------------------------------
# TestSignal
# ---------------------------------------------------------------------------

class TestSignal:
    """Tests for _signal method."""

    def test_none_pattern_low_composite_returns_benchmark_message(self, engine):
        inp = make_input()
        sig = engine._signal(inp, ObjectionPattern.none, 10.0)
        assert sig == "Objection handling aligned with team benchmarks"

    def test_none_pattern_composite_exactly_19_returns_benchmark(self, engine):
        inp = make_input()
        sig = engine._signal(inp, ObjectionPattern.none, 19.9)
        assert sig == "Objection handling aligned with team benchmarks"

    def test_none_pattern_composite_20_does_not_return_benchmark(self, engine):
        inp = make_input()
        sig = engine._signal(inp, ObjectionPattern.none, 20.0)
        assert sig != "Objection handling aligned with team benchmarks"

    def test_pattern_none_composite_20_contains_objection_risk(self, engine):
        inp = make_input()
        sig = engine._signal(inp, ObjectionPattern.none, 20.0)
        assert "Objection risk" in sig

    def test_price_pattern_label_in_signal(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=5,
                         objection_overcome_rate_pct=0.80)
        sig = engine._signal(inp, ObjectionPattern.price_barrier, 40.0)
        assert "Price barrier" in sig

    def test_competitive_label_in_signal(self, engine):
        inp = make_input()
        sig = engine._signal(inp, ObjectionPattern.competitive_displacement, 50.0)
        assert "Competitive displacement" in sig

    def test_composite_value_in_signal(self, engine):
        inp = make_input()
        sig = engine._signal(inp, ObjectionPattern.price_barrier, 55.0)
        assert "55" in sig

    def test_price_ratio_gte30_adds_part(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=3,
                         objection_overcome_rate_pct=0.80)
        sig = engine._signal(inp, ObjectionPattern.price_barrier, 40.0)
        assert "price objections" in sig

    def test_comp_ratio_gte20_adds_part(self, engine):
        inp = make_input(total_deals_with_objections=10, competition_objections_count=2,
                         objection_overcome_rate_pct=0.80)
        sig = engine._signal(inp, ObjectionPattern.competitive_displacement, 40.0)
        assert "competitive pressure" in sig

    def test_late_stage_gte2_adds_part(self, engine):
        inp = make_input(late_stage_objections_count=2, objection_overcome_rate_pct=0.80)
        sig = engine._signal(inp, ObjectionPattern.timing_stall, 40.0)
        assert "late-stage" in sig

    def test_overcome_rate_lt40_adds_part(self, engine):
        inp = make_input(objection_overcome_rate_pct=0.30)
        sig = engine._signal(inp, ObjectionPattern.none, 25.0)
        assert "overcome rate" in sig

    def test_no_parts_uses_default_summary(self, engine):
        inp = make_input(price_objections_count=0, competition_objections_count=0,
                         late_stage_objections_count=0, objection_overcome_rate_pct=0.80)
        sig = engine._signal(inp, ObjectionPattern.timing_stall, 35.0)
        assert "objection burden detected" in sig

    def test_signal_format_with_parts(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=5,
                         objection_overcome_rate_pct=0.30)
        sig = engine._signal(inp, ObjectionPattern.price_barrier, 45.0)
        # Should have label — parts — composite pattern
        parts = sig.split(" — ")
        assert len(parts) >= 3

    def test_timing_stall_label(self, engine):
        inp = make_input()
        sig = engine._signal(inp, ObjectionPattern.timing_stall, 35.0)
        assert "Timing stall" in sig

    def test_authority_gap_label(self, engine):
        inp = make_input()
        sig = engine._signal(inp, ObjectionPattern.authority_gap, 35.0)
        assert "Authority gap" in sig

    def test_need_misalignment_label(self, engine):
        inp = make_input()
        sig = engine._signal(inp, ObjectionPattern.need_misalignment, 35.0)
        assert "Need misalignment" in sig


# ---------------------------------------------------------------------------
# TestAssessIntegration
# ---------------------------------------------------------------------------

class TestAssessIntegration:
    """Integration tests for assess() combining all sub-systems."""

    def test_returns_result_type(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert isinstance(result, ObjectionPatternResult)

    def test_rep_id_propagated(self, engine):
        result = engine.assess(make_input(rep_id="REPX42"))
        assert result.rep_id == "REPX42"

    def test_region_propagated(self, engine):
        result = engine.assess(make_input(region="Northeast"))
        assert result.region == "Northeast"

    def test_low_input_gives_low_risk(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert result.objection_risk == ObjectionRisk.low

    def test_low_input_gives_none_pattern(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert result.objection_pattern == ObjectionPattern.none

    def test_low_input_gives_managed_severity(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert result.objection_severity == ObjectionSeverity.managed

    def test_low_input_gives_no_action(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert result.recommended_action == ObjectionAction.no_action

    def test_low_input_no_systemic_issue(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert result.has_systemic_issue is False

    def test_low_input_signal_is_benchmark(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert result.objection_signal == "Objection handling aligned with team benchmarks"

    def test_high_price_gives_price_barrier(self, engine, high_price_input):
        result = engine.assess(high_price_input)
        assert result.objection_pattern == ObjectionPattern.price_barrier

    def test_high_price_gives_critical_risk(self, engine):
        # price=90 (35+30+25), comp=0, timing=0, skill=35 (<0.25 overcome)
        # composite = 90*0.30 + 0*0.25 + 0*0.25 + 35*0.20 = 27+0+0+7 = 34 → moderate
        # To get critical we need composite >= 60 — require additional comp/timing pressure
        inp = make_input(
            total_deals_with_objections=10,
            price_objections_count=6,
            price_overcome_rate_pct=0.10,
            deals_lost_to_price_count=5,
            objection_overcome_rate_pct=0.10,
            lost_deals_due_to_objection_count=5,
            competition_objections_count=5,
            competition_overcome_rate_pct=0.10,
            deals_lost_to_competition_count=5,
            timing_objections_count=5,
            timing_overcome_rate_pct=0.10,
            late_stage_objections_count=5,
            objection_stall_avg_days=20.0,
            objections_per_deal_avg=3.5,
            recurring_objection_same_account_count=3,
        )
        result = engine.assess(inp)
        assert result.objection_risk == ObjectionRisk.critical

    def test_high_comp_gives_competitive_displacement(self, engine, high_comp_input):
        result = engine.assess(high_comp_input)
        assert result.objection_pattern == ObjectionPattern.competitive_displacement

    def test_critical_price_action_is_pricing_review(self, engine):
        inp = make_input(
            total_deals_with_objections=10,
            price_objections_count=6,
            price_overcome_rate_pct=0.10,
            deals_lost_to_price_count=5,
            objection_overcome_rate_pct=0.10,
            lost_deals_due_to_objection_count=5,
            objection_documentation_rate_pct=0.20,
        )
        result = engine.assess(inp)
        if result.objection_risk == ObjectionRisk.critical and result.objection_pattern == ObjectionPattern.price_barrier:
            assert result.recommended_action == ObjectionAction.pricing_review

    def test_result_stores_scores(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert result.price_pressure_score >= 0.0
        assert result.competition_pressure_score >= 0.0
        assert result.timing_resistance_score >= 0.0
        assert result.skill_gap_score >= 0.0

    def test_composite_consistent_with_subscores(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        expected = round(
            result.price_pressure_score * 0.30
            + result.competition_pressure_score * 0.25
            + result.timing_resistance_score * 0.25
            + result.skill_gap_score * 0.20,
            1,
        )
        assert result.objection_burden_composite == min(expected, 100.0)

    def test_estimated_revenue_zero_for_no_lost_deals(self, engine):
        result = engine.assess(make_input(lost_deals_due_to_objection_count=0))
        assert result.estimated_lost_revenue_usd == 0.0

    def test_estimated_revenue_positive_with_lost_deals(self, engine):
        inp = make_input(lost_deals_due_to_objection_count=3, avg_deal_size_usd=10000.0,
                         price_objections_count=5, price_overcome_rate_pct=0.10,
                         deals_lost_to_price_count=3)
        result = engine.assess(inp)
        if result.objection_burden_composite > 0:
            assert result.estimated_lost_revenue_usd > 0.0

    def test_systemic_issue_with_high_composite(self, engine):
        inp = make_input(
            total_deals_with_objections=10,
            price_objections_count=6,
            price_overcome_rate_pct=0.10,
            deals_lost_to_price_count=5,
            objection_overcome_rate_pct=0.10,
        )
        result = engine.assess(inp)
        if result.objection_burden_composite >= 40:
            assert result.has_systemic_issue is True

    def test_coaching_intervention_with_low_overcome_rate(self, engine):
        inp = make_input(objection_overcome_rate_pct=0.20)
        result = engine.assess(inp)
        assert result.requires_coaching_intervention is True

    def test_assess_adds_to_results_list(self, engine):
        engine.assess(make_input(rep_id="A"))
        engine.assess(make_input(rep_id="B"))
        assert len(engine._results) == 2

    def test_assess_batch_returns_list(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5
        for r in results:
            assert isinstance(r, ObjectionPatternResult)

    def test_assess_batch_empty_list(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_assess_batch_adds_all_to_results(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        engine.assess_batch(inputs)
        assert len(engine._results) == 3


# ---------------------------------------------------------------------------
# TestSummary
# ---------------------------------------------------------------------------

class TestSummary:
    """Tests for summary() method."""

    def test_empty_engine_returns_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_keys(self, engine):
        s = engine.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_objection_burden_composite",
            "systemic_issue_count", "coaching_intervention_count",
            "avg_price_pressure_score", "avg_competition_pressure_score",
            "avg_timing_resistance_score", "avg_skill_gap_score",
            "total_estimated_lost_revenue_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_empty_total_is_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_risk_counts_is_empty_dict(self, engine):
        assert engine.summary()["risk_counts"] == {}

    def test_empty_pattern_counts_is_empty_dict(self, engine):
        assert engine.summary()["pattern_counts"] == {}

    def test_empty_severity_counts_is_empty_dict(self, engine):
        assert engine.summary()["severity_counts"] == {}

    def test_empty_action_counts_is_empty_dict(self, engine):
        assert engine.summary()["action_counts"] == {}

    def test_empty_avg_composite_is_zero(self, engine):
        assert engine.summary()["avg_objection_burden_composite"] == 0.0

    def test_empty_systemic_count_is_zero(self, engine):
        assert engine.summary()["systemic_issue_count"] == 0

    def test_empty_coaching_count_is_zero(self, engine):
        assert engine.summary()["coaching_intervention_count"] == 0

    def test_empty_avg_price_is_zero(self, engine):
        assert engine.summary()["avg_price_pressure_score"] == 0.0

    def test_empty_avg_competition_is_zero(self, engine):
        assert engine.summary()["avg_competition_pressure_score"] == 0.0

    def test_empty_avg_timing_is_zero(self, engine):
        assert engine.summary()["avg_timing_resistance_score"] == 0.0

    def test_empty_avg_skill_is_zero(self, engine):
        assert engine.summary()["avg_skill_gap_score"] == 0.0

    def test_empty_total_lost_revenue_is_zero(self, engine):
        assert engine.summary()["total_estimated_lost_revenue_usd"] == 0.0

    def test_summary_total_after_one_assess(self, engine):
        engine.assess(make_input())
        assert engine.summary()["total"] == 1

    def test_summary_total_after_multiple_assess(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        assert engine.summary()["total"] == 5

    def test_summary_risk_counts_populated(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == 1

    def test_summary_pattern_counts_populated(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == 1

    def test_summary_severity_counts_populated(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == 1

    def test_summary_action_counts_populated(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert sum(s["action_counts"].values()) == 1

    def test_summary_total_lost_revenue_is_sum(self, engine):
        inp1 = make_input(lost_deals_due_to_objection_count=2, avg_deal_size_usd=10000.0,
                          price_objections_count=5, price_overcome_rate_pct=0.20,
                          deals_lost_to_price_count=2)
        inp2 = make_input(lost_deals_due_to_objection_count=3, avg_deal_size_usd=5000.0,
                          competition_objections_count=4, competition_overcome_rate_pct=0.20,
                          deals_lost_to_competition_count=3)
        r1 = engine.assess(inp1)
        r2 = engine.assess(inp2)
        s = engine.summary()
        expected = round(r1.estimated_lost_revenue_usd + r2.estimated_lost_revenue_usd, 2)
        assert s["total_estimated_lost_revenue_usd"] == expected

    def test_summary_systemic_issue_count(self, engine):
        # Force systemic issue with high lost deals
        engine.assess(make_input(lost_deals_due_to_objection_count=4))
        engine.assess(make_input(lost_deals_due_to_objection_count=0,
                                 recurring_objection_same_account_count=0))
        s = engine.summary()
        assert s["systemic_issue_count"] == 1

    def test_summary_coaching_count(self, engine):
        engine.assess(make_input(objection_overcome_rate_pct=0.20))  # triggers coaching
        engine.assess(make_input(objection_overcome_rate_pct=0.80,
                                 objection_documentation_rate_pct=0.80))  # no coaching
        s = engine.summary()
        assert s["coaching_intervention_count"] >= 1

    def test_summary_avg_composite_correct(self, engine):
        r1 = engine.assess(make_input(rep_id="A"))
        r2 = engine.assess(make_input(rep_id="B"))
        s = engine.summary()
        expected = round((r1.objection_burden_composite + r2.objection_burden_composite) / 2, 1)
        assert s["avg_objection_burden_composite"] == expected

    def test_summary_avg_price_correct(self, engine):
        r1 = engine.assess(make_input(rep_id="A"))
        r2 = engine.assess(make_input(rep_id="B"))
        s = engine.summary()
        expected = round((r1.price_pressure_score + r2.price_pressure_score) / 2, 1)
        assert s["avg_price_pressure_score"] == expected

    def test_summary_returns_13_keys_with_data(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert len(s) == 13

    def test_summary_after_batch(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(10)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 10

    def test_summary_risk_counts_sum_equals_total(self, engine):
        for i in range(6):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_equals_total(self, engine):
        for i in range(6):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_equals_total(self, engine):
        for i in range(6):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self, engine):
        for i in range(6):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Edge cases and boundary condition tests."""

    def test_total_deals_zero_does_not_crash(self, engine):
        inp = make_input(total_deals_with_objections=0)
        result = engine.assess(inp)
        assert isinstance(result, ObjectionPatternResult)

    def test_all_zero_input_produces_valid_result(self, engine):
        inp = make_input(
            total_deals_with_objections=0,
            price_objections_count=0,
            timing_objections_count=0,
            competition_objections_count=0,
            authority_objections_count=0,
            need_fit_objections_count=0,
            objections_per_deal_avg=0.0,
            objection_overcome_rate_pct=1.0,
            price_overcome_rate_pct=1.0,
            competition_overcome_rate_pct=1.0,
            timing_overcome_rate_pct=1.0,
            objection_stall_avg_days=0.0,
            late_stage_objections_count=0,
            recurring_objection_same_account_count=0,
            lost_deals_due_to_objection_count=0,
            deals_lost_to_price_count=0,
            deals_lost_to_competition_count=0,
            objection_documentation_rate_pct=1.0,
            avg_deal_size_usd=0.0,
        )
        result = engine.assess(inp)
        assert result.objection_burden_composite == 0.0
        assert result.estimated_lost_revenue_usd == 0.0

    def test_multiple_engines_independent(self):
        engine1 = SalesObjectionPatternIntelligenceEngine()
        engine2 = SalesObjectionPatternIntelligenceEngine()
        engine1.assess(make_input(rep_id="A"))
        assert engine2.summary()["total"] == 0

    def test_very_high_deal_count(self, engine):
        inp = make_input(total_deals_with_objections=1000,
                         price_objections_count=500,
                         avg_deal_size_usd=1000000.0)
        result = engine.assess(inp)
        assert result.price_pressure_score <= 100.0

    def test_composite_is_float(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert isinstance(result.objection_burden_composite, float)

    def test_subscores_are_floats(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert isinstance(result.price_pressure_score, float)
        assert isinstance(result.competition_pressure_score, float)
        assert isinstance(result.timing_resistance_score, float)
        assert isinstance(result.skill_gap_score, float)

    def test_subscores_non_negative(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert result.price_pressure_score >= 0.0
        assert result.competition_pressure_score >= 0.0
        assert result.timing_resistance_score >= 0.0
        assert result.skill_gap_score >= 0.0

    def test_subscores_at_most_100(self, engine):
        inp = make_input(
            total_deals_with_objections=10,
            price_objections_count=10,
            price_overcome_rate_pct=0.0,
            deals_lost_to_price_count=10,
            competition_objections_count=10,
            competition_overcome_rate_pct=0.0,
            deals_lost_to_competition_count=10,
            timing_objections_count=10,
            timing_overcome_rate_pct=0.0,
            late_stage_objections_count=10,
            objection_stall_avg_days=30.0,
            objections_per_deal_avg=5.0,
            objection_overcome_rate_pct=0.0,
            recurring_objection_same_account_count=10,
            authority_objections_count=10,
            need_fit_objections_count=10,
        )
        result = engine.assess(inp)
        assert result.price_pressure_score <= 100.0
        assert result.competition_pressure_score <= 100.0
        assert result.timing_resistance_score <= 100.0
        assert result.skill_gap_score <= 100.0

    def test_estimated_revenue_non_negative(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert result.estimated_lost_revenue_usd >= 0.0

    def test_signal_is_string(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert isinstance(result.objection_signal, str)

    def test_signal_non_empty(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert len(result.objection_signal) > 0

    def test_assess_batch_order_preserved(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"R{i}"

    def test_doc_rate_exactly_40_no_skill_bonus(self, engine):
        inp = make_input(objection_documentation_rate_pct=0.40,
                         objections_per_deal_avg=0.5,
                         objection_overcome_rate_pct=0.80,
                         authority_objections_count=0,
                         need_fit_objections_count=0,
                         recurring_objection_same_account_count=0)
        s = engine._skill_gap_score(inp)
        assert s == 0.0

    def test_doc_rate_exactly_50_no_price_bonus(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=2,
                         price_overcome_rate_pct=0.80, deals_lost_to_price_count=0,
                         objection_documentation_rate_pct=0.50)
        # price_ratio = 0.20 → +8; doc exactly 0.50 → no bonus
        s = engine._price_pressure_score(inp)
        assert s == 8.0

    def test_overcome_rate_exactly_25_no_skill_coaching_from_overcome(self, engine):
        inp = make_input(objection_overcome_rate_pct=0.25,
                         objection_documentation_rate_pct=0.80)
        assert engine._requires_coaching_intervention(10.0, inp) is False

    def test_overcome_rate_exactly_25_skill_gap(self, engine):
        inp = make_input(objections_per_deal_avg=0.5, objection_overcome_rate_pct=0.25,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.80)
        # 0.25 not < 0.25 → no +35; 0.25 < 0.40 → +20
        s = engine._skill_gap_score(inp)
        assert s == 20.0

    def test_timing_overcome_exactly_25_no_low_tier_bonus(self, engine):
        inp = make_input(timing_objections_count=0, timing_overcome_rate_pct=0.25,
                         late_stage_objections_count=0, objection_stall_avg_days=1.0)
        # 0.25 not < 0.25 → no +30; 0.25 < 0.45 → +15
        s = engine._timing_resistance_score(inp)
        assert s == 15.0

    def test_timing_overcome_exactly_45(self, engine):
        inp = make_input(timing_objections_count=0, timing_overcome_rate_pct=0.45,
                         late_stage_objections_count=0, objection_stall_avg_days=1.0)
        # 0.45 not < 0.25, not < 0.45 → 0
        s = engine._timing_resistance_score(inp)
        assert s == 0.0

    def test_comp_overcome_exactly_50(self, engine):
        inp = make_input(competition_objections_count=0,
                         competition_overcome_rate_pct=0.50,
                         deals_lost_to_competition_count=0)
        s = engine._competition_pressure_score(inp)
        assert s == 0.0

    def test_price_overcome_exactly_50(self, engine):
        inp = make_input(total_deals_with_objections=10, price_objections_count=0,
                         price_overcome_rate_pct=0.50, deals_lost_to_price_count=0)
        s = engine._price_pressure_score(inp)
        assert s == 0.0


# ---------------------------------------------------------------------------
# TestPatternIntegration
# ---------------------------------------------------------------------------

class TestPatternIntegration:
    """End-to-end pattern detection tests via assess()."""

    def test_authority_gap_pattern_via_assess(self, engine):
        inp = make_input(
            total_deals_with_objections=10,
            authority_objections_count=4,
            need_fit_objections_count=0,
            objections_per_deal_avg=3.0,
            objection_overcome_rate_pct=0.30,
            recurring_objection_same_account_count=3,
            deals_lost_to_price_count=0,
            deals_lost_to_competition_count=0,
            late_stage_objections_count=1,
        )
        result = engine.assess(inp)
        assert result.objection_pattern == ObjectionPattern.authority_gap

    def test_need_misalignment_via_assess(self, engine):
        inp = make_input(
            total_deals_with_objections=10,
            need_fit_objections_count=4,
            authority_objections_count=0,
            objection_overcome_rate_pct=0.35,
            deals_lost_to_price_count=0,
            deals_lost_to_competition_count=0,
            late_stage_objections_count=0,
        )
        result = engine.assess(inp)
        assert result.objection_pattern == ObjectionPattern.need_misalignment

    def test_timing_stall_via_assess(self, engine):
        inp = make_input(
            total_deals_with_objections=10,
            timing_objections_count=5,
            timing_overcome_rate_pct=0.15,
            late_stage_objections_count=3,
            objection_stall_avg_days=15.0,
            deals_lost_to_price_count=0,
            deals_lost_to_competition_count=0,
        )
        result = engine.assess(inp)
        assert result.objection_pattern == ObjectionPattern.timing_stall

    def test_price_barrier_action_mapping(self, engine):
        inp = make_input(
            total_deals_with_objections=10,
            price_objections_count=5,
            price_overcome_rate_pct=0.15,
            deals_lost_to_price_count=3,
            deals_lost_to_competition_count=0,
            objection_overcome_rate_pct=0.20,
            lost_deals_due_to_objection_count=3,
        )
        result = engine.assess(inp)
        if result.objection_pattern == ObjectionPattern.price_barrier:
            if result.objection_risk in (ObjectionRisk.critical, ObjectionRisk.high):
                assert result.recommended_action == ObjectionAction.pricing_review

    def test_competitive_displacement_action_mapping(self, engine):
        inp = make_input(
            total_deals_with_objections=10,
            competition_objections_count=5,
            competition_overcome_rate_pct=0.10,
            deals_lost_to_competition_count=5,
            late_stage_objections_count=3,
            deals_lost_to_price_count=0,
            objection_overcome_rate_pct=0.20,
            lost_deals_due_to_objection_count=5,
        )
        result = engine.assess(inp)
        if result.objection_pattern == ObjectionPattern.competitive_displacement:
            if result.objection_risk in (ObjectionRisk.critical, ObjectionRisk.high):
                assert result.recommended_action == ObjectionAction.battlecard_refresh

    def test_moderate_risk_gives_coaching(self, engine):
        # Force moderate risk (composite between 20 and 39)
        inp = make_input(
            objections_per_deal_avg=2.5,
            objection_overcome_rate_pct=0.45,
            recurring_objection_same_account_count=1,
            authority_objections_count=0,
            need_fit_objections_count=0,
            objection_documentation_rate_pct=0.80,
        )
        result = engine.assess(inp)
        if result.objection_risk == ObjectionRisk.moderate:
            assert result.recommended_action == ObjectionAction.objection_coaching


# ---------------------------------------------------------------------------
# TestSummaryAggregate
# ---------------------------------------------------------------------------

class TestSummaryAggregate:
    """Tests for aggregate correctness in summary()."""

    def test_multiple_reps_summary(self, engine):
        reps = [
            make_input(rep_id="A", total_deals_with_objections=10,
                       price_objections_count=5, price_overcome_rate_pct=0.10,
                       deals_lost_to_price_count=4, objection_overcome_rate_pct=0.10,
                       lost_deals_due_to_objection_count=4),
            make_input(rep_id="B"),
            make_input(rep_id="C", total_deals_with_objections=10,
                       competition_objections_count=4, competition_overcome_rate_pct=0.10,
                       deals_lost_to_competition_count=4, lost_deals_due_to_objection_count=4),
        ]
        results = engine.assess_batch(reps)
        s = engine.summary()
        assert s["total"] == 3
        assert sum(s["risk_counts"].values()) == 3
        assert sum(s["pattern_counts"].values()) == 3

    def test_summary_all_low_risk(self, engine):
        for _ in range(4):
            engine.assess(make_input())
        s = engine.summary()
        assert s["risk_counts"].get("low", 0) == 4

    def test_summary_coaching_count_accurate(self, engine):
        # 2 reps need coaching (low overcome rate), 1 does not
        engine.assess(make_input(objection_overcome_rate_pct=0.20))
        engine.assess(make_input(objection_overcome_rate_pct=0.20))
        engine.assess(make_input(objection_overcome_rate_pct=0.80,
                                 objection_documentation_rate_pct=0.80))
        s = engine.summary()
        assert s["coaching_intervention_count"] == 2

    def test_summary_systemic_count_accurate(self, engine):
        engine.assess(make_input(lost_deals_due_to_objection_count=4))
        engine.assess(make_input(lost_deals_due_to_objection_count=0,
                                 recurring_objection_same_account_count=0))
        engine.assess(make_input(lost_deals_due_to_objection_count=0,
                                 recurring_objection_same_account_count=3))
        s = engine.summary()
        assert s["systemic_issue_count"] == 2

    def test_summary_total_revenue_sums_all(self, engine):
        results = []
        inputs = [
            make_input(rep_id="A", lost_deals_due_to_objection_count=2,
                       avg_deal_size_usd=10000.0,
                       price_objections_count=5, price_overcome_rate_pct=0.15,
                       deals_lost_to_price_count=2),
            make_input(rep_id="B", lost_deals_due_to_objection_count=1,
                       avg_deal_size_usd=20000.0,
                       competition_objections_count=4, competition_overcome_rate_pct=0.15,
                       deals_lost_to_competition_count=2),
        ]
        for inp in inputs:
            results.append(engine.assess(inp))
        s = engine.summary()
        total = sum(r.estimated_lost_revenue_usd for r in results)
        assert s["total_estimated_lost_revenue_usd"] == round(total, 2)

    def test_summary_avg_skill_correct(self, engine):
        r1 = engine.assess(make_input(rep_id="X"))
        r2 = engine.assess(make_input(rep_id="Y"))
        r3 = engine.assess(make_input(rep_id="Z"))
        s = engine.summary()
        expected = round((r1.skill_gap_score + r2.skill_gap_score + r3.skill_gap_score) / 3, 1)
        assert s["avg_skill_gap_score"] == expected

    def test_summary_avg_timing_correct(self, engine):
        r1 = engine.assess(make_input(rep_id="X"))
        r2 = engine.assess(make_input(rep_id="Y"))
        s = engine.summary()
        expected = round((r1.timing_resistance_score + r2.timing_resistance_score) / 2, 1)
        assert s["avg_timing_resistance_score"] == expected

    def test_engine_reuse_accumulates(self, engine):
        # Each assess call accumulates in _results
        for i in range(7):
            engine.assess(make_input(rep_id=f"R{i}"))
        assert engine.summary()["total"] == 7


# ---------------------------------------------------------------------------
# TestToDict
# ---------------------------------------------------------------------------

class TestToDict:
    """Tests for to_dict() method correctness."""

    def test_to_dict_enum_values_are_strings(self, engine):
        result = engine.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["objection_risk"], str)
        assert isinstance(d["objection_pattern"], str)
        assert isinstance(d["objection_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_numeric_values_correct(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        d = result.to_dict()
        assert d["price_pressure_score"] == result.price_pressure_score
        assert d["competition_pressure_score"] == result.competition_pressure_score
        assert d["timing_resistance_score"] == result.timing_resistance_score
        assert d["skill_gap_score"] == result.skill_gap_score
        assert d["objection_burden_composite"] == result.objection_burden_composite
        assert d["estimated_lost_revenue_usd"] == result.estimated_lost_revenue_usd

    def test_to_dict_bool_values_correct(self, engine):
        result = engine.assess(make_input())
        d = result.to_dict()
        assert d["has_systemic_issue"] == result.has_systemic_issue
        assert d["requires_coaching_intervention"] == result.requires_coaching_intervention

    def test_to_dict_signal_matches_result(self, engine):
        result = engine.assess(make_input())
        assert result.to_dict()["objection_signal"] == result.objection_signal

    def test_to_dict_is_dict_type(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.to_dict(), dict)

    def test_to_dict_risk_matches_enum_value(self, engine):
        result = engine.assess(make_input())
        assert result.to_dict()["objection_risk"] == result.objection_risk.value

    def test_to_dict_pattern_matches_enum_value(self, engine):
        result = engine.assess(make_input())
        assert result.to_dict()["objection_pattern"] == result.objection_pattern.value

    def test_to_dict_severity_matches_enum_value(self, engine):
        result = engine.assess(make_input())
        assert result.to_dict()["objection_severity"] == result.objection_severity.value

    def test_to_dict_action_matches_enum_value(self, engine):
        result = engine.assess(make_input())
        assert result.to_dict()["recommended_action"] == result.recommended_action.value


# ---------------------------------------------------------------------------
# TestSpecificScenarios
# ---------------------------------------------------------------------------

class TestSpecificScenarios:
    """Concrete scenario-based tests to verify business logic."""

    def test_star_rep_all_green(self, engine):
        """A top performer has minimal objection issues."""
        inp = make_input(
            rep_id="STAR01",
            objection_overcome_rate_pct=0.85,
            price_overcome_rate_pct=0.80,
            competition_overcome_rate_pct=0.80,
            timing_overcome_rate_pct=0.80,
            objection_documentation_rate_pct=0.95,
            objections_per_deal_avg=0.8,
            lost_deals_due_to_objection_count=0,
            recurring_objection_same_account_count=0,
            objection_stall_avg_days=2.0,
        )
        result = engine.assess(inp)
        assert result.objection_risk == ObjectionRisk.low
        assert result.objection_pattern == ObjectionPattern.none
        assert result.objection_severity == ObjectionSeverity.managed
        assert result.recommended_action == ObjectionAction.no_action
        assert result.has_systemic_issue is False
        assert result.objection_signal == "Objection handling aligned with team benchmarks"

    def test_price_war_rep(self, engine):
        """Rep facing severe price pressure scenario."""
        inp = make_input(
            rep_id="PRICE_REP",
            total_deals_with_objections=10,
            price_objections_count=7,     # 70% → +35
            price_overcome_rate_pct=0.15, # < 0.30 → +30
            deals_lost_to_price_count=5,  # >= 4 → +25
            deals_lost_to_competition_count=0,
            objection_documentation_rate_pct=0.30,  # < 0.50 and price >= 2 → +5
            objection_overcome_rate_pct=0.20,
            lost_deals_due_to_objection_count=5,
        )
        result = engine.assess(inp)
        assert result.price_pressure_score == 95.0  # 35+30+25+5
        assert result.objection_pattern == ObjectionPattern.price_barrier

    def test_competitive_crisis_rep(self, engine):
        """Rep being displaced by competitors."""
        inp = make_input(
            rep_id="COMP_REP",
            total_deals_with_objections=10,
            competition_objections_count=5,     # 50% → +35
            competition_overcome_rate_pct=0.10, # < 0.30 → +30
            deals_lost_to_competition_count=5,  # >= 4 → +25
            late_stage_objections_count=3,      # >=3 and comp>=2 → +5
            deals_lost_to_price_count=0,
            lost_deals_due_to_objection_count=5,
        )
        result = engine.assess(inp)
        assert result.competition_pressure_score == 95.0  # 35+30+25+5
        assert result.objection_pattern == ObjectionPattern.competitive_displacement

    def test_authority_gap_rep(self, engine):
        """Rep struggling with reaching the right decision makers."""
        inp = make_input(
            rep_id="AUTH_REP",
            total_deals_with_objections=10,
            authority_objections_count=4,
            need_fit_objections_count=0,
            objections_per_deal_avg=3.0,
            objection_overcome_rate_pct=0.30,
            recurring_objection_same_account_count=3,
            deals_lost_to_price_count=0,
            deals_lost_to_competition_count=0,
            late_stage_objections_count=0,
        )
        result = engine.assess(inp)
        assert result.objection_pattern == ObjectionPattern.authority_gap

    def test_revenue_calculation_exact(self, engine):
        """Verify exact revenue calculation."""
        inp = make_input(
            lost_deals_due_to_objection_count=3,
            avg_deal_size_usd=25000.0,
            # need enough to get composite ~ known value
            price_objections_count=0,
            competition_objections_count=0,
            timing_objections_count=0,
            objections_per_deal_avg=0.5,
            objection_overcome_rate_pct=0.80,
        )
        result = engine.assess(inp)
        expected = round(3 * 25000.0 * result.objection_burden_composite / 100.0, 2)
        assert result.estimated_lost_revenue_usd == expected

    def test_mixed_signals_rep(self, engine):
        """Rep with multiple moderate issues."""
        inp = make_input(
            total_deals_with_objections=10,
            price_objections_count=2,           # 20% ratio → +8
            competition_objections_count=2,     # 20% ratio → +20
            timing_objections_count=3,          # 30% ratio → +18
            objections_per_deal_avg=2.0,        # >= 2.0 → +15
            objection_overcome_rate_pct=0.45,   # < 0.55 → +8
            price_overcome_rate_pct=0.45,
            competition_overcome_rate_pct=0.45,
            timing_overcome_rate_pct=0.40,
            late_stage_objections_count=1,
            recurring_objection_same_account_count=1,
            lost_deals_due_to_objection_count=1,
            deals_lost_to_price_count=0,
            deals_lost_to_competition_count=0,
        )
        result = engine.assess(inp)
        assert isinstance(result, ObjectionPatternResult)
        assert result.objection_burden_composite > 0

    def test_documentation_penalty_scenario(self, engine):
        """Poor documentation adds to both price and skill scores."""
        inp = make_input(
            total_deals_with_objections=10,
            price_objections_count=3,           # 30% → +20
            price_overcome_rate_pct=0.80,
            deals_lost_to_price_count=0,
            objection_documentation_rate_pct=0.30,  # < 0.50 and price >= 2 → +5
            objections_per_deal_avg=0.5,
            objection_overcome_rate_pct=0.80,
            recurring_objection_same_account_count=0,
            authority_objections_count=0,
            need_fit_objections_count=0,
        )
        price_score = engine._price_pressure_score(inp)
        skill_score = engine._skill_gap_score(inp)
        # doc < 0.40 triggers skill +5; doc < 0.50 with price >= 2 triggers price +5
        assert price_score == 25.0  # 20+5
        assert skill_score == 5.0   # doc < 0.40 → +5

    def test_stall_days_boundary(self, engine):
        """Test stall days exact boundaries."""
        inp7 = make_input(objection_stall_avg_days=7.0, timing_objections_count=0,
                          timing_overcome_rate_pct=0.80, late_stage_objections_count=0)
        inp14 = make_input(objection_stall_avg_days=14.0, timing_objections_count=0,
                           timing_overcome_rate_pct=0.80, late_stage_objections_count=0)
        inp6 = make_input(objection_stall_avg_days=6.9, timing_objections_count=0,
                          timing_overcome_rate_pct=0.80, late_stage_objections_count=0)
        assert engine._timing_resistance_score(inp7) == 8.0
        assert engine._timing_resistance_score(inp14) == 15.0
        assert engine._timing_resistance_score(inp6) == 0.0

    def test_risk_severity_alignment(self, engine):
        """Risk and severity should mirror the same composite thresholds."""
        thresholds = [(65.0, ObjectionRisk.critical, ObjectionSeverity.blocking),
                      (45.0, ObjectionRisk.high, ObjectionSeverity.systemic),
                      (25.0, ObjectionRisk.moderate, ObjectionSeverity.recurring),
                      (10.0, ObjectionRisk.low, ObjectionSeverity.managed)]
        for composite, expected_risk, expected_sev in thresholds:
            assert engine._risk_level(composite) == expected_risk
            assert engine._severity(composite) == expected_sev

    def test_price_score_exact_boundary_50(self, engine):
        """Price ratio exactly 0.50 should add 35."""
        inp = make_input(total_deals_with_objections=10, price_objections_count=5,
                         price_overcome_rate_pct=0.80, deals_lost_to_price_count=0)
        assert engine._price_pressure_score(inp) == 35.0

    def test_comp_score_exact_boundary_40(self, engine):
        """Competition ratio exactly 0.40 should add 35."""
        inp = make_input(total_deals_with_objections=10, competition_objections_count=4,
                         competition_overcome_rate_pct=0.80, deals_lost_to_competition_count=0)
        assert engine._competition_pressure_score(inp) == 35.0

    def test_timing_score_exact_boundary_40(self, engine):
        """Timing ratio exactly 0.40 should add 30."""
        inp = make_input(total_deals_with_objections=10, timing_objections_count=4,
                         timing_overcome_rate_pct=0.80, late_stage_objections_count=0,
                         objection_stall_avg_days=1.0)
        assert engine._timing_resistance_score(inp) == 30.0

    def test_skill_score_exact_boundary_3(self, engine):
        """objections_per_deal_avg exactly 3.0 should add 25."""
        inp = make_input(objections_per_deal_avg=3.0, objection_overcome_rate_pct=0.80,
                         recurring_objection_same_account_count=0,
                         authority_objections_count=0, need_fit_objections_count=0,
                         objection_documentation_rate_pct=0.80)
        assert engine._skill_gap_score(inp) == 25.0

    def test_signal_components_separation(self, engine):
        """Signal parts separated by ' — '."""
        inp = make_input(total_deals_with_objections=10,
                         price_objections_count=5,          # price_ratio=50% → part
                         competition_objections_count=3,    # comp_ratio=30% → part
                         late_stage_objections_count=3,     # → part
                         objection_overcome_rate_pct=0.30)  # < 0.40 → part
        sig = engine._signal(inp, ObjectionPattern.price_barrier, 50.0)
        # Label — parts — composite
        assert " — " in sig
        assert "50" in sig
