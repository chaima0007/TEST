import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // SCE-001 — critical, carbon_debt_acceleration (carbon_loss>0.85, org_matter>0.80)
  {
    id: "SCE-001", soil_type: "argile_lourde", region: "Beauce",
    carbon_loss_rate: 0.92, organic_matter_depletion: 0.88, tillage_intensity: 0.70, erosion_rate: 0.72,
    sequestration_potential: 0.20, regenerative_adoption: 0.18, cover_crop_use: 0.15,
    market_offset_credibility: 0.25, policy_incentive_effectiveness: 0.22,
    biodiversity_indicator: 0.20, fungal_network_health: 0.22,
    heavy_metal_contamination: 0.65, monoculture_pressure: 0.70,
    irrigation_salinization: 0.60, drought_vulnerability: 0.65,
    carbon_credit_fraud_risk: 0.60, farmer_income_impact: 0.65,
  },
  // SCE-002 — critical, tillage_erosion_crisis (tillage>0.85, erosion>0.80)
  {
    id: "SCE-002", soil_type: "limon_sableux", region: "Picardie",
    carbon_loss_rate: 0.75, organic_matter_depletion: 0.70, tillage_intensity: 0.90, erosion_rate: 0.88,
    sequestration_potential: 0.22, regenerative_adoption: 0.20, cover_crop_use: 0.18,
    market_offset_credibility: 0.25, policy_incentive_effectiveness: 0.22,
    biodiversity_indicator: 0.22, fungal_network_health: 0.25,
    heavy_metal_contamination: 0.60, monoculture_pressure: 0.65,
    irrigation_salinization: 0.58, drought_vulnerability: 0.62,
    carbon_credit_fraud_risk: 0.58, farmer_income_impact: 0.62,
  },
  // SCE-003 — critical, rewilding_sequestration_collapse (seq_potential>0.80, regen_adoption<0.20)
  {
    id: "SCE-003", soil_type: "tourbe_dégradée", region: "Normandie",
    carbon_loss_rate: 0.78, organic_matter_depletion: 0.72, tillage_intensity: 0.65, erosion_rate: 0.70,
    sequestration_potential: 0.85, regenerative_adoption: 0.10, cover_crop_use: 0.12,
    market_offset_credibility: 0.22, policy_incentive_effectiveness: 0.20,
    biodiversity_indicator: 0.18, fungal_network_health: 0.22,
    heavy_metal_contamination: 0.62, monoculture_pressure: 0.68,
    irrigation_salinization: 0.58, drought_vulnerability: 0.60,
    carbon_credit_fraud_risk: 0.62, farmer_income_impact: 0.60,
  },
  // SCE-004 — high, market_greenwashing_fraud (fraud_risk>0.80, credibility<0.25)
  {
    id: "SCE-004", soil_type: "calcaire_sec", region: "Champagne",
    carbon_loss_rate: 0.48, organic_matter_depletion: 0.45, tillage_intensity: 0.50, erosion_rate: 0.45,
    sequestration_potential: 0.55, regenerative_adoption: 0.50, cover_crop_use: 0.48,
    market_offset_credibility: 0.20, policy_incentive_effectiveness: 0.45,
    biodiversity_indicator: 0.50, fungal_network_health: 0.52,
    heavy_metal_contamination: 0.45, monoculture_pressure: 0.48,
    irrigation_salinization: 0.42, drought_vulnerability: 0.45,
    carbon_credit_fraud_risk: 0.85, farmer_income_impact: 0.45,
  },
  // SCE-005 — high, soil_microbiome_collapse (fungal<0.20, monoculture>0.80)
  {
    id: "SCE-005", soil_type: "limon_argileux", region: "Grand_Est",
    carbon_loss_rate: 0.50, organic_matter_depletion: 0.48, tillage_intensity: 0.52, erosion_rate: 0.48,
    sequestration_potential: 0.50, regenerative_adoption: 0.45, cover_crop_use: 0.48,
    market_offset_credibility: 0.50, policy_incentive_effectiveness: 0.45,
    biodiversity_indicator: 0.45, fungal_network_health: 0.15,
    heavy_metal_contamination: 0.48, monoculture_pressure: 0.85,
    irrigation_salinization: 0.45, drought_vulnerability: 0.48,
    carbon_credit_fraud_risk: 0.50, farmer_income_impact: 0.48,
  },
  // SCE-006 — moderate, none
  {
    id: "SCE-006", soil_type: "sable_humifère", region: "Bretagne",
    carbon_loss_rate: 0.30, organic_matter_depletion: 0.28, tillage_intensity: 0.30, erosion_rate: 0.28,
    sequestration_potential: 0.60, regenerative_adoption: 0.55, cover_crop_use: 0.58,
    market_offset_credibility: 0.60, policy_incentive_effectiveness: 0.58,
    biodiversity_indicator: 0.62, fungal_network_health: 0.60,
    heavy_metal_contamination: 0.28, monoculture_pressure: 0.30,
    irrigation_salinization: 0.25, drought_vulnerability: 0.28,
    carbon_credit_fraud_risk: 0.30, farmer_income_impact: 0.28,
  },
  // SCE-007 — low, none
  {
    id: "SCE-007", soil_type: "humus_riche", region: "Auvergne",
    carbon_loss_rate: 0.10, organic_matter_depletion: 0.08, tillage_intensity: 0.10, erosion_rate: 0.08,
    sequestration_potential: 0.85, regenerative_adoption: 0.80, cover_crop_use: 0.82,
    market_offset_credibility: 0.88, policy_incentive_effectiveness: 0.85,
    biodiversity_indicator: 0.88, fungal_network_health: 0.85,
    heavy_metal_contamination: 0.08, monoculture_pressure: 0.10,
    irrigation_salinization: 0.08, drought_vulnerability: 0.10,
    carbon_credit_fraud_risk: 0.10, farmer_income_impact: 0.08,
  },
  // SCE-008 — low, none
  {
    id: "SCE-008", soil_type: "prairie_permanente", region: "Massif_Central",
    carbon_loss_rate: 0.12, organic_matter_depletion: 0.10, tillage_intensity: 0.12, erosion_rate: 0.10,
    sequestration_potential: 0.82, regenerative_adoption: 0.78, cover_crop_use: 0.80,
    market_offset_credibility: 0.85, policy_incentive_effectiveness: 0.82,
    biodiversity_indicator: 0.85, fungal_network_health: 0.82,
    heavy_metal_contamination: 0.10, monoculture_pressure: 0.12,
    irrigation_salinization: 0.10, drought_vulnerability: 0.12,
    carbon_credit_fraud_risk: 0.12, farmer_income_impact: 0.10,
  },
];

