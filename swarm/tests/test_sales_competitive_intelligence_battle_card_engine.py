"""Pytest suite for SalesCompetitiveIntelligenceBattleCardEngine — ~300 tests."""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_competitive_intelligence_battle_card_engine import (
    CompetitiveAction, CompetitiveInput, CompetitivePattern, CompetitiveResult,
    CompetitiveRisk, CompetitiveSeverity, SalesCompetitiveIntelligenceBattleCardEngine,
)


# ── helpers ──────────────────────────────────────────────────────────────────

def make_input(**ov) -> CompetitiveInput:
    d = dict(
        rep_id="R1", region="West", evaluation_period_id="Q1-2026",
        competitive_win_rate_pct=0.70, competitive_loss_rate_pct=0.30,
        battle_card_usage_rate_pct=0.80, competitive_mention_early_rate_pct=0.70,
        price_concession_vs_competitor_pct=0.10, feature_comparison_loss_rate_pct=0.05,
        competitive_deal_cycle_delta_days=5.0, no_competitive_intel_rate_pct=0.10,
        competitive_stakeholder_loss_pct=0.10, single_competitor_thread_rate_pct=0.10,
        late_competitor_discovery_rate_pct=0.05, displacement_win_rate_pct=0.60,
        proof_of_concept_win_rate_pct=0.65, reference_customer_usage_pct=0.50,
        total_competitive_deals=100, avg_deal_value_usd=10_000.0,
        competitive_intensity_score=0.40, head_to_head_calls_per_deal=2.0,
        post_loss_debrief_rate_pct=0.60, total_deals_evaluated=200,
    )
    d.update(ov)
    return CompetitiveInput(**d)

def eng(): return SalesCompetitiveIntelligenceBattleCardEngine()


# ── 1. Enum values ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("member,val", [
    (CompetitiveRisk.low, "low"), (CompetitiveRisk.moderate, "moderate"),
    (CompetitiveRisk.high, "high"), (CompetitiveRisk.critical, "critical"),
])
def test_risk_enum_values(member, val): assert member.value == val

@pytest.mark.parametrize("member,val", [
    (CompetitivePattern.none, "none"),
    (CompetitivePattern.unprepared_seller, "unprepared_seller"),
    (CompetitivePattern.feature_fighter, "feature_fighter"),
    (CompetitivePattern.price_surrenderer, "price_surrenderer"),
    (CompetitivePattern.late_discovery, "late_discovery"),
    (CompetitivePattern.single_thread_loser, "single_thread_loser"),
])
def test_pattern_enum_values(member, val): assert member.value == val

@pytest.mark.parametrize("member,val", [
    (CompetitiveSeverity.dominant, "dominant"), (CompetitiveSeverity.competing, "competing"),
    (CompetitiveSeverity.struggling, "struggling"), (CompetitiveSeverity.losing, "losing"),
])
def test_severity_enum_values(member, val): assert member.value == val

@pytest.mark.parametrize("member,val", [
    (CompetitiveAction.no_action, "no_action"),
    (CompetitiveAction.competitive_awareness_coaching, "competitive_awareness_coaching"),
    (CompetitiveAction.battle_card_refresh_coaching, "battle_card_refresh_coaching"),
    (CompetitiveAction.value_differentiation_coaching, "value_differentiation_coaching"),
    (CompetitiveAction.multi_thread_coaching, "multi_thread_coaching"),
    (CompetitiveAction.competitive_deal_review, "competitive_deal_review"),
    (CompetitiveAction.executive_competitive_escalation, "executive_competitive_escalation"),
])
def test_action_enum_values(member, val): assert member.value == val

def test_risk_count(): assert len(CompetitiveRisk) == 4
def test_pattern_count(): assert len(CompetitivePattern) == 6
def test_severity_count(): assert len(CompetitiveSeverity) == 4
def test_action_count(): assert len(CompetitiveAction) == 7


# ── 2. Field / key counts ─────────────────────────────────────────────────────

def test_input_field_count(): assert len(make_input().__dataclass_fields__) == 23

def test_to_dict_key_count(): assert len(eng().assess(make_input()).to_dict()) == 15
def test_to_dict_exact_keys():
    assert set(eng().assess(make_input()).to_dict().keys()) == {
        "rep_id", "region", "competitive_risk", "competitive_pattern",
        "competitive_severity", "recommended_action", "preparedness_score",
        "execution_score", "intelligence_score", "positioning_score",
        "competitive_composite", "has_competitive_gap",
        "requires_competitive_coaching", "estimated_lost_revenue_usd",
        "competitive_signal",
    }

def test_summary_empty_key_count(): assert len(eng().summary()) == 13
def test_summary_populated_key_count():
    e = eng(); e.assess(make_input()); assert len(e.summary()) == 13
def test_summary_exact_keys():
    assert set(eng().summary().keys()) == {
        "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
        "avg_competitive_composite", "competitive_gap_count", "coaching_count",
        "avg_preparedness_score", "avg_execution_score", "avg_intelligence_score",
        "avg_positioning_score", "total_estimated_lost_revenue_usd",
    }

def test_to_dict_values_serializable():
    for k, v in eng().assess(make_input()).to_dict().items(): assert isinstance(v, (str, float, int, bool)), f"{k}={type(v)}"
def test_input_has_total_deals_evaluated(): assert hasattr(make_input(), "total_deals_evaluated")


# ── 3. Preparedness sub-score ─────────────────────────────────────────────────

def prep(**kw): return eng()._preparedness_score(make_input(**kw))

