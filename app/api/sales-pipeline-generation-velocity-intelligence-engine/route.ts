import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    pipeline_risk: "low", pipeline_pattern: "none",
    pipeline_severity: "generating", recommended_action: "no_action",
    generation_rate_score: 0.0, pipeline_volume_score: 0.0,
    prospecting_quality_score: 0.0, consistency_score: 0.0,
    pipeline_composite: 0.0,
    has_pipeline_gap: false, requires_pipeline_coaching: false,
    estimated_pipeline_shortfall_usd: 0.0,
    pipeline_signal: "Pipeline generation healthy — outreach conversion, volume, and prospecting quality within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    pipeline_risk: "low", pipeline_pattern: "none",
    pipeline_severity: "generating", recommended_action: "no_action",
    generation_rate_score: 4.0, pipeline_volume_score: 3.0,
    prospecting_quality_score: 5.0, consistency_score: 2.0,
    pipeline_composite: 3.65,
    has_pipeline_gap: false, requires_pipeline_coaching: false,
    estimated_pipeline_shortfall_usd: 0.0,
    pipeline_signal: "Pipeline generation healthy — outreach conversion, volume, and prospecting quality within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    pipeline_risk: "moderate", pipeline_pattern: "slow_starter",
    pipeline_severity: "adequate", recommended_action: "pipeline_generation_coaching",
    generation_rate_score: 20.0, pipeline_volume_score: 18.0,
    prospecting_quality_score: 22.0, consistency_score: 15.0,
    pipeline_composite: 19.55,
    has_pipeline_gap: false, requires_pipeline_coaching: true,
    estimated_pipeline_shortfall_usd: 128000.0,
    pipeline_signal: "Slow starter — 9% outreach-to-connect — 1.0 new opps/week — 1 consecutive low-pipeline weeks — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    pipeline_risk: "moderate", pipeline_pattern: "channel_dependency",
    pipeline_severity: "adequate", recommended_action: "pipeline_generation_coaching",
    generation_rate_score: 22.0, pipeline_volume_score: 20.0,
    prospecting_quality_score: 18.0, consistency_score: 25.0,
    pipeline_composite: 21.35,
    has_pipeline_gap: false, requires_pipeline_coaching: true,
    estimated_pipeline_shortfall_usd: 256000.0,
    pipeline_signal: "Channel dependency — 8% outreach-to-connect — 0.8 new opps/week — 2 consecutive low-pipeline weeks — composite 21",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    pipeline_risk: "high", pipeline_pattern: "reactive_only",
    pipeline_severity: "sluggish", recommended_action: "pipeline_generation_coaching",
    generation_rate_score: 42.0, pipeline_volume_score: 38.0,
    prospecting_quality_score: 35.0, consistency_score: 40.0,
    pipeline_composite: 39.25,
    has_pipeline_gap: true, requires_pipeline_coaching: true,
    estimated_pipeline_shortfall_usd: 864000.0,
    pipeline_signal: "Reactive only — 6% outreach-to-connect — 0.5 new opps/week — 3 consecutive low-pipeline weeks — composite 39",
  },
  {
    rep_id: "rep_006", region: "West",
    pipeline_risk: "high", pipeline_pattern: "territory_exhaustion",
    pipeline_severity: "sluggish", recommended_action: "icp_targeting_coaching",
    generation_rate_score: 48.0, pipeline_volume_score: 45.0,
    prospecting_quality_score: 52.0, consistency_score: 38.0,
    pipeline_composite: 46.95,
    has_pipeline_gap: true, requires_pipeline_coaching: true,
    estimated_pipeline_shortfall_usd: 1620000.0,
    pipeline_signal: "Territory exhaustion — 4% outreach-to-connect — 0.3 new opps/week — 4 consecutive low-pipeline weeks — composite 47",
  },
  {
    rep_id: "rep_007", region: "APAC",
    pipeline_risk: "critical", pipeline_pattern: "burst_and_fade",
    pipeline_severity: "stalled", recommended_action: "pipeline_reset_intervention",
    generation_rate_score: 70.0, pipeline_volume_score: 65.0,
    prospecting_quality_score: 68.0, consistency_score: 72.0,
    pipeline_composite: 68.35,
    has_pipeline_gap: true, requires_pipeline_coaching: true,
    estimated_pipeline_shortfall_usd: 3240000.0,
    pipeline_signal: "Burst and fade — 3% outreach-to-connect — 0.2 new opps/week — 6 consecutive low-pipeline weeks — composite 68",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    pipeline_risk: "critical", pipeline_pattern: "burst_and_fade",
    pipeline_severity: "stalled", recommended_action: "pipeline_reset_intervention",
    generation_rate_score: 100.0, pipeline_volume_score: 100.0,
    prospecting_quality_score: 100.0, consistency_score: 100.0,
    pipeline_composite: 100.0,
    has_pipeline_gap: true, requires_pipeline_coaching: true,
    estimated_pipeline_shortfall_usd: 5333000.0,
    pipeline_signal: "Burst and fade — 3% outreach-to-connect — 0.2 new opps/week — 8 consecutive low-pipeline weeks — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-pipeline-generation-velocity-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.pipeline_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.pipeline_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_gr = 0, total_pv = 0, total_pq = 0, total_cs = 0, total_short = 0;

  for (const r of mockReps) {
    risk_counts[r.pipeline_risk]         = (risk_counts[r.pipeline_risk] || 0) + 1;
    pattern_counts[r.pipeline_pattern]   = (pattern_counts[r.pipeline_pattern] || 0) + 1;
    severity_counts[r.pipeline_severity] = (severity_counts[r.pipeline_severity] || 0) + 1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action] || 0) + 1;
    total_comp  += r.pipeline_composite;
    total_gr    += r.generation_rate_score;
    total_pv    += r.pipeline_volume_score;
    total_pq    += r.prospecting_quality_score;
    total_cs    += r.consistency_score;
    total_short += r.estimated_pipeline_shortfall_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                       n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_pipeline_composite:                      Math.round((total_comp / n) * 10) / 10,
      pipeline_gap_count:                          mockReps.filter((r) => r.has_pipeline_gap).length,
      coaching_count:                              mockReps.filter((r) => r.requires_pipeline_coaching).length,
      avg_generation_rate_score:                   Math.round((total_gr / n) * 10) / 10,
      avg_pipeline_volume_score:                   Math.round((total_pv / n) * 10) / 10,
      avg_prospecting_quality_score:               Math.round((total_pq / n) * 10) / 10,
      avg_consistency_score:                       Math.round((total_cs / n) * 10) / 10,
      total_estimated_pipeline_shortfall_usd:      Math.round(total_short * 100) / 100,
    },
  });
}
