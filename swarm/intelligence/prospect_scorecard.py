"""
Prospect Scorecard — composite scoring engine fusing multi-dimensional signals.

Unlike the BANT-only LeadQualificationEngine, the Scorecard combines:
  - BANT qualification (budget, authority, need, timeline)  — 40 pts max
  - Behavioral engagement (email opens, replies, demo attended) — 30 pts max
  - Temporal momentum (recency, contact frequency, response speed) — 20 pts max
  - Market fit (sector match, company size, website quality) — 10 pts max

Total: 0–100 composite score → tier (A/B/C/D)

Tier definitions:
  A (≥ 80) — Immediate action. High-value, engaged, qualified prospect.
  B (≥ 60) — Active nurture. Good fit, some gaps to address.
  C (≥ 40) — Long-term nurture. Possible fit, low engagement.
  D (< 40)  — Deprioritize. Poor fit or disengaged.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


# ── Tier ─────────────────────────────────────────────────────────────────────

class ScorecardTier(str, Enum):
    A = "A"   # ≥ 80
    B = "B"   # ≥ 60
    C = "C"   # ≥ 40
    D = "D"   # < 40


# ── Dimension data classes ────────────────────────────────────────────────────

@dataclass
class BANTDimension:
    """Raw BANT inputs (0–100 scale each, normalized to 40 pts)."""
    budget_score:    int   # 0–100 from LeadQualificationEngine
    authority_score: int   # 0–100
    need_score:      int   # 0–100
    timeline_score:  int   # 0–100

    @property
    def composite(self) -> int:
        """Weighted average → 0–40."""
        avg = (
            self.budget_score * 0.30
            + self.authority_score * 0.20
            + self.need_score * 0.25
            + self.timeline_score * 0.25
        )
        return round(avg * 0.40)


@dataclass
class BehavioralDimension:
    """Email / interaction engagement signals → 0–30."""
    opened_email:    bool = False
    replied_email:   bool = False
    clicked_link:    bool = False
    attended_demo:   bool = False
    visited_website: bool = False
    requested_quote: bool = False

    @property
    def composite(self) -> int:
        score = 0
        if self.opened_email:    score += 4
        if self.clicked_link:    score += 6
        if self.replied_email:   score += 8
        if self.visited_website: score += 4
        if self.attended_demo:   score += 5
        if self.requested_quote: score += 3
        return min(30, score)


@dataclass
class TemporalDimension:
    """Recency and frequency of engagement → 0–20."""
    days_since_contact:  float = 0.0
    response_time_hours: Optional[float] = None   # how fast they replied
    contact_frequency:   float = 0.0              # avg days between contacts

    @property
    def recency_score(self) -> int:
        if self.days_since_contact == 0:
            return 10
        if self.days_since_contact <= 2:
            return 9
        if self.days_since_contact <= 5:
            return 7
        if self.days_since_contact <= 10:
            return 5
        if self.days_since_contact <= 20:
            return 2
        return 0

    @property
    def response_speed_score(self) -> int:
        if self.response_time_hours is None:
            return 0
        if self.response_time_hours <= 2:
            return 6
        if self.response_time_hours <= 24:
            return 4
        if self.response_time_hours <= 72:
            return 2
        return 0

    @property
    def frequency_score(self) -> int:
        if self.contact_frequency <= 0:
            return 0
        if self.contact_frequency <= 3:
            return 4
        if self.contact_frequency <= 7:
            return 3
        if self.contact_frequency <= 14:
            return 1
        return 0

    @property
    def composite(self) -> int:
        return min(20, self.recency_score + self.response_speed_score + self.frequency_score)


@dataclass
class MarketFitDimension:
    """Sector match and company attributes → 0–10."""
    sector_match:    bool = False   # target sector (artisan/PME)
    has_website:     bool = False   # already has a site (can be improved)
    company_age_years: float = 0.0  # established business = higher value
    employee_count:  int = 0

    @property
    def composite(self) -> int:
        score = 0
        if self.sector_match:    score += 4
        if self.has_website:     score += 2
        if self.company_age_years >= 5:  score += 2
        elif self.company_age_years >= 2: score += 1
        if self.employee_count >= 5:  score += 2
        elif self.employee_count >= 1: score += 1
        return min(10, score)


# ── Scorecard record ──────────────────────────────────────────────────────────

@dataclass
class Scorecard:
    prospect_id:  str
    company_name: str
    sector:       str

    bant:         BANTDimension
    behavioral:   BehavioralDimension
    temporal:     TemporalDimension
    market_fit:   MarketFitDimension

    notes:        str = ""
    created_at:   datetime = field(default_factory=datetime.utcnow)
    updated_at:   datetime = field(default_factory=datetime.utcnow)

    @property
    def bant_score(self) -> int:
        return self.bant.composite

    @property
    def behavioral_score(self) -> int:
        return self.behavioral.composite

    @property
    def temporal_score(self) -> int:
        return self.temporal.composite

    @property
    def market_fit_score(self) -> int:
        return self.market_fit.composite

    @property
    def total_score(self) -> int:
        return min(100, self.bant_score + self.behavioral_score + self.temporal_score + self.market_fit_score)

    @property
    def tier(self) -> ScorecardTier:
        s = self.total_score
        if s >= 80: return ScorecardTier.A
        if s >= 60: return ScorecardTier.B
        if s >= 40: return ScorecardTier.C
        return ScorecardTier.D

    @property
    def dimension_breakdown(self) -> Dict[str, int]:
        return {
            "bant":        self.bant_score,
            "behavioral":  self.behavioral_score,
            "temporal":    self.temporal_score,
            "market_fit":  self.market_fit_score,
        }

    def to_dict(self) -> dict:
        return {
            "prospect_id":       self.prospect_id,
            "company_name":      self.company_name,
            "sector":            self.sector,
            "total_score":       self.total_score,
            "tier":              self.tier.value,
            "bant_score":        self.bant_score,
            "behavioral_score":  self.behavioral_score,
            "temporal_score":    self.temporal_score,
            "market_fit_score":  self.market_fit_score,
            "dimension_breakdown": self.dimension_breakdown,
            "notes":             self.notes,
            "created_at":        self.created_at.isoformat(),
            "updated_at":        self.updated_at.isoformat(),
        }


# ── Engine ────────────────────────────────────────────────────────────────────

class ProspectScorecard:
    """
    Composite scoring engine for prospects.

    Usage::
        engine = ProspectScorecard()
        scorecard = engine.score(
            prospect_id="p001",
            company_name="Plomberie Martin",
            sector="artisan",
            bant=BANTDimension(budget_score=80, authority_score=70, need_score=90, timeline_score=60),
            behavioral=BehavioralDimension(replied_email=True, attended_demo=True),
            temporal=TemporalDimension(days_since_contact=3, response_time_hours=4),
            market_fit=MarketFitDimension(sector_match=True, has_website=True),
        )
        print(scorecard.total_score, scorecard.tier)
    """

    def __init__(self) -> None:
        self._scorecards: Dict[str, Scorecard] = {}

    # ── Score ─────────────────────────────────────────────────────────────────

    def score(
        self,
        prospect_id: str,
        company_name: str,
        sector: str = "",
        bant: Optional[BANTDimension] = None,
        behavioral: Optional[BehavioralDimension] = None,
        temporal: Optional[TemporalDimension] = None,
        market_fit: Optional[MarketFitDimension] = None,
        notes: str = "",
        ts: Optional[datetime] = None,
    ) -> Scorecard:
        now = ts or datetime.utcnow()
        card = Scorecard(
            prospect_id=prospect_id,
            company_name=company_name,
            sector=sector,
            bant=bant or BANTDimension(0, 0, 0, 0),
            behavioral=behavioral or BehavioralDimension(),
            temporal=temporal or TemporalDimension(),
            market_fit=market_fit or MarketFitDimension(),
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self._scorecards[prospect_id] = card
        return card

    def update(
        self,
        prospect_id: str,
        bant: Optional[BANTDimension] = None,
        behavioral: Optional[BehavioralDimension] = None,
        temporal: Optional[TemporalDimension] = None,
        market_fit: Optional[MarketFitDimension] = None,
        notes: Optional[str] = None,
        ts: Optional[datetime] = None,
    ) -> Optional[Scorecard]:
        card = self._scorecards.get(prospect_id)
        if not card:
            return None
        if bant is not None:       card.bant = bant
        if behavioral is not None: card.behavioral = behavioral
        if temporal is not None:   card.temporal = temporal
        if market_fit is not None: card.market_fit = market_fit
        if notes is not None:      card.notes = notes
        card.updated_at = ts or datetime.utcnow()
        return card

    # ── Queries ───────────────────────────────────────────────────────────────

    def get(self, prospect_id: str) -> Optional[Scorecard]:
        return self._scorecards.get(prospect_id)

    def all_scorecards(self, limit: Optional[int] = None) -> List[Scorecard]:
        """Returns all scorecards sorted by total_score descending."""
        ranked = sorted(self._scorecards.values(), key=lambda c: c.total_score, reverse=True)
        return ranked[:limit] if limit else ranked

    def by_tier(self, tier: ScorecardTier) -> List[Scorecard]:
        return sorted(
            [c for c in self._scorecards.values() if c.tier == tier],
            key=lambda c: c.total_score,
            reverse=True,
        )

    def top_n(self, n: int = 10) -> List[Scorecard]:
        return self.all_scorecards(limit=n)

    # ── Analytics ─────────────────────────────────────────────────────────────

    def tier_distribution(self) -> Dict[str, int]:
        counts = {t.value: 0 for t in ScorecardTier}
        for c in self._scorecards.values():
            counts[c.tier.value] += 1
        return counts

    def average_score(self) -> float:
        if not self._scorecards:
            return 0.0
        return round(sum(c.total_score for c in self._scorecards.values()) / len(self._scorecards), 1)

    def dimension_averages(self) -> Dict[str, float]:
        if not self._scorecards:
            return {"bant": 0.0, "behavioral": 0.0, "temporal": 0.0, "market_fit": 0.0}
        cards = list(self._scorecards.values())
        n = len(cards)
        return {
            "bant":        round(sum(c.bant_score for c in cards) / n, 1),
            "behavioral":  round(sum(c.behavioral_score for c in cards) / n, 1),
            "temporal":    round(sum(c.temporal_score for c in cards) / n, 1),
            "market_fit":  round(sum(c.market_fit_score for c in cards) / n, 1),
        }

    def weakest_dimension(self) -> str:
        avgs = self.dimension_averages()
        maxes = {"bant": 40, "behavioral": 30, "temporal": 20, "market_fit": 10}
        pct = {k: avgs[k] / maxes[k] for k in avgs}
        return min(pct, key=pct.get)  # type: ignore[arg-type]

    def sector_breakdown(self) -> Dict[str, Dict[str, float]]:
        sectors: Dict[str, List[int]] = {}
        for c in self._scorecards.values():
            sectors.setdefault(c.sector, []).append(c.total_score)
        return {
            sector: {"count": len(scores), "avg_score": round(sum(scores) / len(scores), 1)}
            for sector, scores in sectors.items()
        }

    def summary(self) -> dict:
        dist = self.tier_distribution()
        return {
            "total":             len(self._scorecards),
            "tier_A":            dist["A"],
            "tier_B":            dist["B"],
            "tier_C":            dist["C"],
            "tier_D":            dist["D"],
            "avg_score":         self.average_score(),
            "weakest_dimension": self.weakest_dimension() if self._scorecards else "",
            "dimension_averages": self.dimension_averages(),
            "sector_breakdown":  self.sector_breakdown(),
        }

    # ── Reset ─────────────────────────────────────────────────────────────────

    def reset(self) -> None:
        self._scorecards.clear()
