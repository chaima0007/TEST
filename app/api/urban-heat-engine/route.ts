import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// ── Module 354 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// Urban Heat Island & City Climate Emergency Intelligence Engine
// 8 entities covering all 5 heat patterns and all 4 risk levels.

interface UheInput {
  id: string;
  city_type: string;
  region: string;
  heat_island_intensity_index: number;
  extreme_heat_mortality_rate: number;
  urban_cooling_infrastructure_deficit: number;
  green_space_accessibility_inequality: number;
  air_conditioning_energy_spiral: number;
  cooling_poverty_exposure: number;
  urban_albedo_reduction_factor: number;
  heat_vulnerable_population_density: number;
  flood_heat_compound_risk: number;
  urban_biodiversity_collapse: number;
  pavement_heat_retention_index: number;
  night_cooling_failure_rate: number;
  emergency_cooling_center_gap: number;
  housing_heat_trap_density: number;
  urban_tree_canopy_deficit: number;
  heat_adaptation_funding_gap: number;
  urban_heat_mortality_inequality: number;
}

const MOCK_ENTITIES: UheInput[] = [
  // UHE-001 — APAC, megacity → critical, lethal_heat_dome
  // extreme_heat_mortality_rate≥0.70 AND heat_vulnerable_population_density≥0.65 → lethal_heat_dome
  // composite≥60 → critical
  {
    id: "UHE-001", city_type: "megacity", region: "APAC",
    heat_island_intensity_index: 0.80,
    extreme_heat_mortality_rate: 0.82,
    urban_cooling_infrastructure_deficit: 0.65,
    green_space_accessibility_inequality: 0.70,
    air_conditioning_energy_spiral: 0.65,
    cooling_poverty_exposure: 0.60,
    urban_albedo_reduction_factor: 0.62,
    heat_vulnerable_population_density: 0.78,
    flood_heat_compound_risk: 0.55,
    urban_biodiversity_collapse: 0.60,
    pavement_heat_retention_index: 0.75,
    night_cooling_failure_rate: 0.68,
    emergency_cooling_center_gap: 0.60,
    housing_heat_trap_density: 0.60,
    urban_tree_canopy_deficit: 0.65,
    heat_adaptation_funding_gap: 0.62,
    urban_heat_mortality_inequality: 0.72,
  },
  // UHE-002 — EMEA, small_city → low, none
  // All low values → composite<20, no pattern triggered
  {
    id: "UHE-002", city_type: "small_city", region: "EMEA",
    heat_island_intensity_index: 0.10,
    extreme_heat_mortality_rate: 0.08,
    urban_cooling_infrastructure_deficit: 0.10,
    green_space_accessibility_inequality: 0.08,
    air_conditioning_energy_spiral: 0.10,
    cooling_poverty_exposure: 0.08,
    urban_albedo_reduction_factor: 0.10,
    heat_vulnerable_population_density: 0.08,
    flood_heat_compound_risk: 0.10,
    urban_biodiversity_collapse: 0.08,
    pavement_heat_retention_index: 0.10,
    night_cooling_failure_rate: 0.08,
    emergency_cooling_center_gap: 0.08,
    housing_heat_trap_density: 0.10,
    urban_tree_canopy_deficit: 0.08,
    heat_adaptation_funding_gap: 0.10,
    urban_heat_mortality_inequality: 0.08,
  },
  // UHE-003 — MEA, industrial_city → high, cooling_infrastructure_collapse
  // urban_cooling_infrastructure_deficit≥0.70 AND emergency_cooling_center_gap≥0.65 → cooling_infrastructure_collapse
  // extreme_heat_mortality_rate=0.50<0.70 → avoids lethal_heat_dome
  // composite in [40,60) → high
  {
    id: "UHE-003", city_type: "industrial_city", region: "MEA",
    heat_island_intensity_index: 0.55,
    extreme_heat_mortality_rate: 0.50,
    urban_cooling_infrastructure_deficit: 0.78,
    green_space_accessibility_inequality: 0.50,
    air_conditioning_energy_spiral: 0.55,
    cooling_poverty_exposure: 0.45,
    urban_albedo_reduction_factor: 0.48,
    heat_vulnerable_population_density: 0.50,
    flood_heat_compound_risk: 0.42,
    urban_biodiversity_collapse: 0.45,
    pavement_heat_retention_index: 0.50,
    night_cooling_failure_rate: 0.48,
    emergency_cooling_center_gap: 0.75,
    housing_heat_trap_density: 0.45,
    urban_tree_canopy_deficit: 0.42,
    heat_adaptation_funding_gap: 0.48,
    urban_heat_mortality_inequality: 0.45,
  },
  // UHE-004 — LATAM, coastal_city → low, none
  // All low values → composite<20, no pattern triggered
  {
    id: "UHE-004", city_type: "coastal_city", region: "LATAM",
    heat_island_intensity_index: 0.08,
    extreme_heat_mortality_rate: 0.10,
    urban_cooling_infrastructure_deficit: 0.10,
    green_space_accessibility_inequality: 0.10,
    air_conditioning_energy_spiral: 0.08,
    cooling_poverty_exposure: 0.08,
    urban_albedo_reduction_factor: 0.08,
    heat_vulnerable_population_density: 0.10,
    flood_heat_compound_risk: 0.08,
    urban_biodiversity_collapse: 0.10,
    pavement_heat_retention_index: 0.10,
    night_cooling_failure_rate: 0.08,
    emergency_cooling_center_gap: 0.08,
    housing_heat_trap_density: 0.08,
    urban_tree_canopy_deficit: 0.10,
    heat_adaptation_funding_gap: 0.08,
    urban_heat_mortality_inequality: 0.10,
  },
  // UHE-005 — LATAM, informal_settlement → critical, heat_poverty_trap
  // cooling_poverty_exposure≥0.70 AND housing_heat_trap_density≥0.65 → heat_poverty_trap
  // extreme_heat_mortality_rate=0.60<0.70 → avoids lethal_heat_dome
  // urban_cooling_infrastructure_deficit=0.65<0.70 → avoids cooling_infrastructure_collapse
  // composite≥60 → critical
  {
    id: "UHE-005", city_type: "informal_settlement", region: "LATAM",
    heat_island_intensity_index: 0.72,
    extreme_heat_mortality_rate: 0.60,
    urban_cooling_infrastructure_deficit: 0.65,
    green_space_accessibility_inequality: 0.65,
    air_conditioning_energy_spiral: 0.72,
    cooling_poverty_exposure: 0.85,
    urban_albedo_reduction_factor: 0.62,
    heat_vulnerable_population_density: 0.60,
    flood_heat_compound_risk: 0.60,
    urban_biodiversity_collapse: 0.65,
    pavement_heat_retention_index: 0.68,
    night_cooling_failure_rate: 0.72,
    emergency_cooling_center_gap: 0.60,
    housing_heat_trap_density: 0.78,
    urban_tree_canopy_deficit: 0.62,
    heat_adaptation_funding_gap: 0.65,
    urban_heat_mortality_inequality: 0.70,
  },
  // UHE-006 — NOAM, suburban_sprawl → moderate, none
  // composite in [20,40), no pattern triggered
  {
    id: "UHE-006", city_type: "suburban_sprawl", region: "NOAM",
    heat_island_intensity_index: 0.28,
    extreme_heat_mortality_rate: 0.25,
    urban_cooling_infrastructure_deficit: 0.25,
    green_space_accessibility_inequality: 0.28,
    air_conditioning_energy_spiral: 0.22,
    cooling_poverty_exposure: 0.25,
    urban_albedo_reduction_factor: 0.25,
    heat_vulnerable_population_density: 0.22,
    flood_heat_compound_risk: 0.20,
    urban_biodiversity_collapse: 0.22,
    pavement_heat_retention_index: 0.28,
    night_cooling_failure_rate: 0.22,
    emergency_cooling_center_gap: 0.22,
    housing_heat_trap_density: 0.20,
    urban_tree_canopy_deficit: 0.22,
    heat_adaptation_funding_gap: 0.20,
    urban_heat_mortality_inequality: 0.22,
  },
  // UHE-007 — MEA, arid_city → high, green_desert_city
  // urban_tree_canopy_deficit≥0.70 AND urban_albedo_reduction_factor≥0.65 → green_desert_city
  // extreme_heat_mortality_rate=0.42<0.70 → avoids lethal_heat_dome
  // urban_cooling_infrastructure_deficit=0.45<0.70 → avoids cooling_infrastructure_collapse
  // composite in [40,60) → high
  {
    id: "UHE-007", city_type: "arid_city", region: "MEA",
    heat_island_intensity_index: 0.55,
    extreme_heat_mortality_rate: 0.42,
    urban_cooling_infrastructure_deficit: 0.45,
    green_space_accessibility_inequality: 0.48,
    air_conditioning_energy_spiral: 0.45,
    cooling_poverty_exposure: 0.42,
    urban_albedo_reduction_factor: 0.72,
    heat_vulnerable_population_density: 0.40,
    flood_heat_compound_risk: 0.38,
    urban_biodiversity_collapse: 0.45,
    pavement_heat_retention_index: 0.50,
    night_cooling_failure_rate: 0.45,
    emergency_cooling_center_gap: 0.42,
    housing_heat_trap_density: 0.42,
    urban_tree_canopy_deficit: 0.80,
    heat_adaptation_funding_gap: 0.40,
    urban_heat_mortality_inequality: 0.38,
  },
  // UHE-008 — APAC, coastal_megacity → critical, compound_climate_crisis
  // flood_heat_compound_risk≥0.70 AND heat_island_intensity_index≥0.65 → compound_climate_crisis
  // extreme_heat_mortality_rate=0.60<0.70 → avoids lethal_heat_dome
  // urban_cooling_infrastructure_deficit=0.65<0.70 → avoids cooling_infrastructure_collapse
  // composite≥60 → critical
  {
    id: "UHE-008", city_type: "coastal_megacity", region: "APAC",
    heat_island_intensity_index: 0.80,
    extreme_heat_mortality_rate: 0.60,
    urban_cooling_infrastructure_deficit: 0.65,
    green_space_accessibility_inequality: 0.62,
    air_conditioning_energy_spiral: 0.70,
    cooling_poverty_exposure: 0.62,
    urban_albedo_reduction_factor: 0.60,
    heat_vulnerable_population_density: 0.62,
    flood_heat_compound_risk: 0.85,
    urban_biodiversity_collapse: 0.68,
    pavement_heat_retention_index: 0.70,
    night_cooling_failure_rate: 0.65,
    emergency_cooling_center_gap: 0.60,
    housing_heat_trap_density: 0.60,
    urban_tree_canopy_deficit: 0.62,
    heat_adaptation_funding_gap: 0.68,
    urban_heat_mortality_inequality: 0.65,
  },
];

