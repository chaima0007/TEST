import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // EPE-001 — critical, energy_access_collapse (access_gap>0.85, rural_elec>0.80)
  {
    id: "EPE-001", energy_sector: "residential", region: "SSA",
    energy_access_gap: 0.92, fossil_fuel_dependency_lock: 0.70,
    green_transition_inequality: 0.65, energy_cost_burden: 0.72,
    grid_infrastructure_failure: 0.82, rural_electrification_gap: 0.88,
    just_transition_policy_failure: 0.68, stranded_community_risk: 0.65,
    climate_migration_energy: 0.70, colonial_energy_debt: 0.68,
    renewable_transition_exclusion: 0.65, energy_affordability_crisis: 0.72,
    utility_privatization_harm: 0.60, subsidy_capture_by_wealthy: 0.65,
    carbon_tax_regressive_impact: 0.62, global_south_transition_gap: 0.68,
    energy_democracy_erosion: 0.60,
  },
  // EPE-002 — critical, just_transition_failure (jt_policy>0.85, stranded>0.80)
  {
    id: "EPE-002", energy_sector: "fossil_fuel_extraction", region: "APAC",
    energy_access_gap: 0.62, fossil_fuel_dependency_lock: 0.88,
    green_transition_inequality: 0.70, energy_cost_burden: 0.65,
    grid_infrastructure_failure: 0.68, rural_electrification_gap: 0.60,
    just_transition_policy_failure: 0.90, stranded_community_risk: 0.85,
    climate_migration_energy: 0.75, colonial_energy_debt: 0.65,
    renewable_transition_exclusion: 0.70, energy_affordability_crisis: 0.65,
    utility_privatization_harm: 0.62, subsidy_capture_by_wealthy: 0.68,
    carbon_tax_regressive_impact: 0.60, global_south_transition_gap: 0.65,
    energy_democracy_erosion: 0.68,
  },
  // EPE-003 — high, green_inequality_trap (green_ineq>0.85, renewable_excl>0.80)
  {
    id: "EPE-003", energy_sector: "renewable_transition", region: "EMEA",
    energy_access_gap: 0.48, fossil_fuel_dependency_lock: 0.50,
    green_transition_inequality: 0.88, energy_cost_burden: 0.50,
    grid_infrastructure_failure: 0.48, rural_electrification_gap: 0.45,
    just_transition_policy_failure: 0.50, stranded_community_risk: 0.48,
    climate_migration_energy: 0.50, colonial_energy_debt: 0.45,
    renewable_transition_exclusion: 0.82, energy_affordability_crisis: 0.50,
    utility_privatization_harm: 0.48, subsidy_capture_by_wealthy: 0.52,
    carbon_tax_regressive_impact: 0.48, global_south_transition_gap: 0.45,
    energy_democracy_erosion: 0.50,
  },
  // EPE-004 — high, colonial_energy_debt_crisis (colonial>0.80, global_south>0.75)
  {
    id: "EPE-004", energy_sector: "utility", region: "LATAM",
    energy_access_gap: 0.45, fossil_fuel_dependency_lock: 0.50,
    green_transition_inequality: 0.48, energy_cost_burden: 0.52,
    grid_infrastructure_failure: 0.45, rural_electrification_gap: 0.48,
    just_transition_policy_failure: 0.50, stranded_community_risk: 0.45,
    climate_migration_energy: 0.52, colonial_energy_debt: 0.85,
    renewable_transition_exclusion: 0.50, energy_affordability_crisis: 0.48,
    utility_privatization_harm: 0.50, subsidy_capture_by_wealthy: 0.48,
    carbon_tax_regressive_impact: 0.45, global_south_transition_gap: 0.80,
    energy_democracy_erosion: 0.48,
  },
  // EPE-005 — moderate, energy_affordability_crisis_pattern (afford>0.80, carbon_tax>0.75)
  {
    id: "EPE-005", energy_sector: "household", region: "NOAM",
    energy_access_gap: 0.28, fossil_fuel_dependency_lock: 0.30,
    green_transition_inequality: 0.30, energy_cost_burden: 0.30,
    grid_infrastructure_failure: 0.28, rural_electrification_gap: 0.25,
    just_transition_policy_failure: 0.28, stranded_community_risk: 0.30,
    climate_migration_energy: 0.28, colonial_energy_debt: 0.25,
    renewable_transition_exclusion: 0.28, energy_affordability_crisis: 0.82,
    utility_privatization_harm: 0.30, subsidy_capture_by_wealthy: 0.28,
    carbon_tax_regressive_impact: 0.78, global_south_transition_gap: 0.25,
    energy_democracy_erosion: 0.28,
  },
  // EPE-006 — moderate, none
  {
    id: "EPE-006", energy_sector: "industrial", region: "EMEA",
    energy_access_gap: 0.30, fossil_fuel_dependency_lock: 0.28,
    green_transition_inequality: 0.30, energy_cost_burden: 0.32,
    grid_infrastructure_failure: 0.28, rural_electrification_gap: 0.25,
    just_transition_policy_failure: 0.30, stranded_community_risk: 0.28,
    climate_migration_energy: 0.30, colonial_energy_debt: 0.25,
    renewable_transition_exclusion: 0.28, energy_affordability_crisis: 0.30,
    utility_privatization_harm: 0.32, subsidy_capture_by_wealthy: 0.28,
    carbon_tax_regressive_impact: 0.25, global_south_transition_gap: 0.28,
    energy_democracy_erosion: 0.30,
  },
  // EPE-007 — low, none
  {
    id: "EPE-007", energy_sector: "grid_operator", region: "NOAM",
    energy_access_gap: 0.10, fossil_fuel_dependency_lock: 0.12,
    green_transition_inequality: 0.10, energy_cost_burden: 0.12,
    grid_infrastructure_failure: 0.10, rural_electrification_gap: 0.08,
    just_transition_policy_failure: 0.10, stranded_community_risk: 0.12,
    climate_migration_energy: 0.10, colonial_energy_debt: 0.08,
    renewable_transition_exclusion: 0.10, energy_affordability_crisis: 0.12,
    utility_privatization_harm: 0.10, subsidy_capture_by_wealthy: 0.12,
    carbon_tax_regressive_impact: 0.08, global_south_transition_gap: 0.10,
    energy_democracy_erosion: 0.10,
  },
  // EPE-008 — low, none
  {
    id: "EPE-008", energy_sector: "municipal", region: "APAC",
    energy_access_gap: 0.12, fossil_fuel_dependency_lock: 0.10,
    green_transition_inequality: 0.12, energy_cost_burden: 0.10,
    grid_infrastructure_failure: 0.12, rural_electrification_gap: 0.10,
    just_transition_policy_failure: 0.12, stranded_community_risk: 0.10,
    climate_migration_energy: 0.12, colonial_energy_debt: 0.10,
    renewable_transition_exclusion: 0.12, energy_affordability_crisis: 0.10,
    utility_privatization_harm: 0.12, subsidy_capture_by_wealthy: 0.10,
    carbon_tax_regressive_impact: 0.10, global_south_transition_gap: 0.12,
    energy_democracy_erosion: 0.10,
  },
];

