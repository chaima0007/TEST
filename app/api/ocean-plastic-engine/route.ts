import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  // OPE-001 — critical, great_garbage_patch_expansion (plastic_conc>0.85, microplastic>0.80)
  {
    entity_id: "OPE-001", ocean_zone: "north_pacific_gyre", region: "APAC",
    plastic_concentration: 0.92, microplastic_density: 0.88, macroplastic_accumulation: 0.82,
    marine_biodiversity_loss: 0.75, coral_reef_damage: 0.70, fisheries_contamination: 0.72,
    human_health_exposure: 0.78, cleanup_effectiveness: 0.72, corporate_accountability: 0.68,
    policy_enforcement: 0.65, recycling_rate: 0.60, single_use_reduction: 0.62,
    circular_economy_adoption: 0.58, coastal_management: 0.65, treaty_compliance: 0.60,
    innovation_investment: 0.55, community_action: 0.62,
  },
  // OPE-002 — critical, microplastic_food_chain_collapse (microplastic>0.85, fisheries>0.80)
  {
    entity_id: "OPE-002", ocean_zone: "south_atlantic", region: "LATAM",
    plastic_concentration: 0.78, microplastic_density: 0.90, macroplastic_accumulation: 0.75,
    marine_biodiversity_loss: 0.72, coral_reef_damage: 0.68, fisheries_contamination: 0.85,
    human_health_exposure: 0.82, cleanup_effectiveness: 0.70, corporate_accountability: 0.72,
    policy_enforcement: 0.68, recycling_rate: 0.62, single_use_reduction: 0.60,
    circular_economy_adoption: 0.55, coastal_management: 0.62, treaty_compliance: 0.58,
    innovation_investment: 0.52, community_action: 0.65,
  },
  // OPE-003 — critical, coastal_ecosystem_destruction (coral>0.85, biodiversity>0.80)
  {
    entity_id: "OPE-003", ocean_zone: "coral_triangle", region: "SEA",
    plastic_concentration: 0.80, microplastic_density: 0.78, macroplastic_accumulation: 0.82,
    marine_biodiversity_loss: 0.88, coral_reef_damage: 0.92, fisheries_contamination: 0.75,
    human_health_exposure: 0.76, cleanup_effectiveness: 0.68, corporate_accountability: 0.65,
    policy_enforcement: 0.62, recycling_rate: 0.58, single_use_reduction: 0.55,
    circular_economy_adoption: 0.52, coastal_management: 0.60, treaty_compliance: 0.55,
    innovation_investment: 0.50, community_action: 0.60,
  },
  // OPE-004 — high, corporate_plastic_impunity (corporate_acc>0.80, policy>0.75)
  {
    entity_id: "OPE-004", ocean_zone: "mediterranean", region: "EMEA",
    plastic_concentration: 0.55, microplastic_density: 0.52, macroplastic_accumulation: 0.50,
    marine_biodiversity_loss: 0.48, coral_reef_damage: 0.45, fisheries_contamination: 0.50,
    human_health_exposure: 0.52, cleanup_effectiveness: 0.48, corporate_accountability: 0.85,
    policy_enforcement: 0.80, recycling_rate: 0.48, single_use_reduction: 0.45,
    circular_economy_adoption: 0.42, coastal_management: 0.50, treaty_compliance: 0.45,
    innovation_investment: 0.40, community_action: 0.48,
  },
  // OPE-005 — high, treaty_governance_failure (treaty>0.80, single_use>0.75)
  {
    entity_id: "OPE-005", ocean_zone: "arctic_ocean", region: "NOAM",
    plastic_concentration: 0.50, microplastic_density: 0.48, macroplastic_accumulation: 0.45,
    marine_biodiversity_loss: 0.50, coral_reef_damage: 0.42, fisheries_contamination: 0.48,
    human_health_exposure: 0.50, cleanup_effectiveness: 0.45, corporate_accountability: 0.50,
    policy_enforcement: 0.48, recycling_rate: 0.45, single_use_reduction: 0.78,
    circular_economy_adoption: 0.45, coastal_management: 0.48, treaty_compliance: 0.85,
    innovation_investment: 0.42, community_action: 0.45,
  },
  // OPE-006 — moderate, none
  {
    entity_id: "OPE-006", ocean_zone: "north_sea", region: "EMEA",
    plastic_concentration: 0.30, microplastic_density: 0.28, macroplastic_accumulation: 0.25,
    marine_biodiversity_loss: 0.30, coral_reef_damage: 0.25, fisheries_contamination: 0.28,
    human_health_exposure: 0.30, cleanup_effectiveness: 0.28, corporate_accountability: 0.25,
    policy_enforcement: 0.28, recycling_rate: 0.30, single_use_reduction: 0.28,
    circular_economy_adoption: 0.25, coastal_management: 0.30, treaty_compliance: 0.25,
    innovation_investment: 0.28, community_action: 0.30,
  },
  // OPE-007 — low, none
  {
    entity_id: "OPE-007", ocean_zone: "southern_ocean", region: "ANT",
    plastic_concentration: 0.10, microplastic_density: 0.08, macroplastic_accumulation: 0.10,
    marine_biodiversity_loss: 0.10, coral_reef_damage: 0.08, fisheries_contamination: 0.10,
    human_health_exposure: 0.08, cleanup_effectiveness: 0.10, corporate_accountability: 0.08,
    policy_enforcement: 0.10, recycling_rate: 0.12, single_use_reduction: 0.10,
    circular_economy_adoption: 0.12, coastal_management: 0.10, treaty_compliance: 0.08,
    innovation_investment: 0.10, community_action: 0.12,
  },
  // OPE-008 — low, none
  {
    entity_id: "OPE-008", ocean_zone: "baltic_sea", region: "EMEA",
    plastic_concentration: 0.12, microplastic_density: 0.10, macroplastic_accumulation: 0.12,
    marine_biodiversity_loss: 0.10, coral_reef_damage: 0.08, fisheries_contamination: 0.10,
    human_health_exposure: 0.12, cleanup_effectiveness: 0.10, corporate_accountability: 0.08,
    policy_enforcement: 0.10, recycling_rate: 0.14, single_use_reduction: 0.12,
    circular_economy_adoption: 0.14, coastal_management: 0.12, treaty_compliance: 0.10,
    innovation_investment: 0.12, community_action: 0.14,
  },
];

