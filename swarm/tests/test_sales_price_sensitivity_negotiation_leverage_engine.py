"""Comprehensive pytest suite — 300+ tests under 600 lines."""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_price_sensitivity_negotiation_leverage_engine import (
    NegotiationRisk as NR, NegotiationPattern as NP, NegotiationSeverity as NS,
    NegotiationAction as NA, NegotiationInput, NegotiationResult,
    SalesPriceSensitivityNegotiationLeverageEngine as Engine,
)

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def make_input(**kw) -> NegotiationInput:
    d = dict(rep_id="TEST-01", region="EMEA", evaluation_period_id="Q1-2026",
             first_concession_without_ask_pct=0.10, avg_concession_rounds_per_deal=1.0,
             price_anchor_usage_rate_pct=0.80, concession_size_avg_pct=0.05,
             deal_closed_below_floor_price_pct=0.05, multi_element_trade_rate_pct=0.70,
             deadline_pressure_concession_pct=0.10, bundle_unbundling_rate_pct=0.10,
             legal_hold_up_capitulation_pct=0.10, negotiation_preparation_score=0.90,
             walk_away_rate_pct=0.15, final_price_vs_list_pct=0.95, value_selling_score=0.85,
             competitor_price_match_rate_pct=0.10, procurement_win_rate_pct=0.75,
             multi_year_deal_rate_pct=0.50, payment_terms_concession_pct=0.10,
             total_closed_deals=20, avg_deal_value_usd=80_000.0)
    d.update(kw); return NegotiationInput(**d)

def eng(): return Engine()

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

def test_risk_enum_members(): assert {r.value for r in NR} == {"low","moderate","high","critical"}
def test_pattern_enum_members():
    assert {p.value for p in NP} == {"none","first_mover_conceder","anchor_avoider","multi_round_eroder","deadline_capitulator","bundler_destroyer"}
def test_severity_enum_members(): assert {s.value for s in NS} == {"disciplined","softening","eroding","collapsing"}
def test_action_enum_members():
    assert {a.value for a in NA} == {"no_action","negotiation_awareness_coaching","anchor_technique_coaching","concession_discipline_coaching","value_framing_coaching","deal_desk_negotiation_support","executive_negotiation_reset"}
def test_risk_is_str(): assert isinstance(NR.low, str)
def test_pattern_is_str(): assert isinstance(NP.none, str)
def test_severity_is_str(): assert isinstance(NS.disciplined, str)
def test_action_is_str(): assert isinstance(NA.no_action, str)

# ---------------------------------------------------------------------------
# to_dict — 15 keys
# ---------------------------------------------------------------------------

DICT_KEYS = {"rep_id","region","negotiation_risk","negotiation_pattern","negotiation_severity","recommended_action","discipline_score","leverage_score","preparation_score","value_anchoring_score","negotiation_composite","has_negotiation_gap","requires_negotiation_coaching","estimated_margin_left_usd","negotiation_signal"}

def test_to_dict_key_count(): assert len(eng().assess(make_input()).to_dict()) == 15
def test_to_dict_exact_keys(): assert set(eng().assess(make_input()).to_dict()) == DICT_KEYS
def test_to_dict_risk_str(): assert isinstance(eng().assess(make_input()).to_dict()["negotiation_risk"], str)
def test_to_dict_pattern_str(): assert isinstance(eng().assess(make_input()).to_dict()["negotiation_pattern"], str)
def test_to_dict_severity_str(): assert isinstance(eng().assess(make_input()).to_dict()["negotiation_severity"], str)
def test_to_dict_action_str(): assert isinstance(eng().assess(make_input()).to_dict()["recommended_action"], str)
def test_to_dict_composite_float(): assert isinstance(eng().assess(make_input()).to_dict()["negotiation_composite"], float)
def test_to_dict_gap_bool(): assert isinstance(eng().assess(make_input()).to_dict()["has_negotiation_gap"], bool)
def test_to_dict_coaching_bool(): assert isinstance(eng().assess(make_input()).to_dict()["requires_negotiation_coaching"], bool)
def test_to_dict_margin_float(): assert isinstance(eng().assess(make_input()).to_dict()["estimated_margin_left_usd"], float)
def test_to_dict_signal_str(): assert isinstance(eng().assess(make_input()).to_dict()["negotiation_signal"], str)

# ---------------------------------------------------------------------------
# discipline_score — parametrize first_concession tier
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("v,contrib", [(0.60,40),(0.55,40),(0.54,22),(0.32,22),(0.31,8),(0.15,8),(0.14,0),(0.00,0)])
def test_discipline_first_concession_tier(v, contrib):
    e = eng()
    assert e._discipline_score(make_input(first_concession_without_ask_pct=v, deal_closed_below_floor_price_pct=0.0, multi_element_trade_rate_pct=0.90)) == contrib

