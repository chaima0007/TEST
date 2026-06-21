import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // UFE-001 — critical, stormwater_infrastructure_collapse (stormwater_age>0.85, drainage_deficit>0.80)
  {
    id: "UFE-001", city_type: "métropole_côtière", region: "APAC",
    flood_frequency_increase: 0.88, impervious_surface_expansion: 0.72,
    stormwater_system_age: 0.90, drainage_capacity_deficit: 0.85,
    combined_sewer_overflow: 0.70, green_infrastructure_adoption: 0.20,
    early_warning_effectiveness: 0.65, emergency_response_capacity: 0.60,
    low_income_flood_exposure: 0.72, climate_vulnerability_index: 0.75,
    insurance_coverage_gap: 0.65, urban_heat_compounding: 0.70,
    sea_level_rise_interaction: 0.80, maintenance_budget_gap: 0.70,
    nature_based_solution_adoption: 0.25, informal_settlement_exposure: 0.65,
    urban_planning_integration: 0.68,
  },
  // UFE-002 — critical, informal_settlement_flood_trap (informal_exp>0.85, low_income_exp>0.80)
  {
    id: "UFE-002", city_type: "ville_deltaïque", region: "SSA",
    flood_frequency_increase: 0.85, impervious_surface_expansion: 0.70,
    stormwater_system_age: 0.72, drainage_capacity_deficit: 0.70,
    combined_sewer_overflow: 0.75, green_infrastructure_adoption: 0.15,
    early_warning_effectiveness: 0.68, emergency_response_capacity: 0.55,
    low_income_flood_exposure: 0.88, climate_vulnerability_index: 0.80,
    insurance_coverage_gap: 0.72, urban_heat_compounding: 0.65,
    sea_level_rise_interaction: 0.75, maintenance_budget_gap: 0.70,
    nature_based_solution_adoption: 0.20, informal_settlement_exposure: 0.90,
    urban_planning_integration: 0.72,
  },
  // UFE-003 — critical, urban_heat_flood_compound (heat_compound>0.85, impervious>0.80)
  {
    id: "UFE-003", city_type: "agglomération_industrielle", region: "EMEA",
    flood_frequency_increase: 0.80, impervious_surface_expansion: 0.88,
    stormwater_system_age: 0.72, drainage_capacity_deficit: 0.75,
    combined_sewer_overflow: 0.72, green_infrastructure_adoption: 0.18,
    early_warning_effectiveness: 0.65, emergency_response_capacity: 0.60,
    low_income_flood_exposure: 0.70, climate_vulnerability_index: 0.78,
    insurance_coverage_gap: 0.68, urban_heat_compounding: 0.90,
    sea_level_rise_interaction: 0.65, maintenance_budget_gap: 0.72,
    nature_based_solution_adoption: 0.22, informal_settlement_exposure: 0.65,
    urban_planning_integration: 0.70,
  },
  // UFE-004 — high, drainage_capacity_failure (cso>0.80, drainage_deficit>0.75)
  {
    id: "UFE-004", city_type: "ville_fluviale", region: "LATAM",
    flood_frequency_increase: 0.55, impervious_surface_expansion: 0.50,
    stormwater_system_age: 0.50, drainage_capacity_deficit: 0.80,
    combined_sewer_overflow: 0.85, green_infrastructure_adoption: 0.30,
    early_warning_effectiveness: 0.50, emergency_response_capacity: 0.48,
    low_income_flood_exposure: 0.52, climate_vulnerability_index: 0.55,
    insurance_coverage_gap: 0.50, urban_heat_compounding: 0.45,
    sea_level_rise_interaction: 0.45, maintenance_budget_gap: 0.50,
    nature_based_solution_adoption: 0.30, informal_settlement_exposure: 0.48,
    urban_planning_integration: 0.52,
  },
  // UFE-005 — high, climate_adaptation_funding_gap (maint_budget>0.80, insurance_gap>0.75)
  {
    id: "UFE-005", city_type: "zone_périurbaine", region: "NOAM",
    flood_frequency_increase: 0.52, impervious_surface_expansion: 0.48,
    stormwater_system_age: 0.50, drainage_capacity_deficit: 0.72,
    combined_sewer_overflow: 0.50, green_infrastructure_adoption: 0.28,
    early_warning_effectiveness: 0.48, emergency_response_capacity: 0.50,
    low_income_flood_exposure: 0.52, climate_vulnerability_index: 0.55,
    insurance_coverage_gap: 0.78, urban_heat_compounding: 0.50,
    sea_level_rise_interaction: 0.45, maintenance_budget_gap: 0.85,
    nature_based_solution_adoption: 0.25, informal_settlement_exposure: 0.48,
    urban_planning_integration: 0.50,
  },
  // UFE-006 — moderate, none
  {
    id: "UFE-006", city_type: "ville_moyenne", region: "EMEA",
    flood_frequency_increase: 0.30, impervious_surface_expansion: 0.28,
    stormwater_system_age: 0.30, drainage_capacity_deficit: 0.30,
    combined_sewer_overflow: 0.28, green_infrastructure_adoption: 0.50,
    early_warning_effectiveness: 0.30, emergency_response_capacity: 0.35,
    low_income_flood_exposure: 0.28, climate_vulnerability_index: 0.30,
    insurance_coverage_gap: 0.28, urban_heat_compounding: 0.28,
    sea_level_rise_interaction: 0.25, maintenance_budget_gap: 0.30,
    nature_based_solution_adoption: 0.45, informal_settlement_exposure: 0.25,
    urban_planning_integration: 0.30,
  },
  // UFE-007 — low, none
  {
    id: "UFE-007", city_type: "agglomération_alpine", region: "EMEA",
    flood_frequency_increase: 0.10, impervious_surface_expansion: 0.12,
    stormwater_system_age: 0.10, drainage_capacity_deficit: 0.10,
    combined_sewer_overflow: 0.08, green_infrastructure_adoption: 0.75,
    early_warning_effectiveness: 0.10, emergency_response_capacity: 0.80,
    low_income_flood_exposure: 0.10, climate_vulnerability_index: 0.12,
    insurance_coverage_gap: 0.10, urban_heat_compounding: 0.08,
    sea_level_rise_interaction: 0.05, maintenance_budget_gap: 0.10,
    nature_based_solution_adoption: 0.70, informal_settlement_exposure: 0.08,
    urban_planning_integration: 0.12,
  },
  // UFE-008 — low, none
  {
    id: "UFE-008", city_type: "commune_rurale_péri-urbaine", region: "NOAM",
    flood_frequency_increase: 0.12, impervious_surface_expansion: 0.10,
    stormwater_system_age: 0.12, drainage_capacity_deficit: 0.10,
    combined_sewer_overflow: 0.10, green_infrastructure_adoption: 0.70,
    early_warning_effectiveness: 0.12, emergency_response_capacity: 0.75,
    low_income_flood_exposure: 0.12, climate_vulnerability_index: 0.10,
    insurance_coverage_gap: 0.12, urban_heat_compounding: 0.10,
    sea_level_rise_interaction: 0.08, maintenance_budget_gap: 0.12,
    nature_based_solution_adoption: 0.65, informal_settlement_exposure: 0.10,
    urban_planning_integration: 0.10,
  },
];

