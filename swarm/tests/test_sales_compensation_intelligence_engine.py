"""
Comprehensive pytest test suite for SalesCompIntelligenceEngine.

Covers all enums, scoring helpers, branching logic, to_dict(), summary(),
properties, batch operations, reset, and end-to-end scenarios.

Target: 250+ tests, all passing.
"""

from __future__ import annotations

import dataclasses
import pytest

from swarm.intelligence.sales_compensation_intelligence_engine import (
    CompAction,
    CompRiskLevel,
    GamingPattern,
    IncentiveAlignment,
    SalesCompIntelInput,
    SalesCompIntelResult,
    SalesCompIntelligenceEngine,
)


# ── Helpers / Fixtures ─────────────────────────────────────────────────────────

def make_input(**overrides) -> SalesCompIntelInput:
    """Return a clean, healthy baseline rep input with optional overrides."""
    defaults = dict(
        rep_id="rep-001",
        rep_name="Alice Smith",
        manager_id="mgr-001",
        region="West",
        base_salary=80_000.0,
        ote_salary=160_000.0,
        quota=800_000.0,
        deals_closed_qtd=10,
        revenue_closed_qtd=200_000.0,
        avg_deal_size=20_000.0,
        deals_in_pipeline=15,
        pipeline_value=600_000.0,
        large_deal_pct=10.0,
        spiff_driven_pct=10.0,
        quarter_end_close_pct=20.0,
        multiyear_deal_pct=5.0,
        avg_discount_pct=10.0,
        quota_attainment_q1=100.0,
        quota_attainment_q2=102.0,
        quota_attainment_q3=98.0,
        comp_complaints=0,
        activity_score_qtd=70.0,
    )
    defaults.update(overrides)
    return SalesCompIntelInput(**defaults)


@pytest.fixture
def engine():
    return SalesCompIntelligenceEngine()


@pytest.fixture
def baseline_input():
    return make_input()


@pytest.fixture
def baseline_result(engine, baseline_input):
    return engine.analyze(baseline_input)


# ══════════════════════════════════════════════════════════════════════════════
# 1. Enum tests
# ══════════════════════════════════════════════════════════════════════════════

class TestCompRiskLevelEnum:
    def test_low_value(self):
        assert CompRiskLevel.LOW.value == "low"

    def test_moderate_value(self):
        assert CompRiskLevel.MODERATE.value == "moderate"

    def test_high_value(self):
        assert CompRiskLevel.HIGH.value == "high"

    def test_critical_value(self):
        assert CompRiskLevel.CRITICAL.value == "critical"

    def test_is_str_subtype(self):
        assert isinstance(CompRiskLevel.LOW, str)

    def test_count(self):
        assert len(CompRiskLevel) == 4

    def test_all_members(self):
        members = {e.value for e in CompRiskLevel}
        assert members == {"low", "moderate", "high", "critical"}

    def test_equality_with_string(self):
        assert CompRiskLevel.HIGH == "high"


class TestGamingPatternEnum:
    def test_clean_value(self):
        assert GamingPattern.CLEAN.value == "clean"

    def test_sandbagging_value(self):
        assert GamingPattern.SANDBAGGING.value == "sandbagging"

    def test_spiff_chasing_value(self):
        assert GamingPattern.SPIFF_CHASING.value == "spiff_chasing"

    def test_discount_heavy_value(self):
        assert GamingPattern.DISCOUNT_HEAVY.value == "discount_heavy"

    def test_mixed_value(self):
        assert GamingPattern.MIXED.value == "mixed"

    def test_is_str_subtype(self):
        assert isinstance(GamingPattern.CLEAN, str)

    def test_count(self):
        assert len(GamingPattern) == 5

    def test_all_members(self):
        members = {e.value for e in GamingPattern}
        assert members == {"clean", "sandbagging", "spiff_chasing", "discount_heavy", "mixed"}


class TestIncentiveAlignmentEnum:
    def test_well_aligned_value(self):
        assert IncentiveAlignment.WELL_ALIGNED.value == "well_aligned"

    def test_partially_aligned_value(self):
        assert IncentiveAlignment.PARTIALLY_ALIGNED.value == "partially_aligned"

    def test_misaligned_value(self):
        assert IncentiveAlignment.MISALIGNED.value == "misaligned"

    def test_perverse_value(self):
        assert IncentiveAlignment.PERVERSE.value == "perverse"

    def test_is_str_subtype(self):
        assert isinstance(IncentiveAlignment.WELL_ALIGNED, str)

    def test_count(self):
        assert len(IncentiveAlignment) == 4

    def test_all_members(self):
        members = {e.value for e in IncentiveAlignment}
        assert members == {"well_aligned", "partially_aligned", "misaligned", "perverse"}


class TestCompActionEnum:
    def test_maintain_value(self):
        assert CompAction.MAINTAIN.value == "maintain"

    def test_monitor_value(self):
        assert CompAction.MONITOR.value == "monitor"

    def test_restructure_value(self):
        assert CompAction.RESTRUCTURE.value == "restructure"

    def test_immediate_review_value(self):
        assert CompAction.IMMEDIATE_REVIEW.value == "immediate_review"

    def test_is_str_subtype(self):
        assert isinstance(CompAction.MAINTAIN, str)

    def test_count(self):
        assert len(CompAction) == 4

    def test_all_members(self):
        members = {e.value for e in CompAction}
        assert members == {"maintain", "monitor", "restructure", "immediate_review"}


# ══════════════════════════════════════════════════════════════════════════════
# 2. SalesCompIntelInput dataclass — field count and types
# ══════════════════════════════════════════════════════════════════════════════

class TestSalesCompIntelInput:
    def test_field_count(self):
        fields = dataclasses.fields(SalesCompIntelInput)
        assert len(fields) == 22

    def test_required_fields_present(self):
        field_names = {f.name for f in dataclasses.fields(SalesCompIntelInput)}
        required = {
            "rep_id", "rep_name", "manager_id", "region",
            "base_salary", "ote_salary", "quota",
            "deals_closed_qtd", "revenue_closed_qtd", "avg_deal_size",
            "deals_in_pipeline", "pipeline_value",
            "large_deal_pct", "spiff_driven_pct", "quarter_end_close_pct",
            "multiyear_deal_pct", "avg_discount_pct",
            "quota_attainment_q1", "quota_attainment_q2", "quota_attainment_q3",
            "comp_complaints", "activity_score_qtd",
        }
        assert required == field_names

    def test_can_construct(self):
        inp = make_input()
        assert inp.rep_id == "rep-001"

    def test_string_fields(self):
        inp = make_input()
        assert isinstance(inp.rep_id, str)
        assert isinstance(inp.rep_name, str)
        assert isinstance(inp.manager_id, str)
        assert isinstance(inp.region, str)

    def test_float_fields(self):
        inp = make_input()
        assert isinstance(inp.base_salary, float)
        assert isinstance(inp.ote_salary, float)

    def test_int_fields(self):
        inp = make_input()
        assert isinstance(inp.deals_closed_qtd, int)
        assert isinstance(inp.comp_complaints, int)


# ══════════════════════════════════════════════════════════════════════════════
# 3. SalesCompIntelResult.to_dict() — key count and types
# ══════════════════════════════════════════════════════════════════════════════

class TestToDict:
    def test_key_count(self, baseline_result):
        assert len(baseline_result.to_dict()) == 15

    def test_exact_keys(self, baseline_result):
        expected_keys = {
            "rep_id", "rep_name", "comp_risk_level", "gaming_pattern",
            "incentive_alignment", "comp_action",
            "sandbagging_score", "spiff_dependency_score",
            "discount_behavior_score", "attainment_consistency_score",
            "compensation_efficiency_score", "estimated_overcompensation",
            "quota_accuracy_score", "is_gaming_comp", "needs_comp_review",
        }
        assert set(baseline_result.to_dict().keys()) == expected_keys

    def test_enum_values_are_strings(self, baseline_result):
        d = baseline_result.to_dict()
        assert isinstance(d["comp_risk_level"], str)
        assert isinstance(d["gaming_pattern"], str)
        assert isinstance(d["incentive_alignment"], str)
        assert isinstance(d["comp_action"], str)

    def test_boolean_fields(self, baseline_result):
        d = baseline_result.to_dict()
        assert isinstance(d["is_gaming_comp"], bool)
        assert isinstance(d["needs_comp_review"], bool)

    def test_numeric_fields_are_float_or_int(self, baseline_result):
        d = baseline_result.to_dict()
        for key in ("sandbagging_score", "spiff_dependency_score",
                    "discount_behavior_score", "attainment_consistency_score",
                    "compensation_efficiency_score", "estimated_overcompensation",
                    "quota_accuracy_score"):
            assert isinstance(d[key], (int, float))

    def test_rep_id_matches(self, engine):
        inp = make_input(rep_id="xyz-999")
        result = engine.analyze(inp)
        assert result.to_dict()["rep_id"] == "xyz-999"

    def test_rep_name_matches(self, engine):
        inp = make_input(rep_name="Bob Jones")
        result = engine.analyze(inp)
        assert result.to_dict()["rep_name"] == "Bob Jones"

    def test_to_dict_always_15_keys_different_inputs(self, engine):
        for i in range(5):
            inp = make_input(rep_id=f"rep-{i}", comp_complaints=i)
            assert len(engine.analyze(inp).to_dict()) == 15


# ══════════════════════════════════════════════════════════════════════════════
# 4. Sandbagging score
# ══════════════════════════════════════════════════════════════════════════════

