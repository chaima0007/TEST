import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  // RRE-001 — LATAM, avortement → critical, total_abortion_ban_crisis
  { entity_id: "RRE-001", rights_domain: "avortement", region: "LATAM",
    legal_access: 0.05, healthcare_access: 0.20, coercion_index: 0.60,
    criminalization_risk: 0.92, maternal_mortality_rate: 0.75, contraception_coverage: 0.30,
    sex_education_quality: 0.18, poverty_intersection: 0.78, racial_disparity: 0.55,
    geographic_inequality: 0.68, provider_shortage: 0.72, stigma_index: 0.75,
    data_surveillance: 0.42, political_restriction: 0.88, international_compliance: 0.12,
    youth_access: 0.15, disability_inclusion: 0.10 },

  // RRE-002 — APAC, stérilisation → critical, coercive_sterilization_pattern
  { entity_id: "RRE-002", rights_domain: "stérilisation", region: "APAC",
    legal_access: 0.22, healthcare_access: 0.35, coercion_index: 0.82,
    criminalization_risk: 0.55, maternal_mortality_rate: 0.48, contraception_coverage: 0.40,
    sex_education_quality: 0.22, poverty_intersection: 0.70, racial_disparity: 0.80,
    geographic_inequality: 0.60, provider_shortage: 0.58, stigma_index: 0.72,
    data_surveillance: 0.50, political_restriction: 0.65, international_compliance: 0.18,
    youth_access: 0.20, disability_inclusion: 0.15 },

  // RRE-003 — SSA, santé maternelle → critical, maternal_mortality_collapse
  { entity_id: "RRE-003", rights_domain: "santé_maternelle", region: "SSA",
    legal_access: 0.28, healthcare_access: 0.12, coercion_index: 0.55,
    criminalization_risk: 0.60, maternal_mortality_rate: 0.90, contraception_coverage: 0.22,
    sex_education_quality: 0.20, poverty_intersection: 0.85, racial_disparity: 0.65,
    geographic_inequality: 0.75, provider_shortage: 0.88, stigma_index: 0.60,
    data_surveillance: 0.30, political_restriction: 0.58, international_compliance: 0.20,
    youth_access: 0.18, disability_inclusion: 0.08 },

  // RRE-004 — MEA, contraception → high, contraception_access_barrier
  { entity_id: "RRE-004", rights_domain: "contraception", region: "MEA",
    legal_access: 0.38, healthcare_access: 0.35, coercion_index: 0.50,
    criminalization_risk: 0.45, maternal_mortality_rate: 0.52, contraception_coverage: 0.20,
    sex_education_quality: 0.25, poverty_intersection: 0.62, racial_disparity: 0.48,
    geographic_inequality: 0.55, provider_shortage: 0.72, stigma_index: 0.58,
    data_surveillance: 0.38, political_restriction: 0.55, international_compliance: 0.28,
    youth_access: 0.22, disability_inclusion: 0.18 },

  // RRE-005 — EMEA, surveillance → high, reproductive_surveillance_state
  { entity_id: "RRE-005", rights_domain: "surveillance_reproductive", region: "EMEA",
    legal_access: 0.42, healthcare_access: 0.55, coercion_index: 0.58,
    criminalization_risk: 0.48, maternal_mortality_rate: 0.32, contraception_coverage: 0.60,
    sex_education_quality: 0.40, poverty_intersection: 0.42, racial_disparity: 0.38,
    geographic_inequality: 0.42, provider_shortage: 0.45, stigma_index: 0.55,
    data_surveillance: 0.82, political_restriction: 0.78, international_compliance: 0.35,
    youth_access: 0.38, disability_inclusion: 0.30 },

  // RRE-006 — NOAM, éducation sexuelle → moderate, none
  { entity_id: "RRE-006", rights_domain: "éducation_sexuelle", region: "NOAM",
    legal_access: 0.65, healthcare_access: 0.62, coercion_index: 0.30,
    criminalization_risk: 0.25, maternal_mortality_rate: 0.28, contraception_coverage: 0.68,
    sex_education_quality: 0.38, poverty_intersection: 0.35, racial_disparity: 0.40,
    geographic_inequality: 0.30, provider_shortage: 0.32, stigma_index: 0.35,
    data_surveillance: 0.28, political_restriction: 0.30, international_compliance: 0.62,
    youth_access: 0.42, disability_inclusion: 0.40 },

  // RRE-007 — NOAM, avortement → low, none
  { entity_id: "RRE-007", rights_domain: "avortement", region: "NOAM",
    legal_access: 0.90, healthcare_access: 0.88, coercion_index: 0.08,
    criminalization_risk: 0.05, maternal_mortality_rate: 0.10, contraception_coverage: 0.92,
    sex_education_quality: 0.85, poverty_intersection: 0.12, racial_disparity: 0.10,
    geographic_inequality: 0.08, provider_shortage: 0.10, stigma_index: 0.08,
    data_surveillance: 0.05, political_restriction: 0.08, international_compliance: 0.95,
    youth_access: 0.88, disability_inclusion: 0.82 },

  // RRE-008 — EU, droits reproductifs → low, none
  { entity_id: "RRE-008", rights_domain: "droits_reproductifs", region: "EU",
    legal_access: 0.88, healthcare_access: 0.90, coercion_index: 0.05,
    criminalization_risk: 0.04, maternal_mortality_rate: 0.08, contraception_coverage: 0.90,
    sex_education_quality: 0.88, poverty_intersection: 0.10, racial_disparity: 0.08,
    geographic_inequality: 0.06, provider_shortage: 0.08, stigma_index: 0.06,
    data_surveillance: 0.04, political_restriction: 0.05, international_compliance: 0.98,
    youth_access: 0.90, disability_inclusion: 0.85 },
];