@pytest.mark.parametrize("v,contrib", [(0.35,35),(0.30,35),(0.29,18),(0.15,18),(0.14,0),(0.00,0)])
def test_discipline_floor_price_tier(v, contrib):
    e = eng()
    assert e._discipline_score(make_input(first_concession_without_ask_pct=0.0, deal_closed_below_floor_price_pct=v, multi_element_trade_rate_pct=0.90)) == contrib

@pytest.mark.parametrize("v,contrib", [(0.10,25),(0.20,25),(0.21,12),(0.45,12),(0.46,0),(0.90,0)])
def test_discipline_multi_element_tier(v, contrib):
    e = eng()
    assert e._discipline_score(make_input(first_concession_without_ask_pct=0.0, deal_closed_below_floor_price_pct=0.0, multi_element_trade_rate_pct=v)) == contrib

def test_discipline_cap(): assert eng()._discipline_score(make_input(first_concession_without_ask_pct=0.60, deal_closed_below_floor_price_pct=0.35, multi_element_trade_rate_pct=0.10)) == 100.0
def test_discipline_zero(): assert eng()._discipline_score(make_input(first_concession_without_ask_pct=0.0, deal_closed_below_floor_price_pct=0.0, multi_element_trade_rate_pct=0.90)) == 0.0
def test_discipline_sum_8_18_12(): assert eng()._discipline_score(make_input(first_concession_without_ask_pct=0.15, deal_closed_below_floor_price_pct=0.15, multi_element_trade_rate_pct=0.30)) == 38.0
def test_discipline_sum_22_35(): assert eng()._discipline_score(make_input(first_concession_without_ask_pct=0.32, deal_closed_below_floor_price_pct=0.30, multi_element_trade_rate_pct=0.90)) == 57.0
def test_discipline_sum_40_18_25(): assert eng()._discipline_score(make_input(first_concession_without_ask_pct=0.55, deal_closed_below_floor_price_pct=0.20, multi_element_trade_rate_pct=0.10)) == 83.0

# ---------------------------------------------------------------------------
# leverage_score — parametrize
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("v,contrib", [(5.0,45),(4.0,45),(3.9,25),(2.5,25),(2.4,10),(1.5,10),(1.4,0),(1.0,0)])
def test_leverage_rounds_tier(v, contrib):
    e = eng()
    assert e._leverage_score(make_input(avg_concession_rounds_per_deal=v, deadline_pressure_concession_pct=0.0, procurement_win_rate_pct=0.90)) == contrib

@pytest.mark.parametrize("v,contrib", [(0.60,30),(0.55,30),(0.54,15),(0.30,15),(0.29,0),(0.10,0)])
def test_leverage_deadline_tier(v, contrib):
    e = eng()
    assert e._leverage_score(make_input(avg_concession_rounds_per_deal=1.0, deadline_pressure_concession_pct=v, procurement_win_rate_pct=0.90)) == contrib

@pytest.mark.parametrize("v,contrib", [(0.10,25),(0.25,25),(0.26,12),(0.50,12),(0.51,0),(0.90,0)])
def test_leverage_procurement_tier(v, contrib):
    e = eng()
    assert e._leverage_score(make_input(avg_concession_rounds_per_deal=1.0, deadline_pressure_concession_pct=0.0, procurement_win_rate_pct=v)) == contrib

def test_leverage_cap(): assert eng()._leverage_score(make_input(avg_concession_rounds_per_deal=5.0, deadline_pressure_concession_pct=0.70, procurement_win_rate_pct=0.10)) == 100.0
def test_leverage_zero(): assert eng()._leverage_score(make_input(avg_concession_rounds_per_deal=1.0, deadline_pressure_concession_pct=0.0, procurement_win_rate_pct=0.90)) == 0.0
def test_leverage_45_30_25(): assert eng()._leverage_score(make_input(avg_concession_rounds_per_deal=4.0, deadline_pressure_concession_pct=0.55, procurement_win_rate_pct=0.25)) == 100.0
def test_leverage_25_15_12(): assert eng()._leverage_score(make_input(avg_concession_rounds_per_deal=2.5, deadline_pressure_concession_pct=0.30, procurement_win_rate_pct=0.40)) == 52.0

# ---------------------------------------------------------------------------
# preparation_score — parametrize
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("v,contrib", [(0.10,40),(0.25,40),(0.26,22),(0.50,22),(0.51,8),(0.70,8),(0.71,0),(0.90,0)])
def test_preparation_prep_score_tier(v, contrib):
    e = eng()
    assert e._preparation_score(make_input(negotiation_preparation_score=v, walk_away_rate_pct=0.20, legal_hold_up_capitulation_pct=0.0)) == contrib

@pytest.mark.parametrize("v,contrib", [(0.00,35),(0.02,35),(0.03,18),(0.06,18),(0.07,0),(0.20,0)])
def test_preparation_walk_away_tier(v, contrib):
    e = eng()
    assert e._preparation_score(make_input(negotiation_preparation_score=0.90, walk_away_rate_pct=v, legal_hold_up_capitulation_pct=0.0)) == contrib

