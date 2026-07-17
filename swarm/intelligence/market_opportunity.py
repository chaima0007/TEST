"""
Market Opportunity Scanner — identifies and scores market entry opportunities.

Three-dimension composite scoring:
  market_attractiveness(40%) + penetrability(35%) + strategic_fit(25%)
  → opportunity_score 0-100, OpportunityPhase: EMERGING/GROWING/MATURE/DECLINING
  → RiskLevel: LOW/MEDIUM/HIGH/CRITICAL
"""

from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple


class OpportunityPhase(str, Enum):
    EMERGING = "emerging"
    GROWING = "growing"
    MATURE = "mature"
    DECLINING = "declining"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


_PHASE_SCORE = {
    OpportunityPhase.EMERGING: 90,
    OpportunityPhase.GROWING: 65,
    OpportunityPhase.MATURE: 40,
    OpportunityPhase.DECLINING: 15,
}

_ADVANTAGES: Dict[str, str] = {
    "fast_growing_market": "Marché en forte croissance (>20%/an)",
    "low_competition": "Faible concurrence détectée",
    "strong_demand": "Tendance de demande très positive",
    "high_expertise": "Forte expertise interne dans ce secteur",
    "existing_share": "Part de marché existante — avantage acquis",
    "large_tam": "Marché total adressable très large (>100M€)",
    "optimal_deal_size": "Taille de deal optimale pour notre équipe commerciale",
}

_RISKS: Dict[str, str] = {
    "high_saturation": "Marché saturé — différenciation difficile",
    "regulatory_barrier": "Complexité réglementaire élevée",
    "tech_disruption": "Risque de disruption technologique imminente",
    "declining_demand": "Tendance de demande négative détectée",
    "slow_growth": "Croissance de marché faible ou nulle",
    "no_expertise": "Expertise interne insuffisante dans ce secteur",
    "large_competitors": "Présence de grands acteurs établis (>10 concurrents)",
}

_ACTIONS: Dict[str, str] = {
    "invest_now": "Allouer des ressources commerciales en priorité dès maintenant",
    "pilot_first": "Lancer un projet pilote pour valider l'approche avant d'investir",
    "differentiate": "Développer une proposition de valeur différenciante avant d'entrer",
    "monitor": "Surveiller l'évolution du marché — pas d'action immédiate recommandée",
    "exit_or_optimize": "Optimiser les opérations existantes ou envisager un retrait progressif",
    "hire_expertise": "Recruter des experts sectoriels avant d'approcher ce marché",
    "partner": "Envisager un partenariat avec un acteur local pour réduire le risque d'entrée",
}


@dataclass
class MarketSignals:
    opportunity_id: str
    market_name: str
    sector: str
    sub_sector: str
    total_addressable_market_eur: float  # TAM in EUR
    annual_growth_rate_pct: float        # fraction: 0.12 = 12%
    competitor_count: int
    our_market_share_pct: float          # 0-100
    avg_deal_size_eur: float
    avg_sales_cycle_days: int
    demand_trend: float                  # -1.0 to +1.0
    regulatory_complexity: float         # 0-100
    tech_disruption_risk: float          # 0-100
    our_expertise_score: float           # 0-100

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ScoredOpportunity:
    market: MarketSignals
    opportunity_score: float
    opportunity_phase: OpportunityPhase
    risk_level: RiskLevel
    market_attractiveness: float
    penetrability: float
    strategic_fit: float
    projected_revenue_2y_eur: float
    key_advantages: List[str]
    key_risks: List[str]
    recommended_actions: List[str]

    def to_dict(self) -> dict:
        return {
            "market": self.market.to_dict(),
            "opportunity_score": self.opportunity_score,
            "opportunity_phase": self.opportunity_phase.value,
            "risk_level": self.risk_level.value,
            "market_attractiveness": self.market_attractiveness,
            "penetrability": self.penetrability,
            "strategic_fit": self.strategic_fit,
            "projected_revenue_2y_eur": self.projected_revenue_2y_eur,
            "key_advantages": self.key_advantages,
            "key_risks": self.key_risks,
            "recommended_actions": self.recommended_actions,
        }


# ─── Dimension scorers ────────────────────────────────────────────────────────