type EPEInput = typeof MOCK_ENTITIES[0];

function accessScore(e: EPEInput): number {
  return Math.round((e.energy_access_gap * 0.4 + e.grid_infrastructure_failure * 0.35 + e.rural_electrification_gap * 0.25) * 100 * 100) / 100;
}
function justiceScore(e: EPEInput): number {
  return Math.round((e.energy_cost_burden * 0.4 + e.subsidy_capture_by_wealthy * 0.35 + e.utility_privatization_harm * 0.25) * 100 * 100) / 100;
}
function transitionScore(e: EPEInput): number {
  return Math.round((e.just_transition_policy_failure * 0.4 + e.renewable_transition_exclusion * 0.35 + e.green_transition_inequality * 0.25) * 100 * 100) / 100;
}
function systemicScore(e: EPEInput): number {
  return Math.round((e.colonial_energy_debt * 0.4 + e.global_south_transition_gap * 0.35 + e.energy_democracy_erosion * 0.25) * 100 * 100) / 100;
}
function compositeScore(acc: number, jus: number, tra: number, sys: number): number {
  return Math.round((acc * 0.30 + jus * 0.25 + tra * 0.25 + sys * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function energyPattern(e: EPEInput): string {
  if (e.energy_access_gap > 0.85 && e.rural_electrification_gap > 0.80) return "energy_access_collapse";
  if (e.just_transition_policy_failure > 0.85 && e.stranded_community_risk > 0.80) return "just_transition_failure";
  if (e.green_transition_inequality > 0.85 && e.renewable_transition_exclusion > 0.80) return "green_inequality_trap";
  if (e.colonial_energy_debt > 0.80 && e.global_south_transition_gap > 0.75) return "colonial_energy_debt_crisis";
  if (e.energy_affordability_crisis > 0.80 && e.carbon_tax_regressive_impact > 0.75) return "energy_affordability_crisis_pattern";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_pauvreté_énergétique_systémique";
  if (composite >= 40) return "crise_justice_climatique_majeure";
  if (composite >= 20) return "inégalité_énergétique_structurelle";
  return "accès_énergie_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_accès_énergie_critique";
  if (risk === "high") return "transition_juste_accélérée_communautés_vulnérables";
  if (risk === "moderate") return "renforcement_politiques_justice_énergétique";
  return "veille_accès_énergie_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise pauvreté énergétique systémique — justice climatique en péril";
  if (risk === "high") return "🟠 Crise justice climatique majeure détectée";
  if (risk === "moderate") return "🟡 Inégalité énergétique structurelle active";
  return "🟢 Accès énergie sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[energy-poverty-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tAcc = 0, tJus = 0, tTra = 0, tSys = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.energy_pattern]    = (pattern_distribution[ent.energy_pattern]    || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tAcc  += ent.access_score;
      tJus  += ent.justice_score;
      tTra  += ent.transition_score;
      tSys  += ent.systemic_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;
    const avgAccess    = Math.round(tAcc  / n * 10) / 10;

    const summary = {
      module_id:                              379,
      module_name:                            "Energy Poverty & Climate Justice Intelligence Engine",
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
      avg_estimated_energy_justice_index:     Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary, avg_access: avgAccess }, "energy-poverty-engine")
    ));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/energy-poverty-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return sealResponse(NextResponse.json(sealResponse(await upstream.json(), "energy-poverty-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "energy-poverty-engine"),
      { status: 502 }
    ));
  }
}
