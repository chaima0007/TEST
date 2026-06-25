from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# ── Enums ─────────────────────────────────────────────────────────────────────

class SystemRisk(str, Enum):
    LOW      = "low"
    MODERATE = "moderate"
    HIGH     = "high"
    CRITICAL = "critical"


class SystemPattern(str, Enum):
    NONE                  = "none"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    CAPACITY_BREACH       = "capacity_breach"
    SECURITY_INCIDENT     = "security_incident"
    INTEGRATION_FAILURE   = "integration_failure"
    SERVICE_OUTAGE        = "service_outage"


class SystemSeverity(str, Enum):
    NOMINAL  = "nominal"
    DEGRADED = "degraded"
    IMPAIRED = "impaired"
    CRITICAL = "critical"


class SystemAction(str, Enum):
    NO_ACTION               = "no_action"
    HEALTH_MONITORING       = "health_monitoring"
    PERFORMANCE_TUNING      = "performance_tuning"
    CAPACITY_EXPANSION      = "capacity_expansion"
    SECURITY_PATCHING       = "security_patching"
    INTEGRATION_REMEDIATION = "integration_remediation"
    INCIDENT_RESPONSE       = "incident_response"
    DISASTER_RECOVERY       = "disaster_recovery"
    EMERGENCY_SHUTDOWN      = "emergency_shutdown"


# ── Input dataclass ────────────────────────────────────────────────────────────

@dataclass
class SystemInput:
    system_id:                    str
    environment:                  str
    region:                       str
    cpu_utilization_pct:          float   # 0–1
    memory_utilization_pct:       float   # 0–1
    disk_utilization_pct:         float   # 0–1
    network_latency_ms:           float   # milliseconds
    error_rate_pct:               float   # 0–1, % of requests with errors
    uptime_pct:                   float   # 0–1, system uptime over 30 days
    incident_count_30d:           int     # incidents in last 30 days
    mean_time_to_recovery_hours:  float   # MTTR
    security_vulnerability_count: int     # open vulnerabilities
    failed_security_scans:        int     # failed security checks
    patch_compliance_pct:         float   # 0–1, % systems patched
    integration_failure_rate_pct: float   # 0–1, API/integration failure %
    api_error_rate_pct:           float   # 0–1
    data_pipeline_lag_minutes:    float   # lag in data pipelines
    sla_compliance_pct:           float   # 0–1, % SLAs met
    backup_success_rate_pct:      float   # 0–1
    change_failure_rate_pct:      float   # 0–1, % changes causing incidents
    deployment_frequency_per_week: float
    avg_response_time_ms:         float


# ── Result dataclass ───────────────────────────────────────────────────────────

@dataclass
class SystemResult:
    system_id:                    str
    region:                       str
    system_risk:                  SystemRisk
    system_pattern:               SystemPattern
    system_severity:              SystemSeverity
    recommended_action:           SystemAction
    performance_score:            float
    capacity_score:               float
    security_score:               float
    reliability_score:            float
    system_composite:             float
    has_system_alert:             bool
    requires_immediate_action:    bool
    estimated_downtime_risk_hours: float
    system_signal:                str

    def to_dict(self) -> dict:
        return {
            "system_id":                    self.system_id,
            "region":                       self.region,
            "system_risk":                  self.system_risk.value,
            "system_pattern":               self.system_pattern.value,
            "system_severity":              self.system_severity.value,
            "recommended_action":           self.recommended_action.value,
            "performance_score":            self.performance_score,
            "capacity_score":               self.capacity_score,
            "security_score":               self.security_score,
            "reliability_score":            self.reliability_score,
            "system_composite":             self.system_composite,
            "has_system_alert":             self.has_system_alert,
            "requires_immediate_action":    self.requires_immediate_action,
            "estimated_downtime_risk_hours": self.estimated_downtime_risk_hours,
            "system_signal":                self.system_signal,
        }


# ── Engine ─────────────────────────────────────────────────────────────────────

