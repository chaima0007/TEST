import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_NETWORKS = [
  // NT-001 supply_chain EMEA — critical/cascade_failure
  { network_id:"NT-001", network_type:"supply_chain",         region:"EMEA",  connectivity_density:0.75, cascade_vulnerability_score:0.88, attractor_basin_stability:0.15, phase_transition_proximity:0.82, resilience_redundancy_score:0.12, small_world_coefficient:0.20, clustering_coefficient:0.30, hub_concentration_risk:0.90, information_flow_efficiency:0.22, self_organized_criticality_index:0.85, network_modularity_score:0.18, recovery_speed_score:0.10, interdependency_depth:0.88, perturbation_propagation_rate:0.92, adaptive_capacity_score:0.08, topology_robustness:0.12, emergent_behavior_predictability:0.10 },
  // NT-002 financial_market NAMER — low
  { network_id:"NT-002", network_type:"financial_market",     region:"NAMER", connectivity_density:0.55, cascade_vulnerability_score:0.12, attractor_basin_stability:0.88, phase_transition_proximity:0.10, resilience_redundancy_score:0.85, small_world_coefficient:0.78, clustering_coefficient:0.80, hub_concentration_risk:0.15, information_flow_efficiency:0.88, self_organized_criticality_index:0.20, network_modularity_score:0.82, recovery_speed_score:0.90, interdependency_depth:0.25, perturbation_propagation_rate:0.12, adaptive_capacity_score:0.88, topology_robustness:0.85, emergent_behavior_predictability:0.90 },
  // NT-003 social_influence APAC — high/phase_transition_collapse
  { network_id:"NT-003", network_type:"social_influence",     region:"APAC",  connectivity_density:0.60, cascade_vulnerability_score:0.55, attractor_basin_stability:0.35, phase_transition_proximity:0.75, resilience_redundancy_score:0.42, small_world_coefficient:0.52, clustering_coefficient:0.50, hub_concentration_risk:0.50, information_flow_efficiency:0.50, self_organized_criticality_index:0.62, network_modularity_score:0.45, recovery_speed_score:0.42, interdependency_depth:0.58, perturbation_propagation_rate:0.58, adaptive_capacity_score:0.40, topology_robustness:0.45, emergent_behavior_predictability:0.35 },
  // NT-004 infrastructure LATAM — low
  { network_id:"NT-004", network_type:"infrastructure",       region:"LATAM", connectivity_density:0.50, cascade_vulnerability_score:0.18, attractor_basin_stability:0.82, phase_transition_proximity:0.12, resilience_redundancy_score:0.80, small_world_coefficient:0.72, clustering_coefficient:0.75, hub_concentration_risk:0.20, information_flow_efficiency:0.80, self_organized_criticality_index:0.22, network_modularity_score:0.78, recovery_speed_score:0.82, interdependency_depth:0.30, perturbation_propagation_rate:0.18, adaptive_capacity_score:0.80, topology_robustness:0.80, emergent_behavior_predictability:0.82 },
  // NT-005 innovation_cluster EMEA — critical/hub_fragility
  { network_id:"NT-005", network_type:"innovation_cluster",   region:"EMEA",  connectivity_density:0.70, cascade_vulnerability_score:0.72, attractor_basin_stability:0.20, phase_transition_proximity:0.68, resilience_redundancy_score:0.18, small_world_coefficient:0.25, clustering_coefficient:0.28, hub_concentration_risk:0.92, information_flow_efficiency:0.30, self_organized_criticality_index:0.78, network_modularity_score:0.20, recovery_speed_score:0.15, interdependency_depth:0.80, perturbation_propagation_rate:0.80, adaptive_capacity_score:0.15, topology_robustness:0.15, emergent_behavior_predictability:0.15 },
  // NT-006 regulatory_ecosystem MEA — moderate
  { network_id:"NT-006", network_type:"regulatory_ecosystem", region:"MEA",   connectivity_density:0.45, cascade_vulnerability_score:0.32, attractor_basin_stability:0.65, phase_transition_proximity:0.30, resilience_redundancy_score:0.62, small_world_coefficient:0.60, clustering_coefficient:0.62, hub_concentration_risk:0.35, information_flow_efficiency:0.62, self_organized_criticality_index:0.40, network_modularity_score:0.60, recovery_speed_score:0.62, interdependency_depth:0.42, perturbation_propagation_rate:0.32, adaptive_capacity_score:0.60, topology_robustness:0.62, emergent_behavior_predictability:0.62 },
  // NT-007 talent_market NAMER — high/complexity_overload
  { network_id:"NT-007", network_type:"talent_market",        region:"NAMER", connectivity_density:0.55, cascade_vulnerability_score:0.48, attractor_basin_stability:0.42, phase_transition_proximity:0.45, resilience_redundancy_score:0.45, small_world_coefficient:0.48, clustering_coefficient:0.48, hub_concentration_risk:0.52, information_flow_efficiency:0.48, self_organized_criticality_index:0.88, network_modularity_score:0.44, recovery_speed_score:0.46, interdependency_depth:0.55, perturbation_propagation_rate:0.48, adaptive_capacity_score:0.44, topology_robustness:0.46, emergent_behavior_predictability:0.25 },
  // NT-008 geopolitical_alliance APAC — low
  { network_id:"NT-008", network_type:"geopolitical_alliance", region:"APAC", connectivity_density:0.48, cascade_vulnerability_score:0.15, attractor_basin_stability:0.85, phase_transition_proximity:0.12, resilience_redundancy_score:0.82, small_world_coefficient:0.75, clustering_coefficient:0.78, hub_concentration_risk:0.18, information_flow_efficiency:0.82, self_organized_criticality_index:0.18, network_modularity_score:0.80, recovery_speed_score:0.85, interdependency_depth:0.28, perturbation_propagation_rate:0.15, adaptive_capacity_score:0.82, topology_robustness:0.82, emergent_behavior_predictability:0.85 },
];

