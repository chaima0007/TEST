import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  // mock mode — no external dependency required
}

const SWARM_API_URL = process.env.SWARM_API_URL;

// 8 mock entities covering all 5 patterns and all 4 risk levels
// PWU-001: critical, mass_automation_displacement   (automation>0.85, cognitive_job>0.80, composite≥60)
// PWU-002: critical, welfare_state_implosion        (welfare_state>0.85, UBI_fiscal>0.80, composite≥60)
// PWU-003: high,     social_contract_collapse       (social_contract>0.85, cohesion>0.80, composite≥40)
// PWU-004: high,     middle_class_extinction_event  (middle_class>0.80, polarization>0.75, composite≥40)
// PWU-005: critical, political_automation_revolt    (political_instab>0.80, automation_tax>0.75, composite≥60)
// PWU-006: moderate, none                           (composite≥20 <40)
// PWU-007: low,      none                           (composite<20)
// PWU-008: low,      none                           (composite<20)

const mockEntities = [
  {
    id: "PWU-001",
    economic_sector: "manufacturing",
    region: "NAMER",
    automation_displacement_rate: 0.90,
    UBI_fiscal_sustainability: 0.55,
    retraining_program_failure: 0.70,
    social_contract_breakdown: 0.60,
    gig_worker_precariousness: 0.65,
    cognitive_job_extinction: 0.88,
    labor_market_polarization: 0.70,
    meaning_crisis_intensity: 0.65,
    political_instability_unemployment: 0.60,
    welfare_state_collapse: 0.50,
    automation_tax_resistance: 0.55,
    UBI_inflation_risk: 0.55,
    skills_gap_acceleration: 0.75,
    inequality_amplification_AI: 0.65,
    union_power_collapse: 0.70,
    middle_class_extinction: 0.65,
    social_cohesion_erosion: 0.55,
    // computed
    displacement_score: 85.55,
    social_score: 59.50,
    economic_score: 53.25,
    political_score: 59.50,
    composite_score: 65.75,
    risk_level: "critical",
    post_work_pattern: "mass_automation_displacement",
    severity: "effondrement_post_travail_systémique",
    recommended_action: "intervention_urgente_revenu_universel",
    signal: "🔴 Effondrement post-travail systémique — disruption emploi IA critique",
  },
  {
    id: "PWU-002",
    economic_sector: "public_services",
    region: "EMEA",
    automation_displacement_rate: 0.55,
    UBI_fiscal_sustainability: 0.88,
    retraining_program_failure: 0.60,
    social_contract_breakdown: 0.65,
    gig_worker_precariousness: 0.60,
    cognitive_job_extinction: 0.50,
    labor_market_polarization: 0.55,
    meaning_crisis_intensity: 0.60,
    political_instability_unemployment: 0.65,
    welfare_state_collapse: 0.90,
    automation_tax_resistance: 0.60,
    UBI_inflation_risk: 0.80,
    skills_gap_acceleration: 0.60,
    inequality_amplification_AI: 0.70,
    union_power_collapse: 0.65,
    middle_class_extinction: 0.60,
    social_cohesion_erosion: 0.60,
    // computed
    displacement_score: 54.50,
    social_score: 62.00,
    economic_score: 86.70,
    political_score: 64.50,
    composite_score: 66.43,
    risk_level: "critical",
    post_work_pattern: "welfare_state_implosion",
    severity: "effondrement_post_travail_systémique",
    recommended_action: "intervention_urgente_revenu_universel",
    signal: "🔴 Effondrement post-travail systémique — disruption emploi IA critique",
  },
  {
    id: "PWU-003",
    economic_sector: "retail_commerce",
    region: "APAC",
    automation_displacement_rate: 0.55,
    UBI_fiscal_sustainability: 0.35,
    retraining_program_failure: 0.50,
    social_contract_breakdown: 0.88,
    gig_worker_precariousness: 0.55,
    cognitive_job_extinction: 0.50,
    labor_market_polarization: 0.50,
    meaning_crisis_intensity: 0.60,
    political_instability_unemployment: 0.40,
    welfare_state_collapse: 0.30,
    automation_tax_resistance: 0.35,
    UBI_inflation_risk: 0.35,
    skills_gap_acceleration: 0.50,
    inequality_amplification_AI: 0.45,
    union_power_collapse: 0.50,
    middle_class_extinction: 0.55,
    social_cohesion_erosion: 0.85,
    // computed
    displacement_score: 52.00,
    social_score: 79.95,
    economic_score: 33.25,
    political_score: 39.50,
    composite_score: 51.80,
    risk_level: "high",
    post_work_pattern: "social_contract_collapse",
    severity: "disruption_emploi_revenu_majeure",
    recommended_action: "audit_systémique_transition_emploi",
    signal: "🟠 Disruption emploi & revenu universel majeure détectée",
  },
  {
    id: "PWU-004",
    economic_sector: "finance_banking",
    region: "LATAM",
    automation_displacement_rate: 0.60,
    UBI_fiscal_sustainability: 0.35,
    retraining_program_failure: 0.55,
    social_contract_breakdown: 0.55,
    gig_worker_precariousness: 0.60,
    cognitive_job_extinction: 0.55,
    labor_market_polarization: 0.80,
    meaning_crisis_intensity: 0.60,
    political_instability_unemployment: 0.40,
    welfare_state_collapse: 0.30,
    automation_tax_resistance: 0.35,
    UBI_inflation_risk: 0.40,
    skills_gap_acceleration: 0.65,
    inequality_amplification_AI: 0.55,
    union_power_collapse: 0.60,
    middle_class_extinction: 0.85,
    social_cohesion_erosion: 0.50,
    // computed
    displacement_score: 59.50,
    social_score: 54.50,
    economic_score: 34.50,
    political_score: 42.00,
    composite_score: 48.50,
    risk_level: "high",
    post_work_pattern: "middle_class_extinction_event",
    severity: "disruption_emploi_revenu_majeure",
    recommended_action: "audit_systémique_transition_emploi",
    signal: "🟠 Disruption emploi & revenu universel majeure détectée",
  },
  {
    id: "PWU-005",
    economic_sector: "transportation_logistics",
    region: "NAMER",
    automation_displacement_rate: 0.70,
    UBI_fiscal_sustainability: 0.55,
    retraining_program_failure: 0.65,
    social_contract_breakdown: 0.65,
    gig_worker_precariousness: 0.70,
    cognitive_job_extinction: 0.65,
    labor_market_polarization: 0.65,
    meaning_crisis_intensity: 0.70,
    political_instability_unemployment: 0.85,
    welfare_state_collapse: 0.50,
    automation_tax_resistance: 0.80,
    UBI_inflation_risk: 0.60,
    skills_gap_acceleration: 0.75,
    inequality_amplification_AI: 0.75,
    union_power_collapse: 0.70,
    middle_class_extinction: 0.65,
    social_cohesion_erosion: 0.60,
    // computed
    displacement_score: 69.50,
    social_score: 64.50,
    economic_score: 54.50,
    political_score: 80.75,
    composite_score: 66.75,
    risk_level: "critical",
    post_work_pattern: "political_automation_revolt",
    severity: "effondrement_post_travail_systémique",
    recommended_action: "intervention_urgente_revenu_universel",
    signal: "🔴 Effondrement post-travail systémique — disruption emploi IA critique",
  },
  {
    id: "PWU-006",
    economic_sector: "healthcare",
    region: "EMEA",
    automation_displacement_rate: 0.25,
    UBI_fiscal_sustainability: 0.28,
    retraining_program_failure: 0.25,
    social_contract_breakdown: 0.30,
    gig_worker_precariousness: 0.28,
    cognitive_job_extinction: 0.20,
    labor_market_polarization: 0.25,
    meaning_crisis_intensity: 0.28,
    political_instability_unemployment: 0.28,
    welfare_state_collapse: 0.25,
    automation_tax_resistance: 0.25,
    UBI_inflation_risk: 0.30,
    skills_gap_acceleration: 0.25,
    inequality_amplification_AI: 0.30,
    union_power_collapse: 0.28,
    middle_class_extinction: 0.25,
    social_cohesion_erosion: 0.25,
    // computed
    displacement_score: 23.25,
    social_score: 27.75,
    economic_score: 27.45,
    political_score: 27.45,
    composite_score: 26.26,
    risk_level: "moderate",
    post_work_pattern: "none",
    severity: "transition_post_travail_active",
    recommended_action: "renforcement_filets_protection_sociale",
    signal: "🟡 Transition post-travail active en cours",
  },
  {
    id: "PWU-007",
    economic_sector: "education",
    region: "APAC",
    automation_displacement_rate: 0.07,
    UBI_fiscal_sustainability: 0.07,
    retraining_program_failure: 0.06,
    social_contract_breakdown: 0.08,
    gig_worker_precariousness: 0.07,
    cognitive_job_extinction: 0.06,
    labor_market_polarization: 0.07,
    meaning_crisis_intensity: 0.07,
    political_instability_unemployment: 0.07,
    welfare_state_collapse: 0.06,
    automation_tax_resistance: 0.06,
    UBI_inflation_risk: 0.08,
    skills_gap_acceleration: 0.08,
    inequality_amplification_AI: 0.08,
    union_power_collapse: 0.06,
    middle_class_extinction: 0.06,
    social_cohesion_erosion: 0.06,
    // computed
    displacement_score: 6.90,
    social_score: 7.05,
    economic_score: 6.90,
    political_score: 6.90,
    composite_score: 6.94,
    risk_level: "low",
    post_work_pattern: "none",
    severity: "risque_post_travail_contenu",
    recommended_action: "veille_disruption_marché_travail",
    signal: "🟢 Risque post-travail contenu",
  },
  {
    id: "PWU-008",
    economic_sector: "agriculture",
    region: "LATAM",
    automation_displacement_rate: 0.05,
    UBI_fiscal_sustainability: 0.05,
    retraining_program_failure: 0.04,
    social_contract_breakdown: 0.06,
    gig_worker_precariousness: 0.05,
    cognitive_job_extinction: 0.04,
    labor_market_polarization: 0.05,
    meaning_crisis_intensity: 0.05,
    political_instability_unemployment: 0.05,
    welfare_state_collapse: 0.04,
    automation_tax_resistance: 0.04,
    UBI_inflation_risk: 0.06,
    skills_gap_acceleration: 0.06,
    inequality_amplification_AI: 0.06,
    union_power_collapse: 0.04,
    middle_class_extinction: 0.04,
    social_cohesion_erosion: 0.05,
    // computed
    displacement_score: 4.90,
    social_score: 5.40,
    economic_score: 4.90,
    political_score: 4.90,
    composite_score: 5.03,
    risk_level: "low",
    post_work_pattern: "none",
    severity: "risque_post_travail_contenu",
    recommended_action: "veille_disruption_marché_travail",
    signal: "🟢 Risque post-travail contenu",
  },
];

