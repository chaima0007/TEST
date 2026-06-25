"""Comprehensive pytest test suite for swarm.intelligence.territory_optimizer."""

from __future__ import annotations

import pytest

from swarm.intelligence.territory_optimizer import (
    TerritoryHealth,
    TerritoryAction,
    CoverageRisk,
    TerritoryInput,
    TerritoryResult,
    TerritoryOptimizerEngine,
    _pipeline_coverage,
    _white_space_pct,
    _balance_score,
    _territory_health,
    _coverage_risk,
    _territory_action,
    _build_strengths,
    _build_gaps,
    _build_recommendations,
    _territory_kpis,
)


# ─── Fixtures ─────────────────────────────────────────────────────────────────

def make_input(**overrides) -> TerritoryInput:
    """Return a base TerritoryInput with sane defaults; override any field."""
    defaults = dict(
        territory_id="T001",
        territory_name="EMEA North",
        region="emea",
        rep_name="Alice Dupont",
        rep_tenure_months=24,
        total_accounts=80,
        active_accounts=60,
        total_pipeline_eur=500_000.0,
        weighted_pipeline_eur=300_000.0,
        closed_won_ytd_eur=150_000.0,
        quota_eur=100_000.0,
        avg_account_health=75.0,
        accounts_with_qbr_pct=70.0,
        accounts_at_risk_count=2,
        white_space_accounts=8,
        avg_deal_cycle_days=45,
        deals_in_flight=5,
        rep_quota_attainment_pct=100.0,
        rep_ramp_complete=True,
        tam_eur=2_000_000.0,
        market_penetration_pct=50.0,
        competitive_intensity=30.0,
    )
    defaults.update(overrides)
    return TerritoryInput(**defaults)


@pytest.fixture
def base_input() -> TerritoryInput:
    """Standard healthy territory."""
    return make_input()


@pytest.fixture
def critical_input() -> TerritoryInput:
    """Territory in critical health."""
    return make_input(
        weighted_pipeline_eur=10_000.0,
        quota_eur=200_000.0,
        avg_account_health=20.0,
        accounts_with_qbr_pct=10.0,
        rep_quota_attainment_pct=20.0,
        white_space_accounts=70,
        total_accounts=80,
        accounts_at_risk_count=8,
        rep_ramp_complete=False,
    )


@pytest.fixture
def engine() -> TerritoryOptimizerEngine:
    return TerritoryOptimizerEngine()


# ─── 1. TestTerritoryHealthEnum ───────────────────────────────────────────────

class TestTerritoryHealthEnum:
    def test_members_exist(self):
        assert TerritoryHealth.OPTIMAL
        assert TerritoryHealth.BALANCED
        assert TerritoryHealth.IMBALANCED
        assert TerritoryHealth.CRITICAL

    def test_string_values(self):
        assert TerritoryHealth.OPTIMAL.value == "optimal"
        assert TerritoryHealth.BALANCED.value == "balanced"
        assert TerritoryHealth.IMBALANCED.value == "imbalanced"
        assert TerritoryHealth.CRITICAL.value == "critical"

    def test_is_str_subclass(self):
        assert isinstance(TerritoryHealth.OPTIMAL, str)
        assert isinstance(TerritoryHealth.CRITICAL, str)

    def test_equality_with_string(self):
        assert TerritoryHealth.OPTIMAL == "optimal"
        assert TerritoryHealth.CRITICAL == "critical"

    def test_four_members_total(self):
        assert len(list(TerritoryHealth)) == 4

    def test_unique_values(self):
        values = [m.value for m in TerritoryHealth]
        assert len(values) == len(set(values))

    def test_enum_identity(self):
        assert TerritoryHealth("optimal") is TerritoryHealth.OPTIMAL
        assert TerritoryHealth("critical") is TerritoryHealth.CRITICAL


# ─── 2. TestTerritoryActionEnum ───────────────────────────────────────────────

class TestTerritoryActionEnum:
    def test_members_exist(self):
        assert TerritoryAction.MAINTAIN
        assert TerritoryAction.REBALANCE
        assert TerritoryAction.HIRE
        assert TerritoryAction.SPLIT
        assert TerritoryAction.MERGE

    def test_string_values(self):
        assert TerritoryAction.MAINTAIN.value == "maintain"
        assert TerritoryAction.REBALANCE.value == "rebalance"
        assert TerritoryAction.HIRE.value == "hire"
        assert TerritoryAction.SPLIT.value == "split"
        assert TerritoryAction.MERGE.value == "merge"

    def test_is_str_subclass(self):
        assert isinstance(TerritoryAction.MAINTAIN, str)
        assert isinstance(TerritoryAction.SPLIT, str)

    def test_five_members_total(self):
        assert len(list(TerritoryAction)) == 5

    def test_unique_values(self):
        values = [m.value for m in TerritoryAction]
        assert len(values) == len(set(values))

    def test_enum_identity(self):
        assert TerritoryAction("split") is TerritoryAction.SPLIT
        assert TerritoryAction("merge") is TerritoryAction.MERGE


# ─── 3. TestCoverageRiskEnum ──────────────────────────────────────────────────

class TestCoverageRiskEnum:
    def test_members_exist(self):
        assert CoverageRisk.LOW
        assert CoverageRisk.MEDIUM
        assert CoverageRisk.HIGH
        assert CoverageRisk.CRITICAL

    def test_string_values(self):
        assert CoverageRisk.LOW.value == "low"
        assert CoverageRisk.MEDIUM.value == "medium"
        assert CoverageRisk.HIGH.value == "high"
        assert CoverageRisk.CRITICAL.value == "critical"

    def test_is_str_subclass(self):
        assert isinstance(CoverageRisk.LOW, str)
        assert isinstance(CoverageRisk.CRITICAL, str)

    def test_four_members_total(self):
        assert len(list(CoverageRisk)) == 4

    def test_enum_identity(self):
        assert CoverageRisk("low") is CoverageRisk.LOW
        assert CoverageRisk("critical") is CoverageRisk.CRITICAL


# ─── 4. TestTerritoryInputDataclass ───────────────────────────────────────────

class TestTerritoryInputDataclass:
    def test_instantiation(self, base_input):
        assert base_input.territory_id == "T001"

    def test_all_fields_accessible(self, base_input):
        assert base_input.territory_name == "EMEA North"
        assert base_input.region == "emea"
        assert base_input.rep_name == "Alice Dupont"
        assert base_input.rep_tenure_months == 24
        assert base_input.total_accounts == 80
        assert base_input.active_accounts == 60
        assert base_input.quota_eur == 100_000.0
        assert base_input.avg_account_health == 75.0
        assert base_input.accounts_with_qbr_pct == 70.0
        assert base_input.accounts_at_risk_count == 2
        assert base_input.white_space_accounts == 8
        assert base_input.avg_deal_cycle_days == 45
        assert base_input.deals_in_flight == 5
        assert base_input.rep_quota_attainment_pct == 100.0
        assert base_input.rep_ramp_complete is True
        assert base_input.tam_eur == 2_000_000.0
        assert base_input.market_penetration_pct == 50.0
        assert base_input.competitive_intensity == 30.0

    def test_boolean_field(self):
        inp = make_input(rep_ramp_complete=False)
        assert inp.rep_ramp_complete is False

    def test_zero_values_allowed(self):
        inp = make_input(quota_eur=0.0, total_accounts=0, white_space_accounts=0)
        assert inp.quota_eur == 0.0
        assert inp.total_accounts == 0

    def test_override_id(self):
        inp = make_input(territory_id="X999")
        assert inp.territory_id == "X999"

    def test_numeric_types(self, base_input):
        assert isinstance(base_input.total_pipeline_eur, (int, float))
        assert isinstance(base_input.weighted_pipeline_eur, (int, float))
        assert isinstance(base_input.closed_won_ytd_eur, (int, float))
        assert isinstance(base_input.quota_eur, (int, float))
        assert isinstance(base_input.avg_account_health, (int, float))


# ─── 5. TestTerritoryResultToDict ─────────────────────────────────────────────