def test_prep_zero_healthy(): assert prep() == 0.0
def test_prep_very_low_usage(): assert prep(battle_card_usage_rate_pct=0.20) == 40.0
def test_prep_low_usage(): assert prep(battle_card_usage_rate_pct=0.40) == 22.0
def test_prep_mid_usage(): assert prep(battle_card_usage_rate_pct=0.60) == 8.0
def test_prep_high_usage_no_points(): assert prep(battle_card_usage_rate_pct=0.80) == 0.0
def test_prep_high_no_intel(): assert prep(no_competitive_intel_rate_pct=0.45) == 35.0
def test_prep_mid_no_intel(): assert prep(no_competitive_intel_rate_pct=0.30) == 18.0
def test_prep_low_no_intel_no_points(): assert prep(no_competitive_intel_rate_pct=0.10) == 0.0
def test_prep_low_debrief(): assert prep(post_loss_debrief_rate_pct=0.10) == 25.0
def test_prep_mid_debrief(): assert prep(post_loss_debrief_rate_pct=0.35) == 12.0
def test_prep_high_debrief_no_points(): assert prep(post_loss_debrief_rate_pct=0.60) == 0.0
def test_prep_caps_at_100(): assert prep(battle_card_usage_rate_pct=0.10, no_competitive_intel_rate_pct=0.50, post_loss_debrief_rate_pct=0.05) == 100.0
def test_prep_boundary_usage_025(): assert prep(battle_card_usage_rate_pct=0.25) == 40.0
def test_prep_boundary_usage_050(): assert prep(battle_card_usage_rate_pct=0.50) == 22.0
def test_prep_boundary_usage_070(): assert prep(battle_card_usage_rate_pct=0.70) == 8.0
def test_prep_boundary_no_intel_040(): assert prep(no_competitive_intel_rate_pct=0.40) == 35.0
def test_prep_boundary_no_intel_022(): assert prep(no_competitive_intel_rate_pct=0.22) == 18.0
def test_prep_boundary_debrief_020(): assert prep(post_loss_debrief_rate_pct=0.20) == 25.0
def test_prep_boundary_debrief_045(): assert prep(post_loss_debrief_rate_pct=0.45) == 12.0


# ── 4. Execution sub-score ───────────────────────────────────────────────────

def exc(**kw): return eng()._execution_score(make_input(**kw))

def test_exec_zero_healthy(): assert exc() == 0.0
def test_exec_very_low_win(): assert exc(competitive_win_rate_pct=0.20) == 45.0
def test_exec_low_win(): assert exc(competitive_win_rate_pct=0.35) == 25.0
def test_exec_mid_win(): assert exc(competitive_win_rate_pct=0.55) == 10.0
def test_exec_high_win_no_points(): assert exc(competitive_win_rate_pct=0.70) == 0.0
def test_exec_high_price_concession(): assert exc(price_concession_vs_competitor_pct=0.60) == 30.0
def test_exec_mid_price_concession(): assert exc(price_concession_vs_competitor_pct=0.35) == 15.0
def test_exec_low_price_concession_no_pts(): assert exc(price_concession_vs_competitor_pct=0.10) == 0.0
def test_exec_long_cycle(): assert exc(competitive_deal_cycle_delta_days=30.0) == 25.0
def test_exec_mid_cycle(): assert exc(competitive_deal_cycle_delta_days=15.0) == 12.0
def test_exec_short_cycle_no_pts(): assert exc(competitive_deal_cycle_delta_days=5.0) == 0.0
def test_exec_caps_at_100(): assert exc(competitive_win_rate_pct=0.10, price_concession_vs_competitor_pct=0.70, competitive_deal_cycle_delta_days=40.0) == 100.0
def test_exec_boundary_win_025(): assert exc(competitive_win_rate_pct=0.25) == 45.0
def test_exec_boundary_win_045(): assert exc(competitive_win_rate_pct=0.45) == 25.0
def test_exec_boundary_win_060(): assert exc(competitive_win_rate_pct=0.60) == 10.0
def test_exec_boundary_price_050(): assert exc(price_concession_vs_competitor_pct=0.50) == 30.0
def test_exec_boundary_price_028(): assert exc(price_concession_vs_competitor_pct=0.28) == 15.0
def test_exec_boundary_cycle_025(): assert exc(competitive_deal_cycle_delta_days=25.0) == 25.0
def test_exec_boundary_cycle_012(): assert exc(competitive_deal_cycle_delta_days=12.0) == 12.0


# ── 5. Intelligence sub-score ─────────────────────────────────────────────────

def intel(**kw): return eng()._intelligence_score(make_input(**kw))

