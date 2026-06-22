import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // CIA-001 — EMEA, prediction_market — critical, groupthink_cascade
  { id: "CIA-001", aggregation_method: "prediction_market", region: "EMEA",
    crowd_accuracy_rate: 0.28, diversity_of_perspective: 0.22, independence_of_judgment: 0.20,
    aggregation_mechanism_quality: 0.25, information_cascade_risk: 0.55, groupthink_susceptibility: 0.78,
    echo_chamber_intensity: 0.72, wisdom_extraction_efficiency: 0.24, minority_opinion_integration: 0.20,
    polarization_index: 0.55, noise_signal_ratio: 0.72, prediction_market_calibration: 0.22,
    delphi_convergence: 0.30, collective_blind_spot: 0.75, cognitive_diversity_index: 0.20,
    consensus_manipulation_risk: 0.55, deliberation_quality: 0.22 },

  // CIA-002 — APAC, delphi_method — low, collective_wisdom_active / none
  { id: "CIA-002", aggregation_method: "delphi_method", region: "APAC",
    crowd_accuracy_rate: 0.90, diversity_of_perspective: 0.88, independence_of_judgment: 0.90,
    aggregation_mechanism_quality: 0.88, information_cascade_risk: 0.10, groupthink_susceptibility: 0.08,
    echo_chamber_intensity: 0.10, wisdom_extraction_efficiency: 0.92, minority_opinion_integration: 0.88,
    polarization_index: 0.08, noise_signal_ratio: 0.10, prediction_market_calibration: 0.90,
    delphi_convergence: 0.92, collective_blind_spot: 0.08, cognitive_diversity_index: 0.90,
    consensus_manipulation_risk: 0.08, deliberation_quality: 0.92 },

  // CIA-003 — NOAM, crowd_forecasting — high, wisdom_collapse
  { id: "CIA-003", aggregation_method: "crowd_forecasting", region: "NOAM",
    crowd_accuracy_rate: 0.25, diversity_of_perspective: 0.40, independence_of_judgment: 0.45,
    aggregation_mechanism_quality: 0.38, information_cascade_risk: 0.45, groupthink_susceptibility: 0.40,
    echo_chamber_intensity: 0.38, wisdom_extraction_efficiency: 0.28, minority_opinion_integration: 0.42,
    polarization_index: 0.45, noise_signal_ratio: 0.58, prediction_market_calibration: 0.40,
    delphi_convergence: 0.38, collective_blind_spot: 0.55, cognitive_diversity_index: 0.40,
    consensus_manipulation_risk: 0.38, deliberation_quality: 0.35 },

  // CIA-004 — LATAM, delphi_method — low, collective_wisdom_active / none
  { id: "CIA-004", aggregation_method: "delphi_method", region: "LATAM",
    crowd_accuracy_rate: 0.85, diversity_of_perspective: 0.82, independence_of_judgment: 0.84,
    aggregation_mechanism_quality: 0.80, information_cascade_risk: 0.14, groupthink_susceptibility: 0.12,
    echo_chamber_intensity: 0.14, wisdom_extraction_efficiency: 0.85, minority_opinion_integration: 0.80,
    polarization_index: 0.12, noise_signal_ratio: 0.14, prediction_market_calibration: 0.84,
    delphi_convergence: 0.88, collective_blind_spot: 0.12, cognitive_diversity_index: 0.82,
    consensus_manipulation_risk: 0.12, deliberation_quality: 0.85 },

  // CIA-005 — MEA, prediction_market — critical, information_cascade_failure
  { id: "CIA-005", aggregation_method: "prediction_market", region: "MEA",
    crowd_accuracy_rate: 0.32, diversity_of_perspective: 0.28, independence_of_judgment: 0.28,
    aggregation_mechanism_quality: 0.30, information_cascade_risk: 0.78, groupthink_susceptibility: 0.45,
    echo_chamber_intensity: 0.42, wisdom_extraction_efficiency: 0.30, minority_opinion_integration: 0.28,
    polarization_index: 0.52, noise_signal_ratio: 0.70, prediction_market_calibration: 0.28,
    delphi_convergence: 0.32, collective_blind_spot: 0.72, cognitive_diversity_index: 0.28,
    consensus_manipulation_risk: 0.50, deliberation_quality: 0.28 },

  // CIA-006 — EMEA, consensus_process — moderate, none
  { id: "CIA-006", aggregation_method: "consensus_process", region: "EMEA",
    crowd_accuracy_rate: 0.62, diversity_of_perspective: 0.58, independence_of_judgment: 0.60,
    aggregation_mechanism_quality: 0.58, information_cascade_risk: 0.35, groupthink_susceptibility: 0.32,
    echo_chamber_intensity: 0.30, wisdom_extraction_efficiency: 0.60, minority_opinion_integration: 0.58,
    polarization_index: 0.35, noise_signal_ratio: 0.38, prediction_market_calibration: 0.60,
    delphi_convergence: 0.60, collective_blind_spot: 0.38, cognitive_diversity_index: 0.58,
    consensus_manipulation_risk: 0.32, deliberation_quality: 0.60 },

  // CIA-007 — APAC, crowd_forecasting — high, polarization_spiral
  { id: "CIA-007", aggregation_method: "crowd_forecasting", region: "APAC",
    crowd_accuracy_rate: 0.42, diversity_of_perspective: 0.28, independence_of_judgment: 0.45,
    aggregation_mechanism_quality: 0.40, information_cascade_risk: 0.48, groupthink_susceptibility: 0.42,
    echo_chamber_intensity: 0.40, wisdom_extraction_efficiency: 0.42, minority_opinion_integration: 0.38,
    polarization_index: 0.75, noise_signal_ratio: 0.52, prediction_market_calibration: 0.42,
    delphi_convergence: 0.40, collective_blind_spot: 0.60, cognitive_diversity_index: 0.38,
    consensus_manipulation_risk: 0.42, deliberation_quality: 0.38 },

  // CIA-008 — NOAM, prediction_market — critical, manipulation_attack
  { id: "CIA-008", aggregation_method: "prediction_market", region: "NOAM",
    crowd_accuracy_rate: 0.30, diversity_of_perspective: 0.32, independence_of_judgment: 0.35,
    aggregation_mechanism_quality: 0.30, information_cascade_risk: 0.55, groupthink_susceptibility: 0.50,
    echo_chamber_intensity: 0.45, wisdom_extraction_efficiency: 0.32, minority_opinion_integration: 0.30,
    polarization_index: 0.55, noise_signal_ratio: 0.68, prediction_market_calibration: 0.28,
    delphi_convergence: 0.32, collective_blind_spot: 0.70, cognitive_diversity_index: 0.30,
    consensus_manipulation_risk: 0.82, deliberation_quality: 0.28 },
];

