import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // EHE-001 — critical, epigenetic_catastrophe (epigenetic_toxin>=0.70, intergenerational>=0.65)
  {
    id: "EHE-001", health_domain: "epigenetic_toxicology", region: "EMEA",
    epigenetic_toxin_exposure_rate: 0.88, endocrine_disruption_prevalence: 0.75,
    microplastic_bioaccumulation_index: 0.80, air_quality_chronic_disease_coupling: 0.82,
    heavy_metal_cognitive_impairment_rate: 0.78, pesticide_epigenetic_impact: 0.72,
    forever_chemical_contamination_level: 0.65, gut_microbiome_disruption_index: 0.70,
    intergenerational_epigenetic_damage: 0.85, environmental_health_inequality: 0.78,
    chemical_industry_capture_of_regulation: 0.68, biodiversity_loss_health_cascade: 0.75,
    noise_pollution_cardiovascular_risk: 0.65, light_pollution_circadian_disruption: 0.60,
    urban_heat_mortality_index: 0.78, soil_contamination_food_chain_risk: 0.72,
    industrial_waste_community_exposure: 0.68,
  },
  // EHE-002 — low, none
  {
    id: "EHE-002", health_domain: "environmental_baseline", region: "NOAM",
    epigenetic_toxin_exposure_rate: 0.10, endocrine_disruption_prevalence: 0.12,
    microplastic_bioaccumulation_index: 0.08, air_quality_chronic_disease_coupling: 0.10,
    heavy_metal_cognitive_impairment_rate: 0.12, pesticide_epigenetic_impact: 0.08,
    forever_chemical_contamination_level: 0.10, gut_microbiome_disruption_index: 0.12,
    intergenerational_epigenetic_damage: 0.08, environmental_health_inequality: 0.10,
    chemical_industry_capture_of_regulation: 0.12, biodiversity_loss_health_cascade: 0.10,
    noise_pollution_cardiovascular_risk: 0.08, light_pollution_circadian_disruption: 0.10,
    urban_heat_mortality_index: 0.12, soil_contamination_food_chain_risk: 0.10,
    industrial_waste_community_exposure: 0.08,
  },
  // EHE-003 — high, chemical_body_burden (forever>=0.70, endocrine>=0.65)
  {
    id: "EHE-003", health_domain: "chemical_contamination", region: "APAC",
    epigenetic_toxin_exposure_rate: 0.52, endocrine_disruption_prevalence: 0.68,
    microplastic_bioaccumulation_index: 0.48, air_quality_chronic_disease_coupling: 0.50,
    heavy_metal_cognitive_impairment_rate: 0.45, pesticide_epigenetic_impact: 0.50,
    forever_chemical_contamination_level: 0.75, gut_microbiome_disruption_index: 0.52,
    intergenerational_epigenetic_damage: 0.45, environmental_health_inequality: 0.50,
    chemical_industry_capture_of_regulation: 0.48, biodiversity_loss_health_cascade: 0.52,
    noise_pollution_cardiovascular_risk: 0.45, light_pollution_circadian_disruption: 0.48,
    urban_heat_mortality_index: 0.50, soil_contamination_food_chain_risk: 0.48,
    industrial_waste_community_exposure: 0.45,
  },
  // EHE-004 — low, none
  {
    id: "EHE-004", health_domain: "environmental_baseline", region: "LATAM",
    epigenetic_toxin_exposure_rate: 0.15, endocrine_disruption_prevalence: 0.14,
    microplastic_bioaccumulation_index: 0.12, air_quality_chronic_disease_coupling: 0.14,
    heavy_metal_cognitive_impairment_rate: 0.15, pesticide_epigenetic_impact: 0.12,
    forever_chemical_contamination_level: 0.14, gut_microbiome_disruption_index: 0.15,
    intergenerational_epigenetic_damage: 0.12, environmental_health_inequality: 0.15,
    chemical_industry_capture_of_regulation: 0.14, biodiversity_loss_health_cascade: 0.12,
    noise_pollution_cardiovascular_risk: 0.14, light_pollution_circadian_disruption: 0.12,
    urban_heat_mortality_index: 0.14, soil_contamination_food_chain_risk: 0.15,
    industrial_waste_community_exposure: 0.12,
  },
  // EHE-005 — critical, microbiome_collapse (microplastic>=0.70, gut>=0.65)
  {
    id: "EHE-005", health_domain: "microbiome_health", region: "MEA",
    epigenetic_toxin_exposure_rate: 0.78, endocrine_disruption_prevalence: 0.72,
    microplastic_bioaccumulation_index: 0.85, air_quality_chronic_disease_coupling: 0.78,
    heavy_metal_cognitive_impairment_rate: 0.70, pesticide_epigenetic_impact: 0.68,
    forever_chemical_contamination_level: 0.62, gut_microbiome_disruption_index: 0.80,
    intergenerational_epigenetic_damage: 0.55, environmental_health_inequality: 0.72,
    chemical_industry_capture_of_regulation: 0.62, biodiversity_loss_health_cascade: 0.70,
    noise_pollution_cardiovascular_risk: 0.65, light_pollution_circadian_disruption: 0.62,
    urban_heat_mortality_index: 0.75, soil_contamination_food_chain_risk: 0.68,
    industrial_waste_community_exposure: 0.60,
  },
  // EHE-006 — moderate, none
  {
    id: "EHE-006", health_domain: "urban_environment", region: "EMEA",
    epigenetic_toxin_exposure_rate: 0.30, endocrine_disruption_prevalence: 0.28,
    microplastic_bioaccumulation_index: 0.32, air_quality_chronic_disease_coupling: 0.30,
    heavy_metal_cognitive_impairment_rate: 0.28, pesticide_epigenetic_impact: 0.30,
    forever_chemical_contamination_level: 0.28, gut_microbiome_disruption_index: 0.30,
    intergenerational_epigenetic_damage: 0.28, environmental_health_inequality: 0.32,
    chemical_industry_capture_of_regulation: 0.30, biodiversity_loss_health_cascade: 0.28,
    noise_pollution_cardiovascular_risk: 0.30, light_pollution_circadian_disruption: 0.28,
    urban_heat_mortality_index: 0.30, soil_contamination_food_chain_risk: 0.32,
    industrial_waste_community_exposure: 0.28,
  },
  // EHE-007 — high, environmental_injustice (inequality>=0.70, industrial_waste>=0.65)
  {
    id: "EHE-007", health_domain: "environmental_justice", region: "NOAM",
    epigenetic_toxin_exposure_rate: 0.52, endocrine_disruption_prevalence: 0.50,
    microplastic_bioaccumulation_index: 0.48, air_quality_chronic_disease_coupling: 0.55,
    heavy_metal_cognitive_impairment_rate: 0.50, pesticide_epigenetic_impact: 0.48,
    forever_chemical_contamination_level: 0.52, gut_microbiome_disruption_index: 0.50,
    intergenerational_epigenetic_damage: 0.48, environmental_health_inequality: 0.78,
    chemical_industry_capture_of_regulation: 0.52, biodiversity_loss_health_cascade: 0.50,
    noise_pollution_cardiovascular_risk: 0.48, light_pollution_circadian_disruption: 0.50,
    urban_heat_mortality_index: 0.52, soil_contamination_food_chain_risk: 0.50,
    industrial_waste_community_exposure: 0.72,
  },
  // EHE-008 — critical, regulatory_chemical_capture (chemical_capture>=0.70, air_quality>=0.65)
  {
    id: "EHE-008", health_domain: "regulatory_environment", region: "APAC",
    epigenetic_toxin_exposure_rate: 0.65, endocrine_disruption_prevalence: 0.78,
    microplastic_bioaccumulation_index: 0.60, air_quality_chronic_disease_coupling: 0.82,
    heavy_metal_cognitive_impairment_rate: 0.72, pesticide_epigenetic_impact: 0.68,
    forever_chemical_contamination_level: 0.62, gut_microbiome_disruption_index: 0.60,
    intergenerational_epigenetic_damage: 0.58, environmental_health_inequality: 0.65,
    chemical_industry_capture_of_regulation: 0.88, biodiversity_loss_health_cascade: 0.78,
    noise_pollution_cardiovascular_risk: 0.68, light_pollution_circadian_disruption: 0.65,
    urban_heat_mortality_index: 0.80, soil_contamination_food_chain_risk: 0.75,
    industrial_waste_community_exposure: 0.60,
  },
];

