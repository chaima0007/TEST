import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // SKG-001 — EMEA, enterprise_ontology — critical, ontology_collapse
  { id: "SKG-001", graph_domain: "enterprise_ontology", region: "EMEA",
    ontology_coherence: 0.08, knowledge_connectivity: 0.45, inference_accuracy: 0.40,
    semantic_drift_rate: 0.55, schema_obsolescence: 0.80, entity_disambiguation_quality: 0.38,
    relation_extraction_precision: 0.42, knowledge_freshness: 0.30, cross_domain_linking: 0.38,
    graph_completeness: 0.35, reasoning_depth: 0.38, knowledge_pollution_rate: 0.60,
    provenance_integrity: 0.42, federated_query_efficiency: 0.38, ontological_conflict_rate: 0.72,
    knowledge_sovereignty: 0.42, graph_scalability: 0.38 },

  // SKG-002 — APAC, biomedical_kg — low, knowledge_optimum / none
  { id: "SKG-002", graph_domain: "biomedical_kg", region: "APAC",
    ontology_coherence: 0.92, knowledge_connectivity: 0.90, inference_accuracy: 0.91,
    semantic_drift_rate: 0.08, schema_obsolescence: 0.07, entity_disambiguation_quality: 0.90,
    relation_extraction_precision: 0.91, knowledge_freshness: 0.92, cross_domain_linking: 0.90,
    graph_completeness: 0.92, reasoning_depth: 0.90, knowledge_pollution_rate: 0.07,
    provenance_integrity: 0.92, federated_query_efficiency: 0.91, ontological_conflict_rate: 0.06,
    knowledge_sovereignty: 0.92, graph_scalability: 0.90 },

  // SKG-003 — NOAM, financial_graph — high, knowledge_fragmentation
  { id: "SKG-003", graph_domain: "financial_graph", region: "NOAM",
    ontology_coherence: 0.58, knowledge_connectivity: 0.22, inference_accuracy: 0.55,
    semantic_drift_rate: 0.42, schema_obsolescence: 0.38, entity_disambiguation_quality: 0.55,
    relation_extraction_precision: 0.58, knowledge_freshness: 0.55, cross_domain_linking: 0.28,
    graph_completeness: 0.58, reasoning_depth: 0.55, knowledge_pollution_rate: 0.38,
    provenance_integrity: 0.58, federated_query_efficiency: 0.52, ontological_conflict_rate: 0.35,
    knowledge_sovereignty: 0.60, graph_scalability: 0.55 },

  // SKG-004 — LATAM, biomedical_kg — low, knowledge_optimum / none
  { id: "SKG-004", graph_domain: "biomedical_kg", region: "LATAM",
    ontology_coherence: 0.85, knowledge_connectivity: 0.83, inference_accuracy: 0.84,
    semantic_drift_rate: 0.12, schema_obsolescence: 0.10, entity_disambiguation_quality: 0.84,
    relation_extraction_precision: 0.85, knowledge_freshness: 0.84, cross_domain_linking: 0.83,
    graph_completeness: 0.85, reasoning_depth: 0.83, knowledge_pollution_rate: 0.10,
    provenance_integrity: 0.85, federated_query_efficiency: 0.84, ontological_conflict_rate: 0.09,
    knowledge_sovereignty: 0.85, graph_scalability: 0.83 },

  // SKG-005 — MEA, enterprise_ontology — critical, semantic_pollution
  { id: "SKG-005", graph_domain: "enterprise_ontology", region: "MEA",
    ontology_coherence: 0.30, knowledge_connectivity: 0.40, inference_accuracy: 0.35,
    semantic_drift_rate: 0.72, schema_obsolescence: 0.45, entity_disambiguation_quality: 0.35,
    relation_extraction_precision: 0.40, knowledge_freshness: 0.30, cross_domain_linking: 0.42,
    graph_completeness: 0.38, reasoning_depth: 0.35, knowledge_pollution_rate: 0.78,
    provenance_integrity: 0.40, federated_query_efficiency: 0.35, ontological_conflict_rate: 0.45,
    knowledge_sovereignty: 0.40, graph_scalability: 0.35 },

  // SKG-006 — EMEA, legal_knowledge — moderate, none
  { id: "SKG-006", graph_domain: "legal_knowledge", region: "EMEA",
    ontology_coherence: 0.65, knowledge_connectivity: 0.62, inference_accuracy: 0.63,
    semantic_drift_rate: 0.28, schema_obsolescence: 0.30, entity_disambiguation_quality: 0.63,
    relation_extraction_precision: 0.65, knowledge_freshness: 0.65, cross_domain_linking: 0.62,
    graph_completeness: 0.65, reasoning_depth: 0.63, knowledge_pollution_rate: 0.28,
    provenance_integrity: 0.65, federated_query_efficiency: 0.62, ontological_conflict_rate: 0.28,
    knowledge_sovereignty: 0.65, graph_scalability: 0.62 },

  // SKG-007 — APAC, financial_graph — high, sovereignty_breach
  { id: "SKG-007", graph_domain: "financial_graph", region: "APAC",
    ontology_coherence: 0.55, knowledge_connectivity: 0.52, inference_accuracy: 0.53,
    semantic_drift_rate: 0.35, schema_obsolescence: 0.38, entity_disambiguation_quality: 0.53,
    relation_extraction_precision: 0.55, knowledge_freshness: 0.55, cross_domain_linking: 0.52,
    graph_completeness: 0.42, reasoning_depth: 0.53, knowledge_pollution_rate: 0.35,
    provenance_integrity: 0.28, federated_query_efficiency: 0.50, ontological_conflict_rate: 0.38,
    knowledge_sovereignty: 0.18, graph_scalability: 0.52 },

  // SKG-008 — NOAM, enterprise_ontology — critical, graph_staleness
  { id: "SKG-008", graph_domain: "enterprise_ontology", region: "NOAM",
    ontology_coherence: 0.28, knowledge_connectivity: 0.40, inference_accuracy: 0.30,
    semantic_drift_rate: 0.60, schema_obsolescence: 0.82, entity_disambiguation_quality: 0.30,
    relation_extraction_precision: 0.35, knowledge_freshness: 0.22, cross_domain_linking: 0.52,
    graph_completeness: 0.32, reasoning_depth: 0.30, knowledge_pollution_rate: 0.55,
    provenance_integrity: 0.38, federated_query_efficiency: 0.30, ontological_conflict_rate: 0.42,
    knowledge_sovereignty: 0.35, graph_scalability: 0.30 },
];

