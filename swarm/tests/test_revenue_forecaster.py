"""
Comprehensive tests for swarm/intelligence/revenue_forecaster.py
Run from /home/user/TEST:
    python -m pytest swarm/tests/test_revenue_forecaster.py -v
"""

from __future__ import annotations

import pytest

from swarm.intelligence.revenue_forecaster import (
    DealRisk,
    QuarterLabel,
    ForecastScenario,
    ForecastDeal,
    ForecastDealResult,
    RevenueForecast,
    RevenueForecastEngine,
    _STAGE_WIN_PROB,
    _STAGE_MAX_DAYS,
    _quarter_label,
    _adjusted_win_probability,
    _scenario_probability,
    _deal_risk,
    _build_factors,
    _pipeline_health_score,
)


# ─── Shared helpers ────────────────────────────────────────────────────────────

def make_deal(
    deal_id: str = "D1",
    deal_name: str = "Test Deal",
    amount_eur: float = 10_000.0,
    stage: str = "proposal",
    close_date_days: int = 30,
    segment: str = "smb",
    days_in_stage: int = 5,
    num_competitors: int = 0,
    champion_strength: float = 60.0,
    has_verbal_commit: bool = False,
    has_budget_approved: bool = False,
    is_renewal: bool = False,
) -> ForecastDeal:
    return ForecastDeal(
        deal_id=deal_id,
        deal_name=deal_name,
        amount_eur=amount_eur,
        stage=stage,
        close_date_days=close_date_days,
        segment=segment,
        days_in_stage=days_in_stage,
        num_competitors=num_competitors,
        champion_strength=champion_strength,
        has_verbal_commit=has_verbal_commit,
        has_budget_approved=has_budget_approved,
        is_renewal=is_renewal,
    )


def engine_with_forecast(deals=None) -> tuple[RevenueForecastEngine, RevenueForecast]:
    e = RevenueForecastEngine()
    if deals is None:
        deals = [make_deal()]
    f = e.forecast(deals)
    return e, f


# ─── 1. Enums ─────────────────────────────────────────────────────────────────

class TestEnums:
    def test_deal_risk_values(self):
        assert DealRisk.HIGH.value == "high"
        assert DealRisk.MEDIUM.value == "medium"
        assert DealRisk.LOW.value == "low"
        assert DealRisk.NONE.value == "none"

    def test_quarter_label_values(self):
        assert QuarterLabel.CURRENT.value == "current_quarter"
        assert QuarterLabel.NEXT.value == "next_quarter"
        assert QuarterLabel.BEYOND.value == "beyond"

    def test_forecast_scenario_values(self):
        assert ForecastScenario.CONSERVATIVE.value == "conservative"
        assert ForecastScenario.BASE.value == "base"
        assert ForecastScenario.OPTIMISTIC.value == "optimistic"

    def test_deal_risk_is_str_enum(self):
        assert isinstance(DealRisk.HIGH, str)

    def test_quarter_label_is_str_enum(self):
        assert isinstance(QuarterLabel.CURRENT, str)

    def test_forecast_scenario_is_str_enum(self):
        assert isinstance(ForecastScenario.BASE, str)

    def test_deal_risk_membership(self):
        members = {r.value for r in DealRisk}
        assert members == {"high", "medium", "low", "none"}

    def test_quarter_label_membership(self):
        members = {q.value for q in QuarterLabel}
        assert members == {"current_quarter", "next_quarter", "beyond"}

    def test_forecast_scenario_membership(self):
        members = {s.value for s in ForecastScenario}
        assert members == {"conservative", "base", "optimistic"}


# ─── 2. Stage constants ────────────────────────────────────────────────────────

class TestStageConstants:
    def test_stage_win_prob_all_stages_present(self):
        for stage in ("prospecting", "qualification", "demo", "proposal", "negotiation", "closing"):
            assert stage in _STAGE_WIN_PROB

    def test_stage_win_prob_prospecting(self):
        assert _STAGE_WIN_PROB["prospecting"] == pytest.approx(0.10)

    def test_stage_win_prob_qualification(self):
        assert _STAGE_WIN_PROB["qualification"] == pytest.approx(0.20)

    def test_stage_win_prob_demo(self):
        assert _STAGE_WIN_PROB["demo"] == pytest.approx(0.35)

    def test_stage_win_prob_proposal(self):
        assert _STAGE_WIN_PROB["proposal"] == pytest.approx(0.50)

    def test_stage_win_prob_negotiation(self):
        assert _STAGE_WIN_PROB["negotiation"] == pytest.approx(0.70)

    def test_stage_win_prob_closing(self):
        assert _STAGE_WIN_PROB["closing"] == pytest.approx(0.85)

    def test_stage_max_days_all_stages_present(self):
        for stage in ("prospecting", "qualification", "demo", "proposal", "negotiation", "closing"):
            assert stage in _STAGE_MAX_DAYS

    def test_stage_max_days_prospecting(self):
        assert _STAGE_MAX_DAYS["prospecting"] == 14

    def test_stage_max_days_qualification(self):
        assert _STAGE_MAX_DAYS["qualification"] == 21

    def test_stage_max_days_demo(self):
        assert _STAGE_MAX_DAYS["demo"] == 21

    def test_stage_max_days_proposal(self):
        assert _STAGE_MAX_DAYS["proposal"] == 30

    def test_stage_max_days_negotiation(self):
        assert _STAGE_MAX_DAYS["negotiation"] == 21

    def test_stage_max_days_closing(self):
        assert _STAGE_MAX_DAYS["closing"] == 14

    def test_all_win_probs_in_range(self):
        for prob in _STAGE_WIN_PROB.values():
            assert 0.0 < prob < 1.0

    def test_win_prob_increases_across_funnel(self):
        stages = ["prospecting", "qualification", "demo", "proposal", "negotiation", "closing"]
        probs = [_STAGE_WIN_PROB[s] for s in stages]
        assert probs == sorted(probs)


# ─── 3. _quarter_label ────────────────────────────────────────────────────────

class TestQuarterLabel:
    def test_negative_is_current(self):
        assert _quarter_label(-10) == QuarterLabel.CURRENT

    def test_zero_is_current(self):
        assert _quarter_label(0) == QuarterLabel.CURRENT

    def test_boundary_90_is_current(self):
        assert _quarter_label(90) == QuarterLabel.CURRENT

    def test_91_is_next(self):
        assert _quarter_label(91) == QuarterLabel.NEXT

    def test_boundary_180_is_next(self):
        assert _quarter_label(180) == QuarterLabel.NEXT

    def test_181_is_beyond(self):
        assert _quarter_label(181) == QuarterLabel.BEYOND

    def test_very_large_is_beyond(self):
        assert _quarter_label(999) == QuarterLabel.BEYOND

    def test_very_negative_is_current(self):
        assert _quarter_label(-365) == QuarterLabel.CURRENT

    def test_mid_next_range(self):
        assert _quarter_label(135) == QuarterLabel.NEXT

    def test_day_1_is_current(self):
        assert _quarter_label(1) == QuarterLabel.CURRENT


# ─── 4. _adjusted_win_probability ─────────────────────────────────────────────

