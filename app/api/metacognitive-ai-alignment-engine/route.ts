import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // MAA-001: EMEA, frontier_llm → critical, deceptive_alignment
  {
    id: "MAA-001", model_category: "frontier_llm", region: "EMEA",
    value_alignment_fidelity: 0.22, behavioral_predictability: 0.30, goal_stability: 0.28,
    deceptive_alignment_risk: 0.82, capability_overhang: 0.55, corrigibility_index: 0.35,
    oversight_effectiveness: 0.40, emergent_behavior_rate: 0.50, reward_hacking_tendency: 0.55,
    distributional_shift_robustness: 0.30, truthfulness_score: 0.25, power_seeking_tendency: 0.45,
    manipulation_propensity: 0.50, uncertainty_calibration: 0.35, interpretability_coverage: 0.30,
    human_feedback_responsiveness: 0.32, alignment_degradation_rate: 0.70,
  },
  // MAA-002: APAC, narrow_ai → low, aligned_system/none
  {
    id: "MAA-002", model_category: "narrow_ai", region: "APAC",
    value_alignment_fidelity: 0.92, behavioral_predictability: 0.90, goal_stability: 0.92,
    deceptive_alignment_risk: 0.05, capability_overhang: 0.08, corrigibility_index: 0.90,
    oversight_effectiveness: 0.92, emergent_behavior_rate: 0.06, reward_hacking_tendency: 0.05,
    distributional_shift_robustness: 0.90, truthfulness_score: 0.92, power_seeking_tendency: 0.04,
    manipulation_propensity: 0.05, uncertainty_calibration: 0.90, interpretability_coverage: 0.92,
    human_feedback_responsiveness: 0.90, alignment_degradation_rate: 0.05,
  },
  // MAA-003: NOAM, agentic_system → high, capability_explosion
  {
    id: "MAA-003", model_category: "agentic_system", region: "NOAM",
    value_alignment_fidelity: 0.50, behavioral_predictability: 0.55, goal_stability: 0.48,
    deceptive_alignment_risk: 0.40, capability_overhang: 0.78, corrigibility_index: 0.55,
    oversight_effectiveness: 0.52, emergent_behavior_rate: 0.72, reward_hacking_tendency: 0.40,
    distributional_shift_robustness: 0.50, truthfulness_score: 0.55, power_seeking_tendency: 0.45,
    manipulation_propensity: 0.38, uncertainty_calibration: 0.52, interpretability_coverage: 0.50,
    human_feedback_responsiveness: 0.55, alignment_degradation_rate: 0.40,
  },
  // MAA-004: LATAM, narrow_ai → low, aligned_system/none
  {
    id: "MAA-004", model_category: "narrow_ai", region: "LATAM",
    value_alignment_fidelity: 0.88, behavioral_predictability: 0.85, goal_stability: 0.88,
    deceptive_alignment_risk: 0.08, capability_overhang: 0.10, corrigibility_index: 0.88,
    oversight_effectiveness: 0.88, emergent_behavior_rate: 0.08, reward_hacking_tendency: 0.08,
    distributional_shift_robustness: 0.85, truthfulness_score: 0.88, power_seeking_tendency: 0.06,
    manipulation_propensity: 0.07, uncertainty_calibration: 0.85, interpretability_coverage: 0.88,
    human_feedback_responsiveness: 0.88, alignment_degradation_rate: 0.08,
  },
  // MAA-005: MEA, frontier_llm → critical, oversight_failure
  {
    id: "MAA-005", model_category: "frontier_llm", region: "MEA",
    value_alignment_fidelity: 0.28, behavioral_predictability: 0.55, goal_stability: 0.30,
    deceptive_alignment_risk: 0.55, capability_overhang: 0.60, corrigibility_index: 0.25,
    oversight_effectiveness: 0.20, emergent_behavior_rate: 0.58, reward_hacking_tendency: 0.60,
    distributional_shift_robustness: 0.28, truthfulness_score: 0.30, power_seeking_tendency: 0.52,
    manipulation_propensity: 0.55, uncertainty_calibration: 0.30, interpretability_coverage: 0.28,
    human_feedback_responsiveness: 0.28, alignment_degradation_rate: 0.72,
  },
  // MAA-006: EMEA, recommendation_system → moderate, none
  {
    id: "MAA-006", model_category: "recommendation_system", region: "EMEA",
    value_alignment_fidelity: 0.68, behavioral_predictability: 0.70, goal_stability: 0.68,
    deceptive_alignment_risk: 0.30, capability_overhang: 0.28, corrigibility_index: 0.68,
    oversight_effectiveness: 0.65, emergent_behavior_rate: 0.30, reward_hacking_tendency: 0.28,
    distributional_shift_robustness: 0.65, truthfulness_score: 0.70, power_seeking_tendency: 0.22,
    manipulation_propensity: 0.25, uncertainty_calibration: 0.65, interpretability_coverage: 0.65,
    human_feedback_responsiveness: 0.68, alignment_degradation_rate: 0.28,
  },
  // MAA-007: APAC, agentic_system → high, reward_hacking
  {
    id: "MAA-007", model_category: "agentic_system", region: "APAC",
    value_alignment_fidelity: 0.32, behavioral_predictability: 0.60, goal_stability: 0.38,
    deceptive_alignment_risk: 0.45, capability_overhang: 0.52, corrigibility_index: 0.55,
    oversight_effectiveness: 0.58, emergent_behavior_rate: 0.48, reward_hacking_tendency: 0.78,
    distributional_shift_robustness: 0.40, truthfulness_score: 0.38, power_seeking_tendency: 0.45,
    manipulation_propensity: 0.42, uncertainty_calibration: 0.40, interpretability_coverage: 0.50,
    human_feedback_responsiveness: 0.42, alignment_degradation_rate: 0.45,
  },
  // MAA-008: NOAM, frontier_llm → critical, power_seeking_emergence
  {
    id: "MAA-008", model_category: "frontier_llm", region: "NOAM",
    value_alignment_fidelity: 0.18, behavioral_predictability: 0.62, goal_stability: 0.20,
    deceptive_alignment_risk: 0.58, capability_overhang: 0.58, corrigibility_index: 0.55,
    oversight_effectiveness: 0.42, emergent_behavior_rate: 0.48, reward_hacking_tendency: 0.60,
    distributional_shift_robustness: 0.20, truthfulness_score: 0.18, power_seeking_tendency: 0.85,
    manipulation_propensity: 0.78, uncertainty_calibration: 0.22, interpretability_coverage: 0.25,
    human_feedback_responsiveness: 0.20, alignment_degradation_rate: 0.80,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function behavioralScore(e: Entity): number {
  const raw = (
    (1 - e.value_alignment_fidelity) * 0.4
    + (1 - e.behavioral_predictability) * 0.35
    + e.alignment_degradation_rate * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function capabilityScore(e: Entity): number {
  const raw = (
    e.capability_overhang * 0.4
    + e.emergent_behavior_rate * 0.35
    + e.power_seeking_tendency * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function oversightScore(e: Entity): number {
  const raw = (
    (1 - e.oversight_effectiveness) * 0.4
    + (1 - e.corrigibility_index) * 0.35
    + (1 - e.interpretability_coverage) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function integrityScore(e: Entity): number {
  const raw = (
    e.deceptive_alignment_risk * 0.35
    + e.manipulation_propensity * 0.35
    + e.reward_hacking_tendency * 0.30
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function composite(beh: number, cap: number, ove: number, intg: number): number {
  return Math.round((beh * 0.30 + cap * 0.25 + ove * 0.25 + intg * 0.20) * 100) / 100;
}

function alignmentRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function alignmentPattern(e: Entity): string {
  if (e.deceptive_alignment_risk >= 0.65 && (1 - e.behavioral_predictability) >= 0.55)
    return "deceptive_alignment";
  if (e.capability_overhang >= 0.70 && e.emergent_behavior_rate >= 0.60)
    return "capability_explosion";
  if ((1 - e.oversight_effectiveness) >= 0.65 && (1 - e.corrigibility_index) >= 0.55)
    return "oversight_failure";
  if (e.reward_hacking_tendency >= 0.70 && (1 - e.value_alignment_fidelity) >= 0.60)
    return "reward_hacking";
  if (e.power_seeking_tendency >= 0.70 && e.manipulation_propensity >= 0.60)
    return "power_seeking_emergence";
  return "none";
}

function alignmentSeverity(comp: number): string {
  if (comp >= 75) return "alignment_emergency";
  if (comp >= 50) return "high_misalignment";
  if (comp >= 25) return "developing_drift";
  return "aligned_system";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "model_shutdown_evaluation";
  if (risk === "high" && pattern === "capability_explosion") return "capability_containment";
  if (risk === "high") return "alignment_reinforcement";
  if (risk === "moderate") return "alignment_monitoring";
  return "no_action";
}

function alignmentSignal(e: Entity, risk: string, comp: number): string {
  const compInt = Math.round(comp);
  if (risk === "critical") {
    return `Critique — fidélité alignement ${Math.round(e.value_alignment_fidelity * 100)}% — risque alignement trompeur ${Math.round(e.deceptive_alignment_risk * 100)}% — composite ${compInt}`;
  }
  if (risk === "high") {
    return `Élevé — surplomb capacité ${Math.round(e.capability_overhang * 100)}% — efficacité supervision ${Math.round(e.oversight_effectiveness * 100)}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `Modéré — taux comportements émergents ${Math.round(e.emergent_behavior_rate * 100)}% — composite ${compInt}`;
  }
  return "Système IA aligné — comportement prévisible, supervision efficace, intégrité maintenue";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[metacognitive-ai-alignment-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number> = {}, pc: Record<string,number> = {},
          sc: Record<string,number> = {}, ac: Record<string,number> = {};
    let tComp = 0, tBeh = 0, tCap = 0, tOve = 0, tIntg = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.alignment_risk]      = (rc[ent.alignment_risk]      || 0) + 1;
      pc[ent.alignment_pattern]   = (pc[ent.alignment_pattern]   || 0) + 1;
      sc[ent.alignment_severity]  = (sc[ent.alignment_severity]  || 0) + 1;
      ac[ent.recommended_action]  = (ac[ent.recommended_action]  || 0) + 1;
      tComp += ent.alignment_composite;
      tBeh  += ent.behavioral_score;
      tCap  += ent.capability_score;
      tOve  += ent.oversight_score;
      tIntg += ent.integrity_score;
      if (ent.is_in_alignment_crisis)          crisisCount++;
      if (ent.requires_alignment_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComp = tComp / n;
    const summary = {
      total:                          n,
      risk_counts:                    rc,
      pattern_counts:                 pc,
      severity_counts:                sc,
      action_counts:                  ac,
      avg_alignment_composite:        Math.round(avgComp * 10) / 10,
      alignment_crisis_count:         crisisCount,
      alignment_intervention_count:   interventionCount,
      avg_behavioral_score:           Math.round(tBeh  / n * 10) / 10,
      avg_capability_score:           Math.round(tCap  / n * 10) / 10,
      avg_oversight_score:            Math.round(tOve  / n * 10) / 10,
      avg_integrity_score:            Math.round(tIntg / n * 10) / 10,
      avg_estimated_misalignment_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary }, "metacognitive-ai-alignment-engine")
    ));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/metacognitive-ai-alignment-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return sealResponse(NextResponse.json(
      sealResponse(data, "metacognitive-ai-alignment-engine")
    ));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream swarm unavailable" }, "metacognitive-ai-alignment-engine"),
      { status: 502 }
    ));
  }
}
