from dataclasses import dataclass
from typing import Literal


@dataclass
class SwarmNodeInput:
    node_id: str
    node_role: Literal[
        "analyst_agent",
        "strategy_agent",
        "risk_agent",
        "legal_agent",
        "financial_agent",
        "market_agent",
        "governance_agent",
        "meta_orchestrator",
    ]
    region: str
    consensus_alignment_score: float = 0.0
    inter_agent_coherence: float = 0.0
    swarm_synchrony_index: float = 0.0
    emergent_intelligence_score: float = 0.0
    collective_decision_quality: float = 0.0
    agent_diversity_coefficient: float = 0.0
    information_redundancy_risk: float = 0.0
    swarm_drift_detection_score: float = 0.0
    meta_learning_velocity: float = 0.0
    conflict_resolution_efficiency: float = 0.0
    collective_memory_integrity: float = 0.0
    swarm_resilience_score: float = 0.0
    distributed_reasoning_clarity: float = 0.0
    cross_agent_trust_level: float = 0.0
    orchestration_overhead_ratio: float = 0.0
    collective_creativity_index: float = 0.0
    swarm_convergence_speed: float = 0.0


class _SwarmAssessment:
    def __init__(self, node: SwarmNodeInput):
        self.node = node
        self._compute()

    def _compute(self):
        n = self.node

        # Sub-scores (higher = worse / more risk)
        self.coherence_score = round(
            (
                (1 - n.inter_agent_coherence)
                + (1 - n.swarm_synchrony_index)
                + n.swarm_drift_detection_score
            )
            / 3,
            10,
        )

        self.intelligence_score = round(
            (
                (1 - n.emergent_intelligence_score)
                + (1 - n.collective_decision_quality)
                + (1 - n.meta_learning_velocity)
            )
            / 3,
            10,
        )

        self.consensus_score = round(
            (
                (1 - n.consensus_alignment_score)
                + (1 - n.conflict_resolution_efficiency)
                + (1 - n.cross_agent_trust_level)
            )
            / 3,
            10,
        )

        self.resilience_score = round(
            (
                (1 - n.swarm_resilience_score)
                + (1 - n.collective_memory_integrity)
                + n.information_redundancy_risk
            )
            / 3,
            10,
        )

        raw_composite = (
            self.coherence_score * 0.30
            + self.intelligence_score * 0.25
            + self.consensus_score * 0.25
            + self.resilience_score * 0.20
        )
        self.swarm_composite = round(min(raw_composite, 1.0), 2)

        # Pattern detection (checked in order)
        if n.inter_agent_coherence <= 0.25 and n.swarm_synchrony_index <= 0.25:
            self.swarm_pattern = "swarm_fragmentation"
        elif n.consensus_alignment_score <= 0.30 and n.conflict_resolution_efficiency <= 0.30:
            self.swarm_pattern = "consensus_deadlock"
        elif n.swarm_drift_detection_score >= 0.65:
            self.swarm_pattern = "emergent_drift"
        elif n.collective_memory_integrity <= 0.25:
            self.swarm_pattern = "collective_amnesia"
        elif n.orchestration_overhead_ratio >= 0.70:
            self.swarm_pattern = "orchestration_collapse"
        else:
            self.swarm_pattern = "none"

        # Severity
        c = self.swarm_composite
        if c >= 0.60:
            self.swarm_severity = "disintegrated"
        elif c >= 0.40:
            self.swarm_severity = "drifting"
        elif c >= 0.20:
            self.swarm_severity = "synchronizing"
        else:
            self.swarm_severity = "unified"

        # Risk level
        if c >= 0.60:
            self.swarm_risk = "critical"
        elif c >= 0.40:
            self.swarm_risk = "high"
        elif c >= 0.20:
            self.swarm_risk = "moderate"
        else:
            self.swarm_risk = "low"

        # Recommended action
        pat = self.swarm_pattern
        risk = self.swarm_risk
        if risk == "critical" and pat in ("swarm_fragmentation", "orchestration_collapse"):
            self.recommended_action = "emergency_swarm_reset"
        elif risk == "critical":
            self.recommended_action = "orchestration_override"
        elif risk == "high" and pat in ("consensus_deadlock", "emergent_drift"):
            self.recommended_action = "consensus_protocol_refresh"
        elif risk == "high":
            self.recommended_action = "diversity_rebalancing"
        elif risk == "moderate":
            self.recommended_action = "swarm_monitoring"
        else:
            self.recommended_action = "no_action"

        # Boolean flags
        self.has_fragmentation_signal = (
            c >= 0.40
            or n.swarm_drift_detection_score >= 0.50
            or n.inter_agent_coherence <= 0.30
        )
        self.requires_emergency_reset = (
            c >= 0.25
            or n.orchestration_overhead_ratio >= 0.60
            or n.consensus_alignment_score <= 0.30
        )

        # French signal string
        coh_pct = round((1 - self.coherence_score) * 100)
        con_pct = round((1 - self.consensus_score) * 100)
        res_pct = round((1 - self.resilience_score) * 100)

        if c < 0.20:
            self.swarm_signal = (
                f"Intelligence collective émergente unifiée — cohérence {coh_pct}%"
                f" — consensus {con_pct}% — résilience essaim {res_pct}%"
            )
        else:
            label_map = {
                "swarm_fragmentation": "Fragmentation essaim",
                "consensus_deadlock": "Blocage consensus",
                "emergent_drift": "Dérive émergente",
                "collective_amnesia": "Amnésie collective",
                "orchestration_collapse": "Effondrement orchestration",
                "none": "Divergence collective",
            }
            label = label_map[pat]
            composite_pct = round((1 - c) * 100)
            self.swarm_signal = (
                f"{label} — cohérence {coh_pct}% — consensus {con_pct}%"
                f" — résilience essaim {res_pct}% — composite {composite_pct}"
            )

    def to_dict(self) -> dict:
        return {
            "node_id": self.node.node_id,
            "node_role": self.node.node_role,
            "region": self.node.region,
            "swarm_risk": self.swarm_risk,
            "swarm_pattern": self.swarm_pattern,
            "swarm_severity": self.swarm_severity,
            "recommended_action": self.recommended_action,
            "coherence_score": self.coherence_score,
            "intelligence_score": self.intelligence_score,
            "consensus_score": self.consensus_score,
            "resilience_score": self.resilience_score,
            "swarm_composite": self.swarm_composite,
            "has_fragmentation_signal": self.has_fragmentation_signal,
            "requires_emergency_reset": self.requires_emergency_reset,
            "swarm_signal": self.swarm_signal,
        }


