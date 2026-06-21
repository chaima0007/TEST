import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  // SWARM_API_URL guard — evaluated at module load time in dev,
  // at request time in production edge runtime (no-op if set).
}

const MOCK_ENTITIES = [
  // SEC-001 — EMEA, military_space → critical, orbital_warfare
  {
    id: "SEC-001", space_sector: "military_space", region: "EMEA",
    orbital_congestion_index: 0.65, space_debris_collision_risk: 0.60, launch_frequency_dominance: 0.55,
    satellite_dependency_vulnerability: 0.52, space_weaponization_level: 0.82,
    commercial_space_monopoly_risk: 0.50, space_resource_extraction_conflict: 0.30,
    regulatory_vacuum_exploitation: 0.50, space_sovereignty_erosion: 0.55,
    dual_use_technology_proliferation: 0.65, space_internet_dominance: 0.45,
    anti_satellite_capability: 0.75, space_supply_chain_fragility: 0.58,
    orbital_slot_competition: 0.52, space_insurance_systemic_risk: 0.48,
    low_earth_orbit_saturation: 0.60, cislunar_territorial_dispute: 0.48,
  },
  // SEC-002 — APAC, commercial_satellite → low, none
  {
    id: "SEC-002", space_sector: "commercial_satellite", region: "APAC",
    orbital_congestion_index: 0.12, space_debris_collision_risk: 0.10, launch_frequency_dominance: 0.15,
    satellite_dependency_vulnerability: 0.12, space_weaponization_level: 0.10,
    commercial_space_monopoly_risk: 0.12, space_resource_extraction_conflict: 0.10,
    regulatory_vacuum_exploitation: 0.12, space_sovereignty_erosion: 0.10,
    dual_use_technology_proliferation: 0.15, space_internet_dominance: 0.10,
    anti_satellite_capability: 0.12, space_supply_chain_fragility: 0.14,
    orbital_slot_competition: 0.12, space_insurance_systemic_risk: 0.10,
    low_earth_orbit_saturation: 0.15, cislunar_territorial_dispute: 0.10,
  },
  // SEC-003 — NOAM, launch_services → high, kessler_syndrome
  {
    id: "SEC-003", space_sector: "launch_services", region: "NOAM",
    orbital_congestion_index: 0.72, space_debris_collision_risk: 0.68, launch_frequency_dominance: 0.38,
    satellite_dependency_vulnerability: 0.42, space_weaponization_level: 0.30,
    commercial_space_monopoly_risk: 0.35, space_resource_extraction_conflict: 0.30,
    regulatory_vacuum_exploitation: 0.32, space_sovereignty_erosion: 0.30,
    dual_use_technology_proliferation: 0.35, space_internet_dominance: 0.30,
    anti_satellite_capability: 0.28, space_supply_chain_fragility: 0.38,
    orbital_slot_competition: 0.42, space_insurance_systemic_risk: 0.40,
    low_earth_orbit_saturation: 0.55, cislunar_territorial_dispute: 0.28,
  },
  // SEC-004 — LATAM, ground_infrastructure → low, none
  {
    id: "SEC-004", space_sector: "ground_infrastructure", region: "LATAM",
    orbital_congestion_index: 0.15, space_debris_collision_risk: 0.12, launch_frequency_dominance: 0.18,
    satellite_dependency_vulnerability: 0.15, space_weaponization_level: 0.12,
    commercial_space_monopoly_risk: 0.15, space_resource_extraction_conflict: 0.12,
    regulatory_vacuum_exploitation: 0.10, space_sovereignty_erosion: 0.14,
    dual_use_technology_proliferation: 0.16, space_internet_dominance: 0.12,
    anti_satellite_capability: 0.14, space_supply_chain_fragility: 0.16,
    orbital_slot_competition: 0.14, space_insurance_systemic_risk: 0.12,
    low_earth_orbit_saturation: 0.18, cislunar_territorial_dispute: 0.12,
  },
  // SEC-005 — NOAM, commercial_space → critical, commercial_colonization
  {
    id: "SEC-005", space_sector: "commercial_space", region: "NOAM",
    orbital_congestion_index: 0.62, space_debris_collision_risk: 0.60, launch_frequency_dominance: 0.65,
    satellite_dependency_vulnerability: 0.58, space_weaponization_level: 0.58,
    commercial_space_monopoly_risk: 0.78, space_resource_extraction_conflict: 0.40,
    regulatory_vacuum_exploitation: 0.55, space_sovereignty_erosion: 0.60,
    dual_use_technology_proliferation: 0.60, space_internet_dominance: 0.72,
    anti_satellite_capability: 0.55, space_supply_chain_fragility: 0.52,
    orbital_slot_competition: 0.58, space_insurance_systemic_risk: 0.55,
    low_earth_orbit_saturation: 0.58, cislunar_territorial_dispute: 0.52,
  },
  // SEC-006 — MEA, space_mining → moderate, none
  {
    id: "SEC-006", space_sector: "space_mining", region: "MEA",
    orbital_congestion_index: 0.32, space_debris_collision_risk: 0.28, launch_frequency_dominance: 0.32,
    satellite_dependency_vulnerability: 0.30, space_weaponization_level: 0.28,
    commercial_space_monopoly_risk: 0.30, space_resource_extraction_conflict: 0.20,
    regulatory_vacuum_exploitation: 0.30, space_sovereignty_erosion: 0.28,
    dual_use_technology_proliferation: 0.32, space_internet_dominance: 0.28,
    anti_satellite_capability: 0.30, space_supply_chain_fragility: 0.32,
    orbital_slot_competition: 0.30, space_insurance_systemic_risk: 0.28,
    low_earth_orbit_saturation: 0.30, cislunar_territorial_dispute: 0.25,
  },
  // SEC-007 — APAC, cislunar_operations → high, space_resource_war
  {
    id: "SEC-007", space_sector: "cislunar_operations", region: "APAC",
    orbital_congestion_index: 0.45, space_debris_collision_risk: 0.42, launch_frequency_dominance: 0.42,
    satellite_dependency_vulnerability: 0.45, space_weaponization_level: 0.35,
    commercial_space_monopoly_risk: 0.40, space_resource_extraction_conflict: 0.75,
    regulatory_vacuum_exploitation: 0.50, space_sovereignty_erosion: 0.55,
    dual_use_technology_proliferation: 0.38, space_internet_dominance: 0.38,
    anti_satellite_capability: 0.32, space_supply_chain_fragility: 0.48,
    orbital_slot_competition: 0.45, space_insurance_systemic_risk: 0.42,
    low_earth_orbit_saturation: 0.48, cislunar_territorial_dispute: 0.68,
  },
  // SEC-008 — EMEA, regulatory_space → critical, regulatory_vacuum_crisis
  {
    id: "SEC-008", space_sector: "regulatory_space", region: "EMEA",
    orbital_congestion_index: 0.65, space_debris_collision_risk: 0.62, launch_frequency_dominance: 0.60,
    satellite_dependency_vulnerability: 0.58, space_weaponization_level: 0.60,
    commercial_space_monopoly_risk: 0.62, space_resource_extraction_conflict: 0.40,
    regulatory_vacuum_exploitation: 0.78, space_sovereignty_erosion: 0.72,
    dual_use_technology_proliferation: 0.62, space_internet_dominance: 0.58,
    anti_satellite_capability: 0.58, space_supply_chain_fragility: 0.60,
    orbital_slot_competition: 0.58, space_insurance_systemic_risk: 0.55,
    low_earth_orbit_saturation: 0.60, cislunar_territorial_dispute: 0.55,
  },
];

