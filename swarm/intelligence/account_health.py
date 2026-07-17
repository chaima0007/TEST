"""
Account Health Monitor — tracks customer health to predict churn and expansion opportunities.

Composite health scoring:
  engagement(30%) + product_adoption(25%) + financial_health(25%) + relationship(20%)
  → HealthTier: CHAMPION / HEALTHY / NEUTRAL / AT_RISK / CHURNING
  → AccountAction: EXPAND / NURTURE / STABILIZE / SAVE / OFFBOARD
"""

from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple


class HealthTier(str, Enum):
    CHAMPION = "champion"
    HEALTHY = "healthy"
    NEUTRAL = "neutral"
    AT_RISK = "at_risk"
    CHURNING = "churning"


class AccountAction(str, Enum):
    EXPAND = "expand"
    NURTURE = "nurture"
    STABILIZE = "stabilize"
    SAVE = "save"
    OFFBOARD = "offboard"


class ContractType(str, Enum):
    MONTHLY = "monthly"
    ANNUAL = "annual"
    MULTI_YEAR = "multi_year"


_HEALTH_SIGNALS: Dict[str, str] = {
    "high_engagement": "Engagement élevé — utilisation active et régulière de la plateforme",
    "low_engagement": "Faible engagement — risque d'attrition si non adressé rapidement",
    "strong_adoption": "Adoption produit forte — plusieurs fonctionnalités clés utilisées",
    "low_adoption": "Adoption produit insuffisante — ROI perçu probablement faible",
    "on_time_payments": "Historique de paiement excellent — client financièrement sain",
    "payment_issues": "Problèmes de paiement détectés — risque financier à surveiller",
    "strong_relationship": "Relation client solide — contacts multiples, satisfaction élevée",
    "weak_relationship": "Relation client fragile — risque de départ si champion quitte",
    "expansion_ready": "Compte prêt pour l'expansion — signaux d'usage et de croissance positifs",
    "upsell_opportunity": "Opportunité d'upsell identifiée — usage proche des limites",
    "renewal_at_risk": "Renouvellement à risque — contrat expirant avec signaux négatifs",
    "nps_detractor": "NPS détracteur — risque fort de churn et de bouche-à-oreille négatif",
    "nps_promoter": "NPS promoteur — excellent potentiel de recommandation et d'expansion",
    "support_overload": "Surcharge support — trop de tickets ouverts, satisfaction en baisse",
    "power_user": "Power users identifiés — excellent signe d'adoption profonde",
}

_ACTIONS: Dict[AccountAction, str] = {
    AccountAction.EXPAND: "Planifier un business review pour présenter les opportunités d'expansion",
    AccountAction.NURTURE: "Lancer une séquence de nurture ciblée — formation, contenu, check-ins réguliers",
    AccountAction.STABILIZE: "Initier un plan de succès client personnalisé pour améliorer l'adoption",
    AccountAction.SAVE: "Escalader en urgence — QBR de sauvetage, mobilisation du management, offre de rétention",
    AccountAction.OFFBOARD: "Préparer un offboarding professionnel — récupérer les apprentissages et maintenir la relation",
}


