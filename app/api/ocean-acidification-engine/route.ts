import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // OAE-001 — critical, coral_reef_mass_extinction (coral_bleaching>0.85, aragonite_saturation>0.80)
  {
    entity_id: "OAE-001", marine_ecosystem: "coral_reef", region: "APAC",
    pH_decline_rate: 0.88, coral_bleaching_intensity: 0.92,
    calcification_failure_rate: 0.78, fishery_collapse_risk: 0.72,
    food_chain_disruption: 0.70, aragonite_saturation_collapse: 0.87,
    pteropod_dissolution_rate: 0.80, oyster_shellfish_collapse: 0.68,
    carbon_sink_degradation: 0.75, deep_ocean_acidification: 0.82,
    marine_biodiversity_loss: 0.78, coastal_economy_impact: 0.80,
    fishery_dependent_population: 0.75, tipping_point_proximity: 0.72,
    recovery_capacity: 0.15, co2_absorption_decline: 0.70,
    nutrient_cycle_disruption: 0.72,
  },
  // OAE-002 — low, none (open_ocean, NOAM)
  {
    entity_id: "OAE-002", marine_ecosystem: "open_ocean", region: "NOAM",
    pH_decline_rate: 0.10, coral_bleaching_intensity: 0.08,
    calcification_failure_rate: 0.10, fishery_collapse_risk: 0.12,
    food_chain_disruption: 0.10, aragonite_saturation_collapse: 0.08,
    pteropod_dissolution_rate: 0.10, oyster_shellfish_collapse: 0.10,
    carbon_sink_degradation: 0.12, deep_ocean_acidification: 0.10,
    marine_biodiversity_loss: 0.08, coastal_economy_impact: 0.10,
    fishery_dependent_population: 0.12, tipping_point_proximity: 0.08,
    recovery_capacity: 0.90, co2_absorption_decline: 0.10,
    nutrient_cycle_disruption: 0.10,
  },
  // OAE-003 — critical, fishery_ecosystem_collapse (fishery_collapse>0.85, food_chain>0.80)
  {
    entity_id: "OAE-003", marine_ecosystem: "continental_shelf", region: "LATAM",
    pH_decline_rate: 0.80, coral_bleaching_intensity: 0.75,
    calcification_failure_rate: 0.72, fishery_collapse_risk: 0.90,
    food_chain_disruption: 0.85, aragonite_saturation_collapse: 0.78,
    pteropod_dissolution_rate: 0.72, oyster_shellfish_collapse: 0.70,
    carbon_sink_degradation: 0.72, deep_ocean_acidification: 0.75,
    marine_biodiversity_loss: 0.70, coastal_economy_impact: 0.82,
    fishery_dependent_population: 0.88, tipping_point_proximity: 0.70,
    recovery_capacity: 0.18, co2_absorption_decline: 0.68,
    nutrient_cycle_disruption: 0.75,
  },
  // OAE-004 — moderate, none (estuary, EMEA)
  {
    entity_id: "OAE-004", marine_ecosystem: "estuary", region: "EMEA",
    pH_decline_rate: 0.30, coral_bleaching_intensity: 0.25,
    calcification_failure_rate: 0.28, fishery_collapse_risk: 0.30,
    food_chain_disruption: 0.28, aragonite_saturation_collapse: 0.25,
    pteropod_dissolution_rate: 0.28, oyster_shellfish_collapse: 0.30,
    carbon_sink_degradation: 0.25, deep_ocean_acidification: 0.28,
    marine_biodiversity_loss: 0.30, coastal_economy_impact: 0.28,
    fishery_dependent_population: 0.30, tipping_point_proximity: 0.25,
    recovery_capacity: 0.65, co2_absorption_decline: 0.28,
    nutrient_cycle_disruption: 0.28,
  },
  // OAE-005 — critical, carbon_sink_failure (carbon_sink>0.85, co2_absorption>0.80)
  {
    entity_id: "OAE-005", marine_ecosystem: "polar_ocean", region: "ARCTIC",
    pH_decline_rate: 0.85, coral_bleaching_intensity: 0.68,
    calcification_failure_rate: 0.72, fishery_collapse_risk: 0.75,
    food_chain_disruption: 0.70, aragonite_saturation_collapse: 0.80,
    pteropod_dissolution_rate: 0.78, oyster_shellfish_collapse: 0.65,
    carbon_sink_degradation: 0.90, deep_ocean_acidification: 0.85,
    marine_biodiversity_loss: 0.70, coastal_economy_impact: 0.68,
    fishery_dependent_population: 0.62, tipping_point_proximity: 0.80,
    recovery_capacity: 0.12, co2_absorption_decline: 0.88,
    nutrient_cycle_disruption: 0.72,
  },
  // OAE-006 — high, shellfish_industry_extinction (oyster>0.80, calcification>0.75)
  {
    entity_id: "OAE-006", marine_ecosystem: "coastal_bay", region: "APAC",
    pH_decline_rate: 0.55, coral_bleaching_intensity: 0.50,
    calcification_failure_rate: 0.80, fishery_collapse_risk: 0.48,
    food_chain_disruption: 0.45, aragonite_saturation_collapse: 0.52,
    pteropod_dissolution_rate: 0.48, oyster_shellfish_collapse: 0.85,
    carbon_sink_degradation: 0.45, deep_ocean_acidification: 0.48,
    marine_biodiversity_loss: 0.50, coastal_economy_impact: 0.72,
    fishery_dependent_population: 0.68, tipping_point_proximity: 0.50,
    recovery_capacity: 0.38, co2_absorption_decline: 0.45,
    nutrient_cycle_disruption: 0.50,
  },
  // OAE-007 — high, marine_biodiversity_crisis (biodiversity>0.80, tipping_point>0.75)
  {
    entity_id: "OAE-007", marine_ecosystem: "deep_sea", region: "LATAM",
    pH_decline_rate: 0.52, coral_bleaching_intensity: 0.55,
    calcification_failure_rate: 0.50, fishery_collapse_risk: 0.52,
    food_chain_disruption: 0.50, aragonite_saturation_collapse: 0.48,
    pteropod_dissolution_rate: 0.52, oyster_shellfish_collapse: 0.45,
    carbon_sink_degradation: 0.50, deep_ocean_acidification: 0.55,
    marine_biodiversity_loss: 0.85, coastal_economy_impact: 0.52,
    fishery_dependent_population: 0.50, tipping_point_proximity: 0.82,
    recovery_capacity: 0.28, co2_absorption_decline: 0.48,
    nutrient_cycle_disruption: 0.55,
  },
  // OAE-008 — critical, none (mangrove_coast, MEA — high composite via broadly elevated scores)
  {
    entity_id: "OAE-008", marine_ecosystem: "mangrove_coast", region: "MEA",
    pH_decline_rate: 0.82, coral_bleaching_intensity: 0.78,
    calcification_failure_rate: 0.75, fishery_collapse_risk: 0.80,
    food_chain_disruption: 0.78, aragonite_saturation_collapse: 0.75,
    pteropod_dissolution_rate: 0.78, oyster_shellfish_collapse: 0.72,
    carbon_sink_degradation: 0.78, deep_ocean_acidification: 0.80,
    marine_biodiversity_loss: 0.75, coastal_economy_impact: 0.82,
    fishery_dependent_population: 0.80, tipping_point_proximity: 0.72,
    recovery_capacity: 0.15, co2_absorption_decline: 0.75,
    nutrient_cycle_disruption: 0.78,
  },
];