type SecEntity = typeof MOCK_ENTITIES[0];

function congestionScore(e: SecEntity): number {
  return Math.round((e.orbital_congestion_index * 0.4 + e.space_debris_collision_risk * 0.35 + e.low_earth_orbit_saturation * 0.25) * 100 * 100) / 100;
}
function militarizationScore(e: SecEntity): number {
  return Math.round((e.space_weaponization_level * 0.4 + e.anti_satellite_capability * 0.35 + e.dual_use_technology_proliferation * 0.25) * 100 * 100) / 100;
}
function monopolyScore(e: SecEntity): number {
  return Math.round((e.commercial_space_monopoly_risk * 0.4 + e.space_internet_dominance * 0.35 + e.launch_frequency_dominance * 0.25) * 100 * 100) / 100;
}
function sovereigntyScore(e: SecEntity): number {
  return Math.round((e.space_sovereignty_erosion * 0.4 + e.regulatory_vacuum_exploitation * 0.35 + e.cislunar_territorial_dispute * 0.25) * 100 * 100) / 100;
}
function compositeScore(cg: number, ml: number, mo: number, sv: number): number {
  return Math.round((cg * 0.30 + ml * 0.25 + mo * 0.25 + sv * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function spacePattern(e: SecEntity): string {
  if (e.space_weaponization_level >= 0.70 && e.anti_satellite_capability >= 0.65) return "orbital_warfare";
  if (e.orbital_congestion_index >= 0.70 && e.space_debris_collision_risk >= 0.65) return "kessler_syndrome";
  if (e.commercial_space_monopoly_risk >= 0.70 && e.space_internet_dominance >= 0.65) return "commercial_colonization";
  if (e.space_resource_extraction_conflict >= 0.70 && e.cislunar_territorial_dispute >= 0.65) return "space_resource_war";
  if (e.regulatory_vacuum_exploitation >= 0.70 && e.space_sovereignty_erosion >= 0.65) return "regulatory_vacuum_crisis";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_orbitale_systémique";
  if (composite >= 40) return "escalade_spatiale_majeure";
  if (composite >= 20) return "tension_orbitale";
  return "espace_stable";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_souveraineté_spatiale_urgente";
  if (risk === "high") return "diplomatie_spatiale_activée";
  if (risk === "moderate") return "surveillance_orbital_renforcée";
  return "monitoring_continu";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise orbitale systémique — espace sous tension extrême";
  if (risk === "high") return "🟠 Escalade spatiale majeure détectée";
  if (risk === "moderate") return "🟡 Tensions orbitales en développement";
  return "🟢 Environnement spatial stable";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const cg = congestionScore(e);
      const ml = militarizationScore(e);
      const mo = monopolyScore(e);
      const sv = sovereigntyScore(e);
      const comp = compositeScore(cg, ml, mo, sv);
      const risk = riskLevel(comp);
      const pat = spacePattern(e);
      const sev = severity(comp);
      const action = recommendedAction(risk);
      const sig = signal(risk);
      return {
        id: e.entity_id,
        space_sector: e.space_sector,
        region: e.region,
        congestion_score: cg,
        militarization_score: ml,
        monopoly_score: mo,
        sovereignty_score: sv,
        composite_score: comp,
        risk_level: risk,
        space_pattern: pat,
        severity: sev,
        recommended_action: action,
        signal: sig,
        orbital_congestion_index: e.orbital_congestion_index,
        space_weaponization_level: e.space_weaponization_level,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let totalComp = 0;
    let criticalCount = 0;
    let highCount = 0;
    let moderateCount = 0;
    let lowCount = 0;
    let totalCongestion = 0;

    for (const ent of entities) {
      rc[ent.risk_level] = (rc[ent.risk_level] || 0) + 1;
      pc[ent.space_pattern] = (pc[ent.space_pattern] || 0) + 1;
      sc[ent.severity] = (sc[ent.severity] || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      totalComp += ent.composite_score;
      totalCongestion += ent.congestion_score;
      if (ent.risk_level === "critical") criticalCount++;
      else if (ent.risk_level === "high") highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else lowCount++;
    }

    const n = entities.length;
    const avgComp = totalComp / n;

    const summary = {
      module_id: 331,
      module_name: "Space Economy & Orbital Sovereignty Intelligence Engine",
      total_entities: n,
      critical_count: criticalCount,
      high_count: highCount,
      moderate_count: moderateCount,
      low_count: lowCount,
      avg_composite: Math.round(avgComp * 100) / 100,
      pattern_distribution: pc,
      risk_distribution: rc,
      severity_distribution: sc,
      action_distribution: ac,
      avg_estimated_orbital_risk_index: Math.round(avgComp / 100 * 10 * 100) / 100,
      avg_congestion_score: Math.round(totalCongestion / n * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "space-economy-sovereignty-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/space-economy-sovereignty-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "space-economy-sovereignty-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "space-economy-sovereignty-engine"),
      { status: 502 }
    );
  }
}
