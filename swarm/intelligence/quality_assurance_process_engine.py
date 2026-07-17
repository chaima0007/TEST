"""
Module 238 — Quality Assurance & Process Optimization Engine
Monitors defect rates, process adherence, SLA compliance, audit scores, and
supplier quality — then recommends the right corrective action before quality
degradation becomes a customer-impacting event.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class QualityRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class QualityPattern(str, Enum):
    none                    = "none"
    defect_surge            = "defect_surge"
    process_deviation       = "process_deviation"
    sla_breach              = "sla_breach"
    audit_failure           = "audit_failure"
    supplier_quality_failure = "supplier_quality_failure"


class QualitySeverity(str, Enum):
    excellent   = "excellent"
    acceptable  = "acceptable"
    degraded    = "degraded"
    critical    = "critical"


class QualityAction(str, Enum):
    no_action                  = "no_action"
    quality_monitoring         = "quality_monitoring"
    process_review             = "process_review"
    corrective_action          = "corrective_action"
    supplier_audit             = "supplier_audit"
    sla_remediation            = "sla_remediation"
    quality_hold               = "quality_hold"
    process_redesign           = "process_redesign"
    emergency_quality_lockdown = "emergency_quality_lockdown"


@dataclass
class QualityInput:
    process_id: str
    process_type: str                      # manufacturing/software/service/procurement/delivery
    region: str
    defect_rate_pct: float                 # 0-1
    first_pass_yield_pct: float            # 0-1 (1=100% pass first time)
    customer_complaint_rate: float         # 0-1
    rework_rate_pct: float                 # 0-1
    cycle_time_variance_pct: float         # %
    sla_breach_rate: float                 # 0-1
    audit_score: float                     # 0-1 (1=perfect audit)
    process_adherence_score: float         # 0-1 (1=fully adhered)
    supplier_defect_rate: float            # 0-1
    inspection_failure_rate: float         # 0-1
    change_control_compliance_pct: float   # 0-1
    root_cause_resolution_rate: float      # 0-1 (1=all resolved)
    customer_satisfaction_score: float     # 0-1 (1=excellent)
    cost_of_quality_ratio: float           # 0-1
    testing_coverage_pct: float            # 0-1
    preventive_maintenance_score: float    # 0-1 (1=up to date)
    documentation_completeness_pct: float  # 0-1


@dataclass
class QualityResult:
    process_id: str
    region: str
    quality_risk: str
    quality_pattern: str
    quality_severity: str
    recommended_action: str
    defect_score: float
    process_score: float
    compliance_score: float
    supplier_score: float
    quality_composite: float
    has_quality_alert: bool
    requires_immediate_action: bool
    estimated_quality_risk_index: float
    quality_signal: str

    def to_dict(self) -> Dict:
        return {
            "process_id":                   self.process_id,
            "region":                       self.region,
            "quality_risk":                 self.quality_risk,
            "quality_pattern":              self.quality_pattern,
            "quality_severity":             self.quality_severity,
            "recommended_action":           self.recommended_action,
            "defect_score":                 self.defect_score,
            "process_score":                self.process_score,
            "compliance_score":             self.compliance_score,
            "supplier_score":               self.supplier_score,
            "quality_composite":            self.quality_composite,
            "has_quality_alert":            self.has_quality_alert,
            "requires_immediate_action":    self.requires_immediate_action,
            "estimated_quality_risk_index": self.estimated_quality_risk_index,
            "quality_signal":               self.quality_signal,
        }


class QualityAssuranceProcessEngine:
    def __init__(self) -> None:
        self._results: List[QualityResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _defect_score(self, i: QualityInput) -> float:
        s = 0
        if   i.defect_rate_pct >= 0.15: s += 40
        elif i.defect_rate_pct >= 0.08: s += 22
        elif i.defect_rate_pct >= 0.03: s += 8

        if   i.rework_rate_pct >= 0.20: s += 35
        elif i.rework_rate_pct >= 0.10: s += 18
        elif i.rework_rate_pct >= 0.04: s += 6

        if   i.first_pass_yield_pct <= 0.70: s += 25
        elif i.first_pass_yield_pct <= 0.85: s += 12
        return min(s, 100)

    def _process_score(self, i: QualityInput) -> float:
        s = 0
        if   i.process_adherence_score <= 0.50: s += 40
        elif i.process_adherence_score <= 0.70: s += 22
        elif i.process_adherence_score <= 0.85: s += 8

        if   i.cycle_time_variance_pct >= 40: s += 35
        elif i.cycle_time_variance_pct >= 20: s += 18
        elif i.cycle_time_variance_pct >= 10: s += 6

        if   i.root_cause_resolution_rate <= 0.50: s += 25
        elif i.root_cause_resolution_rate <= 0.70: s += 12
        return min(s, 100)

    def _compliance_score(self, i: QualityInput) -> float:
        s = 0
        if   i.audit_score <= 0.50: s += 40
        elif i.audit_score <= 0.70: s += 22
        elif i.audit_score <= 0.85: s += 8

        if   i.sla_breach_rate >= 0.20: s += 35
        elif i.sla_breach_rate >= 0.10: s += 18
        elif i.sla_breach_rate >= 0.04: s += 6

        if   i.change_control_compliance_pct <= 0.60: s += 25
        elif i.change_control_compliance_pct <= 0.80: s += 12
        return min(s, 100)

    def _supplier_score(self, i: QualityInput) -> float:
        s = 0
        if   i.supplier_defect_rate >= 0.15: s += 45
        elif i.supplier_defect_rate >= 0.08: s += 25
        elif i.supplier_defect_rate >= 0.03: s += 10

        if   i.inspection_failure_rate >= 0.20: s += 30
        elif i.inspection_failure_rate >= 0.10: s += 15

        if   i.documentation_completeness_pct <= 0.60: s += 25
        elif i.documentation_completeness_pct <= 0.80: s += 12
        return min(s, 100)

    def _composite(self, def_s: float, proc_s: float, comp_s: float, sup_s: float) -> float:
        return min(round(def_s * 0.30 + proc_s * 0.25 + comp_s * 0.25 + sup_s * 0.20, 2), 100.0)

    def _risk(self, c: float) -> QualityRisk:
        if c >= 60: return QualityRisk.critical
        if c >= 40: return QualityRisk.high
        if c >= 20: return QualityRisk.moderate
        return QualityRisk.low

    def _severity(self, c: float) -> QualitySeverity:
        if c >= 60: return QualitySeverity.critical
        if c >= 40: return QualitySeverity.degraded
        if c >= 20: return QualitySeverity.acceptable
        return QualitySeverity.excellent

    def _pattern(self, i: QualityInput) -> QualityPattern:
        if i.defect_rate_pct >= 0.12 or i.rework_rate_pct >= 0.18:
            return QualityPattern.defect_surge
        if i.audit_score <= 0.50 or i.change_control_compliance_pct <= 0.55:
            return QualityPattern.audit_failure
        if i.sla_breach_rate >= 0.15 or i.customer_complaint_rate >= 0.12:
            return QualityPattern.sla_breach
        if i.supplier_defect_rate >= 0.12 or i.inspection_failure_rate >= 0.18:
            return QualityPattern.supplier_quality_failure
        if i.process_adherence_score <= 0.55 and i.cycle_time_variance_pct >= 30:
            return QualityPattern.process_deviation
        return QualityPattern.none

    def _action(self, risk: QualityRisk, pat: QualityPattern) -> QualityAction:
        if risk == QualityRisk.critical:
            if pat == QualityPattern.defect_surge:
                return QualityAction.emergency_quality_lockdown
            if pat == QualityPattern.audit_failure:
                return QualityAction.emergency_quality_lockdown
            return QualityAction.quality_hold
        if risk == QualityRisk.high:
            if pat == QualityPattern.defect_surge:
                return QualityAction.quality_hold
            if pat == QualityPattern.audit_failure:
                return QualityAction.process_redesign
            if pat == QualityPattern.sla_breach:
                return QualityAction.sla_remediation
            if pat == QualityPattern.supplier_quality_failure:
                return QualityAction.supplier_audit
            if pat == QualityPattern.process_deviation:
                return QualityAction.corrective_action
            return QualityAction.process_review
        if risk == QualityRisk.moderate:
            return QualityAction.quality_monitoring
        return QualityAction.no_action

    def _signal(self, i: QualityInput, pat: QualityPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Qualité excellente — aucun défaut significatif, conformité maintenue, "
                "fournisseurs fiables"
            )
        labels = {
            QualityPattern.defect_surge:             "Surge de défauts",
            QualityPattern.process_deviation:        "Déviation processus",
            QualityPattern.sla_breach:               "Violation SLA",
            QualityPattern.audit_failure:            "Échec audit",
            QualityPattern.supplier_quality_failure: "Défaillance fournisseur",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — "
            f"défauts {i.defect_rate_pct * 100:.0f}% — "
            f"SLA {i.sla_breach_rate * 100:.0f}% — "
            f"audit {i.audit_score * 100:.0f}% — "
            f"composite {comp:.0f}"
        )

    def _has_quality_alert(self, i: QualityInput, comp: float) -> bool:
        return (
            comp >= 40
            or i.defect_rate_pct >= 0.10
            or i.sla_breach_rate >= 0.12
            or i.audit_score <= 0.55
        )

    def _requires_immediate_action(self, i: QualityInput, comp: float) -> bool:
        return (
            comp >= 25
            or i.defect_rate_pct >= 0.15
            or i.customer_complaint_rate >= 0.10
            or i.supplier_defect_rate >= 0.15
        )

    def _quality_risk_index(self, i: QualityInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.customer_satisfaction_score + 0.01) * 10, 10.0), 2)

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, i: QualityInput) -> QualityResult:
        def_s  = self._defect_score(i)
        proc_s = self._process_score(i)
        comp_s = self._compliance_score(i)
        sup_s  = self._supplier_score(i)
        comp   = self._composite(def_s, proc_s, comp_s, sup_s)
        risk   = self._risk(comp)
        sev    = self._severity(comp)
        pat    = self._pattern(i)
        act    = self._action(risk, pat)
        result = QualityResult(
            process_id=i.process_id,
            region=i.region,
            quality_risk=risk.value,
            quality_pattern=pat.value,
            quality_severity=sev.value,
            recommended_action=act.value,
            defect_score=def_s,
            process_score=proc_s,
            compliance_score=comp_s,
            supplier_score=sup_s,
            quality_composite=comp,
            has_quality_alert=self._has_quality_alert(i, comp),
            requires_immediate_action=self._requires_immediate_action(i, comp),
            estimated_quality_risk_index=self._quality_risk_index(i, comp),
            quality_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[QualityInput]) -> List[QualityResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_quality_composite": 0.0,
                "quality_alert_count": 0,
                "immediate_action_count": 0,
                "avg_defect_score": 0.0,
                "avg_process_score": 0.0,
                "avg_compliance_score": 0.0,
                "avg_supplier_score": 0.0,
                "avg_estimated_quality_risk_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        t_comp = t_def = t_proc = t_comp_s = t_sup = t_idx = 0.0
        alert_c = imm_c = 0
        for r in self._results:
            rc[r.quality_risk]          = rc.get(r.quality_risk, 0)          + 1
            pc[r.quality_pattern]       = pc.get(r.quality_pattern, 0)       + 1
            sc[r.quality_severity]      = sc.get(r.quality_severity, 0)      + 1
            ac[r.recommended_action]    = ac.get(r.recommended_action, 0)    + 1
            t_comp   += r.quality_composite
            t_def    += r.defect_score
            t_proc   += r.process_score
            t_comp_s += r.compliance_score
            t_sup    += r.supplier_score
            t_idx    += r.estimated_quality_risk_index
            if r.has_quality_alert:          alert_c += 1
            if r.requires_immediate_action:  imm_c   += 1
        return {
            "total":                             n,
            "risk_counts":                       rc,
            "pattern_counts":                    pc,
            "severity_counts":                   sc,
            "action_counts":                     ac,
            "avg_quality_composite":             round(t_comp / n, 1),
            "quality_alert_count":               alert_c,
            "immediate_action_count":            imm_c,
            "avg_defect_score":                  round(t_def / n, 1),
            "avg_process_score":                 round(t_proc / n, 1),
            "avg_compliance_score":              round(t_comp_s / n, 1),
            "avg_supplier_score":                round(t_sup / n, 1),
            "avg_estimated_quality_risk_index":  round(t_idx / n, 2),
        }


# ── mock data & smoke test ────────────────────────────────────────────────────

def _mock_processes() -> List[QualityInput]:
    return [
        QualityInput(
            process_id="QA-001", process_type="manufacturing", region="EMEA",
            defect_rate_pct=0.18, first_pass_yield_pct=0.62,
            customer_complaint_rate=0.18, rework_rate_pct=0.22,
            cycle_time_variance_pct=25, sla_breach_rate=0.08,
            audit_score=0.42, process_adherence_score=0.60,
            supplier_defect_rate=0.10, inspection_failure_rate=0.12,
            change_control_compliance_pct=0.65, root_cause_resolution_rate=0.55,
            customer_satisfaction_score=0.35, cost_of_quality_ratio=0.28,
            testing_coverage_pct=0.50, preventive_maintenance_score=0.45,
            documentation_completeness_pct=0.70,
        ),
        QualityInput(
            process_id="QA-002", process_type="software", region="NAMER",
            defect_rate_pct=0.01, first_pass_yield_pct=0.98,
            customer_complaint_rate=0.01, rework_rate_pct=0.02,
            cycle_time_variance_pct=3, sla_breach_rate=0.01,
            audit_score=0.97, process_adherence_score=0.97,
            supplier_defect_rate=0.01, inspection_failure_rate=0.01,
            change_control_compliance_pct=0.98, root_cause_resolution_rate=0.97,
            customer_satisfaction_score=0.96, cost_of_quality_ratio=0.03,
            testing_coverage_pct=0.97, preventive_maintenance_score=0.95,
            documentation_completeness_pct=0.98,
        ),
        QualityInput(
            process_id="QA-003", process_type="service", region="APAC",
            defect_rate_pct=0.08, first_pass_yield_pct=0.80,
            customer_complaint_rate=0.16, rework_rate_pct=0.09,
            cycle_time_variance_pct=15, sla_breach_rate=0.22,
            audit_score=0.72, process_adherence_score=0.60,
            supplier_defect_rate=0.04, inspection_failure_rate=0.06,
            change_control_compliance_pct=0.78, root_cause_resolution_rate=0.65,
            customer_satisfaction_score=0.62, cost_of_quality_ratio=0.15,
            testing_coverage_pct=0.70, preventive_maintenance_score=0.72,
            documentation_completeness_pct=0.80,
        ),
        QualityInput(
            process_id="QA-004", process_type="delivery", region="LATAM",
            defect_rate_pct=0.02, first_pass_yield_pct=0.97,
            customer_complaint_rate=0.02, rework_rate_pct=0.01,
            cycle_time_variance_pct=4, sla_breach_rate=0.02,
            audit_score=0.94, process_adherence_score=0.95,
            supplier_defect_rate=0.02, inspection_failure_rate=0.02,
            change_control_compliance_pct=0.96, root_cause_resolution_rate=0.94,
            customer_satisfaction_score=0.93, cost_of_quality_ratio=0.04,
            testing_coverage_pct=0.94, preventive_maintenance_score=0.92,
            documentation_completeness_pct=0.96,
        ),
        QualityInput(
            process_id="QA-005", process_type="procurement", region="EMEA",
            defect_rate_pct=0.14, first_pass_yield_pct=0.70,
            customer_complaint_rate=0.14, rework_rate_pct=0.12,
            cycle_time_variance_pct=18, sla_breach_rate=0.09,
            audit_score=0.45, process_adherence_score=0.58,
            supplier_defect_rate=0.22, inspection_failure_rate=0.28,
            change_control_compliance_pct=0.52, root_cause_resolution_rate=0.48,
            customer_satisfaction_score=0.38, cost_of_quality_ratio=0.30,
            testing_coverage_pct=0.55, preventive_maintenance_score=0.50,
            documentation_completeness_pct=0.65,
        ),
        QualityInput(
            process_id="QA-006", process_type="manufacturing", region="NAMER",
            defect_rate_pct=0.06, first_pass_yield_pct=0.88,
            customer_complaint_rate=0.05, rework_rate_pct=0.08,
            cycle_time_variance_pct=35, sla_breach_rate=0.05,
            audit_score=0.78, process_adherence_score=0.48,
            supplier_defect_rate=0.06, inspection_failure_rate=0.08,
            change_control_compliance_pct=0.72, root_cause_resolution_rate=0.62,
            customer_satisfaction_score=0.70, cost_of_quality_ratio=0.12,
            testing_coverage_pct=0.78, preventive_maintenance_score=0.75,
            documentation_completeness_pct=0.82,
        ),
        QualityInput(
            process_id="QA-007", process_type="software", region="APAC",
            defect_rate_pct=0.05, first_pass_yield_pct=0.88,
            customer_complaint_rate=0.07, rework_rate_pct=0.06,
            cycle_time_variance_pct=12, sla_breach_rate=0.14,
            audit_score=0.38, process_adherence_score=0.55,
            supplier_defect_rate=0.05, inspection_failure_rate=0.07,
            change_control_compliance_pct=0.42, root_cause_resolution_rate=0.60,
            customer_satisfaction_score=0.62, cost_of_quality_ratio=0.14,
            testing_coverage_pct=0.72, preventive_maintenance_score=0.70,
            documentation_completeness_pct=0.76,
        ),
        QualityInput(
            process_id="QA-008", process_type="service", region="MEA",
            defect_rate_pct=0.20, first_pass_yield_pct=0.58,
            customer_complaint_rate=0.22, rework_rate_pct=0.25,
            cycle_time_variance_pct=30, sla_breach_rate=0.12,
            audit_score=0.55, process_adherence_score=0.50,
            supplier_defect_rate=0.18, inspection_failure_rate=0.14,
            change_control_compliance_pct=0.60, root_cause_resolution_rate=0.40,
            customer_satisfaction_score=0.30, cost_of_quality_ratio=0.32,
            testing_coverage_pct=0.48, preventive_maintenance_score=0.42,
            documentation_completeness_pct=0.62,
        ),
    ]


if __name__ == "__main__":
    engine = QualityAssuranceProcessEngine()
    results = engine.assess_batch(_mock_processes())
    print("=== QualityAssuranceProcessEngine Smoke Test ===")
    for r in results:
        d = r.to_dict()
        assert len(d) == 15, f"Expected 15 keys, got {len(d)}"
        print(
            f"{r.process_id}  risk={r.quality_risk:<8}  pattern={r.quality_pattern:<25}"
            f"  composite={r.quality_composite:5.1f}  action={r.recommended_action}"
        )
    s = engine.summary()
    assert len(s) == 13, f"Expected 13 summary keys, got {len(s)}"
    print(f"\nSummary ({len(s)} keys): {s}")
    print("PASSED")
