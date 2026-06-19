import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"BR-001", region:"EMEA",  evaluation_period_id:"Q1-2026", outbound_activity_decay_rate_pct:0.55, meetings_booked_decay_rate_pct:0.50, pipeline_creation_decay_rate_pct:0.48, avg_response_time_increase_pct:0.60, proposal_error_rate_pct:0.32, crm_entry_accuracy_drop_pct:0.40, follow_up_timeliness_score:0.25, call_quality_score_decay_pct:0.45, manager_meeting_attendance_rate_pct:0.45, team_activity_participation_rate_pct:0.40, enablement_session_attendance_rate_pct:0.30, voluntary_overtime_rate_pct:0.55, weekend_work_frequency_pct:0.60, avg_daily_work_hours:12.5, vacation_utilization_pct:0.10, deal_abandonment_rate_pct:0.28, prospecting_avoidance_rate_pct:0.55, quota_attainment_trend:0.45, total_active_deals:18, avg_deal_value_usd:85000 },
  { rep_id:"BR-002", region:"NAMER", evaluation_period_id:"Q1-2026", outbound_activity_decay_rate_pct:0.08, meetings_booked_decay_rate_pct:0.05, pipeline_creation_decay_rate_pct:0.06, avg_response_time_increase_pct:0.10, proposal_error_rate_pct:0.04, crm_entry_accuracy_drop_pct:0.05, follow_up_timeliness_score:0.88, call_quality_score_decay_pct:0.05, manager_meeting_attendance_rate_pct:0.95, team_activity_participation_rate_pct:0.92, enablement_session_attendance_rate_pct:0.88, voluntary_overtime_rate_pct:0.08, weekend_work_frequency_pct:0.10, avg_daily_work_hours:8.5, vacation_utilization_pct:0.85, deal_abandonment_rate_pct:0.04, prospecting_avoidance_rate_pct:0.06, quota_attainment_trend:0.92, total_active_deals:32, avg_deal_value_usd:110000 },
  { rep_id:"BR-003", region:"APAC",  evaluation_period_id:"Q1-2026", outbound_activity_decay_rate_pct:0.35, meetings_booked_decay_rate_pct:0.30, pipeline_creation_decay_rate_pct:0.28, avg_response_time_increase_pct:0.38, proposal_error_rate_pct:0.18, crm_entry_accuracy_drop_pct:0.22, follow_up_timeliness_score:0.50, call_quality_score_decay_pct:0.28, manager_meeting_attendance_rate_pct:0.68, team_activity_participation_rate_pct:0.62, enablement_session_attendance_rate_pct:0.55, voluntary_overtime_rate_pct:0.32, weekend_work_frequency_pct:0.38, avg_daily_work_hours:10.5, vacation_utilization_pct:0.38, deal_abandonment_rate_pct:0.15, prospecting_avoidance_rate_pct:0.32, quota_attainment_trend:0.68, total_active_deals:22, avg_deal_value_usd:75000 },
  { rep_id:"BR-004", region:"LATAM", evaluation_period_id:"Q1-2026", outbound_activity_decay_rate_pct:0.05, meetings_booked_decay_rate_pct:0.04, pipeline_creation_decay_rate_pct:0.04, avg_response_time_increase_pct:0.06, proposal_error_rate_pct:0.02, crm_entry_accuracy_drop_pct:0.03, follow_up_timeliness_score:0.92, call_quality_score_decay_pct:0.03, manager_meeting_attendance_rate_pct:0.98, team_activity_participation_rate_pct:0.95, enablement_session_attendance_rate_pct:0.92, voluntary_overtime_rate_pct:0.05, weekend_work_frequency_pct:0.06, avg_daily_work_hours:8.0, vacation_utilization_pct:0.90, deal_abandonment_rate_pct:0.02, prospecting_avoidance_rate_pct:0.04, quota_attainment_trend:0.96, total_active_deals:15, avg_deal_value_usd:60000 },
  { rep_id:"BR-005", region:"EMEA",  evaluation_period_id:"Q1-2026", outbound_activity_decay_rate_pct:0.62, meetings_booked_decay_rate_pct:0.58, pipeline_creation_decay_rate_pct:0.55, avg_response_time_increase_pct:0.70, proposal_error_rate_pct:0.38, crm_entry_accuracy_drop_pct:0.48, follow_up_timeliness_score:0.18, call_quality_score_decay_pct:0.55, manager_meeting_attendance_rate_pct:0.38, team_activity_participation_rate_pct:0.32, enablement_session_attendance_rate_pct:0.22, voluntary_overtime_rate_pct:0.62, weekend_work_frequency_pct:0.68, avg_daily_work_hours:13.5, vacation_utilization_pct:0.05, deal_abandonment_rate_pct:0.35, prospecting_avoidance_rate_pct:0.65, quota_attainment_trend:0.38, total_active_deals:25, avg_deal_value_usd:95000 },
  { rep_id:"BR-006", region:"NAMER", evaluation_period_id:"Q1-2026", outbound_activity_decay_rate_pct:0.18, meetings_booked_decay_rate_pct:0.15, pipeline_creation_decay_rate_pct:0.14, avg_response_time_increase_pct:0.20, proposal_error_rate_pct:0.09, crm_entry_accuracy_drop_pct:0.10, follow_up_timeliness_score:0.75, call_quality_score_decay_pct:0.12, manager_meeting_attendance_rate_pct:0.85, team_activity_participation_rate_pct:0.80, enablement_session_attendance_rate_pct:0.72, voluntary_overtime_rate_pct:0.18, weekend_work_frequency_pct:0.20, avg_daily_work_hours:9.0, vacation_utilization_pct:0.65, deal_abandonment_rate_pct:0.08, prospecting_avoidance_rate_pct:0.15, quota_attainment_trend:0.82, total_active_deals:28, avg_deal_value_usd:92000 },
  { rep_id:"BR-007", region:"APAC",  evaluation_period_id:"Q1-2026", outbound_activity_decay_rate_pct:0.48, meetings_booked_decay_rate_pct:0.44, pipeline_creation_decay_rate_pct:0.42, avg_response_time_increase_pct:0.52, proposal_error_rate_pct:0.28, crm_entry_accuracy_drop_pct:0.35, follow_up_timeliness_score:0.35, call_quality_score_decay_pct:0.40, manager_meeting_attendance_rate_pct:0.52, team_activity_participation_rate_pct:0.48, enablement_session_attendance_rate_pct:0.38, voluntary_overtime_rate_pct:0.48, weekend_work_frequency_pct:0.52, avg_daily_work_hours:11.5, vacation_utilization_pct:0.18, deal_abandonment_rate_pct:0.24, prospecting_avoidance_rate_pct:0.48, quota_attainment_trend:0.55, total_active_deals:20, avg_deal_value_usd:80000 },
  { rep_id:"BR-008", region:"MEA",   evaluation_period_id:"Q1-2026", outbound_activity_decay_rate_pct:0.22, meetings_booked_decay_rate_pct:0.18, pipeline_creation_decay_rate_pct:0.16, avg_response_time_increase_pct:0.25, proposal_error_rate_pct:0.11, crm_entry_accuracy_drop_pct:0.14, follow_up_timeliness_score:0.68, call_quality_score_decay_pct:0.15, manager_meeting_attendance_rate_pct:0.78, team_activity_participation_rate_pct:0.72, enablement_session_attendance_rate_pct:0.65, voluntary_overtime_rate_pct:0.22, weekend_work_frequency_pct:0.25, avg_daily_work_hours:9.5, vacation_utilization_pct:0.55, deal_abandonment_rate_pct:0.10, prospecting_avoidance_rate_pct:0.20, quota_attainment_trend:0.78, total_active_deals:24, avg_deal_value_usd:70000 },
];

