"""
Comprehensive tests for swarm/intelligence/expansion_revenue.py
Run from /home/user/TEST:
    python -m pytest swarm/tests/test_expansion_revenue.py -v
"""

from __future__ import annotations

import pytest

from swarm.intelligence.expansion_revenue import (
    ExpansionTier,
    ExpansionAction,
    ExpansionInput,
    ExpansionResult,
    ExpansionRevenueDetector,
    _seat_utilization,
    _modules_utilization,
    _utilization_score,
    _relationship_score,
    _growth_score,
    _timing_score,
    _expansion_score,
    _expansion_tier,
    _expansion_action,
    _opportunity_types,
    _estimated_expansion_eur,
    _build_signals,
)


# ─── Fixtures / helpers ───────────────────────────────────────────────────────

def make_input(
    account_id: str = "acct_001",
    account_name: str = "Acme Corp",
    current_arr_eur: float = 100_000.0,
    product_tier: str = "professional",
    contract_months_remaining: int = 6,
    seats_licensed: int = 100,
    seats_used: int = 75,
    feature_adoption_pct: float = 65.0,
    modules_purchased: int = 3,
    modules_available: int = 8,
    nps_score: int = 30,
    executive_engagement: bool = True,
    champion_strength: int = 70,
    days_since_last_qbr: int = 45,
    expansion_signals: int = 2,
    competitive_pressure: bool = False,
    previous_expansion_done: bool = False,
    health_score: float = 75.0,
) -> ExpansionInput:
    return ExpansionInput(
        account_id=account_id,
        account_name=account_name,
        current_arr_eur=current_arr_eur,
        product_tier=product_tier,
        contract_months_remaining=contract_months_remaining,
        seats_licensed=seats_licensed,
        seats_used=seats_used,
        feature_adoption_pct=feature_adoption_pct,
        modules_purchased=modules_purchased,
        modules_available=modules_available,
        nps_score=nps_score,
        executive_engagement=executive_engagement,
        champion_strength=champion_strength,
        days_since_last_qbr=days_since_last_qbr,
        expansion_signals=expansion_signals,
        competitive_pressure=competitive_pressure,
        previous_expansion_done=previous_expansion_done,
        health_score=health_score,
    )


# ─── Class 1: ExpansionTier enum ──────────────────────────────────────────────

class TestExpansionTierEnum:
    def test_hot_value(self):
        assert ExpansionTier.HOT.value == "hot"

    def test_warm_value(self):
        assert ExpansionTier.WARM.value == "warm"

    def test_cool_value(self):
        assert ExpansionTier.COOL.value == "cool"

    def test_cold_value(self):
        assert ExpansionTier.COLD.value == "cold"

    def test_all_four_tiers_exist(self):
        assert len(ExpansionTier) == 4

    def test_tier_is_str(self):
        assert isinstance(ExpansionTier.HOT, str)


# ─── Class 2: ExpansionAction enum ───────────────────────────────────────────

class TestExpansionActionEnum:
    def test_close_value(self):
        assert ExpansionAction.CLOSE.value == "close"

    def test_nurture_value(self):
        assert ExpansionAction.NURTURE.value == "nurture"

    def test_qualify_value(self):
        assert ExpansionAction.QUALIFY.value == "qualify"

    def test_watch_value(self):
        assert ExpansionAction.WATCH.value == "watch"

    def test_all_four_actions_exist(self):
        assert len(ExpansionAction) == 4

    def test_action_is_str(self):
        assert isinstance(ExpansionAction.CLOSE, str)


# ─── Class 3: _seat_utilization ──────────────────────────────────────────────

class TestSeatUtilization:
    def test_basic_calculation(self):
        inp = make_input(seats_used=75, seats_licensed=100)
        assert _seat_utilization(inp) == 75.0

    def test_rounding_to_1dp(self):
        inp = make_input(seats_used=1, seats_licensed=3)
        # 1/3 * 100 = 33.333... → 33.3
        assert _seat_utilization(inp) == 33.3

    def test_full_utilization(self):
        inp = make_input(seats_used=100, seats_licensed=100)
        assert _seat_utilization(inp) == 100.0

    def test_over_utilization(self):
        inp = make_input(seats_used=110, seats_licensed=100)
        assert _seat_utilization(inp) == 110.0

    def test_zero_seats_licensed_uses_max_1(self):
        inp = make_input(seats_used=50, seats_licensed=0)
        # max(1, 0) = 1 → 50/1*100 = 5000.0
        assert _seat_utilization(inp) == 5000.0

    def test_zero_seats_used(self):
        inp = make_input(seats_used=0, seats_licensed=100)
        assert _seat_utilization(inp) == 0.0

    def test_high_utilization_rounded(self):
        inp = make_input(seats_used=91, seats_licensed=100)
        assert _seat_utilization(inp) == 91.0

    def test_float_rounding(self):
        inp = make_input(seats_used=2, seats_licensed=3)
        # 2/3 * 100 = 66.666... → 66.7
        assert _seat_utilization(inp) == 66.7


# ─── Class 4: _modules_utilization ───────────────────────────────────────────

class TestModulesUtilization:
    def test_basic_calculation(self):
        inp = make_input(modules_purchased=3, modules_available=8)
        assert _modules_utilization(inp) == 37.5

    def test_zero_modules_available_uses_max_1(self):
        inp = make_input(modules_purchased=5, modules_available=0)
        # max(1, 0) = 1 → 5/1*100 = 500.0
        assert _modules_utilization(inp) == 500.0

    def test_full_utilization(self):
        inp = make_input(modules_purchased=8, modules_available=8)
        assert _modules_utilization(inp) == 100.0

    def test_zero_modules_purchased(self):
        inp = make_input(modules_purchased=0, modules_available=8)
        assert _modules_utilization(inp) == 0.0

    def test_rounding_to_1dp(self):
        inp = make_input(modules_purchased=1, modules_available=3)
        # 1/3 * 100 = 33.333... → 33.3
        assert _modules_utilization(inp) == 33.3

    def test_partial_utilization(self):
        inp = make_input(modules_purchased=4, modules_available=10)
        assert _modules_utilization(inp) == 40.0


# ─── Class 5: _utilization_score seat thresholds ─────────────────────────────

class TestUtilizationScoreSeatThresholds:
    def test_seat_util_above_90_base_100(self):
        inp = make_input(feature_adoption_pct=0.0)
        score = _utilization_score(inp, 91.0)
        assert score == 100.0

    def test_seat_util_exactly_90_not_above_90(self):
        # 90 is NOT > 90, so falls to >80 branch → base 80
        inp = make_input(feature_adoption_pct=0.0)
        score = _utilization_score(inp, 90.0)
        assert score == 80.0

    def test_seat_util_above_80_base_80(self):
        inp = make_input(feature_adoption_pct=0.0)
        score = _utilization_score(inp, 85.0)
        assert score == 80.0

    def test_seat_util_exactly_80_not_above_80(self):
        # 80 is NOT > 80, so falls to >70 branch → base 60
        inp = make_input(feature_adoption_pct=0.0)
        score = _utilization_score(inp, 80.0)
        assert score == 60.0

    def test_seat_util_above_70_base_60(self):
        inp = make_input(feature_adoption_pct=0.0)
        score = _utilization_score(inp, 75.0)
        assert score == 60.0

    def test_seat_util_exactly_70_not_above_70(self):
        # 70 is NOT > 70, so falls to >50 branch → base 40
        inp = make_input(feature_adoption_pct=0.0)
        score = _utilization_score(inp, 70.0)
        assert score == 40.0

    def test_seat_util_above_50_base_40(self):
        inp = make_input(feature_adoption_pct=0.0)
        score = _utilization_score(inp, 60.0)
        assert score == 40.0

    def test_seat_util_exactly_50_not_above_50(self):
        # 50 is NOT > 50, so falls to else → base 20
        inp = make_input(feature_adoption_pct=0.0)
        score = _utilization_score(inp, 50.0)
        assert score == 20.0

    def test_seat_util_below_50_base_20(self):
        inp = make_input(feature_adoption_pct=0.0)
        score = _utilization_score(inp, 30.0)
        assert score == 20.0

    def test_seat_util_zero_base_20(self):
        inp = make_input(feature_adoption_pct=0.0)
        score = _utilization_score(inp, 0.0)
        assert score == 20.0


