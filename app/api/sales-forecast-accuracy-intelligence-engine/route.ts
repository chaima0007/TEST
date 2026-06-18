import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    forecast_risk: "low", forecast_pattern: "none",
    forecast_severity: "reliable", recommended_action: "no_action",
    forecast_accuracy_score: 0.0, forecast_discipline_score: 0.0,
    pipeline_health_score: 0.0, crm_hygiene_score: 0.0,
    forecast_effectiveness_composite: 0.0, is_forecast_unreliable: false,
    requires_pipeline_inspection: false, estimated_revenue_variance_usd: 0.0,
    forecast_signal: "Forecast accuracy within acceptable benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    forecast_risk: "low", forecast_pattern: "none",
    forecast_severity: "reliable", recommended_action: "no_action",
    forecast_accuracy_score: 5.0, forecast_discipline_score: 8.0,
    pipeline_health_score: 5.0, crm_hygiene_score: 0.0,
    forecast_effectiveness_composite: 5.0, is_forecast_unreliable: false,
    requires_pipeline_inspection: false, estimated_revenue_variance_usd: 0.0,
    forecast_signal: "Forecast accuracy within acceptable benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    forecast_risk: "moderate", forecast_pattern: "stage_manipulation",
    forecast_severity: "variable", recommended_action: "forecast_recalibration",
    forecast_accuracy_score: 25.0, forecast_discipline_score: 30.0,
    pipeline_health_score: 18.0, crm_hygiene_score: 10.0,
    forecast_effectiveness_composite: 22.0, is_forecast_unreliable: false,
    requires_pipeline_inspection: true, estimated_revenue_variance_usd: 5500.0,
    forecast_signal: "Stage manipulation — 2 late-stage slippages — 1 unforecast closes — composite 22",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    forecast_risk: "moderate", forecast_pattern: "crm_neglect",
    forecast_severity: "variable", recommended_action: "forecast_recalibration",
    forecast_accuracy_score: 12.0, forecast_discipline_score: 20.0,
    pipeline_health_score: 25.0, crm_hygiene_score: 35.0,
    forecast_effectiveness_composite: 21.0, is_forecast_unreliable: false,
    requires_pipeline_inspection: true, estimated_revenue_variance_usd: 7200.0,
    forecast_signal: "Crm neglect — 1 sandbagged deals — composite 21",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    forecast_risk: "high", forecast_pattern: "systematic_overforecast",
    forecast_severity: "unreliable", recommended_action: "pipeline_inspection",
    forecast_accuracy_score: 45.0, forecast_discipline_score: 30.0,
    pipeline_health_score: 28.0, crm_hygiene_score: 20.0,
    forecast_effectiveness_composite: 33.0, is_forecast_unreliable: false,
    requires_pipeline_inspection: true, estimated_revenue_variance_usd: 28000.0,
    forecast_signal: "Systematic overforecast — 3 over-forecasted deals — 2 late-stage slippages — composite 33",
  },
  {
    rep_id: "rep_006", region: "West",
    forecast_risk: "high", forecast_pattern: "pipeline_gap",
    forecast_severity: "unreliable", recommended_action: "pipeline_inspection",
    forecast_accuracy_score: 35.0, forecast_discipline_score: 40.0,
    pipeline_health_score: 45.0, crm_hygiene_score: 25.0,
    forecast_effectiveness_composite: 37.0, is_forecast_unreliable: false,
    requires_pipeline_inspection: true, estimated_revenue_variance_usd: 45000.0,
    forecast_signal: "Pipeline gap — 3 over-forecasted deals — 3 late-stage slippages — composite 37",
  },
  {
    rep_id: "rep_007", region: "APAC",
    forecast_risk: "critical", forecast_pattern: "systematic_overforecast",
    forecast_severity: "chaotic", recommended_action: "forecast_override",
    forecast_accuracy_score: 65.0, forecast_discipline_score: 55.0,
    pipeline_health_score: 50.0, crm_hygiene_score: 40.0,
    forecast_effectiveness_composite: 55.0, is_forecast_unreliable: true,
    requires_pipeline_inspection: true, estimated_revenue_variance_usd: 120000.0,
    forecast_signal: "Systematic overforecast — 5 over-forecasted deals — 4 late-stage slippages — 2 sandbagged deals — composite 55",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    forecast_risk: "critical", forecast_pattern: "sandbag_behavior",
    forecast_severity: "chaotic", recommended_action: "forecast_review_cadence",
    forecast_accuracy_score: 70.0, forecast_discipline_score: 65.0,
    pipeline_health_score: 60.0, crm_hygiene_score: 70.0,
    forecast_effectiveness_composite: 67.0, is_forecast_unreliable: true,
    requires_pipeline_inspection: true, estimated_revenue_variance_usd: 210000.0,
    forecast_signal: "Sandbag behavior — 6 over-forecasted deals — 5 late-stage slippages — 4 sandbagged deals — composite 67",
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
  let total_comp = 0, total_acc = 0, total_disc = 0, total_pipe = 0, total_crm = 0, total_var = 0;

  for (const r of mockReps) {
    risk_counts[r.forecast_risk]       = (risk_counts[r.forecast_risk] || 0) + 1;
    pattern_counts[r.forecast_pattern] = (pattern_counts[r.forecast_pattern] || 0) + 1;
    severity_counts[r.forecast_severity] = (severity_counts[r.forecast_severity] || 0) + 1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.forecast_effectiveness_composite;
    total_acc  += r.forecast_accuracy_score;
    total_disc += r.forecast_discipline_score;
    total_pipe += r.pipeline_health_score;
    total_crm  += r.crm_hygiene_score;
    total_var  += r.estimated_revenue_variance_usd;
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
      avg_forecast_effectiveness_composite: Math.round((total_comp / n) * 10) / 10,
      unreliable_forecast_count:            mockReps.filter((r) => r.is_forecast_unreliable).length,
      pipeline_inspection_count:            mockReps.filter((r) => r.requires_pipeline_inspection).length,
      avg_forecast_accuracy_score:          Math.round((total_acc / n) * 10) / 10,
      avg_forecast_discipline_score:        Math.round((total_disc / n) * 10) / 10,
      avg_pipeline_health_score:            Math.round((total_pipe / n) * 10) / 10,
      avg_crm_hygiene_score:                Math.round((total_crm / n) * 10) / 10,
      total_estimated_revenue_variance_usd: Math.round(total_var * 100) / 100,
    },
  });
}
