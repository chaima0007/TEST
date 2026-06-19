import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ─── Math (mirrors Python exactly) ───────────────────────────────────────────

interface FscInput {
  entity_id: string;
  food_system_type: string;
  region: string;
  crop_yield_collapse_risk: number;
  monoculture_vulnerability: number;
  seed_sovereignty_erosion: number;
  agrochemical_dependency: number;
  soil_degradation_rate: number;
  pollinator_collapse_index: number;
  extreme_weather_frequency: number;
  supply_chain_food_fragility: number;
  food_import_dependency: number;
  price_spike_transmission: number;
  urban_food_desert_expansion: number;
  protein_transition_disruption: number;
  vertical_farming_disruption_gap: number;
  water_food_nexus_stress: number;
  nitrogen_cycle_disruption: number;
  smallholder_displacement_rate: number;
  food_system_digitalization_risk: number;
}

function productionScore(e: FscInput): number {
  return Math.round((e.crop_yield_collapse_risk * 0.4 + e.soil_degradation_rate * 0.35 + e.pollinator_collapse_index * 0.25) * 100 * 100) / 100;
}

function supplyScore(e: FscInput): number {
  return Math.round((e.food_import_dependency * 0.4 + e.supply_chain_food_fragility * 0.35 + e.monoculture_vulnerability * 0.25) * 100 * 100) / 100;
}

function accessScore(e: FscInput): number {
  return Math.round((e.price_spike_transmission * 0.4 + e.urban_food_desert_expansion * 0.35 + e.smallholder_displacement_rate * 0.25) * 100 * 100) / 100;
}

function resilienceScore(e: FscInput): number {
  return Math.round((e.extreme_weather_frequency * 0.4 + e.nitrogen_cycle_disruption * 0.35 + e.agrochemical_dependency * 0.25) * 100 * 100) / 100;
}

function composite(prod: number, sup: number, acc: number, res: number): number {
  return Math.round((prod * 0.30 + sup * 0.25 + acc * 0.25 + res * 0.20) * 100) / 100;
}

function foodPattern(e: FscInput): string {
  if (e.crop_yield_collapse_risk >= 0.70 && e.food_import_dependency >= 0.65) return "famine_cascade";
  if (e.monoculture_vulnerability >= 0.70 && e.pollinator_collapse_index >= 0.65) return "monoculture_collapse";
  if (e.price_spike_transmission >= 0.70 && e.supply_chain_food_fragility >= 0.65) return "price_shock_explosion";
  if (e.soil_degradation_rate >= 0.70 && e.nitrogen_cycle_disruption >= 0.65) return "soil_death_spiral";
  if (e.protein_transition_disruption >= 0.70 && e.smallholder_displacement_rate >= 0.60) return "protein_transition_shock";
  return "none";
}

function foodRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function foodSeverity(comp: number): string {
  if (comp >= 75) return "food_emergency";
  if (comp >= 50) return "food_crisis";
  if (comp >= 25) return "food_stress";
  return "food_secure";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "food_emergency_protocol";
  if (risk === "high" && pattern === "famine_cascade") return "emergency_food_reserves";
  if (risk === "high") return "food_resilience_program";
  if (risk === "moderate") return "food_monitoring";
  return "no_action";
}

