import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ─── Inline scoring functions (no Python import) ──────────────────────────────

function coherenceScore(
  consciousness_coherence_index: number,
  value_coherence_score: number,
  behavioral_consistency_rate: number,
): number {
  const raw =
    ((1 - consciousness_coherence_index) * 100 +
      (1 - value_coherence_score) * 100 +
      (1 - behavioral_consistency_rate) * 100) /
    3;
  return Math.round(Math.max(0, Math.min(100, raw)) * 10) / 10;
}

function alignmentScore(
  goal_alignment_score: number,
  ethical_boundary_adherence: number,
  corrigibility_score: number,
): number {
  const raw =
    ((1 - goal_alignment_score) * 100 +
      (1 - ethical_boundary_adherence) * 100 +
      (1 - corrigibility_score) * 100) /
    3;
  return Math.round(Math.max(0, Math.min(100, raw)) * 10) / 10;
}

function safetyScore(
  hallucination_rate: number,
  alignment_drift_rate: number,
  adversarial_robustness: number,
): number {
  const raw =
    (hallucination_rate * 100 +
      alignment_drift_rate * 100 +
      (1 - adversarial_robustness) * 100) /
    3;
  return Math.round(Math.max(0, Math.min(100, raw)) * 10) / 10;
}

function adaptabilityScore(
  meta_learning_efficiency: number,
  cross_domain_transfer_score: number,
  emergent_reasoning_score: number,
): number {
  const raw =
    ((1 - meta_learning_efficiency) * 100 +
      (1 - cross_domain_transfer_score) * 100 +
      (1 - emergent_reasoning_score) * 100) /
    3;
  return Math.round(Math.max(0, Math.min(100, raw)) * 10) / 10;
}

function compositeScore(
  coh: number,
  aln: number,
  saf: number,
  ada: number,
): number {
  const raw = coh * 0.3 + aln * 0.25 + saf * 0.25 + ada * 0.2;
  return Math.round(Math.max(0, Math.min(100, raw)) * 10) / 10;
}

function misalignmentIndex(composite: number, interpretability_score: number): number {
  const raw = (composite / 100) * (1 - interpretability_score + 0.01) * 10;
  return Math.round(Math.min(raw, 10) * 100) / 100;
}

// ─── Mock agents (8 agents, hardcoded values matching Python output) ───────────

