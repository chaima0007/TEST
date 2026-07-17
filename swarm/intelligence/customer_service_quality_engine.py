"""Customer Service Quality Engine — monitors resolution rates, escalation patterns,
agent capacity and customer satisfaction to detect service degradation early."""

from __future__ import annotations

import dataclasses
from enum import Enum


class ServiceRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ServicePattern(str, Enum):
    none                 = "none"
    resolution_failure   = "resolution_failure"
    escalation_cascade   = "escalation_cascade"
    agent_burnout        = "agent_burnout"
    sla_breach           = "sla_breach"
    satisfaction_collapse = "satisfaction_collapse"


class ServiceSeverity(str, Enum):
    excellent  = "excellent"
    acceptable = "acceptable"
    degraded   = "degraded"
    failing    = "failing"


class ServiceAction(str, Enum):
    no_action                = "no_action"
    quality_monitoring       = "quality_monitoring"
    coaching_intervention    = "coaching_intervention"
    team_rebalancing         = "team_rebalancing"
    sla_recovery_plan        = "sla_recovery_plan"
    escalation_process_review = "escalation_process_review"
    agent_support_program    = "agent_support_program"
    capacity_emergency       = "capacity_emergency"
    executive_service_review = "executive_service_review"


@dataclasses.dataclass
class ServiceInput:
    ticket_id:                    str
    agent_id:                     str
    region:                       str
    first_contact_resolution_pct: float   # 0-1
    avg_resolution_time_hours:    float
    sla_breach_rate_pct:          float   # 0-1
    reopened_ticket_rate_pct:     float   # 0-1
    escalation_rate_pct:          float   # 0-1
    escalation_to_level3_pct:     float   # 0-1
    agent_utilization_pct:        float   # 0-1
    avg_handle_time_minutes:      float
    backlog_growth_rate_pct:      float   # 0-1
    customer_satisfaction_score:  float   # 0-1
    nps_from_support:             float   # -100 to 100
    complaint_rate_pct:           float   # 0-1
    agent_satisfaction_score:     float   # 0-1
    knowledge_base_usage_pct:     float   # 0-1
    ticket_volume_spike_pct:      float   # % above normal
    repeat_contact_rate_pct:      float   # 0-1
    channel_deflection_failure_pct: float # 0-1
    avg_queue_wait_minutes:       float


