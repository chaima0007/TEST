import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_SEGMENTS = [
  // HP-001 — critical, personalization_blindspot
  { segment_id:"HP-001", channel_type:"email_sequence",          region:"EMEA",  personalization_depth_score:0.12, contextual_relevance_accuracy:0.15, behavioral_signal_utilization:0.18, privacy_consent_compliance:0.72, real_time_adaptation_speed:0.20, segment_granularity_score:0.15, cross_channel_coherence:0.22, propensity_model_accuracy:0.18, fatigue_risk_score:0.45, value_proposition_fit:0.25, emotional_resonance_score:0.20, next_best_action_precision:0.15, attribution_clarity_score:0.28, lifetime_value_impact:0.18, churn_prevention_effectiveness:0.22, conversion_lift_estimate:0.12, recommendation_diversity_score:0.30 },
  // HP-002 — low, hyperpersonalized
  { segment_id:"HP-002", channel_type:"in_app_experience",       region:"NAMER", personalization_depth_score:0.88, contextual_relevance_accuracy:0.92, behavioral_signal_utilization:0.70, privacy_consent_compliance:0.95, real_time_adaptation_speed:0.90, segment_granularity_score:0.92, cross_channel_coherence:0.88, propensity_model_accuracy:0.90, fatigue_risk_score:0.12, value_proposition_fit:0.92, emotional_resonance_score:0.88, next_best_action_precision:0.90, attribution_clarity_score:0.92, lifetime_value_impact:0.88, churn_prevention_effectiveness:0.90, conversion_lift_estimate:0.85, recommendation_diversity_score:0.80 },
  // HP-003 — high, audience_fatigue
  { segment_id:"HP-003", channel_type:"sales_outreach",          region:"APAC",  personalization_depth_score:0.82, contextual_relevance_accuracy:0.55, behavioral_signal_utilization:0.60, privacy_consent_compliance:0.68, real_time_adaptation_speed:0.48, segment_granularity_score:0.52, cross_channel_coherence:0.28, propensity_model_accuracy:0.50, fatigue_risk_score:0.78, value_proposition_fit:0.48, emotional_resonance_score:0.42, next_best_action_precision:0.45, attribution_clarity_score:0.50, lifetime_value_impact:0.45, churn_prevention_effectiveness:0.40, conversion_lift_estimate:0.38, recommendation_diversity_score:0.35 },
  // HP-004 — low, personalizing
  { segment_id:"HP-004", channel_type:"content_recommendation",  region:"LATAM", personalization_depth_score:0.72, contextual_relevance_accuracy:0.78, behavioral_signal_utilization:0.62, privacy_consent_compliance:0.88, real_time_adaptation_speed:0.75, segment_granularity_score:0.78, cross_channel_coherence:0.80, propensity_model_accuracy:0.75, fatigue_risk_score:0.22, value_proposition_fit:0.78, emotional_resonance_score:0.75, next_best_action_precision:0.78, attribution_clarity_score:0.80, lifetime_value_impact:0.75, churn_prevention_effectiveness:0.78, conversion_lift_estimate:0.72, recommendation_diversity_score:0.70 },
  // HP-005 — critical, privacy_breach
  { segment_id:"HP-005", channel_type:"pricing_adaptation",      region:"EMEA",  personalization_depth_score:0.70, contextual_relevance_accuracy:0.55, behavioral_signal_utilization:0.92, privacy_consent_compliance:0.18, real_time_adaptation_speed:0.60, segment_granularity_score:0.65, cross_channel_coherence:0.55, propensity_model_accuracy:0.58, fatigue_risk_score:0.55, value_proposition_fit:0.52, emotional_resonance_score:0.48, next_best_action_precision:0.52, attribution_clarity_score:0.20, lifetime_value_impact:0.50, churn_prevention_effectiveness:0.48, conversion_lift_estimate:0.42, recommendation_diversity_score:0.40 },
  // HP-006 — moderate, none
  { segment_id:"HP-006", channel_type:"product_bundling",        region:"NAMER", personalization_depth_score:0.55, contextual_relevance_accuracy:0.58, behavioral_signal_utilization:0.50, privacy_consent_compliance:0.75, real_time_adaptation_speed:0.52, segment_granularity_score:0.55, cross_channel_coherence:0.60, propensity_model_accuracy:0.55, fatigue_risk_score:0.38, value_proposition_fit:0.58, emotional_resonance_score:0.52, next_best_action_precision:0.55, attribution_clarity_score:0.60, lifetime_value_impact:0.52, churn_prevention_effectiveness:0.50, conversion_lift_estimate:0.48, recommendation_diversity_score:0.52 },
  // HP-007 — high, relevance_decay
  { segment_id:"HP-007", channel_type:"timing_optimization",     region:"MEA",   personalization_depth_score:0.60, contextual_relevance_accuracy:0.32, behavioral_signal_utilization:0.45, privacy_consent_compliance:0.70, real_time_adaptation_speed:0.38, segment_granularity_score:0.42, cross_channel_coherence:0.48, propensity_model_accuracy:0.28, fatigue_risk_score:0.55, value_proposition_fit:0.38, emotional_resonance_score:0.32, next_best_action_precision:0.30, attribution_clarity_score:0.45, lifetime_value_impact:0.38, churn_prevention_effectiveness:0.35, conversion_lift_estimate:0.32, recommendation_diversity_score:0.40 },
  // HP-008 — critical, attribution_chaos
  { segment_id:"HP-008", channel_type:"channel_mix",             region:"APAC",  personalization_depth_score:0.58, contextual_relevance_accuracy:0.45, behavioral_signal_utilization:0.55, privacy_consent_compliance:0.60, real_time_adaptation_speed:0.42, segment_granularity_score:0.48, cross_channel_coherence:0.38, propensity_model_accuracy:0.52, fatigue_risk_score:0.60, value_proposition_fit:0.40, emotional_resonance_score:0.38, next_best_action_precision:0.45, attribution_clarity_score:0.15, lifetime_value_impact:0.28, churn_prevention_effectiveness:0.25, conversion_lift_estimate:0.22, recommendation_diversity_score:0.35 },
];

