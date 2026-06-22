import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // SE-001 — EMEA, satellite_operations → critical, orbital_collision_cascade
  {
    id: "SE-001", space_segment: "satellite_operations", region: "EMEA",
    orbital_asset_concentration: 0.72, launch_cost_competitiveness: 0.30,
    satellite_constellation_density: 0.78, space_debris_collision_risk: 0.82,
    spectrum_congestion: 0.68, space_sovereignty_gap: 0.55, launch_vehicle_dependency: 0.60,
    ground_infrastructure_resilience: 0.35, space_weather_vulnerability: 0.65,
    commercialization_readiness: 0.40, space_mining_viability: 0.25,
    anti_satellite_threat: 0.55, orbital_slot_scarcity: 0.70, space_insurance_gap: 0.60,
    regulatory_space_framework: 0.35, international_cooperation_index: 0.40,
    new_space_innovation_rate: 0.38,
  },
  // SE-002 — APAC, launch_services → low, space_optimum/none
  {
    id: "SE-002", space_segment: "launch_services", region: "APAC",
    orbital_asset_concentration: 0.15, launch_cost_competitiveness: 0.88,
    satellite_constellation_density: 0.20, space_debris_collision_risk: 0.12,
    spectrum_congestion: 0.18, space_sovereignty_gap: 0.10, launch_vehicle_dependency: 0.15,
    ground_infrastructure_resilience: 0.90, space_weather_vulnerability: 0.12,
    commercialization_readiness: 0.85, space_mining_viability: 0.75,
    anti_satellite_threat: 0.10, orbital_slot_scarcity: 0.15, space_insurance_gap: 0.12,
    regulatory_space_framework: 0.88, international_cooperation_index: 0.85,
    new_space_innovation_rate: 0.88,
  },
  // SE-003 — NOAM, space_mining → high, space_sovereignty_loss
  {
    id: "SE-003", space_segment: "space_mining", region: "NOAM",
    orbital_asset_concentration: 0.55, launch_cost_competitiveness: 0.45,
    satellite_constellation_density: 0.48, space_debris_collision_risk: 0.40,
    spectrum_congestion: 0.42, space_sovereignty_gap: 0.75, launch_vehicle_dependency: 0.50,
    ground_infrastructure_resilience: 0.55, space_weather_vulnerability: 0.48,
    commercialization_readiness: 0.50, space_mining_viability: 0.60,
    anti_satellite_threat: 0.65, orbital_slot_scarcity: 0.45, space_insurance_gap: 0.50,
    regulatory_space_framework: 0.40, international_cooperation_index: 0.38,
    new_space_innovation_rate: 0.52,
  },
  // SE-004 — LATAM, launch_services → low, space_optimum/none
  {
    id: "SE-004", space_segment: "launch_services", region: "LATAM",
    orbital_asset_concentration: 0.18, launch_cost_competitiveness: 0.80,
    satellite_constellation_density: 0.22, space_debris_collision_risk: 0.15,
    spectrum_congestion: 0.20, space_sovereignty_gap: 0.18, launch_vehicle_dependency: 0.20,
    ground_infrastructure_resilience: 0.82, space_weather_vulnerability: 0.18,
    commercialization_readiness: 0.78, space_mining_viability: 0.55,
    anti_satellite_threat: 0.15, orbital_slot_scarcity: 0.18, space_insurance_gap: 0.20,
    regulatory_space_framework: 0.75, international_cooperation_index: 0.72,
    new_space_innovation_rate: 0.75,
  },
  // SE-005 — MEA, satellite_operations → critical, spectrum_war
  {
    id: "SE-005", space_segment: "satellite_operations", region: "MEA",
    orbital_asset_concentration: 0.68, launch_cost_competitiveness: 0.28,
    satellite_constellation_density: 0.60, space_debris_collision_risk: 0.62,
    spectrum_congestion: 0.82, space_sovereignty_gap: 0.65, launch_vehicle_dependency: 0.70,
    ground_infrastructure_resilience: 0.28, space_weather_vulnerability: 0.72,
    commercialization_readiness: 0.30, space_mining_viability: 0.20,
    anti_satellite_threat: 0.58, orbital_slot_scarcity: 0.78, space_insurance_gap: 0.68,
    regulatory_space_framework: 0.25, international_cooperation_index: 0.28,
    new_space_innovation_rate: 0.30,
  },
  // SE-006 — EMEA, ground_stations → moderate, none
  {
    id: "SE-006", space_segment: "ground_stations", region: "EMEA",
    orbital_asset_concentration: 0.35, launch_cost_competitiveness: 0.60,
    satellite_constellation_density: 0.38, space_debris_collision_risk: 0.30,
    spectrum_congestion: 0.32, space_sovereignty_gap: 0.35, launch_vehicle_dependency: 0.38,
    ground_infrastructure_resilience: 0.62, space_weather_vulnerability: 0.35,
    commercialization_readiness: 0.58, space_mining_viability: 0.40,
    anti_satellite_threat: 0.30, orbital_slot_scarcity: 0.32, space_insurance_gap: 0.35,
    regulatory_space_framework: 0.60, international_cooperation_index: 0.58,
    new_space_innovation_rate: 0.55,
  },
  // SE-007 — APAC, space_mining → high, launch_monopoly
  {
    id: "SE-007", space_segment: "space_mining", region: "APAC",
    orbital_asset_concentration: 0.58, launch_cost_competitiveness: 0.25,
    satellite_constellation_density: 0.52, space_debris_collision_risk: 0.45,
    spectrum_congestion: 0.48, space_sovereignty_gap: 0.55, launch_vehicle_dependency: 0.78,
    ground_infrastructure_resilience: 0.48, space_weather_vulnerability: 0.50,
    commercialization_readiness: 0.42, space_mining_viability: 0.55,
    anti_satellite_threat: 0.50, orbital_slot_scarcity: 0.48, space_insurance_gap: 0.55,
    regulatory_space_framework: 0.38, international_cooperation_index: 0.40,
    new_space_innovation_rate: 0.45,
  },
  // SE-008 — NOAM, satellite_operations → critical, space_weather_blackout
  {
    id: "SE-008", space_segment: "satellite_operations", region: "NOAM",
    orbital_asset_concentration: 0.75, launch_cost_competitiveness: 0.32,
    satellite_constellation_density: 0.65, space_debris_collision_risk: 0.68,
    spectrum_congestion: 0.62, space_sovereignty_gap: 0.58, launch_vehicle_dependency: 0.62,
    ground_infrastructure_resilience: 0.22, space_weather_vulnerability: 0.85,
    commercialization_readiness: 0.35, space_mining_viability: 0.30,
    anti_satellite_threat: 0.55, orbital_slot_scarcity: 0.60, space_insurance_gap: 0.65,
    regulatory_space_framework: 0.30, international_cooperation_index: 0.32,
    new_space_innovation_rate: 0.35,
  },
];

