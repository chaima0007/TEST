import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // DDG-001: critical, algorithmic_autocracy (algorithmic_bias>=0.70 AND AI_policy>=0.65, comp≈72)
  { id:"DDG-001", governance_domain:"automated_decision_system", region:"EMEA",
    algorithmic_bias_in_governance:0.85, digital_exclusion_index:0.75, surveillance_democracy_ratio:0.65,
    platform_political_capture:0.60, misinformation_amplification_rate:0.70, citizen_digital_participation:0.30,
    e_voting_integrity_risk:0.60, algorithmic_accountability_gap:0.78, open_data_governance_level:0.25,
    regulatory_tech_capture:0.70, digital_rights_erosion_index:0.72, AI_policy_decision_autonomy:0.80,
    cross_platform_polarization:0.68, electoral_manipulation_risk:0.65, civic_tech_adoption:0.25,
    democratic_AI_oversight:0.20, digital_identity_sovereignty_risk:0.70 },

  // DDG-002: low, no pattern (comp≈11)
  { id:"DDG-002", governance_domain:"civic_digital_services", region:"NAMER",
    algorithmic_bias_in_governance:0.12, digital_exclusion_index:0.10, surveillance_democracy_ratio:0.12,
    platform_political_capture:0.15, misinformation_amplification_rate:0.12, citizen_digital_participation:0.85,
    e_voting_integrity_risk:0.10, algorithmic_accountability_gap:0.10, open_data_governance_level:0.88,
    regulatory_tech_capture:0.12, digital_rights_erosion_index:0.08, AI_policy_decision_autonomy:0.15,
    cross_platform_polarization:0.15, electoral_manipulation_risk:0.10, civic_tech_adoption:0.82,
    democratic_AI_oversight:0.90, digital_identity_sovereignty_risk:0.10 },

  // DDG-003: high, electoral_subversion (electoral_manipulation_risk>=0.70 AND misinformation>=0.65, comp≈52)
  { id:"DDG-003", governance_domain:"electoral_infrastructure", region:"LATAM",
    algorithmic_bias_in_governance:0.50, digital_exclusion_index:0.40, surveillance_democracy_ratio:0.40,
    platform_political_capture:0.55, misinformation_amplification_rate:0.75, citizen_digital_participation:0.55,
    e_voting_integrity_risk:0.55, algorithmic_accountability_gap:0.50, open_data_governance_level:0.50,
    regulatory_tech_capture:0.48, digital_rights_erosion_index:0.42, AI_policy_decision_autonomy:0.45,
    cross_platform_polarization:0.50, electoral_manipulation_risk:0.78, civic_tech_adoption:0.50,
    democratic_AI_oversight:0.45, digital_identity_sovereignty_risk:0.45 },

  // DDG-004: low, no pattern (comp≈13)
  { id:"DDG-004", governance_domain:"open_government_platform", region:"APAC",
    algorithmic_bias_in_governance:0.15, digital_exclusion_index:0.12, surveillance_democracy_ratio:0.15,
    platform_political_capture:0.10, misinformation_amplification_rate:0.15, citizen_digital_participation:0.88,
    e_voting_integrity_risk:0.12, algorithmic_accountability_gap:0.15, open_data_governance_level:0.85,
    regulatory_tech_capture:0.10, digital_rights_erosion_index:0.10, AI_policy_decision_autonomy:0.12,
    cross_platform_polarization:0.12, electoral_manipulation_risk:0.12, civic_tech_adoption:0.80,
    democratic_AI_oversight:0.88, digital_identity_sovereignty_risk:0.12 },

  // DDG-005: critical, surveillance_democracy (surveillance_ratio>=0.70 AND digital_rights_erosion>=0.65, comp≈68)
  { id:"DDG-005", governance_domain:"state_surveillance_system", region:"MEA",
    algorithmic_bias_in_governance:0.65, digital_exclusion_index:0.65, surveillance_democracy_ratio:0.82,
    platform_political_capture:0.58, misinformation_amplification_rate:0.68, citizen_digital_participation:0.30,
    e_voting_integrity_risk:0.65, algorithmic_accountability_gap:0.72, open_data_governance_level:0.20,
    regulatory_tech_capture:0.65, digital_rights_erosion_index:0.78, AI_policy_decision_autonomy:0.60,
    cross_platform_polarization:0.70, electoral_manipulation_risk:0.60, civic_tech_adoption:0.22,
    democratic_AI_oversight:0.18, digital_identity_sovereignty_risk:0.80 },

  // DDG-006: moderate, no pattern (comp≈32)
  { id:"DDG-006", governance_domain:"digital_public_services", region:"EMEA",
    algorithmic_bias_in_governance:0.35, digital_exclusion_index:0.32, surveillance_democracy_ratio:0.35,
    platform_political_capture:0.28, misinformation_amplification_rate:0.35, citizen_digital_participation:0.65,
    e_voting_integrity_risk:0.30, algorithmic_accountability_gap:0.35, open_data_governance_level:0.60,
    regulatory_tech_capture:0.30, digital_rights_erosion_index:0.28, AI_policy_decision_autonomy:0.30,
    cross_platform_polarization:0.30, electoral_manipulation_risk:0.30, civic_tech_adoption:0.62,
    democratic_AI_oversight:0.65, digital_identity_sovereignty_risk:0.32 },

  // DDG-007: high, digital_disenfranchisement (digital_exclusion>=0.70 AND citizen_participation<=0.35, comp≈54)
  { id:"DDG-007", governance_domain:"rural_digital_governance", region:"SSA",
    algorithmic_bias_in_governance:0.55, digital_exclusion_index:0.78, surveillance_democracy_ratio:0.45,
    platform_political_capture:0.45, misinformation_amplification_rate:0.50, citizen_digital_participation:0.28,
    e_voting_integrity_risk:0.45, algorithmic_accountability_gap:0.55, open_data_governance_level:0.40,
    regulatory_tech_capture:0.50, digital_rights_erosion_index:0.52, AI_policy_decision_autonomy:0.50,
    cross_platform_polarization:0.52, electoral_manipulation_risk:0.48, civic_tech_adoption:0.38,
    democratic_AI_oversight:0.35, digital_identity_sovereignty_risk:0.48 },

  // DDG-008: critical, platform_sovereignty_capture (platform_capture>=0.70 AND regulatory_capture>=0.65, comp≈67)
  { id:"DDG-008", governance_domain:"platform_regulated_media", region:"NOAM",
    algorithmic_bias_in_governance:0.68, digital_exclusion_index:0.65, surveillance_democracy_ratio:0.62,
    platform_political_capture:0.82, misinformation_amplification_rate:0.65, citizen_digital_participation:0.30,
    e_voting_integrity_risk:0.62, algorithmic_accountability_gap:0.75, open_data_governance_level:0.22,
    regulatory_tech_capture:0.78, digital_rights_erosion_index:0.62, AI_policy_decision_autonomy:0.60,
    cross_platform_polarization:0.65, electoral_manipulation_risk:0.60, civic_tech_adoption:0.25,
    democratic_AI_oversight:0.20, digital_identity_sovereignty_risk:0.68 },
];

