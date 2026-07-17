"""Comprehensive pytest suite for SalesProposalQualityWinRateIntelligenceEngine."""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_proposal_quality_win_rate_intelligence_engine import (
    ProposalRisk, ProposalPattern, ProposalSeverity, ProposalAction,
    ProposalInput, ProposalResult,
    SalesProposalQualityWinRateIntelligenceEngine as Engine,
)

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def make_input(**kw) -> ProposalInput:
    d = dict(rep_id="TEST-01", region="EMEA", evaluation_period_id="Q1-2026",
             proposal_to_close_rate_pct=0.65, proposal_sent_without_discovery_rate_pct=0.05,
             avg_days_to_send_proposal=8.0, proposal_revision_count_avg=1.5,
             executive_sponsor_present_in_proposal_pct=0.80, proposal_customization_score=0.80,
             value_articulation_score=0.80, competitive_differentiation_score=0.75,
             pricing_structure_complexity_score=0.20, proposal_response_time_days=5.0,
             unanswered_proposal_rate_pct=0.05, proposal_reused_template_rate_pct=0.05,
             mutual_success_plan_inclusion_rate_pct=0.75, roi_case_included_rate_pct=0.80,
             legal_redline_rate_pct=0.10, multi_stakeholder_proposal_rate_pct=0.75,
             proposal_champion_alignment_score=0.80, total_proposals_sent=20,
             avg_deal_value_usd=90000.0)
    d.update(kw); return ProposalInput(**d)

def eng(): return Engine()

# ---------------------------------------------------------------------------
# 1. Enum membership
# ---------------------------------------------------------------------------
def test_risk_members(): assert {e.value for e in ProposalRisk} == {"low","moderate","high","critical"}
def test_pattern_members(): assert {e.value for e in ProposalPattern} == {"none","premature_proposer","template_lazy","ghosted_proposer","revision_looper","orphaned_proposal"}
def test_severity_members(): assert {e.value for e in ProposalSeverity} == {"converting","softening","stalling","collapsing"}
def test_action_members(): assert {e.value for e in ProposalAction} == {"no_action","proposal_quality_monitoring","customization_coaching","discovery_gate_enforcement","engagement_reactivation_coaching","deal_desk_proposal_support","champion_alignment_coaching","proposal_quality_coaching","proposal_strategy_intervention","proposal_framework_redesign"}
def test_risk_is_str(): assert isinstance(ProposalRisk.low, str)
def test_pattern_is_str(): assert isinstance(ProposalPattern.none, str)
def test_severity_is_str(): assert isinstance(ProposalSeverity.converting, str)
def test_action_is_str(): assert isinstance(ProposalAction.no_action, str)
def test_risk_count(): assert len(ProposalRisk) == 4
def test_pattern_count(): assert len(ProposalPattern) == 6
def test_severity_count(): assert len(ProposalSeverity) == 4
def test_action_count(): assert len(ProposalAction) == 10

# ---------------------------------------------------------------------------
# 2. ProposalInput — 22 fields
# ---------------------------------------------------------------------------
_ALL_FIELDS = ["rep_id","region","evaluation_period_id","proposal_to_close_rate_pct",
    "proposal_sent_without_discovery_rate_pct","avg_days_to_send_proposal",
    "proposal_revision_count_avg","executive_sponsor_present_in_proposal_pct",
    "proposal_customization_score","value_articulation_score",
    "competitive_differentiation_score","pricing_structure_complexity_score",
    "proposal_response_time_days","unanswered_proposal_rate_pct",
    "proposal_reused_template_rate_pct","mutual_success_plan_inclusion_rate_pct",
    "roi_case_included_rate_pct","legal_redline_rate_pct",
    "multi_stakeholder_proposal_rate_pct","proposal_champion_alignment_score",
    "total_proposals_sent","avg_deal_value_usd"]

@pytest.mark.parametrize("f", _ALL_FIELDS)
def test_input_has_field(f): assert hasattr(make_input(), f)

def test_input_total_proposals_int(): assert isinstance(make_input().total_proposals_sent, int)
def test_input_rep_id(): assert make_input().rep_id == "TEST-01"
def test_input_region(): assert make_input().region == "EMEA"
def test_input_period(): assert make_input().evaluation_period_id == "Q1-2026"
def test_input_override(): assert make_input(rep_id="X").rep_id == "X"

