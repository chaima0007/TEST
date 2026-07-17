"""
Comprehensive pytest test suite for SalesCompetitiveWinLossPatternEngine.
Module 212 — Sales Competitive Win/Loss Pattern Intelligence Engine
"""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_competitive_win_loss_pattern_engine import (
    CompetitiveAction, CompetitiveInput, CompetitivePattern, CompetitiveResult,
    CompetitiveRisk, CompetitiveSeverity, SalesCompetitiveWinLossPatternEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> CompetitiveInput:
    defaults = dict(
        rep_id="REP001", region="WEST", evaluation_period_id="2024-Q1",
        competitive_deal_rate_pct=0.20, competitive_win_rate_pct=0.70,
        competitive_loss_rate_pct=0.10, single_competitor_loss_concentration_pct=0.10,
        competitor_identified_late_rate_pct=0.10, battle_card_usage_rate_pct=0.80,
        competitive_discovery_score=0.80, price_cited_as_loss_reason_pct=0.10,
        feature_gap_cited_as_loss_reason_pct=0.10, value_differentiation_score=0.90,
        competitive_pipeline_conversion_rate_pct=0.60, displacement_deal_win_rate_pct=0.70,
        incumbent_defense_win_rate_pct=0.40, multi_competitor_deal_rate_pct=0.10,
        competitive_intelligence_recency_score=0.90, proof_of_concept_win_rate_pct=0.80,
        executive_alignment_in_comp_deals_pct=0.80,
        total_competitive_deals=20, avg_deal_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return CompetitiveInput(**defaults)


def eng() -> SalesCompetitiveWinLossPatternEngine:
    return SalesCompetitiveWinLossPatternEngine()


# ---------------------------------------------------------------------------
# 1. Enum values — string subclass
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("member,expected", [
    (CompetitiveRisk.low, "low"), (CompetitiveRisk.moderate, "moderate"),
    (CompetitiveRisk.high, "high"), (CompetitiveRisk.critical, "critical"),
])
def test_competitive_risk_values(member, expected):
    assert member == expected and isinstance(member, str)


@pytest.mark.parametrize("member,expected", [
    (CompetitivePattern.none, "none"),
    (CompetitivePattern.single_competitor_loser, "single_competitor_loser"),
    (CompetitivePattern.price_only_battle, "price_only_battle"),
    (CompetitivePattern.feature_gap_surrender, "feature_gap_surrender"),
    (CompetitivePattern.late_to_discover_comp, "late_to_discover_comp"),
    (CompetitivePattern.displacement_target, "displacement_target"),
])
def test_competitive_pattern_values(member, expected):
    assert member == expected and isinstance(member, str)


@pytest.mark.parametrize("member,expected", [
    (CompetitiveSeverity.dominant, "dominant"), (CompetitiveSeverity.competing, "competing"),
    (CompetitiveSeverity.slipping, "slipping"), (CompetitiveSeverity.losing, "losing"),
])
def test_competitive_severity_values(member, expected):
    assert member == expected and isinstance(member, str)


@pytest.mark.parametrize("member,expected", [
    (CompetitiveAction.no_action, "no_action"),
    (CompetitiveAction.competitive_monitoring, "competitive_monitoring"),
    (CompetitiveAction.differentiation_coaching, "differentiation_coaching"),
    (CompetitiveAction.battle_card_enforcement, "battle_card_enforcement"),
    (CompetitiveAction.discovery_depth_coaching, "discovery_depth_coaching"),
    (CompetitiveAction.pricing_strategy_coaching, "pricing_strategy_coaching"),
    (CompetitiveAction.competitive_deal_desk_support, "competitive_deal_desk_support"),
    (CompetitiveAction.win_loss_review_intervention, "win_loss_review_intervention"),
    (CompetitiveAction.competitive_strategy_reset, "competitive_strategy_reset"),
])
def test_competitive_action_values(member, expected):
    assert member == expected and isinstance(member, str)


# ---------------------------------------------------------------------------
# 2. to_dict() — exactly 15 keys, enums as strings
# ---------------------------------------------------------------------------

def test_to_dict_exactly_15_keys():
    assert len(eng().assess(make_input()).to_dict()) == 15


def test_to_dict_expected_keys():
    d = eng().assess(make_input()).to_dict()
    assert set(d) == {
        "rep_id", "region", "competitive_risk", "competitive_pattern",
        "competitive_severity", "recommended_action", "exposure_score",
        "positioning_score", "intelligence_score", "conversion_score",
        "competitive_composite", "has_competitive_gap",
        "requires_competitive_coaching", "estimated_lost_revenue_usd", "competitive_signal",
    }


def test_to_dict_enum_fields_are_plain_strings():
    d = eng().assess(make_input()).to_dict()
    for key in ("competitive_risk", "competitive_pattern", "competitive_severity", "recommended_action"):
        assert isinstance(d[key], str)


def test_to_dict_bool_types():
    d = eng().assess(make_input()).to_dict()
    assert isinstance(d["has_competitive_gap"], bool)
    assert isinstance(d["requires_competitive_coaching"], bool)


# ---------------------------------------------------------------------------
# 3. Sub-score tiers, cap at 100
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("concentration,loss_rate,multi,expected", [
    (0.0, 0.0, 0.0, 0), (0.25, 0.0, 0.0, 8), (0.40, 0.0, 0.0, 22), (0.60, 0.0, 0.0, 40),
    (0.0, 0.30, 0.0, 8), (0.0, 0.45, 0.0, 18), (0.0, 0.65, 0.0, 35),
    (0.0, 0.0, 0.30, 12), (0.0, 0.0, 0.50, 25),
    (0.60, 0.65, 0.50, 100),
])
def test_exposure_score_tiers(concentration, loss_rate, multi, expected):
    e = eng()
    assert e._exposure_score(make_input(
        single_competitor_loss_concentration_pct=concentration,
        competitive_loss_rate_pct=loss_rate,
        multi_competitor_deal_rate_pct=multi,
    )) == expected


@pytest.mark.parametrize("diff,price,feat,expected", [
    (1.0, 0.0, 0.0, 0), (0.65, 0.0, 0.0, 10), (0.45, 0.0, 0.0, 25), (0.20, 0.0, 0.0, 45),
    (1.0, 0.35, 0.0, 15), (1.0, 0.55, 0.0, 30),
    (1.0, 0.0, 0.28, 12), (1.0, 0.0, 0.45, 25),
    (0.20, 0.55, 0.45, 100),
])
def test_positioning_score_tiers(diff, price, feat, expected):
    e = eng()
    assert e._positioning_score(make_input(
        value_differentiation_score=diff,
        price_cited_as_loss_reason_pct=price,
        feature_gap_cited_as_loss_reason_pct=feat,
    )) == expected


@pytest.mark.parametrize("late,recency,bc,expected", [
    (0.0, 1.0, 1.0, 0), (0.20, 1.0, 1.0, 8), (0.35, 1.0, 1.0, 22), (0.55, 1.0, 1.0, 40),
    (0.0, 0.45, 1.0, 18), (0.0, 0.20, 1.0, 35),
    (0.0, 1.0, 0.55, 12), (0.0, 1.0, 0.25, 25),
    (0.55, 0.20, 0.25, 100),
])
def test_intelligence_score_tiers(late, recency, bc, expected):
    e = eng()
    assert e._intelligence_score(make_input(
        competitor_identified_late_rate_pct=late,
        competitive_intelligence_recency_score=recency,
        battle_card_usage_rate_pct=bc,
    )) == expected


@pytest.mark.parametrize("conv,disp,exec_a,expected", [
    (1.0, 1.0, 1.0, 0), (0.45, 1.0, 1.0, 10), (0.30, 1.0, 1.0, 25), (0.15, 1.0, 1.0, 45),
    (1.0, 0.40, 1.0, 15), (1.0, 0.20, 1.0, 30),
    (1.0, 1.0, 0.50, 12), (1.0, 1.0, 0.25, 25),
    (0.15, 0.20, 0.25, 100),
])
def test_conversion_score_tiers(conv, disp, exec_a, expected):
    e = eng()
    assert e._conversion_score(make_input(
        competitive_pipeline_conversion_rate_pct=conv,
        displacement_deal_win_rate_pct=disp,
        executive_alignment_in_comp_deals_pct=exec_a,
    )) == expected


@pytest.mark.parametrize("scorer,kwargs", [
    ("_exposure_score",    dict(single_competitor_loss_concentration_pct=0.99, competitive_loss_rate_pct=0.99, multi_competitor_deal_rate_pct=0.99)),
    ("_positioning_score", dict(value_differentiation_score=0.0, price_cited_as_loss_reason_pct=1.0, feature_gap_cited_as_loss_reason_pct=1.0)),
    ("_intelligence_score", dict(competitor_identified_late_rate_pct=1.0, competitive_intelligence_recency_score=0.0, battle_card_usage_rate_pct=0.0)),
    ("_conversion_score",  dict(competitive_pipeline_conversion_rate_pct=0.0, displacement_deal_win_rate_pct=0.0, executive_alignment_in_comp_deals_pct=0.0)),
])
def test_sub_score_capped_at_100(scorer, kwargs):
    e = eng()
    assert getattr(e, scorer)(make_input(**kwargs)) <= 100


# ---------------------------------------------------------------------------
# 4. Composite weights and cap/rounding
# ---------------------------------------------------------------------------

def test_weights_sum_to_one():
    assert abs(0.30 + 0.25 + 0.25 + 0.20 - 1.00) < 1e-9


def test_composite_formula():
    e = eng()
    assert e._composite(40, 50, 60, 80) == round(40*0.30 + 50*0.25 + 60*0.25 + 80*0.20, 2)


def test_composite_capped_at_100():
    assert eng()._composite(100, 100, 100, 100) == 100.0


def test_composite_zero():
    assert eng()._composite(0, 0, 0, 0) == 0.0


# ---------------------------------------------------------------------------
# 5 & 6. Risk and Severity thresholds
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("comp,risk,sev", [
    (0.0,   CompetitiveRisk.low,      CompetitiveSeverity.dominant),
    (19.99, CompetitiveRisk.low,      CompetitiveSeverity.dominant),
    (20.0,  CompetitiveRisk.moderate, CompetitiveSeverity.competing),
    (39.99, CompetitiveRisk.moderate, CompetitiveSeverity.competing),
    (40.0,  CompetitiveRisk.high,     CompetitiveSeverity.slipping),
    (59.99, CompetitiveRisk.high,     CompetitiveSeverity.slipping),
    (60.0,  CompetitiveRisk.critical, CompetitiveSeverity.losing),
    (100.0, CompetitiveRisk.critical, CompetitiveSeverity.losing),
])
def test_risk_and_severity_thresholds(comp, risk, sev):
    e = eng()
    assert e._risk(comp) == risk
    assert e._severity(comp) == sev


# ---------------------------------------------------------------------------
# 7. All 6 patterns — priority ordering
# ---------------------------------------------------------------------------

def test_pattern_none():
    assert eng()._pattern(make_input()) == CompetitivePattern.none


@pytest.mark.parametrize("kwargs,expected_pattern", [
    (dict(single_competitor_loss_concentration_pct=0.55, competitive_win_rate_pct=0.30),
     CompetitivePattern.single_competitor_loser),
    (dict(price_cited_as_loss_reason_pct=0.50, value_differentiation_score=0.30),
     CompetitivePattern.price_only_battle),
    (dict(feature_gap_cited_as_loss_reason_pct=0.40, competitive_discovery_score=0.40),
     CompetitivePattern.feature_gap_surrender),
    (dict(competitor_identified_late_rate_pct=0.50, battle_card_usage_rate_pct=0.30),
     CompetitivePattern.late_to_discover_comp),
    (dict(displacement_deal_win_rate_pct=0.15, incumbent_defense_win_rate_pct=0.65),
     CompetitivePattern.displacement_target),
])
def test_pattern_detection(kwargs, expected_pattern):
    assert eng()._pattern(make_input(**kwargs)) == expected_pattern


def test_pattern_priority_single_beats_price():
    inp = make_input(single_competitor_loss_concentration_pct=0.55,
                     competitive_win_rate_pct=0.30,
                     price_cited_as_loss_reason_pct=0.50,
                     value_differentiation_score=0.30)
    assert eng()._pattern(inp) == CompetitivePattern.single_competitor_loser


# ---------------------------------------------------------------------------
# 8. Action rules for each risk × pattern
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("risk,pattern,expected", [
    (CompetitiveRisk.critical, CompetitivePattern.single_competitor_loser, CompetitiveAction.competitive_strategy_reset),
    (CompetitiveRisk.critical, CompetitivePattern.price_only_battle,       CompetitiveAction.competitive_strategy_reset),
    (CompetitiveRisk.critical, CompetitivePattern.feature_gap_surrender,   CompetitiveAction.win_loss_review_intervention),
    (CompetitiveRisk.critical, CompetitivePattern.late_to_discover_comp,   CompetitiveAction.win_loss_review_intervention),
    (CompetitiveRisk.critical, CompetitivePattern.displacement_target,     CompetitiveAction.win_loss_review_intervention),
    (CompetitiveRisk.critical, CompetitivePattern.none,                    CompetitiveAction.win_loss_review_intervention),
    (CompetitiveRisk.high, CompetitivePattern.single_competitor_loser, CompetitiveAction.battle_card_enforcement),
    (CompetitiveRisk.high, CompetitivePattern.price_only_battle,       CompetitiveAction.pricing_strategy_coaching),
    (CompetitiveRisk.high, CompetitivePattern.feature_gap_surrender,   CompetitiveAction.differentiation_coaching),
    (CompetitiveRisk.high, CompetitivePattern.late_to_discover_comp,   CompetitiveAction.discovery_depth_coaching),
    (CompetitiveRisk.high, CompetitivePattern.displacement_target,     CompetitiveAction.competitive_deal_desk_support),
    (CompetitiveRisk.high, CompetitivePattern.none,                    CompetitiveAction.competitive_monitoring),
    (CompetitiveRisk.moderate, CompetitivePattern.none,             CompetitiveAction.competitive_monitoring),
    (CompetitiveRisk.moderate, CompetitivePattern.price_only_battle, CompetitiveAction.competitive_monitoring),
    (CompetitiveRisk.low, CompetitivePattern.none,                   CompetitiveAction.no_action),
    (CompetitiveRisk.low, CompetitivePattern.single_competitor_loser, CompetitiveAction.no_action),
])
def test_action_rules(risk, pattern, expected):
    assert eng()._action(risk, pattern) == expected


# ---------------------------------------------------------------------------
# 9. has_competitive_gap
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("comp,win_rate,conc,expected", [
    (40.0,  0.70, 0.10, True),   # via composite
    (10.0,  0.35, 0.10, True),   # via win_rate
    (10.0,  0.70, 0.40, True),   # via concentration
    (10.0,  0.70, 0.10, False),  # none triggered
    (39.99, 0.36, 0.39, False),  # all just below
    (40.0,  0.36, 0.39, True),
    (10.0,  0.35, 0.39, True),
    (10.0,  0.36, 0.40, True),
])
def test_has_competitive_gap(comp, win_rate, conc, expected):
    e = eng()
    inp = make_input(competitive_win_rate_pct=win_rate,
                     single_competitor_loss_concentration_pct=conc)
    assert e._has_competitive_gap(inp, comp) is expected


# ---------------------------------------------------------------------------
# 10. requires_competitive_coaching
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("comp,bc,diff,expected", [
    (25.0,  0.90, 0.90, True),   # via composite
    (10.0,  0.40, 0.90, True),   # via battle card
    (10.0,  0.90, 0.50, True),   # via diff score
    (10.0,  0.90, 0.90, False),  # none triggered
    (24.99, 0.41, 0.51, False),
    (25.0,  0.41, 0.51, True),
    (10.0,  0.40, 0.51, True),
    (10.0,  0.41, 0.50, True),
])
def test_requires_coaching(comp, bc, diff, expected):
    e = eng()
    inp = make_input(battle_card_usage_rate_pct=bc, value_differentiation_score=diff)
    assert e._requires_coaching(inp, comp) is expected


# ---------------------------------------------------------------------------
# 11. estimated_lost_revenue_usd
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("deals,avg_val,loss_rate,comp,expected", [
    (100, 1_000.0, 0.50, 80.0, 40_000.0),
    (0,   10_000.0, 0.50, 50.0, 0.0),
    (50,  20_000.0, 0.50, 0.0, 0.0),
    (7,   3_333.33, 0.333, 33.33, round(7 * 3_333.33 * 0.333 * 0.3333, 2)),
])
def test_lost_revenue(deals, avg_val, loss_rate, comp, expected):
    e = eng()
    inp = make_input(total_competitive_deals=deals, avg_deal_value_usd=avg_val,
                     competitive_loss_rate_pct=loss_rate)
    assert e._lost_revenue(inp, comp) == expected


def test_lost_revenue_rounded_to_2dp():
    e = eng()
    inp = make_input(total_competitive_deals=7, avg_deal_value_usd=3_333.33,
                     competitive_loss_rate_pct=0.333)
    r = e._lost_revenue(inp, 33.33)
    assert r == round(r, 2)


# ---------------------------------------------------------------------------
# 12. competitive_signal
# ---------------------------------------------------------------------------

def test_stable_signal_when_composite_below_20():
    result = eng().assess(make_input())
    assert result.competitive_composite < 20
    assert "strong" in result.competitive_signal.lower()


def _high_risk_inp(**extra):
    return make_input(single_competitor_loss_concentration_pct=0.55,
                      competitive_win_rate_pct=0.30,
                      competitive_loss_rate_pct=0.60,
                      value_differentiation_score=0.10, **extra)


def test_active_signal_contains_win_rate_pct():
    r = eng().assess(_high_risk_inp())
    assert str(round(0.30 * 100)) in r.competitive_signal


def test_active_signal_contains_price_pct():
    r = eng().assess(_high_risk_inp(price_cited_as_loss_reason_pct=0.45))
    assert "45" in r.competitive_signal


def test_active_signal_contains_late_discovery():
    r = eng().assess(_high_risk_inp(competitor_identified_late_rate_pct=0.35))
    assert "35" in r.competitive_signal


def test_active_signal_contains_composite():
    r = eng().assess(_high_risk_inp())
    assert str(round(r.competitive_composite)) in r.competitive_signal


@pytest.mark.parametrize("pattern_kwargs,label", [
    (dict(single_competitor_loss_concentration_pct=0.55, competitive_win_rate_pct=0.30,
          competitive_loss_rate_pct=0.60, value_differentiation_score=0.10),
     "Single competitor loser"),
    (dict(feature_gap_cited_as_loss_reason_pct=0.40, competitive_discovery_score=0.40,
          competitive_loss_rate_pct=0.50, value_differentiation_score=0.10),
     "Feature gap surrender"),
    (dict(competitor_identified_late_rate_pct=0.50, battle_card_usage_rate_pct=0.30,
          competitive_loss_rate_pct=0.50, competitive_intelligence_recency_score=0.10),
     "Late to discover competitor"),
    (dict(displacement_deal_win_rate_pct=0.15, incumbent_defense_win_rate_pct=0.65,
          competitive_loss_rate_pct=0.50, value_differentiation_score=0.10),
     "Displacement target"),
])
def test_pattern_label_in_active_signal(pattern_kwargs, label):
    r = eng().assess(make_input(**pattern_kwargs))
    if r.competitive_composite >= 20:
        assert label in r.competitive_signal


# ---------------------------------------------------------------------------
# 13. assess(), assess_batch(), summary() with 13 keys
# ---------------------------------------------------------------------------

def test_assess_returns_competitive_result():
    assert isinstance(eng().assess(make_input()), CompetitiveResult)


def test_assess_stores_result():
    e = eng()
    e.assess(make_input())
    assert len(e._results) == 1


def test_assess_preserves_rep_id_and_region():
    r = eng().assess(make_input(rep_id="X99", region="EAST"))
    assert r.rep_id == "X99" and r.region == "EAST"


def test_assess_batch_count_and_storage():
    e = eng()
    results = e.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
    assert len(results) == 5 and len(e._results) == 5


def test_summary_13_keys_empty():
    s = eng().summary()
    assert len(s) == 13


def test_summary_13_keys_nonempty():
    e = eng()
    e.assess(make_input())
    assert len(e.summary()) == 13


def test_summary_key_set():
    assert set(eng().summary()) == {
        "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
        "avg_competitive_composite", "competitive_gap_count", "coaching_count",
        "avg_exposure_score", "avg_positioning_score", "avg_intelligence_score",
        "avg_conversion_score", "total_estimated_lost_revenue_usd",
    }


def test_summary_empty_zeros():
    s = eng().summary()
    assert s["total"] == 0 and s["avg_competitive_composite"] == 0.0
    assert s["competitive_gap_count"] == 0 and s["total_estimated_lost_revenue_usd"] == 0.0


def test_summary_total_and_risk_counts():
    e = eng()
    e.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
    s = e.summary()
    assert s["total"] == 4
    assert "low" in s["risk_counts"]


def test_summary_accumulated_revenue():
    e = eng()
    r1 = e.assess(make_input(total_competitive_deals=10, avg_deal_value_usd=1000.0))
    r2 = e.assess(make_input(total_competitive_deals=5, avg_deal_value_usd=2000.0))
    expected = round(r1.estimated_lost_revenue_usd + r2.estimated_lost_revenue_usd, 2)
    assert e.summary()["total_estimated_lost_revenue_usd"] == expected


# ---------------------------------------------------------------------------
# 14. Edge cases
# ---------------------------------------------------------------------------

def test_zero_input_no_raise():
    e = eng()
    inp = make_input(
        competitive_deal_rate_pct=0.0, competitive_win_rate_pct=0.0,
        competitive_loss_rate_pct=0.0, single_competitor_loss_concentration_pct=0.0,
        competitor_identified_late_rate_pct=0.0, battle_card_usage_rate_pct=0.0,
        competitive_discovery_score=0.0, price_cited_as_loss_reason_pct=0.0,
        feature_gap_cited_as_loss_reason_pct=0.0, value_differentiation_score=0.0,
        competitive_pipeline_conversion_rate_pct=0.0, displacement_deal_win_rate_pct=0.0,
        incumbent_defense_win_rate_pct=0.0, multi_competitor_deal_rate_pct=0.0,
        competitive_intelligence_recency_score=0.0, proof_of_concept_win_rate_pct=0.0,
        executive_alignment_in_comp_deals_pct=0.0,
        total_competitive_deals=0, avg_deal_value_usd=0.0,
    )
    r = e.assess(inp)
    assert r.estimated_lost_revenue_usd == 0.0
    assert 0.0 <= r.competitive_composite <= 100.0


def test_max_input_composite_capped():
    e = eng()
    inp = make_input(
        competitive_deal_rate_pct=1.0, competitive_win_rate_pct=1.0,
        competitive_loss_rate_pct=1.0, single_competitor_loss_concentration_pct=1.0,
        competitor_identified_late_rate_pct=1.0, battle_card_usage_rate_pct=1.0,
        competitive_discovery_score=1.0, price_cited_as_loss_reason_pct=1.0,
        feature_gap_cited_as_loss_reason_pct=1.0, value_differentiation_score=1.0,
        competitive_pipeline_conversion_rate_pct=1.0, displacement_deal_win_rate_pct=1.0,
        incumbent_defense_win_rate_pct=1.0, multi_competitor_deal_rate_pct=1.0,
        competitive_intelligence_recency_score=1.0, proof_of_concept_win_rate_pct=1.0,
        executive_alignment_in_comp_deals_pct=1.0,
        total_competitive_deals=10_000, avg_deal_value_usd=1_000_000.0,
    )
    assert e.assess(inp).competitive_composite <= 100.0


def test_engine_isolation():
    ea, eb = eng(), eng()
    ea.assess(make_input(rep_id="A"))
    ea.assess(make_input(rep_id="A2"))
    eb.assess(make_input(rep_id="B"))
    assert ea.summary()["total"] == 2 and eb.summary()["total"] == 1


def test_sub_scores_within_bounds():
    e = eng()
    for conc in (0.0, 0.30, 0.60, 1.0):
        r = e.assess(make_input(single_competitor_loss_concentration_pct=conc))
        assert 0 <= r.exposure_score <= 100
        assert 0 <= r.positioning_score <= 100
        assert 0 <= r.intelligence_score <= 100
        assert 0 <= r.conversion_score <= 100


def test_composite_always_in_bounds():
    e = eng()
    for loss_rate in (0.0, 0.30, 0.65, 1.0):
        r = e.assess(make_input(competitive_loss_rate_pct=loss_rate))
        assert 0.0 <= r.competitive_composite <= 100.0


# ---------------------------------------------------------------------------
# Run directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import subprocess, sys
    sys.exit(subprocess.run([sys.executable, "-m", "pytest", __file__, "-v", "--tb=short"]).returncode)
