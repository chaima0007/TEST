import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    velocity_risk: "low", velocity_pattern: "none",
    velocity_severity: "healthy", recommended_action: "no_action",
    cycle_length_score: 0.0, stage_stall_score: 0.0,
    buyer_engagement_score: 0.0, late_stage_drag_score: 0.0,
    velocity_composite: 0.0, is_velocity_degraded: false, requires_intervention: false,
    estimated_at_risk_deals: 0,
    velocity_signal: "Sales cycle velocity within healthy parameters — no degradation signals",
  },
  {
    rep_id: "rep_002", region: "East",
    velocity_risk: "low", velocity_pattern: "stage_progression_stall",
    velocity_severity: "slowing", recommended_action: "no_action",
    cycle_length_score: 8.0, stage_stall_score: 14.0,
    buyer_engagement_score: 8.0, late_stage_drag_score: 5.0,
    velocity_composite: 9.1, is_velocity_degraded: false, requires_intervention: false,
    estimated_at_risk_deals: 1,
    velocity_signal: "Stage progression stall — cycle 68d vs 60d benchmark (+13%) — 1 deal stalled 14d+ — composite 9",
  },
  {
    rep_id: "rep_003", region: "Central",
    velocity_risk: "moderate", velocity_pattern: "buyer_inactivity",
    velocity_severity: "slowing", recommended_action: "cycle_review",
    cycle_length_score: 18.0, stage_stall_score: 20.0,
    buyer_engagement_score: 28.0, late_stage_drag_score: 10.0,
    velocity_composite: 19.8, is_velocity_degraded: false, requires_intervention: false,
    estimated_at_risk_deals: 3,
    velocity_signal: "Buyer inactivity — 4.2d avg buyer response — cycle 78d vs 60d benchmark (+30%) — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    velocity_risk: "moderate", velocity_pattern: "approval_bottleneck",
    velocity_severity: "slowing", recommended_action: "cycle_review",
    cycle_length_score: 22.0, stage_stall_score: 18.0,
    buyer_engagement_score: 15.0, late_stage_drag_score: 22.0,
    velocity_composite: 19.9, is_velocity_degraded: false, requires_intervention: false,
    estimated_at_risk_deals: 2,
    velocity_signal: "Approval bottleneck — approval 18d vs 10d benchmark — 2 late-stage stalled — composite 20",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    velocity_risk: "high", velocity_pattern: "late_stage_drag",
    velocity_severity: "degraded", recommended_action: "buyer_re_engagement",
    cycle_length_score: 35.0, stage_stall_score: 30.0,
    buyer_engagement_score: 38.0, late_stage_drag_score: 42.0,
    velocity_composite: 35.3, is_velocity_degraded: false, requires_intervention: true,
    estimated_at_risk_deals: 6,
    velocity_signal: "Late stage drag — 3 late-stage stalled — 7.5d avg buyer response — cycle 92d vs 60d — composite 35",
  },
  {
    rep_id: "rep_006", region: "West",
    velocity_risk: "high", velocity_pattern: "deal_aging",
    velocity_severity: "degraded", recommended_action: "deal_qualification_reset",
    cycle_length_score: 42.0, stage_stall_score: 45.0,
    buyer_engagement_score: 30.0, late_stage_drag_score: 30.0,
    velocity_composite: 38.1, is_velocity_degraded: false, requires_intervention: true,
    estimated_at_risk_deals: 7,
    velocity_signal: "Deal aging — 3 deals stalled 30d+ — cycle 108d vs 60d benchmark (+80%) — 4 close dates slipped — composite 38",
  },
  {
    rep_id: "rep_007", region: "APAC",
    velocity_risk: "critical", velocity_pattern: "deal_aging",
    velocity_severity: "stalled", recommended_action: "executive_acceleration",
    cycle_length_score: 70.0, stage_stall_score: 65.0,
    buyer_engagement_score: 58.0, late_stage_drag_score: 55.0,
    velocity_composite: 63.8, is_velocity_degraded: true, requires_intervention: true,
    estimated_at_risk_deals: 10,
    velocity_signal: "Deal aging — 5 deals stalled 30d+ — cycle 145d vs 60d (+142%) — 5 late-stage stalled — composite 64",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    velocity_risk: "critical", velocity_pattern: "late_stage_drag",
    velocity_severity: "stalled", recommended_action: "executive_acceleration",
    cycle_length_score: 75.0, stage_stall_score: 70.0,
    buyer_engagement_score: 65.0, late_stage_drag_score: 72.0,
    velocity_composite: 70.8, is_velocity_degraded: true, requires_intervention: true,
    estimated_at_risk_deals: 12,
    velocity_signal: "Late stage drag — 6 late-stage stalled of 8 — approval 28d vs 10d benchmark — 8d avg buyer response — composite 71",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-cycle-velocity-degradation-engine`);
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
  let total_comp = 0, total_cy = 0, total_st = 0, total_bu = 0, total_la = 0, total_ar = 0;

  for (const r of mockReps) {
    risk_counts[r.velocity_risk]      = (risk_counts[r.velocity_risk] || 0) + 1;
    pattern_counts[r.velocity_pattern] = (pattern_counts[r.velocity_pattern] || 0) + 1;
    severity_counts[r.velocity_severity] = (severity_counts[r.velocity_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.velocity_composite;
    total_cy   += r.cycle_length_score;
    total_st   += r.stage_stall_score;
    total_bu   += r.buyer_engagement_score;
    total_la   += r.late_stage_drag_score;
    total_ar   += r.estimated_at_risk_deals;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                         n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_velocity_composite:        Math.round((total_comp / n) * 10) / 10,
      degraded_count:                mockReps.filter((r) => r.is_velocity_degraded).length,
      intervention_count:            mockReps.filter((r) => r.requires_intervention).length,
      avg_cycle_length_score:        Math.round((total_cy / n) * 10) / 10,
      avg_stage_stall_score:         Math.round((total_st / n) * 10) / 10,
      avg_buyer_engagement_score:    Math.round((total_bu / n) * 10) / 10,
      avg_late_stage_drag_score:     Math.round((total_la / n) * 10) / 10,
      total_estimated_at_risk_deals: total_ar,
    },
  });
}