type SCEInput = typeof MOCK_ENTITIES[0];

function degradationScore(e: SCEInput): number {
  return Math.round((e.carbon_loss_rate * 0.4 + e.organic_matter_depletion * 0.35 + e.erosion_rate * 0.25) * 100 * 100) / 100;
}
function sequestrationScore(e: SCEInput): number {
  return Math.round(((1 - e.sequestration_potential) * 0.4 + (1 - e.regenerative_adoption) * 0.35 + (1 - e.cover_crop_use) * 0.25) * 100 * 100) / 100;
}
function policyScore(e: SCEInput): number {
  return Math.round(((1 - e.policy_incentive_effectiveness) * 0.4 + (1 - e.market_offset_credibility) * 0.35 + e.carbon_credit_fraud_risk * 0.25) * 100 * 100) / 100;
}
function biodiversityScore(e: SCEInput): number {
  return Math.round(((1 - e.biodiversity_indicator) * 0.4 + (1 - e.fungal_network_health) * 0.35 + e.monoculture_pressure * 0.25) * 100 * 100) / 100;
}
function compositeScore(deg: number, seq: number, pol: number, bio: number): number {
  return Math.round((deg * 0.30 + seq * 0.25 + pol * 0.25 + bio * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function carbonPattern(e: SCEInput): string {
  if (e.carbon_loss_rate > 0.85 && e.organic_matter_depletion > 0.80) return "carbon_debt_acceleration";
  if (e.tillage_intensity > 0.85 && e.erosion_rate > 0.80) return "tillage_erosion_crisis";
  if (e.sequestration_potential > 0.80 && e.regenerative_adoption < 0.20) return "rewilding_sequestration_collapse";
  if (e.carbon_credit_fraud_risk > 0.80 && e.market_offset_credibility < 0.25) return "market_greenwashing_fraud";
  if (e.fungal_network_health < 0.20 && e.monoculture_pressure > 0.80) return "soil_microbiome_collapse";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_carbone_sol_systémique";
  if (composite >= 40) return "dégradation_sol_majeure";
  if (composite >= 20) return "appauvrissement_sol_structurel";
  return "sol_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_restauration_sol_critique";
  if (risk === "high") return "programme_séquestration_carbone_accéléré";
  if (risk === "moderate") return "renforcement_pratiques_régénératives";
  return "veille_carbone_sol_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise carbone sol systémique — séquestration en péril immédiat";
  if (risk === "high") return "🟠 Dégradation sol majeure — action urgente requise";
  if (risk === "moderate") return "🟡 Appauvrissement sol structurel détecté";
  return "🟢 Sol sous surveillance carbone";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[soil-carbon-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tDeg = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.carbon_pattern]    = (pattern_distribution[ent.carbon_pattern]    || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tDeg  += ent.degradation_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite   = Math.round(tComp / n * 10) / 10;
    const avgDegradation = Math.round(tDeg  / n * 10) / 10;

    const summary = {
      module_id:                          409,
      module_name:                        "Carbone Sol Agricole & Séquestration Intelligence Engine",
      total:                              n,
      critical:                           criticalCount,
      high:                               highCount,
      moderate:                           moderateCount,
      low:                                lowCount,
      avg_composite:                      avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_soil_carbon_index:    Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary, avg_degradation: avgDegradation }, "soil-carbon-engine")
    ));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/soil-carbon-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return sealResponse(NextResponse.json(sealResponse(await upstream.json(), "soil-carbon-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "soil-carbon-engine"),
      { status: 502 }
    ));
  }
}
