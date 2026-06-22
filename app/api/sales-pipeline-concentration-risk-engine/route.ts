import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-pipeline-concentration-risk-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    concentration_risk: "low", concentration_pattern: "none",
    concentration_severity: "diversified", recommended_action: "no_action",
    deal_concentration_score: 0.0, account_concentration_score: 0.0,
    product_concentration_score: 0.0, stage_concentration_score: 0.0,
    concentration_composite: 0.0, is_fragile_pipeline: false, requires_rebalancing: false,
    estimated_at_risk_revenue_usd: 0.0,
    concentration_signal: "Pipeline well-diversified across deals, accounts, and stages",
  },
  {
    rep_id: "rep_002", region: "East",
    concentration_risk: "low", concentration_pattern: "product_concentration",
    concentration_severity: "diversified", recommended_action: "no_action",
    deal_concentration_score: 5.0, account_concentration_score: 8.0,
    product_concentration_score: 24.0, stage_concentration_score: 6.0,
    concentration_composite: 9.8, is_fragile_pipeline: false, requires_rebalancing: false,
    estimated_at_risk_revenue_usd: 7840.0,
    concentration_signal: "Top product line 76% of pipeline — 3/5 lines — composite 10",
  },
  {
    rep_id: "rep_003", region: "Central",
    concentration_risk: "moderate", concentration_pattern: "stage_bottleneck",
    concentration_severity: "watch", recommended_action: "pipeline_diversification",
    deal_concentration_score: 12.0, account_concentration_score: 15.0,
    product_concentration_score: 18.0, stage_concentration_score: 48.0,
    concentration_composite: 20.3, is_fragile_pipeline: false, requires_rebalancing: false,
    estimated_at_risk_revenue_usd: 30450.0,
    concentration_signal: "72% of deals in single stage — 28% stale — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    concentration_risk: "moderate", concentration_pattern: "account_overexposure",
    concentration_severity: "watch", recommended_action: "pipeline_diversification",
    deal_concentration_score: 18.0, account_concentration_score: 38.0,
    product_concentration_score: 12.0, stage_concentration_score: 14.0,
    concentration_composite: 22.3, is_fragile_pipeline: false, requires_rebalancing: true,
    estimated_at_risk_revenue_usd: 44600.0,
    concentration_signal: "Top account $200K — 41% of pipeline — 4 unique accounts — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    concentration_risk: "high", concentration_pattern: "whale_dependency",
    concentration_severity: "concentrated", recommended_action: "rep_rebalancing",
    deal_concentration_score: 55.0, account_concentration_score: 40.0,
    product_concentration_score: 20.0, stage_concentration_score: 18.0,
    concentration_composite: 39.0, is_fragile_pipeline: false, requires_rebalancing: true,
    estimated_at_risk_revenue_usd: 117000.0,
    concentration_signal: "Top deal $270K — 47% of pipeline — composite 39",
  },
  {
    rep_id: "rep_006", region: "West",
    concentration_risk: "high", concentration_pattern: "whale_dependency",
    concentration_severity: "concentrated", recommended_action: "rep_rebalancing",
    deal_concentration_score: 68.0, account_concentration_score: 55.0,
    product_concentration_score: 25.0, stage_concentration_score: 22.0,
    concentration_composite: 48.4, is_fragile_pipeline: true, requires_rebalancing: true,
    estimated_at_risk_revenue_usd: 193600.0,
    concentration_signal: "Top deal $400K — 62% of pipeline — composite 48",
  },
  {
    rep_id: "rep_007", region: "APAC",
    concentration_risk: "critical", concentration_pattern: "rep_single_point",
    concentration_severity: "critical", recommended_action: "forecast_risk_flag",
    deal_concentration_score: 60.0, account_concentration_score: 70.0,
    product_concentration_score: 35.0, stage_concentration_score: 40.0,
    concentration_composite: 57.8, is_fragile_pipeline: true, requires_rebalancing: true,
    estimated_at_risk_revenue_usd: 289000.0,
    concentration_signal: "90% pipeline held by single rep — 2 deals — composite 58",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    concentration_risk: "critical", concentration_pattern: "whale_dependency",
    concentration_severity: "critical", recommended_action: "executive_review",
    deal_concentration_score: 82.0, account_concentration_score: 78.0,
    product_concentration_score: 50.0, stage_concentration_score: 45.0,
    concentration_composite: 70.6, is_fragile_pipeline: true, requires_rebalancing: true,
    estimated_at_risk_revenue_usd: 423600.0,
    concentration_signal: "Top deal $580K — 75% of pipeline — composite 71",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-pipeline-concentration-risk-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.concentration_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.concentration_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_deal = 0, total_acc = 0, total_prod = 0, total_stg = 0;
  let total_rev = 0;

  for (const r of mockReps) {
    risk_counts[r.concentration_risk]       = (risk_counts[r.concentration_risk] || 0) + 1;
    pattern_counts[r.concentration_pattern] = (pattern_counts[r.concentration_pattern] || 0) + 1;
    severity_counts[r.concentration_severity] = (severity_counts[r.concentration_severity] || 0) + 1;
    action_counts[r.recommended_action]       = (action_counts[r.recommended_action] || 0) + 1;
    total_comp  += r.concentration_composite;
    total_deal  += r.deal_concentration_score;
    total_acc   += r.account_concentration_score;
    total_prod  += r.product_concentration_score;
    total_stg   += r.stage_concentration_score;
    total_rev   += r.estimated_at_risk_revenue_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                                n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_concentration_composite:          Math.round((total_comp / n) * 10) / 10,
      fragile_pipeline_count:               mockReps.filter((r) => r.is_fragile_pipeline).length,
      rebalancing_count:                    mockReps.filter((r) => r.requires_rebalancing).length,
      avg_deal_concentration_score:         Math.round((total_deal / n) * 10) / 10,
      avg_account_concentration_score:      Math.round((total_acc  / n) * 10) / 10,
      avg_product_concentration_score:      Math.round((total_prod / n) * 10) / 10,
      avg_stage_concentration_score:        Math.round((total_stg  / n) * 10) / 10,
      total_estimated_at_risk_revenue_usd:  Math.round(total_rev * 100) / 100,
    },
  }));
}
