import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) { /* offline mock mode */ }

const SWARM_API_URL = process.env.SWARM_API_URL;

// 8 mock entities covering all 5 patterns and all 4 risk levels
// DIE-001: critical, biometric_surveillance_state   (biometric>0.85 AND government_coercion>0.80, composite>=60)
// DIE-002: low,      none                           (all low, composite<20)
// DIE-003: high,     identity_monopoly_empire       (identity_monopoly>0.85 AND private_capture>0.80, composite>=40<60)
// DIE-004: low,      none                           (all low, composite<20)
// DIE-005: critical, identity_exclusion_crisis      (exclusion_risk>0.85 AND stateless>0.80, composite>=60)
// DIE-006: moderate, none                           (composite>=20<40)
// DIE-007: high,     identity_weaponization         (weaponization_risk>0.80 AND democratic_manip>0.75, composite>=40<60)
// DIE-008: critical, sovereign_identity_collapse    (self_sovereign_suppression>0.80 AND consent_erosion>0.75, composite>=60)

const mockEntities = [
  {
    entity_id: "DIE-001",
    identity_system: "etat_biometrique_centralise",
    region: "APAC",
    biometric_surveillance_integration: 0.88,
    identity_monopoly_capture: 0.60,
    exclusion_risk: 0.60,
    data_breach_vulnerability: 0.65,
    government_identity_coercion: 0.85,
    private_identity_capture: 0.58,
    interoperability_failure: 0.50,
    self_sovereign_suppression: 0.65,
    digital_twin_identity_risk: 0.72,
    demographic_targeting_capacity: 0.58,
    identity_weaponization_risk: 0.60,
    stateless_person_exclusion: 0.55,
    cross_border_identity_friction: 0.62,
    consent_identity_erosion: 0.62,
    algorithmic_identity_discrimination: 0.60,
    identity_theft_amplification: 0.58,
    democratic_identity_manipulation: 0.55,
    // computed
    surveillance_score: 82.95,
    exclusion_score: 55.75,
    sovereignty_score: 62.2,
    weaponization_score: 57.75,
    composite_score: 65.92,
    risk_level: "critical",
    identity_pattern: "biometric_surveillance_state",
    severity: "souveraineté_identitaire_effondrée",
    recommended_action: "restauration_souveraineté_identitaire_urgente",
    signal: "🔴 Souveraineté identitaire effondrée — contrôle systémique de l'identité",
  },
  {
    entity_id: "DIE-002",
    identity_system: "identite_liberale_ouverte",
    region: "EMEA",
    biometric_surveillance_integration: 0.07,
    identity_monopoly_capture: 0.06,
    exclusion_risk: 0.07,
    data_breach_vulnerability: 0.08,
    government_identity_coercion: 0.06,
    private_identity_capture: 0.07,
    interoperability_failure: 0.05,
    self_sovereign_suppression: 0.06,
    digital_twin_identity_risk: 0.07,
    demographic_targeting_capacity: 0.06,
    identity_weaponization_risk: 0.05,
    stateless_person_exclusion: 0.06,
    cross_border_identity_friction: 0.07,
    consent_identity_erosion: 0.06,
    algorithmic_identity_discrimination: 0.07,
    identity_theft_amplification: 0.06,
    democratic_identity_manipulation: 0.05,
    // computed
    surveillance_score: 6.65,
    exclusion_score: 6.15,
    sovereignty_score: 6.25,
    weaponization_score: 5.25,
    composite_score: 6.15,
    risk_level: "low",
    identity_pattern: "none",
    severity: "risque_identitaire_contenu",
    recommended_action: "veille_identité_numérique",
    signal: "🟢 Risque identitaire limité et contenu",
  },
  {
    entity_id: "DIE-003",
    identity_system: "monopole_identite_prive",
    region: "NAMER",
    biometric_surveillance_integration: 0.45,
    identity_monopoly_capture: 0.88,
    exclusion_risk: 0.50,
    data_breach_vulnerability: 0.55,
    government_identity_coercion: 0.42,
    private_identity_capture: 0.82,
    interoperability_failure: 0.42,
    self_sovereign_suppression: 0.78,
    digital_twin_identity_risk: 0.48,
    demographic_targeting_capacity: 0.42,
    identity_weaponization_risk: 0.45,
    stateless_person_exclusion: 0.45,
    cross_border_identity_friction: 0.50,
    consent_identity_erosion: 0.75,
    algorithmic_identity_discrimination: 0.52,
    identity_theft_amplification: 0.48,
    democratic_identity_manipulation: 0.40,
    // computed
    surveillance_score: 44.70,
    exclusion_score: 46.25,
    sovereignty_score: 77.95,
    weaponization_score: 42.50,
    composite_score: 52.96,
    risk_level: "high",
    identity_pattern: "identity_monopoly_empire",
    severity: "identité_numérique_sous_contrôle",
    recommended_action: "protection_identité_décentralisée",
    signal: "🟠 Identité numérique sous contrôle avancé détecté",
  },
  {
    entity_id: "DIE-004",
    identity_system: "systeme_identite_distribue",
    region: "LATAM",
    biometric_surveillance_integration: 0.09,
    identity_monopoly_capture: 0.08,
    exclusion_risk: 0.09,
    data_breach_vulnerability: 0.10,
    government_identity_coercion: 0.08,
    private_identity_capture: 0.09,
    interoperability_failure: 0.07,
    self_sovereign_suppression: 0.08,
    digital_twin_identity_risk: 0.09,
    demographic_targeting_capacity: 0.08,
    identity_weaponization_risk: 0.07,
    stateless_person_exclusion: 0.08,
    cross_border_identity_friction: 0.09,
    consent_identity_erosion: 0.08,
    algorithmic_identity_discrimination: 0.09,
    identity_theft_amplification: 0.08,
    democratic_identity_manipulation: 0.07,
    // computed
    surveillance_score: 8.65,
    exclusion_score: 8.15,
    sovereignty_score: 8.25,
    weaponization_score: 7.25,
    composite_score: 8.14,
    risk_level: "low",
    identity_pattern: "none",
    severity: "risque_identitaire_contenu",
    recommended_action: "veille_identité_numérique",
    signal: "🟢 Risque identitaire limité et contenu",
  },
  {
    entity_id: "DIE-005",
    identity_system: "systeme_exclusion_identitaire",
    region: "MEA",
    biometric_surveillance_integration: 0.55,
    identity_monopoly_capture: 0.55,
    exclusion_risk: 0.88,
    data_breach_vulnerability: 0.62,
    government_identity_coercion: 0.50,
    private_identity_capture: 0.60,
    interoperability_failure: 0.70,
    self_sovereign_suppression: 0.72,
    digital_twin_identity_risk: 0.60,
    demographic_targeting_capacity: 0.62,
    identity_weaponization_risk: 0.65,
    stateless_person_exclusion: 0.82,
    cross_border_identity_friction: 0.75,
    consent_identity_erosion: 0.68,
    algorithmic_identity_discrimination: 0.70,
    identity_theft_amplification: 0.60,
    democratic_identity_manipulation: 0.60,
    // computed
    surveillance_score: 54.50,
    exclusion_score: 81.40,
    sovereignty_score: 67.60,
    weaponization_score: 62.50,
    composite_score: 66.10,
    risk_level: "critical",
    identity_pattern: "identity_exclusion_crisis",
    severity: "souveraineté_identitaire_effondrée",
    recommended_action: "restauration_souveraineté_identitaire_urgente",
    signal: "🔴 Souveraineté identitaire effondrée — contrôle systémique de l'identité",
  },
  {
    entity_id: "DIE-006",
    identity_system: "identite_numerique_partielle",
    region: "EMEA",
    biometric_surveillance_integration: 0.25,
    identity_monopoly_capture: 0.22,
    exclusion_risk: 0.28,
    data_breach_vulnerability: 0.30,
    government_identity_coercion: 0.22,
    private_identity_capture: 0.22,
    interoperability_failure: 0.25,
    self_sovereign_suppression: 0.24,
    digital_twin_identity_risk: 0.28,
    demographic_targeting_capacity: 0.25,
    identity_weaponization_risk: 0.26,
    stateless_person_exclusion: 0.22,
    cross_border_identity_friction: 0.28,
    consent_identity_erosion: 0.25,
    algorithmic_identity_discrimination: 0.26,
    identity_theft_amplification: 0.24,
    democratic_identity_manipulation: 0.24,
    // computed
    surveillance_score: 24.70,
    exclusion_score: 25.15,
    sovereignty_score: 23.85,
    weaponization_score: 25.05,
    composite_score: 24.67,
    risk_level: "moderate",
    identity_pattern: "none",
    severity: "vulnérabilité_identitaire_structurelle",
    recommended_action: "renforcement_droits_identitaires",
    signal: "🟡 Vulnérabilité identitaire structurelle active",
  },
  {
    entity_id: "DIE-007",
    identity_system: "identite_arme_politique",
    region: "APAC",
    biometric_surveillance_integration: 0.48,
    identity_monopoly_capture: 0.50,
    exclusion_risk: 0.50,
    data_breach_vulnerability: 0.55,
    government_identity_coercion: 0.45,
    private_identity_capture: 0.48,
    interoperability_failure: 0.45,
    self_sovereign_suppression: 0.55,
    digital_twin_identity_risk: 0.50,
    demographic_targeting_capacity: 0.68,
    identity_weaponization_risk: 0.82,
    stateless_person_exclusion: 0.48,
    cross_border_identity_friction: 0.52,
    consent_identity_erosion: 0.52,
    algorithmic_identity_discrimination: 0.55,
    identity_theft_amplification: 0.50,
    democratic_identity_manipulation: 0.78,
    // computed
    surveillance_score: 47.45,
    exclusion_score: 48.05,
    sovereignty_score: 52.20,
    weaponization_score: 77.10,
    composite_score: 54.72,
    risk_level: "high",
    identity_pattern: "identity_weaponization",
    severity: "identité_numérique_sous_contrôle",
    recommended_action: "protection_identité_décentralisée",
    signal: "🟠 Identité numérique sous contrôle avancé détecté",
  },
  {
    entity_id: "DIE-008",
    identity_system: "souverainete_identitaire_supprimee",
    region: "NAMER",
    biometric_surveillance_integration: 0.62,
    identity_monopoly_capture: 0.60,
    exclusion_risk: 0.60,
    data_breach_vulnerability: 0.68,
    government_identity_coercion: 0.58,
    private_identity_capture: 0.55,
    interoperability_failure: 0.58,
    self_sovereign_suppression: 0.85,
    digital_twin_identity_risk: 0.65,
    demographic_targeting_capacity: 0.62,
    identity_weaponization_risk: 0.65,
    stateless_person_exclusion: 0.55,
    cross_border_identity_friction: 0.62,
    consent_identity_erosion: 0.80,
    algorithmic_identity_discrimination: 0.68,
    identity_theft_amplification: 0.65,
    democratic_identity_manipulation: 0.60,
    // computed
    surveillance_score: 61.35,
    exclusion_score: 57.75,
    sovereignty_score: 75.75,
    weaponization_score: 62.50,
    composite_score: 64.28,
    risk_level: "critical",
    identity_pattern: "sovereign_identity_collapse",
    severity: "souveraineté_identitaire_effondrée",
    recommended_action: "restauration_souveraineté_identitaire_urgente",
    signal: "🔴 Souveraineté identitaire effondrée — contrôle systémique de l'identité",
  },
];