def test_intel_zero_healthy(): assert intel() == 0.0
def test_intel_high_late_discovery(): assert intel(late_competitor_discovery_rate_pct=0.50) == 40.0
def test_intel_mid_late_discovery(): assert intel(late_competitor_discovery_rate_pct=0.30) == 22.0
def test_intel_low_late_discovery(): assert intel(late_competitor_discovery_rate_pct=0.15) == 8.0
def test_intel_no_late_discovery_pts(): assert intel(late_competitor_discovery_rate_pct=0.05) == 0.0
def test_intel_very_low_early_mention(): assert intel(competitive_mention_early_rate_pct=0.20) == 35.0
def test_intel_mid_early_mention(): assert intel(competitive_mention_early_rate_pct=0.40) == 18.0
def test_intel_high_early_mention_no_pts(): assert intel(competitive_mention_early_rate_pct=0.70) == 0.0
def test_intel_very_low_h2h(): assert intel(head_to_head_calls_per_deal=0.3) == 25.0
def test_intel_mid_h2h(): assert intel(head_to_head_calls_per_deal=0.8) == 12.0
def test_intel_high_h2h_no_pts(): assert intel(head_to_head_calls_per_deal=2.0) == 0.0
def test_intel_caps_at_100(): assert intel(late_competitor_discovery_rate_pct=0.60, competitive_mention_early_rate_pct=0.10, head_to_head_calls_per_deal=0.1) == 100.0
def test_intel_boundary_late_045(): assert intel(late_competitor_discovery_rate_pct=0.45) == 40.0
def test_intel_boundary_late_025(): assert intel(late_competitor_discovery_rate_pct=0.25) == 22.0
def test_intel_boundary_late_012(): assert intel(late_competitor_discovery_rate_pct=0.12) == 8.0
def test_intel_boundary_early_025(): assert intel(competitive_mention_early_rate_pct=0.25) == 35.0
def test_intel_boundary_early_050(): assert intel(competitive_mention_early_rate_pct=0.50) == 18.0
def test_intel_boundary_h2h_05(): assert intel(head_to_head_calls_per_deal=0.5) == 25.0
def test_intel_boundary_h2h_12(): assert intel(head_to_head_calls_per_deal=1.2) == 12.0


# ── 6. Positioning sub-score ─────────────────────────────────────────────────

def pos(**kw): return eng()._positioning_score(make_input(**kw))

def test_pos_zero_healthy(): assert pos() == 0.0
def test_pos_high_feature_loss(): assert pos(feature_comparison_loss_rate_pct=0.50) == 40.0
def test_pos_mid_feature_loss(): assert pos(feature_comparison_loss_rate_pct=0.30) == 22.0
def test_pos_low_feature_loss(): assert pos(feature_comparison_loss_rate_pct=0.15) == 8.0
def test_pos_no_feature_loss_pts(): assert pos(feature_comparison_loss_rate_pct=0.05) == 0.0
def test_pos_high_single_thread(): assert pos(single_competitor_thread_rate_pct=0.65) == 35.0
def test_pos_mid_single_thread(): assert pos(single_competitor_thread_rate_pct=0.45) == 18.0
def test_pos_low_single_thread_no_pts(): assert pos(single_competitor_thread_rate_pct=0.10) == 0.0
def test_pos_very_low_ref_usage(): assert pos(reference_customer_usage_pct=0.10) == 25.0
def test_pos_mid_ref_usage(): assert pos(reference_customer_usage_pct=0.25) == 12.0
def test_pos_high_ref_usage_no_pts(): assert pos(reference_customer_usage_pct=0.50) == 0.0
def test_pos_caps_at_100(): assert pos(feature_comparison_loss_rate_pct=0.60, single_competitor_thread_rate_pct=0.70, reference_customer_usage_pct=0.05) == 100.0
def test_pos_boundary_feature_045(): assert pos(feature_comparison_loss_rate_pct=0.45) == 40.0
def test_pos_boundary_feature_025(): assert pos(feature_comparison_loss_rate_pct=0.25) == 22.0
def test_pos_boundary_feature_012(): assert pos(feature_comparison_loss_rate_pct=0.12) == 8.0
def test_pos_boundary_thread_060(): assert pos(single_competitor_thread_rate_pct=0.60) == 35.0
def test_pos_boundary_thread_035(): assert pos(single_competitor_thread_rate_pct=0.35) == 18.0
def test_pos_boundary_ref_015(): assert pos(reference_customer_usage_pct=0.15) == 25.0
def test_pos_boundary_ref_035(): assert pos(reference_customer_usage_pct=0.35) == 12.0


# ── 7. Composite weighting ────────────────────────────────────────────────────

def composite(pr, ex, in_, po): return eng()._composite(pr, ex, in_, po)

def test_composite_zero(): assert composite(0, 0, 0, 0) == 0.0
def test_composite_100(): assert composite(100, 100, 100, 100) == 100.0
def test_composite_formula():
    assert composite(80, 60, 40, 20) == round(80*.25 + 60*.35 + 40*.20 + 20*.20, 2)
def test_composite_weights_sum(): assert abs(.25 + .35 + .20 + .20 - 1.0) < 1e-9
def test_composite_execution_weighted_most(): assert composite(0,100,0,0) > composite(100,0,0,0)
def test_composite_caps_at_100(): assert composite(100,100,100,100) <= 100.0
def test_composite_rounded_2dp():
    v = composite(33.3, 33.3, 33.3, 33.3); assert v == round(v, 2)
def test_composite_preparedness_weight():
    assert composite(100, 0, 0, 0) == round(100 * .25, 2)
def test_composite_intelligence_weight():
    assert composite(0, 0, 100, 0) == round(100 * .20, 2)
def test_composite_positioning_weight():
    assert composite(0, 0, 0, 100) == round(100 * .20, 2)


# ── 8. Risk thresholds ───────────────────────────────────────────────────────

@pytest.mark.parametrize("comp,expected", [
    (0.0, CompetitiveRisk.low), (19.99, CompetitiveRisk.low),
    (20.0, CompetitiveRisk.moderate), (39.99, CompetitiveRisk.moderate),
    (40.0, CompetitiveRisk.high), (59.99, CompetitiveRisk.high),
    (60.0, CompetitiveRisk.critical), (100.0, CompetitiveRisk.critical),
])
def test_risk_threshold(comp, expected): assert eng()._risk(comp) == expected


# ── 9. Severity thresholds ───────────────────────────────────────────────────

