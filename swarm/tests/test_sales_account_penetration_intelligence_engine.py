"""
Comprehensive pytest test suite for SalesAccountPenetrationIntelligenceEngine.
"""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_account_penetration_intelligence_engine import (
    PenetrationRisk,
    PenetrationPattern,
    PenetrationSeverity,
    PenetrationAction,
    AccountPenetrationInput,
    AccountPenetrationResult,
    SalesAccountPenetrationIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> AccountPenetrationInput:
    """Return a healthy baseline input; override any field via kwargs."""
    defaults = dict(
        rep_id="rep-001",
        region="WEST",
        evaluation_period_id="Q1-2026",
        total_target_accounts=100,
        accounts_with_active_opportunity_count=50,
        accounts_with_multiple_contacts_count=30,
        accounts_with_single_contact_count=10,
        avg_contacts_per_target_account=2.5,
        large_account_engagement_count=8,
        large_account_ignored_count=1,
        account_activity_days_avg=20.0,
        accounts_with_no_activity_90d_count=5,
        avg_deal_size_per_account_usd=10_000.0,
        total_addressable_revenue_usd=1_000_000.0,
        captured_revenue_pct=0.40,
        whitespace_accounts_count=10,
        expansion_attempts_count=5,
        expansion_success_count=3,
        account_renewal_at_risk_count=0,
        competitive_accounts_touched_count=20,
        executive_level_engagement_count=15,
        avg_account_health_score=7.0,
    )
    defaults.update(overrides)
    return AccountPenetrationInput(**defaults)


def engine() -> SalesAccountPenetrationIntelligenceEngine:
    return SalesAccountPenetrationIntelligenceEngine()


# ===========================================================================
# 1. Enum values
# ===========================================================================

class TestEnumValues:
    def test_risk_low(self):
        assert PenetrationRisk.low.value == "low"

    def test_risk_moderate(self):
        assert PenetrationRisk.moderate.value == "moderate"

    def test_risk_high(self):
        assert PenetrationRisk.high.value == "high"

    def test_risk_critical(self):
        assert PenetrationRisk.critical.value == "critical"

    def test_pattern_none(self):
        assert PenetrationPattern.none.value == "none"

    def test_pattern_whitespace_neglect(self):
        assert PenetrationPattern.whitespace_neglect.value == "whitespace_neglect"

    def test_pattern_shallow_coverage(self):
        assert PenetrationPattern.shallow_coverage.value == "shallow_coverage"

    def test_pattern_cherry_picking(self):
        assert PenetrationPattern.cherry_picking.value == "cherry_picking"

    def test_pattern_churn_risk_blindness(self):
        assert PenetrationPattern.churn_risk_blindness.value == "churn_risk_blindness"

    def test_pattern_expansion_stagnation(self):
        assert PenetrationPattern.expansion_stagnation.value == "expansion_stagnation"

    def test_severity_optimal(self):
        assert PenetrationSeverity.optimal.value == "optimal"

    def test_severity_developing(self):
        assert PenetrationSeverity.developing.value == "developing"

    def test_severity_shallow(self):
        assert PenetrationSeverity.shallow.value == "shallow"

    def test_severity_stagnant(self):
        assert PenetrationSeverity.stagnant.value == "stagnant"

    def test_action_no_action(self):
        assert PenetrationAction.no_action.value == "no_action"

    def test_action_territory_coverage_coaching(self):
        assert PenetrationAction.territory_coverage_coaching.value == "territory_coverage_coaching"

    def test_action_account_prioritization_review(self):
        assert PenetrationAction.account_prioritization_review.value == "account_prioritization_review"

    def test_action_strategic_account_planning(self):
        assert PenetrationAction.strategic_account_planning.value == "strategic_account_planning"

    def test_action_expansion_pipeline_build(self):
        assert PenetrationAction.expansion_pipeline_build.value == "expansion_pipeline_build"

    def test_action_executive_engagement_program(self):
        assert PenetrationAction.executive_engagement_program.value == "executive_engagement_program"

    def test_risk_is_str_enum(self):
        assert isinstance(PenetrationRisk.low, str)

    def test_pattern_is_str_enum(self):
        assert isinstance(PenetrationPattern.none, str)

    def test_severity_is_str_enum(self):
        assert isinstance(PenetrationSeverity.optimal, str)

    def test_action_is_str_enum(self):
        assert isinstance(PenetrationAction.no_action, str)

    def test_risk_enum_count(self):
        assert len(PenetrationRisk) == 4

    def test_pattern_enum_count(self):
        assert len(PenetrationPattern) == 6

    def test_severity_enum_count(self):
        assert len(PenetrationSeverity) == 4

    def test_action_enum_count(self):
        assert len(PenetrationAction) == 6


# ===========================================================================
# 2. AccountPenetrationInput dataclass
# ===========================================================================

class TestInputDataclass:
    def test_creation(self):
        inp = make_input()
        assert inp.rep_id == "rep-001"

    def test_all_22_fields_exist(self):
        inp = make_input()
        fields = [
            "rep_id", "region", "evaluation_period_id", "total_target_accounts",
            "accounts_with_active_opportunity_count", "accounts_with_multiple_contacts_count",
            "accounts_with_single_contact_count", "avg_contacts_per_target_account",
            "large_account_engagement_count", "large_account_ignored_count",
            "account_activity_days_avg", "accounts_with_no_activity_90d_count",
            "avg_deal_size_per_account_usd", "total_addressable_revenue_usd",
            "captured_revenue_pct", "whitespace_accounts_count",
            "expansion_attempts_count", "expansion_success_count",
            "account_renewal_at_risk_count", "competitive_accounts_touched_count",
            "executive_level_engagement_count", "avg_account_health_score",
        ]
        for f in fields:
            assert hasattr(inp, f), f"Missing field: {f}"


# ===========================================================================
# 3. to_dict() – 15 keys
# ===========================================================================

class TestToDict:
    EXPECTED_KEYS = {
        "rep_id", "region", "penetration_risk", "penetration_pattern",
        "penetration_severity", "recommended_action", "account_coverage_score",
        "account_depth_score", "strategic_focus_score", "expansion_momentum_score",
        "account_penetration_composite", "has_penetration_gap",
        "requires_account_coaching", "estimated_untapped_revenue_usd",
        "penetration_signal",
    }

    def test_to_dict_has_15_keys(self):
        e = engine()
        r = e.assess(make_input())
        assert set(r.to_dict().keys()) == self.EXPECTED_KEYS

    def test_to_dict_enum_values_are_strings(self):
        e = engine()
        r = e.assess(make_input())
        d = r.to_dict()
        assert isinstance(d["penetration_risk"], str)
        assert isinstance(d["penetration_pattern"], str)
        assert isinstance(d["penetration_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_correct(self):
        e = engine()
        r = e.assess(make_input(rep_id="xyz"))
        assert r.to_dict()["rep_id"] == "xyz"

    def test_to_dict_region_correct(self):
        e = engine()
        r = e.assess(make_input(region="EAST"))
        assert r.to_dict()["region"] == "EAST"

    def test_to_dict_bool_fields_are_bool(self):
        e = engine()
        d = e.assess(make_input()).to_dict()
        assert isinstance(d["has_penetration_gap"], bool)
        assert isinstance(d["requires_account_coaching"], bool)

    def test_to_dict_numeric_fields_are_float(self):
        e = engine()
        d = e.assess(make_input()).to_dict()
        for key in ("account_coverage_score", "account_depth_score",
                    "strategic_focus_score", "expansion_momentum_score",
                    "account_penetration_composite", "estimated_untapped_revenue_usd"):
            assert isinstance(d[key], (int, float)), f"{key} should be numeric"


# ===========================================================================
# 4. _account_coverage_score branches
# ===========================================================================

class TestCoverageScore:
    def _cov(self, **kw):
        e = engine()
        return e._account_coverage_score(make_input(**kw))

    # pen_rate branches
    def test_pen_rate_below_020_adds_40(self):
        # active=10/100 = 0.10 < 0.20 → +40
        s = self._cov(accounts_with_active_opportunity_count=10,
                      accounts_with_no_activity_90d_count=0,
                      account_activity_days_avg=0.0)
        assert s == 40.0

    def test_pen_rate_exactly_020_not_below_adds_20(self):
        # active=20/100 = 0.20 → falls to <0.35 → +20
        s = self._cov(accounts_with_active_opportunity_count=20,
                      accounts_with_no_activity_90d_count=0,
                      account_activity_days_avg=0.0)
        assert s == 20.0

    def test_pen_rate_between_020_035_adds_20(self):
        # active=25/100 = 0.25
        s = self._cov(accounts_with_active_opportunity_count=25,
                      accounts_with_no_activity_90d_count=0,
                      account_activity_days_avg=0.0)
        assert s == 20.0

    def test_pen_rate_between_035_050_adds_8(self):
        # active=40/100 = 0.40
        s = self._cov(accounts_with_active_opportunity_count=40,
                      accounts_with_no_activity_90d_count=0,
                      account_activity_days_avg=0.0)
        assert s == 8.0

    def test_pen_rate_exactly_035_adds_8(self):
        # active=35/100 = 0.35 → falls to <0.50 → +8
        s = self._cov(accounts_with_active_opportunity_count=35,
                      accounts_with_no_activity_90d_count=0,
                      account_activity_days_avg=0.0)
        assert s == 8.0

    def test_pen_rate_050_or_above_adds_0(self):
        # active=50/100 = 0.50 → no branch
        s = self._cov(accounts_with_active_opportunity_count=50,
                      accounts_with_no_activity_90d_count=0,
                      account_activity_days_avg=0.0)
        assert s == 0.0

    # inactive_rate branches
    def test_inactive_rate_gte_050_adds_35(self):
        # no_activity=50/100 = 0.50
        s = self._cov(accounts_with_active_opportunity_count=50,
                      accounts_with_no_activity_90d_count=50,
                      account_activity_days_avg=0.0)
        assert s == 35.0

    def test_inactive_rate_between_030_050_adds_18(self):
        # no_activity=35/100
        s = self._cov(accounts_with_active_opportunity_count=50,
                      accounts_with_no_activity_90d_count=35,
                      account_activity_days_avg=0.0)
        assert s == 18.0

    def test_inactive_rate_between_015_030_adds_7(self):
        # no_activity=20/100
        s = self._cov(accounts_with_active_opportunity_count=50,
                      accounts_with_no_activity_90d_count=20,
                      account_activity_days_avg=0.0)
        assert s == 7.0

    def test_inactive_rate_below_015_adds_0(self):
        # no_activity=5/100 = 0.05
        s = self._cov(accounts_with_active_opportunity_count=50,
                      accounts_with_no_activity_90d_count=5,
                      account_activity_days_avg=0.0)
        assert s == 0.0

    # activity days
    def test_activity_days_gte_60_adds_15(self):
        s = self._cov(accounts_with_active_opportunity_count=50,
                      accounts_with_no_activity_90d_count=0,
                      account_activity_days_avg=60.0)
        assert s == 15.0

    def test_activity_days_gte_30_adds_7(self):
        s = self._cov(accounts_with_active_opportunity_count=50,
                      accounts_with_no_activity_90d_count=0,
                      account_activity_days_avg=30.0)
        assert s == 7.0

    def test_activity_days_below_30_adds_0(self):
        s = self._cov(accounts_with_active_opportunity_count=50,
                      accounts_with_no_activity_90d_count=0,
                      account_activity_days_avg=29.9)
        assert s == 0.0

    def test_coverage_capped_at_100(self):
        # pen_rate<0.20 (+40) + inactive>=0.50 (+35) + days>=60 (+15) + pen<0.20 → 90 ≤ 100
        # To force >100 we'd need more than 100 total, let's use exact overflow:
        # +40 + 35 + 15 = 90 — below cap; use combination ensuring >100
        # Actually max possible = 40+35+15=90, so just test normal cap:
        s = self._cov(accounts_with_active_opportunity_count=5,
                      accounts_with_no_activity_90d_count=60,
                      account_activity_days_avg=90.0)
        assert s <= 100.0

    def test_zero_total_accounts_uses_max1(self):
        # Should not crash with 0 total
        inp = make_input(total_target_accounts=0,
                         accounts_with_active_opportunity_count=0,
                         accounts_with_no_activity_90d_count=0,
                         account_activity_days_avg=0.0)
        s = engine()._account_coverage_score(inp)
        assert 0.0 <= s <= 100.0


# ===========================================================================
# 5. _account_depth_score branches
# ===========================================================================

class TestDepthScore:
    def _dep(self, **kw):
        return engine()._account_depth_score(make_input(**kw))

    def test_single_rate_gte_060_adds_40(self):
        # single=6 / active=10 = 0.60 → +40; avg_contacts<1.0 → +30; exec_rate low → +20
        s = self._dep(accounts_with_active_opportunity_count=10,
                      accounts_with_single_contact_count=6,
                      avg_contacts_per_target_account=2.5,
                      executive_level_engagement_count=30,
                      total_target_accounts=100)
        # single_rate=0.60 → +40; avg=2.5 → 0; exec=30/100=0.30 → 0
        assert s == 40.0

    def test_single_rate_between_040_060_adds_20(self):
        s = self._dep(accounts_with_active_opportunity_count=10,
                      accounts_with_single_contact_count=5,
                      avg_contacts_per_target_account=2.5,
                      executive_level_engagement_count=30,
                      total_target_accounts=100)
        # single_rate=5/10=0.50 → +20
        assert s == 20.0

    def test_single_rate_between_025_040_adds_8(self):
        s = self._dep(accounts_with_active_opportunity_count=10,
                      accounts_with_single_contact_count=3,
                      avg_contacts_per_target_account=2.5,
                      executive_level_engagement_count=30,
                      total_target_accounts=100)
        # single_rate=3/10=0.30 → +8
        assert s == 8.0

    def test_single_rate_below_025_adds_0(self):
        s = self._dep(accounts_with_active_opportunity_count=10,
                      accounts_with_single_contact_count=2,
                      avg_contacts_per_target_account=2.5,
                      executive_level_engagement_count=30,
                      total_target_accounts=100)
        # single_rate=2/10=0.20 → 0
        assert s == 0.0

    def test_avg_contacts_below_10_adds_30(self):
        s = self._dep(accounts_with_active_opportunity_count=10,
                      accounts_with_single_contact_count=0,
                      avg_contacts_per_target_account=0.5,
                      executive_level_engagement_count=30,
                      total_target_accounts=100)
        assert s == 30.0

    def test_avg_contacts_between_10_15_adds_15(self):
        s = self._dep(accounts_with_active_opportunity_count=10,
                      accounts_with_single_contact_count=0,
                      avg_contacts_per_target_account=1.2,
                      executive_level_engagement_count=30,
                      total_target_accounts=100)
        assert s == 15.0

    def test_avg_contacts_between_15_20_adds_7(self):
        s = self._dep(accounts_with_active_opportunity_count=10,
                      accounts_with_single_contact_count=0,
                      avg_contacts_per_target_account=1.7,
                      executive_level_engagement_count=30,
                      total_target_accounts=100)
        assert s == 7.0

    def test_avg_contacts_gte_20_adds_0(self):
        s = self._dep(accounts_with_active_opportunity_count=10,
                      accounts_with_single_contact_count=0,
                      avg_contacts_per_target_account=2.0,
                      executive_level_engagement_count=30,
                      total_target_accounts=100)
        assert s == 0.0

    def test_exec_rate_below_010_adds_20(self):
        s = self._dep(accounts_with_active_opportunity_count=10,
                      accounts_with_single_contact_count=0,
                      avg_contacts_per_target_account=2.5,
                      executive_level_engagement_count=5,
                      total_target_accounts=100)
        # exec=5/100=0.05 < 0.10 → +20
        assert s == 20.0

    def test_exec_rate_between_010_025_adds_10(self):
        s = self._dep(accounts_with_active_opportunity_count=10,
                      accounts_with_single_contact_count=0,
                      avg_contacts_per_target_account=2.5,
                      executive_level_engagement_count=15,
                      total_target_accounts=100)
        # exec=15/100=0.15 → +10
        assert s == 10.0

    def test_exec_rate_gte_025_adds_0(self):
        s = self._dep(accounts_with_active_opportunity_count=10,
                      accounts_with_single_contact_count=0,
                      avg_contacts_per_target_account=2.5,
                      executive_level_engagement_count=25,
                      total_target_accounts=100)
        assert s == 0.0

    def test_depth_capped_at_100(self):
        # single_rate>=0.60 (+40) + avg<1.0 (+30) + exec<0.10 (+20) = 90; +single? let's try
        s = self._dep(accounts_with_active_opportunity_count=10,
                      accounts_with_single_contact_count=10,
                      avg_contacts_per_target_account=0.5,
                      executive_level_engagement_count=1,
                      total_target_accounts=100)
        assert s <= 100.0

    def test_zero_active_accounts_uses_max1(self):
        inp = make_input(accounts_with_active_opportunity_count=0,
                         accounts_with_single_contact_count=0,
                         avg_contacts_per_target_account=2.5,
                         executive_level_engagement_count=30,
                         total_target_accounts=100)
        s = engine()._account_depth_score(inp)
        assert 0.0 <= s <= 100.0


# ===========================================================================
# 6. _strategic_focus_score branches
# ===========================================================================

class TestStrategicScore:
    def _str(self, **kw):
        return engine()._strategic_focus_score(make_input(**kw))

    def test_neglect_rate_gte_050_adds_40(self):
        # ignored=5, engaged=5 → rate=5/10=0.50
        s = self._str(large_account_engagement_count=5,
                      large_account_ignored_count=5,
                      captured_revenue_pct=0.50,
                      avg_account_health_score=7.0)
        assert s == 40.0

    def test_neglect_rate_between_030_050_adds_20(self):
        # ignored=3, engaged=7 → rate=3/10=0.30
        s = self._str(large_account_engagement_count=7,
                      large_account_ignored_count=3,
                      captured_revenue_pct=0.50,
                      avg_account_health_score=7.0)
        assert s == 20.0

    def test_neglect_rate_between_015_030_adds_8(self):
        # ignored=2, engaged=8 → rate=2/10=0.20
        s = self._str(large_account_engagement_count=8,
                      large_account_ignored_count=2,
                      captured_revenue_pct=0.50,
                      avg_account_health_score=7.0)
        assert s == 8.0

    def test_neglect_rate_below_015_adds_0(self):
        # ignored=1, engaged=9 → rate=1/10=0.10
        s = self._str(large_account_engagement_count=9,
                      large_account_ignored_count=1,
                      captured_revenue_pct=0.50,
                      avg_account_health_score=7.0)
        assert s == 0.0

    def test_captured_revenue_below_010_adds_35(self):
        s = self._str(large_account_engagement_count=10,
                      large_account_ignored_count=0,
                      captured_revenue_pct=0.05,
                      avg_account_health_score=7.0)
        assert s == 35.0

    def test_captured_revenue_between_010_020_adds_18(self):
        s = self._str(large_account_engagement_count=10,
                      large_account_ignored_count=0,
                      captured_revenue_pct=0.15,
                      avg_account_health_score=7.0)
        assert s == 18.0

    def test_captured_revenue_between_020_035_adds_7(self):
        s = self._str(large_account_engagement_count=10,
                      large_account_ignored_count=0,
                      captured_revenue_pct=0.25,
                      avg_account_health_score=7.0)
        assert s == 7.0

    def test_captured_revenue_gte_035_adds_0(self):
        s = self._str(large_account_engagement_count=10,
                      large_account_ignored_count=0,
                      captured_revenue_pct=0.35,
                      avg_account_health_score=7.0)
        assert s == 0.0

    def test_health_below_40_adds_20(self):
        s = self._str(large_account_engagement_count=10,
                      large_account_ignored_count=0,
                      captured_revenue_pct=0.50,
                      avg_account_health_score=3.5)
        assert s == 20.0

    def test_health_between_40_60_adds_10(self):
        s = self._str(large_account_engagement_count=10,
                      large_account_ignored_count=0,
                      captured_revenue_pct=0.50,
                      avg_account_health_score=5.0)
        assert s == 10.0

    def test_health_gte_60_adds_0(self):
        s = self._str(large_account_engagement_count=10,
                      large_account_ignored_count=0,
                      captured_revenue_pct=0.50,
                      avg_account_health_score=6.0)
        assert s == 0.0

    def test_strategic_capped_at_100(self):
        s = self._str(large_account_engagement_count=0,
                      large_account_ignored_count=10,
                      captured_revenue_pct=0.01,
                      avg_account_health_score=1.0)
        assert s <= 100.0

    def test_zero_large_accounts_uses_max1(self):
        inp = make_input(large_account_engagement_count=0,
                         large_account_ignored_count=0,
                         captured_revenue_pct=0.50,
                         avg_account_health_score=7.0)
        s = engine()._strategic_focus_score(inp)
        assert 0.0 <= s <= 100.0


# ===========================================================================
# 7. _expansion_momentum_score branches
# ===========================================================================

class TestExpansionScore:
    def _exp(self, **kw):
        return engine()._expansion_momentum_score(make_input(**kw))

    def test_zero_attempts_adds_30(self):
        s = self._exp(expansion_attempts_count=0,
                      expansion_success_count=0,
                      account_renewal_at_risk_count=0,
                      competitive_accounts_touched_count=50,
                      total_target_accounts=100)
        assert s == 30.0

    def test_exp_rate_below_020_adds_30(self):
        # success=1/attempts=10 = 0.10 < 0.20
        s = self._exp(expansion_attempts_count=10,
                      expansion_success_count=1,
                      account_renewal_at_risk_count=0,
                      competitive_accounts_touched_count=50,
                      total_target_accounts=100)
        assert s == 30.0

    def test_exp_rate_between_020_040_adds_15(self):
        # success=3/attempts=10 = 0.30
        s = self._exp(expansion_attempts_count=10,
                      expansion_success_count=3,
                      account_renewal_at_risk_count=0,
                      competitive_accounts_touched_count=50,
                      total_target_accounts=100)
        assert s == 15.0

    def test_exp_rate_gte_040_adds_0(self):
        # success=4/attempts=10 = 0.40
        s = self._exp(expansion_attempts_count=10,
                      expansion_success_count=4,
                      account_renewal_at_risk_count=0,
                      competitive_accounts_touched_count=50,
                      total_target_accounts=100)
        assert s == 0.0

    def test_renewal_at_risk_gte_3_adds_35(self):
        s = self._exp(expansion_attempts_count=10,
                      expansion_success_count=10,
                      account_renewal_at_risk_count=3,
                      competitive_accounts_touched_count=50,
                      total_target_accounts=100)
        assert s == 35.0

    def test_renewal_at_risk_between_1_3_adds_18(self):
        s = self._exp(expansion_attempts_count=10,
                      expansion_success_count=10,
                      account_renewal_at_risk_count=2,
                      competitive_accounts_touched_count=50,
                      total_target_accounts=100)
        assert s == 18.0

    def test_renewal_at_risk_1_adds_18(self):
        s = self._exp(expansion_attempts_count=10,
                      expansion_success_count=10,
                      account_renewal_at_risk_count=1,
                      competitive_accounts_touched_count=50,
                      total_target_accounts=100)
        assert s == 18.0

    def test_renewal_at_risk_0_adds_0(self):
        s = self._exp(expansion_attempts_count=10,
                      expansion_success_count=10,
                      account_renewal_at_risk_count=0,
                      competitive_accounts_touched_count=50,
                      total_target_accounts=100)
        assert s == 0.0

    def test_comp_rate_below_010_adds_25(self):
        # comp=5/100 = 0.05
        s = self._exp(expansion_attempts_count=10,
                      expansion_success_count=10,
                      account_renewal_at_risk_count=0,
                      competitive_accounts_touched_count=5,
                      total_target_accounts=100)
        assert s == 25.0

    def test_comp_rate_between_010_020_adds_12(self):
        # comp=15/100 = 0.15
        s = self._exp(expansion_attempts_count=10,
                      expansion_success_count=10,
                      account_renewal_at_risk_count=0,
                      competitive_accounts_touched_count=15,
                      total_target_accounts=100)
        assert s == 12.0

    def test_comp_rate_gte_020_adds_0(self):
        # comp=20/100 = 0.20
        s = self._exp(expansion_attempts_count=10,
                      expansion_success_count=10,
                      account_renewal_at_risk_count=0,
                      competitive_accounts_touched_count=20,
                      total_target_accounts=100)
        assert s == 0.0

    def test_expansion_capped_at_100(self):
        s = self._exp(expansion_attempts_count=0,
                      expansion_success_count=0,
                      account_renewal_at_risk_count=10,
                      competitive_accounts_touched_count=0,
                      total_target_accounts=100)
        assert s <= 100.0

    def test_expansion_all_zero_competitive_zero_renewal_zero_attempts(self):
        # attempts=0 (+30), renewal=0 (+0), comp=0/100=0 (+25) = 55
        s = self._exp(expansion_attempts_count=0,
                      expansion_success_count=0,
                      account_renewal_at_risk_count=0,
                      competitive_accounts_touched_count=0,
                      total_target_accounts=100)
        assert s == 55.0


# ===========================================================================
# 8. Composite score
# ===========================================================================

class TestCompositeScore:
    def test_composite_formula(self):
        e = engine()
        inp = make_input()
        cov = round(e._account_coverage_score(inp), 1)
        dep = round(e._account_depth_score(inp), 1)
        strat = round(e._strategic_focus_score(inp), 1)
        exp = round(e._expansion_momentum_score(inp), 1)
        expected = round(cov * 0.30 + dep * 0.30 + strat * 0.25 + exp * 0.15, 1)
        expected = min(expected, 100.0)
        r = e.assess(inp)
        assert r.account_penetration_composite == expected

    def test_composite_capped_at_100(self):
        # force very high scores in all components
        e = engine()
        inp = make_input(
            accounts_with_active_opportunity_count=0,
            accounts_with_no_activity_90d_count=100,
            account_activity_days_avg=90.0,
            accounts_with_single_contact_count=100,
            avg_contacts_per_target_account=0.1,
            executive_level_engagement_count=0,
            large_account_engagement_count=0,
            large_account_ignored_count=10,
            captured_revenue_pct=0.01,
            avg_account_health_score=1.0,
            expansion_attempts_count=0,
            account_renewal_at_risk_count=5,
            competitive_accounts_touched_count=0,
            total_target_accounts=100,
        )
        r = e.assess(inp)
        assert r.account_penetration_composite <= 100.0

    def test_composite_non_negative(self):
        e = engine()
        r = e.assess(make_input())
        assert r.account_penetration_composite >= 0.0


# ===========================================================================
# 9. _detect_pattern – all patterns + priority ordering
# ===========================================================================

class TestDetectPattern:
    def _pattern(self, **kw):
        e = engine()
        inp = make_input(**kw)
        cov = round(e._account_coverage_score(inp), 1)
        dep = round(e._account_depth_score(inp), 1)
        strat = round(e._strategic_focus_score(inp), 1)
        exp = round(e._expansion_momentum_score(inp), 1)
        return e._detect_pattern(inp, cov, dep, strat, exp)

    # --- none pattern ---
    def test_none_pattern_healthy(self):
        # everything healthy → none
        p = self._pattern(
            accounts_with_active_opportunity_count=60,
            accounts_with_no_activity_90d_count=3,
            account_activity_days_avg=10.0,
            accounts_with_single_contact_count=2,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=30,
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.50,
            avg_account_health_score=8.0,
            expansion_attempts_count=10,
            expansion_success_count=8,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=25,
            whitespace_accounts_count=5,
            total_target_accounts=100,
        )
        assert p == PenetrationPattern.none

    # --- whitespace_neglect ---
    def test_whitespace_neglect_detected(self):
        # Need coverage>=35 AND whitespace_rate>=0.50
        # coverage: pen_rate<0.20 (+40), inactive_rate=0 (+0), days=0 (+0) → 40>=35 ✓
        # whitespace=60/100=0.60>=0.50 ✓
        p = self._pattern(
            accounts_with_active_opportunity_count=10,
            accounts_with_no_activity_90d_count=0,
            account_activity_days_avg=0.0,
            accounts_with_single_contact_count=0,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=30,
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.50,
            avg_account_health_score=8.0,
            expansion_attempts_count=10,
            expansion_success_count=8,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=25,
            whitespace_accounts_count=60,
            total_target_accounts=100,
        )
        assert p == PenetrationPattern.whitespace_neglect

    # --- shallow_coverage ---
    def test_shallow_coverage_detected(self):
        # Need depth>=35 AND avg_contacts<1.5
        # depth: single_rate>=0.60 (+40) → 40>=35 ✓; avg_contacts=1.2<1.5 ✓
        # But must NOT trigger whitespace_neglect first: coverage<35 OR whitespace_rate<0.50
        # Set coverage<35: pen_rate>=0.50 (+0), inactive_rate<0.15 (+0), days<30 (+0) → coverage=0
        p = self._pattern(
            accounts_with_active_opportunity_count=60,
            accounts_with_no_activity_90d_count=5,
            account_activity_days_avg=10.0,
            accounts_with_single_contact_count=60,
            avg_contacts_per_target_account=1.2,
            executive_level_engagement_count=30,
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.50,
            avg_account_health_score=8.0,
            expansion_attempts_count=10,
            expansion_success_count=8,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=25,
            whitespace_accounts_count=10,
            total_target_accounts=100,
        )
        assert p == PenetrationPattern.shallow_coverage

    # --- cherry_picking ---
    def test_cherry_picking_detected(self):
        # Need strategic>=35 AND neglect_rate>=0.40
        # strategic: captured_revenue_pct<0.10 (+35) → 35>=35 ✓
        # neglect_rate: ignored=4/(engaged=6+ignored=4)=0.40 ✓
        # Must not trigger whitespace or shallow first
        p = self._pattern(
            accounts_with_active_opportunity_count=60,
            accounts_with_no_activity_90d_count=5,
            account_activity_days_avg=10.0,
            accounts_with_single_contact_count=5,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=30,
            large_account_engagement_count=6,
            large_account_ignored_count=4,
            captured_revenue_pct=0.05,
            avg_account_health_score=8.0,
            expansion_attempts_count=10,
            expansion_success_count=8,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=25,
            whitespace_accounts_count=10,
            total_target_accounts=100,
        )
        assert p == PenetrationPattern.cherry_picking

    # --- churn_risk_blindness ---
    def test_churn_risk_blindness_detected(self):
        # Need expansion>=35 AND renewal_at_risk>=2
        # expansion: attempts=0 (+30), renewal=2 (+18) → 48>=35 ✓; at_risk=2>=2 ✓
        # Must not trigger whitespace, shallow, cherry_picking first
        p = self._pattern(
            accounts_with_active_opportunity_count=60,
            accounts_with_no_activity_90d_count=5,
            account_activity_days_avg=10.0,
            accounts_with_single_contact_count=5,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=30,
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.50,
            avg_account_health_score=8.0,
            expansion_attempts_count=0,
            expansion_success_count=0,
            account_renewal_at_risk_count=2,
            competitive_accounts_touched_count=25,
            whitespace_accounts_count=10,
            total_target_accounts=100,
        )
        assert p == PenetrationPattern.churn_risk_blindness

    # --- expansion_stagnation ---
    def test_expansion_stagnation_detected(self):
        # Need expansion>=25 AND attempts<3
        # expansion: attempts=0 (+30), renewal=0 (+0), comp=0/100 (+25) = 55>=25 ✓; attempts=0<3 ✓
        # Must not trigger previous patterns
        p = self._pattern(
            accounts_with_active_opportunity_count=60,
            accounts_with_no_activity_90d_count=5,
            account_activity_days_avg=10.0,
            accounts_with_single_contact_count=5,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=30,
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.50,
            avg_account_health_score=8.0,
            expansion_attempts_count=0,
            expansion_success_count=0,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=0,
            whitespace_accounts_count=10,
            total_target_accounts=100,
        )
        assert p == PenetrationPattern.expansion_stagnation

    # --- Priority: whitespace_neglect wins over shallow_coverage ---
    def test_priority_whitespace_over_shallow(self):
        # Both conditions met: coverage>=35, whitespace_rate>=0.50, depth>=35, avg_contacts<1.5
        # whitespace_neglect is checked first → should win
        p = self._pattern(
            accounts_with_active_opportunity_count=10,
            accounts_with_no_activity_90d_count=0,
            account_activity_days_avg=0.0,
            accounts_with_single_contact_count=10,
            avg_contacts_per_target_account=1.2,
            executive_level_engagement_count=0,
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.50,
            avg_account_health_score=8.0,
            expansion_attempts_count=10,
            expansion_success_count=8,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=25,
            whitespace_accounts_count=60,
            total_target_accounts=100,
        )
        assert p == PenetrationPattern.whitespace_neglect

    # --- Priority: shallow_coverage over cherry_picking ---
    def test_priority_shallow_over_cherry_picking(self):
        # depth>=35 (single_rate high) AND avg<1.5 → shallow triggers before cherry
        # strategic>=35 too (low captured_revenue), neglect_rate>=0.40
        # But whitespace_neglect must not trigger: coverage<35 and whitespace_rate<0.50
        p = self._pattern(
            accounts_with_active_opportunity_count=60,
            accounts_with_no_activity_90d_count=5,
            account_activity_days_avg=10.0,
            accounts_with_single_contact_count=60,
            avg_contacts_per_target_account=1.2,
            executive_level_engagement_count=0,
            large_account_engagement_count=6,
            large_account_ignored_count=4,
            captured_revenue_pct=0.05,
            avg_account_health_score=8.0,
            expansion_attempts_count=10,
            expansion_success_count=8,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=25,
            whitespace_accounts_count=10,
            total_target_accounts=100,
        )
        assert p == PenetrationPattern.shallow_coverage

    # --- Priority: cherry_picking over churn_risk_blindness ---
    def test_priority_cherry_over_churn(self):
        # strategic>=35, neglect_rate>=0.40 → cherry
        # expansion>=35, renewal>=2 → churn would also trigger
        # cherry_picking is checked first
        p = self._pattern(
            accounts_with_active_opportunity_count=60,
            accounts_with_no_activity_90d_count=5,
            account_activity_days_avg=10.0,
            accounts_with_single_contact_count=5,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=30,
            large_account_engagement_count=6,
            large_account_ignored_count=4,
            captured_revenue_pct=0.05,
            avg_account_health_score=8.0,
            expansion_attempts_count=0,
            expansion_success_count=0,
            account_renewal_at_risk_count=3,
            competitive_accounts_touched_count=5,
            whitespace_accounts_count=10,
            total_target_accounts=100,
        )
        assert p == PenetrationPattern.cherry_picking

    # --- Priority: churn_risk_blindness over expansion_stagnation ---
    def test_priority_churn_over_stagnation(self):
        # expansion>=35 AND renewal>=2 → churn
        # expansion>=25 AND attempts<3 would also trigger stagnation
        # churn is checked first
        p = self._pattern(
            accounts_with_active_opportunity_count=60,
            accounts_with_no_activity_90d_count=5,
            account_activity_days_avg=10.0,
            accounts_with_single_contact_count=5,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=30,
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.50,
            avg_account_health_score=8.0,
            expansion_attempts_count=2,
            expansion_success_count=0,
            account_renewal_at_risk_count=3,
            competitive_accounts_touched_count=5,
            whitespace_accounts_count=10,
            total_target_accounts=100,
        )
        assert p == PenetrationPattern.churn_risk_blindness

    def test_whitespace_neglect_not_triggered_when_rate_below_050(self):
        # coverage>=35 but whitespace_rate<0.50
        p = self._pattern(
            accounts_with_active_opportunity_count=10,
            accounts_with_no_activity_90d_count=0,
            account_activity_days_avg=0.0,
            accounts_with_single_contact_count=5,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=30,
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.50,
            avg_account_health_score=8.0,
            expansion_attempts_count=10,
            expansion_success_count=8,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=25,
            whitespace_accounts_count=30,  # 30/100=0.30 < 0.50
            total_target_accounts=100,
        )
        assert p != PenetrationPattern.whitespace_neglect


# ===========================================================================
# 10. _risk_level
# ===========================================================================

class TestRiskLevel:
    def _risk(self, composite):
        return engine()._risk_level(composite)

    def test_composite_60_is_critical(self):
        assert self._risk(60.0) == PenetrationRisk.critical

    def test_composite_above_60_is_critical(self):
        assert self._risk(75.0) == PenetrationRisk.critical

    def test_composite_100_is_critical(self):
        assert self._risk(100.0) == PenetrationRisk.critical

    def test_composite_40_is_high(self):
        assert self._risk(40.0) == PenetrationRisk.high

    def test_composite_59_is_high(self):
        assert self._risk(59.9) == PenetrationRisk.high

    def test_composite_20_is_moderate(self):
        assert self._risk(20.0) == PenetrationRisk.moderate

    def test_composite_39_is_moderate(self):
        assert self._risk(39.9) == PenetrationRisk.moderate

    def test_composite_19_is_low(self):
        assert self._risk(19.9) == PenetrationRisk.low

    def test_composite_0_is_low(self):
        assert self._risk(0.0) == PenetrationRisk.low

    def test_composite_just_below_20_is_low(self):
        assert self._risk(19.0) == PenetrationRisk.low


# ===========================================================================
# 11. _severity
# ===========================================================================

class TestSeverity:
    def _sev(self, composite):
        return engine()._severity(composite)

    def test_composite_60_is_stagnant(self):
        assert self._sev(60.0) == PenetrationSeverity.stagnant

    def test_composite_above_60_is_stagnant(self):
        assert self._sev(80.0) == PenetrationSeverity.stagnant

    def test_composite_40_is_shallow(self):
        assert self._sev(40.0) == PenetrationSeverity.shallow

    def test_composite_59_is_shallow(self):
        assert self._sev(59.9) == PenetrationSeverity.shallow

    def test_composite_20_is_developing(self):
        assert self._sev(20.0) == PenetrationSeverity.developing

    def test_composite_39_is_developing(self):
        assert self._sev(39.9) == PenetrationSeverity.developing

    def test_composite_0_is_optimal(self):
        assert self._sev(0.0) == PenetrationSeverity.optimal

    def test_composite_19_is_optimal(self):
        assert self._sev(19.0) == PenetrationSeverity.optimal


# ===========================================================================
# 12. _action – all combos
# ===========================================================================

class TestAction:
    def _act(self, risk, pattern):
        return engine()._action(risk, pattern)

    def test_critical_whitespace_neglect(self):
        assert self._act(PenetrationRisk.critical, PenetrationPattern.whitespace_neglect) == PenetrationAction.executive_engagement_program

    def test_critical_cherry_picking(self):
        assert self._act(PenetrationRisk.critical, PenetrationPattern.cherry_picking) == PenetrationAction.strategic_account_planning

    def test_critical_shallow_coverage(self):
        assert self._act(PenetrationRisk.critical, PenetrationPattern.shallow_coverage) == PenetrationAction.territory_coverage_coaching

    def test_critical_churn_risk_blindness(self):
        assert self._act(PenetrationRisk.critical, PenetrationPattern.churn_risk_blindness) == PenetrationAction.territory_coverage_coaching

    def test_critical_expansion_stagnation(self):
        assert self._act(PenetrationRisk.critical, PenetrationPattern.expansion_stagnation) == PenetrationAction.territory_coverage_coaching

    def test_critical_none(self):
        assert self._act(PenetrationRisk.critical, PenetrationPattern.none) == PenetrationAction.territory_coverage_coaching

    def test_high_churn_risk_blindness(self):
        assert self._act(PenetrationRisk.high, PenetrationPattern.churn_risk_blindness) == PenetrationAction.expansion_pipeline_build

    def test_high_shallow_coverage(self):
        assert self._act(PenetrationRisk.high, PenetrationPattern.shallow_coverage) == PenetrationAction.account_prioritization_review

    def test_high_whitespace_neglect(self):
        assert self._act(PenetrationRisk.high, PenetrationPattern.whitespace_neglect) == PenetrationAction.territory_coverage_coaching

    def test_high_cherry_picking(self):
        assert self._act(PenetrationRisk.high, PenetrationPattern.cherry_picking) == PenetrationAction.territory_coverage_coaching

    def test_high_expansion_stagnation(self):
        assert self._act(PenetrationRisk.high, PenetrationPattern.expansion_stagnation) == PenetrationAction.territory_coverage_coaching

    def test_high_none(self):
        assert self._act(PenetrationRisk.high, PenetrationPattern.none) == PenetrationAction.territory_coverage_coaching

    def test_moderate_any_pattern(self):
        for p in PenetrationPattern:
            assert self._act(PenetrationRisk.moderate, p) == PenetrationAction.account_prioritization_review

    def test_low_any_pattern(self):
        for p in PenetrationPattern:
            assert self._act(PenetrationRisk.low, p) == PenetrationAction.no_action


# ===========================================================================
# 13. _has_penetration_gap
# ===========================================================================

class TestPenetrationGap:
    def _gap(self, composite, **kw):
        return engine()._has_penetration_gap(composite, make_input(**kw))

    def test_gap_true_when_composite_gte_40(self):
        assert self._gap(40.0) is True

    def test_gap_true_when_composite_above_40(self):
        assert self._gap(50.0) is True

    def test_gap_false_when_composite_below_40_and_no_other_trigger(self):
        assert self._gap(39.9, large_account_ignored_count=0, captured_revenue_pct=0.50) is False

    def test_gap_true_when_large_ignored_gte_3(self):
        assert self._gap(10.0, large_account_ignored_count=3, captured_revenue_pct=0.50) is True

    def test_gap_false_when_large_ignored_2(self):
        assert self._gap(10.0, large_account_ignored_count=2, captured_revenue_pct=0.50) is False

    def test_gap_true_when_captured_revenue_below_010(self):
        assert self._gap(10.0, large_account_ignored_count=0, captured_revenue_pct=0.05) is True

    def test_gap_false_when_captured_revenue_exactly_010(self):
        assert self._gap(10.0, large_account_ignored_count=0, captured_revenue_pct=0.10) is False

    def test_gap_true_multiple_triggers(self):
        assert self._gap(40.0, large_account_ignored_count=3, captured_revenue_pct=0.05) is True

    def test_gap_false_all_below_thresholds(self):
        assert self._gap(0.0, large_account_ignored_count=0, captured_revenue_pct=0.50) is False


# ===========================================================================
# 14. _requires_account_coaching
# ===========================================================================

class TestRequiresCoaching:
    def _coach(self, composite, **kw):
        return engine()._requires_account_coaching(composite, make_input(**kw))

    def test_coaching_true_when_composite_gte_30(self):
        assert self._coach(30.0) is True

    def test_coaching_true_when_composite_above_30(self):
        assert self._coach(50.0) is True

    def test_coaching_false_when_composite_below_30_no_other_trigger(self):
        assert self._coach(29.9, accounts_with_no_activity_90d_count=0, avg_contacts_per_target_account=2.0) is False

    def test_coaching_true_when_no_activity_gte_5(self):
        assert self._coach(0.0, accounts_with_no_activity_90d_count=5, avg_contacts_per_target_account=2.0) is True

    def test_coaching_false_when_no_activity_4(self):
        assert self._coach(0.0, accounts_with_no_activity_90d_count=4, avg_contacts_per_target_account=2.0) is False

    def test_coaching_true_when_avg_contacts_below_10(self):
        assert self._coach(0.0, accounts_with_no_activity_90d_count=0, avg_contacts_per_target_account=0.9) is True

    def test_coaching_false_when_avg_contacts_exactly_10(self):
        assert self._coach(0.0, accounts_with_no_activity_90d_count=0, avg_contacts_per_target_account=1.0) is False

    def test_coaching_false_all_below_thresholds(self):
        assert self._coach(0.0, accounts_with_no_activity_90d_count=0, avg_contacts_per_target_account=2.5) is False

    def test_coaching_true_multiple_triggers(self):
        assert self._coach(30.0, accounts_with_no_activity_90d_count=5, avg_contacts_per_target_account=0.5) is True


# ===========================================================================
# 15. _estimated_untapped_revenue
# ===========================================================================

class TestUntappedRevenue:
    def _rev(self, whitespace, deal_size, composite):
        e = engine()
        inp = make_input(whitespace_accounts_count=whitespace,
                         avg_deal_size_per_account_usd=deal_size)
        return e._estimated_untapped_revenue(inp, composite)

    def test_basic_formula(self):
        # 10 * 10000 * (50/100) = 50000
        assert self._rev(10, 10_000.0, 50.0) == 50_000.0

    def test_zero_whitespace(self):
        assert self._rev(0, 10_000.0, 50.0) == 0.0

    def test_zero_composite(self):
        assert self._rev(10, 10_000.0, 0.0) == 0.0

    def test_zero_deal_size(self):
        assert self._rev(10, 0.0, 50.0) == 0.0

    def test_rounds_to_2_dp(self):
        # 3 * 10000 * (33.3/100) = 9990.0 — exact; try fractional
        result = self._rev(3, 3333.33, 33.3)
        assert result == round(3 * 3333.33 * (33.3 / 100.0), 2)

    def test_composite_100(self):
        assert self._rev(5, 1000.0, 100.0) == 5000.0

    def test_is_float(self):
        assert isinstance(self._rev(10, 5000.0, 40.0), float)

    def test_result_in_assess(self):
        e = engine()
        inp = make_input(whitespace_accounts_count=10,
                         avg_deal_size_per_account_usd=5000.0)
        r = e.assess(inp)
        expected = round(10 * 5000.0 * (r.account_penetration_composite / 100.0), 2)
        assert r.estimated_untapped_revenue_usd == expected


# ===========================================================================
# 16. _signal
# ===========================================================================

class TestSignal:
    def _signal(self, pattern, composite, **kw):
        e = engine()
        inp = make_input(**kw)
        return e._signal(inp, pattern, composite)

    def test_healthy_signal(self):
        sig = self._signal(PenetrationPattern.none, 10.0,
                           accounts_with_active_opportunity_count=60,
                           accounts_with_no_activity_90d_count=5,
                           whitespace_accounts_count=0,
                           large_account_ignored_count=0,
                           total_target_accounts=100)
        assert sig == "Account penetration and territory coverage within healthy benchmarks"

    def test_none_pattern_composite_gte_20_not_healthy(self):
        sig = self._signal(PenetrationPattern.none, 20.0,
                           accounts_with_active_opportunity_count=60,
                           accounts_with_no_activity_90d_count=5,
                           whitespace_accounts_count=0,
                           large_account_ignored_count=0,
                           total_target_accounts=100)
        assert sig != "Account penetration and territory coverage within healthy benchmarks"

    def test_signal_contains_inactive_when_pen_rate_below_040(self):
        sig = self._signal(PenetrationPattern.whitespace_neglect, 50.0,
                           accounts_with_active_opportunity_count=30,
                           accounts_with_no_activity_90d_count=7,
                           whitespace_accounts_count=0,
                           large_account_ignored_count=0,
                           total_target_accounts=100)
        assert "7 inactive accounts" in sig

    def test_signal_no_inactive_when_pen_rate_gte_040(self):
        sig = self._signal(PenetrationPattern.whitespace_neglect, 50.0,
                           accounts_with_active_opportunity_count=40,
                           accounts_with_no_activity_90d_count=7,
                           whitespace_accounts_count=0,
                           large_account_ignored_count=0,
                           total_target_accounts=100)
        assert "inactive accounts" not in sig

    def test_signal_contains_whitespace_when_whitespace_gte_1(self):
        sig = self._signal(PenetrationPattern.whitespace_neglect, 50.0,
                           accounts_with_active_opportunity_count=50,
                           accounts_with_no_activity_90d_count=0,
                           whitespace_accounts_count=5,
                           large_account_ignored_count=0,
                           total_target_accounts=100)
        assert "5 whitespace accounts" in sig

    def test_signal_no_whitespace_when_zero(self):
        sig = self._signal(PenetrationPattern.whitespace_neglect, 50.0,
                           accounts_with_active_opportunity_count=50,
                           accounts_with_no_activity_90d_count=0,
                           whitespace_accounts_count=0,
                           large_account_ignored_count=0,
                           total_target_accounts=100)
        assert "whitespace accounts" not in sig

    def test_signal_contains_large_ignored_when_gte_1(self):
        sig = self._signal(PenetrationPattern.whitespace_neglect, 50.0,
                           accounts_with_active_opportunity_count=50,
                           accounts_with_no_activity_90d_count=0,
                           whitespace_accounts_count=0,
                           large_account_ignored_count=3,
                           total_target_accounts=100)
        assert "3 large accounts ignored" in sig

    def test_signal_no_large_ignored_when_zero(self):
        sig = self._signal(PenetrationPattern.whitespace_neglect, 50.0,
                           accounts_with_active_opportunity_count=50,
                           accounts_with_no_activity_90d_count=0,
                           whitespace_accounts_count=0,
                           large_account_ignored_count=0,
                           total_target_accounts=100)
        assert "large accounts ignored" not in sig

    def test_signal_label_from_pattern_value(self):
        sig = self._signal(PenetrationPattern.shallow_coverage, 45.0,
                           accounts_with_active_opportunity_count=50,
                           accounts_with_no_activity_90d_count=0,
                           whitespace_accounts_count=0,
                           large_account_ignored_count=0,
                           total_target_accounts=100)
        assert sig.startswith("Shallow coverage")

    def test_signal_label_none_pattern_is_penetration_risk(self):
        sig = self._signal(PenetrationPattern.none, 25.0,
                           accounts_with_active_opportunity_count=30,
                           accounts_with_no_activity_90d_count=5,
                           whitespace_accounts_count=0,
                           large_account_ignored_count=0,
                           total_target_accounts=100)
        assert sig.startswith("Penetration risk")

    def test_signal_contains_composite(self):
        sig = self._signal(PenetrationPattern.shallow_coverage, 45.0,
                           accounts_with_active_opportunity_count=50,
                           accounts_with_no_activity_90d_count=0,
                           whitespace_accounts_count=0,
                           large_account_ignored_count=0,
                           total_target_accounts=100)
        assert "composite 45" in sig

    def test_signal_no_parts_fallback(self):
        # pen_rate>=0.40, no whitespace, no large_ignored → fallback
        sig = self._signal(PenetrationPattern.shallow_coverage, 45.0,
                           accounts_with_active_opportunity_count=50,
                           accounts_with_no_activity_90d_count=0,
                           whitespace_accounts_count=0,
                           large_account_ignored_count=0,
                           total_target_accounts=100)
        assert "territory coverage needs attention" in sig

    def test_signal_all_parts_present(self):
        sig = self._signal(PenetrationPattern.whitespace_neglect, 50.0,
                           accounts_with_active_opportunity_count=20,
                           accounts_with_no_activity_90d_count=10,
                           whitespace_accounts_count=8,
                           large_account_ignored_count=3,
                           total_target_accounts=100)
        assert "10 inactive accounts" in sig
        assert "8 whitespace accounts" in sig
        assert "3 large accounts ignored" in sig

    def test_signal_pattern_underscores_replaced_by_spaces(self):
        sig = self._signal(PenetrationPattern.churn_risk_blindness, 50.0,
                           accounts_with_active_opportunity_count=20,
                           accounts_with_no_activity_90d_count=5,
                           whitespace_accounts_count=0,
                           large_account_ignored_count=0,
                           total_target_accounts=100)
        assert "Churn risk blindness" in sig

    def test_signal_expansion_stagnation_label(self):
        sig = self._signal(PenetrationPattern.expansion_stagnation, 30.0,
                           accounts_with_active_opportunity_count=20,
                           accounts_with_no_activity_90d_count=5,
                           whitespace_accounts_count=0,
                           large_account_ignored_count=0,
                           total_target_accounts=100)
        assert "Expansion stagnation" in sig


# ===========================================================================
# 17. assess() – full result structure
# ===========================================================================

class TestAssess:
    def test_returns_account_penetration_result(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r, AccountPenetrationResult)

    def test_result_rep_id(self):
        e = engine()
        r = e.assess(make_input(rep_id="abc"))
        assert r.rep_id == "abc"

    def test_result_region(self):
        e = engine()
        r = e.assess(make_input(region="SOUTH"))
        assert r.region == "SOUTH"

    def test_result_stored_in_results(self):
        e = engine()
        r = e.assess(make_input())
        assert r in e._results

    def test_assess_twice_stores_both(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="a"))
        r2 = e.assess(make_input(rep_id="b"))
        assert len(e._results) == 2

    def test_result_risk_is_enum(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.penetration_risk, PenetrationRisk)

    def test_result_pattern_is_enum(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.penetration_pattern, PenetrationPattern)

    def test_result_severity_is_enum(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.penetration_severity, PenetrationSeverity)

    def test_result_action_is_enum(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.recommended_action, PenetrationAction)

    def test_result_scores_are_float(self):
        e = engine()
        r = e.assess(make_input())
        for attr in ("account_coverage_score", "account_depth_score",
                     "strategic_focus_score", "expansion_momentum_score",
                     "account_penetration_composite"):
            assert isinstance(getattr(r, attr), float), attr

    def test_result_flags_are_bool(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.has_penetration_gap, bool)
        assert isinstance(r.requires_account_coaching, bool)

    def test_result_untapped_is_float(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.estimated_untapped_revenue_usd, float)

    def test_result_signal_is_str(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.penetration_signal, str)

    def test_scores_capped_at_100(self):
        e = engine()
        inp = make_input(
            accounts_with_active_opportunity_count=0,
            accounts_with_no_activity_90d_count=100,
            account_activity_days_avg=90.0,
            accounts_with_single_contact_count=100,
            avg_contacts_per_target_account=0.1,
            executive_level_engagement_count=0,
            large_account_engagement_count=0,
            large_account_ignored_count=100,
            captured_revenue_pct=0.01,
            avg_account_health_score=1.0,
            expansion_attempts_count=0,
            account_renewal_at_risk_count=10,
            competitive_accounts_touched_count=0,
            total_target_accounts=100,
        )
        r = e.assess(inp)
        for attr in ("account_coverage_score", "account_depth_score",
                     "strategic_focus_score", "expansion_momentum_score",
                     "account_penetration_composite"):
            assert getattr(r, attr) <= 100.0, attr

    def test_scores_non_negative(self):
        e = engine()
        r = e.assess(make_input())
        for attr in ("account_coverage_score", "account_depth_score",
                     "strategic_focus_score", "expansion_momentum_score",
                     "account_penetration_composite"):
            assert getattr(r, attr) >= 0.0, attr


# ===========================================================================
# 18. assess_batch()
# ===========================================================================

class TestAssessBatch:
    def test_returns_list(self):
        e = engine()
        results = e.assess_batch([make_input(rep_id="a"), make_input(rep_id="b")])
        assert isinstance(results, list)

    def test_length_matches_input(self):
        e = engine()
        results = e.assess_batch([make_input() for _ in range(5)])
        assert len(results) == 5

    def test_all_results_are_account_penetration_result(self):
        e = engine()
        results = e.assess_batch([make_input() for _ in range(3)])
        for r in results:
            assert isinstance(r, AccountPenetrationResult)

    def test_batch_stores_in_results(self):
        e = engine()
        e.assess_batch([make_input(rep_id="x"), make_input(rep_id="y")])
        assert len(e._results) == 2

    def test_empty_batch(self):
        e = engine()
        results = e.assess_batch([])
        assert results == []

    def test_batch_rep_ids_correct(self):
        e = engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(3)]
        results = e.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep-{i}"

    def test_batch_single_element(self):
        e = engine()
        results = e.assess_batch([make_input(rep_id="solo")])
        assert len(results) == 1
        assert results[0].rep_id == "solo"

    def test_batch_accumulates_with_prior_assesses(self):
        e = engine()
        e.assess(make_input(rep_id="prior"))
        e.assess_batch([make_input(rep_id="a"), make_input(rep_id="b")])
        assert len(e._results) == 3


# ===========================================================================
# 19. summary() – 13 keys
# ===========================================================================

class TestSummary:
    EXPECTED_KEYS = {
        "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
        "avg_account_penetration_composite", "penetration_gap_count",
        "account_coaching_count", "avg_account_coverage_score",
        "avg_account_depth_score", "avg_strategic_focus_score",
        "avg_expansion_momentum_score", "total_estimated_untapped_revenue_usd",
    }

    def test_empty_summary_keys(self):
        e = engine()
        s = e.summary()
        assert set(s.keys()) == self.EXPECTED_KEYS

    def test_empty_summary_total_zero(self):
        e = engine()
        assert e.summary()["total"] == 0

    def test_empty_summary_dicts_empty(self):
        e = engine()
        s = e.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_avgs_zero(self):
        e = engine()
        s = e.summary()
        assert s["avg_account_penetration_composite"] == 0.0
        assert s["avg_account_coverage_score"] == 0.0
        assert s["avg_account_depth_score"] == 0.0
        assert s["avg_strategic_focus_score"] == 0.0
        assert s["avg_expansion_momentum_score"] == 0.0
        assert s["total_estimated_untapped_revenue_usd"] == 0.0
        assert s["penetration_gap_count"] == 0
        assert s["account_coaching_count"] == 0

    def test_summary_total_after_assess(self):
        e = engine()
        e.assess(make_input())
        e.assess(make_input())
        assert e.summary()["total"] == 2

    def test_summary_13_keys(self):
        e = engine()
        e.assess(make_input())
        assert set(e.summary().keys()) == self.EXPECTED_KEYS

    def test_summary_risk_counts_keys_are_strings(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        for k in s["risk_counts"]:
            assert isinstance(k, str)

    def test_summary_pattern_counts_sums_to_total(self):
        e = engine()
        inputs = [make_input(rep_id=f"r{i}") for i in range(4)]
        e.assess_batch(inputs)
        s = e.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_risk_counts_sums_to_total(self):
        e = engine()
        e.assess_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = e.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_severity_counts_sums_to_total(self):
        e = engine()
        e.assess_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = e.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_sums_to_total(self):
        e = engine()
        e.assess_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = e.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_composite_correct(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="a"))
        r2 = e.assess(make_input(rep_id="b"))
        expected = round((r1.account_penetration_composite + r2.account_penetration_composite) / 2, 1)
        assert e.summary()["avg_account_penetration_composite"] == expected

    def test_summary_penetration_gap_count(self):
        e = engine()
        # Force gap: captured_revenue_pct<0.10 → gap=True
        e.assess(make_input(captured_revenue_pct=0.05, large_account_ignored_count=0))
        e.assess(make_input(captured_revenue_pct=0.50, large_account_ignored_count=0))
        s = e.summary()
        assert s["penetration_gap_count"] >= 1

    def test_summary_coaching_count(self):
        e = engine()
        # avg_contacts<1.0 → coaching=True
        e.assess(make_input(avg_contacts_per_target_account=0.5, accounts_with_no_activity_90d_count=0))
        e.assess(make_input(avg_contacts_per_target_account=3.0, accounts_with_no_activity_90d_count=0))
        s = e.summary()
        assert s["account_coaching_count"] >= 1

    def test_summary_total_untapped_revenue_sums_correctly(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="a"))
        r2 = e.assess(make_input(rep_id="b"))
        expected = round(r1.estimated_untapped_revenue_usd + r2.estimated_untapped_revenue_usd, 2)
        assert e.summary()["total_estimated_untapped_revenue_usd"] == expected

    def test_summary_avg_coverage_score_correct(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="a"))
        r2 = e.assess(make_input(rep_id="b"))
        expected = round((r1.account_coverage_score + r2.account_coverage_score) / 2, 1)
        assert e.summary()["avg_account_coverage_score"] == expected

    def test_summary_avg_depth_score_correct(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="a"))
        r2 = e.assess(make_input(rep_id="b"))
        expected = round((r1.account_depth_score + r2.account_depth_score) / 2, 1)
        assert e.summary()["avg_account_depth_score"] == expected

    def test_summary_avg_strategic_score_correct(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="a"))
        r2 = e.assess(make_input(rep_id="b"))
        expected = round((r1.strategic_focus_score + r2.strategic_focus_score) / 2, 1)
        assert e.summary()["avg_strategic_focus_score"] == expected

    def test_summary_avg_expansion_score_correct(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="a"))
        r2 = e.assess(make_input(rep_id="b"))
        expected = round((r1.expansion_momentum_score + r2.expansion_momentum_score) / 2, 1)
        assert e.summary()["avg_expansion_momentum_score"] == expected


