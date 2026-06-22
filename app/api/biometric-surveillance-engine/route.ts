import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[biometric-surveillance-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

// 8 mock entities covering all 5 patterns and all 4 risk levels
// BSE-001: critical, total_biometric_state  (facial>=0.70, infra>=0.65, composite>=60)
// BSE-002: low, no pattern                  (all low, composite<20)
// BSE-003: high, genetic_panopticon         (DNA>=0.70, consent_violation>=0.65, composite>=40 <60)
// BSE-004: low, no pattern                  (all low, composite<20)
// BSE-005: critical, predictive_persecution (policing_bias>=0.70, persecution>=0.65, composite>=60)
// BSE-006: moderate, no pattern             (composite>=20 <40)
// BSE-007: high, identity_monopoly          (commercialization>=0.70, cross_border>=0.65, composite>=40 <60)
// BSE-008: critical, biometric_apartheid    (apartheid_risk>=0.70, suppression>=0.65, composite>=60)

const mockEntities = [
  {
    id: "BSE-001",
    surveillance_domain: "urban_security",
    region: "APAC",
    facial_recognition_deployment_density: 0.85,
    behavioral_biometric_collection_rate: 0.80,
    DNA_database_expansion_rate: 0.55,
    biometric_data_commercialization_risk: 0.55,
    cross_border_biometric_sharing_level: 0.50,
    biometric_error_rate_impact: 0.60,
    surveillance_infrastructure_concentration: 0.78,
    biometric_consent_violation_index: 0.60,
    predictive_policing_bias: 0.55,
    emotion_recognition_deployment: 0.65,
    voice_print_mass_collection: 0.70,
    gait_analysis_deployment: 0.75,
    biometric_resistance_suppression: 0.60,
    identity_theft_systemic_risk: 0.50,
    biometric_political_persecution_risk: 0.55,
    permanent_record_creation_rate: 0.65,
    biometric_apartheid_risk: 0.45,
    // computed
    deployment_score: 80.25,
    violation_score: 61.25,
    control_score: 72.45,
    persecution_score: 60.25,
    composite_score: 69.51,
    risk_level: "critical",
    surveillance_pattern: "total_biometric_state",
    severity: "état_surveillance_total",
    recommended_action: "résistance_biométrique_urgente",
    signal: "🔴 État de surveillance totale — contrôle biométrique systémique",
  },
  {
    id: "BSE-002",
    surveillance_domain: "border_control",
    region: "EMEA",
    facial_recognition_deployment_density: 0.10,
    behavioral_biometric_collection_rate: 0.08,
    DNA_database_expansion_rate: 0.05,
    biometric_data_commercialization_risk: 0.07,
    cross_border_biometric_sharing_level: 0.06,
    biometric_error_rate_impact: 0.04,
    surveillance_infrastructure_concentration: 0.08,
    biometric_consent_violation_index: 0.06,
    predictive_policing_bias: 0.05,
    emotion_recognition_deployment: 0.04,
    voice_print_mass_collection: 0.03,
    gait_analysis_deployment: 0.05,
    biometric_resistance_suppression: 0.04,
    identity_theft_systemic_risk: 0.05,
    biometric_political_persecution_risk: 0.03,
    permanent_record_creation_rate: 0.04,
    biometric_apartheid_risk: 0.02,
    // computed
    deployment_score: 8.0,
    violation_score: 5.6,
    control_score: 6.65,
    persecution_score: 4.1,
    composite_score: 6.34,
    risk_level: "low",
    surveillance_pattern: "none",
    severity: "surveillance_contenue",
    recommended_action: "veille_biométrique_continue",
    signal: "🟢 Surveillance biométrique contenue",
  },
  {
    id: "BSE-003",
    surveillance_domain: "law_enforcement",
    region: "NAMER",
    facial_recognition_deployment_density: 0.45,
    behavioral_biometric_collection_rate: 0.40,
    DNA_database_expansion_rate: 0.78,
    biometric_data_commercialization_risk: 0.50,
    cross_border_biometric_sharing_level: 0.45,
    biometric_error_rate_impact: 0.40,
    surveillance_infrastructure_concentration: 0.42,
    biometric_consent_violation_index: 0.72,
    predictive_policing_bias: 0.38,
    emotion_recognition_deployment: 0.30,
    voice_print_mass_collection: 0.35,
    gait_analysis_deployment: 0.30,
    biometric_resistance_suppression: 0.38,
    identity_theft_systemic_risk: 0.35,
    biometric_political_persecution_risk: 0.30,
    permanent_record_creation_rate: 0.40,
    biometric_apartheid_risk: 0.25,
    // computed
    deployment_score: 40.0,
    violation_score: 62.3,
    control_score: 41.95,
    persecution_score: 34.75,
    composite_score: 45.74,
    risk_level: "high",
    surveillance_pattern: "genetic_panopticon",
    severity: "contrôle_biométrique_avancé",
    recommended_action: "régulation_biométrique_stricte",
    signal: "🟠 Contrôle biométrique avancé détecté",
  },
  {
    id: "BSE-004",
    surveillance_domain: "workplace_monitoring",
    region: "LATAM",
    facial_recognition_deployment_density: 0.12,
    behavioral_biometric_collection_rate: 0.10,
    DNA_database_expansion_rate: 0.08,
    biometric_data_commercialization_risk: 0.09,
    cross_border_biometric_sharing_level: 0.07,
    biometric_error_rate_impact: 0.06,
    surveillance_infrastructure_concentration: 0.10,
    biometric_consent_violation_index: 0.09,
    predictive_policing_bias: 0.07,
    emotion_recognition_deployment: 0.05,
    voice_print_mass_collection: 0.06,
    gait_analysis_deployment: 0.07,
    biometric_resistance_suppression: 0.05,
    identity_theft_systemic_risk: 0.06,
    biometric_political_persecution_risk: 0.04,
    permanent_record_creation_rate: 0.06,
    biometric_apartheid_risk: 0.03,
    // computed
    deployment_score: 9.95,
    violation_score: 7.85,
    control_score: 8.65,
    persecution_score: 4.65,
    composite_score: 7.92,
    risk_level: "low",
    surveillance_pattern: "none",
    severity: "surveillance_contenue",
    recommended_action: "veille_biométrique_continue",
    signal: "🟢 Surveillance biométrique contenue",
  },
  {
    id: "BSE-005",
    surveillance_domain: "political_monitoring",
    region: "MEA",
    facial_recognition_deployment_density: 0.60,
    behavioral_biometric_collection_rate: 0.55,
    DNA_database_expansion_rate: 0.50,
    biometric_data_commercialization_risk: 0.50,
    cross_border_biometric_sharing_level: 0.45,
    biometric_error_rate_impact: 0.55,
    surveillance_infrastructure_concentration: 0.58,
    biometric_consent_violation_index: 0.55,
    predictive_policing_bias: 0.82,
    emotion_recognition_deployment: 0.70,
    voice_print_mass_collection: 0.65,
    gait_analysis_deployment: 0.60,
    biometric_resistance_suppression: 0.62,
    identity_theft_systemic_risk: 0.55,
    biometric_political_persecution_risk: 0.78,
    permanent_record_creation_rate: 0.72,
    biometric_apartheid_risk: 0.55,
    // computed
    deployment_score: 60.5,
    violation_score: 54.5,
    control_score: 68.95,
    persecution_score: 74.45,
    composite_score: 64.36,
    risk_level: "critical",
    surveillance_pattern: "predictive_persecution",
    severity: "état_surveillance_total",
    recommended_action: "résistance_biométrique_urgente",
    signal: "🔴 État de surveillance totale — contrôle biométrique systémique",
  },
  {
    id: "BSE-006",
    surveillance_domain: "healthcare_biometrics",
    region: "EMEA",
    facial_recognition_deployment_density: 0.28,
    behavioral_biometric_collection_rate: 0.22,
    DNA_database_expansion_rate: 0.25,
    biometric_data_commercialization_risk: 0.30,
    cross_border_biometric_sharing_level: 0.20,
    biometric_error_rate_impact: 0.25,
    surveillance_infrastructure_concentration: 0.25,
    biometric_consent_violation_index: 0.28,
    predictive_policing_bias: 0.20,
    emotion_recognition_deployment: 0.18,
    voice_print_mass_collection: 0.22,
    gait_analysis_deployment: 0.18,
    biometric_resistance_suppression: 0.20,
    identity_theft_systemic_risk: 0.22,
    biometric_political_persecution_risk: 0.15,
    permanent_record_creation_rate: 0.20,
    biometric_apartheid_risk: 0.12,
    // computed
    deployment_score: 23.9,
    violation_score: 27.05,
    control_score: 24.0,
    persecution_score: 18.2,
    composite_score: 23.62,
    risk_level: "moderate",
    surveillance_pattern: "none",
    severity: "dérive_biométrique_active",
    recommended_action: "renforcement_droits_biométriques",
    signal: "🟡 Dérive biométrique — vigilance requise",
  },
  {
    id: "BSE-007",
    surveillance_domain: "financial_identity",
    region: "NAMER",
    facial_recognition_deployment_density: 0.42,
    behavioral_biometric_collection_rate: 0.38,
    DNA_database_expansion_rate: 0.35,
    biometric_data_commercialization_risk: 0.80,
    cross_border_biometric_sharing_level: 0.72,
    biometric_error_rate_impact: 0.45,
    surveillance_infrastructure_concentration: 0.40,
    biometric_consent_violation_index: 0.48,
    predictive_policing_bias: 0.35,
    emotion_recognition_deployment: 0.30,
    voice_print_mass_collection: 0.42,
    gait_analysis_deployment: 0.30,
    biometric_resistance_suppression: 0.38,
    identity_theft_systemic_risk: 0.50,
    biometric_political_persecution_risk: 0.32,
    permanent_record_creation_rate: 0.42,
    biometric_apartheid_risk: 0.28,
    // computed
    deployment_score: 38.05,
    violation_score: 55.0,
    control_score: 42.15,
    persecution_score: 36.1,
    composite_score: 43.09,
    risk_level: "high",
    surveillance_pattern: "identity_monopoly",
    severity: "contrôle_biométrique_avancé",
    recommended_action: "régulation_biométrique_stricte",
    signal: "🟠 Contrôle biométrique avancé détecté",
  },
  {
    id: "BSE-008",
    surveillance_domain: "population_control",
    region: "APAC",
    facial_recognition_deployment_density: 0.62,
    behavioral_biometric_collection_rate: 0.58,
    DNA_database_expansion_rate: 0.55,
    biometric_data_commercialization_risk: 0.52,
    cross_border_biometric_sharing_level: 0.48,
    biometric_error_rate_impact: 0.60,
    surveillance_infrastructure_concentration: 0.62,
    biometric_consent_violation_index: 0.58,
    predictive_policing_bias: 0.55,
    emotion_recognition_deployment: 0.65,
    voice_print_mass_collection: 0.60,
    gait_analysis_deployment: 0.55,
    biometric_resistance_suppression: 0.78,
    identity_theft_systemic_risk: 0.55,
    biometric_political_persecution_risk: 0.60,
    permanent_record_creation_rate: 0.65,
    biometric_apartheid_risk: 0.82,
    // computed
    deployment_score: 59.25,
    violation_score: 55.7,
    control_score: 65.55,
    persecution_score: 73.25,
    composite_score: 63.09,
    risk_level: "critical",
    surveillance_pattern: "biometric_apartheid",
    severity: "état_surveillance_total",
    recommended_action: "résistance_biométrique_urgente",
    signal: "🔴 État de surveillance totale — contrôle biométrique systémique",
  },
];

export async function GET(request: Request) {
  if (!SWARM_API_URL) {
    const { searchParams } = new URL(request.url);
    const risk    = searchParams.get("risk");
    const pattern = searchParams.get("pattern");

    let entities = [...mockEntities];
    if (risk)    entities = entities.filter((e) => e.risk_level === risk);
    if (pattern) entities = entities.filter((e) => e.surveillance_pattern === pattern);

    const risk_distribution:     Record<string, number> = {};
    const pattern_distribution:  Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution:   Record<string, number> = {};
    let total_composite = 0;
    let total_facial    = 0;
    let critical_count  = 0;
    let high_count      = 0;
    let moderate_count  = 0;
    let low_count       = 0;

    for (const e of mockEntities) {
      risk_distribution[e.risk_level]           = (risk_distribution[e.risk_level] || 0) + 1;
      pattern_distribution[e.surveillance_pattern] = (pattern_distribution[e.surveillance_pattern] || 0) + 1;
      severity_distribution[e.severity]         = (severity_distribution[e.severity] || 0) + 1;
      action_distribution[e.recommended_action] = (action_distribution[e.recommended_action] || 0) + 1;
      total_composite += e.composite_score;
      total_facial    += e.facial_recognition_deployment_density;
      if (e.risk_level === "critical")       critical_count++;
      else if (e.risk_level === "high")      high_count++;
      else if (e.risk_level === "moderate")  moderate_count++;
      else                                   low_count++;
    }

    const n             = mockEntities.length;
    const avg_composite = Math.round((total_composite / n) * 100) / 100;

    return sealResponse(NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id:   333,
        module_name: "Biometric Surveillance & Identity Control Intelligence Engine",
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
        avg_estimated_surveillance_index: Math.round((avg_composite / 100 * 10) * 100) / 100,
        avg_facial_recognition_density:   Math.round((total_facial / n) * 100) / 100,
      },
    } as Record<string, unknown>)));
  }

  try {
    const { searchParams } = new URL(request.url);
    const url = new URL(`${SWARM_API_URL}/api/biometric-surveillance-engine`);
    const risk    = searchParams.get("risk");
    const pattern = searchParams.get("pattern");
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(await res.json()));
  } catch {}

  return sealResponse(NextResponse.json(
    sealResponse({ entities: [], summary: {} } as Record<string, unknown>),
    { status: 502 },
  ));
}
