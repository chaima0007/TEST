import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockTerritories = [
  {
    territory_id: "TF-001", territory_type: "urban", region: "EMEA",
    terraforming_risk: "critical", eco_pattern: "urban_heat_surge",
    terraforming_severity: "critical", recommended_action: "urban_cooling_deployment",
    ecosystem_score: 57, climate_score: 87, resource_score: 65, resilience_score: 100,
    terraforming_composite: 75.1, has_ecological_alert: true, requires_emergency_action: true,
    estimated_ecological_risk_index: 6.46,
    terraforming_signal: "Surchauffe urbaine — santé écosystème 30% — biodiversité 25% — proximité point basculement 78% — composite 75",
  },
  {
    territory_id: "TF-002", territory_type: "peri_urban", region: "NAMER",
    terraforming_risk: "high", eco_pattern: "urban_heat_surge",
    terraforming_severity: "degraded", recommended_action: "green_corridor_activation",
    ecosystem_score: 40, climate_score: 52, resource_score: 52, resilience_score: 52,
    terraforming_composite: 48.4, has_ecological_alert: true, requires_emergency_action: true,
    estimated_ecological_risk_index: 3.05,
    terraforming_signal: "Surchauffe urbaine — santé écosystème 45% — biodiversité 42% — proximité point basculement 48% — composite 48",
  },
  {
    territory_id: "TF-003", territory_type: "rural", region: "APAC",
    terraforming_risk: "low", eco_pattern: "none",
    terraforming_severity: "regenerating", recommended_action: "no_action",
    ecosystem_score: 0, climate_score: 0, resource_score: 0, resilience_score: 0,
    terraforming_composite: 0.0, has_ecological_alert: false, requires_emergency_action: false,
    estimated_ecological_risk_index: 0.0,
    terraforming_signal: "Territoire en régénération — biodiversité croissante, sols sains, cycle hydrique intact, résilience écologique forte",
  },
  {
    territory_id: "TF-004", territory_type: "coastal", region: "LATAM",
    terraforming_risk: "high", eco_pattern: "biodiversity_collapse",
    terraforming_severity: "degraded", recommended_action: "biodiversity_reintroduction",
    ecosystem_score: 52, climate_score: 38, resource_score: 52, resilience_score: 52,
    terraforming_composite: 48.5, has_ecological_alert: true, requires_emergency_action: true,
    estimated_ecological_risk_index: 3.54,
    terraforming_signal: "Effondrement biodiversité — santé écosystème 35% — biodiversité 32% — proximité point basculement 58% — composite 48",
  },
  {
    territory_id: "TF-005", territory_type: "forest", region: "MEA",
    terraforming_risk: "low", eco_pattern: "none",
    terraforming_severity: "regenerating", recommended_action: "no_action",
    ecosystem_score: 0, climate_score: 0, resource_score: 0, resilience_score: 0,
    terraforming_composite: 0.0, has_ecological_alert: false, requires_emergency_action: false,
    estimated_ecological_risk_index: 0.0,
    terraforming_signal: "Territoire en régénération — biodiversité croissante, sols sains, cycle hydrique intact, résilience écologique forte",
  },
  {
    territory_id: "TF-006", territory_type: "wetland", region: "EMEA",
    terraforming_risk: "low", eco_pattern: "none",
    terraforming_severity: "regenerating", recommended_action: "no_action",
    ecosystem_score: 14, climate_score: 6, resource_score: 26, resilience_score: 26,
    terraforming_composite: 17.4, has_ecological_alert: false, requires_emergency_action: false,
    estimated_ecological_risk_index: 0.8,
    terraforming_signal: "Territoire en régénération — biodiversité croissante, sols sains, cycle hydrique intact, résilience écologique forte",
  },
  {
    territory_id: "TF-007", territory_type: "industrial", region: "NAMER",
    terraforming_risk: "critical", eco_pattern: "urban_heat_surge",
    terraforming_severity: "critical", recommended_action: "urban_cooling_deployment",
    ecosystem_score: 75, climate_score: 100, resource_score: 100, resilience_score: 100,
    terraforming_composite: 92.5, has_ecological_alert: true, requires_emergency_action: true,
    estimated_ecological_risk_index: 8.6,
    terraforming_signal: "Surchauffe urbaine — santé écosystème 18% — biodiversité 15% — proximité point basculement 90% — composite 92",
  },
  {
    territory_id: "TF-008", territory_type: "agricultural", region: "APAC",
    terraforming_risk: "high", eco_pattern: "none",
    terraforming_severity: "degraded", recommended_action: "eco_monitoring",
    ecosystem_score: 40, climate_score: 38, resource_score: 52, resilience_score: 38,
    terraforming_composite: 42.1, has_ecological_alert: true, requires_emergency_action: true,
    estimated_ecological_risk_index: 2.57,
    terraforming_signal: "None — santé écosystème 48% — biodiversité 45% — proximité point basculement 42% — composite 42",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (!process.env.SWARM_API_URL) {
    let territories = [...mockTerritories];
    if (risk)    territories = territories.filter((t) => t.terraforming_risk === risk);
    if (pattern) territories = territories.filter((t) => t.eco_pattern === pattern);

    const risk_counts:     Record<string, number> = {};
    const pattern_counts:  Record<string, number> = {};
    const severity_counts: Record<string, number> = {};
    const action_counts:   Record<string, number> = {};
    let total_comp = 0, total_eco = 0, total_cli = 0, total_res = 0,
        total_resil = 0, total_risk_idx = 0;

    for (const t of mockTerritories) {
      risk_counts[t.terraforming_risk]     = (risk_counts[t.terraforming_risk] || 0) + 1;
      pattern_counts[t.eco_pattern]        = (pattern_counts[t.eco_pattern] || 0) + 1;
      severity_counts[t.terraforming_severity] = (severity_counts[t.terraforming_severity] || 0) + 1;
      action_counts[t.recommended_action]  = (action_counts[t.recommended_action] || 0) + 1;
      total_comp      += t.terraforming_composite;
      total_eco       += t.ecosystem_score;
      total_cli       += t.climate_score;
      total_res       += t.resource_score;
      total_resil     += t.resilience_score;
      total_risk_idx  += t.estimated_ecological_risk_index;
    }

    const n = mockTerritories.length;

    return NextResponse.json({
      territories,
      summary: {
        total:                                n,
        risk_counts,
        pattern_counts,
        severity_counts,
        action_counts,
        avg_terraforming_composite:           Math.round((total_comp     / n) * 10) / 10,
        ecological_alert_count:               mockTerritories.filter((t) => t.has_ecological_alert).length,
        emergency_action_count:               mockTerritories.filter((t) => t.requires_emergency_action).length,
        avg_ecosystem_score:                  Math.round((total_eco      / n) * 10) / 10,
        avg_climate_score:                    Math.round((total_cli      / n) * 10) / 10,
        avg_resource_score:                   Math.round((total_res      / n) * 10) / 10,
        avg_resilience_score:                 Math.round((total_resil    / n) * 10) / 10,
        avg_estimated_ecological_risk_index:  Math.round((total_risk_idx / n) * 100) / 100,
      },
    });
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/anthropocene-terraforming-engine`);
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(await res.json());
  } catch {}

  return NextResponse.json({ territories: [], summary: {} });
}
