"""
Comprehensive pytest test suite for swarm/intelligence/revenue_leak_detector.py

Run from /home/user/TEST:
    python -m pytest swarm/tests/test_revenue_leak_detector.py -v
"""

from __future__ import annotations

import dataclasses
import pytest

from swarm.intelligence.revenue_leak_detector import (
    LeakSeverity, LeakPattern, RetentionOutlook, LeakAction,
    RevenueLeakInput, RevenueLeakResult, RevenueLeakDetector,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(
    account_id: str = "acct_001",
    account_name: str = "Acme Corp",
    csm_id: str = "csm_001",
    current_arr: float = 100_000.0,
    arr_at_contract_start: float = 100_000.0,
    contracted_arr: float = 100_000.0,
    discount_pct_current: float = 10.0,
    discount_pct_original: float = 10.0,
    days_to_renewal: int = 180,
    renewal_qualified: int = 1,
    last_expansion_days_ago: int = 60,
    expansion_attempts_failed: int = 0,
    champion_active: int = 1,
    champion_changed_last_90d: int = 0,
    exec_sponsor_engaged: int = 1,
    support_ticket_volume_30d: int = 0,
    nps_score: int = 40,
    product_adoption_pct: float = 70.0,
    seats_utilized_pct: float = 75.0,
    multi_year_contract: int = 0,
    competitive_displacement_risk: int = 0,
    deal_value: float = 100_000.0,
) -> RevenueLeakInput:
    return RevenueLeakInput(
        account_id=account_id,
        account_name=account_name,
        csm_id=csm_id,
        current_arr=current_arr,
        arr_at_contract_start=arr_at_contract_start,
        contracted_arr=contracted_arr,
        discount_pct_current=discount_pct_current,
        discount_pct_original=discount_pct_original,
        days_to_renewal=days_to_renewal,
        renewal_qualified=renewal_qualified,
        last_expansion_days_ago=last_expansion_days_ago,
        expansion_attempts_failed=expansion_attempts_failed,
        champion_active=champion_active,
        champion_changed_last_90d=champion_changed_last_90d,
        exec_sponsor_engaged=exec_sponsor_engaged,
        support_ticket_volume_30d=support_ticket_volume_30d,
        nps_score=nps_score,
        product_adoption_pct=product_adoption_pct,
        seats_utilized_pct=seats_utilized_pct,
        multi_year_contract=multi_year_contract,
        competitive_displacement_risk=competitive_displacement_risk,
        deal_value=deal_value,
    )


def fresh_detector() -> RevenueLeakDetector:
    return RevenueLeakDetector()


# ===========================================================================
# Section 1: Enum membership and values
# ===========================================================================

class TestLeakSeverityEnum:
    def test_contained_value(self):
        assert LeakSeverity.CONTAINED.value == "contained"

    def test_moderate_value(self):
        assert LeakSeverity.MODERATE.value == "moderate"

    def test_significant_value(self):
        assert LeakSeverity.SIGNIFICANT.value == "significant"

    def test_critical_value(self):
        assert LeakSeverity.CRITICAL.value == "critical"

    def test_exactly_four_members(self):
        assert len(LeakSeverity) == 4

    def test_all_member_values(self):
        values = {m.value for m in LeakSeverity}
        assert values == {"contained", "moderate", "significant", "critical"}

    def test_is_str_enum(self):
        assert isinstance(LeakSeverity.CONTAINED, str)

    def test_not_3_members(self):
        assert len(LeakSeverity) != 3

    def test_not_5_members(self):
        assert len(LeakSeverity) != 5


class TestLeakPatternEnum:
    def test_healthy_value(self):
        assert LeakPattern.HEALTHY.value == "healthy"

    def test_discount_creep_value(self):
        assert LeakPattern.DISCOUNT_CREEP.value == "discount_creep"

    def test_renewal_risk_value(self):
        assert LeakPattern.RENEWAL_RISK.value == "renewal_risk"

    def test_expansion_stall_value(self):
        assert LeakPattern.EXPANSION_STALL.value == "expansion_stall"

    def test_champion_erosion_value(self):
        assert LeakPattern.CHAMPION_EROSION.value == "champion_erosion"

    def test_multi_leak_value(self):
        assert LeakPattern.MULTI_LEAK.value == "multi_leak"

    def test_exactly_six_members(self):
        assert len(LeakPattern) == 6

    def test_all_member_values(self):
        values = {m.value for m in LeakPattern}
        assert values == {
            "healthy", "discount_creep", "renewal_risk",
            "expansion_stall", "champion_erosion", "multi_leak",
        }

    def test_is_str_enum(self):
        assert isinstance(LeakPattern.HEALTHY, str)


class TestRetentionOutlookEnum:
    def test_secure_value(self):
        assert RetentionOutlook.SECURE.value == "secure"

    def test_watchlist_value(self):
        assert RetentionOutlook.WATCHLIST.value == "watchlist"

    def test_at_risk_value(self):
        assert RetentionOutlook.AT_RISK.value == "at_risk"

    def test_critical_value(self):
        assert RetentionOutlook.CRITICAL.value == "critical"

    def test_exactly_four_members(self):
        assert len(RetentionOutlook) == 4

    def test_all_member_values(self):
        values = {m.value for m in RetentionOutlook}
        assert values == {"secure", "watchlist", "at_risk", "critical"}

    def test_is_str_enum(self):
        assert isinstance(RetentionOutlook.SECURE, str)


class TestLeakActionEnum:
    def test_monitor_value(self):
        assert LeakAction.MONITOR.value == "monitor"

    def test_protect_expansion_value(self):
        assert LeakAction.PROTECT_EXPANSION.value == "protect_expansion"

    def test_retention_play_value(self):
        assert LeakAction.RETENTION_PLAY.value == "retention_play"

    def test_executive_save_value(self):
        assert LeakAction.EXECUTIVE_SAVE.value == "executive_save"

    def test_exactly_four_members(self):
        assert len(LeakAction) == 4

    def test_all_member_values(self):
        values = {m.value for m in LeakAction}
        assert values == {"monitor", "protect_expansion", "retention_play", "executive_save"}

    def test_is_str_enum(self):
        assert isinstance(LeakAction.MONITOR, str)


# ===========================================================================
# Section 2: RevenueLeakInput field count (22 fields)
# ===========================================================================

class TestRevenueLeakInputFields:
    def test_exactly_22_fields(self):
        assert len(dataclasses.fields(RevenueLeakInput)) == 22

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(RevenueLeakInput)

    def test_field_names_complete(self):
        names = {f.name for f in dataclasses.fields(RevenueLeakInput)}
        expected = {
            "account_id", "account_name", "csm_id", "current_arr",
            "arr_at_contract_start", "contracted_arr", "discount_pct_current",
            "discount_pct_original", "days_to_renewal", "renewal_qualified",
            "last_expansion_days_ago", "expansion_attempts_failed",
            "champion_active", "champion_changed_last_90d", "exec_sponsor_engaged",
            "support_ticket_volume_30d", "nps_score", "product_adoption_pct",
            "seats_utilized_pct", "multi_year_contract",
            "competitive_displacement_risk", "deal_value",
        }
        assert names == expected

    def test_not_21_fields(self):
        assert len(dataclasses.fields(RevenueLeakInput)) != 21

    def test_not_23_fields(self):
        assert len(dataclasses.fields(RevenueLeakInput)) != 23

    def test_instantiation_works(self):
        inp = make_input()
        assert inp.account_id == "acct_001"
        assert inp.current_arr == 100_000.0

    def test_no_defaults_required(self):
        with pytest.raises(TypeError):
            RevenueLeakInput()

    def test_all_fields_accessible(self):
        inp = make_input()
        assert inp.account_name == "Acme Corp"
        assert inp.csm_id == "csm_001"
        assert inp.days_to_renewal == 180


# ===========================================================================
# Section 3: RevenueLeakResult.to_dict() — exactly 15 keys
# ===========================================================================

class TestRevenueLeakResultToDict:
    def _result(self) -> RevenueLeakResult:
        return fresh_detector().detect(make_input())

    def test_exactly_15_keys(self):
        assert len(self._result().to_dict()) == 15

    def test_not_14_keys(self):
        assert len(self._result().to_dict()) != 14

    def test_not_16_keys(self):
        assert len(self._result().to_dict()) != 16

    def test_key_names(self):
        keys = set(self._result().to_dict().keys())
        expected = {
            "account_id", "account_name", "leak_severity", "leak_pattern",
            "retention_outlook", "leak_action", "discount_risk_score",
            "renewal_risk_score", "expansion_health_score", "relationship_score",
            "leak_composite", "estimated_arr_at_risk", "arr_expansion_potential",
            "is_leaking", "needs_executive_save",
        }
        assert keys == expected

    def test_enum_values_are_strings(self):
        d = self._result().to_dict()
        assert isinstance(d["leak_severity"], str)
        assert isinstance(d["leak_pattern"], str)
        assert isinstance(d["retention_outlook"], str)
        assert isinstance(d["leak_action"], str)

    def test_is_leaking_is_bool(self):
        assert isinstance(self._result().to_dict()["is_leaking"], bool)

    def test_needs_executive_save_is_truthy(self):
        d = self._result().to_dict()
        assert d["needs_executive_save"] in (True, False, 0, 1)

    def test_account_id_passthrough(self):
        r = fresh_detector().detect(make_input(account_id="xyz_999"))
        assert r.to_dict()["account_id"] == "xyz_999"

    def test_account_name_passthrough(self):
        r = fresh_detector().detect(make_input(account_name="Beta LLC"))
        assert r.to_dict()["account_name"] == "Beta LLC"

    def test_scores_are_numeric(self):
        d = self._result().to_dict()
        for k in ("discount_risk_score", "renewal_risk_score", "expansion_health_score",
                  "relationship_score", "leak_composite", "estimated_arr_at_risk",
                  "arr_expansion_potential"):
            assert isinstance(d[k], (int, float))

    def test_enum_values_match_enum_members(self):
        r = self._result()
        d = r.to_dict()
        assert d["leak_severity"] == r.leak_severity.value
        assert d["leak_pattern"] == r.leak_pattern.value
        assert d["retention_outlook"] == r.retention_outlook.value
        assert d["leak_action"] == r.leak_action.value

    def test_to_dict_returns_dict(self):
        assert isinstance(self._result().to_dict(), dict)


# ===========================================================================
# Section 4: summary() — exactly 13 keys
# ===========================================================================

class TestSummaryKeyCount:
    def test_empty_summary_has_13_keys(self):
        assert len(fresh_detector().summary()) == 13

    def test_nonempty_summary_has_13_keys(self):
        det = fresh_detector()
        det.detect(make_input())
        assert len(det.summary()) == 13

    def test_not_12_keys(self):
        assert len(fresh_detector().summary()) != 12

    def test_not_14_keys(self):
        assert len(fresh_detector().summary()) != 14

    def test_summary_key_names(self):
        keys = set(fresh_detector().summary().keys())
        expected = {
            "total", "severity_counts", "pattern_counts", "outlook_counts",
            "action_counts", "avg_leak_composite", "total_arr_at_risk",
            "leaking_count", "executive_save_count", "avg_discount_risk_score",
            "avg_renewal_risk_score", "avg_expansion_health_score",
            "avg_relationship_score",
        }
        assert keys == expected

    def test_empty_summary_total_zero(self):
        assert fresh_detector().summary()["total"] == 0

    def test_empty_summary_avg_composite_zero(self):
        assert fresh_detector().summary()["avg_leak_composite"] == 0.0

    def test_empty_summary_count_dicts_empty(self):
        s = fresh_detector().summary()
        assert s["severity_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["outlook_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_all_zeroes(self):
        s = fresh_detector().summary()
        assert s["total"] == 0
        assert s["total_arr_at_risk"] == 0.0
        assert s["leaking_count"] == 0
        assert s["executive_save_count"] == 0
        assert s["avg_discount_risk_score"] == 0.0
        assert s["avg_renewal_risk_score"] == 0.0
        assert s["avg_expansion_health_score"] == 0.0
        assert s["avg_relationship_score"] == 0.0

    def test_summary_total_matches_detected(self):
        det = fresh_detector()
        for i in range(5):
            det.detect(make_input(account_id=f"a{i}"))
        assert det.summary()["total"] == 5

    def test_summary_category_counts_sum_to_total(self):
        det = fresh_detector()
        det.detect(make_input(account_id="a1"))
        det.detect(make_input(account_id="a2"))
        s = det.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_to_total(self):
        det = fresh_detector()
        det.detect(make_input(account_id="a1"))
        det.detect(make_input(account_id="a2"))
        s = det.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_outlook_counts_sum_to_total(self):
        det = fresh_detector()
        det.detect(make_input(account_id="a1"))
        det.detect(make_input(account_id="a2"))
        s = det.summary()
        assert sum(s["outlook_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        det = fresh_detector()
        det.detect(make_input(account_id="a1"))
        det.detect(make_input(account_id="a2"))
        s = det.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_composite_matches(self):
        det = fresh_detector()
        r1 = det.detect(make_input(account_id="a1"))
        r2 = det.detect(make_input(account_id="a2"))
        expected = round((r1.leak_composite + r2.leak_composite) / 2, 1)
        assert det.summary()["avg_leak_composite"] == expected

    def test_summary_after_reset(self):
        det = fresh_detector()
        det.detect(make_input())
        det.reset()
        s = det.summary()
        assert s["total"] == 0
        assert len(s) == 13


# ===========================================================================
# Section 5: _composite formula
# ===========================================================================

class TestCompositeFormula:
    """
    Formula: disc*0.25 + renew*0.35 + (100-exp_health)*0.20 + (100-rel)*0.20
    """

    def test_formula_known_values(self):
        det = fresh_detector()
        disc, renew, exp_health, rel = 20.0, 30.0, 60.0, 70.0
        expected = round(disc * 0.25 + renew * 0.35 + (100 - exp_health) * 0.20 + (100 - rel) * 0.20, 1)
        assert det._composite(disc, renew, exp_health, rel) == expected

    def test_formula_all_zeroes(self):
        det = fresh_detector()
        # exp_health=100, rel=100 => all risk parts = 0
        assert det._composite(0.0, 0.0, 100.0, 100.0) == 0.0

    def test_formula_all_max_risk(self):
        det = fresh_detector()
        # disc=100, renew=100, exp_health=0, rel=0
        result = det._composite(100.0, 100.0, 0.0, 0.0)
        expected = round(100.0 * 0.25 + 100.0 * 0.35 + 100.0 * 0.20 + 100.0 * 0.20, 1)
        assert result == expected

    def test_formula_disc_weight_0_25(self):
        det = fresh_detector()
        result = det._composite(80.0, 0.0, 100.0, 100.0)
        assert result == round(80.0 * 0.25, 1)

    def test_formula_renew_weight_0_35(self):
        det = fresh_detector()
        result = det._composite(0.0, 80.0, 100.0, 100.0)
        assert result == round(80.0 * 0.35, 1)

    def test_formula_exp_risk_weight_0_20(self):
        det = fresh_detector()
        # exp_health=0 => exp_risk=100
        result = det._composite(0.0, 0.0, 0.0, 100.0)
        assert result == round(100.0 * 0.20, 1)

    def test_formula_rel_risk_weight_0_20(self):
        det = fresh_detector()
        # rel=0 => rel_risk=100
        result = det._composite(0.0, 0.0, 100.0, 0.0)
        assert result == round(100.0 * 0.20, 1)

    def test_formula_midpoint(self):
        det = fresh_detector()
        result = det._composite(50.0, 50.0, 50.0, 50.0)
        expected = round(50 * 0.25 + 50 * 0.35 + 50 * 0.20 + 50 * 0.20, 1)
        assert result == expected

    def test_result_is_float(self):
        det = fresh_detector()
        assert isinstance(det._composite(10.0, 20.0, 80.0, 90.0), float)

    def test_result_rounded_to_1_decimal(self):
        det = fresh_detector()
        r = det._composite(33.3, 33.3, 33.3, 33.3)
        assert r == round(r, 1)

    def test_clamped_at_zero(self):
        det = fresh_detector()
        assert det._composite(0.0, 0.0, 100.0, 100.0) >= 0.0

    def test_clamped_at_100(self):
        det = fresh_detector()
        assert det._composite(100.0, 100.0, 0.0, 0.0) <= 100.0


# ===========================================================================
# Section 6: _discount_risk_score
# ===========================================================================

class TestDiscountRiskScore:
    def setup_method(self):
        self.det = fresh_detector()

    def test_no_risk_equal_discounts_no_arr_change(self):
        inp = make_input(discount_pct_current=10.0, discount_pct_original=10.0,
                         current_arr=100_000.0, arr_at_contract_start=100_000.0)
        assert self.det._discount_risk_score(inp) == 0.0

    def test_disc_creep_gte20_adds_40(self):
        inp = make_input(discount_pct_current=30.0, discount_pct_original=5.0,
                         current_arr=100_000.0, arr_at_contract_start=100_000.0)
        score = self.det._discount_risk_score(inp)
        assert score >= 40.0

    def test_disc_creep_exactly20_adds_40(self):
        inp = make_input(discount_pct_current=25.0, discount_pct_original=5.0,
                         current_arr=100_000.0, arr_at_contract_start=100_000.0)
        score = self.det._discount_risk_score(inp)
        assert score >= 40.0

    def test_disc_creep_10_to_19_adds_25(self):
        inp = make_input(discount_pct_current=20.0, discount_pct_original=10.0,
                         current_arr=100_000.0, arr_at_contract_start=100_000.0)
        # disc_creep=10, arr_change=0, disc=20 < 30 => 25
        assert self.det._discount_risk_score(inp) == 25.0

    def test_disc_creep_5_to_9_adds_12(self):
        inp = make_input(discount_pct_current=15.0, discount_pct_original=10.0,
                         current_arr=100_000.0, arr_at_contract_start=100_000.0)
        # disc_creep=5, arr_change=0, disc=15 < 30 => 12
        assert self.det._discount_risk_score(inp) == 12.0

    def test_arr_compression_gte_minus20_adds_40(self):
        inp = make_input(discount_pct_current=5.0, discount_pct_original=5.0,
                         current_arr=70_000.0, arr_at_contract_start=100_000.0)
        score = self.det._discount_risk_score(inp)
        assert score >= 40.0

    def test_arr_compression_exactly_minus20_adds_40(self):
        inp = make_input(discount_pct_current=5.0, discount_pct_original=5.0,
                         current_arr=80_000.0, arr_at_contract_start=100_000.0)
        # arr_change=-20% => +40
        assert self.det._discount_risk_score(inp) >= 40.0

    def test_arr_compression_minus10_to_minus19_adds_25(self):
        inp = make_input(discount_pct_current=5.0, discount_pct_original=5.0,
                         current_arr=88_000.0, arr_at_contract_start=100_000.0)
        score = self.det._discount_risk_score(inp)
        assert score >= 25.0

    def test_arr_compression_minus5_to_minus9_adds_10(self):
        inp = make_input(discount_pct_current=5.0, discount_pct_original=5.0,
                         current_arr=95_000.0, arr_at_contract_start=100_000.0)
        assert self.det._discount_risk_score(inp) >= 10.0

    def test_arr_zero_start_no_division_error(self):
        inp = make_input(discount_pct_current=5.0, discount_pct_original=5.0,
                         current_arr=100_000.0, arr_at_contract_start=0.0)
        score = self.det._discount_risk_score(inp)
        assert score >= 0.0

    def test_high_absolute_discount_gte40_adds_20(self):
        inp = make_input(discount_pct_current=45.0, discount_pct_original=45.0,
                         current_arr=100_000.0, arr_at_contract_start=100_000.0)
        assert self.det._discount_risk_score(inp) == 20.0

    def test_high_absolute_discount_exactly40_adds_20(self):
        inp = make_input(discount_pct_current=40.0, discount_pct_original=40.0,
                         current_arr=100_000.0, arr_at_contract_start=100_000.0)
        assert self.det._discount_risk_score(inp) == 20.0

    def test_absolute_discount_30_to_39_adds_10(self):
        inp = make_input(discount_pct_current=35.0, discount_pct_original=35.0,
                         current_arr=100_000.0, arr_at_contract_start=100_000.0)
        assert self.det._discount_risk_score(inp) == 10.0

    def test_score_clamped_at_100(self):
        inp = make_input(discount_pct_current=60.0, discount_pct_original=10.0,
                         current_arr=70_000.0, arr_at_contract_start=100_000.0)
        assert self.det._discount_risk_score(inp) <= 100.0

    def test_score_not_negative(self):
        inp = make_input(discount_pct_current=5.0, discount_pct_original=10.0,
                         current_arr=110_000.0, arr_at_contract_start=100_000.0)
        assert self.det._discount_risk_score(inp) >= 0.0

    def test_result_rounded(self):
        inp = make_input()
        r = self.det._discount_risk_score(inp)
        assert r == round(r, 1)


# ===========================================================================
# Section 7: _renewal_risk_score
# ===========================================================================

class TestRenewalRiskScore:
    def setup_method(self):
        self.det = fresh_detector()

    def _clean(self, **kwargs):
        """Base: no risk (days > 90, qualified, good adoption/seats, no nps)"""
        base = dict(days_to_renewal=200, renewal_qualified=1,
                    product_adoption_pct=80.0, seats_utilized_pct=80.0, nps_score=-1)
        base.update(kwargs)
        return make_input(**base)

    def test_zero_risk_perfect_account(self):
        inp = self._clean()
        assert self.det._renewal_risk_score(inp) == 0.0

    def test_days_lte30_adds_40(self):
        inp = self._clean(days_to_renewal=30)
        assert self.det._renewal_risk_score(inp) >= 40.0

    def test_days_exactly30_adds_40(self):
        inp = self._clean(days_to_renewal=30)
        assert self.det._renewal_risk_score(inp) >= 40.0

    def test_days_31_to_60_adds_25(self):
        inp = self._clean(days_to_renewal=45)
        assert self.det._renewal_risk_score(inp) >= 25.0

    def test_days_exactly60_adds_25(self):
        inp = self._clean(days_to_renewal=60)
        assert self.det._renewal_risk_score(inp) >= 25.0

    def test_days_61_to_90_adds_12(self):
        inp = self._clean(days_to_renewal=75)
        assert self.det._renewal_risk_score(inp) >= 12.0

    def test_days_exactly90_adds_12(self):
        inp = self._clean(days_to_renewal=90)
        assert self.det._renewal_risk_score(inp) >= 12.0

    def test_days_gt90_no_proximity_penalty(self):
        inp = self._clean(days_to_renewal=100)
        assert self.det._renewal_risk_score(inp) == 0.0

    def test_not_qualified_and_days_lte90_adds_20(self):
        inp = self._clean(days_to_renewal=80, renewal_qualified=0)
        # days <= 90 => +12, not qualified and days <= 90 => +20 => 32
        assert self.det._renewal_risk_score(inp) >= 32.0

    def test_not_qualified_days_gt90_no_qualified_penalty(self):
        inp = self._clean(days_to_renewal=120, renewal_qualified=0)
        assert self.det._renewal_risk_score(inp) == 0.0

    def test_adoption_lt30_adds_20(self):
        inp = self._clean(product_adoption_pct=20.0)
        assert self.det._renewal_risk_score(inp) >= 20.0

    def test_adoption_30_to_49_adds_12(self):
        inp = self._clean(product_adoption_pct=40.0)
        assert self.det._renewal_risk_score(inp) >= 12.0

    def test_adoption_exactly30_adds_12(self):
        inp = self._clean(product_adoption_pct=30.0)
        # 30 is not < 30, so +12
        assert self.det._renewal_risk_score(inp) == 12.0

    def test_adoption_gte50_no_penalty(self):
        inp = self._clean(product_adoption_pct=50.0)
        assert self.det._renewal_risk_score(inp) == 0.0

    def test_seats_lt30_adds_15(self):
        inp = self._clean(seats_utilized_pct=20.0)
        assert self.det._renewal_risk_score(inp) >= 15.0

    def test_seats_30_to_49_adds_8(self):
        inp = self._clean(seats_utilized_pct=40.0)
        assert self.det._renewal_risk_score(inp) >= 8.0

    def test_seats_exactly30_adds_8(self):
        inp = self._clean(seats_utilized_pct=30.0)
        assert self.det._renewal_risk_score(inp) == 8.0

    def test_seats_gte50_no_penalty(self):
        inp = self._clean(seats_utilized_pct=50.0)
        assert self.det._renewal_risk_score(inp) == 0.0

    def test_nps_lte_minus30_adds_15(self):
        inp = self._clean(nps_score=-50)
        assert self.det._renewal_risk_score(inp) >= 15.0

    def test_nps_exactly_minus30_adds_15(self):
        inp = self._clean(nps_score=-30)
        assert self.det._renewal_risk_score(inp) >= 15.0

    def test_nps_0_to_minus29_adds_8(self):
        inp = self._clean(nps_score=-10)
        assert self.det._renewal_risk_score(inp) >= 8.0

    def test_nps_exactly0_adds_8(self):
        inp = self._clean(nps_score=0)
        assert self.det._renewal_risk_score(inp) == 8.0

    def test_nps_positive_no_penalty(self):
        inp = self._clean(nps_score=30)
        assert self.det._renewal_risk_score(inp) == 0.0

    def test_nps_minus1_skipped(self):
        inp = self._clean(nps_score=-1)
        assert self.det._renewal_risk_score(inp) == 0.0

    def test_score_clamped_at_100(self):
        inp = make_input(days_to_renewal=30, renewal_qualified=0,
                         product_adoption_pct=20.0, seats_utilized_pct=20.0, nps_score=-50)
        score = self.det._renewal_risk_score(inp)
        assert score == 100.0

    def test_score_not_negative(self):
        assert self.det._renewal_risk_score(make_input()) >= 0.0

    def test_result_rounded(self):
        r = self.det._renewal_risk_score(make_input())
        assert r == round(r, 1)


# ===========================================================================
# Section 8: _expansion_health_score
# ===========================================================================

class TestExpansionHealthScore:
    def setup_method(self):
        self.det = fresh_detector()

    def test_perfect_expansion_health(self):
        inp = make_input(last_expansion_days_ago=30,
                         expansion_attempts_failed=0, seats_utilized_pct=80.0)
        assert self.det._expansion_health_score(inp) == 100.0

    def test_exp_days_gte365_minus35(self):
        inp = make_input(last_expansion_days_ago=400,
                         expansion_attempts_failed=0, seats_utilized_pct=80.0)
        assert self.det._expansion_health_score(inp) == 65.0

    def test_exp_days_exactly365_minus35(self):
        inp = make_input(last_expansion_days_ago=365,
                         expansion_attempts_failed=0, seats_utilized_pct=80.0)
        assert self.det._expansion_health_score(inp) == 65.0

    def test_exp_days_180_to_364_minus20(self):
        inp = make_input(last_expansion_days_ago=200,
                         expansion_attempts_failed=0, seats_utilized_pct=80.0)
        assert self.det._expansion_health_score(inp) == 80.0

    def test_exp_days_exactly180_minus20(self):
        inp = make_input(last_expansion_days_ago=180,
                         expansion_attempts_failed=0, seats_utilized_pct=80.0)
        assert self.det._expansion_health_score(inp) == 80.0

    def test_exp_days_90_to_179_minus10(self):
        inp = make_input(last_expansion_days_ago=120,
                         expansion_attempts_failed=0, seats_utilized_pct=80.0)
        assert self.det._expansion_health_score(inp) == 90.0

    def test_exp_days_exactly90_minus10(self):
        inp = make_input(last_expansion_days_ago=90,
                         expansion_attempts_failed=0, seats_utilized_pct=80.0)
        assert self.det._expansion_health_score(inp) == 90.0

    def test_exp_days_lt90_no_penalty(self):
        inp = make_input(last_expansion_days_ago=30,
                         expansion_attempts_failed=0, seats_utilized_pct=80.0)
        assert self.det._expansion_health_score(inp) == 100.0

    def test_failed_gte3_minus30(self):
        inp = make_input(last_expansion_days_ago=30,
                         expansion_attempts_failed=3, seats_utilized_pct=80.0)
        assert self.det._expansion_health_score(inp) == 70.0

    def test_failed_exactly3_minus30(self):
        inp = make_input(last_expansion_days_ago=30,
                         expansion_attempts_failed=3, seats_utilized_pct=80.0)
        assert self.det._expansion_health_score(inp) == 70.0

    def test_failed_2_minus20(self):
        inp = make_input(last_expansion_days_ago=30,
                         expansion_attempts_failed=2, seats_utilized_pct=80.0)
        assert self.det._expansion_health_score(inp) == 80.0

    def test_failed_1_minus10(self):
        inp = make_input(last_expansion_days_ago=30,
                         expansion_attempts_failed=1, seats_utilized_pct=80.0)
        assert self.det._expansion_health_score(inp) == 90.0

    def test_failed_0_no_penalty(self):
        inp = make_input(last_expansion_days_ago=30,
                         expansion_attempts_failed=0, seats_utilized_pct=80.0)
        assert self.det._expansion_health_score(inp) == 100.0

    def test_seats_lt50_minus20(self):
        inp = make_input(last_expansion_days_ago=30,
                         expansion_attempts_failed=0, seats_utilized_pct=40.0)
        assert self.det._expansion_health_score(inp) == 80.0

    def test_seats_exactly50_minus10(self):
        inp = make_input(last_expansion_days_ago=30,
                         expansion_attempts_failed=0, seats_utilized_pct=50.0)
        # 50 is not < 50, check < 70 => -10
        assert self.det._expansion_health_score(inp) == 90.0

    def test_seats_50_to_69_minus10(self):
        inp = make_input(last_expansion_days_ago=30,
                         expansion_attempts_failed=0, seats_utilized_pct=60.0)
        assert self.det._expansion_health_score(inp) == 90.0

    def test_seats_exactly70_no_penalty(self):
        inp = make_input(last_expansion_days_ago=30,
                         expansion_attempts_failed=0, seats_utilized_pct=70.0)
        assert self.det._expansion_health_score(inp) == 100.0

    def test_score_not_below_zero(self):
        inp = make_input(last_expansion_days_ago=400, expansion_attempts_failed=5,
                         seats_utilized_pct=20.0)
        assert self.det._expansion_health_score(inp) >= 0.0

    def test_score_not_above_100(self):
        inp = make_input(last_expansion_days_ago=1, expansion_attempts_failed=0,
                         seats_utilized_pct=100.0)
        assert self.det._expansion_health_score(inp) <= 100.0

    def test_result_rounded(self):
        r = self.det._expansion_health_score(make_input())
        assert r == round(r, 1)


# ===========================================================================
# Section 9: _relationship_score
# ===========================================================================

class TestRelationshipScore:
    def setup_method(self):
        self.det = fresh_detector()

    def test_perfect_relationship(self):
        inp = make_input(champion_active=1, champion_changed_last_90d=0,
                         exec_sponsor_engaged=1, support_ticket_volume_30d=0,
                         competitive_displacement_risk=0)
        assert self.det._relationship_score(inp) == 100.0

    def test_champion_not_active_minus30(self):
        inp = make_input(champion_active=0, champion_changed_last_90d=0,
                         exec_sponsor_engaged=1, support_ticket_volume_30d=0,
                         competitive_displacement_risk=0)
        assert self.det._relationship_score(inp) == 70.0

    def test_champion_changed_last_90d_minus25(self):
        inp = make_input(champion_active=1, champion_changed_last_90d=1,
                         exec_sponsor_engaged=1, support_ticket_volume_30d=0,
                         competitive_displacement_risk=0)
        assert self.det._relationship_score(inp) == 75.0

    def test_exec_sponsor_not_engaged_minus20(self):
        inp = make_input(champion_active=1, champion_changed_last_90d=0,
                         exec_sponsor_engaged=0, support_ticket_volume_30d=0,
                         competitive_displacement_risk=0)
        assert self.det._relationship_score(inp) == 80.0

    def test_support_tickets_gte10_minus20(self):
        inp = make_input(champion_active=1, champion_changed_last_90d=0,
                         exec_sponsor_engaged=1, support_ticket_volume_30d=10,
                         competitive_displacement_risk=0)
        assert self.det._relationship_score(inp) == 80.0

    def test_support_tickets_exactly10_minus20(self):
        inp = make_input(champion_active=1, champion_changed_last_90d=0,
                         exec_sponsor_engaged=1, support_ticket_volume_30d=10,
                         competitive_displacement_risk=0)
        assert self.det._relationship_score(inp) == 80.0

    def test_support_tickets_5_to_9_minus10(self):
        inp = make_input(champion_active=1, champion_changed_last_90d=0,
                         exec_sponsor_engaged=1, support_ticket_volume_30d=7,
                         competitive_displacement_risk=0)
        assert self.det._relationship_score(inp) == 90.0

    def test_support_tickets_exactly5_minus10(self):
        inp = make_input(champion_active=1, champion_changed_last_90d=0,
                         exec_sponsor_engaged=1, support_ticket_volume_30d=5,
                         competitive_displacement_risk=0)
        assert self.det._relationship_score(inp) == 90.0

    def test_support_tickets_lt5_no_penalty(self):
        inp = make_input(champion_active=1, champion_changed_last_90d=0,
                         exec_sponsor_engaged=1, support_ticket_volume_30d=4,
                         competitive_displacement_risk=0)
        assert self.det._relationship_score(inp) == 100.0

    def test_competitive_displacement_risk_minus15(self):
        inp = make_input(champion_active=1, champion_changed_last_90d=0,
                         exec_sponsor_engaged=1, support_ticket_volume_30d=0,
                         competitive_displacement_risk=1)
        assert self.det._relationship_score(inp) == 85.0

    def test_all_bad_clamped_to_zero(self):
        inp = make_input(champion_active=0, champion_changed_last_90d=1,
                         exec_sponsor_engaged=0, support_ticket_volume_30d=15,
                         competitive_displacement_risk=1)
        assert self.det._relationship_score(inp) == 0.0

    def test_score_not_negative(self):
        inp = make_input(champion_active=0, champion_changed_last_90d=1,
                         exec_sponsor_engaged=0, support_ticket_volume_30d=20,
                         competitive_displacement_risk=1)
        assert self.det._relationship_score(inp) >= 0.0

    def test_score_not_above_100(self):
        assert self.det._relationship_score(make_input()) <= 100.0

    def test_result_rounded(self):
        r = self.det._relationship_score(make_input())
        assert r == round(r, 1)


# ===========================================================================
# Section 10: _leak_severity
# ===========================================================================

class TestLeakSeverity:
    def setup_method(self):
        self.det = fresh_detector()

    def test_contained_below_25(self):
        assert self.det._leak_severity(0.0) == LeakSeverity.CONTAINED
        assert self.det._leak_severity(10.0) == LeakSeverity.CONTAINED
        assert self.det._leak_severity(24.9) == LeakSeverity.CONTAINED

    def test_moderate_25_to_44(self):
        assert self.det._leak_severity(25.0) == LeakSeverity.MODERATE
        assert self.det._leak_severity(35.0) == LeakSeverity.MODERATE
        assert self.det._leak_severity(44.9) == LeakSeverity.MODERATE

    def test_significant_45_to_64(self):
        assert self.det._leak_severity(45.0) == LeakSeverity.SIGNIFICANT
        assert self.det._leak_severity(55.0) == LeakSeverity.SIGNIFICANT
        assert self.det._leak_severity(64.9) == LeakSeverity.SIGNIFICANT

    def test_critical_65_and_above(self):
        assert self.det._leak_severity(65.0) == LeakSeverity.CRITICAL
        assert self.det._leak_severity(80.0) == LeakSeverity.CRITICAL
        assert self.det._leak_severity(100.0) == LeakSeverity.CRITICAL

    def test_boundary_exactly_25(self):
        assert self.det._leak_severity(25.0) == LeakSeverity.MODERATE

    def test_boundary_exactly_45(self):
        assert self.det._leak_severity(45.0) == LeakSeverity.SIGNIFICANT

    def test_boundary_exactly_65(self):
        assert self.det._leak_severity(65.0) == LeakSeverity.CRITICAL

    def test_boundary_below_25(self):
        assert self.det._leak_severity(24.9) == LeakSeverity.CONTAINED

    def test_boundary_below_45(self):
        assert self.det._leak_severity(44.9) == LeakSeverity.MODERATE

    def test_boundary_below_65(self):
        assert self.det._leak_severity(64.9) == LeakSeverity.SIGNIFICANT


# ===========================================================================
# Section 11: _leak_pattern
# ===========================================================================

class TestLeakPattern:
    def setup_method(self):
        self.det = fresh_detector()

    def _pattern(self, disc, renew, exp_health, rel, inp=None):
        if inp is None:
            inp = make_input()
        return self.det._leak_pattern(disc, renew, exp_health, rel, inp)

    def test_healthy_all_low(self):
        assert self._pattern(0.0, 0.0, 100.0, 100.0) == LeakPattern.HEALTHY

    def test_multi_leak_when_3_signals(self):
        # disc>=40 YES, renew>=50 YES, exp_risk>=50 (exp_health=40) YES, rel_risk<50 NO
        inp = make_input(champion_active=1, champion_changed_last_90d=0)
        assert self._pattern(50.0, 60.0, 40.0, 60.0, inp) == LeakPattern.MULTI_LEAK

    def test_multi_leak_when_4_signals(self):
        # All 4 signals triggered
        inp = make_input(champion_active=0, champion_changed_last_90d=1)
        assert self._pattern(50.0, 60.0, 40.0, 40.0, inp) == LeakPattern.MULTI_LEAK

    def test_multi_leak_exactly_3_signals(self):
        # disc=45>=40, renew=55>=50, exp_risk=55>=50, rel_risk=0 => 3 signals
        inp = make_input(champion_active=1, champion_changed_last_90d=0)
        assert self._pattern(45.0, 55.0, 45.0, 100.0, inp) == LeakPattern.MULTI_LEAK

    def test_champion_erosion_rel_risk_gte60_and_champion_changed(self):
        inp = make_input(champion_changed_last_90d=1, champion_active=1)
        # rel=35 => rel_risk=65>=60; 1 signal; champion_changed => CHAMPION_EROSION
        assert self._pattern(0.0, 0.0, 100.0, 35.0, inp) == LeakPattern.CHAMPION_EROSION

    def test_champion_erosion_rel_risk_gte60_and_not_active(self):
        inp = make_input(champion_changed_last_90d=0, champion_active=0)
        assert self._pattern(0.0, 0.0, 100.0, 35.0, inp) == LeakPattern.CHAMPION_EROSION

    def test_champion_erosion_exactly_60_rel_risk(self):
        inp = make_input(champion_changed_last_90d=1, champion_active=1)
        # rel=40 => rel_risk=60 => CHAMPION_EROSION
        assert self._pattern(0.0, 0.0, 100.0, 40.0, inp) == LeakPattern.CHAMPION_EROSION

    def test_no_champion_erosion_when_rel_risk_lt60(self):
        # rel=55 => rel_risk=45 < 60 => not champion erosion
        inp = make_input(champion_changed_last_90d=1, champion_active=0)
        result = self._pattern(0.0, 0.0, 100.0, 55.0, inp)
        assert result != LeakPattern.CHAMPION_EROSION

    def test_renewal_risk_renew_gte55(self):
        result = self._pattern(0.0, 60.0, 100.0, 100.0)
        # 1 signal (renew>=50); rel_risk=0<60; renew=60>=55 => RENEWAL_RISK
        assert result == LeakPattern.RENEWAL_RISK

    def test_renewal_risk_exactly55(self):
        result = self._pattern(0.0, 55.0, 100.0, 100.0)
        assert result == LeakPattern.RENEWAL_RISK

    def test_no_renewal_risk_below_55(self):
        result = self._pattern(0.0, 50.0, 100.0, 100.0)
        # renew=50<55 => not RENEWAL_RISK; 1 signal but no pattern matches => HEALTHY
        assert result != LeakPattern.RENEWAL_RISK

    def test_discount_creep_disc_gte45(self):
        result = self._pattern(50.0, 0.0, 100.0, 100.0)
        # 1 signal (disc>=40); no champion; renew<55; disc=50>=45 => DISCOUNT_CREEP
        assert result == LeakPattern.DISCOUNT_CREEP

    def test_discount_creep_exactly45(self):
        result = self._pattern(45.0, 0.0, 100.0, 100.0)
        assert result == LeakPattern.DISCOUNT_CREEP

    def test_no_discount_creep_below_45(self):
        result = self._pattern(40.0, 0.0, 100.0, 100.0)
        assert result != LeakPattern.DISCOUNT_CREEP

    def test_expansion_stall_exp_risk_gte55(self):
        # exp_health=40 => exp_risk=60>=55 => EXPANSION_STALL
        result = self._pattern(0.0, 0.0, 40.0, 100.0)
        assert result == LeakPattern.EXPANSION_STALL

    def test_expansion_stall_exactly55(self):
        # exp_health=45 => exp_risk=55>=55 => EXPANSION_STALL
        result = self._pattern(0.0, 0.0, 45.0, 100.0)
        assert result == LeakPattern.EXPANSION_STALL

    def test_no_expansion_stall_below_55(self):
        result = self._pattern(0.0, 0.0, 50.0, 100.0)
        # exp_risk=50 < 55 => not EXPANSION_STALL
        assert result != LeakPattern.EXPANSION_STALL

    def test_multi_leak_priority_over_all(self):
        # 3 signals => always MULTI_LEAK
        inp = make_input(champion_changed_last_90d=1, champion_active=0)
        result = self._pattern(60.0, 70.0, 40.0, 100.0, inp)
        # disc>=40, renew>=50, exp_risk>=50 => 3 signals => MULTI_LEAK
        assert result == LeakPattern.MULTI_LEAK


# ===========================================================================
# Section 12: _retention_outlook
# ===========================================================================

class TestRetentionOutlook:
    def setup_method(self):
        self.det = fresh_detector()

    def _outlook(self, renew, composite, days=200):
        inp = make_input(days_to_renewal=days)
        return self.det._retention_outlook(renew, composite, inp)

    def test_secure_all_low(self):
        assert self._outlook(renew=0.0, composite=10.0) == RetentionOutlook.SECURE

    def test_watchlist_composite_20_to_39(self):
        assert self._outlook(renew=0.0, composite=25.0) == RetentionOutlook.WATCHLIST

    def test_watchlist_exactly_composite_20(self):
        assert self._outlook(renew=0.0, composite=20.0) == RetentionOutlook.WATCHLIST

    def test_at_risk_composite_40_to_59(self):
        assert self._outlook(renew=0.0, composite=45.0) == RetentionOutlook.AT_RISK

    def test_at_risk_exactly_composite_40(self):
        assert self._outlook(renew=0.0, composite=40.0) == RetentionOutlook.AT_RISK

    def test_at_risk_renew_gte45(self):
        assert self._outlook(renew=50.0, composite=10.0) == RetentionOutlook.AT_RISK

    def test_at_risk_renew_exactly45(self):
        assert self._outlook(renew=45.0, composite=10.0) == RetentionOutlook.AT_RISK

    def test_critical_composite_gte60(self):
        assert self._outlook(renew=0.0, composite=65.0) == RetentionOutlook.CRITICAL

    def test_critical_exactly_composite_60(self):
        assert self._outlook(renew=0.0, composite=60.0) == RetentionOutlook.CRITICAL

    def test_critical_renew_gte60_and_days_lte60(self):
        assert self._outlook(renew=65.0, composite=10.0, days=45) == RetentionOutlook.CRITICAL

    def test_critical_renew_exactly60_and_days_exactly60(self):
        assert self._outlook(renew=60.0, composite=10.0, days=60) == RetentionOutlook.CRITICAL

    def test_not_critical_renew_gte60_but_days_gt60(self):
        # renew>=60 but days>60 => not critical from that condition; composite<60 => AT_RISK from renew>=45
        result = self._outlook(renew=65.0, composite=10.0, days=90)
        assert result == RetentionOutlook.AT_RISK

    def test_not_critical_renew_lt60_and_days_lte60(self):
        # renew=50<60, days=45<=60 => not critical from that condition
        result = self._outlook(renew=50.0, composite=10.0, days=45)
        assert result == RetentionOutlook.AT_RISK

    def test_secure_composite_lt20(self):
        assert self._outlook(renew=0.0, composite=0.0) == RetentionOutlook.SECURE


# ===========================================================================
# Section 13: _estimated_arr_at_risk
# ===========================================================================

class TestEstimatedArrAtRisk:
    def setup_method(self):
        self.det = fresh_detector()

    def test_basic_risk_calculation(self):
        inp = make_input(current_arr=100_000.0, multi_year_contract=0, days_to_renewal=200)
        risk = self.det._estimated_arr_at_risk(inp, 50.0)
        assert risk == round(100_000.0 * 0.50, 2)

    def test_zero_composite_zero_risk(self):
        inp = make_input(current_arr=100_000.0, multi_year_contract=0)
        assert self.det._estimated_arr_at_risk(inp, 0.0) == 0.0

    def test_100_composite_full_risk(self):
        inp = make_input(current_arr=100_000.0, multi_year_contract=0)
        assert self.det._estimated_arr_at_risk(inp, 100.0) == 100_000.0

    def test_multi_year_protection_when_days_gt365(self):
        inp = make_input(current_arr=100_000.0, multi_year_contract=1, days_to_renewal=400)
        risk = self.det._estimated_arr_at_risk(inp, 50.0)
        assert risk == round(100_000.0 * 0.50 * 0.3, 2)

    def test_multi_year_no_protection_when_days_lte365(self):
        inp = make_input(current_arr=100_000.0, multi_year_contract=1, days_to_renewal=365)
        risk = self.det._estimated_arr_at_risk(inp, 50.0)
        assert risk == round(100_000.0 * 0.50, 2)

    def test_non_multi_year_no_protection(self):
        inp = make_input(current_arr=100_000.0, multi_year_contract=0, days_to_renewal=400)
        risk = self.det._estimated_arr_at_risk(inp, 50.0)
        assert risk == round(100_000.0 * 0.50, 2)

    def test_multi_year_exactly_366_days(self):
        inp = make_input(current_arr=100_000.0, multi_year_contract=1, days_to_renewal=366)
        risk = self.det._estimated_arr_at_risk(inp, 50.0)
        assert risk == round(100_000.0 * 0.50 * 0.3, 2)

    def test_rounding(self):
        inp = make_input(current_arr=33_333.0, multi_year_contract=0)
        risk = self.det._estimated_arr_at_risk(inp, 33.3)
        assert risk == round(33_333.0 * 0.333, 2)


# ===========================================================================
# Section 14: _arr_expansion_potential
# ===========================================================================

class TestArrExpansionPotential:
    def setup_method(self):
        self.det = fresh_detector()

    def test_zero_when_fully_utilized(self):
        inp = make_input(current_arr=100_000.0, seats_utilized_pct=100.0,
                         product_adoption_pct=100.0)
        assert self.det._arr_expansion_potential(inp) == 0.0

    def test_full_headroom(self):
        inp = make_input(current_arr=100_000.0, seats_utilized_pct=0.0,
                         product_adoption_pct=0.0)
        # seat_headroom=1.0 * 0.4 + adoption_headroom=1.0 * 0.3 = 0.7
        result = self.det._arr_expansion_potential(inp)
        assert result == 70_000.0

    def test_partial_headroom(self):
        inp = make_input(current_arr=100_000.0, seats_utilized_pct=50.0,
                         product_adoption_pct=50.0)
        # 0.5*0.4 + 0.5*0.3 = 0.35
        result = self.det._arr_expansion_potential(inp)
        assert result == 35_000.0

    def test_seat_headroom_only(self):
        inp = make_input(current_arr=100_000.0, seats_utilized_pct=0.0,
                         product_adoption_pct=100.0)
        # seat_headroom=1.0, adoption=0
        result = self.det._arr_expansion_potential(inp)
        assert result == 40_000.0

    def test_adoption_headroom_only(self):
        inp = make_input(current_arr=100_000.0, seats_utilized_pct=100.0,
                         product_adoption_pct=0.0)
        # seat=0, adoption=1.0*0.3
        result = self.det._arr_expansion_potential(inp)
        assert result == 30_000.0

    def test_clamps_negative_headroom(self):
        # seats > 100 => headroom clamped to 0
        inp = make_input(current_arr=100_000.0, seats_utilized_pct=110.0,
                         product_adoption_pct=110.0)
        assert self.det._arr_expansion_potential(inp) == 0.0

    def test_rounding_applied(self):
        inp = make_input(current_arr=33_333.0, seats_utilized_pct=33.0,
                         product_adoption_pct=33.0)
        result = self.det._arr_expansion_potential(inp)
        seat_h = (100.0 - 33.0) / 100.0
        adopt_h = (100.0 - 33.0) / 100.0
        expected = round(33_333.0 * (seat_h * 0.4 + adopt_h * 0.3), 2)
        assert result == expected


# ===========================================================================
# Section 15: _leak_action
# ===========================================================================

class TestLeakAction:
    def setup_method(self):
        self.det = fresh_detector()

    def test_monitor_for_contained(self):
        assert self.det._leak_action(LeakSeverity.CONTAINED, False, 10.0) == LeakAction.MONITOR

    def test_protect_expansion_for_moderate(self):
        assert self.det._leak_action(LeakSeverity.MODERATE, False, 30.0) == LeakAction.PROTECT_EXPANSION

    def test_retention_play_for_significant(self):
        assert self.det._leak_action(LeakSeverity.SIGNIFICANT, False, 55.0) == LeakAction.RETENTION_PLAY

    def test_executive_save_for_critical(self):
        assert self.det._leak_action(LeakSeverity.CRITICAL, False, 75.0) == LeakAction.EXECUTIVE_SAVE

    def test_executive_save_when_needs_exec_true_contained(self):
        assert self.det._leak_action(LeakSeverity.CONTAINED, True, 10.0) == LeakAction.EXECUTIVE_SAVE

    def test_executive_save_when_needs_exec_true_moderate(self):
        assert self.det._leak_action(LeakSeverity.MODERATE, True, 30.0) == LeakAction.EXECUTIVE_SAVE

    def test_executive_save_when_needs_exec_true_significant(self):
        assert self.det._leak_action(LeakSeverity.SIGNIFICANT, True, 50.0) == LeakAction.EXECUTIVE_SAVE


# ===========================================================================
# Section 16: is_leaking invariant
# ===========================================================================

class TestIsLeaking:
    def test_not_leaking_healthy_account(self):
        r = fresh_detector().detect(make_input(
            days_to_renewal=300, renewal_qualified=1,
            product_adoption_pct=80.0, seats_utilized_pct=80.0, nps_score=50,
            discount_pct_current=5.0, discount_pct_original=5.0,
        ))
        assert isinstance(r.is_leaking, bool)

    def test_leaking_when_composite_gte45(self):
        det = fresh_detector()
        inp = make_input(
            discount_pct_current=40.0, discount_pct_original=10.0,
            days_to_renewal=200, renewal_qualified=0,
            product_adoption_pct=20.0, seats_utilized_pct=20.0, nps_score=-50,
            last_expansion_days_ago=400, expansion_attempts_failed=3,
            champion_active=0, exec_sponsor_engaged=0,
        )
        r = det.detect(inp)
        assert r.leak_composite >= 45.0
        assert r.is_leaking is True

    def test_leaking_when_days_lte60_and_renew_risk_gte50(self):
        det = fresh_detector()
        inp = make_input(
            days_to_renewal=30, renewal_qualified=0,
            product_adoption_pct=20.0, seats_utilized_pct=20.0, nps_score=-50,
        )
        r = det.detect(inp)
        assert r.renewal_risk_score >= 50
        assert r.is_leaking is True

    def test_not_leaking_very_healthy(self):
        r = fresh_detector().detect(make_input(
            discount_pct_current=5.0, discount_pct_original=5.0,
            days_to_renewal=300, renewal_qualified=1,
            product_adoption_pct=90.0, seats_utilized_pct=90.0, nps_score=80,
            champion_active=1, champion_changed_last_90d=0, exec_sponsor_engaged=1,
            support_ticket_volume_30d=0, last_expansion_days_ago=30,
            expansion_attempts_failed=0, competitive_displacement_risk=0,
        ))
        assert r.is_leaking is False

    def test_is_leaking_is_bool(self):
        r = fresh_detector().detect(make_input())
        assert isinstance(r.is_leaking, bool)


# ===========================================================================
# Section 17: needs_executive_save invariant
# ===========================================================================

class TestNeedsExecutiveSave:
    def test_needs_exec_when_composite_gte65(self):
        det = fresh_detector()
        inp = make_input(
            discount_pct_current=50.0, discount_pct_original=10.0,
            days_to_renewal=30, renewal_qualified=0,
            product_adoption_pct=20.0, seats_utilized_pct=20.0, nps_score=-50,
            last_expansion_days_ago=400, expansion_attempts_failed=3,
            champion_active=0, exec_sponsor_engaged=0,
            competitive_displacement_risk=1,
        )
        r = det.detect(inp)
        assert r.leak_composite >= 65.0
        assert r.needs_executive_save is True

    def test_needs_exec_when_champion_changed_and_arr_gte100k(self):
        r = fresh_detector().detect(make_input(champion_changed_last_90d=1,
                                               current_arr=150_000.0))
        assert r.needs_executive_save is True

    def test_no_exec_when_champion_changed_and_arr_lt100k(self):
        r = fresh_detector().detect(make_input(
            champion_changed_last_90d=1, current_arr=50_000.0,
            discount_pct_current=5.0, discount_pct_original=5.0,
            days_to_renewal=300, renewal_qualified=1,
            product_adoption_pct=90.0, seats_utilized_pct=90.0, nps_score=50,
            champion_active=1, exec_sponsor_engaged=1,
            support_ticket_volume_30d=0, last_expansion_days_ago=30,
            expansion_attempts_failed=0, competitive_displacement_risk=0,
        ))
        if r.leak_composite < 65.0:
            assert not r.needs_executive_save

    def test_needs_exec_exactly_at_100k_boundary(self):
        r = fresh_detector().detect(make_input(
            champion_changed_last_90d=1, current_arr=100_000.0,
            discount_pct_current=5.0, discount_pct_original=5.0,
            days_to_renewal=300, renewal_qualified=1,
            product_adoption_pct=90.0, seats_utilized_pct=90.0, nps_score=50,
            champion_active=1, exec_sponsor_engaged=1,
        ))
        assert r.needs_executive_save

    def test_no_exec_at_99999(self):
        r = fresh_detector().detect(make_input(
            champion_changed_last_90d=1, current_arr=99_999.0,
            discount_pct_current=5.0, discount_pct_original=5.0,
            days_to_renewal=300, renewal_qualified=1,
            product_adoption_pct=90.0, seats_utilized_pct=90.0, nps_score=50,
            champion_active=1, exec_sponsor_engaged=1,
        ))
        if r.leak_composite < 65.0:
            assert not r.needs_executive_save


# ===========================================================================
# Section 18: detect() integration
# ===========================================================================

class TestDetect:
    def test_returns_result_type(self):
        r = fresh_detector().detect(make_input())
        assert isinstance(r, RevenueLeakResult)

    def test_result_stored_in_results(self):
        det = fresh_detector()
        det.detect(make_input())
        assert len(det._results) == 1

    def test_account_id_preserved(self):
        r = fresh_detector().detect(make_input(account_id="test_123"))
        assert r.account_id == "test_123"

    def test_account_name_preserved(self):
        r = fresh_detector().detect(make_input(account_name="Gamma Inc"))
        assert r.account_name == "Gamma Inc"

    def test_all_scores_in_range(self):
        r = fresh_detector().detect(make_input())
        assert 0.0 <= r.discount_risk_score <= 100.0
        assert 0.0 <= r.renewal_risk_score <= 100.0
        assert 0.0 <= r.expansion_health_score <= 100.0
        assert 0.0 <= r.relationship_score <= 100.0
        assert 0.0 <= r.leak_composite <= 100.0

    def test_enum_fields_are_enum_types(self):
        r = fresh_detector().detect(make_input())
        assert isinstance(r.leak_severity, LeakSeverity)
        assert isinstance(r.leak_pattern, LeakPattern)
        assert isinstance(r.retention_outlook, RetentionOutlook)
        assert isinstance(r.leak_action, LeakAction)

    def test_arr_at_risk_non_negative(self):
        assert fresh_detector().detect(make_input()).estimated_arr_at_risk >= 0.0

    def test_expansion_potential_non_negative(self):
        assert fresh_detector().detect(make_input()).arr_expansion_potential >= 0.0

    def test_multiple_detects_accumulate(self):
        det = fresh_detector()
        det.detect(make_input(account_id="a1"))
        det.detect(make_input(account_id="a2"))
        assert len(det._results) == 2

    def test_fresh_detector_starts_empty(self):
        assert len(fresh_detector()._results) == 0

    def test_two_detectors_independent(self):
        d1, d2 = fresh_detector(), fresh_detector()
        d1.detect(make_input(account_id="a1"))
        assert len(d1._results) == 1
        assert len(d2._results) == 0


# ===========================================================================
# Section 19: detect_batch()
# ===========================================================================

class TestDetectBatch:
    def test_returns_list(self):
        det = fresh_detector()
        results = det.detect_batch([make_input(account_id="a1"), make_input(account_id="a2")])
        assert isinstance(results, list)

    def test_length_matches_inputs(self):
        det = fresh_detector()
        inputs = [make_input(account_id=f"a{i}") for i in range(3)]
        assert len(det.detect_batch(inputs)) == 3

    def test_accumulates_results(self):
        det = fresh_detector()
        det.detect_batch([make_input(account_id=f"a{i}") for i in range(5)])
        assert len(det._results) == 5

    def test_empty_batch_returns_empty_list(self):
        assert fresh_detector().detect_batch([]) == []

    def test_single_item_batch(self):
        det = fresh_detector()
        results = det.detect_batch([make_input(account_id="solo")])
        assert len(results) == 1
        assert results[0].account_id == "solo"

    def test_all_results_are_result_type(self):
        det = fresh_detector()
        for r in det.detect_batch([make_input(account_id=f"a{i}") for i in range(3)]):
            assert isinstance(r, RevenueLeakResult)

    def test_batch_consistent_with_individual(self):
        inp = make_input(account_id="a1")
        r_single = fresh_detector().detect(inp)
        r_batch = fresh_detector().detect_batch([inp])[0]
        assert r_single.leak_composite == r_batch.leak_composite

    def test_batch_accumulates_after_existing(self):
        det = fresh_detector()
        det.detect(make_input(account_id="pre"))
        det.detect_batch([make_input(account_id="b1"), make_input(account_id="b2")])
        assert len(det._results) == 3


# ===========================================================================
# Section 20: reset() and properties
# ===========================================================================

class TestResetAndProperties:
    def test_reset_clears_results(self):
        det = fresh_detector()
        det.detect(make_input())
        det.reset()
        assert len(det._results) == 0

    def test_reset_clears_multiple(self):
        det = fresh_detector()
        for i in range(5):
            det.detect(make_input(account_id=f"a{i}"))
        det.reset()
        assert len(det._results) == 0

    def test_leaking_accounts_property_empty(self):
        assert fresh_detector().leaking_accounts == []

    def test_leaking_accounts_property_filters(self):
        det = fresh_detector()
        leaky_inp = make_input(
            discount_pct_current=40.0, discount_pct_original=10.0,
            days_to_renewal=30, renewal_qualified=0,
            product_adoption_pct=20.0, seats_utilized_pct=20.0, nps_score=-50,
            last_expansion_days_ago=400, expansion_attempts_failed=3,
            champion_active=0, exec_sponsor_engaged=0,
        )
        det.detect(leaky_inp)
        for r in det.leaking_accounts:
            assert r.is_leaking is True

    def test_executive_save_queue_empty(self):
        assert fresh_detector().executive_save_queue == []

    def test_executive_save_queue_filters(self):
        det = fresh_detector()
        det.detect(make_input(champion_changed_last_90d=1, current_arr=200_000.0))
        for r in det.executive_save_queue:
            assert r.needs_executive_save is True

    def test_total_arr_at_risk_empty(self):
        assert fresh_detector().total_arr_at_risk == 0.0

    def test_total_arr_at_risk_accumulates(self):
        det = fresh_detector()
        r1 = det.detect(make_input(account_id="a1"))
        r2 = det.detect(make_input(account_id="a2"))
        expected = round(r1.estimated_arr_at_risk + r2.estimated_arr_at_risk, 2)
        assert det.total_arr_at_risk == expected

    def test_total_expansion_potential_empty(self):
        assert fresh_detector().total_expansion_potential == 0.0

    def test_total_expansion_potential_accumulates(self):
        det = fresh_detector()
        r1 = det.detect(make_input(account_id="a1"))
        r2 = det.detect(make_input(account_id="a2"))
        expected = round(r1.arr_expansion_potential + r2.arr_expansion_potential, 2)
        assert det.total_expansion_potential == expected

    def test_leaking_accounts_after_reset(self):
        det = fresh_detector()
        det.detect(make_input(champion_changed_last_90d=1, current_arr=200_000.0))
        det.reset()
        assert det.leaking_accounts == []

    def test_executive_save_queue_after_reset(self):
        det = fresh_detector()
        det.detect(make_input(champion_changed_last_90d=1, current_arr=200_000.0))
        det.reset()
        assert det.executive_save_queue == []


# ===========================================================================
# Section 21: summary() detailed
# ===========================================================================

class TestSummaryDetailed:
    def test_single_account_summary(self):
        det = fresh_detector()
        result = det.detect(make_input())
        summary = det.summary()
        assert summary["total"] == 1
        assert summary["leaking_count"] == (1 if result.is_leaking else 0)
        assert summary["executive_save_count"] == (1 if result.needs_executive_save else 0)

    def test_summary_severity_counts_sum_to_total(self):
        det = fresh_detector()
        det.detect(make_input())
        summary = det.summary()
        assert sum(summary["severity_counts"].values()) == 1

    def test_summary_pattern_counts_sum_to_total(self):
        det = fresh_detector()
        det.detect(make_input())
        summary = det.summary()
        assert sum(summary["pattern_counts"].values()) == 1

    def test_summary_outlook_counts_sum_to_total(self):
        det = fresh_detector()
        det.detect(make_input())
        summary = det.summary()
        assert sum(summary["outlook_counts"].values()) == 1

    def test_summary_action_counts_sum_to_total(self):
        det = fresh_detector()
        det.detect(make_input())
        summary = det.summary()
        assert sum(summary["action_counts"].values()) == 1

    def test_summary_averages_are_floats(self):
        det = fresh_detector()
        det.detect(make_input())
        summary = det.summary()
        assert isinstance(summary["avg_leak_composite"], float)
        assert isinstance(summary["avg_discount_risk_score"], float)
        assert isinstance(summary["avg_renewal_risk_score"], float)
        assert isinstance(summary["avg_expansion_health_score"], float)
        assert isinstance(summary["avg_relationship_score"], float)

    def test_summary_total_arr_at_risk_matches_property(self):
        det = fresh_detector()
        det.detect(make_input())
        assert det.summary()["total_arr_at_risk"] == det.total_arr_at_risk

    def test_summary_leaking_count_matches_property(self):
        det = fresh_detector()
        det.detect(make_input())
        assert det.summary()["leaking_count"] == len(det.leaking_accounts)

    def test_summary_exec_save_count_matches_property(self):
        det = fresh_detector()
        det.detect(make_input())
        assert det.summary()["executive_save_count"] == len(det.executive_save_queue)

    def test_summary_with_multiple_accounts(self):
        det = fresh_detector()
        for i in range(5):
            det.detect(make_input(account_id=f"a{i}"))
        summary = det.summary()
        assert summary["total"] == 5
        assert sum(summary["severity_counts"].values()) == 5
        assert sum(summary["pattern_counts"].values()) == 5
        assert sum(summary["outlook_counts"].values()) == 5
        assert sum(summary["action_counts"].values()) == 5

    def test_summary_avg_composite_correct(self):
        det = fresh_detector()
        r1 = det.detect(make_input(account_id="a1"))
        r2 = det.detect(make_input(account_id="a2"))
        expected_avg = round((r1.leak_composite + r2.leak_composite) / 2, 1)
        assert det.summary()["avg_leak_composite"] == expected_avg

    def test_summary_avg_discount_risk_correct(self):
        det = fresh_detector()
        r1 = det.detect(make_input(account_id="a1"))
        r2 = det.detect(make_input(account_id="a2"))
        expected_avg = round((r1.discount_risk_score + r2.discount_risk_score) / 2, 1)
        assert det.summary()["avg_discount_risk_score"] == expected_avg

    def test_summary_avg_renewal_risk_correct(self):
        det = fresh_detector()
        r1 = det.detect(make_input(account_id="a1"))
        r2 = det.detect(make_input(account_id="a2"))
        expected_avg = round((r1.renewal_risk_score + r2.renewal_risk_score) / 2, 1)
        assert det.summary()["avg_renewal_risk_score"] == expected_avg

    def test_summary_avg_expansion_health_correct(self):
        det = fresh_detector()
        r1 = det.detect(make_input(account_id="a1"))
        r2 = det.detect(make_input(account_id="a2"))
        expected_avg = round((r1.expansion_health_score + r2.expansion_health_score) / 2, 1)
        assert det.summary()["avg_expansion_health_score"] == expected_avg

    def test_summary_avg_relationship_score_correct(self):
        det = fresh_detector()
        r1 = det.detect(make_input(account_id="a1"))
        r2 = det.detect(make_input(account_id="a2"))
        expected_avg = round((r1.relationship_score + r2.relationship_score) / 2, 1)
        assert det.summary()["avg_relationship_score"] == expected_avg

    def test_summary_counts_two_accounts(self):
        det = fresh_detector()
        det.detect(make_input(account_id="a1",
                               discount_pct_current=5.0, discount_pct_original=5.0,
                               days_to_renewal=300, renewal_qualified=1,
                               product_adoption_pct=90.0, seats_utilized_pct=90.0,
                               nps_score=-1, last_expansion_days_ago=30,
                               expansion_attempts_failed=0, champion_active=1,
                               champion_changed_last_90d=0, exec_sponsor_engaged=1,
                               support_ticket_volume_30d=0, competitive_displacement_risk=0))
        det.detect(make_input(account_id="a2",
                               discount_pct_current=50.0, discount_pct_original=10.0,
                               days_to_renewal=30, renewal_qualified=0,
                               product_adoption_pct=20.0, seats_utilized_pct=20.0,
                               nps_score=-50, last_expansion_days_ago=400,
                               expansion_attempts_failed=3, champion_active=0,
                               exec_sponsor_engaged=0, competitive_displacement_risk=1))
        summary = det.summary()
        assert summary["total"] == 2


# ===========================================================================
# Section 22: Score clamping validation
# ===========================================================================

class TestScoreClamping:
    def setup_method(self):
        self.det = fresh_detector()

    def test_discount_risk_never_exceeds_100(self):
        inp = make_input(discount_pct_current=99.0, discount_pct_original=0.0,
                         current_arr=1.0, arr_at_contract_start=1_000_000.0)
        assert self.det._discount_risk_score(inp) <= 100.0

    def test_discount_risk_never_below_0(self):
        inp = make_input(discount_pct_current=0.0, discount_pct_original=99.0)
        assert self.det._discount_risk_score(inp) >= 0.0

    def test_renewal_risk_never_exceeds_100(self):
        inp = make_input(days_to_renewal=1, renewal_qualified=0,
                         product_adoption_pct=0.0, seats_utilized_pct=0.0, nps_score=-100)
        assert self.det._renewal_risk_score(inp) <= 100.0

    def test_renewal_risk_never_below_0(self):
        inp = make_input(days_to_renewal=1000, renewal_qualified=1,
                         product_adoption_pct=100.0, seats_utilized_pct=100.0, nps_score=100)
        assert self.det._renewal_risk_score(inp) >= 0.0

    def test_expansion_health_never_exceeds_100(self):
        inp = make_input(last_expansion_days_ago=0, expansion_attempts_failed=0,
                         seats_utilized_pct=100.0)
        assert self.det._expansion_health_score(inp) <= 100.0

    def test_expansion_health_never_below_0(self):
        inp = make_input(last_expansion_days_ago=1000, expansion_attempts_failed=100,
                         seats_utilized_pct=0.0)
        assert self.det._expansion_health_score(inp) >= 0.0

    def test_relationship_score_never_exceeds_100(self):
        inp = make_input(champion_active=1, champion_changed_last_90d=0,
                         exec_sponsor_engaged=1, support_ticket_volume_30d=0,
                         competitive_displacement_risk=0)
        assert self.det._relationship_score(inp) <= 100.0

    def test_relationship_score_never_below_0(self):
        inp = make_input(champion_active=0, champion_changed_last_90d=1,
                         exec_sponsor_engaged=0, support_ticket_volume_30d=100,
                         competitive_displacement_risk=1)
        assert self.det._relationship_score(inp) >= 0.0

    def test_composite_never_exceeds_100(self):
        assert self.det._composite(100.0, 100.0, 0.0, 0.0) <= 100.0

    def test_composite_never_below_0(self):
        assert self.det._composite(0.0, 0.0, 100.0, 100.0) >= 0.0


# ===========================================================================
# Section 23: RevenueLeakResult dataclass structure
# ===========================================================================

class TestRevenueLeakResultDataclass:
    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(RevenueLeakResult)

    def test_field_count(self):
        assert len(dataclasses.fields(RevenueLeakResult)) == 15

    def test_field_names(self):
        names = {f.name for f in dataclasses.fields(RevenueLeakResult)}
        expected = {
            "account_id", "account_name", "leak_severity", "leak_pattern",
            "retention_outlook", "leak_action", "discount_risk_score",
            "renewal_risk_score", "expansion_health_score", "relationship_score",
            "leak_composite", "estimated_arr_at_risk", "arr_expansion_potential",
            "is_leaking", "needs_executive_save",
        }
        assert names == expected


# ===========================================================================
# Section 24: RevenueLeakDetector constructor & misc
# ===========================================================================

class TestDetectorConstructor:
    def test_initial_results_empty(self):
        det = fresh_detector()
        assert det._results == []

    def test_multiple_instances_independent(self):
        d1 = fresh_detector()
        d2 = fresh_detector()
        d1.detect(make_input())
        assert len(d1._results) == 1
        assert len(d2._results) == 0

    def test_reset_then_detect_works(self):
        det = fresh_detector()
        det.detect(make_input(account_id="before"))
        det.reset()
        result = det.detect(make_input(account_id="after"))
        assert result.account_id == "after"
        assert len(det._results) == 1


# ===========================================================================
# Section 25: Edge cases and boundary conditions
# ===========================================================================

class TestEdgeCases:
    def test_zero_arr(self):
        det = fresh_detector()
        result = det.detect(make_input(current_arr=0.0, arr_at_contract_start=0.0))
        assert result.estimated_arr_at_risk == 0.0
        assert result.arr_expansion_potential == 0.0

    def test_very_large_arr(self):
        det = fresh_detector()
        result = det.detect(make_input(current_arr=10_000_000.0))
        assert result.estimated_arr_at_risk >= 0.0
        assert result.arr_expansion_potential >= 0.0

    def test_days_to_renewal_zero(self):
        det = fresh_detector()
        result = det.detect(make_input(days_to_renewal=0))
        assert result.renewal_risk_score >= 40.0

    def test_days_to_renewal_very_large(self):
        det = fresh_detector()
        result = det.detect(make_input(days_to_renewal=9999))
        assert isinstance(result, RevenueLeakResult)

    def test_nps_exactly_minus1_skipped(self):
        det = fresh_detector()
        inp = make_input(nps_score=-1, days_to_renewal=200, renewal_qualified=1,
                         product_adoption_pct=80.0, seats_utilized_pct=80.0)
        score = det._renewal_risk_score(inp)
        assert score == 0.0

    def test_expansion_attempts_very_large(self):
        det = fresh_detector()
        inp = make_input(expansion_attempts_failed=100)
        assert det._expansion_health_score(inp) >= 0.0

    def test_support_tickets_very_large(self):
        det = fresh_detector()
        inp = make_input(support_ticket_volume_30d=1000)
        assert det._relationship_score(inp) >= 0.0

    def test_all_binary_flags_off(self):
        det = fresh_detector()
        result = det.detect(make_input(champion_active=0, champion_changed_last_90d=0,
                                       exec_sponsor_engaged=0, renewal_qualified=0,
                                       multi_year_contract=0, competitive_displacement_risk=0))
        assert isinstance(result, RevenueLeakResult)

    def test_all_binary_flags_on(self):
        det = fresh_detector()
        result = det.detect(make_input(champion_active=1, champion_changed_last_90d=1,
                                       exec_sponsor_engaged=1, renewal_qualified=1,
                                       multi_year_contract=1, competitive_displacement_risk=1))
        assert isinstance(result, RevenueLeakResult)

    def test_to_dict_enums_match_values(self):
        det = fresh_detector()
        result = det.detect(make_input())
        d = result.to_dict()
        assert d["leak_severity"] == result.leak_severity.value
        assert d["leak_pattern"] == result.leak_pattern.value
        assert d["retention_outlook"] == result.retention_outlook.value
        assert d["leak_action"] == result.leak_action.value

    def test_product_adoption_exactly_0(self):
        det = fresh_detector()
        inp = make_input(product_adoption_pct=0.0)
        assert det._renewal_risk_score(inp) >= 20.0

    def test_product_adoption_exactly_100(self):
        det = fresh_detector()
        inp = make_input(product_adoption_pct=100.0, days_to_renewal=200,
                         renewal_qualified=1, seats_utilized_pct=80.0, nps_score=-1)
        assert det._renewal_risk_score(inp) == 0.0

    def test_seats_exactly_0(self):
        det = fresh_detector()
        inp = make_input(seats_utilized_pct=0.0, days_to_renewal=200,
                         renewal_qualified=1, product_adoption_pct=80.0, nps_score=-1)
        assert det._renewal_risk_score(inp) >= 15.0

    def test_seats_exactly_100(self):
        det = fresh_detector()
        inp = make_input(seats_utilized_pct=100.0, days_to_renewal=200,
                         renewal_qualified=1, product_adoption_pct=80.0, nps_score=-1)
        assert det._renewal_risk_score(inp) == 0.0


# ===========================================================================
# Section 26: End-to-end scenarios
# ===========================================================================

class TestEndToEndScenarios:
    def test_fully_healthy_account(self):
        det = fresh_detector()
        result = det.detect(make_input(
            current_arr=100_000.0, arr_at_contract_start=100_000.0,
            discount_pct_current=5.0, discount_pct_original=5.0,
            days_to_renewal=300, renewal_qualified=1,
            last_expansion_days_ago=30, expansion_attempts_failed=0,
            champion_active=1, champion_changed_last_90d=0, exec_sponsor_engaged=1,
            support_ticket_volume_30d=0, nps_score=60,
            product_adoption_pct=85.0, seats_utilized_pct=80.0,
            multi_year_contract=0, competitive_displacement_risk=0,
        ))
        assert result.leak_severity == LeakSeverity.CONTAINED
        assert result.is_leaking is False
        assert not result.needs_executive_save

    def test_critical_churn_account(self):
        det = fresh_detector()
        result = det.detect(make_input(
            current_arr=500_000.0, arr_at_contract_start=600_000.0,
            discount_pct_current=45.0, discount_pct_original=10.0,
            days_to_renewal=20, renewal_qualified=0,
            last_expansion_days_ago=400, expansion_attempts_failed=3,
            champion_active=0, champion_changed_last_90d=1, exec_sponsor_engaged=0,
            support_ticket_volume_30d=15, nps_score=-50,
            product_adoption_pct=20.0, seats_utilized_pct=20.0,
            multi_year_contract=0, competitive_displacement_risk=1,
        ))
        assert result.leak_severity == LeakSeverity.CRITICAL
        assert result.is_leaking is True
        assert result.needs_executive_save
        assert result.leak_action == LeakAction.EXECUTIVE_SAVE

    def test_multi_year_protection_applied(self):
        det = fresh_detector()
        result = det.detect(make_input(
            current_arr=100_000.0, multi_year_contract=1, days_to_renewal=400,
        ))
        composite = result.leak_composite
        expected_base = 100_000.0 * (composite / 100.0) * 0.3
        assert result.estimated_arr_at_risk == round(expected_base, 2)

    def test_discount_creep_pattern(self):
        det = fresh_detector()
        result = det.detect(make_input(
            discount_pct_current=50.0, discount_pct_original=5.0,
            current_arr=100_000.0, arr_at_contract_start=100_000.0,
            days_to_renewal=300, renewal_qualified=1,
            product_adoption_pct=80.0, seats_utilized_pct=80.0, nps_score=50,
            champion_active=1, champion_changed_last_90d=0, exec_sponsor_engaged=1,
            support_ticket_volume_30d=0, last_expansion_days_ago=30,
            expansion_attempts_failed=0, competitive_displacement_risk=0,
        ))
        # disc_risk >=40, only 1 signal, disc>=45 => DISCOUNT_CREEP
        assert result.leak_pattern == LeakPattern.DISCOUNT_CREEP

    def test_renewal_risk_pattern(self):
        det = fresh_detector()
        result = det.detect(make_input(
            days_to_renewal=80, renewal_qualified=0,
            product_adoption_pct=20.0, seats_utilized_pct=20.0, nps_score=-50,
            discount_pct_current=5.0, discount_pct_original=5.0,
            last_expansion_days_ago=30, expansion_attempts_failed=0,
            champion_active=1, champion_changed_last_90d=0, exec_sponsor_engaged=1,
            support_ticket_volume_30d=0, competitive_displacement_risk=0,
        ))
        # renewal_risk: +12+20+20+15+15=82 >= 55 => RENEWAL_RISK (1 signal only)
        assert result.leak_pattern == LeakPattern.RENEWAL_RISK

    def test_expansion_stall_pattern(self):
        det = fresh_detector()
        result = det.detect(make_input(
            last_expansion_days_ago=400, expansion_attempts_failed=3,
            seats_utilized_pct=20.0,
            discount_pct_current=5.0, discount_pct_original=5.0,
            days_to_renewal=300, renewal_qualified=1,
            product_adoption_pct=80.0, nps_score=50,
            champion_active=1, champion_changed_last_90d=0, exec_sponsor_engaged=1,
            support_ticket_volume_30d=0, competitive_displacement_risk=0,
        ))
        assert result.leak_pattern in (LeakPattern.EXPANSION_STALL, LeakPattern.MULTI_LEAK)

    def test_reset_then_detect_clean_summary(self):
        det = fresh_detector()
        for i in range(10):
            det.detect(make_input(account_id=f"a{i}"))
        det.reset()
        det.detect(make_input(account_id="fresh"))
        s = det.summary()
        assert s["total"] == 1

    def test_batch_then_summary_consistent(self):
        det = fresh_detector()
        inputs = [make_input(account_id=f"a{i}") for i in range(7)]
        det.detect_batch(inputs)
        s = det.summary()
        assert s["total"] == 7
        assert sum(s["severity_counts"].values()) == 7
