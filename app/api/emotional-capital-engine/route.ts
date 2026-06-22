import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_UNITS = [
  // EC-001 executive_layer EMEA — critical burnout_crisis
  { unit_id:"EC-001", workforce_segment:"executive_layer",  region:"EMEA",  psychological_safety_score:0.30, burnout_prevalence_rate:0.78, emotional_exhaustion_index:0.82, meaning_alignment_score:0.28, social_connection_quality:0.32, autonomy_satisfaction_score:0.35, recognition_adequacy:0.22, resilience_capital_score:0.18, grief_processing_support:0.15, somatic_health_score:0.22, financial_anxiety_exposure:0.55, purpose_clarity_score:0.30, community_belonging_index:0.25, leadership_empathy_score:0.28, work_life_integration_score:0.20, emotional_contagion_awareness:0.35, joy_at_work_index:0.15 },
  // EC-002 technical_staff NAMER — low flourishing
  { unit_id:"EC-002", workforce_segment:"technical_staff",  region:"NAMER", psychological_safety_score:0.92, burnout_prevalence_rate:0.08, emotional_exhaustion_index:0.10, meaning_alignment_score:0.90, social_connection_quality:0.88, autonomy_satisfaction_score:0.92, recognition_adequacy:0.88, resilience_capital_score:0.90, grief_processing_support:0.85, somatic_health_score:0.88, financial_anxiety_exposure:0.05, purpose_clarity_score:0.92, community_belonging_index:0.88, leadership_empathy_score:0.90, work_life_integration_score:0.88, emotional_contagion_awareness:0.85, joy_at_work_index:0.92 },
  // EC-003 frontline_workers APAC — high meaning_collapse
  { unit_id:"EC-003", workforce_segment:"frontline_workers", region:"APAC", psychological_safety_score:0.62, burnout_prevalence_rate:0.30, emotional_exhaustion_index:0.30, meaning_alignment_score:0.22, social_connection_quality:0.55, autonomy_satisfaction_score:0.52, recognition_adequacy:0.55, resilience_capital_score:0.55, grief_processing_support:0.52, somatic_health_score:0.62, financial_anxiety_exposure:0.35, purpose_clarity_score:0.18, community_belonging_index:0.55, leadership_empathy_score:0.65, work_life_integration_score:0.55, emotional_contagion_awareness:0.52, joy_at_work_index:0.48 },
  // EC-004 creative_teams LATAM — moderate recovering
  { unit_id:"EC-004", workforce_segment:"creative_teams",   region:"LATAM", psychological_safety_score:0.58, burnout_prevalence_rate:0.42, emotional_exhaustion_index:0.28, meaning_alignment_score:0.62, social_connection_quality:0.62, autonomy_satisfaction_score:0.62, recognition_adequacy:0.50, resilience_capital_score:0.55, grief_processing_support:0.58, somatic_health_score:0.65, financial_anxiety_exposure:0.30, purpose_clarity_score:0.56, community_belonging_index:0.58, leadership_empathy_score:0.60, work_life_integration_score:0.58, emotional_contagion_awareness:0.58, joy_at_work_index:0.68 },
  // EC-005 remote_workforce EMEA — critical isolation_epidemic
  { unit_id:"EC-005", workforce_segment:"remote_workforce", region:"EMEA",  psychological_safety_score:0.38, burnout_prevalence_rate:0.55, emotional_exhaustion_index:0.55, meaning_alignment_score:0.42, social_connection_quality:0.18, autonomy_satisfaction_score:0.32, recognition_adequacy:0.28, resilience_capital_score:0.22, grief_processing_support:0.20, somatic_health_score:0.32, financial_anxiety_exposure:0.62, purpose_clarity_score:0.40, community_belonging_index:0.15, leadership_empathy_score:0.35, work_life_integration_score:0.25, emotional_contagion_awareness:0.28, joy_at_work_index:0.18 },
  // EC-006 gig_workforce NAMER — moderate none
  { unit_id:"EC-006", workforce_segment:"gig_workforce",    region:"NAMER", psychological_safety_score:0.62, burnout_prevalence_rate:0.32, emotional_exhaustion_index:0.30, meaning_alignment_score:0.58, social_connection_quality:0.55, autonomy_satisfaction_score:0.60, recognition_adequacy:0.52, resilience_capital_score:0.58, grief_processing_support:0.50, somatic_health_score:0.60, financial_anxiety_exposure:0.40, purpose_clarity_score:0.58, community_belonging_index:0.52, leadership_empathy_score:0.60, work_life_integration_score:0.55, emotional_contagion_awareness:0.58, joy_at_work_index:0.55 },
  // EC-007 customer_facing APAC — high safety_erosion
  { unit_id:"EC-007", workforce_segment:"customer_facing",  region:"APAC",  psychological_safety_score:0.28, burnout_prevalence_rate:0.40, emotional_exhaustion_index:0.42, meaning_alignment_score:0.60, social_connection_quality:0.60, autonomy_satisfaction_score:0.55, recognition_adequacy:0.35, resilience_capital_score:0.48, grief_processing_support:0.42, somatic_health_score:0.52, financial_anxiety_exposure:0.38, purpose_clarity_score:0.58, community_belonging_index:0.55, leadership_empathy_score:0.22, work_life_integration_score:0.52, emotional_contagion_awareness:0.45, joy_at_work_index:0.45 },
  // EC-008 caregiving_roles MEA — critical joy_deficit
  { unit_id:"EC-008", workforce_segment:"caregiving_roles", region:"MEA",   psychological_safety_score:0.50, burnout_prevalence_rate:0.55, emotional_exhaustion_index:0.62, meaning_alignment_score:0.55, social_connection_quality:0.42, autonomy_satisfaction_score:0.32, recognition_adequacy:0.22, resilience_capital_score:0.22, grief_processing_support:0.20, somatic_health_score:0.28, financial_anxiety_exposure:0.60, purpose_clarity_score:0.50, community_belonging_index:0.38, leadership_empathy_score:0.45, work_life_integration_score:0.28, emotional_contagion_awareness:0.25, joy_at_work_index:0.12 },
];