class TestTerritoryResultToDict:
    def _make_result(self) -> TerritoryResult:
        return TerritoryResult(
            territory_id="T001",
            territory_name="North",
            region="emea",
            rep_name="Bob",
            territory_health=TerritoryHealth.OPTIMAL,
            territory_action=TerritoryAction.MAINTAIN,
            coverage_risk=CoverageRisk.LOW,
            balance_score=85.0,
            quota_attainment_pct=100.0,
            pipeline_coverage_ratio=3.0,
            white_space_pct=10.0,
            strengths=["Great pipeline"],
            gaps=[],
            recommendations=["Keep it up"],
            territory_kpis={"deals_in_flight": 5},
        )

    def test_to_dict_returns_dict(self):
        r = self._make_result()
        assert isinstance(r.to_dict(), dict)

    def test_health_serialized_as_string(self):
        r = self._make_result()
        assert r.to_dict()["territory_health"] == "optimal"

    def test_action_serialized_as_string(self):
        r = self._make_result()
        assert r.to_dict()["territory_action"] == "maintain"

    def test_coverage_risk_serialized_as_string(self):
        r = self._make_result()
        assert r.to_dict()["coverage_risk"] == "low"

    def test_all_expected_keys_present(self):
        r = self._make_result()
        d = r.to_dict()
        for key in [
            "territory_id", "territory_name", "region", "rep_name",
            "territory_health", "territory_action", "coverage_risk",
            "balance_score", "quota_attainment_pct", "pipeline_coverage_ratio",
            "white_space_pct", "strengths", "gaps", "recommendations",
            "territory_kpis",
        ]:
            assert key in d, f"Missing key: {key}"

    def test_lists_preserved(self):
        r = self._make_result()
        d = r.to_dict()
        assert d["strengths"] == ["Great pipeline"]
        assert d["gaps"] == []
        assert d["recommendations"] == ["Keep it up"]

    def test_numeric_values_preserved(self):
        r = self._make_result()
        d = r.to_dict()
        assert d["balance_score"] == 85.0
        assert d["pipeline_coverage_ratio"] == 3.0
        assert d["white_space_pct"] == 10.0

    def test_kpis_preserved(self):
        r = self._make_result()
        d = r.to_dict()
        assert d["territory_kpis"] == {"deals_in_flight": 5}

    def test_all_enum_values_as_string_critical(self):
        r = self._make_result()
        r.territory_health = TerritoryHealth.CRITICAL
        r.territory_action = TerritoryAction.REBALANCE
        r.coverage_risk = CoverageRisk.CRITICAL
        d = r.to_dict()
        assert d["territory_health"] == "critical"
        assert d["territory_action"] == "rebalance"
        assert d["coverage_risk"] == "critical"


# ─── 6. TestPipelineCoverage ──────────────────────────────────────────────────

class TestPipelineCoverage:
    def test_normal_calculation(self):
        inp = make_input(weighted_pipeline_eur=300_000.0, quota_eur=100_000.0)
        assert _pipeline_coverage(inp) == 3.0

    def test_quota_zero_returns_zero(self):
        inp = make_input(weighted_pipeline_eur=50_000.0, quota_eur=0.0)
        assert _pipeline_coverage(inp) == 0.0

    def test_quota_negative_returns_zero(self):
        inp = make_input(weighted_pipeline_eur=50_000.0, quota_eur=-1.0)
        assert _pipeline_coverage(inp) == 0.0

    def test_rounding_to_2dp(self):
        inp = make_input(weighted_pipeline_eur=100_000.0, quota_eur=30_000.0)
        result = _pipeline_coverage(inp)
        assert result == round(100_000.0 / 30_000.0, 2)
        assert result == 3.33

    def test_returns_float(self):
        inp = make_input(weighted_pipeline_eur=200_000.0, quota_eur=100_000.0)
        assert isinstance(_pipeline_coverage(inp), float)

    def test_less_than_one(self):
        inp = make_input(weighted_pipeline_eur=50_000.0, quota_eur=100_000.0)
        assert _pipeline_coverage(inp) == 0.5

    def test_exactly_one(self):
        inp = make_input(weighted_pipeline_eur=100_000.0, quota_eur=100_000.0)
        assert _pipeline_coverage(inp) == 1.0

    def test_exactly_two(self):
        inp = make_input(weighted_pipeline_eur=200_000.0, quota_eur=100_000.0)
        assert _pipeline_coverage(inp) == 2.0

    def test_exactly_three(self):
        inp = make_input(weighted_pipeline_eur=300_000.0, quota_eur=100_000.0)
        assert _pipeline_coverage(inp) == 3.0

    def test_zero_pipeline_nonzero_quota(self):
        inp = make_input(weighted_pipeline_eur=0.0, quota_eur=100_000.0)
        assert _pipeline_coverage(inp) == 0.0

    def test_rounding_second_case(self):
        inp = make_input(weighted_pipeline_eur=10_000.0, quota_eur=3_000.0)
        result = _pipeline_coverage(inp)
        assert result == round(10_000.0 / 3_000.0, 2)


# ─── 7. TestWhiteSpacePct ─────────────────────────────────────────────────────

class TestWhiteSpacePct:
    def test_normal_calculation(self):
        inp = make_input(white_space_accounts=10, total_accounts=100)
        assert _white_space_pct(inp) == 10.0

    def test_total_zero_returns_zero(self):
        inp = make_input(white_space_accounts=5, total_accounts=0)
        assert _white_space_pct(inp) == 0.0

    def test_total_negative_returns_zero(self):
        inp = make_input(white_space_accounts=5, total_accounts=-1)
        assert _white_space_pct(inp) == 0.0

    def test_rounded_to_1dp(self):
        inp = make_input(white_space_accounts=1, total_accounts=3)
        result = _white_space_pct(inp)
        assert result == round(1 / 3 * 100, 1)

    def test_returns_float(self):
        inp = make_input(white_space_accounts=10, total_accounts=100)
        assert isinstance(_white_space_pct(inp), float)

    def test_zero_white_space(self):
        inp = make_input(white_space_accounts=0, total_accounts=100)
        assert _white_space_pct(inp) == 0.0

    def test_all_white_space(self):
        inp = make_input(white_space_accounts=100, total_accounts=100)
        assert _white_space_pct(inp) == 100.0

    def test_boundary_10_pct(self):
        inp = make_input(white_space_accounts=10, total_accounts=100)
        assert _white_space_pct(inp) == 10.0

    def test_boundary_25_pct(self):
        inp = make_input(white_space_accounts=25, total_accounts=100)
        assert _white_space_pct(inp) == 25.0

    def test_boundary_40_pct(self):
        inp = make_input(white_space_accounts=40, total_accounts=100)
        assert _white_space_pct(inp) == 40.0


# ─── 8. TestBalanceScoreComponents ────────────────────────────────────────────

