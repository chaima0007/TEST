import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// 8 mock entities covering all 5 patterns and all 4 risk levels
// CHE-001: critical / active_cultural_destruction
// CHE-002: low / none
// CHE-003: high / intangible_heritage_collapse
// CHE-004: low / none
// CHE-005: critical / cultural_commodification_crisis
// CHE-006: moderate / none
// CHE-007: high / indigenous_erasure
// CHE-008: critical / cultural_memory_implosion
const MOCK_ENTITIES = [
  {
    id: "CHE-001", cultural_domain: "sites_patrimoine_mondial", region: "MEA",
    heritage_physical_destruction_rate: 0.88, cultural_gentrification_displacement: 0.60, digital_colonialism_cultural_impact: 0.55,
    intangible_heritage_extinction_speed: 0.58, cultural_commodification_distortion: 0.55, AI_cultural_appropriation_risk: 0.50,
    conflict_cultural_targeting_index: 0.82, climate_cultural_heritage_threat: 0.65, tourism_overcrowding_degradation: 0.50,
    cultural_funding_collapse: 0.60, indigenous_cultural_sovereignty_erosion: 0.55, language_heritage_extinction_rate: 0.52,
    institutional_cultural_memory_loss: 0.58, global_brand_monoculture_dominance: 0.50, cultural_resistance_suppression: 0.62,
    diaspora_cultural_connection_severing: 0.55, generational_cultural_transmission_failure: 0.60,
  },
  {
    id: "CHE-002", cultural_domain: "arts_vivants", region: "EMEA",
    heritage_physical_destruction_rate: 0.08, cultural_gentrification_displacement: 0.10, digital_colonialism_cultural_impact: 0.12,
    intangible_heritage_extinction_speed: 0.10, cultural_commodification_distortion: 0.08, AI_cultural_appropriation_risk: 0.10,
    conflict_cultural_targeting_index: 0.08, climate_cultural_heritage_threat: 0.10, tourism_overcrowding_degradation: 0.12,
    cultural_funding_collapse: 0.10, indigenous_cultural_sovereignty_erosion: 0.08, language_heritage_extinction_rate: 0.10,
    institutional_cultural_memory_loss: 0.08, global_brand_monoculture_dominance: 0.10, cultural_resistance_suppression: 0.08,
    diaspora_cultural_connection_severing: 0.10, generational_cultural_transmission_failure: 0.12,
  },
  {
    id: "CHE-003", cultural_domain: "traditions_orales", region: "APAC",
    heritage_physical_destruction_rate: 0.42, cultural_gentrification_displacement: 0.45, digital_colonialism_cultural_impact: 0.48,
    intangible_heritage_extinction_speed: 0.82, cultural_commodification_distortion: 0.45, AI_cultural_appropriation_risk: 0.42,
    conflict_cultural_targeting_index: 0.40, climate_cultural_heritage_threat: 0.45, tourism_overcrowding_degradation: 0.40,
    cultural_funding_collapse: 0.45, indigenous_cultural_sovereignty_erosion: 0.42, language_heritage_extinction_rate: 0.45,
    institutional_cultural_memory_loss: 0.40, global_brand_monoculture_dominance: 0.42, cultural_resistance_suppression: 0.40,
    diaspora_cultural_connection_severing: 0.45, generational_cultural_transmission_failure: 0.75,
  },
  {
    id: "CHE-004", cultural_domain: "musiques_traditionnelles", region: "NOAM",
    heritage_physical_destruction_rate: 0.10, cultural_gentrification_displacement: 0.12, digital_colonialism_cultural_impact: 0.10,
    intangible_heritage_extinction_speed: 0.12, cultural_commodification_distortion: 0.10, AI_cultural_appropriation_risk: 0.12,
    conflict_cultural_targeting_index: 0.08, climate_cultural_heritage_threat: 0.10, tourism_overcrowding_degradation: 0.10,
    cultural_funding_collapse: 0.12, indigenous_cultural_sovereignty_erosion: 0.10, language_heritage_extinction_rate: 0.08,
    institutional_cultural_memory_loss: 0.10, global_brand_monoculture_dominance: 0.12, cultural_resistance_suppression: 0.10,
    diaspora_cultural_connection_severing: 0.08, generational_cultural_transmission_failure: 0.10,
  },
  {
    id: "CHE-005", cultural_domain: "artisanat_identitaire", region: "LATAM",
    heritage_physical_destruction_rate: 0.55, cultural_gentrification_displacement: 0.60, digital_colonialism_cultural_impact: 0.62,
    intangible_heritage_extinction_speed: 0.55, cultural_commodification_distortion: 0.88, AI_cultural_appropriation_risk: 0.65,
    conflict_cultural_targeting_index: 0.50, climate_cultural_heritage_threat: 0.52, tourism_overcrowding_degradation: 0.75,
    cultural_funding_collapse: 0.60, indigenous_cultural_sovereignty_erosion: 0.58, language_heritage_extinction_rate: 0.50,
    institutional_cultural_memory_loss: 0.55, global_brand_monoculture_dominance: 0.82, cultural_resistance_suppression: 0.62,
    diaspora_cultural_connection_severing: 0.55, generational_cultural_transmission_failure: 0.55,
  },
  {
    id: "CHE-006", cultural_domain: "architecture_vernaculaire", region: "EMEA",
    heritage_physical_destruction_rate: 0.28, cultural_gentrification_displacement: 0.30, digital_colonialism_cultural_impact: 0.28,
    intangible_heritage_extinction_speed: 0.30, cultural_commodification_distortion: 0.28, AI_cultural_appropriation_risk: 0.30,
    conflict_cultural_targeting_index: 0.25, climate_cultural_heritage_threat: 0.30, tourism_overcrowding_degradation: 0.32,
    cultural_funding_collapse: 0.28, indigenous_cultural_sovereignty_erosion: 0.30, language_heritage_extinction_rate: 0.28,
    institutional_cultural_memory_loss: 0.30, global_brand_monoculture_dominance: 0.28, cultural_resistance_suppression: 0.25,
    diaspora_cultural_connection_severing: 0.28, generational_cultural_transmission_failure: 0.30,
  },
  {
    id: "CHE-007", cultural_domain: "langues_autochtones", region: "APAC",
    heritage_physical_destruction_rate: 0.45, cultural_gentrification_displacement: 0.48, digital_colonialism_cultural_impact: 0.50,
    intangible_heritage_extinction_speed: 0.48, cultural_commodification_distortion: 0.42, AI_cultural_appropriation_risk: 0.45,
    conflict_cultural_targeting_index: 0.40, climate_cultural_heritage_threat: 0.45, tourism_overcrowding_degradation: 0.42,
    cultural_funding_collapse: 0.45, indigenous_cultural_sovereignty_erosion: 0.82, language_heritage_extinction_rate: 0.78,
    institutional_cultural_memory_loss: 0.45, global_brand_monoculture_dominance: 0.42, cultural_resistance_suppression: 0.48,
    diaspora_cultural_connection_severing: 0.42, generational_cultural_transmission_failure: 0.45,
  },
  {
    id: "CHE-008", cultural_domain: "archives_mémoire_collective", region: "NOAM",
    heritage_physical_destruction_rate: 0.62, cultural_gentrification_displacement: 0.65, digital_colonialism_cultural_impact: 0.68,
    intangible_heritage_extinction_speed: 0.65, cultural_commodification_distortion: 0.60, AI_cultural_appropriation_risk: 0.65,
    conflict_cultural_targeting_index: 0.60, climate_cultural_heritage_threat: 0.65, tourism_overcrowding_degradation: 0.60,
    cultural_funding_collapse: 0.65, indigenous_cultural_sovereignty_erosion: 0.62, language_heritage_extinction_rate: 0.60,
    institutional_cultural_memory_loss: 0.85, global_brand_monoculture_dominance: 0.62, cultural_resistance_suppression: 0.65,
    diaspora_cultural_connection_severing: 0.78, generational_cultural_transmission_failure: 0.65,
  },
];

