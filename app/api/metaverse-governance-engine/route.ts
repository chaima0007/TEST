import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[metaverse-governance-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const MOCK_ENTITIES = [
  // MGE-001 — critical, platform_monopoly_capture (concentration>0.85, user_lock_in>0.80)
  {
    id: "MGE-001", platform_type: "social_vr_platform", region: "NOAM",
    platform_concentration: 0.92, user_lock_in: 0.88,
    virtual_labor_rights: 0.70, economic_extraction: 0.72,
    identity_exploitation: 0.68, biometric_harvesting: 0.65,
    addiction_mechanics: 0.72, minor_exposure: 0.68,
    psychological_manipulation: 0.70, interoperability_barrier: 0.82,
    regulatory_gap: 0.65, tax_avoidance: 0.68,
    virtual_crime_rate: 0.60, property_rights_clarity: 0.62,
    content_moderation_failure: 0.70, environmental_footprint: 0.65,
    wealth_inequality_virtual: 0.68,
  },
  // MGE-002 — critical, virtual_labor_exploitation (labor_rights>0.85, extraction>0.80)
  {
    id: "MGE-002", platform_type: "play_to_earn_metaverse", region: "APAC",
    platform_concentration: 0.65, user_lock_in: 0.62,
    virtual_labor_rights: 0.90, economic_extraction: 0.85,
    identity_exploitation: 0.65, biometric_harvesting: 0.60,
    addiction_mechanics: 0.68, minor_exposure: 0.65,
    psychological_manipulation: 0.62, interoperability_barrier: 0.60,
    regulatory_gap: 0.68, tax_avoidance: 0.65,
    virtual_crime_rate: 0.72, property_rights_clarity: 0.58,
    content_moderation_failure: 0.65, environmental_footprint: 0.70,
    wealth_inequality_virtual: 0.75,
  },
  // MGE-003 — critical, identity_data_colonialism (identity>0.85, biometric>0.80)
  {
    id: "MGE-003", platform_type: "immersive_commerce_world", region: "EMEA",
    platform_concentration: 0.68, user_lock_in: 0.65,
    virtual_labor_rights: 0.60, economic_extraction: 0.62,
    identity_exploitation: 0.90, biometric_harvesting: 0.85,
    addiction_mechanics: 0.65, minor_exposure: 0.62,
    psychological_manipulation: 0.68, interoperability_barrier: 0.65,
    regulatory_gap: 0.70, tax_avoidance: 0.68,
    virtual_crime_rate: 0.58, property_rights_clarity: 0.55,
    content_moderation_failure: 0.60, environmental_footprint: 0.62,
    wealth_inequality_virtual: 0.65,
  },
  // MGE-004 — high, addiction_by_design_crisis (addiction>0.85, minor_exposure>0.80)
  {
    id: "MGE-004", platform_type: "gaming_metaverse", region: "APAC",
    platform_concentration: 0.48, user_lock_in: 0.52,
    virtual_labor_rights: 0.45, economic_extraction: 0.50,
    identity_exploitation: 0.48, biometric_harvesting: 0.45,
    addiction_mechanics: 0.88, minor_exposure: 0.83,
    psychological_manipulation: 0.52, interoperability_barrier: 0.48,
    regulatory_gap: 0.50, tax_avoidance: 0.45,
    virtual_crime_rate: 0.48, property_rights_clarity: 0.52,
    content_moderation_failure: 0.55, environmental_footprint: 0.48,
    wealth_inequality_virtual: 0.50,
  },
  // MGE-005 — high, regulatory_jurisdiction_vacuum (reg_gap>0.80, tax_avoid>0.75)
  {
    id: "MGE-005", platform_type: "decentralized_virtual_world", region: "LATAM",
    platform_concentration: 0.45, user_lock_in: 0.48,
    virtual_labor_rights: 0.50, economic_extraction: 0.45,
    identity_exploitation: 0.48, biometric_harvesting: 0.45,
    addiction_mechanics: 0.50, minor_exposure: 0.48,
    psychological_manipulation: 0.45, interoperability_barrier: 0.50,
    regulatory_gap: 0.85, tax_avoidance: 0.80,
    virtual_crime_rate: 0.52, property_rights_clarity: 0.45,
    content_moderation_failure: 0.50, environmental_footprint: 0.48,
    wealth_inequality_virtual: 0.50,
  },
  // MGE-006 — moderate, none
  {
    id: "MGE-006", platform_type: "enterprise_virtual_office", region: "EMEA",
    platform_concentration: 0.30, user_lock_in: 0.28,
    virtual_labor_rights: 0.32, economic_extraction: 0.28,
    identity_exploitation: 0.30, biometric_harvesting: 0.28,
    addiction_mechanics: 0.25, minor_exposure: 0.22,
    psychological_manipulation: 0.28, interoperability_barrier: 0.30,
    regulatory_gap: 0.28, tax_avoidance: 0.25,
    virtual_crime_rate: 0.22, property_rights_clarity: 0.30,
    content_moderation_failure: 0.28, environmental_footprint: 0.30,
    wealth_inequality_virtual: 0.28,
  },
  // MGE-007 — low, none
  {
    id: "MGE-007", platform_type: "educational_metaverse", region: "NOAM",
    platform_concentration: 0.10, user_lock_in: 0.12,
    virtual_labor_rights: 0.08, economic_extraction: 0.10,
    identity_exploitation: 0.10, biometric_harvesting: 0.08,
    addiction_mechanics: 0.10, minor_exposure: 0.12,
    psychological_manipulation: 0.08, interoperability_barrier: 0.10,
    regulatory_gap: 0.12, tax_avoidance: 0.08,
    virtual_crime_rate: 0.10, property_rights_clarity: 0.12,
    content_moderation_failure: 0.10, environmental_footprint: 0.08,
    wealth_inequality_virtual: 0.10,
  },
  // MGE-008 — low, none
  {
    id: "MGE-008", platform_type: "open_source_virtual_commons", region: "SSA",
    platform_concentration: 0.08, user_lock_in: 0.10,
    virtual_labor_rights: 0.10, economic_extraction: 0.08,
    identity_exploitation: 0.08, biometric_harvesting: 0.10,
    addiction_mechanics: 0.08, minor_exposure: 0.10,
    psychological_manipulation: 0.10, interoperability_barrier: 0.08,
    regulatory_gap: 0.10, tax_avoidance: 0.08,
    virtual_crime_rate: 0.08, property_rights_clarity: 0.10,
    content_moderation_failure: 0.08, environmental_footprint: 0.10,
    wealth_inequality_virtual: 0.08,
  },
];

type MGEInput = typeof MOCK_ENTITIES[0];

function monopolyScore(e: MGEInput): number {
  return Math.round((e.platform_concentration * 0.40 + e.user_lock_in * 0.35 + e.interoperability_barrier * 0.25) * 100 * 100) / 100;
}
function exploitationScore(e: MGEInput): number {
  return Math.round((e.virtual_labor_rights * 0.40 + e.economic_extraction * 0.35 + e.wealth_inequality_virtual * 0.25) * 100 * 100) / 100;
}
function identityScore(e: MGEInput): number {
  return Math.round((e.identity_exploitation * 0.40 + e.biometric_harvesting * 0.35 + e.tax_avoidance * 0.25) * 100 * 100) / 100;
}
function addictionScore(e: MGEInput): number {
  return Math.round((e.addiction_mechanics * 0.40 + e.minor_exposure * 0.35 + e.psychological_manipulation * 0.25) * 100 * 100) / 100;
}
function compositeScore(mon: number, exp: number, ide: number, add: number): number {
  return Math.round((mon * 0.30 + exp * 0.25 + ide * 0.25 + add * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function metaversePattern(e: MGEInput): string {
  if (e.platform_concentration > 0.85 && e.user_lock_in > 0.80) return "platform_monopoly_capture";
  if (e.virtual_labor_rights > 0.85 && e.economic_extraction > 0.80) return "virtual_labor_exploitation";
  if (e.identity_exploitation > 0.85 && e.biometric_harvesting > 0.80) return "identity_data_colonialism";
  if (e.addiction_mechanics > 0.85 && e.minor_exposure > 0.80) return "addiction_by_design_crisis";
  if (e.regulatory_gap > 0.80 && e.tax_avoidance > 0.75) return "regulatory_jurisdiction_vacuum";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_gouvernance_métavers_systémique";
  if (composite >= 40) return "crise_économie_virtuelle_majeure";
  if (composite >= 20) return "déséquilibre_pouvoir_numérique_structurel";
  return "surveillance_métavers_active";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_régulation_métavers_critique";
  if (risk === "high") return "réforme_accélérée_économie_virtuelle_exploitée";
  if (risk === "moderate") return "renforcement_gouvernance_numérique_mondiale";
  return "veille_métavers_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise gouvernance métavers systémique — souveraineté numérique en péril";
  if (risk === "high") return "🟠 Crise économie virtuelle majeure détectée";
  if (risk === "moderate") return "🟡 Déséquilibre pouvoir numérique structurel actif";
  return "🟢 Métavers sous surveillance active";
}

const SWARM_API_URL = process.env.SWARM_API_URL;

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const mon  = monopolyScore(e);
      const exp  = exploitationScore(e);
      const ide  = identityScore(e);
      const add  = addictionScore(e);
      const comp = compositeScore(mon, exp, ide, add);
      const risk = riskLevel(comp);
      const pat  = metaversePattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:               e.entity_id,
        platform_type:           e.platform_type,
        region:                  e.region,
        monopoly_score:          mon,
        exploitation_score:      exp,
        identity_score:          ide,
        addiction_score:         add,
        composite_score:         comp,
        risk_level:              risk,
        metaverse_pattern:       pat,
        severity:                sev,
        recommended_action:      action,
        signal:                  sig,
        platform_concentration:  e.platform_concentration,
        regulatory_gap:          e.regulatory_gap,
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
      pattern_distribution[ent.metaverse_pattern] = (pattern_distribution[ent.metaverse_pattern] || 0) + 1;
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
      module_id:                                400,
      module_name:                              "Gouvernance Métavers & Économie Monde Virtuel Intelligence Engine",
      total:                                    n,
      critical:                                 criticalCount,
      high:                                     highCount,
      moderate:                                 moderateCount,
      low:                                      lowCount,
      avg_composite:                            avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_metaverse_governance_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>)));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/metaverse-governance-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(sealResponse(await res.json())));
  } catch {}
  return sealResponse(NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 }));
}
