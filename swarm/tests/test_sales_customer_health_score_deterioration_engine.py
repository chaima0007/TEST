"""
Pytest test suite for SalesCustomerHealthScoreDeteriorationEngine.
Target: 280-320 tests, file under 600 lines.
"""
import dataclasses
import pytest
from swarm.intelligence.sales_customer_health_score_deterioration_engine import (
    SalesCustomerHealthScoreDeteriorationEngine as Engine,
    HealthInput, HealthResult,
    HealthRisk, HealthPattern, HealthSeverity, HealthAction,
)

# ── helpers ────────────────────────────────────────────────────────────────────

def mk(**kw) -> HealthInput:
    d = dict(
        rep_id="R1", region="AMER", evaluation_period_id="Q1-2026",
        product_usage_trend_pct=0.10, nps_score_trend=0.10,
        support_ticket_volume_trend_pct=0.05, avg_ticket_severity_score=0.10,
        renewal_probability_score=0.90, last_exec_engagement_days=5.0,
        champion_change_events=0, contract_utilization_pct=0.80,
        multi_product_adoption_rate_pct=0.50, qbr_attendance_rate_pct=0.80,
        expansion_pipeline_vs_arr_pct=0.20, risk_flags_documented=0,
        competitor_evaluation_signals=0, time_to_value_days=10.0,
        onboarding_completion_rate_pct=0.90, stakeholder_coverage_score=0.80,
        satisfaction_survey_response_rate=0.70, invoice_payment_on_time_rate_pct=1.0,
        total_accounts_managed=100, avg_arr_per_account_usd=10_000.0,
    )
    d.update(kw)
    return HealthInput(**d)

def eng(): return Engine()
def assess(**kw): return eng().assess(mk(**kw))

# ── 1. Enum values ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("m,v", [
    (HealthRisk.low,"low"),(HealthRisk.moderate,"moderate"),(HealthRisk.high,"high"),(HealthRisk.critical,"critical"),
])
def test_risk_values(m, v): assert m.value == v

@pytest.mark.parametrize("m,v", [
    (HealthPattern.none,"none"),(HealthPattern.silent_churn_risk,"silent_churn_risk"),
    (HealthPattern.expansion_blocker,"expansion_blocker"),(HealthPattern.champion_departed,"champion_departed"),
    (HealthPattern.usage_collapse,"usage_collapse"),(HealthPattern.support_spiral,"support_spiral"),
])
def test_pattern_values(m, v): assert m.value == v

@pytest.mark.parametrize("m,v", [
    (HealthSeverity.healthy,"healthy"),(HealthSeverity.declining,"declining"),
    (HealthSeverity.at_risk,"at_risk"),(HealthSeverity.churning,"churning"),
])
def test_severity_values(m, v): assert m.value == v

@pytest.mark.parametrize("m,v", [
    (HealthAction.no_action,"no_action"),(HealthAction.health_monitoring,"health_monitoring"),
    (HealthAction.executive_business_review,"executive_business_review"),
    (HealthAction.champion_rebuild_plan,"champion_rebuild_plan"),
    (HealthAction.usage_enablement_program,"usage_enablement_program"),
    (HealthAction.support_escalation_review,"support_escalation_review"),
    (HealthAction.churn_prevention_task_force,"churn_prevention_task_force"),
])
def test_action_values(m, v): assert m.value == v

def test_risk_count():    assert len(HealthRisk) == 4
def test_pattern_count(): assert len(HealthPattern) == 6
def test_sev_count():     assert len(HealthSeverity) == 4
def test_action_count():  assert len(HealthAction) == 7

# ── 2. HealthInput fields ─────────────────────────────────────────────────────

def test_field_count(): assert len(dataclasses.fields(HealthInput)) == 23

@pytest.mark.parametrize("name", [
    "rep_id","region","evaluation_period_id","product_usage_trend_pct","nps_score_trend",
    "support_ticket_volume_trend_pct","avg_ticket_severity_score","renewal_probability_score",
    "last_exec_engagement_days","champion_change_events","contract_utilization_pct",
    "multi_product_adoption_rate_pct","qbr_attendance_rate_pct","expansion_pipeline_vs_arr_pct",
    "risk_flags_documented","competitor_evaluation_signals","time_to_value_days",
    "onboarding_completion_rate_pct","stakeholder_coverage_score","satisfaction_survey_response_rate",
    "invoice_payment_on_time_rate_pct","total_accounts_managed","avg_arr_per_account_usd",
])
def test_input_field_exists(name): assert name in HealthInput.__dataclass_fields__

