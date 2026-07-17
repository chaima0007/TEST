"""
Lead Prioritizer — ranks sales leads by urgency across 6 dimensions:
  recency(20%) + responsiveness(25%) + deal_value(20%) + engagement(15%)
  + activity(10%) + pipeline_health(10%) → priority_score 0-100
  → LeadPriority: HOT / WARM / COLD / DORMANT (thresholds: 70 / 50 / 30)
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional


class LeadPriority(str, Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"
    DORMANT = "dormant"


@dataclass
class LeadSignals:
    lead_id: str
    name: str
    company: str
    sector: str
    days_since_last_contact: int
    response_rate: float        # 0.0 – 1.0
    deal_value_eur: float
    days_in_pipeline: int
    open_rate: float            # 0.0 – 1.0
    meetings_completed: int
    proposal_sent: bool

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PrioritizedLead:
    signals: LeadSignals
    priority_score: float
    priority_tier: LeadPriority
    score_breakdown: Dict[str, float]
    action_items: List[str]
    risk_flags: List[str]

    def to_dict(self) -> dict:
        return {
            "signals": self.signals.to_dict(),
            "priority_score": self.priority_score,
            "priority_tier": self.priority_tier.value,
            "score_breakdown": self.score_breakdown,
            "action_items": self.action_items,
            "risk_flags": self.risk_flags,
        }


_WEIGHTS = {
    "recency": 0.20,
    "responsiveness": 0.25,
    "deal_value": 0.20,
    "engagement": 0.15,
    "activity": 0.10,
    "pipeline_health": 0.10,
}

_ACTION_ITEMS: Dict[LeadPriority, List[str]] = {
    LeadPriority.HOT: [
        "Appeler dans les 24h",
        "Proposer une date de signature",
        "Préparer les documents contractuels",
    ],
    LeadPriority.WARM: [
        "Relancer par email cette semaine",
        "Planifier une démo ou un appel de qualification",
        "Envoyer un cas client similaire",
    ],
    LeadPriority.COLD: [
        "Séquence de réactivation automatique",
        "Requalifier les besoins",
        "Ajuster le positionnement tarifaire si nécessaire",
    ],
    LeadPriority.DORMANT: [
        "Email breakup — fermer ou archiver",
        "Vérifier si le contact a changé de poste",
        "Remettre en liste froide pour 90 jours",
    ],
}


def _recency_score(days: int) -> float:
    if days <= 3:
        return 100.0
    if days <= 7:
        return 85.0
    penalty = (days - 7) * 3.0
    return max(0.0, 85.0 - penalty)


def _value_score(value_eur: float) -> float:
    return min(100.0, value_eur / 20.0)


def _activity_score(meetings: int) -> float:
    return min(100.0, meetings * 20.0)


def _pipeline_health_score(days_in_pipeline: int, proposal_sent: bool) -> float:
    base = 100.0 if proposal_sent else 70.0
    if days_in_pipeline > 30:
        penalty = (days_in_pipeline - 30) * 2.0
        base = max(0.0, base - penalty)
    return base


def _compute_breakdown(signals: LeadSignals) -> Dict[str, float]:
    return {
        "recency": _recency_score(signals.days_since_last_contact),
        "responsiveness": signals.response_rate * 100.0,
        "deal_value": _value_score(signals.deal_value_eur),
        "engagement": signals.open_rate * 100.0,
        "activity": _activity_score(signals.meetings_completed),
        "pipeline_health": _pipeline_health_score(
            signals.days_in_pipeline, signals.proposal_sent
        ),
    }


def _compute_priority_score(breakdown: Dict[str, float]) -> float:
    raw = sum(breakdown[k] * w for k, w in _WEIGHTS.items())
    return round(max(0.0, min(100.0, raw)), 4)


def _classify_priority(score: float) -> LeadPriority:
    if score >= 70:
        return LeadPriority.HOT
    if score >= 50:
        return LeadPriority.WARM
    if score >= 30:
        return LeadPriority.COLD
    return LeadPriority.DORMANT


def _compute_risk_flags(signals: LeadSignals, breakdown: Dict[str, float]) -> List[str]:
    flags: List[str] = []
    if signals.days_since_last_contact > 14:
        flags.append(f"Pas de contact depuis {signals.days_since_last_contact} jours")
    if signals.response_rate < 0.20:
        flags.append("Taux de réponse très faible (< 20%)")
    if signals.days_in_pipeline > 45:
        flags.append(f"En pipeline depuis {signals.days_in_pipeline} jours — risque de stagnation")
    if not signals.proposal_sent and signals.days_in_pipeline > 20:
        flags.append("Aucun devis envoyé après 20 jours")
    if signals.open_rate < 0.15:
        flags.append("Faible taux d'ouverture des emails")
    return flags


def _prioritize(signals: LeadSignals) -> PrioritizedLead:
    breakdown = _compute_breakdown(signals)
    score = _compute_priority_score(breakdown)
    tier = _classify_priority(score)
    return PrioritizedLead(
        signals=signals,
        priority_score=score,
        priority_tier=tier,
        score_breakdown=breakdown,
        action_items=_ACTION_ITEMS[tier],
        risk_flags=_compute_risk_flags(signals, breakdown),
    )


class LeadPrioritizer:
    def __init__(self) -> None:
        self._store: Dict[str, PrioritizedLead] = {}

    def add_lead(self, signals: LeadSignals) -> PrioritizedLead:
        result = _prioritize(signals)
        self._store[signals.lead_id] = result
        return result

    def get(self, lead_id: str) -> Optional[PrioritizedLead]:
        return self._store.get(lead_id)

    def all_leads(self) -> List[PrioritizedLead]:
        return sorted(
            self._store.values(),
            key=lambda p: p.priority_score,
            reverse=True,
        )

    def hot_leads(self) -> List[PrioritizedLead]:
        return [p for p in self._store.values() if p.priority_tier == LeadPriority.HOT]

    def by_tier(self, tier: LeadPriority) -> List[PrioritizedLead]:
        return [p for p in self._store.values() if p.priority_tier == tier]

    def stale_leads(self, threshold: int = 30) -> List[PrioritizedLead]:
        return [
            p for p in self._store.values()
            if p.signals.days_in_pipeline >= threshold
        ]

    def at_risk(self) -> List[PrioritizedLead]:
        return [p for p in self._store.values() if len(p.risk_flags) > 0]

    def sector_stats(self, sector: str) -> dict:
        items = [p for p in self._store.values() if p.signals.sector == sector]
        count = len(items)
        avg_score = sum(p.priority_score for p in items) / count if count else 0.0
        hot_count = sum(1 for p in items if p.priority_tier == LeadPriority.HOT)
        total_value = sum(p.signals.deal_value_eur for p in items)
        return {
            "sector": sector,
            "count": count,
            "avg_priority_score": round(avg_score, 4),
            "hot_count": hot_count,
            "total_deal_value_eur": round(total_value, 2),
        }

    def summary(self) -> dict:
        items = list(self._store.values())
        count = len(items)
        if count == 0:
            return {"total": 0, "tier_counts": {t.value: 0 for t in LeadPriority},
                    "avg_score": 0.0, "total_pipeline_value": 0.0, "at_risk_count": 0}
        tier_counts = {t.value: 0 for t in LeadPriority}
        for p in items:
            tier_counts[p.priority_tier.value] += 1
        return {
            "total": count,
            "tier_counts": tier_counts,
            "avg_score": round(sum(p.priority_score for p in items) / count, 4),
            "total_pipeline_value": round(sum(p.signals.deal_value_eur for p in items), 2),
            "at_risk_count": sum(1 for p in items if p.risk_flags),
        }

    def reset(self) -> None:
        self._store.clear()