type Entity = typeof MOCK_ENTITIES[0];

function exclusionScore(e: Entity): number {
  const raw = (
    e.digital_exclusion_index * 0.40
    + e.algorithmic_bias_in_governance * 0.35
    + e.digital_rights_erosion_index * 0.25
  ) * 100;
  return Math.min(Math.round(raw * 100) / 100, 100);
}

function manipulationScore(e: Entity): number {
  const raw = (
    e.misinformation_amplification_rate * 0.40
    + e.electoral_manipulation_risk * 0.35
    + e.platform_political_capture * 0.25
  ) * 100;
  return Math.min(Math.round(raw * 100) / 100, 100);
}

function accountabilityScore(e: Entity): number {
  const raw = (
    e.algorithmic_accountability_gap * 0.40
    + e.AI_policy_decision_autonomy * 0.35
    + e.regulatory_tech_capture * 0.25
  ) * 100;
  return Math.min(Math.round(raw * 100) / 100, 100);
}

function sovereigntyScore(e: Entity): number {
  const raw = (
    e.digital_identity_sovereignty_risk * 0.40
    + e.surveillance_democracy_ratio * 0.35
    + e.cross_platform_polarization * 0.25
  ) * 100;
  return Math.min(Math.round(raw * 100) / 100, 100);
}