def _market_attractiveness(m: MarketSignals) -> Tuple[float, List[str], List[str]]:
    advantages: List[str] = []
    risks: List[str] = []

    growth = m.annual_growth_rate_pct
    growth_score = max(0.0, min(100.0, 50.0 + growth * 500.0))
    if growth >= 0.20:
        advantages.append("fast_growing_market")
    elif growth < 0.0:
        risks.append("slow_growth")

    demand = m.demand_trend
    demand_score = (max(-1.0, min(1.0, demand)) + 1.0) / 2.0 * 100.0
    if demand < -0.20:
        risks.append("declining_demand")
    elif demand > 0.50:
        advantages.append("strong_demand")

    tam = m.total_addressable_market_eur
    if tam > 0:
        size_score = min(100.0, math.log10(max(1.0, tam)) / 9.0 * 100.0)
    else:
        size_score = 0.0
    if tam >= 100_000_000:
        advantages.append("large_tam")

    score = growth_score * 0.40 + demand_score * 0.35 + size_score * 0.25
    return round(score, 2), advantages, risks


def _penetrability(m: MarketSignals) -> Tuple[float, List[str], List[str]]:
    advantages: List[str] = []
    risks: List[str] = []

    saturation = max(0.0, 100.0 - m.competitor_count * 10.0)
    if m.competitor_count <= 3:
        advantages.append("low_competition")
    elif m.competitor_count > 10:
        risks.append("large_competitors")

    regulatory = max(0.0, 100.0 - m.regulatory_complexity)
    if m.regulatory_complexity > 50:
        risks.append("regulatory_barrier")

    disruption = max(0.0, 100.0 - m.tech_disruption_risk)
    if m.tech_disruption_risk > 55:
        risks.append("tech_disruption")

    score = saturation * 0.40 + regulatory * 0.35 + disruption * 0.25
    if m.competitor_count > 10:
        risks.append("high_saturation")

    return round(max(0.0, score), 2), advantages, risks


def _strategic_fit(m: MarketSignals) -> Tuple[float, List[str], List[str]]:
    advantages: List[str] = []
    risks: List[str] = []

    expertise = m.our_expertise_score
    if expertise >= 75:
        advantages.append("high_expertise")
    elif expertise < 35:
        risks.append("no_expertise")

    market_share_bonus = min(30.0, m.our_market_share_pct * 2.0)
    if m.our_market_share_pct > 0:
        advantages.append("existing_share")

    deal = m.avg_deal_size_eur
    if 20_000 <= deal <= 200_000:
        deal_score = 100.0
        advantages.append("optimal_deal_size")
    elif 10_000 <= deal < 20_000 or 200_000 < deal <= 500_000:
        deal_score = 80.0
    else:
        deal_score = 60.0

    score = expertise * 0.50 + market_share_bonus * (100.0 / 30.0) * 0.20 + deal_score * 0.30
    return round(min(100.0, score), 2), advantages, risks


def _opportunity_phase(m: MarketSignals, saturation_score: float) -> OpportunityPhase:
    growth = m.annual_growth_rate_pct
    saturation = 100.0 - saturation_score  # higher = more saturated
    demand = m.demand_trend

    if growth >= 0.20 and saturation <= 30 and demand > 0.30:
        return OpportunityPhase.EMERGING
    if growth >= 0.08 or (growth >= 0.0 and demand > 0.10):
        return OpportunityPhase.GROWING
    if growth >= -0.05:
        return OpportunityPhase.MATURE
    return OpportunityPhase.DECLINING


def _risk_level(m: MarketSignals) -> RiskLevel:
    if m.regulatory_complexity > 70 or m.tech_disruption_risk > 75 or m.competitor_count > 15:
        return RiskLevel.CRITICAL
    if m.regulatory_complexity > 50 or m.tech_disruption_risk > 55 or m.competitor_count > 8:
        return RiskLevel.HIGH
    if m.regulatory_complexity > 30 or m.competitor_count > 4:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def _projected_revenue(
    m: MarketSignals,
    opportunity_score: float,
) -> float:
    share_gain_pct = (opportunity_score / 100.0) * 0.03  # up to 3% share gain over 2 years
    tam_target = m.total_addressable_market_eur * share_gain_pct
    if m.avg_deal_size_eur > 0 and m.avg_sales_cycle_days > 0:
        deals_per_year = 365.0 / m.avg_sales_cycle_days * (opportunity_score / 100.0) * 5
        revenue_from_deals = deals_per_year * 2 * m.avg_deal_size_eur
        blended = (tam_target * 0.50 + revenue_from_deals * 0.50)
    else:
        blended = tam_target
    return round(blended, 2)


