import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"BR-001", region:"EMEA",  evaluation_period_id:"Q2-2026", activity_volume_trend_pct:-0.38, win_rate_trend_pct:-0.22, pipeline_creation_trend_pct:-0.28, avg_deal_size_trend_pct:-0.12, pto_utilization_rate_pct:0.05, unplanned_absence_days:6, overtime_hours_per_week:18, after_hours_activity_rate_pct:0.52, manager_satisfaction_score:0.22, peer_collaboration_score:0.28, recognition_received_count:0, voluntary_task_completion_pct:0.28, training_participation_pct:0.15, internal_mobility_applications:1, tenure_months:18, consecutive_quota_miss_streak:3, comp_plan_satisfaction_score:0.18, career_path_clarity_score:0.20, exit_interview_signals:1, team_attrition_exposure_pct:0.45 },
  { rep_id:"BR-002", region:"APAC",  evaluation_period_id:"Q2-2026", activity_volume_trend_pct:-0.08, win_rate_trend_pct:-0.30, pipeline_creation_trend_pct:-0.18, avg_deal_size_trend_pct:-0.05, pto_utilization_rate_pct:0.10, unplanned_absence_days:3, overtime_hours_per_week:14, after_hours_activity_rate_pct:0.38, manager_satisfaction_score:0.40, peer_collaboration_score:0.35, recognition_received_count:1, voluntary_task_completion_pct:0.55, training_participation_pct:0.38, internal_mobility_applications:0, tenure_months:30, consecutive_quota_miss_streak:2, comp_plan_satisfaction_score:0.35, career_path_clarity_score:0.40, exit_interview_signals:0, team_attrition_exposure_pct:0.28 },
  { rep_id:"BR-003", region:"NAMER", evaluation_period_id:"Q2-2026", activity_volume_trend_pct:0.12, win_rate_trend_pct:0.08, pipeline_creation_trend_pct:0.15, avg_deal_size_trend_pct:0.05, pto_utilization_rate_pct:0.55, unplanned_absence_days:0, overtime_hours_per_week:2, after_hours_activity_rate_pct:0.08, manager_satisfaction_score:0.88, peer_collaboration_score:0.85, recognition_received_count:5, voluntary_task_completion_pct:0.88, training_participation_pct:0.85, internal_mobility_applications:0, tenure_months:48, consecutive_quota_miss_streak:0, comp_plan_satisfaction_score:0.82, career_path_clarity_score:0.88, exit_interview_signals:0, team_attrition_exposure_pct:0.05 },
  { rep_id:"BR-004", region:"LATAM", evaluation_period_id:"Q2-2026", activity_volume_trend_pct:-0.22, win_rate_trend_pct:-0.15, pipeline_creation_trend_pct:-0.08, avg_deal_size_trend_pct:-0.10, pto_utilization_rate_pct:0.08, unplanned_absence_days:4, overtime_hours_per_week:22, after_hours_activity_rate_pct:0.60, manager_satisfaction_score:0.32, peer_collaboration_score:0.48, recognition_received_count:1, voluntary_task_completion_pct:0.42, training_participation_pct:0.28, internal_mobility_applications:0, tenure_months:12, consecutive_quota_miss_streak:2, comp_plan_satisfaction_score:0.28, career_path_clarity_score:0.30, exit_interview_signals:0, team_attrition_exposure_pct:0.38 },
  { rep_id:"BR-005", region:"EMEA",  evaluation_period_id:"Q2-2026", activity_volume_trend_pct:-0.45, win_rate_trend_pct:-0.35, pipeline_creation_trend_pct:-0.40, avg_deal_size_trend_pct:-0.20, pto_utilization_rate_pct:0.02, unplanned_absence_days:9, overtime_hours_per_week:28, after_hours_activity_rate_pct:0.72, manager_satisfaction_score:0.15, peer_collaboration_score:0.18, recognition_received_count:0, voluntary_task_completion_pct:0.15, training_participation_pct:0.08, internal_mobility_applications:2, tenure_months:22, consecutive_quota_miss_streak:4, comp_plan_satisfaction_score:0.12, career_path_clarity_score:0.15, exit_interview_signals:1, team_attrition_exposure_pct:0.60 },
  { rep_id:"BR-006", region:"MEA",   evaluation_period_id:"Q2-2026", activity_volume_trend_pct:0.05, win_rate_trend_pct:-0.05, pipeline_creation_trend_pct:0.02, avg_deal_size_trend_pct:0.00, pto_utilization_rate_pct:0.42, unplanned_absence_days:1, overtime_hours_per_week:5, after_hours_activity_rate_pct:0.18, manager_satisfaction_score:0.72, peer_collaboration_score:0.68, recognition_received_count:3, voluntary_task_completion_pct:0.72, training_participation_pct:0.65, internal_mobility_applications:0, tenure_months:36, consecutive_quota_miss_streak:1, comp_plan_satisfaction_score:0.65, career_path_clarity_score:0.70, exit_interview_signals:0, team_attrition_exposure_pct:0.12 },
  { rep_id:"BR-007", region:"APAC",  evaluation_period_id:"Q2-2026", activity_volume_trend_pct:-0.18, win_rate_trend_pct:-0.10, pipeline_creation_trend_pct:-0.12, avg_deal_size_trend_pct:-0.08, pto_utilization_rate_pct:0.18, unplanned_absence_days:2, overtime_hours_per_week:10, after_hours_activity_rate_pct:0.28, manager_satisfaction_score:0.55, peer_collaboration_score:0.52, recognition_received_count:2, voluntary_task_completion_pct:0.60, training_participation_pct:0.48, internal_mobility_applications:0, tenure_months:15, consecutive_quota_miss_streak:1, comp_plan_satisfaction_score:0.52, career_path_clarity_score:0.48, exit_interview_signals:0, team_attrition_exposure_pct:0.22 },
  { rep_id:"BR-008", region:"NAMER", evaluation_period_id:"Q2-2026", activity_volume_trend_pct:-0.28, win_rate_trend_pct:-0.18, pipeline_creation_trend_pct:-0.22, avg_deal_size_trend_pct:-0.15, pto_utilization_rate_pct:0.05, unplanned_absence_days:5, overtime_hours_per_week:16, after_hours_activity_rate_pct:0.42, manager_satisfaction_score:0.28, peer_collaboration_score:0.22, recognition_received_count:0, voluntary_task_completion_pct:0.35, training_participation_pct:0.22, internal_mobility_applications:1, tenure_months:28, consecutive_quota_miss_streak:3, comp_plan_satisfaction_score:0.22, career_path_clarity_score:0.28, exit_interview_signals:0, team_attrition_exposure_pct:0.48 },
];

function disScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.activity_volume_trend_pct     <= -0.30) s += 40;
  else if (inp.activity_volume_trend_pct     <= -0.15) s += 22;
  else if (inp.activity_volume_trend_pct     <= -0.05) s += 8;
  if      (inp.training_participation_pct    <= 0.25)  s += 35;
  else if (inp.training_participation_pct    <= 0.50)  s += 18;
  if      (inp.voluntary_task_completion_pct <= 0.40)  s += 25;
  else if (inp.voluntary_task_completion_pct <= 0.65)  s += 12;
  return Math.min(s, 100);
}
function fatScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.overtime_hours_per_week       >= 20)    s += 40;
  else if (inp.overtime_hours_per_week       >= 12)    s += 22;
  else if (inp.overtime_hours_per_week       >= 6)     s += 8;
  if      (inp.after_hours_activity_rate_pct >= 0.50)  s += 35;
  else if (inp.after_hours_activity_rate_pct >= 0.30)  s += 18;
  if      (inp.unplanned_absence_days        >= 5)     s += 25;
  else if (inp.unplanned_absence_days        >= 2)     s += 12;
  return Math.min(s, 100);
}
function sentScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.comp_plan_satisfaction_score  <= 0.30)  s += 40;
  else if (inp.comp_plan_satisfaction_score  <= 0.50)  s += 22;
  else if (inp.comp_plan_satisfaction_score  <= 0.70)  s += 8;
  if      (inp.career_path_clarity_score     <= 0.25)  s += 35;
  else if (inp.career_path_clarity_score     <= 0.50)  s += 18;
  if      (inp.manager_satisfaction_score    <= 0.30)  s += 25;
  else if (inp.manager_satisfaction_score    <= 0.50)  s += 12;
  return Math.min(s, 100);
}
function perfScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.win_rate_trend_pct            <= -0.25) s += 45;
  else if (inp.win_rate_trend_pct            <= -0.10) s += 25;
  else if (inp.win_rate_trend_pct            <= -0.03) s += 10;
  if      (inp.pipeline_creation_trend_pct   <= -0.25) s += 30;
  else if (inp.pipeline_creation_trend_pct   <= -0.10) s += 15;
  if      (inp.consecutive_quota_miss_streak >= 3)     s += 25;
  else if (inp.consecutive_quota_miss_streak >= 2)     s += 12;
  return Math.min(s, 100);
}
function composite(d: number, f: number, se: number, p: number): number {
  return Math.min(Math.round((d*0.30 + f*0.25 + se*0.30 + p*0.15)*100)/100, 100);
}
function pattern(inp: typeof MOCK_REPS[0]): string {
  if (inp.activity_volume_trend_pct <= -0.20 && inp.training_participation_pct <= 0.40) return "gradual_disengagement";
  if (inp.consecutive_quota_miss_streak >= 2 && inp.comp_plan_satisfaction_score <= 0.45) return "quota_fatigue";
  if (inp.manager_satisfaction_score <= 0.35 && inp.peer_collaboration_score <= 0.40) return "manager_friction";
  if (inp.peer_collaboration_score <= 0.30 && inp.recognition_received_count <= 1) return "peer_isolation";
  if (inp.recognition_received_count <= 1 && inp.career_path_clarity_score <= 0.35) return "recognition_drought";
  return "none";
}
function risk(c: number): string {
  if (c >= 60) return "critical";
  if (c >= 40) return "high";
  if (c >= 20) return "moderate";
  return "low";
}
function severity(c: number): string {
  if (c >= 60) return "flight_risk";
  if (c >= 40) return "burning_out";
  if (c >= 20) return "straining";
  return "thriving";
}
function action(r: string, p: string): string {
  if (r === "critical") return "retention_package_discussion";
  if (r === "high") {
    if (p === "gradual_disengagement") return "workload_rebalancing";
    if (p === "quota_fatigue") return "territory_reassignment";
    if (p === "manager_friction") return "manager_mediation";
    if (p === "peer_isolation" || p === "recognition_drought") return "recognition_intervention";
    return "workload_rebalancing";
  }
  if (r === "moderate") return "wellness_check_in";
  return "no_action";
}
function signal(inp: typeof MOCK_REPS[0], pat: string, comp: number): string {
  if (comp < 20) return "Rep engagement and wellbeing healthy — activity trends, sentiment, and performance indicators within normal benchmarks";
  const labels: Record<string,string> = {
    gradual_disengagement: "Gradual disengagement", quota_fatigue: "Quota fatigue",
    manager_friction: "Manager friction", peer_isolation: "Peer isolation",
    recognition_drought: "Recognition drought"
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  const actTrend = Math.round(inp.activity_volume_trend_pct * 100);
  const wrTrend  = Math.round(inp.win_rate_trend_pct * 100);
  const mgrScore = Math.round(inp.manager_satisfaction_score * 100);
  return `${label} — activity trend ${actTrend > 0 ? "+" : ""}${actTrend}% — win rate trend ${wrTrend > 0 ? "+" : ""}${wrTrend}% — manager satisfaction ${mgrScore}% — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(inp => {
      const d   = disScore(inp);
      const f   = fatScore(inp);
      const se  = sentScore(inp);
      const p   = perfScore(inp);
      const comp = composite(d, f, se, p);
      const pat  = pattern(inp);
      const r    = risk(comp);
      const sev  = severity(comp);
      const act  = action(r, pat);
      const repCost = 85000 * (1.5 + (inp.tenure_months / 24) * 0.5) * (comp / 100);
      return {
        rep_id: inp.rep_id, region: inp.region,
        burnout_risk: r, burnout_pattern: pat, burnout_severity: sev, recommended_action: act,
        disengagement_score: d, fatigue_score: f, sentiment_score: se, performance_erosion_score: p,
        burnout_composite: comp,
        has_burnout_gap: comp >= 40 || inp.activity_volume_trend_pct <= -0.20 || inp.consecutive_quota_miss_streak >= 2,
        is_flight_risk: comp >= 25 || inp.internal_mobility_applications >= 1 || inp.comp_plan_satisfaction_score <= 0.40 || inp.exit_interview_signals >= 1,
        estimated_replacement_cost_usd: Math.round(repCost * 100) / 100,
        burnout_signal: signal(inp, pat, comp),
      };
    });

    const risk_counts: Record<string,number> = {};
    const pattern_counts: Record<string,number> = {};
    const severity_counts: Record<string,number> = {};
    const action_counts: Record<string,number> = {};
    let total_comp=0, total_dis=0, total_fat=0, total_sent=0, total_perf=0, total_rc=0;
    let gap_count=0, flight_count=0;
    for (const r of reps) {
      risk_counts[r.burnout_risk] = (risk_counts[r.burnout_risk]||0)+1;
      pattern_counts[r.burnout_pattern] = (pattern_counts[r.burnout_pattern]||0)+1;
      severity_counts[r.burnout_severity] = (severity_counts[r.burnout_severity]||0)+1;
      action_counts[r.recommended_action] = (action_counts[r.recommended_action]||0)+1;
      total_comp += r.burnout_composite;
      total_dis  += r.disengagement_score;
      total_fat  += r.fatigue_score;
      total_sent += r.sentiment_score;
      total_perf += r.performance_erosion_score;
      total_rc   += r.estimated_replacement_cost_usd;
      if (r.has_burnout_gap) gap_count++;
      if (r.is_flight_risk)  flight_count++;
    }
    const n = reps.length;
    const summary = {
      total: n, risk_counts, pattern_counts, severity_counts, action_counts,
      avg_burnout_composite: Math.round(total_comp/n*10)/10,
      burnout_gap_count: gap_count, flight_risk_count: flight_count,
      avg_disengagement_score: Math.round(total_dis/n*10)/10,
      avg_fatigue_score: Math.round(total_fat/n*10)/10,
      avg_sentiment_score: Math.round(total_sent/n*10)/10,
      avg_performance_erosion_score: Math.round(total_perf/n*10)/10,
      total_estimated_replacement_cost_usd: Math.round(total_rc*100)/100,
    };
    return NextResponse.json(sealResponse({ reps, summary } as Record<string,unknown>));
  }

  const res = await fetch(`${process.env.SWARM_API_URL}/sales-rep-burnout-attrition-risk-intelligence-engine`);
  const data = await res.json();
  return NextResponse.json(data);
}