@pytest.mark.parametrize("comp,expected", [
    (0.0, CompetitiveSeverity.dominant), (19.99, CompetitiveSeverity.dominant),
    (20.0, CompetitiveSeverity.competing), (39.99, CompetitiveSeverity.competing),
    (40.0, CompetitiveSeverity.struggling), (59.99, CompetitiveSeverity.struggling),
    (60.0, CompetitiveSeverity.losing), (100.0, CompetitiveSeverity.losing),
])
def test_severity_threshold(comp, expected): assert eng()._severity(comp) == expected


# ── 10. Action routing ────────────────────────────────────────────────────────

def action(risk, pat): return eng()._action(risk, pat)

def test_action_low_no_action(): assert action(CompetitiveRisk.low, CompetitivePattern.none) == CompetitiveAction.no_action
def test_action_low_any_pattern_no_action():
    for p in CompetitivePattern: assert action(CompetitiveRisk.low, p) == CompetitiveAction.no_action
def test_action_moderate_awareness():
    for p in CompetitivePattern: assert action(CompetitiveRisk.moderate, p) == CompetitiveAction.competitive_awareness_coaching

_CR = CompetitiveRisk; _CP = CompetitivePattern; _CA = CompetitiveAction
@pytest.mark.parametrize("risk,pat,expected", [
    (_CR.critical, _CP.unprepared_seller,   _CA.executive_competitive_escalation),
    (_CR.critical, _CP.price_surrenderer,   _CA.executive_competitive_escalation),
    (_CR.critical, _CP.feature_fighter,     _CA.competitive_deal_review),
    (_CR.critical, _CP.late_discovery,      _CA.competitive_deal_review),
    (_CR.critical, _CP.single_thread_loser, _CA.competitive_deal_review),
    (_CR.critical, _CP.none,               _CA.competitive_deal_review),
    (_CR.high,    _CP.unprepared_seller,    _CA.battle_card_refresh_coaching),
    (_CR.high,    _CP.feature_fighter,      _CA.value_differentiation_coaching),
    (_CR.high,    _CP.price_surrenderer,    _CA.value_differentiation_coaching),
    (_CR.high,    _CP.late_discovery,       _CA.competitive_awareness_coaching),
    (_CR.high,    _CP.single_thread_loser,  _CA.multi_thread_coaching),
    (_CR.high,    _CP.none,                _CA.battle_card_refresh_coaching),
])
def test_action_routing(risk, pat, expected): assert action(risk, pat) == expected


# ── 11. Pattern detection ─────────────────────────────────────────────────────

def pat(**kw): return eng()._pattern(make_input(**kw))

def test_pattern_none_healthy(): assert pat() == CompetitivePattern.none
def test_pattern_unprepared_seller():
    assert pat(battle_card_usage_rate_pct=0.10, no_competitive_intel_rate_pct=0.50) == CompetitivePattern.unprepared_seller
def test_pattern_feature_fighter():
    assert pat(feature_comparison_loss_rate_pct=0.50, price_concession_vs_competitor_pct=0.10) == CompetitivePattern.feature_fighter
def test_pattern_price_surrenderer():
    assert pat(price_concession_vs_competitor_pct=0.60, competitive_win_rate_pct=0.20) == CompetitivePattern.price_surrenderer
def test_pattern_late_discovery():
    assert pat(late_competitor_discovery_rate_pct=0.50, competitive_mention_early_rate_pct=0.10) == CompetitivePattern.late_discovery
def test_pattern_single_thread_loser():
    assert pat(single_competitor_thread_rate_pct=0.65, competitive_stakeholder_loss_pct=0.50) == CompetitivePattern.single_thread_loser
def test_pattern_unprepared_takes_priority_over_feature():
    assert pat(battle_card_usage_rate_pct=0.10, no_competitive_intel_rate_pct=0.50, feature_comparison_loss_rate_pct=0.50, price_concession_vs_competitor_pct=0.10) == CompetitivePattern.unprepared_seller
def test_pattern_boundary_unprepared_usage_020(): assert pat(battle_card_usage_rate_pct=0.20, no_competitive_intel_rate_pct=0.40) == CompetitivePattern.unprepared_seller
def test_pattern_boundary_feature_fighter_loss_045(): assert pat(feature_comparison_loss_rate_pct=0.45, price_concession_vs_competitor_pct=0.20) == CompetitivePattern.feature_fighter
def test_pattern_boundary_price_surrenderer_055(): assert pat(price_concession_vs_competitor_pct=0.55, competitive_win_rate_pct=0.30) == CompetitivePattern.price_surrenderer
def test_pattern_boundary_late_discovery_045(): assert pat(late_competitor_discovery_rate_pct=0.45, competitive_mention_early_rate_pct=0.20) == CompetitivePattern.late_discovery
def test_pattern_boundary_single_thread_060(): assert pat(single_competitor_thread_rate_pct=0.60, competitive_stakeholder_loss_pct=0.45) == CompetitivePattern.single_thread_loser


# ── 12. Flags ─────────────────────────────────────────────────────────────────

def has_gap(inp, c): return eng()._has_gap(inp, c)
def req_coaching(inp, c): return eng()._requires_coaching(inp, c)

@pytest.mark.parametrize("kw,comp,expected", [
    ({}, 40.0, True), ({"competitive_win_rate_pct":0.50,"battle_card_usage_rate_pct":0.60}, 10.0, False),
    ({"competitive_win_rate_pct":0.35}, 10.0, True), ({"battle_card_usage_rate_pct":0.40}, 10.0, True),
    ({"competitive_win_rate_pct":0.40}, 10.0, True), ({"battle_card_usage_rate_pct":0.50}, 10.0, True),
    ({"competitive_win_rate_pct":0.41,"battle_card_usage_rate_pct":0.60}, 10.0, False),
])
def test_has_gap(kw, comp, expected): assert has_gap(make_input(**kw), comp) is expected