export async function GET(request: Request) {
  if (!process.env.SWARM_API_URL) {
    const { searchParams } = new URL(request.url);
    const risk    = searchParams.get("risk");
    const pattern = searchParams.get("pattern");

    let entities = [...mockEntities];
    if (risk)    entities = entities.filter((e) => e.risk_level === risk);
    if (pattern) entities = entities.filter((e) => e.identity_pattern === pattern);

    const risk_distribution:     Record<string, number> = {};
    const pattern_distribution:  Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution:   Record<string, number> = {};
    let total_composite              = 0;
    let total_biometric_surveillance = 0;
    let critical_count  = 0;
    let high_count      = 0;
    let moderate_count  = 0;
    let low_count       = 0;

    for (const e of mockEntities) {
      risk_distribution[e.risk_level]              = (risk_distribution[e.risk_level] || 0) + 1;
      pattern_distribution[e.identity_pattern]     = (pattern_distribution[e.identity_pattern] || 0) + 1;
      severity_distribution[e.severity]            = (severity_distribution[e.severity] || 0) + 1;
      action_distribution[e.recommended_action]    = (action_distribution[e.recommended_action] || 0) + 1;
      total_composite              += e.composite_score;
      total_biometric_surveillance += e.biometric_surveillance_integration;
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
        module_id:   376,
        module_name: "Digital Identity & Decentralized Sovereignty Intelligence Engine",
        total:            n,
        critical:         critical_count,
        high:             high_count,
        moderate:         moderate_count,
        low:              low_count,
        avg_composite,
        pattern_distribution,
        risk_distribution,
        severity_distribution,
        action_distribution,
        avg_estimated_identity_sovereignty_index: Math.round((avg_composite / 100 * 10) * 100) / 100,
        avg_biometric_surveillance: Math.round((total_biometric_surveillance / n) * 100) / 100,
      },
    } as Record<string, unknown>));
  }

  try {
    const { searchParams } = new URL(request.url);
    const url = new URL(`${SWARM_API_URL}/api/digital-identity-engine`);
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
