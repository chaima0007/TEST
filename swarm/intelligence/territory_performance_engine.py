from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TerritoryStatus(str, Enum):
    OVERPERFORMING  = "overperforming"
    ON_TARGET       = "on_target"
    UNDERPERFORMING = "underperforming"
    CRITICAL        = "critical"


class TerritoryRisk(str, Enum):
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"


class MarketPenetration(str, Enum):
    SATURATED    = "saturated"
    HIGH         = "high"
    MEDIUM       = "medium"
    LOW          = "low"
    UNTAPPED     = "untapped"


class TerritoryAction(str, Enum):
    MAINTAIN           = "maintain"
    EXPAND             = "expand"
    FOCUS              = "focus"
    REBALANCE          = "rebalance"
    URGENT_INTERVENTION = "urgent_intervention"


@dataclass
class TerritoryPerformanceInput:
    territory_id:          str
    territory_name:        str
    rep_id:                str
    region:                str
    target_revenue:        float    # period revenue target
    actual_revenue:        float    # revenue achieved so far
    projected_revenue:     float    # projected end-of-period
    total_accounts:        int      # accounts in territory
    active_accounts:       int      # accounts with activity in period
    new_accounts_won:      int      # new logos acquired
    churned_accounts:      int      # accounts lost
    total_addressable_mkt: float    # TAM for territory
    current_penetration:   float    # % of TAM currently captured (0–100)
    pipeline_value:        float    # open pipeline
    weighted_pipeline:     float    # probability-weighted pipeline
    avg_deal_size:         float
    win_rate:              float    # 0–100
    avg_sales_cycle_days:  int
    activities_count:      int      # total activities (calls/emails/meetings)
    days_remaining:        int
    total_period_days:     int


@dataclass
class TerritoryPerformanceResult:
    territory_id:          str
    territory_name:        str
    territory_status:      TerritoryStatus
    territory_risk:        TerritoryRisk
    market_penetration:    MarketPenetration
    territory_action:      TerritoryAction
    attainment_pct:        float    # actual_revenue / target_revenue × 100
    projected_attainment:  float    # projected_revenue / target_revenue × 100
    coverage_ratio:        float    # (actual + weighted_pipeline) / target
    penetration_pct:       float    # actual current_penetration
    account_health_score:  float    # 0–100
    activity_score:        float    # 0–100
    growth_score:          float    # 0–100
    is_at_risk:            bool
    needs_rebalancing:     bool

    def to_dict(self) -> dict:
        return {
            "territory_id":        self.territory_id,
            "territory_name":      self.territory_name,
            "territory_status":    self.territory_status.value,
            "territory_risk":      self.territory_risk.value,
            "market_penetration":  self.market_penetration.value,
            "territory_action":    self.territory_action.value,
            "attainment_pct":      self.attainment_pct,
            "projected_attainment": self.projected_attainment,
            "coverage_ratio":      self.coverage_ratio,
            "penetration_pct":     self.penetration_pct,
            "account_health_score": self.account_health_score,
            "activity_score":      self.activity_score,
            "growth_score":        self.growth_score,
            "is_at_risk":          self.is_at_risk,
            "needs_rebalancing":   self.needs_rebalancing,
        }