class TestAdjustedWinProbability:
    def test_base_with_neutral_attrs_proposal(self):
        # base=0.50, no adj triggers
        deal = make_deal(stage="proposal", champion_strength=60, num_competitors=0,
                         has_budget_approved=False, has_verbal_commit=False,
                         is_renewal=False, close_date_days=30, days_in_stage=5)
        result = _adjusted_win_probability(deal)
        assert result == pytest.approx(0.50)

    def test_base_prospecting(self):
        deal = make_deal(stage="prospecting", champion_strength=60)
        result = _adjusted_win_probability(deal)
        assert result == pytest.approx(0.10)

    def test_base_qualification(self):
        deal = make_deal(stage="qualification", champion_strength=60)
        assert _adjusted_win_probability(deal) == pytest.approx(0.20)

    def test_base_demo(self):
        deal = make_deal(stage="demo", champion_strength=60)
        assert _adjusted_win_probability(deal) == pytest.approx(0.35)

    def test_base_negotiation(self):
        deal = make_deal(stage="negotiation", champion_strength=60)
        assert _adjusted_win_probability(deal) == pytest.approx(0.70)

    def test_base_closing(self):
        deal = make_deal(stage="closing", champion_strength=60)
        assert _adjusted_win_probability(deal) == pytest.approx(0.85)

    def test_unknown_stage_defaults_to_020(self):
        deal = make_deal(stage="discovery", champion_strength=60)
        assert _adjusted_win_probability(deal) == pytest.approx(0.20)

    def test_stage_case_insensitive(self):
        deal = make_deal(stage="Proposal", champion_strength=60)
        assert _adjusted_win_probability(deal) == pytest.approx(0.50)

    def test_champion_strength_75_adds_008(self):
        deal_base = make_deal(stage="qualification", champion_strength=60)
        deal_champ = make_deal(stage="qualification", champion_strength=75)
        assert _adjusted_win_probability(deal_champ) == pytest.approx(
            _adjusted_win_probability(deal_base) + 0.08
        )

    def test_champion_strength_exactly_75_adds_008(self):
        deal = make_deal(stage="demo", champion_strength=75, num_competitors=0,
                         has_budget_approved=False, has_verbal_commit=False,
                         close_date_days=30, days_in_stage=5, is_renewal=False)
        assert _adjusted_win_probability(deal) == pytest.approx(0.35 + 0.08)

    def test_champion_strength_above_75_adds_008(self):
        deal = make_deal(stage="demo", champion_strength=100, num_competitors=0,
                         has_budget_approved=False, has_verbal_commit=False,
                         close_date_days=30, days_in_stage=5, is_renewal=False)
        assert _adjusted_win_probability(deal) == pytest.approx(0.35 + 0.08)

    def test_champion_strength_below_40_subtracts_010(self):
        deal = make_deal(stage="demo", champion_strength=39, num_competitors=0,
                         has_budget_approved=False, has_verbal_commit=False,
                         close_date_days=30, days_in_stage=5, is_renewal=False)
        assert _adjusted_win_probability(deal) == pytest.approx(0.35 - 0.10)

    def test_champion_strength_exactly_40_no_penalty(self):
        deal_base = make_deal(stage="demo", champion_strength=60)
        deal_40 = make_deal(stage="demo", champion_strength=40)
        # neither 40 >= 75 nor 40 < 40, so no adj
        assert _adjusted_win_probability(deal_40) == _adjusted_win_probability(deal_base)

    def test_has_budget_approved_adds_010(self):
        deal = make_deal(stage="demo", champion_strength=60, has_budget_approved=True,
                         num_competitors=0, has_verbal_commit=False, close_date_days=30,
                         days_in_stage=5, is_renewal=False)
        assert _adjusted_win_probability(deal) == pytest.approx(0.35 + 0.10)

    def test_has_verbal_commit_adds_012(self):
        deal = make_deal(stage="demo", champion_strength=60, has_verbal_commit=True,
                         num_competitors=0, has_budget_approved=False, close_date_days=30,
                         days_in_stage=5, is_renewal=False)
        assert _adjusted_win_probability(deal) == pytest.approx(0.35 + 0.12)

    def test_four_competitors_subtracts_008(self):
        deal = make_deal(stage="demo", champion_strength=60, num_competitors=4,
                         has_budget_approved=False, has_verbal_commit=False,
                         close_date_days=30, days_in_stage=5, is_renewal=False)
        assert _adjusted_win_probability(deal) == pytest.approx(0.35 - 0.08)

    def test_five_competitors_subtracts_008(self):
        deal = make_deal(stage="demo", champion_strength=60, num_competitors=5,
                         has_budget_approved=False, has_verbal_commit=False,
                         close_date_days=30, days_in_stage=5, is_renewal=False)
        assert _adjusted_win_probability(deal) == pytest.approx(0.35 - 0.08)

    def test_two_competitors_subtracts_004(self):
        deal = make_deal(stage="demo", champion_strength=60, num_competitors=2,
                         has_budget_approved=False, has_verbal_commit=False,
                         close_date_days=30, days_in_stage=5, is_renewal=False)
        assert _adjusted_win_probability(deal) == pytest.approx(0.35 - 0.04)

    def test_three_competitors_subtracts_004(self):
        deal = make_deal(stage="demo", champion_strength=60, num_competitors=3,
                         has_budget_approved=False, has_verbal_commit=False,
                         close_date_days=30, days_in_stage=5, is_renewal=False)
        assert _adjusted_win_probability(deal) == pytest.approx(0.35 - 0.04)

    def test_one_competitor_no_penalty(self):
        deal_base = make_deal(stage="demo", champion_strength=60, num_competitors=0)
        deal_1 = make_deal(stage="demo", champion_strength=60, num_competitors=1)
        assert _adjusted_win_probability(deal_1) == _adjusted_win_probability(deal_base)

    def test_overdue_subtracts_010(self):
        deal = make_deal(stage="demo", champion_strength=60, close_date_days=-1,
                         num_competitors=0, has_budget_approved=False, has_verbal_commit=False,
                         days_in_stage=5, is_renewal=False)
        assert _adjusted_win_probability(deal) == pytest.approx(0.35 - 0.10)

    def test_days_in_stage_double_max_subtracts_008(self):
        # proposal max_days=30, 2x=60
        deal = make_deal(stage="proposal", champion_strength=60, days_in_stage=61,
                         num_competitors=0, has_budget_approved=False, has_verbal_commit=False,
                         close_date_days=30, is_renewal=False)
        assert _adjusted_win_probability(deal) == pytest.approx(0.50 - 0.08)

    def test_days_in_stage_1_5x_max_subtracts_004(self):
        # proposal max_days=30, 1.5x=45, so days_in_stage=46 triggers -0.04 but not -0.08
        deal = make_deal(stage="proposal", champion_strength=60, days_in_stage=46,
                         num_competitors=0, has_budget_approved=False, has_verbal_commit=False,
                         close_date_days=30, is_renewal=False)
        assert _adjusted_win_probability(deal) == pytest.approx(0.50 - 0.04)

    def test_days_in_stage_at_exactly_double_max_subtracts_008(self):
        # closing max_days=14, 2x=28
        deal = make_deal(stage="closing", champion_strength=60, days_in_stage=29,
                         num_competitors=0, has_budget_approved=False, has_verbal_commit=False,
                         close_date_days=30, is_renewal=False)
        assert _adjusted_win_probability(deal) == pytest.approx(0.85 - 0.08)

    def test_days_in_stage_between_1_5_and_2x(self):
        # closing max=14, 1.5x=21, 2x=28; days=22 triggers -0.04
        deal = make_deal(stage="closing", champion_strength=60, days_in_stage=22,
                         num_competitors=0, has_budget_approved=False, has_verbal_commit=False,
                         close_date_days=30, is_renewal=False)
        assert _adjusted_win_probability(deal) == pytest.approx(0.85 - 0.04)

    def test_is_renewal_adds_005(self):
        deal = make_deal(stage="demo", champion_strength=60, is_renewal=True,
                         num_competitors=0, has_budget_approved=False, has_verbal_commit=False,
                         close_date_days=30, days_in_stage=5)
        assert _adjusted_win_probability(deal) == pytest.approx(0.35 + 0.05)

    def test_result_clamped_to_max_097(self):
        # closing + all positives → might exceed 0.97
        deal = make_deal(stage="closing", champion_strength=90, has_budget_approved=True,
                         has_verbal_commit=True, is_renewal=True, num_competitors=0,
                         close_date_days=10, days_in_stage=1)
        result = _adjusted_win_probability(deal)
        assert result <= 0.97

    def test_result_clamped_to_min_003(self):
        # prospecting + all negatives → might go below 0.03
        deal = make_deal(stage="prospecting", champion_strength=10, has_budget_approved=False,
                         has_verbal_commit=False, is_renewal=False, num_competitors=5,
                         close_date_days=-30, days_in_stage=100)
        result = _adjusted_win_probability(deal)
        assert result >= 0.03

    def test_multiple_adjustments_combine(self):
        # proposal base=0.50, has_verbal_commit=+0.12, is_renewal=+0.05
        deal = make_deal(stage="proposal", champion_strength=60, has_verbal_commit=True,
                         is_renewal=True, num_competitors=0, has_budget_approved=False,
                         close_date_days=30, days_in_stage=5)
        assert _adjusted_win_probability(deal) == pytest.approx(0.50 + 0.12 + 0.05)

    def test_return_type_is_float(self):
        deal = make_deal()
        assert isinstance(_adjusted_win_probability(deal), float)


