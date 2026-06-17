"""
Conversion Funnel Tracker — records prospect progression through funnel stages
and computes conversion rates, velocity, and drop-off analysis per stage.

Funnel stages (ordered):
  LEAD → CONTACTED → OPENED → REPLIED → DEMO → QUOTED → NEGOTIATING → WON / LOST

Each prospect is tracked with timestamps per stage entry, allowing computation
of:
  - Conversion rate: stage N → stage N+1
  - Average time-to-convert per stage transition
  - Drop-off rate per stage
  - Overall lead-to-close rate
  - Pipeline value at each stage
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple


# ── Funnel stages ─────────────────────────────────────────────────────────────

class FunnelStage(str, Enum):
    LEAD         = "lead"
    CONTACTED    = "contacted"
    OPENED       = "opened"
    REPLIED      = "replied"
    DEMO         = "demo"
    QUOTED       = "quoted"
    NEGOTIATING  = "negotiating"
    WON          = "won"
    LOST         = "lost"

STAGE_ORDER: List[FunnelStage] = [
    FunnelStage.LEAD,
    FunnelStage.CONTACTED,
    FunnelStage.OPENED,
    FunnelStage.REPLIED,
    FunnelStage.DEMO,
    FunnelStage.QUOTED,
    FunnelStage.NEGOTIATING,
    FunnelStage.WON,
]

TERMINAL_STAGES = {FunnelStage.WON, FunnelStage.LOST}


# ── Prospect funnel record ────────────────────────────────────────────────────

@dataclass
class StageEntry:
    stage:      FunnelStage
    entered_at: datetime
    exited_at:  Optional[datetime] = None

    @property
    def duration_hours(self) -> Optional[float]:
        if self.exited_at is None:
            return None
        delta = self.exited_at - self.entered_at
        return delta.total_seconds() / 3600

    def to_dict(self) -> dict:
        return {
            "stage":          self.stage.value,
            "entered_at":     self.entered_at.isoformat(),
            "exited_at":      self.exited_at.isoformat() if self.exited_at else None,
            "duration_hours": round(self.duration_hours, 2) if self.duration_hours is not None else None,
        }


@dataclass
class FunnelRecord:
    prospect_id:   str
    company_name:  str
    sector:        str
    current_stage: FunnelStage
    quote_value:   float = 0.0    # TTC EUR — set when QUOTED
    entries:       List[StageEntry] = field(default_factory=list)

    # ── Stage management ──────────────────────────────────────────────────────

    def advance(self, new_stage: FunnelStage, ts: Optional[datetime] = None) -> bool:
        """Move to new_stage. Returns False if the transition is not valid."""
        now = ts or datetime.utcnow()
        # Close current stage
        if self.entries:
            self.entries[-1].exited_at = now
        self.entries.append(StageEntry(stage=new_stage, entered_at=now))
        self.current_stage = new_stage
        return True

    def time_in_stage(self, stage: FunnelStage) -> Optional[float]:
        """Return hours spent in a given stage (None if never entered)."""
        for e in self.entries:
            if e.stage == stage:
                return e.duration_hours
        return None

    @property
    def is_active(self) -> bool:
        return self.current_stage not in TERMINAL_STAGES

    @property
    def is_won(self) -> bool:
        return self.current_stage == FunnelStage.WON

    @property
    def is_lost(self) -> bool:
        return self.current_stage == FunnelStage.LOST

    @property
    def stages_reached(self) -> List[FunnelStage]:
        return [e.stage for e in self.entries]

    @property
    def days_in_funnel(self) -> float:
        if not self.entries:
            return 0.0
        start = self.entries[0].entered_at
        last = self.entries[-1]
        # Terminal stages have no exit — use their entered_at as end point
        end = last.exited_at or (last.entered_at if self.current_stage in TERMINAL_STAGES else datetime.utcnow())
        return (end - start).total_seconds() / 86400

    def to_dict(self) -> dict:
        return {
            "prospect_id":   self.prospect_id,
            "company_name":  self.company_name,
            "sector":        self.sector,
            "current_stage": self.current_stage.value,
            "quote_value":   self.quote_value,
            "is_active":     self.is_active,
            "is_won":        self.is_won,
            "days_in_funnel": round(self.days_in_funnel, 1),
            "stages_reached": [s.value for s in self.stages_reached],
            "entries":       [e.to_dict() for e in self.entries],
        }


# ── Stage transition stats ────────────────────────────────────────────────────

@dataclass
class TransitionStats:
    from_stage:       FunnelStage
    to_stage:         FunnelStage
    prospects_entered: int = 0   # number who reached from_stage
    prospects_converted: int = 0 # number who advanced to to_stage

    @property
    def conversion_rate(self) -> float:
        return self.prospects_converted / self.prospects_entered if self.prospects_entered else 0.0

    @property
    def drop_off_rate(self) -> float:
        return 1.0 - self.conversion_rate

    def to_dict(self) -> dict:
        return {
            "from_stage":          self.from_stage.value,
            "to_stage":            self.to_stage.value,
            "prospects_entered":   self.prospects_entered,
            "prospects_converted": self.prospects_converted,
            "conversion_rate_pct": round(self.conversion_rate * 100, 1),
            "drop_off_rate_pct":   round(self.drop_off_rate * 100, 1),
        }


# ── Funnel Tracker ────────────────────────────────────────────────────────────

class ConversionFunnelTracker:
    """
    Tracks prospect progression through the sales funnel.

    Usage::
        funnel = ConversionFunnelTracker()
        funnel.add_prospect("p001", "Plomberie Martin", "artisan")
        funnel.advance("p001", FunnelStage.CONTACTED)
        funnel.advance("p001", FunnelStage.OPENED)
        funnel.advance("p001", FunnelStage.QUOTED, quote_value=598.80)
        funnel.advance("p001", FunnelStage.WON)
        report = funnel.stage_report()
    """

    def __init__(self) -> None:
        self._records: Dict[str, FunnelRecord] = {}

    # ── Prospect management ───────────────────────────────────────────────────

    def add_prospect(
        self,
        prospect_id: str,
        company_name: str,
        sector: str = "",
        ts: Optional[datetime] = None,
    ) -> FunnelRecord:
        now = ts or datetime.utcnow()
        rec = FunnelRecord(
            prospect_id=prospect_id,
            company_name=company_name,
            sector=sector,
            current_stage=FunnelStage.LEAD,
            entries=[StageEntry(stage=FunnelStage.LEAD, entered_at=now)],
        )
        self._records[prospect_id] = rec
        return rec

    def get(self, prospect_id: str) -> Optional[FunnelRecord]:
        return self._records.get(prospect_id)

    def get_or_add(
        self,
        prospect_id: str,
        company_name: str = "",
        sector: str = "",
        ts: Optional[datetime] = None,
    ) -> FunnelRecord:
        if prospect_id not in self._records:
            return self.add_prospect(prospect_id, company_name, sector, ts=ts)
        return self._records[prospect_id]

    def all_records(self) -> List[FunnelRecord]:
        return list(self._records.values())

    # ── Stage advancement ─────────────────────────────────────────────────────

    def advance(
        self,
        prospect_id: str,
        new_stage: FunnelStage,
        quote_value: Optional[float] = None,
        ts: Optional[datetime] = None,
    ) -> bool:
        rec = self._records.get(prospect_id)
        if not rec:
            return False
        if quote_value is not None:
            rec.quote_value = quote_value
        return rec.advance(new_stage, ts=ts)

    def mark_won(self, prospect_id: str, quote_value: Optional[float] = None, ts: Optional[datetime] = None) -> bool:
        return self.advance(prospect_id, FunnelStage.WON, quote_value=quote_value, ts=ts)

    def mark_lost(self, prospect_id: str, ts: Optional[datetime] = None) -> bool:
        return self.advance(prospect_id, FunnelStage.LOST, ts=ts)

    # ── Stage queries ─────────────────────────────────────────────────────────

    def by_stage(self, stage: FunnelStage) -> List[FunnelRecord]:
        return [r for r in self._records.values() if r.current_stage == stage]

    def active(self) -> List[FunnelRecord]:
        return [r for r in self._records.values() if r.is_active]

    def won(self) -> List[FunnelRecord]:
        return [r for r in self._records.values() if r.is_won]

    def lost(self) -> List[FunnelRecord]:
        return [r for r in self._records.values() if r.is_lost]

    def by_sector(self, sector: str) -> List[FunnelRecord]:
        return [r for r in self._records.values() if sector.lower() in r.sector.lower()]

    # ── Analytics ─────────────────────────────────────────────────────────────

    def stage_counts(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for r in self._records.values():
            k = r.current_stage.value
            counts[k] = counts.get(k, 0) + 1
        return counts

    def stage_report(self) -> List[TransitionStats]:
        """Compute conversion rate for each consecutive stage pair."""
        results = []
        for i in range(len(STAGE_ORDER) - 1):
            from_s = STAGE_ORDER[i]
            to_s   = STAGE_ORDER[i + 1]
            entered = sum(
                1 for r in self._records.values()
                if any(e.stage == from_s for e in r.entries)
            )
            converted = sum(
                1 for r in self._records.values()
                if any(e.stage == from_s for e in r.entries)
                and any(e.stage == to_s   for e in r.entries)
            )
            results.append(TransitionStats(
                from_stage=from_s,
                to_stage=to_s,
                prospects_entered=entered,
                prospects_converted=converted,
            ))
        return results

    def overall_conversion_rate(self) -> float:
        """LEAD → WON conversion rate."""
        total = len(self._records)
        won   = sum(1 for r in self._records.values() if r.is_won)
        return won / total if total else 0.0

    def total_pipeline_value(self) -> float:
        """Sum of quote_value for all active prospects (excluding won/lost)."""
        return sum(r.quote_value for r in self._records.values() if r.is_active and r.quote_value > 0)

    def total_won_revenue(self) -> float:
        return sum(r.quote_value for r in self.won())

    def average_deal_size(self) -> float:
        won_records = self.won()
        if not won_records:
            return 0.0
        return sum(r.quote_value for r in won_records) / len(won_records)

    def average_days_to_close(self) -> float:
        """Average days from LEAD entry to WON for closed deals."""
        won_records = self.won()
        if not won_records:
            return 0.0
        return sum(r.days_in_funnel for r in won_records) / len(won_records)

    def average_time_per_stage(self) -> Dict[str, Optional[float]]:
        """Average hours spent in each stage across all records."""
        totals: Dict[str, List[float]] = {}
        for r in self._records.values():
            for e in r.entries:
                if e.duration_hours is not None:
                    totals.setdefault(e.stage.value, []).append(e.duration_hours)
        return {
            stage: round(sum(hours) / len(hours), 1) if hours else None
            for stage, hours in totals.items()
        }

    def top_prospects(self, n: int = 10) -> List[FunnelRecord]:
        """Active prospects sorted by quote_value descending."""
        active = sorted(
            [r for r in self._records.values() if r.is_active and r.quote_value > 0],
            key=lambda r: r.quote_value,
            reverse=True,
        )
        return active[:n]

    def sector_summary(self) -> Dict[str, dict]:
        """Per-sector totals: count, won, pipeline value."""
        result: Dict[str, dict] = {}
        for r in self._records.values():
            s = r.sector or "unknown"
            if s not in result:
                result[s] = {"count": 0, "won": 0, "pipeline": 0.0, "revenue": 0.0}
            result[s]["count"] += 1
            if r.is_won:
                result[s]["won"] += 1
                result[s]["revenue"] += r.quote_value
            elif r.is_active and r.quote_value > 0:
                result[s]["pipeline"] += r.quote_value
        return result

    def summary(self) -> dict:
        total = len(self._records)
        won_r = self.won()
        lost_r = self.lost()
        active_r = self.active()
        return {
            "total_prospects":    total,
            "active":             len(active_r),
            "won":                len(won_r),
            "lost":               len(lost_r),
            "overall_cvr_pct":    round(self.overall_conversion_rate() * 100, 1),
            "total_pipeline_eur": round(self.total_pipeline_value(), 2),
            "total_won_eur":      round(self.total_won_revenue(), 2),
            "avg_deal_size_eur":  round(self.average_deal_size(), 2),
            "avg_days_to_close":  round(self.average_days_to_close(), 1),
            "stage_counts":       self.stage_counts(),
        }

    # ── Reset ─────────────────────────────────────────────────────────────────

    def reset(self) -> None:
        self._records.clear()
