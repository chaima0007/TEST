import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// SBR-001: EMEA, gain_of_function → critical, bioweapon_proliferation
// SBR-002: APAC, vaccine_research → low, biosecure/none
// SBR-003: NOAM, pathogen_modification → high, lab_leak_risk
// SBR-004: LATAM, vaccine_research → low, biosecure/none
// SBR-005: MEA, gain_of_function → critical, surveillance_blindspot
// SBR-006: EMEA, gene_therapy → moderate, none
// SBR-007: APAC, pathogen_modification → high, pandemic_unpreparedness
// SBR-008: NOAM, gain_of_function → critical, gene_drive_risk
const MOCK_ENTITIES = [
  // SBR-001 — critical, bioweapon_proliferation
  // bioweapon_proliferation_risk≥0.65 AND (1-international_treaty_adherence)≥0.55 → treaty≤0.45
  // composite≥60 → need high scores across sub-scores
  { id:"SBR-001", bio_domain:"gain_of_function", region:"EMEA",
    pathogen_engineering_capability:0.85, dual_use_research_exposure:0.82, containment_protocol_quality:0.15,
    biosurveillance_coverage:0.20, bioweapon_proliferation_risk:0.88, lab_safety_compliance:0.22,
    international_treaty_adherence:0.30, pandemic_preparedness_index:0.18, gene_drive_deployment_risk:0.50,
    biosecurity_governance_maturity:0.18, academic_biosecurity_culture:0.20, emerging_pathogen_monitoring:0.22,
    biodefense_investment_rate:0.18, supply_chain_bio_vulnerability:0.80, synthetic_pathogen_detectability:0.15,
    public_health_response_speed:0.18, biosecurity_intelligence_coverage:0.20 },

  // SBR-002 — low, none (biosecure)
  { id:"SBR-002", bio_domain:"vaccine_research", region:"APAC",
    pathogen_engineering_capability:0.10, dual_use_research_exposure:0.08, containment_protocol_quality:0.92,
    biosurveillance_coverage:0.90, bioweapon_proliferation_risk:0.08, lab_safety_compliance:0.92,
    international_treaty_adherence:0.95, pandemic_preparedness_index:0.92, gene_drive_deployment_risk:0.05,
    biosecurity_governance_maturity:0.90, academic_biosecurity_culture:0.92, emerging_pathogen_monitoring:0.90,
    biodefense_investment_rate:0.88, supply_chain_bio_vulnerability:0.08, synthetic_pathogen_detectability:0.92,
    public_health_response_speed:0.92, biosecurity_intelligence_coverage:0.90 },

  // SBR-003 — high, lab_leak_risk
  // (1-lab_safety_compliance)≥0.65 → lab_safety≤0.35 AND pathogen_engineering_capability≥0.60
  // composite≥40 but <60
  { id:"SBR-003", bio_domain:"pathogen_modification", region:"NOAM",
    pathogen_engineering_capability:0.72, dual_use_research_exposure:0.55, containment_protocol_quality:0.38,
    biosurveillance_coverage:0.52, bioweapon_proliferation_risk:0.42, lab_safety_compliance:0.28,
    international_treaty_adherence:0.62, pandemic_preparedness_index:0.55, gene_drive_deployment_risk:0.35,
    biosecurity_governance_maturity:0.48, academic_biosecurity_culture:0.52, emerging_pathogen_monitoring:0.58,
    biodefense_investment_rate:0.50, supply_chain_bio_vulnerability:0.45, synthetic_pathogen_detectability:0.60,
    public_health_response_speed:0.55, biosecurity_intelligence_coverage:0.52 },

  // SBR-004 — low, none (biosecure)
  { id:"SBR-004", bio_domain:"vaccine_research", region:"LATAM",
    pathogen_engineering_capability:0.12, dual_use_research_exposure:0.10, containment_protocol_quality:0.88,
    biosurveillance_coverage:0.85, bioweapon_proliferation_risk:0.10, lab_safety_compliance:0.88,
    international_treaty_adherence:0.90, pandemic_preparedness_index:0.88, gene_drive_deployment_risk:0.08,
    biosecurity_governance_maturity:0.85, academic_biosecurity_culture:0.88, emerging_pathogen_monitoring:0.85,
    biodefense_investment_rate:0.82, supply_chain_bio_vulnerability:0.12, synthetic_pathogen_detectability:0.88,
    public_health_response_speed:0.88, biosecurity_intelligence_coverage:0.85 },

  // SBR-005 — critical, surveillance_blindspot
  // (1-biosurveillance_coverage)≥0.65 → biosurveillance≤0.35 AND (1-emerging_pathogen_monitoring)≥0.60 → monitoring≤0.40
  // lab_safety_compliance=0.50 so (1-lsc)=0.50 < 0.65 → lab_leak_risk does NOT fire first
  // composite≥60
  { id:"SBR-005", bio_domain:"gain_of_function", region:"MEA",
    pathogen_engineering_capability:0.78, dual_use_research_exposure:0.75, containment_protocol_quality:0.18,
    biosurveillance_coverage:0.22, bioweapon_proliferation_risk:0.60, lab_safety_compliance:0.50,
    international_treaty_adherence:0.50, pandemic_preparedness_index:0.20, gene_drive_deployment_risk:0.45,
    biosecurity_governance_maturity:0.25, academic_biosecurity_culture:0.28, emerging_pathogen_monitoring:0.25,
    biodefense_investment_rate:0.20, supply_chain_bio_vulnerability:0.75, synthetic_pathogen_detectability:0.20,
    public_health_response_speed:0.22, biosecurity_intelligence_coverage:0.25 },

  // SBR-006 — moderate, none
  // composite≥20 but <40; no pattern triggers
  { id:"SBR-006", bio_domain:"gene_therapy", region:"EMEA",
    pathogen_engineering_capability:0.30, dual_use_research_exposure:0.28, containment_protocol_quality:0.65,
    biosurveillance_coverage:0.62, bioweapon_proliferation_risk:0.25, lab_safety_compliance:0.68,
    international_treaty_adherence:0.72, pandemic_preparedness_index:0.65, gene_drive_deployment_risk:0.30,
    biosecurity_governance_maturity:0.65, academic_biosecurity_culture:0.68, emerging_pathogen_monitoring:0.65,
    biodefense_investment_rate:0.62, supply_chain_bio_vulnerability:0.32, synthetic_pathogen_detectability:0.68,
    public_health_response_speed:0.65, biosecurity_intelligence_coverage:0.62 },

  // SBR-007 — high, pandemic_unpreparedness
  // (1-pandemic_preparedness_index)≥0.70 → preparedness≤0.30 AND (1-public_health_response_speed)≥0.60 → response≤0.40
  // composite≥40 but <60
  { id:"SBR-007", bio_domain:"pathogen_modification", region:"APAC",
    pathogen_engineering_capability:0.55, dual_use_research_exposure:0.52, containment_protocol_quality:0.40,
    biosurveillance_coverage:0.50, bioweapon_proliferation_risk:0.38, lab_safety_compliance:0.55,
    international_treaty_adherence:0.60, pandemic_preparedness_index:0.22, gene_drive_deployment_risk:0.40,
    biosecurity_governance_maturity:0.50, academic_biosecurity_culture:0.55, emerging_pathogen_monitoring:0.55,
    biodefense_investment_rate:0.45, supply_chain_bio_vulnerability:0.48, synthetic_pathogen_detectability:0.58,
    public_health_response_speed:0.28, biosecurity_intelligence_coverage:0.50 },

  // SBR-008 — critical, gene_drive_risk
  // gene_drive_deployment_risk≥0.70 AND (1-biosecurity_governance_maturity)≥0.60 → governance≤0.40
  // lab_safety_compliance=0.50 → (1-lsc)=0.50 < 0.65: no lab_leak_risk
  // biosurveillance_coverage=0.50 → (1-bs)=0.50 < 0.65: no surveillance_blindspot
  // pandemic_preparedness_index=0.40 → (1-pp)=0.60 < 0.70: no pandemic_unpreparedness
  // composite≥60
  { id:"SBR-008", bio_domain:"gain_of_function", region:"NOAM",
    pathogen_engineering_capability:0.80, dual_use_research_exposure:0.78, containment_protocol_quality:0.18,
    biosurveillance_coverage:0.50, bioweapon_proliferation_risk:0.62, lab_safety_compliance:0.50,
    international_treaty_adherence:0.52, pandemic_preparedness_index:0.40, gene_drive_deployment_risk:0.82,
    biosecurity_governance_maturity:0.32, academic_biosecurity_culture:0.35, emerging_pathogen_monitoring:0.30,
    biodefense_investment_rate:0.22, supply_chain_bio_vulnerability:0.72, synthetic_pathogen_detectability:0.22,
    public_health_response_speed:0.45, biosecurity_intelligence_coverage:0.28 },
];

