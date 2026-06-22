import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_TARGETS = [
  // CW-001 EMEA — critical narrative_capture
  { target_id:"CW-001", threat_domain:"narrative_warfare", region:"EMEA", disinformation_exposure_rate:0.85, source_credibility_score:0.15, narrative_coherence_score:0.18, deepfake_detection_capability:0.20, echo_chamber_penetration:0.78, adversarial_bot_density:0.72, information_decay_velocity:0.80, fact_checking_coverage:0.12, cognitive_bias_exploitation_risk:0.82, media_literacy_score:0.15, counter_narrative_strength:0.12, epistemic_resilience_score:0.18, institutional_trust_level:0.15, cross_source_verification_rate:0.10, manipulation_detection_latency:0.85, information_sovereignty_score:0.12, strategic_communication_clarity:0.15 },
  // CW-002 NAMER — low sovereign
  { target_id:"CW-002", threat_domain:"algorithmic_amplification", region:"NAMER", disinformation_exposure_rate:0.08, source_credibility_score:0.92, narrative_coherence_score:0.90, deepfake_detection_capability:0.95, echo_chamber_penetration:0.08, adversarial_bot_density:0.05, information_decay_velocity:0.05, fact_checking_coverage:0.92, cognitive_bias_exploitation_risk:0.08, media_literacy_score:0.92, counter_narrative_strength:0.90, epistemic_resilience_score:0.92, institutional_trust_level:0.90, cross_source_verification_rate:0.92, manipulation_detection_latency:0.05, information_sovereignty_score:0.92, strategic_communication_clarity:0.92 },
  // CW-003 APAC — high deepfake_assault
  { target_id:"CW-003", threat_domain:"deepfake_campaign", region:"APAC", disinformation_exposure_rate:0.55, source_credibility_score:0.42, narrative_coherence_score:0.48, deepfake_detection_capability:0.18, echo_chamber_penetration:0.52, adversarial_bot_density:0.45, information_decay_velocity:0.58, fact_checking_coverage:0.35, cognitive_bias_exploitation_risk:0.55, media_literacy_score:0.38, counter_narrative_strength:0.35, epistemic_resilience_score:0.40, institutional_trust_level:0.42, cross_source_verification_rate:0.32, manipulation_detection_latency:0.60, information_sovereignty_score:0.40, strategic_communication_clarity:0.42 },
  // CW-004 LATAM — low resistant
  { target_id:"CW-004", threat_domain:"astroturfing", region:"LATAM", disinformation_exposure_rate:0.20, source_credibility_score:0.75, narrative_coherence_score:0.78, deepfake_detection_capability:0.80, echo_chamber_penetration:0.18, adversarial_bot_density:0.15, information_decay_velocity:0.20, fact_checking_coverage:0.78, cognitive_bias_exploitation_risk:0.20, media_literacy_score:0.78, counter_narrative_strength:0.75, epistemic_resilience_score:0.78, institutional_trust_level:0.75, cross_source_verification_rate:0.78, manipulation_detection_latency:0.18, information_sovereignty_score:0.78, strategic_communication_clarity:0.80 },
  // CW-005 EMEA — critical epistemic_collapse
  { target_id:"CW-005", threat_domain:"epistemic_attack", region:"EMEA", disinformation_exposure_rate:0.75, source_credibility_score:0.20, narrative_coherence_score:0.22, deepfake_detection_capability:0.25, echo_chamber_penetration:0.70, adversarial_bot_density:0.65, information_decay_velocity:0.78, fact_checking_coverage:0.18, cognitive_bias_exploitation_risk:0.82, media_literacy_score:0.18, counter_narrative_strength:0.15, epistemic_resilience_score:0.18, institutional_trust_level:0.28, cross_source_verification_rate:0.15, manipulation_detection_latency:0.80, information_sovereignty_score:0.20, strategic_communication_clarity:0.18 },
  // CW-006 NAMER — moderate none
  { target_id:"CW-006", threat_domain:"influence_operation", region:"NAMER", disinformation_exposure_rate:0.35, source_credibility_score:0.58, narrative_coherence_score:0.55, deepfake_detection_capability:0.58, echo_chamber_penetration:0.32, adversarial_bot_density:0.28, information_decay_velocity:0.38, fact_checking_coverage:0.55, cognitive_bias_exploitation_risk:0.38, media_literacy_score:0.55, counter_narrative_strength:0.52, epistemic_resilience_score:0.55, institutional_trust_level:0.55, cross_source_verification_rate:0.52, manipulation_detection_latency:0.35, information_sovereignty_score:0.55, strategic_communication_clarity:0.58 },
  // CW-007 APAC — high bot_swarm_attack
  { target_id:"CW-007", threat_domain:"algorithmic_amplification", region:"APAC", disinformation_exposure_rate:0.62, source_credibility_score:0.38, narrative_coherence_score:0.42, deepfake_detection_capability:0.40, echo_chamber_penetration:0.72, adversarial_bot_density:0.78, information_decay_velocity:0.65, fact_checking_coverage:0.38, cognitive_bias_exploitation_risk:0.60, media_literacy_score:0.38, counter_narrative_strength:0.35, epistemic_resilience_score:0.38, institutional_trust_level:0.42, cross_source_verification_rate:0.35, manipulation_detection_latency:0.65, information_sovereignty_score:0.38, strategic_communication_clarity:0.40 },
  // CW-008 MEA — critical trust_erosion
  { target_id:"CW-008", threat_domain:"memory_hole", region:"MEA", disinformation_exposure_rate:0.78, source_credibility_score:0.22, narrative_coherence_score:0.38, deepfake_detection_capability:0.22, echo_chamber_penetration:0.72, adversarial_bot_density:0.68, information_decay_velocity:0.82, fact_checking_coverage:0.15, cognitive_bias_exploitation_risk:0.75, media_literacy_score:0.18, counter_narrative_strength:0.15, epistemic_resilience_score:0.22, institutional_trust_level:0.22, cross_source_verification_rate:0.12, manipulation_detection_latency:0.82, information_sovereignty_score:0.18, strategic_communication_clarity:0.20 },
];

