import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// 8 mock entities covering all 5 patterns and all 4 risk levels
// AJE-001: critical, racial_algorithm_bias     (recidivism>=0.70, systemic_racism>=0.65, composite>=60)
// AJE-002: low, no pattern                     (all low, composite<20)
// AJE-003: high, justice_opacity_crisis        (opacity>=0.70, due_process>=0.65, composite>=40 <60)
// AJE-004: low, no pattern                     (all low, composite<20)
// AJE-005: critical, predictive_persecution    (policing>=0.70, pretrial>=0.65, composite>=60)
// AJE-006: moderate, no pattern                (composite>=20 <40)
// AJE-007: high, poverty_discrimination_cascade (poverty>=0.70, legal_rep>=0.65, composite>=40 <60)
// AJE-008: critical, wrongful_AI_conviction    (wrongful>=0.70, facial_err>=0.65, composite>=60)

const mockEntities = [
  {
    entity_id: "AJE-001",
    justice_domain: "criminal_sentencing",
    region: "NAMER",
    recidivism_AI_racial_bias_index: 0.85,
    pretrial_detention_algorithmic_amplification: 0.60,
    sentencing_AI_disparity_rate: 0.80,
    parole_AI_discrimination_index: 0.70,
    predictive_policing_racial_profiling: 0.75,
    facial_recognition_justice_error_rate: 0.55,
    algorithmic_opacity_in_courts: 0.60,
    AI_due_process_violation_rate: 0.55,
    criminal_justice_AI_accountability_gap: 0.50,
    poverty_AI_bias_amplification: 0.55,
    immigration_AI_detention_bias: 0.50,
    data_quality_justice_impact: 0.60,
    AI_legal_representation_inequality: 0.50,
    wrongful_conviction_AI_contribution: 0.60,
    justice_outcome_wealth_AI_correlation: 0.50,
    AI_rehabilitation_assessment_bias: 0.65,
    systemic_racism_AI_reproduction: 0.78,
    // computed
    bias_score: 80.75,
    opacity_score: 55.75,
    discrimination_score: 52.0,
    systemic_score: 65.95,
    composite_score: 64.35,
    risk_level: "critical",
    justice_pattern: "racial_algorithm_bias",
    severity: "injustice_algorithmique_systémique",
    recommended_action: "réforme_urgente_justice_algorithmique",
    signal: "🔴 Injustice algorithmique systémique — biais judiciaire IA critique",
  },
  {
    entity_id: "AJE-002",
    justice_domain: "parole_review",
    region: "EMEA",
    recidivism_AI_racial_bias_index: 0.08,
    pretrial_detention_algorithmic_amplification: 0.07,
    sentencing_AI_disparity_rate: 0.06,
    parole_AI_discrimination_index: 0.05,
    predictive_policing_racial_profiling: 0.05,
    facial_recognition_justice_error_rate: 0.03,
    algorithmic_opacity_in_courts: 0.07,
    AI_due_process_violation_rate: 0.06,
    criminal_justice_AI_accountability_gap: 0.05,
    poverty_AI_bias_amplification: 0.06,
    immigration_AI_detention_bias: 0.04,
    data_quality_justice_impact: 0.05,
    AI_legal_representation_inequality: 0.05,
    wrongful_conviction_AI_contribution: 0.04,
    justice_outcome_wealth_AI_correlation: 0.04,
    AI_rehabilitation_assessment_bias: 0.06,
    systemic_racism_AI_reproduction: 0.05,
    // computed
    bias_score: 6.55,
    opacity_score: 6.15,
    discrimination_score: 5.15,
    systemic_score: 4.15,
    composite_score: 5.62,
    risk_level: "low",
    justice_pattern: "none",
    severity: "biais_algorithmique_contenu",
    recommended_action: "veille_biais_judiciaire_IA",
    signal: "🟢 Biais algorithmique judiciaire contenu",
  },
  {
    entity_id: "AJE-003",
    justice_domain: "court_decision_systems",
    region: "APAC",
    recidivism_AI_racial_bias_index: 0.40,
    pretrial_detention_algorithmic_amplification: 0.38,
    sentencing_AI_disparity_rate: 0.35,
    parole_AI_discrimination_index: 0.32,
    predictive_policing_racial_profiling: 0.30,
    facial_recognition_justice_error_rate: 0.25,
    algorithmic_opacity_in_courts: 0.80,
    AI_due_process_violation_rate: 0.75,
    criminal_justice_AI_accountability_gap: 0.60,
    poverty_AI_bias_amplification: 0.35,
    immigration_AI_detention_bias: 0.30,
    data_quality_justice_impact: 0.38,
    AI_legal_representation_inequality: 0.30,
    wrongful_conviction_AI_contribution: 0.28,
    justice_outcome_wealth_AI_correlation: 0.28,
    AI_rehabilitation_assessment_bias: 0.35,
    systemic_racism_AI_reproduction: 0.30,
    // computed
    bias_score: 35.75,
    opacity_score: 73.25,
    discrimination_score: 31.5,
    systemic_score: 28.05,
    composite_score: 42.52,
    risk_level: "high",
    justice_pattern: "justice_opacity_crisis",
    severity: "biais_judiciaire_IA_majeur",
    recommended_action: "audit_systémique_IA_judiciaire",
    signal: "🟠 Biais judiciaire IA majeur détecté",
  },
  {
    entity_id: "AJE-004",
    justice_domain: "immigration_enforcement",
    region: "LATAM",
    recidivism_AI_racial_bias_index: 0.07,
    pretrial_detention_algorithmic_amplification: 0.06,
    sentencing_AI_disparity_rate: 0.05,
    parole_AI_discrimination_index: 0.04,
    predictive_policing_racial_profiling: 0.04,
    facial_recognition_justice_error_rate: 0.05,
    algorithmic_opacity_in_courts: 0.06,
    AI_due_process_violation_rate: 0.05,
    criminal_justice_AI_accountability_gap: 0.04,
    poverty_AI_bias_amplification: 0.08,
    immigration_AI_detention_bias: 0.06,
    data_quality_justice_impact: 0.05,
    AI_legal_representation_inequality: 0.06,
    wrongful_conviction_AI_contribution: 0.03,
    justice_outcome_wealth_AI_correlation: 0.05,
    AI_rehabilitation_assessment_bias: 0.04,
    systemic_racism_AI_reproduction: 0.04,
    // computed
    bias_score: 5.55,
    opacity_score: 5.15,
    discrimination_score: 6.55,
    systemic_score: 3.9,
    composite_score: 5.37,
    risk_level: "low",
    justice_pattern: "none",
    severity: "biais_algorithmique_contenu",
    recommended_action: "veille_biais_judiciaire_IA",
    signal: "🟢 Biais algorithmique judiciaire contenu",
  },
  {
    entity_id: "AJE-005",
    justice_domain: "predictive_policing",
    region: "NAMER",
    recidivism_AI_racial_bias_index: 0.70,
    pretrial_detention_algorithmic_amplification: 0.78,
    sentencing_AI_disparity_rate: 0.65,
    parole_AI_discrimination_index: 0.60,
    predictive_policing_racial_profiling: 0.82,
    facial_recognition_justice_error_rate: 0.50,
    algorithmic_opacity_in_courts: 0.65,
    AI_due_process_violation_rate: 0.60,
    criminal_justice_AI_accountability_gap: 0.55,
    poverty_AI_bias_amplification: 0.55,
    immigration_AI_detention_bias: 0.50,
    data_quality_justice_impact: 0.58,
    AI_legal_representation_inequality: 0.50,
    wrongful_conviction_AI_contribution: 0.55,
    justice_outcome_wealth_AI_correlation: 0.50,
    AI_rehabilitation_assessment_bias: 0.62,
    systemic_racism_AI_reproduction: 0.60,
    // computed
    bias_score: 71.25,
    opacity_score: 60.75,
    discrimination_score: 52.0,
    systemic_score: 55.75,
    composite_score: 60.71,
    risk_level: "critical",
    justice_pattern: "predictive_persecution",
    severity: "injustice_algorithmique_systémique",
    recommended_action: "réforme_urgente_justice_algorithmique",
    signal: "🔴 Injustice algorithmique systémique — biais judiciaire IA critique",
  },
  {
    entity_id: "AJE-006",
    justice_domain: "bail_assessment",
    region: "EMEA",
    recidivism_AI_racial_bias_index: 0.28,
    pretrial_detention_algorithmic_amplification: 0.25,
    sentencing_AI_disparity_rate: 0.25,
    parole_AI_discrimination_index: 0.22,
    predictive_policing_racial_profiling: 0.22,
    facial_recognition_justice_error_rate: 0.15,
    algorithmic_opacity_in_courts: 0.24,
    AI_due_process_violation_rate: 0.22,
    criminal_justice_AI_accountability_gap: 0.20,
    poverty_AI_bias_amplification: 0.25,
    immigration_AI_detention_bias: 0.20,
    data_quality_justice_impact: 0.22,
    AI_legal_representation_inequality: 0.22,
    wrongful_conviction_AI_contribution: 0.18,
    justice_outcome_wealth_AI_correlation: 0.20,
    AI_rehabilitation_assessment_bias: 0.22,
    systemic_racism_AI_reproduction: 0.20,
    // computed
    bias_score: 25.45,
    opacity_score: 22.3,
    discrimination_score: 22.7,
    systemic_score: 18.05,
    composite_score: 22.5,
    risk_level: "moderate",
    justice_pattern: "none",
    severity: "discrimination_algorithmique_active",
    recommended_action: "renforcement_équité_algorithmique",
    signal: "🟡 Discrimination algorithmique active",
  },
  {
    entity_id: "AJE-007",
    justice_domain: "public_defense_allocation",
    region: "LATAM",
    recidivism_AI_racial_bias_index: 0.40,
    pretrial_detention_algorithmic_amplification: 0.38,
    sentencing_AI_disparity_rate: 0.38,
    parole_AI_discrimination_index: 0.35,
    predictive_policing_racial_profiling: 0.35,
    facial_recognition_justice_error_rate: 0.25,
    algorithmic_opacity_in_courts: 0.38,
    AI_due_process_violation_rate: 0.35,
    criminal_justice_AI_accountability_gap: 0.30,
    poverty_AI_bias_amplification: 0.80,
    immigration_AI_detention_bias: 0.55,
    data_quality_justice_impact: 0.45,
    AI_legal_representation_inequality: 0.72,
    wrongful_conviction_AI_contribution: 0.28,
    justice_outcome_wealth_AI_correlation: 0.60,
    AI_rehabilitation_assessment_bias: 0.42,
    systemic_racism_AI_reproduction: 0.30,
    // computed
    bias_score: 38.05,
    opacity_score: 34.95,
    discrimination_score: 72.2,
    systemic_score: 28.05,
    composite_score: 43.81,
    risk_level: "high",
    justice_pattern: "poverty_discrimination_cascade",
    severity: "biais_judiciaire_IA_majeur",
    recommended_action: "audit_systémique_IA_judiciaire",
    signal: "🟠 Biais judiciaire IA majeur détecté",
  },
  {
    entity_id: "AJE-008",
    justice_domain: "facial_recognition_courts",
    region: "APAC",
    recidivism_AI_racial_bias_index: 0.75,
    pretrial_detention_algorithmic_amplification: 0.62,
    sentencing_AI_disparity_rate: 0.70,
    parole_AI_discrimination_index: 0.65,
    predictive_policing_racial_profiling: 0.65,
    facial_recognition_justice_error_rate: 0.72,
    algorithmic_opacity_in_courts: 0.65,
    AI_due_process_violation_rate: 0.60,
    criminal_justice_AI_accountability_gap: 0.55,
    poverty_AI_bias_amplification: 0.55,
    immigration_AI_detention_bias: 0.50,
    data_quality_justice_impact: 0.60,
    AI_legal_representation_inequality: 0.50,
    wrongful_conviction_AI_contribution: 0.82,
    justice_outcome_wealth_AI_correlation: 0.50,
    AI_rehabilitation_assessment_bias: 0.68,
    systemic_racism_AI_reproduction: 0.78,
    // computed
    bias_score: 70.75,
    opacity_score: 60.75,
    discrimination_score: 52.0,
    systemic_score: 77.9,
    composite_score: 64.99,
    risk_level: "critical",
    justice_pattern: "wrongful_AI_conviction",
    severity: "injustice_algorithmique_systémique",
    recommended_action: "réforme_urgente_justice_algorithmique",
    signal: "🔴 Injustice algorithmique systémique — biais judiciaire IA critique",
  },
];

