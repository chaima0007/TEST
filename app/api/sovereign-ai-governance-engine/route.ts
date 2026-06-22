import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_SYSTEMS = [
  // SAG-001 critical alignment_failure
  {
    system_id: "SAG-001", ai_domain: "autonomous_agent", region: "EMEA",
    alignment_score: 0.18, explainability_score: 0.25, bias_audit_completeness: 0.20,
    human_oversight_level: 0.22, autonomous_decision_risk: 0.88, data_provenance_clarity: 0.28,
    model_drift_detection_capability: 0.20, adversarial_robustness_score: 0.18, regulatory_ai_compliance: 0.30,
    ethical_review_frequency: 0.15, model_transparency_index: 0.22, sovereignty_preservation_score: 0.25,
    algorithmic_accountability_score: 0.20, ai_rights_framework_clarity: 0.18, unintended_consequence_monitoring: 0.15,
    stakeholder_consent_coverage: 0.22, ai_incident_response_maturity: 0.18,
  },
  // SAG-002 low aligned
  {
    system_id: "SAG-002", ai_domain: "predictive_model", region: "NAMER",
    alignment_score: 0.92, explainability_score: 0.90, bias_audit_completeness: 0.88,
    human_oversight_level: 0.95, autonomous_decision_risk: 0.08, data_provenance_clarity: 0.92,
    model_drift_detection_capability: 0.90, adversarial_robustness_score: 0.88, regulatory_ai_compliance: 0.95,
    ethical_review_frequency: 0.92, model_transparency_index: 0.90, sovereignty_preservation_score: 0.92,
    algorithmic_accountability_score: 0.88, ai_rights_framework_clarity: 0.90, unintended_consequence_monitoring: 0.92,
    stakeholder_consent_coverage: 0.95, ai_incident_response_maturity: 0.90,
  },
  // SAG-003 high opacity_crisis
  {
    system_id: "SAG-003", ai_domain: "generative_llm", region: "APAC",
    alignment_score: 0.55, explainability_score: 0.18, bias_audit_completeness: 0.45,
    human_oversight_level: 0.50, autonomous_decision_risk: 0.55, data_provenance_clarity: 0.48,
    model_drift_detection_capability: 0.50, adversarial_robustness_score: 0.45, regulatory_ai_compliance: 0.58,
    ethical_review_frequency: 0.50, model_transparency_index: 0.20, sovereignty_preservation_score: 0.52,
    algorithmic_accountability_score: 0.45, ai_rights_framework_clarity: 0.48, unintended_consequence_monitoring: 0.50,
    stakeholder_consent_coverage: 0.52, ai_incident_response_maturity: 0.48,
  },
  // SAG-004 low monitored
  {
    system_id: "SAG-004", ai_domain: "computer_vision", region: "LATAM",
    alignment_score: 0.78, explainability_score: 0.75, bias_audit_completeness: 0.72,
    human_oversight_level: 0.80, autonomous_decision_risk: 0.20, data_provenance_clarity: 0.78,
    model_drift_detection_capability: 0.75, adversarial_robustness_score: 0.72, regulatory_ai_compliance: 0.80,
    ethical_review_frequency: 0.78, model_transparency_index: 0.75, sovereignty_preservation_score: 0.78,
    algorithmic_accountability_score: 0.72, ai_rights_framework_clarity: 0.75, unintended_consequence_monitoring: 0.78,
    stakeholder_consent_coverage: 0.80, ai_incident_response_maturity: 0.75,
  },
  // SAG-005 critical regulatory_breach
  {
    system_id: "SAG-005", ai_domain: "decision_engine", region: "EMEA",
    alignment_score: 0.42, explainability_score: 0.38, bias_audit_completeness: 0.22,
    human_oversight_level: 0.35, autonomous_decision_risk: 0.72, data_provenance_clarity: 0.30,
    model_drift_detection_capability: 0.28, adversarial_robustness_score: 0.30, regulatory_ai_compliance: 0.18,
    ethical_review_frequency: 0.20, model_transparency_index: 0.35, sovereignty_preservation_score: 0.38,
    algorithmic_accountability_score: 0.30, ai_rights_framework_clarity: 0.25, unintended_consequence_monitoring: 0.22,
    stakeholder_consent_coverage: 0.28, ai_incident_response_maturity: 0.25,
  },
  // SAG-006 moderate none
  {
    system_id: "SAG-006", ai_domain: "reinforcement_agent", region: "NAMER",
    alignment_score: 0.62, explainability_score: 0.60, bias_audit_completeness: 0.58,
    human_oversight_level: 0.65, autonomous_decision_risk: 0.38, data_provenance_clarity: 0.60,
    model_drift_detection_capability: 0.62, adversarial_robustness_score: 0.58, regulatory_ai_compliance: 0.65,
    ethical_review_frequency: 0.60, model_transparency_index: 0.62, sovereignty_preservation_score: 0.60,
    algorithmic_accountability_score: 0.58, ai_rights_framework_clarity: 0.62, unintended_consequence_monitoring: 0.60,
    stakeholder_consent_coverage: 0.65, ai_incident_response_maturity: 0.60,
  },
  // SAG-007 high sovereignty_erosion
  {
    system_id: "SAG-007", ai_domain: "swarm_intelligence", region: "MEA",
    alignment_score: 0.48, explainability_score: 0.45, bias_audit_completeness: 0.42,
    human_oversight_level: 0.22, autonomous_decision_risk: 0.62, data_provenance_clarity: 0.40,
    model_drift_detection_capability: 0.45, adversarial_robustness_score: 0.40, regulatory_ai_compliance: 0.48,
    ethical_review_frequency: 0.42, model_transparency_index: 0.45, sovereignty_preservation_score: 0.20,
    algorithmic_accountability_score: 0.42, ai_rights_framework_clarity: 0.38, unintended_consequence_monitoring: 0.40,
    stakeholder_consent_coverage: 0.42, ai_incident_response_maturity: 0.35,
  },
  // SAG-008 critical bias_amplification
  {
    system_id: "SAG-008", ai_domain: "biometric_system", region: "APAC",
    alignment_score: 0.30, explainability_score: 0.28, bias_audit_completeness: 0.15,
    human_oversight_level: 0.28, autonomous_decision_risk: 0.78, data_provenance_clarity: 0.22,
    model_drift_detection_capability: 0.25, adversarial_robustness_score: 0.22, regulatory_ai_compliance: 0.28,
    ethical_review_frequency: 0.22, model_transparency_index: 0.28, sovereignty_preservation_score: 0.25,
    algorithmic_accountability_score: 0.18, ai_rights_framework_clarity: 0.20, unintended_consequence_monitoring: 0.18,
    stakeholder_consent_coverage: 0.22, ai_incident_response_maturity: 0.20,
  },
];

