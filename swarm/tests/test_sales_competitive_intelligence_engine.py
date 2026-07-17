"""
Comprehensive pytest test suite for SalesCompetitiveIntelligenceEngine.
Covers enums, dataclasses, sub-scores, composite formula, thresholds,
patterns, flags, pipeline formula, signals, assess(), assess_batch(),
summary(), and edge cases.
"""
from __future__ import annotations
import math
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from swarm.intelligence.sales_competitive_intelligence_engine import (
    CompRisk,
    CompPattern,
    CompSeverity,
    CompAction,
    CompInput,
    CompResult,
    SalesCompetitiveIntelligenceEngine,
)


# ── Helper ─────────────────────────────────────────────────────────────────

def make_input(**overrides) -> CompInput:
    """Return a minimal valid CompInput (all metrics mid-range / neutral).

    With these defaults the engine should produce a moderate-to-low composite
    so that tests can easily push a single dimension over a boundary.
    """
    defaults = dict(
        rep_id="REP-001",
        region="North",
        evaluation_period_id="Q2-2026",
        win_rate_vs_competitor_pct=0.55,        # above 0.50 – no score
        competitive_deal_pct=0.30,
        avg_discount_in_comp_deals_pct=0.10,    # below 0.12 – no score
        price_objection_rate_pct=0.20,
        feature_gap_mention_rate_pct=0.20,      # below 0.30 – no score
        battle_card_usage_rate_pct=0.80,        # above 0.75 – no score
        late_stage_competitive_loss_pct=0.10,   # below 0.25 – no score
        displacement_win_rate_pct=0.50,         # above 0.40 – no score
        proof_of_concept_win_rate_pct=0.60,     # above 0.55 – no score
        avg_cycle_len_comp_deals_days=30.0,
        multi_vendor_eval_pct=0.30,             # below 0.40 – no score
        executive_alignment_pct=0.75,           # above 0.70 – no score
        competitor_mention_per_call=1.0,        # below 1.5 – no score
        differentiation_score=0.70,             # above 0.60 – no score
        reference_customer_usage_rate=0.50,     # above 0.45 – no score
        total_competitive_deals=20,
        avg_deal_value_usd=50_000.0,
        total_pipeline_at_risk_usd=1_000_000.0,
    )
    defaults.update(overrides)
    return CompInput(**defaults)


def engine() -> SalesCompetitiveIntelligenceEngine:
    return SalesCompetitiveIntelligenceEngine()


# ══════════════════════════════════════════════════════════════════════════════
# 1.  ENUM VALUES AND COUNTS
# ══════════════════════════════════════════════════════════════════════════════

class TestCompRiskEnum:
    def test_count(self):
        assert len(CompRisk) == 4

    def test_low_value(self):
        assert CompRisk.low.value == "low"

    def test_moderate_value(self):
        assert CompRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert CompRisk.high.value == "high"

    def test_critical_value(self):
        assert CompRisk.critical.value == "critical"

    def test_is_str_enum(self):
        assert isinstance(CompRisk.low, str)

    def test_members(self):
        members = {m.value for m in CompRisk}
        assert members == {"low", "moderate", "high", "critical"}

    def test_lookup_by_value(self):
        assert CompRisk("moderate") == CompRisk.moderate


class TestCompPatternEnum:
    def test_count(self):
        assert len(CompPattern) == 6

    def test_none_value(self):
        assert CompPattern.none.value == "none"

    def test_price_surrender_value(self):
        assert CompPattern.price_surrender.value == "price_surrender"

    def test_feature_gap_concession_value(self):
        assert CompPattern.feature_gap_concession.value == "feature_gap_concession"

    def test_late_entry_loss_value(self):
        assert CompPattern.late_entry_loss.value == "late_entry_loss"

    def test_relationship_deficit_value(self):
        assert CompPattern.relationship_deficit.value == "relationship_deficit"

    def test_multi_vendor_spread_value(self):
        assert CompPattern.multi_vendor_spread.value == "multi_vendor_spread"

    def test_is_str_enum(self):
        assert isinstance(CompPattern.none, str)

    def test_members(self):
        members = {m.value for m in CompPattern}
        assert members == {
            "none", "price_surrender", "feature_gap_concession",
            "late_entry_loss", "relationship_deficit", "multi_vendor_spread",
        }


class TestCompSeverityEnum:
    def test_count(self):
        assert len(CompSeverity) == 4

    def test_dominant_value(self):
        assert CompSeverity.dominant.value == "dominant"

    def test_competitive_value(self):
        assert CompSeverity.competitive.value == "competitive"

    def test_challenged_value(self):
        assert CompSeverity.challenged.value == "challenged"

    def test_losing_value(self):
        assert CompSeverity.losing.value == "losing"

    def test_is_str_enum(self):
        assert isinstance(CompSeverity.dominant, str)

    def test_members(self):
        members = {m.value for m in CompSeverity}
        assert members == {"dominant", "competitive", "challenged", "losing"}


class TestCompActionEnum:
    def test_count(self):
        assert len(CompAction) == 7

    def test_no_action_value(self):
        assert CompAction.no_action.value == "no_action"

    def test_competitive_monitoring_value(self):
        assert CompAction.competitive_monitoring.value == "competitive_monitoring"

    def test_battle_card_coaching_value(self):
        assert CompAction.battle_card_coaching.value == "battle_card_coaching"

    def test_value_differentiation_coaching_value(self):
        assert CompAction.value_differentiation_coaching.value == "value_differentiation_coaching"

    def test_competitive_escalation_value(self):
        assert CompAction.competitive_escalation.value == "competitive_escalation"

    def test_win_loss_review_value(self):
        assert CompAction.win_loss_review.value == "win_loss_review"

    def test_competitive_strategy_reset_value(self):
        assert CompAction.competitive_strategy_reset.value == "competitive_strategy_reset"

    def test_is_str_enum(self):
        assert isinstance(CompAction.no_action, str)

    def test_members(self):
        members = {m.value for m in CompAction}
        assert members == {
            "no_action", "competitive_monitoring", "battle_card_coaching",
            "value_differentiation_coaching", "competitive_escalation",
            "win_loss_review", "competitive_strategy_reset",
        }


# ══════════════════════════════════════════════════════════════════════════════
# 2.  CompInput FIELDS
# ══════════════════════════════════════════════════════════════════════════════

class TestCompInputFields:
    def test_rep_id(self):
        inp = make_input(rep_id="X99")
        assert inp.rep_id == "X99"

    def test_region(self):
        inp = make_input(region="South")
        assert inp.region == "South"

    def test_evaluation_period_id(self):
        inp = make_input(evaluation_period_id="Q1-2025")
        assert inp.evaluation_period_id == "Q1-2025"

    def test_win_rate_vs_competitor_pct(self):
        inp = make_input(win_rate_vs_competitor_pct=0.42)
        assert inp.win_rate_vs_competitor_pct == pytest.approx(0.42)

    def test_competitive_deal_pct(self):
        inp = make_input(competitive_deal_pct=0.75)
        assert inp.competitive_deal_pct == pytest.approx(0.75)

    def test_avg_discount_in_comp_deals_pct(self):
        inp = make_input(avg_discount_in_comp_deals_pct=0.18)
        assert inp.avg_discount_in_comp_deals_pct == pytest.approx(0.18)

    def test_price_objection_rate_pct(self):
        inp = make_input(price_objection_rate_pct=0.33)
        assert inp.price_objection_rate_pct == pytest.approx(0.33)

    def test_feature_gap_mention_rate_pct(self):
        inp = make_input(feature_gap_mention_rate_pct=0.55)
        assert inp.feature_gap_mention_rate_pct == pytest.approx(0.55)

    def test_battle_card_usage_rate_pct(self):
        inp = make_input(battle_card_usage_rate_pct=0.60)
        assert inp.battle_card_usage_rate_pct == pytest.approx(0.60)

    def test_late_stage_competitive_loss_pct(self):
        inp = make_input(late_stage_competitive_loss_pct=0.40)
        assert inp.late_stage_competitive_loss_pct == pytest.approx(0.40)

    def test_displacement_win_rate_pct(self):
        inp = make_input(displacement_win_rate_pct=0.15)
        assert inp.displacement_win_rate_pct == pytest.approx(0.15)

    def test_proof_of_concept_win_rate_pct(self):
        inp = make_input(proof_of_concept_win_rate_pct=0.50)
        assert inp.proof_of_concept_win_rate_pct == pytest.approx(0.50)

    def test_avg_cycle_len_comp_deals_days(self):
        inp = make_input(avg_cycle_len_comp_deals_days=90.0)
        assert inp.avg_cycle_len_comp_deals_days == pytest.approx(90.0)

    def test_multi_vendor_eval_pct(self):
        inp = make_input(multi_vendor_eval_pct=0.70)
        assert inp.multi_vendor_eval_pct == pytest.approx(0.70)

    def test_executive_alignment_pct(self):
        inp = make_input(executive_alignment_pct=0.20)
        assert inp.executive_alignment_pct == pytest.approx(0.20)

    def test_competitor_mention_per_call(self):
        inp = make_input(competitor_mention_per_call=3.5)
        assert inp.competitor_mention_per_call == pytest.approx(3.5)

    def test_differentiation_score(self):
        inp = make_input(differentiation_score=0.30)
        assert inp.differentiation_score == pytest.approx(0.30)

    def test_reference_customer_usage_rate(self):
        inp = make_input(reference_customer_usage_rate=0.10)
        assert inp.reference_customer_usage_rate == pytest.approx(0.10)

    def test_total_competitive_deals(self):
        inp = make_input(total_competitive_deals=42)
        assert inp.total_competitive_deals == 42

    def test_avg_deal_value_usd(self):
        inp = make_input(avg_deal_value_usd=75_000.0)
        assert inp.avg_deal_value_usd == pytest.approx(75_000.0)

    def test_total_pipeline_at_risk_usd(self):
        inp = make_input(total_pipeline_at_risk_usd=2_000_000.0)
        assert inp.total_pipeline_at_risk_usd == pytest.approx(2_000_000.0)

    def test_field_count(self):
        import dataclasses
        assert len(dataclasses.fields(CompInput)) == 21


