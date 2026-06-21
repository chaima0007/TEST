import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // PME-001 — critical, clinical_trial_access_barrier (clinical_trial_access>0.85, research_funding_barrier>0.80)
  {
    id: "PME-001", substance_category: "psilocybine", region: "NOAM",
    clinical_evidence_gap: 0.90, fda_scheduling_barrier: 0.75,
    insurance_coverage_exclusion: 0.85, therapist_training_deficit: 0.80,
    clinical_trial_access: 0.92, indigenous_knowledge_theft: 0.60,
    commercialization_monopoly_risk: 0.65, harm_reduction_suppression: 0.72,
    mental_health_treatment_gap: 0.85, war_on_drugs_incarceration: 0.75,
    racial_disparity_enforcement: 0.78, decriminalization_policy_gap: 0.70,
    patient_access_equity: 0.70, research_funding_barrier: 0.88,
    synthetic_analogues_risk: 0.65, underground_session_risk: 0.65,
    informed_consent_gap: 0.82,
  },
  // PME-002 — critical, regulatory_scheduling_blockade (fda_scheduling_barrier>0.85, decriminalization_policy_gap>0.80)
  {
    id: "PME-002", substance_category: "mdma", region: "EMEA",
    clinical_evidence_gap: 0.78, fda_scheduling_barrier: 0.92,
    insurance_coverage_exclusion: 0.75, therapist_training_deficit: 0.72,
    clinical_trial_access: 0.80, indigenous_knowledge_theft: 0.55,
    commercialization_monopoly_risk: 0.60, harm_reduction_suppression: 0.75,
    mental_health_treatment_gap: 0.80, war_on_drugs_incarceration: 0.70,
    racial_disparity_enforcement: 0.72, decriminalization_policy_gap: 0.88,
    patient_access_equity: 0.68, research_funding_barrier: 0.75,
    synthetic_analogues_risk: 0.60, underground_session_risk: 0.60,
    informed_consent_gap: 0.70,
  },
  // PME-003 — critical, harm_reduction_policy_failure (harm_reduction_suppression>0.80, underground_session_risk>0.75)
  {
    id: "PME-003", substance_category: "ketamine", region: "LATAM",
    clinical_evidence_gap: 0.82, fda_scheduling_barrier: 0.78,
    insurance_coverage_exclusion: 0.78, therapist_training_deficit: 0.75,
    clinical_trial_access: 0.80, indigenous_knowledge_theft: 0.55,
    commercialization_monopoly_risk: 0.60, harm_reduction_suppression: 0.88,
    mental_health_treatment_gap: 0.82, war_on_drugs_incarceration: 0.72,
    racial_disparity_enforcement: 0.75, decriminalization_policy_gap: 0.72,
    patient_access_equity: 0.68, research_funding_barrier: 0.78,
    synthetic_analogues_risk: 0.60, underground_session_risk: 0.85,
    informed_consent_gap: 0.75,
  },
  // PME-004 — high, commercialization_equity_gap (commercialization_monopoly_risk>0.85, insurance_coverage_exclusion>0.80)
  {
    id: "PME-004", substance_category: "ayahuasca", region: "APAC",
    clinical_evidence_gap: 0.50, fda_scheduling_barrier: 0.48,
    insurance_coverage_exclusion: 0.88, therapist_training_deficit: 0.45,
    clinical_trial_access: 0.50, indigenous_knowledge_theft: 0.45,
    commercialization_monopoly_risk: 0.90, harm_reduction_suppression: 0.45,
    mental_health_treatment_gap: 0.52, war_on_drugs_incarceration: 0.45,
    racial_disparity_enforcement: 0.50, decriminalization_policy_gap: 0.45,
    patient_access_equity: 0.45, research_funding_barrier: 0.48,
    synthetic_analogues_risk: 0.45, underground_session_risk: 0.45,
    informed_consent_gap: 0.45,
  },
  // PME-005 — high, indigenous_knowledge_appropriation (indigenous_knowledge_theft>0.80, commercialization_monopoly_risk>0.75)
  {
    id: "PME-005", substance_category: "ibogaine", region: "SSA",
    clinical_evidence_gap: 0.48, fda_scheduling_barrier: 0.45,
    insurance_coverage_exclusion: 0.45, therapist_training_deficit: 0.42,
    clinical_trial_access: 0.48, indigenous_knowledge_theft: 0.88,
    commercialization_monopoly_risk: 0.82, harm_reduction_suppression: 0.42,
    mental_health_treatment_gap: 0.50, war_on_drugs_incarceration: 0.45,
    racial_disparity_enforcement: 0.48, decriminalization_policy_gap: 0.42,
    patient_access_equity: 0.42, research_funding_barrier: 0.45,
    synthetic_analogues_risk: 0.42, underground_session_risk: 0.42,
    informed_consent_gap: 0.42,
  },
  // PME-006 — moderate, none
  {
    id: "PME-006", substance_category: "lsd", region: "EMEA",
    clinical_evidence_gap: 0.28, fda_scheduling_barrier: 0.28,
    insurance_coverage_exclusion: 0.30, therapist_training_deficit: 0.25,
    clinical_trial_access: 0.28, indigenous_knowledge_theft: 0.25,
    commercialization_monopoly_risk: 0.25, harm_reduction_suppression: 0.25,
    mental_health_treatment_gap: 0.30, war_on_drugs_incarceration: 0.28,
    racial_disparity_enforcement: 0.30, decriminalization_policy_gap: 0.25,
    patient_access_equity: 0.25, research_funding_barrier: 0.30,
    synthetic_analogues_risk: 0.25, underground_session_risk: 0.25,
    informed_consent_gap: 0.25,
  },
  // PME-007 — low, none
  {
    id: "PME-007", substance_category: "mescaline", region: "NOAM",
    clinical_evidence_gap: 0.10, fda_scheduling_barrier: 0.10,
    insurance_coverage_exclusion: 0.12, therapist_training_deficit: 0.08,
    clinical_trial_access: 0.10, indigenous_knowledge_theft: 0.08,
    commercialization_monopoly_risk: 0.08, harm_reduction_suppression: 0.08,
    mental_health_treatment_gap: 0.10, war_on_drugs_incarceration: 0.10,
    racial_disparity_enforcement: 0.12, decriminalization_policy_gap: 0.08,
    patient_access_equity: 0.08, research_funding_barrier: 0.12,
    synthetic_analogues_risk: 0.08, underground_session_risk: 0.08,
    informed_consent_gap: 0.08,
  },
  // PME-008 — low, none
  {
    id: "PME-008", substance_category: "dmt", region: "APAC",
    clinical_evidence_gap: 0.12, fda_scheduling_barrier: 0.12,
    insurance_coverage_exclusion: 0.10, therapist_training_deficit: 0.10,
    clinical_trial_access: 0.12, indigenous_knowledge_theft: 0.10,
    commercialization_monopoly_risk: 0.10, harm_reduction_suppression: 0.10,
    mental_health_treatment_gap: 0.12, war_on_drugs_incarceration: 0.12,
    racial_disparity_enforcement: 0.10, decriminalization_policy_gap: 0.10,
    patient_access_equity: 0.10, research_funding_barrier: 0.10,
    synthetic_analogues_risk: 0.10, underground_session_risk: 0.10,
    informed_consent_gap: 0.10,
  },
];