# ─── 5. _scenario_probability ─────────────────────────────────────────────────

class TestScenarioProbability:
    def test_base_returns_unchanged(self):
        assert _scenario_probability(0.50, ForecastScenario.BASE) == pytest.approx(0.50)

    def test_conservative_multiplies_070(self):
        assert _scenario_probability(0.50, ForecastScenario.CONSERVATIVE) == pytest.approx(0.35)

    def test_optimistic_multiplies_130(self):
        assert _scenario_probability(0.50, ForecastScenario.OPTIMISTIC) == pytest.approx(0.65)

    def test_conservative_floor_003(self):
        assert _scenario_probability(0.03, ForecastScenario.CONSERVATIVE) == pytest.approx(0.03)

    def test_optimistic_cap_097(self):
        # 0.97 * 1.30 > 0.97, should cap
        result = _scenario_probability(0.97, ForecastScenario.OPTIMISTIC)
        assert result == pytest.approx(0.97)

    def test_conservative_very_low_adj_floor(self):
        result = _scenario_probability(0.04, ForecastScenario.CONSERVATIVE)
        # 0.04 * 0.70 = 0.028 < 0.03, should floor
        assert result == pytest.approx(0.03)

    def test_optimistic_near_cap(self):
        result = _scenario_probability(0.80, ForecastScenario.OPTIMISTIC)
        # 0.80 * 1.30 = 1.04 > 0.97, cap
        assert result == pytest.approx(0.97)

    def test_all_scenarios_ordering(self):
        adj = 0.50
        c = _scenario_probability(adj, ForecastScenario.CONSERVATIVE)
        b = _scenario_probability(adj, ForecastScenario.BASE)
        o = _scenario_probability(adj, ForecastScenario.OPTIMISTIC)
        assert c <= b <= o

    def test_base_exact_passthrough(self):
        for val in (0.10, 0.35, 0.75, 0.97):
            assert _scenario_probability(val, ForecastScenario.BASE) == pytest.approx(val)

    def test_conservative_rounding(self):
        # 0.35 * 0.70 = 0.245
        result = _scenario_probability(0.35, ForecastScenario.CONSERVATIVE)
        assert result == pytest.approx(0.245)


# ─── 6. _deal_risk ────────────────────────────────────────────────────────────

class TestDealRisk:
    def test_low_adj_prob_is_high_risk(self):
        deal = make_deal(stage="proposal", days_in_stage=5, close_date_days=30)
        assert _deal_risk(deal, 0.20) == DealRisk.HIGH

    def test_exactly_025_is_high_risk(self):
        deal = make_deal(stage="proposal", days_in_stage=5, close_date_days=30)
        assert _deal_risk(deal, 0.24) == DealRisk.HIGH

    def test_overdue_and_below_050_is_high_risk(self):
        deal = make_deal(stage="proposal", days_in_stage=5, close_date_days=-1)
        assert _deal_risk(deal, 0.40) == DealRisk.HIGH

    def test_overdue_but_above_050_not_high(self):
        deal = make_deal(stage="proposal", days_in_stage=5, close_date_days=-1)
        risk = _deal_risk(deal, 0.55)
        assert risk != DealRisk.HIGH

    def test_adj_025_exact_medium_not_high(self):
        deal = make_deal(stage="proposal", days_in_stage=5, close_date_days=30)
        # 0.25 is NOT < 0.25, so not HIGH, but < 0.45 → MEDIUM
        assert _deal_risk(deal, 0.25) == DealRisk.MEDIUM

    def test_adj_below_045_is_medium(self):
        deal = make_deal(stage="proposal", days_in_stage=5, close_date_days=30)
        assert _deal_risk(deal, 0.30) == DealRisk.MEDIUM

    def test_stale_deal_is_medium(self):
        # proposal max=30, 2x=60; days_in_stage=61 → stale
        deal = make_deal(stage="proposal", days_in_stage=61, close_date_days=30)
        assert _deal_risk(deal, 0.60) == DealRisk.MEDIUM

    def test_adj_075_or_above_is_none(self):
        deal = make_deal(stage="proposal", days_in_stage=5, close_date_days=30)
        assert _deal_risk(deal, 0.75) == DealRisk.NONE

    def test_adj_above_075_is_none(self):
        deal = make_deal(stage="proposal", days_in_stage=5, close_date_days=30)
        assert _deal_risk(deal, 0.90) == DealRisk.NONE

    def test_adj_045_to_075_not_stale_is_low(self):
        deal = make_deal(stage="proposal", days_in_stage=5, close_date_days=30)
        assert _deal_risk(deal, 0.60) == DealRisk.LOW

    def test_adj_exactly_045_is_low(self):
        deal = make_deal(stage="proposal", days_in_stage=5, close_date_days=30)
        assert _deal_risk(deal, 0.45) == DealRisk.LOW

    def test_staleness_uses_correct_max_days_per_stage(self):
        # closing max=14, 2x=28; days=29 → stale
        deal = make_deal(stage="closing", days_in_stage=29, close_date_days=30)
        assert _deal_risk(deal, 0.60) == DealRisk.MEDIUM

    def test_unknown_stage_max_days_defaults_21(self):
        deal = make_deal(stage="unknown_stage", days_in_stage=43, close_date_days=30)
        # 43 > 21*2=42 → stale → MEDIUM
        assert _deal_risk(deal, 0.60) == DealRisk.MEDIUM

    def test_not_stale_just_below_double_max(self):
        # proposal max=30, 2x=60; days=60 → NOT stale (not >60)
        deal = make_deal(stage="proposal", days_in_stage=60, close_date_days=30)
        # adj=0.60 → not HIGH (>=0.25), not stale, >= 0.45, < 0.75 → LOW
        assert _deal_risk(deal, 0.60) == DealRisk.LOW


# ─── 7. _build_factors ────────────────────────────────────────────────────────

