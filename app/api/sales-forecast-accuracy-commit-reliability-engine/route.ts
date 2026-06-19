import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"FC-001", region:"EMEA",  evaluation_period_id:"Q1-2026", commit_vs_actual_variance_pct:0.45, overcommit_frequency_pct:0.65, undercommit_frequency_pct:0.10, forecast_miss_rate_pct:0.65, commit_category_accuracy_pct:0.38, best_case_to_close_conversion_pct:0.18, pipeline_to_commit_escalation_rate_pct:0.48, category_downgrade_rate_pct:0.40, last_week_close_rate_pct:0.60, pull_in_frequency_pct:0.25, push_out_frequency_pct:0.50, avg_days_in_commit_before_close:4.0, crm_forecast_update_frequency_days:9.0, deal_stage_accuracy_at_commit_pct:0.32, close_date_change_frequency:3.5, rolling_3q_forecast_accuracy_pct:0.48, upside_capture_rate_pct:0.22, total_commit_deals:22, avg_deal_value_usd:92000, quota_attainment_pct:0.55 },
  { rep_id:"FC-002", region:"NAMER", evaluation_period_id:"Q1-2026", commit_vs_actual_variance_pct:0.07, overcommit_frequency_pct:0.12, undercommit_frequency_pct:0.10, forecast_miss_rate_pct:0.10, commit_category_accuracy_pct:0.88, best_case_to_close_conversion_pct:0.72, pipeline_to_commit_escalation_rate_pct:0.08, category_downgrade_rate_pct:0.06, last_week_close_rate_pct:0.18, pull_in_frequency_pct:0.12, push_out_frequency_pct:0.10, avg_days_in_commit_before_close:18.0, crm_forecast_update_frequency_days:2.0, deal_stage_accuracy_at_commit_pct:0.92, close_date_change_frequency:0.8, rolling_3q_forecast_accuracy_pct:0.91, upside_capture_rate_pct:0.78, total_commit_deals:30, avg_deal_value_usd:115000, quota_attainment_pct:0.96 },
  { rep_id:"FC-003", region:"APAC",  evaluation_period_id:"Q1-2026", commit_vs_actual_variance_pct:0.25, overcommit_frequency_pct:0.38, undercommit_frequency_pct:0.18, forecast_miss_rate_pct:0.38, commit_category_accuracy_pct:0.62, best_case_to_close_conversion_pct:0.40, pipeline_to_commit_escalation_rate_pct:0.28, category_downgrade_rate_pct:0.22, last_week_close_rate_pct:0.38, pull_in_frequency_pct:0.18, push_out_frequency_pct:0.30, avg_days_in_commit_before_close:10.0, crm_forecast_update_frequency_days:5.0, deal_stage_accuracy_at_commit_pct:0.65, close_date_change_frequency:2.2, rolling_3q_forecast_accuracy_pct:0.68, upside_capture_rate_pct:0.50, total_commit_deals:20, avg_deal_value_usd:78000, quota_attainment_pct:0.75 },
  { rep_id:"FC-004", region:"LATAM", evaluation_period_id:"Q1-2026", commit_vs_actual_variance_pct:0.04, overcommit_frequency_pct:0.08, undercommit_frequency_pct:0.62, forecast_miss_rate_pct:0.08, commit_category_accuracy_pct:0.82, best_case_to_close_conversion_pct:0.65, pipeline_to_commit_escalation_rate_pct:0.05, category_downgrade_rate_pct:0.04, last_week_close_rate_pct:0.12, pull_in_frequency_pct:0.08, push_out_frequency_pct:0.08, avg_days_in_commit_before_close:22.0, crm_forecast_update_frequency_days:1.5, deal_stage_accuracy_at_commit_pct:0.95, close_date_change_frequency:0.5, rolling_3q_forecast_accuracy_pct:0.96, upside_capture_rate_pct:0.88, total_commit_deals:16, avg_deal_value_usd:62000, quota_attainment_pct:1.05 },
  { rep_id:"FC-005", region:"EMEA",  evaluation_period_id:"Q1-2026", commit_vs_actual_variance_pct:0.55, overcommit_frequency_pct:0.72, undercommit_frequency_pct:0.08, forecast_miss_rate_pct:0.72, commit_category_accuracy_pct:0.28, best_case_to_close_conversion_pct:0.12, pipeline_to_commit_escalation_rate_pct:0.58, category_downgrade_rate_pct:0.52, last_week_close_rate_pct:0.68, pull_in_frequency_pct:0.30, push_out_frequency_pct:0.60, avg_days_in_commit_before_close:3.0, crm_forecast_update_frequency_days:12.0, deal_stage_accuracy_at_commit_pct:0.22, close_date_change_frequency:4.5, rolling_3q_forecast_accuracy_pct:0.38, upside_capture_rate_pct:0.15, total_commit_deals:28, avg_deal_value_usd:108000, quota_attainment_pct:0.42 },
  { rep_id:"FC-006", region:"NAMER", evaluation_period_id:"Q1-2026", commit_vs_actual_variance_pct:0.14, overcommit_frequency_pct:0.22, undercommit_frequency_pct:0.15, forecast_miss_rate_pct:0.18, commit_category_accuracy_pct:0.78, best_case_to_close_conversion_pct:0.58, pipeline_to_commit_escalation_rate_pct:0.15, category_downgrade_rate_pct:0.12, last_week_close_rate_pct:0.25, pull_in_frequency_pct:0.15, push_out_frequency_pct:0.18, avg_days_in_commit_before_close:14.0, crm_forecast_update_frequency_days:3.0, deal_stage_accuracy_at_commit_pct:0.82, close_date_change_frequency:1.2, rolling_3q_forecast_accuracy_pct:0.82, upside_capture_rate_pct:0.68, total_commit_deals:26, avg_deal_value_usd:88000, quota_attainment_pct:0.88 },
  { rep_id:"FC-007", region:"APAC",  evaluation_period_id:"Q1-2026", commit_vs_actual_variance_pct:0.38, overcommit_frequency_pct:0.30, undercommit_frequency_pct:0.58, forecast_miss_rate_pct:0.30, commit_category_accuracy_pct:0.50, best_case_to_close_conversion_pct:0.85, pipeline_to_commit_escalation_rate_pct:0.20, category_downgrade_rate_pct:0.35, last_week_close_rate_pct:0.28, pull_in_frequency_pct:0.22, push_out_frequency_pct:0.25, avg_days_in_commit_before_close:16.0, crm_forecast_update_frequency_days:4.5, deal_stage_accuracy_at_commit_pct:0.72, close_date_change_frequency:1.8, rolling_3q_forecast_accuracy_pct:0.85, upside_capture_rate_pct:0.90, total_commit_deals:18, avg_deal_value_usd:82000, quota_attainment_pct:1.12 },
  { rep_id:"FC-008", region:"MEA",   evaluation_period_id:"Q1-2026", commit_vs_actual_variance_pct:0.20, overcommit_frequency_pct:0.32, undercommit_frequency_pct:0.22, forecast_miss_rate_pct:0.28, commit_category_accuracy_pct:0.68, best_case_to_close_conversion_pct:0.48, pipeline_to_commit_escalation_rate_pct:0.22, category_downgrade_rate_pct:0.18, last_week_close_rate_pct:0.30, pull_in_frequency_pct:0.16, push_out_frequency_pct:0.28, avg_days_in_commit_before_close:12.0, crm_forecast_update_frequency_days:4.0, deal_stage_accuracy_at_commit_pct:0.70, close_date_change_frequency:1.6, rolling_3q_forecast_accuracy_pct:0.74, upside_capture_rate_pct:0.58, total_commit_deals:24, avg_deal_value_usd:72000, quota_attainment_pct:0.80 },
];

