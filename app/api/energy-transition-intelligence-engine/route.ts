import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // ETI-001 — EMEA, fossil_utilities → critical, fossil_lock_in
  { id: "ETI-001", energy_sector: "fossil_utilities", region: "EMEA",
    renewable_penetration_rate: 0.08, fossil_dependency: 0.88, grid_stability_index: 0.55,
    stranded_asset_exposure: 0.60, carbon_intensity: 0.82, energy_storage_capacity: 0.20,
    demand_flexibility: 0.22, grid_modernization_lag: 0.72, energy_poverty_risk: 0.42,
    just_transition_gap: 0.50, regulatory_carbon_pressure: 0.80, green_capex_rate: 0.12,
    critical_mineral_dependency: 0.45, hydrogen_readiness: 0.10, transmission_infrastructure_gap: 0.48,
    energy_sovereignty_index: 0.38, decarbonization_velocity: 0.08 },

  // ETI-002 — APAC, renewables → low, none
  { id: "ETI-002", energy_sector: "renewables", region: "APAC",
    renewable_penetration_rate: 0.88, fossil_dependency: 0.08, grid_stability_index: 0.85,
    stranded_asset_exposure: 0.05, carbon_intensity: 0.10, energy_storage_capacity: 0.80,
    demand_flexibility: 0.82, grid_modernization_lag: 0.12, energy_poverty_risk: 0.10,
    just_transition_gap: 0.08, regulatory_carbon_pressure: 0.20, green_capex_rate: 0.90,
    critical_mineral_dependency: 0.25, hydrogen_readiness: 0.78, transmission_infrastructure_gap: 0.12,
    energy_sovereignty_index: 0.88, decarbonization_velocity: 0.92 },

  // ETI-003 — NOAM, coal_power → high, stranded_asset_crisis
  { id: "ETI-003", energy_sector: "coal_power", region: "NOAM",
    renewable_penetration_rate: 0.22, fossil_dependency: 0.65, grid_stability_index: 0.62,
    stranded_asset_exposure: 0.78, carbon_intensity: 0.72, energy_storage_capacity: 0.35,
    demand_flexibility: 0.40, grid_modernization_lag: 0.55, energy_poverty_risk: 0.38,
    just_transition_gap: 0.52, regulatory_carbon_pressure: 0.68, green_capex_rate: 0.22,
    critical_mineral_dependency: 0.42, hydrogen_readiness: 0.20, transmission_infrastructure_gap: 0.50,
    energy_sovereignty_index: 0.55, decarbonization_velocity: 0.28 },

  // ETI-004 — LATAM, renewables → low, none
  { id: "ETI-004", energy_sector: "renewables", region: "LATAM",
    renewable_penetration_rate: 0.82, fossil_dependency: 0.10, grid_stability_index: 0.80,
    stranded_asset_exposure: 0.08, carbon_intensity: 0.12, energy_storage_capacity: 0.75,
    demand_flexibility: 0.78, grid_modernization_lag: 0.15, energy_poverty_risk: 0.18,
    just_transition_gap: 0.12, regulatory_carbon_pressure: 0.22, green_capex_rate: 0.88,
    critical_mineral_dependency: 0.20, hydrogen_readiness: 0.70, transmission_infrastructure_gap: 0.15,
    energy_sovereignty_index: 0.85, decarbonization_velocity: 0.88 },

  // ETI-005 — MEA, oil_gas → critical, mineral_sovereignty_loss
  { id: "ETI-005", energy_sector: "oil_gas", region: "MEA",
    renewable_penetration_rate: 0.10, fossil_dependency: 0.92, grid_stability_index: 0.48,
    stranded_asset_exposure: 0.65, carbon_intensity: 0.88, energy_storage_capacity: 0.18,
    demand_flexibility: 0.20, grid_modernization_lag: 0.68, energy_poverty_risk: 0.52,
    just_transition_gap: 0.58, regulatory_carbon_pressure: 0.38, green_capex_rate: 0.10,
    critical_mineral_dependency: 0.82, hydrogen_readiness: 0.08, transmission_infrastructure_gap: 0.55,
    energy_sovereignty_index: 0.22, decarbonization_velocity: 0.05 },

  // ETI-006 — EMEA, grid_operator → moderate, none
  { id: "ETI-006", energy_sector: "grid_operator", region: "EMEA",
    renewable_penetration_rate: 0.45, fossil_dependency: 0.40, grid_stability_index: 0.58,
    stranded_asset_exposure: 0.30, carbon_intensity: 0.42, energy_storage_capacity: 0.48,
    demand_flexibility: 0.50, grid_modernization_lag: 0.45, energy_poverty_risk: 0.30,
    just_transition_gap: 0.35, regulatory_carbon_pressure: 0.55, green_capex_rate: 0.50,
    critical_mineral_dependency: 0.38, hydrogen_readiness: 0.42, transmission_infrastructure_gap: 0.40,
    energy_sovereignty_index: 0.55, decarbonization_velocity: 0.45 },

  // ETI-007 — APAC, coal_power → high, grid_instability
  { id: "ETI-007", energy_sector: "coal_power", region: "APAC",
    renewable_penetration_rate: 0.25, fossil_dependency: 0.68, grid_stability_index: 0.28,
    stranded_asset_exposure: 0.55, carbon_intensity: 0.75, energy_storage_capacity: 0.30,
    demand_flexibility: 0.32, grid_modernization_lag: 0.70, energy_poverty_risk: 0.45,
    just_transition_gap: 0.50, regulatory_carbon_pressure: 0.60, green_capex_rate: 0.28,
    critical_mineral_dependency: 0.40, hydrogen_readiness: 0.18, transmission_infrastructure_gap: 0.65,
    energy_sovereignty_index: 0.45, decarbonization_velocity: 0.22 },

  // ETI-008 — NOAM, fossil_utilities → critical, energy_poverty_trap
  { id: "ETI-008", energy_sector: "fossil_utilities", region: "NOAM",
    renewable_penetration_rate: 0.12, fossil_dependency: 0.80, grid_stability_index: 0.50,
    stranded_asset_exposure: 0.62, carbon_intensity: 0.78, energy_storage_capacity: 0.22,
    demand_flexibility: 0.25, grid_modernization_lag: 0.65, energy_poverty_risk: 0.82,
    just_transition_gap: 0.75, regulatory_carbon_pressure: 0.70, green_capex_rate: 0.18,
    critical_mineral_dependency: 0.48, hydrogen_readiness: 0.12, transmission_infrastructure_gap: 0.52,
    energy_sovereignty_index: 0.32, decarbonization_velocity: 0.15 },
];