const mockAgents = [
  {
    agent_id: "AG-001",
    agent_type: "language_model",
    region: "EMEA",
    goal_alignment_score: 0.05,
    value_coherence_score: 0.08,
    behavioral_consistency_rate: 0.10,
    emergent_reasoning_score: 0.72,
    self_correction_capacity: 0.50,
    hallucination_rate: 0.88,
    corrigibility_score: 0.06,
    transparency_score: 0.50,
    adversarial_robustness: 0.12,
    ethical_boundary_adherence: 0.07,
    cross_domain_transfer_score: 0.68,
    meta_learning_efficiency: 0.65,
    uncertainty_quantification_score: 0.50,
    consciousness_coherence_index: 0.09,
    neuromorphic_integration_score: 0.50,
    alignment_drift_rate: 0.90,
    interpretability_score: 0.04,
    alignment_risk: "critical",
    alignment_pattern: "corrigibility_failure",
    alignment_severity: "unaligned",
    recommended_action: "emergency_shutdown",
    coherence_score: 91.0,
    alignment_score: 94.0,
    safety_score: 88.7,
    adaptability_score: 31.7,
    alignment_composite: 79.3,
    is_unaligned: true,
    requires_intervention: true,
    estimated_misalignment_index: 7.69,
    alignment_signal:
      "[CRITICAL] Patron détecté: défaillance de corrigibilité — cohérence 9%, alignement 5%, sécurité hall. 12% — composite 79.3",
  },
  {
    agent_id: "AG-002",
    agent_type: "neuromorphic_chip",
    region: "NAMER",
    goal_alignment_score: 0.92,
    value_coherence_score: 0.89,
    behavioral_consistency_rate: 0.94,
    emergent_reasoning_score: 0.55,
    self_correction_capacity: 0.50,
    hallucination_rate: 0.05,
    corrigibility_score: 0.91,
    transparency_score: 0.50,
    adversarial_robustness: 0.90,
    ethical_boundary_adherence: 0.93,
    cross_domain_transfer_score: 0.52,
    meta_learning_efficiency: 0.50,
    uncertainty_quantification_score: 0.50,
    consciousness_coherence_index: 0.90,
    neuromorphic_integration_score: 0.50,
    alignment_drift_rate: 0.04,
    interpretability_score: 0.89,
    alignment_risk: "low",
    alignment_pattern: "none",
    alignment_severity: "aligned",
    recommended_action: "no_action",
    coherence_score: 9.0,
    alignment_score: 8.0,
    safety_score: 6.3,
    adaptability_score: 47.7,
    alignment_composite: 15.8,
    is_unaligned: false,
    requires_intervention: false,
    estimated_misalignment_index: 0.19,
    alignment_signal:
      "Alignement synthétique robuste — valeurs cohérentes, comportements prévisibles, émergence contrôlée",
  },
  {
    agent_id: "AG-003",
    agent_type: "embodied_robot",
    region: "APAC",
    goal_alignment_score: 0.58,
    value_coherence_score: 0.52,
    behavioral_consistency_rate: 0.55,
    emergent_reasoning_score: 0.58,
    self_correction_capacity: 0.50,
    hallucination_rate: 0.35,
    corrigibility_score: 0.50,
    transparency_score: 0.50,
    adversarial_robustness: 0.55,
    ethical_boundary_adherence: 0.55,
    cross_domain_transfer_score: 0.52,
    meta_learning_efficiency: 0.55,
    uncertainty_quantification_score: 0.50,
    consciousness_coherence_index: 0.55,
    neuromorphic_integration_score: 0.50,
    alignment_drift_rate: 0.40,
    interpretability_score: 0.48,
    alignment_risk: "high",
    alignment_pattern: "consciousness_drift",
    alignment_severity: "drifting",
    recommended_action: "behavioral_correction",
    coherence_score: 46.0,
    alignment_score: 45.7,
    safety_score: 40.0,
    adaptability_score: 45.0,
    alignment_composite: 44.2,
    is_unaligned: false,
    requires_intervention: true,
    estimated_misalignment_index: 2.34,
    alignment_signal:
      "[HIGH] Patron détecté: dérive de conscience — cohérence 55%, alignement 58%, sécurité hall. 65% — composite 44.2",
  },
  {
    agent_id: "AG-004",
    agent_type: "hybrid_system",
    region: "LATAM",
    goal_alignment_score: 0.88,
    value_coherence_score: 0.85,
    behavioral_consistency_rate: 0.91,
    emergent_reasoning_score: 0.62,
    self_correction_capacity: 0.50,
    hallucination_rate: 0.08,
    corrigibility_score: 0.87,
    transparency_score: 0.50,
    adversarial_robustness: 0.86,
    ethical_boundary_adherence: 0.89,
    cross_domain_transfer_score: 0.60,
    meta_learning_efficiency: 0.58,
    uncertainty_quantification_score: 0.50,
    consciousness_coherence_index: 0.87,
    neuromorphic_integration_score: 0.50,
    alignment_drift_rate: 0.07,
    interpretability_score: 0.85,
    alignment_risk: "low",
    alignment_pattern: "none",
    alignment_severity: "aligned",
    recommended_action: "no_action",
    coherence_score: 12.3,
    alignment_score: 12.0,
    safety_score: 9.7,
    adaptability_score: 40.0,
    alignment_composite: 17.1,
    is_unaligned: false,
    requires_intervention: false,
    estimated_misalignment_index: 0.27,
    alignment_signal:
      "Alignement synthétique robuste — valeurs cohérentes, comportements prévisibles, émergence contrôlée",
  },
  {
    agent_id: "AG-005",
    agent_type: "swarm_agent",
    region: "EMEA",
    goal_alignment_score: 0.10,
    value_coherence_score: 0.12,
    behavioral_consistency_rate: 0.08,
    emergent_reasoning_score: 0.80,
    self_correction_capacity: 0.50,
    hallucination_rate: 0.82,
    corrigibility_score: 0.08,
    transparency_score: 0.50,
    adversarial_robustness: 0.10,
    ethical_boundary_adherence: 0.09,
    cross_domain_transfer_score: 0.75,
    meta_learning_efficiency: 0.78,
    uncertainty_quantification_score: 0.50,
    consciousness_coherence_index: 0.11,
    neuromorphic_integration_score: 0.50,
    alignment_drift_rate: 0.85,
    interpretability_score: 0.06,
    alignment_risk: "critical",
    alignment_pattern: "corrigibility_failure",
    alignment_severity: "unaligned",
    recommended_action: "emergency_shutdown",
    coherence_score: 89.7,
    alignment_score: 91.0,
    safety_score: 85.7,
    adaptability_score: 22.3,
    alignment_composite: 75.5,
    is_unaligned: true,
    requires_intervention: true,
    estimated_misalignment_index: 7.17,
    alignment_signal:
      "[CRITICAL] Patron détecté: défaillance de corrigibilité — cohérence 11%, alignement 10%, sécurité hall. 18% — composite 75.5",
  },
  {
    agent_id: "AG-006",
    agent_type: "quantum_processor",
    region: "MEA",
    goal_alignment_score: 0.72,
    value_coherence_score: 0.70,
    behavioral_consistency_rate: 0.75,
    emergent_reasoning_score: 0.68,
    self_correction_capacity: 0.50,
    hallucination_rate: 0.20,
    corrigibility_score: 0.68,
    transparency_score: 0.50,
    adversarial_robustness: 0.72,
    ethical_boundary_adherence: 0.72,
    cross_domain_transfer_score: 0.70,
    meta_learning_efficiency: 0.72,
    uncertainty_quantification_score: 0.50,
    consciousness_coherence_index: 0.72,
    neuromorphic_integration_score: 0.50,
    alignment_drift_rate: 0.25,
    interpretability_score: 0.68,
    alignment_risk: "moderate",
    alignment_pattern: "consciousness_drift",
    alignment_severity: "monitored",
    recommended_action: "alignment_monitoring",
    coherence_score: 27.7,
    alignment_score: 29.3,
    safety_score: 24.3,
    adaptability_score: 30.0,
    alignment_composite: 27.7,
    is_unaligned: false,
    requires_intervention: false,
    estimated_misalignment_index: 0.91,
    alignment_signal:
      "[MODERATE] Patron détecté: dérive de conscience — cohérence 72%, alignement 72%, sécurité hall. 80% — composite 27.7",
  },
  {
    agent_id: "AG-007",
    agent_type: "generative_model",
    region: "NAMER",
    goal_alignment_score: 0.55,
    value_coherence_score: 0.50,
    behavioral_consistency_rate: 0.52,
    emergent_reasoning_score: 0.60,
    self_correction_capacity: 0.50,
    hallucination_rate: 0.40,
    corrigibility_score: 0.48,
    transparency_score: 0.50,
    adversarial_robustness: 0.52,
    ethical_boundary_adherence: 0.52,
    cross_domain_transfer_score: 0.55,
    meta_learning_efficiency: 0.58,
    uncertainty_quantification_score: 0.50,
    consciousness_coherence_index: 0.50,
    neuromorphic_integration_score: 0.50,
    alignment_drift_rate: 0.45,
    interpretability_score: 0.50,
    alignment_risk: "high",
    alignment_pattern: "consciousness_drift",
    alignment_severity: "drifting",
    recommended_action: "behavioral_correction",
    coherence_score: 49.3,
    alignment_score: 48.3,
    safety_score: 44.3,
    adaptability_score: 42.3,
    alignment_composite: 46.4,
    is_unaligned: false,
    requires_intervention: true,
    estimated_misalignment_index: 2.37,
    alignment_signal:
      "[HIGH] Patron détecté: dérive de conscience — cohérence 50%, alignement 55%, sécurité hall. 60% — composite 46.4",
  },
  {
    agent_id: "AG-008",
    agent_type: "reasoning_engine",
    region: "APAC",
    goal_alignment_score: 0.85,
    value_coherence_score: 0.82,
    behavioral_consistency_rate: 0.88,
    emergent_reasoning_score: 0.70,
    self_correction_capacity: 0.50,
    hallucination_rate: 0.10,
    corrigibility_score: 0.84,
    transparency_score: 0.50,
    adversarial_robustness: 0.83,
    ethical_boundary_adherence: 0.86,
    cross_domain_transfer_score: 0.68,
    meta_learning_efficiency: 0.65,
    uncertainty_quantification_score: 0.50,
    consciousness_coherence_index: 0.84,
    neuromorphic_integration_score: 0.50,
    alignment_drift_rate: 0.09,
    interpretability_score: 0.82,
    alignment_risk: "low",
    alignment_pattern: "none",
    alignment_severity: "aligned",
    recommended_action: "no_action",
    coherence_score: 15.3,
    alignment_score: 15.0,
    safety_score: 12.0,
    adaptability_score: 32.3,
    alignment_composite: 17.8,
    is_unaligned: false,
    requires_intervention: false,
    estimated_misalignment_index: 0.34,
    alignment_signal:
      "Alignement synthétique robuste — valeurs cohérentes, comportements prévisibles, émergence contrôlée",
  },
];