type Rep = typeof MOCK_REPS[0];

function accuracyScore(i: Rep): number {
  let s = 0;
  if      (i.commit_vs_actual_variance_pct   >= 0.40) s += 40; else if (i.commit_vs_actual_variance_pct >= 0.22) s += 22; else if (i.commit_vs_actual_variance_pct >= 0.10) s += 8;
  if      (i.forecast_miss_rate_pct          >= 0.60) s += 35; else if (i.forecast_miss_rate_pct >= 0.40) s += 18; else if (i.forecast_miss_rate_pct >= 0.20) s += 6;
  if      (i.rolling_3q_forecast_accuracy_pct <= 0.55) s += 25; else if (i.rolling_3q_forecast_accuracy_pct <= 0.70) s += 12;
  return Math.min(s, 100);
}
function disciplineScore(i: Rep): number {
  let s = 0;
  if      (i.commit_category_accuracy_pct <= 0.40) s += 45; else if (i.commit_category_accuracy_pct <= 0.60) s += 25; else if (i.commit_category_accuracy_pct <= 0.75) s += 10;
  if      (i.category_downgrade_rate_pct  >= 0.35) s += 30; else if (i.category_downgrade_rate_pct >= 0.20) s += 15;
  if      (i.close_date_change_frequency  >= 3.0)  s += 25; else if (i.close_date_change_frequency >= 2.0) s += 12;
  return Math.min(s, 100);
}
function timingScore(i: Rep): number {
  let s = 0;
  if      (i.last_week_close_rate_pct                 >= 0.55) s += 40; else if (i.last_week_close_rate_pct >= 0.35) s += 22; else if (i.last_week_close_rate_pct >= 0.20) s += 8;
  if      (i.pipeline_to_commit_escalation_rate_pct   >= 0.40) s += 35; else if (i.pipeline_to_commit_escalation_rate_pct >= 0.25) s += 18;
  if      (i.push_out_frequency_pct                   >= 0.45) s += 25; else if (i.push_out_frequency_pct >= 0.28) s += 12;
  return Math.min(s, 100);
}
function reliabilityScore(i: Rep): number {
  let s = 0;
  if      (i.overcommit_frequency_pct                >= 0.60) s += 40; else if (i.overcommit_frequency_pct >= 0.40) s += 22; else if (i.overcommit_frequency_pct >= 0.22) s += 8;
  if      (i.undercommit_frequency_pct               >= 0.55) s += 35; else if (i.undercommit_frequency_pct >= 0.35) s += 18;
  if      (i.crm_forecast_update_frequency_days      >= 7.0)  s += 25; else if (i.crm_forecast_update_frequency_days >= 4.0) s += 12;
  return Math.min(s, 100);
}
function composite(ac: number, di: number, ti: number, re: number): number {
  return Math.min(Math.round((ac * 0.30 + di * 0.25 + ti * 0.25 + re * 0.20) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.overcommit_frequency_pct >= 0.55 && i.commit_vs_actual_variance_pct >= 0.30)        return "chronic_overcommit";
  if (i.undercommit_frequency_pct >= 0.50 && i.rolling_3q_forecast_accuracy_pct >= 0.80)    return "sandbagger";
  if (i.push_out_frequency_pct >= 0.40 && i.close_date_change_frequency >= 2.5)             return "commit_drifter";
  if (i.last_week_close_rate_pct >= 0.50 && i.pipeline_to_commit_escalation_rate_pct >= 0.35) return "late_push_abuser";
  if (i.category_downgrade_rate_pct >= 0.30 && i.commit_category_accuracy_pct <= 0.55)      return "category_manipulator";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "blind_spot"; if (c >= 40) return "unreliable"; if (c >= 20) return "drifting"; return "accurate"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "chronic_overcommit" || p === "sandbagger") return "executive_forecast_audit"; return "forecast_process_reset"; }
  if (r === "high") {
    if (p === "chronic_overcommit")    return "deal_by_deal_review";
    if (p === "sandbagger")            return "manager_forecast_alignment";
    if (p === "commit_drifter")        return "commit_cadence_coaching";
    if (p === "late_push_abuser")      return "pipeline_review_increase";
    if (p === "category_manipulator")  return "forecast_hygiene_training";
    return "forecast_monitoring";
  }
  if (r === "moderate") return "forecast_monitoring";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Forecast reliability strong — commit accuracy, category discipline, and timing patterns within benchmark targets";
  const labels: Record<string,string> = { chronic_overcommit:"Chronic overcommit", sandbagger:"Sandbagger", commit_drifter:"Commit drifter", late_push_abuser:"Late push abuser", category_manipulator:"Category manipulator" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(i.commit_vs_actual_variance_pct*100)}% commit variance — ${Math.round(i.forecast_miss_rate_pct*100)}% miss rate — ${Math.round(i.rolling_3q_forecast_accuracy_pct*100)}% 3Q accuracy — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(i => {
      const ac = accuracyScore(i), di = disciplineScore(i), ti = timingScore(i), re = reliabilityScore(i);
      const comp = composite(ac, di, ti, re), pat = pattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      const err = Math.round(i.total_commit_deals * i.avg_deal_value_usd * i.commit_vs_actual_variance_pct * (comp/100) * 100) / 100;
      return {
        rep_id: i.rep_id, region: i.region,
        forecast_risk: r, forecast_pattern: pat, forecast_severity: sev, recommended_action: act,
        accuracy_score: ac, discipline_score: di, timing_score: ti, reliability_score: re,
        forecast_composite: comp,
        has_forecast_gap: comp >= 40 || i.forecast_miss_rate_pct >= 0.40 || i.rolling_3q_forecast_accuracy_pct <= 0.65,
        requires_manager_review: comp >= 25 || i.commit_vs_actual_variance_pct >= 0.20 || i.push_out_frequency_pct >= 0.30,
        estimated_forecast_error_usd: err,
        forecast_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tac=0,tdi=0,tti=0,tre=0,tcomp=0,tfe=0,gc=0,mc=0;
    for (const r of reps) {
      rc[r.forecast_risk]=(rc[r.forecast_risk]||0)+1; pc[r.forecast_pattern]=(pc[r.forecast_pattern]||0)+1;
      sc[r.forecast_severity]=(sc[r.forecast_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      tac+=r.accuracy_score; tdi+=r.discipline_score; tti+=r.timing_score; tre+=r.reliability_score;
      tcomp+=r.forecast_composite; tfe+=r.estimated_forecast_error_usd;
      if (r.has_forecast_gap) gc++; if (r.requires_manager_review) mc++;
    }
    const n = reps.length;
    return NextResponse.json(sealResponse({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_forecast_composite: Math.round(tcomp/n*10)/10,
      forecast_gap_count: gc, manager_review_count: mc,
      avg_accuracy_score: Math.round(tac/n*10)/10,
      avg_discipline_score: Math.round(tdi/n*10)/10,
      avg_timing_score: Math.round(tti/n*10)/10,
      avg_reliability_score: Math.round(tre/n*10)/10,
      total_estimated_forecast_error_usd: Math.round(tfe*100)/100,
    }} as Record<string,unknown>));
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-forecast-accuracy-commit-reliability-engine`)).json());
}