class CollectiveConsciousnessOrchestrationEngine:
    def assess_batch(self, nodes: list) -> list:
        results = []
        for node in nodes:
            assessment = _SwarmAssessment(node)
            results.append(assessment.to_dict())
        return results

    def summary(self, results: list) -> dict:
        total = len(results)

        risk_counts: dict = {}
        pattern_counts: dict = {}
        severity_counts: dict = {}
        action_counts: dict = {}

        sum_composite = 0.0
        fragmentation_signal_count = 0
        emergency_reset_count = 0
        sum_coherence = 0.0
        sum_intelligence = 0.0
        sum_consensus = 0.0
        sum_resilience = 0.0
        sum_entropy = 0.0

        for r in results:
            risk_counts[r["swarm_risk"]] = risk_counts.get(r["swarm_risk"], 0) + 1
            pattern_counts[r["swarm_pattern"]] = pattern_counts.get(r["swarm_pattern"], 0) + 1
            severity_counts[r["swarm_severity"]] = severity_counts.get(r["swarm_severity"], 0) + 1
            action_counts[r["recommended_action"]] = action_counts.get(r["recommended_action"], 0) + 1

            sum_composite += r["swarm_composite"]
            if r["has_fragmentation_signal"]:
                fragmentation_signal_count += 1
            if r["requires_emergency_reset"]:
                emergency_reset_count += 1
            sum_coherence += r["coherence_score"]
            sum_intelligence += r["intelligence_score"]
            sum_consensus += r["consensus_score"]
            sum_resilience += r["resilience_score"]

            entropy_index = min(round(r["swarm_composite"] * 10, 2), 10.0)
            sum_entropy += entropy_index

        if total == 0:
            avg_composite = 0.0
            avg_coherence = 0.0
            avg_intelligence = 0.0
            avg_consensus = 0.0
            avg_resilience = 0.0
            avg_entropy = 0.0
        else:
            avg_composite = round(sum_composite / total, 2)
            avg_coherence = round(sum_coherence / total, 2)
            avg_intelligence = round(sum_intelligence / total, 2)
            avg_consensus = round(sum_consensus / total, 2)
            avg_resilience = round(sum_resilience / total, 2)
            avg_entropy = round(sum_entropy / total, 2)

        return {
            "total": total,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_swarm_composite": avg_composite,
            "fragmentation_signal_count": fragmentation_signal_count,
            "emergency_reset_count": emergency_reset_count,
            "avg_coherence_score": avg_coherence,
            "avg_intelligence_score": avg_intelligence,
            "avg_consensus_score": avg_consensus,
            "avg_resilience_score": avg_resilience,
            "avg_estimated_swarm_entropy_index": avg_entropy,
        }