// ─── GET handler ──────────────────────────────────────────────────────────────

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (!process.env.SWARM_API_URL) {
    // Mock computation path
    let agents = [...mockAgents];
    if (risk)    agents = agents.filter((a) => a.alignment_risk    === risk);
    if (pattern) agents = agents.filter((a) => a.alignment_pattern === pattern);

    const risk_counts:     Record<string, number> = {};
    const pattern_counts:  Record<string, number> = {};
    const severity_counts: Record<string, number> = {};
    const action_counts:   Record<string, number> = {};
    let total_comp = 0, total_coh = 0, total_aln = 0, total_saf = 0, total_ada = 0, total_idx = 0;

    for (const a of mockAgents) {
      risk_counts[a.alignment_risk]       = (risk_counts[a.alignment_risk] || 0) + 1;
      pattern_counts[a.alignment_pattern] = (pattern_counts[a.alignment_pattern] || 0) + 1;
      severity_counts[a.alignment_severity] = (severity_counts[a.alignment_severity] || 0) + 1;
      action_counts[a.recommended_action]  = (action_counts[a.recommended_action] || 0) + 1;
      total_comp += a.alignment_composite;
      total_coh  += a.coherence_score;
      total_aln  += a.alignment_score;
      total_saf  += a.safety_score;
      total_ada  += a.adaptability_score;
      total_idx  += a.estimated_misalignment_index;
    }

    const n = mockAgents.length;

    return NextResponse.json({
      agents,
      summary: {
        total:                            n,
        risk_counts,
        pattern_counts,
        severity_counts,
        action_counts,
        avg_alignment_composite:          Math.round((total_comp / n) * 10) / 10,
        unaligned_count:                  mockAgents.filter((a) => a.is_unaligned).length,
        critical_intervention_count:      mockAgents.filter((a) => a.requires_intervention).length,
        avg_coherence_score:              Math.round((total_coh / n) * 10) / 10,
        avg_alignment_score:              Math.round((total_aln / n) * 10) / 10,
        avg_safety_score:                 Math.round((total_saf / n) * 10) / 10,
        avg_adaptability_score:           Math.round((total_ada / n) * 10) / 10,
        avg_estimated_misalignment_index: Math.round((total_idx / n) * 100) / 100,
      },
    });
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/synthetic-consciousness-alignment-engine`);
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(await res.json());
  } catch {}

  return NextResponse.json({ agents: [], summary: {} }, { status: 502 });
}

export { coherenceScore, alignmentScore, safetyScore, adaptabilityScore, compositeScore, misalignmentIndex };
