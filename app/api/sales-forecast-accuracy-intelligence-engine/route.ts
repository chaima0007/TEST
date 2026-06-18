import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    forecast_risk: "low", forecast_pattern: "none",
    forecast_severity: "precise", recommended_action: "no_action",
    accuracy_score: 0.0, discipline_score: 0.0,
    stage_score: 0.0, commit_score: 0.0,
    forecast_composite: 0.0,
    has_forecast_gap: false, requires_forecast_coaching: false,
    estimated_revenue_at_risk_usd: 0.0,
    forecast_signal: "Forecast accuracy healthy — variance, commit discipline, and stage accuracy within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    forecast_risk: "low", forecast_pattern: "none",
    forecast_severity: "precise", recommended_action: "no_action",
    accuracy_score: 3.0, discipline_score: 4.0,
    stage_score: 2.0, commit_score: 5.0,
    forecast_composite: 3.35,
    has_forecast_gap: false, requires_forecast_coaching: false,
    estimated_revenue_at_risk_usd: 0.0,
    forecast_signal: "Forecast accuracy healthy — variance, commit discipline, and stage accuracy within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    forecast_risk: "moderate", forecast_pattern: "chronic_under_forecasting",
    forecast_severity: "calibrating", recommended_action: "forecast_calibration_coaching",
    accuracy_score: 18.0, discipline_score: 20.0,
    stage_score: 22.0, commit_score: 15.0,
    forecast_composite: 19.45,
    has_forecast_gap: false, requires_forecast_coaching: true,
    estimated_revenue_at_risk_usd: 36000.0,
    forecast_signal: "Chronic under forecasting — 12% forecast variance — 58% commit-to-close rate — 10% committed deals lost — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    forecast_risk: "moderate", forecast_pattern: "recency_bias_sandbagging",
    forecast_severity: "calibrating", recommended_action: "forecast_calibration_coaching",
    accuracy_score: 22.0, discipline_score: 25.0,
    stage_score: 18.0, commit_score: 20.0,
    forecast_composite: 21.7,
    has_forecast_gap: false, requires_forecast_coaching: true,
    estimated_revenue_at_risk_usd: 84000.0,
    forecast_signal: "Recency bias sandbagging — 15% forecast variance — 62% commit-to-close rate — 15% committed deals lost — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    forecast_risk: "high", forecast_pattern: "end_of_quarter_cliff",
    forecast_severity: "drifting", recommended_action: "pipeline_inspection_coaching",
    accuracy_score: 40.0, discipline_score: 45.0,
    stage_score: 38.0, commit_score: 30.0,
    forecast_composite: 39.2,
    has_forecast_gap: false, requires_forecast_coaching: true,
    estimated_revenue_at_risk_usd: 228000.0,
    forecast_signal: "End of quarter cliff — 25% forecast variance — 48% commit-to-close rate — 25% committed deals lost — composite 39",
  },
  {
    rep_id: "rep_006", region: "West",
    forecast_risk: "high", forecast_pattern: "chronic_over_forecasting",
    forecast_severity: "drifting", recommended_action: "commit_discipline_coaching",
    accuracy_score: 52.0, discipline_score: 48.0,
    stage_score: 42.0, commit_score: 55.0,
    forecast_composite: 49.55,
    has_forecast_gap: true, requires_forecast_coaching: true,
    estimated_revenue_at_risk_usd: 540000.0,
    forecast_signal: "Chronic over forecasting — 30% forecast variance — 38% commit-to-close rate — 35% committed deals lost — composite 50",
  },
  {
    rep_id: "rep_007", region: "APAC",
    forecast_risk: "critical", forecast_pattern: "stage_inflation_blindspot",
    forecast_severity: "unreliable", recommended_action: "stage_criteria_coaching",
    accuracy_score: 72.0, discipline_score: 68.0,
    stage_score: 75.0, commit_score: 65.0,
    forecast_composite: 71.2,
    has_forecast_gap: true, requires_forecast_coaching: true,
    estimated_revenue_at_risk_usd: 1440000.0,
    forecast_signal: "Stage inflation blindspot — 42% forecast variance — 30% commit-to-close rate — 45% committed deals lost — composite 71",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    forecast_risk: "critical", forecast_pattern: "stage_inflation_blindspot",
    forecast_severity: "unreliable", recommended_action: "stage_criteria_coaching",
    accuracy_score: 100.0, discipline_score: 100.0,
    stage_score: 100.0, commit_score: 100.0,
    forecast_composite: 100.0,
    has_forecast_gap: true, requires_forecast_coaching: true,
    estimated_revenue_at_risk_usd: 2400000.0,
    forecast_signal: "Stage inflation blindspot — 50% forecast variance — 30% commit-to-close rate — 50% committed deals lost — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-forecast-accuracy-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.forecast_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.forecast_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_acc = 0, total_dis = 0, total_sta = 0, total_com = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.forecast_risk]         = (risk_counts[r.forecast_risk] || 0) + 1;
    pattern_counts[r.forecast_pattern]   = (pattern_counts[r.forecast_pattern] || 0) + 1;
    severity_counts[r.forecast_severity] = (severity_counts[r.forecast_severity] || 0) + 1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.forecast_composite;
    total_acc  += r.accuracy_score;
    total_dis  += r.discipline_score;
    total_sta  += r.stage_score;
    total_com  += r.commit_score;
    total_loss += r.estimated_revenue_at_risk_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                 n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_forecast_composite:                Math.round((total_comp / n) * 10) / 10,
      forecast_gap_count:                    mockReps.filter((r) => r.has_forecast_gap).length,
      coaching_count:                        mockReps.filter((r) => r.requires_forecast_coaching).length,
      avg_accuracy_score:                    Math.round((total_acc / n) * 10) / 10,
      avg_discipline_score:                  Math.round((total_dis / n) * 10) / 10,
      avg_stage_score:                       Math.round((total_sta / n) * 10) / 10,
      avg_commit_score:                      Math.round((total_com / n) * 10) / 10,
      total_estimated_revenue_at_risk_usd:   Math.round(total_loss * 100) / 100,
    },
  });
}
