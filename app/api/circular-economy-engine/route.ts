import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// 8 mock entities covering all 5 patterns and all 4 risk levels
// CEE-001: critical / linear_lock_in
// CEE-002: low / none
// CEE-003: high / waste_crisis
// CEE-004: low / none
// CEE-005: critical / regeneration_collapse
// CEE-006: moderate / none
// CEE-007: high / circular_inequality
// CEE-008: critical / systemic_inertia
const MOCK_ENTITIES = [
  {
    entity_id: "CEE-001", economy_sector: "manufacturing", region: "EMEA",
    material_circularity_rate: 0.20, waste_generation_index: 0.55, resource_efficiency_score: 0.25,
    product_lifecycle_extension: 0.30, regenerative_business_model_adoption: 0.30, supply_loop_closure_rate: 0.28,
    industrial_symbiosis_level: 0.28, consumer_circular_behavior: 0.30, repair_reuse_accessibility: 0.32,
    circular_financing_availability: 0.28, regulatory_circular_support: 0.35, linear_economy_lock_in: 0.80,
    circular_innovation_pipeline: 0.28, carbon_circularity_coupling: 0.25, biodiversity_regeneration_index: 0.30,
    social_circular_equity: 0.32, systemic_circular_transition_readiness: 0.28,
  },
  {
    entity_id: "CEE-002", economy_sector: "services", region: "APAC",
    material_circularity_rate: 0.85, waste_generation_index: 0.10, resource_efficiency_score: 0.88,
    product_lifecycle_extension: 0.82, regenerative_business_model_adoption: 0.85, supply_loop_closure_rate: 0.80,
    industrial_symbiosis_level: 0.82, consumer_circular_behavior: 0.85, repair_reuse_accessibility: 0.80,
    circular_financing_availability: 0.82, regulatory_circular_support: 0.85, linear_economy_lock_in: 0.10,
    circular_innovation_pipeline: 0.88, carbon_circularity_coupling: 0.80, biodiversity_regeneration_index: 0.85,
    social_circular_equity: 0.82, systemic_circular_transition_readiness: 0.88,
  },
  {
    entity_id: "CEE-003", economy_sector: "logistics", region: "NOAM",
    material_circularity_rate: 0.42, waste_generation_index: 0.78, resource_efficiency_score: 0.45,
    product_lifecycle_extension: 0.40, regenerative_business_model_adoption: 0.45, supply_loop_closure_rate: 0.28,
    industrial_symbiosis_level: 0.40, consumer_circular_behavior: 0.45, repair_reuse_accessibility: 0.42,
    circular_financing_availability: 0.40, regulatory_circular_support: 0.45, linear_economy_lock_in: 0.50,
    circular_innovation_pipeline: 0.42, carbon_circularity_coupling: 0.38, biodiversity_regeneration_index: 0.42,
    social_circular_equity: 0.45, systemic_circular_transition_readiness: 0.42,
  },
  {
    entity_id: "CEE-004", economy_sector: "technology", region: "LATAM",
    material_circularity_rate: 0.82, waste_generation_index: 0.12, resource_efficiency_score: 0.80,
    product_lifecycle_extension: 0.85, regenerative_business_model_adoption: 0.80, supply_loop_closure_rate: 0.82,
    industrial_symbiosis_level: 0.80, consumer_circular_behavior: 0.82, repair_reuse_accessibility: 0.85,
    circular_financing_availability: 0.80, regulatory_circular_support: 0.82, linear_economy_lock_in: 0.12,
    circular_innovation_pipeline: 0.85, carbon_circularity_coupling: 0.82, biodiversity_regeneration_index: 0.80,
    social_circular_equity: 0.82, systemic_circular_transition_readiness: 0.85,
  },
  {
    entity_id: "CEE-005", economy_sector: "agriculture", region: "MEA",
    material_circularity_rate: 0.22, waste_generation_index: 0.60, resource_efficiency_score: 0.25,
    product_lifecycle_extension: 0.20, regenerative_business_model_adoption: 0.28, supply_loop_closure_rate: 0.25,
    industrial_symbiosis_level: 0.22, consumer_circular_behavior: 0.25, repair_reuse_accessibility: 0.28,
    circular_financing_availability: 0.22, regulatory_circular_support: 0.28, linear_economy_lock_in: 0.55,
    circular_innovation_pipeline: 0.25, carbon_circularity_coupling: 0.20, biodiversity_regeneration_index: 0.28,
    social_circular_equity: 0.30, systemic_circular_transition_readiness: 0.28,
  },
  {
    entity_id: "CEE-006", economy_sector: "retail", region: "EMEA",
    material_circularity_rate: 0.62, waste_generation_index: 0.35, resource_efficiency_score: 0.60,
    product_lifecycle_extension: 0.58, regenerative_business_model_adoption: 0.60, supply_loop_closure_rate: 0.62,
    industrial_symbiosis_level: 0.58, consumer_circular_behavior: 0.60, repair_reuse_accessibility: 0.62,
    circular_financing_availability: 0.58, regulatory_circular_support: 0.62, linear_economy_lock_in: 0.35,
    circular_innovation_pipeline: 0.60, carbon_circularity_coupling: 0.58, biodiversity_regeneration_index: 0.60,
    social_circular_equity: 0.62, systemic_circular_transition_readiness: 0.60,
  },
  {
    entity_id: "CEE-007", economy_sector: "construction", region: "APAC",
    material_circularity_rate: 0.48, waste_generation_index: 0.45, resource_efficiency_score: 0.45,
    product_lifecycle_extension: 0.45, regenerative_business_model_adoption: 0.48, supply_loop_closure_rate: 0.45,
    industrial_symbiosis_level: 0.48, consumer_circular_behavior: 0.48, repair_reuse_accessibility: 0.32,
    circular_financing_availability: 0.45, regulatory_circular_support: 0.48, linear_economy_lock_in: 0.50,
    circular_innovation_pipeline: 0.45, carbon_circularity_coupling: 0.42, biodiversity_regeneration_index: 0.45,
    social_circular_equity: 0.28, systemic_circular_transition_readiness: 0.48,
  },
  {
    entity_id: "CEE-008", economy_sector: "energy", region: "LATAM",
    material_circularity_rate: 0.25, waste_generation_index: 0.55, resource_efficiency_score: 0.28,
    product_lifecycle_extension: 0.25, regenerative_business_model_adoption: 0.28, supply_loop_closure_rate: 0.25,
    industrial_symbiosis_level: 0.28, consumer_circular_behavior: 0.25, repair_reuse_accessibility: 0.28,
    circular_financing_availability: 0.25, regulatory_circular_support: 0.32, linear_economy_lock_in: 0.55,
    circular_innovation_pipeline: 0.25, carbon_circularity_coupling: 0.22, biodiversity_regeneration_index: 0.28,
    social_circular_equity: 0.28, systemic_circular_transition_readiness: 0.28,
  },
];

