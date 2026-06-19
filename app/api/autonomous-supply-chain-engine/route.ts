import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_NODES = [
  // ASC-001 tier1_supplier EMEA — critical supplier_collapse
  { node_id:"ASC-001", node_type:"tier1_supplier",       region:"EMEA",  supplier_concentration_risk:0.88, lead_time_variability:0.75, inventory_buffer_adequacy:0.18, demand_forecast_accuracy:0.22, geopolitical_disruption_exposure:0.72, climate_disruption_risk:0.55, single_source_dependency:0.90, digital_twin_coverage:0.15, autonomous_reorder_capability:0.12, supplier_financial_health:0.20, nearshoring_readiness:0.18, multi_modal_transport_flexibility:0.22, real_time_visibility_score:0.18, circular_economy_integration:0.15, carbon_footprint_compliance:0.30, ethical_sourcing_score:0.28, disruption_recovery_speed:0.15 },
  // ASC-002 nearshoring_cluster NAMER — low autonomous
  { node_id:"ASC-002", node_type:"nearshoring_cluster",  region:"NAMER", supplier_concentration_risk:0.12, lead_time_variability:0.15, inventory_buffer_adequacy:0.92, demand_forecast_accuracy:0.90, geopolitical_disruption_exposure:0.10, climate_disruption_risk:0.12, single_source_dependency:0.08, digital_twin_coverage:0.95, autonomous_reorder_capability:0.92, supplier_financial_health:0.90, nearshoring_readiness:0.95, multi_modal_transport_flexibility:0.90, real_time_visibility_score:0.92, circular_economy_integration:0.85, carbon_footprint_compliance:0.90, ethical_sourcing_score:0.92, disruption_recovery_speed:0.90 },
  // ASC-003 distribution_hub APAC — high demand_shock
  { node_id:"ASC-003", node_type:"distribution_hub",     region:"APAC",  supplier_concentration_risk:0.48, lead_time_variability:0.62, inventory_buffer_adequacy:0.38, demand_forecast_accuracy:0.28, geopolitical_disruption_exposure:0.55, climate_disruption_risk:0.50, single_source_dependency:0.42, digital_twin_coverage:0.45, autonomous_reorder_capability:0.38, supplier_financial_health:0.55, nearshoring_readiness:0.40, multi_modal_transport_flexibility:0.48, real_time_visibility_score:0.42, circular_economy_integration:0.38, carbon_footprint_compliance:0.52, ethical_sourcing_score:0.55, disruption_recovery_speed:0.42 },
  // ASC-004 digital_supply LATAM — low adaptive
  { node_id:"ASC-004", node_type:"digital_supply",       region:"LATAM", supplier_concentration_risk:0.22, lead_time_variability:0.20, inventory_buffer_adequacy:0.78, demand_forecast_accuracy:0.80, geopolitical_disruption_exposure:0.28, climate_disruption_risk:0.25, single_source_dependency:0.18, digital_twin_coverage:0.82, autonomous_reorder_capability:0.80, supplier_financial_health:0.78, nearshoring_readiness:0.72, multi_modal_transport_flexibility:0.75, real_time_visibility_score:0.80, circular_economy_integration:0.70, carbon_footprint_compliance:0.78, ethical_sourcing_score:0.80, disruption_recovery_speed:0.75 },
  // ASC-005 cold_chain MEA — critical climate_disruption
  { node_id:"ASC-005", node_type:"cold_chain",           region:"MEA",   supplier_concentration_risk:0.62, lead_time_variability:0.70, inventory_buffer_adequacy:0.20, demand_forecast_accuracy:0.35, geopolitical_disruption_exposure:0.68, climate_disruption_risk:0.85, single_source_dependency:0.58, digital_twin_coverage:0.22, autonomous_reorder_capability:0.18, supplier_financial_health:0.35, nearshoring_readiness:0.25, multi_modal_transport_flexibility:0.28, real_time_visibility_score:0.22, circular_economy_integration:0.20, carbon_footprint_compliance:0.28, ethical_sourcing_score:0.32, disruption_recovery_speed:0.18 },
  // ASC-006 manufacturing_plant EMEA — moderate none
  { node_id:"ASC-006", node_type:"manufacturing_plant",  region:"EMEA",  supplier_concentration_risk:0.38, lead_time_variability:0.35, inventory_buffer_adequacy:0.62, demand_forecast_accuracy:0.65, geopolitical_disruption_exposure:0.42, climate_disruption_risk:0.38, single_source_dependency:0.30, digital_twin_coverage:0.60, autonomous_reorder_capability:0.55, supplier_financial_health:0.65, nearshoring_readiness:0.58, multi_modal_transport_flexibility:0.60, real_time_visibility_score:0.58, circular_economy_integration:0.55, carbon_footprint_compliance:0.65, ethical_sourcing_score:0.62, disruption_recovery_speed:0.58 },
  // ASC-007 last_mile APAC — high logistics_breakdown
  { node_id:"ASC-007", node_type:"last_mile",            region:"APAC",  supplier_concentration_risk:0.45, lead_time_variability:0.72, inventory_buffer_adequacy:0.35, demand_forecast_accuracy:0.48, geopolitical_disruption_exposure:0.50, climate_disruption_risk:0.55, single_source_dependency:0.40, digital_twin_coverage:0.50, autonomous_reorder_capability:0.42, supplier_financial_health:0.48, nearshoring_readiness:0.38, multi_modal_transport_flexibility:0.18, real_time_visibility_score:0.45, circular_economy_integration:0.35, carbon_footprint_compliance:0.48, ethical_sourcing_score:0.52, disruption_recovery_speed:0.40 },
  // ASC-008 tier2_supplier NAMER — critical digital_blindspot
  { node_id:"ASC-008", node_type:"tier2_supplier",       region:"NAMER", supplier_concentration_risk:0.70, lead_time_variability:0.60, inventory_buffer_adequacy:0.28, demand_forecast_accuracy:0.45, geopolitical_disruption_exposure:0.45, climate_disruption_risk:0.40, single_source_dependency:0.65, digital_twin_coverage:0.10, autonomous_reorder_capability:0.12, supplier_financial_health:0.42, nearshoring_readiness:0.30, multi_modal_transport_flexibility:0.38, real_time_visibility_score:0.15, circular_economy_integration:0.28, carbon_footprint_compliance:0.42, ethical_sourcing_score:0.45, disruption_recovery_speed:0.35 },
];

