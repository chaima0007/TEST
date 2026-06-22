import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"RV-001", region:"EMEA",  cohort_id:"Q1-2026", weeks_since_start:16, expected_ramp_weeks:24, quota_attainment_at_ramp_pct:0.15, weeks_to_first_deal:14, outbound_activity_vs_benchmark_pct:0.28, meetings_booked_vs_benchmark_pct:0.25, pipeline_created_vs_benchmark_pct:0.20, deals_in_stage_3plus_vs_benchmark_pct:0.10, product_certification_completion_pct:0.38, sales_playbook_completion_pct:0.32, call_shadowing_hours_completed:4.0, manager_coaching_sessions_completed:2, onboarding_portal_activity_score:0.22, peer_collaboration_rate_pct:0.18, voluntary_extra_training_pct:0.08, win_rate_vs_cohort_avg:0.45, avg_deal_size_vs_cohort_avg:0.60, total_deals_attempted:8, avg_deal_value_usd:85000 },
  { rep_id:"RV-002", region:"NAMER", cohort_id:"Q1-2026", weeks_since_start:12, expected_ramp_weeks:20, quota_attainment_at_ramp_pct:0.65, weeks_to_first_deal:5, outbound_activity_vs_benchmark_pct:0.92, meetings_booked_vs_benchmark_pct:0.88, pipeline_created_vs_benchmark_pct:0.85, deals_in_stage_3plus_vs_benchmark_pct:0.80, product_certification_completion_pct:0.95, sales_playbook_completion_pct:0.90, call_shadowing_hours_completed:18.0, manager_coaching_sessions_completed:10, onboarding_portal_activity_score:0.88, peer_collaboration_rate_pct:0.82, voluntary_extra_training_pct:0.65, win_rate_vs_cohort_avg:1.25, avg_deal_size_vs_cohort_avg:1.10, total_deals_attempted:18, avg_deal_value_usd:110000 },
  { rep_id:"RV-003", region:"APAC",  cohort_id:"Q1-2026", weeks_since_start:18, expected_ramp_weeks:24, quota_attainment_at_ramp_pct:0.35, weeks_to_first_deal:10, outbound_activity_vs_benchmark_pct:0.52, meetings_booked_vs_benchmark_pct:0.48, pipeline_created_vs_benchmark_pct:0.42, deals_in_stage_3plus_vs_benchmark_pct:0.35, product_certification_completion_pct:0.62, sales_playbook_completion_pct:0.58, call_shadowing_hours_completed:10.0, manager_coaching_sessions_completed:6, onboarding_portal_activity_score:0.52, peer_collaboration_rate_pct:0.45, voluntary_extra_training_pct:0.28, win_rate_vs_cohort_avg:0.85, avg_deal_size_vs_cohort_avg:0.90, total_deals_attempted:12, avg_deal_value_usd:72000 },
  { rep_id:"RV-004", region:"LATAM", cohort_id:"Q1-2026", weeks_since_start:8, expected_ramp_weeks:20, quota_attainment_at_ramp_pct:0.42, weeks_to_first_deal:4, outbound_activity_vs_benchmark_pct:0.85, meetings_booked_vs_benchmark_pct:0.80, pipeline_created_vs_benchmark_pct:0.78, deals_in_stage_3plus_vs_benchmark_pct:0.72, product_certification_completion_pct:0.88, sales_playbook_completion_pct:0.82, call_shadowing_hours_completed:15.0, manager_coaching_sessions_completed:8, onboarding_portal_activity_score:0.80, peer_collaboration_rate_pct:0.75, voluntary_extra_training_pct:0.55, win_rate_vs_cohort_avg:1.05, avg_deal_size_vs_cohort_avg:0.95, total_deals_attempted:10, avg_deal_value_usd:62000 },
  { rep_id:"RV-005", region:"EMEA",  cohort_id:"Q1-2026", weeks_since_start:20, expected_ramp_weeks:24, quota_attainment_at_ramp_pct:0.08, weeks_to_first_deal:18, outbound_activity_vs_benchmark_pct:0.18, meetings_booked_vs_benchmark_pct:0.15, pipeline_created_vs_benchmark_pct:0.12, deals_in_stage_3plus_vs_benchmark_pct:0.05, product_certification_completion_pct:0.25, sales_playbook_completion_pct:0.22, call_shadowing_hours_completed:2.0, manager_coaching_sessions_completed:1, onboarding_portal_activity_score:0.12, peer_collaboration_rate_pct:0.10, voluntary_extra_training_pct:0.02, win_rate_vs_cohort_avg:0.20, avg_deal_size_vs_cohort_avg:0.40, total_deals_attempted:3, avg_deal_value_usd:90000 },
  { rep_id:"RV-006", region:"NAMER", cohort_id:"Q1-2026", weeks_since_start:14, expected_ramp_weeks:20, quota_attainment_at_ramp_pct:0.50, weeks_to_first_deal:7, outbound_activity_vs_benchmark_pct:0.70, meetings_booked_vs_benchmark_pct:0.65, pipeline_created_vs_benchmark_pct:0.62, deals_in_stage_3plus_vs_benchmark_pct:0.55, product_certification_completion_pct:0.78, sales_playbook_completion_pct:0.72, call_shadowing_hours_completed:12.0, manager_coaching_sessions_completed:7, onboarding_portal_activity_score:0.68, peer_collaboration_rate_pct:0.60, voluntary_extra_training_pct:0.40, win_rate_vs_cohort_avg:0.95, avg_deal_size_vs_cohort_avg:1.00, total_deals_attempted:14, avg_deal_value_usd:92000 },
  { rep_id:"RV-007", region:"APAC",  cohort_id:"Q1-2026", weeks_since_start:16, expected_ramp_weeks:24, quota_attainment_at_ramp_pct:0.60, weeks_to_first_deal:8, outbound_activity_vs_benchmark_pct:0.62, meetings_booked_vs_benchmark_pct:0.58, pipeline_created_vs_benchmark_pct:0.55, deals_in_stage_3plus_vs_benchmark_pct:0.22, product_certification_completion_pct:0.72, sales_playbook_completion_pct:0.68, call_shadowing_hours_completed:11.0, manager_coaching_sessions_completed:6, onboarding_portal_activity_score:0.60, peer_collaboration_rate_pct:0.55, voluntary_extra_training_pct:0.35, win_rate_vs_cohort_avg:0.90, avg_deal_size_vs_cohort_avg:0.85, total_deals_attempted:11, avg_deal_value_usd:78000 },
  { rep_id:"RV-008", region:"MEA",   cohort_id:"Q1-2026", weeks_since_start:10, expected_ramp_weeks:20, quota_attainment_at_ramp_pct:0.28, weeks_to_first_deal:8, outbound_activity_vs_benchmark_pct:0.42, meetings_booked_vs_benchmark_pct:0.38, pipeline_created_vs_benchmark_pct:0.35, deals_in_stage_3plus_vs_benchmark_pct:0.28, product_certification_completion_pct:0.52, sales_playbook_completion_pct:0.48, call_shadowing_hours_completed:7.0, manager_coaching_sessions_completed:4, onboarding_portal_activity_score:0.42, peer_collaboration_rate_pct:0.35, voluntary_extra_training_pct:0.18, win_rate_vs_cohort_avg:0.70, avg_deal_size_vs_cohort_avg:0.80, total_deals_attempted:8, avg_deal_value_usd:68000 },
];

