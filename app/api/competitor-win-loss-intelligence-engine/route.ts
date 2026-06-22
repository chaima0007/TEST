import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[competitor-win-loss-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    competitive_risk: "low", competitive_pattern: "none",
    competitive_severity: "stable", recommended_action: "no_action",
    price_vulnerability_score: 0.0, feature_gap_score: 0.0,
    intel_coverage_score: 0.0, execution_quality_score: 0.0,
    competitive_composite: 0.0, is_competitive_risk: false, requires_battlecard_update: false,
    estimated_revenue_at_risk_usd: 0.0,
    competitive_signal: "Competitive win/loss within healthy parameters",
  },
  {
    rep_id: "rep_002", region: "East",
    competitive_risk: "low", competitive_pattern: "none",
    competitive_severity: "stable", recommended_action: "monitor",
    price_vulnerability_score: 8.0, feature_gap_score: 5.0,
    intel_coverage_score: 12.0, execution_quality_score: 4.0,
    competitive_composite: 7.5, is_competitive_risk: false, requires_battlecard_update: false,
    estimated_revenue_at_risk_usd: 3750.0,
    competitive_signal: "Competitive win/loss within healthy parameters",
  },
  {
    rep_id: "rep_003", region: "Central",
    competitive_risk: "moderate", competitive_pattern: "intel_blindspot",
    competitive_severity: "watch", recommended_action: "battlecard_update",
    price_vulnerability_score: 10.0, feature_gap_score: 8.0,
    intel_coverage_score: 38.0, execution_quality_score: 12.0,
    competitive_composite: 17.5, is_competitive_risk: false, requires_battlecard_update: false,
    estimated_revenue_at_risk_usd: 17500.0,
    competitive_signal: "4 deals without intel — battlecard usage 1/6 — composite 18",
  },
  {
    rep_id: "rep_004", region: "Southeast",
    competitive_risk: "moderate", competitive_pattern: "price_displacement",
    competitive_severity: "watch", recommended_action: "battlecard_update",
    price_vulnerability_score: 42.0, feature_gap_score: 12.0,
    intel_coverage_score: 15.0, execution_quality_score: 10.0,
    competitive_composite: 22.0, is_competitive_risk: false, requires_battlecard_update: true,
    estimated_revenue_at_risk_usd: 44000.0,
    competitive_signal: "5 deals lost on price — 45% loss rate — composite 22",
  },
  {
    rep_id: "rep_005", region: "Northeast",
    competitive_risk: "high", competitive_pattern: "feature_gap",
    competitive_severity: "threatened", recommended_action: "sales_coaching",
    price_vulnerability_score: 15.0, feature_gap_score: 40.0,
    intel_coverage_score: 25.0, execution_quality_score: 18.0,
    competitive_composite: 25.5, is_competitive_risk: false, requires_battlecard_update: true,
    estimated_revenue_at_risk_usd: 76500.0,
    competitive_signal: "6 deals lost on features — 3 late-stage losses — composite 26",
  },
  {
    rep_id: "rep_006", region: "Northwest",
    competitive_risk: "high", competitive_pattern: "relationship_loss",
    competitive_severity: "threatened", recommended_action: "sales_coaching",
    price_vulnerability_score: 20.0, feature_gap_score: 22.0,
    intel_coverage_score: 20.0, execution_quality_score: 42.0,
    competitive_composite: 26.0, is_competitive_risk: false, requires_battlecard_update: true,
    estimated_revenue_at_risk_usd: 130000.0,
    competitive_signal: "4 relationship losses — 65d since last win — composite 26",
  },
  {
    rep_id: "rep_007", region: "Southwest",
    competitive_risk: "critical", competitive_pattern: "systematic_loss",
    competitive_severity: "critical", recommended_action: "executive_escalation",
    price_vulnerability_score: 55.0, feature_gap_score: 48.0,
    intel_coverage_score: 50.0, execution_quality_score: 45.0,
    competitive_composite: 50.3, is_competitive_risk: true, requires_battlecard_update: true,
    estimated_revenue_at_risk_usd: 377250.0,
    competitive_signal: "Loss streak 6 — 0 wins vs 9 losses — composite 50",
  },
  {
    rep_id: "rep_008", region: "Mountain",
    competitive_risk: "critical", competitive_pattern: "systematic_loss",
    competitive_severity: "critical", recommended_action: "executive_escalation",
    price_vulnerability_score: 65.0, feature_gap_score: 62.0,
    intel_coverage_score: 70.0, execution_quality_score: 55.0,
    competitive_composite: 63.9, is_competitive_risk: true, requires_battlecard_update: true,
    estimated_revenue_at_risk_usd: 575100.0,
    competitive_signal: "Loss streak 8 — 0 wins vs 10 losses — composite 64",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/competitor-win-loss-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.competitive_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.competitive_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_price = 0, total_feat = 0, total_intel = 0, total_exec = 0, total_rev = 0;

  for (const r of mockReps) {
    risk_counts[r.competitive_risk]       = (risk_counts[r.competitive_risk] || 0) + 1;
    pattern_counts[r.competitive_pattern] = (pattern_counts[r.competitive_pattern] || 0) + 1;
    severity_counts[r.competitive_severity] = (severity_counts[r.competitive_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp  += r.competitive_composite;
    total_price += r.price_vulnerability_score;
    total_feat  += r.feature_gap_score;
    total_intel += r.intel_coverage_score;
    total_exec  += r.execution_quality_score;
    total_rev   += r.estimated_revenue_at_risk_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                              n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_competitive_composite:          Math.round((total_comp  / n) * 10) / 10,
      competitive_risk_count:             mockReps.filter((r) => r.is_competitive_risk).length,
      battlecard_update_count:            mockReps.filter((r) => r.requires_battlecard_update).length,
      avg_price_vulnerability_score:      Math.round((total_price / n) * 10) / 10,
      avg_feature_gap_score:              Math.round((total_feat  / n) * 10) / 10,
      avg_intel_coverage_score:           Math.round((total_intel / n) * 10) / 10,
      avg_execution_quality_score:        Math.round((total_exec  / n) * 10) / 10,
      total_estimated_revenue_at_risk_usd: Math.round(total_rev * 100) / 100,
    },
  }));
}
