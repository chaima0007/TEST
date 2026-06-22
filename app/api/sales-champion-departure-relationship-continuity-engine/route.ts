import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"CR-001", region:"EMEA",  evaluation_period_id:"Q2-2026", champion_engagement_drop_rate_pct:0.72, champion_response_latency_trend:0.82, org_change_detected_rate_pct:0.52, champion_linkedin_activity_drop_pct:0.65, single_threaded_deal_rate_pct:0.78, backup_contact_coverage_rate_pct:0.12, executive_sponsor_coverage_rate_pct:0.10, champion_internal_advocacy_score:0.18, champion_tenure_avg_months:5.0, stakeholder_mapping_completeness_score:0.15, champion_deal_influence_score:0.82, internal_coach_coverage_rate_pct:0.12, economic_buyer_direct_access_rate_pct:0.10, champion_replacement_recovery_rate_pct:0.10, deal_ghosting_after_champion_loss_rate_pct:0.68, relationship_breadth_score:0.15, champion_departure_detected_deals:8, total_active_deals:22, avg_deal_value_usd:88000 },
  { rep_id:"CR-002", region:"APAC",  evaluation_period_id:"Q2-2026", champion_engagement_drop_rate_pct:0.08, champion_response_latency_trend:0.12, org_change_detected_rate_pct:0.08, champion_linkedin_activity_drop_pct:0.10, single_threaded_deal_rate_pct:0.12, backup_contact_coverage_rate_pct:0.88, executive_sponsor_coverage_rate_pct:0.82, champion_internal_advocacy_score:0.85, champion_tenure_avg_months:32.0, stakeholder_mapping_completeness_score:0.88, champion_deal_influence_score:0.55, internal_coach_coverage_rate_pct:0.82, economic_buyer_direct_access_rate_pct:0.78, champion_replacement_recovery_rate_pct:0.72, deal_ghosting_after_champion_loss_rate_pct:0.08, relationship_breadth_score:0.88, champion_departure_detected_deals:1, total_active_deals:28, avg_deal_value_usd:115000 },
  { rep_id:"CR-003", region:"NAMER", evaluation_period_id:"Q2-2026", champion_engagement_drop_rate_pct:0.38, champion_response_latency_trend:0.42, org_change_detected_rate_pct:0.28, champion_linkedin_activity_drop_pct:0.35, single_threaded_deal_rate_pct:0.42, backup_contact_coverage_rate_pct:0.48, executive_sponsor_coverage_rate_pct:0.42, champion_internal_advocacy_score:0.55, champion_tenure_avg_months:16.0, stakeholder_mapping_completeness_score:0.52, champion_deal_influence_score:0.62, internal_coach_coverage_rate_pct:0.48, economic_buyer_direct_access_rate_pct:0.42, champion_replacement_recovery_rate_pct:0.38, deal_ghosting_after_champion_loss_rate_pct:0.35, relationship_breadth_score:0.48, champion_departure_detected_deals:4, total_active_deals:35, avg_deal_value_usd:96000 },
  { rep_id:"CR-004", region:"LATAM", evaluation_period_id:"Q2-2026", champion_engagement_drop_rate_pct:0.62, champion_response_latency_trend:0.72, org_change_detected_rate_pct:0.48, champion_linkedin_activity_drop_pct:0.55, single_threaded_deal_rate_pct:0.82, backup_contact_coverage_rate_pct:0.10, executive_sponsor_coverage_rate_pct:0.08, champion_internal_advocacy_score:0.12, champion_tenure_avg_months:4.0, stakeholder_mapping_completeness_score:0.10, champion_deal_influence_score:0.88, internal_coach_coverage_rate_pct:0.08, economic_buyer_direct_access_rate_pct:0.08, champion_replacement_recovery_rate_pct:0.05, deal_ghosting_after_champion_loss_rate_pct:0.75, relationship_breadth_score:0.10, champion_departure_detected_deals:7, total_active_deals:18, avg_deal_value_usd:78000 },
  { rep_id:"CR-005", region:"EMEA",  evaluation_period_id:"Q2-2026", champion_engagement_drop_rate_pct:0.12, champion_response_latency_trend:0.15, org_change_detected_rate_pct:0.12, champion_linkedin_activity_drop_pct:0.12, single_threaded_deal_rate_pct:0.18, backup_contact_coverage_rate_pct:0.82, executive_sponsor_coverage_rate_pct:0.75, champion_internal_advocacy_score:0.78, champion_tenure_avg_months:28.0, stakeholder_mapping_completeness_score:0.82, champion_deal_influence_score:0.50, internal_coach_coverage_rate_pct:0.75, economic_buyer_direct_access_rate_pct:0.72, champion_replacement_recovery_rate_pct:0.65, deal_ghosting_after_champion_loss_rate_pct:0.10, relationship_breadth_score:0.82, champion_departure_detected_deals:2, total_active_deals:40, avg_deal_value_usd:105000 },
  { rep_id:"CR-006", region:"MEA",   evaluation_period_id:"Q2-2026", champion_engagement_drop_rate_pct:0.85, champion_response_latency_trend:0.92, org_change_detected_rate_pct:0.62, champion_linkedin_activity_drop_pct:0.78, single_threaded_deal_rate_pct:0.92, backup_contact_coverage_rate_pct:0.05, executive_sponsor_coverage_rate_pct:0.05, champion_internal_advocacy_score:0.08, champion_tenure_avg_months:3.0, stakeholder_mapping_completeness_score:0.08, champion_deal_influence_score:0.92, internal_coach_coverage_rate_pct:0.05, economic_buyer_direct_access_rate_pct:0.05, champion_replacement_recovery_rate_pct:0.05, deal_ghosting_after_champion_loss_rate_pct:0.85, relationship_breadth_score:0.08, champion_departure_detected_deals:10, total_active_deals:15, avg_deal_value_usd:72000 },
  { rep_id:"CR-007", region:"APAC",  evaluation_period_id:"Q2-2026", champion_engagement_drop_rate_pct:0.25, champion_response_latency_trend:0.28, org_change_detected_rate_pct:0.18, champion_linkedin_activity_drop_pct:0.22, single_threaded_deal_rate_pct:0.28, backup_contact_coverage_rate_pct:0.68, executive_sponsor_coverage_rate_pct:0.62, champion_internal_advocacy_score:0.68, champion_tenure_avg_months:22.0, stakeholder_mapping_completeness_score:0.68, champion_deal_influence_score:0.58, internal_coach_coverage_rate_pct:0.62, economic_buyer_direct_access_rate_pct:0.58, champion_replacement_recovery_rate_pct:0.55, deal_ghosting_after_champion_loss_rate_pct:0.18, relationship_breadth_score:0.68, champion_departure_detected_deals:2, total_active_deals:32, avg_deal_value_usd:98000 },
  { rep_id:"CR-008", region:"NAMER", evaluation_period_id:"Q2-2026", champion_engagement_drop_rate_pct:0.48, champion_response_latency_trend:0.55, org_change_detected_rate_pct:0.38, champion_linkedin_activity_drop_pct:0.45, single_threaded_deal_rate_pct:0.55, backup_contact_coverage_rate_pct:0.32, executive_sponsor_coverage_rate_pct:0.28, champion_internal_advocacy_score:0.38, champion_tenure_avg_months:10.0, stakeholder_mapping_completeness_score:0.38, champion_deal_influence_score:0.72, internal_coach_coverage_rate_pct:0.32, economic_buyer_direct_access_rate_pct:0.28, champion_replacement_recovery_rate_pct:0.22, deal_ghosting_after_champion_loss_rate_pct:0.48, relationship_breadth_score:0.35, champion_departure_detected_deals:5, total_active_deals:25, avg_deal_value_usd:92000 },
];

