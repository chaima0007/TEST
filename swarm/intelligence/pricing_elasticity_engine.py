from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ElasticityCategory(str, Enum):
    INELASTIC  = "inelastic"
    LOW        = "low"
    MODERATE   = "moderate"
    HIGH       = "high"
    EXTREME    = "extreme"


class PricingRisk(str, Enum):
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"


class PricingStance(str, Enum):
    PREMIUM     = "premium"
    COMPETITIVE = "competitive"
    NEUTRAL     = "neutral"
    DEFENSIVE   = "defensive"
    VULNERABLE  = "vulnerable"


class PricingAction(str, Enum):
    INCREASE          = "increase"
    HOLD              = "hold"
    OPTIMIZE          = "optimize"
    DISCOUNT_CONTROL  = "discount_control"
    RESTRUCTURE       = "restructure"


@dataclass
class PricingElasticityInput:
    segment_id:                str
    segment_name:              str
    industry:                  str
    region:                    str
    avg_deal_size_current:     float    # current average deal size
    avg_deal_size_prev:        float    # previous period average deal size
    price_increase_pct:        float    # recent price increase applied (0–100)
    deals_before_increase:     int      # deal count before price increase
    deals_after_increase:      int      # deal count after price increase
    price_objection_rate:      float    # % of deals with price objections (0–100)
    discount_request_rate:     float    # % of deals requesting discount (0–100)
    avg_discount_given_pct:    float    # average discount given (0–100)
    win_rate_at_list_price:    float    # win rate at full list price (0–100)
    win_rate_with_discount:    float    # win rate when discount applied (0–100)
    churn_due_to_price:        float    # % of churned accounts citing price (0–100)
    competitive_price_gap:     float    # our price vs avg competitor (positive = we cost more)
    total_pipeline_value:      float    # total pipeline value at stake
    deals_in_pipeline:         int      # number of deals in pipeline
    nps_price_sensitivity:     float    # NPS sub-score on pricing (-100 to 100)
    upsell_conversion_rate:    float    # % of customers accepting upsell (0–100)
    willingness_to_pay_index:  float    # survey-based WTP (0–100)
    contract_length_avg_months: int     # average contract duration


@dataclass
class PricingElasticityResult:
    segment_id:                    str
    segment_name:                  str
    elasticity_category:           ElasticityCategory
    pricing_risk:                  PricingRisk
    pricing_stance:                PricingStance
    pricing_action:                PricingAction
    price_elasticity_index:        float    # 0–100, higher = more price-sensitive
    discount_leak_score:           float    # 0–100, higher = more discount abuse
    competitive_pressure_score:    float    # 0–100
    revenue_at_risk:               float    # estimated $ at risk from current pricing
    expansion_opportunity:         float    # estimated $ opportunity from optimal pricing
    optimal_price_adjustment_pct:  float    # recommended % change (-20 to +20)
    pricing_confidence_score:      float    # 0–100 model confidence
    is_price_sensitive:            bool
    needs_pricing_review:          bool

    def to_dict(self) -> dict:
        return {
            "segment_id":                   self.segment_id,
            "segment_name":                 self.segment_name,
            "elasticity_category":          self.elasticity_category.value,
            "pricing_risk":                 self.pricing_risk.value,
            "pricing_stance":               self.pricing_stance.value,
            "pricing_action":               self.pricing_action.value,
            "price_elasticity_index":       self.price_elasticity_index,
            "discount_leak_score":          self.discount_leak_score,
            "competitive_pressure_score":   self.competitive_pressure_score,
            "revenue_at_risk":              self.revenue_at_risk,
            "expansion_opportunity":        self.expansion_opportunity,
            "optimal_price_adjustment_pct": self.optimal_price_adjustment_pct,
            "pricing_confidence_score":     self.pricing_confidence_score,
            "is_price_sensitive":           self.is_price_sensitive,
            "needs_pricing_review":         self.needs_pricing_review,
        }


