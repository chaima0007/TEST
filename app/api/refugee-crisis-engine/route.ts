import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  // mock mode — no external dependency required
}

const SWARM_API_URL = process.env.SWARM_API_URL;

// 8 mock entities covering all 5 patterns and all 4 risk levels
// RCE-001: critical, climate_mass_displacement     (climate_accel>0.85, volume>0.80, composite≥60)
// RCE-002: low, none                               (all low, composite<20)
// RCE-003: high, asylum_system_implosion           (asylum_collapse>0.85, host_overflow>0.80, composite≥40<60)
// RCE-004: low, none                               (all low, composite<20)
// RCE-005: critical, statelessness_crisis          (statelessness>0.85, return_impossible>0.80, composite≥60)
// RCE-006: moderate, none                          (composite≥20<40)
// RCE-007: high, refugee_trafficking_epidemic      (trafficking>0.80, border_harm>0.75, composite≥40<60)
// RCE-008: critical, protracted_displacement_trap  (protracted>0.80, econ_exclusion>0.75, composite≥60)

const mockEntities = [
  {
    id: "RCE-001",
    displacement_type: "climate_induced",
    region: "SAHEL",
    displacement_volume: 0.88,
    climate_displacement_acceleration: 0.90,
    conflict_displacement_intensity: 0.75,
    asylum_system_collapse: 0.60,
    statelessness_risk: 0.55,
    host_country_capacity_overflow: 0.62,
    refugee_integration_failure: 0.70,
    trafficking_vulnerability: 0.65,
    return_impossibility: 0.60,
    UNHCR_funding_gap: 0.55,
    border_militarization_harm: 0.60,
    xenophobia_political_backlash: 0.60,
    protracted_displacement_duration: 0.65,
    education_access_gap: 0.60,
    healthcare_refugee_gap: 0.58,
    economic_exclusion_refugees: 0.65,
    secondary_displacement_risk: 0.70,
    // computed
    displacement_score: 85.45,
    protection_score: 60.75,
    integration_score: 65.75,
    systemic_score: 58.25,
    composite_score: 68.91,
    risk_level: "critical",
    displacement_pattern: "climate_mass_displacement",
    severity: "crise_déplacement_catastrophique",
    recommended_action: "intervention_humanitaire_urgente",
    signal: "🔴 Crise déplacement catastrophique — intervention humanitaire d'urgence requise",
  },
  {
    id: "RCE-002",
    displacement_type: "conflict_induced",
    region: "EMEA",
    displacement_volume: 0.07,
    climate_displacement_acceleration: 0.06,
    conflict_displacement_intensity: 0.05,
    asylum_system_collapse: 0.06,
    statelessness_risk: 0.04,
    host_country_capacity_overflow: 0.05,
    refugee_integration_failure: 0.07,
    trafficking_vulnerability: 0.06,
    return_impossibility: 0.05,
    UNHCR_funding_gap: 0.05,
    border_militarization_harm: 0.05,
    xenophobia_political_backlash: 0.05,
    protracted_displacement_duration: 0.06,
    education_access_gap: 0.05,
    healthcare_refugee_gap: 0.04,
    economic_exclusion_refugees: 0.06,
    secondary_displacement_risk: 0.05,
    // computed
    displacement_score: 6.15,
    protection_score: 5.15,
    integration_score: 6.15,
    systemic_score: 5.40,
    composite_score: 5.75,
    risk_level: "low",
    displacement_pattern: "none",
    severity: "déplacement_contenu",
    recommended_action: "veille_déplacement_préventive",
    signal: "🟢 Déplacement contenu — veille préventive maintenue",
  },
  {
    id: "RCE-003",
    displacement_type: "mixed_flow",
    region: "MENA",
    displacement_volume: 0.45,
    climate_displacement_acceleration: 0.40,
    conflict_displacement_intensity: 0.38,
    asylum_system_collapse: 0.88,
    statelessness_risk: 0.30,
    host_country_capacity_overflow: 0.85,
    refugee_integration_failure: 0.48,
    trafficking_vulnerability: 0.38,
    return_impossibility: 0.40,
    UNHCR_funding_gap: 0.60,
    border_militarization_harm: 0.35,
    xenophobia_political_backlash: 0.55,
    protracted_displacement_duration: 0.42,
    education_access_gap: 0.38,
    healthcare_refugee_gap: 0.40,
    economic_exclusion_refugees: 0.42,
    secondary_displacement_risk: 0.44,
    // computed
    displacement_score: 41.50,
    protection_score: 34.95,
    integration_score: 43.40,
    systemic_score: 69.95,
    composite_score: 46.03,
    risk_level: "high",
    displacement_pattern: "asylum_system_implosion",
    severity: "déplacement_forcé_majeur",
    recommended_action: "mobilisation_protection_internationale",
    signal: "🟠 Déplacement forcé majeur détecté — mobilisation internationale nécessaire",
  },
  {
    id: "RCE-004",
    displacement_type: "internal_displacement",
    region: "APAC",
    displacement_volume: 0.06,
    climate_displacement_acceleration: 0.05,
    conflict_displacement_intensity: 0.04,
    asylum_system_collapse: 0.05,
    statelessness_risk: 0.05,
    host_country_capacity_overflow: 0.04,
    refugee_integration_failure: 0.08,
    trafficking_vulnerability: 0.05,
    return_impossibility: 0.04,
    UNHCR_funding_gap: 0.04,
    border_militarization_harm: 0.04,
    xenophobia_political_backlash: 0.04,
    protracted_displacement_duration: 0.05,
    education_access_gap: 0.06,
    healthcare_refugee_gap: 0.05,
    economic_exclusion_refugees: 0.07,
    secondary_displacement_risk: 0.04,
    // computed
    displacement_score: 5.15,
    protection_score: 4.65,
    integration_score: 7.15,
    systemic_score: 4.40,
    composite_score: 5.38,
    risk_level: "low",
    displacement_pattern: "none",
    severity: "déplacement_contenu",
    recommended_action: "veille_déplacement_préventive",
    signal: "🟢 Déplacement contenu — veille préventive maintenue",
  },
  {
    id: "RCE-005",
    displacement_type: "stateless_population",
    region: "SEA",
    displacement_volume: 0.75,
    climate_displacement_acceleration: 0.65,
    conflict_displacement_intensity: 0.80,
    asylum_system_collapse: 0.60,
    statelessness_risk: 0.90,
    host_country_capacity_overflow: 0.55,
    refugee_integration_failure: 0.65,
    trafficking_vulnerability: 0.70,
    return_impossibility: 0.88,
    UNHCR_funding_gap: 0.70,
    border_militarization_harm: 0.65,
    xenophobia_political_backlash: 0.65,
    protracted_displacement_duration: 0.75,
    education_access_gap: 0.55,
    healthcare_refugee_gap: 0.60,
    economic_exclusion_refugees: 0.60,
    secondary_displacement_risk: 0.68,
    // computed
    displacement_score: 72.75,
    protection_score: 73.25,
    integration_score: 60.75,
    systemic_score: 64.75,
    composite_score: 68.28,
    risk_level: "critical",
    displacement_pattern: "statelessness_crisis",
    severity: "crise_déplacement_catastrophique",
    recommended_action: "intervention_humanitaire_urgente",
    signal: "🔴 Crise déplacement catastrophique — intervention humanitaire d'urgence requise",
  },
  {
    id: "RCE-006",
    displacement_type: "economic_migrants",
    region: "LATAM",
    displacement_volume: 0.25,
    climate_displacement_acceleration: 0.22,
    conflict_displacement_intensity: 0.20,
    asylum_system_collapse: 0.23,
    statelessness_risk: 0.20,
    host_country_capacity_overflow: 0.22,
    refugee_integration_failure: 0.26,
    trafficking_vulnerability: 0.24,
    return_impossibility: 0.20,
    UNHCR_funding_gap: 0.20,
    border_militarization_harm: 0.22,
    xenophobia_political_backlash: 0.22,
    protracted_displacement_duration: 0.24,
    education_access_gap: 0.22,
    healthcare_refugee_gap: 0.20,
    economic_exclusion_refugees: 0.23,
    secondary_displacement_risk: 0.22,
    // computed
    displacement_score: 22.70,
    protection_score: 22.30,
    integration_score: 23.95,
    systemic_score: 21.70,
    composite_score: 22.71,
    risk_level: "moderate",
    displacement_pattern: "none",
    severity: "vulnérabilité_réfugiés_active",
    recommended_action: "renforcement_dispositif_accueil",
    signal: "🟡 Vulnérabilité réfugiés active — renforcement du dispositif d'accueil",
  },
  {
    id: "RCE-007",
    displacement_type: "conflict_induced",
    region: "HORN_AFRICA",
    displacement_volume: 0.45,
    climate_displacement_acceleration: 0.38,
    conflict_displacement_intensity: 0.42,
    asylum_system_collapse: 0.38,
    statelessness_risk: 0.40,
    host_country_capacity_overflow: 0.35,
    refugee_integration_failure: 0.48,
    trafficking_vulnerability: 0.85,
    return_impossibility: 0.42,
    UNHCR_funding_gap: 0.32,
    border_militarization_harm: 0.80,
    xenophobia_political_backlash: 0.35,
    protracted_displacement_duration: 0.50,
    education_access_gap: 0.38,
    healthcare_refugee_gap: 0.42,
    economic_exclusion_refugees: 0.42,
    secondary_displacement_risk: 0.55,
    // computed
    displacement_score: 41.80,
    protection_score: 72.00,
    integration_score: 43.40,
    systemic_score: 35.15,
    composite_score: 48.42,
    risk_level: "high",
    displacement_pattern: "refugee_trafficking_epidemic",
    severity: "déplacement_forcé_majeur",
    recommended_action: "mobilisation_protection_internationale",
    signal: "🟠 Déplacement forcé majeur détecté — mobilisation internationale nécessaire",
  },
  {
    id: "RCE-008",
    displacement_type: "protracted_refugee",
    region: "CENTRAL_ASIA",
    displacement_volume: 0.72,
    climate_displacement_acceleration: 0.55,
    conflict_displacement_intensity: 0.68,
    asylum_system_collapse: 0.65,
    statelessness_risk: 0.55,
    host_country_capacity_overflow: 0.60,
    refugee_integration_failure: 0.85,
    trafficking_vulnerability: 0.65,
    return_impossibility: 0.70,
    UNHCR_funding_gap: 0.72,
    border_militarization_harm: 0.60,
    xenophobia_political_backlash: 0.70,
    protracted_displacement_duration: 0.88,
    education_access_gap: 0.78,
    healthcare_refugee_gap: 0.75,
    economic_exclusion_refugees: 0.82,
    secondary_displacement_risk: 0.80,
    // computed
    displacement_score: 65.05,
    protection_score: 60.75,
    integration_score: 82.20,
    systemic_score: 68.70,
    composite_score: 68.99,
    risk_level: "critical",
    displacement_pattern: "protracted_displacement_trap",
    severity: "crise_déplacement_catastrophique",
    recommended_action: "intervention_humanitaire_urgente",
    signal: "🔴 Crise déplacement catastrophique — intervention humanitaire d'urgence requise",
  },
];