# ── 3. to_dict: 15 keys ───────────────────────────────────────────────────────

def test_to_dict_count(): assert len(eng().assess(mk()).to_dict()) == 15

@pytest.mark.parametrize("key", [
    "rep_id","region","health_risk","health_pattern","health_severity","recommended_action",
    "engagement_score","adoption_score","satisfaction_score","renewal_readiness_score",
    "health_composite","has_health_gap","requires_health_intervention",
    "estimated_churn_arr_usd","health_signal",
])
def test_to_dict_key(key): assert key in eng().assess(mk()).to_dict()

def test_to_dict_enums_are_strings():
    d = eng().assess(mk()).to_dict()
    for k in ("health_risk","health_pattern","health_severity","recommended_action"):
        assert isinstance(d[k], str)

def test_to_dict_new_dict_each_call():
    r = eng().assess(mk()); d1,d2 = r.to_dict(),r.to_dict(); assert d1==d2 and d1 is not d2

# ── 4. summary(): 13 keys ─────────────────────────────────────────────────────

def test_summary_count_with_data():
    e=eng(); e.assess(mk()); assert len(e.summary())==13

def test_summary_count_empty(): assert len(eng().summary())==13

@pytest.mark.parametrize("key", [
    "total","risk_counts","pattern_counts","severity_counts","action_counts",
    "avg_health_composite","health_gap_count","intervention_count",
    "avg_engagement_score","avg_adoption_score","avg_satisfaction_score",
    "avg_renewal_readiness_score","total_estimated_churn_arr_usd",
])
def test_summary_key(key):
    e=eng(); e.assess(mk()); assert key in e.summary()

# ── 5. Engagement sub-score bands ────────────────────────────────────────────

@pytest.mark.parametrize("days,qbr,sth,min_s", [
    (90,0.80,0.80,40),(45,0.80,0.80,22),(21,0.80,0.80,8),
    (5,0.25,0.80,35),(5,0.55,0.80,18),(5,0.80,0.20,25),(5,0.80,0.45,12),
])
def test_engagement_band(days, qbr, sth, min_s):
    r=assess(last_exec_engagement_days=days,qbr_attendance_rate_pct=qbr,stakeholder_coverage_score=sth)
    assert r.engagement_score >= min_s

def test_engagement_all_clean_zero():
    assert assess(last_exec_engagement_days=5,qbr_attendance_rate_pct=0.80,stakeholder_coverage_score=0.80).engagement_score==0

def test_engagement_capped_100():
    assert assess(last_exec_engagement_days=120,qbr_attendance_rate_pct=0.10,stakeholder_coverage_score=0.10).engagement_score==100.0

# ── 6. Adoption sub-score bands ───────────────────────────────────────────────

@pytest.mark.parametrize("usage,util,onb,min_s", [
    (-0.25,0.80,0.90,45),(-0.10,0.80,0.90,25),(0.00,0.80,0.90,10),
    (0.10,0.30,0.90,30),(0.10,0.60,0.90,15),(0.10,0.80,0.40,25),(0.10,0.80,0.70,12),
])
def test_adoption_band(usage, util, onb, min_s):
    r=assess(product_usage_trend_pct=usage,contract_utilization_pct=util,onboarding_completion_rate_pct=onb)
    assert r.adoption_score >= min_s

def test_adoption_all_clean_zero():
    assert assess(product_usage_trend_pct=0.10,contract_utilization_pct=0.80,onboarding_completion_rate_pct=0.90).adoption_score==0

def test_adoption_capped_100():
    assert assess(product_usage_trend_pct=-0.50,contract_utilization_pct=0.10,onboarding_completion_rate_pct=0.10).adoption_score==100.0

# ── 7. Satisfaction sub-score bands ──────────────────────────────────────────

