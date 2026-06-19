import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    penetration_risk: "low", penetration_pattern: "none",
    penetration_severity: "optimal", recommended_action: "no_action",
    account_coverage_score: 0.0, account_depth_score: 0.0,
    strategic_focus_score: 0.0, expansion_momentum_score: 0.0,
    account_penetration_composite: 0.0,
    has_penetration_gap: false, requires_account_coaching: false,
    estimated_untapped_revenue_usd: 0.0,
    penetration_signal: "Account penetration and territory coverage within healthy benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    penetration_risk: "low", penetration_pattern: "none",
    penetration_severity: "optimal", recommended_action: "no_action",
    account_coverage_score: 5.0, account_depth_score: 4.0,
    strategic_focus_score: 3.0, expansion_momentum_score: 5.0,
    account_penetration_composite: 4.3,
    has_penetration_gap: false, requires_account_coaching: false,
    estimated_untapped_revenue_usd: 0.0,
    penetration_signal: "Account penetration and territory coverage within healthy benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    penetration_risk: "moderate", penetration_pattern: "expansion_stagnation",
    penetration_severity: "developing", recommended_action: "account_prioritization_review",
    account_coverage_score: 8.0, account_depth_score: 15.0,
    strategic_focus_score: 18.0, expansion_momentum_score: 30.0,
    account_penetration_composite: 16.35,
    has_penetration_gap: false, requires_account_coaching: false,
    estimated_untapped_revenue_usd: 14400.0,
    penetration_signal: "Expansion stagnation — 4 inactive accounts — 6 whitespace accounts — composite 16",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    penetration_risk: "moderate", penetration_pattern: "shallow_coverage",
    penetration_severity: "developing", recommended_action: "account_prioritization_review",
    account_coverage_score: 20.0, account_depth_score: 38.0,
    strategic_focus_score: 12.0, expansion_momentum_score: 18.0,
    account_penetration_composite: 22.65,
    has_penetration_gap: false, requires_account_coaching: false,
    estimated_untapped_revenue_usd: 27000.0,
    penetration_signal: "Shallow coverage — 6 inactive accounts — 9 whitespace accounts — composite 23",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    penetration_risk: "high", penetration_pattern: "cherry_picking",
    penetration_severity: "shallow", recommended_action: "territory_coverage_coaching",
    account_coverage_score: 28.0, account_depth_score: 30.0,
    strategic_focus_score: 38.0, expansion_momentum_score: 20.0,
    account_penetration_composite: 29.75,
    has_penetration_gap: false, requires_account_coaching: true,
    estimated_untapped_revenue_usd: 54000.0,
    penetration_signal: "Cherry picking — 9 inactive accounts — 12 whitespace accounts — 4 large accounts ignored — composite 30",
  },
  {
    rep_id: "rep_006", region: "West",
    penetration_risk: "high", penetration_pattern: "churn_risk_blindness",
    penetration_severity: "shallow", recommended_action: "expansion_pipeline_build",
    account_coverage_score: 25.0, account_depth_score: 35.0,
    strategic_focus_score: 22.0, expansion_momentum_score: 40.0,
    account_penetration_composite: 30.55,
    has_penetration_gap: true, requires_account_coaching: true,
    estimated_untapped_revenue_usd: 81000.0,
    penetration_signal: "Churn risk blindness — 10 inactive accounts — 15 whitespace accounts — 3 renewals at risk — composite 31",
  },
  {
    rep_id: "rep_007", region: "APAC",
    penetration_risk: "critical", penetration_pattern: "whitespace_neglect",
    penetration_severity: "stagnant", recommended_action: "executive_engagement_program",
    account_coverage_score: 58.0, account_depth_score: 62.0,
    strategic_focus_score: 55.0, expansion_momentum_score: 50.0,
    account_penetration_composite: 57.35,
    has_penetration_gap: true, requires_account_coaching: true,
    estimated_untapped_revenue_usd: 270000.0,
    penetration_signal: "Whitespace neglect — 22 inactive accounts — 30 whitespace accounts — 8 large accounts ignored — composite 57",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    penetration_risk: "critical", penetration_pattern: "cherry_picking",
    penetration_severity: "stagnant", recommended_action: "strategic_account_planning",
    account_coverage_score: 75.0, account_depth_score: 68.0,
    strategic_focus_score: 72.0, expansion_momentum_score: 65.0,
    account_penetration_composite: 70.95,
    has_penetration_gap: true, requires_account_coaching: true,
    estimated_untapped_revenue_usd: 540000.0,
    penetration_signal: "Cherry picking — 28 inactive accounts — 36 whitespace accounts — 12 large accounts ignored — composite 71",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-account-penetration-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.penetration_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.penetration_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_cov = 0, total_dep = 0, total_str = 0, total_exp = 0, total_unt = 0;

  for (const r of mockReps) {
    risk_counts[r.penetration_risk]       = (risk_counts[r.penetration_risk] || 0) + 1;
    pattern_counts[r.penetration_pattern] = (pattern_counts[r.penetration_pattern] || 0) + 1;
    severity_counts[r.penetration_severity] = (severity_counts[r.penetration_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.account_penetration_composite;
    total_cov  += r.account_coverage_score;
    total_dep  += r.account_depth_score;
    total_str  += r.strategic_focus_score;
    total_exp  += r.expansion_momentum_score;
    total_unt  += r.estimated_untapped_revenue_usd;
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
      avg_account_penetration_composite:      Math.round((total_comp / n) * 10) / 10,
      penetration_gap_count:                  mockReps.filter((r) => r.has_penetration_gap).length,
      account_coaching_count:                 mockReps.filter((r) => r.requires_account_coaching).length,
      avg_account_coverage_score:             Math.round((total_cov / n) * 10) / 10,
      avg_account_depth_score:                Math.round((total_dep / n) * 10) / 10,
      avg_strategic_focus_score:              Math.round((total_str / n) * 10) / 10,
      avg_expansion_momentum_score:           Math.round((total_exp / n) * 10) / 10,
      total_estimated_untapped_revenue_usd:   Math.round(total_unt * 100) / 100,
    },
  });
}