# ══════════════════════════════════════════════════════════════════════════════
# 3.  CompResult.to_dict()
# ══════════════════════════════════════════════════════════════════════════════

class TestCompResultToDict:
    def _result(self) -> CompResult:
        return engine().assess(make_input())

    def test_to_dict_returns_dict(self):
        assert isinstance(self._result().to_dict(), dict)

    def test_to_dict_exactly_15_keys(self):
        assert len(self._result().to_dict()) == 15

    def test_key_rep_id(self):
        assert "rep_id" in self._result().to_dict()

    def test_key_region(self):
        assert "region" in self._result().to_dict()

    def test_key_comp_risk(self):
        assert "comp_risk" in self._result().to_dict()

    def test_key_comp_pattern(self):
        assert "comp_pattern" in self._result().to_dict()

    def test_key_comp_severity(self):
        assert "comp_severity" in self._result().to_dict()

    def test_key_recommended_action(self):
        assert "recommended_action" in self._result().to_dict()

    def test_key_win_rate_score(self):
        assert "win_rate_score" in self._result().to_dict()

    def test_key_positioning_score(self):
        assert "positioning_score" in self._result().to_dict()

    def test_key_battle_readiness_score(self):
        assert "battle_readiness_score" in self._result().to_dict()

    def test_key_relationship_advantage_score(self):
        assert "relationship_advantage_score" in self._result().to_dict()

    def test_key_comp_composite(self):
        assert "comp_composite" in self._result().to_dict()

    def test_key_has_comp_gap(self):
        assert "has_comp_gap" in self._result().to_dict()

    def test_key_requires_comp_coaching(self):
        assert "requires_comp_coaching" in self._result().to_dict()

    def test_key_estimated_pipeline_at_risk_usd(self):
        assert "estimated_pipeline_at_risk_usd" in self._result().to_dict()

    def test_key_comp_signal(self):
        assert "comp_signal" in self._result().to_dict()

    def test_comp_risk_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["comp_risk"], str)

    def test_comp_pattern_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["comp_pattern"], str)

    def test_comp_severity_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["comp_severity"], str)

    def test_recommended_action_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_win_rate_score_is_number(self):
        d = self._result().to_dict()
        assert isinstance(d["win_rate_score"], (int, float))

    def test_comp_composite_is_number(self):
        d = self._result().to_dict()
        assert isinstance(d["comp_composite"], (int, float))

    def test_has_comp_gap_is_bool(self):
        d = self._result().to_dict()
        assert isinstance(d["has_comp_gap"], bool)

    def test_requires_comp_coaching_is_bool(self):
        d = self._result().to_dict()
        assert isinstance(d["requires_comp_coaching"], bool)

    def test_estimated_pipeline_is_number(self):
        d = self._result().to_dict()
        assert isinstance(d["estimated_pipeline_at_risk_usd"], (int, float))

    def test_comp_signal_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["comp_signal"], str)

    def test_rep_id_value_matches(self):
        inp = make_input(rep_id="ZREP")
        d = engine().assess(inp).to_dict()
        assert d["rep_id"] == "ZREP"

    def test_region_value_matches(self):
        inp = make_input(region="West")
        d = engine().assess(inp).to_dict()
        assert d["region"] == "West"

    def test_all_values_json_serializable(self):
        import json
        d = self._result().to_dict()
        # must not raise
        json.dumps(d)


# ══════════════════════════════════════════════════════════════════════════════
# 4.  SUB-SCORE METHODS – boundary conditions
# ══════════════════════════════════════════════════════════════════════════════

class TestWinRateScore:
    def _score(self, **kw):
        return engine()._win_rate_score(make_input(**kw))

    # win_rate_vs_competitor_pct
    def test_wr_exactly_030_gets_45(self):
        assert self._score(win_rate_vs_competitor_pct=0.30,
                           displacement_win_rate_pct=0.50,
                           late_stage_competitive_loss_pct=0.10) == 45

    def test_wr_below_030_gets_45(self):
        assert self._score(win_rate_vs_competitor_pct=0.29,
                           displacement_win_rate_pct=0.50,
                           late_stage_competitive_loss_pct=0.10) == 45

    def test_wr_zero_gets_45(self):
        assert self._score(win_rate_vs_competitor_pct=0.0,
                           displacement_win_rate_pct=0.50,
                           late_stage_competitive_loss_pct=0.10) == 45

    def test_wr_031_gets_25(self):
        assert self._score(win_rate_vs_competitor_pct=0.31,
                           displacement_win_rate_pct=0.50,
                           late_stage_competitive_loss_pct=0.10) == 25

    def test_wr_exactly_050_gets_25(self):
        assert self._score(win_rate_vs_competitor_pct=0.50,
                           displacement_win_rate_pct=0.50,
                           late_stage_competitive_loss_pct=0.10) == 25

    def test_wr_051_gets_10(self):
        assert self._score(win_rate_vs_competitor_pct=0.51,
                           displacement_win_rate_pct=0.50,
                           late_stage_competitive_loss_pct=0.10) == 10

    def test_wr_exactly_065_gets_10(self):
        assert self._score(win_rate_vs_competitor_pct=0.65,
                           displacement_win_rate_pct=0.50,
                           late_stage_competitive_loss_pct=0.10) == 10

    def test_wr_066_gets_0(self):
        assert self._score(win_rate_vs_competitor_pct=0.66,
                           displacement_win_rate_pct=0.50,
                           late_stage_competitive_loss_pct=0.10) == 0

    # displacement_win_rate_pct
    def test_disp_exactly_020_gets_30(self):
        assert self._score(win_rate_vs_competitor_pct=0.70,
                           displacement_win_rate_pct=0.20,
                           late_stage_competitive_loss_pct=0.10) == 30

    def test_disp_below_020_gets_30(self):
        assert self._score(win_rate_vs_competitor_pct=0.70,
                           displacement_win_rate_pct=0.10,
                           late_stage_competitive_loss_pct=0.10) == 30

    def test_disp_021_gets_15(self):
        assert self._score(win_rate_vs_competitor_pct=0.70,
                           displacement_win_rate_pct=0.21,
                           late_stage_competitive_loss_pct=0.10) == 15

    def test_disp_exactly_040_gets_15(self):
        assert self._score(win_rate_vs_competitor_pct=0.70,
                           displacement_win_rate_pct=0.40,
                           late_stage_competitive_loss_pct=0.10) == 15

    def test_disp_041_gets_0(self):
        assert self._score(win_rate_vs_competitor_pct=0.70,
                           displacement_win_rate_pct=0.41,
                           late_stage_competitive_loss_pct=0.10) == 0

    # late_stage_competitive_loss_pct
    def test_late_exactly_040_gets_25(self):
        assert self._score(win_rate_vs_competitor_pct=0.70,
                           displacement_win_rate_pct=0.50,
                           late_stage_competitive_loss_pct=0.40) == 25

    def test_late_above_040_gets_25(self):
        assert self._score(win_rate_vs_competitor_pct=0.70,
                           displacement_win_rate_pct=0.50,
                           late_stage_competitive_loss_pct=0.80) == 25

    def test_late_exactly_025_gets_12(self):
        assert self._score(win_rate_vs_competitor_pct=0.70,
                           displacement_win_rate_pct=0.50,
                           late_stage_competitive_loss_pct=0.25) == 12

    def test_late_039_gets_12(self):
        assert self._score(win_rate_vs_competitor_pct=0.70,
                           displacement_win_rate_pct=0.50,
                           late_stage_competitive_loss_pct=0.39) == 12

    def test_late_below_025_gets_0(self):
        assert self._score(win_rate_vs_competitor_pct=0.70,
                           displacement_win_rate_pct=0.50,
                           late_stage_competitive_loss_pct=0.10) == 0

    # cap at 100
    def test_capped_at_100(self):
        s = self._score(win_rate_vs_competitor_pct=0.0,
                        displacement_win_rate_pct=0.0,
                        late_stage_competitive_loss_pct=1.0)
        assert s == 100.0

    # zero
    def test_all_zero_risk(self):
        s = self._score(win_rate_vs_competitor_pct=1.0,
                        displacement_win_rate_pct=1.0,
                        late_stage_competitive_loss_pct=0.0)
        assert s == 0.0


