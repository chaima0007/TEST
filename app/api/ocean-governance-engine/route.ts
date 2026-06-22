import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // OGE-001 — critical, high_seas_jurisdiction_vacuum (jurisdictional_gap>0.85, flag_state>0.80)
  {
    id: "OGE-001", ocean_zone: "haute_mer", region: "Atlantique Nord",
    jurisdictional_gap: 0.92, flag_state_compliance: 0.85,
    illegal_fishing_intensity: 0.72, treaty_ratification_rate: 0.68,
    marine_protected_coverage: 0.70, biodiversity_loss_rate: 0.72,
    enforcement_capacity: 0.68, satellite_monitoring: 0.65,
    high_seas_treaty_implementation: 0.70, deep_sea_mining_governance: 0.65,
    military_use_regulation: 0.68, pollution_accountability: 0.62,
    equity_of_access: 0.70, benefit_sharing_mechanism: 0.65,
    climate_adaptation_integration: 0.68, indigenous_maritime_rights: 0.62,
    corporate_accountability: 0.65,
  },
  // OGE-002 — critical, illeagal_fishing_impunity (illegal_fishing>0.85, enforcement>0.80)
  {
    id: "OGE-002", ocean_zone: "zone_économique_exclusive", region: "Pacifique Ouest",
    jurisdictional_gap: 0.68, flag_state_compliance: 0.65,
    illegal_fishing_intensity: 0.90, treaty_ratification_rate: 0.65,
    marine_protected_coverage: 0.62, biodiversity_loss_rate: 0.68,
    enforcement_capacity: 0.85, satellite_monitoring: 0.70,
    high_seas_treaty_implementation: 0.65, deep_sea_mining_governance: 0.62,
    military_use_regulation: 0.65, pollution_accountability: 0.60,
    equity_of_access: 0.65, benefit_sharing_mechanism: 0.62,
    climate_adaptation_integration: 0.65, indigenous_maritime_rights: 0.60,
    corporate_accountability: 0.62,
  },
  // OGE-003 — critical, biodiversity_treaty_collapse (biodiversity_loss>0.85, treaty_rat>0.80)
  {
    id: "OGE-003", ocean_zone: "mer_territoriale", region: "Océan Indien",
    jurisdictional_gap: 0.70, flag_state_compliance: 0.68,
    illegal_fishing_intensity: 0.65, treaty_ratification_rate: 0.82,
    marine_protected_coverage: 0.65, biodiversity_loss_rate: 0.88,
    enforcement_capacity: 0.70, satellite_monitoring: 0.65,
    high_seas_treaty_implementation: 0.68, deep_sea_mining_governance: 0.62,
    military_use_regulation: 0.60, pollution_accountability: 0.65,
    equity_of_access: 0.68, benefit_sharing_mechanism: 0.62,
    climate_adaptation_integration: 0.65, indigenous_maritime_rights: 0.60,
    corporate_accountability: 0.62,
  },
  // OGE-004 — high, deep_sea_resource_capture (deep_sea_mining>0.80, corporate_accountability>0.75)
  {
    id: "OGE-004", ocean_zone: "fond_marin_international", region: "Arctique",
    jurisdictional_gap: 0.48, flag_state_compliance: 0.45,
    illegal_fishing_intensity: 0.50, treaty_ratification_rate: 0.48,
    marine_protected_coverage: 0.50, biodiversity_loss_rate: 0.52,
    enforcement_capacity: 0.48, satellite_monitoring: 0.50,
    high_seas_treaty_implementation: 0.48, deep_sea_mining_governance: 0.85,
    military_use_regulation: 0.48, pollution_accountability: 0.50,
    equity_of_access: 0.48, benefit_sharing_mechanism: 0.50,
    climate_adaptation_integration: 0.48, indigenous_maritime_rights: 0.45,
    corporate_accountability: 0.80,
  },
  // OGE-005 — high, marine_protected_area_failure (marine_prot>0.80, biodiversity>0.75)
  {
    id: "OGE-005", ocean_zone: "zone_protégée_marine", region: "Méditerranée",
    jurisdictional_gap: 0.45, flag_state_compliance: 0.48,
    illegal_fishing_intensity: 0.50, treaty_ratification_rate: 0.48,
    marine_protected_coverage: 0.85, biodiversity_loss_rate: 0.80,
    enforcement_capacity: 0.48, satellite_monitoring: 0.45,
    high_seas_treaty_implementation: 0.48, deep_sea_mining_governance: 0.45,
    military_use_regulation: 0.48, pollution_accountability: 0.50,
    equity_of_access: 0.48, benefit_sharing_mechanism: 0.45,
    climate_adaptation_integration: 0.48, indigenous_maritime_rights: 0.45,
    corporate_accountability: 0.48,
  },
  // OGE-006 — moderate, none
  {
    id: "OGE-006", ocean_zone: "plateau_continental", region: "Atlantique Sud",
    jurisdictional_gap: 0.30, flag_state_compliance: 0.28,
    illegal_fishing_intensity: 0.32, treaty_ratification_rate: 0.28,
    marine_protected_coverage: 0.30, biodiversity_loss_rate: 0.32,
    enforcement_capacity: 0.28, satellite_monitoring: 0.30,
    high_seas_treaty_implementation: 0.28, deep_sea_mining_governance: 0.30,
    military_use_regulation: 0.28, pollution_accountability: 0.30,
    equity_of_access: 0.28, benefit_sharing_mechanism: 0.30,
    climate_adaptation_integration: 0.28, indigenous_maritime_rights: 0.25,
    corporate_accountability: 0.28,
  },
  // OGE-007 — low, none
  {
    id: "OGE-007", ocean_zone: "mer_intérieure", region: "Europe Nord",
    jurisdictional_gap: 0.10, flag_state_compliance: 0.12,
    illegal_fishing_intensity: 0.10, treaty_ratification_rate: 0.12,
    marine_protected_coverage: 0.10, biodiversity_loss_rate: 0.12,
    enforcement_capacity: 0.10, satellite_monitoring: 0.08,
    high_seas_treaty_implementation: 0.10, deep_sea_mining_governance: 0.12,
    military_use_regulation: 0.10, pollution_accountability: 0.10,
    equity_of_access: 0.12, benefit_sharing_mechanism: 0.10,
    climate_adaptation_integration: 0.12, indigenous_maritime_rights: 0.08,
    corporate_accountability: 0.10,
  },
  // OGE-008 — low, none
  {
    id: "OGE-008", ocean_zone: "détroit_international", region: "Asie Pacifique",
    jurisdictional_gap: 0.12, flag_state_compliance: 0.10,
    illegal_fishing_intensity: 0.12, treaty_ratification_rate: 0.10,
    marine_protected_coverage: 0.12, biodiversity_loss_rate: 0.10,
    enforcement_capacity: 0.12, satellite_monitoring: 0.10,
    high_seas_treaty_implementation: 0.12, deep_sea_mining_governance: 0.10,
    military_use_regulation: 0.12, pollution_accountability: 0.10,
    equity_of_access: 0.10, benefit_sharing_mechanism: 0.12,
    climate_adaptation_integration: 0.10, indigenous_maritime_rights: 0.10,
    corporate_accountability: 0.12,
  },
];

