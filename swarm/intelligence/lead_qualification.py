"""
Lead Qualification Engine — BANT-based lead scoring.

BANT dimensions:
  Budget   — confirmed budget range, fit with package pricing
  Authority— decision-maker access, role level
  Need     — pain severity, problem articulated
  Timeline — urgency, days to decision

Each dimension scores 0–25, total 0–100.
Qualification tiers:
  HOT   ≥ 75  — immediate follow-up, priority prospect
  WARM  ≥ 50  — nurture, scheduled touchpoints
  COOL  ≥ 25  — keep in pipeline, lower frequency
  COLD  < 25  — deprioritise or disqualify
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


# ── Enums ─────────────────────────────────────────────────────────────────────

class AuthorityLevel(str, Enum):
    UNKNOWN    = "unknown"
    INFLUENCER = "influencer"   # Can advocate but can't sign
    MANAGER    = "manager"      # Operational authority
    DIRECTOR   = "director"     # Budget authority
    OWNER      = "owner"        # Full decision power


class Timeline(str, Enum):
    UNKNOWN        = "unknown"
    NO_TIMELINE    = "no_timeline"      # No urgency
    NEXT_YEAR      = "next_year"        # 6-12 months
    NEXT_QUARTER   = "next_quarter"     # 3-6 months
    THIS_QUARTER   = "this_quarter"     # 1-3 months
    IMMEDIATE      = "immediate"        # < 1 month


class QualificationTier(str, Enum):
    HOT  = "hot"   # ≥ 75
    WARM = "warm"  # 50–74
    COOL = "cool"  # 25–49
    COLD = "cold"  # < 25


# ── BANT dimension weights ─────────────────────────────────────────────────────

_AUTHORITY_SCORES: Dict[AuthorityLevel, int] = {
    AuthorityLevel.UNKNOWN:    5,
    AuthorityLevel.INFLUENCER: 10,
    AuthorityLevel.MANAGER:    15,
    AuthorityLevel.DIRECTOR:   20,
    AuthorityLevel.OWNER:      25,
}

_TIMELINE_SCORES: Dict[Timeline, int] = {
    Timeline.UNKNOWN:      5,
    Timeline.NO_TIMELINE:  5,
    Timeline.NEXT_YEAR:    8,
    Timeline.NEXT_QUARTER: 15,
    Timeline.THIS_QUARTER: 20,
    Timeline.IMMEDIATE:    25,
}


def _budget_score(budget_eur: float, confirmed: bool) -> int:
    """0–25 based on budget size and whether it's confirmed."""
    if budget_eur <= 0:
        return 0
    # Scale to our packages: starter ~360 / standard ~600 / premium ~960 / enterprise ~1200+
    if budget_eur >= 1200:
        raw = 25
    elif budget_eur >= 960:
        raw = 20
    elif budget_eur >= 600:
        raw = 16
    elif budget_eur >= 360:
        raw = 10
    else:
        raw = 5
    # Halve if unconfirmed
    return raw if confirmed else max(2, raw // 2)


def _need_score(severity: int, articulated: bool) -> int:
    """0–25. severity 1–5, articulated = they have described the pain clearly."""
    clamped = max(1, min(5, severity))
    base = clamped * 4   # 4–20
    bonus = 5 if articulated else 0
    return min(25, base + bonus)


# ── Qualification record ──────────────────────────────────────────────────────

@dataclass
class BANTScore:
    budget_eur:           float = 0.0
    budget_confirmed:     bool = False
    authority_level:      AuthorityLevel = AuthorityLevel.UNKNOWN
    need_severity:        int = 1          # 1–5
    need_articulated:     bool = False
    timeline:             Timeline = Timeline.UNKNOWN

    @property
    def budget_pts(self) -> int:
        return _budget_score(self.budget_eur, self.budget_confirmed)

    @property
    def authority_pts(self) -> int:
        return _AUTHORITY_SCORES[self.authority_level]

    @property
    def need_pts(self) -> int:
        return _need_score(self.need_severity, self.need_articulated)

    @property
    def timeline_pts(self) -> int:
        return _TIMELINE_SCORES[self.timeline]

    @property
    def total(self) -> int:
        return self.budget_pts + self.authority_pts + self.need_pts + self.timeline_pts

    @property
    def tier(self) -> QualificationTier:
        t = self.total
        if t >= 75:
            return QualificationTier.HOT
        if t >= 50:
            return QualificationTier.WARM
        if t >= 25:
            return QualificationTier.COOL
        return QualificationTier.COLD

    def to_dict(self) -> dict:
        return {
            "budget_eur":       self.budget_eur,
            "budget_confirmed": self.budget_confirmed,
            "authority_level":  self.authority_level.value,
            "need_severity":    self.need_severity,
            "need_articulated": self.need_articulated,
            "timeline":         self.timeline.value,
            "budget_pts":       self.budget_pts,
            "authority_pts":    self.authority_pts,
            "need_pts":         self.need_pts,
            "timeline_pts":     self.timeline_pts,
            "total":            self.total,
            "tier":             self.tier.value,
        }


@dataclass
class QualificationRecord:
    record_id:     str
    prospect_id:   str
    company_name:  str
    sector:        str
    contact_name:  str = ""
    contact_role:  str = ""
    bant:          BANTScore = field(default_factory=BANTScore)
    notes:         str = ""
    qualified_at:  datetime = field(default_factory=datetime.utcnow)
    last_updated:  datetime = field(default_factory=datetime.utcnow)

    @property
    def score(self) -> int:
        return self.bant.total

    @property
    def tier(self) -> QualificationTier:
        return self.bant.tier

    def update_bant(
        self,
        budget_eur: Optional[float] = None,
        budget_confirmed: Optional[bool] = None,
        authority_level: Optional[AuthorityLevel] = None,
        need_severity: Optional[int] = None,
        need_articulated: Optional[bool] = None,
        timeline: Optional[Timeline] = None,
        notes: Optional[str] = None,
    ) -> None:
        if budget_eur is not None:
            self.bant.budget_eur = budget_eur
        if budget_confirmed is not None:
            self.bant.budget_confirmed = budget_confirmed
        if authority_level is not None:
            self.bant.authority_level = authority_level
        if need_severity is not None:
            self.bant.need_severity = max(1, min(5, need_severity))
        if need_articulated is not None:
            self.bant.need_articulated = need_articulated
        if timeline is not None:
            self.bant.timeline = timeline
        if notes is not None:
            self.notes = notes
        self.last_updated = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "record_id":    self.record_id,
            "prospect_id":  self.prospect_id,
            "company_name": self.company_name,
            "sector":       self.sector,
            "contact_name": self.contact_name,
            "contact_role": self.contact_role,
            "notes":        self.notes,
            "qualified_at": self.qualified_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "bant":         self.bant.to_dict(),
        }


