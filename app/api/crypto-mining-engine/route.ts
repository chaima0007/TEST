import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  // CME-001 — critical, carbon_bomb_mining_operation (carbon_intensity>0.85, coal_dependency>0.80)
  {
    entity_id: "CME-001", mining_type: "proof_of_work", region: "APAC",
    carbon_intensity: 0.90, renewable_energy_share: 0.05, coal_dependency: 0.88,
    energy_consumption_gwh: 0.85, water_usage_intensity: 0.80, cooling_water_stress: 0.78,
    e_waste_generation: 0.75, hardware_lifecycle: 0.20, grid_strain: 0.80,
    local_energy_price_impact: 0.75, regulatory_compliance: 0.10, community_opposition: 0.85,
    noise_pollution: 0.80, heat_island_effect: 0.75, toxic_chemical_use: 0.70,
    carbon_credit_offset: 0.10, energy_efficiency_rating: 0.10,
  },
  // CME-002 — critical, coal_powered_crypto_expansion (coal_dep>0.80, energy_consump>0.75, carbon_int≤0.85)
  {
    entity_id: "CME-002", mining_type: "proof_of_work", region: "EMEA",
    carbon_intensity: 0.75, renewable_energy_share: 0.08, coal_dependency: 0.85,
    energy_consumption_gwh: 0.88, water_usage_intensity: 0.78, cooling_water_stress: 0.75,
    e_waste_generation: 0.72, hardware_lifecycle: 0.22, grid_strain: 0.82,
    local_energy_price_impact: 0.78, regulatory_compliance: 0.12, community_opposition: 0.80,
    noise_pollution: 0.75, heat_island_effect: 0.70, toxic_chemical_use: 0.68,
    carbon_credit_offset: 0.10, energy_efficiency_rating: 0.12,
  },
  // CME-003 — critical, water_crisis_cooling_drain (water_usage>0.80, cooling_water>0.75, carbon_int≤0.85, coal_dep≤0.80)
  {
    entity_id: "CME-003", mining_type: "asic_mining", region: "NOAM",
    carbon_intensity: 0.78, renewable_energy_share: 0.10, coal_dependency: 0.70,
    energy_consumption_gwh: 0.82, water_usage_intensity: 0.88, cooling_water_stress: 0.85,
    e_waste_generation: 0.70, hardware_lifecycle: 0.25, grid_strain: 0.78,
    local_energy_price_impact: 0.72, regulatory_compliance: 0.15, community_opposition: 0.78,
    noise_pollution: 0.70, heat_island_effect: 0.72, toxic_chemical_use: 0.65,
    carbon_credit_offset: 0.12, energy_efficiency_rating: 0.15,
  },
  // CME-004 — high, e_waste_toxic_dumping (e_waste>0.80, toxic_chemical>0.75)
  {
    entity_id: "CME-004", mining_type: "gpu_mining", region: "LATAM",
    carbon_intensity: 0.50, renewable_energy_share: 0.30, coal_dependency: 0.45,
    energy_consumption_gwh: 0.52, water_usage_intensity: 0.48, cooling_water_stress: 0.50,
    e_waste_generation: 0.85, hardware_lifecycle: 0.30, grid_strain: 0.50,
    local_energy_price_impact: 0.48, regulatory_compliance: 0.35, community_opposition: 0.55,
    noise_pollution: 0.45, heat_island_effect: 0.48, toxic_chemical_use: 0.80,
    carbon_credit_offset: 0.40, energy_efficiency_rating: 0.45,
  },
  // CME-005 — high, energy_grid_destabilization (grid_strain>0.80, local_energy_price>0.75)
  {
    entity_id: "CME-005", mining_type: "proof_of_work", region: "SSA",
    carbon_intensity: 0.48, renewable_energy_share: 0.28, coal_dependency: 0.45,
    energy_consumption_gwh: 0.75, water_usage_intensity: 0.50, cooling_water_stress: 0.48,
    e_waste_generation: 0.55, hardware_lifecycle: 0.48, grid_strain: 0.85,
    local_energy_price_impact: 0.80, regulatory_compliance: 0.30, community_opposition: 0.72,
    noise_pollution: 0.60, heat_island_effect: 0.55, toxic_chemical_use: 0.50,
    carbon_credit_offset: 0.42, energy_efficiency_rating: 0.50,
  },
  // CME-006 — moderate, none
  {
    entity_id: "CME-006", mining_type: "proof_of_stake", region: "EMEA",
    carbon_intensity: 0.30, renewable_energy_share: 0.55, coal_dependency: 0.28,
    energy_consumption_gwh: 0.32, water_usage_intensity: 0.30, cooling_water_stress: 0.28,
    e_waste_generation: 0.30, hardware_lifecycle: 0.62, grid_strain: 0.30,
    local_energy_price_impact: 0.28, regulatory_compliance: 0.65, community_opposition: 0.30,
    noise_pollution: 0.25, heat_island_effect: 0.28, toxic_chemical_use: 0.25,
    carbon_credit_offset: 0.55, energy_efficiency_rating: 0.60,
  },
  // CME-007 — low, none
  {
    entity_id: "CME-007", mining_type: "proof_of_stake", region: "NOAM",
    carbon_intensity: 0.10, renewable_energy_share: 0.88, coal_dependency: 0.08,
    energy_consumption_gwh: 0.10, water_usage_intensity: 0.10, cooling_water_stress: 0.08,
    e_waste_generation: 0.10, hardware_lifecycle: 0.88, grid_strain: 0.12,
    local_energy_price_impact: 0.08, regulatory_compliance: 0.92, community_opposition: 0.08,
    noise_pollution: 0.08, heat_island_effect: 0.10, toxic_chemical_use: 0.08,
    carbon_credit_offset: 0.85, energy_efficiency_rating: 0.88,
  },
  // CME-008 — low, none
  {
    entity_id: "CME-008", mining_type: "green_mining", region: "APAC",
    carbon_intensity: 0.12, renewable_energy_share: 0.85, coal_dependency: 0.10,
    energy_consumption_gwh: 0.12, water_usage_intensity: 0.12, cooling_water_stress: 0.10,
    e_waste_generation: 0.12, hardware_lifecycle: 0.85, grid_strain: 0.10,
    local_energy_price_impact: 0.10, regulatory_compliance: 0.90, community_opposition: 0.10,
    noise_pollution: 0.10, heat_island_effect: 0.12, toxic_chemical_use: 0.10,
    carbon_credit_offset: 0.82, energy_efficiency_rating: 0.85,
  },
];