class TestBalanceScoreComponents:
    """Test each component of _balance_score in near-isolation."""

    # ---- Pipeline Coverage component (0-30 pts) ----
    def test_pc_gte_3_gives_30(self):
        # All other factors minimised to see only pc contribution
        inp = make_input(
            weighted_pipeline_eur=300_000.0, quota_eur=100_000.0,  # pc=3
            avg_account_health=0.0, accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=50, total_accounts=100,  # ws=50% -> 0pts
        )
        score = _balance_score(inp)
        # 30 (pc) + 0 (health) + 0 (qbr) + 0 (attainment) + 0 (ws)
        assert score == 30.0

    def test_pc_gte_2_gives_22(self):
        inp = make_input(
            weighted_pipeline_eur=200_000.0, quota_eur=100_000.0,  # pc=2
            avg_account_health=0.0, accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 22.0

    def test_pc_gte_1_5_gives_14(self):
        inp = make_input(
            weighted_pipeline_eur=150_000.0, quota_eur=100_000.0,  # pc=1.5
            avg_account_health=0.0, accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 14.0

    def test_pc_gte_1_gives_8(self):
        inp = make_input(
            weighted_pipeline_eur=100_000.0, quota_eur=100_000.0,  # pc=1
            avg_account_health=0.0, accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 8.0

    def test_pc_below_1_gives_0(self):
        inp = make_input(
            weighted_pipeline_eur=50_000.0, quota_eur=100_000.0,  # pc=0.5
            avg_account_health=0.0, accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 0.0

    # ---- Account health component (0-20 pts) ----
    def test_account_health_max_20(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,  # pc<1 -> 0pts
            avg_account_health=100.0,  # 100*0.2=20 -> capped at 20
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 20.0

    def test_account_health_partial(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=50.0,  # 50*0.2=10
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 10.0

    def test_account_health_zero(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 0.0

    # ---- QBR coverage component (0-15 pts) ----
    def test_qbr_max_15(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=100.0,  # 100*0.15=15 -> capped at 15
            rep_quota_attainment_pct=0.0,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 15.0

    def test_qbr_partial(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=60.0,  # 60*0.15=9
            rep_quota_attainment_pct=0.0,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 9.0

    def test_qbr_zero(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 0.0

    # ---- Quota attainment component (0-20 pts) ----
    def test_attainment_gte_100_gives_20(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=100.0,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 20.0

    def test_attainment_gte_75_gives_15(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=75.0,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 15.0

    def test_attainment_gte_50_gives_8(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=50.0,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 8.0

    def test_attainment_below_50_gives_0(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=49.9,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 0.0

    # ---- White space component (0-15 pts) ----
    def test_ws_lte_10_gives_15(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=10, total_accounts=100,  # ws=10%
        )
        score = _balance_score(inp)
        assert score == 15.0

    def test_ws_lte_25_gives_10(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=20, total_accounts=100,  # ws=20%
        )
        score = _balance_score(inp)
        assert score == 10.0

    def test_ws_lte_40_gives_5(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=30, total_accounts=100,  # ws=30%
        )
        score = _balance_score(inp)
        assert score == 5.0

    def test_ws_above_40_gives_0(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=50, total_accounts=100,  # ws=50%
        )
        score = _balance_score(inp)
        assert score == 0.0

    def test_ws_exactly_10_pct(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=10, total_accounts=100,  # ws=10.0 -> <=10 -> 15
        )
        assert _balance_score(inp) == 15.0

    def test_ws_exactly_25_pct(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=25, total_accounts=100,  # ws=25.0 -> <=25 -> 10
        )
        assert _balance_score(inp) == 10.0

    def test_ws_exactly_40_pct(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=40, total_accounts=100,  # ws=40.0 -> <=40 -> 5
        )
        assert _balance_score(inp) == 5.0


# ─── 9. TestBalanceScoreAggregate ─────────────────────────────────────────────

class TestBalanceScoreAggregate:
    def test_returns_float(self, base_input):
        assert isinstance(_balance_score(base_input), float)

    def test_score_clamped_0_100(self):
        inp = make_input(
            weighted_pipeline_eur=300_000.0, quota_eur=100_000.0,
            avg_account_health=100.0,
            accounts_with_qbr_pct=100.0,
            rep_quota_attainment_pct=200.0,
            white_space_accounts=0, total_accounts=100,
        )
        score = _balance_score(inp)
        assert 0.0 <= score <= 100.0

    def test_max_possible_score(self):
        inp = make_input(
            weighted_pipeline_eur=300_000.0, quota_eur=100_000.0,  # pc>=3 -> 30
            avg_account_health=100.0,  # 20
            accounts_with_qbr_pct=100.0,  # 15
            rep_quota_attainment_pct=100.0,  # 20
            white_space_accounts=0, total_accounts=100,  # ws=0 -> <=10 -> 15
        )
        score = _balance_score(inp)
        assert score == 100.0

    def test_minimum_possible_score(self):
        inp = make_input(
            weighted_pipeline_eur=0.0, quota_eur=100_000.0,
            avg_account_health=0.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=0.0,
            white_space_accounts=50, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 0.0

    def test_rounded_to_1dp(self, base_input):
        score = _balance_score(base_input)
        assert score == round(score, 1)

    def test_combined_partial_score(self):
        # pc>=2 (22) + health=50 (10) + qbr=0 (0) + attainment=75 (15) + ws=20% (10) = 57
        inp = make_input(
            weighted_pipeline_eur=200_000.0, quota_eur=100_000.0,
            avg_account_health=50.0,
            accounts_with_qbr_pct=0.0,
            rep_quota_attainment_pct=75.0,
            white_space_accounts=20, total_accounts=100,
        )
        score = _balance_score(inp)
        assert score == 57.0

    def test_quota_zero_no_crash(self):
        inp = make_input(quota_eur=0.0)
        score = _balance_score(inp)
        assert isinstance(score, float)
        assert score >= 0.0

    def test_total_accounts_zero_no_crash(self):
        inp = make_input(total_accounts=0, white_space_accounts=0)
        score = _balance_score(inp)
        assert isinstance(score, float)

    def test_base_input_is_high(self, base_input):
        # base_input: pc=3 (30) + health=75 (15) + qbr=70 (10.5) + att=100 (20) + ws=10% (15) = 90.5
        score = _balance_score(base_input)
        assert score >= 80.0


# ─── 10. TestTerritoryHealthThresholds ────────────────────────────────────────

class TestTerritoryHealthThresholds:
    def test_score_80_is_optimal(self):
        assert _territory_health(80.0) == TerritoryHealth.OPTIMAL

    def test_score_79_is_balanced(self):
        assert _territory_health(79.9) == TerritoryHealth.BALANCED

    def test_score_60_is_balanced(self):
        assert _territory_health(60.0) == TerritoryHealth.BALANCED

    def test_score_59_is_imbalanced(self):
        assert _territory_health(59.9) == TerritoryHealth.IMBALANCED

    def test_score_35_is_imbalanced(self):
        assert _territory_health(35.0) == TerritoryHealth.IMBALANCED

    def test_score_34_is_critical(self):
        assert _territory_health(34.9) == TerritoryHealth.CRITICAL

    def test_score_100_is_optimal(self):
        assert _territory_health(100.0) == TerritoryHealth.OPTIMAL

    def test_score_0_is_critical(self):
        assert _territory_health(0.0) == TerritoryHealth.CRITICAL

    def test_score_81_is_optimal(self):
        assert _territory_health(81.0) == TerritoryHealth.OPTIMAL

    def test_score_61_is_balanced(self):
        assert _territory_health(61.0) == TerritoryHealth.BALANCED

    def test_score_36_is_imbalanced(self):
        assert _territory_health(36.0) == TerritoryHealth.IMBALANCED

    def test_return_type_is_enum(self):
        result = _territory_health(50.0)
        assert isinstance(result, TerritoryHealth)


# ─── 11. TestCoverageRiskCalculation ──────────────────────────────────────────

class TestCoverageRiskCalculation:
    def _make_low_risk_input(self) -> TerritoryInput:
        """risk_score = 0 -> LOW"""
        return make_input(
            white_space_accounts=10, total_accounts=100,  # ws=10% -> <=25 -> no pts
            accounts_at_risk_count=0,  # <=2 -> no pts
            accounts_with_qbr_pct=80.0,  # >=50 -> no pts
            rep_ramp_complete=True,  # ramped -> no pts
        )

    def test_all_good_is_low(self):
        inp = self._make_low_risk_input()
        assert _coverage_risk(inp, _white_space_pct(inp)) == CoverageRisk.LOW

    def test_risk_score_0_is_low(self):
        inp = self._make_low_risk_input()
        assert _coverage_risk(inp, 10.0) == CoverageRisk.LOW

    def test_risk_score_1_is_medium(self):
        # ws>25 -> +1, rest clean
        inp = make_input(
            white_space_accounts=30, total_accounts=100,  # ws=30% -> >25 -> +1
            accounts_at_risk_count=0,
            accounts_with_qbr_pct=80.0,
            rep_ramp_complete=True,
        )
        assert _coverage_risk(inp, 30.0) == CoverageRisk.MEDIUM

    def test_risk_score_2_is_medium(self):
        # ws>25 (+1) + at_risk=3..5 (+1) = 2
        inp = make_input(
            accounts_at_risk_count=3,
            accounts_with_qbr_pct=80.0,
            rep_ramp_complete=True,
        )
        assert _coverage_risk(inp, 30.0) == CoverageRisk.MEDIUM

    def test_risk_score_3_is_high(self):
        # ws>40 (+2) + at_risk=3..5 (+1) = 3
        inp = make_input(
            accounts_at_risk_count=3,
            accounts_with_qbr_pct=80.0,
            rep_ramp_complete=True,
        )
        assert _coverage_risk(inp, 45.0) == CoverageRisk.HIGH

    def test_risk_score_4_is_high(self):
        # ws>40 (+2) + at_risk>5 (+2) = 4 -> HIGH
        inp = make_input(
            accounts_at_risk_count=6,
            accounts_with_qbr_pct=80.0,
            rep_ramp_complete=True,
        )
        assert _coverage_risk(inp, 45.0) == CoverageRisk.HIGH

    def test_risk_score_5_is_critical(self):
        # ws>40 (+2) + at_risk>5 (+2) + qbr<30 (+2) would be 6, but let's use 5
        # ws>40 (+2) + at_risk>2 (+1) + not_ramp (+2) = 5
        inp = make_input(
            accounts_at_risk_count=3,
            accounts_with_qbr_pct=60.0,  # >=50 -> 0pts
            rep_ramp_complete=False,  # +2
        )
        assert _coverage_risk(inp, 45.0) == CoverageRisk.CRITICAL

    def test_risk_score_6_is_critical(self):
        # ws>40(+2) + at_risk>5(+2) + not_ramp(+2) = 6
        inp = make_input(
            accounts_at_risk_count=6,
            accounts_with_qbr_pct=60.0,
            rep_ramp_complete=False,
        )
        assert _coverage_risk(inp, 45.0) == CoverageRisk.CRITICAL

    def test_ws_gt_40_adds_2(self):
        inp = make_input(
            accounts_at_risk_count=0,
            accounts_with_qbr_pct=80.0,
            rep_ramp_complete=True,
        )
        # ws=41 -> +2 -> MEDIUM (score=2)
        assert _coverage_risk(inp, 41.0) == CoverageRisk.MEDIUM

    def test_ws_gt_25_lte_40_adds_1(self):
        inp = make_input(
            accounts_at_risk_count=0,
            accounts_with_qbr_pct=80.0,
            rep_ramp_complete=True,
        )
        # ws=26 -> +1 -> MEDIUM (score=1)
        assert _coverage_risk(inp, 26.0) == CoverageRisk.MEDIUM

    def test_ws_lte_25_adds_0(self):
        inp = make_input(
            accounts_at_risk_count=0,
            accounts_with_qbr_pct=80.0,
            rep_ramp_complete=True,
        )
        # ws=25 -> no pts
        assert _coverage_risk(inp, 25.0) == CoverageRisk.LOW

    def test_at_risk_gt_5_adds_2(self):
        inp = make_input(
            accounts_at_risk_count=6,
            accounts_with_qbr_pct=80.0,
            rep_ramp_complete=True,
        )
        assert _coverage_risk(inp, 10.0) == CoverageRisk.MEDIUM

    def test_at_risk_gt_2_lte_5_adds_1(self):
        inp = make_input(
            accounts_at_risk_count=3,
            accounts_with_qbr_pct=80.0,
            rep_ramp_complete=True,
        )
        assert _coverage_risk(inp, 10.0) == CoverageRisk.MEDIUM

    def test_at_risk_lte_2_adds_0(self):
        inp = make_input(
            accounts_at_risk_count=2,
            accounts_with_qbr_pct=80.0,
            rep_ramp_complete=True,
        )
        assert _coverage_risk(inp, 10.0) == CoverageRisk.LOW

    def test_qbr_lt_30_adds_2(self):
        inp = make_input(
            accounts_at_risk_count=0,
            accounts_with_qbr_pct=29.0,
            rep_ramp_complete=True,
        )
        assert _coverage_risk(inp, 10.0) == CoverageRisk.MEDIUM

    def test_qbr_lt_50_gte_30_adds_1(self):
        inp = make_input(
            accounts_at_risk_count=0,
            accounts_with_qbr_pct=40.0,
            rep_ramp_complete=True,
        )
        assert _coverage_risk(inp, 10.0) == CoverageRisk.MEDIUM

    def test_qbr_gte_50_adds_0(self):
        inp = make_input(
            accounts_at_risk_count=0,
            accounts_with_qbr_pct=50.0,
            rep_ramp_complete=True,
        )
        assert _coverage_risk(inp, 10.0) == CoverageRisk.LOW

    def test_not_ramp_adds_2(self):
        inp = make_input(
            accounts_at_risk_count=0,
            accounts_with_qbr_pct=80.0,
            rep_ramp_complete=False,
        )
        assert _coverage_risk(inp, 10.0) == CoverageRisk.MEDIUM

    def test_returns_coverage_risk_enum(self, base_input):
        result = _coverage_risk(base_input, _white_space_pct(base_input))
        assert isinstance(result, CoverageRisk)


# ─── 12. TestTerritoryActionMaintain ──────────────────────────────────────────

class TestTerritoryActionMaintain:
    def test_optimal_low_returns_maintain(self):
        inp = make_input(
            total_accounts=50,
            weighted_pipeline_eur=300_000.0, quota_eur=100_000.0,
        )
        action = _territory_action(inp, TerritoryHealth.OPTIMAL, CoverageRisk.LOW, 3.0, 10.0)
        assert action == TerritoryAction.MAINTAIN

    def test_balanced_low_risk_not_overridden_returns_maintain(self):
        # BALANCED + LOW -> falls to default MAINTAIN (not REBALANCE)
        inp = make_input(
            total_accounts=50,
            weighted_pipeline_eur=300_000.0, quota_eur=100_000.0,
        )
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.LOW, 3.0, 10.0)
        assert action == TerritoryAction.MAINTAIN

    def test_default_fallback_is_maintain(self):
        inp = make_input(total_accounts=50, quota_eur=300_000.0)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.MEDIUM, 2.5, 15.0)
        assert action == TerritoryAction.MAINTAIN


# ─── 13. TestTerritoryActionSplit ─────────────────────────────────────────────

class TestTerritoryActionSplit:
    def test_accounts_gt_150_pc_lt_2_returns_split(self):
        inp = make_input(total_accounts=151, weighted_pipeline_eur=150_000.0, quota_eur=100_000.0)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.MEDIUM, 1.5, 10.0)
        assert action == TerritoryAction.SPLIT

    def test_accounts_200_pc_0_returns_split(self):
        inp = make_input(total_accounts=200, weighted_pipeline_eur=0.0, quota_eur=100_000.0)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.LOW, 0.0, 10.0)
        assert action == TerritoryAction.SPLIT

    def test_accounts_gt_150_pc_gte_2_no_split(self):
        inp = make_input(total_accounts=200)
        action = _territory_action(inp, TerritoryHealth.OPTIMAL, CoverageRisk.LOW, 2.0, 5.0)
        # OPTIMAL + LOW -> MAINTAIN takes priority before SPLIT check
        assert action == TerritoryAction.MAINTAIN

    def test_accounts_exactly_150_not_split(self):
        inp = make_input(total_accounts=150)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.MEDIUM, 1.5, 10.0)
        # 150 is not >150
        assert action != TerritoryAction.SPLIT


# ─── 14. TestTerritoryActionHire ──────────────────────────────────────────────

class TestTerritoryActionHire:
    def test_accounts_gt_100_critical_coverage_returns_hire(self):
        inp = make_input(total_accounts=101)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.CRITICAL, 2.5, 10.0)
        assert action == TerritoryAction.HIRE

    def test_accounts_gt_100_critical_health_returns_hire(self):
        inp = make_input(total_accounts=101)
        action = _territory_action(inp, TerritoryHealth.CRITICAL, CoverageRisk.LOW, 2.5, 10.0)
        assert action == TerritoryAction.HIRE

    def test_accounts_lte_100_critical_coverage_no_hire(self):
        inp = make_input(total_accounts=100)
        action = _territory_action(inp, TerritoryHealth.CRITICAL, CoverageRisk.CRITICAL, 0.5, 50.0)
        # 100 is not >100, health is CRITICAL -> REBALANCE
        assert action == TerritoryAction.REBALANCE

    def test_accounts_gt_100_high_coverage_no_hire(self):
        inp = make_input(total_accounts=150)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.HIGH, 2.5, 10.0)
        # pc>=2 so SPLIT not triggered; no CRITICAL -> no HIRE; BALANCED+HIGH -> REBALANCE
        assert action == TerritoryAction.REBALANCE

    def test_accounts_150_critical_coverage_returns_hire(self):
        inp = make_input(total_accounts=151, weighted_pipeline_eur=200_000.0, quota_eur=100_000.0)
        # accounts>150 AND pc<2 -> SPLIT checked first
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.CRITICAL, 1.9, 10.0)
        # pc<2 AND accounts>150 -> SPLIT takes priority over HIRE
        assert action == TerritoryAction.SPLIT


# ─── 15. TestTerritoryActionRebalance ─────────────────────────────────────────

class TestTerritoryActionRebalance:
    def test_critical_health_returns_rebalance(self):
        inp = make_input(total_accounts=50)
        action = _territory_action(inp, TerritoryHealth.CRITICAL, CoverageRisk.LOW, 2.5, 10.0)
        assert action == TerritoryAction.REBALANCE

    def test_imbalanced_health_returns_rebalance(self):
        inp = make_input(total_accounts=50)
        action = _territory_action(inp, TerritoryHealth.IMBALANCED, CoverageRisk.LOW, 2.5, 10.0)
        assert action == TerritoryAction.REBALANCE

    def test_balanced_high_coverage_returns_rebalance(self):
        inp = make_input(total_accounts=50)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.HIGH, 2.5, 10.0)
        assert action == TerritoryAction.REBALANCE

    def test_balanced_critical_coverage_returns_rebalance(self):
        inp = make_input(total_accounts=50)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.CRITICAL, 2.5, 10.0)
        assert action == TerritoryAction.REBALANCE

    def test_imbalanced_low_coverage_rebalance(self):
        inp = make_input(total_accounts=50)
        action = _territory_action(inp, TerritoryHealth.IMBALANCED, CoverageRisk.LOW, 0.5, 10.0)
        assert action == TerritoryAction.REBALANCE

    def test_balanced_medium_coverage_no_rebalance(self):
        inp = make_input(total_accounts=50)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.MEDIUM, 2.5, 10.0)
        assert action == TerritoryAction.MAINTAIN


# ─── 16. TestTerritoryActionMerge ─────────────────────────────────────────────

class TestTerritoryActionMerge:
    def test_small_territory_low_quota_returns_merge(self):
        inp = make_input(total_accounts=10, quota_eur=100_000.0)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.LOW, 2.5, 5.0)
        assert action == TerritoryAction.MERGE

    def test_accounts_exactly_19(self):
        inp = make_input(total_accounts=19, quota_eur=100_000.0)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.LOW, 2.5, 5.0)
        assert action == TerritoryAction.MERGE

    def test_accounts_exactly_20_no_merge(self):
        inp = make_input(total_accounts=20, quota_eur=100_000.0)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.LOW, 2.5, 5.0)
        # 20 is not <20 -> MAINTAIN
        assert action == TerritoryAction.MAINTAIN

    def test_quota_exactly_199999_merge(self):
        inp = make_input(total_accounts=10, quota_eur=199_999.0)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.LOW, 2.5, 5.0)
        assert action == TerritoryAction.MERGE

    def test_quota_exactly_200000_no_merge(self):
        inp = make_input(total_accounts=10, quota_eur=200_000.0)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.LOW, 2.5, 5.0)
        # quota not <200000 -> MAINTAIN
        assert action == TerritoryAction.MAINTAIN

    def test_small_accounts_high_quota_no_merge(self):
        inp = make_input(total_accounts=5, quota_eur=500_000.0)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.LOW, 2.5, 5.0)
        assert action == TerritoryAction.MAINTAIN

    def test_large_accounts_low_quota_no_merge(self):
        inp = make_input(total_accounts=50, quota_eur=50_000.0)
        action = _territory_action(inp, TerritoryHealth.BALANCED, CoverageRisk.LOW, 2.5, 5.0)
        assert action == TerritoryAction.MAINTAIN