class TestBuildFactors:
    def test_clean_deal_no_risk_factors(self):
        deal = make_deal(stage="demo", champion_strength=60, num_competitors=0,
                         close_date_days=30, has_budget_approved=False,
                         days_in_stage=5, has_verbal_commit=False, is_renewal=False)
        risks, _ = _build_factors(deal, 0.50)
        assert risks == []

    def test_overdue_adds_risk_factor(self):
        deal = make_deal(close_date_days=-5, champion_strength=60, num_competitors=0,
                         days_in_stage=5, stage="demo")
        risks, _ = _build_factors(deal, 0.40)
        assert any("5j" in r for r in risks)

    def test_overdue_risk_message_contains_delay(self):
        deal = make_deal(close_date_days=-10, champion_strength=60, num_competitors=0,
                         days_in_stage=5, stage="demo")
        risks, _ = _build_factors(deal, 0.40)
        assert any("10j" in r for r in risks)

    def test_stale_deal_adds_blocked_risk(self):
        deal = make_deal(stage="proposal", days_in_stage=65, champion_strength=60,
                         num_competitors=0, close_date_days=30, has_budget_approved=True)
        risks, _ = _build_factors(deal, 0.60)
        assert any("bloqué" in r.lower() for r in risks)

    def test_stale_blocked_message_contains_stage(self):
        deal = make_deal(stage="proposal", days_in_stage=65, champion_strength=60,
                         num_competitors=0, close_date_days=30, has_budget_approved=True)
        risks, _ = _build_factors(deal, 0.60)
        assert any("proposal" in r for r in risks)

    def test_four_competitors_strong_competitive_risk(self):
        deal = make_deal(num_competitors=4, champion_strength=60, close_date_days=30,
                         days_in_stage=5, stage="demo", has_budget_approved=True)
        risks, _ = _build_factors(deal, 0.40)
        assert any("forte" in r for r in risks)

    def test_two_competitors_comparative_risk(self):
        deal = make_deal(num_competitors=2, champion_strength=60, close_date_days=30,
                         days_in_stage=5, stage="demo", has_budget_approved=True)
        risks, _ = _build_factors(deal, 0.40)
        assert any("comparative" in r for r in risks)

    def test_one_competitor_no_competitive_risk(self):
        deal = make_deal(num_competitors=1, champion_strength=60, close_date_days=30,
                         days_in_stage=5, stage="demo", has_budget_approved=True)
        risks, _ = _build_factors(deal, 0.40)
        assert not any("concurrent" in r for r in risks)

    def test_weak_champion_adds_risk(self):
        deal = make_deal(champion_strength=30, num_competitors=0, close_date_days=30,
                         days_in_stage=5, stage="demo", has_budget_approved=True)
        risks, _ = _build_factors(deal, 0.40)
        assert any("faible" in r.lower() for r in risks)

    def test_strong_champion_no_weak_risk(self):
        deal = make_deal(champion_strength=80, num_competitors=0, close_date_days=30,
                         days_in_stage=5, stage="demo", has_budget_approved=True)
        risks, _ = _build_factors(deal, 0.70)
        assert not any("faible" in r.lower() for r in risks)

    def test_budget_not_approved_at_proposal_adds_risk(self):
        deal = make_deal(stage="proposal", has_budget_approved=False, champion_strength=60,
                         num_competitors=0, close_date_days=30, days_in_stage=5)
        risks, _ = _build_factors(deal, 0.50)
        assert any("budget" in r.lower() for r in risks)

    def test_budget_not_approved_at_negotiation_adds_risk(self):
        deal = make_deal(stage="negotiation", has_budget_approved=False, champion_strength=60,
                         num_competitors=0, close_date_days=30, days_in_stage=5)
        risks, _ = _build_factors(deal, 0.70)
        assert any("budget" in r.lower() for r in risks)

    def test_budget_not_approved_at_closing_adds_risk(self):
        deal = make_deal(stage="closing", has_budget_approved=False, champion_strength=60,
                         num_competitors=0, close_date_days=30, days_in_stage=5)
        risks, _ = _build_factors(deal, 0.85)
        assert any("budget" in r.lower() for r in risks)

    def test_budget_not_approved_at_demo_no_risk(self):
        deal = make_deal(stage="demo", has_budget_approved=False, champion_strength=60,
                         num_competitors=0, close_date_days=30, days_in_stage=5)
        risks, _ = _build_factors(deal, 0.35)
        assert not any("budget" in r.lower() for r in risks)

    def test_verbal_commit_upside(self):
        deal = make_deal(has_verbal_commit=True, champion_strength=60, num_competitors=0,
                         close_date_days=30, days_in_stage=5, stage="demo",
                         has_budget_approved=True)
        _, upsides = _build_factors(deal, 0.50)
        assert any("verbal" in u.lower() or "engagement" in u.lower() for u in upsides)

    def test_budget_approved_upside(self):
        deal = make_deal(has_budget_approved=True, champion_strength=60, num_competitors=0,
                         close_date_days=30, days_in_stage=5, stage="demo",
                         has_verbal_commit=False)
        _, upsides = _build_factors(deal, 0.50)
        assert any("budget" in u.lower() or "approuvé" in u.lower() for u in upsides)

    def test_strong_champion_upside(self):
        deal = make_deal(champion_strength=80, num_competitors=0, close_date_days=30,
                         days_in_stage=5, stage="demo", has_budget_approved=True,
                         has_verbal_commit=False, is_renewal=False)
        _, upsides = _build_factors(deal, 0.50)
        assert any("champion" in u.lower() or "fort" in u.lower() for u in upsides)

    def test_renewal_upside(self):
        deal = make_deal(is_renewal=True, champion_strength=60, num_competitors=0,
                         close_date_days=30, days_in_stage=5, stage="demo",
                         has_budget_approved=True, has_verbal_commit=False)
        _, upsides = _build_factors(deal, 0.50)
        assert any("renouvellement" in u.lower() for u in upsides)

    def test_close_within_30_days_upside(self):
        deal = make_deal(close_date_days=20, champion_strength=60, num_competitors=0,
                         days_in_stage=5, stage="demo", has_budget_approved=True,
                         has_verbal_commit=False, is_renewal=False)
        _, upsides = _build_factors(deal, 0.50)
        assert any("20j" in u for u in upsides)

    def test_close_exactly_30_days_upside(self):
        deal = make_deal(close_date_days=30, champion_strength=60, num_competitors=0,
                         days_in_stage=5, stage="demo", has_budget_approved=True,
                         has_verbal_commit=False, is_renewal=False)
        _, upsides = _build_factors(deal, 0.50)
        assert any("30j" in u for u in upsides)

    def test_close_31_days_no_momentum_upside(self):
        deal = make_deal(close_date_days=31, champion_strength=60, num_competitors=0,
                         days_in_stage=5, stage="demo", has_budget_approved=True,
                         has_verbal_commit=False, is_renewal=False)
        _, upsides = _build_factors(deal, 0.50)
        assert not any("momentum" in u.lower() for u in upsides)

    def test_overdue_no_close_soon_upside(self):
        deal = make_deal(close_date_days=-5, champion_strength=60, num_competitors=0,
                         days_in_stage=5, stage="demo", has_budget_approved=True,
                         has_verbal_commit=False, is_renewal=False)
        _, upsides = _build_factors(deal, 0.40)
        assert not any("momentum" in u.lower() for u in upsides)

    def test_returns_tuple_of_two_lists(self):
        deal = make_deal()
        result = _build_factors(deal, 0.50)
        assert isinstance(result, tuple)
        assert len(result) == 2
        risks, upsides = result
        assert isinstance(risks, list)
        assert isinstance(upsides, list)

    def test_no_upside_no_verbal_budget_champion_renewal_soon(self):
        deal = make_deal(stage="qualification", champion_strength=50, num_competitors=1,
                         close_date_days=60, days_in_stage=5,
                         has_verbal_commit=False, has_budget_approved=False, is_renewal=False)
        _, upsides = _build_factors(deal, 0.40)
        assert upsides == []

    def test_num_competitors_count_in_message(self):
        deal = make_deal(num_competitors=5, champion_strength=60, close_date_days=30,
                         days_in_stage=5, stage="demo", has_budget_approved=True)
        risks, _ = _build_factors(deal, 0.40)
        assert any("5" in r for r in risks)


# ─── 8. _pipeline_health_score ────────────────────────────────────────────────

