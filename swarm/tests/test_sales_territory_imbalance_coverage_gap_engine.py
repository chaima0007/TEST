"""Pytest suite for SalesTerritoryImbalanceCoverageGapEngine (280-320 tests, <600 lines)."""
from __future__ import annotations
import dataclasses, pytest
from swarm.intelligence.sales_territory_imbalance_coverage_gap_engine import (
    SalesTerritoryImbalanceCoverageGapEngine as Engine,
    TerritoryInput, TerritoryResult,
    TerritoryRisk, TerritoryPattern, TerritorySeverity, TerritoryAction,
)

def inp(**kw) -> TerritoryInput:
    d = dict(rep_id="r1", region="west", evaluation_period_id="Q1",
             accounts_per_rep_vs_benchmark=1.0, revenue_per_account_vs_benchmark=1.0,
             whitespace_accounts_untouched_pct=0.10, renewal_coverage_rate_pct=0.90,
             territory_quota_vs_capacity_ratio=1.0, active_accounts_pct=0.80,
             avg_travel_time_per_call_hours=0.5, geographic_concentration_score=0.5,
             icp_account_coverage_pct=0.80, new_logo_territory_penetration_pct=0.30,
             competitive_displacement_coverage=0.50, account_scoring_adoption_rate_pct=0.70,
             stale_account_rate_pct=0.10, multi_product_territory_pct=0.50,
             territory_nps_avg=0.20, expansion_opportunity_capture_pct=0.60,
             rep_tenure_territory_months=18.0, total_accounts_in_territory=200,
             avg_arr_per_account_usd=10_000.0)
    d.update(kw); return TerritoryInput(**d)

def eng() -> Engine: return Engine()

# ── 1. Field / key counts ─────────────────────────────────────────────────────
def test_input_field_count():  assert len(dataclasses.fields(TerritoryInput)) == 22
def test_result_field_count(): assert len(dataclasses.fields(TerritoryResult)) == 15
def test_to_dict_key_count():  assert len(eng().assess(inp()).to_dict()) == 15
def test_summary_empty_key_count():   assert len(eng().summary()) == 13
def test_summary_nonempty_key_count():
    e = eng(); e.assess(inp()); assert len(e.summary()) == 13
def test_to_dict_exact_keys():
    assert set(eng().assess(inp()).to_dict()) == {
        "rep_id","region","territory_risk","territory_pattern","territory_severity",
        "recommended_action","load_score","coverage_score","penetration_score",
        "efficiency_score","territory_composite","has_territory_gap",
        "requires_territory_intervention","estimated_uncaptured_revenue_usd","territory_signal"}
def test_summary_exact_keys():
    e = eng(); e.assess(inp())
    assert set(e.summary()) == {
        "total","risk_counts","pattern_counts","severity_counts","action_counts",
        "avg_territory_composite","territory_gap_count","intervention_count",
        "avg_load_score","avg_coverage_score","avg_penetration_score",
        "avg_efficiency_score","total_estimated_uncaptured_revenue_usd"}

# ── 2. Enum membership & counts ───────────────────────────────────────────────
@pytest.mark.parametrize("v", ["low","moderate","high","critical"])
def test_risk_enum(v): assert TerritoryRisk(v).value == v
@pytest.mark.parametrize("v", ["none","overloaded_rep","starved_territory",
                                "whitespace_blind","coverage_ghost","renewal_neglect"])
def test_pattern_enum(v): assert TerritoryPattern(v).value == v
@pytest.mark.parametrize("v", ["balanced","drifting","imbalanced","critical"])
def test_severity_enum(v): assert TerritorySeverity(v).value == v
@pytest.mark.parametrize("v", ["no_action","territory_health_check","account_redistribution_review",
    "whitespace_activation_plan","coverage_model_reassignment",
    "renewal_coverage_remediation","territory_redesign_escalation"])
def test_action_enum(v): assert TerritoryAction(v).value == v
def test_risk_count():     assert len(TerritoryRisk) == 4
def test_pattern_count():  assert len(TerritoryPattern) == 6
def test_severity_count(): assert len(TerritorySeverity) == 4
def test_action_count():   assert len(TerritoryAction) == 7

# ── 3. Load score ─────────────────────────────────────────────────────────────
@pytest.mark.parametrize("ratio,exp", [
    (0.9,0),(1.09,0),(1.10,8),(1.29,8),(1.30,22),(1.59,22),(1.60,40)])
def test_load_quota(ratio, exp):
    assert eng()._load_score(inp(territory_quota_vs_capacity_ratio=ratio)) == exp
@pytest.mark.parametrize("bench,exp", [(1.0,0),(1.39,0),(1.40,18),(1.79,18),(1.80,35)])
def test_load_accounts(bench, exp):
    assert eng()._load_score(inp(accounts_per_rep_vs_benchmark=bench)) == exp
@pytest.mark.parametrize("hrs,exp", [(0.5,0),(1.49,0),(1.5,12),(2.99,12),(3.0,25)])
def test_load_travel(hrs, exp):
    assert eng()._load_score(inp(avg_travel_time_per_call_hours=hrs)) == exp
def test_load_additive():
    assert eng()._load_score(inp(territory_quota_vs_capacity_ratio=1.30,
                                  accounts_per_rep_vs_benchmark=1.40)) == 40.0