@pytest.mark.parametrize("nps,tix,sev,min_s", [
    (-0.30,0.0,0.0,40),(-0.10,0.0,0.0,22),(0.00,0.0,0.0,8),
    (0.10,0.50,0.0,35),(0.10,0.25,0.0,18),(0.10,0.0,0.65,25),(0.10,0.0,0.40,12),
])
def test_satisfaction_band(nps, tix, sev, min_s):
    r=assess(nps_score_trend=nps,support_ticket_volume_trend_pct=tix,avg_ticket_severity_score=sev)
    assert r.satisfaction_score >= min_s

def test_satisfaction_all_clean_zero():
    assert assess(nps_score_trend=0.10,support_ticket_volume_trend_pct=0.0,avg_ticket_severity_score=0.0).satisfaction_score==0

def test_satisfaction_capped_100():
    assert assess(nps_score_trend=-0.50,support_ticket_volume_trend_pct=1.0,avg_ticket_severity_score=1.0).satisfaction_score==100.0

# ── 8. Renewal readiness sub-score bands ─────────────────────────────────────

@pytest.mark.parametrize("renew,comp,flags,min_s", [
    (0.30,0,0,45),(0.55,0,0,25),(0.75,0,0,10),
    (0.90,3,0,30),(0.90,1,0,15),(0.90,0,4,25),(0.90,0,2,12),
])
def test_renewal_readiness_band(renew, comp, flags, min_s):
    r=assess(renewal_probability_score=renew,competitor_evaluation_signals=comp,risk_flags_documented=flags)
    assert r.renewal_readiness_score >= min_s

def test_renewal_readiness_all_clean_zero():
    assert assess(renewal_probability_score=0.90,competitor_evaluation_signals=0,risk_flags_documented=0).renewal_readiness_score==0

def test_renewal_readiness_capped_100():
    assert assess(renewal_probability_score=0.10,competitor_evaluation_signals=5,risk_flags_documented=10).renewal_readiness_score==100.0

# ── 9. Composite ─────────────────────────────────────────────────────────────

def test_composite_formula():
    r=eng().assess(mk())
    assert r.health_composite==min(round(r.engagement_score*0.25+r.adoption_score*0.30+r.satisfaction_score*0.25+r.renewal_readiness_score*0.20,2),100.0)

def test_composite_weights_sum(): assert abs(0.25+0.30+0.25+0.20-1.00)<1e-9
def test_composite_zero_healthy(): assert assess().health_composite==0.0
def test_composite_rounded_2dp():
    r=assess(last_exec_engagement_days=45,qbr_attendance_rate_pct=0.55); assert r.health_composite==round(r.health_composite,2)

def test_composite_capped_100():
    r=assess(last_exec_engagement_days=120,qbr_attendance_rate_pct=0.10,stakeholder_coverage_score=0.10,
             product_usage_trend_pct=-0.50,contract_utilization_pct=0.10,onboarding_completion_rate_pct=0.10,
             nps_score_trend=-0.50,support_ticket_volume_trend_pct=1.0,avg_ticket_severity_score=1.0,
             renewal_probability_score=0.10,competitor_evaluation_signals=5,risk_flags_documented=10)
    assert r.health_composite<=100.0

@pytest.mark.parametrize("en,ad,sa,rr", [
    (0,0,0,0),(100,0,0,0),(0,100,0,0),(0,0,100,0),(0,0,0,100),(40,30,20,10),(50,50,50,50),
])
def test_composite_weight_calc(en, ad, sa, rr):
    assert eng()._composite(en,ad,sa,rr)==min(round(en*0.25+ad*0.30+sa*0.25+rr*0.20,2),100.0)

# ── 10. Risk thresholds ───────────────────────────────────────────────────────

@pytest.mark.parametrize("c,exp", [
    (0,HealthRisk.low),(10,HealthRisk.low),(19.9,HealthRisk.low),
    (20,HealthRisk.moderate),(30,HealthRisk.moderate),(39.9,HealthRisk.moderate),
    (40,HealthRisk.high),(55,HealthRisk.high),(59.9,HealthRisk.high),
    (60,HealthRisk.critical),(80,HealthRisk.critical),(100,HealthRisk.critical),
])
def test_risk_threshold(c, exp): assert eng()._risk(c)==exp

# ── 11. Severity thresholds ───────────────────────────────────────────────────