class TestPositioningScore:
    def _score(self, **kw):
        return engine()._positioning_score(make_input(**kw))

    # avg_discount_in_comp_deals_pct
    def test_disc_exactly_030_gets_40(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.30,
                        feature_gap_mention_rate_pct=0.0,
                        differentiation_score=1.0)
        assert s == 40

    def test_disc_above_030_gets_40(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.50,
                        feature_gap_mention_rate_pct=0.0,
                        differentiation_score=1.0)
        assert s == 40

    def test_disc_exactly_020_gets_22(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.20,
                        feature_gap_mention_rate_pct=0.0,
                        differentiation_score=1.0)
        assert s == 22

    def test_disc_029_gets_22(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.29,
                        feature_gap_mention_rate_pct=0.0,
                        differentiation_score=1.0)
        assert s == 22

    def test_disc_exactly_012_gets_8(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.12,
                        feature_gap_mention_rate_pct=0.0,
                        differentiation_score=1.0)
        assert s == 8

    def test_disc_019_gets_8(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.19,
                        feature_gap_mention_rate_pct=0.0,
                        differentiation_score=1.0)
        assert s == 8

    def test_disc_below_012_gets_0(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.05,
                        feature_gap_mention_rate_pct=0.0,
                        differentiation_score=1.0)
        assert s == 0

    # feature_gap_mention_rate_pct
    def test_fg_exactly_050_gets_35(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.0,
                        feature_gap_mention_rate_pct=0.50,
                        differentiation_score=1.0)
        assert s == 35

    def test_fg_above_050_gets_35(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.0,
                        feature_gap_mention_rate_pct=0.90,
                        differentiation_score=1.0)
        assert s == 35

    def test_fg_exactly_030_gets_18(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.0,
                        feature_gap_mention_rate_pct=0.30,
                        differentiation_score=1.0)
        assert s == 18

    def test_fg_049_gets_18(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.0,
                        feature_gap_mention_rate_pct=0.49,
                        differentiation_score=1.0)
        assert s == 18

    def test_fg_below_030_gets_0(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.0,
                        feature_gap_mention_rate_pct=0.10,
                        differentiation_score=1.0)
        assert s == 0

    # differentiation_score
    def test_diff_exactly_035_gets_25(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.0,
                        feature_gap_mention_rate_pct=0.0,
                        differentiation_score=0.35)
        assert s == 25

    def test_diff_below_035_gets_25(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.0,
                        feature_gap_mention_rate_pct=0.0,
                        differentiation_score=0.10)
        assert s == 25

    def test_diff_exactly_060_gets_12(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.0,
                        feature_gap_mention_rate_pct=0.0,
                        differentiation_score=0.60)
        assert s == 12

    def test_diff_036_to_060_gets_12(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.0,
                        feature_gap_mention_rate_pct=0.0,
                        differentiation_score=0.50)
        assert s == 12

    def test_diff_above_060_gets_0(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.0,
                        feature_gap_mention_rate_pct=0.0,
                        differentiation_score=0.80)
        assert s == 0

    # cap
    def test_capped_at_100(self):
        s = self._score(avg_discount_in_comp_deals_pct=1.0,
                        feature_gap_mention_rate_pct=1.0,
                        differentiation_score=0.0)
        assert s == 100.0

    def test_zero_all(self):
        s = self._score(avg_discount_in_comp_deals_pct=0.0,
                        feature_gap_mention_rate_pct=0.0,
                        differentiation_score=1.0)
        assert s == 0.0


class TestBattleReadinessScore:
    def _score(self, **kw):
        return engine()._battle_readiness_score(make_input(**kw))

    # battle_card_usage_rate_pct
    def test_bc_exactly_025_gets_40(self):
        s = self._score(battle_card_usage_rate_pct=0.25,
                        proof_of_concept_win_rate_pct=1.0,
                        reference_customer_usage_rate=1.0)
        assert s == 40

    def test_bc_below_025_gets_40(self):
        s = self._score(battle_card_usage_rate_pct=0.10,
                        proof_of_concept_win_rate_pct=1.0,
                        reference_customer_usage_rate=1.0)
        assert s == 40

    def test_bc_exactly_055_gets_22(self):
        s = self._score(battle_card_usage_rate_pct=0.55,
                        proof_of_concept_win_rate_pct=1.0,
                        reference_customer_usage_rate=1.0)
        assert s == 22

    def test_bc_026_to_055_gets_22(self):
        s = self._score(battle_card_usage_rate_pct=0.40,
                        proof_of_concept_win_rate_pct=1.0,
                        reference_customer_usage_rate=1.0)
        assert s == 22

    def test_bc_exactly_075_gets_8(self):
        s = self._score(battle_card_usage_rate_pct=0.75,
                        proof_of_concept_win_rate_pct=1.0,
                        reference_customer_usage_rate=1.0)
        assert s == 8

    def test_bc_056_to_075_gets_8(self):
        s = self._score(battle_card_usage_rate_pct=0.65,
                        proof_of_concept_win_rate_pct=1.0,
                        reference_customer_usage_rate=1.0)
        assert s == 8

    def test_bc_above_075_gets_0(self):
        s = self._score(battle_card_usage_rate_pct=0.80,
                        proof_of_concept_win_rate_pct=1.0,
                        reference_customer_usage_rate=1.0)
        assert s == 0

    # proof_of_concept_win_rate_pct
    def test_poc_exactly_035_gets_35(self):
        s = self._score(battle_card_usage_rate_pct=1.0,
                        proof_of_concept_win_rate_pct=0.35,
                        reference_customer_usage_rate=1.0)
        assert s == 35

    def test_poc_below_035_gets_35(self):
        s = self._score(battle_card_usage_rate_pct=1.0,
                        proof_of_concept_win_rate_pct=0.10,
                        reference_customer_usage_rate=1.0)
        assert s == 35

    def test_poc_exactly_055_gets_18(self):
        s = self._score(battle_card_usage_rate_pct=1.0,
                        proof_of_concept_win_rate_pct=0.55,
                        reference_customer_usage_rate=1.0)
        assert s == 18

    def test_poc_036_to_055_gets_18(self):
        s = self._score(battle_card_usage_rate_pct=1.0,
                        proof_of_concept_win_rate_pct=0.45,
                        reference_customer_usage_rate=1.0)
        assert s == 18

    def test_poc_above_055_gets_0(self):
        s = self._score(battle_card_usage_rate_pct=1.0,
                        proof_of_concept_win_rate_pct=0.70,
                        reference_customer_usage_rate=1.0)
        assert s == 0

    # reference_customer_usage_rate
    def test_ref_exactly_020_gets_25(self):
        s = self._score(battle_card_usage_rate_pct=1.0,
                        proof_of_concept_win_rate_pct=1.0,
                        reference_customer_usage_rate=0.20)
        assert s == 25

    def test_ref_below_020_gets_25(self):
        s = self._score(battle_card_usage_rate_pct=1.0,
                        proof_of_concept_win_rate_pct=1.0,
                        reference_customer_usage_rate=0.05)
        assert s == 25

    def test_ref_exactly_045_gets_12(self):
        s = self._score(battle_card_usage_rate_pct=1.0,
                        proof_of_concept_win_rate_pct=1.0,
                        reference_customer_usage_rate=0.45)
        assert s == 12

    def test_ref_021_to_045_gets_12(self):
        s = self._score(battle_card_usage_rate_pct=1.0,
                        proof_of_concept_win_rate_pct=1.0,
                        reference_customer_usage_rate=0.35)
        assert s == 12

    def test_ref_above_045_gets_0(self):
        s = self._score(battle_card_usage_rate_pct=1.0,
                        proof_of_concept_win_rate_pct=1.0,
                        reference_customer_usage_rate=0.60)
        assert s == 0

    # cap
    def test_capped_at_100(self):
        s = self._score(battle_card_usage_rate_pct=0.0,
                        proof_of_concept_win_rate_pct=0.0,
                        reference_customer_usage_rate=0.0)
        assert s == 100.0

    def test_zero_all(self):
        s = self._score(battle_card_usage_rate_pct=1.0,
                        proof_of_concept_win_rate_pct=1.0,
                        reference_customer_usage_rate=1.0)
        assert s == 0.0


class TestRelationshipAdvantageScore:
    def _score(self, **kw):
        return engine()._relationship_advantage_score(make_input(**kw))

    # executive_alignment_pct
    def test_exec_exactly_025_gets_45(self):
        s = self._score(executive_alignment_pct=0.25,
                        multi_vendor_eval_pct=0.0,
                        competitor_mention_per_call=0.0)
        assert s == 45

    def test_exec_below_025_gets_45(self):
        s = self._score(executive_alignment_pct=0.10,
                        multi_vendor_eval_pct=0.0,
                        competitor_mention_per_call=0.0)
        assert s == 45

    def test_exec_exactly_050_gets_25(self):
        s = self._score(executive_alignment_pct=0.50,
                        multi_vendor_eval_pct=0.0,
                        competitor_mention_per_call=0.0)
        assert s == 25

    def test_exec_026_to_050_gets_25(self):
        s = self._score(executive_alignment_pct=0.40,
                        multi_vendor_eval_pct=0.0,
                        competitor_mention_per_call=0.0)
        assert s == 25

    def test_exec_exactly_070_gets_10(self):
        s = self._score(executive_alignment_pct=0.70,
                        multi_vendor_eval_pct=0.0,
                        competitor_mention_per_call=0.0)
        assert s == 10

    def test_exec_051_to_070_gets_10(self):
        s = self._score(executive_alignment_pct=0.60,
                        multi_vendor_eval_pct=0.0,
                        competitor_mention_per_call=0.0)
        assert s == 10

    def test_exec_above_070_gets_0(self):
        s = self._score(executive_alignment_pct=0.80,
                        multi_vendor_eval_pct=0.0,
                        competitor_mention_per_call=0.0)
        assert s == 0

    # multi_vendor_eval_pct
    def test_mv_exactly_060_gets_30(self):
        s = self._score(executive_alignment_pct=1.0,
                        multi_vendor_eval_pct=0.60,
                        competitor_mention_per_call=0.0)
        assert s == 30

    def test_mv_above_060_gets_30(self):
        s = self._score(executive_alignment_pct=1.0,
                        multi_vendor_eval_pct=0.90,
                        competitor_mention_per_call=0.0)
        assert s == 30

    def test_mv_exactly_040_gets_15(self):
        s = self._score(executive_alignment_pct=1.0,
                        multi_vendor_eval_pct=0.40,
                        competitor_mention_per_call=0.0)
        assert s == 15

    def test_mv_041_to_059_gets_15(self):
        s = self._score(executive_alignment_pct=1.0,
                        multi_vendor_eval_pct=0.50,
                        competitor_mention_per_call=0.0)
        assert s == 15

    def test_mv_below_040_gets_0(self):
        s = self._score(executive_alignment_pct=1.0,
                        multi_vendor_eval_pct=0.20,
                        competitor_mention_per_call=0.0)
        assert s == 0

    # competitor_mention_per_call
    def test_cm_exactly_30_gets_25(self):
        s = self._score(executive_alignment_pct=1.0,
                        multi_vendor_eval_pct=0.0,
                        competitor_mention_per_call=3.0)
        assert s == 25

    def test_cm_above_30_gets_25(self):
        s = self._score(executive_alignment_pct=1.0,
                        multi_vendor_eval_pct=0.0,
                        competitor_mention_per_call=5.0)
        assert s == 25

    def test_cm_exactly_15_gets_12(self):
        s = self._score(executive_alignment_pct=1.0,
                        multi_vendor_eval_pct=0.0,
                        competitor_mention_per_call=1.5)
        assert s == 12

    def test_cm_between_15_and_30_gets_12(self):
        s = self._score(executive_alignment_pct=1.0,
                        multi_vendor_eval_pct=0.0,
                        competitor_mention_per_call=2.0)
        assert s == 12

    def test_cm_below_15_gets_0(self):
        s = self._score(executive_alignment_pct=1.0,
                        multi_vendor_eval_pct=0.0,
                        competitor_mention_per_call=1.0)
        assert s == 0

    # cap
    def test_capped_at_100(self):
        s = self._score(executive_alignment_pct=0.0,
                        multi_vendor_eval_pct=1.0,
                        competitor_mention_per_call=5.0)
        assert s == 100.0

    def test_zero_all(self):
        s = self._score(executive_alignment_pct=1.0,
                        multi_vendor_eval_pct=0.0,
                        competitor_mention_per_call=0.0)
        assert s == 0.0