type Rep = typeof MOCK_REPS[0];

function velocityScore(i: Rep): number {
  let s = 0;
  const rampProgress = i.weeks_since_start / Math.max(i.expected_ramp_weeks, 1);
  const quotaGap = Math.max(0, rampProgress - i.quota_attainment_at_ramp_pct);
  if      (quotaGap >= 0.50) s += 40; else if (quotaGap >= 0.30) s += 22; else if (quotaGap >= 0.15) s += 8;
  const firstDealThresh70 = Math.floor(i.expected_ramp_weeks * 0.70);
  const firstDealThresh45 = Math.floor(i.expected_ramp_weeks * 0.45);
  if      (i.weeks_to_first_deal >= firstDealThresh70) s += 35; else if (i.weeks_to_first_deal >= firstDealThresh45) s += 18;
  if      (i.pipeline_created_vs_benchmark_pct <= 0.30) s += 25; else if (i.pipeline_created_vs_benchmark_pct <= 0.55) s += 12;
  return Math.min(s, 100);
}
function readinessScore(i: Rep): number {
  let s = 0;
  if      (i.product_certification_completion_pct <= 0.40) s += 40; else if (i.product_certification_completion_pct <= 0.65) s += 22; else if (i.product_certification_completion_pct <= 0.80) s += 8;
  if      (i.sales_playbook_completion_pct        <= 0.35) s += 35; else if (i.sales_playbook_completion_pct <= 0.60) s += 18;
  if      (i.manager_coaching_sessions_completed  <= 2)    s += 25; else if (i.manager_coaching_sessions_completed <= 5) s += 12;
  return Math.min(s, 100);
}
function activityScore(i: Rep): number {
  let s = 0;
  if      (i.outbound_activity_vs_benchmark_pct    <= 0.30) s += 45; else if (i.outbound_activity_vs_benchmark_pct <= 0.55) s += 25; else if (i.outbound_activity_vs_benchmark_pct <= 0.75) s += 10;
  if      (i.meetings_booked_vs_benchmark_pct      <= 0.30) s += 30; else if (i.meetings_booked_vs_benchmark_pct <= 0.55) s += 15;
  if      (i.deals_in_stage_3plus_vs_benchmark_pct <= 0.20) s += 25; else if (i.deals_in_stage_3plus_vs_benchmark_pct <= 0.45) s += 12;
  return Math.min(s, 100);
}
function engagementScore(i: Rep): number {
  let s = 0;
  if      (i.onboarding_portal_activity_score <= 0.25) s += 40; else if (i.onboarding_portal_activity_score <= 0.50) s += 22; else if (i.onboarding_portal_activity_score <= 0.70) s += 8;
  if      (i.peer_collaboration_rate_pct      <= 0.20) s += 35; else if (i.peer_collaboration_rate_pct <= 0.45) s += 18;
  if      (i.voluntary_extra_training_pct     <= 0.10) s += 25; else if (i.voluntary_extra_training_pct <= 0.30) s += 12;
  return Math.min(s, 100);
}
function composite(ve: number, re: number, ac: number, en: number): number {
  return Math.min(Math.round((ve * 0.30 + re * 0.25 + ac * 0.25 + en * 0.20) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  const rampProgress = i.weeks_since_start / Math.max(i.expected_ramp_weeks, 1);
  const quotaGap = Math.max(0, rampProgress - i.quota_attainment_at_ramp_pct);
  if (quotaGap >= 0.40 && i.pipeline_created_vs_benchmark_pct <= 0.40)                              return "stalled_ramp";
  if (i.quota_attainment_at_ramp_pct >= 0.55 && i.deals_in_stage_3plus_vs_benchmark_pct <= 0.30)   return "plateau_trap";
  if (i.product_certification_completion_pct <= 0.50 && i.sales_playbook_completion_pct <= 0.50)    return "knowledge_gap";
  if (i.outbound_activity_vs_benchmark_pct <= 0.40 && i.meetings_booked_vs_benchmark_pct <= 0.40)  return "activity_laggard";
  if (i.pipeline_created_vs_benchmark_pct <= 0.35 && i.deals_in_stage_3plus_vs_benchmark_pct <= 0.25) return "pipeline_void";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "failed"; if (c >= 40) return "stalled"; if (c >= 20) return "at_risk"; return "on_track"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "stalled_ramp" || p === "pipeline_void") return "early_exit_assessment"; return "ramp_plan_reset"; }
  if (r === "high") {
    if (p === "stalled_ramp")     return "manager_ramp_intervention";
    if (p === "plateau_trap")     return "territory_assignment_review";
    if (p === "knowledge_gap")    return "skills_gap_coaching";
    if (p === "activity_laggard") return "enablement_acceleration";
    if (p === "pipeline_void")    return "pipeline_building_support";
    return "ramp_monitoring";
  }
  if (r === "moderate") return "ramp_monitoring";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Rep ramp on track — velocity, readiness, activity, and engagement within expected benchmarks";
  const labels: Record<string,string> = { stalled_ramp:"Stalled ramp", plateau_trap:"Plateau trap", knowledge_gap:"Knowledge gap", activity_laggard:"Activity laggard", pipeline_void:"Pipeline void" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  const rampPct = Math.round(i.weeks_since_start / Math.max(i.expected_ramp_weeks, 1) * 100);
  return `${label} — ${rampPct}% ramp elapsed — ${Math.round(i.quota_attainment_at_ramp_pct*100)}% quota attained — ${Math.round(i.pipeline_created_vs_benchmark_pct*100)}% pipeline benchmark — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[sales-onboarding-ramp-velocity-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tve=0,tre=0,tac=0,ten=0,tcomp=0,tdel=0,gc=0,ic=0;
    for (const r of reps) {
      rc[r.ramp_risk]=(rc[r.ramp_risk]||0)+1; pc[r.ramp_pattern]=(pc[r.ramp_pattern]||0)+1;
      sc[r.ramp_severity]=(sc[r.ramp_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      tve+=r.velocity_score; tre+=r.readiness_score; tac+=r.activity_score; ten+=r.engagement_score;
      tcomp+=r.ramp_composite; tdel+=r.estimated_ramp_delay_weeks;
      if (r.has_ramp_gap) gc++; if (r.requires_intervention) ic++;
    }
    const n = reps.length;
    return sealResponse(NextResponse.json(sealResponse({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_ramp_composite: Math.round(tcomp/n*10)/10,
      ramp_gap_count: gc, intervention_count: ic,
      avg_velocity_score: Math.round(tve/n*10)/10,
      avg_readiness_score: Math.round(tre/n*10)/10,
      avg_activity_score: Math.round(tac/n*10)/10,
      avg_engagement_score: Math.round(ten/n*10)/10,
      avg_estimated_ramp_delay_weeks: Math.round(tdel/n*10)/10,
    }} as Record<string,unknown>)));
  }
  return sealResponse(NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-onboarding-ramp-velocity-engine`, { next: { revalidate: 30 } })).json()));
}