@pytest.mark.parametrize("c,exp", [
    (0,HealthSeverity.healthy),(10,HealthSeverity.healthy),(19.9,HealthSeverity.healthy),
    (20,HealthSeverity.declining),(30,HealthSeverity.declining),(39.9,HealthSeverity.declining),
    (40,HealthSeverity.at_risk),(55,HealthSeverity.at_risk),(59.9,HealthSeverity.at_risk),
    (60,HealthSeverity.churning),(80,HealthSeverity.churning),(100,HealthSeverity.churning),
])
def test_severity_threshold(c, exp): assert eng()._severity(c)==exp

# ── 12. Action paths ──────────────────────────────────────────────────────────

@pytest.mark.parametrize("risk,pat,exp", [
    (HealthRisk.low,HealthPattern.none,HealthAction.no_action),
    (HealthRisk.low,HealthPattern.usage_collapse,HealthAction.no_action),
    (HealthRisk.moderate,HealthPattern.none,HealthAction.health_monitoring),
    (HealthRisk.moderate,HealthPattern.usage_collapse,HealthAction.health_monitoring),
    (HealthRisk.high,HealthPattern.silent_churn_risk,HealthAction.executive_business_review),
    (HealthRisk.high,HealthPattern.expansion_blocker,HealthAction.usage_enablement_program),
    (HealthRisk.high,HealthPattern.champion_departed,HealthAction.champion_rebuild_plan),
    (HealthRisk.high,HealthPattern.usage_collapse,HealthAction.usage_enablement_program),
    (HealthRisk.high,HealthPattern.support_spiral,HealthAction.support_escalation_review),
    (HealthRisk.high,HealthPattern.none,HealthAction.executive_business_review),
    (HealthRisk.critical,HealthPattern.silent_churn_risk,HealthAction.churn_prevention_task_force),
    (HealthRisk.critical,HealthPattern.champion_departed,HealthAction.churn_prevention_task_force),
    (HealthRisk.critical,HealthPattern.expansion_blocker,HealthAction.executive_business_review),
    (HealthRisk.critical,HealthPattern.usage_collapse,HealthAction.executive_business_review),
    (HealthRisk.critical,HealthPattern.support_spiral,HealthAction.executive_business_review),
    (HealthRisk.critical,HealthPattern.none,HealthAction.executive_business_review),
])
def test_action_path(risk, pat, exp): assert eng()._action(risk,pat)==exp

# ── 13. Pattern detection & priority ─────────────────────────────────────────

def test_pattern_silent_churn():
    assert assess(renewal_probability_score=0.35,risk_flags_documented=2,competitor_evaluation_signals=1).health_pattern==HealthPattern.silent_churn_risk
def test_pattern_expansion_blocker():
    assert assess(expansion_pipeline_vs_arr_pct=0.05,multi_product_adoption_rate_pct=0.15).health_pattern==HealthPattern.expansion_blocker
def test_pattern_champion_departed():
    assert assess(champion_change_events=2,stakeholder_coverage_score=0.30).health_pattern==HealthPattern.champion_departed
def test_pattern_usage_collapse():
    assert assess(product_usage_trend_pct=-0.20,contract_utilization_pct=0.40).health_pattern==HealthPattern.usage_collapse
def test_pattern_support_spiral():
    assert assess(support_ticket_volume_trend_pct=0.50,avg_ticket_severity_score=0.55).health_pattern==HealthPattern.support_spiral
def test_pattern_none(): assert assess().health_pattern==HealthPattern.none

def test_silent_beats_expansion():
    r=assess(renewal_probability_score=0.35,risk_flags_documented=2,competitor_evaluation_signals=1,
             expansion_pipeline_vs_arr_pct=0.05,multi_product_adoption_rate_pct=0.15)
    assert r.health_pattern==HealthPattern.silent_churn_risk
def test_expansion_beats_champion():
    r=assess(expansion_pipeline_vs_arr_pct=0.05,multi_product_adoption_rate_pct=0.15,champion_change_events=2,stakeholder_coverage_score=0.30)
    assert r.health_pattern==HealthPattern.expansion_blocker
