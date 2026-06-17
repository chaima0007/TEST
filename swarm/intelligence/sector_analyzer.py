"""
Sector Analyzer — provides market intelligence per business sector.

Returns:
  - Market size estimate (number of businesses in France)
  - Competition density (how many web agencies already targeting this sector)
  - Average web performance score for the sector
  - ROI multiplier for outreach campaigns
  - Recommended outreach volume per division cycle
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ── Sector database ────────────────────────────────────────────────────────────

@dataclass
class SectorProfile:
    name: str
    market_size_fr: int         # estimated business count in France
    avg_pagespeed: int          # typical mobile PageSpeed score
    competition_density: float  # 0-1 (1 = fully saturated by web agencies)
    avg_revenue_impact_eur: int # avg annual revenue impact of bad perf
    outreach_roi_multiplier: float  # expected reply rate multiplier vs baseline
    tags: List[str] = field(default_factory=list)

    def icp_priority(self) -> str:
        """Return S/A/B/C based on combined opportunity."""
        score = (
            (1 - self.competition_density) * 0.35
            + (1 - self.avg_pagespeed / 100) * 0.35
            + self.outreach_roi_multiplier / 3.0 * 0.30
        )
        if score >= 0.65:  return "S"
        if score >= 0.50:  return "A"
        if score >= 0.35:  return "B"
        return "C"

    def recommended_volume(self) -> int:
        """Emails to send per weekly cycle based on market size and saturation."""
        base = min(self.market_size_fr // 100, 200)
        return max(20, int(base * (1 - self.competition_density * 0.5)))

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "market_size_fr": self.market_size_fr,
            "avg_pagespeed": self.avg_pagespeed,
            "competition_density": self.competition_density,
            "avg_revenue_impact_eur": self.avg_revenue_impact_eur,
            "outreach_roi_multiplier": self.outreach_roi_multiplier,
            "icp_priority": self.icp_priority(),
            "recommended_volume": self.recommended_volume(),
            "tags": self.tags,
        }


_SECTOR_DB: Dict[str, SectorProfile] = {
    "artisans_batiment": SectorProfile(
        name="Artisans & Bâtiment",
        market_size_fr=620_000,
        avg_pagespeed=28,
        competition_density=0.15,
        avg_revenue_impact_eur=32_000,
        outreach_roi_multiplier=2.8,
        tags=["plombier", "électricien", "maçon", "menuisier", "couvreur"],
    ),
    "restauration_hotellerie": SectorProfile(
        name="Restauration & Hôtellerie",
        market_size_fr=185_000,
        avg_pagespeed=32,
        competition_density=0.25,
        avg_revenue_impact_eur=58_000,
        outreach_roi_multiplier=2.6,
        tags=["restaurant", "hôtel", "brasserie", "traiteur", "chambre d'hôtes"],
    ),
    "medical_soins": SectorProfile(
        name="Médical & Cabinets de Soin",
        market_size_fr=280_000,
        avg_pagespeed=35,
        competition_density=0.20,
        avg_revenue_impact_eur=45_000,
        outreach_roi_multiplier=2.4,
        tags=["médecin", "dentiste", "kiné", "ophtalmo", "cabinet médical"],
    ),
    "garages_concessionnaires": SectorProfile(
        name="Garages & Concessionnaires",
        market_size_fr=42_000,
        avg_pagespeed=38,
        competition_density=0.30,
        avg_revenue_impact_eur=22_000,
        outreach_roi_multiplier=2.1,
        tags=["garage", "carrosserie", "concessionnaire", "réparation auto"],
    ),
    "agences_immobilieres": SectorProfile(
        name="Agences Immobilières",
        market_size_fr=30_000,
        avg_pagespeed=42,
        competition_density=0.40,
        avg_revenue_impact_eur=35_000,
        outreach_roi_multiplier=1.9,
        tags=["agence immo", "immobilier", "promoteur", "gestionnaire locatif"],
    ),
    "services_juridiques": SectorProfile(
        name="Services Juridiques & Comptabilité",
        market_size_fr=95_000,
        avg_pagespeed=40,
        competition_density=0.22,
        avg_revenue_impact_eur=28_000,
        outreach_roi_multiplier=2.2,
        tags=["avocat", "notaire", "comptable", "expert-comptable", "huissier"],
    ),
    "ecoles_formation": SectorProfile(
        name="Écoles & Organismes de Formation",
        market_size_fr=55_000,
        avg_pagespeed=44,
        competition_density=0.35,
        avg_revenue_impact_eur=18_000,
        outreach_roi_multiplier=1.7,
        tags=["école", "formation", "auto-école", "soutien scolaire", "université"],
    ),
    "boutiques_beaute": SectorProfile(
        name="Boutiques & Beauté",
        market_size_fr=120_000,
        avg_pagespeed=36,
        competition_density=0.28,
        avg_revenue_impact_eur=14_000,
        outreach_roi_multiplier=1.8,
        tags=["coiffeur", "esthéticienne", "boutique", "parfumerie", "spa"],
    ),
    "associations_loisirs": SectorProfile(
        name="Associations & Loisirs",
        market_size_fr=1_500_000,
        avg_pagespeed=29,
        competition_density=0.08,
        avg_revenue_impact_eur=5_000,
        outreach_roi_multiplier=1.2,
        tags=["association", "club", "sport", "loisirs", "culture"],
    ),
}


# ── Analyzer ───────────────────────────────────────────────────────────────────

class SectorAnalyzer:
    """Offline sector intelligence engine using the built-in sector database."""

    def get(self, sector_key: str) -> Optional[SectorProfile]:
        return _SECTOR_DB.get(sector_key)

    def get_by_name(self, name: str) -> Optional[SectorProfile]:
        name_lower = name.lower()
        for profile in _SECTOR_DB.values():
            if name_lower in profile.name.lower() or profile.name.lower() in name_lower:
                return profile
            if any(tag in name_lower for tag in profile.tags):
                return profile
        return None

    def all_sectors(self) -> List[SectorProfile]:
        return list(_SECTOR_DB.values())

    def ranked_by_opportunity(self) -> List[SectorProfile]:
        """Rank sectors by combined ICP × market size × avg revenue impact."""
        def score(p: SectorProfile) -> float:
            return (
                (1 - p.competition_density) * 0.30
                + (1 - p.avg_pagespeed / 100) * 0.25
                + min(p.market_size_fr / 1_000_000, 1.0) * 0.20
                + min(p.avg_revenue_impact_eur / 60_000, 1.0) * 0.15
                + min(p.outreach_roi_multiplier / 3.0, 1.0) * 0.10
            )
        return sorted(_SECTOR_DB.values(), key=score, reverse=True)

    def s_priority_sectors(self) -> List[SectorProfile]:
        return [p for p in _SECTOR_DB.values() if p.icp_priority() == "S"]

    def total_addressable_market(self) -> int:
        """Total number of French businesses across all tracked sectors."""
        return sum(p.market_size_fr for p in _SECTOR_DB.values())

    def weekly_outreach_plan(self) -> Dict[str, int]:
        """Recommended email volume per sector for one weekly cycle."""
        return {p.name: p.recommended_volume() for p in self.ranked_by_opportunity()}

    def competition_report(self) -> List[dict]:
        """Sectors sorted by lowest competition density (most opportunity)."""
        return [
            {
                "sector": p.name,
                "competition_density": p.competition_density,
                "opportunity_score": round((1 - p.competition_density) * p.outreach_roi_multiplier, 3),
            }
            for p in sorted(_SECTOR_DB.values(), key=lambda p: p.competition_density)
        ]