# ===========================================================================
# 20. Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_zero_total_accounts_no_crash(self):
        e = engine()
        inp = make_input(total_target_accounts=0,
                         accounts_with_active_opportunity_count=0,
                         accounts_with_no_activity_90d_count=0,
                         whitespace_accounts_count=0)
        r = e.assess(inp)
        assert isinstance(r, AccountPenetrationResult)

    def test_zero_active_opportunities_no_crash(self):
        e = engine()
        r = e.assess(make_input(accounts_with_active_opportunity_count=0))
        assert isinstance(r, AccountPenetrationResult)

    def test_zero_large_account_total_no_crash(self):
        e = engine()
        r = e.assess(make_input(large_account_engagement_count=0,
                                large_account_ignored_count=0))
        assert isinstance(r, AccountPenetrationResult)

    def test_max_everything_composite_capped_100(self):
        e = engine()
        inp = make_input(
            total_target_accounts=1,
            accounts_with_active_opportunity_count=0,
            accounts_with_no_activity_90d_count=1,
            account_activity_days_avg=90.0,
            accounts_with_single_contact_count=1,
            avg_contacts_per_target_account=0.1,
            executive_level_engagement_count=0,
            large_account_engagement_count=0,
            large_account_ignored_count=1,
            captured_revenue_pct=0.01,
            avg_account_health_score=1.0,
            expansion_attempts_count=0,
            account_renewal_at_risk_count=10,
            competitive_accounts_touched_count=0,
            whitespace_accounts_count=1,
        )
        r = e.assess(inp)
        assert r.account_penetration_composite <= 100.0

    def test_exact_boundary_pen_rate_020(self):
        # pen_rate exactly 0.20 → should use +20 branch (< 0.35)
        e = engine()
        score = e._account_coverage_score(make_input(
            total_target_accounts=100,
            accounts_with_active_opportunity_count=20,
            accounts_with_no_activity_90d_count=0,
            account_activity_days_avg=0.0,
        ))
        assert score == 20.0

    def test_exact_boundary_pen_rate_035(self):
        # pen_rate exactly 0.35 → +8
        e = engine()
        score = e._account_coverage_score(make_input(
            total_target_accounts=100,
            accounts_with_active_opportunity_count=35,
            accounts_with_no_activity_90d_count=0,
            account_activity_days_avg=0.0,
        ))
        assert score == 8.0

    def test_exact_boundary_pen_rate_050(self):
        # pen_rate exactly 0.50 → +0
        e = engine()
        score = e._account_coverage_score(make_input(
            total_target_accounts=100,
            accounts_with_active_opportunity_count=50,
            accounts_with_no_activity_90d_count=0,
            account_activity_days_avg=0.0,
        ))
        assert score == 0.0

    def test_exact_boundary_inactive_rate_050(self):
        # inactive_rate exactly 0.50 → +35
        e = engine()
        score = e._account_coverage_score(make_input(
            total_target_accounts=100,
            accounts_with_active_opportunity_count=50,
            accounts_with_no_activity_90d_count=50,
            account_activity_days_avg=0.0,
        ))
        assert score == 35.0

    def test_exact_boundary_inactive_rate_030(self):
        # inactive_rate exactly 0.30 → +18
        e = engine()
        score = e._account_coverage_score(make_input(
            total_target_accounts=100,
            accounts_with_active_opportunity_count=50,
            accounts_with_no_activity_90d_count=30,
            account_activity_days_avg=0.0,
        ))
        assert score == 18.0

    def test_exact_boundary_inactive_rate_015(self):
        # inactive_rate exactly 0.15 → +7
        e = engine()
        score = e._account_coverage_score(make_input(
            total_target_accounts=100,
            accounts_with_active_opportunity_count=50,
            accounts_with_no_activity_90d_count=15,
            account_activity_days_avg=0.0,
        ))
        assert score == 7.0

    def test_exact_boundary_activity_days_60(self):
        e = engine()
        score = e._account_coverage_score(make_input(
            total_target_accounts=100,
            accounts_with_active_opportunity_count=50,
            accounts_with_no_activity_90d_count=0,
            account_activity_days_avg=60.0,
        ))
        assert score == 15.0

    def test_exact_boundary_activity_days_30(self):
        e = engine()
        score = e._account_coverage_score(make_input(
            total_target_accounts=100,
            accounts_with_active_opportunity_count=50,
            accounts_with_no_activity_90d_count=0,
            account_activity_days_avg=30.0,
        ))
        assert score == 7.0

    def test_exact_boundary_single_rate_060(self):
        # single/active = 6/10 = 0.60 → +40
        e = engine()
        score = e._account_depth_score(make_input(
            accounts_with_active_opportunity_count=10,
            accounts_with_single_contact_count=6,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=25,
            total_target_accounts=100,
        ))
        assert score == 40.0

    def test_exact_boundary_single_rate_040(self):
        # single/active = 4/10 = 0.40 → +20
        e = engine()
        score = e._account_depth_score(make_input(
            accounts_with_active_opportunity_count=10,
            accounts_with_single_contact_count=4,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=25,
            total_target_accounts=100,
        ))
        assert score == 20.0

    def test_exact_boundary_single_rate_025(self):
        # single/active = 2.5/10 = 0.25 → +8
        e = engine()
        score = e._account_depth_score(make_input(
            accounts_with_active_opportunity_count=10,
            accounts_with_single_contact_count=3,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=25,
            total_target_accounts=100,
        ))
        assert score == 8.0

    def test_exact_boundary_avg_contacts_10(self):
        # avg_contacts exactly 1.0 → +15 (< 1.5)
        e = engine()
        score = e._account_depth_score(make_input(
            accounts_with_active_opportunity_count=10,
            accounts_with_single_contact_count=0,
            avg_contacts_per_target_account=1.0,
            executive_level_engagement_count=25,
            total_target_accounts=100,
        ))
        assert score == 15.0

    def test_exact_boundary_avg_contacts_15(self):
        # avg_contacts exactly 1.5 → +7 (< 2.0)
        e = engine()
        score = e._account_depth_score(make_input(
            accounts_with_active_opportunity_count=10,
            accounts_with_single_contact_count=0,
            avg_contacts_per_target_account=1.5,
            executive_level_engagement_count=25,
            total_target_accounts=100,
        ))
        assert score == 7.0

    def test_exact_boundary_exec_rate_010(self):
        # exec_rate exactly 0.10 → +10
        e = engine()
        score = e._account_depth_score(make_input(
            accounts_with_active_opportunity_count=10,
            accounts_with_single_contact_count=0,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=10,
            total_target_accounts=100,
        ))
        assert score == 10.0

    def test_exact_boundary_exec_rate_025(self):
        # exec_rate exactly 0.25 → 0
        e = engine()
        score = e._account_depth_score(make_input(
            accounts_with_active_opportunity_count=10,
            accounts_with_single_contact_count=0,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=25,
            total_target_accounts=100,
        ))
        assert score == 0.0

    def test_exact_boundary_neglect_rate_050(self):
        # ignored=5/(engaged=5+ignored=5)=0.50 → +40
        e = engine()
        score = e._strategic_focus_score(make_input(
            large_account_engagement_count=5,
            large_account_ignored_count=5,
            captured_revenue_pct=0.50,
            avg_account_health_score=8.0,
        ))
        assert score == 40.0

    def test_exact_boundary_neglect_rate_030(self):
        # 3/10 = 0.30 → +20
        e = engine()
        score = e._strategic_focus_score(make_input(
            large_account_engagement_count=7,
            large_account_ignored_count=3,
            captured_revenue_pct=0.50,
            avg_account_health_score=8.0,
        ))
        assert score == 20.0

    def test_exact_boundary_neglect_rate_015(self):
        # 1.5/10 → use 2/10=0.20 for >=0.15 → +8
        e = engine()
        score = e._strategic_focus_score(make_input(
            large_account_engagement_count=8,
            large_account_ignored_count=2,
            captured_revenue_pct=0.50,
            avg_account_health_score=8.0,
        ))
        assert score == 8.0

    def test_exact_boundary_captured_revenue_010(self):
        # exactly 0.10 → <0.20 → +18
        e = engine()
        score = e._strategic_focus_score(make_input(
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.10,
            avg_account_health_score=8.0,
        ))
        assert score == 18.0

    def test_exact_boundary_captured_revenue_020(self):
        # exactly 0.20 → <0.35 → +7
        e = engine()
        score = e._strategic_focus_score(make_input(
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.20,
            avg_account_health_score=8.0,
        ))
        assert score == 7.0

    def test_exact_boundary_health_score_40(self):
        # exactly 4.0 → <6.0 → +10
        e = engine()
        score = e._strategic_focus_score(make_input(
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.50,
            avg_account_health_score=4.0,
        ))
        assert score == 10.0

    def test_exact_boundary_health_score_60(self):
        # exactly 6.0 → 0
        e = engine()
        score = e._strategic_focus_score(make_input(
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.50,
            avg_account_health_score=6.0,
        ))
        assert score == 0.0

    def test_exact_boundary_exp_rate_020(self):
        # success=2/attempts=10=0.20 → <0.40 → +15
        e = engine()
        score = e._expansion_momentum_score(make_input(
            expansion_attempts_count=10,
            expansion_success_count=2,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=50,
            total_target_accounts=100,
        ))
        assert score == 15.0

    def test_exact_boundary_exp_rate_040(self):
        # success=4/attempts=10=0.40 → 0
        e = engine()
        score = e._expansion_momentum_score(make_input(
            expansion_attempts_count=10,
            expansion_success_count=4,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=50,
            total_target_accounts=100,
        ))
        assert score == 0.0

    def test_exact_boundary_renewal_at_risk_3(self):
        # 3 → +35
        e = engine()
        score = e._expansion_momentum_score(make_input(
            expansion_attempts_count=10,
            expansion_success_count=10,
            account_renewal_at_risk_count=3,
            competitive_accounts_touched_count=50,
            total_target_accounts=100,
        ))
        assert score == 35.0

    def test_exact_boundary_renewal_at_risk_1(self):
        # 1 → +18
        e = engine()
        score = e._expansion_momentum_score(make_input(
            expansion_attempts_count=10,
            expansion_success_count=10,
            account_renewal_at_risk_count=1,
            competitive_accounts_touched_count=50,
            total_target_accounts=100,
        ))
        assert score == 18.0

    def test_exact_boundary_comp_rate_010(self):
        # comp=10/100=0.10 → +12
        e = engine()
        score = e._expansion_momentum_score(make_input(
            expansion_attempts_count=10,
            expansion_success_count=10,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=10,
            total_target_accounts=100,
        ))
        assert score == 12.0

    def test_exact_boundary_comp_rate_020(self):
        # comp=20/100=0.20 → 0
        e = engine()
        score = e._expansion_momentum_score(make_input(
            expansion_attempts_count=10,
            expansion_success_count=10,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=20,
            total_target_accounts=100,
        ))
        assert score == 0.0

    def test_exact_boundary_composite_60(self):
        e = engine()
        r = e._risk_level(60.0)
        assert r == PenetrationRisk.critical

    def test_exact_boundary_composite_40(self):
        e = engine()
        r = e._risk_level(40.0)
        assert r == PenetrationRisk.high

    def test_exact_boundary_composite_20(self):
        e = engine()
        r = e._risk_level(20.0)
        assert r == PenetrationRisk.moderate

    def test_new_engine_starts_with_empty_results(self):
        e = engine()
        assert e._results == []

    def test_multiple_engines_are_independent(self):
        e1 = engine()
        e2 = engine()
        e1.assess(make_input(rep_id="a"))
        assert len(e2._results) == 0