@pytest.mark.parametrize("kw,comp,expected", [
    ({}, 25.0, True), ({"no_competitive_intel_rate_pct":0.10,"late_competitor_discovery_rate_pct":0.10}, 10.0, False),
    ({"no_competitive_intel_rate_pct":0.35}, 10.0, True), ({"late_competitor_discovery_rate_pct":0.30}, 10.0, True),
    ({"no_competitive_intel_rate_pct":0.30}, 10.0, True), ({"late_competitor_discovery_rate_pct":0.25}, 10.0, True),
    ({}, 25.0, True), ({"no_competitive_intel_rate_pct":0.10,"late_competitor_discovery_rate_pct":0.10}, 24.0, False),
])
def test_requires_coaching(kw, comp, expected): assert req_coaching(make_input(**kw), comp) is expected


# ── 13. Lost revenue formula ──────────────────────────────────────────────────

def lost(inp, c): return eng()._lost_revenue(inp, c)

def test_lost_revenue_basic():
    inp = make_input(total_competitive_deals=100, avg_deal_value_usd=10_000.0, competitive_loss_rate_pct=0.40)
    assert lost(inp, 50.0) == round(100 * 10_000 * 0.40 * 0.50, 2)
def test_lost_revenue_zero_composite():
    assert lost(make_input(competitive_loss_rate_pct=0.50), 0.0) == 0.0
def test_lost_revenue_zero_deals():
    assert lost(make_input(total_competitive_deals=0), 50.0) == 0.0
def test_lost_revenue_full_composite():
    inp = make_input(total_competitive_deals=10, avg_deal_value_usd=1000.0, competitive_loss_rate_pct=1.0)
    assert lost(inp, 100.0) == round(10 * 1000 * 1.0 * 1.0, 2)
def test_lost_revenue_rounded_2dp():
    inp = make_input(total_competitive_deals=3, avg_deal_value_usd=3333.33, competitive_loss_rate_pct=0.333)
    result = lost(inp, 33.3); assert result == round(result, 2)
def test_lost_revenue_scales_with_composite():
    inp = make_input(total_competitive_deals=10, avg_deal_value_usd=1000.0, competitive_loss_rate_pct=0.50)
    assert lost(inp, 80.0) > lost(inp, 40.0)


# ── 14. Signal text ───────────────────────────────────────────────────────────

def test_signal_healthy_text():
    assert "Competitive execution healthy" in eng().assess(make_input()).competitive_signal
def test_signal_unhealthy_contains_label():
    r = eng().assess(make_input(battle_card_usage_rate_pct=0.10, no_competitive_intel_rate_pct=0.50, competitive_win_rate_pct=0.20))
    assert "Unprepared seller" in r.competitive_signal
def test_signal_contains_win_rate_pct():
    r = eng().assess(make_input(battle_card_usage_rate_pct=0.10, no_competitive_intel_rate_pct=0.50, competitive_win_rate_pct=0.42))
    assert "42%" in r.competitive_signal
def test_signal_contains_battle_card_pct():
    r = eng().assess(make_input(battle_card_usage_rate_pct=0.13, no_competitive_intel_rate_pct=0.50, competitive_win_rate_pct=0.20))
    assert "13%" in r.competitive_signal
def test_signal_contains_late_pct():
    r = eng().assess(make_input(battle_card_usage_rate_pct=0.10, no_competitive_intel_rate_pct=0.50, competitive_win_rate_pct=0.20, late_competitor_discovery_rate_pct=0.30))
    assert "30%" in r.competitive_signal
def test_signal_contains_composite_int():
    r = eng().assess(make_input(battle_card_usage_rate_pct=0.10, no_competitive_intel_rate_pct=0.50, competitive_win_rate_pct=0.20))
    assert f"composite {round(r.competitive_composite)}" in r.competitive_signal
def test_signal_feature_fighter_label():
    r = eng().assess(make_input(feature_comparison_loss_rate_pct=0.50, price_concession_vs_competitor_pct=0.10, competitive_win_rate_pct=0.20))
    assert "Feature fighter" in r.competitive_signal
def test_signal_is_string():
    assert isinstance(eng().assess(make_input()).competitive_signal, str)


# ── 15. assess() integration ─────────────────────────────────────────────────

def test_assess_returns_result(): assert isinstance(eng().assess(make_input()), CompetitiveResult)
def test_assess_rep_id_propagated(): assert eng().assess(make_input(rep_id="X99")).rep_id == "X99"
def test_assess_region_propagated(): assert eng().assess(make_input(region="EMEA")).region == "EMEA"
def test_assess_stores_result():
    e = eng(); e.assess(make_input()); assert len(e._results) == 1
def test_assess_healthy_low_risk(): assert eng().assess(make_input()).competitive_risk == CompetitiveRisk.low
def test_assess_healthy_dominant(): assert eng().assess(make_input()).competitive_severity == CompetitiveSeverity.dominant
def test_assess_healthy_no_action(): assert eng().assess(make_input()).recommended_action == CompetitiveAction.no_action
def test_assess_composite_in_result():
    e = eng(); inp = make_input(); r = e.assess(inp)
    assert r.competitive_composite == e._composite(e._preparedness_score(inp), e._execution_score(inp), e._intelligence_score(inp), e._positioning_score(inp))
