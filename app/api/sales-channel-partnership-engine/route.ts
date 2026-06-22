import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_CHANNELS = [
  { channel_id:"CH-001", channel_type:"direct",      region:"EMEA",  channel_revenue_contribution:0.22, partner_performance_score:0.25, channel_coverage_score:0.28, margin_per_channel:0.22, conflict_index:0.72, partner_engagement_score:0.28, certification_compliance_pct:0.30, deal_registration_rate:0.28, channel_marketing_roi:0.25, co_selling_effectiveness:0.28, partner_churn_risk:0.78, territory_overlap_score:0.75, icp_alignment_score:0.28, training_program_effectiveness:0.25, revenue_forecast_accuracy:0.28, digital_channel_adoption:0.30, partner_satisfaction_score:0.22 },
  { channel_id:"CH-002", channel_type:"indirect",    region:"NAMER", channel_revenue_contribution:0.90, partner_performance_score:0.92, channel_coverage_score:0.94, margin_per_channel:0.88, conflict_index:0.05, partner_engagement_score:0.92, certification_compliance_pct:0.95, deal_registration_rate:0.92, channel_marketing_roi:0.90, co_selling_effectiveness:0.92, partner_churn_risk:0.04, territory_overlap_score:0.06, icp_alignment_score:0.92, training_program_effectiveness:0.90, revenue_forecast_accuracy:0.92, digital_channel_adoption:0.88, partner_satisfaction_score:0.94 },
  { channel_id:"CH-003", channel_type:"digital",     region:"APAC",  channel_revenue_contribution:0.55, partner_performance_score:0.38, channel_coverage_score:0.42, margin_per_channel:0.30, conflict_index:0.52, partner_engagement_score:0.38, certification_compliance_pct:0.45, deal_registration_rate:0.48, channel_marketing_roi:0.50, co_selling_effectiveness:0.45, partner_churn_risk:0.58, territory_overlap_score:0.62, icp_alignment_score:0.42, training_program_effectiveness:0.42, revenue_forecast_accuracy:0.45, digital_channel_adoption:0.78, partner_satisfaction_score:0.38 },
  { channel_id:"CH-004", channel_type:"distributor", region:"LATAM", channel_revenue_contribution:0.78, partner_performance_score:0.82, channel_coverage_score:0.80, margin_per_channel:0.75, conflict_index:0.12, partner_engagement_score:0.82, certification_compliance_pct:0.85, deal_registration_rate:0.82, channel_marketing_roi:0.78, co_selling_effectiveness:0.80, partner_churn_risk:0.08, territory_overlap_score:0.10, icp_alignment_score:0.82, training_program_effectiveness:0.80, revenue_forecast_accuracy:0.82, digital_channel_adoption:0.65, partner_satisfaction_score:0.85 },
  { channel_id:"CH-005", channel_type:"reseller",    region:"EMEA",  channel_revenue_contribution:0.30, partner_performance_score:0.28, channel_coverage_score:0.32, margin_per_channel:0.25, conflict_index:0.65, partner_engagement_score:0.32, certification_compliance_pct:0.28, deal_registration_rate:0.30, channel_marketing_roi:0.28, co_selling_effectiveness:0.28, partner_churn_risk:0.72, territory_overlap_score:0.68, icp_alignment_score:0.30, training_program_effectiveness:0.28, revenue_forecast_accuracy:0.30, digital_channel_adoption:0.35, partner_satisfaction_score:0.25 },
  { channel_id:"CH-006", channel_type:"marketplace", region:"APAC",  channel_revenue_contribution:0.65, partner_performance_score:0.62, channel_coverage_score:0.60, margin_per_channel:0.32, conflict_index:0.28, partner_engagement_score:0.65, certification_compliance_pct:0.65, deal_registration_rate:0.62, channel_marketing_roi:0.65, co_selling_effectiveness:0.62, partner_churn_risk:0.22, territory_overlap_score:0.25, icp_alignment_score:0.65, training_program_effectiveness:0.62, revenue_forecast_accuracy:0.65, digital_channel_adoption:0.92, partner_satisfaction_score:0.65 },
  { channel_id:"CH-007", channel_type:"oem",         region:"MEA",   channel_revenue_contribution:0.42, partner_performance_score:0.38, channel_coverage_score:0.36, margin_per_channel:0.38, conflict_index:0.48, partner_engagement_score:0.40, certification_compliance_pct:0.42, deal_registration_rate:0.40, channel_marketing_roi:0.38, co_selling_effectiveness:0.40, partner_churn_risk:0.52, territory_overlap_score:0.55, icp_alignment_score:0.38, training_program_effectiveness:0.40, revenue_forecast_accuracy:0.42, digital_channel_adoption:0.42, partner_satisfaction_score:0.38 },
  { channel_id:"CH-008", channel_type:"retail",      region:"NAMER", channel_revenue_contribution:0.72, partner_performance_score:0.70, channel_coverage_score:0.72, margin_per_channel:0.65, conflict_index:0.18, partner_engagement_score:0.72, certification_compliance_pct:0.72, deal_registration_rate:0.70, channel_marketing_roi:0.72, co_selling_effectiveness:0.70, partner_churn_risk:0.12, territory_overlap_score:0.15, icp_alignment_score:0.72, training_program_effectiveness:0.70, revenue_forecast_accuracy:0.72, digital_channel_adoption:0.60, partner_satisfaction_score:0.72 },
];

