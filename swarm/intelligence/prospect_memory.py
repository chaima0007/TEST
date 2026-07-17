"""
Prospect Memory — persists the interaction history of each prospect across cycles.

Tracks per-prospect:
  - Every message exchanged (inbound/outbound)
  - Sentiment evolution over time
  - Objections raised and how they were handled
  - Touch count and last-contact date
  - Deal stage progression
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


# ── Enums ─────────────────────────────────────────────────────────────────────

class MessageDirection(str, Enum):
    OUTBOUND = "outbound"    # swarm → prospect
    INBOUND  = "inbound"     # prospect → swarm


class DealStage(str, Enum):
    DETECTED      = "detected"       # scraped, not yet contacted
    CONTACTED     = "contacted"      # first email sent
    OPENED        = "opened"         # email opened, no reply
    REPLIED       = "replied"        # prospect responded
    NEGOTIATING   = "negotiating"    # active negotiation thread
    QUOTED        = "quoted"         # quote sent / Stripe link shared
    WON           = "won"            # payment confirmed
    LOST          = "lost"           # declined or went cold
    UNSUBSCRIBED  = "unsubscribed"   # opt-out received


# ── Models ────────────────────────────────────────────────────────────────────

@dataclass
class Message:
    direction: MessageDirection
    content: str
    timestamp: datetime.datetime
    agent_id: str = ""
    sentiment: str = ""          # positif / négatif / neutre / …
    objection_type: str = ""     # price / trust / timing / none / …

    def to_dict(self) -> dict:
        return {
            "direction": self.direction.value,
            "content": self.content[:500],   # truncate for storage
            "timestamp": self.timestamp.isoformat(),
            "agent_id": self.agent_id,
            "sentiment": self.sentiment,
            "objection_type": self.objection_type,
        }


@dataclass
class SentimentSnapshot:
    sentiment: str
    score: float         # 0.0 (very negative) → 1.0 (very positive)
    timestamp: datetime.datetime

    def to_dict(self) -> dict:
        return {
            "sentiment": self.sentiment,
            "score": round(self.score, 3),
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class ProspectRecord:
    """Full memory for a single prospect."""
    prospect_id: str
    company_name: str
    sector: str
    email: str
    created_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    stage: DealStage = DealStage.DETECTED
    messages: List[Message] = field(default_factory=list)
    sentiment_history: List[SentimentSnapshot] = field(default_factory=list)
    objections_seen: List[str] = field(default_factory=list)   # e.g. ["price", "timing"]
    tags: List[str] = field(default_factory=list)
    assigned_agent: str = ""
    quote_eur: float = 0.0
    notes: str = ""
    last_contacted_at: Optional[datetime.datetime] = None

    # ── Computed properties ───────────────────────────────────────────────────

    @property
    def touch_count(self) -> int:
        return sum(1 for m in self.messages if m.direction == MessageDirection.OUTBOUND)

    @property
    def reply_count(self) -> int:
        return sum(1 for m in self.messages if m.direction == MessageDirection.INBOUND)

    @property
    def latest_sentiment(self) -> Optional[str]:
        return self.sentiment_history[-1].sentiment if self.sentiment_history else None

    @property
    def sentiment_trend(self) -> str:
        """'improving' | 'declining' | 'stable' | 'unknown'"""
        if len(self.sentiment_history) < 2:
            return "unknown"
        last  = self.sentiment_history[-1].score
        first = self.sentiment_history[0].score
        delta = last - first
        if delta > 0.15:
            return "improving"
        if delta < -0.15:
            return "declining"
        return "stable"

    @property
    def days_since_contact(self) -> Optional[float]:
        if not self.last_contacted_at:
            return None
        return (datetime.datetime.utcnow() - self.last_contacted_at).total_seconds() / 86400

    # ── Mutation helpers ──────────────────────────────────────────────────────

    def add_message(
        self,
        direction: MessageDirection,
        content: str,
        agent_id: str = "",
        sentiment: str = "",
        objection_type: str = "",
        timestamp: Optional[datetime.datetime] = None,
    ) -> Message:
        ts = timestamp or datetime.datetime.utcnow()
        msg = Message(
            direction=direction,
            content=content,
            timestamp=ts,
            agent_id=agent_id,
            sentiment=sentiment,
            objection_type=objection_type,
        )
        self.messages.append(msg)
        if direction == MessageDirection.OUTBOUND:
            self.last_contacted_at = ts
        if objection_type and objection_type not in ("none", "") and objection_type not in self.objections_seen:
            self.objections_seen.append(objection_type)
        return msg

    def record_sentiment(self, sentiment: str, score: float, timestamp: Optional[datetime.datetime] = None) -> None:
        self.sentiment_history.append(SentimentSnapshot(
            sentiment=sentiment,
            score=max(0.0, min(1.0, score)),
            timestamp=timestamp or datetime.datetime.utcnow(),
        ))

    def advance_stage(self, new_stage: DealStage) -> None:
        self.stage = new_stage

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    # ── Serialisation ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "prospect_id": self.prospect_id,
            "company_name": self.company_name,
            "sector": self.sector,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "stage": self.stage.value,
            "touch_count": self.touch_count,
            "reply_count": self.reply_count,
            "latest_sentiment": self.latest_sentiment,
            "sentiment_trend": self.sentiment_trend,
            "objections_seen": self.objections_seen,
            "tags": self.tags,
            "assigned_agent": self.assigned_agent,
            "quote_eur": self.quote_eur,
            "notes": self.notes,
            "last_contacted_at": self.last_contacted_at.isoformat() if self.last_contacted_at else None,
            "message_count": len(self.messages),
            "messages": [m.to_dict() for m in self.messages[-5:]],   # last 5 only
            "sentiment_history": [s.to_dict() for s in self.sentiment_history],
        }

    def summary(self) -> str:
        """One-line human-readable summary."""
        return (
            f"{self.company_name} ({self.sector}) | "
            f"Stage: {self.stage.value} | "
            f"Touches: {self.touch_count} | "
            f"Replies: {self.reply_count} | "
            f"Trend: {self.sentiment_trend}"
        )


# ── Memory store ──────────────────────────────────────────────────────────────

class ProspectMemory:
    """
    Central in-memory store for all prospect interaction histories.
    Designed for in-process use; persistence to DB happens externally.
    """

    def __init__(self) -> None:
        self._records: Dict[str, ProspectRecord] = {}

    # ── CRUD ──────────────────────────────────────────────────────────────────

    def get_or_create(
        self,
        prospect_id: str,
        company_name: str = "",
        sector: str = "",
        email: str = "",
    ) -> ProspectRecord:
        if prospect_id not in self._records:
            self._records[prospect_id] = ProspectRecord(
                prospect_id=prospect_id,
                company_name=company_name,
                sector=sector,
                email=email,
            )
        return self._records[prospect_id]

    def get(self, prospect_id: str) -> Optional[ProspectRecord]:
        return self._records.get(prospect_id)

    def upsert(self, record: ProspectRecord) -> None:
        self._records[record.prospect_id] = record

    def delete(self, prospect_id: str) -> bool:
        if prospect_id in self._records:
            del self._records[prospect_id]
            return True
        return False

    # ── Log interaction helpers ────────────────────────────────────────────────

    def log_outbound(
        self,
        prospect_id: str,
        content: str,
        agent_id: str = "",
        company_name: str = "",
        sector: str = "",
        email: str = "",
        timestamp: Optional[datetime.datetime] = None,
    ) -> Message:
        rec = self.get_or_create(prospect_id, company_name, sector, email)
        rec.advance_stage(DealStage.CONTACTED)
        return rec.add_message(
            MessageDirection.OUTBOUND, content, agent_id=agent_id, timestamp=timestamp
        )

    def log_inbound(
        self,
        prospect_id: str,
        content: str,
        sentiment: str = "",
        sentiment_score: float = 0.5,
        objection_type: str = "",
        agent_id: str = "",
        timestamp: Optional[datetime.datetime] = None,
    ) -> Message:
        rec = self.get_or_create(prospect_id)
        rec.advance_stage(DealStage.REPLIED)
        if sentiment:
            rec.record_sentiment(sentiment, sentiment_score, timestamp)
        return rec.add_message(
            MessageDirection.INBOUND,
            content,
            agent_id=agent_id,
            sentiment=sentiment,
            objection_type=objection_type,
            timestamp=timestamp,
        )

    # ── Queries ────────────────────────────────────────────────────────────────

    def by_stage(self, stage: DealStage) -> List[ProspectRecord]:
        return [r for r in self._records.values() if r.stage == stage]

    def by_sector(self, sector: str) -> List[ProspectRecord]:
        return [r for r in self._records.values() if sector.lower() in r.sector.lower()]

    def by_agent(self, agent_id: str) -> List[ProspectRecord]:
        return [r for r in self._records.values() if r.assigned_agent == agent_id]

    def with_objection(self, objection_type: str) -> List[ProspectRecord]:
        return [r for r in self._records.values() if objection_type in r.objections_seen]

    def cold_prospects(self, idle_days: float = 7.0) -> List[ProspectRecord]:
        """Contacted but no reply for more than `idle_days` days."""
        results = []
        for r in self._records.values():
            if r.stage in (DealStage.CONTACTED, DealStage.OPENED) and r.days_since_contact is not None:
                if r.days_since_contact >= idle_days:
                    results.append(r)
        return sorted(results, key=lambda r: r.days_since_contact or 0, reverse=True)

    def won_deals(self) -> List[ProspectRecord]:
        return self.by_stage(DealStage.WON)

    def active_negotiations(self) -> List[ProspectRecord]:
        return [r for r in self._records.values() if r.stage in (DealStage.NEGOTIATING, DealStage.QUOTED)]

    def top_by_reply_count(self, n: int = 10) -> List[ProspectRecord]:
        return sorted(self._records.values(), key=lambda r: r.reply_count, reverse=True)[:n]

    # ── Aggregate stats ────────────────────────────────────────────────────────

    def summary(self) -> dict:
        records = list(self._records.values())
        by_stage: Dict[str, int] = {}
        for r in records:
            by_stage[r.stage.value] = by_stage.get(r.stage.value, 0) + 1

        total_revenue = sum(r.quote_eur for r in records if r.stage == DealStage.WON)
        return {
            "total_prospects": len(records),
            "by_stage": by_stage,
            "active_negotiations": sum(1 for r in records if r.stage in (DealStage.NEGOTIATING, DealStage.QUOTED)),
            "won_deals": by_stage.get("won", 0),
            "total_won_revenue_eur": round(total_revenue, 2),
            "total_messages": sum(len(r.messages) for r in records),
            "avg_touches": round(sum(r.touch_count for r in records) / max(len(records), 1), 1),
        }

    # ── Reset ─────────────────────────────────────────────────────────────────

    def reset(self) -> None:
        self._records.clear()

    def all_records(self) -> List[ProspectRecord]:
        return list(self._records.values())

    def count(self) -> int:
        return len(self._records)
