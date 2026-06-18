import { NextResponse } from "next/server";

const MOCK_REPS = [
  { rep_id:"CH-001", region:"EMEA",  evaluation_period_id:"Q2-2026", product_usage_trend_pct:-0.32, nps_score_trend:-0.28, support_ticket_volume_trend_pct:0.58, avg_ticket_severity_score:0.72, renewal_probability_score:0.22, last_exec_engagement_days:95, champion_change_events:3, contract_utilization_pct:0.28, multi_product_adoption_rate_pct:0.08, qbr_attendance_rate_pct:0.20, expansion_pipeline_vs_arr_pct:0.02, risk_flags_documented:5, competitor_evaluation_signals:3, time_to_value_days:95, onboarding_completion_rate_pct:0.38, stakeholder_coverage_score:0.18, satisfaction_survey_response_rate:0.25, invoice_payment_on_time_rate_pct:0.62, total_accounts_managed:8, avg_arr_per_account_usd:145000 },
  { rep_id:"CH-002", region:"APAC",  evaluation_period_id:"Q2-2026", product_usage_trend_pct:0.28, nps_score_trend:0.22, support_ticket_volume_trend_pct:0.08, avg_ticket_severity_score:0.15, renewal_probability_score:0.92, last_exec_engagement_days:12, champion_change_events:0, contract_utilization_pct:0.88, multi_product_adoption_rate_pct:0.72, qbr_attendance_rate_pct:0.90, expansion_pipeline_vs_arr_pct:0.35, risk_flags_documented:0, competitor_evaluation_signals:0, time_to_value_days:18, onboarding_completion_rate_pct:0.95, stakeholder_coverage_score:0.82, satisfaction_survey_response_rate:0.88, invoice_payment_on_time_rate_pct:1.0, total_accounts_managed:12, avg_arr_per_account_usd:98000 },
  { rep_id:"CH-003", region:"NAMER", evaluation_period_id:"Q2-2026", product_usage_trend_pct:-0.08, nps_score_trend:-0.05, support_ticket_volume_trend_pct:0.28, avg_ticket_severity_score:0.42, renewal_probability_score:0.58, last_exec_engagement_days:48, champion_change_events:1, contract_utilization_pct:0.62, multi_product_adoption_rate_pct:0.38, qbr_attendance_rate_pct:0.55, expansion_pipeline_vs_arr_pct:0.12, risk_flags_documented:2, competitor_evaluation_signals:1, time_to_value_days:42, onboarding_completion_rate_pct:0.72, stakeholder_coverage_score:0.45, satisfaction_survey_response_rate:0.62, invoice_payment_on_time_rate_pct:0.88, total_accounts_managed:10, avg_arr_per_account_usd:115000 },
  { rep_id:"CH-004", region:"LATAM", evaluation_period_id:"Q2-2026", product_usage_trend_pct:-0.22, nps_score_trend:-0.18, support_ticket_volume_trend_pct:0.52, avg_ticket_severity_score:0.62, renewal_probability_score:0.32, last_exec_engagement_days:75, champion_change_events:2, contract_utilization_pct:0.35, multi_product_adoption_rate_pct:0.12, qbr_attendance_rate_pct:0.25, expansion_pipeline_vs_arr_pct:0.03, risk_flags_documented:4, competitor_evaluation_signals:2, time_to_value_days:78, onboarding_completion_rate_pct:0.45, stakeholder_coverage_score:0.22, satisfaction_survey_response_rate:0.32, invoice_payment_on_time_rate_pct:0.72, total_accounts_managed:9, avg_arr_per_account_usd:128000 },
  { rep_id:"CH-005", region:"EMEA",  evaluation_period_id:"Q2-2026", product_usage_trend_pct:0.15, nps_score_trend:0.12, support_ticket_volume_trend_pct:0.12, avg_ticket_severity_score:0.22, renewal_probability_score:0.82, last_exec_engagement_days:22, champion_change_events:0, contract_utilization_pct:0.78, multi_product_adoption_rate_pct:0.58, qbr_attendance_rate_pct:0.78, expansion_pipeline_vs_arr_pct:0.25, risk_flags_documented:0, competitor_evaluation_signals:0, time_to_value_days:25, onboarding_completion_rate_pct:0.88, stakeholder_coverage_score:0.72, satisfaction_survey_response_rate:0.78, invoice_payment_on_time_rate_pct:0.96, total_accounts_managed:11, avg_arr_per_account_usd:105000 },
  { rep_id:"CH-006", region:"MEA",   evaluation_period_id:"Q2-2026", product_usage_trend_pct:-0.42, nps_score_trend:-0.38, support_ticket_volume_trend_pct:0.68, avg_ticket_severity_score:0.82, renewal_probability_score:0.12, last_exec_engagement_days:118, champion_change_events:4, contract_utilization_pct:0.18, multi_product_adoption_rate_pct:0.05, qbr_attendance_rate_pct:0.10, expansion_pipeline_vs_arr_pct:0.01, risk_flags_documented:6, competitor_evaluation_signals:4, time_to_value_days:125, onboarding_completion_rate_pct:0.25, stakeholder_coverage_score:0.10, satisfaction_survey_response_rate:0.15, invoice_payment_on_time_rate_pct:0.52, total_accounts_managed:7, avg_arr_per_account_usd:165000 },
  { rep_id:"CH-007", region:"APAC",  evaluation_period_id:"Q2-2026", product_usage_trend_pct:-0.05, nps_score_trend:0.02, support_ticket_volume_trend_pct:0.18, avg_ticket_severity_score:0.32, renewal_probability_score:0.68, last_exec_engagement_days:32, champion_change_events:1, contract_utilization_pct:0.72, multi_product_adoption_rate_pct:0.45, qbr_attendance_rate_pct:0.68, expansion_pipeline_vs_arr_pct:0.18, risk_flags_documented:1, competitor_evaluation_signals:0, time_to_value_days:32, onboarding_completion_rate_pct:0.82, stakeholder_coverage_score:0.58, satisfaction_survey_response_rate:0.68, invoice_payment_on_time_rate_pct:0.92, total_accounts_managed:10, avg_arr_per_account_usd:110000 },
  { rep_id:"CH-008", region:"NAMER", evaluation_period_id:"Q2-2026", product_usage_trend_pct:-0.15, nps_score_trend:-0.12, support_ticket_volume_trend_pct:0.38, avg_ticket_severity_score:0.52, renewal_probability_score:0.45, last_exec_engagement_days:62, champion_change_events:2, contract_utilization_pct:0.48, multi_product_adoption_rate_pct:0.25, qbr_attendance_rate_pct:0.38, expansion_pipeline_vs_arr_pct:0.06, risk_flags_documented:3, competitor_evaluation_signals:1, time_to_value_days:58, onboarding_completion_rate_pct:0.58, stakeholder_coverage_score:0.32, satisfaction_survey_response_rate:0.45, invoice_payment_on_time_rate_pct:0.80, total_accounts_managed:9, avg_arr_per_account_usd:122000 },
];

