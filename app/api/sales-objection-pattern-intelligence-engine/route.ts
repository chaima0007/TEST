import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    objection_risk: "low", objection_pattern: "none",
    objection_severity: "managed", recommended_action: "no_action",
    price_pressure_score: 0.0, competition_pressure_score: 0.0,
    timing_resistance_score: 0.0, skill_gap_score: 0.0,
    objection_burden_composite: 0.0, has_systemic_issue: false,
    requires_coaching_intervention: false, estimated_lost_revenue_usd: 0.0,
    objection_signal: "Objection handling aligned with team benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    objection_risk: "low", objection_pattern: "none",
    objection_severity: "managed", recommended_action: "no_action",
    price_pressure_score: 8.0, competition_pressure_score: 8.0,
    timing_resistance_score: 8.0, skill_gap_score: 0.0,
    objection_burden_composite: 6.4, has_systemic_issue: false,
    requires_coaching_intervention: false, estimated_lost_revenue_usd: 0.0,
    objection_signal: "Objection handling aligned with team benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    objection_risk: "moderate", objection_pattern: "timing_stall",
    objection_severity: "recurring", recommended_action: "objection_coaching",
    price_pressure_score: 12.0, competition_pressure_score: 8.0,
    timing_resistance_score: 38.0, skill_gap_score: 15.0,
    objection_burden_composite: 20.8, has_systemic_issue: false,
    requires_coaching_intervention: true, estimated_lost_revenue_usd: 10400.0,
    objection_signal: "Timing stall — 3 late-stage objections — 65% overcome rate — composite 21",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    objection_risk: "moderate", objection_pattern: "need_misalignment",
    objection_severity: "recurring", recommended_action: "objection_coaching",
    price_pressure_score: 8.0, competition_pressure_score: 12.0,
    timing_resistance_score: 8.0, skill_gap_score: 28.0,
    objection_burden_composite: 14.6, has_systemic_issue: false,
    requires_coaching_intervention: false, estimated_lost_revenue_usd: 0.0,
    objection_signal: "Need misalignment — 35% overcome rate — composite 25",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    objection_risk: "high", objection_pattern: "price_barrier",
    objection_severity: "systemic", recommended_action: "pricing_review",
    price_pressure_score: 50.0, competition_pressure_score: 8.0,
    timing_resistance_score: 0.0, skill_gap_score: 23.0,
    objection_burden_composite: 24.2, has_systemic_issue: false,
    requires_coaching_intervention: true, estimated_lost_revenue_usd: 24200.0,
    objection_signal: "Price barrier — price objections in 6/12 deals — 30% overcome rate — composite 41",
  },
  {
    rep_id: "rep_006", region: "West",
    objection_risk: "high", objection_pattern: "competitive_displacement",
    objection_severity: "systemic", recommended_action: "battlecard_refresh",
    price_pressure_score: 8.0, competition_pressure_score: 50.0,
    timing_resistance_score: 20.0, skill_gap_score: 23.0,
    objection_burden_composite: 24.9, has_systemic_issue: true,
    requires_coaching_intervention: true, estimated_lost_revenue_usd: 62250.0,
    objection_signal: "Competitive displacement — competitive pressure in 5 deals — 3 late-stage objections — composite 43",
  },
  {
    rep_id: "rep_007", region: "APAC",
    objection_risk: "critical", objection_pattern: "competitive_displacement",
    objection_severity: "blocking", recommended_action: "battlecard_refresh",
    price_pressure_score: 43.0, competition_pressure_score: 73.0,
    timing_resistance_score: 45.0, skill_gap_score: 55.0,
    objection_burden_composite: 54.0, has_systemic_issue: true,
    requires_coaching_intervention: true, estimated_lost_revenue_usd: 162000.0,
    objection_signal: "Competitive displacement — price objections in 5/8 deals — competitive pressure in 4 deals — 4 late-stage objections — composite 64",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    objection_risk: "critical", objection_pattern: "price_barrier",
    objection_severity: "blocking", recommended_action: "pricing_review",
    price_pressure_score: 85.0, competition_pressure_score: 30.0,
    timing_resistance_score: 60.0, skill_gap_score: 70.0,
    objection_burden_composite: 62.0, has_systemic_issue: true,
    requires_coaching_intervention: true, estimated_lost_revenue_usd: 310000.0,
    objection_signal: "Price barrier — price objections in 7/9 deals — competitive pressure in 3 deals — 5 late-stage objections — 20% overcome rate — composite 70",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-objection-pattern-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.objection_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.objection_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_price = 0, total_compp = 0, total_timing = 0, total_skill = 0, total_rev = 0;

  for (const r of mockReps) {
    risk_counts[r.objection_risk]           = (risk_counts[r.objection_risk] || 0) + 1;
    pattern_counts[r.objection_pattern]     = (pattern_counts[r.objection_pattern] || 0) + 1;
    severity_counts[r.objection_severity]   = (severity_counts[r.objection_severity] || 0) + 1;
    action_counts[r.recommended_action]     = (action_counts[r.recommended_action] || 0) + 1;
    total_comp    += r.objection_burden_composite;
    total_price   += r.price_pressure_score;
    total_compp   += r.competition_pressure_score;
    total_timing  += r.timing_resistance_score;
    total_skill   += r.skill_gap_score;
    total_rev     += r.estimated_lost_revenue_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                              n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_objection_burden_composite:     Math.round((total_comp / n) * 10) / 10,
      systemic_issue_count:               mockReps.filter((r) => r.has_systemic_issue).length,
      coaching_intervention_count:        mockReps.filter((r) => r.requires_coaching_intervention).length,
      avg_price_pressure_score:           Math.round((total_price / n) * 10) / 10,
      avg_competition_pressure_score:     Math.round((total_compp / n) * 10) / 10,
      avg_timing_resistance_score:        Math.round((total_timing / n) * 10) / 10,
      avg_skill_gap_score:                Math.round((total_skill / n) * 10) / 10,
      total_estimated_lost_revenue_usd:   Math.round(total_rev * 100) / 100,
    },
  });
}