def _recommended_actions(
    phase: OpportunityPhase,
    risk: RiskLevel,
    score: float,
    expertise: float,
    has_competitors: bool,
) -> List[str]:
    actions: List[str] = []
    if phase == OpportunityPhase.EMERGING and risk in (RiskLevel.LOW, RiskLevel.MEDIUM):
        actions.append("invest_now")
    elif phase == OpportunityPhase.GROWING and risk != RiskLevel.CRITICAL:
        actions.append("pilot_first")
    elif phase == OpportunityPhase.MATURE:
        actions.append("differentiate")
        actions.append("monitor")
    elif phase == OpportunityPhase.DECLINING:
        actions.append("exit_or_optimize")

    if expertise < 40:
        actions.append("hire_expertise")
    if has_competitors and risk in (RiskLevel.HIGH, RiskLevel.CRITICAL):
        actions.append("partner")

    seen: set = set()
    return [a for a in actions if not (a in seen or seen.add(a))]  # type: ignore[func-returns-value]


def _score_opportunity(m: MarketSignals) -> ScoredOpportunity:
    attract, adv1, risk1 = _market_attractiveness(m)
    penet, adv2, risk2 = _penetrability(m)
    fit, adv3, risk3 = _strategic_fit(m)

    score = round(attract * 0.40 + penet * 0.35 + fit * 0.25, 2)

    saturation_for_phase = max(0.0, 100.0 - m.competitor_count * 10.0)
    phase = _opportunity_phase(m, saturation_for_phase)
    risk = _risk_level(m)

    advantages = adv1 + adv2 + adv3
    risks = risk1 + risk2 + risk3

    adv_msgs = [_ADVANTAGES[k] for k in advantages if k in _ADVANTAGES]
    risk_msgs = [_RISKS[k] for k in risks if k in _RISKS]
    actions = [_ACTIONS[k] for k in _recommended_actions(
        phase, risk, score, m.our_expertise_score, m.competitor_count > 3
    ) if k in _ACTIONS]

    proj_rev = _projected_revenue(m, score)

    return ScoredOpportunity(
        market=m,
        opportunity_score=score,
        opportunity_phase=phase,
        risk_level=risk,
        market_attractiveness=attract,
        penetrability=penet,
        strategic_fit=fit,
        projected_revenue_2y_eur=proj_rev,
        key_advantages=adv_msgs,
        key_risks=risk_msgs,
        recommended_actions=actions,
    )


class MarketOpportunityScanner:
    def __init__(self) -> None:
        self._store: Dict[str, ScoredOpportunity] = {}

    def scan(self, market: MarketSignals) -> ScoredOpportunity:
        result = _score_opportunity(market)
        self._store[market.opportunity_id] = result
        return result

    def scan_batch(self, markets: List[MarketSignals]) -> List[ScoredOpportunity]:
        return [self.scan(m) for m in markets]

    def get(self, opportunity_id: str) -> Optional[ScoredOpportunity]:
        return self._store.get(opportunity_id)

    def all_opportunities(self) -> List[ScoredOpportunity]:
        return sorted(self._store.values(), key=lambda o: o.opportunity_score, reverse=True)

    def top_opportunities(self, n: int = 5) -> List[ScoredOpportunity]:
        return self.all_opportunities()[:n]

    def by_phase(self, phase: OpportunityPhase) -> List[ScoredOpportunity]:
        return [o for o in self._store.values() if o.opportunity_phase == phase]

    def by_risk(self, risk: RiskLevel) -> List[ScoredOpportunity]:
        return [o for o in self._store.values() if o.risk_level == risk]

    def emerging_markets(self) -> List[ScoredOpportunity]:
        return self.by_phase(OpportunityPhase.EMERGING)

    def summary(self) -> dict:
        items = list(self._store.values())
        count = len(items)
        if count == 0:
            return {
                "total": 0,
                "phase_counts": {p.value: 0 for p in OpportunityPhase},
                "risk_counts": {r.value: 0 for r in RiskLevel},
                "avg_opportunity_score": 0.0,
                "total_projected_revenue_2y_eur": 0.0,
                "top_sector": None,
            }
        phase_counts = {p.value: 0 for p in OpportunityPhase}
        risk_counts = {r.value: 0 for r in RiskLevel}
        sector_revenue: Dict[str, float] = {}
        for o in items:
            phase_counts[o.opportunity_phase.value] += 1
            risk_counts[o.risk_level.value] += 1
            sector_revenue[o.market.sector] = (
                sector_revenue.get(o.market.sector, 0.0) + o.projected_revenue_2y_eur
            )
        avg_score = sum(o.opportunity_score for o in items) / count
        total_proj = sum(o.projected_revenue_2y_eur for o in items)
        top_sector = max(sector_revenue, key=lambda k: sector_revenue[k]) if sector_revenue else None
        return {
            "total": count,
            "phase_counts": phase_counts,
            "risk_counts": risk_counts,
            "avg_opportunity_score": round(avg_score, 2),
            "total_projected_revenue_2y_eur": round(total_proj, 2),
            "top_sector": top_sector,
        }

    def reset(self) -> None:
        self._store.clear()