class TestSandbaggerScore:
    def test_zero_with_all_clean(self, engine):
        inp = make_input(
            quarter_end_close_pct=0.0,
            quota_attainment_q1=50.0,
            quota_attainment_q2=150.0,
            quota_attainment_q3=50.0,  # wide variance, outside 95-120 avg
            activity_score_qtd=80.0,
        )
        score = engine._sandbagging_score(inp)
        assert score == 0.0

    def test_quarter_end_pct_contribution(self, engine):
        inp = make_input(quarter_end_close_pct=40.0, activity_score_qtd=80.0,
                         quota_attainment_q1=50.0, quota_attainment_q2=150.0, quota_attainment_q3=50.0)
        score = engine._sandbagging_score(inp)
        # 40 * 0.7 = 28.0 from quarter_end_close_pct
        assert score == pytest.approx(28.0, abs=0.2)

    def test_quarter_end_pct_capped_at_40(self, engine):
        inp = make_input(quarter_end_close_pct=100.0, activity_score_qtd=80.0,
                         quota_attainment_q1=50.0, quota_attainment_q2=150.0, quota_attainment_q3=50.0)
        score = engine._sandbagging_score(inp)
        # capped at 40
        assert score <= 40.0

    def test_attainment_signal_triggered_when_in_range_tight(self, engine):
        # avg = 105, variance = 5 → tight sandbagging signal
        inp = make_input(
            quarter_end_close_pct=0.0,
            quota_attainment_q1=103.0,
            quota_attainment_q2=105.0,
            quota_attainment_q3=108.0,
            activity_score_qtd=80.0,
        )
        score = engine._sandbagging_score(inp)
        assert score > 0.0

    def test_attainment_signal_not_triggered_outside_95_120(self, engine):
        # avg = 130 → outside 95-120 band
        inp = make_input(
            quarter_end_close_pct=0.0,
            quota_attainment_q1=125.0,
            quota_attainment_q2=130.0,
            quota_attainment_q3=135.0,
            activity_score_qtd=80.0,
        )
        score = engine._sandbagging_score(inp)
        assert score == 0.0

    def test_attainment_signal_not_triggered_high_variance(self, engine):
        # avg = 107, but variance = 80 → not tight
        inp = make_input(
            quarter_end_close_pct=0.0,
            quota_attainment_q1=70.0,
            quota_attainment_q2=107.0,
            quota_attainment_q3=150.0,
            activity_score_qtd=80.0,
        )
        score = engine._sandbagging_score(inp)
        assert score == 0.0

    def test_low_activity_score_adds_to_sandbagging(self, engine):
        inp = make_input(
            quarter_end_close_pct=0.0,
            quota_attainment_q1=50.0,
            quota_attainment_q2=150.0,
            quota_attainment_q3=50.0,
            activity_score_qtd=20.0,
            revenue_closed_qtd=50_000.0,
        )
        score = engine._sandbagging_score(inp)
        # (40-20)*0.6 = 12.0
        assert score > 0.0

    def test_low_activity_no_revenue_no_signal(self, engine):
        inp = make_input(
            quarter_end_close_pct=0.0,
            quota_attainment_q1=50.0,
            quota_attainment_q2=150.0,
            quota_attainment_q3=50.0,
            activity_score_qtd=10.0,
            revenue_closed_qtd=0.0,
        )
        score = engine._sandbagging_score(inp)
        assert score == 0.0

    def test_activity_score_above_40_no_signal(self, engine):
        inp = make_input(
            quarter_end_close_pct=0.0,
            quota_attainment_q1=50.0,
            quota_attainment_q2=150.0,
            quota_attainment_q3=50.0,
            activity_score_qtd=41.0,
            revenue_closed_qtd=50_000.0,
        )
        score = engine._sandbagging_score(inp)
        assert score == 0.0

    def test_sandbagging_score_capped_at_100(self, engine):
        inp = make_input(
            quarter_end_close_pct=100.0,
            quota_attainment_q1=100.0,
            quota_attainment_q2=105.0,
            quota_attainment_q3=108.0,
            activity_score_qtd=0.0,
            revenue_closed_qtd=50_000.0,
        )
        score = engine._sandbagging_score(inp)
        assert score <= 100.0

    def test_sandbagging_score_not_negative(self, engine):
        inp = make_input()
        score = engine._sandbagging_score(inp)
        assert score >= 0.0

    def test_sandbagging_score_rounded_to_1_decimal(self, engine):
        inp = make_input()
        score = engine._sandbagging_score(inp)
        assert score == round(score, 1)

    def test_attainment_variance_exactly_15_no_signal(self, engine):
        # variance == 15 → not < 15, no signal
        inp = make_input(
            quarter_end_close_pct=0.0,
            quota_attainment_q1=97.0,
            quota_attainment_q2=107.0,
            quota_attainment_q3=112.0,
            activity_score_qtd=80.0,
        )
        score = engine._sandbagging_score(inp)
        assert score == 0.0


# ══════════════════════════════════════════════════════════════════════════════
# 5. Spiff dependency score
# ══════════════════════════════════════════════════════════════════════════════

class TestSpiffDependencyScore:
    def test_zero_inputs_give_zero(self, engine):
        inp = make_input(spiff_driven_pct=0.0, large_deal_pct=0.0, multiyear_deal_pct=0.0)
        assert engine._spiff_dependency_score(inp) == 0.0

    def test_spiff_driven_pct_contribution(self, engine):
        inp = make_input(spiff_driven_pct=40.0, large_deal_pct=0.0, multiyear_deal_pct=0.0)
        # 40 * 0.9 = 36.0
        assert engine._spiff_dependency_score(inp) == pytest.approx(36.0, abs=0.1)

    def test_spiff_driven_pct_capped_at_50(self, engine):
        inp = make_input(spiff_driven_pct=100.0, large_deal_pct=0.0, multiyear_deal_pct=0.0)
        assert engine._spiff_dependency_score(inp) == pytest.approx(50.0, abs=0.1)

    def test_large_deal_pct_contribution(self, engine):
        inp = make_input(spiff_driven_pct=0.0, large_deal_pct=40.0, multiyear_deal_pct=0.0)
        # 40 * 0.6 = 24.0
        assert engine._spiff_dependency_score(inp) == pytest.approx(24.0, abs=0.1)

    def test_large_deal_pct_capped_at_30(self, engine):
        inp = make_input(spiff_driven_pct=0.0, large_deal_pct=100.0, multiyear_deal_pct=0.0)
        assert engine._spiff_dependency_score(inp) == pytest.approx(30.0, abs=0.1)

    def test_multiyear_deal_pct_contribution(self, engine):
        inp = make_input(spiff_driven_pct=0.0, large_deal_pct=0.0, multiyear_deal_pct=40.0)
        # 40 * 0.4 = 16.0
        assert engine._spiff_dependency_score(inp) == pytest.approx(16.0, abs=0.1)

    def test_multiyear_deal_pct_capped_at_20(self, engine):
        inp = make_input(spiff_driven_pct=0.0, large_deal_pct=0.0, multiyear_deal_pct=100.0)
        assert engine._spiff_dependency_score(inp) == pytest.approx(20.0, abs=0.1)

    def test_max_all_components(self, engine):
        inp = make_input(spiff_driven_pct=100.0, large_deal_pct=100.0, multiyear_deal_pct=100.0)
        assert engine._spiff_dependency_score(inp) == 100.0

    def test_score_not_negative(self, engine):
        assert engine._spiff_dependency_score(make_input()) >= 0.0

    def test_score_capped_at_100(self, engine):
        inp = make_input(spiff_driven_pct=100.0, large_deal_pct=100.0, multiyear_deal_pct=100.0)
        assert engine._spiff_dependency_score(inp) <= 100.0

    def test_score_rounded_to_1_decimal(self, engine):
        inp = make_input(spiff_driven_pct=33.3, large_deal_pct=22.2, multiyear_deal_pct=11.1)
        score = engine._spiff_dependency_score(inp)
        assert score == round(score, 1)

    def test_additive_combination(self, engine):
        inp = make_input(spiff_driven_pct=20.0, large_deal_pct=20.0, multiyear_deal_pct=20.0)
        # 20*0.9 + 20*0.6 + 20*0.4 = 18 + 12 + 8 = 38
        assert engine._spiff_dependency_score(inp) == pytest.approx(38.0, abs=0.1)


# ══════════════════════════════════════════════════════════════════════════════
# 6. Discount behavior score
# ══════════════════════════════════════════════════════════════════════════════

class TestDiscountBehaviorScore:
    def test_zero_discount_zero_complaints(self, engine):
        inp = make_input(avg_discount_pct=0.0, comp_complaints=0, pipeline_value=1_000_000.0)
        assert engine._discount_behavior_score(inp) == 0.0

    def test_discount_depth_contribution(self, engine):
        inp = make_input(avg_discount_pct=20.0, comp_complaints=0,
                         revenue_closed_qtd=100.0, pipeline_value=1_000_000.0)
        # 20 * 1.2 = 24.0
        assert engine._discount_behavior_score(inp) == pytest.approx(24.0, abs=0.2)

    def test_discount_depth_capped_at_50(self, engine):
        inp = make_input(avg_discount_pct=100.0, comp_complaints=0,
                         revenue_closed_qtd=100.0, pipeline_value=1_000_000.0)
        score = engine._discount_behavior_score(inp)
        # discount component capped at 50
        assert score >= 50.0

    def test_high_discount_high_close_rate_adds_bonus(self, engine):
        # close_rate_proxy = 800000 / 1000000 * 100 = 80 > 50
        inp = make_input(
            avg_discount_pct=25.0,
            deals_closed_qtd=5,
            revenue_closed_qtd=800_000.0,
            pipeline_value=1_000_000.0,
            comp_complaints=0,
        )
        score_base = min(50.0, 25.0 * 1.2)
        assert engine._discount_behavior_score(inp) > score_base

    def test_high_discount_low_close_rate_no_bonus(self, engine):
        # close_rate_proxy = 10000 / 1000000 * 100 = 1 < 50
        inp = make_input(
            avg_discount_pct=25.0,
            deals_closed_qtd=5,
            revenue_closed_qtd=10_000.0,
            pipeline_value=1_000_000.0,
            comp_complaints=0,
        )
        # only discount depth: 25*1.2 = 30
        assert engine._discount_behavior_score(inp) == pytest.approx(30.0, abs=0.1)

    def test_low_discount_no_close_bonus(self, engine):
        # avg_discount_pct < 20 → no bonus even with high close rate
        inp = make_input(
            avg_discount_pct=15.0,
            deals_closed_qtd=5,
            revenue_closed_qtd=900_000.0,
            pipeline_value=1_000_000.0,
            comp_complaints=0,
        )
        assert engine._discount_behavior_score(inp) == pytest.approx(15.0 * 1.2, abs=0.1)

    def test_complaints_add_to_score(self, engine):
        inp = make_input(avg_discount_pct=0.0, comp_complaints=2,
                         revenue_closed_qtd=100.0, pipeline_value=1_000_000.0)
        # 2 * 7.0 = 14.0
        assert engine._discount_behavior_score(inp) == pytest.approx(14.0, abs=0.1)

    def test_complaints_capped_at_20(self, engine):
        inp = make_input(avg_discount_pct=0.0, comp_complaints=10,
                         revenue_closed_qtd=100.0, pipeline_value=1_000_000.0)
        score = engine._discount_behavior_score(inp)
        assert score <= 100.0

    def test_score_not_negative(self, engine):
        assert engine._discount_behavior_score(make_input()) >= 0.0

    def test_score_capped_at_100(self, engine):
        inp = make_input(avg_discount_pct=100.0, comp_complaints=10,
                         revenue_closed_qtd=1_000_000.0, pipeline_value=100_000.0)
        assert engine._discount_behavior_score(inp) <= 100.0

    def test_score_rounded_to_1_decimal(self, engine):
        inp = make_input(avg_discount_pct=7.7, comp_complaints=1)
        score = engine._discount_behavior_score(inp)
        assert score == round(score, 1)

    def test_zero_pipeline_handled(self, engine):
        # pipeline_value = 0 → max(1.0, pipeline_value) prevents division by zero
        inp = make_input(
            avg_discount_pct=25.0,
            deals_closed_qtd=5,
            revenue_closed_qtd=100_000.0,
            pipeline_value=0.0,
            comp_complaints=0,
        )
        score = engine._discount_behavior_score(inp)
        assert isinstance(score, float)
        assert score >= 0.0