# ─── Class 6: _utilization_score feature adoption bonuses ────────────────────

class TestUtilizationScoreFeatureAdoption:
    def test_feature_adoption_above_80_adds_15(self):
        inp = make_input(feature_adoption_pct=85.0)
        score = _utilization_score(inp, 60.0)  # base 40
        assert score == 55.0  # 40 + 15

    def test_feature_adoption_exactly_80_not_above_80(self):
        # 80 is NOT > 80, so goes to >60 branch → +8
        inp = make_input(feature_adoption_pct=80.0)
        score = _utilization_score(inp, 60.0)  # base 40
        assert score == 48.0  # 40 + 8

    def test_feature_adoption_above_60_adds_8(self):
        inp = make_input(feature_adoption_pct=70.0)
        score = _utilization_score(inp, 60.0)  # base 40
        assert score == 48.0  # 40 + 8

    def test_feature_adoption_exactly_60_no_bonus(self):
        # 60 is NOT > 60, so no bonus
        inp = make_input(feature_adoption_pct=60.0)
        score = _utilization_score(inp, 60.0)  # base 40
        assert score == 40.0

    def test_feature_adoption_below_60_no_bonus(self):
        inp = make_input(feature_adoption_pct=40.0)
        score = _utilization_score(inp, 60.0)  # base 40
        assert score == 40.0

    def test_clamped_to_100_max(self):
        # seat>90 → base 100, feature>80 → +15 → 115 → clamped to 100
        inp = make_input(feature_adoption_pct=90.0)
        score = _utilization_score(inp, 95.0)
        assert score == 100.0

    def test_clamped_to_0_min(self):
        # base 20, no feature bonus → min is 0
        # This combination can't go below 0 with positive base
        inp = make_input(feature_adoption_pct=0.0)
        score = _utilization_score(inp, 0.0)
        assert score >= 0.0


# ─── Class 7: _relationship_score ────────────────────────────────────────────

class TestRelationshipScore:
    def test_executive_engagement_adds_30(self):
        inp = make_input(
            executive_engagement=True,
            champion_strength=0,
            nps_score=-999,
            days_since_last_qbr=91,  # neutral: no bonus/penalty
        )
        score = _relationship_score(inp)
        assert score == 30.0

    def test_no_executive_engagement_no_bonus(self):
        inp = make_input(
            executive_engagement=False,
            champion_strength=0,
            nps_score=-999,
            days_since_last_qbr=91,
        )
        score = _relationship_score(inp)
        assert score == 0.0

    def test_champion_above_80_adds_25(self):
        inp = make_input(
            executive_engagement=False,
            champion_strength=85,
            nps_score=-999,
            days_since_last_qbr=91,
        )
        assert _relationship_score(inp) == 25.0

    def test_champion_exactly_80_not_above_80(self):
        # 80 NOT > 80, falls to >60 → +15
        inp = make_input(
            executive_engagement=False,
            champion_strength=80,
            nps_score=-999,
            days_since_last_qbr=91,
        )
        assert _relationship_score(inp) == 15.0

    def test_champion_above_60_adds_15(self):
        inp = make_input(
            executive_engagement=False,
            champion_strength=70,
            nps_score=-999,
            days_since_last_qbr=91,
        )
        assert _relationship_score(inp) == 15.0

    def test_champion_exactly_60_not_above_60(self):
        # 60 NOT > 60, falls to >40 → +8
        inp = make_input(
            executive_engagement=False,
            champion_strength=60,
            nps_score=-999,
            days_since_last_qbr=91,
        )
        assert _relationship_score(inp) == 8.0

    def test_champion_above_40_adds_8(self):
        inp = make_input(
            executive_engagement=False,
            champion_strength=50,
            nps_score=-999,
            days_since_last_qbr=91,
        )
        assert _relationship_score(inp) == 8.0

    def test_champion_at_40_no_bonus(self):
        # 40 NOT > 40 → no bonus
        inp = make_input(
            executive_engagement=False,
            champion_strength=40,
            nps_score=-999,
            days_since_last_qbr=91,
        )
        assert _relationship_score(inp) == 0.0

    def test_nps_minus_999_skipped(self):
        inp = make_input(
            executive_engagement=False,
            champion_strength=0,
            nps_score=-999,
            days_since_last_qbr=91,
        )
        assert _relationship_score(inp) == 0.0

    def test_nps_above_50_adds_20(self):
        inp = make_input(
            executive_engagement=False,
            champion_strength=0,
            nps_score=60,
            days_since_last_qbr=91,
        )
        assert _relationship_score(inp) == 20.0

    def test_nps_exactly_50_not_above_50(self):
        # 50 NOT > 50, falls to >20 → +10
        inp = make_input(
            executive_engagement=False,
            champion_strength=0,
            nps_score=50,
            days_since_last_qbr=91,
        )
        assert _relationship_score(inp) == 10.0

    def test_nps_above_20_adds_10(self):
        inp = make_input(
            executive_engagement=False,
            champion_strength=0,
            nps_score=30,
            days_since_last_qbr=91,
        )
        assert _relationship_score(inp) == 10.0

    def test_nps_exactly_20_no_nps_bonus(self):
        # 20 NOT > 20, not < -20, not < 0 → no NPS bonus/penalty
        inp = make_input(
            executive_engagement=False,
            champion_strength=0,
            nps_score=20,
            days_since_last_qbr=91,
        )
        assert _relationship_score(inp) == 0.0

    def test_nps_below_minus_20_subtracts_30(self):
        inp = make_input(
            executive_engagement=True,
            champion_strength=0,
            nps_score=-30,
            days_since_last_qbr=91,
        )
        # 30 (exec) - 30 (nps) = 0 → clamped to 0
        assert _relationship_score(inp) == 0.0

    def test_nps_exactly_minus_20_not_below_minus_20(self):
        # -20 NOT < -20, but -20 < 0 → -15
        inp = make_input(
            executive_engagement=False,
            champion_strength=0,
            nps_score=-20,
            days_since_last_qbr=91,
        )
        # 0 - 15 = -15 → clamped to 0
        assert _relationship_score(inp) == 0.0

    def test_nps_below_0_subtracts_15(self):
        inp = make_input(
            executive_engagement=True,
            champion_strength=0,
            nps_score=-10,
            days_since_last_qbr=91,
        )
        # 30 (exec) - 15 (nps) = 15
        assert _relationship_score(inp) == 15.0

    def test_days_qbr_at_30_adds_15(self):
        inp = make_input(
            executive_engagement=False,
            champion_strength=0,
            nps_score=-999,
            days_since_last_qbr=30,
        )
        assert _relationship_score(inp) == 15.0

    def test_days_qbr_below_30_adds_15(self):
        inp = make_input(
            executive_engagement=False,
            champion_strength=0,
            nps_score=-999,
            days_since_last_qbr=10,
        )
        assert _relationship_score(inp) == 15.0

    def test_days_qbr_at_90_adds_5(self):
        inp = make_input(
            executive_engagement=False,
            champion_strength=0,
            nps_score=-999,
            days_since_last_qbr=90,
        )
        assert _relationship_score(inp) == 5.0

    def test_days_qbr_between_31_and_90_adds_5(self):
        inp = make_input(
            executive_engagement=False,
            champion_strength=0,
            nps_score=-999,
            days_since_last_qbr=60,
        )
        assert _relationship_score(inp) == 5.0

    def test_days_qbr_91_to_180_no_change(self):
        inp = make_input(
            executive_engagement=False,
            champion_strength=0,
            nps_score=-999,
            days_since_last_qbr=120,
        )
        assert _relationship_score(inp) == 0.0

    def test_days_qbr_above_180_subtracts_10(self):
        inp = make_input(
            executive_engagement=True,
            champion_strength=0,
            nps_score=-999,
            days_since_last_qbr=200,
        )
        # 30 - 10 = 20
        assert _relationship_score(inp) == 20.0

    def test_clamped_to_100_max(self):
        # All bonuses: exec(30) + champion>80(25) + nps>50(20) + qbr<=30(15) = 90
        inp = make_input(
            executive_engagement=True,
            champion_strength=90,
            nps_score=80,
            days_since_last_qbr=10,
        )
        score = _relationship_score(inp)
        assert score == 90.0

    def test_clamped_to_0_min(self):
        # nps < -20 → -30, days_qbr > 180 → -10, no other bonuses → -40 → clamped to 0
        inp = make_input(
            executive_engagement=False,
            champion_strength=0,
            nps_score=-50,
            days_since_last_qbr=200,
        )
        assert _relationship_score(inp) == 0.0


