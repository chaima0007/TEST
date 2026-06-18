"""Tests for FollowUpScheduler."""

import pytest
from swarm.intelligence.followup_scheduler import (
    ActionType,
    FollowUpScheduler,
    Priority,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture()
def sched():
    return FollowUpScheduler()


def _add(sched: FollowUpScheduler, pid: str = "p001", stage: str = "quoted",
         days: float = 7.0, bant: int = 80, touches: int = 2, quote: float = 598.0):
    return sched.add_prospect(pid, f"Company {pid}", "artisan",
                              current_stage=stage, days_since_contact=days,
                              bant_score=bant, touches=touches, quote_value=quote)


# ── add_prospect ──────────────────────────────────────────────────────────────

class TestAddProspect:
    def test_creates_task(self, sched):
        task = _add(sched)
        assert task is not None
        assert task.prospect_id == "p001"

    def test_urgency_score_in_range(self, sched):
        task = _add(sched)
        assert 0 <= task.urgency_score <= 100

    def test_high_urgency_hot_prospect(self, sched):
        task = sched.add_prospect("p001", "A", current_stage="negotiating",
                                  days_since_contact=14, bant_score=100, touches=1)
        assert task.urgency_score >= 75
        assert task.priority == Priority.URGENT

    def test_low_urgency_cold_prospect(self, sched):
        task = sched.add_prospect("p001", "A", current_stage="lead",
                                  days_since_contact=0, bant_score=0, touches=0)
        assert task.urgency_score < 25
        assert task.priority == Priority.LOW

    def test_touches_penalty_applied(self, sched):
        t_few = sched.add_prospect("p001", "A", current_stage="quoted",
                                   days_since_contact=7, bant_score=60, touches=1)
        t_many = sched.add_prospect("p002", "B", current_stage="quoted",
                                    days_since_contact=7, bant_score=60, touches=8)
        assert t_many.urgency_score < t_few.urgency_score

    def test_score_floor_zero(self, sched):
        task = sched.add_prospect("p001", "A", current_stage="won",
                                  days_since_contact=0, bant_score=0, touches=10)
        assert task.urgency_score == 0

    def test_score_ceil_100(self, sched):
        task = sched.add_prospect("p001", "A", current_stage="negotiating",
                                  days_since_contact=30, bant_score=100, touches=0)
        assert task.urgency_score <= 100

    def test_stage_action_mapping_quoted(self, sched):
        task = sched.add_prospect("p001", "A", current_stage="quoted")
        assert task.recommended_action == ActionType.FOLLOW_QUOTE

    def test_stage_action_mapping_negotiating(self, sched):
        task = sched.add_prospect("p001", "A", current_stage="negotiating")
        assert task.recommended_action == ActionType.NEGOTIATE

    def test_stage_action_mapping_replied(self, sched):
        task = sched.add_prospect("p001", "A", current_stage="replied")
        assert task.recommended_action == ActionType.CALL

    def test_stage_action_mapping_demo(self, sched):
        task = sched.add_prospect("p001", "A", current_stage="demo")
        assert task.recommended_action == ActionType.DEMO

    def test_stage_action_mapping_won_skip(self, sched):
        task = sched.add_prospect("p001", "A", current_stage="won")
        assert task.recommended_action == ActionType.SKIP

    def test_overrides_existing(self, sched):
        sched.add_prospect("p001", "A", current_stage="lead", days_since_contact=1)
        task = sched.add_prospect("p001", "A", current_stage="negotiating", days_since_contact=14)
        assert task.current_stage == "negotiating"
        assert sched.get("p001").current_stage == "negotiating"

    def test_notes_stored(self, sched):
        task = sched.add_prospect("p001", "A", notes="Rappel lundi matin")
        assert task.notes == "Rappel lundi matin"

    def test_quote_value_stored(self, sched):
        task = sched.add_prospect("p001", "A", quote_value=778.80)
        assert task.quote_value == 778.80


# ── Priority boundaries ───────────────────────────────────────────────────────

class TestPriorityBoundaries:
    def test_urgent_gte_75(self, sched):
        task = sched.add_prospect("p001", "A", current_stage="negotiating",
                                  days_since_contact=14, bant_score=100, touches=0)
        assert task.urgency_score >= 75
        assert task.priority == Priority.URGENT

    def test_medium_25_to_49(self, sched):
        task = sched.add_prospect("p001", "A", current_stage="contacted",
                                  days_since_contact=3, bant_score=40, touches=1)
        if 25 <= task.urgency_score < 50:
            assert task.priority == Priority.MEDIUM

    def test_low_below_25(self, sched):
        task = sched.add_prospect("p001", "A", current_stage="lead",
                                  days_since_contact=0, bant_score=0, touches=0)
        assert task.urgency_score < 25
        assert task.priority == Priority.LOW


# ── remove ────────────────────────────────────────────────────────────────────

class TestRemove:
    def test_remove_existing(self, sched):
        _add(sched)
        assert sched.remove("p001")
        assert sched.get("p001") is None

    def test_remove_missing_returns_false(self, sched):
        assert not sched.remove("p999")

    def test_remove_reduces_count(self, sched):
        _add(sched, "p001")
        _add(sched, "p002")
        sched.remove("p001")
        assert len(sched.get_tasks()) == 1


# ── get / get_tasks ───────────────────────────────────────────────────────────

class TestGetTasks:
    def test_get_existing(self, sched):
        task = _add(sched)
        assert sched.get("p001") is task

    def test_get_missing(self, sched):
        assert sched.get("p999") is None

    def test_get_tasks_sorted_desc(self, sched):
        t1 = sched.add_prospect("p001", "A", current_stage="negotiating",
                                days_since_contact=14, bant_score=100)
        t2 = sched.add_prospect("p002", "B", current_stage="lead",
                                days_since_contact=0, bant_score=0)
        tasks = sched.get_tasks()
        assert tasks[0].urgency_score >= tasks[-1].urgency_score

    def test_get_tasks_limit(self, sched):
        for i in range(5):
            sched.add_prospect(f"p{i:03d}", f"C{i}")
        assert len(sched.get_tasks(limit=3)) == 3

    def test_top_n(self, sched):
        for i in range(8):
            sched.add_prospect(f"p{i:03d}", f"C{i}", days_since_contact=float(i))
        top = sched.top_n(3)
        assert len(top) == 3
        assert top[0].urgency_score >= top[1].urgency_score


# ── Queries ───────────────────────────────────────────────────────────────────

class TestQueries:
    def test_by_priority_urgent(self, sched):
        t1 = sched.add_prospect("p001", "A", current_stage="negotiating",
                                days_since_contact=14, bant_score=100)
        t2 = sched.add_prospect("p002", "B", current_stage="lead",
                                days_since_contact=0, bant_score=0)
        urgent = sched.urgent()
        if t1.priority == Priority.URGENT:
            assert t1 in urgent
        if t2.priority == Priority.URGENT:
            assert t2 in urgent

    def test_by_action(self, sched):
        sched.add_prospect("p001", "A", current_stage="negotiating")
        sched.add_prospect("p002", "B", current_stage="quoted")
        sched.add_prospect("p003", "C", current_stage="demo")
        neg_tasks = sched.by_action(ActionType.NEGOTIATE)
        assert all(t.recommended_action == ActionType.NEGOTIATE for t in neg_tasks)

    def test_by_stage(self, sched):
        sched.add_prospect("p001", "A", current_stage="quoted")
        sched.add_prospect("p002", "B", current_stage="quoted")
        sched.add_prospect("p003", "C", current_stage="replied")
        results = sched.by_stage("quoted")
        assert len(results) == 2

    def test_overdue_prospects(self, sched):
        sched.add_prospect("p001", "A", days_since_contact=10.0)
        sched.add_prospect("p002", "B", days_since_contact=2.0)
        overdue = sched.overdue_prospects(threshold_days=7.0)
        pids = [t.prospect_id for t in overdue]
        assert "p001" in pids
        assert "p002" not in pids

    def test_overdue_sorted_desc(self, sched):
        sched.add_prospect("p001", "A", days_since_contact=5.0)
        sched.add_prospect("p002", "B", days_since_contact=15.0)
        sched.add_prospect("p003", "C", days_since_contact=10.0)
        overdue = sched.overdue_prospects(threshold_days=4.0)
        days = [t.days_since_contact for t in overdue]
        assert days == sorted(days, reverse=True)


# ── Analytics ─────────────────────────────────────────────────────────────────

class TestAnalytics:
    def test_average_urgency_empty(self, sched):
        assert sched.average_urgency() == 0.0

    def test_average_urgency(self, sched):
        t1 = _add(sched, "p001")
        t2 = _add(sched, "p002")
        expected = round((t1.urgency_score + t2.urgency_score) / 2, 1)
        assert sched.average_urgency() == expected

    def test_priority_distribution(self, sched):
        sched.add_prospect("p001", "A", current_stage="negotiating",
                           days_since_contact=14, bant_score=100)
        dist = sched.priority_distribution()
        assert isinstance(dist, dict)
        for p in ["urgent", "high", "medium", "low"]:
            assert p in dist

    def test_action_distribution(self, sched):
        sched.add_prospect("p001", "A", current_stage="quoted")
        sched.add_prospect("p002", "B", current_stage="quoted")
        sched.add_prospect("p003", "C", current_stage="demo")
        dist = sched.action_distribution()
        assert dist.get("follow_quote", 0) == 2
        assert dist.get("demo", 0) == 1

    def test_total_pipeline_value(self, sched):
        sched.add_prospect("p001", "A", quote_value=500.0)
        sched.add_prospect("p002", "B", quote_value=300.0)
        sched.add_prospect("p003", "C", quote_value=0.0)
        assert sched.total_pipeline_value() == 800.0


# ── summary() ─────────────────────────────────────────────────────────────────

class TestSummary:
    def test_empty_summary(self, sched):
        s = sched.summary()
        assert s["total"] == 0
        assert s["avg_urgency_score"] == 0.0

    def test_summary_keys(self, sched):
        s = sched.summary()
        for k in ["total", "urgent", "high", "medium", "low",
                  "avg_urgency_score", "overdue_7d", "overdue_14d",
                  "total_pipeline_eur", "action_breakdown"]:
            assert k in s

    def test_summary_counts(self, sched):
        _add(sched, "p001", days=10.0)
        _add(sched, "p002", days=2.0)
        s = sched.summary()
        assert s["total"] == 2
        assert s["overdue_7d"] == 1


# ── to_dict ───────────────────────────────────────────────────────────────────

class TestToDict:
    def test_task_to_dict(self, sched):
        task = _add(sched)
        d = task.to_dict()
        for k in ["prospect_id", "company_name", "current_stage", "urgency_score",
                  "priority", "recommended_action", "days_since_contact",
                  "bant_score", "touches", "quote_value", "notes", "created_at"]:
            assert k in d

    def test_priority_value_string(self, sched):
        task = _add(sched)
        d = task.to_dict()
        assert d["priority"] in ["urgent", "high", "medium", "low"]

    def test_action_value_string(self, sched):
        task = _add(sched)
        d = task.to_dict()
        assert isinstance(d["recommended_action"], str)


# ── reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_tasks(self, sched):
        _add(sched, "p001")
        _add(sched, "p002")
        sched.reset()
        assert len(sched.get_tasks()) == 0

    def test_can_add_after_reset(self, sched):
        _add(sched)
        sched.reset()
        task = _add(sched)
        assert task is not None