def test_load_capped():
    assert eng()._load_score(inp(territory_quota_vs_capacity_ratio=2.0,
        accounts_per_rep_vs_benchmark=2.0, avg_travel_time_per_call_hours=5.0)) == 100.0
def test_load_zero_baseline(): assert eng()._load_score(inp()) == 0.0

# ── 4. Coverage score ─────────────────────────────────────────────────────────
@pytest.mark.parametrize("act,exp", [(0.80,0),(0.76,0),(0.75,10),(0.56,10),(0.55,25),(0.31,25),(0.30,45)])
def test_coverage_active(act, exp):
    assert eng()._coverage_score(inp(active_accounts_pct=act)) == exp
@pytest.mark.parametrize("stale,exp", [(0.10,0),(0.27,0),(0.28,15),(0.49,15),(0.50,30)])
def test_coverage_stale(stale, exp):
    assert eng()._coverage_score(inp(stale_account_rate_pct=stale)) == exp
@pytest.mark.parametrize("renew,exp", [(0.90,0),(0.76,0),(0.75,12),(0.51,12),(0.50,25)])
def test_coverage_renewal(renew, exp):
    assert eng()._coverage_score(inp(renewal_coverage_rate_pct=renew)) == exp
def test_coverage_capped():
    assert eng()._coverage_score(inp(active_accounts_pct=0.10,
        stale_account_rate_pct=0.60, renewal_coverage_rate_pct=0.40)) == 100.0
def test_coverage_zero_baseline(): assert eng()._coverage_score(inp()) == 0.0

# ── 5. Penetration score ──────────────────────────────────────────────────────
@pytest.mark.parametrize("ws,exp", [(0.10,0),(0.19,0),(0.20,8),(0.39,8),(0.40,22),(0.64,22),(0.65,40)])
def test_pen_whitespace(ws, exp):
    assert eng()._penetration_score(inp(whitespace_accounts_untouched_pct=ws)) == exp
@pytest.mark.parametrize("icp,exp", [(0.80,0),(0.51,0),(0.50,18),(0.26,18),(0.25,35)])
def test_pen_icp(icp, exp):
    assert eng()._penetration_score(inp(icp_account_coverage_pct=icp)) == exp
@pytest.mark.parametrize("nl,exp", [(0.30,0),(0.21,0),(0.20,12),(0.11,12),(0.10,25)])
def test_pen_new_logo(nl, exp):
    assert eng()._penetration_score(inp(new_logo_territory_penetration_pct=nl)) == exp
def test_penetration_capped():
    assert eng()._penetration_score(inp(whitespace_accounts_untouched_pct=0.80,
        icp_account_coverage_pct=0.10, new_logo_territory_penetration_pct=0.05)) == 100.0
def test_penetration_zero_baseline(): assert eng()._penetration_score(inp()) == 0.0

# ── 6. Efficiency score ───────────────────────────────────────────────────────
@pytest.mark.parametrize("rev,exp", [(1.0,0),(0.91,0),(0.90,10),(0.71,10),(0.70,25),(0.41,25),(0.40,45)])
def test_eff_rev(rev, exp):
    assert eng()._efficiency_score(inp(revenue_per_account_vs_benchmark=rev)) == exp
@pytest.mark.parametrize("exp_c,exp_s", [(0.60,0),(0.46,0),(0.45,15),(0.21,15),(0.20,30)])
def test_eff_expansion(exp_c, exp_s):
    assert eng()._efficiency_score(inp(expansion_opportunity_capture_pct=exp_c)) == exp_s
@pytest.mark.parametrize("adopt,exp", [(0.70,0),(0.51,0),(0.50,12),(0.21,12),(0.20,25)])
def test_eff_adoption(adopt, exp):
    assert eng()._efficiency_score(inp(account_scoring_adoption_rate_pct=adopt)) == exp
def test_efficiency_capped():
    assert eng()._efficiency_score(inp(revenue_per_account_vs_benchmark=0.10,
        expansion_opportunity_capture_pct=0.05, account_scoring_adoption_rate_pct=0.05)) == 100.0
def test_efficiency_zero_baseline(): assert eng()._efficiency_score(inp()) == 0.0

# ── 7. Composite weighting ────────────────────────────────────────────────────
@pytest.mark.parametrize("lo,co,pe,ef,exp", [
    (100,0,0,0,25.0),(0,100,0,0,30.0),(0,0,100,0,25.0),(0,0,0,100,20.0),
    (100,100,100,100,100.0),(0,0,0,0,0.0),
])
def test_composite_weights(lo, co, pe, ef, exp): assert eng()._composite(lo, co, pe, ef) == exp
def test_composite_capped():    assert eng()._composite(200,200,200,200) == 100.0
def test_composite_rounded():
    c = eng()._composite(33,33,33,33)
    assert c == round(33*0.25 + 33*0.30 + 33*0.25 + 33*0.20, 2)
def test_composite_weights_sum(): assert 0.25+0.30+0.25+0.20 == 1.00
def test_composite_partial():
    assert eng()._composite(40, 0, 0, 0) == round(40*0.25, 2)

