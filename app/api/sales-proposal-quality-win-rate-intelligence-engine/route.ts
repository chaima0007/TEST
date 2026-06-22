import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"PQ-001", region:"EMEA",  evaluation_period_id:"Q2-2026", proposal_to_close_rate_pct:0.12, proposal_sent_without_discovery_rate_pct:0.65, avg_days_to_send_proposal:3.5, proposal_revision_count_avg:2.8, executive_sponsor_present_in_proposal_pct:0.18, proposal_customization_score:0.15, value_articulation_score:0.22, competitive_differentiation_score:0.18, pricing_structure_complexity_score:0.72, proposal_response_time_days:18.0, unanswered_proposal_rate_pct:0.55, proposal_reused_template_rate_pct:0.72, mutual_success_plan_inclusion_rate_pct:0.12, roi_case_included_rate_pct:0.18, legal_redline_rate_pct:0.42, multi_stakeholder_proposal_rate_pct:0.15, proposal_champion_alignment_score:0.18, total_proposals_sent:24, avg_deal_value_usd:88000 },
  { rep_id:"PQ-002", region:"APAC",  evaluation_period_id:"Q2-2026", proposal_to_close_rate_pct:0.68, proposal_sent_without_discovery_rate_pct:0.08, avg_days_to_send_proposal:9.0, proposal_revision_count_avg:1.2, executive_sponsor_present_in_proposal_pct:0.82, proposal_customization_score:0.88, value_articulation_score:0.85, competitive_differentiation_score:0.78, pricing_structure_complexity_score:0.18, proposal_response_time_days:4.0, unanswered_proposal_rate_pct:0.08, proposal_reused_template_rate_pct:0.08, mutual_success_plan_inclusion_rate_pct:0.78, roi_case_included_rate_pct:0.88, legal_redline_rate_pct:0.10, multi_stakeholder_proposal_rate_pct:0.82, proposal_champion_alignment_score:0.88, total_proposals_sent:31, avg_deal_value_usd:112000 },
  { rep_id:"PQ-003", region:"NAMER", evaluation_period_id:"Q2-2026", proposal_to_close_rate_pct:0.32, proposal_sent_without_discovery_rate_pct:0.38, avg_days_to_send_proposal:8.0, proposal_revision_count_avg:2.2, executive_sponsor_present_in_proposal_pct:0.45, proposal_customization_score:0.48, value_articulation_score:0.52, competitive_differentiation_score:0.42, pricing_structure_complexity_score:0.42, proposal_response_time_days:9.0, unanswered_proposal_rate_pct:0.28, proposal_reused_template_rate_pct:0.38, mutual_success_plan_inclusion_rate_pct:0.42, roi_case_included_rate_pct:0.52, legal_redline_rate_pct:0.22, multi_stakeholder_proposal_rate_pct:0.52, proposal_champion_alignment_score:0.55, total_proposals_sent:38, avg_deal_value_usd:96000 },
  { rep_id:"PQ-004", region:"LATAM", evaluation_period_id:"Q2-2026", proposal_to_close_rate_pct:0.15, proposal_sent_without_discovery_rate_pct:0.58, avg_days_to_send_proposal:2.5, proposal_revision_count_avg:3.5, executive_sponsor_present_in_proposal_pct:0.12, proposal_customization_score:0.12, value_articulation_score:0.15, competitive_differentiation_score:0.10, pricing_structure_complexity_score:0.82, proposal_response_time_days:22.0, unanswered_proposal_rate_pct:0.62, proposal_reused_template_rate_pct:0.75, mutual_success_plan_inclusion_rate_pct:0.08, roi_case_included_rate_pct:0.10, legal_redline_rate_pct:0.55, multi_stakeholder_proposal_rate_pct:0.10, proposal_champion_alignment_score:0.10, total_proposals_sent:18, avg_deal_value_usd:78000 },
  { rep_id:"PQ-005", region:"EMEA",  evaluation_period_id:"Q2-2026", proposal_to_close_rate_pct:0.58, proposal_sent_without_discovery_rate_pct:0.12, avg_days_to_send_proposal:7.0, proposal_revision_count_avg:1.5, executive_sponsor_present_in_proposal_pct:0.72, proposal_customization_score:0.78, value_articulation_score:0.75, competitive_differentiation_score:0.68, pricing_structure_complexity_score:0.22, proposal_response_time_days:5.0, unanswered_proposal_rate_pct:0.12, proposal_reused_template_rate_pct:0.12, mutual_success_plan_inclusion_rate_pct:0.68, roi_case_included_rate_pct:0.78, legal_redline_rate_pct:0.12, multi_stakeholder_proposal_rate_pct:0.72, proposal_champion_alignment_score:0.78, total_proposals_sent:42, avg_deal_value_usd:102000 },
  { rep_id:"PQ-006", region:"MEA",   evaluation_period_id:"Q2-2026", proposal_to_close_rate_pct:0.08, proposal_sent_without_discovery_rate_pct:0.72, avg_days_to_send_proposal:1.5, proposal_revision_count_avg:5.5, executive_sponsor_present_in_proposal_pct:0.05, proposal_customization_score:0.08, value_articulation_score:0.08, competitive_differentiation_score:0.05, pricing_structure_complexity_score:0.92, proposal_response_time_days:25.0, unanswered_proposal_rate_pct:0.72, proposal_reused_template_rate_pct:0.88, mutual_success_plan_inclusion_rate_pct:0.05, roi_case_included_rate_pct:0.05, legal_redline_rate_pct:0.65, multi_stakeholder_proposal_rate_pct:0.05, proposal_champion_alignment_score:0.05, total_proposals_sent:14, avg_deal_value_usd:72000 },
  { rep_id:"PQ-007", region:"APAC",  evaluation_period_id:"Q2-2026", proposal_to_close_rate_pct:0.48, proposal_sent_without_discovery_rate_pct:0.18, avg_days_to_send_proposal:11.0, proposal_revision_count_avg:1.8, executive_sponsor_present_in_proposal_pct:0.62, proposal_customization_score:0.68, value_articulation_score:0.65, competitive_differentiation_score:0.58, pricing_structure_complexity_score:0.28, proposal_response_time_days:6.0, unanswered_proposal_rate_pct:0.18, proposal_reused_template_rate_pct:0.18, mutual_success_plan_inclusion_rate_pct:0.58, roi_case_included_rate_pct:0.68, legal_redline_rate_pct:0.15, multi_stakeholder_proposal_rate_pct:0.62, proposal_champion_alignment_score:0.68, total_proposals_sent:35, avg_deal_value_usd:98000 },
  { rep_id:"PQ-008", region:"NAMER", evaluation_period_id:"Q2-2026", proposal_to_close_rate_pct:0.22, proposal_sent_without_discovery_rate_pct:0.48, avg_days_to_send_proposal:5.5, proposal_revision_count_avg:3.2, executive_sponsor_present_in_proposal_pct:0.28, proposal_customization_score:0.32, value_articulation_score:0.38, competitive_differentiation_score:0.28, pricing_structure_complexity_score:0.58, proposal_response_time_days:14.0, unanswered_proposal_rate_pct:0.42, proposal_reused_template_rate_pct:0.52, mutual_success_plan_inclusion_rate_pct:0.25, roi_case_included_rate_pct:0.32, legal_redline_rate_pct:0.38, multi_stakeholder_proposal_rate_pct:0.32, proposal_champion_alignment_score:0.35, total_proposals_sent:28, avg_deal_value_usd:91000 },
];

