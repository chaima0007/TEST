import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // FSE-001 — critical, famine_emergency (famine_risk>0.85, acute_hunger>0.80)
  {
    id: "FSE-001", food_system_type: "humanitarian_crisis", region: "SSA",
    acute_hunger_prevalence: 0.88, famine_risk_level: 0.92,
    agricultural_production_collapse: 0.78, climate_crop_failure: 0.72,
    supply_chain_disruption_food: 0.80, price_volatility_extreme: 0.75,
    seed_monopoly_risk: 0.60, water_food_nexus_stress: 0.70,
    conflict_food_weaponization: 0.85, food_import_dependency: 0.72,
    nutrition_transition_risk: 0.65, smallholder_collapse: 0.78,
    fertilizer_supply_crisis: 0.65, food_waste_system_failure: 0.55,
    urban_food_desert_expansion: 0.60, WFP_funding_gap: 0.82,
    geopolitical_food_coercion: 0.70,
  },
  // FSE-002 — low, none
  {
    id: "FSE-002", food_system_type: "diversified_economy", region: "NOAM",
    acute_hunger_prevalence: 0.08, famine_risk_level: 0.05,
    agricultural_production_collapse: 0.10, climate_crop_failure: 0.08,
    supply_chain_disruption_food: 0.10, price_volatility_extreme: 0.08,
    seed_monopoly_risk: 0.12, water_food_nexus_stress: 0.10,
    conflict_food_weaponization: 0.05, food_import_dependency: 0.15,
    nutrition_transition_risk: 0.12, smallholder_collapse: 0.08,
    fertilizer_supply_crisis: 0.10, food_waste_system_failure: 0.12,
    urban_food_desert_expansion: 0.10, WFP_funding_gap: 0.05,
    geopolitical_food_coercion: 0.08,
  },
  // FSE-003 — critical, agricultural_collapse (prod_collapse>0.85, climate_crop>0.80)
  {
    id: "FSE-003", food_system_type: "agrarian_subsistence", region: "APAC",
    acute_hunger_prevalence: 0.72, famine_risk_level: 0.70,
    agricultural_production_collapse: 0.90, climate_crop_failure: 0.86,
    supply_chain_disruption_food: 0.68, price_volatility_extreme: 0.65,
    seed_monopoly_risk: 0.60, water_food_nexus_stress: 0.75,
    conflict_food_weaponization: 0.55, food_import_dependency: 0.60,
    nutrition_transition_risk: 0.58, smallholder_collapse: 0.82,
    fertilizer_supply_crisis: 0.65, food_waste_system_failure: 0.50,
    urban_food_desert_expansion: 0.55, WFP_funding_gap: 0.72,
    geopolitical_food_coercion: 0.55,
  },
  // FSE-004 — high, food_supply_chain_crisis (supply_chain>0.85, price_vol>0.80)
  {
    id: "FSE-004", food_system_type: "import_dependent", region: "MEA",
    acute_hunger_prevalence: 0.48, famine_risk_level: 0.42,
    agricultural_production_collapse: 0.45, climate_crop_failure: 0.42,
    supply_chain_disruption_food: 0.90, price_volatility_extreme: 0.85,
    seed_monopoly_risk: 0.50, water_food_nexus_stress: 0.52,
    conflict_food_weaponization: 0.40, food_import_dependency: 0.65,
    nutrition_transition_risk: 0.48, smallholder_collapse: 0.45,
    fertilizer_supply_crisis: 0.48, food_waste_system_failure: 0.42,
    urban_food_desert_expansion: 0.45, WFP_funding_gap: 0.50,
    geopolitical_food_coercion: 0.48,
  },
  // FSE-005 — critical, food_geopolitical_weapon (geo_coercion>0.80, import_dep>0.75)
  {
    id: "FSE-005", food_system_type: "geopolitical_leverage", region: "EMEA",
    acute_hunger_prevalence: 0.65, famine_risk_level: 0.62,
    agricultural_production_collapse: 0.70, climate_crop_failure: 0.65,
    supply_chain_disruption_food: 0.72, price_volatility_extreme: 0.68,
    seed_monopoly_risk: 0.60, water_food_nexus_stress: 0.65,
    conflict_food_weaponization: 0.78, food_import_dependency: 0.82,
    nutrition_transition_risk: 0.58, smallholder_collapse: 0.65,
    fertilizer_supply_crisis: 0.60, food_waste_system_failure: 0.55,
    urban_food_desert_expansion: 0.60, WFP_funding_gap: 0.65,
    geopolitical_food_coercion: 0.88,
  },
  // FSE-006 — moderate, none
  {
    id: "FSE-006", food_system_type: "developing_mixed", region: "LATAM",
    acute_hunger_prevalence: 0.28, famine_risk_level: 0.25,
    agricultural_production_collapse: 0.30, climate_crop_failure: 0.28,
    supply_chain_disruption_food: 0.30, price_volatility_extreme: 0.28,
    seed_monopoly_risk: 0.32, water_food_nexus_stress: 0.28,
    conflict_food_weaponization: 0.22, food_import_dependency: 0.30,
    nutrition_transition_risk: 0.28, smallholder_collapse: 0.30,
    fertilizer_supply_crisis: 0.28, food_waste_system_failure: 0.25,
    urban_food_desert_expansion: 0.28, WFP_funding_gap: 0.25,
    geopolitical_food_coercion: 0.25,
  },
  // FSE-007 — high, seed_fertilizer_monopoly_crisis (seed_mono>0.80, fertilizer>0.75)
  {
    id: "FSE-007", food_system_type: "industrial_agri", region: "APAC",
    acute_hunger_prevalence: 0.45, famine_risk_level: 0.40,
    agricultural_production_collapse: 0.50, climate_crop_failure: 0.45,
    supply_chain_disruption_food: 0.48, price_volatility_extreme: 0.50,
    seed_monopoly_risk: 0.85, water_food_nexus_stress: 0.52,
    conflict_food_weaponization: 0.35, food_import_dependency: 0.55,
    nutrition_transition_risk: 0.45, smallholder_collapse: 0.55,
    fertilizer_supply_crisis: 0.80, food_waste_system_failure: 0.42,
    urban_food_desert_expansion: 0.45, WFP_funding_gap: 0.48,
    geopolitical_food_coercion: 0.50,
  },
  // FSE-008 — moderate, none (urban food system, NOAM)
  {
    id: "FSE-008", food_system_type: "urban_food_system", region: "NOAM",
    acute_hunger_prevalence: 0.22, famine_risk_level: 0.18,
    agricultural_production_collapse: 0.22, climate_crop_failure: 0.20,
    supply_chain_disruption_food: 0.25, price_volatility_extreme: 0.22,
    seed_monopoly_risk: 0.28, water_food_nexus_stress: 0.20,
    conflict_food_weaponization: 0.15, food_import_dependency: 0.35,
    nutrition_transition_risk: 0.38, smallholder_collapse: 0.20,
    fertilizer_supply_crisis: 0.22, food_waste_system_failure: 0.35,
    urban_food_desert_expansion: 0.40, WFP_funding_gap: 0.18,
    geopolitical_food_coercion: 0.18,
  },
];

