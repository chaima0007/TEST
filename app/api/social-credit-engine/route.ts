import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// 8 mock entities covering all 5 patterns and all 4 risk levels
// SCR-001: critical, total_behavioral_control      (deployment_density>=0.70, automated_punishment>=0.65, composite>=60)
// SCR-002: low,      none                          (all low, composite<20)
// SCR-003: high,     dissent_elimination           (dissent_penalization>=0.70, opposition_targeting>=0.65, composite>=40<60)
// SCR-004: low,      none                          (all low, composite<20)
// SCR-005: critical, collective_punishment_system  (family_collective>=0.70, social_ostracism>=0.65, composite>=60)
// SCR-006: moderate, none                          (composite>=20<40)
// SCR-007: high,     behavioral_homogenization_lock(behavioral_norm_homogenization>=0.70, opacity>=0.65, composite>=40<60)
// SCR-008: critical, corporate_state_score_fusion  (corporate_scoring_integration>=0.70, private_public_fusion>=0.65, composite>=60)

const mockEntities = [
  {
    id: "SCR-001",
    control_domain: "population_scoring",
    region: "APAC",
    behavioral_score_deployment_density: 0.88,
    access_restriction_based_on_score: 0.82,
    corporate_social_scoring_integration: 0.60,
    gamification_compliance_mechanism: 0.70,
    score_opacity_and_unappealability: 0.75,
    AI_behavioral_prediction_scoring: 0.72,
    cross_sector_score_aggregation: 0.68,
    dissent_behavioral_penalization: 0.65,
    score_based_opportunity_denial: 0.70,
    social_ostracism_enforcement: 0.68,
    private_public_score_fusion: 0.55,
    automated_punishment_system: 0.78,
    behavioral_norm_homogenization: 0.72,
    opposition_score_targeting: 0.60,
    family_collective_score_punishment: 0.55,
    score_export_to_allied_systems: 0.60,
    resistance_detection_scoring: 0.65,
    // computed
    control_score: 83.4,
    opacity_score: 72.2,
    punishment_score: 60.75,
    homogenization_score: 70.1,
    composite_score: 72.28,
    risk_level: "critical",
    social_credit_pattern: "total_behavioral_control",
    severity: "contrôle_comportemental_total",
    recommended_action: "résistance_crédit_social_urgente",
    signal: "🔴 Contrôle comportemental total — crédit social systémique",
  },
  {
    id: "SCR-002",
    control_domain: "civic_engagement",
    region: "EMEA",
    behavioral_score_deployment_density: 0.08,
    access_restriction_based_on_score: 0.06,
    corporate_social_scoring_integration: 0.05,
    gamification_compliance_mechanism: 0.07,
    score_opacity_and_unappealability: 0.06,
    AI_behavioral_prediction_scoring: 0.05,
    cross_sector_score_aggregation: 0.04,
    dissent_behavioral_penalization: 0.05,
    score_based_opportunity_denial: 0.04,
    social_ostracism_enforcement: 0.06,
    private_public_score_fusion: 0.04,
    automated_punishment_system: 0.05,
    behavioral_norm_homogenization: 0.07,
    opposition_score_targeting: 0.05,
    family_collective_score_punishment: 0.04,
    score_export_to_allied_systems: 0.03,
    resistance_detection_scoring: 0.04,
    // computed
    control_score: 6.55,
    opacity_score: 5.15,
    punishment_score: 4.75,
    homogenization_score: 6.65,
    composite_score: 5.77,
    risk_level: "low",
    social_credit_pattern: "none",
    severity: "scoring_comportemental_limité",
    recommended_action: "veille_scoring_comportemental",
    signal: "🟢 Scoring comportemental limité et contenu",
  },
  {
    id: "SCR-003",
    control_domain: "political_compliance",
    region: "MEA",
    behavioral_score_deployment_density: 0.48,
    access_restriction_based_on_score: 0.45,
    corporate_social_scoring_integration: 0.38,
    gamification_compliance_mechanism: 0.35,
    score_opacity_and_unappealability: 0.42,
    AI_behavioral_prediction_scoring: 0.40,
    cross_sector_score_aggregation: 0.38,
    dissent_behavioral_penalization: 0.82,
    score_based_opportunity_denial: 0.50,
    social_ostracism_enforcement: 0.40,
    private_public_score_fusion: 0.35,
    automated_punishment_system: 0.42,
    behavioral_norm_homogenization: 0.40,
    opposition_score_targeting: 0.78,
    family_collective_score_punishment: 0.35,
    score_export_to_allied_systems: 0.45,
    resistance_detection_scoring: 0.55,
    // computed
    control_score: 45.45,
    opacity_score: 40.3,
    punishment_score: 68.85,
    homogenization_score: 38.75,
    composite_score: 48.67,
    risk_level: "high",
    social_credit_pattern: "dissent_elimination",
    severity: "système_crédit_social_avancé",
    recommended_action: "interdiction_système_crédit_social",
    signal: "🟠 Système crédit social avancé détecté",
  },
  {
    id: "SCR-004",
    control_domain: "corporate_hr",
    region: "NAMER",
    behavioral_score_deployment_density: 0.10,
    access_restriction_based_on_score: 0.09,
    corporate_social_scoring_integration: 0.08,
    gamification_compliance_mechanism: 0.10,
    score_opacity_and_unappealability: 0.09,
    AI_behavioral_prediction_scoring: 0.07,
    cross_sector_score_aggregation: 0.06,
    dissent_behavioral_penalization: 0.08,
    score_based_opportunity_denial: 0.07,
    social_ostracism_enforcement: 0.09,
    private_public_score_fusion: 0.06,
    automated_punishment_system: 0.08,
    behavioral_norm_homogenization: 0.10,
    opposition_score_targeting: 0.07,
    family_collective_score_punishment: 0.06,
    score_export_to_allied_systems: 0.05,
    resistance_detection_scoring: 0.06,
    // computed
    control_score: 9.15,
    opacity_score: 7.55,
    punishment_score: 7.15,
    homogenization_score: 9.65,
    composite_score: 8.35,
    risk_level: "low",
    social_credit_pattern: "none",
    severity: "scoring_comportemental_limité",
    recommended_action: "veille_scoring_comportemental",
    signal: "🟢 Scoring comportemental limité et contenu",
  },
  {
    id: "SCR-005",
    control_domain: "family_social_control",
    region: "APAC",
    behavioral_score_deployment_density: 0.65,
    access_restriction_based_on_score: 0.72,
    corporate_social_scoring_integration: 0.55,
    gamification_compliance_mechanism: 0.68,
    score_opacity_and_unappealability: 0.70,
    AI_behavioral_prediction_scoring: 0.68,
    cross_sector_score_aggregation: 0.65,
    dissent_behavioral_penalization: 0.60,
    score_based_opportunity_denial: 0.68,
    social_ostracism_enforcement: 0.78,
    private_public_score_fusion: 0.55,
    automated_punishment_system: 0.62,
    behavioral_norm_homogenization: 0.65,
    opposition_score_targeting: 0.55,
    family_collective_score_punishment: 0.85,
    score_export_to_allied_systems: 0.60,
    resistance_detection_scoring: 0.62,
    // computed
    control_score: 66.7,
    opacity_score: 68.05,
    punishment_score: 64.5,
    homogenization_score: 70.3,
    composite_score: 67.21,
    risk_level: "critical",
    social_credit_pattern: "collective_punishment_system",
    severity: "contrôle_comportemental_total",
    recommended_action: "résistance_crédit_social_urgente",
    signal: "🔴 Contrôle comportemental total — crédit social systémique",
  },
  {
    id: "SCR-006",
    control_domain: "workplace_conduct",
    region: "LATAM",
    behavioral_score_deployment_density: 0.28,
    access_restriction_based_on_score: 0.25,
    corporate_social_scoring_integration: 0.22,
    gamification_compliance_mechanism: 0.25,
    score_opacity_and_unappealability: 0.28,
    AI_behavioral_prediction_scoring: 0.22,
    cross_sector_score_aggregation: 0.20,
    dissent_behavioral_penalization: 0.25,
    score_based_opportunity_denial: 0.22,
    social_ostracism_enforcement: 0.24,
    private_public_score_fusion: 0.20,
    automated_punishment_system: 0.22,
    behavioral_norm_homogenization: 0.26,
    opposition_score_targeting: 0.22,
    family_collective_score_punishment: 0.18,
    score_export_to_allied_systems: 0.15,
    resistance_detection_scoring: 0.20,
    // computed
    control_score: 25.45,
    opacity_score: 23.9,
    punishment_score: 22.2,
    homogenization_score: 25.05,
    composite_score: 24.17,
    risk_level: "moderate",
    social_credit_pattern: "none",
    severity: "notation_comportementale_structurelle",
    recommended_action: "protection_droits_comportementaux",
    signal: "🟡 Notation comportementale structurelle active",
  },
  {
    id: "SCR-007",
    control_domain: "cultural_normalization",
    region: "EMEA",
    behavioral_score_deployment_density: 0.45,
    access_restriction_based_on_score: 0.48,
    corporate_social_scoring_integration: 0.42,
    gamification_compliance_mechanism: 0.55,
    score_opacity_and_unappealability: 0.78,
    AI_behavioral_prediction_scoring: 0.68,
    cross_sector_score_aggregation: 0.62,
    dissent_behavioral_penalization: 0.48,
    score_based_opportunity_denial: 0.45,
    social_ostracism_enforcement: 0.50,
    private_public_score_fusion: 0.40,
    automated_punishment_system: 0.42,
    behavioral_norm_homogenization: 0.82,
    opposition_score_targeting: 0.45,
    family_collective_score_punishment: 0.40,
    score_export_to_allied_systems: 0.38,
    resistance_detection_scoring: 0.45,
    // computed
    control_score: 45.3,
    opacity_score: 70.5,
    punishment_score: 44.95,
    homogenization_score: 64.05,
    composite_score: 55.26,
    risk_level: "high",
    social_credit_pattern: "behavioral_homogenization_lock",
    severity: "système_crédit_social_avancé",
    recommended_action: "interdiction_système_crédit_social",
    signal: "🟠 Système crédit social avancé détecté",
  },
  {
    id: "SCR-008",
    control_domain: "corporate_state_integration",
    region: "NAMER",
    behavioral_score_deployment_density: 0.68,
    access_restriction_based_on_score: 0.72,
    corporate_social_scoring_integration: 0.85,
    gamification_compliance_mechanism: 0.65,
    score_opacity_and_unappealability: 0.60,
    AI_behavioral_prediction_scoring: 0.72,
    cross_sector_score_aggregation: 0.68,
    dissent_behavioral_penalization: 0.65,
    score_based_opportunity_denial: 0.70,
    social_ostracism_enforcement: 0.60,
    private_public_score_fusion: 0.78,
    automated_punishment_system: 0.60,
    behavioral_norm_homogenization: 0.62,
    opposition_score_targeting: 0.60,
    family_collective_score_punishment: 0.62,
    score_export_to_allied_systems: 0.72,
    resistance_detection_scoring: 0.68,
    // computed
    control_score: 67.4,
    opacity_score: 66.2,
    punishment_score: 62.5,
    homogenization_score: 62.05,
    composite_score: 64.81,
    risk_level: "critical",
    social_credit_pattern: "corporate_state_score_fusion",
    severity: "contrôle_comportemental_total",
    recommended_action: "résistance_crédit_social_urgente",
    signal: "🔴 Contrôle comportemental total — crédit social systémique",
  },
];

