"""
Module 235 — Resource Optimization & Capacity Planning Engine
Evaluates human, tech, financial and physical resources for overload, capacity gaps,
allocation imbalances, efficiency constraints and utilisation inefficiencies — then
recommends the appropriate operational or strategic response.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class ResourceRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CapacityPattern(str, Enum):
    none                    = "none"
    resource_overload       = "resource_overload"
    capacity_gap            = "capacity_gap"
    allocation_imbalance    = "allocation_imbalance"
    utilization_inefficiency = "utilization_inefficiency"
    constraint_bottleneck   = "constraint_bottleneck"


class ResourceSeverity(str, Enum):
    optimal  = "optimal"
    balanced = "balanced"
    strained = "strained"
    critical = "critical"


class ResourceAction(str, Enum):
    no_action                 = "no_action"
    utilization_monitoring    = "utilization_monitoring"
    reallocation_plan         = "reallocation_plan"
    capacity_expansion        = "capacity_expansion"
    constraint_resolution     = "constraint_resolution"
    load_balancing            = "load_balancing"
    emergency_redeployment    = "emergency_redeployment"
    workforce_restructuring   = "workforce_restructuring"
    strategic_capacity_review = "strategic_capacity_review"


@dataclass
class ResourceInput:
    resource_id: str
    resource_type: str                      # human / tech / financial / physical
    region: str
    utilization_rate: float                 # 0-1
    capacity_headroom_pct: float            # 0-1, 1 = lots of room
    overallocation_score: float             # 0-1
    skill_coverage_gap_score: float         # 0-1, 1 = large gap
    demand_forecast_variance_pct: float     # % deviation
    burnout_risk_score: float               # 0-1
    absenteeism_rate: float                 # 0-1
    throughput_efficiency_score: float      # 0-1, 1 = optimal
    bottleneck_severity_score: float        # 0-1
    resource_flexibility_score: float       # 0-1, 1 = flexible
    cross_training_coverage_pct: float      # 0-1
    tech_utilization_pct: float             # 0-1
    idle_resource_pct: float                # 0-1
    peak_demand_coverage_score: float       # 0-1, 1 = fully covered
    succession_readiness_score: float       # 0-1, 1 = ready
    contractor_dependency_pct: float        # 0-1
    planning_horizon_days: int


@dataclass
class ResourceResult:
    resource_id: str
    region: str
    resource_risk: str
    capacity_pattern: str
    resource_severity: str
    recommended_action: str
    utilization_score: float
    allocation_score: float
    efficiency_score: float
    planning_score: float
    resource_composite: float
    has_capacity_alert: bool
    requires_strategic_review: bool
    estimated_capacity_gap_index: float
    resource_signal: str

    def to_dict(self) -> Dict:
        return {
            "resource_id":                    self.resource_id,
            "region":                         self.region,
            "resource_risk":                  self.resource_risk,
            "capacity_pattern":               self.capacity_pattern,
            "resource_severity":              self.resource_severity,
            "recommended_action":             self.recommended_action,
            "utilization_score":              self.utilization_score,
            "allocation_score":               self.allocation_score,
            "efficiency_score":               self.efficiency_score,
            "planning_score":                 self.planning_score,
            "resource_composite":             self.resource_composite,
            "has_capacity_alert":             self.has_capacity_alert,
            "requires_strategic_review":      self.requires_strategic_review,
            "estimated_capacity_gap_index":   self.estimated_capacity_gap_index,
            "resource_signal":                self.resource_signal,
        }


class ResourceOptimizationCapacityEngine:
    def __init__(self) -> None:
        self._results: List[ResourceResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _utilization_score(self, i: ResourceInput) -> float:
        s = 0
        if   i.overallocation_score >= 0.80: s += 40
        elif i.overallocation_score >= 0.55: s += 22
        elif i.overallocation_score >= 0.30: s += 8

        if   i.utilization_rate >= 0.95: s += 30
        elif i.utilization_rate >= 0.80: s += 16
        elif i.utilization_rate >= 0.65: s += 6

        if   i.burnout_risk_score >= 0.70: s += 30
        elif i.burnout_risk_score >= 0.40: s += 14
        return min(s, 100)

    def _allocation_score(self, i: ResourceInput) -> float:
        s = 0
        if   i.skill_coverage_gap_score >= 0.60: s += 40
        elif i.skill_coverage_gap_score >= 0.35: s += 22
        elif i.skill_coverage_gap_score >= 0.15: s += 8

        if   i.idle_resource_pct >= 0.30: s += 35
        elif i.idle_resource_pct >= 0.15: s += 18
        elif i.idle_resource_pct >= 0.05: s += 6

        if   i.contractor_dependency_pct >= 0.60: s += 25
        elif i.contractor_dependency_pct >= 0.35: s += 12
        return min(s, 100)

    def _efficiency_score(self, i: ResourceInput) -> float:
        s = 0
        if   i.throughput_efficiency_score <= 0.40: s += 40
        elif i.throughput_efficiency_score <= 0.65: s += 22
        elif i.throughput_efficiency_score <= 0.80: s += 8

        if   i.bottleneck_severity_score >= 0.70: s += 35
        elif i.bottleneck_severity_score >= 0.40: s += 18
        elif i.bottleneck_severity_score >= 0.20: s += 6

        if   i.tech_utilization_pct <= 0.40: s += 25
        elif i.tech_utilization_pct <= 0.65: s += 12
        return min(s, 100)

    def _planning_score(self, i: ResourceInput) -> float:
        s = 0
        if   i.demand_forecast_variance_pct >= 40: s += 40
        elif i.demand_forecast_variance_pct >= 20: s += 22
        elif i.demand_forecast_variance_pct >= 10: s += 8

        if   i.peak_demand_coverage_score <= 0.40: s += 35
        elif i.peak_demand_coverage_score <= 0.65: s += 18
        elif i.peak_demand_coverage_score <= 0.80: s += 6

        if   i.succession_readiness_score <= 0.30: s += 25
        elif i.succession_readiness_score <= 0.55: s += 12
        return min(s, 100)

    def _composite(self, util: float, alloc: float, eff: float, plan: float) -> float:
        return min(round(util * 0.30 + alloc * 0.25 + eff * 0.25 + plan * 0.20, 2), 100.0)

    def _risk(self, c: float) -> ResourceRisk:
        if c >= 60: return ResourceRisk.critical
        if c >= 40: return ResourceRisk.high
        if c >= 20: return ResourceRisk.moderate
        return ResourceRisk.low

    def _severity(self, c: float) -> ResourceSeverity:
        if c >= 60: return ResourceSeverity.critical
        if c >= 40: return ResourceSeverity.strained
        if c >= 20: return ResourceSeverity.balanced
        return ResourceSeverity.optimal

    def _pattern(self, i: ResourceInput) -> CapacityPattern:
        if i.utilization_rate >= 0.95 or i.overallocation_score >= 0.75:
            return CapacityPattern.resource_overload
        if i.skill_coverage_gap_score >= 0.50 or i.peak_demand_coverage_score <= 0.40:
            return CapacityPattern.capacity_gap
        if i.idle_resource_pct >= 0.20 and i.utilization_rate >= 0.80:
            return CapacityPattern.allocation_imbalance
        if i.throughput_efficiency_score <= 0.45 or i.bottleneck_severity_score >= 0.60:
            return CapacityPattern.constraint_bottleneck
        if i.tech_utilization_pct <= 0.45 or i.contractor_dependency_pct >= 0.55:
            return CapacityPattern.utilization_inefficiency
        return CapacityPattern.none

    def _action(self, risk: ResourceRisk, pat: CapacityPattern) -> ResourceAction:
        if risk == ResourceRisk.critical:
            if pat == CapacityPattern.resource_overload:
                return ResourceAction.emergency_redeployment
            if pat == CapacityPattern.capacity_gap:
                return ResourceAction.strategic_capacity_review
            return ResourceAction.workforce_restructuring
        if risk == ResourceRisk.high:
            if pat == CapacityPattern.resource_overload:
                return ResourceAction.load_balancing
            if pat == CapacityPattern.capacity_gap:
                return ResourceAction.capacity_expansion
            if pat == CapacityPattern.constraint_bottleneck:
                return ResourceAction.constraint_resolution
            if pat == CapacityPattern.allocation_imbalance:
                return ResourceAction.reallocation_plan
            return ResourceAction.utilization_monitoring
        if risk == ResourceRisk.moderate:
            return ResourceAction.utilization_monitoring
        return ResourceAction.no_action

    def _has_capacity_alert(self, i: ResourceInput, comp: float) -> bool:
        return (
            comp >= 40
            or i.utilization_rate >= 0.90
            or i.overallocation_score >= 0.70
            or i.skill_coverage_gap_score >= 0.50
        )

    def _requires_strategic_review(self, i: ResourceInput, comp: float) -> bool:
        return (
            comp >= 25
            or i.demand_forecast_variance_pct >= 30
            or i.succession_readiness_score <= 0.30
            or i.peak_demand_coverage_score <= 0.40
        )

    def _capacity_gap_index(self, i: ResourceInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.resource_flexibility_score + 0.01) * 10, 10.0), 2)

    def _signal(self, i: ResourceInput, pat: CapacityPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Ressources optimales — capacité équilibrée, pas de surcharge détectée"
            )
        labels: Dict[CapacityPattern, str] = {
            CapacityPattern.resource_overload:        "Surcharge ressources",
            CapacityPattern.capacity_gap:             "Écart de capacité",
            CapacityPattern.allocation_imbalance:     "Déséquilibre d'allocation",
            CapacityPattern.constraint_bottleneck:    "Goulot d'étranglement",
            CapacityPattern.utilization_inefficiency: "Inefficacité d'utilisation",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — "
            f"util. {i.utilization_rate * 100:.0f}% — "
            f"gap compétences {i.skill_coverage_gap_score * 100:.0f}% — "
            f"couverture pointe {i.peak_demand_coverage_score * 100:.0f}% — "
            f"composite {comp:.0f}"
        )

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, i: ResourceInput) -> ResourceResult:
        util  = self._utilization_score(i)
        alloc = self._allocation_score(i)
        eff   = self._efficiency_score(i)
        plan  = self._planning_score(i)
        comp  = self._composite(util, alloc, eff, plan)
        risk  = self._risk(comp)
        sev   = self._severity(comp)
        pat   = self._pattern(i)
        act   = self._action(risk, pat)
        result = ResourceResult(
            resource_id=i.resource_id,
            region=i.region,
            resource_risk=risk.value,
            capacity_pattern=pat.value,
            resource_severity=sev.value,
            recommended_action=act.value,
            utilization_score=util,
            allocation_score=alloc,
            efficiency_score=eff,
            planning_score=plan,
            resource_composite=comp,
            has_capacity_alert=self._has_capacity_alert(i, comp),
            requires_strategic_review=self._requires_strategic_review(i, comp),
            estimated_capacity_gap_index=self._capacity_gap_index(i, comp),
            resource_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ResourceInput]) -> List[ResourceResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total":                            0,
                "risk_counts":                      {},
                "pattern_counts":                   {},
                "severity_counts":                  {},
                "action_counts":                    {},
                "avg_resource_composite":           0.0,
                "capacity_alert_count":             0,
                "strategic_review_count":           0,
                "avg_utilization_score":            0.0,
                "avg_allocation_score":             0.0,
                "avg_efficiency_score":             0.0,
                "avg_planning_score":               0.0,
                "avg_estimated_capacity_gap_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tutil = talloc = teff = tplan = tcomp = tgap = 0.0
        alert_c = review_c = 0
        for r in self._results:
            rc[r.resource_risk]         = rc.get(r.resource_risk, 0)         + 1
            pc[r.capacity_pattern]      = pc.get(r.capacity_pattern, 0)      + 1
            sc[r.resource_severity]     = sc.get(r.resource_severity, 0)     + 1
            ac[r.recommended_action]    = ac.get(r.recommended_action, 0)    + 1
            tutil  += r.utilization_score
            talloc += r.allocation_score
            teff   += r.efficiency_score
            tplan  += r.planning_score
            tcomp  += r.resource_composite
            tgap   += r.estimated_capacity_gap_index
            if r.has_capacity_alert:        alert_c  += 1
            if r.requires_strategic_review: review_c += 1
        return {
            "total":                            n,
            "risk_counts":                      rc,
            "pattern_counts":                   pc,
            "severity_counts":                  sc,
            "action_counts":                    ac,
            "avg_resource_composite":           round(tcomp  / n, 1),
            "capacity_alert_count":             alert_c,
            "strategic_review_count":           review_c,
            "avg_utilization_score":            round(tutil  / n, 1),
            "avg_allocation_score":             round(talloc / n, 1),
            "avg_efficiency_score":             round(teff   / n, 1),
            "avg_planning_score":               round(tplan  / n, 1),
            "avg_estimated_capacity_gap_index": round(tgap   / n, 2),
        }