type Target = typeof MOCK_TARGETS[0];

function exposureScore(t: Target): number {
  let s = 0;
  if      (t.disinformation_exposure_rate >= 0.70) s += 40; else if (t.disinformation_exposure_rate >= 0.45) s += 22; else if (t.disinformation_exposure_rate >= 0.25) s += 8;
  if      (t.echo_chamber_penetration >= 0.70) s += 35; else if (t.echo_chamber_penetration >= 0.45) s += 18; else if (t.echo_chamber_penetration >= 0.25) s += 6;
  if      (t.adversarial_bot_density >= 0.65) s += 25; else if (t.adversarial_bot_density >= 0.40) s += 12;
  return Math.min(s, 100);
}
function detectionScore(t: Target): number {
  let s = 0;
  if      (t.deepfake_detection_capability <= 0.25) s += 40; else if (t.deepfake_detection_capability <= 0.50) s += 22; else if (t.deepfake_detection_capability <= 0.70) s += 8;
  if      (t.fact_checking_coverage <= 0.25) s += 35; else if (t.fact_checking_coverage <= 0.50) s += 18; else if (t.fact_checking_coverage <= 0.70) s += 6;
  if      (t.cross_source_verification_rate <= 0.30) s += 25; else if (t.cross_source_verification_rate <= 0.55) s += 12;
  return Math.min(s, 100);
}
function resilienceScore(t: Target): number {
  let s = 0;
  if      (t.epistemic_resilience_score <= 0.25) s += 40; else if (t.epistemic_resilience_score <= 0.50) s += 22; else if (t.epistemic_resilience_score <= 0.70) s += 8;
  if      (t.media_literacy_score <= 0.25) s += 35; else if (t.media_literacy_score <= 0.50) s += 18; else if (t.media_literacy_score <= 0.70) s += 6;
  if      (t.counter_narrative_strength <= 0.30) s += 25; else if (t.counter_narrative_strength <= 0.55) s += 12;
  return Math.min(s, 100);
}
function sovereigntyScore(t: Target): number {
  let s = 0;
  if      (t.information_sovereignty_score <= 0.25) s += 40; else if (t.information_sovereignty_score <= 0.50) s += 22; else if (t.information_sovereignty_score <= 0.70) s += 8;
  if      (t.institutional_trust_level <= 0.25) s += 35; else if (t.institutional_trust_level <= 0.50) s += 18; else if (t.institutional_trust_level <= 0.70) s += 6;
  if      (t.manipulation_detection_latency >= 0.70) s += 25; else if (t.manipulation_detection_latency >= 0.45) s += 12;
  return Math.min(s, 100);
}
function composite(exp: number, det: number, res: number, sov: number): number {
  return Math.min(Math.round((exp * 0.30 + det * 0.25 + res * 0.25 + sov * 0.20) * 100) / 100, 100);
}
function warfarePattern(t: Target): string {
  if (t.disinformation_exposure_rate >= 0.7 && t.narrative_coherence_score <= 0.3) return "narrative_capture";
  if (t.deepfake_detection_capability <= 0.3 && ["deepfake_campaign","perception_hacking"].includes(t.threat_domain)) return "deepfake_assault";
  if (t.epistemic_resilience_score <= 0.25 && t.cognitive_bias_exploitation_risk >= 0.7) return "epistemic_collapse";
  if (t.adversarial_bot_density >= 0.7 && t.echo_chamber_penetration >= 0.65) return "bot_swarm_attack";
  if (t.institutional_trust_level <= 0.3 && t.source_credibility_score <= 0.35) return "trust_erosion";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "captured"; if (c >= 40) return "compromised"; if (c >= 20) return "resistant"; return "sovereign"; }
