"""Pricing Optimizer — recommends optimal pricing strategy per deal/segment."""

from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class PricingStrategy(str, Enum):
    PREMIUM = "premium"         # charge above market
    COMPETITIVE = "competitive"  # at market rate
    PENETRATION = "penetration"  # below market to win
    VALUE_BASED = "value_based"  # tied to customer ROI
    FREEMIUM = "freemium"       # free tier + upsell
    ANCHOR = "anchor"           # high anchor, discount to close


class DiscountRisk(str, Enum):
    HIGH = "high"       # discount >30% — margin threat
    MEDIUM = "medium"   # discount 15-30%
    LOW = "low"         # discount <15%
    NONE = "none"       # no discount needed


class DealUrgency(str, Enum):
    CRITICAL = "critical"   # deal at risk without action
    HIGH = "high"           # close this quarter
    MEDIUM = "medium"       # close within 2 quarters
    LOW = "low"             # exploratory


@dataclass
class PricingInput:
    deal_id: str
    deal_name: str
    list_price_eur: float              # standard list price
    current_proposed_eur: float        # price currently on the table
    cost_to_serve_eur: float           # internal cost
    competitor_price_eur: float        # best competitor offer
    customer_budget_eur: float         # stated budget
    customer_size: str                 # startup / smb / mid_market / enterprise
    industry: str
    deal_stage: str                    # prospecting / qualification / demo / proposal / negotiation / closing
    days_in_stage: int
    num_competitors: int               # competing solutions in evaluation
    champion_strength: float           # 0-100: internal champion advocacy
    decision_maker_engaged: bool
    has_business_case: bool            # ROI/business case prepared
    urgency_driver: str                # regulatory / cost_savings / growth / competitive / none
    contract_length_months: int
    expansion_potential_eur: float     # upsell potential
    historical_discount_pct: float     # avg discount given to similar deals


@dataclass
class PricingResult:
    deal_id: str
    deal_name: str
    recommended_price_eur: float
    recommended_strategy: PricingStrategy
    discount_pct: float                # recommended discount from list
    discount_risk: DiscountRisk
    deal_urgency: DealUrgency
    price_score: float                 # 0-100 quality of pricing position
    win_probability_boost_pct: float   # expected win prob uplift from applying recommendation
    margin_pct: float                  # recommended margin
    value_gap_eur: float               # list - competitor (positive = we're pricier)
    pricing_signals: list[str]
    negotiation_tips: list[str]
    risk_flags: list[str]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["recommended_strategy"] = self.recommended_strategy.value
        d["discount_risk"] = self.discount_risk.value
        d["deal_urgency"] = self.deal_urgency.value
        return d


_STAGE_MAX_DAYS = {
    "prospecting": 14, "qualification": 21, "demo": 21,
    "proposal": 30, "negotiation": 21, "closing": 14,
}

_SIZE_DISCOUNT_CEILING = {
    "startup": 20, "smb": 25, "mid_market": 30, "enterprise": 35,
}

_URGENCY_DRIVERS = {
    "regulatory": DealUrgency.CRITICAL,
    "competitive": DealUrgency.HIGH,
    "cost_savings": DealUrgency.HIGH,
    "growth": DealUrgency.MEDIUM,
    "none": DealUrgency.LOW,
}


def _deal_urgency(inp: PricingInput) -> DealUrgency:
    # Stage-based urgency
    max_days = _STAGE_MAX_DAYS.get(inp.deal_stage.lower(), 21)
    stage_overdue = inp.days_in_stage > max_days * 1.5

    driver_urgency = _URGENCY_DRIVERS.get(inp.urgency_driver.lower(), DealUrgency.LOW)

    if driver_urgency == DealUrgency.CRITICAL:
        return DealUrgency.CRITICAL
    if driver_urgency == DealUrgency.HIGH and stage_overdue:
        return DealUrgency.CRITICAL
    if driver_urgency == DealUrgency.HIGH or stage_overdue:
        return DealUrgency.HIGH
    if driver_urgency == DealUrgency.MEDIUM:
        return DealUrgency.MEDIUM
    return DealUrgency.LOW


def _recommended_discount(inp: PricingInput) -> float:
    """Recommend optimal discount % from list price."""
    ceiling = _SIZE_DISCOUNT_CEILING.get(inp.customer_size.lower(), 25)

    base_discount = 0.0

    # Competitor pressure
    if inp.competitor_price_eur > 0 and inp.list_price_eur > 0:
        price_gap_pct = (inp.list_price_eur - inp.competitor_price_eur) / inp.list_price_eur * 100
        if price_gap_pct > 0:
            base_discount += min(price_gap_pct * 0.6, 15)  # meet competitor halfway

    # Budget constraint
    if inp.customer_budget_eur > 0 and inp.list_price_eur > 0:
        budget_gap_pct = max(0, (inp.list_price_eur - inp.customer_budget_eur) / inp.list_price_eur * 100)
        base_discount += min(budget_gap_pct * 0.5, 10)

    # Competitive intensity
    base_discount += min(inp.num_competitors * 1.5, 8)

    # Historical baseline
    base_discount += inp.historical_discount_pct * 0.3

    # Reduce discount if champion strong + DM engaged + business case
    strengths = sum([
        inp.champion_strength >= 70,
        inp.decision_maker_engaged,
        inp.has_business_case,
    ])
    base_discount -= strengths * 2.5

    # Contract length bonus: longer = bigger discount
    if inp.contract_length_months >= 24:
        base_discount += 5
    elif inp.contract_length_months >= 12:
        base_discount += 2

    return round(max(0, min(ceiling, base_discount)), 1)


