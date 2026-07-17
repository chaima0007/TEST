from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class HealthTier(str, Enum):
    CHAMPION = "champion"
    HEALTHY = "healthy"
    AT_RISK = "at_risk"
    CRITICAL = "critical"


class HealthAction(str, Enum):
    CELEBRATE = "celebrate"
    MAINTAIN = "maintain"
    INTERVENE = "intervene"
    ESCALATE = "escalate"


class ChurnRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    IMMINENT = "imminent"


class ExpansionPotential(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    LIMITED = "limited"
    NONE = "none"


@dataclass
class AccountHealthInput:
    account_id: str
    account_name: str
    arr_eur: float
    segment: str  # enterprise / mid_market / smb
    # Product usage
    dau_mau_ratio: float            # 0-1, daily/monthly active user ratio
    feature_adoption_pct: float     # 0-100
    integrations_active: int        # count of active integrations
    # Support & satisfaction
    nps_score: int                  # -100 to 100
    support_tickets_last_90d: int
    critical_tickets_open: int
    # Commercial signals
    contract_months_remaining: int
    expansion_discussions: bool
    last_qbr_days_ago: int         # days since last QBR
    # Relationship
    executive_sponsor_engaged: bool
    champion_score: int             # 0-10
    stakeholders_active: int
    # Billing
    payment_on_time: bool
    invoices_overdue: int


@dataclass
class AccountHealthResult:
    account_id: str
    account_name: str
    arr_eur: float
    segment: str
    health_score: float
    health_tier: HealthTier
    health_action: HealthAction
    churn_risk: ChurnRisk
    expansion_potential: ExpansionPotential
    health_drivers: list[str]
    risk_signals: list[str]
    recommended_plays: list[str]
    renewal_probability_pct: float

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "account_name": self.account_name,
            "arr_eur": self.arr_eur,
            "segment": self.segment,
            "health_score": self.health_score,
            "health_tier": self.health_tier.value,
            "health_action": self.health_action.value,
            "churn_risk": self.churn_risk.value,
            "expansion_potential": self.expansion_potential.value,
            "health_drivers": self.health_drivers,
            "risk_signals": self.risk_signals,
            "recommended_plays": self.recommended_plays,
            "renewal_probability_pct": self.renewal_probability_pct,
        }


def _usage_score(inp: AccountHealthInput) -> float:
    """Max 35 pts — product engagement signals."""
    score = 0.0
    # DAU/MAU ratio: 0-15 pts
    score += min(15.0, inp.dau_mau_ratio * 15.0 / 0.4)
    # Feature adoption: 0-12 pts
    score += min(12.0, inp.feature_adoption_pct * 12.0 / 60.0)
    # Integrations: 0-8 pts (2 pts each, max 4)
    score += min(8.0, inp.integrations_active * 2.0)
    return min(35.0, score)


def _satisfaction_score(inp: AccountHealthInput) -> float:
    """Max 25 pts — NPS, tickets, support quality."""
    score = 0.0
    # NPS: -100 to 100 → 0-15 pts
    nps_norm = (inp.nps_score + 100) / 200.0  # 0-1
    score += nps_norm * 15.0
    # Support tickets burden (fewer = better): 0-6 pts
    if inp.support_tickets_last_90d <= 2:
        score += 6.0
    elif inp.support_tickets_last_90d <= 5:
        score += 4.0
    elif inp.support_tickets_last_90d <= 10:
        score += 2.0
    # No critical open tickets: 0-4 pts
    if inp.critical_tickets_open == 0:
        score += 4.0
    elif inp.critical_tickets_open == 1:
        score += 2.0
    return min(25.0, score)