type UFEInput = typeof MOCK_ENTITIES[0];

function exposureScore(e: UFEInput): number {
  return Math.round((e.flood_frequency_increase * 0.40 + e.impervious_surface_expansion * 0.35 + e.sea_level_rise_interaction * 0.25) * 100 * 100) / 100;
}
function infrastructureScore(e: UFEInput): number {
  return Math.round((e.drainage_capacity_deficit * 0.40 + e.stormwater_system_age * 0.35 + e.maintenance_budget_gap * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: UFEInput): number {
  return Math.round((e.combined_sewer_overflow * 0.40 + e.urban_planning_integration * 0.35 + e.early_warning_effectiveness * 0.25) * 100 * 100) / 100;
}
function equityScore(e: UFEInput): number {
  return Math.round((e.low_income_flood_exposure * 0.40 + e.informal_settlement_exposure * 0.35 + e.insurance_coverage_gap * 0.25) * 100 * 100) / 100;
}
function compositeScore(exp: number, inf: number, gov: number, eq: number): number {
  return Math.round((exp * 0.30 + inf * 0.25 + gov * 0.25 + eq * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function floodPattern(e: UFEInput): string {
  if (e.stormwater_system_age > 0.85 && e.drainage_capacity_deficit > 0.80) return "stormwater_infrastructure_collapse";
  if (e.informal_settlement_exposure > 0.85 && e.low_income_flood_exposure > 0.80) return "informal_settlement_flood_trap";
  if (e.urban_heat_compounding > 0.85 && e.impervious_surface_expansion > 0.80) return "urban_heat_flood_compound";
  if (e.combined_sewer_overflow > 0.80 && e.drainage_capacity_deficit > 0.75) return "drainage_capacity_failure";
  if (e.maintenance_budget_gap > 0.80 && e.insurance_coverage_gap > 0.75) return "climate_adaptation_funding_gap";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_inondation_urbaine_systémique";
  if (composite >= 40) return "crise_résilience_hydraulique_majeure";
  if (composite >= 20) return "vulnérabilité_eaux_pluviales_structurelle";
  return "gestion_inondations_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_infrastructure_hydraulique_critique";
  if (risk === "high") return "réhabilitation_accélérée_réseaux_eaux_pluviales";
  if (risk === "moderate") return "renforcement_gouvernance_eaux_pluviales_urbaines";
  return "veille_résilience_inondations_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise inondation urbaine systémique — infrastructure hydraulique en péril";
  if (risk === "high") return "🟠 Crise résilience hydraulique majeure détectée";
  if (risk === "moderate") return "🟡 Vulnérabilité eaux pluviales structurelle active";
  return "🟢 Gestion inondations sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const exp  = exposureScore(e);
      const inf  = infrastructureScore(e);
      const gov  = governanceScore(e);
      const eq   = equityScore(e);
      const comp = compositeScore(exp, inf, gov, eq);
      const risk = riskLevel(comp);
      const pat  = floodPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:                  e.entity_id,
        city_type:                  e.city_type,
        region:                     e.region,
        exposure_score:             exp,
        infrastructure_score:       inf,
        governance_score:           gov,
        equity_score:               eq,
        composite_score:            comp,
        risk_level:                 risk,
        flood_pattern:              pat,
        severity:                   sev,
        recommended_action:         action,
        signal:                     sig,
        drainage_capacity_deficit:  e.drainage_capacity_deficit,
        low_income_flood_exposure:  e.low_income_flood_exposure,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tExp = 0, tInf = 0, tGov = 0, tEq = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.flood_pattern]     = (pattern_distribution[ent.flood_pattern]     || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tExp  += ent.exposure_score;
      tInf  += ent.infrastructure_score;
      tGov  += ent.governance_score;
      tEq   += ent.equity_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite    = Math.round(tComp / n * 10) / 10;
    const avgExposure     = Math.round(tExp  / n * 10) / 10;

    const summary = {
      module_id:                              429,
      module_name:                            "Inondations Urbaines & Gestion Eaux Pluviales Intelligence Engine",
      total:                                  n,
      critical:                               criticalCount,
      high:                                   highCount,
      moderate:                               moderateCount,
      low:                                    lowCount,
      avg_composite:                          avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_flood_resilience_index:   Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, avg_exposure: avgExposure }, "urban-flooding-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/urban-flooding-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "urban-flooding-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "urban-flooding-engine"),
      { status: 502 }
    );
  }
}