type Entity = typeof MOCK_ENTITIES[0];

function accessScore(e: Entity): number {
  const raw = (
    (1 - e.healthcare_access) * 0.40
    + (1 - e.contraception_coverage) * 0.35
    + e.provider_shortage * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function legalScore(e: Entity): number {
  const raw = (
    (1 - e.legal_access) * 0.40
    + e.criminalization_risk * 0.35
    + e.political_restriction * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function coercionScore(e: Entity): number {
  const raw = (
    e.coercion_index * 0.40
    + e.stigma_index * 0.35
    + e.data_surveillance * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function disparityScore(e: Entity): number {
  const raw = (
    e.racial_disparity * 0.40
    + e.geographic_inequality * 0.35
    + e.poverty_intersection * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function reproductiveComposite(access: number, legal: number, coercion: number, disparity: number): number {
  return Math.round((access * 0.30 + legal * 0.25 + coercion * 0.25 + disparity * 0.20) * 100) / 100;
}

function reproductiveRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function reproductivePattern(e: Entity): string {
  if (e.criminalization_risk >= 0.75 && e.legal_access <= 0.20) return "total_abortion_ban_crisis";
  if (e.coercion_index >= 0.70 && e.racial_disparity >= 0.65) return "coercive_sterilization_pattern";
  if (e.maternal_mortality_rate >= 0.70 && e.healthcare_access <= 0.30) return "maternal_mortality_collapse";
  if ((1 - e.contraception_coverage) >= 0.65 && e.provider_shortage >= 0.60) return "contraception_access_barrier";
  if (e.data_surveillance >= 0.70 && e.political_restriction >= 0.65) return "reproductive_surveillance_state";
  return "none";
}

function reproductiveSeverity(comp: number): string {
  if (comp >= 75) return "urgence_reproductive";
  if (comp >= 50) return "risque_reproductif_élevé";
  if (comp >= 25) return "stress_reproductif";
  return "autonomie_corporelle_préservée";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "intervention_d_urgence_reproductive";
  if (risk === "high" && pattern === "maternal_mortality_collapse") return "sauvetage_maternel_prioritaire";
  if (risk === "high") return "renforcement_droits_reproductifs";
  if (risk === "moderate") return "surveillance_reproductive";
  return "aucune_action";
}

function reproductiveSignal(e: Entity, risk: string, comp: number): string {
  const compInt = Math.round(comp);
  if (risk === "critical") {
    return `Critique — accès légal ${Math.round(e.legal_access * 100)}% — risque criminalisation ${Math.round(e.criminalization_risk * 100)}% — composite ${compInt}`;
  }
  if (risk === "high") {
    return `Élevé — couverture contraception ${Math.round(e.contraception_coverage * 100)}% — mortalité maternelle ${Math.round(e.maternal_mortality_rate * 100)}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `Modéré — accès soins ${Math.round(e.healthcare_access * 100)}% — composite ${compInt}`;
  }
  return "Droits reproductifs protégés — autonomie corporelle respectée, accès universel garanti";
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const access   = accessScore(e);
      const legal    = legalScore(e);
      const coercion = coercionScore(e);
      const disparity = disparityScore(e);
      const comp     = reproductiveComposite(access, legal, coercion, disparity);
      const risk     = reproductiveRisk(comp);
      const pattern  = reproductivePattern(e);
      const severity = reproductiveSeverity(comp);
      const action   = recommendedAction(risk, pattern);
      const signal   = reproductiveSignal(e, risk, comp);

      return {
        entity_id:                           e.entity_id,
        region:                              e.region,
        rights_domain:                       e.rights_domain,
        reproductive_risk:                   risk,
        reproductive_pattern:                pattern,
        reproductive_severity:               severity,
        recommended_action:                  action,
        access_score:                        access,
        legal_score:                         legal,
        coercion_score:                      coercion,
        disparity_score:                     disparity,
        reproductive_composite:              comp,
        is_in_reproductive_crisis:           comp >= 60,
        requires_reproductive_intervention:  comp >= 40,
        reproductive_signal:                 signal,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tAccess = 0, tLegal = 0, tCoercion = 0, tDisparity = 0, tComp = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.reproductive_risk]     = (rc[ent.reproductive_risk]     || 0) + 1;
      pc[ent.reproductive_pattern]  = (pc[ent.reproductive_pattern]  || 0) + 1;
      sc[ent.reproductive_severity] = (sc[ent.reproductive_severity] || 0) + 1;
      ac[ent.recommended_action]    = (ac[ent.recommended_action]    || 0) + 1;
      tAccess    += ent.access_score;
      tLegal     += ent.legal_score;
      tCoercion  += ent.coercion_score;
      tDisparity += ent.disparity_score;
      tComp      += ent.reproductive_composite;
      if (ent.is_in_reproductive_crisis)          crisisCount++;
      if (ent.requires_reproductive_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 10) / 10;

    const summary = {
      total:                                   n,
      risk_counts:                             rc,
      pattern_counts:                          pc,
      severity_counts:                         sc,
      action_counts:                           ac,
      avg_reproductive_composite:              avgComp,
      reproductive_crisis_count:               crisisCount,
      reproductive_intervention_count:         interventionCount,
      avg_access_score:                        Math.round(tAccess    / n * 10) / 10,
      avg_legal_score:                         Math.round(tLegal     / n * 10) / 10,
      avg_coercion_score:                      Math.round(tCoercion  / n * 10) / 10,
      avg_disparity_score:                     Math.round(tDisparity / n * 10) / 10,
      avg_estimated_reproductive_rights_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/reproductive-rights-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(sealResponse(await res.json()));
  } catch {}
  return NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 });
}