# ─── 17. TestBuildStrengths ───────────────────────────────────────────────────

class TestBuildStrengths:
    def test_excellent_pipeline_coverage(self):
        inp = make_input(
            weighted_pipeline_eur=300_000.0, quota_eur=100_000.0,
            rep_quota_attainment_pct=0.0,
            avg_account_health=0.0,
            white_space_accounts=50, total_accounts=100,
            accounts_with_qbr_pct=0.0,
            market_penetration_pct=0.0,
            rep_tenure_months=0,
        )
        strengths = _build_strengths(inp, 3.0, 50.0)
        assert any("Couverture pipeline excellente" in s for s in strengths)

    def test_good_pipeline_coverage(self):
        inp = make_input(
            weighted_pipeline_eur=200_000.0, quota_eur=100_000.0,
            rep_quota_attainment_pct=0.0,
            avg_account_health=0.0,
            white_space_accounts=50, total_accounts=100,
            accounts_with_qbr_pct=0.0,
            market_penetration_pct=0.0,
            rep_tenure_months=0,
        )
        strengths = _build_strengths(inp, 2.0, 50.0)
        assert any("Bonne couverture pipeline" in s for s in strengths)

    def test_quota_attainment_100_pct(self):
        inp = make_input(rep_quota_attainment_pct=100.0, avg_account_health=0.0,
                         accounts_with_qbr_pct=0.0, market_penetration_pct=0.0, rep_tenure_months=0,
                         white_space_accounts=50, total_accounts=100)
        strengths = _build_strengths(inp, 0.0, 50.0)
        assert any("Atteinte quota" in s for s in strengths)

    def test_quota_attainment_75_pct(self):
        inp = make_input(rep_quota_attainment_pct=75.0, avg_account_health=0.0,
                         accounts_with_qbr_pct=0.0, market_penetration_pct=0.0, rep_tenure_months=0,
                         white_space_accounts=50, total_accounts=100)
        strengths = _build_strengths(inp, 0.0, 50.0)
        assert any("Progression quota solide" in s for s in strengths)

    def test_high_account_health(self):
        inp = make_input(avg_account_health=70.0, rep_quota_attainment_pct=0.0,
                         accounts_with_qbr_pct=0.0, market_penetration_pct=0.0, rep_tenure_months=0,
                         white_space_accounts=50, total_accounts=100)
        strengths = _build_strengths(inp, 0.0, 50.0)
        assert any("Santé comptes élevée" in s for s in strengths)

    def test_low_white_space_trigger(self):
        inp = make_input(avg_account_health=0.0, rep_quota_attainment_pct=0.0,
                         accounts_with_qbr_pct=0.0, market_penetration_pct=0.0, rep_tenure_months=0)
        strengths = _build_strengths(inp, 0.0, 15.0)  # ws=15 -> <=15
        assert any("Excellent taux de pénétration" in s for s in strengths)

    def test_high_qbr_coverage(self):
        inp = make_input(accounts_with_qbr_pct=70.0, avg_account_health=0.0,
                         rep_quota_attainment_pct=0.0, market_penetration_pct=0.0, rep_tenure_months=0,
                         white_space_accounts=50, total_accounts=100)
        strengths = _build_strengths(inp, 0.0, 50.0)
        assert any("Cadence QBR forte" in s for s in strengths)

    def test_high_market_penetration(self):
        inp = make_input(market_penetration_pct=40.0, avg_account_health=0.0,
                         rep_quota_attainment_pct=0.0, accounts_with_qbr_pct=0.0, rep_tenure_months=0,
                         white_space_accounts=50, total_accounts=100)
        strengths = _build_strengths(inp, 0.0, 50.0)
        assert any("Pénétration marché significative" in s for s in strengths)

    def test_experienced_rep(self):
        inp = make_input(rep_tenure_months=18, avg_account_health=0.0,
                         rep_quota_attainment_pct=0.0, accounts_with_qbr_pct=0.0,
                         market_penetration_pct=0.0, white_space_accounts=50, total_accounts=100)
        strengths = _build_strengths(inp, 0.0, 50.0)
        assert any("Rep expérimenté" in s for s in strengths)

    def test_no_strength_returns_empty_list(self):
        inp = make_input(
            avg_account_health=0.0, rep_quota_attainment_pct=0.0,
            accounts_with_qbr_pct=0.0, market_penetration_pct=0.0,
            rep_tenure_months=0, white_space_accounts=50, total_accounts=100
        )
        strengths = _build_strengths(inp, 0.0, 50.0)
        assert strengths == []

    def test_returns_list(self, base_input):
        ws = _white_space_pct(base_input)
        pc = _pipeline_coverage(base_input)
        assert isinstance(_build_strengths(base_input, pc, ws), list)

    def test_pc_exactly_2_is_good_not_excellent(self):
        inp = make_input()
        strengths = _build_strengths(inp, 2.0, 50.0)
        assert any("Bonne couverture pipeline" in s for s in strengths)
        assert not any("excellente" in s for s in strengths)

    def test_tenure_exactly_18(self):
        inp = make_input(rep_tenure_months=18, avg_account_health=0.0,
                         rep_quota_attainment_pct=0.0, accounts_with_qbr_pct=0.0,
                         market_penetration_pct=0.0, white_space_accounts=50, total_accounts=100)
        strengths = _build_strengths(inp, 0.0, 50.0)
        assert any("Rep expérimenté" in s for s in strengths)

    def test_tenure_17_no_exp_strength(self):
        inp = make_input(rep_tenure_months=17, avg_account_health=0.0,
                         rep_quota_attainment_pct=0.0, accounts_with_qbr_pct=0.0,
                         market_penetration_pct=0.0, white_space_accounts=50, total_accounts=100)
        strengths = _build_strengths(inp, 0.0, 50.0)
        assert not any("Rep expérimenté" in s for s in strengths)


