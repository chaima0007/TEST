import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    quota_risk: "low", quota_pattern: "none",
    quota_severity: "disciplined", recommended_action: "no_action",
    pacing_score: 0.0, consistency_score: 0.0,
    forecast_score: 0.0, pipeline_health_score: 0.0,
    quota_composite: 0.0,
    has_quota_gap: false, requires_quota_coaching: false,
    estimated_revenue_at_risk_usd: 0.0,
    quota_signal: "Quota attainment healthy — pacing, consistency, and forecast accuracy within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    quota_risk: "low", quota_pattern: "none",
    quota_severity: "disciplined", recommended_action: "no_action",
    pacing_score: 4.0, consistency_score: 3.0,
    forecast_score: 5.0, pipeline_health_score: 2.0,
    quota_composite: 3.65,
    has_quota_gap: false, requires_quota_coaching: false,
    estimated_revenue_at_risk_usd: 0.0,
    quota_signal: "Quota attainment healthy — pacing, consistency, and forecast accuracy within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    quota_risk: "moderate", quota_pattern: "early_coasting",
    quota_severity: "developing", recommended_action: "pipeline_pacing_coaching",
    pacing_score: 20.0, consistency_score: 22.0,
    forecast_score: 18.0, pipeline_health_score: 15.0,
    quota_composite: 19.55,
    has_quota_gap: false, requires_quota_coaching: false,
    estimated_revenue_at_risk_usd: 24000.0,
    quota_signal: "Early coasting — 88% quota attained — 28% deals in final 2 weeks — 82% forecast accuracy — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    quota_risk: "moderate", quota_pattern: "late_quarter_cliff",
    quota_severity: "developing", recommended_action: "pipeline_pacing_coaching",
    pacing_score: 30.0, consistency_score: 25.0,
    forecast_score: 22.0, pipeline_health_score: 18.0,
    quota_composite: 25.2,
    has_quota_gap: false, requires_quota_coaching: true,
    estimated_revenue_at_risk_usd: 48000.0,
    quota_signal: "Late quarter cliff — 82% quota attained — 52% deals in final 2 weeks — 74% forecast accuracy — composite 25",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    quota_risk: "high", quota_pattern: "feast_or_famine",
    quota_severity: "inconsistent", recommended_action: "activity_rhythm_coaching",
    pacing_score: 35.0, consistency_score: 48.0,
    forecast_score: 38.0, pipeline_health_score: 32.0,
    quota_composite: 39.15,
    has_quota_gap: false, requires_quota_coaching: true,
    estimated_revenue_at_risk_usd: 112000.0,
    quota_signal: "Feast or famine — 72% quota attained — 46% deals in final 2 weeks — 65% forecast accuracy — composite 39",
  },
  {
    rep_id: "rep_006", region: "West",
    quota_risk: "high", quota_pattern: "sandbagging",
    quota_severity: "inconsistent", recommended_action: "pipeline_pacing_coaching",
    pacing_score: 42.0, consistency_score: 38.0,
    forecast_score: 45.0, pipeline_health_score: 40.0,
    quota_composite: 41.55,
    has_quota_gap: true, requires_quota_coaching: true,
    estimated_revenue_at_risk_usd: 185000.0,
    quota_signal: "Sandbagging — 68% quota attained — 55% deals in final 2 weeks — 58% forecast accuracy — composite 42",
  },
  {
    rep_id: "rep_007", region: "APAC",
    quota_risk: "critical", quota_pattern: "consistent_underperformance",
    quota_severity: "at_risk", recommended_action: "performance_improvement_plan",
    pacing_score: 65.0, consistency_score: 70.0,
    forecast_score: 62.0, pipeline_health_score: 58.0,
    quota_composite: 65.2,
    has_quota_gap: true, requires_quota_coaching: true,
    estimated_revenue_at_risk_usd: 420000.0,
    quota_signal: "Consistent underperformance — 52% quota attained — 72% deals in final 2 weeks — 48% forecast accuracy — composite 65",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    quota_risk: "critical", quota_pattern: "consistent_underperformance",
    quota_severity: "at_risk", recommended_action: "performance_improvement_plan",
    pacing_score: 100.0, consistency_score: 100.0,
    forecast_score: 100.0, pipeline_health_score: 100.0,
    quota_composite: 100.0,
    has_quota_gap: true, requires_quota_coaching: true,
    estimated_revenue_at_risk_usd: 880000.0,
    quota_signal: "Consistent underperformance — 45% quota attained — 75% deals in final 2 weeks — 45% forecast accuracy — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-quota-attainment-pattern-intelligence-engine`);
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
  let total_comp = 0, total_pac = 0, total_con = 0, total_for = 0, total_pip = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.quota_risk]         = (risk_counts[r.quota_risk] || 0) + 1;
    pattern_counts[r.quota_pattern]   = (pattern_counts[r.quota_pattern] || 0) + 1;
    severity_counts[r.quota_severity] = (severity_counts[r.quota_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.quota_composite;
    total_pac  += r.pacing_score;
    total_con  += r.consistency_score;
    total_for  += r.forecast_score;
    total_pip  += r.pipeline_health_score;
    total_loss += r.estimated_revenue_at_risk_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                  n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_quota_composite:                    Math.round((total_comp / n) * 10) / 10,
      quota_gap_count:                        mockReps.filter((r) => r.has_quota_gap).length,
      coaching_count:                         mockReps.filter((r) => r.requires_quota_coaching).length,
      avg_pacing_score:                       Math.round((total_pac / n) * 10) / 10,
      avg_consistency_score:                  Math.round((total_con / n) * 10) / 10,
      avg_forecast_score:                     Math.round((total_for / n) * 10) / 10,
      avg_pipeline_health_score:              Math.round((total_pip / n) * 10) / 10,
      total_estimated_revenue_at_risk_usd:    Math.round(total_loss * 100) / 100,
    },
  });
}
