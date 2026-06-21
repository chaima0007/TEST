import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // NRE-001 — critical, mental_surveillance_state (neural_data>0.85, mental_health_surv>0.80)
  {
    id: "NRE-001", neurotechnology_type: "bci_consumer", region: "APAC",
    neural_data_collection: 0.92, mental_privacy_protection: 0.10,
    cognitive_manipulation_risk: 0.72, bci_corporate_control: 0.70,
    informed_consent_quality: 0.12, algorithmic_thought_influence: 0.68,
    emotion_detection_deployment: 0.88, memory_augmentation_inequality: 0.70,
    mental_health_surveillance: 0.88, neuro_data_commercialization: 0.75,
    regulatory_framework_gap: 0.80, equity_of_enhancement_access: 0.15,
    cross_border_data_flow: 0.85, re_identification_risk: 0.78,
    military_application_risk: 0.65, therapeutic_vs_enhancement_boundary: 0.60,
    judicial_neural_evidence: 0.70,
  },
  // NRE-002 — critical, cognitive_manipulation_crisis (cog_manip>0.85, algo_thought>0.80)
  {
    id: "NRE-002", neurotechnology_type: "neurofeedback_platform", region: "NOAM",
    neural_data_collection: 0.65, mental_privacy_protection: 0.15,
    cognitive_manipulation_risk: 0.90, bci_corporate_control: 0.72,
    informed_consent_quality: 0.10, algorithmic_thought_influence: 0.88,
    emotion_detection_deployment: 0.80, memory_augmentation_inequality: 0.68,
    mental_health_surveillance: 0.72, neuro_data_commercialization: 0.78,
    regulatory_framework_gap: 0.82, equity_of_enhancement_access: 0.18,
    cross_border_data_flow: 0.78, re_identification_risk: 0.68,
    military_application_risk: 0.60, therapeutic_vs_enhancement_boundary: 0.65,
    judicial_neural_evidence: 0.62,
  },
  // NRE-003 — critical, neural_data_commodification (neuro_data_comm>0.85, re_id>0.80)
  {
    id: "NRE-003", neurotechnology_type: "emotion_detection_ai", region: "EMEA",
    neural_data_collection: 0.78, mental_privacy_protection: 0.12,
    cognitive_manipulation_risk: 0.75, bci_corporate_control: 0.68,
    informed_consent_quality: 0.08, algorithmic_thought_influence: 0.72,
    emotion_detection_deployment: 0.92, memory_augmentation_inequality: 0.72,
    mental_health_surveillance: 0.75, neuro_data_commercialization: 0.88,
    regulatory_framework_gap: 0.80, equity_of_enhancement_access: 0.12,
    cross_border_data_flow: 0.88, re_identification_risk: 0.85,
    military_application_risk: 0.62, therapeutic_vs_enhancement_boundary: 0.58,
    judicial_neural_evidence: 0.68,
  },
  // NRE-004 — high, bci_corporate_monopoly (bci_corp>0.80, reg_gap>0.75)
  {
    id: "NRE-004", neurotechnology_type: "deep_brain_stimulation", region: "LATAM",
    neural_data_collection: 0.55, mental_privacy_protection: 0.30,
    cognitive_manipulation_risk: 0.52, bci_corporate_control: 0.85,
    informed_consent_quality: 0.35, algorithmic_thought_influence: 0.48,
    emotion_detection_deployment: 0.50, memory_augmentation_inequality: 0.52,
    mental_health_surveillance: 0.50, neuro_data_commercialization: 0.55,
    regulatory_framework_gap: 0.80, equity_of_enhancement_access: 0.30,
    cross_border_data_flow: 0.55, re_identification_risk: 0.48,
    military_application_risk: 0.45, therapeutic_vs_enhancement_boundary: 0.55,
    judicial_neural_evidence: 0.48,
  },
  // NRE-005 — high, brain_enhancement_inequality (mem_aug>0.80, equity_access<0.25)
  {
    id: "NRE-005", neurotechnology_type: "cognitive_enhancement_implant", region: "SSA",
    neural_data_collection: 0.48, mental_privacy_protection: 0.35,
    cognitive_manipulation_risk: 0.50, bci_corporate_control: 0.55,
    informed_consent_quality: 0.30, algorithmic_thought_influence: 0.45,
    emotion_detection_deployment: 0.48, memory_augmentation_inequality: 0.85,
    mental_health_surveillance: 0.48, neuro_data_commercialization: 0.52,
    regulatory_framework_gap: 0.70, equity_of_enhancement_access: 0.10,
    cross_border_data_flow: 0.50, re_identification_risk: 0.45,
    military_application_risk: 0.55, therapeutic_vs_enhancement_boundary: 0.48,
    judicial_neural_evidence: 0.42,
  },
  // NRE-006 — moderate, none
  {
    id: "NRE-006", neurotechnology_type: "eeg_wellness", region: "EMEA",
    neural_data_collection: 0.30, mental_privacy_protection: 0.60,
    cognitive_manipulation_risk: 0.28, bci_corporate_control: 0.32,
    informed_consent_quality: 0.65, algorithmic_thought_influence: 0.28,
    emotion_detection_deployment: 0.30, memory_augmentation_inequality: 0.30,
    mental_health_surveillance: 0.28, neuro_data_commercialization: 0.30,
    regulatory_framework_gap: 0.35, equity_of_enhancement_access: 0.55,
    cross_border_data_flow: 0.30, re_identification_risk: 0.28,
    military_application_risk: 0.25, therapeutic_vs_enhancement_boundary: 0.30,
    judicial_neural_evidence: 0.25,
  },
  // NRE-007 — low, none
  {
    id: "NRE-007", neurotechnology_type: "non_invasive_tms", region: "NOAM",
    neural_data_collection: 0.10, mental_privacy_protection: 0.88,
    cognitive_manipulation_risk: 0.10, bci_corporate_control: 0.12,
    informed_consent_quality: 0.90, algorithmic_thought_influence: 0.10,
    emotion_detection_deployment: 0.10, memory_augmentation_inequality: 0.12,
    mental_health_surveillance: 0.10, neuro_data_commercialization: 0.10,
    regulatory_framework_gap: 0.12, equity_of_enhancement_access: 0.82,
    cross_border_data_flow: 0.10, re_identification_risk: 0.10,
    military_application_risk: 0.08, therapeutic_vs_enhancement_boundary: 0.12,
    judicial_neural_evidence: 0.10,
  },
  // NRE-008 — low, none
  {
    id: "NRE-008", neurotechnology_type: "therapeutic_neuroprosthetic", region: "APAC",
    neural_data_collection: 0.12, mental_privacy_protection: 0.85,
    cognitive_manipulation_risk: 0.12, bci_corporate_control: 0.10,
    informed_consent_quality: 0.88, algorithmic_thought_influence: 0.12,
    emotion_detection_deployment: 0.12, memory_augmentation_inequality: 0.10,
    mental_health_surveillance: 0.12, neuro_data_commercialization: 0.12,
    regulatory_framework_gap: 0.10, equity_of_enhancement_access: 0.85,
    cross_border_data_flow: 0.12, re_identification_risk: 0.10,
    military_application_risk: 0.10, therapeutic_vs_enhancement_boundary: 0.08,
    judicial_neural_evidence: 0.12,
  },
];