type Segment = typeof MOCK_SEGMENTS[0];

function relevanceScore(s: Segment): number {
  let sc = 0;
  if      (s.contextual_relevance_accuracy <= 0.25) sc += 40; else if (s.contextual_relevance_accuracy <= 0.50) sc += 22; else if (s.contextual_relevance_accuracy <= 0.70) sc += 8;
  if      (s.propensity_model_accuracy <= 0.25)     sc += 35; else if (s.propensity_model_accuracy <= 0.50)     sc += 18; else if (s.propensity_model_accuracy <= 0.70)     sc += 6;
  if      (s.next_best_action_precision <= 0.25)    sc += 25; else if (s.next_best_action_precision <= 0.50)    sc += 12;
  return Math.min(sc, 100);
}
function fatigueScore(s: Segment): number {
  let sc = 0;
  if      (s.fatigue_risk_score >= 0.75)            sc += 40; else if (s.fatigue_risk_score >= 0.50)            sc += 22; else if (s.fatigue_risk_score >= 0.30)            sc += 8;
  if      (s.personalization_depth_score >= 0.90)   sc += 35; else if (s.personalization_depth_score >= 0.75)   sc += 18; else if (s.personalization_depth_score >= 0.60)   sc += 6;
  if      (s.cross_channel_coherence <= 0.25)       sc += 25; else if (s.cross_channel_coherence <= 0.50)       sc += 12;
  return Math.min(sc, 100);
}
function privacyScore(s: Segment): number {
  let sc = 0;
  if      (s.privacy_consent_compliance <= 0.25)    sc += 40; else if (s.privacy_consent_compliance <= 0.50)    sc += 22; else if (s.privacy_consent_compliance <= 0.70)    sc += 8;
  if      (s.attribution_clarity_score <= 0.25)     sc += 35; else if (s.attribution_clarity_score <= 0.50)     sc += 18; else if (s.attribution_clarity_score <= 0.70)     sc += 6;
  if      (s.behavioral_signal_utilization >= 0.90) sc += 25; else if (s.behavioral_signal_utilization >= 0.75) sc += 12;
  return Math.min(sc, 100);
}
function impactScore(s: Segment): number {
  let sc = 0;
  if      (s.conversion_lift_estimate <= 0.20)        sc += 40; else if (s.conversion_lift_estimate <= 0.40)        sc += 22; else if (s.conversion_lift_estimate <= 0.60)        sc += 8;
  if      (s.lifetime_value_impact <= 0.20)           sc += 35; else if (s.lifetime_value_impact <= 0.40)           sc += 18; else if (s.lifetime_value_impact <= 0.60)           sc += 6;
  if      (s.churn_prevention_effectiveness <= 0.20)  sc += 25; else if (s.churn_prevention_effectiveness <= 0.40)  sc += 12;
  return Math.min(sc, 100);
}
function composite(rel: number, fat: number, priv: number, imp: number): number {
  return Math.min(Math.round((rel * 0.30 + fat * 0.25 + priv * 0.25 + imp * 0.20) * 100) / 100, 100);
}
function personalizationPattern(s: Segment): string {
  if (s.privacy_consent_compliance <= 0.30 && s.behavioral_signal_utilization >= 0.75) return "privacy_breach";
  if (s.attribution_clarity_score <= 0.25 && s.conversion_lift_estimate <= 0.30)       return "attribution_chaos";
  if (s.personalization_depth_score <= 0.25 && s.contextual_relevance_accuracy <= 0.30) return "personalization_blindspot";
  if (s.fatigue_risk_score >= 0.65 && s.cross_channel_coherence <= 0.45)               return "audience_fatigue";
  if (s.propensity_model_accuracy <= 0.35 && s.next_best_action_precision <= 0.35)     return "relevance_decay";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "irrelevant"; if (c >= 40) return "generic"; if (c >= 20) return "personalizing"; return "hyperpersonalized"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "privacy_breach") return "consent_audit";
    return "personalization_reset";
  }
  if (r === "high") {
    if (p === "audience_fatigue") return "fatigue_recovery";
    return "segment_refresh";
  }
  if (r === "moderate") return "personalization_monitoring";
  return "no_action";
}
function signal(s: Segment, pat: string, comp: number): string {
  if (comp < 20)
    return "Hyperpersonnalisation efficace — ciblage précis, consentement respecté, impact revenus confirmé, modèles propensity performants";
  const labels: Record<string, string> = {
    personalization_blindspot: "Point aveugle personnalisation",
    audience_fatigue:          "Fatigue audience",
    privacy_breach:            "Risque vie privée",
    relevance_decay:           "Dégradation pertinence",
    attribution_chaos:         "Chaos attribution revenus",
  };
  const label = labels[pat] ?? pat.replace(/_/g, " ");
  return `${label} — profondeur ${s.personalization_depth_score.toFixed(2)} — pertinence ${Math.round(s.contextual_relevance_accuracy * 100)}% — consentement ${Math.round(s.privacy_consent_compliance * 100)}% — lift conversion ${Math.round(s.conversion_lift_estimate * 100)}% — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const segments = MOCK_SEGMENTS.map(s => {
      const rel = relevanceScore(s), fat = fatigueScore(s), priv = privacyScore(s), imp = impactScore(s);
      const comp = composite(rel, fat, priv, imp), pat = personalizationPattern(s), r = risk(comp), sev = severity(comp), act = action(r, pat);
      return {
        segment_id: s.segment_id, channel_type: s.channel_type, region: s.region,
        personalization_risk: r, personalization_pattern: pat, personalization_severity: sev, recommended_action: act,
        relevance_score: rel, fatigue_score: fat, privacy_score: priv, impact_score: imp,
        personalization_composite: comp,
        has_targeting_gap: comp >= 35 || s.segment_granularity_score <= 0.30 || s.next_best_action_precision <= 0.30 || s.propensity_model_accuracy <= 0.30,
        requires_consent_review: comp >= 25 || s.privacy_consent_compliance <= 0.40 || s.behavioral_signal_utilization >= 0.80 || s.attribution_clarity_score <= 0.30,
        estimated_personalization_gap_index: Math.min(Math.round(comp / 100 * (1 - s.attribution_clarity_score + 0.01) * 10 * 100) / 100, 10.0),
        personalization_signal: signal(s, pat, comp),
      };
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let trel=0, tfat=0, tpriv=0, timp=0, tcomp=0, tgap=0, gapC=0, consentC=0;
    for (const seg of segments) {
      rc[seg.personalization_risk]    = (rc[seg.personalization_risk]    || 0) + 1;
      pc[seg.personalization_pattern] = (pc[seg.personalization_pattern] || 0) + 1;
      sc[seg.personalization_severity]= (sc[seg.personalization_severity]|| 0) + 1;
      ac[seg.recommended_action]      = (ac[seg.recommended_action]      || 0) + 1;
      trel += seg.relevance_score; tfat += seg.fatigue_score; tpriv += seg.privacy_score; timp += seg.impact_score;
      tcomp += seg.personalization_composite; tgap += seg.estimated_personalization_gap_index;
      if (seg.has_targeting_gap)       gapC++;
      if (seg.requires_consent_review) consentC++;
    }
    const n = segments.length;
    return NextResponse.json(sealResponse({
      segments,
      summary: {
        total: n,
        risk_counts: rc,
        pattern_counts: pc,
        severity_counts: sc,
        action_counts: ac,
        avg_personalization_composite: Math.round(tcomp / n * 10) / 10,
        targeting_gap_count: gapC,
        consent_review_required_count: consentC,
        avg_relevance_score: Math.round(trel / n * 10) / 10,
        avg_fatigue_score: Math.round(tfat / n * 10) / 10,
        avg_privacy_score: Math.round(tpriv / n * 10) / 10,
        avg_impact_score: Math.round(timp / n * 10) / 10,
        avg_estimated_personalization_gap_index: Math.round(tgap / n * 100) / 100,
      },
    }, "hyperpersonalization-engine"));
  }
  return NextResponse.json(sealResponse(
    await (await fetch(`${process.env.SWARM_API_URL}/hyperpersonalization-engine`)).json(),
    "hyperpersonalization-engine"
  ));
}
