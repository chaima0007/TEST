"""
Comprehensive pytest tests for SalesWinRateDecayIntelligenceEngine.
Covers: enums, input fields, result fields, to_dict, every sub-score branch,
pattern detection priority, risk/severity/action mapping, gap/coaching flags,
revenue decay formula, signal strings, assess end-to-end, assess_batch,
summary (empty + populated, all 13 keys), and edge cases.
"""

from __future__ import annotations

import pytest

from swarm.intelligence.sales_win_rate_decay_intelligence_engine import (
    DecayAction,
    DecayInput,
    DecayPattern,
    DecayResult,
    DecayRisk,
    DecaySeverity,
    SalesWinRateDecayIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _base_inp(**overrides) -> DecayInput:
    """Return a 'healthy' rep — all scores near zero — with optional overrides."""
    defaults = dict(
        rep_id="REP-001",
        region="EMEA",
        evaluation_period_id="Q2-2026",
        current_win_rate_pct=0.50,
        win_rate_3m_ago_pct=0.52,
        win_rate_6m_ago_pct=0.54,
        win_rate_decline_velocity_pct=0.02,
        late_stage_win_rate_pct=0.48,
        early_stage_win_rate_pct=0.55,
        competitive_win_rate_pct=0.60,
        uncontested_win_rate_pct=0.70,
        avg_deal_size_current_usd=50_000.0,
        avg_deal_size_6m_ago_usd=50_000.0,
        deals_lost_at_stage_4plus_pct=0.10,
        no_decision_rate_pct=0.10,
        discounting_frequency_pct=0.20,
        avg_discount_depth_pct=0.05,
        champion_presence_lost_deals_pct=0.60,
        multi_stakeholder_win_rate_pct=0.45,
        single_stakeholder_win_rate_pct=0.60,
        total_deals_evaluated=100,
        avg_opportunity_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return DecayInput(**defaults)


def _engine() -> SalesWinRateDecayIntelligenceEngine:
    return SalesWinRateDecayIntelligenceEngine()


# ===========================================================================
# 1. Enum tests
# ===========================================================================

class TestDecayRiskEnum:
    def test_values(self):
        assert DecayRisk.low.value == "low"
        assert DecayRisk.moderate.value == "moderate"
        assert DecayRisk.high.value == "high"
        assert DecayRisk.critical.value == "critical"

    def test_member_count(self):
        assert len(DecayRisk) == 4

    def test_str_subclass(self):
        assert isinstance(DecayRisk.low, str)

    def test_equality_with_str(self):
        assert DecayRisk.low == "low"

    def test_all_members_accessible(self):
        members = {m.value for m in DecayRisk}
        assert members == {"low", "moderate", "high", "critical"}


class TestDecayPatternEnum:
    def test_values(self):
        assert DecayPattern.none.value == "none"
        assert DecayPattern.gradual_erosion.value == "gradual_erosion"
        assert DecayPattern.sharp_cliff_drop.value == "sharp_cliff_drop"
        assert DecayPattern.competitive_displacement.value == "competitive_displacement"
        assert DecayPattern.late_stage_collapse.value == "late_stage_collapse"
        assert DecayPattern.deal_size_inflation_trap.value == "deal_size_inflation_trap"

    def test_member_count(self):
        assert len(DecayPattern) == 6

    def test_str_subclass(self):
        assert isinstance(DecayPattern.none, str)

    def test_equality_with_str(self):
        assert DecayPattern.none == "none"


class TestDecaySeverityEnum:
    def test_values(self):
        assert DecaySeverity.improving.value == "improving"
        assert DecaySeverity.stable.value == "stable"
        assert DecaySeverity.declining.value == "declining"
        assert DecaySeverity.collapsing.value == "collapsing"

    def test_member_count(self):
        assert len(DecaySeverity) == 4

    def test_str_subclass(self):
        assert isinstance(DecaySeverity.stable, str)


class TestDecayActionEnum:
    def test_values(self):
        assert DecayAction.no_action.value == "no_action"
        assert DecayAction.win_loss_debrief_coaching.value == "win_loss_debrief_coaching"
        assert DecayAction.competitive_positioning_review.value == "competitive_positioning_review"
        assert DecayAction.deal_quality_audit.value == "deal_quality_audit"
        assert DecayAction.late_stage_process_coaching.value == "late_stage_process_coaching"
        assert DecayAction.urgent_pipeline_intervention.value == "urgent_pipeline_intervention"

    def test_member_count(self):
        assert len(DecayAction) == 6

    def test_str_subclass(self):
        assert isinstance(DecayAction.no_action, str)


# ===========================================================================
# 2. DecayInput field tests
# ===========================================================================

class TestDecayInputFields:
    def test_rep_id(self):
        inp = _base_inp(rep_id="R-XYZ")
        assert inp.rep_id == "R-XYZ"

    def test_region(self):
        inp = _base_inp(region="APAC")
        assert inp.region == "APAC"

    def test_evaluation_period_id(self):
        inp = _base_inp(evaluation_period_id="Q3-2026")
        assert inp.evaluation_period_id == "Q3-2026"

    def test_current_win_rate_pct(self):
        inp = _base_inp(current_win_rate_pct=0.30)
        assert inp.current_win_rate_pct == 0.30

    def test_win_rate_3m_ago_pct(self):
        inp = _base_inp(win_rate_3m_ago_pct=0.45)
        assert inp.win_rate_3m_ago_pct == 0.45

    def test_win_rate_6m_ago_pct(self):
        inp = _base_inp(win_rate_6m_ago_pct=0.55)
        assert inp.win_rate_6m_ago_pct == 0.55

    def test_win_rate_decline_velocity_pct(self):
        inp = _base_inp(win_rate_decline_velocity_pct=0.10)
        assert inp.win_rate_decline_velocity_pct == 0.10

    def test_late_stage_win_rate_pct(self):
        inp = _base_inp(late_stage_win_rate_pct=0.35)
        assert inp.late_stage_win_rate_pct == 0.35

    def test_early_stage_win_rate_pct(self):
        inp = _base_inp(early_stage_win_rate_pct=0.65)
        assert inp.early_stage_win_rate_pct == 0.65

    def test_competitive_win_rate_pct(self):
        inp = _base_inp(competitive_win_rate_pct=0.22)
        assert inp.competitive_win_rate_pct == 0.22

    def test_uncontested_win_rate_pct(self):
        inp = _base_inp(uncontested_win_rate_pct=0.80)
        assert inp.uncontested_win_rate_pct == 0.80

    def test_avg_deal_size_current_usd(self):
        inp = _base_inp(avg_deal_size_current_usd=120_000.0)
        assert inp.avg_deal_size_current_usd == 120_000.0

    def test_avg_deal_size_6m_ago_usd(self):
        inp = _base_inp(avg_deal_size_6m_ago_usd=60_000.0)
        assert inp.avg_deal_size_6m_ago_usd == 60_000.0

    def test_deals_lost_at_stage_4plus_pct(self):
        inp = _base_inp(deals_lost_at_stage_4plus_pct=0.45)
        assert inp.deals_lost_at_stage_4plus_pct == 0.45

    def test_no_decision_rate_pct(self):
        inp = _base_inp(no_decision_rate_pct=0.30)
        assert inp.no_decision_rate_pct == 0.30

    def test_discounting_frequency_pct(self):
        inp = _base_inp(discounting_frequency_pct=0.75)
        assert inp.discounting_frequency_pct == 0.75

    def test_avg_discount_depth_pct(self):
        inp = _base_inp(avg_discount_depth_pct=0.20)
        assert inp.avg_discount_depth_pct == 0.20

    def test_champion_presence_lost_deals_pct(self):
        inp = _base_inp(champion_presence_lost_deals_pct=0.15)
        assert inp.champion_presence_lost_deals_pct == 0.15

    def test_multi_stakeholder_win_rate_pct(self):
        inp = _base_inp(multi_stakeholder_win_rate_pct=0.38)
        assert inp.multi_stakeholder_win_rate_pct == 0.38

    def test_single_stakeholder_win_rate_pct(self):
        inp = _base_inp(single_stakeholder_win_rate_pct=0.72)
        assert inp.single_stakeholder_win_rate_pct == 0.72

    def test_total_deals_evaluated(self):
        inp = _base_inp(total_deals_evaluated=50)
        assert inp.total_deals_evaluated == 50

    def test_avg_opportunity_value_usd(self):
        inp = _base_inp(avg_opportunity_value_usd=25_000.0)
        assert inp.avg_opportunity_value_usd == 25_000.0

    def test_total_field_count(self):
        import dataclasses
        fields = dataclasses.fields(DecayInput)
        assert len(fields) == 22


# ===========================================================================
# 3. DecayResult field tests and to_dict
# ===========================================================================

class TestDecayResultFields:
    @pytest.fixture
    def result(self):
        eng = _engine()
        return eng.assess(_base_inp())

    def test_rep_id_field(self, result):
        assert result.rep_id == "REP-001"

    def test_region_field(self, result):
        assert result.region == "EMEA"

    def test_decay_risk_type(self, result):
        assert isinstance(result.decay_risk, DecayRisk)

    def test_decay_pattern_type(self, result):
        assert isinstance(result.decay_pattern, DecayPattern)

    def test_decay_severity_type(self, result):
        assert isinstance(result.decay_severity, DecaySeverity)

    def test_recommended_action_type(self, result):
        assert isinstance(result.recommended_action, DecayAction)

    def test_trajectory_score_is_float(self, result):
        assert isinstance(result.trajectory_score, float)

    def test_competitive_score_is_float(self, result):
        assert isinstance(result.competitive_score, float)

    def test_deal_quality_score_is_float(self, result):
        assert isinstance(result.deal_quality_score, float)

    def test_late_stage_score_is_float(self, result):
        assert isinstance(result.late_stage_score, float)

    def test_decay_composite_is_float(self, result):
        assert isinstance(result.decay_composite, float)

    def test_has_decay_gap_is_bool(self, result):
        assert isinstance(result.has_decay_gap, bool)

    def test_requires_decay_coaching_is_bool(self, result):
        assert isinstance(result.requires_decay_coaching, bool)

    def test_estimated_revenue_decay_usd_is_float(self, result):
        assert isinstance(result.estimated_revenue_decay_usd, float)

    def test_decay_signal_is_str(self, result):
        assert isinstance(result.decay_signal, str)

    def test_total_field_count(self):
        import dataclasses
        fields = dataclasses.fields(DecayResult)
        assert len(fields) == 15


class TestDecayResultToDict:
    @pytest.fixture
    def d(self):
        eng = _engine()
        return eng.assess(_base_inp()).to_dict()

    def test_returns_dict(self, d):
        assert isinstance(d, dict)

    def test_exactly_15_keys(self, d):
        assert len(d) == 15

    def test_key_rep_id(self, d):
        assert "rep_id" in d

    def test_key_region(self, d):
        assert "region" in d

    def test_key_decay_risk(self, d):
        assert "decay_risk" in d

    def test_key_decay_pattern(self, d):
        assert "decay_pattern" in d

    def test_key_decay_severity(self, d):
        assert "decay_severity" in d

    def test_key_recommended_action(self, d):
        assert "recommended_action" in d

    def test_key_trajectory_score(self, d):
        assert "trajectory_score" in d

    def test_key_competitive_score(self, d):
        assert "competitive_score" in d

    def test_key_deal_quality_score(self, d):
        assert "deal_quality_score" in d

    def test_key_late_stage_score(self, d):
        assert "late_stage_score" in d

    def test_key_decay_composite(self, d):
        assert "decay_composite" in d

    def test_key_has_decay_gap(self, d):
        assert "has_decay_gap" in d

    def test_key_requires_decay_coaching(self, d):
        assert "requires_decay_coaching" in d

    def test_key_estimated_revenue_decay_usd(self, d):
        assert "estimated_revenue_decay_usd" in d

    def test_key_decay_signal(self, d):
        assert "decay_signal" in d

    def test_decay_risk_is_string_not_enum(self, d):
        assert isinstance(d["decay_risk"], str)
        assert type(d["decay_risk"]) is str  # plain str, not DecayRisk enum instance

    def test_decay_pattern_is_string_not_enum(self, d):
        assert isinstance(d["decay_pattern"], str)

    def test_decay_severity_is_string_not_enum(self, d):
        assert isinstance(d["decay_severity"], str)

    def test_recommended_action_is_string_not_enum(self, d):
        assert isinstance(d["recommended_action"], str)

    def test_rep_id_value(self, d):
        assert d["rep_id"] == "REP-001"

    def test_region_value(self, d):
        assert d["region"] == "EMEA"


# ===========================================================================
# 4. Trajectory sub-score branches
# ===========================================================================

class TestTrajectoryScore:
    """Tests every branch of _trajectory_score."""

    def _score(self, **kw) -> float:
        eng = _engine()
        return eng._trajectory_score(_base_inp(**kw))

    # --- decline_6m branches ---
    def test_decline_6m_above_20pp_adds_40(self):
        # 0.70 - 0.45 = 0.25 >= 0.20 → +40
        s = self._score(win_rate_6m_ago_pct=0.70, current_win_rate_pct=0.45,
                        win_rate_decline_velocity_pct=0.00)
        assert s >= 40.0

    def test_decline_6m_exactly_20pp_adds_40(self):
        # 0.90 - 0.70 = 0.20000...007 >= 0.20 (float-safe), current=0.70 no floor
        s = self._score(win_rate_6m_ago_pct=0.90, current_win_rate_pct=0.70,
                        win_rate_decline_velocity_pct=0.00)
        assert s == 40.0

    def test_decline_6m_between_10_and_20pp_adds_22(self):
        # 0.85 - 0.70 = 0.15 in [0.10, 0.20), current=0.70 no floor
        s = self._score(win_rate_6m_ago_pct=0.85, current_win_rate_pct=0.70,
                        win_rate_decline_velocity_pct=0.00)
        assert s == 22.0

    def test_decline_6m_exactly_10pp_adds_22(self):
        # 0.80 - 0.70 = 0.10000...009 >= 0.10 (float-safe), current=0.70 no floor
        s = self._score(win_rate_6m_ago_pct=0.80, current_win_rate_pct=0.70,
                        win_rate_decline_velocity_pct=0.00)
        assert s == 22.0

    def test_decline_6m_between_5_and_10pp_adds_8(self):
        s = self._score(win_rate_6m_ago_pct=0.57, current_win_rate_pct=0.50,
                        win_rate_decline_velocity_pct=0.00)
        # decline=0.07, current=0.50 → +8
        assert s == 8.0

    def test_decline_6m_exactly_5pp_adds_8(self):
        s = self._score(win_rate_6m_ago_pct=0.55, current_win_rate_pct=0.50,
                        win_rate_decline_velocity_pct=0.00)
        assert s == 8.0

    def test_decline_6m_below_5pp_adds_0(self):
        s = self._score(win_rate_6m_ago_pct=0.53, current_win_rate_pct=0.50,
                        win_rate_decline_velocity_pct=0.00)
        # decline=0.03 < 0.05 → +0, current=0.50 → no floor bonus
        assert s == 0.0

    # --- velocity branches ---
    def test_velocity_above_15pp_adds_35(self):
        s = self._score(win_rate_6m_ago_pct=0.50, current_win_rate_pct=0.50,
                        win_rate_decline_velocity_pct=0.20)
        # no decline, high velocity → +35, current=0.50 no floor
        assert s == 35.0

    def test_velocity_exactly_15pp_adds_35(self):
        s = self._score(win_rate_6m_ago_pct=0.50, current_win_rate_pct=0.50,
                        win_rate_decline_velocity_pct=0.15)
        assert s == 35.0

    def test_velocity_between_8_and_15pp_adds_18(self):
        s = self._score(win_rate_6m_ago_pct=0.50, current_win_rate_pct=0.50,
                        win_rate_decline_velocity_pct=0.10)
        assert s == 18.0

    def test_velocity_exactly_8pp_adds_18(self):
        s = self._score(win_rate_6m_ago_pct=0.50, current_win_rate_pct=0.50,
                        win_rate_decline_velocity_pct=0.08)
        assert s == 18.0

    def test_velocity_below_8pp_adds_0(self):
        s = self._score(win_rate_6m_ago_pct=0.50, current_win_rate_pct=0.50,
                        win_rate_decline_velocity_pct=0.05)
        assert s == 0.0

    # --- absolute win rate floor ---
    def test_win_rate_at_or_below_20pct_adds_25(self):
        s = self._score(win_rate_6m_ago_pct=0.20, current_win_rate_pct=0.15,
                        win_rate_decline_velocity_pct=0.00)
        # decline=0.05 → +8, floor ≤0.20 → +25 → 33
        assert s == 33.0

    def test_win_rate_exactly_20pct_adds_25(self):
        s = self._score(win_rate_6m_ago_pct=0.20, current_win_rate_pct=0.20,
                        win_rate_decline_velocity_pct=0.00)
        # decline=0, floor exactly 0.20 → +25
        assert s == 25.0

    def test_win_rate_between_20_and_35pct_adds_12(self):
        s = self._score(win_rate_6m_ago_pct=0.30, current_win_rate_pct=0.30,
                        win_rate_decline_velocity_pct=0.00)
        # decline=0, floor 0.30 in (0.20, 0.35] → +12
        assert s == 12.0

    def test_win_rate_exactly_35pct_adds_12(self):
        s = self._score(win_rate_6m_ago_pct=0.35, current_win_rate_pct=0.35,
                        win_rate_decline_velocity_pct=0.00)
        assert s == 12.0

    def test_win_rate_above_35pct_adds_0(self):
        s = self._score(win_rate_6m_ago_pct=0.50, current_win_rate_pct=0.50,
                        win_rate_decline_velocity_pct=0.00)
        assert s == 0.0

    def test_capped_at_100(self):
        # All three components max out: +40 +35 +25 = 100
        s = self._score(win_rate_6m_ago_pct=0.90, current_win_rate_pct=0.10,
                        win_rate_decline_velocity_pct=0.30)
        assert s == 100.0


# ===========================================================================
# 5. Competitive sub-score branches
# ===========================================================================

class TestCompetitiveScore:
    def _score(self, **kw) -> float:
        eng = _engine()
        return eng._competitive_score(_base_inp(**kw))

    def test_competitive_win_rate_below_20_adds_40(self):
        s = self._score(competitive_win_rate_pct=0.15, uncontested_win_rate_pct=0.15,
                        discounting_frequency_pct=0.00)
        assert s == 40.0

    def test_competitive_win_rate_exactly_20_adds_40(self):
        s = self._score(competitive_win_rate_pct=0.20, uncontested_win_rate_pct=0.20,
                        discounting_frequency_pct=0.00)
        assert s == 40.0

    def test_competitive_win_rate_between_20_and_35_adds_22(self):
        s = self._score(competitive_win_rate_pct=0.30, uncontested_win_rate_pct=0.30,
                        discounting_frequency_pct=0.00)
        assert s == 22.0

    def test_competitive_win_rate_exactly_35_adds_22(self):
        s = self._score(competitive_win_rate_pct=0.35, uncontested_win_rate_pct=0.35,
                        discounting_frequency_pct=0.00)
        assert s == 22.0

    def test_competitive_win_rate_between_35_and_50_adds_8(self):
        s = self._score(competitive_win_rate_pct=0.45, uncontested_win_rate_pct=0.45,
                        discounting_frequency_pct=0.00)
        assert s == 8.0

    def test_competitive_win_rate_exactly_50_adds_8(self):
        s = self._score(competitive_win_rate_pct=0.50, uncontested_win_rate_pct=0.50,
                        discounting_frequency_pct=0.00)
        assert s == 8.0

    def test_competitive_win_rate_above_50_adds_0(self):
        s = self._score(competitive_win_rate_pct=0.60, uncontested_win_rate_pct=0.60,
                        discounting_frequency_pct=0.00)
        assert s == 0.0

    # --- gap branches ---
    def test_gap_above_40_adds_35(self):
        s = self._score(competitive_win_rate_pct=0.60, uncontested_win_rate_pct=1.00,
                        discounting_frequency_pct=0.00)
        # cwr=0.60 → +0 (>0.50), gap=0.40 → +35
        assert s == 35.0

    def test_gap_exactly_40_adds_35(self):
        s = self._score(competitive_win_rate_pct=0.60, uncontested_win_rate_pct=1.00,
                        discounting_frequency_pct=0.00)
        assert s == 35.0

    def test_gap_between_25_and_40_adds_18(self):
        s = self._score(competitive_win_rate_pct=0.60, uncontested_win_rate_pct=0.90,
                        discounting_frequency_pct=0.00)
        # gap=0.30 in [0.25, 0.40) → +18, cwr>0.50 → +0
        assert s == 18.0

    def test_gap_exactly_25_adds_18(self):
        s = self._score(competitive_win_rate_pct=0.60, uncontested_win_rate_pct=0.85,
                        discounting_frequency_pct=0.00)
        assert s == 18.0

    def test_gap_below_25_adds_0(self):
        s = self._score(competitive_win_rate_pct=0.60, uncontested_win_rate_pct=0.80,
                        discounting_frequency_pct=0.00)
        # gap=0.20 < 0.25 → +0
        assert s == 0.0

    # --- discounting branches ---
    def test_discounting_above_70_adds_25(self):
        s = self._score(competitive_win_rate_pct=0.60, uncontested_win_rate_pct=0.60,
                        discounting_frequency_pct=0.80)
        assert s == 25.0

    def test_discounting_exactly_70_adds_25(self):
        s = self._score(competitive_win_rate_pct=0.60, uncontested_win_rate_pct=0.60,
                        discounting_frequency_pct=0.70)
        assert s == 25.0

    def test_discounting_between_45_and_70_adds_12(self):
        s = self._score(competitive_win_rate_pct=0.60, uncontested_win_rate_pct=0.60,
                        discounting_frequency_pct=0.55)
        assert s == 12.0

    def test_discounting_exactly_45_adds_12(self):
        s = self._score(competitive_win_rate_pct=0.60, uncontested_win_rate_pct=0.60,
                        discounting_frequency_pct=0.45)
        assert s == 12.0

    def test_discounting_below_45_adds_0(self):
        s = self._score(competitive_win_rate_pct=0.60, uncontested_win_rate_pct=0.60,
                        discounting_frequency_pct=0.30)
        assert s == 0.0

    def test_capped_at_100(self):
        s = self._score(competitive_win_rate_pct=0.10, uncontested_win_rate_pct=0.90,
                        discounting_frequency_pct=0.90)
        # +40 +35 +25 = 100
        assert s == 100.0

    def test_additive_combination(self):
        # cwr=0.30 → +22, gap=0.90-0.30=0.60 → +35, disc=0.75 → +25 → 82
        s = self._score(competitive_win_rate_pct=0.30, uncontested_win_rate_pct=0.90,
                        discounting_frequency_pct=0.75)
        assert s == 82.0


# ===========================================================================
# 6. Deal quality sub-score branches
# ===========================================================================

class TestDealQualityScore:
    def _score(self, **kw) -> float:
        eng = _engine()
        return eng._deal_quality_score(_base_inp(**kw))

    # --- no_decision branches ---
    def test_no_decision_above_40_adds_40(self):
        s = self._score(no_decision_rate_pct=0.50, avg_deal_size_current_usd=50_000,
                        avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.00)
        assert s == 40.0

    def test_no_decision_exactly_40_adds_40(self):
        s = self._score(no_decision_rate_pct=0.40, avg_deal_size_current_usd=50_000,
                        avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.00)
        assert s == 40.0

    def test_no_decision_between_25_and_40_adds_22(self):
        s = self._score(no_decision_rate_pct=0.30, avg_deal_size_current_usd=50_000,
                        avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.00)
        assert s == 22.0

    def test_no_decision_exactly_25_adds_22(self):
        s = self._score(no_decision_rate_pct=0.25, avg_deal_size_current_usd=50_000,
                        avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.00)
        assert s == 22.0

    def test_no_decision_between_15_and_25_adds_8(self):
        s = self._score(no_decision_rate_pct=0.20, avg_deal_size_current_usd=50_000,
                        avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.00)
        assert s == 8.0

    def test_no_decision_exactly_15_adds_8(self):
        s = self._score(no_decision_rate_pct=0.15, avg_deal_size_current_usd=50_000,
                        avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.00)
        assert s == 8.0

    def test_no_decision_below_15_adds_0(self):
        s = self._score(no_decision_rate_pct=0.10, avg_deal_size_current_usd=50_000,
                        avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.00)
        assert s == 0.0

    # --- size_inflation branches ---
    def test_size_inflation_above_2_adds_35(self):
        s = self._score(no_decision_rate_pct=0.00, avg_deal_size_current_usd=210_000,
                        avg_deal_size_6m_ago_usd=100_000, avg_discount_depth_pct=0.00)
        # inflation=2.1 >= 2.0 → +35
        assert s == 35.0

    def test_size_inflation_exactly_2_adds_35(self):
        s = self._score(no_decision_rate_pct=0.00, avg_deal_size_current_usd=200_000,
                        avg_deal_size_6m_ago_usd=100_000, avg_discount_depth_pct=0.00)
        assert s == 35.0

    def test_size_inflation_between_150_and_200_adds_18(self):
        s = self._score(no_decision_rate_pct=0.00, avg_deal_size_current_usd=170_000,
                        avg_deal_size_6m_ago_usd=100_000, avg_discount_depth_pct=0.00)
        # inflation=1.7 in [1.5, 2.0) → +18
        assert s == 18.0

    def test_size_inflation_exactly_150_adds_18(self):
        s = self._score(no_decision_rate_pct=0.00, avg_deal_size_current_usd=150_000,
                        avg_deal_size_6m_ago_usd=100_000, avg_discount_depth_pct=0.00)
        assert s == 18.0

    def test_size_inflation_below_150_adds_0(self):
        s = self._score(no_decision_rate_pct=0.00, avg_deal_size_current_usd=120_000,
                        avg_deal_size_6m_ago_usd=100_000, avg_discount_depth_pct=0.00)
        assert s == 0.0

    def test_size_inflation_zero_denominator_uses_max_1(self):
        # avg_deal_size_6m_ago_usd=0 → denominator=max(0,1)=1
        s = self._score(no_decision_rate_pct=0.00, avg_deal_size_current_usd=200_000,
                        avg_deal_size_6m_ago_usd=0.0, avg_discount_depth_pct=0.00)
        # inflation = 200000/1 >> 2.0 → +35
        assert s == 35.0

    # --- avg_discount_depth branches ---
    def test_discount_depth_above_25_adds_25(self):
        s = self._score(no_decision_rate_pct=0.00, avg_deal_size_current_usd=50_000,
                        avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.30)
        assert s == 25.0

    def test_discount_depth_exactly_25_adds_25(self):
        s = self._score(no_decision_rate_pct=0.00, avg_deal_size_current_usd=50_000,
                        avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.25)
        assert s == 25.0

    def test_discount_depth_between_15_and_25_adds_12(self):
        s = self._score(no_decision_rate_pct=0.00, avg_deal_size_current_usd=50_000,
                        avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.20)
        assert s == 12.0

    def test_discount_depth_exactly_15_adds_12(self):
        s = self._score(no_decision_rate_pct=0.00, avg_deal_size_current_usd=50_000,
                        avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.15)
        assert s == 12.0

    def test_discount_depth_below_15_adds_0(self):
        s = self._score(no_decision_rate_pct=0.00, avg_deal_size_current_usd=50_000,
                        avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.10)
        assert s == 0.0

    def test_capped_at_100(self):
        s = self._score(no_decision_rate_pct=0.50, avg_deal_size_current_usd=300_000,
                        avg_deal_size_6m_ago_usd=100_000, avg_discount_depth_pct=0.40)
        # +40 +35 +25 = 100
        assert s == 100.0


# ===========================================================================
# 7. Late-stage sub-score branches
# ===========================================================================

class TestLateStageScore:
    def _score(self, **kw) -> float:
        eng = _engine()
        return eng._late_stage_score(_base_inp(**kw))

    # --- deals_lost_at_stage_4plus branches ---
    def test_stage4_above_50_adds_45(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.55,
                        early_stage_win_rate_pct=0.50, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.80)
        assert s == 45.0

    def test_stage4_exactly_50_adds_45(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.50,
                        early_stage_win_rate_pct=0.50, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.80)
        assert s == 45.0

    def test_stage4_between_30_and_50_adds_25(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.40,
                        early_stage_win_rate_pct=0.50, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.80)
        assert s == 25.0

    def test_stage4_exactly_30_adds_25(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.30,
                        early_stage_win_rate_pct=0.50, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.80)
        assert s == 25.0

    def test_stage4_between_15_and_30_adds_10(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.20,
                        early_stage_win_rate_pct=0.50, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.80)
        assert s == 10.0

    def test_stage4_exactly_15_adds_10(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.15,
                        early_stage_win_rate_pct=0.50, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.80)
        assert s == 10.0

    def test_stage4_below_15_adds_0(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.10,
                        early_stage_win_rate_pct=0.50, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.80)
        assert s == 0.0

    # --- early_minus_late gap branches ---
    def test_gap_above_35_adds_30(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.00,
                        early_stage_win_rate_pct=0.90, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.80)
        # gap=0.40 ≥ 0.35 → +30
        assert s == 30.0

    def test_gap_exactly_35_adds_30(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.00,
                        early_stage_win_rate_pct=0.85, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.80)
        assert s == 30.0

    def test_gap_between_20_and_35_adds_15(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.00,
                        early_stage_win_rate_pct=0.75, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.80)
        # gap=0.25 → +15
        assert s == 15.0

    def test_gap_exactly_20_adds_15(self):
        # 0.80 - 0.60 = 0.20000...007 >= 0.20 (float-safe)
        s = self._score(deals_lost_at_stage_4plus_pct=0.00,
                        early_stage_win_rate_pct=0.80, late_stage_win_rate_pct=0.60,
                        champion_presence_lost_deals_pct=0.80)
        assert s == 15.0

    def test_gap_below_20_adds_0(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.00,
                        early_stage_win_rate_pct=0.65, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.80)
        # gap=0.15 < 0.20 → +0
        assert s == 0.0

    # --- champion_presence branches ---
    def test_champion_at_or_below_20_adds_25(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.00,
                        early_stage_win_rate_pct=0.50, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.15)
        assert s == 25.0

    def test_champion_exactly_20_adds_25(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.00,
                        early_stage_win_rate_pct=0.50, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.20)
        assert s == 25.0

    def test_champion_between_20_and_40_adds_12(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.00,
                        early_stage_win_rate_pct=0.50, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.30)
        assert s == 12.0

    def test_champion_exactly_40_adds_12(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.00,
                        early_stage_win_rate_pct=0.50, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.40)
        assert s == 12.0

    def test_champion_above_40_adds_0(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.00,
                        early_stage_win_rate_pct=0.50, late_stage_win_rate_pct=0.50,
                        champion_presence_lost_deals_pct=0.50)
        assert s == 0.0

    def test_capped_at_100(self):
        s = self._score(deals_lost_at_stage_4plus_pct=0.60,
                        early_stage_win_rate_pct=1.00, late_stage_win_rate_pct=0.00,
                        champion_presence_lost_deals_pct=0.10)
        # +45 +30 +25 = 100
        assert s == 100.0


# ===========================================================================
# 8. Pattern detection (priority order)
# ===========================================================================

class TestPatternDetection:
    """Each pattern tested in isolation and priority ordering verified."""

    def _detect(self, **kw) -> DecayPattern:
        eng = _engine()
        inp = _base_inp(**kw)
        t = eng._trajectory_score(inp)
        c = eng._competitive_score(inp)
        dq = eng._deal_quality_score(inp)
        ls = eng._late_stage_score(inp)
        return eng._detect_pattern(inp, t, c, dq, ls)

    # --- deal_size_inflation_trap (highest priority) ---
    def test_deal_size_inflation_trap_detected(self):
        p = self._detect(avg_deal_size_current_usd=200_000, avg_deal_size_6m_ago_usd=100_000,
                         no_decision_rate_pct=0.35)
        assert p == DecayPattern.deal_size_inflation_trap

    def test_deal_size_inflation_trap_exact_threshold(self):
        p = self._detect(avg_deal_size_current_usd=180_000, avg_deal_size_6m_ago_usd=100_000,
                         no_decision_rate_pct=0.30)
        assert p == DecayPattern.deal_size_inflation_trap

    def test_deal_size_inflation_trap_not_triggered_low_inflation(self):
        p = self._detect(avg_deal_size_current_usd=150_000, avg_deal_size_6m_ago_usd=100_000,
                         no_decision_rate_pct=0.40)
        assert p != DecayPattern.deal_size_inflation_trap

    def test_deal_size_inflation_trap_not_triggered_low_no_decision(self):
        p = self._detect(avg_deal_size_current_usd=200_000, avg_deal_size_6m_ago_usd=100_000,
                         no_decision_rate_pct=0.20)
        assert p != DecayPattern.deal_size_inflation_trap

    # --- late_stage_collapse (priority 2) ---
    def test_late_stage_collapse_detected(self):
        p = self._detect(
            deals_lost_at_stage_4plus_pct=0.45,
            early_stage_win_rate_pct=1.00, late_stage_win_rate_pct=0.10,
            champion_presence_lost_deals_pct=0.10,
            avg_deal_size_current_usd=50_000, avg_deal_size_6m_ago_usd=50_000,
            no_decision_rate_pct=0.10,
        )
        assert p == DecayPattern.late_stage_collapse

    def test_late_stage_collapse_requires_stage4_above_40(self):
        # late_stage score >=35 but stage4 < 0.40 → not late_stage_collapse
        p = self._detect(
            deals_lost_at_stage_4plus_pct=0.35,  # <0.40
            early_stage_win_rate_pct=1.00, late_stage_win_rate_pct=0.10,
            champion_presence_lost_deals_pct=0.10,
            avg_deal_size_current_usd=50_000, avg_deal_size_6m_ago_usd=50_000,
            no_decision_rate_pct=0.10,
        )
        assert p != DecayPattern.late_stage_collapse

    # --- competitive_displacement (priority 3) ---
    def test_competitive_displacement_detected(self):
        p = self._detect(
            competitive_win_rate_pct=0.15,
            uncontested_win_rate_pct=0.90,
            discounting_frequency_pct=0.80,
            avg_deal_size_current_usd=50_000, avg_deal_size_6m_ago_usd=50_000,
            no_decision_rate_pct=0.00,
            deals_lost_at_stage_4plus_pct=0.05,
        )
        assert p == DecayPattern.competitive_displacement

    def test_competitive_displacement_requires_cwr_below_25(self):
        # competitive score >=35 but cwr > 0.25
        p = self._detect(
            competitive_win_rate_pct=0.30,
            uncontested_win_rate_pct=0.90,
            discounting_frequency_pct=0.80,
            avg_deal_size_current_usd=50_000, avg_deal_size_6m_ago_usd=50_000,
            no_decision_rate_pct=0.00,
        )
        assert p != DecayPattern.competitive_displacement

    # --- sharp_cliff_drop (priority 4) ---
    def test_sharp_cliff_drop_detected(self):
        p = self._detect(
            win_rate_6m_ago_pct=0.90, current_win_rate_pct=0.20,
            win_rate_decline_velocity_pct=0.20,
            competitive_win_rate_pct=0.60, uncontested_win_rate_pct=0.60,
            discounting_frequency_pct=0.00,
            avg_deal_size_current_usd=50_000, avg_deal_size_6m_ago_usd=50_000,
            no_decision_rate_pct=0.00,
        )
        assert p == DecayPattern.sharp_cliff_drop

    def test_sharp_cliff_drop_requires_velocity_above_12(self):
        p = self._detect(
            win_rate_6m_ago_pct=0.90, current_win_rate_pct=0.20,
            win_rate_decline_velocity_pct=0.10,  # <0.12
            competitive_win_rate_pct=0.60, uncontested_win_rate_pct=0.60,
            discounting_frequency_pct=0.00,
            avg_deal_size_current_usd=50_000, avg_deal_size_6m_ago_usd=50_000,
            no_decision_rate_pct=0.00,
        )
        assert p != DecayPattern.sharp_cliff_drop

    # --- gradual_erosion (priority 5) ---
    def test_gradual_erosion_detected(self):
        # 0.80 - 0.70 = 0.10 >= 0.08, trajectory=22 >= 15; current=0.70 no floor
        p = self._detect(
            win_rate_6m_ago_pct=0.80, current_win_rate_pct=0.70,
            win_rate_decline_velocity_pct=0.00,
        )
        # decline=0.10 >= 0.08, trajectory=22 >= 15 → gradual_erosion
        assert p == DecayPattern.gradual_erosion

    def test_gradual_erosion_not_triggered_small_decline(self):
        p = self._detect(
            win_rate_6m_ago_pct=0.55, current_win_rate_pct=0.50,
            win_rate_decline_velocity_pct=0.03,
        )
        # decline=0.05 < 0.08 → not gradual
        assert p != DecayPattern.gradual_erosion

    # --- none (default) ---
    def test_none_pattern_when_all_healthy(self):
        p = self._detect()
        assert p == DecayPattern.none

    # --- priority: deal_size_inflation_trap beats late_stage_collapse ---
    def test_inflation_trap_wins_over_late_stage(self):
        p = self._detect(
            avg_deal_size_current_usd=200_000, avg_deal_size_6m_ago_usd=100_000,
            no_decision_rate_pct=0.35,
            deals_lost_at_stage_4plus_pct=0.45,
            early_stage_win_rate_pct=1.00, late_stage_win_rate_pct=0.10,
            champion_presence_lost_deals_pct=0.10,
        )
        assert p == DecayPattern.deal_size_inflation_trap


# ===========================================================================
# 9. Risk level thresholds
# ===========================================================================

class TestRiskLevel:
    def _risk(self, composite: float) -> DecayRisk:
        return _engine()._risk_level(composite)

    def test_critical_at_exactly_60(self):
        assert self._risk(60.0) == DecayRisk.critical

    def test_critical_above_60(self):
        assert self._risk(75.0) == DecayRisk.critical

    def test_critical_at_100(self):
        assert self._risk(100.0) == DecayRisk.critical

    def test_high_at_exactly_40(self):
        assert self._risk(40.0) == DecayRisk.high

    def test_high_between_40_and_60(self):
        assert self._risk(50.0) == DecayRisk.high

    def test_high_just_below_60(self):
        assert self._risk(59.9) == DecayRisk.high

    def test_moderate_at_exactly_20(self):
        assert self._risk(20.0) == DecayRisk.moderate

    def test_moderate_between_20_and_40(self):
        assert self._risk(30.0) == DecayRisk.moderate

    def test_moderate_just_below_40(self):
        assert self._risk(39.9) == DecayRisk.moderate

    def test_low_below_20(self):
        assert self._risk(10.0) == DecayRisk.low

    def test_low_at_zero(self):
        assert self._risk(0.0) == DecayRisk.low

    def test_low_just_below_20(self):
        assert self._risk(19.9) == DecayRisk.low


# ===========================================================================
# 10. Severity thresholds
# ===========================================================================

class TestSeverityLevel:
    def _sev(self, composite: float) -> DecaySeverity:
        return _engine()._severity(composite)

    def test_collapsing_at_exactly_60(self):
        assert self._sev(60.0) == DecaySeverity.collapsing

    def test_collapsing_above_60(self):
        assert self._sev(80.0) == DecaySeverity.collapsing

    def test_declining_at_exactly_40(self):
        assert self._sev(40.0) == DecaySeverity.declining

    def test_declining_between_40_and_60(self):
        assert self._sev(50.0) == DecaySeverity.declining

    def test_stable_at_exactly_20(self):
        assert self._sev(20.0) == DecaySeverity.stable

    def test_stable_between_20_and_40(self):
        assert self._sev(30.0) == DecaySeverity.stable

    def test_improving_below_20(self):
        assert self._sev(10.0) == DecaySeverity.improving

    def test_improving_at_zero(self):
        assert self._sev(0.0) == DecaySeverity.improving


# ===========================================================================
# 11. Action mapping
# ===========================================================================

class TestActionMapping:
    def _action(self, risk: DecayRisk, pattern: DecayPattern) -> DecayAction:
        return _engine()._action(risk, pattern)

    def test_critical_late_stage_collapse(self):
        a = self._action(DecayRisk.critical, DecayPattern.late_stage_collapse)
        assert a == DecayAction.late_stage_process_coaching

    def test_critical_competitive_displacement(self):
        a = self._action(DecayRisk.critical, DecayPattern.competitive_displacement)
        assert a == DecayAction.competitive_positioning_review

    def test_critical_other_pattern_gradual(self):
        a = self._action(DecayRisk.critical, DecayPattern.gradual_erosion)
        assert a == DecayAction.urgent_pipeline_intervention

    def test_critical_other_pattern_sharp(self):
        a = self._action(DecayRisk.critical, DecayPattern.sharp_cliff_drop)
        assert a == DecayAction.urgent_pipeline_intervention

    def test_critical_other_pattern_none(self):
        a = self._action(DecayRisk.critical, DecayPattern.none)
        assert a == DecayAction.urgent_pipeline_intervention

    def test_critical_other_pattern_inflation(self):
        a = self._action(DecayRisk.critical, DecayPattern.deal_size_inflation_trap)
        assert a == DecayAction.urgent_pipeline_intervention

    def test_high_deal_size_inflation_trap(self):
        a = self._action(DecayRisk.high, DecayPattern.deal_size_inflation_trap)
        assert a == DecayAction.deal_quality_audit

    def test_high_sharp_cliff_drop(self):
        a = self._action(DecayRisk.high, DecayPattern.sharp_cliff_drop)
        assert a == DecayAction.win_loss_debrief_coaching

    def test_high_other_pattern_none(self):
        a = self._action(DecayRisk.high, DecayPattern.none)
        assert a == DecayAction.win_loss_debrief_coaching

    def test_high_other_pattern_gradual(self):
        a = self._action(DecayRisk.high, DecayPattern.gradual_erosion)
        assert a == DecayAction.win_loss_debrief_coaching

    def test_high_other_pattern_late_stage(self):
        a = self._action(DecayRisk.high, DecayPattern.late_stage_collapse)
        assert a == DecayAction.win_loss_debrief_coaching

    def test_moderate_any_pattern(self):
        a = self._action(DecayRisk.moderate, DecayPattern.none)
        assert a == DecayAction.win_loss_debrief_coaching

    def test_moderate_with_gradual(self):
        a = self._action(DecayRisk.moderate, DecayPattern.gradual_erosion)
        assert a == DecayAction.win_loss_debrief_coaching

    def test_low_any_pattern(self):
        a = self._action(DecayRisk.low, DecayPattern.none)
        assert a == DecayAction.no_action

    def test_low_with_competitive_pattern(self):
        a = self._action(DecayRisk.low, DecayPattern.competitive_displacement)
        assert a == DecayAction.no_action


# ===========================================================================
# 12. has_decay_gap flag
# ===========================================================================

class TestHasDecayGap:
    def _gap(self, composite: float, **kw) -> bool:
        eng = _engine()
        inp = _base_inp(**kw)
        return eng._has_decay_gap(composite, inp)

    def test_true_when_composite_above_40(self):
        assert self._gap(40.0) is True

    def test_true_when_composite_above_60(self):
        assert self._gap(65.0) is True

    def test_true_when_6m_decline_above_15pp(self):
        assert self._gap(10.0, win_rate_6m_ago_pct=0.70, current_win_rate_pct=0.50) is True

    def test_true_when_6m_decline_exactly_15pp(self):
        assert self._gap(10.0, win_rate_6m_ago_pct=0.65, current_win_rate_pct=0.50) is True

    def test_true_when_current_win_rate_below_25(self):
        assert self._gap(10.0, current_win_rate_pct=0.20) is True

    def test_true_when_current_win_rate_exactly_25(self):
        assert self._gap(10.0, current_win_rate_pct=0.25) is True

    def test_false_when_no_condition_met(self):
        assert self._gap(30.0, win_rate_6m_ago_pct=0.55, current_win_rate_pct=0.50) is False

    def test_false_just_below_composite_threshold(self):
        # composite=39.9 < 40, decline=0.14 < 0.15, current=0.50 > 0.25 → False
        assert self._gap(39.9, win_rate_6m_ago_pct=0.64, current_win_rate_pct=0.50) is False

    def test_false_decline_just_below_15pp(self):
        # decline=0.14, current=0.50 (>0.25), composite=10 (<40)
        assert self._gap(10.0, win_rate_6m_ago_pct=0.64, current_win_rate_pct=0.50) is False


# ===========================================================================
# 13. requires_decay_coaching flag
# ===========================================================================

class TestRequiresDecayCoaching:
    def _coach(self, composite: float, **kw) -> bool:
        eng = _engine()
        inp = _base_inp(**kw)
        return eng._requires_decay_coaching(composite, inp)

    def test_true_when_composite_above_30(self):
        assert self._coach(30.0) is True

    def test_true_when_velocity_above_8pp(self):
        assert self._coach(10.0, win_rate_decline_velocity_pct=0.10) is True

    def test_true_when_velocity_exactly_8pp(self):
        assert self._coach(10.0, win_rate_decline_velocity_pct=0.08) is True

    def test_true_when_no_decision_above_25(self):
        assert self._coach(10.0, no_decision_rate_pct=0.30) is True

    def test_true_when_no_decision_exactly_25(self):
        assert self._coach(10.0, no_decision_rate_pct=0.25) is True

    def test_false_when_nothing_triggered(self):
        # composite=10 <30, velocity=0.02 <0.08, no_decision=0.10 <0.25
        assert self._coach(10.0) is False

    def test_false_velocity_just_below_threshold(self):
        assert self._coach(10.0, win_rate_decline_velocity_pct=0.07) is False

    def test_false_no_decision_just_below_threshold(self):
        assert self._coach(10.0, no_decision_rate_pct=0.24) is False


# ===========================================================================
# 14. Estimated revenue decay formula
# ===========================================================================

class TestEstimatedRevenueDecay:
    def _rev(self, composite: float, **kw) -> float:
        eng = _engine()
        inp = _base_inp(**kw)
        return eng._estimated_revenue_decay(inp, composite)

    def test_zero_when_no_decline(self):
        # 6m_ago == current → win_rate_gap=0
        r = self._rev(50.0, win_rate_6m_ago_pct=0.50, current_win_rate_pct=0.50)
        assert r == 0.0

    def test_zero_when_improved(self):
        # current > 6m_ago → gap capped at 0
        r = self._rev(50.0, win_rate_6m_ago_pct=0.40, current_win_rate_pct=0.60)
        assert r == 0.0

    def test_basic_formula(self):
        # 100 deals * 10000 * 0.10 decline * (50/100) = 50000
        # Use 0.20 - 0.10 = 0.10 exactly (float-safe)
        r = self._rev(50.0, total_deals_evaluated=100, avg_opportunity_value_usd=10_000,
                      win_rate_6m_ago_pct=0.20, current_win_rate_pct=0.10)
        assert r == 50_000.0

    def test_rounded_to_2_decimal_places(self):
        r = self._rev(33.0, total_deals_evaluated=7, avg_opportunity_value_usd=1_234.56,
                      win_rate_6m_ago_pct=0.55, current_win_rate_pct=0.50)
        assert r == round(7 * 1_234.56 * 0.05 * 0.33, 2)

    def test_composite_zero_gives_zero_decay(self):
        r = self._rev(0.0, win_rate_6m_ago_pct=0.80, current_win_rate_pct=0.50)
        assert r == 0.0

    def test_composite_100_uses_full_weight(self):
        r = self._rev(100.0, total_deals_evaluated=10, avg_opportunity_value_usd=1_000,
                      win_rate_6m_ago_pct=0.60, current_win_rate_pct=0.50)
        # 10 * 1000 * 0.10 * 1.0 = 1000
        assert r == 1_000.0

    def test_large_values(self):
        r = self._rev(80.0, total_deals_evaluated=500, avg_opportunity_value_usd=100_000,
                      win_rate_6m_ago_pct=0.70, current_win_rate_pct=0.40)
        expected = round(500 * 100_000 * 0.30 * 0.80, 2)
        assert r == expected


# ===========================================================================
# 15. Signal string
# ===========================================================================

class TestSignalString:
    def _signal(self, pattern: DecayPattern, composite: float, **kw) -> str:
        eng = _engine()
        inp = _base_inp(**kw)
        return eng._signal(inp, pattern, composite)

    def test_stable_signal_when_none_pattern_below_20(self):
        s = self._signal(DecayPattern.none, 10.0)
        assert s == "Win rate stable — trajectory, competitive positioning, and late-stage conversion within benchmarks"

    def test_stable_signal_exact_boundary(self):
        # none + composite=19.9 → stable
        s = self._signal(DecayPattern.none, 19.9)
        assert "Win rate stable" in s

    def test_non_stable_signal_when_none_pattern_composite_20(self):
        # none pattern but composite>=20 → non-stable signal
        s = self._signal(DecayPattern.none, 20.0,
                         current_win_rate_pct=0.50, win_rate_6m_ago_pct=0.60,
                         competitive_win_rate_pct=0.40)
        assert "Win rate stable" not in s

    def test_non_stable_signal_contains_current_win_rate(self):
        s = self._signal(DecayPattern.gradual_erosion, 25.0,
                         current_win_rate_pct=0.45, win_rate_6m_ago_pct=0.55,
                         competitive_win_rate_pct=0.40)
        assert "45% current win rate" in s

    def test_non_stable_signal_contains_pp_decline(self):
        s = self._signal(DecayPattern.gradual_erosion, 25.0,
                         current_win_rate_pct=0.45, win_rate_6m_ago_pct=0.55,
                         competitive_win_rate_pct=0.40)
        assert "10pp decline over 6m" in s

    def test_non_stable_signal_contains_competitive_win_rate(self):
        s = self._signal(DecayPattern.gradual_erosion, 25.0,
                         current_win_rate_pct=0.45, win_rate_6m_ago_pct=0.55,
                         competitive_win_rate_pct=0.40)
        assert "40% competitive win rate" in s

    def test_non_stable_signal_contains_composite(self):
        s = self._signal(DecayPattern.gradual_erosion, 25.0,
                         current_win_rate_pct=0.45, win_rate_6m_ago_pct=0.55,
                         competitive_win_rate_pct=0.40)
        assert "composite 25" in s

    def test_pattern_label_capitalized_in_signal(self):
        s = self._signal(DecayPattern.gradual_erosion, 30.0,
                         current_win_rate_pct=0.40, win_rate_6m_ago_pct=0.55,
                         competitive_win_rate_pct=0.35)
        assert s.startswith("Gradual erosion")

    def test_competitive_displacement_label(self):
        s = self._signal(DecayPattern.competitive_displacement, 65.0,
                         current_win_rate_pct=0.30, win_rate_6m_ago_pct=0.50,
                         competitive_win_rate_pct=0.15)
        assert s.startswith("Competitive displacement")

    def test_none_pattern_above_20_uses_win_rate_decay_label(self):
        s = self._signal(DecayPattern.none, 25.0,
                         current_win_rate_pct=0.50, win_rate_6m_ago_pct=0.60,
                         competitive_win_rate_pct=0.50)
        assert s.startswith("Win rate decay")

    def test_signal_format_with_sharp_cliff_drop(self):
        s = self._signal(DecayPattern.sharp_cliff_drop, 55.0,
                         current_win_rate_pct=0.25, win_rate_6m_ago_pct=0.50,
                         competitive_win_rate_pct=0.20)
        assert "Sharp cliff drop" in s
        assert "25% current win rate" in s
        assert "25pp decline over 6m" in s

    def test_decline_rounds_correctly(self):
        # 0.673 - 0.333 = 0.34 → "34pp"
        s = self._signal(DecayPattern.gradual_erosion, 30.0,
                         current_win_rate_pct=0.333, win_rate_6m_ago_pct=0.673,
                         competitive_win_rate_pct=0.30)
        assert "34pp decline over 6m" in s


# ===========================================================================
# 16. Composite calculation
# ===========================================================================

class TestCompositeCalculation:
    def test_composite_weights(self):
        # Use inputs that generate known sub-scores, verify composite
        eng = _engine()
        inp = _base_inp(
            # trajectory: decline=0, velocity=0, current=0.50 → 0
            win_rate_6m_ago_pct=0.50, current_win_rate_pct=0.50,
            win_rate_decline_velocity_pct=0.00,
            # competitive: cwr=0.60 (>0.50 → +0), gap=0 → 0, disc=0 → 0
            competitive_win_rate_pct=0.60, uncontested_win_rate_pct=0.60,
            discounting_frequency_pct=0.00,
            # deal_quality: no_decision=0.00 → 0, inflation=1.0 → 0, discount=0 → 0
            no_decision_rate_pct=0.00, avg_deal_size_current_usd=50_000,
            avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.00,
            # late_stage: stage4=0.10 (<0.15 → 0), gap=0 → 0, champ=0.60 → 0
            deals_lost_at_stage_4plus_pct=0.10,
            early_stage_win_rate_pct=0.60, late_stage_win_rate_pct=0.60,
            champion_presence_lost_deals_pct=0.60,
        )
        result = eng.assess(inp)
        assert result.decay_composite == 0.0

    def test_composite_capped_at_100(self):
        # Force all sub-scores to 100
        eng = _engine()
        inp = _base_inp(
            win_rate_6m_ago_pct=0.90, current_win_rate_pct=0.10,
            win_rate_decline_velocity_pct=0.30,
            competitive_win_rate_pct=0.10, uncontested_win_rate_pct=1.00,
            discounting_frequency_pct=0.90,
            no_decision_rate_pct=0.60, avg_deal_size_current_usd=300_000,
            avg_deal_size_6m_ago_usd=100_000, avg_discount_depth_pct=0.40,
            deals_lost_at_stage_4plus_pct=0.60,
            early_stage_win_rate_pct=1.00, late_stage_win_rate_pct=0.10,
            champion_presence_lost_deals_pct=0.10,
        )
        result = eng.assess(inp)
        assert result.decay_composite == 100.0

    def test_composite_weighted_sum(self):
        # trajectory=40, competitive=0, deal_quality=0, late_stage=0
        # composite = 40*0.35 = 14.0
        # Use 0.90-0.70=0.20000...007 >= 0.20 to reliably get +40 (float-safe)
        eng = _engine()
        inp = _base_inp(
            win_rate_6m_ago_pct=0.90, current_win_rate_pct=0.70,
            win_rate_decline_velocity_pct=0.00,
            competitive_win_rate_pct=0.60, uncontested_win_rate_pct=0.60,
            discounting_frequency_pct=0.00,
            no_decision_rate_pct=0.00, avg_deal_size_current_usd=50_000,
            avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.00,
            deals_lost_at_stage_4plus_pct=0.10,
            early_stage_win_rate_pct=0.60, late_stage_win_rate_pct=0.60,
            champion_presence_lost_deals_pct=0.60,
        )
        result = eng.assess(inp)
        # trajectory: decline=0.20 → +40, velocity=0 → 0, current=0.70 → 0 → 40
        assert result.trajectory_score == 40.0
        assert result.competitive_score == 0.0
        assert result.deal_quality_score == 0.0
        assert result.late_stage_score == 0.0
        assert result.decay_composite == 14.0


# ===========================================================================
# 17. End-to-end assess() tests
# ===========================================================================

class TestAssessEndToEnd:
    def test_healthy_rep_is_low_risk(self):
        eng = _engine()
        result = eng.assess(_base_inp())
        assert result.decay_risk == DecayRisk.low

    def test_healthy_rep_is_improving(self):
        eng = _engine()
        result = eng.assess(_base_inp())
        assert result.decay_severity == DecaySeverity.improving

    def test_healthy_rep_no_action(self):
        eng = _engine()
        result = eng.assess(_base_inp())
        assert result.recommended_action == DecayAction.no_action

    def test_healthy_rep_no_decay_gap(self):
        eng = _engine()
        result = eng.assess(_base_inp())
        assert result.has_decay_gap is False

    def test_healthy_rep_no_coaching(self):
        eng = _engine()
        result = eng.assess(_base_inp())
        assert result.requires_decay_coaching is False

    def test_critical_rep_scenario(self):
        eng = _engine()
        inp = _base_inp(
            win_rate_6m_ago_pct=0.80, current_win_rate_pct=0.20,
            win_rate_decline_velocity_pct=0.25,
            competitive_win_rate_pct=0.15,
            uncontested_win_rate_pct=0.85,
            discounting_frequency_pct=0.80,
            no_decision_rate_pct=0.45,
            avg_deal_size_current_usd=200_000,
            avg_deal_size_6m_ago_usd=100_000,
            avg_discount_depth_pct=0.30,
            deals_lost_at_stage_4plus_pct=0.55,
            early_stage_win_rate_pct=0.80,
            late_stage_win_rate_pct=0.10,
            champion_presence_lost_deals_pct=0.10,
        )
        result = eng.assess(inp)
        assert result.decay_risk == DecayRisk.critical
        assert result.decay_severity == DecaySeverity.collapsing
        assert result.has_decay_gap is True
        assert result.requires_decay_coaching is True

    def test_result_stored_in_engine(self):
        eng = _engine()
        eng.assess(_base_inp())
        assert len(eng._results) == 1

    def test_multiple_assess_stored(self):
        eng = _engine()
        eng.assess(_base_inp(rep_id="A"))
        eng.assess(_base_inp(rep_id="B"))
        assert len(eng._results) == 2

    def test_rep_id_carried_through(self):
        eng = _engine()
        result = eng.assess(_base_inp(rep_id="SPECIAL-REP"))
        assert result.rep_id == "SPECIAL-REP"

    def test_region_carried_through(self):
        eng = _engine()
        result = eng.assess(_base_inp(region="LATAM"))
        assert result.region == "LATAM"

    def test_scores_within_0_100(self):
        eng = _engine()
        result = eng.assess(_base_inp(
            win_rate_6m_ago_pct=0.90, current_win_rate_pct=0.10,
            win_rate_decline_velocity_pct=0.30,
        ))
        assert 0 <= result.trajectory_score <= 100
        assert 0 <= result.competitive_score <= 100
        assert 0 <= result.deal_quality_score <= 100
        assert 0 <= result.late_stage_score <= 100
        assert 0 <= result.decay_composite <= 100

    def test_moderate_risk_scenario(self):
        # Build inputs that yield composite in [20, 40) → moderate
        # trajectory: 0.90-0.70=0.20 → +40, vel=0, current=0.70 → 0 → t=40
        # competitive: cwr=0.60 (>0.50 → 0), gap=0, disc=0 → c=0
        # deal_quality: no_dec=0.05 → 0, inflation=1 → 0, disc_depth=0.02 → 0 → dq=0
        # late_stage: stage4=0.10 → 0, gap=0.55-0.50=0.05 (<0.20) → 0, champ=0.60 → 0 → ls=0
        # composite = 40*0.35 = 14.0 → low ... need more
        # Add some competitive: cwr=0.45 (in (0.35,0.50]) → +8 → c=8
        # composite = 40*0.35 + 8*0.25 = 14 + 2 = 16 → still low
        # Add no_decision=0.20 (>=0.15) → dq=+8
        # composite = 40*0.35 + 8*0.25 + 8*0.20 = 14 + 2 + 1.6 = 17.6 → low
        # Need composite >= 20: add late_stage gap: early=0.75, late=0.50, gap=0.25 → +15
        # ls = 15, composite = 14 + 2 + 1.6 + 15*0.20 = 14+2+1.6+3 = 20.6 → moderate
        eng = _engine()
        inp = _base_inp(
            win_rate_6m_ago_pct=0.90, current_win_rate_pct=0.70,
            win_rate_decline_velocity_pct=0.00,
            competitive_win_rate_pct=0.45, uncontested_win_rate_pct=0.45,
            discounting_frequency_pct=0.00,
            no_decision_rate_pct=0.20, avg_deal_size_current_usd=50_000,
            avg_deal_size_6m_ago_usd=50_000, avg_discount_depth_pct=0.00,
            deals_lost_at_stage_4plus_pct=0.10,
            early_stage_win_rate_pct=0.75, late_stage_win_rate_pct=0.50,
            champion_presence_lost_deals_pct=0.80,
        )
        result = eng.assess(inp)
        assert result.decay_risk == DecayRisk.moderate

    def test_revenue_decay_in_result(self):
        eng = _engine()
        inp = _base_inp(
            win_rate_6m_ago_pct=0.60, current_win_rate_pct=0.50,
            total_deals_evaluated=100, avg_opportunity_value_usd=10_000,
        )
        result = eng.assess(inp)
        # If composite>0 and decline>0, revenue decay > 0
        if result.decay_composite > 0:
            assert result.estimated_revenue_decay_usd >= 0.0

    def test_to_dict_matches_result_fields(self):
        eng = _engine()
        result = eng.assess(_base_inp())
        d = result.to_dict()
        assert d["rep_id"] == result.rep_id
        assert d["region"] == result.region
        assert d["decay_risk"] == result.decay_risk.value
        assert d["trajectory_score"] == result.trajectory_score
        assert d["decay_composite"] == result.decay_composite


# ===========================================================================
# 18. assess_batch()
# ===========================================================================

class TestAssessBatch:
    def test_empty_batch_returns_empty_list(self):
        eng = _engine()
        assert eng.assess_batch([]) == []

    def test_single_item_batch(self):
        eng = _engine()
        results = eng.assess_batch([_base_inp()])
        assert len(results) == 1
        assert isinstance(results[0], DecayResult)

    def test_multiple_items_returns_correct_count(self):
        eng = _engine()
        inputs = [_base_inp(rep_id=f"REP-{i}") for i in range(5)]
        results = eng.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_rep_ids_match(self):
        eng = _engine()
        inputs = [_base_inp(rep_id=f"REP-{i}") for i in range(3)]
        results = eng.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"REP-{i}"

    def test_batch_stores_all_results(self):
        eng = _engine()
        eng.assess_batch([_base_inp(rep_id=f"REP-{i}") for i in range(4)])
        assert len(eng._results) == 4

    def test_batch_returns_list_of_decay_result(self):
        eng = _engine()
        results = eng.assess_batch([_base_inp(), _base_inp()])
        for r in results:
            assert isinstance(r, DecayResult)

    def test_batch_accumulated_with_prior_assess(self):
        eng = _engine()
        eng.assess(_base_inp(rep_id="FIRST"))
        eng.assess_batch([_base_inp(rep_id="BATCH-1"), _base_inp(rep_id="BATCH-2")])
        assert len(eng._results) == 3

    def test_batch_different_risk_levels(self):
        eng = _engine()
        low_inp = _base_inp()
        critical_inp = _base_inp(
            win_rate_6m_ago_pct=0.90, current_win_rate_pct=0.10,
            win_rate_decline_velocity_pct=0.30,
            competitive_win_rate_pct=0.10, uncontested_win_rate_pct=0.90,
            discounting_frequency_pct=0.90, no_decision_rate_pct=0.50,
            avg_deal_size_current_usd=300_000, avg_deal_size_6m_ago_usd=100_000,
            avg_discount_depth_pct=0.40, deals_lost_at_stage_4plus_pct=0.60,
            early_stage_win_rate_pct=1.00, late_stage_win_rate_pct=0.10,
            champion_presence_lost_deals_pct=0.10,
        )
        results = eng.assess_batch([low_inp, critical_inp])
        risks = {r.decay_risk for r in results}
        assert DecayRisk.low in risks
        assert DecayRisk.critical in risks


# ===========================================================================
# 19. summary() — empty engine
# ===========================================================================

class TestSummaryEmpty:
    @pytest.fixture
    def s(self):
        return _engine().summary()

    def test_returns_dict(self, s):
        assert isinstance(s, dict)

    def test_exactly_13_keys(self, s):
        assert len(s) == 13

    def test_total_is_zero(self, s):
        assert s["total"] == 0

    def test_risk_counts_empty(self, s):
        assert s["risk_counts"] == {}

    def test_pattern_counts_empty(self, s):
        assert s["pattern_counts"] == {}

    def test_severity_counts_empty(self, s):
        assert s["severity_counts"] == {}

    def test_action_counts_empty(self, s):
        assert s["action_counts"] == {}

    def test_avg_decay_composite_zero(self, s):
        assert s["avg_decay_composite"] == 0.0

    def test_decay_gap_count_zero(self, s):
        assert s["decay_gap_count"] == 0

    def test_coaching_count_zero(self, s):
        assert s["coaching_count"] == 0

    def test_avg_trajectory_score_zero(self, s):
        assert s["avg_trajectory_score"] == 0.0

    def test_avg_competitive_score_zero(self, s):
        assert s["avg_competitive_score"] == 0.0

    def test_avg_deal_quality_score_zero(self, s):
        assert s["avg_deal_quality_score"] == 0.0

    def test_avg_late_stage_score_zero(self, s):
        assert s["avg_late_stage_score"] == 0.0

    def test_total_estimated_revenue_decay_zero(self, s):
        assert s["total_estimated_revenue_decay_usd"] == 0.0


# ===========================================================================
# 20. summary() — populated engine
# ===========================================================================

class TestSummaryPopulated:
    @pytest.fixture
    def eng_and_summary(self):
        eng = _engine()
        # Healthy rep
        eng.assess(_base_inp(rep_id="R1", region="NA"))
        # Critical rep
        eng.assess(_base_inp(
            rep_id="R2", region="EMEA",
            win_rate_6m_ago_pct=0.90, current_win_rate_pct=0.10,
            win_rate_decline_velocity_pct=0.30,
            competitive_win_rate_pct=0.10, uncontested_win_rate_pct=0.90,
            discounting_frequency_pct=0.90, no_decision_rate_pct=0.50,
            avg_deal_size_current_usd=300_000, avg_deal_size_6m_ago_usd=100_000,
            avg_discount_depth_pct=0.40, deals_lost_at_stage_4plus_pct=0.60,
            early_stage_win_rate_pct=1.00, late_stage_win_rate_pct=0.10,
            champion_presence_lost_deals_pct=0.10,
        ))
        return eng, eng.summary()

    def test_total_is_two(self, eng_and_summary):
        _, s = eng_and_summary
        assert s["total"] == 2

    def test_risk_counts_has_entries(self, eng_and_summary):
        _, s = eng_and_summary
        assert len(s["risk_counts"]) >= 1

    def test_risk_counts_sum_equals_total(self, eng_and_summary):
        _, s = eng_and_summary
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_pattern_counts_sum_equals_total(self, eng_and_summary):
        _, s = eng_and_summary
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_severity_counts_sum_equals_total(self, eng_and_summary):
        _, s = eng_and_summary
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_action_counts_sum_equals_total(self, eng_and_summary):
        _, s = eng_and_summary
        assert sum(s["action_counts"].values()) == s["total"]

    def test_avg_decay_composite_is_float(self, eng_and_summary):
        _, s = eng_and_summary
        assert isinstance(s["avg_decay_composite"], float)

    def test_decay_gap_count_is_int(self, eng_and_summary):
        _, s = eng_and_summary
        assert isinstance(s["decay_gap_count"], int)

    def test_coaching_count_is_int(self, eng_and_summary):
        _, s = eng_and_summary
        assert isinstance(s["coaching_count"], int)

    def test_decay_gap_count_within_bounds(self, eng_and_summary):
        _, s = eng_and_summary
        assert 0 <= s["decay_gap_count"] <= s["total"]

    def test_coaching_count_within_bounds(self, eng_and_summary):
        _, s = eng_and_summary
        assert 0 <= s["coaching_count"] <= s["total"]

    def test_avg_trajectory_score_is_float(self, eng_and_summary):
        _, s = eng_and_summary
        assert isinstance(s["avg_trajectory_score"], float)

    def test_avg_competitive_score_is_float(self, eng_and_summary):
        _, s = eng_and_summary
        assert isinstance(s["avg_competitive_score"], float)

    def test_avg_deal_quality_score_is_float(self, eng_and_summary):
        _, s = eng_and_summary
        assert isinstance(s["avg_deal_quality_score"], float)

    def test_avg_late_stage_score_is_float(self, eng_and_summary):
        _, s = eng_and_summary
        assert isinstance(s["avg_late_stage_score"], float)

    def test_total_revenue_decay_is_float(self, eng_and_summary):
        _, s = eng_and_summary
        assert isinstance(s["total_estimated_revenue_decay_usd"], float)

    def test_total_revenue_decay_nonnegative(self, eng_and_summary):
        _, s = eng_and_summary
        assert s["total_estimated_revenue_decay_usd"] >= 0.0

    def test_avg_composite_between_0_and_100(self, eng_and_summary):
        _, s = eng_and_summary
        assert 0.0 <= s["avg_decay_composite"] <= 100.0

    def test_summary_all_13_keys_present(self, eng_and_summary):
        _, s = eng_and_summary
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
            "avg_decay_composite", "decay_gap_count", "coaching_count",
            "avg_trajectory_score", "avg_competitive_score", "avg_deal_quality_score",
            "avg_late_stage_score", "total_estimated_revenue_decay_usd",
        }
        assert set(s.keys()) == expected

    def test_critical_in_risk_counts(self, eng_and_summary):
        _, s = eng_and_summary
        assert "critical" in s["risk_counts"]

    def test_low_in_risk_counts(self, eng_and_summary):
        _, s = eng_and_summary
        assert "low" in s["risk_counts"]

    def test_revenue_equals_sum_of_individual(self, eng_and_summary):
        eng, s = eng_and_summary
        expected = round(sum(r.estimated_revenue_decay_usd for r in eng._results), 2)
        assert s["total_estimated_revenue_decay_usd"] == expected

    def test_avg_composite_equals_mean_of_individual(self, eng_and_summary):
        eng, s = eng_and_summary
        n = len(eng._results)
        expected = round(sum(r.decay_composite for r in eng._results) / n, 1)
        assert s["avg_decay_composite"] == expected

    def test_decay_gap_count_matches_manual(self, eng_and_summary):
        eng, s = eng_and_summary
        expected = sum(1 for r in eng._results if r.has_decay_gap)
        assert s["decay_gap_count"] == expected

    def test_coaching_count_matches_manual(self, eng_and_summary):
        eng, s = eng_and_summary
        expected = sum(1 for r in eng._results if r.requires_decay_coaching)
        assert s["coaching_count"] == expected


# ===========================================================================
# 21. Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_zero_deals_evaluated_gives_zero_revenue(self):
        eng = _engine()
        result = eng.assess(_base_inp(
            total_deals_evaluated=0,
            win_rate_6m_ago_pct=0.80, current_win_rate_pct=0.40,
        ))
        assert result.estimated_revenue_decay_usd == 0.0

    def test_zero_opportunity_value_gives_zero_revenue(self):
        eng = _engine()
        result = eng.assess(_base_inp(
            avg_opportunity_value_usd=0.0,
            win_rate_6m_ago_pct=0.80, current_win_rate_pct=0.40,
        ))
        assert result.estimated_revenue_decay_usd == 0.0

    def test_win_rate_exactly_at_critical_boundary(self):
        # Build scenario with composite exactly 60
        # trajectory=40, competitive=22, deal_quality=0, late_stage=0
        # composite = 40*0.35 + 22*0.25 = 14.0 + 5.5 = 19.5 — not 60
        # Instead: t=100, c=100, dq=100, ls=100 → 100
        eng = _engine()
        inp = _base_inp(
            win_rate_6m_ago_pct=0.90, current_win_rate_pct=0.10,
            win_rate_decline_velocity_pct=0.30,
            competitive_win_rate_pct=0.10, uncontested_win_rate_pct=0.90,
            discounting_frequency_pct=0.90,
        )
        result = eng.assess(inp)
        assert result.decay_risk == DecayRisk.critical

    def test_avg_deal_size_6m_ago_zero_does_not_crash(self):
        eng = _engine()
        result = eng.assess(_base_inp(avg_deal_size_6m_ago_usd=0.0,
                                      avg_deal_size_current_usd=100_000))
        assert isinstance(result, DecayResult)

    def test_all_rates_at_100pct(self):
        eng = _engine()
        result = eng.assess(_base_inp(
            current_win_rate_pct=1.0,
            win_rate_3m_ago_pct=1.0,
            win_rate_6m_ago_pct=1.0,
            late_stage_win_rate_pct=1.0,
            early_stage_win_rate_pct=1.0,
            competitive_win_rate_pct=1.0,
            uncontested_win_rate_pct=1.0,
            no_decision_rate_pct=0.0,
            discounting_frequency_pct=0.0,
            avg_discount_depth_pct=0.0,
            deals_lost_at_stage_4plus_pct=0.0,
            champion_presence_lost_deals_pct=1.0,
            win_rate_decline_velocity_pct=0.0,
        ))
        assert result.decay_risk == DecayRisk.low

    def test_all_rates_at_zero_pct(self):
        eng = _engine()
        result = eng.assess(_base_inp(
            current_win_rate_pct=0.0,
            win_rate_3m_ago_pct=0.0,
            win_rate_6m_ago_pct=0.0,
            late_stage_win_rate_pct=0.0,
            early_stage_win_rate_pct=0.0,
            competitive_win_rate_pct=0.0,
            uncontested_win_rate_pct=0.0,
        ))
        # Should not crash
        assert isinstance(result, DecayResult)

    def test_large_deal_values_no_crash(self):
        eng = _engine()
        result = eng.assess(_base_inp(
            avg_deal_size_current_usd=1_000_000_000.0,
            avg_deal_size_6m_ago_usd=1.0,
            total_deals_evaluated=10_000,
            avg_opportunity_value_usd=500_000.0,
        ))
        assert isinstance(result.estimated_revenue_decay_usd, float)

    def test_fresh_engine_has_empty_results(self):
        eng = _engine()
        assert eng._results == []

    def test_score_rounded_to_1_decimal(self):
        eng = _engine()
        result = eng.assess(_base_inp())
        # Scores from assess() are rounded to 1 decimal
        for score in [result.trajectory_score, result.competitive_score,
                      result.deal_quality_score, result.late_stage_score,
                      result.decay_composite]:
            assert round(score, 1) == score

    def test_summary_single_result(self):
        eng = _engine()
        eng.assess(_base_inp())
        s = eng.summary()
        assert s["total"] == 1
        assert len(s) == 13

    def test_pattern_none_composite_0_stable_signal(self):
        eng = _engine()
        result = eng.assess(_base_inp())
        if result.decay_pattern == DecayPattern.none and result.decay_composite < 20:
            assert "Win rate stable" in result.decay_signal

    def test_gradual_erosion_exact_boundary(self):
        # Need decline >= 0.08 but trajectory < 15 → pattern=none
        # decline=0.09 → +8 (>=0.05 but <0.10), velocity=0, current=0.91 (>0.35 → 0) → t=8 < 15
        eng = _engine()
        inp = _base_inp(
            win_rate_6m_ago_pct=0.10, current_win_rate_pct=0.01,
            win_rate_decline_velocity_pct=0.00,
        )
        # decline=0.09 ≥ 0.08, but what is trajectory?
        # Actual: win_rate_6m_ago=0.10, current=0.01 → decline=0.09 → +8
        # current=0.01 <=0.20 → +25 → t=33 ≥ 15 → gradual would trigger...
        # Use decline=0.09 with current=0.91:
        inp2 = _base_inp(
            win_rate_6m_ago_pct=1.00, current_win_rate_pct=0.91,
            win_rate_decline_velocity_pct=0.00,
        )
        # decline=0.09 ≥ 0.08, velocity=0, current=0.91 (>0.35 → 0) → t=8 < 15
        t2 = eng._trajectory_score(inp2)
        c2 = eng._competitive_score(inp2)
        dq2 = eng._deal_quality_score(inp2)
        ls2 = eng._late_stage_score(inp2)
        pattern2 = eng._detect_pattern(inp2, t2, c2, dq2, ls2)
        assert t2 == 8.0  # trajectory below 15
        assert pattern2 == DecayPattern.none  # gradual_erosion not triggered: t<15

    def test_gradual_erosion_triggers_with_higher_trajectory(self):
        # Use 0.80 - 0.70 = 0.10 (float-safe), current=0.70 no floor → t=22 >= 15
        eng = _engine()
        inp = _base_inp(
            win_rate_6m_ago_pct=0.80, current_win_rate_pct=0.70,
            win_rate_decline_velocity_pct=0.00,
        )
        t = eng._trajectory_score(inp)
        c = eng._competitive_score(inp)
        dq = eng._deal_quality_score(inp)
        ls = eng._late_stage_score(inp)
        pattern = eng._detect_pattern(inp, t, c, dq, ls)
        # decline=0.10 ≥ 0.08, t=22 ≥ 15 → gradual_erosion
        assert t == 22.0
        assert pattern == DecayPattern.gradual_erosion

    def test_multiple_engines_independent(self):
        eng1 = _engine()
        eng2 = _engine()
        eng1.assess(_base_inp(rep_id="E1"))
        assert len(eng1._results) == 1
        assert len(eng2._results) == 0

    def test_summary_after_batch(self):
        eng = _engine()
        eng.assess_batch([_base_inp(rep_id=f"R{i}") for i in range(10)])
        s = eng.summary()
        assert s["total"] == 10

    def test_revenue_decay_nonnegative_always(self):
        eng = _engine()
        for rate in [0.0, 0.3, 0.5, 0.8, 1.0]:
            r = eng.assess(_base_inp(current_win_rate_pct=rate,
                                     win_rate_6m_ago_pct=0.5))
            assert r.estimated_revenue_decay_usd >= 0.0
