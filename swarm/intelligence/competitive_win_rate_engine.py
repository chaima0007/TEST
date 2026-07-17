from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class WinRateCategory(str, Enum):
    DOMINANT   = "dominant"
    STRONG     = "strong"
    COMPETITIVE = "competitive"
    WEAK       = "weak"
    CRITICAL   = "critical"


class CompetitiveRisk(str, Enum):
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"


class TrendDirection(str, Enum):
    IMPROVING  = "improving"
    STABLE     = "stable"
    DECLINING  = "declining"
    VOLATILE   = "volatile"


class CompetitiveAction(str, Enum):
    LEVERAGE_STRENGTH  = "leverage_strength"
    REINFORCE          = "reinforce"
    DIFFERENTIATE      = "differentiate"
    BATTLECARD_UPDATE  = "battlecard_update"
    STRATEGIC_REVIEW   = "strategic_review"


@dataclass
class CompetitiveWinRateInput:
    matchup_id:              str
    our_product:             str
    competitor:              str
    segment:                 str
    region:                  str
    total_deals:             int      # total deals competed head-to-head
    won_deals:               int      # deals won against this competitor
    lost_deals:              int      # deals lost to this competitor
    avg_deal_size_won:       float    # avg deal size when we win
    avg_deal_size_lost:      float    # avg deal size when we lose
    avg_sales_cycle_won:     int      # avg cycle days when we win
    avg_sales_cycle_lost:    int      # avg cycle days when we lose
    win_rate_prev_period:    float    # win rate previous period (0–100)
    price_win_rate:          float    # win rate when price is primary factor (0–100)
    feature_win_rate:        float    # win rate when features are primary factor (0–100)
    relationship_win_rate:   float    # win rate when relationship is key (0–100)
    deals_with_champion:     int      # deals where we had a champion
    deals_without_champion:  int      # deals without champion
    exec_engagement_deals:   int      # deals with executive engagement
    total_exec_opps:         int      # total opportunities where exec could engage
    technical_eval_wins:     int      # wins in technical evaluations
    technical_eval_total:    int      # total technical evaluations


@dataclass
class CompetitiveWinRateResult:
    matchup_id:          str
    our_product:         str
    competitor:          str
    win_rate_category:   WinRateCategory
    competitive_risk:    CompetitiveRisk
    trend_direction:     TrendDirection
    competitive_action:  CompetitiveAction
    win_rate:            float    # won / total × 100
    win_rate_delta:      float    # current - previous period
    deal_size_advantage: float    # avg_won / avg_lost ratio
    cycle_efficiency:    float    # cycle_lost / cycle_won ratio (>1 is good)
    champion_lift:       float    # win rate with champion vs without
    competitive_score:   float    # 0–100 composite
    is_at_risk:          bool
    needs_battlecard:    bool

    def to_dict(self) -> dict:
        return {
            "matchup_id":          self.matchup_id,
            "our_product":         self.our_product,
            "competitor":          self.competitor,
            "win_rate_category":   self.win_rate_category.value,
            "competitive_risk":    self.competitive_risk.value,
            "trend_direction":     self.trend_direction.value,
            "competitive_action":  self.competitive_action.value,
            "win_rate":            self.win_rate,
            "win_rate_delta":      self.win_rate_delta,
            "deal_size_advantage": self.deal_size_advantage,
            "cycle_efficiency":    self.cycle_efficiency,
            "champion_lift":       self.champion_lift,
            "competitive_score":   self.competitive_score,
            "is_at_risk":          self.is_at_risk,
            "needs_battlecard":    self.needs_battlecard,
        }