# ---------------------------------------------------------------------------
# 3. to_dict — exactly 15 keys
# ---------------------------------------------------------------------------
_DICT_KEYS = {"rep_id","region","proposal_risk","proposal_pattern","proposal_severity",
    "recommended_action","quality_score","readiness_score","execution_score","alignment_score",
    "proposal_composite","has_proposal_gap","requires_proposal_coaching",
    "estimated_deal_loss_usd","proposal_signal"}

def test_to_dict_key_count(): assert len(eng().assess(make_input()).to_dict()) == 15
def test_to_dict_exact_keys(): assert set(eng().assess(make_input()).to_dict().keys()) == _DICT_KEYS
def test_to_dict_risk_str(): assert isinstance(eng().assess(make_input()).to_dict()["proposal_risk"], str)
def test_to_dict_pattern_str(): assert isinstance(eng().assess(make_input()).to_dict()["proposal_pattern"], str)
def test_to_dict_severity_str(): assert isinstance(eng().assess(make_input()).to_dict()["proposal_severity"], str)
def test_to_dict_action_str(): assert isinstance(eng().assess(make_input()).to_dict()["recommended_action"], str)
def test_to_dict_composite_float(): assert isinstance(eng().assess(make_input()).to_dict()["proposal_composite"], float)
def test_to_dict_gap_bool(): assert isinstance(eng().assess(make_input()).to_dict()["has_proposal_gap"], bool)
def test_to_dict_coaching_bool(): assert isinstance(eng().assess(make_input()).to_dict()["requires_proposal_coaching"], bool)
def test_to_dict_rep_id(): assert eng().assess(make_input()).to_dict()["rep_id"] == "TEST-01"
def test_to_dict_region(): assert eng().assess(make_input()).to_dict()["region"] == "EMEA"
def test_to_dict_signal_str(): assert isinstance(eng().assess(make_input()).to_dict()["proposal_signal"], str)

# ---------------------------------------------------------------------------
# 4. _quality_score
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("custom,va,roi,expected", [
    (0.80, 0.90, 0.90,  0.0),  # all above thresholds
    (0.20, 0.90, 0.90, 40.0),  # custom <=0.20
    (0.45, 0.90, 0.90, 22.0),  # custom <=0.45
    (0.65, 0.90, 0.90,  8.0),  # custom <=0.65
    (0.90, 0.25, 0.90, 35.0),  # va <=0.25
    (0.90, 0.55, 0.90, 18.0),  # va <=0.55
    (0.90, 0.90, 0.30, 25.0),  # roi <=0.30
    (0.90, 0.90, 0.55, 12.0),  # roi <=0.55
    (0.10, 0.10, 0.10,100.0),  # all worst → cap 100
    (0.44, 0.50, 0.50, 52.0),  # 22+18+12
    (0.21, 0.90, 0.90, 22.0),  # just above 0.20 → tier 2
])
def test_quality_score(custom, va, roi, expected):
    e = Engine()
    assert e._quality_score(make_input(proposal_customization_score=custom,
        value_articulation_score=va, roi_case_included_rate_pct=roi)) == expected

# ---------------------------------------------------------------------------
# 5. _readiness_score
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("disc,exec_s,msp,expected", [
    (0.05, 0.90, 0.90,  0.0),
    (0.55, 0.90, 0.90, 40.0),
    (0.30, 0.90, 0.90, 22.0),
    (0.15, 0.90, 0.90,  8.0),
    (0.14, 0.90, 0.90,  0.0),
    (0.05, 0.20, 0.90, 35.0),
    (0.05, 0.45, 0.90, 18.0),
    (0.05, 0.46, 0.90,  0.0),
    (0.05, 0.90, 0.20, 25.0),
    (0.05, 0.90, 0.45, 12.0),
    (0.05, 0.90, 0.46,  0.0),
    (0.60, 0.10, 0.10,100.0),
])
def test_readiness_score(disc, exec_s, msp, expected):
    e = Engine()
    assert e._readiness_score(make_input(
        proposal_sent_without_discovery_rate_pct=disc,
        executive_sponsor_present_in_proposal_pct=exec_s,
        mutual_success_plan_inclusion_rate_pct=msp)) == expected