# ══════════════════════════════════════════════════════════════════════════════
# 5.  COMPOSITE FORMULA WEIGHTS
# ══════════════════════════════════════════════════════════════════════════════

class TestCompositeFormula:
    def test_weights_sum_to_1(self):
        assert pytest.approx(0.35 + 0.25 + 0.25 + 0.15, abs=1e-9) == 1.00

    def test_composite_with_all_zero(self):
        c = engine()._composite(0, 0, 0, 0)
        assert c == 0.0

    def test_composite_with_all_100(self):
        c = engine()._composite(100, 100, 100, 100)
        assert c == 100.0

    def test_composite_only_wr(self):
        # 100 * 0.35 = 35
        c = engine()._composite(100, 0, 0, 0)
        assert c == pytest.approx(35.0, abs=0.01)

    def test_composite_only_po(self):
        # 100 * 0.25 = 25
        c = engine()._composite(0, 100, 0, 0)
        assert c == pytest.approx(25.0, abs=0.01)

    def test_composite_only_br(self):
        # 100 * 0.25 = 25
        c = engine()._composite(0, 0, 100, 0)
        assert c == pytest.approx(25.0, abs=0.01)

    def test_composite_only_ra(self):
        # 100 * 0.15 = 15
        c = engine()._composite(0, 0, 0, 100)
        assert c == pytest.approx(15.0, abs=0.01)

    def test_composite_is_capped_at_100(self):
        c = engine()._composite(200, 200, 200, 200)
        assert c == 100.0

    def test_composite_rounded_to_2dp(self):
        # 10*0.35 + 10*0.25 + 10*0.25 + 10*0.15 = 10.00
        c = engine()._composite(10, 10, 10, 10)
        assert c == pytest.approx(10.0, abs=0.01)

    def test_composite_specific_values(self):
        # 40*0.35 + 60*0.25 + 80*0.25 + 20*0.15 = 14+15+20+3 = 52
        c = engine()._composite(40, 60, 80, 20)
        assert c == pytest.approx(52.0, abs=0.01)

    def test_composite_non_integer_inputs(self):
        c = engine()._composite(33.33, 66.67, 50.0, 25.0)
        expected = min(round(33.33 * 0.35 + 66.67 * 0.25 + 50.0 * 0.25 + 25.0 * 0.15, 2), 100.0)
        assert c == pytest.approx(expected, abs=0.01)


# ══════════════════════════════════════════════════════════════════════════════
# 6.  RISK / SEVERITY / ACTION THRESHOLDS
# ══════════════════════════════════════════════════════════════════════════════

class TestRiskThresholds:
    def _risk(self, composite):
        return engine()._risk(composite)

    def test_composite_0_is_low(self):
        assert self._risk(0) == CompRisk.low

    def test_composite_19_is_low(self):
        assert self._risk(19.9) == CompRisk.low

    def test_composite_exactly_20_is_moderate(self):
        assert self._risk(20) == CompRisk.moderate

    def test_composite_39_is_moderate(self):
        assert self._risk(39.9) == CompRisk.moderate

    def test_composite_exactly_40_is_high(self):
        assert self._risk(40) == CompRisk.high

    def test_composite_59_is_high(self):
        assert self._risk(59.9) == CompRisk.high

    def test_composite_exactly_60_is_critical(self):
        assert self._risk(60) == CompRisk.critical

    def test_composite_100_is_critical(self):
        assert self._risk(100) == CompRisk.critical


class TestSeverityThresholds:
    def _sev(self, composite):
        return engine()._severity(composite)

    def test_composite_0_is_dominant(self):
        assert self._sev(0) == CompSeverity.dominant

    def test_composite_19_is_dominant(self):
        assert self._sev(19.9) == CompSeverity.dominant

    def test_composite_exactly_20_is_competitive(self):
        assert self._sev(20) == CompSeverity.competitive

    def test_composite_39_is_competitive(self):
        assert self._sev(39.9) == CompSeverity.competitive

    def test_composite_exactly_40_is_challenged(self):
        assert self._sev(40) == CompSeverity.challenged

    def test_composite_59_is_challenged(self):
        assert self._sev(59.9) == CompSeverity.challenged

    def test_composite_exactly_60_is_losing(self):
        assert self._sev(60) == CompSeverity.losing

    def test_composite_100_is_losing(self):
        assert self._sev(100) == CompSeverity.losing


class TestActionThresholds:
    def _action(self, risk, pattern):
        return engine()._action(risk, pattern)

    # low risk
    def test_low_none_is_no_action(self):
        assert self._action(CompRisk.low, CompPattern.none) == CompAction.no_action

    def test_low_any_pattern_is_no_action(self):
        assert self._action(CompRisk.low, CompPattern.price_surrender) == CompAction.no_action

    # moderate risk
    def test_moderate_none_is_monitoring(self):
        assert self._action(CompRisk.moderate, CompPattern.none) == CompAction.competitive_monitoring

    def test_moderate_price_surrender_is_monitoring(self):
        assert self._action(CompRisk.moderate, CompPattern.price_surrender) == CompAction.competitive_monitoring

    def test_moderate_feature_gap_is_monitoring(self):
        assert self._action(CompRisk.moderate, CompPattern.feature_gap_concession) == CompAction.competitive_monitoring

    def test_moderate_late_entry_is_monitoring(self):
        assert self._action(CompRisk.moderate, CompPattern.late_entry_loss) == CompAction.competitive_monitoring

    # high risk
    def test_high_price_surrender_is_value_diff(self):
        assert self._action(CompRisk.high, CompPattern.price_surrender) == CompAction.value_differentiation_coaching

    def test_high_feature_gap_is_battle_card(self):
        assert self._action(CompRisk.high, CompPattern.feature_gap_concession) == CompAction.battle_card_coaching

    def test_high_late_entry_is_escalation(self):
        assert self._action(CompRisk.high, CompPattern.late_entry_loss) == CompAction.competitive_escalation

    def test_high_relationship_deficit_is_escalation(self):
        assert self._action(CompRisk.high, CompPattern.relationship_deficit) == CompAction.competitive_escalation

    def test_high_multi_vendor_is_battle_card(self):
        assert self._action(CompRisk.high, CompPattern.multi_vendor_spread) == CompAction.battle_card_coaching

    def test_high_none_is_battle_card(self):
        assert self._action(CompRisk.high, CompPattern.none) == CompAction.battle_card_coaching

    # critical risk
    def test_critical_price_surrender_is_strategy_reset(self):
        assert self._action(CompRisk.critical, CompPattern.price_surrender) == CompAction.competitive_strategy_reset

    def test_critical_feature_gap_is_strategy_reset(self):
        assert self._action(CompRisk.critical, CompPattern.feature_gap_concession) == CompAction.competitive_strategy_reset

    def test_critical_late_entry_is_win_loss_review(self):
        assert self._action(CompRisk.critical, CompPattern.late_entry_loss) == CompAction.win_loss_review

    def test_critical_relationship_deficit_is_win_loss_review(self):
        assert self._action(CompRisk.critical, CompPattern.relationship_deficit) == CompAction.win_loss_review

    def test_critical_multi_vendor_is_win_loss_review(self):
        assert self._action(CompRisk.critical, CompPattern.multi_vendor_spread) == CompAction.win_loss_review

    def test_critical_none_is_win_loss_review(self):
        assert self._action(CompRisk.critical, CompPattern.none) == CompAction.win_loss_review


# ══════════════════════════════════════════════════════════════════════════════
# 7.  PATTERN DETECTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════