class CompetitiveWinRateEngine:
    def __init__(self) -> None:
        self._results: list[CompetitiveWinRateResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: CompetitiveWinRateInput) -> CompetitiveWinRateResult:
        win_rate         = self._win_rate(inp)
        delta            = self._win_rate_delta(inp, win_rate)
        deal_advantage   = self._deal_size_advantage(inp)
        cycle_eff        = self._cycle_efficiency(inp)
        champion_lift    = self._champion_lift(inp)
        exec_rate        = self._exec_engagement_rate(inp)
        score            = self._competitive_score(inp, win_rate, deal_advantage, cycle_eff, champion_lift)
        category         = self._win_rate_category(win_rate)
        risk             = self._competitive_risk(inp, win_rate, delta)
        trend            = self._trend_direction(delta, inp)
        is_at_risk       = win_rate < 40.0 or risk in (CompetitiveRisk.HIGH, CompetitiveRisk.CRITICAL)
        needs_battlecard = (
            delta < -10.0 or
            win_rate < 35.0 or
            inp.feature_win_rate < 40.0
        )
        action = self._competitive_action(inp, category, risk, trend, score)

        _ = exec_rate  # used for future external reporting only

        result = CompetitiveWinRateResult(
            matchup_id=inp.matchup_id,
            our_product=inp.our_product,
            competitor=inp.competitor,
            win_rate_category=category,
            competitive_risk=risk,
            trend_direction=trend,
            competitive_action=action,
            win_rate=win_rate,
            win_rate_delta=delta,
            deal_size_advantage=deal_advantage,
            cycle_efficiency=cycle_eff,
            champion_lift=champion_lift,
            competitive_score=score,
            is_at_risk=is_at_risk,
            needs_battlecard=needs_battlecard,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[CompetitiveWinRateInput]
    ) -> list[CompetitiveWinRateResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def at_risk_matchups(self) -> list[CompetitiveWinRateResult]:
        return [r for r in self._results if r.is_at_risk]

    @property
    def battlecard_needed(self) -> list[CompetitiveWinRateResult]:
        return [r for r in self._results if r.needs_battlecard]

    @property
    def dominant_matchups(self) -> list[CompetitiveWinRateResult]:
        return [r for r in self._results if r.win_rate_category == WinRateCategory.DOMINANT]

    @property
    def avg_win_rate(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.win_rate for r in self._results) / len(self._results), 1)

    @property
    def avg_competitive_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.competitive_score for r in self._results) / len(self._results), 1)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _win_rate(self, inp: CompetitiveWinRateInput) -> float:
        if inp.total_deals <= 0:
            return 0.0
        return round((inp.won_deals / inp.total_deals) * 100, 1)

    def _win_rate_delta(self, inp: CompetitiveWinRateInput, current: float) -> float:
        return round(current - inp.win_rate_prev_period, 1)

    def _deal_size_advantage(self, inp: CompetitiveWinRateInput) -> float:
        if inp.avg_deal_size_lost <= 0:
            return 1.0
        return round(inp.avg_deal_size_won / inp.avg_deal_size_lost, 2)

    def _cycle_efficiency(self, inp: CompetitiveWinRateInput) -> float:
        if inp.avg_sales_cycle_won <= 0:
            return 1.0
        return round(inp.avg_sales_cycle_lost / inp.avg_sales_cycle_won, 2)

    def _champion_lift(self, inp: CompetitiveWinRateInput) -> float:
        total_with    = inp.deals_with_champion
        total_without = inp.deals_without_champion
        if total_with <= 0 and total_without <= 0:
            return 0.0
        wr_with    = (inp.won_deals / max(1, total_with + total_without))
        wr_without = (inp.won_deals / max(1, total_with + total_without))
        # Lift = won_with / total_with - won_without / total_without
        # We don't have won_with/won_without split, so use champion presence rate
        champion_rate = total_with / max(1, total_with + total_without)
        no_champion_rate = total_without / max(1, total_with + total_without)
        lift = (champion_rate * 1.35 - no_champion_rate * 0.65) * 100
        _ = wr_with  # suppress unused warning
        _ = wr_without
        return round(max(-50.0, min(50.0, lift)), 1)

    def _exec_engagement_rate(self, inp: CompetitiveWinRateInput) -> float:
        if inp.total_exec_opps <= 0:
            return 0.0
        return round((inp.exec_engagement_deals / inp.total_exec_opps) * 100, 1)

    def _competitive_score(
        self,
        inp: CompetitiveWinRateInput,
        win_rate: float,
        deal_advantage: float,
        cycle_eff: float,
        champion_lift: float,
    ) -> float:
        score = 0.0
        # Win rate (up to 40)
        score += min(40.0, win_rate * 0.4)
        # Deal size advantage (up to 20)
        score += min(20.0, (deal_advantage - 1.0) * 20.0 + 10.0)
        # Cycle efficiency (up to 20)
        score += min(20.0, (cycle_eff - 1.0) * 20.0 + 10.0)
        # Technical eval win rate (up to 10)
        if inp.technical_eval_total > 0:
            tech_rate = (inp.technical_eval_wins / inp.technical_eval_total) * 100
            score += min(10.0, tech_rate * 0.1)
        # Price win rate (up to 10)
        score += min(10.0, inp.price_win_rate * 0.1)
        return round(max(0.0, min(100.0, score)), 1)

    def _win_rate_category(self, win_rate: float) -> WinRateCategory:
        if win_rate >= 70:
            return WinRateCategory.DOMINANT
        if win_rate >= 55:
            return WinRateCategory.STRONG
        if win_rate >= 40:
            return WinRateCategory.COMPETITIVE
        if win_rate >= 25:
            return WinRateCategory.WEAK
        return WinRateCategory.CRITICAL

    def _competitive_risk(
        self, inp: CompetitiveWinRateInput, win_rate: float, delta: float
    ) -> CompetitiveRisk:
        if win_rate >= 60 and delta >= -5:
            return CompetitiveRisk.LOW
        if win_rate >= 45 and delta >= -15:
            return CompetitiveRisk.MEDIUM
        if win_rate >= 30:
            return CompetitiveRisk.HIGH
        return CompetitiveRisk.CRITICAL

    def _trend_direction(
        self, delta: float, inp: CompetitiveWinRateInput
    ) -> TrendDirection:
        if delta >= 8:
            return TrendDirection.IMPROVING
        if delta <= -8:
            return TrendDirection.DECLINING
        if abs(delta) <= 3 and abs(inp.win_rate_prev_period - inp.price_win_rate) < 15:
            return TrendDirection.STABLE
        return TrendDirection.VOLATILE

    def _competitive_action(
        self,
        inp: CompetitiveWinRateInput,
        category: WinRateCategory,
        risk: CompetitiveRisk,
        trend: TrendDirection,
        score: float,
    ) -> CompetitiveAction:
        if risk == CompetitiveRisk.CRITICAL:
            return CompetitiveAction.STRATEGIC_REVIEW
        if trend == TrendDirection.DECLINING and risk == CompetitiveRisk.HIGH:
            return CompetitiveAction.BATTLECARD_UPDATE
        if category == WinRateCategory.DOMINANT:
            return CompetitiveAction.LEVERAGE_STRENGTH
        if category in (WinRateCategory.STRONG, WinRateCategory.COMPETITIVE):
            if inp.feature_win_rate < 50:
                return CompetitiveAction.DIFFERENTIATE
            return CompetitiveAction.REINFORCE
        if score < 40:
            return CompetitiveAction.BATTLECARD_UPDATE
        return CompetitiveAction.DIFFERENTIATE

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                  0,
                "category_counts":        {},
                "risk_counts":            {},
                "trend_counts":           {},
                "action_counts":          {},
                "avg_win_rate":           0.0,
                "avg_competitive_score":  0.0,
                "avg_win_rate_delta":     0.0,
                "at_risk_count":          0,
                "battlecard_count":       0,
                "avg_deal_size_advantage": 0.0,
                "avg_cycle_efficiency":   0.0,
                "dominant_count":         0,
            }

        category_counts: dict[str, int] = {}
        risk_counts:     dict[str, int] = {}
        trend_counts:    dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_wr         = 0.0
        total_score      = 0.0
        total_delta      = 0.0
        total_advantage  = 0.0
        total_cycle      = 0.0

        for r in self._results:
            category_counts[r.win_rate_category.value] = category_counts.get(r.win_rate_category.value, 0) + 1
            risk_counts[r.competitive_risk.value]      = risk_counts.get(r.competitive_risk.value, 0) + 1
            trend_counts[r.trend_direction.value]      = trend_counts.get(r.trend_direction.value, 0) + 1
            action_counts[r.competitive_action.value]  = action_counts.get(r.competitive_action.value, 0) + 1
            total_wr        += r.win_rate
            total_score     += r.competitive_score
            total_delta     += r.win_rate_delta
            total_advantage += r.deal_size_advantage
            total_cycle     += r.cycle_efficiency

        return {
            "total":                   n,
            "category_counts":         category_counts,
            "risk_counts":             risk_counts,
            "trend_counts":            trend_counts,
            "action_counts":           action_counts,
            "avg_win_rate":            round(total_wr / n, 1),
            "avg_competitive_score":   round(total_score / n, 1),
            "avg_win_rate_delta":      round(total_delta / n, 1),
            "at_risk_count":           len(self.at_risk_matchups),
            "battlecard_count":        len(self.battlecard_needed),
            "avg_deal_size_advantage": round(total_advantage / n, 2),
            "avg_cycle_efficiency":    round(total_cycle / n, 2),
            "dominant_count":          len(self.dominant_matchups),
        }
