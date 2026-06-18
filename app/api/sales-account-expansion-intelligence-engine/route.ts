import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    expansion_risk: "low", expansion_pattern: "none",
    expansion_severity: "growing", recommended_action: "no_action",
    expansion_capture_score: 0.0, portfolio_penetration_score: 0.0,
    renewal_health_score: 0.0, executive_coverage_score: 0.0,
    account_expansion_composite: 0.0, has_expansion_gap: false,
    requires_account_review: false, estimated_expansion_revenue_upside_usd: 0.0,
    expansion_signal: "Account expansion momentum strong across portfolio",
  },
  {
    rep_id: "rep_002", region: "East",
    expansion_risk: "low", expansion_pattern: "none",
    expansion_severity: "growing", recommended_action: "no_action",
    expansion_capture_score: 8.0, portfolio_penetration_score: 5.0,
    renewal_health_score: 0.0, executive_coverage_score: 10.0,
    account_expansion_composite: 6.0, has_expansion_gap: false,
    requires_account_review: false, estimated_expansion_revenue_upside_usd: 0.0,
    expansion_signal: "Account expansion momentum strong across portfolio",
  },
  {
    rep_id: "rep_003", region: "Central",
    expansion_risk: "moderate", expansion_pattern: "executive_gap",
    expansion_severity: "steady", recommended_action: "expansion_outreach",
    expansion_capture_score: 20.0, portfolio_penetration_score: 18.0,
    renewal_health_score: 12.0, executive_coverage_score: 30.0,
    account_expansion_composite: 20.0, has_expansion_gap: false,
    requires_account_review: false, estimated_expansion_revenue_upside_usd: 12000.0,
    expansion_signal: "Executive gap — 3 untapped expansion accounts — 2 cross-sell opportunities ignored — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    expansion_risk: "moderate", expansion_pattern: "low_penetration",
    expansion_severity: "steady", recommended_action: "expansion_outreach",
    expansion_capture_score: 15.0, portfolio_penetration_score: 30.0,
    renewal_health_score: 15.0, executive_coverage_score: 20.0,
    account_expansion_composite: 20.0, has_expansion_gap: false,
    requires_account_review: false, estimated_expansion_revenue_upside_usd: 8000.0,
    expansion_signal: "Low penetration — 2 untapped expansion accounts — 4 cross-sell opportunities ignored — composite 20",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    expansion_risk: "high", expansion_pattern: "cross_sell_neglect",
    expansion_severity: "declining", recommended_action: "cross_sell_campaign",
    expansion_capture_score: 35.0, portfolio_penetration_score: 30.0,
    renewal_health_score: 25.0, executive_coverage_score: 40.0,
    account_expansion_composite: 32.0, has_expansion_gap: false,
    requires_account_review: true, estimated_expansion_revenue_upside_usd: 48000.0,
    expansion_signal: "Cross sell neglect — 5 untapped expansion accounts — 6 cross-sell opportunities ignored — composite 32",
  },
  {
    rep_id: "rep_006", region: "West",
    expansion_risk: "high", expansion_pattern: "renewal_risk",
    expansion_severity: "declining", recommended_action: "renewal_acceleration",
    expansion_capture_score: 40.0, portfolio_penetration_score: 35.0,
    renewal_health_score: 45.0, executive_coverage_score: 30.0,
    account_expansion_composite: 37.0, has_expansion_gap: false,
    requires_account_review: true, estimated_expansion_revenue_upside_usd: 75000.0,
    expansion_signal: "Renewal risk — 4 untapped expansion accounts — 3 renewals unsecured — composite 37",
  },
  {
    rep_id: "rep_007", region: "APAC",
    expansion_risk: "critical", expansion_pattern: "stagnant_portfolio",
    expansion_severity: "stagnant", recommended_action: "expansion_outreach",
    expansion_capture_score: 65.0, portfolio_penetration_score: 55.0,
    renewal_health_score: 50.0, executive_coverage_score: 55.0,
    account_expansion_composite: 57.0, has_expansion_gap: true,
    requires_account_review: true, estimated_expansion_revenue_upside_usd: 160000.0,
    expansion_signal: "Stagnant portfolio — 7 untapped expansion accounts — 5 cross-sell opportunities ignored — 4 renewals unsecured — composite 57",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    expansion_risk: "critical", expansion_pattern: "stagnant_portfolio",
    expansion_severity: "stagnant", recommended_action: "expansion_outreach",
    expansion_capture_score: 70.0, portfolio_penetration_score: 65.0,
    renewal_health_score: 65.0, executive_coverage_score: 70.0,
    account_expansion_composite: 67.0, has_expansion_gap: true,
    requires_account_review: true, estimated_expansion_revenue_upside_usd: 280000.0,
    expansion_signal: "Stagnant portfolio — 9 untapped expansion accounts — 8 cross-sell opportunities ignored — 6 renewals unsecured — composite 67",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-account-expansion-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.expansion_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.expansion_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_cap = 0, total_pen = 0, total_ren = 0, total_exe = 0, total_ups = 0;

  for (const r of mockReps) {
    risk_counts[r.expansion_risk]       = (risk_counts[r.expansion_risk] || 0) + 1;
    pattern_counts[r.expansion_pattern] = (pattern_counts[r.expansion_pattern] || 0) + 1;
    severity_counts[r.expansion_severity] = (severity_counts[r.expansion_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.account_expansion_composite;
    total_cap  += r.expansion_capture_score;
    total_pen  += r.portfolio_penetration_score;
    total_ren  += r.renewal_health_score;
    total_exe  += r.executive_coverage_score;
    total_ups  += r.estimated_expansion_revenue_upside_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                        n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_account_expansion_composite:              Math.round((total_comp / n) * 10) / 10,
      expansion_gap_count:                          mockReps.filter((r) => r.has_expansion_gap).length,
      account_review_count:                         mockReps.filter((r) => r.requires_account_review).length,
      avg_expansion_capture_score:                  Math.round((total_cap / n) * 10) / 10,
      avg_portfolio_penetration_score:              Math.round((total_pen / n) * 10) / 10,
      avg_renewal_health_score:                     Math.round((total_ren / n) * 10) / 10,
      avg_executive_coverage_score:                 Math.round((total_exe / n) * 10) / 10,
      total_estimated_expansion_revenue_upside_usd: Math.round(total_ups * 100) / 100,
    },
  });
}
