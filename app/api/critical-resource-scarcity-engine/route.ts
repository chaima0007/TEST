import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // CRS-001 — critical, supply_shock (rare_earth_metals, EMEA)
  {
    id: "CRS-001", resource_category: "rare_earth_metals", region: "EMEA",
    supply_concentration_risk: 0.88, demand_growth_rate: 0.55, substitution_difficulty: 0.60,
    geopolitical_supply_risk: 0.62, stockpile_adequacy: 0.18, recycling_circularity_rate: 0.20,
    processing_choke_point: 0.72, reserve_depletion_rate: 0.50, alternative_source_development: 0.22,
    price_volatility_index: 0.75, import_dependency: 0.60, environmental_extraction_cost: 0.68,
    water_stress_index: 0.45, food_system_fragility: 0.30, semiconductor_supply_risk: 0.50,
    rare_earth_concentration: 0.60, critical_mineral_pipeline_gap: 0.70,
  },
  // CRS-002 — low, resource_abundant/none (water_resources, APAC)
  {
    id: "CRS-002", resource_category: "water_resources", region: "APAC",
    supply_concentration_risk: 0.12, demand_growth_rate: 0.15, substitution_difficulty: 0.10,
    geopolitical_supply_risk: 0.10, stockpile_adequacy: 0.88, recycling_circularity_rate: 0.82,
    processing_choke_point: 0.08, reserve_depletion_rate: 0.12, alternative_source_development: 0.85,
    price_volatility_index: 0.10, import_dependency: 0.08, environmental_extraction_cost: 0.10,
    water_stress_index: 0.15, food_system_fragility: 0.12, semiconductor_supply_risk: 0.10,
    rare_earth_concentration: 0.08, critical_mineral_pipeline_gap: 0.10,
  },
  // CRS-003 — high, geopolitical_embargo (semiconductors, NOAM)
  {
    id: "CRS-003", resource_category: "semiconductors", region: "NOAM",
    supply_concentration_risk: 0.60, demand_growth_rate: 0.62, substitution_difficulty: 0.58,
    geopolitical_supply_risk: 0.78, stockpile_adequacy: 0.40, recycling_circularity_rate: 0.35,
    processing_choke_point: 0.55, reserve_depletion_rate: 0.48, alternative_source_development: 0.38,
    price_volatility_index: 0.68, import_dependency: 0.72, environmental_extraction_cost: 0.55,
    water_stress_index: 0.40, food_system_fragility: 0.25, semiconductor_supply_risk: 0.80,
    rare_earth_concentration: 0.50, critical_mineral_pipeline_gap: 0.65,
  },
  // CRS-004 — low, resource_abundant/none (water_resources, LATAM)
  {
    id: "CRS-004", resource_category: "water_resources", region: "LATAM",
    supply_concentration_risk: 0.15, demand_growth_rate: 0.18, substitution_difficulty: 0.12,
    geopolitical_supply_risk: 0.12, stockpile_adequacy: 0.85, recycling_circularity_rate: 0.78,
    processing_choke_point: 0.10, reserve_depletion_rate: 0.15, alternative_source_development: 0.80,
    price_volatility_index: 0.12, import_dependency: 0.10, environmental_extraction_cost: 0.12,
    water_stress_index: 0.20, food_system_fragility: 0.18, semiconductor_supply_risk: 0.12,
    rare_earth_concentration: 0.10, critical_mineral_pipeline_gap: 0.12,
  },
  // CRS-005 — critical, demand_explosion (oil_gas, MEA)
  {
    id: "CRS-005", resource_category: "oil_gas", region: "MEA",
    supply_concentration_risk: 0.72, demand_growth_rate: 0.85, substitution_difficulty: 0.78,
    geopolitical_supply_risk: 0.68, stockpile_adequacy: 0.30, recycling_circularity_rate: 0.15,
    processing_choke_point: 0.65, reserve_depletion_rate: 0.70, alternative_source_development: 0.20,
    price_volatility_index: 0.82, import_dependency: 0.58, environmental_extraction_cost: 0.75,
    water_stress_index: 0.72, food_system_fragility: 0.60, semiconductor_supply_risk: 0.35,
    rare_earth_concentration: 0.40, critical_mineral_pipeline_gap: 0.68,
  },
  // CRS-006 — moderate, none (food_systems, EMEA)
  {
    id: "CRS-006", resource_category: "food_systems", region: "EMEA",
    supply_concentration_risk: 0.35, demand_growth_rate: 0.38, substitution_difficulty: 0.32,
    geopolitical_supply_risk: 0.30, stockpile_adequacy: 0.58, recycling_circularity_rate: 0.50,
    processing_choke_point: 0.28, reserve_depletion_rate: 0.35, alternative_source_development: 0.52,
    price_volatility_index: 0.42, import_dependency: 0.38, environmental_extraction_cost: 0.40,
    water_stress_index: 0.38, food_system_fragility: 0.45, semiconductor_supply_risk: 0.25,
    rare_earth_concentration: 0.28, critical_mineral_pipeline_gap: 0.35,
  },
  // CRS-007 — high, depletion_crisis (semiconductors, APAC)
  {
    id: "CRS-007", resource_category: "semiconductors", region: "APAC",
    supply_concentration_risk: 0.58, demand_growth_rate: 0.60, substitution_difficulty: 0.55,
    geopolitical_supply_risk: 0.52, stockpile_adequacy: 0.42, recycling_circularity_rate: 0.32,
    processing_choke_point: 0.55, reserve_depletion_rate: 0.78, alternative_source_development: 0.22,
    price_volatility_index: 0.65, import_dependency: 0.60, environmental_extraction_cost: 0.52,
    water_stress_index: 0.48, food_system_fragility: 0.30, semiconductor_supply_risk: 0.75,
    rare_earth_concentration: 0.55, critical_mineral_pipeline_gap: 0.70,
  },
  // CRS-008 — critical, processing_monopoly (rare_earth_metals, NOAM)
  {
    id: "CRS-008", resource_category: "rare_earth_metals", region: "NOAM",
    supply_concentration_risk: 0.75, demand_growth_rate: 0.65, substitution_difficulty: 0.60,
    geopolitical_supply_risk: 0.70, stockpile_adequacy: 0.25, recycling_circularity_rate: 0.18,
    processing_choke_point: 0.82, reserve_depletion_rate: 0.65, alternative_source_development: 0.28,
    price_volatility_index: 0.78, import_dependency: 0.62, environmental_extraction_cost: 0.72,
    water_stress_index: 0.50, food_system_fragility: 0.35, semiconductor_supply_risk: 0.60,
    rare_earth_concentration: 0.78, critical_mineral_pipeline_gap: 0.80,
  },
];

