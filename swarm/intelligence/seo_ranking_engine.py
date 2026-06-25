"""
SEO Ranking Intelligence Engine — Caelum Partners Swarm Module

Scores client websites on organic search performance using a composite
formula and classifies them into four risk tiers for prioritised action.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


# ── Risk thresholds ────────────────────────────────────────────────────────────

def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critique"
    if composite >= 40:
        return "élevé"
    if composite >= 20:
        return "modéré"
    return "faible"


# ── Detection patterns (French) ────────────────────────────────────────────────

SEO_PATTERNS: List[str] = [
    "pénalité détectée",
    "vitesse page insuffisante",
    "Core Web Vitals échoué",
    "classement local absent",
    "contenu dupliqué",
]


# ── Data class ─────────────────────────────────────────────────────────────────

@dataclass
class SEOSite:
    id: str
    name: str
    sector: str
    domain: str
    avg_position: float          # 1–100 (lower = better)
    organic_traffic_monthly: int
    keyword_count: int
    backlink_count: int
    domain_authority: float      # 0–100
    page_speed_mobile: float     # 0–100
    core_web_vitals_score: float # 0–100
    indexation_rate: float       # 0–100
    local_seo_score: float       # 0–100
    patterns_detected: List[str] = field(default_factory=list)

    # Derived — computed in __post_init__
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)

    def __post_init__(self) -> None:
        raw = (
            (100 - self.avg_position) * 0.30
            + self.page_speed_mobile * 0.25
            + self.core_web_vitals_score * 0.25
            + self.local_seo_score * 0.20
        )
        self.composite_score = round(raw, 2)
        self.risk_level = _risk_level(self.composite_score)

    def to_dict(self) -> Dict:
        """Return exactly 15 keys."""
        return {
            "id": self.id,
            "name": self.name,
            "sector": self.sector,
            "domain": self.domain,
            "avg_position": self.avg_position,
            "organic_traffic_monthly": self.organic_traffic_monthly,
            "keyword_count": self.keyword_count,
            "backlink_count": self.backlink_count,
            "domain_authority": self.domain_authority,
            "page_speed_mobile": self.page_speed_mobile,
            "core_web_vitals_score": self.core_web_vitals_score,
            "indexation_rate": self.indexation_rate,
            "local_seo_score": self.local_seo_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
        }


# ── Engine ─────────────────────────────────────────────────────────────────────

class SEORankingEngine:
    """
    Analyses SEO performance across 8 mock client websites and surfaces
    composite risk scores and actionable pattern signals.

    Risk distribution (8 sites):
      critique : 3 sites  (composite >= 60  -> worst SEO health)
      eleve    : 2 sites  (composite 40-59)
      modere   : 1 site   (composite 20-39)
      faible   : 2 sites  (composite  0-19  -> best SEO health)

    All 5 SEO patterns appear at least once across the dataset.
    """

    def __init__(self) -> None:
        self.sites: List[SEOSite] = self._build_mock_sites()

    # ── Mock data ──────────────────────────────────────────────────────────────

    @staticmethod
    def _build_mock_sites() -> List[SEOSite]:
        """
        Composite formula:
          (100 - avg_position)*0.30
          + page_speed_mobile*0.25
          + core_web_vitals_score*0.25
          + local_seo_score*0.20

        Risk thresholds:
          >= 60 -> critique   (sites 1-3)
          >= 40 -> eleve      (sites 4-5)
          >= 20 -> modere     (site 6)
           < 20 -> faible     (sites 7-8)
        """
        return [
            # ── CRITIQUE (3) ──────────────────────────────────────────────────

            # Site 1 — avg_position=5 -> (95)*0.30 + 82*0.25 + 78*0.25 + 74*0.20
            #         = 28.50 + 20.50 + 19.50 + 14.80 = 83.30
            SEOSite(
                id="seo_001",
                name="Plomberie Leblanc SARL",
                sector="Artisans & Bâtiment",
                domain="plomberie-leblanc.fr",
                avg_position=5,
                organic_traffic_monthly=18400,
                keyword_count=312,
                backlink_count=890,
                domain_authority=52.0,
                page_speed_mobile=82.0,
                core_web_vitals_score=78.0,
                indexation_rate=94.0,
                local_seo_score=74.0,
                patterns_detected=["pénalité détectée"],
            ),

            # Site 2 — avg_position=8 -> (92)*0.30 + 75*0.25 + 71*0.25 + 70*0.20
            #         = 27.60 + 18.75 + 17.75 + 14.00 = 78.10
            SEOSite(
                id="seo_002",
                name="Restaurant Le Gaulois",
                sector="Restauration & Hôtellerie",
                domain="legaulois-restaurant.fr",
                avg_position=8,
                organic_traffic_monthly=24700,
                keyword_count=527,
                backlink_count=1240,
                domain_authority=61.0,
                page_speed_mobile=75.0,
                core_web_vitals_score=71.0,
                indexation_rate=98.0,
                local_seo_score=70.0,
                patterns_detected=["contenu dupliqué"],
            ),

            # Site 3 — avg_position=12 -> (88)*0.30 + 68*0.25 + 74*0.25 + 65*0.20
            #         = 26.40 + 17.00 + 18.50 + 13.00 = 74.90
            SEOSite(
                id="seo_003",
                name="Cabinet Médical Marchand",
                sector="Médical & Cabinets de Soin",
                domain="cabinet-marchand.fr",
                avg_position=12,
                organic_traffic_monthly=9800,
                keyword_count=184,
                backlink_count=420,
                domain_authority=44.0,
                page_speed_mobile=68.0,
                core_web_vitals_score=74.0,
                indexation_rate=91.0,
                local_seo_score=65.0,
                patterns_detected=["pénalité détectée", "vitesse page insuffisante"],
            ),

            # ── ÉLEVÉ (2) ────────────────────────────────────────────────────

            # Site 4 — avg_position=35 -> (65)*0.30 + 45*0.25 + 42*0.25 + 38*0.20
            #         = 19.50 + 11.25 + 10.50 + 7.60 = 48.85
            SEOSite(
                id="seo_004",
                name="Auto Garage Martin",
                sector="Garages & Concessionnaires",
                domain="garage-martin.fr",
                avg_position=35,
                organic_traffic_monthly=5200,
                keyword_count=98,
                backlink_count=175,
                domain_authority=31.0,
                page_speed_mobile=45.0,
                core_web_vitals_score=42.0,
                indexation_rate=78.0,
                local_seo_score=38.0,
                patterns_detected=["vitesse page insuffisante", "Core Web Vitals échoué"],
            ),

            # Site 5 — avg_position=42 -> (58)*0.30 + 52*0.25 + 48*0.25 + 30*0.20
            #         = 17.40 + 13.00 + 12.00 + 6.00 = 48.40
            SEOSite(
                id="seo_005",
                name="Immo Provence",
                sector="Agences Immobilières",
                domain="immo-provence.fr",
                avg_position=42,
                organic_traffic_monthly=7100,
                keyword_count=143,
                backlink_count=312,
                domain_authority=38.0,
                page_speed_mobile=52.0,
                core_web_vitals_score=48.0,
                indexation_rate=85.0,
                local_seo_score=30.0,
                patterns_detected=["classement local absent"],
            ),

            # ── MODÉRÉ (1) ───────────────────────────────────────────────────

            # Site 6 — avg_position=65 -> (35)*0.30 + 30*0.25 + 25*0.25 + 28*0.20
            #         = 10.50 + 7.50 + 6.25 + 5.60 = 29.85
            SEOSite(
                id="seo_006",
                name="École de Langues LinguaMax",
                sector="Écoles & Formation",
                domain="linguamax.fr",
                avg_position=65,
                organic_traffic_monthly=3400,
                keyword_count=67,
                backlink_count=89,
                domain_authority=22.0,
                page_speed_mobile=30.0,
                core_web_vitals_score=25.0,
                indexation_rate=63.0,
                local_seo_score=28.0,
                patterns_detected=["Core Web Vitals échoué", "classement local absent"],
            ),

            # ── FAIBLE (2) ────────────────────────────────────────────────────

            # Site 7 — avg_position=88 -> (12)*0.30 + 15*0.25 + 10*0.25 + 8*0.20
            #         = 3.60 + 3.75 + 2.50 + 1.60 = 11.45
            SEOSite(
                id="seo_007",
                name="Boulangerie Du Pain Quotidien",
                sector="Artisans Boulangers",
                domain="boulangerie-dupain.fr",
                avg_position=88,
                organic_traffic_monthly=820,
                keyword_count=14,
                backlink_count=23,
                domain_authority=9.0,
                page_speed_mobile=15.0,
                core_web_vitals_score=10.0,
                indexation_rate=41.0,
                local_seo_score=8.0,
                patterns_detected=[
                    "vitesse page insuffisante",
                    "Core Web Vitals échoué",
                    "classement local absent",
                    "contenu dupliqué",
                ],
            ),

            # Site 8 — avg_position=92 -> (8)*0.30 + 12*0.25 + 8*0.25 + 5*0.20
            #         = 2.40 + 3.00 + 2.00 + 1.00 = 8.40
            SEOSite(
                id="seo_008",
                name="Coiff & Style",
                sector="Boutiques & Beauté",
                domain="coiff-style.fr",
                avg_position=92,
                organic_traffic_monthly=510,
                keyword_count=9,
                backlink_count=11,
                domain_authority=7.0,
                page_speed_mobile=12.0,
                core_web_vitals_score=8.0,
                indexation_rate=35.0,
                local_seo_score=5.0,
                patterns_detected=[
                    "pénalité détectée",
                    "vitesse page insuffisante",
                    "Core Web Vitals échoué",
                    "classement local absent",
                    "contenu dupliqué",
                ],
            ),
        ]

    # ── Public API ─────────────────────────────────────────────────────────────

    def get_entities(self) -> List[Dict]:
        """Return all sites as dicts (15 keys each)."""
        return [s.to_dict() for s in self.sites]

    def summary(self) -> Dict:
        """Return exactly 13-key summary dict."""
        n = len(self.sites)
        avg_pos = round(sum(s.avg_position for s in self.sites) / n, 2)
        avg_traffic = round(sum(s.organic_traffic_monthly for s in self.sites) / n, 2)
        avg_da = round(sum(s.domain_authority for s in self.sites) / n, 2)
        avg_composite = round(sum(s.composite_score for s in self.sites) / n, 2)
        avg_estimated_seo_index = round(avg_composite / 100 * 10, 2)

        by_risk = {r: sum(1 for s in self.sites if s.risk_level == r)
                   for r in ("critique", "élevé", "modéré", "faible")}

        top = max(self.sites, key=lambda s: s.composite_score)

        all_patterns: List[str] = []
        for s in self.sites:
            all_patterns.extend(s.patterns_detected)
        patterns_detected = list(dict.fromkeys(all_patterns))  # unique, insertion order

        return {
            "total_sites": n,
            "avg_position": avg_pos,
            "avg_organic_traffic": avg_traffic,
            "avg_domain_authority": avg_da,
            "sites_critique": by_risk["critique"],
            "sites_eleve": by_risk["élevé"],
            "sites_modere": by_risk["modéré"],
            "sites_faible": by_risk["faible"],
            "top_risk_site": top.name,
            "top_risk_score": top.composite_score,
            "patterns_detected": patterns_detected,
            "avg_composite": avg_composite,
            "avg_estimated_seo_index": avg_estimated_seo_index,
        }
