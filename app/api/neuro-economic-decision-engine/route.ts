import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // NED-001 — EMEA, financial_markets → critical, cognitive_overload
  { entity_id:"NED-001", decision_domain:"financial_markets", region:"EMEA",
    cognitive_load:0.88, loss_aversion_bias:0.72, anchoring_effect:0.65,
    framing_susceptibility:0.70, sunk_cost_fallacy:0.68, hyperbolic_discounting:0.75,
    overconfidence_index:0.60, herding_tendency:0.55, attention_scarcity:0.82,
    emotional_override:0.65, decision_fatigue:0.78, information_asymmetry:0.72,
    choice_paralysis:0.60, recency_bias:0.70, rational_override_capacity:0.20,
    metacognitive_awareness:0.18, decision_coherence:0.15 },

  // NED-002 — APAC, investment → low, rational_clarity/none
  { entity_id:"NED-002", decision_domain:"investment", region:"APAC",
    cognitive_load:0.15, loss_aversion_bias:0.12, anchoring_effect:0.10,
    framing_susceptibility:0.14, sunk_cost_fallacy:0.12, hyperbolic_discounting:0.10,
    overconfidence_index:0.12, herding_tendency:0.10, attention_scarcity:0.12,
    emotional_override:0.10, decision_fatigue:0.12, information_asymmetry:0.15,
    choice_paralysis:0.10, recency_bias:0.12, rational_override_capacity:0.92,
    metacognitive_awareness:0.90, decision_coherence:0.92 },

  // NED-003 — NOAM, strategic_planning → high, bias_cascade
  { entity_id:"NED-003", decision_domain:"strategic_planning", region:"NOAM",
    cognitive_load:0.52, loss_aversion_bias:0.78, anchoring_effect:0.72,
    framing_susceptibility:0.60, sunk_cost_fallacy:0.65, hyperbolic_discounting:0.48,
    overconfidence_index:0.75, herding_tendency:0.42, attention_scarcity:0.50,
    emotional_override:0.48, decision_fatigue:0.52, information_asymmetry:0.55,
    choice_paralysis:0.45, recency_bias:0.62, rational_override_capacity:0.40,
    metacognitive_awareness:0.38, decision_coherence:0.42 },

  // NED-004 — LATAM, investment → low, rational_clarity/none
  { entity_id:"NED-004", decision_domain:"investment", region:"LATAM",
    cognitive_load:0.18, loss_aversion_bias:0.15, anchoring_effect:0.12,
    framing_susceptibility:0.16, sunk_cost_fallacy:0.14, hyperbolic_discounting:0.12,
    overconfidence_index:0.15, herding_tendency:0.12, attention_scarcity:0.18,
    emotional_override:0.14, decision_fatigue:0.15, information_asymmetry:0.18,
    choice_paralysis:0.12, recency_bias:0.15, rational_override_capacity:0.88,
    metacognitive_awareness:0.86, decision_coherence:0.90 },

  // NED-005 — MEA, financial_markets → critical, emotional_hijack
  { entity_id:"NED-005", decision_domain:"financial_markets", region:"MEA",
    cognitive_load:0.60, loss_aversion_bias:0.65, anchoring_effect:0.58,
    framing_susceptibility:0.62, sunk_cost_fallacy:0.70, hyperbolic_discounting:0.80,
    overconfidence_index:0.55, herding_tendency:0.62, attention_scarcity:0.58,
    emotional_override:0.85, decision_fatigue:0.72, information_asymmetry:0.65,
    choice_paralysis:0.58, recency_bias:0.68, rational_override_capacity:0.22,
    metacognitive_awareness:0.25, decision_coherence:0.20 },

  // NED-006 — EMEA, risk_assessment → moderate, none
  { entity_id:"NED-006", decision_domain:"risk_assessment", region:"EMEA",
    cognitive_load:0.38, loss_aversion_bias:0.35, anchoring_effect:0.32,
    framing_susceptibility:0.38, sunk_cost_fallacy:0.35, hyperbolic_discounting:0.32,
    overconfidence_index:0.30, herding_tendency:0.35, attention_scarcity:0.35,
    emotional_override:0.38, decision_fatigue:0.35, information_asymmetry:0.40,
    choice_paralysis:0.32, recency_bias:0.38, rational_override_capacity:0.62,
    metacognitive_awareness:0.60, decision_coherence:0.58 },

  // NED-007 — APAC, strategic_planning → high, decision_paralysis
  { entity_id:"NED-007", decision_domain:"strategic_planning", region:"APAC",
    cognitive_load:0.55, loss_aversion_bias:0.50, anchoring_effect:0.45,
    framing_susceptibility:0.52, sunk_cost_fallacy:0.48, hyperbolic_discounting:0.50,
    overconfidence_index:0.42, herding_tendency:0.48, attention_scarcity:0.52,
    emotional_override:0.50, decision_fatigue:0.55, information_asymmetry:0.72,
    choice_paralysis:0.82, recency_bias:0.48, rational_override_capacity:0.38,
    metacognitive_awareness:0.40, decision_coherence:0.35 },

  // NED-008 — NOAM, financial_markets → critical, herding_collapse
  { entity_id:"NED-008", decision_domain:"financial_markets", region:"NOAM",
    cognitive_load:0.65, loss_aversion_bias:0.60, anchoring_effect:0.58,
    framing_susceptibility:0.65, sunk_cost_fallacy:0.72, hyperbolic_discounting:0.82,
    overconfidence_index:0.58, herding_tendency:0.88, attention_scarcity:0.58,
    emotional_override:0.65, decision_fatigue:0.75, information_asymmetry:0.55,
    choice_paralysis:0.55, recency_bias:0.72, rational_override_capacity:0.22,
    metacognitive_awareness:0.18, decision_coherence:0.20 },
];

