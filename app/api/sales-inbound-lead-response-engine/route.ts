import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    lead_response_risk: "low", lead_response_pattern: "none",
    lead_response_severity: "responsive", recommended_action: "no_action",
    response_speed_score: 0.0, qualification_quality_score: 0.0,
    lead_conversion_score: 0.0, lead_discipline_score: 0.0,
    lead_response_composite: 0.0, has_response_gap: false,
    requires_lead_coaching: false, estimated_lost_pipeline_usd: 0.0,
    lead_response_signal: "Inbound lead response rate and quality within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    lead_response_risk: "low", lead_response_pattern: "none",
    lead_response_severity: "responsive", recommended_action: "no_action",
    response_speed_score: 5.0, qualification_quality_score: 8.0,
    lead_conversion_score: 5.0, lead_discipline_score: 0.0,
    lead_response_composite: 5.0, has_response_gap: false,
    requires_lead_coaching: false, estimated_lost_pipeline_usd: 0.0,
    lead_response_signal: "Inbound lead response rate and quality within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    lead_response_risk: "moderate", lead_response_pattern: "poor_qualification",
    lead_response_severity: "delayed", recommended_action: "response_time_coaching",
    response_speed_score: 18.0, qualification_quality_score: 30.0,
    lead_conversion_score: 18.0, lead_discipline_score: 15.0,
    lead_response_composite: 21.0, has_response_gap: false,
    requires_lead_coaching: true, estimated_lost_pipeline_usd: 6000.0,
    lead_response_signal: "Poor qualification — 2 leads never contacted — 6h avg response time — composite 21",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    lead_response_risk: "moderate", lead_response_pattern: "slow_response",
    lead_response_severity: "delayed", recommended_action: "response_time_coaching",
    response_speed_score: 35.0, qualification_quality_score: 15.0,
    lead_conversion_score: 18.0, lead_discipline_score: 10.0,
    lead_response_composite: 21.0, has_response_gap: true,
    requires_lead_coaching: false, estimated_lost_pipeline_usd: 9000.0,
    lead_response_signal: "Slow response — 3 leads never contacted — 14h avg response time — composite 21",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    lead_response_risk: "high", lead_response_pattern: "icp_miss",
    lead_response_severity: "lagging", recommended_action: "lead_prioritization",
    response_speed_score: 25.0, qualification_quality_score: 35.0,
    lead_conversion_score: 42.0, lead_discipline_score: 20.0,
    lead_response_composite: 31.0, has_response_gap: false,
    requires_lead_coaching: true, estimated_lost_pipeline_usd: 36000.0,
    lead_response_signal: "Icp miss — 4 leads never contacted — 18h avg response time — composite 31",
  },
  {
    rep_id: "rep_006", region: "West",
    lead_response_risk: "high", lead_response_pattern: "lead_neglect",
    lead_response_severity: "lagging", recommended_action: "crm_discipline",
    response_speed_score: 35.0, qualification_quality_score: 28.0,
    lead_conversion_score: 38.0, lead_discipline_score: 48.0,
    lead_response_composite: 37.0, has_response_gap: true,
    requires_lead_coaching: true, estimated_lost_pipeline_usd: 60000.0,
    lead_response_signal: "Lead neglect — 6 leads never contacted — 22h avg response time — 2 lost to competitor — composite 37",
  },
  {
    rep_id: "rep_007", region: "APAC",
    lead_response_risk: "critical", lead_response_pattern: "slow_response",
    lead_response_severity: "critical", recommended_action: "response_time_coaching",
    response_speed_score: 65.0, qualification_quality_score: 55.0,
    lead_conversion_score: 58.0, lead_discipline_score: 50.0,
    lead_response_composite: 58.0, has_response_gap: true,
    requires_lead_coaching: true, estimated_lost_pipeline_usd: 150000.0,
    lead_response_signal: "Slow response — 10 leads never contacted — 36h avg response time — 4 lost to competitor — composite 58",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    lead_response_risk: "critical", lead_response_pattern: "lead_neglect",
    lead_response_severity: "critical", recommended_action: "lead_cadence_reset",
    response_speed_score: 70.0, qualification_quality_score: 65.0,
    lead_conversion_score: 65.0, lead_discipline_score: 72.0,
    lead_response_composite: 68.0, has_response_gap: true,
    requires_lead_coaching: true, estimated_lost_pipeline_usd: 280000.0,
    lead_response_signal: "Lead neglect — 15 leads never contacted — 48h avg response time — 6 lost to competitor — composite 68",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-inbound-lead-response-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.lead_response_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.lead_response_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_sp = 0, total_qu = 0, total_co = 0, total_di = 0, total_lost = 0;

  for (const r of mockReps) {
    risk_counts[r.lead_response_risk]         = (risk_counts[r.lead_response_risk] || 0) + 1;
    pattern_counts[r.lead_response_pattern]   = (pattern_counts[r.lead_response_pattern] || 0) + 1;
    severity_counts[r.lead_response_severity] = (severity_counts[r.lead_response_severity] || 0) + 1;
    action_counts[r.recommended_action]       = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.lead_response_composite;
    total_sp   += r.response_speed_score;
    total_qu   += r.qualification_quality_score;
    total_co   += r.lead_conversion_score;
    total_di   += r.lead_discipline_score;
    total_lost += r.estimated_lost_pipeline_usd;
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
      avg_lead_response_composite:          Math.round((total_comp / n) * 10) / 10,
      response_gap_count:                   mockReps.filter((r) => r.has_response_gap).length,
      lead_coaching_count:                  mockReps.filter((r) => r.requires_lead_coaching).length,
      avg_response_speed_score:             Math.round((total_sp / n) * 10) / 10,
      avg_qualification_quality_score:      Math.round((total_qu / n) * 10) / 10,
      avg_lead_conversion_score:            Math.round((total_co / n) * 10) / 10,
      avg_lead_discipline_score:            Math.round((total_di / n) * 10) / 10,
      total_estimated_lost_pipeline_usd:    Math.round(total_lost * 100) / 100,
    },
  });
}