type FSEInput = typeof MOCK_ENTITIES[0];

function hungerScore(e: FSEInput): number {
  return Math.round((e.acute_hunger_prevalence * 0.4 + e.famine_risk_level * 0.35 + e.conflict_food_weaponization * 0.25) * 100 * 100) / 100;
}
function productionScore(e: FSEInput): number {
  return Math.round((e.agricultural_production_collapse * 0.4 + e.climate_crop_failure * 0.35 + e.smallholder_collapse * 0.25) * 100 * 100) / 100;
}
function accessScore(e: FSEInput): number {
  return Math.round((e.supply_chain_disruption_food * 0.4 + e.price_volatility_extreme * 0.35 + e.food_import_dependency * 0.25) * 100 * 100) / 100;
}
function systemicScore(e: FSEInput): number {
  return Math.round((e.geopolitical_food_coercion * 0.4 + e.seed_monopoly_risk * 0.35 + e.fertilizer_supply_crisis * 0.25) * 100 * 100) / 100;
}
function compositeScore(hun: number, prod: number, acc: number, sys: number): number {
  return Math.round((hun * 0.30 + prod * 0.25 + acc * 0.25 + sys * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function foodPattern(e: FSEInput): string {
  if (e.famine_risk_level > 0.85 && e.acute_hunger_prevalence > 0.80) return "famine_emergency";
  if (e.agricultural_production_collapse > 0.85 && e.climate_crop_failure > 0.80) return "agricultural_collapse";
  if (e.supply_chain_disruption_food > 0.85 && e.price_volatility_extreme > 0.80) return "food_supply_chain_crisis";
  if (e.geopolitical_food_coercion > 0.80 && e.food_import_dependency > 0.75) return "food_geopolitical_weapon";
  if (e.seed_monopoly_risk > 0.80 && e.fertilizer_supply_crisis > 0.75) return "seed_fertilizer_monopoly_crisis";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "famine_systémique_catastrophique";
  if (composite >= 40) return "crise_alimentaire_majeure";
  if (composite >= 20) return "insécurité_alimentaire_structurelle";
  return "système_alimentaire_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_humanitaire_urgente_famine";
  if (risk === "high") return "mobilisation_aide_alimentaire_accélérée";
  if (risk === "moderate") return "renforcement_résilience_alimentaire";
  return "veille_sécurité_alimentaire_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Famine systémique — effondrement alimentaire catastrophique imminent";
  if (risk === "high") return "🟠 Crise alimentaire majeure détectée";
  if (risk === "moderate") return "🟡 Insécurité alimentaire structurelle active";
  return "🟢 Système alimentaire sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const hun  = hungerScore(e);
      const prod = productionScore(e);
      const acc  = accessScore(e);
      const sys  = systemicScore(e);
      const comp = compositeScore(hun, prod, acc, sys);
      const risk = riskLevel(comp);
      const pat  = foodPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:                      e.entity_id,
        food_system_type:               e.food_system_type,
        region:                         e.region,
        hunger_score:                   hun,
        production_score:               prod,
        access_score:                   acc,
        systemic_score:                 sys,
        composite_score:                comp,
        risk_level:                     risk,
        food_pattern:                   pat,
        severity:                       sev,
        recommended_action:             action,
        signal:                         sig,
        acute_hunger_prevalence:        e.acute_hunger_prevalence,
        famine_risk_level:              e.famine_risk_level,
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
      pattern_distribution[ent.food_pattern]      = (pattern_distribution[ent.food_pattern]      || 0) + 1;
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
      module_id:                              387,
      module_name:                            "Global Food Security & Famine Intelligence Engine",
      total:                                  n,
      critical:                               criticalCount,
      high:                                   highCount,
      moderate:                               moderateCount,
      low:                                    lowCount,
      avg_composite:                          avgComposite,
      risk_distribution,
      pattern_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_food_security_index:      Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "food-security-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/food-security-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "food-security-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "food-security-engine"),
      { status: 502 }
    );
  }
}
