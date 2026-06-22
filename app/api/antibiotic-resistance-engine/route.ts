import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // ARE-001 — critical, post_antibiotic_era (last_resort>=0.70, pipeline_drought>=0.65)
  {
    id: "ARE-001", health_context: "résistance_last_resort", region: "EMEA",
    AMR_mortality_acceleration_rate: 0.82, last_resort_antibiotic_failure_rate: 0.88,
    agricultural_antibiotic_overuse_index: 0.72, hospital_acquired_AMR_prevalence: 0.68,
    AMR_surveillance_gap_index: 0.75, new_antibiotic_pipeline_drought: 0.80,
    global_AMR_spread_velocity: 0.78, poor_hygiene_AMR_amplification: 0.70,
    AMR_travel_transmission_rate: 0.65, pharmaceutical_industry_AMR_neglect: 0.78,
    wastewater_AMR_contamination: 0.72, soil_AMR_reservoir_expansion: 0.68,
    AMR_impact_on_surgery_safety: 0.80, AMR_impact_on_cancer_treatment: 0.75,
    AMR_poverty_mortality_amplification: 0.72, one_health_AMR_approach_deficit: 0.68,
    AMR_geopolitical_cooperation_failure: 0.75,
  },
  // ARE-002 — low, none
  {
    id: "ARE-002", health_context: "surveillance_de_base", region: "NOAM",
    AMR_mortality_acceleration_rate: 0.10, last_resort_antibiotic_failure_rate: 0.08,
    agricultural_antibiotic_overuse_index: 0.12, hospital_acquired_AMR_prevalence: 0.10,
    AMR_surveillance_gap_index: 0.08, new_antibiotic_pipeline_drought: 0.12,
    global_AMR_spread_velocity: 0.10, poor_hygiene_AMR_amplification: 0.08,
    AMR_travel_transmission_rate: 0.10, pharmaceutical_industry_AMR_neglect: 0.12,
    wastewater_AMR_contamination: 0.08, soil_AMR_reservoir_expansion: 0.10,
    AMR_impact_on_surgery_safety: 0.12, AMR_impact_on_cancer_treatment: 0.08,
    AMR_poverty_mortality_amplification: 0.10, one_health_AMR_approach_deficit: 0.12,
    AMR_geopolitical_cooperation_failure: 0.08,
  },
  // ARE-003 — high, agricultural_AMR_reservoir (agri>=0.70, soil>=0.65)
  {
    id: "ARE-003", health_context: "agriculture_intensive", region: "APAC",
    AMR_mortality_acceleration_rate: 0.48, last_resort_antibiotic_failure_rate: 0.50,
    agricultural_antibiotic_overuse_index: 0.82, hospital_acquired_AMR_prevalence: 0.45,
    AMR_surveillance_gap_index: 0.50, new_antibiotic_pipeline_drought: 0.48,
    global_AMR_spread_velocity: 0.52, poor_hygiene_AMR_amplification: 0.50,
    AMR_travel_transmission_rate: 0.45, pharmaceutical_industry_AMR_neglect: 0.50,
    wastewater_AMR_contamination: 0.55, soil_AMR_reservoir_expansion: 0.72,
    AMR_impact_on_surgery_safety: 0.48, AMR_impact_on_cancer_treatment: 0.45,
    AMR_poverty_mortality_amplification: 0.52, one_health_AMR_approach_deficit: 0.50,
    AMR_geopolitical_cooperation_failure: 0.48,
  },
  // ARE-004 — low, none
  {
    id: "ARE-004", health_context: "environnement_contrôlé", region: "LATAM",
    AMR_mortality_acceleration_rate: 0.14, last_resort_antibiotic_failure_rate: 0.12,
    agricultural_antibiotic_overuse_index: 0.15, hospital_acquired_AMR_prevalence: 0.12,
    AMR_surveillance_gap_index: 0.14, new_antibiotic_pipeline_drought: 0.10,
    global_AMR_spread_velocity: 0.12, poor_hygiene_AMR_amplification: 0.15,
    AMR_travel_transmission_rate: 0.12, pharmaceutical_industry_AMR_neglect: 0.14,
    wastewater_AMR_contamination: 0.10, soil_AMR_reservoir_expansion: 0.12,
    AMR_impact_on_surgery_safety: 0.14, AMR_impact_on_cancer_treatment: 0.12,
    AMR_poverty_mortality_amplification: 0.15, one_health_AMR_approach_deficit: 0.12,
    AMR_geopolitical_cooperation_failure: 0.14,
  },
  // ARE-005 — critical, hospital_AMR_catastrophe (hospital>=0.70, surgery>=0.65)
  {
    id: "ARE-005", health_context: "infections_nosocomiales", region: "MEA",
    AMR_mortality_acceleration_rate: 0.78, last_resort_antibiotic_failure_rate: 0.65,
    agricultural_antibiotic_overuse_index: 0.70, hospital_acquired_AMR_prevalence: 0.88,
    AMR_surveillance_gap_index: 0.72, new_antibiotic_pipeline_drought: 0.60,
    global_AMR_spread_velocity: 0.75, poor_hygiene_AMR_amplification: 0.80,
    AMR_travel_transmission_rate: 0.62, pharmaceutical_industry_AMR_neglect: 0.70,
    wastewater_AMR_contamination: 0.68, soil_AMR_reservoir_expansion: 0.62,
    AMR_impact_on_surgery_safety: 0.85, AMR_impact_on_cancer_treatment: 0.78,
    AMR_poverty_mortality_amplification: 0.70, one_health_AMR_approach_deficit: 0.65,
    AMR_geopolitical_cooperation_failure: 0.72,
  },
  // ARE-006 — moderate, none
  {
    id: "ARE-006", health_context: "résistance_émergente", region: "EMEA",
    AMR_mortality_acceleration_rate: 0.30, last_resort_antibiotic_failure_rate: 0.28,
    agricultural_antibiotic_overuse_index: 0.32, hospital_acquired_AMR_prevalence: 0.28,
    AMR_surveillance_gap_index: 0.30, new_antibiotic_pipeline_drought: 0.32,
    global_AMR_spread_velocity: 0.28, poor_hygiene_AMR_amplification: 0.30,
    AMR_travel_transmission_rate: 0.32, pharmaceutical_industry_AMR_neglect: 0.28,
    wastewater_AMR_contamination: 0.30, soil_AMR_reservoir_expansion: 0.28,
    AMR_impact_on_surgery_safety: 0.32, AMR_impact_on_cancer_treatment: 0.30,
    AMR_poverty_mortality_amplification: 0.28, one_health_AMR_approach_deficit: 0.30,
    AMR_geopolitical_cooperation_failure: 0.32,
  },
  // ARE-007 — high, AMR_global_spread (spread>=0.70, travel>=0.65)
  {
    id: "ARE-007", health_context: "dissémination_mondiale", region: "NOAM",
    AMR_mortality_acceleration_rate: 0.52, last_resort_antibiotic_failure_rate: 0.48,
    agricultural_antibiotic_overuse_index: 0.50, hospital_acquired_AMR_prevalence: 0.52,
    AMR_surveillance_gap_index: 0.48, new_antibiotic_pipeline_drought: 0.52,
    global_AMR_spread_velocity: 0.78, poor_hygiene_AMR_amplification: 0.50,
    AMR_travel_transmission_rate: 0.72, pharmaceutical_industry_AMR_neglect: 0.50,
    wastewater_AMR_contamination: 0.52, soil_AMR_reservoir_expansion: 0.48,
    AMR_impact_on_surgery_safety: 0.50, AMR_impact_on_cancer_treatment: 0.52,
    AMR_poverty_mortality_amplification: 0.50, one_health_AMR_approach_deficit: 0.48,
    AMR_geopolitical_cooperation_failure: 0.52,
  },
  // ARE-008 — critical, pharmaceutical_neglect_crisis (pharma>=0.70, one_health>=0.65)
  {
    id: "ARE-008", health_context: "négligence_pharmaceutique", region: "APAC",
    AMR_mortality_acceleration_rate: 0.75, last_resort_antibiotic_failure_rate: 0.68,
    agricultural_antibiotic_overuse_index: 0.65, hospital_acquired_AMR_prevalence: 0.60,
    AMR_surveillance_gap_index: 0.78, new_antibiotic_pipeline_drought: 0.62,
    global_AMR_spread_velocity: 0.72, poor_hygiene_AMR_amplification: 0.68,
    AMR_travel_transmission_rate: 0.60, pharmaceutical_industry_AMR_neglect: 0.88,
    wastewater_AMR_contamination: 0.70, soil_AMR_reservoir_expansion: 0.65,
    AMR_impact_on_surgery_safety: 0.60, AMR_impact_on_cancer_treatment: 0.68,
    AMR_poverty_mortality_amplification: 0.75, one_health_AMR_approach_deficit: 0.80,
    AMR_geopolitical_cooperation_failure: 0.78,
  },
];