export async function GET(request: Request) {
  if (!SWARM_API_URL) {
    const { searchParams } = new URL(request.url);
    const risk    = searchParams.get("risk");
    const pattern = searchParams.get("pattern");

    let entities = [...mockEntities];
    if (risk)    entities = entities.filter((e) => e.risk_level === risk);
    if (pattern) entities = entities.filter((e) => e.post_work_pattern === pattern);

    const risk_distribution:     Record<string, number> = {};
    const pattern_distribution:  Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution:   Record<string, number> = {};
    let total_composite          = 0;
    let critical                 = 0;
    let high                     = 0;
    let moderate                 = 0;
    let low                      = 0;

    for (const e of mockEntities) {
      risk_distribution[e.risk_level]         = (risk_distribution[e.risk_level] || 0) + 1;
      pattern_distribution[e.post_work_pattern] = (pattern_distribution[e.post_work_pattern] || 0) + 1;
      severity_distribution[e.severity]       = (severity_distribution[e.severity] || 0) + 1;
      action_distribution[e.recommended_action] = (action_distribution[e.recommended_action] || 0) + 1;
      total_composite    += e.composite_score;
      if (e.risk_level === "critical")      critical++;
      else if (e.risk_level === "high")     high++;
      else if (e.risk_level === "moderate") moderate++;
      else                                  low++;
    }

    const n             = mockEntities.length;
    const avg_composite = Math.round((total_composite / n) * 100) / 100;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id:   374,
        module_name: "Post-Work Society & Universal Basic Income Intelligence Engine",
        total:       n,
        critical,
        high,
        moderate,
        low,
        avg_composite,
        distributions: {
          pattern:  pattern_distribution,
          risk:     risk_distribution,
          severity: severity_distribution,
          action:   action_distribution,
        },
        avg_estimated_post_work_disruption_index: Math.round((avg_composite / 100 * 10) * 100) / 100,
        pattern_distribution,
        risk_distribution,
        severity_distribution,
      },
    } as Record<string, unknown>));
  }

  try {
    const { searchParams } = new URL(request.url);
    const url = new URL(`${SWARM_API_URL}/api/post-work-ubi-engine`);
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