function compositeScore(excl: number, manip: number, acct: number, sov: number): number {
  return Math.min(Math.round((excl * 0.30 + manip * 0.25 + acct * 0.25 + sov * 0.20) * 100) / 100, 100);
}

function democracyPattern(e: Entity): string {
  if (e.algorithmic_bias_in_governance >= 0.70 && e.AI_policy_decision_autonomy >= 0.65) return "algorithmic_autocracy";
  if (e.digital_exclusion_index >= 0.70 && e.citizen_digital_participation <= 0.35)       return "digital_disenfranchisement";
  if (e.electoral_manipulation_risk >= 0.70 && e.misinformation_amplification_rate >= 0.65) return "electoral_subversion";
  if (e.surveillance_democracy_ratio >= 0.70 && e.digital_rights_erosion_index >= 0.65)   return "surveillance_democracy";
  if (e.platform_political_capture >= 0.70 && e.regulatory_tech_capture >= 0.65)          return "platform_sovereignty_capture";
  return "none";
}

function riskLevel(c: number): string {
  if (c >= 60) return "critical";
  if (c >= 40) return "high";
  if (c >= 20) return "moderate";
  return "low";
}

function severity(risk: string): string {
  if (risk === "critical") return "démocratie_numérique_compromise";
  if (risk === "high")     return "risque_démocratique_élevé";
  if (risk === "moderate") return "fragilité_gouvernance";
  return "gouvernance_stable";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_démocratique_urgente";
  if (risk === "high")     return "réforme_gouvernance_algorithmique";
  if (risk === "moderate") return "renforcement_oversight_numérique";
  return "surveillance_continue";
}

function democracySignal(risk: string): string {
  if (risk === "critical") return "🔴 Démocratie numérique en péril — intervention urgente";
  if (risk === "high")     return "🟠 Risques algorithmiques majeurs détectés";
  if (risk === "moderate") return "🟡 Fragilités gouvernance numérique";
  return "🟢 Gouvernance démocratique numérique stable";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[digital-democracy-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const patternDist: Record<string,number>  = {};
    const riskDist: Record<string,number>     = {};
    const severityDist: Record<string,number> = {};
    const actionDist: Record<string,number>   = {};
    let tComp = 0, tExcl = 0;
    let criticalC = 0, highC = 0, moderateC = 0, lowC = 0;

    for (const ent of entities) {
      patternDist[ent.democracy_pattern]  = (patternDist[ent.democracy_pattern]  || 0) + 1;
      riskDist[ent.risk_level]            = (riskDist[ent.risk_level]            || 0) + 1;
      severityDist[ent.severity]          = (severityDist[ent.severity]          || 0) + 1;
      actionDist[ent.recommended_action]  = (actionDist[ent.recommended_action]  || 0) + 1;
      tComp += ent.composite_score;
      tExcl += ent.exclusion_score;
      if (ent.risk_level === "critical")   criticalC++;
      else if (ent.risk_level === "high")  highC++;
      else if (ent.risk_level === "moderate") moderateC++;
      else                                 lowC++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 10) / 10;
    const summary = {
      module_id:                          330,
      module_name:                        "Digital Democracy & Algorithmic Governance Intelligence Engine",
      total_entities:                     n,
      critical_count:                     criticalC,
      high_count:                         highC,
      moderate_count:                     moderateC,
      low_count:                          lowC,
      avg_composite:                      avgComp,
      pattern_distribution:               patternDist,
      risk_distribution:                  riskDist,
      severity_distribution:              severityDist,
      action_distribution:                actionDist,
      avg_estimated_democracy_risk_index: Math.round(avgComp / 100 * 10 * 100) / 100,
      avg_exclusion_score:                Math.round(tExcl / n * 10) / 10,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>, "digital-democracy-engine")));
  }

  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digital-democracy-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    return sealResponse(NextResponse.json(sealResponse(await res.json() as Record<string, unknown>, "digital-democracy-engine")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse({ error: "upstream unavailable" } as Record<string, unknown>, "digital-democracy-engine"), { status: 502 }));
  }
}
