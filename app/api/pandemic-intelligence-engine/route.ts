import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// PAN-001: MEA, respiratory_pathogen → critical, pandemic_emergence
// PAN-002: APAC, endemic_virus       → low,      none
// PAN-003: NOAM, respiratory_pathogen → high,    variant_escape_cascade
// PAN-004: LATAM, vector_borne       → low,      none
// PAN-005: EMEA, respiratory_pathogen → critical, healthcare_system_collapse
// PAN-006: APAC, bacterial_pathogen  → moderate, none
// PAN-007: MEA,  zoonotic            → high,     zoonotic_explosion
// PAN-008: NOAM, drug_resistant      → critical, amr_catastrophe
const MOCK_ENTITIES = [
  // PAN-001 — critical, pandemic_emergence
  // pandemic_emergence: transmission_velocity≥0.70 AND surveillance_gap_index≥0.65
  // composite≥60
  { entity_id:"PAN-001", pathogen_category:"respiratory_pathogen", region:"MEA",
    transmission_velocity:0.88,          case_fatality_escalation_risk:0.82, healthcare_capacity_saturation:0.78,
    genomic_variant_emergence_rate:0.60, vaccine_efficacy_erosion:0.58,      surveillance_gap_index:0.85,
    cross_border_spread_velocity:0.84,   pandemic_preparedness_deficit:0.80, zoonotic_spillover_risk:0.50,
    antimicrobial_resistance_amplification:0.55, supply_chain_medical_fragility:0.72, public_health_compliance_erosion:0.70,
    long_covid_economic_burden:0.65,     variant_immune_evasion_potential:0.60, healthcare_worker_attrition:0.68,
    global_health_governance_gap:0.75,   digital_health_surveillance_coverage:0.15 },

  // PAN-002 — low, none
  // composite<20 — all risk-driving fields low, protective fields high
  { entity_id:"PAN-002", pathogen_category:"endemic_virus", region:"APAC",
    transmission_velocity:0.10,          case_fatality_escalation_risk:0.08, healthcare_capacity_saturation:0.12,
    genomic_variant_emergence_rate:0.10, vaccine_efficacy_erosion:0.08,      surveillance_gap_index:0.10,
    cross_border_spread_velocity:0.08,   pandemic_preparedness_deficit:0.10, zoonotic_spillover_risk:0.08,
    antimicrobial_resistance_amplification:0.08, supply_chain_medical_fragility:0.10, public_health_compliance_erosion:0.10,
    long_covid_economic_burden:0.08,     variant_immune_evasion_potential:0.10, healthcare_worker_attrition:0.08,
    global_health_governance_gap:0.10,   digital_health_surveillance_coverage:0.90 },

  // PAN-003 — high, variant_escape_cascade
  // variant_escape_cascade: variant_immune_evasion_potential≥0.70 AND vaccine_efficacy_erosion≥0.65
  // 40≤composite<60; pandemic_emergence must NOT fire: either transmission_velocity<0.70 OR surveillance_gap_index<0.65
  { entity_id:"PAN-003", pathogen_category:"respiratory_pathogen", region:"NOAM",
    transmission_velocity:0.55,          case_fatality_escalation_risk:0.52, healthcare_capacity_saturation:0.50,
    genomic_variant_emergence_rate:0.55, vaccine_efficacy_erosion:0.72,      surveillance_gap_index:0.48,
    cross_border_spread_velocity:0.60,   pandemic_preparedness_deficit:0.50, zoonotic_spillover_risk:0.40,
    antimicrobial_resistance_amplification:0.42, supply_chain_medical_fragility:0.48, public_health_compliance_erosion:0.45,
    long_covid_economic_burden:0.50,     variant_immune_evasion_potential:0.78, healthcare_worker_attrition:0.45,
    global_health_governance_gap:0.48,   digital_health_surveillance_coverage:0.52 },

  // PAN-004 — low, none
  { entity_id:"PAN-004", pathogen_category:"vector_borne", region:"LATAM",
    transmission_velocity:0.12,          case_fatality_escalation_risk:0.10, healthcare_capacity_saturation:0.15,
    genomic_variant_emergence_rate:0.12, vaccine_efficacy_erosion:0.10,      surveillance_gap_index:0.12,
    cross_border_spread_velocity:0.10,   pandemic_preparedness_deficit:0.12, zoonotic_spillover_risk:0.10,
    antimicrobial_resistance_amplification:0.10, supply_chain_medical_fragility:0.12, public_health_compliance_erosion:0.12,
    long_covid_economic_burden:0.10,     variant_immune_evasion_potential:0.12, healthcare_worker_attrition:0.10,
    global_health_governance_gap:0.12,   digital_health_surveillance_coverage:0.88 },

  // PAN-005 — critical, healthcare_system_collapse
  // healthcare_system_collapse: healthcare_capacity_saturation≥0.70 AND healthcare_worker_attrition≥0.65
  // composite≥60; pandemic_emergence must NOT fire: either transmission_velocity<0.70 OR surveillance_gap_index<0.65
  // variant_escape_cascade must NOT fire: either variant_immune_evasion_potential<0.70 OR vaccine_efficacy_erosion<0.65
  { entity_id:"PAN-005", pathogen_category:"respiratory_pathogen", region:"EMEA",
    transmission_velocity:0.55,          case_fatality_escalation_risk:0.85, healthcare_capacity_saturation:0.88,
    genomic_variant_emergence_rate:0.62, vaccine_efficacy_erosion:0.55,      surveillance_gap_index:0.55,
    cross_border_spread_velocity:0.78,   pandemic_preparedness_deficit:0.82, zoonotic_spillover_risk:0.52,
    antimicrobial_resistance_amplification:0.62, supply_chain_medical_fragility:0.80, public_health_compliance_erosion:0.75,
    long_covid_economic_burden:0.70,     variant_immune_evasion_potential:0.60, healthcare_worker_attrition:0.82,
    global_health_governance_gap:0.78,   digital_health_surveillance_coverage:0.18 },

  // PAN-006 — moderate, none
  // 20≤composite<40; no pattern triggers
  { entity_id:"PAN-006", pathogen_category:"bacterial_pathogen", region:"APAC",
    transmission_velocity:0.32,          case_fatality_escalation_risk:0.30, healthcare_capacity_saturation:0.35,
    genomic_variant_emergence_rate:0.28, vaccine_efficacy_erosion:0.30,      surveillance_gap_index:0.32,
    cross_border_spread_velocity:0.30,   pandemic_preparedness_deficit:0.35, zoonotic_spillover_risk:0.28,
    antimicrobial_resistance_amplification:0.32, supply_chain_medical_fragility:0.35, public_health_compliance_erosion:0.30,
    long_covid_economic_burden:0.28,     variant_immune_evasion_potential:0.30, healthcare_worker_attrition:0.30,
    global_health_governance_gap:0.32,   digital_health_surveillance_coverage:0.65 },

  // PAN-007 — high, zoonotic_explosion
  // zoonotic_explosion: zoonotic_spillover_risk≥0.70 AND genomic_variant_emergence_rate≥0.65
  // 40≤composite<60; pandemic_emergence must NOT fire; variant_escape_cascade must NOT fire;
  // healthcare_system_collapse must NOT fire
  { entity_id:"PAN-007", pathogen_category:"zoonotic", region:"MEA",
    transmission_velocity:0.55,          case_fatality_escalation_risk:0.52, healthcare_capacity_saturation:0.55,
    genomic_variant_emergence_rate:0.78, vaccine_efficacy_erosion:0.48,      surveillance_gap_index:0.50,
    cross_border_spread_velocity:0.58,   pandemic_preparedness_deficit:0.52, zoonotic_spillover_risk:0.82,
    antimicrobial_resistance_amplification:0.45, supply_chain_medical_fragility:0.50, public_health_compliance_erosion:0.48,
    long_covid_economic_burden:0.50,     variant_immune_evasion_potential:0.55, healthcare_worker_attrition:0.48,
    global_health_governance_gap:0.50,   digital_health_surveillance_coverage:0.50 },

  // PAN-008 — critical, amr_catastrophe
  // amr_catastrophe: antimicrobial_resistance_amplification≥0.70 AND pandemic_preparedness_deficit≥0.65
  // composite≥60; pandemic_emergence must NOT fire; variant_escape_cascade must NOT fire;
  // healthcare_system_collapse must NOT fire; zoonotic_explosion must NOT fire
  { entity_id:"PAN-008", pathogen_category:"drug_resistant", region:"NOAM",
    transmission_velocity:0.60,          case_fatality_escalation_risk:0.80, healthcare_capacity_saturation:0.60,
    genomic_variant_emergence_rate:0.55, vaccine_efficacy_erosion:0.55,      surveillance_gap_index:0.60,
    cross_border_spread_velocity:0.75,   pandemic_preparedness_deficit:0.85, zoonotic_spillover_risk:0.40,
    antimicrobial_resistance_amplification:0.88, supply_chain_medical_fragility:0.75, public_health_compliance_erosion:0.70,
    long_covid_economic_burden:0.65,     variant_immune_evasion_potential:0.60, healthcare_worker_attrition:0.62,
    global_health_governance_gap:0.82,   digital_health_surveillance_coverage:0.20 },
];

