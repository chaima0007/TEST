"""
Module 290 — Semantic Web & Knowledge Graph Intelligence Engine
Caelum Partners Swarm Intelligence Platform
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class SemanticKnowledgeInput:
    entity_id: str
    graph_domain: str
    region: str
    ontology_coherence: float
    knowledge_connectivity: float
    inference_accuracy: float
    semantic_drift_rate: float
    schema_obsolescence: float
    entity_disambiguation_quality: float
    relation_extraction_precision: float
    knowledge_freshness: float
    cross_domain_linking: float
    graph_completeness: float
    reasoning_depth: float
    knowledge_pollution_rate: float
    provenance_integrity: float
    federated_query_efficiency: float
    ontological_conflict_rate: float
    knowledge_sovereignty: float
    graph_scalability: float


@dataclass
class SemanticKnowledgeResult:
    entity_id: str
    region: str
    graph_domain: str
    kg_risk: str
    kg_pattern: str
    kg_severity: str
    recommended_action: str
    coherence_score: float
    connectivity_score: float
    freshness_score: float
    sovereignty_score: float
    kg_composite: float
    is_in_kg_crisis: bool
    requires_kg_intervention: bool
    kg_signal: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "graph_domain": self.graph_domain,
            "kg_risk": self.kg_risk,
            "kg_pattern": self.kg_pattern,
            "kg_severity": self.kg_severity,
            "recommended_action": self.recommended_action,
            "coherence_score": self.coherence_score,
            "connectivity_score": self.connectivity_score,
            "freshness_score": self.freshness_score,
            "sovereignty_score": self.sovereignty_score,
            "kg_composite": self.kg_composite,
            "is_in_kg_crisis": self.is_in_kg_crisis,
            "requires_kg_intervention": self.requires_kg_intervention,
            "kg_signal": self.kg_signal,
        }


def _coherence_score(inp: SemanticKnowledgeInput) -> float:
    raw = (
        (1 - inp.ontology_coherence) * 0.4
        + inp.ontological_conflict_rate * 0.35
        + inp.schema_obsolescence * 0.25
    ) * 100
    return round(raw, 2)


def _connectivity_score(inp: SemanticKnowledgeInput) -> float:
    raw = (
        (1 - inp.knowledge_connectivity) * 0.4
        + (1 - inp.cross_domain_linking) * 0.35
        + (1 - inp.relation_extraction_precision) * 0.25
    ) * 100
    return round(raw, 2)


def _freshness_score(inp: SemanticKnowledgeInput) -> float:
    raw = (
        inp.semantic_drift_rate * 0.4
        + inp.knowledge_pollution_rate * 0.35
        + (1 - inp.knowledge_freshness) * 0.25
    ) * 100
    return round(raw, 2)


def _sovereignty_score(inp: SemanticKnowledgeInput) -> float:
    raw = (
        (1 - inp.knowledge_sovereignty) * 0.4
        + (1 - inp.provenance_integrity) * 0.35
        + (1 - inp.graph_completeness) * 0.25
    ) * 100
    return round(raw, 2)


def _composite(coh: float, con: float, fre: float, sov: float) -> float:
    return round(coh * 0.30 + con * 0.25 + fre * 0.25 + sov * 0.20, 2)


def _kg_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _kg_pattern(inp: SemanticKnowledgeInput) -> str:
    if (1 - inp.ontology_coherence) >= 0.65 and inp.ontological_conflict_rate >= 0.55:
        return "ontology_collapse"
    if (1 - inp.knowledge_connectivity) >= 0.65 and (1 - inp.cross_domain_linking) >= 0.55:
        return "knowledge_fragmentation"
    if inp.knowledge_pollution_rate >= 0.65 and inp.semantic_drift_rate >= 0.55:
        return "semantic_pollution"
    if (1 - inp.knowledge_sovereignty) >= 0.70 and (1 - inp.provenance_integrity) >= 0.60:
        return "sovereignty_breach"
    if inp.schema_obsolescence >= 0.65 and (1 - inp.knowledge_freshness) >= 0.60:
        return "graph_staleness"
    return "none"


def _kg_severity(composite: float) -> str:
    if composite >= 75:
        return "graph_collapse"
    if composite >= 50:
        return "high_degradation"
    if composite >= 25:
        return "developing_drift"
    return "knowledge_optimum"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "kg_emergency_reconstruction"
    if risk == "high":
        if pattern == "semantic_pollution":
            return "knowledge_cleansing"
        return "graph_restructuring"
    if risk == "moderate":
        return "kg_monitoring"
    return "no_action"


def _kg_signal(inp: SemanticKnowledgeInput, risk: str, composite: float) -> str:
    if risk == "critical":
        return (
            f"Critique — cohérence ontologique {int(inp.ontology_coherence * 100)}% "
            f"— pollution connaissance {int(inp.knowledge_pollution_rate * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — connectivité graphe {int(inp.knowledge_connectivity * 100)}% "
            f"— fraîcheur {int(inp.knowledge_freshness * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — dérive sémantique {int(inp.semantic_drift_rate * 100)}% "
            f"— composite {int(composite)}"
        )
    return "Graphe de connaissance optimal — ontologie cohérente, connaissance fraîche et souveraine"


def analyze(inp: SemanticKnowledgeInput) -> SemanticKnowledgeResult:
    coh = _coherence_score(inp)
    con = _connectivity_score(inp)
    fre = _freshness_score(inp)
    sov = _sovereignty_score(inp)
    comp = _composite(coh, con, fre, sov)
    risk = _kg_risk(comp)
    pattern = _kg_pattern(inp)
    severity = _kg_severity(comp)
    action = _recommended_action(risk, pattern)
    signal = _kg_signal(inp, risk, comp)

    return SemanticKnowledgeResult(
        entity_id=inp.entity_id,
        region=inp.region,
        graph_domain=inp.graph_domain,
        kg_risk=risk,
        kg_pattern=pattern,
        kg_severity=severity,
        recommended_action=action,
        coherence_score=coh,
        connectivity_score=con,
        freshness_score=fre,
        sovereignty_score=sov,
        kg_composite=comp,
        is_in_kg_crisis=comp >= 60,
        requires_kg_intervention=comp >= 40,
        kg_signal=signal,
    )


class SemanticKnowledgeGraphEngine:
    def run(self, inputs: list[SemanticKnowledgeInput]) -> dict[str, Any]:
        results = [analyze(inp) for inp in inputs]
        dicts = [r.to_dict() for r in results]

        risk_counts: dict[str, int] = {}
        pattern_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_composite = 0.0
        total_coherence = 0.0
        total_connectivity = 0.0
        total_freshness = 0.0
        total_sovereignty = 0.0
        kg_crisis_count = 0
        kg_intervention_count = 0

        for r in results:
            risk_counts[r.kg_risk] = risk_counts.get(r.kg_risk, 0) + 1
            pattern_counts[r.kg_pattern] = pattern_counts.get(r.kg_pattern, 0) + 1
            severity_counts[r.kg_severity] = severity_counts.get(r.kg_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.kg_composite
            total_coherence += r.coherence_score
            total_connectivity += r.connectivity_score
            total_freshness += r.freshness_score
            total_sovereignty += r.sovereignty_score
            if r.is_in_kg_crisis:
                kg_crisis_count += 1
            if r.requires_kg_intervention:
                kg_intervention_count += 1

        n = len(results)
        avg_composite = round(total_composite / n, 2) if n else 0.0

        summary: dict[str, Any] = {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_kg_composite": avg_composite,
            "kg_crisis_count": kg_crisis_count,
            "kg_intervention_count": kg_intervention_count,
            "avg_coherence_score": round(total_coherence / n, 2) if n else 0.0,
            "avg_connectivity_score": round(total_connectivity / n, 2) if n else 0.0,
            "avg_freshness_score": round(total_freshness / n, 2) if n else 0.0,
            "avg_sovereignty_score": round(total_sovereignty / n, 2) if n else 0.0,
            "avg_estimated_kg_risk_index": round(avg_composite / 100 * 10, 2) if n else 0.0,
        }

        return {"entities": dicts, "summary": summary}
