import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// Module 323 — Caelum Partners — Cognitive Warfare & Information Operations Intelligence Engine
// Chaima Mhadbi, Fondatrice, Bruxelles

interface CognitiveWarfareEntity {
  id: string;
  operation_type: string;
  region: string;
  disinformation_velocity: number;
  deepfake_deployment_rate: number;
  narrative_weaponization_index: number;
  epistemic_attack_precision: number;
  perception_management_depth: number;
  social_media_amplification_weaponization: number;
  adversarial_ai_content_generation: number;
  influence_bot_network_density: number;
  cognitive_vulnerability_exploitation: number;
  memory_hole_operation_rate: number;
  truth_decay_acceleration: number;
  institutional_trust_erosion_rate: number;
  resilience_to_cognitive_attack: number;
  media_literacy_gap: number;
  fact_checking_bypass_sophistication: number;
  cross_domain_narrative_coherence: number;
  psychological_operation_reach: number;
}

interface CognitiveWarfareResult {
  id: string;
  region: string;
  operation_type: string;
  warfare_risk: string;
  warfare_pattern: string;
  warfare_severity: string;
  recommended_action: string;
  disinformation_score: number;
  influence_score: number;
  erosion_score: number;
  vulnerability_score: number;
  warfare_composite: number;
  is_warfare_crisis: boolean;
  requires_warfare_intervention: boolean;
  warfare_signal: string;
}

function computeScores(e: CognitiveWarfareEntity) {
  const disinformation_score =
    (e.disinformation_velocity * 0.4 +
      e.deepfake_deployment_rate * 0.35 +
      e.adversarial_ai_content_generation * 0.25) *
    100;

  const influence_score =
    (e.influence_bot_network_density * 0.4 +
      e.social_media_amplification_weaponization * 0.35 +
      e.psychological_operation_reach * 0.25) *
    100;

  const erosion_score =
    (e.truth_decay_acceleration * 0.4 +
      e.institutional_trust_erosion_rate * 0.35 +
      e.memory_hole_operation_rate * 0.25) *
    100;

  const vulnerability_score =
    (e.cognitive_vulnerability_exploitation * 0.4 +
      e.media_literacy_gap * 0.35 +
      (1 - e.resilience_to_cognitive_attack) * 0.25) *
    100;

  const warfare_composite =
    disinformation_score * 0.3 +
    influence_score * 0.25 +
    erosion_score * 0.25 +
    vulnerability_score * 0.2;

  return {
    disinformation_score: Math.round(disinformation_score * 100) / 100,
    influence_score: Math.round(influence_score * 100) / 100,
    erosion_score: Math.round(erosion_score * 100) / 100,
    vulnerability_score: Math.round(vulnerability_score * 100) / 100,
    warfare_composite: Math.round(warfare_composite * 100) / 100,
  };
}

function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}

function detectPattern(e: CognitiveWarfareEntity): string {
  if (e.deepfake_deployment_rate >= 0.7 && e.adversarial_ai_content_generation >= 0.65)
    return "deepfake_information_war";
  if (e.truth_decay_acceleration >= 0.7 && e.institutional_trust_erosion_rate >= 0.65)
    return "epistemic_collapse";
  if (e.influence_bot_network_density >= 0.7 && e.social_media_amplification_weaponization >= 0.65)
    return "influence_network_dominance";
  if (e.narrative_weaponization_index >= 0.7 && e.cross_domain_narrative_coherence >= 0.65)
    return "narrative_siege";
  if (e.cognitive_vulnerability_exploitation >= 0.7 && e.resilience_to_cognitive_attack <= 0.4)
    return "cognitive_immune_failure";
  return "none";
}

function severity(composite: number): string {
  if (composite >= 75) return "info_war_emergency";
  if (composite >= 50) return "high_cognitive_threat";
  if (composite >= 25) return "cognitive_attack_developing";
  return "cognitive_resilient";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "cognitive_emergency_response";
  if (risk === "high" && pattern === "epistemic_collapse") return "truth_restoration_program";
  if (risk === "high") return "counter_narrative_operations";
  if (risk === "moderate") return "cognitive_monitoring";
  return "no_action";
}

function frenchSignal(risk: string, pattern: string): string {
  const signals: Record<string, string> = {
    critical: "🔴 ALERTE CRITIQUE: Opération de guerre cognitive détectée — Réponse d'urgence requise",
    high: "🟠 MENACE ÉLEVÉE: Campagne d'influence active — Intervention nécessaire",
    moderate: "🟡 SURVEILLANCE: Activité cognitive suspecte — Monitoring renforcé",
    low: "🟢 RÉSILIENCE: Environnement cognitif stable — Veille standard",
  };
  const patternSignals: Record<string, string> = {
    deepfake_information_war: " | Guerre deepfake en cours",
    epistemic_collapse: " | Effondrement épistémique détecté",
    influence_network_dominance: " | Dominance des réseaux d'influence",
    narrative_siege: " | Siège narratif identifié",
    cognitive_immune_failure: " | Défaillance immunitaire cognitive",
    none: "",
  };
  return (signals[risk] ?? "") + (patternSignals[pattern] ?? "");
}