type Entity = typeof MOCK_ENTITIES[0];

function coherenceScore(e: Entity): number {
  const raw = (
    (1 - e.ontology_coherence) * 0.4
    + e.ontological_conflict_rate * 0.35
    + e.schema_obsolescence * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function connectivityScore(e: Entity): number {
  const raw = (
    (1 - e.knowledge_connectivity) * 0.4
    + (1 - e.cross_domain_linking) * 0.35
    + (1 - e.relation_extraction_precision) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function freshnesScore(e: Entity): number {
  const raw = (
    e.semantic_drift_rate * 0.4
    + e.knowledge_pollution_rate * 0.35
    + (1 - e.knowledge_freshness) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function sovereigntyScore(e: Entity): number {
  const raw = (
    (1 - e.knowledge_sovereignty) * 0.4
    + (1 - e.provenance_integrity) * 0.35
    + (1 - e.graph_completeness) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function kgComposite(coh: number, con: number, fre: number, sov: number): number {
  return Math.round((coh * 0.30 + con * 0.25 + fre * 0.25 + sov * 0.20) * 100) / 100;
}

function kgRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function kgPattern(e: Entity): string {
  if ((1 - e.ontology_coherence) >= 0.65 && e.ontological_conflict_rate >= 0.55) return "ontology_collapse";
  if ((1 - e.knowledge_connectivity) >= 0.65 && (1 - e.cross_domain_linking) >= 0.55) return "knowledge_fragmentation";
  if (e.knowledge_pollution_rate >= 0.65 && e.semantic_drift_rate >= 0.55) return "semantic_pollution";
  if ((1 - e.knowledge_sovereignty) >= 0.70 && (1 - e.provenance_integrity) >= 0.60) return "sovereignty_breach";
  if (e.schema_obsolescence >= 0.65 && (1 - e.knowledge_freshness) >= 0.60) return "graph_staleness";
  return "none";
}

function kgSeverity(comp: number): string {
  if (comp >= 75) return "graph_collapse";
  if (comp >= 50) return "high_degradation";
  if (comp >= 25) return "developing_drift";
  return "knowledge_optimum";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "kg_emergency_reconstruction";
  if (risk === "high") {
    if (pattern === "semantic_pollution") return "knowledge_cleansing";
    return "graph_restructuring";
  }
  if (risk === "moderate") return "kg_monitoring";
  return "no_action";
}

function kgSignal(e: Entity, risk: string, comp: number): string {
  if (risk === "critical") {
    return `Critique — cohérence ontologique ${Math.round(e.ontology_coherence * 100)}% — pollution connaissance ${Math.round(e.knowledge_pollution_rate * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "high") {
    return `Élevé — connectivité graphe ${Math.round(e.knowledge_connectivity * 100)}% — fraîcheur ${Math.round(e.knowledge_freshness * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "moderate") {
    return `Modéré — dérive sémantique ${Math.round(e.semantic_drift_rate * 100)}% — composite ${Math.round(comp)}`;
  }
  return "Graphe de connaissance optimal — ontologie cohérente, connaissance fraîche et souveraine";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const coh = coherenceScore(e);
      const con = connectivityScore(e);
      const fre = freshnesScore(e);
      const sov = sovereigntyScore(e);
      const comp = kgComposite(coh, con, fre, sov);
      const risk = kgRisk(comp);
      const pattern = kgPattern(e);
      const severity = kgSeverity(comp);
      const action = recommendedAction(risk, pattern);
      return {
        id: e.entity_id,
        region: e.region,
        graph_domain: e.graph_domain,
        kg_risk: risk,
        kg_pattern: pattern,
        kg_severity: severity,
        recommended_action: action,
        coherence_score: coh,
        connectivity_score: con,
        freshness_score: fre,
        sovereignty_score: sov,
        kg_composite: comp,
        is_in_kg_crisis: comp >= 60,
        requires_kg_intervention: comp >= 40,
        kg_signal: kgSignal(e, risk, comp),
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tCoh = 0, tCon = 0, tFre = 0, tSov = 0, tComp = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.kg_risk]          = (rc[ent.kg_risk]          || 0) + 1;
      pc[ent.kg_pattern]       = (pc[ent.kg_pattern]       || 0) + 1;
      sc[ent.kg_severity]      = (sc[ent.kg_severity]      || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tCoh  += ent.coherence_score;
      tCon  += ent.connectivity_score;
      tFre  += ent.freshness_score;
      tSov  += ent.sovereignty_score;
      tComp += ent.kg_composite;
      if (ent.is_in_kg_crisis)           crisisCount++;
      if (ent.requires_kg_intervention)  interventionCount++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 100) / 100;
    const summary = {
      total: n,
      risk_counts: rc,
      pattern_counts: pc,
      severity_counts: sc,
      action_counts: ac,
      avg_kg_composite: avgComp,
      kg_crisis_count: crisisCount,
      kg_intervention_count: interventionCount,
      avg_coherence_score:    Math.round(tCoh / n * 100) / 100,
      avg_connectivity_score: Math.round(tCon / n * 100) / 100,
      avg_freshness_score:    Math.round(tFre / n * 100) / 100,
      avg_sovereignty_score:  Math.round(tSov / n * 100) / 100,
      avg_estimated_kg_risk_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "semantic-knowledge-graph-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/semantic-knowledge-graph-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    const data = await upstream.json();
    return NextResponse.json(sealResponse(data, "semantic-knowledge-graph-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream swarm unavailable" }, "semantic-knowledge-graph-engine"),
      { status: 502 }
    );
  }
}