type Rep = typeof MOCK_REPS[0];

function engagementScore(i: Rep): number {
  let s = 0;
  if      (i.last_exec_engagement_days  >= 90)   s += 40; else if (i.last_exec_engagement_days >= 45) s += 22; else if (i.last_exec_engagement_days >= 21) s += 8;
  if      (i.qbr_attendance_rate_pct    <= 0.25) s += 35; else if (i.qbr_attendance_rate_pct <= 0.55) s += 18;
  if      (i.stakeholder_coverage_score <= 0.20) s += 25; else if (i.stakeholder_coverage_score <= 0.45) s += 12;
  return Math.min(s, 100);
}
function adoptionScore(i: Rep): number {
  let s = 0;
  if      (i.product_usage_trend_pct        <= -0.25) s += 45; else if (i.product_usage_trend_pct <= -0.10) s += 25; else if (i.product_usage_trend_pct <= 0.0) s += 10;
  if      (i.contract_utilization_pct       <= 0.30)  s += 30; else if (i.contract_utilization_pct <= 0.60) s += 15;
  if      (i.onboarding_completion_rate_pct <= 0.40)  s += 25; else if (i.onboarding_completion_rate_pct <= 0.70) s += 12;
  return Math.min(s, 100);
}
function satisfactionScore(i: Rep): number {
  let s = 0;
  if      (i.nps_score_trend                   <= -0.30) s += 40; else if (i.nps_score_trend <= -0.10) s += 22; else if (i.nps_score_trend <= 0.0) s += 8;
  if      (i.support_ticket_volume_trend_pct   >= 0.50)  s += 35; else if (i.support_ticket_volume_trend_pct >= 0.25) s += 18;
  if      (i.avg_ticket_severity_score         >= 0.65)  s += 25; else if (i.avg_ticket_severity_score >= 0.40) s += 12;
  return Math.min(s, 100);
}
function renewalReadinessScore(i: Rep): number {
  let s = 0;
  if      (i.renewal_probability_score    <= 0.30) s += 45; else if (i.renewal_probability_score <= 0.55) s += 25; else if (i.renewal_probability_score <= 0.75) s += 10;
  if      (i.competitor_evaluation_signals >= 3)   s += 30; else if (i.competitor_evaluation_signals >= 1) s += 15;
  if      (i.risk_flags_documented        >= 4)    s += 25; else if (i.risk_flags_documented >= 2) s += 12;
  return Math.min(s, 100);
}
function composite(en: number, ad: number, sa: number, rr: number): number {
  return Math.min(Math.round((en * 0.25 + ad * 0.30 + sa * 0.25 + rr * 0.20) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.renewal_probability_score <= 0.35 && i.risk_flags_documented >= 2 && i.competitor_evaluation_signals >= 1) return "silent_churn_risk";
  if (i.expansion_pipeline_vs_arr_pct <= 0.05 && i.multi_product_adoption_rate_pct <= 0.15) return "expansion_blocker";
  if (i.champion_change_events >= 2 && i.stakeholder_coverage_score <= 0.30) return "champion_departed";
  if (i.product_usage_trend_pct <= -0.20 && i.contract_utilization_pct <= 0.40) return "usage_collapse";
  if (i.support_ticket_volume_trend_pct >= 0.50 && i.avg_ticket_severity_score >= 0.55) return "support_spiral";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "churning"; if (c >= 40) return "at_risk"; if (c >= 20) return "declining"; return "healthy"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "silent_churn_risk" || p === "champion_departed") return "churn_prevention_task_force"; return "executive_business_review"; }
  if (r === "high") { if (p === "silent_churn_risk") return "executive_business_review"; if (p === "expansion_blocker") return "usage_enablement_program"; if (p === "champion_departed") return "champion_rebuild_plan"; if (p === "usage_collapse") return "usage_enablement_program"; if (p === "support_spiral") return "support_escalation_review"; return "executive_business_review"; }
  if (r === "moderate") return "health_monitoring";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Customer health stable — usage, NPS trend, renewal probability, and engagement within healthy benchmarks";
  const labels: Record<string,string> = { silent_churn_risk:"Silent churn risk", expansion_blocker:"Expansion blocker", champion_departed:"Champion departed", usage_collapse:"Usage collapse", support_spiral:"Support spiral" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  const usage = Math.round(i.product_usage_trend_pct * 100);
  const sign = usage >= 0 ? "+" : "";
  return `${label} — ${sign}${usage}% usage trend — ${Math.round(i.renewal_probability_score*100)}% renewal probability — ${Math.round(i.last_exec_engagement_days)}d since exec contact — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(i => {
      const en = engagementScore(i), ad = adoptionScore(i), sa = satisfactionScore(i), rr = renewalReadinessScore(i);
      const comp = composite(en, ad, sa, rr), pat = pattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      const churnP = (comp/100) * (1.0 - i.renewal_probability_score);
      const ca = Math.round(i.total_accounts_managed * i.avg_arr_per_account_usd * churnP * 100) / 100;
      return {
        rep_id: i.rep_id, region: i.region,
        health_risk: r, health_pattern: pat, health_severity: sev, recommended_action: act,
        engagement_score: en, adoption_score: ad, satisfaction_score: sa, renewal_readiness_score: rr,
        health_composite: comp,
        has_health_gap: comp >= 40 || i.renewal_probability_score <= 0.65 || i.product_usage_trend_pct <= -0.05,
        requires_health_intervention: comp >= 25 || i.competitor_evaluation_signals >= 1 || i.champion_change_events >= 1,
        estimated_churn_arr_usd: ca,
        health_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let ten=0, tad=0, tsa=0, trr=0, tcomp=0, tca=0, gc=0, ic=0;
    for (const r of reps) {
      rc[r.health_risk]=(rc[r.health_risk]||0)+1; pc[r.health_pattern]=(pc[r.health_pattern]||0)+1;
      sc[r.health_severity]=(sc[r.health_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      ten+=r.engagement_score; tad+=r.adoption_score; tsa+=r.satisfaction_score; trr+=r.renewal_readiness_score;
      tcomp+=r.health_composite; tca+=r.estimated_churn_arr_usd;
      if (r.has_health_gap) gc++; if (r.requires_health_intervention) ic++;
    }
    const n = reps.length;
    return NextResponse.json({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_health_composite: Math.round(tcomp/n*10)/10,
      health_gap_count: gc, intervention_count: ic,
      avg_engagement_score: Math.round(ten/n*10)/10,
      avg_adoption_score: Math.round(tad/n*10)/10,
      avg_satisfaction_score: Math.round(tsa/n*10)/10,
      avg_renewal_readiness_score: Math.round(trr/n*10)/10,
      total_estimated_churn_arr_usd: Math.round(tca*100)/100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-customer-health-score-deterioration-engine`)).json());
}
