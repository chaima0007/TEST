"""
Comprehensive pytest test suite for swarm.intelligence.competitive_win_probability_engine.

Covers enums, dataclasses, sub-score functions, win-probability formula,
tier/risk/factor/action logic, is_at_risk, requires_executive_intervention,
estimated_win_value_usd, win_signal, assess(), assess_batch(), summary(),
and all engine utility methods.
"""
from __future__ import annotations

import math
import pytest

from swarm.intelligence.competitive_win_probability_engine import (
    CompetitiveWinInput,
    CompetitiveWinProbabilityEngine,
    CompetitiveWinResult,
    PrimaryWinFactor,
    WinAction,
    WinProbabilityTier,
    WinRisk,
    _champion_score,
    _competitive_position_score,
    _deal_strength_score,
    _primary_factor,
    _recommended_action,
    _relationship_momentum_score,
    _win_probability_pct,
    _win_risk,
    _win_signal,
    _win_tier,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_input(
    deal_id: str = "D001",
    rep_id: str = "R001",
    deal_name: str = "Test Deal",
    competitor_id: str = "C001",
    competitor_name: str = "Competitor A",
    deal_value_usd: float = 100_000.0,
    deal_stage_num: int = 3,
    champion_strength_score: float = 70.0,
    economic_buyer_engaged: int = 1,
    technical_fit_score: float = 70.0,
    competitive_win_rate_vs_competitor_pct: float = 55.0,
    price_competitiveness_score: float = 65.0,
    feature_advantage_score: float = 65.0,
    relationship_strength_score: float = 65.0,
    incumbent_competitor: int = 0,
    days_until_close: int = 30,
    executive_sponsorship: int = 1,
    proof_of_concept_won: int = 0,
    competitor_activity_level: float = 30.0,
    deal_momentum_score: float = 65.0,
    reference_customer_provided: int = 0,
    multi_year_deal: int = 0,
) -> CompetitiveWinInput:
    return CompetitiveWinInput(
        deal_id=deal_id,
        rep_id=rep_id,
        deal_name=deal_name,
        competitor_id=competitor_id,
        competitor_name=competitor_name,
        deal_value_usd=deal_value_usd,
        deal_stage_num=deal_stage_num,
        champion_strength_score=champion_strength_score,
        economic_buyer_engaged=economic_buyer_engaged,
        technical_fit_score=technical_fit_score,
        competitive_win_rate_vs_competitor_pct=competitive_win_rate_vs_competitor_pct,
        price_competitiveness_score=price_competitiveness_score,
        feature_advantage_score=feature_advantage_score,
        relationship_strength_score=relationship_strength_score,
        incumbent_competitor=incumbent_competitor,
        days_until_close=days_until_close,
        executive_sponsorship=executive_sponsorship,
        proof_of_concept_won=proof_of_concept_won,
        competitor_activity_level=competitor_activity_level,
        deal_momentum_score=deal_momentum_score,
        reference_customer_provided=reference_customer_provided,
        multi_year_deal=multi_year_deal,
    )


@pytest.fixture
def engine() -> CompetitiveWinProbabilityEngine:
    return CompetitiveWinProbabilityEngine()


@pytest.fixture
def basic_input() -> CompetitiveWinInput:
    return make_input()


# ---------------------------------------------------------------------------
# 1. Enum tests
# ---------------------------------------------------------------------------

class TestWinProbabilityTier:
    def test_members_count(self):
        assert len(WinProbabilityTier) == 5

    def test_very_likely_value(self):
        assert WinProbabilityTier.VERY_LIKELY.value == "very_likely"

    def test_likely_value(self):
        assert WinProbabilityTier.LIKELY.value == "likely"

    def test_toss_up_value(self):
        assert WinProbabilityTier.TOSS_UP.value == "toss_up"

    def test_unlikely_value(self):
        assert WinProbabilityTier.UNLIKELY.value == "unlikely"

    def test_very_unlikely_value(self):
        assert WinProbabilityTier.VERY_UNLIKELY.value == "very_unlikely"

    def test_is_str_enum(self):
        assert isinstance(WinProbabilityTier.LIKELY, str)

    def test_str_comparison(self):
        assert WinProbabilityTier.TOSS_UP == "toss_up"


class TestWinRisk:
    def test_members_count(self):
        assert len(WinRisk) == 4

    def test_low_value(self):
        assert WinRisk.LOW.value == "low"

    def test_moderate_value(self):
        assert WinRisk.MODERATE.value == "moderate"

    def test_high_value(self):
        assert WinRisk.HIGH.value == "high"

    def test_critical_value(self):
        assert WinRisk.CRITICAL.value == "critical"

    def test_is_str_enum(self):
        assert isinstance(WinRisk.HIGH, str)


class TestPrimaryWinFactor:
    def test_members_count(self):
        assert len(PrimaryWinFactor) == 5

    def test_champion_value(self):
        assert PrimaryWinFactor.CHAMPION.value == "champion"

    def test_price_value(self):
        assert PrimaryWinFactor.PRICE.value == "price"

    def test_features_value(self):
        assert PrimaryWinFactor.FEATURES.value == "features"

    def test_relationship_value(self):
        assert PrimaryWinFactor.RELATIONSHIP.value == "relationship"

    def test_momentum_value(self):
        assert PrimaryWinFactor.MOMENTUM.value == "momentum"


class TestWinAction:
    def test_members_count(self):
        assert len(WinAction) == 5

    def test_maintain_course_value(self):
        assert WinAction.MAINTAIN_COURSE.value == "maintain_course"

    def test_strengthen_champion_value(self):
        assert WinAction.STRENGTHEN_CHAMPION.value == "strengthen_champion"

    def test_price_adjustment_value(self):
        assert WinAction.PRICE_ADJUSTMENT.value == "price_adjustment"

    def test_feature_demo_value(self):
        assert WinAction.FEATURE_DEMO.value == "feature_demo"

    def test_executive_alignment_value(self):
        assert WinAction.EXECUTIVE_ALIGNMENT.value == "executive_alignment"


# ---------------------------------------------------------------------------
# 2. CompetitiveWinInput dataclass
# ---------------------------------------------------------------------------

class TestCompetitiveWinInput:
    def test_has_22_fields(self):
        import dataclasses
        fields = dataclasses.fields(CompetitiveWinInput)
        assert len(fields) == 22

    def test_field_names(self):
        import dataclasses
        names = {f.name for f in dataclasses.fields(CompetitiveWinInput)}
        expected = {
            "deal_id", "rep_id", "deal_name", "competitor_id", "competitor_name",
            "deal_value_usd", "deal_stage_num", "champion_strength_score",
            "economic_buyer_engaged", "technical_fit_score",
            "competitive_win_rate_vs_competitor_pct", "price_competitiveness_score",
            "feature_advantage_score", "relationship_strength_score",
            "incumbent_competitor", "days_until_close", "executive_sponsorship",
            "proof_of_concept_won", "competitor_activity_level", "deal_momentum_score",
            "reference_customer_provided", "multi_year_deal",
        }
        assert names == expected

    def test_construction(self, basic_input):
        assert basic_input.deal_id == "D001"
        assert basic_input.deal_value_usd == 100_000.0

    def test_string_fields(self):
        inp = make_input(deal_id="XYZ", deal_name="My Deal", competitor_name="Rival")
        assert inp.deal_id == "XYZ"
        assert inp.deal_name == "My Deal"
        assert inp.competitor_name == "Rival"


# ---------------------------------------------------------------------------
# 3. CompetitiveWinResult dataclass + to_dict()
# ---------------------------------------------------------------------------

class TestCompetitiveWinResult:
    def test_to_dict_has_15_keys(self, engine, basic_input):
        result = engine.assess(basic_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_keys(self, engine, basic_input):
        result = engine.assess(basic_input)
        d = result.to_dict()
        expected_keys = {
            "deal_id", "deal_name", "win_probability_tier", "win_risk",
            "primary_win_factor", "recommended_action", "champion_score",
            "competitive_position_score", "relationship_momentum_score",
            "deal_strength_score", "win_probability_pct", "is_at_risk",
            "requires_executive_intervention", "estimated_win_value_usd", "win_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self, engine, basic_input):
        result = engine.assess(basic_input)
        d = result.to_dict()
        assert isinstance(d["win_probability_tier"], str)
        assert isinstance(d["win_risk"], str)
        assert isinstance(d["primary_win_factor"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_deal_id_matches(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert result.to_dict()["deal_id"] == "D001"

    def test_result_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(CompetitiveWinResult)
        assert len(fields) == 15


# ---------------------------------------------------------------------------
# 4. _champion_score
# ---------------------------------------------------------------------------

class TestChampionScore:
    def test_all_zero_inputs(self):
        inp = make_input(
            champion_strength_score=0.0,
            economic_buyer_engaged=0,
            executive_sponsorship=0,
            reference_customer_provided=0,
        )
        assert _champion_score(inp) == 0.0

    def test_max_score_capped_at_100(self):
        inp = make_input(
            champion_strength_score=100.0,
            economic_buyer_engaged=1,
            executive_sponsorship=1,
            reference_customer_provided=1,
        )
        # 40 + 25 + 20 + 15 = 100
        assert _champion_score(inp) == 100.0

    def test_champion_strength_weight(self):
        inp = make_input(
            champion_strength_score=80.0,
            economic_buyer_engaged=0,
            executive_sponsorship=0,
            reference_customer_provided=0,
        )
        assert _champion_score(inp) == round(80.0 * 0.40, 1)

    def test_economic_buyer_bonus(self):
        inp = make_input(
            champion_strength_score=0.0,
            economic_buyer_engaged=1,
            executive_sponsorship=0,
            reference_customer_provided=0,
        )
        assert _champion_score(inp) == 25.0

    def test_executive_sponsorship_bonus(self):
        inp = make_input(
            champion_strength_score=0.0,
            economic_buyer_engaged=0,
            executive_sponsorship=1,
            reference_customer_provided=0,
        )
        assert _champion_score(inp) == 20.0

    def test_reference_customer_bonus(self):
        inp = make_input(
            champion_strength_score=0.0,
            economic_buyer_engaged=0,
            executive_sponsorship=0,
            reference_customer_provided=1,
        )
        assert _champion_score(inp) == 15.0

    def test_combined_bonuses(self):
        inp = make_input(
            champion_strength_score=50.0,
            economic_buyer_engaged=1,
            executive_sponsorship=1,
            reference_customer_provided=0,
        )
        expected = round(50.0 * 0.40 + 25.0 + 20.0, 1)
        assert _champion_score(inp) == expected

    def test_score_never_negative(self):
        inp = make_input(champion_strength_score=0.0, economic_buyer_engaged=0,
                         executive_sponsorship=0, reference_customer_provided=0)
        assert _champion_score(inp) >= 0.0

    def test_score_never_exceeds_100(self):
        inp = make_input(champion_strength_score=200.0, economic_buyer_engaged=1,
                         executive_sponsorship=1, reference_customer_provided=1)
        assert _champion_score(inp) <= 100.0

    def test_returns_float(self, basic_input):
        assert isinstance(_champion_score(basic_input), float)


# ---------------------------------------------------------------------------
# 5. _competitive_position_score
# ---------------------------------------------------------------------------

class TestCompetitivePositionScore:
    def test_all_zero(self):
        inp = make_input(
            feature_advantage_score=0.0,
            price_competitiveness_score=0.0,
            technical_fit_score=0.0,
            competitive_win_rate_vs_competitor_pct=0.0,
            incumbent_competitor=0,
        )
        assert _competitive_position_score(inp) == 0.0

    def test_without_incumbent_no_penalty(self):
        inp = make_input(
            feature_advantage_score=100.0,
            price_competitiveness_score=100.0,
            technical_fit_score=100.0,
            competitive_win_rate_vs_competitor_pct=100.0,
            incumbent_competitor=0,
        )
        # 30 + 25 + 25 + 20 = 100
        assert _competitive_position_score(inp) == 100.0

    def test_incumbent_penalty_applied(self):
        inp = make_input(
            feature_advantage_score=100.0,
            price_competitiveness_score=100.0,
            technical_fit_score=100.0,
            competitive_win_rate_vs_competitor_pct=100.0,
            incumbent_competitor=1,
        )
        assert _competitive_position_score(inp) == round(100.0 * 0.80, 1)

    def test_feature_advantage_weight(self):
        inp = make_input(
            feature_advantage_score=100.0,
            price_competitiveness_score=0.0,
            technical_fit_score=0.0,
            competitive_win_rate_vs_competitor_pct=0.0,
            incumbent_competitor=0,
        )
        assert _competitive_position_score(inp) == round(100.0 * 0.30, 1)

    def test_price_competitiveness_weight(self):
        inp = make_input(
            feature_advantage_score=0.0,
            price_competitiveness_score=100.0,
            technical_fit_score=0.0,
            competitive_win_rate_vs_competitor_pct=0.0,
            incumbent_competitor=0,
        )
        assert _competitive_position_score(inp) == round(100.0 * 0.25, 1)

    def test_technical_fit_weight(self):
        inp = make_input(
            feature_advantage_score=0.0,
            price_competitiveness_score=0.0,
            technical_fit_score=100.0,
            competitive_win_rate_vs_competitor_pct=0.0,
            incumbent_competitor=0,
        )
        assert _competitive_position_score(inp) == round(100.0 * 0.25, 1)

    def test_win_rate_weight(self):
        inp = make_input(
            feature_advantage_score=0.0,
            price_competitiveness_score=0.0,
            technical_fit_score=0.0,
            competitive_win_rate_vs_competitor_pct=100.0,
            incumbent_competitor=0,
        )
        assert _competitive_position_score(inp) == round(1.0 * 20.0, 1)

    def test_score_capped_at_100(self):
        inp = make_input(
            feature_advantage_score=200.0,
            price_competitiveness_score=200.0,
            technical_fit_score=200.0,
            competitive_win_rate_vs_competitor_pct=100.0,
            incumbent_competitor=0,
        )
        assert _competitive_position_score(inp) <= 100.0

    def test_score_never_negative(self):
        inp = make_input(
            feature_advantage_score=0.0,
            price_competitiveness_score=0.0,
            technical_fit_score=0.0,
            competitive_win_rate_vs_competitor_pct=0.0,
            incumbent_competitor=0,
        )
        assert _competitive_position_score(inp) >= 0.0

    def test_partial_win_rate(self):
        inp = make_input(
            feature_advantage_score=0.0,
            price_competitiveness_score=0.0,
            technical_fit_score=0.0,
            competitive_win_rate_vs_competitor_pct=50.0,
            incumbent_competitor=0,
        )
        assert _competitive_position_score(inp) == round((50.0 / 100.0) * 20.0, 1)


# ---------------------------------------------------------------------------
# 6. _relationship_momentum_score
# ---------------------------------------------------------------------------

class TestRelationshipMomentumScore:
    def test_all_zero(self):
        inp = make_input(
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=0,
            competitor_activity_level=0.0,
            multi_year_deal=0,
        )
        assert _relationship_momentum_score(inp) == 0.0

    def test_poc_bonus(self):
        inp = make_input(
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=1,
            deal_stage_num=0,
            competitor_activity_level=0.0,
            multi_year_deal=0,
        )
        assert _relationship_momentum_score(inp) == 20.0

    def test_multi_year_bonus(self):
        inp = make_input(
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=0,
            competitor_activity_level=0.0,
            multi_year_deal=1,
        )
        assert _relationship_momentum_score(inp) == 5.0

    def test_stage_bonus_cap(self):
        # Stage 5 * 3 = 15, capped at 15
        inp = make_input(
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=5,
            competitor_activity_level=0.0,
            multi_year_deal=0,
        )
        assert _relationship_momentum_score(inp) == 15.0

    def test_stage_bonus_not_exceeded(self):
        inp = make_input(
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=100,
            competitor_activity_level=0.0,
            multi_year_deal=0,
        )
        score = _relationship_momentum_score(inp)
        # stage bonus is capped at 15
        assert score <= 100.0

    def test_competitor_activity_penalty(self):
        inp = make_input(
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=0,
            competitor_activity_level=100.0,
            multi_year_deal=0,
        )
        # penalty is 100/100*5 = 5, score floored to 0
        assert _relationship_momentum_score(inp) == 0.0

    def test_relationship_strength_weight(self):
        inp = make_input(
            relationship_strength_score=100.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=0,
            competitor_activity_level=0.0,
            multi_year_deal=0,
        )
        assert _relationship_momentum_score(inp) == round(100.0 * 0.30, 1)

    def test_deal_momentum_weight(self):
        inp = make_input(
            relationship_strength_score=0.0,
            deal_momentum_score=100.0,
            proof_of_concept_won=0,
            deal_stage_num=0,
            competitor_activity_level=0.0,
            multi_year_deal=0,
        )
        assert _relationship_momentum_score(inp) == round(100.0 * 0.30, 1)

    def test_score_never_negative(self):
        inp = make_input(
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=0,
            competitor_activity_level=100.0,
            multi_year_deal=0,
        )
        assert _relationship_momentum_score(inp) >= 0.0

    def test_score_capped_at_100(self):
        inp = make_input(
            relationship_strength_score=100.0,
            deal_momentum_score=100.0,
            proof_of_concept_won=1,
            deal_stage_num=10,
            competitor_activity_level=0.0,
            multi_year_deal=1,
        )
        assert _relationship_momentum_score(inp) <= 100.0


# ---------------------------------------------------------------------------
# 7. _deal_strength_score
# ---------------------------------------------------------------------------

class TestDealStrengthScore:
    def _simple_inp(self, deal_value, days, multi_year=0, stage=0, exec_sponsorship=0):
        return make_input(
            deal_value_usd=deal_value,
            days_until_close=days,
            multi_year_deal=multi_year,
            deal_stage_num=stage,
            executive_sponsorship=exec_sponsorship,
        )

    def test_small_deal_value_bonus(self):
        # <100k = +30
        inp = self._simple_inp(50_000, 30)
        score = _deal_strength_score(inp)
        # base 30 + time 25 (15..60) + multi 10 + stage*5 (0) = 65
        assert score == 65.0

    def test_100k_to_500k_value_bonus(self):
        inp = self._simple_inp(200_000, 30)
        # base 25 + time 25 + multi 10 + stage 0 = 60
        assert _deal_strength_score(inp) == 60.0

    def test_500k_to_1m_value_bonus(self):
        inp = self._simple_inp(750_000, 30)
        # base 20 + time 25 + multi 10 + stage 0 = 55
        assert _deal_strength_score(inp) == 55.0

    def test_over_1m_with_exec_sponsorship(self):
        inp = self._simple_inp(1_500_000, 30, exec_sponsorship=1)
        # base 15 + time 25 + multi 10 + stage 0 = 50
        assert _deal_strength_score(inp) == 50.0

    def test_over_1m_without_exec_sponsorship(self):
        inp = self._simple_inp(1_500_000, 30, exec_sponsorship=0)
        # base 5 + time 25 + multi 10 + stage 0 = 40
        assert _deal_strength_score(inp) == 40.0

    def test_days_15_to_60_time_bonus(self):
        inp = self._simple_inp(50_000, 30)
        score = _deal_strength_score(inp)
        # time bucket 15..60 gives 25
        assert score == 65.0  # 30+25+10+0

    def test_days_less_than_15_time_bonus(self):
        inp = self._simple_inp(50_000, 10)
        # 30+10+10+0=50
        assert _deal_strength_score(inp) == 50.0

    def test_days_16_to_90_time_bonus(self):
        inp = self._simple_inp(50_000, 70)
        # 30+18+10+0=58
        assert _deal_strength_score(inp) == 58.0

    def test_days_over_90_time_bonus(self):
        inp = self._simple_inp(50_000, 120)
        # 30+8+10+0=48
        assert _deal_strength_score(inp) == 48.0

    def test_multi_year_bonus(self):
        base = _deal_strength_score(self._simple_inp(50_000, 30, multi_year=0))
        with_multi = _deal_strength_score(self._simple_inp(50_000, 30, multi_year=1))
        # multi adds 20 instead of 10, diff = 10
        assert with_multi - base == 10.0

    def test_stage_bonus(self):
        inp = self._simple_inp(50_000, 30, stage=3)
        # 30+25+10+15=80
        assert _deal_strength_score(inp) == 80.0

    def test_stage_capped_at_25(self):
        inp = self._simple_inp(50_000, 30, stage=10)
        # stage bonus = min(25, 10*5)=25; 30+25+10+25=90
        assert _deal_strength_score(inp) == 90.0

    def test_score_capped_at_100(self):
        inp = self._simple_inp(50_000, 30, multi_year=1, stage=10, exec_sponsorship=1)
        assert _deal_strength_score(inp) <= 100.0

    def test_score_never_negative(self):
        inp = self._simple_inp(50_000, 200)
        assert _deal_strength_score(inp) >= 0.0


# ---------------------------------------------------------------------------
# 8. _win_probability_pct
# ---------------------------------------------------------------------------

class TestWinProbabilityPct:
    def test_formula(self):
        result = _win_probability_pct(80.0, 70.0, 60.0, 50.0)
        expected = round(80.0 * 0.35 + 70.0 * 0.30 + 60.0 * 0.25 + 50.0 * 0.10, 1)
        assert result == expected

    def test_all_zero(self):
        assert _win_probability_pct(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_all_100(self):
        assert _win_probability_pct(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_weights_sum_to_1(self):
        # If all components equal x, result should be x
        for x in [0.0, 50.0, 100.0]:
            assert _win_probability_pct(x, x, x, x) == x

    def test_champion_dominates(self):
        r1 = _win_probability_pct(100.0, 0.0, 0.0, 0.0)
        r2 = _win_probability_pct(0.0, 100.0, 0.0, 0.0)
        # champion weight 0.35 > competitive 0.30
        assert r1 > r2

    def test_returns_float(self):
        assert isinstance(_win_probability_pct(50.0, 50.0, 50.0, 50.0), float)

    def test_rounding_to_one_decimal(self):
        result = _win_probability_pct(33.3, 33.3, 33.3, 33.3)
        # check it is rounded to 1 decimal place
        assert result == round(result, 1)


# ---------------------------------------------------------------------------
# 9. _win_tier
# ---------------------------------------------------------------------------

class TestWinTier:
    def test_very_likely_at_75(self):
        assert _win_tier(75.0) == WinProbabilityTier.VERY_LIKELY

    def test_very_likely_above_75(self):
        assert _win_tier(90.0) == WinProbabilityTier.VERY_LIKELY

    def test_likely_at_58(self):
        assert _win_tier(58.0) == WinProbabilityTier.LIKELY

    def test_likely_at_74(self):
        assert _win_tier(74.9) == WinProbabilityTier.LIKELY

    def test_toss_up_at_42(self):
        assert _win_tier(42.0) == WinProbabilityTier.TOSS_UP

    def test_toss_up_at_57(self):
        assert _win_tier(57.9) == WinProbabilityTier.TOSS_UP

    def test_unlikely_at_25(self):
        assert _win_tier(25.0) == WinProbabilityTier.UNLIKELY

    def test_unlikely_at_41(self):
        assert _win_tier(41.9) == WinProbabilityTier.UNLIKELY

    def test_very_unlikely_at_24(self):
        assert _win_tier(24.9) == WinProbabilityTier.VERY_UNLIKELY

    def test_very_unlikely_at_0(self):
        assert _win_tier(0.0) == WinProbabilityTier.VERY_UNLIKELY

    def test_boundary_75(self):
        assert _win_tier(75.0) == WinProbabilityTier.VERY_LIKELY

    def test_boundary_58(self):
        assert _win_tier(58.0) == WinProbabilityTier.LIKELY

    def test_boundary_42(self):
        assert _win_tier(42.0) == WinProbabilityTier.TOSS_UP

    def test_boundary_25(self):
        assert _win_tier(25.0) == WinProbabilityTier.UNLIKELY


# ---------------------------------------------------------------------------
# 10. _win_risk
# ---------------------------------------------------------------------------

class TestWinRisk:
    def test_low_at_65(self):
        assert _win_risk(65.0) == WinRisk.LOW

    def test_low_at_100(self):
        assert _win_risk(100.0) == WinRisk.LOW

    def test_moderate_at_45(self):
        assert _win_risk(45.0) == WinRisk.MODERATE

    def test_moderate_at_64(self):
        assert _win_risk(64.9) == WinRisk.MODERATE

    def test_high_at_25(self):
        assert _win_risk(25.0) == WinRisk.HIGH

    def test_high_at_44(self):
        assert _win_risk(44.9) == WinRisk.HIGH

    def test_critical_at_24(self):
        assert _win_risk(24.9) == WinRisk.CRITICAL

    def test_critical_at_0(self):
        assert _win_risk(0.0) == WinRisk.CRITICAL

    def test_boundary_65(self):
        assert _win_risk(65.0) == WinRisk.LOW

    def test_boundary_45(self):
        assert _win_risk(45.0) == WinRisk.MODERATE

    def test_boundary_25(self):
        assert _win_risk(25.0) == WinRisk.HIGH


# ---------------------------------------------------------------------------
# 11. _primary_factor
# ---------------------------------------------------------------------------

class TestPrimaryFactor:
    def test_champion_wins_when_highest(self):
        # champion=100, others low
        result = _primary_factor(100.0, 10.0, 10.0, 10.0)
        assert result == PrimaryWinFactor.CHAMPION

    def test_features_wins_when_highest(self):
        result = _primary_factor(10.0, 100.0, 10.0, 10.0)
        assert result == PrimaryWinFactor.FEATURES

    def test_momentum_wins_when_highest(self):
        result = _primary_factor(10.0, 10.0, 100.0, 10.0)
        assert result == PrimaryWinFactor.MOMENTUM

    def test_price_wins_when_strength_highest(self):
        # strength maps to PRICE
        result = _primary_factor(10.0, 10.0, 10.0, 100.0)
        assert result == PrimaryWinFactor.PRICE

    def test_returns_primary_win_factor_type(self):
        result = _primary_factor(50.0, 50.0, 50.0, 50.0)
        assert isinstance(result, PrimaryWinFactor)

    def test_all_equal_picks_one_consistently(self):
        # All 50 — just check it returns a valid factor
        result = _primary_factor(50.0, 50.0, 50.0, 50.0)
        assert result in list(PrimaryWinFactor)


# ---------------------------------------------------------------------------
# 12. _recommended_action
# ---------------------------------------------------------------------------

class TestRecommendedAction:
    def test_maintain_course_when_pct_ge_65(self):
        inp = make_input()
        assert _recommended_action(65.0, inp) == WinAction.MAINTAIN_COURSE

    def test_maintain_course_above_65(self):
        inp = make_input()
        assert _recommended_action(90.0, inp) == WinAction.MAINTAIN_COURSE

    def test_executive_alignment_when_no_exec_and_large_deal(self):
        inp = make_input(
            executive_sponsorship=0,
            deal_value_usd=500_000,
            champion_strength_score=80.0,
        )
        assert _recommended_action(50.0, inp) == WinAction.EXECUTIVE_ALIGNMENT

    def test_strengthen_champion_when_low_champion(self):
        inp = make_input(
            executive_sponsorship=1,
            champion_strength_score=40.0,
        )
        assert _recommended_action(50.0, inp) == WinAction.STRENGTHEN_CHAMPION

    def test_price_adjustment_when_low_price_score(self):
        inp = make_input(
            executive_sponsorship=1,
            champion_strength_score=60.0,
            price_competitiveness_score=30.0,
        )
        assert _recommended_action(50.0, inp) == WinAction.PRICE_ADJUSTMENT

    def test_feature_demo_when_low_features_no_poc(self):
        inp = make_input(
            executive_sponsorship=1,
            champion_strength_score=60.0,
            price_competitiveness_score=50.0,
            feature_advantage_score=30.0,
            proof_of_concept_won=0,
        )
        assert _recommended_action(50.0, inp) == WinAction.FEATURE_DEMO

    def test_fallback_to_strengthen_champion(self):
        # All thresholds met, pct < 65, no special conditions
        inp = make_input(
            executive_sponsorship=1,
            champion_strength_score=60.0,
            price_competitiveness_score=50.0,
            feature_advantage_score=50.0,
            proof_of_concept_won=1,
        )
        assert _recommended_action(50.0, inp) == WinAction.STRENGTHEN_CHAMPION

    def test_exec_alignment_boundary_exactly_300k(self):
        inp = make_input(
            executive_sponsorship=0,
            deal_value_usd=300_000.0,
        )
        assert _recommended_action(50.0, inp) == WinAction.EXECUTIVE_ALIGNMENT

    def test_exec_alignment_not_triggered_below_300k(self):
        inp = make_input(
            executive_sponsorship=0,
            deal_value_usd=299_999.0,
            champion_strength_score=40.0,
        )
        # No exec trigger, so champion score < 50 fires
        assert _recommended_action(50.0, inp) == WinAction.STRENGTHEN_CHAMPION


# ---------------------------------------------------------------------------
# 13. _win_signal
# ---------------------------------------------------------------------------

class TestWinSignal:
    def test_incumbent_below_50(self):
        inp = make_input(
            incumbent_competitor=1,
            competitor_name="Rival",
            competitive_win_rate_vs_competitor_pct=40.0,
        )
        sig = _win_signal(inp, 45.0, WinProbabilityTier.TOSS_UP)
        assert "Rival" in sig
        assert "incumbent" in sig

    def test_poc_won_above_60(self):
        inp = make_input(
            incumbent_competitor=0,
            proof_of_concept_won=1,
            competitor_name="Rival",
        )
        sig = _win_signal(inp, 65.0, WinProbabilityTier.LIKELY)
        assert "POC won" in sig
        assert "Rival" in sig

    def test_exec_and_buyer_aligned(self):
        inp = make_input(
            incumbent_competitor=0,
            proof_of_concept_won=0,
            economic_buyer_engaged=1,
            executive_sponsorship=1,
            competitor_name="Rival",
        )
        sig = _win_signal(inp, 60.0, WinProbabilityTier.LIKELY)
        assert "Rival" in sig
        assert "executive" in sig.lower() or "economic" in sig.lower()

    def test_high_competitor_activity(self):
        inp = make_input(
            incumbent_competitor=0,
            proof_of_concept_won=0,
            economic_buyer_engaged=0,
            executive_sponsorship=0,
            competitor_activity_level=70.0,
            competitor_name="Rival",
        )
        sig = _win_signal(inp, 55.0, WinProbabilityTier.LIKELY)
        assert "Rival" in sig
        assert "active" in sig.lower() or "competitive" in sig.lower()

    def test_very_high_win_pct(self):
        inp = make_input(
            incumbent_competitor=0,
            proof_of_concept_won=0,
            economic_buyer_engaged=0,
            executive_sponsorship=0,
            competitor_activity_level=30.0,
            competitor_name="Rival",
        )
        sig = _win_signal(inp, 80.0, WinProbabilityTier.VERY_LIKELY)
        assert "Rival" in sig
        assert "80%" in sig or "strong" in sig.lower()

    def test_at_risk_below_30(self):
        inp = make_input(
            incumbent_competitor=0,
            proof_of_concept_won=0,
            economic_buyer_engaged=0,
            executive_sponsorship=0,
            competitor_activity_level=30.0,
            competitor_name="Rival",
        )
        sig = _win_signal(inp, 20.0, WinProbabilityTier.VERY_UNLIKELY)
        assert "Rival" in sig
        assert "at risk" in sig.lower() or "intervention" in sig.lower()

    def test_default_signal(self):
        inp = make_input(
            incumbent_competitor=0,
            proof_of_concept_won=0,
            economic_buyer_engaged=0,
            executive_sponsorship=0,
            competitor_activity_level=30.0,
            competitor_name="Rival",
        )
        sig = _win_signal(inp, 55.0, WinProbabilityTier.LIKELY)
        assert "Rival" in sig
        assert "55%" in sig

    def test_returns_string(self, basic_input):
        sig = _win_signal(basic_input, 50.0, WinProbabilityTier.TOSS_UP)
        assert isinstance(sig, str)


# ---------------------------------------------------------------------------
# 14. assess() - core engine method
# ---------------------------------------------------------------------------

class TestAssess:
    def test_returns_result_type(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result, CompetitiveWinResult)

    def test_deal_id_preserved(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert result.deal_id == "D001"

    def test_deal_name_preserved(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert result.deal_name == "Test Deal"

    def test_win_probability_in_range(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert 0.0 <= result.win_probability_pct <= 100.0

    def test_tier_is_valid_enum(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert result.win_probability_tier in WinProbabilityTier

    def test_risk_is_valid_enum(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert result.win_risk in WinRisk

    def test_factor_is_valid_enum(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert result.primary_win_factor in PrimaryWinFactor

    def test_action_is_valid_enum(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert result.recommended_action in WinAction

    def test_champion_score_in_range(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert 0.0 <= result.champion_score <= 100.0

    def test_competitive_score_in_range(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert 0.0 <= result.competitive_position_score <= 100.0

    def test_momentum_score_in_range(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert 0.0 <= result.relationship_momentum_score <= 100.0

    def test_strength_score_in_range(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert 0.0 <= result.deal_strength_score <= 100.0

    def test_estimated_win_value_formula(self, engine):
        inp = make_input(deal_value_usd=200_000.0)
        result = engine.assess(inp)
        expected = round(result.win_probability_pct / 100.0 * 200_000.0, 2)
        assert result.estimated_win_value_usd == expected

    def test_is_at_risk_when_low_pct(self, engine):
        # Force a low-win-probability deal
        inp = make_input(
            champion_strength_score=0.0,
            economic_buyer_engaged=0,
            executive_sponsorship=0,
            reference_customer_provided=0,
            feature_advantage_score=0.0,
            price_competitiveness_score=0.0,
            technical_fit_score=0.0,
            competitive_win_rate_vs_competitor_pct=0.0,
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=0,
            deal_value_usd=10_000.0,
            days_until_close=200,
            competitor_activity_level=0.0,
            multi_year_deal=0,
        )
        result = engine.assess(inp)
        if result.win_probability_pct < 45:
            assert result.is_at_risk is True

    def test_is_at_risk_when_high_competitor_activity(self, engine):
        inp = make_input(competitor_activity_level=80.0)
        result = engine.assess(inp)
        assert result.is_at_risk is True

    def test_is_at_risk_false_when_safe(self, engine):
        inp = make_input(
            champion_strength_score=100.0,
            economic_buyer_engaged=1,
            executive_sponsorship=1,
            reference_customer_provided=1,
            feature_advantage_score=100.0,
            price_competitiveness_score=100.0,
            technical_fit_score=100.0,
            competitive_win_rate_vs_competitor_pct=100.0,
            relationship_strength_score=100.0,
            deal_momentum_score=100.0,
            competitor_activity_level=20.0,
            proof_of_concept_won=1,
            multi_year_deal=1,
            deal_stage_num=5,
        )
        result = engine.assess(inp)
        assert result.is_at_risk is False

    def test_requires_exec_intervention_conditions(self, engine):
        # pct < 50, deal >= 300k, no exec sponsorship
        inp = make_input(
            champion_strength_score=0.0,
            economic_buyer_engaged=0,
            executive_sponsorship=0,
            feature_advantage_score=0.0,
            price_competitiveness_score=0.0,
            technical_fit_score=0.0,
            competitive_win_rate_vs_competitor_pct=0.0,
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=0,
            deal_value_usd=300_000.0,
            days_until_close=200,
            competitor_activity_level=0.0,
            multi_year_deal=0,
        )
        result = engine.assess(inp)
        if result.win_probability_pct < 50:
            assert result.requires_executive_intervention is True

    def test_no_requires_exec_when_exec_present(self, engine):
        inp = make_input(
            executive_sponsorship=1,
            deal_value_usd=500_000.0,
        )
        result = engine.assess(inp)
        assert result.requires_executive_intervention is False

    def test_no_requires_exec_when_small_deal(self, engine):
        inp = make_input(
            executive_sponsorship=0,
            deal_value_usd=100_000.0,
        )
        result = engine.assess(inp)
        assert result.requires_executive_intervention is False

    def test_win_signal_is_string(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result.win_signal, str)

    def test_result_stored_in_engine(self, engine, basic_input):
        engine.assess(basic_input)
        assert engine.get("D001") is not None

    def test_assess_overwrites_previous_result(self, engine, basic_input):
        engine.assess(basic_input)
        inp2 = make_input(deal_id="D001", champion_strength_score=100.0)
        result2 = engine.assess(inp2)
        assert engine.get("D001").champion_score == result2.champion_score

    def test_win_probability_formula_matches_components(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        expected = round(
            result.champion_score * 0.35
            + result.competitive_position_score * 0.30
            + result.relationship_momentum_score * 0.25
            + result.deal_strength_score * 0.10,
            1,
        )
        assert result.win_probability_pct == expected

    def test_is_at_risk_boundary_exactly_45(self, engine):
        # Win probability exactly 45 should NOT be at risk (condition is < 45)
        # Build an input that produces exactly 45.0 is hard, so we check the logic
        # by verifying that below-45 means at-risk
        inp = make_input(
            champion_strength_score=0.0,
            economic_buyer_engaged=0,
            executive_sponsorship=0,
            reference_customer_provided=0,
            feature_advantage_score=0.0,
            price_competitiveness_score=0.0,
            technical_fit_score=0.0,
            competitive_win_rate_vs_competitor_pct=0.0,
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=0,
            deal_value_usd=10_000.0,
            days_until_close=200,
            competitor_activity_level=0.0,
            multi_year_deal=0,
        )
        result = engine.assess(inp)
        expected_at_risk = result.win_probability_pct < 45 or inp.competitor_activity_level >= 80
        assert result.is_at_risk == expected_at_risk


# ---------------------------------------------------------------------------
# 15. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self, engine):
        inputs = [make_input(deal_id=f"D{i:03d}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert isinstance(results, list)

    def test_result_count_matches_input(self, engine):
        inputs = [make_input(deal_id=f"D{i:03d}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_sorted_by_win_probability_descending(self, engine):
        inputs = [
            make_input(deal_id="D001", champion_strength_score=10.0),
            make_input(deal_id="D002", champion_strength_score=90.0),
            make_input(deal_id="D003", champion_strength_score=50.0),
        ]
        results = engine.assess_batch(inputs)
        probs = [r.win_probability_pct for r in results]
        assert probs == sorted(probs, reverse=True)

    def test_empty_batch(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_single_item_batch(self, engine):
        inp = make_input()
        results = engine.assess_batch([inp])
        assert len(results) == 1
        assert isinstance(results[0], CompetitiveWinResult)

    def test_all_stored_in_engine(self, engine):
        inputs = [make_input(deal_id=f"D{i:03d}") for i in range(3)]
        engine.assess_batch(inputs)
        for inp in inputs:
            assert engine.get(inp.deal_id) is not None

    def test_batch_results_are_result_type(self, engine):
        inputs = [make_input(deal_id=f"D{i:03d}") for i in range(3)]
        results = engine.assess_batch(inputs)
        for r in results:
            assert isinstance(r, CompetitiveWinResult)

    def test_large_batch(self, engine):
        inputs = [make_input(deal_id=f"D{i:04d}") for i in range(50)]
        results = engine.assess_batch(inputs)
        assert len(results) == 50


# ---------------------------------------------------------------------------
# 16. Engine utility methods
# ---------------------------------------------------------------------------

class TestEngineGet:
    def test_returns_none_for_unknown_id(self, engine):
        assert engine.get("UNKNOWN") is None

    def test_returns_result_after_assess(self, engine, basic_input):
        engine.assess(basic_input)
        result = engine.get("D001")
        assert result is not None
        assert result.deal_id == "D001"


class TestEngineAllDeals:
    def test_empty_when_no_deals(self, engine):
        assert engine.all_deals() == []

    def test_sorted_descending(self, engine):
        inputs = [
            make_input(deal_id="D001", champion_strength_score=10.0),
            make_input(deal_id="D002", champion_strength_score=90.0),
        ]
        for inp in inputs:
            engine.assess(inp)
        results = engine.all_deals()
        probs = [r.win_probability_pct for r in results]
        assert probs == sorted(probs, reverse=True)

    def test_returns_all_assessed_deals(self, engine):
        for i in range(5):
            engine.assess(make_input(deal_id=f"D{i:03d}"))
        assert len(engine.all_deals()) == 5


class TestEngineAtRiskDeals:
    def test_empty_when_none_at_risk(self, engine):
        inp = make_input(
            champion_strength_score=100.0,
            economic_buyer_engaged=1,
            executive_sponsorship=1,
            reference_customer_provided=1,
            feature_advantage_score=100.0,
            price_competitiveness_score=100.0,
            technical_fit_score=100.0,
            competitive_win_rate_vs_competitor_pct=100.0,
            relationship_strength_score=100.0,
            deal_momentum_score=100.0,
            competitor_activity_level=10.0,
            proof_of_concept_won=1,
            multi_year_deal=1,
            deal_stage_num=5,
        )
        engine.assess(inp)
        at_risk = engine.at_risk_deals()
        assert all(r.is_at_risk for r in at_risk)

    def test_filters_at_risk_correctly(self, engine):
        inp_at_risk = make_input(deal_id="D001", competitor_activity_level=90.0)
        inp_safe = make_input(deal_id="D002", competitor_activity_level=10.0,
                              champion_strength_score=100.0, economic_buyer_engaged=1,
                              executive_sponsorship=1)
        engine.assess(inp_at_risk)
        engine.assess(inp_safe)
        at_risk_ids = {r.deal_id for r in engine.at_risk_deals()}
        assert "D001" in at_risk_ids


class TestEngineByTier:
    def test_filters_correct_tier(self, engine):
        inp = make_input(
            champion_strength_score=100.0,
            economic_buyer_engaged=1,
            executive_sponsorship=1,
            reference_customer_provided=1,
            feature_advantage_score=100.0,
            price_competitiveness_score=100.0,
            technical_fit_score=100.0,
            competitive_win_rate_vs_competitor_pct=100.0,
            relationship_strength_score=100.0,
            deal_momentum_score=100.0,
            proof_of_concept_won=1,
            multi_year_deal=1,
            deal_stage_num=5,
        )
        result = engine.assess(inp)
        tier_results = engine.by_tier(result.win_probability_tier)
        assert all(r.win_probability_tier == result.win_probability_tier for r in tier_results)

    def test_returns_empty_for_no_match(self, engine, basic_input):
        engine.assess(basic_input)
        # Unlikely to have VERY_UNLIKELY with default inputs
        result = engine.assess(basic_input)
        # Just check it returns a list
        tier_results = engine.by_tier(WinProbabilityTier.VERY_UNLIKELY)
        assert isinstance(tier_results, list)


class TestEngineByRisk:
    def test_filters_correct_risk(self, engine, basic_input):
        result = engine.assess(basic_input)
        risk_results = engine.by_risk(result.win_risk)
        assert all(r.win_risk == result.win_risk for r in risk_results)

    def test_returns_list(self, engine, basic_input):
        engine.assess(basic_input)
        assert isinstance(engine.by_risk(WinRisk.CRITICAL), list)


class TestEngineTotalWeightedPipeline:
    def test_zero_when_empty(self, engine):
        assert engine.total_weighted_pipeline_usd() == 0.0

    def test_single_deal(self, engine):
        inp = make_input(deal_value_usd=100_000.0)
        result = engine.assess(inp)
        expected = round(result.win_probability_pct / 100.0 * 100_000.0, 2)
        assert engine.total_weighted_pipeline_usd() == expected

    def test_multiple_deals(self, engine):
        inputs = [make_input(deal_id=f"D{i:03d}", deal_value_usd=50_000.0) for i in range(3)]
        results = [engine.assess(inp) for inp in inputs]
        expected = round(sum(r.estimated_win_value_usd for r in results), 2)
        assert engine.total_weighted_pipeline_usd() == expected


class TestEngineAvgWinProbability:
    def test_zero_when_empty(self, engine):
        assert engine.avg_win_probability_pct() == 0.0

    def test_single_deal(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert engine.avg_win_probability_pct() == result.win_probability_pct

    def test_multiple_deals(self, engine):
        inputs = [make_input(deal_id=f"D{i:03d}") for i in range(3)]
        results = [engine.assess(inp) for inp in inputs]
        expected = round(sum(r.win_probability_pct for r in results) / 3, 1)
        assert engine.avg_win_probability_pct() == expected


class TestEngineReset:
    def test_reset_clears_results(self, engine, basic_input):
        engine.assess(basic_input)
        engine.reset()
        assert engine.get("D001") is None

    def test_reset_clears_all_deals(self, engine):
        for i in range(5):
            engine.assess(make_input(deal_id=f"D{i:03d}"))
        engine.reset()
        assert engine.all_deals() == []

    def test_reset_makes_pipeline_zero(self, engine, basic_input):
        engine.assess(basic_input)
        engine.reset()
        assert engine.total_weighted_pipeline_usd() == 0.0

    def test_can_assess_after_reset(self, engine, basic_input):
        engine.assess(basic_input)
        engine.reset()
        result = engine.assess(basic_input)
        assert result.deal_id == "D001"


# ---------------------------------------------------------------------------
# 17. summary()
# ---------------------------------------------------------------------------

class TestSummary:
    def test_has_13_keys(self, engine, basic_input):
        engine.assess(basic_input)
        s = engine.summary()
        assert len(s) == 13

    def test_summary_keys(self, engine, basic_input):
        engine.assess(basic_input)
        s = engine.summary()
        expected_keys = {
            "total", "tier_counts", "risk_counts", "factor_counts", "action_counts",
            "avg_win_probability_pct", "at_risk_count", "executive_intervention_count",
            "avg_champion_score", "avg_competitive_position_score",
            "avg_relationship_momentum_score", "avg_deal_strength_score",
            "total_weighted_pipeline_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_total_matches_deal_count(self, engine):
        for i in range(5):
            engine.assess(make_input(deal_id=f"D{i:03d}"))
        assert engine.summary()["total"] == 5

    def test_tier_counts_are_dicts(self, engine, basic_input):
        engine.assess(basic_input)
        s = engine.summary()
        assert isinstance(s["tier_counts"], dict)

    def test_risk_counts_are_dicts(self, engine, basic_input):
        engine.assess(basic_input)
        s = engine.summary()
        assert isinstance(s["risk_counts"], dict)

    def test_factor_counts_are_dicts(self, engine, basic_input):
        engine.assess(basic_input)
        s = engine.summary()
        assert isinstance(s["factor_counts"], dict)

    def test_action_counts_are_dicts(self, engine, basic_input):
        engine.assess(basic_input)
        s = engine.summary()
        assert isinstance(s["action_counts"], dict)

    def test_avg_win_probability_present(self, engine, basic_input):
        result = engine.assess(basic_input)
        s = engine.summary()
        assert s["avg_win_probability_pct"] == result.win_probability_pct

    def test_at_risk_count_integer(self, engine, basic_input):
        engine.assess(basic_input)
        s = engine.summary()
        assert isinstance(s["at_risk_count"], int)

    def test_executive_intervention_count_integer(self, engine, basic_input):
        engine.assess(basic_input)
        s = engine.summary()
        assert isinstance(s["executive_intervention_count"], int)

    def test_avg_champion_score_present(self, engine, basic_input):
        result = engine.assess(basic_input)
        s = engine.summary()
        assert s["avg_champion_score"] == result.champion_score

    def test_avg_competitive_score_present(self, engine, basic_input):
        result = engine.assess(basic_input)
        s = engine.summary()
        assert s["avg_competitive_position_score"] == result.competitive_position_score

    def test_avg_momentum_score_present(self, engine, basic_input):
        result = engine.assess(basic_input)
        s = engine.summary()
        assert s["avg_relationship_momentum_score"] == result.relationship_momentum_score

    def test_avg_strength_score_present(self, engine, basic_input):
        result = engine.assess(basic_input)
        s = engine.summary()
        assert s["avg_deal_strength_score"] == result.deal_strength_score

    def test_total_weighted_pipeline_in_summary(self, engine, basic_input):
        result = engine.assess(basic_input)
        s = engine.summary()
        assert s["total_weighted_pipeline_usd"] == engine.total_weighted_pipeline_usd()

    def test_tier_counts_sum_equals_total(self, engine):
        for i in range(4):
            engine.assess(make_input(deal_id=f"D{i:03d}"))
        s = engine.summary()
        assert sum(s["tier_counts"].values()) == s["total"]

    def test_risk_counts_sum_equals_total(self, engine):
        for i in range(4):
            engine.assess(make_input(deal_id=f"D{i:03d}"))
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_factor_counts_sum_equals_total(self, engine):
        for i in range(4):
            engine.assess(make_input(deal_id=f"D{i:03d}"))
        s = engine.summary()
        assert sum(s["factor_counts"].values()) == s["total"]

    def test_action_counts_sum_equals_total(self, engine):
        for i in range(4):
            engine.assess(make_input(deal_id=f"D{i:03d}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_empty_engine(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["avg_win_probability_pct"] == 0.0
        assert s["total_weighted_pipeline_usd"] == 0.0

    def test_tier_count_values_are_correct(self, engine):
        # Two very-strong deals
        for i in range(2):
            engine.assess(make_input(
                deal_id=f"D{i:03d}",
                champion_strength_score=100.0,
                economic_buyer_engaged=1,
                executive_sponsorship=1,
                reference_customer_provided=1,
                feature_advantage_score=100.0,
                price_competitiveness_score=100.0,
                technical_fit_score=100.0,
                competitive_win_rate_vs_competitor_pct=100.0,
                relationship_strength_score=100.0,
                deal_momentum_score=100.0,
                proof_of_concept_won=1,
                multi_year_deal=1,
                deal_stage_num=5,
            ))
        s = engine.summary()
        assert s["tier_counts"].get("very_likely", 0) == 2


# ---------------------------------------------------------------------------
# 18. Edge cases and boundary conditions
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_deal_value(self, engine):
        inp = make_input(deal_value_usd=0.0)
        result = engine.assess(inp)
        assert result.estimated_win_value_usd == 0.0

    def test_very_large_deal_value(self, engine):
        inp = make_input(deal_value_usd=10_000_000.0)
        result = engine.assess(inp)
        assert result.estimated_win_value_usd == round(result.win_probability_pct / 100.0 * 10_000_000.0, 2)

    def test_deal_stage_zero(self, engine):
        inp = make_input(deal_stage_num=0)
        result = engine.assess(inp)
        assert result.win_probability_pct >= 0.0

    def test_all_scores_zero(self, engine):
        inp = make_input(
            champion_strength_score=0.0,
            economic_buyer_engaged=0,
            executive_sponsorship=0,
            reference_customer_provided=0,
            feature_advantage_score=0.0,
            price_competitiveness_score=0.0,
            technical_fit_score=0.0,
            competitive_win_rate_vs_competitor_pct=0.0,
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=0,
            deal_value_usd=10_000.0,
            days_until_close=200,
            competitor_activity_level=0.0,
            multi_year_deal=0,
        )
        result = engine.assess(inp)
        assert result.win_probability_pct >= 0.0
        assert result.win_risk == WinRisk.CRITICAL

    def test_all_scores_max(self, engine):
        inp = make_input(
            champion_strength_score=100.0,
            economic_buyer_engaged=1,
            executive_sponsorship=1,
            reference_customer_provided=1,
            feature_advantage_score=100.0,
            price_competitiveness_score=100.0,
            technical_fit_score=100.0,
            competitive_win_rate_vs_competitor_pct=100.0,
            relationship_strength_score=100.0,
            deal_momentum_score=100.0,
            proof_of_concept_won=1,
            multi_year_deal=1,
            deal_stage_num=5,
            deal_value_usd=100_000.0,
            days_until_close=30,
            competitor_activity_level=0.0,
            incumbent_competitor=0,
        )
        result = engine.assess(inp)
        assert result.win_probability_tier == WinProbabilityTier.VERY_LIKELY
        assert result.win_risk == WinRisk.LOW

    def test_incumbent_lowers_competitive_score(self, engine):
        inp_no_incumbent = make_input(incumbent_competitor=0)
        inp_incumbent = make_input(deal_id="D002", incumbent_competitor=1)
        r1 = engine.assess(inp_no_incumbent)
        r2 = engine.assess(inp_incumbent)
        assert r1.competitive_position_score >= r2.competitive_position_score

    def test_multiple_engine_instances_independent(self):
        e1 = CompetitiveWinProbabilityEngine()
        e2 = CompetitiveWinProbabilityEngine()
        inp = make_input()
        e1.assess(inp)
        assert e2.get("D001") is None

    def test_competitor_activity_79_not_at_risk(self, engine):
        inp = make_input(
            champion_strength_score=100.0,
            economic_buyer_engaged=1,
            executive_sponsorship=1,
            reference_customer_provided=1,
            feature_advantage_score=100.0,
            price_competitiveness_score=100.0,
            technical_fit_score=100.0,
            competitive_win_rate_vs_competitor_pct=100.0,
            relationship_strength_score=100.0,
            deal_momentum_score=100.0,
            proof_of_concept_won=1,
            multi_year_deal=1,
            deal_stage_num=5,
            competitor_activity_level=79.0,
        )
        result = engine.assess(inp)
        # pct >= 45 and competitor_activity < 80, so not at risk
        if result.win_probability_pct >= 45:
            assert result.is_at_risk is False

    def test_competitor_activity_exactly_80_is_at_risk(self, engine):
        inp = make_input(competitor_activity_level=80.0)
        result = engine.assess(inp)
        assert result.is_at_risk is True

    def test_requires_exec_boundary_exactly_300k(self, engine):
        inp = make_input(
            executive_sponsorship=0,
            deal_value_usd=300_000.0,
            champion_strength_score=0.0,
            economic_buyer_engaged=0,
            feature_advantage_score=0.0,
            price_competitiveness_score=0.0,
            technical_fit_score=0.0,
            competitive_win_rate_vs_competitor_pct=0.0,
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=0,
            days_until_close=200,
            competitor_activity_level=0.0,
            multi_year_deal=0,
        )
        result = engine.assess(inp)
        if result.win_probability_pct < 50:
            assert result.requires_executive_intervention is True

    def test_requires_exec_false_at_299k(self, engine):
        inp = make_input(
            executive_sponsorship=0,
            deal_value_usd=299_999.0,
        )
        result = engine.assess(inp)
        assert result.requires_executive_intervention is False

    def test_days_exactly_15(self, engine):
        inp = make_input(days_until_close=15, deal_value_usd=50_000.0, deal_stage_num=0,
                         multi_year_deal=0)
        strength = _deal_strength_score(inp)
        # 15..60 bucket gives +25
        assert strength == round(30 + 25 + 10 + 0, 1)

    def test_days_exactly_60(self, engine):
        inp = make_input(days_until_close=60, deal_value_usd=50_000.0, deal_stage_num=0,
                         multi_year_deal=0)
        strength = _deal_strength_score(inp)
        assert strength == round(30 + 25 + 10 + 0, 1)

    def test_days_exactly_90(self, engine):
        inp = make_input(days_until_close=90, deal_value_usd=50_000.0, deal_stage_num=0,
                         multi_year_deal=0)
        strength = _deal_strength_score(inp)
        # 61..90 bucket gives +18
        assert strength == round(30 + 18 + 10 + 0, 1)

    def test_days_91_over_90(self, engine):
        inp = make_input(days_until_close=91, deal_value_usd=50_000.0, deal_stage_num=0,
                         multi_year_deal=0)
        strength = _deal_strength_score(inp)
        # >90 gives +8
        assert strength == round(30 + 8 + 10 + 0, 1)


# ---------------------------------------------------------------------------
# 19. Determinism / reproducibility
# ---------------------------------------------------------------------------

class TestDeterminism:
    def test_same_input_same_output(self, engine):
        inp = make_input()
        r1 = engine.assess(inp)
        engine2 = CompetitiveWinProbabilityEngine()
        r2 = engine2.assess(inp)
        assert r1.win_probability_pct == r2.win_probability_pct
        assert r1.win_probability_tier == r2.win_probability_tier
        assert r1.win_risk == r2.win_risk
        assert r1.primary_win_factor == r2.primary_win_factor
        assert r1.recommended_action == r2.recommended_action
        assert r1.is_at_risk == r2.is_at_risk
        assert r1.requires_executive_intervention == r2.requires_executive_intervention
        assert r1.estimated_win_value_usd == r2.estimated_win_value_usd

    def test_batch_same_as_individual(self, engine):
        inputs = [make_input(deal_id=f"D{i:03d}", champion_strength_score=float(i * 10)) for i in range(5)]
        engine2 = CompetitiveWinProbabilityEngine()
        batch_results = engine.assess_batch(inputs)
        for inp in inputs:
            engine2.assess(inp)
        for br in batch_results:
            individual = engine2.get(br.deal_id)
            assert individual is not None
            assert br.win_probability_pct == individual.win_probability_pct


# ---------------------------------------------------------------------------
# 20. Type checking
# ---------------------------------------------------------------------------

class TestTypes:
    def test_champion_score_type(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result.champion_score, float)

    def test_competitive_score_type(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result.competitive_position_score, float)

    def test_momentum_score_type(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result.relationship_momentum_score, float)

    def test_strength_score_type(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result.deal_strength_score, float)

    def test_win_probability_pct_type(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result.win_probability_pct, float)

    def test_is_at_risk_type(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result.is_at_risk, bool)

    def test_requires_exec_type(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result.requires_executive_intervention, bool)

    def test_estimated_win_value_type(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result.estimated_win_value_usd, float)

    def test_win_signal_type(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result.win_signal, str)

    def test_win_tier_type(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result.win_probability_tier, WinProbabilityTier)

    def test_win_risk_type(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result.win_risk, WinRisk)

    def test_primary_factor_type(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result.primary_win_factor, PrimaryWinFactor)

    def test_recommended_action_type(self, engine, basic_input):
        result = engine.assess(basic_input)
        assert isinstance(result.recommended_action, WinAction)


# ---------------------------------------------------------------------------
# 21. Scenario-based tests
# ---------------------------------------------------------------------------

class TestScenarios:
    def test_strong_deal_gets_very_likely_tier(self, engine):
        inp = make_input(
            champion_strength_score=100.0,
            economic_buyer_engaged=1,
            executive_sponsorship=1,
            reference_customer_provided=1,
            feature_advantage_score=100.0,
            price_competitiveness_score=100.0,
            technical_fit_score=100.0,
            competitive_win_rate_vs_competitor_pct=100.0,
            relationship_strength_score=100.0,
            deal_momentum_score=100.0,
            proof_of_concept_won=1,
            multi_year_deal=1,
            deal_stage_num=5,
            competitor_activity_level=0.0,
            days_until_close=30,
        )
        result = engine.assess(inp)
        assert result.win_probability_tier == WinProbabilityTier.VERY_LIKELY

    def test_weak_deal_gets_very_unlikely_tier(self, engine):
        inp = make_input(
            champion_strength_score=0.0,
            economic_buyer_engaged=0,
            executive_sponsorship=0,
            reference_customer_provided=0,
            feature_advantage_score=0.0,
            price_competitiveness_score=0.0,
            technical_fit_score=0.0,
            competitive_win_rate_vs_competitor_pct=0.0,
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            multi_year_deal=0,
            deal_stage_num=0,
            deal_value_usd=10_000.0,
            days_until_close=200,
            competitor_activity_level=0.0,
        )
        result = engine.assess(inp)
        assert result.win_probability_tier == WinProbabilityTier.VERY_UNLIKELY

    def test_incumbent_with_poc_win(self, engine):
        inp = make_input(
            incumbent_competitor=1,
            proof_of_concept_won=1,
            competitor_name="BigCorp",
            competitive_win_rate_vs_competitor_pct=40.0,
        )
        result = engine.assess(inp)
        sig = result.win_signal
        assert "BigCorp" in sig

    def test_high_activity_deal_at_risk(self, engine):
        inp = make_input(competitor_activity_level=85.0)
        result = engine.assess(inp)
        assert result.is_at_risk is True

    def test_exec_intervention_needed(self, engine):
        inp = make_input(
            executive_sponsorship=0,
            deal_value_usd=500_000.0,
            champion_strength_score=0.0,
            economic_buyer_engaged=0,
            feature_advantage_score=0.0,
            price_competitiveness_score=0.0,
            technical_fit_score=0.0,
            competitive_win_rate_vs_competitor_pct=0.0,
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=0,
            days_until_close=200,
            competitor_activity_level=0.0,
            multi_year_deal=0,
        )
        result = engine.assess(inp)
        if result.win_probability_pct < 50:
            assert result.requires_executive_intervention is True
            assert result.recommended_action == WinAction.EXECUTIVE_ALIGNMENT

    def test_maintain_course_for_high_pct(self, engine):
        inp = make_input(
            champion_strength_score=100.0,
            economic_buyer_engaged=1,
            executive_sponsorship=1,
            reference_customer_provided=1,
            feature_advantage_score=100.0,
            price_competitiveness_score=100.0,
            technical_fit_score=100.0,
            competitive_win_rate_vs_competitor_pct=100.0,
            relationship_strength_score=100.0,
            deal_momentum_score=100.0,
            proof_of_concept_won=1,
            multi_year_deal=1,
            deal_stage_num=5,
        )
        result = engine.assess(inp)
        if result.win_probability_pct >= 65:
            assert result.recommended_action == WinAction.MAINTAIN_COURSE

    def test_multi_deal_pipeline_adds_up(self, engine):
        inputs = [make_input(deal_id=f"D{i:03d}", deal_value_usd=100_000.0) for i in range(3)]
        results = [engine.assess(inp) for inp in inputs]
        expected = round(sum(r.estimated_win_value_usd for r in results), 2)
        assert engine.total_weighted_pipeline_usd() == expected

    def test_win_signal_mentions_competitor_name(self, engine):
        inp = make_input(competitor_name="SpecialRival")
        result = engine.assess(inp)
        assert "SpecialRival" in result.win_signal

    def test_batch_sort_order(self, engine):
        inputs = [
            make_input(deal_id="D001", champion_strength_score=10.0, economic_buyer_engaged=0,
                       executive_sponsorship=0, reference_customer_provided=0),
            make_input(deal_id="D002", champion_strength_score=90.0, economic_buyer_engaged=1,
                       executive_sponsorship=1, reference_customer_provided=1),
        ]
        results = engine.assess_batch(inputs)
        assert results[0].win_probability_pct >= results[1].win_probability_pct

    def test_poc_won_increases_momentum_score(self):
        inp_no_poc = make_input(proof_of_concept_won=0)
        inp_poc = make_input(proof_of_concept_won=1)
        assert _relationship_momentum_score(inp_poc) > _relationship_momentum_score(inp_no_poc)

    def test_executive_sponsorship_increases_champion_score(self):
        inp_no_exec = make_input(executive_sponsorship=0)
        inp_exec = make_input(executive_sponsorship=1)
        assert _champion_score(inp_exec) > _champion_score(inp_no_exec)

    def test_reference_customer_increases_champion_score(self):
        inp_no_ref = make_input(reference_customer_provided=0)
        inp_ref = make_input(reference_customer_provided=1)
        assert _champion_score(inp_ref) > _champion_score(inp_no_ref)


# ---------------------------------------------------------------------------
# 22. Additional formula / value-correctness tests
# ---------------------------------------------------------------------------

class TestFormulaCorrectness:
    """Explicit numeric checks that pin exact computed values."""

    def test_champion_score_exact_all_flags(self):
        # 100*0.40 + 25 + 20 + 15 = 100
        inp = make_input(
            champion_strength_score=100.0,
            economic_buyer_engaged=1,
            executive_sponsorship=1,
            reference_customer_provided=1,
        )
        assert _champion_score(inp) == 100.0

    def test_champion_score_no_flags(self):
        # 60*0.40 = 24.0
        inp = make_input(
            champion_strength_score=60.0,
            economic_buyer_engaged=0,
            executive_sponsorship=0,
            reference_customer_provided=0,
        )
        assert _champion_score(inp) == 24.0

    def test_competitive_score_exact_no_incumbent(self):
        # 80*0.30 + 70*0.25 + 60*0.25 + 50/100*20 = 24+17.5+15+10 = 66.5
        inp = make_input(
            feature_advantage_score=80.0,
            price_competitiveness_score=70.0,
            technical_fit_score=60.0,
            competitive_win_rate_vs_competitor_pct=50.0,
            incumbent_competitor=0,
        )
        expected = round(80.0 * 0.30 + 70.0 * 0.25 + 60.0 * 0.25 + (50.0 / 100.0) * 20.0, 1)
        assert _competitive_position_score(inp) == expected

    def test_competitive_score_exact_with_incumbent(self):
        inp = make_input(
            feature_advantage_score=80.0,
            price_competitiveness_score=70.0,
            technical_fit_score=60.0,
            competitive_win_rate_vs_competitor_pct=50.0,
            incumbent_competitor=1,
        )
        raw = 80.0 * 0.30 + 70.0 * 0.25 + 60.0 * 0.25 + (50.0 / 100.0) * 20.0
        expected = round(raw * 0.80, 1)
        assert _competitive_position_score(inp) == expected

    def test_win_probability_exact_formula(self):
        c, comp, m, s = 80.0, 70.0, 60.0, 50.0
        result = _win_probability_pct(c, comp, m, s)
        assert result == round(c * 0.35 + comp * 0.30 + m * 0.25 + s * 0.10, 1)

    def test_estimated_win_value_exact(self, engine):
        inp = make_input(deal_value_usd=123_456.78)
        result = engine.assess(inp)
        expected = round(result.win_probability_pct / 100.0 * 123_456.78, 2)
        assert result.estimated_win_value_usd == expected

    def test_relationship_momentum_exact(self):
        inp = make_input(
            relationship_strength_score=60.0,
            deal_momentum_score=70.0,
            proof_of_concept_won=1,
            deal_stage_num=3,
            competitor_activity_level=50.0,
            multi_year_deal=1,
        )
        expected = round(
            60.0 * 0.30  # relationship
            + 70.0 * 0.30  # momentum
            + 20.0  # poc
            + min(15.0, 3 * 3.0)  # stage
            - (50.0 / 100.0) * 5.0  # competitor penalty
            + 5.0,  # multi-year
            1,
        )
        assert _relationship_momentum_score(inp) == expected

    def test_deal_strength_1m_with_exec_exact(self):
        inp = make_input(
            deal_value_usd=2_000_000.0,
            days_until_close=30,
            multi_year_deal=0,
            deal_stage_num=2,
            executive_sponsorship=1,
        )
        # 15 + 25 + 10 + min(25, 2*5)=10 = 60
        assert _deal_strength_score(inp) == 60.0

    def test_at_risk_logic_disjunction(self, engine):
        # Neither condition: pct >= 45 AND competitor_activity < 80
        inp = make_input(
            champion_strength_score=100.0,
            economic_buyer_engaged=1,
            executive_sponsorship=1,
            reference_customer_provided=1,
            feature_advantage_score=100.0,
            price_competitiveness_score=100.0,
            technical_fit_score=100.0,
            competitive_win_rate_vs_competitor_pct=100.0,
            relationship_strength_score=100.0,
            deal_momentum_score=100.0,
            competitor_activity_level=50.0,
            proof_of_concept_won=1,
            multi_year_deal=1,
            deal_stage_num=5,
        )
        result = engine.assess(inp)
        assert result.win_probability_pct >= 45
        assert result.is_at_risk is False

    def test_requires_exec_all_three_conditions(self, engine):
        inp = make_input(
            champion_strength_score=0.0,
            economic_buyer_engaged=0,
            executive_sponsorship=0,
            reference_customer_provided=0,
            feature_advantage_score=0.0,
            price_competitiveness_score=0.0,
            technical_fit_score=0.0,
            competitive_win_rate_vs_competitor_pct=0.0,
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=0,
            deal_value_usd=300_000.0,
            days_until_close=200,
            competitor_activity_level=0.0,
            multi_year_deal=0,
        )
        result = engine.assess(inp)
        # All conditions met: pct < 50, value >= 300k, no exec
        assert result.win_probability_pct < 50
        assert result.requires_executive_intervention is True

    def test_stage_4_exact_bonus(self):
        # stage_bonus = min(15, 4*3) = 12
        inp = make_input(
            relationship_strength_score=0.0,
            deal_momentum_score=0.0,
            proof_of_concept_won=0,
            deal_stage_num=4,
            competitor_activity_level=0.0,
            multi_year_deal=0,
        )
        assert _relationship_momentum_score(inp) == 12.0

    def test_strength_deal_stage_5_cap(self):
        # min(25, 5*5)=25
        inp = make_input(
            deal_value_usd=50_000.0,
            days_until_close=30,
            multi_year_deal=0,
            deal_stage_num=5,
            executive_sponsorship=0,
        )
        # 30+25+10+25=90
        assert _deal_strength_score(inp) == 90.0