type Entity = typeof MOCK_ENTITIES[0];

function transmissionScore(e: Entity): number {
  const raw = (
    e.transmission_velocity            * 0.40 +
    e.cross_border_spread_velocity     * 0.35 +
    e.variant_immune_evasion_potential * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function severityScore(e: Entity): number {
  const raw = (
    e.case_fatality_escalation_risk * 0.40 +
    e.healthcare_capacity_saturation * 0.35 +
    e.healthcare_worker_attrition    * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function preparednessScore(e: Entity): number {
  const raw = (
    e.pandemic_preparedness_deficit                   * 0.40 +
    e.surveillance_gap_index                          * 0.35 +
    (1 - e.digital_health_surveillance_coverage)      * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function systemicScore(e: Entity): number {
  const raw = (
    e.antimicrobial_resistance_amplification * 0.40 +
    e.global_health_governance_gap           * 0.35 +
    e.supply_chain_medical_fragility         * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function pandemicComposite(trans: number, sev: number, prep: number, syst: number): number {
  return Math.round((trans * 0.30 + sev * 0.25 + prep * 0.25 + syst * 0.20) * 100) / 100;
}

function pandemicRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function pandemicPattern(e: Entity): string {
  if (e.transmission_velocity >= 0.70 && e.surveillance_gap_index >= 0.65)
    return "pandemic_emergence";
  if (e.variant_immune_evasion_potential >= 0.70 && e.vaccine_efficacy_erosion >= 0.65)
    return "variant_escape_cascade";
  if (e.healthcare_capacity_saturation >= 0.70 && e.healthcare_worker_attrition >= 0.65)
    return "healthcare_system_collapse";
  if (e.antimicrobial_resistance_amplification >= 0.70 && e.pandemic_preparedness_deficit >= 0.65)
    return "amr_catastrophe";
  if (e.zoonotic_spillover_risk >= 0.70 && e.genomic_variant_emergence_rate >= 0.65)
    return "zoonotic_explosion";
  return "none";
}

function pandemicSeverity(comp: number): string {
  if (comp >= 75) return "pandemic_emergency";
  if (comp >= 50) return "epidemic_crisis";
  if (comp >= 25) return "outbreak_developing";
  return "containment_adequate";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "pandemic_emergency_response";
  if (risk === "high" && pattern === "healthcare_system_collapse") return "surge_capacity_activation";
  if (risk === "high") return "enhanced_surveillance";
  if (risk === "moderate") return "outbreak_monitoring";
  return "no_action";
}

function pandemicSignal(e: Entity, risk: string, comp: number): string {
  if (risk === "critical") {
    return `Critique — vélocité transmission ${Math.round(e.transmission_velocity * 100)}% — saturation capacité sanitaire ${Math.round(e.healthcare_capacity_saturation * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "high") {
    return `Élevé — déficit préparation pandémique ${Math.round(e.pandemic_preparedness_deficit * 100)}% — résistance antimicrobiens ${Math.round(e.antimicrobial_resistance_amplification * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "moderate") {
    return `Modéré — indice lacune surveillance ${Math.round(e.surveillance_gap_index * 100)}% — composite ${Math.round(comp)}`;
  }
  return "Confinement adéquat — surveillance épidémique solide, capacité sanitaire préservée, préparation pandémique robuste";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const trans = transmissionScore(e);
      const sev   = severityScore(e);
      const prep  = preparednessScore(e);
      const syst  = systemicScore(e);
      const comp  = pandemicComposite(trans, sev, prep, syst);
      const risk  = pandemicRisk(comp);
      const pat   = pandemicPattern(e);
      const severity = pandemicSeverity(comp);
      const action   = recommendedAction(risk, pat);
      const signal   = pandemicSignal(e, risk, comp);
      return {
        entity_id:                       e.entity_id,
        region:                          e.region,
        pathogen_category:               e.pathogen_category,
        pandemic_risk:                   risk,
        pandemic_pattern:                pat,
        pandemic_severity:               severity,
        recommended_action:              action,
        transmission_score:              trans,
        severity_score:                  sev,
        preparedness_score:              prep,
        systemic_score:                  syst,
        pandemic_composite:              comp,
        is_pandemic_crisis:              comp >= 60,
        requires_pandemic_intervention:  comp >= 40,
        pandemic_signal:                 signal,
      };
    });

    const rc: Record<string,number> = {};
    const pc: Record<string,number> = {};
    const sc: Record<string,number> = {};
    const ac: Record<string,number> = {};
    let tTrans=0, tSev=0, tPrep=0, tSyst=0, tComp=0;
    let crisisC=0, interventionC=0;

    for (const ent of entities) {
      rc[ent.pandemic_risk]           = (rc[ent.pandemic_risk]           || 0) + 1;
      pc[ent.pandemic_pattern]        = (pc[ent.pandemic_pattern]        || 0) + 1;
      sc[ent.pandemic_severity]       = (sc[ent.pandemic_severity]       || 0) + 1;
      ac[ent.recommended_action]      = (ac[ent.recommended_action]      || 0) + 1;
      tTrans += ent.transmission_score;
      tSev   += ent.severity_score;
      tPrep  += ent.preparedness_score;
      tSyst  += ent.systemic_score;
      tComp  += ent.pandemic_composite;
      if (ent.is_pandemic_crisis)             crisisC++;
      if (ent.requires_pandemic_intervention) interventionC++;
    }

    const n = entities.length;
    const avgComp = tComp / n;

    const nonNone = Object.entries(pc).filter(([k]) => k !== "none");
    const dominantPattern = nonNone.length
      ? nonNone.reduce((a, b) => (b[1] > a[1] ? b : a))[0]
      : "none";

    const highestRiskEntity =
      (entities.find(e => e.pandemic_risk === "critical") ??
       entities.find(e => e.pandemic_risk === "high")     ??
       entities.find(e => e.pandemic_risk === "moderate") ??
       entities[0])?.entity_id ?? "";

    const summary = {
      total_entities_analyzed:             n,
      critical_pandemic_risks:             rc["critical"]  || 0,
      high_pandemic_risks:                 rc["high"]      || 0,
      moderate_pandemic_risks:             rc["moderate"]  || 0,
      low_pandemic_risks:                  rc["low"]       || 0,
      pandemic_crises_detected:            crisisC,
      pandemic_interventions_required:     interventionC,
      dominant_pandemic_pattern:           dominantPattern,
      avg_estimated_pandemic_threat_index: Math.round(avgComp / 100 * 10 * 100) / 100,
      highest_risk_entity:                 highestRiskEntity,
      results:                             entities,
      analysis_timestamp:                  new Date().toISOString(),
      engine_version:                      "325.0.0",
      // distribution helpers for the dashboard
      risk_counts:                         rc,
      pattern_counts:                      pc,
      severity_counts:                     sc,
      action_counts:                       ac,
      avg_transmission_score:              Math.round(tTrans / n * 10) / 10,
      avg_severity_score:                  Math.round(tSev   / n * 10) / 10,
      avg_preparedness_score:              Math.round(tPrep  / n * 10) / 10,
      avg_systemic_score:                  Math.round(tSyst  / n * 10) / 10,
      avg_pandemic_composite:              Math.round(avgComp * 10) / 10,
    };

    return NextResponse.json(sealResponse(summary, "pandemic-intelligence-engine"));
  }

  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/pandemic-intelligence-engine`);
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    return NextResponse.json(sealResponse(await res.json(), "pandemic-intelligence-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream pandemic intelligence unavailable" }, "pandemic-intelligence-engine"),
      { status: 502 }
    );
  }
}