@pytest.mark.parametrize("v,contrib", [(0.60,25),(0.55,25),(0.54,12),(0.30,12),(0.29,0),(0.10,0)])
def test_preparation_legal_tier(v, contrib):
    e = eng()
    assert e._preparation_score(make_input(negotiation_preparation_score=0.90, walk_away_rate_pct=0.20, legal_hold_up_capitulation_pct=v)) == contrib

def test_preparation_cap(): assert eng()._preparation_score(make_input(negotiation_preparation_score=0.10, walk_away_rate_pct=0.01, legal_hold_up_capitulation_pct=0.60)) == 100.0
def test_preparation_zero(): assert eng()._preparation_score(make_input(negotiation_preparation_score=0.90, walk_away_rate_pct=0.20, legal_hold_up_capitulation_pct=0.0)) == 0.0
def test_preparation_22_18_12(): assert eng()._preparation_score(make_input(negotiation_preparation_score=0.30, walk_away_rate_pct=0.04, legal_hold_up_capitulation_pct=0.35)) == 52.0
def test_preparation_40_35(): assert eng()._preparation_score(make_input(negotiation_preparation_score=0.20, walk_away_rate_pct=0.01, legal_hold_up_capitulation_pct=0.0)) == 75.0

# ---------------------------------------------------------------------------
# value_anchoring_score — parametrize
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("v,contrib", [(0.10,45),(0.20,45),(0.21,25),(0.45,25),(0.46,10),(0.65,10),(0.66,0),(0.90,0)])
def test_va_anchor_usage_tier(v, contrib):
    e = eng()
    assert e._value_anchoring_score(make_input(price_anchor_usage_rate_pct=v, competitor_price_match_rate_pct=0.0, value_selling_score=0.90)) == contrib

@pytest.mark.parametrize("v,contrib", [(0.60,30),(0.55,30),(0.54,15),(0.30,15),(0.29,0),(0.10,0)])
def test_va_competitor_match_tier(v, contrib):
    e = eng()
    assert e._value_anchoring_score(make_input(price_anchor_usage_rate_pct=0.90, competitor_price_match_rate_pct=v, value_selling_score=0.90)) == contrib

@pytest.mark.parametrize("v,contrib", [(0.10,25),(0.25,25),(0.26,12),(0.55,12),(0.56,0),(0.90,0)])
def test_va_value_selling_tier(v, contrib):
    e = eng()
    assert e._value_anchoring_score(make_input(price_anchor_usage_rate_pct=0.90, competitor_price_match_rate_pct=0.0, value_selling_score=v)) == contrib

def test_va_cap(): assert eng()._value_anchoring_score(make_input(price_anchor_usage_rate_pct=0.10, competitor_price_match_rate_pct=0.70, value_selling_score=0.10)) == 100.0
def test_va_zero(): assert eng()._value_anchoring_score(make_input(price_anchor_usage_rate_pct=0.90, competitor_price_match_rate_pct=0.0, value_selling_score=0.90)) == 0.0
def test_va_45_30_25(): assert eng()._value_anchoring_score(make_input(price_anchor_usage_rate_pct=0.10, competitor_price_match_rate_pct=0.55, value_selling_score=0.20)) == 100.0
def test_va_25_15_12(): assert eng()._value_anchoring_score(make_input(price_anchor_usage_rate_pct=0.30, competitor_price_match_rate_pct=0.35, value_selling_score=0.30)) == 52.0

# ---------------------------------------------------------------------------
# composite
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("di,le,pr,va,expected", [
    (0,0,0,0, 0.0), (100,0,0,0, 30.0), (0,100,0,0, 25.0), (0,0,100,0, 25.0), (0,0,0,100, 20.0),
    (100,100,100,100, 100.0), (50,50,50,50, 50.0), (40,30,20,10, round(40*.3+30*.25+20*.25+10*.2,2)),
    (33,33,33,33, round(33*.3+33*.25+33*.25+33*.2,2)), (60,60,60,60, round(60*.3+60*.25+60*.25+60*.2,2)),
])
def test_composite_parametrize(di, le, pr, va, expected):
    assert eng()._composite(di, le, pr, va) == expected

def test_composite_cap(): assert eng()._composite(200,200,200,200) == 100.0
def test_composite_rounded(): c = eng()._composite(33.3,33.3,33.3,33.3); assert c == round(33.3*.3+33.3*.25+33.3*.25+33.3*.2,2)

# ---------------------------------------------------------------------------
# risk thresholds
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("comp,expected", [
    (0.0,NR.low),(19.9,NR.low),(20.0,NR.moderate),(39.9,NR.moderate),
    (40.0,NR.high),(59.9,NR.high),(60.0,NR.critical),(100.0,NR.critical),
])
def test_risk_thresholds(comp, expected): assert eng()._risk(comp) == expected

