import { NextResponse } from "next/server";

const MOCK_REPS = [
  { rep_id:"MQ-001", region:"EMEA",  evaluation_period_id:"Q2-2026", meetings_to_opportunity_rate_pct:0.12, discovery_completion_rate_pct:0.22, next_step_confirmed_rate_pct:0.18, demo_to_proposal_rate_pct:0.15, proposal_to_close_rate_pct:0.10, avg_meeting_duration_minutes:22, no_show_rate_pct:0.32, reschedule_rate_pct:0.48, multi_stakeholder_meeting_rate_pct:0.12, pain_identified_rate_pct:0.22, budget_confirmed_in_meeting_rate_pct:0.08, decision_process_mapped_rate_pct:0.10, meeting_notes_completion_rate_pct:0.18, repeat_meeting_same_stage_rate_pct:0.52, meeting_to_pipeline_velocity_days:28, champion_identified_meeting_rate_pct:0.12, competitive_mentioned_rate_pct:0.45, executive_access_secured_rate_pct:0.08, total_meetings_held:22, avg_deal_value_usd:85000 },
  { rep_id:"MQ-002", region:"APAC",  evaluation_period_id:"Q2-2026", meetings_to_opportunity_rate_pct:0.72, discovery_completion_rate_pct:0.88, next_step_confirmed_rate_pct:0.85, demo_to_proposal_rate_pct:0.78, proposal_to_close_rate_pct:0.62, avg_meeting_duration_minutes:48, no_show_rate_pct:0.04, reschedule_rate_pct:0.08, multi_stakeholder_meeting_rate_pct:0.65, pain_identified_rate_pct:0.82, budget_confirmed_in_meeting_rate_pct:0.72, decision_process_mapped_rate_pct:0.68, meeting_notes_completion_rate_pct:0.92, repeat_meeting_same_stage_rate_pct:0.08, meeting_to_pipeline_velocity_days:5, champion_identified_meeting_rate_pct:0.78, competitive_mentioned_rate_pct:0.35, executive_access_secured_rate_pct:0.55, total_meetings_held:14, avg_deal_value_usd:72000 },
  { rep_id:"MQ-003", region:"NAMER", evaluation_period_id:"Q2-2026", meetings_to_opportunity_rate_pct:0.35, discovery_completion_rate_pct:0.52, next_step_confirmed_rate_pct:0.48, demo_to_proposal_rate_pct:0.42, proposal_to_close_rate_pct:0.28, avg_meeting_duration_minutes:35, no_show_rate_pct:0.12, reschedule_rate_pct:0.22, multi_stakeholder_meeting_rate_pct:0.32, pain_identified_rate_pct:0.48, budget_confirmed_in_meeting_rate_pct:0.35, decision_process_mapped_rate_pct:0.38, meeting_notes_completion_rate_pct:0.55, repeat_meeting_same_stage_rate_pct:0.28, meeting_to_pipeline_velocity_days:14, champion_identified_meeting_rate_pct:0.42, competitive_mentioned_rate_pct:0.28, executive_access_secured_rate_pct:0.22, total_meetings_held:18, avg_deal_value_usd:65000 },
  { rep_id:"MQ-004", region:"LATAM", evaluation_period_id:"Q2-2026", meetings_to_opportunity_rate_pct:0.18, discovery_completion_rate_pct:0.28, next_step_confirmed_rate_pct:0.22, demo_to_proposal_rate_pct:0.18, proposal_to_close_rate_pct:0.12, avg_meeting_duration_minutes:28, no_show_rate_pct:0.28, reschedule_rate_pct:0.38, multi_stakeholder_meeting_rate_pct:0.18, pain_identified_rate_pct:0.25, budget_confirmed_in_meeting_rate_pct:0.12, decision_process_mapped_rate_pct:0.15, meeting_notes_completion_rate_pct:0.25, repeat_meeting_same_stage_rate_pct:0.45, meeting_to_pipeline_velocity_days:24, champion_identified_meeting_rate_pct:0.18, competitive_mentioned_rate_pct:0.55, executive_access_secured_rate_pct:0.10, total_meetings_held:19, avg_deal_value_usd:78000 },
  { rep_id:"MQ-005", region:"EMEA",  evaluation_period_id:"Q2-2026", meetings_to_opportunity_rate_pct:0.58, discovery_completion_rate_pct:0.72, next_step_confirmed_rate_pct:0.68, demo_to_proposal_rate_pct:0.62, proposal_to_close_rate_pct:0.45, avg_meeting_duration_minutes:42, no_show_rate_pct:0.06, reschedule_rate_pct:0.12, multi_stakeholder_meeting_rate_pct:0.55, pain_identified_rate_pct:0.68, budget_confirmed_in_meeting_rate_pct:0.55, decision_process_mapped_rate_pct:0.52, meeting_notes_completion_rate_pct:0.78, repeat_meeting_same_stage_rate_pct:0.12, meeting_to_pipeline_velocity_days:8, champion_identified_meeting_rate_pct:0.62, competitive_mentioned_rate_pct:0.32, executive_access_secured_rate_pct:0.42, total_meetings_held:16, avg_deal_value_usd:92000 },
  { rep_id:"MQ-006", region:"MEA",   evaluation_period_id:"Q2-2026", meetings_to_opportunity_rate_pct:0.08, discovery_completion_rate_pct:0.18, next_step_confirmed_rate_pct:0.15, demo_to_proposal_rate_pct:0.12, proposal_to_close_rate_pct:0.08, avg_meeting_duration_minutes:18, no_show_rate_pct:0.38, reschedule_rate_pct:0.52, multi_stakeholder_meeting_rate_pct:0.08, pain_identified_rate_pct:0.15, budget_confirmed_in_meeting_rate_pct:0.05, decision_process_mapped_rate_pct:0.08, meeting_notes_completion_rate_pct:0.12, repeat_meeting_same_stage_rate_pct:0.58, meeting_to_pipeline_velocity_days:32, champion_identified_meeting_rate_pct:0.08, competitive_mentioned_rate_pct:0.62, executive_access_secured_rate_pct:0.05, total_meetings_held:25, avg_deal_value_usd:55000 },
  { rep_id:"MQ-007", region:"APAC",  evaluation_period_id:"Q2-2026", meetings_to_opportunity_rate_pct:0.42, discovery_completion_rate_pct:0.62, next_step_confirmed_rate_pct:0.58, demo_to_proposal_rate_pct:0.52, proposal_to_close_rate_pct:0.35, avg_meeting_duration_minutes:38, no_show_rate_pct:0.09, reschedule_rate_pct:0.16, multi_stakeholder_meeting_rate_pct:0.42, pain_identified_rate_pct:0.58, budget_confirmed_in_meeting_rate_pct:0.42, decision_process_mapped_rate_pct:0.45, meeting_notes_completion_rate_pct:0.65, repeat_meeting_same_stage_rate_pct:0.18, meeting_to_pipeline_velocity_days:10, champion_identified_meeting_rate_pct:0.52, competitive_mentioned_rate_pct:0.25, executive_access_secured_rate_pct:0.32, total_meetings_held:15, avg_deal_value_usd:68000 },
  { rep_id:"MQ-008", region:"NAMER", evaluation_period_id:"Q2-2026", meetings_to_opportunity_rate_pct:0.22, discovery_completion_rate_pct:0.35, next_step_confirmed_rate_pct:0.28, demo_to_proposal_rate_pct:0.18, proposal_to_close_rate_pct:0.15, avg_meeting_duration_minutes:25, no_show_rate_pct:0.22, reschedule_rate_pct:0.32, multi_stakeholder_meeting_rate_pct:0.22, pain_identified_rate_pct:0.32, budget_confirmed_in_meeting_rate_pct:0.18, decision_process_mapped_rate_pct:0.22, meeting_notes_completion_rate_pct:0.38, repeat_meeting_same_stage_rate_pct:0.38, meeting_to_pipeline_velocity_days:18, champion_identified_meeting_rate_pct:0.25, competitive_mentioned_rate_pct:0.42, executive_access_secured_rate_pct:0.15, total_meetings_held:17, avg_deal_value_usd:75000 },
];

