import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_NODES = [
  // CCO-001: meta_orchestrator, EMEA → critical, swarm_fragmentation
  { node_id:"CCO-001", node_role:"meta_orchestrator", region:"EMEA", consensus_alignment_score:0.15, inter_agent_coherence:0.18, swarm_synchrony_index:0.20, emergent_intelligence_score:0.22, collective_decision_quality:0.18, agent_diversity_coefficient:0.45, information_redundancy_risk:0.75, swarm_drift_detection_score:0.72, meta_learning_velocity:0.20, conflict_resolution_efficiency:0.18, collective_memory_integrity:0.22, swarm_resilience_score:0.20, distributed_reasoning_clarity:0.18, cross_agent_trust_level:0.15, orchestration_overhead_ratio:0.78, collective_creativity_index:0.22, swarm_convergence_speed:0.18 },
  // CCO-002: strategy_agent, NAMER → low, unified
  { node_id:"CCO-002", node_role:"strategy_agent", region:"NAMER", consensus_alignment_score:0.92, inter_agent_coherence:0.90, swarm_synchrony_index:0.88, emergent_intelligence_score:0.91, collective_decision_quality:0.89, agent_diversity_coefficient:0.72, information_redundancy_risk:0.08, swarm_drift_detection_score:0.10, meta_learning_velocity:0.88, conflict_resolution_efficiency:0.90, collective_memory_integrity:0.92, swarm_resilience_score:0.91, distributed_reasoning_clarity:0.89, cross_agent_trust_level:0.93, orchestration_overhead_ratio:0.10, collective_creativity_index:0.88, swarm_convergence_speed:0.90 },
  // CCO-003: risk_agent, APAC → high, consensus_deadlock
  { node_id:"CCO-003", node_role:"risk_agent", region:"APAC", consensus_alignment_score:0.22, inter_agent_coherence:0.48, swarm_synchrony_index:0.45, emergent_intelligence_score:0.52, collective_decision_quality:0.50, agent_diversity_coefficient:0.60, information_redundancy_risk:0.55, swarm_drift_detection_score:0.48, meta_learning_velocity:0.50, conflict_resolution_efficiency:0.25, collective_memory_integrity:0.52, swarm_resilience_score:0.48, distributed_reasoning_clarity:0.50, cross_agent_trust_level:0.45, orchestration_overhead_ratio:0.50, collective_creativity_index:0.48, swarm_convergence_speed:0.45 },
  // CCO-004: financial_agent, LATAM → low, synchronizing
  { node_id:"CCO-004", node_role:"financial_agent", region:"LATAM", consensus_alignment_score:0.78, inter_agent_coherence:0.80, swarm_synchrony_index:0.75, emergent_intelligence_score:0.82, collective_decision_quality:0.78, agent_diversity_coefficient:0.68, information_redundancy_risk:0.15, swarm_drift_detection_score:0.12, meta_learning_velocity:0.80, conflict_resolution_efficiency:0.78, collective_memory_integrity:0.80, swarm_resilience_score:0.82, distributed_reasoning_clarity:0.78, cross_agent_trust_level:0.80, orchestration_overhead_ratio:0.15, collective_creativity_index:0.78, swarm_convergence_speed:0.80 },
  // CCO-005: governance_agent, EMEA → critical, emergent_drift
  { node_id:"CCO-005", node_role:"governance_agent", region:"EMEA", consensus_alignment_score:0.28, inter_agent_coherence:0.35, swarm_synchrony_index:0.30, emergent_intelligence_score:0.30, collective_decision_quality:0.28, agent_diversity_coefficient:0.50, information_redundancy_risk:0.68, swarm_drift_detection_score:0.78, meta_learning_velocity:0.25, conflict_resolution_efficiency:0.30, collective_memory_integrity:0.28, swarm_resilience_score:0.25, distributed_reasoning_clarity:0.28, cross_agent_trust_level:0.22, orchestration_overhead_ratio:0.65, collective_creativity_index:0.28, swarm_convergence_speed:0.25 },
  // CCO-006: analyst_agent, NAMER → moderate, none
  { node_id:"CCO-006", node_role:"analyst_agent", region:"NAMER", consensus_alignment_score:0.60, inter_agent_coherence:0.62, swarm_synchrony_index:0.58, emergent_intelligence_score:0.65, collective_decision_quality:0.62, agent_diversity_coefficient:0.65, information_redundancy_risk:0.35, swarm_drift_detection_score:0.30, meta_learning_velocity:0.62, conflict_resolution_efficiency:0.60, collective_memory_integrity:0.65, swarm_resilience_score:0.62, distributed_reasoning_clarity:0.60, cross_agent_trust_level:0.62, orchestration_overhead_ratio:0.38, collective_creativity_index:0.60, swarm_convergence_speed:0.62 },
  // CCO-007: legal_agent, APAC → high, collective_amnesia
  { node_id:"CCO-007", node_role:"legal_agent", region:"APAC", consensus_alignment_score:0.38, inter_agent_coherence:0.42, swarm_synchrony_index:0.40, emergent_intelligence_score:0.45, collective_decision_quality:0.42, agent_diversity_coefficient:0.55, information_redundancy_risk:0.58, swarm_drift_detection_score:0.45, meta_learning_velocity:0.40, conflict_resolution_efficiency:0.42, collective_memory_integrity:0.18, swarm_resilience_score:0.40, distributed_reasoning_clarity:0.42, cross_agent_trust_level:0.40, orchestration_overhead_ratio:0.55, collective_creativity_index:0.40, swarm_convergence_speed:0.42 },
  // CCO-008: market_agent, MEA → critical, orchestration_collapse
  { node_id:"CCO-008", node_role:"market_agent", region:"MEA", consensus_alignment_score:0.20, inter_agent_coherence:0.22, swarm_synchrony_index:0.18, emergent_intelligence_score:0.20, collective_decision_quality:0.18, agent_diversity_coefficient:0.40, information_redundancy_risk:0.80, swarm_drift_detection_score:0.65, meta_learning_velocity:0.18, conflict_resolution_efficiency:0.20, collective_memory_integrity:0.22, swarm_resilience_score:0.18, distributed_reasoning_clarity:0.20, cross_agent_trust_level:0.18, orchestration_overhead_ratio:0.82, collective_creativity_index:0.20, swarm_convergence_speed:0.18 },
];