@dataclass
class AccountMetrics:
    account_id: str
    account_name: str
    industry: str
    contract_type: ContractType
    arr_eur: float                    # Annual Recurring Revenue
    contract_start_date: str          # ISO date
    days_until_renewal: int           # negative = overdue
    # Engagement metrics
    dau_wau_ratio: float              # 0-1 (daily/weekly active users ratio)
    feature_adoption_pct: float       # 0-100 % of key features used
    logins_last_30d: int
    api_calls_last_30d: int
    # Product signals
    features_used: int
    total_features: int
    integrations_active: int
    users_active: int
    users_licensed: int
    # Financial health
    payments_on_time_pct: float       # 0-100
    overdue_invoices: int
    expansion_revenue_eur: float      # upsells/cross-sells this year
    # Relationship
    nps_score: int                    # -100 to 100 (NPS), -999 = not collected
    support_tickets_open: int
    support_tickets_30d: int
    executive_contacts: int           # C-level contacts in account
    last_qbr_days: int                # days since last QBR
    csm_sentiment: float              # 0-100 CSM's subjective health rating
    # Usage limits
    usage_pct_of_limit: float         # 0-100+ (>100 = over limit)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AccountHealth:
    account: AccountMetrics
    health_tier: HealthTier
    health_score: float               # 0-100
    engagement_score: float
    adoption_score: float
    financial_score: float
    relationship_score: float
    churn_risk_pct: float             # 0-100
    expansion_potential_eur: float
    primary_action: AccountAction
    health_signals: List[str]
    risk_signals: List[str]
    renewal_forecast: str             # "confident" | "uncertain" | "at_risk"

    def to_dict(self) -> dict:
        return {
            "account": self.account.to_dict(),
            "health_tier": self.health_tier.value,
            "health_score": self.health_score,
            "engagement_score": self.engagement_score,
            "adoption_score": self.adoption_score,
            "financial_score": self.financial_score,
            "relationship_score": self.relationship_score,
            "churn_risk_pct": self.churn_risk_pct,
            "expansion_potential_eur": self.expansion_potential_eur,
            "primary_action": self.primary_action.value,
            "health_signals": self.health_signals,
            "risk_signals": self.risk_signals,
            "renewal_forecast": self.renewal_forecast,
        }


# ─── Dimension scorers ────────────────────────────────────────────────────────

def _engagement(a: AccountMetrics) -> Tuple[float, List[str], List[str]]:
    good: List[str] = []
    bad: List[str] = []

    dau_score = min(100.0, a.dau_wau_ratio * 200.0)   # 0.5 ratio = 100 pts
    login_score = min(100.0, a.logins_last_30d / 20.0 * 100.0)  # 20 logins = 100
    api_score = min(100.0, math.log10(max(1, a.api_calls_last_30d)) / 4.0 * 100.0)  # 10k calls = 100

    if a.dau_wau_ratio >= 0.35:
        good.append("high_engagement")
    elif a.dau_wau_ratio < 0.10:
        bad.append("low_engagement")

    score = dau_score * 0.45 + login_score * 0.30 + api_score * 0.25
    return round(score, 2), good, bad


def _adoption(a: AccountMetrics) -> Tuple[float, List[str], List[str]]:
    good: List[str] = []
    bad: List[str] = []

    feature_score = min(100.0, a.feature_adoption_pct)

    user_ratio = (a.users_active / a.users_licensed * 100.0) if a.users_licensed > 0 else 0.0
    user_score = min(100.0, user_ratio)

    integration_score = min(100.0, a.integrations_active * 25.0)  # 4 integrations = 100

    if a.feature_adoption_pct >= 70:
        good.append("strong_adoption")
        if a.users_active >= 5:
            good.append("power_user")
    elif a.feature_adoption_pct < 35:
        bad.append("low_adoption")

    if a.usage_pct_of_limit >= 80:
        good.append("upsell_opportunity")

    score = feature_score * 0.45 + user_score * 0.35 + integration_score * 0.20
    return round(score, 2), good, bad


def _financial(a: AccountMetrics) -> Tuple[float, List[str], List[str]]:
    good: List[str] = []
    bad: List[str] = []

    payment_score = a.payments_on_time_pct
    overdue_penalty = min(40.0, a.overdue_invoices * 15.0)

    if a.payments_on_time_pct >= 95 and a.overdue_invoices == 0:
        good.append("on_time_payments")
    if a.overdue_invoices >= 2:
        bad.append("payment_issues")

    expansion_score = min(30.0, (a.expansion_revenue_eur / a.arr_eur * 100.0) * 0.60) if a.arr_eur > 0 else 0.0

    score = payment_score * 0.60 + expansion_score + (30.0 - overdue_penalty) * 0.40
    return round(min(100.0, max(0.0, score)), 2), good, bad


