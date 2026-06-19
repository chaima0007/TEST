import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// PP-001: EMEA, corporate_executives → critical, identity_lock
// identity_lock: (1-values_coherence)≥0.65 => values_coherence≤0.35, identity_brand_fusion≥0.60
// critical composite ≥ 60
const MOCK_ENTITIES = [
  {
    entity_id: "PP-001", segment_type: "corporate_executives", region: "EMEA",
    values_coherence: 0.12, motivation_alignment: 0.18, cognitive_rigidity: 0.78,
    status_orientation: 0.85, risk_appetite_behavioral: 0.22, social_conformity_pressure: 0.55,
    identity_brand_fusion: 0.82, novelty_seeking: 0.20, loss_sensitivity: 0.72,
    authority_deference: 0.68, tribalism_intensity: 0.58, cognitive_dissonance_tolerance: 0.75,
    future_orientation: 0.25, hedonism_index: 0.60, autonomy_drive: 0.20,
    empathy_capacity: 0.28, reciprocity_responsiveness: 0.32,
  },
  // PP-002: APAC, digital_natives → low, behavioral_fluidity/none
  {
    entity_id: "PP-002", segment_type: "digital_natives", region: "APAC",
    values_coherence: 0.88, motivation_alignment: 0.90, cognitive_rigidity: 0.12,
    status_orientation: 0.20, risk_appetite_behavioral: 0.78, social_conformity_pressure: 0.15,
    identity_brand_fusion: 0.18, novelty_seeking: 0.85, loss_sensitivity: 0.12,
    authority_deference: 0.15, tribalism_intensity: 0.10, cognitive_dissonance_tolerance: 0.15,
    future_orientation: 0.88, hedonism_index: 0.55, autonomy_drive: 0.90,
    empathy_capacity: 0.82, reciprocity_responsiveness: 0.80,
  },
  // PP-003: NOAM, traditionalist_consumers → high, tribalism_capture
  // tribalism_capture: tribalism_intensity≥0.70, social_conformity_pressure≥0.60
  // high: composite 40–59
  {
    entity_id: "PP-003", segment_type: "traditionalist_consumers", region: "NOAM",
    values_coherence: 0.45, motivation_alignment: 0.42, cognitive_rigidity: 0.58,
    status_orientation: 0.50, risk_appetite_behavioral: 0.30, social_conformity_pressure: 0.72,
    identity_brand_fusion: 0.48, novelty_seeking: 0.32, loss_sensitivity: 0.55,
    authority_deference: 0.58, tribalism_intensity: 0.78, cognitive_dissonance_tolerance: 0.42,
    future_orientation: 0.40, hedonism_index: 0.35, autonomy_drive: 0.38,
    empathy_capacity: 0.42, reciprocity_responsiveness: 0.45,
  },
  // PP-004: LATAM, digital_natives → low, behavioral_fluidity/none
  {
    entity_id: "PP-004", segment_type: "digital_natives", region: "LATAM",
    values_coherence: 0.85, motivation_alignment: 0.88, cognitive_rigidity: 0.15,
    status_orientation: 0.25, risk_appetite_behavioral: 0.72, social_conformity_pressure: 0.18,
    identity_brand_fusion: 0.22, novelty_seeking: 0.80, loss_sensitivity: 0.15,
    authority_deference: 0.18, tribalism_intensity: 0.12, cognitive_dissonance_tolerance: 0.18,
    future_orientation: 0.82, hedonism_index: 0.62, autonomy_drive: 0.85,
    empathy_capacity: 0.78, reciprocity_responsiveness: 0.75,
  },
  // PP-005: MEA, corporate_executives → critical, loss_aversion_paralysis
  // loss_aversion_paralysis: loss_sensitivity≥0.70, cognitive_rigidity≥0.60
  // critical: composite ≥ 60
  {
    entity_id: "PP-005", segment_type: "corporate_executives", region: "MEA",
    values_coherence: 0.22, motivation_alignment: 0.20, cognitive_rigidity: 0.82,
    status_orientation: 0.80, risk_appetite_behavioral: 0.15, social_conformity_pressure: 0.52,
    identity_brand_fusion: 0.48, novelty_seeking: 0.15, loss_sensitivity: 0.88,
    authority_deference: 0.72, tribalism_intensity: 0.55, cognitive_dissonance_tolerance: 0.70,
    future_orientation: 0.18, hedonism_index: 0.42, autonomy_drive: 0.15,
    empathy_capacity: 0.22, reciprocity_responsiveness: 0.28,
  },
  // PP-006: EMEA, mainstream_consumers → moderate, none
  // moderate: composite 20–39
  {
    entity_id: "PP-006", segment_type: "mainstream_consumers", region: "EMEA",
    values_coherence: 0.62, motivation_alignment: 0.60, cognitive_rigidity: 0.35,
    status_orientation: 0.45, risk_appetite_behavioral: 0.52, social_conformity_pressure: 0.38,
    identity_brand_fusion: 0.40, novelty_seeking: 0.55, loss_sensitivity: 0.35,
    authority_deference: 0.38, tribalism_intensity: 0.30, cognitive_dissonance_tolerance: 0.32,
    future_orientation: 0.58, hedonism_index: 0.48, autonomy_drive: 0.60,
    empathy_capacity: 0.62, reciprocity_responsiveness: 0.58,
  },
  // PP-007: APAC, traditionalist_consumers → high, motivation_void
  // motivation_void: (1-motivation_alignment)≥0.65 => motivation_alignment≤0.35, (1-autonomy_drive)≥0.60 => autonomy_drive≤0.40
  // high: composite 40–59
  {
    entity_id: "PP-007", segment_type: "traditionalist_consumers", region: "APAC",
    values_coherence: 0.40, motivation_alignment: 0.28, cognitive_rigidity: 0.55,
    status_orientation: 0.52, risk_appetite_behavioral: 0.28, social_conformity_pressure: 0.55,
    identity_brand_fusion: 0.42, novelty_seeking: 0.30, loss_sensitivity: 0.58,
    authority_deference: 0.62, tribalism_intensity: 0.52, cognitive_dissonance_tolerance: 0.48,
    future_orientation: 0.35, hedonism_index: 0.30, autonomy_drive: 0.32,
    empathy_capacity: 0.40, reciprocity_responsiveness: 0.38,
  },
  // PP-008: NOAM, conservative_investors → critical, authority_dependency
  // authority_dependency: authority_deference≥0.70, (1-autonomy_drive)≥0.65 => autonomy_drive≤0.35
  // critical: composite ≥ 60
  {
    entity_id: "PP-008", segment_type: "conservative_investors", region: "NOAM",
    values_coherence: 0.18, motivation_alignment: 0.22, cognitive_rigidity: 0.75,
    status_orientation: 0.70, risk_appetite_behavioral: 0.12, social_conformity_pressure: 0.65,
    identity_brand_fusion: 0.52, novelty_seeking: 0.18, loss_sensitivity: 0.75,
    authority_deference: 0.85, tribalism_intensity: 0.62, cognitive_dissonance_tolerance: 0.72,
    future_orientation: 0.20, hedonism_index: 0.30, autonomy_drive: 0.28,
    empathy_capacity: 0.25, reciprocity_responsiveness: 0.30,
  },
];

