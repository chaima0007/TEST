import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // PME-001 — critical, abrupt_thaw_collapse (degradation>0.85, thermokarst>0.80)
  {
    entity_id: "PME-001", ecosystem_type: "toundra_continentale", region: "Sibérie",
    permafrost_degradation_rate: 0.92, active_layer_deepening: 0.88,
    methane_flux_intensity: 0.78, thermokarst_expansion: 0.86,
    subsea_methane_seepage: 0.72, carbon_stock_released: 0.80,
    tipping_point_proximity: 0.75, feedback_loop_acceleration: 0.70,
    albedo_reduction: 0.68, sea_level_contribution: 0.65,
    infrastructure_damage_rate: 0.72, indigenous_displacement: 0.65,
    monitoring_gap: 0.70, international_coordination_failure: 0.68,
    adaptation_capacity: 0.20, economic_loss_rate: 0.70,
    ecosystem_biodiversity_loss: 0.68,
  },
  // PME-002 — critical, subsea_methane_eruption (subsea_seepage>0.85, methane_flux>0.80)
  {
    entity_id: "PME-002", ecosystem_type: "plateau_sous_marin_arctique", region: "Arctique_Est",
    permafrost_degradation_rate: 0.78, active_layer_deepening: 0.72,
    methane_flux_intensity: 0.88, thermokarst_expansion: 0.68,
    subsea_methane_seepage: 0.90, carbon_stock_released: 0.82,
    tipping_point_proximity: 0.78, feedback_loop_acceleration: 0.72,
    albedo_reduction: 0.70, sea_level_contribution: 0.75,
    infrastructure_damage_rate: 0.65, indigenous_displacement: 0.68,
    monitoring_gap: 0.72, international_coordination_failure: 0.70,
    adaptation_capacity: 0.18, economic_loss_rate: 0.68,
    ecosystem_biodiversity_loss: 0.70,
  },
  // PME-003 — critical, tipping_point_cascade (tipping>0.85, feedback>0.80)
  {
    entity_id: "PME-003", ecosystem_type: "tourbière_boréale", region: "Canada_Nord",
    permafrost_degradation_rate: 0.80, active_layer_deepening: 0.75,
    methane_flux_intensity: 0.72, thermokarst_expansion: 0.70,
    subsea_methane_seepage: 0.65, carbon_stock_released: 0.78,
    tipping_point_proximity: 0.90, feedback_loop_acceleration: 0.85,
    albedo_reduction: 0.80, sea_level_contribution: 0.68,
    infrastructure_damage_rate: 0.62, indigenous_displacement: 0.65,
    monitoring_gap: 0.68, international_coordination_failure: 0.72,
    adaptation_capacity: 0.15, economic_loss_rate: 0.65,
    ecosystem_biodiversity_loss: 0.68,
  },
  // PME-004 — high, infrastructure_sinkhole_crisis (infra_damage>0.80, econ_loss>0.75)
  {
    entity_id: "PME-004", ecosystem_type: "pergélisol_urbain", region: "Alaska",
    permafrost_degradation_rate: 0.52, active_layer_deepening: 0.50,
    methane_flux_intensity: 0.48, thermokarst_expansion: 0.45,
    subsea_methane_seepage: 0.42, carbon_stock_released: 0.50,
    tipping_point_proximity: 0.48, feedback_loop_acceleration: 0.45,
    albedo_reduction: 0.42, sea_level_contribution: 0.48,
    infrastructure_damage_rate: 0.85, indigenous_displacement: 0.50,
    monitoring_gap: 0.48, international_coordination_failure: 0.45,
    adaptation_capacity: 0.35, economic_loss_rate: 0.80,
    ecosystem_biodiversity_loss: 0.48,
  },
  // PME-005 — high, indigenous_territory_loss (indigenous_disp>0.80, biodiversity>0.75)
  {
    entity_id: "PME-005", ecosystem_type: "territoire_autochtone_arctique", region: "Groenland",
    permafrost_degradation_rate: 0.48, active_layer_deepening: 0.45,
    methane_flux_intensity: 0.50, thermokarst_expansion: 0.48,
    subsea_methane_seepage: 0.42, carbon_stock_released: 0.45,
    tipping_point_proximity: 0.50, feedback_loop_acceleration: 0.48,
    albedo_reduction: 0.45, sea_level_contribution: 0.52,
    infrastructure_damage_rate: 0.48, indigenous_displacement: 0.85,
    monitoring_gap: 0.50, international_coordination_failure: 0.48,
    adaptation_capacity: 0.30, economic_loss_rate: 0.50,
    ecosystem_biodiversity_loss: 0.80,
  },
  // PME-006 — moderate, none
  {
    entity_id: "PME-006", ecosystem_type: "toundra_alpine", region: "Scandinavie",
    permafrost_degradation_rate: 0.30, active_layer_deepening: 0.28,
    methane_flux_intensity: 0.30, thermokarst_expansion: 0.28,
    subsea_methane_seepage: 0.25, carbon_stock_released: 0.30,
    tipping_point_proximity: 0.28, feedback_loop_acceleration: 0.25,
    albedo_reduction: 0.28, sea_level_contribution: 0.30,
    infrastructure_damage_rate: 0.28, indigenous_displacement: 0.25,
    monitoring_gap: 0.30, international_coordination_failure: 0.28,
    adaptation_capacity: 0.55, economic_loss_rate: 0.28,
    ecosystem_biodiversity_loss: 0.30,
  },
  // PME-007 — low, none
  {
    entity_id: "PME-007", ecosystem_type: "pergélisol_subarctique", region: "Finlande",
    permafrost_degradation_rate: 0.10, active_layer_deepening: 0.12,
    methane_flux_intensity: 0.10, thermokarst_expansion: 0.08,
    subsea_methane_seepage: 0.10, carbon_stock_released: 0.12,
    tipping_point_proximity: 0.10, feedback_loop_acceleration: 0.08,
    albedo_reduction: 0.10, sea_level_contribution: 0.12,
    infrastructure_damage_rate: 0.10, indigenous_displacement: 0.08,
    monitoring_gap: 0.10, international_coordination_failure: 0.12,
    adaptation_capacity: 0.80, economic_loss_rate: 0.10,
    ecosystem_biodiversity_loss: 0.10,
  },
  // PME-008 — low, none
  {
    entity_id: "PME-008", ecosystem_type: "zone_périarctique", region: "Islande",
    permafrost_degradation_rate: 0.12, active_layer_deepening: 0.10,
    methane_flux_intensity: 0.12, thermokarst_expansion: 0.10,
    subsea_methane_seepage: 0.08, carbon_stock_released: 0.10,
    tipping_point_proximity: 0.12, feedback_loop_acceleration: 0.10,
    albedo_reduction: 0.08, sea_level_contribution: 0.10,
    infrastructure_damage_rate: 0.12, indigenous_displacement: 0.10,
    monitoring_gap: 0.08, international_coordination_failure: 0.10,
    adaptation_capacity: 0.82, economic_loss_rate: 0.12,
    ecosystem_biodiversity_loss: 0.10,
  },
];