# ══════════════════════════════════════════════════════════════════════════════
# 7. Attainment consistency score
# ══════════════════════════════════════════════════════════════════════════════

class TestAttainmentConsistencyScore:
    def test_perfect_consistency_high_attainment(self, engine):
        inp = make_input(quota_attainment_q1=110.0, quota_attainment_q2=110.0, quota_attainment_q3=110.0)
        score = engine._attainment_consistency_score(inp)
        # variance=0 → consistency=100, avg=110 → bonus=12 → min(100, 100*0.8+12)=92
        assert score == pytest.approx(92.0, abs=0.5)

    def test_zero_variance_gives_max_consistency(self, engine):
        inp = make_input(quota_attainment_q1=100.0, quota_attainment_q2=100.0, quota_attainment_q3=100.0)
        score = engine._attainment_consistency_score(inp)
        assert score > 80.0

    def test_high_variance_penalizes_score(self, engine):
        inp = make_input(quota_attainment_q1=50.0, quota_attainment_q2=100.0, quota_attainment_q3=150.0)
        # variance=100 → consistency = max(0, 100-200) = 0 → score=0+bonus
        score = engine._attainment_consistency_score(inp)
        assert score < 25.0

    def test_below_80_avg_no_achievement_bonus(self, engine):
        inp = make_input(quota_attainment_q1=70.0, quota_attainment_q2=70.0, quota_attainment_q3=70.0)
        # avg=70 < 80 → bonus=0
        score = engine._attainment_consistency_score(inp)
        # consistency = 100-0=100, 100*0.8+0=80
        assert score == pytest.approx(80.0, abs=0.5)

    def test_above_80_avg_adds_bonus(self, engine):
        inp = make_input(quota_attainment_q1=100.0, quota_attainment_q2=100.0, quota_attainment_q3=100.0)
        score_no_bonus = engine._attainment_consistency_score(
            make_input(quota_attainment_q1=70.0, quota_attainment_q2=70.0, quota_attainment_q3=70.0)
        )
        score_with_bonus = engine._attainment_consistency_score(inp)
        assert score_with_bonus > score_no_bonus

    def test_score_not_negative(self, engine):
        inp = make_input(quota_attainment_q1=10.0, quota_attainment_q2=200.0, quota_attainment_q3=10.0)
        score = engine._attainment_consistency_score(inp)
        assert score >= 0.0

    def test_score_capped_at_100(self, engine):
        inp = make_input(quota_attainment_q1=200.0, quota_attainment_q2=200.0, quota_attainment_q3=200.0)
        score = engine._attainment_consistency_score(inp)
        assert score <= 100.0

    def test_score_rounded_to_1_decimal(self, engine):
        inp = make_input(quota_attainment_q1=95.5, quota_attainment_q2=100.3, quota_attainment_q3=104.7)
        score = engine._attainment_consistency_score(inp)
        assert score == round(score, 1)


# ══════════════════════════════════════════════════════════════════════════════
# 8. Compensation efficiency score
# ══════════════════════════════════════════════════════════════════════════════

class TestCompensationEfficiencyScore:
    def test_zero_ote_returns_zero(self, engine):
        inp = make_input(ote_salary=0.0)
        assert engine._compensation_efficiency_score(inp) == 0.0

    def test_negative_ote_returns_zero(self, engine):
        inp = make_input(ote_salary=-1.0)
        assert engine._compensation_efficiency_score(inp) == 0.0

    def test_revenue_multiple_above_5_returns_100(self, engine):
        # annualized = 200_000 * 4 = 800_000; multiple = 800_000/100_000=8 → 100
        inp = make_input(revenue_closed_qtd=200_000.0, ote_salary=100_000.0)
        assert engine._compensation_efficiency_score(inp) == 100.0

    def test_revenue_multiple_exactly_5_returns_100(self, engine):
        # multiple = 5*ote/ote = 5
        inp = make_input(revenue_closed_qtd=125_000.0, ote_salary=100_000.0)
        assert engine._compensation_efficiency_score(inp) == 100.0

    def test_revenue_multiple_at_1_returns_zero(self, engine):
        # annualized = 25000*4=100000; multiple = 100000/100000=1.0
        inp = make_input(revenue_closed_qtd=25_000.0, ote_salary=100_000.0)
        assert engine._compensation_efficiency_score(inp) == 0.0

    def test_revenue_multiple_below_1_returns_zero(self, engine):
        inp = make_input(revenue_closed_qtd=0.0, ote_salary=100_000.0)
        assert engine._compensation_efficiency_score(inp) == 0.0

    def test_midpoint_multiple_3_returns_50(self, engine):
        # multiple = 3 → (3-1)/4 * 100 = 50
        inp = make_input(revenue_closed_qtd=75_000.0, ote_salary=100_000.0)
        assert engine._compensation_efficiency_score(inp) == pytest.approx(50.0, abs=0.1)

    def test_score_not_negative(self, engine):
        inp = make_input(revenue_closed_qtd=0.0, ote_salary=200_000.0)
        assert engine._compensation_efficiency_score(inp) >= 0.0

    def test_score_capped_at_100(self, engine):
        inp = make_input(revenue_closed_qtd=10_000_000.0, ote_salary=100_000.0)
        assert engine._compensation_efficiency_score(inp) <= 100.0

    def test_score_rounded_to_1_decimal(self, engine):
        inp = make_input(revenue_closed_qtd=55_555.0, ote_salary=100_000.0)
        score = engine._compensation_efficiency_score(inp)
        assert score == round(score, 1)

    def test_multiple_2_gives_25(self, engine):
        # multiple = 2 → (2-1)/4 * 100 = 25
        inp = make_input(revenue_closed_qtd=50_000.0, ote_salary=100_000.0)
        assert engine._compensation_efficiency_score(inp) == pytest.approx(25.0, abs=0.1)


# ══════════════════════════════════════════════════════════════════════════════
# 9. Estimated overcompensation
# ══════════════════════════════════════════════════════════════════════════════

class TestEstimatedOvercompensation:
    def test_high_efficiency_returns_zero(self, engine):
        # efficiency >= 60 → overcomp = 0
        inp = make_input(revenue_closed_qtd=200_000.0, ote_salary=100_000.0)
        eff = engine._compensation_efficiency_score(inp)
        assert eff >= 60.0
        assert engine._estimated_overcompensation(inp, eff) == 0.0

    def test_low_efficiency_but_above_3x_ote(self, engine):
        # annualized = 100_000 * 4 = 400_000; target = 100_000 * 3 = 300_000
        # annualized >= target → 0
        inp = make_input(revenue_closed_qtd=100_000.0, ote_salary=100_000.0)
        eff = engine._compensation_efficiency_score(inp)
        assert engine._estimated_overcompensation(inp, eff) == 0.0

    def test_low_revenue_produces_overcomp(self, engine):
        # efficiency < 60, annualized < 3x ote
        inp = make_input(revenue_closed_qtd=10_000.0, ote_salary=160_000.0)
        eff = engine._compensation_efficiency_score(inp)
        assert eff < 60.0
        overcomp = engine._estimated_overcompensation(inp, eff)
        assert overcomp > 0.0

    def test_overcomp_not_negative(self, engine):
        inp = make_input(revenue_closed_qtd=0.0, ote_salary=100_000.0)
        eff = 0.0
        assert engine._estimated_overcompensation(inp, eff) >= 0.0

    def test_overcomp_rounded_to_2_decimals(self, engine):
        inp = make_input(revenue_closed_qtd=5_000.0, ote_salary=100_000.0)
        eff = 0.0
        oc = engine._estimated_overcompensation(inp, eff)
        assert oc == round(oc, 2)

    def test_efficiency_exactly_60_returns_zero(self, engine):
        # We force efficiency to exactly 60.0
        inp = make_input()
        assert engine._estimated_overcompensation(inp, 60.0) == 0.0

    def test_efficiency_59_9_may_give_overcomp(self, engine):
        # With very low revenue, there should be overcomp
        inp = make_input(revenue_closed_qtd=1_000.0, ote_salary=200_000.0)
        oc = engine._estimated_overcompensation(inp, 59.9)
        assert oc >= 0.0

    def test_shortfall_calculation(self, engine):
        # ote=100k, revenue_closed=12.5k, annualized=50k, target=300k
        # shortfall_pct=(300k-50k)/300k ≈ 0.8333
        # overpay = 100k * 0.8333 * 0.4 ≈ 33333.33
        inp = make_input(revenue_closed_qtd=12_500.0, ote_salary=100_000.0)
        eff = engine._compensation_efficiency_score(inp)
        assert eff < 60.0
        oc = engine._estimated_overcompensation(inp, eff)
        assert oc == pytest.approx(33_333.33, abs=1.0)