type Node = typeof MOCK_NODES[0];

function concentrationScore(n: Node): number {
  let s = 0;
  if      (n.supplier_concentration_risk >= 0.70) s += 40; else if (n.supplier_concentration_risk >= 0.50) s += 22; else if (n.supplier_concentration_risk >= 0.30) s += 8;
  if      (n.single_source_dependency >= 0.75) s += 35; else if (n.single_source_dependency >= 0.50) s += 18; else if (n.single_source_dependency >= 0.25) s += 6;
  if      (n.supplier_financial_health <= 0.25) s += 25; else if (n.supplier_financial_health <= 0.50) s += 12;
  return Math.min(s, 100);
}

function disruptionScore(n: Node): number {
  let s = 0;
  if      (n.geopolitical_disruption_exposure >= 0.70) s += 40; else if (n.geopolitical_disruption_exposure >= 0.50) s += 22; else if (n.geopolitical_disruption_exposure >= 0.30) s += 8;
  if      (n.climate_disruption_risk >= 0.70) s += 35; else if (n.climate_disruption_risk >= 0.50) s += 18; else if (n.climate_disruption_risk >= 0.30) s += 6;
  if      (n.lead_time_variability >= 0.65) s += 25; else if (n.lead_time_variability >= 0.40) s += 12;
  return Math.min(s, 100);
}

function resilienceScore(n: Node): number {
  let s = 0;
  if      (n.disruption_recovery_speed <= 0.25) s += 40; else if (n.disruption_recovery_speed <= 0.50) s += 22; else if (n.disruption_recovery_speed <= 0.70) s += 8;
  if      (n.inventory_buffer_adequacy <= 0.25) s += 35; else if (n.inventory_buffer_adequacy <= 0.50) s += 18; else if (n.inventory_buffer_adequacy <= 0.70) s += 6;
  if      (n.multi_modal_transport_flexibility <= 0.25) s += 25; else if (n.multi_modal_transport_flexibility <= 0.50) s += 12;
  return Math.min(s, 100);
}

function intelligenceScore(n: Node): number {
  let s = 0;
  if      (n.digital_twin_coverage <= 0.20) s += 40; else if (n.digital_twin_coverage <= 0.45) s += 22; else if (n.digital_twin_coverage <= 0.65) s += 8;
  if      (n.autonomous_reorder_capability <= 0.20) s += 35; else if (n.autonomous_reorder_capability <= 0.45) s += 18; else if (n.autonomous_reorder_capability <= 0.65) s += 6;
  if      (n.real_time_visibility_score <= 0.25) s += 25; else if (n.real_time_visibility_score <= 0.50) s += 12;
  return Math.min(s, 100);
}

function composite(conc: number, disr: number, res: number, intel: number): number {
  return Math.min(Math.round((conc * 0.30 + disr * 0.25 + res * 0.25 + intel * 0.20) * 100) / 100, 100);
}

function disruptionPattern(n: Node): string {
  if (n.supplier_concentration_risk >= 0.70 && n.single_source_dependency >= 0.65) return "supplier_collapse";
  if (n.geopolitical_disruption_exposure >= 0.65 || n.climate_disruption_risk >= 0.70) return "climate_disruption";
  if (n.demand_forecast_accuracy <= 0.35) return "demand_shock";
  if (n.multi_modal_transport_flexibility <= 0.25 && n.lead_time_variability >= 0.60) return "logistics_breakdown";
  if (n.digital_twin_coverage <= 0.20 && n.real_time_visibility_score <= 0.25) return "digital_blindspot";
  return "none";
}

