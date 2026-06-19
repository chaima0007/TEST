import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"DV-001", region:"EMEA",  evaluation_period_id:"Q2-2026", avg_days_in_current_stage:38, avg_cycle_length_days:155, cycle_length_vs_benchmark_pct:0.62, stage_regression_count:3, no_activity_streak_days:16, champion_response_time_days:12, executive_sponsor_days_since_contact:45, next_step_defined_rate_pct:0.18, mutual_action_plan_completion_pct:0.12, close_date_slip_count:4, close_date_slip_days_avg:22, proposal_sent_to_response_days:18, poc_to_commercial_days:75, avg_stakeholder_response_rate_pct:0.18, multi_threaded_deal_rate_pct:0.15, competitive_re_eval_trigger_pct:0.42, late_stage_stall_rate_pct:0.52, total_active_deals:8, avg_deal_value_usd:85000 },
  { rep_id:"DV-002", region:"APAC",  evaluation_period_id:"Q2-2026", avg_days_in_current_stage:8,  avg_cycle_length_days:62,  cycle_length_vs_benchmark_pct:0.05, stage_regression_count:0, no_activity_streak_days:1,  champion_response_time_days:1.5, executive_sponsor_days_since_contact:5,  next_step_defined_rate_pct:0.92, mutual_action_plan_completion_pct:0.88, close_date_slip_count:0, close_date_slip_days_avg:0,  proposal_sent_to_response_days:3,  poc_to_commercial_days:18, avg_stakeholder_response_rate_pct:0.85, multi_threaded_deal_rate_pct:0.82, competitive_re_eval_trigger_pct:0.05, late_stage_stall_rate_pct:0.05, total_active_deals:14, avg_deal_value_usd:55000 },
  { rep_id:"DV-003", region:"NAMER", evaluation_period_id:"Q2-2026", avg_days_in_current_stage:22, avg_cycle_length_days:95,  cycle_length_vs_benchmark_pct:0.28, stage_regression_count:1, no_activity_streak_days:5,  champion_response_time_days:4,   executive_sponsor_days_since_contact:18, next_step_defined_rate_pct:0.55, mutual_action_plan_completion_pct:0.48, close_date_slip_count:2, close_date_slip_days_avg:12, proposal_sent_to_response_days:8,  poc_to_commercial_days:38, avg_stakeholder_response_rate_pct:0.52, multi_threaded_deal_rate_pct:0.48, competitive_re_eval_trigger_pct:0.18, late_stage_stall_rate_pct:0.22, total_active_deals:11, avg_deal_value_usd:72000 },
  { rep_id:"DV-004", region:"LATAM", evaluation_period_id:"Q2-2026", avg_days_in_current_stage:15, avg_cycle_length_days:78,  cycle_length_vs_benchmark_pct:0.15, stage_regression_count:0, no_activity_streak_days:3,  champion_response_time_days:2.5, executive_sponsor_days_since_contact:12, next_step_defined_rate_pct:0.72, mutual_action_plan_completion_pct:0.68, close_date_slip_count:1, close_date_slip_days_avg:7,  proposal_sent_to_response_days:5,  poc_to_commercial_days:25, avg_stakeholder_response_rate_pct:0.68, multi_threaded_deal_rate_pct:0.65, competitive_re_eval_trigger_pct:0.10, late_stage_stall_rate_pct:0.12, total_active_deals:9,  avg_deal_value_usd:62000 },
  { rep_id:"DV-005", region:"EMEA",  evaluation_period_id:"Q2-2026", avg_days_in_current_stage:42, avg_cycle_length_days:175, cycle_length_vs_benchmark_pct:0.72, stage_regression_count:4, no_activity_streak_days:18, champion_response_time_days:14,  executive_sponsor_days_since_contact:55, next_step_defined_rate_pct:0.15, mutual_action_plan_completion_pct:0.08, close_date_slip_count:5, close_date_slip_days_avg:28, proposal_sent_to_response_days:22, poc_to_commercial_days:95, avg_stakeholder_response_rate_pct:0.12, multi_threaded_deal_rate_pct:0.12, competitive_re_eval_trigger_pct:0.48, late_stage_stall_rate_pct:0.62, total_active_deals:6,  avg_deal_value_usd:120000 },
  { rep_id:"DV-006", region:"MEA",   evaluation_period_id:"Q2-2026", avg_days_in_current_stage:12, avg_cycle_length_days:68,  cycle_length_vs_benchmark_pct:0.08, stage_regression_count:0, no_activity_streak_days:2,  champion_response_time_days:2,   executive_sponsor_days_since_contact:8,  next_step_defined_rate_pct:0.82, mutual_action_plan_completion_pct:0.78, close_date_slip_count:0, close_date_slip_days_avg:0,  proposal_sent_to_response_days:4,  poc_to_commercial_days:22, avg_stakeholder_response_rate_pct:0.78, multi_threaded_deal_rate_pct:0.75, competitive_re_eval_trigger_pct:0.08, late_stage_stall_rate_pct:0.08, total_active_deals:12, avg_deal_value_usd:48000 },
  { rep_id:"DV-007", region:"APAC",  evaluation_period_id:"Q2-2026", avg_days_in_current_stage:28, avg_cycle_length_days:115, cycle_length_vs_benchmark_pct:0.38, stage_regression_count:2, no_activity_streak_days:8,  champion_response_time_days:6,   executive_sponsor_days_since_contact:28, next_step_defined_rate_pct:0.38, mutual_action_plan_completion_pct:0.32, close_date_slip_count:3, close_date_slip_days_avg:15, proposal_sent_to_response_days:12, poc_to_commercial_days:52, avg_stakeholder_response_rate_pct:0.38, multi_threaded_deal_rate_pct:0.35, competitive_re_eval_trigger_pct:0.28, late_stage_stall_rate_pct:0.35, total_active_deals:10, avg_deal_value_usd:68000 },
  { rep_id:"DV-008", region:"NAMER", evaluation_period_id:"Q2-2026", avg_days_in_current_stage:32, avg_cycle_length_days:135, cycle_length_vs_benchmark_pct:0.48, stage_regression_count:2, no_activity_streak_days:12, champion_response_time_days:9,   executive_sponsor_days_since_contact:35, next_step_defined_rate_pct:0.28, mutual_action_plan_completion_pct:0.22, close_date_slip_count:3, close_date_slip_days_avg:18, proposal_sent_to_response_days:15, poc_to_commercial_days:62, avg_stakeholder_response_rate_pct:0.28, multi_threaded_deal_rate_pct:0.22, competitive_re_eval_trigger_pct:0.32, late_stage_stall_rate_pct:0.42, total_active_deals:7,  avg_deal_value_usd:95000 },
];

function stScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.avg_days_in_current_stage     >= 30)   s += 40;
  else if (inp.avg_days_in_current_stage     >= 18)   s += 22;
  else if (inp.avg_days_in_current_stage     >= 10)   s += 8;
  if      (inp.cycle_length_vs_benchmark_pct >= 0.50) s += 35;
  else if (inp.cycle_length_vs_benchmark_pct >= 0.25) s += 18;
  else if (inp.cycle_length_vs_benchmark_pct >= 0.10) s += 6;
  if      (inp.stage_regression_count        >= 3)    s += 25;
  else if (inp.stage_regression_count        >= 2)    s += 12;
  return Math.min(s, 100);
}
function engScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.no_activity_streak_days           >= 14)   s += 40;
  else if (inp.no_activity_streak_days           >= 7)    s += 22;
  else if (inp.no_activity_streak_days           >= 3)    s += 8;
  if      (inp.champion_response_time_days       >= 10)   s += 35;
  else if (inp.champion_response_time_days       >= 5)    s += 18;
  if      (inp.avg_stakeholder_response_rate_pct <= 0.25) s += 25;
  else if (inp.avg_stakeholder_response_rate_pct <= 0.50) s += 12;
  return Math.min(s, 100);
}
function hygScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.next_step_defined_rate_pct        <= 0.30) s += 40;
  else if (inp.next_step_defined_rate_pct        <= 0.55) s += 22;
  else if (inp.next_step_defined_rate_pct        <= 0.75) s += 8;
  if      (inp.mutual_action_plan_completion_pct <= 0.25) s += 35;
  else if (inp.mutual_action_plan_completion_pct <= 0.50) s += 18;
  if      (inp.close_date_slip_count             >= 3)    s += 25;
  else if (inp.close_date_slip_count             >= 2)    s += 12;
  return Math.min(s, 100);
}
function pipScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.late_stage_stall_rate_pct       >= 0.45) s += 45;
  else if (inp.late_stage_stall_rate_pct       >= 0.25) s += 25;
  else if (inp.late_stage_stall_rate_pct       >= 0.12) s += 10;
  if      (inp.competitive_re_eval_trigger_pct >= 0.35) s += 30;
  else if (inp.competitive_re_eval_trigger_pct >= 0.20) s += 15;
  if      (inp.multi_threaded_deal_rate_pct    <= 0.25) s += 25;
  else if (inp.multi_threaded_deal_rate_pct    <= 0.50) s += 12;
  return Math.min(s, 100);
}
function composite(st: number, eng: number, hy: number, pip: number): number {
  return Math.min(Math.round((st*0.30 + eng*0.30 + hy*0.25 + pip*0.15)*100)/100, 100);
}
function pattern(inp: typeof MOCK_REPS[0]): string {
  if (inp.no_activity_streak_days >= 10 && inp.avg_days_in_current_stage >= 20) return "stalled_pipeline";
  if (inp.stage_regression_count >= 2 && inp.close_date_slip_count >= 2) return "stage_regression";
  if (inp.no_activity_streak_days >= 14 && inp.champion_response_time_days >= 8) return "ghost_deal";
  if (inp.champion_response_time_days >= 7 && inp.executive_sponsor_days_since_contact >= 30) return "champion_gone_dark";
  if (inp.avg_cycle_length_days >= 120 && inp.late_stage_stall_rate_pct >= 0.30) return "multistage_drag";
  return "none";
}
function risk(c: number): string {
  if (c >= 60) return "critical";
  if (c >= 40) return "high";
  if (c >= 20) return "moderate";
  return "low";
}
function severity(c: number): string {
  if (c >= 60) return "collapsed";
  if (c >= 40) return "slowing";
  if (c >= 20) return "on_track";
  return "accelerating";
}
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "ghost_deal" || p === "champion_gone_dark") return "deal_rescue_escalation";
    return "pipeline_triage";
  }
  if (r === "high") {
    if (p === "stalled_pipeline" || p === "stage_regression") return "deal_acceleration_coaching";
    if (p === "ghost_deal") return "champion_reactivation";
    if (p === "champion_gone_dark" || p === "multistage_drag") return "executive_involvement";
    return "deal_acceleration_coaching";
  }
  if (r === "moderate") return "velocity_monitoring";
  return "no_action";
}
function signal(inp: typeof MOCK_REPS[0], pat: string, comp: number): string {
  if (comp < 20) return "Deal velocity healthy — stage progression, engagement cadence, and pipeline hygiene within benchmarks";
  const labels: Record<string,string> = {
    stalled_pipeline:"Stalled pipeline", stage_regression:"Stage regression",
    ghost_deal:"Ghost deal", champion_gone_dark:"Champion gone dark", multistage_drag:"Multistage drag"
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(inp.avg_days_in_current_stage)}d in current stage — ${inp.no_activity_streak_days}d no activity — ${inp.close_date_slip_count} close-date slips — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(inp => {
      const st  = stScore(inp);
      const eng = engScore(inp);
      const hy  = hygScore(inp);
      const pip = pipScore(inp);
      const comp = composite(st, eng, hy, pip);
      const pat  = pattern(inp);
      const r    = risk(comp);
      const sev  = severity(comp);
      const act  = action(r, pat);
      const stall = inp.late_stage_stall_rate_pct + inp.close_date_slip_count / 10;
      const atRisk = inp.total_active_deals * inp.avg_deal_value_usd * Math.min(stall, 1.0) * (comp / 100);
      return {
        rep_id: inp.rep_id, region: inp.region,
        velocity_risk: r, velocity_pattern: pat, velocity_severity: sev, recommended_action: act,
        stage_stall_score: st, engagement_decay_score: eng, deal_hygiene_score: hy, pipeline_risk_score: pip,
        velocity_composite: comp,
        has_velocity_gap: comp >= 40 || inp.close_date_slip_count >= 2 || inp.no_activity_streak_days >= 10,
        requires_velocity_intervention: comp >= 25 || inp.late_stage_stall_rate_pct >= 0.30 || inp.stage_regression_count >= 2,
        estimated_at_risk_pipeline_usd: Math.round(atRisk * 100) / 100,
        velocity_signal: signal(inp, pat, comp),
      };
    });

    const risk_counts: Record<string,number> = {};
    const pattern_counts: Record<string,number> = {};
    const severity_counts: Record<string,number> = {};
    const action_counts: Record<string,number> = {};
    let total_comp=0, total_st=0, total_eng=0, total_hy=0, total_pip=0, total_ar=0;
    let gap_count=0, intervention_count=0;
    for (const r of reps) {
      risk_counts[r.velocity_risk] = (risk_counts[r.velocity_risk]||0)+1;
      pattern_counts[r.velocity_pattern] = (pattern_counts[r.velocity_pattern]||0)+1;
      severity_counts[r.velocity_severity] = (severity_counts[r.velocity_severity]||0)+1;
      action_counts[r.recommended_action] = (action_counts[r.recommended_action]||0)+1;
      total_comp += r.velocity_composite;
      total_st   += r.stage_stall_score;
      total_eng  += r.engagement_decay_score;
      total_hy   += r.deal_hygiene_score;
      total_pip  += r.pipeline_risk_score;
      total_ar   += r.estimated_at_risk_pipeline_usd;
      if (r.has_velocity_gap) gap_count++;
      if (r.requires_velocity_intervention) intervention_count++;
    }
    const n = reps.length;
    const summary = {
      total: n, risk_counts, pattern_counts, severity_counts, action_counts,
      avg_velocity_composite: Math.round(total_comp/n*10)/10,
      velocity_gap_count: gap_count, intervention_count,
      avg_stage_stall_score: Math.round(total_st/n*10)/10,
      avg_engagement_decay_score: Math.round(total_eng/n*10)/10,
      avg_deal_hygiene_score: Math.round(total_hy/n*10)/10,
      avg_pipeline_risk_score: Math.round(total_pip/n*10)/10,
      total_estimated_at_risk_pipeline_usd: Math.round(total_ar*100)/100,
    };
    return NextResponse.json(sealResponse({ reps, summary } as Record<string,unknown>));
  }

  const res = await fetch(`${process.env.SWARM_API_URL}/sales-deal-velocity-collapse-intelligence-engine`);
  const data = await res.json();
  return NextResponse.json(data);
}
