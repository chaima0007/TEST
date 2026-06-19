import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    quota_risk: "low", quota_pattern: "none",
    quota_severity: "on_track", recommended_action: "no_action",
    attainment_consistency_score: 0.0, deal_quality_score: 0.0,
    pipeline_health_score: 0.0, forecast_reliability_score: 0.0,
    quota_effectiveness_composite: 0.0,
    is_below_quota_threshold: false, requires_performance_intervention: false,
    estimated_quota_gap_usd: 0.0,
    quota_signal: "Quota attainment consistent and on track",
  },
  {
    rep_id: "rep_002", region: "East",
    quota_risk: "low", quota_pattern: "none",
    quota_severity: "on_track", recommended_action: "no_action",
    attainment_consistency_score: 5.0, deal_quality_score: 5.0,
    pipeline_health_score: 5.0, forecast_reliability_score: 5.0,
    quota_effectiveness_composite: 5.0,
    is_below_quota_threshold: false, requires_performance_intervention: false,
    estimated_quota_gap_usd: 0.0,
    quota_signal: "Quota attainment consistent and on track",
  },
  {
    rep_id: "rep_003", region: "Central",
    quota_risk: "moderate", quota_pattern: "late_quarter_surge",
    quota_severity: "developing", recommended_action: "quota_coaching",
    attainment_consistency_score: 20.0, deal_quality_score: 15.0,
    pipeline_health_score: 18.0, forecast_reliability_score: 22.0,
    quota_effectiveness_composite: 19.1,
    is_below_quota_threshold: false, requires_performance_intervention: false,
    estimated_quota_gap_usd: 7000.0,
    quota_signal: "Late quarter surge — 82% quota attainment — 1/4 quarters below quota — 2 deals pushed out — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    quota_risk: "moderate", quota_pattern: "quota_avoidance",
    quota_severity: "developing", recommended_action: "quota_coaching",
    attainment_consistency_score: 15.0, deal_quality_score: 25.0,
    pipeline_health_score: 22.0, forecast_reliability_score: 18.0,
    quota_effectiveness_composite: 19.85,
    is_below_quota_threshold: false, requires_performance_intervention: false,
    estimated_quota_gap_usd: 10000.0,
    quota_signal: "Quota avoidance — 80% quota attainment — 1/4 quarters below quota — 4 deals pushed out — composite 20",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    quota_risk: "high", quota_pattern: "early_drop_off",
    quota_severity: "at_risk", recommended_action: "deal_acceleration",
    attainment_consistency_score: 25.0, deal_quality_score: 20.0,
    pipeline_health_score: 35.0, forecast_reliability_score: 30.0,
    quota_effectiveness_composite: 27.25,
    is_below_quota_threshold: true, requires_performance_intervention: true,
    estimated_quota_gap_usd: 32000.0,
    quota_signal: "Early drop off — 68% quota attainment — 2/4 quarters below quota — 3 deals pushed out — composite 27",
  },
  {
    rep_id: "rep_006", region: "West",
    quota_risk: "high", quota_pattern: "consistent_underperformance",
    quota_severity: "at_risk", recommended_action: "quota_coaching",
    attainment_consistency_score: 40.0, deal_quality_score: 25.0,
    pipeline_health_score: 30.0, forecast_reliability_score: 28.0,
    quota_effectiveness_composite: 31.85,
    is_below_quota_threshold: true, requires_performance_intervention: true,
    estimated_quota_gap_usd: 50000.0,
    quota_signal: "Consistent underperformance — 55% quota attainment — 3/4 quarters below quota — composite 32",
  },
  {
    rep_id: "rep_007", region: "APAC",
    quota_risk: "critical", quota_pattern: "consistent_underperformance",
    quota_severity: "critical", recommended_action: "performance_plan",
    attainment_consistency_score: 70.0, deal_quality_score: 45.0,
    pipeline_health_score: 55.0, forecast_reliability_score: 60.0,
    quota_effectiveness_composite: 59.25,
    is_below_quota_threshold: true, requires_performance_intervention: true,
    estimated_quota_gap_usd: 140000.0,
    quota_signal: "Consistent underperformance — 40% quota attainment — 4/4 quarters below quota — 6 deals pushed out — composite 59",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    quota_risk: "critical", quota_pattern: "quota_avoidance",
    quota_severity: "critical", recommended_action: "deal_acceleration",
    attainment_consistency_score: 75.0, deal_quality_score: 55.0,
    pipeline_health_score: 65.0, forecast_reliability_score: 70.0,
    quota_effectiveness_composite: 66.5,
    is_below_quota_threshold: true, requires_performance_intervention: true,
    estimated_quota_gap_usd: 240000.0,
    quota_signal: "Quota avoidance — 32% quota attainment — 4/4 quarters below quota — 8 deals pushed out — composite 67",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-quota-attainment-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.quota_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.quota_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_con = 0, total_dq = 0, total_pipe = 0, total_fc = 0, total_gap = 0;

  for (const r of mockReps) {
    risk_counts[r.quota_risk]       = (risk_counts[r.quota_risk] || 0) + 1;
    pattern_counts[r.quota_pattern] = (pattern_counts[r.quota_pattern] || 0) + 1;
    severity_counts[r.quota_severity] = (severity_counts[r.quota_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.quota_effectiveness_composite;
    total_con  += r.attainment_consistency_score;
    total_dq   += r.deal_quality_score;
    total_pipe += r.pipeline_health_score;
    total_fc   += r.forecast_reliability_score;
    total_gap  += r.estimated_quota_gap_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_quota_effectiveness_composite:    Math.round((total_comp / n) * 10) / 10,
      below_quota_threshold_count:          mockReps.filter((r) => r.is_below_quota_threshold).length,
      performance_intervention_count:       mockReps.filter((r) => r.requires_performance_intervention).length,
      avg_attainment_consistency_score:     Math.round((total_con / n) * 10) / 10,
      avg_deal_quality_score:               Math.round((total_dq / n) * 10) / 10,
      avg_pipeline_health_score:            Math.round((total_pipe / n) * 10) / 10,
      avg_forecast_reliability_score:       Math.round((total_fc / n) * 10) / 10,
      total_estimated_quota_gap_usd:        Math.round(total_gap * 100) / 100,
    },
  });
}
