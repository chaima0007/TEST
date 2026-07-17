"""Tests for LeadPrioritizer intelligence module."""

import pytest
from swarm.intelligence.lead_prioritizer import (
    LeadPriority,
    LeadSignals,
    LeadPrioritizer,
    _recency_score,
    _value_score,
    _activity_score,
    _pipeline_health_score,
    _compute_breakdown,
    _compute_priority_score,
    _classify_priority,
    _compute_risk_flags,
)


# ─── Fixtures ────────────────────────────────────────────────────────────────

def hot_signals():
    return LeadSignals(
        lead_id="l001",
        name="Jean Martin",
        company="Cabinet Dupont",
        sector="avocat",
        days_since_last_contact=1,
        response_rate=0.85,
        deal_value_eur=1200.0,
        days_in_pipeline=10,
        open_rate=0.75,
        meetings_completed=4,
        proposal_sent=True,
    )


def cold_signals():
    return LeadSignals(
        lead_id="l002",
        name="Marie Leclerc",
        company="Resto Le Zinc",
        sector="restaurant",
        days_since_last_contact=25,
        response_rate=0.10,
        deal_value_eur=200.0,
        days_in_pipeline=55,
        open_rate=0.08,
        meetings_completed=0,
        proposal_sent=False,
    )


def warm_signals():
    return LeadSignals(
        lead_id="l003",
        name="Pierre Blanc",
        company="PME Solutions",
        sector="pme",
        days_since_last_contact=5,
        response_rate=0.50,
        deal_value_eur=800.0,
        days_in_pipeline=20,
        open_rate=0.45,
        meetings_completed=2,
        proposal_sent=False,
    )


@pytest.fixture
def prio():
    return LeadPrioritizer()


@pytest.fixture
def prio_with_leads(prio):
    prio.add_lead(hot_signals())
    prio.add_lead(cold_signals())
    prio.add_lead(warm_signals())
    return prio


# ─── TestLeadSignals ──────────────────────────────────────────────────────────

class TestLeadSignals:
    def test_to_dict_keys(self):
        s = hot_signals()
        d = s.to_dict()
        for key in ["lead_id", "name", "company", "sector", "days_since_last_contact",
                    "response_rate", "deal_value_eur", "days_in_pipeline",
                    "open_rate", "meetings_completed", "proposal_sent"]:
            assert key in d

    def test_to_dict_values(self):
        s = hot_signals()
        d = s.to_dict()
        assert d["lead_id"] == "l001"
        assert d["response_rate"] == 0.85
        assert d["proposal_sent"] is True

    def test_fields_stored(self):
        s = cold_signals()
        assert s.days_since_last_contact == 25
        assert s.meetings_completed == 0
        assert s.proposal_sent is False


# ─── TestScoringHelpers ───────────────────────────────────────────────────────

class TestScoringHelpers:
    def test_recency_fresh(self):
        assert _recency_score(0) == 100.0
        assert _recency_score(3) == 100.0

    def test_recency_recent(self):
        assert _recency_score(5) == 85.0
        assert _recency_score(7) == 85.0

    def test_recency_penalty(self):
        score_8 = _recency_score(8)
        score_14 = _recency_score(14)
        assert score_8 < 85.0
        assert score_14 < score_8

    def test_recency_floor(self):
        assert _recency_score(100) == 0.0

    def test_value_score_zero(self):
        assert _value_score(0) == 0.0

    def test_value_score_caps_at_100(self):
        assert _value_score(2000) == 100.0
        assert _value_score(10000) == 100.0

    def test_value_score_proportional(self):
        assert _value_score(1000) == 50.0
        assert _value_score(500) == 25.0

    def test_activity_zero(self):
        assert _activity_score(0) == 0.0

    def test_activity_caps(self):
        assert _activity_score(5) == 100.0
        assert _activity_score(10) == 100.0

    def test_activity_proportional(self):
        assert _activity_score(2) == 40.0
        assert _activity_score(3) == 60.0

    def test_pipeline_health_proposal_sent(self):
        score = _pipeline_health_score(10, True)
        assert score == 100.0

    def test_pipeline_health_no_proposal(self):
        score = _pipeline_health_score(10, False)
        assert score == 70.0

    def test_pipeline_health_penalty_over_30(self):
        score_30 = _pipeline_health_score(30, True)
        score_40 = _pipeline_health_score(40, True)
        assert score_30 == 100.0
        assert score_40 < 100.0

    def test_pipeline_health_floor(self):
        assert _pipeline_health_score(200, False) == 0.0