class TestPatternDetection:
    def _pat(self, **kw):
        return engine()._pattern(make_input(**kw))

    # price_surrender: avg_discount >= 0.25 AND win_rate <= 0.40
    def test_price_surrender_triggered(self):
        p = self._pat(avg_discount_in_comp_deals_pct=0.25, win_rate_vs_competitor_pct=0.40,
                      feature_gap_mention_rate_pct=0.0, differentiation_score=1.0,
                      late_stage_competitive_loss_pct=0.0, competitive_deal_pct=0.0,
                      executive_alignment_pct=1.0, multi_vendor_eval_pct=0.0,
                      displacement_win_rate_pct=1.0)
        assert p == CompPattern.price_surrender

    def test_price_surrender_not_triggered_low_discount(self):
        p = self._pat(avg_discount_in_comp_deals_pct=0.24, win_rate_vs_competitor_pct=0.40,
                      feature_gap_mention_rate_pct=0.0, differentiation_score=1.0,
                      late_stage_competitive_loss_pct=0.0, competitive_deal_pct=0.0,
                      executive_alignment_pct=1.0, multi_vendor_eval_pct=0.0,
                      displacement_win_rate_pct=1.0)
        assert p != CompPattern.price_surrender

    def test_price_surrender_not_triggered_high_win_rate(self):
        p = self._pat(avg_discount_in_comp_deals_pct=0.30, win_rate_vs_competitor_pct=0.41,
                      feature_gap_mention_rate_pct=0.0, differentiation_score=1.0,
                      late_stage_competitive_loss_pct=0.0, competitive_deal_pct=0.0,
                      executive_alignment_pct=1.0, multi_vendor_eval_pct=0.0,
                      displacement_win_rate_pct=1.0)
        assert p != CompPattern.price_surrender

    # feature_gap_concession: feature_gap >= 0.45 AND diff_score <= 0.40
    def test_feature_gap_concession_triggered(self):
        p = self._pat(feature_gap_mention_rate_pct=0.45, differentiation_score=0.40,
                      avg_discount_in_comp_deals_pct=0.0, win_rate_vs_competitor_pct=1.0,
                      late_stage_competitive_loss_pct=0.0, competitive_deal_pct=0.0,
                      executive_alignment_pct=1.0, multi_vendor_eval_pct=0.0,
                      displacement_win_rate_pct=1.0)
        assert p == CompPattern.feature_gap_concession

    def test_feature_gap_concession_not_triggered_low_mention(self):
        p = self._pat(feature_gap_mention_rate_pct=0.44, differentiation_score=0.40,
                      avg_discount_in_comp_deals_pct=0.0, win_rate_vs_competitor_pct=1.0,
                      late_stage_competitive_loss_pct=0.0, competitive_deal_pct=0.0,
                      executive_alignment_pct=1.0, multi_vendor_eval_pct=0.0,
                      displacement_win_rate_pct=1.0)
        assert p != CompPattern.feature_gap_concession

    def test_feature_gap_concession_not_triggered_high_diff(self):
        p = self._pat(feature_gap_mention_rate_pct=0.50, differentiation_score=0.41,
                      avg_discount_in_comp_deals_pct=0.0, win_rate_vs_competitor_pct=1.0,
                      late_stage_competitive_loss_pct=0.0, competitive_deal_pct=0.0,
                      executive_alignment_pct=1.0, multi_vendor_eval_pct=0.0,
                      displacement_win_rate_pct=1.0)
        assert p != CompPattern.feature_gap_concession

    # late_entry_loss: late_stage >= 0.35 AND comp_deal >= 0.50
    def test_late_entry_loss_triggered(self):
        p = self._pat(late_stage_competitive_loss_pct=0.35, competitive_deal_pct=0.50,
                      avg_discount_in_comp_deals_pct=0.0, win_rate_vs_competitor_pct=1.0,
                      feature_gap_mention_rate_pct=0.0, differentiation_score=1.0,
                      executive_alignment_pct=1.0, multi_vendor_eval_pct=0.0,
                      displacement_win_rate_pct=1.0)
        assert p == CompPattern.late_entry_loss

    def test_late_entry_loss_not_triggered_low_late(self):
        p = self._pat(late_stage_competitive_loss_pct=0.34, competitive_deal_pct=0.60,
                      avg_discount_in_comp_deals_pct=0.0, win_rate_vs_competitor_pct=1.0,
                      feature_gap_mention_rate_pct=0.0, differentiation_score=1.0,
                      executive_alignment_pct=1.0, multi_vendor_eval_pct=0.0,
                      displacement_win_rate_pct=1.0)
        assert p != CompPattern.late_entry_loss

    def test_late_entry_loss_not_triggered_low_comp_deal(self):
        p = self._pat(late_stage_competitive_loss_pct=0.40, competitive_deal_pct=0.49,
                      avg_discount_in_comp_deals_pct=0.0, win_rate_vs_competitor_pct=1.0,
                      feature_gap_mention_rate_pct=0.0, differentiation_score=1.0,
                      executive_alignment_pct=1.0, multi_vendor_eval_pct=0.0,
                      displacement_win_rate_pct=1.0)
        assert p != CompPattern.late_entry_loss

    # relationship_deficit: exec_align <= 0.25 AND multi_vendor >= 0.50
    def test_relationship_deficit_triggered(self):
        p = self._pat(executive_alignment_pct=0.25, multi_vendor_eval_pct=0.50,
                      avg_discount_in_comp_deals_pct=0.0, win_rate_vs_competitor_pct=1.0,
                      feature_gap_mention_rate_pct=0.0, differentiation_score=1.0,
                      late_stage_competitive_loss_pct=0.0, competitive_deal_pct=0.0,
                      displacement_win_rate_pct=1.0)
        assert p == CompPattern.relationship_deficit

    def test_relationship_deficit_not_triggered_high_exec(self):
        p = self._pat(executive_alignment_pct=0.26, multi_vendor_eval_pct=0.70,
                      avg_discount_in_comp_deals_pct=0.0, win_rate_vs_competitor_pct=1.0,
                      feature_gap_mention_rate_pct=0.0, differentiation_score=1.0,
                      late_stage_competitive_loss_pct=0.0, competitive_deal_pct=0.0,
                      displacement_win_rate_pct=1.0)
        assert p != CompPattern.relationship_deficit

    def test_relationship_deficit_not_triggered_low_mv(self):
        p = self._pat(executive_alignment_pct=0.20, multi_vendor_eval_pct=0.49,
                      avg_discount_in_comp_deals_pct=0.0, win_rate_vs_competitor_pct=1.0,
                      feature_gap_mention_rate_pct=0.0, differentiation_score=1.0,
                      late_stage_competitive_loss_pct=0.0, competitive_deal_pct=0.0,
                      displacement_win_rate_pct=1.0)
        assert p != CompPattern.relationship_deficit

    # multi_vendor_spread: multi_vendor >= 0.65 AND displacement <= 0.25
    def test_multi_vendor_spread_triggered(self):
        p = self._pat(multi_vendor_eval_pct=0.65, displacement_win_rate_pct=0.25,
                      avg_discount_in_comp_deals_pct=0.0, win_rate_vs_competitor_pct=1.0,
                      feature_gap_mention_rate_pct=0.0, differentiation_score=1.0,
                      late_stage_competitive_loss_pct=0.0, competitive_deal_pct=0.0,
                      executive_alignment_pct=1.0)
        assert p == CompPattern.multi_vendor_spread

    def test_multi_vendor_spread_not_triggered_low_mv(self):
        p = self._pat(multi_vendor_eval_pct=0.64, displacement_win_rate_pct=0.20,
                      avg_discount_in_comp_deals_pct=0.0, win_rate_vs_competitor_pct=1.0,
                      feature_gap_mention_rate_pct=0.0, differentiation_score=1.0,
                      late_stage_competitive_loss_pct=0.0, competitive_deal_pct=0.0,
                      executive_alignment_pct=1.0)
        assert p != CompPattern.multi_vendor_spread

    def test_multi_vendor_spread_not_triggered_high_disp(self):
        p = self._pat(multi_vendor_eval_pct=0.70, displacement_win_rate_pct=0.26,
                      avg_discount_in_comp_deals_pct=0.0, win_rate_vs_competitor_pct=1.0,
                      feature_gap_mention_rate_pct=0.0, differentiation_score=1.0,
                      late_stage_competitive_loss_pct=0.0, competitive_deal_pct=0.0,
                      executive_alignment_pct=1.0)
        assert p != CompPattern.multi_vendor_spread

    # none
    def test_none_pattern_default(self):
        p = self._pat()  # all mid-range neutral defaults
        assert p == CompPattern.none

    # priority (price_surrender checked first)
    def test_price_surrender_takes_priority_over_feature_gap(self):
        p = self._pat(avg_discount_in_comp_deals_pct=0.30, win_rate_vs_competitor_pct=0.30,
                      feature_gap_mention_rate_pct=0.50, differentiation_score=0.30,
                      late_stage_competitive_loss_pct=0.0, competitive_deal_pct=0.0,
                      executive_alignment_pct=1.0, multi_vendor_eval_pct=0.0,
                      displacement_win_rate_pct=1.0)
        assert p == CompPattern.price_surrender


# ══════════════════════════════════════════════════════════════════════════════
# 8.  has_comp_gap FLAG CONDITIONS
# ══════════════════════════════════════════════════════════════════════════════

