import { NextResponse } from "next/server";

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json({ error: "SWARM_API_URL not configured" }, { status: 503 });
  }
  return NextResponse.json({ reps: MOCK_REPS, summary: buildSummary(MOCK_REPS) });
}

const MOCK_REPS = [
  { rep_id:"R001", region:"EMEA",  coach_risk:"critical",  coach_pattern:"passive_resistor",   coach_severity:"unreachable",  recommended_action:"leadership_intervention",          receptivity_score:88, implementation_score:90, engagement_score:85, improvement_score:82, coach_composite:87.3, has_coach_gap:true,  requires_coach_intervention:true,  estimated_coaching_waste_usd:8500,  coach_signal:"Passive resistor — 15% feedback implemented — 35% sessions attended — 70% habit reversion rate — composite 87" },
  { rep_id:"R002", region:"APAC",  coach_risk:"critical",  coach_pattern:"active_deflector",   coach_severity:"unreachable",  recommended_action:"leadership_intervention",          receptivity_score:75, implementation_score:78, engagement_score:70, improvement_score:68, coach_composite:73.9, has_coach_gap:true,  requires_coach_intervention:true,  estimated_coaching_waste_usd:6800,  coach_signal:"Active deflector — 22% feedback implemented — 55% sessions attended — 60% habit reversion rate — composite 74" },
  { rep_id:"R003", region:"NOAM",  coach_risk:"high",      coach_pattern:"habit_reverter",     coach_severity:"resistant",    recommended_action:"structured_feedback_plan",         receptivity_score:55, implementation_score:58, engagement_score:50, improvement_score:45, coach_composite:53.4, has_coach_gap:true,  requires_coach_intervention:true,  estimated_coaching_waste_usd:3800,  coach_signal:"Habit reverter — 60% feedback implemented — 75% sessions attended — 55% habit reversion rate — composite 53" },
  { rep_id:"R004", region:"LATAM", coach_risk:"high",      coach_pattern:"selective_listener", coach_severity:"resistant",    recommended_action:"structured_feedback_plan",         receptivity_score:48, implementation_score:44, engagement_score:42, improvement_score:40, coach_composite:44.6, has_coach_gap:true,  requires_coach_intervention:true,  estimated_coaching_waste_usd:2900,  coach_signal:"Selective listener — 45% feedback implemented — 80% sessions attended — 40% habit reversion rate — composite 45" },
  { rep_id:"R005", region:"EMEA",  coach_risk:"moderate",  coach_pattern:"ghost_committor",    coach_severity:"developing",   recommended_action:"coaching_check_in",               receptivity_score:28, implementation_score:25, engagement_score:22, improvement_score:20, coach_composite:24.1, has_coach_gap:true,  requires_coach_intervention:true,  estimated_coaching_waste_usd:1200,  coach_signal:"Ghost committor — 38% feedback implemented — 65% sessions attended — 32% habit reversion rate — composite 24" },
  { rep_id:"R006", region:"APAC",  coach_risk:"low",       coach_pattern:"none",               coach_severity:"receptive",    recommended_action:"no_action",                       receptivity_score:8,  implementation_score:6,  engagement_score:5,  improvement_score:4,  coach_composite:5.9,  has_coach_gap:false, requires_coach_intervention:false, estimated_coaching_waste_usd:0,     coach_signal:"Coaching receptivity strong — implementation rate, engagement, action items, and skill improvement within benchmarks" },
  { rep_id:"R007", region:"NOAM",  coach_risk:"high",      coach_pattern:"passive_resistor",   coach_severity:"resistant",    recommended_action:"manager_escalation",              receptivity_score:60, implementation_score:62, engagement_score:55, improvement_score:52, coach_composite:58.1, has_coach_gap:true,  requires_coach_intervention:true,  estimated_coaching_waste_usd:4500,  coach_signal:"Passive resistor — 28% feedback implemented — 45% sessions attended — 55% habit reversion rate — composite 58" },
  { rep_id:"R008", region:"LATAM", coach_risk:"low",       coach_pattern:"none",               coach_severity:"receptive",    recommended_action:"no_action",                       receptivity_score:5,  implementation_score:4,  engagement_score:6,  improvement_score:3,  coach_composite:4.5,  has_coach_gap:false, requires_coach_intervention:false, estimated_coaching_waste_usd:0,     coach_signal:"Coaching receptivity strong — all metrics within benchmarks" },
];

function buildSummary(reps: typeof MOCK_REPS) {
  const risk_counts:     Record<string,number> = {};
  const pattern_counts:  Record<string,number> = {};
  const severity_counts: Record<string,number> = {};
  const action_counts:   Record<string,number> = {};
  let comp=0, re=0, im=0, en=0, ip=0, cw=0, gap=0, intv=0;
  for (const r of reps) {
    risk_counts[r.coach_risk]         = (risk_counts[r.coach_risk]||0)+1;
    pattern_counts[r.coach_pattern]   = (pattern_counts[r.coach_pattern]||0)+1;
    severity_counts[r.coach_severity] = (severity_counts[r.coach_severity]||0)+1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action]||0)+1;
    comp+=r.coach_composite; re+=r.receptivity_score; im+=r.implementation_score;
    en+=r.engagement_score; ip+=r.improvement_score;
    cw+=r.estimated_coaching_waste_usd;
    if (r.has_coach_gap)              gap++;
    if (r.requires_coach_intervention) intv++;
  }
  const n = reps.length;
  return {
    total: n, risk_counts, pattern_counts, severity_counts, action_counts,
    avg_coach_composite:                    Math.round(comp/n*10)/10,
    coach_gap_count:                        gap,
    intervention_count:                     intv,
    avg_receptivity_score:                  Math.round(re/n*10)/10,
    avg_implementation_score:               Math.round(im/n*10)/10,
    avg_engagement_score:                   Math.round(en/n*10)/10,
    avg_improvement_score:                  Math.round(ip/n*10)/10,
    total_estimated_coaching_waste_usd:     Math.round(cw*100)/100,
  };
}