# ---------------------------------------------------------------------------
# 6. _execution_score
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("unans,revs,days,expected", [
    (0.05, 0.5,  5.0,  0.0),
    (0.50, 0.5,  5.0, 45.0),
    (0.30, 0.5,  5.0, 25.0),
    (0.15, 0.5,  5.0, 10.0),
    (0.14, 0.5,  5.0,  0.0),
    (0.05, 5.0,  5.0, 30.0),
    (0.05, 3.0,  5.0, 15.0),
    (0.05, 2.9,  5.0,  0.0),
    (0.05, 0.5, 21.0, 25.0),
    (0.05, 0.5, 10.0, 12.0),
    (0.05, 0.5,  9.9,  0.0),
    (0.90,10.0, 30.0,100.0),
    (0.30, 3.0, 10.0, 52.0),
])
def test_execution_score(unans, revs, days, expected):
    e = Engine()
    assert e._execution_score(make_input(
        unanswered_proposal_rate_pct=unans,
        proposal_revision_count_avg=revs,
        avg_days_to_send_proposal=days)) == expected

# ---------------------------------------------------------------------------
# 7. _alignment_score
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("champ,multi,comp_d,expected", [
    (0.80, 0.90, 0.90,  0.0),
    (0.20, 0.90, 0.90, 45.0),
    (0.45, 0.90, 0.90, 25.0),
    (0.65, 0.90, 0.90, 10.0),
    (0.66, 0.90, 0.90,  0.0),
    (0.90, 0.20, 0.90, 30.0),
    (0.90, 0.45, 0.90, 15.0),
    (0.90, 0.46, 0.90,  0.0),
    (0.90, 0.90, 0.20, 25.0),
    (0.90, 0.90, 0.50, 12.0),
    (0.90, 0.90, 0.51,  0.0),
    (0.05, 0.05, 0.05,100.0),
    (0.40, 0.40, 0.40, 52.0),
])
def test_alignment_score(champ, multi, comp_d, expected):
    e = Engine()
    assert e._alignment_score(make_input(
        proposal_champion_alignment_score=champ,
        multi_stakeholder_proposal_rate_pct=multi,
        competitive_differentiation_score=comp_d)) == expected

# ---------------------------------------------------------------------------
# 8. _composite
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("qu,re,ex,al,expected", [
    (0, 0, 0, 0, 0.0),
    (100,100,100,100,100.0),
    (40, 0, 0, 0, round(40*0.30,2)),
    (0, 40, 0, 0, round(40*0.25,2)),
    (0, 0, 40, 0, round(40*0.25,2)),
    (0, 0, 0, 40, round(40*0.20,2)),
    (80,60,40,20, round(80*0.30+60*0.25+40*0.25+20*0.20,2)),
    (33,33,33,33, round(33*0.30+33*0.25+33*0.25+33*0.20,2)),
    (200,200,200,200,100.0),
])
def test_composite(qu, re, ex, al, expected):
    assert Engine()._composite(qu, re, ex, al) == expected

# ---------------------------------------------------------------------------
# 9. Pattern detection
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("kw,expected_pattern", [
    ({}, ProposalPattern.none),
    ({"proposal_sent_without_discovery_rate_pct":0.50,"avg_days_to_send_proposal":5.0}, ProposalPattern.premature_proposer),
    ({"proposal_sent_without_discovery_rate_pct":0.70,"avg_days_to_send_proposal":3.0}, ProposalPattern.premature_proposer),
    ({"proposal_sent_without_discovery_rate_pct":0.49,"avg_days_to_send_proposal":3.0}, ProposalPattern.none),
    ({"proposal_sent_without_discovery_rate_pct":0.60,"avg_days_to_send_proposal":6.0}, ProposalPattern.none),
    ({"proposal_reused_template_rate_pct":0.60,"proposal_customization_score":0.30}, ProposalPattern.template_lazy),
    ({"proposal_reused_template_rate_pct":0.59,"proposal_customization_score":0.20}, ProposalPattern.none),
    ({"proposal_reused_template_rate_pct":0.70,"proposal_customization_score":0.31}, ProposalPattern.none),
    ({"unanswered_proposal_rate_pct":0.45,"proposal_response_time_days":14.0}, ProposalPattern.ghosted_proposer),
    ({"unanswered_proposal_rate_pct":0.44,"proposal_response_time_days":20.0}, ProposalPattern.none),
    ({"unanswered_proposal_rate_pct":0.50,"proposal_response_time_days":13.0}, ProposalPattern.none),
    ({"proposal_revision_count_avg":4.0,"legal_redline_rate_pct":0.35}, ProposalPattern.revision_looper),
    ({"proposal_revision_count_avg":3.9,"legal_redline_rate_pct":0.40}, ProposalPattern.none),
    ({"proposal_revision_count_avg":5.0,"legal_redline_rate_pct":0.34}, ProposalPattern.none),
    ({"executive_sponsor_present_in_proposal_pct":0.20,"proposal_champion_alignment_score":0.30}, ProposalPattern.orphaned_proposal),
    ({"executive_sponsor_present_in_proposal_pct":0.21,"proposal_champion_alignment_score":0.20}, ProposalPattern.none),
    ({"executive_sponsor_present_in_proposal_pct":0.10,"proposal_champion_alignment_score":0.31}, ProposalPattern.none),
])
def test_pattern(kw, expected_pattern):
    assert Engine()._pattern(make_input(**kw)) == expected_pattern