type Network = typeof MOCK_NETWORKS[0];

function topologyScore(n: Network): number {
  const quality = (1 - n.hub_concentration_risk) * 0.40 + n.clustering_coefficient * 0.35 + n.network_modularity_score * 0.25;
  return Math.min(Math.round((1 - quality) * 100 * 100) / 100, 100);
}
function dynamicsScore(n: Network): number {
  return Math.min(Math.round((n.cascade_vulnerability_score * 40 + n.perturbation_propagation_rate * 35 + n.phase_transition_proximity * 25) * 100) / 100, 100);
}
function resilienceScore(n: Network): number {
  const quality = n.resilience_redundancy_score * 0.40 + n.recovery_speed_score * 0.35 + n.adaptive_capacity_score * 0.25;
  return Math.min(Math.round((1 - quality) * 100 * 100) / 100, 100);
}
function emergenceScore(n: Network): number {
  const quality = (1 - n.self_organized_criticality_index) * 0.40 + n.emergent_behavior_predictability * 0.35 + n.attractor_basin_stability * 0.25;
  return Math.min(Math.round((1 - quality) * 100 * 100) / 100, 100);
}
function composite(topo: number, dyn: number, res: number, emg: number): number {
  return Math.min(Math.round((topo * 0.30 + dyn * 0.25 + res * 0.25 + emg * 0.20) * 100) / 100, 100);
}
function networkRisk(c: number): string {
  if (c >= 60) return "critical";
  if (c >= 40) return "high";
  if (c >= 20) return "moderate";
  return "low";
}
function networkPattern(n: Network): string {
  if (n.cascade_vulnerability_score >= 0.80 && n.perturbation_propagation_rate >= 0.80) return "cascade_failure";
  if (n.phase_transition_proximity >= 0.70 && n.attractor_basin_stability <= 0.40) return "phase_transition_collapse";
  if (n.hub_concentration_risk >= 0.85) return "hub_fragility";
  if (n.attractor_basin_stability <= 0.25 && n.self_organized_criticality_index >= 0.70) return "attractor_instability";
  if (n.self_organized_criticality_index >= 0.85 && n.emergent_behavior_predictability <= 0.30) return "complexity_overload";
  return "none";
}
function networkSeverity(c: number): string {
  if (c >= 60) return "cascading";
  if (c >= 40) return "critical_point";
  if (c >= 20) return "fluctuating";
  return "stable_complex";
}
function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") {
    if (pattern === "cascade_failure" || pattern === "hub_fragility" || pattern === "attractor_instability") return "emergency_decoupling";
    return "network_partitioning";
  }
  if (risk === "high") {
    if (pattern === "phase_transition_collapse" || pattern === "complexity_overload") return "redundancy_injection";
    return "hub_bypass";
  }
  if (risk === "moderate") return "topology_monitoring";
  return "no_action";
}
function networkSignal(n: Network, pattern: string, comp: number): string {
  if (comp < 20) return "Réseau complexe stable — topologie robuste, dynamiques maîtrisées, résilience émergente forte";
  const labels: Record<string, string> = {
    cascade_failure: "Défaillance en cascade",
    phase_transition_collapse: "Effondrement par transition de phase",
    hub_fragility: "Fragilité des nœuds centraux",
    attractor_instability: "Instabilité des bassins attracteurs",
    complexity_overload: "Surcharge de complexité émergente",
  };
  const label = labels[pattern] ?? pattern.replace(/_/g, " ");
  return `${label} — vulnérabilité cascade ${n.cascade_vulnerability_score.toFixed(2)} — proximité transition ${n.phase_transition_proximity.toFixed(2)} — concentration hub ${n.hub_concentration_risk.toFixed(2)} — composite ${Math.round(comp)}`;
}
function cascadeRiskIndex(n: Network, comp: number): number {
  return Math.round(Math.min(comp / 100 * (n.cascade_vulnerability_score + n.perturbation_propagation_rate) / 2 * 10, 10.0) * 100) / 100;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const networks = MOCK_NETWORKS.map(n => {
      const topo = topologyScore(n), dyn = dynamicsScore(n), res = resilienceScore(n), emg = emergenceScore(n);
      const comp = composite(topo, dyn, res, emg);
      const risk = networkRisk(comp), pat = networkPattern(n), sev = networkSeverity(comp), act = recommendedAction(risk, pat);
      return {
        network_id: n.network_id,
        network_type: n.network_type,
        region: n.region,
        network_risk: risk,
        network_pattern: pat,
        network_severity: sev,
        recommended_action: act,
        topology_score: topo,
        dynamics_score: dyn,
        resilience_score: res,
        emergence_score: emg,
        network_composite: comp,
        cascade_vulnerability_score: n.cascade_vulnerability_score,
        network_signal: networkSignal(n, pat, comp),
        estimated_cascade_risk_index: cascadeRiskIndex(n, comp),
      };
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let ttopo=0, tdyn=0, tres=0, temg=0, tcomp=0, tcri=0, cascadingC=0, interventionC=0;
    for (const net of networks) {
      rc[net.network_risk] = (rc[net.network_risk]||0) + 1;
      pc[net.network_pattern] = (pc[net.network_pattern]||0) + 1;
      sc[net.network_severity] = (sc[net.network_severity]||0) + 1;
      ac[net.recommended_action] = (ac[net.recommended_action]||0) + 1;
      ttopo += net.topology_score; tdyn += net.dynamics_score;
      tres += net.resilience_score; temg += net.emergence_score;
      tcomp += net.network_composite; tcri += net.estimated_cascade_risk_index;
      if (net.network_severity === "cascading") cascadingC++;
      if (net.network_risk === "critical" || net.network_risk === "high") interventionC++;
    }
    const n = networks.length;
    return NextResponse.json(sealResponse({ networks, summary: {
      total: n,
      risk_counts: rc,
      pattern_counts: pc,
      severity_counts: sc,
      action_counts: ac,
      avg_network_composite: Math.round(tcomp / n * 10) / 10,
      cascading_count: cascadingC,
      critical_intervention_count: interventionC,
      avg_topology_score: Math.round(ttopo / n * 10) / 10,
      avg_dynamics_score: Math.round(tdyn / n * 10) / 10,
      avg_resilience_score: Math.round(tres / n * 10) / 10,
      avg_emergence_score: Math.round(temg / n * 10) / 10,
      avg_estimated_cascade_risk_index: Math.round(tcri / n * 100) / 100,
    }} as Record<string,unknown>));
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/complex-network-physics-engine`)).json());
}
