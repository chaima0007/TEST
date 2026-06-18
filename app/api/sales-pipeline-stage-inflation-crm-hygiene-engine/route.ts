import { NextResponse } from "next/server";

const MOCK_REPS = [
  { rep_id:"PH-001", region:"EMEA",  evaluation_period_id:"Q1-2026", stage_advancement_without_exit_criteria_pct:0.62, deal_regression_rate_pct:0.38, avg_days_in_current_stage:45.0, stage_3_to_close_conversion_rate_pct:0.12, closed_won_below_forecast_pct:0.48, stage_skip_rate_pct:0.22, crm_update_latency_days:9.5, verified_next_step_in_crm_rate_pct:0.18, competitive_status_missing_rate_pct:0.55, decision_criteria_captured_rate_pct:0.15, technical_validation_complete_rate_pct:0.18, budget_verified_rate_pct:0.22, close_date_slip_rate_pct:0.65, pipeline_creation_to_close_ratio:7.2, opp_age_over_180_days_pct:0.45, discovery_to_proposal_ratio:6.8, data_completeness_score:0.22, manual_close_date_push_rate_pct:0.58, win_rate_vs_forecast_accuracy_delta:0.35, total_pipeline_deals:35, avg_deal_value_usd:95000 },
  { rep_id:"PH-002", region:"NAMER", evaluation_period_id:"Q1-2026", stage_advancement_without_exit_criteria_pct:0.18, deal_regression_rate_pct:0.08, avg_days_in_current_stage:12.0, stage_3_to_close_conversion_rate_pct:0.42, closed_won_below_forecast_pct:0.10, stage_skip_rate_pct:0.05, crm_update_latency_days:1.2, verified_next_step_in_crm_rate_pct:0.82, competitive_status_missing_rate_pct:0.12, decision_criteria_captured_rate_pct:0.78, technical_validation_complete_rate_pct:0.85, budget_verified_rate_pct:0.80, close_date_slip_rate_pct:0.14, pipeline_creation_to_close_ratio:2.1, opp_age_over_180_days_pct:0.08, discovery_to_proposal_ratio:2.2, data_completeness_score:0.88, manual_close_date_push_rate_pct:0.10, win_rate_vs_forecast_accuracy_delta:0.06, total_pipeline_deals:28, avg_deal_value_usd:110000 },
  { rep_id:"PH-003", region:"APAC",  evaluation_period_id:"Q1-2026", stage_advancement_without_exit_criteria_pct:0.48, deal_regression_rate_pct:0.28, avg_days_in_current_stage:38.0, stage_3_to_close_conversion_rate_pct:0.22, closed_won_below_forecast_pct:0.32, stage_skip_rate_pct:0.15, crm_update_latency_days:6.5, verified_next_step_in_crm_rate_pct:0.32, competitive_status_missing_rate_pct:0.40, decision_criteria_captured_rate_pct:0.28, technical_validation_complete_rate_pct:0.30, budget_verified_rate_pct:0.35, close_date_slip_rate_pct:0.42, pipeline_creation_to_close_ratio:5.8, opp_age_over_180_days_pct:0.30, discovery_to_proposal_ratio:4.5, data_completeness_score:0.38, manual_close_date_push_rate_pct:0.38, win_rate_vs_forecast_accuracy_delta:0.22, total_pipeline_deals:42, avg_deal_value_usd:78000 },
  { rep_id:"PH-004", region:"LATAM", evaluation_period_id:"Q1-2026", stage_advancement_without_exit_criteria_pct:0.08, deal_regression_rate_pct:0.05, avg_days_in_current_stage:8.0, stage_3_to_close_conversion_rate_pct:0.58, closed_won_below_forecast_pct:0.05, stage_skip_rate_pct:0.02, crm_update_latency_days:0.8, verified_next_step_in_crm_rate_pct:0.92, competitive_status_missing_rate_pct:0.06, decision_criteria_captured_rate_pct:0.90, technical_validation_complete_rate_pct:0.92, budget_verified_rate_pct:0.90, close_date_slip_rate_pct:0.08, pipeline_creation_to_close_ratio:1.8, opp_age_over_180_days_pct:0.04, discovery_to_proposal_ratio:1.5, data_completeness_score:0.95, manual_close_date_push_rate_pct:0.05, win_rate_vs_forecast_accuracy_delta:0.03, total_pipeline_deals:22, avg_deal_value_usd:65000 },
  { rep_id:"PH-005", region:"EMEA",  evaluation_period_id:"Q1-2026", stage_advancement_without_exit_criteria_pct:0.55, deal_regression_rate_pct:0.40, avg_days_in_current_stage:55.0, stage_3_to_close_conversion_rate_pct:0.09, closed_won_below_forecast_pct:0.50, stage_skip_rate_pct:0.28, crm_update_latency_days:12.0, verified_next_step_in_crm_rate_pct:0.12, competitive_status_missing_rate_pct:0.68, decision_criteria_captured_rate_pct:0.10, technical_validation_complete_rate_pct:0.12, budget_verified_rate_pct:0.15, close_date_slip_rate_pct:0.70, pipeline_creation_to_close_ratio:8.5, opp_age_over_180_days_pct:0.52, discovery_to_proposal_ratio:7.2, data_completeness_score:0.16, manual_close_date_push_rate_pct:0.65, win_rate_vs_forecast_accuracy_delta:0.38, total_pipeline_deals:48, avg_deal_value_usd:120000 },
  { rep_id:"PH-006", region:"NAMER", evaluation_period_id:"Q1-2026", stage_advancement_without_exit_criteria_pct:0.32, deal_regression_rate_pct:0.18, avg_days_in_current_stage:22.0, stage_3_to_close_conversion_rate_pct:0.30, closed_won_below_forecast_pct:0.20, stage_skip_rate_pct:0.10, crm_update_latency_days:3.5, verified_next_step_in_crm_rate_pct:0.58, competitive_status_missing_rate_pct:0.28, decision_criteria_captured_rate_pct:0.50, technical_validation_complete_rate_pct:0.55, budget_verified_rate_pct:0.52, close_date_slip_rate_pct:0.28, pipeline_creation_to_close_ratio:3.2, opp_age_over_180_days_pct:0.16, discovery_to_proposal_ratio:3.0, data_completeness_score:0.62, manual_close_date_push_rate_pct:0.22, win_rate_vs_forecast_accuracy_delta:0.14, total_pipeline_deals:31, avg_deal_value_usd:88000 },
  { rep_id:"PH-007", region:"APAC",  evaluation_period_id:"Q1-2026", stage_advancement_without_exit_criteria_pct:0.72, deal_regression_rate_pct:0.45, avg_days_in_current_stage:62.0, stage_3_to_close_conversion_rate_pct:0.06, closed_won_below_forecast_pct:0.55, stage_skip_rate_pct:0.35, crm_update_latency_days:14.0, verified_next_step_in_crm_rate_pct:0.08, competitive_status_missing_rate_pct:0.75, decision_criteria_captured_rate_pct:0.08, technical_validation_complete_rate_pct:0.10, budget_verified_rate_pct:0.10, close_date_slip_rate_pct:0.78, pipeline_creation_to_close_ratio:9.8, opp_age_over_180_days_pct:0.60, discovery_to_proposal_ratio:8.5, data_completeness_score:0.10, manual_close_date_push_rate_pct:0.72, win_rate_vs_forecast_accuracy_delta:0.45, total_pipeline_deals:52, avg_deal_value_usd:130000 },
  { rep_id:"PH-008", region:"LATAM", evaluation_period_id:"Q1-2026", stage_advancement_without_exit_criteria_pct:0.42, deal_regression_rate_pct:0.22, avg_days_in_current_stage:30.0, stage_3_to_close_conversion_rate_pct:0.26, closed_won_below_forecast_pct:0.28, stage_skip_rate_pct:0.12, crm_update_latency_days:4.8, verified_next_step_in_crm_rate_pct:0.42, competitive_status_missing_rate_pct:0.35, decision_criteria_captured_rate_pct:0.40, technical_validation_complete_rate_pct:0.42, budget_verified_rate_pct:0.45, close_date_slip_rate_pct:0.35, pipeline_creation_to_close_ratio:4.5, opp_age_over_180_days_pct:0.22, discovery_to_proposal_ratio:3.8, data_completeness_score:0.50, manual_close_date_push_rate_pct:0.30, win_rate_vs_forecast_accuracy_delta:0.18, total_pipeline_deals:38, avg_deal_value_usd:72000 },
];

