import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "r_001", rep_name: "Alice Martin", manager_id: "mgr_001", region: "EMEA",
    forecast_band: "commit", forecast_accuracy: "good", call_reliability: "high",
    forecast_action: "commit_as_is",
    adjusted_forecast: 426400, coverage_ratio: 3.2, sandbagging_score: 18.0,
    pipeline_health: 77.5, commit_vs_quota_pct: 84.0, upside_potential: 100000,
    is_at_risk: false, is_sandbagging: false,
    quota: 500000, submitted_commit: 420000, submitted_best_case: 520000,
    closed_won_qtd: 180000, late_stage_pipeline: 350000,
  },
  {
    rep_id: "r_002", rep_name: "Bruno Silva", manager_id: "mgr_002", region: "NAMER",
    forecast_band: "likely", forecast_accuracy: "poor", call_reliability: "unreliable",
    forecast_action: "escalate",
    adjusted_forecast: 280000, coverage_ratio: 1.2, sandbagging_score: 5.0,
    pipeline_health: 22.0, commit_vs_quota_pct: 72.0, upside_potential: 80000,
    is_at_risk: true, is_sandbagging: false,
    quota: 500000, submitted_commit: 360000, submitted_best_case: 440000,
    closed_won_qtd: 95000, late_stage_pipeline: 200000,
  },
  {
    rep_id: "r_003", rep_name: "Claire Dupont", manager_id: "mgr_001", region: "EMEA",
    forecast_band: "upside", forecast_accuracy: "excellent", call_reliability: "high",
    forecast_action: "adjust_up",
    adjusted_forecast: 588000, coverage_ratio: 4.1, sandbagging_score: 68.0,
    pipeline_health: 91.0, commit_vs_quota_pct: 90.0, upside_potential: 150000,
    is_at_risk: false, is_sandbagging: true,
    quota: 500000, submitted_commit: 450000, submitted_best_case: 600000,
    closed_won_qtd: 220000, late_stage_pipeline: 480000,
  },
  {
    rep_id: "r_004", rep_name: "David Chen", manager_id: "mgr_003", region: "APAC",
    forecast_band: "best_case", forecast_accuracy: "excellent", call_reliability: "high",
    forecast_action: "commit_as_is",
    adjusted_forecast: 571000, coverage_ratio: 3.8, sandbagging_score: 12.0,
    pipeline_health: 88.0, commit_vs_quota_pct: 110.0, upside_potential: 20000,
    is_at_risk: false, is_sandbagging: false,
    quota: 500000, submitted_commit: 550000, submitted_best_case: 570000,
    closed_won_qtd: 280000, late_stage_pipeline: 420000,
  },
  {
    rep_id: "r_005", rep_name: "Eva Müller", manager_id: "mgr_002", region: "NAMER",
    forecast_band: "likely", forecast_accuracy: "fair", call_reliability: "low",
    forecast_action: "investigate",
    adjusted_forecast: 312000, coverage_ratio: 1.8, sandbagging_score: 22.0,
    pipeline_health: 38.0, commit_vs_quota_pct: 78.0, upside_potential: 120000,
    is_at_risk: true, is_sandbagging: false,
    quota: 500000, submitted_commit: 390000, submitted_best_case: 510000,
    closed_won_qtd: 110000, late_stage_pipeline: 280000,
  },
  {
    rep_id: "r_006", rep_name: "François Leblanc", manager_id: "mgr_001", region: "EMEA",
    forecast_band: "commit", forecast_accuracy: "good", call_reliability: "medium",
    forecast_action: "commit_as_is",
    adjusted_forecast: 408000, coverage_ratio: 2.9, sandbagging_score: 35.0,
    pipeline_health: 62.0, commit_vs_quota_pct: 82.0, upside_potential: 90000,
    is_at_risk: false, is_sandbagging: false,
    quota: 500000, submitted_commit: 410000, submitted_best_case: 500000,
    closed_won_qtd: 165000, late_stage_pipeline: 310000,
  },
  {
    rep_id: "r_007", rep_name: "Gina Rossi", manager_id: "mgr_004", region: "LATAM",
    forecast_band: "likely", forecast_accuracy: "poor", call_reliability: "unreliable",
    forecast_action: "adjust_down",
    adjusted_forecast: 264000, coverage_ratio: 2.1, sandbagging_score: 8.0,
    pipeline_health: 30.0, commit_vs_quota_pct: 68.0, upside_potential: 70000,
    is_at_risk: false, is_sandbagging: false,
    quota: 500000, submitted_commit: 340000, submitted_best_case: 410000,
    closed_won_qtd: 90000, late_stage_pipeline: 240000,
  },
  {
    rep_id: "r_008", rep_name: "Henry Park", manager_id: "mgr_003", region: "APAC",
    forecast_band: "commit", forecast_accuracy: "good", call_reliability: "medium",
    forecast_action: "commit_as_is",
    adjusted_forecast: 445000, coverage_ratio: 3.5, sandbagging_score: 28.0,
    pipeline_health: 70.0, commit_vs_quota_pct: 86.0, upside_potential: 110000,
    is_at_risk: false, is_sandbagging: false,
    quota: 500000, submitted_commit: 430000, submitted_best_case: 540000,
    closed_won_qtd: 195000, late_stage_pipeline: 375000,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const band     = searchParams.get("band");
  const accuracy = searchParams.get("accuracy");
  const region   = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-forecast`);
      if (band)     url.searchParams.set("band", band);
      if (accuracy) url.searchParams.set("accuracy", accuracy);
      if (region)   url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (band)     reps = reps.filter((r) => r.forecast_band === band);
  if (accuracy) reps = reps.filter((r) => r.forecast_accuracy === accuracy);
  if (region)   reps = reps.filter((r) => r.region === region);

  const band_counts:       Record<string, number> = {};
  const accuracy_counts:   Record<string, number> = {};
  const action_counts:     Record<string, number> = {};
  let total_coverage = 0, total_health = 0, total_adj = 0, total_upside = 0, total_sand = 0;

  for (const r of mockReps) {
    band_counts[r.forecast_band]         = (band_counts[r.forecast_band] || 0) + 1;
    accuracy_counts[r.forecast_accuracy] = (accuracy_counts[r.forecast_accuracy] || 0) + 1;
    action_counts[r.forecast_action]     = (action_counts[r.forecast_action] || 0) + 1;
    total_coverage += r.coverage_ratio;
    total_health   += r.pipeline_health;
    total_adj      += r.adjusted_forecast;
    total_upside   += r.upside_potential;
    total_sand     += r.sandbagging_score;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                   n,
      band_counts,
      accuracy_counts,
      action_counts,
      avg_coverage_ratio:      Math.round((total_coverage / n) * 100) / 100,
      avg_pipeline_health:     Math.round((total_health / n) * 10) / 10,
      total_adjusted_forecast: Math.round(total_adj * 100) / 100,
      at_risk_count:           mockReps.filter((r) => r.is_at_risk).length,
      sandbagging_count:       mockReps.filter((r) => r.is_sandbagging).length,
      high_reliability_count:  mockReps.filter((r) => r.call_reliability === "high").length,
      total_upside_potential:  Math.round(total_upside * 100) / 100,
      avg_sandbagging_score:   Math.round((total_sand / n) * 10) / 10,
    },
  });
}