def _relationship_score(inp: AccountHealthInput) -> float:
    """Max 25 pts — exec engagement, champion, QBR cadence."""
    score = 0.0
    # Executive sponsor: 8 pts
    if inp.executive_sponsor_engaged:
        score += 8.0
    # Champion score (0-10 → 0-9 pts)
    score += inp.champion_score * 0.9
    # Stakeholders active: 0-5 pts
    score += min(5.0, inp.stakeholders_active * 1.5)
    # QBR recency: 0-3 pts
    if inp.last_qbr_days_ago <= 30:
        score += 3.0
    elif inp.last_qbr_days_ago <= 60:
        score += 1.5
    return min(25.0, score)


def _commercial_score(inp: AccountHealthInput) -> float:
    """Max 15 pts — billing health, contract horizon, expansion signals."""
    score = 0.0
    # Payment on time: 5 pts
    if inp.payment_on_time:
        score += 5.0
    # No overdue invoices: 0-3 pts
    if inp.invoices_overdue == 0:
        score += 3.0
    elif inp.invoices_overdue == 1:
        score += 1.0
    # Contract months remaining (≥6 = good): 0-4 pts
    if inp.contract_months_remaining >= 6:
        score += 4.0
    elif inp.contract_months_remaining >= 3:
        score += 2.0
    # Expansion discussions: 3 pts
    if inp.expansion_discussions:
        score += 3.0
    return min(15.0, score)


def _health_score(inp: AccountHealthInput) -> float:
    total = (
        _usage_score(inp)
        + _satisfaction_score(inp)
        + _relationship_score(inp)
        + _commercial_score(inp)
    )
    return round(min(100.0, max(0.0, total)), 1)


def _health_tier(score: float) -> HealthTier:
    if score >= 80:
        return HealthTier.CHAMPION
    if score >= 60:
        return HealthTier.HEALTHY
    if score >= 35:
        return HealthTier.AT_RISK
    return HealthTier.CRITICAL


def _churn_risk(score: float, inp: AccountHealthInput) -> ChurnRisk:
    if score < 35 or inp.critical_tickets_open >= 2 or inp.invoices_overdue >= 2:
        return ChurnRisk.IMMINENT
    if score < 60 or (inp.contract_months_remaining <= 3 and score < 70):
        return ChurnRisk.HIGH
    if score < 75 or inp.nps_score < 0:
        return ChurnRisk.MEDIUM
    return ChurnRisk.LOW


def _expansion_potential(score: float, inp: AccountHealthInput) -> ExpansionPotential:
    if score >= 75 and inp.expansion_discussions and inp.champion_score >= 7:
        return ExpansionPotential.STRONG
    if score >= 60 and (inp.expansion_discussions or inp.champion_score >= 6):
        return ExpansionPotential.MODERATE
    if score >= 45:
        return ExpansionPotential.LIMITED
    return ExpansionPotential.NONE


def _health_action(tier: HealthTier, churn: ChurnRisk) -> HealthAction:
    if tier == HealthTier.CHAMPION:
        return HealthAction.CELEBRATE
    if tier == HealthTier.HEALTHY:
        return HealthAction.MAINTAIN
    if tier == HealthTier.AT_RISK or churn == ChurnRisk.HIGH:
        return HealthAction.INTERVENE
    return HealthAction.ESCALATE


def _renewal_probability(score: float, inp: AccountHealthInput) -> float:
    base = score * 0.85
    if inp.contract_months_remaining <= 2:
        base -= 10.0
    if inp.invoices_overdue >= 2:
        base -= 8.0
    if inp.nps_score < -20:
        base -= 5.0
    if inp.executive_sponsor_engaged:
        base += 5.0
    if inp.expansion_discussions:
        base += 3.0
    return round(min(100.0, max(0.0, base)), 1)


