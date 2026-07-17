"""
Customer Retention — predicts churn risk and lifetime value for active customers.

Churn risk is computed from 5 signals:
  login_recency(25%) + support_tickets(20%) + contract_health(20%)
  + engagement_trend(20%) + nps_score(15%)
  → churn_score 0-100 (high = high risk) → ChurnRisk: LOW/MEDIUM/HIGH/CRITICAL

LTV is estimated from: avg_monthly_revenue × predicted_months_remaining × upsell_multiplier
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional


class ChurnRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class CustomerSignals:
    customer_id: str
    name: str
    company: str
    sector: str
    days_since_last_login: int
    open_support_tickets: int
    contract_months_remaining: int
    engagement_trend: float        # -1.0 (declining) to +1.0 (growing)
    nps_score: int                 # -100 to 100
    avg_monthly_revenue_eur: float
    months_as_customer: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RetentionProfile:
    signals: CustomerSignals
    churn_score: float
    churn_risk: ChurnRisk
    ltv_eur: float
    predicted_months_remaining: int
    risk_factors: List[str]
    retention_actions: List[str]
    score_breakdown: Dict[str, float]

    def to_dict(self) -> dict:
        return {
            "signals": self.signals.to_dict(),
            "churn_score": self.churn_score,
            "churn_risk": self.churn_risk.value,
            "ltv_eur": self.ltv_eur,
            "predicted_months_remaining": self.predicted_months_remaining,
            "risk_factors": self.risk_factors,
            "retention_actions": self.retention_actions,
            "score_breakdown": self.score_breakdown,
        }


_RETENTION_ACTIONS: Dict[ChurnRisk, List[str]] = {
    ChurnRisk.CRITICAL: [
        "Appel de rétention immédiat — directeur de compte",
        "Proposer une remise ou une extension de contrat",
        "Escalader en interne — risque de perte imminent",
    ],
    ChurnRisk.HIGH: [
        "Planifier un QBR (Quarterly Business Review)",
        "Envoyer un rapport de valeur personnalisé",
        "Identifier le décisionnaire et le recontacter",
    ],
    ChurnRisk.MEDIUM: [
        "Email de check-in mensuel automatique",
        "Proposer une session d'onboarding avancé",
        "Partager des cas d'usage similaires à leur secteur",
    ],
    ChurnRisk.LOW: [
        "Identifier les opportunités d'upsell",
        "Inviter au programme ambassadeur",
        "Recueillir un témoignage ou une étude de cas",
    ],
}


def _login_recency_risk(days: int) -> float:
    if days <= 3:
        return 0.0
    if days <= 14:
        return (days - 3) * 5.0
    return min(100.0, 55.0 + (days - 14) * 2.5)


def _ticket_risk(tickets: int) -> float:
    return min(100.0, tickets * 25.0)


def _contract_risk(months_remaining: int) -> float:
    if months_remaining >= 12:
        return 0.0
    if months_remaining >= 6:
        return 20.0
    if months_remaining >= 3:
        return 50.0
    if months_remaining >= 1:
        return 75.0
    return 100.0


def _engagement_trend_risk(trend: float) -> float:
    clamped = max(-1.0, min(1.0, trend))
    return (1.0 - clamped) * 50.0


def _nps_risk(nps: int) -> float:
    clamped = max(-100, min(100, nps))
    return (100 - clamped) / 2.0


def _compute_breakdown(s: CustomerSignals) -> Dict[str, float]:
    return {
        "login_recency": _login_recency_risk(s.days_since_last_login),
        "support_tickets": _ticket_risk(s.open_support_tickets),
        "contract_health": _contract_risk(s.contract_months_remaining),
        "engagement_trend": _engagement_trend_risk(s.engagement_trend),
        "nps_score": _nps_risk(s.nps_score),
    }


_WEIGHTS = {
    "login_recency": 0.25,
    "support_tickets": 0.20,
    "contract_health": 0.20,
    "engagement_trend": 0.20,
    "nps_score": 0.15,
}


def _compute_churn_score(breakdown: Dict[str, float]) -> float:
    raw = sum(breakdown[k] * w for k, w in _WEIGHTS.items())
    return round(max(0.0, min(100.0, raw)), 4)


def _classify_churn(score: float) -> ChurnRisk:
    if score >= 75:
        return ChurnRisk.CRITICAL
    if score >= 55:
        return ChurnRisk.HIGH
    if score >= 35:
        return ChurnRisk.MEDIUM
    return ChurnRisk.LOW


def _predicted_months(churn_score: float, contract_months: int) -> int:
    survival = max(0.0, 1.0 - churn_score / 100.0)
    predicted = int(contract_months * survival + 12 * survival)
    return max(0, predicted)


def _upsell_multiplier(engagement_trend: float, nps: int) -> float:
    base = 1.0
    if engagement_trend > 0.5 and nps > 30:
        base = 1.30
    elif engagement_trend > 0.0 and nps >= 0:
        base = 1.10
    elif engagement_trend < -0.3 or nps < -20:
        base = 0.80
    return base


def _compute_ltv(s: CustomerSignals, predicted_months: int) -> float:
    mult = _upsell_multiplier(s.engagement_trend, s.nps_score)
    return round(s.avg_monthly_revenue_eur * predicted_months * mult, 2)


def _compute_risk_factors(s: CustomerSignals, breakdown: Dict[str, float]) -> List[str]:
    factors: List[str] = []
    if breakdown["login_recency"] > 50:
        factors.append(f"Inactif depuis {s.days_since_last_login} jours")
    if s.open_support_tickets >= 3:
        factors.append(f"{s.open_support_tickets} tickets support ouverts")
    if s.contract_months_remaining <= 3:
        factors.append(f"Contrat expire dans {s.contract_months_remaining} mois")
    if s.engagement_trend < -0.3:
        factors.append("Tendance d'engagement en déclin")
    if s.nps_score < 0:
        factors.append(f"NPS négatif ({s.nps_score})")
    return factors


def _analyze(s: CustomerSignals) -> RetentionProfile:
    breakdown = _compute_breakdown(s)
    churn_score = _compute_churn_score(breakdown)
    churn_risk = _classify_churn(churn_score)
    predicted_months = _predicted_months(churn_score, s.contract_months_remaining)
    ltv = _compute_ltv(s, predicted_months)
    return RetentionProfile(
        signals=s,
        churn_score=churn_score,
        churn_risk=churn_risk,
        ltv_eur=ltv,
        predicted_months_remaining=predicted_months,
        risk_factors=_compute_risk_factors(s, breakdown),
        retention_actions=_RETENTION_ACTIONS[churn_risk],
        score_breakdown=breakdown,
    )


class CustomerRetention:
    def __init__(self) -> None:
        self._store: Dict[str, RetentionProfile] = {}

    def analyze(self, signals: CustomerSignals) -> RetentionProfile:
        profile = _analyze(signals)
        self._store[signals.customer_id] = profile
        return profile

    def analyze_batch(self, signals_list: List[CustomerSignals]) -> List[RetentionProfile]:
        return [self.analyze(s) for s in signals_list]

    def get(self, customer_id: str) -> Optional[RetentionProfile]:
        return self._store.get(customer_id)

    def all_customers(self) -> List[RetentionProfile]:
        return sorted(self._store.values(), key=lambda p: p.churn_score, reverse=True)

    def at_risk(self) -> List[RetentionProfile]:
        return [p for p in self._store.values()
                if p.churn_risk in (ChurnRisk.HIGH, ChurnRisk.CRITICAL)]

    def by_risk(self, risk: ChurnRisk) -> List[RetentionProfile]:
        return [p for p in self._store.values() if p.churn_risk == risk]

    def top_ltv(self, n: int = 5) -> List[RetentionProfile]:
        return sorted(self._store.values(), key=lambda p: p.ltv_eur, reverse=True)[:n]

    def expiring_soon(self, months: int = 3) -> List[RetentionProfile]:
        return [p for p in self._store.values()
                if p.signals.contract_months_remaining <= months]

    def portfolio_summary(self) -> dict:
        items = list(self._store.values())
        count = len(items)
        if count == 0:
            return {
                "total": 0,
                "risk_counts": {r.value: 0 for r in ChurnRisk},
                "avg_churn_score": 0.0,
                "total_ltv_eur": 0.0,
                "total_monthly_revenue_eur": 0.0,
                "at_risk_revenue_eur": 0.0,
            }
        risk_counts = {r.value: 0 for r in ChurnRisk}
        for p in items:
            risk_counts[p.churn_risk.value] += 1
        at_risk_rev = sum(
            p.signals.avg_monthly_revenue_eur
            for p in items
            if p.churn_risk in (ChurnRisk.HIGH, ChurnRisk.CRITICAL)
        )
        return {
            "total": count,
            "risk_counts": risk_counts,
            "avg_churn_score": round(sum(p.churn_score for p in items) / count, 4),
            "total_ltv_eur": round(sum(p.ltv_eur for p in items), 2),
            "total_monthly_revenue_eur": round(sum(p.signals.avg_monthly_revenue_eur for p in items), 2),
            "at_risk_revenue_eur": round(at_risk_rev, 2),
        }

    def reset(self) -> None:
        self._store.clear()
