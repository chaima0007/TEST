"""
Module 219 — Sales Account Churn Early Warning Engine
Detects early churn signals in existing accounts before renewal risk
becomes visible — usage decay, sponsor loss, support escalations.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class ChurnRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ChurnPattern(str, Enum):
    none                 = "none"
    usage_collapse       = "usage_collapse"
    sponsor_exodus       = "sponsor_exodus"
    support_spiral       = "support_spiral"
    competitive_switch   = "competitive_switch"
    value_gap_crisis     = "value_gap_crisis"


class ChurnSeverity(str, Enum):
    healthy    = "healthy"
    watching   = "watching"
    at_risk    = "at_risk"
    churning   = "churning"


class ChurnAction(str, Enum):
    no_action                     = "no_action"
    health_monitoring             = "health_monitoring"
    executive_business_review     = "executive_business_review"
    success_plan_reset            = "success_plan_reset"
    competitive_defense_playbook  = "competitive_defense_playbook"
    sponsor_re_engagement         = "sponsor_re_engagement"
    support_escalation_resolution = "support_escalation_resolution"
    renewal_risk_intervention     = "renewal_risk_intervention"
    executive_save_call           = "executive_save_call"


@dataclass
class ChurnInput:
    account_id: str
    region: str
    evaluation_period_id: str
    # Usage signals
    product_usage_decay_pct: float           # % drop in active usage vs prior period
    feature_adoption_rate_pct: float         # % of contracted features actively used
    login_frequency_decay_pct: float         # % drop in login frequency
    api_call_volume_decay_pct: float         # % drop in API/integration calls
    # Relationship signals
    executive_sponsor_engaged: float         # 0-1 (1 = fully engaged)
    champion_tenure_months: float            # months current champion has been in role
    stakeholder_count_change: float          # net change in active stakeholders (negative = loss)
    last_exec_meeting_days_ago: float        # days since last executive-level contact
    # Support & satisfaction
    open_support_tickets: int                # count of open tickets
    avg_ticket_resolution_days: float        # avg days to resolve tickets
    nps_score_change: float                  # change in NPS since last measurement
    escalation_frequency_pct: float          # % of tickets that escalate
    # Competitive & value
    competitive_evaluation_signal: float     # 0-1 (1 = actively evaluating alternatives)
    roi_achievement_pct: float               # % of expected ROI actually achieved
    contract_utilization_pct: float          # % of contracted capacity used
    renewal_conversation_initiated: float    # 0-1 (1 = rep has opened renewal convo)
    # Volume context
    arr_usd: float                           # annual recurring revenue
    contract_months_remaining: int           # months until renewal
    days_to_renewal: int


@dataclass
class ChurnResult:
    account_id: str
    region: str
    churn_risk: str
    churn_pattern: str
    churn_severity: str
    recommended_action: str
    usage_score: float
    relationship_score: float
    support_score: float
    value_score: float
    churn_composite: float
    has_churn_signal: bool
    requires_executive_action: bool
    estimated_arr_at_risk_usd: float
    churn_signal: str

    def to_dict(self) -> Dict:
        return {
            "account_id":                 self.account_id,
            "region":                     self.region,
            "churn_risk":                 self.churn_risk,
            "churn_pattern":              self.churn_pattern,
            "churn_severity":             self.churn_severity,
            "recommended_action":         self.recommended_action,
            "usage_score":                self.usage_score,
            "relationship_score":         self.relationship_score,
            "support_score":              self.support_score,
            "value_score":                self.value_score,
            "churn_composite":            self.churn_composite,
            "has_churn_signal":           self.has_churn_signal,
            "requires_executive_action":  self.requires_executive_action,
            "estimated_arr_at_risk_usd":  self.estimated_arr_at_risk_usd,
            "churn_signal":               self.churn_signal,
        }


class SalesAccountChurnEarlyWarningEngine:
    def __init__(self) -> None:
        self._results: List[ChurnResult] = []

    def _usage_score(self, i: ChurnInput) -> float:
        s = 0
        if   i.product_usage_decay_pct   >= 0.50: s += 40
        elif i.product_usage_decay_pct   >= 0.30: s += 22
        elif i.product_usage_decay_pct   >= 0.15: s += 8

        if   i.feature_adoption_rate_pct <= 0.25: s += 35
        elif i.feature_adoption_rate_pct <= 0.45: s += 18
        elif i.feature_adoption_rate_pct <= 0.60: s += 6

        if   i.login_frequency_decay_pct >= 0.50: s += 25
        elif i.login_frequency_decay_pct >= 0.30: s += 12
        return min(s, 100)

    def _relationship_score(self, i: ChurnInput) -> float:
        s = 0
        if   i.executive_sponsor_engaged   <= 0.20: s += 40
        elif i.executive_sponsor_engaged   <= 0.45: s += 22
        elif i.executive_sponsor_engaged   <= 0.65: s += 8

        if   i.last_exec_meeting_days_ago  >= 120: s += 35
        elif i.last_exec_meeting_days_ago  >= 60:  s += 18
        elif i.last_exec_meeting_days_ago  >= 30:  s += 6

        if   i.stakeholder_count_change    <= -3:  s += 25
        elif i.stakeholder_count_change    <= -1:  s += 12
        return min(s, 100)

    def _support_score(self, i: ChurnInput) -> float:
        s = 0
        if   i.open_support_tickets        >= 10:  s += 40
        elif i.open_support_tickets        >= 5:   s += 22
        elif i.open_support_tickets        >= 2:   s += 8

        if   i.escalation_frequency_pct   >= 0.40: s += 35
        elif i.escalation_frequency_pct   >= 0.20: s += 18

        if   i.avg_ticket_resolution_days  >= 14:  s += 25
        elif i.avg_ticket_resolution_days  >= 7:   s += 12
        return min(s, 100)

    def _value_score(self, i: ChurnInput) -> float:
        s = 0
        if   i.roi_achievement_pct         <= 0.30: s += 45
        elif i.roi_achievement_pct         <= 0.55: s += 25
        elif i.roi_achievement_pct         <= 0.75: s += 10

        if   i.competitive_evaluation_signal >= 0.60: s += 30
        elif i.competitive_evaluation_signal >= 0.35: s += 15

        if   i.contract_utilization_pct    <= 0.30: s += 25
        elif i.contract_utilization_pct    <= 0.55: s += 12
        return min(s, 100)

    def _composite(self, us: float, re: float, su: float, va: float) -> float:
        return min(round(us * 0.30 + re * 0.25 + su * 0.25 + va * 0.20, 2), 100.0)

    def _risk(self, c: float) -> ChurnRisk:
        if c >= 60: return ChurnRisk.critical
        if c >= 40: return ChurnRisk.high
        if c >= 20: return ChurnRisk.moderate
        return ChurnRisk.low

    def _severity(self, c: float) -> ChurnSeverity:
        if c >= 60: return ChurnSeverity.churning
        if c >= 40: return ChurnSeverity.at_risk
        if c >= 20: return ChurnSeverity.watching
        return ChurnSeverity.healthy

    def _pattern(self, i: ChurnInput) -> ChurnPattern:
        if (i.product_usage_decay_pct >= 0.45
                and i.login_frequency_decay_pct >= 0.40):
            return ChurnPattern.usage_collapse
        if (i.executive_sponsor_engaged <= 0.25
                and i.stakeholder_count_change <= -2):
            return ChurnPattern.sponsor_exodus
        if (i.open_support_tickets >= 6
                and i.escalation_frequency_pct >= 0.30):
            return ChurnPattern.support_spiral
        if (i.competitive_evaluation_signal >= 0.55
                and i.roi_achievement_pct <= 0.60):
            return ChurnPattern.competitive_switch
        if (i.roi_achievement_pct <= 0.40
                and i.contract_utilization_pct <= 0.40):
            return ChurnPattern.value_gap_crisis
        return ChurnPattern.none

    def _action(self, risk: ChurnRisk, pat: ChurnPattern) -> ChurnAction:
        if risk == ChurnRisk.critical:
            if pat in (ChurnPattern.sponsor_exodus, ChurnPattern.competitive_switch):
                return ChurnAction.executive_save_call
            return ChurnAction.renewal_risk_intervention
        if risk == ChurnRisk.high:
            if pat == ChurnPattern.usage_collapse:    return ChurnAction.success_plan_reset
            if pat == ChurnPattern.sponsor_exodus:    return ChurnAction.sponsor_re_engagement
            if pat == ChurnPattern.support_spiral:    return ChurnAction.support_escalation_resolution
            if pat == ChurnPattern.competitive_switch: return ChurnAction.competitive_defense_playbook
            if pat == ChurnPattern.value_gap_crisis:  return ChurnAction.executive_business_review
            return ChurnAction.health_monitoring
        if risk == ChurnRisk.moderate:
            return ChurnAction.health_monitoring
        return ChurnAction.no_action

    def _signal(self, i: ChurnInput, pat: ChurnPattern, comp: float) -> str:
        if comp < 20:
            return "Account health strong — usage, relationship, support and value indicators within healthy benchmarks"
        labels = {
            ChurnPattern.usage_collapse:     "Usage collapse",
            ChurnPattern.sponsor_exodus:     "Sponsor exodus",
            ChurnPattern.support_spiral:     "Support spiral",
            ChurnPattern.competitive_switch: "Competitive switch",
            ChurnPattern.value_gap_crisis:   "Value gap crisis",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — {round(i.product_usage_decay_pct*100)}% usage decay — "
            f"{round(i.roi_achievement_pct*100)}% ROI achieved — "
            f"{i.days_to_renewal}d to renewal — "
            f"composite {round(comp)}"
        )

    def _has_churn_signal(self, i: ChurnInput, comp: float) -> bool:
        return (comp >= 40
                or i.product_usage_decay_pct >= 0.30
                or i.days_to_renewal <= 90)

    def _requires_executive_action(self, i: ChurnInput, comp: float) -> bool:
        return (comp >= 25
                or i.executive_sponsor_engaged <= 0.40
                or i.competitive_evaluation_signal >= 0.35)

    def _arr_at_risk(self, i: ChurnInput, comp: float) -> float:
        return round(i.arr_usd * (comp / 100), 2)

    def assess(self, i: ChurnInput) -> ChurnResult:
        us  = self._usage_score(i)
        re  = self._relationship_score(i)
        su  = self._support_score(i)
        va  = self._value_score(i)
        comp = self._composite(us, re, su, va)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = ChurnResult(
            account_id=i.account_id,
            region=i.region,
            churn_risk=risk.value,
            churn_pattern=pat.value,
            churn_severity=sev.value,
            recommended_action=act.value,
            usage_score=us,
            relationship_score=re,
            support_score=su,
            value_score=va,
            churn_composite=comp,
            has_churn_signal=self._has_churn_signal(i, comp),
            requires_executive_action=self._requires_executive_action(i, comp),
            estimated_arr_at_risk_usd=self._arr_at_risk(i, comp),
            churn_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ChurnInput]) -> List[ChurnResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_churn_composite": 0.0,
                "churn_signal_count": 0,
                "executive_action_count": 0,
                "avg_usage_score": 0.0,
                "avg_relationship_score": 0.0,
                "avg_support_score": 0.0,
                "avg_value_score": 0.0,
                "total_estimated_arr_at_risk_usd": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tus = tre = tsu = tva = tcomp = tarr = 0.0
        gc = ec = 0
        for r in self._results:
            rc[r.churn_risk]      = rc.get(r.churn_risk, 0)      + 1
            pc[r.churn_pattern]   = pc.get(r.churn_pattern, 0)   + 1
            sc[r.churn_severity]  = sc.get(r.churn_severity, 0)  + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            tus  += r.usage_score
            tre  += r.relationship_score
            tsu  += r.support_score
            tva  += r.value_score
            tcomp += r.churn_composite
            tarr += r.estimated_arr_at_risk_usd
            if r.has_churn_signal:          gc += 1
            if r.requires_executive_action: ec += 1
        return {
            "total":                              n,
            "risk_counts":                        rc,
            "pattern_counts":                     pc,
            "severity_counts":                    sc,
            "action_counts":                      ac,
            "avg_churn_composite":                round(tcomp / n, 1),
            "churn_signal_count":                 gc,
            "executive_action_count":             ec,
            "avg_usage_score":                    round(tus / n, 1),
            "avg_relationship_score":             round(tre / n, 1),
            "avg_support_score":                  round(tsu / n, 1),
            "avg_value_score":                    round(tva / n, 1),
            "total_estimated_arr_at_risk_usd":    round(tarr, 2),
        }