type OGEInput = (typeof MOCK_ENTITIES)[0];

function jurisdictionScore(e: OGEInput): number {
  return Math.round((e.jurisdictional_gap * 0.4 + e.flag_state_compliance * 0.35 + e.illegal_fishing_intensity * 0.25) * 100 * 100) / 100;
}
function conservationScore(e: OGEInput): number {
  return Math.round((e.biodiversity_loss_rate * 0.4 + e.marine_protected_coverage * 0.35 + e.treaty_ratification_rate * 0.25) * 100 * 100) / 100;
}
function enforcementScore(e: OGEInput): number {
  return Math.round((e.enforcement_capacity * 0.4 + e.satellite_monitoring * 0.35 + e.high_seas_treaty_implementation * 0.25) * 100 * 100) / 100;
}
function equityScore(e: OGEInput): number {
  return Math.round((e.equity_of_access * 0.4 + e.benefit_sharing_mechanism * 0.35 + e.indigenous_maritime_rights * 0.25) * 100 * 100) / 100;
}
function compositeScore(jur: number, con: number, enf: number, eq: number): number {
  return Math.round((jur * 0.30 + con * 0.25 + enf * 0.25 + eq * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function oceanPattern(e: OGEInput): string {
  if (e.jurisdictional_gap > 0.85 && e.flag_state_compliance > 0.80) return "high_seas_jurisdiction_vacuum";
  if (e.illegal_fishing_intensity > 0.85 && e.enforcement_capacity > 0.80) return "illeagal_fishing_impunity";
  if (e.biodiversity_loss_rate > 0.85 && e.treaty_ratification_rate > 0.80) return "biodiversity_treaty_collapse";
  if (e.deep_sea_mining_governance > 0.80 && e.corporate_accountability > 0.75) return "deep_sea_resource_capture";
  if (e.marine_protected_coverage > 0.80 && e.biodiversity_loss_rate > 0.75) return "marine_protected_area_failure";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_gouvernance_océanique_systémique";
  if (composite >= 40) return "crise_haute_mer_majeure";
  if (composite >= 20) return "déficit_gouvernance_maritime_structurel";
  return "gouvernance_océanique_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_traité_haute_mer_critique";
  if (risk === "high") return "renforcement_accéléré_juridiction_maritime";
  if (risk === "moderate") return "consolidation_politiques_conservation_marine";
  return "veille_gouvernance_océanique_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise gouvernance océanique systémique — traité haute mer en péril";
  if (risk === "high") return "🟠 Crise haute mer majeure détectée";
  if (risk === "moderate") return "🟡 Déficit gouvernance maritime structurel actif";
  return "🟢 Gouvernance océanique sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[ocean-governance-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tJur = 0, tCon = 0, tEnf = 0, tEq = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.ocean_pattern]     = (pattern_distribution[ent.ocean_pattern]     || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tJur  += ent.jurisdiction_score;
      tCon  += ent.conservation_score;
      tEnf  += ent.enforcement_score;
      tEq   += ent.equity_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite    = Math.round(tComp / n * 10) / 10;
    const avgJurisdiction = Math.round(tJur  / n * 10) / 10;

    const summary = {
      module_id:                              420,
      module_name:                            "Gouvernance Océans & Traité Haute Mer Intelligence Engine",
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
      avg_estimated_ocean_governance_index:   Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary, avg_jurisdiction: avgJurisdiction }, "ocean-governance-engine")
    ));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/ocean-governance-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return sealResponse(NextResponse.json(sealResponse(await upstream.json(), "ocean-governance-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "ocean-governance-engine"),
      { status: 502 }
    ));
  }
}
