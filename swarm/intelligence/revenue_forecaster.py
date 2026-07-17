"""Revenue Forecaster — probabilistic pipeline-to-revenue forecast with scenario analysis."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class DealRisk(str, Enum):
    HIGH = "high"       # likely to slip or be lost
    MEDIUM = "medium"   # needs attention
    LOW = "low"         # solid deal, minor concerns
    NONE = "none"       # high confidence, minimal risk


class QuarterLabel(str, Enum):
    CURRENT = "current_quarter"
    NEXT = "next_quarter"
    BEYOND = "beyond"


class ForecastScenario(str, Enum):
    CONSERVATIVE = "conservative"   # 0.70× adjusted probability
    BASE = "base"                   # 1.00× adjusted probability
    OPTIMISTIC = "optimistic"       # 1.30× adjusted probability (capped 0.97)


_STAGE_WIN_PROB: dict[str, float] = {
    "prospecting": 0.10,
    "qualification": 0.20,
    "demo": 0.35,
    "proposal": 0.50,
    "negotiation": 0.70,
    "closing": 0.85,
}

_STAGE_MAX_DAYS: dict[str, int] = {
    "prospecting": 14, "qualification": 21, "demo": 21,
    "proposal": 30, "negotiation": 21, "closing": 14,
}


@dataclass
class ForecastDeal:
    deal_id: str
    deal_name: str
    amount_eur: float
    stage: str                      # prospecting / qualification / demo / proposal / negotiation / closing
    close_date_days: int            # days from today (negative = overdue)
    segment: str                    # startup / smb / mid_market / enterprise
    days_in_stage: int
    num_competitors: int
    champion_strength: float        # 0-100
    has_verbal_commit: bool
    has_budget_approved: bool
    is_renewal: bool


@dataclass
class ForecastDealResult:
    deal_id: str
    deal_name: str
    amount_eur: float
    stage: str
    segment: str
    close_date_days: int
    base_win_probability_pct: float
    adjusted_win_probability_pct: float
    weighted_value_eur: float           # amount * adjusted_prob
    conservative_value_eur: float
    optimistic_value_eur: float
    deal_risk: DealRisk
    quarter_label: QuarterLabel
    risk_factors: list[str]
    upside_factors: list[str]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["deal_risk"] = self.deal_risk.value
        d["quarter_label"] = self.quarter_label.value
        return d


@dataclass
class RevenueForecast:
    total_pipeline_eur: float
    conservative_forecast_eur: float
    base_forecast_eur: float
    optimistic_forecast_eur: float
    current_quarter_pipeline_eur: float
    next_quarter_pipeline_eur: float
    beyond_pipeline_eur: float
    avg_win_probability_pct: float
    pipeline_health_score: float        # 0-100
    deal_count: int
    high_risk_count: int
    deals: list[ForecastDealResult]
    segment_breakdown: dict[str, float]
    stage_breakdown: dict[str, float]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["deals"] = [deal.to_dict() for deal in self.deals]
        return d


# ─── Calculation helpers ──────────────────────────────────────────────────────

def _quarter_label(close_date_days: int) -> QuarterLabel:
    if close_date_days <= 90:
        return QuarterLabel.CURRENT
    if close_date_days <= 180:
        return QuarterLabel.NEXT
    return QuarterLabel.BEYOND


def _adjusted_win_probability(inp: ForecastDeal) -> float:
    base = _STAGE_WIN_PROB.get(inp.stage.lower(), 0.20)
    adj = 0.0

    # Champion quality
    if inp.champion_strength >= 75:
        adj += 0.08
    elif inp.champion_strength < 40:
        adj -= 0.10

    # Budget commitment
    if inp.has_budget_approved:
        adj += 0.10

    # Verbal commitment (strong signal)
    if inp.has_verbal_commit:
        adj += 0.12

    # Competitive pressure
    if inp.num_competitors >= 4:
        adj -= 0.08
    elif inp.num_competitors >= 2:
        adj -= 0.04

    # Overdue penalty
    if inp.close_date_days < 0:
        adj -= 0.10

    # Stage staleness
    max_days = _STAGE_MAX_DAYS.get(inp.stage.lower(), 21)
    if inp.days_in_stage > max_days * 2:
        adj -= 0.08
    elif inp.days_in_stage > max_days * 1.5:
        adj -= 0.04

    # Renewal uplift
    if inp.is_renewal:
        adj += 0.05

    return round(max(0.03, min(0.97, base + adj)), 3)


def _scenario_probability(adj: float, scenario: ForecastScenario) -> float:
    if scenario == ForecastScenario.CONSERVATIVE:
        return round(max(0.03, adj * 0.70), 3)
    if scenario == ForecastScenario.OPTIMISTIC:
        return round(min(0.97, adj * 1.30), 3)
    return adj


def _deal_risk(inp: ForecastDeal, adj_prob: float) -> DealRisk:
    max_days = _STAGE_MAX_DAYS.get(inp.stage.lower(), 21)
    stale = inp.days_in_stage > max_days * 2
    overdue = inp.close_date_days < 0

    if adj_prob < 0.25 or (overdue and adj_prob < 0.50):
        return DealRisk.HIGH
    if adj_prob < 0.45 or stale:
        return DealRisk.MEDIUM
    if adj_prob >= 0.75:
        return DealRisk.NONE
    return DealRisk.LOW


def _build_factors(inp: ForecastDeal, adj_prob: float) -> tuple[list[str], list[str]]:
    risks: list[str] = []
    upsides: list[str] = []

    if inp.close_date_days < 0:
        risks.append(f"Clôture en retard de {-inp.close_date_days}j — risque de glissement")
    max_days = _STAGE_MAX_DAYS.get(inp.stage.lower(), 21)
    if inp.days_in_stage > max_days * 2:
        risks.append(f"Deal bloqué en {inp.stage} depuis {inp.days_in_stage}j")
    if inp.num_competitors >= 4:
        risks.append(f"{inp.num_competitors} concurrents — pression compétitive forte")
    elif inp.num_competitors >= 2:
        risks.append(f"{inp.num_competitors} concurrents — évaluation comparative en cours")
    if inp.champion_strength < 40:
        risks.append(f"Champion faible ({inp.champion_strength:.0f}/100) — deal instable")
    if not inp.has_budget_approved and inp.stage in ("proposal", "negotiation", "closing"):
        risks.append("Budget non approuvé à ce stade avancé du cycle")

    if inp.has_verbal_commit:
        upsides.append("Engagement verbal confirmé — probabilité de signature élevée")
    if inp.has_budget_approved:
        upsides.append("Budget approuvé — décision financière validée")
    if inp.champion_strength >= 75:
        upsides.append(f"Champion fort ({inp.champion_strength:.0f}/100) — advocacy interne solide")
    if inp.is_renewal:
        upsides.append("Renouvellement — historique client positif")
    if inp.close_date_days > 0 and inp.close_date_days <= 30:
        upsides.append(f"Clôture prévue dans {inp.close_date_days}j — momentum actif")

    return risks, upsides


def _pipeline_health_score(deals: list[ForecastDealResult]) -> float:
    if not deals:
        return 0.0
    avg_prob = sum(d.adjusted_win_probability_pct for d in deals) / len(deals)
    high_risk_pct = sum(1 for d in deals if d.deal_risk == DealRisk.HIGH) / len(deals) * 100
    return round(max(0, min(100, avg_prob - high_risk_pct * 0.3)), 1)


class RevenueForecastEngine:
    """Builds probabilistic revenue forecasts from a sales pipeline."""

    def __init__(self) -> None:
        self._last_forecast: Optional[RevenueForecast] = None

    def forecast(self, deals_input: list[ForecastDeal]) -> RevenueForecast:
        deal_results: list[ForecastDealResult] = []

        for inp in deals_input:
            adj = _adjusted_win_probability(inp)
            base_prob = _STAGE_WIN_PROB.get(inp.stage.lower(), 0.20)
            cons_prob = _scenario_probability(adj, ForecastScenario.CONSERVATIVE)
            opt_prob = _scenario_probability(adj, ForecastScenario.OPTIMISTIC)
            risk = _deal_risk(inp, adj)
            quarter = _quarter_label(inp.close_date_days)
            risk_factors, upside_factors = _build_factors(inp, adj)

            deal_results.append(ForecastDealResult(
                deal_id=inp.deal_id,
                deal_name=inp.deal_name,
                amount_eur=inp.amount_eur,
                stage=inp.stage,
                segment=inp.segment,
                close_date_days=inp.close_date_days,
                base_win_probability_pct=round(base_prob * 100, 1),
                adjusted_win_probability_pct=round(adj * 100, 1),
                weighted_value_eur=round(inp.amount_eur * adj, 2),
                conservative_value_eur=round(inp.amount_eur * cons_prob, 2),
                optimistic_value_eur=round(inp.amount_eur * opt_prob, 2),
                deal_risk=risk,
                quarter_label=quarter,
                risk_factors=risk_factors,
                upside_factors=upside_factors,
            ))

        total_pipeline = sum(d.amount_eur for d in deal_results)
        base_forecast = round(sum(d.weighted_value_eur for d in deal_results), 2)
        cons_forecast = round(sum(d.conservative_value_eur for d in deal_results), 2)
        opt_forecast = round(sum(d.optimistic_value_eur for d in deal_results), 2)

        cq = round(sum(d.weighted_value_eur for d in deal_results if d.quarter_label == QuarterLabel.CURRENT), 2)
        nq = round(sum(d.weighted_value_eur for d in deal_results if d.quarter_label == QuarterLabel.NEXT), 2)
        bq = round(sum(d.weighted_value_eur for d in deal_results if d.quarter_label == QuarterLabel.BEYOND), 2)

        avg_prob = (
            round(sum(d.adjusted_win_probability_pct for d in deal_results) / len(deal_results), 1)
            if deal_results else 0.0
        )

        segment_breakdown: dict[str, float] = {}
        stage_breakdown: dict[str, float] = {}
        for d in deal_results:
            segment_breakdown[d.segment] = round(segment_breakdown.get(d.segment, 0) + d.weighted_value_eur, 2)
            stage_breakdown[d.stage] = round(stage_breakdown.get(d.stage, 0) + d.weighted_value_eur, 2)

        health = _pipeline_health_score(deal_results)

        forecast = RevenueForecast(
            total_pipeline_eur=round(total_pipeline, 2),
            conservative_forecast_eur=cons_forecast,
            base_forecast_eur=base_forecast,
            optimistic_forecast_eur=opt_forecast,
            current_quarter_pipeline_eur=cq,
            next_quarter_pipeline_eur=nq,
            beyond_pipeline_eur=bq,
            avg_win_probability_pct=avg_prob,
            pipeline_health_score=health,
            deal_count=len(deal_results),
            high_risk_count=sum(1 for d in deal_results if d.deal_risk == DealRisk.HIGH),
            deals=sorted(deal_results, key=lambda d: d.weighted_value_eur, reverse=True),
            segment_breakdown=segment_breakdown,
            stage_breakdown=stage_breakdown,
        )
        self._last_forecast = forecast
        return forecast

    def get_last(self) -> Optional[RevenueForecast]:
        return self._last_forecast

    def by_risk(self, risk: DealRisk) -> list[ForecastDealResult]:
        if not self._last_forecast:
            return []
        return [d for d in self._last_forecast.deals if d.deal_risk == risk]

    def by_quarter(self, quarter: QuarterLabel) -> list[ForecastDealResult]:
        if not self._last_forecast:
            return []
        return [d for d in self._last_forecast.deals if d.quarter_label == quarter]

    def high_risk_deals(self) -> list[ForecastDealResult]:
        return self.by_risk(DealRisk.HIGH)

    def current_quarter_deals(self) -> list[ForecastDealResult]:
        return self.by_quarter(QuarterLabel.CURRENT)

    def top_n(self, n: int = 10) -> list[ForecastDealResult]:
        if not self._last_forecast:
            return []
        return self._last_forecast.deals[:n]

    def scenario_summary(self) -> dict:
        if not self._last_forecast:
            return {}
        f = self._last_forecast
        return {
            "conservative": f.conservative_forecast_eur,
            "base": f.base_forecast_eur,
            "optimistic": f.optimistic_forecast_eur,
            "pipeline": f.total_pipeline_eur,
            "conversion_rate_pct": round(f.base_forecast_eur / f.total_pipeline_eur * 100, 1) if f.total_pipeline_eur > 0 else 0.0,
        }

    def reset(self) -> None:
        self._last_forecast = None
