import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // ETC-001 — EMEA, ai_quantum_cluster — critical, convergence_singularity
  { id: "ETC-001", tech_cluster: "ai_quantum_cluster", region: "EMEA",
    ai_capability_acceleration: 0.88, quantum_computing_readiness: 0.75, biotech_convergence_rate: 0.72,
    nanotech_integration: 0.60, robotics_autonomy_level: 0.65, energy_transition_speed: 0.50,
    network_effect_multiplier: 0.68, disruption_velocity: 0.82, incumbent_displacement_rate: 0.60,
    regulatory_adaptation_lag: 0.70, talent_concentration: 0.72, innovation_inequality: 0.55,
    platform_dominance_risk: 0.65, open_source_disruption: 0.58, exponential_blind_spot: 0.62,
    technology_sovereignty_gap: 0.65, adoption_curve_inflection: 0.80 },
  // ETC-002 — APAC, biotech_cluster — low, controlled_innovation/none
  { id: "ETC-002", tech_cluster: "biotech_cluster", region: "APAC",
    ai_capability_acceleration: 0.15, quantum_computing_readiness: 0.20, biotech_convergence_rate: 0.18,
    nanotech_integration: 0.12, robotics_autonomy_level: 0.15, energy_transition_speed: 0.22,
    network_effect_multiplier: 0.18, disruption_velocity: 0.12, incumbent_displacement_rate: 0.15,
    regulatory_adaptation_lag: 0.20, talent_concentration: 0.18, innovation_inequality: 0.15,
    platform_dominance_risk: 0.12, open_source_disruption: 0.18, exponential_blind_spot: 0.15,
    technology_sovereignty_gap: 0.18, adoption_curve_inflection: 0.12 },
  // ETC-003 — NOAM, platform_tech — high, incumbent_collapse
  { id: "ETC-003", tech_cluster: "platform_tech", region: "NOAM",
    ai_capability_acceleration: 0.60, quantum_computing_readiness: 0.45, biotech_convergence_rate: 0.40,
    nanotech_integration: 0.35, robotics_autonomy_level: 0.50, energy_transition_speed: 0.38,
    network_effect_multiplier: 0.62, disruption_velocity: 0.72, incumbent_displacement_rate: 0.78,
    regulatory_adaptation_lag: 0.52, talent_concentration: 0.55, innovation_inequality: 0.48,
    platform_dominance_risk: 0.60, open_source_disruption: 0.65, exponential_blind_spot: 0.45,
    technology_sovereignty_gap: 0.42, adoption_curve_inflection: 0.55 },
  // ETC-004 — LATAM, biotech_cluster — low, controlled_innovation/none
  { id: "ETC-004", tech_cluster: "biotech_cluster", region: "LATAM",
    ai_capability_acceleration: 0.18, quantum_computing_readiness: 0.15, biotech_convergence_rate: 0.20,
    nanotech_integration: 0.15, robotics_autonomy_level: 0.12, energy_transition_speed: 0.18,
    network_effect_multiplier: 0.15, disruption_velocity: 0.18, incumbent_displacement_rate: 0.12,
    regulatory_adaptation_lag: 0.22, talent_concentration: 0.15, innovation_inequality: 0.18,
    platform_dominance_risk: 0.15, open_source_disruption: 0.12, exponential_blind_spot: 0.18,
    technology_sovereignty_gap: 0.15, adoption_curve_inflection: 0.18 },
  // ETC-005 — MEA, ai_quantum_cluster — critical, platform_monopolization
  { id: "ETC-005", tech_cluster: "ai_quantum_cluster", region: "MEA",
    ai_capability_acceleration: 0.78, quantum_computing_readiness: 0.55, biotech_convergence_rate: 0.45,
    nanotech_integration: 0.50, robotics_autonomy_level: 0.60, energy_transition_speed: 0.42,
    network_effect_multiplier: 0.70, disruption_velocity: 0.65, incumbent_displacement_rate: 0.60,
    regulatory_adaptation_lag: 0.68, talent_concentration: 0.72, innovation_inequality: 0.55,
    platform_dominance_risk: 0.80, open_source_disruption: 0.58, exponential_blind_spot: 0.55,
    technology_sovereignty_gap: 0.62, adoption_curve_inflection: 0.72 },
  // ETC-006 — EMEA, energy_tech — moderate, none
  { id: "ETC-006", tech_cluster: "energy_tech", region: "EMEA",
    ai_capability_acceleration: 0.35, quantum_computing_readiness: 0.30, biotech_convergence_rate: 0.28,
    nanotech_integration: 0.32, robotics_autonomy_level: 0.35, energy_transition_speed: 0.55,
    network_effect_multiplier: 0.38, disruption_velocity: 0.35, incumbent_displacement_rate: 0.32,
    regulatory_adaptation_lag: 0.38, talent_concentration: 0.35, innovation_inequality: 0.30,
    platform_dominance_risk: 0.30, open_source_disruption: 0.35, exponential_blind_spot: 0.32,
    technology_sovereignty_gap: 0.35, adoption_curve_inflection: 0.30 },
  // ETC-007 — APAC, platform_tech — high, sovereignty_vacuum
  { id: "ETC-007", tech_cluster: "platform_tech", region: "APAC",
    ai_capability_acceleration: 0.55, quantum_computing_readiness: 0.42, biotech_convergence_rate: 0.38,
    nanotech_integration: 0.35, robotics_autonomy_level: 0.48, energy_transition_speed: 0.38,
    network_effect_multiplier: 0.50, disruption_velocity: 0.52, incumbent_displacement_rate: 0.48,
    regulatory_adaptation_lag: 0.55, talent_concentration: 0.52, innovation_inequality: 0.45,
    platform_dominance_risk: 0.55, open_source_disruption: 0.48, exponential_blind_spot: 0.65,
    technology_sovereignty_gap: 0.75, adoption_curve_inflection: 0.50 },
  // ETC-008 — NOAM, ai_quantum_cluster — critical, innovation_inequality_spiral
  { id: "ETC-008", tech_cluster: "ai_quantum_cluster", region: "NOAM",
    ai_capability_acceleration: 0.65, quantum_computing_readiness: 0.55, biotech_convergence_rate: 0.50,
    nanotech_integration: 0.58, robotics_autonomy_level: 0.70, energy_transition_speed: 0.48,
    network_effect_multiplier: 0.75, disruption_velocity: 0.68, incumbent_displacement_rate: 0.62,
    regulatory_adaptation_lag: 0.72, talent_concentration: 0.70, innovation_inequality: 0.78,
    platform_dominance_risk: 0.65, open_source_disruption: 0.72, exponential_blind_spot: 0.55,
    technology_sovereignty_gap: 0.60, adoption_curve_inflection: 0.75 },
];

