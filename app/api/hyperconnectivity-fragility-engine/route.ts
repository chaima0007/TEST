import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // HF-001 — EMEA, cloud_core — critical, cascade_failure_risk
  { entity_id:"HF-001", infrastructure_layer:"cloud_core", region:"EMEA",
    node_density:0.82, interconnection_depth:0.88, single_point_concentration:0.85,
    cascading_vulnerability:0.80, network_centrality_risk:0.78, latency_criticality:0.75,
    bandwidth_saturation:0.72, protocol_obsolescence:0.45, dependency_depth:0.70,
    redundancy_deficit:0.72, cyber_attack_surface:0.68, supply_chain_digital_exposure:0.60,
    cloud_concentration_risk:0.75, data_sovereignty_gap:0.62, patch_velocity:0.35,
    zero_day_exposure:0.60, infrastructure_age:0.55 },
  // HF-002 — APAC, edge_network — low, none
  { entity_id:"HF-002", infrastructure_layer:"edge_network", region:"APAC",
    node_density:0.25, interconnection_depth:0.20, single_point_concentration:0.18,
    cascading_vulnerability:0.15, network_centrality_risk:0.20, latency_criticality:0.22,
    bandwidth_saturation:0.18, protocol_obsolescence:0.15, dependency_depth:0.20,
    redundancy_deficit:0.18, cyber_attack_surface:0.22, supply_chain_digital_exposure:0.18,
    cloud_concentration_risk:0.20, data_sovereignty_gap:0.15, patch_velocity:0.88,
    zero_day_exposure:0.12, infrastructure_age:0.18 },
  // HF-003 — NOAM, data_centers — high, dependency_collapse
  { entity_id:"HF-003", infrastructure_layer:"data_centers", region:"NOAM",
    node_density:0.62, interconnection_depth:0.65, single_point_concentration:0.55,
    cascading_vulnerability:0.58, network_centrality_risk:0.52, latency_criticality:0.60,
    bandwidth_saturation:0.55, protocol_obsolescence:0.48, dependency_depth:0.72,
    redundancy_deficit:0.68, cyber_attack_surface:0.55, supply_chain_digital_exposure:0.50,
    cloud_concentration_risk:0.62, data_sovereignty_gap:0.45, patch_velocity:0.50,
    zero_day_exposure:0.50, infrastructure_age:0.52 },
  // HF-004 — LATAM, edge_network — low, none
  { entity_id:"HF-004", infrastructure_layer:"edge_network", region:"LATAM",
    node_density:0.22, interconnection_depth:0.18, single_point_concentration:0.20,
    cascading_vulnerability:0.18, network_centrality_risk:0.22, latency_criticality:0.20,
    bandwidth_saturation:0.15, protocol_obsolescence:0.20, dependency_depth:0.18,
    redundancy_deficit:0.22, cyber_attack_surface:0.20, supply_chain_digital_exposure:0.15,
    cloud_concentration_risk:0.18, data_sovereignty_gap:0.20, patch_velocity:0.82,
    zero_day_exposure:0.15, infrastructure_age:0.20 },
  // HF-005 — MEA, cloud_core — critical, cyber_systemic_attack
  { entity_id:"HF-005", infrastructure_layer:"cloud_core", region:"MEA",
    node_density:0.78, interconnection_depth:0.80, single_point_concentration:0.55,
    cascading_vulnerability:0.60, network_centrality_risk:0.65, latency_criticality:0.70,
    bandwidth_saturation:0.68, protocol_obsolescence:0.50, dependency_depth:0.60,
    redundancy_deficit:0.62, cyber_attack_surface:0.82, supply_chain_digital_exposure:0.72,
    cloud_concentration_risk:0.70, data_sovereignty_gap:0.60, patch_velocity:0.22,
    zero_day_exposure:0.78, infrastructure_age:0.55 },
  // HF-006 — EMEA, telecom_backbone — moderate, none
  { entity_id:"HF-006", infrastructure_layer:"telecom_backbone", region:"EMEA",
    node_density:0.35, interconnection_depth:0.32, single_point_concentration:0.32,
    cascading_vulnerability:0.30, network_centrality_risk:0.35, latency_criticality:0.38,
    bandwidth_saturation:0.32, protocol_obsolescence:0.30, dependency_depth:0.32,
    redundancy_deficit:0.28, cyber_attack_surface:0.35, supply_chain_digital_exposure:0.30,
    cloud_concentration_risk:0.28, data_sovereignty_gap:0.32, patch_velocity:0.65,
    zero_day_exposure:0.30, infrastructure_age:0.35 },
  // HF-007 — APAC, data_centers — high, sovereignty_breach
  { entity_id:"HF-007", infrastructure_layer:"data_centers", region:"APAC",
    node_density:0.65, interconnection_depth:0.62, single_point_concentration:0.52,
    cascading_vulnerability:0.55, network_centrality_risk:0.58, latency_criticality:0.60,
    bandwidth_saturation:0.55, protocol_obsolescence:0.50, dependency_depth:0.60,
    redundancy_deficit:0.55, cyber_attack_surface:0.58, supply_chain_digital_exposure:0.72,
    cloud_concentration_risk:0.72, data_sovereignty_gap:0.78, patch_velocity:0.48,
    zero_day_exposure:0.52, infrastructure_age:0.50 },
  // HF-008 — NOAM, cloud_core — critical, infrastructure_obsolescence
  { entity_id:"HF-008", infrastructure_layer:"cloud_core", region:"NOAM",
    node_density:0.75, interconnection_depth:0.72, single_point_concentration:0.68,
    cascading_vulnerability:0.62, network_centrality_risk:0.70, latency_criticality:0.65,
    bandwidth_saturation:0.62, protocol_obsolescence:0.80, dependency_depth:0.68,
    redundancy_deficit:0.55, cyber_attack_surface:0.62, supply_chain_digital_exposure:0.65,
    cloud_concentration_risk:0.60, data_sovereignty_gap:0.58, patch_velocity:0.40,
    zero_day_exposure:0.55, infrastructure_age:0.82 },
];

