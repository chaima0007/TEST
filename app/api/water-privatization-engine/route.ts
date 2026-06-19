import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  // WPE-001 — critical, corporate_water_monopoly (private_control>0.85, public_utility_div>0.80)
  {
    entity_id: "WPE-001", water_system: "municipal_distribution", region: "LATAM",
    private_control_share: 0.92, price_unaffordability: 0.75,
    access_inequality: 0.80, aquifer_depletion_rate: 0.70,
    corporate_extraction: 0.72, public_utility_divestment: 0.88,
    regulatory_capture: 0.78, treaty_compliance: 0.65,
    drought_frequency: 0.68, infrastructure_privatization: 0.82,
    community_rights_erosion: 0.75, indigenous_water_rights: 0.70,
    agricultural_monopoly: 0.68, investment_return_priority: 0.80,
    service_quality_decline: 0.72, tariff_shock_index: 0.70,
    cross_border_tension: 0.65,
  },
  // WPE-002 — critical, affordability_crisis_collapse (price_unafford>0.85, tariff_shock>0.80)
  {
    entity_id: "WPE-002", water_system: "urban_water_utility", region: "SSA",
    private_control_share: 0.72, price_unaffordability: 0.90,
    access_inequality: 0.85, aquifer_depletion_rate: 0.65,
    corporate_extraction: 0.68, public_utility_divestment: 0.70,
    regulatory_capture: 0.75, treaty_compliance: 0.68,
    drought_frequency: 0.72, infrastructure_privatization: 0.70,
    community_rights_erosion: 0.78, indigenous_water_rights: 0.68,
    agricultural_monopoly: 0.65, investment_return_priority: 0.75,
    service_quality_decline: 0.80, tariff_shock_index: 0.85,
    cross_border_tension: 0.60,
  },
  // WPE-003 — critical, aquifer_depletion_emergency (aquifer>0.85, corp_extraction>0.80)
  {
    entity_id: "WPE-003", water_system: "groundwater_basin", region: "MENA",
    private_control_share: 0.70, price_unaffordability: 0.68,
    access_inequality: 0.72, aquifer_depletion_rate: 0.90,
    corporate_extraction: 0.85, public_utility_divestment: 0.65,
    regulatory_capture: 0.72, treaty_compliance: 0.70,
    drought_frequency: 0.78, infrastructure_privatization: 0.68,
    community_rights_erosion: 0.70, indigenous_water_rights: 0.65,
    agricultural_monopoly: 0.72, investment_return_priority: 0.68,
    service_quality_decline: 0.65, tariff_shock_index: 0.62,
    cross_border_tension: 0.70,
  },
  // WPE-004 — high, cross_border_water_conflict (cross_border>0.80, treaty>0.75)
  {
    entity_id: "WPE-004", water_system: "transboundary_river", region: "APAC",
    private_control_share: 0.48, price_unaffordability: 0.50,
    access_inequality: 0.52, aquifer_depletion_rate: 0.50,
    corporate_extraction: 0.48, public_utility_divestment: 0.45,
    regulatory_capture: 0.50, treaty_compliance: 0.80,
    drought_frequency: 0.52, infrastructure_privatization: 0.48,
    community_rights_erosion: 0.50, indigenous_water_rights: 0.52,
    agricultural_monopoly: 0.48, investment_return_priority: 0.50,
    service_quality_decline: 0.45, tariff_shock_index: 0.48,
    cross_border_tension: 0.85,
  },
  // WPE-005 — high, climate_water_scarcity_trap (drought>0.80, agri_mono>0.75)
  {
    entity_id: "WPE-005", water_system: "irrigation_network", region: "NOAM",
    private_control_share: 0.50, price_unaffordability: 0.48,
    access_inequality: 0.50, aquifer_depletion_rate: 0.52,
    corporate_extraction: 0.50, public_utility_divestment: 0.48,
    regulatory_capture: 0.50, treaty_compliance: 0.48,
    drought_frequency: 0.85, infrastructure_privatization: 0.50,
    community_rights_erosion: 0.48, indigenous_water_rights: 0.50,
    agricultural_monopoly: 0.80, investment_return_priority: 0.48,
    service_quality_decline: 0.50, tariff_shock_index: 0.48,
    cross_border_tension: 0.45,
  },
  // WPE-006 — moderate, none
  {
    entity_id: "WPE-006", water_system: "rural_water_cooperative", region: "EMEA",
    private_control_share: 0.30, price_unaffordability: 0.28,
    access_inequality: 0.32, aquifer_depletion_rate: 0.28,
    corporate_extraction: 0.30, public_utility_divestment: 0.28,
    regulatory_capture: 0.30, treaty_compliance: 0.25,
    drought_frequency: 0.28, infrastructure_privatization: 0.30,
    community_rights_erosion: 0.28, indigenous_water_rights: 0.30,
    agricultural_monopoly: 0.28, investment_return_priority: 0.30,
    service_quality_decline: 0.28, tariff_shock_index: 0.25,
    cross_border_tension: 0.28,
  },
  // WPE-007 — low, none
  {
    entity_id: "WPE-007", water_system: "public_utility_network", region: "EMEA",
    private_control_share: 0.10, price_unaffordability: 0.12,
    access_inequality: 0.10, aquifer_depletion_rate: 0.08,
    corporate_extraction: 0.10, public_utility_divestment: 0.08,
    regulatory_capture: 0.10, treaty_compliance: 0.08,
    drought_frequency: 0.10, infrastructure_privatization: 0.12,
    community_rights_erosion: 0.10, indigenous_water_rights: 0.08,
    agricultural_monopoly: 0.10, investment_return_priority: 0.12,
    service_quality_decline: 0.10, tariff_shock_index: 0.08,
    cross_border_tension: 0.10,
  },
  // WPE-008 — low, none
  {
    entity_id: "WPE-008", water_system: "community_water_board", region: "APAC",
    private_control_share: 0.12, price_unaffordability: 0.10,
    access_inequality: 0.12, aquifer_depletion_rate: 0.10,
    corporate_extraction: 0.12, public_utility_divestment: 0.10,
    regulatory_capture: 0.12, treaty_compliance: 0.10,
    drought_frequency: 0.12, infrastructure_privatization: 0.10,
    community_rights_erosion: 0.12, indigenous_water_rights: 0.10,
    agricultural_monopoly: 0.12, investment_return_priority: 0.10,
    service_quality_decline: 0.12, tariff_shock_index: 0.10,
    cross_border_tension: 0.12,
  },
];