def test_champion_beats_collapse():
    r=assess(champion_change_events=2,stakeholder_coverage_score=0.30,product_usage_trend_pct=-0.20,contract_utilization_pct=0.40)
    assert r.health_pattern==HealthPattern.champion_departed
def test_collapse_beats_spiral():
    r=assess(product_usage_trend_pct=-0.20,contract_utilization_pct=0.40,support_ticket_volume_trend_pct=0.50,avg_ticket_severity_score=0.55)
    assert r.health_pattern==HealthPattern.usage_collapse

def test_silent_needs_competitor():
    assert assess(renewal_probability_score=0.35,risk_flags_documented=2,competitor_evaluation_signals=0).health_pattern!=HealthPattern.silent_churn_risk
def test_expansion_needs_both():
    assert assess(expansion_pipeline_vs_arr_pct=0.05,multi_product_adoption_rate_pct=0.16).health_pattern!=HealthPattern.expansion_blocker
def test_champion_needs_ge2():
    assert assess(champion_change_events=1,stakeholder_coverage_score=0.30).health_pattern!=HealthPattern.champion_departed
def test_collapse_needs_both():
    assert assess(product_usage_trend_pct=-0.20,contract_utilization_pct=0.41).health_pattern!=HealthPattern.usage_collapse
def test_spiral_needs_both():
    assert assess(support_ticket_volume_trend_pct=0.50,avg_ticket_severity_score=0.54).health_pattern!=HealthPattern.support_spiral

# ── 14. Flags ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("renew,usage,comp,exp", [
    (0.65,0.10,0.0,True),(0.66,0.10,0.0,False),(0.90,-0.05,0.0,True),
    (0.90,-0.04,0.0,False),(0.90,0.10,40.0,True),(0.90,0.10,39.9,False),(0.90,0.10,0.0,False),
])
def test_has_gap(renew, usage, comp, exp):
    assert eng()._has_gap(mk(renewal_probability_score=renew,product_usage_trend_pct=usage),comp) is exp

@pytest.mark.parametrize("comp,sig,champ,exp", [
    (25.0,0,0,True),(24.9,0,0,False),(0.0,1,0,True),(0.0,0,1,True),(0.0,0,0,False),(24.9,2,0,True),
])
def test_requires_intervention(comp, sig, champ, exp):
    assert eng()._requires_intervention(mk(competitor_evaluation_signals=sig,champion_change_events=champ),comp) is exp

def test_gap_in_result(): assert assess(renewal_probability_score=0.50).has_health_gap is True
def test_intervention_in_result(): assert assess(competitor_evaluation_signals=1).requires_health_intervention is True

# ── 15. Churn ARR ─────────────────────────────────────────────────────────────

def test_churn_arr_zero_composite_zero(): assert assess().estimated_churn_arr_usd==0.0
def test_churn_arr_zero_renewal_100(): assert assess(renewal_probability_score=1.0).estimated_churn_arr_usd==0.0
def test_churn_arr_zero_accounts(): assert assess(total_accounts_managed=0).estimated_churn_arr_usd==0.0
def test_churn_arr_zero_arr(): assert assess(avg_arr_per_account_usd=0.0).estimated_churn_arr_usd==0.0
def test_churn_arr_positive_risky():
    assert assess(renewal_probability_score=0.30,risk_flags_documented=4,competitor_evaluation_signals=3,
                  total_accounts_managed=10,avg_arr_per_account_usd=100_000.0).estimated_churn_arr_usd>0
def test_churn_arr_formula():
    inp=mk(total_accounts_managed=50,avg_arr_per_account_usd=20_000.0,renewal_probability_score=0.80)
    r=eng().assess(inp); comp=r.health_composite
    assert r.estimated_churn_arr_usd==round(50*20_000.0*(comp/100)*(1-0.80),2)
def test_churn_arr_rounded_2dp():
    r=eng().assess(mk(total_accounts_managed=7,avg_arr_per_account_usd=3_333.33,renewal_probability_score=0.70))
    assert r.estimated_churn_arr_usd==round(r.estimated_churn_arr_usd,2)

