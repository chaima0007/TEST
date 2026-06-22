import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[worker-automation-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

// 8 mock entities covering all 5 patterns and all 4 risk levels
// WAE-001: critical, mass_workforce_obsolescence   (displacement_rate>0.85, automation_penetration>0.80, composite≥60)
// WAE-002: low,      none                          (all favourable, composite<20)
// WAE-003: critical, skill_mismatch_crisis         (skill_adaptability<0.15, reskilling_investment<0.20, composite≥60)
// WAE-004: low,      none                          (all favourable, composite<20)
// WAE-005: critical, social_safety_net_collapse    (social_safety_coverage<0.15, union_strength<0.20, composite≥60)
// WAE-006: moderate, none                          (composite≥20<40)
// WAE-007: high,     automation_inequality_trap    (wage_inequality>0.80, platform_economy_growth>0.75, composite≥40<60)
// WAE-008: high,     policy_vacuum_crisis          (policy_effectiveness<0.20, job_creation_rate<0.20, composite≥40<60)

const mockEntities = [
  {
    id: "WAE-001",
    sector_type: "manufacturing",
    region: "RUST_BELT",
    displacement_rate: 0.90,
    automation_penetration: 0.88,
    skill_adaptability: 0.12,
    reskilling_investment: 0.10,
    social_safety_coverage: 0.25,
    policy_effectiveness: 0.20,
    job_creation_rate: 0.15,
    union_strength: 0.30,
    education_quality: 0.25,
    wage_inequality: 0.75,
    geographic_mobility: 0.20,
    age_vulnerability: 0.80,
    gender_impact: 0.60,
    manufacturing_exposure: 0.92,
    service_sector_risk: 0.50,
    platform_economy_growth: 0.40,
    retraining_success_rate: 0.15,
    // computed
    displacement_score: 89.80,
    skill_gap_score: 87.95,
    social_safety_score: 73.25,
    policy_response_score: 79.50,
    composite_score: 83.14,
    risk_level: "critical",
    automation_pattern: "mass_workforce_obsolescence",
    severity: "crise_obsolescence_massive_travailleurs",
    recommended_action: "intervention_urgente_reconversion_massive",
    signal: "🔴 Crise d'obsolescence massive des travailleurs — intervention d'urgence requise",
  },
  {
    id: "WAE-002",
    sector_type: "tech_services",
    region: "NORDIC",
    displacement_rate: 0.08,
    automation_penetration: 0.10,
    skill_adaptability: 0.88,
    reskilling_investment: 0.85,
    social_safety_coverage: 0.92,
    policy_effectiveness: 0.88,
    job_creation_rate: 0.85,
    union_strength: 0.80,
    education_quality: 0.90,
    wage_inequality: 0.10,
    geographic_mobility: 0.85,
    age_vulnerability: 0.10,
    gender_impact: 0.12,
    manufacturing_exposure: 0.08,
    service_sector_risk: 0.12,
    platform_economy_growth: 0.15,
    retraining_success_rate: 0.90,
    // computed
    displacement_score: 8.70,
    skill_gap_score: 12.55,
    social_safety_score: 12.70,
    policy_response_score: 12.05,
    composite_score: 11.33,
    risk_level: "low",
    automation_pattern: "none",
    severity: "transition_emploi_sous_surveillance",
    recommended_action: "veille_transformation_emploi_continue",
    signal: "🟢 Transition emploi sous surveillance — veille préventive maintenue",
  },
  {
    id: "WAE-003",
    sector_type: "logistics",
    region: "SOUTHEAST_ASIA",
    displacement_rate: 0.75,
    automation_penetration: 0.70,
    skill_adaptability: 0.10,
    reskilling_investment: 0.12,
    social_safety_coverage: 0.20,
    policy_effectiveness: 0.22,
    job_creation_rate: 0.20,
    union_strength: 0.18,
    education_quality: 0.20,
    wage_inequality: 0.70,
    geographic_mobility: 0.15,
    age_vulnerability: 0.65,
    gender_impact: 0.55,
    manufacturing_exposure: 0.70,
    service_sector_risk: 0.60,
    platform_economy_growth: 0.50,
    retraining_success_rate: 0.10,
    // computed
    displacement_score: 72.00,
    skill_gap_score: 89.30,
    social_safety_score: 78.20,
    policy_response_score: 79.20,
    composite_score: 79.31,
    risk_level: "critical",
    automation_pattern: "skill_mismatch_crisis",
    severity: "crise_obsolescence_massive_travailleurs",
    recommended_action: "intervention_urgente_reconversion_massive",
    signal: "🔴 Crise d'obsolescence massive des travailleurs — intervention d'urgence requise",
  },
  {
    id: "WAE-004",
    sector_type: "public_services",
    region: "WESTERN_EUROPE",
    displacement_rate: 0.06,
    automation_penetration: 0.08,
    skill_adaptability: 0.80,
    reskilling_investment: 0.78,
    social_safety_coverage: 0.88,
    policy_effectiveness: 0.82,
    job_creation_rate: 0.75,
    union_strength: 0.75,
    education_quality: 0.85,
    wage_inequality: 0.12,
    geographic_mobility: 0.70,
    age_vulnerability: 0.15,
    gender_impact: 0.10,
    manufacturing_exposure: 0.06,
    service_sector_risk: 0.10,
    platform_economy_growth: 0.12,
    retraining_success_rate: 0.82,
    // computed
    displacement_score: 6.70,
    skill_gap_score: 20.20,
    social_safety_score: 16.55,
    policy_response_score: 18.70,
    composite_score: 14.94,
    risk_level: "low",
    automation_pattern: "none",
    severity: "transition_emploi_sous_surveillance",
    recommended_action: "veille_transformation_emploi_continue",
    signal: "🟢 Transition emploi sous surveillance — veille préventive maintenue",
  },
  {
    id: "WAE-005",
    sector_type: "retail",
    region: "LATIN_AMERICA",
    displacement_rate: 0.78,
    automation_penetration: 0.72,
    skill_adaptability: 0.20,
    reskilling_investment: 0.18,
    social_safety_coverage: 0.10,
    policy_effectiveness: 0.18,
    job_creation_rate: 0.18,
    union_strength: 0.12,
    education_quality: 0.20,
    wage_inequality: 0.80,
    geographic_mobility: 0.18,
    age_vulnerability: 0.72,
    gender_impact: 0.68,
    manufacturing_exposure: 0.55,
    service_sector_risk: 0.75,
    platform_economy_growth: 0.60,
    retraining_success_rate: 0.18,
    // computed
    displacement_score: 70.15,
    skill_gap_score: 81.20,
    social_safety_score: 86.80,
    policy_response_score: 81.30,
    composite_score: 79.31,
    risk_level: "critical",
    automation_pattern: "social_safety_net_collapse",
    severity: "crise_obsolescence_massive_travailleurs",
    recommended_action: "intervention_urgente_reconversion_massive",
    signal: "🔴 Crise d'obsolescence massive des travailleurs — intervention d'urgence requise",
  },
  {
    id: "WAE-006",
    sector_type: "finance",
    region: "EMEA",
    displacement_rate: 0.22,
    automation_penetration: 0.24,
    skill_adaptability: 0.62,
    reskilling_investment: 0.58,
    social_safety_coverage: 0.65,
    policy_effectiveness: 0.60,
    job_creation_rate: 0.55,
    union_strength: 0.55,
    education_quality: 0.60,
    wage_inequality: 0.30,
    geographic_mobility: 0.55,
    age_vulnerability: 0.28,
    gender_impact: 0.25,
    manufacturing_exposure: 0.18,
    service_sector_risk: 0.28,
    platform_economy_growth: 0.32,
    retraining_success_rate: 0.60,
    // computed
    displacement_score: 21.70,
    skill_gap_score: 39.90,
    social_safety_score: 37.25,
    policy_response_score: 41.25,
    composite_score: 34.05,
    risk_level: "moderate",
    automation_pattern: "none",
    severity: "vulnérabilité_transformation_emploi",
    recommended_action: "renforcement_filets_protection_sociale",
    signal: "🟡 Vulnérabilité à la transformation de l'emploi — renforcement des protections sociales",
  },
  {
    id: "WAE-007",
    sector_type: "gig_economy",
    region: "NORTH_AMERICA",
    displacement_rate: 0.45,
    automation_penetration: 0.48,
    skill_adaptability: 0.45,
    reskilling_investment: 0.40,
    social_safety_coverage: 0.38,
    policy_effectiveness: 0.40,
    job_creation_rate: 0.42,
    union_strength: 0.32,
    education_quality: 0.48,
    wage_inequality: 0.85,
    geographic_mobility: 0.50,
    age_vulnerability: 0.45,
    gender_impact: 0.42,
    manufacturing_exposure: 0.38,
    service_sector_risk: 0.55,
    platform_economy_growth: 0.82,
    retraining_success_rate: 0.45,
    // computed
    displacement_score: 44.30,
    skill_gap_score: 56.75,
    social_safety_score: 69.85,
    policy_response_score: 56.70,
    composite_score: 56.28,
    risk_level: "high",
    automation_pattern: "automation_inequality_trap",
    severity: "déplacement_automatisation_majeur",
    recommended_action: "programme_requalification_accéléré",
    signal: "🟠 Déplacement par automatisation majeur détecté — requalification accélérée nécessaire",
  },
  {
    id: "WAE-008",
    sector_type: "agriculture",
    region: "SUB_SAHARAN_AFRICA",
    displacement_rate: 0.35,
    automation_penetration: 0.32,
    skill_adaptability: 0.45,
    reskilling_investment: 0.50,
    social_safety_coverage: 0.50,
    policy_effectiveness: 0.15,
    job_creation_rate: 0.18,
    union_strength: 0.45,
    education_quality: 0.65,
    wage_inequality: 0.35,
    geographic_mobility: 0.30,
    age_vulnerability: 0.45,
    gender_impact: 0.40,
    manufacturing_exposure: 0.30,
    service_sector_risk: 0.40,
    platform_economy_growth: 0.30,
    retraining_success_rate: 0.50,
    // computed
    displacement_score: 32.70,
    skill_gap_score: 52.00,
    social_safety_score: 48.00,
    policy_response_score: 66.75,
    composite_score: 48.16,
    risk_level: "high",
    automation_pattern: "policy_vacuum_crisis",
    severity: "déplacement_automatisation_majeur",
    recommended_action: "programme_requalification_accéléré",
    signal: "🟠 Déplacement par automatisation majeur détecté — requalification accélérée nécessaire",
  },
];

export async function GET() {
  if (!SWARM_API_URL) {
    const risk_distribution:     Record<string, number> = {};
    const pattern_distribution:  Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution:   Record<string, number> = {};
    let total_composite = 0;
    let critical        = 0;
    let high            = 0;
    let moderate        = 0;
    let low             = 0;

    for (const e of mockEntities) {
      risk_distribution[e.risk_level]           = (risk_distribution[e.risk_level] || 0) + 1;
      pattern_distribution[e.automation_pattern] = (pattern_distribution[e.automation_pattern] || 0) + 1;
      severity_distribution[e.severity]         = (severity_distribution[e.severity] || 0) + 1;
      action_distribution[e.recommended_action] = (action_distribution[e.recommended_action] || 0) + 1;
      total_composite += e.composite_score;
      if (e.risk_level === "critical")      critical++;
      else if (e.risk_level === "high")     high++;
      else if (e.risk_level === "moderate") moderate++;
      else                                  low++;
    }

    const n             = mockEntities.length;
    const avg_composite = Math.round((total_composite / n) * 100) / 100;

    return sealResponse(NextResponse.json(sealResponse({
      entities: mockEntities,
      summary: {
        module_id:   393,
        module_name: "Automatisation & Déplacement des Travailleurs Intelligence Engine",
        total:    n,
        critical,
        high,
        moderate,
        low,
        avg_composite,
        pattern_distribution,
        risk_distribution,
        severity_distribution,
        action_distribution,
        avg_estimated_automation_displacement_index: Math.round((avg_composite / 100 * 10) * 100) / 100,
      },
    } as Record<string, unknown>)));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/worker-automation-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(sealResponse(await res.json())));
  } catch {}

  return sealResponse(NextResponse.json(
    sealResponse({ entities: [], summary: {} } as Record<string, unknown>),
    { status: 502 },
  ));
}
