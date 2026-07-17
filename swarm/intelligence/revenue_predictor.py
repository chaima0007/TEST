"""
Revenue Predictor — weighted revenue forecasting from pipeline deal signals.

Adjusts closing probability using lead quality, churn risk, and pipeline stage:
  adjusted_prob = base_prob * lead_factor * churn_factor * stage_factor
  weighted_value = deal_value * adjusted_prob
  ConfidenceLevel: LOW / MEDIUM / HIGH / VERY_HIGH
  RevenuePeriod: MONTHLY / QUARTERLY / ANNUAL
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple


class RevenuePeriod(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"


class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


_STAGE_FACTOR: Dict[str, float] = {
    "prospecting":  0.70,
    "qualified":    0.85,
    "proposal":     0.95,
    "negotiation":  1.00,
    "closing":      1.05,
}

_PERIOD_MONTHS: Dict[RevenuePeriod, int] = {
    RevenuePeriod.MONTHLY:    1,
    RevenuePeriod.QUARTERLY:  3,
    RevenuePeriod.ANNUAL:    12,
}


@dataclass
class DealSignals:
    deal_id: str
    name: str
    company: str
    sector: str
    stage: str
    deal_value_eur: float
    probability: float          # 0.0-1.0 estimated closing probability
    expected_close_days: int    # days until expected close
    lead_score: float           # 0-100 from LeadPrioritizer
    churn_risk_score: float     # 0-100 from CustomerRetention
    months_in_pipeline: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RevenuePrediction:
    deal: DealSignals
    adjusted_probability: float
    weighted_value_eur: float
    confidence: ConfidenceLevel
    expected_close_date_offset_days: int
    risk_factors: List[str]
    upside_factors: List[str]

    def to_dict(self) -> dict:
        return {
            "deal": self.deal.to_dict(),
            "adjusted_probability": self.adjusted_probability,
            "weighted_value_eur": self.weighted_value_eur,
            "confidence": self.confidence.value,
            "expected_close_date_offset_days": self.expected_close_date_offset_days,
            "risk_factors": self.risk_factors,
            "upside_factors": self.upside_factors,
        }


@dataclass
class PeriodForecast:
    period: RevenuePeriod
    predictions: List[RevenuePrediction]
    total_pipeline_eur: float
    expected_revenue_eur: float
    conservative_eur: float
    optimistic_eur: float
    by_stage: Dict[str, dict]
    by_sector: Dict[str, float]
    confidence_distribution: Dict[str, int]

    def to_dict(self) -> dict:
        return {
            "period": self.period.value,
            "predictions": [p.to_dict() for p in self.predictions],
            "total_pipeline_eur": self.total_pipeline_eur,
            "expected_revenue_eur": self.expected_revenue_eur,
            "conservative_eur": self.conservative_eur,
            "optimistic_eur": self.optimistic_eur,
            "by_stage": self.by_stage,
            "by_sector": self.by_sector,
            "confidence_distribution": self.confidence_distribution,
        }


def _lead_factor(lead_score: float) -> float:
    clamped = max(0.0, min(100.0, lead_score))
    return 0.50 + (clamped / 100.0) * 0.50


def _churn_factor(churn_risk_score: float) -> float:
    clamped = max(0.0, min(100.0, churn_risk_score))
    return 1.0 - (clamped / 200.0)


def _stage_factor(stage: str) -> float:
    return _STAGE_FACTOR.get(stage.lower(), 0.80)


def _adjusted_probability(deal: DealSignals) -> float:
    adj = deal.probability * _lead_factor(deal.lead_score) * _churn_factor(deal.churn_risk_score) * _stage_factor(deal.stage)
    return round(max(0.0, min(1.0, adj)), 4)


def _confidence(adj_prob: float, stage: str, lead_score: float) -> ConfidenceLevel:
    stage_l = stage.lower()
    late_stage = stage_l in ("negotiation", "closing")
    mid_stage = stage_l in ("proposal",)

    if adj_prob >= 0.70 and late_stage and lead_score >= 60:
        return ConfidenceLevel.VERY_HIGH
    if adj_prob >= 0.50 and (late_stage or mid_stage):
        return ConfidenceLevel.HIGH
    if adj_prob >= 0.30:
        return ConfidenceLevel.MEDIUM
    return ConfidenceLevel.LOW


def _risk_factors(deal: DealSignals) -> List[str]:
    risks: List[str] = []
    if deal.churn_risk_score > 60:
        risks.append("Haut risque de churn client")
    if deal.months_in_pipeline > 6:
        risks.append("Pipeline trop long (>6 mois)")
    if deal.lead_score < 40:
        risks.append("Score lead faible (<40)")
    if deal.expected_close_days > 90:
        risks.append("Délai de clôture élevé (>90 jours)")
    if deal.probability < 0.30:
        risks.append("Probabilité de base insuffisante")
    return risks


def _upside_factors(deal: DealSignals) -> List[str]:
    upsides: List[str] = []
    if deal.lead_score >= 75:
        upsides.append("Score lead élevé (≥75)")
    if deal.churn_risk_score <= 25:
        upsides.append("Faible risque de churn")
    if deal.stage.lower() in ("negotiation", "closing") and deal.months_in_pipeline <= 3:
        upsides.append("Progression pipeline rapide")
    if deal.deal_value_eur >= 50_000:
        upsides.append("Opportunité haute valeur (≥50k€)")
    if deal.probability >= 0.70:
        upsides.append("Forte probabilité de base")
    return upsides


def _predict_one(deal: DealSignals) -> RevenuePrediction:
    adj_prob = _adjusted_probability(deal)
    weighted = round(deal.deal_value_eur * adj_prob, 2)
    conf = _confidence(adj_prob, deal.stage, deal.lead_score)
    return RevenuePrediction(
        deal=deal,
        adjusted_probability=adj_prob,
        weighted_value_eur=weighted,
        confidence=conf,
        expected_close_date_offset_days=deal.expected_close_days,
        risk_factors=_risk_factors(deal),
        upside_factors=_upside_factors(deal),
    )


def _build_forecast(predictions: List[RevenuePrediction], period: RevenuePeriod) -> PeriodForecast:
    total_pipeline = sum(p.deal.deal_value_eur for p in predictions)
    expected = sum(p.weighted_value_eur for p in predictions)
    conservative = round(expected * 0.75, 2)
    optimistic = round(expected * 1.25, 2)

    by_stage: Dict[str, dict] = {}
    by_sector: Dict[str, float] = {}
    conf_dist: Dict[str, int] = {c.value: 0 for c in ConfidenceLevel}

    for p in predictions:
        stage = p.deal.stage
        if stage not in by_stage:
            by_stage[stage] = {"count": 0, "pipeline_eur": 0.0, "weighted_eur": 0.0}
        by_stage[stage]["count"] += 1
        by_stage[stage]["pipeline_eur"] = round(by_stage[stage]["pipeline_eur"] + p.deal.deal_value_eur, 2)
        by_stage[stage]["weighted_eur"] = round(by_stage[stage]["weighted_eur"] + p.weighted_value_eur, 2)

        sector = p.deal.sector
        by_sector[sector] = round(by_sector.get(sector, 0.0) + p.weighted_value_eur, 2)

        conf_dist[p.confidence.value] += 1

    return PeriodForecast(
        period=period,
        predictions=sorted(predictions, key=lambda p: p.weighted_value_eur, reverse=True),
        total_pipeline_eur=round(total_pipeline, 2),
        expected_revenue_eur=round(expected, 2),
        conservative_eur=conservative,
        optimistic_eur=optimistic,
        by_stage=by_stage,
        by_sector=by_sector,
        confidence_distribution=conf_dist,
    )


class RevenuePredictor:
    def __init__(self) -> None:
        self._predictions: Dict[str, RevenuePrediction] = {}

    def predict(self, deal: DealSignals) -> RevenuePrediction:
        result = _predict_one(deal)
        self._predictions[deal.deal_id] = result
        return result

    def predict_batch(self, deals: List[DealSignals]) -> List[RevenuePrediction]:
        return [self.predict(d) for d in deals]

    def forecast_period(
        self, deals: List[DealSignals], period: RevenuePeriod = RevenuePeriod.QUARTERLY
    ) -> PeriodForecast:
        months = _PERIOD_MONTHS[period]
        days_limit = months * 30
        preds = [self.predict(d) for d in deals]
        in_period = [p for p in preds if p.deal.expected_close_days <= days_limit]
        return _build_forecast(in_period, period)

    def get(self, deal_id: str) -> Optional[RevenuePrediction]:
        return self._predictions.get(deal_id)

    def all_predictions(self) -> List[RevenuePrediction]:
        return sorted(self._predictions.values(), key=lambda p: p.weighted_value_eur, reverse=True)

    def top_opportunities(self, n: int = 5) -> List[RevenuePrediction]:
        return self.all_predictions()[:n]

    def at_risk_deals(self) -> List[RevenuePrediction]:
        return [p for p in self._predictions.values() if p.risk_factors]

    def by_confidence(self, level: ConfidenceLevel) -> List[RevenuePrediction]:
        return [p for p in self._predictions.values() if p.confidence == level]

    def summary(self) -> dict:
        items = list(self._predictions.values())
        count = len(items)
        if count == 0:
            return {
                "total_deals": 0,
                "total_pipeline_eur": 0.0,
                "expected_revenue_eur": 0.0,
                "conservative_eur": 0.0,
                "optimistic_eur": 0.0,
                "avg_adjusted_probability": 0.0,
                "at_risk_count": 0,
                "confidence_distribution": {c.value: 0 for c in ConfidenceLevel},
            }
        total_pipeline = sum(p.deal.deal_value_eur for p in items)
        expected = sum(p.weighted_value_eur for p in items)
        avg_prob = sum(p.adjusted_probability for p in items) / count
        conf_dist = {c.value: 0 for c in ConfidenceLevel}
        for p in items:
            conf_dist[p.confidence.value] += 1
        return {
            "total_deals": count,
            "total_pipeline_eur": round(total_pipeline, 2),
            "expected_revenue_eur": round(expected, 2),
            "conservative_eur": round(expected * 0.75, 2),
            "optimistic_eur": round(expected * 1.25, 2),
            "avg_adjusted_probability": round(avg_prob, 4),
            "at_risk_count": sum(1 for p in items if p.risk_factors),
            "confidence_distribution": conf_dist,
        }

    def reset(self) -> None:
        self._predictions.clear()
