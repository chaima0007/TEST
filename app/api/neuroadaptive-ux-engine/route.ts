import { NextResponse } from "next/server";

const MOCK_INTERFACES = [
  // NUX-001 enterprise_dashboard EMEA — critical cognitive_overload
  { interface_id:"NUX-001", ux_domain:"enterprise_dashboard", region:"EMEA",  cognitive_load_score:0.88, task_completion_rate:0.32, attention_retention_score:0.28, error_recovery_efficiency:0.22, adaptive_personalization_score:0.20, emotional_resonance_index:0.18, decision_fatigue_risk:0.82, information_density_balance:0.15, flow_state_facilitation:0.22, sensory_overload_risk:0.78, accessibility_compliance_score:0.30, cross_modal_coherence:0.25, feedback_loop_responsiveness:0.20, user_agency_score:0.28, cognitive_bias_mitigation:0.22, engagement_depth_score:0.25, neuroadaptive_accuracy:0.18 },
  // NUX-002 mobile_app NAMER — low neuroptimal
  { interface_id:"NUX-002", ux_domain:"mobile_app",           region:"NAMER", cognitive_load_score:0.15, task_completion_rate:0.92, attention_retention_score:0.90, error_recovery_efficiency:0.88, adaptive_personalization_score:0.92, emotional_resonance_index:0.88, decision_fatigue_risk:0.12, information_density_balance:0.88, flow_state_facilitation:0.90, sensory_overload_risk:0.10, accessibility_compliance_score:0.95, cross_modal_coherence:0.90, feedback_loop_responsiveness:0.92, user_agency_score:0.90, cognitive_bias_mitigation:0.88, engagement_depth_score:0.92, neuroadaptive_accuracy:0.90 },
  // NUX-003 voice_interface APAC — high attention_fragmentation
  { interface_id:"NUX-003", ux_domain:"voice_interface",      region:"APAC",  cognitive_load_score:0.52, task_completion_rate:0.55, attention_retention_score:0.28, error_recovery_efficiency:0.48, adaptive_personalization_score:0.55, emotional_resonance_index:0.45, decision_fatigue_risk:0.55, information_density_balance:0.50, flow_state_facilitation:0.32, sensory_overload_risk:0.45, accessibility_compliance_score:0.62, cross_modal_coherence:0.50, feedback_loop_responsiveness:0.52, user_agency_score:0.55, cognitive_bias_mitigation:0.48, engagement_depth_score:0.52, neuroadaptive_accuracy:0.55 },
  // NUX-004 ar_overlay LATAM — low optimizing
  { interface_id:"NUX-004", ux_domain:"ar_overlay",           region:"LATAM", cognitive_load_score:0.28, task_completion_rate:0.80, attention_retention_score:0.78, error_recovery_efficiency:0.75, adaptive_personalization_score:0.80, emotional_resonance_index:0.75, decision_fatigue_risk:0.22, information_density_balance:0.78, flow_state_facilitation:0.75, sensory_overload_risk:0.20, accessibility_compliance_score:0.82, cross_modal_coherence:0.80, feedback_loop_responsiveness:0.78, user_agency_score:0.80, cognitive_bias_mitigation:0.75, engagement_depth_score:0.78, neuroadaptive_accuracy:0.80 },
  // NUX-005 haptic_feedback EMEA — critical adaptation_failure
  { interface_id:"NUX-005", ux_domain:"haptic_feedback",      region:"EMEA",  cognitive_load_score:0.72, task_completion_rate:0.28, attention_retention_score:0.38, error_recovery_efficiency:0.22, adaptive_personalization_score:0.18, emotional_resonance_index:0.22, decision_fatigue_risk:0.68, information_density_balance:0.25, flow_state_facilitation:0.32, sensory_overload_risk:0.58, accessibility_compliance_score:0.35, cross_modal_coherence:0.28, feedback_loop_responsiveness:0.25, user_agency_score:0.32, cognitive_bias_mitigation:0.28, engagement_depth_score:0.32, neuroadaptive_accuracy:0.20 },
  // NUX-006 neural_bci NAMER — moderate none
  { interface_id:"NUX-006", ux_domain:"neural_bci",           region:"NAMER", cognitive_load_score:0.42, task_completion_rate:0.65, attention_retention_score:0.60, error_recovery_efficiency:0.58, adaptive_personalization_score:0.62, emotional_resonance_index:0.58, decision_fatigue_risk:0.38, information_density_balance:0.62, flow_state_facilitation:0.58, sensory_overload_risk:0.35, accessibility_compliance_score:0.68, cross_modal_coherence:0.62, feedback_loop_responsiveness:0.60, user_agency_score:0.62, cognitive_bias_mitigation:0.58, engagement_depth_score:0.60, neuroadaptive_accuracy:0.62 },
  // NUX-007 ambient_computing APAC — high engagement_collapse
  { interface_id:"NUX-007", ux_domain:"ambient_computing",    region:"APAC",  cognitive_load_score:0.58, task_completion_rate:0.32, attention_retention_score:0.45, error_recovery_efficiency:0.38, adaptive_personalization_score:0.48, emotional_resonance_index:0.35, decision_fatigue_risk:0.62, information_density_balance:0.40, flow_state_facilitation:0.45, sensory_overload_risk:0.52, accessibility_compliance_score:0.55, cross_modal_coherence:0.42, feedback_loop_responsiveness:0.48, user_agency_score:0.45, cognitive_bias_mitigation:0.42, engagement_depth_score:0.22, neuroadaptive_accuracy:0.48 },
  // NUX-008 conversational_ai MEA — critical accessibility_gap
  { interface_id:"NUX-008", ux_domain:"conversational_ai",    region:"MEA",   cognitive_load_score:0.78, task_completion_rate:0.25, attention_retention_score:0.32, error_recovery_efficiency:0.18, adaptive_personalization_score:0.22, emotional_resonance_index:0.15, decision_fatigue_risk:0.72, information_density_balance:0.20, flow_state_facilitation:0.28, sensory_overload_risk:0.68, accessibility_compliance_score:0.32, cross_modal_coherence:0.22, feedback_loop_responsiveness:0.20, user_agency_score:0.28, cognitive_bias_mitigation:0.18, engagement_depth_score:0.22, neuroadaptive_accuracy:0.20 },
];

