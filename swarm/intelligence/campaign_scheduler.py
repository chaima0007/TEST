"""
Campaign Scheduler — plans and queues outreach campaigns per sector.

Determines:
  - Optimal send windows (best day/hour by sector)
  - Rate limits (max emails/hour to avoid spam filters)
  - Campaign batching (split large sectors into waves)
  - Priority ordering (Tier A prospects first)
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ── Constants ─────────────────────────────────────────────────────────────────

# Best send windows per sector category (day_of_week 0=Mon, hour in 24h)
_SECTOR_WINDOWS: Dict[str, List[Tuple[int, int]]] = {
    "artisan":       [(1, 7), (2, 7), (3, 8)],       # Tue-Thu early morning
    "restaurant":    [(1, 9), (2, 9), (0, 8)],        # Mon-Wed mid-morning
    "médical":       [(0, 8), (1, 8), (3, 8)],        # Mon/Tue/Thu morning
    "garage":        [(0, 8), (2, 8), (4, 9)],        # Mon/Wed/Fri
    "immobilier":    [(1, 10), (2, 10), (3, 10)],     # Tue-Thu mid-morning
    "juridique":     [(0, 9), (1, 9), (2, 9)],        # Mon-Wed professional hours
    "formation":     [(1, 8), (3, 8), (4, 8)],        # Tue/Thu/Fri
    "beauté":        [(1, 9), (2, 9), (4, 9)],        # Tue/Wed/Fri
    "association":   [(0, 10), (2, 10), (4, 10)],     # Mon/Wed/Fri mid-morning
    "default":       [(1, 9), (3, 9), (0, 8)],        # Tue/Thu/Mon
}

MAX_PER_HOUR = 150          # global rate limit
MAX_PER_SECTOR_PER_WAVE = 50  # max leads in a single batch to avoid domain-level blocks
MIN_HOURS_BETWEEN_WAVES = 4   # minimum gap between waves


# ── Models ────────────────────────────────────────────────────────────────────

@dataclass
class CampaignWave:
    wave_id: str
    sector: str
    agent_id: str
    email_count: int
    scheduled_at: datetime.datetime
    priority: str       # "urgent" | "high" | "normal" | "low"
    tier_filter: str    # "A" | "B" | "C" | "all"
    status: str = "pending"   # "pending" | "running" | "done" | "cancelled"

    def to_dict(self) -> dict:
        return {
            "wave_id": self.wave_id,
            "sector": self.sector,
            "agent_id": self.agent_id,
            "email_count": self.email_count,
            "scheduled_at": self.scheduled_at.isoformat(),
            "priority": self.priority,
            "tier_filter": self.tier_filter,
            "status": self.status,
        }


@dataclass
class CampaignPlan:
    plan_id: str
    created_at: datetime.datetime
    total_emails: int
    total_waves: int
    waves: List[CampaignWave] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "plan_id": self.plan_id,
            "created_at": self.created_at.isoformat(),
            "total_emails": self.total_emails,
            "total_waves": self.total_waves,
            "waves": [w.to_dict() for w in self.waves],
        }


# ── Scheduler ─────────────────────────────────────────────────────────────────

class CampaignScheduler:
    """
    Schedules outreach campaign waves with sector-aware send windows.
    Respects rate limits and minimum gaps between waves.
    """

    def __init__(
        self,
        max_per_hour: int = MAX_PER_HOUR,
        max_per_wave: int = MAX_PER_SECTOR_PER_WAVE,
        min_gap_hours: int = MIN_HOURS_BETWEEN_WAVES,
    ):
        self.max_per_hour = max_per_hour
        self.max_per_wave = max_per_wave
        self.min_gap_hours = min_gap_hours
        self._plans: Dict[str, CampaignPlan] = {}

    def plan(
        self,
        sector: str,
        total_leads: int,
        agent_id: str,
        tier_filter: str = "A",
        priority: str = "normal",
        start_from: Optional[datetime.datetime] = None,
    ) -> CampaignPlan:
        """Create a campaign plan with optimal wave scheduling."""
        if start_from is None:
            start_from = datetime.datetime.utcnow()

        waves_needed = max(1, (total_leads + self.max_per_wave - 1) // self.max_per_wave)
        plan_id = self._make_id(sector, agent_id)
        waves: List[CampaignWave] = []

        current_time = self._next_send_window(sector, start_from)

        for i in range(waves_needed):
            count = min(self.max_per_wave, total_leads - i * self.max_per_wave)
            wave = CampaignWave(
                wave_id=f"{plan_id}_w{i + 1}",
                sector=sector,
                agent_id=agent_id,
                email_count=count,
                scheduled_at=current_time,
                priority=priority,
                tier_filter=tier_filter,
            )
            waves.append(wave)
            current_time = self._next_send_window(
                sector,
                current_time + datetime.timedelta(hours=self.min_gap_hours),
            )

        plan = CampaignPlan(
            plan_id=plan_id,
            created_at=start_from,
            total_emails=total_leads,
            total_waves=waves_needed,
            waves=waves,
        )
        self._plans[plan_id] = plan
        return plan

    def plan_multi_sector(
        self,
        sector_volumes: Dict[str, int],
        agent_assignments: Optional[Dict[str, str]] = None,
        start_from: Optional[datetime.datetime] = None,
    ) -> List[CampaignPlan]:
        """Plan campaigns for multiple sectors sorted by priority."""
        if start_from is None:
            start_from = datetime.datetime.utcnow()
        if agent_assignments is None:
            agent_assignments = {}

        # Sort: higher volume → earlier (greedy)
        sorted_sectors = sorted(sector_volumes.items(), key=lambda x: x[1], reverse=True)

        plans = []
        offset = datetime.timedelta(hours=0)
        for sector, volume in sorted_sectors:
            agent = agent_assignments.get(sector, "2.1")
            plan = self.plan(
                sector=sector,
                total_leads=volume,
                agent_id=agent,
                start_from=start_from + offset,
            )
            plans.append(plan)
            offset += datetime.timedelta(hours=1)

        return plans

    def get_plan(self, plan_id: str) -> Optional[CampaignPlan]:
        return self._plans.get(plan_id)

    def list_plans(self) -> List[CampaignPlan]:
        return list(self._plans.values())

    def cancel_wave(self, plan_id: str, wave_id: str) -> bool:
        plan = self._plans.get(plan_id)
        if not plan:
            return False
        for wave in plan.waves:
            if wave.wave_id == wave_id:
                wave.status = "cancelled"
                return True
        return False

    def mark_wave_done(self, plan_id: str, wave_id: str) -> bool:
        plan = self._plans.get(plan_id)
        if not plan:
            return False
        for wave in plan.waves:
            if wave.wave_id == wave_id:
                wave.status = "done"
                return True
        return False

    def pending_waves(self, as_of: Optional[datetime.datetime] = None) -> List[CampaignWave]:
        """Return all pending waves scheduled up to now (or as_of)."""
        as_of = as_of or datetime.datetime.utcnow()
        result = []
        for plan in self._plans.values():
            for wave in plan.waves:
                if wave.status == "pending" and wave.scheduled_at <= as_of:
                    result.append(wave)
        return sorted(result, key=lambda w: w.scheduled_at)

    def summary(self) -> dict:
        all_waves = [w for p in self._plans.values() for w in p.waves]
        return {
            "total_plans": len(self._plans),
            "total_waves": len(all_waves),
            "total_emails_planned": sum(w.email_count for w in all_waves),
            "pending": sum(1 for w in all_waves if w.status == "pending"),
            "done": sum(1 for w in all_waves if w.status == "done"),
            "cancelled": sum(1 for w in all_waves if w.status == "cancelled"),
        }

    def reset(self) -> None:
        self._plans.clear()

    # ── Internal ──────────────────────────────────────────────────────────────

    def _best_windows(self, sector: str) -> List[Tuple[int, int]]:
        s = sector.lower()
        for key, windows in _SECTOR_WINDOWS.items():
            if key in s:
                return windows
        return _SECTOR_WINDOWS["default"]

    def _next_send_window(self, sector: str, after: datetime.datetime) -> datetime.datetime:
        """Find the next preferred send slot for a sector starting after `after`."""
        windows = self._best_windows(sector)
        # Check up to 7 days ahead
        for day_offset in range(7):
            candidate = after + datetime.timedelta(days=day_offset)
            for (day_of_week, hour) in windows:
                if candidate.weekday() == day_of_week:
                    slot = candidate.replace(hour=hour, minute=0, second=0, microsecond=0)
                    if slot > after:
                        return slot
        # Fallback: next morning
        return (after + datetime.timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)

    @staticmethod
    def _make_id(sector: str, agent_id: str) -> str:
        import hashlib, time
        raw = f"{sector}:{agent_id}:{time.time_ns()}"
        return "plan_" + hashlib.sha256(raw.encode()).hexdigest()[:10]
