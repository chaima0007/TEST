import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // PRE-001 — critical, mass_incarceration_industrial (incarceration>0.85, drug>0.80)
  {
    id: "PRE-001", justice_system_type: "pénal_carcéral", region: "NOAM",
    incarceration_rate_excess: 0.92, pretrial_detention_rate: 0.78,
    racial_sentencing_disparity: 0.70, mandatory_minimum_overuse: 0.72,
    private_prison_profit_motive: 0.68, recidivism_rate_high: 0.70,
    rehabilitation_program_gap: 0.65, solitary_confinement_use: 0.60,
    prison_labor_exploitation: 0.62, mental_health_treatment_gap: 0.65,
    overcrowding_rate: 0.72, bail_system_inequality: 0.68,
    public_defender_underresourcing: 0.70, reentry_program_deficit: 0.65,
    voting_rights_disenfranchisement: 0.60, family_separation_impact: 0.68,
    drug_offense_overincarceration: 0.88,
  },
  // PRE-002 — critical, racial_disparity_sentencing (racial>0.85, mandatory>0.80)
  {
    id: "PRE-002", justice_system_type: "tribunal_correctionnel", region: "NOAM",
    incarceration_rate_excess: 0.72, pretrial_detention_rate: 0.70,
    racial_sentencing_disparity: 0.90, mandatory_minimum_overuse: 0.85,
    private_prison_profit_motive: 0.65, recidivism_rate_high: 0.68,
    rehabilitation_program_gap: 0.62, solitary_confinement_use: 0.58,
    prison_labor_exploitation: 0.60, mental_health_treatment_gap: 0.62,
    overcrowding_rate: 0.68, bail_system_inequality: 0.78,
    public_defender_underresourcing: 0.80, reentry_program_deficit: 0.65,
    voting_rights_disenfranchisement: 0.70, family_separation_impact: 0.65,
    drug_offense_overincarceration: 0.70,
  },
  // PRE-003 — critical, recidivism_rehabilitation_gap (recidivism>0.85, rehab_gap>0.80)
  {
    id: "PRE-003", justice_system_type: "établissement_pénitentiaire", region: "EMEA",
    incarceration_rate_excess: 0.65, pretrial_detention_rate: 0.68,
    racial_sentencing_disparity: 0.62, mandatory_minimum_overuse: 0.65,
    private_prison_profit_motive: 0.60, recidivism_rate_high: 0.88,
    rehabilitation_program_gap: 0.82, solitary_confinement_use: 0.62,
    prison_labor_exploitation: 0.58, mental_health_treatment_gap: 0.70,
    overcrowding_rate: 0.78, bail_system_inequality: 0.62,
    public_defender_underresourcing: 0.65, reentry_program_deficit: 0.80,
    voting_rights_disenfranchisement: 0.58, family_separation_impact: 0.72,
    drug_offense_overincarceration: 0.65,
  },
  // PRE-004 — high, prison_privatization_abuse (private>0.80, labor>0.75)
  {
    id: "PRE-004", justice_system_type: "prison_privée", region: "NOAM",
    incarceration_rate_excess: 0.50, pretrial_detention_rate: 0.48,
    racial_sentencing_disparity: 0.52, mandatory_minimum_overuse: 0.50,
    private_prison_profit_motive: 0.85, recidivism_rate_high: 0.48,
    rehabilitation_program_gap: 0.50, solitary_confinement_use: 0.52,
    prison_labor_exploitation: 0.80, mental_health_treatment_gap: 0.48,
    overcrowding_rate: 0.50, bail_system_inequality: 0.48,
    public_defender_underresourcing: 0.50, reentry_program_deficit: 0.48,
    voting_rights_disenfranchisement: 0.45, family_separation_impact: 0.50,
    drug_offense_overincarceration: 0.48,
  },
  // PRE-005 — high, solitary_confinement_torture (solitary>0.80, mental_health>0.75)
  {
    id: "PRE-005", justice_system_type: "centre_détention_sécurité_max", region: "LATAM",
    incarceration_rate_excess: 0.48, pretrial_detention_rate: 0.52,
    racial_sentencing_disparity: 0.50, mandatory_minimum_overuse: 0.48,
    private_prison_profit_motive: 0.50, recidivism_rate_high: 0.52,
    rehabilitation_program_gap: 0.48, solitary_confinement_use: 0.85,
    prison_labor_exploitation: 0.50, mental_health_treatment_gap: 0.80,
    overcrowding_rate: 0.52, bail_system_inequality: 0.48,
    public_defender_underresourcing: 0.52, reentry_program_deficit: 0.48,
    voting_rights_disenfranchisement: 0.50, family_separation_impact: 0.52,
    drug_offense_overincarceration: 0.48,
  },
  // PRE-006 — moderate, none
  {
    id: "PRE-006", justice_system_type: "tribunal_de_première_instance", region: "APAC",
    incarceration_rate_excess: 0.28, pretrial_detention_rate: 0.30,
    racial_sentencing_disparity: 0.28, mandatory_minimum_overuse: 0.30,
    private_prison_profit_motive: 0.28, recidivism_rate_high: 0.32,
    rehabilitation_program_gap: 0.28, solitary_confinement_use: 0.30,
    prison_labor_exploitation: 0.28, mental_health_treatment_gap: 0.32,
    overcrowding_rate: 0.30, bail_system_inequality: 0.28,
    public_defender_underresourcing: 0.30, reentry_program_deficit: 0.28,
    voting_rights_disenfranchisement: 0.25, family_separation_impact: 0.30,
    drug_offense_overincarceration: 0.28,
  },
  // PRE-007 — low, none
  {
    id: "PRE-007", justice_system_type: "système_pénal_nordique", region: "EMEA",
    incarceration_rate_excess: 0.10, pretrial_detention_rate: 0.12,
    racial_sentencing_disparity: 0.10, mandatory_minimum_overuse: 0.08,
    private_prison_profit_motive: 0.10, recidivism_rate_high: 0.12,
    rehabilitation_program_gap: 0.08, solitary_confinement_use: 0.10,
    prison_labor_exploitation: 0.08, mental_health_treatment_gap: 0.10,
    overcrowding_rate: 0.12, bail_system_inequality: 0.10,
    public_defender_underresourcing: 0.08, reentry_program_deficit: 0.10,
    voting_rights_disenfranchisement: 0.08, family_separation_impact: 0.10,
    drug_offense_overincarceration: 0.10,
  },
  // PRE-008 — low, none
  {
    id: "PRE-008", justice_system_type: "maison_de_justice", region: "APAC",
    incarceration_rate_excess: 0.12, pretrial_detention_rate: 0.10,
    racial_sentencing_disparity: 0.12, mandatory_minimum_overuse: 0.10,
    private_prison_profit_motive: 0.12, recidivism_rate_high: 0.10,
    rehabilitation_program_gap: 0.12, solitary_confinement_use: 0.08,
    prison_labor_exploitation: 0.10, mental_health_treatment_gap: 0.12,
    overcrowding_rate: 0.10, bail_system_inequality: 0.12,
    public_defender_underresourcing: 0.10, reentry_program_deficit: 0.12,
    voting_rights_disenfranchisement: 0.10, family_separation_impact: 0.08,
    drug_offense_overincarceration: 0.10,
  },
];