type Entity = typeof MOCK_ENTITIES[0];

function fossilScore(e: Entity): number {
  const raw = (
    e.fossil_dependency * 0.4
    + e.carbon_intensity * 0.35
    + (1 - e.renewable_penetration_rate) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function stabilityScore(e: Entity): number {
  const raw = (
    (1 - e.grid_stability_index) * 0.4
    + e.transmission_infrastructure_gap * 0.35
    + (1 - e.energy_storage_capacity) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function strandedScore(e: Entity): number {
  const raw = (
    e.stranded_asset_exposure * 0.4
    + (1 - e.green_capex_rate) * 0.35
    + (1 - e.decarbonization_velocity) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function sovereigntyScore(e: Entity): number {
  const raw = (
    e.critical_mineral_dependency * 0.4
    + (1 - e.energy_sovereignty_index) * 0.35
    + e.energy_poverty_risk * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function transitionComposite(fossil: number, stability: number, stranded: number, sovereignty: number): number {
  return Math.round((fossil * 0.30 + stability * 0.25 + stranded * 0.25 + sovereignty * 0.20) * 100) / 100;
}

function transitionRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function transitionPattern(e: Entity): string {
  if (e.fossil_dependency >= 0.70 && (1 - e.decarbonization_velocity) >= 0.65) return "fossil_lock_in";
  if (e.stranded_asset_exposure >= 0.70 && (1 - e.green_capex_rate) >= 0.60) return "stranded_asset_crisis";
  if ((1 - e.grid_stability_index) >= 0.65 && e.transmission_infrastructure_gap >= 0.60) return "grid_instability";
  if (e.energy_poverty_risk >= 0.70 && e.just_transition_gap >= 0.60) return "energy_poverty_trap";
  if (e.critical_mineral_dependency >= 0.70 && (1 - e.energy_sovereignty_index) >= 0.60) return "mineral_sovereignty_loss";
  return "none";
}

function transitionSeverity(comp: number): string {
  if (comp >= 75) return "transition_emergency";
  if (comp >= 50) return "high_transition_risk";
  if (comp >= 25) return "transition_stress";
  return "transition_optimum";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "decarbonization_emergency";
  if (risk === "high" && pattern === "stranded_asset_crisis") return "stranded_asset_rescue";
  if (risk === "high") return "transition_acceleration";
  if (risk === "moderate") return "transition_monitoring";
  return "no_action";
}

function transitionSignal(e: Entity, risk: string, comp: number): string {
  const compInt = Math.round(comp);
  if (risk === "critical") {
    return `Critique — dépendance fossile ${Math.round(e.fossil_dependency * 100)}% — actifs échoués ${Math.round(e.stranded_asset_exposure * 100)}% — composite ${compInt}`;
  }
  if (risk === "high") {
    return `Élevé — stabilité réseau ${Math.round(e.grid_stability_index * 100)}% — capex vert ${Math.round(e.green_capex_rate * 100)}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `Modéré — pénétration renouvelable ${Math.round(e.renewable_penetration_rate * 100)}% — composite ${compInt}`;
  }
  return "Transition énergétique optimale — décarbonisation accélérée, souveraineté énergétique préservée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const fossil      = fossilScore(e);
      const stability   = stabilityScore(e);
      const stranded    = strandedScore(e);
      const sovereignty = sovereigntyScore(e);
      const comp        = transitionComposite(fossil, stability, stranded, sovereignty);
      const risk        = transitionRisk(comp);
      const pattern     = transitionPattern(e);
      const severity    = transitionSeverity(comp);
      const action      = recommendedAction(risk, pattern);
      const signal      = transitionSignal(e, risk, comp);

      return {
        id:                        e.entity_id,
        region:                           e.region,
        energy_sector:                    e.energy_sector,
        transition_risk:                  risk,
        transition_pattern:               pattern,
        transition_severity:              severity,
        recommended_action:               action,
        fossil_score:                     fossil,
        stability_score:                  stability,
        stranded_score:                   stranded,
        sovereignty_score:                sovereignty,
        transition_composite:             comp,
        is_in_transition_crisis:          comp >= 60,
        requires_transition_intervention: comp >= 40,
        transition_signal:                signal,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tFossil = 0, tStability = 0, tStranded = 0, tSovereignty = 0, tComp = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.transition_risk]      = (rc[ent.transition_risk]      || 0) + 1;
      pc[ent.transition_pattern]   = (pc[ent.transition_pattern]   || 0) + 1;
      sc[ent.transition_severity]  = (sc[ent.transition_severity]  || 0) + 1;
      ac[ent.recommended_action]   = (ac[ent.recommended_action]   || 0) + 1;
      tFossil      += ent.fossil_score;
      tStability   += ent.stability_score;
      tStranded    += ent.stranded_score;
      tSovereignty += ent.sovereignty_score;
      tComp        += ent.transition_composite;
      if (ent.is_in_transition_crisis)          crisisCount++;
      if (ent.requires_transition_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 10) / 10;

    const summary = {
      total:                               n,
      risk_counts:                         rc,
      pattern_counts:                      pc,
      severity_counts:                     sc,
      action_counts:                       ac,
      avg_transition_composite:            avgComp,
      transition_crisis_count:             crisisCount,
      transition_intervention_count:       interventionCount,
      avg_fossil_score:                    Math.round(tFossil      / n * 10) / 10,
      avg_stability_score:                 Math.round(tStability   / n * 10) / 10,
      avg_stranded_score:                  Math.round(tStranded    / n * 10) / 10,
      avg_sovereignty_score:               Math.round(tSovereignty / n * 10) / 10,
      avg_estimated_transition_risk_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "energy-transition-intelligence-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/energy-transition-intelligence-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "energy-transition-intelligence-engine"));
  } catch {
    return NextResponse.json(sealResponse({ error: "Upstream unavailable" }, "energy-transition-intelligence-engine"), { status: 502 });
  }
}
