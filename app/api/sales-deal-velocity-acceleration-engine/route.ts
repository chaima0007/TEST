import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_DEALS = [
  { deal_id:"DV-001", region:"EMEA",  pipeline_stage:"proposal",           days_in_current_stage:58, expected_stage_duration_days:14, stage_regression_count:3, last_activity_days_ago:18, decision_date_pushed_count:5, decision_criteria_agreed:0.12, procurement_engaged:0.08, legal_review_started:0.0, stakeholder_response_rate_pct:0.10, active_stakeholder_count:1, economic_buyer_engaged:0.08, multithreading_score:0.08, champion_last_contact_days:28, champion_sentiment_score:0.15, champion_internal_advocacy:0.08, budget_confirmed:0.08, deal_value_usd:280000, days_to_close_target:8, win_probability_pct:0.12 },
  { deal_id:"DV-002", region:"NAMER", pipeline_stage:"discovery",          days_in_current_stage:4,  expected_stage_duration_days:7,  stage_regression_count:0, last_activity_days_ago:1,  decision_date_pushed_count:0, decision_criteria_agreed:0.85, procurement_engaged:0.80, legal_review_started:0.0, stakeholder_response_rate_pct:0.90, active_stakeholder_count:6, economic_buyer_engaged:0.88, multithreading_score:0.85, champion_last_contact_days:2,  champion_sentiment_score:0.90, champion_internal_advocacy:0.88, budget_confirmed:0.85, deal_value_usd:95000,  days_to_close_target:45, win_probability_pct:0.82 },
  { deal_id:"DV-003", region:"APAC",  pipeline_stage:"negotiation",        days_in_current_stage:28, expected_stage_duration_days:14, stage_regression_count:1, last_activity_days_ago:8,  decision_date_pushed_count:2, decision_criteria_agreed:0.45, procurement_engaged:0.40, legal_review_started:0.5, stakeholder_response_rate_pct:0.38, active_stakeholder_count:3, economic_buyer_engaged:0.40, multithreading_score:0.38, champion_last_contact_days:12, champion_sentiment_score:0.50, champion_internal_advocacy:0.42, budget_confirmed:0.40, deal_value_usd:145000, days_to_close_target:18, win_probability_pct:0.50 },
  { deal_id:"DV-004", region:"LATAM", pipeline_stage:"proof_of_concept",   days_in_current_stage:3,  expected_stage_duration_days:10, stage_regression_count:0, last_activity_days_ago:1,  decision_date_pushed_count:0, decision_criteria_agreed:0.92, procurement_engaged:0.88, legal_review_started:0.0, stakeholder_response_rate_pct:0.92, active_stakeholder_count:5, economic_buyer_engaged:0.90, multithreading_score:0.90, champion_last_contact_days:1,  champion_sentiment_score:0.92, champion_internal_advocacy:0.90, budget_confirmed:0.92, deal_value_usd:200000, days_to_close_target:60, win_probability_pct:0.88 },
  { deal_id:"DV-005", region:"EMEA",  pipeline_stage:"commercial_review",  days_in_current_stage:45, expected_stage_duration_days:10, stage_regression_count:2, last_activity_days_ago:14, decision_date_pushed_count:4, decision_criteria_agreed:0.18, procurement_engaged:0.12, legal_review_started:0.0, stakeholder_response_rate_pct:0.15, active_stakeholder_count:1, economic_buyer_engaged:0.10, multithreading_score:0.12, champion_last_contact_days:22, champion_sentiment_score:0.18, champion_internal_advocacy:0.10, budget_confirmed:0.10, deal_value_usd:420000, days_to_close_target:5,  win_probability_pct:0.08 },
  { deal_id:"DV-006", region:"NAMER", pipeline_stage:"qualification",      days_in_current_stage:10, expected_stage_duration_days:7,  stage_regression_count:0, last_activity_days_ago:3,  decision_date_pushed_count:1, decision_criteria_agreed:0.68, procurement_engaged:0.60, legal_review_started:0.0, stakeholder_response_rate_pct:0.70, active_stakeholder_count:4, economic_buyer_engaged:0.65, multithreading_score:0.65, champion_last_contact_days:3,  champion_sentiment_score:0.72, champion_internal_advocacy:0.68, budget_confirmed:0.65, deal_value_usd:120000, days_to_close_target:30, win_probability_pct:0.65 },
  { deal_id:"DV-007", region:"APAC",  pipeline_stage:"solution_demo",      days_in_current_stage:35, expected_stage_duration_days:12, stage_regression_count:2, last_activity_days_ago:12, decision_date_pushed_count:3, decision_criteria_agreed:0.28, procurement_engaged:0.22, legal_review_started:0.0, stakeholder_response_rate_pct:0.22, active_stakeholder_count:1, economic_buyer_engaged:0.20, multithreading_score:0.22, champion_last_contact_days:18, champion_sentiment_score:0.30, champion_internal_advocacy:0.22, budget_confirmed:0.22, deal_value_usd:195000, days_to_close_target:12, win_probability_pct:0.22 },
  { deal_id:"DV-008", region:"MEA",   pipeline_stage:"proposal",           days_in_current_stage:20, expected_stage_duration_days:14, stage_regression_count:1, last_activity_days_ago:5,  decision_date_pushed_count:2, decision_criteria_agreed:0.55, procurement_engaged:0.50, legal_review_started:0.5, stakeholder_response_rate_pct:0.55, active_stakeholder_count:3, economic_buyer_engaged:0.52, multithreading_score:0.52, champion_last_contact_days:6,  champion_sentiment_score:0.60, champion_internal_advocacy:0.55, budget_confirmed:0.55, deal_value_usd:160000, days_to_close_target:22, win_probability_pct:0.58 },
];