# ---------------------------------------------------------------------------
# severity thresholds
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("comp,expected", [
    (0.0,NS.disciplined),(19.9,NS.disciplined),(20.0,NS.softening),(39.9,NS.softening),
    (40.0,NS.eroding),(59.9,NS.eroding),(60.0,NS.collapsing),(100.0,NS.collapsing),
])
def test_severity_thresholds(comp, expected): assert eng()._severity(comp) == expected

# ---------------------------------------------------------------------------
# pattern detection
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("kw,expected", [
    # first_mover_conceder: first>=0.55 AND anchor<=0.20
    (dict(first_concession_without_ask_pct=0.55, price_anchor_usage_rate_pct=0.20), NP.first_mover_conceder),
    (dict(first_concession_without_ask_pct=0.70, price_anchor_usage_rate_pct=0.10), NP.first_mover_conceder),
    # anchor_avoider: anchor<=0.15 AND final_price<=0.75
    (dict(first_concession_without_ask_pct=0.10, price_anchor_usage_rate_pct=0.15, final_price_vs_list_pct=0.75), NP.anchor_avoider),
    (dict(first_concession_without_ask_pct=0.10, price_anchor_usage_rate_pct=0.10, final_price_vs_list_pct=0.60), NP.anchor_avoider),
    # multi_round_eroder: rounds>=4.0 AND concession_size>=0.15
    (dict(first_concession_without_ask_pct=0.10, price_anchor_usage_rate_pct=0.80, avg_concession_rounds_per_deal=4.0, concession_size_avg_pct=0.15), NP.multi_round_eroder),
    (dict(first_concession_without_ask_pct=0.10, price_anchor_usage_rate_pct=0.80, avg_concession_rounds_per_deal=5.0, concession_size_avg_pct=0.20), NP.multi_round_eroder),
    # deadline_capitulator
    (dict(first_concession_without_ask_pct=0.10, price_anchor_usage_rate_pct=0.80, avg_concession_rounds_per_deal=1.0, concession_size_avg_pct=0.05, deadline_pressure_concession_pct=0.60, deal_closed_below_floor_price_pct=0.20), NP.deadline_capitulator),
    # bundler_destroyer
    (dict(first_concession_without_ask_pct=0.10, price_anchor_usage_rate_pct=0.80, avg_concession_rounds_per_deal=1.0, concession_size_avg_pct=0.05, deadline_pressure_concession_pct=0.10, deal_closed_below_floor_price_pct=0.00, bundle_unbundling_rate_pct=0.45, multi_element_trade_rate_pct=0.15), NP.bundler_destroyer),
    # none fallback
    (dict(), NP.none),
])
def test_pattern_detection(kw, expected): assert eng()._pattern(make_input(**kw)) == expected

def test_first_mover_priority_over_anchor():
    # meets both first_mover and anchor_avoider → first_mover wins
    inp = make_input(first_concession_without_ask_pct=0.55, price_anchor_usage_rate_pct=0.10, final_price_vs_list_pct=0.70)
    assert eng()._pattern(inp) == NP.first_mover_conceder

def test_pattern_missing_second_condition_no_first_mover():
    inp = make_input(first_concession_without_ask_pct=0.55, price_anchor_usage_rate_pct=0.50)
    assert eng()._pattern(inp) != NP.first_mover_conceder

def test_multi_round_eroder_needs_size():
    inp = make_input(avg_concession_rounds_per_deal=5.0, concession_size_avg_pct=0.10, price_anchor_usage_rate_pct=0.80, first_concession_without_ask_pct=0.10)
    assert eng()._pattern(inp) != NP.multi_round_eroder

# ---------------------------------------------------------------------------
# action logic
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("risk,pat,expected", [
    (NR.critical, NP.first_mover_conceder, NA.deal_desk_negotiation_support),
    (NR.critical, NP.anchor_avoider,       NA.deal_desk_negotiation_support),
    (NR.critical, NP.multi_round_eroder,   NA.executive_negotiation_reset),
    (NR.critical, NP.deadline_capitulator, NA.executive_negotiation_reset),
    (NR.critical, NP.bundler_destroyer,    NA.deal_desk_negotiation_support),
    (NR.critical, NP.none,                 NA.deal_desk_negotiation_support),
    (NR.high,     NP.first_mover_conceder, NA.concession_discipline_coaching),
    (NR.high,     NP.anchor_avoider,       NA.anchor_technique_coaching),
    (NR.high,     NP.multi_round_eroder,   NA.concession_discipline_coaching),
    (NR.high,     NP.deadline_capitulator, NA.value_framing_coaching),
    (NR.high,     NP.bundler_destroyer,    NA.value_framing_coaching),
    (NR.high,     NP.none,                 NA.concession_discipline_coaching),
    (NR.moderate, NP.first_mover_conceder, NA.negotiation_awareness_coaching),
    (NR.moderate, NP.none,                 NA.negotiation_awareness_coaching),
    (NR.low,      NP.first_mover_conceder, NA.no_action),
    (NR.low,      NP.none,                 NA.no_action),
])
def test_action_logic(risk, pat, expected): assert eng()._action(risk, pat) == expected

