import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // OCN-001 — critical, ecological_ocean_collapse (coral_reef_system, APAC)
  {
    id: "OCN-001", ocean_domain: "coral_reef_system", region: "APAC",
    ocean_acidification_severity: 0.88, plastic_pollution_saturation: 0.55, deep_sea_mining_disruption: 0.50,
    maritime_trade_route_vulnerability: 0.55, illegal_fishing_intensity: 0.60, coral_reef_collapse_rate: 0.82,
    submarine_cable_security_risk: 0.48, marine_biodiversity_collapse: 0.75, ocean_heat_content_anomaly: 0.80,
    arctic_route_geopolitics: 0.40, blue_carbon_sequestration_loss: 0.70, piracy_maritime_crime_index: 0.45,
    exclusive_economic_zone_conflict: 0.50, ocean_sovereignty_dispute_intensity: 0.52, plastic_microplastic_food_chain: 0.60,
    seabed_resource_competition: 0.48, maritime_surveillance_gap: 0.45,
  },
  // OCN-002 — low, none (amazon_coast, LATAM)
  {
    id: "OCN-002", ocean_domain: "amazon_coast", region: "LATAM",
    ocean_acidification_severity: 0.12, plastic_pollution_saturation: 0.15, deep_sea_mining_disruption: 0.10,
    maritime_trade_route_vulnerability: 0.14, illegal_fishing_intensity: 0.18, coral_reef_collapse_rate: 0.12,
    submarine_cable_security_risk: 0.10, marine_biodiversity_collapse: 0.15, ocean_heat_content_anomaly: 0.18,
    arctic_route_geopolitics: 0.10, blue_carbon_sequestration_loss: 0.14, piracy_maritime_crime_index: 0.12,
    exclusive_economic_zone_conflict: 0.10, ocean_sovereignty_dispute_intensity: 0.12, plastic_microplastic_food_chain: 0.15,
    seabed_resource_competition: 0.10, maritime_surveillance_gap: 0.12,
  },
  // OCN-003 — high, maritime_security_crisis (strait_chokepoint, MEA)
  {
    id: "OCN-003", ocean_domain: "strait_chokepoint", region: "MEA",
    ocean_acidification_severity: 0.45, plastic_pollution_saturation: 0.50, deep_sea_mining_disruption: 0.48,
    maritime_trade_route_vulnerability: 0.55, illegal_fishing_intensity: 0.52, coral_reef_collapse_rate: 0.42,
    submarine_cable_security_risk: 0.82, marine_biodiversity_collapse: 0.45, ocean_heat_content_anomaly: 0.50,
    arctic_route_geopolitics: 0.40, blue_carbon_sequestration_loss: 0.48, piracy_maritime_crime_index: 0.75,
    exclusive_economic_zone_conflict: 0.50, ocean_sovereignty_dispute_intensity: 0.55, plastic_microplastic_food_chain: 0.48,
    seabed_resource_competition: 0.52, maritime_surveillance_gap: 0.60,
  },
  // OCN-004 — low, none (north_sea, EMEA)
  {
    id: "OCN-004", ocean_domain: "north_sea", region: "EMEA",
    ocean_acidification_severity: 0.18, plastic_pollution_saturation: 0.20, deep_sea_mining_disruption: 0.15,
    maritime_trade_route_vulnerability: 0.18, illegal_fishing_intensity: 0.15, coral_reef_collapse_rate: 0.12,
    submarine_cable_security_risk: 0.15, marine_biodiversity_collapse: 0.18, ocean_heat_content_anomaly: 0.20,
    arctic_route_geopolitics: 0.22, blue_carbon_sequestration_loss: 0.18, piracy_maritime_crime_index: 0.10,
    exclusive_economic_zone_conflict: 0.15, ocean_sovereignty_dispute_intensity: 0.18, plastic_microplastic_food_chain: 0.20,
    seabed_resource_competition: 0.15, maritime_surveillance_gap: 0.12,
  },
  // OCN-005 — critical, ocean_sovereignty_war (south_china_sea, APAC)
  {
    id: "OCN-005", ocean_domain: "south_china_sea", region: "APAC",
    ocean_acidification_severity: 0.60, plastic_pollution_saturation: 0.58, deep_sea_mining_disruption: 0.62,
    maritime_trade_route_vulnerability: 0.65, illegal_fishing_intensity: 0.68, coral_reef_collapse_rate: 0.55,
    submarine_cable_security_risk: 0.60, marine_biodiversity_collapse: 0.58, ocean_heat_content_anomaly: 0.62,
    arctic_route_geopolitics: 0.48, blue_carbon_sequestration_loss: 0.55, piracy_maritime_crime_index: 0.58,
    exclusive_economic_zone_conflict: 0.82, ocean_sovereignty_dispute_intensity: 0.88, plastic_microplastic_food_chain: 0.55,
    seabed_resource_competition: 0.75, maritime_surveillance_gap: 0.58,
  },
  // OCN-006 — moderate, none (atlantic_coast, NOAM)
  {
    id: "OCN-006", ocean_domain: "atlantic_coast", region: "NOAM",
    ocean_acidification_severity: 0.32, plastic_pollution_saturation: 0.35, deep_sea_mining_disruption: 0.28,
    maritime_trade_route_vulnerability: 0.30, illegal_fishing_intensity: 0.32, coral_reef_collapse_rate: 0.28,
    submarine_cable_security_risk: 0.30, marine_biodiversity_collapse: 0.32, ocean_heat_content_anomaly: 0.35,
    arctic_route_geopolitics: 0.30, blue_carbon_sequestration_loss: 0.32, piracy_maritime_crime_index: 0.25,
    exclusive_economic_zone_conflict: 0.28, ocean_sovereignty_dispute_intensity: 0.30, plastic_microplastic_food_chain: 0.35,
    seabed_resource_competition: 0.28, maritime_surveillance_gap: 0.30,
  },
  // OCN-007 — high, blue_economy_disruption (indian_ocean, MEA)
  {
    id: "OCN-007", ocean_domain: "indian_ocean", region: "MEA",
    ocean_acidification_severity: 0.50, plastic_pollution_saturation: 0.52, deep_sea_mining_disruption: 0.78,
    maritime_trade_route_vulnerability: 0.82, illegal_fishing_intensity: 0.58, coral_reef_collapse_rate: 0.48,
    submarine_cable_security_risk: 0.55, marine_biodiversity_collapse: 0.50, ocean_heat_content_anomaly: 0.55,
    arctic_route_geopolitics: 0.42, blue_carbon_sequestration_loss: 0.52, piracy_maritime_crime_index: 0.58,
    exclusive_economic_zone_conflict: 0.52, ocean_sovereignty_dispute_intensity: 0.55, plastic_microplastic_food_chain: 0.50,
    seabed_resource_competition: 0.58, maritime_surveillance_gap: 0.52,
  },
  // OCN-008 — critical, plastic_collapse (pacific_gyre, APAC)
  {
    id: "OCN-008", ocean_domain: "pacific_gyre", region: "APAC",
    ocean_acidification_severity: 0.62, plastic_pollution_saturation: 0.88, deep_sea_mining_disruption: 0.58,
    maritime_trade_route_vulnerability: 0.60, illegal_fishing_intensity: 0.65, coral_reef_collapse_rate: 0.58,
    submarine_cable_security_risk: 0.55, marine_biodiversity_collapse: 0.68, ocean_heat_content_anomaly: 0.72,
    arctic_route_geopolitics: 0.45, blue_carbon_sequestration_loss: 0.65, piracy_maritime_crime_index: 0.50,
    exclusive_economic_zone_conflict: 0.52, ocean_sovereignty_dispute_intensity: 0.55, plastic_microplastic_food_chain: 0.82,
    seabed_resource_competition: 0.55, maritime_surveillance_gap: 0.52,
  },
];

