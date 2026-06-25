"""
Deal Accelerator — diagnoses stalled deals and generates unblocking strategies.

Composite stall score:
  inactivity_risk(35%) + stakeholder_gap(25%) + competitive_risk(20%) + budget_risk(20%)
  → DealHealth: ACTIVE / AT_RISK / STALLED / CRITICAL / LOST
  → AccelerationStrategy: EXECUTIVE_SPONSOR / REQUALIFY / COMPETITIVE_PLAY / VALUE_PROOF /
                          URGENCY_CREATE / CHAMPION_BUILD / BUDGET_RESHAPE / DIRECT_CLOSE
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple


class DealHealth(str, Enum):
    ACTIVE = "active"
    AT_RISK = "at_risk"
    STALLED = "stalled"
    CRITICAL = "critical"
    LOST = "lost"


class AccelerationStrategy(str, Enum):
    EXECUTIVE_SPONSOR = "executive_sponsor"
    REQUALIFY = "requalify"
    COMPETITIVE_PLAY = "competitive_play"
    VALUE_PROOF = "value_proof"
    URGENCY_CREATE = "urgency_create"
    CHAMPION_BUILD = "champion_build"
    BUDGET_RESHAPE = "budget_reshape"
    DIRECT_CLOSE = "direct_close"


class SalesStage(str, Enum):
    PROSPECTING = "prospecting"
    DISCOVERY = "discovery"
    DEMO = "demo"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSING = "closing"


_STAGE_EXPECTED_DAYS: Dict[SalesStage, int] = {
    SalesStage.PROSPECTING: 14,
    SalesStage.DISCOVERY: 21,
    SalesStage.DEMO: 21,
    SalesStage.PROPOSAL: 30,
    SalesStage.NEGOTIATION: 21,
    SalesStage.CLOSING: 14,
}

_BLOCKERS: Dict[str, str] = {
    "no_activity": "Aucune activité détectée depuis plus de 14 jours — deal inactif",
    "single_threaded": "Contact unique dans le compte — risque élevé si le champion quitte",
    "no_decision_maker": "Décideur final non identifié — impossible de progresser sans lui",
    "budget_not_confirmed": "Budget non confirmé — risque d'abandon en fin de cycle",
    "no_champion": "Aucun champion interne identifié — pas de défenseur du projet côté client",
    "competitive_threat": "Concurrent actif identifié dans le deal — risque de perte élevé",
    "long_cycle": "Cycle de vente anormalement long — signes de désengagement",
    "low_engagement": "Engagement client en baisse — réponses rares, réunions annulées",
    "no_next_step": "Aucune prochaine étape planifiée — deal sans momentum",
    "price_objection": "Objection prix non résolue — bloquant confirmé",
    "technical_hold": "Validation technique en attente — blocage IT/légal/sécurité",
    "executive_misalignment": "Désalignement au niveau direction — pas de sponsorship exécutif",
}

_STRATEGIES: Dict[AccelerationStrategy, str] = {
    AccelerationStrategy.EXECUTIVE_SPONSOR: "Impliquer un exécutif côté vendeur pour créer un lien C-level direct",
    AccelerationStrategy.REQUALIFY: "Requalifier le deal — vérifier BANT complet avant de continuer à investir",
    AccelerationStrategy.COMPETITIVE_PLAY: "Activer une stratégie de différenciation vs concurrent — ROI comparatif, proof of concept",
    AccelerationStrategy.VALUE_PROOF: "Présenter un business case chiffré ou une preuve de valeur (étude de cas, POC, ROI calculator)",
    AccelerationStrategy.URGENCY_CREATE: "Créer un événement de clôture — offre limitée, deadline contractuelle, implémentation avant fin trimestre",
    AccelerationStrategy.CHAMPION_BUILD: "Identifier et activer un champion interne — trouver la personne qui bénéficie le plus du projet",
    AccelerationStrategy.BUDGET_RESHAPE: "Retravailler la proposition financière — phasage, financement, ROI rapide (Quick Win)",
    AccelerationStrategy.DIRECT_CLOSE: "Demander directement la commande — trial close, proposition ferme avec deadline",
}


@dataclass
class DealContext:
    deal_id: str
    deal_name: str
    company: str
    contact_name: str
    stage: SalesStage
    deal_value_eur: float
    days_in_stage: int
    days_since_last_activity: int
    close_date_in_days: int          # days until expected close (negative = overdue)
    # Stakeholder map
    contacts_count: int              # total contacts in deal
    decision_maker_identified: bool
    champion_identified: bool
    executive_sponsor: bool          # have we engaged C-level?
    # Engagement signals
    last_email_response_days: int    # days since last response (-1 = never)
    meetings_last_30d: int
    prospect_initiated_last_30d: int # times prospect reached out to us
    # Competitive landscape
    has_competitor: bool
    competitor_name: Optional[str]
    competitor_strength: float       # 0-100
    # Budget / financial
    budget_confirmed: bool
    price_objection: bool
    technical_hold: bool
    # Risk flags
    rep_notes_concern: bool          # rep flagged this deal as concerning
    next_step_defined: bool

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AccelerationPlan:
    deal: DealContext
    deal_health: DealHealth
    stall_score: float               # 0-100, higher = more stalled
    inactivity_risk: float
    stakeholder_gap: float
    competitive_risk: float
    budget_risk: float
    primary_strategy: AccelerationStrategy
    secondary_strategies: List[AccelerationStrategy]
    active_blockers: List[str]
    action_plan: List[str]
    days_to_act: int                 # recommended action window (0 = immediate)
    win_probability_adj: float       # adjusted win probability 0-100
    deal_momentum: float             # 0-100

    def to_dict(self) -> dict:
        return {
            "deal": self.deal.to_dict(),
            "deal_health": self.deal_health.value,
            "stall_score": self.stall_score,
            "inactivity_risk": self.inactivity_risk,
            "stakeholder_gap": self.stakeholder_gap,
            "competitive_risk": self.competitive_risk,
            "budget_risk": self.budget_risk,
            "primary_strategy": self.primary_strategy.value,
            "secondary_strategies": [s.value for s in self.secondary_strategies],
            "active_blockers": self.active_blockers,
            "action_plan": self.action_plan,
            "days_to_act": self.days_to_act,
            "win_probability_adj": self.win_probability_adj,
            "deal_momentum": self.deal_momentum,
        }


# ─── Dimension scorers ────────────────────────────────────────────────────────

def _inactivity_risk(d: DealContext) -> Tuple[float, List[str]]:
    blockers: List[str] = []

    last_act = d.days_since_last_activity
    if last_act >= 30:
        act_score = 100.0
        blockers.append("no_activity")
    elif last_act >= 14:
        act_score = 70.0 + (last_act - 14) * (30.0 / 16.0)
        blockers.append("no_activity")
    elif last_act >= 7:
        act_score = 30.0 + (last_act - 7) * (40.0 / 7.0)
    else:
        act_score = last_act * (30.0 / 7.0)

    expected = _STAGE_EXPECTED_DAYS.get(d.stage, 21)
    stage_overrun = max(0, d.days_in_stage - expected)
    overrun_score = min(40.0, stage_overrun * 2.0)
    if stage_overrun > 14:
        blockers.append("long_cycle")

    if not d.next_step_defined:
        blockers.append("no_next_step")
        next_step_penalty = 20.0
    else:
        next_step_penalty = 0.0

    engagement = d.prospect_initiated_last_30d * 15.0 + d.meetings_last_30d * 10.0
    engagement_bonus = min(20.0, engagement)
    low_engage = d.meetings_last_30d == 0 and d.last_email_response_days > 14
    if low_engage:
        blockers.append("low_engagement")

    score = act_score * 0.50 + overrun_score + next_step_penalty - engagement_bonus
    return round(min(100.0, max(0.0, score)), 2), blockers


def _stakeholder_gap(d: DealContext) -> Tuple[float, List[str]]:
    blockers: List[str] = []
    score = 0.0

    if d.contacts_count <= 1:
        score += 40.0
        blockers.append("single_threaded")
    elif d.contacts_count <= 2:
        score += 20.0

    if not d.decision_maker_identified:
        score += 30.0
        blockers.append("no_decision_maker")

    if not d.champion_identified:
        score += 20.0
        blockers.append("no_champion")

    if not d.executive_sponsor and d.deal_value_eur >= 50_000:
        score += 15.0
        blockers.append("executive_misalignment")

    return round(min(100.0, score), 2), blockers


def _competitive_risk(d: DealContext) -> Tuple[float, List[str]]:
    blockers: List[str] = []

    if not d.has_competitor:
        return 0.0, blockers

    score = min(100.0, d.competitor_strength)
    if d.competitor_strength >= 40:
        blockers.append("competitive_threat")

    return round(score, 2), blockers


def _budget_risk(d: DealContext) -> Tuple[float, List[str]]:
    blockers: List[str] = []
    score = 0.0

    if not d.budget_confirmed:
        score += 40.0
        blockers.append("budget_not_confirmed")

    if d.price_objection:
        score += 35.0
        blockers.append("price_objection")

    if d.technical_hold:
        score += 25.0
        blockers.append("technical_hold")

    return round(min(100.0, score), 2), blockers


def _deal_health(stall_score: float, close_days: int, d: DealContext) -> DealHealth:
    overdue = close_days < 0
    if stall_score >= 80 or (overdue and stall_score >= 60):
        return DealHealth.CRITICAL
    if stall_score >= 60 or (overdue and stall_score >= 40):
        return DealHealth.STALLED
    if stall_score >= 35 or overdue:
        return DealHealth.AT_RISK
    if stall_score >= 15:
        return DealHealth.ACTIVE
    return DealHealth.ACTIVE


def _select_strategy(
    d: DealContext,
    inactivity: float,
    stakeholder: float,
    competitive: float,
    budget: float,
) -> Tuple[AccelerationStrategy, List[AccelerationStrategy]]:
    scores: Dict[AccelerationStrategy, float] = {
        AccelerationStrategy.EXECUTIVE_SPONSOR: 0.0,
        AccelerationStrategy.REQUALIFY: 0.0,
        AccelerationStrategy.COMPETITIVE_PLAY: 0.0,
        AccelerationStrategy.VALUE_PROOF: 0.0,
        AccelerationStrategy.URGENCY_CREATE: 0.0,
        AccelerationStrategy.CHAMPION_BUILD: 0.0,
        AccelerationStrategy.BUDGET_RESHAPE: 0.0,
        AccelerationStrategy.DIRECT_CLOSE: 0.0,
    }

    if not d.decision_maker_identified or not d.executive_sponsor:
        scores[AccelerationStrategy.EXECUTIVE_SPONSOR] += 30.0
    if not d.champion_identified:
        scores[AccelerationStrategy.CHAMPION_BUILD] += 25.0
    if competitive >= 50:
        scores[AccelerationStrategy.COMPETITIVE_PLAY] += competitive * 0.5
    if d.price_objection or budget >= 60:
        scores[AccelerationStrategy.BUDGET_RESHAPE] += 25.0
    if not d.budget_confirmed:
        scores[AccelerationStrategy.REQUALIFY] += 20.0
    if d.close_date_in_days <= 7 and d.stage in (SalesStage.NEGOTIATION, SalesStage.CLOSING):
        scores[AccelerationStrategy.DIRECT_CLOSE] += 40.0
    if inactivity >= 60:
        scores[AccelerationStrategy.URGENCY_CREATE] += 30.0
    if d.deal_value_eur >= 30_000 and not d.executive_sponsor:
        scores[AccelerationStrategy.VALUE_PROOF] += 20.0

    sorted_strategies = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_strategies[0][0]
    secondary = [s for s, sc in sorted_strategies[1:4] if sc > 0]

    return primary, secondary


def _win_probability(d: DealContext, stall_score: float) -> float:
    stage_base = {
        SalesStage.PROSPECTING: 10.0,
        SalesStage.DISCOVERY: 20.0,
        SalesStage.DEMO: 35.0,
        SalesStage.PROPOSAL: 50.0,
        SalesStage.NEGOTIATION: 65.0,
        SalesStage.CLOSING: 80.0,
    }
    base = stage_base.get(d.stage, 30.0)

    # Adjustments
    if d.decision_maker_identified:
        base += 5.0
    if d.champion_identified:
        base += 8.0
    if d.budget_confirmed:
        base += 7.0
    if d.has_competitor:
        base -= d.competitor_strength * 0.15
    if d.price_objection:
        base -= 10.0
    if not d.next_step_defined:
        base -= 8.0

    stall_penalty = stall_score * 0.30
    return round(min(100.0, max(0.0, base - stall_penalty)), 2)


def _deal_momentum(d: DealContext) -> float:
    score = 50.0
    score += min(20.0, d.prospect_initiated_last_30d * 10.0)
    score += min(20.0, d.meetings_last_30d * 7.0)
    if d.last_email_response_days > 0 and d.last_email_response_days <= 3:
        score += 10.0
    elif d.last_email_response_days > 14:
        score -= 20.0
    if d.next_step_defined:
        score += 10.0
    else:
        score -= 15.0
    if d.days_since_last_activity > 14:
        score -= 20.0
    return round(min(100.0, max(0.0, score)), 2)


def _build_action_plan(
    primary: AccelerationStrategy,
    secondary: List[AccelerationStrategy],
    blockers: List[str],
    d: DealContext,
) -> Tuple[List[str], int]:
    actions: List[str] = [_STRATEGIES[primary]]
    for s in secondary[:2]:
        actions.append(_STRATEGIES[s])

    days_to_act = 0
    if "no_activity" in blockers:
        days_to_act = 0
    elif "no_next_step" in blockers:
        days_to_act = 1
    elif d.close_date_in_days <= 14:
        days_to_act = 0
    else:
        days_to_act = min(3, max(0, d.days_since_last_activity - 7))

    return actions, days_to_act


def _accelerate_deal(d: DealContext) -> AccelerationPlan:
    inact, b1 = _inactivity_risk(d)
    stakeh, b2 = _stakeholder_gap(d)
    comp, b3 = _competitive_risk(d)
    budget, b4 = _budget_risk(d)

    stall_score = round(
        inact * 0.35 + stakeh * 0.25 + comp * 0.20 + budget * 0.20,
        2,
    )

    health = _deal_health(stall_score, d.close_date_in_days, d)
    primary, secondary = _select_strategy(d, inact, stakeh, comp, budget)

    all_blockers = b1 + b2 + b3 + b4
    seen: set = set()
    unique_blockers = [_BLOCKERS[k] for k in all_blockers if k in _BLOCKERS and not (k in seen or seen.add(k))]  # type: ignore[func-returns-value]

    action_plan, days_to_act = _build_action_plan(primary, secondary, all_blockers, d)
    win_prob = _win_probability(d, stall_score)
    momentum = _deal_momentum(d)

    return AccelerationPlan(
        deal=d,
        deal_health=health,
        stall_score=stall_score,
        inactivity_risk=inact,
        stakeholder_gap=stakeh,
        competitive_risk=comp,
        budget_risk=budget,
        primary_strategy=primary,
        secondary_strategies=secondary,
        active_blockers=unique_blockers,
        action_plan=action_plan,
        days_to_act=days_to_act,
        win_probability_adj=win_prob,
        deal_momentum=momentum,
    )


class DealAccelerator:
    def __init__(self) -> None:
        self._store: Dict[str, AccelerationPlan] = {}

    def accelerate(self, deal: DealContext) -> AccelerationPlan:
        plan = _accelerate_deal(deal)
        self._store[deal.deal_id] = plan
        return plan

    def accelerate_batch(self, deals: List[DealContext]) -> List[AccelerationPlan]:
        return [self.accelerate(d) for d in deals]

    def get(self, deal_id: str) -> Optional[AccelerationPlan]:
        return self._store.get(deal_id)

    def all_plans(self) -> List[AccelerationPlan]:
        return sorted(self._store.values(), key=lambda p: p.stall_score, reverse=True)

    def by_health(self, health: DealHealth) -> List[AccelerationPlan]:
        return [p for p in self._store.values() if p.deal_health == health]

    def critical_deals(self) -> List[AccelerationPlan]:
        return self.by_health(DealHealth.CRITICAL)

    def stalled_deals(self) -> List[AccelerationPlan]:
        return [p for p in self._store.values() if p.deal_health in (DealHealth.STALLED, DealHealth.CRITICAL)]

    def by_strategy(self, strategy: AccelerationStrategy) -> List[AccelerationPlan]:
        return [p for p in self._store.values() if p.primary_strategy == strategy]

    def top_at_risk(self, n: int = 5) -> List[AccelerationPlan]:
        return self.all_plans()[:n]

    def pipeline_at_risk_eur(self) -> float:
        return sum(
            p.deal.deal_value_eur
            for p in self._store.values()
            if p.deal_health in (DealHealth.STALLED, DealHealth.CRITICAL, DealHealth.AT_RISK)
        )

    def summary(self) -> dict:
        items = list(self._store.values())
        count = len(items)
        if count == 0:
            return {
                "total": 0,
                "health_counts": {h.value: 0 for h in DealHealth},
                "strategy_counts": {s.value: 0 for s in AccelerationStrategy},
                "avg_stall_score": 0.0,
                "avg_win_probability": 0.0,
                "pipeline_at_risk_eur": 0.0,
                "critical_count": 0,
            }
        health_counts = {h.value: 0 for h in DealHealth}
        strategy_counts = {s.value: 0 for s in AccelerationStrategy}
        for p in items:
            health_counts[p.deal_health.value] += 1
            strategy_counts[p.primary_strategy.value] += 1
        avg_stall = sum(p.stall_score for p in items) / count
        avg_win = sum(p.win_probability_adj for p in items) / count
        at_risk = self.pipeline_at_risk_eur()
        return {
            "total": count,
            "health_counts": health_counts,
            "strategy_counts": strategy_counts,
            "avg_stall_score": round(avg_stall, 2),
            "avg_win_probability": round(avg_win, 2),
            "pipeline_at_risk_eur": round(at_risk, 2),
            "critical_count": health_counts[DealHealth.CRITICAL.value],
        }

    def reset(self) -> None:
        self._store.clear()