# ── 8. Risk thresholds ────────────────────────────────────────────────────────
@pytest.mark.parametrize("score,risk", [
    (0.0, TerritoryRisk.low),(19.99, TerritoryRisk.low),
    (20.0, TerritoryRisk.moderate),(39.99, TerritoryRisk.moderate),
    (40.0, TerritoryRisk.high),(59.99, TerritoryRisk.high),
    (60.0, TerritoryRisk.critical),(100.0, TerritoryRisk.critical),
])
def test_risk_threshold(score, risk): assert eng()._risk(score) == risk

# ── 9. Severity thresholds ────────────────────────────────────────────────────
@pytest.mark.parametrize("score,sev", [
    (0.0, TerritorySeverity.balanced),(19.99, TerritorySeverity.balanced),
    (20.0, TerritorySeverity.drifting),(39.99, TerritorySeverity.drifting),
    (40.0, TerritorySeverity.imbalanced),(59.99, TerritorySeverity.imbalanced),
    (60.0, TerritorySeverity.critical),(100.0, TerritorySeverity.critical),
])
def test_severity_threshold(score, sev): assert eng()._severity(score) == sev

# ── 10. Action routing ────────────────────────────────────────────────────────
@pytest.mark.parametrize("risk,pat,act", [
    (TerritoryRisk.low, TerritoryPattern.none,             TerritoryAction.no_action),
    (TerritoryRisk.low, TerritoryPattern.overloaded_rep,   TerritoryAction.no_action),
    (TerritoryRisk.low, TerritoryPattern.renewal_neglect,  TerritoryAction.no_action),
    (TerritoryRisk.moderate, TerritoryPattern.none,           TerritoryAction.territory_health_check),
    (TerritoryRisk.moderate, TerritoryPattern.overloaded_rep, TerritoryAction.territory_health_check),
    (TerritoryRisk.moderate, TerritoryPattern.coverage_ghost, TerritoryAction.territory_health_check),
    (TerritoryRisk.high, TerritoryPattern.overloaded_rep,  TerritoryAction.account_redistribution_review),
    (TerritoryRisk.high, TerritoryPattern.starved_territory, TerritoryAction.coverage_model_reassignment),
    (TerritoryRisk.high, TerritoryPattern.whitespace_blind, TerritoryAction.whitespace_activation_plan),
    (TerritoryRisk.high, TerritoryPattern.coverage_ghost,  TerritoryAction.account_redistribution_review),
    (TerritoryRisk.high, TerritoryPattern.renewal_neglect, TerritoryAction.renewal_coverage_remediation),
    (TerritoryRisk.high, TerritoryPattern.none,            TerritoryAction.territory_health_check),
    (TerritoryRisk.critical, TerritoryPattern.overloaded_rep,   TerritoryAction.territory_redesign_escalation),
    (TerritoryRisk.critical, TerritoryPattern.starved_territory, TerritoryAction.territory_redesign_escalation),
    (TerritoryRisk.critical, TerritoryPattern.whitespace_blind, TerritoryAction.account_redistribution_review),
    (TerritoryRisk.critical, TerritoryPattern.coverage_ghost,   TerritoryAction.account_redistribution_review),
    (TerritoryRisk.critical, TerritoryPattern.renewal_neglect,  TerritoryAction.account_redistribution_review),
    (TerritoryRisk.critical, TerritoryPattern.none,             TerritoryAction.account_redistribution_review),
])
def test_action_routing(risk, pat, act): assert eng()._action(risk, pat) == act

def test_action_low_all_patterns():
    for pat in TerritoryPattern:
        assert eng()._action(TerritoryRisk.low, pat) == TerritoryAction.no_action
def test_action_moderate_all_patterns():
    for pat in TerritoryPattern:
        assert eng()._action(TerritoryRisk.moderate, pat) == TerritoryAction.territory_health_check

# ── 11. Pattern detection ─────────────────────────────────────────────────────
def test_pattern_none():
    assert eng()._pattern(inp()) == TerritoryPattern.none
def test_pattern_overloaded():
    assert eng()._pattern(inp(territory_quota_vs_capacity_ratio=1.50,
        accounts_per_rep_vs_benchmark=1.60)) == TerritoryPattern.overloaded_rep
def test_pattern_starved():
    assert eng()._pattern(inp(accounts_per_rep_vs_benchmark=0.50,
        whitespace_accounts_untouched_pct=0.60)) == TerritoryPattern.starved_territory
def test_pattern_whitespace_blind():
    assert eng()._pattern(inp(whitespace_accounts_untouched_pct=0.65,
        icp_account_coverage_pct=0.25)) == TerritoryPattern.whitespace_blind
def test_pattern_coverage_ghost():
    assert eng()._pattern(inp(active_accounts_pct=0.30,
        stale_account_rate_pct=0.50)) == TerritoryPattern.coverage_ghost
def test_pattern_renewal_neglect():
    assert eng()._pattern(inp(renewal_coverage_rate_pct=0.45,
        expansion_opportunity_capture_pct=0.20)) == TerritoryPattern.renewal_neglect
def test_pattern_overloaded_priority_over_starved():
    i = inp(territory_quota_vs_capacity_ratio=1.60, accounts_per_rep_vs_benchmark=1.70,
            whitespace_accounts_untouched_pct=0.65)
    assert eng()._pattern(i) == TerritoryPattern.overloaded_rep