type Channel = typeof MOCK_CHANNELS[0];

function performanceScore(i: Channel): number {
  let s = 0;
  if      (i.partner_performance_score <= 0.30) s += 40; else if (i.partner_performance_score <= 0.55) s += 22; else if (i.partner_performance_score <= 0.75) s += 8;
  if      (i.channel_revenue_contribution <= 0.20) s += 35; else if (i.channel_revenue_contribution <= 0.45) s += 18; else if (i.channel_revenue_contribution <= 0.65) s += 6;
  if      (i.revenue_forecast_accuracy <= 0.30) s += 25; else if (i.revenue_forecast_accuracy <= 0.55) s += 12;
  return Math.min(s, 100);
}
function coverageScore(i: Channel): number {
  let s = 0;
  if      (i.channel_coverage_score <= 0.30) s += 40; else if (i.channel_coverage_score <= 0.55) s += 22; else if (i.channel_coverage_score <= 0.75) s += 8;
  if      (i.territory_overlap_score >= 0.70) s += 35; else if (i.territory_overlap_score >= 0.45) s += 18; else if (i.territory_overlap_score >= 0.25) s += 6;
  if      (i.icp_alignment_score <= 0.30) s += 25; else if (i.icp_alignment_score <= 0.55) s += 12;
  return Math.min(s, 100);
}
function healthScore(i: Channel): number {
  let s = 0;
  if      (i.conflict_index >= 0.70) s += 40; else if (i.conflict_index >= 0.45) s += 22; else if (i.conflict_index >= 0.25) s += 8;
  if      (i.partner_churn_risk >= 0.70) s += 35; else if (i.partner_churn_risk >= 0.45) s += 18; else if (i.partner_churn_risk >= 0.25) s += 6;
  if      (i.partner_satisfaction_score <= 0.30) s += 25; else if (i.partner_satisfaction_score <= 0.55) s += 12;
  return Math.min(s, 100);
}
function enablementScore(i: Channel): number {
  let s = 0;
  if      (i.training_program_effectiveness <= 0.30) s += 40; else if (i.training_program_effectiveness <= 0.55) s += 22; else if (i.training_program_effectiveness <= 0.75) s += 8;
  if      (i.certification_compliance_pct <= 0.30) s += 35; else if (i.certification_compliance_pct <= 0.55) s += 18; else if (i.certification_compliance_pct <= 0.75) s += 6;
  if      (i.co_selling_effectiveness <= 0.30) s += 25; else if (i.co_selling_effectiveness <= 0.55) s += 12;
  return Math.min(s, 100);
}
function composite(perf: number, cov: number, hlth: number, enab: number): number {
  return Math.min(Math.round((perf * 0.30 + cov * 0.25 + hlth * 0.25 + enab * 0.20) * 100) / 100, 100);
}
function channelPattern(i: Channel): string {
  if (i.conflict_index >= 0.5 || i.territory_overlap_score >= 0.6)                              return "channel_conflict";
  if (i.partner_performance_score <= 0.4 && i.partner_engagement_score <= 0.4)                  return "partner_underperformance";
  if (i.margin_per_channel <= 0.35)                                                              return "margin_erosion";
  if (i.channel_coverage_score <= 0.4 || i.icp_alignment_score <= 0.35)                         return "coverage_gap";
  if (i.territory_overlap_score >= 0.55 && i.channel_revenue_contribution >= 0.6)               return "channel_cannibalization";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "degraded"; if (c >= 20) return "stable"; return "optimized"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "channel_conflict")         return "emergency_rebalancing";
    if (p === "margin_erosion")           return "channel_restructuring";
    if (p === "partner_underperformance") return "partner_termination";
    return "emergency_rebalancing";
  }
  if (r === "high") {
    if (p === "channel_conflict")         return "conflict_mediation";
    if (p === "partner_underperformance") return "partner_enablement";
    if (p === "margin_erosion")           return "margin_protection";
    if (p === "coverage_gap")             return "coverage_expansion";
    return "channel_monitoring";
  }
  if (r === "moderate") return "channel_monitoring";
  return "no_action";
}
function signal(i: Channel, pat: string, comp: number): string {
  if (comp < 20) return "Canaux de vente performants — partenaires engagés, couverture optimale, marges protégées";
  const labels: Record<string,string> = {
    channel_conflict:"Conflit canal", partner_underperformance:"Sous-performance partenaire",
    margin_erosion:"Érosion marge", coverage_gap:"Lacune couverture", channel_cannibalization:"Cannibalisation canal",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — performance partenaires ${Math.round(i.partner_performance_score*100)}% — conflits ${Math.round(i.conflict_index*100)}% — couverture ${Math.round(i.channel_coverage_score*100)}% — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[sales-channel-partnership-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tperf=0,tcov=0,thlth=0,tenab=0,tcomp=0,tridx=0,alertC=0,reviewC=0;
    for (const e of channels) {
      rc[e.channel_risk]=(rc[e.channel_risk]||0)+1;
      pc[e.channel_pattern]=(pc[e.channel_pattern]||0)+1;
      sc[e.channel_severity]=(sc[e.channel_severity]||0)+1;
      ac[e.recommended_action]=(ac[e.recommended_action]||0)+1;
      tperf+=e.performance_score; tcov+=e.coverage_score; thlth+=e.health_score; tenab+=e.enablement_score;
      tcomp+=e.channel_composite; tridx+=e.estimated_channel_risk_index;
      if (e.has_channel_alert)        alertC++;
      if (e.requires_strategic_review) reviewC++;
    }
    const n = channels.length;
    return sealResponse(NextResponse.json(sealResponse({ channels, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_channel_composite: Math.round(tcomp/n*10)/10,
      channel_alert_count: alertC, strategic_review_count: reviewC,
      avg_performance_score: Math.round(tperf/n*10)/10,
      avg_coverage_score: Math.round(tcov/n*10)/10,
      avg_health_score: Math.round(thlth/n*10)/10,
      avg_enablement_score: Math.round(tenab/n*10)/10,
      avg_estimated_channel_risk_index: Math.round(tridx/n*100)/100,
    }} as Record<string,unknown>)));
  }
  return sealResponse(NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-channel-partnership-engine`, { next: { revalidate: 30 } })).json()));
}