def _relationship(a: AccountMetrics) -> Tuple[float, List[str], List[str]]:
    good: List[str] = []
    bad: List[str] = []

    nps_score = 0.0
    if a.nps_score != -999:
        nps_score = min(100.0, (a.nps_score + 100.0) / 2.0)
        if a.nps_score <= -20:
            bad.append("nps_detractor")
        elif a.nps_score >= 50:
            good.append("nps_promoter")
    else:
        nps_score = 50.0  # unknown = neutral

    support_penalty = min(30.0, a.support_tickets_open * 10.0 + a.support_tickets_30d * 2.0)
    if a.support_tickets_open >= 3:
        bad.append("support_overload")

    exec_bonus = min(20.0, a.executive_contacts * 7.0)
    qbr_score = 100.0 if a.last_qbr_days <= 90 else max(0.0, 100.0 - (a.last_qbr_days - 90) * 1.0)

    sentiment_score = a.csm_sentiment

    if exec_bonus >= 14 and nps_score >= 60:
        good.append("strong_relationship")
    elif exec_bonus == 0 and nps_score < 50:
        bad.append("weak_relationship")

    score = (nps_score + sentiment_score) / 2.0 * 0.45 + (100.0 - support_penalty) * 0.25 + exec_bonus * (100.0 / 20.0) * 0.15 + qbr_score * 0.15
    return round(min(100.0, max(0.0, score)), 2), good, bad


def _health_tier(score: float) -> HealthTier:
    if score >= 80:
        return HealthTier.CHAMPION
    if score >= 65:
        return HealthTier.HEALTHY
    if score >= 45:
        return HealthTier.NEUTRAL
    if score >= 25:
        return HealthTier.AT_RISK
    return HealthTier.CHURNING


def _churn_risk(health_score: float, days_renewal: int, overdue: int, nps: int) -> float:
    base_risk = 100.0 - health_score
    if days_renewal <= 30 and health_score < 50:
        base_risk = min(100.0, base_risk + 20.0)
    if overdue >= 2:
        base_risk = min(100.0, base_risk + 15.0)
    if nps != -999 and nps <= -30:
        base_risk = min(100.0, base_risk + 10.0)
    return round(base_risk, 2)


def _expansion_potential(a: AccountMetrics, health_score: float) -> float:
    if health_score < 50:
        return 0.0
    base = a.arr_eur * (health_score / 100.0) * 0.30
    usage_boost = 1.5 if a.usage_pct_of_limit >= 80 else 1.0
    return round(base * usage_boost, 2)


def _primary_action(tier: HealthTier, days_renewal: int, expansion: float) -> AccountAction:
    if tier == HealthTier.CHURNING:
        return AccountAction.SAVE if days_renewal > 0 else AccountAction.OFFBOARD
    if tier == HealthTier.AT_RISK:
        return AccountAction.SAVE
    if tier == HealthTier.NEUTRAL:
        return AccountAction.STABILIZE
    if tier == HealthTier.HEALTHY:
        return AccountAction.EXPAND if expansion > 0 else AccountAction.NURTURE
    return AccountAction.EXPAND  # CHAMPION


def _renewal_forecast(score: float, days: int) -> str:
    if score >= 70:
        return "confident"
    if score >= 45 or days > 90:
        return "uncertain"
    return "at_risk"


def _additional_signals(a: AccountMetrics, health_score: float) -> List[str]:
    extra: List[str] = []
    if health_score >= 75 and a.usage_pct_of_limit >= 60:
        extra.append("expansion_ready")
    if a.days_until_renewal <= 60 and health_score < 60:
        extra.append("renewal_at_risk")
    return extra


def _assess_account(a: AccountMetrics) -> AccountHealth:
    eng_score, eng_good, eng_bad = _engagement(a)
    adp_score, adp_good, adp_bad = _adoption(a)
    fin_score, fin_good, fin_bad = _financial(a)
    rel_score, rel_good, rel_bad = _relationship(a)

    health_score = round(
        eng_score * 0.30
        + adp_score * 0.25
        + fin_score * 0.25
        + rel_score * 0.20,
        2,
    )

    tier = _health_tier(health_score)
    churn = _churn_risk(health_score, a.days_until_renewal, a.overdue_invoices, a.nps_score)
    expansion = _expansion_potential(a, health_score)
    action = _primary_action(tier, a.days_until_renewal, expansion)
    renewal = _renewal_forecast(health_score, a.days_until_renewal)

    all_good = eng_good + adp_good + fin_good + rel_good + _additional_signals(a, health_score)
    all_bad = eng_bad + adp_bad + fin_bad + rel_bad

    seen: set = set()
    unique_good = [_HEALTH_SIGNALS[k] for k in all_good if k in _HEALTH_SIGNALS and not (k in seen or seen.add(k))]  # type: ignore[func-returns-value]
    seen2: set = set()
    unique_bad = [_HEALTH_SIGNALS[k] for k in all_bad if k in _HEALTH_SIGNALS and not (k in seen2 or seen2.add(k))]  # type: ignore[func-returns-value]

    return AccountHealth(
        account=a,
        health_tier=tier,
        health_score=health_score,
        engagement_score=eng_score,
        adoption_score=adp_score,
        financial_score=fin_score,
        relationship_score=rel_score,
        churn_risk_pct=churn,
        expansion_potential_eur=expansion,
        primary_action=action,
        health_signals=unique_good,
        risk_signals=unique_bad,
        renewal_forecast=renewal,
    )