class PricingElasticityEngine:
    def __init__(self) -> None:
        self._results: list[PricingElasticityResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: PricingElasticityInput) -> PricingElasticityResult:
        elasticity_idx   = self._price_elasticity_index(inp)
        discount_leak    = self._discount_leak_score(inp)
        comp_pressure    = self._competitive_pressure_score(inp)
        revenue_risk     = self._revenue_at_risk(inp, elasticity_idx, comp_pressure)
        expansion_opp    = self._expansion_opportunity(inp, elasticity_idx)
        optimal_adj      = self._optimal_price_adjustment(inp, elasticity_idx, comp_pressure)
        confidence       = self._pricing_confidence(inp)
        category         = self._elasticity_category(elasticity_idx)
        risk             = self._pricing_risk(inp, elasticity_idx, comp_pressure)
        stance           = self._pricing_stance(inp, elasticity_idx, comp_pressure)
        is_sensitive     = elasticity_idx >= 55.0 or inp.price_objection_rate >= 40.0
        needs_review     = (
            discount_leak >= 50.0 or
            comp_pressure >= 60.0 or
            inp.churn_due_to_price >= 25.0
        )
        action = self._pricing_action(inp, risk, stance, elasticity_idx, discount_leak)

        result = PricingElasticityResult(
            segment_id=inp.segment_id,
            segment_name=inp.segment_name,
            elasticity_category=category,
            pricing_risk=risk,
            pricing_stance=stance,
            pricing_action=action,
            price_elasticity_index=elasticity_idx,
            discount_leak_score=discount_leak,
            competitive_pressure_score=comp_pressure,
            revenue_at_risk=revenue_risk,
            expansion_opportunity=expansion_opp,
            optimal_price_adjustment_pct=optimal_adj,
            pricing_confidence_score=confidence,
            is_price_sensitive=is_sensitive,
            needs_pricing_review=needs_review,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[PricingElasticityInput]
    ) -> list[PricingElasticityResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def price_sensitive_segments(self) -> list[PricingElasticityResult]:
        return [r for r in self._results if r.is_price_sensitive]

    @property
    def review_needed(self) -> list[PricingElasticityResult]:
        return [r for r in self._results if r.needs_pricing_review]

    @property
    def total_revenue_at_risk(self) -> float:
        return round(sum(r.revenue_at_risk for r in self._results), 2)

    @property
    def total_expansion_opportunity(self) -> float:
        return round(sum(r.expansion_opportunity for r in self._results), 2)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _price_elasticity_index(self, inp: PricingElasticityInput) -> float:
        score = 0.0
        # Price objection rate (up to 30)
        score += min(30.0, inp.price_objection_rate * 0.5)
        # Discount lift: win_rate difference between discounted and list (up to 25)
        discount_lift = max(0.0, inp.win_rate_with_discount - inp.win_rate_at_list_price)
        score += min(25.0, discount_lift * 0.8)
        # Demand response to price increase (up to 25)
        if inp.deals_before_increase > 0 and inp.price_increase_pct > 0:
            demand_change = (inp.deals_before_increase - inp.deals_after_increase) / inp.deals_before_increase
            if demand_change > 0:
                price_elasticity = demand_change / (inp.price_increase_pct / 100)
                score += min(25.0, price_elasticity * 10.0)
        # WTP signal (inverse: low WTP = high elasticity) (up to 20)
        score += min(20.0, (100.0 - inp.willingness_to_pay_index) * 0.2)
        return round(max(0.0, min(100.0, score)), 1)

    def _discount_leak_score(self, inp: PricingElasticityInput) -> float:
        score = 0.0
        # Discount request rate (up to 40)
        score += min(40.0, inp.discount_request_rate * 0.6)
        # Average discount depth (up to 35)
        score += min(35.0, inp.avg_discount_given_pct * 1.0)
        # Gap between list and discounted win rates (up to 25)
        discount_lift = max(0.0, inp.win_rate_with_discount - inp.win_rate_at_list_price)
        score += min(25.0, discount_lift * 0.6)
        return round(max(0.0, min(100.0, score)), 1)

    def _competitive_pressure_score(self, inp: PricingElasticityInput) -> float:
        score = 0.0
        # Positive gap (we're more expensive) under pressure (up to 40)
        if inp.competitive_price_gap > 0:
            score += min(40.0, inp.competitive_price_gap * 2.0)
        # Churn due to price (up to 35)
        score += min(35.0, inp.churn_due_to_price * 0.7)
        # Price NPS sensitivity (negative NPS = high pressure) (up to 25)
        if inp.nps_price_sensitivity < 0:
            score += min(25.0, abs(inp.nps_price_sensitivity) * 0.25)
        return round(max(0.0, min(100.0, score)), 1)

    def _revenue_at_risk(
        self,
        inp: PricingElasticityInput,
        elasticity_idx: float,
        comp_pressure: float,
    ) -> float:
        risk_factor = (elasticity_idx * 0.6 + comp_pressure * 0.4) / 100.0
        return round(inp.total_pipeline_value * risk_factor * 0.3, 2)

    def _expansion_opportunity(
        self, inp: PricingElasticityInput, elasticity_idx: float
    ) -> float:
        if elasticity_idx >= 60:
            return 0.0
        headroom_pct = (60.0 - elasticity_idx) / 60.0
        return round(inp.total_pipeline_value * headroom_pct * 0.15, 2)

    def _optimal_price_adjustment(
        self,
        inp: PricingElasticityInput,
        elasticity_idx: float,
        comp_pressure: float,
    ) -> float:
        # Start from WTP headroom
        if inp.willingness_to_pay_index >= 70 and elasticity_idx < 40:
            adj = min(15.0, (inp.willingness_to_pay_index - 70) * 0.3)
        elif elasticity_idx >= 60 or comp_pressure >= 60:
            adj = max(-15.0, -comp_pressure * 0.1)
        elif inp.avg_discount_given_pct >= 20:
            adj = min(10.0, inp.avg_discount_given_pct * 0.2)
        else:
            adj = 0.0
        return round(max(-20.0, min(20.0, adj)), 1)

    def _pricing_confidence(self, inp: PricingElasticityInput) -> float:
        signals = 0
        if inp.deals_before_increase > 10:
            signals += 20
        if inp.deals_in_pipeline > 20:
            signals += 20
        if inp.willingness_to_pay_index > 0:
            signals += 20
        if inp.contract_length_avg_months >= 12:
            signals += 20
        if inp.upsell_conversion_rate > 0:
            signals += 20
        return round(float(signals), 1)

    def _elasticity_category(self, index: float) -> ElasticityCategory:
        if index >= 75:
            return ElasticityCategory.EXTREME
        if index >= 55:
            return ElasticityCategory.HIGH
        if index >= 35:
            return ElasticityCategory.MODERATE
        if index >= 15:
            return ElasticityCategory.LOW
        return ElasticityCategory.INELASTIC

    def _pricing_risk(
        self, inp: PricingElasticityInput, elasticity: float, comp_pressure: float
    ) -> PricingRisk:
        combined = elasticity * 0.5 + comp_pressure * 0.5
        if combined >= 65 or inp.churn_due_to_price >= 30:
            return PricingRisk.CRITICAL
        if combined >= 45 or inp.price_objection_rate >= 40:
            return PricingRisk.HIGH
        if combined >= 25:
            return PricingRisk.MEDIUM
        return PricingRisk.LOW

    def _pricing_stance(
        self,
        inp: PricingElasticityInput,
        elasticity: float,
        comp_pressure: float,
    ) -> PricingStance:
        if inp.willingness_to_pay_index >= 70 and elasticity < 35:
            return PricingStance.PREMIUM
        if comp_pressure >= 60 or inp.churn_due_to_price >= 25:
            return PricingStance.VULNERABLE
        if comp_pressure >= 40 or elasticity >= 55:
            return PricingStance.DEFENSIVE
        if inp.competitive_price_gap <= -10:
            return PricingStance.COMPETITIVE
        return PricingStance.NEUTRAL

    def _pricing_action(
        self,
        inp: PricingElasticityInput,
        risk: PricingRisk,
        stance: PricingStance,
        elasticity: float,
        discount_leak: float,
    ) -> PricingAction:
        if risk == PricingRisk.CRITICAL or stance == PricingStance.VULNERABLE:
            return PricingAction.RESTRUCTURE
        if discount_leak >= 50:
            return PricingAction.DISCOUNT_CONTROL
        if stance == PricingStance.PREMIUM and elasticity < 35:
            return PricingAction.INCREASE
        if stance in (PricingStance.DEFENSIVE, PricingStance.COMPETITIVE):
            return PricingAction.OPTIMIZE
        if elasticity < 25 and inp.willingness_to_pay_index >= 60:
            return PricingAction.INCREASE
        return PricingAction.HOLD

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                             0,
                "elasticity_counts":                 {},
                "risk_counts":                       {},
                "stance_counts":                     {},
                "action_counts":                     {},
                "avg_price_elasticity_index":        0.0,
                "avg_discount_leak_score":           0.0,
                "total_revenue_at_risk":             0.0,
                "total_expansion_opportunity":       0.0,
                "price_sensitive_count":             0,
                "review_needed_count":               0,
                "avg_competitive_pressure_score":    0.0,
                "avg_optimal_price_adjustment_pct":  0.0,
            }

        elasticity_counts: dict[str, int] = {}
        risk_counts:       dict[str, int] = {}
        stance_counts:     dict[str, int] = {}
        action_counts:     dict[str, int] = {}
        total_elasticity = 0.0
        total_discount   = 0.0
        total_comp_pres  = 0.0
        total_adj        = 0.0

        for r in self._results:
            elasticity_counts[r.elasticity_category.value] = elasticity_counts.get(r.elasticity_category.value, 0) + 1
            risk_counts[r.pricing_risk.value]               = risk_counts.get(r.pricing_risk.value, 0) + 1
            stance_counts[r.pricing_stance.value]           = stance_counts.get(r.pricing_stance.value, 0) + 1
            action_counts[r.pricing_action.value]           = action_counts.get(r.pricing_action.value, 0) + 1
            total_elasticity += r.price_elasticity_index
            total_discount   += r.discount_leak_score
            total_comp_pres  += r.competitive_pressure_score
            total_adj        += r.optimal_price_adjustment_pct

        return {
            "total":                             n,
            "elasticity_counts":                 elasticity_counts,
            "risk_counts":                       risk_counts,
            "stance_counts":                     stance_counts,
            "action_counts":                     action_counts,
            "avg_price_elasticity_index":        round(total_elasticity / n, 1),
            "avg_discount_leak_score":           round(total_discount / n, 1),
            "total_revenue_at_risk":             self.total_revenue_at_risk,
            "total_expansion_opportunity":       self.total_expansion_opportunity,
            "price_sensitive_count":             len(self.price_sensitive_segments),
            "review_needed_count":               len(self.review_needed),
            "avg_competitive_pressure_score":    round(total_comp_pres / n, 1),
            "avg_optimal_price_adjustment_pct":  round(total_adj / n, 1),
        }