# ─── Class 8: _growth_score ──────────────────────────────────────────────────

class TestGrowthScore:
    def test_zero_expansion_signals(self):
        inp = make_input(expansion_signals=0, competitive_pressure=True, previous_expansion_done=False)
        assert _growth_score(inp) == 0.0

    def test_one_expansion_signal_adds_25(self):
        inp = make_input(expansion_signals=1, competitive_pressure=True, previous_expansion_done=False)
        assert _growth_score(inp) == 25.0

    def test_two_expansion_signals_adds_50(self):
        inp = make_input(expansion_signals=2, competitive_pressure=True, previous_expansion_done=False)
        assert _growth_score(inp) == 50.0

    def test_three_expansion_signals_adds_75(self):
        inp = make_input(expansion_signals=3, competitive_pressure=True, previous_expansion_done=False)
        assert _growth_score(inp) == 75.0

    def test_four_expansion_signals_capped_at_75(self):
        # 4 * 25 = 100, but min(75, 100) = 75
        inp = make_input(expansion_signals=4, competitive_pressure=True, previous_expansion_done=False)
        assert _growth_score(inp) == 75.0

    def test_no_competitive_pressure_adds_15(self):
        inp = make_input(expansion_signals=0, competitive_pressure=False, previous_expansion_done=False)
        assert _growth_score(inp) == 15.0

    def test_competitive_pressure_no_bonus(self):
        inp = make_input(expansion_signals=0, competitive_pressure=True, previous_expansion_done=False)
        assert _growth_score(inp) == 0.0

    def test_previous_expansion_adds_10(self):
        inp = make_input(expansion_signals=0, competitive_pressure=True, previous_expansion_done=True)
        assert _growth_score(inp) == 10.0

    def test_all_bonuses_combined(self):
        # min(75, 3*25)=75 + 15 (no_competitive) + 10 (prev_expansion) = 100
        inp = make_input(expansion_signals=3, competitive_pressure=False, previous_expansion_done=True)
        assert _growth_score(inp) == 100.0

    def test_clamped_to_100(self):
        # 75 + 15 + 10 = 100 (exactly at max, already tested)
        # Verify clamping works: 75 + 15 + 10 = 100 → not over
        inp = make_input(expansion_signals=5, competitive_pressure=False, previous_expansion_done=True)
        # min(75, 125)=75 + 15 + 10 = 100
        assert _growth_score(inp) == 100.0

    def test_clamped_to_0_min(self):
        inp = make_input(expansion_signals=0, competitive_pressure=True, previous_expansion_done=False)
        assert _growth_score(inp) >= 0.0


# ─── Class 9: _timing_score branches ─────────────────────────────────────────

class TestTimingScore:
    def test_months_zero_returns_40(self):
        inp = make_input(contract_months_remaining=0)
        assert _timing_score(inp) == 40.0

    def test_months_1_returns_70(self):
        inp = make_input(contract_months_remaining=1)
        assert _timing_score(inp) == 70.0

    def test_months_2_returns_70(self):
        inp = make_input(contract_months_remaining=2)
        assert _timing_score(inp) == 70.0

    def test_months_3_returns_100(self):
        inp = make_input(contract_months_remaining=3)
        assert _timing_score(inp) == 100.0

    def test_months_6_returns_100(self):
        inp = make_input(contract_months_remaining=6)
        assert _timing_score(inp) == 100.0

    def test_months_9_returns_100(self):
        inp = make_input(contract_months_remaining=9)
        assert _timing_score(inp) == 100.0

    def test_months_10_returns_60(self):
        inp = make_input(contract_months_remaining=10)
        assert _timing_score(inp) == 60.0

    def test_months_15_returns_60(self):
        inp = make_input(contract_months_remaining=15)
        assert _timing_score(inp) == 60.0

    def test_months_18_returns_60(self):
        inp = make_input(contract_months_remaining=18)
        assert _timing_score(inp) == 60.0

    def test_months_19_returns_30(self):
        inp = make_input(contract_months_remaining=19)
        assert _timing_score(inp) == 30.0

    def test_months_24_returns_30(self):
        inp = make_input(contract_months_remaining=24)
        assert _timing_score(inp) == 30.0

    def test_months_36_returns_30(self):
        inp = make_input(contract_months_remaining=36)
        assert _timing_score(inp) == 30.0

    def test_all_return_floats(self):
        for m in [0, 1, 3, 9, 10, 18, 19]:
            inp = make_input(contract_months_remaining=m)
            assert isinstance(_timing_score(inp), float)


# ─── Class 10: _expansion_score ──────────────────────────────────────────────

