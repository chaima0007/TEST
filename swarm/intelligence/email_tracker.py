"""
Email open/click rate tracker for Division 2 outreach campaigns.
Stores events in-memory with optional Redis backend.
Computes per-campaign and per-agent metrics for A/B test feedback.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ── Events ────────────────────────────────────────────────────────────────────

@dataclass
class TrackingEvent:
    event_id: str
    campaign_id: str
    email_id: str
    agent_id: str
    sector: str
    event_type: str          # "sent" | "open" | "click" | "reply" | "unsubscribe"
    timestamp: float = field(default_factory=time.time)
    metadata: Dict = field(default_factory=dict)


@dataclass
class CampaignMetrics:
    campaign_id: str
    agent_id: str
    sector: str
    sent: int = 0
    opens: int = 0
    clicks: int = 0
    replies: int = 0
    unsubscribes: int = 0

    @property
    def open_rate(self) -> float:
        return self.opens / self.sent if self.sent else 0.0

    @property
    def click_rate(self) -> float:
        return self.clicks / self.sent if self.sent else 0.0

    @property
    def reply_rate(self) -> float:
        return self.replies / self.sent if self.sent else 0.0

    @property
    def conversion_score(self) -> float:
        """Weighted engagement: reply > click > open."""
        return (
            self.reply_rate * 0.60
            + self.click_rate * 0.25
            + self.open_rate * 0.15
        )

    def to_dict(self) -> dict:
        return {
            "campaign_id": self.campaign_id,
            "agent_id": self.agent_id,
            "sector": self.sector,
            "sent": self.sent,
            "opens": self.opens,
            "clicks": self.clicks,
            "replies": self.replies,
            "unsubscribes": self.unsubscribes,
            "open_rate": round(self.open_rate, 4),
            "click_rate": round(self.click_rate, 4),
            "reply_rate": round(self.reply_rate, 4),
            "conversion_score": round(self.conversion_score, 4),
        }


# ── Tracker ───────────────────────────────────────────────────────────────────

class EmailTracker:
    """
    Tracks open/click/reply events per email campaign and agent.
    Thread-safe for single-process use; swap _store for Redis in production.
    """

    VALID_EVENTS = frozenset({"sent", "open", "click", "reply", "unsubscribe"})

    def __init__(self):
        self._events: List[TrackingEvent] = []
        self._metrics: Dict[str, CampaignMetrics] = {}  # campaign_id → metrics

    # ── Core tracking ──────────────────────────────────────────────────────────

    def track(
        self,
        campaign_id: str,
        email_id: str,
        agent_id: str,
        sector: str,
        event_type: str,
        metadata: Optional[dict] = None,
    ) -> TrackingEvent:
        if event_type not in self.VALID_EVENTS:
            raise ValueError(f"Unknown event_type '{event_type}'. Valid: {self.VALID_EVENTS}")

        event = TrackingEvent(
            event_id=self._make_event_id(campaign_id, email_id, event_type),
            campaign_id=campaign_id,
            email_id=email_id,
            agent_id=agent_id,
            sector=sector,
            event_type=event_type,
            metadata=metadata or {},
        )
        self._events.append(event)
        self._update_metrics(event)
        return event

    def _update_metrics(self, event: TrackingEvent) -> None:
        cid = event.campaign_id
        if cid not in self._metrics:
            self._metrics[cid] = CampaignMetrics(
                campaign_id=cid,
                agent_id=event.agent_id,
                sector=event.sector,
            )
        m = self._metrics[cid]
        if event.event_type == "sent":
            m.sent += 1
        elif event.event_type == "open":
            m.opens += 1
        elif event.event_type == "click":
            m.clicks += 1
        elif event.event_type == "reply":
            m.replies += 1
        elif event.event_type == "unsubscribe":
            m.unsubscribes += 1

    # ── Pixel / link helpers ───────────────────────────────────────────────────

    def tracking_pixel_url(self, base_url: str, campaign_id: str, email_id: str) -> str:
        """Return 1×1 GIF URL to embed in HTML emails for open tracking."""
        return f"{base_url}/track/open?cid={campaign_id}&eid={email_id}"

    def tracked_link(self, base_url: str, campaign_id: str, email_id: str, destination: str) -> str:
        """Wrap a destination URL for click tracking."""
        import urllib.parse
        dest_encoded = urllib.parse.quote(destination, safe="")
        return f"{base_url}/track/click?cid={campaign_id}&eid={email_id}&url={dest_encoded}"

    # ── Queries ────────────────────────────────────────────────────────────────

    def get_metrics(self, campaign_id: str) -> Optional[CampaignMetrics]:
        return self._metrics.get(campaign_id)

    def get_agent_metrics(self, agent_id: str) -> List[CampaignMetrics]:
        return [m for m in self._metrics.values() if m.agent_id == agent_id]

    def get_sector_metrics(self, sector: str) -> List[CampaignMetrics]:
        return [m for m in self._metrics.values() if m.sector.lower() == sector.lower()]

    def get_events(self, campaign_id: Optional[str] = None) -> List[TrackingEvent]:
        if campaign_id is None:
            return list(self._events)
        return [e for e in self._events if e.campaign_id == campaign_id]

    def top_campaigns(self, n: int = 10) -> List[CampaignMetrics]:
        """Return top-N campaigns ranked by conversion_score."""
        return sorted(
            self._metrics.values(),
            key=lambda m: m.conversion_score,
            reverse=True,
        )[:n]

    def agent_leaderboard(self) -> List[dict]:
        """Aggregate metrics per agent_id, ranked by avg conversion_score."""
        by_agent: Dict[str, List[CampaignMetrics]] = {}
        for m in self._metrics.values():
            by_agent.setdefault(m.agent_id, []).append(m)

        rows = []
        for agent_id, campaigns in by_agent.items():
            total_sent = sum(c.sent for c in campaigns)
            total_opens = sum(c.opens for c in campaigns)
            total_clicks = sum(c.clicks for c in campaigns)
            total_replies = sum(c.replies for c in campaigns)
            conv = (
                (total_replies / total_sent * 0.60)
                + (total_clicks / total_sent * 0.25)
                + (total_opens / total_sent * 0.15)
            ) if total_sent else 0.0
            rows.append({
                "agent_id": agent_id,
                "campaigns": len(campaigns),
                "total_sent": total_sent,
                "total_opens": total_opens,
                "total_replies": total_replies,
                "conversion_score": round(conv, 4),
            })

        return sorted(rows, key=lambda r: r["conversion_score"], reverse=True)

    def summary(self) -> dict:
        """Global summary across all tracked campaigns."""
        all_metrics = list(self._metrics.values())
        if not all_metrics:
            return {"campaigns": 0, "emails_sent": 0, "open_rate": 0.0, "reply_rate": 0.0}
        total_sent = sum(m.sent for m in all_metrics)
        total_opens = sum(m.opens for m in all_metrics)
        total_replies = sum(m.replies for m in all_metrics)
        return {
            "campaigns": len(all_metrics),
            "emails_sent": total_sent,
            "open_rate": round(total_opens / total_sent, 4) if total_sent else 0.0,
            "reply_rate": round(total_replies / total_sent, 4) if total_sent else 0.0,
            "total_opens": total_opens,
            "total_replies": total_replies,
        }

    def reset(self) -> None:
        self._events.clear()
        self._metrics.clear()

    # ── Internal ───────────────────────────────────────────────────────────────

    @staticmethod
    def _make_event_id(campaign_id: str, email_id: str, event_type: str) -> str:
        raw = f"{campaign_id}:{email_id}:{event_type}:{time.time_ns()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
