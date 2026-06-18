import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    onboarding_risk: "low", onboarding_pattern: "none",
    onboarding_severity: "ramping", recommended_action: "no_action",
    ramp_velocity_score: 0.0, training_completion_score: 0.0,
    manager_support_score: 0.0, early_performance_score: 0.0,
    onboarding_composite: 0.0,
    has_onboarding_gap: false, requires_onboarding_intervention: false,
    estimated_ramp_delay_cost_usd: 0.0,
    onboarding_signal: "Onboarding velocity healthy — rep progressing within expected ramp benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    onboarding_risk: "low", onboarding_pattern: "none",
    onboarding_severity: "ramping", recommended_action: "no_action",
    ramp_velocity_score: 4.0, training_completion_score: 3.0,
    manager_support_score: 5.0, early_performance_score: 2.0,
    onboarding_composite: 3.65,
    has_onboarding_gap: false, requires_onboarding_intervention: false,
    estimated_ramp_delay_cost_usd: 0.0,
    onboarding_signal: "Onboarding velocity healthy — rep progressing within expected ramp benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    onboarding_risk: "moderate", onboarding_pattern: "slow_ramp",
    onboarding_severity: "developing", recommended_action: "ramp_support_coaching",
    ramp_velocity_score: 25.0, training_completion_score: 18.0,
    manager_support_score: 20.0, early_performance_score: 10.0,
    onboarding_composite: 19.55,
    has_onboarding_gap: false, requires_onboarding_intervention: false,
    estimated_ramp_delay_cost_usd: 23400.0,
    onboarding_signal: "Slow ramp — 62% training complete — 58% pipeline target — 72% manager 1:1 attendance — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    onboarding_risk: "moderate", onboarding_pattern: "training_gap",
    onboarding_severity: "developing", recommended_action: "ramp_support_coaching",
    ramp_velocity_score: 20.0, training_completion_score: 32.0,
    manager_support_score: 18.0, early_performance_score: 14.0,
    onboarding_composite: 22.1,
    has_onboarding_gap: false, requires_onboarding_intervention: true,
    estimated_ramp_delay_cost_usd: 31500.0,
    onboarding_signal: "Training gap — 48% training complete — 62% pipeline target — 68% manager 1:1 attendance — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    onboarding_risk: "high", onboarding_pattern: "product_knowledge_gap",
    onboarding_severity: "struggling", recommended_action: "product_enablement_bootcamp",
    ramp_velocity_score: 38.0, training_completion_score: 45.0,
    manager_support_score: 35.0, early_performance_score: 28.0,
    onboarding_composite: 38.0,
    has_onboarding_gap: true, requires_onboarding_intervention: true,
    estimated_ramp_delay_cost_usd: 91800.0,
    onboarding_signal: "Product knowledge gap — 38% training complete — 45% pipeline target — 55% manager 1:1 attendance — composite 38",
  },
  {
    rep_id: "rep_006", region: "West",
    onboarding_risk: "high", onboarding_pattern: "manager_neglect",
    onboarding_severity: "struggling", recommended_action: "manager_engagement_review",
    ramp_velocity_score: 32.0, training_completion_score: 30.0,
    manager_support_score: 58.0, early_performance_score: 22.0,
    onboarding_composite: 37.3,
    has_onboarding_gap: true, requires_onboarding_intervention: true,
    estimated_ramp_delay_cost_usd: 88200.0,
    onboarding_signal: "Manager neglect — 52% training complete — 52% pipeline target — 35% manager 1:1 attendance — composite 37",
  },
  {
    rep_id: "rep_007", region: "APAC",
    onboarding_risk: "critical", onboarding_pattern: "early_attrition_signal",
    onboarding_severity: "at_risk", recommended_action: "early_retention_intervention",
    ramp_velocity_score: 68.0, training_completion_score: 72.0,
    manager_support_score: 65.0, early_performance_score: 58.0,
    onboarding_composite: 67.1,
    has_onboarding_gap: true, requires_onboarding_intervention: true,
    estimated_ramp_delay_cost_usd: 163800.0,
    onboarding_signal: "Early attrition signal — 28% training complete — 35% pipeline target — 30% manager 1:1 attendance — composite 67",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    onboarding_risk: "critical", onboarding_pattern: "early_attrition_signal",
    onboarding_severity: "at_risk", recommended_action: "early_retention_intervention",
    ramp_velocity_score: 80.0, training_completion_score: 78.0,
    manager_support_score: 72.0, early_performance_score: 68.0,
    onboarding_composite: 75.5,
    has_onboarding_gap: true, requires_onboarding_intervention: true,
    estimated_ramp_delay_cost_usd: 197820.0,
    onboarding_signal: "Early attrition signal — 35% training complete — 42% pipeline target — 25% manager 1:1 attendance — composite 78",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-onboarding-effectiveness-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.onboarding_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.onboarding_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_ramp = 0, total_train = 0, total_mgr = 0, total_perf = 0, total_cost = 0;

  for (const r of mockReps) {
    risk_counts[r.onboarding_risk]       = (risk_counts[r.onboarding_risk] || 0) + 1;
    pattern_counts[r.onboarding_pattern] = (pattern_counts[r.onboarding_pattern] || 0) + 1;
    severity_counts[r.onboarding_severity] = (severity_counts[r.onboarding_severity] || 0) + 1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action] || 0) + 1;
    total_comp  += r.onboarding_composite;
    total_ramp  += r.ramp_velocity_score;
    total_train += r.training_completion_score;
    total_mgr   += r.manager_support_score;
    total_perf  += r.early_performance_score;
    total_cost  += r.estimated_ramp_delay_cost_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_onboarding_composite:                 Math.round((total_comp / n) * 10) / 10,
      onboarding_gap_count:                     mockReps.filter((r) => r.has_onboarding_gap).length,
      intervention_count:                       mockReps.filter((r) => r.requires_onboarding_intervention).length,
      avg_ramp_velocity_score:                  Math.round((total_ramp / n) * 10) / 10,
      avg_training_completion_score:            Math.round((total_train / n) * 10) / 10,
      avg_manager_support_score:                Math.round((total_mgr / n) * 10) / 10,
      avg_early_performance_score:              Math.round((total_perf / n) * 10) / 10,
      total_estimated_ramp_delay_cost_usd:      Math.round(total_cost * 100) / 100,
    },
  });
}
