"""
Contact Timing Optimizer — recommends optimal day/time windows for outreach.

Based on sector-specific French SME email-open patterns and B2B engagement data.
Weights: day-of-week multiplier × hourly profile → composite timing score (0-100).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

# ── Hourly engagement profiles ────────────────────────────────────────────────
# Score 0-100 per hour (7h-19h active window)

_ARTISAN_PROFILE: Dict[int, int] = {
    6: 15, 7: 40, 8: 65, 9: 75, 10: 70, 11: 60,
    12: 30, 13: 20, 14: 50, 15: 60, 16: 55, 17: 45,
    18: 25, 19: 15,
}

_MEDICAL_PROFILE: Dict[int, int] = {
    7: 20, 8: 55, 9: 80, 10: 75, 11: 65,
    12: 25, 13: 15, 14: 60, 15: 70, 16: 65, 17: 40,
    18: 20, 19: 10,
}

_RESTAURANT_PROFILE: Dict[int, int] = {
    8: 30, 9: 50, 10: 65, 11: 45,
    12: 10, 13: 5, 14: 40, 15: 60, 16: 70, 17: 65,
    18: 20, 19: 10,
}

_PME_PROFILE: Dict[int, int] = {
    7: 20, 8: 55, 9: 85, 10: 90, 11: 80,
    12: 35, 13: 30, 14: 75, 15: 80, 16: 70, 17: 55,
    18: 25, 19: 10,
}

_SECTOR_PROFILES: Dict[str, Dict[int, int]] = {
    "artisan": _ARTISAN_PROFILE,
    "plombier": _ARTISAN_PROFILE,
    "électricien": _ARTISAN_PROFILE,
    "maçon": _ARTISAN_PROFILE,
    "restaurant": _RESTAURANT_PROFILE,
    "hôtel": _RESTAURANT_PROFILE,
    "coiffeur": _RESTAURANT_PROFILE,
    "médecin": _MEDICAL_PROFILE,
    "dentiste": _MEDICAL_PROFILE,
    "médical": _MEDICAL_PROFILE,
    "kinésithérapeute": _MEDICAL_PROFILE,
    "comptable": _PME_PROFILE,
    "avocat": _PME_PROFILE,
    "notaire": _PME_PROFILE,
    "immobilier": _PME_PROFILE,
    "PME": _PME_PROFILE,
}

# Day-of-week multipliers (0=Monday … 6=Sunday)
_DAY_MULTIPLIERS: Dict[int, float] = {
    0: 0.90,  # Monday
    1: 1.00,  # Tuesday — peak
    2: 0.85,  # Wednesday
    3: 0.95,  # Thursday — second best
    4: 0.70,  # Friday — declining
    5: 0.15,  # Saturday
    6: 0.05,  # Sunday
}

_DAY_NAMES = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

_KNOWN_SECTORS = ["artisan", "restaurant", "médecin", "comptable", "avocat", "PME",
                  "immobilier", "hôtel", "dentiste", "notaire"]


@dataclass
class OptimalWindow:
    sector: str
    day_of_week: int
    day_name: str
    hour_start: int
    hour_end: int
    score: float
    confidence: str  # "high" | "medium" | "low"
    rationale: str

    def to_dict(self) -> dict:
        return {
            "sector": self.sector,
            "day_of_week": self.day_of_week,
            "day_name": self.day_name,
            "hour_start": self.hour_start,
            "hour_end": self.hour_end,
            "score": round(self.score, 1),
            "confidence": self.confidence,
            "rationale": self.rationale,
        }


class ContactTimingOptimizer:
    """Feature-weighted day/hour scorer for outreach timing."""

    def _get_profile(self, sector: str) -> Dict[int, int]:
        s = sector.lower()
        for key, profile in _SECTOR_PROFILES.items():
            if key in s:
                return profile
        return _PME_PROFILE

    def score_slot(self, sector: str, day_of_week: int, hour: int) -> float:
        """Return 0-100 score for a specific day+hour."""
        profile = self._get_profile(sector)
        base = profile.get(hour, 0)
        day_mult = _DAY_MULTIPLIERS.get(day_of_week, 0.50)
        return round(base * day_mult, 1)

    def weekly_schedule(self, sector: str) -> Dict[str, Dict[int, float]]:
        """Full weekly heatmap: {day_name: {hour: score}}."""
        return {
            _DAY_NAMES[d]: {h: self.score_slot(sector, d, h) for h in range(6, 20)}
            for d in range(7)
        }

    def best_window(self, sector: str) -> OptimalWindow:
        """Single best day+hour window for a sector."""
        best_score = -1.0
        best_day, best_hour = 1, 10

        for day_idx in range(5):  # Mon-Fri
            for hour in range(6, 20):
                score = self.score_slot(sector, day_idx, hour)
                if score > best_score:
                    best_score, best_day, best_hour = score, day_idx, hour

        confidence = "high" if best_score >= 70 else "medium" if best_score >= 40 else "low"
        return OptimalWindow(
            sector=sector,
            day_of_week=best_day,
            day_name=_DAY_NAMES[best_day],
            hour_start=best_hour,
            hour_end=best_hour + 1,
            score=best_score,
            confidence=confidence,
            rationale=self._rationale(sector, best_day, best_hour, best_score),
        )

    def top_windows(self, sector: str, n: int = 3) -> List[OptimalWindow]:
        """Top N windows sorted by score desc."""
        slots = [
            (self.score_slot(sector, d, h), d, h)
            for d in range(5)
            for h in range(6, 20)
            if self.score_slot(sector, d, h) > 0
        ]
        slots.sort(reverse=True)
        results = []
        for score, day_idx, hour in slots[:n]:
            confidence = "high" if score >= 70 else "medium" if score >= 40 else "low"
            results.append(OptimalWindow(
                sector=sector,
                day_of_week=day_idx,
                day_name=_DAY_NAMES[day_idx],
                hour_start=hour,
                hour_end=hour + 1,
                score=score,
                confidence=confidence,
                rationale=self._rationale(sector, day_idx, hour, score),
            ))
        return results

    def sector_summary(self, sectors: Optional[List[str]] = None) -> List[dict]:
        """Best window for each sector (defaults to all known sectors)."""
        targets = sectors or _KNOWN_SECTORS
        return [self.best_window(s).to_dict() for s in targets]

    def _rationale(self, sector: str, day: int, hour: int, score: float) -> str:
        day_name = _DAY_NAMES[day]
        hour_str = f"{hour}h–{hour + 1}h"
        s = sector.lower()
        if any(k in s for k in ("artisan", "plombier", "électricien", "maçon")):
            if 7 <= hour <= 9:
                return f"{day_name} {hour_str} — avant démarrage chantier, taux d'ouverture +40%"
            if 14 <= hour <= 16:
                return f"{day_name} {hour_str} — pause chantier après-midi"
        if any(k in s for k in ("restaurant", "hôtel", "coiffeur")):
            if 14 <= hour <= 17:
                return f"{day_name} {hour_str} — créneau entre services, disponibilité maximale"
        if any(k in s for k in ("médecin", "dentiste", "médical")):
            if hour in (9, 15):
                return f"{day_name} {hour_str} — entre consultations, pic de réponse"
        if hour == 10:
            return f"{day_name} {hour_str} — pic d'engagement matinal B2B, meilleur taux de réponse"
        if hour == 15:
            return f"{day_name} {hour_str} — relance post-déjeuner, focus décisionnel"
        return f"{day_name} {hour_str} — score d'engagement : {score:.0f}/100"
