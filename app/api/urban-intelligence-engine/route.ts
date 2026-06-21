import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // UCI-001 — critical, surveillance_state (megacity, EMEA)
  {
    id: "UCI-001", city_type: "megacity", region: "EMEA",
    surveillance_density: 0.88, digital_infrastructure_vulnerability: 0.55, social_control_index: 0.82,
    inequality_tension_index: 0.60, migration_pressure: 0.65, housing_crisis_index: 0.58,
    mobility_gridlock_risk: 0.70, energy_grid_fragility: 0.50, water_system_stress: 0.48,
    food_supply_resilience: 0.45, civic_ai_governance_gap: 0.55, algorithmic_discrimination_risk: 0.72,
    smart_city_lock_in: 0.60, data_extractivism_index: 0.58, urban_heat_island_intensity: 0.65,
    infrastructure_decay_rate: 0.52, civic_engagement_erosion: 0.68,
  },
  // UCI-002 — low, none (medium_city, APAC)
  {
    id: "UCI-002", city_type: "medium_city", region: "APAC",
    surveillance_density: 0.12, digital_infrastructure_vulnerability: 0.15, social_control_index: 0.10,
    inequality_tension_index: 0.14, migration_pressure: 0.18, housing_crisis_index: 0.12,
    mobility_gridlock_risk: 0.15, energy_grid_fragility: 0.10, water_system_stress: 0.12,
    food_supply_resilience: 0.85, civic_ai_governance_gap: 0.15, algorithmic_discrimination_risk: 0.10,
    smart_city_lock_in: 0.12, data_extractivism_index: 0.10, urban_heat_island_intensity: 0.15,
    infrastructure_decay_rate: 0.12, civic_engagement_erosion: 0.10,
  },
  // UCI-003 — high, algorithmic_oppression (smart_city, NOAM)
  {
    id: "UCI-003", city_type: "smart_city", region: "NOAM",
    surveillance_density: 0.58, digital_infrastructure_vulnerability: 0.52, social_control_index: 0.55,
    inequality_tension_index: 0.60, migration_pressure: 0.50, housing_crisis_index: 0.58,
    mobility_gridlock_risk: 0.48, energy_grid_fragility: 0.50, water_system_stress: 0.45,
    food_supply_resilience: 0.50, civic_ai_governance_gap: 0.78, algorithmic_discrimination_risk: 0.82,
    smart_city_lock_in: 0.62, data_extractivism_index: 0.60, urban_heat_island_intensity: 0.45,
    infrastructure_decay_rate: 0.48, civic_engagement_erosion: 0.55,
  },
  // UCI-004 — low, none (medium_city, LATAM)
  {
    id: "UCI-004", city_type: "medium_city", region: "LATAM",
    surveillance_density: 0.15, digital_infrastructure_vulnerability: 0.18, social_control_index: 0.12,
    inequality_tension_index: 0.18, migration_pressure: 0.22, housing_crisis_index: 0.16,
    mobility_gridlock_risk: 0.20, energy_grid_fragility: 0.15, water_system_stress: 0.18,
    food_supply_resilience: 0.80, civic_ai_governance_gap: 0.18, algorithmic_discrimination_risk: 0.12,
    smart_city_lock_in: 0.14, data_extractivism_index: 0.12, urban_heat_island_intensity: 0.20,
    infrastructure_decay_rate: 0.15, civic_engagement_erosion: 0.14,
  },
  // UCI-005 — critical, social_explosion (megacity, MEA)
  {
    id: "UCI-005", city_type: "megacity", region: "MEA",
    surveillance_density: 0.62, digital_infrastructure_vulnerability: 0.60, social_control_index: 0.58,
    inequality_tension_index: 0.85, migration_pressure: 0.80, housing_crisis_index: 0.78,
    mobility_gridlock_risk: 0.72, energy_grid_fragility: 0.65, water_system_stress: 0.70,
    food_supply_resilience: 0.25, civic_ai_governance_gap: 0.58, algorithmic_discrimination_risk: 0.55,
    smart_city_lock_in: 0.48, data_extractivism_index: 0.45, urban_heat_island_intensity: 0.80,
    infrastructure_decay_rate: 0.75, civic_engagement_erosion: 0.72,
  },
  // UCI-006 — moderate, none (smart_city, EMEA)
  {
    id: "UCI-006", city_type: "smart_city", region: "EMEA",
    surveillance_density: 0.35, digital_infrastructure_vulnerability: 0.38, social_control_index: 0.30,
    inequality_tension_index: 0.35, migration_pressure: 0.38, housing_crisis_index: 0.32,
    mobility_gridlock_risk: 0.40, energy_grid_fragility: 0.35, water_system_stress: 0.30,
    food_supply_resilience: 0.62, civic_ai_governance_gap: 0.38, algorithmic_discrimination_risk: 0.32,
    smart_city_lock_in: 0.35, data_extractivism_index: 0.30, urban_heat_island_intensity: 0.35,
    infrastructure_decay_rate: 0.32, civic_engagement_erosion: 0.30,
  },
  // UCI-007 — high, infrastructure_collapse (megacity, APAC)
  {
    id: "UCI-007", city_type: "megacity", region: "APAC",
    surveillance_density: 0.52, digital_infrastructure_vulnerability: 0.80, social_control_index: 0.50,
    inequality_tension_index: 0.55, migration_pressure: 0.60, housing_crisis_index: 0.58,
    mobility_gridlock_risk: 0.65, energy_grid_fragility: 0.75, water_system_stress: 0.62,
    food_supply_resilience: 0.42, civic_ai_governance_gap: 0.55, algorithmic_discrimination_risk: 0.50,
    smart_city_lock_in: 0.52, data_extractivism_index: 0.48, urban_heat_island_intensity: 0.58,
    infrastructure_decay_rate: 0.70, civic_engagement_erosion: 0.55,
  },
  // UCI-008 — critical, smart_city_monopoly (megacity, NOAM)
  {
    id: "UCI-008", city_type: "megacity", region: "NOAM",
    surveillance_density: 0.62, digital_infrastructure_vulnerability: 0.60, social_control_index: 0.58,
    inequality_tension_index: 0.65, migration_pressure: 0.55, housing_crisis_index: 0.60,
    mobility_gridlock_risk: 0.62, energy_grid_fragility: 0.58, water_system_stress: 0.55,
    food_supply_resilience: 0.40, civic_ai_governance_gap: 0.68, algorithmic_discrimination_risk: 0.65,
    smart_city_lock_in: 0.85, data_extractivism_index: 0.78, urban_heat_island_intensity: 0.60,
    infrastructure_decay_rate: 0.55, civic_engagement_erosion: 0.62,
  },
];

