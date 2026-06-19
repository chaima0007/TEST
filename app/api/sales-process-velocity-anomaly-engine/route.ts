import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", rep_id: "rep_01",
    velocity_anomaly: "normal", velocity_risk: "low",
    velocity_alert: "none", velocity_severity: "clean",
    stage_completion_score: 5.0, timeline_deviation_score: 3.0,
    forecast_integrity_score: 8.0, pattern_risk_score: 4.0,
    velocity_composite: 5.0, is_anomalous: false, requires_review: false,
    pipeline_days_deviation: 5.0,
    velocity_signal: "deal velocity within normal parameters",
  },
  {
    deal_id: "deal_002", rep_id: "rep_01",
    velocity_anomaly: "suspicious_fast", velocity_risk: "moderate",
    velocity_alert: "flag", velocity_severity: "watch",
    stage_completion_score: 10.0, timeline_deviation_score: 30.0,
    forecast_integrity_score: 12.0, pattern_risk_score: 20.0,
    velocity_composite: 19.9, is_anomalous: false, requires_review: false,
    pipeline_days_deviation: -45.0,
    velocity_signal: "deal closed 55% faster than avg (38 vs 85 days) — composite 20",
  },
  {
    deal_id: "deal_003", rep_id: "rep_02",
    velocity_anomaly: "stage_skipping", velocity_risk: "moderate",
    velocity_alert: "review", velocity_severity: "watch",
    stage_completion_score: 30.0, timeline_deviation_score: 18.0,
    forecast_integrity_score: 15.0, pattern_risk_score: 10.0,
    velocity_composite: 19.6, is_anomalous: false, requires_review: false,
    pipeline_days_deviation: -30.0,
    velocity_signal: "2 stage skip(s) detected — 2/5 stages completed — composite 20",
  },
  {
    deal_id: "deal_004", rep_id: "rep_02",
    velocity_anomaly: "recycled", velocity_risk: "high",
    velocity_alert: "review", velocity_severity: "anomalous",
    stage_completion_score: 42.0, timeline_deviation_score: 28.0,
    forecast_integrity_score: 32.0, pattern_risk_score: 22.0,
    velocity_composite: 32.2, is_anomalous: false, requires_review: true,
    pipeline_days_deviation: 60.0,
    velocity_signal: "deal recycled 3x — instability in qualification — composite 32",
  },
  {
    deal_id: "deal_005", rep_id: "rep_03",
    velocity_anomaly: "forced_close", velocity_risk: "high",
    velocity_alert: "escalate", velocity_severity: "anomalous",
    stage_completion_score: 25.0, timeline_deviation_score: 40.0,
    forecast_integrity_score: 68.0, pattern_risk_score: 15.0,
    velocity_composite: 40.8, is_anomalous: true, requires_review: true,
    pipeline_days_deviation: -20.0,
    velocity_signal: "end-of-period forced close — 4 date changes, 3 category shifts — composite 41",
  },
  {
    deal_id: "deal_006", rep_id: "rep_03",
    velocity_anomaly: "stalled", velocity_risk: "moderate",
    velocity_alert: "flag", velocity_severity: "watch",
    stage_completion_score: 10.0, timeline_deviation_score: 25.0,
    forecast_integrity_score: 15.0, pattern_risk_score: 5.0,
    velocity_composite: 15.5, is_anomalous: false, requires_review: false,
    pipeline_days_deviation: 120.0,
    velocity_signal: "deal stalled — 215 days vs avg 85 — composite 16",
  },
  {
    deal_id: "deal_007", rep_id: "rep_04",
    velocity_anomaly: "suspicious_fast", velocity_risk: "critical",
    velocity_alert: "audit", velocity_severity: "fraud_risk",
    stage_completion_score: 65.0, timeline_deviation_score: 78.0,
    forecast_integrity_score: 48.0, pattern_risk_score: 68.0,
    velocity_composite: 66.4, is_anomalous: true, requires_review: true,
    pipeline_days_deviation: -78.0,
    velocity_signal: "deal closed 92% faster than avg (7 vs 85 days) — composite 66",
  },
  {
    deal_id: "deal_008", rep_id: "rep_04",
    velocity_anomaly: "stage_skipping", velocity_risk: "critical",
    velocity_alert: "audit", velocity_severity: "fraud_risk",
    stage_completion_score: 100.0, timeline_deviation_score: 62.0,
    forecast_integrity_score: 55.0, pattern_risk_score: 45.0,
    velocity_composite: 70.3, is_anomalous: true, requires_review: true,
    pipeline_days_deviation: -70.0,
    velocity_signal: "3 stage skip(s) detected — 1/5 stages completed — composite 70",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const anomaly  = searchParams.get("anomaly");
  const risk     = searchParams.get("risk");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-process-velocity-anomaly-engine`);
      if (anomaly) url.searchParams.set("anomaly", anomaly);
      if (risk)    url.searchParams.set("risk",    risk);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (anomaly) deals = deals.filter((d) => d.velocity_anomaly === anomaly);
  if (risk)    deals = deals.filter((d) => d.velocity_risk    === risk);

  const anomaly_counts:  Record<string, number> = {};
  const risk_counts:     Record<string, number> = {};
  const alert_counts:    Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  let total_comp = 0, total_stage = 0, total_time = 0, total_fore = 0, total_pat = 0, total_dev = 0;

  for (const d of mockDeals) {
    anomaly_counts[d.velocity_anomaly]   = (anomaly_counts[d.velocity_anomaly] || 0) + 1;
    risk_counts[d.velocity_risk]         = (risk_counts[d.velocity_risk] || 0) + 1;
    alert_counts[d.velocity_alert]       = (alert_counts[d.velocity_alert] || 0) + 1;
    severity_counts[d.velocity_severity] = (severity_counts[d.velocity_severity] || 0) + 1;
    total_comp  += d.velocity_composite;
    total_stage += d.stage_completion_score;
    total_time  += d.timeline_deviation_score;
    total_fore  += d.forecast_integrity_score;
    total_pat   += d.pattern_risk_score;
    total_dev   += d.pipeline_days_deviation;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total:                          n,
      anomaly_counts,
      risk_counts,
      alert_counts,
      severity_counts,
      avg_velocity_composite:         Math.round((total_comp  / n) * 10) / 10,
      anomalous_count:                mockDeals.filter((d) => d.is_anomalous).length,
      review_required_count:          mockDeals.filter((d) => d.requires_review).length,
      avg_stage_completion_score:     Math.round((total_stage / n) * 10) / 10,
      avg_timeline_deviation_score:   Math.round((total_time  / n) * 10) / 10,
      avg_forecast_integrity_score:   Math.round((total_fore  / n) * 10) / 10,
      avg_pattern_risk_score:         Math.round((total_pat   / n) * 10) / 10,
      avg_pipeline_days_deviation:    Math.round((total_dev   / n) * 10) / 10,
    },
  });
}