class TestPipelineHealthScore:
    def _make_result(self, adj_pct: float, risk: DealRisk) -> ForecastDealResult:
        return ForecastDealResult(
            deal_id="x", deal_name="x", amount_eur=1000, stage="demo",
            segment="smb", close_date_days=30,
            base_win_probability_pct=35.0,
            adjusted_win_probability_pct=adj_pct,
            weighted_value_eur=1000 * adj_pct / 100,
            conservative_value_eur=700 * adj_pct / 100,
            optimistic_value_eur=1300 * adj_pct / 100,
            deal_risk=risk,
            quarter_label=QuarterLabel.CURRENT,
            risk_factors=[],
            upside_factors=[],
        )

    def test_empty_list_returns_zero(self):
        assert _pipeline_health_score([]) == 0.0

    def test_single_deal_no_high_risk(self):
        r = self._make_result(60.0, DealRisk.LOW)
        score = _pipeline_health_score([r])
        # avg_prob=60, high_risk_pct=0, score=max(0,min(100,60-0))=60
        assert score == pytest.approx(60.0, abs=0.2)

    def test_single_high_risk_deal(self):
        r = self._make_result(60.0, DealRisk.HIGH)
        score = _pipeline_health_score([r])
        # avg=60, high_risk_pct=100, score=60-100*0.3=60-30=30
        assert score == pytest.approx(30.0, abs=0.2)

    def test_all_high_risk_reduces_score(self):
        deals = [self._make_result(50.0, DealRisk.HIGH) for _ in range(4)]
        score = _pipeline_health_score(deals)
        # avg=50, high_risk_pct=100, score=50-30=20
        assert score == pytest.approx(20.0, abs=0.2)

    def test_score_clamped_to_max_100(self):
        # 97 avg prob, no high risk → min(100, 97) = 97
        r = self._make_result(97.0, DealRisk.NONE)
        assert _pipeline_health_score([r]) <= 100.0

    def test_score_clamped_to_min_0(self):
        # Very low prob + all high risk: could go negative
        deals = [self._make_result(5.0, DealRisk.HIGH) for _ in range(5)]
        assert _pipeline_health_score(deals) >= 0.0

    def test_mixed_risk_partial_penalty(self):
        low = self._make_result(70.0, DealRisk.LOW)
        high = self._make_result(70.0, DealRisk.HIGH)
        score = _pipeline_health_score([low, high])
        # avg=70, high_risk_pct=50, penalty=50*0.3=15, score=70-15=55
        assert score == pytest.approx(55.0, abs=0.2)

    def test_no_high_risk_score_equals_avg_prob(self):
        deals = [
            self._make_result(40.0, DealRisk.LOW),
            self._make_result(60.0, DealRisk.NONE),
        ]
        score = _pipeline_health_score(deals)
        # avg=50, high_risk_pct=0, score=50
        assert score == pytest.approx(50.0, abs=0.2)

    def test_return_type_float(self):
        r = self._make_result(50.0, DealRisk.LOW)
        assert isinstance(_pipeline_health_score([r]), float)


# ─── 9. ForecastDeal dataclass ────────────────────────────────────────────────

class TestForecastDeal:
    def test_creation_with_all_fields(self):
        d = make_deal()
        assert d.deal_id == "D1"
        assert d.amount_eur == 10_000.0
        assert d.stage == "proposal"

    def test_fields_preserved(self):
        d = ForecastDeal(
            deal_id="xyz", deal_name="Big Deal", amount_eur=50_000,
            stage="closing", close_date_days=10, segment="enterprise",
            days_in_stage=3, num_competitors=1, champion_strength=85.0,
            has_verbal_commit=True, has_budget_approved=True, is_renewal=False,
        )
        assert d.deal_id == "xyz"
        assert d.deal_name == "Big Deal"
        assert d.amount_eur == 50_000
        assert d.stage == "closing"
        assert d.close_date_days == 10
        assert d.segment == "enterprise"
        assert d.has_verbal_commit is True
        assert d.has_budget_approved is True
        assert d.is_renewal is False


# ─── 10. ForecastDealResult.to_dict ──────────────────────────────────────────

class TestForecastDealResultToDict:
    def _make_result(self) -> ForecastDealResult:
        return ForecastDealResult(
            deal_id="R1", deal_name="Result Deal", amount_eur=5000.0,
            stage="proposal", segment="smb", close_date_days=45,
            base_win_probability_pct=50.0, adjusted_win_probability_pct=55.0,
            weighted_value_eur=2750.0, conservative_value_eur=1925.0,
            optimistic_value_eur=3575.0, deal_risk=DealRisk.LOW,
            quarter_label=QuarterLabel.CURRENT, risk_factors=["risk1"],
            upside_factors=["up1"],
        )

    def test_to_dict_returns_dict(self):
        assert isinstance(self._make_result().to_dict(), dict)

    def test_deal_risk_is_string_value(self):
        d = self._make_result().to_dict()
        assert d["deal_risk"] == "low"

    def test_quarter_label_is_string_value(self):
        d = self._make_result().to_dict()
        assert d["quarter_label"] == "current_quarter"

    def test_all_expected_keys_present(self):
        d = self._make_result().to_dict()
        for key in ("deal_id", "deal_name", "amount_eur", "stage", "segment",
                    "close_date_days", "base_win_probability_pct",
                    "adjusted_win_probability_pct", "weighted_value_eur",
                    "conservative_value_eur", "optimistic_value_eur",
                    "deal_risk", "quarter_label", "risk_factors", "upside_factors"):
            assert key in d

    def test_risk_factors_preserved(self):
        d = self._make_result().to_dict()
        assert d["risk_factors"] == ["risk1"]

    def test_upside_factors_preserved(self):
        d = self._make_result().to_dict()
        assert d["upside_factors"] == ["up1"]

    def test_deal_risk_high_serializes_as_high(self):
        r = self._make_result()
        r.deal_risk = DealRisk.HIGH
        assert r.to_dict()["deal_risk"] == "high"

    def test_quarter_label_beyond_serializes(self):
        r = self._make_result()
        r.quarter_label = QuarterLabel.BEYOND
        assert r.to_dict()["quarter_label"] == "beyond"

    def test_numeric_values_preserved(self):
        d = self._make_result().to_dict()
        assert d["amount_eur"] == 5000.0
        assert d["weighted_value_eur"] == 2750.0


# ─── 11. RevenueForecast.to_dict ─────────────────────────────────────────────

class TestRevenueForecastToDict:
    def test_to_dict_returns_dict(self):
        _, f = engine_with_forecast()
        assert isinstance(f.to_dict(), dict)

    def test_deals_key_is_list_of_dicts(self):
        _, f = engine_with_forecast([make_deal(), make_deal(deal_id="D2")])
        d = f.to_dict()
        assert isinstance(d["deals"], list)
        assert all(isinstance(x, dict) for x in d["deals"])

    def test_deal_risk_in_nested_dict_is_string(self):
        _, f = engine_with_forecast()
        d = f.to_dict()
        assert isinstance(d["deals"][0]["deal_risk"], str)

    def test_quarter_label_in_nested_dict_is_string(self):
        _, f = engine_with_forecast()
        d = f.to_dict()
        assert isinstance(d["deals"][0]["quarter_label"], str)

    def test_top_level_keys_present(self):
        _, f = engine_with_forecast()
        d = f.to_dict()
        for key in ("total_pipeline_eur", "base_forecast_eur", "conservative_forecast_eur",
                    "optimistic_forecast_eur", "deal_count", "high_risk_count",
                    "pipeline_health_score", "segment_breakdown", "stage_breakdown"):
            assert key in d


# ─── 12. RevenueForecastEngine.forecast ──────────────────────────────────────