type WPEInput = (typeof MOCK_ENTITIES)[0];

function accessScore(e: WPEInput): number {
  return Math.round((e.access_inequality * 0.4 + e.price_unaffordability * 0.35 + e.service_quality_decline * 0.25) * 100 * 100) / 100;
}
function privatizationScore(e: WPEInput): number {
  return Math.round((e.private_control_share * 0.4 + e.infrastructure_privatization * 0.35 + e.public_utility_divestment * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: WPEInput): number {
  return Math.round((e.regulatory_capture * 0.4 + e.community_rights_erosion * 0.35 + e.investment_return_priority * 0.25) * 100 * 100) / 100;
}
function conflictScore(e: WPEInput): number {
  return Math.round((e.cross_border_tension * 0.4 + e.treaty_compliance * 0.35 + e.indigenous_water_rights * 0.25) * 100 * 100) / 100;
}
function compositeScore(acc: number, priv: number, gov: number, con: number): number {
  return Math.round((acc * 0.30 + priv * 0.25 + gov * 0.25 + con * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function waterPattern(e: WPEInput): string {
  if (e.private_control_share > 0.85 && e.public_utility_divestment > 0.80) return "corporate_water_monopoly";
  if (e.price_unaffordability > 0.85 && e.tariff_shock_index > 0.80) return "affordability_crisis_collapse";
  if (e.aquifer_depletion_rate > 0.85 && e.corporate_extraction > 0.80) return "aquifer_depletion_emergency";
  if (e.cross_border_tension > 0.80 && e.treaty_compliance > 0.75) return "cross_border_water_conflict";
  if (e.drought_frequency > 0.80 && e.agricultural_monopoly > 0.75) return "climate_water_scarcity_trap";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_privatisation_eau_systémique";
  if (composite >= 40) return "crise_bien_commun_hydrique_majeure";
  if (composite >= 20) return "inégalité_accès_eau_structurelle";
  return "accès_eau_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_remunicipalisation_eau_critique";
  if (risk === "high") return "régulation_renforcée_tarifs_eau_communautés_vulnérables";
  if (risk === "moderate") return "renforcement_gouvernance_bien_commun_hydrique";
  return "veille_accès_eau_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise privatisation eau systémique — bien commun hydrique en péril";
  if (risk === "high") return "🟠 Crise bien commun hydrique majeure détectée";
  if (risk === "moderate") return "🟡 Inégalité accès eau structurelle active";
  return "🟢 Accès eau sous surveillance";
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const acc  = accessScore(e);
      const priv = privatizationScore(e);
      const gov  = governanceScore(e);
      const con  = conflictScore(e);
      const comp = compositeScore(acc, priv, gov, con);
      const risk = riskLevel(comp);
      const pat  = waterPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        entity_id:              e.entity_id,
        water_system:           e.water_system,
        region:                 e.region,
        access_score:           acc,
        privatization_score:    priv,
        governance_score:       gov,
        conflict_score:         con,
        composite_score:        comp,
        risk_level:             risk,
        water_pattern:          pat,
        severity:               sev,
        recommended_action:     action,
        signal:                 sig,
        private_control_share:  e.private_control_share,
        aquifer_depletion_rate: e.aquifer_depletion_rate,
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
      pattern_distribution[ent.water_pattern]     = (pattern_distribution[ent.water_pattern]     || 0) + 1;
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
      module_id:                          404,
      module_name:                        "Privatisation Eau & Bien Commun Hydrique Intelligence Engine",
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
      avg_estimated_water_commons_index:  Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/water-privatization-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(sealResponse(await res.json()));
  } catch {}
  return NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 });
}