def _health_drivers(inp: AccountHealthInput, score: float) -> list[str]:
    drivers: list[str] = []
    if inp.dau_mau_ratio >= 0.3:
        drivers.append(f"Engagement produit fort — DAU/MAU {inp.dau_mau_ratio:.0%}")
    if inp.feature_adoption_pct >= 50:
        drivers.append(f"Adoption features élevée — {inp.feature_adoption_pct:.0f}% des features actives")
    if inp.nps_score >= 30:
        drivers.append(f"NPS excellent ({inp.nps_score}) — compte promoteur actif")
    if inp.executive_sponsor_engaged:
        drivers.append("Sponsor exécutif engagé — décision de renouvellement facilitée")
    if inp.champion_score >= 7:
        drivers.append(f"Champion fort ({inp.champion_score}/10) — défenseur interne actif")
    if inp.expansion_discussions:
        drivers.append("Discussions expansion en cours — signal d'upsell positif")
    if inp.integrations_active >= 3:
        drivers.append(f"{inp.integrations_active} intégrations actives — fort ancrage technique")
    if inp.payment_on_time and inp.invoices_overdue == 0:
        drivers.append("Historique de paiement parfait — compte fiable")
    return drivers


def _risk_signals(inp: AccountHealthInput, score: float) -> list[str]:
    signals: list[str] = []
    if inp.dau_mau_ratio < 0.2:
        signals.append(f"Engagement produit faible — DAU/MAU {inp.dau_mau_ratio:.0%} sous le seuil")
    if inp.feature_adoption_pct < 30:
        signals.append(f"Adoption features insuffisante — {inp.feature_adoption_pct:.0f}% seulement")
    if inp.nps_score < 0:
        signals.append(f"NPS négatif ({inp.nps_score}) — risque de churn élevé")
    if inp.critical_tickets_open >= 1:
        signals.append(f"{inp.critical_tickets_open} ticket(s) critique(s) ouvert(s) — blocage produit")
    if inp.contract_months_remaining <= 3:
        signals.append(f"Renouvellement dans {inp.contract_months_remaining} mois — fenêtre de risque")
    if inp.last_qbr_days_ago > 90:
        signals.append(f"Dernier QBR il y a {inp.last_qbr_days_ago}j — relation négligée")
    if not inp.executive_sponsor_engaged:
        signals.append("Aucun sponsor exécutif — vulnérabilité organisationnelle")
    if inp.invoices_overdue >= 1:
        signals.append(f"{inp.invoices_overdue} facture(s) en retard — signal financier préoccupant")
    if inp.champion_score <= 4:
        signals.append(f"Champion faible ({inp.champion_score}/10) — risque si changement de contact")
    return signals


def _recommended_plays(
    tier: HealthTier, churn: ChurnRisk, expansion: ExpansionPotential, inp: AccountHealthInput
) -> list[str]:
    plays: list[str] = []
    if tier == HealthTier.CHAMPION:
        plays.append("Programme référence client — case study ou témoignage")
        plays.append("Présenter la roadmap produit en avant-première — renforcer la fidélité")
        if expansion == ExpansionPotential.STRONG:
            plays.append("Initier une conversation upsell/cross-sell formelle")
    elif tier == HealthTier.HEALTHY:
        plays.append("QBR prochain trimestre — maintenir l'alignement stratégique")
        plays.append("Identifier des opportunités d'adoption features non utilisées")
        if expansion != ExpansionPotential.NONE:
            plays.append("Explorer les besoins additionnels — potentiel expansion identifié")
    elif tier == HealthTier.AT_RISK:
        plays.append("Appel de revue urgente — identifier les frictions et blocages")
        plays.append("Escalade interne — impliquer le management dans la relation")
        if inp.critical_tickets_open >= 1:
            plays.append("Résoudre les tickets critiques en priorité absolue — unlocker le compte")
        if inp.dau_mau_ratio < 0.2:
            plays.append("Session d'activation produit — former les utilisateurs inactifs")
    else:
        plays.append("Escalade C-level immédiate — mobiliser direction pour sauver le compte")
        plays.append("Plan de récupération 30j — objectifs mesurables et responsables définis")
        plays.append("Executive Business Review d'urgence — valeur démontrée, roadmap personnalisée")
        if inp.invoices_overdue >= 1:
            plays.append("Résoudre les impayés en priorité — éviter la suspension de service")
    return plays


