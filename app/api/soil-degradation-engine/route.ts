import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // SDE-001 — critical, topsoil_extinction (topsoil>=0.70, monoculture>=0.65)
  {
    entity_id: "SDE-001", land_type: "cropland", region: "APAC",
    topsoil_loss_acceleration_rate: 0.85, soil_carbon_depletion_index: 0.60,
    microbiome_diversity_collapse: 0.55, desertification_expansion_rate: 0.60,
    agricultural_chemical_soil_toxicity: 0.65, compaction_crisis_density: 0.70,
    irrigation_salt_accumulation: 0.55, soil_erosion_from_extreme_weather: 0.75,
    land_conversion_pressure: 0.60, regenerative_agriculture_adoption_gap: 0.65,
    soil_acidification_rate: 0.62, phosphorus_depletion_trajectory: 0.55,
    groundwater_contamination_from_soil: 0.60, soil_food_web_collapse: 0.58,
    land_tenure_insecurity: 0.50, monoculture_soil_exhaustion_rate: 0.78,
    urban_soil_sealing_expansion: 0.45,
  },
  // SDE-002 — low, none (forest, NOAM)
  {
    entity_id: "SDE-002", land_type: "forest", region: "NOAM",
    topsoil_loss_acceleration_rate: 0.10, soil_carbon_depletion_index: 0.12,
    microbiome_diversity_collapse: 0.10, desertification_expansion_rate: 0.08,
    agricultural_chemical_soil_toxicity: 0.10, compaction_crisis_density: 0.12,
    irrigation_salt_accumulation: 0.10, soil_erosion_from_extreme_weather: 0.12,
    land_conversion_pressure: 0.10, regenerative_agriculture_adoption_gap: 0.12,
    soil_acidification_rate: 0.10, phosphorus_depletion_trajectory: 0.08,
    groundwater_contamination_from_soil: 0.10, soil_food_web_collapse: 0.12,
    land_tenure_insecurity: 0.10, monoculture_soil_exhaustion_rate: 0.10,
    urban_soil_sealing_expansion: 0.08,
  },
  // SDE-003 — high, soil_biome_collapse (microbiome>=0.70, food_web>=0.65)
  {
    entity_id: "SDE-003", land_type: "pasture", region: "LATAM",
    topsoil_loss_acceleration_rate: 0.45, soil_carbon_depletion_index: 0.45,
    microbiome_diversity_collapse: 0.78, desertification_expansion_rate: 0.42,
    agricultural_chemical_soil_toxicity: 0.42, compaction_crisis_density: 0.45,
    irrigation_salt_accumulation: 0.40, soil_erosion_from_extreme_weather: 0.45,
    land_conversion_pressure: 0.50, regenerative_agriculture_adoption_gap: 0.42,
    soil_acidification_rate: 0.40, phosphorus_depletion_trajectory: 0.42,
    groundwater_contamination_from_soil: 0.45, soil_food_web_collapse: 0.72,
    land_tenure_insecurity: 0.40, monoculture_soil_exhaustion_rate: 0.42,
    urban_soil_sealing_expansion: 0.35,
  },
  // SDE-004 — low, none (wetland, EMEA)
  {
    entity_id: "SDE-004", land_type: "wetland", region: "EMEA",
    topsoil_loss_acceleration_rate: 0.15, soil_carbon_depletion_index: 0.14,
    microbiome_diversity_collapse: 0.12, desertification_expansion_rate: 0.10,
    agricultural_chemical_soil_toxicity: 0.15, compaction_crisis_density: 0.14,
    irrigation_salt_accumulation: 0.12, soil_erosion_from_extreme_weather: 0.15,
    land_conversion_pressure: 0.12, regenerative_agriculture_adoption_gap: 0.15,
    soil_acidification_rate: 0.12, phosphorus_depletion_trajectory: 0.10,
    groundwater_contamination_from_soil: 0.12, soil_food_web_collapse: 0.14,
    land_tenure_insecurity: 0.12, monoculture_soil_exhaustion_rate: 0.12,
    urban_soil_sealing_expansion: 0.10,
  },
  // SDE-005 — critical, desertification_cascade (desert>=0.70, erosion>=0.65)
  {
    entity_id: "SDE-005", land_type: "dryland", region: "MEA",
    topsoil_loss_acceleration_rate: 0.70, soil_carbon_depletion_index: 0.62,
    microbiome_diversity_collapse: 0.60, desertification_expansion_rate: 0.88,
    agricultural_chemical_soil_toxicity: 0.62, compaction_crisis_density: 0.65,
    irrigation_salt_accumulation: 0.60, soil_erosion_from_extreme_weather: 0.82,
    land_conversion_pressure: 0.68, regenerative_agriculture_adoption_gap: 0.72,
    soil_acidification_rate: 0.60, phosphorus_depletion_trajectory: 0.58,
    groundwater_contamination_from_soil: 0.65, soil_food_web_collapse: 0.60,
    land_tenure_insecurity: 0.55, monoculture_soil_exhaustion_rate: 0.62,
    urban_soil_sealing_expansion: 0.50,
  },
  // SDE-006 — moderate, none (arable, NOAM)
  {
    entity_id: "SDE-006", land_type: "arable", region: "NOAM",
    topsoil_loss_acceleration_rate: 0.30, soil_carbon_depletion_index: 0.28,
    microbiome_diversity_collapse: 0.30, desertification_expansion_rate: 0.25,
    agricultural_chemical_soil_toxicity: 0.30, compaction_crisis_density: 0.28,
    irrigation_salt_accumulation: 0.28, soil_erosion_from_extreme_weather: 0.30,
    land_conversion_pressure: 0.28, regenerative_agriculture_adoption_gap: 0.30,
    soil_acidification_rate: 0.28, phosphorus_depletion_trajectory: 0.25,
    groundwater_contamination_from_soil: 0.28, soil_food_web_collapse: 0.28,
    land_tenure_insecurity: 0.28, monoculture_soil_exhaustion_rate: 0.28,
    urban_soil_sealing_expansion: 0.25,
  },
  // SDE-007 — high, chemical_soil_death (chem_tox>=0.70, acidif>=0.65)
  {
    entity_id: "SDE-007", land_type: "industrial_farmland", region: "APAC",
    topsoil_loss_acceleration_rate: 0.48, soil_carbon_depletion_index: 0.45,
    microbiome_diversity_collapse: 0.48, desertification_expansion_rate: 0.42,
    agricultural_chemical_soil_toxicity: 0.82, compaction_crisis_density: 0.48,
    irrigation_salt_accumulation: 0.50, soil_erosion_from_extreme_weather: 0.48,
    land_conversion_pressure: 0.50, regenerative_agriculture_adoption_gap: 0.45,
    soil_acidification_rate: 0.75, phosphorus_depletion_trajectory: 0.45,
    groundwater_contamination_from_soil: 0.52, soil_food_web_collapse: 0.45,
    land_tenure_insecurity: 0.42, monoculture_soil_exhaustion_rate: 0.45,
    urban_soil_sealing_expansion: 0.40,
  },
  // SDE-008 — critical, phosphorus_crisis (phosphorus>=0.70, carbon>=0.65)
  {
    entity_id: "SDE-008", land_type: "degraded_agricultural", region: "EMEA",
    topsoil_loss_acceleration_rate: 0.65, soil_carbon_depletion_index: 0.82,
    microbiome_diversity_collapse: 0.68, desertification_expansion_rate: 0.62,
    agricultural_chemical_soil_toxicity: 0.68, compaction_crisis_density: 0.65,
    irrigation_salt_accumulation: 0.62, soil_erosion_from_extreme_weather: 0.65,
    land_conversion_pressure: 0.70, regenerative_agriculture_adoption_gap: 0.68,
    soil_acidification_rate: 0.65, phosphorus_depletion_trajectory: 0.88,
    groundwater_contamination_from_soil: 0.72, soil_food_web_collapse: 0.68,
    land_tenure_insecurity: 0.60, monoculture_soil_exhaustion_rate: 0.60,
    urban_soil_sealing_expansion: 0.55,
  },
];

