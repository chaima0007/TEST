from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ExpansionReadinessTier(str, Enum):
    NOT_READY = "not_ready"
    BUILDING  = "building"
    READY     = "ready"
    PRIMED    = "primed"


class ExpansionMotion(str, Enum):
    SEAT_EXPANSION = "seat_expansion"
    UPSELL_TIER    = "upsell_tier"
    CROSS_SELL     = "cross_sell"
    RENEWAL_LOCK   = "renewal_lock"
    HOLD           = "hold"


class ExpansionPriority(str, Enum):
    LOW    = "low"
    MEDIUM = "medium"
    HIGH   = "high"
    URGENT = "urgent"


class ExpansionAction(str, Enum):
    MAINTAIN         = "maintain"
    NURTURE          = "nurture"
    ENGAGE           = "engage"
    CLOSE_EXPANSION  = "close_expansion"


@dataclass
class CustomerExpansionInput:
    account_id:                  str
    account_name:                str
    industry:                    str
    region:                      str
    current_mrr:                 float    # current monthly recurring revenue
    contract_end_months:         int      # months until contract renewal
    seats_used:                  int      # seats actively in use
    seats_purchased:             int      # seats on current contract
    max_seats_available:         int      # max seats on current tier
    feature_adoption_rate:       float    # % of available features actively used (0-100)
    nps_score:                   float    # net promoter score (-100 to 100)
    support_health_score:        float    # 0-100, higher = healthier
    executive_engagement_score:  float    # 0-100 (exec-level relationship strength)
    last_qbr_months_ago:         int      # months since last QBR / EBR
    expansion_conversations_had: int      # count of expansion discussions initiated
    upsell_opportunity_count:    int      # identified upsell opportunities in CRM
    cross_sell_products_eligible: int     # number of add-on products the account qualifies for
    contract_size_growth_yoy_pct: float   # % growth in contract value year-over-year
    avg_mau_pct:                 float    # % of purchased seats that are monthly active (0-100)
    business_outcomes_pct:       float    # % of agreed success criteria met (0-100)
    competitor_interest_signals: int      # detected competitor evaluation events
    champion_strength_score:     float    # 0-100 (champion advocacy + access strength)


@dataclass
class CustomerExpansionResult:
    account_id:                  str
    account_name:                str
    expansion_readiness_tier:    ExpansionReadinessTier
    expansion_motion:            ExpansionMotion
    expansion_priority:          ExpansionPriority
    expansion_action:            ExpansionAction
    product_depth_score:         float    # 0-100
    relationship_strength_score: float    # 0-100
    financial_health_score:      float    # 0-100
    timing_score:                float    # 0-100 (urgency/timing signal)
    expansion_readiness_score:   float    # 0-100 composite
    estimated_expansion_arr:     float    # estimated $ expansion opportunity (annual)
    expansion_confidence_score:  float    # 0-100 model confidence
    is_expansion_ready:          bool
    needs_success_intervention:  bool

    def to_dict(self) -> dict:
        return {
            "account_id":                   self.account_id,
            "account_name":                 self.account_name,
            "expansion_readiness_tier":     self.expansion_readiness_tier.value,
            "expansion_motion":             self.expansion_motion.value,
            "expansion_priority":           self.expansion_priority.value,
            "expansion_action":             self.expansion_action.value,
            "product_depth_score":          self.product_depth_score,
            "relationship_strength_score":  self.relationship_strength_score,
            "financial_health_score":       self.financial_health_score,
            "timing_score":                 self.timing_score,
            "expansion_readiness_score":    self.expansion_readiness_score,
            "estimated_expansion_arr":      self.estimated_expansion_arr,
            "expansion_confidence_score":   self.expansion_confidence_score,
            "is_expansion_ready":           self.is_expansion_ready,
            "needs_success_intervention":   self.needs_success_intervention,
        }