type OPEInput = (typeof MOCK_ENTITIES)[0];

function pollutionScore(e: OPEInput): number {
  return Math.round((e.plastic_concentration * 0.4 + e.microplastic_density * 0.35 + e.macroplastic_accumulation * 0.25) * 100 * 100) / 100;
}
function ecosystemScore(e: OPEInput): number {
  return Math.round((e.marine_biodiversity_loss * 0.4 + e.coral_reef_damage * 0.35 + e.fisheries_contamination * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: OPEInput): number {
  return Math.round((e.corporate_accountability * 0.4 + e.policy_enforcement * 0.35 + e.treaty_compliance * 0.25) * 100 * 100) / 100;
}
function healthScore(e: OPEInput): number {
  return Math.round((e.human_health_exposure * 0.4 + e.cleanup_effectiveness * 0.35 + e.community_action * 0.25) * 100 * 100) / 100;
}
function compositeScore(pol: number, eco: number, gov: number, hlt: number): number {
  return Math.round((pol * 0.30 + eco * 0.25 + gov * 0.25 + hlt * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function oceanPattern(e: OPEInput): string {
  if (e.plastic_concentration > 0.85 && e.microplastic_density > 0.80) return "great_garbage_patch_expansion";
  if (e.microplastic_density > 0.85 && e.fisheries_contamination > 0.80) return "microplastic_food_chain_collapse";
  if (e.coral_reef_damage > 0.85 && e.marine_biodiversity_loss > 0.80) return "coastal_ecosystem_destruction";
  if (e.corporate_accountability > 0.80 && e.policy_enforcement > 0.75) return "corporate_plastic_impunity";
  if (e.treaty_compliance > 0.80 && e.single_use_reduction > 0.75) return "treaty_governance_failure";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_plastique_océanique_systémique";
  if (composite >= 40) return "crise_écosystème_marin_majeure";
  if (composite >= 20) return "contamination_plastique_structurelle";
  return "surveillance_débris_marins_active";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_dépollution_océanique_critique";
  if (risk === "high") return "mobilisation_accélérée_nettoyage_zones_vulnérables";
  if (risk === "moderate") return "renforcement_politiques_réduction_plastique";
  return "veille_contamination_plastique_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise plastique océanique systémique — écosystèmes marins en péril";
  if (risk === "high") return "🟠 Crise écosystème marin majeure détectée";
  if (risk === "moderate") return "🟡 Contamination plastique structurelle active";
  return "🟢 Surveillance débris marins active";
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const pol  = pollutionScore(e);
      const eco  = ecosystemScore(e);
      const gov  = governanceScore(e);
      const hlt  = healthScore(e);
      const comp = compositeScore(pol, eco, gov, hlt);
      const risk = riskLevel(comp);
      const pat  = oceanPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        entity_id:             e.entity_id,
        ocean_zone:            e.ocean_zone,
        region:                e.region,
        pollution_score:       pol,
        ecosystem_score:       eco,
        governance_score:      gov,
        health_score:          hlt,
        composite_score:       comp,
        risk_level:            risk,
        ocean_pattern:         pat,
        severity:              sev,
        recommended_action:    action,
        signal:                sig,
        plastic_concentration: e.plastic_concentration,
        microplastic_density:  e.microplastic_density,
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
      pattern_distribution[ent.ocean_pattern]     = (pattern_distribution[ent.ocean_pattern]     || 0) + 1;
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
      module_id:                           402,
      module_name:                         "Pollution Plastique Océanique & Débris Marins Intelligence Engine",
      total:                               n,
      critical:                            criticalCount,
      high:                                highCount,
      moderate:                            moderateCount,
      low:                                 lowCount,
      avg_composite:                       avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_ocean_plastic_index:   Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary } as Record<string, unknown>)
    );
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/ocean-plastic-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(sealResponse(await res.json()));
  } catch {}
  return NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 });
}
