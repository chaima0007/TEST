import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-deal-momentum-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "REP-001", region: "West",
    momentum_risk: "low", momentum_pattern: "none",
    momentum_severity: "accelerating", recommended_action: "no_action",
    velocity_score: 5.0, engagement_score: 5.0,
    momentum_score: 5.0, discipline_score: 5.0,
    momentum_composite: 5.0,
    has_momentum_gap: false, requires_momentum_coaching: false,
    estimated_stalled_pipeline_usd: 0.0,
    momentum_signal: "Deal momentum strong — velocity, engagement, forecast movement, and next-step discipline within benchmarks",
  },
  {
    rep_id: "REP-002", region: "East",
    momentum_risk: "low", momentum_pattern: "none",
    momentum_severity: "accelerating", recommended_action: "no_action",
    velocity_score: 8.0, engagement_score: 6.0,
    momentum_score: 7.0, discipline_score: 6.0,
    momentum_composite: 7.0,
    has_momentum_gap: false, requires_momentum_coaching: true,
    estimated_stalled_pipeline_usd: 15000.0,
    momentum_signal: "Deal momentum strong — velocity, engagement, forecast movement, and next-step discipline within benchmarks",
  },
  {
    rep_id: "REP-003", region: "Central",
    momentum_risk: "moderate", momentum_pattern: "none",
    momentum_severity: "steady", recommended_action: "pipeline_review",
    velocity_score: 20.0, engagement_score: 18.0,
    momentum_score: 22.0, discipline_score: 16.0,
    momentum_composite: 19.8,
    has_momentum_gap: false, requires_momentum_coaching: true,
    estimated_stalled_pipeline_usd: 40000.0,
    momentum_signal: "None — 15% deals stalled — 20% close dates slipped — 8d avg last contact — composite 20",
  },
  {
    rep_id: "REP-004", region: "Northeast",
    momentum_risk: "moderate", momentum_pattern: "forecast_drift",
    momentum_severity: "steady", recommended_action: "pipeline_review",
    velocity_score: 22.0, engagement_score: 25.0,
    momentum_score: 28.0, discipline_score: 18.0,
    momentum_composite: 23.45,
    has_momentum_gap: false, requires_momentum_coaching: true,
    estimated_stalled_pipeline_usd: 75000.0,
    momentum_signal: "Forecast drift — 20% deals stalled — 30% close dates slipped — 10d avg last contact — composite 23",
  },
  {
    rep_id: "REP-005", region: "Southeast",
    momentum_risk: "high", momentum_pattern: "contact_desert",
    momentum_severity: "decelerating", recommended_action: "contact_cadence_coaching",
    velocity_score: 32.0, engagement_score: 48.0,
    momentum_score: 35.0, discipline_score: 28.0,
    momentum_composite: 37.05,
    has_momentum_gap: true, requires_momentum_coaching: true,
    estimated_stalled_pipeline_usd: 120000.0,
    momentum_signal: "Contact desert — 30% deals stalled — 40% close dates slipped — 16d avg last contact — composite 37",
  },
  {
    rep_id: "REP-006", region: "West",
    momentum_risk: "high", momentum_pattern: "slow_burn",
    momentum_severity: "decelerating", recommended_action: "deal_acceleration_coaching",
    velocity_score: 45.0, engagement_score: 35.0,
    momentum_score: 42.0, discipline_score: 30.0,
    momentum_composite: 39.75,
    has_momentum_gap: true, requires_momentum_coaching: true,
    estimated_stalled_pipeline_usd: 185000.0,
    momentum_signal: "Slow burn — 35% deals stalled — 45% close dates slipped — 12d avg last contact — composite 40",
  },
  {
    rep_id: "REP-007", region: "APAC",
    momentum_risk: "critical", momentum_pattern: "stall_accumulator",
    momentum_severity: "stalled", recommended_action: "executive_deal_rescue",
    velocity_score: 68.0, engagement_score: 60.0,
    momentum_score: 58.0, discipline_score: 52.0,
    momentum_composite: 61.8,
    has_momentum_gap: true, requires_momentum_coaching: true,
    estimated_stalled_pipeline_usd: 420000.0,
    momentum_signal: "Stall accumulator — 55% deals stalled — 60% close dates slipped — 20d avg last contact — composite 62",
  },
  {
    rep_id: "REP-008", region: "EMEA",
    momentum_risk: "critical", momentum_pattern: "late_stage_freeze",
    momentum_severity: "stalled", recommended_action: "executive_deal_rescue",
    velocity_score: 78.0, engagement_score: 72.0,
    momentum_score: 70.0, discipline_score: 65.0,
    momentum_composite: 73.25,
    has_momentum_gap: true, requires_momentum_coaching: true,
    estimated_stalled_pipeline_usd: 700000.0,
    momentum_signal: "Late-stage freeze — 70% deals stalled — 75% close dates slipped — 25d avg last contact — composite 73",
  },
];

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/api/sales-deal-momentum-intelligence-engine`, { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_v = 0, total_e = 0, total_m = 0, total_d = 0, total_sp = 0;

  for (const r of mockReps) {
    risk_counts[r.momentum_risk]       = (risk_counts[r.momentum_risk] || 0) + 1;
    pattern_counts[r.momentum_pattern] = (pattern_counts[r.momentum_pattern] || 0) + 1;
    severity_counts[r.momentum_severity] = (severity_counts[r.momentum_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.momentum_composite;
    total_v    += r.velocity_score;
    total_e    += r.engagement_score;
    total_m    += r.momentum_score;
    total_d    += r.discipline_score;
    total_sp   += r.estimated_stalled_pipeline_usd;
  }

  const n = mockReps.length;
  return sealResponse(NextResponse.json({
    reps: mockReps,
    summary: {
      total:                                  n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_momentum_composite:                 Math.round((total_comp / n) * 10) / 10,
      momentum_gap_count:                     mockReps.filter((r) => r.has_momentum_gap).length,
      coaching_count:                         mockReps.filter((r) => r.requires_momentum_coaching).length,
      avg_velocity_score:                     Math.round((total_v / n) * 10) / 10,
      avg_engagement_score:                   Math.round((total_e / n) * 10) / 10,
      avg_momentum_score:                     Math.round((total_m / n) * 10) / 10,
      avg_discipline_score:                   Math.round((total_d / n) * 10) / 10,
      total_estimated_stalled_pipeline_usd:   Math.round(total_sp * 100) / 100,
    },
  }));
}
