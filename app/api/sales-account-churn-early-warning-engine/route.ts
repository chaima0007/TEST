import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ACCOUNTS = [
  { account_id:"CH-001", region:"EMEA",  evaluation_period_id:"Q1-2026", product_usage_decay_pct:0.55, feature_adoption_rate_pct:0.22, login_frequency_decay_pct:0.50, api_call_volume_decay_pct:0.48, executive_sponsor_engaged:0.18, champion_tenure_months:3.0, stakeholder_count_change:-4.0, last_exec_meeting_days_ago:130.0, open_support_tickets:9, avg_ticket_resolution_days:16.0, nps_score_change:-35.0, escalation_frequency_pct:0.45, competitive_evaluation_signal:0.65, roi_achievement_pct:0.28, contract_utilization_pct:0.25, renewal_conversation_initiated:0.0, arr_usd:180000, contract_months_remaining:2, days_to_renewal:55 },
  { account_id:"CH-002", region:"NAMER", evaluation_period_id:"Q1-2026", product_usage_decay_pct:0.05, feature_adoption_rate_pct:0.88, login_frequency_decay_pct:0.04, api_call_volume_decay_pct:0.06, executive_sponsor_engaged:0.92, champion_tenure_months:24.0, stakeholder_count_change:2.0, last_exec_meeting_days_ago:18.0, open_support_tickets:1, avg_ticket_resolution_days:2.0, nps_score_change:12.0, escalation_frequency_pct:0.05, competitive_evaluation_signal:0.05, roi_achievement_pct:1.20, contract_utilization_pct:0.92, renewal_conversation_initiated:1.0, arr_usd:250000, contract_months_remaining:8, days_to_renewal:240 },
  { account_id:"CH-003", region:"APAC",  evaluation_period_id:"Q1-2026", product_usage_decay_pct:0.28, feature_adoption_rate_pct:0.48, login_frequency_decay_pct:0.25, api_call_volume_decay_pct:0.22, executive_sponsor_engaged:0.55, champion_tenure_months:8.0, stakeholder_count_change:-1.0, last_exec_meeting_days_ago:55.0, open_support_tickets:4, avg_ticket_resolution_days:8.0, nps_score_change:-8.0, escalation_frequency_pct:0.18, competitive_evaluation_signal:0.30, roi_achievement_pct:0.65, contract_utilization_pct:0.58, renewal_conversation_initiated:0.5, arr_usd:120000, contract_months_remaining:4, days_to_renewal:115 },
  { account_id:"CH-004", region:"LATAM", evaluation_period_id:"Q1-2026", product_usage_decay_pct:0.02, feature_adoption_rate_pct:0.92, login_frequency_decay_pct:0.02, api_call_volume_decay_pct:0.03, executive_sponsor_engaged:0.95, champion_tenure_months:36.0, stakeholder_count_change:4.0, last_exec_meeting_days_ago:12.0, open_support_tickets:0, avg_ticket_resolution_days:1.5, nps_score_change:18.0, escalation_frequency_pct:0.02, competitive_evaluation_signal:0.02, roi_achievement_pct:1.40, contract_utilization_pct:0.96, renewal_conversation_initiated:1.0, arr_usd:85000, contract_months_remaining:10, days_to_renewal:300 },
  { account_id:"CH-005", region:"EMEA",  evaluation_period_id:"Q1-2026", product_usage_decay_pct:0.62, feature_adoption_rate_pct:0.15, login_frequency_decay_pct:0.58, api_call_volume_decay_pct:0.60, executive_sponsor_engaged:0.10, champion_tenure_months:2.0, stakeholder_count_change:-6.0, last_exec_meeting_days_ago:160.0, open_support_tickets:14, avg_ticket_resolution_days:22.0, nps_score_change:-45.0, escalation_frequency_pct:0.55, competitive_evaluation_signal:0.78, roi_achievement_pct:0.18, contract_utilization_pct:0.15, renewal_conversation_initiated:0.0, arr_usd:320000, contract_months_remaining:1, days_to_renewal:28 },
  { account_id:"CH-006", region:"NAMER", evaluation_period_id:"Q1-2026", product_usage_decay_pct:0.12, feature_adoption_rate_pct:0.72, login_frequency_decay_pct:0.10, api_call_volume_decay_pct:0.12, executive_sponsor_engaged:0.78, champion_tenure_months:15.0, stakeholder_count_change:1.0, last_exec_meeting_days_ago:28.0, open_support_tickets:2, avg_ticket_resolution_days:4.0, nps_score_change:5.0, escalation_frequency_pct:0.08, competitive_evaluation_signal:0.12, roi_achievement_pct:0.95, contract_utilization_pct:0.80, renewal_conversation_initiated:0.8, arr_usd:195000, contract_months_remaining:6, days_to_renewal:180 },
  { account_id:"CH-007", region:"APAC",  evaluation_period_id:"Q1-2026", product_usage_decay_pct:0.38, feature_adoption_rate_pct:0.32, login_frequency_decay_pct:0.35, api_call_volume_decay_pct:0.30, executive_sponsor_engaged:0.30, champion_tenure_months:5.0, stakeholder_count_change:-3.0, last_exec_meeting_days_ago:90.0, open_support_tickets:7, avg_ticket_resolution_days:12.0, nps_score_change:-20.0, escalation_frequency_pct:0.32, competitive_evaluation_signal:0.55, roi_achievement_pct:0.42, contract_utilization_pct:0.35, renewal_conversation_initiated:0.2, arr_usd:145000, contract_months_remaining:3, days_to_renewal:80 },
  { account_id:"CH-008", region:"MEA",   evaluation_period_id:"Q1-2026", product_usage_decay_pct:0.18, feature_adoption_rate_pct:0.62, login_frequency_decay_pct:0.15, api_call_volume_decay_pct:0.16, executive_sponsor_engaged:0.65, champion_tenure_months:12.0, stakeholder_count_change:0.0, last_exec_meeting_days_ago:40.0, open_support_tickets:3, avg_ticket_resolution_days:6.0, nps_score_change:-2.0, escalation_frequency_pct:0.12, competitive_evaluation_signal:0.22, roi_achievement_pct:0.80, contract_utilization_pct:0.68, renewal_conversation_initiated:0.6, arr_usd:105000, contract_months_remaining:5, days_to_renewal:145 },
];