type Entity = typeof MOCK_ENTITIES[0];

function topologyScore(e: Entity): number {
  const raw = e.single_point_concentration * 0.4 + e.cascading_vulnerability * 0.35 + e.network_centrality_risk * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}
function dependencyScore(e: Entity): number {
  const raw = e.dependency_depth * 0.4 + e.redundancy_deficit * 0.35 + e.cloud_concentration_risk * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}
function securityScore(e: Entity): number {
  const raw = e.cyber_attack_surface * 0.35 + e.zero_day_exposure * 0.35 + (1 - e.patch_velocity) * 0.30;
  return Math.round(raw * 100 * 100) / 100;
}
function sovereigntyScore(e: Entity): number {
  const raw = e.data_sovereignty_gap * 0.4 + e.supply_chain_digital_exposure * 0.35 + e.protocol_obsolescence * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}
function compositeScore(topo: number, dep: number, sec: number, sov: number): number {
  return Math.round((topo * 0.30 + dep * 0.25 + sec * 0.25 + sov * 0.20) * 100) / 100;
}
function fragilityrisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}
function fragilityPattern(e: Entity): string {
  if (e.cascading_vulnerability >= 0.65 && e.single_point_concentration >= 0.60) return "cascade_failure_risk";
  if (e.dependency_depth >= 0.65 && e.redundancy_deficit >= 0.60) return "dependency_collapse";
  if (e.cyber_attack_surface >= 0.65 && e.zero_day_exposure >= 0.55) return "cyber_systemic_attack";
  if (e.data_sovereignty_gap >= 0.65 && e.cloud_concentration_risk >= 0.55) return "sovereignty_breach";
  if (e.protocol_obsolescence >= 0.65 && e.infrastructure_age >= 0.65) return "infrastructure_obsolescence";
  return "none";
}
function fragilitySeverity(comp: number): string {
  if (comp >= 75) return "fragile_critical";
  if (comp >= 50) return "high_fragility";
  if (comp >= 25) return "developing_vulnerability";
  return "resilient_infrastructure";
}
function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "infrastructure_emergency";
  if (risk === "high" && pattern === "cascade_failure_risk") return "cascade_circuit_breaker";
  if (risk === "high") return "fragility_hardening";
  if (risk === "moderate") return "infrastructure_monitoring";
  return "no_action";
}
function fragilitySignal(e: Entity, risk: string, comp: number): string {
  const compInt = Math.round(comp);
  if (risk === "critical") {
    return `Critique — point unique concentration ${Math.round(e.single_point_concentration * 100)}% — vulnérabilité cascade ${Math.round(e.cascading_vulnerability * 100)}% — composite ${compInt}`;
  }
  if (risk === "high") {
    return `Élevé — profondeur dépendance ${Math.round(e.dependency_depth * 100)}% — surface cyber ${Math.round(e.cyber_attack_surface * 100)}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `Modéré — exposition souveraineté ${Math.round(e.data_sovereignty_gap * 100)}% — composite ${compInt}`;
  }
  return "Infrastructure hyperconnectée résiliente — redondance suffisante, souveraineté préservée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const topo = topologyScore(e);
      const dep  = dependencyScore(e);
      const sec  = securityScore(e);
      const sov  = sovereigntyScore(e);
      const comp = compositeScore(topo, dep, sec, sov);
      const pat  = fragilityPattern(e);
      const risk = fragilityrisk(comp);
      const sev  = fragilitySeverity(comp);
      const act  = recommendedAction(risk, pat);
      return {
        entity_id:                          e.entity_id,
        region:                             e.region,
        infrastructure_layer:               e.infrastructure_layer,
        fragility_risk:                     risk,
        fragility_pattern:                  pat,
        fragility_severity:                 sev,
        recommended_action:                 act,
        topology_score:                     topo,
        dependency_score:                   dep,
        security_score:                     sec,
        sovereignty_score:                  sov,
        fragility_composite:                comp,
        is_in_fragility_crisis:             comp >= 60,
        requires_infrastructure_intervention: comp >= 40,
        fragility_signal:                   fragilitySignal(e, risk, comp),
      };
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tTopo=0, tDep=0, tSec=0, tSov=0, tComp=0, crisisC=0, interventionC=0;
    for (const ent of entities) {
      rc[ent.fragility_risk]    = (rc[ent.fragility_risk]    || 0) + 1;
      pc[ent.fragility_pattern] = (pc[ent.fragility_pattern] || 0) + 1;
      sc[ent.fragility_severity]= (sc[ent.fragility_severity]|| 0) + 1;
      ac[ent.recommended_action]= (ac[ent.recommended_action]|| 0) + 1;
      tTopo  += ent.topology_score;
      tDep   += ent.dependency_score;
      tSec   += ent.security_score;
      tSov   += ent.sovereignty_score;
      tComp  += ent.fragility_composite;
      if (ent.is_in_fragility_crisis)              crisisC++;
      if (ent.requires_infrastructure_intervention) interventionC++;
    }
    const n = entities.length;
    const avgComp = tComp / n;
    const summary = {
      total:                            n,
      risk_counts:                      rc,
      pattern_counts:                   pc,
      severity_counts:                  sc,
      action_counts:                    ac,
      avg_fragility_composite:          Math.round(avgComp * 10) / 10,
      fragility_crisis_count:           crisisC,
      infrastructure_intervention_count: interventionC,
      avg_topology_score:               Math.round(tTopo / n * 10) / 10,
      avg_dependency_score:             Math.round(tDep / n * 10) / 10,
      avg_security_score:               Math.round(tSec / n * 10) / 10,
      avg_sovereignty_score:            Math.round(tSov / n * 10) / 10,
      avg_estimated_fragility_index:    Math.round(avgComp / 100 * 10 * 100) / 100,
    };
    return NextResponse.json(sealResponse({ entities, summary }, "hyperconnectivity-fragility-engine"));
  }
  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/hyperconnectivity-fragility-engine`);
    return NextResponse.json(sealResponse(await upstream.json(), "hyperconnectivity-fragility-engine"));
  } catch {
    return NextResponse.json(sealResponse({ error: "upstream unavailable" }, "hyperconnectivity-fragility-engine"), { status: 502 });
  }
}