# ─── 18. TestBuildGaps ────────────────────────────────────────────────────────

class TestBuildGaps:
    def _no_gap_input(self) -> TerritoryInput:
        return make_input(
            weighted_pipeline_eur=300_000.0, quota_eur=100_000.0,  # pc=3
            white_space_accounts=10, total_accounts=100,  # ws=10%
            accounts_with_qbr_pct=70.0,
            accounts_at_risk_count=1,
            rep_quota_attainment_pct=80.0,
            rep_ramp_complete=True,
            market_penetration_pct=30.0,
            competitive_intensity=50.0,
        )

    def test_low_pipeline_gap(self):
        inp = make_input(weighted_pipeline_eur=100_000.0, quota_eur=100_000.0)  # pc=1.0 <1.5
        gaps = _build_gaps(inp, 1.0, 10.0, TerritoryHealth.BALANCED)
        assert any("Pipeline insuffisant" in g for g in gaps)

    def test_high_white_space_gap(self):
        inp = make_input(white_space_accounts=40, total_accounts=100)  # ws=40 >30
        gaps = _build_gaps(inp, 3.0, 40.0, TerritoryHealth.BALANCED)
        assert any("non couverts" in g for g in gaps)

    def test_low_qbr_gap(self):
        inp = make_input(accounts_with_qbr_pct=30.0)  # <40
        gaps = _build_gaps(inp, 3.0, 10.0, TerritoryHealth.BALANCED)
        assert any("Cadence QBR faible" in g for g in gaps)

    def test_accounts_at_risk_gap(self):
        inp = make_input(accounts_at_risk_count=4)  # >3
        gaps = _build_gaps(inp, 3.0, 10.0, TerritoryHealth.BALANCED)
        assert any("à risque" in g for g in gaps)

    def test_low_quota_attainment_gap(self):
        inp = make_input(rep_quota_attainment_pct=40.0)  # <50
        gaps = _build_gaps(inp, 3.0, 10.0, TerritoryHealth.BALANCED)
        assert any("Atteinte quota" in g for g in gaps)

    def test_not_ramped_gap(self):
        inp = make_input(rep_ramp_complete=False)
        gaps = _build_gaps(inp, 3.0, 10.0, TerritoryHealth.BALANCED)
        assert any("ramp" in g for g in gaps)

    def test_low_market_penetration_gap(self):
        inp = make_input(market_penetration_pct=10.0)  # <15
        gaps = _build_gaps(inp, 3.0, 10.0, TerritoryHealth.BALANCED)
        assert any("Faible pénétration marché" in g for g in gaps)

    def test_high_competitive_intensity_gap(self):
        inp = make_input(competitive_intensity=71.0)  # >70
        gaps = _build_gaps(inp, 3.0, 10.0, TerritoryHealth.BALANCED)
        assert any("Pression concurrentielle" in g for g in gaps)

    def test_overloaded_territory_gap(self):
        inp = make_input(total_accounts=131)  # >130
        gaps = _build_gaps(inp, 3.0, 10.0, TerritoryHealth.BALANCED)
        assert any("surchargé" in g for g in gaps)

    def test_no_gaps_when_all_good(self):
        inp = self._no_gap_input()
        gaps = _build_gaps(inp, 3.0, 10.0, TerritoryHealth.OPTIMAL)
        assert gaps == []

    def test_returns_list(self, base_input):
        pc = _pipeline_coverage(base_input)
        ws = _white_space_pct(base_input)
        health = _territory_health(_balance_score(base_input))
        assert isinstance(_build_gaps(base_input, pc, ws, health), list)

    def test_pc_exactly_1_5_no_gap(self):
        # pc=1.5 is NOT <1.5
        inp = make_input()
        gaps = _build_gaps(inp, 1.5, 10.0, TerritoryHealth.BALANCED)
        assert not any("Pipeline insuffisant" in g for g in gaps)

    def test_at_risk_exactly_3_no_gap(self):
        # >3 triggers, so exactly 3 does NOT trigger
        inp = make_input(accounts_at_risk_count=3)
        gaps = _build_gaps(inp, 3.0, 10.0, TerritoryHealth.BALANCED)
        assert not any("à risque" in g for g in gaps)

    def test_ws_exactly_30_triggers_gap(self):
        # >30 triggers; 30.0 does NOT
        inp = make_input(white_space_accounts=30, total_accounts=100)
        gaps = _build_gaps(inp, 3.0, 30.0, TerritoryHealth.BALANCED)
        assert not any("non couverts" in g for g in gaps)

    def test_ws_31_triggers_gap(self):
        inp = make_input(white_space_accounts=31, total_accounts=100)
        gaps = _build_gaps(inp, 3.0, 31.0, TerritoryHealth.BALANCED)
        assert any("non couverts" in g for g in gaps)