class TestRevenueForecastEngineForecast:
    def test_returns_revenue_forecast(self):
        e = RevenueForecastEngine()
        f = e.forecast([make_deal()])
        assert isinstance(f, RevenueForecast)

    def test_empty_deals_returns_zero_pipeline(self):
        e = RevenueForecastEngine()
        f = e.forecast([])
        assert f.total_pipeline_eur == 0.0

    def test_empty_deals_zero_forecasts(self):
        e = RevenueForecastEngine()
        f = e.forecast([])
        assert f.base_forecast_eur == 0.0
        assert f.conservative_forecast_eur == 0.0
        assert f.optimistic_forecast_eur == 0.0

    def test_empty_deals_zero_avg_prob(self):
        e = RevenueForecastEngine()
        f = e.forecast([])
        assert f.avg_win_probability_pct == 0.0

    def test_empty_deals_zero_deal_count(self):
        e = RevenueForecastEngine()
        f = e.forecast([])
        assert f.deal_count == 0

    def test_deal_count_matches_input(self):
        deals = [make_deal(deal_id=str(i)) for i in range(5)]
        _, f = engine_with_forecast(deals)
        assert f.deal_count == 5

    def test_total_pipeline_sum_of_amounts(self):
        deals = [make_deal(deal_id="1", amount_eur=10_000), make_deal(deal_id="2", amount_eur=20_000)]
        _, f = engine_with_forecast(deals)
        assert f.total_pipeline_eur == pytest.approx(30_000.0)

    def test_base_forecast_eur_weighted_sum(self):
        deal = make_deal(stage="proposal", amount_eur=10_000, champion_strength=60,
                         num_competitors=0, has_budget_approved=False,
                         has_verbal_commit=False, is_renewal=False,
                         close_date_days=30, days_in_stage=5)
        _, f = engine_with_forecast([deal])
        adj = _adjusted_win_probability(deal)
        assert f.base_forecast_eur == pytest.approx(10_000 * adj, rel=1e-3)

    def test_conservative_less_than_base(self):
        _, f = engine_with_forecast([make_deal(amount_eur=50_000)])
        assert f.conservative_forecast_eur <= f.base_forecast_eur

    def test_optimistic_greater_than_base(self):
        _, f = engine_with_forecast([make_deal(amount_eur=50_000)])
        assert f.optimistic_forecast_eur >= f.base_forecast_eur

    def test_deals_sorted_by_weighted_value_desc(self):
        deals = [
            make_deal(deal_id="small", amount_eur=1_000),
            make_deal(deal_id="large", amount_eur=100_000, stage="closing",
                      champion_strength=80),
            make_deal(deal_id="medium", amount_eur=10_000, stage="proposal"),
        ]
        _, f = engine_with_forecast(deals)
        wvs = [d.weighted_value_eur for d in f.deals]
        assert wvs == sorted(wvs, reverse=True)

    def test_current_quarter_pipeline_correct(self):
        current_deal = make_deal(deal_id="cur", close_date_days=30, amount_eur=10_000)
        beyond_deal = make_deal(deal_id="bey", close_date_days=200, amount_eur=10_000)
        _, f = engine_with_forecast([current_deal, beyond_deal])
        # Only current deal's weighted value should be in current_quarter_pipeline_eur
        adj_cur = _adjusted_win_probability(current_deal)
        assert f.current_quarter_pipeline_eur == pytest.approx(10_000 * adj_cur, rel=1e-3)

    def test_next_quarter_pipeline_correct(self):
        next_deal = make_deal(deal_id="nxt", close_date_days=120, amount_eur=15_000)
        current_deal = make_deal(deal_id="cur", close_date_days=30, amount_eur=10_000)
        _, f = engine_with_forecast([next_deal, current_deal])
        adj_nxt = _adjusted_win_probability(next_deal)
        assert f.next_quarter_pipeline_eur == pytest.approx(15_000 * adj_nxt, rel=1e-3)

    def test_beyond_pipeline_correct(self):
        beyond_deal = make_deal(deal_id="bey", close_date_days=200, amount_eur=20_000)
        _, f = engine_with_forecast([beyond_deal])
        adj = _adjusted_win_probability(beyond_deal)
        assert f.beyond_pipeline_eur == pytest.approx(20_000 * adj, rel=1e-3)

    def test_segment_breakdown_keys(self):
        deals = [
            make_deal(deal_id="1", segment="startup"),
            make_deal(deal_id="2", segment="enterprise"),
        ]
        _, f = engine_with_forecast(deals)
        assert "startup" in f.segment_breakdown
        assert "enterprise" in f.segment_breakdown

    def test_stage_breakdown_keys(self):
        deals = [
            make_deal(deal_id="1", stage="demo"),
            make_deal(deal_id="2", stage="closing"),
        ]
        _, f = engine_with_forecast(deals)
        assert "demo" in f.stage_breakdown
        assert "closing" in f.stage_breakdown

    def test_segment_breakdown_sums_weighted_value(self):
        d1 = make_deal(deal_id="1", segment="smb", amount_eur=10_000, stage="proposal",
                       champion_strength=60, num_competitors=0)
        _, f = engine_with_forecast([d1])
        adj = _adjusted_win_probability(d1)
        assert f.segment_breakdown["smb"] == pytest.approx(10_000 * adj, rel=1e-3)

    def test_stage_breakdown_sums_weighted_value(self):
        d1 = make_deal(deal_id="1", stage="demo", amount_eur=10_000, champion_strength=60,
                       num_competitors=0, close_date_days=30, days_in_stage=5)
        _, f = engine_with_forecast([d1])
        adj = _adjusted_win_probability(d1)
        assert f.stage_breakdown["demo"] == pytest.approx(10_000 * adj, rel=1e-3)

    def test_high_risk_count_correct(self):
        # Very low probability deal → HIGH risk
        low_prob_deal = make_deal(stage="prospecting", champion_strength=10, num_competitors=5,
                                  close_date_days=-30, days_in_stage=100, amount_eur=5000)
        good_deal = make_deal(deal_id="G", stage="closing", champion_strength=90,
                              has_budget_approved=True, has_verbal_commit=True)
        _, f = engine_with_forecast([low_prob_deal, good_deal])
        assert f.high_risk_count >= 1

    def test_avg_win_probability_pct_is_average(self):
        deals = [make_deal(deal_id=str(i)) for i in range(3)]
        _, f = engine_with_forecast(deals)
        adj_probs = [_adjusted_win_probability(d) * 100 for d in deals]
        expected_avg = sum(adj_probs) / len(adj_probs)
        assert f.avg_win_probability_pct == pytest.approx(expected_avg, abs=0.2)

    def test_pipeline_health_score_in_range(self):
        _, f = engine_with_forecast([make_deal()])
        assert 0.0 <= f.pipeline_health_score <= 100.0

    def test_deal_result_base_win_probability_pct(self):
        deal = make_deal(stage="demo")
        _, f = engine_with_forecast([deal])
        assert f.deals[0].base_win_probability_pct == pytest.approx(35.0)

    def test_deal_result_adjusted_win_probability_pct(self):
        deal = make_deal(stage="demo", champion_strength=60, num_competitors=0,
                         has_budget_approved=False, has_verbal_commit=False,
                         is_renewal=False, close_date_days=30, days_in_stage=5)
        _, f = engine_with_forecast([deal])
        assert f.deals[0].adjusted_win_probability_pct == pytest.approx(35.0)

    def test_deal_result_fields_propagated(self):
        deal = make_deal(deal_id="ABC", deal_name="My Deal", amount_eur=7500.0,
                         stage="closing", segment="enterprise", close_date_days=15)
        _, f = engine_with_forecast([deal])
        r = f.deals[0]
        assert r.deal_id == "ABC"
        assert r.deal_name == "My Deal"
        assert r.amount_eur == 7500.0
        assert r.stage == "closing"
        assert r.segment == "enterprise"
        assert r.close_date_days == 15

    def test_deal_weighted_value_eur_computed(self):
        deal = make_deal(amount_eur=10_000, stage="proposal", champion_strength=60,
                         num_competitors=0, has_budget_approved=False, has_verbal_commit=False,
                         is_renewal=False, close_date_days=30, days_in_stage=5)
        _, f = engine_with_forecast([deal])
        adj = _adjusted_win_probability(deal)
        assert f.deals[0].weighted_value_eur == pytest.approx(10_000 * adj, rel=1e-3)

    def test_sets_last_forecast(self):
        e, f = engine_with_forecast()
        assert e.get_last() is f

    def test_forecast_replaces_last(self):
        e = RevenueForecastEngine()
        f1 = e.forecast([make_deal(deal_id="D1")])
        f2 = e.forecast([make_deal(deal_id="D2")])
        assert e.get_last() is f2

    def test_multiple_deals_same_segment_breakdown_aggregated(self):
        d1 = make_deal(deal_id="1", segment="smb", amount_eur=10_000, stage="proposal",
                       champion_strength=60, num_competitors=0, has_budget_approved=False,
                       has_verbal_commit=False, is_renewal=False, close_date_days=30, days_in_stage=5)
        d2 = make_deal(deal_id="2", segment="smb", amount_eur=10_000, stage="proposal",
                       champion_strength=60, num_competitors=0, has_budget_approved=False,
                       has_verbal_commit=False, is_renewal=False, close_date_days=30, days_in_stage=5)
        _, f = engine_with_forecast([d1, d2])
        adj = _adjusted_win_probability(d1)
        assert f.segment_breakdown["smb"] == pytest.approx(2 * 10_000 * adj, rel=1e-3)

    def test_quarter_labels_assigned_correctly(self):
        current = make_deal(deal_id="c", close_date_days=30)
        nxt = make_deal(deal_id="n", close_date_days=120)
        bey = make_deal(deal_id="b", close_date_days=200)
        _, f = engine_with_forecast([current, nxt, bey])
        labels = {d.deal_id: d.quarter_label for d in f.deals}
        assert labels["c"] == QuarterLabel.CURRENT
        assert labels["n"] == QuarterLabel.NEXT
        assert labels["b"] == QuarterLabel.BEYOND