class TestExpansionScore:
    def test_all_zero(self):
        assert _expansion_score(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_all_100(self):
        assert _expansion_score(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_weights_sum_to_1(self):
        # util*0.30 + rel*0.25 + growth*0.25 + timing*0.20 = 1.0 for all=100
        result = _expansion_score(100.0, 100.0, 100.0, 100.0)
        assert result == 100.0

    def test_only_util_contributes_30_pct(self):
        result = _expansion_score(100.0, 0.0, 0.0, 0.0)
        assert result == 30.0

    def test_only_rel_contributes_25_pct(self):
        result = _expansion_score(0.0, 100.0, 0.0, 0.0)
        assert result == 25.0

    def test_only_growth_contributes_25_pct(self):
        result = _expansion_score(0.0, 0.0, 100.0, 0.0)
        assert result == 25.0

    def test_only_timing_contributes_20_pct(self):
        result = _expansion_score(0.0, 0.0, 0.0, 100.0)
        assert result == 20.0

    def test_rounding_to_2dp(self):
        # Test that rounding to 2dp works
        result = _expansion_score(33.33, 33.33, 33.33, 33.33)
        assert result == round(33.33 * 0.30 + 33.33 * 0.25 + 33.33 * 0.25 + 33.33 * 0.20, 2)

    def test_typical_values(self):
        result = _expansion_score(80.0, 75.0, 100.0, 100.0)
        expected = round(80.0 * 0.30 + 75.0 * 0.25 + 100.0 * 0.25 + 100.0 * 0.20, 2)
        assert result == expected


# ─── Class 11: _expansion_tier boundaries ────────────────────────────────────

class TestExpansionTierBoundaries:
    def test_score_70_is_hot(self):
        assert _expansion_tier(70.0) == ExpansionTier.HOT

    def test_score_70_point_1_is_hot(self):
        assert _expansion_tier(70.1) == ExpansionTier.HOT

    def test_score_100_is_hot(self):
        assert _expansion_tier(100.0) == ExpansionTier.HOT

    def test_score_69_99_is_warm(self):
        assert _expansion_tier(69.99) == ExpansionTier.WARM

    def test_score_45_is_warm(self):
        assert _expansion_tier(45.0) == ExpansionTier.WARM

    def test_score_44_99_is_cool(self):
        assert _expansion_tier(44.99) == ExpansionTier.COOL

    def test_score_25_is_cool(self):
        assert _expansion_tier(25.0) == ExpansionTier.COOL

    def test_score_24_99_is_cold(self):
        assert _expansion_tier(24.99) == ExpansionTier.COLD

    def test_score_0_is_cold(self):
        assert _expansion_tier(0.0) == ExpansionTier.COLD

    def test_score_negative_is_cold(self):
        assert _expansion_tier(-1.0) == ExpansionTier.COLD


# ─── Class 12: _expansion_action ─────────────────────────────────────────────

class TestExpansionAction:
    def test_hot_tier_returns_close(self):
        inp = make_input()
        assert _expansion_action(ExpansionTier.HOT, inp) == ExpansionAction.CLOSE

    def test_warm_tier_returns_nurture(self):
        inp = make_input()
        assert _expansion_action(ExpansionTier.WARM, inp) == ExpansionAction.NURTURE

    def test_cool_tier_returns_qualify(self):
        inp = make_input()
        assert _expansion_action(ExpansionTier.COOL, inp) == ExpansionAction.QUALIFY

    def test_cold_tier_returns_watch(self):
        inp = make_input()
        assert _expansion_action(ExpansionTier.COLD, inp) == ExpansionAction.WATCH


# ─── Class 13: _opportunity_types ────────────────────────────────────────────

class TestOpportunityTypes:
    def test_seat_expansion_when_seat_util_above_80(self):
        inp = make_input(
            seats_used=85, seats_licensed=100,
            product_tier="enterprise", health_score=50,  # prevent UPSELL
            modules_purchased=6, modules_available=8,    # modules_util=75 → no CROSS_SELL
            contract_months_remaining=0,                  # prevent RENEWAL_UPLIFT
            feature_adoption_pct=60.0,                   # prevent NEW_MODULE
        )
        seat_util = _seat_utilization(inp)   # 85.0
        modules_util = _modules_utilization(inp)  # 75.0
        types = _opportunity_types(inp, seat_util, modules_util)
        assert "SEAT_EXPANSION" in types

    def test_no_seat_expansion_when_seat_util_exactly_80(self):
        inp = make_input(
            seats_used=80, seats_licensed=100,
            product_tier="enterprise", health_score=50,
            modules_purchased=6, modules_available=8,
            contract_months_remaining=0,
            feature_adoption_pct=60.0,
        )
        types = _opportunity_types(inp, 80.0, 75.0)
        assert "SEAT_EXPANSION" not in types

    def test_upsell_when_not_enterprise_and_health_above_65(self):
        inp = make_input(
            product_tier="professional",
            health_score=65.0,
            seats_used=50, seats_licensed=100,       # seat_util=50 → no SEAT_EXPANSION
            modules_purchased=6, modules_available=8, # modules_util=75 → no CROSS_SELL
            contract_months_remaining=0,               # prevent RENEWAL_UPLIFT
            feature_adoption_pct=60.0,                # prevent NEW_MODULE
        )
        types = _opportunity_types(inp, 50.0, 75.0)
        assert "UPSELL" in types

    def test_no_upsell_for_enterprise_tier(self):
        inp = make_input(
            product_tier="enterprise",
            health_score=80.0,
            seats_used=50, seats_licensed=100,
            modules_purchased=6, modules_available=8,
            contract_months_remaining=0,
            feature_adoption_pct=60.0,
        )
        types = _opportunity_types(inp, 50.0, 75.0)
        assert "UPSELL" not in types

    def test_no_upsell_when_health_below_65(self):
        inp = make_input(
            product_tier="professional",
            health_score=64.9,
            seats_used=50, seats_licensed=100,
            modules_purchased=6, modules_available=8,
            contract_months_remaining=0,
            feature_adoption_pct=60.0,
        )
        types = _opportunity_types(inp, 50.0, 75.0)
        assert "UPSELL" not in types

    def test_cross_sell_when_modules_util_below_60_and_more_available(self):
        inp = make_input(
            product_tier="enterprise", health_score=50,  # no UPSELL
            seats_used=50, seats_licensed=100,            # seat_util=50 → no SEAT_EXPANSION
            modules_purchased=3, modules_available=8,     # modules_util=37.5
            contract_months_remaining=0,
            feature_adoption_pct=60.0,
        )
        types = _opportunity_types(inp, 50.0, 37.5)
        assert "CROSS_SELL" in types

    def test_no_cross_sell_when_modules_util_exactly_60(self):
        # modules_util = 60 → NOT < 60
        inp = make_input(
            modules_purchased=6, modules_available=10,
        )
        types = _opportunity_types(inp, 50.0, 60.0)
        assert "CROSS_SELL" not in types

    def test_no_cross_sell_when_all_modules_purchased(self):
        inp = make_input(
            modules_purchased=8, modules_available=8,
        )
        types = _opportunity_types(inp, 50.0, 100.0)
        assert "CROSS_SELL" not in types

    def test_renewal_uplift_when_contract_between_1_and_9_and_health_above_65(self):
        inp = make_input(
            contract_months_remaining=6,
            health_score=65.0,
            product_tier="enterprise",
            seats_used=50, seats_licensed=100,
            modules_purchased=6, modules_available=8,
            feature_adoption_pct=60.0,
        )
        types = _opportunity_types(inp, 50.0, 75.0)
        assert "RENEWAL_UPLIFT" in types

    def test_no_renewal_uplift_when_contract_is_0(self):
        inp = make_input(contract_months_remaining=0, health_score=80.0)
        types = _opportunity_types(inp, 50.0, 75.0)
        assert "RENEWAL_UPLIFT" not in types

    def test_no_renewal_uplift_when_contract_above_9(self):
        inp = make_input(contract_months_remaining=10, health_score=80.0)
        types = _opportunity_types(inp, 50.0, 75.0)
        assert "RENEWAL_UPLIFT" not in types

    def test_no_renewal_uplift_when_health_below_65(self):
        inp = make_input(contract_months_remaining=6, health_score=64.9)
        types = _opportunity_types(inp, 50.0, 75.0)
        assert "RENEWAL_UPLIFT" not in types

    def test_new_module_when_feature_adoption_below_50(self):
        inp = make_input(
            feature_adoption_pct=49.9,
            product_tier="enterprise",
            health_score=50.0,
            seats_used=50, seats_licensed=100,
            modules_purchased=6, modules_available=8,
            contract_months_remaining=0,
        )
        types = _opportunity_types(inp, 50.0, 75.0)
        assert "NEW_MODULE" in types

    def test_no_new_module_when_feature_adoption_exactly_50(self):
        inp = make_input(feature_adoption_pct=50.0)
        types = _opportunity_types(inp, 50.0, 75.0)
        assert "NEW_MODULE" not in types

    def test_no_new_module_when_feature_adoption_above_50(self):
        inp = make_input(feature_adoption_pct=70.0)
        types = _opportunity_types(inp, 50.0, 75.0)
        assert "NEW_MODULE" not in types

    def test_empty_list_when_no_conditions_met(self):
        inp = make_input(
            product_tier="enterprise",     # no UPSELL
            health_score=50.0,            # below 65 → no UPSELL, no RENEWAL_UPLIFT
            seats_used=50, seats_licensed=100,  # 50% → no SEAT_EXPANSION
            modules_purchased=6, modules_available=8,  # 75% → no CROSS_SELL
            contract_months_remaining=0,  # no RENEWAL_UPLIFT
            feature_adoption_pct=60.0,   # no NEW_MODULE
        )
        types = _opportunity_types(inp, 50.0, 75.0)
        assert types == []

    def test_multiple_opportunity_types_can_coexist(self):
        inp = make_input(
            seats_used=90, seats_licensed=100,  # SEAT_EXPANSION
            product_tier="starter",
            health_score=80.0,                 # UPSELL
            modules_purchased=2, modules_available=8,  # CROSS_SELL (25%)
            contract_months_remaining=6,        # RENEWAL_UPLIFT
            feature_adoption_pct=30.0,          # NEW_MODULE
        )
        seat_util = _seat_utilization(inp)      # 90
        modules_util = _modules_utilization(inp)  # 25
        types = _opportunity_types(inp, seat_util, modules_util)
        assert "SEAT_EXPANSION" in types
        assert "UPSELL" in types
        assert "CROSS_SELL" in types
        assert "RENEWAL_UPLIFT" in types
        assert "NEW_MODULE" in types


# ─── Class 14: _estimated_expansion_eur ──────────────────────────────────────

class TestEstimatedExpansionEur:
    def test_seat_expansion_below_cap(self):
        # seat_util = 90/100*100 = 90, additional_pct = min(0.40, (90-80)/100) = 0.10
        inp = make_input(
            current_arr_eur=100_000.0,
            seats_used=90, seats_licensed=100,
        )
        est = _estimated_expansion_eur(inp, 60.0, ["SEAT_EXPANSION"])
        assert est == pytest.approx(10_000.0, rel=1e-6)

    def test_seat_expansion_capped_at_40_pct(self):
        # seat_util = 130% → additional_pct = min(0.40, (130-80)/100) = min(0.40, 0.50) = 0.40
        inp = make_input(
            current_arr_eur=100_000.0,
            seats_used=130, seats_licensed=100,
        )
        est = _estimated_expansion_eur(inp, 60.0, ["SEAT_EXPANSION"])
        assert est == pytest.approx(40_000.0, rel=1e-6)

    def test_upsell_starter_adds_50_pct(self):
        inp = make_input(current_arr_eur=100_000.0, product_tier="starter")
        est = _estimated_expansion_eur(inp, 60.0, ["UPSELL"])
        assert est == pytest.approx(50_000.0, rel=1e-6)

    def test_upsell_professional_adds_30_pct(self):
        inp = make_input(current_arr_eur=100_000.0, product_tier="professional")
        est = _estimated_expansion_eur(inp, 60.0, ["UPSELL"])
        assert est == pytest.approx(30_000.0, rel=1e-6)

    def test_cross_sell_calculation(self):
        # modules_util = 3/8 = 0.375; est += 100000 * (1-0.375) * 0.25 = 15625.0
        inp = make_input(
            current_arr_eur=100_000.0,
            modules_purchased=3, modules_available=8,
        )
        est = _estimated_expansion_eur(inp, 60.0, ["CROSS_SELL"])
        assert est == pytest.approx(15_625.0, rel=1e-6)

    def test_renewal_uplift_adds_10_pct(self):
        inp = make_input(current_arr_eur=100_000.0)
        est = _estimated_expansion_eur(inp, 60.0, ["RENEWAL_UPLIFT"])
        assert est == pytest.approx(10_000.0, rel=1e-6)

    def test_new_module_without_cross_sell_adds_12_pct(self):
        inp = make_input(current_arr_eur=100_000.0)
        est = _estimated_expansion_eur(inp, 60.0, ["NEW_MODULE"])
        assert est == pytest.approx(12_000.0, rel=1e-6)

    def test_new_module_with_cross_sell_not_counted(self):
        # CROSS_SELL present → NEW_MODULE not added
        inp = make_input(
            current_arr_eur=100_000.0,
            modules_purchased=3, modules_available=8,
        )
        est_with_both = _estimated_expansion_eur(inp, 60.0, ["CROSS_SELL", "NEW_MODULE"])
        est_cross_only = _estimated_expansion_eur(inp, 60.0, ["CROSS_SELL"])
        assert est_with_both == est_cross_only

    def test_empty_opportunity_types_returns_zero(self):
        inp = make_input(current_arr_eur=100_000.0)
        est = _estimated_expansion_eur(inp, 60.0, [])
        assert est == 0.0

    def test_multiple_opportunity_types_sum(self):
        inp = make_input(
            current_arr_eur=100_000.0,
            product_tier="starter",         # UPSELL → 50%
            modules_purchased=3, modules_available=8,  # CROSS_SELL → 15.625%
        )
        # UPSELL: 50000, CROSS_SELL: 15625 → total 65625
        est = _estimated_expansion_eur(inp, 60.0, ["UPSELL", "CROSS_SELL"])
        assert est == pytest.approx(65_625.0, rel=1e-6)

    def test_result_rounded_to_2dp(self):
        inp = make_input(current_arr_eur=100_001.0, modules_purchased=1, modules_available=3)
        # CROSS_SELL: modules_util = 1/3; est = 100001 * (1-1/3) * 0.25
        est = _estimated_expansion_eur(inp, 60.0, ["CROSS_SELL"])
        assert est == round(max(0.0, est), 2)

    def test_result_never_negative(self):
        inp = make_input(current_arr_eur=0.0)
        est = _estimated_expansion_eur(inp, 60.0, ["SEAT_EXPANSION", "UPSELL"])
        assert est >= 0.0


# ─── Class 15: _build_signals — positive signals ─────────────────────────────

class TestBuildSignalsPositives:
    def _run(self, **kwargs):
        inp = make_input(**kwargs)
        seat_util = _seat_utilization(inp)
        modules_util = _modules_utilization(inp)
        tier = ExpansionTier.WARM
        opp_types = _opportunity_types(inp, seat_util, modules_util)
        positives, risks, actions = _build_signals(inp, tier, opp_types, seat_util, modules_util)
        return positives, risks, actions

    def test_seat_util_above_90_capacity_message(self):
        positives, _, _ = self._run(seats_used=95, seats_licensed=100)
        assert any("95" in p or "Capacité" in p for p in positives)

    def test_seat_util_above_80_high_utilization_message(self):
        positives, _, _ = self._run(seats_used=85, seats_licensed=100)
        assert any("85" in p or "Forte" in p for p in positives)

    def test_feature_adoption_above_80_excellent_message(self):
        positives, _, _ = self._run(feature_adoption_pct=90.0)
        assert any("excellente" in p or "90" in p for p in positives)

    def test_feature_adoption_above_60_good_message(self):
        positives, _, _ = self._run(feature_adoption_pct=70.0)
        assert any("Bonne" in p or "70" in p for p in positives)

    def test_executive_engagement_message(self):
        positives, _, _ = self._run(executive_engagement=True)
        assert any("exécutif" in p.lower() or "Engagement" in p for p in positives)

    def test_no_exec_engagement_no_message(self):
        positives, _, _ = self._run(executive_engagement=False, champion_strength=0, feature_adoption_pct=60.0)
        assert not any("exécutif" in p.lower() for p in positives)

    def test_champion_above_80_very_active_message(self):
        positives, _, _ = self._run(champion_strength=90)
        assert any("actif" in p or "Champion" in p for p in positives)

    def test_champion_above_60_engaged_message(self):
        positives, _, _ = self._run(champion_strength=70)
        assert any("engagé" in p.lower() or "Champion" in p for p in positives)

    def test_nps_above_50_excellent_message(self):
        positives, _, _ = self._run(nps_score=60)
        assert any("NPS" in p for p in positives)

    def test_nps_minus_999_no_nps_message(self):
        positives, _, _ = self._run(nps_score=-999, executive_engagement=False, champion_strength=0, feature_adoption_pct=60.0)
        assert not any("NPS" in p for p in positives)

    def test_expansion_signals_positive_message(self):
        positives, _, _ = self._run(expansion_signals=2)
        assert any("signal" in p.lower() for p in positives)

    def test_previous_expansion_done_message(self):
        positives, _, _ = self._run(previous_expansion_done=True)
        assert any("Historique" in p or "expansion" in p.lower() for p in positives)

    def test_qbr_within_30_days_message(self):
        positives, _, _ = self._run(days_since_last_qbr=20)
        assert any("QBR" in p for p in positives)

    def test_contract_months_3_to_9_renewal_window_message(self):
        positives, _, _ = self._run(contract_months_remaining=6)
        assert any("Renouvellement" in p or "mois" in p for p in positives)


# ─── Class 16: _build_signals — risk factors ─────────────────────────────────

class TestBuildSignalsRisks:
    def _run_with_tier(self, tier=ExpansionTier.WARM, **kwargs):
        inp = make_input(**kwargs)
        seat_util = _seat_utilization(inp)
        modules_util = _modules_utilization(inp)
        opp_types = _opportunity_types(inp, seat_util, modules_util)
        positives, risks, actions = _build_signals(inp, tier, opp_types, seat_util, modules_util)
        return positives, risks, actions

    def test_competitive_pressure_risk(self):
        _, risks, _ = self._run_with_tier(competitive_pressure=True)
        assert any("concurrentielle" in r or "compétitif" in r.lower() for r in risks)

    def test_health_score_below_50_risk(self):
        _, risks, _ = self._run_with_tier(health_score=40.0)
        assert any("Santé" in r or "santé" in r for r in risks)

    def test_health_score_50_and_above_no_health_risk(self):
        _, risks, _ = self._run_with_tier(health_score=50.0)
        assert not any("Santé" in r for r in risks)

    def test_negative_nps_risk(self):
        _, risks, _ = self._run_with_tier(nps_score=-10)
        assert any("NPS" in r for r in risks)

    def test_nps_minus_999_no_nps_risk(self):
        _, risks, _ = self._run_with_tier(nps_score=-999)
        assert not any("NPS" in r for r in risks)

    def test_champion_below_30_risk(self):
        _, risks, _ = self._run_with_tier(champion_strength=20)
        assert any("Champion" in r or "champion" in r.lower() for r in risks)

    def test_no_exec_engagement_hot_tier_risk(self):
        _, risks, _ = self._run_with_tier(tier=ExpansionTier.HOT, executive_engagement=False)
        assert any("exécutif" in r.lower() or "Pas" in r for r in risks)

    def test_no_exec_engagement_warm_tier_no_such_risk(self):
        # The exec_engagement risk for HOT only (when tier==HOT)
        _, risks, _ = self._run_with_tier(tier=ExpansionTier.WARM, executive_engagement=False)
        assert not any("Pas d'engagement exécutif" in r for r in risks)

    def test_qbr_above_180_days_risk(self):
        _, risks, _ = self._run_with_tier(days_since_last_qbr=200)
        assert any("QBR" in r for r in risks)

    def test_qbr_at_180_no_risk(self):
        _, risks, _ = self._run_with_tier(days_since_last_qbr=180)
        assert not any("QBR" in r for r in risks)

    def test_contract_months_zero_risk(self):
        _, risks, _ = self._run_with_tier(contract_months_remaining=0)
        assert any("expiré" in r.lower() or "Contrat" in r for r in risks)

    def test_feature_adoption_below_30_churn_risk(self):
        _, risks, _ = self._run_with_tier(feature_adoption_pct=20.0)
        assert any("Adoption" in r or "churn" in r.lower() for r in risks)

    def test_feature_adoption_exactly_30_no_churn_risk(self):
        _, risks, _ = self._run_with_tier(feature_adoption_pct=30.0)
        assert not any("risque de churn" in r.lower() for r in risks)

    def test_modules_util_above_90_risk(self):
        inp = make_input(modules_purchased=10, modules_available=10)
        seat_util = _seat_utilization(inp)
        modules_util = _modules_utilization(inp)  # 100.0
        opp_types = _opportunity_types(inp, seat_util, modules_util)
        _, risks, _ = _build_signals(inp, ExpansionTier.WARM, opp_types, seat_util, modules_util)
        assert any("modules" in r.lower() or "expansion" in r.lower() for r in risks)


# ─── Class 17: _build_signals — recommended actions ──────────────────────────

class TestBuildSignalsActions:
    def _run_with_opp(self, opp_types, tier=ExpansionTier.WARM, **kwargs):
        inp = make_input(**kwargs)
        seat_util = _seat_utilization(inp)
        modules_util = _modules_utilization(inp)
        _, _, actions = _build_signals(inp, tier, opp_types, seat_util, modules_util)
        return actions

    def test_seat_expansion_action(self):
        actions = self._run_with_opp(["SEAT_EXPANSION"])
        assert any("licences" in a.lower() or "extension" in a.lower() for a in actions)

    def test_upsell_action(self):
        actions = self._run_with_opp(["UPSELL"])
        assert any("démonstration" in a.lower() or "tier" in a.lower() for a in actions)

    def test_cross_sell_action(self):
        actions = self._run_with_opp(["CROSS_SELL"], modules_purchased=3, modules_available=8)
        assert any("module" in a.lower() or "QBR" in a for a in actions)

    def test_renewal_uplift_action(self):
        actions = self._run_with_opp(["RENEWAL_UPLIFT"], contract_months_remaining=6)
        assert any("renouvellement" in a.lower() or "tarifaire" in a.lower() for a in actions)

    def test_new_module_action(self):
        actions = self._run_with_opp(["NEW_MODULE"], feature_adoption_pct=30.0)
        assert any("adoption" in a.lower() or "activation" in a.lower() for a in actions)

    def test_competitive_pressure_action(self):
        actions = self._run_with_opp([], competitive_pressure=True)
        assert any("valeur" in a.lower() or "Renforcer" in a for a in actions)

    def test_health_score_below_60_action(self):
        actions = self._run_with_opp([], health_score=50.0)
        assert any("santé" in a.lower() or "Priorité" in a for a in actions)

    def test_no_exec_engagement_hot_warm_action(self):
        actions = self._run_with_opp([], tier=ExpansionTier.HOT, executive_engagement=False)
        assert any("executive" in a.lower() or "briefing" in a.lower() for a in actions)

    def test_no_exec_engagement_cold_tier_no_briefing_action(self):
        actions = self._run_with_opp([], tier=ExpansionTier.COLD, executive_engagement=False)
        assert not any("briefing" in a.lower() for a in actions)

    def test_qbr_above_90_days_action(self):
        actions = self._run_with_opp([], days_since_last_qbr=100)
        assert any("QBR" in a for a in actions)

    def test_qbr_exactly_90_no_schedule_action(self):
        actions = self._run_with_opp([], days_since_last_qbr=90)
        assert not any("Planifier un QBR" in a for a in actions)


# ─── Class 18: ExpansionRevenueDetector.detect ───────────────────────────────

class TestDetectorDetect:
    def setup_method(self):
        self.detector = ExpansionRevenueDetector()

    def test_detect_returns_expansion_result(self):
        inp = make_input()
        result = self.detector.detect(inp)
        assert isinstance(result, ExpansionResult)

    def test_detect_stores_result(self):
        inp = make_input(account_id="acct_001")
        self.detector.detect(inp)
        assert self.detector.get("acct_001") is not None

    def test_detect_result_has_correct_account_id(self):
        inp = make_input(account_id="test_123")
        result = self.detector.detect(inp)
        assert result.account_id == "test_123"

    def test_detect_result_has_correct_arr(self):
        inp = make_input(current_arr_eur=200_000.0)
        result = self.detector.detect(inp)
        assert result.current_arr_eur == 200_000.0

    def test_detect_result_has_expansion_tier(self):
        inp = make_input()
        result = self.detector.detect(inp)
        assert isinstance(result.expansion_tier, ExpansionTier)

    def test_detect_result_has_expansion_action(self):
        inp = make_input()
        result = self.detector.detect(inp)
        assert isinstance(result.expansion_action, ExpansionAction)

    def test_detect_result_expansion_score_in_range(self):
        inp = make_input()
        result = self.detector.detect(inp)
        assert 0.0 <= result.expansion_score <= 100.0

    def test_detect_result_has_opportunity_types_list(self):
        inp = make_input()
        result = self.detector.detect(inp)
        assert isinstance(result.opportunity_types, list)

    def test_detect_result_has_signals(self):
        inp = make_input()
        result = self.detector.detect(inp)
        assert isinstance(result.positive_signals, list)
        assert isinstance(result.risk_factors, list)
        assert isinstance(result.recommended_actions, list)

    def test_detect_overwrites_previous_result(self):
        inp1 = make_input(account_id="acct_001", current_arr_eur=100_000.0)
        inp2 = make_input(account_id="acct_001", current_arr_eur=200_000.0)
        self.detector.detect(inp1)
        self.detector.detect(inp2)
        assert self.detector.get("acct_001").current_arr_eur == 200_000.0


# ─── Class 19: ExpansionRevenueDetector.detect_batch ─────────────────────────

class TestDetectorDetectBatch:
    def setup_method(self):
        self.detector = ExpansionRevenueDetector()

    def test_detect_batch_returns_list(self):
        inputs = [make_input(account_id=f"acct_{i}") for i in range(3)]
        results = self.detector.detect_batch(inputs)
        assert isinstance(results, list)
        assert len(results) == 3

    def test_detect_batch_sorted_desc_by_score(self):
        # Create inputs with different scores by varying parameters
        inp_high = make_input(
            account_id="high",
            seats_used=95, seats_licensed=100,
            feature_adoption_pct=90.0,
            executive_engagement=True,
            champion_strength=90,
            nps_score=80,
            days_since_last_qbr=10,
            expansion_signals=3,
            competitive_pressure=False,
            previous_expansion_done=True,
            contract_months_remaining=6,
        )
        inp_low = make_input(
            account_id="low",
            seats_used=20, seats_licensed=100,
            feature_adoption_pct=10.0,
            executive_engagement=False,
            champion_strength=0,
            nps_score=-50,
            days_since_last_qbr=200,
            expansion_signals=0,
            competitive_pressure=True,
            previous_expansion_done=False,
            contract_months_remaining=24,
        )
        results = self.detector.detect_batch([inp_low, inp_high])
        assert results[0].account_id == "high"
        assert results[-1].account_id == "low"

    def test_detect_batch_stores_all_results(self):
        inputs = [make_input(account_id=f"acct_{i}") for i in range(5)]
        self.detector.detect_batch(inputs)
        for i in range(5):
            assert self.detector.get(f"acct_{i}") is not None

    def test_detect_batch_empty_list(self):
        results = self.detector.detect_batch([])
        assert results == []


# ─── Class 20: ExpansionRevenueDetector queries ──────────────────────────────

class TestDetectorQueries:
    def setup_method(self):
        self.detector = ExpansionRevenueDetector()
        # Add a variety of accounts
        inputs = [
            make_input(
                account_id="hot_acct",
                seats_used=95, seats_licensed=100,
                feature_adoption_pct=90.0,
                executive_engagement=True,
                champion_strength=90,
                nps_score=80,
                days_since_last_qbr=10,
                expansion_signals=3,
                competitive_pressure=False,
                previous_expansion_done=True,
                contract_months_remaining=6,
            ),
            make_input(
                account_id="cold_acct",
                seats_used=20, seats_licensed=100,
                feature_adoption_pct=10.0,
                executive_engagement=False,
                champion_strength=0,
                nps_score=-50,
                days_since_last_qbr=200,
                expansion_signals=0,
                competitive_pressure=True,
                previous_expansion_done=False,
                contract_months_remaining=24,
            ),
        ]
        self.detector.detect_batch(inputs)

    def test_get_existing_account(self):
        result = self.detector.get("hot_acct")
        assert result is not None
        assert result.account_id == "hot_acct"

    def test_get_missing_account_returns_none(self):
        assert self.detector.get("nonexistent") is None

    def test_all_accounts_sorted_desc_by_score(self):
        all_r = self.detector.all_accounts()
        scores = [r.expansion_score for r in all_r]
        assert scores == sorted(scores, reverse=True)

    def test_by_tier_returns_correct_tier(self):
        all_r = self.detector.all_accounts()
        for tier in ExpansionTier:
            for r in self.detector.by_tier(tier):
                assert r.expansion_tier == tier

    def test_hot_returns_hot_accounts(self):
        for r in self.detector.hot():
            assert r.expansion_tier == ExpansionTier.HOT

    def test_warm_returns_warm_accounts(self):
        for r in self.detector.warm():
            assert r.expansion_tier == ExpansionTier.WARM

    def test_ready_to_close_returns_close_action(self):
        for r in self.detector.ready_to_close():
            assert r.expansion_action == ExpansionAction.CLOSE

    def test_with_opportunity_type_filters_correctly(self):
        all_r = self.detector.all_accounts()
        for opp_type in ["SEAT_EXPANSION", "UPSELL", "CROSS_SELL", "RENEWAL_UPLIFT", "NEW_MODULE"]:
            filtered = self.detector.with_opportunity_type(opp_type)
            for r in filtered:
                assert opp_type in r.opportunity_types

    def test_with_opportunity_type_unknown_returns_empty(self):
        filtered = self.detector.with_opportunity_type("FAKE_TYPE")
        assert filtered == []


# ─── Class 21: ExpansionRevenueDetector aggregates ───────────────────────────

class TestDetectorAggregates:
    def setup_method(self):
        self.detector = ExpansionRevenueDetector()
        self.detector.detect(make_input(account_id="a1", current_arr_eur=100_000.0))
        self.detector.detect(make_input(account_id="a2", current_arr_eur=200_000.0))

    def test_total_current_arr_eur(self):
        assert self.detector.total_current_arr_eur() == pytest.approx(300_000.0, rel=1e-6)

    def test_total_estimated_expansion_eur_is_float(self):
        total = self.detector.total_estimated_expansion_eur()
        assert isinstance(total, float)
        assert total >= 0.0

    def test_avg_expansion_score_range(self):
        avg = self.detector.avg_expansion_score()
        assert 0.0 <= avg <= 100.0

    def test_avg_expansion_score_empty_returns_zero(self):
        d = ExpansionRevenueDetector()
        assert d.avg_expansion_score() == 0.0

    def test_top_n_returns_n_results(self):
        top = self.detector.top_n(1)
        assert len(top) == 1

    def test_top_n_sorted_by_estimated_expansion_eur_desc(self):
        top = self.detector.top_n(10)
        eurs = [r.estimated_expansion_eur for r in top]
        assert eurs == sorted(eurs, reverse=True)

    def test_top_n_more_than_available(self):
        top = self.detector.top_n(100)
        assert len(top) == 2

    def test_reset_clears_all_results(self):
        self.detector.reset()
        assert self.detector.all_accounts() == []
        assert self.detector.get("a1") is None


# ─── Class 22: ExpansionRevenueDetector.summary ───────────────────────────────

class TestDetectorSummary:
    def setup_method(self):
        self.detector = ExpansionRevenueDetector()

    def test_summary_empty_detector(self):
        summary = self.detector.summary()
        assert summary["total"] == 0
        assert summary["tier_counts"] == {}
        assert summary["action_counts"] == {}
        assert summary["avg_expansion_score"] == 0.0
        assert summary["total_estimated_expansion_eur"] == 0.0
        assert summary["total_current_arr_eur"] == 0.0
        assert summary["hot_count"] == 0
        assert summary["close_ready_count"] == 0

    def test_summary_has_all_required_keys(self):
        self.detector.detect(make_input())
        summary = self.detector.summary()
        required_keys = [
            "total", "tier_counts", "action_counts", "avg_expansion_score",
            "total_estimated_expansion_eur", "total_current_arr_eur",
            "hot_count", "close_ready_count",
        ]
        for key in required_keys:
            assert key in summary

    def test_summary_total_count(self):
        for i in range(3):
            self.detector.detect(make_input(account_id=f"acct_{i}"))
        assert self.detector.summary()["total"] == 3

    def test_summary_tier_counts_correct(self):
        self.detector.detect(make_input())
        summary = self.detector.summary()
        tier_counts = summary["tier_counts"]
        total_from_tiers = sum(tier_counts.values())
        assert total_from_tiers == summary["total"]

    def test_summary_action_counts_correct(self):
        for i in range(3):
            self.detector.detect(make_input(account_id=f"acct_{i}"))
        summary = self.detector.summary()
        action_counts = summary["action_counts"]
        total_from_actions = sum(action_counts.values())
        assert total_from_actions == summary["total"]

    def test_summary_hot_count_matches_hot(self):
        for i in range(3):
            self.detector.detect(make_input(account_id=f"acct_{i}"))
        summary = self.detector.summary()
        assert summary["hot_count"] == len(self.detector.hot())

    def test_summary_close_ready_count_matches_ready_to_close(self):
        for i in range(3):
            self.detector.detect(make_input(account_id=f"acct_{i}"))
        summary = self.detector.summary()
        assert summary["close_ready_count"] == len(self.detector.ready_to_close())


# ─── Class 23: ExpansionResult.to_dict ───────────────────────────────────────

class TestExpansionResultToDict:
    def test_to_dict_returns_dict(self):
        detector = ExpansionRevenueDetector()
        result = detector.detect(make_input())
        assert isinstance(result.to_dict(), dict)

    def test_to_dict_expansion_tier_is_string(self):
        detector = ExpansionRevenueDetector()
        result = detector.detect(make_input())
        d = result.to_dict()
        assert isinstance(d["expansion_tier"], str)

    def test_to_dict_expansion_action_is_string(self):
        detector = ExpansionRevenueDetector()
        result = detector.detect(make_input())
        d = result.to_dict()
        assert isinstance(d["expansion_action"], str)

    def test_to_dict_has_all_fields(self):
        detector = ExpansionRevenueDetector()
        result = detector.detect(make_input())
        d = result.to_dict()
        expected_fields = [
            "account_id", "account_name", "current_arr_eur", "product_tier",
            "expansion_tier", "expansion_action", "expansion_score",
            "utilization_score", "relationship_score", "growth_score", "timing_score",
            "opportunity_types", "estimated_expansion_eur",
            "seat_utilization_pct", "modules_utilization_pct",
            "positive_signals", "risk_factors", "recommended_actions",
        ]
        for field in expected_fields:
            assert field in d


# ─── Class 24: Integration end-to-end scenarios ──────────────────────────────

class TestIntegrationScenarios:
    def test_hot_enterprise_account(self):
        """High utilization + strong relationship + clear expansion signals = HOT"""
        inp = make_input(
            account_id="enterprise_hot",
            current_arr_eur=500_000.0,
            product_tier="professional",
            contract_months_remaining=6,
            seats_used=95, seats_licensed=100,
            feature_adoption_pct=85.0,
            modules_purchased=2, modules_available=8,
            nps_score=60,
            executive_engagement=True,
            champion_strength=85,
            days_since_last_qbr=20,
            expansion_signals=3,
            competitive_pressure=False,
            previous_expansion_done=True,
            health_score=80.0,
        )
        detector = ExpansionRevenueDetector()
        result = detector.detect(inp)
        assert result.expansion_tier == ExpansionTier.HOT
        assert result.expansion_action == ExpansionAction.CLOSE
        assert result.estimated_expansion_eur > 0
        assert len(result.opportunity_types) > 0

    def test_cold_account_with_competitive_pressure(self):
        """Low usage + bad NPS + competitive threat = COLD"""
        inp = make_input(
            account_id="cold_risky",
            current_arr_eur=50_000.0,
            product_tier="starter",
            contract_months_remaining=24,
            seats_used=10, seats_licensed=100,
            feature_adoption_pct=10.0,
            modules_purchased=1, modules_available=8,
            nps_score=-40,
            executive_engagement=False,
            champion_strength=10,
            days_since_last_qbr=200,
            expansion_signals=0,
            competitive_pressure=True,
            previous_expansion_done=False,
            health_score=30.0,
        )
        detector = ExpansionRevenueDetector()
        result = detector.detect(inp)
        assert result.expansion_tier == ExpansionTier.COLD
        assert result.expansion_action == ExpansionAction.WATCH
        assert len(result.risk_factors) > 0

    def test_seat_utilization_computed_correctly_in_result(self):
        inp = make_input(seats_used=80, seats_licensed=100)
        detector = ExpansionRevenueDetector()
        result = detector.detect(inp)
        assert result.seat_utilization_pct == 80.0

    def test_modules_utilization_computed_correctly_in_result(self):
        inp = make_input(modules_purchased=4, modules_available=8)
        detector = ExpansionRevenueDetector()
        result = detector.detect(inp)
        assert result.modules_utilization_pct == 50.0

    def test_batch_ordering_with_three_accounts(self):
        detector = ExpansionRevenueDetector()
        inputs = [
            make_input(account_id="mid", expansion_signals=1, competitive_pressure=False),
            make_input(account_id="best", expansion_signals=3, competitive_pressure=False,
                       executive_engagement=True, champion_strength=90, nps_score=70,
                       seats_used=95, seats_licensed=100, feature_adoption_pct=90.0,
                       contract_months_remaining=6, days_since_last_qbr=10,
                       previous_expansion_done=True),
            make_input(account_id="worst", expansion_signals=0, competitive_pressure=True,
                       executive_engagement=False, champion_strength=0, nps_score=-50,
                       seats_used=5, seats_licensed=100, feature_adoption_pct=5.0,
                       contract_months_remaining=24, days_since_last_qbr=300),
        ]
        results = detector.detect_batch(inputs)
        account_ids = [r.account_id for r in results]
        assert account_ids[0] == "best"
        assert account_ids[-1] == "worst"

    def test_total_estimated_expansion_across_multiple_accounts(self):
        detector = ExpansionRevenueDetector()
        detector.detect(make_input(account_id="a1", current_arr_eur=100_000.0))
        detector.detect(make_input(account_id="a2", current_arr_eur=100_000.0))
        total = detector.total_estimated_expansion_eur()
        # Just verify it's non-negative and a float
        assert isinstance(total, float)
        assert total >= 0.0