# ─── 19. TestBuildRecommendations ─────────────────────────────────────────────

class TestBuildRecommendations:
    def test_split_action_recs(self):
        inp = make_input(total_accounts=200)
        recs = _build_recommendations(inp, TerritoryAction.SPLIT, 10.0, 3.0)
        assert any("Diviser" in r for r in recs)
        assert any("division" in r for r in recs)

    def test_hire_action_recs(self):
        inp = make_input()
        recs = _build_recommendations(inp, TerritoryAction.HIRE, 10.0, 3.0)
        assert any("Recruter" in r for r in recs)
        assert any("critères" in r for r in recs)

    def test_merge_action_recs(self):
        inp = make_input(total_accounts=10)
        recs = _build_recommendations(inp, TerritoryAction.MERGE, 5.0, 3.0)
        assert any("Fusionner" in r for r in recs)

    def test_rebalance_action_recs(self):
        inp = make_input()
        recs = _build_recommendations(inp, TerritoryAction.REBALANCE, 10.0, 3.0)
        assert any("Rebalancer" in r for r in recs)

    def test_rebalance_with_high_ws_adds_prospection(self):
        inp = make_input(white_space_accounts=30, total_accounts=100)
        recs = _build_recommendations(inp, TerritoryAction.REBALANCE, 30.0, 3.0)
        assert any("prospection" in r for r in recs)

    def test_rebalance_with_low_ws_no_prospection(self):
        inp = make_input(white_space_accounts=5, total_accounts=100)
        recs = _build_recommendations(inp, TerritoryAction.REBALANCE, 10.0, 3.0)
        assert not any("prospection" in r for r in recs)

    def test_low_pc_generates_pipeline_rec(self):
        inp = make_input()
        recs = _build_recommendations(inp, TerritoryAction.MAINTAIN, 10.0, 1.5)  # pc<2
        assert any("pipeline" in r.lower() for r in recs)

    def test_pc_gte_2_no_pipeline_rec(self):
        inp = make_input()
        recs = _build_recommendations(inp, TerritoryAction.MAINTAIN, 10.0, 2.0)
        assert not any("Accélérer la génération pipeline" in r for r in recs)

    def test_low_qbr_generates_qbr_rec(self):
        inp = make_input(accounts_with_qbr_pct=40.0)  # <50
        recs = _build_recommendations(inp, TerritoryAction.MAINTAIN, 10.0, 3.0)
        assert any("QBR" in r for r in recs)

    def test_qbr_gte_50_no_qbr_rec(self):
        inp = make_input(accounts_with_qbr_pct=50.0)
        recs = _build_recommendations(inp, TerritoryAction.MAINTAIN, 10.0, 3.0)
        assert not any("Planifier des QBRs" in r for r in recs)

    def test_accounts_at_risk_generates_cs_rec(self):
        inp = make_input(accounts_at_risk_count=3)  # >2
        recs = _build_recommendations(inp, TerritoryAction.MAINTAIN, 10.0, 3.0)
        assert any("CS" in r or "risque" in r for r in recs)

    def test_at_risk_lte_2_no_cs_rec(self):
        inp = make_input(accounts_at_risk_count=2)
        recs = _build_recommendations(inp, TerritoryAction.MAINTAIN, 10.0, 3.0)
        assert not any("Déployer une intervention CS" in r for r in recs)

    def test_low_market_penetration_with_tam_generates_tam_rec(self):
        inp = make_input(market_penetration_pct=10.0, tam_eur=1_000_000.0)  # <20, tam>0
        recs = _build_recommendations(inp, TerritoryAction.MAINTAIN, 10.0, 3.0)
        assert any("TAM" in r for r in recs)

    def test_low_market_penetration_no_tam_no_tam_rec(self):
        inp = make_input(market_penetration_pct=10.0, tam_eur=0.0)
        recs = _build_recommendations(inp, TerritoryAction.MAINTAIN, 10.0, 3.0)
        assert not any("Cartographier le TAM" in r for r in recs)

    def test_not_ramped_generates_ramp_rec(self):
        inp = make_input(rep_ramp_complete=False)
        recs = _build_recommendations(inp, TerritoryAction.MAINTAIN, 10.0, 3.0)
        assert any("ramp" in r.lower() for r in recs)

    def test_ramped_no_ramp_rec(self):
        inp = make_input(rep_ramp_complete=True)
        recs = _build_recommendations(inp, TerritoryAction.MAINTAIN, 10.0, 3.0)
        assert not any("Accélérer le ramp" in r for r in recs)

    def test_returns_list(self, base_input):
        assert isinstance(_build_recommendations(base_input, TerritoryAction.MAINTAIN, 10.0, 3.0), list)


# ─── 20. TestEngineAnalyze ────────────────────────────────────────────────────