# ─── 13. RevenueForecastEngine query methods ──────────────────────────────────

class TestRevenueForecastEngineQueryMethods:
    def test_get_last_none_before_forecast(self):
        e = RevenueForecastEngine()
        assert e.get_last() is None

    def test_get_last_returns_forecast_after_call(self):
        e, f = engine_with_forecast()
        assert e.get_last() is f

    def test_by_risk_returns_empty_before_forecast(self):
        e = RevenueForecastEngine()
        assert e.by_risk(DealRisk.HIGH) == []

    def test_by_risk_filters_correctly(self):
        # Create a deal that will be HIGH risk (low adj prob)
        high_risk = make_deal(deal_id="hr", stage="prospecting", champion_strength=10,
                              num_competitors=5, close_date_days=-30, days_in_stage=100)
        low_risk = make_deal(deal_id="lr", stage="closing", champion_strength=90,
                             has_budget_approved=True, has_verbal_commit=True)
        e = RevenueForecastEngine()
        e.forecast([high_risk, low_risk])
        high_risk_deals = e.by_risk(DealRisk.HIGH)
        assert all(d.deal_risk == DealRisk.HIGH for d in high_risk_deals)

    def test_by_risk_medium_returns_medium_deals(self):
        # proposal adj ~0.30 → MEDIUM
        medium_deal = make_deal(deal_id="md", stage="proposal", champion_strength=30,
                                num_competitors=0, close_date_days=30, days_in_stage=5,
                                has_budget_approved=False, has_verbal_commit=False)
        e = RevenueForecastEngine()
        e.forecast([medium_deal])
        adj = _adjusted_win_probability(medium_deal)
        risk = _deal_risk(medium_deal, adj)
        result = e.by_risk(risk)
        assert len(result) >= 1

    def test_by_quarter_returns_empty_before_forecast(self):
        e = RevenueForecastEngine()
        assert e.by_quarter(QuarterLabel.CURRENT) == []

    def test_by_quarter_current_only_returns_current(self):
        current = make_deal(deal_id="c", close_date_days=30)
        beyond = make_deal(deal_id="b", close_date_days=200)
        e = RevenueForecastEngine()
        e.forecast([current, beyond])
        results = e.by_quarter(QuarterLabel.CURRENT)
        assert all(d.quarter_label == QuarterLabel.CURRENT for d in results)

    def test_by_quarter_next_filters_next(self):
        nxt = make_deal(deal_id="n", close_date_days=120)
        cur = make_deal(deal_id="c", close_date_days=30)
        e = RevenueForecastEngine()
        e.forecast([nxt, cur])
        results = e.by_quarter(QuarterLabel.NEXT)
        assert all(d.quarter_label == QuarterLabel.NEXT for d in results)

    def test_high_risk_deals_delegates_to_by_risk(self):
        high_risk = make_deal(stage="prospecting", champion_strength=5, num_competitors=5,
                              close_date_days=-50, days_in_stage=100)
        e = RevenueForecastEngine()
        e.forecast([high_risk])
        assert e.high_risk_deals() == e.by_risk(DealRisk.HIGH)

    def test_current_quarter_deals_delegates_to_by_quarter(self):
        e = RevenueForecastEngine()
        e.forecast([make_deal(close_date_days=30)])
        assert e.current_quarter_deals() == e.by_quarter(QuarterLabel.CURRENT)

    def test_top_n_returns_empty_before_forecast(self):
        e = RevenueForecastEngine()
        assert e.top_n(5) == []

    def test_top_n_returns_n_deals(self):
        deals = [make_deal(deal_id=str(i)) for i in range(10)]
        e = RevenueForecastEngine()
        e.forecast(deals)
        assert len(e.top_n(5)) == 5

    def test_top_n_returns_all_if_fewer_than_n(self):
        deals = [make_deal(deal_id=str(i)) for i in range(3)]
        e = RevenueForecastEngine()
        e.forecast(deals)
        assert len(e.top_n(10)) == 3

    def test_top_n_default_is_10(self):
        deals = [make_deal(deal_id=str(i)) for i in range(15)]
        e = RevenueForecastEngine()
        e.forecast(deals)
        assert len(e.top_n()) == 10

    def test_top_n_sorted_by_weighted_value(self):
        deals = [make_deal(deal_id=str(i), amount_eur=float((i + 1) * 10_000)) for i in range(5)]
        e = RevenueForecastEngine()
        e.forecast(deals)
        top = e.top_n(3)
        wvs = [d.weighted_value_eur for d in top]
        assert wvs == sorted(wvs, reverse=True)

    def test_scenario_summary_empty_before_forecast(self):
        e = RevenueForecastEngine()
        assert e.scenario_summary() == {}

    def test_scenario_summary_keys(self):
        e, _ = engine_with_forecast()
        s = e.scenario_summary()
        assert set(s.keys()) == {"conservative", "base", "optimistic", "pipeline", "conversion_rate_pct"}

    def test_scenario_summary_conservative_matches_forecast(self):
        e, f = engine_with_forecast()
        assert e.scenario_summary()["conservative"] == f.conservative_forecast_eur

    def test_scenario_summary_base_matches_forecast(self):
        e, f = engine_with_forecast()
        assert e.scenario_summary()["base"] == f.base_forecast_eur

    def test_scenario_summary_optimistic_matches_forecast(self):
        e, f = engine_with_forecast()
        assert e.scenario_summary()["optimistic"] == f.optimistic_forecast_eur

    def test_scenario_summary_pipeline_matches_forecast(self):
        e, f = engine_with_forecast()
        assert e.scenario_summary()["pipeline"] == f.total_pipeline_eur

    def test_scenario_summary_conversion_rate_pct(self):
        e, f = engine_with_forecast()
        expected = round(f.base_forecast_eur / f.total_pipeline_eur * 100, 1)
        assert e.scenario_summary()["conversion_rate_pct"] == pytest.approx(expected)

    def test_scenario_summary_zero_pipeline_zero_conversion(self):
        e = RevenueForecastEngine()
        e.forecast([])
        # No last forecast (empty deals still sets it), check conversion rate
        s = e.scenario_summary()
        assert s["conversion_rate_pct"] == 0.0

    def test_reset_clears_last_forecast(self):
        e, _ = engine_with_forecast()
        e.reset()
        assert e.get_last() is None

    def test_reset_makes_by_risk_return_empty(self):
        e, _ = engine_with_forecast()
        e.reset()
        assert e.by_risk(DealRisk.HIGH) == []

    def test_reset_makes_scenario_summary_empty(self):
        e, _ = engine_with_forecast()
        e.reset()
        assert e.scenario_summary() == {}

    def test_reset_makes_top_n_empty(self):
        e, _ = engine_with_forecast()
        e.reset()
        assert e.top_n() == []

    def test_engine_stateless_before_forecast(self):
        e = RevenueForecastEngine()
        assert e.high_risk_deals() == []
        assert e.current_quarter_deals() == []
        assert e.by_quarter(QuarterLabel.BEYOND) == []