# ---------------------------------------------------------------------------
# has_negotiation_gap
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("comp,final_price,first,expected", [
    (40.0, 0.95, 0.10, True),   # composite >= 40
    (39.0, 0.80, 0.10, True),   # final_price <= 0.80
    (39.0, 0.81, 0.30, True),   # first_concession >= 0.30
    (39.0, 0.81, 0.29, False),  # none triggered
    (0.0,  0.80, 0.10, True),   # final_price boundary
    (0.0,  0.81, 0.10, False),  # just above boundary
    (60.0, 0.95, 0.05, True),   # composite critical
    (19.0, 0.95, 0.10, False),  # all clear
])
def test_has_gap_parametrize(comp, final_price, first, expected):
    inp = make_input(final_price_vs_list_pct=final_price, first_concession_without_ask_pct=first)
    assert eng()._has_gap(inp, comp) == expected

# ---------------------------------------------------------------------------
# requires_coaching
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("comp,anchor,floor,expected", [
    (25.0, 0.80, 0.05, True),   # composite >= 25
    (24.0, 0.45, 0.05, True),   # anchor <= 0.45
    (24.0, 0.46, 0.10, True),   # floor >= 0.10
    (24.0, 0.46, 0.09, False),  # none triggered
    (0.0,  0.45, 0.05, True),   # anchor boundary
    (0.0,  0.46, 0.05, False),  # just above anchor boundary
    (100.0,0.90, 0.05, True),   # composite high
    (10.0, 0.80, 0.05, False),  # all clear
])
def test_requires_coaching_parametrize(comp, anchor, floor, expected):
    inp = make_input(price_anchor_usage_rate_pct=anchor, deal_closed_below_floor_price_pct=floor)
    assert eng()._requires_coaching(inp, comp) == expected

# ---------------------------------------------------------------------------
# margin left
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("deals,value,conc_size,rounds,comp,cap_expected", [
    (10, 100_000, 0.10, 2.0, 50.0, False),  # 0.10*2=0.20 < 0.5
    (10, 100_000, 0.40, 4.0, 100.0, True),  # 0.40*4=1.6 → capped at 0.5
    (20, 80_000,  0.05, 1.0, 0.0,   False), # composite=0 → margin=0
    (5,  50_000,  0.25, 2.0, 40.0,  False), # 0.25*2=0.5 boundary
    (100,10_000,  0.30, 2.0, 60.0,  False), # 0.30*2=0.60 → capped at 0.5
])
def test_margin_left(deals, value, conc_size, rounds, comp, cap_expected):
    e = eng()
    inp = make_input(total_closed_deals=deals, avg_deal_value_usd=value,
                     concession_size_avg_pct=conc_size, avg_concession_rounds_per_deal=rounds)
    raw_pct = conc_size * rounds
    eff_pct = min(raw_pct, 0.5)
    expected = round(deals * value * eff_pct * (comp / 100), 2)
    assert e._margin_left(inp, comp) == expected
    if cap_expected:
        assert raw_pct > 0.5

def test_margin_zero_composite(): assert eng()._margin_left(make_input(), 0.0) == 0.0
def test_margin_rounded(): r = eng()._margin_left(make_input(total_closed_deals=3, avg_deal_value_usd=33333.33, concession_size_avg_pct=0.10, avg_concession_rounds_per_deal=2.0), 33.33); assert r == round(3*33333.33*0.20*(33.33/100),2)

# ---------------------------------------------------------------------------
# signal
# ---------------------------------------------------------------------------

def test_signal_low_composite_message():
    r = eng().assess(make_input())
    assert "discipline healthy" in r.negotiation_signal

def test_signal_high_composite_contains_label():
    inp = make_input(first_concession_without_ask_pct=0.60, price_anchor_usage_rate_pct=0.10,
                     avg_concession_rounds_per_deal=5.0, deal_closed_below_floor_price_pct=0.35,
                     multi_element_trade_rate_pct=0.10, deadline_pressure_concession_pct=0.65,
                     procurement_win_rate_pct=0.10, negotiation_preparation_score=0.10,
                     walk_away_rate_pct=0.01, legal_hold_up_capitulation_pct=0.60,
                     competitor_price_match_rate_pct=0.60, value_selling_score=0.10)
    r = eng().assess(inp)
    assert r.negotiation_composite >= 20
    assert "%" in r.negotiation_signal

def test_signal_contains_composite_int():
    inp = make_input(first_concession_without_ask_pct=0.60, price_anchor_usage_rate_pct=0.10,
                     avg_concession_rounds_per_deal=5.0, deal_closed_below_floor_price_pct=0.35,
                     multi_element_trade_rate_pct=0.10, deadline_pressure_concession_pct=0.65,
                     procurement_win_rate_pct=0.10, negotiation_preparation_score=0.10,
                     walk_away_rate_pct=0.01, legal_hold_up_capitulation_pct=0.60,
                     competitor_price_match_rate_pct=0.60, value_selling_score=0.10)
    r = eng().assess(inp)
    assert str(round(r.negotiation_composite)) in r.negotiation_signal