def test_pattern_first_match_wins():
    # premature beats template_lazy
    pat = Engine()._pattern(make_input(
        proposal_sent_without_discovery_rate_pct=0.60, avg_days_to_send_proposal=4.0,
        proposal_reused_template_rate_pct=0.70, proposal_customization_score=0.20))
    assert pat == ProposalPattern.premature_proposer

# ---------------------------------------------------------------------------
# 10. Risk thresholds
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("composite,expected", [
    (0.0, ProposalRisk.low), (19.99, ProposalRisk.low),
    (20.0, ProposalRisk.moderate), (39.99, ProposalRisk.moderate),
    (40.0, ProposalRisk.high), (59.99, ProposalRisk.high),
    (60.0, ProposalRisk.critical), (100.0, ProposalRisk.critical),
])
def test_risk(composite, expected): assert Engine()._risk(composite) == expected

# ---------------------------------------------------------------------------
# 11. Severity thresholds
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("composite,expected", [
    (0.0, ProposalSeverity.converting), (19.99, ProposalSeverity.converting),
    (20.0, ProposalSeverity.softening), (39.99, ProposalSeverity.softening),
    (40.0, ProposalSeverity.stalling), (59.99, ProposalSeverity.stalling),
    (60.0, ProposalSeverity.collapsing), (100.0, ProposalSeverity.collapsing),
])
def test_severity(composite, expected): assert Engine()._severity(composite) == expected

# ---------------------------------------------------------------------------
# 12. Action logic
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("risk,pattern,expected_action", [
    (ProposalRisk.low, ProposalPattern.none, ProposalAction.no_action),
    (ProposalRisk.low, ProposalPattern.premature_proposer, ProposalAction.no_action),
    (ProposalRisk.low, ProposalPattern.template_lazy, ProposalAction.no_action),
    (ProposalRisk.low, ProposalPattern.ghosted_proposer, ProposalAction.no_action),
    (ProposalRisk.low, ProposalPattern.revision_looper, ProposalAction.no_action),
    (ProposalRisk.low, ProposalPattern.orphaned_proposal, ProposalAction.no_action),
    (ProposalRisk.moderate, ProposalPattern.none, ProposalAction.proposal_quality_monitoring),
    (ProposalRisk.moderate, ProposalPattern.premature_proposer, ProposalAction.proposal_quality_monitoring),
    (ProposalRisk.moderate, ProposalPattern.template_lazy, ProposalAction.proposal_quality_monitoring),
    (ProposalRisk.moderate, ProposalPattern.ghosted_proposer, ProposalAction.proposal_quality_monitoring),
    (ProposalRisk.moderate, ProposalPattern.revision_looper, ProposalAction.proposal_quality_monitoring),
    (ProposalRisk.moderate, ProposalPattern.orphaned_proposal, ProposalAction.proposal_quality_monitoring),
    (ProposalRisk.high, ProposalPattern.premature_proposer, ProposalAction.discovery_gate_enforcement),
    (ProposalRisk.high, ProposalPattern.template_lazy, ProposalAction.customization_coaching),
    (ProposalRisk.high, ProposalPattern.ghosted_proposer, ProposalAction.engagement_reactivation_coaching),
    (ProposalRisk.high, ProposalPattern.revision_looper, ProposalAction.deal_desk_proposal_support),
    (ProposalRisk.high, ProposalPattern.orphaned_proposal, ProposalAction.champion_alignment_coaching),
    (ProposalRisk.high, ProposalPattern.none, ProposalAction.proposal_quality_coaching),
    (ProposalRisk.critical, ProposalPattern.premature_proposer, ProposalAction.proposal_framework_redesign),
    (ProposalRisk.critical, ProposalPattern.template_lazy, ProposalAction.proposal_framework_redesign),
    (ProposalRisk.critical, ProposalPattern.ghosted_proposer, ProposalAction.proposal_strategy_intervention),
    (ProposalRisk.critical, ProposalPattern.revision_looper, ProposalAction.proposal_strategy_intervention),
    (ProposalRisk.critical, ProposalPattern.orphaned_proposal, ProposalAction.proposal_strategy_intervention),
    (ProposalRisk.critical, ProposalPattern.none, ProposalAction.proposal_strategy_intervention),
])
def test_action(risk, pattern, expected_action):
    assert Engine()._action(risk, pattern) == expected_action