class TestHasCompGap:
    def _gap(self, composite, **kw):
        inp = make_input(**kw)
        return engine()._has_gap(inp, composite)

    def test_gap_true_when_composite_ge_40(self):
        assert self._gap(40) is True

    def test_gap_true_when_composite_above_40(self):
        assert self._gap(60) is True

    def test_gap_false_by_composite_alone_when_below_40(self):
        # composite < 40, win_rate > 0.45, late_stage < 0.30 → False
        assert self._gap(39,
                         win_rate_vs_competitor_pct=0.50,
                         late_stage_competitive_loss_pct=0.10) is False

    def test_gap_true_when_win_rate_exactly_045(self):
        assert self._gap(0, win_rate_vs_competitor_pct=0.45,
                         late_stage_competitive_loss_pct=0.10) is True

    def test_gap_true_when_win_rate_below_045(self):
        assert self._gap(0, win_rate_vs_competitor_pct=0.30,
                         late_stage_competitive_loss_pct=0.10) is True

    def test_gap_false_when_win_rate_above_045(self):
        assert self._gap(0, win_rate_vs_competitor_pct=0.46,
                         late_stage_competitive_loss_pct=0.10) is False

    def test_gap_true_when_late_stage_exactly_030(self):
        assert self._gap(0, win_rate_vs_competitor_pct=0.80,
                         late_stage_competitive_loss_pct=0.30) is True

    def test_gap_true_when_late_stage_above_030(self):
        assert self._gap(0, win_rate_vs_competitor_pct=0.80,
                         late_stage_competitive_loss_pct=0.50) is True

    def test_gap_false_when_late_stage_below_030(self):
        assert self._gap(0, win_rate_vs_competitor_pct=0.80,
                         late_stage_competitive_loss_pct=0.20) is False

    def test_gap_true_composite_dominates_even_good_inputs(self):
        assert self._gap(50,
                         win_rate_vs_competitor_pct=0.90,
                         late_stage_competitive_loss_pct=0.01) is True


# ══════════════════════════════════════════════════════════════════════════════
# 9.  requires_comp_coaching FLAG CONDITIONS
# ══════════════════════════════════════════════════════════════════════════════

class TestRequiresCompCoaching:
    def _coaching(self, composite, **kw):
        inp = make_input(**kw)
        return engine()._requires_coaching(inp, composite)

    def test_coaching_true_when_composite_ge_25(self):
        assert self._coaching(25,
                              battle_card_usage_rate_pct=0.90,
                              differentiation_score=0.90) is True

    def test_coaching_true_when_composite_above_25(self):
        assert self._coaching(50,
                              battle_card_usage_rate_pct=0.90,
                              differentiation_score=0.90) is True

    def test_coaching_false_by_composite_alone_when_below_25(self):
        # composite < 25, bc_usage > 0.45, diff_score > 0.50 → False
        assert self._coaching(24,
                              battle_card_usage_rate_pct=0.90,
                              differentiation_score=0.90) is False

    def test_coaching_true_when_battle_card_exactly_045(self):
        assert self._coaching(0,
                              battle_card_usage_rate_pct=0.45,
                              differentiation_score=0.90) is True

    def test_coaching_true_when_battle_card_below_045(self):
        assert self._coaching(0,
                              battle_card_usage_rate_pct=0.20,
                              differentiation_score=0.90) is True

    def test_coaching_false_when_battle_card_above_045(self):
        assert self._coaching(0,
                              battle_card_usage_rate_pct=0.46,
                              differentiation_score=0.90) is False

    def test_coaching_true_when_diff_score_exactly_050(self):
        assert self._coaching(0,
                              battle_card_usage_rate_pct=0.90,
                              differentiation_score=0.50) is True

    def test_coaching_true_when_diff_score_below_050(self):
        assert self._coaching(0,
                              battle_card_usage_rate_pct=0.90,
                              differentiation_score=0.30) is True

    def test_coaching_false_when_diff_score_above_050(self):
        assert self._coaching(0,
                              battle_card_usage_rate_pct=0.90,
                              differentiation_score=0.51) is False

    def test_coaching_true_composite_dominates(self):
        assert self._coaching(30,
                              battle_card_usage_rate_pct=0.90,
                              differentiation_score=0.90) is True


# ══════════════════════════════════════════════════════════════════════════════
# 10. estimated_pipeline_at_risk_usd FORMULA
# ══════════════════════════════════════════════════════════════════════════════

class TestPipelineAtRisk:
    def _risk_usd(self, composite, **kw):
        inp = make_input(**kw)
        return engine()._pipeline_at_risk(inp, composite)

    def test_zero_pipeline_gives_zero(self):
        result = self._risk_usd(50, total_pipeline_at_risk_usd=0.0,
                                win_rate_vs_competitor_pct=0.50)
        assert result == 0.0

    def test_zero_composite_gives_zero(self):
        result = self._risk_usd(0, total_pipeline_at_risk_usd=1_000_000.0,
                                win_rate_vs_competitor_pct=0.50)
        assert result == 0.0

    def test_formula_correctness(self):
        # loss_prob = min(1.0, (1-0.40)*(50/100)) = 0.60*0.50 = 0.30
        result = self._risk_usd(50, win_rate_vs_competitor_pct=0.40,
                                total_pipeline_at_risk_usd=1_000_000.0)
        assert result == pytest.approx(300_000.0, abs=0.01)

    def test_loss_prob_capped_at_1(self):
        # (1-0.0)*(200/100)=2.0 → capped at 1.0 → full pipeline
        result = self._risk_usd(200, win_rate_vs_competitor_pct=0.0,
                                total_pipeline_at_risk_usd=500_000.0)
        assert result == pytest.approx(500_000.0, abs=0.01)

    def test_result_rounded_to_2dp(self):
        # (1-0.33)*(33/100)=0.67*0.33=0.2211
        result = self._risk_usd(33, win_rate_vs_competitor_pct=0.33,
                                total_pipeline_at_risk_usd=100.0)
        expected = round(100.0 * min(1.0, 0.67 * 0.33), 2)
        assert result == pytest.approx(expected, abs=0.01)

    def test_full_win_rate_gives_zero(self):
        # loss_prob = min(1.0, (1-1.0)*(60/100)) = 0.0
        result = self._risk_usd(60, win_rate_vs_competitor_pct=1.0,
                                total_pipeline_at_risk_usd=1_000_000.0)
        assert result == 0.0

    def test_pipeline_at_risk_is_float(self):
        result = self._risk_usd(50, win_rate_vs_competitor_pct=0.50,
                                total_pipeline_at_risk_usd=200_000.0)
        assert isinstance(result, float)

    def test_large_pipeline(self):
        result = self._risk_usd(80, win_rate_vs_competitor_pct=0.20,
                                total_pipeline_at_risk_usd=10_000_000.0)
        expected = round(10_000_000.0 * min(1.0, 0.80 * 0.80), 2)
        assert result == pytest.approx(expected, abs=0.01)


# ══════════════════════════════════════════════════════════════════════════════
# 11. _signal OUTPUT FOR LOW AND HIGH COMPOSITE
# ══════════════════════════════════════════════════════════════════════════════

class TestSignalOutput:
    def _signal(self, composite, pattern=CompPattern.none, **kw):
        inp = make_input(**kw)
        return engine()._signal(inp, pattern, composite)

    def test_low_composite_returns_strong_message(self):
        sig = self._signal(19)
        assert "strong" in sig.lower()

    def test_composite_below_20_exact_string(self):
        sig = self._signal(0)
        assert sig == (
            "Competitive position strong — win rate, positioning, "
            "battle readiness, and executive alignment within benchmarks"
        )

    def test_composite_exactly_19_is_low(self):
        sig = self._signal(19)
        assert "strong" in sig.lower()

    def test_composite_exactly_20_is_high_format(self):
        sig = self._signal(20, pattern=CompPattern.none,
                           win_rate_vs_competitor_pct=0.55,
                           avg_discount_in_comp_deals_pct=0.10,
                           late_stage_competitive_loss_pct=0.10)
        assert "—" in sig

    def test_high_composite_contains_win_rate_pct(self):
        sig = self._signal(50, pattern=CompPattern.none,
                           win_rate_vs_competitor_pct=0.60,
                           avg_discount_in_comp_deals_pct=0.15,
                           late_stage_competitive_loss_pct=0.20)
        assert "60%" in sig

    def test_high_composite_contains_discount_pct(self):
        sig = self._signal(50, pattern=CompPattern.none,
                           win_rate_vs_competitor_pct=0.50,
                           avg_discount_in_comp_deals_pct=0.25,
                           late_stage_competitive_loss_pct=0.20)
        assert "25%" in sig

    def test_high_composite_contains_late_pct(self):
        sig = self._signal(50, pattern=CompPattern.none,
                           win_rate_vs_competitor_pct=0.50,
                           avg_discount_in_comp_deals_pct=0.10,
                           late_stage_competitive_loss_pct=0.35)
        assert "35%" in sig

    def test_high_composite_contains_composite_int(self):
        sig = self._signal(50, pattern=CompPattern.none,
                           win_rate_vs_competitor_pct=0.50,
                           avg_discount_in_comp_deals_pct=0.10,
                           late_stage_competitive_loss_pct=0.20)
        assert "50" in sig

    def test_pattern_label_price_surrender(self):
        sig = self._signal(50, pattern=CompPattern.price_surrender,
                           win_rate_vs_competitor_pct=0.50,
                           avg_discount_in_comp_deals_pct=0.10,
                           late_stage_competitive_loss_pct=0.20)
        assert "Price surrender" in sig

    def test_pattern_label_feature_gap_concession(self):
        sig = self._signal(50, pattern=CompPattern.feature_gap_concession,
                           win_rate_vs_competitor_pct=0.50,
                           avg_discount_in_comp_deals_pct=0.10,
                           late_stage_competitive_loss_pct=0.20)
        assert "Feature-gap concession" in sig

    def test_pattern_label_late_entry_loss(self):
        sig = self._signal(50, pattern=CompPattern.late_entry_loss,
                           win_rate_vs_competitor_pct=0.50,
                           avg_discount_in_comp_deals_pct=0.10,
                           late_stage_competitive_loss_pct=0.20)
        assert "Late-entry loss" in sig

    def test_pattern_label_relationship_deficit(self):
        sig = self._signal(50, pattern=CompPattern.relationship_deficit,
                           win_rate_vs_competitor_pct=0.50,
                           avg_discount_in_comp_deals_pct=0.10,
                           late_stage_competitive_loss_pct=0.20)
        assert "Relationship deficit" in sig

    def test_pattern_label_multi_vendor_spread(self):
        sig = self._signal(50, pattern=CompPattern.multi_vendor_spread,
                           win_rate_vs_competitor_pct=0.50,
                           avg_discount_in_comp_deals_pct=0.10,
                           late_stage_competitive_loss_pct=0.20)
        assert "Multi-vendor spread" in sig

    def test_signal_is_string(self):
        assert isinstance(self._signal(50), str)

    def test_signal_low_is_string(self):
        assert isinstance(self._signal(5), str)