type MockEntity = typeof MOCK_ENTITIES[0];

function destructionScore(e: MockEntity): number {
  return Math.round((e.heritage_physical_destruction_rate * 0.4 + e.conflict_cultural_targeting_index * 0.35 + e.climate_cultural_heritage_threat * 0.25) * 100 * 100) / 100;
}
function erosionScore(e: MockEntity): number {
  return Math.round((e.intangible_heritage_extinction_speed * 0.4 + e.language_heritage_extinction_rate * 0.35 + e.generational_cultural_transmission_failure * 0.25) * 100 * 100) / 100;
}
function commodificationScore(e: MockEntity): number {
  return Math.round((e.cultural_commodification_distortion * 0.4 + e.global_brand_monoculture_dominance * 0.35 + e.tourism_overcrowding_degradation * 0.25) * 100 * 100) / 100;
}
function sovereigntyScore(e: MockEntity): number {
  return Math.round((e.indigenous_cultural_sovereignty_erosion * 0.4 + e.cultural_resistance_suppression * 0.35 + e.cultural_funding_collapse * 0.25) * 100 * 100) / 100;
}
function compositeScore(dest: number, eros: number, comm: number, sov: number): number {
  return Math.round((dest * 0.30 + eros * 0.25 + comm * 0.25 + sov * 0.20) * 100) / 100;
}
function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}
function culturalPattern(e: MockEntity): string {
  if (e.heritage_physical_destruction_rate >= 0.70 && e.conflict_cultural_targeting_index >= 0.65) return "active_cultural_destruction";
  if (e.intangible_heritage_extinction_speed >= 0.70 && e.generational_cultural_transmission_failure >= 0.65) return "intangible_heritage_collapse";
  if (e.cultural_commodification_distortion >= 0.70 && e.global_brand_monoculture_dominance >= 0.65) return "cultural_commodification_crisis";
  if (e.indigenous_cultural_sovereignty_erosion >= 0.70 && e.language_heritage_extinction_rate >= 0.65) return "indigenous_erasure";
  if (e.institutional_cultural_memory_loss >= 0.70 && e.diaspora_cultural_connection_severing >= 0.65) return "cultural_memory_implosion";
  return "none";
}
function severity(risk: string): string {
  const map: Record<string, string> = {
    critical: "destruction_patrimoine_systémique",
    high:     "crise_capital_culturel_majeure",
    moderate: "érosion_culturelle_structurelle",
    low:      "patrimoine_relativement_préservé",
  };
  return map[risk] ?? risk;
}
function recommendedAction(risk: string): string {
  const map: Record<string, string> = {
    critical: "protection_patrimoine_urgente",
    high:     "stratégie_préservation_culturelle_activée",
    moderate: "renforcement_transmission_culturelle",
    low:      "veille_patrimoine_continue",
  };
  return map[risk] ?? risk;
}
function signal(risk: string): string {
  const map: Record<string, string> = {
    critical: "🔴 Destruction patrimoine systémique — capital culturel en péril",
    high:     "🟠 Crise capital culturel majeure détectée",
    moderate: "🟡 Érosion culturelle structurelle active",
    low:      "🟢 Patrimoine culturel relativement préservé",
  };
  return map[risk] ?? risk;
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const dest = destructionScore(e);
      const eros = erosionScore(e);
      const comm = commodificationScore(e);
      const sov  = sovereigntyScore(e);
      const comp = compositeScore(dest, eros, comm, sov);
      const risk = riskLevel(comp);
      const pattern = culturalPattern(e);
      const sev = severity(risk);
      const action = recommendedAction(risk);
      const sig = signal(risk);
      return {
        id: e.entity_id,
        cultural_domain: e.cultural_domain,
        region: e.region,
        destruction_score: dest,
        erosion_score: eros,
        commodification_score: comm,
        sovereignty_score: sov,
        composite_score: comp,
        risk_level: risk,
        cultural_pattern: pattern,
        severity: sev,
        recommended_action: action,
        signal: sig,
        heritage_physical_destruction_rate: e.heritage_physical_destruction_rate,
        indigenous_cultural_sovereignty_erosion: e.indigenous_cultural_sovereignty_erosion,
      };
    });

    const riskDist: Record<string, number>     = {};
    const patDist: Record<string, number>      = {};
    const sevDist: Record<string, number>      = {};
    const actionDist: Record<string, number>   = {};
    let totalComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      riskDist[ent.risk_level]         = (riskDist[ent.risk_level]         || 0) + 1;
      patDist[ent.cultural_pattern]    = (patDist[ent.cultural_pattern]    || 0) + 1;
      sevDist[ent.severity]            = (sevDist[ent.severity]            || 0) + 1;
      actionDist[ent.recommended_action] = (actionDist[ent.recommended_action] || 0) + 1;
      totalComp += ent.composite_score;
      if (ent.risk_level === "critical") criticalCount++;
      else if (ent.risk_level === "high") highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(totalComp / n * 100) / 100;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id: 341,
        module_name: "Cultural Capital & Heritage Destruction Intelligence Engine",
        total_entities: n,
        critical_count: criticalCount,
        high_count: highCount,
        moderate_count: moderateCount,
        low_count: lowCount,
        avg_composite: avgComposite,
        pattern_distribution: patDist,
        risk_distribution: riskDist,
        severity_distribution: sevDist,
        action_distribution: actionDist,
        avg_estimated_heritage_risk_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
      },
    } as Record<string, unknown>, "cultural-heritage-engine"));
  }

  try {
    const res = await fetch(`${SWARM_API_URL}/cultural-heritage-engine`);
    if (res.ok) return NextResponse.json(sealResponse(await res.json() as Record<string, unknown>, "cultural-heritage-engine"));
  } catch {}

  return NextResponse.json(
    sealResponse({ error: "Upstream unavailable" } as Record<string, unknown>, "cultural-heritage-engine"),
    { status: 502 }
  );
}