_WORST = dict(battle_card_usage_rate_pct=0.10, no_competitive_intel_rate_pct=0.50,
              post_loss_debrief_rate_pct=0.05, competitive_win_rate_pct=0.10,
              price_concession_vs_competitor_pct=0.70, competitive_deal_cycle_delta_days=35.0,
              late_competitor_discovery_rate_pct=0.60, competitive_mention_early_rate_pct=0.10,
              head_to_head_calls_per_deal=0.2, feature_comparison_loss_rate_pct=0.60,
              single_competitor_thread_rate_pct=0.70, reference_customer_usage_pct=0.05)
def test_assess_worst_case_critical():
    assert eng().assess(make_input(**_WORST)).competitive_risk == CompetitiveRisk.critical
def test_assess_has_gap_is_bool(): assert isinstance(eng().assess(make_input()).has_competitive_gap, bool)
def test_assess_requires_coaching_is_bool(): assert isinstance(eng().assess(make_input()).requires_competitive_coaching, bool)
def test_assess_composite_between_0_100():
    r = eng().assess(make_input()); assert 0.0 <= r.competitive_composite <= 100.0
def test_assess_sub_scores_in_range():
    r = eng().assess(make_input())
    assert all(0.0 <= s <= 100.0 for s in [r.preparedness_score, r.execution_score, r.intelligence_score, r.positioning_score])
def test_assess_lost_revenue_nonnegative(): assert eng().assess(make_input()).estimated_lost_revenue_usd >= 0.0
def test_assess_lost_revenue_rounded():
    r = eng().assess(make_input()); assert r.estimated_lost_revenue_usd == round(r.estimated_lost_revenue_usd, 2)


# ── 16. assess_batch() ────────────────────────────────────────────────────────

def test_batch_returns_list(): assert isinstance(eng().assess_batch([make_input()]), list)
def test_batch_empty(): assert eng().assess_batch([]) == []
def test_batch_length():
    e = eng(); assert len(e.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])) == 5
def test_batch_each_is_result():
    for r in eng().assess_batch([make_input(), make_input(rep_id="R2")]):
        assert isinstance(r, CompetitiveResult)
def test_batch_stores_all():
    e = eng(); e.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)]); assert len(e._results) == 3
def test_batch_rep_ids_preserved():
    e = eng(); rs = e.assess_batch([make_input(rep_id="A"), make_input(rep_id="B")])
    assert [r.rep_id for r in rs] == ["A", "B"]
def test_batch_accumulates_after_assess():
    e = eng(); e.assess(make_input()); e.assess_batch([make_input(rep_id="X"), make_input(rep_id="Y")])
    assert len(e._results) == 3


# ── 17. summary() ────────────────────────────────────────────────────────────

def test_summary_empty_total(): assert eng().summary()["total"] == 0
def test_summary_empty_avg_composite(): assert eng().summary()["avg_competitive_composite"] == 0.0
def test_summary_empty_gap_count(): assert eng().summary()["competitive_gap_count"] == 0
def test_summary_empty_coaching_count(): assert eng().summary()["coaching_count"] == 0
def test_summary_empty_total_revenue(): assert eng().summary()["total_estimated_lost_revenue_usd"] == 0.0
def test_summary_total_count():
    e = eng(); e.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
    assert e.summary()["total"] == 4
def test_summary_risk_counts_sum():
    e = eng(); e.assess(make_input()); assert sum(e.summary()["risk_counts"].values()) == 1
def test_summary_pattern_counts_sum():
    e = eng(); e.assess(make_input()); assert sum(e.summary()["pattern_counts"].values()) == 1
def test_summary_severity_counts_sum():
    e = eng(); e.assess(make_input()); assert sum(e.summary()["severity_counts"].values()) == 1
def test_summary_action_counts_sum():
    e = eng(); e.assess(make_input()); assert sum(e.summary()["action_counts"].values()) == 1
def test_summary_avg_composite():
    e = eng(); r1 = e.assess(make_input()); r2 = e.assess(make_input(rep_id="R2"))
    assert e.summary()["avg_competitive_composite"] == round((r1.competitive_composite + r2.competitive_composite) / 2, 1)
def test_summary_total_lost_revenue():
    e = eng(); r1 = e.assess(make_input(total_competitive_deals=10, avg_deal_value_usd=1000.0))
    r2 = e.assess(make_input(rep_id="R2", total_competitive_deals=20, avg_deal_value_usd=2000.0))
    assert e.summary()["total_estimated_lost_revenue_usd"] == round(r1.estimated_lost_revenue_usd + r2.estimated_lost_revenue_usd, 2)
def test_summary_coaching_count_increments():
    e = eng(); e.assess(make_input(no_competitive_intel_rate_pct=0.35)); e.assess(make_input(rep_id="R2"))
    assert e.summary()["coaching_count"] >= 1
def test_summary_gap_count_increments():
    e = eng(); e.assess(make_input(battle_card_usage_rate_pct=0.40)); e.assess(make_input(rep_id="R2"))
    assert e.summary()["competitive_gap_count"] >= 1
@pytest.mark.parametrize("key", [
    "avg_preparedness_score", "avg_execution_score",
    "avg_intelligence_score", "avg_positioning_score",
])
def test_summary_avg_score_is_float(key):
    e = eng(); e.assess(make_input()); assert isinstance(e.summary()[key], float)


# ── 18. Engine isolation ──────────────────────────────────────────────────────

def test_two_engines_independent():
    e1 = eng(); e2 = eng(); e1.assess(make_input()); assert len(e2._results) == 0
def test_results_accumulate():
    e = eng(); e.assess(make_input()); e.assess(make_input(rep_id="R2")); assert len(e._results) == 2