type PREInput = typeof MOCK_ENTITIES[0];

function incarcerationScore(e: PREInput): number {
  return Math.round((e.incarceration_rate_excess * 0.4 + e.pretrial_detention_rate * 0.35 + e.drug_offense_overincarceration * 0.25) * 100 * 100) / 100;
}
function racialScore(e: PREInput): number {
  return Math.round((e.racial_sentencing_disparity * 0.4 + e.mandatory_minimum_overuse * 0.35 + e.bail_system_inequality * 0.25) * 100 * 100) / 100;
}
function rehabilitationScore(e: PREInput): number {
  return Math.round((e.recidivism_rate_high * 0.4 + e.rehabilitation_program_gap * 0.35 + e.reentry_program_deficit * 0.25) * 100 * 100) / 100;
}
function systemicScore(e: PREInput): number {
  return Math.round((e.private_prison_profit_motive * 0.4 + e.solitary_confinement_use * 0.35 + e.prison_labor_exploitation * 0.25) * 100 * 100) / 100;
}
function compositeScore(inc: number, rac: number, reh: number, sys: number): number {
  return Math.round((inc * 0.30 + rac * 0.25 + reh * 0.25 + sys * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function justicePattern(e: PREInput): string {
  if (e.incarceration_rate_excess > 0.85 && e.drug_offense_overincarceration > 0.80) return "mass_incarceration_industrial";
  if (e.racial_sentencing_disparity > 0.85 && e.mandatory_minimum_overuse > 0.80) return "racial_disparity_sentencing";
  if (e.recidivism_rate_high > 0.85 && e.rehabilitation_program_gap > 0.80) return "recidivism_rehabilitation_gap";
  if (e.private_prison_profit_motive > 0.80 && e.prison_labor_exploitation > 0.75) return "prison_privatization_abuse";
  if (e.solitary_confinement_use > 0.80 && e.mental_health_treatment_gap > 0.75) return "solitary_confinement_torture";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_justice_pénale_systémique";
  if (composite >= 40) return "crise_droits_fondamentaux_majeure";
  if (composite >= 20) return "inégalité_carcérale_structurelle";
  return "système_pénal_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_réforme_pénale_critique";
  if (risk === "high") return "réforme_systémique_accélérée_droits_détenus";
  if (risk === "moderate") return "renforcement_politiques_justice_réparatrice";
  return "veille_système_pénal_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise justice pénale systémique — droits fondamentaux en péril";
  if (risk === "high") return "🟠 Crise droits fondamentaux majeure détectée";
  if (risk === "moderate") return "🟡 Inégalité carcérale structurelle active";
  return "🟢 Système pénal sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[prison-reform-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tInc = 0, tRac = 0, tReh = 0, tSys = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.justice_pattern]   = (pattern_distribution[ent.justice_pattern]   || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tInc  += ent.incarceration_score;
      tRac  += ent.racial_score;
      tReh  += ent.rehabilitation_score;
      tSys  += ent.systemic_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite        = Math.round(tComp / n * 10) / 10;
    const avgIncarceration    = Math.round(tInc  / n * 10) / 10;

    const summary = {
      module_id:                              443,
      module_name:                            "Réforme Pénale & Justice Systémique Intelligence Engine",
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
      avg_estimated_justice_reform_index:     Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary, avg_incarceration: avgIncarceration }, "prison-reform-engine")
    ));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/prison-reform-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return sealResponse(NextResponse.json(sealResponse(await upstream.json(), "prison-reform-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "prison-reform-engine"),
      { status: 502 }
    ));
  }
}
