import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-forecast-sanity-check-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    forecast_risk: "low", forecast_pattern: "none",
    forecast_severity: "accurate", recommended_action: "no_action",
    overforecast_bias_score: 0.0, pipeline_quality_score: 0.0,
    stage_integrity_score: 0.0, history_alignment_score: 0.0,
    forecast_sanity_composite: 0.0,
    has_forecast_gap: false, requires_forecast_review: false,
    estimated_forecast_variance_usd: 0.0,
    forecast_signal: "Forecast accuracy healthy — historical alignment and pipeline quality within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    forecast_risk: "low", forecast_pattern: "none",
    forecast_severity: "accurate", recommended_action: "no_action",
    overforecast_bias_score: 3.0, pipeline_quality_score: 5.0,
    stage_integrity_score: 4.0, history_alignment_score: 2.0,
    forecast_sanity_composite: 3.65,
    has_forecast_gap: false, requires_forecast_review: false,
    estimated_forecast_variance_usd: 0.0,
    forecast_signal: "Forecast accuracy healthy — historical alignment and pipeline quality within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    forecast_risk: "moderate", forecast_pattern: "sandbag_bias",
    forecast_severity: "drifting", recommended_action: "forecast_review_coaching",
    overforecast_bias_score: 12.0, pipeline_quality_score: 20.0,
    stage_integrity_score: 18.0, history_alignment_score: 14.0,
    forecast_sanity_composite: 16.7,
    has_forecast_gap: false, requires_forecast_review: false,
    estimated_forecast_variance_usd: 18350.0,
    forecast_signal: "Sandbag bias — 72% of expected attainment — 1 manual overrides — 12% close dates pushed — composite 17",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    forecast_risk: "moderate", forecast_pattern: "stage_inflation",
    forecast_severity: "drifting", recommended_action: "forecast_review_coaching",
    overforecast_bias_score: 20.0, pipeline_quality_score: 22.0,
    stage_integrity_score: 28.0, history_alignment_score: 15.0,
    forecast_sanity_composite: 21.95,
    has_forecast_gap: false, requires_forecast_review: true,
    estimated_forecast_variance_usd: 35250.0,
    forecast_signal: "Stage inflation — 115% of expected attainment — 2 manual overrides — 18% close dates pushed — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    forecast_risk: "high", forecast_pattern: "history_disconnect",
    forecast_severity: "unreliable", recommended_action: "historical_recalibration",
    overforecast_bias_score: 35.0, pipeline_quality_score: 38.0,
    stage_integrity_score: 32.0, history_alignment_score: 40.0,
    forecast_sanity_composite: 36.3,
    has_forecast_gap: true, requires_forecast_review: true,
    estimated_forecast_variance_usd: 87500.0,
    forecast_signal: "History disconnect — 138% of expected attainment — 4 manual overrides — 28% close dates pushed — composite 36",
  },
  {
    rep_id: "rep_006", region: "West",
    forecast_risk: "high", forecast_pattern: "late_quarter_stuffing",
    forecast_severity: "unreliable", recommended_action: "pipeline_validation_session",
    overforecast_bias_score: 45.0, pipeline_quality_score: 40.0,
    stage_integrity_score: 38.0, history_alignment_score: 30.0,
    forecast_sanity_composite: 39.7,
    has_forecast_gap: true, requires_forecast_review: true,
    estimated_forecast_variance_usd: 125400.0,
    forecast_signal: "Late quarter stuffing — 145% of expected attainment — 4 manual overrides — 32% close dates pushed — composite 40",
  },
  {
    rep_id: "rep_007", region: "APAC",
    forecast_risk: "critical", forecast_pattern: "overforecast_bias",
    forecast_severity: "distorted", recommended_action: "forecast_override_intervention",
    overforecast_bias_score: 70.0, pipeline_quality_score: 65.0,
    stage_integrity_score: 60.0, history_alignment_score: 55.0,
    forecast_sanity_composite: 63.75,
    has_forecast_gap: true, requires_forecast_review: true,
    estimated_forecast_variance_usd: 246000.0,
    forecast_signal: "Overforecast bias — 158% of expected attainment — 6 manual overrides — 38% close dates pushed — composite 64",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    forecast_risk: "critical", forecast_pattern: "overforecast_bias",
    forecast_severity: "distorted", recommended_action: "deal_stage_audit",
    overforecast_bias_score: 85.0, pipeline_quality_score: 80.0,
    stage_integrity_score: 75.0, history_alignment_score: 70.0,
    forecast_sanity_composite: 79.25,
    has_forecast_gap: true, requires_forecast_review: true,
    estimated_forecast_variance_usd: 323000.0,
    forecast_signal: "Overforecast bias — 167% of expected attainment — 5 manual overrides — 40% close dates pushed — composite 95",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-forecast-sanity-check-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.forecast_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.forecast_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_over = 0, total_pipe = 0, total_stage = 0, total_hist = 0, total_var = 0;

  for (const r of mockReps) {
    risk_counts[r.forecast_risk]       = (risk_counts[r.forecast_risk] || 0) + 1;
    pattern_counts[r.forecast_pattern] = (pattern_counts[r.forecast_pattern] || 0) + 1;
    severity_counts[r.forecast_severity] = (severity_counts[r.forecast_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp  += r.forecast_sanity_composite;
    total_over  += r.overforecast_bias_score;
    total_pipe  += r.pipeline_quality_score;
    total_stage += r.stage_integrity_score;
    total_hist  += r.history_alignment_score;
    total_var   += r.estimated_forecast_variance_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_forecast_sanity_composite:            Math.round((total_comp / n) * 10) / 10,
      forecast_gap_count:                       mockReps.filter((r) => r.has_forecast_gap).length,
      review_required_count:                    mockReps.filter((r) => r.requires_forecast_review).length,
      avg_overforecast_bias_score:              Math.round((total_over / n) * 10) / 10,
      avg_pipeline_quality_score:               Math.round((total_pipe / n) * 10) / 10,
      avg_stage_integrity_score:                Math.round((total_stage / n) * 10) / 10,
      avg_history_alignment_score:              Math.round((total_hist / n) * 10) / 10,
      total_estimated_forecast_variance_usd:    Math.round(total_var * 100) / 100,
    },
  }));
}