type PMEInput = typeof MOCK_ENTITIES[0];

function thawScore(e: PMEInput): number {
  return Math.round((e.permafrost_degradation_rate * 0.4 + e.active_layer_deepening * 0.35 + e.thermokarst_expansion * 0.25) * 100 * 100) / 100;
}
function methaneScore(e: PMEInput): number {
  return Math.round((e.methane_flux_intensity * 0.4 + e.subsea_methane_seepage * 0.35 + e.carbon_stock_released * 0.25) * 100 * 100) / 100;
}
function feedbackScore(e: PMEInput): number {
  return Math.round((e.tipping_point_proximity * 0.4 + e.feedback_loop_acceleration * 0.35 + e.albedo_reduction * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: PMEInput): number {
  return Math.round((e.international_coordination_failure * 0.4 + e.monitoring_gap * 0.35 + e.indigenous_displacement * 0.25) * 100 * 100) / 100;
}
function compositeScore(thaw: number, methane: number, feedback: number, gov: number): number {
  return Math.round((thaw * 0.30 + methane * 0.25 + feedback * 0.25 + gov * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function permafrostPattern(e: PMEInput): string {
  if (e.permafrost_degradation_rate > 0.85 && e.thermokarst_expansion > 0.80) return "abrupt_thaw_collapse";
  if (e.subsea_methane_seepage > 0.85 && e.methane_flux_intensity > 0.80) return "subsea_methane_eruption";
  if (e.tipping_point_proximity > 0.85 && e.feedback_loop_acceleration > 0.80) return "tipping_point_cascade";
  if (e.infrastructure_damage_rate > 0.80 && e.economic_loss_rate > 0.75) return "infrastructure_sinkhole_crisis";
  if (e.indigenous_displacement > 0.80 && e.ecosystem_biodiversity_loss > 0.75) return "indigenous_territory_loss";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_pergélisol_méthane_systémique";
  if (composite >= 40) return "crise_climatique_arctique_majeure";
  if (composite >= 20) return "dégradation_pergélisol_structurelle";
  return "pergélisol_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_pergélisol_méthane_critique";
  if (risk === "high") return "surveillance_renforcée_émissions_arctiques";
  if (risk === "moderate") return "renforcement_monitoring_pergélisol_régional";
  return "veille_pergélisol_méthane_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise pergélisol & méthane systémique — basculement climatique imminent";
  if (risk === "high") return "🟠 Crise climatique arctique majeure détectée";
  if (risk === "moderate") return "🟡 Dégradation pergélisol structurelle active";
  return "🟢 Pergélisol sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const thaw  = thawScore(e);
      const meth  = methaneScore(e);
      const feed  = feedbackScore(e);
      const gov   = governanceScore(e);
      const comp  = compositeScore(thaw, meth, feed, gov);
      const risk  = riskLevel(comp);
      const pat   = permafrostPattern(e);
      const sev   = severity(comp);
      const action = recommendedAction(risk);
      const sig   = signal(risk);
      return {
        entity_id:                   e.entity_id,
        ecosystem_type:              e.ecosystem_type,
        region:                      e.region,
        thaw_score:                  thaw,
        methane_score:               meth,
        feedback_score:              feed,
        governance_score:            gov,
        composite_score:             comp,
        risk_level:                  risk,
        permafrost_pattern:          pat,
        severity:                    sev,
        recommended_action:          action,
        signal:                      sig,
        permafrost_degradation_rate: e.permafrost_degradation_rate,
        methane_flux_intensity:      e.methane_flux_intensity,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tThaw = 0, tMeth = 0, tFeed = 0, tGov = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]             = (risk_distribution[ent.risk_level]             || 0) + 1;
      pattern_distribution[ent.permafrost_pattern]  = (pattern_distribution[ent.permafrost_pattern]  || 0) + 1;
      severity_distribution[ent.severity]           = (severity_distribution[ent.severity]           || 0) + 1;
      action_distribution[ent.recommended_action]   = (action_distribution[ent.recommended_action]   || 0) + 1;
      tThaw += ent.thaw_score;
      tMeth += ent.methane_score;
      tFeed += ent.feedback_score;
      tGov  += ent.governance_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;
    const avgThaw      = Math.round(tThaw / n * 10) / 10;

    const summary = {
      module_id:                            433,
      module_name:                          "Pergélisol & Méthane Arctique Intelligence Engine",
      total:                                n,
      critical:                             criticalCount,
      high:                                 highCount,
      moderate:                             moderateCount,
      low:                                  lowCount,
      avg_composite:                        avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_permafrost_risk_index:  Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, avg_thaw: avgThaw }, "permafrost-methane-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/permafrost-methane-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "permafrost-methane-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "permafrost-methane-engine"),
      { status: 502 }
    );
  }
}
