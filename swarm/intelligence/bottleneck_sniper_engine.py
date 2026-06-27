"""Module 314 — Bottleneck Sniper System Constraint Intelligence Engine

Identifies and scores operational bottlenecks and system constraints using
Theory of Constraints (TOC) principles across flow, constraint exploitation,
system dynamics, and resilience dimensions.

Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


# ─── Input ────────────────────────────────────────────────────────────────────

@dataclass
class BottleneckSniperInput:
    entity_id: str
    system_type: str
    region: str
    # Flow metrics (all 0.0–1.0)
    throughput_reduction_rate: float
    constraint_utilization_excess: float
    queue_accumulation_rate: float
    resource_starvation_index: float
    batch_size_mismatch: float
    variability_amplification: float
    dependency_chain_fragility: float
    capacity_imbalance_index: float
    wip_explosion_risk: float
    policy_constraint_density: float
    market_constraint_severity: float
    inventory_buffer_gaps: float
    protective_capacity_deficit: float
    constraint_exploitation_gap: float   # how much constraint could be better used — high=bad
    subordination_failure_rate: float
    elevation_difficulty_index: float
    constraint_migration_velocity: float


# ─── Result ───────────────────────────────────────────────────────────────────

@dataclass
class BottleneckSniperResult:
    entity_id: str
    region: str
    system_type: str
    constraint_risk: str
    constraint_pattern: str
    constraint_severity: str
    recommended_action: str
    flow_score: float
    constraint_score: float
    system_score: float
    resilience_score: float
    constraint_composite: float
    is_constraint_crisis: bool
    requires_constraint_intervention: bool
    constraint_signal: str

    def to_dict(self) -> dict:
        return {
            "entity_id":                        self.entity_id,
            "region":                           self.region,
            "system_type":                      self.system_type,
            "constraint_risk":                  self.constraint_risk,
            "constraint_pattern":               self.constraint_pattern,
            "constraint_severity":              self.constraint_severity,
            "recommended_action":               self.recommended_action,
            "flow_score":                       self.flow_score,
            "constraint_score":                 self.constraint_score,
            "system_score":                     self.system_score,
            "resilience_score":                 self.resilience_score,
            "constraint_composite":             self.constraint_composite,
            "is_constraint_crisis":             self.is_constraint_crisis,
            "requires_constraint_intervention": self.requires_constraint_intervention,
            "constraint_signal":                self.constraint_signal,
        }


# ─── Scoring helpers ──────────────────────────────────────────────────────────

def _flow_score(inp: BottleneckSniperInput) -> float:
    """Flow degradation score — weight 0.30 in composite."""
    return (
        inp.throughput_reduction_rate * 0.40
        + inp.queue_accumulation_rate * 0.35
        + inp.wip_explosion_risk * 0.25
    ) * 100


def _constraint_score(inp: BottleneckSniperInput) -> float:
    """Constraint exploitation score — weight 0.25 in composite."""
    return (
        inp.constraint_utilization_excess * 0.40
        + inp.constraint_exploitation_gap * 0.35
        + inp.capacity_imbalance_index * 0.25
    ) * 100


def _system_score(inp: BottleneckSniperInput) -> float:
    """System dynamics score — weight 0.25 in composite."""
    return (
        inp.dependency_chain_fragility * 0.40
        + inp.variability_amplification * 0.35
        + inp.policy_constraint_density * 0.25
    ) * 100


def _resilience_score(inp: BottleneckSniperInput) -> float:
    """Resilience deficit score — weight 0.20 in composite."""
    return (
        inp.protective_capacity_deficit * 0.40
        + inp.inventory_buffer_gaps * 0.35
        + inp.resource_starvation_index * 0.25
    ) * 100


def _composite(fl: float, co: float, sy: float, re: float) -> float:
    return fl * 0.30 + co * 0.25 + sy * 0.25 + re * 0.20


def _risk(comp: float) -> str:
    if comp >= 60:
        return "critical"
    if comp >= 40:
        return "high"
    if comp >= 20:
        return "moderate"
    return "low"


def _pattern(inp: BottleneckSniperInput) -> str:
    if inp.throughput_reduction_rate >= 0.70 and inp.constraint_utilization_excess >= 0.65:
        return "critical_path_failure"
    if inp.policy_constraint_density >= 0.70 and inp.subordination_failure_rate >= 0.65:
        return "policy_constraint_dominance"
    if inp.market_constraint_severity >= 0.70 and inp.constraint_exploitation_gap >= 0.65:
        return "market_constraint_crisis"
    if inp.wip_explosion_risk >= 0.70 and inp.queue_accumulation_rate >= 0.65:
        return "wip_catastrophe"
    if inp.resource_starvation_index >= 0.70 and inp.dependency_chain_fragility >= 0.65:
        return "cascade_starvation"
    return "none"


def _severity(comp: float) -> str:
    if comp >= 75:
        return "system_halt"
    if comp >= 50:
        return "critical_constraint"
    if comp >= 25:
        return "constraint_building"
    return "flow_optimal"


def _action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "emergency_constraint_bypass"
    if risk == "high" and pattern == "policy_constraint_dominance":
        return "policy_redesign"
    if risk == "high":
        return "constraint_exploitation_program"
    if risk == "moderate":
        return "bottleneck_monitoring"
    return "no_action"


def _signal(inp: BottleneckSniperInput, pattern: str, comp: float) -> str:
    if comp < 20:
        return (
            "Flux système optimal — contraintes bien gérées, débit préservé, "
            "aucune intervention requise"
        )
    pattern_labels: dict[str, str] = {
        "critical_path_failure":      "Défaillance du chemin critique",
        "policy_constraint_dominance": "Dominance des contraintes de politique",
        "market_constraint_crisis":   "Crise de contrainte marché",
        "wip_catastrophe":            "Catastrophe WIP en cours",
        "cascade_starvation":         "Carence en cascade détectée",
    }
    label = pattern_labels.get(pattern, pattern.replace("_", " ").capitalize())
    return (
        f"{label} — débit réduit {round(inp.throughput_reduction_rate * 100)}% — "
        f"WIP explosion {round(inp.wip_explosion_risk * 100)}% — "
        f"file d'attente {round(inp.queue_accumulation_rate * 100)}% — "
        f"composite {round(comp)}"
    )


# ─── Engine ───────────────────────────────────────────────────────────────────

class BottleneckSniperEngine:
    """Analyze a batch of entities for system constraint risk."""

    def analyze_one(self, inp: BottleneckSniperInput) -> BottleneckSniperResult:
        fl = round(_flow_score(inp), 2)
        co = round(_constraint_score(inp), 2)
        sy = round(_system_score(inp), 2)
        re = round(_resilience_score(inp), 2)
        comp = round(_composite(fl, co, sy, re), 2)
        risk = _risk(comp)
        pattern = _pattern(inp)
        severity = _severity(comp)
        action = _action(risk, pattern)
        signal = _signal(inp, pattern, comp)

        return BottleneckSniperResult(
            entity_id=inp.entity_id,
            region=inp.region,
            system_type=inp.system_type,
            constraint_risk=risk,
            constraint_pattern=pattern,
            constraint_severity=severity,
            recommended_action=action,
            flow_score=fl,
            constraint_score=co,
            system_score=sy,
            resilience_score=re,
            constraint_composite=comp,
            is_constraint_crisis=comp >= 60,
            requires_constraint_intervention=comp >= 40,
            constraint_signal=signal,
        )

    def analyze(self, entities: list[BottleneckSniperInput]) -> dict:
        results = [self.analyze_one(e) for e in entities]

        total = len(results)
        critical_count  = sum(1 for r in results if r.constraint_risk == "critical")
        high_count      = sum(1 for r in results if r.constraint_risk == "high")
        moderate_count  = sum(1 for r in results if r.constraint_risk == "moderate")
        low_count       = sum(1 for r in results if r.constraint_risk == "low")

        crisis_count       = sum(1 for r in results if r.is_constraint_crisis)
        intervention_count = sum(1 for r in results if r.requires_constraint_intervention)

        # Dominant pattern (most frequent, excluding "none")
        pattern_counts: dict[str, int] = {}
        for r in results:
            pattern_counts[r.constraint_pattern] = pattern_counts.get(r.constraint_pattern, 0) + 1
        non_none = {k: v for k, v in pattern_counts.items() if k != "none"}
        dominant_pattern = max(non_none, key=lambda k: non_none[k]) if non_none else "none"

        avg_flow       = round(sum(r.flow_score       for r in results) / total, 2) if total else 0.0
        avg_constraint = round(sum(r.constraint_score for r in results) / total, 2) if total else 0.0
        avg_system     = round(sum(r.system_score     for r in results) / total, 2) if total else 0.0
        avg_resilience = round(sum(r.resilience_score for r in results) / total, 2) if total else 0.0
        avg_composite  = round(sum(r.constraint_composite for r in results) / total, 2) if total else 0.0

        return {
            "total_entities":               total,
            "critical_count":               critical_count,
            "high_count":                   high_count,
            "moderate_count":               moderate_count,
            "low_count":                    low_count,
            "crisis_entities":              crisis_count,
            "intervention_required":        intervention_count,
            "dominant_pattern":             dominant_pattern,
            "avg_flow_score":               avg_flow,
            "avg_constraint_score":         avg_constraint,
            "avg_system_score":             avg_system,
            "avg_resilience_score":         avg_resilience,
            "avg_constraint_composite":     avg_composite,
            "avg_estimated_constraint_index": round(avg_composite / 100 * 10, 2),
        }
