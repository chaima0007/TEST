import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ─── Inline scoring functions ─────────────────────────────────────────────────

function reasoningScore(
  confirmation_bias_intensity: number,
  dunning_kruger_index: number,
  overconfidence_calibration_gap: number,
): number {
  const raw =
    (confirmation_bias_intensity * 0.4 +
      dunning_kruger_index * 0.35 +
      overconfidence_calibration_gap * 0.25) *
    100;
  return Math.round(Math.max(0, Math.min(100, raw)) * 10) / 10;
}

function heuristicScore(
  availability_heuristic_dominance: number,
  anchoring_distortion_rate: number,
  narrative_fallacy_exposure: number,
): number {
  const raw =
    (availability_heuristic_dominance * 0.4 +
      anchoring_distortion_rate * 0.35 +
      narrative_fallacy_exposure * 0.25) *
    100;
  return Math.round(Math.max(0, Math.min(100, raw)) * 10) / 10;
}

function groupScore(
  groupthink_susceptibility: number,
  echo_chamber_intensity: number,
  status_quo_bias_strength: number,
): number {
  const raw =
    (groupthink_susceptibility * 0.4 +
      echo_chamber_intensity * 0.35 +
      status_quo_bias_strength * 0.25) *
    100;
  return Math.round(Math.max(0, Math.min(100, raw)) * 10) / 10;
}

function metaScore(
  metacognitive_accuracy: number,
  epistemic_humility_deficit: number,
  debiasing_capacity: number,
): number {
  const raw =
    ((1 - metacognitive_accuracy) * 0.4 +
      epistemic_humility_deficit * 0.35 +
      (1 - debiasing_capacity) * 0.25) *
    100;
  return Math.round(Math.max(0, Math.min(100, raw)) * 10) / 10;
}

function compositeScore(
  reasoning: number,
  heuristic: number,
  group: number,
  meta: number,
): number {
  const raw = reasoning * 0.3 + heuristic * 0.25 + group * 0.25 + meta * 0.2;
  return Math.round(Math.max(0, Math.min(100, raw)) * 10) / 10;
}

// ─── Mock entities ─────────────────────────────────────────────────────────────

