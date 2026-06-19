import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    velocity_risk: "low", velocity_pattern: "none",
    velocity_severity: "flowing", recommended_action: "no_action",
    progression_speed_score: 0.0, pipeline_stagnation_score: 0.0,
    stage_efficiency_score: 0.0, deal_momentum_score: 0.0,
    deal_velocity_composite: 0.0,
    has_velocity_gap: false, requires_deal_coaching: false,
    estimated_revenue_delayed_usd: 0.0,
    velocity_signal: "Deal velocity and pipeline progression within healthy benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    velocity_risk: "low", velocity_pattern: "none",
    velocity_severity: "flowing", recommended_action: "no_action",
    progression_speed_score: 5.0, pipeline_stagnation_score: 5.0,
    stage_efficiency_score: 5.0, deal_momentum_score: 5.0,
    deal_velocity_composite: 5.0,
    has_velocity_gap: false, requires_deal_coaching: false,
    estimated_revenue_delayed_usd: 0.0,
    velocity_signal: "Deal velocity and pipeline progression within healthy benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    velocity_risk: "moderate", velocity_pattern: "cycle_time_bloat",
    velocity_severity: "developing", recommended_action: "deal_progression_coaching",
    progression_speed_score: 10.0, pipeline_stagnation_score: 15.0,
    stage_efficiency_score: 22.0, deal_momentum_score: 18.0,
    deal_velocity_composite: 16.05,
    has_velocity_gap: false, requires_deal_coaching: false,
    estimated_revenue_delayed_usd: 13500.0,
    velocity_signal: "Cycle time bloat — 65d avg cycle — 3 stalled deals — 3 close dates slipped — composite 16",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    velocity_risk: "moderate", velocity_pattern: "late_stage_stall",
    velocity_severity: "developing", recommended_action: "deal_progression_coaching",
    progression_speed_score: 10.0, pipeline_stagnation_score: 18.0,
    stage_efficiency_score: 30.0, deal_momentum_score: 15.0,
    deal_velocity_composite: 18.25,
    has_velocity_gap: false, requires_deal_coaching: false,
    estimated_revenue_delayed_usd: 18000.0,
    velocity_signal: "Late stage stall — 72d avg cycle — 4 stalled deals — 4 close dates slipped — composite 18",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    velocity_risk: "high", velocity_pattern: "slow_progression",
    velocity_severity: "slowing", recommended_action: "deal_progression_coaching",
    progression_speed_score: 35.0, pipeline_stagnation_score: 28.0,
    stage_efficiency_score: 25.0, deal_momentum_score: 20.0,
    deal_velocity_composite: 28.25,
    has_velocity_gap: false, requires_deal_coaching: true,
    estimated_revenue_delayed_usd: 45000.0,
    velocity_signal: "Slow progression — 95d avg cycle — 6 stalled deals — 5 close dates slipped — composite 28",
  },
  {
    rep_id: "rep_006", region: "West",
    velocity_risk: "high", velocity_pattern: "stuck_deals",
    velocity_severity: "slowing", recommended_action: "deal_progression_coaching",
    progression_speed_score: 25.0, pipeline_stagnation_score: 40.0,
    stage_efficiency_score: 28.0, deal_momentum_score: 22.0,
    deal_velocity_composite: 29.35,
    has_velocity_gap: true, requires_deal_coaching: true,
    estimated_revenue_delayed_usd: 72000.0,
    velocity_signal: "Stuck deals — 85d avg cycle — 8 stalled deals — 4 close dates slipped — composite 29",
  },
  {
    rep_id: "rep_007", region: "APAC",
    velocity_risk: "critical", velocity_pattern: "stuck_deals",
    velocity_severity: "stalled", recommended_action: "deal_rescue",
    progression_speed_score: 65.0, pipeline_stagnation_score: 60.0,
    stage_efficiency_score: 55.0, deal_momentum_score: 50.0,
    deal_velocity_composite: 59.25,
    has_velocity_gap: true, requires_deal_coaching: true,
    estimated_revenue_delayed_usd: 200000.0,
    velocity_signal: "Stuck deals — 150d avg cycle — 12 stalled deals — 8 close dates slipped — composite 59",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    velocity_risk: "critical", velocity_pattern: "slow_progression",
    velocity_severity: "stalled", recommended_action: "cycle_time_reduction",
    progression_speed_score: 70.0, pipeline_stagnation_score: 65.0,
    stage_efficiency_score: 65.0, deal_momentum_score: 62.0,
    deal_velocity_composite: 66.05,
    has_velocity_gap: true, requires_deal_coaching: true,
    estimated_revenue_delayed_usd: 360000.0,
    velocity_signal: "Slow progression — 200d avg cycle — 15 stalled deals — 10 close dates slipped — composite 66",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-deal-velocity-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.velocity_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.velocity_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_sp = 0, total_stag = 0, total_eff = 0, total_mom = 0, total_del = 0;

  for (const r of mockReps) {
    risk_counts[r.velocity_risk]       = (risk_counts[r.velocity_risk] || 0) + 1;
    pattern_counts[r.velocity_pattern] = (pattern_counts[r.velocity_pattern] || 0) + 1;
    severity_counts[r.velocity_severity] = (severity_counts[r.velocity_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.deal_velocity_composite;
    total_sp   += r.progression_speed_score;
    total_stag += r.pipeline_stagnation_score;
    total_eff  += r.stage_efficiency_score;
    total_mom  += r.deal_momentum_score;
    total_del  += r.estimated_revenue_delayed_usd;
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
      avg_deal_velocity_composite:          Math.round((total_comp / n) * 10) / 10,
      velocity_gap_count:                   mockReps.filter((r) => r.has_velocity_gap).length,
      deal_coaching_count:                  mockReps.filter((r) => r.requires_deal_coaching).length,
      avg_progression_speed_score:          Math.round((total_sp / n) * 10) / 10,
      avg_pipeline_stagnation_score:        Math.round((total_stag / n) * 10) / 10,
      avg_stage_efficiency_score:           Math.round((total_eff / n) * 10) / 10,
      avg_deal_momentum_score:              Math.round((total_mom / n) * 10) / 10,
      total_estimated_revenue_delayed_usd:  Math.round(total_del * 100) / 100,
    },
  });
}