# ---------------------------------------------------------------------------
# 13. Flags
# ---------------------------------------------------------------------------
def test_gap_false_healthy(): assert not Engine()._has_gap(make_input(), 10.0)
def test_gap_true_composite(): assert Engine()._has_gap(make_input(), 40.0)
def test_gap_true_close_rate(): assert Engine()._has_gap(make_input(proposal_to_close_rate_pct=0.25), 10.0)
def test_gap_true_unanswered(): assert Engine()._has_gap(make_input(unanswered_proposal_rate_pct=0.30), 10.0)
def test_gap_false_close_rate_above(): assert not Engine()._has_gap(make_input(proposal_to_close_rate_pct=0.26), 10.0)
def test_gap_false_unanswered_below(): assert not Engine()._has_gap(make_input(unanswered_proposal_rate_pct=0.29), 10.0)
def test_coaching_false_healthy(): assert not Engine()._requires_coaching(make_input(), 10.0)
def test_coaching_true_composite(): assert Engine()._requires_coaching(make_input(), 25.0)
def test_coaching_true_discovery(): assert Engine()._requires_coaching(make_input(proposal_sent_without_discovery_rate_pct=0.30), 10.0)
def test_coaching_true_custom(): assert Engine()._requires_coaching(make_input(proposal_customization_score=0.50), 10.0)
def test_coaching_false_custom_above(): assert not Engine()._requires_coaching(make_input(proposal_customization_score=0.51), 10.0)
def test_coaching_false_discovery_below(): assert not Engine()._requires_coaching(make_input(proposal_sent_without_discovery_rate_pct=0.29), 10.0)

# ---------------------------------------------------------------------------
# 14. Deal loss estimate
# ---------------------------------------------------------------------------
def test_deal_loss_zero_composite(): assert Engine()._deal_loss_estimate(make_input(), 0.0) == 0.0
def test_deal_loss_zero_proposals(): assert Engine()._deal_loss_estimate(make_input(total_proposals_sent=0), 80.0) == 0.0
def test_deal_loss_zero_deal_value(): assert Engine()._deal_loss_estimate(make_input(avg_deal_value_usd=0.0), 50.0) == 0.0
def test_deal_loss_perfect_close_rate(): assert Engine()._deal_loss_estimate(make_input(proposal_to_close_rate_pct=1.0), 50.0) == 0.0
def test_deal_loss_formula():
    inp = make_input(total_proposals_sent=10, avg_deal_value_usd=100000.0, proposal_to_close_rate_pct=0.50)
    assert Engine()._deal_loss_estimate(inp, 50.0) == round(10*100000.0*0.50*0.50, 2)
def test_deal_loss_rounded():
    inp = make_input(total_proposals_sent=3, avg_deal_value_usd=10000.0, proposal_to_close_rate_pct=0.33)
    r = Engine()._deal_loss_estimate(inp, 33.0)
    assert r == round(3*10000.0*0.67*0.33, 2)
def test_deal_loss_full():
    inp = make_input(total_proposals_sent=20, avg_deal_value_usd=50000.0, proposal_to_close_rate_pct=0.0)
    assert Engine()._deal_loss_estimate(inp, 100.0) == round(20*50000.0*1.0*1.0, 2)

# ---------------------------------------------------------------------------
# 15. Signal
# ---------------------------------------------------------------------------
_HEALTHY = ("Proposal quality and win rate healthy — customization, discovery readiness, "
            "and champion alignment within benchmark targets")

