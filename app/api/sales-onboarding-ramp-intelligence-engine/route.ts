import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"OR-001", region:"EMEA",  evaluation_period_id:"Q2-2026", weeks_since_start:10, quota_attainment_vs_ramp_plan_pct:0.15, first_meeting_booked_days:25, first_opportunity_created_days:38, product_certification_completion_pct:0.22, training_module_completion_pct:0.28, call_shadowing_sessions_completed:1, manager_1on1_frequency_per_month:0.8, pipeline_coverage_ratio:0.8, avg_deal_size_vs_team_avg_pct:0.55, outbound_activity_vs_plan_pct:0.32, discovery_call_pass_rate_pct:0.18, demo_to_next_step_rate_pct:0.20, competitive_win_rate_ramp_pct:0.10, peer_buddy_engagement_score:0.15, onboarding_satisfaction_score:0.28, net_promoter_internal_score:0.25, tool_adoption_rate_pct:0.35, avg_deal_value_usd:80000 },
  { rep_id:"OR-002", region:"APAC",  evaluation_period_id:"Q2-2026", weeks_since_start:12, quota_attainment_vs_ramp_plan_pct:0.88, first_meeting_booked_days:5, first_opportunity_created_days:8, product_certification_completion_pct:0.95, training_module_completion_pct:0.92, call_shadowing_sessions_completed:8, manager_1on1_frequency_per_month:4.5, pipeline_coverage_ratio:4.2, avg_deal_size_vs_team_avg_pct:1.05, outbound_activity_vs_plan_pct:0.92, discovery_call_pass_rate_pct:0.78, demo_to_next_step_rate_pct:0.72, competitive_win_rate_ramp_pct:0.55, peer_buddy_engagement_score:0.88, onboarding_satisfaction_score:0.92, net_promoter_internal_score:0.88, tool_adoption_rate_pct:0.95, avg_deal_value_usd:65000 },
  { rep_id:"OR-003", region:"NAMER", evaluation_period_id:"Q2-2026", weeks_since_start:8, quota_attainment_vs_ramp_plan_pct:0.52, first_meeting_booked_days:12, first_opportunity_created_days:18, product_certification_completion_pct:0.62, training_module_completion_pct:0.58, call_shadowing_sessions_completed:4, manager_1on1_frequency_per_month:2.5, pipeline_coverage_ratio:2.2, avg_deal_size_vs_team_avg_pct:0.88, outbound_activity_vs_plan_pct:0.65, discovery_call_pass_rate_pct:0.48, demo_to_next_step_rate_pct:0.45, competitive_win_rate_ramp_pct:0.32, peer_buddy_engagement_score:0.55, onboarding_satisfaction_score:0.62, net_promoter_internal_score:0.58, tool_adoption_rate_pct:0.72, avg_deal_value_usd:72000 },
  { rep_id:"OR-004", region:"LATAM", evaluation_period_id:"Q2-2026", weeks_since_start:14, quota_attainment_vs_ramp_plan_pct:0.22, first_meeting_booked_days:22, first_opportunity_created_days:35, product_certification_completion_pct:0.35, training_module_completion_pct:0.32, call_shadowing_sessions_completed:2, manager_1on1_frequency_per_month:0.5, pipeline_coverage_ratio:0.6, avg_deal_size_vs_team_avg_pct:0.62, outbound_activity_vs_plan_pct:0.42, discovery_call_pass_rate_pct:0.22, demo_to_next_step_rate_pct:0.18, competitive_win_rate_ramp_pct:0.12, peer_buddy_engagement_score:0.18, onboarding_satisfaction_score:0.30, net_promoter_internal_score:0.28, tool_adoption_rate_pct:0.42, avg_deal_value_usd:88000 },
  { rep_id:"OR-005", region:"EMEA",  evaluation_period_id:"Q2-2026", weeks_since_start:6, quota_attainment_vs_ramp_plan_pct:0.72, first_meeting_booked_days:7, first_opportunity_created_days:12, product_certification_completion_pct:0.82, training_module_completion_pct:0.78, call_shadowing_sessions_completed:6, manager_1on1_frequency_per_month:3.8, pipeline_coverage_ratio:3.5, avg_deal_size_vs_team_avg_pct:0.95, outbound_activity_vs_plan_pct:0.82, discovery_call_pass_rate_pct:0.65, demo_to_next_step_rate_pct:0.60, competitive_win_rate_ramp_pct:0.42, peer_buddy_engagement_score:0.75, onboarding_satisfaction_score:0.82, net_promoter_internal_score:0.78, tool_adoption_rate_pct:0.88, avg_deal_value_usd:92000 },
  { rep_id:"OR-006", region:"MEA",   evaluation_period_id:"Q2-2026", weeks_since_start:16, quota_attainment_vs_ramp_plan_pct:0.08, first_meeting_booked_days:32, first_opportunity_created_days:48, product_certification_completion_pct:0.15, training_module_completion_pct:0.18, call_shadowing_sessions_completed:0, manager_1on1_frequency_per_month:0.3, pipeline_coverage_ratio:0.3, avg_deal_size_vs_team_avg_pct:0.42, outbound_activity_vs_plan_pct:0.18, discovery_call_pass_rate_pct:0.10, demo_to_next_step_rate_pct:0.08, competitive_win_rate_ramp_pct:0.05, peer_buddy_engagement_score:0.05, onboarding_satisfaction_score:0.15, net_promoter_internal_score:0.12, tool_adoption_rate_pct:0.22, avg_deal_value_usd:55000 },
  { rep_id:"OR-007", region:"APAC",  evaluation_period_id:"Q2-2026", weeks_since_start:9, quota_attainment_vs_ramp_plan_pct:0.62, first_meeting_booked_days:9, first_opportunity_created_days:14, product_certification_completion_pct:0.72, training_module_completion_pct:0.68, call_shadowing_sessions_completed:5, manager_1on1_frequency_per_month:3.2, pipeline_coverage_ratio:2.8, avg_deal_size_vs_team_avg_pct:0.92, outbound_activity_vs_plan_pct:0.72, discovery_call_pass_rate_pct:0.55, demo_to_next_step_rate_pct:0.52, competitive_win_rate_ramp_pct:0.38, peer_buddy_engagement_score:0.65, onboarding_satisfaction_score:0.72, net_promoter_internal_score:0.68, tool_adoption_rate_pct:0.80, avg_deal_value_usd:68000 },
  { rep_id:"OR-008", region:"NAMER", evaluation_period_id:"Q2-2026", weeks_since_start:11, quota_attainment_vs_ramp_plan_pct:0.35, first_meeting_booked_days:18, first_opportunity_created_days:28, product_certification_completion_pct:0.48, training_module_completion_pct:0.45, call_shadowing_sessions_completed:3, manager_1on1_frequency_per_month:1.5, pipeline_coverage_ratio:1.5, avg_deal_size_vs_team_avg_pct:0.72, outbound_activity_vs_plan_pct:0.55, discovery_call_pass_rate_pct:0.35, demo_to_next_step_rate_pct:0.32, competitive_win_rate_ramp_pct:0.22, peer_buddy_engagement_score:0.38, onboarding_satisfaction_score:0.48, net_promoter_internal_score:0.42, tool_adoption_rate_pct:0.58, avg_deal_value_usd:75000 },
];