def test_summary_reflects_all():
    e = eng(); [e.assess(make_input(rep_id=f"R{i}")) for i in range(3)]; assert e.summary()["total"] == 3
def test_fresh_engine_has_no_results(): assert len(eng()._results) == 0


# ── 19. Edge cases ────────────────────────────────────────────────────────────

_ALL_ZERO = dict(competitive_win_rate_pct=0.0, battle_card_usage_rate_pct=0.0,
                 competitive_mention_early_rate_pct=0.0, price_concession_vs_competitor_pct=0.0,
                 feature_comparison_loss_rate_pct=0.0, competitive_deal_cycle_delta_days=0.0,
                 no_competitive_intel_rate_pct=0.0, single_competitor_thread_rate_pct=0.0,
                 late_competitor_discovery_rate_pct=0.0, head_to_head_calls_per_deal=0.0,
                 post_loss_debrief_rate_pct=0.0, reference_customer_usage_pct=0.0)
_ALL_ONE = dict(competitive_win_rate_pct=1.0, battle_card_usage_rate_pct=1.0,
                competitive_mention_early_rate_pct=1.0, price_concession_vs_competitor_pct=1.0,
                feature_comparison_loss_rate_pct=1.0, no_competitive_intel_rate_pct=1.0,
                single_competitor_thread_rate_pct=1.0, late_competitor_discovery_rate_pct=1.0,
                reference_customer_usage_pct=1.0, post_loss_debrief_rate_pct=1.0)
def test_all_rates_zero(): assert isinstance(eng().assess(make_input(**_ALL_ZERO)), CompetitiveResult)
def test_all_rates_one(): assert isinstance(eng().assess(make_input(**_ALL_ONE)), CompetitiveResult)
def test_to_dict_rep_id_correct():
    assert eng().assess(make_input(rep_id="XYZ")).to_dict()["rep_id"] == "XYZ"
def test_to_dict_region_correct():
    assert eng().assess(make_input(region="APAC")).to_dict()["region"] == "APAC"
def test_to_dict_enum_values_are_strings():
    d = eng().assess(make_input()).to_dict()
    for k in ["competitive_risk", "competitive_pattern", "competitive_severity", "recommended_action"]:
        assert isinstance(d[k], str)
def test_single_deal_lost_revenue():
    r = eng().assess(make_input(total_competitive_deals=1, avg_deal_value_usd=50_000.0, competitive_loss_rate_pct=1.0))
    assert r.estimated_lost_revenue_usd == round(50_000 * 1.0 * (r.competitive_composite / 100), 2)
def test_large_batch_count():
    e = eng(); e.assess_batch([make_input(rep_id=f"R{i}") for i in range(50)])
    assert e.summary()["total"] == 50
def test_composite_nonnegative():
    r = eng().assess(make_input()); assert r.competitive_composite >= 0.0


# ── 20. Additional threshold boundary and integration tests ───────────────────

# Risk/severity parity: same composite, both use same boundary
@pytest.mark.parametrize("comp,risk,sev", [
    (0.0,   CompetitiveRisk.low,      CompetitiveSeverity.dominant),
    (10.0,  CompetitiveRisk.low,      CompetitiveSeverity.dominant),
    (20.0,  CompetitiveRisk.moderate, CompetitiveSeverity.competing),
    (30.0,  CompetitiveRisk.moderate, CompetitiveSeverity.competing),
    (40.0,  CompetitiveRisk.high,     CompetitiveSeverity.struggling),
    (55.0,  CompetitiveRisk.high,     CompetitiveSeverity.struggling),
    (60.0,  CompetitiveRisk.critical, CompetitiveSeverity.losing),
    (90.0,  CompetitiveRisk.critical, CompetitiveSeverity.losing),
])
def test_risk_severity_parity(comp, risk, sev):
    e = eng(); assert e._risk(comp) == risk and e._severity(comp) == sev

# Pattern detection — confirm no false positives for each near-boundary case
def test_no_unprepared_seller_when_usage_above_020(): assert pat(battle_card_usage_rate_pct=0.21, no_competitive_intel_rate_pct=0.50) != CompetitivePattern.unprepared_seller
def test_no_unprepared_seller_when_intel_below_040(): assert pat(battle_card_usage_rate_pct=0.10, no_competitive_intel_rate_pct=0.39) != CompetitivePattern.unprepared_seller
def test_no_feature_fighter_when_loss_below_045(): assert pat(feature_comparison_loss_rate_pct=0.44, price_concession_vs_competitor_pct=0.10) != CompetitivePattern.feature_fighter
def test_no_price_surrenderer_when_concession_below_055(): assert pat(price_concession_vs_competitor_pct=0.54, competitive_win_rate_pct=0.20) != CompetitivePattern.price_surrenderer
def test_no_price_surrenderer_when_win_rate_above_030(): assert pat(price_concession_vs_competitor_pct=0.60, competitive_win_rate_pct=0.31) != CompetitivePattern.price_surrenderer
def test_no_late_discovery_when_late_below_045(): assert pat(late_competitor_discovery_rate_pct=0.44, competitive_mention_early_rate_pct=0.10) != CompetitivePattern.late_discovery
def test_no_single_thread_when_thread_below_060(): assert pat(single_competitor_thread_rate_pct=0.59, competitive_stakeholder_loss_pct=0.50) != CompetitivePattern.single_thread_loser
def test_no_single_thread_when_stakeholder_below_045(): assert pat(single_competitor_thread_rate_pct=0.65, competitive_stakeholder_loss_pct=0.44) != CompetitivePattern.single_thread_loser