type Rep = typeof MOCK_REPS[0];

function conversionScore(i: Rep): number {
  let s = 0;
  if      (i.meetings_to_opportunity_rate_pct <= 0.20) s += 40; else if (i.meetings_to_opportunity_rate_pct <= 0.40) s += 22; else if (i.meetings_to_opportunity_rate_pct <= 0.60) s += 8;
  if      (i.demo_to_proposal_rate_pct        <= 0.25) s += 35; else if (i.demo_to_proposal_rate_pct <= 0.50) s += 18;
  if      (i.proposal_to_close_rate_pct       <= 0.15) s += 25; else if (i.proposal_to_close_rate_pct <= 0.30) s += 12;
  return Math.min(s, 100);
}
function qualityScore(i: Rep): number {
  let s = 0;
  if      (i.discovery_completion_rate_pct        <= 0.30) s += 40; else if (i.discovery_completion_rate_pct <= 0.55) s += 22; else if (i.discovery_completion_rate_pct <= 0.75) s += 8;
  if      (i.pain_identified_rate_pct             <= 0.30) s += 35; else if (i.pain_identified_rate_pct <= 0.55) s += 18;
  if      (i.multi_stakeholder_meeting_rate_pct   <= 0.20) s += 25; else if (i.multi_stakeholder_meeting_rate_pct <= 0.40) s += 12;
  return Math.min(s, 100);
}
function executionScore(i: Rep): number {
  let s = 0;
  if      (i.no_show_rate_pct                    >= 0.30) s += 40; else if (i.no_show_rate_pct >= 0.18) s += 22; else if (i.no_show_rate_pct >= 0.08) s += 8;
  if      (i.reschedule_rate_pct                 >= 0.40) s += 35; else if (i.reschedule_rate_pct >= 0.22) s += 18;
  if      (i.meeting_notes_completion_rate_pct   <= 0.30) s += 25; else if (i.meeting_notes_completion_rate_pct <= 0.55) s += 12;
  return Math.min(s, 100);
}
function advancementScore(i: Rep): number {
  let s = 0;
  if      (i.next_step_confirmed_rate_pct         <= 0.30) s += 45; else if (i.next_step_confirmed_rate_pct <= 0.55) s += 25; else if (i.next_step_confirmed_rate_pct <= 0.75) s += 10;
  if      (i.repeat_meeting_same_stage_rate_pct   >= 0.45) s += 30; else if (i.repeat_meeting_same_stage_rate_pct >= 0.25) s += 15;
  if      (i.meeting_to_pipeline_velocity_days    >= 21)   s += 25; else if (i.meeting_to_pipeline_velocity_days >= 12) s += 12;
  return Math.min(s, 100);
}
function composite(co: number, qu: number, ex: number, ad: number): number {
  return Math.min(Math.round((co * 0.30 + qu * 0.25 + ex * 0.20 + ad * 0.25) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.meetings_to_opportunity_rate_pct <= 0.20 && i.total_meetings_held >= 15) return "calendar_stuffing";
  if (i.discovery_completion_rate_pct <= 0.30 && i.pain_identified_rate_pct <= 0.35) return "discovery_skipper";
  if (i.next_step_confirmed_rate_pct <= 0.25 && i.repeat_meeting_same_stage_rate_pct >= 0.40) return "next_step_avoider";
  if (i.no_show_rate_pct >= 0.25 && i.reschedule_rate_pct >= 0.30) return "phantom_meeting_maker";
  if (i.demo_to_proposal_rate_pct <= 0.20 && i.repeat_meeting_same_stage_rate_pct >= 0.35) return "demo_looper";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "collapsing"; if (c >= 40) return "stalling"; if (c >= 20) return "slipping"; return "converting"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "calendar_stuffing" || p === "phantom_meeting_maker") return "full_pipeline_reset"; return "meeting_audit"; }
  if (r === "high") { if (p === "calendar_stuffing") return "pipeline_qualification_coaching"; if (p === "discovery_skipper") return "discovery_coaching"; if (p === "next_step_avoider") return "next_step_discipline_coaching"; if (p === "phantom_meeting_maker") return "pipeline_qualification_coaching"; if (p === "demo_looper") return "next_step_discipline_coaching"; return "discovery_coaching"; }
  if (r === "moderate") return "meeting_quality_monitoring";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Meeting quality and conversion healthy — discovery completion, next steps, and opportunity creation within benchmarks";
  const labels: Record<string, string> = { calendar_stuffing:"Calendar stuffing", discovery_skipper:"Discovery skipper", next_step_avoider:"Next-step avoider", phantom_meeting_maker:"Phantom meeting maker", demo_looper:"Demo looper" };
  const label = labels[pat] ?? pat.replace(/_/g, " ");
  return `${label} — ${Math.round(i.meetings_to_opportunity_rate_pct * 100)}% meetings→opp — ${Math.round(i.discovery_completion_rate_pct * 100)}% discovery complete — ${Math.round(i.next_step_confirmed_rate_pct * 100)}% next steps confirmed — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(i => {
      const co = conversionScore(i), qu = qualityScore(i), ex = executionScore(i), ad = advancementScore(i);
      const comp = composite(co, qu, ex, ad), pat = pattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      const wasted = Math.round(i.total_meetings_held * 350 * (1 - i.meetings_to_opportunity_rate_pct) * (comp / 100) * 100) / 100;
      return {
        rep_id: i.rep_id, region: i.region,
        meeting_risk: r, meeting_pattern: pat, meeting_severity: sev, recommended_action: act,
        conversion_score: co, quality_score: qu, execution_score: ex, advancement_score: ad,
        meeting_composite: comp,
        has_meeting_gap: comp >= 40 || i.meetings_to_opportunity_rate_pct <= 0.40 || i.next_step_confirmed_rate_pct <= 0.55,
        requires_meeting_coaching: comp >= 25 || i.discovery_completion_rate_pct <= 0.55 || i.no_show_rate_pct >= 0.15,
        estimated_wasted_meeting_usd: wasted,
        meeting_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tco=0, tqu=0, tex=0, tad=0, tcomp=0, tw=0, gc=0, cc=0;
    for (const r of reps) {
      rc[r.meeting_risk]=(rc[r.meeting_risk]||0)+1; pc[r.meeting_pattern]=(pc[r.meeting_pattern]||0)+1;
      sc[r.meeting_severity]=(sc[r.meeting_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      tco+=r.conversion_score; tqu+=r.quality_score; tex+=r.execution_score; tad+=r.advancement_score;
      tcomp+=r.meeting_composite; tw+=r.estimated_wasted_meeting_usd;
      if (r.has_meeting_gap) gc++; if (r.requires_meeting_coaching) cc++;
    }
    const n = reps.length;
    return NextResponse.json({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_meeting_composite: Math.round(tcomp/n*10)/10,
      meeting_gap_count: gc, coaching_count: cc,
      avg_conversion_score: Math.round(tco/n*10)/10,
      avg_quality_score: Math.round(tqu/n*10)/10,
      avg_execution_score: Math.round(tex/n*10)/10,
      avg_advancement_score: Math.round(tad/n*10)/10,
      total_estimated_wasted_meeting_usd: Math.round(tw*100)/100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-meeting-quality-conversion-intelligence-engine`)).json());
}