type SDEInput = typeof MOCK_ENTITIES[0];

function physicalScore(e: SDEInput): number {
  return Math.round((e.topsoil_loss_acceleration_rate * 0.4 + e.soil_erosion_from_extreme_weather * 0.35 + e.compaction_crisis_density * 0.25) * 100 * 100) / 100;
}
function chemicalScore(e: SDEInput): number {
  return Math.round((e.agricultural_chemical_soil_toxicity * 0.4 + e.soil_acidification_rate * 0.35 + e.irrigation_salt_accumulation * 0.25) * 100 * 100) / 100;
}
function biologicalScore(e: SDEInput): number {
  return Math.round((e.microbiome_diversity_collapse * 0.4 + e.soil_food_web_collapse * 0.35 + e.soil_carbon_depletion_index * 0.25) * 100 * 100) / 100;
}
function systemicScore(e: SDEInput): number {
  return Math.round((e.desertification_expansion_rate * 0.4 + e.monoculture_soil_exhaustion_rate * 0.35 + e.regenerative_agriculture_adoption_gap * 0.25) * 100 * 100) / 100;
}
function compositeScore(phys: number, chem: number, bio: number, sys: number): number {
  return Math.round((phys * 0.30 + chem * 0.25 + bio * 0.25 + sys * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function soilPattern(e: SDEInput): string {
  if (e.topsoil_loss_acceleration_rate >= 0.70 && e.monoculture_soil_exhaustion_rate >= 0.65) return "topsoil_extinction";
  if (e.microbiome_diversity_collapse >= 0.70 && e.soil_food_web_collapse >= 0.65) return "soil_biome_collapse";
  if (e.desertification_expansion_rate >= 0.70 && e.soil_erosion_from_extreme_weather >= 0.65) return "desertification_cascade";
  if (e.agricultural_chemical_soil_toxicity >= 0.70 && e.soil_acidification_rate >= 0.65) return "chemical_soil_death";
  if (e.phosphorus_depletion_trajectory >= 0.70 && e.soil_carbon_depletion_index >= 0.65) return "phosphorus_crisis";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "extinction_sol_systémique";
  if (composite >= 40) return "crise_dégradation_sols_majeure";
  if (composite >= 20) return "dégradation_sols_structurelle";
  return "sols_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "régénération_urgente_sols_critiques";
  if (risk === "high") return "transition_agriculture_régénératrice_accélérée";
  if (risk === "moderate") return "renforcement_protection_sols";
  return "veille_santé_sols_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Extinction sol systémique — fondement alimentaire en péril";
  if (risk === "high") return "🟠 Crise dégradation sols majeure détectée";
  if (risk === "moderate") return "🟡 Dégradation sols structurelle active";
  return "🟢 Santé sols sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const phys  = physicalScore(e);
      const chem  = chemicalScore(e);
      const bio   = biologicalScore(e);
      const sys   = systemicScore(e);
      const comp  = compositeScore(phys, chem, bio, sys);
      const risk  = riskLevel(comp);
      const pat   = soilPattern(e);
      const sev   = severity(comp);
      const action = recommendedAction(risk);
      const sig   = signal(risk);
      return {
        entity_id:                        e.entity_id,
        land_type:                        e.land_type,
        region:                           e.region,
        physical_score:                   phys,
        chemical_score:                   chem,
        biological_score:                 bio,
        systemic_score:                   sys,
        composite_score:                  comp,
        risk_level:                       risk,
        soil_pattern:                     pat,
        severity:                         sev,
        recommended_action:               action,
        signal:                           sig,
        topsoil_loss_acceleration_rate:   e.topsoil_loss_acceleration_rate,
        desertification_expansion_rate:   e.desertification_expansion_rate,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tPhys = 0, tChem = 0, tBio = 0, tSys = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.soil_pattern]      = (pattern_distribution[ent.soil_pattern]      || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tPhys += ent.physical_score;
      tChem += ent.chemical_score;
      tBio  += ent.biological_score;
      tSys  += ent.systemic_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                            356,
      module_name:                          "Soil Degradation & Land Collapse Intelligence Engine",
      total_entities:                       n,
      critical_count:                       criticalCount,
      high_count:                           highCount,
      moderate_count:                       moderateCount,
      low_count:                            lowCount,
      avg_composite:                        avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_soil_degradation_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "soil-degradation-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/soil-degradation-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "soil-degradation-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "soil-degradation-engine"),
      { status: 502 }
    );
  }
}