class ITSystemsHealthMonitoringEngine:
    def __init__(self) -> None:
        self._results: list[SystemResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: SystemInput) -> SystemResult:
        perf  = self._performance_score(inp)
        cap   = self._capacity_score(inp)
        sec   = self._security_score(inp)
        rel   = self._reliability_score(inp)
        comp  = self._composite(perf, cap, sec, rel)
        risk  = self._system_risk(comp)
        sev   = self._system_severity(comp)
        pat   = self._system_pattern(inp)
        act   = self._system_action(risk, pat)
        alert = self._has_system_alert(inp, comp)
        immed = self._requires_immediate_action(inp, comp)
        dtr   = self._estimated_downtime_risk_hours(inp, comp)
        sig   = self._system_signal(inp, comp, risk)

        result = SystemResult(
            system_id=inp.system_id,
            region=inp.region,
            system_risk=risk,
            system_pattern=pat,
            system_severity=sev,
            recommended_action=act,
            performance_score=perf,
            capacity_score=cap,
            security_score=sec,
            reliability_score=rel,
            system_composite=comp,
            has_system_alert=alert,
            requires_immediate_action=immed,
            estimated_downtime_risk_hours=dtr,
            system_signal=sig,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[SystemInput]) -> list[SystemResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _performance_score(self, inp: SystemInput) -> float:
        score = 0.0
        # avg_response_time_ms (up to 40)
        if inp.avg_response_time_ms >= 2000:
            score += 40.0
        elif inp.avg_response_time_ms >= 1000:
            score += 22.0
        elif inp.avg_response_time_ms >= 500:
            score += 8.0
        # error_rate_pct (up to 35)
        if inp.error_rate_pct >= 0.10:
            score += 35.0
        elif inp.error_rate_pct >= 0.05:
            score += 18.0
        elif inp.error_rate_pct >= 0.02:
            score += 6.0
        # network_latency_ms (up to 25)
        if inp.network_latency_ms >= 500:
            score += 25.0
        elif inp.network_latency_ms >= 200:
            score += 12.0
        return round(max(0.0, min(100.0, score)), 1)

    def _capacity_score(self, inp: SystemInput) -> float:
        score = 0.0
        # cpu_utilization_pct (up to 40)
        if inp.cpu_utilization_pct >= 0.90:
            score += 40.0
        elif inp.cpu_utilization_pct >= 0.75:
            score += 22.0
        elif inp.cpu_utilization_pct >= 0.60:
            score += 8.0
        # memory_utilization_pct (up to 35)
        if inp.memory_utilization_pct >= 0.88:
            score += 35.0
        elif inp.memory_utilization_pct >= 0.72:
            score += 18.0
        elif inp.memory_utilization_pct >= 0.60:
            score += 6.0
        # disk_utilization_pct (up to 25)
        if inp.disk_utilization_pct >= 0.90:
            score += 25.0
        elif inp.disk_utilization_pct >= 0.75:
            score += 12.0
        return round(max(0.0, min(100.0, score)), 1)

    def _security_score(self, inp: SystemInput) -> float:
        score = 0.0
        # security_vulnerability_count (up to 45)
        if inp.security_vulnerability_count >= 10:
            score += 45.0
        elif inp.security_vulnerability_count >= 5:
            score += 25.0
        elif inp.security_vulnerability_count >= 1:
            score += 10.0
        # patch_compliance_pct (up to 30)
        if inp.patch_compliance_pct <= 0.60:
            score += 30.0
        elif inp.patch_compliance_pct <= 0.80:
            score += 15.0
        # failed_security_scans (up to 25)
        if inp.failed_security_scans >= 3:
            score += 25.0
        elif inp.failed_security_scans >= 1:
            score += 12.0
        return round(max(0.0, min(100.0, score)), 1)

    def _reliability_score(self, inp: SystemInput) -> float:
        score = 0.0
        # uptime_pct (up to 40)
        if inp.uptime_pct <= 0.95:
            score += 40.0
        elif inp.uptime_pct <= 0.98:
            score += 22.0
        elif inp.uptime_pct <= 0.995:
            score += 8.0
        # incident_count_30d (up to 35)
        if inp.incident_count_30d >= 8:
            score += 35.0
        elif inp.incident_count_30d >= 4:
            score += 18.0
        elif inp.incident_count_30d >= 1:
            score += 6.0
        # backup_success_rate_pct (up to 25)
        if inp.backup_success_rate_pct <= 0.80:
            score += 25.0
        elif inp.backup_success_rate_pct <= 0.92:
            score += 12.0
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self, perf: float, cap: float, sec: float, rel: float
    ) -> float:
        comp = perf * 0.30 + cap * 0.25 + sec * 0.25 + rel * 0.20
        return round(max(0.0, min(100.0, comp)), 1)

    # ── classification helpers ─────────────────────────────────────────────────

    def _system_risk(self, comp: float) -> SystemRisk:
        if comp >= 60:
            return SystemRisk.CRITICAL
        if comp >= 40:
            return SystemRisk.HIGH
        if comp >= 20:
            return SystemRisk.MODERATE
        return SystemRisk.LOW

    def _system_severity(self, comp: float) -> SystemSeverity:
        if comp >= 60:
            return SystemSeverity.CRITICAL
        if comp >= 40:
            return SystemSeverity.IMPAIRED
        if comp >= 20:
            return SystemSeverity.DEGRADED
        return SystemSeverity.NOMINAL

    def _system_pattern(self, inp: SystemInput) -> SystemPattern:
        # Priority order: 1 → 5
        if inp.avg_response_time_ms >= 1500 and inp.error_rate_pct >= 0.08:
            return SystemPattern.PERFORMANCE_DEGRADATION
        if inp.cpu_utilization_pct >= 0.88 and inp.memory_utilization_pct >= 0.85:
            return SystemPattern.CAPACITY_BREACH
        if inp.security_vulnerability_count >= 8 and inp.failed_security_scans >= 2:
            return SystemPattern.SECURITY_INCIDENT
        if inp.integration_failure_rate_pct >= 0.15 and inp.api_error_rate_pct >= 0.10:
            return SystemPattern.INTEGRATION_FAILURE
        if inp.uptime_pct <= 0.97 and inp.incident_count_30d >= 5:
            return SystemPattern.SERVICE_OUTAGE
        return SystemPattern.NONE

    def _system_action(self, risk: SystemRisk, pat: SystemPattern) -> SystemAction:
        if risk == SystemRisk.CRITICAL:
            if pat in (SystemPattern.SECURITY_INCIDENT, SystemPattern.SERVICE_OUTAGE):
                return SystemAction.DISASTER_RECOVERY
            return SystemAction.INCIDENT_RESPONSE
        if risk == SystemRisk.HIGH:
            if pat == SystemPattern.PERFORMANCE_DEGRADATION:
                return SystemAction.PERFORMANCE_TUNING
            if pat == SystemPattern.CAPACITY_BREACH:
                return SystemAction.CAPACITY_EXPANSION
            if pat == SystemPattern.SECURITY_INCIDENT:
                return SystemAction.SECURITY_PATCHING
            if pat == SystemPattern.INTEGRATION_FAILURE:
                return SystemAction.INTEGRATION_REMEDIATION
            if pat == SystemPattern.SERVICE_OUTAGE:
                return SystemAction.INCIDENT_RESPONSE
            return SystemAction.HEALTH_MONITORING
        if risk == SystemRisk.MODERATE:
            return SystemAction.HEALTH_MONITORING
        return SystemAction.NO_ACTION

    def _has_system_alert(self, inp: SystemInput, comp: float) -> bool:
        return (
            comp >= 40
            or inp.uptime_pct <= 0.98
            or inp.security_vulnerability_count >= 5
        )

    def _requires_immediate_action(self, inp: SystemInput, comp: float) -> bool:
        return (
            comp >= 25
            or inp.error_rate_pct >= 0.05
            or inp.security_vulnerability_count >= 3
        )

    def _estimated_downtime_risk_hours(self, inp: SystemInput, comp: float) -> float:
        return round(
            inp.mean_time_to_recovery_hours * (comp / 100) * (1 - inp.uptime_pct + 0.01),
            2,
        )

    def _system_signal(
        self, inp: SystemInput, comp: float, risk: SystemRisk
    ) -> str:
        if comp < 20:
            return (
                "System health nominal — performance, capacity, security and "
                "reliability within operational thresholds"
            )
        label = risk.value.upper()
        cpu_pct   = round(inp.cpu_utilization_pct * 100)
        err_pct   = round(inp.error_rate_pct * 100)
        up_pct    = round(inp.uptime_pct * 100, 1)
        vulns     = inp.security_vulnerability_count
        comp_rnd  = round(comp)
        return (
            f"{label} — {cpu_pct}% CPU — {err_pct}% error rate — "
            f"{up_pct}% uptime — {vulns} vulns — composite {comp_rnd}"
        )

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                           0,
                "risk_counts":                     {},
                "pattern_counts":                  {},
                "severity_counts":                 {},
                "action_counts":                   {},
                "avg_system_composite":            0.0,
                "system_alert_count":              0,
                "immediate_action_count":          0,
                "avg_performance_score":           0.0,
                "avg_capacity_score":              0.0,
                "avg_security_score":              0.0,
                "avg_reliability_score":           0.0,
                "avg_estimated_downtime_risk_hours": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp  = 0.0
        total_perf  = 0.0
        total_cap   = 0.0
        total_sec   = 0.0
        total_rel   = 0.0
        total_dtr   = 0.0

        for r in self._results:
            risk_counts[r.system_risk.value]       = risk_counts.get(r.system_risk.value, 0) + 1
            pattern_counts[r.system_pattern.value] = pattern_counts.get(r.system_pattern.value, 0) + 1
            severity_counts[r.system_severity.value] = severity_counts.get(r.system_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.system_composite
            total_perf += r.performance_score
            total_cap  += r.capacity_score
            total_sec  += r.security_score
            total_rel  += r.reliability_score
            total_dtr  += r.estimated_downtime_risk_hours

        return {
            "total":                           n,
            "risk_counts":                     risk_counts,
            "pattern_counts":                  pattern_counts,
            "severity_counts":                 severity_counts,
            "action_counts":                   action_counts,
            "avg_system_composite":            round(total_comp / n, 1),
            "system_alert_count":              sum(1 for r in self._results if r.has_system_alert),
            "immediate_action_count":          sum(1 for r in self._results if r.requires_immediate_action),
            "avg_performance_score":           round(total_perf / n, 1),
            "avg_capacity_score":              round(total_cap / n, 1),
            "avg_security_score":              round(total_sec / n, 1),
            "avg_reliability_score":           round(total_rel / n, 1),
            "avg_estimated_downtime_risk_hours": round(total_dtr / n, 2),
        }