function foodSignal(e: FscInput, risk: string, comp: number): string {
  if (risk === "critical") {
    return `Critique — risque effondrement rendements ${Math.round(e.crop_yield_collapse_risk * 100)}% — dépendance importations alimentaires ${Math.round(e.food_import_dependency * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "high") {
    return `Élevé — vulnérabilité monoculture ${Math.round(e.monoculture_vulnerability * 100)}% — dégradation sols ${Math.round(e.soil_degradation_rate * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "moderate") {
    return `Modéré — transmission choc prix ${Math.round(e.price_spike_transmission * 100)}% — composite ${Math.round(comp)}`;
  }
  return "Système alimentaire stable — résilience agricole solide, souveraineté alimentaire préservée, aucun risque imminent d'effondrement";
}

function analyzeEntity(e: FscInput) {
  const prod = productionScore(e);
  const sup  = supplyScore(e);
  const acc  = accessScore(e);
  const res  = resilienceScore(e);
  const comp = composite(prod, sup, acc, res);
  const pat  = foodPattern(e);
  const risk = foodRisk(comp);
  const sev  = foodSeverity(comp);
  const action = recommendedAction(risk, pat);
  const signal = foodSignal(e, risk, comp);

  return {
    entity_id: e.entity_id,
    region: e.region,
    food_system_type: e.food_system_type,
    food_risk: risk,
    food_pattern: pat,
    food_severity: sev,
    recommended_action: action,
    production_score: prod,
    supply_score: sup,
    access_score: acc,
    resilience_score: res,
    food_composite: comp,
    is_food_crisis: comp >= 60,
    requires_food_intervention: comp >= 40,
    food_signal: signal,
  };
}

// ─── Mock entities ────────────────────────────────────────────────────────────

const mockEntities: FscInput[] = [
  {
    entity_id: "FSC-001", region: "MEA", food_system_type: "arid_agriculture",
    crop_yield_collapse_risk: 0.82, food_import_dependency: 0.78, soil_degradation_rate: 0.75,
    pollinator_collapse_index: 0.70, monoculture_vulnerability: 0.60, supply_chain_food_fragility: 0.68,
    price_spike_transmission: 0.72, urban_food_desert_expansion: 0.65, smallholder_displacement_rate: 0.60,
    extreme_weather_frequency: 0.78, nitrogen_cycle_disruption: 0.65, agrochemical_dependency: 0.55,
    seed_sovereignty_erosion: 0.65, protein_transition_disruption: 0.45, vertical_farming_disruption_gap: 0.50,
    water_food_nexus_stress: 0.72, food_system_digitalization_risk: 0.40,
  },
  {
    entity_id: "FSC-002", region: "LATAM", food_system_type: "diverse_agriculture",
    crop_yield_collapse_risk: 0.22, food_import_dependency: 0.20, soil_degradation_rate: 0.25,
    pollinator_collapse_index: 0.20, monoculture_vulnerability: 0.22, supply_chain_food_fragility: 0.22,
    price_spike_transmission: 0.20, urban_food_desert_expansion: 0.22, smallholder_displacement_rate: 0.20,
    extreme_weather_frequency: 0.25, nitrogen_cycle_disruption: 0.20, agrochemical_dependency: 0.22,
    seed_sovereignty_erosion: 0.20, protein_transition_disruption: 0.22, vertical_farming_disruption_gap: 0.20,
    water_food_nexus_stress: 0.22, food_system_digitalization_risk: 0.20,
  },
  {
    entity_id: "FSC-003", region: "NOAM", food_system_type: "industrial_agriculture",
    crop_yield_collapse_risk: 0.55, food_import_dependency: 0.40, soil_degradation_rate: 0.55,
    pollinator_collapse_index: 0.72, monoculture_vulnerability: 0.78, supply_chain_food_fragility: 0.50,
    price_spike_transmission: 0.48, urban_food_desert_expansion: 0.45, smallholder_displacement_rate: 0.52,
    extreme_weather_frequency: 0.55, nitrogen_cycle_disruption: 0.50, agrochemical_dependency: 0.65,
    seed_sovereignty_erosion: 0.70, protein_transition_disruption: 0.58, vertical_farming_disruption_gap: 0.45,
    water_food_nexus_stress: 0.50, food_system_digitalization_risk: 0.55,
  },
  {
    entity_id: "FSC-004", region: "APAC", food_system_type: "rice_system",
    crop_yield_collapse_risk: 0.28, food_import_dependency: 0.25, soil_degradation_rate: 0.30,
    pollinator_collapse_index: 0.22, monoculture_vulnerability: 0.28, supply_chain_food_fragility: 0.25,
    price_spike_transmission: 0.28, urban_food_desert_expansion: 0.25, smallholder_displacement_rate: 0.28,
    extreme_weather_frequency: 0.30, nitrogen_cycle_disruption: 0.25, agrochemical_dependency: 0.28,
    seed_sovereignty_erosion: 0.25, protein_transition_disruption: 0.25, vertical_farming_disruption_gap: 0.28,
    water_food_nexus_stress: 0.30, food_system_digitalization_risk: 0.25,
  },
  {
    entity_id: "FSC-005", region: "EMEA", food_system_type: "wheat_system",
    crop_yield_collapse_risk: 0.72, food_import_dependency: 0.55, soil_degradation_rate: 0.82,
    pollinator_collapse_index: 0.58, monoculture_vulnerability: 0.65, supply_chain_food_fragility: 0.62,
    price_spike_transmission: 0.68, urban_food_desert_expansion: 0.55, smallholder_displacement_rate: 0.58,
    extreme_weather_frequency: 0.70, nitrogen_cycle_disruption: 0.75, agrochemical_dependency: 0.65,
    seed_sovereignty_erosion: 0.60, protein_transition_disruption: 0.48, vertical_farming_disruption_gap: 0.42,
    water_food_nexus_stress: 0.68, food_system_digitalization_risk: 0.45,
  },
  {
    entity_id: "FSC-006", region: "APAC", food_system_type: "mixed_farming",
    crop_yield_collapse_risk: 0.35, food_import_dependency: 0.32, soil_degradation_rate: 0.38,
    pollinator_collapse_index: 0.30, monoculture_vulnerability: 0.35, supply_chain_food_fragility: 0.33,
    price_spike_transmission: 0.38, urban_food_desert_expansion: 0.35, smallholder_displacement_rate: 0.32,
    extreme_weather_frequency: 0.40, nitrogen_cycle_disruption: 0.35, agrochemical_dependency: 0.38,
    seed_sovereignty_erosion: 0.32, protein_transition_disruption: 0.35, vertical_farming_disruption_gap: 0.30,
    water_food_nexus_stress: 0.40, food_system_digitalization_risk: 0.33,
  },
  {
    entity_id: "FSC-007", region: "NOAM", food_system_type: "meat_system",
    crop_yield_collapse_risk: 0.52, food_import_dependency: 0.42, soil_degradation_rate: 0.52,
    pollinator_collapse_index: 0.45, monoculture_vulnerability: 0.55, supply_chain_food_fragility: 0.55,
    price_spike_transmission: 0.50, urban_food_desert_expansion: 0.48, smallholder_displacement_rate: 0.68,
    extreme_weather_frequency: 0.55, nitrogen_cycle_disruption: 0.50, agrochemical_dependency: 0.62,
    seed_sovereignty_erosion: 0.48, protein_transition_disruption: 0.78, vertical_farming_disruption_gap: 0.52,
    water_food_nexus_stress: 0.48, food_system_digitalization_risk: 0.58,
  },
  {
    entity_id: "FSC-008", region: "MEA", food_system_type: "import_dependent",
    crop_yield_collapse_risk: 0.72, food_import_dependency: 0.85, soil_degradation_rate: 0.68,
    pollinator_collapse_index: 0.58, monoculture_vulnerability: 0.65, supply_chain_food_fragility: 0.75,
    price_spike_transmission: 0.82, urban_food_desert_expansion: 0.72, smallholder_displacement_rate: 0.65,
    extreme_weather_frequency: 0.72, nitrogen_cycle_disruption: 0.62, agrochemical_dependency: 0.58,
    seed_sovereignty_erosion: 0.68, protein_transition_disruption: 0.52, vertical_farming_disruption_gap: 0.48,
    water_food_nexus_stress: 0.78, food_system_digitalization_risk: 0.45,
  },
];

// ─── Route handler ────────────────────────────────────────────────────────────

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (!SWARM_API_URL) {
    const allResults = mockEntities.map(analyzeEntity);
    let entities = [...allResults];
    if (risk)    entities = entities.filter((e) => e.food_risk === risk);
    if (pattern) entities = entities.filter((e) => e.food_pattern === pattern);

    const risk_counts:     Record<string, number> = {};
    const pattern_counts:  Record<string, number> = {};
    const severity_counts: Record<string, number> = {};
    const action_counts:   Record<string, number> = {};
    let total_comp = 0, total_prod = 0, total_sup = 0, total_acc = 0, total_res = 0;

    for (const r of allResults) {
      risk_counts[r.food_risk]          = (risk_counts[r.food_risk] || 0) + 1;
      pattern_counts[r.food_pattern]    = (pattern_counts[r.food_pattern] || 0) + 1;
      severity_counts[r.food_severity]  = (severity_counts[r.food_severity] || 0) + 1;
      action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
      total_comp += r.food_composite;
      total_prod += r.production_score;
      total_sup  += r.supply_score;
      total_acc  += r.access_score;
      total_res  += r.resilience_score;
    }

    const n = allResults.length;
    const avg_comp = Math.round((total_comp / n) * 100) / 100;

    const pattern_entries = Object.entries(pattern_counts);
    const dominant_food_pattern = pattern_entries.reduce((a, b) => b[1] > a[1] ? b : a, pattern_entries[0])[0];

    const region_totals: Record<string, { sum: number; count: number }> = {};
    for (const r of allResults) {
      if (!region_totals[r.region]) region_totals[r.region] = { sum: 0, count: 0 };
      region_totals[r.region].sum   += r.food_composite;
      region_totals[r.region].count += 1;
    }
    const most_vulnerable_region = Object.entries(region_totals)
      .reduce((a, b) => (b[1].sum / b[1].count) > (a[1].sum / a[1].count) ? b : a)[0];

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        total_entities:                    n,
        critical_count:                    allResults.filter((r) => r.food_risk === "critical").length,
        high_count:                        allResults.filter((r) => r.food_risk === "high").length,
        moderate_count:                    allResults.filter((r) => r.food_risk === "moderate").length,
        low_count:                         allResults.filter((r) => r.food_risk === "low").length,
        food_crisis_count:                 allResults.filter((r) => r.is_food_crisis).length,
        requires_intervention_count:       allResults.filter((r) => r.requires_food_intervention).length,
        avg_food_composite:                avg_comp,
        avg_estimated_food_crisis_index:   Math.round((avg_comp / 100 * 10) * 100) / 100,
        dominant_food_pattern,
        most_vulnerable_region,
        risk_counts,
        pattern_counts,
        severity_counts,
        action_counts,
        avg_production_score:              Math.round((total_prod / n) * 10) / 10,
        avg_supply_score:                  Math.round((total_sup  / n) * 10) / 10,
        avg_access_score:                  Math.round((total_acc  / n) * 10) / 10,
        avg_resilience_score:              Math.round((total_res  / n) * 10) / 10,
      },
    } as Record<string, unknown>));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/food-system-collapse-engine`);
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(await res.json());
  } catch {}

  return NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 });
}