type Rep = typeof MOCK_REPS[0];

function activityScore(i: Rep): number {
  let s = 0;
  if      (i.outbound_activity_decay_rate_pct >= 0.50) s += 40; else if (i.outbound_activity_decay_rate_pct >= 0.30) s += 22; else if (i.outbound_activity_decay_rate_pct >= 0.15) s += 8;
  if      (i.pipeline_creation_decay_rate_pct >= 0.45) s += 35; else if (i.pipeline_creation_decay_rate_pct >= 0.25) s += 18;
  if      (i.prospecting_avoidance_rate_pct   >= 0.50) s += 25; else if (i.prospecting_avoidance_rate_pct >= 0.30) s += 12;
  return Math.min(s, 100);
}
function qualityScore(i: Rep): number {
  let s = 0;
  if      (i.proposal_error_rate_pct      >= 0.30) s += 40; else if (i.proposal_error_rate_pct >= 0.15) s += 22; else if (i.proposal_error_rate_pct >= 0.07) s += 8;
  if      (i.follow_up_timeliness_score   <= 0.30) s += 35; else if (i.follow_up_timeliness_score <= 0.55) s += 18;
  if      (i.deal_abandonment_rate_pct    >= 0.25) s += 25; else if (i.deal_abandonment_rate_pct >= 0.12) s += 12;
  return Math.min(s, 100);
}
function engagementScore(i: Rep): number {
  let s = 0;
  if      (i.manager_meeting_attendance_rate_pct     <= 0.55) s += 45; else if (i.manager_meeting_attendance_rate_pct <= 0.75) s += 25; else if (i.manager_meeting_attendance_rate_pct <= 0.88) s += 10;
  if      (i.enablement_session_attendance_rate_pct  <= 0.35) s += 30; else if (i.enablement_session_attendance_rate_pct <= 0.60) s += 15;
  if      (i.vacation_utilization_pct               <= 0.20) s += 25; else if (i.vacation_utilization_pct <= 0.45) s += 12;
  return Math.min(s, 100);
}
function stressScore(i: Rep): number {
  let s = 0;
  if      (i.weekend_work_frequency_pct   >= 0.55) s += 45; else if (i.weekend_work_frequency_pct >= 0.35) s += 25; else if (i.weekend_work_frequency_pct >= 0.20) s += 10;
  if      (i.avg_daily_work_hours         >= 12.0) s += 30; else if (i.avg_daily_work_hours >= 10.0) s += 15;
  if      (i.voluntary_overtime_rate_pct  >= 0.50) s += 25; else if (i.voluntary_overtime_rate_pct >= 0.30) s += 12;
  return Math.min(s, 100);
}
function composite(ac: number, qu: number, en: number, st: number): number {
  return Math.min(Math.round((ac * 0.30 + qu * 0.25 + en * 0.25 + st * 0.20) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.outbound_activity_decay_rate_pct >= 0.45 && i.pipeline_creation_decay_rate_pct >= 0.40) return "activity_cliff";
  if (i.proposal_error_rate_pct >= 0.25 && i.follow_up_timeliness_score <= 0.40)                return "quality_erosion";
  if (i.weekend_work_frequency_pct >= 0.50 && i.avg_daily_work_hours >= 11.0)                   return "weekend_overload";
  if (i.manager_meeting_attendance_rate_pct <= 0.60 && i.enablement_session_attendance_rate_pct <= 0.40) return "disengagement_spiral";
  if (i.deal_abandonment_rate_pct >= 0.22 && i.prospecting_avoidance_rate_pct >= 0.35)          return "pipeline_withdrawal";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "burned_out"; if (c >= 40) return "fatigued"; if (c >= 20) return "stressed"; return "thriving"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "activity_cliff" || p === "pipeline_withdrawal") return "retention_risk_escalation"; return "immediate_support_intervention"; }
  if (r === "high") {
    if (p === "activity_cliff")        return "quota_relief_assessment";
    if (p === "quality_erosion")       return "coaching_cadence_increase";
    if (p === "weekend_overload")      return "territory_rebalancing";
    if (p === "disengagement_spiral")  return "manager_wellbeing_check_in";
    if (p === "pipeline_withdrawal")   return "workload_review_conversation";
    return "productivity_monitoring";
  }
  if (r === "moderate") return "productivity_monitoring";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Rep productivity healthy — activity levels, quality, engagement and stress indicators within benchmark targets";
  const labels: Record<string,string> = { activity_cliff:"Activity cliff", quality_erosion:"Quality erosion", disengagement_spiral:"Disengagement spiral", weekend_overload:"Weekend overload", pipeline_withdrawal:"Pipeline withdrawal" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(i.outbound_activity_decay_rate_pct*100)}% activity decay — ${Math.round(i.weekend_work_frequency_pct*100)}% weekend work — ${Math.round(i.quota_attainment_trend*100)}% quota trend — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(i => {
      const ac = activityScore(i), qu = qualityScore(i), en = engagementScore(i), st = stressScore(i);
      const comp = composite(ac, qu, en, st), pat = pattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      const loss = Math.round(i.total_active_deals * i.avg_deal_value_usd * (1 - i.quota_attainment_trend) * (comp/100) * 100) / 100;
      return {
        rep_id: i.rep_id, region: i.region,
        burnout_risk: r, burnout_pattern: pat, burnout_severity: sev, recommended_action: act,
        activity_score: ac, quality_score: qu, engagement_score: en, stress_score: st,
        burnout_composite: comp,
        has_burnout_signal: comp >= 40 || i.outbound_activity_decay_rate_pct >= 0.30 || i.quota_attainment_trend <= 0.70,
        requires_manager_action: comp >= 25 || i.manager_meeting_attendance_rate_pct <= 0.75 || i.weekend_work_frequency_pct >= 0.30,
        estimated_productivity_loss_usd: loss,
        burnout_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tac=0, tqu=0, ten=0, tst=0, tcomp=0, tpl=0, gc=0, mc=0;
    for (const r of reps) {
      rc[r.burnout_risk]=(rc[r.burnout_risk]||0)+1; pc[r.burnout_pattern]=(pc[r.burnout_pattern]||0)+1;
      sc[r.burnout_severity]=(sc[r.burnout_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      tac+=r.activity_score; tqu+=r.quality_score; ten+=r.engagement_score; tst+=r.stress_score;
      tcomp+=r.burnout_composite; tpl+=r.estimated_productivity_loss_usd;
      if (r.has_burnout_signal) gc++; if (r.requires_manager_action) mc++;
    }
    const n = reps.length;
    return NextResponse.json(sealResponse({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_burnout_composite: Math.round(tcomp/n*10)/10,
      burnout_signal_count: gc, manager_action_count: mc,
      avg_activity_score: Math.round(tac/n*10)/10,
      avg_quality_score: Math.round(tqu/n*10)/10,
      avg_engagement_score: Math.round(ten/n*10)/10,
      avg_stress_score: Math.round(tst/n*10)/10,
      total_estimated_productivity_loss_usd: Math.round(tpl*100)/100,
    }} as Record<string,unknown>));
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-rep-burnout-productivity-decay-engine`)).json());
}