// ── Scoring functions (mirrors Python engine exactly) ──────────────────────────

function thermalScore(e: UheInput): number {
  return Math.round((e.heat_island_intensity_index * 0.4 + e.pavement_heat_retention_index * 0.35 + e.urban_albedo_reduction_factor * 0.25) * 100 * 100) / 100;
}

function mortalityScore(e: UheInput): number {
  return Math.round((e.extreme_heat_mortality_rate * 0.4 + e.heat_vulnerable_population_density * 0.35 + e.urban_heat_mortality_inequality * 0.25) * 100 * 100) / 100;
}

function adaptationScore(e: UheInput): number {
  return Math.round((e.urban_cooling_infrastructure_deficit * 0.4 + e.emergency_cooling_center_gap * 0.35 + e.heat_adaptation_funding_gap * 0.25) * 100 * 100) / 100;
}

function equityScore(e: UheInput): number {
  return Math.round((e.cooling_poverty_exposure * 0.4 + e.green_space_accessibility_inequality * 0.35 + e.housing_heat_trap_density * 0.25) * 100 * 100) / 100;
}

function uheComposite(th: number, mo: number, ad: number, eq: number): number {
  return Math.round((th * 0.30 + mo * 0.25 + ad * 0.25 + eq * 0.20) * 100) / 100;
}

function uheRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function uhePattern(e: UheInput): string {
  if (e.extreme_heat_mortality_rate >= 0.70 && e.heat_vulnerable_population_density >= 0.65) return "lethal_heat_dome";
  if (e.urban_cooling_infrastructure_deficit >= 0.70 && e.emergency_cooling_center_gap >= 0.65) return "cooling_infrastructure_collapse";
  if (e.urban_tree_canopy_deficit >= 0.70 && e.urban_albedo_reduction_factor >= 0.65) return "green_desert_city";
  if (e.cooling_poverty_exposure >= 0.70 && e.housing_heat_trap_density >= 0.65) return "heat_poverty_trap";
  if (e.flood_heat_compound_risk >= 0.70 && e.heat_island_intensity_index >= 0.65) return "compound_climate_crisis";
  return "none";
}

function uheSeverity(risk: string): string {
  if (risk === "critical") return "urgence_chaleur_urbaine_létale";
  if (risk === "high") return "crise_chaleur_urbaine_majeure";
  if (risk === "moderate") return "stress_thermique_structurel";
  return "chaleur_urbaine_gérée";
}

function uheAction(risk: string): string {
  if (risk === "critical") return "plan_urgence_chaleur_urbaine";
  if (risk === "high") return "infrastructure_refroidissement_urgente";
  if (risk === "moderate") return "verdissement_urbain_accéléré";
  return "veille_chaleur_urbaine_continue";
}