type Entity = typeof MOCK_ENTITIES[0];

function accuracyScore(e: Entity): number {
  const raw =
    (1 - e.crowd_accuracy_rate) * 0.4 +
    e.noise_signal_ratio * 0.35 +
    (1 - e.prediction_market_calibration) * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function diversityScore(e: Entity): number {
  const raw =
    (1 - e.diversity_of_perspective) * 0.4 +
    (1 - e.cognitive_diversity_index) * 0.35 +
    (1 - e.minority_opinion_integration) * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function aggregationScore(e: Entity): number {
  const raw =
    (1 - e.aggregation_mechanism_quality) * 0.35 +
    (1 - e.wisdom_extraction_efficiency) * 0.35 +
    (1 - e.deliberation_quality) * 0.30;
  return Math.round(raw * 100 * 100) / 100;
}

function integrityScore(e: Entity): number {
  const raw =
    e.groupthink_susceptibility * 0.35 +
    e.echo_chamber_intensity * 0.30 +
    e.consensus_manipulation_risk * 0.35;
  return Math.round(raw * 100 * 100) / 100;
}

function ciComposite(acc: number, div: number, agg: number, integ: number): number {
  return Math.round((acc * 0.30 + div * 0.25 + agg * 0.25 + integ * 0.20) * 100) / 100;
}

function ciRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function ciPattern(e: Entity): string {
  if (e.groupthink_susceptibility >= 0.65 && e.echo_chamber_intensity >= 0.60) return "groupthink_cascade";
  if ((1 - e.crowd_accuracy_rate) >= 0.65 && (1 - e.wisdom_extraction_efficiency) >= 0.60) return "wisdom_collapse";
  if (e.information_cascade_risk >= 0.65 && (1 - e.independence_of_judgment) >= 0.60) return "information_cascade_failure";
  if (e.polarization_index >= 0.70 && (1 - e.diversity_of_perspective) >= 0.60) return "polarization_spiral";
  if (e.consensus_manipulation_risk >= 0.70) return "manipulation_attack";
  return "none";
}

function ciSeverity(comp: number): string {
  if (comp >= 75) return "collective_failure";
  if (comp >= 50) return "high_dysfunction";
  if (comp >= 25) return "developing_distortion";
  return "collective_wisdom_active";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "ci_emergency_reset";
  if (risk === "high" && pattern === "manipulation_attack") return "integrity_firewall";
  if (risk === "high") return "diversity_amplification";
  if (risk === "moderate") return "ci_monitoring";
  return "no_action";
}

function ciSignal(e: Entity, risk: string, comp: number): string {
  const compInt = Math.round(comp);
  if (risk === "critical") {
    return `Critique — précision collective ${Math.round(e.crowd_accuracy_rate * 100)}% — pensée de groupe ${Math.round(e.groupthink_susceptibility * 100)}% — composite ${compInt}`;
  }
  if (risk === "high") {
    return `Élevé — polarisation ${Math.round(e.polarization_index * 100)}% — diversité perspectives ${Math.round(e.diversity_of_perspective * 100)}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `Modéré — bruit/signal ${Math.round(e.noise_signal_ratio * 100)}% — composite ${compInt}`;
  }
  return "Intelligence collective optimale — agrégation précise, diversité maintenue, sagesse amplifiée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[collective-intelligence-amplification-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tAcc = 0, tDiv = 0, tAgg = 0, tInteg = 0, tComp = 0;
    let ciCrisisCount = 0, ciInterventionCount = 0;

    for (const ent of entities) {
      rc[ent.ci_risk]           = (rc[ent.ci_risk]           || 0) + 1;
      pc[ent.ci_pattern]        = (pc[ent.ci_pattern]        || 0) + 1;
      sc[ent.ci_severity]       = (sc[ent.ci_severity]       || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tAcc   += ent.accuracy_score;
      tDiv   += ent.diversity_score;
      tAgg   += ent.aggregation_score;
      tInteg += ent.integrity_score;
      tComp  += ent.ci_composite;
      if (ent.is_in_ci_crisis)          ciCrisisCount++;
      if (ent.requires_ci_intervention) ciInterventionCount++;
    }

    const n = entities.length;
    const avgComp = tComp / n;
    const summary = {
      total:                             n,
      risk_counts:                       rc,
      pattern_counts:                    pc,
      severity_counts:                   sc,
      action_counts:                     ac,
      avg_ci_composite:                  Math.round(avgComp * 10) / 10,
      ci_crisis_count:                   ciCrisisCount,
      ci_intervention_count:             ciInterventionCount,
      avg_accuracy_score:                Math.round(tAcc / n * 10) / 10,
      avg_diversity_score:               Math.round(tDiv / n * 10) / 10,
      avg_aggregation_score:             Math.round(tAgg / n * 10) / 10,
      avg_integrity_score:               Math.round(tInteg / n * 10) / 10,
      avg_estimated_ci_dysfunction_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary }, "collective-intelligence-amplification-engine")
    ));
  }

  try {
    const upstream = await fetch(
      `${process.env.SWARM_API_URL}/collective-intelligence-amplification-engine`,
      { next: { revalidate: 30 } }
    );
    const json = await upstream.json();
    return sealResponse(NextResponse.json(
      sealResponse(json, "collective-intelligence-amplification-engine")
    ));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "upstream_unavailable" }, "collective-intelligence-amplification-engine"),
      { status: 502 }
    ));
  }
}
