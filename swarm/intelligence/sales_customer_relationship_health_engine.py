from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class RelationshipRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class RelationshipPattern(str, Enum):
    none                = "none"
    relationship_decay  = "relationship_decay"
    executive_neglect   = "executive_neglect"
    account_health_crisis = "account_health_crisis"
    expansion_neglect   = "expansion_neglect"
    qbr_backlog         = "qbr_backlog"


class RelationshipSeverity(str, Enum):
    healthy    = "healthy"
    at_risk    = "at_risk"
    degrading  = "degrading"
    critical   = "critical"


class RelationshipAction(str, Enum):
    no_action                  = "no_action"
    proactive_outreach         = "proactive_outreach"
    account_health_review      = "account_health_review"
    executive_engagement_push  = "executive_engagement_push"
    expansion_strategy_session = "expansion_strategy_session"
    relationship_recovery_plan = "relationship_recovery_plan"
    customer_success_emergency = "customer_success_emergency"
    executive_intervention     = "executive_intervention"


@dataclass
class CustomerRelationshipInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_active_accounts: int
    accounts_contacted_last_30d: int
    executive_meetings_last_90d: int
    qbr_completed_last_6m_count: int
    qbr_overdue_count: int
    avg_nps_score: float
    nps_score_decline_count: int
    support_escalations_count: int
    usage_declining_accounts_count: int
    expansion_conversations_initiated: int
    renewal_risk_accounts_identified: int
    renewal_risk_accounts_addressed: int
    account_plan_stale_count: int
    account_plan_current_count: int
    stakeholder_mapping_complete_rate_pct: float
    avg_relationship_depth_score: float
    customer_feedback_loop_rate_pct: float
    avg_account_revenue_usd: float
    nps_responses_collected: int


@dataclass
class CustomerRelationshipResult:
    rep_id: str
    region: str
    relationship_risk: RelationshipRisk
    relationship_pattern: RelationshipPattern
    relationship_severity: RelationshipSeverity
    recommended_action: RelationshipAction
    engagement_frequency_score: float
    relationship_quality_score: float
    account_health_score: float
    strategic_depth_score: float
    relationship_health_composite: float
    is_relationship_at_risk: bool
    requires_csa_intervention: bool
    estimated_revenue_at_risk_usd: float
    relationship_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                          self.rep_id,
            "region":                          self.region,
            "relationship_risk":               self.relationship_risk.value,
            "relationship_pattern":            self.relationship_pattern.value,
            "relationship_severity":           self.relationship_severity.value,
            "recommended_action":              self.recommended_action.value,
            "engagement_frequency_score":      self.engagement_frequency_score,
            "relationship_quality_score":      self.relationship_quality_score,
            "account_health_score":            self.account_health_score,
            "strategic_depth_score":           self.strategic_depth_score,
            "relationship_health_composite":   self.relationship_health_composite,
            "is_relationship_at_risk":         self.is_relationship_at_risk,
            "requires_csa_intervention":       self.requires_csa_intervention,
            "estimated_revenue_at_risk_usd":   self.estimated_revenue_at_risk_usd,
            "relationship_signal":             self.relationship_signal,
        }


