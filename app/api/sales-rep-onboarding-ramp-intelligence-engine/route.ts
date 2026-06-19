import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    ramp_risk: "low", ramp_pattern: "none",
    ramp_severity: "accelerating", recommended_action: "no_action",
    pipeline_score: 0.0, activity_score: 0.0,
    coaching_score: 0.0, progression_score: 0.0,
    ramp_composite: 0.0,
    has_ramp_gap: false, requires_ramp_intervention: false,
    estimated_ramp_revenue_loss_usd: 0.0,
    ramp_signal: "Ramp progression healthy — pipeline build, activity adoption, and coaching engagement within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    ramp_risk: "low", ramp_pattern: "none",
    ramp_severity: "accelerating", recommended_action: "no_action",
    pipeline_score: 3.0, activity_score: 4.0,
    coaching_score: 2.0, progression_score: 5.0,
    ramp_composite: 3.35,
    has_ramp_gap: false, requires_ramp_intervention: false,
    estimated_ramp_revenue_loss_usd: 0.0,
    ramp_signal: "Ramp progression healthy — pipeline build, activity adoption, and coaching engagement within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    ramp_risk: "moderate", ramp_pattern: "activity_adoption_lag",
    ramp_severity: "on_track", recommended_action: "activity_habits_coaching",
    pipeline_score: 18.0, activity_score: 25.0,
    coaching_score: 12.0, progression_score: 20.0,
    ramp_composite: 19.3,
    has_ramp_gap: false, requires_ramp_intervention: false,
    estimated_ramp_revenue_loss_usd: 12000.0,
    ramp_signal: "Activity adoption lag — 65% pipeline target built — 55% activity adoption — week 8 of 24 — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    ramp_risk: "moderate", ramp_pattern: "slow_pipeline_build",
    ramp_severity: "on_track", recommended_action: "pipeline_build_coaching",
    pipeline_score: 28.0, activity_score: 18.0,
    coaching_score: 22.0, progression_score: 15.0,
    ramp_composite: 22.1,
    has_ramp_gap: false, requires_ramp_intervention: true,
    estimated_ramp_revenue_loss_usd: 28000.0,
    ramp_signal: "Slow pipeline build — 42% pipeline target built — 65% activity adoption — week 10 of 24 — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    ramp_risk: "high", ramp_pattern: "first_deal_stall",
    ramp_severity: "lagging", recommended_action: "deal_progression_coaching",
    pipeline_score: 40.0, activity_score: 35.0,
    coaching_score: 30.0, progression_score: 42.0,
    ramp_composite: 37.05,
    has_ramp_gap: false, requires_ramp_intervention: true,
    estimated_ramp_revenue_loss_usd: 68000.0,
    ramp_signal: "First deal stall — 35% pipeline target built — 45% activity adoption — week 15 of 24 — composite 37",
  },
  {
    rep_id: "rep_006", region: "West",
    ramp_risk: "high", ramp_pattern: "coaching_resistance",
    ramp_severity: "lagging", recommended_action: "manager_led_intervention",
    pipeline_score: 45.0, activity_score: 40.0,
    coaching_score: 52.0, progression_score: 38.0,
    ramp_composite: 44.15,
    has_ramp_gap: true, requires_ramp_intervention: true,
    estimated_ramp_revenue_loss_usd: 126000.0,
    ramp_signal: "Coaching resistance — 30% pipeline target built — 40% activity adoption — week 16 of 24 — composite 44",
  },
  {
    rep_id: "rep_007", region: "APAC",
    ramp_risk: "critical", ramp_pattern: "early_exit_risk",
    ramp_severity: "derailing", recommended_action: "ramp_extension_review",
    pipeline_score: 68.0, activity_score: 72.0,
    coaching_score: 60.0, progression_score: 78.0,
    ramp_composite: 68.8,
    has_ramp_gap: true, requires_ramp_intervention: true,
    estimated_ramp_revenue_loss_usd: 280000.0,
    ramp_signal: "Early exit risk — 15% pipeline target built — 25% activity adoption — week 18 of 24 — composite 69",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    ramp_risk: "critical", ramp_pattern: "early_exit_risk",
    ramp_severity: "derailing", recommended_action: "ramp_extension_review",
    pipeline_score: 100.0, activity_score: 100.0,
    coaching_score: 100.0, progression_score: 100.0,
    ramp_composite: 100.0,
    has_ramp_gap: true, requires_ramp_intervention: true,
    estimated_ramp_revenue_loss_usd: 42500.0,
    ramp_signal: "Early exit risk — 10% pipeline target built — 20% activity adoption — week 20 of 24 — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-rep-onboarding-ramp-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.ramp_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.ramp_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_pip = 0, total_act = 0, total_coa = 0, total_pro = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.ramp_risk]           = (risk_counts[r.ramp_risk] || 0) + 1;
    pattern_counts[r.ramp_pattern]     = (pattern_counts[r.ramp_pattern] || 0) + 1;
    severity_counts[r.ramp_severity]   = (severity_counts[r.ramp_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.ramp_composite;
    total_pip  += r.pipeline_score;
    total_act  += r.activity_score;
    total_coa  += r.coaching_score;
    total_pro  += r.progression_score;
    total_loss += r.estimated_ramp_revenue_loss_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                      n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_ramp_composite:                         Math.round((total_comp / n) * 10) / 10,
      ramp_gap_count:                             mockReps.filter((r) => r.has_ramp_gap).length,
      intervention_count:                         mockReps.filter((r) => r.requires_ramp_intervention).length,
      avg_pipeline_score:                         Math.round((total_pip / n) * 10) / 10,
      avg_activity_score:                         Math.round((total_act / n) * 10) / 10,
      avg_coaching_score:                         Math.round((total_coa / n) * 10) / 10,
      avg_progression_score:                      Math.round((total_pro / n) * 10) / 10,
      total_estimated_ramp_revenue_loss_usd:      Math.round(total_loss * 100) / 100,
    },
  });
}