type PMEInput = (typeof MOCK_ENTITIES)[0];

function clinicalScore(e: PMEInput): number {
  return Math.round((e.clinical_evidence_gap * 0.4 + e.research_funding_barrier * 0.35 + e.informed_consent_gap * 0.25) * 100 * 100) / 100;
}
function accessScore(e: PMEInput): number {
  return Math.round((e.clinical_trial_access * 0.4 + e.insurance_coverage_exclusion * 0.35 + e.therapist_training_deficit * 0.25) * 100 * 100) / 100;
}
function regulatoryScore(e: PMEInput): number {
  return Math.round((e.fda_scheduling_barrier * 0.4 + e.decriminalization_policy_gap * 0.35 + e.harm_reduction_suppression * 0.25) * 100 * 100) / 100;
}
function equityScore(e: PMEInput): number {
  return Math.round((e.racial_disparity_enforcement * 0.4 + e.war_on_drugs_incarceration * 0.35 + e.patient_access_equity * 0.25) * 100 * 100) / 100;
}
function compositeScore(cli: number, acc: number, reg: number, eq: number): number {
  return Math.round((cli * 0.30 + acc * 0.25 + reg * 0.25 + eq * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function psychedelicPattern(e: PMEInput): string {
  if (e.clinical_trial_access > 0.85 && e.research_funding_barrier > 0.80) return "clinical_trial_access_barrier";
  if (e.fda_scheduling_barrier > 0.85 && e.decriminalization_policy_gap > 0.80) return "regulatory_scheduling_blockade";
  if (e.commercialization_monopoly_risk > 0.85 && e.insurance_coverage_exclusion > 0.80) return "commercialization_equity_gap";
  if (e.indigenous_knowledge_theft > 0.80 && e.commercialization_monopoly_risk > 0.75) return "indigenous_knowledge_appropriation";
  if (e.harm_reduction_suppression > 0.80 && e.underground_session_risk > 0.75) return "harm_reduction_policy_failure";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_médecine_psychédélique_systémique";
  if (composite >= 40) return "blocage_réforme_politique_drogues_majeur";
  if (composite >= 20) return "inégalité_accès_thérapies_psychédéliques";
  return "surveillance_réforme_politique_drogues";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_réforme_politique_drogues_critique";
  if (risk === "high") return "accélération_déprogrammation_accès_essais_cliniques";
  if (risk === "moderate") return "renforcement_politiques_médecine_psychédélique";
  return "veille_réforme_drogues_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise médecine psychédélique systémique — réforme politique drogues en péril";
  if (risk === "high") return "🟠 Blocage réforme politique drogues majeur détecté";
  if (risk === "moderate") return "🟡 Inégalité accès thérapies psychédéliques active";
  return "🟢 Surveillance réforme politique drogues";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const cli  = clinicalScore(e);
      const acc  = accessScore(e);
      const reg  = regulatoryScore(e);
      const eq   = equityScore(e);
      const comp = compositeScore(cli, acc, reg, eq);
      const risk = riskLevel(comp);
      const pat  = psychedelicPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:                       e.entity_id,
        substance_category:              e.substance_category,
        region:                          e.region,
        clinical_score:                  cli,
        access_score:                    acc,
        regulatory_score:                reg,
        equity_score:                    eq,
        composite_score:                 comp,
        risk_level:                      risk,
        psychedelic_pattern:             pat,
        severity:                        sev,
        recommended_action:              action,
        signal:                          sig,
        clinical_trial_access:           e.clinical_trial_access,
        racial_disparity_enforcement:    e.racial_disparity_enforcement,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tCli = 0, tAcc = 0, tReg = 0, tEq = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.psychedelic_pattern] = (pattern_distribution[ent.psychedelic_pattern] || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tCli  += ent.clinical_score;
      tAcc  += ent.access_score;
      tReg  += ent.regulatory_score;
      tEq   += ent.equity_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite  = Math.round(tComp / n * 10) / 10;
    const avgClinical   = Math.round(tCli  / n * 10) / 10;

    const summary = {
      module_id:                          437,
      module_name:                        "Médecine Psychédélique & Réforme Politique des Drogues Intelligence Engine",
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
      avg_estimated_drug_reform_index:    Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, avg_clinical: avgClinical }, "psychedelic-medicine-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/psychedelic-medicine-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "psychedelic-medicine-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "psychedelic-medicine-engine"),
      { status: 502 }
    );
  }
}