class SalesCustomerRelationshipHealthEngine:

    def __init__(self) -> None:
        self._results: list[CustomerRelationshipResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _engagement_frequency_score(self, inp: CustomerRelationshipInput) -> float:
        score = 0.0
        total = max(inp.total_active_accounts, 1)

        contact_ratio = inp.accounts_contacted_last_30d / total
        if contact_ratio < 0.40:
            score += 35.0
        elif contact_ratio < 0.60:
            score += 20.0
        elif contact_ratio < 0.75:
            score += 8.0

        if inp.qbr_overdue_count >= 3:
            score += 30.0
        elif inp.qbr_overdue_count >= 2:
            score += 15.0
        elif inp.qbr_overdue_count >= 1:
            score += 8.0

        exec_ratio = inp.executive_meetings_last_90d / total
        if exec_ratio < 0.10:
            score += 20.0
        elif exec_ratio < 0.20:
            score += 10.0

        return min(score, 100.0)

    def _relationship_quality_score(self, inp: CustomerRelationshipInput) -> float:
        score = 0.0

        if inp.avg_nps_score < 0:
            score += 40.0
        elif inp.avg_nps_score < 20:
            score += 25.0
        elif inp.avg_nps_score < 40:
            score += 10.0

        if inp.nps_score_decline_count >= 3:
            score += 25.0
        elif inp.nps_score_decline_count >= 2:
            score += 12.0
        elif inp.nps_score_decline_count >= 1:
            score += 6.0

        if inp.avg_relationship_depth_score < 4.0:
            score += 20.0
        elif inp.avg_relationship_depth_score < 6.0:
            score += 10.0

        # Low feedback loop rate = no pulse on account health
        if inp.customer_feedback_loop_rate_pct < 0.30:
            score += 15.0
        elif inp.customer_feedback_loop_rate_pct < 0.50:
            score += 8.0

        return min(score, 100.0)

    def _account_health_score(self, inp: CustomerRelationshipInput) -> float:
        score = 0.0

        if inp.usage_declining_accounts_count >= 4:
            score += 35.0
        elif inp.usage_declining_accounts_count >= 2:
            score += 20.0
        elif inp.usage_declining_accounts_count >= 1:
            score += 8.0

        if inp.support_escalations_count >= 5:
            score += 30.0
        elif inp.support_escalations_count >= 3:
            score += 15.0
        elif inp.support_escalations_count >= 1:
            score += 5.0

        identified = max(inp.renewal_risk_accounts_identified, 1)
        addressed_ratio = inp.renewal_risk_accounts_addressed / identified
        if addressed_ratio < 0.40:
            score += 25.0
        elif addressed_ratio < 0.60:
            score += 12.0

        return min(score, 100.0)

    def _strategic_depth_score(self, inp: CustomerRelationshipInput) -> float:
        score = 0.0
        total_plans = inp.account_plan_stale_count + inp.account_plan_current_count
        total_plans_denom = max(total_plans, 1)

        stale_ratio = inp.account_plan_stale_count / total_plans_denom
        if stale_ratio >= 0.40:
            score += 35.0
        elif stale_ratio >= 0.25:
            score += 20.0

        if inp.stakeholder_mapping_complete_rate_pct < 0.40:
            score += 30.0
        elif inp.stakeholder_mapping_complete_rate_pct < 0.60:
            score += 15.0

        total = max(inp.total_active_accounts, 1)
        exp_rate = inp.expansion_conversations_initiated / total
        if exp_rate < 0.10:
            score += 20.0
        elif exp_rate < 0.25:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: CustomerRelationshipInput,
                         frequency: float, quality: float,
                         health: float, strategic: float) -> RelationshipPattern:
        # Priority: relationship_decay > executive_neglect > account_health_crisis
        #           > expansion_neglect > qbr_backlog > none
        if quality >= 35 and inp.nps_score_decline_count >= 2:
            return RelationshipPattern.relationship_decay

        total = max(inp.total_active_accounts, 1)
        exec_ratio = inp.executive_meetings_last_90d / total
        if frequency >= 30 and exec_ratio < 0.10:
            return RelationshipPattern.executive_neglect

        if health >= 40 and (inp.usage_declining_accounts_count >= 3 or inp.support_escalations_count >= 4):
            return RelationshipPattern.account_health_crisis

        if strategic >= 35 and inp.expansion_conversations_initiated < 2:
            return RelationshipPattern.expansion_neglect

        if inp.qbr_overdue_count >= 3:
            return RelationshipPattern.qbr_backlog

        return RelationshipPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> RelationshipRisk:
        if composite >= 60:
            return RelationshipRisk.critical
        if composite >= 40:
            return RelationshipRisk.high
        if composite >= 20:
            return RelationshipRisk.moderate
        return RelationshipRisk.low

    def _severity(self, composite: float) -> RelationshipSeverity:
        if composite >= 60:
            return RelationshipSeverity.critical
        if composite >= 40:
            return RelationshipSeverity.degrading
        if composite >= 20:
            return RelationshipSeverity.at_risk
        return RelationshipSeverity.healthy

    def _action(self, risk: RelationshipRisk, pattern: RelationshipPattern) -> RelationshipAction:
        if risk == RelationshipRisk.critical:
            if pattern == RelationshipPattern.relationship_decay:
                return RelationshipAction.executive_intervention
            if pattern == RelationshipPattern.account_health_crisis:
                return RelationshipAction.customer_success_emergency
            return RelationshipAction.relationship_recovery_plan
        if risk == RelationshipRisk.high:
            if pattern == RelationshipPattern.executive_neglect:
                return RelationshipAction.executive_engagement_push
            if pattern == RelationshipPattern.expansion_neglect:
                return RelationshipAction.expansion_strategy_session
            return RelationshipAction.account_health_review
        if risk == RelationshipRisk.moderate:
            return RelationshipAction.proactive_outreach
        return RelationshipAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _is_relationship_at_risk(self, composite: float,
                                  inp: CustomerRelationshipInput) -> bool:
        identified = max(inp.renewal_risk_accounts_identified, 1)
        return (
            composite >= 40
            or inp.usage_declining_accounts_count >= 3
            or (inp.renewal_risk_accounts_identified > 0
                and inp.renewal_risk_accounts_addressed / identified < 0.40)
        )

    def _requires_csa_intervention(self, composite: float,
                                    inp: CustomerRelationshipInput) -> bool:
        return (
            composite >= 30
            or inp.support_escalations_count >= 4
            or inp.nps_score_decline_count >= 3
        )

    # ------------------------------------------------------------------
    # Revenue at risk
    # ------------------------------------------------------------------

    def _estimated_revenue_at_risk(self, inp: CustomerRelationshipInput,
                                    composite: float) -> float:
        return round(
            inp.renewal_risk_accounts_identified * inp.avg_account_revenue_usd * (composite / 100.0), 2
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: CustomerRelationshipInput,
                pattern: RelationshipPattern, composite: float) -> str:
        if pattern == RelationshipPattern.none and composite < 20:
            return "Customer relationship health strong across portfolio"
        parts: list[str] = []
        if inp.nps_score_decline_count >= 1:
            parts.append(f"{inp.nps_score_decline_count} NPS declining accounts")
        if inp.usage_declining_accounts_count >= 2:
            parts.append(f"{inp.usage_declining_accounts_count} usage declining")
        if inp.qbr_overdue_count >= 2:
            parts.append(f"{inp.qbr_overdue_count} QBRs overdue")
        if inp.support_escalations_count >= 3:
            parts.append(f"{inp.support_escalations_count} escalations")
        label = pattern.value.replace("_", " ") if pattern != RelationshipPattern.none else "Relationship risk"
        summary = " — ".join(parts) if parts else "relationship health degrading"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: CustomerRelationshipInput) -> CustomerRelationshipResult:
        frequency  = round(self._engagement_frequency_score(inp), 1)
        quality    = round(self._relationship_quality_score(inp), 1)
        health     = round(self._account_health_score(inp), 1)
        strategic  = round(self._strategic_depth_score(inp), 1)

        composite = round(frequency * 0.25 + quality * 0.30 + health * 0.25 + strategic * 0.20, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, frequency, quality, health, strategic)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        at_risk   = self._is_relationship_at_risk(composite, inp)
        csa_req   = self._requires_csa_intervention(composite, inp)
        revenue   = self._estimated_revenue_at_risk(inp, composite)
        signal    = self._signal(inp, pattern, composite)

        result = CustomerRelationshipResult(
            rep_id=inp.rep_id,
            region=inp.region,
            relationship_risk=risk,
            relationship_pattern=pattern,
            relationship_severity=severity,
            recommended_action=action,
            engagement_frequency_score=frequency,
            relationship_quality_score=quality,
            account_health_score=health,
            strategic_depth_score=strategic,
            relationship_health_composite=composite,
            is_relationship_at_risk=at_risk,
            requires_csa_intervention=csa_req,
            estimated_revenue_at_risk_usd=revenue,
            relationship_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[CustomerRelationshipInput]) -> list[CustomerRelationshipResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_relationship_health_composite": 0.0,
                "relationship_at_risk_count": 0,
                "csa_intervention_count": 0,
                "avg_engagement_frequency_score": 0.0,
                "avg_relationship_quality_score": 0.0,
                "avg_account_health_score": 0.0,
                "avg_strategic_depth_score": 0.0,
                "total_estimated_revenue_at_risk_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_freq = total_qual = total_hlth = total_strat = total_rev = 0.0

        for r in self._results:
            risk_counts[r.relationship_risk.value]       = risk_counts.get(r.relationship_risk.value, 0) + 1
            pattern_counts[r.relationship_pattern.value] = pattern_counts.get(r.relationship_pattern.value, 0) + 1
            severity_counts[r.relationship_severity.value] = severity_counts.get(r.relationship_severity.value, 0) + 1
            action_counts[r.recommended_action.value]      = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.relationship_health_composite
            total_freq  += r.engagement_frequency_score
            total_qual  += r.relationship_quality_score
            total_hlth  += r.account_health_score
            total_strat += r.strategic_depth_score
            total_rev   += r.estimated_revenue_at_risk_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_relationship_health_composite":    round(total_comp / n, 1),
            "relationship_at_risk_count":           sum(1 for r in self._results if r.is_relationship_at_risk),
            "csa_intervention_count":               sum(1 for r in self._results if r.requires_csa_intervention),
            "avg_engagement_frequency_score":       round(total_freq / n, 1),
            "avg_relationship_quality_score":       round(total_qual / n, 1),
            "avg_account_health_score":             round(total_hlth / n, 1),
            "avg_strategic_depth_score":            round(total_strat / n, 1),
            "total_estimated_revenue_at_risk_usd":  round(total_rev, 2),
        }