type Acct = typeof MOCK_ACCOUNTS[0];

function usageScore(i: Acct): number {
  let s = 0;
  if      (i.product_usage_decay_pct   >= 0.50) s += 40; else if (i.product_usage_decay_pct >= 0.30) s += 22; else if (i.product_usage_decay_pct >= 0.15) s += 8;
  if      (i.feature_adoption_rate_pct <= 0.25) s += 35; else if (i.feature_adoption_rate_pct <= 0.45) s += 18; else if (i.feature_adoption_rate_pct <= 0.60) s += 6;
  if      (i.login_frequency_decay_pct >= 0.50) s += 25; else if (i.login_frequency_decay_pct >= 0.30) s += 12;
  return Math.min(s, 100);
}
function relationshipScore(i: Acct): number {
  let s = 0;
  if      (i.executive_sponsor_engaged  <= 0.20) s += 40; else if (i.executive_sponsor_engaged <= 0.45) s += 22; else if (i.executive_sponsor_engaged <= 0.65) s += 8;
  if      (i.last_exec_meeting_days_ago >= 120)  s += 35; else if (i.last_exec_meeting_days_ago >= 60) s += 18; else if (i.last_exec_meeting_days_ago >= 30) s += 6;
  if      (i.stakeholder_count_change   <= -3)   s += 25; else if (i.stakeholder_count_change <= -1) s += 12;
  return Math.min(s, 100);
}
function supportScore(i: Acct): number {
  let s = 0;
  if      (i.open_support_tickets       >= 10)   s += 40; else if (i.open_support_tickets >= 5) s += 22; else if (i.open_support_tickets >= 2) s += 8;
  if      (i.escalation_frequency_pct  >= 0.40) s += 35; else if (i.escalation_frequency_pct >= 0.20) s += 18;
  if      (i.avg_ticket_resolution_days >= 14)   s += 25; else if (i.avg_ticket_resolution_days >= 7) s += 12;
  return Math.min(s, 100);
}
function valueScore(i: Acct): number {
  let s = 0;
  if      (i.roi_achievement_pct            <= 0.30) s += 45; else if (i.roi_achievement_pct <= 0.55) s += 25; else if (i.roi_achievement_pct <= 0.75) s += 10;
  if      (i.competitive_evaluation_signal  >= 0.60) s += 30; else if (i.competitive_evaluation_signal >= 0.35) s += 15;
  if      (i.contract_utilization_pct       <= 0.30) s += 25; else if (i.contract_utilization_pct <= 0.55) s += 12;
  return Math.min(s, 100);
}
function composite(us: number, re: number, su: number, va: number): number {
  return Math.min(Math.round((us * 0.30 + re * 0.25 + su * 0.25 + va * 0.20) * 100) / 100, 100);
}
function pattern(i: Acct): string {
  if (i.product_usage_decay_pct >= 0.45 && i.login_frequency_decay_pct >= 0.40)           return "usage_collapse";
  if (i.executive_sponsor_engaged <= 0.25 && i.stakeholder_count_change <= -2)             return "sponsor_exodus";
  if (i.open_support_tickets >= 6 && i.escalation_frequency_pct >= 0.30)                  return "support_spiral";
  if (i.competitive_evaluation_signal >= 0.55 && i.roi_achievement_pct <= 0.60)            return "competitive_switch";
  if (i.roi_achievement_pct <= 0.40 && i.contract_utilization_pct <= 0.40)                return "value_gap_crisis";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "churning"; if (c >= 40) return "at_risk"; if (c >= 20) return "watching"; return "healthy"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "sponsor_exodus" || p === "competitive_switch") return "executive_save_call"; return "renewal_risk_intervention"; }
  if (r === "high") {
    if (p === "usage_collapse")     return "success_plan_reset";
    if (p === "sponsor_exodus")     return "sponsor_re_engagement";
    if (p === "support_spiral")     return "support_escalation_resolution";
    if (p === "competitive_switch") return "competitive_defense_playbook";
    if (p === "value_gap_crisis")   return "executive_business_review";
    return "health_monitoring";
  }
  if (r === "moderate") return "health_monitoring";
  return "no_action";
}
function signal(i: Acct, pat: string, comp: number): string {
  if (comp < 20) return "Account health strong — usage, relationship, support and value indicators within healthy benchmarks";
  const labels: Record<string,string> = { usage_collapse:"Usage collapse", sponsor_exodus:"Sponsor exodus", support_spiral:"Support spiral", competitive_switch:"Competitive switch", value_gap_crisis:"Value gap crisis" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(i.product_usage_decay_pct*100)}% usage decay — ${Math.round(i.roi_achievement_pct*100)}% ROI achieved — ${i.days_to_renewal}d to renewal — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const accounts = MOCK_ACCOUNTS.map(i => {
      const us = usageScore(i), re = relationshipScore(i), su = supportScore(i), va = valueScore(i);
      const comp = composite(us, re, su, va), pat = pattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      return {
        account_id: i.account_id, region: i.region,
        churn_risk: r, churn_pattern: pat, churn_severity: sev, recommended_action: act,
        usage_score: us, relationship_score: re, support_score: su, value_score: va,
        churn_composite: comp,
        has_churn_signal: comp >= 40 || i.product_usage_decay_pct >= 0.30 || i.days_to_renewal <= 90,
        requires_executive_action: comp >= 25 || i.executive_sponsor_engaged <= 0.40 || i.competitive_evaluation_signal >= 0.35,
        estimated_arr_at_risk_usd: Math.round(i.arr_usd * (comp/100) * 100) / 100,
        churn_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tus=0,tre=0,tsu=0,tva=0,tcomp=0,tarr=0,gc=0,ec=0;
    for (const a of accounts) {
      rc[a.churn_risk]=(rc[a.churn_risk]||0)+1; pc[a.churn_pattern]=(pc[a.churn_pattern]||0)+1;
      sc[a.churn_severity]=(sc[a.churn_severity]||0)+1; ac[a.recommended_action]=(ac[a.recommended_action]||0)+1;
      tus+=a.usage_score; tre+=a.relationship_score; tsu+=a.support_score; tva+=a.value_score;
      tcomp+=a.churn_composite; tarr+=a.estimated_arr_at_risk_usd;
      if (a.has_churn_signal) gc++; if (a.requires_executive_action) ec++;
    }
    const n = accounts.length;
    return NextResponse.json(sealResponse({ accounts, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_churn_composite: Math.round(tcomp/n*10)/10,
      churn_signal_count: gc, executive_action_count: ec,
      avg_usage_score: Math.round(tus/n*10)/10,
      avg_relationship_score: Math.round(tre/n*10)/10,
      avg_support_score: Math.round(tsu/n*10)/10,
      avg_value_score: Math.round(tva/n*10)/10,
      total_estimated_arr_at_risk_usd: Math.round(tarr*100)/100,
    }} as Record<string,unknown>));
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-account-churn-early-warning-engine`)).json());
}