def _pricing_strategy(inp: PricingInput, discount: float, urgency: DealUrgency) -> PricingStrategy:
    if inp.list_price_eur < inp.competitor_price_eur * 0.85:
        return PricingStrategy.PENETRATION
    if inp.has_business_case and inp.champion_strength >= 75:
        return PricingStrategy.VALUE_BASED
    if discount == 0 and inp.list_price_eur > inp.competitor_price_eur * 1.15:
        return PricingStrategy.PREMIUM
    if urgency in (DealUrgency.CRITICAL, DealUrgency.HIGH) and inp.num_competitors >= 3:
        return PricingStrategy.ANCHOR
    if inp.customer_size == "startup" and inp.expansion_potential_eur >= inp.list_price_eur * 2:
        return PricingStrategy.FREEMIUM
    return PricingStrategy.COMPETITIVE


def _price_score(inp: PricingInput, recommended: float, margin: float) -> float:
    """Quality of pricing position: margin health(40%) + competitive position(30%) + deal readiness(30%)."""
    margin_score = min(100, margin * 1.5)

    # Competitive position: how well we're positioned vs competitor
    if inp.competitor_price_eur > 0:
        ratio = recommended / inp.competitor_price_eur
        comp_score = min(100, max(0, 100 - abs(1 - ratio) * 200))
    else:
        comp_score = 70.0

    # Deal readiness: champion + DM + business case + urgency
    readiness = (
        inp.champion_strength * 0.35
        + (100 if inp.decision_maker_engaged else 0) * 0.25
        + (100 if inp.has_business_case else 0) * 0.20
        + (80 if inp.urgency_driver != "none" else 20) * 0.20
    )

    return round(max(0, min(100, margin_score * 0.40 + comp_score * 0.30 + readiness * 0.30)), 2)


def _win_probability_boost(discount: float, strategy: PricingStrategy, urgency: DealUrgency) -> float:
    """Expected win probability boost from applying recommended pricing."""
    base = discount * 0.4  # every 1% discount → 0.4% boost
    if strategy == PricingStrategy.VALUE_BASED:
        base += 8
    if strategy == PricingStrategy.COMPETITIVE:
        base += 4
    if urgency in (DealUrgency.CRITICAL, DealUrgency.HIGH):
        base += 5
    return round(min(25, base), 1)


def _discount_risk(discount: float) -> DiscountRisk:
    if discount >= 30:
        return DiscountRisk.HIGH
    if discount >= 15:
        return DiscountRisk.MEDIUM
    if discount > 0:
        return DiscountRisk.LOW
    return DiscountRisk.NONE


def _build_signals(
    inp: PricingInput,
    discount: float,
    strategy: PricingStrategy,
    urgency: DealUrgency,
    margin: float,
) -> tuple[list[str], list[str], list[str]]:
    pricing: list[str] = []
    tips: list[str] = []
    risks: list[str] = []

    if inp.champion_strength >= 75:
        pricing.append("Champion fort — peut justifier le prix sans discount agressif")
    if inp.has_business_case:
        pricing.append("Business case préparé — pricing value-based justifiable")
    if inp.decision_maker_engaged:
        pricing.append("Décideur impliqué — cycle court, moins de pression prix")
    if inp.contract_length_months >= 24:
        pricing.append("Contrat long terme — discount multi-annuel possible")
    if inp.expansion_potential_eur >= inp.list_price_eur:
        pricing.append("Fort potentiel d'expansion — accepter un prix initial inférieur")
    if inp.competitor_price_eur > inp.list_price_eur * 1.1:
        pricing.append("Compétiteurs plus chers — avantage prix naturel")

    if margin < 40:
        risks.append(f"Marge faible ({margin:.0f}%) — risque sur la profitabilité")
    if discount >= 25:
        risks.append(f"Discount élevé ({discount:.0f}%) — précédent dangereux pour les renouvellements")
    if inp.num_competitors >= 4:
        risks.append(f"{inp.num_competitors} concurrents — évaluation très compétitive")
    if urgency == DealUrgency.CRITICAL:
        risks.append("Urgence critique — risque de churn si décision non prise rapidement")
    if inp.champion_strength < 40:
        risks.append("Champion faible — deal à risque sans renforcement de la relation")

    if strategy == PricingStrategy.VALUE_BASED:
        tips.append("Présenter le ROI chiffré avec la business case et des benchmarks sectoriels")
    if strategy == PricingStrategy.ANCHOR:
        tips.append("Commencer avec le prix plein, puis accorder le discount progressivement")
    if inp.num_competitors >= 3:
        tips.append("Demander une liste des concurrents évalués et personaliser les objections")
    if discount > 0:
        tips.append("Conditionner le discount à une signature avant fin de trimestre")
    if inp.expansion_potential_eur > 0:
        tips.append("Proposer un prix d'entrée réduit avec engagement de upsell formalisé")
    if inp.decision_maker_engaged:
        tips.append("Organiser un exec-to-exec call pour valider le budget et la timeline")

    return pricing, tips, risks


