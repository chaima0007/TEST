"""
Comprehensive pytest test suite for SalesMultithreadingDepthRelationshipBreadthEngine.
"""
import pytest
from swarm.intelligence.sales_multithreading_depth_relationship_breadth_engine import (
    MultithreadRisk,
    MultithreadPattern,
    MultithreadSeverity,
    MultithreadAction,
    MultithreadInput,
    MultithreadResult,
    SalesMultithreadingDepthRelationshipBreadthEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> MultithreadInput:
    """Return a baseline 'good health' input; override individual fields as needed."""
    defaults = dict(
        rep_id="REP-001",
        region="EMEA",
        evaluation_period_id="Q2-2026",
        avg_contacts_per_account=4.0,
        single_threaded_account_rate_pct=0.10,
        avg_new_contacts_added_per_quarter=2.0,
        contact_attrition_rate_pct=0.10,
        economic_buyer_engaged_rate_pct=0.80,
        technical_buyer_engaged_rate_pct=0.80,
        end_user_engaged_rate_pct=0.80,
        champion_to_non_champion_ratio=0.30,
        avg_email_threads_per_contact=5.0,
        multi_contact_meeting_rate_pct=0.70,
        cross_functional_reach_score=0.80,
        referral_introduction_rate_pct=0.50,
        dormant_contact_rate_pct=0.05,
        contact_map_completeness_score=0.80,
        buying_committee_size_vs_avg=1.20,
        c_suite_engaged_rate_pct=0.50,
        vp_engaged_rate_pct=0.50,
        total_active_accounts=100,
        avg_deal_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return MultithreadInput(**defaults)


def fresh_engine() -> SalesMultithreadingDepthRelationshipBreadthEngine:
    return SalesMultithreadingDepthRelationshipBreadthEngine()


# ---------------------------------------------------------------------------
# 1. Enum values — str subclass
# ---------------------------------------------------------------------------

class TestEnumValues:
    def test_multithread_risk_is_str_subclass(self):
        for member in MultithreadRisk:
            assert isinstance(member, str)

    def test_multithread_risk_values(self):
        assert MultithreadRisk.low.value == "low"
        assert MultithreadRisk.moderate.value == "moderate"
        assert MultithreadRisk.high.value == "high"
        assert MultithreadRisk.critical.value == "critical"

    def test_multithread_pattern_is_str_subclass(self):
        for member in MultithreadPattern:
            assert isinstance(member, str)

    def test_multithread_pattern_values(self):
        assert MultithreadPattern.none.value == "none"
        assert MultithreadPattern.single_thread_dependency.value == "single_thread_dependency"
        assert MultithreadPattern.vertical_tunnel.value == "vertical_tunnel"
        assert MultithreadPattern.it_bubble.value == "it_bubble"
        assert MultithreadPattern.executive_bypass.value == "executive_bypass"
        assert MultithreadPattern.breadth_stall.value == "breadth_stall"

    def test_multithread_severity_is_str_subclass(self):
        for member in MultithreadSeverity:
            assert isinstance(member, str)

    def test_multithread_severity_values(self):
        assert MultithreadSeverity.networked.value == "networked"
        assert MultithreadSeverity.adequate.value == "adequate"
        assert MultithreadSeverity.thin.value == "thin"
        assert MultithreadSeverity.isolated.value == "isolated"

    def test_multithread_action_is_str_subclass(self):
        for member in MultithreadAction:
            assert isinstance(member, str)

    def test_multithread_action_values(self):
        expected = {
            "no_action", "multithreading_monitoring", "contact_expansion_coaching",
            "stakeholder_mapping_workshop", "exec_introduction_coaching",
            "it_champion_bridge_coaching", "relationship_breadth_sprint",
            "account_rescue_intervention", "deal_restructure_escalation",
        }
        assert {m.value for m in MultithreadAction} == expected


# ---------------------------------------------------------------------------
# 2. to_dict() — 15 keys, enums as strings
# ---------------------------------------------------------------------------

class TestToDict:
    def test_to_dict_has_15_keys(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        expected_keys = {
            "rep_id", "region", "multithread_risk", "multithread_pattern",
            "multithread_severity", "recommended_action", "depth_score",
            "coverage_score", "quality_score", "network_score",
            "multithread_composite", "has_multithread_gap",
            "requires_expansion_coaching", "estimated_vulnerable_pipeline_usd",
            "multithread_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enums_serialized_as_strings(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        for key in ("multithread_risk", "multithread_pattern", "multithread_severity", "recommended_action"):
            assert isinstance(d[key], str), f"{key} should be str"

    def test_to_dict_values_match_result_fields(self):
        eng = fresh_engine()
        inp = make_input(rep_id="R99", region="APAC")
        r = eng.assess(inp)
        d = r.to_dict()
        assert d["rep_id"] == "R99"
        assert d["region"] == "APAC"
        assert d["depth_score"] == r.depth_score
        assert d["multithread_composite"] == r.multithread_composite


# ---------------------------------------------------------------------------
# 3. Sub-score thresholds and caps
# ---------------------------------------------------------------------------

class TestDepthScore:
    def _ds(self, **kw):
        return fresh_engine()._depth_score(make_input(**kw))

    def test_all_zeros_gives_zero(self):
        # perfect scores (low risk) should give 0
        score = self._ds(
            single_threaded_account_rate_pct=0.0,
            avg_contacts_per_account=10.0,
            avg_new_contacts_added_per_quarter=5.0,
        )
        assert score == 0

    def test_single_threaded_tier_high(self):
        score = self._ds(single_threaded_account_rate_pct=0.60,
                         avg_contacts_per_account=10.0,
                         avg_new_contacts_added_per_quarter=5.0)
        assert score == 40

    def test_single_threaded_tier_mid(self):
        score = self._ds(single_threaded_account_rate_pct=0.40,
                         avg_contacts_per_account=10.0,
                         avg_new_contacts_added_per_quarter=5.0)
        assert score == 22

    def test_single_threaded_tier_low(self):
        score = self._ds(single_threaded_account_rate_pct=0.22,
                         avg_contacts_per_account=10.0,
                         avg_new_contacts_added_per_quarter=5.0)
        assert score == 8

    def test_avg_contacts_tier_lowest(self):
        score = self._ds(single_threaded_account_rate_pct=0.0,
                         avg_contacts_per_account=1.5,
                         avg_new_contacts_added_per_quarter=5.0)
        assert score == 35

    def test_avg_contacts_tier_mid(self):
        score = self._ds(single_threaded_account_rate_pct=0.0,
                         avg_contacts_per_account=2.5,
                         avg_new_contacts_added_per_quarter=5.0)
        assert score == 18

    def test_avg_contacts_tier_low(self):
        score = self._ds(single_threaded_account_rate_pct=0.0,
                         avg_contacts_per_account=3.5,
                         avg_new_contacts_added_per_quarter=5.0)
        assert score == 6

    def test_new_contacts_tier_lowest(self):
        score = self._ds(single_threaded_account_rate_pct=0.0,
                         avg_contacts_per_account=10.0,
                         avg_new_contacts_added_per_quarter=0.5)
        assert score == 25

    def test_new_contacts_tier_mid(self):
        score = self._ds(single_threaded_account_rate_pct=0.0,
                         avg_contacts_per_account=10.0,
                         avg_new_contacts_added_per_quarter=1.2)
        assert score == 12

    def test_depth_score_capped_at_100(self):
        score = self._ds(
            single_threaded_account_rate_pct=0.99,
            avg_contacts_per_account=1.0,
            avg_new_contacts_added_per_quarter=0.0,
        )
        assert score == 100

    def test_depth_score_additive(self):
        score = self._ds(
            single_threaded_account_rate_pct=0.60,
            avg_contacts_per_account=1.5,
            avg_new_contacts_added_per_quarter=0.5,
        )
        assert score == min(40 + 35 + 25, 100)


class TestCoverageScore:
    def _cs(self, **kw):
        return fresh_engine()._coverage_score(make_input(**kw))

    def test_all_good_gives_zero(self):
        score = self._cs(economic_buyer_engaged_rate_pct=0.90,
                         c_suite_engaged_rate_pct=0.80,
                         contact_map_completeness_score=0.90)
        assert score == 0

    def test_eb_tier_lowest(self):
        score = self._cs(economic_buyer_engaged_rate_pct=0.25,
                         c_suite_engaged_rate_pct=0.80,
                         contact_map_completeness_score=0.90)
        assert score == 45

    def test_eb_tier_mid(self):
        score = self._cs(economic_buyer_engaged_rate_pct=0.50,
                         c_suite_engaged_rate_pct=0.80,
                         contact_map_completeness_score=0.90)
        assert score == 25

    def test_eb_tier_low(self):
        score = self._cs(economic_buyer_engaged_rate_pct=0.70,
                         c_suite_engaged_rate_pct=0.80,
                         contact_map_completeness_score=0.90)
        assert score == 10

    def test_csuite_tier_lowest(self):
        score = self._cs(economic_buyer_engaged_rate_pct=0.90,
                         c_suite_engaged_rate_pct=0.15,
                         contact_map_completeness_score=0.90)
        assert score == 30

    def test_csuite_tier_mid(self):
        score = self._cs(economic_buyer_engaged_rate_pct=0.90,
                         c_suite_engaged_rate_pct=0.35,
                         contact_map_completeness_score=0.90)
        assert score == 15

    def test_map_completeness_tier_lowest(self):
        score = self._cs(economic_buyer_engaged_rate_pct=0.90,
                         c_suite_engaged_rate_pct=0.80,
                         contact_map_completeness_score=0.25)
        assert score == 25

    def test_map_completeness_tier_mid(self):
        score = self._cs(economic_buyer_engaged_rate_pct=0.90,
                         c_suite_engaged_rate_pct=0.80,
                         contact_map_completeness_score=0.50)
        assert score == 12

    def test_coverage_score_capped_at_100(self):
        score = self._cs(economic_buyer_engaged_rate_pct=0.0,
                         c_suite_engaged_rate_pct=0.0,
                         contact_map_completeness_score=0.0)
        assert score == 100


class TestQualityScore:
    def _qs(self, **kw):
        return fresh_engine()._quality_score(make_input(**kw))

    def test_all_good_gives_zero(self):
        score = self._qs(multi_contact_meeting_rate_pct=0.90,
                         cross_functional_reach_score=0.90,
                         referral_introduction_rate_pct=0.90)
        assert score == 0

    def test_multi_contact_tier_lowest(self):
        score = self._qs(multi_contact_meeting_rate_pct=0.20,
                         cross_functional_reach_score=0.90,
                         referral_introduction_rate_pct=0.90)
        assert score == 40

    def test_multi_contact_tier_mid(self):
        score = self._qs(multi_contact_meeting_rate_pct=0.45,
                         cross_functional_reach_score=0.90,
                         referral_introduction_rate_pct=0.90)
        assert score == 22

    def test_multi_contact_tier_low(self):
        score = self._qs(multi_contact_meeting_rate_pct=0.65,
                         cross_functional_reach_score=0.90,
                         referral_introduction_rate_pct=0.90)
        assert score == 8

    def test_cfr_tier_lowest(self):
        score = self._qs(multi_contact_meeting_rate_pct=0.90,
                         cross_functional_reach_score=0.20,
                         referral_introduction_rate_pct=0.90)
        assert score == 35

    def test_cfr_tier_mid(self):
        score = self._qs(multi_contact_meeting_rate_pct=0.90,
                         cross_functional_reach_score=0.45,
                         referral_introduction_rate_pct=0.90)
        assert score == 18

    def test_referral_tier_lowest(self):
        score = self._qs(multi_contact_meeting_rate_pct=0.90,
                         cross_functional_reach_score=0.90,
                         referral_introduction_rate_pct=0.15)
        assert score == 25

    def test_referral_tier_mid(self):
        score = self._qs(multi_contact_meeting_rate_pct=0.90,
                         cross_functional_reach_score=0.90,
                         referral_introduction_rate_pct=0.35)
        assert score == 12

    def test_quality_score_capped_at_100(self):
        score = self._qs(multi_contact_meeting_rate_pct=0.0,
                         cross_functional_reach_score=0.0,
                         referral_introduction_rate_pct=0.0)
        assert score == 100


class TestNetworkScore:
    def _ns(self, **kw):
        return fresh_engine()._network_score(make_input(**kw))

    def test_all_good_gives_zero(self):
        score = self._ns(dormant_contact_rate_pct=0.0,
                         contact_attrition_rate_pct=0.0,
                         buying_committee_size_vs_avg=2.0)
        assert score == 0

    def test_dormant_tier_highest(self):
        score = self._ns(dormant_contact_rate_pct=0.55,
                         contact_attrition_rate_pct=0.0,
                         buying_committee_size_vs_avg=2.0)
        assert score == 45

    def test_dormant_tier_mid(self):
        score = self._ns(dormant_contact_rate_pct=0.35,
                         contact_attrition_rate_pct=0.0,
                         buying_committee_size_vs_avg=2.0)
        assert score == 25

    def test_dormant_tier_low(self):
        score = self._ns(dormant_contact_rate_pct=0.20,
                         contact_attrition_rate_pct=0.0,
                         buying_committee_size_vs_avg=2.0)
        assert score == 10

    def test_attrition_tier_highest(self):
        score = self._ns(dormant_contact_rate_pct=0.0,
                         contact_attrition_rate_pct=0.40,
                         buying_committee_size_vs_avg=2.0)
        assert score == 30

    def test_attrition_tier_mid(self):
        score = self._ns(dormant_contact_rate_pct=0.0,
                         contact_attrition_rate_pct=0.22,
                         buying_committee_size_vs_avg=2.0)
        assert score == 15

    def test_committee_tier_lowest(self):
        score = self._ns(dormant_contact_rate_pct=0.0,
                         contact_attrition_rate_pct=0.0,
                         buying_committee_size_vs_avg=0.50)
        assert score == 25

    def test_committee_tier_mid(self):
        score = self._ns(dormant_contact_rate_pct=0.0,
                         contact_attrition_rate_pct=0.0,
                         buying_committee_size_vs_avg=0.75)
        assert score == 12

    def test_network_score_capped_at_100(self):
        score = self._ns(dormant_contact_rate_pct=1.0,
                         contact_attrition_rate_pct=1.0,
                         buying_committee_size_vs_avg=0.0)
        assert score == 100


# ---------------------------------------------------------------------------
# 4. Composite weights and cap
# ---------------------------------------------------------------------------

class TestComposite:
    def test_weights_sum_formula(self):
        eng = fresh_engine()
        # With known sub-scores verify the formula
        result = eng._composite(80.0, 60.0, 40.0, 20.0)
        expected = round(80 * 0.30 + 60 * 0.25 + 40 * 0.25 + 20 * 0.20, 2)
        assert result == expected

    def test_composite_capped_at_100(self):
        eng = fresh_engine()
        assert eng._composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_composite_zero_inputs(self):
        eng = fresh_engine()
        assert eng._composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_composite_weights_add_to_1(self):
        # 1*0.30 + 1*0.25 + 1*0.25 + 1*0.20 = 1.00
        eng = fresh_engine()
        assert eng._composite(100.0, 100.0, 100.0, 100.0) == 100.0
        assert eng._composite(1.0, 1.0, 1.0, 1.0) == round(1.0, 2)

    def test_composite_rounding_to_2dp(self):
        eng = fresh_engine()
        result = eng._composite(33.0, 33.0, 33.0, 33.0)
        assert result == round(33 * 0.30 + 33 * 0.25 + 33 * 0.25 + 33 * 0.20, 2)


# ---------------------------------------------------------------------------
# 5. Risk tiers
# ---------------------------------------------------------------------------

class TestRisk:
    def _risk(self, c):
        return fresh_engine()._risk(c)

    def test_critical_at_60(self):
        assert self._risk(60.0) == MultithreadRisk.critical

    def test_critical_above_60(self):
        assert self._risk(95.0) == MultithreadRisk.critical

    def test_high_at_40(self):
        assert self._risk(40.0) == MultithreadRisk.high

    def test_high_below_60(self):
        assert self._risk(59.9) == MultithreadRisk.high

    def test_moderate_at_20(self):
        assert self._risk(20.0) == MultithreadRisk.moderate

    def test_moderate_below_40(self):
        assert self._risk(39.9) == MultithreadRisk.moderate

    def test_low_below_20(self):
        assert self._risk(19.9) == MultithreadRisk.low

    def test_low_at_zero(self):
        assert self._risk(0.0) == MultithreadRisk.low


# ---------------------------------------------------------------------------
# 6. Severity tiers
# ---------------------------------------------------------------------------

class TestSeverity:
    def _sev(self, c):
        return fresh_engine()._severity(c)

    def test_isolated_at_60(self):
        assert self._sev(60.0) == MultithreadSeverity.isolated

    def test_thin_at_40(self):
        assert self._sev(40.0) == MultithreadSeverity.thin

    def test_adequate_at_20(self):
        assert self._sev(20.0) == MultithreadSeverity.adequate

    def test_networked_below_20(self):
        assert self._sev(19.9) == MultithreadSeverity.networked

    def test_networked_at_zero(self):
        assert self._sev(0.0) == MultithreadSeverity.networked


# ---------------------------------------------------------------------------
# 7. All 6 patterns — priority order
# ---------------------------------------------------------------------------

class TestPattern:
    def _pattern(self, **kw):
        return fresh_engine()._pattern(make_input(**kw))

    def test_single_thread_dependency(self):
        pat = self._pattern(
            single_threaded_account_rate_pct=0.55,
            avg_contacts_per_account=1.8,
        )
        assert pat == MultithreadPattern.single_thread_dependency

    def test_it_bubble(self):
        # must NOT trigger single_thread_dependency first
        pat = self._pattern(
            single_threaded_account_rate_pct=0.10,
            avg_contacts_per_account=4.0,
            c_suite_engaged_rate_pct=0.15,
            vp_engaged_rate_pct=0.20,
            technical_buyer_engaged_rate_pct=0.70,
        )
        assert pat == MultithreadPattern.it_bubble

    def test_executive_bypass(self):
        pat = self._pattern(
            single_threaded_account_rate_pct=0.10,
            avg_contacts_per_account=4.0,
            c_suite_engaged_rate_pct=0.70,
            end_user_engaged_rate_pct=0.20,
            technical_buyer_engaged_rate_pct=0.30,
            vp_engaged_rate_pct=0.50,
        )
        assert pat == MultithreadPattern.executive_bypass

    def test_vertical_tunnel(self):
        pat = self._pattern(
            single_threaded_account_rate_pct=0.10,
            avg_contacts_per_account=4.0,
            c_suite_engaged_rate_pct=0.30,
            vp_engaged_rate_pct=0.55,
            economic_buyer_engaged_rate_pct=0.20,
            technical_buyer_engaged_rate_pct=0.30,
        )
        assert pat == MultithreadPattern.vertical_tunnel

    def test_breadth_stall(self):
        pat = self._pattern(
            single_threaded_account_rate_pct=0.10,
            avg_contacts_per_account=4.0,
            c_suite_engaged_rate_pct=0.30,
            vp_engaged_rate_pct=0.30,
            technical_buyer_engaged_rate_pct=0.30,
            economic_buyer_engaged_rate_pct=0.80,
            dormant_contact_rate_pct=0.50,
            avg_new_contacts_added_per_quarter=0.8,
        )
        assert pat == MultithreadPattern.breadth_stall

    def test_none_pattern(self):
        pat = self._pattern()  # baseline good health
        assert pat == MultithreadPattern.none

    def test_single_thread_dependency_priority_over_it_bubble(self):
        # If single_thread_dependency conditions AND it_bubble conditions both met
        pat = self._pattern(
            single_threaded_account_rate_pct=0.55,
            avg_contacts_per_account=1.8,
            c_suite_engaged_rate_pct=0.15,
            vp_engaged_rate_pct=0.20,
            technical_buyer_engaged_rate_pct=0.70,
        )
        assert pat == MultithreadPattern.single_thread_dependency


# ---------------------------------------------------------------------------
# 8. Action rules — risk × pattern
# ---------------------------------------------------------------------------

class TestAction:
    def _action(self, risk, pat):
        return fresh_engine()._action(risk, pat)

    # Critical
    def test_critical_single_thread_dependency(self):
        assert self._action(MultithreadRisk.critical, MultithreadPattern.single_thread_dependency) == MultithreadAction.deal_restructure_escalation

    def test_critical_breadth_stall(self):
        assert self._action(MultithreadRisk.critical, MultithreadPattern.breadth_stall) == MultithreadAction.deal_restructure_escalation

    def test_critical_it_bubble(self):
        assert self._action(MultithreadRisk.critical, MultithreadPattern.it_bubble) == MultithreadAction.account_rescue_intervention

    def test_critical_executive_bypass(self):
        assert self._action(MultithreadRisk.critical, MultithreadPattern.executive_bypass) == MultithreadAction.account_rescue_intervention

    def test_critical_vertical_tunnel(self):
        assert self._action(MultithreadRisk.critical, MultithreadPattern.vertical_tunnel) == MultithreadAction.account_rescue_intervention

    def test_critical_none(self):
        assert self._action(MultithreadRisk.critical, MultithreadPattern.none) == MultithreadAction.account_rescue_intervention

    # High
    def test_high_single_thread_dependency(self):
        assert self._action(MultithreadRisk.high, MultithreadPattern.single_thread_dependency) == MultithreadAction.contact_expansion_coaching

    def test_high_it_bubble(self):
        assert self._action(MultithreadRisk.high, MultithreadPattern.it_bubble) == MultithreadAction.it_champion_bridge_coaching

    def test_high_executive_bypass(self):
        assert self._action(MultithreadRisk.high, MultithreadPattern.executive_bypass) == MultithreadAction.exec_introduction_coaching

    def test_high_vertical_tunnel(self):
        assert self._action(MultithreadRisk.high, MultithreadPattern.vertical_tunnel) == MultithreadAction.stakeholder_mapping_workshop

    def test_high_breadth_stall(self):
        assert self._action(MultithreadRisk.high, MultithreadPattern.breadth_stall) == MultithreadAction.relationship_breadth_sprint

    def test_high_none(self):
        assert self._action(MultithreadRisk.high, MultithreadPattern.none) == MultithreadAction.multithreading_monitoring

    # Moderate
    def test_moderate_any_pattern(self):
        for pat in MultithreadPattern:
            assert self._action(MultithreadRisk.moderate, pat) == MultithreadAction.multithreading_monitoring

    # Low
    def test_low_any_pattern(self):
        for pat in MultithreadPattern:
            assert self._action(MultithreadRisk.low, pat) == MultithreadAction.no_action


# ---------------------------------------------------------------------------
# 9. has_multithread_gap
# ---------------------------------------------------------------------------

class TestHasMultithreadGap:
    def _gap(self, comp, **kw):
        eng = fresh_engine()
        inp = make_input(**kw)
        return eng._has_multithread_gap(inp, comp)

    def test_gap_true_composite_gte_40(self):
        assert self._gap(40.0) is True

    def test_gap_true_single_threaded_gte_040(self):
        assert self._gap(0.0, single_threaded_account_rate_pct=0.40) is True

    def test_gap_true_eb_lte_040(self):
        assert self._gap(0.0, economic_buyer_engaged_rate_pct=0.40) is True

    def test_gap_false_all_ok(self):
        assert self._gap(39.9,
                         single_threaded_account_rate_pct=0.39,
                         economic_buyer_engaged_rate_pct=0.41) is False

    def test_gap_true_composite_exactly_60(self):
        assert self._gap(60.0) is True


# ---------------------------------------------------------------------------
# 10. requires_expansion_coaching
# ---------------------------------------------------------------------------

class TestRequiresExpansionCoaching:
    def _rec(self, comp, **kw):
        eng = fresh_engine()
        inp = make_input(**kw)
        return eng._requires_expansion_coaching(inp, comp)

    def test_true_composite_gte_25(self):
        assert self._rec(25.0) is True

    def test_true_avg_contacts_lte_25(self):
        assert self._rec(0.0, avg_contacts_per_account=2.5) is True

    def test_true_multi_contact_lte_040(self):
        assert self._rec(0.0, multi_contact_meeting_rate_pct=0.40) is True

    def test_false_all_ok(self):
        assert self._rec(24.9,
                         avg_contacts_per_account=2.6,
                         multi_contact_meeting_rate_pct=0.41) is False

    def test_true_composite_exactly_25(self):
        assert self._rec(25.0) is True


# ---------------------------------------------------------------------------
# 11. estimated_vulnerable_pipeline_usd
# ---------------------------------------------------------------------------

class TestVulnerablePipeline:
    def _vp(self, comp, **kw):
        eng = fresh_engine()
        inp = make_input(**kw)
        return eng._vulnerable_pipeline(inp, comp)

    def test_formula_basic(self):
        result = self._vp(50.0,
                          total_active_accounts=100,
                          avg_deal_value_usd=50_000.0,
                          single_threaded_account_rate_pct=0.30)
        expected = round(100 * 50_000.0 * 0.30 * (50.0 / 100), 2)
        assert result == expected

    def test_zero_composite_gives_zero(self):
        assert self._vp(0.0, total_active_accounts=100,
                        avg_deal_value_usd=50_000.0,
                        single_threaded_account_rate_pct=0.50) == 0.0

    def test_zero_accounts_gives_zero(self):
        assert self._vp(80.0, total_active_accounts=0,
                        avg_deal_value_usd=50_000.0,
                        single_threaded_account_rate_pct=0.50) == 0.0

    def test_rounded_to_2dp(self):
        result = self._vp(33.33,
                          total_active_accounts=7,
                          avg_deal_value_usd=12_345.67,
                          single_threaded_account_rate_pct=0.333)
        assert result == round(7 * 12_345.67 * 0.333 * (33.33 / 100), 2)

    def test_full_single_threaded(self):
        result = self._vp(100.0,
                          total_active_accounts=10,
                          avg_deal_value_usd=100_000.0,
                          single_threaded_account_rate_pct=1.0)
        assert result == round(10 * 100_000.0 * 1.0 * 1.0, 2)


# ---------------------------------------------------------------------------
# 12. multithread_signal
# ---------------------------------------------------------------------------

class TestMultithreadSignal:
    def _signal(self, comp, pat, **kw):
        eng = fresh_engine()
        inp = make_input(**kw)
        return eng._signal(inp, pat, comp)

    def test_stable_message_below_20(self):
        msg = self._signal(10.0, MultithreadPattern.none)
        assert "strong" in msg.lower()
        assert "benchmark" in msg.lower()

    def test_active_includes_label_single_thread(self):
        msg = self._signal(50.0, MultithreadPattern.single_thread_dependency,
                           avg_contacts_per_account=1.5,
                           single_threaded_account_rate_pct=0.60,
                           economic_buyer_engaged_rate_pct=0.30)
        assert "Single-thread dependency" in msg

    def test_active_includes_label_it_bubble(self):
        msg = self._signal(50.0, MultithreadPattern.it_bubble,
                           avg_contacts_per_account=3.0,
                           single_threaded_account_rate_pct=0.20,
                           economic_buyer_engaged_rate_pct=0.60)
        assert "IT bubble" in msg

    def test_active_includes_label_executive_bypass(self):
        msg = self._signal(50.0, MultithreadPattern.executive_bypass,
                           avg_contacts_per_account=3.0,
                           single_threaded_account_rate_pct=0.20,
                           economic_buyer_engaged_rate_pct=0.60)
        assert "Executive bypass" in msg

    def test_active_includes_label_vertical_tunnel(self):
        msg = self._signal(50.0, MultithreadPattern.vertical_tunnel,
                           avg_contacts_per_account=3.0,
                           single_threaded_account_rate_pct=0.20,
                           economic_buyer_engaged_rate_pct=0.60)
        assert "Vertical tunnel" in msg

    def test_active_includes_label_breadth_stall(self):
        msg = self._signal(50.0, MultithreadPattern.breadth_stall,
                           avg_contacts_per_account=3.0,
                           single_threaded_account_rate_pct=0.20,
                           economic_buyer_engaged_rate_pct=0.60)
        assert "Breadth stall" in msg

    def test_active_includes_pct_components(self):
        msg = self._signal(45.0, MultithreadPattern.none,
                           avg_contacts_per_account=2.3,
                           single_threaded_account_rate_pct=0.45,
                           economic_buyer_engaged_rate_pct=0.35)
        assert "avg contacts/account" in msg
        assert "single-threaded" in msg
        assert "EB engaged" in msg
        assert "composite" in msg

    def test_active_shows_composite_rounded(self):
        msg = self._signal(47.7, MultithreadPattern.none,
                           avg_contacts_per_account=2.0,
                           single_threaded_account_rate_pct=0.50,
                           economic_buyer_engaged_rate_pct=0.35)
        assert "composite 48" in msg


# ---------------------------------------------------------------------------
# 13. assess(), assess_batch(), summary()
# ---------------------------------------------------------------------------

class TestAssess:
    def test_assess_returns_multithread_result(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result, MultithreadResult)

    def test_assess_rep_id_region_propagated(self):
        eng = fresh_engine()
        result = eng.assess(make_input(rep_id="X1", region="LATAM"))
        assert result.rep_id == "X1"
        assert result.region == "LATAM"

    def test_assess_stores_result(self):
        eng = fresh_engine()
        eng.assess(make_input())
        assert len(eng._results) == 1

    def test_assess_batch_returns_list(self):
        eng = fresh_engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = eng.assess_batch(inputs)
        assert len(results) == 5
        assert all(isinstance(r, MultithreadResult) for r in results)

    def test_assess_batch_stores_all(self):
        eng = fresh_engine()
        eng.assess_batch([make_input() for _ in range(3)])
        assert len(eng._results) == 3

    def test_summary_empty_engine(self):
        eng = fresh_engine()
        s = eng.summary()
        assert s["total"] == 0
        assert s["avg_multithread_composite"] == 0.0
        assert s["total_estimated_vulnerable_pipeline_usd"] == 0.0

    def test_summary_has_13_keys(self):
        eng = fresh_engine()
        s = eng.summary()
        assert len(s) == 13

    def test_summary_13_keys_names(self):
        eng = fresh_engine()
        s = eng.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_multithread_composite", "multithread_gap_count",
            "expansion_coaching_count", "avg_depth_score", "avg_coverage_score",
            "avg_quality_score", "avg_network_score",
            "total_estimated_vulnerable_pipeline_usd",
        }
        assert set(s.keys()) == expected

    def test_summary_totals_after_batch(self):
        eng = fresh_engine()
        eng.assess_batch([make_input() for _ in range(4)])
        s = eng.summary()
        assert s["total"] == 4

    def test_summary_risk_counts_sum_to_total(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=str(i)) for i in range(6)])
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_to_total(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=str(i)) for i in range(4)])
        s = eng.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_avg_composite_rounded(self):
        eng = fresh_engine()
        # Two identical inputs — average should equal a single result's composite
        inp = make_input()
        r = fresh_engine().assess(inp)
        eng.assess(make_input())
        eng.assess(make_input())
        s = eng.summary()
        assert s["avg_multithread_composite"] == round(r.multithread_composite, 1)