function uheSignal(risk: string): string {
  if (risk === "critical") return "🔴 Urgence chaleur urbaine létale — vies humaines en danger";
  if (risk === "high") return "🟠 Crise chaleur urbaine majeure détectée";
  if (risk === "moderate") return "🟡 Stress thermique structurel actif";
  return "🟢 Chaleur urbaine sous surveillance";
}

function analyzeEntity(e: UheInput) {
  const th = thermalScore(e);
  const mo = mortalityScore(e);
  const ad = adaptationScore(e);
  const eq = equityScore(e);
  const comp = uheComposite(th, mo, ad, eq);
  const risk = uheRisk(comp);
  const pattern = uhePattern(e);
  const severity = uheSeverity(risk);
  const action = uheAction(risk);
  const signal = uheSignal(risk);

  return {
    id: e.entity_id,
    city_type: e.city_type,
    region: e.region,
    thermal_score: th,
    mortality_score: mo,
    adaptation_score: ad,
    equity_score: eq,
    composite_score: comp,
    risk_level: risk,
    heat_pattern: pattern,
    severity,
    recommended_action: action,
    signal,
    heat_island_intensity_index: e.heat_island_intensity_index,
    extreme_heat_mortality_rate: e.extreme_heat_mortality_rate,
  };
}

// ── GET handler ────────────────────────────────────────────────────────────────

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[urban-heat-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    const pattern_distribution: Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number> = {};
    let tComp = 0, tThermal = 0, tMortality = 0, tAdaptation = 0, tEquity = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level] = (risk_distribution[ent.risk_level] || 0) + 1;
      pattern_distribution[ent.heat_pattern] = (pattern_distribution[ent.heat_pattern] || 0) + 1;
      severity_distribution[ent.severity] = (severity_distribution[ent.severity] || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
      tThermal += ent.thermal_score;
      tMortality += ent.mortality_score;
      tAdaptation += ent.adaptation_score;
      tEquity += ent.equity_score;
    }

    const n = entities.length;
    const avgComp = Math.round((tComp / n) * 100) / 100;

    return sealResponse(NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id: 354,
        module_name: "Urban Heat Island & City Climate Emergency Intelligence Engine",
        total_entities: n,
        critical_count: risk_distribution["critical"] || 0,
        high_count: risk_distribution["high"] || 0,
        moderate_count: risk_distribution["moderate"] || 0,
        low_count: risk_distribution["low"] || 0,
        avg_composite: avgComp,
        pattern_distribution,
        risk_distribution,
        severity_distribution,
        action_distribution,
        avg_estimated_urban_heat_index: Math.round(avgComp / 100 * 10 * 100) / 100,
        avg_thermal_score: Math.round(tThermal / n * 100) / 100,
        avg_mortality_score: Math.round(tMortality / n * 100) / 100,
        avg_adaptation_score: Math.round(tAdaptation / n * 100) / 100,
        avg_equity_score: Math.round(tEquity / n * 100) / 100,
      },
    } as Record<string, unknown>, "urban-heat-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/urban-heat-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return sealResponse(NextResponse.json(sealResponse(await upstream.json() as Record<string, unknown>, "urban-heat-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "SWARM_API_URL unreachable" } as Record<string, unknown>, "urban-heat-engine"),
      { status: 502 }
    ));
  }
}
