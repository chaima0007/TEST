import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    decay_risk: "low", decay_pattern: "none",
    decay_severity: "improving", recommended_action: "no_action",
    trajectory_score: 0.0, competitive_score: 0.0,
    deal_quality_score: 0.0, late_stage_score: 0.0,
    decay_composite: 0.0,
    has_decay_gap: false, requires_decay_coaching: false,
    estimated_revenue_decay_usd: 0.0,
    decay_signal: "Win rate stable — trajectory, competitive positioning, and late-stage conversion within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    decay_risk: "low", decay_pattern: "none",
    decay_severity: "improving", recommended_action: "no_action",
    trajectory_score: 3.0, competitive_score: 4.0,
    deal_quality_score: 2.0, late_stage_score: 5.0,
    decay_composite: 3.45,
    has_decay_gap: false, requires_decay_coaching: false,
    estimated_revenue_decay_usd: 0.0,
    decay_signal: "Win rate stable — trajectory, competitive positioning, and late-stage conversion within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    decay_risk: "moderate", decay_pattern: "gradual_erosion",
    decay_severity: "stable", recommended_action: "win_loss_debrief_coaching",
    trajectory_score: 18.0, competitive_score: 20.0,
    deal_quality_score: 15.0, late_stage_score: 22.0,
    decay_composite: 18.65,
    has_decay_gap: false, requires_decay_coaching: false,
    estimated_revenue_decay_usd: 36000.0,
    decay_signal: "Gradual erosion — 38% current win rate — 6pp decline over 6m — 40% competitive win rate — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    decay_risk: "moderate", decay_pattern: "gradual_erosion",
    decay_severity: "stable", recommended_action: "win_loss_debrief_coaching",
    trajectory_score: 25.0, competitive_score: 18.0,
    deal_quality_score: 22.0, late_stage_score: 20.0,
    decay_composite: 21.9,
    has_decay_gap: false, requires_decay_coaching: true,
    estimated_revenue_decay_usd: 78000.0,
    decay_signal: "Gradual erosion — 32% current win rate — 10pp decline over 6m — 35% competitive win rate — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    decay_risk: "high", decay_pattern: "competitive_displacement",
    decay_severity: "declining", recommended_action: "win_loss_debrief_coaching",
    trajectory_score: 38.0, competitive_score: 45.0,
    deal_quality_score: 30.0, late_stage_score: 35.0,
    decay_composite: 37.65,
    has_decay_gap: false, requires_decay_coaching: true,
    estimated_revenue_decay_usd: 185000.0,
    decay_signal: "Competitive displacement — 25% current win rate — 15pp decline over 6m — 22% competitive win rate — composite 38",
  },
  {
    rep_id: "rep_006", region: "West",
    decay_risk: "high", decay_pattern: "late_stage_collapse",
    decay_severity: "declining", recommended_action: "win_loss_debrief_coaching",
    trajectory_score: 42.0, competitive_score: 35.0,
    deal_quality_score: 38.0, late_stage_score: 52.0,
    decay_composite: 41.3,
    has_decay_gap: true, requires_decay_coaching: true,
    estimated_revenue_decay_usd: 320000.0,
    decay_signal: "Late stage collapse — 22% current win rate — 18pp decline over 6m — 28% competitive win rate — composite 41",
  },
  {
    rep_id: "rep_007", region: "APAC",
    decay_risk: "critical", decay_pattern: "sharp_cliff_drop",
    decay_severity: "collapsing", recommended_action: "urgent_pipeline_intervention",
    trajectory_score: 68.0, competitive_score: 62.0,
    deal_quality_score: 55.0, late_stage_score: 60.0,
    decay_composite: 63.55,
    has_decay_gap: true, requires_decay_coaching: true,
    estimated_revenue_decay_usd: 780000.0,
    decay_signal: "Sharp cliff drop — 15% current win rate — 25pp decline over 6m — 15% competitive win rate — composite 64",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    decay_risk: "critical", decay_pattern: "deal_size_inflation_trap",
    decay_severity: "collapsing", recommended_action: "urgent_pipeline_intervention",
    trajectory_score: 100.0, competitive_score: 100.0,
    deal_quality_score: 100.0, late_stage_score: 100.0,
    decay_composite: 100.0,
    has_decay_gap: true, requires_decay_coaching: true,
    estimated_revenue_decay_usd: 4200000.0,
    decay_signal: "Deal size inflation trap — 12% current win rate — 28pp decline over 6m — 8% competitive win rate — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-win-rate-decay-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.decay_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.decay_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_tra = 0, total_com = 0, total_dq = 0, total_ls = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.decay_risk]         = (risk_counts[r.decay_risk] || 0) + 1;
    pattern_counts[r.decay_pattern]   = (pattern_counts[r.decay_pattern] || 0) + 1;
    severity_counts[r.decay_severity] = (severity_counts[r.decay_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.decay_composite;
    total_tra  += r.trajectory_score;
    total_com  += r.competitive_score;
    total_dq   += r.deal_quality_score;
    total_ls   += r.late_stage_score;
    total_loss += r.estimated_revenue_decay_usd;
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
      avg_decay_composite:                    Math.round((total_comp / n) * 10) / 10,
      decay_gap_count:                        mockReps.filter((r) => r.has_decay_gap).length,
      coaching_count:                         mockReps.filter((r) => r.requires_decay_coaching).length,
      avg_trajectory_score:                   Math.round((total_tra / n) * 10) / 10,
      avg_competitive_score:                  Math.round((total_com / n) * 10) / 10,
      avg_deal_quality_score:                 Math.round((total_dq / n) * 10) / 10,
      avg_late_stage_score:                   Math.round((total_ls / n) * 10) / 10,
      total_estimated_revenue_decay_usd:      Math.round(total_loss * 100) / 100,
    },
  });
}