class TestEngineAnalyze:
    def test_analyze_returns_result(self, engine, base_input):
        result = engine.analyze(base_input)
        assert isinstance(result, TerritoryResult)

    def test_analyze_stores_result(self, engine, base_input):
        engine.analyze(base_input)
        assert engine.get("T001") is not None

    def test_get_returns_none_for_unknown(self, engine):
        assert engine.get("UNKNOWN") is None

    def test_analyze_stores_by_territory_id(self, engine, base_input):
        result = engine.analyze(base_input)
        assert engine.get("T001") is result

    def test_analyze_overwrites_previous_result(self, engine, base_input):
        engine.analyze(base_input)
        modified = make_input(territory_id="T001", rep_name="New Rep")
        engine.analyze(modified)
        assert engine.get("T001").rep_name == "New Rep"

    def test_result_territory_id_matches_input(self, engine, base_input):
        result = engine.analyze(base_input)
        assert result.territory_id == base_input.territory_id

    def test_result_territory_name_matches_input(self, engine, base_input):
        result = engine.analyze(base_input)
        assert result.territory_name == base_input.territory_name

    def test_result_region_matches_input(self, engine, base_input):
        result = engine.analyze(base_input)
        assert result.region == base_input.region

    def test_result_rep_name_matches_input(self, engine, base_input):
        result = engine.analyze(base_input)
        assert result.rep_name == base_input.rep_name

    def test_result_balance_score_is_float(self, engine, base_input):
        result = engine.analyze(base_input)
        assert isinstance(result.balance_score, (int, float))

    def test_result_territory_health_is_enum(self, engine, base_input):
        result = engine.analyze(base_input)
        assert isinstance(result.territory_health, TerritoryHealth)

    def test_result_territory_action_is_enum(self, engine, base_input):
        result = engine.analyze(base_input)
        assert isinstance(result.territory_action, TerritoryAction)

    def test_result_coverage_risk_is_enum(self, engine, base_input):
        result = engine.analyze(base_input)
        assert isinstance(result.coverage_risk, CoverageRisk)

    def test_result_strengths_is_list(self, engine, base_input):
        result = engine.analyze(base_input)
        assert isinstance(result.strengths, list)

    def test_result_gaps_is_list(self, engine, base_input):
        result = engine.analyze(base_input)
        assert isinstance(result.gaps, list)

    def test_result_recommendations_is_list(self, engine, base_input):
        result = engine.analyze(base_input)
        assert isinstance(result.recommendations, list)

    def test_result_kpis_is_dict(self, engine, base_input):
        result = engine.analyze(base_input)
        assert isinstance(result.territory_kpis, dict)

    def test_kpis_has_pipeline_coverage(self, engine, base_input):
        result = engine.analyze(base_input)
        assert "pipeline_coverage_ratio" in result.territory_kpis

    def test_kpis_has_deals_in_flight(self, engine, base_input):
        result = engine.analyze(base_input)
        assert "deals_in_flight" in result.territory_kpis

    def test_kpis_has_closed_won_ytd(self, engine, base_input):
        result = engine.analyze(base_input)
        assert "closed_won_ytd_eur" in result.territory_kpis

    def test_quota_attainment_rounded_1dp(self, engine):
        inp = make_input(rep_quota_attainment_pct=99.999)
        result = engine.analyze(inp)
        assert result.quota_attainment_pct == round(99.999, 1)

    def test_critical_territory_fields(self, engine, critical_input):
        result = engine.analyze(critical_input)
        assert result.territory_health == TerritoryHealth.CRITICAL


# ─── 21. TestEngineBatchAndFilters ────────────────────────────────────────────

