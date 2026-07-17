from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class ExpansionOpportunity(str, Enum):
    UPSELL = "upsell"
    CROSS_SELL = "cross_sell"
    RENEWAL_UPGRADE = "renewal_upgrade"
    WHITESPACE = "whitespace"
    AT_RISK = "at_risk"


class ExpansionPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AccountHealth(str, Enum):
    CHAMPION = "champion"
    HEALTHY = "healthy"
    STABLE = "stable"
    AT_RISK = "at_risk"


class ExpansionAction(str, Enum):
    SCHEDULE_EXECUTIVE_BRIEFING = "schedule_executive_briefing"
    PROPOSE_EXPANSION = "propose_expansion"
    QBR_REQUIRED = "qbr_required"
    RETAIN_FOCUS = "retain_focus"


@dataclass
class AccountExpansionInput:
    account_id: str
    account_name: str
    rep_id: str
    contract_value_usd: float
    contract_renewal_days: int
    product_adoption_score: float
    active_users_count: int
    total_licensed_users_count: int
    support_ticket_count_90d: int
    nps_score: float
    exec_sponsor_engaged: int
    champion_identified: int
    qbr_completed_last_180d: int
    upsell_discussion_held: int
    cross_sell_product_gaps: int
    competitor_in_account: int
    days_since_last_touchpoint: int
    escalation_count_90d: int
    expansion_budget_confirmed: int
    expansion_usd_potential: float
    industry_growth_score: float
    account_tenure_days: int


@dataclass
class AccountExpansionResult:
    account_id: str
    account_name: str
    expansion_opportunity: ExpansionOpportunity
    expansion_priority: ExpansionPriority
    account_health: AccountHealth
    expansion_action: ExpansionAction
    adoption_health_score: float
    relationship_health_score: float
    commercial_readiness_score: float
    risk_score: float
    expansion_composite: float
    estimated_expansion_arr_usd: float
    is_expansion_ready: bool
    needs_retention_focus: bool
    primary_expansion_signal: str

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "account_name": self.account_name,
            "expansion_opportunity": self.expansion_opportunity.value,
            "expansion_priority": self.expansion_priority.value,
            "account_health": self.account_health.value,
            "expansion_action": self.expansion_action.value,
            "adoption_health_score": self.adoption_health_score,
            "relationship_health_score": self.relationship_health_score,
            "commercial_readiness_score": self.commercial_readiness_score,
            "risk_score": self.risk_score,
            "expansion_composite": self.expansion_composite,
            "estimated_expansion_arr_usd": self.estimated_expansion_arr_usd,
            "is_expansion_ready": self.is_expansion_ready,
            "needs_retention_focus": self.needs_retention_focus,
            "primary_expansion_signal": self.primary_expansion_signal,
        }


def _adoption_health_score(inp: AccountExpansionInput) -> float:
    score = 0.0
    # Product adoption (0-35)
    if inp.product_adoption_score >= 80:
        score += 35.0
    elif inp.product_adoption_score >= 60:
        score += 25.0
    elif inp.product_adoption_score >= 40:
        score += 15.0
    elif inp.product_adoption_score >= 20:
        score += 8.0
    # User utilization rate (0-30)
    if inp.total_licensed_users_count > 0:
        util = inp.active_users_count / inp.total_licensed_users_count
    else:
        util = 0.0
    if util >= 0.9:
        score += 30.0
    elif util >= 0.7:
        score += 22.0
    elif util >= 0.5:
        score += 14.0
    elif util >= 0.3:
        score += 7.0
    # NPS contribution (0-20)
    if inp.nps_score >= 50:
        score += 20.0
    elif inp.nps_score >= 20:
        score += 14.0
    elif inp.nps_score >= 0:
        score += 8.0
    elif inp.nps_score >= -20:
        score += 3.0
    # Support health (0-15) — penalties for high tickets
    if inp.support_ticket_count_90d == 0:
        score += 15.0
    elif inp.support_ticket_count_90d <= 2:
        score += 10.0
    elif inp.support_ticket_count_90d <= 5:
        score += 5.0
    # Escalation penalty
    if inp.escalation_count_90d >= 3:
        score -= 10.0
    elif inp.escalation_count_90d >= 1:
        score -= 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _relationship_health_score(inp: AccountExpansionInput) -> float:
    score = 0.0
    # Executive sponsor (0-30)
    if inp.exec_sponsor_engaged:
        score += 30.0
    # Champion (0-25)
    if inp.champion_identified:
        score += 25.0
    # QBR completed (0-20)
    if inp.qbr_completed_last_180d:
        score += 20.0
    # Recency of touchpoint (0-15)
    if inp.days_since_last_touchpoint <= 7:
        score += 15.0
    elif inp.days_since_last_touchpoint <= 14:
        score += 10.0
    elif inp.days_since_last_touchpoint <= 30:
        score += 6.0
    elif inp.days_since_last_touchpoint <= 60:
        score += 2.0
    # Account tenure bonus (0-10)
    if inp.account_tenure_days >= 730:
        score += 10.0
    elif inp.account_tenure_days >= 365:
        score += 7.0
    elif inp.account_tenure_days >= 180:
        score += 4.0
    # Competitor presence penalty
    if inp.competitor_in_account:
        score -= 10.0
    return max(0.0, min(100.0, round(score, 1)))


