"""Tests for WorkflowOrchestrator."""

import pytest
from intelligence.workflow_orchestrator import (
    DecisionConfidence,
    DivisionTarget,
    ProspectSignals,
    WorkflowAction,
    WorkflowDecision,
    WorkflowOrchestrator,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture()
def orch():
    return WorkflowOrchestrator()


def _sig(**kwargs) -> ProspectSignals:
    defaults = dict(
        prospect_id="p001",
        company_name="Test Co",
        sector="artisan",
        funnel_stage="lead",
        bant_score=50,
        days_since_contact=3.0,
        touches=1,
        buying_signal=0.0,
        objection_type="none",
        negotiation_status="",
        quote_sent=False,
        invoice_sent=False,
        is_lost=False,
    )
    defaults.update(kwargs)
    return ProspectSignals(**defaults)


# ── Output structure ──────────────────────────────────────────────────────────

class TestDecideOutput:
    def test_returns_workflow_decision(self, orch):
        d = orch.decide(_sig())
        assert isinstance(d, WorkflowDecision)

    def test_decision_has_prospect_id(self, orch):
        d = orch.decide(_sig(prospect_id="p123"))
        assert d.prospect_id == "p123"

    def test_urgency_score_in_range(self, orch):
        d = orch.decide(_sig())
        assert 0 <= d.urgency_score <= 100

    def test_division_is_valid_enum(self, orch):
        d = orch.decide(_sig())
        assert isinstance(d.division, DivisionTarget)

    def test_action_is_valid_enum(self, orch):
        d = orch.decide(_sig())
        assert isinstance(d.action, WorkflowAction)

    def test_confidence_is_valid_enum(self, orch):
        d = orch.decide(_sig())
        assert isinstance(d.confidence, DecisionConfidence)

    def test_reasoning_not_empty(self, orch):
        d = orch.decide(_sig())
        assert d.reasoning and len(d.reasoning) > 5

    def test_agent_id_not_empty(self, orch):
        d = orch.decide(_sig())
        assert d.agent_id and "." in d.agent_id

    def test_to_dict_has_all_keys(self, orch):
        d = orch.decide(_sig())
        dd = d.to_dict()
        for k in ["prospect_id", "company_name", "division", "agent_id", "action",
                  "urgency_score", "confidence", "reasoning", "signals_used", "created_at"]:
            assert k in dd

    def test_to_dict_action_is_string(self, orch):
        d = orch.decide(_sig())
        assert isinstance(d.to_dict()["action"], str)

    def test_to_dict_division_is_string(self, orch):
        d = orch.decide(_sig())
        assert isinstance(d.to_dict()["division"], str)


# ── Rule 1 — Lost ─────────────────────────────────────────────────────────────

class TestRuleLost:
    def test_is_lost_flag(self, orch):
        d = orch.decide(_sig(is_lost=True))
        assert d.action == WorkflowAction.ARCHIVE

    def test_lost_stage(self, orch):
        d = orch.decide(_sig(funnel_stage="lost"))
        assert d.action == WorkflowAction.ARCHIVE

    def test_lost_routes_to_division_6(self, orch):
        d = orch.decide(_sig(is_lost=True))
        assert d.division == DivisionTarget.BRANDING


# ── Rule 2 — Won ──────────────────────────────────────────────────────────────

class TestRuleWon:
    def test_won_no_invoice_triggers_generate(self, orch):
        d = orch.decide(_sig(funnel_stage="won", invoice_sent=False))
        assert d.action == WorkflowAction.GENERATE_INVOICE
        assert d.division == DivisionTarget.FINANCE

    def test_won_invoice_sent_triggers_close(self, orch):
        d = orch.decide(_sig(funnel_stage="won", invoice_sent=True))
        assert d.action == WorkflowAction.CLOSE
        assert d.division == DivisionTarget.PRODUCTION


# ── Rule 3 — Negotiating ──────────────────────────────────────────────────────

class TestRuleNegotiating:
    def test_negotiating_stage_triggers_negotiate(self, orch):
        d = orch.decide(_sig(funnel_stage="negotiating"))
        assert d.action == WorkflowAction.NEGOTIATE

    def test_negotiation_status_in_progress(self, orch):
        d = orch.decide(_sig(funnel_stage="contacted", negotiation_status="in_progress"))
        assert d.action == WorkflowAction.NEGOTIATE

    def test_failed_negotiation_triggers_nurture(self, orch):
        d = orch.decide(_sig(funnel_stage="negotiating", negotiation_status="failed"))
        assert d.action == WorkflowAction.NURTURE
        assert d.division == DivisionTarget.NEGOTIATION

    def test_high_buying_signal_in_negotiation_triggers_close(self, orch):
        d = orch.decide(_sig(funnel_stage="negotiating", buying_signal=0.75))
        assert d.action == WorkflowAction.CLOSE


# ── Rule 4 — Quoted ──────────────────────────────────────────────────────────

class TestRuleQuoted:
    def test_quoted_overdue_triggers_urgent_followup(self, orch):
        d = orch.decide(_sig(funnel_stage="quoted", days_since_contact=16.0))
        assert d.action == WorkflowAction.FOLLOW_UP_QUOTE
        assert d.division == DivisionTarget.NEGOTIATION

    def test_quoted_5plus_days_triggers_followup(self, orch):
        d = orch.decide(_sig(funnel_stage="quoted", days_since_contact=7.0))
        assert d.action == WorkflowAction.FOLLOW_UP_QUOTE

    def test_quoted_recent_triggers_wait(self, orch):
        d = orch.decide(_sig(funnel_stage="quoted", days_since_contact=2.0))
        assert d.action == WorkflowAction.WAIT

    def test_quote_sent_flag(self, orch):
        d = orch.decide(_sig(quote_sent=True, days_since_contact=6.0))
        assert d.action == WorkflowAction.FOLLOW_UP_QUOTE


# ── Rule 5 — Demo ─────────────────────────────────────────────────────────────

class TestRuleDemo:
    def test_demo_stage_triggers_schedule_demo(self, orch):
        d = orch.decide(_sig(funnel_stage="demo"))
        assert d.action == WorkflowAction.SCHEDULE_DEMO
        assert d.division == DivisionTarget.NEGOTIATION


# ── Rule 6 — Replied with buying signal ──────────────────────────────────────

class TestRuleBuyingSignal:
    def test_replied_high_bant_high_signal_sends_quote(self, orch):
        d = orch.decide(_sig(funnel_stage="replied", buying_signal=0.75, bant_score=80))
        assert d.action == WorkflowAction.SEND_QUOTE
        assert d.division == DivisionTarget.FINANCE

    def test_replied_medium_bant_signal_schedules_demo(self, orch):
        d = orch.decide(_sig(funnel_stage="replied", buying_signal=0.75, bant_score=40))
        assert d.action == WorkflowAction.SCHEDULE_DEMO


# ── Rule 7 — Objections ───────────────────────────────────────────────────────

class TestRuleObjections:
    def test_price_objection_routes_to_negotiation(self, orch):
        d = orch.decide(_sig(funnel_stage="replied", objection_type="price"))
        assert d.action == WorkflowAction.HANDLE_OBJECTION
        assert d.division == DivisionTarget.NEGOTIATION

    def test_trust_objection_routes_to_agent_3_2(self, orch):
        d = orch.decide(_sig(funnel_stage="replied", objection_type="trust"))
        assert d.agent_id == "3.2"

    def test_timing_objection_routes_to_agent_3_5(self, orch):
        d = orch.decide(_sig(funnel_stage="replied", objection_type="timing"))
        assert d.agent_id == "3.5"

    def test_competitor_objection_routes_to_agent_3_1(self, orch):
        d = orch.decide(_sig(funnel_stage="replied", objection_type="competitor"))
        assert d.agent_id == "3.1"

    def test_technical_objection_routes_to_agent_3_4(self, orch):
        d = orch.decide(_sig(funnel_stage="replied", objection_type="technical"))
        assert d.agent_id == "3.4"

    def test_objection_in_signals_used(self, orch):
        d = orch.decide(_sig(funnel_stage="replied", objection_type="price"))
        assert "objection_type" in d.signals_used


# ── Rule 8 — Replied no signal ────────────────────────────────────────────────

class TestRuleRepliedNoSignal:
    def test_replied_no_signal_sends_followup(self, orch):
        d = orch.decide(_sig(funnel_stage="replied", buying_signal=0.0, objection_type="none"))
        assert d.action == WorkflowAction.SEND_FOLLOWUP_EMAIL
        assert d.division == DivisionTarget.OUTREACH


# ── Rule 9 — Contacted / opened ──────────────────────────────────────────────

class TestRuleContactedOpened:
    def test_contacted_overdue_triggers_followup(self, orch):
        d = orch.decide(_sig(funnel_stage="contacted", days_since_contact=8.0))
        assert d.action == WorkflowAction.SEND_FOLLOWUP_EMAIL

    def test_opened_recent_triggers_wait(self, orch):
        d = orch.decide(_sig(funnel_stage="opened", days_since_contact=2.0))
        assert d.action == WorkflowAction.WAIT

    def test_contacted_routes_to_outreach(self, orch):
        d = orch.decide(_sig(funnel_stage="contacted", days_since_contact=10.0))
        assert d.division == DivisionTarget.OUTREACH


# ── Rule 10 — Lead ───────────────────────────────────────────────────────────

class TestRuleLead:
    def test_lead_low_bant_triggers_enrich(self, orch):
        d = orch.decide(_sig(funnel_stage="lead", bant_score=10))
        assert d.action == WorkflowAction.ENRICH_PROSPECT
        assert d.division == DivisionTarget.DETECTION

    def test_lead_high_bant_triggers_first_email(self, orch):
        d = orch.decide(_sig(funnel_stage="lead", bant_score=50))
        assert d.action == WorkflowAction.SEND_FIRST_EMAIL
        assert d.division == DivisionTarget.OUTREACH

    def test_lead_bant_threshold_is_25(self, orch):
        low = orch.decide(_sig(funnel_stage="lead", bant_score=24))
        high = orch.decide(_sig(funnel_stage="lead", bant_score=25, prospect_id="p002"))
        assert low.action == WorkflowAction.ENRICH_PROSPECT
        assert high.action == WorkflowAction.SEND_FIRST_EMAIL


# ── decide_batch ─────────────────────────────────────────────────────────────

class TestDecideBatch:
    def test_returns_list(self, orch):
        sigs = [_sig(prospect_id=f"p{i:03d}") for i in range(5)]
        results = orch.decide_batch(sigs)
        assert isinstance(results, list)
        assert len(results) == 5

    def test_sorted_descending_urgency(self, orch):
        sigs = [
            _sig(prospect_id="p001", funnel_stage="negotiating", bant_score=100, days_since_contact=14),
            _sig(prospect_id="p002", funnel_stage="lead", bant_score=0, days_since_contact=0),
        ]
        results = orch.decide_batch(sigs)
        assert results[0].urgency_score >= results[1].urgency_score

    def test_empty_batch(self, orch):
        assert orch.decide_batch([]) == []

    def test_decisions_stored(self, orch):
        sigs = [_sig(prospect_id="p001"), _sig(prospect_id="p002", company_name="X")]
        orch.decide_batch(sigs)
        assert orch.get("p001") is not None
        assert orch.get("p002") is not None


# ── get / get_queue ───────────────────────────────────────────────────────────

class TestGetters:
    def test_get_existing(self, orch):
        orch.decide(_sig(prospect_id="p001"))
        assert orch.get("p001") is not None

    def test_get_missing(self, orch):
        assert orch.get("p999") is None

    def test_get_queue_sorted(self, orch):
        orch.decide(_sig(prospect_id="p001", funnel_stage="lead", bant_score=0))
        orch.decide(_sig(prospect_id="p002", funnel_stage="negotiating", bant_score=100, days_since_contact=14))
        queue = orch.get_queue()
        assert queue[0].urgency_score >= queue[-1].urgency_score

    def test_get_queue_limit(self, orch):
        for i in range(6):
            orch.decide(_sig(prospect_id=f"p{i:03d}"))
        assert len(orch.get_queue(limit=3)) == 3

    def test_by_division(self, orch):
        orch.decide(_sig(prospect_id="p001", funnel_stage="won", invoice_sent=False))
        results = orch.by_division(DivisionTarget.FINANCE)
        assert len(results) >= 1

    def test_by_action(self, orch):
        orch.decide(_sig(prospect_id="p001", is_lost=True))
        results = orch.by_action(WorkflowAction.ARCHIVE)
        assert len(results) == 1

    def test_by_confidence(self, orch):
        orch.decide(_sig(prospect_id="p001"))
        results = orch.by_confidence(DecisionConfidence.HIGH)
        assert isinstance(results, list)


# ── Overwrite ────────────────────────────────────────────────────────────────

class TestOverwrite:
    def test_decide_overwrites_existing(self, orch):
        orch.decide(_sig(funnel_stage="lead"))
        d2 = orch.decide(_sig(funnel_stage="negotiating"))
        assert d2.action == WorkflowAction.NEGOTIATE
        assert orch.get("p001").action == WorkflowAction.NEGOTIATE


# ── Analytics ────────────────────────────────────────────────────────────────

class TestAnalytics:
    def test_average_urgency_empty(self, orch):
        assert orch.average_urgency() == 0.0

    def test_average_urgency(self, orch):
        orch.decide(_sig(prospect_id="p001"))
        orch.decide(_sig(prospect_id="p002", funnel_stage="negotiating", bant_score=100))
        avg = orch.average_urgency()
        assert avg > 0

    def test_division_distribution(self, orch):
        orch.decide(_sig(prospect_id="p001", funnel_stage="won"))
        orch.decide(_sig(prospect_id="p002", funnel_stage="lead", bant_score=10))
        dist = orch.division_distribution()
        assert isinstance(dist, dict)
        assert sum(dist.values()) == 2

    def test_action_distribution(self, orch):
        orch.decide(_sig(prospect_id="p001", is_lost=True))
        orch.decide(_sig(prospect_id="p002", is_lost=True, company_name="B"))
        dist = orch.action_distribution()
        assert dist.get("archive", 0) == 2

    def test_confidence_distribution(self, orch):
        orch.decide(_sig(prospect_id="p001"))
        dist = orch.confidence_distribution()
        assert isinstance(dist, dict)
        assert sum(dist.values()) >= 1

    def test_summary_keys(self, orch):
        orch.decide(_sig())
        s = orch.summary()
        for k in ["total", "avg_urgency_score", "division_distribution",
                  "action_distribution", "confidence_distribution"]:
            assert k in s

    def test_summary_total(self, orch):
        for i in range(4):
            orch.decide(_sig(prospect_id=f"p{i:03d}"))
        assert orch.summary()["total"] == 4


# ── Reset ────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_decisions(self, orch):
        orch.decide(_sig())
        orch.reset()
        assert len(orch.get_queue()) == 0
        assert orch.average_urgency() == 0.0

    def test_can_decide_after_reset(self, orch):
        orch.decide(_sig())
        orch.reset()
        d = orch.decide(_sig())
        assert d is not None