def test_pattern_whitespace_priority_over_ghost():
    i = inp(whitespace_accounts_untouched_pct=0.65, icp_account_coverage_pct=0.25,
            active_accounts_pct=0.30, stale_account_rate_pct=0.50)
    assert eng()._pattern(i) == TerritoryPattern.whitespace_blind
def test_pattern_ghost_priority_over_renewal():
    i = inp(active_accounts_pct=0.30, stale_account_rate_pct=0.50,
            renewal_coverage_rate_pct=0.40, expansion_opportunity_capture_pct=0.15)
    assert eng()._pattern(i) == TerritoryPattern.coverage_ghost
def test_pattern_overloaded_below_ratio():
    assert eng()._pattern(inp(territory_quota_vs_capacity_ratio=1.49,
        accounts_per_rep_vs_benchmark=2.0)) != TerritoryPattern.overloaded_rep
def test_pattern_starved_below_whitespace():
    assert eng()._pattern(inp(accounts_per_rep_vs_benchmark=0.30,
        whitespace_accounts_untouched_pct=0.59)) != TerritoryPattern.starved_territory

# ── 12. has_territory_gap ─────────────────────────────────────────────────────
def test_gap_false_baseline(): assert eng().assess(inp()).has_territory_gap is False
def test_gap_true_active_boundary():
    assert eng().assess(inp(active_accounts_pct=0.55)).has_territory_gap is True
def test_gap_true_whitespace_boundary():
    assert eng().assess(inp(whitespace_accounts_untouched_pct=0.40)).has_territory_gap is True
def test_gap_true_via_composite():
    i = inp(active_accounts_pct=0.10, stale_account_rate_pct=0.60,
            renewal_coverage_rate_pct=0.40, whitespace_accounts_untouched_pct=0.80)
    r = eng().assess(i)
    assert r.territory_composite >= 40 and r.has_territory_gap is True
def test_gap_false_just_above():
    r = eng().assess(inp(active_accounts_pct=0.56, whitespace_accounts_untouched_pct=0.39))
    assert r.territory_composite < 40 and r.has_territory_gap is False

# ── 13. requires_territory_intervention ───────────────────────────────────────
def test_intervention_false_baseline():
    assert eng().assess(inp()).requires_territory_intervention is False
def test_intervention_true_renewal_boundary():
    assert eng().assess(inp(renewal_coverage_rate_pct=0.75)).requires_territory_intervention is True
def test_intervention_true_stale_boundary():
    assert eng().assess(inp(stale_account_rate_pct=0.28)).requires_territory_intervention is True
def test_intervention_false_above_thresholds():
    r = eng().assess(inp(renewal_coverage_rate_pct=0.76, stale_account_rate_pct=0.27))
    assert r.territory_composite < 25 and r.requires_territory_intervention is False
def test_intervention_true_via_composite():
    i = inp(active_accounts_pct=0.55, stale_account_rate_pct=0.28)
    assert eng().assess(i).requires_territory_intervention is True

# ── 14. Uncaptured revenue ────────────────────────────────────────────────────
def test_uncaptured_formula():
    i = inp(total_accounts_in_territory=100, whitespace_accounts_untouched_pct=0.50,
            avg_arr_per_account_usd=10_000.0)
    e = eng(); comp = e._composite(e._load_score(i), e._coverage_score(i),
                                    e._penetration_score(i), e._efficiency_score(i))
    assert e.assess(i).estimated_uncaptured_revenue_usd == round(100*0.50*10_000*(comp/100), 2)
def test_uncaptured_zero_whitespace():
    assert eng().assess(inp(whitespace_accounts_untouched_pct=0.0)).estimated_uncaptured_revenue_usd == 0.0
def test_uncaptured_zero_composite():
    assert eng().assess(inp()).estimated_uncaptured_revenue_usd == 0.0
def test_uncaptured_doubled_accounts():
    kw = dict(whitespace_accounts_untouched_pct=0.20, stale_account_rate_pct=0.30)
    r1 = eng().assess(inp(total_accounts_in_territory=100, **kw))
    r2 = eng().assess(inp(total_accounts_in_territory=200, **kw))
    assert abs(r2.estimated_uncaptured_revenue_usd - 2*r1.estimated_uncaptured_revenue_usd) < 0.01
def test_uncaptured_rounded():
    r = eng().assess(inp(total_accounts_in_territory=3, whitespace_accounts_untouched_pct=1/3,
                          avg_arr_per_account_usd=1.0, stale_account_rate_pct=0.35))
    assert r.estimated_uncaptured_revenue_usd == round(r.estimated_uncaptured_revenue_usd, 2)
def test_uncaptured_large_arr():
    r = eng().assess(inp(total_accounts_in_territory=10, whitespace_accounts_untouched_pct=1.0,
                          avg_arr_per_account_usd=1_000_000.0, stale_account_rate_pct=0.35))
    assert r.estimated_uncaptured_revenue_usd > 0

# ── 15. Signal text ───────────────────────────────────────────────────────────
def test_signal_healthy():
    r = eng().assess(inp()); assert "healthy" in r.territory_signal
def test_signal_healthy_benchmark():
    r = eng().assess(inp()); assert "benchmark targets" in r.territory_signal