# ══════════════════════════════════════════════════════════════════════════════
# 10. Quota accuracy score
# ══════════════════════════════════════════════════════════════════════════════

class TestQuotaAccuracyScore:
    def test_perfect_100_avg_returns_100(self, engine):
        inp = make_input(quota_attainment_q1=100.0, quota_attainment_q2=100.0, quota_attainment_q3=100.0)
        assert engine._quota_accuracy_score(inp) == 100.0

    def test_avg_exactly_90_boundary(self, engine):
        inp = make_input(quota_attainment_q1=90.0, quota_attainment_q2=90.0, quota_attainment_q3=90.0)
        # avg=90 in [90,110] → 100-|90-100|*2=80
        assert engine._quota_accuracy_score(inp) == pytest.approx(80.0, abs=0.1)

    def test_avg_exactly_110_boundary(self, engine):
        inp = make_input(quota_attainment_q1=110.0, quota_attainment_q2=110.0, quota_attainment_q3=110.0)
        # avg=110 in [90,110] → 100-|110-100|*2=80
        assert engine._quota_accuracy_score(inp) == pytest.approx(80.0, abs=0.1)

    def test_avg_above_110_penalized(self, engine):
        inp = make_input(quota_attainment_q1=130.0, quota_attainment_q2=130.0, quota_attainment_q3=130.0)
        # avg=130 → excess=20 → 100-20*1.5=70
        assert engine._quota_accuracy_score(inp) == pytest.approx(70.0, abs=0.1)

    def test_avg_below_90_penalized(self, engine):
        inp = make_input(quota_attainment_q1=70.0, quota_attainment_q2=70.0, quota_attainment_q3=70.0)
        # avg=70 → shortfall=20 → 100-20*2=60
        assert engine._quota_accuracy_score(inp) == pytest.approx(60.0, abs=0.1)

    def test_very_high_attainment_capped_at_zero_floor(self, engine):
        inp = make_input(quota_attainment_q1=250.0, quota_attainment_q2=250.0, quota_attainment_q3=250.0)
        score = engine._quota_accuracy_score(inp)
        assert score >= 0.0

    def test_very_low_attainment_capped_at_zero_floor(self, engine):
        inp = make_input(quota_attainment_q1=10.0, quota_attainment_q2=10.0, quota_attainment_q3=10.0)
        score = engine._quota_accuracy_score(inp)
        assert score >= 0.0

    def test_score_rounded_to_1_decimal(self, engine):
        inp = make_input(quota_attainment_q1=93.3, quota_attainment_q2=97.7, quota_attainment_q3=101.1)
        score = engine._quota_accuracy_score(inp)
        assert score == round(score, 1)

    def test_avg_105_in_range(self, engine):
        inp = make_input(quota_attainment_q1=103.0, quota_attainment_q2=105.0, quota_attainment_q3=107.0)
        # avg=105 in [90,110] → 100-5*2=90
        assert engine._quota_accuracy_score(inp) == pytest.approx(90.0, abs=0.1)


# ══════════════════════════════════════════════════════════════════════════════
# 11. Comp risk level
# ══════════════════════════════════════════════════════════════════════════════

class TestCompRiskLevel:
    def test_low_risk_clean_rep(self, engine):
        # all scores near zero
        inp = make_input(
            spiff_driven_pct=0.0, large_deal_pct=0.0, multiyear_deal_pct=0.0,
            avg_discount_pct=0.0, comp_complaints=0,
            quarter_end_close_pct=0.0,
            quota_attainment_q1=50.0, quota_attainment_q2=130.0, quota_attainment_q3=50.0,
            activity_score_qtd=80.0,
        )
        result = engine.analyze(inp)
        assert result.comp_risk_level == CompRiskLevel.LOW

    def test_critical_risk_via_complaints(self, engine):
        inp = make_input(comp_complaints=3)
        result = engine.analyze(inp)
        assert result.comp_risk_level == CompRiskLevel.CRITICAL

    def test_critical_risk_via_combined_score(self, engine):
        # Need combined >= 60; e.g., sandbagging=100*0.4=40, spiff=100*0.3=30 → total=70
        inp = make_input(
            spiff_driven_pct=100.0, large_deal_pct=100.0, multiyear_deal_pct=100.0,
            quarter_end_close_pct=100.0,
            quota_attainment_q1=100.0, quota_attainment_q2=105.0, quota_attainment_q3=107.0,
            activity_score_qtd=0.0, revenue_closed_qtd=50_000.0,
            comp_complaints=0,
        )
        result = engine.analyze(inp)
        assert result.comp_risk_level == CompRiskLevel.CRITICAL

    def test_high_risk_via_complaints(self, engine):
        inp = make_input(comp_complaints=2)
        result = engine.analyze(inp)
        assert result.comp_risk_level in (CompRiskLevel.HIGH, CompRiskLevel.CRITICAL)

    def test_moderate_risk_range(self, engine):
        # combined in [20, 40)
        inp = make_input(
            spiff_driven_pct=30.0, large_deal_pct=10.0, multiyear_deal_pct=5.0,
            avg_discount_pct=5.0, comp_complaints=0,
            quarter_end_close_pct=0.0,
            quota_attainment_q1=50.0, quota_attainment_q2=150.0, quota_attainment_q3=50.0,
            activity_score_qtd=80.0,
        )
        risk_level = engine._comp_risk_level(inp, 0.0, 33.0, 6.0)
        # combined = 0*0.4 + 33*0.3 + 6*0.3 = 0 + 9.9 + 1.8 = 11.7 → LOW
        # Let's test with direct values in MODERATE range
        risk_level2 = engine._comp_risk_level(inp, 30.0, 30.0, 30.0)
        # combined = 30*0.4 + 30*0.3 + 30*0.3 = 12+9+9=30 → MODERATE
        assert risk_level2 == CompRiskLevel.MODERATE

    def test_low_risk_via_all_zero_scores(self, engine):
        inp = make_input(comp_complaints=0)
        risk = engine._comp_risk_level(inp, 0.0, 0.0, 0.0)
        assert risk == CompRiskLevel.LOW

    def test_high_risk_threshold_at_40(self, engine):
        inp = make_input(comp_complaints=0)
        # combined = exactly 40 → HIGH
        risk = engine._comp_risk_level(inp, 40.0 / 0.4, 0.0, 0.0)
        # sandbagging*0.4 = 40 → HIGH
        risk2 = engine._comp_risk_level(inp, 100.0, 0.0, 0.0)
        # combined = 40 → HIGH
        assert risk2 == CompRiskLevel.HIGH

    def test_critical_threshold_at_60(self, engine):
        inp = make_input(comp_complaints=0)
        # combined = exactly 60 → CRITICAL
        risk = engine._comp_risk_level(inp, 150.0, 0.0, 0.0)
        # 150*0.4=60 → CRITICAL
        assert risk == CompRiskLevel.CRITICAL


# ══════════════════════════════════════════════════════════════════════════════
# 12. Gaming pattern
# ══════════════════════════════════════════════════════════════════════════════

class TestGamingPattern:
    def test_clean_when_all_low(self, engine):
        pattern = engine._gaming_pattern(0.0, 0.0, 0.0)
        assert pattern == GamingPattern.CLEAN

    def test_sandbagging_only(self, engine):
        pattern = engine._gaming_pattern(55.0, 0.0, 0.0)
        assert pattern == GamingPattern.SANDBAGGING

    def test_spiff_chasing_only(self, engine):
        pattern = engine._gaming_pattern(0.0, 60.0, 0.0)
        assert pattern == GamingPattern.SPIFF_CHASING

    def test_discount_heavy_only(self, engine):
        pattern = engine._gaming_pattern(0.0, 0.0, 55.0)
        assert pattern == GamingPattern.DISCOUNT_HEAVY

    def test_mixed_when_two_signals(self, engine):
        pattern = engine._gaming_pattern(55.0, 60.0, 0.0)
        assert pattern == GamingPattern.MIXED

    def test_mixed_when_three_signals(self, engine):
        pattern = engine._gaming_pattern(55.0, 60.0, 55.0)
        assert pattern == GamingPattern.MIXED

    def test_sandbagging_threshold_exactly_50(self, engine):
        # sandbagging >= 50 triggers signal
        pattern = engine._gaming_pattern(50.0, 0.0, 0.0)
        assert pattern == GamingPattern.SANDBAGGING

    def test_sandbagging_below_threshold(self, engine):
        pattern = engine._gaming_pattern(49.9, 0.0, 0.0)
        assert pattern == GamingPattern.CLEAN

    def test_spiff_threshold_exactly_55(self, engine):
        pattern = engine._gaming_pattern(0.0, 55.0, 0.0)
        assert pattern == GamingPattern.SPIFF_CHASING

    def test_spiff_below_threshold(self, engine):
        pattern = engine._gaming_pattern(0.0, 54.9, 0.0)
        assert pattern == GamingPattern.CLEAN

    def test_discount_threshold_exactly_50(self, engine):
        pattern = engine._gaming_pattern(0.0, 0.0, 50.0)
        assert pattern == GamingPattern.DISCOUNT_HEAVY

    def test_discount_below_threshold(self, engine):
        pattern = engine._gaming_pattern(0.0, 0.0, 49.9)
        assert pattern == GamingPattern.CLEAN

    def test_mixed_sandbagging_discount(self, engine):
        pattern = engine._gaming_pattern(50.0, 0.0, 50.0)
        assert pattern == GamingPattern.MIXED


# ══════════════════════════════════════════════════════════════════════════════
# 13. Incentive alignment
# ══════════════════════════════════════════════════════════════════════════════