type Entity = typeof MOCK_ENTITIES[0];

function containmentScore(e: Entity): number {
  const raw = (
    (1 - e.containment_protocol_quality) * 0.4 +
    (1 - e.lab_safety_compliance) * 0.35 +
    (1 - e.biosurveillance_coverage) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function proliferationScore(e: Entity): number {
  const raw = (
    e.bioweapon_proliferation_risk * 0.4 +
    e.dual_use_research_exposure * 0.35 +
    e.pathogen_engineering_capability * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function governanceScore(e: Entity): number {
  const raw = (
    (1 - e.biosecurity_governance_maturity) * 0.4 +
    (1 - e.international_treaty_adherence) * 0.35 +
    (1 - e.academic_biosecurity_culture) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function preparednessScore(e: Entity): number {
  const raw = (
    (1 - e.pandemic_preparedness_index) * 0.4 +
    (1 - e.public_health_response_speed) * 0.35 +
    (1 - e.biodefense_investment_rate) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function bioComposite(cont: number, prol: number, gov: number, prep: number): number {
  return Math.round((cont * 0.30 + prol * 0.25 + gov * 0.25 + prep * 0.20) * 100) / 100;
}

function bioRisk(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}

function bioPattern(e: Entity): string {
  if (e.bioweapon_proliferation_risk >= 0.65 && (1 - e.international_treaty_adherence) >= 0.55)
    return "bioweapon_proliferation";
  if ((1 - e.lab_safety_compliance) >= 0.65 && e.pathogen_engineering_capability >= 0.60)
    return "lab_leak_risk";
  if ((1 - e.biosurveillance_coverage) >= 0.65 && (1 - e.emerging_pathogen_monitoring) >= 0.60)
    return "surveillance_blindspot";
  if ((1 - e.pandemic_preparedness_index) >= 0.70 && (1 - e.public_health_response_speed) >= 0.60)
    return "pandemic_unpreparedness";
  if (e.gene_drive_deployment_risk >= 0.70 && (1 - e.biosecurity_governance_maturity) >= 0.60)
    return "gene_drive_risk";
  return "none";
}

function bioSeverity(composite: number): string {
  if (composite >= 75) return "biosecurity_emergency";
  if (composite >= 50) return "high_bio_risk";
  if (composite >= 25) return "bio_stress";
  return "biosecure";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "biosecurity_emergency_response";
  if (risk === "high" && pattern === "bioweapon_proliferation") return "bioweapon_interdiction";
  if (risk === "high") return "biosecurity_reinforcement";
  if (risk === "moderate") return "bio_monitoring";
  return "no_action";
}

function bioSignal(e: Entity, risk: string, composite: number): string {
  if (risk === "critical") {
    return `Critique — risque prolifération bioarmes ${Math.round(e.bioweapon_proliferation_risk * 100)}% — qualité confinement ${Math.round(e.containment_protocol_quality * 100)}% — composite ${Math.round(composite)}`;
  }
  if (risk === "high") {
    return `Élevé — couverture biosurveillance ${Math.round(e.biosurveillance_coverage * 100)}% — préparation pandémique ${Math.round(e.pandemic_preparedness_index * 100)}% — composite ${Math.round(composite)}`;
  }
  if (risk === "moderate") {
    return `Modéré — exposition recherche double usage ${Math.round(e.dual_use_research_exposure * 100)}% — composite ${Math.round(composite)}`;
  }
  return "Biosécurité optimale — confinement rigoureux, gouvernance mature, préparation pandémique solide";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[synthetic-biology-risk-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number> = {};
    const pc: Record<string,number> = {};
    const sc: Record<string,number> = {};
    const ac: Record<string,number> = {};
    let tCont = 0, tProl = 0, tGov = 0, tPrep = 0, tComp = 0;
    let crisisC = 0, interventionC = 0;

    for (const ent of entities) {
      rc[ent.bio_risk]           = (rc[ent.bio_risk]           || 0) + 1;
      pc[ent.bio_pattern]        = (pc[ent.bio_pattern]        || 0) + 1;
      sc[ent.bio_severity]       = (sc[ent.bio_severity]       || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tCont  += ent.containment_score;
      tProl  += ent.proliferation_score;
      tGov   += ent.governance_score;
      tPrep  += ent.preparedness_score;
      tComp  += ent.bio_composite;
      if (ent.is_in_bio_crisis)          crisisC++;
      if (ent.requires_bio_intervention) interventionC++;
    }

    const n = entities.length;
    const avgComp = tComp / n;
    const summary = {
      total:                        n,
      risk_counts:                  rc,
      pattern_counts:               pc,
      severity_counts:              sc,
      action_counts:                ac,
      avg_bio_composite:            Math.round(avgComp * 10) / 10,
      bio_crisis_count:             crisisC,
      bio_intervention_count:       interventionC,
      avg_containment_score:        Math.round(tCont / n * 10) / 10,
      avg_proliferation_score:      Math.round(tProl / n * 10) / 10,
      avg_governance_score:         Math.round(tGov  / n * 10) / 10,
      avg_preparedness_score:       Math.round(tPrep / n * 10) / 10,
      avg_estimated_bio_risk_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "synthetic-biology-risk-engine")));
  }

  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/synthetic-biology-risk-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    return sealResponse(NextResponse.json(sealResponse(await res.json(), "synthetic-biology-risk-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream biosecurity intelligence unavailable" }, "synthetic-biology-risk-engine"),
      { status: 502 }
    ));
  }
}