# ══════════════════════════════════════════════════════════════════════════════
# 12. assess() INTEGRATION TEST
# ══════════════════════════════════════════════════════════════════════════════

class TestAssessIntegration:
    def test_returns_comp_result(self):
        result = engine().assess(make_input())
        assert isinstance(result, CompResult)

    def test_rep_id_propagated(self):
        result = engine().assess(make_input(rep_id="RX1"))
        assert result.rep_id == "RX1"

    def test_region_propagated(self):
        result = engine().assess(make_input(region="East"))
        assert result.region == "East"

    def test_composite_within_range(self):
        result = engine().assess(make_input())
        assert 0.0 <= result.comp_composite <= 100.0

    def test_win_rate_score_within_range(self):
        result = engine().assess(make_input())
        assert 0.0 <= result.win_rate_score <= 100.0

    def test_positioning_score_within_range(self):
        result = engine().assess(make_input())
        assert 0.0 <= result.positioning_score <= 100.0

    def test_battle_readiness_score_within_range(self):
        result = engine().assess(make_input())
        assert 0.0 <= result.battle_readiness_score <= 100.0

    def test_relationship_advantage_score_within_range(self):
        result = engine().assess(make_input())
        assert 0.0 <= result.relationship_advantage_score <= 100.0

    def test_comp_risk_is_enum(self):
        result = engine().assess(make_input())
        assert isinstance(result.comp_risk, CompRisk)

    def test_comp_pattern_is_enum(self):
        result = engine().assess(make_input())
        assert isinstance(result.comp_pattern, CompPattern)

    def test_comp_severity_is_enum(self):
        result = engine().assess(make_input())
        assert isinstance(result.comp_severity, CompSeverity)

    def test_recommended_action_is_enum(self):
        result = engine().assess(make_input())
        assert isinstance(result.recommended_action, CompAction)

    def test_has_comp_gap_is_bool(self):
        result = engine().assess(make_input())
        assert isinstance(result.has_comp_gap, bool)

    def test_requires_comp_coaching_is_bool(self):
        result = engine().assess(make_input())
        assert isinstance(result.requires_comp_coaching, bool)

    def test_pipeline_at_risk_is_float(self):
        result = engine().assess(make_input())
        assert isinstance(result.estimated_pipeline_at_risk_usd, float)

    def test_signal_is_string(self):
        result = engine().assess(make_input())
        assert isinstance(result.comp_signal, str)

    def test_result_stored_in_engine(self):
        e = SalesCompetitiveIntelligenceEngine()
        e.assess(make_input())
        assert len(e._results) == 1

    def test_worst_case_input_critical_risk(self):
        inp = make_input(
            win_rate_vs_competitor_pct=0.10,
            avg_discount_in_comp_deals_pct=0.50,
            feature_gap_mention_rate_pct=0.80,
            battle_card_usage_rate_pct=0.05,
            late_stage_competitive_loss_pct=0.70,
            displacement_win_rate_pct=0.05,
            proof_of_concept_win_rate_pct=0.10,
            executive_alignment_pct=0.05,
            multi_vendor_eval_pct=0.90,
            competitor_mention_per_call=5.0,
            differentiation_score=0.10,
            reference_customer_usage_rate=0.05,
        )
        result = engine().assess(inp)
        assert result.comp_risk == CompRisk.critical

    def test_best_case_input_low_risk(self):
        inp = make_input(
            win_rate_vs_competitor_pct=0.90,
            avg_discount_in_comp_deals_pct=0.0,
            feature_gap_mention_rate_pct=0.0,
            battle_card_usage_rate_pct=1.0,
            late_stage_competitive_loss_pct=0.0,
            displacement_win_rate_pct=0.90,
            proof_of_concept_win_rate_pct=0.90,
            executive_alignment_pct=0.90,
            multi_vendor_eval_pct=0.0,
            competitor_mention_per_call=0.0,
            differentiation_score=0.90,
            reference_customer_usage_rate=0.90,
        )
        result = engine().assess(inp)
        assert result.comp_risk == CompRisk.low

    def test_assess_accumulates_results_across_calls(self):
        e = SalesCompetitiveIntelligenceEngine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B"))
        assert len(e._results) == 2


# ══════════════════════════════════════════════════════════════════════════════
# 13. assess_batch()
# ══════════════════════════════════════════════════════════════════════════════

class TestAssessBatch:
    def test_returns_list(self):
        e = SalesCompetitiveIntelligenceEngine()
        results = e.assess_batch([make_input(rep_id="A"), make_input(rep_id="B")])
        assert isinstance(results, list)

    def test_returns_correct_count(self):
        e = SalesCompetitiveIntelligenceEngine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = e.assess_batch(inputs)
        assert len(results) == 5

    def test_empty_batch_returns_empty_list(self):
        e = SalesCompetitiveIntelligenceEngine()
        assert e.assess_batch([]) == []

    def test_all_items_are_comp_result(self):
        e = SalesCompetitiveIntelligenceEngine()
        results = e.assess_batch([make_input(rep_id="X"), make_input(rep_id="Y")])
        assert all(isinstance(r, CompResult) for r in results)

    def test_rep_ids_preserved(self):
        e = SalesCompetitiveIntelligenceEngine()
        results = e.assess_batch([make_input(rep_id="ALPHA"), make_input(rep_id="BETA")])
        assert results[0].rep_id == "ALPHA"
        assert results[1].rep_id == "BETA"

    def test_batch_accumulates_in_results_store(self):
        e = SalesCompetitiveIntelligenceEngine()
        e.assess_batch([make_input(rep_id="P"), make_input(rep_id="Q"), make_input(rep_id="R")])
        assert len(e._results) == 3

    def test_single_item_batch(self):
        e = SalesCompetitiveIntelligenceEngine()
        results = e.assess_batch([make_input(rep_id="SOLO")])
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"

    def test_batch_then_single_assess(self):
        e = SalesCompetitiveIntelligenceEngine()
        e.assess_batch([make_input(rep_id="B1"), make_input(rep_id="B2")])
        e.assess(make_input(rep_id="S1"))
        assert len(e._results) == 3


# ══════════════════════════════════════════════════════════════════════════════
# 14. summary() – EMPTY AND POPULATED
# ══════════════════════════════════════════════════════════════════════════════

class TestSummaryEmpty:
    def _empty_summary(self):
        return SalesCompetitiveIntelligenceEngine().summary()

    def test_returns_dict(self):
        assert isinstance(self._empty_summary(), dict)

    def test_exactly_13_keys(self):
        assert len(self._empty_summary()) == 13

    def test_key_total(self):
        assert "total" in self._empty_summary()

    def test_key_risk_counts(self):
        assert "risk_counts" in self._empty_summary()

    def test_key_pattern_counts(self):
        assert "pattern_counts" in self._empty_summary()

    def test_key_severity_counts(self):
        assert "severity_counts" in self._empty_summary()

    def test_key_action_counts(self):
        assert "action_counts" in self._empty_summary()

    def test_key_avg_comp_composite(self):
        assert "avg_comp_composite" in self._empty_summary()

    def test_key_comp_gap_count(self):
        assert "comp_gap_count" in self._empty_summary()

    def test_key_coaching_count(self):
        assert "coaching_count" in self._empty_summary()

    def test_key_avg_win_rate_score(self):
        assert "avg_win_rate_score" in self._empty_summary()

    def test_key_avg_positioning_score(self):
        assert "avg_positioning_score" in self._empty_summary()

    def test_key_avg_battle_readiness_score(self):
        assert "avg_battle_readiness_score" in self._empty_summary()

    def test_key_avg_relationship_advantage_score(self):
        assert "avg_relationship_advantage_score" in self._empty_summary()

    def test_key_total_estimated_pipeline_at_risk_usd(self):
        assert "total_estimated_pipeline_at_risk_usd" in self._empty_summary()

    def test_total_is_zero(self):
        assert self._empty_summary()["total"] == 0

    def test_risk_counts_empty_dict(self):
        assert self._empty_summary()["risk_counts"] == {}

    def test_pattern_counts_empty_dict(self):
        assert self._empty_summary()["pattern_counts"] == {}

    def test_severity_counts_empty_dict(self):
        assert self._empty_summary()["severity_counts"] == {}

    def test_action_counts_empty_dict(self):
        assert self._empty_summary()["action_counts"] == {}

    def test_avg_comp_composite_zero(self):
        assert self._empty_summary()["avg_comp_composite"] == 0.0

    def test_comp_gap_count_zero(self):
        assert self._empty_summary()["comp_gap_count"] == 0

    def test_coaching_count_zero(self):
        assert self._empty_summary()["coaching_count"] == 0

    def test_total_pipeline_zero(self):
        assert self._empty_summary()["total_estimated_pipeline_at_risk_usd"] == 0.0


