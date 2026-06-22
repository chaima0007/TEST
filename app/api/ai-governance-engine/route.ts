import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[ai-governance-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── Mock entities ──────────────────────────────────────────────────────────────
// Module 360 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// 8 entities covering all 5 AI governance patterns and all 4 risk levels.

const MOCK_ENTITIES = [
  // AGE-001 — EMEA, national_AI_regulation → critical, governance_vacuum_crisis
  // AI_regulatory_fragmentation_index>=0.70 AND AI_deployment_speed_vs_governance_gap>=0.65 → governance_vacuum_crisis
  // composite≥60 → critical
  {
    id: "AGE-001", governance_context: "national_AI_regulation", region: "EMEA",
    AI_regulatory_fragmentation_index: 0.80,
    AI_safety_standard_gap: 0.75,
    autonomous_system_accountability_vacuum: 0.72,
    AI_liability_unclarity_risk: 0.68,
    algorithmic_auditing_deficit: 0.65,
    AI_international_cooperation_failure: 0.70,
    AI_compute_governance_gap: 0.65,
    AI_training_data_governance_risk: 0.60,
    AI_deployment_speed_vs_governance_gap: 0.78,
    existential_risk_regulatory_blindspot: 0.65,
    AI_market_concentration_regulatory_gap: 0.62,
    democratic_AI_oversight_weakness: 0.68,
    AI_whistleblower_protection_gap: 0.58,
    AI_incident_reporting_deficit: 0.55,
    regulatory_capture_by_AI_industry: 0.62,
    AI_rights_legal_framework_absence: 0.50,
    AI_geopolitical_standards_war: 0.58,
  },
  // AGE-002 — APAC, supranational_governance → low, none
  // All values low → composite<20, no pattern triggered
  {
    id: "AGE-002", governance_context: "supranational_governance", region: "APAC",
    AI_regulatory_fragmentation_index: 0.10,
    AI_safety_standard_gap: 0.12,
    autonomous_system_accountability_vacuum: 0.10,
    AI_liability_unclarity_risk: 0.12,
    algorithmic_auditing_deficit: 0.08,
    AI_international_cooperation_failure: 0.12,
    AI_compute_governance_gap: 0.10,
    AI_training_data_governance_risk: 0.12,
    AI_deployment_speed_vs_governance_gap: 0.15,
    existential_risk_regulatory_blindspot: 0.10,
    AI_market_concentration_regulatory_gap: 0.12,
    democratic_AI_oversight_weakness: 0.10,
    AI_whistleblower_protection_gap: 0.10,
    AI_incident_reporting_deficit: 0.08,
    regulatory_capture_by_AI_industry: 0.08,
    AI_rights_legal_framework_absence: 0.10,
    AI_geopolitical_standards_war: 0.10,
  },
  // AGE-003 — NOAM, accountability_framework → high, accountability_collapse
  // autonomous_system_accountability_vacuum>=0.70 AND AI_liability_unclarity_risk>=0.65 → accountability_collapse
  // reg_frag=0.55<0.70 → avoids governance_vacuum_crisis
  // composite in [40,60) → high
  {
    id: "AGE-003", governance_context: "accountability_framework", region: "NOAM",
    AI_regulatory_fragmentation_index: 0.55,
    AI_safety_standard_gap: 0.50,
    autonomous_system_accountability_vacuum: 0.78,
    AI_liability_unclarity_risk: 0.72,
    algorithmic_auditing_deficit: 0.60,
    AI_international_cooperation_failure: 0.48,
    AI_compute_governance_gap: 0.45,
    AI_training_data_governance_risk: 0.50,
    AI_deployment_speed_vs_governance_gap: 0.52,
    existential_risk_regulatory_blindspot: 0.48,
    AI_market_concentration_regulatory_gap: 0.45,
    democratic_AI_oversight_weakness: 0.50,
    AI_whistleblower_protection_gap: 0.42,
    AI_incident_reporting_deficit: 0.40,
    regulatory_capture_by_AI_industry: 0.42,
    AI_rights_legal_framework_absence: 0.38,
    AI_geopolitical_standards_war: 0.40,
  },
  // AGE-004 — LATAM, democratic_oversight → low, none
  // All values very low → composite<20, no pattern triggered
  {
    id: "AGE-004", governance_context: "democratic_oversight", region: "LATAM",
    AI_regulatory_fragmentation_index: 0.08,
    AI_safety_standard_gap: 0.10,
    autonomous_system_accountability_vacuum: 0.08,
    AI_liability_unclarity_risk: 0.10,
    algorithmic_auditing_deficit: 0.08,
    AI_international_cooperation_failure: 0.10,
    AI_compute_governance_gap: 0.08,
    AI_training_data_governance_risk: 0.10,
    AI_deployment_speed_vs_governance_gap: 0.12,
    existential_risk_regulatory_blindspot: 0.08,
    AI_market_concentration_regulatory_gap: 0.10,
    democratic_AI_oversight_weakness: 0.08,
    AI_whistleblower_protection_gap: 0.08,
    AI_incident_reporting_deficit: 0.10,
    regulatory_capture_by_AI_industry: 0.10,
    AI_rights_legal_framework_absence: 0.08,
    AI_geopolitical_standards_war: 0.08,
  },
  // AGE-005 — MEA, industry_capture_risk → critical, AI_regulatory_capture
  // regulatory_capture_by_AI_industry>=0.70 AND democratic_AI_oversight_weakness>=0.65 → AI_regulatory_capture
  // reg_frag=0.75 but deploy_speed=0.55<0.65 → avoids governance_vacuum_crisis
  // acc_vac=0.62<0.70 → avoids accountability_collapse
  // composite≥60 → critical
  {
    id: "AGE-005", governance_context: "industry_capture_risk", region: "MEA",
    AI_regulatory_fragmentation_index: 0.75,
    AI_safety_standard_gap: 0.70,
    autonomous_system_accountability_vacuum: 0.62,
    AI_liability_unclarity_risk: 0.58,
    algorithmic_auditing_deficit: 0.65,
    AI_international_cooperation_failure: 0.72,
    AI_compute_governance_gap: 0.68,
    AI_training_data_governance_risk: 0.65,
    AI_deployment_speed_vs_governance_gap: 0.55,
    existential_risk_regulatory_blindspot: 0.68,
    AI_market_concentration_regulatory_gap: 0.65,
    democratic_AI_oversight_weakness: 0.78,
    AI_whistleblower_protection_gap: 0.62,
    AI_incident_reporting_deficit: 0.60,
    regulatory_capture_by_AI_industry: 0.82,
    AI_rights_legal_framework_absence: 0.58,
    AI_geopolitical_standards_war: 0.60,
  },
  // AGE-006 — EMEA, standards_development → moderate, none
  // All values moderate → composite in [20,40), no pattern triggered
  {
    id: "AGE-006", governance_context: "standards_development", region: "EMEA",
    AI_regulatory_fragmentation_index: 0.35,
    AI_safety_standard_gap: 0.32,
    autonomous_system_accountability_vacuum: 0.28,
    AI_liability_unclarity_risk: 0.30,
    algorithmic_auditing_deficit: 0.25,
    AI_international_cooperation_failure: 0.32,
    AI_compute_governance_gap: 0.28,
    AI_training_data_governance_risk: 0.30,
    AI_deployment_speed_vs_governance_gap: 0.30,
    existential_risk_regulatory_blindspot: 0.30,
    AI_market_concentration_regulatory_gap: 0.28,
    democratic_AI_oversight_weakness: 0.28,
    AI_whistleblower_protection_gap: 0.25,
    AI_incident_reporting_deficit: 0.22,
    regulatory_capture_by_AI_industry: 0.25,
    AI_rights_legal_framework_absence: 0.22,
    AI_geopolitical_standards_war: 0.25,
  },
  // AGE-007 — APAC, existential_safety_gap → high, existential_risk_blindspot
  // existential_risk_regulatory_blindspot>=0.70 AND AI_safety_standard_gap>=0.65 → existential_risk_blindspot
  // reg_frag=0.55<0.70 → avoids governance_vacuum_crisis
  // acc_vac=0.55<0.70 → avoids accountability_collapse
  // reg_cap=0.48<0.70 → avoids AI_regulatory_capture
  // composite in [40,60) → high
  {
    id: "AGE-007", governance_context: "existential_safety_gap", region: "APAC",
    AI_regulatory_fragmentation_index: 0.55,
    AI_safety_standard_gap: 0.72,
    autonomous_system_accountability_vacuum: 0.55,
    AI_liability_unclarity_risk: 0.50,
    algorithmic_auditing_deficit: 0.52,
    AI_international_cooperation_failure: 0.50,
    AI_compute_governance_gap: 0.48,
    AI_training_data_governance_risk: 0.52,
    AI_deployment_speed_vs_governance_gap: 0.50,
    existential_risk_regulatory_blindspot: 0.78,
    AI_market_concentration_regulatory_gap: 0.60,
    democratic_AI_oversight_weakness: 0.55,
    AI_whistleblower_protection_gap: 0.45,
    AI_incident_reporting_deficit: 0.42,
    regulatory_capture_by_AI_industry: 0.48,
    AI_rights_legal_framework_absence: 0.40,
    AI_geopolitical_standards_war: 0.50,
  },
  // AGE-008 — NOAM, geopolitical_AI_fragmentation → critical, geopolitical_standards_war
  // AI_geopolitical_standards_war>=0.70 AND AI_international_cooperation_failure>=0.65 → geopolitical_standards_war
  // reg_frag=0.65<0.70 → avoids governance_vacuum_crisis
  // acc_vac=0.62<0.70 → avoids accountability_collapse
  // reg_cap=0.62<0.70 → avoids AI_regulatory_capture
  // exist_risk=0.68<0.70 → avoids existential_risk_blindspot
  // composite≥60 → critical
  {
    id: "AGE-008", governance_context: "geopolitical_AI_fragmentation", region: "NOAM",
    AI_regulatory_fragmentation_index: 0.65,
    AI_safety_standard_gap: 0.62,
    autonomous_system_accountability_vacuum: 0.62,
    AI_liability_unclarity_risk: 0.58,
    algorithmic_auditing_deficit: 0.60,
    AI_international_cooperation_failure: 0.78,
    AI_compute_governance_gap: 0.65,
    AI_training_data_governance_risk: 0.62,
    AI_deployment_speed_vs_governance_gap: 0.60,
    existential_risk_regulatory_blindspot: 0.68,
    AI_market_concentration_regulatory_gap: 0.70,
    democratic_AI_oversight_weakness: 0.65,
    AI_whistleblower_protection_gap: 0.58,
    AI_incident_reporting_deficit: 0.55,
    regulatory_capture_by_AI_industry: 0.62,
    AI_rights_legal_framework_absence: 0.52,
    AI_geopolitical_standards_war: 0.82,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function regulatoryScore(e: Entity): number {
  const raw = (
    e.AI_regulatory_fragmentation_index * 0.4 +
    e.AI_safety_standard_gap * 0.35 +
    e.AI_deployment_speed_vs_governance_gap * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function accountabilityScore(e: Entity): number {
  const raw = (
    e.autonomous_system_accountability_vacuum * 0.4 +
    e.AI_liability_unclarity_risk * 0.35 +
    e.algorithmic_auditing_deficit * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function governanceScore(e: Entity): number {
  const raw = (
    e.AI_international_cooperation_failure * 0.4 +
    e.democratic_AI_oversight_weakness * 0.35 +
    e.regulatory_capture_by_AI_industry * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function systemicScore(e: Entity): number {
  const raw = (
    e.existential_risk_regulatory_blindspot * 0.4 +
    e.AI_market_concentration_regulatory_gap * 0.35 +
    e.AI_geopolitical_standards_war * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function computeComposite(reg: number, acc: number, gov: number, sys: number): number {
  return Math.round((reg * 0.30 + acc * 0.25 + gov * 0.25 + sys * 0.20) * 100) / 100;
}

function aiGovernancePattern(e: Entity): string {
  if (e.AI_regulatory_fragmentation_index >= 0.70 && e.AI_deployment_speed_vs_governance_gap >= 0.65)
    return "governance_vacuum_crisis";
  if (e.autonomous_system_accountability_vacuum >= 0.70 && e.AI_liability_unclarity_risk >= 0.65)
    return "accountability_collapse";
  if (e.regulatory_capture_by_AI_industry >= 0.70 && e.democratic_AI_oversight_weakness >= 0.65)
    return "AI_regulatory_capture";
  if (e.existential_risk_regulatory_blindspot >= 0.70 && e.AI_safety_standard_gap >= 0.65)
    return "existential_risk_blindspot";
  if (e.AI_geopolitical_standards_war >= 0.70 && e.AI_international_cooperation_failure >= 0.65)
    return "geopolitical_standards_war";
  return "none";
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function severity(risk: string): string {
  if (risk === "critical") return "vide_gouvernance_IA_systémique";
  if (risk === "high") return "crise_régulation_IA_majeure";
  if (risk === "moderate") return "fragilité_gouvernance_IA_structurelle";
  return "gouvernance_IA_relative";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_gouvernance_IA_urgente";
  if (risk === "high") return "régulation_IA_internationale_accélérée";
  if (risk === "moderate") return "renforcement_oversight_IA_démocratique";
  return "veille_gouvernance_IA_continue";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Vide gouvernance IA systémique — IA hors contrôle démocratique";
  if (risk === "high") return "🟠 Crise régulation IA majeure détectée";
  if (risk === "moderate") return "🟡 Fragilité gouvernance IA structurelle active";
  return "🟢 Gouvernance IA relativement maintenue";
}

export async function GET() {
  if (!SWARM_API_URL) {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "SWARM_API_URL not configured" }, "ai-governance-engine") as Record<string, unknown>,
      { status: 502 }
    ));
  }

  try {
    const entities = MOCK_ENTITIES.map(e => {
      const reg  = regulatoryScore(e);
      const acc  = accountabilityScore(e);
      const gov  = governanceScore(e);
      const sys  = systemicScore(e);
      const comp = computeComposite(reg, acc, gov, sys);
      const pat  = aiGovernancePattern(e);
      const risk = riskLevel(comp);
      const sev  = severity(risk);
      const act  = recommendedAction(risk);
      const sig  = signal(risk);

      return {
        id:                              e.entity_id,
        governance_context:                     e.governance_context,
        region:                                 e.region,
        regulatory_score:                       reg,
        accountability_score:                   acc,
        governance_score:                       gov,
        systemic_score:                         sys,
        composite_score:                        comp,
        risk_level:                             risk,
        ai_governance_pattern:                  pat,
        severity:                               sev,
        recommended_action:                     act,
        signal:                                 sig,
        AI_regulatory_fragmentation_index:      e.AI_regulatory_fragmentation_index,
        existential_risk_regulatory_blindspot:  e.existential_risk_regulatory_blindspot,
      };
    });

    const patternDist:  Record<string, number> = {};
    const riskDist:     Record<string, number> = {};
    const severityDist: Record<string, number> = {};
    const actionDist:   Record<string, number> = {};
    let tComp = 0, tReg = 0;

    for (const ent of entities) {
      patternDist[ent.ai_governance_pattern]  = (patternDist[ent.ai_governance_pattern]  || 0) + 1;
      riskDist[ent.risk_level]                = (riskDist[ent.risk_level]                || 0) + 1;
      severityDist[ent.severity]              = (severityDist[ent.severity]              || 0) + 1;
      actionDist[ent.recommended_action]      = (actionDist[ent.recommended_action]      || 0) + 1;
      tComp += ent.composite_score;
      tReg  += ent.regulatory_score;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 100) / 100;

    const summary = {
      module_id:                          360,
      module_name:                        "AI Governance & Regulatory Intelligence Engine",
      total_entities:                     n,
      critical_count:                     riskDist["critical"]  || 0,
      high_count:                         riskDist["high"]      || 0,
      moderate_count:                     riskDist["moderate"]  || 0,
      low_count:                          riskDist["low"]       || 0,
      avg_composite:                      avgComposite,
      pattern_distribution:               patternDist,
      risk_distribution:                  riskDist,
      severity_distribution:              severityDist,
      action_distribution:                actionDist,
      avg_estimated_ai_governance_index:  Math.round(avgComposite / 100 * 10 * 100) / 100,
      avg_regulatory_score:               Math.round(tReg / n * 100) / 100,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary }, "ai-governance-engine") as Record<string, unknown>
    ));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Erreur moteur gouvernance IA" }, "ai-governance-engine") as Record<string, unknown>,
      { status: 502 }
    ));
  }
}