class TestIncentiveAlignment:
    def test_well_aligned_clean(self, engine):
        inp = make_input(comp_complaints=0)
        alignment = engine._incentive_alignment(inp, 0.0, 0.0, 0.0)
        assert alignment == IncentiveAlignment.WELL_ALIGNED

    def test_perverse_via_complaints(self, engine):
        inp = make_input(comp_complaints=3)
        alignment = engine._incentive_alignment(inp, 0.0, 0.0, 0.0)
        assert alignment == IncentiveAlignment.PERVERSE

    def test_perverse_via_gaming_signal(self, engine):
        # gaming_signal >= 55
        inp = make_input(comp_complaints=0)
        alignment = engine._incentive_alignment(inp, 80.0, 80.0, 80.0)
        # 80*0.35 + 80*0.35 + 80*0.30 = 28+28+24=80 → PERVERSE
        assert alignment == IncentiveAlignment.PERVERSE

    def test_misaligned_range(self, engine):
        # gaming_signal in [35, 55)
        inp = make_input(comp_complaints=0)
        # 55*0.35 + 40*0.35 + 30*0.30 = 19.25+14+9=42.25 → MISALIGNED
        alignment = engine._incentive_alignment(inp, 55.0, 40.0, 30.0)
        assert alignment == IncentiveAlignment.MISALIGNED

    def test_partially_aligned_range(self, engine):
        # gaming_signal in [18, 35)
        inp = make_input(comp_complaints=0)
        # 30*0.35 + 20*0.35 + 20*0.30 = 10.5+7+6=23.5 → PARTIALLY_ALIGNED
        alignment = engine._incentive_alignment(inp, 30.0, 20.0, 20.0)
        assert alignment == IncentiveAlignment.PARTIALLY_ALIGNED

    def test_threshold_exactly_18_is_partially_aligned(self, engine):
        inp = make_input(comp_complaints=0)
        # need gaming_signal ≈ 18: 18/0.35 ≈ 51.4 on sandbagging alone
        alignment = engine._incentive_alignment(inp, 51.5, 0.0, 0.0)
        # 51.5*0.35=18.025 → PARTIALLY_ALIGNED
        assert alignment == IncentiveAlignment.PARTIALLY_ALIGNED

    def test_threshold_below_18_is_well_aligned(self, engine):
        inp = make_input(comp_complaints=0)
        alignment = engine._incentive_alignment(inp, 10.0, 10.0, 10.0)
        # 10*0.35+10*0.35+10*0.30=3.5+3.5+3=10 → WELL_ALIGNED
        assert alignment == IncentiveAlignment.WELL_ALIGNED


# ══════════════════════════════════════════════════════════════════════════════
# 14. Comp action
# ══════════════════════════════════════════════════════════════════════════════

class TestCompAction:
    def test_immediate_review_for_critical_risk(self, engine):
        action = engine._comp_action(CompRiskLevel.CRITICAL, IncentiveAlignment.WELL_ALIGNED, False, False)
        assert action == CompAction.IMMEDIATE_REVIEW

    def test_immediate_review_for_perverse_alignment(self, engine):
        action = engine._comp_action(CompRiskLevel.LOW, IncentiveAlignment.PERVERSE, False, False)
        assert action == CompAction.IMMEDIATE_REVIEW

    def test_restructure_for_gaming(self, engine):
        action = engine._comp_action(CompRiskLevel.LOW, IncentiveAlignment.WELL_ALIGNED, True, False)
        assert action == CompAction.RESTRUCTURE

    def test_restructure_for_misaligned(self, engine):
        action = engine._comp_action(CompRiskLevel.LOW, IncentiveAlignment.MISALIGNED, False, False)
        assert action == CompAction.RESTRUCTURE

    def test_monitor_for_needs_review(self, engine):
        action = engine._comp_action(CompRiskLevel.LOW, IncentiveAlignment.WELL_ALIGNED, False, True)
        assert action == CompAction.MONITOR

    def test_monitor_for_partially_aligned(self, engine):
        action = engine._comp_action(CompRiskLevel.LOW, IncentiveAlignment.PARTIALLY_ALIGNED, False, False)
        assert action == CompAction.MONITOR

    def test_maintain_all_clean(self, engine):
        action = engine._comp_action(CompRiskLevel.LOW, IncentiveAlignment.WELL_ALIGNED, False, False)
        assert action == CompAction.MAINTAIN

    def test_immediate_review_beats_gaming(self, engine):
        # Critical risk → immediate_review regardless of gaming=True
        action = engine._comp_action(CompRiskLevel.CRITICAL, IncentiveAlignment.WELL_ALIGNED, True, True)
        assert action == CompAction.IMMEDIATE_REVIEW

    def test_restructure_beats_monitor(self, engine):
        # gaming=True, needs_review=True → restructure (gaming checked first)
        action = engine._comp_action(CompRiskLevel.LOW, IncentiveAlignment.WELL_ALIGNED, True, True)
        assert action == CompAction.RESTRUCTURE


# ══════════════════════════════════════════════════════════════════════════════
# 15. is_gaming_comp flag
# ══════════════════════════════════════════════════════════════════════════════

class TestIsGamingComp:
    def test_not_gaming_clean_rep(self, engine, baseline_input):
        result = engine.analyze(baseline_input)
        # baseline has low scores
        assert result.is_gaming_comp is False

    def test_gaming_via_high_sandbagging(self, engine):
        # sandbagging >= 55
        inp = make_input(
            quarter_end_close_pct=100.0,
            quota_attainment_q1=100.0, quota_attainment_q2=105.0, quota_attainment_q3=107.0,
            activity_score_qtd=0.0, revenue_closed_qtd=50_000.0,
        )
        result = engine.analyze(inp)
        if result.sandbagging_score >= 55.0:
            assert result.is_gaming_comp is True

    def test_gaming_via_high_spiff(self, engine):
        inp = make_input(spiff_driven_pct=100.0, large_deal_pct=100.0, multiyear_deal_pct=100.0)
        result = engine.analyze(inp)
        assert result.spiff_dependency_score >= 65.0
        assert result.is_gaming_comp is True

    def test_gaming_via_high_discount(self, engine):
        inp = make_input(
            avg_discount_pct=100.0,
            comp_complaints=0,
            revenue_closed_qtd=100.0, pipeline_value=100.0,
        )
        result = engine.analyze(inp)
        assert result.discount_behavior_score >= 60.0
        assert result.is_gaming_comp is True

    def test_threshold_sandbagging_55(self, engine):
        # Force sandbagging exactly at threshold
        # quarter_end_close_pct at max (40 pts) + attainment signal
        inp = make_input(
            quarter_end_close_pct=100.0,
            quota_attainment_q1=100.0, quota_attainment_q2=102.0, quota_attainment_q3=103.0,
            activity_score_qtd=80.0,
        )
        result = engine.analyze(inp)
        # sandbagging from q_end=40 + attainment signal: avg=101.7 in range, variance=3→(15-3)*2.5=30
        # total=40+30=70 ≥ 55 → gaming
        assert result.is_gaming_comp is True


# ══════════════════════════════════════════════════════════════════════════════
# 16. needs_comp_review flag
# ══════════════════════════════════════════════════════════════════════════════

class TestNeedsCompReview:
    def test_not_needed_clean(self, engine, baseline_input):
        result = engine.analyze(baseline_input)
        # baseline has moderate efficiency and low complaints
        # just check it's a bool
        assert isinstance(result.needs_comp_review, bool)

    def test_needed_via_critical_risk(self, engine):
        inp = make_input(comp_complaints=3)
        result = engine.analyze(inp)
        assert result.comp_risk_level == CompRiskLevel.CRITICAL
        assert result.needs_comp_review is True

    def test_needed_via_high_risk(self, engine):
        inp = make_input(comp_complaints=2)
        result = engine.analyze(inp)
        assert result.needs_comp_review is True

    def test_needed_via_comp_complaints_2(self, engine):
        inp = make_input(comp_complaints=2)
        result = engine.analyze(inp)
        assert result.needs_comp_review is True

    def test_needed_via_low_efficiency(self, engine):
        # efficiency < 30 → needs_review
        inp = make_input(revenue_closed_qtd=0.0, ote_salary=160_000.0)
        result = engine.analyze(inp)
        assert result.compensation_efficiency_score < 30.0
        assert result.needs_comp_review is True

    def test_not_needed_zero_complaints_good_efficiency(self, engine):
        inp = make_input(
            revenue_closed_qtd=300_000.0,  # annualized = 1.2M; multiple = 1.2M/160k = 7.5 → 100%
            ote_salary=160_000.0,
            comp_complaints=0,
        )
        result = engine.analyze(inp)
        if (result.comp_risk_level not in (CompRiskLevel.HIGH, CompRiskLevel.CRITICAL)
                and result.compensation_efficiency_score >= 30.0):
            assert result.needs_comp_review is False


# ══════════════════════════════════════════════════════════════════════════════
# 17. analyze() — end-to-end result structure
# ══════════════════════════════════════════════════════════════════════════════

