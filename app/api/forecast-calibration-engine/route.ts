import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", rep_name: "Alice Martin", region: "NAMER", quarter: "Q2-2026",
    calibration_rating: "excellent", calibration_risk: "low",
    bias_type: "accurate", calibration_action: "no_action",
    accuracy_score: 92.0, bias_score: 12.0, consistency_score: 88.0, data_quality_score: 90.0,
    calibration_composite: 90.8, is_sandbagging: false, is_over_optimistic: false,
    estimated_forecast_error_usd: 45000.0,
    calibration_signal: "forecast accuracy 88% (4Q avg)",
    forecasted_amount_usd: 500000.0,
  },
  {
    rep_id: "rep_002", rep_name: "Bruno Silva", region: "EMEA", quarter: "Q2-2026",
    calibration_rating: "poor", calibration_risk: "critical",
    bias_type: "over_optimistic", calibration_action: "system_override",
    accuracy_score: 8.0, bias_score: 78.0, consistency_score: 15.0, data_quality_score: 22.0,
    calibration_composite: 16.5, is_sandbagging: false, is_over_optimistic: true,
    estimated_forecast_error_usd: 665000.0,
    calibration_signal: "over-optimistic — missed forecast by $400,000; close date pushes: 6",
    forecasted_amount_usd: 800000.0,
  },
  {
    rep_id: "rep_003", rep_name: "Clara Nguyen", region: "APAC", quarter: "Q2-2026",
    calibration_rating: "excellent", calibration_risk: "low",
    bias_type: "accurate", calibration_action: "no_action",
    accuracy_score: 95.0, bias_score: 8.0, consistency_score: 92.0, data_quality_score: 88.0,
    calibration_composite: 93.3, is_sandbagging: false, is_over_optimistic: false,
    estimated_forecast_error_usd: 23000.0,
    calibration_signal: "forecast accuracy 94% (4Q avg)",
    forecasted_amount_usd: 350000.0,
  },
  {
    rep_id: "rep_004", rep_name: "Diego Ferreira", region: "LATAM", quarter: "Q2-2026",
    calibration_rating: "fair", calibration_risk: "high",
    bias_type: "sandbagging", calibration_action: "forecast_adjustment",
    accuracy_score: 42.0, bias_score: 55.0, consistency_score: 38.0, data_quality_score: 35.0,
    calibration_composite: 38.3, is_sandbagging: true, is_over_optimistic: false,
    estimated_forecast_error_usd: 246000.0,
    calibration_signal: "sandbagging detected — closed 148% of forecast; quota pressure likely",
    forecasted_amount_usd: 400000.0,
  },
  {
    rep_id: "rep_005", rep_name: "Elena Kovacs", region: "EMEA", quarter: "Q2-2026",
    calibration_rating: "good", calibration_risk: "moderate",
    bias_type: "accurate", calibration_action: "coaching_required",
    accuracy_score: 65.0, bias_score: 28.0, consistency_score: 62.0, data_quality_score: 58.0,
    calibration_composite: 62.9, is_sandbagging: false, is_over_optimistic: false,
    estimated_forecast_error_usd: 148000.0,
    calibration_signal: "late stage slippage 28% — deals not closing as forecasted",
    forecasted_amount_usd: 400000.0,
  },
  {
    rep_id: "rep_006", rep_name: "Felix Okafor", region: "NAMER", quarter: "Q2-2026",
    calibration_rating: "poor", calibration_risk: "critical",
    bias_type: "inconsistent", calibration_action: "system_override",
    accuracy_score: 15.0, bias_score: 72.0, consistency_score: 12.0, data_quality_score: 18.0,
    calibration_composite: 18.5, is_sandbagging: false, is_over_optimistic: false,
    estimated_forecast_error_usd: 487000.0,
    calibration_signal: "manager overrode forecast 5x this quarter — rep forecasting untrusted",
    forecasted_amount_usd: 600000.0,
  },
  {
    rep_id: "rep_007", rep_name: "Gabriela Torres", region: "LATAM", quarter: "Q2-2026",
    calibration_rating: "good", calibration_risk: "low",
    bias_type: "accurate", calibration_action: "no_action",
    accuracy_score: 78.0, bias_score: 18.0, consistency_score: 72.0, data_quality_score: 80.0,
    calibration_composite: 75.6, is_sandbagging: false, is_over_optimistic: false,
    estimated_forecast_error_usd: 73000.0,
    calibration_signal: "forecast accuracy 82% (4Q avg)",
    forecasted_amount_usd: 300000.0,
  },
  {
    rep_id: "rep_008", rep_name: "Hiro Tanaka", region: "APAC", quarter: "Q2-2026",
    calibration_rating: "fair", calibration_risk: "moderate",
    bias_type: "over_optimistic", calibration_action: "coaching_required",
    accuracy_score: 38.0, bias_score: 45.0, consistency_score: 42.0, data_quality_score: 48.0,
    calibration_composite: 44.0, is_sandbagging: false, is_over_optimistic: true,
    estimated_forecast_error_usd: 197000.0,
    calibration_signal: "CRM data lag 8 days — forecast accuracy compromised by stale data",
    forecasted_amount_usd: 350000.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const rating = searchParams.get("rating");
  const risk   = searchParams.get("risk");
  const bias   = searchParams.get("bias");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/forecast-calibration-engine`);
      if (rating) url.searchParams.set("rating", rating);
      if (risk)   url.searchParams.set("risk", risk);
      if (bias)   url.searchParams.set("bias", bias);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (rating) reps = reps.filter((r) => r.calibration_rating === rating);
  if (risk)   reps = reps.filter((r) => r.calibration_risk === risk);
  if (bias)   reps = reps.filter((r) => r.bias_type === bias);

  const cal_counts:   Record<string, number> = {};
  const risk_counts:  Record<string, number> = {};
  const bias_counts:  Record<string, number> = {};
  const act_counts:   Record<string, number> = {};
  let total_comp = 0, total_acc = 0, total_bias = 0, total_cons = 0, total_dq = 0, total_err = 0;

  for (const r of mockReps) {
    cal_counts[r.calibration_rating]  = (cal_counts[r.calibration_rating] || 0) + 1;
    risk_counts[r.calibration_risk]   = (risk_counts[r.calibration_risk] || 0) + 1;
    bias_counts[r.bias_type]          = (bias_counts[r.bias_type] || 0) + 1;
    act_counts[r.calibration_action]  = (act_counts[r.calibration_action] || 0) + 1;
    total_comp  += r.calibration_composite;
    total_acc   += r.accuracy_score;
    total_bias  += r.bias_score;
    total_cons  += r.consistency_score;
    total_dq    += r.data_quality_score;
    total_err   += r.estimated_forecast_error_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total: n,
      calibration_counts: cal_counts,
      risk_counts,
      bias_type_counts: bias_counts,
      action_counts: act_counts,
      avg_calibration_composite:    Math.round((total_comp / n) * 10) / 10,
      sandbagging_count:            mockReps.filter((r) => r.is_sandbagging).length,
      over_optimistic_count:        mockReps.filter((r) => r.is_over_optimistic).length,
      avg_accuracy_score:           Math.round((total_acc / n) * 10) / 10,
      avg_bias_score:               Math.round((total_bias / n) * 10) / 10,
      avg_consistency_score:        Math.round((total_cons / n) * 10) / 10,
      avg_data_quality_score:       Math.round((total_dq / n) * 10) / 10,
      total_forecast_error_exposure_usd: Math.round(total_err),
    },
  });
}