type Interface = typeof MOCK_INTERFACES[0];

function cognitiveScore(i: Interface): number {
  let s = 0;
  if      (i.cognitive_load_score >= 0.75) s += 40; else if (i.cognitive_load_score >= 0.55) s += 22; else if (i.cognitive_load_score >= 0.40) s += 8;
  if      (i.decision_fatigue_risk >= 0.70) s += 35; else if (i.decision_fatigue_risk >= 0.50) s += 18; else if (i.decision_fatigue_risk >= 0.35) s += 6;
  if      (i.sensory_overload_risk >= 0.65) s += 25; else if (i.sensory_overload_risk >= 0.45) s += 12;
  return Math.min(s, 100);
}
function engagementScore(i: Interface): number {
  let s = 0;
  if      (i.attention_retention_score <= 0.35) s += 40; else if (i.attention_retention_score <= 0.55) s += 22; else if (i.attention_retention_score <= 0.70) s += 8;
  if      (i.flow_state_facilitation <= 0.30) s += 35; else if (i.flow_state_facilitation <= 0.50) s += 18; else if (i.flow_state_facilitation <= 0.65) s += 6;
  if      (i.engagement_depth_score <= 0.35) s += 25; else if (i.engagement_depth_score <= 0.55) s += 12;
  return Math.min(s, 100);
}
function adaptationScore(i: Interface): number {
  let s = 0;
  if      (i.adaptive_personalization_score <= 0.30) s += 40; else if (i.adaptive_personalization_score <= 0.50) s += 22; else if (i.adaptive_personalization_score <= 0.65) s += 8;
  if      (i.neuroadaptive_accuracy <= 0.30) s += 35; else if (i.neuroadaptive_accuracy <= 0.50) s += 18; else if (i.neuroadaptive_accuracy <= 0.65) s += 6;
  if      (i.feedback_loop_responsiveness <= 0.35) s += 25; else if (i.feedback_loop_responsiveness <= 0.55) s += 12;
  return Math.min(s, 100);
}
function accessibilityScore(i: Interface): number {
  let s = 0;
  if      (i.accessibility_compliance_score <= 0.50) s += 40; else if (i.accessibility_compliance_score <= 0.70) s += 22; else if (i.accessibility_compliance_score <= 0.80) s += 8;
  if      (i.user_agency_score <= 0.35) s += 35; else if (i.user_agency_score <= 0.55) s += 18; else if (i.user_agency_score <= 0.70) s += 6;
  if      (i.cognitive_bias_mitigation <= 0.30) s += 25; else if (i.cognitive_bias_mitigation <= 0.50) s += 12;
  return Math.min(s, 100);
}
function composite(cog: number, eng: number, adp: number, acc: number): number {
  return Math.min(Math.round((cog * 0.30 + eng * 0.25 + adp * 0.25 + acc * 0.20) * 100) / 100, 100);
}
function uxPattern(i: Interface): string {
  if (i.cognitive_load_score >= 0.75 && i.sensory_overload_risk >= 0.65) return "cognitive_overload";
  if (i.attention_retention_score <= 0.35 && i.flow_state_facilitation <= 0.40) return "attention_fragmentation";
  if (i.adaptive_personalization_score <= 0.30 && i.neuroadaptive_accuracy <= 0.30) return "adaptation_failure";
  if (i.engagement_depth_score <= 0.30 && i.task_completion_rate <= 0.40) return "engagement_collapse";
  if (i.accessibility_compliance_score <= 0.50 && i.user_agency_score <= 0.40) return "accessibility_gap";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "critical_load"; if (c >= 40) return "strained"; if (c >= 20) return "optimizing"; return "neuroptimal"; }