class TestSummaryPopulated:
    def _make_engine_with_results(self, n=3):
        e = SalesCompetitiveIntelligenceEngine()
        for i in range(n):
            e.assess(make_input(rep_id=f"REP-{i}"))
        return e

    def test_total_matches_count(self):
        e = self._make_engine_with_results(4)
        assert e.summary()["total"] == 4

    def test_risk_counts_sums_to_total(self):
        e = self._make_engine_with_results(5)
        s = e.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_pattern_counts_sums_to_total(self):
        e = self._make_engine_with_results(5)
        s = e.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_severity_counts_sums_to_total(self):
        e = self._make_engine_with_results(5)
        s = e.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_action_counts_sums_to_total(self):
        e = self._make_engine_with_results(5)
        s = e.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_avg_comp_composite_is_float(self):
        e = self._make_engine_with_results(3)
        assert isinstance(e.summary()["avg_comp_composite"], float)

    def test_comp_gap_count_le_total(self):
        e = self._make_engine_with_results(6)
        s = e.summary()
        assert s["comp_gap_count"] <= s["total"]

    def test_coaching_count_le_total(self):
        e = self._make_engine_with_results(6)
        s = e.summary()
        assert s["coaching_count"] <= s["total"]

    def test_total_pipeline_is_float(self):
        e = self._make_engine_with_results(3)
        assert isinstance(e.summary()["total_estimated_pipeline_at_risk_usd"], float)

    def test_risk_counts_keys_are_valid_risk_values(self):
        e = self._make_engine_with_results(10)
        valid = {r.value for r in CompRisk}
        for k in e.summary()["risk_counts"]:
            assert k in valid

    def test_pattern_counts_keys_are_valid_pattern_values(self):
        e = self._make_engine_with_results(10)
        valid = {p.value for p in CompPattern}
        for k in e.summary()["pattern_counts"]:
            assert k in valid

    def test_severity_counts_keys_are_valid_severity_values(self):
        e = self._make_engine_with_results(10)
        valid = {s.value for s in CompSeverity}
        for k in e.summary()["severity_counts"]:
            assert k in valid

    def test_action_counts_keys_are_valid_action_values(self):
        e = self._make_engine_with_results(10)
        valid = {a.value for a in CompAction}
        for k in e.summary()["action_counts"]:
            assert k in valid

    def test_avg_composite_is_reasonable(self):
        e = self._make_engine_with_results(5)
        avg = e.summary()["avg_comp_composite"]
        assert 0.0 <= avg <= 100.0

    def test_mixed_inputs_summary_total(self):
        e = SalesCompetitiveIntelligenceEngine()
        # a bad rep
        e.assess(make_input(rep_id="BAD",
                            win_rate_vs_competitor_pct=0.10,
                            avg_discount_in_comp_deals_pct=0.50))
        # a good rep
        e.assess(make_input(rep_id="GOOD",
                            win_rate_vs_competitor_pct=0.90,
                            avg_discount_in_comp_deals_pct=0.0))
        assert e.summary()["total"] == 2


# ══════════════════════════════════════════════════════════════════════════════
# 15. EDGE CASES
# ══════════════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    def test_all_zero_floats_does_not_crash(self):
        inp = make_input(
            win_rate_vs_competitor_pct=0.0,
            competitive_deal_pct=0.0,
            avg_discount_in_comp_deals_pct=0.0,
            price_objection_rate_pct=0.0,
            feature_gap_mention_rate_pct=0.0,
            battle_card_usage_rate_pct=0.0,
            late_stage_competitive_loss_pct=0.0,
            displacement_win_rate_pct=0.0,
            proof_of_concept_win_rate_pct=0.0,
            avg_cycle_len_comp_deals_days=0.0,
            multi_vendor_eval_pct=0.0,
            executive_alignment_pct=0.0,
            competitor_mention_per_call=0.0,
            differentiation_score=0.0,
            reference_customer_usage_rate=0.0,
            total_competitive_deals=0,
            avg_deal_value_usd=0.0,
            total_pipeline_at_risk_usd=0.0,
        )
        result = engine().assess(inp)
        assert isinstance(result, CompResult)

    def test_all_max_floats_does_not_crash(self):
        inp = make_input(
            win_rate_vs_competitor_pct=1.0,
            competitive_deal_pct=1.0,
            avg_discount_in_comp_deals_pct=1.0,
            price_objection_rate_pct=1.0,
            feature_gap_mention_rate_pct=1.0,
            battle_card_usage_rate_pct=1.0,
            late_stage_competitive_loss_pct=1.0,
            displacement_win_rate_pct=1.0,
            proof_of_concept_win_rate_pct=1.0,
            avg_cycle_len_comp_deals_days=365.0,
            multi_vendor_eval_pct=1.0,
            executive_alignment_pct=1.0,
            competitor_mention_per_call=10.0,
            differentiation_score=1.0,
            reference_customer_usage_rate=1.0,
            total_competitive_deals=9999,
            avg_deal_value_usd=1_000_000.0,
            total_pipeline_at_risk_usd=100_000_000.0,
        )
        result = engine().assess(inp)
        assert isinstance(result, CompResult)

    def test_composite_never_exceeds_100(self):
        inp = make_input(
            win_rate_vs_competitor_pct=0.0,
            avg_discount_in_comp_deals_pct=1.0,
            feature_gap_mention_rate_pct=1.0,
            battle_card_usage_rate_pct=0.0,
            late_stage_competitive_loss_pct=1.0,
            displacement_win_rate_pct=0.0,
            proof_of_concept_win_rate_pct=0.0,
            executive_alignment_pct=0.0,
            multi_vendor_eval_pct=1.0,
            competitor_mention_per_call=10.0,
            differentiation_score=0.0,
            reference_customer_usage_rate=0.0,
        )
        result = engine().assess(inp)
        assert result.comp_composite <= 100.0

    def test_composite_never_below_zero(self):
        result = engine().assess(make_input(
            win_rate_vs_competitor_pct=1.0,
            avg_discount_in_comp_deals_pct=0.0,
            feature_gap_mention_rate_pct=0.0,
            battle_card_usage_rate_pct=1.0,
            late_stage_competitive_loss_pct=0.0,
            displacement_win_rate_pct=1.0,
            proof_of_concept_win_rate_pct=1.0,
            executive_alignment_pct=1.0,
            multi_vendor_eval_pct=0.0,
            competitor_mention_per_call=0.0,
            differentiation_score=1.0,
            reference_customer_usage_rate=1.0,
        ))
        assert result.comp_composite >= 0.0

    def test_pipeline_at_risk_never_exceeds_total(self):
        inp = make_input(
            win_rate_vs_competitor_pct=0.0,
            total_pipeline_at_risk_usd=500_000.0,
        )
        result = engine().assess(inp)
        assert result.estimated_pipeline_at_risk_usd <= 500_000.0

    def test_pipeline_at_risk_never_negative(self):
        result = engine().assess(make_input(
            win_rate_vs_competitor_pct=1.0,
            total_pipeline_at_risk_usd=1_000_000.0,
        ))
        assert result.estimated_pipeline_at_risk_usd >= 0.0

    def test_single_char_rep_id(self):
        result = engine().assess(make_input(rep_id="A"))
        assert result.rep_id == "A"

    def test_empty_string_rep_id(self):
        result = engine().assess(make_input(rep_id=""))
        assert result.rep_id == ""

    def test_boundary_composite_exactly_60_is_critical(self):
        e = SalesCompetitiveIntelligenceEngine()
        assert e._risk(60.0) == CompRisk.critical

    def test_boundary_composite_599_is_high(self):
        e = SalesCompetitiveIntelligenceEngine()
        assert e._risk(59.9) == CompRisk.high

    def test_boundary_composite_exactly_40_is_high(self):
        e = SalesCompetitiveIntelligenceEngine()
        assert e._risk(40.0) == CompRisk.high

    def test_boundary_composite_399_is_moderate(self):
        e = SalesCompetitiveIntelligenceEngine()
        assert e._risk(39.9) == CompRisk.moderate

    def test_boundary_composite_exactly_20_is_moderate(self):
        e = SalesCompetitiveIntelligenceEngine()
        assert e._risk(20.0) == CompRisk.moderate

    def test_boundary_composite_199_is_low(self):
        e = SalesCompetitiveIntelligenceEngine()
        assert e._risk(19.9) == CompRisk.low

    def test_to_dict_stable_between_calls(self):
        r = engine().assess(make_input())
        d1 = r.to_dict()
        d2 = r.to_dict()
        assert d1 == d2

    def test_new_engine_has_empty_results(self):
        e = SalesCompetitiveIntelligenceEngine()
        assert e._results == []

    def test_multiple_engines_independent(self):
        e1 = SalesCompetitiveIntelligenceEngine()
        e2 = SalesCompetitiveIntelligenceEngine()
        e1.assess(make_input(rep_id="E1"))
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_zero_total_competitive_deals(self):
        result = engine().assess(make_input(total_competitive_deals=0))
        assert isinstance(result, CompResult)

    def test_very_large_competitor_mention(self):
        result = engine().assess(make_input(competitor_mention_per_call=999.9))
        assert result.relationship_advantage_score <= 100.0

    def test_assess_result_matches_manual_calculation(self):
        e = SalesCompetitiveIntelligenceEngine()
        inp = make_input(
            win_rate_vs_competitor_pct=0.66,    # no score
            displacement_win_rate_pct=0.50,      # no score
            late_stage_competitive_loss_pct=0.10, # no score
            avg_discount_in_comp_deals_pct=0.10,  # no score
            feature_gap_mention_rate_pct=0.20,    # no score
            differentiation_score=0.70,           # no score
            battle_card_usage_rate_pct=0.80,      # no score
            proof_of_concept_win_rate_pct=0.60,   # no score
            reference_customer_usage_rate=0.50,   # no score
            executive_alignment_pct=0.75,         # no score
            multi_vendor_eval_pct=0.30,           # no score
            competitor_mention_per_call=1.0,      # no score
        )
        result = e.assess(inp)
        # All sub-scores should be 0
        assert result.win_rate_score == 0.0
        assert result.positioning_score == 0.0
        assert result.battle_readiness_score == 0.0
        assert result.relationship_advantage_score == 0.0
        assert result.comp_composite == 0.0