type Entity = typeof MOCK_ENTITIES[0];

function accelerationScore(e: Entity): number {
  const raw = e.ai_capability_acceleration * 0.35 + e.disruption_velocity * 0.35 + e.adoption_curve_inflection * 0.30;
  return Math.round(raw * 100 * 100) / 100;
}
function displacementScore(e: Entity): number {
  const raw = e.incumbent_displacement_rate * 0.40 + e.open_source_disruption * 0.35 + e.network_effect_multiplier * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}
function concentrationScore(e: Entity): number {
  const raw = e.talent_concentration * 0.40 + e.platform_dominance_risk * 0.35 + e.innovation_inequality * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}
function sovereigntyScore(e: Entity): number {
  const raw = e.technology_sovereignty_gap * 0.40 + e.exponential_blind_spot * 0.35 + e.regulatory_adaptation_lag * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}
function disruptionComposite(acc: number, disp: number, conc: number, sov: number): number {
  return Math.round((acc * 0.30 + disp * 0.25 + conc * 0.25 + sov * 0.20) * 100) / 100;
}
function disruptionRisk(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function disruptionPattern(e: Entity): string {
  if (e.ai_capability_acceleration >= 0.70 && (e.quantum_computing_readiness + e.biotech_convergence_rate) / 2 >= 0.60)
    return "convergence_singularity";
  if (e.incumbent_displacement_rate >= 0.70 && e.disruption_velocity >= 0.65)
    return "incumbent_collapse";
  if (e.platform_dominance_risk >= 0.70 && e.talent_concentration >= 0.65)
    return "platform_monopolization";
  if (e.technology_sovereignty_gap >= 0.70 && e.exponential_blind_spot >= 0.60)
    return "sovereignty_vacuum";
  if (e.innovation_inequality >= 0.70 && e.regulatory_adaptation_lag >= 0.60)
    return "innovation_inequality_spiral";
  return "none";
}
function disruptionSeverity(composite: number): string {
  if (composite >= 75) return "exponential_rupture";
  if (composite >= 50) return "high_disruption";
  if (composite >= 25) return "disruption_developing";
  return "controlled_innovation";
}
function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "disruption_emergency_response";
  if (risk === "high" && pattern === "convergence_singularity") return "singularity_preparedness";
  if (risk === "high") return "disruption_hedging";
  if (risk === "moderate") return "tech_monitoring";
  return "no_action";
}
function disruptionSignal(e: Entity, risk: string, composite: number): string {
  const compInt = Math.round(composite);
  if (risk === "critical") {
    return `Critique — accélération IA ${Math.round(e.ai_capability_acceleration * 100)}% — déplacement ${Math.round(e.incumbent_displacement_rate * 100)}% — composite ${compInt}`;
  }
  if (risk === "high") {
    return `Élevé — concentration talentielle ${Math.round(e.talent_concentration * 100)}% — vitesse disruption ${Math.round(e.disruption_velocity * 100)}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `Modéré — inégalité innovation ${Math.round(e.innovation_inequality * 100)}% — composite ${compInt}`;
  }
  return "Convergence technologique maîtrisée — souveraineté préservée, disruption anticipée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[exponential-tech-convergence-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number> = {}, pc: Record<string,number> = {},
          sc: Record<string,number> = {}, ac: Record<string,number> = {};
    let tAcc=0, tDisp=0, tConc=0, tSov=0, tComp=0, crisisC=0, interventionC=0;
    for (const ent of entities) {
      rc[ent.disruption_risk]     = (rc[ent.disruption_risk]     || 0) + 1;
      pc[ent.disruption_pattern]  = (pc[ent.disruption_pattern]  || 0) + 1;
      sc[ent.disruption_severity] = (sc[ent.disruption_severity] || 0) + 1;
      ac[ent.recommended_action]  = (ac[ent.recommended_action]  || 0) + 1;
      tAcc  += ent.acceleration_score;
      tDisp += ent.displacement_score;
      tConc += ent.concentration_score;
      tSov  += ent.sovereignty_score;
      tComp += ent.disruption_composite;
      if (ent.is_in_disruption_crisis)          crisisC++;
      if (ent.requires_disruption_intervention) interventionC++;
    }
    const n = entities.length;
    const avgComp = Math.round(tComp / n * 10) / 10;
    const summary = {
      total:                            n,
      risk_counts:                      rc,
      pattern_counts:                   pc,
      severity_counts:                  sc,
      action_counts:                    ac,
      avg_disruption_composite:         avgComp,
      disruption_crisis_count:          crisisC,
      disruption_intervention_count:    interventionC,
      avg_acceleration_score:           Math.round(tAcc  / n * 10) / 10,
      avg_displacement_score:           Math.round(tDisp / n * 10) / 10,
      avg_concentration_score:          Math.round(tConc / n * 10) / 10,
      avg_sovereignty_score:            Math.round(tSov  / n * 10) / 10,
      avg_estimated_disruption_index:   Math.round(avgComp / 100 * 10 * 100) / 100,
    };
    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "exponential-tech-convergence-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/exponential-tech-convergence-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return sealResponse(NextResponse.json(sealResponse(data, "exponential-tech-convergence-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream swarm unavailable" }, "exponential-tech-convergence-engine"),
      { status: 502 }
    ));
  }
}
