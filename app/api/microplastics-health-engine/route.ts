import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[microplastics-health-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  // MPH-001 — critical, endocrine_disruption_epidemic (endocrine>0.85, chem_add>0.80)
  {
    id: "MPH-001", exposure_route: "ingestion_alimentaire", region: "NOAM",
    blood_microplastic_concentration: 0.88, lung_particle_accumulation: 0.82,
    digestive_system_exposure: 0.80, endocrine_disruption_risk: 0.90,
    cardiovascular_inflammation: 0.75, placental_crossing_rate: 0.72,
    neurotoxicity_indicator: 0.70, carcinogenicity_evidence: 0.68,
    daily_ingestion_estimate: 0.85, air_inhalation_intensity: 0.72,
    food_packaging_leaching: 0.82, seafood_contamination: 0.75,
    drinking_water_particles: 0.70, skin_absorption_rate: 0.62,
    chemical_additive_toxicity: 0.85, bioaccumulation_factor: 0.78,
    regulatory_detection_gap: 0.80,
  },
  // MPH-002 — critical, cardiovascular_microplastic_crisis (cardio>0.85, blood>0.80)
  {
    id: "MPH-002", exposure_route: "inhalation_atmosphérique", region: "APAC",
    blood_microplastic_concentration: 0.88, lung_particle_accumulation: 0.85,
    digestive_system_exposure: 0.78, endocrine_disruption_risk: 0.72,
    cardiovascular_inflammation: 0.90, placental_crossing_rate: 0.68,
    neurotoxicity_indicator: 0.74, carcinogenicity_evidence: 0.72,
    daily_ingestion_estimate: 0.78, air_inhalation_intensity: 0.88,
    food_packaging_leaching: 0.75, seafood_contamination: 0.72,
    drinking_water_particles: 0.68, skin_absorption_rate: 0.65,
    chemical_additive_toxicity: 0.78, bioaccumulation_factor: 0.75,
    regulatory_detection_gap: 0.82,
  },
  // MPH-003 — critical, maternal_fetal_exposure_trap (placental>0.85, neuro>0.80)
  {
    id: "MPH-003", exposure_route: "transfert_placentaire", region: "EMEA",
    blood_microplastic_concentration: 0.78, lung_particle_accumulation: 0.72,
    digestive_system_exposure: 0.75, endocrine_disruption_risk: 0.78,
    cardiovascular_inflammation: 0.72, placental_crossing_rate: 0.90,
    neurotoxicity_indicator: 0.85, carcinogenicity_evidence: 0.80,
    daily_ingestion_estimate: 0.82, air_inhalation_intensity: 0.70,
    food_packaging_leaching: 0.78, seafood_contamination: 0.75,
    drinking_water_particles: 0.72, skin_absorption_rate: 0.65,
    chemical_additive_toxicity: 0.75, bioaccumulation_factor: 0.78,
    regulatory_detection_gap: 0.80,
  },
  // MPH-004 — high, food_chain_saturation_collapse (seafood>0.85, food_pack>0.80)
  {
    id: "MPH-004", exposure_route: "contamination_chaîne_alimentaire", region: "SSA",
    blood_microplastic_concentration: 0.42, lung_particle_accumulation: 0.40,
    digestive_system_exposure: 0.45, endocrine_disruption_risk: 0.40,
    cardiovascular_inflammation: 0.38, placental_crossing_rate: 0.38,
    neurotoxicity_indicator: 0.40, carcinogenicity_evidence: 0.38,
    daily_ingestion_estimate: 0.45, air_inhalation_intensity: 0.38,
    food_packaging_leaching: 0.85, seafood_contamination: 0.90,
    drinking_water_particles: 0.42, skin_absorption_rate: 0.35,
    chemical_additive_toxicity: 0.42, bioaccumulation_factor: 0.45,
    regulatory_detection_gap: 0.42,
  },
  // MPH-005 — high, regulatory_threshold_vacuum (reg_gap>0.85, bioaccum>0.80)
  {
    id: "MPH-005", exposure_route: "accumulation_bioaccumulation", region: "LATAM",
    blood_microplastic_concentration: 0.52, lung_particle_accumulation: 0.50,
    digestive_system_exposure: 0.55, endocrine_disruption_risk: 0.52,
    cardiovascular_inflammation: 0.48, placental_crossing_rate: 0.50,
    neurotoxicity_indicator: 0.52, carcinogenicity_evidence: 0.55,
    daily_ingestion_estimate: 0.58, air_inhalation_intensity: 0.50,
    food_packaging_leaching: 0.55, seafood_contamination: 0.52,
    drinking_water_particles: 0.50, skin_absorption_rate: 0.48,
    chemical_additive_toxicity: 0.55, bioaccumulation_factor: 0.85,
    regulatory_detection_gap: 0.90,
  },
  // MPH-006 — moderate, none
  {
    id: "MPH-006", exposure_route: "absorption_cutanée", region: "MENA",
    blood_microplastic_concentration: 0.28, lung_particle_accumulation: 0.30,
    digestive_system_exposure: 0.28, endocrine_disruption_risk: 0.30,
    cardiovascular_inflammation: 0.28, placental_crossing_rate: 0.25,
    neurotoxicity_indicator: 0.28, carcinogenicity_evidence: 0.25,
    daily_ingestion_estimate: 0.30, air_inhalation_intensity: 0.28,
    food_packaging_leaching: 0.30, seafood_contamination: 0.28,
    drinking_water_particles: 0.30, skin_absorption_rate: 0.32,
    chemical_additive_toxicity: 0.28, bioaccumulation_factor: 0.30,
    regulatory_detection_gap: 0.28,
  },
  // MPH-007 — low, none
  {
    id: "MPH-007", exposure_route: "eau_potable_filtrée", region: "EMEA",
    blood_microplastic_concentration: 0.10, lung_particle_accumulation: 0.08,
    digestive_system_exposure: 0.10, endocrine_disruption_risk: 0.10,
    cardiovascular_inflammation: 0.08, placental_crossing_rate: 0.08,
    neurotoxicity_indicator: 0.10, carcinogenicity_evidence: 0.08,
    daily_ingestion_estimate: 0.10, air_inhalation_intensity: 0.08,
    food_packaging_leaching: 0.10, seafood_contamination: 0.08,
    drinking_water_particles: 0.12, skin_absorption_rate: 0.10,
    chemical_additive_toxicity: 0.08, bioaccumulation_factor: 0.10,
    regulatory_detection_gap: 0.10,
  },
  // MPH-008 — low, none
  {
    id: "MPH-008", exposure_route: "milieu_rural_protégé", region: "NOAM",
    blood_microplastic_concentration: 0.12, lung_particle_accumulation: 0.10,
    digestive_system_exposure: 0.12, endocrine_disruption_risk: 0.10,
    cardiovascular_inflammation: 0.12, placental_crossing_rate: 0.10,
    neurotoxicity_indicator: 0.12, carcinogenicity_evidence: 0.10,
    daily_ingestion_estimate: 0.12, air_inhalation_intensity: 0.10,
    food_packaging_leaching: 0.12, seafood_contamination: 0.10,
    drinking_water_particles: 0.10, skin_absorption_rate: 0.12,
    chemical_additive_toxicity: 0.10, bioaccumulation_factor: 0.12,
    regulatory_detection_gap: 0.10,
  },
];