class AccountHealthScorerEngine:
    def __init__(self) -> None:
        self._results: dict[str, AccountHealthResult] = {}

    def score(self, inp: AccountHealthInput) -> AccountHealthResult:
        hs = _health_score(inp)
        tier = _health_tier(hs)
        churn = _churn_risk(hs, inp)
        expansion = _expansion_potential(hs, inp)
        action = _health_action(tier, churn)
        result = AccountHealthResult(
            account_id=inp.account_id,
            account_name=inp.account_name,
            arr_eur=inp.arr_eur,
            segment=inp.segment,
            health_score=hs,
            health_tier=tier,
            health_action=action,
            churn_risk=churn,
            expansion_potential=expansion,
            health_drivers=_health_drivers(inp, hs),
            risk_signals=_risk_signals(inp, hs),
            recommended_plays=_recommended_plays(tier, churn, expansion, inp),
            renewal_probability_pct=_renewal_probability(hs, inp),
        )
        self._results[inp.account_id] = result
        return result

    def score_batch(self, accounts: list[AccountHealthInput]) -> list[AccountHealthResult]:
        results = [self.score(a) for a in accounts]
        return sorted(results, key=lambda r: r.health_score, reverse=True)

    def all_accounts(self) -> list[AccountHealthResult]:
        return sorted(self._results.values(), key=lambda r: r.health_score, reverse=True)

    def by_tier(self, tier: HealthTier) -> list[AccountHealthResult]:
        return [r for r in self._results.values() if r.health_tier == tier]

    def by_action(self, action: HealthAction) -> list[AccountHealthResult]:
        return [r for r in self._results.values() if r.health_action == action]

    def by_churn_risk(self, risk: ChurnRisk) -> list[AccountHealthResult]:
        return [r for r in self._results.values() if r.churn_risk == risk]

    def champions(self) -> list[AccountHealthResult]:
        return self.by_tier(HealthTier.CHAMPION)

    def critical_accounts(self) -> list[AccountHealthResult]:
        return self.by_tier(HealthTier.CRITICAL)

    def needs_escalation(self) -> list[AccountHealthResult]:
        return self.by_action(HealthAction.ESCALATE)

    def at_risk_accounts(self) -> list[AccountHealthResult]:
        return [
            r for r in self._results.values()
            if r.health_tier in (HealthTier.AT_RISK, HealthTier.CRITICAL)
        ]

    def expansion_ready(self) -> list[AccountHealthResult]:
        return [
            r for r in self._results.values()
            if r.expansion_potential in (ExpansionPotential.STRONG, ExpansionPotential.MODERATE)
        ]

    def avg_health_score(self) -> float:
        if not self._results:
            return 0.0
        scores = [r.health_score for r in self._results.values()]
        return round(sum(scores) / len(scores), 1)

    def total_arr_at_risk_eur(self) -> float:
        return sum(
            r.arr_eur for r in self._results.values()
            if r.health_tier in (HealthTier.AT_RISK, HealthTier.CRITICAL)
        )

    def summary(self) -> dict:
        all_r = list(self._results.values())
        n = len(all_r)
        return {
            "total": n,
            "tier_counts": {t.value: sum(1 for r in all_r if r.health_tier == t) for t in HealthTier},
            "action_counts": {a.value: sum(1 for r in all_r if r.health_action == a) for a in HealthAction},
            "churn_counts": {c.value: sum(1 for r in all_r if r.churn_risk == c) for c in ChurnRisk},
            "avg_health_score": self.avg_health_score(),
            "champion_count": len(self.champions()),
            "critical_count": len(self.critical_accounts()),
            "total_arr_at_risk_eur": self.total_arr_at_risk_eur(),
        }

    def reset(self) -> None:
        self._results.clear()