function disruptionRisk(c: number): string {
  if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low";
}

function disruptionSeverity(c: number): string {
  if (c >= 60) return "fractured"; if (c >= 40) return "stressed"; if (c >= 20) return "adaptive"; return "autonomous";
}

function recommendedAction(r: string, p: string): string {
  if (r === "critical") {
    if (p === "supplier_collapse" || p === "demand_shock") return "emergency_sourcing";
    return "supply_diversification";
  }
  if (r === "high") {
    if (p === "climate_disruption" || p === "logistics_breakdown") return "nearshoring_acceleration";
    return "buffer_stockpiling";
  }
  if (r === "moderate") return "resilience_monitoring";
  return "no_action";
}

function disruptionSignal(n: Node, pat: string, comp: number): string {
  if (comp < 20) return "Chaîne d'approvisionnement autonome — résilience forte, couverture digitale optimale, risque de rupture minimal";
  const labels: Record<string, string> = {
    supplier_collapse:  "Effondrement fournisseur",
    demand_shock:       "Choc demande",
    logistics_breakdown:"Rupture logistique",
    digital_blindspot:  "Angle mort digital",
    climate_disruption: "Disruption climatique",
  };
  const label = labels[pat] ?? pat.replace(/_/g, " ");
  return `${label} — concentration ${n.supplier_concentration_risk.toFixed(2)} — exposition géopolitique ${n.geopolitical_disruption_exposure.toFixed(2)} — récupération ${n.disruption_recovery_speed.toFixed(2)} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const nodes = MOCK_NODES.map(n => {
      const conc = concentrationScore(n), disr = disruptionScore(n), res = resilienceScore(n), intel = intelligenceScore(n);
      const comp = composite(conc, disr, res, intel);
      const pat  = disruptionPattern(n), r = disruptionRisk(comp), sev = disruptionSeverity(comp), act = recommendedAction(r, pat);
      return {
        node_id:    n.node_id,
        node_type:  n.node_type,
        region:     n.region,
        disruption_risk:     r,
        disruption_pattern:  pat,
        disruption_severity: sev,
        recommended_action:  act,
        concentration_score: conc,
        disruption_score:    disr,
        resilience_score:    res,
        intelligence_score:  intel,
        supply_chain_composite: comp,
        has_critical_exposure:           comp >= 40 || n.supplier_concentration_risk >= 0.70 || n.single_source_dependency >= 0.75 || n.geopolitical_disruption_exposure >= 0.65,
        requires_immediate_intervention: comp >= 25 || n.climate_disruption_risk >= 0.65 || n.digital_twin_coverage <= 0.20 || n.disruption_recovery_speed <= 0.20,
        estimated_disruption_impact_index: Math.min(Math.round(comp / 100 * (1 - n.demand_forecast_accuracy + 0.01) * 10 * 100) / 100, 10.0),
        disruption_signal: disruptionSignal(n, pat, comp),
      };
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tComp=0, tConc=0, tDisr=0, tRes=0, tIntel=0, tImpact=0, critC=0, intervC=0;
    for (const nd of nodes) {
      rc[nd.disruption_risk]     = (rc[nd.disruption_risk]     || 0) + 1;
      pc[nd.disruption_pattern]  = (pc[nd.disruption_pattern]  || 0) + 1;
      sc[nd.disruption_severity] = (sc[nd.disruption_severity] || 0) + 1;
      ac[nd.recommended_action]  = (ac[nd.recommended_action]  || 0) + 1;
      tComp += nd.supply_chain_composite;
      tConc += nd.concentration_score; tDisr += nd.disruption_score;
      tRes  += nd.resilience_score;   tIntel += nd.intelligence_score;
      tImpact += nd.estimated_disruption_impact_index;
      if (nd.has_critical_exposure)           critC++;
      if (nd.requires_immediate_intervention) intervC++;
    }
    const n = nodes.length;
    return NextResponse.json(sealResponse({ nodes, summary: {
      total: n,
      risk_counts:     rc,
      pattern_counts:  pc,
      severity_counts: sc,
      action_counts:   ac,
      avg_supply_chain_composite:              Math.round(tComp  / n * 10) / 10,
      critical_exposure_count:                 critC,
      intervention_required_count:             intervC,
      avg_concentration_score:                 Math.round(tConc  / n * 10) / 10,
      avg_disruption_score:                    Math.round(tDisr  / n * 10) / 10,
      avg_resilience_score:                    Math.round(tRes   / n * 10) / 10,
      avg_intelligence_score:                  Math.round(tIntel / n * 10) / 10,
      avg_estimated_disruption_impact_index:   Math.round(tImpact/ n * 100) / 100,
    }} as Record<string,unknown>));
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/autonomous-supply-chain-engine`)).json());
}
