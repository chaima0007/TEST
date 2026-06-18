import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    burnout_risk: "low", attrition_pattern: "none",
    burnout_severity: "healthy", recommended_action: "no_action",
    workload_strain_score: 0.0, engagement_decay_score: 0.0,
    quota_pressure_score: 0.0, flight_signal_score: 0.0,
    burnout_composite: 0.0, is_burnout_risk: false, is_flight_risk: false,
    estimated_replacement_cost_usd: 0.0,
    burnout_signal: "Rep burnout indicators within healthy range",
  },
  {
    rep_id: "rep_002", region: "East",
    burnout_risk: "low", attrition_pattern: "workload_exhaustion",
    burnout_severity: "healthy", recommended_action: "no_action",
    workload_strain_score: 12.0, engagement_decay_score: 6.0,
    quota_pressure_score: 8.0, flight_signal_score: 4.0,
    burnout_composite: 8.0, is_burnout_risk: false, is_flight_risk: false,
    estimated_replacement_cost_usd: 9600.0,
    burnout_signal: "Workload exhaustion pattern — 22% after-hours activity — composite 8",
  },
  {
    rep_id: "rep_003", region: "Central",
    burnout_risk: "moderate", attrition_pattern: "quota_pressure",
    burnout_severity: "watch", recommended_action: "wellness_checkin",
    workload_strain_score: 20.0, engagement_decay_score: 18.0,
    quota_pressure_score: 28.0, flight_signal_score: 8.0,
    burnout_composite: 20.4, is_burnout_risk: false, is_flight_risk: false,
    estimated_replacement_cost_usd: 24480.0,
    burnout_signal: "Quota pressure pattern — 2 missed quota periods — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    burnout_risk: "moderate", attrition_pattern: "disengagement",
    burnout_severity: "watch", recommended_action: "wellness_checkin",
    workload_strain_score: 18.0, engagement_decay_score: 30.0,
    quota_pressure_score: 20.0, flight_signal_score: 12.0,
    burnout_composite: 21.3, is_burnout_risk: false, is_flight_risk: false,
    estimated_replacement_cost_usd: 25560.0,
    burnout_signal: "Disengagement pattern — CRM compliance dropped 18pp — only 5d PTO taken — composite 21",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    burnout_risk: "high", attrition_pattern: "workload_exhaustion",
    burnout_severity: "at_risk", recommended_action: "workload_rebalance",
    workload_strain_score: 55.0, engagement_decay_score: 30.0,
    quota_pressure_score: 25.0, flight_signal_score: 20.0,
    burnout_composite: 35.3, is_burnout_risk: false, is_flight_risk: true,
    estimated_replacement_cost_usd: 42360.0,
    burnout_signal: "Workload exhaustion pattern — 40% after-hours activity — 3 sick days 90d — composite 35",
  },
  {
    rep_id: "rep_006", region: "West",
    burnout_risk: "high", attrition_pattern: "compensation_dissatisfaction",
    burnout_severity: "at_risk", recommended_action: "retention_interview",
    workload_strain_score: 30.0, engagement_decay_score: 35.0,
    quota_pressure_score: 32.0, flight_signal_score: 42.0,
    burnout_composite: 33.8, is_burnout_risk: false, is_flight_risk: true,
    estimated_replacement_cost_usd: 40560.0,
    burnout_signal: "Compensation dissatisfaction pattern — LinkedIn activity spike detected — composite 34",
  },
  {
    rep_id: "rep_007", region: "APAC",
    burnout_risk: "critical", attrition_pattern: "manager_conflict",
    burnout_severity: "flight_risk", recommended_action: "executive_retention",
    workload_strain_score: 65.0, engagement_decay_score: 62.0,
    quota_pressure_score: 70.0, flight_signal_score: 55.0,
    burnout_composite: 64.3, is_burnout_risk: true, is_flight_risk: true,
    estimated_replacement_cost_usd: 77160.0,
    burnout_signal: "Manager conflict pattern — 4 escalations raised — LinkedIn activity spike detected — 0d PTO taken — composite 64",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    burnout_risk: "critical", attrition_pattern: "quota_pressure",
    burnout_severity: "flight_risk", recommended_action: "retention_interview",
    workload_strain_score: 70.0, engagement_decay_score: 65.0,
    quota_pressure_score: 80.0, flight_signal_score: 60.0,
    burnout_composite: 71.3, is_burnout_risk: true, is_flight_risk: true,
    estimated_replacement_cost_usd: 85560.0,
    burnout_signal: "Quota pressure pattern — 3 consecutive missed quota periods — 50% after-hours activity — 6 disengaged deals — composite 71",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-rep-burnout-attrition-risk-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.burnout_risk      === risk);
  if (pattern) reps = reps.filter((r) => r.attrition_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_work = 0, total_eng = 0, total_quot = 0, total_flt = 0, total_cost = 0;

  for (const r of mockReps) {
    risk_counts[r.burnout_risk]           = (risk_counts[r.burnout_risk] || 0) + 1;
    pattern_counts[r.attrition_pattern]   = (pattern_counts[r.attrition_pattern] || 0) + 1;
    severity_counts[r.burnout_severity]   = (severity_counts[r.burnout_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.burnout_composite;
    total_work += r.workload_strain_score;
    total_eng  += r.engagement_decay_score;
    total_quot += r.quota_pressure_score;
    total_flt  += r.flight_signal_score;
    total_cost += r.estimated_replacement_cost_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                   n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_burnout_composite:                   Math.round((total_comp / n) * 10) / 10,
      burnout_risk_count:                      mockReps.filter((r) => r.is_burnout_risk).length,
      flight_risk_count:                       mockReps.filter((r) => r.is_flight_risk).length,
      avg_workload_strain_score:               Math.round((total_work / n) * 10) / 10,
      avg_engagement_decay_score:              Math.round((total_eng  / n) * 10) / 10,
      avg_quota_pressure_score:                Math.round((total_quot / n) * 10) / 10,
      avg_flight_signal_score:                 Math.round((total_flt  / n) * 10) / 10,
      total_estimated_replacement_cost_usd:    Math.round(total_cost * 100) / 100,
    },
  });
}