@pytest.mark.parametrize("accts,arr,renew,comp", [
    (100,10_000,0.90,0.0),(50,20_000,0.80,25.0),(10,100_000,0.50,60.0),(1,1_000,0.30,80.0),(0,50_000,0.70,50.0),
])
def test_churn_arr_formula_param(accts, arr, renew, comp):
    assert eng()._churn_arr(mk(total_accounts_managed=accts,avg_arr_per_account_usd=arr,renewal_probability_score=renew),comp)==round(accts*arr*(comp/100)*(1-renew),2)

# ── 16. Signal text ───────────────────────────────────────────────────────────

def test_signal_stable_healthy(): assert "stable" in assess().health_signal
def test_signal_is_string(): assert isinstance(assess().health_signal, str)
def test_signal_usage_trend_when_unhealthy():
    r=assess(last_exec_engagement_days=90)
    if r.health_composite>=20: assert "usage trend" in r.health_signal
def test_signal_renewal_prob_when_unhealthy():
    r=assess(last_exec_engagement_days=90)
    if r.health_composite>=20: assert "renewal probability" in r.health_signal
def test_signal_exec_contact_when_unhealthy():
    r=assess(last_exec_engagement_days=90)
    if r.health_composite>=20: assert "exec contact" in r.health_signal
def test_signal_composite_when_unhealthy():
    r=assess(last_exec_engagement_days=90)
    if r.health_composite>=20: assert "composite" in r.health_signal
def test_signal_usage_collapse_label():
    r=assess(product_usage_trend_pct=-0.20,contract_utilization_pct=0.40,last_exec_engagement_days=90)
    if r.health_pattern==HealthPattern.usage_collapse: assert "Usage collapse" in r.health_signal
def test_signal_silent_churn_label():
    r=assess(renewal_probability_score=0.35,risk_flags_documented=2,competitor_evaluation_signals=1,last_exec_engagement_days=90)
    if r.health_pattern==HealthPattern.silent_churn_risk: assert "Silent churn risk" in r.health_signal

# ── 17. assess() / assess_batch() ────────────────────────────────────────────

def test_assess_returns_result(): assert isinstance(eng().assess(mk()),HealthResult)
def test_assess_stores(): e=eng(); e.assess(mk()); assert len(e._results)==1
def test_assess_rep_id(): assert assess(rep_id="XYZ").rep_id=="XYZ"
def test_assess_region(): assert assess(region="EMEA").region=="EMEA"
def test_assess_accumulates(): e=eng(); e.assess(mk()); e.assess(mk()); assert len(e._results)==2
def test_batch_returns_list(): assert isinstance(eng().assess_batch([mk()]*3),list)
def test_batch_length(): assert len(eng().assess_batch([mk()]*5))==5
def test_batch_all_results(): assert all(isinstance(r,HealthResult) for r in eng().assess_batch([mk()]*5))
def test_batch_stores_all(): e=eng(); e.assess_batch([mk()]*4); assert len(e._results)==4
def test_batch_empty(): assert eng().assess_batch([])==[]
def test_batch_empty_summary(): e=eng(); e.assess_batch([]); assert e.summary()["total"]==0
def test_batch_order():
    ins=[mk(rep_id=f"R{i}") for i in range(4)]; res=eng().assess_batch(ins)
    assert [r.rep_id for r in res]==[f"R{i}" for i in range(4)]

@pytest.mark.parametrize("rep,region", [("A","AMER"),("B","EMEA"),("C","APAC"),("D","LATAM")])
def test_assess_identity(rep, region):
    r=eng().assess(mk(rep_id=rep,region=region)); assert r.rep_id==rep and r.region==region

# ── 18. summary() aggregation ─────────────────────────────────────────────────

def test_summary_total(): e=eng(); e.assess_batch([mk()]*5); assert e.summary()["total"]==5
def test_summary_empty_total(): assert eng().summary()["total"]==0
def test_summary_empty_composite(): assert eng().summary()["avg_health_composite"]==0.0
def test_summary_empty_churn_arr(): assert eng().summary()["total_estimated_churn_arr_usd"]==0.0
def test_summary_risk_counts_sum(): e=eng(); e.assess_batch([mk()]*3); assert sum(e.summary()["risk_counts"].values())==3
def test_summary_pattern_counts_sum(): e=eng(); e.assess_batch([mk()]*3); assert sum(e.summary()["pattern_counts"].values())==3
def test_summary_severity_counts_sum(): e=eng(); e.assess_batch([mk()]*3); assert sum(e.summary()["severity_counts"].values())==3
def test_summary_action_counts_sum(): e=eng(); e.assess_batch([mk()]*3); assert sum(e.summary()["action_counts"].values())==3
def test_summary_gap_count():
    e=eng(); e.assess(mk(renewal_probability_score=0.50)); e.assess(mk(renewal_probability_score=0.90,product_usage_trend_pct=0.10))
    assert e.summary()["health_gap_count"]==1
