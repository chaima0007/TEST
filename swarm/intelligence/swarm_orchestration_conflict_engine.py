"""
Module 239 — Swarm Orchestration & Conflict Resolution Engine
Detects and resolves coordination conflicts, deadlocks, cascade failures,
and communication breakdowns across multi-agent swarms.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class OrchestrationRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ConflictPattern(str, Enum):
    none                    = "none"
    resource_contention     = "resource_contention"
    goal_misalignment       = "goal_misalignment"
    communication_breakdown = "communication_breakdown"
    cascade_failure         = "cascade_failure"
    deadlock                = "deadlock"


class OrchestrationSeverity(str, Enum):
    harmonized = "harmonized"
    balanced   = "balanced"
    degraded   = "degraded"
    critical   = "critical"


class OrchestrationAction(str, Enum):
    no_action                      = "no_action"
    coordination_monitoring        = "coordination_monitoring"
    task_redistribution            = "task_redistribution"
    goal_realignment               = "goal_realignment"
    communication_protocol_update  = "communication_protocol_update"
    cascade_isolation              = "cascade_isolation"
    deadlock_resolution            = "deadlock_resolution"
    emergency_reorchestration      = "emergency_reorchestration"
    swarm_reset                    = "swarm_reset"


@dataclass
class OrchestrationInput:
    swarm_id: str
    swarm_type: str                          # sales/ops/finance/product/support
    region: str
    task_conflict_rate: float                # 0-1
    resource_contention_score: float         # 0-1
    goal_alignment_score: float              # 0-1, 1=perfectly aligned
    inter_agent_communication_latency_ms: int
    message_failure_rate: float              # 0-1
    agent_response_time_variance: float      # % variance
    deadlock_occurrence_count: int
    cascade_failure_risk_score: float        # 0-1
    coordination_overhead_pct: float         # 0-1
    task_duplication_rate: float             # 0-1
    role_overlap_score: float                # 0-1
    priority_conflict_count: int
    consensus_achievement_rate: float        # 0-1, 1=always reaches consensus
    autonomy_balance_score: float            # 0-1, 1=well-balanced
    workload_distribution_gini: float        # 0-1, 0=perfectly equal
    human_escalation_rate: float             # 0-1
    orchestration_efficiency_score: float    # 0-1, 1=optimal


@dataclass
class OrchestrationResult:
    swarm_id: str
    region: str
    orchestration_risk: str
    conflict_pattern: str
    orchestration_severity: str
    recommended_action: str
    conflict_score: float
    coordination_score: float
    efficiency_score: float
    resilience_score: float
    orchestration_composite: float
    has_orchestration_alert: bool
    requires_human_intervention: bool
    estimated_swarm_health_index: float
    orchestration_signal: str

    def to_dict(self) -> Dict:
        return {
            "swarm_id":                    self.swarm_id,
            "region":                      self.region,
            "orchestration_risk":          self.orchestration_risk,
            "conflict_pattern":            self.conflict_pattern,
            "orchestration_severity":      self.orchestration_severity,
            "recommended_action":          self.recommended_action,
            "conflict_score":              self.conflict_score,
            "coordination_score":          self.coordination_score,
            "efficiency_score":            self.efficiency_score,
            "resilience_score":            self.resilience_score,
            "orchestration_composite":     self.orchestration_composite,
            "has_orchestration_alert":     self.has_orchestration_alert,
            "requires_human_intervention": self.requires_human_intervention,
            "estimated_swarm_health_index": self.estimated_swarm_health_index,
            "orchestration_signal":        self.orchestration_signal,
        }


class SwarmOrchestrationConflictEngine:
    def __init__(self) -> None:
        self._results: List[OrchestrationResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _conflict_score(self, i: OrchestrationInput) -> float:
        s = 0
        if   i.task_conflict_rate >= 0.30: s += 40
        elif i.task_conflict_rate >= 0.15: s += 22
        elif i.task_conflict_rate >= 0.05: s += 8

        if   i.role_overlap_score >= 0.60: s += 35
        elif i.role_overlap_score >= 0.35: s += 18
        elif i.role_overlap_score >= 0.15: s += 6

        if   i.priority_conflict_count >= 10: s += 25
        elif i.priority_conflict_count >= 5:  s += 12
        elif i.priority_conflict_count >= 2:  s += 6
        return min(s, 100)

    def _coordination_score(self, i: OrchestrationInput) -> float:
        s = 0
        if   i.message_failure_rate >= 0.20: s += 40
        elif i.message_failure_rate >= 0.10: s += 22
        elif i.message_failure_rate >= 0.03: s += 8

        if   i.coordination_overhead_pct >= 0.40: s += 35
        elif i.coordination_overhead_pct >= 0.20: s += 18
        elif i.coordination_overhead_pct >= 0.08: s += 6

        if   i.consensus_achievement_rate <= 0.50: s += 25
        elif i.consensus_achievement_rate <= 0.70: s += 12
        return min(s, 100)

    def _efficiency_score(self, i: OrchestrationInput) -> float:
        s = 0
        if   i.task_duplication_rate >= 0.25: s += 40
        elif i.task_duplication_rate >= 0.12: s += 22
        elif i.task_duplication_rate >= 0.05: s += 8

        if   i.orchestration_efficiency_score <= 0.40: s += 35
        elif i.orchestration_efficiency_score <= 0.60: s += 18
        elif i.orchestration_efficiency_score <= 0.75: s += 6

        if   i.workload_distribution_gini >= 0.60: s += 25
        elif i.workload_distribution_gini >= 0.35: s += 12
        return min(s, 100)

    def _resilience_score(self, i: OrchestrationInput) -> float:
        s = 0
        if   i.deadlock_occurrence_count >= 3: s += 40
        elif i.deadlock_occurrence_count >= 1: s += 22

        if   i.cascade_failure_risk_score >= 0.60: s += 35
        elif i.cascade_failure_risk_score >= 0.35: s += 18
        elif i.cascade_failure_risk_score >= 0.15: s += 6

        if   i.human_escalation_rate >= 0.30: s += 25
        elif i.human_escalation_rate >= 0.15: s += 12
        return min(s, 100)

    def _composite(self, cf: float, co: float, ef: float, re: float) -> float:
        return min(round(cf * 0.30 + co * 0.25 + ef * 0.25 + re * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity                                                     #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> OrchestrationRisk:
        if c >= 60: return OrchestrationRisk.critical
        if c >= 40: return OrchestrationRisk.high
        if c >= 20: return OrchestrationRisk.moderate
        return OrchestrationRisk.low

    def _severity(self, c: float) -> OrchestrationSeverity:
        if c >= 60: return OrchestrationSeverity.critical
        if c >= 40: return OrchestrationSeverity.degraded
        if c >= 20: return OrchestrationSeverity.balanced
        return OrchestrationSeverity.harmonized

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: OrchestrationInput) -> ConflictPattern:
        if (i.deadlock_occurrence_count >= 2
                or (i.message_failure_rate >= 0.20
                    and i.consensus_achievement_rate <= 0.40)):
            return ConflictPattern.deadlock
        if (i.cascade_failure_risk_score >= 0.65
                or i.human_escalation_rate >= 0.35):
            return ConflictPattern.cascade_failure
        if (i.resource_contention_score >= 0.60
                and i.task_conflict_rate >= 0.25):
            return ConflictPattern.resource_contention
        if (i.goal_alignment_score <= 0.35
                or i.priority_conflict_count >= 8):
            return ConflictPattern.goal_misalignment
        if (i.message_failure_rate >= 0.18
                or i.inter_agent_communication_latency_ms >= 500):
            return ConflictPattern.communication_breakdown
        return ConflictPattern.none

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: OrchestrationRisk, pat: ConflictPattern) -> OrchestrationAction:
        if risk == OrchestrationRisk.critical:
            if pat == ConflictPattern.deadlock:        return OrchestrationAction.swarm_reset
            if pat == ConflictPattern.cascade_failure: return OrchestrationAction.emergency_reorchestration
            return OrchestrationAction.emergency_reorchestration
        if risk == OrchestrationRisk.high:
            if pat == ConflictPattern.deadlock:               return OrchestrationAction.deadlock_resolution
            if pat == ConflictPattern.cascade_failure:        return OrchestrationAction.cascade_isolation
            if pat == ConflictPattern.resource_contention:    return OrchestrationAction.task_redistribution
            if pat == ConflictPattern.goal_misalignment:      return OrchestrationAction.goal_realignment
            if pat == ConflictPattern.communication_breakdown: return OrchestrationAction.communication_protocol_update
            return OrchestrationAction.coordination_monitoring
        if risk == OrchestrationRisk.moderate:
            return OrchestrationAction.coordination_monitoring
        return OrchestrationAction.no_action

    # ------------------------------------------------------------------ #
    #  Derived booleans & indices                                          #
    # ------------------------------------------------------------------ #

    def _has_alert(self, i: OrchestrationInput, comp: float) -> bool:
        return (comp >= 40
                or i.deadlock_occurrence_count >= 1
                or i.cascade_failure_risk_score >= 0.55
                or i.task_conflict_rate >= 0.25)

    def _requires_human(self, i: OrchestrationInput, comp: float) -> bool:
        return (comp >= 25
                or i.deadlock_occurrence_count >= 2
                or i.human_escalation_rate >= 0.25
                or i.cascade_failure_risk_score >= 0.65)

    def _health_index(self, i: OrchestrationInput, comp: float) -> float:
        return round(min((1 - comp / 100) * i.orchestration_efficiency_score * 10, 10.0), 2)

    def _signal(self, i: OrchestrationInput, pat: ConflictPattern, comp: float) -> str:
        if comp < 20:
            return "Essaim bien orchestré — coordination fluide, aucun conflit, efficacité optimale"
        labels = {
            ConflictPattern.resource_contention:     "Contention ressources",
            ConflictPattern.goal_misalignment:       "Désalignement objectifs",
            ConflictPattern.communication_breakdown: "Rupture communication",
            ConflictPattern.cascade_failure:         "Défaillance en cascade",
            ConflictPattern.deadlock:                "Situation de blocage",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — conflit {i.task_conflict_rate * 100:.0f}%"
            f" — échec comm {i.message_failure_rate * 100:.0f}%"
            f" — deadlocks {i.deadlock_occurrence_count}"
            f" — composite {comp:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: OrchestrationInput) -> OrchestrationResult:
        cf   = self._conflict_score(i)
        co   = self._coordination_score(i)
        ef   = self._efficiency_score(i)
        re   = self._resilience_score(i)
        comp = self._composite(cf, co, ef, re)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = OrchestrationResult(
            swarm_id=i.swarm_id,
            region=i.region,
            orchestration_risk=risk.value,
            conflict_pattern=pat.value,
            orchestration_severity=sev.value,
            recommended_action=act.value,
            conflict_score=cf,
            coordination_score=co,
            efficiency_score=ef,
            resilience_score=re,
            orchestration_composite=comp,
            has_orchestration_alert=self._has_alert(i, comp),
            requires_human_intervention=self._requires_human(i, comp),
            estimated_swarm_health_index=self._health_index(i, comp),
            orchestration_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[OrchestrationInput]) -> List[OrchestrationResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_orchestration_composite": 0.0,
                "orchestration_alert_count": 0,
                "human_intervention_count": 0,
                "avg_conflict_score": 0.0,
                "avg_coordination_score": 0.0,
                "avg_efficiency_score": 0.0,
                "avg_resilience_score": 0.0,
                "avg_estimated_swarm_health_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tcf = tco = tef = tre = tcomp = thealth = 0.0
        alert_count = human_count = 0
        for r in self._results:
            rc[r.orchestration_risk]    = rc.get(r.orchestration_risk, 0)    + 1
            pc[r.conflict_pattern]      = pc.get(r.conflict_pattern, 0)      + 1
            sc[r.orchestration_severity]= sc.get(r.orchestration_severity, 0)+ 1
            ac[r.recommended_action]    = ac.get(r.recommended_action, 0)    + 1
            tcf    += r.conflict_score
            tco    += r.coordination_score
            tef    += r.efficiency_score
            tre    += r.resilience_score
            tcomp  += r.orchestration_composite
            thealth+= r.estimated_swarm_health_index
            if r.has_orchestration_alert:      alert_count += 1
            if r.requires_human_intervention:  human_count += 1
        return {
            "total":                             n,
            "risk_counts":                       rc,
            "pattern_counts":                    pc,
            "severity_counts":                   sc,
            "action_counts":                     ac,
            "avg_orchestration_composite":       round(tcomp / n, 1),
            "orchestration_alert_count":         alert_count,
            "human_intervention_count":          human_count,
            "avg_conflict_score":                round(tcf / n, 1),
            "avg_coordination_score":            round(tco / n, 1),
            "avg_efficiency_score":              round(tef / n, 1),
            "avg_resilience_score":              round(tre / n, 1),
            "avg_estimated_swarm_health_index":  round(thealth / n, 2),
        }