class PricingOptimizer:
    """Recommends optimal pricing strategies and discounts per deal."""

    def __init__(self) -> None:
        self._results: dict[str, PricingResult] = {}

    def optimize(self, inp: PricingInput) -> PricingResult:
        urgency = _deal_urgency(inp)
        discount = _recommended_discount(inp)
        strategy = _pricing_strategy(inp, discount, urgency)

        recommended_price = round(inp.list_price_eur * (1 - discount / 100), 2)
        margin = (
            round((recommended_price - inp.cost_to_serve_eur) / recommended_price * 100, 1)
            if recommended_price > 0
            else 0.0
        )

        score = _price_score(inp, recommended_price, margin)
        win_boost = _win_probability_boost(discount, strategy, urgency)
        disc_risk = _discount_risk(discount)
        value_gap = round(inp.list_price_eur - inp.competitor_price_eur, 2)
        pricing_sigs, tips, risks = _build_signals(inp, discount, strategy, urgency, margin)

        result = PricingResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            recommended_price_eur=recommended_price,
            recommended_strategy=strategy,
            discount_pct=discount,
            discount_risk=disc_risk,
            deal_urgency=urgency,
            price_score=score,
            win_probability_boost_pct=win_boost,
            margin_pct=margin,
            value_gap_eur=value_gap,
            pricing_signals=pricing_sigs,
            negotiation_tips=tips,
            risk_flags=risks,
        )
        self._results[inp.deal_id] = result
        return result

    def optimize_batch(self, inputs: list[PricingInput]) -> list[PricingResult]:
        return sorted([self.optimize(inp) for inp in inputs], key=lambda r: r.price_score, reverse=True)

    def get(self, deal_id: str) -> Optional[PricingResult]:
        return self._results.get(deal_id)

    def all_deals(self) -> list[PricingResult]:
        return sorted(self._results.values(), key=lambda r: r.price_score, reverse=True)

    def by_strategy(self, strategy: PricingStrategy) -> list[PricingResult]:
        return [r for r in self.all_deals() if r.recommended_strategy == strategy]

    def by_urgency(self, urgency: DealUrgency) -> list[PricingResult]:
        return [r for r in self.all_deals() if r.deal_urgency == urgency]

    def high_risk_discounts(self) -> list[PricingResult]:
        return [r for r in self.all_deals() if r.discount_risk == DiscountRisk.HIGH]

    def critical_deals(self) -> list[PricingResult]:
        return self.by_urgency(DealUrgency.CRITICAL)

    def total_recommended_pipeline_eur(self) -> float:
        return round(sum(r.recommended_price_eur for r in self.all_deals()), 2)

    def avg_margin_pct(self) -> float:
        all_r = self.all_deals()
        if not all_r:
            return 0.0
        return round(sum(r.margin_pct for r in all_r) / len(all_r), 1)

    def summary(self) -> dict:
        all_r = self.all_deals()
        if not all_r:
            return {
                "total": 0,
                "strategy_counts": {},
                "urgency_counts": {},
                "avg_price_score": 0.0,
                "avg_discount_pct": 0.0,
                "avg_margin_pct": 0.0,
                "total_pipeline_eur": 0.0,
            }
        strategy_counts: dict[str, int] = {}
        urgency_counts: dict[str, int] = {}
        total_score = total_discount = total_margin = 0.0
        for r in all_r:
            strategy_counts[r.recommended_strategy.value] = strategy_counts.get(r.recommended_strategy.value, 0) + 1
            urgency_counts[r.deal_urgency.value] = urgency_counts.get(r.deal_urgency.value, 0) + 1
            total_score += r.price_score
            total_discount += r.discount_pct
            total_margin += r.margin_pct
        n = len(all_r)
        return {
            "total": n,
            "strategy_counts": strategy_counts,
            "urgency_counts": urgency_counts,
            "avg_price_score": round(total_score / n, 1),
            "avg_discount_pct": round(total_discount / n, 1),
            "avg_margin_pct": round(total_margin / n, 1),
            "total_pipeline_eur": self.total_recommended_pipeline_eur(),
        }

    def reset(self) -> None:
        self._results.clear()
