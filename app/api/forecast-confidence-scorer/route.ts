import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", rep_name: "Alice Martin", manager_id: "mgr_001",
    confidence_level: "committed", forecast_pattern: "reliable",
    pipeline_health: "healthy", forecast_action: "accept",
    historical_accuracy_score: 88.0, pipeline_coverage_score: 92.0,
    deal_quality_score: 85.0, activity_signal_score: 82.0,
    forecast_composite: 88.6, attainment_probability: 91.0,
    pipeline_coverage_ratio: 4.1, is_forecast_reliable: true,
    needs_forecast_scrub: false, region: "NAMER",
  },
  {
    rep_id: "rep_002", rep_name: "Ben Torres", manager_id: "mgr_001",
    confidence_level: "low", forecast_pattern: "optimistic_bias",
    pipeline_health: "underpipelined", forecast_action: "escalate_to_manager",
    historical_accuracy_score: 22.0, pipeline_coverage_score: 15.0,
    deal_quality_score: 18.0, activity_signal_score: 20.0,
    forecast_composite: 18.9, attainment_probability: 22.0,
    pipeline_coverage_ratio: 1.2, is_forecast_reliable: false,
    needs_forecast_scrub: true, region: "EMEA",
  },
  {
    rep_id: "rep_003", rep_name: "Clara Nguyen", manager_id: "mgr_002",
    confidence_level: "high", forecast_pattern: "reliable",
    pipeline_health: "adequate", forecast_action: "accept",
    historical_accuracy_score: 68.0, pipeline_coverage_score: 65.0,
    deal_quality_score: 62.0, activity_signal_score: 60.0,
    forecast_composite: 64.9, attainment_probability: 68.0,
    pipeline_coverage_ratio: 2.5, is_forecast_reliable: false,
    needs_forecast_scrub: false, region: "APAC",
  },
  {
    rep_id: "rep_004", rep_name: "David Kim", manager_id: "mgr_002",
    confidence_level: "moderate", forecast_pattern: "volatile",
    pipeline_health: "adequate", forecast_action: "scrub_required",
    historical_accuracy_score: 38.0, pipeline_coverage_score: 42.0,
    deal_quality_score: 35.0, activity_signal_score: 40.0,
    forecast_composite: 39.4, attainment_probability: 38.0,
    pipeline_coverage_ratio: 2.2, is_forecast_reliable: false,
    needs_forecast_scrub: true, region: "NAMER",
  },
  {
    rep_id: "rep_005", rep_name: "Eva Rossi", manager_id: "mgr_003",
    confidence_level: "committed", forecast_pattern: "reliable",
    pipeline_health: "healthy", forecast_action: "accept",
    historical_accuracy_score: 92.0, pipeline_coverage_score: 88.0,
    deal_quality_score: 90.0, activity_signal_score: 85.0,
    forecast_composite: 89.4, attainment_probability: 94.0,
    pipeline_coverage_ratio: 3.8, is_forecast_reliable: true,
    needs_forecast_scrub: false, region: "EMEA",
  },
  {
    rep_id: "rep_006", rep_name: "Frank Li", manager_id: "mgr_003",
    confidence_level: "moderate", forecast_pattern: "sandbagging",
    pipeline_health: "overpipelined", forecast_action: "review_with_rep",
    historical_accuracy_score: 55.0, pipeline_coverage_score: 72.0,
    deal_quality_score: 58.0, activity_signal_score: 62.0,
    forecast_composite: 63.0, attainment_probability: 55.0,
    pipeline_coverage_ratio: 5.8, is_forecast_reliable: false,
    needs_forecast_scrub: false, region: "APAC",
  },
  {
    rep_id: "rep_007", rep_name: "Grace Obi", manager_id: "mgr_004",
    confidence_level: "high", forecast_pattern: "reliable",
    pipeline_health: "healthy", forecast_action: "accept",
    historical_accuracy_score: 75.0, pipeline_coverage_score: 78.0,
    deal_quality_score: 72.0, activity_signal_score: 68.0,
    forecast_composite: 74.9, attainment_probability: 77.0,
    pipeline_coverage_ratio: 3.2, is_forecast_reliable: true,
    needs_forecast_scrub: false, region: "LATAM",
  },
  {
    rep_id: "rep_008", rep_name: "Hugo Patel", manager_id: "mgr_004",
    confidence_level: "low", forecast_pattern: "insufficient",
    pipeline_health: "underpipelined", forecast_action: "escalate_to_manager",
    historical_accuracy_score: 10.0, pipeline_coverage_score: 8.0,
    deal_quality_score: 12.0, activity_signal_score: 15.0,
    forecast_composite: 10.4, attainment_probability: 12.0,
    pipeline_coverage_ratio: 0.9, is_forecast_reliable: false,
    needs_forecast_scrub: true, region: "NAMER",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const confidence = searchParams.get("confidence");
  const pattern    = searchParams.get("pattern");
  const region     = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/forecast-confidence-scorer`);
      if (confidence) url.searchParams.set("confidence", confidence);
      if (pattern)    url.searchParams.set("pattern", pattern);
      if (region)     url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (confidence) reps = reps.filter((r) => r.confidence_level === confidence);
  if (pattern)    reps = reps.filter((r) => r.forecast_pattern === pattern);
  if (region)     reps = reps.filter((r) => r.region === region);

  const confidence_counts: Record<string, number> = {};
  const pattern_counts:    Record<string, number> = {};
  const health_counts:     Record<string, number> = {};
  const action_counts:     Record<string, number> = {};
  let total_comp = 0, total_attain = 0, total_hist = 0,
      total_pipe = 0, total_qual = 0, total_act = 0;

  for (const r of mockReps) {
    confidence_counts[r.confidence_level] = (confidence_counts[r.confidence_level] || 0) + 1;
    pattern_counts[r.forecast_pattern]    = (pattern_counts[r.forecast_pattern] || 0) + 1;
    health_counts[r.pipeline_health]      = (health_counts[r.pipeline_health] || 0) + 1;
    action_counts[r.forecast_action]      = (action_counts[r.forecast_action] || 0) + 1;
    total_comp   += r.forecast_composite;
    total_attain += r.attainment_probability;
    total_hist   += r.historical_accuracy_score;
    total_pipe   += r.pipeline_coverage_score;
    total_qual   += r.deal_quality_score;
    total_act    += r.activity_signal_score;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total: n,
      confidence_counts,
      pattern_counts,
      pipeline_health_counts: health_counts,
      action_counts,
      avg_forecast_composite:         Math.round((total_comp / n) * 10) / 10,
      avg_attainment_probability:     Math.round((total_attain / n) * 10) / 10,
      reliable_count:                 mockReps.filter((r) => r.is_forecast_reliable).length,
      scrub_count:                    mockReps.filter((r) => r.needs_forecast_scrub).length,
      avg_historical_accuracy_score:  Math.round((total_hist / n) * 10) / 10,
      avg_pipeline_coverage_score:    Math.round((total_pipe / n) * 10) / 10,
      avg_deal_quality_score:         Math.round((total_qual / n) * 10) / 10,
      avg_activity_signal_score:      Math.round((total_act / n) * 10) / 10,
    },
  });
}