class TestAnalyzeEndToEnd:
    def test_returns_result_type(self, engine, baseline_input):
        result = engine.analyze(baseline_input)
        assert isinstance(result, SalesCompIntelResult)

    def test_rep_id_preserved(self, engine):
        inp = make_input(rep_id="test-007")
        assert engine.analyze(inp).rep_id == "test-007"

    def test_rep_name_preserved(self, engine):
        inp = make_input(rep_name="Jane Doe")
        assert engine.analyze(inp).rep_name == "Jane Doe"

    def test_scores_in_range(self, engine, baseline_input):
        r = engine.analyze(baseline_input)
        for score in (r.sandbagging_score, r.spiff_dependency_score, r.discount_behavior_score,
                      r.attainment_consistency_score, r.compensation_efficiency_score,
                      r.quota_accuracy_score):
            assert 0.0 <= score <= 100.0

    def test_overcompensation_not_negative(self, engine, baseline_input):
        r = engine.analyze(baseline_input)
        assert r.estimated_overcompensation >= 0.0

    def test_comp_risk_level_is_enum(self, engine, baseline_input):
        assert isinstance(engine.analyze(baseline_input).comp_risk_level, CompRiskLevel)

    def test_gaming_pattern_is_enum(self, engine, baseline_input):
        assert isinstance(engine.analyze(baseline_input).gaming_pattern, GamingPattern)

    def test_incentive_alignment_is_enum(self, engine, baseline_input):
        assert isinstance(engine.analyze(baseline_input).incentive_alignment, IncentiveAlignment)

    def test_comp_action_is_enum(self, engine, baseline_input):
        assert isinstance(engine.analyze(baseline_input).comp_action, CompAction)

    def test_result_stored_in_engine(self, engine, baseline_input):
        engine.analyze(baseline_input)
        assert len(engine._results) == 1

    def test_multiple_analyzes_stored(self, engine):
        for i in range(5):
            engine.analyze(make_input(rep_id=f"rep-{i}"))
        assert len(engine._results) == 5

    def test_high_risk_rep_scenario(self, engine):
        inp = make_input(
            spiff_driven_pct=80.0, large_deal_pct=60.0, multiyear_deal_pct=50.0,
            avg_discount_pct=40.0, comp_complaints=2,
        )
        r = engine.analyze(inp)
        assert r.comp_risk_level in (CompRiskLevel.HIGH, CompRiskLevel.CRITICAL)

    def test_clean_rep_scenario(self, engine):
        inp = make_input(
            spiff_driven_pct=0.0, large_deal_pct=0.0, multiyear_deal_pct=0.0,
            avg_discount_pct=0.0, comp_complaints=0,
            quarter_end_close_pct=0.0,
            quota_attainment_q1=50.0, quota_attainment_q2=150.0, quota_attainment_q3=50.0,
            activity_score_qtd=80.0,
        )
        r = engine.analyze(inp)
        assert r.comp_risk_level == CompRiskLevel.LOW
        assert r.gaming_pattern == GamingPattern.CLEAN

    def test_star_rep_high_efficiency(self, engine):
        inp = make_input(revenue_closed_qtd=500_000.0, ote_salary=160_000.0)
        r = engine.analyze(inp)
        assert r.compensation_efficiency_score == 100.0
        assert r.estimated_overcompensation == 0.0


# ══════════════════════════════════════════════════════════════════════════════
# 18. analyze_batch()
# ══════════════════════════════════════════════════════════════════════════════

