import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    crm_adoption_risk: "low", crm_adoption_pattern: "none",
    crm_adoption_severity: "compliant", recommended_action: "no_action",
    data_freshness_score: 0.0, data_completeness_score: 0.0,
    activity_logging_score: 0.0, forecast_data_quality_score: 0.0,
    crm_adoption_composite: 0.0,
    has_crm_gap: false, requires_crm_coaching: false,
    estimated_forecast_risk_usd: 0.0,
    crm_adoption_signal: "CRM adoption healthy — data freshness, completeness, and activity logging within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    crm_adoption_risk: "low", crm_adoption_pattern: "none",
    crm_adoption_severity: "compliant", recommended_action: "no_action",
    data_freshness_score: 2.0, data_completeness_score: 4.0,
    activity_logging_score: 3.0, forecast_data_quality_score: 2.0,
    crm_adoption_composite: 2.8,
    has_crm_gap: false, requires_crm_coaching: false,
    estimated_forecast_risk_usd: 0.0,
    crm_adoption_signal: "CRM adoption healthy — data freshness, completeness, and activity logging within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    crm_adoption_risk: "moderate", crm_adoption_pattern: "lazy_entry",
    crm_adoption_severity: "developing", recommended_action: "crm_coaching",
    data_freshness_score: 25.0, data_completeness_score: 12.0,
    activity_logging_score: 18.0, forecast_data_quality_score: 15.0,
    crm_adoption_composite: 18.3,
    has_crm_gap: false, requires_crm_coaching: false,
    estimated_forecast_risk_usd: 8550.0,
    crm_adoption_signal: "Lazy entry — 5.0d avg update lag — 75% fields complete — 1.8 logs/deal/wk — composite 18",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    crm_adoption_risk: "moderate", crm_adoption_pattern: "activity_logging_gap",
    crm_adoption_severity: "developing", recommended_action: "crm_coaching",
    data_freshness_score: 18.0, data_completeness_score: 20.0,
    activity_logging_score: 38.0, forecast_data_quality_score: 12.0,
    crm_adoption_composite: 23.0,
    has_crm_gap: false, requires_crm_coaching: true,
    estimated_forecast_risk_usd: 13680.0,
    crm_adoption_signal: "Activity logging gap — 6.0d avg update lag — 68% fields complete — 0.8 logs/deal/wk — composite 23",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    crm_adoption_risk: "high", crm_adoption_pattern: "incomplete_records",
    crm_adoption_severity: "neglected", recommended_action: "data_cleanup_session",
    data_freshness_score: 30.0, data_completeness_score: 48.0,
    activity_logging_score: 35.0, forecast_data_quality_score: 28.0,
    crm_adoption_composite: 36.2,
    has_crm_gap: true, requires_crm_coaching: true,
    estimated_forecast_risk_usd: 42750.0,
    crm_adoption_signal: "Incomplete records — 9.0d avg update lag — 52% fields complete — 0.5 logs/deal/wk — composite 36",
  },
  {
    rep_id: "rep_006", region: "West",
    crm_adoption_risk: "high", crm_adoption_pattern: "stale_data",
    crm_adoption_severity: "neglected", recommended_action: "crm_coaching",
    data_freshness_score: 55.0, data_completeness_score: 32.0,
    activity_logging_score: 28.0, forecast_data_quality_score: 35.0,
    crm_adoption_composite: 39.95,
    has_crm_gap: true, requires_crm_coaching: true,
    estimated_forecast_risk_usd: 57000.0,
    crm_adoption_signal: "Stale data — 12.0d avg update lag — 55% fields complete — 0.6 logs/deal/wk — composite 40",
  },
  {
    rep_id: "rep_007", region: "APAC",
    crm_adoption_risk: "critical", crm_adoption_pattern: "stale_data",
    crm_adoption_severity: "abandoned", recommended_action: "data_cleanup_session",
    data_freshness_score: 78.0, data_completeness_score: 65.0,
    activity_logging_score: 72.0, forecast_data_quality_score: 60.0,
    crm_adoption_composite: 70.05,
    has_crm_gap: true, requires_crm_coaching: true,
    estimated_forecast_risk_usd: 85500.0,
    crm_adoption_signal: "Stale data — 16.0d avg update lag — 38% fields complete — 0.3 logs/deal/wk — composite 70",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    crm_adoption_risk: "critical", crm_adoption_pattern: "stale_data",
    crm_adoption_severity: "abandoned", recommended_action: "crm_adoption_program",
    data_freshness_score: 100.0, data_completeness_score: 100.0,
    activity_logging_score: 100.0, forecast_data_quality_score: 100.0,
    crm_adoption_composite: 100.0,
    has_crm_gap: true, requires_crm_coaching: true,
    estimated_forecast_risk_usd: 102600.0,
    crm_adoption_signal: "Stale data — 18.0d avg update lag — 38% fields complete — 0.4 logs/deal/wk — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-crm-adoption-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.crm_adoption_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.crm_adoption_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_fr = 0, total_co = 0, total_ac = 0, total_fo = 0, total_impact = 0;

  for (const r of mockReps) {
    risk_counts[r.crm_adoption_risk]       = (risk_counts[r.crm_adoption_risk] || 0) + 1;
    pattern_counts[r.crm_adoption_pattern] = (pattern_counts[r.crm_adoption_pattern] || 0) + 1;
    severity_counts[r.crm_adoption_severity] = (severity_counts[r.crm_adoption_severity] || 0) + 1;
    action_counts[r.recommended_action]    = (action_counts[r.recommended_action] || 0) + 1;
    total_comp   += r.crm_adoption_composite;
    total_fr     += r.data_freshness_score;
    total_co     += r.data_completeness_score;
    total_ac     += r.activity_logging_score;
    total_fo     += r.forecast_data_quality_score;
    total_impact += r.estimated_forecast_risk_usd;
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
      avg_crm_adoption_composite:               Math.round((total_comp / n) * 10) / 10,
      crm_gap_count:                            mockReps.filter((r) => r.has_crm_gap).length,
      coaching_count:                           mockReps.filter((r) => r.requires_crm_coaching).length,
      avg_data_freshness_score:                 Math.round((total_fr / n) * 10) / 10,
      avg_data_completeness_score:              Math.round((total_co / n) * 10) / 10,
      avg_activity_logging_score:               Math.round((total_ac / n) * 10) / 10,
      avg_forecast_data_quality_score:          Math.round((total_fo / n) * 10) / 10,
      total_estimated_forecast_risk_usd:        Math.round(total_impact * 100) / 100,
    },
  });
}