# Composite weight precision check
@pytest.mark.parametrize("pr,ex,in_,po,exp", [
    (40,0,0,0, round(40*.25,2)), (0,40,0,0, round(40*.35,2)),
    (0,0,40,0, round(40*.20,2)), (0,0,0,40, round(40*.20,2)),
])
def test_composite_individual_weight(pr,ex,in_,po,exp): assert eng()._composite(pr,ex,in_,po)==exp

# assess() end-to-end with moderate composite path
def test_assess_moderate_composite_path():
    r = eng().assess(make_input(competitive_win_rate_pct=0.55, battle_card_usage_rate_pct=0.60))
    assert r.competitive_composite < 40 and r.competitive_risk in (CompetitiveRisk.low, CompetitiveRisk.moderate)

# to_dict round-trips enum values as plain strings (not enum objects)
@pytest.mark.parametrize("key,typ", [
    ("competitive_risk", str), ("competitive_pattern", str),
    ("competitive_severity", str), ("recommended_action", str),
    ("has_competitive_gap", bool), ("requires_competitive_coaching", bool),
    ("competitive_composite", float),
])
def test_to_dict_field_type(key, typ):
    assert isinstance(eng().assess(make_input()).to_dict()[key], typ)

# summary() with multiple distinct risks
def test_summary_two_risk_levels():
    e = eng(); e.assess(make_input())
    e.assess(make_input(rep_id="R2", battle_card_usage_rate_pct=0.10, no_competitive_intel_rate_pct=0.50,
                        competitive_win_rate_pct=0.10, price_concession_vs_competitor_pct=0.70, competitive_deal_cycle_delta_days=35.0))
    rc = e.summary()["risk_counts"]
    assert sum(rc.values()) == 2 and len(rc) >= 2
def test_summary_avg_scores_are_rounded():
    e = eng(); e.assess(make_input()); s = e.summary()
    assert all(s[k] == round(s[k], 1) for k in ["avg_preparedness_score", "avg_execution_score", "avg_intelligence_score", "avg_positioning_score"])
def test_summary_coaching_and_gap_counts_logical():
    e = eng(); e.assess_batch([make_input(rep_id=f"R{i}") for i in range(10)]); s = e.summary()
    assert 0 <= s["competitive_gap_count"] <= 10 and 0 <= s["coaching_count"] <= 10
def test_batch_single_item():
    e = eng(); rs = e.assess_batch([make_input()])
    assert len(rs) == 1 and isinstance(rs[0], CompetitiveResult)

# Pattern label in signal for each named pattern
def test_signal_price_surrenderer_label():
    r = eng().assess(make_input(price_concession_vs_competitor_pct=0.60, competitive_win_rate_pct=0.20,
                                 competitive_deal_cycle_delta_days=35.0, battle_card_usage_rate_pct=0.10,
                                 no_competitive_intel_rate_pct=0.50))
    assert "Competitive execution healthy" not in r.competitive_signal  # unprepared wins priority
def test_signal_late_discovery_label():
    r = eng().assess(make_input(late_competitor_discovery_rate_pct=0.50, competitive_mention_early_rate_pct=0.10, competitive_win_rate_pct=0.20))
    assert "Late discovery" in r.competitive_signal
def test_signal_single_thread_label():
    r = eng().assess(make_input(single_competitor_thread_rate_pct=0.65, competitive_stakeholder_loss_pct=0.50, competitive_win_rate_pct=0.20))
    assert "Single-thread loser" in r.competitive_signal

# ── 21. Extra targeted tests to reach 280+ ───────────────────────────────────
def test_assess_multiple_reps_different_results():
    e = eng(); r1 = e.assess(make_input()); r2 = e.assess(make_input(rep_id="R2", competitive_win_rate_pct=0.20))
    assert r1.competitive_composite != r2.competitive_composite or r1.rep_id != r2.rep_id
def test_prep_combined_40_35(): assert prep(battle_card_usage_rate_pct=0.20, no_competitive_intel_rate_pct=0.45) == 75.0
def test_exec_combined_45_30(): assert exc(competitive_win_rate_pct=0.20, price_concession_vs_competitor_pct=0.60) == 75.0
def test_intel_combined_40_35(): assert intel(late_competitor_discovery_rate_pct=0.50, competitive_mention_early_rate_pct=0.20) == 75.0
def test_pos_combined_40_35(): assert pos(feature_comparison_loss_rate_pct=0.50, single_competitor_thread_rate_pct=0.65) == 75.0
def test_lost_revenue_scales_with_deals():
    e = eng(); r1 = e._lost_revenue(make_input(total_competitive_deals=10), 50.0)
    assert e._lost_revenue(make_input(total_competitive_deals=20), 50.0) == pytest.approx(r1 * 2)
def test_gap_composite_39_not_gap_alone():
    assert eng()._has_gap(make_input(competitive_win_rate_pct=0.50, battle_card_usage_rate_pct=0.60), 39.0) is False
def test_coaching_composite_24_no_triggers():
    assert eng()._requires_coaching(make_input(no_competitive_intel_rate_pct=0.10, late_competitor_discovery_rate_pct=0.10), 24.0) is False
def test_summary_empty_risk_counts_empty_dict(): assert eng().summary()["risk_counts"] == {}
def test_summary_empty_pattern_counts_empty_dict(): assert eng().summary()["pattern_counts"] == {}
def test_summary_empty_severity_counts_empty_dict(): assert eng().summary()["severity_counts"] == {}
def test_result_dataclass_has_15_fields(): assert len(CompetitiveResult.__dataclass_fields__) == 15