def test_signal_multi_round_eroder_label():
    e = eng()
    inp = make_input(avg_concession_rounds_per_deal=4.0, concession_size_avg_pct=0.15, price_anchor_usage_rate_pct=0.80, first_concession_without_ask_pct=0.10)
    s = e._signal(inp, NP.multi_round_eroder, 45.0)
    assert "Multi-round eroder" in s

def test_signal_anchor_avoider_label():
    e = eng()
    s = e._signal(make_input(), NP.anchor_avoider, 30.0)
    assert "Anchor avoider" in s

def test_signal_deadline_capitulator_label():
    e = eng()
    s = e._signal(make_input(), NP.deadline_capitulator, 25.0)
    assert "Deadline capitulator" in s

def test_signal_bundler_destroyer_label():
    e = eng()
    s = e._signal(make_input(), NP.bundler_destroyer, 22.0)
    assert "Bundler destroyer" in s

def test_signal_first_mover_label():
    e = eng()
    s = e._signal(make_input(), NP.first_mover_conceder, 30.0)
    assert "First-mover conceder" in s

# ---------------------------------------------------------------------------
# assess() integration
# ---------------------------------------------------------------------------

def test_assess_returns_result(): assert isinstance(eng().assess(make_input()), NegotiationResult)
def test_assess_rep_id(): assert eng().assess(make_input(rep_id="R1")).rep_id == "R1"
def test_assess_region(): assert eng().assess(make_input(region="APAC")).region == "APAC"
def test_assess_low_defaults(): r = eng().assess(make_input()); assert r.negotiation_risk == NR.low; assert r.recommended_action == NA.no_action
def test_assess_scores_non_negative():
    r = eng().assess(make_input())
    assert all(s >= 0 for s in [r.discipline_score, r.leverage_score, r.preparation_score, r.value_anchoring_score])
def test_assess_composite_range(): r = eng().assess(make_input()); assert 0 <= r.negotiation_composite <= 100
def test_assess_stores_result(): e = eng(); e.assess(make_input()); assert len(e._results) == 1
def test_assess_multiple_stored(): e = eng(); [e.assess(make_input(rep_id=f"R{i}")) for i in range(3)]; assert len(e._results) == 3

def test_assess_critical():
    inp = make_input(first_concession_without_ask_pct=0.60, price_anchor_usage_rate_pct=0.10,
                     avg_concession_rounds_per_deal=5.0, concession_size_avg_pct=0.20,
                     deal_closed_below_floor_price_pct=0.35, multi_element_trade_rate_pct=0.10,
                     deadline_pressure_concession_pct=0.65, procurement_win_rate_pct=0.10,
                     negotiation_preparation_score=0.10, walk_away_rate_pct=0.01,
                     legal_hold_up_capitulation_pct=0.60, competitor_price_match_rate_pct=0.60,
                     value_selling_score=0.10)
    r = eng().assess(inp)
    assert r.negotiation_risk == NR.critical
    assert r.negotiation_severity == NS.collapsing

def test_assess_moderate():
    inp = make_input(first_concession_without_ask_pct=0.32, deal_closed_below_floor_price_pct=0.15,
                     multi_element_trade_rate_pct=0.90, avg_concession_rounds_per_deal=1.5,
                     deadline_pressure_concession_pct=0.30, procurement_win_rate_pct=0.90,
                     negotiation_preparation_score=0.70, walk_away_rate_pct=0.06,
                     legal_hold_up_capitulation_pct=0.00, price_anchor_usage_rate_pct=0.90,
                     competitor_price_match_rate_pct=0.00, value_selling_score=0.90)
    assert eng().assess(inp).negotiation_risk == NR.moderate

@pytest.mark.parametrize("rep_id,region", [("A","EMEA"),("B","APAC"),("C","AMER"),("D","LATAM"),("E","MEA")])
def test_identity_passthrough(rep_id, region):
    r = eng().assess(make_input(rep_id=rep_id, region=region))
    assert r.rep_id == rep_id and r.region == region
    assert r.to_dict()["rep_id"] == rep_id and r.to_dict()["region"] == region

# ---------------------------------------------------------------------------
# assess_batch
# ---------------------------------------------------------------------------

def test_batch_list(): assert isinstance(eng().assess_batch([make_input()]), list)
def test_batch_count(): assert len(eng().assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])) == 5
def test_batch_empty(): assert eng().assess_batch([]) == []
def test_batch_all_results(): assert all(isinstance(r, NegotiationResult) for r in eng().assess_batch([make_input(rep_id=f"R{i}") for i in range(3)]))
def test_batch_stores_all(): e = eng(); e.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)]); assert len(e._results) == 4
def test_batch_order_preserved():
    ids = ["X","Y","Z"]
    assert [r.rep_id for r in eng().assess_batch([make_input(rep_id=i) for i in ids])] == ids