const mockEntities = [
  // MCB-001: EMEA, corporate_boardroom → critical, dunning_kruger_crisis
  {
    entity_id: "MCB-001",
    decision_system_type: "corporate_boardroom",
    region: "EMEA",
    confirmation_bias_intensity: 0.80,
    dunning_kruger_index: 0.85,
    availability_heuristic_dominance: 0.70,
    anchoring_distortion_rate: 0.65,
    groupthink_susceptibility: 0.60,
    sunk_cost_fallacy_grip: 0.70,
    overconfidence_calibration_gap: 0.80,
    black_swan_blindness: 0.55,
    narrative_fallacy_exposure: 0.60,
    planning_fallacy_severity: 0.65,
    hindsight_bias_contamination: 0.55,
    status_quo_bias_strength: 0.55,
    cognitive_load_saturation: 0.70,
    metacognitive_accuracy: 0.25,
    epistemic_humility_deficit: 0.75,
    debiasing_capacity: 0.20,
    echo_chamber_intensity: 0.55,
    bias_risk: "critical",
    bias_pattern: "dunning_kruger_crisis",
    bias_severity: "high_bias_risk",
    recommended_action: "cognitive_emergency_debiasing",
    reasoning_score: 81.8,
    heuristic_score: 65.8,
    group_score: 57.0,
    meta_score: 76.2,
    bias_composite: 70.5,
    is_bias_crisis: true,
    requires_bias_intervention: true,
    bias_signal:
      "[CRITICAL] Patron détecté: crise Dunning-Kruger — raisonnement 80%, DK 85%, groupthink 60%, précision méta 25% — composite 70.5",
  },
  // MCB-002: APAC, research_team → low, none
  {
    entity_id: "MCB-002",
    decision_system_type: "research_team",
    region: "APAC",
    confirmation_bias_intensity: 0.10,
    dunning_kruger_index: 0.08,
    availability_heuristic_dominance: 0.12,
    anchoring_distortion_rate: 0.10,
    groupthink_susceptibility: 0.10,
    sunk_cost_fallacy_grip: 0.08,
    overconfidence_calibration_gap: 0.09,
    black_swan_blindness: 0.12,
    narrative_fallacy_exposure: 0.08,
    planning_fallacy_severity: 0.10,
    hindsight_bias_contamination: 0.09,
    status_quo_bias_strength: 0.10,
    cognitive_load_saturation: 0.12,
    metacognitive_accuracy: 0.88,
    epistemic_humility_deficit: 0.08,
    debiasing_capacity: 0.90,
    echo_chamber_intensity: 0.08,
    bias_risk: "low",
    bias_pattern: "none",
    bias_severity: "cognitive_clarity",
    recommended_action: "no_action",
    reasoning_score: 9.0,
    heuristic_score: 10.3,
    group_score: 9.3,
    meta_score: 10.1,
    bias_composite: 9.6,
    is_bias_crisis: false,
    requires_bias_intervention: false,
    bias_signal:
      "Cognition saine — biais maîtrisés, raisonnement calibré, métacognition fonctionnelle, humilité épistémique adéquate",
  },
  // MCB-003: NOAM, government_agency → high, groupthink_capture
  {
    entity_id: "MCB-003",
    decision_system_type: "government_agency",
    region: "NOAM",
    confirmation_bias_intensity: 0.55,
    dunning_kruger_index: 0.50,
    availability_heuristic_dominance: 0.50,
    anchoring_distortion_rate: 0.45,
    groupthink_susceptibility: 0.82,
    sunk_cost_fallacy_grip: 0.50,
    overconfidence_calibration_gap: 0.45,
    black_swan_blindness: 0.50,
    narrative_fallacy_exposure: 0.45,
    planning_fallacy_severity: 0.50,
    hindsight_bias_contamination: 0.45,
    status_quo_bias_strength: 0.50,
    cognitive_load_saturation: 0.50,
    metacognitive_accuracy: 0.45,
    epistemic_humility_deficit: 0.50,
    debiasing_capacity: 0.45,
    echo_chamber_intensity: 0.75,
    bias_risk: "high",
    bias_pattern: "groupthink_capture",
    bias_severity: "high_bias_risk",
    recommended_action: "red_team_intervention",
    reasoning_score: 50.8,
    heuristic_score: 47.0,
    group_score: 71.6,
    meta_score: 53.2,
    bias_composite: 55.5,
    is_bias_crisis: false,
    requires_bias_intervention: true,
    bias_signal:
      "[HIGH] Patron détecté: capture groupthink — raisonnement 55%, DK 50%, groupthink 82%, précision méta 45% — composite 55.5",
  },
  // MCB-004: LATAM, startup → low, none
  {
    entity_id: "MCB-004",
    decision_system_type: "startup",
    region: "LATAM",
    confirmation_bias_intensity: 0.18,
    dunning_kruger_index: 0.15,
    availability_heuristic_dominance: 0.20,
    anchoring_distortion_rate: 0.15,
    groupthink_susceptibility: 0.18,
    sunk_cost_fallacy_grip: 0.12,
    overconfidence_calibration_gap: 0.20,
    black_swan_blindness: 0.22,
    narrative_fallacy_exposure: 0.18,
    planning_fallacy_severity: 0.20,
    hindsight_bias_contamination: 0.15,
    status_quo_bias_strength: 0.18,
    cognitive_load_saturation: 0.22,
    metacognitive_accuracy: 0.82,
    epistemic_humility_deficit: 0.15,
    debiasing_capacity: 0.80,
    echo_chamber_intensity: 0.15,
    bias_risk: "low",
    bias_pattern: "none",
    bias_severity: "cognitive_clarity",
    recommended_action: "no_action",
    reasoning_score: 17.4,
    heuristic_score: 17.8,
    group_score: 17.0,
    meta_score: 17.5,
    bias_composite: 17.4,
    is_bias_crisis: false,
    requires_bias_intervention: false,
    bias_signal:
      "Cognition saine — biais maîtrisés, raisonnement calibré, métacognition fonctionnelle, humilité épistémique adéquate",
  },
  // MCB-005: MEA, intelligence_agency → critical, black_swan_blindness
  {
    entity_id: "MCB-005",
    decision_system_type: "intelligence_agency",
    region: "MEA",
    confirmation_bias_intensity: 0.60,
    dunning_kruger_index: 0.55,
    availability_heuristic_dominance: 0.70,
    anchoring_distortion_rate: 0.65,
    groupthink_susceptibility: 0.60,
    sunk_cost_fallacy_grip: 0.65,
    overconfidence_calibration_gap: 0.72,
    black_swan_blindness: 0.82,
    narrative_fallacy_exposure: 0.60,
    planning_fallacy_severity: 0.65,
    hindsight_bias_contamination: 0.60,
    status_quo_bias_strength: 0.60,
    cognitive_load_saturation: 0.68,
    metacognitive_accuracy: 0.35,
    epistemic_humility_deficit: 0.65,
    debiasing_capacity: 0.30,
    echo_chamber_intensity: 0.58,
    bias_risk: "critical",
    bias_pattern: "black_swan_blindness",
    bias_severity: "high_bias_risk",
    recommended_action: "cognitive_emergency_debiasing",
    reasoning_score: 61.3,
    heuristic_score: 65.8,
    group_score: 59.3,
    meta_score: 66.2,
    bias_composite: 62.9,
    is_bias_crisis: true,
    requires_bias_intervention: true,
    bias_signal:
      "[CRITICAL] Patron détecté: cécité cygne noir — raisonnement 60%, DK 55%, groupthink 60%, précision méta 35% — composite 62.9",
  },
  // MCB-006: EMEA, investment_committee → moderate, none
  {
    entity_id: "MCB-006",
    decision_system_type: "investment_committee",
    region: "EMEA",
    confirmation_bias_intensity: 0.35,
    dunning_kruger_index: 0.30,
    availability_heuristic_dominance: 0.32,
    anchoring_distortion_rate: 0.30,
    groupthink_susceptibility: 0.35,
    sunk_cost_fallacy_grip: 0.32,
    overconfidence_calibration_gap: 0.30,
    black_swan_blindness: 0.35,
    narrative_fallacy_exposure: 0.30,
    planning_fallacy_severity: 0.30,
    hindsight_bias_contamination: 0.28,
    status_quo_bias_strength: 0.32,
    cognitive_load_saturation: 0.35,
    metacognitive_accuracy: 0.68,
    epistemic_humility_deficit: 0.30,
    debiasing_capacity: 0.65,
    echo_chamber_intensity: 0.28,
    bias_risk: "moderate",
    bias_pattern: "none",
    bias_severity: "bias_accumulation",
    recommended_action: "bias_monitoring",
    reasoning_score: 32.0,
    heuristic_score: 30.8,
    group_score: 31.8,
    meta_score: 32.0,
    bias_composite: 31.6,
    is_bias_crisis: false,
    requires_bias_intervention: false,
    bias_signal:
      "[MODERATE] Patron détecté: biais diffus non classifié — raisonnement 35%, DK 30%, groupthink 35%, précision méta 68% — composite 31.6",
  },
  // MCB-007: APAC, media_organization → high, narrative_trap
  {
    entity_id: "MCB-007",
    decision_system_type: "media_organization",
    region: "APAC",
    confirmation_bias_intensity: 0.72,
    dunning_kruger_index: 0.50,
    availability_heuristic_dominance: 0.60,
    anchoring_distortion_rate: 0.55,
    groupthink_susceptibility: 0.55,
    sunk_cost_fallacy_grip: 0.50,
    overconfidence_calibration_gap: 0.50,
    black_swan_blindness: 0.55,
    narrative_fallacy_exposure: 0.80,
    planning_fallacy_severity: 0.55,
    hindsight_bias_contamination: 0.50,
    status_quo_bias_strength: 0.50,
    cognitive_load_saturation: 0.55,
    metacognitive_accuracy: 0.40,
    epistemic_humility_deficit: 0.55,
    debiasing_capacity: 0.38,
    echo_chamber_intensity: 0.52,
    bias_risk: "high",
    bias_pattern: "narrative_trap",
    bias_severity: "high_bias_risk",
    recommended_action: "systematic_debiasing",
    reasoning_score: 58.8,
    heuristic_score: 63.3,
    group_score: 52.7,
    meta_score: 58.8,
    bias_composite: 58.4,
    is_bias_crisis: false,
    requires_bias_intervention: true,
    bias_signal:
      "[HIGH] Patron détecté: piège narratif — raisonnement 72%, DK 50%, groupthink 55%, précision méta 40% — composite 58.4",
  },
  // MCB-008: NOAM, ai_decision_system → critical, metacognitive_collapse
  {
    entity_id: "MCB-008",
    decision_system_type: "ai_decision_system",
    region: "NOAM",
    confirmation_bias_intensity: 0.70,
    dunning_kruger_index: 0.65,
    availability_heuristic_dominance: 0.70,
    anchoring_distortion_rate: 0.65,
    groupthink_susceptibility: 0.60,
    sunk_cost_fallacy_grip: 0.65,
    overconfidence_calibration_gap: 0.55,
    black_swan_blindness: 0.65,
    narrative_fallacy_exposure: 0.65,
    planning_fallacy_severity: 0.70,
    hindsight_bias_contamination: 0.65,
    status_quo_bias_strength: 0.60,
    cognitive_load_saturation: 0.72,
    metacognitive_accuracy: 0.22,
    epistemic_humility_deficit: 0.78,
    debiasing_capacity: 0.25,
    echo_chamber_intensity: 0.60,
    bias_risk: "critical",
    bias_pattern: "metacognitive_collapse",
    bias_severity: "high_bias_risk",
    recommended_action: "cognitive_emergency_debiasing",
    reasoning_score: 64.5,
    heuristic_score: 67.0,
    group_score: 60.0,
    meta_score: 77.2,
    bias_composite: 66.5,
    is_bias_crisis: true,
    requires_bias_intervention: true,
    bias_signal:
      "[CRITICAL] Patron détecté: effondrement métacognitif — raisonnement 70%, DK 65%, groupthink 60%, précision méta 22% — composite 66.5",
  },
];