class TerritoryPerformanceEngine:
    def __init__(self) -> None:
        self._results: list[TerritoryPerformanceResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: TerritoryPerformanceInput) -> TerritoryPerformanceResult:
        attainment    = self._attainment_pct(inp)
        projected     = self._projected_attainment(inp)
        coverage      = self._coverage_ratio(inp)
        account_health = self._account_health_score(inp)
        activity      = self._activity_score(inp)
        growth        = self._growth_score(inp, account_health, activity)
        status        = self._territory_status(projected)
        risk          = self._territory_risk(inp, projected, account_health)
        penetration   = self._market_penetration(inp.current_penetration)
        is_at_risk    = projected < 80.0 or risk in (TerritoryRisk.HIGH, TerritoryRisk.CRITICAL)
        needs_rebalancing = (
            inp.current_penetration > 60.0 or
            (inp.total_accounts > 0 and inp.active_accounts / inp.total_accounts < 0.3)
        )
        action = self._territory_action(inp, status, risk, penetration, coverage)

        result = TerritoryPerformanceResult(
            territory_id=inp.territory_id,
            territory_name=inp.territory_name,
            territory_status=status,
            territory_risk=risk,
            market_penetration=penetration,
            territory_action=action,
            attainment_pct=attainment,
            projected_attainment=projected,
            coverage_ratio=coverage,
            penetration_pct=inp.current_penetration,
            account_health_score=account_health,
            activity_score=activity,
            growth_score=growth,
            is_at_risk=is_at_risk,
            needs_rebalancing=needs_rebalancing,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[TerritoryPerformanceInput]
    ) -> list[TerritoryPerformanceResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def at_risk_territories(self) -> list[TerritoryPerformanceResult]:
        return [r for r in self._results if r.is_at_risk]

    @property
    def rebalancing_territories(self) -> list[TerritoryPerformanceResult]:
        return [r for r in self._results if r.needs_rebalancing]

    @property
    def high_performing_territories(self) -> list[TerritoryPerformanceResult]:
        return [r for r in self._results if r.territory_status in (
            TerritoryStatus.OVERPERFORMING, TerritoryStatus.ON_TARGET
        )]

    @property
    def total_revenue_gap(self) -> float:
        total = 0.0
        for r in self._results:
            # Cannot compute gap without original targets, so use coverage proxy
            # gap ≈ 0 when projected ≥ 100
            if r.projected_attainment < 100.0:
                total += (100.0 - r.projected_attainment) / 100.0
        return round(total, 2)

    @property
    def avg_attainment(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.attainment_pct for r in self._results) / len(self._results), 1)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _attainment_pct(self, inp: TerritoryPerformanceInput) -> float:
        if inp.target_revenue <= 0:
            return 0.0
        return round((inp.actual_revenue / inp.target_revenue) * 100, 1)

    def _projected_attainment(self, inp: TerritoryPerformanceInput) -> float:
        if inp.target_revenue <= 0:
            return 0.0
        return round((inp.projected_revenue / inp.target_revenue) * 100, 1)

    def _coverage_ratio(self, inp: TerritoryPerformanceInput) -> float:
        if inp.target_revenue <= 0:
            return 0.0
        return round((inp.actual_revenue + inp.weighted_pipeline) / inp.target_revenue, 2)

    def _account_health_score(self, inp: TerritoryPerformanceInput) -> float:
        score = 0.0
        # Active account ratio (up to 40)
        if inp.total_accounts > 0:
            active_ratio = inp.active_accounts / inp.total_accounts
            score += active_ratio * 40.0
        # New account growth (up to 30)
        if inp.total_accounts > 0:
            growth_rate = inp.new_accounts_won / max(1, inp.total_accounts) * 100
            score += min(30.0, growth_rate * 3.0)
        # Churn penalty (up to -20)
        if inp.total_accounts > 0:
            churn_rate = inp.churned_accounts / inp.total_accounts
            score -= churn_rate * 40.0
        # Win rate contribution (up to 30)
        score += inp.win_rate * 0.30
        return round(max(0.0, min(100.0, score)), 1)

    def _activity_score(self, inp: TerritoryPerformanceInput) -> float:
        if inp.total_period_days <= 0 or inp.total_accounts <= 0:
            return 0.0
        days_elapsed = max(1, inp.total_period_days - inp.days_remaining)
        activities_per_day = inp.activities_count / days_elapsed
        activities_per_account = inp.activities_count / inp.total_accounts
        score = min(50.0, activities_per_day * 5.0) + min(50.0, activities_per_account * 5.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _growth_score(
        self, inp: TerritoryPerformanceInput, account_health: float, activity: float
    ) -> float:
        score = 0.0
        # Pipeline coverage (up to 40)
        if inp.target_revenue > 0:
            pipe_ratio = inp.pipeline_value / inp.target_revenue
            score += min(40.0, pipe_ratio * 20.0)
        # Account health contribution (30%)
        score += account_health * 0.30
        # Activity contribution (30%)
        score += activity * 0.30
        return round(max(0.0, min(100.0, score)), 1)

    def _territory_status(self, projected: float) -> TerritoryStatus:
        if projected >= 105:
            return TerritoryStatus.OVERPERFORMING
        if projected >= 90:
            return TerritoryStatus.ON_TARGET
        if projected >= 70:
            return TerritoryStatus.UNDERPERFORMING
        return TerritoryStatus.CRITICAL

    def _territory_risk(
        self, inp: TerritoryPerformanceInput, projected: float, account_health: float
    ) -> TerritoryRisk:
        if projected >= 95 and account_health >= 65:
            return TerritoryRisk.LOW
        if projected >= 80 and account_health >= 45:
            return TerritoryRisk.MEDIUM
        if projected >= 60:
            return TerritoryRisk.HIGH
        return TerritoryRisk.CRITICAL

    def _market_penetration(self, pct: float) -> MarketPenetration:
        if pct >= 70:
            return MarketPenetration.SATURATED
        if pct >= 50:
            return MarketPenetration.HIGH
        if pct >= 25:
            return MarketPenetration.MEDIUM
        if pct >= 10:
            return MarketPenetration.LOW
        return MarketPenetration.UNTAPPED

    def _territory_action(
        self,
        inp: TerritoryPerformanceInput,
        status: TerritoryStatus,
        risk: TerritoryRisk,
        penetration: MarketPenetration,
        coverage: float,
    ) -> TerritoryAction:
        if risk == TerritoryRisk.CRITICAL:
            return TerritoryAction.URGENT_INTERVENTION
        if status == TerritoryStatus.UNDERPERFORMING and risk == TerritoryRisk.HIGH:
            return TerritoryAction.FOCUS
        if penetration == MarketPenetration.SATURATED and coverage >= 1.0:
            return TerritoryAction.REBALANCE
        if penetration in (MarketPenetration.LOW, MarketPenetration.UNTAPPED):
            return TerritoryAction.EXPAND
        if status in (TerritoryStatus.OVERPERFORMING, TerritoryStatus.ON_TARGET):
            return TerritoryAction.MAINTAIN
        return TerritoryAction.FOCUS

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                    0,
                "status_counts":            {},
                "risk_counts":              {},
                "penetration_counts":       {},
                "action_counts":            {},
                "avg_attainment_pct":       0.0,
                "avg_projected_attainment": 0.0,
                "total_revenue_gap":        0.0,
                "at_risk_count":            0,
                "rebalancing_count":        0,
                "avg_account_health":       0.0,
                "avg_growth_score":         0.0,
                "high_performing_count":    0,
            }

        status_counts:      dict[str, int] = {}
        risk_counts:        dict[str, int] = {}
        penetration_counts: dict[str, int] = {}
        action_counts:      dict[str, int] = {}
        total_attainment    = 0.0
        total_projected     = 0.0
        total_health        = 0.0
        total_growth        = 0.0

        for r in self._results:
            status_counts[r.territory_status.value]   = status_counts.get(r.territory_status.value, 0) + 1
            risk_counts[r.territory_risk.value]        = risk_counts.get(r.territory_risk.value, 0) + 1
            penetration_counts[r.market_penetration.value] = penetration_counts.get(r.market_penetration.value, 0) + 1
            action_counts[r.territory_action.value]    = action_counts.get(r.territory_action.value, 0) + 1
            total_attainment += r.attainment_pct
            total_projected  += r.projected_attainment
            total_health     += r.account_health_score
            total_growth     += r.growth_score

        return {
            "total":                    n,
            "status_counts":            status_counts,
            "risk_counts":              risk_counts,
            "penetration_counts":       penetration_counts,
            "action_counts":            action_counts,
            "avg_attainment_pct":       round(total_attainment / n, 1),
            "avg_projected_attainment": round(total_projected / n, 1),
            "total_revenue_gap":        self.total_revenue_gap,
            "at_risk_count":            len(self.at_risk_territories),
            "rebalancing_count":        len(self.rebalancing_territories),
            "avg_account_health":       round(total_health / n, 1),
            "avg_growth_score":         round(total_growth / n, 1),
            "high_performing_count":    len(self.high_performing_territories),
        }
