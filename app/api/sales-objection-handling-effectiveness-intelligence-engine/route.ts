import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    objection_risk: "low", objection_pattern: "none",
    objection_severity: "proficient", recommended_action: "no_action",
    price_score: 0.0, value_score: 0.0,
    competitive_score: 0.0, timing_score: 0.0,
    objection_composite: 0.0,
    has_objection_gap: false, requires_objection_coaching: false,
    estimated_revenue_surrendered_usd: 0.0,
    objection_signal: "Objection handling proficient — price defense, value articulation, and competitive positioning within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    objection_risk: "low", objection_pattern: "none",
    objection_severity: "proficient", recommended_action: "no_action",
    price_score: 4.0, value_score: 3.0,
    competitive_score: 5.0, timing_score: 2.0,
    objection_composite: 3.5,
    has_objection_gap: false, requires_objection_coaching: false,
    estimated_revenue_surrendered_usd: 0.0,
    objection_signal: "Objection handling proficient — price defense, value articulation, and competitive positioning within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    objection_risk: "moderate", objection_pattern: "none",
    objection_severity: "managing", recommended_action: "objection_scripting_coaching",
    price_score: 22.0, value_score: 20.0,
    competitive_score: 22.0, timing_score: 18.0,
    objection_composite: 21.1,
    has_objection_gap: false, requires_objection_coaching: true,
    estimated_revenue_surrendered_usd: 31500.0,
    objection_signal: "Objection handling risk — 35% price objections lead to discount — 52% value objection close rate — 58% competitive win rate — composite 21",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    objection_risk: "moderate", objection_pattern: "timing_deferral",
    objection_severity: "managing", recommended_action: "objection_scripting_coaching",
    price_score: 25.0, value_score: 28.0,
    competitive_score: 22.0, timing_score: 35.0,
    objection_composite: 27.2,
    has_objection_gap: false, requires_objection_coaching: true,
    estimated_revenue_surrendered_usd: 62400.0,
    objection_signal: "Timing deferral — 40% price objections lead to discount — 45% value objection close rate — 52% competitive win rate — composite 27",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    objection_risk: "high", objection_pattern: "competitor_deflection",
    objection_severity: "struggling", recommended_action: "competitive_response_coaching",
    price_score: 40.0, value_score: 38.0,
    competitive_score: 55.0, timing_score: 32.0,
    objection_composite: 41.5,
    has_objection_gap: true, requires_objection_coaching: true,
    estimated_revenue_surrendered_usd: 216000.0,
    objection_signal: "Competitor deflection — 52% price objections lead to discount — 38% value objection close rate — 28% competitive win rate — composite 42",
  },
  {
    rep_id: "rep_006", region: "West",
    objection_risk: "high", objection_pattern: "value_gap_avoidance",
    objection_severity: "struggling", recommended_action: "objection_scripting_coaching",
    price_score: 48.0, value_score: 55.0,
    competitive_score: 45.0, timing_score: 40.0,
    objection_composite: 48.5,
    has_objection_gap: true, requires_objection_coaching: true,
    estimated_revenue_surrendered_usd: 384000.0,
    objection_signal: "Value gap avoidance — 58% price objections lead to discount — 28% value objection close rate — 38% competitive win rate — composite 49",
  },
  {
    rep_id: "rep_007", region: "APAC",
    objection_risk: "critical", objection_pattern: "price_capitulation",
    objection_severity: "collapsing", recommended_action: "closing_technique_coaching",
    price_score: 75.0, value_score: 68.0,
    competitive_score: 72.0, timing_score: 65.0,
    objection_composite: 70.8,
    has_objection_gap: true, requires_objection_coaching: true,
    estimated_revenue_surrendered_usd: 875000.0,
    objection_signal: "Price capitulation — 68% price objections lead to discount — 22% value objection close rate — 20% competitive win rate — composite 71",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    objection_risk: "critical", objection_pattern: "price_capitulation",
    objection_severity: "collapsing", recommended_action: "closing_technique_coaching",
    price_score: 100.0, value_score: 100.0,
    competitive_score: 100.0, timing_score: 100.0,
    objection_composite: 100.0,
    has_objection_gap: true, requires_objection_coaching: true,
    estimated_revenue_surrendered_usd: 937500.0,
    objection_signal: "Price capitulation — 75% price objections lead to discount — 15% value objection close rate — 20% competitive win rate — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-objection-handling-effectiveness-intelligence-engine`);
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
  let total_comp = 0, total_pri = 0, total_val = 0, total_com = 0, total_tim = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.objection_risk]         = (risk_counts[r.objection_risk] || 0) + 1;
    pattern_counts[r.objection_pattern]   = (pattern_counts[r.objection_pattern] || 0) + 1;
    severity_counts[r.objection_severity] = (severity_counts[r.objection_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.objection_composite;
    total_pri  += r.price_score;
    total_val  += r.value_score;
    total_com  += r.competitive_score;
    total_tim  += r.timing_score;
    total_loss += r.estimated_revenue_surrendered_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                       n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_objection_composite:                     Math.round((total_comp / n) * 10) / 10,
      objection_gap_count:                         mockReps.filter((r) => r.has_objection_gap).length,
      coaching_count:                              mockReps.filter((r) => r.requires_objection_coaching).length,
      avg_price_score:                             Math.round((total_pri / n) * 10) / 10,
      avg_value_score:                             Math.round((total_val / n) * 10) / 10,
      avg_competitive_score:                       Math.round((total_com / n) * 10) / 10,
      avg_timing_score:                            Math.round((total_tim / n) * 10) / 10,
      total_estimated_revenue_surrendered_usd:     Math.round(total_loss * 100) / 100,
    },
  });
}