# ---------------------------------------------------------------------------
# summary()
# ---------------------------------------------------------------------------

SUMMARY_KEYS = {"total","risk_counts","pattern_counts","severity_counts","action_counts","avg_negotiation_composite","negotiation_gap_count","coaching_count","avg_discipline_score","avg_leverage_score","avg_preparation_score","avg_value_anchoring_score","total_estimated_margin_left_usd"}

def test_summary_empty_keys(): assert set(eng().summary()) == SUMMARY_KEYS
def test_summary_key_count(): assert len(eng().summary()) == 13
def test_summary_empty_total(): assert eng().summary()["total"] == 0
def test_summary_empty_gap(): assert eng().summary()["negotiation_gap_count"] == 0
def test_summary_empty_coaching(): assert eng().summary()["coaching_count"] == 0
def test_summary_empty_margin(): assert eng().summary()["total_estimated_margin_left_usd"] == 0.0
def test_summary_empty_composite(): assert eng().summary()["avg_negotiation_composite"] == 0.0

def test_summary_after_one():
    e = eng(); e.assess(make_input()); s = e.summary()
    assert s["total"] == 1 and "low" in s["risk_counts"]

def test_summary_risk_counts():
    e = eng(); e.assess(make_input()); s = e.summary()
    assert s["risk_counts"]["low"] == 1

def test_summary_pattern_counts():
    e = eng(); e.assess(make_input()); s = e.summary()
    assert sum(s["pattern_counts"].values()) == 1

def test_summary_severity_counts():
    e = eng(); e.assess(make_input()); s = e.summary()
    assert sum(s["severity_counts"].values()) == 1

def test_summary_action_counts():
    e = eng(); e.assess(make_input()); s = e.summary()
    assert sum(s["action_counts"].values()) == 1

def test_summary_five_total():
    e = eng(); [e.assess(make_input(rep_id=f"R{i}")) for i in range(5)]
    assert e.summary()["total"] == 5

def test_summary_margin_sum():
    e = eng()
    r1 = e.assess(make_input(total_closed_deals=10))
    r2 = e.assess(make_input(total_closed_deals=20))
    s = e.summary()
    assert s["total_estimated_margin_left_usd"] == round(r1.estimated_margin_left_usd + r2.estimated_margin_left_usd, 2)

def test_summary_avg_composite_type():
    e = eng(); e.assess(make_input())
    assert isinstance(e.summary()["avg_negotiation_composite"], float)

def test_summary_avg_discipline_type():
    e = eng(); e.assess(make_input())
    assert isinstance(e.summary()["avg_discipline_score"], float)

def test_summary_avg_leverage_type():
    e = eng(); e.assess(make_input())
    assert isinstance(e.summary()["avg_leverage_score"], float)

def test_summary_avg_preparation_type():
    e = eng(); e.assess(make_input())
    assert isinstance(e.summary()["avg_preparation_score"], float)

def test_summary_avg_va_type():
    e = eng(); e.assess(make_input())
    assert isinstance(e.summary()["avg_value_anchoring_score"], float)

def test_summary_multiple_risk_buckets():
    e = eng()
    e.assess(make_input())
    e.assess(make_input(first_concession_without_ask_pct=0.60, price_anchor_usage_rate_pct=0.10,
                        avg_concession_rounds_per_deal=5.0, deal_closed_below_floor_price_pct=0.35,
                        multi_element_trade_rate_pct=0.10, deadline_pressure_concession_pct=0.65,
                        procurement_win_rate_pct=0.10, negotiation_preparation_score=0.10,
                        walk_away_rate_pct=0.01, legal_hold_up_capitulation_pct=0.60,
                        competitor_price_match_rate_pct=0.60, value_selling_score=0.10))
    s = e.summary()
    assert s["total"] == 2 and len(s["risk_counts"]) >= 2

def test_summary_gap_count_accumulates():
    e = eng()
    e.assess(make_input(final_price_vs_list_pct=0.70))  # has gap
    e.assess(make_input())  # may or may not
    s = e.summary()
    assert s["negotiation_gap_count"] >= 1

def test_summary_coaching_count_accumulates():
    e = eng()
    e.assess(make_input(price_anchor_usage_rate_pct=0.30))  # needs coaching
    s = e.summary()
    assert s["coaching_count"] >= 1

