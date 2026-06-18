"""Module 25 — Price Optimization Engine."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PricingStrategy(str, Enum):
    PREMIUM = "premium"
    COMPETITIVE = "competitive"
    PENETRATION = "penetration"
    VALUE_BASED = "value_based"


class DiscountRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXCESSIVE = "excessive"


class PricingAction(str, Enum):
    HOLD = "hold"
    INCREASE = "increase"
    BUNDLE = "bundle"
    DISCOUNT = "discount"
    RESTRUCTURE = "restructure"


class RevenueImpact(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


@dataclass
class DealPricingContext:
    deal_id: str
    account_name: str
    segment: str
    # Financial context
    list_price_eur: float          # catalogue price
    proposed_price_eur: float      # rep's proposed price
    competitor_price_eur: float    # known or estimated competitor price
    customer_budget_eur: float     # confirmed budget ceiling
    # Deal health
    deal_health_score: float       # 0-100 (from other modules)
    days_to_close: int
    # Customer profile
    icp_fit_score: float           # 0-100
    strategic_account: bool        # key account flag
    multi_year_deal: bool
    expansion_potential: float     # 0-100 likelihood of expansion
    # History
    previous_discount_pct: float   # discount given last renewal/deal (0-100)
    years_as_customer: int         # 0 = new prospect
    nps_score: Optional[float]     # -100 to 100, None if no NPS
    # Market context
    quota_attainment_pct: float    # rep's quota attainment this period
    end_of_quarter: bool
    competitive_pressure: bool


@dataclass
class PriceOptimizationResult:
    deal_id: str
    account_name: str
    segment: str
    list_price_eur: float
    proposed_price_eur: float
    optimized_price_eur: float
    recommended_discount_pct: float
    max_acceptable_discount_pct: float
    pricing_strategy: PricingStrategy
    discount_risk: DiscountRisk
    pricing_action: PricingAction
    revenue_impact: RevenueImpact
    price_optimization_score: float  # 0-100
    pricing_rationale: list[str]
    negotiation_guardrails: list[str]
    value_anchors: list[str]
    bundle_options: list[str]

    def to_dict(self) -> dict:
        return {
            "deal_id": self.deal_id,
            "account_name": self.account_name,
            "segment": self.segment,
            "list_price_eur": self.list_price_eur,
            "proposed_price_eur": self.proposed_price_eur,
            "optimized_price_eur": self.optimized_price_eur,
            "recommended_discount_pct": self.recommended_discount_pct,
            "max_acceptable_discount_pct": self.max_acceptable_discount_pct,
            "pricing_strategy": self.pricing_strategy.value,
            "discount_risk": self.discount_risk.value,
            "pricing_action": self.pricing_action.value,
            "revenue_impact": self.revenue_impact.value,
            "price_optimization_score": self.price_optimization_score,
            "pricing_rationale": self.pricing_rationale,
            "negotiation_guardrails": self.negotiation_guardrails,
            "value_anchors": self.value_anchors,
            "bundle_options": self.bundle_options,
        }


def _current_discount_pct(ctx: DealPricingContext) -> float:
    if ctx.list_price_eur <= 0:
        return 0.0
    return round((ctx.list_price_eur - ctx.proposed_price_eur) / ctx.list_price_eur * 100, 1)


def _recommended_discount(ctx: DealPricingContext) -> float:
    """Compute optimal discount %."""
    base = 0.0
    # Segment base discount
    if ctx.segment == "smb":
        base = 5.0
    elif ctx.segment == "mid_market":
        base = 8.0
    else:
        base = 10.0  # enterprise
    # Additions
    if ctx.strategic_account:
        base += 3.0
    if ctx.multi_year_deal:
        base += 4.0
    if ctx.competitive_pressure:
        base += 3.0
    if ctx.end_of_quarter:
        base += 2.0
    if ctx.icp_fit_score >= 80:
        base -= 2.0  # strong fit = less discount needed
    if ctx.deal_health_score >= 80:
        base -= 1.0
    if ctx.years_as_customer >= 3:
        base += 2.0
    # Cap by segment
    caps = {"smb": 15.0, "mid_market": 20.0, "enterprise": 25.0}
    cap = caps.get(ctx.segment, 20.0)
    return round(min(max(0.0, base), cap), 1)


def _max_acceptable_discount(ctx: DealPricingContext) -> float:
    """Floor below which we should walk away or restructure."""
    floors = {"smb": 20.0, "mid_market": 28.0, "enterprise": 35.0}
    base = floors.get(ctx.segment, 25.0)
    if ctx.strategic_account:
        base += 5.0
    if ctx.multi_year_deal:
        base += 5.0
    return round(base, 1)


def _optimized_price(ctx: DealPricingContext, rec_discount: float) -> float:
    return round(ctx.list_price_eur * (1 - rec_discount / 100), 0)


def _pricing_strategy(ctx: DealPricingContext, rec_discount: float) -> PricingStrategy:
    current_disc = _current_discount_pct(ctx)
    if ctx.icp_fit_score >= 80 and not ctx.competitive_pressure and ctx.deal_health_score >= 75:
        return PricingStrategy.VALUE_BASED
    if rec_discount <= 5:
        return PricingStrategy.PREMIUM
    if ctx.competitive_pressure and ctx.competitor_price_eur < ctx.proposed_price_eur:
        return PricingStrategy.COMPETITIVE
    if ctx.years_as_customer == 0 and ctx.segment != "enterprise":
        return PricingStrategy.PENETRATION
    return PricingStrategy.VALUE_BASED


def _discount_risk(current_disc: float, max_disc: float, segment: str) -> DiscountRisk:
    threshold = {"smb": 15.0, "mid_market": 20.0, "enterprise": 25.0}.get(segment, 20.0)
    if current_disc > max_disc:
        return DiscountRisk.EXCESSIVE
    if current_disc > threshold:
        return DiscountRisk.HIGH
    if current_disc > threshold * 0.6:
        return DiscountRisk.MEDIUM
    return DiscountRisk.LOW


def _pricing_action(
    ctx: DealPricingContext,
    current_disc: float,
    rec_disc: float,
    risk: DiscountRisk,
) -> PricingAction:
    if risk == DiscountRisk.EXCESSIVE:
        return PricingAction.RESTRUCTURE
    if current_disc < rec_disc - 3:
        return PricingAction.DISCOUNT
    if ctx.expansion_potential >= 70 or ctx.multi_year_deal:
        return PricingAction.BUNDLE
    if ctx.icp_fit_score >= 80 and ctx.deal_health_score >= 75 and not ctx.competitive_pressure:
        return PricingAction.INCREASE
    return PricingAction.HOLD


def _revenue_impact(
    ctx: DealPricingContext,
    optimized: float,
) -> RevenueImpact:
    if optimized > ctx.proposed_price_eur:
        return RevenueImpact.POSITIVE
    if optimized < ctx.proposed_price_eur * 0.95:
        return RevenueImpact.NEGATIVE
    return RevenueImpact.NEUTRAL


def _price_optimization_score(
    ctx: DealPricingContext,
    current_disc: float,
    max_disc: float,
) -> float:
    """Higher score = better pricing health (less unnecessary discount)."""
    pts = 0.0
    # Discount control: 40 pts
    if current_disc <= max_disc * 0.3:
        pts += 40
    elif current_disc <= max_disc * 0.6:
        pts += 25
    elif current_disc <= max_disc * 0.85:
        pts += 12
    # ICP fit bonus: 20 pts
    pts += ctx.icp_fit_score * 0.20
    # Deal health: 20 pts
    pts += ctx.deal_health_score * 0.20
    # Strategic bonuses: 20 pts
    if ctx.multi_year_deal:
        pts += 8
    if ctx.strategic_account:
        pts += 6
    if ctx.expansion_potential >= 70:
        pts += 6
    return max(0.0, min(100.0, round(pts, 1)))


def _pricing_rationale(
    ctx: DealPricingContext,
    rec_disc: float,
    current_disc: float,
    strategy: PricingStrategy,
) -> list[str]:
    rationale: list[str] = []
    rationale.append(
        f"Stratégie {strategy.value.replace('_', ' ')} recommandée — "
        f"remise optimale : {rec_disc:.1f}% vs remise actuelle : {current_disc:.1f}%"
    )
    if ctx.multi_year_deal:
        rationale.append("Engagement pluriannuel : bonus remise de +4% accordé")
    if ctx.competitive_pressure:
        rationale.append("Pression concurrentielle détectée — remise compétitive justifiée")
    if ctx.icp_fit_score >= 80:
        rationale.append("ICP fit élevé : valeur perçue forte — défendre le prix liste")
    if ctx.strategic_account:
        rationale.append("Compte stratégique : flexibilité tarifaire autorisée dans les guardrails")
    if ctx.end_of_quarter:
        rationale.append("Fin de trimestre : bonus tactique de +2% pour accélérer le closing")
    if ctx.years_as_customer >= 3:
        rationale.append("Client fidèle (3+ ans) : remise fidélité de +2% incluse")
    return rationale


def _negotiation_guardrails(
    ctx: DealPricingContext,
    rec_disc: float,
    max_disc: float,
) -> list[str]:
    guardrails: list[str] = []
    guardrails.append(f"Ne jamais descendre en dessous de {max_disc:.0f}% de remise sans approbation manager")
    guardrails.append(f"Remise cible recommandée : {rec_disc:.1f}% — toute remise supérieure nécessite une validation")
    if ctx.previous_discount_pct > rec_disc:
        guardrails.append(
            f"Historique : remise précédente à {ctx.previous_discount_pct:.1f}% — attention à l'effet cliquet"
        )
    if ctx.end_of_quarter:
        guardrails.append("Fin de trimestre : ne pas sacrifier la marge pour un deal qui peut attendre")
    guardrails.append("Toute remise > 15% doit être accompagnée d'un engagement (volume, durée ou expansion)")
    return guardrails


def _value_anchors(ctx: DealPricingContext) -> list[str]:
    anchors: list[str] = []
    anchors.append("ROI documenté clients similaires — présenter avant toute discussion prix")
    if ctx.expansion_potential >= 70:
        anchors.append(f"Potentiel d'expansion élevé ({ctx.expansion_potential:.0f}%) — valeur lifetime client multiplied")
    if ctx.multi_year_deal:
        anchors.append("Engagement multi-annuel : coût total inférieur avec visibilité tarifaire garantie")
    if ctx.nps_score is not None and ctx.nps_score >= 50:
        anchors.append(f"NPS client actif : {ctx.nps_score:.0f} — satisfaction prouvée, migration risquée")
    anchors.append("Coût de migration concurrente — switching cost à quantifier et présenter")
    anchors.append("Support & SLA premium inclus — valeur cachée à rendre visible")
    return anchors


def _bundle_options(ctx: DealPricingContext) -> list[str]:
    options: list[str] = []
    if ctx.multi_year_deal:
        options.append("Bundle 2 ans : remise -5% + formation offerte + SLA premium")
        options.append("Bundle 3 ans : remise -8% + CSM dédié + QBR trimestriels")
    if ctx.expansion_potential >= 60:
        options.append("Bundle expansion : licences additionnelles à -10% incluses dans le deal initial")
    if ctx.segment == "enterprise":
        options.append("Bundle enterprise : API + SSO + audit de sécurité inclus sans surcoût")
    options.append("Bundle success : onboarding accéléré + certification utilisateurs inclus")
    return options


class PriceOptimizationEngine:
    """Computes optimal pricing and discount strategy for deals."""

    def __init__(self) -> None:
        self._results: dict[str, PriceOptimizationResult] = {}

    def optimize(self, ctx: DealPricingContext) -> PriceOptimizationResult:
        current_disc = _current_discount_pct(ctx)
        rec_disc = _recommended_discount(ctx)
        max_disc = _max_acceptable_discount(ctx)
        optimized = _optimized_price(ctx, rec_disc)
        strategy = _pricing_strategy(ctx, rec_disc)
        risk = _discount_risk(current_disc, max_disc, ctx.segment)
        action = _pricing_action(ctx, current_disc, rec_disc, risk)
        impact = _revenue_impact(ctx, optimized)
        score = _price_optimization_score(ctx, current_disc, max_disc)

        result = PriceOptimizationResult(
            deal_id=ctx.deal_id,
            account_name=ctx.account_name,
            segment=ctx.segment,
            list_price_eur=ctx.list_price_eur,
            proposed_price_eur=ctx.proposed_price_eur,
            optimized_price_eur=optimized,
            recommended_discount_pct=rec_disc,
            max_acceptable_discount_pct=max_disc,
            pricing_strategy=strategy,
            discount_risk=risk,
            pricing_action=action,
            revenue_impact=impact,
            price_optimization_score=score,
            pricing_rationale=_pricing_rationale(ctx, rec_disc, current_disc, strategy),
            negotiation_guardrails=_negotiation_guardrails(ctx, rec_disc, max_disc),
            value_anchors=_value_anchors(ctx),
            bundle_options=_bundle_options(ctx),
        )
        self._results[ctx.deal_id] = result
        return result

    def optimize_batch(self, contexts: list[DealPricingContext]) -> list[PriceOptimizationResult]:
        results = [self.optimize(c) for c in contexts]
        return sorted(results, key=lambda r: r.price_optimization_score, reverse=True)

    # ── Read helpers ──────────────────────────────────────────────────────────

    def all_deals(self) -> list[PriceOptimizationResult]:
        return sorted(self._results.values(), key=lambda r: r.price_optimization_score, reverse=True)

    def by_risk(self, risk: DiscountRisk) -> list[PriceOptimizationResult]:
        return [r for r in self.all_deals() if r.discount_risk == risk]

    def by_action(self, action: PricingAction) -> list[PriceOptimizationResult]:
        return [r for r in self.all_deals() if r.pricing_action == action]

    def by_strategy(self, strategy: PricingStrategy) -> list[PriceOptimizationResult]:
        return [r for r in self.all_deals() if r.pricing_strategy == strategy]

    def excessive_discount_deals(self) -> list[PriceOptimizationResult]:
        return self.by_risk(DiscountRisk.EXCESSIVE)

    def needs_restructure(self) -> list[PriceOptimizationResult]:
        return self.by_action(PricingAction.RESTRUCTURE)

    def positive_revenue_impact(self) -> list[PriceOptimizationResult]:
        return [r for r in self.all_deals() if r.revenue_impact == RevenueImpact.POSITIVE]

    def avg_optimization_score(self) -> float:
        deals = list(self._results.values())
        if not deals:
            return 0.0
        return round(sum(r.price_optimization_score for r in deals) / len(deals), 1)

    def total_revenue_at_risk_eur(self) -> float:
        return round(
            sum(
                r.list_price_eur - r.proposed_price_eur
                for r in self._results.values()
                if r.discount_risk in (DiscountRisk.HIGH, DiscountRisk.EXCESSIVE)
            ),
            2,
        )

    def summary(self) -> dict:
        deals = list(self._results.values())
        n = len(deals)
        risk_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        strategy_counts: dict[str, int] = {}
        impact_counts: dict[str, int] = {}
        for r in deals:
            risk_counts[r.discount_risk.value] = risk_counts.get(r.discount_risk.value, 0) + 1
            action_counts[r.pricing_action.value] = action_counts.get(r.pricing_action.value, 0) + 1
            strategy_counts[r.pricing_strategy.value] = strategy_counts.get(r.pricing_strategy.value, 0) + 1
            impact_counts[r.revenue_impact.value] = impact_counts.get(r.revenue_impact.value, 0) + 1
        return {
            "total": n,
            "risk_counts": risk_counts,
            "action_counts": action_counts,
            "strategy_counts": strategy_counts,
            "revenue_impact_counts": impact_counts,
            "avg_optimization_score": self.avg_optimization_score(),
            "excessive_discount_count": len(self.excessive_discount_deals()),
            "restructure_count": len(self.needs_restructure()),
            "total_revenue_at_risk_eur": self.total_revenue_at_risk_eur(),
        }

    def reset(self) -> None:
        self._results.clear()
