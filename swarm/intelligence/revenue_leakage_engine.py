from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LeakageCategory(str, Enum):
    MINIMAL     = "minimal"
    MODERATE    = "moderate"
    SIGNIFICANT = "significant"
    CRITICAL    = "critical"


class LeakageRisk(str, Enum):
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"


class LeakagePattern(str, Enum):
    DISCOUNT_HEAVY  = "discount_heavy"
    LATE_STAGE_LOSS = "late_stage_loss"
    CHAMPION_DEFICIT = "champion_deficit"
    MULTIYEAR_MISS  = "multiyear_miss"
    MIXED           = "mixed"


class LeakageAction(str, Enum):
    MONITOR              = "monitor"
    PRICING_REVIEW       = "pricing_review"
    CHAMPION_COACHING    = "champion_coaching"
    DEAL_STRUCTURING     = "deal_structuring"
    URGENT_INTERVENTION  = "urgent_intervention"


@dataclass
class RevenuLeakageInput:
    rep_id:                    str
    rep_name:                  str
    region:                    str
    segment:                   str
    total_deals:               int      # total deals closed (won + lost)
    discounted_deals:          int      # deals where discount was applied
    total_discount_value:      float    # total $ discounted across all deals
    avg_list_price:            float    # average list price per deal
    late_stage_losses:         int      # deals lost at stage 4+
    early_stage_exits:         int      # deals that went no-decision before stage 3
    no_decision_deals:         int      # total no-decision outcomes
    deals_without_champion:    int      # closed-lost deals with no champion
    total_deals_with_champion_possible: int  # deals where champion was possible
    deals_missing_exec_sponsor: int     # closed-lost due to no exec sponsor
    total_exec_possible:       int      # deals where exec sponsor was possible
    multiyear_opportunities:   int      # deals where multiyear was an option
    multiyear_closed:          int      # multiyear deals actually closed
    expansion_opportunities:   int      # existing customers with expansion potential
    expansion_closed:          int      # expansions actually closed
    price_objection_deals:     int      # deals lost primarily due to price
    total_pipeline_value:      float    # total current pipeline value
    avg_deal_size:             float    # average won deal size


@dataclass
class RevenuLeakageResult:
    rep_id:                  str
    rep_name:                str
    leakage_category:        LeakageCategory
    leakage_risk:            LeakageRisk
    leakage_pattern:         LeakagePattern
    leakage_action:          LeakageAction
    discount_leakage_score:  float    # 0–100, higher = more leakage
    process_leakage_score:   float    # 0–100
    champion_leakage_score:  float    # 0–100
    expansion_leakage_score: float    # 0–100
    total_leakage_score:     float    # 0–100 composite
    estimated_lost_revenue:  float    # $ estimated revenue lost
    recovery_potential:      float    # 0–100 % recoverable
    is_high_risk:            bool
    needs_coaching:          bool

    def to_dict(self) -> dict:
        return {
            "rep_id":                  self.rep_id,
            "rep_name":                self.rep_name,
            "leakage_category":        self.leakage_category.value,
            "leakage_risk":            self.leakage_risk.value,
            "leakage_pattern":         self.leakage_pattern.value,
            "leakage_action":          self.leakage_action.value,
            "discount_leakage_score":  self.discount_leakage_score,
            "process_leakage_score":   self.process_leakage_score,
            "champion_leakage_score":  self.champion_leakage_score,
            "expansion_leakage_score": self.expansion_leakage_score,
            "total_leakage_score":     self.total_leakage_score,
            "estimated_lost_revenue":  self.estimated_lost_revenue,
            "recovery_potential":      self.recovery_potential,
            "is_high_risk":            self.is_high_risk,
            "needs_coaching":          self.needs_coaching,
        }