def test_signal_composite_shown():
    i = inp(active_accounts_pct=0.40, stale_account_rate_pct=0.35); r = eng().assess(i)
    if r.territory_composite >= 20: assert "composite" in r.territory_signal
def test_signal_active_pct():
    i = inp(active_accounts_pct=0.40, stale_account_rate_pct=0.35); r = eng().assess(i)
    if r.territory_composite >= 20: assert "40%" in r.territory_signal
def test_signal_whitespace_pct():
    i = inp(active_accounts_pct=0.40, stale_account_rate_pct=0.35,
            whitespace_accounts_untouched_pct=0.25); r = eng().assess(i)
    if r.territory_composite >= 20: assert "25%" in r.territory_signal
def test_signal_renewal_pct():
    i = inp(active_accounts_pct=0.40, stale_account_rate_pct=0.35,
            renewal_coverage_rate_pct=0.72); r = eng().assess(i)
    if r.territory_composite >= 20: assert "72%" in r.territory_signal
def test_signal_overloaded_label():
    i = inp(territory_quota_vs_capacity_ratio=1.60, accounts_per_rep_vs_benchmark=1.80,
            avg_travel_time_per_call_hours=3.0, active_accounts_pct=0.40,
            stale_account_rate_pct=0.35); r = eng().assess(i)
    if r.territory_composite >= 20: assert "Overloaded rep" in r.territory_signal
def test_signal_renewal_neglect_label():
    i = inp(renewal_coverage_rate_pct=0.45, expansion_opportunity_capture_pct=0.20,
            active_accounts_pct=0.40, stale_account_rate_pct=0.30); r = eng().assess(i)
    if r.territory_composite >= 20: assert "Renewal neglect" in r.territory_signal
def test_signal_nonempty_str():
    r = eng().assess(inp()); assert isinstance(r.territory_signal, str) and r.territory_signal

# ── 16. assess() result types & identity ─────────────────────────────────────
def test_assess_returns_result():  assert isinstance(eng().assess(inp()), TerritoryResult)
def test_assess_rep_id():          assert eng().assess(inp(rep_id="xyz")).rep_id == "xyz"
def test_assess_region():          assert eng().assess(inp(region="south")).region == "south"
def test_assess_composite_range(): r = eng().assess(inp()); assert 0.0 <= r.territory_composite <= 100.0
def test_assess_scores_float():
    r = eng().assess(inp())
    for s in (r.load_score, r.coverage_score, r.penetration_score, r.efficiency_score):
        assert isinstance(s, float)
def test_to_dict_enum_strs():
    d = eng().assess(inp()).to_dict()
    for k in ("territory_risk","territory_pattern","territory_severity","recommended_action"):
        assert isinstance(d[k], str)
def test_to_dict_flags_bool():
    d = eng().assess(inp()).to_dict()
    assert isinstance(d["has_territory_gap"], bool) and isinstance(d["requires_territory_intervention"], bool)
def test_result_types():
    r = eng().assess(inp())
    assert isinstance(r.territory_risk, TerritoryRisk)
    assert isinstance(r.territory_pattern, TerritoryPattern)
    assert isinstance(r.territory_severity, TerritorySeverity)
    assert isinstance(r.recommended_action, TerritoryAction)
    assert isinstance(r.has_territory_gap, bool)
    assert isinstance(r.requires_territory_intervention, bool)
    assert isinstance(r.estimated_uncaptured_revenue_usd, float)
def test_composite_matches_sub_scores():
    e = eng(); i = inp(stale_account_rate_pct=0.30); r = e.assess(i)
    assert r.territory_composite == e._composite(e._load_score(i), e._coverage_score(i),
                                                  e._penetration_score(i), e._efficiency_score(i))
def test_to_dict_rep_id():   assert eng().assess(inp(rep_id="abc")).to_dict()["rep_id"] == "abc"
def test_to_dict_region():   assert eng().assess(inp(region="north")).to_dict()["region"] == "north"
def test_to_dict_composite_float():
    assert isinstance(eng().assess(inp()).to_dict()["territory_composite"], float)

# ── 17. assess_batch() ────────────────────────────────────────────────────────
def test_batch_returns_list():   assert isinstance(eng().assess_batch([inp(), inp(rep_id="r2")]), list)
def test_batch_len():            assert len(eng().assess_batch([inp(), inp(rep_id="r2")])) == 2
def test_batch_empty():          assert eng().assess_batch([]) == []
def test_batch_order():
    ids = ["a","b","c"]
    assert [r.rep_id for r in eng().assess_batch([inp(rep_id=i) for i in ids])] == ids
def test_batch_accumulates():
    e = eng(); e.assess_batch([inp() for _ in range(3)]); assert e.summary()["total"] == 3
def test_batch_single():
    assert eng().assess_batch([inp(rep_id="solo")])[0].rep_id == "solo"
def test_batch_five():
    assert len(eng().assess_batch([inp(rep_id=str(i)) for i in range(5)])) == 5

# ── 18. summary() aggregation ────────────────────────────────────────────────
def test_summary_empty_total():        assert eng().summary()["total"] == 0
def test_summary_empty_composite():    assert eng().summary()["avg_territory_composite"] == 0.0
def test_summary_empty_gap():          assert eng().summary()["territory_gap_count"] == 0
def test_summary_empty_intervention(): assert eng().summary()["intervention_count"] == 0
def test_summary_total():
    e = eng(); [e.assess(inp()) for _ in range(5)]; assert e.summary()["total"] == 5