type SwarmNode = typeof MOCK_NODES[0];

function coherenceScore(n: SwarmNode): number {
  return Math.round(((1 - n.inter_agent_coherence) + (1 - n.swarm_synchrony_index) + n.swarm_drift_detection_score) / 3 * 100) / 100;
}
function intelligenceScore(n: SwarmNode): number {
  return Math.round(((1 - n.emergent_intelligence_score) + (1 - n.collective_decision_quality) + (1 - n.meta_learning_velocity)) / 3 * 100) / 100;
}
function consensusScore(n: SwarmNode): number {
  return Math.round(((1 - n.consensus_alignment_score) + (1 - n.conflict_resolution_efficiency) + (1 - n.cross_agent_trust_level)) / 3 * 100) / 100;
}
function resilienceScore(n: SwarmNode): number {
  return Math.round(((1 - n.swarm_resilience_score) + (1 - n.collective_memory_integrity) + n.information_redundancy_risk) / 3 * 100) / 100;
}
function composite(coh: number, int_: number, con: number, res: number): number {
  return Math.min(Math.round((coh * 0.30 + int_ * 0.25 + con * 0.25 + res * 0.20) * 100) / 100, 1.0);
}
function swarmPattern(n: SwarmNode): string {
  if (n.inter_agent_coherence <= 0.25 && n.swarm_synchrony_index <= 0.25) return "swarm_fragmentation";
  if (n.consensus_alignment_score <= 0.30 && n.conflict_resolution_efficiency <= 0.30) return "consensus_deadlock";
  if (n.swarm_drift_detection_score >= 0.65) return "emergent_drift";
  if (n.collective_memory_integrity <= 0.25) return "collective_amnesia";
  if (n.orchestration_overhead_ratio >= 0.70) return "orchestration_collapse";
  return "none";
}
function swarmRisk(c: number): string { if (c >= 0.60) return "critical"; if (c >= 0.40) return "high"; if (c >= 0.20) return "moderate"; return "low"; }
function swarmSeverity(c: number): string { if (c >= 0.60) return "disintegrated"; if (c >= 0.40) return "drifting"; if (c >= 0.20) return "synchronizing"; return "unified"; }
function swarmAction(risk: string, pattern: string): string {
  if (risk === "critical") {
    if (pattern === "swarm_fragmentation" || pattern === "orchestration_collapse") return "emergency_swarm_reset";
    return "orchestration_override";
  }
  if (risk === "high") {
    if (pattern === "consensus_deadlock" || pattern === "emergent_drift") return "consensus_protocol_refresh";
    return "diversity_rebalancing";
  }
  if (risk === "moderate") return "swarm_monitoring";
  return "no_action";
}
function swarmSignal(n: SwarmNode, pattern: string, coh: number, con: number, res: number, comp: number): string {
  if (comp < 0.20) {
    return `Intelligence collective émergente unifiée — cohérence ${Math.round((1 - coh) * 100)}% — consensus ${Math.round((1 - con) * 100)}% — résilience essaim ${Math.round((1 - res) * 100)}%`;
  }
  const labels: Record<string, string> = {
    swarm_fragmentation: "Fragmentation essaim",
    consensus_deadlock: "Blocage consensus",
    emergent_drift: "Dérive émergente",
    collective_amnesia: "Amnésie collective",
    orchestration_collapse: "Effondrement orchestration",
    none: "Divergence collective",
  };
  const label = labels[pattern] ?? pattern.replace(/_/g, " ");
  return `${label} — cohérence ${Math.round((1 - coh) * 100)}% — consensus ${Math.round((1 - con) * 100)}% — résilience essaim ${Math.round((1 - res) * 100)}% — composite ${Math.round((1 - comp) * 100)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[collective-consciousness-orchestration-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string, number> = {}, pc: Record<string, number> = {}, sc: Record<string, number> = {}, ac: Record<string, number> = {};
    let tcoh = 0, tint = 0, tcon = 0, tres = 0, tcomp = 0, fragC = 0, resetC = 0;
    for (const nd of nodes) {
      rc[nd.swarm_risk] = (rc[nd.swarm_risk] || 0) + 1;
      pc[nd.swarm_pattern] = (pc[nd.swarm_pattern] || 0) + 1;
      sc[nd.swarm_severity] = (sc[nd.swarm_severity] || 0) + 1;
      ac[nd.recommended_action] = (ac[nd.recommended_action] || 0) + 1;
      tcoh += nd.coherence_score; tint += nd.intelligence_score; tcon += nd.consensus_score; tres += nd.resilience_score;
      tcomp += nd.swarm_composite;
      if (nd.has_fragmentation_signal) fragC++;
      if (nd.requires_emergency_reset) resetC++;
    }
    const n2 = nodes.length;
    const avgComp = Math.round(tcomp / n2 * 100) / 100;

    return sealResponse(NextResponse.json(sealResponse({
      nodes,
      summary: {
        total: n2,
        risk_counts: rc,
        pattern_counts: pc,
        severity_counts: sc,
        action_counts: ac,
        avg_swarm_composite: avgComp,
        fragmentation_signal_count: fragC,
        emergency_reset_count: resetC,
        avg_coherence_score: Math.round(tcoh / n2 * 100) / 100,
        avg_intelligence_score: Math.round(tint / n2 * 100) / 100,
        avg_consensus_score: Math.round(tcon / n2 * 100) / 100,
        avg_resilience_score: Math.round(tres / n2 * 100) / 100,
        avg_estimated_swarm_entropy_index: Math.round(nodes.reduce((s, nd) => s + Math.min(nd.swarm_composite * 10, 10.0), 0) / n2 * 100) / 100,
      },
    }, "Collective Consciousness Orchestration Engine")));
  }
  return sealResponse(NextResponse.json(sealResponse(
    await (await fetch(`${process.env.SWARM_API_URL}/collective-consciousness-orchestration-engine`, { next: { revalidate: 30 } })).json(),
    "Collective Consciousness Orchestration Engine"
  )));
}
