import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // UAM-001 — critique: airspace_collision_risk + battery_fire_safety_gap + regulatory_certification_bottleneck
  {
    id: "UAM-001", vehicle_type: "taxi_aérien_électrique", region: "Île-de-France",
    collision_avoidance_gap: 0.90, airspace_management_failure: 0.88,
    vertiport_density_deficit: 0.78, battery_energy_density_risk: 0.85,
    noise_impact_residential: 0.72, weather_operational_limit: 0.70,
    cybersecurity_vulnerability: 0.75, community_acceptance_gap: 0.68,
    emergency_landing_protocol_gap: 0.82, insurance_framework_absence: 0.75,
    equity_access_gap: 0.70, carbon_lifecycle_emission: 0.68,
    pilot_certification_gap: 0.85, air_traffic_controller_overload: 0.80,
    regulatory_certification_delay: 0.88, urban_integration_planning_gap: 0.72,
    emergency_medical_use_barrier: 0.70,
  },
  // UAM-002 — critique: airspace_collision_risk + noise_pollution_community_conflict + elite_mobility_gentrification
  {
    id: "UAM-002", vehicle_type: "drone_cargo_urbain", region: "Grand Paris",
    collision_avoidance_gap: 0.85, airspace_management_failure: 0.82,
    vertiport_density_deficit: 0.75, battery_energy_density_risk: 0.72,
    noise_impact_residential: 0.88, weather_operational_limit: 0.68,
    cybersecurity_vulnerability: 0.70, community_acceptance_gap: 0.80,
    emergency_landing_protocol_gap: 0.75, insurance_framework_absence: 0.70,
    equity_access_gap: 0.85, carbon_lifecycle_emission: 0.65,
    pilot_certification_gap: 0.72, air_traffic_controller_overload: 0.75,
    regulatory_certification_delay: 0.70, urban_integration_planning_gap: 0.68,
    emergency_medical_use_barrier: 0.65,
  },
  // UAM-003 — critique: battery_fire_safety_gap + regulatory_certification_bottleneck
  {
    id: "UAM-003", vehicle_type: "véhicule_volant_autonome", region: "Lyon Métropole",
    collision_avoidance_gap: 0.78, airspace_management_failure: 0.75,
    vertiport_density_deficit: 0.80, battery_energy_density_risk: 0.90,
    noise_impact_residential: 0.65, weather_operational_limit: 0.72,
    cybersecurity_vulnerability: 0.80, community_acceptance_gap: 0.62,
    emergency_landing_protocol_gap: 0.78, insurance_framework_absence: 0.82,
    equity_access_gap: 0.65, carbon_lifecycle_emission: 0.70,
    pilot_certification_gap: 0.88, air_traffic_controller_overload: 0.72,
    regulatory_certification_delay: 0.85, urban_integration_planning_gap: 0.75,
    emergency_medical_use_barrier: 0.80,
  },
  // UAM-004 — élevé: noise_pollution_community_conflict
  {
    id: "UAM-004", vehicle_type: "hélicoptère_électrique", region: "Marseille",
    collision_avoidance_gap: 0.50, airspace_management_failure: 0.48,
    vertiport_density_deficit: 0.52, battery_energy_density_risk: 0.55,
    noise_impact_residential: 0.80, weather_operational_limit: 0.52,
    cybersecurity_vulnerability: 0.48, community_acceptance_gap: 0.78,
    emergency_landing_protocol_gap: 0.50, insurance_framework_absence: 0.52,
    equity_access_gap: 0.55, carbon_lifecycle_emission: 0.50,
    pilot_certification_gap: 0.52, air_traffic_controller_overload: 0.50,
    regulatory_certification_delay: 0.55, urban_integration_planning_gap: 0.50,
    emergency_medical_use_barrier: 0.48,
  },
  // UAM-005 — élevé: elite_mobility_gentrification
  {
    id: "UAM-005", vehicle_type: "aéronef_vtol_premium", region: "Bordeaux",
    collision_avoidance_gap: 0.48, airspace_management_failure: 0.50,
    vertiport_density_deficit: 0.52, battery_energy_density_risk: 0.50,
    noise_impact_residential: 0.55, weather_operational_limit: 0.48,
    cybersecurity_vulnerability: 0.50, community_acceptance_gap: 0.58,
    emergency_landing_protocol_gap: 0.48, insurance_framework_absence: 0.55,
    equity_access_gap: 0.82, carbon_lifecycle_emission: 0.50,
    pilot_certification_gap: 0.55, air_traffic_controller_overload: 0.48,
    regulatory_certification_delay: 0.52, urban_integration_planning_gap: 0.50,
    emergency_medical_use_barrier: 0.55,
  },
  // UAM-006 — modéré: no pattern
  {
    id: "UAM-006", vehicle_type: "navette_aérienne_partagée", region: "Toulouse",
    collision_avoidance_gap: 0.30, airspace_management_failure: 0.28,
    vertiport_density_deficit: 0.32, battery_energy_density_risk: 0.30,
    noise_impact_residential: 0.28, weather_operational_limit: 0.32,
    cybersecurity_vulnerability: 0.28, community_acceptance_gap: 0.30,
    emergency_landing_protocol_gap: 0.28, insurance_framework_absence: 0.32,
    equity_access_gap: 0.30, carbon_lifecycle_emission: 0.28,
    pilot_certification_gap: 0.30, air_traffic_controller_overload: 0.32,
    regulatory_certification_delay: 0.28, urban_integration_planning_gap: 0.30,
    emergency_medical_use_barrier: 0.32,
  },
  // UAM-007 — faible: no pattern
  {
    id: "UAM-007", vehicle_type: "drone_surveillance_léger", region: "Nantes",
    collision_avoidance_gap: 0.10, airspace_management_failure: 0.12,
    vertiport_density_deficit: 0.10, battery_energy_density_risk: 0.12,
    noise_impact_residential: 0.10, weather_operational_limit: 0.12,
    cybersecurity_vulnerability: 0.10, community_acceptance_gap: 0.12,
    emergency_landing_protocol_gap: 0.10, insurance_framework_absence: 0.12,
    equity_access_gap: 0.10, carbon_lifecycle_emission: 0.12,
    pilot_certification_gap: 0.10, air_traffic_controller_overload: 0.12,
    regulatory_certification_delay: 0.10, urban_integration_planning_gap: 0.12,
    emergency_medical_use_barrier: 0.10,
  },
  // UAM-008 — faible: no pattern
  {
    id: "UAM-008", vehicle_type: "planeur_urbain_silencieux", region: "Bretagne",
    collision_avoidance_gap: 0.12, airspace_management_failure: 0.10,
    vertiport_density_deficit: 0.12, battery_energy_density_risk: 0.10,
    noise_impact_residential: 0.12, weather_operational_limit: 0.10,
    cybersecurity_vulnerability: 0.12, community_acceptance_gap: 0.10,
    emergency_landing_protocol_gap: 0.12, insurance_framework_absence: 0.10,
    equity_access_gap: 0.12, carbon_lifecycle_emission: 0.10,
    pilot_certification_gap: 0.12, air_traffic_controller_overload: 0.10,
    regulatory_certification_delay: 0.12, urban_integration_planning_gap: 0.10,
    emergency_medical_use_barrier: 0.12,
  },
];