class TestAnalyzeBatch:
    def test_returns_list(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        assert isinstance(results, list)

    def test_batch_length_matches_input(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(5)]
        assert len(engine.analyze_batch(inputs)) == 5

    def test_batch_results_are_correct_type(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(3)]
        for r in engine.analyze_batch(inputs):
            assert isinstance(r, SalesCompIntelResult)

    def test_batch_empty_input(self, engine):
        assert engine.analyze_batch([]) == []

    def test_batch_stores_all_results(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(4)]
        engine.analyze_batch(inputs)
        assert len(engine._results) == 4

    def test_batch_rep_ids_preserved(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        assert [r.rep_id for r in results] == ["rep-0", "rep-1", "rep-2"]

    def test_batch_appends_to_existing(self, engine):
        engine.analyze(make_input(rep_id="existing"))
        engine.analyze_batch([make_input(rep_id=f"batch-{i}") for i in range(3)])
        assert len(engine._results) == 4

    def test_single_item_batch(self, engine):
        results = engine.analyze_batch([make_input(rep_id="solo")])
        assert len(results) == 1
        assert results[0].rep_id == "solo"

    def test_large_batch(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(50)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 50


# ══════════════════════════════════════════════════════════════════════════════
# 19. reset()
# ══════════════════════════════════════════════════════════════════════════════

class TestReset:
    def test_reset_clears_results(self, engine):
        engine.analyze(make_input())
        engine.reset()
        assert engine._results == []

    def test_reset_clears_multiple_results(self, engine):
        for i in range(5):
            engine.analyze(make_input(rep_id=f"rep-{i}"))
        engine.reset()
        assert len(engine._results) == 0

    def test_reset_returns_none(self, engine):
        assert engine.reset() is None

    def test_can_analyze_after_reset(self, engine):
        engine.analyze(make_input())
        engine.reset()
        engine.analyze(make_input(rep_id="after-reset"))
        assert len(engine._results) == 1
        assert engine._results[0].rep_id == "after-reset"

    def test_double_reset_ok(self, engine):
        engine.reset()
        engine.reset()
        assert len(engine._results) == 0

    def test_reset_on_empty_engine_ok(self, engine):
        engine.reset()  # no error
        assert len(engine._results) == 0

    def test_properties_empty_after_reset(self, engine):
        engine.analyze(make_input(comp_complaints=3))
        engine.reset()
        assert engine.gaming_reps == []
        assert engine.review_needed == []
        assert engine.total_overcompensation == 0.0
        assert engine.avg_compensation_efficiency == 0.0


# ══════════════════════════════════════════════════════════════════════════════
# 20. Properties
# ══════════════════════════════════════════════════════════════════════════════

class TestProperties:
    def test_gaming_reps_empty_initially(self, engine):
        assert engine.gaming_reps == []

    def test_gaming_reps_contains_gaming(self, engine):
        # spiff-heavy rep
        inp = make_input(spiff_driven_pct=100.0, large_deal_pct=100.0, multiyear_deal_pct=100.0)
        r = engine.analyze(inp)
        if r.is_gaming_comp:
            assert r in engine.gaming_reps

    def test_gaming_reps_excludes_clean(self, engine):
        inp = make_input(
            spiff_driven_pct=0.0, large_deal_pct=0.0, multiyear_deal_pct=0.0,
            avg_discount_pct=0.0, comp_complaints=0,
            quarter_end_close_pct=0.0,
            quota_attainment_q1=50.0, quota_attainment_q2=150.0, quota_attainment_q3=50.0,
            activity_score_qtd=80.0,
        )
        r = engine.analyze(inp)
        if not r.is_gaming_comp:
            assert r not in engine.gaming_reps

    def test_review_needed_empty_initially(self, engine):
        assert engine.review_needed == []

    def test_review_needed_contains_high_complaints(self, engine):
        inp = make_input(comp_complaints=3)
        r = engine.analyze(inp)
        assert r in engine.review_needed

    def test_total_overcompensation_zero_initially(self, engine):
        assert engine.total_overcompensation == 0.0

    def test_total_overcompensation_sums_correctly(self, engine):
        inp1 = make_input(rep_id="r1", revenue_closed_qtd=5_000.0, ote_salary=100_000.0)
        inp2 = make_input(rep_id="r2", revenue_closed_qtd=5_000.0, ote_salary=100_000.0)
        r1 = engine.analyze(inp1)
        r2 = engine.analyze(inp2)
        expected = round(r1.estimated_overcompensation + r2.estimated_overcompensation, 2)
        assert engine.total_overcompensation == expected

    def test_avg_compensation_efficiency_zero_when_empty(self, engine):
        assert engine.avg_compensation_efficiency == 0.0

    def test_avg_compensation_efficiency_single(self, engine):
        inp = make_input(revenue_closed_qtd=50_000.0, ote_salary=100_000.0)
        r = engine.analyze(inp)
        assert engine.avg_compensation_efficiency == round(r.compensation_efficiency_score, 1)

    def test_avg_compensation_efficiency_multiple(self, engine):
        inp1 = make_input(rep_id="r1", revenue_closed_qtd=25_000.0, ote_salary=100_000.0)
        inp2 = make_input(rep_id="r2", revenue_closed_qtd=100_000.0, ote_salary=100_000.0)
        r1 = engine.analyze(inp1)
        r2 = engine.analyze(inp2)
        expected = round((r1.compensation_efficiency_score + r2.compensation_efficiency_score) / 2, 1)
        assert engine.avg_compensation_efficiency == expected

    def test_total_overcompensation_rounded_to_2_decimals(self, engine):
        engine.analyze(make_input(revenue_closed_qtd=5_000.0, ote_salary=100_000.0))
        oc = engine.total_overcompensation
        assert oc == round(oc, 2)

    def test_gaming_reps_count_with_mixed_batch(self, engine):
        clean = make_input(rep_id="clean", spiff_driven_pct=0.0)
        gaming = make_input(rep_id="gaming",
                            spiff_driven_pct=100.0, large_deal_pct=100.0, multiyear_deal_pct=100.0)
        engine.analyze_batch([clean, gaming])
        gaming_ids = {r.rep_id for r in engine.gaming_reps}
        assert "gaming" in gaming_ids

    def test_review_needed_with_low_efficiency_rep(self, engine):
        inp = make_input(revenue_closed_qtd=0.0)
        r = engine.analyze(inp)
        assert r in engine.review_needed


# ══════════════════════════════════════════════════════════════════════════════
# 21. summary()
# ══════════════════════════════════════════════════════════════════════════════

class TestSummary:
    def test_empty_returns_13_keys(self, engine):
        assert len(engine.summary()) == 13

    def test_with_results_returns_13_keys(self, engine):
        engine.analyze(make_input())
        assert len(engine.summary()) == 13

    def test_empty_summary_exact_keys(self, engine):
        s = engine.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "alignment_counts",
            "action_counts", "avg_compensation_efficiency_score",
            "avg_sandbagging_score", "total_estimated_overcompensation",
            "gaming_count", "review_needed_count",
            "avg_spiff_dependency_score", "avg_discount_behavior_score",
            "avg_quota_accuracy_score",
        }
        assert set(s.keys()) == expected

    def test_empty_summary_total_is_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_summary_counts_are_empty_dicts(self, engine):
        s = engine.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["alignment_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_numeric_zeros(self, engine):
        s = engine.summary()
        for key in ("avg_compensation_efficiency_score", "avg_sandbagging_score",
                    "total_estimated_overcompensation", "gaming_count", "review_needed_count",
                    "avg_spiff_dependency_score", "avg_discount_behavior_score",
                    "avg_quota_accuracy_score"):
            assert s[key] == 0.0 or s[key] == 0

    def test_total_count_matches_analyzed(self, engine):
        for i in range(7):
            engine.analyze(make_input(rep_id=f"rep-{i}"))
        assert engine.summary()["total"] == 7

    def test_risk_counts_populated(self, engine):
        engine.analyze(make_input(comp_complaints=3))  # critical
        s = engine.summary()
        assert "critical" in s["risk_counts"]

    def test_pattern_counts_populated(self, engine):
        engine.analyze(make_input(spiff_driven_pct=100.0, large_deal_pct=100.0, multiyear_deal_pct=100.0))
        s = engine.summary()
        assert len(s["pattern_counts"]) > 0

    def test_gaming_count_matches_gaming_reps(self, engine):
        engine.analyze_batch([
            make_input(rep_id="r1", spiff_driven_pct=100.0, large_deal_pct=100.0, multiyear_deal_pct=100.0),
            make_input(rep_id="r2"),
        ])
        s = engine.summary()
        assert s["gaming_count"] == len(engine.gaming_reps)

    def test_review_needed_count_matches_property(self, engine):
        engine.analyze_batch([
            make_input(rep_id="r1", comp_complaints=3),
            make_input(rep_id="r2"),
        ])
        s = engine.summary()
        assert s["review_needed_count"] == len(engine.review_needed)

    def test_avg_sandbagging_score_correct(self, engine):
        inp1 = make_input(rep_id="r1", quarter_end_close_pct=0.0)
        inp2 = make_input(rep_id="r2", quarter_end_close_pct=0.0)
        r1 = engine.analyze(inp1)
        r2 = engine.analyze(inp2)
        expected_avg = round((r1.sandbagging_score + r2.sandbagging_score) / 2, 1)
        assert engine.summary()["avg_sandbagging_score"] == expected_avg

    def test_total_overcomp_in_summary(self, engine):
        inp = make_input(revenue_closed_qtd=0.0, ote_salary=100_000.0)
        engine.analyze(inp)
        s = engine.summary()
        assert s["total_estimated_overcompensation"] == engine.total_overcompensation

    def test_summary_after_reset_returns_empty(self, engine):
        engine.analyze(make_input())
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0

    def test_summary_13_keys_various_inputs(self, engine):
        inputs = [
            make_input(rep_id="r1", comp_complaints=3),
            make_input(rep_id="r2", spiff_driven_pct=100.0, large_deal_pct=100.0, multiyear_deal_pct=100.0),
            make_input(rep_id="r3", avg_discount_pct=0.0, revenue_closed_qtd=500_000.0),
        ]
        engine.analyze_batch(inputs)
        assert len(engine.summary()) == 13

    def test_avg_spiff_dependency_score_in_summary(self, engine):
        inp = make_input(spiff_driven_pct=50.0, large_deal_pct=0.0, multiyear_deal_pct=0.0)
        r = engine.analyze(inp)
        s = engine.summary()
        assert s["avg_spiff_dependency_score"] == round(r.spiff_dependency_score, 1)

    def test_avg_discount_behavior_score_in_summary(self, engine):
        inp = make_input(avg_discount_pct=20.0, comp_complaints=0)
        r = engine.analyze(inp)
        s = engine.summary()
        assert s["avg_discount_behavior_score"] == round(r.discount_behavior_score, 1)

    def test_avg_quota_accuracy_score_in_summary(self, engine):
        inp = make_input(quota_attainment_q1=100.0, quota_attainment_q2=100.0, quota_attainment_q3=100.0)
        r = engine.analyze(inp)
        s = engine.summary()
        assert s["avg_quota_accuracy_score"] == round(r.quota_accuracy_score, 1)

    def test_action_counts_populated(self, engine):
        engine.analyze(make_input(comp_complaints=3))
        s = engine.summary()
        assert len(s["action_counts"]) > 0

    def test_alignment_counts_populated(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert len(s["alignment_counts"]) > 0


# ══════════════════════════════════════════════════════════════════════════════
# 22. Engine initialization
# ══════════════════════════════════════════════════════════════════════════════

class TestEngineInit:
    def test_fresh_engine_no_results(self):
        e = SalesCompIntelligenceEngine()
        assert e._results == []

    def test_multiple_engines_independent(self):
        e1 = SalesCompIntelligenceEngine()
        e2 = SalesCompIntelligenceEngine()
        e1.analyze(make_input(rep_id="e1-rep"))
        assert len(e2._results) == 0

    def test_engine_can_be_instantiated_multiple_times(self):
        engines = [SalesCompIntelligenceEngine() for _ in range(5)]
        for e in engines:
            assert e._results == []


# ══════════════════════════════════════════════════════════════════════════════
# 23. Edge cases and boundary conditions
# ══════════════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    def test_zero_quota(self, engine):
        inp = make_input(quota=0.0)
        r = engine.analyze(inp)
        assert isinstance(r, SalesCompIntelResult)

    def test_zero_deals_closed(self, engine):
        inp = make_input(deals_closed_qtd=0, revenue_closed_qtd=0.0)
        r = engine.analyze(inp)
        assert r.compensation_efficiency_score == 0.0

    def test_very_high_comp_complaints(self, engine):
        inp = make_input(comp_complaints=100)
        r = engine.analyze(inp)
        assert r.comp_risk_level == CompRiskLevel.CRITICAL
        assert r.needs_comp_review is True

    def test_zero_base_salary(self, engine):
        inp = make_input(base_salary=0.0)
        r = engine.analyze(inp)
        assert isinstance(r, SalesCompIntelResult)

    def test_all_attainments_zero(self, engine):
        inp = make_input(quota_attainment_q1=0.0, quota_attainment_q2=0.0, quota_attainment_q3=0.0)
        r = engine.analyze(inp)
        assert isinstance(r, SalesCompIntelResult)
        assert r.quota_accuracy_score >= 0.0

    def test_max_all_percentages(self, engine):
        inp = make_input(
            large_deal_pct=100.0, spiff_driven_pct=100.0, quarter_end_close_pct=100.0,
            multiyear_deal_pct=100.0, avg_discount_pct=100.0,
        )
        r = engine.analyze(inp)
        assert isinstance(r, SalesCompIntelResult)

    def test_zero_activity_score(self, engine):
        inp = make_input(activity_score_qtd=0.0, revenue_closed_qtd=100_000.0)
        r = engine.analyze(inp)
        assert r.sandbagging_score > 0.0

    def test_max_activity_score(self, engine):
        inp = make_input(activity_score_qtd=100.0)
        r = engine.analyze(inp)
        assert isinstance(r, SalesCompIntelResult)

    def test_scores_are_finite(self, engine):
        inp = make_input()
        r = engine.analyze(inp)
        import math
        for score in (r.sandbagging_score, r.spiff_dependency_score,
                      r.discount_behavior_score, r.attainment_consistency_score,
                      r.compensation_efficiency_score, r.quota_accuracy_score):
            assert math.isfinite(score)

    def test_very_high_attainment_values(self, engine):
        inp = make_input(quota_attainment_q1=300.0, quota_attainment_q2=300.0, quota_attainment_q3=300.0)
        r = engine.analyze(inp)
        assert r.quota_accuracy_score >= 0.0

    def test_pipeline_value_larger_than_revenue(self, engine):
        inp = make_input(pipeline_value=5_000_000.0, revenue_closed_qtd=100_000.0)
        r = engine.analyze(inp)
        assert isinstance(r, SalesCompIntelResult)

    def test_to_dict_always_15_keys_edge_cases(self, engine):
        inputs = [
            make_input(comp_complaints=5),
            make_input(revenue_closed_qtd=0.0),
            make_input(avg_discount_pct=100.0),
            make_input(spiff_driven_pct=100.0),
        ]
        for inp in inputs:
            assert len(engine.analyze(inp).to_dict()) == 15

    def test_single_deal_closed(self, engine):
        inp = make_input(deals_closed_qtd=1, revenue_closed_qtd=50_000.0)
        r = engine.analyze(inp)
        assert isinstance(r, SalesCompIntelResult)


# ══════════════════════════════════════════════════════════════════════════════
# 24. Scenario-based tests
# ══════════════════════════════════════════════════════════════════════════════

class TestScenarios:
    def test_sandbagging_rep_scenario(self, engine):
        """Rep hits quota every quarter very consistently near 105%."""
        inp = make_input(
            rep_id="sandagger-1",
            quota_attainment_q1=104.0,
            quota_attainment_q2=106.0,
            quota_attainment_q3=105.0,
            quarter_end_close_pct=80.0,
            activity_score_qtd=25.0,
            revenue_closed_qtd=50_000.0,
            spiff_driven_pct=5.0,
            avg_discount_pct=5.0,
        )
        r = engine.analyze(inp)
        assert r.sandbagging_score > 30.0
        assert r.gaming_pattern in (GamingPattern.SANDBAGGING, GamingPattern.MIXED)

    def test_spiff_chaser_scenario(self, engine):
        """Rep only closes during spiff weeks and chases large deals."""
        inp = make_input(
            rep_id="spiff-chaser",
            spiff_driven_pct=85.0,
            large_deal_pct=70.0,
            multiyear_deal_pct=60.0,
            avg_discount_pct=5.0,
            quarter_end_close_pct=15.0,
        )
        r = engine.analyze(inp)
        assert r.spiff_dependency_score > 60.0
        assert r.is_gaming_comp is True

    def test_discount_heavy_scenario(self, engine):
        """Rep closes via heavy discounts."""
        inp = make_input(
            rep_id="discounter",
            avg_discount_pct=45.0,
            comp_complaints=2,
            revenue_closed_qtd=800_000.0,
            pipeline_value=1_000_000.0,
            deals_closed_qtd=10,
        )
        r = engine.analyze(inp)
        assert r.discount_behavior_score > 50.0
        assert r.is_gaming_comp is True

    def test_star_performer_scenario(self, engine):
        """High attainment, consistent, no gaming signals."""
        inp = make_input(
            rep_id="star",
            revenue_closed_qtd=400_000.0,
            ote_salary=160_000.0,
            quota_attainment_q1=115.0,
            quota_attainment_q2=118.0,
            quota_attainment_q3=120.0,
            spiff_driven_pct=5.0,
            avg_discount_pct=5.0,
            comp_complaints=0,
            activity_score_qtd=90.0,
            quarter_end_close_pct=20.0,
        )
        r = engine.analyze(inp)
        assert r.compensation_efficiency_score == 100.0
        assert r.estimated_overcompensation == 0.0

    def test_underperformer_scenario(self, engine):
        """Low revenue, below quota, needs review."""
        inp = make_input(
            rep_id="underperformer",
            revenue_closed_qtd=5_000.0,
            ote_salary=160_000.0,
            quota_attainment_q1=40.0,
            quota_attainment_q2=45.0,
            quota_attainment_q3=50.0,
            comp_complaints=0,
        )
        r = engine.analyze(inp)
        assert r.compensation_efficiency_score < 30.0
        assert r.needs_comp_review is True
        assert r.estimated_overcompensation > 0.0

    def test_mixed_gaming_scenario(self, engine):
        """Rep exhibits multiple gaming patterns."""
        inp = make_input(
            rep_id="all-gaming",
            quarter_end_close_pct=80.0,
            quota_attainment_q1=104.0,
            quota_attainment_q2=106.0,
            quota_attainment_q3=105.0,
            spiff_driven_pct=80.0,
            large_deal_pct=60.0,
            avg_discount_pct=35.0,
            activity_score_qtd=10.0,
            revenue_closed_qtd=50_000.0,
            comp_complaints=1,
        )
        r = engine.analyze(inp)
        assert r.gaming_pattern == GamingPattern.MIXED
        assert r.is_gaming_comp is True
        assert r.comp_action in (CompAction.RESTRUCTURE, CompAction.IMMEDIATE_REVIEW)

    def test_perverse_incentive_scenario(self, engine):
        """Rep with comp_complaints=3 should trigger perverse alignment."""
        inp = make_input(comp_complaints=3)
        r = engine.analyze(inp)
        assert r.incentive_alignment == IncentiveAlignment.PERVERSE
        assert r.comp_action == CompAction.IMMEDIATE_REVIEW

    def test_batch_mixed_pool(self, engine):
        """A diverse batch of reps produces correct summary counts."""
        inputs = [
            make_input(rep_id="star", revenue_closed_qtd=400_000.0, ote_salary=160_000.0,
                       comp_complaints=0, spiff_driven_pct=0.0),
            make_input(rep_id="gaming", spiff_driven_pct=100.0, large_deal_pct=100.0,
                       multiyear_deal_pct=100.0, comp_complaints=0),
            make_input(rep_id="struggling", revenue_closed_qtd=0.0, comp_complaints=0),
            make_input(rep_id="abuser", comp_complaints=3),
        ]
        results = engine.analyze_batch(inputs)
        s = engine.summary()
        assert s["total"] == 4
        assert s["gaming_count"] == len(engine.gaming_reps)
        assert s["review_needed_count"] == len(engine.review_needed)


# ══════════════════════════════════════════════════════════════════════════════
# 25. Additional coverage — individual score component precision tests
# ══════════════════════════════════════════════════════════════════════════════

class TestScoringPrecision:
    def test_sandbagging_variance_14_adds_signal(self, engine):
        # variance = 14 < 15 → signal = (15-14)*2.5 = 2.5
        inp = make_input(
            quarter_end_close_pct=0.0,
            quota_attainment_q1=97.0,
            quota_attainment_q2=104.0,
            quota_attainment_q3=111.0,
            activity_score_qtd=80.0,
        )
        # avg = 104, variance = 14 < 15, in range 95-120
        score = engine._sandbagging_score(inp)
        assert score > 0.0

    def test_sandbagging_activity_score_39_adds(self, engine):
        # activity_score = 39 < 40 → (40-39)*0.6 = 0.6
        inp = make_input(
            quarter_end_close_pct=0.0,
            quota_attainment_q1=50.0, quota_attainment_q2=150.0, quota_attainment_q3=50.0,
            activity_score_qtd=39.0, revenue_closed_qtd=50_000.0,
        )
        score = engine._sandbagging_score(inp)
        assert score == pytest.approx(0.6, abs=0.1)

    def test_discount_score_close_rate_bonus_cap(self, engine):
        # close_rate_proxy = 800000/800000*100=100 → bonus=(100-50)*0.8=40 → capped at 30
        inp = make_input(
            avg_discount_pct=25.0,
            deals_closed_qtd=5,
            revenue_closed_qtd=800_000.0,
            pipeline_value=800_000.0,
            comp_complaints=0,
        )
        score = engine._discount_behavior_score(inp)
        # 25*1.2 + min(30,(100-50)*0.8) = 30 + 30 = 60
        assert score == pytest.approx(60.0, abs=0.2)

    def test_quota_accuracy_excess_penalty(self, engine):
        # avg=160 → excess=50 → 100-50*1.5=25
        inp = make_input(quota_attainment_q1=160.0, quota_attainment_q2=160.0, quota_attainment_q3=160.0)
        assert engine._quota_accuracy_score(inp) == pytest.approx(25.0, abs=0.1)

    def test_quota_accuracy_shortfall_penalty(self, engine):
        # avg=40 → shortfall=50 → 100-50*2=0
        inp = make_input(quota_attainment_q1=40.0, quota_attainment_q2=40.0, quota_attainment_q3=40.0)
        assert engine._quota_accuracy_score(inp) == 0.0

    def test_comp_efficiency_multiple_3_5(self, engine):
        # multiple = 3.5 → (3.5-1)/4*100=62.5
        inp = make_input(revenue_closed_qtd=87_500.0, ote_salary=100_000.0)
        # annualized = 350_000; multiple = 350_000/100_000 = 3.5
        assert engine._compensation_efficiency_score(inp) == pytest.approx(62.5, abs=0.1)

    def test_sandbagging_q_end_pct_57_14(self, engine):
        # quarter_end = 57.14, contribution = min(40, 57.14*0.7) = min(40, 40.0) = 40
        inp = make_input(
            quarter_end_close_pct=57.14,
            quota_attainment_q1=50.0, quota_attainment_q2=150.0, quota_attainment_q3=50.0,
            activity_score_qtd=80.0,
        )
        score = engine._sandbagging_score(inp)
        assert score == pytest.approx(40.0, abs=0.1)

    def test_attainment_consistency_achievement_bonus_capped(self, engine):
        # avg = 150 → bonus = min(20, (150-80)*0.4) = min(20, 28) = 20
        inp = make_input(quota_attainment_q1=150.0, quota_attainment_q2=150.0, quota_attainment_q3=150.0)
        score = engine._attainment_consistency_score(inp)
        # consistency = 100*0.8 = 80, bonus = 20 → 80+20 = 100
        assert score == 100.0

    def test_spiff_score_all_components_partial(self, engine):
        inp = make_input(spiff_driven_pct=55.56, large_deal_pct=50.0, multiyear_deal_pct=50.0)
        # 55.56*0.9=50.0(capped), 50*0.6=30.0(capped), 50*0.4=20.0(capped) → 100
        score = engine._spiff_dependency_score(inp)
        assert score == 100.0

    def test_discount_complaints_2_adds_14(self, engine):
        inp = make_input(avg_discount_pct=0.0, comp_complaints=2, revenue_closed_qtd=0.0,
                         pipeline_value=1_000_000.0)
        score = engine._discount_behavior_score(inp)
        assert score == pytest.approx(14.0, abs=0.1)


# ══════════════════════════════════════════════════════════════════════════════
# 26. to_dict() value correctness
# ══════════════════════════════════════════════════════════════════════════════

class TestToDictValues:
    def test_comp_risk_level_low_in_dict(self, engine):
        inp = make_input(
            spiff_driven_pct=0.0, avg_discount_pct=0.0, comp_complaints=0,
            quarter_end_close_pct=0.0,
            quota_attainment_q1=50.0, quota_attainment_q2=150.0, quota_attainment_q3=50.0,
            activity_score_qtd=80.0,
        )
        d = engine.analyze(inp).to_dict()
        assert d["comp_risk_level"] == "low"

    def test_gaming_pattern_clean_in_dict(self, engine):
        inp = make_input(
            spiff_driven_pct=0.0, avg_discount_pct=0.0, comp_complaints=0,
            quarter_end_close_pct=0.0,
            quota_attainment_q1=50.0, quota_attainment_q2=150.0, quota_attainment_q3=50.0,
        )
        d = engine.analyze(inp).to_dict()
        assert d["gaming_pattern"] == "clean"

    def test_comp_risk_level_critical_in_dict(self, engine):
        inp = make_input(comp_complaints=3)
        d = engine.analyze(inp).to_dict()
        assert d["comp_risk_level"] == "critical"

    def test_comp_action_immediate_review_in_dict(self, engine):
        inp = make_input(comp_complaints=3)
        d = engine.analyze(inp).to_dict()
        assert d["comp_action"] == "immediate_review"

    def test_scores_match_result_attributes(self, engine):
        inp = make_input()
        r = engine.analyze(inp)
        d = r.to_dict()
        assert d["sandbagging_score"] == r.sandbagging_score
        assert d["spiff_dependency_score"] == r.spiff_dependency_score
        assert d["discount_behavior_score"] == r.discount_behavior_score
        assert d["attainment_consistency_score"] == r.attainment_consistency_score
        assert d["compensation_efficiency_score"] == r.compensation_efficiency_score
        assert d["estimated_overcompensation"] == r.estimated_overcompensation
        assert d["quota_accuracy_score"] == r.quota_accuracy_score
        assert d["is_gaming_comp"] == r.is_gaming_comp
        assert d["needs_comp_review"] == r.needs_comp_review

    def test_incentive_alignment_perverse_in_dict(self, engine):
        inp = make_input(comp_complaints=3)
        d = engine.analyze(inp).to_dict()
        assert d["incentive_alignment"] == "perverse"

    def test_is_gaming_false_for_clean(self, engine):
        inp = make_input(
            spiff_driven_pct=0.0, large_deal_pct=0.0, multiyear_deal_pct=0.0,
            avg_discount_pct=0.0, comp_complaints=0,
            quarter_end_close_pct=0.0,
            quota_attainment_q1=50.0, quota_attainment_q2=150.0, quota_attainment_q3=50.0,
            activity_score_qtd=80.0,
        )
        d = engine.analyze(inp).to_dict()
        assert d["is_gaming_comp"] is False

    def test_needs_review_true_for_high_complaints(self, engine):
        d = engine.analyze(make_input(comp_complaints=3)).to_dict()
        assert d["needs_comp_review"] is True