# ── Engine ────────────────────────────────────────────────────────────────────

class LeadQualificationEngine:
    """
    Scores and segments prospects using BANT methodology.

    Usage::
        engine = LeadQualificationEngine()
        rec = engine.qualify("p001", "Plomberie Martin", "artisan",
            budget_eur=600.0, budget_confirmed=True,
            authority_level=AuthorityLevel.OWNER,
            need_severity=4, need_articulated=True,
            timeline=Timeline.THIS_QUARTER)
        print(rec.score, rec.tier)  # 82, hot
    """

    def __init__(self) -> None:
        self._records: Dict[str, QualificationRecord] = {}
        self._counter = 0

    def _next_id(self) -> str:
        self._counter += 1
        return f"qual_{self._counter:05d}"

    # ── Qualify / update ──────────────────────────────────────────────────────

    def qualify(
        self,
        prospect_id: str,
        company_name: str,
        sector: str = "",
        contact_name: str = "",
        contact_role: str = "",
        budget_eur: float = 0.0,
        budget_confirmed: bool = False,
        authority_level: AuthorityLevel = AuthorityLevel.UNKNOWN,
        need_severity: int = 1,
        need_articulated: bool = False,
        timeline: Timeline = Timeline.UNKNOWN,
        notes: str = "",
        ts: Optional[datetime] = None,
    ) -> QualificationRecord:
        rec_id = self._next_id()
        now = ts or datetime.utcnow()
        bant = BANTScore(
            budget_eur=budget_eur,
            budget_confirmed=budget_confirmed,
            authority_level=authority_level,
            need_severity=max(1, min(5, need_severity)),
            need_articulated=need_articulated,
            timeline=timeline,
        )
        rec = QualificationRecord(
            record_id=rec_id,
            prospect_id=prospect_id,
            company_name=company_name,
            sector=sector,
            contact_name=contact_name,
            contact_role=contact_role,
            bant=bant,
            notes=notes,
            qualified_at=now,
            last_updated=now,
        )
        self._records[prospect_id] = rec
        return rec

    def update(
        self,
        prospect_id: str,
        **kwargs,
    ) -> Optional[QualificationRecord]:
        rec = self._records.get(prospect_id)
        if not rec:
            return None
        rec.update_bant(**kwargs)
        return rec

    def get(self, prospect_id: str) -> Optional[QualificationRecord]:
        return self._records.get(prospect_id)

    def get_or_qualify(
        self,
        prospect_id: str,
        company_name: str = "",
        sector: str = "",
        **kwargs,
    ) -> QualificationRecord:
        if prospect_id in self._records:
            return self._records[prospect_id]
        return self.qualify(prospect_id, company_name, sector, **kwargs)

    def all_records(self) -> List[QualificationRecord]:
        return list(self._records.values())

    # ── Queries ───────────────────────────────────────────────────────────────

    def by_tier(self, tier: QualificationTier) -> List[QualificationRecord]:
        return [r for r in self._records.values() if r.tier == tier]

    def hot(self) -> List[QualificationRecord]:
        return self.by_tier(QualificationTier.HOT)

    def warm(self) -> List[QualificationRecord]:
        return self.by_tier(QualificationTier.WARM)

    def by_sector(self, sector: str) -> List[QualificationRecord]:
        return [r for r in self._records.values() if sector.lower() in r.sector.lower()]

    def top_n(self, n: int = 10) -> List[QualificationRecord]:
        return sorted(self._records.values(), key=lambda r: r.score, reverse=True)[:n]

    # ── Analytics ─────────────────────────────────────────────────────────────

    def tier_distribution(self) -> Dict[str, int]:
        counts: Dict[str, int] = {t.value: 0 for t in QualificationTier}
        for r in self._records.values():
            counts[r.tier.value] += 1
        return counts

    def average_score(self) -> float:
        if not self._records:
            return 0.0
        return round(sum(r.score for r in self._records.values()) / len(self._records), 1)

    def average_score_by_sector(self) -> Dict[str, float]:
        by_sector: Dict[str, List[int]] = {}
        for r in self._records.values():
            s = r.sector or "unknown"
            by_sector.setdefault(s, []).append(r.score)
        return {
            s: round(sum(scores) / len(scores), 1)
            for s, scores in by_sector.items()
        }

    def weakest_dimension(self) -> str:
        """Returns the BANT dimension with the lowest average score."""
        totals = {"budget": 0, "authority": 0, "need": 0, "timeline": 0}
        n = len(self._records)
        if n == 0:
            return "unknown"
        for r in self._records.values():
            totals["budget"]    += r.bant.budget_pts
            totals["authority"] += r.bant.authority_pts
            totals["need"]      += r.bant.need_pts
            totals["timeline"]  += r.bant.timeline_pts
        avgs = {k: v / n for k, v in totals.items()}
        return min(avgs, key=avgs.__getitem__)

    def dimension_averages(self) -> Dict[str, float]:
        n = len(self._records)
        if n == 0:
            return {"budget": 0.0, "authority": 0.0, "need": 0.0, "timeline": 0.0}
        return {
            "budget":    round(sum(r.bant.budget_pts    for r in self._records.values()) / n, 1),
            "authority": round(sum(r.bant.authority_pts for r in self._records.values()) / n, 1),
            "need":      round(sum(r.bant.need_pts      for r in self._records.values()) / n, 1),
            "timeline":  round(sum(r.bant.timeline_pts  for r in self._records.values()) / n, 1),
        }

    def summary(self) -> dict:
        total = len(self._records)
        dist = self.tier_distribution()
        return {
            "total":          total,
            "tier_hot":       dist["hot"],
            "tier_warm":      dist["warm"],
            "tier_cool":      dist["cool"],
            "tier_cold":      dist["cold"],
            "avg_score":      self.average_score(),
            "weakest_bant":   self.weakest_dimension(),
            "dimension_avgs": self.dimension_averages(),
        }

    # ── Reset ─────────────────────────────────────────────────────────────────

    def reset(self) -> None:
        self._records.clear()
        self._counter = 0
