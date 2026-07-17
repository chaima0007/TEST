"""
Comprehensive pytest tests for swarm/intelligence/contract_renewal.py

Covers all enums, dataclasses, private scoring helpers, business rule edge cases,
and ContractRenewalEngine public API methods.
"""

from __future__ import annotations

import pytest

from swarm.intelligence.contract_renewal import (
    RenewalRisk,
    RenewalAction,
    UpliftPotential,
    RenewalInput,
    RenewalResult,
    ContractRenewalEngine,
    _renewal_score,
    _uplift_score,
    _uplift_potential,
    _renewal_risk,
    _recommended_uplift,
    _renewal_action,
    _build_churn_signals,
    _build_retention_levers,
    _build_negotiation_tactics,
    _build_timeline_steps,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def make_input(**overrides) -> RenewalInput:
    """Return a baseline RenewalInput with sensible defaults, easy to override."""
    defaults = dict(
        contract_id="C001",
        account_name="Acme Corp",
        segment="enterprise",
        arr_eur=100_000.0,
        days_to_renewal=60,
        health_score=70.0,
        nps_score=30.0,
        product_adoption_score=60.0,
        support_escalations=0,
        executive_engaged=True,
        champion_strength=70.0,
        qbr_completed_last_90d=True,
        stakeholder_count=3,
        current_discount_pct=10.0,
        price_increase_proposed=5.0,
        competitive_bids_received=0,
        budget_confirmed=True,
        multi_year_interest=False,
        seat_utilization_pct=75.0,
        feature_adoption_pct=60.0,
        expansion_history=False,
        new_use_cases=0,
    )
    defaults.update(overrides)
    return RenewalInput(**defaults)


@pytest.fixture
def baseline_input() -> RenewalInput:
    return make_input()


@pytest.fixture
def red_input() -> RenewalInput:
    """Input that should produce a RED renewal risk."""
    return make_input(
        health_score=0.0,
        nps_score=-100.0,
        executive_engaged=False,
        champion_strength=0.0,
        qbr_completed_last_90d=False,
        support_escalations=3,
        competitive_bids_received=2,
        price_increase_proposed=20.0,
        budget_confirmed=False,
        multi_year_interest=False,
        stakeholder_count=0,
    )


@pytest.fixture
def green_input() -> RenewalInput:
    """Input that should produce a GREEN renewal risk."""
    return make_input(
        health_score=100.0,
        nps_score=100.0,
        executive_engaged=True,
        champion_strength=90.0,
        qbr_completed_last_90d=True,
        support_escalations=0,
        competitive_bids_received=0,
        price_increase_proposed=0.0,
        budget_confirmed=True,
        multi_year_interest=True,
        stakeholder_count=5,
    )


@pytest.fixture
def engine() -> ContractRenewalEngine:
    return ContractRenewalEngine()


# ---------------------------------------------------------------------------
# 1. TestRenewalRiskEnum
# ---------------------------------------------------------------------------

class TestRenewalRiskEnum:
    def test_green_value(self):
        assert RenewalRisk.GREEN.value == "green"

    def test_yellow_value(self):
        assert RenewalRisk.YELLOW.value == "yellow"

    def test_orange_value(self):
        assert RenewalRisk.ORANGE.value == "orange"

    def test_red_value(self):
        assert RenewalRisk.RED.value == "red"

    def test_is_str_enum(self):
        assert isinstance(RenewalRisk.GREEN, str)

    def test_members_count(self):
        assert len(RenewalRisk) == 4

    def test_green_str_comparison(self):
        assert RenewalRisk.GREEN == "green"

    def test_red_str_comparison(self):
        assert RenewalRisk.RED == "red"

    def test_enum_identity(self):
        assert RenewalRisk("green") is RenewalRisk.GREEN

    def test_all_values_unique(self):
        vals = [r.value for r in RenewalRisk]
        assert len(vals) == len(set(vals))


# ---------------------------------------------------------------------------
# 2. TestRenewalActionEnum
# ---------------------------------------------------------------------------

class TestRenewalActionEnum:
    def test_close_renewal_value(self):
        assert RenewalAction.CLOSE_RENEWAL.value == "close_renewal"

    def test_accelerate_value(self):
        assert RenewalAction.ACCELERATE.value == "accelerate"

    def test_intervene_value(self):
        assert RenewalAction.INTERVENE.value == "intervene"

    def test_save_value(self):
        assert RenewalAction.SAVE.value == "save"

    def test_early_renew_value(self):
        assert RenewalAction.EARLY_RENEW.value == "early_renew"

    def test_is_str_enum(self):
        assert isinstance(RenewalAction.SAVE, str)

    def test_members_count(self):
        assert len(RenewalAction) == 5

    def test_all_values_unique(self):
        vals = [a.value for a in RenewalAction]
        assert len(vals) == len(set(vals))

    def test_str_comparison(self):
        assert RenewalAction.SAVE == "save"

    def test_by_value(self):
        assert RenewalAction("intervene") is RenewalAction.INTERVENE


# ---------------------------------------------------------------------------
# 3. TestUpliftPotentialEnum
# ---------------------------------------------------------------------------

class TestUpliftPotentialEnum:
    def test_high_value(self):
        assert UpliftPotential.HIGH.value == "high"

    def test_medium_value(self):
        assert UpliftPotential.MEDIUM.value == "medium"

    def test_low_value(self):
        assert UpliftPotential.LOW.value == "low"

    def test_is_str_enum(self):
        assert isinstance(UpliftPotential.HIGH, str)

    def test_members_count(self):
        assert len(UpliftPotential) == 3

    def test_all_values_unique(self):
        vals = [u.value for u in UpliftPotential]
        assert len(vals) == len(set(vals))

    def test_str_comparison(self):
        assert UpliftPotential.LOW == "low"

    def test_by_value(self):
        assert UpliftPotential("high") is UpliftPotential.HIGH


# ---------------------------------------------------------------------------
# 4. TestRenewalInputDataclass
# ---------------------------------------------------------------------------

class TestRenewalInputDataclass:
    def test_instantiation(self, baseline_input):
        assert baseline_input.contract_id == "C001"

    def test_all_fields_accessible(self, baseline_input):
        assert hasattr(baseline_input, "arr_eur")
        assert hasattr(baseline_input, "days_to_renewal")
        assert hasattr(baseline_input, "health_score")
        assert hasattr(baseline_input, "nps_score")
        assert hasattr(baseline_input, "product_adoption_score")
        assert hasattr(baseline_input, "support_escalations")
        assert hasattr(baseline_input, "executive_engaged")
        assert hasattr(baseline_input, "champion_strength")
        assert hasattr(baseline_input, "qbr_completed_last_90d")
        assert hasattr(baseline_input, "stakeholder_count")
        assert hasattr(baseline_input, "current_discount_pct")
        assert hasattr(baseline_input, "price_increase_proposed")
        assert hasattr(baseline_input, "competitive_bids_received")
        assert hasattr(baseline_input, "budget_confirmed")
        assert hasattr(baseline_input, "multi_year_interest")
        assert hasattr(baseline_input, "seat_utilization_pct")
        assert hasattr(baseline_input, "feature_adoption_pct")
        assert hasattr(baseline_input, "expansion_history")
        assert hasattr(baseline_input, "new_use_cases")

    def test_bool_fields(self, baseline_input):
        assert isinstance(baseline_input.executive_engaged, bool)
        assert isinstance(baseline_input.budget_confirmed, bool)

    def test_float_fields(self, baseline_input):
        assert isinstance(baseline_input.arr_eur, (int, float))
        assert isinstance(baseline_input.health_score, (int, float))

    def test_int_fields(self, baseline_input):
        assert isinstance(baseline_input.days_to_renewal, int)
        assert isinstance(baseline_input.support_escalations, int)

    def test_mutable(self, baseline_input):
        baseline_input.arr_eur = 999.0
        assert baseline_input.arr_eur == 999.0

    def test_segment_string(self, baseline_input):
        assert isinstance(baseline_input.segment, str)


# ---------------------------------------------------------------------------
# 5. TestRenewalResultToDict
# ---------------------------------------------------------------------------

class TestRenewalResultToDict:
    def _make_result(self) -> RenewalResult:
        return RenewalResult(
            contract_id="C001",
            account_name="Acme",
            segment="enterprise",
            arr_eur=100_000.0,
            days_to_renewal=60,
            renewal_risk=RenewalRisk.GREEN,
            renewal_action=RenewalAction.CLOSE_RENEWAL,
            uplift_potential=UpliftPotential.HIGH,
            renewal_score=80.0,
            uplift_score=72.0,
            recommended_uplift_pct=10.0,
            churn_signals=[],
            retention_levers=[],
            negotiation_tactics=[],
            timeline_steps=[],
        )

    def test_returns_dict(self):
        r = self._make_result()
        assert isinstance(r.to_dict(), dict)

    def test_risk_serialized_as_string(self):
        d = self._make_result().to_dict()
        assert d["renewal_risk"] == "green"
        assert isinstance(d["renewal_risk"], str)

    def test_action_serialized_as_string(self):
        d = self._make_result().to_dict()
        assert d["renewal_action"] == "close_renewal"
        assert isinstance(d["renewal_action"], str)

    def test_uplift_serialized_as_string(self):
        d = self._make_result().to_dict()
        assert d["uplift_potential"] == "high"
        assert isinstance(d["uplift_potential"], str)

    def test_numeric_fields_present(self):
        d = self._make_result().to_dict()
        assert d["arr_eur"] == 100_000.0
        assert d["renewal_score"] == 80.0
        assert d["uplift_score"] == 72.0
        assert d["recommended_uplift_pct"] == 10.0

    def test_list_fields_present(self):
        d = self._make_result().to_dict()
        assert isinstance(d["churn_signals"], list)
        assert isinstance(d["retention_levers"], list)
        assert isinstance(d["negotiation_tactics"], list)
        assert isinstance(d["timeline_steps"], list)

    def test_all_expected_keys_present(self):
        d = self._make_result().to_dict()
        expected_keys = {
            "contract_id", "account_name", "segment", "arr_eur", "days_to_renewal",
            "renewal_risk", "renewal_action", "uplift_potential", "renewal_score",
            "uplift_score", "recommended_uplift_pct", "churn_signals",
            "retention_levers", "negotiation_tactics", "timeline_steps",
        }
        assert expected_keys.issubset(d.keys())

    def test_red_risk_dict(self):
        r = self._make_result()
        r.renewal_risk = RenewalRisk.RED
        assert r.to_dict()["renewal_risk"] == "red"


# ---------------------------------------------------------------------------
# 6. TestRenewalScoreHealthComponent
# ---------------------------------------------------------------------------

class TestRenewalScoreHealthComponent:
    """health_score * 0.30 contributes 0..30 to renewal_score."""

    def _isolated_health_score(self, health: float) -> float:
        """Score with everything else zeroed out."""
        inp = make_input(
            health_score=health,
            nps_score=-100.0,          # NPS min → 0 pts
            executive_engaged=False,
            champion_strength=0.0,
            qbr_completed_last_90d=False,
            support_escalations=0,
            competitive_bids_received=0,
            price_increase_proposed=0.0,
            budget_confirmed=False,
            multi_year_interest=False,
            stakeholder_count=0,
        )
        return _renewal_score(inp)

    def test_health_zero(self):
        assert self._isolated_health_score(0.0) == 0.0

    def test_health_100(self):
        assert self._isolated_health_score(100.0) == pytest.approx(30.0)

    def test_health_50(self):
        assert self._isolated_health_score(50.0) == pytest.approx(15.0)

    def test_health_70(self):
        assert self._isolated_health_score(70.0) == pytest.approx(21.0)

    def test_health_30(self):
        assert self._isolated_health_score(30.0) == pytest.approx(9.0)

    def test_health_contribution_proportional(self):
        s40 = self._isolated_health_score(40.0)
        s80 = self._isolated_health_score(80.0)
        assert pytest.approx(s80, rel=1e-3) == s40 * 2


# ---------------------------------------------------------------------------
# 7. TestRenewalScoreNPSNormalisation
# ---------------------------------------------------------------------------

class TestRenewalScoreNPSNormalisation:
    """NPS normalised -100..+100 → 0..20 pts."""

    def _nps_contribution(self, nps: float) -> float:
        """Extract NPS contribution only."""
        inp_zero_base = make_input(
            health_score=0.0,
            nps_score=nps,
            executive_engaged=False,
            champion_strength=0.0,
            qbr_completed_last_90d=False,
            support_escalations=0,
            competitive_bids_received=0,
            price_increase_proposed=0.0,
            budget_confirmed=False,
            multi_year_interest=False,
            stakeholder_count=0,
        )
        return _renewal_score(inp_zero_base)

    def test_nps_minus_100_gives_zero(self):
        assert self._nps_contribution(-100.0) == 0.0

    def test_nps_plus_100_gives_20(self):
        assert self._nps_contribution(100.0) == pytest.approx(20.0)

    def test_nps_zero_gives_10(self):
        assert self._nps_contribution(0.0) == pytest.approx(10.0)

    def test_nps_50_gives_15(self):
        assert self._nps_contribution(50.0) == pytest.approx(15.0)

    def test_nps_minus_50_gives_5(self):
        assert self._nps_contribution(-50.0) == pytest.approx(5.0)

    def test_nps_clamped_below_zero(self):
        # Even if below -100 NPS is somehow provided, score can't go negative from NPS
        inp = make_input(
            health_score=0.0,
            nps_score=-200.0,
            executive_engaged=False,
            champion_strength=0.0,
            qbr_completed_last_90d=False,
            support_escalations=0,
            competitive_bids_received=0,
            price_increase_proposed=0.0,
            budget_confirmed=False,
            multi_year_interest=False,
            stakeholder_count=0,
        )
        assert _renewal_score(inp) >= 0.0

    def test_nps_clamped_above_20(self):
        inp = make_input(
            health_score=0.0,
            nps_score=200.0,
            executive_engaged=False,
            champion_strength=0.0,
            qbr_completed_last_90d=False,
            support_escalations=0,
            competitive_bids_received=0,
            price_increase_proposed=0.0,
            budget_confirmed=False,
            multi_year_interest=False,
            stakeholder_count=0,
        )
        # NPS contribution can't exceed 20
        assert _renewal_score(inp) <= 20.0


# ---------------------------------------------------------------------------
# 8. TestRenewalScoreRelationship (exec+10, champion thresholds, qbr+5)
# ---------------------------------------------------------------------------

class TestRenewalScoreRelationship:
    """Relationship signals contribute to renewal score."""

    _REL_BASE = dict(
        health_score=0.0,
        nps_score=-100.0,
        executive_engaged=False,
        champion_strength=0.0,
        qbr_completed_last_90d=False,
        support_escalations=0,
        competitive_bids_received=0,
        price_increase_proposed=0.0,
        budget_confirmed=False,
        multi_year_interest=False,
        stakeholder_count=0,
    )

    def _base_no_relationship(self, **extra) -> float:
        return _renewal_score(make_input(**{**self._REL_BASE, **extra}))

    def test_executive_engaged_adds_10(self):
        base = self._base_no_relationship()
        with_exec = self._base_no_relationship(executive_engaged=True)
        assert with_exec - base == pytest.approx(10.0)

    def test_champion_strength_70_adds_10(self):
        base = self._base_no_relationship()
        with_champ = self._base_no_relationship(champion_strength=70.0)
        assert with_champ - base == pytest.approx(10.0)

    def test_champion_strength_100_adds_10(self):
        base = self._base_no_relationship()
        with_champ = self._base_no_relationship(champion_strength=100.0)
        assert with_champ - base == pytest.approx(10.0)

    def test_champion_strength_69_adds_5(self):
        base = self._base_no_relationship()
        with_champ = self._base_no_relationship(champion_strength=69.0)
        assert with_champ - base == pytest.approx(5.0)

    def test_champion_strength_40_adds_5(self):
        base = self._base_no_relationship()
        with_champ = self._base_no_relationship(champion_strength=40.0)
        assert with_champ - base == pytest.approx(5.0)

    def test_champion_strength_39_adds_nothing(self):
        base = self._base_no_relationship()
        with_champ = self._base_no_relationship(champion_strength=39.0)
        assert with_champ == base

    def test_champion_strength_0_adds_nothing(self):
        base = self._base_no_relationship()
        with_champ = self._base_no_relationship(champion_strength=0.0)
        assert with_champ == base

    def test_qbr_adds_5(self):
        base = self._base_no_relationship()
        with_qbr = self._base_no_relationship(qbr_completed_last_90d=True)
        assert with_qbr - base == pytest.approx(5.0)

    def test_all_relationship_max_25(self):
        # exec(10) + champion>=70(10) + qbr(5) = 25
        score = self._base_no_relationship(
            executive_engaged=True,
            champion_strength=70.0,
            qbr_completed_last_90d=True,
        )
        assert score == pytest.approx(25.0)


# ---------------------------------------------------------------------------
# 9. TestRenewalScoreDeductions
# ---------------------------------------------------------------------------

class TestRenewalScoreDeductions:
    """Risk deductions: escalations, competitor bids, price increase."""

    _DED_BASE = dict(
        health_score=50.0,
        nps_score=0.0,
        executive_engaged=True,
        champion_strength=70.0,
        qbr_completed_last_90d=True,
        budget_confirmed=True,
        multi_year_interest=False,
        stakeholder_count=0,
        support_escalations=0,
        competitive_bids_received=0,
        price_increase_proposed=0.0,
    )

    def _base_good(self, **extra) -> float:
        """Good baseline score without deductions."""
        return _renewal_score(make_input(**{**self._DED_BASE, **extra}))

    def _base_score(self):
        return self._base_good()

    def test_no_deductions_baseline(self):
        # health=50→15, nps=0→10, exec→10, champ70→10, qbr→5, budget→8 = 58
        score = self._base_good()
        assert score == pytest.approx(58.0)

    def test_escalations_3_deducts_15(self):
        score = self._base_good(support_escalations=3)
        assert score == pytest.approx(self._base_score() - 15.0)

    def test_escalations_5_deducts_15(self):
        score = self._base_good(support_escalations=5)
        assert score == pytest.approx(self._base_score() - 15.0)

    def test_escalations_1_deducts_7(self):
        score = self._base_good(support_escalations=1)
        assert score == pytest.approx(self._base_score() - 7.0)

    def test_escalations_2_deducts_7(self):
        score = self._base_good(support_escalations=2)
        assert score == pytest.approx(self._base_score() - 7.0)

    def test_escalations_0_no_deduction(self):
        score = self._base_good(support_escalations=0)
        assert score == pytest.approx(self._base_score())

    def test_competitor_bids_2_deducts_10(self):
        score = self._base_good(competitive_bids_received=2)
        assert score == pytest.approx(self._base_score() - 10.0)

    def test_competitor_bids_5_deducts_10(self):
        score = self._base_good(competitive_bids_received=5)
        assert score == pytest.approx(self._base_score() - 10.0)

    def test_competitor_bids_1_deducts_5(self):
        score = self._base_good(competitive_bids_received=1)
        assert score == pytest.approx(self._base_score() - 5.0)

    def test_competitor_bids_0_no_deduction(self):
        score = self._base_good(competitive_bids_received=0)
        assert score == pytest.approx(self._base_score())

    def test_price_increase_above_15_deducts_8(self):
        score = self._base_good(price_increase_proposed=16.0)
        assert score == pytest.approx(self._base_score() - 8.0)

    def test_price_increase_exactly_15_not_deducted_by_8(self):
        # >15 threshold, 15 itself is "above 5 but not above 15" → -3
        score = self._base_good(price_increase_proposed=15.0)
        assert score == pytest.approx(self._base_score() - 3.0)

    def test_price_increase_above_5_deducts_3(self):
        score = self._base_good(price_increase_proposed=10.0)
        assert score == pytest.approx(self._base_score() - 3.0)

    def test_price_increase_exactly_5_no_deduction(self):
        # >5 threshold, exactly 5 → no deduction
        score = self._base_good(price_increase_proposed=5.0)
        assert score == pytest.approx(self._base_score())

    def test_price_increase_0_no_deduction(self):
        score = self._base_good(price_increase_proposed=0.0)
        assert score == pytest.approx(self._base_score())

    def test_combined_deductions(self):
        score = self._base_good(
            support_escalations=3,
            competitive_bids_received=2,
            price_increase_proposed=20.0,
        )
        # -15 -10 -8 = -33
        assert score == pytest.approx(self._base_score() - 33.0)


# ---------------------------------------------------------------------------
# 10. TestRenewalScoreBonus
# ---------------------------------------------------------------------------

class TestRenewalScoreBonus:
    """Positive signals: budget+8, multi_year+7, stakeholders>=3 → +5."""

    _BONUS_BASE = dict(
        health_score=0.0,
        nps_score=-100.0,
        executive_engaged=False,
        champion_strength=0.0,
        qbr_completed_last_90d=False,
        support_escalations=0,
        competitive_bids_received=0,
        price_increase_proposed=0.0,
        budget_confirmed=False,
        multi_year_interest=False,
        stakeholder_count=0,
    )

    def _base_no_bonus(self, **extra) -> float:
        return _renewal_score(make_input(**{**self._BONUS_BASE, **extra}))

    def test_budget_confirmed_adds_8(self):
        base = self._base_no_bonus()
        with_budget = self._base_no_bonus(budget_confirmed=True)
        assert with_budget - base == pytest.approx(8.0)

    def test_multi_year_adds_7(self):
        base = self._base_no_bonus()
        with_multi = self._base_no_bonus(multi_year_interest=True)
        assert with_multi - base == pytest.approx(7.0)

    def test_stakeholders_3_adds_5(self):
        base = self._base_no_bonus()
        with_stake = self._base_no_bonus(stakeholder_count=3)
        assert with_stake - base == pytest.approx(5.0)

    def test_stakeholders_10_adds_5(self):
        base = self._base_no_bonus()
        with_stake = self._base_no_bonus(stakeholder_count=10)
        assert with_stake - base == pytest.approx(5.0)

    def test_stakeholders_2_adds_nothing(self):
        base = self._base_no_bonus()
        with_stake = self._base_no_bonus(stakeholder_count=2)
        assert with_stake == base

    def test_stakeholders_1_adds_nothing(self):
        base = self._base_no_bonus()
        with_stake = self._base_no_bonus(stakeholder_count=1)
        assert with_stake == base

    def test_stakeholders_0_adds_nothing(self):
        base = self._base_no_bonus()
        with_stake = self._base_no_bonus(stakeholder_count=0)
        assert with_stake == base

    def test_all_bonuses_combined(self):
        score = self._base_no_bonus(
            budget_confirmed=True,
            multi_year_interest=True,
            stakeholder_count=3,
        )
        assert score == pytest.approx(20.0)  # 8+7+5

    def test_no_budget_no_bonus(self):
        score = self._base_no_bonus(budget_confirmed=False)
        assert score == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# 11. TestRenewalScoreClamping
# ---------------------------------------------------------------------------

class TestRenewalScoreClamping:
    def test_cannot_exceed_100(self, green_input):
        # Perfect inputs should be clamped to 100
        score = _renewal_score(green_input)
        assert score <= 100.0

    def test_cannot_go_below_0(self, red_input):
        score = _renewal_score(red_input)
        assert score >= 0.0

    def test_floor_is_zero_with_all_negatives(self):
        inp = make_input(
            health_score=0.0,
            nps_score=-100.0,
            executive_engaged=False,
            champion_strength=0.0,
            qbr_completed_last_90d=False,
            support_escalations=3,
            competitive_bids_received=2,
            price_increase_proposed=20.0,
            budget_confirmed=False,
            multi_year_interest=False,
            stakeholder_count=0,
        )
        assert _renewal_score(inp) == 0.0

    def test_ceiling_is_at_most_100_with_all_positives(self):
        inp = make_input(
            health_score=100.0,
            nps_score=100.0,
            executive_engaged=True,
            champion_strength=100.0,
            qbr_completed_last_90d=True,
            support_escalations=0,
            competitive_bids_received=0,
            price_increase_proposed=0.0,
            budget_confirmed=True,
            multi_year_interest=True,
            stakeholder_count=5,
        )
        score = _renewal_score(inp)
        assert score <= 100.0
        assert score > 0.0

    def test_returns_float(self, baseline_input):
        score = _renewal_score(baseline_input)
        assert isinstance(score, (int, float))

    def test_rounded_to_1dp(self, baseline_input):
        score = _renewal_score(baseline_input)
        assert score == round(score, 1)


# ---------------------------------------------------------------------------
# 12. TestUpliftScoreSeats
# ---------------------------------------------------------------------------

class TestUpliftScoreSeats:
    """seat_utilization_pct thresholds: >=90→+30, >=75→+20, >=60→+10."""

    def _seat_only_score(self, seat: float) -> float:
        return _uplift_score(make_input(
            seat_utilization_pct=seat,
            feature_adoption_pct=0.0,
            expansion_history=False,
            new_use_cases=0,
            health_score=0.0,
        ))

    def test_seat_90_gives_30(self):
        assert self._seat_only_score(90.0) == pytest.approx(30.0)

    def test_seat_100_gives_30(self):
        assert self._seat_only_score(100.0) == pytest.approx(30.0)

    def test_seat_89_gives_20(self):
        assert self._seat_only_score(89.0) == pytest.approx(20.0)

    def test_seat_75_gives_20(self):
        assert self._seat_only_score(75.0) == pytest.approx(20.0)

    def test_seat_74_gives_10(self):
        assert self._seat_only_score(74.0) == pytest.approx(10.0)

    def test_seat_60_gives_10(self):
        assert self._seat_only_score(60.0) == pytest.approx(10.0)

    def test_seat_59_gives_0(self):
        assert self._seat_only_score(59.0) == pytest.approx(0.0)

    def test_seat_0_gives_0(self):
        assert self._seat_only_score(0.0) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# 13. TestUpliftScoreFeatures
# ---------------------------------------------------------------------------

class TestUpliftScoreFeatures:
    """feature_adoption_pct thresholds: >=80→+25, >=60→+15, >=40→+5."""

    def _feature_only_score(self, feat: float) -> float:
        return _uplift_score(make_input(
            seat_utilization_pct=0.0,
            feature_adoption_pct=feat,
            expansion_history=False,
            new_use_cases=0,
            health_score=0.0,
        ))

    def test_feature_80_gives_25(self):
        assert self._feature_only_score(80.0) == pytest.approx(25.0)

    def test_feature_100_gives_25(self):
        assert self._feature_only_score(100.0) == pytest.approx(25.0)

    def test_feature_79_gives_15(self):
        assert self._feature_only_score(79.0) == pytest.approx(15.0)

    def test_feature_60_gives_15(self):
        assert self._feature_only_score(60.0) == pytest.approx(15.0)

    def test_feature_59_gives_5(self):
        assert self._feature_only_score(59.0) == pytest.approx(5.0)

    def test_feature_40_gives_5(self):
        assert self._feature_only_score(40.0) == pytest.approx(5.0)

    def test_feature_39_gives_0(self):
        assert self._feature_only_score(39.0) == pytest.approx(0.0)

    def test_feature_0_gives_0(self):
        assert self._feature_only_score(0.0) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# 14. TestUpliftScoreExpansionAndUseCases
# ---------------------------------------------------------------------------

class TestUpliftScoreExpansionAndUseCases:
    """expansion_history→+20, new_use_cases capped at 25 (>=4 cases → 25 max)."""

    def _expansion_score(self, expansion: bool, new_uc: int) -> float:
        return _uplift_score(make_input(
            seat_utilization_pct=0.0,
            feature_adoption_pct=0.0,
            expansion_history=expansion,
            new_use_cases=new_uc,
            health_score=0.0,
        ))

    def test_expansion_history_true_adds_20(self):
        assert self._expansion_score(True, 0) == pytest.approx(20.0)

    def test_expansion_history_false_adds_0(self):
        assert self._expansion_score(False, 0) == pytest.approx(0.0)

    def test_one_use_case_adds_8(self):
        assert self._expansion_score(False, 1) == pytest.approx(8.0)

    def test_two_use_cases_adds_16(self):
        assert self._expansion_score(False, 2) == pytest.approx(16.0)

    def test_three_use_cases_adds_24(self):
        assert self._expansion_score(False, 3) == pytest.approx(24.0)

    def test_four_use_cases_capped_at_25(self):
        # 4 * 8 = 32, capped at 25
        assert self._expansion_score(False, 4) == pytest.approx(25.0)

    def test_ten_use_cases_capped_at_25(self):
        assert self._expansion_score(False, 10) == pytest.approx(25.0)

    def test_zero_use_cases_adds_0(self):
        assert self._expansion_score(False, 0) == pytest.approx(0.0)

    def test_expansion_plus_use_cases(self):
        # expansion(20) + 1 use case(8) = 28
        assert self._expansion_score(True, 1) == pytest.approx(28.0)

    def test_health_70_adds_10_to_uplift(self):
        score_low = _uplift_score(make_input(
            seat_utilization_pct=0.0, feature_adoption_pct=0.0,
            expansion_history=False, new_use_cases=0, health_score=69.0,
        ))
        score_high = _uplift_score(make_input(
            seat_utilization_pct=0.0, feature_adoption_pct=0.0,
            expansion_history=False, new_use_cases=0, health_score=70.0,
        ))
        assert score_high - score_low == pytest.approx(10.0)

    def test_health_below_70_no_bonus(self):
        score = _uplift_score(make_input(
            seat_utilization_pct=0.0, feature_adoption_pct=0.0,
            expansion_history=False, new_use_cases=0, health_score=69.9,
        ))
        assert score == pytest.approx(0.0)

    def test_uplift_score_clamped_at_100(self):
        score = _uplift_score(make_input(
            seat_utilization_pct=100.0,
            feature_adoption_pct=100.0,
            expansion_history=True,
            new_use_cases=10,
            health_score=100.0,
        ))
        assert score <= 100.0

    def test_uplift_score_returns_float(self):
        score = _uplift_score(make_input())
        assert isinstance(score, (int, float))


# ---------------------------------------------------------------------------
# 15. TestUpliftPotentialThresholds
# ---------------------------------------------------------------------------

class TestUpliftPotentialThresholds:
    def test_score_70_is_high(self):
        assert _uplift_potential(70.0) == UpliftPotential.HIGH

    def test_score_69_is_medium(self):
        assert _uplift_potential(69.0) == UpliftPotential.MEDIUM

    def test_score_100_is_high(self):
        assert _uplift_potential(100.0) == UpliftPotential.HIGH

    def test_score_40_is_medium(self):
        assert _uplift_potential(40.0) == UpliftPotential.MEDIUM

    def test_score_39_is_low(self):
        assert _uplift_potential(39.0) == UpliftPotential.LOW

    def test_score_0_is_low(self):
        assert _uplift_potential(0.0) == UpliftPotential.LOW

    def test_score_50_is_medium(self):
        assert _uplift_potential(50.0) == UpliftPotential.MEDIUM

    def test_exact_boundary_70_high(self):
        assert _uplift_potential(70.0) == UpliftPotential.HIGH

    def test_exact_boundary_40_medium(self):
        assert _uplift_potential(40.0) == UpliftPotential.MEDIUM

    def test_just_below_40_low(self):
        assert _uplift_potential(39.9) == UpliftPotential.LOW


# ---------------------------------------------------------------------------
# 16. TestRenewalRiskThresholds
# ---------------------------------------------------------------------------

class TestRenewalRiskThresholds:
    def test_score_75_is_green(self):
        assert _renewal_risk(75.0) == RenewalRisk.GREEN

    def test_score_74_is_yellow(self):
        assert _renewal_risk(74.0) == RenewalRisk.YELLOW

    def test_score_100_is_green(self):
        assert _renewal_risk(100.0) == RenewalRisk.GREEN

    def test_score_50_is_yellow(self):
        assert _renewal_risk(50.0) == RenewalRisk.YELLOW

    def test_score_49_is_orange(self):
        assert _renewal_risk(49.0) == RenewalRisk.ORANGE

    def test_score_25_is_orange(self):
        assert _renewal_risk(25.0) == RenewalRisk.ORANGE

    def test_score_24_is_red(self):
        assert _renewal_risk(24.0) == RenewalRisk.RED

    def test_score_0_is_red(self):
        assert _renewal_risk(0.0) == RenewalRisk.RED

    def test_score_74_9_is_yellow(self):
        assert _renewal_risk(74.9) == RenewalRisk.YELLOW

    def test_score_50_exactly_yellow(self):
        assert _renewal_risk(50.0) == RenewalRisk.YELLOW

    def test_score_25_exactly_orange(self):
        assert _renewal_risk(25.0) == RenewalRisk.ORANGE


# ---------------------------------------------------------------------------
# 17. TestRecommendedUplift
# ---------------------------------------------------------------------------

class TestRecommendedUplift:
    """HIGH+health>=70: max(8,min(proposed,15)); MEDIUM: min(proposed,8); LOW: min(proposed,3)."""

    def test_high_uplift_high_health_returns_at_least_8(self):
        # up_score=70, health=70, proposed=5 → max(8, min(5,15)) = max(8,5) = 8
        result = _recommended_uplift(
            make_input(price_increase_proposed=5.0, health_score=70.0),
            70.0,
        )
        assert result == pytest.approx(8.0)

    def test_high_uplift_high_health_proposed_above_8(self):
        # up_score=70, health=70, proposed=12 → max(8, min(12,15)) = max(8,12) = 12
        result = _recommended_uplift(
            make_input(price_increase_proposed=12.0, health_score=70.0),
            70.0,
        )
        assert result == pytest.approx(12.0)

    def test_high_uplift_high_health_caps_at_15(self):
        # up_score=70, health=70, proposed=20 → max(8, min(20,15)) = max(8,15) = 15
        result = _recommended_uplift(
            make_input(price_increase_proposed=20.0, health_score=70.0),
            70.0,
        )
        assert result == pytest.approx(15.0)

    def test_high_uplift_low_health_uses_medium_path(self):
        # up_score=70 but health=69 → falls to up_score>=40 path: min(proposed,8)
        result = _recommended_uplift(
            make_input(price_increase_proposed=10.0, health_score=69.0),
            70.0,
        )
        assert result == pytest.approx(8.0)

    def test_medium_uplift_caps_at_8(self):
        result = _recommended_uplift(
            make_input(price_increase_proposed=10.0, health_score=70.0),
            50.0,
        )
        assert result == pytest.approx(8.0)

    def test_medium_uplift_below_cap(self):
        result = _recommended_uplift(
            make_input(price_increase_proposed=5.0, health_score=70.0),
            50.0,
        )
        assert result == pytest.approx(5.0)

    def test_medium_uplift_exact_boundary_40(self):
        result = _recommended_uplift(
            make_input(price_increase_proposed=10.0, health_score=70.0),
            40.0,
        )
        assert result == pytest.approx(8.0)

    def test_low_uplift_caps_at_3(self):
        result = _recommended_uplift(
            make_input(price_increase_proposed=10.0, health_score=70.0),
            39.0,
        )
        assert result == pytest.approx(3.0)

    def test_low_uplift_below_cap(self):
        result = _recommended_uplift(
            make_input(price_increase_proposed=2.0, health_score=70.0),
            39.0,
        )
        assert result == pytest.approx(2.0)

    def test_low_uplift_zero_proposed(self):
        result = _recommended_uplift(
            make_input(price_increase_proposed=0.0, health_score=70.0),
            0.0,
        )
        assert result == pytest.approx(0.0)

    def test_returns_float(self):
        result = _recommended_uplift(make_input(), 50.0)
        assert isinstance(result, (int, float))

    def test_rounded_to_1dp(self):
        result = _recommended_uplift(make_input(price_increase_proposed=7.333), 50.0)
        assert result == round(result, 1)


# ---------------------------------------------------------------------------
# 18. TestRenewalActionMapping
# ---------------------------------------------------------------------------

class TestRenewalActionMapping:
    def test_red_risk_returns_save(self):
        inp = make_input(health_score=50.0)
        action = _renewal_action(inp, RenewalRisk.RED, UpliftPotential.LOW, 30)
        assert action == RenewalAction.SAVE

    def test_orange_risk_returns_intervene(self):
        inp = make_input(health_score=50.0)
        action = _renewal_action(inp, RenewalRisk.ORANGE, UpliftPotential.LOW, 30)
        assert action == RenewalAction.INTERVENE

    def test_green_days_91_health_80_early_renew(self):
        inp = make_input(health_score=80.0)
        action = _renewal_action(inp, RenewalRisk.GREEN, UpliftPotential.HIGH, 91)
        assert action == RenewalAction.EARLY_RENEW

    def test_green_days_200_health_80_early_renew(self):
        inp = make_input(health_score=80.0)
        action = _renewal_action(inp, RenewalRisk.GREEN, UpliftPotential.HIGH, 200)
        assert action == RenewalAction.EARLY_RENEW

    def test_green_days_90_close_renewal(self):
        inp = make_input(health_score=80.0)
        action = _renewal_action(inp, RenewalRisk.GREEN, UpliftPotential.HIGH, 90)
        assert action == RenewalAction.CLOSE_RENEWAL

    def test_green_days_30_close_renewal(self):
        inp = make_input(health_score=50.0)
        action = _renewal_action(inp, RenewalRisk.GREEN, UpliftPotential.LOW, 30)
        assert action == RenewalAction.CLOSE_RENEWAL

    def test_green_days_91_health_79_accelerate(self):
        # days > 90 but health < 80 → falls to ACCELERATE
        inp = make_input(health_score=79.0)
        action = _renewal_action(inp, RenewalRisk.GREEN, UpliftPotential.MEDIUM, 91)
        assert action == RenewalAction.ACCELERATE

    def test_yellow_returns_accelerate(self):
        inp = make_input(health_score=70.0)
        action = _renewal_action(inp, RenewalRisk.YELLOW, UpliftPotential.MEDIUM, 60)
        assert action == RenewalAction.ACCELERATE

    def test_yellow_returns_accelerate_high_days(self):
        inp = make_input(health_score=70.0)
        action = _renewal_action(inp, RenewalRisk.YELLOW, UpliftPotential.HIGH, 200)
        assert action == RenewalAction.ACCELERATE

    def test_red_overrides_other_conditions(self):
        # Even with high days and health, RED → SAVE
        inp = make_input(health_score=90.0)
        action = _renewal_action(inp, RenewalRisk.RED, UpliftPotential.HIGH, 200)
        assert action == RenewalAction.SAVE

    def test_orange_overrides_green_conditions(self):
        inp = make_input(health_score=90.0)
        action = _renewal_action(inp, RenewalRisk.ORANGE, UpliftPotential.HIGH, 200)
        assert action == RenewalAction.INTERVENE


# ---------------------------------------------------------------------------
# 19. TestBuildChurnSignals
# ---------------------------------------------------------------------------

class TestBuildChurnSignals:
    def test_no_signals_clean_input(self):
        inp = make_input(
            support_escalations=0,
            competitive_bids_received=0,
            nps_score=50.0,
            champion_strength=80.0,
            executive_engaged=True,
            product_adoption_score=70.0,
            price_increase_proposed=0.0,
            budget_confirmed=True,
            days_to_renewal=90,
        )
        signals = _build_churn_signals(inp, 80.0)
        assert signals == []

    def test_escalations_3_critical_signal(self):
        inp = make_input(support_escalations=3)
        signals = _build_churn_signals(inp, 50.0)
        assert any("3" in s and "escalade" in s.lower() for s in signals)

    def test_escalations_5_critical_signal(self):
        inp = make_input(support_escalations=5)
        signals = _build_churn_signals(inp, 50.0)
        assert any("5" in s for s in signals)

    def test_escalations_1_mild_signal(self):
        inp = make_input(support_escalations=1)
        signals = _build_churn_signals(inp, 50.0)
        assert any("1" in s and "escalade" in s.lower() for s in signals)

    def test_escalations_2_mild_signal(self):
        inp = make_input(support_escalations=2)
        signals = _build_churn_signals(inp, 50.0)
        assert any("2" in s for s in signals)

    def test_escalations_0_no_signal(self):
        inp = make_input(support_escalations=0,
                        competitive_bids_received=0, nps_score=50.0,
                        champion_strength=80.0, executive_engaged=True,
                        product_adoption_score=70.0, price_increase_proposed=0.0,
                        budget_confirmed=True, days_to_renewal=90)
        signals = _build_churn_signals(inp, 80.0)
        assert not any("escalade" in s.lower() for s in signals)

    def test_2_competitor_bids_high_risk_signal(self):
        inp = make_input(competitive_bids_received=2)
        signals = _build_churn_signals(inp, 50.0)
        assert any("2" in s and "concurrent" in s.lower() for s in signals)

    def test_1_competitor_bid_signal(self):
        inp = make_input(competitive_bids_received=1)
        signals = _build_churn_signals(inp, 50.0)
        assert any("concurrent" in s.lower() for s in signals)

    def test_negative_nps_signal(self):
        inp = make_input(nps_score=-10.0)
        signals = _build_churn_signals(inp, 50.0)
        assert any("nps" in s.lower() and "négatif" in s.lower() for s in signals)

    def test_low_nps_under_20_signal(self):
        inp = make_input(nps_score=10.0)
        signals = _build_churn_signals(inp, 50.0)
        assert any("nps" in s.lower() for s in signals)

    def test_nps_20_no_nps_signal(self):
        inp = make_input(nps_score=20.0, support_escalations=0,
                        competitive_bids_received=0, champion_strength=80.0,
                        executive_engaged=True, product_adoption_score=70.0,
                        price_increase_proposed=0.0, budget_confirmed=True,
                        days_to_renewal=90)
        signals = _build_churn_signals(inp, 80.0)
        assert not any("nps" in s.lower() for s in signals)

    def test_champion_below_30_signal(self):
        inp = make_input(champion_strength=29.0)
        signals = _build_churn_signals(inp, 50.0)
        assert any("champion" in s.lower() for s in signals)

    def test_champion_30_no_signal(self):
        inp = make_input(champion_strength=30.0, support_escalations=0,
                        competitive_bids_received=0, nps_score=50.0,
                        executive_engaged=True, product_adoption_score=70.0,
                        price_increase_proposed=0.0, budget_confirmed=True,
                        days_to_renewal=90)
        signals = _build_churn_signals(inp, 80.0)
        assert not any("champion" in s.lower() for s in signals)

    def test_exec_not_engaged_signal(self):
        inp = make_input(executive_engaged=False)
        signals = _build_churn_signals(inp, 50.0)
        assert any("exécutif" in s.lower() or "sponsor" in s.lower() for s in signals)

    def test_low_product_adoption_signal(self):
        inp = make_input(product_adoption_score=39.0)
        signals = _build_churn_signals(inp, 50.0)
        assert any("adoption" in s.lower() for s in signals)

    def test_product_adoption_40_no_signal(self):
        inp = make_input(product_adoption_score=40.0, support_escalations=0,
                        competitive_bids_received=0, nps_score=50.0,
                        champion_strength=80.0, executive_engaged=True,
                        price_increase_proposed=0.0, budget_confirmed=True,
                        days_to_renewal=90)
        signals = _build_churn_signals(inp, 80.0)
        assert not any("adoption" in s.lower() for s in signals)

    def test_price_above_15_signal(self):
        inp = make_input(price_increase_proposed=16.0)
        signals = _build_churn_signals(inp, 50.0)
        assert any("prix" in s.lower() or "hausse" in s.lower() for s in signals)

    def test_budget_not_confirmed_near_renewal_signal(self):
        inp = make_input(budget_confirmed=False, days_to_renewal=59)
        signals = _build_churn_signals(inp, 50.0)
        assert any("budget" in s.lower() for s in signals)

    def test_budget_not_confirmed_far_from_renewal_no_signal(self):
        inp = make_input(budget_confirmed=False, days_to_renewal=61,
                        support_escalations=0, competitive_bids_received=0,
                        nps_score=50.0, champion_strength=80.0,
                        executive_engaged=True, product_adoption_score=70.0,
                        price_increase_proposed=0.0)
        signals = _build_churn_signals(inp, 80.0)
        assert not any("budget" in s.lower() for s in signals)

    def test_returns_list(self, baseline_input):
        signals = _build_churn_signals(baseline_input, 50.0)
        assert isinstance(signals, list)


# ---------------------------------------------------------------------------
# 20. TestBuildRetentionLevers
# ---------------------------------------------------------------------------

class TestBuildRetentionLevers:
    def test_health_70_lever(self):
        inp = make_input(health_score=70.0)
        levers = _build_retention_levers(inp, RenewalRisk.YELLOW)
        assert any("roi" in l.lower() or "santé" in l.lower() for l in levers)

    def test_health_below_70_no_health_lever(self):
        inp = make_input(health_score=69.0, expansion_history=False,
                        multi_year_interest=False, seat_utilization_pct=0.0,
                        qbr_completed_last_90d=False, stakeholder_count=0,
                        new_use_cases=0, executive_engaged=False)
        levers = _build_retention_levers(inp, RenewalRisk.YELLOW)
        assert not any("santé" in l.lower() for l in levers)

    def test_expansion_history_lever(self):
        inp = make_input(expansion_history=True)
        levers = _build_retention_levers(inp, RenewalRisk.YELLOW)
        assert any("expansion" in l.lower() or "croit" in l.lower() for l in levers)

    def test_no_expansion_history_no_lever(self):
        inp = make_input(expansion_history=False, health_score=0.0,
                        multi_year_interest=False, seat_utilization_pct=0.0,
                        qbr_completed_last_90d=False, stakeholder_count=0,
                        new_use_cases=0, executive_engaged=False)
        levers = _build_retention_levers(inp, RenewalRisk.YELLOW)
        assert not any("expansion" in l.lower() for l in levers)

    def test_multi_year_lever(self):
        inp = make_input(multi_year_interest=True)
        levers = _build_retention_levers(inp, RenewalRisk.YELLOW)
        assert any("pluriannuel" in l.lower() or "multi" in l.lower() for l in levers)

    def test_seat_80_lever(self):
        inp = make_input(seat_utilization_pct=80.0)
        levers = _build_retention_levers(inp, RenewalRisk.YELLOW)
        assert any("siège" in l.lower() or "80" in l for l in levers)

    def test_seat_79_no_seat_lever(self):
        inp = make_input(seat_utilization_pct=79.0, health_score=0.0,
                        expansion_history=False, multi_year_interest=False,
                        qbr_completed_last_90d=False, stakeholder_count=0,
                        new_use_cases=0, executive_engaged=False)
        levers = _build_retention_levers(inp, RenewalRisk.YELLOW)
        assert not any("siège" in l.lower() for l in levers)

    def test_qbr_lever(self):
        inp = make_input(qbr_completed_last_90d=True)
        levers = _build_retention_levers(inp, RenewalRisk.YELLOW)
        assert any("qbr" in l.lower() for l in levers)

    def test_stakeholder_3_lever(self):
        inp = make_input(stakeholder_count=3)
        levers = _build_retention_levers(inp, RenewalRisk.YELLOW)
        assert any("3" in l and "prenante" in l.lower() for l in levers)

    def test_new_use_cases_lever(self):
        inp = make_input(new_use_cases=2)
        levers = _build_retention_levers(inp, RenewalRisk.YELLOW)
        assert any("cas" in l.lower() or "usage" in l.lower() for l in levers)

    def test_no_use_cases_no_lever(self):
        inp = make_input(new_use_cases=0, health_score=0.0,
                        expansion_history=False, multi_year_interest=False,
                        seat_utilization_pct=0.0, qbr_completed_last_90d=False,
                        stakeholder_count=0, executive_engaged=False)
        levers = _build_retention_levers(inp, RenewalRisk.YELLOW)
        assert not any("cas" in l.lower() for l in levers)

    def test_exec_engaged_lever(self):
        inp = make_input(executive_engaged=True)
        levers = _build_retention_levers(inp, RenewalRisk.YELLOW)
        assert any("exécutif" in l.lower() or "exécutiv" in l.lower() for l in levers)

    def test_red_risk_champion_50_lever(self):
        inp = make_input(champion_strength=50.0)
        levers = _build_retention_levers(inp, RenewalRisk.RED)
        assert any("champion" in l.lower() for l in levers)

    def test_orange_risk_champion_50_lever(self):
        inp = make_input(champion_strength=50.0)
        levers = _build_retention_levers(inp, RenewalRisk.ORANGE)
        assert any("champion" in l.lower() for l in levers)

    def test_green_risk_champion_50_no_champion_lever(self):
        inp = make_input(champion_strength=50.0, health_score=0.0,
                        expansion_history=False, multi_year_interest=False,
                        seat_utilization_pct=0.0, qbr_completed_last_90d=False,
                        stakeholder_count=0, new_use_cases=0,
                        executive_engaged=False)
        levers = _build_retention_levers(inp, RenewalRisk.GREEN)
        assert not any("champion" in l.lower() for l in levers)

    def test_returns_list(self):
        inp = make_input()
        levers = _build_retention_levers(inp, RenewalRisk.YELLOW)
        assert isinstance(levers, list)


# ---------------------------------------------------------------------------
# 21. TestEngineScore
# ---------------------------------------------------------------------------

class TestEngineScore:
    def test_score_returns_renewal_result(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert isinstance(result, RenewalResult)

    def test_score_stores_result(self, engine, baseline_input):
        engine.score(baseline_input)
        assert engine.get("C001") is not None

    def test_score_contract_id_preserved(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert result.contract_id == "C001"

    def test_score_account_name_preserved(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert result.account_name == "Acme Corp"

    def test_score_arr_preserved(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert result.arr_eur == pytest.approx(100_000.0)

    def test_score_renewal_score_is_numeric(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert isinstance(result.renewal_score, (int, float))

    def test_score_renewal_risk_is_enum(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert isinstance(result.renewal_risk, RenewalRisk)

    def test_score_renewal_action_is_enum(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert isinstance(result.renewal_action, RenewalAction)

    def test_score_uplift_potential_is_enum(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert isinstance(result.uplift_potential, UpliftPotential)

    def test_score_churn_signals_is_list(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert isinstance(result.churn_signals, list)

    def test_score_retention_levers_is_list(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert isinstance(result.retention_levers, list)

    def test_score_timeline_steps_is_list(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert isinstance(result.timeline_steps, list)

    def test_score_negotiation_tactics_is_list(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert isinstance(result.negotiation_tactics, list)

    def test_score_overwrite_contract(self, engine):
        inp1 = make_input(contract_id="C001", arr_eur=100_000.0)
        inp2 = make_input(contract_id="C001", arr_eur=200_000.0)
        engine.score(inp1)
        engine.score(inp2)
        result = engine.get("C001")
        assert result.arr_eur == pytest.approx(200_000.0)

    def test_get_nonexistent_returns_none(self, engine):
        assert engine.get("NONEXISTENT") is None

    def test_score_red_input_has_save_action(self, engine, red_input):
        result = engine.score(red_input)
        assert result.renewal_action == RenewalAction.SAVE

    def test_score_green_input_has_green_risk(self, engine, green_input):
        result = engine.score(green_input)
        assert result.renewal_risk == RenewalRisk.GREEN

    def test_score_recommended_uplift_pct_numeric(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert isinstance(result.recommended_uplift_pct, (int, float))

    def test_score_renewal_score_range(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert 0.0 <= result.renewal_score <= 100.0

    def test_score_uplift_score_range(self, engine, baseline_input):
        result = engine.score(baseline_input)
        assert 0.0 <= result.uplift_score <= 100.0


# ---------------------------------------------------------------------------
# 22. TestEngineBatchAndFilters
# ---------------------------------------------------------------------------

class TestEngineBatchAndFilters:
    def _three_inputs(self) -> list[RenewalInput]:
        return [
            make_input(contract_id="C001", health_score=100.0, nps_score=100.0,
                      executive_engaged=True, champion_strength=90.0,
                      qbr_completed_last_90d=True, budget_confirmed=True,
                      multi_year_interest=True, stakeholder_count=5,
                      support_escalations=0, competitive_bids_received=0,
                      price_increase_proposed=0.0),
            make_input(contract_id="C002", health_score=50.0, nps_score=0.0,
                      executive_engaged=False, champion_strength=50.0,
                      qbr_completed_last_90d=False, budget_confirmed=False,
                      multi_year_interest=False, stakeholder_count=1,
                      support_escalations=1, competitive_bids_received=0,
                      price_increase_proposed=5.0),
            make_input(contract_id="C003", health_score=0.0, nps_score=-100.0,
                      executive_engaged=False, champion_strength=0.0,
                      qbr_completed_last_90d=False, budget_confirmed=False,
                      multi_year_interest=False, stakeholder_count=0,
                      support_escalations=3, competitive_bids_received=2,
                      price_increase_proposed=20.0),
        ]

    def test_batch_returns_list(self, engine):
        results = engine.score_batch(self._three_inputs())
        assert isinstance(results, list)

    def test_batch_returns_all_results(self, engine):
        results = engine.score_batch(self._three_inputs())
        assert len(results) == 3

    def test_batch_sorted_descending(self, engine):
        results = engine.score_batch(self._three_inputs())
        scores = [r.renewal_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_batch_highest_score_first(self, engine):
        results = engine.score_batch(self._three_inputs())
        assert results[0].contract_id == "C001"

    def test_batch_lowest_score_last(self, engine):
        results = engine.score_batch(self._three_inputs())
        assert results[-1].contract_id == "C003"

    def test_batch_stores_all_in_engine(self, engine):
        engine.score_batch(self._three_inputs())
        assert engine.get("C001") is not None
        assert engine.get("C002") is not None
        assert engine.get("C003") is not None

    def test_all_contracts_sorted_desc(self, engine):
        engine.score_batch(self._three_inputs())
        all_r = engine.all_contracts()
        scores = [r.renewal_score for r in all_r]
        assert scores == sorted(scores, reverse=True)

    def test_by_risk_green(self, engine):
        engine.score_batch(self._three_inputs())
        green = engine.by_risk(RenewalRisk.GREEN)
        for r in green:
            assert r.renewal_risk == RenewalRisk.GREEN

    def test_by_risk_red(self, engine):
        engine.score_batch(self._three_inputs())
        red = engine.by_risk(RenewalRisk.RED)
        for r in red:
            assert r.renewal_risk == RenewalRisk.RED

    def test_by_action_save(self, engine):
        engine.score_batch(self._three_inputs())
        saves = engine.by_action(RenewalAction.SAVE)
        for r in saves:
            assert r.renewal_action == RenewalAction.SAVE

    def test_at_risk_contains_only_red_orange(self, engine):
        engine.score_batch(self._three_inputs())
        at_risk = engine.at_risk()
        for r in at_risk:
            assert r.renewal_risk in (RenewalRisk.RED, RenewalRisk.ORANGE)

    def test_at_risk_excludes_green_yellow(self, engine):
        engine.score_batch(self._three_inputs())
        at_risk = engine.at_risk()
        for r in at_risk:
            assert r.renewal_risk not in (RenewalRisk.GREEN, RenewalRisk.YELLOW)

    def test_green_method_returns_only_green(self, engine):
        engine.score_batch(self._three_inputs())
        green = engine.green()
        for r in green:
            assert r.renewal_risk == RenewalRisk.GREEN

    def test_by_risk_returns_empty_for_absent_risk(self, engine):
        # Only score one red input
        engine.score(make_input(
            health_score=0.0, nps_score=-100.0, executive_engaged=False,
            champion_strength=0.0, qbr_completed_last_90d=False,
            budget_confirmed=False, multi_year_interest=False,
            stakeholder_count=0, support_escalations=3,
            competitive_bids_received=2, price_increase_proposed=20.0,
        ))
        assert engine.by_risk(RenewalRisk.GREEN) == []

    def test_empty_engine_all_contracts(self, engine):
        assert engine.all_contracts() == []

    def test_empty_engine_at_risk(self, engine):
        assert engine.at_risk() == []

    def test_empty_engine_green(self, engine):
        assert engine.green() == []


# ---------------------------------------------------------------------------
# 23. TestEngineAggregates
# ---------------------------------------------------------------------------

class TestEngineAggregates:
    def _load_three(self, engine: ContractRenewalEngine) -> None:
        inputs = [
            # RED: score near 0
            make_input(contract_id="C_RED", arr_eur=50_000.0,
                      health_score=0.0, nps_score=-100.0,
                      executive_engaged=False, champion_strength=0.0,
                      qbr_completed_last_90d=False, budget_confirmed=False,
                      multi_year_interest=False, stakeholder_count=0,
                      support_escalations=3, competitive_bids_received=2,
                      price_increase_proposed=20.0),
            # GREEN: high score
            make_input(contract_id="C_GREEN", arr_eur=200_000.0,
                      health_score=100.0, nps_score=100.0,
                      executive_engaged=True, champion_strength=90.0,
                      qbr_completed_last_90d=True, budget_confirmed=True,
                      multi_year_interest=True, stakeholder_count=5,
                      support_escalations=0, competitive_bids_received=0,
                      price_increase_proposed=0.0,
                      seat_utilization_pct=95.0, feature_adoption_pct=85.0,
                      expansion_history=True, new_use_cases=4),
            # YELLOW: mid score
            make_input(contract_id="C_YEL", arr_eur=100_000.0,
                      health_score=60.0, nps_score=10.0,
                      executive_engaged=False, champion_strength=50.0,
                      qbr_completed_last_90d=False, budget_confirmed=True,
                      multi_year_interest=False, stakeholder_count=2,
                      support_escalations=1, competitive_bids_received=0,
                      price_increase_proposed=5.0),
        ]
        engine.score_batch(inputs)

    def test_needs_save_returns_save_actions(self, engine):
        self._load_three(engine)
        saves = engine.needs_save()
        for r in saves:
            assert r.renewal_action == RenewalAction.SAVE

    def test_high_uplift_returns_high_potential(self, engine):
        self._load_three(engine)
        high = engine.high_uplift()
        for r in high:
            assert r.uplift_potential == UpliftPotential.HIGH

    def test_total_arr_at_risk_is_numeric(self, engine):
        self._load_three(engine)
        val = engine.total_arr_at_risk()
        assert isinstance(val, (int, float))

    def test_total_arr_at_risk_only_red_orange(self, engine):
        self._load_three(engine)
        at_risk = engine.at_risk()
        expected = round(sum(r.arr_eur for r in at_risk), 2)
        assert engine.total_arr_at_risk() == pytest.approx(expected)

    def test_total_arr_renewing_sums_all(self, engine):
        self._load_three(engine)
        val = engine.total_arr_renewing()
        assert val == pytest.approx(350_000.0)

    def test_avg_renewal_score_rounded_to_1dp(self, engine):
        self._load_three(engine)
        avg = engine.avg_renewal_score()
        assert avg == round(avg, 1)

    def test_avg_renewal_score_numeric(self, engine):
        self._load_three(engine)
        assert isinstance(engine.avg_renewal_score(), (int, float))

    def test_avg_renewal_score_empty_engine_zero(self, engine):
        assert engine.avg_renewal_score() == 0.0

    def test_total_potential_uplift_eur_numeric(self, engine):
        self._load_three(engine)
        assert isinstance(engine.total_potential_uplift_eur(), (int, float))

    def test_total_potential_uplift_eur_formula(self, engine):
        self._load_three(engine)
        expected = round(sum(
            r.arr_eur * r.recommended_uplift_pct / 100.0
            for r in engine.all_contracts()
        ), 2)
        assert engine.total_potential_uplift_eur() == pytest.approx(expected)

    def test_total_potential_uplift_eur_empty_zero(self, engine):
        assert engine.total_potential_uplift_eur() == pytest.approx(0.0)

    def test_summary_returns_dict(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert isinstance(s, dict)

    def test_summary_total_correct(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert s["total"] == 3

    def test_summary_risk_counts_present(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert "risk_counts" in s
        assert isinstance(s["risk_counts"], dict)

    def test_summary_action_counts_present(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert "action_counts" in s

    def test_summary_uplift_counts_present(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert "uplift_counts" in s

    def test_summary_avg_renewal_score(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert s["avg_renewal_score"] == engine.avg_renewal_score()

    def test_summary_total_arr_at_risk(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert s["total_arr_at_risk_eur"] == engine.total_arr_at_risk()

    def test_summary_total_arr_renewing(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert s["total_arr_renewing_eur"] == engine.total_arr_renewing()

    def test_summary_total_potential_uplift(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert s["total_potential_uplift_eur"] == engine.total_potential_uplift_eur()

    def test_summary_needs_save_count(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert s["needs_save_count"] == len(engine.needs_save())

    def test_summary_high_uplift_count(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert s["high_uplift_count"] == len(engine.high_uplift())

    def test_summary_empty_engine(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}
        assert s["action_counts"] == {}
        assert s["uplift_counts"] == {}
        assert s["avg_renewal_score"] == 0.0
        assert s["total_arr_at_risk_eur"] == 0.0
        assert s["total_arr_renewing_eur"] == 0.0
        assert s["total_potential_uplift_eur"] == 0.0
        assert s["needs_save_count"] == 0
        assert s["high_uplift_count"] == 0

    def test_reset_clears_all(self, engine):
        self._load_three(engine)
        engine.reset()
        assert engine.all_contracts() == []
        assert engine.total_arr_renewing() == 0.0
        assert engine.avg_renewal_score() == 0.0

    def test_reset_then_rescore(self, engine, baseline_input):
        self._load_three(engine)
        engine.reset()
        engine.score(baseline_input)
        assert len(engine.all_contracts()) == 1

    def test_total_arr_renewing_empty_zero(self, engine):
        assert engine.total_arr_renewing() == pytest.approx(0.0)

    def test_needs_save_count_in_summary_matches(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert isinstance(s["needs_save_count"], int)

    def test_high_uplift_count_in_summary_matches(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert isinstance(s["high_uplift_count"], int)

    def test_single_contract_avg_equals_its_score(self, engine, baseline_input):
        engine.score(baseline_input)
        result = engine.get("C001")
        assert engine.avg_renewal_score() == pytest.approx(result.renewal_score)

    def test_two_contracts_avg(self, engine):
        inp1 = make_input(contract_id="C001", health_score=100.0, nps_score=100.0,
                         executive_engaged=True, champion_strength=90.0,
                         qbr_completed_last_90d=True, budget_confirmed=True,
                         multi_year_interest=True, stakeholder_count=5,
                         support_escalations=0, competitive_bids_received=0,
                         price_increase_proposed=0.0)
        inp2 = make_input(contract_id="C002", health_score=0.0, nps_score=-100.0,
                         executive_engaged=False, champion_strength=0.0,
                         qbr_completed_last_90d=False, budget_confirmed=False,
                         multi_year_interest=False, stakeholder_count=0,
                         support_escalations=3, competitive_bids_received=2,
                         price_increase_proposed=20.0)
        r1 = engine.score(inp1)
        r2 = engine.score(inp2)
        expected_avg = round((r1.renewal_score + r2.renewal_score) / 2, 1)
        assert engine.avg_renewal_score() == pytest.approx(expected_avg)