function action(r: string, p: string): string {
  if (r === "critical") return p === "cognitive_overload" ? "ux_redesign" : "load_shedding";
  if (r === "high")     return p === "attention_fragmentation" ? "adaptation_sprint" : "accessibility_audit";
  if (r === "moderate") return "ux_monitoring";
  return "no_action";
}
function signal(i: Interface, pat: string, comp: number): string {
  if (comp < 20) return "Interface neuroadaptive optimale — charge cognitive maîtrisée, engagement élevé, adaptation précise";
  const labels: Record<string,string> = {
    cognitive_overload:      "Surcharge cognitive",
    attention_fragmentation: "Fragmentation attentionnelle",
    adaptation_failure:      "Échec adaptation",
    engagement_collapse:     "Effondrement engagement",
    accessibility_gap:       "Lacune accessibilité",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — charge cog. ${Math.round(i.cognitive_load_score*100)}% — rétention att. ${Math.round(i.attention_retention_score*100)}% — adapt. neuro ${Math.round(i.neuroadaptive_accuracy*100)}% — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const interfaces = MOCK_INTERFACES.map(i => {
      const cog = cognitiveScore(i), eng = engagementScore(i), adp = adaptationScore(i), acc = accessibilityScore(i);
      const comp = composite(cog, eng, adp, acc), pat = uxPattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      return {
        interface_id: i.interface_id, ux_domain: i.ux_domain, region: i.region,
        ux_risk: r, ux_pattern: pat, ux_severity: sev, recommended_action: act,
        cognitive_score: cog, engagement_score: eng, adaptation_score: adp, accessibility_score: acc,
        ux_composite: comp,
        has_load_signal: comp >= 40 || i.cognitive_load_score >= 0.60 || i.sensory_overload_risk >= 0.55 || i.decision_fatigue_risk >= 0.60,
        requires_intervention: comp >= 25 || i.adaptive_personalization_score <= 0.35 || i.neuroadaptive_accuracy <= 0.35 || i.accessibility_compliance_score <= 0.55,
        estimated_cognitive_friction_index: Math.min(Math.round(comp/100*(1-adp/100+0.01)*10*100)/100, 10.0),
        ux_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tcog=0,teng=0,tadp=0,tacc=0,tcomp=0,tfri=0,loadC=0,intervC=0;
    for (const iface of interfaces) {
      rc[iface.ux_risk]=(rc[iface.ux_risk]||0)+1;
      pc[iface.ux_pattern]=(pc[iface.ux_pattern]||0)+1;
      sc[iface.ux_severity]=(sc[iface.ux_severity]||0)+1;
      ac[iface.recommended_action]=(ac[iface.recommended_action]||0)+1;
      tcog+=iface.cognitive_score; teng+=iface.engagement_score; tadp+=iface.adaptation_score; tacc+=iface.accessibility_score;
      tcomp+=iface.ux_composite; tfri+=iface.estimated_cognitive_friction_index;
      if (iface.has_load_signal) loadC++;
      if (iface.requires_intervention) intervC++;
    }
    const n = interfaces.length;
    return NextResponse.json({ interfaces, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_ux_composite: Math.round(tcomp/n*10)/10,
      load_signal_count: loadC, intervention_required_count: intervC,
      avg_cognitive_score: Math.round(tcog/n*10)/10,
      avg_engagement_score: Math.round(teng/n*10)/10,
      avg_adaptation_score: Math.round(tadp/n*10)/10,
      avg_accessibility_score: Math.round(tacc/n*10)/10,
      avg_estimated_cognitive_friction_index: Math.round(tfri/n*100)/100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/neuroadaptive-ux-engine`)).json());
}