type EntityInput = typeof MOCK_ENTITIES[0];

function ecologicalScore(e: EntityInput): number {
  const raw = (
    e.ocean_acidification_severity * 0.4
    + e.coral_reef_collapse_rate * 0.35
    + e.marine_biodiversity_collapse * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function economicScore(e: EntityInput): number {
  const raw = (
    e.maritime_trade_route_vulnerability * 0.4
    + e.deep_sea_mining_disruption * 0.35
    + e.illegal_fishing_intensity * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function securityScore(e: EntityInput): number {
  const raw = (
    e.submarine_cable_security_risk * 0.4
    + e.piracy_maritime_crime_index * 0.35
    + e.maritime_surveillance_gap * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function geopoliticalScore(e: EntityInput): number {
  const raw = (
    e.ocean_sovereignty_dispute_intensity * 0.4
    + e.exclusive_economic_zone_conflict * 0.35
    + e.seabed_resource_competition * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function oceanComposite(eco: number, econ: number, sec: number, geo: number): number {
  return Math.round((eco * 0.30 + econ * 0.25 + sec * 0.25 + geo * 0.20) * 100) / 100;
}

function oceanRisk(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}

function oceanPattern(e: EntityInput): string {
  if (e.ocean_acidification_severity >= 0.70 && e.coral_reef_collapse_rate >= 0.65) return "ecological_ocean_collapse";
  if (e.submarine_cable_security_risk >= 0.70 && e.piracy_maritime_crime_index >= 0.65) return "maritime_security_crisis";
  if (e.maritime_trade_route_vulnerability >= 0.70 && e.deep_sea_mining_disruption >= 0.65) return "blue_economy_disruption";
  if (e.ocean_sovereignty_dispute_intensity >= 0.70 && e.exclusive_economic_zone_conflict >= 0.65) return "ocean_sovereignty_war";
  if (e.plastic_pollution_saturation >= 0.70 && e.plastic_microplastic_food_chain >= 0.65) return "plastic_collapse";
  return "none";
}

function oceanSeverity(composite: number): string {
  if (composite >= 75) return "ocean_emergency";
  if (composite >= 50) return "ocean_crisis";
  if (composite >= 25) return "ocean_stress";
  return "ocean_stable";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "ocean_emergency_response";
  if (risk === "high" && pattern === "maritime_security_crisis") return "naval_security_deployment";
  if (risk === "high") return "ocean_resilience_program";
  if (risk === "moderate") return "ocean_monitoring";
  return "no_action";
}

function oceanSignal(e: EntityInput, risk: string, composite: number): string {
  if (risk === "critical") {
    return `Critique — acidification océanique ${Math.round(e.ocean_acidification_severity * 100)}% — effondrement récifs coralliens ${Math.round(e.coral_reef_collapse_rate * 100)}% — composite ${Math.round(composite)}`;
  }
  if (risk === "high") {
    return `Élevé — vulnérabilité routes maritimes ${Math.round(e.maritime_trade_route_vulnerability * 100)}% — risque câbles sous-marins ${Math.round(e.submarine_cable_security_risk * 100)}% — composite ${Math.round(composite)}`;
  }
  if (risk === "moderate") {
    return `Modéré — pollution plastique ${Math.round(e.plastic_pollution_saturation * 100)}% — composite ${Math.round(composite)}`;
  }
  return "Océan stable — écosystèmes marins sains, souveraineté maritime préservée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const eco       = ecologicalScore(e);
      const econ      = economicScore(e);
      const sec       = securityScore(e);
      const geo       = geopoliticalScore(e);
      const composite = oceanComposite(eco, econ, sec, geo);
      const risk      = oceanRisk(composite);
      const pattern   = oceanPattern(e);
      const severity  = oceanSeverity(composite);
      const action    = recommendedAction(risk, pattern);
      const signal    = oceanSignal(e, risk, composite);

      return {
        id:                    e.entity_id,
        region:                       e.region,
        ocean_domain:                 e.ocean_domain,
        ocean_risk:                   risk,
        ocean_pattern:                pattern,
        ocean_severity:               severity,
        recommended_action:           action,
        ecological_score:             eco,
        economic_score:               econ,
        security_score:               sec,
        geopolitical_score:           geo,
        ocean_composite:              composite,
        is_ocean_crisis:              composite >= 60,
        requires_ocean_intervention:  composite >= 40,
        ocean_signal:                 signal,
      };
    });

    const risk_counts: Record<string, number>     = {};
    const pattern_counts: Record<string, number>  = {};
    const severity_counts: Record<string, number> = {};
    const action_counts: Record<string, number>   = {};
    let tEco = 0, tEcon = 0, tSec = 0, tGeo = 0, tComp = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      risk_counts[ent.ocean_risk]         = (risk_counts[ent.ocean_risk]         || 0) + 1;
      pattern_counts[ent.ocean_pattern]   = (pattern_counts[ent.ocean_pattern]   || 0) + 1;
      severity_counts[ent.ocean_severity] = (severity_counts[ent.ocean_severity] || 0) + 1;
      action_counts[ent.recommended_action] = (action_counts[ent.recommended_action] || 0) + 1;
      tEco  += ent.ecological_score;
      tEcon += ent.economic_score;
      tSec  += ent.security_score;
      tGeo  += ent.geopolitical_score;
      tComp += ent.ocean_composite;
      if (ent.is_ocean_crisis)              crisisCount++;
      if (ent.requires_ocean_intervention)  interventionCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      total:                           n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_ocean_composite:             avgComposite,
      ocean_crisis_count:              crisisCount,
      ocean_intervention_count:        interventionCount,
      avg_ecological_score:            Math.round(tEco  / n * 10) / 10,
      avg_economic_score:              Math.round(tEcon / n * 10) / 10,
      avg_security_score:              Math.round(tSec  / n * 10) / 10,
      avg_geopolitical_score:          Math.round(tGeo  / n * 10) / 10,
      avg_estimated_ocean_risk_index:  Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "ocean-intelligence-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/ocean-intelligence-engine`);
    const data = await upstream.json();
    return NextResponse.json(sealResponse(data, "ocean-intelligence-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable" }, "ocean-intelligence-engine"),
      { status: 502 }
    );
  }
}
