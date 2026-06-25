"""
Competitor Scorer — evaluates competitor threat level across 5 dimensions:
  price_index (25%), seo_strength (30%), tech_quality (20%), review_score (15%), market_share (10%)
  → composite threat_score 0-100 → ThreatLevel Low/Medium/High/Critical
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional


class ThreatLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class CompetitorProfile:
    competitor_id: str
    name: str
    sector: str
    website: str
    price_index: float
    seo_strength: float
    tech_quality: float
    review_score: float
    market_share_pct: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ScoredCompetitor:
    profile: CompetitorProfile
    threat_score: float
    threat_level: ThreatLevel
    dimension_scores: Dict[str, float]
    strengths: List[str]
    vulnerabilities: List[str]
    recommendations: List[str]

    def to_dict(self) -> dict:
        return {
            "profile": self.profile.to_dict(),
            "threat_score": self.threat_score,
            "threat_level": self.threat_level.value,
            "dimension_scores": self.dimension_scores,
            "strengths": self.strengths,
            "vulnerabilities": self.vulnerabilities,
            "recommendations": self.recommendations,
        }


_WEIGHTS = {
    "price": 0.25,
    "seo": 0.30,
    "tech": 0.20,
    "reviews": 0.15,
    "market": 0.10,
}

_RECOMMENDATIONS = {
    ThreatLevel.CRITICAL: [
        "Priorité absolue : différenciation immédiate",
        "Surveiller toute baisse de prix",
        "Contre-attaquer sur les avis clients",
    ],
    ThreatLevel.HIGH: [
        "Analyser leur positionnement prix",
        "Accélérer les optimisations SEO",
        "Mettre en avant les garanties",
    ],
    ThreatLevel.MEDIUM: [
        "Maintenir la veille mensuelle",
        "Exploiter leurs vulnérabilités identifiées",
        "Renforcer la fidélisation clients",
    ],
    ThreatLevel.LOW: [
        "Veille trimestrielle suffisante",
        "Opportunité de conversion de leurs clients insatisfaits",
    ],
}


def _compute_dimension_scores(profile: CompetitorProfile) -> Dict[str, float]:
    price_threat = 100.0 - profile.price_index
    seo = profile.seo_strength
    tech = profile.tech_quality
    review_normalized = (profile.review_score / 5.0) * 100.0
    market = profile.market_share_pct

    return {
        "price_threat": price_threat,
        "seo": seo,
        "tech": tech,
        "review_normalized": review_normalized,
        "market": market,
    }


def _compute_threat_score(dimension_scores: Dict[str, float]) -> float:
    score = (
        dimension_scores["price_threat"] * _WEIGHTS["price"]
        + dimension_scores["seo"] * _WEIGHTS["seo"]
        + dimension_scores["tech"] * _WEIGHTS["tech"]
        + dimension_scores["review_normalized"] * _WEIGHTS["reviews"]
        + dimension_scores["market"] * _WEIGHTS["market"]
    )
    return round(max(0.0, min(100.0, score)), 4)


def _classify_threat(threat_score: float) -> ThreatLevel:
    if threat_score >= 75:
        return ThreatLevel.CRITICAL
    if threat_score >= 55:
        return ThreatLevel.HIGH
    if threat_score >= 35:
        return ThreatLevel.MEDIUM
    return ThreatLevel.LOW


def _compute_strengths(
    dimension_scores: Dict[str, float], review_score: float
) -> List[str]:
    strengths: List[str] = []
    if dimension_scores["price_threat"] > 70:
        strengths.append("Prix agressif — attire les clients sensibles au coût")
    if dimension_scores["seo"] > 70:
        strengths.append("SEO fort — bonne visibilité Google")
    if dimension_scores["tech"] > 70:
        strengths.append("Stack technique moderne — UX supérieure")
    if dimension_scores["review_normalized"] > 70:
        strengths.append(f"Excellents avis clients ({review_score:.1f}/5)")
    if dimension_scores["market"] > 70:
        strengths.append("Part de marché élevée — forte notoriété")
    return strengths


def _compute_vulnerabilities(
    dimension_scores: Dict[str, float], review_score: float
) -> List[str]:
    vulnerabilities: List[str] = []
    if dimension_scores["price_threat"] < 40:
        vulnerabilities.append("Prix élevés — cible segment premium uniquement")
    if dimension_scores["seo"] < 40:
        vulnerabilities.append("Faible SEO — peu visible sur Google")
    if dimension_scores["tech"] < 40:
        vulnerabilities.append("Site technique médiocre — opportunité de disruption")
    if dimension_scores["review_normalized"] < 40:
        vulnerabilities.append(
            f"Avis clients faibles ({review_score:.1f}/5) — insatisfaction"
        )
    if dimension_scores["market"] < 40:
        vulnerabilities.append("Part de marché faible — peu d'effet réseau")
    return vulnerabilities


def _score_profile(profile: CompetitorProfile) -> ScoredCompetitor:
    dimension_scores = _compute_dimension_scores(profile)
    threat_score = _compute_threat_score(dimension_scores)
    threat_level = _classify_threat(threat_score)
    strengths = _compute_strengths(dimension_scores, profile.review_score)
    vulnerabilities = _compute_vulnerabilities(dimension_scores, profile.review_score)
    recommendations = _RECOMMENDATIONS[threat_level]

    return ScoredCompetitor(
        profile=profile,
        threat_score=threat_score,
        threat_level=threat_level,
        dimension_scores=dimension_scores,
        strengths=strengths,
        vulnerabilities=vulnerabilities,
        recommendations=recommendations,
    )


class CompetitorScorer:
    def __init__(self) -> None:
        self._store: Dict[str, ScoredCompetitor] = {}

    def score(self, profile: CompetitorProfile) -> ScoredCompetitor:
        result = _score_profile(profile)
        self._store[profile.competitor_id] = result
        return result

    def score_batch(
        self, profiles: List[CompetitorProfile]
    ) -> List[ScoredCompetitor]:
        return [self.score(p) for p in profiles]

    def get(self, competitor_id: str) -> Optional[ScoredCompetitor]:
        return self._store.get(competitor_id)

    def all_scored(self) -> List[ScoredCompetitor]:
        return list(self._store.values())

    def top_threats(self, n: int = 5) -> List[ScoredCompetitor]:
        return sorted(
            self._store.values(), key=lambda s: s.threat_score, reverse=True
        )[:n]

    def by_threat_level(self, level: ThreatLevel) -> List[ScoredCompetitor]:
        return [s for s in self._store.values() if s.threat_level == level]

    def sector_summary(self, sector: str) -> dict:
        items = [s for s in self._store.values() if s.profile.sector == sector]
        count = len(items)
        avg_threat = (
            sum(s.threat_score for s in items) / count if count else 0.0
        )
        critical_count = sum(
            1 for s in items if s.threat_level == ThreatLevel.CRITICAL
        )
        high_count = sum(1 for s in items if s.threat_level == ThreatLevel.HIGH)
        top = max(items, key=lambda s: s.threat_score) if items else None
        top_threat_name = top.profile.name if top else None

        return {
            "sector": sector,
            "count": count,
            "avg_threat": round(avg_threat, 4),
            "critical_count": critical_count,
            "high_count": high_count,
            "top_threat_name": top_threat_name,
        }

    def market_snapshot(self) -> dict:
        items = list(self._store.values())
        count = len(items)
        avg_threat = (
            sum(s.threat_score for s in items) / count if count else 0.0
        )
        level_counts = {level.value: 0 for level in ThreatLevel}
        for s in items:
            level_counts[s.threat_level.value] += 1
        top = max(items, key=lambda s: s.threat_score) if items else None

        return {
            "total_competitors": count,
            "avg_threat_score": round(avg_threat, 4),
            "threat_level_distribution": level_counts,
            "top_threat": top.profile.name if top else None,
        }

    def reset(self) -> None:
        self._store.clear()