export async function GET(request: Request) {
  if (!SWARM_API_URL) {
    const { searchParams } = new URL(request.url);
    const risk    = searchParams.get("risk");
    const pattern = searchParams.get("pattern");

    let entities = [...mockEntities];
    if (risk)    entities = entities.filter((e) => e.risk_level === risk);
    if (pattern) entities = entities.filter((e) => e.displacement_pattern === pattern);

    const risk_distribution:     Record<string, number> = {};
    const pattern_distribution:  Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution:   Record<string, number> = {};
    let total_composite       = 0;
    let total_displacement    = 0;
    let critical              = 0;
    let high                  = 0;
    let moderate              = 0;
    let low                   = 0;

    for (const e of mockEntities) {
      risk_distribution[e.risk_level]             = (risk_distribution[e.risk_level] || 0) + 1;
      pattern_distribution[e.displacement_pattern] = (pattern_distribution[e.displacement_pattern] || 0) + 1;
      severity_distribution[e.severity]           = (severity_distribution[e.severity] || 0) + 1;
      action_distribution[e.recommended_action]   = (action_distribution[e.recommended_action] || 0) + 1;
      total_composite    += e.composite_score;
      total_displacement += e.displacement_volume;
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
        module_id:   385,
        module_name: "Global Refugee Crisis & Forced Displacement Intelligence Engine",
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
        avg_estimated_displacement_index: Math.round((avg_composite / 100 * 10) * 100) / 100,
      },
    } as Record<string, unknown>));
  }

  try {
    const { searchParams } = new URL(request.url);
    const url = new URL(`${SWARM_API_URL}/api/refugee-crisis-engine`);
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
