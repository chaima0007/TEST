import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    ramp_risk: "low", ramp_pattern: "none",
    ramp_severity: "on_track", recommended_action: "no_action",
    activation_score: 0.0, pipeline_health_score: 0.0,
    knowledge_score: 0.0, productivity_score: 0.0,
    ramp_composite: 0.0,
    has_ramp_gap: false, requires_ramp_coaching: false,
    estimated_ramp_cost_usd: 0.0,
    ramp_signal: "Rep ramp on track — quota activation, pipeline build, and knowledge acquisition within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    ramp_risk: "low", ramp_pattern: "none",
    ramp_severity: "on_track", recommended_action: "no_action",
    activation_score: 4.0, pipeline_health_score: 3.0,
    knowledge_score: 5.0, productivity_score: 2.0,
    ramp_composite: 3.65,
    has_ramp_gap: false, requires_ramp_coaching: true,
    estimated_ramp_cost_usd: 0.0,
    ramp_signal: "Rep ramp on track — quota activation, pipeline build, and knowledge acquisition within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    ramp_risk: "moderate", ramp_pattern: "knowledge_laggard",
    ramp_severity: "watch", recommended_action: "accelerated_onboarding",
    activation_score: 20.0, pipeline_health_score: 18.0,
    knowledge_score: 28.0, productivity_score: 14.0,
    ramp_composite: 20.5,
    has_ramp_gap: true, requires_ramp_coaching: true,
    estimated_ramp_cost_usd: 45000.0,
    ramp_signal: "Knowledge laggard — 55% quota attained — 2.1x pipeline coverage — 58% certs complete — composite 21",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    ramp_risk: "moderate", ramp_pattern: "pipeline_builder_gap",
    ramp_severity: "watch", recommended_action: "accelerated_onboarding",
    activation_score: 22.0, pipeline_health_score: 28.0,
    knowledge_score: 18.0, productivity_score: 15.0,
    ramp_composite: 21.55,
    has_ramp_gap: true, requires_ramp_coaching: true,
    estimated_ramp_cost_usd: 68000.0,
    ramp_signal: "Pipeline builder gap — 45% quota attained — 1.5x pipeline coverage — 72% certs complete — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    ramp_risk: "high", ramp_pattern: "coaching_resistant",
    ramp_severity: "at_risk", recommended_action: "manager_escalation",
    activation_score: 40.0, pipeline_health_score: 38.0,
    knowledge_score: 42.0, productivity_score: 35.0,
    ramp_composite: 39.25,
    has_ramp_gap: true, requires_ramp_coaching: true,
    estimated_ramp_cost_usd: 162000.0,
    ramp_signal: "Coaching resistant — 30% quota attained — 1.2x pipeline coverage — 48% certs complete — composite 39",
  },
  {
    rep_id: "rep_006", region: "West",
    ramp_risk: "high", ramp_pattern: "quota_plateau",
    ramp_severity: "at_risk", recommended_action: "quota_expectation_reset",
    activation_score: 48.0, pipeline_health_score: 42.0,
    knowledge_score: 40.0, productivity_score: 50.0,
    ramp_composite: 44.9,
    has_ramp_gap: true, requires_ramp_coaching: true,
    estimated_ramp_cost_usd: 247500.0,
    ramp_signal: "Quota plateau — 22% quota attained — 1.1x pipeline coverage — 65% certs complete — composite 45",
  },
  {
    rep_id: "rep_007", region: "APAC",
    ramp_risk: "critical", ramp_pattern: "slow_activator",
    ramp_severity: "stalled", recommended_action: "ramp_extension_review",
    activation_score: 72.0, pipeline_health_score: 65.0,
    knowledge_score: 68.0, productivity_score: 70.0,
    ramp_composite: 69.05,
    has_ramp_gap: true, requires_ramp_coaching: true,
    estimated_ramp_cost_usd: 483350.0,
    ramp_signal: "Slow activator — 10% quota attained — 0.8x pipeline coverage — 30% certs complete — composite 69",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    ramp_risk: "critical", ramp_pattern: "slow_activator",
    ramp_severity: "stalled", recommended_action: "ramp_extension_review",
    activation_score: 100.0, pipeline_health_score: 100.0,
    knowledge_score: 100.0, productivity_score: 100.0,
    ramp_composite: 100.0,
    has_ramp_gap: true, requires_ramp_coaching: true,
    estimated_ramp_cost_usd: 750000.0,
    ramp_signal: "Slow activator — 2% quota attained — 0.4x pipeline coverage — 10% certs complete — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-rep-ramp-intelligence-engine`);
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
  let total_comp = 0, total_a = 0, total_p = 0, total_k = 0, total_pr = 0, total_cost = 0;

  for (const r of mockReps) {
    risk_counts[r.ramp_risk]             = (risk_counts[r.ramp_risk] || 0) + 1;
    pattern_counts[r.ramp_pattern]       = (pattern_counts[r.ramp_pattern] || 0) + 1;
    severity_counts[r.ramp_severity]     = (severity_counts[r.ramp_severity] || 0) + 1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.ramp_composite;
    total_a    += r.activation_score;
    total_p    += r.pipeline_health_score;
    total_k    += r.knowledge_score;
    total_pr   += r.productivity_score;
    total_cost += r.estimated_ramp_cost_usd;
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
      avg_ramp_composite:                 Math.round((total_comp / n) * 10) / 10,
      ramp_gap_count:                     mockReps.filter((r) => r.has_ramp_gap).length,
      coaching_count:                     mockReps.filter((r) => r.requires_ramp_coaching).length,
      avg_activation_score:               Math.round((total_a  / n) * 10) / 10,
      avg_pipeline_health_score:          Math.round((total_p  / n) * 10) / 10,
      avg_knowledge_score:                Math.round((total_k  / n) * 10) / 10,
      avg_productivity_score:             Math.round((total_pr / n) * 10) / 10,
      total_estimated_ramp_cost_usd:      Math.round(total_cost * 100) / 100,
    },
  });
}
