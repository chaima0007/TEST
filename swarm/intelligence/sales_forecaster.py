"""
Sales Forecaster — projects monthly revenue based on pipeline state,
sector multipliers, close probability by stage, and timing signals.

Methodology:
  Expected revenue = Σ (deal_value × close_probability[stage] × sector_mult × timing_mult)
  Confidence = f(data_points, pipeline_age, historical_variance)

Pipeline stages and default close probabilities:
  prospected   → 0.05
  contacted    → 0.12
  qualified    → 0.25
  proposal     → 0.45
  negotiation  → 0.70
  verbal_close → 0.90
  closed_won   → 1.00
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


# ── Enums ─────────────────────────────────────────────────────────────────────

class PipelineStage(str, Enum):
    PROSPECTED   = "prospected"
    CONTACTED    = "contacted"
    QUALIFIED    = "qualified"
    PROPOSAL     = "proposal"
    NEGOTIATION  = "negotiation"
    VERBAL_CLOSE = "verbal_close"
    CLOSED_WON   = "closed_won"


class ForecastScenario(str, Enum):
    PESSIMISTIC = "pessimistic"
    BASE        = "base"
    OPTIMISTIC  = "optimistic"


# ── Configuration ──────────────────────────────────────────────────────────────

_STAGE_PROBABILITY: Dict[PipelineStage, float] = {
    PipelineStage.PROSPECTED:   0.05,
    PipelineStage.CONTACTED:    0.12,
    PipelineStage.QUALIFIED:    0.25,
    PipelineStage.PROPOSAL:     0.45,
    PipelineStage.NEGOTIATION:  0.70,
    PipelineStage.VERBAL_CLOSE: 0.90,
    PipelineStage.CLOSED_WON:   1.00,
}

_SECTOR_MULTIPLIERS: Dict[str, float] = {
    "pme":         1.00,
    "avocat":      1.15,
    "comptable":   1.10,
    "notaire":     1.12,
    "médecin":     0.95,
    "dentiste":    0.98,
    "immobilier":  1.08,
    "restaurant":  0.85,
    "hôtel":       0.90,
    "artisan":     0.80,
    "coiffeur":    0.75,
    "default":     1.00,
}

_SCENARIO_MODIFIERS: Dict[ForecastScenario, float] = {
    ForecastScenario.PESSIMISTIC: 0.65,
    ForecastScenario.BASE:        1.00,
    ForecastScenario.OPTIMISTIC:  1.35,
}


# ── Data models ───────────────────────────────────────────────────────────────

@dataclass
class Deal:
    deal_id:   str
    sector:    str
    stage:     PipelineStage
    value_eur: float
    days_in_stage: int = 0
    agent_id:  str = ""

    @property
    def close_probability(self) -> float:
        base = _STAGE_PROBABILITY[self.stage]
        stale_penalty = max(0, (self.days_in_stage - 14) * 0.005)
        return max(0.01, min(1.0, base - stale_penalty))

    @property
    def sector_multiplier(self) -> float:
        s = self.sector.lower()
        for key, mult in _SECTOR_MULTIPLIERS.items():
            if key in s:
                return mult
        return _SECTOR_MULTIPLIERS["default"]

    @property
    def weighted_value(self) -> float:
        return self.value_eur * self.close_probability * self.sector_multiplier

    def to_dict(self) -> dict:
        return {
            "deal_id":           self.deal_id,
            "sector":            self.sector,
            "stage":             self.stage.value,
            "value_eur":         self.value_eur,
            "days_in_stage":     self.days_in_stage,
            "close_probability": round(self.close_probability, 3),
            "sector_multiplier": round(self.sector_multiplier, 2),
            "weighted_value":    round(self.weighted_value, 2),
        }


@dataclass
class ForecastResult:
    scenario:          ForecastScenario
    expected_revenue:  float
    deals_count:       int
    pipeline_value:    float
    weighted_pipeline: float
    by_stage:          Dict[str, float] = field(default_factory=dict)
    by_sector:         Dict[str, float] = field(default_factory=dict)
    confidence:        float = 0.5      # 0-1
    rationale:         str  = ""

    def to_dict(self) -> dict:
        return {
            "scenario":          self.scenario.value,
            "expected_revenue":  round(self.expected_revenue, 2),
            "deals_count":       self.deals_count,
            "pipeline_value":    round(self.pipeline_value, 2),
            "weighted_pipeline": round(self.weighted_pipeline, 2),
            "by_stage":          {k: round(v, 2) for k, v in self.by_stage.items()},
            "by_sector":         {k: round(v, 2) for k, v in self.by_sector.items()},
            "confidence":        round(self.confidence, 3),
            "rationale":         self.rationale,
        }


# ── Forecaster ────────────────────────────────────────────────────────────────

class SalesForecaster:
    """
    Projects monthly revenue from a pipeline of Deal objects.

    Usage::
        fc = SalesForecaster()
        fc.add_deal(Deal("d1", "avocat", PipelineStage.PROPOSAL, 890))
        fc.add_deal(Deal("d2", "artisan", PipelineStage.NEGOTIATION, 340))
        result = fc.forecast(ForecastScenario.BASE)
        print(result.expected_revenue)
    """

    def __init__(self) -> None:
        self._deals: Dict[str, Deal] = {}
        self._closed_won_history: List[float] = []

    # ── Pipeline management ───────────────────────────────────────────────────

    def add_deal(self, deal: Deal) -> None:
        self._deals[deal.deal_id] = deal

    def update_stage(self, deal_id: str, stage: PipelineStage, days_in_stage: int = 0) -> None:
        if deal_id in self._deals:
            self._deals[deal_id].stage = stage
            self._deals[deal_id].days_in_stage = days_in_stage

    def remove_deal(self, deal_id: str) -> None:
        self._deals.pop(deal_id, None)

    def close_won(self, deal_id: str) -> Optional[float]:
        deal = self._deals.pop(deal_id, None)
        if deal:
            self._closed_won_history.append(deal.value_eur)
            return deal.value_eur
        return None

    def get_deal(self, deal_id: str) -> Optional[Deal]:
        return self._deals.get(deal_id)

    def all_deals(self) -> List[Deal]:
        return list(self._deals.values())

    def deals_by_stage(self, stage: PipelineStage) -> List[Deal]:
        return [d for d in self._deals.values() if d.stage == stage]

    # ── Forecasting ───────────────────────────────────────────────────────────

    def forecast(self, scenario: ForecastScenario = ForecastScenario.BASE) -> ForecastResult:
        deals = list(self._deals.values())
        if not deals:
            return ForecastResult(
                scenario=scenario,
                expected_revenue=0.0,
                deals_count=0,
                pipeline_value=0.0,
                weighted_pipeline=0.0,
                confidence=0.0,
                rationale="Pipeline vide — aucune affaire à prévoir",
            )

        pipeline_value = sum(d.value_eur for d in deals)
        weighted_sum   = sum(d.weighted_value for d in deals)
        modifier       = _SCENARIO_MODIFIERS[scenario]
        expected       = weighted_sum * modifier

        by_stage: Dict[str, float] = {}
        by_sector: Dict[str, float] = {}
        for d in deals:
            by_stage[d.stage.value]  = by_stage.get(d.stage.value, 0) + d.weighted_value
            by_sector[d.sector]      = by_sector.get(d.sector, 0)     + d.weighted_value

        confidence = self._compute_confidence(deals)
        rationale  = self._build_rationale(deals, expected, scenario, confidence)

        return ForecastResult(
            scenario=scenario,
            expected_revenue=expected,
            deals_count=len(deals),
            pipeline_value=pipeline_value,
            weighted_pipeline=weighted_sum,
            by_stage=by_stage,
            by_sector=by_sector,
            confidence=confidence,
            rationale=rationale,
        )

    def all_scenarios(self) -> List[ForecastResult]:
        return [self.forecast(s) for s in ForecastScenario]

    def pipeline_summary(self) -> dict:
        deals = list(self._deals.values())
        by_stage_count: Dict[str, int] = {}
        for d in deals:
            by_stage_count[d.stage.value] = by_stage_count.get(d.stage.value, 0) + 1

        base = self.forecast(ForecastScenario.BASE)
        return {
            "total_deals":        len(deals),
            "pipeline_value_eur": round(sum(d.value_eur for d in deals), 2),
            "weighted_pipeline":  round(base.weighted_pipeline, 2),
            "base_forecast":      round(base.expected_revenue, 2),
            "confidence":         round(base.confidence, 3),
            "by_stage_count":     by_stage_count,
            "closed_won_history": self._closed_won_history[-10:],
        }

    def top_deals(self, n: int = 5) -> List[Deal]:
        return sorted(self._deals.values(), key=lambda d: d.weighted_value, reverse=True)[:n]

    def stale_deals(self, threshold_days: int = 14) -> List[Deal]:
        return [d for d in self._deals.values() if d.days_in_stage >= threshold_days]

    def reset(self) -> None:
        self._deals.clear()
        self._closed_won_history.clear()

    # ── Internal ──────────────────────────────────────────────────────────────

    def _compute_confidence(self, deals: List[Deal]) -> float:
        n = len(deals)
        if n == 0:
            return 0.0
        data_score   = min(1.0, n / 20)
        late_stage   = sum(1 for d in deals if d.stage in (
            PipelineStage.NEGOTIATION, PipelineStage.VERBAL_CLOSE, PipelineStage.PROPOSAL
        ))
        stage_score  = min(1.0, late_stage / max(n, 1))
        history_score = min(1.0, len(self._closed_won_history) / 10)
        return round((data_score * 0.4 + stage_score * 0.4 + history_score * 0.2), 3)

    def _build_rationale(
        self, deals: List[Deal], expected: float, scenario: ForecastScenario, confidence: float
    ) -> str:
        late = sum(1 for d in deals if d.stage in (
            PipelineStage.NEGOTIATION, PipelineStage.VERBAL_CLOSE
        ))
        conf_label = "élevée" if confidence >= 0.7 else "moyenne" if confidence >= 0.4 else "faible"
        scen_label = {"pessimistic": "pessimiste", "base": "de base", "optimistic": "optimiste"}[scenario.value]
        return (
            f"Scénario {scen_label} — {len(deals)} affaires en pipeline, "
            f"{late} en négociation ou verbal close. "
            f"Confiance {conf_label} ({confidence:.0%}). "
            f"Prévision : {expected:,.0f}€."
        )