type OAEInput = typeof MOCK_ENTITIES[0];

function chemicalScore(e: OAEInput): number {
  return Math.round((e.pH_decline_rate * 0.40 + e.aragonite_saturation_collapse * 0.35 + e.deep_ocean_acidification * 0.25) * 100 * 100) / 100;
}
function biologicalScore(e: OAEInput): number {
  return Math.round((e.coral_bleaching_intensity * 0.40 + e.marine_biodiversity_loss * 0.35 + e.pteropod_dissolution_rate * 0.25) * 100 * 100) / 100;
}
function foodSystemScore(e: OAEInput): number {
  return Math.round((e.fishery_collapse_risk * 0.40 + e.food_chain_disruption * 0.35 + e.oyster_shellfish_collapse * 0.25) * 100 * 100) / 100;
}
function systemicScore(e: OAEInput): number {
  return Math.round((e.carbon_sink_degradation * 0.40 + e.tipping_point_proximity * 0.35 + e.co2_absorption_decline * 0.25) * 100 * 100) / 100;
}
function compositeScore(chem: number, bio: number, food: number, sys: number): number {
  return Math.round((chem * 0.30 + bio * 0.25 + food * 0.25 + sys * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function oceanPattern(e: OAEInput): string {
  if (e.coral_bleaching_intensity > 0.85 && e.aragonite_saturation_collapse > 0.80) return "coral_reef_mass_extinction";
  if (e.fishery_collapse_risk > 0.85 && e.food_chain_disruption > 0.80) return "fishery_ecosystem_collapse";
  if (e.carbon_sink_degradation > 0.85 && e.co2_absorption_decline > 0.80) return "carbon_sink_failure";
  if (e.oyster_shellfish_collapse > 0.80 && e.calcification_failure_rate > 0.75) return "shellfish_industry_extinction";
  if (e.marine_biodiversity_loss > 0.80 && e.tipping_point_proximity > 0.75) return "marine_biodiversity_crisis";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "extinction_marine_systémique";
  if (composite >= 40) return "crise_acidification_océanique_majeure";
  if (composite >= 20) return "acidification_océanique_structurelle";
  return "écosystèmes_marins_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_écosystèmes_marins_critiques";
  if (risk === "high") return "restauration_marine_accélérée";
  if (risk === "moderate") return "renforcement_protection_milieux_marins";
  return "veille_acidification_océanique_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Extinction marine systémique — effondrement des écosystèmes océaniques";
  if (risk === "high") return "🟠 Crise acidification océanique majeure détectée";
  if (risk === "moderate") return "🟡 Acidification océanique structurelle active";
  return "🟢 Écosystèmes marins sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const chem  = chemicalScore(e);
      const bio   = biologicalScore(e);
      const food  = foodSystemScore(e);
      const sys   = systemicScore(e);
      const comp  = compositeScore(chem, bio, food, sys);
      const risk  = riskLevel(comp);
      const pat   = oceanPattern(e);
      const sev   = severity(comp);
      const action = recommendedAction(risk);
      const sig   = signal(risk);
      return {
        entity_id:                   e.entity_id,
        marine_ecosystem:            e.marine_ecosystem,
        region:                      e.region,
        chemical_score:              chem,
        biological_score:            bio,
        food_system_score:           food,
        systemic_score:              sys,
        composite_score:             comp,
        risk_level:                  risk,
        ocean_pattern:               pat,
        severity:                    sev,
        recommended_action:          action,
        signal:                      sig,
        pH_decline_rate:             e.pH_decline_rate,
        coral_bleaching_intensity:   e.coral_bleaching_intensity,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.ocean_pattern]     = (pattern_distribution[ent.ocean_pattern]     || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                                372,
      module_name:                              "Ocean Acidification & Marine Ecosystem Collapse Intelligence Engine",
      total:                                    n,
      critical:                                 criticalCount,
      high:                                     highCount,
      moderate:                                 moderateCount,
      low:                                      lowCount,
      avg_composite:                            avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_ocean_acidification_index:  Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "ocean-acidification-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/ocean-acidification-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "ocean-acidification-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "ocean-acidification-engine"),
      { status: 502 }
    );
  }
}