class CustomerExpansionReadinessEngine:
    def __init__(self) -> None:
        self._results: list[CustomerExpansionResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: CustomerExpansionInput) -> CustomerExpansionResult:
        prod_depth   = self._product_depth_score(inp)
        rel_strength = self._relationship_strength_score(inp)
        fin_health   = self._financial_health_score(inp)
        timing       = self._timing_score(inp)
        readiness    = self._expansion_readiness_score(prod_depth, rel_strength, fin_health, timing)
        tier         = self._readiness_tier(readiness)
        motion       = self._expansion_motion(inp, prod_depth, readiness)
        priority     = self._expansion_priority(inp, readiness, timing)
        est_arr      = self._estimated_expansion_arr(inp, readiness)
        confidence   = self._expansion_confidence(inp)
        is_ready     = readiness >= 60.0 and inp.nps_score >= 20.0
        needs_interv = (
            inp.nps_score < 0 or
            inp.support_health_score < 40.0 or
            inp.avg_mau_pct < 40.0
        )
        action = self._expansion_action(tier, priority, is_ready, needs_interv)

        result = CustomerExpansionResult(
            account_id=inp.account_id,
            account_name=inp.account_name,
            expansion_readiness_tier=tier,
            expansion_motion=motion,
            expansion_priority=priority,
            expansion_action=action,
            product_depth_score=prod_depth,
            relationship_strength_score=rel_strength,
            financial_health_score=fin_health,
            timing_score=timing,
            expansion_readiness_score=readiness,
            estimated_expansion_arr=est_arr,
            expansion_confidence_score=confidence,
            is_expansion_ready=is_ready,
            needs_success_intervention=needs_interv,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[CustomerExpansionInput]
    ) -> list[CustomerExpansionResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def expansion_ready_accounts(self) -> list[CustomerExpansionResult]:
        return [r for r in self._results if r.is_expansion_ready]

    @property
    def intervention_needed(self) -> list[CustomerExpansionResult]:
        return [r for r in self._results if r.needs_success_intervention]

    @property
    def total_expansion_arr(self) -> float:
        return round(sum(r.estimated_expansion_arr for r in self._results), 2)

    @property
    def avg_readiness_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.expansion_readiness_score for r in self._results) / len(self._results), 1)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _product_depth_score(self, inp: CustomerExpansionInput) -> float:
        score = 0.0
        # Feature adoption (up to 40)
        score += min(40.0, inp.feature_adoption_rate * 0.4)
        # Seat utilization: using most of purchased seats signals value (up to 30)
        if inp.seats_purchased > 0:
            util = inp.seats_used / inp.seats_purchased * 100
            score += min(30.0, util * 0.3)
        # Monthly active user rate (up to 20)
        score += min(20.0, inp.avg_mau_pct * 0.2)
        # Business outcomes met (up to 10)
        score += min(10.0, inp.business_outcomes_pct * 0.1)
        return round(max(0.0, min(100.0, score)), 1)

    def _relationship_strength_score(self, inp: CustomerExpansionInput) -> float:
        score = 0.0
        # NPS contribution (up to 35): NPS is -100 to 100 → normalize to 0-35
        score += min(35.0, max(0.0, (inp.nps_score + 100) / 200.0 * 35.0))
        # Executive engagement (up to 30)
        score += min(30.0, inp.executive_engagement_score * 0.3)
        # Champion strength (up to 25)
        score += min(25.0, inp.champion_strength_score * 0.25)
        # QBR recency: recent QBR = higher score (up to 10)
        if inp.last_qbr_months_ago <= 3:
            score += 10.0
        elif inp.last_qbr_months_ago <= 6:
            score += 6.0
        elif inp.last_qbr_months_ago <= 12:
            score += 2.0
        return round(max(0.0, min(100.0, score)), 1)

    def _financial_health_score(self, inp: CustomerExpansionInput) -> float:
        score = 0.0
        # Support health (up to 35)
        score += min(35.0, inp.support_health_score * 0.35)
        # Contract growth trajectory (up to 35)
        if inp.contract_size_growth_yoy_pct > 0:
            score += min(35.0, inp.contract_size_growth_yoy_pct * 1.5)
        # Business outcomes met (up to 30)
        score += min(30.0, inp.business_outcomes_pct * 0.3)
        # Competitor signals reduce score (up to -20)
        score -= min(20.0, inp.competitor_interest_signals * 8.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _timing_score(self, inp: CustomerExpansionInput) -> float:
        score = 0.0
        # Renewal proximity: 3-9 months is the sweet spot for expansion conversations (up to 40)
        months = inp.contract_end_months
        if 3 <= months <= 9:
            score += 40.0
        elif 1 <= months < 3:
            score += 25.0  # too close, risky
        elif 10 <= months <= 14:
            score += 20.0
        else:
            score += 5.0
        # Expansion conversations already started (up to 30)
        score += min(30.0, inp.expansion_conversations_had * 10.0)
        # Identified opportunities in CRM (up to 20)
        score += min(20.0, inp.upsell_opportunity_count * 7.0)
        # Competitor pressure creates urgency (up to 10)
        score += min(10.0, inp.competitor_interest_signals * 4.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _expansion_readiness_score(
        self,
        prod_depth: float,
        rel_strength: float,
        fin_health: float,
        timing: float,
    ) -> float:
        composite = (
            prod_depth   * 0.30 +
            rel_strength * 0.30 +
            fin_health   * 0.20 +
            timing       * 0.20
        )
        return round(max(0.0, min(100.0, composite)), 1)

    def _readiness_tier(self, score: float) -> ExpansionReadinessTier:
        if score >= 75:
            return ExpansionReadinessTier.PRIMED
        if score >= 55:
            return ExpansionReadinessTier.READY
        if score >= 35:
            return ExpansionReadinessTier.BUILDING
        return ExpansionReadinessTier.NOT_READY

    def _expansion_motion(
        self, inp: CustomerExpansionInput, prod_depth: float, readiness: float
    ) -> ExpansionMotion:
        if readiness < 30:
            return ExpansionMotion.HOLD
        # Seat headroom: lots of unused purchased seats → seat expansion
        if inp.seats_purchased > 0:
            seat_headroom = (inp.max_seats_available - inp.seats_used) / max(1, inp.max_seats_available)
            if seat_headroom >= 0.3 and prod_depth >= 60:
                return ExpansionMotion.SEAT_EXPANSION
        # Cross-sell: multiple eligible add-on products
        if inp.cross_sell_products_eligible >= 2 and readiness >= 50:
            return ExpansionMotion.CROSS_SELL
        # Renewal lock: high NPS, contract ending soon
        if inp.contract_end_months <= 4 and inp.nps_score >= 40:
            return ExpansionMotion.RENEWAL_LOCK
        # Default upsell
        if readiness >= 50:
            return ExpansionMotion.UPSELL_TIER
        return ExpansionMotion.HOLD

    def _expansion_priority(
        self, inp: CustomerExpansionInput, readiness: float, timing: float
    ) -> ExpansionPriority:
        combined = readiness * 0.6 + timing * 0.4
        if combined >= 70 or (inp.contract_end_months <= 3 and readiness >= 50):
            return ExpansionPriority.URGENT
        if combined >= 52:
            return ExpansionPriority.HIGH
        if combined >= 35:
            return ExpansionPriority.MEDIUM
        return ExpansionPriority.LOW

    def _estimated_expansion_arr(
        self, inp: CustomerExpansionInput, readiness: float
    ) -> float:
        if readiness < 35:
            return 0.0
        base_arr = inp.current_mrr * 12
        # Seat expansion opportunity
        seat_headroom = max(0, inp.max_seats_available - inp.seats_used)
        seat_arr = (seat_headroom * inp.current_mrr / max(1, inp.seats_purchased)) * 12

        # Cross-sell opportunity estimate
        cross_sell_arr = inp.cross_sell_products_eligible * base_arr * 0.15

        # Upsell tier (feature-gated upgrade)
        upsell_arr = base_arr * 0.25 if inp.feature_adoption_rate >= 70 else base_arr * 0.10

        # Apply readiness probability
        probability = readiness / 100.0
        total = (seat_arr * 0.4 + cross_sell_arr * 0.3 + upsell_arr * 0.3) * probability
        return round(max(0.0, total), 2)

    def _expansion_confidence(self, inp: CustomerExpansionInput) -> float:
        signals = 0
        if inp.expansion_conversations_had > 0:
            signals += 20
        if inp.upsell_opportunity_count > 0:
            signals += 20
        if inp.last_qbr_months_ago <= 6:
            signals += 20
        if inp.business_outcomes_pct >= 70:
            signals += 20
        if inp.champion_strength_score >= 60:
            signals += 20
        return round(float(signals), 1)

    def _expansion_action(
        self,
        tier: ExpansionReadinessTier,
        priority: ExpansionPriority,
        is_ready: bool,
        needs_interv: bool,
    ) -> ExpansionAction:
        if needs_interv and not is_ready:
            return ExpansionAction.NURTURE
        if tier == ExpansionReadinessTier.PRIMED or priority == ExpansionPriority.URGENT:
            return ExpansionAction.CLOSE_EXPANSION
        if is_ready or priority == ExpansionPriority.HIGH:
            return ExpansionAction.ENGAGE
        if tier == ExpansionReadinessTier.BUILDING:
            return ExpansionAction.NURTURE
        return ExpansionAction.MAINTAIN

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                          0,
                "tier_counts":                    {},
                "motion_counts":                  {},
                "priority_counts":                {},
                "action_counts":                  {},
                "avg_expansion_readiness_score":  0.0,
                "total_estimated_expansion_arr":  0.0,
                "ready_count":                    0,
                "intervention_needed_count":      0,
                "avg_product_depth_score":        0.0,
                "avg_relationship_strength_score": 0.0,
                "avg_timing_score":               0.0,
                "avg_expansion_confidence_score": 0.0,
            }

        tier_counts:     dict[str, int] = {}
        motion_counts:   dict[str, int] = {}
        priority_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_readiness  = 0.0
        total_prod_depth = 0.0
        total_rel        = 0.0
        total_timing     = 0.0
        total_conf       = 0.0

        for r in self._results:
            tier_counts[r.expansion_readiness_tier.value]  = tier_counts.get(r.expansion_readiness_tier.value, 0) + 1
            motion_counts[r.expansion_motion.value]        = motion_counts.get(r.expansion_motion.value, 0) + 1
            priority_counts[r.expansion_priority.value]    = priority_counts.get(r.expansion_priority.value, 0) + 1
            action_counts[r.expansion_action.value]        = action_counts.get(r.expansion_action.value, 0) + 1
            total_readiness  += r.expansion_readiness_score
            total_prod_depth += r.product_depth_score
            total_rel        += r.relationship_strength_score
            total_timing     += r.timing_score
            total_conf       += r.expansion_confidence_score

        return {
            "total":                           n,
            "tier_counts":                     tier_counts,
            "motion_counts":                   motion_counts,
            "priority_counts":                 priority_counts,
            "action_counts":                   action_counts,
            "avg_expansion_readiness_score":   round(total_readiness / n, 1),
            "total_estimated_expansion_arr":   self.total_expansion_arr,
            "ready_count":                     len(self.expansion_ready_accounts),
            "intervention_needed_count":       len(self.intervention_needed),
            "avg_product_depth_score":         round(total_prod_depth / n, 1),
            "avg_relationship_strength_score": round(total_rel / n, 1),
            "avg_timing_score":                round(total_timing / n, 1),
            "avg_expansion_confidence_score":  round(total_conf / n, 1),
        }