def test_signal_healthy_exact(): assert Engine()._signal(make_input(), ProposalPattern.none, 0.0) == _HEALTHY
def test_signal_healthy_below_20(): assert "healthy" in Engine()._signal(make_input(), ProposalPattern.none, 19.99)
def test_signal_at_20_not_healthy(): assert "healthy" not in Engine()._signal(make_input(), ProposalPattern.none, 20.0)
def test_signal_close_pct(): assert "65% proposals close" in Engine()._signal(make_input(proposal_to_close_rate_pct=0.65), ProposalPattern.none, 20.0)
def test_signal_ghost_pct(): assert "5% unanswered" in Engine()._signal(make_input(unanswered_proposal_rate_pct=0.05), ProposalPattern.none, 20.0)
def test_signal_custom_pct(): assert "80% customization score" in Engine()._signal(make_input(proposal_customization_score=0.80), ProposalPattern.none, 20.0)
def test_signal_composite_int(): assert "composite 42" in Engine()._signal(make_input(), ProposalPattern.none, 42.0)
def test_signal_premature_label(): assert "Premature proposer" in Engine()._signal(make_input(), ProposalPattern.premature_proposer, 50.0)
def test_signal_template_label(): assert "Template lazy" in Engine()._signal(make_input(), ProposalPattern.template_lazy, 50.0)
def test_signal_ghosted_label(): assert "Ghosted proposer" in Engine()._signal(make_input(), ProposalPattern.ghosted_proposer, 50.0)
def test_signal_revision_label(): assert "Revision looper" in Engine()._signal(make_input(), ProposalPattern.revision_looper, 50.0)
def test_signal_orphaned_label(): assert "Orphaned proposal" in Engine()._signal(make_input(), ProposalPattern.orphaned_proposal, 50.0)
def test_signal_none_label(): assert "None" in Engine()._signal(make_input(), ProposalPattern.none, 25.0)

# ---------------------------------------------------------------------------
# 16. assess() end-to-end
# ---------------------------------------------------------------------------
def test_assess_returns_result(): assert isinstance(eng().assess(make_input()), ProposalResult)
def test_assess_low_risk_default(): assert eng().assess(make_input()).proposal_risk == ProposalRisk.low
def test_assess_converting_default(): assert eng().assess(make_input()).proposal_severity == ProposalSeverity.converting
def test_assess_no_action_default(): assert eng().assess(make_input()).recommended_action == ProposalAction.no_action
def test_assess_none_pattern_default(): assert eng().assess(make_input()).proposal_pattern == ProposalPattern.none
def test_assess_no_gap_default(): assert not eng().assess(make_input()).has_proposal_gap
def test_assess_rep_id(): assert eng().assess(make_input(rep_id="REPX")).rep_id == "REPX"
def test_assess_region(): assert eng().assess(make_input(region="LATAM")).region == "LATAM"
def test_assess_composite_float(): assert isinstance(eng().assess(make_input()).proposal_composite, float)
def test_assess_deal_loss_float(): assert isinstance(eng().assess(make_input()).estimated_deal_loss_usd, float)
def test_assess_signal_str(): assert isinstance(eng().assess(make_input()).proposal_signal, str)
def test_assess_composite_nonneg(): assert eng().assess(make_input()).proposal_composite >= 0
def test_assess_quality_nonneg(): assert eng().assess(make_input()).quality_score >= 0
def test_assess_readiness_nonneg(): assert eng().assess(make_input()).readiness_score >= 0
def test_assess_execution_nonneg(): assert eng().assess(make_input()).execution_score >= 0
def test_assess_alignment_nonneg(): assert eng().assess(make_input()).alignment_score >= 0
def test_assess_accumulates():
    e = eng(); e.assess(make_input()); e.assess(make_input(rep_id="R2"))
    assert len(e._results) == 2
def test_assess_critical_worst_case():
    r = eng().assess(make_input(
        proposal_customization_score=0.10, value_articulation_score=0.10, roi_case_included_rate_pct=0.10,
        proposal_sent_without_discovery_rate_pct=0.90, executive_sponsor_present_in_proposal_pct=0.05,
        mutual_success_plan_inclusion_rate_pct=0.05, unanswered_proposal_rate_pct=0.60,
        proposal_revision_count_avg=6.0, avg_days_to_send_proposal=25.0,
        proposal_champion_alignment_score=0.05, multi_stakeholder_proposal_rate_pct=0.05,
        competitive_differentiation_score=0.05))
    assert r.proposal_risk == ProposalRisk.critical
def test_assess_composite_le_100():
    r = eng().assess(make_input(
        proposal_customization_score=0.01, value_articulation_score=0.01, roi_case_included_rate_pct=0.01,
        proposal_sent_without_discovery_rate_pct=0.99, executive_sponsor_present_in_proposal_pct=0.01,
        mutual_success_plan_inclusion_rate_pct=0.01, unanswered_proposal_rate_pct=0.99,
        proposal_revision_count_avg=9.0, avg_days_to_send_proposal=30.0,
        proposal_champion_alignment_score=0.01, multi_stakeholder_proposal_rate_pct=0.01,
        competitive_differentiation_score=0.01))
    assert r.proposal_composite <= 100.0