type EntityInput = typeof MOCK_ENTITIES[0];

function surveillanceScore(e: EntityInput): number {
  const raw = (
    e.surveillance_density * 0.4
    + e.social_control_index * 0.35
    + e.algorithmic_discrimination_risk * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function resilienceScore(e: EntityInput): number {
  const raw = (
    e.digital_infrastructure_vulnerability * 0.4
    + e.energy_grid_fragility * 0.35
    + e.water_system_stress * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function socialScore(e: EntityInput): number {
  const raw = (
    e.inequality_tension_index * 0.4
    + e.housing_crisis_index * 0.35
    + e.civic_engagement_erosion * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function governanceScore(e: EntityInput): number {
  const raw = (
    e.civic_ai_governance_gap * 0.4
    + e.smart_city_lock_in * 0.35
    + e.data_extractivism_index * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function urbanComposite(surv: number, res: number, soc: number, gov: number): number {
  return Math.round((surv * 0.30 + res * 0.25 + soc * 0.25 + gov * 0.20) * 100) / 100;
}

function urbanRisk(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}

function urbanPattern(e: EntityInput): string {
  if (e.surveillance_density >= 0.70 && e.social_control_index >= 0.65) return "surveillance_state";
  if (e.digital_infrastructure_vulnerability >= 0.70 && e.energy_grid_fragility >= 0.65) return "infrastructure_collapse";
  if (e.inequality_tension_index >= 0.70 && e.housing_crisis_index >= 0.65) return "social_explosion";
  if (e.algorithmic_discrimination_risk >= 0.70 && e.civic_ai_governance_gap >= 0.60) return "algorithmic_oppression";
  if (e.smart_city_lock_in >= 0.70 && e.data_extractivism_index >= 0.65) return "smart_city_monopoly";
  return "none";
}

function urbanSeverity(composite: number): string {
  if (composite >= 75) return "urban_emergency";
  if (composite >= 50) return "high_urban_risk";
  if (composite >= 25) return "urban_tension";
  return "urban_resilient";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "urban_emergency_intervention";
  if (risk === "high" && pattern === "surveillance_state") return "civil_liberties_audit";
  if (risk === "high") return "urban_resilience_program";
  if (risk === "moderate") return "urban_monitoring";
  return "no_action";
}

function urbanSignal(e: EntityInput, risk: string, composite: number): string {
  if (risk === "critical") {
    return `Critique — densité surveillance ${Math.round(e.surveillance_density * 100)}% — tension sociale ${Math.round(e.inequality_tension_index * 100)}% — composite ${Math.round(composite)}`;
  }
  if (risk === "high") {
    return `Élevé — vulnérabilité infrastructure ${Math.round(e.digital_infrastructure_vulnerability * 100)}% — écart gouvernance IA ${Math.round(e.civic_ai_governance_gap * 100)}% — composite ${Math.round(composite)}`;
  }
  if (risk === "moderate") {
    return `Modéré — fragmentation urbaine ${Math.round(e.housing_crisis_index * 100)}% — composite ${Math.round(composite)}`;
  }
  return "Ville résiliente — gouvernance urbaine saine, cohésion sociale élevée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const surv      = surveillanceScore(e);
      const res       = resilienceScore(e);
      const soc       = socialScore(e);
      const gov       = governanceScore(e);
      const composite = urbanComposite(surv, res, soc, gov);
      const risk      = urbanRisk(composite);
      const pattern   = urbanPattern(e);
      const severity  = urbanSeverity(composite);
      const action    = recommendedAction(risk, pattern);
      const signal    = urbanSignal(e, risk, composite);

      return {
        id:                    e.entity_id,
        region:                       e.region,
        city_type:                    e.city_type,
        urban_risk:                   risk,
        urban_pattern:                pattern,
        urban_severity:               severity,
        recommended_action:           action,
        surveillance_score:           surv,
        resilience_score:             res,
        social_score:                 soc,
        governance_score:             gov,
        urban_composite:              composite,
        is_urban_crisis:              composite >= 60,
        requires_urban_intervention:  composite >= 40,
        urban_signal:                 signal,
      };
    });

    const risk_counts: Record<string, number>     = {};
    const pattern_counts: Record<string, number>  = {};
    const severity_counts: Record<string, number> = {};
    const action_counts: Record<string, number>   = {};
    let tSurv = 0, tRes = 0, tSoc = 0, tGov = 0, tComp = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      risk_counts[ent.urban_risk]         = (risk_counts[ent.urban_risk]         || 0) + 1;
      pattern_counts[ent.urban_pattern]   = (pattern_counts[ent.urban_pattern]   || 0) + 1;
      severity_counts[ent.urban_severity] = (severity_counts[ent.urban_severity] || 0) + 1;
      action_counts[ent.recommended_action] = (action_counts[ent.recommended_action] || 0) + 1;
      tSurv += ent.surveillance_score;
      tRes  += ent.resilience_score;
      tSoc  += ent.social_score;
      tGov  += ent.governance_score;
      tComp += ent.urban_composite;
      if (ent.is_urban_crisis)             crisisCount++;
      if (ent.requires_urban_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      total:                          n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_urban_composite:            avgComposite,
      urban_crisis_count:             crisisCount,
      urban_intervention_count:       interventionCount,
      avg_surveillance_score:         Math.round(tSurv / n * 10) / 10,
      avg_resilience_score:           Math.round(tRes  / n * 10) / 10,
      avg_social_score:               Math.round(tSoc  / n * 10) / 10,
      avg_governance_score:           Math.round(tGov  / n * 10) / 10,
      avg_estimated_urban_risk_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "urban-intelligence-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/urban-intelligence-engine`);
    const data = await upstream.json();
    return NextResponse.json(sealResponse(data, "urban-intelligence-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable" }, "urban-intelligence-engine"),
      { status: 502 }
    );
  }
}