# ─── TestBreakdown ────────────────────────────────────────────────────────────

class TestBreakdown:
    def test_breakdown_keys(self):
        b = _compute_breakdown(hot_signals())
        for key in ["recency", "responsiveness", "deal_value", "engagement", "activity", "pipeline_health"]:
            assert key in b

    def test_breakdown_values_range(self):
        for signals in [hot_signals(), cold_signals(), warm_signals()]:
            b = _compute_breakdown(signals)
            for v in b.values():
                assert 0.0 <= v <= 100.0

    def test_responsiveness_from_response_rate(self):
        b = _compute_breakdown(hot_signals())
        assert b["responsiveness"] == pytest.approx(85.0)

    def test_engagement_from_open_rate(self):
        b = _compute_breakdown(hot_signals())
        assert b["engagement"] == pytest.approx(75.0)


# ─── TestPriorityScore ────────────────────────────────────────────────────────

class TestPriorityScore:
    def test_score_range(self):
        for signals in [hot_signals(), cold_signals(), warm_signals()]:
            b = _compute_breakdown(signals)
            score = _compute_priority_score(b)
            assert 0.0 <= score <= 100.0

    def test_hot_scores_higher(self):
        b_hot = _compute_breakdown(hot_signals())
        b_cold = _compute_breakdown(cold_signals())
        assert _compute_priority_score(b_hot) > _compute_priority_score(b_cold)

    def test_score_clamped(self):
        all_100 = {k: 100.0 for k in ["recency", "responsiveness", "deal_value", "engagement", "activity", "pipeline_health"]}
        assert _compute_priority_score(all_100) == 100.0

    def test_score_zero(self):
        all_0 = {k: 0.0 for k in ["recency", "responsiveness", "deal_value", "engagement", "activity", "pipeline_health"]}
        assert _compute_priority_score(all_0) == 0.0


# ─── TestClassify ─────────────────────────────────────────────────────────────

class TestClassify:
    def test_hot_threshold(self):
        assert _classify_priority(70.0) == LeadPriority.HOT
        assert _classify_priority(100.0) == LeadPriority.HOT
        assert _classify_priority(75.0) == LeadPriority.HOT

    def test_warm_threshold(self):
        assert _classify_priority(50.0) == LeadPriority.WARM
        assert _classify_priority(69.9) == LeadPriority.WARM

    def test_cold_threshold(self):
        assert _classify_priority(30.0) == LeadPriority.COLD
        assert _classify_priority(49.9) == LeadPriority.COLD

    def test_dormant_threshold(self):
        assert _classify_priority(0.0) == LeadPriority.DORMANT
        assert _classify_priority(29.9) == LeadPriority.DORMANT


# ─── TestRiskFlags ────────────────────────────────────────────────────────────

class TestRiskFlags:
    def test_no_flags_for_hot_lead(self):
        s = hot_signals()
        from swarm.intelligence.lead_prioritizer import _compute_breakdown
        b = _compute_breakdown(s)
        flags = _compute_risk_flags(s, b)
        assert flags == []

    def test_stale_contact_flag(self):
        s = cold_signals()
        b = _compute_breakdown(s)
        flags = _compute_risk_flags(s, b)
        assert any("contact" in f.lower() for f in flags)

    def test_low_response_rate_flag(self):
        s = cold_signals()
        b = _compute_breakdown(s)
        flags = _compute_risk_flags(s, b)
        assert any("réponse" in f.lower() for f in flags)

    def test_long_pipeline_flag(self):
        s = cold_signals()
        b = _compute_breakdown(s)
        flags = _compute_risk_flags(s, b)
        assert any("pipeline" in f.lower() for f in flags)

    def test_no_proposal_flag(self):
        s = cold_signals()
        b = _compute_breakdown(s)
        flags = _compute_risk_flags(s, b)
        assert any("devis" in f.lower() for f in flags)

    def test_low_open_rate_flag(self):
        s = cold_signals()
        b = _compute_breakdown(s)
        flags = _compute_risk_flags(s, b)
        assert any("ouverture" in f.lower() for f in flags)