class RevenuLeakageEngine:
    def __init__(self) -> None:
        self._results: list[RevenuLeakageResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: RevenuLeakageInput) -> RevenuLeakageResult:
        discount_score   = self._discount_leakage(inp)
        process_score    = self._process_leakage(inp)
        champion_score   = self._champion_leakage(inp)
        expansion_score  = self._expansion_leakage(inp)
        total_score      = self._total_leakage_score(discount_score, process_score,
                                                      champion_score, expansion_score)
        est_lost         = self._estimated_lost_revenue(inp, discount_score, process_score,
                                                        champion_score, expansion_score)
        recovery         = self._recovery_potential(inp, total_score)
        category         = self._leakage_category(total_score)
        risk             = self._leakage_risk(inp, total_score)
        pattern          = self._leakage_pattern(discount_score, process_score,
                                                  champion_score, expansion_score)
        is_high_risk     = total_score >= 60.0 or risk in (LeakageRisk.HIGH, LeakageRisk.CRITICAL)
        needs_coaching   = (
            discount_score >= 50.0 or
            champion_score >= 55.0 or
            process_score  >= 60.0
        )
        action = self._leakage_action(inp, category, risk, pattern, total_score)

        result = RevenuLeakageResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            leakage_category=category,
            leakage_risk=risk,
            leakage_pattern=pattern,
            leakage_action=action,
            discount_leakage_score=discount_score,
            process_leakage_score=process_score,
            champion_leakage_score=champion_score,
            expansion_leakage_score=expansion_score,
            total_leakage_score=total_score,
            estimated_lost_revenue=est_lost,
            recovery_potential=recovery,
            is_high_risk=is_high_risk,
            needs_coaching=needs_coaching,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[RevenuLeakageInput]
    ) -> list[RevenuLeakageResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def high_risk_reps(self) -> list[RevenuLeakageResult]:
        return [r for r in self._results if r.is_high_risk]

    @property
    def coaching_needed(self) -> list[RevenuLeakageResult]:
        return [r for r in self._results if r.needs_coaching]

    @property
    def total_estimated_loss(self) -> float:
        return round(sum(r.estimated_lost_revenue for r in self._results), 2)

    @property
    def avg_leakage_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.total_leakage_score for r in self._results) / len(self._results), 1)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _discount_leakage(self, inp: RevenuLeakageInput) -> float:
        score = 0.0
        if inp.total_deals <= 0:
            return 0.0
        # Discount frequency (up to 40)
        discount_rate = inp.discounted_deals / inp.total_deals
        score += discount_rate * 40.0
        # Discount depth (up to 35)
        if inp.avg_list_price > 0 and inp.total_deals > 0:
            avg_discount_per_deal = inp.total_discount_value / inp.total_deals
            discount_depth = avg_discount_per_deal / inp.avg_list_price
            score += min(35.0, discount_depth * 100.0)
        # Price objection rate (up to 25)
        price_obj_rate = inp.price_objection_deals / inp.total_deals
        score += min(25.0, price_obj_rate * 50.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _process_leakage(self, inp: RevenuLeakageInput) -> float:
        score = 0.0
        if inp.total_deals <= 0:
            return 0.0
        # Late-stage loss rate (up to 45) — most expensive leakage type
        late_loss_rate = inp.late_stage_losses / inp.total_deals
        score += min(45.0, late_loss_rate * 90.0)
        # No-decision rate (up to 30)
        no_dec_rate = inp.no_decision_deals / inp.total_deals
        score += min(30.0, no_dec_rate * 60.0)
        # Early exit rate (up to 25)
        early_exit_rate = inp.early_stage_exits / inp.total_deals
        score += min(25.0, early_exit_rate * 50.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _champion_leakage(self, inp: RevenuLeakageInput) -> float:
        score = 0.0
        # Missing champion loss rate (up to 50)
        if inp.total_deals_with_champion_possible > 0:
            no_champ_rate = inp.deals_without_champion / inp.total_deals_with_champion_possible
            score += min(50.0, no_champ_rate * 70.0)
        # Missing exec sponsor rate (up to 50)
        if inp.total_exec_possible > 0:
            no_exec_rate = inp.deals_missing_exec_sponsor / inp.total_exec_possible
            score += min(50.0, no_exec_rate * 70.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _expansion_leakage(self, inp: RevenuLeakageInput) -> float:
        score = 0.0
        # Multiyear conversion miss (up to 50)
        if inp.multiyear_opportunities > 0:
            multiyear_miss = 1.0 - (inp.multiyear_closed / inp.multiyear_opportunities)
            score += min(50.0, multiyear_miss * 60.0)
        # Expansion conversion miss (up to 50)
        if inp.expansion_opportunities > 0:
            expansion_miss = 1.0 - (inp.expansion_closed / inp.expansion_opportunities)
            score += min(50.0, expansion_miss * 60.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _total_leakage_score(
        self,
        discount: float,
        process: float,
        champion: float,
        expansion: float,
    ) -> float:
        score = (
            discount  * 0.30 +
            process   * 0.35 +
            champion  * 0.20 +
            expansion * 0.15
        )
        return round(max(0.0, min(100.0, score)), 1)

    def _estimated_lost_revenue(
        self,
        inp: RevenuLeakageInput,
        discount_score: float,
        process_score: float,
        champion_score: float,
        expansion_score: float,
    ) -> float:
        lost = 0.0
        # Direct discount give-away
        lost += inp.total_discount_value
        # Late-stage losses
        if inp.total_deals > 0:
            lost += inp.late_stage_losses * inp.avg_deal_size * 0.8
            # No-decision (partial — some would never close)
            lost += inp.no_decision_deals * inp.avg_deal_size * 0.4
        # Missed multiyear uplift (avg 20% annual increase × 2 extra years)
        missed_multiyear = inp.multiyear_opportunities - inp.multiyear_closed
        lost += missed_multiyear * inp.avg_deal_size * 0.4
        # Missed expansion
        missed_expansion = inp.expansion_opportunities - inp.expansion_closed
        lost += missed_expansion * inp.avg_deal_size * 0.6
        return round(max(0.0, lost), 2)

    def _recovery_potential(self, inp: RevenuLeakageInput, total_score: float) -> float:
        # Higher leakage = more recoverable; pipeline size adds opportunity
        base = total_score * 0.7
        if inp.total_pipeline_value > 0 and inp.avg_deal_size > 0:
            pipeline_deals = inp.total_pipeline_value / inp.avg_deal_size
            pipeline_boost = min(20.0, pipeline_deals * 2.0)
            base += pipeline_boost
        return round(max(0.0, min(100.0, base)), 1)

    def _leakage_category(self, total_score: float) -> LeakageCategory:
        if total_score >= 65:
            return LeakageCategory.CRITICAL
        if total_score >= 45:
            return LeakageCategory.SIGNIFICANT
        if total_score >= 25:
            return LeakageCategory.MODERATE
        return LeakageCategory.MINIMAL

    def _leakage_risk(self, inp: RevenuLeakageInput, total_score: float) -> LeakageRisk:
        if total_score >= 65 or inp.late_stage_losses >= 5:
            return LeakageRisk.CRITICAL
        if total_score >= 45 or inp.price_objection_deals >= 4:
            return LeakageRisk.HIGH
        if total_score >= 25:
            return LeakageRisk.MEDIUM
        return LeakageRisk.LOW

    def _leakage_pattern(
        self,
        discount: float,
        process: float,
        champion: float,
        expansion: float,
    ) -> LeakagePattern:
        scores = {
            LeakagePattern.DISCOUNT_HEAVY:   discount,
            LeakagePattern.LATE_STAGE_LOSS:  process,
            LeakagePattern.CHAMPION_DEFICIT: champion,
            LeakagePattern.MULTIYEAR_MISS:   expansion,
        }
        top = max(scores, key=lambda k: scores[k])
        top_score = scores[top]
        # If second-highest is within 15 of top, it's mixed
        others = [v for k, v in scores.items() if k != top]
        if others and max(others) >= top_score - 15:
            return LeakagePattern.MIXED
        return top

    def _leakage_action(
        self,
        inp: RevenuLeakageInput,
        category: LeakageCategory,
        risk: LeakageRisk,
        pattern: LeakagePattern,
        total_score: float,
    ) -> LeakageAction:
        if risk == LeakageRisk.CRITICAL:
            return LeakageAction.URGENT_INTERVENTION
        if pattern == LeakagePattern.CHAMPION_DEFICIT:
            return LeakageAction.CHAMPION_COACHING
        if pattern == LeakagePattern.DISCOUNT_HEAVY:
            return LeakageAction.PRICING_REVIEW
        if pattern in (LeakagePattern.LATE_STAGE_LOSS, LeakagePattern.MIXED):
            return LeakageAction.DEAL_STRUCTURING
        if total_score >= 25:
            return LeakageAction.DEAL_STRUCTURING
        return LeakageAction.MONITOR

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                        0,
                "category_counts":              {},
                "risk_counts":                  {},
                "pattern_counts":               {},
                "action_counts":                {},
                "avg_discount_leakage_score":   0.0,
                "avg_total_leakage_score":      0.0,
                "total_estimated_lost_revenue": 0.0,
                "high_risk_count":              0,
                "coaching_count":               0,
                "avg_recovery_potential":       0.0,
                "total_pipeline_value_at_risk": 0.0,
                "avg_process_leakage_score":    0.0,
            }

        category_counts: dict[str, int] = {}
        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_discount  = 0.0
        total_score     = 0.0
        total_recovery  = 0.0
        total_process   = 0.0

        for r in self._results:
            category_counts[r.leakage_category.value] = category_counts.get(r.leakage_category.value, 0) + 1
            risk_counts[r.leakage_risk.value]          = risk_counts.get(r.leakage_risk.value, 0) + 1
            pattern_counts[r.leakage_pattern.value]    = pattern_counts.get(r.leakage_pattern.value, 0) + 1
            action_counts[r.leakage_action.value]      = action_counts.get(r.leakage_action.value, 0) + 1
            total_discount += r.discount_leakage_score
            total_score    += r.total_leakage_score
            total_recovery += r.recovery_potential
            total_process  += r.process_leakage_score

        return {
            "total":                        n,
            "category_counts":              category_counts,
            "risk_counts":                  risk_counts,
            "pattern_counts":               pattern_counts,
            "action_counts":                action_counts,
            "avg_discount_leakage_score":   round(total_discount / n, 1),
            "avg_total_leakage_score":      round(total_score / n, 1),
            "total_estimated_lost_revenue": self.total_estimated_loss,
            "high_risk_count":              len(self.high_risk_reps),
            "coaching_count":               len(self.coaching_needed),
            "avg_recovery_potential":       round(total_recovery / n, 1),
            "total_pipeline_value_at_risk": round(sum(r.estimated_lost_revenue for r in self._results), 2),
            "avg_process_leakage_score":    round(total_process / n, 1),
        }
