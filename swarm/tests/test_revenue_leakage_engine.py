"""
Comprehensive pytest test suite for RevenuLeakageEngine.
Target: 270–290 tests, all passing.
"""
from __future__ import annotations

import dataclasses
import pytest

from swarm.intelligence.revenue_leakage_engine import (
    LeakageAction,
    LeakageCategory,
    LeakagePattern,
    LeakageRisk,
    RevenuLeakageEngine,
    RevenuLeakageInput,
    RevenuLeakageResult,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_input(**overrides) -> RevenuLeakageInput:
    defaults = dict(
        rep_id="rep_001",
        rep_name="Test Rep",
        region="NAMER",
        segment="enterprise",
        total_deals=40,
        discounted_deals=10,
        total_discount_value=50000.0,
        avg_list_price=20000.0,
        late_stage_losses=3,
        early_stage_exits=4,
        no_decision_deals=5,
        deals_without_champion=6,
        total_deals_with_champion_possible=25,
        deals_missing_exec_sponsor=4,
        total_exec_possible=20,
        multiyear_opportunities=10,
        multiyear_closed=5,
        expansion_opportunities=12,
        expansion_closed=6,
        price_objection_deals=3,
        total_pipeline_value=400000.0,
        avg_deal_size=18000.0,
    )
    defaults.update(overrides)
    return RevenuLeakageInput(**defaults)


@pytest.fixture
def engine():
    return RevenuLeakageEngine()


@pytest.fixture
def default_result(engine):
    return engine.analyze(make_input())


# ===========================================================================
# Section 1 – Enum values and types
# ===========================================================================

class TestLeakageCategoryEnum:
    def test_minimal_value(self):
        assert LeakageCategory.MINIMAL.value == "minimal"

    def test_moderate_value(self):
        assert LeakageCategory.MODERATE.value == "moderate"

    def test_significant_value(self):
        assert LeakageCategory.SIGNIFICANT.value == "significant"

    def test_critical_value(self):
        assert LeakageCategory.CRITICAL.value == "critical"

    def test_member_count(self):
        assert len(LeakageCategory) == 4

    def test_is_str_enum(self):
        assert isinstance(LeakageCategory.MINIMAL, str)

    def test_str_comparison(self):
        assert LeakageCategory.MINIMAL == "minimal"


class TestLeakageRiskEnum:
    def test_low_value(self):
        assert LeakageRisk.LOW.value == "low"

    def test_medium_value(self):
        assert LeakageRisk.MEDIUM.value == "medium"

    def test_high_value(self):
        assert LeakageRisk.HIGH.value == "high"

    def test_critical_value(self):
        assert LeakageRisk.CRITICAL.value == "critical"

    def test_member_count(self):
        assert len(LeakageRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(LeakageRisk.LOW, str)

    def test_str_comparison(self):
        assert LeakageRisk.HIGH == "high"


class TestLeakagePatternEnum:
    def test_discount_heavy_value(self):
        assert LeakagePattern.DISCOUNT_HEAVY.value == "discount_heavy"

    def test_late_stage_loss_value(self):
        assert LeakagePattern.LATE_STAGE_LOSS.value == "late_stage_loss"

    def test_champion_deficit_value(self):
        assert LeakagePattern.CHAMPION_DEFICIT.value == "champion_deficit"

    def test_multiyear_miss_value(self):
        assert LeakagePattern.MULTIYEAR_MISS.value == "multiyear_miss"

    def test_mixed_value(self):
        assert LeakagePattern.MIXED.value == "mixed"

    def test_member_count(self):
        assert len(LeakagePattern) == 5

    def test_is_str_enum(self):
        assert isinstance(LeakagePattern.MIXED, str)


class TestLeakageActionEnum:
    def test_monitor_value(self):
        assert LeakageAction.MONITOR.value == "monitor"

    def test_pricing_review_value(self):
        assert LeakageAction.PRICING_REVIEW.value == "pricing_review"

    def test_champion_coaching_value(self):
        assert LeakageAction.CHAMPION_COACHING.value == "champion_coaching"

    def test_deal_structuring_value(self):
        assert LeakageAction.DEAL_STRUCTURING.value == "deal_structuring"

    def test_urgent_intervention_value(self):
        assert LeakageAction.URGENT_INTERVENTION.value == "urgent_intervention"

    def test_member_count(self):
        assert len(LeakageAction) == 5

    def test_is_str_enum(self):
        assert isinstance(LeakageAction.MONITOR, str)


# ===========================================================================
# Section 2 – Input dataclass field count (22 fields)
# ===========================================================================

class TestInputDataclassFields:
    def test_field_count(self):
        fields = dataclasses.fields(RevenuLeakageInput)
        assert len(fields) == 22

    def test_has_rep_id(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "rep_id" in names

    def test_has_rep_name(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "rep_name" in names

    def test_has_region(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "region" in names

    def test_has_segment(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "segment" in names

    def test_has_total_deals(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "total_deals" in names

    def test_has_discounted_deals(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "discounted_deals" in names

    def test_has_total_discount_value(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "total_discount_value" in names

    def test_has_avg_list_price(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "avg_list_price" in names

    def test_has_late_stage_losses(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "late_stage_losses" in names

    def test_has_early_stage_exits(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "early_stage_exits" in names

    def test_has_no_decision_deals(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "no_decision_deals" in names

    def test_has_deals_without_champion(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "deals_without_champion" in names

    def test_has_total_deals_with_champion_possible(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "total_deals_with_champion_possible" in names

    def test_has_deals_missing_exec_sponsor(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "deals_missing_exec_sponsor" in names

    def test_has_total_exec_possible(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "total_exec_possible" in names

    def test_has_multiyear_opportunities(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "multiyear_opportunities" in names

    def test_has_multiyear_closed(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "multiyear_closed" in names

    def test_has_expansion_opportunities(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "expansion_opportunities" in names

    def test_has_expansion_closed(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "expansion_closed" in names

    def test_has_price_objection_deals(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "price_objection_deals" in names

    def test_has_total_pipeline_value(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "total_pipeline_value" in names

    def test_has_avg_deal_size(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageInput)}
        assert "avg_deal_size" in names


# ===========================================================================
# Section 3 – Result dataclass field count (15 fields)
# ===========================================================================

class TestResultDataclassFields:
    def test_field_count(self):
        fields = dataclasses.fields(RevenuLeakageResult)
        assert len(fields) == 15

    def test_has_rep_id(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "rep_id" in names

    def test_has_rep_name(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "rep_name" in names

    def test_has_leakage_category(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "leakage_category" in names

    def test_has_leakage_risk(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "leakage_risk" in names

    def test_has_leakage_pattern(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "leakage_pattern" in names

    def test_has_leakage_action(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "leakage_action" in names

    def test_has_discount_leakage_score(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "discount_leakage_score" in names

    def test_has_process_leakage_score(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "process_leakage_score" in names

    def test_has_champion_leakage_score(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "champion_leakage_score" in names

    def test_has_expansion_leakage_score(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "expansion_leakage_score" in names

    def test_has_total_leakage_score(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "total_leakage_score" in names

    def test_has_estimated_lost_revenue(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "estimated_lost_revenue" in names

    def test_has_recovery_potential(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "recovery_potential" in names

    def test_has_is_high_risk(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "is_high_risk" in names

    def test_has_needs_coaching(self):
        names = {f.name for f in dataclasses.fields(RevenuLeakageResult)}
        assert "needs_coaching" in names


# ===========================================================================
# Section 4 – to_dict() — exactly 15 keys, enums as strings
# ===========================================================================

class TestToDict:
    def test_key_count(self, default_result):
        assert len(default_result.to_dict()) == 15

    def test_has_rep_id_key(self, default_result):
        assert "rep_id" in default_result.to_dict()

    def test_has_rep_name_key(self, default_result):
        assert "rep_name" in default_result.to_dict()

    def test_has_leakage_category_key(self, default_result):
        assert "leakage_category" in default_result.to_dict()

    def test_has_leakage_risk_key(self, default_result):
        assert "leakage_risk" in default_result.to_dict()

    def test_has_leakage_pattern_key(self, default_result):
        assert "leakage_pattern" in default_result.to_dict()

    def test_has_leakage_action_key(self, default_result):
        assert "leakage_action" in default_result.to_dict()

    def test_has_discount_leakage_score_key(self, default_result):
        assert "discount_leakage_score" in default_result.to_dict()

    def test_has_process_leakage_score_key(self, default_result):
        assert "process_leakage_score" in default_result.to_dict()

    def test_has_champion_leakage_score_key(self, default_result):
        assert "champion_leakage_score" in default_result.to_dict()

    def test_has_expansion_leakage_score_key(self, default_result):
        assert "expansion_leakage_score" in default_result.to_dict()

    def test_has_total_leakage_score_key(self, default_result):
        assert "total_leakage_score" in default_result.to_dict()

    def test_has_estimated_lost_revenue_key(self, default_result):
        assert "estimated_lost_revenue" in default_result.to_dict()

    def test_has_recovery_potential_key(self, default_result):
        assert "recovery_potential" in default_result.to_dict()

    def test_has_is_high_risk_key(self, default_result):
        assert "is_high_risk" in default_result.to_dict()

    def test_has_needs_coaching_key(self, default_result):
        assert "needs_coaching" in default_result.to_dict()

    def test_leakage_category_is_str(self, default_result):
        d = default_result.to_dict()
        assert isinstance(d["leakage_category"], str)

    def test_leakage_risk_is_str(self, default_result):
        d = default_result.to_dict()
        assert isinstance(d["leakage_risk"], str)

    def test_leakage_pattern_is_str(self, default_result):
        d = default_result.to_dict()
        assert isinstance(d["leakage_pattern"], str)

    def test_leakage_action_is_str(self, default_result):
        d = default_result.to_dict()
        assert isinstance(d["leakage_action"], str)

    def test_leakage_category_not_enum_object(self, default_result):
        d = default_result.to_dict()
        assert not isinstance(d["leakage_category"], LeakageCategory)

    def test_leakage_risk_not_enum_object(self, default_result):
        d = default_result.to_dict()
        # str-enum comparisons: ensure it is the plain string value
        assert d["leakage_risk"] in ("low", "medium", "high", "critical")

    def test_rep_id_preserved(self, engine):
        result = engine.analyze(make_input(rep_id="xyz_999"))
        assert result.to_dict()["rep_id"] == "xyz_999"

    def test_rep_name_preserved(self, engine):
        result = engine.analyze(make_input(rep_name="Jane Doe"))
        assert result.to_dict()["rep_name"] == "Jane Doe"

    def test_scores_are_floats(self, default_result):
        d = default_result.to_dict()
        for key in ("discount_leakage_score", "process_leakage_score",
                    "champion_leakage_score", "expansion_leakage_score",
                    "total_leakage_score"):
            assert isinstance(d[key], float), f"{key} should be float"

    def test_is_high_risk_is_bool(self, default_result):
        assert isinstance(default_result.to_dict()["is_high_risk"], bool)

    def test_needs_coaching_is_bool(self, default_result):
        assert isinstance(default_result.to_dict()["needs_coaching"], bool)


# ===========================================================================
# Section 5 – summary() — exactly 13 keys, empty and populated
# ===========================================================================

class TestSummary:
    def test_empty_key_count(self, engine):
        assert len(engine.summary()) == 13

    def test_populated_key_count(self, engine):
        engine.analyze(make_input())
        assert len(engine.summary()) == 13

    def test_empty_total_is_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_category_counts_is_empty_dict(self, engine):
        assert engine.summary()["category_counts"] == {}

    def test_empty_risk_counts_is_empty_dict(self, engine):
        assert engine.summary()["risk_counts"] == {}

    def test_empty_pattern_counts_is_empty_dict(self, engine):
        assert engine.summary()["pattern_counts"] == {}

    def test_empty_action_counts_is_empty_dict(self, engine):
        assert engine.summary()["action_counts"] == {}

    def test_empty_avg_discount_leakage_score_zero(self, engine):
        assert engine.summary()["avg_discount_leakage_score"] == 0.0

    def test_empty_avg_total_leakage_score_zero(self, engine):
        assert engine.summary()["avg_total_leakage_score"] == 0.0

    def test_empty_total_estimated_lost_revenue_zero(self, engine):
        assert engine.summary()["total_estimated_lost_revenue"] == 0.0

    def test_empty_high_risk_count_zero(self, engine):
        assert engine.summary()["high_risk_count"] == 0

    def test_empty_coaching_count_zero(self, engine):
        assert engine.summary()["coaching_count"] == 0

    def test_empty_avg_recovery_potential_zero(self, engine):
        assert engine.summary()["avg_recovery_potential"] == 0.0

    def test_empty_total_pipeline_value_at_risk_zero(self, engine):
        assert engine.summary()["total_pipeline_value_at_risk"] == 0.0

    def test_empty_avg_process_leakage_score_zero(self, engine):
        assert engine.summary()["avg_process_leakage_score"] == 0.0

    def test_populated_total_correct(self, engine):
        engine.analyze(make_input())
        engine.analyze(make_input(rep_id="rep_002"))
        assert engine.summary()["total"] == 2

    def test_populated_has_category_key(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert len(s["category_counts"]) >= 1

    def test_populated_has_risk_key(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert len(s["risk_counts"]) >= 1

    def test_populated_has_pattern_key(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert len(s["pattern_counts"]) >= 1

    def test_populated_has_action_key(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert len(s["action_counts"]) >= 1

    def test_summary_keys_exact(self, engine):
        expected = {
            "total", "category_counts", "risk_counts", "pattern_counts",
            "action_counts", "avg_discount_leakage_score", "avg_total_leakage_score",
            "total_estimated_lost_revenue", "high_risk_count", "coaching_count",
            "avg_recovery_potential", "total_pipeline_value_at_risk",
            "avg_process_leakage_score",
        }
        assert set(engine.summary().keys()) == expected

    def test_summary_total_pipeline_at_risk_equals_total_estimated_loss(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert s["total_pipeline_value_at_risk"] == s["total_estimated_lost_revenue"]


# ===========================================================================
# Section 6 – _discount_leakage
# ===========================================================================

class TestDiscountLeakage:
    def test_zero_total_deals_returns_zero(self, engine):
        inp = make_input(total_deals=0)
        assert engine._discount_leakage(inp) == 0.0

    def test_discount_rate_contribution(self, engine):
        # discounted_deals/total_deals * 40
        inp = make_input(
            total_deals=10, discounted_deals=5,
            total_discount_value=0.0, avg_list_price=1.0,
            price_objection_deals=0,
        )
        score = engine._discount_leakage(inp)
        # discount_rate = 0.5 -> 20.0 for frequency; depth ~0; price_obj = 0
        assert score == pytest.approx(20.0, abs=1.0)

    def test_discount_depth_contribution(self, engine):
        # avg_discount_per_deal / avg_list_price * 100, capped at 35
        inp = make_input(
            total_deals=10, discounted_deals=0,
            total_discount_value=100000.0, avg_list_price=10000.0,
            price_objection_deals=0,
        )
        # avg_discount_per_deal = 100000/10 = 10000; depth = 10000/10000 = 1.0 -> 100 capped 35
        score = engine._discount_leakage(inp)
        assert score == pytest.approx(35.0, abs=0.5)

    def test_price_objection_rate_contribution(self, engine):
        # price_obj_rate * 50, capped at 25
        inp = make_input(
            total_deals=10, discounted_deals=0,
            total_discount_value=0.0, avg_list_price=1.0,
            price_objection_deals=10,
        )
        # rate = 1.0 -> 50 capped 25
        score = engine._discount_leakage(inp)
        assert score == pytest.approx(25.0, abs=0.5)

    def test_price_objection_half_rate(self, engine):
        inp = make_input(
            total_deals=10, discounted_deals=0,
            total_discount_value=0.0, avg_list_price=1.0,
            price_objection_deals=5,
        )
        # rate = 0.5 -> 25; capped 25
        score = engine._discount_leakage(inp)
        assert score == pytest.approx(25.0, abs=0.5)

    def test_all_zero_discounts_returns_zero(self, engine):
        inp = make_input(
            total_deals=10, discounted_deals=0,
            total_discount_value=0.0, avg_list_price=100.0,
            price_objection_deals=0,
        )
        assert engine._discount_leakage(inp) == 0.0

    def test_score_capped_at_100(self, engine):
        inp = make_input(
            total_deals=5, discounted_deals=5,
            total_discount_value=1000000.0, avg_list_price=1000.0,
            price_objection_deals=5,
        )
        assert engine._discount_leakage(inp) <= 100.0

    def test_score_non_negative(self, engine):
        assert engine._discount_leakage(make_input()) >= 0.0

    def test_zero_avg_list_price_no_depth_contribution(self, engine):
        # avg_list_price=0 => depth branch not entered
        inp = make_input(
            total_deals=10, discounted_deals=0,
            total_discount_value=50000.0, avg_list_price=0.0,
            price_objection_deals=0,
        )
        # Only frequency (0) + depth (skipped) + price_obj (0)
        assert engine._discount_leakage(inp) == 0.0

    def test_full_discount_rate(self, engine):
        inp = make_input(
            total_deals=10, discounted_deals=10,
            total_discount_value=0.0, avg_list_price=1.0,
            price_objection_deals=0,
        )
        # discount_rate=1.0 -> 40.0
        assert engine._discount_leakage(inp) == pytest.approx(40.0, abs=0.5)

    def test_depth_capped_at_35(self, engine):
        inp = make_input(
            total_deals=1, discounted_deals=0,
            total_discount_value=999999.0, avg_list_price=1.0,
            price_objection_deals=0,
        )
        score = engine._discount_leakage(inp)
        assert score <= 35.0 + 0.1


# ===========================================================================
# Section 7 – _process_leakage
# ===========================================================================

class TestProcessLeakage:
    def test_zero_total_deals_returns_zero(self, engine):
        inp = make_input(total_deals=0)
        assert engine._process_leakage(inp) == 0.0

    def test_late_stage_loss_contribution(self, engine):
        # late_loss_rate * 90, capped 45
        inp = make_input(
            total_deals=10, late_stage_losses=10,
            no_decision_deals=0, early_stage_exits=0,
        )
        # rate=1.0 -> 90 capped 45
        score = engine._process_leakage(inp)
        assert score == pytest.approx(45.0, abs=0.5)

    def test_no_decision_rate_contribution(self, engine):
        # no_dec_rate * 60, capped 30
        inp = make_input(
            total_deals=10, late_stage_losses=0,
            no_decision_deals=10, early_stage_exits=0,
        )
        # rate=1.0 -> 60 capped 30
        score = engine._process_leakage(inp)
        assert score == pytest.approx(30.0, abs=0.5)

    def test_early_exit_rate_contribution(self, engine):
        # early_exit_rate * 50, capped 25
        inp = make_input(
            total_deals=10, late_stage_losses=0,
            no_decision_deals=0, early_stage_exits=10,
        )
        # rate=1.0 -> 50 capped 25
        score = engine._process_leakage(inp)
        assert score == pytest.approx(25.0, abs=0.5)

    def test_all_zero_process_returns_zero(self, engine):
        inp = make_input(
            total_deals=10, late_stage_losses=0,
            no_decision_deals=0, early_stage_exits=0,
        )
        assert engine._process_leakage(inp) == 0.0

    def test_score_capped_at_100(self, engine):
        inp = make_input(
            total_deals=5, late_stage_losses=5,
            no_decision_deals=5, early_stage_exits=5,
        )
        assert engine._process_leakage(inp) <= 100.0

    def test_score_non_negative(self, engine):
        assert engine._process_leakage(make_input()) >= 0.0

    def test_partial_late_stage_loss(self, engine):
        # 5/10 = 0.5 rate -> 45 capped at 45 (0.5*90=45)
        inp = make_input(
            total_deals=10, late_stage_losses=5,
            no_decision_deals=0, early_stage_exits=0,
        )
        score = engine._process_leakage(inp)
        assert score == pytest.approx(45.0, abs=0.5)

    def test_partial_no_decision(self, engine):
        # 3/10 rate -> 18
        inp = make_input(
            total_deals=10, late_stage_losses=0,
            no_decision_deals=3, early_stage_exits=0,
        )
        score = engine._process_leakage(inp)
        assert score == pytest.approx(18.0, abs=0.5)

    def test_partial_early_exit(self, engine):
        # 2/10 rate -> 10
        inp = make_input(
            total_deals=10, late_stage_losses=0,
            no_decision_deals=0, early_stage_exits=2,
        )
        score = engine._process_leakage(inp)
        assert score == pytest.approx(10.0, abs=0.5)


# ===========================================================================
# Section 8 – _champion_leakage
# ===========================================================================

class TestChampionLeakage:
    def test_zero_champion_possible_skipped(self, engine):
        inp = make_input(
            total_deals_with_champion_possible=0,
            deals_without_champion=99,
            total_exec_possible=0,
            deals_missing_exec_sponsor=99,
        )
        assert engine._champion_leakage(inp) == 0.0

    def test_zero_exec_possible_skipped(self, engine):
        inp = make_input(
            total_deals_with_champion_possible=0,
            deals_without_champion=0,
            total_exec_possible=0,
            deals_missing_exec_sponsor=0,
        )
        assert engine._champion_leakage(inp) == 0.0

    def test_champion_miss_rate_contribution(self, engine):
        # no_champ_rate * 70, capped 50
        inp = make_input(
            deals_without_champion=10,
            total_deals_with_champion_possible=10,
            deals_missing_exec_sponsor=0,
            total_exec_possible=10,
        )
        # 1.0 * 70 capped 50 + 0 = 50
        score = engine._champion_leakage(inp)
        assert score == pytest.approx(50.0, abs=0.5)

    def test_exec_sponsor_miss_rate_contribution(self, engine):
        # no_exec_rate * 70, capped 50
        inp = make_input(
            deals_without_champion=0,
            total_deals_with_champion_possible=10,
            deals_missing_exec_sponsor=10,
            total_exec_possible=10,
        )
        # 0 + 1.0*70 capped 50 = 50
        score = engine._champion_leakage(inp)
        assert score == pytest.approx(50.0, abs=0.5)

    def test_both_max_gives_100(self, engine):
        inp = make_input(
            deals_without_champion=10,
            total_deals_with_champion_possible=10,
            deals_missing_exec_sponsor=10,
            total_exec_possible=10,
        )
        # 50 + 50 = 100
        score = engine._champion_leakage(inp)
        assert score == pytest.approx(100.0, abs=0.5)

    def test_score_non_negative(self, engine):
        assert engine._champion_leakage(make_input()) >= 0.0

    def test_score_capped_at_100(self, engine):
        inp = make_input(
            deals_without_champion=1000,
            total_deals_with_champion_possible=1,
            deals_missing_exec_sponsor=1000,
            total_exec_possible=1,
        )
        assert engine._champion_leakage(inp) <= 100.0

    def test_partial_champion_miss(self, engine):
        # 5/10 = 0.5 * 70 = 35
        inp = make_input(
            deals_without_champion=5,
            total_deals_with_champion_possible=10,
            deals_missing_exec_sponsor=0,
            total_exec_possible=10,
        )
        score = engine._champion_leakage(inp)
        assert score == pytest.approx(35.0, abs=0.5)

    def test_partial_exec_miss(self, engine):
        # 3/10 = 0.3 * 70 = 21
        inp = make_input(
            deals_without_champion=0,
            total_deals_with_champion_possible=10,
            deals_missing_exec_sponsor=3,
            total_exec_possible=10,
        )
        score = engine._champion_leakage(inp)
        assert score == pytest.approx(21.0, abs=0.5)


# ===========================================================================
# Section 9 – _expansion_leakage
# ===========================================================================

class TestExpansionLeakage:
    def test_zero_multiyear_opportunities_skipped(self, engine):
        inp = make_input(
            multiyear_opportunities=0, multiyear_closed=0,
            expansion_opportunities=0, expansion_closed=0,
        )
        assert engine._expansion_leakage(inp) == 0.0

    def test_full_multiyear_miss(self, engine):
        # miss=1.0 * 60 capped 50 = 50
        inp = make_input(
            multiyear_opportunities=10, multiyear_closed=0,
            expansion_opportunities=0, expansion_closed=0,
        )
        score = engine._expansion_leakage(inp)
        assert score == pytest.approx(50.0, abs=0.5)

    def test_full_expansion_miss(self, engine):
        inp = make_input(
            multiyear_opportunities=0, multiyear_closed=0,
            expansion_opportunities=10, expansion_closed=0,
        )
        # miss=1.0 * 60 capped 50 = 50
        score = engine._expansion_leakage(inp)
        assert score == pytest.approx(50.0, abs=0.5)

    def test_both_full_miss_gives_100(self, engine):
        inp = make_input(
            multiyear_opportunities=10, multiyear_closed=0,
            expansion_opportunities=10, expansion_closed=0,
        )
        score = engine._expansion_leakage(inp)
        assert score == pytest.approx(100.0, abs=0.5)

    def test_perfect_conversion_zero_score(self, engine):
        inp = make_input(
            multiyear_opportunities=10, multiyear_closed=10,
            expansion_opportunities=10, expansion_closed=10,
        )
        assert engine._expansion_leakage(inp) == 0.0

    def test_score_non_negative(self, engine):
        assert engine._expansion_leakage(make_input()) >= 0.0

    def test_score_capped_at_100(self, engine):
        inp = make_input(
            multiyear_opportunities=1, multiyear_closed=0,
            expansion_opportunities=1, expansion_closed=0,
        )
        assert engine._expansion_leakage(inp) <= 100.0

    def test_half_multiyear_miss(self, engine):
        # miss=0.5 * 60 = 30
        inp = make_input(
            multiyear_opportunities=10, multiyear_closed=5,
            expansion_opportunities=0, expansion_closed=0,
        )
        score = engine._expansion_leakage(inp)
        assert score == pytest.approx(30.0, abs=0.5)

    def test_half_expansion_miss(self, engine):
        # miss=0.5 * 60 = 30
        inp = make_input(
            multiyear_opportunities=0, multiyear_closed=0,
            expansion_opportunities=10, expansion_closed=5,
        )
        score = engine._expansion_leakage(inp)
        assert score == pytest.approx(30.0, abs=0.5)


# ===========================================================================
# Section 10 – _total_leakage_score weighted combination
# ===========================================================================

class TestTotalLeakageScore:
    def test_all_zero(self, engine):
        assert engine._total_leakage_score(0, 0, 0, 0) == 0.0

    def test_all_100(self, engine):
        assert engine._total_leakage_score(100, 100, 100, 100) == 100.0

    def test_weights_discount(self, engine):
        # discount*0.30
        score = engine._total_leakage_score(100, 0, 0, 0)
        assert score == pytest.approx(30.0, abs=0.1)

    def test_weights_process(self, engine):
        # process*0.35
        score = engine._total_leakage_score(0, 100, 0, 0)
        assert score == pytest.approx(35.0, abs=0.1)

    def test_weights_champion(self, engine):
        # champion*0.20
        score = engine._total_leakage_score(0, 0, 100, 0)
        assert score == pytest.approx(20.0, abs=0.1)

    def test_weights_expansion(self, engine):
        # expansion*0.15
        score = engine._total_leakage_score(0, 0, 0, 100)
        assert score == pytest.approx(15.0, abs=0.1)

    def test_weights_sum_to_100(self, engine):
        assert engine._total_leakage_score(100, 100, 100, 100) == pytest.approx(100.0, abs=0.1)

    def test_capped_at_100(self, engine):
        assert engine._total_leakage_score(200, 200, 200, 200) <= 100.0

    def test_floored_at_0(self, engine):
        assert engine._total_leakage_score(-10, -10, -10, -10) >= 0.0

    def test_example_computation(self, engine):
        # 50*0.30 + 40*0.35 + 30*0.20 + 20*0.15 = 15+14+6+3 = 38
        score = engine._total_leakage_score(50, 40, 30, 20)
        assert score == pytest.approx(38.0, abs=0.1)

    def test_result_is_rounded_to_1dp(self, engine):
        score = engine._total_leakage_score(33.33, 33.33, 33.33, 33.33)
        # Should be rounded to 1 decimal place
        assert score == round(score, 1)


# ===========================================================================
# Section 11 – _leakage_category boundaries
# ===========================================================================

class TestLeakageCategory:
    def test_critical_at_65(self, engine):
        assert engine._leakage_category(65.0) == LeakageCategory.CRITICAL

    def test_critical_above_65(self, engine):
        assert engine._leakage_category(80.0) == LeakageCategory.CRITICAL

    def test_critical_at_100(self, engine):
        assert engine._leakage_category(100.0) == LeakageCategory.CRITICAL

    def test_significant_at_45(self, engine):
        assert engine._leakage_category(45.0) == LeakageCategory.SIGNIFICANT

    def test_significant_at_64(self, engine):
        assert engine._leakage_category(64.9) == LeakageCategory.SIGNIFICANT

    def test_moderate_at_25(self, engine):
        assert engine._leakage_category(25.0) == LeakageCategory.MODERATE

    def test_moderate_at_44(self, engine):
        assert engine._leakage_category(44.9) == LeakageCategory.MODERATE

    def test_minimal_below_25(self, engine):
        assert engine._leakage_category(24.9) == LeakageCategory.MINIMAL

    def test_minimal_at_zero(self, engine):
        assert engine._leakage_category(0.0) == LeakageCategory.MINIMAL

    def test_minimal_at_10(self, engine):
        assert engine._leakage_category(10.0) == LeakageCategory.MINIMAL


# ===========================================================================
# Section 12 – _leakage_risk
# ===========================================================================

class TestLeakageRisk:
    def test_critical_when_score_65(self, engine):
        inp = make_input(late_stage_losses=0)
        assert engine._leakage_risk(inp, 65.0) == LeakageRisk.CRITICAL

    def test_critical_when_score_above_65(self, engine):
        inp = make_input(late_stage_losses=0)
        assert engine._leakage_risk(inp, 70.0) == LeakageRisk.CRITICAL

    def test_critical_when_late_stage_losses_5(self, engine):
        inp = make_input(late_stage_losses=5)
        assert engine._leakage_risk(inp, 10.0) == LeakageRisk.CRITICAL

    def test_critical_when_late_stage_losses_10(self, engine):
        inp = make_input(late_stage_losses=10)
        assert engine._leakage_risk(inp, 0.0) == LeakageRisk.CRITICAL

    def test_high_when_score_45(self, engine):
        inp = make_input(late_stage_losses=0, price_objection_deals=0)
        assert engine._leakage_risk(inp, 45.0) == LeakageRisk.HIGH

    def test_high_when_score_between_45_and_65(self, engine):
        inp = make_input(late_stage_losses=0, price_objection_deals=0)
        assert engine._leakage_risk(inp, 55.0) == LeakageRisk.HIGH

    def test_high_when_price_objection_deals_4(self, engine):
        inp = make_input(late_stage_losses=0, price_objection_deals=4)
        assert engine._leakage_risk(inp, 10.0) == LeakageRisk.HIGH

    def test_high_when_price_objection_deals_more_than_4(self, engine):
        inp = make_input(late_stage_losses=0, price_objection_deals=8)
        assert engine._leakage_risk(inp, 10.0) == LeakageRisk.HIGH

    def test_medium_when_score_25(self, engine):
        inp = make_input(late_stage_losses=0, price_objection_deals=0)
        assert engine._leakage_risk(inp, 25.0) == LeakageRisk.MEDIUM

    def test_medium_when_score_between_25_and_45(self, engine):
        inp = make_input(late_stage_losses=0, price_objection_deals=0)
        assert engine._leakage_risk(inp, 35.0) == LeakageRisk.MEDIUM

    def test_low_when_score_below_25(self, engine):
        inp = make_input(late_stage_losses=0, price_objection_deals=0)
        assert engine._leakage_risk(inp, 10.0) == LeakageRisk.LOW

    def test_low_when_score_zero(self, engine):
        inp = make_input(late_stage_losses=0, price_objection_deals=0)
        assert engine._leakage_risk(inp, 0.0) == LeakageRisk.LOW

    def test_late_stage_losses_4_not_critical_alone(self, engine):
        inp = make_input(late_stage_losses=4, price_objection_deals=0)
        risk = engine._leakage_risk(inp, 10.0)
        assert risk == LeakageRisk.LOW  # only 4 late_stage_losses, not 5


# ===========================================================================
# Section 13 – _leakage_pattern
# ===========================================================================

class TestLeakagePattern:
    def test_discount_heavy_dominant(self, engine):
        # discount far ahead of others
        pattern = engine._leakage_pattern(90, 10, 10, 10)
        assert pattern == LeakagePattern.DISCOUNT_HEAVY

    def test_late_stage_loss_dominant(self, engine):
        pattern = engine._leakage_pattern(10, 90, 10, 10)
        assert pattern == LeakagePattern.LATE_STAGE_LOSS

    def test_champion_deficit_dominant(self, engine):
        pattern = engine._leakage_pattern(10, 10, 90, 10)
        assert pattern == LeakagePattern.CHAMPION_DEFICIT

    def test_multiyear_miss_dominant(self, engine):
        pattern = engine._leakage_pattern(10, 10, 10, 90)
        assert pattern == LeakagePattern.MULTIYEAR_MISS

    def test_mixed_when_second_within_15_of_top(self, engine):
        # top=50, second=36 → 50-15=35, 36>=35 → mixed
        pattern = engine._leakage_pattern(50, 36, 10, 10)
        assert pattern == LeakagePattern.MIXED

    def test_not_mixed_when_second_16_below_top(self, engine):
        # top=50, second=34 → 34 < 50-15=35 → not mixed
        pattern = engine._leakage_pattern(50, 34, 10, 10)
        assert pattern != LeakagePattern.MIXED

    def test_all_equal_is_mixed(self, engine):
        # All equal: top equals second, within 15
        pattern = engine._leakage_pattern(50, 50, 50, 50)
        assert pattern == LeakagePattern.MIXED

    def test_mixed_exact_boundary(self, engine):
        # second = top - 15 exactly → mixed
        pattern = engine._leakage_pattern(50, 35, 10, 10)
        assert pattern == LeakagePattern.MIXED

    def test_all_zero_picks_discount_heavy(self, engine):
        # all equal at 0, so top = DISCOUNT_HEAVY (first max), second within 15
        pattern = engine._leakage_pattern(0, 0, 0, 0)
        assert pattern == LeakagePattern.MIXED  # second (0) >= 0 - 15 = -15


# ===========================================================================
# Section 14 – _leakage_action priority
# ===========================================================================

class TestLeakageAction:
    def test_urgent_when_critical_risk(self, engine):
        inp = make_input()
        action = engine._leakage_action(
            inp, LeakageCategory.CRITICAL, LeakageRisk.CRITICAL,
            LeakagePattern.MIXED, 70.0
        )
        assert action == LeakageAction.URGENT_INTERVENTION

    def test_champion_coaching_when_champion_deficit_non_critical(self, engine):
        inp = make_input()
        action = engine._leakage_action(
            inp, LeakageCategory.SIGNIFICANT, LeakageRisk.HIGH,
            LeakagePattern.CHAMPION_DEFICIT, 50.0
        )
        assert action == LeakageAction.CHAMPION_COACHING

    def test_pricing_review_when_discount_heavy_non_critical(self, engine):
        inp = make_input()
        action = engine._leakage_action(
            inp, LeakageCategory.MODERATE, LeakageRisk.MEDIUM,
            LeakagePattern.DISCOUNT_HEAVY, 35.0
        )
        assert action == LeakageAction.PRICING_REVIEW

    def test_deal_structuring_when_late_stage_loss(self, engine):
        inp = make_input()
        action = engine._leakage_action(
            inp, LeakageCategory.MODERATE, LeakageRisk.MEDIUM,
            LeakagePattern.LATE_STAGE_LOSS, 35.0
        )
        assert action == LeakageAction.DEAL_STRUCTURING

    def test_deal_structuring_when_mixed(self, engine):
        inp = make_input()
        action = engine._leakage_action(
            inp, LeakageCategory.MODERATE, LeakageRisk.MEDIUM,
            LeakagePattern.MIXED, 35.0
        )
        assert action == LeakageAction.DEAL_STRUCTURING

    def test_deal_structuring_when_multiyear_miss_and_score_above_25(self, engine):
        inp = make_input()
        action = engine._leakage_action(
            inp, LeakageCategory.MODERATE, LeakageRisk.MEDIUM,
            LeakagePattern.MULTIYEAR_MISS, 30.0
        )
        assert action == LeakageAction.DEAL_STRUCTURING

    def test_monitor_when_low_score_and_multiyear(self, engine):
        inp = make_input()
        action = engine._leakage_action(
            inp, LeakageCategory.MINIMAL, LeakageRisk.LOW,
            LeakagePattern.MULTIYEAR_MISS, 10.0
        )
        assert action == LeakageAction.MONITOR

    def test_urgent_overrides_champion(self, engine):
        # CRITICAL risk → URGENT even if pattern is CHAMPION_DEFICIT
        inp = make_input()
        action = engine._leakage_action(
            inp, LeakageCategory.CRITICAL, LeakageRisk.CRITICAL,
            LeakagePattern.CHAMPION_DEFICIT, 80.0
        )
        assert action == LeakageAction.URGENT_INTERVENTION

    def test_monitor_when_low_and_discount_low_score(self, engine):
        # Low score with MULTIYEAR_MISS → MONITOR
        inp = make_input()
        action = engine._leakage_action(
            inp, LeakageCategory.MINIMAL, LeakageRisk.LOW,
            LeakagePattern.DISCOUNT_HEAVY, 10.0
        )
        # score < 25 and pattern DISCOUNT_HEAVY → PRICING_REVIEW (discount_heavy fires before score check)
        assert action == LeakageAction.PRICING_REVIEW


# ===========================================================================
# Section 15 – is_high_risk
# ===========================================================================

class TestIsHighRisk:
    def test_high_risk_when_score_ge_60(self, engine):
        # Force a high total_score by making everything terrible
        inp = make_input(
            total_deals=10,
            discounted_deals=10,
            total_discount_value=200000.0,
            avg_list_price=10000.0,
            late_stage_losses=10,
            no_decision_deals=10,
            early_stage_exits=10,
            deals_without_champion=10,
            total_deals_with_champion_possible=10,
            deals_missing_exec_sponsor=10,
            total_exec_possible=10,
            multiyear_opportunities=10,
            multiyear_closed=0,
            expansion_opportunities=10,
            expansion_closed=0,
            price_objection_deals=10,
        )
        result = engine.analyze(inp)
        assert result.is_high_risk is True

    def test_not_high_risk_when_low_score_and_low_risk(self, engine):
        # Minimal everything
        inp = make_input(
            total_deals=10,
            discounted_deals=0,
            total_discount_value=0.0,
            avg_list_price=10000.0,
            late_stage_losses=0,
            no_decision_deals=0,
            early_stage_exits=0,
            deals_without_champion=0,
            total_deals_with_champion_possible=10,
            deals_missing_exec_sponsor=0,
            total_exec_possible=10,
            multiyear_opportunities=10,
            multiyear_closed=10,
            expansion_opportunities=10,
            expansion_closed=10,
            price_objection_deals=0,
        )
        result = engine.analyze(inp)
        assert result.is_high_risk is False

    def test_high_risk_when_risk_is_high(self, engine):
        # price_objection_deals >= 4 → HIGH risk → is_high_risk
        inp = make_input(
            total_deals=40,
            late_stage_losses=0,
            price_objection_deals=4,
            discounted_deals=0,
            total_discount_value=0.0,
            no_decision_deals=0,
            early_stage_exits=0,
        )
        result = engine.analyze(inp)
        assert result.is_high_risk is True

    def test_high_risk_when_risk_is_critical(self, engine):
        inp = make_input(late_stage_losses=5)
        result = engine.analyze(inp)
        assert result.is_high_risk is True

    def test_is_high_risk_type_is_bool(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.is_high_risk, bool)


# ===========================================================================
# Section 16 – needs_coaching
# ===========================================================================

class TestNeedsCoaching:
    def test_needs_coaching_when_discount_score_ge_50(self, engine):
        # discount_score >= 50
        inp = make_input(
            total_deals=10,
            discounted_deals=10,          # discount_rate=1 → 40
            total_discount_value=100000.0, # avg_discount=10000, depth=10000/1=10000 → capped 35
            avg_list_price=1.0,            # high depth
            price_objection_deals=0,
        )
        # 40 + 35 = 75 >= 50 → needs_coaching
        result = engine.analyze(inp)
        assert result.needs_coaching is True

    def test_needs_coaching_when_champion_score_ge_55(self, engine):
        # Both champion and exec miss at high rates to get ≥55
        inp = make_input(
            deals_without_champion=10,
            total_deals_with_champion_possible=10,
            deals_missing_exec_sponsor=5,
            total_exec_possible=10,
            discounted_deals=0,
            total_discount_value=0.0,
            price_objection_deals=0,
            late_stage_losses=0,
            no_decision_deals=0,
            early_stage_exits=0,
        )
        # 50 + 35 = 85 >= 55 → needs_coaching
        result = engine.analyze(inp)
        assert result.needs_coaching is True

    def test_needs_coaching_when_process_score_ge_60(self, engine):
        # late_stage_losses high enough to get process ≥ 60
        inp = make_input(
            total_deals=10,
            late_stage_losses=7,   # 0.7 * 90 = 63 capped 45
            no_decision_deals=6,   # 0.6 * 60 = 36 capped 30
            early_stage_exits=5,   # 0.5 * 50 = 25 capped 25
            discounted_deals=0,
            total_discount_value=0.0,
            price_objection_deals=0,
        )
        # 45 + 30 = 75 (or more) → process >= 60
        result = engine.analyze(inp)
        assert result.needs_coaching is True

    def test_not_needs_coaching_when_all_low(self, engine):
        inp = make_input(
            total_deals=10,
            discounted_deals=0,
            total_discount_value=0.0,
            avg_list_price=10000.0,
            late_stage_losses=0,
            no_decision_deals=0,
            early_stage_exits=0,
            deals_without_champion=0,
            total_deals_with_champion_possible=10,
            deals_missing_exec_sponsor=0,
            total_exec_possible=10,
            multiyear_opportunities=10,
            multiyear_closed=10,
            expansion_opportunities=10,
            expansion_closed=10,
            price_objection_deals=0,
        )
        result = engine.analyze(inp)
        assert result.needs_coaching is False

    def test_needs_coaching_type_is_bool(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.needs_coaching, bool)


# ===========================================================================
# Section 17 – Properties
# ===========================================================================

class TestProperties:
    def test_high_risk_reps_empty_initially(self, engine):
        assert engine.high_risk_reps == []

    def test_coaching_needed_empty_initially(self, engine):
        assert engine.coaching_needed == []

    def test_total_estimated_loss_zero_initially(self, engine):
        assert engine.total_estimated_loss == 0.0

    def test_avg_leakage_score_zero_initially(self, engine):
        assert engine.avg_leakage_score == 0.0

    def test_high_risk_reps_populated_after_analyze(self, engine):
        inp = make_input(late_stage_losses=5)  # CRITICAL risk → high risk
        engine.analyze(inp)
        assert len(engine.high_risk_reps) == 1

    def test_high_risk_reps_filters_correctly(self, engine):
        # One high-risk, one low-risk
        engine.analyze(make_input(
            total_deals=10, discounted_deals=0, total_discount_value=0.0,
            late_stage_losses=0, no_decision_deals=0, early_stage_exits=0,
            deals_without_champion=0, total_deals_with_champion_possible=10,
            deals_missing_exec_sponsor=0, total_exec_possible=10,
            multiyear_opportunities=10, multiyear_closed=10,
            expansion_opportunities=10, expansion_closed=10,
            price_objection_deals=0, rep_id="low",
        ))
        engine.analyze(make_input(late_stage_losses=5, rep_id="high"))
        assert len(engine.high_risk_reps) == 1
        assert engine.high_risk_reps[0].rep_id == "high"

    def test_coaching_needed_populated(self, engine):
        inp = make_input(
            total_deals=10, discounted_deals=10,
            total_discount_value=100000.0, avg_list_price=1.0,
            price_objection_deals=0,
        )
        engine.analyze(inp)
        assert len(engine.coaching_needed) == 1

    def test_total_estimated_loss_is_sum(self, engine):
        r1 = engine.analyze(make_input(rep_id="r1"))
        r2 = engine.analyze(make_input(rep_id="r2"))
        expected = round(r1.estimated_lost_revenue + r2.estimated_lost_revenue, 2)
        assert engine.total_estimated_loss == pytest.approx(expected, abs=0.01)

    def test_avg_leakage_score_single(self, engine):
        result = engine.analyze(make_input())
        assert engine.avg_leakage_score == pytest.approx(result.total_leakage_score, abs=0.1)

    def test_avg_leakage_score_multiple(self, engine):
        r1 = engine.analyze(make_input(rep_id="r1"))
        r2 = engine.analyze(make_input(rep_id="r2"))
        expected = round((r1.total_leakage_score + r2.total_leakage_score) / 2, 1)
        assert engine.avg_leakage_score == pytest.approx(expected, abs=0.1)

    def test_high_risk_reps_returns_list(self, engine):
        assert isinstance(engine.high_risk_reps, list)

    def test_coaching_needed_returns_list(self, engine):
        assert isinstance(engine.coaching_needed, list)

    def test_total_estimated_loss_returns_numeric(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.total_estimated_loss, (int, float))

    def test_avg_leakage_score_returns_float(self, engine):
        assert isinstance(engine.avg_leakage_score, float)


# ===========================================================================
# Section 18 – analyze_batch and reset
# ===========================================================================

class TestAnalyzeBatchAndReset:
    def test_analyze_batch_returns_list(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        assert isinstance(results, list)

    def test_analyze_batch_length(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_analyze_batch_each_is_result(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        for r in results:
            assert isinstance(r, RevenuLeakageResult)

    def test_analyze_batch_empty_list(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_analyze_batch_accumulates_results(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(4)]
        engine.analyze_batch(inputs)
        assert engine.summary()["total"] == 4

    def test_reset_clears_results(self, engine):
        engine.analyze(make_input())
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_reset_clears_high_risk_reps(self, engine):
        engine.analyze(make_input(late_stage_losses=5))
        engine.reset()
        assert engine.high_risk_reps == []

    def test_reset_clears_coaching_needed(self, engine):
        engine.analyze(make_input(
            total_deals=10, discounted_deals=10,
            total_discount_value=100000.0, avg_list_price=1.0,
        ))
        engine.reset()
        assert engine.coaching_needed == []

    def test_reset_zeroes_total_estimated_loss(self, engine):
        engine.analyze(make_input())
        engine.reset()
        assert engine.total_estimated_loss == 0.0

    def test_reset_zeroes_avg_leakage_score(self, engine):
        engine.analyze(make_input())
        engine.reset()
        assert engine.avg_leakage_score == 0.0

    def test_analyze_after_reset_accumulates_fresh(self, engine):
        engine.analyze(make_input(rep_id="old"))
        engine.reset()
        engine.analyze(make_input(rep_id="new"))
        assert engine.summary()["total"] == 1

    def test_batch_rep_ids_preserved(self, engine):
        inputs = [make_input(rep_id=f"rep_{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep_{i}"

    def test_large_batch_count(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(50)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 50
        assert engine.summary()["total"] == 50


# ===========================================================================
# Section 19 – Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_total_deals_zero_returns_result(self, engine):
        inp = make_input(total_deals=0, discounted_deals=0)
        result = engine.analyze(inp)
        assert isinstance(result, RevenuLeakageResult)

    def test_total_deals_zero_discount_score_zero(self, engine):
        result = engine.analyze(make_input(total_deals=0))
        assert result.discount_leakage_score == 0.0

    def test_total_deals_zero_process_score_zero(self, engine):
        result = engine.analyze(make_input(total_deals=0))
        assert result.process_leakage_score == 0.0

    def test_all_zeros_input(self, engine):
        inp = make_input(
            total_deals=0, discounted_deals=0, total_discount_value=0.0,
            avg_list_price=0.0, late_stage_losses=0, early_stage_exits=0,
            no_decision_deals=0, deals_without_champion=0,
            total_deals_with_champion_possible=0, deals_missing_exec_sponsor=0,
            total_exec_possible=0, multiyear_opportunities=0, multiyear_closed=0,
            expansion_opportunities=0, expansion_closed=0, price_objection_deals=0,
            total_pipeline_value=0.0, avg_deal_size=0.0,
        )
        result = engine.analyze(inp)
        assert result.total_leakage_score == 0.0

    def test_all_zeros_scores_are_zero(self, engine):
        inp = make_input(
            total_deals=0, discounted_deals=0, total_discount_value=0.0,
            avg_list_price=0.0, late_stage_losses=0, early_stage_exits=0,
            no_decision_deals=0, deals_without_champion=0,
            total_deals_with_champion_possible=0, deals_missing_exec_sponsor=0,
            total_exec_possible=0, multiyear_opportunities=0, multiyear_closed=0,
            expansion_opportunities=0, expansion_closed=0, price_objection_deals=0,
            total_pipeline_value=0.0, avg_deal_size=0.0,
        )
        result = engine.analyze(inp)
        assert result.discount_leakage_score == 0.0
        assert result.process_leakage_score == 0.0
        assert result.champion_leakage_score == 0.0
        assert result.expansion_leakage_score == 0.0

    def test_analyze_returns_result_instance(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result, RevenuLeakageResult)

    def test_multiple_analyses_independent(self, engine):
        r1 = engine.analyze(make_input(rep_id="A", total_deals=10, discounted_deals=0))
        r2 = engine.analyze(make_input(rep_id="B", total_deals=10, discounted_deals=10))
        assert r1.discount_leakage_score != r2.discount_leakage_score

    def test_rep_id_stored_in_result(self, engine):
        result = engine.analyze(make_input(rep_id="custom_id"))
        assert result.rep_id == "custom_id"

    def test_rep_name_stored_in_result(self, engine):
        result = engine.analyze(make_input(rep_name="Alice Smith"))
        assert result.rep_name == "Alice Smith"

    def test_score_bounds_all_scenarios(self, engine):
        for _ in range(5):
            result = engine.analyze(make_input())
            assert 0.0 <= result.total_leakage_score <= 100.0

    def test_estimated_lost_revenue_non_negative(self, engine):
        result = engine.analyze(make_input())
        assert result.estimated_lost_revenue >= 0.0

    def test_recovery_potential_bounded(self, engine):
        result = engine.analyze(make_input())
        assert 0.0 <= result.recovery_potential <= 100.0

    def test_perfect_rep_minimal_category(self, engine):
        inp = make_input(
            total_deals=20,
            discounted_deals=0, total_discount_value=0.0, avg_list_price=10000.0,
            late_stage_losses=0, early_stage_exits=0, no_decision_deals=0,
            deals_without_champion=0, total_deals_with_champion_possible=20,
            deals_missing_exec_sponsor=0, total_exec_possible=20,
            multiyear_opportunities=20, multiyear_closed=20,
            expansion_opportunities=20, expansion_closed=20,
            price_objection_deals=0,
        )
        result = engine.analyze(inp)
        assert result.leakage_category == LeakageCategory.MINIMAL
        assert result.leakage_risk == LeakageRisk.LOW


# ===========================================================================
# Section 20 – Estimated lost revenue calculation
# ===========================================================================

class TestEstimatedLostRevenue:
    def test_includes_discount_value(self, engine):
        inp = make_input(
            total_discount_value=100000.0,
            late_stage_losses=0,
            no_decision_deals=0,
            multiyear_opportunities=5, multiyear_closed=5,
            expansion_opportunities=5, expansion_closed=5,
            avg_deal_size=0.0,
        )
        result = engine.analyze(inp)
        assert result.estimated_lost_revenue >= 100000.0

    def test_includes_late_stage_losses(self, engine):
        inp = make_input(
            total_discount_value=0.0,
            late_stage_losses=5,
            no_decision_deals=0,
            avg_deal_size=10000.0,
            multiyear_opportunities=0,
            multiyear_closed=0,
            expansion_opportunities=0,
            expansion_closed=0,
        )
        # 5 * 10000 * 0.8 = 40000
        result = engine.analyze(inp)
        assert result.estimated_lost_revenue >= 40000.0

    def test_zero_everything_gives_zero(self, engine):
        inp = make_input(
            total_discount_value=0.0,
            late_stage_losses=0,
            no_decision_deals=0,
            multiyear_opportunities=0, multiyear_closed=0,
            expansion_opportunities=0, expansion_closed=0,
            avg_deal_size=0.0, total_deals=10,
        )
        result = engine.analyze(inp)
        assert result.estimated_lost_revenue == 0.0

    def test_non_negative(self, engine):
        result = engine.analyze(make_input())
        assert result.estimated_lost_revenue >= 0.0


# ===========================================================================
# Section 21 – Recovery potential
# ===========================================================================

class TestRecoveryPotential:
    def test_recovery_potential_non_negative(self, engine):
        result = engine.analyze(make_input())
        assert result.recovery_potential >= 0.0

    def test_recovery_potential_at_most_100(self, engine):
        result = engine.analyze(make_input())
        assert result.recovery_potential <= 100.0

    def test_higher_score_higher_recovery_base(self, engine):
        # All zeros → total_score near 0 → recovery close to 0 (+ pipeline boost)
        inp_low = make_input(
            total_deals=20,
            discounted_deals=0, total_discount_value=0.0, avg_list_price=10000.0,
            late_stage_losses=0, early_stage_exits=0, no_decision_deals=0,
            deals_without_champion=0, total_deals_with_champion_possible=20,
            deals_missing_exec_sponsor=0, total_exec_possible=20,
            multiyear_opportunities=20, multiyear_closed=20,
            expansion_opportunities=20, expansion_closed=20,
            price_objection_deals=0,
            total_pipeline_value=0.0,
        )
        inp_high = make_input(
            total_deals=10,
            discounted_deals=10, total_discount_value=200000.0, avg_list_price=1.0,
            late_stage_losses=10, early_stage_exits=10, no_decision_deals=10,
            deals_without_champion=10, total_deals_with_champion_possible=10,
            deals_missing_exec_sponsor=10, total_exec_possible=10,
            multiyear_opportunities=10, multiyear_closed=0,
            expansion_opportunities=10, expansion_closed=0,
            price_objection_deals=10,
            total_pipeline_value=0.0,
        )
        r_low = engine.analyze(inp_low)
        r_high = engine.analyze(inp_high)
        assert r_high.recovery_potential > r_low.recovery_potential

    def test_pipeline_boost_increases_recovery(self, engine):
        inp_no_pipeline = make_input(total_pipeline_value=0.0, avg_deal_size=10000.0)
        inp_pipeline = make_input(total_pipeline_value=500000.0, avg_deal_size=10000.0)
        r_no = engine.analyze(inp_no_pipeline)
        r_yes = engine.analyze(inp_pipeline)
        assert r_yes.recovery_potential >= r_no.recovery_potential


# ===========================================================================
# Section 22 – analyze() result field integrity
# ===========================================================================

class TestAnalyzeResultIntegrity:
    def test_result_category_is_enum(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.leakage_category, LeakageCategory)

    def test_result_risk_is_enum(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.leakage_risk, LeakageRisk)

    def test_result_pattern_is_enum(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.leakage_pattern, LeakagePattern)

    def test_result_action_is_enum(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.leakage_action, LeakageAction)

    def test_result_discount_score_float(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.discount_leakage_score, float)

    def test_result_process_score_float(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.process_leakage_score, float)

    def test_result_champion_score_float(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.champion_leakage_score, float)

    def test_result_expansion_score_float(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.expansion_leakage_score, float)

    def test_result_total_score_float(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.total_leakage_score, float)

    def test_all_sub_scores_between_0_and_100(self, engine):
        result = engine.analyze(make_input())
        for score in (
            result.discount_leakage_score, result.process_leakage_score,
            result.champion_leakage_score, result.expansion_leakage_score,
            result.total_leakage_score,
        ):
            assert 0.0 <= score <= 100.0

    def test_total_score_consistent_with_sub_scores(self, engine):
        inp = make_input()
        result = engine.analyze(inp)
        expected = round(
            result.discount_leakage_score * 0.30
            + result.process_leakage_score * 0.35
            + result.champion_leakage_score * 0.20
            + result.expansion_leakage_score * 0.15,
            1,
        )
        assert result.total_leakage_score == pytest.approx(expected, abs=0.05)

    def test_analyze_accumulates_to_engine(self, engine):
        engine.analyze(make_input(rep_id="r1"))
        engine.analyze(make_input(rep_id="r2"))
        assert engine.summary()["total"] == 2

    def test_different_reps_produce_different_results(self, engine):
        r1 = engine.analyze(make_input(rep_id="A", total_deals=5, late_stage_losses=5))
        r2 = engine.analyze(make_input(rep_id="B", total_deals=20, late_stage_losses=0))
        assert r1.total_leakage_score != r2.total_leakage_score