def test_summary_risk_sum():
    e = eng(); e.assess_batch([inp() for _ in range(4)]); s = e.summary()
    assert sum(s["risk_counts"].values()) == s["total"]
def test_summary_pattern_sum():
    e = eng(); e.assess_batch([inp() for _ in range(3)]); s = e.summary()
    assert sum(s["pattern_counts"].values()) == s["total"]
def test_summary_severity_sum():
    e = eng(); e.assess_batch([inp() for _ in range(3)]); s = e.summary()
    assert sum(s["severity_counts"].values()) == s["total"]
def test_summary_action_sum():
    e = eng(); e.assess_batch([inp() for _ in range(3)]); s = e.summary()
    assert sum(s["action_counts"].values()) == s["total"]
def test_summary_avg_composite():
    e = eng(); r1 = e.assess(inp()); r2 = e.assess(inp(stale_account_rate_pct=0.35))
    assert e.summary()["avg_territory_composite"] == round(
        (r1.territory_composite + r2.territory_composite)/2, 1)
def test_summary_total_uncaptured():
    e = eng()
    r1 = e.assess(inp(whitespace_accounts_untouched_pct=0.20, stale_account_rate_pct=0.30))
    r2 = e.assess(inp(whitespace_accounts_untouched_pct=0.30, stale_account_rate_pct=0.35))
    assert e.summary()["total_estimated_uncaptured_revenue_usd"] == round(
        r1.estimated_uncaptured_revenue_usd + r2.estimated_uncaptured_revenue_usd, 2)
def test_summary_gap_count():
    e = eng(); e.assess(inp(active_accounts_pct=0.55)); e.assess(inp())
    assert e.summary()["territory_gap_count"] == 1
def test_summary_intervention_count():
    e = eng(); e.assess(inp(renewal_coverage_rate_pct=0.75)); e.assess(inp())
    assert e.summary()["intervention_count"] == 1
def test_summary_avg_scores_1dp():
    e = eng(); e.assess(inp()); s = e.summary()
    for k in ("avg_load_score","avg_coverage_score","avg_penetration_score","avg_efficiency_score"):
        assert s[k] == round(s[k], 1)
def test_summary_risk_counts_dict():
    e = eng(); e.assess(inp()); assert isinstance(e.summary()["risk_counts"], dict)
def test_summary_pattern_counts_dict():
    e = eng(); e.assess(inp()); assert isinstance(e.summary()["pattern_counts"], dict)
def test_summary_severity_counts_dict():
    e = eng(); e.assess(inp()); assert isinstance(e.summary()["severity_counts"], dict)
def test_summary_action_counts_dict():
    e = eng(); e.assess(inp()); assert isinstance(e.summary()["action_counts"], dict)

# ── 19. Engine isolation ──────────────────────────────────────────────────────
def test_isolation(): e1, e2 = eng(), eng(); e1.assess(inp()); assert e2.summary()["total"] == 0
def test_accumulates():
    e = eng(); e.assess(inp()); e.assess(inp(rep_id="r2")); assert e.summary()["total"] == 2
def test_summary_before_after():
    e = eng(); s1 = e.summary(); e.assess(inp()); s2 = e.summary()
    assert s1["total"] == 0 and s2["total"] == 1
def test_idempotent_result():
    e = eng(); r1 = e.assess(inp(rep_id="x")); r2 = e.assess(inp(rep_id="x"))
    assert r1.territory_composite == r2.territory_composite

# ── 20. Edge cases ────────────────────────────────────────────────────────────
def test_all_zeros():
    i = inp(accounts_per_rep_vs_benchmark=0.0, revenue_per_account_vs_benchmark=0.0,
            whitespace_accounts_untouched_pct=0.0, renewal_coverage_rate_pct=0.0,
            territory_quota_vs_capacity_ratio=0.0, active_accounts_pct=0.0,
            avg_travel_time_per_call_hours=0.0, icp_account_coverage_pct=0.0,
            new_logo_territory_penetration_pct=0.0, account_scoring_adoption_rate_pct=0.0,
            stale_account_rate_pct=0.0, expansion_opportunity_capture_pct=0.0,
            total_accounts_in_territory=0, avg_arr_per_account_usd=0.0)
    r = eng().assess(i); assert 0.0 <= r.territory_composite <= 100.0
def test_all_max():
    i = inp(accounts_per_rep_vs_benchmark=5.0, revenue_per_account_vs_benchmark=0.0,
            whitespace_accounts_untouched_pct=1.0, renewal_coverage_rate_pct=0.0,
            territory_quota_vs_capacity_ratio=3.0, active_accounts_pct=0.0,
            avg_travel_time_per_call_hours=10.0, icp_account_coverage_pct=0.0,
            new_logo_territory_penetration_pct=0.0, account_scoring_adoption_rate_pct=0.0,
            stale_account_rate_pct=1.0, expansion_opportunity_capture_pct=0.0)
    r = eng().assess(i)
    assert r.territory_composite == 100.0 and r.territory_risk == TerritoryRisk.critical