type EntityInput = typeof MOCK_ENTITIES[0];

function supplyScore(e: EntityInput): number {
  const raw = (
    e.supply_concentration_risk * 0.4
    + e.processing_choke_point * 0.35
    + (1 - e.stockpile_adequacy) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function demandScore(e: EntityInput): number {
  const raw = (
    e.demand_growth_rate * 0.4
    + e.substitution_difficulty * 0.35
    + e.reserve_depletion_rate * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function geopoliticalScore(e: EntityInput): number {
  const raw = (
    e.geopolitical_supply_risk * 0.4
    + e.import_dependency * 0.35
    + e.rare_earth_concentration * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function sustainabilityScore(e: EntityInput): number {
  const raw = (
    e.environmental_extraction_cost * 0.4
    + (1 - e.recycling_circularity_rate) * 0.35
    + (1 - e.alternative_source_development) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function scarcityComposite(supply: number, demand: number, geo: number, sust: number): number {
  return Math.round((supply * 0.30 + demand * 0.25 + geo * 0.25 + sust * 0.20) * 100) / 100;
}

function scarcityRisk(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}

function scarcityPattern(e: EntityInput): string {
  if (e.supply_concentration_risk >= 0.70 && (1 - e.stockpile_adequacy) >= 0.60) return "supply_shock";
  if (e.geopolitical_supply_risk >= 0.70 && e.import_dependency >= 0.65) return "geopolitical_embargo";
  if (e.demand_growth_rate >= 0.70 && e.substitution_difficulty >= 0.65) return "demand_explosion";
  if (e.reserve_depletion_rate >= 0.70 && (1 - e.alternative_source_development) >= 0.60) return "depletion_crisis";
  if (e.processing_choke_point >= 0.70 && e.rare_earth_concentration >= 0.65) return "processing_monopoly";
  return "none";
}

function scarcitySeverity(composite: number): string {
  if (composite >= 75) return "resource_emergency";
  if (composite >= 50) return "high_scarcity";
  if (composite >= 25) return "supply_tension";
  return "resource_abundant";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "resource_emergency_program";
  if (risk === "high" && pattern === "geopolitical_embargo") return "supply_diversification";
  if (risk === "high") return "strategic_reserve_buildup";
  if (risk === "moderate") return "resource_monitoring";
  return "no_action";
}

function scarcitySignal(e: EntityInput, risk: string, composite: number): string {
  if (risk === "critical") {
    return `Critique — concentration approvisionnement ${Math.round(e.supply_concentration_risk * 100)}% — risque géopolitique ${Math.round(e.geopolitical_supply_risk * 100)}% — composite ${Math.round(composite)}`;
  }
  if (risk === "high") {
    return `Élevé — croissance demande ${Math.round(e.demand_growth_rate * 100)}% — dépendance importations ${Math.round(e.import_dependency * 100)}% — composite ${Math.round(composite)}`;
  }
  if (risk === "moderate") {
    return `Modéré — taux recyclage ${Math.round(e.recycling_circularity_rate * 100)}% — composite ${Math.round(composite)}`;
  }
  return "Ressources critiques abondantes — diversification approvisionnement, circularité élevée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[critical-resource-scarcity-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const risk_counts: Record<string, number>     = {};
    const pattern_counts: Record<string, number>  = {};
    const severity_counts: Record<string, number> = {};
    const action_counts: Record<string, number>   = {};
    let tSupply = 0, tDemand = 0, tGeo = 0, tSust = 0, tComp = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      risk_counts[ent.scarcity_risk]       = (risk_counts[ent.scarcity_risk]       || 0) + 1;
      pattern_counts[ent.scarcity_pattern] = (pattern_counts[ent.scarcity_pattern] || 0) + 1;
      severity_counts[ent.scarcity_severity] = (severity_counts[ent.scarcity_severity] || 0) + 1;
      action_counts[ent.recommended_action]  = (action_counts[ent.recommended_action]  || 0) + 1;
      tSupply += ent.supply_score;
      tDemand += ent.demand_score;
      tGeo    += ent.geopolitical_score;
      tSust   += ent.sustainability_score;
      tComp   += ent.scarcity_composite;
      if (ent.is_in_scarcity_crisis)          crisisCount++;
      if (ent.requires_scarcity_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      total:                          n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_scarcity_composite:         avgComposite,
      scarcity_crisis_count:          crisisCount,
      scarcity_intervention_count:    interventionCount,
      avg_supply_score:               Math.round(tSupply / n * 10) / 10,
      avg_demand_score:               Math.round(tDemand / n * 10) / 10,
      avg_geopolitical_score:         Math.round(tGeo / n * 10) / 10,
      avg_sustainability_score:       Math.round(tSust / n * 10) / 10,
      avg_estimated_scarcity_index:   Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "critical-resource-scarcity-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/critical-resource-scarcity-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return sealResponse(NextResponse.json(sealResponse(data, "critical-resource-scarcity-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream unavailable" }, "critical-resource-scarcity-engine"),
      { status: 502 }
    ));
  }
}
