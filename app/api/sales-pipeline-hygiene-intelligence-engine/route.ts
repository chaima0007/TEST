import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-pipeline-hygiene-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    hygiene_risk: "low", hygiene_pattern: "none",
    hygiene_severity: "clean", recommended_action: "no_action",
    data_completeness_score: 0.0, pipeline_freshness_score: 0.0,
    deal_quality_score: 0.0, forecast_reliability_score: 0.0,
    pipeline_hygiene_composite: 0.0,
    has_hygiene_gap: false, requires_hygiene_coaching: false,
    estimated_forecast_error_usd: 0.0,
    hygiene_signal: "Pipeline hygiene and CRM data quality within healthy benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    hygiene_risk: "low", hygiene_pattern: "none",
    hygiene_severity: "clean", recommended_action: "no_action",
    data_completeness_score: 4.0, pipeline_freshness_score: 3.0,
    deal_quality_score: 5.0, forecast_reliability_score: 2.0,
    pipeline_hygiene_composite: 3.6,
    has_hygiene_gap: false, requires_hygiene_coaching: false,
    estimated_forecast_error_usd: 0.0,
    hygiene_signal: "Pipeline hygiene and CRM data quality within healthy benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    hygiene_risk: "moderate", hygiene_pattern: "stale_activity",
    hygiene_severity: "developing", recommended_action: "crm_coaching",
    data_completeness_score: 18.0, pipeline_freshness_score: 25.0,
    deal_quality_score: 12.0, forecast_reliability_score: 10.0,
    pipeline_hygiene_composite: 17.35,
    has_hygiene_gap: false, requires_hygiene_coaching: false,
    estimated_forecast_error_usd: 15200.0,
    hygiene_signal: "Stale activity — 14 days avg since CRM update — 2 zombie deals — composite 17",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    hygiene_risk: "moderate", hygiene_pattern: "incomplete_qualification",
    hygiene_severity: "developing", recommended_action: "crm_coaching",
    data_completeness_score: 22.0, pipeline_freshness_score: 14.0,
    deal_quality_score: 20.0, forecast_reliability_score: 16.0,
    pipeline_hygiene_composite: 18.8,
    has_hygiene_gap: false, requires_hygiene_coaching: false,
    estimated_forecast_error_usd: 22500.0,
    hygiene_signal: "Incomplete qualification — 68% CRM complete — 1 zombie deals — composite 19",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    hygiene_risk: "high", hygiene_pattern: "zombie_pipeline",
    hygiene_severity: "dirty", recommended_action: "pipeline_audit",
    data_completeness_score: 30.0, pipeline_freshness_score: 38.0,
    deal_quality_score: 35.0, forecast_reliability_score: 28.0,
    pipeline_hygiene_composite: 33.35,
    has_hygiene_gap: false, requires_hygiene_coaching: true,
    estimated_forecast_error_usd: 58800.0,
    hygiene_signal: "Zombie pipeline — 55% CRM complete — 4 zombie deals — 3 overdue close dates — composite 33",
  },
  {
    rep_id: "rep_006", region: "West",
    hygiene_risk: "high", hygiene_pattern: "forecast_distortion",
    hygiene_severity: "dirty", recommended_action: "forecast_recalibration",
    data_completeness_score: 28.0, pipeline_freshness_score: 32.0,
    deal_quality_score: 40.0, forecast_reliability_score: 45.0,
    pipeline_hygiene_composite: 35.35,
    has_hygiene_gap: true, requires_hygiene_coaching: true,
    estimated_forecast_error_usd: 84000.0,
    hygiene_signal: "Forecast distortion — 48% CRM complete — 3 zombie deals — 5 overdue close dates — composite 35",
  },
  {
    rep_id: "rep_007", region: "APAC",
    hygiene_risk: "critical", hygiene_pattern: "data_neglect",
    hygiene_severity: "toxic", recommended_action: "data_cleanup_sprint",
    data_completeness_score: 60.0, pipeline_freshness_score: 65.0,
    deal_quality_score: 55.0, forecast_reliability_score: 50.0,
    pipeline_hygiene_composite: 58.25,
    has_hygiene_gap: true, requires_hygiene_coaching: true,
    estimated_forecast_error_usd: 182000.0,
    hygiene_signal: "Data neglect — 38% CRM complete — 6 zombie deals — 8 overdue close dates — composite 58",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    hygiene_risk: "critical", hygiene_pattern: "zombie_pipeline",
    hygiene_severity: "toxic", recommended_action: "pipeline_purge",
    data_completeness_score: 75.0, pipeline_freshness_score: 80.0,
    deal_quality_score: 70.0, forecast_reliability_score: 65.0,
    pipeline_hygiene_composite: 73.25,
    has_hygiene_gap: true, requires_hygiene_coaching: true,
    estimated_forecast_error_usd: 371525.0,
    hygiene_signal: "Zombie pipeline — 42% CRM complete — 5 zombie deals — 6 overdue close dates — composite 73",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-pipeline-hygiene-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.hygiene_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.hygiene_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_comp_score = 0, total_fresh = 0, total_qual = 0, total_rel = 0, total_imp = 0;

  for (const r of mockReps) {
    risk_counts[r.hygiene_risk]         = (risk_counts[r.hygiene_risk] || 0) + 1;
    pattern_counts[r.hygiene_pattern]   = (pattern_counts[r.hygiene_pattern] || 0) + 1;
    severity_counts[r.hygiene_severity] = (severity_counts[r.hygiene_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp       += r.pipeline_hygiene_composite;
    total_comp_score += r.data_completeness_score;
    total_fresh      += r.pipeline_freshness_score;
    total_qual       += r.deal_quality_score;
    total_rel        += r.forecast_reliability_score;
    total_imp        += r.estimated_forecast_error_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                                n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_pipeline_hygiene_composite:       Math.round((total_comp / n) * 10) / 10,
      hygiene_gap_count:                    mockReps.filter((r) => r.has_hygiene_gap).length,
      hygiene_coaching_count:               mockReps.filter((r) => r.requires_hygiene_coaching).length,
      avg_data_completeness_score:          Math.round((total_comp_score / n) * 10) / 10,
      avg_pipeline_freshness_score:         Math.round((total_fresh / n) * 10) / 10,
      avg_deal_quality_score:               Math.round((total_qual / n) * 10) / 10,
      avg_forecast_reliability_score:       Math.round((total_rel / n) * 10) / 10,
      total_estimated_forecast_error_usd:   Math.round(total_imp * 100) / 100,
    },
  }));
}