def _commercial_readiness_score(inp: AccountExpansionInput) -> float:
    score = 0.0
    # Budget confirmed (0-35)
    if inp.expansion_budget_confirmed:
        score += 35.0
    # Upsell discussion (0-25)
    if inp.upsell_discussion_held:
        score += 25.0
    # Cross-sell gaps (0-20)
    if inp.cross_sell_product_gaps >= 3:
        score += 20.0
    elif inp.cross_sell_product_gaps >= 2:
        score += 14.0
    elif inp.cross_sell_product_gaps >= 1:
        score += 7.0
    # Industry growth (0-10)
    score += inp.industry_growth_score * 0.10
    # Renewal urgency (0-10)
    if 0 < inp.contract_renewal_days <= 90:
        score += 10.0
    elif inp.contract_renewal_days <= 180:
        score += 6.0
    elif inp.contract_renewal_days <= 365:
        score += 3.0
    return max(0.0, min(100.0, round(score, 1)))


def _risk_score(inp: AccountExpansionInput) -> float:
    score = 0.0
    # NPS risk
    if inp.nps_score < -30:
        score += 30.0
    elif inp.nps_score < 0:
        score += 20.0
    elif inp.nps_score < 20:
        score += 10.0
    # Escalations
    if inp.escalation_count_90d >= 3:
        score += 25.0
    elif inp.escalation_count_90d >= 1:
        score += 15.0
    # Competitor presence
    if inp.competitor_in_account:
        score += 20.0
    # Low adoption
    if inp.product_adoption_score < 30:
        score += 15.0
    elif inp.product_adoption_score < 50:
        score += 8.0
    # Renewal proximity risk
    if 0 < inp.contract_renewal_days <= 30:
        score += 10.0
    return max(0.0, min(100.0, round(score, 1)))


def _composite(adoption: float, relationship: float, commercial: float, risk: float) -> float:
    raw = adoption * 0.30 + relationship * 0.30 + commercial * 0.25 + (100.0 - risk) * 0.15
    return round(raw, 1)


def _expansion_opportunity(inp: AccountExpansionInput, adoption: float, risk: float) -> ExpansionOpportunity:
    if risk >= 50 or inp.nps_score < -20:
        return ExpansionOpportunity.AT_RISK
    if inp.expansion_budget_confirmed and inp.upsell_discussion_held:
        return ExpansionOpportunity.UPSELL
    if inp.cross_sell_product_gaps >= 2:
        return ExpansionOpportunity.CROSS_SELL
    if inp.contract_renewal_days <= 180:
        return ExpansionOpportunity.RENEWAL_UPGRADE
    return ExpansionOpportunity.WHITESPACE


def _account_health(composite: float, risk: float) -> AccountHealth:
    if composite >= 80 and risk < 20:
        return AccountHealth.CHAMPION
    if composite >= 65:
        return AccountHealth.HEALTHY
    if composite >= 45:
        return AccountHealth.STABLE
    return AccountHealth.AT_RISK


def _expansion_priority(composite: float, inp: AccountExpansionInput) -> ExpansionPriority:
    if composite < 35 or inp.escalation_count_90d >= 3:
        return ExpansionPriority.CRITICAL
    if composite >= 75 and inp.expansion_budget_confirmed:
        return ExpansionPriority.HIGH
    if composite >= 55:
        return ExpansionPriority.MEDIUM
    return ExpansionPriority.LOW


def _expansion_action(health: AccountHealth, composite: float, inp: AccountExpansionInput) -> ExpansionAction:
    if health == AccountHealth.AT_RISK or inp.escalation_count_90d >= 3:
        return ExpansionAction.RETAIN_FOCUS
    if inp.exec_sponsor_engaged and inp.expansion_budget_confirmed:
        return ExpansionAction.SCHEDULE_EXECUTIVE_BRIEFING
    if composite >= 60 and inp.upsell_discussion_held:
        return ExpansionAction.PROPOSE_EXPANSION
    return ExpansionAction.QBR_REQUIRED


def _estimated_expansion_arr(inp: AccountExpansionInput, composite: float) -> float:
    base = inp.expansion_usd_potential
    if composite >= 75:
        multiplier = 0.85
    elif composite >= 55:
        multiplier = 0.60
    elif composite >= 40:
        multiplier = 0.35
    else:
        multiplier = 0.10
    return round(base * multiplier, 0)