type Deal = typeof MOCK_DEALS[0];

function stallScore(i: Deal): number {
  const ageRatio = i.days_in_current_stage / Math.max(i.expected_stage_duration_days, 1);
  let s = 0;
  if      (ageRatio >= 2.0) s += 40; else if (ageRatio >= 1.5) s += 22; else if (ageRatio >= 1.2) s += 8;
  if      (i.last_activity_days_ago >= 14) s += 35; else if (i.last_activity_days_ago >= 7) s += 18; else if (i.last_activity_days_ago >= 4) s += 6;
  if      (i.stage_regression_count >= 2)  s += 25; else if (i.stage_regression_count >= 1) s += 12;
  return Math.min(s, 100);
}
function decisionScore(i: Deal): number {
  let s = 0;
  if      (i.decision_date_pushed_count >= 4)    s += 40; else if (i.decision_date_pushed_count >= 2) s += 22; else if (i.decision_date_pushed_count >= 1) s += 8;
  if      (i.decision_criteria_agreed   <= 0.30) s += 35; else if (i.decision_criteria_agreed <= 0.55) s += 18; else if (i.decision_criteria_agreed <= 0.75) s += 6;
  if      (i.procurement_engaged        <= 0.25) s += 25; else if (i.procurement_engaged <= 0.50) s += 12;
  return Math.min(s, 100);
}
function stakeholderScore(i: Deal): number {
  let s = 0;
  if      (i.stakeholder_response_rate_pct <= 0.20) s += 40; else if (i.stakeholder_response_rate_pct <= 0.40) s += 22; else if (i.stakeholder_response_rate_pct <= 0.60) s += 8;
  if      (i.economic_buyer_engaged         <= 0.20) s += 35; else if (i.economic_buyer_engaged <= 0.45) s += 18; else if (i.economic_buyer_engaged <= 0.65) s += 6;
  if      (i.multithreading_score           <= 0.25) s += 25; else if (i.multithreading_score <= 0.50) s += 12;
  return Math.min(s, 100);
}
function championScore(i: Deal): number {
  let s = 0;
  if      (i.champion_last_contact_days  >= 21)   s += 45; else if (i.champion_last_contact_days >= 10) s += 25; else if (i.champion_last_contact_days >= 5) s += 10;
  if      (i.champion_sentiment_score    <= 0.30) s += 30; else if (i.champion_sentiment_score <= 0.55) s += 15;
  if      (i.champion_internal_advocacy  <= 0.25) s += 25; else if (i.champion_internal_advocacy <= 0.50) s += 12;
  return Math.min(s, 100);
}
function composite(st: number, de: number, sk: number, ch: number): number {
  return Math.min(Math.round((st * 0.30 + de * 0.25 + sk * 0.25 + ch * 0.20) * 100) / 100, 100);
}
function pattern(i: Deal): string {
  const ageRatio = i.days_in_current_stage / Math.max(i.expected_stage_duration_days, 1);
  if (ageRatio >= 1.8 && i.last_activity_days_ago >= 10)                               return "stage_stall";
  if (i.decision_date_pushed_count >= 3 && i.decision_criteria_agreed <= 0.45)         return "decision_paralysis";
  if (i.stakeholder_response_rate_pct <= 0.30 && i.economic_buyer_engaged <= 0.35)     return "stakeholder_freeze";
  if (i.champion_last_contact_days >= 14 && i.champion_sentiment_score <= 0.45)        return "champion_disengagement";
  if (i.budget_confirmed <= 0.30 && i.decision_date_pushed_count >= 2)                 return "budget_drift";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "frozen"; if (c >= 40) return "stalled"; if (c >= 20) return "slowing"; return "flowing"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "stakeholder_freeze" || p === "decision_paralysis") return "executive_sponsor_bridge"; return "deal_rescue_intervention"; }
  if (r === "high") {
    if (p === "stage_stall")            return "stage_acceleration_call";
    if (p === "decision_paralysis")     return "decision_criteria_alignment";
    if (p === "stakeholder_freeze")     return "stakeholder_mapping_refresh";
    if (p === "champion_disengagement") return "champion_reactivation";
    if (p === "budget_drift")           return "mutual_action_plan_reset";
    return "velocity_monitoring";
  }
  if (r === "moderate") return "velocity_monitoring";
  return "no_action";
}
function signal(i: Deal, pat: string, comp: number): string {
  if (comp < 20) return "Deal velocity on track — stage progression, decision alignment and stakeholder engagement within healthy benchmarks";
  const labels: Record<string,string> = { stage_stall:"Stage stall", decision_paralysis:"Decision paralysis", stakeholder_freeze:"Stakeholder freeze", champion_disengagement:"Champion disengagement", budget_drift:"Budget drift" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${i.days_in_current_stage}d in stage — ${i.decision_date_pushed_count}x close date pushed — champion ${i.champion_last_contact_days}d ago — $${Math.round(i.deal_value_usd/1000)}k deal — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[sales-deal-velocity-acceleration-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tst=0,tde=0,tsk=0,tch=0,tcomp=0,tdelay=0,gc=0,ec=0;
    for (const d of deals) {
      rc[d.velocity_risk]=(rc[d.velocity_risk]||0)+1; pc[d.velocity_pattern]=(pc[d.velocity_pattern]||0)+1;
      sc[d.velocity_severity]=(sc[d.velocity_severity]||0)+1; ac[d.recommended_action]=(ac[d.recommended_action]||0)+1;
      tst+=d.stall_score; tde+=d.decision_score; tsk+=d.stakeholder_score; tch+=d.champion_score;
      tcomp+=d.velocity_composite; tdelay+=d.estimated_delay_days;
      if (d.has_velocity_gap) gc++; if (d.requires_executive_bridge) ec++;
    }
    const n = deals.length;
    return sealResponse(NextResponse.json(sealResponse({ deals, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_velocity_composite: Math.round(tcomp/n*10)/10,
      velocity_gap_count: gc, executive_bridge_count: ec,
      avg_stall_score: Math.round(tst/n*10)/10,
      avg_decision_score: Math.round(tde/n*10)/10,
      avg_stakeholder_score: Math.round(tsk/n*10)/10,
      avg_champion_score: Math.round(tch/n*10)/10,
      avg_estimated_delay_days: Math.round(tdelay/n*10)/10,
    }} as Record<string,unknown>)));
  }
  return sealResponse(NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-deal-velocity-acceleration-engine`, { next: { revalidate: 30 } })).json()));
}
