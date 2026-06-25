"""Competitor Intelligence — monitors and scores competitive threats."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional
import math


class ThreatLevel(str, Enum):
    CRITICAL = "critical"   # >=80
    HIGH = "high"           # >=60
    MEDIUM = "medium"       # >=40
    LOW = "low"             # >=20
    MINIMAL = "minimal"     # <20


class CompetitorType(str, Enum):
    DIRECT = "direct"           # same market, same ICP
    INDIRECT = "indirect"       # adjacent market
    EMERGING = "emerging"       # new entrant
    LEGACY = "legacy"           # established incumbent
    NICHE = "niche"             # specialized segment


class CompetitiveAction(str, Enum):
    MONITOR = "monitor"
    RESPOND = "respond"
    DIFFERENTIATE = "differentiate"
    PREEMPT = "preempt"
    IGNORE = "ignore"


_TYPE_BASE_THREAT = {
    CompetitorType.DIRECT: 60,
    CompetitorType.INDIRECT: 30,
    CompetitorType.EMERGING: 50,
    CompetitorType.LEGACY: 45,
    CompetitorType.NICHE: 35,
}


@dataclass
class CompetitorInput:
    competitor_id: str
    competitor_name: str
    competitor_type: CompetitorType

    # Market signals
    market_share_pct: float            # 0-100
    growth_rate_pct: float             # YoY %
    funding_total_m_eur: float         # total raised in millions
    last_funding_months_ago: int       # months since last round

    # Product signals
    feature_overlap_pct: float         # overlap with our product 0-100
    product_quality_score: float       # 0-100 (user reviews, G2, Capterra)
    pricing_vs_us: float               # 1.0 = same, <1.0 = cheaper, >1.0 = pricier
    has_recent_product_launch: bool

    # Sales & GTM signals
    sales_team_size: int
    marketing_spend_index: float       # 1.0 = same as us, >1.0 = more
    win_rate_against_us_pct: float     # 0-100 (their win rate)
    common_accounts: int               # accounts we share / compete for

    # Intelligence signals
    hiring_velocity: float             # 1.0 = same pace, >1.0 = faster hiring than us
    executive_departures: int          # C-suite departures last 12 months
    negative_reviews_pct: float        # % negative on review sites
    partnership_announcements: int     # strategic partnerships last 6 months


@dataclass
class CompetitorResult:
    competitor_id: str
    competitor_name: str
    competitor_type: CompetitorType
    threat_score: float
    threat_level: ThreatLevel
    market_score: float
    product_score: float
    gtm_score: float
    weakness_score: float             # competitor weaknesses (higher = more weakness = lower threat)
    recommended_action: CompetitiveAction
    threat_signals: list[str]
    opportunity_signals: list[str]    # their weaknesses we can exploit
    battle_card_tips: list[str]
    win_probability_vs_this: float    # our win probability against this competitor

    def to_dict(self) -> dict:
        d = asdict(self)
        d["competitor_type"] = self.competitor_type.value
        d["threat_level"] = self.threat_level.value
        d["recommended_action"] = self.recommended_action.value
        return d


def _market_score(inp: CompetitorInput) -> float:
    """Market presence: share(40%) + growth(30%) + funding momentum(30%)."""
    share_score = min(100, inp.market_share_pct * 1.5)
    growth_score = min(100, max(0, inp.growth_rate_pct * 2))  # 50% growth → 100

    # Funding momentum: recent and large = high
    funding_recency = max(0, 100 - inp.last_funding_months_ago * 3)
    funding_size = min(100, math.log10(max(1, inp.funding_total_m_eur)) / math.log10(500) * 100)
    funding_score = funding_recency * 0.5 + funding_size * 0.5

    return min(100, share_score * 0.40 + growth_score * 0.30 + funding_score * 0.30)


def _product_score(inp: CompetitorInput) -> float:
    """Product threat: feature overlap(40%) + quality(35%) + pricing(15%) + launches(10%)."""
    overlap_score = min(100, inp.feature_overlap_pct)
    quality_score = min(100, inp.product_quality_score)
    # pricing: cheaper is more threatening
    price_score = min(100, max(0, (2.0 - inp.pricing_vs_us) * 50))
    launch_score = 100 if inp.has_recent_product_launch else 0

    return overlap_score * 0.40 + quality_score * 0.35 + price_score * 0.15 + launch_score * 0.10


def _gtm_score(inp: CompetitorInput) -> float:
    """GTM threat: win rate(40%) + sales force(25%) + marketing(20%) + accounts(15%)."""
    win_score = min(100, inp.win_rate_against_us_pct)
    sales_score = min(100, math.log10(max(1, inp.sales_team_size)) / math.log10(1000) * 100)
    mkt_score = min(100, inp.marketing_spend_index * 50)
    accounts_score = min(100, inp.common_accounts * 5)

    return win_score * 0.40 + sales_score * 0.25 + mkt_score * 0.20 + accounts_score * 0.15


def _weakness_score(inp: CompetitorInput) -> float:
    """Their weaknesses — higher = more opportunity for us."""
    score = 0.0
    score += min(30, inp.executive_departures * 10)           # leadership instability
    score += min(25, inp.negative_reviews_pct * 2)            # product/support issues
    score += min(20, max(0, 20 - inp.hiring_velocity * 10))   # slow hiring if velocity<2
    score += min(25, inp.last_funding_months_ago * 1.5) if inp.funding_total_m_eur < 10 else 0
    return min(100, score)


def _threat_score(inp: CompetitorInput, market: float, product: float, gtm: float, weakness: float) -> float:
    """Overall threat: type_base + market(30%) + product(35%) + gtm(25%) - weakness(10%)."""
    type_base = _TYPE_BASE_THREAT.get(inp.competitor_type, 40)
    # normalize type_base to 0-1 contribution weight
    weighted = market * 0.30 + product * 0.35 + gtm * 0.25 - weakness * 0.10
    # blend: 20% type influence, 80% calculated
    raw = type_base * 0.20 + weighted * 0.80
    return round(max(0, min(100, raw)), 2)


def _threat_level(score: float) -> ThreatLevel:
    if score >= 80:
        return ThreatLevel.CRITICAL
    if score >= 60:
        return ThreatLevel.HIGH
    if score >= 40:
        return ThreatLevel.MEDIUM
    if score >= 20:
        return ThreatLevel.LOW
    return ThreatLevel.MINIMAL


def _action(level: ThreatLevel, inp: CompetitorInput) -> CompetitiveAction:
    if level == ThreatLevel.CRITICAL:
        return CompetitiveAction.PREEMPT
    if level == ThreatLevel.HIGH:
        return CompetitiveAction.RESPOND if inp.win_rate_against_us_pct >= 40 else CompetitiveAction.DIFFERENTIATE
    if level == ThreatLevel.MEDIUM:
        return CompetitiveAction.MONITOR
    if level == ThreatLevel.LOW:
        return CompetitiveAction.MONITOR
    return CompetitiveAction.IGNORE


def _win_probability(inp: CompetitorInput, threat_score: float) -> float:
    """Our win probability in head-to-head: 100 - threat_score, adjusted for weakness."""
    weakness_bonus = min(15, _weakness_score(inp) * 0.15)
    raw = 100 - threat_score + weakness_bonus
    return round(max(5, min(95, raw)), 1)


def _build_signals(
    inp: CompetitorInput,
    threat_level: ThreatLevel,
    market: float,
    product: float,
    gtm: float,
) -> tuple[list[str], list[str], list[str]]:
    threats: list[str] = []
    opportunities: list[str] = []
    battle_tips: list[str] = []

    if inp.win_rate_against_us_pct >= 50:
        threats.append(f"Ils gagnent {inp.win_rate_against_us_pct:.0f}% des deals face à nous")
    if inp.growth_rate_pct >= 30:
        threats.append(f"Croissance rapide ({inp.growth_rate_pct:.0f}% YoY) — expansion agressive")
    if inp.has_recent_product_launch:
        threats.append("Lancement produit récent — nouvelles fonctionnalités à analyser")
    if inp.feature_overlap_pct >= 70:
        threats.append(f"Fort chevauchement fonctionnel ({inp.feature_overlap_pct:.0f}%)")
    if inp.last_funding_months_ago <= 6 and inp.funding_total_m_eur >= 10:
        threats.append(f"Financement récent ({inp.funding_total_m_eur:.0f}M€ il y a {inp.last_funding_months_ago} mois)")
    if inp.marketing_spend_index >= 1.5:
        threats.append("Budget marketing supérieur au nôtre — pression sur l'acquisition")
    if inp.partnership_announcements >= 2:
        threats.append(f"{inp.partnership_announcements} partenariats stratégiques récents")

    if inp.executive_departures >= 2:
        opportunities.append(f"{inp.executive_departures} départs C-suite — instabilité interne")
    if inp.negative_reviews_pct >= 20:
        opportunities.append(f"{inp.negative_reviews_pct:.0f}% d'avis négatifs — insatisfaction clients")
    if inp.pricing_vs_us > 1.3:
        opportunities.append("Pricing nettement plus élevé — argument prix en notre faveur")
    if inp.last_funding_months_ago >= 18 and inp.funding_total_m_eur < 10:
        opportunities.append("Faible trésorerie probable — investissements ralentis")
    if inp.hiring_velocity < 0.7:
        opportunities.append("Ralentissement des embauches — capacité d'exécution réduite")
    if inp.negative_reviews_pct >= 15:
        opportunities.append("Insatisfaction produit visible — prospects ouverts à changer")

    # Battle card tips
    if inp.feature_overlap_pct >= 60:
        battle_tips.append("Mettre en avant nos fonctionnalités différenciantes — faire une démo comparative")
    if inp.pricing_vs_us > 1.0:
        battle_tips.append("Valoriser le ROI et le TCO plutôt que le prix unitaire")
    if inp.win_rate_against_us_pct >= 40:
        battle_tips.append("Sécuriser le champion interne avant la phase de comparaison")
    if inp.executive_departures >= 1:
        battle_tips.append("Soulever la question de la stabilité et de la roadmap long-terme")
    if inp.negative_reviews_pct >= 15:
        battle_tips.append("Partager les références clients et les témoignages G2/Capterra")
    if threat_level in (ThreatLevel.CRITICAL, ThreatLevel.HIGH):
        battle_tips.append("Impliquer un exec sponsor tôt dans le cycle de vente")

    return threats, opportunities, battle_tips


class CompetitorIntelligenceEngine:
    """Monitors and scores competitive threats across the market landscape."""

    def __init__(self) -> None:
        self._results: dict[str, CompetitorResult] = {}

    def analyze(self, inp: CompetitorInput) -> CompetitorResult:
        market = round(_market_score(inp), 2)
        product = round(_product_score(inp), 2)
        gtm = round(_gtm_score(inp), 2)
        weakness = round(_weakness_score(inp), 2)
        threat = _threat_score(inp, market, product, gtm, weakness)
        level = _threat_level(threat)
        action = _action(level, inp)
        win_prob = _win_probability(inp, threat)
        threats, opps, tips = _build_signals(inp, level, market, product, gtm)

        result = CompetitorResult(
            competitor_id=inp.competitor_id,
            competitor_name=inp.competitor_name,
            competitor_type=inp.competitor_type,
            threat_score=threat,
            threat_level=level,
            market_score=market,
            product_score=product,
            gtm_score=gtm,
            weakness_score=weakness,
            recommended_action=action,
            threat_signals=threats,
            opportunity_signals=opps,
            battle_card_tips=tips,
            win_probability_vs_this=win_prob,
        )
        self._results[inp.competitor_id] = result
        return result

    def analyze_batch(self, inputs: list[CompetitorInput]) -> list[CompetitorResult]:
        return sorted([self.analyze(inp) for inp in inputs], key=lambda r: r.threat_score, reverse=True)

    def get(self, competitor_id: str) -> Optional[CompetitorResult]:
        return self._results.get(competitor_id)

    def all_competitors(self) -> list[CompetitorResult]:
        return sorted(self._results.values(), key=lambda r: r.threat_score, reverse=True)

    def by_level(self, level: ThreatLevel) -> list[CompetitorResult]:
        return [r for r in self.all_competitors() if r.threat_level == level]

    def critical_threats(self) -> list[CompetitorResult]:
        return self.by_level(ThreatLevel.CRITICAL)

    def high_threats(self) -> list[CompetitorResult]:
        return self.by_level(ThreatLevel.HIGH)

    def urgent_threats(self) -> list[CompetitorResult]:
        return [
            r for r in self.all_competitors()
            if r.threat_level in (ThreatLevel.CRITICAL, ThreatLevel.HIGH)
        ]

    def by_type(self, ctype: CompetitorType) -> list[CompetitorResult]:
        return [r for r in self.all_competitors() if r.competitor_type == ctype]

    def top_threats(self, n: int = 5) -> list[CompetitorResult]:
        return self.all_competitors()[:n]

    def avg_win_probability(self) -> float:
        all_r = self.all_competitors()
        if not all_r:
            return 0.0
        return round(sum(r.win_probability_vs_this for r in all_r) / len(all_r), 1)

    def summary(self) -> dict:
        all_r = self.all_competitors()
        if not all_r:
            return {
                "total": 0,
                "level_counts": {},
                "avg_threat_score": 0.0,
                "avg_win_probability": 0.0,
            }
        level_counts: dict[str, int] = {}
        total_threat = 0.0
        for r in all_r:
            level_counts[r.threat_level.value] = level_counts.get(r.threat_level.value, 0) + 1
            total_threat += r.threat_score
        n = len(all_r)
        return {
            "total": n,
            "level_counts": level_counts,
            "avg_threat_score": round(total_threat / n, 1),
            "avg_win_probability": self.avg_win_probability(),
        }

    def reset(self) -> None:
        self._results.clear()
