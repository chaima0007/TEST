"""
Module 240 — Continuous Improvement & Operational Excellence Engine
Monitors operational improvement initiatives, detects stagnation patterns,
and recommends targeted actions to maintain excellence trajectories.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class ImprovementRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ImprovementPattern(str, Enum):
    none               = "none"
    process_stagnation = "process_stagnation"
    waste_accumulation = "waste_accumulation"
    innovation_deficit = "innovation_deficit"
    kpi_degradation    = "kpi_degradation"
    change_fatigue     = "change_fatigue"


class ImprovementSeverity(str, Enum):
    excellent   = "excellent"
    progressing = "progressing"
    stagnating  = "stagnating"
    declining   = "declining"


class ImprovementAction(str, Enum):
    no_action              = "no_action"
    improvement_monitoring = "improvement_monitoring"
    kaizen_initiative      = "kaizen_initiative"
    lean_review            = "lean_review"
    kpi_reset              = "kpi_reset"
    innovation_sprint      = "innovation_sprint"
    change_management      = "change_management"
    process_reengineering  = "process_reengineering"
    transformation_program = "transformation_program"


@dataclass
class ImprovementInput:
    initiative_id: str
    business_unit: str
    region: str
    process_efficiency_trend: float          # -1 to 1, positive=improving
    waste_reduction_pct: float               # 0-1, 1=fully reduced
    cycle_time_improvement_pct: float        # % improvement
    rework_elimination_rate: float           # 0-1
    innovation_idea_adoption_rate: float     # 0-1
    kpi_attainment_rate: float               # 0-1, 1=all KPIs met
    continuous_improvement_engagement_score: float  # 0-1
    lean_methodology_adherence: float        # 0-1
    change_adoption_velocity: float          # 0-1
    retrospective_action_completion: float   # 0-1, 1=all actions done
    cross_functional_collaboration_score: float  # 0-1
    customer_feedback_integration_score: float   # 0-1
    automation_adoption_rate: float          # 0-1
    benchmark_performance_gap: float         # 0-1, 1=large gap vs benchmark
    employee_improvement_suggestion_rate: float  # 0-1
    measurement_system_maturity: float       # 0-1, 1=mature
    standardization_compliance_pct: float    # 0-1


@dataclass
class ImprovementResult:
    initiative_id: str
    region: str
    improvement_risk: str
    improvement_pattern: str
    improvement_severity: str
    recommended_action: str
    process_score: float
    innovation_score: float
    execution_score: float
    maturity_score: float
    improvement_composite: float
    has_stagnation_signal: bool
    requires_transformation: bool
    estimated_improvement_gap_index: float
    improvement_signal: str

    def to_dict(self) -> Dict:
        return {
            "initiative_id":                   self.initiative_id,
            "region":                          self.region,
            "improvement_risk":                self.improvement_risk,
            "improvement_pattern":             self.improvement_pattern,
            "improvement_severity":            self.improvement_severity,
            "recommended_action":              self.recommended_action,
            "process_score":                   self.process_score,
            "innovation_score":                self.innovation_score,
            "execution_score":                 self.execution_score,
            "maturity_score":                  self.maturity_score,
            "improvement_composite":           self.improvement_composite,
            "has_stagnation_signal":           self.has_stagnation_signal,
            "requires_transformation":         self.requires_transformation,
            "estimated_improvement_gap_index": self.estimated_improvement_gap_index,
            "improvement_signal":              self.improvement_signal,
        }


class ContinuousImprovementExcellenceEngine:
    def __init__(self) -> None:
        self._results: List[ImprovementResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _process_score(self, i: ImprovementInput) -> float:
        s = 0
        if   i.process_efficiency_trend <= -0.1: s += 40
        elif i.process_efficiency_trend <= 0:    s += 22
        elif i.process_efficiency_trend <= 0.1:  s += 8

        if   i.waste_reduction_pct <= 0.20: s += 35
        elif i.waste_reduction_pct <= 0.40: s += 18
        elif i.waste_reduction_pct <= 0.60: s += 6

        if   i.rework_elimination_rate <= 0.30: s += 25
        elif i.rework_elimination_rate <= 0.55: s += 12
        return min(s, 100)

    def _innovation_score(self, i: ImprovementInput) -> float:
        s = 0
        if   i.innovation_idea_adoption_rate <= 0.20: s += 40
        elif i.innovation_idea_adoption_rate <= 0.40: s += 22
        elif i.innovation_idea_adoption_rate <= 0.60: s += 8

        if   i.automation_adoption_rate <= 0.20: s += 35
        elif i.automation_adoption_rate <= 0.40: s += 18
        elif i.automation_adoption_rate <= 0.60: s += 6

        if   i.benchmark_performance_gap >= 0.55: s += 25
        elif i.benchmark_performance_gap >= 0.35: s += 12
        return min(s, 100)

    def _execution_score(self, i: ImprovementInput) -> float:
        s = 0
        if   i.retrospective_action_completion <= 0.40: s += 40
        elif i.retrospective_action_completion <= 0.60: s += 22
        elif i.retrospective_action_completion <= 0.75: s += 8

        if   i.kpi_attainment_rate <= 0.50: s += 35
        elif i.kpi_attainment_rate <= 0.65: s += 18
        elif i.kpi_attainment_rate <= 0.80: s += 6

        if   i.change_adoption_velocity <= 0.30: s += 25
        elif i.change_adoption_velocity <= 0.50: s += 12
        return min(s, 100)

    def _maturity_score(self, i: ImprovementInput) -> float:
        s = 0
        if   i.lean_methodology_adherence <= 0.30: s += 40
        elif i.lean_methodology_adherence <= 0.55: s += 22
        elif i.lean_methodology_adherence <= 0.70: s += 8

        if   i.measurement_system_maturity <= 0.30: s += 35
        elif i.measurement_system_maturity <= 0.55: s += 18
        elif i.measurement_system_maturity <= 0.70: s += 6

        if   i.standardization_compliance_pct <= 0.50: s += 25
        elif i.standardization_compliance_pct <= 0.70: s += 12
        return min(s, 100)

    def _composite(self, pr: float, inn: float, ex: float, mat: float) -> float:
        return min(round(pr * 0.30 + inn * 0.25 + ex * 0.25 + mat * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity                                                     #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> ImprovementRisk:
        if c >= 60: return ImprovementRisk.critical
        if c >= 40: return ImprovementRisk.high
        if c >= 20: return ImprovementRisk.moderate
        return ImprovementRisk.low

    def _severity(self, c: float) -> ImprovementSeverity:
        if c >= 60: return ImprovementSeverity.declining
        if c >= 40: return ImprovementSeverity.stagnating
        if c >= 20: return ImprovementSeverity.progressing
        return ImprovementSeverity.excellent

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: ImprovementInput) -> ImprovementPattern:
        if (i.process_efficiency_trend <= 0
                and i.waste_reduction_pct <= 0.30):
            return ImprovementPattern.process_stagnation
        if (i.rework_elimination_rate <= 0.25
                or i.waste_reduction_pct <= 0.20):
            return ImprovementPattern.waste_accumulation
        if (i.innovation_idea_adoption_rate <= 0.25
                and i.automation_adoption_rate <= 0.25):
            return ImprovementPattern.innovation_deficit
        if (i.kpi_attainment_rate <= 0.50
                or i.retrospective_action_completion <= 0.35):
            return ImprovementPattern.kpi_degradation
        if (i.change_adoption_velocity <= 0.25
                and i.continuous_improvement_engagement_score <= 0.40):
            return ImprovementPattern.change_fatigue
        return ImprovementPattern.none

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: ImprovementRisk, pat: ImprovementPattern) -> ImprovementAction:
        if risk == ImprovementRisk.critical:
            if pat == ImprovementPattern.process_stagnation: return ImprovementAction.transformation_program
            if pat == ImprovementPattern.kpi_degradation:    return ImprovementAction.process_reengineering
            return ImprovementAction.change_management
        if risk == ImprovementRisk.high:
            if pat == ImprovementPattern.process_stagnation: return ImprovementAction.process_reengineering
            if pat == ImprovementPattern.waste_accumulation: return ImprovementAction.lean_review
            if pat == ImprovementPattern.innovation_deficit: return ImprovementAction.innovation_sprint
            if pat == ImprovementPattern.kpi_degradation:    return ImprovementAction.kpi_reset
            if pat == ImprovementPattern.change_fatigue:     return ImprovementAction.change_management
            return ImprovementAction.kaizen_initiative
        if risk == ImprovementRisk.moderate:
            return ImprovementAction.improvement_monitoring
        return ImprovementAction.no_action

    # ------------------------------------------------------------------ #
    #  Derived booleans & indices                                          #
    # ------------------------------------------------------------------ #

    def _has_stagnation(self, i: ImprovementInput, comp: float) -> bool:
        return (comp >= 40
                or i.process_efficiency_trend <= 0
                or i.kpi_attainment_rate <= 0.55
                or i.waste_reduction_pct <= 0.25)

    def _requires_transformation(self, i: ImprovementInput, comp: float) -> bool:
        return (comp >= 25
                or i.benchmark_performance_gap >= 0.50
                or i.retrospective_action_completion <= 0.35
                or i.lean_methodology_adherence <= 0.30)

    def _gap_index(self, i: ImprovementInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.measurement_system_maturity + 0.01) * 10, 10.0), 2)

    def _signal(self, i: ImprovementInput, pat: ImprovementPattern, comp: float) -> str:
        if comp < 20:
            return "Excellence opérationnelle forte — amélioration continue active, KPIs atteints, innovation en cours"
        labels = {
            ImprovementPattern.process_stagnation: "Stagnation process",
            ImprovementPattern.waste_accumulation: "Accumulation déchets",
            ImprovementPattern.innovation_deficit: "Déficit innovation",
            ImprovementPattern.kpi_degradation:    "Dégradation KPIs",
            ImprovementPattern.change_fatigue:     "Fatigue du changement",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — trend process {i.process_efficiency_trend:+.2f}"
            f" — KPIs {i.kpi_attainment_rate * 100:.0f}%"
            f" — adoption inn. {i.innovation_idea_adoption_rate * 100:.0f}%"
            f" — composite {comp:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: ImprovementInput) -> ImprovementResult:
        pr   = self._process_score(i)
        inn  = self._innovation_score(i)
        ex   = self._execution_score(i)
        mat  = self._maturity_score(i)
        comp = self._composite(pr, inn, ex, mat)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = ImprovementResult(
            initiative_id=i.initiative_id,
            region=i.region,
            improvement_risk=risk.value,
            improvement_pattern=pat.value,
            improvement_severity=sev.value,
            recommended_action=act.value,
            process_score=pr,
            innovation_score=inn,
            execution_score=ex,
            maturity_score=mat,
            improvement_composite=comp,
            has_stagnation_signal=self._has_stagnation(i, comp),
            requires_transformation=self._requires_transformation(i, comp),
            estimated_improvement_gap_index=self._gap_index(i, comp),
            improvement_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ImprovementInput]) -> List[ImprovementResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_improvement_composite": 0.0,
                "stagnation_signal_count": 0,
                "transformation_required_count": 0,
                "avg_process_score": 0.0,
                "avg_innovation_score": 0.0,
                "avg_execution_score": 0.0,
                "avg_maturity_score": 0.0,
                "avg_estimated_improvement_gap_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tpr = tinn = tex = tmat = tcomp = tgap = 0.0
        stag_count = transf_count = 0
        for r in self._results:
            rc[r.improvement_risk]     = rc.get(r.improvement_risk, 0)     + 1
            pc[r.improvement_pattern]  = pc.get(r.improvement_pattern, 0)  + 1
            sc[r.improvement_severity] = sc.get(r.improvement_severity, 0) + 1
            ac[r.recommended_action]   = ac.get(r.recommended_action, 0)   + 1
            tpr   += r.process_score
            tinn  += r.innovation_score
            tex   += r.execution_score
            tmat  += r.maturity_score
            tcomp += r.improvement_composite
            tgap  += r.estimated_improvement_gap_index
            if r.has_stagnation_signal:   stag_count   += 1
            if r.requires_transformation: transf_count += 1
        return {
            "total":                              n,
            "risk_counts":                        rc,
            "pattern_counts":                     pc,
            "severity_counts":                    sc,
            "action_counts":                      ac,
            "avg_improvement_composite":          round(tcomp / n, 1),
            "stagnation_signal_count":            stag_count,
            "transformation_required_count":      transf_count,
            "avg_process_score":                  round(tpr / n, 1),
            "avg_innovation_score":               round(tinn / n, 1),
            "avg_execution_score":                round(tex / n, 1),
            "avg_maturity_score":                 round(tmat / n, 1),
            "avg_estimated_improvement_gap_index": round(tgap / n, 2),
        }
