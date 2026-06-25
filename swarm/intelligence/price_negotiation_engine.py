from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DiscountRisk(str, Enum):
    MINIMAL  = "minimal"
    MODERATE = "moderate"
    HIGH     = "high"
    CRITICAL = "critical"


class NegotiationStage(str, Enum):
    INITIAL_OFFER  = "initial_offer"
    COUNTER_OFFER  = "counter_offer"
    FINAL_TERMS    = "final_terms"
    CLOSED         = "closed"
    STALLED        = "stalled"


class PricingStrategy(str, Enum):
    HOLD_PRICE         = "hold_price"
    OFFER_VALUE_ADD    = "offer_value_add"
    CONCEDE_STRATEGIC  = "concede_strategic"
    ESCALATE_TO_EXEC   = "escalate_to_exec"
    WALK_AWAY          = "walk_away"
    ACCEPT_AND_CLOSE   = "accept_and_close"


class MarginHealth(str, Enum):
    STRONG   = "strong"    # margin >= 60%
    HEALTHY  = "healthy"   # margin >= 45%
    THIN     = "thin"      # margin >= 30%
    CRITICAL = "critical"  # margin < 30%


@dataclass
class NegotiationInput:
    deal_id:                  str
    account_id:               str
    rep_id:                   str
    segment:                  str              # smb / mid_market / enterprise
    list_price:               float
    proposed_price:           float            # current offer
    target_price:             float            # rep's floor price
    competitor_price:         float            # known competitor quote (0 if unknown)
    cost_of_goods:            float            # COGS for margin calc
    deal_value:               float            # total contract value
    discount_pct:             float            # current discount % (0–100)
    max_discount_pct:         float            # approved max discount
    num_rounds:               int              # negotiation rounds so far
    buyer_pushback_level:     int              # 0=none, 1=mild, 2=moderate, 3=strong, 4=walk_out
    champion_support:         bool
    economic_buyer_engaged:   bool
    multi_year_deal:          bool
    professional_services:    float            # attached PS value
    annual_contract_value:    float
    customer_lifetime_value:  float           # estimated LCV
    historical_win_rate_at_discount: float    # win rate at current discount level
    days_to_close:            int
    is_strategic_account:     bool
    payment_terms_days:       int             # standard=30, extended=60/90


@dataclass
class NegotiationResult:
    deal_id:                  str
    account_id:               str
    rep_id:                   str
    discount_risk:            DiscountRisk
    negotiation_stage:        NegotiationStage
    pricing_strategy:         PricingStrategy
    margin_health:            MarginHealth
    gross_margin_pct:         float     # 0–100
    effective_discount_pct:   float     # actual discount applied
    price_to_value_score:     float     # 0–100 (how justified is the price)
    negotiation_leverage:     float     # 0–100 (how much leverage we have)
    walkaway_risk:            float     # 0–100 (risk buyer walks away)
    recommended_concession:   float     # $ value of acceptable concession
    is_margin_positive:       bool
    is_strategic:             bool

    def to_dict(self) -> dict:
        return {
            "deal_id":                  self.deal_id,
            "account_id":               self.account_id,
            "rep_id":                   self.rep_id,
            "discount_risk":            self.discount_risk.value,
            "negotiation_stage":        self.negotiation_stage.value,
            "pricing_strategy":         self.pricing_strategy.value,
            "margin_health":            self.margin_health.value,
            "gross_margin_pct":         self.gross_margin_pct,
            "effective_discount_pct":   self.effective_discount_pct,
            "price_to_value_score":     self.price_to_value_score,
            "negotiation_leverage":     self.negotiation_leverage,
            "walkaway_risk":            self.walkaway_risk,
            "recommended_concession":   self.recommended_concession,
            "is_margin_positive":       self.is_margin_positive,
            "is_strategic":             self.is_strategic,
        }


