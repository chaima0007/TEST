"""
Lead scoring engine for the Swarm pipeline.

Converts raw prospect signals into a 0-100 action score,
driving agent prioritisation across divisions 1-3.

Features used:
  - pagespeed_score     (performance urgency, inverted)
  - load_time_ms        (UX penalty)
  - icp_fit             (0.0-1.0, from ProspectEnricher)
  - company_size_weight (TPE=0.6, PME=1.0, ETI=0.8)
  - sector_demand       (pulled from a static demand table)
  - open_rate           (optional email engagement signal)
  - reply_signal        (1.0 if replied, 0 otherwise)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ── Sector demand table ────────────────────────────────────────────────────────

_SECTOR_DEMAND: Dict[str, float] = {
    "artisan":       0.95,
    "plombier":      0.95,
    "électricien":   0.90,
    "restaurant":    0.90,
    "hôtel":         0.88,
    "médecin":       0.85,
    "médical":       0.85,
    "dentiste":      0.82,
    "kinésithérapeute": 0.80,
    "garage":        0.85,
    "concessionnaire": 0.80,
    "immobilier":    0.78,
    "agence immo":   0.78,
    "avocat":        0.80,
    "comptable":     0.75,
    "notaire":       0.75,
    "école":         0.70,
    "formation":     0.68,
    "boulangerie":   0.72,
    "coiffeur":      0.65,
    "beauté":        0.65,
    "photographe":   0.60,
    "association":   0.45,
    "agence web":    0.05,
    "digital":       0.05,
    "marketing":     0.10,
}

_SIZE_WEIGHT: Dict[str, float] = {
    "TPE": 0.60,
    "PME": 1.00,
    "ETI": 0.80,
}


# ── Output ─────────────────────────────────────────────────────────────────────

@dataclass
class LeadScore:
    company_id: str
    action_score: float          # 0-100
    grade: str                   # S / A / B / C / D
    feature_contributions: Dict[str, float] = field(default_factory=dict)
    recommended_action: str = ""

    def to_dict(self) -> dict:
        return {
            "company_id": self.company_id,
            "action_score": round(self.action_score, 2),
            "grade": self.grade,
            "feature_contributions": {k: round(v, 4) for k, v in self.feature_contributions.items()},
            "recommended_action": self.recommended_action,
        }


# ── Scorer ─────────────────────────────────────────────────────────────────────

class LeadScorer:
    """
    Feature-weighted linear scorer.
    Weights sum to 1.0:
      pagespeed (inverted) : 0.30
      load_time (inverted) : 0.15
      icp_fit              : 0.25
      sector_demand        : 0.15
      company_size         : 0.10
      engagement           : 0.05
    """

    WEIGHTS = {
        "pagespeed": 0.30,
        "load_time": 0.15,
        "icp_fit":   0.25,
        "sector":    0.15,
        "size":      0.10,
        "engagement": 0.05,
    }

    GRADE_THRESHOLDS = [
        (85, "S"),
        (70, "A"),
        (50, "B"),
        (30, "C"),
        (0,  "D"),
    ]

    ACTIONS = {
        "S": "Appel téléphonique immédiat — proposition commerciale",
        "A": "Email personnalisé Tier A — Agent 2.1",
        "B": "Email de masse secteur — Agent 2.4",
        "C": "Nurturing séquence 3 emails — Division 2",
        "D": "Exclure du pipeline courant",
    }

    def score(
        self,
        company_id: str,
        pagespeed_score: int,
        load_time_ms: int,
        icp_fit: float,
        sector: str,
        company_size: str = "PME",
        open_rate: float = 0.0,
        reply_signal: float = 0.0,
    ) -> LeadScore:
        # ── Feature normalization ─────────────────────────────────────────────
        # Pagespeed: lower = worse = higher score (invert & clamp)
        speed_feat = max(0.0, min(1.0, (100 - pagespeed_score) / 100))

        # Load time: 0ms=0, 8000+ms=1.0, linear clamp
        lt_feat = max(0.0, min(1.0, load_time_ms / 8000))

        # ICP fit already 0-1
        icp_feat = max(0.0, min(1.0, icp_fit))

        # Sector demand lookup
        sector_feat = self._sector_demand(sector)

        # Company size
        size_feat = _SIZE_WEIGHT.get(company_size.upper(), 0.70)

        # Engagement: blend open + reply
        engage_feat = min(1.0, open_rate * 0.3 + reply_signal * 0.7)

        # ── Weighted sum → 0-100 ──────────────────────────────────────────────
        raw = (
            speed_feat   * self.WEIGHTS["pagespeed"]
            + lt_feat    * self.WEIGHTS["load_time"]
            + icp_feat   * self.WEIGHTS["icp_fit"]
            + sector_feat * self.WEIGHTS["sector"]
            + size_feat  * self.WEIGHTS["size"]
            + engage_feat * self.WEIGHTS["engagement"]
        )
        action_score = round(raw * 100, 4)

        grade = self._grade(action_score)
        contributions = {
            "pagespeed": speed_feat * self.WEIGHTS["pagespeed"],
            "load_time": lt_feat * self.WEIGHTS["load_time"],
            "icp_fit":   icp_feat * self.WEIGHTS["icp_fit"],
            "sector":    sector_feat * self.WEIGHTS["sector"],
            "company_size": size_feat * self.WEIGHTS["size"],
            "engagement": engage_feat * self.WEIGHTS["engagement"],
        }

        return LeadScore(
            company_id=company_id,
            action_score=action_score,
            grade=grade,
            feature_contributions=contributions,
            recommended_action=self.ACTIONS[grade],
        )

    def score_batch(self, leads: List[dict]) -> List[LeadScore]:
        """Score a list of lead dicts and return sorted by score desc."""
        results = [self.score(**lead) for lead in leads]
        return sorted(results, key=lambda s: s.action_score, reverse=True)

    def filter_actionable(self, leads: List[dict], min_grade: str = "B") -> List[LeadScore]:
        """Return only leads at or above the given grade threshold."""
        grade_order = ["D", "C", "B", "A", "S"]
        min_idx = grade_order.index(min_grade.upper())
        scored = self.score_batch(leads)
        return [s for s in scored if grade_order.index(s.grade) >= min_idx]

    def top_n(self, leads: List[dict], n: int = 10) -> List[LeadScore]:
        return self.score_batch(leads)[:n]

    # ── Internal ──────────────────────────────────────────────────────────────

    def _sector_demand(self, sector: str) -> float:
        s = sector.lower()
        for key, val in _SECTOR_DEMAND.items():
            if key in s:
                return val
        return 0.50  # neutral for unknown sectors

    def _grade(self, score: float) -> str:
        for threshold, grade in self.GRADE_THRESHOLDS:
            if score >= threshold:
                return grade
        return "D"