// ─── GET handler ──────────────────────────────────────────────────────────────

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (!SWARM_API_URL) {
    let entities = [...mockEntities];
    if (risk)    entities = entities.filter((e) => e.bias_risk    === risk);
    if (pattern) entities = entities.filter((e) => e.bias_pattern === pattern);

    const risk_counts:     Record<string, number> = {};
    const pattern_counts:  Record<string, number> = {};
    const severity_counts: Record<string, number> = {};
    const action_counts:   Record<string, number> = {};
    let total_comp = 0, total_reasoning = 0, total_heuristic = 0, total_group = 0, total_meta = 0;

    for (const e of mockEntities) {
      risk_counts[e.bias_risk]             = (risk_counts[e.bias_risk] || 0) + 1;
      pattern_counts[e.bias_pattern]       = (pattern_counts[e.bias_pattern] || 0) + 1;
      severity_counts[e.bias_severity]     = (severity_counts[e.bias_severity] || 0) + 1;
      action_counts[e.recommended_action]  = (action_counts[e.recommended_action] || 0) + 1;
      total_comp      += e.bias_composite;
      total_reasoning += e.reasoning_score;
      total_heuristic += e.heuristic_score;
      total_group     += e.group_score;
      total_meta      += e.meta_score;
    }

    const n           = mockEntities.length;
    const avg_comp    = Math.round((total_comp / n) * 10) / 10;

    return NextResponse.json(
      sealResponse(
        {
          entities,
          summary: {
            total: n,
            risk_counts,
            pattern_counts,
            severity_counts,
            action_counts,
            avg_bias_composite:                       avg_comp,
            bias_crisis_count:                        mockEntities.filter((e) => e.is_bias_crisis).length,
            bias_intervention_count:                  mockEntities.filter((e) => e.requires_bias_intervention).length,
            avg_reasoning_score:                      Math.round((total_reasoning / n) * 10) / 10,
            avg_heuristic_score:                      Math.round((total_heuristic / n) * 10) / 10,
            avg_group_score:                          Math.round((total_group     / n) * 10) / 10,
            avg_meta_score:                           Math.round((total_meta      / n) * 10) / 10,
            avg_estimated_cognitive_vulnerability_index: Math.round((avg_comp / 100) * 10 * 100) / 100,
          },
        } as Record<string, unknown>,
        "metacognitive-bias-engine",
      ) as Parameters<typeof NextResponse.json>[0],
    );
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/metacognitive-bias-engine`);
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok)
      return NextResponse.json(
        sealResponse(
          await res.json(),
          "metacognitive-bias-engine",
        ) as Parameters<typeof NextResponse.json>[0],
      );
  } catch {}

  return NextResponse.json(
    sealResponse(
      { entities: [], summary: {} },
      "metacognitive-bias-engine",
    ) as Parameters<typeof NextResponse.json>[0],
    { status: 502 },
  );
}

export {
  reasoningScore,
  heuristicScore,
  groupScore,
  metaScore,
  compositeScore,
};