type NREInput = typeof MOCK_ENTITIES[0];

function mentalPrivacyScore(e: NREInput): number {
  return Math.round((e.neural_data_collection * 0.4 + e.mental_health_surveillance * 0.35 + e.re_identification_risk * 0.25) * 100 * 100) / 100;
}
function cognitiveLibertyScore(e: NREInput): number {
  return Math.round((e.cognitive_manipulation_risk * 0.4 + e.algorithmic_thought_influence * 0.35 + e.bci_corporate_control * 0.25) * 100 * 100) / 100;
}
function consentScore(e: NREInput): number {
  return Math.round(((1 - e.informed_consent_quality) * 0.4 + e.regulatory_framework_gap * 0.35 + e.neuro_data_commercialization * 0.25) * 100 * 100) / 100;
}
function equityScore(e: NREInput): number {
  return Math.round((e.memory_augmentation_inequality * 0.4 + (1 - e.equity_of_enhancement_access) * 0.35 + e.military_application_risk * 0.25) * 100 * 100) / 100;
}
function compositeScore(priv: number, lib: number, con: number, equ: number): number {
  return Math.round((priv * 0.30 + lib * 0.25 + con * 0.25 + equ * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function neuroPattern(e: NREInput): string {
  if (e.neural_data_collection > 0.85 && e.mental_health_surveillance > 0.80) return "mental_surveillance_state";
  if (e.cognitive_manipulation_risk > 0.85 && e.algorithmic_thought_influence > 0.80) return "cognitive_manipulation_crisis";
  if (e.neuro_data_commercialization > 0.85 && e.re_identification_risk > 0.80) return "neural_data_commodification";
  if (e.bci_corporate_control > 0.80 && e.regulatory_framework_gap > 0.75) return "bci_corporate_monopoly";
  if (e.memory_augmentation_inequality > 0.80 && e.equity_of_enhancement_access < 0.25) return "brain_enhancement_inequality";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_neurodroits_systémique";
  if (composite >= 40) return "crise_souveraineté_cérébrale_majeure";
  if (composite >= 20) return "inégalité_neuro_structurelle";
  return "neurodroits_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_protection_neurodroits";
  if (risk === "high") return "régulation_neurotechnologies_accélérée";
  if (risk === "moderate") return "renforcement_cadre_consentement_neuronal";
  return "veille_neurodroits_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise neurodroits systémique — souveraineté cérébrale en péril";
  if (risk === "high") return "🟠 Crise souveraineté cérébrale majeure détectée";
  if (risk === "moderate") return "🟡 Inégalité neuro structurelle active";
  return "🟢 Neurodroits sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const priv = mentalPrivacyScore(e);
      const lib  = cognitiveLibertyScore(e);
      const con  = consentScore(e);
      const equ  = equityScore(e);
      const comp = compositeScore(priv, lib, con, equ);
      const risk = riskLevel(comp);
      const pat  = neuroPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:                  e.entity_id,
        neurotechnology_type:       e.neurotechnology_type,
        region:                     e.region,
        mental_privacy_score:       priv,
        cognitive_liberty_score:    lib,
        consent_score:              con,
        equity_score:               equ,
        composite_score:            comp,
        risk_level:                 risk,
        neuro_pattern:              pat,
        severity:                   sev,
        recommended_action:         action,
        signal:                     sig,
        neural_data_collection:     e.neural_data_collection,
        cognitive_manipulation_risk: e.cognitive_manipulation_risk,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tPriv = 0, tLib = 0, tCon = 0, tEqu = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.neuro_pattern]     = (pattern_distribution[ent.neuro_pattern]     || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tPriv += ent.mental_privacy_score;
      tLib  += ent.cognitive_liberty_score;
      tCon  += ent.consent_score;
      tEqu  += ent.equity_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite    = Math.round(tComp / n * 10) / 10;
    const avgMentalPrivacy = Math.round(tPriv / n * 10) / 10;

    const summary = {
      module_id:                          416,
      module_name:                        "Neurodroits & Souveraineté Données Cérébrales Intelligence Engine",
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
      avg_estimated_neuro_rights_index:   Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, avg_mental_privacy: avgMentalPrivacy }, "neuro-rights-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/neuro-rights-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "neuro-rights-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream indisponible", code: 502 }, "neuro-rights-engine"),
      { status: 502 }
    );
  }
}