type MockEntity = typeof MOCK_ENTITIES[0];

function materialScore(e: MockEntity): number {
  return Math.round((e.material_circularity_rate * 0.4 + e.resource_efficiency_score * 0.35 + e.supply_loop_closure_rate * 0.25) * 100 * 100) / 100;
}
function regenerationScore(e: MockEntity): number {
  return Math.round((e.regenerative_business_model_adoption * 0.4 + e.industrial_symbiosis_level * 0.35 + e.circular_innovation_pipeline * 0.25) * 100 * 100) / 100;
}
function behaviorScore(e: MockEntity): number {
  return Math.round((e.consumer_circular_behavior * 0.4 + e.repair_reuse_accessibility * 0.35 + e.circular_financing_availability * 0.25) * 100 * 100) / 100;
}
function systemScore(e: MockEntity): number {
  return Math.round((e.systemic_circular_transition_readiness * 0.4 + e.regulatory_circular_support * 0.35 + e.biodiversity_regeneration_index * 0.25) * 100 * 100) / 100;
}
function compositeScore(mat: number, reg: number, beh: number, sys: number): number {
  return Math.round((mat * 0.30 + reg * 0.25 + beh * 0.25 + sys * 0.20) * 100) / 100;
}
function riskLevel(comp: number): string {
  if (comp < 40) return "critical";
  if (comp < 60) return "high";
  if (comp < 80) return "moderate";
  return "low";
}
function circularPattern(e: MockEntity): string {
  if (e.material_circularity_rate < 0.35 && e.linear_economy_lock_in > 0.65) return "linear_lock_in";
  if (e.waste_generation_index > 0.70 && e.supply_loop_closure_rate < 0.35) return "waste_crisis";
  if (e.regenerative_business_model_adoption < 0.35 && e.biodiversity_regeneration_index < 0.35) return "regeneration_collapse";
  if (e.social_circular_equity < 0.35 && e.repair_reuse_accessibility < 0.40) return "circular_inequality";
  if (e.systemic_circular_transition_readiness < 0.35 && e.regulatory_circular_support < 0.40) return "systemic_inertia";
  return "none";
}
function severity(risk: string): string {
  const map: Record<string, string> = {
    critical: "effondrement_circulaire",
    high:     "transition_bloquée",
    moderate: "inertie_structurelle",
    low:      "transition_engagée",
  };
  return map[risk] ?? risk;
}
function recommendedAction(risk: string): string {
  const map: Record<string, string> = {
    critical: "activation_protocole_transition_d_urgence",
    high:     "restructuration_modèle_économique",
    moderate: "accélération_leviers_circulaires",
    low:      "optimisation_continue",
  };
  return map[risk] ?? risk;
}
function signal(risk: string): string {
  const map: Record<string, string> = {
    critical: "🔴 Économie linéaire dominante — risque systémique circulaire",
    high:     "🟠 Blocages structurels — transition incomplète",
    moderate: "🟡 Transition en cours — inertie résiduelle",
    low:      "🟢 Circularité avancée — modèle régénératif",
  };
  return map[risk] ?? risk;
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const mat = materialScore(e);
      const reg = regenerationScore(e);
      const beh = behaviorScore(e);
      const sys = systemScore(e);
      const comp = compositeScore(mat, reg, beh, sys);
      const risk = riskLevel(comp);
      const pattern = circularPattern(e);
      const sev = severity(risk);
      const action = recommendedAction(risk);
      const sig = signal(risk);
      return {
        entity_id: e.entity_id,
        economy_sector: e.economy_sector,
        region: e.region,
        material_score: mat,
        regeneration_score: reg,
        behavior_score: beh,
        system_score: sys,
        composite_score: comp,
        risk_level: risk,
        circular_pattern: pattern,
        severity: sev,
        recommended_action: action,
        signal: sig,
        product_lifecycle_extension: e.product_lifecycle_extension,
        carbon_circularity_coupling: e.carbon_circularity_coupling,
      };
    });

    const riskDist: Record<string, number> = {};
    const patDist: Record<string, number> = {};
    const sevDist: Record<string, number> = {};
    const actionDist: Record<string, number> = {};
    let totalComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      riskDist[ent.risk_level] = (riskDist[ent.risk_level] || 0) + 1;
      patDist[ent.circular_pattern] = (patDist[ent.circular_pattern] || 0) + 1;
      sevDist[ent.severity] = (sevDist[ent.severity] || 0) + 1;
      actionDist[ent.recommended_action] = (actionDist[ent.recommended_action] || 0) + 1;
      totalComp += ent.composite_score;
      if (ent.risk_level === "critical") criticalCount++;
      else if (ent.risk_level === "high") highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(totalComp / n * 100) / 100;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id: 329,
        module_name: "Circular Economy & Regenerative Business Intelligence Engine",
        total_entities: n,
        critical_count: criticalCount,
        high_count: highCount,
        moderate_count: moderateCount,
        low_count: lowCount,
        avg_composite: avgComposite,
        pattern_distribution: patDist,
        risk_distribution: riskDist,
        severity_distribution: sevDist,
        action_distribution: actionDist,
        avg_estimated_circularity_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
      },
    } as Record<string, unknown>));
  }

  try {
    const res = await fetch(`${SWARM_API_URL}/circular-economy-engine`);
    if (res.ok) return NextResponse.json(sealResponse(await res.json() as Record<string, unknown>));
  } catch {}

  return NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 });
}