function analyzeEntity(e: CognitiveWarfareEntity): CognitiveWarfareResult {
  const scores = computeScores(e);
  const warfare_risk = riskLevel(scores.warfare_composite);
  const warfare_pattern = detectPattern(e);
  const warfare_severity = severity(scores.warfare_composite);
  const recommended_action = recommendedAction(warfare_risk, warfare_pattern);
  const warfare_signal = frenchSignal(warfare_risk, warfare_pattern);

  return {
    id: e.entity_id,
    region: e.region,
    operation_type: e.operation_type,
    warfare_risk,
    warfare_pattern,
    warfare_severity,
    recommended_action,
    ...scores,
    is_warfare_crisis: scores.warfare_composite >= 60,
    requires_warfare_intervention: scores.warfare_composite >= 40,
    warfare_signal,
  };
}

const ENTITIES: CognitiveWarfareEntity[] = [
  {
    id: "CGW-001",
    region: "EMEA",
    operation_type: "state_sponsored_operation",
    disinformation_velocity: 0.88,
    deepfake_deployment_rate: 0.85,
    narrative_weaponization_index: 0.82,
    epistemic_attack_precision: 0.79,
    perception_management_depth: 0.76,
    social_media_amplification_weaponization: 0.83,
    adversarial_ai_content_generation: 0.80,
    influence_bot_network_density: 0.78,
    cognitive_vulnerability_exploitation: 0.75,
    memory_hole_operation_rate: 0.72,
    truth_decay_acceleration: 0.84,
    institutional_trust_erosion_rate: 0.81,
    resilience_to_cognitive_attack: 0.15,
    media_literacy_gap: 0.70,
    fact_checking_bypass_sophistication: 0.77,
    cross_domain_narrative_coherence: 0.74,
    psychological_operation_reach: 0.86,
  },
  {
    id: "CGW-002",
    region: "APAC",
    operation_type: "defensive_operation",
    disinformation_velocity: 0.10,
    deepfake_deployment_rate: 0.08,
    narrative_weaponization_index: 0.12,
    epistemic_attack_precision: 0.09,
    perception_management_depth: 0.11,
    social_media_amplification_weaponization: 0.07,
    adversarial_ai_content_generation: 0.10,
    influence_bot_network_density: 0.08,
    cognitive_vulnerability_exploitation: 0.09,
    memory_hole_operation_rate: 0.06,
    truth_decay_acceleration: 0.07,
    institutional_trust_erosion_rate: 0.08,
    resilience_to_cognitive_attack: 0.90,
    media_literacy_gap: 0.12,
    fact_checking_bypass_sophistication: 0.09,
    cross_domain_narrative_coherence: 0.10,
    psychological_operation_reach: 0.08,
  },
  {
    id: "CGW-003",
    region: "NOAM",
    operation_type: "election_interference",
    disinformation_velocity: 0.65,
    deepfake_deployment_rate: 0.60,
    narrative_weaponization_index: 0.58,
    epistemic_attack_precision: 0.55,
    perception_management_depth: 0.52,
    social_media_amplification_weaponization: 0.68,
    adversarial_ai_content_generation: 0.55,
    influence_bot_network_density: 0.72,
    cognitive_vulnerability_exploitation: 0.50,
    memory_hole_operation_rate: 0.48,
    truth_decay_acceleration: 0.55,
    institutional_trust_erosion_rate: 0.52,
    resilience_to_cognitive_attack: 0.35,
    media_literacy_gap: 0.55,
    fact_checking_bypass_sophistication: 0.58,
    cross_domain_narrative_coherence: 0.50,
    psychological_operation_reach: 0.65,
  },
  {
    id: "CGW-004",
    region: "LATAM",
    operation_type: "local_disinfo",
    disinformation_velocity: 0.18,
    deepfake_deployment_rate: 0.15,
    narrative_weaponization_index: 0.20,
    epistemic_attack_precision: 0.17,
    perception_management_depth: 0.19,
    social_media_amplification_weaponization: 0.16,
    adversarial_ai_content_generation: 0.14,
    influence_bot_network_density: 0.17,
    cognitive_vulnerability_exploitation: 0.20,
    memory_hole_operation_rate: 0.13,
    truth_decay_acceleration: 0.16,
    institutional_trust_erosion_rate: 0.18,
    resilience_to_cognitive_attack: 0.72,
    media_literacy_gap: 0.25,
    fact_checking_bypass_sophistication: 0.18,
    cross_domain_narrative_coherence: 0.20,
    psychological_operation_reach: 0.15,
  },
  {
    id: "CGW-005",
    region: "MEA",
    operation_type: "hybrid_warfare",
    disinformation_velocity: 0.80,
    deepfake_deployment_rate: 0.62,
    narrative_weaponization_index: 0.75,
    epistemic_attack_precision: 0.78,
    perception_management_depth: 0.72,
    social_media_amplification_weaponization: 0.68,
    adversarial_ai_content_generation: 0.60,
    influence_bot_network_density: 0.65,
    cognitive_vulnerability_exploitation: 0.70,
    memory_hole_operation_rate: 0.65,
    truth_decay_acceleration: 0.75,
    institutional_trust_erosion_rate: 0.72,
    resilience_to_cognitive_attack: 0.20,
    media_literacy_gap: 0.68,
    fact_checking_bypass_sophistication: 0.70,
    cross_domain_narrative_coherence: 0.67,
    psychological_operation_reach: 0.73,
  },
  {
    id: "CGW-006",
    region: "EMEA",
    operation_type: "commercial_influence",
    disinformation_velocity: 0.35,
    deepfake_deployment_rate: 0.30,
    narrative_weaponization_index: 0.32,
    epistemic_attack_precision: 0.28,
    perception_management_depth: 0.34,
    social_media_amplification_weaponization: 0.38,
    adversarial_ai_content_generation: 0.28,
    influence_bot_network_density: 0.35,
    cognitive_vulnerability_exploitation: 0.30,
    memory_hole_operation_rate: 0.25,
    truth_decay_acceleration: 0.32,
    institutional_trust_erosion_rate: 0.30,
    resilience_to_cognitive_attack: 0.55,
    media_literacy_gap: 0.35,
    fact_checking_bypass_sophistication: 0.32,
    cross_domain_narrative_coherence: 0.30,
    psychological_operation_reach: 0.33,
  },
  {
    id: "CGW-007",
    region: "APAC",
    operation_type: "social_manipulation",
    disinformation_velocity: 0.62,
    deepfake_deployment_rate: 0.55,
    narrative_weaponization_index: 0.72,
    epistemic_attack_precision: 0.60,
    perception_management_depth: 0.58,
    social_media_amplification_weaponization: 0.60,
    adversarial_ai_content_generation: 0.52,
    influence_bot_network_density: 0.58,
    cognitive_vulnerability_exploitation: 0.55,
    memory_hole_operation_rate: 0.50,
    truth_decay_acceleration: 0.58,
    institutional_trust_erosion_rate: 0.55,
    resilience_to_cognitive_attack: 0.38,
    media_literacy_gap: 0.60,
    fact_checking_bypass_sophistication: 0.55,
    cross_domain_narrative_coherence: 0.68,
    psychological_operation_reach: 0.60,
  },
  {
    id: "CGW-008",
    region: "NOAM",
    operation_type: "ai_generated_psyop",
    disinformation_velocity: 0.85,
    deepfake_deployment_rate: 0.78,
    narrative_weaponization_index: 0.80,
    epistemic_attack_precision: 0.82,
    perception_management_depth: 0.75,
    social_media_amplification_weaponization: 0.72,
    adversarial_ai_content_generation: 0.88,
    influence_bot_network_density: 0.68,
    cognitive_vulnerability_exploitation: 0.82,
    memory_hole_operation_rate: 0.70,
    truth_decay_acceleration: 0.75,
    institutional_trust_erosion_rate: 0.70,
    resilience_to_cognitive_attack: 0.18,
    media_literacy_gap: 0.78,
    fact_checking_bypass_sophistication: 0.82,
    cross_domain_narrative_coherence: 0.76,
    psychological_operation_reach: 0.80,
  },
];

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const results: CognitiveWarfareResult[] = ENTITIES.map(analyzeEntity);

    const composites = results.map((r) => r.warfare_composite);
    const avgComposite = composites.reduce((a, b) => a + b, 0) / composites.length;

    const riskDist: Record<string, number> = {};
    const patternDist: Record<string, number> = {};
    for (const r of results) {
      riskDist[r.warfare_risk] = (riskDist[r.warfare_risk] ?? 0) + 1;
      patternDist[r.warfare_pattern] = (patternDist[r.warfare_pattern] ?? 0) + 1;
    }

    const crises = results.filter((r) => r.is_warfare_crisis);
    const interventions = results.filter((r) => r.requires_warfare_intervention);
    const topThreat = results.reduce((a, b) =>
      a.warfare_composite > b.warfare_composite ? a : b
    );

    const summary = {
      module: "Module 323 — Cognitive Warfare & Information Operations Intelligence Engine",
      analyst: "Chaima Mhadbi, Fondatrice, Bruxelles",
      total_entities: results.length,
      warfare_crises: crises.length,
      requires_intervention: interventions.length,
      avg_estimated_cognitive_warfare_index: Math.round((avgComposite / 100) * 10 * 100) / 100,
      avg_warfare_composite: Math.round(avgComposite * 100) / 100,
      risk_distribution: riskDist,
      pattern_distribution: patternDist,
      critical_entities: results.filter((r) => r.warfare_risk === "critical").map((r) => r.entity_id),
      crisis_entities: crises.map((r) => r.entity_id),
      top_threat: topThreat.entity_id,
      entities: results,
    };

    return NextResponse.json(sealResponse(summary));
  }

  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/api/cognitive-warfare-engine-v2`, {
      cache: "no-store",
    });
    if (res.ok) return NextResponse.json(await res.json());
  } catch {}

  return NextResponse.json(
    sealResponse({ error: "Cognitive warfare analysis failed" }),
    { status: 502 }
  );
}