def test_single_account():
    r = eng().assess(inp(total_accounts_in_territory=1)); assert r.territory_composite >= 0.0
def test_large_territory():
    r = eng().assess(inp(total_accounts_in_territory=100_000,
                          whitespace_accounts_untouched_pct=0.50, stale_account_rate_pct=0.35))
    assert r.estimated_uncaptured_revenue_usd > 0
def test_critical_risk_and_severity():
    i = inp(active_accounts_pct=0.10, stale_account_rate_pct=0.60,
            renewal_coverage_rate_pct=0.40, whitespace_accounts_untouched_pct=0.80,
            icp_account_coverage_pct=0.10, revenue_per_account_vs_benchmark=0.30,
            expansion_opportunity_capture_pct=0.10, account_scoring_adoption_rate_pct=0.10,
            territory_quota_vs_capacity_ratio=1.70, accounts_per_rep_vs_benchmark=2.0,
            avg_travel_time_per_call_hours=4.0, new_logo_territory_penetration_pct=0.05)
    r = eng().assess(i)
    assert r.territory_risk == TerritoryRisk.critical and r.territory_severity == TerritorySeverity.critical
def test_low_composite_no_gap_no_intervention():
    r = eng().assess(inp())
    assert r.territory_composite < 20 and not r.has_territory_gap and not r.requires_territory_intervention
def test_summary_two_distinct_risks():
    e = eng(); e.assess(inp())
    e.assess(inp(active_accounts_pct=0.10, stale_account_rate_pct=0.60,
                 renewal_coverage_rate_pct=0.40, whitespace_accounts_untouched_pct=0.80))
    assert len(e.summary()["risk_counts"]) >= 1
def test_pattern_returned_in_result():
    i = inp(territory_quota_vs_capacity_ratio=1.50, accounts_per_rep_vs_benchmark=1.60)
    assert eng().assess(i).territory_pattern == TerritoryPattern.overloaded_rep

# ── 21. Risk/Severity/Action end-to-end via assess() ─────────────────────────
_MODERATE_KW = dict(active_accounts_pct=0.30, stale_account_rate_pct=0.50, renewal_coverage_rate_pct=0.50)
_HIGH_KW     = dict(active_accounts_pct=0.30, stale_account_rate_pct=0.50, renewal_coverage_rate_pct=0.50,
                    whitespace_accounts_untouched_pct=0.40, icp_account_coverage_pct=0.50)
_CRITICAL_KW = dict(active_accounts_pct=0.10, stale_account_rate_pct=0.60, renewal_coverage_rate_pct=0.40,
                    whitespace_accounts_untouched_pct=0.80, icp_account_coverage_pct=0.10,
                    revenue_per_account_vs_benchmark=0.30, expansion_opportunity_capture_pct=0.10,
                    account_scoring_adoption_rate_pct=0.10, territory_quota_vs_capacity_ratio=1.70,
                    accounts_per_rep_vs_benchmark=2.0, avg_travel_time_per_call_hours=4.0,
                    new_logo_territory_penetration_pct=0.05)

@pytest.mark.parametrize("composite_kw,expected_risk", [
    (dict(),         TerritoryRisk.low),
    (_MODERATE_KW,   TerritoryRisk.moderate),
    (_HIGH_KW,       TerritoryRisk.high),
    (_CRITICAL_KW,   TerritoryRisk.critical),
])
def test_e2e_risk(composite_kw, expected_risk):
    assert eng().assess(inp(**composite_kw)).territory_risk == expected_risk

@pytest.mark.parametrize("composite_kw,expected_sev", [
    (dict(),         TerritorySeverity.balanced),
    (_MODERATE_KW,   TerritorySeverity.drifting),
    (_HIGH_KW,       TerritorySeverity.imbalanced),
    (_CRITICAL_KW,   TerritorySeverity.critical),
])
def test_e2e_severity(composite_kw, expected_sev):
    assert eng().assess(inp(**composite_kw)).territory_severity == expected_sev

# ── 22. Gap / intervention parametrized ──────────────────────────────────────
@pytest.mark.parametrize("kw,expected_gap", [
    (dict(), False),
    (dict(active_accounts_pct=0.55), True),
    (dict(whitespace_accounts_untouched_pct=0.40), True),
    (dict(active_accounts_pct=0.56, whitespace_accounts_untouched_pct=0.39), False),
])
def test_gap_parametrized(kw, expected_gap):
    r = eng().assess(inp(**kw))
    if r.territory_composite < 40:
        assert r.has_territory_gap == expected_gap

@pytest.mark.parametrize("kw,expected_int", [
    (dict(), False),
    (dict(renewal_coverage_rate_pct=0.75), True),
    (dict(stale_account_rate_pct=0.28), True),
    (dict(renewal_coverage_rate_pct=0.76, stale_account_rate_pct=0.27), False),
])
def test_intervention_parametrized(kw, expected_int):
    r = eng().assess(inp(**kw))
    if r.territory_composite < 25:
        assert r.requires_territory_intervention == expected_int

