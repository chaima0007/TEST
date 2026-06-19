import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    retention_risk: "low", retention_pattern: "none",
    retention_severity: "committed", recommended_action: "no_action",
    compensation_satisfaction_score: 0.0, engagement_vitality_score: 0.0,
    career_progression_score: 0.0, performance_satisfaction_score: 0.0,
    retention_risk_composite: 0.0,
    is_flight_risk: false, requires_retention_action: false,
    estimated_replacement_cost_usd: 0.0,
    retention_signal: "Retention indicators healthy — rep showing strong engagement and satisfaction",
  },
  {
    rep_id: "rep_002", region: "East",
    retention_risk: "low", retention_pattern: "none",
    retention_severity: "committed", recommended_action: "no_action",
    compensation_satisfaction_score: 4.0, engagement_vitality_score: 3.0,
    career_progression_score: 5.0, performance_satisfaction_score: 4.0,
    retention_risk_composite: 3.95,
    is_flight_risk: false, requires_retention_action: false,
    estimated_replacement_cost_usd: 0.0,
    retention_signal: "Retention indicators healthy — rep showing strong engagement and satisfaction",
  },
  {
    rep_id: "rep_003", region: "Central",
    retention_risk: "moderate", retention_pattern: "performance_frustration",
    retention_severity: "developing", recommended_action: "retention_check_in",
    compensation_satisfaction_score: 15.0, engagement_vitality_score: 12.0,
    career_progression_score: 18.0, performance_satisfaction_score: 32.0,
    retention_risk_composite: 18.45,
    is_flight_risk: false, requires_retention_action: false,
    estimated_replacement_cost_usd: 16210.0,
    retention_signal: "Performance frustration — disengagement signals detected — composite 18",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    retention_risk: "moderate", retention_pattern: "disengagement",
    retention_severity: "developing", recommended_action: "retention_check_in",
    compensation_satisfaction_score: 20.0, engagement_vitality_score: 38.0,
    career_progression_score: 14.0, performance_satisfaction_score: 15.0,
    retention_risk_composite: 23.0,
    is_flight_risk: false, requires_retention_action: false,
    estimated_replacement_cost_usd: 19166.7,
    retention_signal: "Disengagement — activity down 16% — composite 23",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    retention_risk: "high", retention_pattern: "career_stagnation",
    retention_severity: "wavering", recommended_action: "career_development_plan",
    compensation_satisfaction_score: 30.0, engagement_vitality_score: 28.0,
    career_progression_score: 40.0, performance_satisfaction_score: 18.0,
    retention_risk_composite: 30.2,
    is_flight_risk: false, requires_retention_action: true,
    estimated_replacement_cost_usd: 32216.7,
    retention_signal: "Career stagnation — 28mo tenure at risk — composite 30",
  },
  {
    rep_id: "rep_006", region: "West",
    retention_risk: "high", retention_pattern: "compensation_risk",
    retention_severity: "wavering", recommended_action: "compensation_review",
    compensation_satisfaction_score: 40.0, engagement_vitality_score: 30.0,
    career_progression_score: 25.0, performance_satisfaction_score: 25.0,
    retention_risk_composite: 31.25,
    is_flight_risk: true, requires_retention_action: true,
    estimated_replacement_cost_usd: 41666.7,
    retention_signal: "Compensation risk — 12% below market comp — composite 31",
  },
  {
    rep_id: "rep_007", region: "APAC",
    retention_risk: "critical", retention_pattern: "compensation_risk",
    retention_severity: "flight_risk", recommended_action: "immediate_retention_package",
    compensation_satisfaction_score: 65.0, engagement_vitality_score: 60.0,
    career_progression_score: 55.0, performance_satisfaction_score: 50.0,
    retention_risk_composite: 59.25,
    is_flight_risk: true, requires_retention_action: true,
    estimated_replacement_cost_usd: 94800.0,
    retention_signal: "Compensation risk — 20% below market comp — activity down 30% — 36mo tenure at risk — composite 59",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    retention_risk: "critical", retention_pattern: "disengagement",
    retention_severity: "flight_risk", recommended_action: "immediate_retention_package",
    compensation_satisfaction_score: 72.0, engagement_vitality_score: 78.0,
    career_progression_score: 68.0, performance_satisfaction_score: 62.0,
    retention_risk_composite: 71.3,
    is_flight_risk: true, requires_retention_action: true,
    estimated_replacement_cost_usd: 113600.0,
    retention_signal: "Disengagement — 22% below market comp — activity down 40% — 48mo tenure at risk — composite 71",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-rep-retention-risk-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.retention_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.retention_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_composite = 0, total_eng = 0, total_car = 0, total_per = 0, total_cost = 0;

  for (const r of mockReps) {
    risk_counts[r.retention_risk]       = (risk_counts[r.retention_risk] || 0) + 1;
    pattern_counts[r.retention_pattern] = (pattern_counts[r.retention_pattern] || 0) + 1;
    severity_counts[r.retention_severity] = (severity_counts[r.retention_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_composite += r.retention_risk_composite;
    total_comp      += r.compensation_satisfaction_score;
    total_eng       += r.engagement_vitality_score;
    total_car       += r.career_progression_score;
    total_per       += r.performance_satisfaction_score;
    total_cost      += r.estimated_replacement_cost_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                  n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_retention_risk_composite:           Math.round((total_composite / n) * 10) / 10,
      flight_risk_count:                      mockReps.filter((r) => r.is_flight_risk).length,
      retention_action_count:                 mockReps.filter((r) => r.requires_retention_action).length,
      avg_compensation_satisfaction_score:    Math.round((total_comp / n) * 10) / 10,
      avg_engagement_vitality_score:          Math.round((total_eng / n) * 10) / 10,
      avg_career_progression_score:           Math.round((total_car / n) * 10) / 10,
      avg_performance_satisfaction_score:     Math.round((total_per / n) * 10) / 10,
      total_estimated_replacement_cost_usd:   Math.round(total_cost * 100) / 100,
    },
  });
}