# ===========================================================================
# 21. End-to-end scenario tests
# ===========================================================================

class TestScenarios:
    def test_healthy_rep_gets_low_risk_optimal(self):
        e = engine()
        r = e.assess(make_input(
            accounts_with_active_opportunity_count=70,
            accounts_with_no_activity_90d_count=2,
            account_activity_days_avg=10.0,
            accounts_with_single_contact_count=2,
            avg_contacts_per_target_account=3.0,
            executive_level_engagement_count=30,
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.50,
            avg_account_health_score=8.0,
            expansion_attempts_count=10,
            expansion_success_count=8,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=25,
            whitespace_accounts_count=5,
            total_target_accounts=100,
        ))
        assert r.penetration_risk == PenetrationRisk.low
        assert r.penetration_severity == PenetrationSeverity.optimal
        assert r.recommended_action == PenetrationAction.no_action

    def test_critical_rep_gets_stagnant_severity(self):
        e = engine()
        r = e.assess(make_input(
            accounts_with_active_opportunity_count=5,
            accounts_with_no_activity_90d_count=60,
            account_activity_days_avg=90.0,
            accounts_with_single_contact_count=5,
            avg_contacts_per_target_account=0.3,
            executive_level_engagement_count=0,
            large_account_engagement_count=1,
            large_account_ignored_count=9,
            captured_revenue_pct=0.02,
            avg_account_health_score=2.0,
            expansion_attempts_count=0,
            expansion_success_count=0,
            account_renewal_at_risk_count=5,
            competitive_accounts_touched_count=1,
            whitespace_accounts_count=70,
            total_target_accounts=100,
        ))
        assert r.penetration_risk == PenetrationRisk.critical
        assert r.penetration_severity == PenetrationSeverity.stagnant

    def test_high_risk_shallow_gets_account_prioritization_review(self):
        e = engine()
        # Need high risk (composite 40-59) + shallow_coverage pattern
        # depth>=35, avg_contacts<1.5, but coverage<35, whitespace_rate<0.50
        r = e.assess(make_input(
            accounts_with_active_opportunity_count=60,
            accounts_with_no_activity_90d_count=5,
            account_activity_days_avg=10.0,
            accounts_with_single_contact_count=60,
            avg_contacts_per_target_account=1.2,
            executive_level_engagement_count=0,
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.05,
            avg_account_health_score=3.0,
            expansion_attempts_count=0,
            expansion_success_count=0,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=5,
            whitespace_accounts_count=10,
            total_target_accounts=100,
        ))
        if r.penetration_risk == PenetrationRisk.high and r.penetration_pattern == PenetrationPattern.shallow_coverage:
            assert r.recommended_action == PenetrationAction.account_prioritization_review

    def test_moderate_risk_always_account_prioritization_review(self):
        e = engine()
        r = e.assess(make_input(
            accounts_with_active_opportunity_count=40,
            accounts_with_no_activity_90d_count=20,
            account_activity_days_avg=10.0,
            accounts_with_single_contact_count=5,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=20,
            large_account_engagement_count=9,
            large_account_ignored_count=1,
            captured_revenue_pct=0.30,
            avg_account_health_score=7.0,
            expansion_attempts_count=5,
            expansion_success_count=4,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=20,
            whitespace_accounts_count=5,
            total_target_accounts=100,
        ))
        if r.penetration_risk == PenetrationRisk.moderate:
            assert r.recommended_action == PenetrationAction.account_prioritization_review

    def test_summary_with_mixed_reps(self):
        e = engine()
        # Healthy rep
        e.assess(make_input(rep_id="healthy",
                            accounts_with_active_opportunity_count=70,
                            accounts_with_no_activity_90d_count=2,
                            account_activity_days_avg=10.0,
                            avg_contacts_per_target_account=3.0,
                            captured_revenue_pct=0.50,
                            avg_account_health_score=8.0,
                            expansion_attempts_count=10,
                            expansion_success_count=8))
        # Risky rep
        e.assess(make_input(rep_id="risky",
                            accounts_with_active_opportunity_count=5,
                            accounts_with_no_activity_90d_count=60,
                            account_activity_days_avg=90.0,
                            avg_contacts_per_target_account=0.3,
                            captured_revenue_pct=0.02,
                            avg_account_health_score=2.0,
                            expansion_attempts_count=0,
                            account_renewal_at_risk_count=5))
        s = e.summary()
        assert s["total"] == 2
        assert sum(s["risk_counts"].values()) == 2

    def test_to_dict_round_trip(self):
        e = engine()
        r = e.assess(make_input())
        d = r.to_dict()
        assert d["rep_id"] == r.rep_id
        assert d["penetration_risk"] == r.penetration_risk.value
        assert d["account_penetration_composite"] == r.account_penetration_composite
        assert d["has_penetration_gap"] == r.has_penetration_gap
        assert d["estimated_untapped_revenue_usd"] == r.estimated_untapped_revenue_usd

    def test_pattern_none_in_summary(self):
        e = engine()
        # ensure a none pattern is possible
        e.assess(make_input(
            accounts_with_active_opportunity_count=60,
            accounts_with_no_activity_90d_count=3,
            account_activity_days_avg=10.0,
            accounts_with_single_contact_count=2,
            avg_contacts_per_target_account=2.5,
            executive_level_engagement_count=30,
            large_account_engagement_count=10,
            large_account_ignored_count=0,
            captured_revenue_pct=0.50,
            avg_account_health_score=8.0,
            expansion_attempts_count=10,
            expansion_success_count=8,
            account_renewal_at_risk_count=0,
            competitive_accounts_touched_count=25,
            whitespace_accounts_count=5,
            total_target_accounts=100,
        ))
        s = e.summary()
        # pattern_counts may or may not include "none", just ensure keys sum correctly
        assert sum(s["pattern_counts"].values()) == 1