type UAMInput = typeof MOCK_ENTITIES[0];

function safetyScore(e: UAMInput): number {
  return Math.round(
    ((e.collision_avoidance_gap + e.airspace_management_failure + e.battery_energy_density_risk + e.emergency_landing_protocol_gap + e.cybersecurity_vulnerability) / 5) * 100 * 0.30 * 100
  ) / 100;
}
function infrastructureScore(e: UAMInput): number {
  return Math.round(
    ((e.vertiport_density_deficit + e.weather_operational_limit + e.urban_integration_planning_gap + e.air_traffic_controller_overload + e.carbon_lifecycle_emission) / 5) * 100 * 0.25 * 100
  ) / 100;
}
function regulatoryScore(e: UAMInput): number {
  return Math.round(
    ((e.pilot_certification_gap + e.regulatory_certification_delay + e.insurance_framework_absence + e.emergency_medical_use_barrier) / 4) * 100 * 0.25 * 100
  ) / 100;
}
function equityScore(e: UAMInput): number {
  return Math.round(
    ((e.noise_impact_residential + e.community_acceptance_gap + e.equity_access_gap) / 3) * 100 * 0.20 * 100
  ) / 100;
}
function compositeScore(sf: number, inf: number, reg: number, eq: number): number {
  return Math.round((sf + inf + reg + eq) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critique";
  if (composite >= 40) return "élevé";
  if (composite >= 20) return "modéré";
  return "faible";
}
function detectPatterns(e: UAMInput): string[] {
  const patterns: string[] = [];
  if ((e.airspace_management_failure + e.collision_avoidance_gap) / 2 > 0.75)
    patterns.push("airspace_collision_risk");
  if ((e.noise_impact_residential + e.community_acceptance_gap) / 2 > 0.70)
    patterns.push("noise_pollution_community_conflict");
  if (e.equity_access_gap > 0.75)
    patterns.push("elite_mobility_gentrification");
  if (e.battery_energy_density_risk > 0.75)
    patterns.push("battery_fire_safety_gap");
  if ((e.regulatory_certification_delay + e.pilot_certification_gap) / 2 > 0.75)
    patterns.push("regulatory_certification_bottleneck");
  return patterns;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const sf   = safetyScore(e);
      const inf  = infrastructureScore(e);
      const reg  = regulatoryScore(e);
      const eq   = equityScore(e);
      const comp = compositeScore(sf, inf, reg, eq);
      const risk = riskLevel(comp);
      const pats = detectPatterns(e);
      return {
        id:                    e.entity_id,
        vehicle_type:                 e.vehicle_type,
        region:                       e.region,
        composite_score:              comp,
        risk_level:                   risk,
        safety_score:                 sf,
        infrastructure_score:         inf,
        regulatory_score:             reg,
        equity_score:                 eq,
        patterns:                     pats,
        collision_avoidance_gap:      e.collision_avoidance_gap,
        noise_impact_residential:     e.noise_impact_residential,
        equity_access_gap:            e.equity_access_gap,
        regulatory_certification_delay: e.regulatory_certification_delay,
        battery_energy_density_risk:  e.battery_energy_density_risk,
      };
    });

    const risk_distribution: Record<string, number>    = {};
    const pattern_distribution: Record<string, number> = {};
    let tSf = 0, tInf = 0, tReg = 0, tEq = 0, tComp = 0;
    let critiqueCount = 0, eleveCount = 0, modereCount = 0, faibleCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level] = (risk_distribution[ent.risk_level] || 0) + 1;
      for (const p of ent.patterns) {
        pattern_distribution[p] = (pattern_distribution[p] || 0) + 1;
      }
      tSf   += ent.safety_score;
      tInf  += ent.infrastructure_score;
      tReg  += ent.regulatory_score;
      tEq   += ent.equity_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critique")      critiqueCount++;
      else if (ent.risk_level === "élevé")    eleveCount++;
      else if (ent.risk_level === "modéré")   modereCount++;
      else                                    faibleCount++;
    }

    const n = entities.length;
    const avgComposite     = Math.round(tComp / n * 10) / 10;
    const avgSafety        = Math.round(tSf   / n * 10) / 10;
    const avgInfrastructure = Math.round(tInf  / n * 10) / 10;
    const avgRegulatory    = Math.round(tReg  / n * 10) / 10;
    const avgEquity        = Math.round(tEq   / n * 10) / 10;

    const topPatterns = Object.entries(pattern_distribution)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([k]) => k);

    const regionCounts: Record<string, number> = {};
    for (const ent of entities) {
      regionCounts[ent.region] = (regionCounts[ent.region] || 0) + 1;
    }
    const dominantRegion = Object.entries(regionCounts).sort((a, b) => b[1] - a[1])[0]?.[0] ?? "";

    const summary = {
      total:                               n,
      critique:                            critiqueCount,
      eleve:                               eleveCount,
      modere:                              modereCount,
      faible:                              faibleCount,
      avg_composite:                       avgComposite,
      avg_safety:                          avgSafety,
      avg_infrastructure:                  avgInfrastructure,
      avg_regulatory:                      avgRegulatory,
      avg_equity:                          avgEquity,
      top_patterns:                        topPatterns,
      dominant_region:                     dominantRegion,
      avg_estimated_uam_readiness_index:   Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, module_id: 439, module_name: "Mobilité Aérienne Urbaine & Véhicules Volants" }, "urban-air-mobility-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/urban-air-mobility-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "urban-air-mobility-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "urban-air-mobility-engine"),
      { status: 502 }
    );
  }
}