type Rep = typeof MOCK_REPS[0];

function stabilityScore(i: Rep): number {
  let s = 0;
  if      (i.champion_engagement_drop_rate_pct >= 0.55) s += 40; else if (i.champion_engagement_drop_rate_pct >= 0.30) s += 22; else if (i.champion_engagement_drop_rate_pct >= 0.15) s += 8;
  if      (i.org_change_detected_rate_pct      >= 0.40) s += 35; else if (i.org_change_detected_rate_pct >= 0.20) s += 18;
  if      (i.champion_tenure_avg_months        <= 6)    s += 25; else if (i.champion_tenure_avg_months <= 12) s += 12;
  return Math.min(s, 100);
}
function coverageScore(i: Rep): number {
  let s = 0;
  if      (i.single_threaded_deal_rate_pct       >= 0.65) s += 45; else if (i.single_threaded_deal_rate_pct >= 0.40) s += 25; else if (i.single_threaded_deal_rate_pct >= 0.20) s += 10;
  if      (i.backup_contact_coverage_rate_pct    <= 0.25) s += 30; else if (i.backup_contact_coverage_rate_pct <= 0.50) s += 15;
  if      (i.executive_sponsor_coverage_rate_pct <= 0.20) s += 25; else if (i.executive_sponsor_coverage_rate_pct <= 0.45) s += 12;
  return Math.min(s, 100);
}
function resilienceScore(i: Rep): number {
  let s = 0;
  if      (i.champion_replacement_recovery_rate_pct      <= 0.15) s += 40; else if (i.champion_replacement_recovery_rate_pct <= 0.35) s += 22; else if (i.champion_replacement_recovery_rate_pct <= 0.55) s += 8;
  if      (i.deal_ghosting_after_champion_loss_rate_pct  >= 0.55) s += 35; else if (i.deal_ghosting_after_champion_loss_rate_pct >= 0.30) s += 18;
  if      (i.internal_coach_coverage_rate_pct            <= 0.20) s += 25; else if (i.internal_coach_coverage_rate_pct <= 0.45) s += 12;
  return Math.min(s, 100);
}
function intelligenceScore(i: Rep): number {
  let s = 0;
  if      (i.stakeholder_mapping_completeness_score  <= 0.20) s += 45; else if (i.stakeholder_mapping_completeness_score <= 0.45) s += 25; else if (i.stakeholder_mapping_completeness_score <= 0.65) s += 10;
  if      (i.relationship_breadth_score              <= 0.20) s += 30; else if (i.relationship_breadth_score <= 0.45) s += 15;
  if      (i.economic_buyer_direct_access_rate_pct   <= 0.20) s += 25; else if (i.economic_buyer_direct_access_rate_pct <= 0.45) s += 12;
  return Math.min(s, 100);
}
function composite(st: number, co: number, re: number, i_: number): number {
  return Math.min(Math.round((st * 0.30 + co * 0.25 + re * 0.25 + i_ * 0.20) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.single_threaded_deal_rate_pct >= 0.60 && i.backup_contact_coverage_rate_pct <= 0.25) return "single_thread_exposed";
  if (i.deal_ghosting_after_champion_loss_rate_pct >= 0.55 && i.champion_replacement_recovery_rate_pct <= 0.20) return "ghost_risk_zone";
  if (i.org_change_detected_rate_pct >= 0.35 && i.champion_tenure_avg_months <= 12) return "org_change_vulnerable";
  if (i.champion_internal_advocacy_score <= 0.25 && i.champion_deal_influence_score >= 0.70) return "advocacy_collapse";
  if (i.stakeholder_mapping_completeness_score <= 0.25 && i.relationship_breadth_score <= 0.30) return "blind_spot_account";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "vulnerable"; if (c >= 20) return "drifting"; return "stable"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "single_thread_exposed" || p === "ghost_risk_zone") return "deal_continuity_escalation"; return "relationship_rescue_intervention"; }
  if (r === "high") {
    if (p === "single_thread_exposed") return "multithreading_urgency_coaching";
    if (p === "ghost_risk_zone")       return "relationship_rescue_intervention";
    if (p === "org_change_vulnerable") return "org_change_alert_protocol";
    if (p === "advocacy_collapse")     return "executive_engagement_activation";
    if (p === "blind_spot_account")    return "stakeholder_mapping_sprint";
    return "multithreading_urgency_coaching";
  }
  if (r === "moderate") return "champion_health_monitoring";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Champion relationships stable — multithreading, engagement, and stakeholder coverage within benchmark targets";
  const labels: Record<string,string> = { single_thread_exposed:"Single-thread exposed", ghost_risk_zone:"Ghost risk zone", org_change_vulnerable:"Org change vulnerable", advocacy_collapse:"Advocacy collapse", blind_spot_account:"Blind spot account" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(i.single_threaded_deal_rate_pct*100)}% single-threaded — ${Math.round(i.champion_engagement_drop_rate_pct*100)}% engagement drop — ${Math.round(i.deal_ghosting_after_champion_loss_rate_pct*100)}% ghosted after champion loss — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[sales-champion-departure-relationship-continuity-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tst=0, tco=0, tre=0, tin=0, tcomp=0, tar=0, gc=0, ic=0;
    for (const r of reps) {
      rc[r.champion_risk]=(rc[r.champion_risk]||0)+1; pc[r.champion_pattern]=(pc[r.champion_pattern]||0)+1;
      sc[r.champion_severity]=(sc[r.champion_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      tst+=r.stability_score; tco+=r.coverage_score; tre+=r.resilience_score; tin+=r.intelligence_score;
      tcomp+=r.champion_composite; tar+=r.estimated_at_risk_pipeline_usd;
      if (r.has_champion_gap) gc++; if (r.requires_champion_intervention) ic++;
    }
    const n = reps.length;
    return sealResponse(NextResponse.json(sealResponse({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_champion_composite: Math.round(tcomp/n*10)/10,
      champion_gap_count: gc, intervention_count: ic,
      avg_stability_score: Math.round(tst/n*10)/10,
      avg_coverage_score: Math.round(tco/n*10)/10,
      avg_resilience_score: Math.round(tre/n*10)/10,
      avg_intelligence_score: Math.round(tin/n*10)/10,
      total_estimated_at_risk_pipeline_usd: Math.round(tar*100)/100,
    }} as Record<string,unknown>)));
  }
  return sealResponse(NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-champion-departure-relationship-continuity-engine`, { next: { revalidate: 30 } })).json()));
}
