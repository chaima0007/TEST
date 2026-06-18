import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    efficiency_risk: "low", efficiency_pattern: "none",
    efficiency_severity: "healthy", recommended_action: "no_action",
    activity_volume_score: 0.0, conversion_efficiency_score: 0.0,
    pipeline_coverage_score: 0.0, activity_mix_score: 0.0,
    pipeline_efficiency_composite: 0.0, is_pipeline_at_risk: false,
    requires_activity_intervention: false, estimated_pipeline_gap_usd: 0.0,
    efficiency_signal: "Pipeline generation efficiency within targets",
  },
  {
    rep_id: "rep_002", region: "East",
    efficiency_risk: "low", efficiency_pattern: "none",
    efficiency_severity: "healthy", recommended_action: "no_action",
    activity_volume_score: 28.0, conversion_efficiency_score: 27.0,
    pipeline_coverage_score: 10.0, activity_mix_score: 0.0,
    pipeline_efficiency_composite: 18.9, is_pipeline_at_risk: true,
    requires_activity_intervention: false, estimated_pipeline_gap_usd: 22680.0,
    efficiency_signal: "Pipeline generation efficiency within targets",
  },
  {
    rep_id: "rep_003", region: "Central",
    efficiency_risk: "moderate", efficiency_pattern: "low_activity_volume",
    efficiency_severity: "underperforming", recommended_action: "activity_increase",
    activity_volume_score: 43.0, conversion_efficiency_score: 27.0,
    pipeline_coverage_score: 25.0, activity_mix_score: 10.0,
    pipeline_efficiency_composite: 28.4, is_pipeline_at_risk: true,
    requires_activity_intervention: false, estimated_pipeline_gap_usd: 85200.0,
    efficiency_signal: "Low activity volume — 75 total activities — 40% pipeline coverage — composite 28",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    efficiency_risk: "moderate", efficiency_pattern: "poor_conversion",
    efficiency_severity: "underperforming", recommended_action: "activity_increase",
    activity_volume_score: 20.0, conversion_efficiency_score: 55.0,
    pipeline_coverage_score: 25.0, activity_mix_score: 22.0,
    pipeline_efficiency_composite: 33.6, is_pipeline_at_risk: true,
    requires_activity_intervention: false, estimated_pipeline_gap_usd: 112560.0,
    efficiency_signal: "Poor conversion — 20% demo-to-opp rate — 0% call connect rate — composite 34",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    efficiency_risk: "high", efficiency_pattern: "pipeline_coverage_gap",
    efficiency_severity: "degraded", recommended_action: "conversion_coaching",
    activity_volume_score: 60.0, conversion_efficiency_score: 55.0,
    pipeline_coverage_score: 40.0, activity_mix_score: 22.0,
    pipeline_efficiency_composite: 47.2, is_pipeline_at_risk: true,
    requires_activity_intervention: true, estimated_pipeline_gap_usd: 236000.0,
    efficiency_signal: "Pipeline coverage gap — 35 total activities — 20% demo-to-opp rate — 30% pipeline coverage — composite 47",
  },
  {
    rep_id: "rep_006", region: "West",
    efficiency_risk: "high", efficiency_pattern: "activity_channel_overreliance",
    efficiency_severity: "degraded", recommended_action: "conversion_coaching",
    activity_volume_score: 43.0, conversion_efficiency_score: 57.0,
    pipeline_coverage_score: 40.0, activity_mix_score: 48.0,
    pipeline_efficiency_composite: 47.2, is_pipeline_at_risk: true,
    requires_activity_intervention: true, estimated_pipeline_gap_usd: 188800.0,
    efficiency_signal: "Activity channel overreliance — 60 total activities — 25% demo-to-opp rate — 20% pipeline coverage — composite 47",
  },
  {
    rep_id: "rep_007", region: "APAC",
    efficiency_risk: "critical", efficiency_pattern: "activity_decay",
    efficiency_severity: "critical", recommended_action: "performance_improvement_plan",
    activity_volume_score: 75.0, conversion_efficiency_score: 85.0,
    pipeline_coverage_score: 70.0, activity_mix_score: 55.0,
    pipeline_efficiency_composite: 72.5, is_pipeline_at_risk: true,
    requires_activity_intervention: true, estimated_pipeline_gap_usd: 362500.0,
    efficiency_signal: "Activity decay — 20 total activities — 10% demo-to-opp rate — 20% pipeline coverage — 5% call connect rate — composite 73",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    efficiency_risk: "critical", efficiency_pattern: "activity_decay",
    efficiency_severity: "critical", recommended_action: "performance_improvement_plan",
    activity_volume_score: 100.0, conversion_efficiency_score: 100.0,
    pipeline_coverage_score: 100.0, activity_mix_score: 70.0,
    pipeline_efficiency_composite: 93.5, is_pipeline_at_risk: true,
    requires_activity_intervention: true, estimated_pipeline_gap_usd: 467500.0,
    efficiency_signal: "Activity decay — 12 total activities — 5% demo-to-opp rate — 0% pipeline coverage — 2% call connect rate — composite 94",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/pipeline-generation-efficiency-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.efficiency_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.efficiency_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_vol = 0, total_conv = 0, total_cov = 0, total_mix = 0, total_gap = 0;

  for (const r of mockReps) {
    risk_counts[r.efficiency_risk]           = (risk_counts[r.efficiency_risk] || 0) + 1;
    pattern_counts[r.efficiency_pattern]     = (pattern_counts[r.efficiency_pattern] || 0) + 1;
    severity_counts[r.efficiency_severity]   = (severity_counts[r.efficiency_severity] || 0) + 1;
    action_counts[r.recommended_action]      = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.pipeline_efficiency_composite;
    total_vol  += r.activity_volume_score;
    total_conv += r.conversion_efficiency_score;
    total_cov  += r.pipeline_coverage_score;
    total_mix  += r.activity_mix_score;
    total_gap  += r.estimated_pipeline_gap_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                              n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_pipeline_efficiency_composite:  Math.round((total_comp / n) * 10) / 10,
      pipeline_at_risk_count:             mockReps.filter((r) => r.is_pipeline_at_risk).length,
      activity_intervention_count:        mockReps.filter((r) => r.requires_activity_intervention).length,
      avg_activity_volume_score:          Math.round((total_vol / n) * 10) / 10,
      avg_conversion_efficiency_score:    Math.round((total_conv / n) * 10) / 10,
      avg_pipeline_coverage_score:        Math.round((total_cov / n) * 10) / 10,
      avg_activity_mix_score:             Math.round((total_mix / n) * 10) / 10,
      total_estimated_pipeline_gap_usd:   Math.round(total_gap * 100) / 100,
    },
  });
}