type EHEInput = typeof MOCK_ENTITIES[0];

function chemicalScore(e: EHEInput): number {
  return Math.round((e.epigenetic_toxin_exposure_rate * 0.4 + e.forever_chemical_contamination_level * 0.35 + e.endocrine_disruption_prevalence * 0.25) * 100 * 100) / 100;
}
function biologicalScore(e: EHEInput): number {
  return Math.round((e.microplastic_bioaccumulation_index * 0.4 + e.gut_microbiome_disruption_index * 0.35 + e.intergenerational_epigenetic_damage * 0.25) * 100 * 100) / 100;
}
function environmentalScore(e: EHEInput): number {
  return Math.round((e.air_quality_chronic_disease_coupling * 0.4 + e.urban_heat_mortality_index * 0.35 + e.biodiversity_loss_health_cascade * 0.25) * 100 * 100) / 100;
}
function socialScore(e: EHEInput): number {
  return Math.round((e.environmental_health_inequality * 0.4 + e.chemical_industry_capture_of_regulation * 0.35 + e.industrial_waste_community_exposure * 0.25) * 100 * 100) / 100;
}
function compositeScore(chem: number, bio: number, env: number, soc: number): number {
  return Math.round((chem * 0.30 + bio * 0.25 + env * 0.25 + soc * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function healthPattern(e: EHEInput): string {
  if (e.epigenetic_toxin_exposure_rate >= 0.70 && e.intergenerational_epigenetic_damage >= 0.65) return "epigenetic_catastrophe";
  if (e.forever_chemical_contamination_level >= 0.70 && e.endocrine_disruption_prevalence >= 0.65) return "chemical_body_burden";
  if (e.microplastic_bioaccumulation_index >= 0.70 && e.gut_microbiome_disruption_index >= 0.65) return "microbiome_collapse";
  if (e.environmental_health_inequality >= 0.70 && e.industrial_waste_community_exposure >= 0.65) return "environmental_injustice";
  if (e.chemical_industry_capture_of_regulation >= 0.70 && e.air_quality_chronic_disease_coupling >= 0.65) return "regulatory_chemical_capture";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "catastrophe_sanitaire_environnementale";
  if (composite >= 40) return "crise_santé_épigénétique_majeure";
  if (composite >= 20) return "dégradation_santé_environnementale";
  return "santé_environnementale_contenue";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_sanitaire_urgente";
  if (risk === "high") return "réglementation_chimique_stricte";
  if (risk === "moderate") return "renforcement_prévention_environnementale";
  return "surveillance_épigénétique_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Catastrophe sanitaire environnementale — dommages épigénétiques systémiques";
  if (risk === "high") return "🟠 Crise santé épigénétique majeure détectée";
  if (risk === "moderate") return "🟡 Dégradation santé environnementale active";
  return "🟢 Santé environnementale relativement contenue";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const chem    = chemicalScore(e);
      const bio     = biologicalScore(e);
      const env     = environmentalScore(e);
      const soc     = socialScore(e);
      const comp    = compositeScore(chem, bio, env, soc);
      const risk    = riskLevel(comp);
      const pattern = healthPattern(e);
      const sev     = severity(comp);
      const action  = recommendedAction(risk);
      const sig     = signal(risk);
      return {
        id:                          e.entity_id,
        health_domain:                      e.health_domain,
        region:                             e.region,
        chemical_score:                     chem,
        biological_score:                   bio,
        environmental_score:                env,
        social_score:                       soc,
        composite_score:                    comp,
        risk_level:                         risk,
        health_pattern:                     pattern,
        severity:                           sev,
        recommended_action:                 action,
        signal:                             sig,
        epigenetic_toxin_exposure_rate:     e.epigenetic_toxin_exposure_rate,
        intergenerational_epigenetic_damage: e.intergenerational_epigenetic_damage,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tChem = 0, tBio = 0, tEnv = 0, tSoc = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]         = (risk_distribution[ent.risk_level]         || 0) + 1;
      pattern_distribution[ent.health_pattern]  = (pattern_distribution[ent.health_pattern]  || 0) + 1;
      severity_distribution[ent.severity]       = (severity_distribution[ent.severity]       || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tChem += ent.chemical_score;
      tBio  += ent.biological_score;
      tEnv  += ent.environmental_score;
      tSoc  += ent.social_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")  criticalCount++;
      else if (ent.risk_level === "high") highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                          340,
      module_name:                        "Epigenetic & Environmental Health Intelligence Engine",
      total_entities:                     n,
      critical_count:                     criticalCount,
      high_count:                         highCount,
      moderate_count:                     moderateCount,
      low_count:                          lowCount,
      avg_composite:                      avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_health_risk_index:    Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "epigenetic-health-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/epigenetic-health-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "epigenetic-health-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "epigenetic-health-engine"),
      { status: 502 }
    );
  }
}