type Rep = typeof MOCK_REPS[0];

function qualityScore(i: Rep): number {
  let s = 0;
  if      (i.proposal_customization_score <= 0.20) s += 40; else if (i.proposal_customization_score <= 0.45) s += 22; else if (i.proposal_customization_score <= 0.65) s += 8;
  if      (i.value_articulation_score     <= 0.25) s += 35; else if (i.value_articulation_score <= 0.55) s += 18;
  if      (i.roi_case_included_rate_pct   <= 0.30) s += 25; else if (i.roi_case_included_rate_pct <= 0.55) s += 12;
  return Math.min(s, 100);
}
function readinessScore(i: Rep): number {
  let s = 0;
  if      (i.proposal_sent_without_discovery_rate_pct  >= 0.55) s += 40; else if (i.proposal_sent_without_discovery_rate_pct >= 0.30) s += 22; else if (i.proposal_sent_without_discovery_rate_pct >= 0.15) s += 8;
  if      (i.executive_sponsor_present_in_proposal_pct <= 0.20) s += 35; else if (i.executive_sponsor_present_in_proposal_pct <= 0.45) s += 18;
  if      (i.mutual_success_plan_inclusion_rate_pct    <= 0.20) s += 25; else if (i.mutual_success_plan_inclusion_rate_pct <= 0.45) s += 12;
  return Math.min(s, 100);
}
function executionScore(i: Rep): number {
  let s = 0;
  if      (i.unanswered_proposal_rate_pct >= 0.50) s += 45; else if (i.unanswered_proposal_rate_pct >= 0.30) s += 25; else if (i.unanswered_proposal_rate_pct >= 0.15) s += 10;
  if      (i.proposal_revision_count_avg  >= 5.0)  s += 30; else if (i.proposal_revision_count_avg >= 3.0) s += 15;
  if      (i.avg_days_to_send_proposal    >= 21)   s += 25; else if (i.avg_days_to_send_proposal >= 10) s += 12;
  return Math.min(s, 100);
}
function alignmentScore(i: Rep): number {
  let s = 0;
  if      (i.proposal_champion_alignment_score   <= 0.20) s += 45; else if (i.proposal_champion_alignment_score <= 0.45) s += 25; else if (i.proposal_champion_alignment_score <= 0.65) s += 10;
  if      (i.multi_stakeholder_proposal_rate_pct <= 0.20) s += 30; else if (i.multi_stakeholder_proposal_rate_pct <= 0.45) s += 15;
  if      (i.competitive_differentiation_score   <= 0.20) s += 25; else if (i.competitive_differentiation_score <= 0.50) s += 12;
  return Math.min(s, 100);
}
function composite(qu: number, re: number, ex: number, al: number): number {
  return Math.min(Math.round((qu * 0.30 + re * 0.25 + ex * 0.25 + al * 0.20) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.proposal_sent_without_discovery_rate_pct >= 0.50 && i.avg_days_to_send_proposal <= 5) return "premature_proposer";
  if (i.proposal_reused_template_rate_pct >= 0.60 && i.proposal_customization_score <= 0.30) return "template_lazy";
  if (i.unanswered_proposal_rate_pct >= 0.45 && i.proposal_response_time_days >= 14) return "ghosted_proposer";
  if (i.proposal_revision_count_avg >= 4.0 && i.legal_redline_rate_pct >= 0.35) return "revision_looper";
  if (i.executive_sponsor_present_in_proposal_pct <= 0.20 && i.proposal_champion_alignment_score <= 0.30) return "orphaned_proposal";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "collapsing"; if (c >= 40) return "stalling"; if (c >= 20) return "softening"; return "converting"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "premature_proposer" || p === "template_lazy") return "proposal_framework_redesign"; return "proposal_strategy_intervention"; }
  if (r === "high") {
    if (p === "premature_proposer") return "discovery_gate_enforcement";
    if (p === "template_lazy")      return "customization_coaching";
    if (p === "ghosted_proposer")   return "engagement_reactivation_coaching";
    if (p === "revision_looper")    return "deal_desk_proposal_support";
    if (p === "orphaned_proposal")  return "champion_alignment_coaching";
    return "proposal_quality_coaching";
  }
  if (r === "moderate") return "proposal_quality_monitoring";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Proposal quality and win rate healthy — customization, discovery readiness, and champion alignment within benchmark targets";
  const labels: Record<string,string> = { premature_proposer:"Premature proposer", template_lazy:"Template lazy", ghosted_proposer:"Ghosted proposer", revision_looper:"Revision looper", orphaned_proposal:"Orphaned proposal" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(i.proposal_to_close_rate_pct*100)}% proposals close — ${Math.round(i.unanswered_proposal_rate_pct*100)}% unanswered — ${Math.round(i.proposal_customization_score*100)}% customization score — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[sales-proposal-quality-win-rate-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tqu=0, tre=0, tex=0, tal=0, tcomp=0, tloss=0, gc=0, cc=0;
    for (const r of reps) {
      rc[r.proposal_risk]=(rc[r.proposal_risk]||0)+1; pc[r.proposal_pattern]=(pc[r.proposal_pattern]||0)+1;
      sc[r.proposal_severity]=(sc[r.proposal_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      tqu+=r.quality_score; tre+=r.readiness_score; tex+=r.execution_score; tal+=r.alignment_score;
      tcomp+=r.proposal_composite; tloss+=r.estimated_deal_loss_usd;
      if (r.has_proposal_gap) gc++; if (r.requires_proposal_coaching) cc++;
    }
    const n = reps.length;
    return sealResponse(NextResponse.json(sealResponse({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_proposal_composite: Math.round(tcomp/n*10)/10,
      proposal_gap_count: gc, coaching_count: cc,
      avg_quality_score: Math.round(tqu/n*10)/10,
      avg_readiness_score: Math.round(tre/n*10)/10,
      avg_execution_score: Math.round(tex/n*10)/10,
      avg_alignment_score: Math.round(tal/n*10)/10,
      total_estimated_deal_loss_usd: Math.round(tloss*100)/100,
    }} as Record<string,unknown>)));
  }
  return sealResponse(NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-proposal-quality-win-rate-intelligence-engine`, { next: { revalidate: 30 } })).json()));
}