type Rep = typeof MOCK_REPS[0];

function accuracyScore(i: Rep): number {
  let s = 0;
  if      (i.stage_advancement_without_exit_criteria_pct >= 0.55) s += 40; else if (i.stage_advancement_without_exit_criteria_pct >= 0.30) s += 22; else if (i.stage_advancement_without_exit_criteria_pct >= 0.15) s += 8;
  if      (i.closed_won_below_forecast_pct                >= 0.45) s += 35; else if (i.closed_won_below_forecast_pct >= 0.25) s += 18;
  if      (i.win_rate_vs_forecast_accuracy_delta          >= 0.30) s += 25; else if (i.win_rate_vs_forecast_accuracy_delta >= 0.15) s += 12;
  return Math.min(s, 100);
}
function hygieneScore(i: Rep): number {
  let s = 0;
  if      (i.crm_update_latency_days          >= 10.0) s += 45; else if (i.crm_update_latency_days >= 5.0) s += 25; else if (i.crm_update_latency_days >= 2.5) s += 10;
  if      (i.verified_next_step_in_crm_rate_pct <= 0.25) s += 30; else if (i.verified_next_step_in_crm_rate_pct <= 0.55) s += 15;
  if      (i.data_completeness_score            <= 0.25) s += 25; else if (i.data_completeness_score <= 0.55) s += 12;
  return Math.min(s, 100);
}
function velocityScore(i: Rep): number {
  let s = 0;
  if      (i.close_date_slip_rate_pct    >= 0.60) s += 45; else if (i.close_date_slip_rate_pct >= 0.35) s += 25; else if (i.close_date_slip_rate_pct >= 0.18) s += 10;
  if      (i.opp_age_over_180_days_pct   >= 0.40) s += 30; else if (i.opp_age_over_180_days_pct >= 0.20) s += 15;
  if      (i.deal_regression_rate_pct    >= 0.35) s += 25; else if (i.deal_regression_rate_pct >= 0.18) s += 12;
  return Math.min(s, 100);
}
function completenessScore(i: Rep): number {
  let s = 0;
  if      (i.decision_criteria_captured_rate_pct     <= 0.20) s += 40; else if (i.decision_criteria_captured_rate_pct <= 0.45) s += 22; else if (i.decision_criteria_captured_rate_pct <= 0.65) s += 8;
  if      (i.budget_verified_rate_pct                <= 0.25) s += 35; else if (i.budget_verified_rate_pct <= 0.50) s += 18;
  if      (i.technical_validation_complete_rate_pct  <= 0.20) s += 25; else if (i.technical_validation_complete_rate_pct <= 0.45) s += 12;
  return Math.min(s, 100);
}
function composite(ac: number, hy: number, ve: number, co: number): number {
  return Math.min(Math.round((ac * 0.30 + hy * 0.25 + ve * 0.25 + co * 0.20) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.stage_advancement_without_exit_criteria_pct >= 0.50 && i.deal_regression_rate_pct >= 0.30) return "stage_inflation_stager";
  if (i.close_date_slip_rate_pct >= 0.55 && i.opp_age_over_180_days_pct >= 0.35)                  return "phantom_pipeline";
  if (i.data_completeness_score <= 0.30 && i.crm_update_latency_days >= 7)                         return "data_black_hole";
  if (i.stage_3_to_close_conversion_rate_pct <= 0.15 && i.pipeline_creation_to_close_ratio >= 5.0) return "vanity_metrics_builder";
  if (i.win_rate_vs_forecast_accuracy_delta >= 0.25 && i.closed_won_below_forecast_pct >= 0.40)    return "forecast_fudger";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "corrupted"; if (c >= 40) return "degraded"; if (c >= 20) return "drifting"; return "clean"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "stage_inflation_stager" || p === "forecast_fudger") return "crm_accuracy_reset"; return "forecast_integrity_audit"; }
  if (r === "high") {
    if (p === "stage_inflation_stager") return "stage_criteria_enforcement";
    if (p === "phantom_pipeline")       return "pipeline_purge_facilitation";
    if (p === "data_black_hole")        return "data_quality_intervention";
    if (p === "vanity_metrics_builder") return "pipeline_review_checkpoint";
    if (p === "forecast_fudger")        return "forecast_integrity_audit";
    return "crm_hygiene_coaching";
  }
  if (r === "moderate") return "crm_hygiene_coaching";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "CRM data clean — stage progression, hygiene, velocity and completeness within benchmark targets";
  const labels: Record<string,string> = { stage_inflation_stager:"Stage inflation stager", phantom_pipeline:"Phantom pipeline", data_black_hole:"Data black hole", vanity_metrics_builder:"Vanity metrics builder", forecast_fudger:"Forecast fudger" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(i.stage_advancement_without_exit_criteria_pct*100)}% advanced without exit criteria — ${Math.round(i.close_date_slip_rate_pct*100)}% close date slip — ${Math.round(i.data_completeness_score*100)}% data completeness — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(i => {
      const ac = accuracyScore(i), hy = hygieneScore(i), ve = velocityScore(i), co = completenessScore(i);
      const comp = composite(ac, hy, ve, co), pat = pattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      const inflated = Math.round(i.total_pipeline_deals * i.avg_deal_value_usd * i.stage_advancement_without_exit_criteria_pct * (comp/100) * 100) / 100;
      return {
        rep_id: i.rep_id, region: i.region,
        hygiene_risk: r, hygiene_pattern: pat, hygiene_severity: sev, recommended_action: act,
        accuracy_score: ac, hygiene_score: hy, velocity_score: ve, completeness_score: co,
        hygiene_composite: comp,
        has_hygiene_gap: comp >= 40 || i.data_completeness_score <= 0.50 || i.stage_advancement_without_exit_criteria_pct >= 0.30,
        requires_hygiene_coaching: comp >= 25 || i.crm_update_latency_days >= 5.0 || i.verified_next_step_in_crm_rate_pct <= 0.60,
        estimated_inflated_pipeline_usd: inflated,
        hygiene_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tac=0, thy=0, tve=0, tco=0, tcomp=0, tinf=0, gc=0, cc=0;
    for (const r of reps) {
      rc[r.hygiene_risk]=(rc[r.hygiene_risk]||0)+1; pc[r.hygiene_pattern]=(pc[r.hygiene_pattern]||0)+1;
      sc[r.hygiene_severity]=(sc[r.hygiene_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      tac+=r.accuracy_score; thy+=r.hygiene_score; tve+=r.velocity_score; tco+=r.completeness_score;
      tcomp+=r.hygiene_composite; tinf+=r.estimated_inflated_pipeline_usd;
      if (r.has_hygiene_gap) gc++; if (r.requires_hygiene_coaching) cc++;
    }
    const n = reps.length;
    return NextResponse.json({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_hygiene_composite: Math.round(tcomp/n*10)/10,
      hygiene_gap_count: gc, coaching_count: cc,
      avg_accuracy_score: Math.round(tac/n*10)/10,
      avg_hygiene_score: Math.round(thy/n*10)/10,
      avg_velocity_score: Math.round(tve/n*10)/10,
      avg_completeness_score: Math.round(tco/n*10)/10,
      total_estimated_inflated_pipeline_usd: Math.round(tinf*100)/100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-pipeline-stage-inflation-crm-hygiene-engine`)).json());
}