type AREInput = typeof MOCK_ENTITIES[0];

function resistanceScore(e: AREInput): number {
  return Math.round((e.last_resort_antibiotic_failure_rate * 0.4 + e.AMR_mortality_acceleration_rate * 0.35 + e.global_AMR_spread_velocity * 0.25) * 100 * 100) / 100;
}
function pipelineScore(e: AREInput): number {
  return Math.round((e.new_antibiotic_pipeline_drought * 0.4 + e.pharmaceutical_industry_AMR_neglect * 0.35 + e.AMR_surveillance_gap_index * 0.25) * 100 * 100) / 100;
}
function transmissionScore(e: AREInput): number {
  return Math.round((e.agricultural_antibiotic_overuse_index * 0.4 + e.wastewater_AMR_contamination * 0.35 + e.soil_AMR_reservoir_expansion * 0.25) * 100 * 100) / 100;
}
function systemicScore(e: AREInput): number {
  return Math.round((e.one_health_AMR_approach_deficit * 0.4 + e.AMR_geopolitical_cooperation_failure * 0.35 + e.AMR_poverty_mortality_amplification * 0.25) * 100 * 100) / 100;
}
function compositeScore(res: number, pipe: number, trans: number, sys: number): number {
  return Math.round((res * 0.30 + pipe * 0.25 + trans * 0.25 + sys * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function amrPattern(e: AREInput): string {
  if (e.last_resort_antibiotic_failure_rate >= 0.70 && e.new_antibiotic_pipeline_drought >= 0.65) return "post_antibiotic_era";
  if (e.agricultural_antibiotic_overuse_index >= 0.70 && e.soil_AMR_reservoir_expansion >= 0.65) return "agricultural_AMR_reservoir";
  if (e.hospital_acquired_AMR_prevalence >= 0.70 && e.AMR_impact_on_surgery_safety >= 0.65) return "hospital_AMR_catastrophe";
  if (e.global_AMR_spread_velocity >= 0.70 && e.AMR_travel_transmission_rate >= 0.65) return "AMR_global_spread";
  if (e.pharmaceutical_industry_AMR_neglect >= 0.70 && e.one_health_AMR_approach_deficit >= 0.65) return "pharmaceutical_neglect_crisis";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "ère_post-antibiotique_systémique";
  if (composite >= 40) return "crise_résistance_antibiotique_majeure";
  if (composite >= 20) return "résistance_antibiotique_structurelle";
  return "AMR_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_AMR_urgence_mondiale";
  if (risk === "high") return "pipeline_antibiotique_urgence";
  if (risk === "moderate") return "renforcement_surveillance_AMR_systémique";
  return "veille_AMR_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Ère post-antibiotique — résistance antimicrobienne critique";
  if (risk === "high") return "🟠 Crise résistance antibiotique majeure détectée";
  if (risk === "moderate") return "🟡 Résistance antibiotique structurelle active";
  return "🟢 AMR sous surveillance et contenu";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[antibiotic-resistance-engine] SWARM_API_URL non défini — mode dégradé activé");
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
      pattern_distribution[ent.amr_pattern]       = (pattern_distribution[ent.amr_pattern]       || 0) + 1;
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
      module_id:                    358,
      module_name:                  "Antibiotic Resistance & Post-Antibiotic Era Intelligence Engine",
      total_entities:               n,
      critical_count:               criticalCount,
      high_count:                   highCount,
      moderate_count:               moderateCount,
      low_count:                    lowCount,
      avg_composite:                avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_AMR_risk_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "antibiotic-resistance-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/antibiotic-resistance-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return sealResponse(NextResponse.json(sealResponse(await upstream.json(), "antibiotic-resistance-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "antibiotic-resistance-engine"),
      { status: 502 }
    ));
  }
}