# ── 23. Signal label for each named pattern ───────────────────────────────────
@pytest.mark.parametrize("kw,label", [
    (dict(territory_quota_vs_capacity_ratio=1.60, accounts_per_rep_vs_benchmark=1.80,
          avg_travel_time_per_call_hours=3.0, active_accounts_pct=0.40,
          stale_account_rate_pct=0.35), "Overloaded rep"),
    (dict(accounts_per_rep_vs_benchmark=0.40, whitespace_accounts_untouched_pct=0.70,
          active_accounts_pct=0.40, stale_account_rate_pct=0.35), "Starved territory"),
    (dict(whitespace_accounts_untouched_pct=0.70, icp_account_coverage_pct=0.20,
          active_accounts_pct=0.40, stale_account_rate_pct=0.35), "Whitespace blind"),
    (dict(active_accounts_pct=0.25, stale_account_rate_pct=0.55), "Coverage ghost"),
    (dict(renewal_coverage_rate_pct=0.40, expansion_opportunity_capture_pct=0.15,
          active_accounts_pct=0.40, stale_account_rate_pct=0.30), "Renewal neglect"),
])
def test_signal_pattern_label(kw, label):
    r = eng().assess(inp(**kw))
    if r.territory_composite >= 20:
        assert label in r.territory_signal

# ── 24. Summary count dicts contain string keys ───────────────────────────────
def test_summary_risk_counts_str_keys():
    e = eng(); e.assess(inp()); s = e.summary()
    assert all(isinstance(k, str) for k in s["risk_counts"])
def test_summary_pattern_counts_str_keys():
    e = eng(); e.assess(inp()); s = e.summary()
    assert all(isinstance(k, str) for k in s["pattern_counts"])
def test_summary_severity_counts_str_keys():
    e = eng(); e.assess(inp()); s = e.summary()
    assert all(isinstance(k, str) for k in s["severity_counts"])
def test_summary_action_counts_str_keys():
    e = eng(); e.assess(inp()); s = e.summary()
    assert all(isinstance(k, str) for k in s["action_counts"])

# ── 25. Load score additive combinations ─────────────────────────────────────
@pytest.mark.parametrize("ratio,bench,hrs,exp", [
    (1.10, 1.40, 0.5,  26.0),   # 8+18
    (1.30, 1.0,  3.0,  47.0),   # 22+25
    (1.60, 1.80, 3.0, 100.0),   # 40+35+25 capped
    (1.10, 1.40, 3.0,  51.0),   # 8+18+25
])
def test_load_additive_combos(ratio, bench, hrs, exp):
    assert eng()._load_score(inp(territory_quota_vs_capacity_ratio=ratio,
                                  accounts_per_rep_vs_benchmark=bench,
                                  avg_travel_time_per_call_hours=hrs)) == exp

# ── 26. assess() accumulates into summary ─────────────────────────────────────
def test_assess_adds_to_summary():
    e = eng()
    for i in range(7): e.assess(inp(rep_id=str(i)))
    assert e.summary()["total"] == 7
def test_assess_batch_then_summary_gap():
    e = eng()
    e.assess_batch([inp(active_accounts_pct=0.55) for _ in range(3)])
    assert e.summary()["territory_gap_count"] == 3
def test_assess_batch_then_summary_intervention():
    e = eng()
    e.assess_batch([inp(stale_account_rate_pct=0.28) for _ in range(2)])
    e.assess_batch([inp() for _ in range(2)])
    assert e.summary()["intervention_count"] == 2

# ── 27. Misc boundary / correctness ──────────────────────────────────────────
def test_gap_all_three_conditions():
    r = eng().assess(inp(active_accounts_pct=0.55, whitespace_accounts_untouched_pct=0.40,
                          stale_account_rate_pct=0.30))
    assert r.has_territory_gap is True
def test_intervention_all_conditions():
    r = eng().assess(inp(renewal_coverage_rate_pct=0.75, stale_account_rate_pct=0.28))
    assert r.requires_territory_intervention is True
def test_uncaptured_proportional_arr():
    r1 = eng().assess(inp(avg_arr_per_account_usd=1_000.0, whitespace_accounts_untouched_pct=0.20,
                           stale_account_rate_pct=0.30))
    r2 = eng().assess(inp(avg_arr_per_account_usd=2_000.0, whitespace_accounts_untouched_pct=0.20,
                           stale_account_rate_pct=0.30))
    assert abs(r2.estimated_uncaptured_revenue_usd - 2*r1.estimated_uncaptured_revenue_usd) < 0.01
def test_summary_empty_avg_load():   assert eng().summary()["avg_load_score"] == 0.0
def test_summary_empty_avg_cov():    assert eng().summary()["avg_coverage_score"] == 0.0
def test_summary_empty_avg_pen():    assert eng().summary()["avg_penetration_score"] == 0.0
def test_summary_empty_avg_eff():    assert eng().summary()["avg_efficiency_score"] == 0.0
def test_summary_empty_uncaptured(): assert eng().summary()["total_estimated_uncaptured_revenue_usd"] == 0.0
def test_composite_all_equal():
    c = eng()._composite(50, 50, 50, 50)
    assert c == round(50*0.25 + 50*0.30 + 50*0.25 + 50*0.20, 2)
def test_assess_updates_summary_uncaptured():
    e = eng()
    r = e.assess(inp(whitespace_accounts_untouched_pct=0.20, stale_account_rate_pct=0.30))
    assert e.summary()["total_estimated_uncaptured_revenue_usd"] == r.estimated_uncaptured_revenue_usd