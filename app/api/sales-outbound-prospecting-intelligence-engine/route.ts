import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    prospecting_risk: "low", prospecting_pattern: "none",
    prospecting_severity: "active", recommended_action: "no_action",
    activity_volume_score: 0.0, targeting_quality_score: 0.0,
    conversion_effectiveness_score: 0.0, pipeline_contribution_score: 0.0,
    prospecting_effectiveness_composite: 0.0,
    has_prospecting_gap: false, requires_prospecting_coaching: false,
    estimated_pipeline_shortfall_usd: 0.0,
    prospecting_signal: "Outbound prospecting activity and pipeline contribution on track",
  },
  {
    rep_id: "rep_002", region: "East",
    prospecting_risk: "low", prospecting_pattern: "none",
    prospecting_severity: "active", recommended_action: "no_action",
    activity_volume_score: 5.0, targeting_quality_score: 5.0,
    conversion_effectiveness_score: 0.0, pipeline_contribution_score: 8.0,
    prospecting_effectiveness_composite: 4.6,
    has_prospecting_gap: false, requires_prospecting_coaching: false,
    estimated_pipeline_shortfall_usd: 0.0,
    prospecting_signal: "Outbound prospecting activity and pipeline contribution on track",
  },
  {
    rep_id: "rep_003", region: "Central",
    prospecting_risk: "moderate", prospecting_pattern: "pipeline_stall",
    prospecting_severity: "developing", recommended_action: "activity_coaching",
    activity_volume_score: 20.0, targeting_quality_score: 15.0,
    conversion_effectiveness_score: 30.0, pipeline_contribution_score: 30.0,
    prospecting_effectiveness_composite: 24.25,
    has_prospecting_gap: false, requires_prospecting_coaching: false,
    estimated_pipeline_shortfall_usd: 11250.0,
    prospecting_signal: "Pipeline stall — 90 total attempts — 8% connect rate — 4 discovery calls booked — composite 24",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    prospecting_risk: "moderate", prospecting_pattern: "poor_targeting",
    prospecting_severity: "developing", recommended_action: "activity_coaching",
    activity_volume_score: 10.0, targeting_quality_score: 30.0,
    conversion_effectiveness_score: 25.0, pipeline_contribution_score: 20.0,
    prospecting_effectiveness_composite: 21.75,
    has_prospecting_gap: false, requires_prospecting_coaching: true,
    estimated_pipeline_shortfall_usd: 9500.0,
    prospecting_signal: "Poor targeting — 120 total attempts — 9% connect rate — 5 discovery calls booked — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    prospecting_risk: "high", prospecting_pattern: "low_connect_rate",
    prospecting_severity: "lagging", recommended_action: "messaging_optimization",
    activity_volume_score: 20.0, targeting_quality_score: 28.0,
    conversion_effectiveness_score: 45.0, pipeline_contribution_score: 35.0,
    prospecting_effectiveness_composite: 33.45,
    has_prospecting_gap: true, requires_prospecting_coaching: true,
    estimated_pipeline_shortfall_usd: 24000.0,
    prospecting_signal: "Low connect rate — 85 total attempts — 4% connect rate — 3 discovery calls booked — composite 33",
  },
  {
    rep_id: "rep_006", region: "West",
    prospecting_risk: "high", prospecting_pattern: "low_activity",
    prospecting_severity: "lagging", recommended_action: "activity_coaching",
    activity_volume_score: 50.0, targeting_quality_score: 25.0,
    conversion_effectiveness_score: 30.0, pipeline_contribution_score: 38.0,
    prospecting_effectiveness_composite: 36.1,
    has_prospecting_gap: true, requires_prospecting_coaching: true,
    estimated_pipeline_shortfall_usd: 36000.0,
    prospecting_signal: "Low activity — 45 total attempts — 7% connect rate — 2 discovery calls booked — composite 36",
  },
  {
    rep_id: "rep_007", region: "APAC",
    prospecting_risk: "critical", prospecting_pattern: "low_activity",
    prospecting_severity: "stalled", recommended_action: "cadence_redesign",
    activity_volume_score: 70.0, targeting_quality_score: 55.0,
    conversion_effectiveness_score: 55.0, pipeline_contribution_score: 60.0,
    prospecting_effectiveness_composite: 59.75,
    has_prospecting_gap: true, requires_prospecting_coaching: true,
    estimated_pipeline_shortfall_usd: 72000.0,
    prospecting_signal: "Low activity — 28 total attempts — 3% connect rate — 1 discovery calls booked — composite 60",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    prospecting_risk: "critical", prospecting_pattern: "poor_targeting",
    prospecting_severity: "stalled", recommended_action: "targeting_calibration",
    activity_volume_score: 65.0, targeting_quality_score: 70.0,
    conversion_effectiveness_score: 65.0, pipeline_contribution_score: 68.0,
    prospecting_effectiveness_composite: 67.2,
    has_prospecting_gap: true, requires_prospecting_coaching: true,
    estimated_pipeline_shortfall_usd: 110000.0,
    prospecting_signal: "Poor targeting — 35 total attempts — 2% connect rate — 0 discovery calls booked — composite 67",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-outbound-prospecting-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.prospecting_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.prospecting_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_vol = 0, total_tgt = 0, total_conv = 0, total_pipe = 0, total_short = 0;

  for (const r of mockReps) {
    risk_counts[r.prospecting_risk]       = (risk_counts[r.prospecting_risk] || 0) + 1;
    pattern_counts[r.prospecting_pattern] = (pattern_counts[r.prospecting_pattern] || 0) + 1;
    severity_counts[r.prospecting_severity] = (severity_counts[r.prospecting_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp  += r.prospecting_effectiveness_composite;
    total_vol   += r.activity_volume_score;
    total_tgt   += r.targeting_quality_score;
    total_conv  += r.conversion_effectiveness_score;
    total_pipe  += r.pipeline_contribution_score;
    total_short += r.estimated_pipeline_shortfall_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_prospecting_effectiveness_composite:  Math.round((total_comp / n) * 10) / 10,
      prospecting_gap_count:                    mockReps.filter((r) => r.has_prospecting_gap).length,
      prospecting_coaching_count:               mockReps.filter((r) => r.requires_prospecting_coaching).length,
      avg_activity_volume_score:                Math.round((total_vol / n) * 10) / 10,
      avg_targeting_quality_score:              Math.round((total_tgt / n) * 10) / 10,
      avg_conversion_effectiveness_score:       Math.round((total_conv / n) * 10) / 10,
      avg_pipeline_contribution_score:          Math.round((total_pipe / n) * 10) / 10,
      total_estimated_pipeline_shortfall_usd:   Math.round(total_short * 100) / 100,
    },
  });
}