type Rep = typeof MOCK_REPS[0];

function readinessScore(i: Rep): number {
  let s = 0;
  if      (i.product_certification_completion_pct <= 0.30) s += 40; else if (i.product_certification_completion_pct <= 0.60) s += 22; else if (i.product_certification_completion_pct <= 0.80) s += 8;
  if      (i.training_module_completion_pct       <= 0.30) s += 35; else if (i.training_module_completion_pct <= 0.60) s += 18;
  if      (i.tool_adoption_rate_pct               <= 0.30) s += 25; else if (i.tool_adoption_rate_pct <= 0.60) s += 12;
  return Math.min(s, 100);
}
function activityScore(i: Rep): number {
  let s = 0;
  if      (i.outbound_activity_vs_plan_pct  <= 0.40) s += 45; else if (i.outbound_activity_vs_plan_pct <= 0.65) s += 25; else if (i.outbound_activity_vs_plan_pct <= 0.85) s += 10;
  if      (i.first_meeting_booked_days      >= 21)   s += 30; else if (i.first_meeting_booked_days >= 12) s += 15;
  if      (i.discovery_call_pass_rate_pct   <= 0.25) s += 25; else if (i.discovery_call_pass_rate_pct <= 0.50) s += 12;
  return Math.min(s, 100);
}
function pipelineScore(i: Rep): number {
  let s = 0;
  if      (i.quota_attainment_vs_ramp_plan_pct <= 0.30) s += 40; else if (i.quota_attainment_vs_ramp_plan_pct <= 0.60) s += 22; else if (i.quota_attainment_vs_ramp_plan_pct <= 0.85) s += 8;
  if      (i.pipeline_coverage_ratio           <= 1.0)  s += 35; else if (i.pipeline_coverage_ratio <= 2.0) s += 18;
  if      (i.first_opportunity_created_days    >= 30)   s += 25; else if (i.first_opportunity_created_days >= 18) s += 12;
  return Math.min(s, 100);
}
function managerSupportScore(i: Rep): number {
  let s = 0;
  if      (i.manager_1on1_frequency_per_month    <= 1.0) s += 45; else if (i.manager_1on1_frequency_per_month <= 2.0) s += 25; else if (i.manager_1on1_frequency_per_month <= 3.0) s += 10;
  if      (i.call_shadowing_sessions_completed   <= 1)   s += 30; else if (i.call_shadowing_sessions_completed <= 3) s += 15;
  if      (i.peer_buddy_engagement_score         <= 0.20) s += 25; else if (i.peer_buddy_engagement_score <= 0.50) s += 12;
  return Math.min(s, 100);
}
function composite(re: number, ac: number, pi: number, ms: number): number {
  return Math.min(Math.round((re * 0.25 + ac * 0.30 + pi * 0.30 + ms * 0.15) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.outbound_activity_vs_plan_pct <= 0.40 && i.first_meeting_booked_days >= 21) return "slow_starter";
  if (i.product_certification_completion_pct <= 0.40 && i.training_module_completion_pct <= 0.40) return "knowledge_gap_blocker";
  if (i.pipeline_coverage_ratio <= 1.0 && i.quota_attainment_vs_ramp_plan_pct <= 0.40) return "pipeline_builder_fail";
  if (i.manager_1on1_frequency_per_month <= 1.0 && i.call_shadowing_sessions_completed <= 2) return "manager_orphan";
  if (i.onboarding_satisfaction_score <= 0.35 && i.net_promoter_internal_score <= 0.35) return "confidence_collapse";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "behind"; if (c >= 20) return "at_risk"; return "on_track"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "pipeline_builder_fail" || p === "slow_starter") return "ramp_extension_or_reset"; return "structured_ramp_acceleration"; }
  if (r === "high") { if (p === "slow_starter") return "pipeline_building_coaching"; if (p === "knowledge_gap_blocker") return "product_knowledge_coaching"; if (p === "pipeline_builder_fail") return "pipeline_building_coaching"; if (p === "manager_orphan") return "manager_engagement_review"; if (p === "confidence_collapse") return "structured_ramp_acceleration"; return "pipeline_building_coaching"; }
  if (r === "moderate") return "ramp_check_in";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Ramp trajectory healthy — activity, pipeline coverage, and product readiness within plan benchmarks";
  const labels: Record<string,string> = { slow_starter:"Slow starter", knowledge_gap_blocker:"Knowledge-gap blocker", pipeline_builder_fail:"Pipeline-builder fail", manager_orphan:"Manager orphan", confidence_collapse:"Confidence collapse" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(i.quota_attainment_vs_ramp_plan_pct*100)}% ramp attainment — ${Math.round(i.outbound_activity_vs_plan_pct*100)}% activity vs plan — ${Math.round(i.product_certification_completion_pct*100)}% certs complete — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(i => {
      const re = readinessScore(i), ac = activityScore(i), pi = pipelineScore(i), ms = managerSupportScore(i);
      const comp = composite(re, ac, pi, ms), pat = pattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      const rampQuota = i.avg_deal_value_usd * 4;
      const rr = Math.round(rampQuota * Math.max(0, 1 - i.quota_attainment_vs_ramp_plan_pct) * (comp/100) * 100) / 100;
      return {
        rep_id: i.rep_id, region: i.region,
        ramp_risk: r, ramp_pattern: pat, ramp_severity: sev, recommended_action: act,
        readiness_score: re, activity_score: ac, pipeline_score: pi, manager_support_score: ms,
        ramp_composite: comp,
        has_ramp_gap: comp >= 40 || i.quota_attainment_vs_ramp_plan_pct <= 0.60 || i.pipeline_coverage_ratio <= 2.0,
        requires_ramp_intervention: comp >= 25 || i.outbound_activity_vs_plan_pct <= 0.65 || i.product_certification_completion_pct <= 0.60,
        estimated_ramp_revenue_risk_usd: rr,
        ramp_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tre=0, tac=0, tpi=0, tms=0, tcomp=0, trr=0, gc=0, ic=0;
    for (const r of reps) {
      rc[r.ramp_risk]=(rc[r.ramp_risk]||0)+1; pc[r.ramp_pattern]=(pc[r.ramp_pattern]||0)+1;
      sc[r.ramp_severity]=(sc[r.ramp_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      tre+=r.readiness_score; tac+=r.activity_score; tpi+=r.pipeline_score; tms+=r.manager_support_score;
      tcomp+=r.ramp_composite; trr+=r.estimated_ramp_revenue_risk_usd;
      if (r.has_ramp_gap) gc++; if (r.requires_ramp_intervention) ic++;
    }
    const n = reps.length;
    return NextResponse.json(sealResponse({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_ramp_composite: Math.round(tcomp/n*10)/10,
      ramp_gap_count: gc, intervention_count: ic,
      avg_readiness_score: Math.round(tre/n*10)/10,
      avg_activity_score: Math.round(tac/n*10)/10,
      avg_pipeline_score: Math.round(tpi/n*10)/10,
      avg_manager_support_score: Math.round(tms/n*10)/10,
      total_estimated_ramp_revenue_risk_usd: Math.round(trr*100)/100,
    }} as Record<string,unknown>));
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-onboarding-ramp-intelligence-engine`)).json());
}
