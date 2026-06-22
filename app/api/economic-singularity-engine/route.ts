import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// Module 315 — Economic Singularity Simulation Intelligence Engine
// Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles

const MOCK_ENTITIES = [
  // ESI-001: EMEA, advanced_economy → critical, singularity_threshold_breach
  {
    id: "ESI-001", economy_type: "advanced_economy", region: "EMEA",
    ai_labor_displacement_velocity: 0.80,
    productivity_growth_acceleration: 0.75,
    capital_concentration_rate: 0.72,
    conventional_rule_breakdown_index: 0.68,
    automation_penetration_depth: 0.70,
    economic_phase_transition_proximity: 0.78,
    value_creation_redistribution_gap: 0.65,
    post_scarcity_emergence_index: 0.60,
    human_economic_relevance_erosion: 0.72,
    institutional_adaptation_lag: 0.62,
    winner_take_all_intensification: 0.70,
    economic_complexity_explosion: 0.68,
    regulatory_obsolescence_rate: 0.60,
    monetary_system_stress: 0.65,
    social_contract_dissolution_risk: 0.62,
    new_economy_emergence_rate: 0.70,
    singularity_resistance_capacity: 0.25,
  },
  // ESI-002: APAC, emerging_economy → low, none
  {
    id: "ESI-002", economy_type: "emerging_economy", region: "APAC",
    ai_labor_displacement_velocity: 0.15,
    productivity_growth_acceleration: 0.45,
    capital_concentration_rate: 0.22,
    conventional_rule_breakdown_index: 0.18,
    automation_penetration_depth: 0.20,
    economic_phase_transition_proximity: 0.12,
    value_creation_redistribution_gap: 0.20,
    post_scarcity_emergence_index: 0.30,
    human_economic_relevance_erosion: 0.15,
    institutional_adaptation_lag: 0.18,
    winner_take_all_intensification: 0.20,
    economic_complexity_explosion: 0.25,
    regulatory_obsolescence_rate: 0.15,
    monetary_system_stress: 0.20,
    social_contract_dissolution_risk: 0.18,
    new_economy_emergence_rate: 0.35,
    singularity_resistance_capacity: 0.80,
  },
  // ESI-003: NOAM, tech_economy → high, labor_extinction_event
  {
    id: "ESI-003", economy_type: "tech_economy", region: "NOAM",
    ai_labor_displacement_velocity: 0.75,
    productivity_growth_acceleration: 0.80,
    capital_concentration_rate: 0.55,
    conventional_rule_breakdown_index: 0.48,
    automation_penetration_depth: 0.70,
    economic_phase_transition_proximity: 0.50,
    value_creation_redistribution_gap: 0.55,
    post_scarcity_emergence_index: 0.60,
    human_economic_relevance_erosion: 0.68,
    institutional_adaptation_lag: 0.45,
    winner_take_all_intensification: 0.58,
    economic_complexity_explosion: 0.60,
    regulatory_obsolescence_rate: 0.50,
    monetary_system_stress: 0.45,
    social_contract_dissolution_risk: 0.52,
    new_economy_emergence_rate: 0.75,
    singularity_resistance_capacity: 0.40,
  },
  // ESI-004: LATAM, developing_economy → low, none
  {
    id: "ESI-004", economy_type: "developing_economy", region: "LATAM",
    ai_labor_displacement_velocity: 0.12,
    productivity_growth_acceleration: 0.28,
    capital_concentration_rate: 0.18,
    conventional_rule_breakdown_index: 0.14,
    automation_penetration_depth: 0.10,
    economic_phase_transition_proximity: 0.10,
    value_creation_redistribution_gap: 0.15,
    post_scarcity_emergence_index: 0.12,
    human_economic_relevance_erosion: 0.10,
    institutional_adaptation_lag: 0.12,
    winner_take_all_intensification: 0.14,
    economic_complexity_explosion: 0.12,
    regulatory_obsolescence_rate: 0.10,
    monetary_system_stress: 0.15,
    social_contract_dissolution_risk: 0.12,
    new_economy_emergence_rate: 0.18,
    singularity_resistance_capacity: 0.88,
  },
  // ESI-005: MEA, resource_economy → critical, institutional_collapse
  {
    id: "ESI-005", economy_type: "resource_economy", region: "MEA",
    ai_labor_displacement_velocity: 0.65,
    productivity_growth_acceleration: 0.55,
    capital_concentration_rate: 0.68,
    conventional_rule_breakdown_index: 0.62,
    automation_penetration_depth: 0.60,
    economic_phase_transition_proximity: 0.65,
    value_creation_redistribution_gap: 0.60,
    post_scarcity_emergence_index: 0.40,
    human_economic_relevance_erosion: 0.58,
    institutional_adaptation_lag: 0.75,
    winner_take_all_intensification: 0.60,
    economic_complexity_explosion: 0.55,
    regulatory_obsolescence_rate: 0.70,
    monetary_system_stress: 0.65,
    social_contract_dissolution_risk: 0.60,
    new_economy_emergence_rate: 0.45,
    singularity_resistance_capacity: 0.22,
  },
  // ESI-006: EMEA, industrial_economy → moderate, none
  {
    id: "ESI-006", economy_type: "industrial_economy", region: "EMEA",
    ai_labor_displacement_velocity: 0.38,
    productivity_growth_acceleration: 0.42,
    capital_concentration_rate: 0.35,
    conventional_rule_breakdown_index: 0.30,
    automation_penetration_depth: 0.42,
    economic_phase_transition_proximity: 0.32,
    value_creation_redistribution_gap: 0.38,
    post_scarcity_emergence_index: 0.35,
    human_economic_relevance_erosion: 0.30,
    institutional_adaptation_lag: 0.35,
    winner_take_all_intensification: 0.32,
    economic_complexity_explosion: 0.38,
    regulatory_obsolescence_rate: 0.35,
    monetary_system_stress: 0.30,
    social_contract_dissolution_risk: 0.35,
    new_economy_emergence_rate: 0.40,
    singularity_resistance_capacity: 0.62,
  },
  // ESI-007: APAC, platform_economy → high, capital_hypercentralization
  {
    id: "ESI-007", economy_type: "platform_economy", region: "APAC",
    ai_labor_displacement_velocity: 0.55,
    productivity_growth_acceleration: 0.68,
    capital_concentration_rate: 0.78,
    conventional_rule_breakdown_index: 0.50,
    automation_penetration_depth: 0.60,
    economic_phase_transition_proximity: 0.52,
    value_creation_redistribution_gap: 0.60,
    post_scarcity_emergence_index: 0.55,
    human_economic_relevance_erosion: 0.50,
    institutional_adaptation_lag: 0.45,
    winner_take_all_intensification: 0.72,
    economic_complexity_explosion: 0.62,
    regulatory_obsolescence_rate: 0.48,
    monetary_system_stress: 0.50,
    social_contract_dissolution_risk: 0.52,
    new_economy_emergence_rate: 0.65,
    singularity_resistance_capacity: 0.35,
  },
  // ESI-008: NOAM, digital_economy → critical, social_contract_rupture
  {
    id: "ESI-008", economy_type: "digital_economy", region: "NOAM",
    ai_labor_displacement_velocity: 0.65,
    productivity_growth_acceleration: 0.82,
    capital_concentration_rate: 0.60,
    conventional_rule_breakdown_index: 0.55,
    automation_penetration_depth: 0.75,
    economic_phase_transition_proximity: 0.60,
    value_creation_redistribution_gap: 0.72,
    post_scarcity_emergence_index: 0.65,
    human_economic_relevance_erosion: 0.60,
    institutional_adaptation_lag: 0.55,
    winner_take_all_intensification: 0.60,
    economic_complexity_explosion: 0.72,
    regulatory_obsolescence_rate: 0.62,
    monetary_system_stress: 0.68,
    social_contract_dissolution_risk: 0.78,
    new_economy_emergence_rate: 0.75,
    singularity_resistance_capacity: 0.18,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function displacementScore(e: Entity): number {
  return Math.round(
    (e.ai_labor_displacement_velocity * 0.40
      + e.human_economic_relevance_erosion * 0.35
      + e.automation_penetration_depth * 0.25) * 100 * 100
  ) / 100;
}

function transitionScore(e: Entity): number {
  return Math.round(
    (e.economic_phase_transition_proximity * 0.40
      + e.conventional_rule_breakdown_index * 0.35
      + e.institutional_adaptation_lag * 0.25) * 100 * 100
  ) / 100;
}

function concentrationScore(e: Entity): number {
  return Math.round(
    (e.capital_concentration_rate * 0.40
      + e.winner_take_all_intensification * 0.35
      + e.value_creation_redistribution_gap * 0.25) * 100 * 100
  ) / 100;
}

function disruptionScore(e: Entity): number {
  return Math.round(
    (e.regulatory_obsolescence_rate * 0.40
      + e.social_contract_dissolution_risk * 0.35
      + (1 - e.singularity_resistance_capacity) * 0.25) * 100 * 100
  ) / 100;
}

function singularityComposite(disp: number, trans: number, conc: number, disrup: number): number {
  return Math.round(
    Math.min(disp * 0.30 + trans * 0.25 + conc * 0.25 + disrup * 0.20, 100) * 100
  ) / 100;
}

function singularityRisk(c: number): string {
  if (c >= 60) return "critical";
  if (c >= 40) return "high";
  if (c >= 20) return "moderate";
  return "low";
}

function singularitySeverity(c: number): string {
  if (c >= 75) return "singularity_imminent";
  if (c >= 50) return "phase_transition_critical";
  if (c >= 25) return "singularity_approaching";
  return "pre_acceleration";
}

function singularityPattern(e: Entity): string {
  if (e.economic_phase_transition_proximity >= 0.70 && e.conventional_rule_breakdown_index >= 0.65)
    return "singularity_threshold_breach";
  if (e.ai_labor_displacement_velocity >= 0.70 && e.human_economic_relevance_erosion >= 0.65)
    return "labor_extinction_event";
  if (e.capital_concentration_rate >= 0.70 && e.winner_take_all_intensification >= 0.65)
    return "capital_hypercentralization";
  if (e.institutional_adaptation_lag >= 0.70 && e.regulatory_obsolescence_rate >= 0.65)
    return "institutional_collapse";
  if (e.social_contract_dissolution_risk >= 0.70 && e.value_creation_redistribution_gap >= 0.65)
    return "social_contract_rupture";
  return "none";
}

function recommendedAction(risk: string, pat: string): string {
  if (risk === "critical") return "emergency_economic_redesign";
  if (risk === "high") {
    if (pat === "labor_extinction_event") return "universal_income_emergency";
    return "singularity_transition_program";
  }
  if (risk === "moderate") return "economic_monitoring";
  return "no_action";
}

function singularitySignal(e: Entity, risk: string, comp: number): string {
  if (risk === "critical") {
    return `Critique — singularité économique imminente — déplacement travail ${Math.round(e.ai_labor_displacement_velocity * 100)}% — transition de phase — composite ${Math.round(comp)}`;
  }
  if (risk === "high") {
    return `Élevé — accélération singularité — déplacement travail ${Math.round(e.ai_labor_displacement_velocity * 100)}% — concentration capital ${Math.round(e.capital_concentration_rate * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "moderate") {
    return `Modéré — proximité transition économique ${Math.round(e.economic_phase_transition_proximity * 100)}% — composite ${Math.round(comp)}`;
  }
  return "Économie résiliente — règles conventionnelles stables, singularité lointaine, capacité d'adaptation institutionnelle préservée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[economic-singularity-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number> = {};
    const pc: Record<string,number> = {};
    const sc: Record<string,number> = {};
    const ac: Record<string,number> = {};
    let tDisp=0, tTrans=0, tConc=0, tDisrup=0, tComp=0, crisisC=0, interventionC=0;

    for (const ent of entities) {
      rc[ent.singularity_risk]       = (rc[ent.singularity_risk]       || 0) + 1;
      pc[ent.singularity_pattern]    = (pc[ent.singularity_pattern]    || 0) + 1;
      sc[ent.singularity_severity]   = (sc[ent.singularity_severity]   || 0) + 1;
      ac[ent.recommended_action]     = (ac[ent.recommended_action]     || 0) + 1;
      tDisp   += ent.displacement_score;
      tTrans  += ent.transition_score;
      tConc   += ent.concentration_score;
      tDisrup += ent.disruption_score;
      tComp   += ent.singularity_composite;
      if (ent.is_singularity_crisis)           crisisC++;
      if (ent.requires_singularity_intervention) interventionC++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 10) / 10;
    const summary = {
      total:                                     n,
      risk_counts:                               rc,
      pattern_counts:                            pc,
      severity_counts:                           sc,
      action_counts:                             ac,
      avg_singularity_composite:                 avgComp,
      singularity_crisis_count:                  crisisC,
      singularity_intervention_count:            interventionC,
      avg_displacement_score:                    Math.round(tDisp   / n * 10) / 10,
      avg_transition_score:                      Math.round(tTrans  / n * 10) / 10,
      avg_concentration_score:                   Math.round(tConc   / n * 10) / 10,
      avg_disruption_score:                      Math.round(tDisrup / n * 10) / 10,
      avg_estimated_singularity_proximity_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary }, "economic-singularity-engine")
    ));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/economic-singularity-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return sealResponse(NextResponse.json(
      sealResponse(data, "economic-singularity-engine")
    ));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream economic singularity engine unavailable" }, "economic-singularity-engine"),
      { status: 502 }
    ));
  }
}
