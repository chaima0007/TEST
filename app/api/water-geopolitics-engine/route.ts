import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// ── Module 318 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// Water Geopolitics & Hydro-Conflict Intelligence Engine
// 8 entities covering all hydro-conflict patterns and risk levels.

const MOCK_ENTITIES = [
  // WGP-001 — MEA, transboundary_river → critical, water_war_imminent
  // transboundary_tension≥0.70 AND hydro_weapon_risk≥0.65 → water_war_imminent
  // composite≥60 → critical
  {
    id: "WGP-001", basin_type: "transboundary_river", region: "MEA",
    water_stress_index: 0.80,              transboundary_tension: 0.85,
    upstream_damming_rate: 0.60,           climate_precipitation_deficit: 0.72,
    groundwater_depletion_rate: 0.60,      agricultural_water_competition: 0.78,
    urban_water_demand_surge: 0.60,        desalination_dependency: 0.55,
    treaty_compliance_gap: 0.70,           hydro_weapon_risk: 0.80,
    water_privatization_risk: 0.60,        sanitation_collapse_index: 0.65,
    flood_extreme_exposure: 0.55,          glacial_melt_velocity: 0.30,
    water_infrastructure_fragility: 0.60,  cross_border_migration_water_pressure: 0.72,
    water_data_sovereignty_gap: 0.58,
  },
  // WGP-002 — APAC, island_nation → low, none
  // All low values → composite<20, no pattern triggered
  {
    id: "WGP-002", basin_type: "island_nation", region: "APAC",
    water_stress_index: 0.10,              transboundary_tension: 0.08,
    upstream_damming_rate: 0.08,           climate_precipitation_deficit: 0.10,
    groundwater_depletion_rate: 0.10,      agricultural_water_competition: 0.08,
    urban_water_demand_surge: 0.10,        desalination_dependency: 0.12,
    treaty_compliance_gap: 0.08,           hydro_weapon_risk: 0.08,
    water_privatization_risk: 0.10,        sanitation_collapse_index: 0.08,
    flood_extreme_exposure: 0.10,          glacial_melt_velocity: 0.08,
    water_infrastructure_fragility: 0.10,  cross_border_migration_water_pressure: 0.08,
    water_data_sovereignty_gap: 0.10,
  },
  // WGP-003 — NOAM, arid_basin → high, aquifer_collapse
  // groundwater_depletion_rate≥0.70 AND water_stress_index≥0.65 → aquifer_collapse
  // transboundary_tension=0.40<0.70 → avoids water_war_imminent
  // composite in [40,60) → high
  {
    id: "WGP-003", basin_type: "arid_basin", region: "NOAM",
    water_stress_index: 0.72,              transboundary_tension: 0.40,
    upstream_damming_rate: 0.38,           climate_precipitation_deficit: 0.45,
    groundwater_depletion_rate: 0.78,      agricultural_water_competition: 0.55,
    urban_water_demand_surge: 0.42,        desalination_dependency: 0.35,
    treaty_compliance_gap: 0.38,           hydro_weapon_risk: 0.35,
    water_privatization_risk: 0.40,        sanitation_collapse_index: 0.42,
    flood_extreme_exposure: 0.30,          glacial_melt_velocity: 0.20,
    water_infrastructure_fragility: 0.45,  cross_border_migration_water_pressure: 0.38,
    water_data_sovereignty_gap: 0.35,
  },
  // WGP-004 — LATAM, amazon_basin → low, none
  // All low values → composite<20, no pattern triggered
  {
    id: "WGP-004", basin_type: "amazon_basin", region: "LATAM",
    water_stress_index: 0.08,              transboundary_tension: 0.10,
    upstream_damming_rate: 0.10,           climate_precipitation_deficit: 0.08,
    groundwater_depletion_rate: 0.08,      agricultural_water_competition: 0.10,
    urban_water_demand_surge: 0.10,        desalination_dependency: 0.08,
    treaty_compliance_gap: 0.08,           hydro_weapon_risk: 0.08,
    water_privatization_risk: 0.10,        sanitation_collapse_index: 0.10,
    flood_extreme_exposure: 0.12,          glacial_melt_velocity: 0.10,
    water_infrastructure_fragility: 0.10,  cross_border_migration_water_pressure: 0.08,
    water_data_sovereignty_gap: 0.10,
  },
  // WGP-005 — MEA, nile_system → critical, upstream_dam_coercion
  // upstream_damming_rate≥0.70 AND treaty_compliance_gap≥0.65 → upstream_dam_coercion
  // transboundary_tension=0.60<0.70 → avoids water_war_imminent
  // groundwater_depletion_rate=0.55<0.70 → avoids aquifer_collapse
  // composite≥60 → critical
  {
    id: "WGP-005", basin_type: "nile_system", region: "MEA",
    water_stress_index: 0.75,              transboundary_tension: 0.60,
    upstream_damming_rate: 0.82,           climate_precipitation_deficit: 0.68,
    groundwater_depletion_rate: 0.55,      agricultural_water_competition: 0.72,
    urban_water_demand_surge: 0.60,        desalination_dependency: 0.65,
    treaty_compliance_gap: 0.80,           hydro_weapon_risk: 0.50,
    water_privatization_risk: 0.55,        sanitation_collapse_index: 0.70,
    flood_extreme_exposure: 0.60,          glacial_melt_velocity: 0.35,
    water_infrastructure_fragility: 0.62,  cross_border_migration_water_pressure: 0.65,
    water_data_sovereignty_gap: 0.55,
  },
  // WGP-006 — EMEA, alpine_watershed → moderate, none
  // composite in [20,40), no pattern triggered
  {
    id: "WGP-006", basin_type: "alpine_watershed", region: "EMEA",
    water_stress_index: 0.28,              transboundary_tension: 0.25,
    upstream_damming_rate: 0.22,           climate_precipitation_deficit: 0.30,
    groundwater_depletion_rate: 0.25,      agricultural_water_competition: 0.28,
    urban_water_demand_surge: 0.25,        desalination_dependency: 0.15,
    treaty_compliance_gap: 0.20,           hydro_weapon_risk: 0.18,
    water_privatization_risk: 0.22,        sanitation_collapse_index: 0.20,
    flood_extreme_exposure: 0.25,          glacial_melt_velocity: 0.35,
    water_infrastructure_fragility: 0.28,  cross_border_migration_water_pressure: 0.22,
    water_data_sovereignty_gap: 0.20,
  },
  // WGP-007 — APAC, himalayan_basin → high, glacial_catastrophe
  // glacial_melt_velocity≥0.70 AND climate_precipitation_deficit≥0.65 → glacial_catastrophe
  // transboundary_tension=0.45<0.70 → avoids water_war_imminent
  // groundwater_depletion_rate=0.40<0.70 → avoids aquifer_collapse
  // upstream_damming_rate=0.40<0.70 → avoids upstream_dam_coercion
  // urban_water_demand_surge=0.42<0.70 → avoids urban_water_crisis
  // composite in [40,60) → high
  {
    id: "WGP-007", basin_type: "himalayan_basin", region: "APAC",
    water_stress_index: 0.48,              transboundary_tension: 0.45,
    upstream_damming_rate: 0.40,           climate_precipitation_deficit: 0.72,
    groundwater_depletion_rate: 0.40,      agricultural_water_competition: 0.50,
    urban_water_demand_surge: 0.42,        desalination_dependency: 0.20,
    treaty_compliance_gap: 0.38,           hydro_weapon_risk: 0.35,
    water_privatization_risk: 0.38,        sanitation_collapse_index: 0.40,
    flood_extreme_exposure: 0.55,          glacial_melt_velocity: 0.80,
    water_infrastructure_fragility: 0.45,  cross_border_migration_water_pressure: 0.40,
    water_data_sovereignty_gap: 0.38,
  },
  // WGP-008 — NOAM, megacity_basin → critical, urban_water_crisis
  // urban_water_demand_surge≥0.70 AND water_infrastructure_fragility≥0.65 → urban_water_crisis
  // transboundary_tension=0.50<0.70 → avoids water_war_imminent
  // groundwater_depletion_rate=0.55<0.70 → avoids aquifer_collapse
  // upstream_damming_rate=0.45<0.70 → avoids upstream_dam_coercion
  // composite≥60 → critical
  {
    id: "WGP-008", basin_type: "megacity_basin", region: "NOAM",
    water_stress_index: 0.70,              transboundary_tension: 0.50,
    upstream_damming_rate: 0.45,           climate_precipitation_deficit: 0.65,
    groundwater_depletion_rate: 0.55,      agricultural_water_competition: 0.72,
    urban_water_demand_surge: 0.82,        desalination_dependency: 0.45,
    treaty_compliance_gap: 0.58,           hydro_weapon_risk: 0.45,
    water_privatization_risk: 0.65,        sanitation_collapse_index: 0.72,
    flood_extreme_exposure: 0.60,          glacial_melt_velocity: 0.30,
    water_infrastructure_fragility: 0.80,  cross_border_migration_water_pressure: 0.60,
    water_data_sovereignty_gap: 0.55,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

// ── Scoring functions (mirrors Python engine exactly) ──────────────────────────

function stressScore(e: Entity): number {
  return Math.round((e.water_stress_index * 0.4 + e.groundwater_depletion_rate * 0.35 + e.climate_precipitation_deficit * 0.25) * 100 * 100) / 100;
}

function conflictScore(e: Entity): number {
  return Math.round((e.transboundary_tension * 0.4 + e.hydro_weapon_risk * 0.35 + e.treaty_compliance_gap * 0.25) * 100 * 100) / 100;
}

function demandScore(e: Entity): number {
  return Math.round((e.agricultural_water_competition * 0.4 + e.urban_water_demand_surge * 0.35 + e.cross_border_migration_water_pressure * 0.25) * 100 * 100) / 100;
}

function infrastructureScore(e: Entity): number {
  return Math.round((e.water_infrastructure_fragility * 0.4 + e.sanitation_collapse_index * 0.35 + e.water_privatization_risk * 0.25) * 100 * 100) / 100;
}

function hydroComposite(str: number, con: number, dem: number, inf: number): number {
  return Math.round((str * 0.30 + con * 0.25 + dem * 0.25 + inf * 0.20) * 100) / 100;
}

function hydroRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function hydroPattern(e: Entity): string {
  if (e.transboundary_tension >= 0.70 && e.hydro_weapon_risk >= 0.65) return "water_war_imminent";
  if (e.groundwater_depletion_rate >= 0.70 && e.water_stress_index >= 0.65) return "aquifer_collapse";
  if (e.upstream_damming_rate >= 0.70 && e.treaty_compliance_gap >= 0.65) return "upstream_dam_coercion";
  if (e.urban_water_demand_surge >= 0.70 && e.water_infrastructure_fragility >= 0.65) return "urban_water_crisis";
  if (e.glacial_melt_velocity >= 0.70 && e.climate_precipitation_deficit >= 0.65) return "glacial_catastrophe";
  return "none";
}

function hydroSeverity(comp: number): string {
  if (comp >= 75) return "water_emergency";
  if (comp >= 50) return "hydro_crisis";
  if (comp >= 25) return "water_tension";
  return "water_secure";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "water_emergency_protocol";
  if (risk === "high" && pattern === "water_war_imminent") return "diplomatic_water_intervention";
  if (risk === "high") return "water_resilience_program";
  if (risk === "moderate") return "hydro_monitoring";
  return "no_action";
}

function hydroSignal(risk: string, pattern: string): string {
  const signals: Record<string, string> = {
    critical: "Crise hydrique critique détectée — intervention immédiate requise",
    high: "Risque hydro-géopolitique élevé — surveillance renforcée nécessaire",
    moderate: "Tension hydrique modérée — suivi régulier recommandé",
    low: "Situation hydrique stable — aucune action immédiate requise",
  };
  const patternSignals: Record<string, string> = {
    water_war_imminent: " | Conflit armé pour l'eau imminent",
    aquifer_collapse: " | Effondrement de l'aquifère en cours",
    upstream_dam_coercion: " | Coercition par barrage en amont détectée",
    urban_water_crisis: " | Crise d'eau urbaine critique",
    glacial_catastrophe: " | Catastrophe glaciaire accélérée",
  };
  let base = signals[risk] ?? "Statut inconnu";
  if (pattern in patternSignals) base += patternSignals[pattern];
  return base;
}

// ── GET handler ────────────────────────────────────────────────────────────────

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[water-geopolitics-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tStr = 0, tCon = 0, tDem = 0, tInf = 0, tComp = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.hydro_risk] = (rc[ent.hydro_risk] || 0) + 1;
      pc[ent.hydro_pattern] = (pc[ent.hydro_pattern] || 0) + 1;
      sc[ent.hydro_severity] = (sc[ent.hydro_severity] || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tStr += ent.stress_score;
      tCon += ent.conflict_score;
      tDem += ent.demand_score;
      tInf += ent.infrastructure_score;
      tComp += ent.hydro_composite;
      if (ent.is_hydro_crisis) crisisCount++;
      if (ent.requires_hydro_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComp = tComp / n;

    return sealResponse(NextResponse.json(sealResponse({
      entities,
      summary: {
        module: "WaterGeopoliticsEngine",
        module_id: 318,
        total_entities: n,
        critical_count: rc["critical"] || 0,
        high_count: rc["high"] || 0,
        moderate_count: rc["moderate"] || 0,
        low_count: rc["low"] || 0,
        hydro_crisis_count: crisisCount,
        requires_intervention_count: interventionCount,
        avg_composite: Math.round(avgComp * 100) / 100,
        avg_estimated_hydro_conflict_index: Math.round(avgComp / 100 * 10 * 100) / 100,
        avg_stress_score: Math.round(tStr / n * 100) / 100,
        avg_conflict_score: Math.round(tCon / n * 100) / 100,
        avg_demand_score: Math.round(tDem / n * 100) / 100,
        avg_infrastructure_score: Math.round(tInf / n * 100) / 100,
        risk_counts: rc,
        pattern_counts: pc,
        severity_counts: sc,
        action_counts: ac,
      },
    } as Record<string, unknown>, "water-geopolitics-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/water-geopolitics-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return sealResponse(NextResponse.json(sealResponse(await upstream.json() as Record<string, unknown>, "water-geopolitics-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "SWARM_API_URL not configured" } as Record<string, unknown>, "water-geopolitics-engine"),
      { status: 502 }
    ));
  }
}