# ---------------------------------------------------------------------------
# Full end-to-end scenario parametrize
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("first,floor,multi,rounds,deadline,proc,prep,walk,legal,anchor,cmatch,vscore,expected_risk", [
    # low risk
    (0.00,0.00,0.90,1.0,0.00,0.90,0.90,0.15,0.00,0.90,0.00,0.90, NR.low),
    # moderate (di=40,le=25,pr=26,va=0 → 24.75)
    (0.32,0.15,0.90,1.5,0.30,0.90,0.70,0.06,0.00,0.90,0.00,0.90, NR.moderate),
    # critical
    (0.60,0.35,0.10,5.0,0.65,0.10,0.10,0.01,0.60,0.10,0.60,0.10, NR.critical),
])
def test_e2e_risk(first,floor,multi,rounds,deadline,proc,prep,walk,legal,anchor,cmatch,vscore,expected_risk):
    e = eng()
    inp = make_input(first_concession_without_ask_pct=first, deal_closed_below_floor_price_pct=floor,
                     multi_element_trade_rate_pct=multi, avg_concession_rounds_per_deal=rounds,
                     deadline_pressure_concession_pct=deadline, procurement_win_rate_pct=proc,
                     negotiation_preparation_score=prep, walk_away_rate_pct=walk,
                     legal_hold_up_capitulation_pct=legal, price_anchor_usage_rate_pct=anchor,
                     competitor_price_match_rate_pct=cmatch, value_selling_score=vscore)
    assert e.assess(inp).negotiation_risk == expected_risk


# ---------------------------------------------------------------------------
# Additional parametrize — sub-score additive combinations
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("first,floor,multi,exp", [
    (0.55,0.30,0.10,100.0),(0.55,0.30,0.90,75.0),(0.55,0.00,0.10,65.0),(0.00,0.30,0.10,60.0),
    (0.32,0.15,0.21,52.0),(0.32,0.00,0.20,47.0),(0.15,0.15,0.30,38.0),(0.15,0.00,0.20,33.0),
    (0.00,0.15,0.20,43.0),(0.00,0.00,0.20,25.0),(0.00,0.00,0.45,12.0),(0.55,0.15,0.90,58.0),
    (0.32,0.30,0.90,57.0),(0.15,0.30,0.90,43.0),
])
def test_discipline_additive(first, floor, multi, exp):
    assert eng()._discipline_score(make_input(first_concession_without_ask_pct=first, deal_closed_below_floor_price_pct=floor, multi_element_trade_rate_pct=multi)) == exp

@pytest.mark.parametrize("rounds,deadline,proc,exp", [
    (4.0,0.55,0.25,100.0),(4.0,0.55,0.90,75.0),(4.0,0.00,0.25,70.0),(1.0,0.55,0.25,55.0),
    (2.5,0.30,0.40,52.0),(2.5,0.00,0.25,50.0),(1.5,0.30,0.40,37.0),(1.5,0.00,0.25,35.0),
    (1.0,0.30,0.25,40.0),(1.0,0.00,0.25,25.0),(1.0,0.00,0.40,12.0),(4.0,0.30,0.90,60.0),
    (2.5,0.55,0.90,55.0),(1.5,0.55,0.90,40.0),
])
def test_leverage_additive(rounds, deadline, proc, exp):
    assert eng()._leverage_score(make_input(avg_concession_rounds_per_deal=rounds, deadline_pressure_concession_pct=deadline, procurement_win_rate_pct=proc)) == exp

@pytest.mark.parametrize("prep,walk,legal,exp", [
    (0.25,0.02,0.55,100.0),(0.25,0.02,0.00,75.0),(0.25,0.20,0.55,65.0),(0.90,0.02,0.55,60.0),
    (0.50,0.06,0.30,52.0),(0.50,0.20,0.55,47.0),(0.70,0.06,0.30,38.0),(0.70,0.20,0.55,33.0),
    (0.90,0.06,0.55,43.0),(0.90,0.20,0.55,25.0),(0.90,0.20,0.30,12.0),(0.25,0.06,0.00,58.0),
    (0.50,0.02,0.00,57.0),(0.70,0.02,0.00,43.0),
])
def test_preparation_additive(prep, walk, legal, exp):
    assert eng()._preparation_score(make_input(negotiation_preparation_score=prep, walk_away_rate_pct=walk, legal_hold_up_capitulation_pct=legal)) == exp

@pytest.mark.parametrize("anchor,cmatch,vscore,exp", [
    (0.20,0.55,0.25,100.0),(0.20,0.55,0.90,75.0),(0.20,0.00,0.25,70.0),(0.90,0.55,0.25,55.0),
    (0.45,0.30,0.55,52.0),(0.45,0.00,0.25,50.0),(0.65,0.30,0.55,37.0),(0.65,0.00,0.25,35.0),
    (0.90,0.30,0.25,40.0),(0.90,0.00,0.25,25.0),(0.90,0.00,0.55,12.0),(0.20,0.30,0.90,60.0),
    (0.45,0.55,0.90,55.0),(0.65,0.55,0.90,40.0),
])
def test_va_additive(anchor, cmatch, vscore, exp):
    assert eng()._value_anchoring_score(make_input(price_anchor_usage_rate_pct=anchor, competitor_price_match_rate_pct=cmatch, value_selling_score=vscore)) == exp