# ---------------------------------------------------------------------------
# 17. assess_batch()
# ---------------------------------------------------------------------------
def test_batch_returns_list(): assert isinstance(eng().assess_batch([make_input()]), list)
def test_batch_empty(): assert eng().assess_batch([]) == []
def test_batch_length():
    e = eng(); assert len(e.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])) == 5
def test_batch_each_result():
    assert isinstance(eng().assess_batch([make_input()])[0], ProposalResult)
def test_batch_accumulates():
    e = eng(); e.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
    assert e.summary()["total"] == 3

# ---------------------------------------------------------------------------
# 18. summary()
# ---------------------------------------------------------------------------
_SUMMARY_KEYS = {"total","risk_counts","pattern_counts","severity_counts","action_counts",
    "avg_proposal_composite","proposal_gap_count","coaching_count","avg_quality_score",
    "avg_readiness_score","avg_execution_score","avg_alignment_score","total_estimated_deal_loss_usd"}

def test_summary_empty_13_keys(): assert len(eng().summary()) == 13
def test_summary_empty_keys(): assert set(eng().summary().keys()) == _SUMMARY_KEYS
def test_summary_empty_total(): assert eng().summary()["total"] == 0
def test_summary_empty_composite(): assert eng().summary()["avg_proposal_composite"] == 0.0
def test_summary_empty_gap(): assert eng().summary()["proposal_gap_count"] == 0
def test_summary_empty_coaching(): assert eng().summary()["coaching_count"] == 0
def test_summary_empty_deal_loss(): assert eng().summary()["total_estimated_deal_loss_usd"] == 0.0
def test_summary_empty_risk_counts(): assert eng().summary()["risk_counts"] == {}
def test_summary_empty_pattern_counts(): assert eng().summary()["pattern_counts"] == {}
def test_summary_empty_severity_counts(): assert eng().summary()["severity_counts"] == {}
def test_summary_empty_action_counts(): assert eng().summary()["action_counts"] == {}
def test_summary_total_count():
    e = eng(); [e.assess(make_input(rep_id=f"R{i}")) for i in range(4)]
    assert e.summary()["total"] == 4
def test_summary_risk_low():
    e = eng(); e.assess(make_input()); assert e.summary()["risk_counts"]["low"] == 1
def test_summary_pattern_none():
    e = eng(); e.assess(make_input()); assert e.summary()["pattern_counts"]["none"] == 1
def test_summary_severity_converting():
    e = eng(); e.assess(make_input()); assert e.summary()["severity_counts"]["converting"] == 1
def test_summary_action_no_action():
    e = eng(); e.assess(make_input()); assert e.summary()["action_counts"]["no_action"] == 1
def test_summary_avg_composite_rounded():
    e = eng(); e.assess(make_input()); v = e.summary()["avg_proposal_composite"]
    assert v == round(v, 1)
def test_summary_avg_quality_rounded():
    e = eng(); e.assess(make_input()); v = e.summary()["avg_quality_score"]
    assert v == round(v, 1)
def test_summary_avg_readiness_rounded():
    e = eng(); e.assess(make_input()); v = e.summary()["avg_readiness_score"]
    assert v == round(v, 1)
def test_summary_avg_execution_rounded():
    e = eng(); e.assess(make_input()); v = e.summary()["avg_execution_score"]
    assert v == round(v, 1)
def test_summary_avg_alignment_rounded():
    e = eng(); e.assess(make_input()); v = e.summary()["avg_alignment_score"]
    assert v == round(v, 1)
def test_summary_deal_loss_rounded():
    e = eng(); e.assess(make_input()); v = e.summary()["total_estimated_deal_loss_usd"]
    assert v == round(v, 2)
def test_summary_gap_count():
    e = eng(); e.assess(make_input(proposal_to_close_rate_pct=0.20)); e.assess(make_input())
    assert e.summary()["proposal_gap_count"] == 1
def test_summary_coaching_count():
    e = eng(); e.assess(make_input(proposal_customization_score=0.30)); e.assess(make_input())
    assert e.summary()["coaching_count"] == 1
def test_summary_after_batch():
    e = eng(); e.assess_batch([make_input(rep_id=f"R{i}") for i in range(6)])
    assert e.summary()["total"] == 6