export async function GET(request: Request) {
  if (!SWARM_API_URL) {
    const { searchParams } = new URL(request.url);
    const risk    = searchParams.get("risk");
    const pattern = searchParams.get("pattern");

    let entities = [...mockEntities];
    if (risk)    entities = entities.filter((e) => e.risk_level === risk);
    if (pattern) entities = entities.filter((e) => e.justice_pattern === pattern);

    const risk_distribution:     Record<string, number> = {};
    const pattern_distribution:  Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution:   Record<string, number> = {};
    let total_composite    = 0;
    let total_recidivism   = 0;
    let critical_count     = 0;
    let high_count         = 0;
    let moderate_count     = 0;
    let low_count          = 0;

    for (const e of mockEntities) {
      risk_distribution[e.risk_level]       = (risk_distribution[e.risk_level] || 0) + 1;
      pattern_distribution[e.justice_pattern] = (pattern_distribution[e.justice_pattern] || 0) + 1;
      severity_distribution[e.severity]     = (severity_distribution[e.severity] || 0) + 1;
      action_distribution[e.recommended_action] = (action_distribution[e.recommended_action] || 0) + 1;
      total_composite  += e.composite_score;
      total_recidivism += e.recidivism_AI_racial_bias_index;
      if (e.risk_level === "critical")      critical_count++;
      else if (e.risk_level === "high")     high_count++;
      else if (e.risk_level === "moderate") moderate_count++;
      else                                  low_count++;
    }

    const n             = mockEntities.length;
    const avg_composite = Math.round((total_composite / n) * 100) / 100;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id:   346,
        module_name: "Algorithmic Justice & Criminal AI Bias Intelligence Engine",
        total_entities:   n,
        critical_count,
        high_count,
        moderate_count,
        low_count,
        avg_composite,
        pattern_distribution,
        risk_distribution,
        severity_distribution,
        action_distribution,
        avg_estimated_justice_bias_index: Math.round((avg_composite / 100 * 10) * 100) / 100,
        avg_recidivism_AI_racial_bias:    Math.round((total_recidivism / n) * 100) / 100,
      },
    } as Record<string, unknown>));
  }

  try {
    const { searchParams } = new URL(request.url);
    const url = new URL(`${SWARM_API_URL}/api/algorithmic-justice-engine`);
    const risk    = searchParams.get("risk");
    const pattern = searchParams.get("pattern");
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(await res.json());
  } catch {}

  return NextResponse.json(
    sealResponse({ entities: [], summary: {} } as Record<string, unknown>),
    { status: 502 },
  );
}