type Unit = typeof MOCK_UNITS[0];

function burnoutScore(u: Unit): number {
  let s = 0;
  if      (u.burnout_prevalence_rate >= 0.65) s += 40; else if (u.burnout_prevalence_rate >= 0.40) s += 22; else if (u.burnout_prevalence_rate >= 0.20) s += 8;
  if      (u.emotional_exhaustion_index >= 0.65) s += 35; else if (u.emotional_exhaustion_index >= 0.40) s += 18; else if (u.emotional_exhaustion_index >= 0.20) s += 6;
  if      (u.financial_anxiety_exposure >= 0.65) s += 25; else if (u.financial_anxiety_exposure >= 0.40) s += 12;
  return Math.min(s, 100);
}
function safetyScore(u: Unit): number {
  let s = 0;
  if      (u.psychological_safety_score <= 0.35) s += 40; else if (u.psychological_safety_score <= 0.55) s += 22; else if (u.psychological_safety_score <= 0.70) s += 8;
  if      (u.leadership_empathy_score <= 0.35) s += 35; else if (u.leadership_empathy_score <= 0.55) s += 18; else if (u.leadership_empathy_score <= 0.70) s += 6;
  if      (u.recognition_adequacy <= 0.35) s += 25; else if (u.recognition_adequacy <= 0.55) s += 12;
  return Math.min(s, 100);
}
function meaningScore(u: Unit): number {
  let s = 0;
  if      (u.meaning_alignment_score <= 0.35) s += 40; else if (u.meaning_alignment_score <= 0.55) s += 22; else if (u.meaning_alignment_score <= 0.70) s += 8;
  if      (u.purpose_clarity_score <= 0.35) s += 35; else if (u.purpose_clarity_score <= 0.55) s += 18; else if (u.purpose_clarity_score <= 0.70) s += 6;
  if      (u.autonomy_satisfaction_score <= 0.35) s += 25; else if (u.autonomy_satisfaction_score <= 0.55) s += 12;
  return Math.min(s, 100);
}
function connectionScore(u: Unit): number {
  let s = 0;
  if      (u.social_connection_quality <= 0.35) s += 40; else if (u.social_connection_quality <= 0.55) s += 22; else if (u.social_connection_quality <= 0.70) s += 8;
  if      (u.community_belonging_index <= 0.35) s += 35; else if (u.community_belonging_index <= 0.55) s += 18; else if (u.community_belonging_index <= 0.70) s += 6;
  if      (u.work_life_integration_score <= 0.35) s += 25; else if (u.work_life_integration_score <= 0.55) s += 12;
  return Math.min(s, 100);
}
function composite(bn: number, sf: number, mn: number, cn: number): number {
  return Math.min(Math.round((bn * 0.30 + sf * 0.25 + mn * 0.25 + cn * 0.20) * 100) / 100, 100);
}
function emotionalPattern(u: Unit): string {
  if (u.burnout_prevalence_rate >= 0.60 || u.emotional_exhaustion_index >= 0.65) return "burnout_crisis";
  if (u.meaning_alignment_score <= 0.35 || u.purpose_clarity_score <= 0.30)      return "meaning_collapse";
  if (u.social_connection_quality <= 0.35 || u.community_belonging_index <= 0.30) return "isolation_epidemic";
  if (u.psychological_safety_score <= 0.35 || u.leadership_empathy_score <= 0.30) return "safety_erosion";
  if (u.joy_at_work_index <= 0.30 && u.resilience_capital_score <= 0.40)          return "joy_deficit";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "crisis"; if (c >= 40) return "depleted"; if (c >= 20) return "recovering"; return "flourishing"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "burnout_crisis") return "burnout_intervention";
    return "emergency_wellbeing";
  }
  if (r === "high") {
    if (p === "meaning_collapse" || p === "joy_deficit") return "meaning_restoration";
    return "connection_program";
  }
  if (r === "moderate") return "wellbeing_monitoring";
  return "no_action";
}
function signal(u: Unit, pat: string, comp: number): string {
  if (comp < 20) return "Capital émotionnel florissant — bien-être optimal, sécurité psychologique forte, sens et connexion préservés";
  const labels: Record<string, string> = {
    burnout_crisis:     "Crise de burnout",
    meaning_collapse:   "Effondrement du sens",
    isolation_epidemic: "Épidémie d'isolement",
    safety_erosion:     "Érosion de la sécurité",
    joy_deficit:        "Déficit de joie au travail",
  };
  const label = labels[pat] ?? pat.replace(/_/g, " ");
  return `${label} — burnout ${Math.round(u.burnout_prevalence_rate * 100)}% — épuisement ${Math.round(u.emotional_exhaustion_index * 100)}% — sécurité psy. ${Math.round(u.psychological_safety_score * 100)}% — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[emotional-capital-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tbn=0, tsf=0, tmn=0, tcn=0, tcomp=0, trisk=0, alertC=0, emergC=0;
    for (const u of units) {
      rc[u.wellbeing_risk]     = (rc[u.wellbeing_risk]     || 0) + 1;
      pc[u.emotional_pattern]  = (pc[u.emotional_pattern]  || 0) + 1;
      sc[u.wellbeing_severity] = (sc[u.wellbeing_severity] || 0) + 1;
      ac[u.recommended_action] = (ac[u.recommended_action] || 0) + 1;
      tbn += u.burnout_score; tsf += u.safety_score; tmn += u.meaning_score; tcn += u.connection_score;
      tcomp += u.emotional_composite; trisk += u.estimated_burnout_risk_index;
      if (u.has_burnout_alert)          alertC++;
      if (u.requires_emergency_support) emergC++;
    }
    const n = units.length;
    return sealResponse(NextResponse.json(sealResponse({ units, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_emotional_composite:          Math.round(tcomp / n * 10) / 10,
      burnout_alert_count:              alertC,
      emergency_support_count:          emergC,
      avg_burnout_score:                Math.round(tbn  / n * 10) / 10,
      avg_safety_score:                 Math.round(tsf  / n * 10) / 10,
      avg_meaning_score:                Math.round(tmn  / n * 10) / 10,
      avg_connection_score:             Math.round(tcn  / n * 10) / 10,
      avg_estimated_burnout_risk_index: Math.round(trisk / n * 100) / 100,
    }} as Record<string,unknown>)));
  }
  return sealResponse(NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/emotional-capital-engine`, { next: { revalidate: 30 } })).json()));
}
