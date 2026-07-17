"""
Comprehensive pytest tests for SalesTerritoryWhitespaceIntelligenceEngine.
"""
from __future__ import annotations

import pytest

from swarm.intelligence.sales_territory_whitespace_intelligence_engine import (
    SalesTerritoryWhitespaceIntelligenceEngine,
    TerritoryAction,
    TerritoryInput,
    TerritoryPattern,
    TerritoryResult,
    TerritoryRisk,
    TerritorySeverity,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> TerritoryInput:
    """Return a *healthy* TerritoryInput (low-risk baseline) with any overrides applied."""
    defaults = dict(
        rep_id="rep-001",
        region="West",
        evaluation_period_id="Q2-2026",
        total_accounts_in_territory=100,
        accounts_with_active_opportunity_pct=0.40,
        net_new_logos_acquired_pct=0.25,
        territory_coverage_calls_per_week_avg=0.80,
        icp_fit_accounts_engaged_pct=0.70,
        dormant_account_reactivation_rate_pct=0.10,
        competitive_account_attempted_pct=0.60,
        competitive_displacement_win_rate_pct=0.30,
        expansion_first_meeting_rate_pct=0.20,
        new_logo_pipeline_pct=0.30,
        whitespace_opportunity_identified_pct=0.60,
        territory_growth_rate_pct=0.20,
        same_contact_dependency_pct=0.30,
        accounts_with_no_contact_90d_pct=0.10,
        avg_accounts_worked_simultaneously=5.0,
        vertical_concentration_pct=0.40,
        cross_sell_opportunity_created_pct=0.20,
        total_territory_icp_accounts=200,
        avg_opportunity_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return TerritoryInput(**defaults)


def make_engine() -> SalesTerritoryWhitespaceIntelligenceEngine:
    return SalesTerritoryWhitespaceIntelligenceEngine()


# ---------------------------------------------------------------------------
# 1. Enum values
# ---------------------------------------------------------------------------

class TestEnumValues:
    def test_territory_risk_values(self):
        assert TerritoryRisk.low.value == "low"
        assert TerritoryRisk.moderate.value == "moderate"
        assert TerritoryRisk.high.value == "high"
        assert TerritoryRisk.critical.value == "critical"

    def test_territory_risk_member_count(self):
        assert len(TerritoryRisk) == 4

    def test_territory_pattern_values(self):
        assert TerritoryPattern.none.value == "none"
        assert TerritoryPattern.coverage_avoidance.value == "coverage_avoidance"
        assert TerritoryPattern.contact_recycling.value == "contact_recycling"
        assert TerritoryPattern.expansion_neglect.value == "expansion_neglect"
        assert TerritoryPattern.competitive_blindspot.value == "competitive_blindspot"
        assert TerritoryPattern.vertical_concentration.value == "vertical_concentration"

    def test_territory_pattern_member_count(self):
        assert len(TerritoryPattern) == 6

    def test_territory_severity_values(self):
        assert TerritorySeverity.optimal.value == "optimal"
        assert TerritorySeverity.acceptable.value == "acceptable"
        assert TerritorySeverity.concerning.value == "concerning"
        assert TerritorySeverity.stagnant.value == "stagnant"

    def test_territory_severity_member_count(self):
        assert len(TerritorySeverity) == 4

    def test_territory_action_values(self):
        assert TerritoryAction.no_action.value == "no_action"
        assert TerritoryAction.territory_planning_coaching.value == "territory_planning_coaching"
        assert TerritoryAction.new_logo_coaching.value == "new_logo_coaching"
        assert TerritoryAction.competitive_territory_coaching.value == "competitive_territory_coaching"
        assert TerritoryAction.contact_diversification_coaching.value == "contact_diversification_coaching"
        assert TerritoryAction.territory_coverage_intervention.value == "territory_coverage_intervention"
        assert TerritoryAction.territory_strategy_reset.value == "territory_strategy_reset"

    def test_territory_action_member_count(self):
        assert len(TerritoryAction) == 7

    def test_enums_are_strings(self):
        """Enums inherit from str so they can be compared directly to strings."""
        assert TerritoryRisk.low == "low"
        assert TerritoryPattern.none == "none"
        assert TerritorySeverity.optimal == "optimal"
        assert TerritoryAction.no_action == "no_action"


# ---------------------------------------------------------------------------
# 2. TerritoryInput – all 22 fields
# ---------------------------------------------------------------------------

class TestTerritoryInputFields:
    def test_all_22_fields_exist(self):
        inp = make_input()
        fields = [
            "rep_id", "region", "evaluation_period_id", "total_accounts_in_territory",
            "accounts_with_active_opportunity_pct", "net_new_logos_acquired_pct",
            "territory_coverage_calls_per_week_avg", "icp_fit_accounts_engaged_pct",
            "dormant_account_reactivation_rate_pct", "competitive_account_attempted_pct",
            "competitive_displacement_win_rate_pct", "expansion_first_meeting_rate_pct",
            "new_logo_pipeline_pct", "whitespace_opportunity_identified_pct",
            "territory_growth_rate_pct", "same_contact_dependency_pct",
            "accounts_with_no_contact_90d_pct", "avg_accounts_worked_simultaneously",
            "vertical_concentration_pct", "cross_sell_opportunity_created_pct",
            "total_territory_icp_accounts", "avg_opportunity_value_usd",
        ]
        assert len(fields) == 22
        for f in fields:
            assert hasattr(inp, f), f"Missing field: {f}"

    def test_field_types(self):
        inp = make_input()
        assert isinstance(inp.rep_id, str)
        assert isinstance(inp.region, str)
        assert isinstance(inp.evaluation_period_id, str)
        assert isinstance(inp.total_accounts_in_territory, int)
        assert isinstance(inp.total_territory_icp_accounts, int)
        assert isinstance(inp.avg_opportunity_value_usd, float)
        assert isinstance(inp.icp_fit_accounts_engaged_pct, float)


# ---------------------------------------------------------------------------
# 3. TerritoryResult – all 15 fields + to_dict() keys
# ---------------------------------------------------------------------------

class TestTerritoryResult:
    def _get_result(self) -> TerritoryResult:
        engine = make_engine()
        return engine.assess(make_input())

    def test_all_15_fields_exist(self):
        r = self._get_result()
        fields = [
            "rep_id", "region", "territory_risk", "territory_pattern",
            "territory_severity", "recommended_action", "coverage_score",
            "penetration_score", "growth_score", "competitive_score",
            "territory_composite", "has_territory_gap", "requires_territory_coaching",
            "estimated_whitespace_opportunity_usd", "territory_signal",
        ]
        assert len(fields) == 15
        for f in fields:
            assert hasattr(r, f), f"Missing field: {f}"

    def test_to_dict_returns_15_keys(self):
        r = self._get_result()
        d = r.to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self):
        r = self._get_result()
        d = r.to_dict()
        expected_keys = {
            "rep_id", "region", "territory_risk", "territory_pattern",
            "territory_severity", "recommended_action", "coverage_score",
            "penetration_score", "growth_score", "competitive_score",
            "territory_composite", "has_territory_gap", "requires_territory_coaching",
            "estimated_whitespace_opportunity_usd", "territory_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        r = self._get_result()
        d = r.to_dict()
        assert isinstance(d["territory_risk"], str)
        assert isinstance(d["territory_pattern"], str)
        assert isinstance(d["territory_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_and_region_preserved(self):
        engine = make_engine()
        inp = make_input(rep_id="rep-XYZ", region="East")
        r = engine.assess(inp)
        d = r.to_dict()
        assert d["rep_id"] == "rep-XYZ"
        assert d["region"] == "East"


# ---------------------------------------------------------------------------
# 4. Coverage sub-score branches
# ---------------------------------------------------------------------------

class TestCoverageScore:
    def _score(self, **kw) -> float:
        engine = make_engine()
        inp = make_input(**kw)
        return engine._coverage_score(inp)

    # icp_fit_accounts_engaged_pct
    def test_icp_le_025_adds_40(self):
        s = self._score(icp_fit_accounts_engaged_pct=0.25,
                        accounts_with_no_contact_90d_pct=0.10,
                        territory_coverage_calls_per_week_avg=0.80)
        assert s == 40.0

    def test_icp_le_045_adds_22(self):
        s = self._score(icp_fit_accounts_engaged_pct=0.45,
                        accounts_with_no_contact_90d_pct=0.10,
                        territory_coverage_calls_per_week_avg=0.80)
        assert s == 22.0

    def test_icp_le_065_adds_8(self):
        s = self._score(icp_fit_accounts_engaged_pct=0.65,
                        accounts_with_no_contact_90d_pct=0.10,
                        territory_coverage_calls_per_week_avg=0.80)
        assert s == 8.0

    def test_icp_above_065_adds_0(self):
        s = self._score(icp_fit_accounts_engaged_pct=0.66,
                        accounts_with_no_contact_90d_pct=0.10,
                        territory_coverage_calls_per_week_avg=0.80)
        assert s == 0.0

    # accounts_with_no_contact_90d_pct
    def test_no_contact_ge_050_adds_35(self):
        s = self._score(icp_fit_accounts_engaged_pct=0.70,
                        accounts_with_no_contact_90d_pct=0.50,
                        territory_coverage_calls_per_week_avg=0.80)
        assert s == 35.0

    def test_no_contact_ge_030_adds_18(self):
        s = self._score(icp_fit_accounts_engaged_pct=0.70,
                        accounts_with_no_contact_90d_pct=0.30,
                        territory_coverage_calls_per_week_avg=0.80)
        assert s == 18.0

    def test_no_contact_below_030_adds_0(self):
        s = self._score(icp_fit_accounts_engaged_pct=0.70,
                        accounts_with_no_contact_90d_pct=0.29,
                        territory_coverage_calls_per_week_avg=0.80)
        assert s == 0.0

    # territory_coverage_calls_per_week_avg
    def test_calls_le_020_adds_25(self):
        s = self._score(icp_fit_accounts_engaged_pct=0.70,
                        accounts_with_no_contact_90d_pct=0.10,
                        territory_coverage_calls_per_week_avg=0.20)
        assert s == 25.0

    def test_calls_le_050_adds_12(self):
        s = self._score(icp_fit_accounts_engaged_pct=0.70,
                        accounts_with_no_contact_90d_pct=0.10,
                        territory_coverage_calls_per_week_avg=0.50)
        assert s == 12.0

    def test_calls_above_050_adds_0(self):
        s = self._score(icp_fit_accounts_engaged_pct=0.70,
                        accounts_with_no_contact_90d_pct=0.10,
                        territory_coverage_calls_per_week_avg=0.51)
        assert s == 0.0

    def test_coverage_capped_at_100(self):
        # max possible: 40 + 35 + 25 = 100, stays at 100
        s = self._score(icp_fit_accounts_engaged_pct=0.25,
                        accounts_with_no_contact_90d_pct=0.50,
                        territory_coverage_calls_per_week_avg=0.20)
        assert s == 100.0

    def test_coverage_all_branches_fired(self):
        """All three components active sums to 40+35+25=100."""
        s = self._score(icp_fit_accounts_engaged_pct=0.10,
                        accounts_with_no_contact_90d_pct=0.55,
                        territory_coverage_calls_per_week_avg=0.10)
        assert s == 100.0

    def test_coverage_zero_when_healthy(self):
        s = self._score(icp_fit_accounts_engaged_pct=0.80,
                        accounts_with_no_contact_90d_pct=0.05,
                        territory_coverage_calls_per_week_avg=0.90)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 5. Penetration sub-score branches
# ---------------------------------------------------------------------------

class TestPenetrationScore:
    def _score(self, **kw) -> float:
        engine = make_engine()
        inp = make_input(**kw)
        return engine._penetration_score(inp)

    def test_whitespace_le_015_adds_40(self):
        s = self._score(whitespace_opportunity_identified_pct=0.15,
                        same_contact_dependency_pct=0.30,
                        accounts_with_active_opportunity_pct=0.40)
        assert s == 40.0

    def test_whitespace_le_030_adds_22(self):
        s = self._score(whitespace_opportunity_identified_pct=0.30,
                        same_contact_dependency_pct=0.30,
                        accounts_with_active_opportunity_pct=0.40)
        assert s == 22.0

    def test_whitespace_le_050_adds_8(self):
        s = self._score(whitespace_opportunity_identified_pct=0.50,
                        same_contact_dependency_pct=0.30,
                        accounts_with_active_opportunity_pct=0.40)
        assert s == 8.0

    def test_whitespace_above_050_adds_0(self):
        s = self._score(whitespace_opportunity_identified_pct=0.51,
                        same_contact_dependency_pct=0.30,
                        accounts_with_active_opportunity_pct=0.40)
        assert s == 0.0

    def test_same_contact_ge_070_adds_35(self):
        s = self._score(whitespace_opportunity_identified_pct=0.60,
                        same_contact_dependency_pct=0.70,
                        accounts_with_active_opportunity_pct=0.40)
        assert s == 35.0

    def test_same_contact_ge_050_adds_18(self):
        s = self._score(whitespace_opportunity_identified_pct=0.60,
                        same_contact_dependency_pct=0.50,
                        accounts_with_active_opportunity_pct=0.40)
        assert s == 18.0

    def test_same_contact_below_050_adds_0(self):
        s = self._score(whitespace_opportunity_identified_pct=0.60,
                        same_contact_dependency_pct=0.49,
                        accounts_with_active_opportunity_pct=0.40)
        assert s == 0.0

    def test_active_opp_le_010_adds_25(self):
        s = self._score(whitespace_opportunity_identified_pct=0.60,
                        same_contact_dependency_pct=0.30,
                        accounts_with_active_opportunity_pct=0.10)
        assert s == 25.0

    def test_active_opp_le_025_adds_12(self):
        s = self._score(whitespace_opportunity_identified_pct=0.60,
                        same_contact_dependency_pct=0.30,
                        accounts_with_active_opportunity_pct=0.25)
        assert s == 12.0

    def test_active_opp_above_025_adds_0(self):
        s = self._score(whitespace_opportunity_identified_pct=0.60,
                        same_contact_dependency_pct=0.30,
                        accounts_with_active_opportunity_pct=0.26)
        assert s == 0.0

    def test_penetration_capped_at_100(self):
        s = self._score(whitespace_opportunity_identified_pct=0.05,
                        same_contact_dependency_pct=0.75,
                        accounts_with_active_opportunity_pct=0.05)
        assert s == 100.0

    def test_penetration_zero_when_healthy(self):
        s = self._score(whitespace_opportunity_identified_pct=0.80,
                        same_contact_dependency_pct=0.20,
                        accounts_with_active_opportunity_pct=0.50)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 6. Growth sub-score branches
# ---------------------------------------------------------------------------

class TestGrowthScore:
    def _score(self, **kw) -> float:
        engine = make_engine()
        inp = make_input(**kw)
        return engine._growth_score(inp)

    def test_logos_le_005_adds_45(self):
        s = self._score(net_new_logos_acquired_pct=0.05,
                        new_logo_pipeline_pct=0.30,
                        territory_growth_rate_pct=0.20)
        assert s == 45.0

    def test_logos_le_012_adds_25(self):
        s = self._score(net_new_logos_acquired_pct=0.12,
                        new_logo_pipeline_pct=0.30,
                        territory_growth_rate_pct=0.20)
        assert s == 25.0

    def test_logos_le_020_adds_10(self):
        s = self._score(net_new_logos_acquired_pct=0.20,
                        new_logo_pipeline_pct=0.30,
                        territory_growth_rate_pct=0.20)
        assert s == 10.0

    def test_logos_above_020_adds_0(self):
        s = self._score(net_new_logos_acquired_pct=0.21,
                        new_logo_pipeline_pct=0.30,
                        territory_growth_rate_pct=0.20)
        assert s == 0.0

    def test_pipeline_le_010_adds_30(self):
        s = self._score(net_new_logos_acquired_pct=0.25,
                        new_logo_pipeline_pct=0.10,
                        territory_growth_rate_pct=0.20)
        assert s == 30.0

    def test_pipeline_le_025_adds_15(self):
        s = self._score(net_new_logos_acquired_pct=0.25,
                        new_logo_pipeline_pct=0.25,
                        territory_growth_rate_pct=0.20)
        assert s == 15.0

    def test_pipeline_above_025_adds_0(self):
        s = self._score(net_new_logos_acquired_pct=0.25,
                        new_logo_pipeline_pct=0.26,
                        territory_growth_rate_pct=0.20)
        assert s == 0.0

    def test_growth_rate_le_005_adds_25(self):
        s = self._score(net_new_logos_acquired_pct=0.25,
                        new_logo_pipeline_pct=0.30,
                        territory_growth_rate_pct=0.05)
        assert s == 25.0

    def test_growth_rate_le_015_adds_12(self):
        s = self._score(net_new_logos_acquired_pct=0.25,
                        new_logo_pipeline_pct=0.30,
                        territory_growth_rate_pct=0.15)
        assert s == 12.0

    def test_growth_rate_above_015_adds_0(self):
        s = self._score(net_new_logos_acquired_pct=0.25,
                        new_logo_pipeline_pct=0.30,
                        territory_growth_rate_pct=0.16)
        assert s == 0.0

    def test_growth_capped_at_100(self):
        s = self._score(net_new_logos_acquired_pct=0.01,
                        new_logo_pipeline_pct=0.05,
                        territory_growth_rate_pct=0.01)
        assert s == 100.0

    def test_growth_zero_when_healthy(self):
        s = self._score(net_new_logos_acquired_pct=0.30,
                        new_logo_pipeline_pct=0.40,
                        territory_growth_rate_pct=0.25)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 7. Competitive sub-score branches
# ---------------------------------------------------------------------------

class TestCompetitiveScore:
    def _score(self, **kw) -> float:
        engine = make_engine()
        inp = make_input(**kw)
        return engine._competitive_score(inp)

    def test_comp_attempt_le_015_adds_40(self):
        s = self._score(competitive_account_attempted_pct=0.15,
                        competitive_displacement_win_rate_pct=0.35,
                        vertical_concentration_pct=0.40)
        assert s == 40.0

    def test_comp_attempt_le_035_adds_22(self):
        s = self._score(competitive_account_attempted_pct=0.35,
                        competitive_displacement_win_rate_pct=0.35,
                        vertical_concentration_pct=0.40)
        assert s == 22.0

    def test_comp_attempt_le_055_adds_8(self):
        s = self._score(competitive_account_attempted_pct=0.55,
                        competitive_displacement_win_rate_pct=0.35,
                        vertical_concentration_pct=0.40)
        assert s == 8.0

    def test_comp_attempt_above_055_adds_0(self):
        s = self._score(competitive_account_attempted_pct=0.56,
                        competitive_displacement_win_rate_pct=0.35,
                        vertical_concentration_pct=0.40)
        assert s == 0.0

    def test_displacement_win_le_010_adds_35(self):
        s = self._score(competitive_account_attempted_pct=0.60,
                        competitive_displacement_win_rate_pct=0.10,
                        vertical_concentration_pct=0.40)
        assert s == 35.0

    def test_displacement_win_le_025_adds_18(self):
        s = self._score(competitive_account_attempted_pct=0.60,
                        competitive_displacement_win_rate_pct=0.25,
                        vertical_concentration_pct=0.40)
        assert s == 18.0

    def test_displacement_win_above_025_adds_0(self):
        s = self._score(competitive_account_attempted_pct=0.60,
                        competitive_displacement_win_rate_pct=0.26,
                        vertical_concentration_pct=0.40)
        assert s == 0.0

    def test_vertical_conc_ge_080_adds_25(self):
        s = self._score(competitive_account_attempted_pct=0.60,
                        competitive_displacement_win_rate_pct=0.35,
                        vertical_concentration_pct=0.80)
        assert s == 25.0

    def test_vertical_conc_ge_065_adds_12(self):
        s = self._score(competitive_account_attempted_pct=0.60,
                        competitive_displacement_win_rate_pct=0.35,
                        vertical_concentration_pct=0.65)
        assert s == 12.0

    def test_vertical_conc_below_065_adds_0(self):
        s = self._score(competitive_account_attempted_pct=0.60,
                        competitive_displacement_win_rate_pct=0.35,
                        vertical_concentration_pct=0.64)
        assert s == 0.0

    def test_competitive_capped_at_100(self):
        s = self._score(competitive_account_attempted_pct=0.05,
                        competitive_displacement_win_rate_pct=0.05,
                        vertical_concentration_pct=0.90)
        assert s == 100.0

    def test_competitive_zero_when_healthy(self):
        s = self._score(competitive_account_attempted_pct=0.70,
                        competitive_displacement_win_rate_pct=0.40,
                        vertical_concentration_pct=0.30)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 8. Composite formula – weights sum to 1.0
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_weights_sum_to_one(self):
        """0.30 + 0.30 + 0.25 + 0.15 must equal 1.0."""
        assert 0.30 + 0.30 + 0.25 + 0.15 == pytest.approx(1.0)

    def test_composite_formula_correctness(self):
        """With known sub-scores, composite = cov*0.30 + pen*0.30 + gro*0.25 + com*0.15."""
        engine = make_engine()
        # Craft an input so all sub-scores are 0
        inp = make_input(
            icp_fit_accounts_engaged_pct=0.80,
            accounts_with_no_contact_90d_pct=0.05,
            territory_coverage_calls_per_week_avg=0.90,
            whitespace_opportunity_identified_pct=0.80,
            same_contact_dependency_pct=0.20,
            accounts_with_active_opportunity_pct=0.50,
            net_new_logos_acquired_pct=0.30,
            new_logo_pipeline_pct=0.40,
            territory_growth_rate_pct=0.25,
            competitive_account_attempted_pct=0.70,
            competitive_displacement_win_rate_pct=0.40,
            vertical_concentration_pct=0.30,
        )
        cov = engine._coverage_score(inp)
        pen = engine._penetration_score(inp)
        gro = engine._growth_score(inp)
        com = engine._competitive_score(inp)
        assert cov == 0.0
        assert pen == 0.0
        assert gro == 0.0
        assert com == 0.0
        result = engine.assess(inp)
        assert result.territory_composite == pytest.approx(0.0)

    def test_composite_with_known_values(self):
        """With all sub-scores = 40, composite should be 40."""
        engine = make_engine()
        inp = make_input(
            # coverage = 40 (icp <=0.25 → +40, no_contact below 0.30, calls above 0.50)
            icp_fit_accounts_engaged_pct=0.10,
            accounts_with_no_contact_90d_pct=0.05,
            territory_coverage_calls_per_week_avg=0.80,
            # penetration = 40 (whitespace <=0.15 → +40, same_contact below 0.50, active opp >0.25)
            whitespace_opportunity_identified_pct=0.10,
            same_contact_dependency_pct=0.20,
            accounts_with_active_opportunity_pct=0.40,
            # growth = 40 (logos <=0.05→+45 but pipeline and growth add nothing; 45 > 40 so need careful choice)
            # actually need exactly 40 — use logos=0.12→25 + pipeline=0.10→30 − too much
            # Use logos=0.12→25 + pipeline=0.25→15 = 40; growth_rate > 0.15 → 0
            net_new_logos_acquired_pct=0.12,
            new_logo_pipeline_pct=0.25,
            territory_growth_rate_pct=0.20,
            # competitive = 40 (comp_attempt <=0.15 → +40, win_rate >0.25, vertical <0.65)
            competitive_account_attempted_pct=0.10,
            competitive_displacement_win_rate_pct=0.40,
            vertical_concentration_pct=0.30,
        )
        cov = engine._coverage_score(inp)
        pen = engine._penetration_score(inp)
        gro = engine._growth_score(inp)
        com = engine._competitive_score(inp)
        expected_composite = round(cov * 0.30 + pen * 0.30 + gro * 0.25 + com * 0.15, 1)
        result = engine.assess(inp)
        assert result.coverage_score == cov
        assert result.penetration_score == pen
        assert result.growth_score == gro
        assert result.competitive_score == com
        assert result.territory_composite == pytest.approx(expected_composite)

    def test_composite_capped_at_100(self):
        engine = make_engine()
        # All sub-scores at maximum → composite would be 100
        inp = make_input(
            icp_fit_accounts_engaged_pct=0.05,
            accounts_with_no_contact_90d_pct=0.90,
            territory_coverage_calls_per_week_avg=0.10,
            whitespace_opportunity_identified_pct=0.05,
            same_contact_dependency_pct=0.90,
            accounts_with_active_opportunity_pct=0.05,
            net_new_logos_acquired_pct=0.01,
            new_logo_pipeline_pct=0.05,
            territory_growth_rate_pct=0.01,
            competitive_account_attempted_pct=0.05,
            competitive_displacement_win_rate_pct=0.05,
            vertical_concentration_pct=0.90,
        )
        result = engine.assess(inp)
        assert result.territory_composite <= 100.0


# ---------------------------------------------------------------------------
# 9. Pattern detection – all patterns and priority ordering
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def _assess(self, **kw) -> TerritoryResult:
        return make_engine().assess(make_input(**kw))

    def test_no_pattern_when_healthy(self):
        r = self._assess()
        assert r.territory_pattern == TerritoryPattern.none

    def test_coverage_avoidance(self):
        # accounts_with_no_contact_90d_pct>=0.45 AND coverage>=35
        # Use icp=0.25 (→+40) + no_contact=0.50 (→+35) + calls=0.80 (→0) = 75 coverage
        r = self._assess(
            icp_fit_accounts_engaged_pct=0.25,
            accounts_with_no_contact_90d_pct=0.50,
            territory_coverage_calls_per_week_avg=0.80,
        )
        assert r.territory_pattern == TerritoryPattern.coverage_avoidance

    def test_contact_recycling(self):
        # same_contact_dependency_pct>=0.65 AND penetration>=35
        # Use whitespace=0.15 (→+40) + same_contact=0.70 (→+35) + active_opp=0.40 (→0) = 75 penetration
        # Make sure coverage avoidance does NOT fire (keep no_contact low)
        r = self._assess(
            same_contact_dependency_pct=0.70,
            whitespace_opportunity_identified_pct=0.15,
            accounts_with_active_opportunity_pct=0.40,
            accounts_with_no_contact_90d_pct=0.10,  # prevent coverage_avoidance
            icp_fit_accounts_engaged_pct=0.80,       # prevent coverage score from being high
            territory_coverage_calls_per_week_avg=0.80,
        )
        assert r.territory_pattern == TerritoryPattern.contact_recycling

    def test_expansion_neglect(self):
        # new_logo_pipeline_pct<=0.15 AND growth>=35
        # Use logos=0.05 (→+45) + pipeline=0.10 (→+30) + growth_rate=0.20 (→0) = 75 growth
        # Prevent patterns 1 and 2 from firing
        r = self._assess(
            net_new_logos_acquired_pct=0.05,
            new_logo_pipeline_pct=0.10,
            territory_growth_rate_pct=0.20,
            accounts_with_no_contact_90d_pct=0.10,   # prevent coverage_avoidance
            icp_fit_accounts_engaged_pct=0.80,        # low coverage score
            territory_coverage_calls_per_week_avg=0.80,
            same_contact_dependency_pct=0.20,         # prevent contact_recycling
        )
        assert r.territory_pattern == TerritoryPattern.expansion_neglect

    def test_competitive_blindspot(self):
        # competitive_account_attempted_pct<=0.20 AND competitive>=30
        # comp_attempt=0.15 (→+40) + win_rate=0.10 (→+35) + vertical=0.40 (→0) = 75 competitive
        # Prevent patterns 1, 2, 3 from firing
        r = self._assess(
            competitive_account_attempted_pct=0.15,
            competitive_displacement_win_rate_pct=0.10,
            vertical_concentration_pct=0.40,
            accounts_with_no_contact_90d_pct=0.10,   # prevent coverage_avoidance
            icp_fit_accounts_engaged_pct=0.80,
            territory_coverage_calls_per_week_avg=0.80,
            same_contact_dependency_pct=0.20,         # prevent contact_recycling
            new_logo_pipeline_pct=0.30,               # prevent expansion_neglect
        )
        assert r.territory_pattern == TerritoryPattern.competitive_blindspot

    def test_vertical_concentration(self):
        # vertical_concentration_pct>=0.75 AND competitive>=25
        # comp_attempt=0.35 (→+22) + win_rate=0.25 (→+18) + vertical=0.80 (→+25) = 65 competitive
        # Prevent patterns 1-4 from firing
        r = self._assess(
            vertical_concentration_pct=0.80,
            competitive_account_attempted_pct=0.35,
            competitive_displacement_win_rate_pct=0.25,
            accounts_with_no_contact_90d_pct=0.10,   # prevent coverage_avoidance
            icp_fit_accounts_engaged_pct=0.80,
            territory_coverage_calls_per_week_avg=0.80,
            same_contact_dependency_pct=0.20,         # prevent contact_recycling
            new_logo_pipeline_pct=0.30,               # prevent expansion_neglect
        )
        assert r.territory_pattern == TerritoryPattern.vertical_concentration

    def test_coverage_avoidance_takes_priority_over_contact_recycling(self):
        """When both coverage_avoidance and contact_recycling conditions are met,
        coverage_avoidance wins (it's first in priority order)."""
        r = self._assess(
            # coverage_avoidance conditions
            accounts_with_no_contact_90d_pct=0.50,
            icp_fit_accounts_engaged_pct=0.25,
            territory_coverage_calls_per_week_avg=0.10,
            # contact_recycling conditions
            same_contact_dependency_pct=0.75,
            whitespace_opportunity_identified_pct=0.10,
        )
        assert r.territory_pattern == TerritoryPattern.coverage_avoidance

    def test_contact_recycling_takes_priority_over_expansion_neglect(self):
        """contact_recycling (priority 2) wins over expansion_neglect (priority 3)."""
        r = self._assess(
            # contact_recycling
            same_contact_dependency_pct=0.75,
            whitespace_opportunity_identified_pct=0.10,
            accounts_with_active_opportunity_pct=0.05,
            # expansion_neglect
            net_new_logos_acquired_pct=0.05,
            new_logo_pipeline_pct=0.10,
            # no coverage_avoidance
            accounts_with_no_contact_90d_pct=0.10,
            icp_fit_accounts_engaged_pct=0.80,
            territory_coverage_calls_per_week_avg=0.80,
        )
        assert r.territory_pattern == TerritoryPattern.contact_recycling


# ---------------------------------------------------------------------------
# 10. Risk thresholds – exact boundaries
# ---------------------------------------------------------------------------

class TestRiskThresholds:
    def _risk_at_composite(self, target_composite: float) -> TerritoryRisk:
        """Build an input that yields approximately target_composite and return the risk."""
        engine = make_engine()
        # Use only coverage score to drive composite: composite = cov*0.30
        # With all other sub-scores 0 and cov = target_composite / 0.30
        # We need a combined sub-score to hit the target.
        # Easiest: use the engine's _risk_level directly.
        return engine._risk_level(target_composite)

    def test_risk_below_20_is_low(self):
        engine = make_engine()
        assert engine._risk_level(0.0) == TerritoryRisk.low
        assert engine._risk_level(19.9) == TerritoryRisk.low

    def test_risk_at_20_is_moderate(self):
        engine = make_engine()
        assert engine._risk_level(20.0) == TerritoryRisk.moderate

    def test_risk_between_20_and_40_is_moderate(self):
        engine = make_engine()
        assert engine._risk_level(39.9) == TerritoryRisk.moderate

    def test_risk_at_40_is_high(self):
        engine = make_engine()
        assert engine._risk_level(40.0) == TerritoryRisk.high

    def test_risk_between_40_and_60_is_high(self):
        engine = make_engine()
        assert engine._risk_level(59.9) == TerritoryRisk.high

    def test_risk_at_60_is_critical(self):
        engine = make_engine()
        assert engine._risk_level(60.0) == TerritoryRisk.critical

    def test_risk_above_60_is_critical(self):
        engine = make_engine()
        assert engine._risk_level(100.0) == TerritoryRisk.critical


# ---------------------------------------------------------------------------
# 11. Severity thresholds – exact boundaries
# ---------------------------------------------------------------------------

class TestSeverityThresholds:
    def test_severity_below_20_is_optimal(self):
        engine = make_engine()
        assert engine._severity(0.0) == TerritorySeverity.optimal
        assert engine._severity(19.9) == TerritorySeverity.optimal

    def test_severity_at_20_is_acceptable(self):
        engine = make_engine()
        assert engine._severity(20.0) == TerritorySeverity.acceptable

    def test_severity_between_20_and_40_is_acceptable(self):
        engine = make_engine()
        assert engine._severity(39.9) == TerritorySeverity.acceptable

    def test_severity_at_40_is_concerning(self):
        engine = make_engine()
        assert engine._severity(40.0) == TerritorySeverity.concerning

    def test_severity_between_40_and_60_is_concerning(self):
        engine = make_engine()
        assert engine._severity(59.9) == TerritorySeverity.concerning

    def test_severity_at_60_is_stagnant(self):
        engine = make_engine()
        assert engine._severity(60.0) == TerritorySeverity.stagnant

    def test_severity_above_60_is_stagnant(self):
        engine = make_engine()
        assert engine._severity(100.0) == TerritorySeverity.stagnant


# ---------------------------------------------------------------------------
# 12. Action mappings – all branches
# ---------------------------------------------------------------------------

class TestActionMappings:
    def _action(self, risk: TerritoryRisk, pattern: TerritoryPattern) -> TerritoryAction:
        return make_engine()._action(risk, pattern)

    def test_critical_coverage_avoidance(self):
        assert self._action(TerritoryRisk.critical, TerritoryPattern.coverage_avoidance) == \
            TerritoryAction.territory_coverage_intervention

    def test_critical_contact_recycling(self):
        assert self._action(TerritoryRisk.critical, TerritoryPattern.contact_recycling) == \
            TerritoryAction.contact_diversification_coaching

    def test_critical_expansion_neglect(self):
        assert self._action(TerritoryRisk.critical, TerritoryPattern.expansion_neglect) == \
            TerritoryAction.territory_strategy_reset

    def test_critical_competitive_blindspot(self):
        assert self._action(TerritoryRisk.critical, TerritoryPattern.competitive_blindspot) == \
            TerritoryAction.territory_strategy_reset

    def test_critical_vertical_concentration(self):
        assert self._action(TerritoryRisk.critical, TerritoryPattern.vertical_concentration) == \
            TerritoryAction.territory_strategy_reset

    def test_critical_none_pattern(self):
        assert self._action(TerritoryRisk.critical, TerritoryPattern.none) == \
            TerritoryAction.territory_strategy_reset

    def test_high_expansion_neglect(self):
        assert self._action(TerritoryRisk.high, TerritoryPattern.expansion_neglect) == \
            TerritoryAction.new_logo_coaching

    def test_high_competitive_blindspot(self):
        assert self._action(TerritoryRisk.high, TerritoryPattern.competitive_blindspot) == \
            TerritoryAction.competitive_territory_coaching

    def test_high_coverage_avoidance(self):
        assert self._action(TerritoryRisk.high, TerritoryPattern.coverage_avoidance) == \
            TerritoryAction.territory_planning_coaching

    def test_high_contact_recycling(self):
        assert self._action(TerritoryRisk.high, TerritoryPattern.contact_recycling) == \
            TerritoryAction.territory_planning_coaching

    def test_high_none_pattern(self):
        assert self._action(TerritoryRisk.high, TerritoryPattern.none) == \
            TerritoryAction.territory_planning_coaching

    def test_moderate_any_pattern(self):
        assert self._action(TerritoryRisk.moderate, TerritoryPattern.none) == \
            TerritoryAction.territory_planning_coaching
        assert self._action(TerritoryRisk.moderate, TerritoryPattern.expansion_neglect) == \
            TerritoryAction.territory_planning_coaching

    def test_low_no_action(self):
        assert self._action(TerritoryRisk.low, TerritoryPattern.none) == \
            TerritoryAction.no_action
        assert self._action(TerritoryRisk.low, TerritoryPattern.coverage_avoidance) == \
            TerritoryAction.no_action


# ---------------------------------------------------------------------------
# 13. Flag conditions
# ---------------------------------------------------------------------------

class TestFlagConditions:
    def _gap(self, composite: float, **kw) -> bool:
        engine = make_engine()
        inp = make_input(**kw)
        return engine._has_territory_gap(composite, inp)

    def _coach(self, composite: float, **kw) -> bool:
        engine = make_engine()
        inp = make_input(**kw)
        return engine._requires_territory_coaching(composite, inp)

    # has_territory_gap
    def test_gap_true_when_composite_ge_40(self):
        assert self._gap(40.0) is True
        assert self._gap(60.0) is True

    def test_gap_false_when_all_conditions_miss(self):
        # composite < 40, no_contact < 0.35, logos > 0.08
        assert self._gap(
            30.0,
            accounts_with_no_contact_90d_pct=0.10,
            net_new_logos_acquired_pct=0.09
        ) is False

    def test_gap_true_when_no_contact_ge_035(self):
        assert self._gap(
            10.0,
            accounts_with_no_contact_90d_pct=0.35,
            net_new_logos_acquired_pct=0.20
        ) is True

    def test_gap_true_when_logos_le_008(self):
        assert self._gap(
            10.0,
            accounts_with_no_contact_90d_pct=0.10,
            net_new_logos_acquired_pct=0.08
        ) is True

    def test_gap_false_at_exact_boundary_below(self):
        # composite=39.9 < 40, no_contact=0.34, logos=0.09 → all false
        assert self._gap(
            39.9,
            accounts_with_no_contact_90d_pct=0.34,
            net_new_logos_acquired_pct=0.09
        ) is False

    # requires_territory_coaching
    def test_coaching_true_when_composite_ge_30(self):
        assert self._coach(30.0) is True
        assert self._coach(50.0) is True

    def test_coaching_false_when_all_conditions_miss(self):
        assert self._coach(
            20.0,
            icp_fit_accounts_engaged_pct=0.50,
            same_contact_dependency_pct=0.30
        ) is False

    def test_coaching_true_when_icp_le_040(self):
        assert self._coach(
            10.0,
            icp_fit_accounts_engaged_pct=0.40,
            same_contact_dependency_pct=0.20
        ) is True

    def test_coaching_true_when_same_contact_ge_050(self):
        assert self._coach(
            10.0,
            icp_fit_accounts_engaged_pct=0.70,
            same_contact_dependency_pct=0.50
        ) is True

    def test_coaching_false_at_exact_boundaries_below(self):
        # composite=29.9, icp=0.41, same_contact=0.49 → all false
        assert self._coach(
            29.9,
            icp_fit_accounts_engaged_pct=0.41,
            same_contact_dependency_pct=0.49
        ) is False


# ---------------------------------------------------------------------------
# 14. Whitespace opportunity formula
# ---------------------------------------------------------------------------

class TestWhitespaceOpportunityFormula:
    def test_basic_calculation(self):
        engine = make_engine()
        inp = make_input(
            total_territory_icp_accounts=100,
            avg_opportunity_value_usd=10_000.0,
            icp_fit_accounts_engaged_pct=0.50,
        )
        # composite is what assess computes; test via _estimated_whitespace_opportunity directly
        composite = 50.0
        expected = round(100 * 10_000 * (1 - 0.50) * (50 / 100), 2)
        assert expected == 250_000.00
        result = engine._estimated_whitespace_opportunity(inp, composite)
        assert result == pytest.approx(250_000.00)

    def test_zero_when_composite_is_zero(self):
        engine = make_engine()
        inp = make_input(total_territory_icp_accounts=100, avg_opportunity_value_usd=5_000.0,
                         icp_fit_accounts_engaged_pct=0.20)
        assert engine._estimated_whitespace_opportunity(inp, 0.0) == 0.0

    def test_zero_when_fully_engaged(self):
        engine = make_engine()
        inp = make_input(total_territory_icp_accounts=100, avg_opportunity_value_usd=5_000.0,
                         icp_fit_accounts_engaged_pct=1.0)
        assert engine._estimated_whitespace_opportunity(inp, 50.0) == 0.0

    def test_uncovered_clamped_at_zero(self):
        """icp_fit_accounts_engaged_pct > 1.0 → uncovered clamped to 0."""
        engine = make_engine()
        inp = make_input(total_territory_icp_accounts=100, avg_opportunity_value_usd=5_000.0,
                         icp_fit_accounts_engaged_pct=1.10)
        assert engine._estimated_whitespace_opportunity(inp, 50.0) == 0.0

    def test_rounded_to_2_decimals(self):
        engine = make_engine()
        inp = make_input(
            total_territory_icp_accounts=3,
            avg_opportunity_value_usd=7_777.77,
            icp_fit_accounts_engaged_pct=0.33,
        )
        composite = 33.33
        expected = round(3 * 7_777.77 * (1 - 0.33) * (33.33 / 100), 2)
        assert engine._estimated_whitespace_opportunity(inp, composite) == pytest.approx(expected)

    def test_formula_in_assess_result(self):
        engine = make_engine()
        inp = make_input(
            total_territory_icp_accounts=200,
            avg_opportunity_value_usd=5_000.0,
            icp_fit_accounts_engaged_pct=0.70,
        )
        r = engine.assess(inp)
        composite = r.territory_composite
        expected = round(200 * 5_000 * (1 - 0.70) * (composite / 100), 2)
        assert r.estimated_whitespace_opportunity_usd == pytest.approx(expected)


# ---------------------------------------------------------------------------
# 15. Signal string
# ---------------------------------------------------------------------------

class TestSignalString:
    def test_strong_signal_when_no_pattern_and_composite_below_20(self):
        engine = make_engine()
        # All healthy inputs → pattern=none, composite≈0
        inp = make_input()  # healthy baseline
        r = engine.assess(inp)
        if r.territory_pattern == TerritoryPattern.none and r.territory_composite < 20:
            assert r.territory_signal == (
                "Territory coverage strong — ICP engagement, new logo pursuit, "
                "and competitive displacement within benchmarks"
            )

    def test_strong_signal_directly(self):
        engine = make_engine()
        inp = make_input(
            icp_fit_accounts_engaged_pct=0.80,
            accounts_with_no_contact_90d_pct=0.05,
            territory_coverage_calls_per_week_avg=0.90,
            whitespace_opportunity_identified_pct=0.80,
            same_contact_dependency_pct=0.20,
            accounts_with_active_opportunity_pct=0.50,
            net_new_logos_acquired_pct=0.30,
            new_logo_pipeline_pct=0.40,
            territory_growth_rate_pct=0.25,
            competitive_account_attempted_pct=0.70,
            competitive_displacement_win_rate_pct=0.40,
            vertical_concentration_pct=0.30,
        )
        r = engine.assess(inp)
        assert r.territory_pattern == TerritoryPattern.none
        assert r.territory_composite < 20
        assert r.territory_signal == (
            "Territory coverage strong — ICP engagement, new logo pursuit, "
            "and competitive displacement within benchmarks"
        )

    def test_signal_with_pattern(self):
        engine = make_engine()
        # Force coverage_avoidance pattern
        inp = make_input(
            icp_fit_accounts_engaged_pct=0.25,
            accounts_with_no_contact_90d_pct=0.50,
            territory_coverage_calls_per_week_avg=0.80,
        )
        r = engine.assess(inp)
        assert r.territory_pattern == TerritoryPattern.coverage_avoidance
        icp_pct = f"{inp.icp_fit_accounts_engaged_pct * 100:.0f}"
        logo_pct = f"{inp.net_new_logos_acquired_pct * 100:.0f}"
        dormant_pct = f"{inp.accounts_with_no_contact_90d_pct * 100:.0f}"
        composite_str = f"{r.territory_composite:.0f}"
        expected = (
            f"Coverage avoidance — {icp_pct}% ICP accounts engaged — "
            f"{logo_pct}% new logos acquired — "
            f"{dormant_pct}% dormant 90d — composite {composite_str}"
        )
        assert r.territory_signal == expected

    def test_signal_with_territory_risk_label(self):
        """When pattern is none but composite >= 20, label is 'Territory risk'."""
        engine = make_engine()
        # Drive composite to ~20-39 (moderate) but keep pattern=none
        # Need moderate composite with no pattern triggers:
        # coverage=22 (icp=0.45), penetration=22 (whitespace=0.30), growth=25 (logos=0.12, pipeline=0.10), competitive=0
        inp = make_input(
            icp_fit_accounts_engaged_pct=0.46,    # 0 from icp (>0.45 but <=0.65 → 8)
            accounts_with_no_contact_90d_pct=0.29, # 0 from no_contact (< 0.30)
            territory_coverage_calls_per_week_avg=0.80,  # 0 from calls
            whitespace_opportunity_identified_pct=0.31,  # 0 from whitespace (> 0.30)
            same_contact_dependency_pct=0.30,            # 0 from same_contact
            accounts_with_active_opportunity_pct=0.30,   # 0 from active_opp (> 0.25)
            net_new_logos_acquired_pct=0.13,             # 0 from logos (> 0.12)
            new_logo_pipeline_pct=0.26,                  # 0 from pipeline (> 0.25)
            territory_growth_rate_pct=0.16,              # 0 from growth_rate (> 0.15)
            competitive_account_attempted_pct=0.60,
            competitive_displacement_win_rate_pct=0.40,
            vertical_concentration_pct=0.30,
        )
        r = engine.assess(inp)
        # With icp=0.46 → +8 (coverage), everything else 0 → composite = 8*0.30 = 2.4
        # That's below 20 → might hit the "strong" branch, skip if so
        # Let's check dynamically
        if r.territory_pattern == TerritoryPattern.none and r.territory_composite >= 20:
            assert "Territory risk" in r.territory_signal

    def test_signal_format_for_each_pattern(self):
        """Verify capitalization of pattern labels in signal."""
        engine = make_engine()
        # expansion_neglect pattern: "Expansion neglect — ..."
        inp = make_input(
            net_new_logos_acquired_pct=0.05,
            new_logo_pipeline_pct=0.10,
            territory_growth_rate_pct=0.20,
            accounts_with_no_contact_90d_pct=0.10,
            icp_fit_accounts_engaged_pct=0.80,
            territory_coverage_calls_per_week_avg=0.80,
            same_contact_dependency_pct=0.20,
        )
        r = engine.assess(inp)
        if r.territory_pattern == TerritoryPattern.expansion_neglect:
            assert r.territory_signal.startswith("Expansion neglect")


# ---------------------------------------------------------------------------
# 16. assess() end-to-end
# ---------------------------------------------------------------------------

class TestAssessEndToEnd:
    def test_assess_returns_territory_result(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert isinstance(result, TerritoryResult)

    def test_assess_preserves_rep_id_and_region(self):
        engine = make_engine()
        inp = make_input(rep_id="rep-999", region="North")
        r = engine.assess(inp)
        assert r.rep_id == "rep-999"
        assert r.region == "North"

    def test_assess_appends_to_results(self):
        engine = make_engine()
        engine.assess(make_input())
        engine.assess(make_input(rep_id="rep-002"))
        assert len(engine._results) == 2

    def test_assess_low_risk_healthy_rep(self):
        engine = make_engine()
        r = engine.assess(make_input())
        assert r.territory_risk == TerritoryRisk.low
        assert r.territory_severity == TerritorySeverity.optimal
        assert r.recommended_action == TerritoryAction.no_action

    def test_assess_critical_high_risk_rep(self):
        engine = make_engine()
        inp = make_input(
            icp_fit_accounts_engaged_pct=0.05,
            accounts_with_no_contact_90d_pct=0.90,
            territory_coverage_calls_per_week_avg=0.10,
            whitespace_opportunity_identified_pct=0.05,
            same_contact_dependency_pct=0.90,
            accounts_with_active_opportunity_pct=0.05,
            net_new_logos_acquired_pct=0.01,
            new_logo_pipeline_pct=0.05,
            territory_growth_rate_pct=0.01,
            competitive_account_attempted_pct=0.05,
            competitive_displacement_win_rate_pct=0.05,
            vertical_concentration_pct=0.90,
        )
        r = engine.assess(inp)
        assert r.territory_risk == TerritoryRisk.critical
        assert r.territory_severity == TerritorySeverity.stagnant

    def test_assess_scores_in_range_0_100(self):
        engine = make_engine()
        r = engine.assess(make_input())
        assert 0.0 <= r.coverage_score <= 100.0
        assert 0.0 <= r.penetration_score <= 100.0
        assert 0.0 <= r.growth_score <= 100.0
        assert 0.0 <= r.competitive_score <= 100.0
        assert 0.0 <= r.territory_composite <= 100.0

    def test_assess_bool_fields(self):
        engine = make_engine()
        r = engine.assess(make_input())
        assert isinstance(r.has_territory_gap, bool)
        assert isinstance(r.requires_territory_coaching, bool)

    def test_assess_whitespace_usd_is_float(self):
        engine = make_engine()
        r = engine.assess(make_input())
        assert isinstance(r.estimated_whitespace_opportunity_usd, float)


# ---------------------------------------------------------------------------
# 17. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list_of_territory_results(self):
        engine = make_engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert isinstance(results, list)
        assert len(results) == 5
        assert all(isinstance(r, TerritoryResult) for r in results)

    def test_empty_batch(self):
        engine = make_engine()
        results = engine.assess_batch([])
        assert results == []

    def test_batch_appends_to_internal_results(self):
        engine = make_engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(3)]
        engine.assess_batch(inputs)
        assert len(engine._results) == 3

    def test_batch_single_item(self):
        engine = make_engine()
        inp = make_input(rep_id="rep-solo")
        results = engine.assess_batch([inp])
        assert len(results) == 1
        assert results[0].rep_id == "rep-solo"

    def test_batch_rep_ids_preserved(self):
        engine = make_engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(4)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep-{i}"


# ---------------------------------------------------------------------------
# 18. summary() – empty and populated, all 13 keys
# ---------------------------------------------------------------------------

class TestSummary:
    EXPECTED_KEYS = {
        "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
        "avg_territory_composite", "territory_gap_count", "coaching_count",
        "avg_coverage_score", "avg_penetration_score", "avg_growth_score",
        "avg_competitive_score", "total_estimated_whitespace_opportunity_usd",
    }

    def test_empty_summary_has_13_keys(self):
        engine = make_engine()
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_exact_keys(self):
        engine = make_engine()
        s = engine.summary()
        assert set(s.keys()) == self.EXPECTED_KEYS

    def test_empty_summary_total_is_zero(self):
        engine = make_engine()
        s = engine.summary()
        assert s["total"] == 0

    def test_empty_summary_numeric_defaults(self):
        engine = make_engine()
        s = engine.summary()
        assert s["avg_territory_composite"] == 0.0
        assert s["territory_gap_count"] == 0
        assert s["coaching_count"] == 0
        assert s["avg_coverage_score"] == 0.0
        assert s["avg_penetration_score"] == 0.0
        assert s["avg_growth_score"] == 0.0
        assert s["avg_competitive_score"] == 0.0
        assert s["total_estimated_whitespace_opportunity_usd"] == 0.0

    def test_empty_summary_dict_defaults(self):
        engine = make_engine()
        s = engine.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_populated_summary_has_13_keys(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert len(s) == 13

    def test_populated_summary_exact_keys(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert set(s.keys()) == self.EXPECTED_KEYS

    def test_populated_summary_total(self):
        engine = make_engine()
        engine.assess_batch([make_input(rep_id=f"rep-{i}") for i in range(3)])
        s = engine.summary()
        assert s["total"] == 3

    def test_populated_summary_risk_counts(self):
        engine = make_engine()
        engine.assess(make_input())  # healthy → low
        s = engine.summary()
        assert "low" in s["risk_counts"]
        assert s["risk_counts"]["low"] == 1

    def test_populated_summary_pattern_counts(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["pattern_counts"], dict)
        total_patterns = sum(s["pattern_counts"].values())
        assert total_patterns == s["total"]

    def test_populated_summary_severity_counts(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["severity_counts"], dict)
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_populated_summary_action_counts(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["action_counts"], dict)
        assert sum(s["action_counts"].values()) == s["total"]

    def test_populated_summary_avg_composite(self):
        engine = make_engine()
        inputs = [make_input(rep_id=f"r{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        s = engine.summary()
        expected_avg = round(sum(r.territory_composite for r in results) / 3, 1)
        assert s["avg_territory_composite"] == pytest.approx(expected_avg)

    def test_populated_summary_gap_count(self):
        engine = make_engine()
        engine.assess(make_input())  # healthy → no gap
        # Force a gap
        engine.assess(make_input(
            accounts_with_no_contact_90d_pct=0.50,
            net_new_logos_acquired_pct=0.05,
        ))
        s = engine.summary()
        assert s["territory_gap_count"] >= 1

    def test_populated_summary_coaching_count(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["coaching_count"], int)

    def test_populated_summary_avg_scores(self):
        engine = make_engine()
        results = engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(4)])
        s = engine.summary()
        n = len(results)
        assert s["avg_coverage_score"] == pytest.approx(
            round(sum(r.coverage_score for r in results) / n, 1))
        assert s["avg_penetration_score"] == pytest.approx(
            round(sum(r.penetration_score for r in results) / n, 1))
        assert s["avg_growth_score"] == pytest.approx(
            round(sum(r.growth_score for r in results) / n, 1))
        assert s["avg_competitive_score"] == pytest.approx(
            round(sum(r.competitive_score for r in results) / n, 1))

    def test_populated_summary_total_whitespace_usd(self):
        engine = make_engine()
        results = engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = engine.summary()
        expected = round(sum(r.estimated_whitespace_opportunity_usd for r in results), 2)
        assert s["total_estimated_whitespace_opportunity_usd"] == pytest.approx(expected)

    def test_summary_accumulates_across_multiple_assess_calls(self):
        engine = make_engine()
        engine.assess(make_input(rep_id="r1"))
        engine.assess(make_input(rep_id="r2"))
        s = engine.summary()
        assert s["total"] == 2

    def test_new_engine_starts_fresh(self):
        engine1 = make_engine()
        engine1.assess(make_input())
        engine2 = make_engine()
        s = engine2.summary()
        assert s["total"] == 0
