"""
Follow-Up Scheduler — produces a ranked daily action list for all active prospects.

Combines signals from multiple intelligence modules:
  - Days since last contact (recency)
  - Funnel stage (stage-level urgency)
  - BANT qualification score (prospect value)
  - Number of previous touches (respects limits)

Each prospect gets an urgency score (0–100) and a recommended action.

Recommended actions:
  CALL        — hot/warm prospect, phone follow-up
  EMAIL       — send personalised follow-up email
  DEMO        — schedule or confirm demo
  SEND_QUOTE  — generate and send quote
  FOLLOW_QUOTE— follow up on sent quote
  NEGOTIATE   — negotiate terms
  CHECK_IN    — light-touch check-in for cool/cold prospects
  CLOSE       — final closing push
  SKIP        — prospect is stuck, no action recommended
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional


# ── Enums ─────────────────────────────────────────────────────────────────────

class ActionType(str, Enum):
    CALL         = "call"
    EMAIL        = "email"
    DEMO         = "demo"
    SEND_QUOTE   = "send_quote"
    FOLLOW_QUOTE = "follow_quote"
    NEGOTIATE    = "negotiate"
    CHECK_IN     = "check_in"
    CLOSE        = "close"
    SKIP         = "skip"


class Priority(str, Enum):
    URGENT  = "urgent"   # Act today — score ≥ 75
    HIGH    = "high"     # Act this week — score ≥ 50
    MEDIUM  = "medium"   # Act within 2 weeks — score ≥ 25
    LOW     = "low"      # When available — score < 25


# ── Stage-level urgency + recommended actions ─────────────────────────────────

_STAGE_URGENCY: Dict[str, int] = {
    "negotiating": 25,   # Hot — close now
    "quoted":      20,
    "demo":        18,
    "replied":     15,
    "opened":      10,
    "contacted":   8,
    "lead":        5,
    "won":         0,
    "lost":        0,
}

_STAGE_ACTION: Dict[str, ActionType] = {
    "lead":        ActionType.EMAIL,
    "contacted":   ActionType.EMAIL,
    "opened":      ActionType.EMAIL,
    "replied":     ActionType.CALL,
    "demo":        ActionType.DEMO,
    "quoted":      ActionType.FOLLOW_QUOTE,
    "negotiating": ActionType.NEGOTIATE,
    "won":         ActionType.SKIP,
    "lost":        ActionType.SKIP,
}


def _recency_urgency(days_since_contact: float) -> int:
    """0–40 based on how long since last touch."""
    if days_since_contact >= 14:
        return 40
    if days_since_contact >= 7:
        return 30
    if days_since_contact >= 3:
        return 15
    if days_since_contact >= 1:
        return 8
    return 0


def _bant_urgency(bant_score: int) -> int:
    """0–25 from BANT score (0–100)."""
    return round(bant_score / 4)


def _touches_penalty(touches: int) -> int:
    """Negative penalty for over-contacted prospects."""
    if touches >= 8:
        return -20
    if touches >= 5:
        return -10
    if touches >= 3:
        return -3
    return 0


# ── Follow-up task ────────────────────────────────────────────────────────────

@dataclass
class FollowUpTask:
    prospect_id:         str
    company_name:        str
    sector:              str
    current_stage:       str
    urgency_score:       int              # 0–100
    priority:            Priority
    recommended_action:  ActionType
    days_since_contact:  float
    bant_score:          int              # 0–100
    touches:             int
    quote_value:         float            # EUR, 0 if no quote
    notes:               str = ""
    created_at:          datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "prospect_id":        self.prospect_id,
            "company_name":       self.company_name,
            "sector":             self.sector,
            "current_stage":      self.current_stage,
            "urgency_score":      self.urgency_score,
            "priority":           self.priority.value,
            "recommended_action": self.recommended_action.value,
            "days_since_contact": self.days_since_contact,
            "bant_score":         self.bant_score,
            "touches":            self.touches,
            "quote_value":        self.quote_value,
            "notes":              self.notes,
            "created_at":         self.created_at.isoformat(),
        }


# ── Scheduler ─────────────────────────────────────────────────────────────────

class FollowUpScheduler:
    """
    Builds a ranked daily action list from prospect data.

    Urgency score = recency (0–40) + stage urgency (0–25) + BANT (0–25) + touches penalty (≤0)
    Cap: 0–100.

    Usage::
        sched = FollowUpScheduler()
        sched.add_prospect(
            prospect_id="p001",
            company_name="Plomberie Martin",
            sector="artisan",
            current_stage="quoted",
            days_since_contact=5.0,
            bant_score=80,
            touches=3,
            quote_value=598.80,
        )
        tasks = sched.get_tasks()  # sorted by urgency_score desc
    """

    def __init__(self) -> None:
        self._tasks: Dict[str, FollowUpTask] = {}

    # ── Add / update ──────────────────────────────────────────────────────────

    def add_prospect(
        self,
        prospect_id: str,
        company_name: str,
        sector: str = "",
        current_stage: str = "lead",
        days_since_contact: float = 0.0,
        bant_score: int = 0,
        touches: int = 0,
        quote_value: float = 0.0,
        notes: str = "",
        ts: Optional[datetime] = None,
    ) -> FollowUpTask:
        raw = (
            _recency_urgency(days_since_contact)
            + _STAGE_URGENCY.get(current_stage, 0)
            + _bant_urgency(bant_score)
            + _touches_penalty(touches)
        )
        score = max(0, min(100, raw))

        if score >= 75:
            priority = Priority.URGENT
        elif score >= 50:
            priority = Priority.HIGH
        elif score >= 25:
            priority = Priority.MEDIUM
        else:
            priority = Priority.LOW

        action = _STAGE_ACTION.get(current_stage, ActionType.EMAIL)

        task = FollowUpTask(
            prospect_id=prospect_id,
            company_name=company_name,
            sector=sector,
            current_stage=current_stage,
            urgency_score=score,
            priority=priority,
            recommended_action=action,
            days_since_contact=days_since_contact,
            bant_score=bant_score,
            touches=touches,
            quote_value=quote_value,
            notes=notes,
            created_at=ts or datetime.utcnow(),
        )
        self._tasks[prospect_id] = task
        return task

    def remove(self, prospect_id: str) -> bool:
        if prospect_id in self._tasks:
            del self._tasks[prospect_id]
            return True
        return False

    # ── Queries ───────────────────────────────────────────────────────────────

    def get(self, prospect_id: str) -> Optional[FollowUpTask]:
        return self._tasks.get(prospect_id)

    def get_tasks(self, limit: Optional[int] = None) -> List[FollowUpTask]:
        """All tasks sorted by urgency_score descending."""
        sorted_tasks = sorted(self._tasks.values(), key=lambda t: t.urgency_score, reverse=True)
        return sorted_tasks[:limit] if limit else sorted_tasks

    def by_priority(self, priority: Priority) -> List[FollowUpTask]:
        return sorted(
            [t for t in self._tasks.values() if t.priority == priority],
            key=lambda t: t.urgency_score,
            reverse=True,
        )

    def urgent(self) -> List[FollowUpTask]:
        return self.by_priority(Priority.URGENT)

    def by_action(self, action: ActionType) -> List[FollowUpTask]:
        return [t for t in self._tasks.values() if t.recommended_action == action]

    def by_stage(self, stage: str) -> List[FollowUpTask]:
        return [t for t in self._tasks.values() if t.current_stage == stage]

    def top_n(self, n: int = 10) -> List[FollowUpTask]:
        return self.get_tasks(limit=n)

    # ── Analytics ─────────────────────────────────────────────────────────────

    def priority_distribution(self) -> Dict[str, int]:
        counts = {p.value: 0 for p in Priority}
        for t in self._tasks.values():
            counts[t.priority.value] += 1
        return counts

    def action_distribution(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for t in self._tasks.values():
            k = t.recommended_action.value
            counts[k] = counts.get(k, 0) + 1
        return counts

    def average_urgency(self) -> float:
        if not self._tasks:
            return 0.0
        return round(sum(t.urgency_score for t in self._tasks.values()) / len(self._tasks), 1)

    def overdue_prospects(self, threshold_days: float = 7.0) -> List[FollowUpTask]:
        """Prospects not contacted in more than threshold_days."""
        return sorted(
            [t for t in self._tasks.values() if t.days_since_contact >= threshold_days],
            key=lambda t: t.days_since_contact,
            reverse=True,
        )

    def total_pipeline_value(self) -> float:
        return round(sum(t.quote_value for t in self._tasks.values() if t.quote_value > 0), 2)

    def summary(self) -> dict:
        dist = self.priority_distribution()
        return {
            "total":              len(self._tasks),
            "urgent":             dist["urgent"],
            "high":               dist["high"],
            "medium":             dist["medium"],
            "low":                dist["low"],
            "avg_urgency_score":  self.average_urgency(),
            "overdue_7d":         len(self.overdue_prospects(7.0)),
            "overdue_14d":        len(self.overdue_prospects(14.0)),
            "total_pipeline_eur": self.total_pipeline_value(),
            "action_breakdown":   self.action_distribution(),
        }

    # ── Reset ─────────────────────────────────────────────────────────────────

    def reset(self) -> None:
        self._tasks.clear()