def test_summary_13_keys_after_assess():
    e = eng(); e.assess(make_input()); assert set(e.summary().keys()) == _SUMMARY_KEYS

# ---------------------------------------------------------------------------
# 19. Edge cases
# ---------------------------------------------------------------------------
def test_zero_deal_value_no_loss(): assert eng().assess(make_input(avg_deal_value_usd=0.0)).estimated_deal_loss_usd == 0.0
def test_zero_proposals_no_loss(): assert eng().assess(make_input(total_proposals_sent=0)).estimated_deal_loss_usd == 0.0
def test_perfect_close_no_loss(): assert eng().assess(make_input(proposal_to_close_rate_pct=1.0)).estimated_deal_loss_usd == 0.0
def test_all_max_composite_is_100():
    r = eng().assess(make_input(
        proposal_customization_score=0.20, value_articulation_score=0.25, roi_case_included_rate_pct=0.30,
        proposal_sent_without_discovery_rate_pct=0.55, executive_sponsor_present_in_proposal_pct=0.20,
        mutual_success_plan_inclusion_rate_pct=0.20, unanswered_proposal_rate_pct=0.50,
        proposal_revision_count_avg=5.0, avg_days_to_send_proposal=21.0,
        proposal_champion_alignment_score=0.20, multi_stakeholder_proposal_rate_pct=0.20,
        competitive_differentiation_score=0.20))
    assert r.proposal_composite == 100.0
def test_many_assess_accumulate():
    e = eng(); [e.assess(make_input()) for _ in range(10)]
    assert e.summary()["total"] == 10
def test_coaching_false_boundary():
    assert not Engine()._requires_coaching(make_input(proposal_customization_score=0.51,
        proposal_sent_without_discovery_rate_pct=0.05), 24.99)
def test_gap_false_at_boundary():
    assert not Engine()._has_gap(make_input(proposal_to_close_rate_pct=0.26,
        unanswered_proposal_rate_pct=0.29), 39.99)
def test_deal_loss_type():
    r = eng().assess(make_input())
    assert isinstance(r.estimated_deal_loss_usd, float)
def test_result_is_dataclass():
    r = eng().assess(make_input())
    assert hasattr(r, '__dataclass_fields__')
def test_healthy_signal_content():
    r = eng().assess(make_input())
    assert "customization" in r.proposal_signal and "discovery" in r.proposal_signal

# ---------------------------------------------------------------------------
# 20. Additional parametrized quality boundary tests
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("custom,expected_contrib", [
    (0.19, 40), (0.20, 40), (0.21, 22), (0.44, 22), (0.45, 22),
    (0.46, 8), (0.64, 8), (0.65, 8), (0.66, 0), (0.99, 0),
])
def test_quality_customization_boundaries(custom, expected_contrib):
    e = Engine()
    s = e._quality_score(make_input(proposal_customization_score=custom,
        value_articulation_score=0.90, roi_case_included_rate_pct=0.90))
    assert s == expected_contrib

@pytest.mark.parametrize("va,expected_contrib", [
    (0.10, 35), (0.25, 35), (0.26, 18), (0.54, 18), (0.55, 18), (0.56, 0), (0.99, 0),
])
def test_quality_value_articulation_boundaries(va, expected_contrib):
    e = Engine()
    s = e._quality_score(make_input(proposal_customization_score=0.90,
        value_articulation_score=va, roi_case_included_rate_pct=0.90))
    assert s == expected_contrib

@pytest.mark.parametrize("roi,expected_contrib", [
    (0.10, 25), (0.30, 25), (0.31, 12), (0.54, 12), (0.55, 12), (0.56, 0), (0.90, 0),
])
def test_quality_roi_boundaries(roi, expected_contrib):
    e = Engine()
    s = e._quality_score(make_input(proposal_customization_score=0.90,
        value_articulation_score=0.90, roi_case_included_rate_pct=roi))
    assert s == expected_contrib

# ---------------------------------------------------------------------------
# 21. Additional parametrized execution boundary tests
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("unans,expected_contrib", [
    (0.50, 45), (0.51, 45), (0.30, 25), (0.31, 25), (0.15, 10), (0.16, 10), (0.14, 0),
])
def test_execution_unanswered_boundaries(unans, expected_contrib):
    e = Engine()
    s = e._execution_score(make_input(unanswered_proposal_rate_pct=unans,
        proposal_revision_count_avg=0.5, avg_days_to_send_proposal=5.0))
    assert s == expected_contrib