class TestEngineBatchAndFilters:
    def _batch_inputs(self):
        return [
            make_input(territory_id="T001", region="emea",
                       weighted_pipeline_eur=300_000.0, quota_eur=100_000.0,
                       avg_account_health=90.0, accounts_with_qbr_pct=90.0,
                       rep_quota_attainment_pct=120.0,
                       white_space_accounts=5, total_accounts=100),
            make_input(territory_id="T002", region="amer",
                       weighted_pipeline_eur=50_000.0, quota_eur=100_000.0,
                       avg_account_health=20.0, accounts_with_qbr_pct=10.0,
                       rep_quota_attainment_pct=20.0,
                       white_space_accounts=70, total_accounts=100,
                       accounts_at_risk_count=8, rep_ramp_complete=False),
            make_input(territory_id="T003", region="emea",
                       weighted_pipeline_eur=200_000.0, quota_eur=100_000.0,
                       avg_account_health=60.0, accounts_with_qbr_pct=60.0,
                       rep_quota_attainment_pct=80.0,
                       white_space_accounts=15, total_accounts=100),
        ]

    def test_batch_returns_list(self, engine):
        results = engine.analyze_batch(self._batch_inputs())
        assert isinstance(results, list)

    def test_batch_returns_all_results(self, engine):
        results = engine.analyze_batch(self._batch_inputs())
        assert len(results) == 3

    def test_batch_sorted_desc_by_balance_score(self, engine):
        results = engine.analyze_batch(self._batch_inputs())
        scores = [r.balance_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_batch_stores_all_results(self, engine):
        engine.analyze_batch(self._batch_inputs())
        assert engine.get("T001") is not None
        assert engine.get("T002") is not None
        assert engine.get("T003") is not None

    def test_all_territories_sorted_desc(self, engine):
        engine.analyze_batch(self._batch_inputs())
        results = engine.all_territories()
        scores = [r.balance_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_by_health_filters_correctly(self, engine):
        engine.analyze_batch(self._batch_inputs())
        all_results = engine.all_territories()
        for health in TerritoryHealth:
            filtered = engine.by_health(health)
            assert all(r.territory_health == health for r in filtered)

    def test_by_action_filters_correctly(self, engine):
        engine.analyze_batch(self._batch_inputs())
        for action in TerritoryAction:
            filtered = engine.by_action(action)
            assert all(r.territory_action == action for r in filtered)

    def test_by_region_emea(self, engine):
        engine.analyze_batch(self._batch_inputs())
        emea = engine.by_region("emea")
        assert all(r.region == "emea" for r in emea)

    def test_by_region_amer(self, engine):
        engine.analyze_batch(self._batch_inputs())
        amer = engine.by_region("amer")
        assert all(r.region == "amer" for r in amer)

    def test_by_region_empty_for_unknown(self, engine):
        engine.analyze_batch(self._batch_inputs())
        assert engine.by_region("apac") == []

    def test_needs_rebalance_only_rebalance_split_hire(self, engine):
        engine.analyze_batch(self._batch_inputs())
        for r in engine.needs_rebalance():
            assert r.territory_action in (TerritoryAction.REBALANCE, TerritoryAction.SPLIT, TerritoryAction.HIRE)

    def test_optimal_returns_only_optimal_health(self, engine):
        engine.analyze_batch(self._batch_inputs())
        for r in engine.optimal():
            assert r.territory_health == TerritoryHealth.OPTIMAL

    def test_critical_returns_only_critical_health(self, engine):
        engine.analyze_batch(self._batch_inputs())
        for r in engine.critical():
            assert r.territory_health == TerritoryHealth.CRITICAL

    def test_by_health_sorted_desc(self, engine):
        engine.analyze_batch(self._batch_inputs())
        results = engine.by_health(TerritoryHealth.OPTIMAL)
        scores = [r.balance_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_by_region_sorted_desc(self, engine):
        engine.analyze_batch(self._batch_inputs())
        results = engine.by_region("emea")
        scores = [r.balance_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_all_territories_length(self, engine):
        engine.analyze_batch(self._batch_inputs())
        assert len(engine.all_territories()) == 3


# ─── 22. TestEngineAggregates ─────────────────────────────────────────────────

class TestEngineAggregates:
    def _load_two(self, engine):
        inp1 = make_input(territory_id="T001", rep_quota_attainment_pct=100.0,
                          closed_won_ytd_eur=100_000.0)
        inp2 = make_input(territory_id="T002", rep_quota_attainment_pct=50.0,
                          closed_won_ytd_eur=50_000.0)
        engine.analyze(inp1)
        engine.analyze(inp2)

    def test_avg_balance_score_empty_returns_0(self, engine):
        assert engine.avg_balance_score() == 0.0

    def test_avg_balance_score_single(self, engine, base_input):
        r = engine.analyze(base_input)
        assert engine.avg_balance_score() == r.balance_score

    def test_avg_balance_score_multiple(self, engine):
        self._load_two(engine)
        vals = [r.balance_score for r in engine.all_territories()]
        expected = round(sum(vals) / len(vals), 1)
        assert engine.avg_balance_score() == expected

    def test_avg_balance_score_rounded_1dp(self, engine):
        self._load_two(engine)
        result = engine.avg_balance_score()
        assert result == round(result, 1)

    def test_avg_quota_attainment_empty_returns_0(self, engine):
        assert engine.avg_quota_attainment() == 0.0

    def test_avg_quota_attainment_single(self, engine, base_input):
        engine.analyze(base_input)
        assert engine.avg_quota_attainment() == round(base_input.rep_quota_attainment_pct, 1)

    def test_avg_quota_attainment_multiple(self, engine):
        self._load_two(engine)
        expected = round((100.0 + 50.0) / 2, 1)
        assert engine.avg_quota_attainment() == expected

    def test_avg_quota_attainment_rounded_1dp(self, engine):
        self._load_two(engine)
        result = engine.avg_quota_attainment()
        assert result == round(result, 1)

    def test_total_pipeline_eur_empty(self, engine):
        assert engine.total_pipeline_eur() == 0.0

    def test_total_pipeline_eur_sums_closed_won(self, engine):
        self._load_two(engine)
        assert engine.total_pipeline_eur() == round(100_000.0 + 50_000.0, 2)

    def test_total_pipeline_eur_single(self, engine):
        engine.analyze(make_input(territory_id="T001", closed_won_ytd_eur=77_777.77))
        assert engine.total_pipeline_eur() == 77_777.77

    def test_needs_rebalance_returns_list(self, engine, base_input):
        engine.analyze(base_input)
        result = engine.needs_rebalance()
        assert isinstance(result, list)

    def test_optimal_returns_list(self, engine, base_input):
        engine.analyze(base_input)
        assert isinstance(engine.optimal(), list)

    def test_critical_returns_list(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.critical(), list)

    def test_summary_empty_engine(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["health_counts"] == {}
        assert s["action_counts"] == {}
        assert s["risk_counts"] == {}
        assert s["avg_balance_score"] == 0.0
        assert s["avg_quota_attainment_pct"] == 0.0
        assert s["needs_rebalance_count"] == 0
        assert s["optimal_count"] == 0
        assert s["critical_count"] == 0

    def test_summary_keys(self, engine, base_input):
        engine.analyze(base_input)
        s = engine.summary()
        for key in [
            "total", "health_counts", "action_counts", "risk_counts",
            "avg_balance_score", "avg_quota_attainment_pct",
            "needs_rebalance_count", "optimal_count", "critical_count",
        ]:
            assert key in s

    def test_summary_total_count(self, engine):
        self._load_two(engine)
        assert engine.summary()["total"] == 2

    def test_summary_health_counts_sum(self, engine):
        self._load_two(engine)
        s = engine.summary()
        assert sum(s["health_counts"].values()) == 2

    def test_summary_action_counts_sum(self, engine):
        self._load_two(engine)
        s = engine.summary()
        assert sum(s["action_counts"].values()) == 2

    def test_summary_risk_counts_sum(self, engine):
        self._load_two(engine)
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == 2

    def test_summary_avg_balance_score_consistent(self, engine):
        self._load_two(engine)
        s = engine.summary()
        assert s["avg_balance_score"] == engine.avg_balance_score()

    def test_summary_avg_quota_consistent(self, engine):
        self._load_two(engine)
        s = engine.summary()
        assert s["avg_quota_attainment_pct"] == engine.avg_quota_attainment()

    def test_summary_needs_rebalance_count(self, engine):
        self._load_two(engine)
        s = engine.summary()
        assert s["needs_rebalance_count"] == len(engine.needs_rebalance())

    def test_summary_optimal_count(self, engine):
        self._load_two(engine)
        s = engine.summary()
        assert s["optimal_count"] == len(engine.optimal())

    def test_summary_critical_count(self, engine):
        self._load_two(engine)
        s = engine.summary()
        assert s["critical_count"] == len(engine.critical())

    def test_reset_clears_all(self, engine, base_input):
        engine.analyze(base_input)
        engine.reset()
        assert engine.all_territories() == []

    def test_reset_makes_get_return_none(self, engine, base_input):
        engine.analyze(base_input)
        engine.reset()
        assert engine.get("T001") is None

    def test_reset_zeroes_avg_balance_score(self, engine, base_input):
        engine.analyze(base_input)
        engine.reset()
        assert engine.avg_balance_score() == 0.0

    def test_reset_zeroes_avg_quota_attainment(self, engine, base_input):
        engine.analyze(base_input)
        engine.reset()
        assert engine.avg_quota_attainment() == 0.0

    def test_reset_zeroes_total_pipeline(self, engine, base_input):
        engine.analyze(base_input)
        engine.reset()
        assert engine.total_pipeline_eur() == 0.0

    def test_reset_summary_empty(self, engine, base_input):
        engine.analyze(base_input)
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_multiple_analyze_same_id_overwrite(self, engine):
        engine.analyze(make_input(territory_id="T001", rep_quota_attainment_pct=100.0))
        engine.analyze(make_input(territory_id="T001", rep_quota_attainment_pct=50.0))
        # only one result stored
        assert len(engine.all_territories()) == 1
        assert engine.get("T001").quota_attainment_pct == 50.0

    def test_fresh_engine_all_territories_empty(self, engine):
        assert engine.all_territories() == []

    def test_fresh_engine_needs_rebalance_empty(self, engine):
        assert engine.needs_rebalance() == []

    def test_fresh_engine_optimal_empty(self, engine):
        assert engine.optimal() == []

    def test_fresh_engine_critical_empty(self, engine):
        assert engine.critical() == []


# ─── Extra: TestTerritoryKPIs ──────────────────────────────────────────────────

class TestTerritoryKPIs:
    def test_returns_dict(self, base_input):
        pc = _pipeline_coverage(base_input)
        ws = _white_space_pct(base_input)
        assert isinstance(_territory_kpis(base_input, pc, ws), dict)

    def test_pipeline_coverage_ratio(self, base_input):
        pc = _pipeline_coverage(base_input)
        ws = _white_space_pct(base_input)
        kpis = _territory_kpis(base_input, pc, ws)
        assert kpis["pipeline_coverage_ratio"] == pc

    def test_quota_attainment_rounded(self, base_input):
        pc = _pipeline_coverage(base_input)
        ws = _white_space_pct(base_input)
        kpis = _territory_kpis(base_input, pc, ws)
        assert kpis["quota_attainment_pct"] == round(base_input.rep_quota_attainment_pct, 1)

    def test_white_space_pct(self, base_input):
        pc = _pipeline_coverage(base_input)
        ws = _white_space_pct(base_input)
        kpis = _territory_kpis(base_input, pc, ws)
        assert kpis["white_space_pct"] == ws

    def test_active_account_pct(self, base_input):
        pc = _pipeline_coverage(base_input)
        ws = _white_space_pct(base_input)
        kpis = _territory_kpis(base_input, pc, ws)
        expected = round(base_input.active_accounts / max(1, base_input.total_accounts) * 100, 1)
        assert kpis["active_account_pct"] == expected

    def test_deals_in_flight(self, base_input):
        pc = _pipeline_coverage(base_input)
        ws = _white_space_pct(base_input)
        kpis = _territory_kpis(base_input, pc, ws)
        assert kpis["deals_in_flight"] == base_input.deals_in_flight

    def test_accounts_at_risk(self, base_input):
        pc = _pipeline_coverage(base_input)
        ws = _white_space_pct(base_input)
        kpis = _territory_kpis(base_input, pc, ws)
        assert kpis["accounts_at_risk"] == base_input.accounts_at_risk_count

    def test_closed_won_ytd(self, base_input):
        pc = _pipeline_coverage(base_input)
        ws = _white_space_pct(base_input)
        kpis = _territory_kpis(base_input, pc, ws)
        assert kpis["closed_won_ytd_eur"] == base_input.closed_won_ytd_eur

    def test_active_account_pct_zero_total(self):
        inp = make_input(total_accounts=0, active_accounts=0)
        kpis = _territory_kpis(inp, 0.0, 0.0)
        assert kpis["active_account_pct"] == 0.0

    def test_market_penetration_pct(self, base_input):
        pc = _pipeline_coverage(base_input)
        ws = _white_space_pct(base_input)
        kpis = _territory_kpis(base_input, pc, ws)
        assert kpis["market_penetration_pct"] == round(base_input.market_penetration_pct, 1)

    def test_all_expected_keys(self, base_input):
        pc = _pipeline_coverage(base_input)
        ws = _white_space_pct(base_input)
        kpis = _territory_kpis(base_input, pc, ws)
        for k in [
            "pipeline_coverage_ratio", "quota_attainment_pct", "white_space_pct",
            "active_account_pct", "avg_account_health", "qbr_coverage_pct",
            "market_penetration_pct", "deals_in_flight", "accounts_at_risk",
            "closed_won_ytd_eur",
        ]:
            assert k in kpis, f"Missing KPI key: {k}"