type MPHInput = (typeof MOCK_ENTITIES)[0];

function exposureScore(e: MPHInput): number {
  return Math.round((e.blood_microplastic_concentration * 0.4 + e.lung_particle_accumulation * 0.35 + e.digestive_system_exposure * 0.25) * 100 * 100) / 100;
}
function healthScore(e: MPHInput): number {
  return Math.round((e.endocrine_disruption_risk * 0.4 + e.cardiovascular_inflammation * 0.35 + e.neurotoxicity_indicator * 0.25) * 100 * 100) / 100;
}
function sourceScore(e: MPHInput): number {
  return Math.round((e.food_packaging_leaching * 0.4 + e.seafood_contamination * 0.35 + e.drinking_water_particles * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: MPHInput): number {
  return Math.round((e.regulatory_detection_gap * 0.4 + e.chemical_additive_toxicity * 0.35 + e.bioaccumulation_factor * 0.25) * 100 * 100) / 100;
}
function compositeScore(exp: number, hlt: number, src: number, gov: number): number {
  return Math.round((exp * 0.30 + hlt * 0.25 + src * 0.25 + gov * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function healthPattern(e: MPHInput): string {
  if (e.endocrine_disruption_risk > 0.85 && e.chemical_additive_toxicity > 0.80) return "endocrine_disruption_epidemic";
  if (e.cardiovascular_inflammation > 0.85 && e.blood_microplastic_concentration > 0.80) return "cardiovascular_microplastic_crisis";
  if (e.placental_crossing_rate > 0.85 && e.neurotoxicity_indicator > 0.80) return "maternal_fetal_exposure_trap";
  if (e.seafood_contamination > 0.85 && e.food_packaging_leaching > 0.80) return "food_chain_saturation_collapse";
  if (e.regulatory_detection_gap > 0.85 && e.bioaccumulation_factor > 0.80) return "regulatory_threshold_vacuum";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_microplastiques_santé_systémique";
  if (composite >= 40) return "crise_contamination_microplastique_majeure";
  if (composite >= 20) return "exposition_microplastique_structurelle";
  return "surveillance_microplastiques_continue";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_décontamination_microplastique_critique";
  if (risk === "high") return "réduction_exposition_sources_microplastiques_prioritaires";
  if (risk === "moderate") return "renforcement_détection_régulation_microplastiques";
  return "veille_exposition_microplastique_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise microplastiques santé systémique — impact sanitaire en péril";
  if (risk === "high") return "🟠 Crise contamination microplastique majeure détectée";
  if (risk === "moderate") return "🟡 Exposition microplastique structurelle active";
  return "🟢 Surveillance microplastiques en cours";
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const exp  = exposureScore(e);
      const hlt  = healthScore(e);
      const src  = sourceScore(e);
      const gov  = governanceScore(e);
      const comp = compositeScore(exp, hlt, src, gov);
      const risk = riskLevel(comp);
      const pat  = healthPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:                        e.entity_id,
        exposure_route:                   e.exposure_route,
        region:                           e.region,
        exposure_score:                   exp,
        health_score:                     hlt,
        source_score:                     src,
        governance_score:                 gov,
        composite_score:                  comp,
        risk_level:                       risk,
        health_pattern:                   pat,
        severity:                         sev,
        recommended_action:               action,
        signal:                           sig,
        blood_microplastic_concentration: e.blood_microplastic_concentration,
        lung_particle_accumulation:       e.lung_particle_accumulation,
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
      pattern_distribution[ent.health_pattern]    = (pattern_distribution[ent.health_pattern]    || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                               426,
      module_name:                             "Microplastiques & Impact Santé Humaine Intelligence Engine",
      total:                                   n,
      critical:                                criticalCount,
      high:                                    highCount,
      moderate:                                moderateCount,
      low:                                     lowCount,
      avg_composite:                           avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_microplastic_health_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>)));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/microplastics-health-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(sealResponse(await res.json())));
  } catch {}
  return sealResponse(NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 }));
}