type Entity = typeof MOCK_ENTITIES[0];

function cognitiveScore(e: Entity): number {
  const raw = (e.cognitive_load * 0.35 + e.attention_scarcity * 0.35 + e.decision_fatigue * 0.30) * 100;
  return Math.round(raw * 100) / 100;
}
function biasScore(e: Entity): number {
  const raw = (e.loss_aversion_bias * 0.25 + e.anchoring_effect * 0.20 + e.framing_susceptibility * 0.20 + e.overconfidence_index * 0.20 + e.recency_bias * 0.15) * 100;
  return Math.round(raw * 100) / 100;
}
function fatigueScore(e: Entity): number {
  const raw = (e.emotional_override * 0.35 + e.herding_tendency * 0.30 + e.hyperbolic_discounting * 0.35) * 100;
  return Math.round(raw * 100) / 100;
}
function coherenceScore(e: Entity): number {
  const raw = ((1 - e.decision_coherence) * 0.4 + (1 - e.rational_override_capacity) * 0.3 + (1 - e.metacognitive_awareness) * 0.3) * 100;
  return Math.round(raw * 100) / 100;
}
function decisionComposite(cog: number, bias: number, fat: number, coh: number): number {
  return Math.round((cog * 0.30 + bias * 0.25 + fat * 0.25 + coh * 0.20) * 100) / 100;
}
function decisionPattern(e: Entity): string {
  if (e.cognitive_load >= 0.70 && e.attention_scarcity >= 0.60) return "cognitive_overload";
  if ((e.loss_aversion_bias + e.anchoring_effect + e.overconfidence_index) / 3 >= 0.65) return "bias_cascade";
  if (e.emotional_override >= 0.70 && (1 - e.rational_override_capacity) >= 0.60) return "emotional_hijack";
  if (e.choice_paralysis >= 0.70 && e.information_asymmetry >= 0.60) return "decision_paralysis";
  if (e.herding_tendency >= 0.70 && (1 - e.metacognitive_awareness) >= 0.60) return "herding_collapse";
  return "none";
}
function decisionRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}
function decisionSeverity(comp: number): string {
  if (comp >= 75) return "severely_impaired";
  if (comp >= 50) return "high_distortion";
  if (comp >= 25) return "moderate_bias";
  return "rational_clarity";
}
function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "decision_architecture_reset";
  if (risk === "high" && pattern === "bias_cascade") return "debiasing_protocol";
  if (risk === "high") return "cognitive_augmentation";
  if (risk === "moderate") return "decision_monitoring";
  return "no_action";
}
function decisionSignal(e: Entity, biasScoreVal: number, comp: number, risk: string): string {
  if (risk === "critical") {
    return `Critique — charge cognitive ${Math.round(e.cognitive_load * 100)}% — biais composite ${Math.round(biasScoreVal)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "high") {
    return `Élevé — surcharge émotionnelle ${Math.round(e.emotional_override * 100)}% — cohérence décisionnelle ${Math.round(e.decision_coherence * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "moderate") {
    return `Modéré — biais d'ancrage ${Math.round(e.anchoring_effect * 100)}% — composite ${Math.round(comp)}`;
  }
  return "Architecture décisionnelle optimale — biais contenus, clarté cognitive élevée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const cog  = cognitiveScore(e);
      const bias = biasScore(e);
      const fat  = fatigueScore(e);
      const coh  = coherenceScore(e);
      const comp = decisionComposite(cog, bias, fat, coh);
      const pat  = decisionPattern(e);
      const risk = decisionRisk(comp);
      const sev  = decisionSeverity(comp);
      const act  = recommendedAction(risk, pat);
      return {
        entity_id:                          e.entity_id,
        region:                             e.region,
        decision_domain:                    e.decision_domain,
        decision_risk:                      risk,
        decision_pattern:                   pat,
        decision_severity:                  sev,
        recommended_action:                 act,
        cognitive_score:                    cog,
        bias_score:                         bias,
        fatigue_score:                      fat,
        coherence_score:                    coh,
        decision_composite:                 comp,
        is_in_decision_crisis:              comp >= 60,
        requires_architecture_intervention: comp >= 40,
        decision_signal:                    decisionSignal(e, bias, comp, risk),
      };
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tComp=0, tCog=0, tBias=0, tFat=0, tCoh=0, crisisC=0, intervC=0;
    for (const ent of entities) {
      rc[ent.decision_risk]       = (rc[ent.decision_risk]       || 0) + 1;
      pc[ent.decision_pattern]    = (pc[ent.decision_pattern]    || 0) + 1;
      sc[ent.decision_severity]   = (sc[ent.decision_severity]   || 0) + 1;
      ac[ent.recommended_action]  = (ac[ent.recommended_action]  || 0) + 1;
      tComp += ent.decision_composite;
      tCog  += ent.cognitive_score;
      tBias += ent.bias_score;
      tFat  += ent.fatigue_score;
      tCoh  += ent.coherence_score;
      if (ent.is_in_decision_crisis)              crisisC++;
      if (ent.requires_architecture_intervention) intervC++;
    }
    const n = entities.length;
    const avgComp = tComp / n;
    const summary = {
      total:                               n,
      risk_counts:                         rc,
      pattern_counts:                      pc,
      severity_counts:                     sc,
      action_counts:                       ac,
      avg_decision_composite:              Math.round(avgComp * 10) / 10,
      decision_crisis_count:               crisisC,
      architecture_intervention_count:     intervC,
      avg_cognitive_score:                 Math.round(tCog  / n * 10) / 10,
      avg_bias_score:                      Math.round(tBias / n * 10) / 10,
      avg_fatigue_score:                   Math.round(tFat  / n * 10) / 10,
      avg_coherence_score:                 Math.round(tCoh  / n * 10) / 10,
      avg_estimated_decision_risk_index:   Math.round(avgComp / 100 * 10 * 100) / 100,
    };
    return NextResponse.json(sealResponse({ entities, summary }, "neuro-economic-decision-engine"));
  }
  return NextResponse.json(sealResponse(
    await (await fetch(`${process.env.SWARM_API_URL}/neuro-economic-decision-engine`)).json(),
    "neuro-economic-decision-engine"
  ));
}