@dataclasses.dataclass
class ServiceResult:
    ticket_id:                  str
    region:                     str
    service_risk:               ServiceRisk
    service_pattern:            ServicePattern
    service_severity:           ServiceSeverity
    recommended_action:         ServiceAction
    resolution_score:           float
    escalation_score:           float
    satisfaction_score:         float
    capacity_score:             float
    service_composite:          float
    has_service_gap:            bool
    requires_management_action: bool
    estimated_churn_risk_pct:   float
    service_signal:             str

    def to_dict(self) -> dict:
        return {
            "ticket_id":                  self.ticket_id,
            "region":                     self.region,
            "service_risk":               self.service_risk.value,
            "service_pattern":            self.service_pattern.value,
            "service_severity":           self.service_severity.value,
            "recommended_action":         self.recommended_action.value,
            "resolution_score":           round(self.resolution_score, 1),
            "escalation_score":           round(self.escalation_score, 1),
            "satisfaction_score":         round(self.satisfaction_score, 1),
            "capacity_score":             round(self.capacity_score, 1),
            "service_composite":          round(self.service_composite, 1),
            "has_service_gap":            self.has_service_gap,
            "requires_management_action": self.requires_management_action,
            "estimated_churn_risk_pct":   self.estimated_churn_risk_pct,
            "service_signal":             self.service_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class CustomerServiceQualityEngine:
    """Detects service quality degradation through resolution, escalation,
    satisfaction and capacity sub-scores."""

    def __init__(self) -> None:
        self._results: list[ServiceResult] = []

    # ── sub-scores (HIGHER = more risk/degradation) ──────────────────────────

    def _resolution_score(self, inp: ServiceInput) -> float:
        score = 0.0
        if inp.first_contact_resolution_pct <= 0.40:
            score += 40.0
        elif inp.first_contact_resolution_pct <= 0.60:
            score += 22.0
        elif inp.first_contact_resolution_pct <= 0.75:
            score += 8.0

        if inp.reopened_ticket_rate_pct >= 0.25:
            score += 35.0
        elif inp.reopened_ticket_rate_pct >= 0.15:
            score += 18.0
        elif inp.reopened_ticket_rate_pct >= 0.08:
            score += 6.0

        if inp.avg_resolution_time_hours >= 48:
            score += 25.0
        elif inp.avg_resolution_time_hours >= 24:
            score += 12.0

        return _clamp(score)

    def _escalation_score(self, inp: ServiceInput) -> float:
        score = 0.0
        if inp.escalation_rate_pct >= 0.35:
            score += 40.0
        elif inp.escalation_rate_pct >= 0.20:
            score += 22.0
        elif inp.escalation_rate_pct >= 0.10:
            score += 8.0

        if inp.escalation_to_level3_pct >= 0.15:
            score += 35.0
        elif inp.escalation_to_level3_pct >= 0.08:
            score += 18.0

        if inp.sla_breach_rate_pct >= 0.30:
            score += 25.0
        elif inp.sla_breach_rate_pct >= 0.15:
            score += 12.0

        return _clamp(score)

    def _satisfaction_score(self, inp: ServiceInput) -> float:
        score = 0.0
        if inp.customer_satisfaction_score <= 0.50:
            score += 45.0
        elif inp.customer_satisfaction_score <= 0.65:
            score += 25.0
        elif inp.customer_satisfaction_score <= 0.78:
            score += 10.0

        if inp.complaint_rate_pct >= 0.15:
            score += 30.0
        elif inp.complaint_rate_pct >= 0.08:
            score += 15.0

        if inp.repeat_contact_rate_pct >= 0.30:
            score += 25.0
        elif inp.repeat_contact_rate_pct >= 0.15:
            score += 12.0

        return _clamp(score)

    def _capacity_score(self, inp: ServiceInput) -> float:
        score = 0.0
        if inp.agent_utilization_pct >= 0.90:
            score += 40.0
        elif inp.agent_utilization_pct >= 0.80:
            score += 22.0
        elif inp.agent_utilization_pct >= 0.70:
            score += 8.0

        if inp.backlog_growth_rate_pct >= 0.40:
            score += 35.0
        elif inp.backlog_growth_rate_pct >= 0.20:
            score += 18.0
        elif inp.backlog_growth_rate_pct >= 0.10:
            score += 6.0

        if inp.avg_queue_wait_minutes >= 60:
            score += 25.0
        elif inp.avg_queue_wait_minutes >= 30:
            score += 12.0

        return _clamp(score)

    # ── classification ────────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> ServiceRisk:
        if composite >= 60:
            return ServiceRisk.critical
        if composite >= 40:
            return ServiceRisk.high
        if composite >= 20:
            return ServiceRisk.moderate
        return ServiceRisk.low

    def _classify_severity(self, composite: float) -> ServiceSeverity:
        if composite >= 60:
            return ServiceSeverity.failing
        if composite >= 40:
            return ServiceSeverity.degraded
        if composite >= 20:
            return ServiceSeverity.acceptable
        return ServiceSeverity.excellent

    def _detect_pattern(self, inp: ServiceInput) -> ServicePattern:
        if inp.first_contact_resolution_pct <= 0.45 and inp.reopened_ticket_rate_pct >= 0.20:
            return ServicePattern.resolution_failure
        if inp.escalation_rate_pct >= 0.30 and inp.escalation_to_level3_pct >= 0.10:
            return ServicePattern.escalation_cascade
        if inp.agent_utilization_pct >= 0.88 and inp.agent_satisfaction_score <= 0.40:
            return ServicePattern.agent_burnout
        if inp.sla_breach_rate_pct >= 0.25 and inp.avg_resolution_time_hours >= 36:
            return ServicePattern.sla_breach
        if inp.customer_satisfaction_score <= 0.55 and inp.complaint_rate_pct >= 0.12:
            return ServicePattern.satisfaction_collapse
        return ServicePattern.none

    def _recommend_action(
        self,
        risk: ServiceRisk,
        pattern: ServicePattern,
    ) -> ServiceAction:
        if risk == ServiceRisk.critical:
            if pattern in (ServicePattern.escalation_cascade, ServicePattern.satisfaction_collapse):
                return ServiceAction.executive_service_review
            return ServiceAction.capacity_emergency

        if risk == ServiceRisk.high:
            if pattern == ServicePattern.resolution_failure:
                return ServiceAction.coaching_intervention
            if pattern == ServicePattern.escalation_cascade:
                return ServiceAction.escalation_process_review
            if pattern == ServicePattern.agent_burnout:
                return ServiceAction.agent_support_program
            if pattern == ServicePattern.sla_breach:
                return ServiceAction.sla_recovery_plan
            if pattern == ServicePattern.satisfaction_collapse:
                return ServiceAction.coaching_intervention
            return ServiceAction.quality_monitoring

        if risk == ServiceRisk.moderate:
            return ServiceAction.team_rebalancing

        return ServiceAction.no_action

    def _build_signal(
        self,
        inp: ServiceInput,
        comp: float,
        risk: ServiceRisk,
    ) -> str:
        if comp < 20:
            return (
                "Service quality excellent — resolution, escalation, satisfaction "
                "and capacity within benchmarks"
            )
        label = risk.value.capitalize()
        fcr   = round(inp.first_contact_resolution_pct * 100)
        csat  = round(inp.customer_satisfaction_score * 100)
        sla   = round(inp.sla_breach_rate_pct * 100)
        c     = round(comp)
        return (
            f"{label} — {fcr}% FCR — CSAT {csat} — {sla}% SLA breach — composite {c}"
        )

    # ── public API ────────────────────────────────────────────────────────────

    def analyze(self, inp: ServiceInput) -> ServiceResult:
        resolution   = self._resolution_score(inp)
        escalation   = self._escalation_score(inp)
        satisfaction = self._satisfaction_score(inp)
        capacity     = self._capacity_score(inp)

        composite = _clamp(
            resolution   * 0.30
            + escalation   * 0.25
            + satisfaction * 0.25
            + capacity     * 0.20
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        pattern  = self._detect_pattern(inp)
        action   = self._recommend_action(risk, pattern)

        has_service_gap = (
            composite >= 40
            or inp.sla_breach_rate_pct >= 0.20
            or inp.customer_satisfaction_score <= 0.60
        )
        requires_management_action = (
            composite >= 25
            or inp.escalation_rate_pct >= 0.20
            or inp.agent_utilization_pct >= 0.85
        )
        estimated_churn_risk_pct = round(
            min((1 - inp.customer_satisfaction_score) * (composite / 100) * 2, 1.0), 2
        )

        result = ServiceResult(
            ticket_id=inp.ticket_id,
            region=inp.region,
            service_risk=risk,
            service_pattern=pattern,
            service_severity=severity,
            recommended_action=action,
            resolution_score=resolution,
            escalation_score=escalation,
            satisfaction_score=satisfaction,
            capacity_score=capacity,
            service_composite=composite,
            has_service_gap=has_service_gap,
            requires_management_action=requires_management_action,
            estimated_churn_risk_pct=estimated_churn_risk_pct,
            service_signal=self._build_signal(inp, composite, risk),
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[ServiceInput]) -> list[ServiceResult]:
        return [self.analyze(i) for i in inputs]

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                       0,
                "risk_counts":                 {},
                "pattern_counts":              {},
                "severity_counts":             {},
                "action_counts":               {},
                "avg_service_composite":       0.0,
                "service_gap_count":           0,
                "management_action_count":     0,
                "avg_resolution_score":        0.0,
                "avg_escalation_score":        0.0,
                "avg_satisfaction_score":      0.0,
                "avg_capacity_score":          0.0,
                "avg_estimated_churn_risk_pct": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_res = total_esc = total_sat = total_cap = total_churn = 0.0
        gap_count = mgmt_count = 0

        for r in self._results:
            risk_counts[r.service_risk.value]         = risk_counts.get(r.service_risk.value, 0) + 1
            pattern_counts[r.service_pattern.value]   = pattern_counts.get(r.service_pattern.value, 0) + 1
            severity_counts[r.service_severity.value] = severity_counts.get(r.service_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.service_composite
            total_res   += r.resolution_score
            total_esc   += r.escalation_score
            total_sat   += r.satisfaction_score
            total_cap   += r.capacity_score
            total_churn += r.estimated_churn_risk_pct
            if r.has_service_gap:
                gap_count += 1
            if r.requires_management_action:
                mgmt_count += 1

        n = len(self._results)
        return {
            "total":                        n,
            "risk_counts":                  risk_counts,
            "pattern_counts":               pattern_counts,
            "severity_counts":              severity_counts,
            "action_counts":                action_counts,
            "avg_service_composite":        round(total_comp  / n, 1),
            "service_gap_count":            gap_count,
            "management_action_count":      mgmt_count,
            "avg_resolution_score":         round(total_res   / n, 1),
            "avg_escalation_score":         round(total_esc   / n, 1),
            "avg_satisfaction_score":       round(total_sat   / n, 1),
            "avg_capacity_score":           round(total_cap   / n, 1),
            "avg_estimated_churn_risk_pct": round(total_churn / n, 2),
        }