type AISystem = typeof MOCK_SYSTEMS[0];

function inv(v: number): number { return 1 - v; }

function alignmentRiskScore(s: AISystem): number {
  return inv(s.alignment_score) * 0.40 + s.autonomous_decision_risk * 0.35 + inv(s.model_drift_detection_capability) * 0.25;
}
function transparencyScore(s: AISystem): number {
  return inv(s.explainability_score) * 0.40 + inv(s.model_transparency_index) * 0.35 + inv(s.algorithmic_accountability_score) * 0.25;
}
function complianceScore(s: AISystem): number {
  return inv(s.regulatory_ai_compliance) * 0.40 + inv(s.ethical_review_frequency) * 0.35 + inv(s.bias_audit_completeness) * 0.25;
}
function sovereigntyScore(s: AISystem): number {
  return inv(s.sovereignty_preservation_score) * 0.40 + inv(s.human_oversight_level) * 0.35 + inv(s.ai_incident_response_maturity) * 0.25;
}
function composite(al: number, tr: number, co: number, so: number): number {
  return Math.min(Math.round((al * 0.30 + tr * 0.25 + co * 0.25 + so * 0.20) * 100 * 100) / 100, 100);
}
function governancePattern(s: AISystem): string {
  if (s.alignment_score < 0.35 || s.autonomous_decision_risk > 0.70) return "alignment_failure";
  if (s.explainability_score < 0.30 && s.model_transparency_index < 0.30) return "opacity_crisis";
  if (s.regulatory_ai_compliance < 0.35 || s.bias_audit_completeness < 0.30) return "regulatory_breach";
  if (s.sovereignty_preservation_score < 0.35 || s.human_oversight_level < 0.30) return "sovereignty_erosion";
  if (s.bias_audit_completeness < 0.40 && s.algorithmic_accountability_score < 0.40) return "bias_amplification";
  return "none";
}
function riskLevel(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string  { if (c >= 60) return "misaligned"; if (c >= 40) return "at_risk"; if (c >= 20) return "monitored"; return "aligned"; }
function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") { return pattern === "alignment_failure" ? "emergency_shutdown" : "alignment_reset"; }
  if (risk === "high")     { return pattern === "bias_amplification" ? "bias_remediation" : "governance_audit"; }
  if (risk === "moderate") return "ai_monitoring";
  return "no_action";
}
function governanceSignal(s: AISystem, pattern: string, comp: number): string {
  if (comp < 20) return "Gouvernance IA exemplaire — alignement robuste, conformité souveraine assurée, contrôle humain effectif et transparence algorithmique validée";
  const labels: Record<string, string> = {
    alignment_failure:   "Échec d'alignement IA",
    opacity_crisis:      "Crise d'opacité algorithmique",
    regulatory_breach:   "Violation réglementaire IA",
    sovereignty_erosion: "Érosion de la souveraineté IA",
    bias_amplification:  "Amplification des biais",
  };
  const label = labels[pattern] ?? pattern.replace(/_/g, " ");
  return `${label} — alignement ${s.alignment_score.toFixed(2)} — conformité ${s.regulatory_ai_compliance.toFixed(2)} — explicabilité ${s.explainability_score.toFixed(2)} — souveraineté ${s.sovereignty_preservation_score.toFixed(2)} — risque autonome ${s.autonomous_decision_risk.toFixed(2)} — composite ${comp.toFixed(1)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[sovereign-ai-governance-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tAl=0, tTr=0, tCo=0, tSo=0, tComp=0, tGap=0, misCount=0, intCount=0;
    for (const sys of systems) {
      rc[sys.governance_risk]    = (rc[sys.governance_risk]    || 0) + 1;
      pc[sys.governance_pattern] = (pc[sys.governance_pattern] || 0) + 1;
      sc[sys.governance_severity]= (sc[sys.governance_severity]|| 0) + 1;
      ac[sys.recommended_action] = (ac[sys.recommended_action] || 0) + 1;
      tAl   += sys.alignment_risk_score;
      tTr   += sys.transparency_score;
      tCo   += sys.compliance_score;
      tSo   += sys.sovereignty_score;
      tComp += sys.governance_composite;
      tGap  += sys.estimated_misalignment_severity_index;
      if (sys.has_misalignment_signal)         misCount++;
      if (sys.requires_immediate_intervention) intCount++;
    }
    const n = systems.length;

    return sealResponse(NextResponse.json(sealResponse({
      systems,
      summary: {
        total:                                      n,
        risk_counts:                                rc,
        pattern_counts:                             pc,
        severity_counts:                            sc,
        action_counts:                              ac,
        avg_governance_composite:                   Math.round(tComp / n * 10) / 10,
        misalignment_signal_count:                  misCount,
        immediate_intervention_count:               intCount,
        avg_alignment_risk_score:                   Math.round(tAl / n * 10) / 10,
        avg_transparency_score:                     Math.round(tTr / n * 10) / 10,
        avg_compliance_score:                       Math.round(tCo / n * 10) / 10,
        avg_sovereignty_score:                      Math.round(tSo / n * 10) / 10,
        avg_estimated_misalignment_severity_index:  Math.round(tGap / n * 100) / 100,
      },
    }, "sovereign-ai-governance-engine")));
  }

  return sealResponse(NextResponse.json(sealResponse(
    await (await fetch(`${process.env.SWARM_API_URL}/sovereign-ai-governance-engine`, { next: { revalidate: 30 } })).json(),
    "sovereign-ai-governance-engine"
  )));
}