type RawEntity = typeof MOCK_ENTITIES[0];

function valuesScore(e: RawEntity): number {
  const raw = (1 - e.values_coherence) * 0.4
    + (1 - e.motivation_alignment) * 0.35
    + e.cognitive_dissonance_tolerance * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function motivationScore(e: RawEntity): number {
  const raw = (1 - e.autonomy_drive) * 0.35
    + e.loss_sensitivity * 0.35
    + (1 - e.future_orientation) * 0.30;
  return Math.round(raw * 100 * 100) / 100;
}

function cognitiveScore(e: RawEntity): number {
  const raw = e.cognitive_rigidity * 0.4
    + e.authority_deference * 0.30
    + (1 - e.novelty_seeking) * 0.30;
  return Math.round(raw * 100 * 100) / 100;
}

function socialScore(e: RawEntity): number {
  const raw = e.tribalism_intensity * 0.4
    + e.social_conformity_pressure * 0.35
    + (1 - e.empathy_capacity) * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function psychComposite(vs: number, ms: number, cs: number, ss: number): number {
  return Math.round((vs * 0.30 + ms * 0.25 + cs * 0.25 + ss * 0.20) * 100) / 100;
}

function psychRisk(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}

function psychPattern(e: RawEntity): string {
  if ((1 - e.values_coherence) >= 0.65 && e.identity_brand_fusion >= 0.60) return "identity_lock";
  if (e.tribalism_intensity >= 0.70 && e.social_conformity_pressure >= 0.60) return "tribalism_capture";
  if (e.loss_sensitivity >= 0.70 && e.cognitive_rigidity >= 0.60) return "loss_aversion_paralysis";
  if ((1 - e.motivation_alignment) >= 0.65 && (1 - e.autonomy_drive) >= 0.60) return "motivation_void";
  if (e.authority_deference >= 0.70 && (1 - e.autonomy_drive) >= 0.65) return "authority_dependency";
  return "none";
}

function psychSeverity(composite: number): string {
  if (composite >= 75) return "behavioral_blockade";
  if (composite >= 50) return "high_resistance";
  if (composite >= 25) return "moderate_friction";
  return "behavioral_fluidity";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "psychographic_intervention";
  if (risk === "high" && pattern === "tribalism_capture") return "de_tribalization_protocol";
  if (risk === "high") return "behavioral_reframing";
  if (risk === "moderate") return "psych_monitoring";
  return "no_action";
}

function psychSignal(e: RawEntity, risk: string, composite: number): string {
  const compInt = Math.round(composite);
  if (risk === "critical") {
    return `Critique — cohérence valeurs ${Math.round(e.values_coherence * 100)}% — tribalisme ${Math.round(e.tribalism_intensity * 100)}% — composite ${compInt}`;
  }
  if (risk === "high") {
    return `Élevé — sensibilité à la perte ${Math.round(e.loss_sensitivity * 100)}% — rigidité cognitive ${Math.round(e.cognitive_rigidity * 100)}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `Modéré — pression conformité ${Math.round(e.social_conformity_pressure * 100)}% — composite ${compInt}`;
  }
  return "Profil psychographique favorable — motivations alignées, fluidité comportementale élevée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const vs = valuesScore(e);
      const ms = motivationScore(e);
      const cs = cognitiveScore(e);
      const ss = socialScore(e);
      const composite = psychComposite(vs, ms, cs, ss);
      const risk = psychRisk(composite);
      const pattern = psychPattern(e);
      const severity = psychSeverity(composite);
      const action = recommendedAction(risk, pattern);
      return {
        entity_id:                   e.entity_id,
        region:                      e.region,
        segment_type:                e.segment_type,
        psych_risk:                  risk,
        psych_pattern:               pattern,
        psych_severity:              severity,
        recommended_action:          action,
        values_score:                vs,
        motivation_score:            ms,
        cognitive_score:             cs,
        social_score:                ss,
        psych_composite:             composite,
        is_in_psych_crisis:          composite >= 60,
        requires_psych_intervention: composite >= 40,
        psych_signal:                psychSignal(e, risk, composite),
      };
    });

    const risk_counts:     Record<string, number> = {};
    const pattern_counts:  Record<string, number> = {};
    const severity_counts: Record<string, number> = {};
    const action_counts:   Record<string, number> = {};
    let tVs = 0, tMs = 0, tCs = 0, tSs = 0, tComp = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      risk_counts[ent.psych_risk]         = (risk_counts[ent.psych_risk]         || 0) + 1;
      pattern_counts[ent.psych_pattern]   = (pattern_counts[ent.psych_pattern]   || 0) + 1;
      severity_counts[ent.psych_severity] = (severity_counts[ent.psych_severity] || 0) + 1;
      action_counts[ent.recommended_action] = (action_counts[ent.recommended_action] || 0) + 1;
      tVs   += ent.values_score;
      tMs   += ent.motivation_score;
      tCs   += ent.cognitive_score;
      tSs   += ent.social_score;
      tComp += ent.psych_composite;
      if (ent.is_in_psych_crisis)          crisisCount++;
      if (ent.requires_psych_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComp = tComp / n;
    const summary = {
      total:                                      n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_psych_composite:                        Math.round(avgComp * 10) / 10,
      psych_crisis_count:                         crisisCount,
      psych_intervention_count:                   interventionCount,
      avg_values_score:                           Math.round(tVs / n * 10) / 10,
      avg_motivation_score:                       Math.round(tMs / n * 10) / 10,
      avg_cognitive_score:                        Math.round(tCs / n * 10) / 10,
      avg_social_score:                           Math.round(tSs / n * 10) / 10,
      avg_estimated_behavioral_resistance_index:  Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary }, "psychographic-profiling-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/psychographic-profiling-engine`);
    const json = await upstream.json();
    return NextResponse.json(
      sealResponse(json, "psychographic-profiling-engine")
    );
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream psychographic profiling engine unavailable" }, "psychographic-profiling-engine"),
      { status: 502 }
    );
  }
}