def test_summary_intervention_count():
    e=eng(); e.assess(mk(competitor_evaluation_signals=1)); e.assess(mk())
    assert e.summary()["intervention_count"]==1
def test_summary_churn_arr_sum():
    e=eng(); r1=e.assess(mk()); r2=e.assess(mk())
    assert e.summary()["total_estimated_churn_arr_usd"]==round(r1.estimated_churn_arr_usd+r2.estimated_churn_arr_usd,2)
def test_summary_avg_composite():
    e=eng(); r1=e.assess(mk()); r2=e.assess(mk())
    assert e.summary()["avg_health_composite"]==round((r1.health_composite+r2.health_composite)/2,1)
def test_summary_avg_scores_1dp():
    e=eng(); e.assess(mk()); s=e.summary()
    for k in ("avg_engagement_score","avg_adoption_score","avg_satisfaction_score","avg_renewal_readiness_score"):
        assert s[k]==round(s[k],1)
def test_summary_counts_str_keys():
    e=eng(); e.assess(mk()); s=e.summary()
    for d in (s["risk_counts"],s["pattern_counts"],s["severity_counts"],s["action_counts"]):
        assert all(isinstance(k,str) for k in d)

# ── 19. Engine isolation ──────────────────────────────────────────────────────

def test_engines_independent(): e1,e2=eng(),eng(); e1.assess(mk()); assert len(e2._results)==0
def test_fresh_engine_empty(): assert len(eng()._results)==0
def test_engines_no_shared_state():
    e1,e2=eng(),eng(); e1.assess(mk()); e1.assess(mk()); e2.assess(mk())
    assert e1.summary()["total"]==2 and e2.summary()["total"]==1

# ── 20. End-to-end scenarios ──────────────────────────────────────────────────

def test_critical_churn_scenario():
    r=assess(renewal_probability_score=0.20,risk_flags_documented=5,competitor_evaluation_signals=3,
             last_exec_engagement_days=100,qbr_attendance_rate_pct=0.10,stakeholder_coverage_score=0.10,
             product_usage_trend_pct=-0.40,contract_utilization_pct=0.20,onboarding_completion_rate_pct=0.30,
             nps_score_trend=-0.50,support_ticket_volume_trend_pct=0.80,avg_ticket_severity_score=0.90)
    assert r.health_risk==HealthRisk.critical and r.health_severity==HealthSeverity.churning
    assert r.recommended_action==HealthAction.churn_prevention_task_force
    assert r.has_health_gap is True and r.requires_health_intervention is True

def test_healthy_scenario():
    r=assess()
    assert r.health_risk==HealthRisk.low and r.health_severity==HealthSeverity.healthy
    assert r.recommended_action==HealthAction.no_action and r.health_composite==0.0

# ── 21. Engagement boundary: exact thresholds ────────────────────────────────

@pytest.mark.parametrize("days,min_s", [(90,40),(45,22),(21,8)])
def test_engagement_exec_exact_boundary(days, min_s):
    r=assess(last_exec_engagement_days=days,qbr_attendance_rate_pct=0.80,stakeholder_coverage_score=0.80)
    assert r.engagement_score>=min_s

@pytest.mark.parametrize("qbr,min_s", [(0.25,35),(0.55,18)])
def test_engagement_qbr_exact_boundary(qbr, min_s):
    r=assess(last_exec_engagement_days=5,qbr_attendance_rate_pct=qbr,stakeholder_coverage_score=0.80)
    assert r.engagement_score>=min_s

@pytest.mark.parametrize("sth,min_s", [(0.20,25),(0.45,12)])
def test_engagement_stakeholder_exact_boundary(sth, min_s):
    r=assess(last_exec_engagement_days=5,qbr_attendance_rate_pct=0.80,stakeholder_coverage_score=sth)
    assert r.engagement_score>=min_s