# ─── TestLeadPrioritizer ──────────────────────────────────────────────────────

class TestLeadPrioritizer:
    def test_add_lead_returns_prioritized(self, prio):
        result = prio.add_lead(hot_signals())
        assert result.priority_score >= 0
        assert result.priority_tier in list(LeadPriority)
        assert result.action_items

    def test_add_lead_stores(self, prio):
        prio.add_lead(hot_signals())
        assert prio.get("l001") is not None

    def test_get_missing_returns_none(self, prio):
        assert prio.get("nonexistent") is None

    def test_all_leads_sorted(self, prio_with_leads):
        leads = prio_with_leads.all_leads()
        scores = [l.priority_score for l in leads]
        assert scores == sorted(scores, reverse=True)

    def test_all_leads_count(self, prio_with_leads):
        assert len(prio_with_leads.all_leads()) == 3

    def test_hot_leads_filter(self, prio_with_leads):
        hot = prio_with_leads.hot_leads()
        assert all(h.priority_tier == LeadPriority.HOT for h in hot)

    def test_by_tier_hot(self, prio_with_leads):
        hot = prio_with_leads.by_tier(LeadPriority.HOT)
        assert all(h.priority_tier == LeadPriority.HOT for h in hot)

    def test_by_tier_cold(self, prio_with_leads):
        cold = prio_with_leads.by_tier(LeadPriority.COLD)
        assert all(c.priority_tier == LeadPriority.COLD for c in cold)

    def test_stale_leads(self, prio_with_leads):
        stale = prio_with_leads.stale_leads(threshold=30)
        for s in stale:
            assert s.signals.days_in_pipeline >= 30

    def test_stale_default_threshold(self, prio_with_leads):
        stale = prio_with_leads.stale_leads()
        for s in stale:
            assert s.signals.days_in_pipeline >= 30

    def test_at_risk(self, prio_with_leads):
        at_risk = prio_with_leads.at_risk()
        assert all(len(p.risk_flags) > 0 for p in at_risk)

    def test_sector_stats(self, prio_with_leads):
        stats = prio_with_leads.sector_stats("avocat")
        assert stats["sector"] == "avocat"
        assert stats["count"] == 1
        assert stats["hot_count"] >= 0
        assert stats["total_deal_value_eur"] == 1200.0

    def test_sector_stats_empty(self, prio_with_leads):
        stats = prio_with_leads.sector_stats("nonexistent")
        assert stats["count"] == 0
        assert stats["avg_priority_score"] == 0.0

    def test_summary_keys(self, prio_with_leads):
        s = prio_with_leads.summary()
        for key in ["total", "tier_counts", "avg_score", "total_pipeline_value", "at_risk_count"]:
            assert key in s

    def test_summary_total(self, prio_with_leads):
        s = prio_with_leads.summary()
        assert s["total"] == 3

    def test_summary_tier_counts_sum(self, prio_with_leads):
        s = prio_with_leads.summary()
        assert sum(s["tier_counts"].values()) == 3

    def test_summary_pipeline_value(self, prio_with_leads):
        s = prio_with_leads.summary()
        assert s["total_pipeline_value"] == pytest.approx(1200.0 + 200.0 + 800.0)

    def test_reset(self, prio_with_leads):
        prio_with_leads.reset()
        assert prio_with_leads.all_leads() == []
        assert prio_with_leads.summary()["total"] == 0

    def test_re_score_same_id(self, prio):
        s1 = hot_signals()
        s2 = hot_signals()
        s2.days_since_last_contact = 30
        prio.add_lead(s1)
        prio.add_lead(s2)
        assert prio.get("l001").signals.days_since_last_contact == 30

    def test_to_dict_shape(self, prio):
        result = prio.add_lead(hot_signals())
        d = result.to_dict()
        for key in ["signals", "priority_score", "priority_tier", "score_breakdown", "action_items", "risk_flags"]:
            assert key in d

    def test_action_items_non_empty(self, prio):
        for signals in [hot_signals(), cold_signals(), warm_signals()]:
            result = prio.add_lead(signals)
            assert len(result.action_items) > 0
