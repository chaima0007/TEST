import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-forecast-sandbagging-detector] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    sandbagging_risk: "low", sandbagging_pattern: "none",
    sandbagging_severity: "clean", recommended_action: "no_action",
    forecast_accuracy_score: 3.0, pattern_consistency_score: 4.0,
    deal_manipulation_score: 0.0, over_attainment_score: 5.0,
    sandbagging_composite: 3.0, is_sandbagging: false, requires_quota_review: false,
    estimated_hidden_pipeline_usd: 0.0,
    sandbagging_signal: "forecast behavior within normal parameters",
  },
  {
    rep_id: "rep_002", region: "East",
    sandbagging_risk: "moderate", sandbagging_pattern: "consistent_low",
    sandbagging_severity: "watch", recommended_action: "monitor",
    forecast_accuracy_score: 12.0, pattern_consistency_score: 18.0,
    deal_manipulation_score: 8.0, over_attainment_score: 12.0,
    sandbagging_composite: 12.3, is_sandbagging: false, requires_quota_review: false,
    estimated_hidden_pipeline_usd: 9840.0,
    sandbagging_signal: "avg over-attainment 128% vs peer avg 105% — composite 12",
  },
  {
    rep_id: "rep_003", region: "Central",
    sandbagging_risk: "moderate", sandbagging_pattern: "deal_hoarding",
    sandbagging_severity: "watch", recommended_action: "manager_review",
    forecast_accuracy_score: 18.0, pattern_consistency_score: 22.0,
    deal_manipulation_score: 30.0, over_attainment_score: 15.0,
    sandbagging_composite: 21.5, is_sandbagging: false, requires_quota_review: false,
    estimated_hidden_pipeline_usd: 43000.0,
    sandbagging_signal: "3 deals held from forecast (2 late-stage uncommitted) — composite 22",
  },
  {
    rep_id: "rep_004", region: "Southeast",
    sandbagging_risk: "high", sandbagging_pattern: "late_pushes",
    sandbagging_severity: "suspicious", recommended_action: "quota_recalibrate",
    forecast_accuracy_score: 38.0, pattern_consistency_score: 32.0,
    deal_manipulation_score: 30.0, over_attainment_score: 25.0,
    sandbagging_composite: 32.0, is_sandbagging: false, requires_quota_review: true,
    estimated_hidden_pipeline_usd: 96000.0,
    sandbagging_signal: "4 deal(s) pushed past period end — composite 32",
  },
  {
    rep_id: "rep_005", region: "Northeast",
    sandbagging_risk: "high", sandbagging_pattern: "forecast_delay",
    sandbagging_severity: "suspicious", recommended_action: "quota_recalibrate",
    forecast_accuracy_score: 50.0, pattern_consistency_score: 45.0,
    deal_manipulation_score: 25.0, over_attainment_score: 38.0,
    sandbagging_composite: 40.5, is_sandbagging: true, requires_quota_review: true,
    estimated_hidden_pipeline_usd: 162000.0,
    sandbagging_signal: "forecast submitted 7 days late — avoids early commitment — composite 41",
  },
  {
    rep_id: "rep_006", region: "Northwest",
    sandbagging_risk: "moderate", sandbagging_pattern: "pull_forward_abuse",
    sandbagging_severity: "watch", recommended_action: "manager_review",
    forecast_accuracy_score: 15.0, pattern_consistency_score: 20.0,
    deal_manipulation_score: 18.0, over_attainment_score: 30.0,
    sandbagging_composite: 20.5, is_sandbagging: false, requires_quota_review: false,
    estimated_hidden_pipeline_usd: 20500.0,
    sandbagging_signal: "4 deal(s) pulled from future period — composite 21",
  },
  {
    rep_id: "rep_007", region: "Southwest",
    sandbagging_risk: "critical", sandbagging_pattern: "deal_hoarding",
    sandbagging_severity: "confirmed", recommended_action: "compensation_audit",
    forecast_accuracy_score: 68.0, pattern_consistency_score: 72.0,
    deal_manipulation_score: 75.0, over_attainment_score: 55.0,
    sandbagging_composite: 68.3, is_sandbagging: true, requires_quota_review: true,
    estimated_hidden_pipeline_usd: 341500.0,
    sandbagging_signal: "6 deals held from forecast (4 late-stage uncommitted) — composite 68",
  },
  {
    rep_id: "rep_008", region: "Mountain",
    sandbagging_risk: "critical", sandbagging_pattern: "consistent_low",
    sandbagging_severity: "confirmed", recommended_action: "compensation_audit",
    forecast_accuracy_score: 50.0, pattern_consistency_score: 100.0,
    deal_manipulation_score: 45.0, over_attainment_score: 68.0,
    sandbagging_composite: 65.5, is_sandbagging: true, requires_quota_review: true,
    estimated_hidden_pipeline_usd: 524000.0,
    sandbagging_signal: "avg over-attainment 195% vs peer avg 108% — composite 66",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-forecast-sandbagging-detector`);
      if (risk)    url.searchParams.set("risk",    risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.sandbagging_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.sandbagging_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_acc = 0, total_pat = 0, total_deal = 0, total_over = 0, total_hidden = 0;

  for (const r of mockReps) {
    risk_counts[r.sandbagging_risk]       = (risk_counts[r.sandbagging_risk] || 0) + 1;
    pattern_counts[r.sandbagging_pattern] = (pattern_counts[r.sandbagging_pattern] || 0) + 1;
    severity_counts[r.sandbagging_severity] = (severity_counts[r.sandbagging_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp   += r.sandbagging_composite;
    total_acc    += r.forecast_accuracy_score;
    total_pat    += r.pattern_consistency_score;
    total_deal   += r.deal_manipulation_score;
    total_over   += r.over_attainment_score;
    total_hidden += r.estimated_hidden_pipeline_usd;
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
      avg_sandbagging_composite:          Math.round((total_comp / n) * 10) / 10,
      sandbagging_count:                  mockReps.filter((r) => r.is_sandbagging).length,
      quota_review_count:                 mockReps.filter((r) => r.requires_quota_review).length,
      avg_forecast_accuracy_score:        Math.round((total_acc  / n) * 10) / 10,
      avg_pattern_consistency_score:      Math.round((total_pat  / n) * 10) / 10,
      avg_deal_manipulation_score:        Math.round((total_deal / n) * 10) / 10,
      avg_over_attainment_score:          Math.round((total_over / n) * 10) / 10,
      total_estimated_hidden_pipeline_usd: Math.round(total_hidden * 100) / 100,
    },
  }));
}
