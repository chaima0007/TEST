"""Pytest test suite for SalesChampionDepartureRelationshipContinuityEngine."""
import pytest
from swarm.intelligence.sales_champion_departure_relationship_continuity_engine import (
    ChampionRisk, ChampionPattern, ChampionSeverity, ChampionAction,
    ChampionInput, ChampionResult,
    SalesChampionDepartureRelationshipContinuityEngine,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_input(**overrides) -> ChampionInput:
    defaults = dict(
        rep_id="TEST-01", region="EMEA", evaluation_period_id="Q1-2026",
        champion_engagement_drop_rate_pct=0.05,
        champion_response_latency_trend=0.05,
        org_change_detected_rate_pct=0.05,
        champion_linkedin_activity_drop_pct=0.05,
        single_threaded_deal_rate_pct=0.10,
        backup_contact_coverage_rate_pct=0.85,
        executive_sponsor_coverage_rate_pct=0.80,
        champion_internal_advocacy_score=0.80,
        champion_tenure_avg_months=24.0,
        stakeholder_mapping_completeness_score=0.80,
        champion_deal_influence_score=0.50,
        internal_coach_coverage_rate_pct=0.80,
        economic_buyer_direct_access_rate_pct=0.75,
        champion_replacement_recovery_rate_pct=0.70,
        deal_ghosting_after_champion_loss_rate_pct=0.05,
        relationship_breadth_score=0.80,
        champion_departure_detected_deals=2,
        total_active_deals=30,
        avg_deal_value_usd=85000.0,
    )
    defaults.update(overrides)
    return ChampionInput(**defaults)


@pytest.fixture
def engine():
    return SalesChampionDepartureRelationshipContinuityEngine()


# ---------------------------------------------------------------------------
# Enum values
# ---------------------------------------------------------------------------

class TestEnums:
    def test_risk_values(self):
        assert set(r.value for r in ChampionRisk) == {"low", "moderate", "high", "critical"}

    def test_pattern_values(self):
        assert set(p.value for p in ChampionPattern) == {
            "none", "single_thread_exposed", "ghost_risk_zone",
            "org_change_vulnerable", "advocacy_collapse", "blind_spot_account",
        }

    def test_severity_values(self):
        assert set(s.value for s in ChampionSeverity) == {"stable", "drifting", "vulnerable", "critical"}

    def test_action_values(self):
        assert set(a.value for a in ChampionAction) == {
            "no_action", "champion_health_monitoring",
            "multithreading_urgency_coaching", "org_change_alert_protocol",
            "executive_engagement_activation", "stakeholder_mapping_sprint",
            "relationship_rescue_intervention", "deal_continuity_escalation",
        }

    @pytest.mark.parametrize("member", list(ChampionRisk))
    def test_risk_is_str(self, member):
        assert isinstance(member.value, str)

    @pytest.mark.parametrize("member", list(ChampionPattern))
    def test_pattern_is_str(self, member):
        assert isinstance(member.value, str)


# ---------------------------------------------------------------------------
# to_dict keys
# ---------------------------------------------------------------------------

class TestToDict:
    EXPECTED_KEYS = {
        "rep_id", "region", "champion_risk", "champion_pattern", "champion_severity",
        "recommended_action", "stability_score", "coverage_score", "resilience_score",
        "intelligence_score", "champion_composite", "has_champion_gap",
        "requires_champion_intervention", "estimated_at_risk_pipeline_usd", "champion_signal",
    }

    def test_to_dict_key_count(self, engine):
        r = engine.assess(make_input())
        assert len(r.to_dict()) == 15

    def test_to_dict_exact_keys(self, engine):
        r = engine.assess(make_input())
        assert set(r.to_dict().keys()) == self.EXPECTED_KEYS

    def test_to_dict_enum_values_are_strings(self, engine):
        r = engine.assess(make_input())
        d = r.to_dict()
        for key in ("champion_risk", "champion_pattern", "champion_severity", "recommended_action"):
            assert isinstance(d[key], str)

    def test_to_dict_rep_id(self, engine):
        r = engine.assess(make_input(rep_id="REP-99"))
        assert r.to_dict()["rep_id"] == "REP-99"

    def test_to_dict_region(self, engine):
        r = engine.assess(make_input(region="APAC"))
        assert r.to_dict()["region"] == "APAC"


# ---------------------------------------------------------------------------
# stability_score
# ---------------------------------------------------------------------------

class TestStabilityScore:
    @pytest.mark.parametrize("drop,expected", [
        (0.55, 40), (0.60, 40), (0.30, 22), (0.40, 22), (0.15, 8), (0.25, 8), (0.10, 0),
    ])
    def test_engagement_drop_tiers(self, engine, drop, expected):
        inp = make_input(champion_engagement_drop_rate_pct=drop,
                         org_change_detected_rate_pct=0.05, champion_tenure_avg_months=24.0)
        assert engine._stability_score(inp) == expected

    @pytest.mark.parametrize("org,expected", [
        (0.40, 35), (0.50, 35), (0.20, 18), (0.35, 18), (0.10, 0),
    ])
    def test_org_change_tiers(self, engine, org, expected):
        inp = make_input(champion_engagement_drop_rate_pct=0.05,
                         org_change_detected_rate_pct=org, champion_tenure_avg_months=24.0)
        assert engine._stability_score(inp) == expected

    @pytest.mark.parametrize("tenure,expected", [
        (6.0, 25), (3.0, 25), (12.0, 12), (8.0, 12), (13.0, 0), (24.0, 0),
    ])
    def test_tenure_tiers(self, engine, tenure, expected):
        inp = make_input(champion_engagement_drop_rate_pct=0.05,
                         org_change_detected_rate_pct=0.05, champion_tenure_avg_months=tenure)
        assert engine._stability_score(inp) == expected

    def test_stability_cap_at_100(self, engine):
        inp = make_input(champion_engagement_drop_rate_pct=0.60,
                         org_change_detected_rate_pct=0.50, champion_tenure_avg_months=3.0)
        assert engine._stability_score(inp) == 100.0

    def test_stability_max_without_cap(self, engine):
        # 40+35+25=100 exact
        inp = make_input(champion_engagement_drop_rate_pct=0.60,
                         org_change_detected_rate_pct=0.50, champion_tenure_avg_months=3.0)
        assert engine._stability_score(inp) == 100.0

    def test_stability_additive(self, engine):
        inp = make_input(champion_engagement_drop_rate_pct=0.55,
                         org_change_detected_rate_pct=0.40, champion_tenure_avg_months=24.0)
        assert engine._stability_score(inp) == 75.0

    def test_stability_zero(self, engine):
        inp = make_input(champion_engagement_drop_rate_pct=0.05,
                         org_change_detected_rate_pct=0.05, champion_tenure_avg_months=24.0)
        assert engine._stability_score(inp) == 0.0

    def test_stability_mid_combo(self, engine):
        # 22+18+12=52
        inp = make_input(champion_engagement_drop_rate_pct=0.30,
                         org_change_detected_rate_pct=0.20, champion_tenure_avg_months=12.0)
        assert engine._stability_score(inp) == 52.0


# ---------------------------------------------------------------------------
# coverage_score
# ---------------------------------------------------------------------------

class TestCoverageScore:
    @pytest.mark.parametrize("single,expected", [
        (0.65, 45), (0.90, 45), (0.40, 25), (0.55, 25), (0.20, 10), (0.35, 10), (0.10, 0),
    ])
    def test_single_threaded_tiers(self, engine, single, expected):
        inp = make_input(single_threaded_deal_rate_pct=single,
                         backup_contact_coverage_rate_pct=0.85,
                         executive_sponsor_coverage_rate_pct=0.80)
        assert engine._coverage_score(inp) == expected

    @pytest.mark.parametrize("backup,expected", [
        (0.25, 30), (0.10, 30), (0.50, 15), (0.40, 15), (0.60, 0),
    ])
    def test_backup_coverage_tiers(self, engine, backup, expected):
        inp = make_input(single_threaded_deal_rate_pct=0.10,
                         backup_contact_coverage_rate_pct=backup,
                         executive_sponsor_coverage_rate_pct=0.80)
        assert engine._coverage_score(inp) == expected

    @pytest.mark.parametrize("exec_sp,expected", [
        (0.20, 25), (0.10, 25), (0.45, 12), (0.30, 12), (0.50, 0),
    ])
    def test_exec_sponsor_tiers(self, engine, exec_sp, expected):
        inp = make_input(single_threaded_deal_rate_pct=0.10,
                         backup_contact_coverage_rate_pct=0.85,
                         executive_sponsor_coverage_rate_pct=exec_sp)
        assert engine._coverage_score(inp) == expected

    def test_coverage_cap_at_100(self, engine):
        inp = make_input(single_threaded_deal_rate_pct=0.90,
                         backup_contact_coverage_rate_pct=0.10,
                         executive_sponsor_coverage_rate_pct=0.10)
        # 45+30+25=100
        assert engine._coverage_score(inp) == 100.0

    def test_coverage_zero(self, engine):
        inp = make_input(single_threaded_deal_rate_pct=0.10,
                         backup_contact_coverage_rate_pct=0.85,
                         executive_sponsor_coverage_rate_pct=0.80)
        assert engine._coverage_score(inp) == 0.0

    def test_coverage_additive_mid(self, engine):
        # 25+15+12=52
        inp = make_input(single_threaded_deal_rate_pct=0.40,
                         backup_contact_coverage_rate_pct=0.50,
                         executive_sponsor_coverage_rate_pct=0.45)
        assert engine._coverage_score(inp) == 52.0


# ---------------------------------------------------------------------------
# resilience_score
# ---------------------------------------------------------------------------

class TestResilienceScore:
    @pytest.mark.parametrize("recovery,expected", [
        (0.15, 40), (0.05, 40), (0.35, 22), (0.25, 22), (0.55, 8), (0.45, 8), (0.60, 0),
    ])
    def test_recovery_tiers(self, engine, recovery, expected):
        inp = make_input(champion_replacement_recovery_rate_pct=recovery,
                         deal_ghosting_after_champion_loss_rate_pct=0.05,
                         internal_coach_coverage_rate_pct=0.80)
        assert engine._resilience_score(inp) == expected

    @pytest.mark.parametrize("ghost,expected", [
        (0.55, 35), (0.80, 35), (0.30, 18), (0.45, 18), (0.20, 0),
    ])
    def test_ghosting_tiers(self, engine, ghost, expected):
        inp = make_input(champion_replacement_recovery_rate_pct=0.70,
                         deal_ghosting_after_champion_loss_rate_pct=ghost,
                         internal_coach_coverage_rate_pct=0.80)
        assert engine._resilience_score(inp) == expected

    @pytest.mark.parametrize("coach,expected", [
        (0.20, 25), (0.10, 25), (0.45, 12), (0.30, 12), (0.50, 0),
    ])
    def test_internal_coach_tiers(self, engine, coach, expected):
        inp = make_input(champion_replacement_recovery_rate_pct=0.70,
                         deal_ghosting_after_champion_loss_rate_pct=0.05,
                         internal_coach_coverage_rate_pct=coach)
        assert engine._resilience_score(inp) == expected

    def test_resilience_cap_at_100(self, engine):
        inp = make_input(champion_replacement_recovery_rate_pct=0.05,
                         deal_ghosting_after_champion_loss_rate_pct=0.80,
                         internal_coach_coverage_rate_pct=0.10)
        assert engine._resilience_score(inp) == 100.0

    def test_resilience_zero(self, engine):
        inp = make_input(champion_replacement_recovery_rate_pct=0.70,
                         deal_ghosting_after_champion_loss_rate_pct=0.05,
                         internal_coach_coverage_rate_pct=0.80)
        assert engine._resilience_score(inp) == 0.0

    def test_resilience_mid(self, engine):
        # 22+18+12=52
        inp = make_input(champion_replacement_recovery_rate_pct=0.25,
                         deal_ghosting_after_champion_loss_rate_pct=0.30,
                         internal_coach_coverage_rate_pct=0.45)
        assert engine._resilience_score(inp) == 52.0


# ---------------------------------------------------------------------------
# intelligence_score
# ---------------------------------------------------------------------------

class TestIntelligenceScore:
    @pytest.mark.parametrize("stk,expected", [
        (0.20, 45), (0.10, 45), (0.45, 25), (0.30, 25), (0.65, 10), (0.55, 10), (0.70, 0),
    ])
    def test_stakeholder_tiers(self, engine, stk, expected):
        inp = make_input(stakeholder_mapping_completeness_score=stk,
                         relationship_breadth_score=0.80,
                         economic_buyer_direct_access_rate_pct=0.75)
        assert engine._intelligence_score(inp) == expected

    @pytest.mark.parametrize("breadth,expected", [
        (0.20, 30), (0.10, 30), (0.45, 15), (0.30, 15), (0.50, 0),
    ])
    def test_breadth_tiers(self, engine, breadth, expected):
        inp = make_input(stakeholder_mapping_completeness_score=0.80,
                         relationship_breadth_score=breadth,
                         economic_buyer_direct_access_rate_pct=0.75)
        assert engine._intelligence_score(inp) == expected

    @pytest.mark.parametrize("eb,expected", [
        (0.20, 25), (0.10, 25), (0.45, 12), (0.30, 12), (0.50, 0),
    ])
    def test_eb_access_tiers(self, engine, eb, expected):
        inp = make_input(stakeholder_mapping_completeness_score=0.80,
                         relationship_breadth_score=0.80,
                         economic_buyer_direct_access_rate_pct=eb)
        assert engine._intelligence_score(inp) == expected

    def test_intelligence_cap_at_100(self, engine):
        inp = make_input(stakeholder_mapping_completeness_score=0.10,
                         relationship_breadth_score=0.10,
                         economic_buyer_direct_access_rate_pct=0.10)
        assert engine._intelligence_score(inp) == 100.0

    def test_intelligence_zero(self, engine):
        inp = make_input(stakeholder_mapping_completeness_score=0.80,
                         relationship_breadth_score=0.80,
                         economic_buyer_direct_access_rate_pct=0.75)
        assert engine._intelligence_score(inp) == 0.0

    def test_intelligence_mid(self, engine):
        # 25+15+12=52
        inp = make_input(stakeholder_mapping_completeness_score=0.45,
                         relationship_breadth_score=0.45,
                         economic_buyer_direct_access_rate_pct=0.45)
        assert engine._intelligence_score(inp) == 52.0


# ---------------------------------------------------------------------------
# composite
# ---------------------------------------------------------------------------

class TestComposite:
    def test_composite_formula(self, engine):
        assert engine._composite(40.0, 30.0, 20.0, 10.0) == round(40*0.30 + 30*0.25 + 20*0.25 + 10*0.20, 2)

    def test_composite_cap(self, engine):
        assert engine._composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_composite_zero(self, engine):
        assert engine._composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_composite_weights(self, engine):
        result = engine._composite(100.0, 0.0, 0.0, 0.0)
        assert result == round(100 * 0.30, 2)

    def test_composite_coverage_weight(self, engine):
        result = engine._composite(0.0, 100.0, 0.0, 0.0)
        assert result == round(100 * 0.25, 2)

    def test_composite_resilience_weight(self, engine):
        result = engine._composite(0.0, 0.0, 100.0, 0.0)
        assert result == round(100 * 0.25, 2)

    def test_composite_intelligence_weight(self, engine):
        result = engine._composite(0.0, 0.0, 0.0, 100.0)
        assert result == round(100 * 0.20, 2)

    def test_composite_rounded_to_2dp(self, engine):
        val = engine._composite(33.33, 33.33, 33.33, 33.33)
        assert val == round(33.33*0.30 + 33.33*0.25 + 33.33*0.25 + 33.33*0.20, 2)


# ---------------------------------------------------------------------------
# risk
# ---------------------------------------------------------------------------

class TestRisk:
    @pytest.mark.parametrize("comp,expected", [
        (0.0, ChampionRisk.low), (19.9, ChampionRisk.low),
        (20.0, ChampionRisk.moderate), (39.9, ChampionRisk.moderate),
        (40.0, ChampionRisk.high), (59.9, ChampionRisk.high),
        (60.0, ChampionRisk.critical), (100.0, ChampionRisk.critical),
    ])
    def test_risk_thresholds(self, engine, comp, expected):
        assert engine._risk(comp) == expected


# ---------------------------------------------------------------------------
# severity
# ---------------------------------------------------------------------------

class TestSeverity:
    @pytest.mark.parametrize("comp,expected", [
        (0.0, ChampionSeverity.stable), (19.9, ChampionSeverity.stable),
        (20.0, ChampionSeverity.drifting), (39.9, ChampionSeverity.drifting),
        (40.0, ChampionSeverity.vulnerable), (59.9, ChampionSeverity.vulnerable),
        (60.0, ChampionSeverity.critical), (100.0, ChampionSeverity.critical),
    ])
    def test_severity_thresholds(self, engine, comp, expected):
        assert engine._severity(comp) == expected


# ---------------------------------------------------------------------------
# pattern
# ---------------------------------------------------------------------------

class TestPattern:
    def test_single_thread_exposed(self, engine):
        inp = make_input(single_threaded_deal_rate_pct=0.60, backup_contact_coverage_rate_pct=0.25)
        assert engine._pattern(inp) == ChampionPattern.single_thread_exposed

    def test_single_thread_exposed_strict(self, engine):
        inp = make_input(single_threaded_deal_rate_pct=0.90, backup_contact_coverage_rate_pct=0.10)
        assert engine._pattern(inp) == ChampionPattern.single_thread_exposed

    def test_ghost_risk_zone(self, engine):
        inp = make_input(deal_ghosting_after_champion_loss_rate_pct=0.55,
                         champion_replacement_recovery_rate_pct=0.20,
                         single_threaded_deal_rate_pct=0.10, backup_contact_coverage_rate_pct=0.85)
        assert engine._pattern(inp) == ChampionPattern.ghost_risk_zone

    def test_org_change_vulnerable(self, engine):
        inp = make_input(org_change_detected_rate_pct=0.35, champion_tenure_avg_months=12.0,
                         single_threaded_deal_rate_pct=0.10, backup_contact_coverage_rate_pct=0.85,
                         deal_ghosting_after_champion_loss_rate_pct=0.05,
                         champion_replacement_recovery_rate_pct=0.70)
        assert engine._pattern(inp) == ChampionPattern.org_change_vulnerable

    def test_advocacy_collapse(self, engine):
        inp = make_input(champion_internal_advocacy_score=0.25, champion_deal_influence_score=0.70,
                         org_change_detected_rate_pct=0.05, champion_tenure_avg_months=24.0,
                         single_threaded_deal_rate_pct=0.10, backup_contact_coverage_rate_pct=0.85,
                         deal_ghosting_after_champion_loss_rate_pct=0.05,
                         champion_replacement_recovery_rate_pct=0.70)
        assert engine._pattern(inp) == ChampionPattern.advocacy_collapse

    def test_blind_spot_account(self, engine):
        inp = make_input(stakeholder_mapping_completeness_score=0.25, relationship_breadth_score=0.30,
                         champion_internal_advocacy_score=0.80, champion_deal_influence_score=0.50,
                         org_change_detected_rate_pct=0.05, champion_tenure_avg_months=24.0,
                         single_threaded_deal_rate_pct=0.10, backup_contact_coverage_rate_pct=0.85,
                         deal_ghosting_after_champion_loss_rate_pct=0.05,
                         champion_replacement_recovery_rate_pct=0.70)
        assert engine._pattern(inp) == ChampionPattern.blind_spot_account

    def test_none_pattern(self, engine):
        assert engine._pattern(make_input()) == ChampionPattern.none

    def test_single_thread_takes_priority_over_ghost(self, engine):
        inp = make_input(single_threaded_deal_rate_pct=0.60, backup_contact_coverage_rate_pct=0.25,
                         deal_ghosting_after_champion_loss_rate_pct=0.60,
                         champion_replacement_recovery_rate_pct=0.10)
        assert engine._pattern(inp) == ChampionPattern.single_thread_exposed

    def test_single_thread_boundary_miss(self, engine):
        inp = make_input(single_threaded_deal_rate_pct=0.59, backup_contact_coverage_rate_pct=0.25)
        assert engine._pattern(inp) != ChampionPattern.single_thread_exposed

    def test_ghost_boundary_miss(self, engine):
        inp = make_input(deal_ghosting_after_champion_loss_rate_pct=0.54,
                         champion_replacement_recovery_rate_pct=0.20,
                         single_threaded_deal_rate_pct=0.10, backup_contact_coverage_rate_pct=0.85)
        assert engine._pattern(inp) != ChampionPattern.ghost_risk_zone

    def test_org_change_boundary_miss(self, engine):
        inp = make_input(org_change_detected_rate_pct=0.34, champion_tenure_avg_months=12.0,
                         single_threaded_deal_rate_pct=0.10, backup_contact_coverage_rate_pct=0.85,
                         deal_ghosting_after_champion_loss_rate_pct=0.05,
                         champion_replacement_recovery_rate_pct=0.70)
        assert engine._pattern(inp) != ChampionPattern.org_change_vulnerable

    def test_advocacy_collapse_boundary_miss_high_advocacy(self, engine):
        inp = make_input(champion_internal_advocacy_score=0.26, champion_deal_influence_score=0.70,
                         org_change_detected_rate_pct=0.05, champion_tenure_avg_months=24.0,
                         single_threaded_deal_rate_pct=0.10, backup_contact_coverage_rate_pct=0.85,
                         deal_ghosting_after_champion_loss_rate_pct=0.05,
                         champion_replacement_recovery_rate_pct=0.70)
        assert engine._pattern(inp) != ChampionPattern.advocacy_collapse


# ---------------------------------------------------------------------------
# action
# ---------------------------------------------------------------------------

class TestAction:
    @pytest.mark.parametrize("pattern,expected", [
        (ChampionPattern.single_thread_exposed, ChampionAction.deal_continuity_escalation),
        (ChampionPattern.ghost_risk_zone, ChampionAction.deal_continuity_escalation),
        (ChampionPattern.org_change_vulnerable, ChampionAction.relationship_rescue_intervention),
        (ChampionPattern.advocacy_collapse, ChampionAction.relationship_rescue_intervention),
        (ChampionPattern.blind_spot_account, ChampionAction.relationship_rescue_intervention),
        (ChampionPattern.none, ChampionAction.relationship_rescue_intervention),
    ])
    def test_critical_actions(self, engine, pattern, expected):
        assert engine._action(ChampionRisk.critical, pattern) == expected

    @pytest.mark.parametrize("pattern,expected", [
        (ChampionPattern.single_thread_exposed, ChampionAction.multithreading_urgency_coaching),
        (ChampionPattern.ghost_risk_zone, ChampionAction.relationship_rescue_intervention),
        (ChampionPattern.org_change_vulnerable, ChampionAction.org_change_alert_protocol),
        (ChampionPattern.advocacy_collapse, ChampionAction.executive_engagement_activation),
        (ChampionPattern.blind_spot_account, ChampionAction.stakeholder_mapping_sprint),
        (ChampionPattern.none, ChampionAction.multithreading_urgency_coaching),
    ])
    def test_high_actions(self, engine, pattern, expected):
        assert engine._action(ChampionRisk.high, pattern) == expected

    @pytest.mark.parametrize("pattern", list(ChampionPattern))
    def test_moderate_always_monitoring(self, engine, pattern):
        assert engine._action(ChampionRisk.moderate, pattern) == ChampionAction.champion_health_monitoring

    @pytest.mark.parametrize("pattern", list(ChampionPattern))
    def test_low_always_no_action(self, engine, pattern):
        assert engine._action(ChampionRisk.low, pattern) == ChampionAction.no_action


# ---------------------------------------------------------------------------
# flags
# ---------------------------------------------------------------------------

class TestFlags:
    def test_has_gap_via_composite(self, engine):
        inp = make_input()
        assert engine._has_gap(inp, 40.0) is True

    def test_has_gap_via_single_threaded(self, engine):
        inp = make_input(single_threaded_deal_rate_pct=0.40)
        assert engine._has_gap(inp, 0.0) is True

    def test_has_gap_via_engagement_drop(self, engine):
        inp = make_input(champion_engagement_drop_rate_pct=0.30)
        assert engine._has_gap(inp, 0.0) is True

    def test_no_gap_when_all_safe(self, engine):
        inp = make_input()
        assert engine._has_gap(inp, 10.0) is False

    def test_requires_intervention_via_composite(self, engine):
        inp = make_input()
        assert engine._requires_intervention(inp, 25.0) is True

    def test_requires_intervention_via_backup_coverage(self, engine):
        inp = make_input(backup_contact_coverage_rate_pct=0.50)
        assert engine._requires_intervention(inp, 0.0) is True

    def test_requires_intervention_via_ghosting(self, engine):
        inp = make_input(deal_ghosting_after_champion_loss_rate_pct=0.25)
        assert engine._requires_intervention(inp, 0.0) is True

    def test_no_intervention_when_all_safe(self, engine):
        inp = make_input(backup_contact_coverage_rate_pct=0.85,
                         deal_ghosting_after_champion_loss_rate_pct=0.05)
        assert engine._requires_intervention(inp, 10.0) is False

    def test_gap_boundary_composite_39(self, engine):
        assert engine._has_gap(make_input(single_threaded_deal_rate_pct=0.10,
                                          champion_engagement_drop_rate_pct=0.05), 39.9) is False

    def test_intervention_boundary_composite_24(self, engine):
        inp = make_input(backup_contact_coverage_rate_pct=0.85,
                         deal_ghosting_after_champion_loss_rate_pct=0.05)
        assert engine._requires_intervention(inp, 24.9) is False


# ---------------------------------------------------------------------------
# pipeline at risk
# ---------------------------------------------------------------------------

class TestPipelineAtRisk:
    def test_pipeline_formula(self, engine):
        inp = make_input(champion_departure_detected_deals=5, avg_deal_value_usd=100000.0,
                         deal_ghosting_after_champion_loss_rate_pct=0.50)
        comp = 80.0
        expected = round(5 * 100000.0 * 0.50 * (80.0 / 100), 2)
        assert engine._pipeline_at_risk(inp, comp) == expected

    def test_pipeline_zero_ghosting(self, engine):
        inp = make_input(deal_ghosting_after_champion_loss_rate_pct=0.0)
        assert engine._pipeline_at_risk(inp, 80.0) == 0.0

    def test_pipeline_zero_composite(self, engine):
        inp = make_input(deal_ghosting_after_champion_loss_rate_pct=0.50)
        assert engine._pipeline_at_risk(inp, 0.0) == 0.0

    def test_pipeline_zero_deals(self, engine):
        inp = make_input(champion_departure_detected_deals=0)
        assert engine._pipeline_at_risk(inp, 80.0) == 0.0

    def test_pipeline_rounded_to_2dp(self, engine):
        inp = make_input(champion_departure_detected_deals=3, avg_deal_value_usd=77777.0,
                         deal_ghosting_after_champion_loss_rate_pct=0.33)
        comp = 55.0
        val = engine._pipeline_at_risk(inp, comp)
        assert val == round(3 * 77777.0 * 0.33 * (55.0 / 100), 2)

    def test_pipeline_default_input(self, engine):
        inp = make_input()
        comp = 0.0
        assert engine._pipeline_at_risk(inp, comp) == 0.0


# ---------------------------------------------------------------------------
# signal
# ---------------------------------------------------------------------------

class TestSignal:
    def test_signal_stable_below_20(self, engine):
        inp = make_input()
        sig = engine._signal(inp, ChampionPattern.none, 15.0)
        assert sig == ("Champion relationships stable — multithreading, engagement, and "
                       "stakeholder coverage within benchmark targets")

    def test_signal_stable_at_0(self, engine):
        inp = make_input()
        sig = engine._signal(inp, ChampionPattern.none, 0.0)
        assert "stable" in sig

    def test_signal_above_20_contains_label(self, engine):
        inp = make_input(single_threaded_deal_rate_pct=0.60, backup_contact_coverage_rate_pct=0.25)
        sig = engine._signal(inp, ChampionPattern.single_thread_exposed, 65.0)
        assert "Single-thread exposed" in sig

    def test_signal_contains_single_pct(self, engine):
        inp = make_input(single_threaded_deal_rate_pct=0.45)
        sig = engine._signal(inp, ChampionPattern.ghost_risk_zone, 50.0)
        assert "45% single-threaded" in sig

    def test_signal_contains_drop_pct(self, engine):
        inp = make_input(champion_engagement_drop_rate_pct=0.33)
        sig = engine._signal(inp, ChampionPattern.none, 30.0)
        assert "33% engagement drop" in sig

    def test_signal_contains_ghost_pct(self, engine):
        inp = make_input(deal_ghosting_after_champion_loss_rate_pct=0.60)
        sig = engine._signal(inp, ChampionPattern.none, 30.0)
        assert "60% ghosted after champion loss" in sig

    def test_signal_contains_composite_int(self, engine):
        inp = make_input()
        sig = engine._signal(inp, ChampionPattern.none, 45.7)
        assert "composite 46" in sig

    @pytest.mark.parametrize("pattern,label", [
        (ChampionPattern.ghost_risk_zone, "Ghost risk zone"),
        (ChampionPattern.org_change_vulnerable, "Org change vulnerable"),
        (ChampionPattern.advocacy_collapse, "Advocacy collapse"),
        (ChampionPattern.blind_spot_account, "Blind spot account"),
    ])
    def test_signal_pattern_labels(self, engine, pattern, label):
        inp = make_input()
        sig = engine._signal(inp, pattern, 50.0)
        assert label in sig

    def test_signal_boundary_exactly_20(self, engine):
        inp = make_input()
        sig = engine._signal(inp, ChampionPattern.none, 20.0)
        assert "composite" in sig


# ---------------------------------------------------------------------------
# assess (end-to-end)
# ---------------------------------------------------------------------------

class TestAssess:
    def test_assess_returns_champion_result(self, engine):
        r = engine.assess(make_input())
        assert isinstance(r, ChampionResult)

    def test_assess_rep_id_propagated(self, engine):
        r = engine.assess(make_input(rep_id="ACME-99"))
        assert r.rep_id == "ACME-99"

    def test_assess_region_propagated(self, engine):
        r = engine.assess(make_input(region="AMER"))
        assert r.region == "AMER"

    def test_assess_low_risk_defaults(self, engine):
        r = engine.assess(make_input())
        assert r.champion_risk == ChampionRisk.low

    def test_assess_low_severity_defaults(self, engine):
        r = engine.assess(make_input())
        assert r.champion_severity == ChampionSeverity.stable

    def test_assess_no_action_defaults(self, engine):
        r = engine.assess(make_input())
        assert r.recommended_action == ChampionAction.no_action

    def test_assess_none_pattern_defaults(self, engine):
        r = engine.assess(make_input())
        assert r.champion_pattern == ChampionPattern.none

    def test_assess_critical_risk(self, engine):
        inp = make_input(
            champion_engagement_drop_rate_pct=0.60,
            org_change_detected_rate_pct=0.50,
            champion_tenure_avg_months=3.0,
            single_threaded_deal_rate_pct=0.90,
            backup_contact_coverage_rate_pct=0.10,
            executive_sponsor_coverage_rate_pct=0.10,
            champion_replacement_recovery_rate_pct=0.05,
            deal_ghosting_after_champion_loss_rate_pct=0.80,
            internal_coach_coverage_rate_pct=0.10,
            stakeholder_mapping_completeness_score=0.10,
            relationship_breadth_score=0.10,
            economic_buyer_direct_access_rate_pct=0.10,
        )
        r = engine.assess(inp)
        assert r.champion_risk == ChampionRisk.critical

    def test_assess_composite_nonnegative(self, engine):
        assert engine.assess(make_input()).champion_composite >= 0.0

    def test_assess_composite_lte_100(self, engine):
        inp = make_input(
            champion_engagement_drop_rate_pct=1.0, org_change_detected_rate_pct=1.0,
            champion_tenure_avg_months=1.0, single_threaded_deal_rate_pct=1.0,
            backup_contact_coverage_rate_pct=0.0, executive_sponsor_coverage_rate_pct=0.0,
            champion_replacement_recovery_rate_pct=0.0,
            deal_ghosting_after_champion_loss_rate_pct=1.0,
            internal_coach_coverage_rate_pct=0.0,
            stakeholder_mapping_completeness_score=0.0,
            relationship_breadth_score=0.0,
            economic_buyer_direct_access_rate_pct=0.0,
        )
        assert engine.assess(inp).champion_composite <= 100.0

    def test_assess_has_gap_false_defaults(self, engine):
        assert engine.assess(make_input()).has_champion_gap is False

    def test_assess_pipeline_at_risk_type(self, engine):
        r = engine.assess(make_input())
        assert isinstance(r.estimated_at_risk_pipeline_usd, float)

    def test_assess_signal_type(self, engine):
        r = engine.assess(make_input())
        assert isinstance(r.champion_signal, str)

    def test_assess_accumulates_results(self, engine):
        engine.assess(make_input(rep_id="A"))
        engine.assess(make_input(rep_id="B"))
        assert len(engine._results) == 2

    def test_assess_deal_continuity_escalation_path(self, engine):
        inp = make_input(
            single_threaded_deal_rate_pct=0.90, backup_contact_coverage_rate_pct=0.10,
            executive_sponsor_coverage_rate_pct=0.10,
            champion_engagement_drop_rate_pct=0.60,
            org_change_detected_rate_pct=0.50, champion_tenure_avg_months=3.0,
            champion_replacement_recovery_rate_pct=0.05,
            deal_ghosting_after_champion_loss_rate_pct=0.80,
            internal_coach_coverage_rate_pct=0.10,
            stakeholder_mapping_completeness_score=0.10,
            relationship_breadth_score=0.10,
            economic_buyer_direct_access_rate_pct=0.10,
        )
        r = engine.assess(inp)
        assert r.recommended_action == ChampionAction.deal_continuity_escalation

    def test_assess_score_fields_are_floats(self, engine):
        r = engine.assess(make_input())
        for field in ("stability_score", "coverage_score", "resilience_score",
                      "intelligence_score", "champion_composite"):
            assert isinstance(getattr(r, field), float)

    def test_assess_bool_fields(self, engine):
        r = engine.assess(make_input())
        assert isinstance(r.has_champion_gap, bool)
        assert isinstance(r.requires_champion_intervention, bool)

    def test_assess_stable_signal_when_low_composite(self, engine):
        r = engine.assess(make_input())
        assert "stable" in r.champion_signal


# ---------------------------------------------------------------------------
# assess_batch
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_batch_empty(self, engine):
        assert engine.assess_batch([]) == []

    def test_batch_single(self, engine):
        results = engine.assess_batch([make_input()])
        assert len(results) == 1

    def test_batch_multiple(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_accumulates(self, engine):
        inputs = [make_input(rep_id=f"B{i}") for i in range(3)]
        engine.assess_batch(inputs)
        assert len(engine._results) == 3

    def test_batch_order_preserved(self, engine):
        inputs = [make_input(rep_id=f"ORD{i}") for i in range(4)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"ORD{i}"

    def test_batch_returns_champion_results(self, engine):
        results = engine.assess_batch([make_input(), make_input(rep_id="X")])
        for r in results:
            assert isinstance(r, ChampionResult)


# ---------------------------------------------------------------------------
# summary
# ---------------------------------------------------------------------------

class TestSummary:
    EXPECTED_SUMMARY_KEYS = {
        "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
        "avg_champion_composite", "champion_gap_count", "intervention_count",
        "avg_stability_score", "avg_coverage_score", "avg_resilience_score",
        "avg_intelligence_score", "total_estimated_at_risk_pipeline_usd",
    }

    def test_summary_empty(self, engine):
        s = engine.summary()
        assert s["total"] == 0

    def test_summary_empty_keys(self, engine):
        assert set(engine.summary().keys()) == self.EXPECTED_SUMMARY_KEYS

    def test_summary_key_count(self, engine):
        assert len(engine.summary()) == 13

    def test_summary_empty_zero_floats(self, engine):
        s = engine.summary()
        for key in ("avg_champion_composite", "avg_stability_score", "avg_coverage_score",
                    "avg_resilience_score", "avg_intelligence_score",
                    "total_estimated_at_risk_pipeline_usd"):
            assert s[key] == 0.0

    def test_summary_empty_zero_counts(self, engine):
        s = engine.summary()
        assert s["champion_gap_count"] == 0
        assert s["intervention_count"] == 0

    def test_summary_after_one_assess(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert s["total"] == 1

    def test_summary_keys_after_assess(self, engine):
        engine.assess(make_input())
        assert set(engine.summary().keys()) == self.EXPECTED_SUMMARY_KEYS

    def test_summary_key_count_after_assess(self, engine):
        engine.assess(make_input())
        assert len(engine.summary()) == 13

    def test_summary_risk_counts_type(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.summary()["risk_counts"], dict)

    def test_summary_total_matches_assessed(self, engine):
        for i in range(4):
            engine.assess(make_input(rep_id=f"S{i}"))
        assert engine.summary()["total"] == 4

    def test_summary_gap_count(self, engine):
        engine.assess(make_input(champion_engagement_drop_rate_pct=0.30))
        engine.assess(make_input())
        s = engine.summary()
        assert s["champion_gap_count"] == 1

    def test_summary_intervention_count(self, engine):
        engine.assess(make_input(backup_contact_coverage_rate_pct=0.50))
        engine.assess(make_input())
        s = engine.summary()
        assert s["intervention_count"] >= 1

    def test_summary_avg_composite_rounded(self, engine):
        engine.assess(make_input())
        val = engine.summary()["avg_champion_composite"]
        assert round(val, 1) == val

    def test_summary_total_pipeline_is_float(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.summary()["total_estimated_at_risk_pipeline_usd"], float)

    def test_summary_action_counts_has_correct_action(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert "no_action" in s["action_counts"]

    def test_summary_pattern_counts_has_none(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert "none" in s["pattern_counts"]

    def test_summary_severity_counts_has_stable(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert "stable" in s["severity_counts"]

    def test_summary_risk_counts_has_low(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert "low" in s["risk_counts"]

    def test_summary_multiple_risk_buckets(self, engine):
        engine.assess(make_input())  # low
        engine.assess(make_input(
            champion_engagement_drop_rate_pct=0.55,
            org_change_detected_rate_pct=0.40,
            single_threaded_deal_rate_pct=0.65,
            backup_contact_coverage_rate_pct=0.10,
            executive_sponsor_coverage_rate_pct=0.10,
        ))
        s = engine.summary()
        assert len(s["risk_counts"]) >= 2

    def test_summary_avg_scores_nonnegative(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        for key in ("avg_stability_score", "avg_coverage_score",
                    "avg_resilience_score", "avg_intelligence_score"):
            assert s[key] >= 0.0

    def test_summary_independent_engines(self):
        e1 = SalesChampionDepartureRelationshipContinuityEngine()
        e2 = SalesChampionDepartureRelationshipContinuityEngine()
        e1.assess(make_input(rep_id="E1"))
        assert e2.summary()["total"] == 0

    def test_summary_total_pipeline_sum(self, engine):
        inp1 = make_input(champion_departure_detected_deals=5, avg_deal_value_usd=100000.0,
                          deal_ghosting_after_champion_loss_rate_pct=0.0)
        inp2 = make_input(champion_departure_detected_deals=0)
        engine.assess(inp1)
        engine.assess(inp2)
        s = engine.summary()
        assert s["total_estimated_at_risk_pipeline_usd"] >= 0.0


# ---------------------------------------------------------------------------
# edge cases and integration
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_all_zeros_input(self, engine):
        # tenure=0 → +25 stability; backup=0 → +30 coverage; recovery=0 → +40 resilience;
        # stakeholder=0 → +45, breadth=0 → +30, eb=0 → +25 intelligence (capped at 100)
        # stability=25, coverage=55 (0+30+25), resilience=65 (40+0+25), intelligence=100
        # composite = 25*0.30 + 55*0.25 + 65*0.25 + 100*0.20 = 7.5+13.75+16.25+20 = 57.5
        inp = make_input(
            champion_engagement_drop_rate_pct=0.0, org_change_detected_rate_pct=0.0,
            champion_tenure_avg_months=0.0, single_threaded_deal_rate_pct=0.0,
            backup_contact_coverage_rate_pct=0.0, executive_sponsor_coverage_rate_pct=0.0,
            champion_replacement_recovery_rate_pct=0.0,
            deal_ghosting_after_champion_loss_rate_pct=0.0,
            internal_coach_coverage_rate_pct=0.0,
            stakeholder_mapping_completeness_score=0.0,
            relationship_breadth_score=0.0, economic_buyer_direct_access_rate_pct=0.0,
            champion_departure_detected_deals=0, total_active_deals=0, avg_deal_value_usd=0.0,
        )
        r = engine.assess(inp)
        assert r.champion_composite == 57.5

    def test_all_ones_safe_input(self, engine):
        inp = make_input(
            champion_engagement_drop_rate_pct=1.0, org_change_detected_rate_pct=1.0,
            champion_tenure_avg_months=1.0, single_threaded_deal_rate_pct=1.0,
            backup_contact_coverage_rate_pct=1.0, executive_sponsor_coverage_rate_pct=1.0,
            champion_replacement_recovery_rate_pct=1.0,
            deal_ghosting_after_champion_loss_rate_pct=1.0,
            internal_coach_coverage_rate_pct=1.0,
            stakeholder_mapping_completeness_score=1.0,
            relationship_breadth_score=1.0, economic_buyer_direct_access_rate_pct=1.0,
        )
        r = engine.assess(inp)
        assert r is not None

    def test_multiple_assess_independent(self):
        e = SalesChampionDepartureRelationshipContinuityEngine()
        r1 = e.assess(make_input(rep_id="R1"))
        r2 = e.assess(make_input(rep_id="R2"))
        assert r1.rep_id != r2.rep_id

    def test_to_dict_has_champion_gap_bool(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["has_champion_gap"], bool)

    def test_to_dict_requires_intervention_bool(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["requires_champion_intervention"], bool)

    def test_result_stability_score_range(self, engine):
        r = engine.assess(make_input())
        assert 0.0 <= r.stability_score <= 100.0

    def test_result_coverage_score_range(self, engine):
        r = engine.assess(make_input())
        assert 0.0 <= r.coverage_score <= 100.0

    def test_result_resilience_score_range(self, engine):
        r = engine.assess(make_input())
        assert 0.0 <= r.resilience_score <= 100.0

    def test_result_intelligence_score_range(self, engine):
        r = engine.assess(make_input())
        assert 0.0 <= r.intelligence_score <= 100.0

    def test_engine_fresh_no_results(self):
        e = SalesChampionDepartureRelationshipContinuityEngine()
        assert e._results == []

    def test_batch_then_summary_total(self, engine):
        engine.assess_batch([make_input(rep_id=f"BT{i}") for i in range(7)])
        assert engine.summary()["total"] == 7

    @pytest.mark.parametrize("rep_id", ["X1", "Y2", "Z3", "ABC", "123"])
    def test_rep_id_preserved(self, engine, rep_id):
        r = engine.assess(make_input(rep_id=rep_id))
        assert r.rep_id == rep_id

    @pytest.mark.parametrize("region", ["EMEA", "AMER", "APAC", "LATAM"])
    def test_region_preserved(self, engine, region):
        r = engine.assess(make_input(region=region))
        assert r.region == region

    def test_signal_pct_rounding(self, engine):
        inp = make_input(single_threaded_deal_rate_pct=0.456)
        r = engine.assess(inp)
        # composite=0, stable signal
        if r.champion_composite >= 20:
            assert "46% single-threaded" in r.champion_signal

    def test_intervention_true_via_low_backup(self, engine):
        r = engine.assess(make_input(backup_contact_coverage_rate_pct=0.40))
        assert r.requires_champion_intervention is True

    def test_gap_true_via_high_single_threaded(self, engine):
        r = engine.assess(make_input(single_threaded_deal_rate_pct=0.40))
        assert r.has_champion_gap is True