def _primary_expansion_signal(inp: AccountExpansionInput, adoption: float,
                               relationship: float, commercial: float) -> str:
    if inp.expansion_budget_confirmed:
        return "expansion budget confirmed — ready to propose"
    if inp.exec_sponsor_engaged and inp.upsell_discussion_held:
        return "exec sponsor + upsell discussion active"
    if inp.cross_sell_product_gaps >= 3:
        return "3+ product gaps — strong cross-sell potential"
    if inp.competitor_in_account:
        return "competitor present — displacement opportunity"
    if inp.contract_renewal_days <= 90:
        return "renewal in 90 days — upgrade window open"
    if inp.nps_score >= 70:
        return "high NPS — strong advocate, expansion ready"
    if inp.product_adoption_score >= 80 and adoption >= 70:
        return "high adoption — ready to expand seat count"
    return "standard account nurture required"


class AccountExpansionIntelligence:
    def __init__(self) -> None:
        self._results: dict[str, AccountExpansionResult] = {}

    def analyze(self, inp: AccountExpansionInput) -> AccountExpansionResult:
        adoption = _adoption_health_score(inp)
        relationship = _relationship_health_score(inp)
        commercial = _commercial_readiness_score(inp)
        risk = _risk_score(inp)
        composite = _composite(adoption, relationship, commercial, risk)

        opportunity = _expansion_opportunity(inp, adoption, risk)
        health = _account_health(composite, risk)
        priority = _expansion_priority(composite, inp)
        action = _expansion_action(health, composite, inp)
        estimated_arr = _estimated_expansion_arr(inp, composite)
        signal = _primary_expansion_signal(inp, adoption, relationship, commercial)

        is_expansion_ready = composite >= 65 and inp.expansion_budget_confirmed == 1
        needs_retention_focus = risk >= 50 or inp.escalation_count_90d >= 3 or inp.nps_score < -20

        result = AccountExpansionResult(
            account_id=inp.account_id,
            account_name=inp.account_name,
            expansion_opportunity=opportunity,
            expansion_priority=priority,
            account_health=health,
            expansion_action=action,
            adoption_health_score=adoption,
            relationship_health_score=relationship,
            commercial_readiness_score=commercial,
            risk_score=risk,
            expansion_composite=composite,
            estimated_expansion_arr_usd=estimated_arr,
            is_expansion_ready=is_expansion_ready,
            needs_retention_focus=needs_retention_focus,
            primary_expansion_signal=signal,
        )
        self._results[inp.account_id] = result
        return result

    def analyze_batch(self, inputs: List[AccountExpansionInput]) -> List[AccountExpansionResult]:
        results = [self.analyze(inp) for inp in inputs]
        results.sort(key=lambda r: r.expansion_composite, reverse=True)
        return results

    def get(self, account_id: str) -> AccountExpansionResult | None:
        return self._results.get(account_id)

    def all_accounts(self) -> List[AccountExpansionResult]:
        return sorted(self._results.values(), key=lambda r: r.expansion_composite, reverse=True)

    def expansion_ready(self) -> List[AccountExpansionResult]:
        return [r for r in self._results.values() if r.is_expansion_ready]

    def retention_focus(self) -> List[AccountExpansionResult]:
        return [r for r in self._results.values() if r.needs_retention_focus]

    def by_opportunity(self, opportunity: ExpansionOpportunity) -> List[AccountExpansionResult]:
        return [r for r in self._results.values() if r.expansion_opportunity == opportunity]

    def by_priority(self, priority: ExpansionPriority) -> List[AccountExpansionResult]:
        return [r for r in self._results.values() if r.expansion_priority == priority]

    def avg_expansion_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.expansion_composite for r in self._results.values()) / len(self._results), 1)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        opportunity_counts: dict[str, int] = {}
        priority_counts: dict[str, int] = {}
        health_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            opportunity_counts[r.expansion_opportunity.value] = opportunity_counts.get(r.expansion_opportunity.value, 0) + 1
            priority_counts[r.expansion_priority.value] = priority_counts.get(r.expansion_priority.value, 0) + 1
            health_counts[r.account_health.value] = health_counts.get(r.account_health.value, 0) + 1
            action_counts[r.expansion_action.value] = action_counts.get(r.expansion_action.value, 0) + 1
        return {
            "total": n,
            "opportunity_counts": opportunity_counts,
            "priority_counts": priority_counts,
            "health_counts": health_counts,
            "action_counts": action_counts,
            "avg_expansion_composite": self.avg_expansion_composite(),
            "expansion_ready_count": len(self.expansion_ready()),
            "retention_focus_count": len(self.retention_focus()),
            "avg_adoption_health_score": round(sum(r.adoption_health_score for r in results) / n, 1) if n else 0.0,
            "avg_relationship_health_score": round(sum(r.relationship_health_score for r in results) / n, 1) if n else 0.0,
            "avg_commercial_readiness_score": round(sum(r.commercial_readiness_score for r in results) / n, 1) if n else 0.0,
            "avg_risk_score": round(sum(r.risk_score for r in results) / n, 1) if n else 0.0,
            "total_expansion_arr_potential_usd": round(sum(r.estimated_expansion_arr_usd for r in results), 0) if n else 0.0,
        }