class PriceNegotiationEngine:
    def __init__(self) -> None:
        self._results: list[NegotiationResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: NegotiationInput) -> NegotiationResult:
        margin_pct   = self._gross_margin_pct(inp)
        eff_discount = self._effective_discount_pct(inp)
        margin_h     = self._margin_health(margin_pct)
        disc_risk    = self._discount_risk(inp, eff_discount, margin_pct)
        leverage     = self._negotiation_leverage(inp)
        walkaway     = self._walkaway_risk(inp)
        ptv_score    = self._price_to_value_score(inp, margin_pct, leverage)
        stage        = self._negotiation_stage(inp)
        strategy     = self._pricing_strategy(inp, disc_risk, leverage, walkaway, margin_h)
        concession   = self._recommended_concession(inp, eff_discount)
        margin_pos   = margin_pct > 0
        strategic    = inp.is_strategic_account or inp.customer_lifetime_value >= 500_000

        result = NegotiationResult(
            deal_id=inp.deal_id,
            account_id=inp.account_id,
            rep_id=inp.rep_id,
            discount_risk=disc_risk,
            negotiation_stage=stage,
            pricing_strategy=strategy,
            margin_health=margin_h,
            gross_margin_pct=margin_pct,
            effective_discount_pct=eff_discount,
            price_to_value_score=ptv_score,
            negotiation_leverage=leverage,
            walkaway_risk=walkaway,
            recommended_concession=concession,
            is_margin_positive=margin_pos,
            is_strategic=strategic,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[NegotiationInput]
    ) -> list[NegotiationResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def high_risk_deals(self) -> list[NegotiationResult]:
        return [r for r in self._results
                if r.discount_risk in (DiscountRisk.HIGH, DiscountRisk.CRITICAL)]

    @property
    def strategic_deals(self) -> list[NegotiationResult]:
        return [r for r in self._results if r.is_strategic]

    @property
    def walk_away_candidates(self) -> list[NegotiationResult]:
        return [r for r in self._results
                if r.pricing_strategy == PricingStrategy.WALK_AWAY]

    @property
    def avg_effective_discount(self) -> float:
        if not self._results:
            return 0.0
        return round(
            sum(r.effective_discount_pct for r in self._results) / len(self._results), 2
        )

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _gross_margin_pct(self, inp: NegotiationInput) -> float:
        if inp.proposed_price <= 0:
            return 0.0
        margin = (inp.proposed_price - inp.cost_of_goods) / inp.proposed_price * 100
        return round(max(-100.0, min(100.0, margin)), 1)

    def _effective_discount_pct(self, inp: NegotiationInput) -> float:
        if inp.list_price <= 0:
            return 0.0
        disc = (1 - inp.proposed_price / inp.list_price) * 100
        return round(max(0.0, min(100.0, disc)), 1)

    def _margin_health(self, margin_pct: float) -> MarginHealth:
        if margin_pct >= 60: return MarginHealth.STRONG
        if margin_pct >= 45: return MarginHealth.HEALTHY
        if margin_pct >= 30: return MarginHealth.THIN
        return MarginHealth.CRITICAL

    def _discount_risk(
        self, inp: NegotiationInput, eff_discount: float, margin_pct: float
    ) -> DiscountRisk:
        risk_score = 0
        # Discount vs max allowed
        if eff_discount > inp.max_discount_pct:        risk_score += 3
        elif eff_discount >= inp.max_discount_pct * 0.9: risk_score += 1
        # Margin deterioration
        if margin_pct < 30:  risk_score += 3
        elif margin_pct < 45: risk_score += 1
        # Win rate at this discount
        if inp.historical_win_rate_at_discount < 0.3:  risk_score += 2
        elif inp.historical_win_rate_at_discount < 0.5: risk_score += 1
        # Buyer behavior
        if inp.buyer_pushback_level >= 4: risk_score += 2
        elif inp.buyer_pushback_level >= 3: risk_score += 1
        # Extended payment terms
        if inp.payment_terms_days >= 90: risk_score += 1

        if risk_score >= 7: return DiscountRisk.CRITICAL
        if risk_score >= 4: return DiscountRisk.HIGH
        if risk_score >= 2: return DiscountRisk.MODERATE
        return DiscountRisk.MINIMAL

    def _negotiation_leverage(self, inp: NegotiationInput) -> float:
        score = 50.0
        # Champion support
        if inp.champion_support:         score += 15
        # Economic buyer engaged
        if inp.economic_buyer_engaged:   score += 12
        # Multi-year deal
        if inp.multi_year_deal:          score += 8
        # Professional services attached
        if inp.professional_services > 0: score += 5
        # Competitive pricing advantage
        if inp.competitor_price > 0 and inp.proposed_price < inp.competitor_price:
            score += 10
        elif inp.competitor_price > 0 and inp.proposed_price > inp.competitor_price:
            score -= 15
        # Strategic account
        if inp.is_strategic_account: score += 5
        # Time pressure (close days)
        if inp.days_to_close <= 7:   score += 5
        elif inp.days_to_close >= 60: score -= 10
        # Pushback = reduces leverage
        score -= inp.buyer_pushback_level * 8
        return round(max(0.0, min(100.0, score)), 1)

    def _walkaway_risk(self, inp: NegotiationInput) -> float:
        # High pushback + unfavorable pricing = walkaway risk
        score = inp.buyer_pushback_level * 15.0
        if inp.competitor_price > 0 and inp.proposed_price > inp.competitor_price * 1.1:
            score += 25
        if inp.num_rounds >= 4:   score += 15
        if not inp.champion_support: score += 10
        if inp.discount_pct > inp.max_discount_pct: score -= 10  # over-discounting buys goodwill
        return round(max(0.0, min(100.0, score)), 1)

    def _price_to_value_score(
        self, inp: NegotiationInput, margin_pct: float, leverage: float
    ) -> float:
        # Composite: margin quality + leverage + ACV justification
        score = margin_pct * 0.4 + leverage * 0.4
        # LTV bonus
        if inp.customer_lifetime_value >= 500_000: score += 10
        elif inp.customer_lifetime_value >= 200_000: score += 5
        # Multi-year justification
        if inp.multi_year_deal: score += 8
        # PS attached adds value context
        if inp.professional_services > 0: score += 5
        return round(max(0.0, min(100.0, score)), 1)

    def _negotiation_stage(self, inp: NegotiationInput) -> NegotiationStage:
        if inp.buyer_pushback_level == 0 and inp.num_rounds == 0:
            return NegotiationStage.INITIAL_OFFER
        if inp.buyer_pushback_level >= 4:
            return NegotiationStage.STALLED
        if inp.days_to_close <= 3:
            return NegotiationStage.FINAL_TERMS
        if inp.num_rounds >= 2:
            return NegotiationStage.COUNTER_OFFER
        return NegotiationStage.INITIAL_OFFER

    def _pricing_strategy(
        self,
        inp: NegotiationInput,
        disc_risk: DiscountRisk,
        leverage: float,
        walkaway: float,
        margin_h: MarginHealth,
    ) -> PricingStrategy:
        if margin_h == MarginHealth.CRITICAL and not inp.is_strategic_account:
            return PricingStrategy.WALK_AWAY
        if disc_risk == DiscountRisk.CRITICAL:
            return PricingStrategy.ESCALATE_TO_EXEC
        if walkaway >= 70 and leverage >= 60:
            return PricingStrategy.ACCEPT_AND_CLOSE
        if leverage >= 70 and disc_risk == DiscountRisk.MINIMAL:
            return PricingStrategy.HOLD_PRICE
        if inp.multi_year_deal or inp.professional_services > 0:
            return PricingStrategy.OFFER_VALUE_ADD
        if disc_risk == DiscountRisk.HIGH and inp.is_strategic_account:
            return PricingStrategy.CONCEDE_STRATEGIC
        if disc_risk == DiscountRisk.HIGH:
            return PricingStrategy.ESCALATE_TO_EXEC
        return PricingStrategy.HOLD_PRICE

    def _recommended_concession(
        self, inp: NegotiationInput, eff_discount: float
    ) -> float:
        remaining_room = max(0.0, inp.max_discount_pct - eff_discount)
        # Offer at most half of remaining room, capped at 5%
        concession_pct = min(5.0, remaining_room * 0.5)
        concession_value = inp.list_price * (concession_pct / 100)
        return round(concession_value, 2)

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                     0,
                "risk_counts":               {},
                "stage_counts":              {},
                "strategy_counts":           {},
                "margin_health_counts":      {},
                "avg_gross_margin_pct":      0.0,
                "avg_effective_discount":    0.0,
                "avg_negotiation_leverage":  0.0,
                "avg_walkaway_risk":         0.0,
                "high_risk_count":           0,
                "strategic_count":           0,
                "walk_away_count":           0,
                "avg_price_to_value_score":  0.0,
            }

        risk_counts:   dict[str, int] = {}
        stage_counts:  dict[str, int] = {}
        strat_counts:  dict[str, int] = {}
        margin_counts: dict[str, int] = {}
        total_margin  = 0.0
        total_disc    = 0.0
        total_lev     = 0.0
        total_walk    = 0.0
        total_ptv     = 0.0

        for r in self._results:
            risk_counts[r.discount_risk.value]      = risk_counts.get(r.discount_risk.value, 0) + 1
            stage_counts[r.negotiation_stage.value] = stage_counts.get(r.negotiation_stage.value, 0) + 1
            strat_counts[r.pricing_strategy.value]  = strat_counts.get(r.pricing_strategy.value, 0) + 1
            margin_counts[r.margin_health.value]    = margin_counts.get(r.margin_health.value, 0) + 1
            total_margin += r.gross_margin_pct
            total_disc   += r.effective_discount_pct
            total_lev    += r.negotiation_leverage
            total_walk   += r.walkaway_risk
            total_ptv    += r.price_to_value_score

        return {
            "total":                     n,
            "risk_counts":               risk_counts,
            "stage_counts":              stage_counts,
            "strategy_counts":           strat_counts,
            "margin_health_counts":      margin_counts,
            "avg_gross_margin_pct":      round(total_margin / n, 1),
            "avg_effective_discount":    round(total_disc / n, 1),
            "avg_negotiation_leverage":  round(total_lev / n, 1),
            "avg_walkaway_risk":         round(total_walk / n, 1),
            "high_risk_count":           len(self.high_risk_deals),
            "strategic_count":           len(self.strategic_deals),
            "walk_away_count":           len(self.walk_away_candidates),
            "avg_price_to_value_score":  round(total_ptv / n, 1),
        }