type CMEInput = typeof MOCK_ENTITIES[0];

function carbonScore(e: CMEInput): number {
  return Math.round((e.carbon_intensity * 0.45 + e.coal_dependency * 0.35 + (1 - e.carbon_credit_offset) * 0.20) * 100 * 100) / 100;
}
function energyScore(e: CMEInput): number {
  return Math.round((e.energy_consumption_gwh * 0.40 + e.grid_strain * 0.35 + (1 - e.energy_efficiency_rating) * 0.25) * 100 * 100) / 100;
}
function waterScore(e: CMEInput): number {
  return Math.round((e.water_usage_intensity * 0.50 + e.cooling_water_stress * 0.50) * 100 * 100) / 100;
}
function eWasteScore(e: CMEInput): number {
  return Math.round((e.e_waste_generation * 0.50 + (1 - e.hardware_lifecycle) * 0.30 + e.toxic_chemical_use * 0.20) * 100 * 100) / 100;
}
function compositeScore(carbon: number, energy: number, water: number, eWaste: number): number {
  return Math.round((carbon * 0.30 + energy * 0.25 + water * 0.25 + eWaste * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function miningPattern(e: CMEInput): string {
  if (e.carbon_intensity > 0.85 && e.coal_dependency > 0.80) return "carbon_bomb_mining_operation";
  if (e.coal_dependency > 0.80 && e.energy_consumption_gwh > 0.75) return "coal_powered_crypto_expansion";
  if (e.water_usage_intensity > 0.80 && e.cooling_water_stress > 0.75) return "water_crisis_cooling_drain";
  if (e.e_waste_generation > 0.80 && e.toxic_chemical_use > 0.75) return "e_waste_toxic_dumping";
  if (e.grid_strain > 0.80 && e.local_energy_price_impact > 0.75) return "energy_grid_destabilization";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_environnementale_minage_critique";
  if (composite >= 40) return "impact_climatique_minage_élevé";
  if (composite >= 20) return "pression_environnementale_modérée";
  return "minage_sous_surveillance_environnementale";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_arrêt_minage_polluant";
  if (risk === "high") return "transition_énergies_renouvelables_minage_accélérée";
  if (risk === "moderate") return "audit_impact_environnemental_minage_requis";
  return "veille_continue_minage_cryptomonnaie";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise environnementale minage critique — impact planétaire immédiat";
  if (risk === "high") return "🟠 Impact climatique minage élevé détecté";
  if (risk === "moderate") return "🟡 Pression environnementale minage modérée active";
  return "🟢 Minage sous surveillance environnementale";
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const carbon  = carbonScore(e);
      const energy  = energyScore(e);
      const water   = waterScore(e);
      const eWaste  = eWasteScore(e);
      const comp    = compositeScore(carbon, energy, water, eWaste);
      const risk    = riskLevel(comp);
      const pat     = miningPattern(e);
      const sev     = severity(comp);
      const action  = recommendedAction(risk);
      const sig     = signal(risk);
      return {
        entity_id:          e.entity_id,
        mining_type:        e.mining_type,
        region:             e.region,
        carbon_score:       carbon,
        energy_score:       energy,
        water_score:        water,
        e_waste_score:      eWaste,
        composite_score:    comp,
        risk_level:         risk,
        mining_pattern:     pat,
        severity:           sev,
        recommended_action: action,
        signal:             sig,
        carbon_intensity:   e.carbon_intensity,
        coal_dependency:    e.coal_dependency,
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
      pattern_distribution[ent.mining_pattern]    = (pattern_distribution[ent.mining_pattern]    || 0) + 1;
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
      module_id:                          399,
      module_name:                        "Minage Cryptomonnaie & Impact Environnemental Intelligence Engine",
      total:                              n,
      critical:                           criticalCount,
      high:                               highCount,
      moderate:                           moderateCount,
      low:                                lowCount,
      avg_composite:                      avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_mining_env_index:     Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/crypto-mining-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(sealResponse(await res.json()));
  } catch {}
  return NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 });
}