class AccountHealthMonitor:
    def __init__(self) -> None:
        self._store: Dict[str, AccountHealth] = {}

    def assess(self, account: AccountMetrics) -> AccountHealth:
        result = _assess_account(account)
        self._store[account.account_id] = result
        return result

    def assess_batch(self, accounts: List[AccountMetrics]) -> List[AccountHealth]:
        return [self.assess(a) for a in accounts]

    def get(self, account_id: str) -> Optional[AccountHealth]:
        return self._store.get(account_id)

    def all_accounts(self) -> List[AccountHealth]:
        return sorted(self._store.values(), key=lambda h: h.health_score, reverse=True)

    def by_tier(self, tier: HealthTier) -> List[AccountHealth]:
        return [h for h in self._store.values() if h.health_tier == tier]

    def churning_accounts(self) -> List[AccountHealth]:
        return self.by_tier(HealthTier.CHURNING)

    def champion_accounts(self) -> List[AccountHealth]:
        return self.by_tier(HealthTier.CHAMPION)

    def at_risk_accounts(self) -> List[AccountHealth]:
        return [h for h in self._store.values() if h.health_tier in (HealthTier.AT_RISK, HealthTier.CHURNING)]

    def expansion_opportunities(self, min_potential: float = 5000.0) -> List[AccountHealth]:
        return sorted(
            [h for h in self._store.values() if h.expansion_potential_eur >= min_potential],
            key=lambda h: h.expansion_potential_eur,
            reverse=True,
        )

    def renewal_at_risk(self, days_threshold: int = 90) -> List[AccountHealth]:
        return [
            h for h in self._store.values()
            if h.account.days_until_renewal <= days_threshold and h.renewal_forecast in ("uncertain", "at_risk")
        ]

    def total_arr(self) -> float:
        return sum(h.account.arr_eur for h in self._store.values())

    def arr_at_risk(self) -> float:
        return sum(
            h.account.arr_eur
            for h in self._store.values()
            if h.health_tier in (HealthTier.AT_RISK, HealthTier.CHURNING)
        )

    def summary(self) -> dict:
        items = list(self._store.values())
        count = len(items)
        if count == 0:
            return {
                "total": 0,
                "tier_counts": {t.value: 0 for t in HealthTier},
                "action_counts": {a.value: 0 for a in AccountAction},
                "avg_health_score": 0.0,
                "avg_churn_risk_pct": 0.0,
                "total_arr_eur": 0.0,
                "arr_at_risk_eur": 0.0,
                "total_expansion_potential_eur": 0.0,
            }
        tier_counts = {t.value: 0 for t in HealthTier}
        action_counts = {a.value: 0 for a in AccountAction}
        for h in items:
            tier_counts[h.health_tier.value] += 1
            action_counts[h.primary_action.value] += 1
        avg_health = sum(h.health_score for h in items) / count
        avg_churn = sum(h.churn_risk_pct for h in items) / count
        total_arr = self.total_arr()
        risk_arr = self.arr_at_risk()
        total_exp = sum(h.expansion_potential_eur for h in items)
        return {
            "total": count,
            "tier_counts": tier_counts,
            "action_counts": action_counts,
            "avg_health_score": round(avg_health, 2),
            "avg_churn_risk_pct": round(avg_churn, 2),
            "total_arr_eur": round(total_arr, 2),
            "arr_at_risk_eur": round(risk_arr, 2),
            "total_expansion_potential_eur": round(total_exp, 2),
        }

    def reset(self) -> None:
        self._store.clear()
