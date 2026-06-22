import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[deal-fragmentation] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", deal_name: "Nexus Platform Deal", rep_id: "rep_003",
    stage: "Negotiation", region: "NAMER",
    fragmentation_risk: "fragmenting", fragmentation_pattern: "multi_signal",
    deal_prognosis: "at_risk_lost", recommended_action: "escalate",
    champion_risk_score: 75.0, engagement_decay_score: 68.4,
    scope_erosion_score: 54.2, timeline_drift_score: 72.6,
    fragmentation_composite_score: 68.4, estimated_deal_at_risk: 218880,
    recovery_probability: 0.0, is_fragmenting: true, needs_immediate_intervention: true,
    deal_value: 320000, initial_deal_value: 480000,
    days_in_current_stage: 42, close_date_pushed_times: 3,
    champion_last_active_days: 22, stage_regression_count: 1,
  },
  {
    deal_id: "deal_002", deal_name: "Aurora Cloud Migration", rep_id: "rep_007",
    stage: "Proposal", region: "EMEA",
    fragmentation_risk: "at_risk", fragmentation_pattern: "engagement_drop",
    deal_prognosis: "likely_slip", recommended_action: "rescue",
    champion_risk_score: 18.4, engagement_decay_score: 62.8,
    scope_erosion_score: 12.0, timeline_drift_score: 44.6,
    fragmentation_composite_score: 38.2, estimated_deal_at_risk: 53480,
    recovery_probability: 52.0, is_fragmenting: false, needs_immediate_intervention: false,
    deal_value: 140000, initial_deal_value: 140000,
    days_in_current_stage: 28, close_date_pushed_times: 2,
    champion_last_active_days: 8, stage_regression_count: 0,
  },
  {
    deal_id: "deal_003", deal_name: "ZenithAI Expansion", rep_id: "rep_002",
    stage: "Discovery", region: "APAC",
    fragmentation_risk: "stable", fragmentation_pattern: "healthy",
    deal_prognosis: "on_track", recommended_action: "maintain",
    champion_risk_score: 4.0, engagement_decay_score: 6.2,
    scope_erosion_score: 0.0, timeline_drift_score: 8.0,
    fragmentation_composite_score: 4.8, estimated_deal_at_risk: 9600,
    recovery_probability: 92.0, is_fragmenting: false, needs_immediate_intervention: false,
    deal_value: 200000, initial_deal_value: 200000,
    days_in_current_stage: 6, close_date_pushed_times: 0,
    champion_last_active_days: 2, stage_regression_count: 0,
  },
  {
    deal_id: "deal_004", deal_name: "Solaris Data Platform", rep_id: "rep_005",
    stage: "Proof of Concept", region: "NAMER",
    fragmentation_risk: "fragmenting", fragmentation_pattern: "champion_loss",
    deal_prognosis: "at_risk_lost", recommended_action: "escalate",
    champion_risk_score: 95.0, engagement_decay_score: 42.4,
    scope_erosion_score: 28.0, timeline_drift_score: 38.6,
    fragmentation_composite_score: 56.8, estimated_deal_at_risk: 284000,
    recovery_probability: 8.0, is_fragmenting: true, needs_immediate_intervention: true,
    deal_value: 500000, initial_deal_value: 620000,
    days_in_current_stage: 38, close_date_pushed_times: 2,
    champion_last_active_days: 0, stage_regression_count: 2,
  },
  {
    deal_id: "deal_005", deal_name: "PeakFlow Analytics", rep_id: "rep_001",
    stage: "Legal Review", region: "EMEA",
    fragmentation_risk: "early_signal", fragmentation_pattern: "timeline_slip",
    deal_prognosis: "needs_attention", recommended_action: "re_engage",
    champion_risk_score: 8.0, engagement_decay_score: 22.4,
    scope_erosion_score: 6.0, timeline_drift_score: 52.0,
    fragmentation_composite_score: 22.8, estimated_deal_at_risk: 52440,
    recovery_probability: 72.0, is_fragmenting: false, needs_immediate_intervention: false,
    deal_value: 230000, initial_deal_value: 230000,
    days_in_current_stage: 24, close_date_pushed_times: 1,
    champion_last_active_days: 4, stage_regression_count: 0,
  },
  {
    deal_id: "deal_006", deal_name: "Harbor Security Suite", rep_id: "rep_006",
    stage: "Negotiation", region: "LATAM",
    fragmentation_risk: "stable", fragmentation_pattern: "healthy",
    deal_prognosis: "on_track", recommended_action: "maintain",
    champion_risk_score: 0.0, engagement_decay_score: 8.0,
    scope_erosion_score: 0.0, timeline_drift_score: 12.0,
    fragmentation_composite_score: 4.0, estimated_deal_at_risk: 7200,
    recovery_probability: 94.0, is_fragmenting: false, needs_immediate_intervention: false,
    deal_value: 180000, initial_deal_value: 180000,
    days_in_current_stage: 10, close_date_pushed_times: 0,
    champion_last_active_days: 1, stage_regression_count: 0,
  },
  {
    deal_id: "deal_007", deal_name: "Orbit ERP Integration", rep_id: "rep_004",
    stage: "Proposal", region: "APAC",
    fragmentation_risk: "at_risk", fragmentation_pattern: "scope_shrink",
    deal_prognosis: "likely_slip", recommended_action: "rescue",
    champion_risk_score: 14.0, engagement_decay_score: 34.6,
    scope_erosion_score: 58.0, timeline_drift_score: 32.0,
    fragmentation_composite_score: 34.2, estimated_deal_at_risk: 68400,
    recovery_probability: 44.0, is_fragmenting: false, needs_immediate_intervention: false,
    deal_value: 200000, initial_deal_value: 340000,
    days_in_current_stage: 20, close_date_pushed_times: 2,
    champion_last_active_days: 6, stage_regression_count: 0,
  },
  {
    deal_id: "deal_008", deal_name: "Vertex CX Platform", rep_id: "rep_008",
    stage: "Discovery", region: "NAMER",
    fragmentation_risk: "early_signal", fragmentation_pattern: "engagement_drop",
    deal_prognosis: "needs_attention", recommended_action: "re_engage",
    champion_risk_score: 12.0, engagement_decay_score: 44.8,
    scope_erosion_score: 4.0, timeline_drift_score: 18.0,
    fragmentation_composite_score: 22.8, estimated_deal_at_risk: 43320,
    recovery_probability: 68.0, is_fragmenting: false, needs_immediate_intervention: false,
    deal_value: 190000, initial_deal_value: 200000,
    days_in_current_stage: 14, close_date_pushed_times: 1,
    champion_last_active_days: 10, stage_regression_count: 0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk     = searchParams.get("risk");
  const pattern  = searchParams.get("pattern");
  const region   = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/deal-fragmentation`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      if (region)  url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let deals = [...mockDeals];
  if (risk)    deals = deals.filter((d) => d.fragmentation_risk === risk);
  if (pattern) deals = deals.filter((d) => d.fragmentation_pattern === pattern);
  if (region)  deals = deals.filter((d) => d.region === region);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const prognosis_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_champ = 0, total_eng = 0,
      total_scope = 0, total_rec = 0, total_at_risk = 0;

  for (const d of mockDeals) {
    risk_counts[d.fragmentation_risk]   = (risk_counts[d.fragmentation_risk] || 0) + 1;
    pattern_counts[d.fragmentation_pattern] = (pattern_counts[d.fragmentation_pattern] || 0) + 1;
    prognosis_counts[d.deal_prognosis]  = (prognosis_counts[d.deal_prognosis] || 0) + 1;
    action_counts[d.recommended_action] = (action_counts[d.recommended_action] || 0) + 1;
    total_comp   += d.fragmentation_composite_score;
    total_champ  += d.champion_risk_score;
    total_eng    += d.engagement_decay_score;
    total_scope  += d.scope_erosion_score;
    total_rec    += d.recovery_probability;
    total_at_risk += d.estimated_deal_at_risk;
  }

  const n = mockDeals.length;

  return sealResponse(NextResponse.json({
    deals,
    summary: {
      total: n,
      risk_counts,
      pattern_counts,
      prognosis_counts,
      action_counts,
      avg_fragmentation_composite_score: Math.round((total_comp / n) * 10) / 10,
      total_estimated_deal_at_risk:      Math.round(total_at_risk),
      fragmenting_count:                 mockDeals.filter((d) => d.is_fragmenting).length,
      intervention_needed_count:         mockDeals.filter((d) => d.needs_immediate_intervention).length,
      avg_champion_risk_score:           Math.round((total_champ / n) * 10) / 10,
      avg_engagement_decay_score:        Math.round((total_eng / n) * 10) / 10,
      avg_scope_erosion_score:           Math.round((total_scope / n) * 10) / 10,
      avg_recovery_probability:          Math.round((total_rec / n) * 10) / 10,
    },
  }));
}
