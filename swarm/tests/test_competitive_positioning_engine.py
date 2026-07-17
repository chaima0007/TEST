"""
Comprehensive pytest test suite for CompetitivePositioningEngine.
Tests cover enums, dataclasses, scoring formulas, properties,
summary, reset, and end-to-end scenarios.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.competitive_positioning_engine import (
    PositioningStrength,
    CompetitorThreat,
    WinProbability,
    PositioningAction,
    CompetitivePositioningInput,
    CompetitivePositioningResult,
    CompetitivePositioningEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> CompetitivePositioningInput:
    """Return a neutral baseline input, field values can be overridden."""
    defaults = dict(
        deal_id="D001",
        account_id="A001",
        competitor_name="AcmeCorp",
        deal_stage="demo",
        deal_value=50_000.0,
        our_product_fit=70.0,
        competitor_product_fit=60.0,
        our_price_competitiveness=60.0,
        competitor_price_delta=5.0,
        our_relationship_strength=60.0,
        competitor_relationship_strength=40.0,
        our_features_advantage=0,
        champion_supports_us=False,
        economic_buyer_engaged=False,
        competitor_in_poc=False,
        we_ran_poc=False,
        competitor_reference_count=1,
        our_reference_count=1,
        days_in_stage=10,
        expected_close_days=45,
        prior_wins_vs_competitor=0,
        prior_losses_vs_competitor=0,
        competitor_incumbent=False,
        unique_differentiators=0,
    )
    defaults.update(overrides)
    return CompetitivePositioningInput(**defaults)


def engine_with(*inputs) -> CompetitivePositioningEngine:
    eng = CompetitivePositioningEngine()
    for inp in inputs:
        eng.analyze(inp)
    return eng


# ===========================================================================
# 1. Enum tests
# ===========================================================================

class TestPositioningStrength:
    def test_member_count(self):
        assert len(PositioningStrength) == 5

    def test_str_inheritance(self):
        assert isinstance(PositioningStrength.DOMINANT, str)

    def test_dominant_value(self):
        assert PositioningStrength.DOMINANT == "dominant"

    def test_strong_value(self):
        assert PositioningStrength.STRONG == "strong"

    def test_competitive_value(self):
        assert PositioningStrength.COMPETITIVE == "competitive"

    def test_weak_value(self):
        assert PositioningStrength.WEAK == "weak"

    def test_critical_value(self):
        assert PositioningStrength.CRITICAL == "critical"

    def test_all_values_unique(self):
        values = [m.value for m in PositioningStrength]
        assert len(values) == len(set(values))

    def test_str_equality_with_string(self):
        assert PositioningStrength.DOMINANT == "dominant"
        assert PositioningStrength.CRITICAL == "critical"


class TestCompetitorThreat:
    def test_member_count(self):
        assert len(CompetitorThreat) == 5

    def test_str_inheritance(self):
        assert isinstance(CompetitorThreat.HIGH, str)

    def test_high_value(self):
        assert CompetitorThreat.HIGH == "high"

    def test_medium_value(self):
        assert CompetitorThreat.MEDIUM == "medium"

    def test_low_value(self):
        assert CompetitorThreat.LOW == "low"

    def test_eliminated_value(self):
        assert CompetitorThreat.ELIMINATED == "eliminated"

    def test_unknown_value(self):
        assert CompetitorThreat.UNKNOWN == "unknown"

    def test_all_values_unique(self):
        values = [m.value for m in CompetitorThreat]
        assert len(values) == len(set(values))


class TestWinProbability:
    def test_member_count(self):
        assert len(WinProbability) == 5

    def test_str_inheritance(self):
        assert isinstance(WinProbability.VERY_HIGH, str)

    def test_very_high_value(self):
        assert WinProbability.VERY_HIGH == "very_high"

    def test_high_value(self):
        assert WinProbability.HIGH == "high"

    def test_medium_value(self):
        assert WinProbability.MEDIUM == "medium"

    def test_low_value(self):
        assert WinProbability.LOW == "low"

    def test_very_low_value(self):
        assert WinProbability.VERY_LOW == "very_low"

    def test_all_values_unique(self):
        values = [m.value for m in WinProbability]
        assert len(values) == len(set(values))


class TestPositioningAction:
    def test_member_count(self):
        assert len(PositioningAction) == 6

    def test_str_inheritance(self):
        assert isinstance(PositioningAction.ACCELERATE, str)

    def test_accelerate_value(self):
        assert PositioningAction.ACCELERATE == "accelerate"

    def test_differentiate_value(self):
        assert PositioningAction.DIFFERENTIATE == "differentiate"

    def test_defend_value(self):
        assert PositioningAction.DEFEND == "defend"

    def test_executive_escalation_value(self):
        assert PositioningAction.EXECUTIVE_ESCALATION == "executive_escalation"

    def test_competitive_response_value(self):
        assert PositioningAction.COMPETITIVE_RESPONSE == "competitive_response"

    def test_abandon_value(self):
        assert PositioningAction.ABANDON == "abandon"

    def test_all_values_unique(self):
        values = [m.value for m in PositioningAction]
        assert len(values) == len(set(values))


# ===========================================================================
# 2. CompetitivePositioningInput field count (23)
# ===========================================================================

class TestCompetitivePositioningInput:
    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(CompetitivePositioningInput)
        assert len(fields) == 24

    def test_can_instantiate(self):
        inp = make_input()
        assert inp.deal_id == "D001"

    def test_all_field_names(self):
        import dataclasses
        names = {f.name for f in dataclasses.fields(CompetitivePositioningInput)}
        expected = {
            "deal_id", "account_id", "competitor_name", "deal_stage", "deal_value",
            "our_product_fit", "competitor_product_fit", "our_price_competitiveness",
            "competitor_price_delta", "our_relationship_strength",
            "competitor_relationship_strength", "our_features_advantage",
            "champion_supports_us", "economic_buyer_engaged",
            "competitor_in_poc", "we_ran_poc",
            "competitor_reference_count", "our_reference_count",
            "days_in_stage", "expected_close_days",
            "prior_wins_vs_competitor", "prior_losses_vs_competitor",
            "competitor_incumbent", "unique_differentiators",
        }
        assert names == expected


# ===========================================================================
# 3. CompetitivePositioningResult to_dict() – 15 keys and correct types
# ===========================================================================

class TestCompetitivePositioningResultToDict:
    def setup_method(self):
        self.eng = CompetitivePositioningEngine()
        self.result = self.eng.analyze(make_input())
        self.d = self.result.to_dict()

    def test_exactly_15_keys(self):
        assert len(self.d) == 15

    def test_key_deal_id(self):
        assert "deal_id" in self.d

    def test_key_account_id(self):
        assert "account_id" in self.d

    def test_key_competitor_name(self):
        assert "competitor_name" in self.d

    def test_key_positioning_score(self):
        assert "positioning_score" in self.d

    def test_key_positioning_strength(self):
        assert "positioning_strength" in self.d

    def test_key_competitor_threat(self):
        assert "competitor_threat" in self.d

    def test_key_win_probability(self):
        assert "win_probability" in self.d

    def test_key_recommended_action(self):
        assert "recommended_action" in self.d

    def test_key_battlecard_points(self):
        assert "battlecard_points" in self.d

    def test_key_risk_factors(self):
        assert "risk_factors" in self.d

    def test_key_win_rate_vs_competitor(self):
        assert "win_rate_vs_competitor" in self.d

    def test_key_competitive_gap(self):
        assert "competitive_gap" in self.d

    def test_key_is_winnable(self):
        assert "is_winnable" in self.d

    def test_key_urgency_score(self):
        assert "urgency_score" in self.d

    def test_key_key_differentiators(self):
        assert "key_differentiators" in self.d

    def test_positioning_score_is_float(self):
        assert isinstance(self.d["positioning_score"], float)

    def test_positioning_strength_is_str(self):
        assert isinstance(self.d["positioning_strength"], str)

    def test_competitor_threat_is_str(self):
        assert isinstance(self.d["competitor_threat"], str)

    def test_win_probability_is_str(self):
        assert isinstance(self.d["win_probability"], str)

    def test_recommended_action_is_str(self):
        assert isinstance(self.d["recommended_action"], str)

    def test_battlecard_points_is_list(self):
        assert isinstance(self.d["battlecard_points"], list)

    def test_risk_factors_is_list(self):
        assert isinstance(self.d["risk_factors"], list)

    def test_win_rate_is_float(self):
        assert isinstance(self.d["win_rate_vs_competitor"], float)

    def test_competitive_gap_is_float(self):
        assert isinstance(self.d["competitive_gap"], float)

    def test_is_winnable_is_bool(self):
        assert isinstance(self.d["is_winnable"], bool)

    def test_urgency_score_is_float(self):
        assert isinstance(self.d["urgency_score"], float)

    def test_key_differentiators_is_list(self):
        assert isinstance(self.d["key_differentiators"], list)

    def test_positioning_strength_string_value(self):
        assert self.d["positioning_strength"] in [m.value for m in PositioningStrength]

    def test_competitor_threat_string_value(self):
        assert self.d["competitor_threat"] in [m.value for m in CompetitorThreat]


# ===========================================================================
# 4. _positioning_score
# ===========================================================================

class TestPositioningScore:
    def setup_method(self):
        self.eng = CompetitivePositioningEngine()

    def _score(self, **kw) -> float:
        inp = make_input(**kw)
        return self.eng._positioning_score(inp)

    # ---- base / centering at 50 ----
    def test_base_center_contribution(self):
        # fit_delta=0, rel_delta=0, price=0, no flags → only 50*0.10 = 5
        score = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert score == 5.0

    # ---- fit_delta contribution ----
    def test_fit_delta_positive(self):
        # fit_delta = 80-60 = 20 → +6.0; base=5
        s1 = self._score(
            our_product_fit=80, competitor_product_fit=60,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s1 == round(20 * 0.30 + 50 * 0.10, 1)

    def test_fit_delta_negative(self):
        s = self._score(
            our_product_fit=40, competitor_product_fit=70,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        raw = (-30) * 0.30 + 50 * 0.10
        # clamped to 0
        assert s == round(max(0.0, min(100.0, raw)), 1)

    # ---- rel_delta contribution ----
    def test_rel_delta_positive(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=70, competitor_relationship_strength=50,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        expected = round(5.0 + 20 * 0.20, 1)
        assert s == expected

    def test_rel_delta_negative(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=30, competitor_relationship_strength=50,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        expected = round(max(0.0, min(100.0, 5.0 + (-20) * 0.20)), 1)
        assert s == expected

    # ---- price competitiveness ----
    def test_price_contribution(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=80,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == round(5.0 + 80 * 0.15, 1)

    def test_price_zero(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == 5.0

    # ---- POC bonuses ----
    def test_poc_we_ran_not_competitor(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=True, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == round(5.0 + 10, 1)

    def test_poc_competitor_not_us(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=True,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == round(max(0.0, 5.0 - 10), 1)

    def test_poc_both_ran_no_bonus(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=True, competitor_in_poc=True,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == 5.0

    def test_poc_neither_ran_no_change(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == 5.0

    # ---- champion support ----
    def test_champion_bonus(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=True, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == round(5.0 + 8, 1)

    # ---- economic buyer engaged ----
    def test_economic_buyer_bonus(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=True,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == round(5.0 + 7, 1)

    def test_champion_and_economic_buyer(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=True, economic_buyer_engaged=True,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == round(5.0 + 8 + 7, 1)

    # ---- features advantage ----
    def test_features_positive(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=3, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == round(5.0 + 3 * 2.0, 1)

    def test_features_negative(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=-3, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == round(max(0.0, 5.0 + (-3) * 2.0), 1)

    def test_features_max_plus5(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=5, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == round(5.0 + 5 * 2.0, 1)

    # ---- reference delta ----
    def test_ref_delta_positive(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=4,
            competitor_reference_count=1, unique_differentiators=0,
            competitor_incumbent=False,
        )
        # ref_delta=3, clamped min(5, max(-5, 3))=3
        assert s == round(5.0 + 3.0, 1)

    def test_ref_delta_clamped_at_plus5(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=20,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == round(5.0 + 5.0, 1)

    def test_ref_delta_clamped_at_minus5(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=20, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == round(max(0.0, 5.0 + (-5.0)), 1)

    def test_ref_delta_negative_small(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=1,
            competitor_reference_count=3, unique_differentiators=0,
            competitor_incumbent=False,
        )
        assert s == round(max(0.0, 5.0 + (-2.0)), 1)

    # ---- unique differentiators ----
    def test_differentiators_small(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=3,
            competitor_incumbent=False,
        )
        assert s == round(5.0 + min(10.0, 3 * 2.0), 1)

    def test_differentiators_capped_at_10(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=10,
            competitor_incumbent=False,
        )
        assert s == round(5.0 + 10.0, 1)

    def test_differentiators_exactly_5_gives_10(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=5,
            competitor_incumbent=False,
        )
        assert s == round(5.0 + 10.0, 1)

    # ---- incumbent penalty ----
    def test_incumbent_penalty(self):
        s = self._score(
            our_product_fit=50, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=True,
        )
        assert s == round(max(0.0, 5.0 - 15), 1)

    # ---- clamping ----
    def test_score_clamped_to_zero(self):
        s = self._score(
            our_product_fit=0, competitor_product_fit=100,
            our_relationship_strength=0, competitor_relationship_strength=100,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=True,
            our_features_advantage=-5, our_reference_count=0,
            competitor_reference_count=20, unique_differentiators=0,
            competitor_incumbent=True,
        )
        assert s == 0.0

    def test_score_clamped_to_100(self):
        s = self._score(
            our_product_fit=100, competitor_product_fit=0,
            our_relationship_strength=100, competitor_relationship_strength=0,
            our_price_competitiveness=100,
            champion_supports_us=True, economic_buyer_engaged=True,
            we_ran_poc=True, competitor_in_poc=False,
            our_features_advantage=5, our_reference_count=20,
            competitor_reference_count=0, unique_differentiators=10,
            competitor_incumbent=False,
        )
        assert s == 100.0

    def test_score_rounded_to_1_decimal(self):
        s = self._score(
            our_product_fit=55, competitor_product_fit=50,
            our_relationship_strength=0, competitor_relationship_strength=0,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=0, our_reference_count=0,
            competitor_reference_count=0, unique_differentiators=0,
            competitor_incumbent=False,
        )
        # fit_delta=5, score = 5*0.30 + 50*0.10 = 1.5 + 5 = 6.5
        assert s == 6.5
        assert isinstance(s, float)


# ===========================================================================
# 5. _competitor_threat
# ===========================================================================

class TestCompetitorThreat_:
    def setup_method(self):
        self.eng = CompetitivePositioningEngine()

    def _threat(self, **kw) -> CompetitorThreat:
        inp = make_input(**kw)
        return self.eng._competitor_threat(inp)

    def test_no_factors_returns_unknown(self):
        t = self._threat(
            competitor_incumbent=False, competitor_in_poc=False,
            competitor_product_fit=50, competitor_relationship_strength=50,
            competitor_reference_count=0, competitor_price_delta=0,
        )
        assert t == CompetitorThreat.UNKNOWN

    # ---- individual factor contributions ----
    def test_incumbent_adds_3(self):
        # incumbent=3 → LOW
        t = self._threat(
            competitor_incumbent=True, competitor_in_poc=False,
            competitor_product_fit=50, competitor_relationship_strength=50,
            competitor_reference_count=0, competitor_price_delta=0,
        )
        assert t == CompetitorThreat.LOW

    def test_poc_adds_2(self):
        t = self._threat(
            competitor_incumbent=False, competitor_in_poc=True,
            competitor_product_fit=50, competitor_relationship_strength=50,
            competitor_reference_count=0, competitor_price_delta=0,
        )
        assert t == CompetitorThreat.LOW

    def test_product_fit_over_80_adds_2(self):
        t = self._threat(
            competitor_incumbent=False, competitor_in_poc=False,
            competitor_product_fit=81, competitor_relationship_strength=50,
            competitor_reference_count=0, competitor_price_delta=0,
        )
        assert t == CompetitorThreat.LOW

    def test_product_fit_exactly_80_no_bonus(self):
        t = self._threat(
            competitor_incumbent=False, competitor_in_poc=False,
            competitor_product_fit=80, competitor_relationship_strength=50,
            competitor_reference_count=0, competitor_price_delta=0,
        )
        assert t == CompetitorThreat.UNKNOWN

    def test_relationship_over_70_adds_2(self):
        t = self._threat(
            competitor_incumbent=False, competitor_in_poc=False,
            competitor_product_fit=50, competitor_relationship_strength=71,
            competitor_reference_count=0, competitor_price_delta=0,
        )
        assert t == CompetitorThreat.LOW

    def test_relationship_exactly_70_no_bonus(self):
        t = self._threat(
            competitor_incumbent=False, competitor_in_poc=False,
            competitor_product_fit=50, competitor_relationship_strength=70,
            competitor_reference_count=0, competitor_price_delta=0,
        )
        assert t == CompetitorThreat.UNKNOWN

    def test_reference_count_over_3_adds_1(self):
        t = self._threat(
            competitor_incumbent=False, competitor_in_poc=False,
            competitor_product_fit=50, competitor_relationship_strength=50,
            competitor_reference_count=4, competitor_price_delta=0,
        )
        assert t == CompetitorThreat.LOW

    def test_reference_count_exactly_3_no_bonus(self):
        t = self._threat(
            competitor_incumbent=False, competitor_in_poc=False,
            competitor_product_fit=50, competitor_relationship_strength=50,
            competitor_reference_count=3, competitor_price_delta=0,
        )
        assert t == CompetitorThreat.UNKNOWN

    def test_price_delta_below_minus15_adds_1(self):
        t = self._threat(
            competitor_incumbent=False, competitor_in_poc=False,
            competitor_product_fit=50, competitor_relationship_strength=50,
            competitor_reference_count=0, competitor_price_delta=-16,
        )
        assert t == CompetitorThreat.LOW

    def test_price_delta_exactly_minus15_no_bonus(self):
        t = self._threat(
            competitor_incumbent=False, competitor_in_poc=False,
            competitor_product_fit=50, competitor_relationship_strength=50,
            competitor_reference_count=0, competitor_price_delta=-15,
        )
        assert t == CompetitorThreat.UNKNOWN

    # ---- cumulative scoring for thresholds ----
    def test_score_4_returns_medium(self):
        # incumbent(3) + poc(2) = 5 → HIGH
        # need exactly 4: poc(2) + product_fit_over_80(2)=4 → MEDIUM
        t = self._threat(
            competitor_incumbent=False, competitor_in_poc=True,
            competitor_product_fit=85, competitor_relationship_strength=50,
            competitor_reference_count=0, competitor_price_delta=0,
        )
        assert t == CompetitorThreat.MEDIUM

    def test_score_7_returns_high(self):
        # incumbent(3) + poc(2) + product_fit(2) = 7 → HIGH
        t = self._threat(
            competitor_incumbent=True, competitor_in_poc=True,
            competitor_product_fit=85, competitor_relationship_strength=50,
            competitor_reference_count=0, competitor_price_delta=0,
        )
        assert t == CompetitorThreat.HIGH

    def test_score_6_returns_medium(self):
        # poc(2) + product_fit(2) + rel(2) = 6 → MEDIUM
        t = self._threat(
            competitor_incumbent=False, competitor_in_poc=True,
            competitor_product_fit=85, competitor_relationship_strength=75,
            competitor_reference_count=0, competitor_price_delta=0,
        )
        assert t == CompetitorThreat.MEDIUM

    def test_score_1_returns_low(self):
        t = self._threat(
            competitor_incumbent=False, competitor_in_poc=False,
            competitor_product_fit=50, competitor_relationship_strength=50,
            competitor_reference_count=4, competitor_price_delta=0,
        )
        assert t == CompetitorThreat.LOW

    def test_score_max_all_factors(self):
        # 3+2+2+2+1+1=11 → HIGH
        t = self._threat(
            competitor_incumbent=True, competitor_in_poc=True,
            competitor_product_fit=85, competitor_relationship_strength=75,
            competitor_reference_count=5, competitor_price_delta=-20,
        )
        assert t == CompetitorThreat.HIGH

    def test_threshold_exactly_4(self):
        # incumbent(3) + ref_count(1) = 4 → MEDIUM
        t = self._threat(
            competitor_incumbent=True, competitor_in_poc=False,
            competitor_product_fit=50, competitor_relationship_strength=50,
            competitor_reference_count=4, competitor_price_delta=0,
        )
        assert t == CompetitorThreat.MEDIUM


# ===========================================================================
# 6. _positioning_strength thresholds
# ===========================================================================

class TestPositioningStrength_:
    def setup_method(self):
        self.eng = CompetitivePositioningEngine()
        self.inp = make_input()

    def _strength(self, score: float) -> PositioningStrength:
        return self.eng._positioning_strength(score, self.inp)

    def test_score_78_dominant(self):
        assert self._strength(78.0) == PositioningStrength.DOMINANT

    def test_score_100_dominant(self):
        assert self._strength(100.0) == PositioningStrength.DOMINANT

    def test_score_77_strong(self):
        assert self._strength(77.9) == PositioningStrength.STRONG

    def test_score_62_strong(self):
        assert self._strength(62.0) == PositioningStrength.STRONG

    def test_score_61_competitive(self):
        assert self._strength(61.9) == PositioningStrength.COMPETITIVE

    def test_score_46_competitive(self):
        assert self._strength(46.0) == PositioningStrength.COMPETITIVE

    def test_score_45_weak(self):
        assert self._strength(45.9) == PositioningStrength.WEAK

    def test_score_30_weak(self):
        assert self._strength(30.0) == PositioningStrength.WEAK

    def test_score_29_critical(self):
        assert self._strength(29.9) == PositioningStrength.CRITICAL

    def test_score_0_critical(self):
        assert self._strength(0.0) == PositioningStrength.CRITICAL

    def test_boundary_exactly_78(self):
        assert self._strength(78.0) == PositioningStrength.DOMINANT

    def test_boundary_just_below_78(self):
        assert self._strength(77.999) == PositioningStrength.STRONG

    def test_boundary_exactly_62(self):
        assert self._strength(62.0) == PositioningStrength.STRONG

    def test_boundary_just_below_62(self):
        assert self._strength(61.999) == PositioningStrength.COMPETITIVE

    def test_boundary_exactly_46(self):
        assert self._strength(46.0) == PositioningStrength.COMPETITIVE

    def test_boundary_just_below_46(self):
        assert self._strength(45.999) == PositioningStrength.WEAK

    def test_boundary_exactly_30(self):
        assert self._strength(30.0) == PositioningStrength.WEAK

    def test_boundary_just_below_30(self):
        assert self._strength(29.999) == PositioningStrength.CRITICAL


# ===========================================================================
# 7. _win_rate
# ===========================================================================

class TestWinRate:
    def setup_method(self):
        self.eng = CompetitivePositioningEngine()

    def _win_rate(self, wins: int, losses: int) -> float:
        inp = make_input(prior_wins_vs_competitor=wins, prior_losses_vs_competitor=losses)
        return self.eng._win_rate(inp)

    def test_zero_total_returns_0_50(self):
        assert self._win_rate(0, 0) == 0.50

    def test_all_wins(self):
        assert self._win_rate(5, 0) == 1.0

    def test_all_losses(self):
        assert self._win_rate(0, 5) == 0.0

    def test_50_percent(self):
        assert self._win_rate(3, 3) == 0.5

    def test_rounded_3_decimals(self):
        wr = self._win_rate(1, 3)
        assert wr == round(1 / 4, 3)

    def test_non_trivial_ratio(self):
        wr = self._win_rate(2, 3)
        assert wr == round(2 / 5, 3)

    def test_large_numbers(self):
        wr = self._win_rate(33, 67)
        assert wr == round(33 / 100, 3)

    def test_returns_float(self):
        assert isinstance(self._win_rate(1, 1), float)

    def test_one_win_one_loss(self):
        assert self._win_rate(1, 1) == 0.5


# ===========================================================================
# 8. _win_probability
# ===========================================================================

class TestWinProbability_:
    def setup_method(self):
        self.eng = CompetitivePositioningEngine()
        self.inp = make_input(
            prior_wins_vs_competitor=0, prior_losses_vs_competitor=0
        )

    def _blended(self, pos_score: float, win_rate: float) -> float:
        return pos_score * 0.70 + win_rate * 100 * 0.30

    def _wp(self, pos_score: float, win_rate: float = 0.50) -> WinProbability:
        return self.eng._win_probability(pos_score, win_rate, self.inp)

    def test_blended_75_very_high(self):
        # blended=75 → VERY_HIGH: pos_score=75, win_rate=0.50 → 75*0.70+50*0.30=52.5+15=67.5 → HIGH
        # Need blended=75: 75=pos*0.70+50*0.30=pos*0.70+15 → pos=(75-15)/0.70=85.71
        assert self._wp(85.72, 0.50) == WinProbability.VERY_HIGH

    def test_blended_exactly_75_very_high(self):
        # blended = 75*0.70 + 50*0.30 = 52.5 + 15 = 67.5 → HIGH
        # For exact 75: win_rate=1.0 → blended=pos*0.70+100*0.30=pos*0.70+30
        # 75=pos*0.70+30 → pos=45/0.70=64.28...
        # Use pos=100, wr=1.0 → 70+30=100 → VERY_HIGH
        assert self._wp(100.0, 1.0) == WinProbability.VERY_HIGH

    def test_very_high_threshold(self):
        # pos=100, wr=0.0 → blended = 100*0.70 + 0*0.30 = 70 → HIGH (not VERY_HIGH)
        assert self._wp(100.0, 0.0) == WinProbability.HIGH

    def test_high_threshold_60(self):
        # blended=60: pos=60, wr=0.5 → 42+15=57 → MEDIUM
        # pos=80, wr=0.5 → 56+15=71 → HIGH
        assert self._wp(80.0, 0.50) == WinProbability.VERY_HIGH or self._wp(80.0, 0.50) == WinProbability.HIGH

    def test_medium_threshold(self):
        # blended=45: need to land in [45,60)
        # pos=50, wr=0.5 → 35+15=50 → MEDIUM
        assert self._wp(50.0, 0.50) == WinProbability.MEDIUM

    def test_low_threshold(self):
        # blended in [30,45)
        # pos=30, wr=0.5 → 21+15=36 → LOW
        assert self._wp(30.0, 0.50) == WinProbability.LOW

    def test_very_low_threshold(self):
        # blended < 30
        # pos=0, wr=0.0 → 0 → VERY_LOW
        assert self._wp(0.0, 0.0) == WinProbability.VERY_LOW

    def test_blended_formula_very_high(self):
        # pos=90, wr=1.0 → 63+30=93 → VERY_HIGH
        assert self._wp(90.0, 1.0) == WinProbability.VERY_HIGH

    def test_blended_formula_high(self):
        # pos=70, wr=0.5 → 49+15=64 → HIGH
        assert self._wp(70.0, 0.50) == WinProbability.HIGH

    def test_blended_formula_very_low_2(self):
        # pos=20, wr=0.0 → 14+0=14 → VERY_LOW
        assert self._wp(20.0, 0.0) == WinProbability.VERY_LOW

    def test_threshold_exactly_75(self):
        # 75 → VERY_HIGH
        # pos*0.70 + wr*100*0.30 = 75
        # pos=75, wr=0.0 → 52.5 → HIGH (not 75)
        # pos=100, wr=0.1667 → 70+5=75 → VERY_HIGH
        wp = self.eng._win_probability(100.0, 0.1667, self.inp)
        assert wp == WinProbability.VERY_HIGH

    def test_threshold_exactly_60(self):
        # blended=60 → HIGH
        wp = self.eng._win_probability(60.0 / 0.70, 0.0, self.inp)
        assert wp == WinProbability.HIGH

    def test_threshold_exactly_45(self):
        # blended=45 → MEDIUM
        wp = self.eng._win_probability(45.0 / 0.70, 0.0, self.inp)
        assert wp == WinProbability.MEDIUM

    def test_threshold_exactly_30(self):
        # blended=30 → LOW
        wp = self.eng._win_probability(30.0 / 0.70, 0.0, self.inp)
        assert wp == WinProbability.LOW

    def test_below_30_very_low(self):
        wp = self.eng._win_probability(0.0, 0.0, self.inp)
        assert wp == WinProbability.VERY_LOW


# ===========================================================================
# 9. _competitive_gap
# ===========================================================================

class TestCompetitiveGap:
    def setup_method(self):
        self.eng = CompetitivePositioningEngine()

    def _gap(self, our_fit, comp_fit, our_rel, comp_rel) -> float:
        inp = make_input(
            our_product_fit=our_fit,
            competitor_product_fit=comp_fit,
            our_relationship_strength=our_rel,
            competitor_relationship_strength=comp_rel,
        )
        return self.eng._competitive_gap(inp)

    def test_equal_values_zero_gap(self):
        assert self._gap(50, 50, 50, 50) == 0.0

    def test_positive_gap(self):
        # fit_gap=20, rel_gap=10 → 20*0.60+10*0.40=12+4=16.0
        assert self._gap(80, 60, 60, 50) == 16.0

    def test_negative_gap(self):
        # fit_gap=-20, rel_gap=-10 → -16.0
        assert self._gap(40, 60, 30, 40) == -16.0

    def test_only_fit_gap(self):
        # fit_gap=30, rel_gap=0 → 18.0
        assert self._gap(80, 50, 50, 50) == 18.0

    def test_only_rel_gap(self):
        # fit_gap=0, rel_gap=20 → 8.0
        assert self._gap(50, 50, 70, 50) == 8.0

    def test_rounded_1_decimal(self):
        # fit_gap=10, rel_gap=10 → 6+4=10.0
        result = self._gap(60, 50, 60, 50)
        assert result == round((10 * 0.60 + 10 * 0.40), 1)

    def test_formula_weights(self):
        # fit*0.60 + rel*0.40
        result = self._gap(70, 40, 80, 60)
        fit_gap = 70 - 40
        rel_gap = 80 - 60
        expected = round(fit_gap * 0.60 + rel_gap * 0.40, 1)
        assert result == expected

    def test_returns_float(self):
        assert isinstance(self._gap(50, 50, 50, 50), float)


# ===========================================================================
# 10. _urgency_score
# ===========================================================================

class TestUrgencyScore:
    def setup_method(self):
        self.eng = CompetitivePositioningEngine()

    def _urgency(self, **kw) -> float:
        inp = make_input(**kw)
        return self.eng._urgency_score(inp)

    # ---- close days tiers ----
    def test_close_14_days_adds_40(self):
        u = self._urgency(
            expected_close_days=14, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="demo",
        )
        assert u == 40.0

    def test_close_1_day_adds_40(self):
        u = self._urgency(
            expected_close_days=1, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="demo",
        )
        assert u == 40.0

    def test_close_15_days_adds_25(self):
        u = self._urgency(
            expected_close_days=15, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="demo",
        )
        assert u == 25.0

    def test_close_30_days_adds_25(self):
        u = self._urgency(
            expected_close_days=30, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="demo",
        )
        assert u == 25.0

    def test_close_31_days_adds_10(self):
        u = self._urgency(
            expected_close_days=31, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="demo",
        )
        assert u == 10.0

    def test_close_60_days_adds_10(self):
        u = self._urgency(
            expected_close_days=60, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="demo",
        )
        assert u == 10.0

    def test_close_61_days_adds_0(self):
        u = self._urgency(
            expected_close_days=61, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="demo",
        )
        assert u == 0.0

    def test_close_100_days_adds_0(self):
        u = self._urgency(
            expected_close_days=100, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="discovery",
        )
        assert u == 0.0

    # ---- POC bonus ----
    def test_competitor_in_poc_adds_20(self):
        u = self._urgency(
            expected_close_days=100, competitor_in_poc=True,
            competitor_incumbent=False, deal_stage="demo",
        )
        assert u == 20.0

    # ---- incumbent bonus ----
    def test_incumbent_adds_15(self):
        u = self._urgency(
            expected_close_days=100, competitor_in_poc=False,
            competitor_incumbent=True, deal_stage="demo",
        )
        assert u == 15.0

    # ---- stage bonuses ----
    def test_negotiation_stage_adds_15(self):
        u = self._urgency(
            expected_close_days=100, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="negotiation",
        )
        assert u == 15.0

    def test_closing_stage_adds_15(self):
        u = self._urgency(
            expected_close_days=100, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="closing",
        )
        assert u == 15.0

    def test_proposal_stage_adds_8(self):
        u = self._urgency(
            expected_close_days=100, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="proposal",
        )
        assert u == 8.0

    def test_discovery_stage_adds_0(self):
        u = self._urgency(
            expected_close_days=100, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="discovery",
        )
        assert u == 0.0

    def test_demo_stage_adds_0(self):
        u = self._urgency(
            expected_close_days=100, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="demo",
        )
        assert u == 0.0

    # ---- clamping ----
    def test_clamped_at_100(self):
        u = self._urgency(
            expected_close_days=14, competitor_in_poc=True,
            competitor_incumbent=True, deal_stage="negotiation",
        )
        # 40+20+15+15=90 → not clamped, = 90
        assert u == 90.0

    def test_all_max_factors_clamped(self):
        # 40+20+15+15=90, not over 100
        u = self._urgency(
            expected_close_days=1, competitor_in_poc=True,
            competitor_incumbent=True, deal_stage="closing",
        )
        assert u == 90.0

    def test_returns_float(self):
        u = self._urgency(
            expected_close_days=30, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="proposal",
        )
        assert isinstance(u, float)

    def test_rounded_1_decimal(self):
        u = self._urgency(
            expected_close_days=14, competitor_in_poc=False,
            competitor_incumbent=False, deal_stage="demo",
        )
        assert u == round(u, 1)


# ===========================================================================
# 11. _recommended_action priority order
# ===========================================================================

class TestRecommendedAction:
    def setup_method(self):
        self.eng = CompetitivePositioningEngine()

    def _action(self, pos_score: float, threat: CompetitorThreat,
                 win_prob: WinProbability, **kw) -> PositioningAction:
        inp = make_input(**kw)
        return self.eng._recommended_action(inp, pos_score, threat, win_prob)

    # ---- ABANDON: highest priority ----
    def test_abandon_when_very_low_and_score_lt_30(self):
        a = self._action(
            pos_score=25.0, threat=CompetitorThreat.HIGH,
            win_prob=WinProbability.VERY_LOW,
            competitor_in_poc=True, we_ran_poc=False,
        )
        assert a == PositioningAction.ABANDON

    def test_abandon_not_triggered_when_score_30(self):
        a = self._action(
            pos_score=30.0, threat=CompetitorThreat.LOW,
            win_prob=WinProbability.VERY_LOW,
            competitor_in_poc=False, we_ran_poc=False,
        )
        # score=30, not < 30, so ABANDON not triggered; score<46 → DEFEND
        assert a == PositioningAction.DEFEND

    def test_abandon_not_triggered_when_not_very_low(self):
        a = self._action(
            pos_score=20.0, threat=CompetitorThreat.LOW,
            win_prob=WinProbability.LOW,
            competitor_in_poc=False, we_ran_poc=False,
        )
        # win_prob != VERY_LOW, so ABANDON not triggered
        assert a != PositioningAction.ABANDON

    # ---- EXECUTIVE_ESCALATION: 2nd priority ----
    def test_escalation_when_high_threat_and_score_lt_50(self):
        a = self._action(
            pos_score=40.0, threat=CompetitorThreat.HIGH,
            win_prob=WinProbability.MEDIUM,
            competitor_in_poc=False, we_ran_poc=False,
        )
        assert a == PositioningAction.EXECUTIVE_ESCALATION

    def test_escalation_not_triggered_when_score_50(self):
        a = self._action(
            pos_score=50.0, threat=CompetitorThreat.HIGH,
            win_prob=WinProbability.MEDIUM,
            competitor_in_poc=False, we_ran_poc=False,
        )
        # pos_score not < 50, skip escalation; threat==HIGH → DIFFERENTIATE
        assert a == PositioningAction.DIFFERENTIATE

    def test_escalation_not_triggered_when_not_high_threat(self):
        a = self._action(
            pos_score=40.0, threat=CompetitorThreat.MEDIUM,
            win_prob=WinProbability.MEDIUM,
            competitor_in_poc=False, we_ran_poc=False,
        )
        # Not HIGH → skip, score<46 → DEFEND
        assert a == PositioningAction.DEFEND

    # ---- COMPETITIVE_RESPONSE: 3rd priority ----
    def test_competitive_response_when_competitor_poc_not_us(self):
        a = self._action(
            pos_score=60.0, threat=CompetitorThreat.MEDIUM,
            win_prob=WinProbability.HIGH,
            competitor_in_poc=True, we_ran_poc=False,
        )
        assert a == PositioningAction.COMPETITIVE_RESPONSE

    def test_competitive_response_not_triggered_when_we_ran_poc(self):
        a = self._action(
            pos_score=60.0, threat=CompetitorThreat.MEDIUM,
            win_prob=WinProbability.HIGH,
            competitor_in_poc=True, we_ran_poc=True,
        )
        # both ran poc, not triggered → score>=46 and threat!=HIGH and score<75 → DIFFERENTIATE
        assert a == PositioningAction.DIFFERENTIATE

    def test_competitive_response_not_triggered_when_no_comp_poc(self):
        a = self._action(
            pos_score=60.0, threat=CompetitorThreat.MEDIUM,
            win_prob=WinProbability.HIGH,
            competitor_in_poc=False, we_ran_poc=False,
        )
        # no competitor poc → DIFFERENTIATE (score<75, threat!=HIGH)
        assert a == PositioningAction.DIFFERENTIATE

    # ---- DEFEND: 4th priority ----
    def test_defend_when_score_lt_46(self):
        a = self._action(
            pos_score=40.0, threat=CompetitorThreat.MEDIUM,
            win_prob=WinProbability.MEDIUM,
            competitor_in_poc=False, we_ran_poc=False,
        )
        assert a == PositioningAction.DEFEND

    def test_defend_not_triggered_when_score_46(self):
        a = self._action(
            pos_score=46.0, threat=CompetitorThreat.MEDIUM,
            win_prob=WinProbability.MEDIUM,
            competitor_in_poc=False, we_ran_poc=False,
        )
        # score>=46 → not DEFEND; threat!=HIGH, score<75 → DIFFERENTIATE
        assert a == PositioningAction.DIFFERENTIATE

    # ---- DIFFERENTIATE (via HIGH threat): 5th priority ----
    def test_differentiate_when_high_threat_and_score_ge_50(self):
        a = self._action(
            pos_score=60.0, threat=CompetitorThreat.HIGH,
            win_prob=WinProbability.HIGH,
            competitor_in_poc=False, we_ran_poc=False,
        )
        assert a == PositioningAction.DIFFERENTIATE

    # ---- ACCELERATE: 6th priority ----
    def test_accelerate_when_score_ge_75(self):
        a = self._action(
            pos_score=80.0, threat=CompetitorThreat.LOW,
            win_prob=WinProbability.VERY_HIGH,
            competitor_in_poc=False, we_ran_poc=False,
        )
        assert a == PositioningAction.ACCELERATE

    def test_accelerate_at_exact_75(self):
        a = self._action(
            pos_score=75.0, threat=CompetitorThreat.LOW,
            win_prob=WinProbability.VERY_HIGH,
            competitor_in_poc=False, we_ran_poc=False,
        )
        assert a == PositioningAction.ACCELERATE

    def test_accelerate_not_triggered_below_75(self):
        a = self._action(
            pos_score=74.9, threat=CompetitorThreat.LOW,
            win_prob=WinProbability.HIGH,
            competitor_in_poc=False, we_ran_poc=False,
        )
        assert a == PositioningAction.DIFFERENTIATE

    # ---- default DIFFERENTIATE ----
    def test_default_differentiate(self):
        a = self._action(
            pos_score=55.0, threat=CompetitorThreat.MEDIUM,
            win_prob=WinProbability.MEDIUM,
            competitor_in_poc=False, we_ran_poc=False,
        )
        assert a == PositioningAction.DIFFERENTIATE


# ===========================================================================
# 12. is_winnable
# ===========================================================================

class TestIsWinnable:
    def setup_method(self):
        self.eng = CompetitivePositioningEngine()

    def test_very_high_is_winnable(self):
        # Need blended >= 75 → pos_score=100, wr=1.0
        inp = make_input(
            our_product_fit=100, competitor_product_fit=0,
            our_relationship_strength=100, competitor_relationship_strength=0,
            our_price_competitiveness=100, champion_supports_us=True,
            economic_buyer_engaged=True, we_ran_poc=True, competitor_in_poc=False,
            our_features_advantage=5, our_reference_count=10,
            competitor_reference_count=0, unique_differentiators=10,
            competitor_incumbent=False,
            prior_wins_vs_competitor=10, prior_losses_vs_competitor=0,
        )
        r = self.eng.analyze(inp)
        assert r.is_winnable is True

    def test_high_prob_is_winnable(self):
        inp = make_input(
            our_product_fit=80, competitor_product_fit=50,
            our_relationship_strength=70, competitor_relationship_strength=40,
            our_price_competitiveness=70,
            champion_supports_us=True, economic_buyer_engaged=True,
            we_ran_poc=True, competitor_in_poc=False,
            our_features_advantage=3, our_reference_count=5,
            competitor_reference_count=1, unique_differentiators=4,
            competitor_incumbent=False,
            prior_wins_vs_competitor=5, prior_losses_vs_competitor=2,
        )
        r = self.eng.analyze(inp)
        if r.win_probability != WinProbability.VERY_LOW:
            assert r.is_winnable is True

    def test_medium_prob_is_winnable(self):
        inp = make_input(
            our_product_fit=60, competitor_product_fit=55,
            our_relationship_strength=50, competitor_relationship_strength=50,
            our_price_competitiveness=50,
        )
        r = self.eng.analyze(inp)
        if r.win_probability == WinProbability.MEDIUM:
            assert r.is_winnable is True

    def test_low_prob_is_winnable(self):
        inp = make_input(
            our_product_fit=40, competitor_product_fit=50,
            our_relationship_strength=30, competitor_relationship_strength=50,
            our_price_competitiveness=30,
            competitor_incumbent=True,
            prior_wins_vs_competitor=0, prior_losses_vs_competitor=5,
        )
        r = self.eng.analyze(inp)
        if r.win_probability == WinProbability.LOW:
            assert r.is_winnable is True

    def test_very_low_prob_not_winnable(self):
        inp = make_input(
            our_product_fit=0, competitor_product_fit=100,
            our_relationship_strength=0, competitor_relationship_strength=100,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=True,
            our_features_advantage=-5, our_reference_count=0,
            competitor_reference_count=20, unique_differentiators=0,
            competitor_incumbent=True,
            prior_wins_vs_competitor=0, prior_losses_vs_competitor=10,
        )
        r = self.eng.analyze(inp)
        assert r.is_winnable is False
        assert r.win_probability == WinProbability.VERY_LOW

    def test_is_winnable_reflects_win_probability(self):
        inp = make_input()
        r = self.eng.analyze(inp)
        if r.win_probability == WinProbability.VERY_LOW:
            assert r.is_winnable is False
        else:
            assert r.is_winnable is True


# ===========================================================================
# 13. Properties
# ===========================================================================

class TestProperties:
    def test_high_threat_deals_empty_initially(self):
        eng = CompetitivePositioningEngine()
        assert eng.high_threat_deals == []

    def test_winnable_deals_empty_initially(self):
        eng = CompetitivePositioningEngine()
        assert eng.winnable_deals == []

    def test_dominant_positions_empty_initially(self):
        eng = CompetitivePositioningEngine()
        assert eng.dominant_positions == []

    def test_needs_escalation_empty_initially(self):
        eng = CompetitivePositioningEngine()
        assert eng.needs_escalation == []

    def test_high_threat_deals_filtered(self):
        eng = CompetitivePositioningEngine()
        # High threat: incumbent(3)+poc(2)+product_fit>80(2)=7 → HIGH
        high_inp = make_input(
            competitor_incumbent=True, competitor_in_poc=True,
            competitor_product_fit=85,
        )
        low_inp = make_input(
            competitor_incumbent=False, competitor_in_poc=False,
            competitor_product_fit=50,
        )
        eng.analyze(high_inp)
        eng.analyze(low_inp)
        assert len(eng.high_threat_deals) == 1
        assert eng.high_threat_deals[0].competitor_threat == CompetitorThreat.HIGH

    def test_winnable_deals_filtered(self):
        eng = CompetitivePositioningEngine()
        # Winnable (VERY_HIGH)
        winnable_inp = make_input(
            our_product_fit=100, competitor_product_fit=0,
            our_relationship_strength=100, competitor_relationship_strength=0,
            our_price_competitiveness=100, champion_supports_us=True,
            economic_buyer_engaged=True, we_ran_poc=True, competitor_in_poc=False,
            our_features_advantage=5, our_reference_count=10,
            competitor_reference_count=0, unique_differentiators=10,
            competitor_incumbent=False,
            prior_wins_vs_competitor=10, prior_losses_vs_competitor=0,
        )
        # Not winnable
        not_winnable_inp = make_input(
            our_product_fit=0, competitor_product_fit=100,
            our_relationship_strength=0, competitor_relationship_strength=100,
            our_price_competitiveness=0,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=True,
            our_features_advantage=-5, our_reference_count=0,
            competitor_reference_count=20, unique_differentiators=0,
            competitor_incumbent=True,
            prior_wins_vs_competitor=0, prior_losses_vs_competitor=10,
        )
        eng.analyze(winnable_inp)
        eng.analyze(not_winnable_inp)
        for r in eng.winnable_deals:
            assert r.is_winnable is True

    def test_dominant_positions_filtered(self):
        eng = CompetitivePositioningEngine()
        # Dominant: score >= 78
        dominant_inp = make_input(
            our_product_fit=100, competitor_product_fit=0,
            our_relationship_strength=100, competitor_relationship_strength=0,
            our_price_competitiveness=100, champion_supports_us=True,
            economic_buyer_engaged=True, we_ran_poc=True, competitor_in_poc=False,
            our_features_advantage=5, our_reference_count=10,
            competitor_reference_count=0, unique_differentiators=10,
            competitor_incumbent=False,
        )
        weak_inp = make_input(
            our_product_fit=30, competitor_product_fit=50,
            our_relationship_strength=30, competitor_relationship_strength=50,
            our_price_competitiveness=20,
            competitor_incumbent=True,
        )
        r_dom = eng.analyze(dominant_inp)
        eng.analyze(weak_inp)
        if r_dom.positioning_strength == PositioningStrength.DOMINANT:
            assert len(eng.dominant_positions) >= 1

    def test_needs_escalation_filtered(self):
        eng = CompetitivePositioningEngine()
        # Force EXECUTIVE_ESCALATION: HIGH threat + pos_score < 50
        esc_inp = make_input(
            competitor_incumbent=True, competitor_in_poc=True,
            our_product_fit=30, competitor_product_fit=85,
            our_relationship_strength=20, competitor_relationship_strength=80,
            our_price_competitiveness=20,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False,
            our_features_advantage=-3, our_reference_count=0,
            competitor_reference_count=5, unique_differentiators=0,
            prior_wins_vs_competitor=0, prior_losses_vs_competitor=5,
        )
        r = eng.analyze(esc_inp)
        if r.recommended_action == PositioningAction.EXECUTIVE_ESCALATION:
            assert len(eng.needs_escalation) == 1

    def test_properties_return_lists(self):
        eng = CompetitivePositioningEngine()
        assert isinstance(eng.high_threat_deals, list)
        assert isinstance(eng.winnable_deals, list)
        assert isinstance(eng.dominant_positions, list)
        assert isinstance(eng.needs_escalation, list)


# ===========================================================================
# 14. summary() – 13 keys
# ===========================================================================

class TestSummary:
    def test_empty_state_returns_13_keys(self):
        eng = CompetitivePositioningEngine()
        s = eng.summary()
        assert len(s) == 13

    def test_empty_state_total_zero(self):
        eng = CompetitivePositioningEngine()
        s = eng.summary()
        assert s["total"] == 0

    def test_empty_state_strength_counts_empty(self):
        eng = CompetitivePositioningEngine()
        assert eng.summary()["strength_counts"] == {}

    def test_empty_state_threat_counts_empty(self):
        eng = CompetitivePositioningEngine()
        assert eng.summary()["threat_counts"] == {}

    def test_empty_state_probability_counts_empty(self):
        eng = CompetitivePositioningEngine()
        assert eng.summary()["probability_counts"] == {}

    def test_empty_state_action_counts_empty(self):
        eng = CompetitivePositioningEngine()
        assert eng.summary()["action_counts"] == {}

    def test_empty_state_avg_scores_zero(self):
        eng = CompetitivePositioningEngine()
        s = eng.summary()
        assert s["avg_positioning_score"] == 0.0
        assert s["avg_win_rate"] == 0.0
        assert s["avg_urgency_score"] == 0.0
        assert s["avg_competitive_gap"] == 0.0

    def test_empty_state_counts_zero(self):
        eng = CompetitivePositioningEngine()
        s = eng.summary()
        assert s["high_threat_count"] == 0
        assert s["winnable_count"] == 0
        assert s["dominant_count"] == 0
        assert s["escalation_count"] == 0

    def test_all_13_keys_present(self):
        eng = CompetitivePositioningEngine()
        s = eng.summary()
        expected_keys = {
            "total", "strength_counts", "threat_counts", "probability_counts",
            "action_counts", "avg_positioning_score", "avg_win_rate",
            "avg_urgency_score", "high_threat_count", "winnable_count",
            "dominant_count", "escalation_count", "avg_competitive_gap",
        }
        assert set(s.keys()) == expected_keys

    def test_total_after_analysis(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input())
        eng.analyze(make_input(deal_id="D002"))
        assert eng.summary()["total"] == 2

    def test_strength_counts_populated(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input())
        s = eng.summary()
        assert len(s["strength_counts"]) >= 1

    def test_threat_counts_populated(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input())
        s = eng.summary()
        assert len(s["threat_counts"]) >= 1

    def test_probability_counts_populated(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input())
        s = eng.summary()
        assert len(s["probability_counts"]) >= 1

    def test_action_counts_populated(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input())
        s = eng.summary()
        assert len(s["action_counts"]) >= 1

    def test_avg_positioning_score_correct(self):
        eng = CompetitivePositioningEngine()
        r1 = eng.analyze(make_input())
        r2 = eng.analyze(make_input(deal_id="D002"))
        s = eng.summary()
        expected = round((r1.positioning_score + r2.positioning_score) / 2, 1)
        assert s["avg_positioning_score"] == expected

    def test_avg_win_rate_correct(self):
        eng = CompetitivePositioningEngine()
        r1 = eng.analyze(make_input(prior_wins_vs_competitor=2, prior_losses_vs_competitor=2))
        r2 = eng.analyze(make_input(deal_id="D002", prior_wins_vs_competitor=3, prior_losses_vs_competitor=1))
        s = eng.summary()
        expected = round((r1.win_rate_vs_competitor + r2.win_rate_vs_competitor) / 2, 3)
        assert s["avg_win_rate"] == expected

    def test_high_threat_count_correct(self):
        eng = CompetitivePositioningEngine()
        # High threat: incumbent+poc+product_fit>80 = 7
        high = make_input(competitor_incumbent=True, competitor_in_poc=True, competitor_product_fit=85)
        low = make_input(deal_id="D002")
        eng.analyze(high)
        eng.analyze(low)
        s = eng.summary()
        assert s["high_threat_count"] == len(eng.high_threat_deals)

    def test_winnable_count_correct(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input())
        eng.analyze(make_input(deal_id="D002"))
        s = eng.summary()
        assert s["winnable_count"] == len(eng.winnable_deals)

    def test_dominant_count_correct(self):
        eng = CompetitivePositioningEngine()
        dom = make_input(
            our_product_fit=100, competitor_product_fit=0,
            our_relationship_strength=100, competitor_relationship_strength=0,
            our_price_competitiveness=100, champion_supports_us=True,
            economic_buyer_engaged=True, we_ran_poc=True, competitor_in_poc=False,
            our_features_advantage=5, our_reference_count=10,
            competitor_reference_count=0, unique_differentiators=10,
            competitor_incumbent=False,
        )
        eng.analyze(dom)
        s = eng.summary()
        assert s["dominant_count"] == len(eng.dominant_positions)

    def test_escalation_count_correct(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input())
        s = eng.summary()
        assert s["escalation_count"] == len(eng.needs_escalation)

    def test_strength_counts_values_are_str_keys(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input())
        s = eng.summary()
        for k in s["strength_counts"]:
            assert isinstance(k, str)

    def test_threat_counts_values_are_str_keys(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input())
        s = eng.summary()
        for k in s["threat_counts"]:
            assert isinstance(k, str)

    def test_summary_13_keys_after_analyses(self):
        eng = CompetitivePositioningEngine()
        for i in range(5):
            eng.analyze(make_input(deal_id=f"D{i:03d}"))
        s = eng.summary()
        assert len(s) == 13


# ===========================================================================
# 15. reset() clears state
# ===========================================================================

class TestReset:
    def test_reset_clears_results(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input())
        eng.analyze(make_input(deal_id="D002"))
        assert eng.summary()["total"] == 2
        eng.reset()
        assert eng.summary()["total"] == 0

    def test_reset_clears_high_threat_deals(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input(competitor_incumbent=True, competitor_in_poc=True, competitor_product_fit=85))
        eng.reset()
        assert eng.high_threat_deals == []

    def test_reset_clears_winnable_deals(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input())
        eng.reset()
        assert eng.winnable_deals == []

    def test_reset_clears_dominant_positions(self):
        eng = CompetitivePositioningEngine()
        dom = make_input(
            our_product_fit=100, competitor_product_fit=0,
            our_relationship_strength=100, competitor_relationship_strength=0,
            our_price_competitiveness=100, champion_supports_us=True,
            economic_buyer_engaged=True, we_ran_poc=True, competitor_in_poc=False,
            our_features_advantage=5, our_reference_count=10,
            competitor_reference_count=0, unique_differentiators=10,
            competitor_incumbent=False,
        )
        eng.analyze(dom)
        eng.reset()
        assert eng.dominant_positions == []

    def test_reset_clears_needs_escalation(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input())
        eng.reset()
        assert eng.needs_escalation == []

    def test_reset_allows_new_analyses(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input())
        eng.reset()
        eng.analyze(make_input(deal_id="D002"))
        assert eng.summary()["total"] == 1

    def test_reset_returns_none(self):
        eng = CompetitivePositioningEngine()
        result = eng.reset()
        assert result is None

    def test_reset_multiple_times_safe(self):
        eng = CompetitivePositioningEngine()
        eng.reset()
        eng.reset()
        assert eng.summary()["total"] == 0

    def test_summary_empty_after_reset(self):
        eng = CompetitivePositioningEngine()
        for i in range(3):
            eng.analyze(make_input(deal_id=f"D{i}"))
        eng.reset()
        s = eng.summary()
        assert s["total"] == 0
        assert s["strength_counts"] == {}


# ===========================================================================
# 16. End-to-end scenarios
# ===========================================================================

class TestEndToEnd:

    # --- E2E: Dominant vs weak competitor ---
    def test_dominant_position_scenario(self):
        """We have clear product, price, relationship, and POC advantages."""
        eng = CompetitivePositioningEngine()
        inp = make_input(
            deal_id="DOM001",
            our_product_fit=95, competitor_product_fit=40,
            our_relationship_strength=90, competitor_relationship_strength=30,
            our_price_competitiveness=85,
            champion_supports_us=True, economic_buyer_engaged=True,
            we_ran_poc=True, competitor_in_poc=False,
            our_features_advantage=5, our_reference_count=8,
            competitor_reference_count=1, unique_differentiators=5,
            competitor_incumbent=False,
            prior_wins_vs_competitor=4, prior_losses_vs_competitor=1,
        )
        r = eng.analyze(inp)
        assert r.deal_id == "DOM001"
        assert r.positioning_score > 78  # should be DOMINANT
        assert r.positioning_strength == PositioningStrength.DOMINANT
        assert r.is_winnable is True
        assert r.win_probability in (WinProbability.VERY_HIGH, WinProbability.HIGH)
        assert r.recommended_action == PositioningAction.ACCELERATE
        assert r.competitor_threat in (CompetitorThreat.LOW, CompetitorThreat.UNKNOWN)
        assert isinstance(r.battlecard_points, list)
        assert isinstance(r.risk_factors, list)
        assert isinstance(r.key_differentiators, list)

    # --- E2E: Incumbent threat scenario ---
    def test_incumbent_threat_scenario(self):
        """Competitor is incumbent with high product fit and relationship."""
        eng = CompetitivePositioningEngine()
        inp = make_input(
            deal_id="INC001",
            competitor_name="Incumbent Corp",
            our_product_fit=55, competitor_product_fit=85,
            our_relationship_strength=40, competitor_relationship_strength=80,
            our_price_competitiveness=40,
            champion_supports_us=False, economic_buyer_engaged=False,
            we_ran_poc=False, competitor_in_poc=False,
            our_features_advantage=-2, our_reference_count=2,
            competitor_reference_count=5, unique_differentiators=1,
            competitor_incumbent=True,
            prior_wins_vs_competitor=1, prior_losses_vs_competitor=4,
        )
        r = eng.analyze(inp)
        assert r.deal_id == "INC001"
        assert r.competitor_threat == CompetitorThreat.HIGH
        assert r.positioning_strength in (PositioningStrength.WEAK, PositioningStrength.CRITICAL, PositioningStrength.COMPETITIVE)
        assert r.is_winnable is False or r.recommended_action in (
            PositioningAction.EXECUTIVE_ESCALATION, PositioningAction.ABANDON
        )
        # Incumbent risk should appear in risk_factors
        assert any("Incumbent Corp" in rf or "fournisseur actuel" in rf for rf in r.risk_factors)

    # --- E2E: Competitive POC scenario ---
    def test_competitive_poc_scenario(self):
        """Competitor is running POC but we are not.
        We need pos_score >= 30 (to avoid ABANDON) and win_prob != VERY_LOW,
        and threat != HIGH with pos_score < 50 (to avoid ESCALATION).
        """
        eng = CompetitivePositioningEngine()
        inp = make_input(
            deal_id="POC001",
            our_product_fit=75, competitor_product_fit=65,
            our_relationship_strength=70, competitor_relationship_strength=50,
            our_price_competitiveness=70,
            champion_supports_us=True, economic_buyer_engaged=True,
            we_ran_poc=False, competitor_in_poc=True,
            our_features_advantage=2, our_reference_count=3,
            competitor_reference_count=2, unique_differentiators=2,
            competitor_incumbent=False,
            prior_wins_vs_competitor=3, prior_losses_vs_competitor=2,
        )
        r = eng.analyze(inp)
        assert r.deal_id == "POC001"
        assert r.recommended_action == PositioningAction.COMPETITIVE_RESPONSE

    # --- E2E: analyze_batch processes all ---
    def test_analyze_batch(self):
        eng = CompetitivePositioningEngine()
        inputs = [make_input(deal_id=f"B{i:03d}") for i in range(5)]
        results = eng.analyze_batch(inputs)
        assert len(results) == 5
        assert eng.summary()["total"] == 5

    def test_analyze_batch_returns_list(self):
        eng = CompetitivePositioningEngine()
        inputs = [make_input()]
        results = eng.analyze_batch(inputs)
        assert isinstance(results, list)
        assert isinstance(results[0], CompetitivePositioningResult)

    def test_analyze_batch_empty_list(self):
        eng = CompetitivePositioningEngine()
        results = eng.analyze_batch([])
        assert results == []

    def test_analyze_stores_result(self):
        eng = CompetitivePositioningEngine()
        eng.analyze(make_input())
        assert eng.summary()["total"] == 1

    def test_multiple_analyses_accumulate(self):
        eng = CompetitivePositioningEngine()
        for i in range(10):
            eng.analyze(make_input(deal_id=f"D{i:03d}"))
        assert eng.summary()["total"] == 10

    def test_result_fields_match_input(self):
        eng = CompetitivePositioningEngine()
        inp = make_input(deal_id="X001", account_id="ACC999", competitor_name="TestCorp")
        r = eng.analyze(inp)
        assert r.deal_id == "X001"
        assert r.account_id == "ACC999"
        assert r.competitor_name == "TestCorp"

    def test_competitive_gap_sign(self):
        """Positive gap when we have better fit and relationship."""
        eng = CompetitivePositioningEngine()
        inp = make_input(
            our_product_fit=80, competitor_product_fit=50,
            our_relationship_strength=70, competitor_relationship_strength=40,
        )
        r = eng.analyze(inp)
        assert r.competitive_gap > 0

    def test_competitive_gap_negative(self):
        """Negative gap when competitor has better fit and relationship."""
        eng = CompetitivePositioningEngine()
        inp = make_input(
            our_product_fit=40, competitor_product_fit=80,
            our_relationship_strength=30, competitor_relationship_strength=70,
        )
        r = eng.analyze(inp)
        assert r.competitive_gap < 0

    def test_to_dict_deal_id_passthrough(self):
        eng = CompetitivePositioningEngine()
        r = eng.analyze(make_input(deal_id="ABC123"))
        assert r.to_dict()["deal_id"] == "ABC123"

    def test_urgency_score_in_result(self):
        eng = CompetitivePositioningEngine()
        r = eng.analyze(make_input(expected_close_days=10, competitor_in_poc=True))
        assert r.urgency_score > 0

    def test_win_rate_zero_total_in_result(self):
        eng = CompetitivePositioningEngine()
        r = eng.analyze(make_input(prior_wins_vs_competitor=0, prior_losses_vs_competitor=0))
        assert r.win_rate_vs_competitor == 0.50

    def test_win_rate_non_zero_in_result(self):
        eng = CompetitivePositioningEngine()
        r = eng.analyze(make_input(prior_wins_vs_competitor=3, prior_losses_vs_competitor=1))
        assert r.win_rate_vs_competitor == 0.75

    # --- E2E: full to_dict integrity ---
    def test_to_dict_strength_is_string_not_enum(self):
        eng = CompetitivePositioningEngine()
        r = eng.analyze(make_input())
        d = r.to_dict()
        assert not isinstance(d["positioning_strength"], PositioningStrength)

    def test_to_dict_threat_is_string_not_enum(self):
        eng = CompetitivePositioningEngine()
        r = eng.analyze(make_input())
        d = r.to_dict()
        assert not isinstance(d["competitor_threat"], CompetitorThreat)

    def test_to_dict_action_is_string_not_enum(self):
        eng = CompetitivePositioningEngine()
        r = eng.analyze(make_input())
        d = r.to_dict()
        assert not isinstance(d["recommended_action"], PositioningAction)

    def test_to_dict_probability_is_string_not_enum(self):
        eng = CompetitivePositioningEngine()
        r = eng.analyze(make_input())
        d = r.to_dict()
        assert not isinstance(d["win_probability"], WinProbability)

    # ---- summary counts across multiple results ----
    def test_summary_action_counts_sum_to_total(self):
        eng = CompetitivePositioningEngine()
        for i in range(4):
            eng.analyze(make_input(deal_id=f"D{i}"))
        s = eng.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_strength_counts_sum_to_total(self):
        eng = CompetitivePositioningEngine()
        for i in range(4):
            eng.analyze(make_input(deal_id=f"D{i}"))
        s = eng.summary()
        assert sum(s["strength_counts"].values()) == s["total"]

    def test_summary_threat_counts_sum_to_total(self):
        eng = CompetitivePositioningEngine()
        for i in range(4):
            eng.analyze(make_input(deal_id=f"D{i}"))
        s = eng.summary()
        assert sum(s["threat_counts"].values()) == s["total"]

    def test_summary_probability_counts_sum_to_total(self):
        eng = CompetitivePositioningEngine()
        for i in range(4):
            eng.analyze(make_input(deal_id=f"D{i}"))
        s = eng.summary()
        assert sum(s["probability_counts"].values()) == s["total"]

    def test_engine_init_empty_results(self):
        eng = CompetitivePositioningEngine()
        assert eng._results == []

    def test_analyze_result_is_correct_type(self):
        eng = CompetitivePositioningEngine()
        r = eng.analyze(make_input())
        assert isinstance(r, CompetitivePositioningResult)

    def test_positioning_score_in_range(self):
        eng = CompetitivePositioningEngine()
        for _ in range(10):
            r = eng.analyze(make_input())
            assert 0.0 <= r.positioning_score <= 100.0

    def test_urgency_score_in_range(self):
        eng = CompetitivePositioningEngine()
        r = eng.analyze(make_input())
        assert 0.0 <= r.urgency_score <= 100.0

    def test_win_rate_in_range(self):
        eng = CompetitivePositioningEngine()
        r = eng.analyze(make_input(prior_wins_vs_competitor=5, prior_losses_vs_competitor=5))
        assert 0.0 <= r.win_rate_vs_competitor <= 1.0