function action(r: string, p: string): string {
  if (r === "critical") return p === "narrative_capture" ? "cognitive_defense_protocol" : "narrative_counterstrike";
  if (r === "high")     return p === "bot_swarm_attack"  ? "bot_neutralization" : "epistemic_reinforcement";
  if (r === "moderate") return "info_monitoring";
  return "no_action";
}
function signal(t: Target, pat: string, comp: number): string {
  if (comp < 20) return "Intégrité informationnelle forte — souveraineté épistémique active, faible exposition aux menaces cognitives";
  const labels: Record<string,string> = {
    narrative_capture:  "Capture narrative",
    deepfake_assault:   "Assaut deepfake",
    epistemic_collapse: "Effondrement épistémique",
    bot_swarm_attack:   "Attaque essaim de bots",
    trust_erosion:      "Érosion de confiance",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — exposition désinformation ${t.disinformation_exposure_rate.toFixed(2)} — densité bots ${t.adversarial_bot_density.toFixed(2)} — résilience épistémique ${t.epistemic_resilience_score.toFixed(2)} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[cognitive-warfare-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tcomp=0, texp=0, tdet=0, tres=0, tsov=0, tvuln=0, activeC=0, immC=0;
    for (const tgt of targets) {
      rc[tgt.cognitive_warfare_risk]  = (rc[tgt.cognitive_warfare_risk]  || 0) + 1;
      pc[tgt.warfare_pattern]         = (pc[tgt.warfare_pattern]         || 0) + 1;
      sc[tgt.cognitive_severity]      = (sc[tgt.cognitive_severity]      || 0) + 1;
      ac[tgt.recommended_action]      = (ac[tgt.recommended_action]      || 0) + 1;
      tcomp += tgt.cognitive_warfare_composite;
      texp  += tgt.exposure_score;
      tdet  += tgt.detection_score;
      tres  += tgt.resilience_score;
      tsov  += tgt.sovereignty_score;
      tvuln += tgt.estimated_cognitive_vulnerability_index;
      if (tgt.has_active_threat)           activeC++;
      if (tgt.requires_immediate_response) immC++;
    }
    const n = targets.length;
    return sealResponse(NextResponse.json(sealResponse({
      targets,
      summary: {
        total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
        avg_cognitive_warfare_composite: Math.round(tcomp / n * 10) / 10,
        active_threat_count: activeC,
        immediate_response_count: immC,
        avg_exposure_score: Math.round(texp / n * 10) / 10,
        avg_detection_score: Math.round(tdet / n * 10) / 10,
        avg_resilience_score: Math.round(tres / n * 10) / 10,
        avg_sovereignty_score: Math.round(tsov / n * 10) / 10,
        avg_estimated_cognitive_vulnerability_index: Math.round(tvuln / n * 100) / 100,
      },
    }, "cognitive-warfare-engine")));
  }
  return sealResponse(NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/cognitive-warfare-engine`, { next: { revalidate: 30 } })).json()));
}