# ---------------------------------------------------------------------------
# 14. Edge cases: zero input, max input, engine isolation
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_input_does_not_crash(self):
        eng = fresh_engine()
        inp = make_input(
            avg_contacts_per_account=0.0,
            single_threaded_account_rate_pct=0.0,
            avg_new_contacts_added_per_quarter=0.0,
            contact_attrition_rate_pct=0.0,
            economic_buyer_engaged_rate_pct=0.0,
            technical_buyer_engaged_rate_pct=0.0,
            end_user_engaged_rate_pct=0.0,
            champion_to_non_champion_ratio=0.0,
            avg_email_threads_per_contact=0.0,
            multi_contact_meeting_rate_pct=0.0,
            cross_functional_reach_score=0.0,
            referral_introduction_rate_pct=0.0,
            dormant_contact_rate_pct=0.0,
            contact_map_completeness_score=0.0,
            buying_committee_size_vs_avg=0.0,
            c_suite_engaged_rate_pct=0.0,
            vp_engaged_rate_pct=0.0,
            total_active_accounts=0,
            avg_deal_value_usd=0.0,
        )
        result = eng.assess(inp)
        assert isinstance(result, MultithreadResult)

    def test_max_input_caps_composite_at_100(self):
        eng = fresh_engine()
        inp = make_input(
            avg_contacts_per_account=0.0,
            single_threaded_account_rate_pct=1.0,
            avg_new_contacts_added_per_quarter=0.0,
            contact_attrition_rate_pct=1.0,
            economic_buyer_engaged_rate_pct=0.0,
            technical_buyer_engaged_rate_pct=1.0,
            end_user_engaged_rate_pct=0.0,
            multi_contact_meeting_rate_pct=0.0,
            cross_functional_reach_score=0.0,
            referral_introduction_rate_pct=0.0,
            dormant_contact_rate_pct=1.0,
            contact_map_completeness_score=0.0,
            buying_committee_size_vs_avg=0.0,
            c_suite_engaged_rate_pct=0.0,
            vp_engaged_rate_pct=0.0,
            total_active_accounts=10_000,
            avg_deal_value_usd=1_000_000.0,
        )
        result = eng.assess(inp)
        assert result.multithread_composite <= 100.0
        assert result.depth_score <= 100
        assert result.coverage_score <= 100
        assert result.quality_score <= 100
        assert result.network_score <= 100

    def test_engine_isolation(self):
        """Two independent engines should not share state."""
        eng1 = fresh_engine()
        eng2 = fresh_engine()
        eng1.assess(make_input(rep_id="A"))
        eng1.assess(make_input(rep_id="B"))
        assert len(eng2._results) == 0
        assert len(eng1._results) == 2

    def test_assess_result_risk_is_string_not_enum(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert type(result.multithread_risk) is str
        assert type(result.multithread_pattern) is str
        assert type(result.multithread_severity) is str
        assert type(result.recommended_action) is str

    def test_summary_total_vulnerable_pipeline_accumulates(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input(total_active_accounts=50, avg_deal_value_usd=10_000.0,
                                    single_threaded_account_rate_pct=0.50))
        r2 = eng.assess(make_input(total_active_accounts=20, avg_deal_value_usd=5_000.0,
                                    single_threaded_account_rate_pct=0.30))
        s = eng.summary()
        expected = round(r1.estimated_vulnerable_pipeline_usd + r2.estimated_vulnerable_pipeline_usd, 2)
        assert s["total_estimated_vulnerable_pipeline_usd"] == expected
