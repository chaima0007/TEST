import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", rep_name: "Sarah Chen", region: "NAMER",
    attrition_risk: "low", attrition_signal: "no_signal",
    compensation_health: "competitive", retention_action: "maintain",
    disengagement_score: 2.0, compensation_risk_score: 5.0,
    performance_satisfaction_score: 92.0, social_risk_score: 3.0,
    attrition_composite: 2.5,
    is_flight_risk: false, needs_urgent_retention: false,
    estimated_pipeline_at_risk_usd: 11250.0,
    primary_attrition_signal: "primary driver: compensation risk",
    tenure_months: 18, quota_attainment_pct: 112.0,
    compensation_vs_market_pct: 105.0,
  },
  {
    rep_id: "rep_002", rep_name: "Marcus Webb", region: "EMEA",
    attrition_risk: "critical", attrition_signal: "likely_departing",
    compensation_health: "underpaid", retention_action: "urgent_retention_meeting",
    disengagement_score: 72.0, compensation_risk_score: 65.0,
    performance_satisfaction_score: 28.0, social_risk_score: 68.0,
    attrition_composite: 81.5,
    is_flight_risk: true, needs_urgent_retention: true,
    estimated_pipeline_at_risk_usd: 326000.0,
    primary_attrition_signal: "high LinkedIn activity — active job search detected",
    tenure_months: 24, quota_attainment_pct: 42.0,
    compensation_vs_market_pct: 72.0,
  },
  {
    rep_id: "rep_003", rep_name: "Priya Nair", region: "APAC",
    attrition_risk: "moderate", attrition_signal: "early_warning",
    compensation_health: "at_risk", retention_action: "recognition_and_development",
    disengagement_score: 30.0, compensation_risk_score: 35.0,
    performance_satisfaction_score: 55.0, social_risk_score: 25.0,
    attrition_composite: 38.0,
    is_flight_risk: false, needs_urgent_retention: false,
    estimated_pipeline_at_risk_usd: 76000.0,
    primary_attrition_signal: "primary driver: disengagement",
    tenure_months: 12, quota_attainment_pct: 78.0,
    compensation_vs_market_pct: 86.0,
  },
  {
    rep_id: "rep_004", rep_name: "Jake Omondi", region: "LATAM",
    attrition_risk: "high", attrition_signal: "active_search",
    compensation_health: "underpaid", retention_action: "compensation_review",
    disengagement_score: 48.0, compensation_risk_score: 58.0,
    performance_satisfaction_score: 42.0, social_risk_score: 52.0,
    attrition_composite: 65.0,
    is_flight_risk: true, needs_urgent_retention: false,
    estimated_pipeline_at_risk_usd: 182000.0,
    primary_attrition_signal: "underpaid vs market (76%) — compensation is primary flight risk",
    tenure_months: 30, quota_attainment_pct: 62.0,
    compensation_vs_market_pct: 76.0,
  },
  {
    rep_id: "rep_005", rep_name: "Elena Vasquez", region: "NAMER",
    attrition_risk: "low", attrition_signal: "no_signal",
    compensation_health: "competitive", retention_action: "maintain",
    disengagement_score: 5.0, compensation_risk_score: 8.0,
    performance_satisfaction_score: 88.0, social_risk_score: 7.0,
    attrition_composite: 10.0,
    is_flight_risk: false, needs_urgent_retention: false,
    estimated_pipeline_at_risk_usd: 42500.0,
    primary_attrition_signal: "primary driver: social risk",
    tenure_months: 36, quota_attainment_pct: 98.0,
    compensation_vs_market_pct: 110.0,
  },
  {
    rep_id: "rep_006", rep_name: "Tom Brennan", region: "EMEA",
    attrition_risk: "high", attrition_signal: "active_search",
    compensation_health: "at_risk", retention_action: "recognition_and_development",
    disengagement_score: 52.0, compensation_risk_score: 40.0,
    performance_satisfaction_score: 38.0, social_risk_score: 55.0,
    attrition_composite: 62.5,
    is_flight_risk: true, needs_urgent_retention: false,
    estimated_pipeline_at_risk_usd: 156250.0,
    primary_attrition_signal: "team attrition contagion — peer departures driving exit risk",
    tenure_months: 14, quota_attainment_pct: 55.0,
    compensation_vs_market_pct: 88.0,
  },
  {
    rep_id: "rep_007", rep_name: "Aisha Kamara", region: "APAC",
    attrition_risk: "moderate", attrition_signal: "early_warning",
    compensation_health: "adequate", retention_action: "recognition_and_development",
    disengagement_score: 22.0, compensation_risk_score: 28.0,
    performance_satisfaction_score: 65.0, social_risk_score: 18.0,
    attrition_composite: 35.5,
    is_flight_risk: false, needs_urgent_retention: false,
    estimated_pipeline_at_risk_usd: 49700.0,
    primary_attrition_signal: "primary driver: disengagement",
    tenure_months: 9, quota_attainment_pct: 85.0,
    compensation_vs_market_pct: 93.0,
  },
  {
    rep_id: "rep_008", rep_name: "Diego Reyes", region: "LATAM",
    attrition_risk: "critical", attrition_signal: "likely_departing",
    compensation_health: "underpaid", retention_action: "urgent_retention_meeting",
    disengagement_score: 65.0, compensation_risk_score: 70.0,
    performance_satisfaction_score: 22.0, social_risk_score: 72.0,
    attrition_composite: 84.0,
    is_flight_risk: true, needs_urgent_retention: true,
    estimated_pipeline_at_risk_usd: 218400.0,
    primary_attrition_signal: "activity collapsed -35% — disengagement in progress",
    tenure_months: 20, quota_attainment_pct: 30.0,
    compensation_vs_market_pct: 68.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk   = searchParams.get("risk");
  const signal = searchParams.get("signal");
  const region = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/rep-attrition-risk-engine`);
      if (risk)   url.searchParams.set("risk", risk);
      if (signal) url.searchParams.set("signal", signal);
      if (region) url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)   reps = reps.filter((r) => r.attrition_risk === risk);
  if (signal) reps = reps.filter((r) => r.attrition_signal === signal);
  if (region) reps = reps.filter((r) => r.region === region);

  const risk_counts:   Record<string, number> = {};
  const sig_counts:    Record<string, number> = {};
  const comp_counts:   Record<string, number> = {};
  const act_counts:    Record<string, number> = {};
  let total_comp = 0, total_dis = 0, total_cr = 0, total_ps = 0, total_sr = 0, total_pipe = 0;

  for (const r of mockReps) {
    risk_counts[r.attrition_risk]        = (risk_counts[r.attrition_risk] || 0) + 1;
    sig_counts[r.attrition_signal]       = (sig_counts[r.attrition_signal] || 0) + 1;
    comp_counts[r.compensation_health]   = (comp_counts[r.compensation_health] || 0) + 1;
    act_counts[r.retention_action]       = (act_counts[r.retention_action] || 0) + 1;
    total_comp  += r.attrition_composite;
    total_dis   += r.disengagement_score;
    total_cr    += r.compensation_risk_score;
    total_ps    += r.performance_satisfaction_score;
    total_sr    += r.social_risk_score;
    total_pipe  += r.estimated_pipeline_at_risk_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total: n,
      risk_counts,
      signal_counts: sig_counts,
      compensation_counts: comp_counts,
      action_counts: act_counts,
      avg_attrition_composite:               Math.round((total_comp / n) * 10) / 10,
      flight_risk_count:                     mockReps.filter((r) => r.is_flight_risk).length,
      urgent_retention_count:                mockReps.filter((r) => r.needs_urgent_retention).length,
      avg_disengagement_score:               Math.round((total_dis / n) * 10) / 10,
      avg_compensation_risk_score:           Math.round((total_cr / n) * 10) / 10,
      avg_performance_satisfaction_score:    Math.round((total_ps / n) * 10) / 10,
      avg_social_risk_score:                 Math.round((total_sr / n) * 10) / 10,
      total_pipeline_at_risk_usd:            Math.round(total_pipe * 100) / 100,
    },
  });
}