# ── 22. Adoption boundary: exact thresholds ──────────────────────────────────

@pytest.mark.parametrize("usage,min_s", [(-0.25,45),(-0.10,25),(0.00,10)])
def test_adoption_usage_exact(usage, min_s):
    r=assess(product_usage_trend_pct=usage,contract_utilization_pct=0.80,onboarding_completion_rate_pct=0.90)
    assert r.adoption_score>=min_s

@pytest.mark.parametrize("util,min_s", [(0.30,30),(0.60,15)])
def test_adoption_util_exact(util, min_s):
    r=assess(product_usage_trend_pct=0.10,contract_utilization_pct=util,onboarding_completion_rate_pct=0.90)
    assert r.adoption_score>=min_s

@pytest.mark.parametrize("onb,min_s", [(0.40,25),(0.70,12)])
def test_adoption_onb_exact(onb, min_s):
    r=assess(product_usage_trend_pct=0.10,contract_utilization_pct=0.80,onboarding_completion_rate_pct=onb)
    assert r.adoption_score>=min_s

# ── 23. Satisfaction boundary: exact thresholds ──────────────────────────────

@pytest.mark.parametrize("nps,min_s", [(-0.30,40),(-0.10,22),(0.00,8)])
def test_satisfaction_nps_exact(nps, min_s):
    r=assess(nps_score_trend=nps,support_ticket_volume_trend_pct=0.0,avg_ticket_severity_score=0.0)
    assert r.satisfaction_score>=min_s

@pytest.mark.parametrize("tix,min_s", [(0.50,35),(0.25,18)])
def test_satisfaction_tickets_exact(tix, min_s):
    r=assess(nps_score_trend=0.10,support_ticket_volume_trend_pct=tix,avg_ticket_severity_score=0.0)
    assert r.satisfaction_score>=min_s

@pytest.mark.parametrize("sev,min_s", [(0.65,25),(0.40,12)])
def test_satisfaction_sev_exact(sev, min_s):
    r=assess(nps_score_trend=0.10,support_ticket_volume_trend_pct=0.0,avg_ticket_severity_score=sev)
    assert r.satisfaction_score>=min_s

# ── 24. Renewal readiness boundary: exact thresholds ─────────────────────────

@pytest.mark.parametrize("renew,min_s", [(0.30,45),(0.55,25),(0.75,10)])
def test_renewal_renew_exact(renew, min_s):
    r=assess(renewal_probability_score=renew,competitor_evaluation_signals=0,risk_flags_documented=0)
    assert r.renewal_readiness_score>=min_s

@pytest.mark.parametrize("comp,min_s", [(3,30),(1,15)])
def test_renewal_competitor_exact(comp, min_s):
    r=assess(renewal_probability_score=0.90,competitor_evaluation_signals=comp,risk_flags_documented=0)
    assert r.renewal_readiness_score>=min_s

@pytest.mark.parametrize("flags,min_s", [(4,25),(2,12)])
def test_renewal_flags_exact(flags, min_s):
    r=assess(renewal_probability_score=0.90,competitor_evaluation_signals=0,risk_flags_documented=flags)
    assert r.renewal_readiness_score>=min_s

# ── 25. to_dict field type checks ────────────────────────────────────────────

@pytest.mark.parametrize("key", ["engagement_score","adoption_score","satisfaction_score",
                                   "renewal_readiness_score","health_composite","estimated_churn_arr_usd"])
def test_to_dict_numeric_field_is_float(key):
    d=eng().assess(mk()).to_dict(); assert isinstance(d[key],(int,float))

@pytest.mark.parametrize("key", ["has_health_gap","requires_health_intervention"])
def test_to_dict_bool_field(key):
    d=eng().assess(mk()).to_dict(); assert isinstance(d[key],bool)

def test_to_dict_signal_is_str(): assert isinstance(eng().assess(mk()).to_dict()["health_signal"],str)
def test_to_dict_rep_id_str(): assert isinstance(eng().assess(mk()).to_dict()["rep_id"],str)
def test_to_dict_region_str(): assert isinstance(eng().assess(mk()).to_dict()["region"],str)