# ─── 14. Integration / end-to-end tests ──────────────────────────────────────

class TestIntegration:
    def _make_pipeline(self) -> list[ForecastDeal]:
        return [
            ForecastDeal(
                deal_id="ENT1", deal_name="Enterprise Alpha", amount_eur=200_000,
                stage="negotiation", close_date_days=20, segment="enterprise",
                days_in_stage=10, num_competitors=1, champion_strength=85,
                has_verbal_commit=True, has_budget_approved=True, is_renewal=False,
            ),
            ForecastDeal(
                deal_id="SMB1", deal_name="SMB Beta", amount_eur=15_000,
                stage="proposal", close_date_days=45, segment="smb",
                days_in_stage=12, num_competitors=2, champion_strength=55,
                has_verbal_commit=False, has_budget_approved=False, is_renewal=False,
            ),
            ForecastDeal(
                deal_id="RENEW1", deal_name="Renewal Client", amount_eur=50_000,
                stage="closing", close_date_days=-5, segment="mid_market",
                days_in_stage=5, num_competitors=0, champion_strength=70,
                has_verbal_commit=False, has_budget_approved=True, is_renewal=True,
            ),
            ForecastDeal(
                deal_id="STALE1", deal_name="Stale Prospect", amount_eur=8_000,
                stage="prospecting", close_date_days=120, segment="startup",
                days_in_stage=50, num_competitors=3, champion_strength=25,
                has_verbal_commit=False, has_budget_approved=False, is_renewal=False,
            ),
        ]

    def test_full_pipeline_forecast(self):
        e = RevenueForecastEngine()
        f = e.forecast(self._make_pipeline())
        assert isinstance(f, RevenueForecast)
        assert f.deal_count == 4

    def test_total_pipeline_correct(self):
        e = RevenueForecastEngine()
        f = e.forecast(self._make_pipeline())
        assert f.total_pipeline_eur == pytest.approx(273_000.0)

    def test_enterprise_deal_highest_weighted_value(self):
        e = RevenueForecastEngine()
        f = e.forecast(self._make_pipeline())
        assert f.deals[0].deal_id == "ENT1"

    def test_overdue_renewal_risk_assessed(self):
        e = RevenueForecastEngine()
        f = e.forecast(self._make_pipeline())
        renew = next(d for d in f.deals if d.deal_id == "RENEW1")
        # Overdue (close_date_days=-5), adj may be >= 0.50 due to renewall+budget
        assert renew.quarter_label == QuarterLabel.CURRENT

    def test_stale_deal_has_risk_factors(self):
        e = RevenueForecastEngine()
        f = e.forecast(self._make_pipeline())
        stale = next(d for d in f.deals if d.deal_id == "STALE1")
        assert len(stale.risk_factors) > 0

    def test_enterprise_has_upside_factors(self):
        e = RevenueForecastEngine()
        f = e.forecast(self._make_pipeline())
        ent = next(d for d in f.deals if d.deal_id == "ENT1")
        assert len(ent.upside_factors) > 0

    def test_segment_breakdown_has_all_segments(self):
        e = RevenueForecastEngine()
        f = e.forecast(self._make_pipeline())
        for seg in ("enterprise", "smb", "mid_market", "startup"):
            assert seg in f.segment_breakdown

    def test_stage_breakdown_has_all_stages_used(self):
        e = RevenueForecastEngine()
        f = e.forecast(self._make_pipeline())
        for stage in ("negotiation", "proposal", "closing", "prospecting"):
            assert stage in f.stage_breakdown

    def test_scenario_ordering_conservative_base_optimistic(self):
        e = RevenueForecastEngine()
        f = e.forecast(self._make_pipeline())
        assert f.conservative_forecast_eur <= f.base_forecast_eur <= f.optimistic_forecast_eur

    def test_to_dict_is_serializable(self):
        import json
        e = RevenueForecastEngine()
        f = e.forecast(self._make_pipeline())
        # Should not raise
        serialized = json.dumps(f.to_dict())
        parsed = json.loads(serialized)
        assert parsed["deal_count"] == 4

    def test_high_risk_deals_method_consistent(self):
        e = RevenueForecastEngine()
        f = e.forecast(self._make_pipeline())
        high_from_method = e.high_risk_deals()
        high_from_forecast = [d for d in f.deals if d.deal_risk == DealRisk.HIGH]
        assert set(d.deal_id for d in high_from_method) == set(d.deal_id for d in high_from_forecast)

    def test_current_quarter_deals_consistent(self):
        e = RevenueForecastEngine()
        f = e.forecast(self._make_pipeline())
        cq_method = e.current_quarter_deals()
        cq_forecast = [d for d in f.deals if d.quarter_label == QuarterLabel.CURRENT]
        assert set(d.deal_id for d in cq_method) == set(d.deal_id for d in cq_forecast)

    def test_multiple_forecast_calls_independent(self):
        e = RevenueForecastEngine()
        f1 = e.forecast([make_deal(deal_id="A", amount_eur=5_000)])
        f2 = e.forecast([make_deal(deal_id="B", amount_eur=10_000)])
        assert f1.total_pipeline_eur == pytest.approx(5_000)
        assert f2.total_pipeline_eur == pytest.approx(10_000)
        assert e.get_last() is f2

    def test_single_deal_quarter_pipeline_sums_correctly(self):
        deal = make_deal(close_date_days=50, amount_eur=20_000, stage="proposal",
                         champion_strength=60, num_competitors=0, has_budget_approved=False,
                         has_verbal_commit=False, is_renewal=False, days_in_stage=5)
        e = RevenueForecastEngine()
        f = e.forecast([deal])
        adj = _adjusted_win_probability(deal)
        assert f.current_quarter_pipeline_eur == pytest.approx(20_000 * adj, rel=1e-3)
        assert f.next_quarter_pipeline_eur == pytest.approx(0.0)
        assert f.beyond_pipeline_eur == pytest.approx(0.0)

    def test_top_n_integration(self):
        e = RevenueForecastEngine()
        e.forecast(self._make_pipeline())
        top2 = e.top_n(2)
        assert len(top2) == 2
        assert top2[0].weighted_value_eur >= top2[1].weighted_value_eur