type SpaceEntity = typeof MOCK_ENTITIES[0];

function orbitalScore(e: SpaceEntity): number {
  return Math.round((e.space_debris_collision_risk * 0.4 + e.spectrum_congestion * 0.35 + e.orbital_slot_scarcity * 0.25) * 100 * 100) / 100;
}
function sovereigntyScore(e: SpaceEntity): number {
  return Math.round((e.space_sovereignty_gap * 0.4 + e.anti_satellite_threat * 0.35 + e.launch_vehicle_dependency * 0.25) * 100 * 100) / 100;
}
function commercialScore(e: SpaceEntity): number {
  return Math.round(((1 - e.commercialization_readiness) * 0.4 + (1 - e.new_space_innovation_rate) * 0.35 + e.space_insurance_gap * 0.25) * 100 * 100) / 100;
}
function resilienceScore(e: SpaceEntity): number {
  return Math.round((e.space_weather_vulnerability * 0.4 + (1 - e.ground_infrastructure_resilience) * 0.35 + e.orbital_asset_concentration * 0.25) * 100 * 100) / 100;
}
function compositeScore(orbital: number, sovereignty: number, commercial: number, resilience: number): number {
  return Math.round((orbital * 0.30 + sovereignty * 0.25 + commercial * 0.25 + resilience * 0.20) * 100) / 100;
}
function spaceRisk(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function spacePattern(e: SpaceEntity): string {
  if (e.space_debris_collision_risk >= 0.70 && e.satellite_constellation_density >= 0.65) return "orbital_collision_cascade";
  if (e.space_sovereignty_gap >= 0.70 && e.anti_satellite_threat >= 0.60) return "space_sovereignty_loss";
  if (e.spectrum_congestion >= 0.70 && e.orbital_slot_scarcity >= 0.65) return "spectrum_war";
  if (e.launch_vehicle_dependency >= 0.70 && (1 - e.launch_cost_competitiveness) >= 0.60) return "launch_monopoly";
  if (e.space_weather_vulnerability >= 0.70 && (1 - e.ground_infrastructure_resilience) >= 0.60) return "space_weather_blackout";
  return "none";
}
function spaceSeverity(composite: number): string {
  if (composite >= 75) return "orbital_emergency";
  if (composite >= 50) return "high_space_risk";
  if (composite >= 25) return "space_stress";
  return "space_optimum";
}
function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "space_emergency_protocol";
  if (risk === "high" && pattern === "orbital_collision_cascade") return "debris_mitigation";
  if (risk === "high") return "space_resilience_program";
  if (risk === "moderate") return "space_monitoring";
  return "no_action";
}
function spaceSignal(e: SpaceEntity, composite: number, risk: string): string {
  if (risk === "critical") {
    return `Critique — risque collision débris ${Math.round(e.space_debris_collision_risk * 100)}% — menace antisatellite ${Math.round(e.anti_satellite_threat * 100)}% — composite ${Math.round(composite)}`;
  }
  if (risk === "high") {
    return `Élevé — congestion spectre ${Math.round(e.spectrum_congestion * 100)}% — souveraineté spatiale ${100 - Math.round(e.space_sovereignty_gap * 100)}% — composite ${Math.round(composite)}`;
  }
  if (risk === "moderate") {
    return `Modéré — vulnérabilité météo spatiale ${Math.round(e.space_weather_vulnerability * 100)}% — composite ${Math.round(composite)}`;
  }
  return "Économie spatiale optimale — infrastructure orbitale sécurisée, souveraineté maintenue";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[space-economy-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number> = {}, pc: Record<string,number> = {},
          sc: Record<string,number> = {}, ac: Record<string,number> = {};
    let tOrbital = 0, tSov = 0, tCom = 0, tRes = 0, tComp = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.space_risk]          = (rc[ent.space_risk]          || 0) + 1;
      pc[ent.space_pattern]       = (pc[ent.space_pattern]       || 0) + 1;
      sc[ent.space_severity]      = (sc[ent.space_severity]      || 0) + 1;
      ac[ent.recommended_action]  = (ac[ent.recommended_action]  || 0) + 1;
      tOrbital    += ent.orbital_score;
      tSov        += ent.sovereignty_score;
      tCom        += ent.commercial_score;
      tRes        += ent.resilience_score;
      tComp       += ent.space_composite;
      if (ent.is_in_space_crisis)           crisisCount++;
      if (ent.requires_space_intervention)  interventionCount++;
    }

    const n = entities.length;
    const avgComp = tComp / n;
    const summary = {
      total:                           n,
      risk_counts:                     rc,
      pattern_counts:                  pc,
      severity_counts:                 sc,
      action_counts:                   ac,
      avg_space_composite:             Math.round(avgComp * 10) / 10,
      space_crisis_count:              crisisCount,
      space_intervention_count:        interventionCount,
      avg_orbital_score:               Math.round(tOrbital / n * 10) / 10,
      avg_sovereignty_score:           Math.round(tSov / n * 10) / 10,
      avg_commercial_score:            Math.round(tCom / n * 10) / 10,
      avg_resilience_score:            Math.round(tRes / n * 10) / 10,
      avg_estimated_space_risk_index:  Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "space-economy-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/space-economy-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return sealResponse(NextResponse.json(sealResponse(await upstream.json(), "space-economy-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "space-economy-engine"),
      { status: 502 }
    ));
  }
}