export async function GET(request: Request) {
  if (!SWARM_API_URL) {
    const { searchParams } = new URL(request.url);
    const risk    = searchParams.get("risk");
    const pattern = searchParams.get("pattern");

    let entities = [...mockEntities];
    if (risk)    entities = entities.filter((e) => e.risk_level === risk);
    if (pattern) entities = entities.filter((e) => e.social_credit_pattern === pattern);

    const risk_distribution:     Record<string, number> = {};
    const pattern_distribution:  Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution:   Record<string, number> = {};
    let total_composite         = 0;
    let total_behavioral_density = 0;
    let critical_count  = 0;
    let high_count      = 0;
    let moderate_count  = 0;
    let low_count       = 0;

    for (const e of mockEntities) {
      risk_distribution[e.risk_level]               = (risk_distribution[e.risk_level] || 0) + 1;
      pattern_distribution[e.social_credit_pattern] = (pattern_distribution[e.social_credit_pattern] || 0) + 1;
      severity_distribution[e.severity]             = (severity_distribution[e.severity] || 0) + 1;
      action_distribution[e.recommended_action]     = (action_distribution[e.recommended_action] || 0) + 1;
      total_composite          += e.composite_score;
      total_behavioral_density += e.behavioral_score_deployment_density;
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
        module_id:   348,
        module_name: "Social Credit & Behavioral Score Intelligence Engine",
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
        avg_estimated_social_credit_index: Math.round((avg_composite / 100 * 10) * 100) / 100,
        avg_behavioral_score_density:      Math.round((total_behavioral_density / n) * 100) / 100,
      },
    } as Record<string, unknown>));
  }

  try {
    const { searchParams } = new URL(request.url);
    const url = new URL(`${SWARM_API_URL}/api/social-credit-engine`);
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
