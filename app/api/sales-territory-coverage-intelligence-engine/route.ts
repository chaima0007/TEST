import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    coverage_risk: "low", coverage_pattern: "none",
    coverage_severity: "optimized", recommended_action: "no_action",
    account_breadth_score: 0.0, account_prioritization_score: 0.0,
    whitespace_exploitation_score: 0.0, churn_prevention_score: 0.0,
    territory_coverage_composite: 0.0, has_coverage_gap: false,
    requires_territory_rebalance: false, estimated_revenue_at_risk_usd: 0.0,
    coverage_signal: "Territory coverage optimized across all segments",
  },
  {
    rep_id: "rep_002", region: "East",
    coverage_risk: "low", coverage_pattern: "none",
    coverage_severity: "optimized", recommended_action: "no_action",
    account_breadth_score: 0.0, account_prioritization_score: 10.0,
    whitespace_exploitation_score: 8.0, churn_prevention_score: 0.0,
    territory_coverage_composite: 5.0, has_coverage_gap: false,
    requires_territory_rebalance: false, estimated_revenue_at_risk_usd: 0.0,
    coverage_signal: "Territory coverage optimized across all segments",
  },
  {
    rep_id: "rep_003", region: "Central",
    coverage_risk: "moderate", coverage_pattern: "whitespace_ignored",
    coverage_severity: "gaps_detected", recommended_action: "account_outreach_blitz",
    account_breadth_score: 10.0, account_prioritization_score: 10.0,
    whitespace_exploitation_score: 45.0, churn_prevention_score: 8.0,
    territory_coverage_composite: 20.0, has_coverage_gap: false,
    requires_territory_rebalance: false, estimated_revenue_at_risk_usd: 0.0,
    coverage_signal: "Whitespace ignored — 6 whitespace opportunities missed — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    coverage_risk: "moderate", coverage_pattern: "high_value_underserved",
    coverage_severity: "gaps_detected", recommended_action: "account_outreach_blitz",
    account_breadth_score: 10.0, account_prioritization_score: 35.0,
    whitespace_exploitation_score: 15.0, churn_prevention_score: 8.0,
    territory_coverage_composite: 20.0, has_coverage_gap: false,
    requires_territory_rebalance: true, estimated_revenue_at_risk_usd: 0.0,
    coverage_signal: "High value underserved — 45% high-value coverage — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    coverage_risk: "high", coverage_pattern: "account_neglect",
    coverage_severity: "underserved", recommended_action: "account_outreach_blitz",
    account_breadth_score: 50.0, account_prioritization_score: 25.0,
    whitespace_exploitation_score: 30.0, churn_prevention_score: 23.0,
    territory_coverage_composite: 33.0, has_coverage_gap: true,
    requires_territory_rebalance: true, estimated_revenue_at_risk_usd: 24000.0,
    coverage_signal: "Account neglect — 8 accounts neglected — 55% high-value coverage — composite 42",
  },
  {
    rep_id: "rep_006", region: "West",
    coverage_risk: "high", coverage_pattern: "churn_risk_uncovered",
    coverage_severity: "underserved", recommended_action: "churn_prevention_sprint",
    account_breadth_score: 25.0, account_prioritization_score: 15.0,
    whitespace_exploitation_score: 30.0, churn_prevention_score: 58.0,
    territory_coverage_composite: 32.0, has_coverage_gap: true,
    requires_territory_rebalance: true, estimated_revenue_at_risk_usd: 30000.0,
    coverage_signal: "Churn risk uncovered — 5 accounts neglected — 30% churn risk contacts — composite 44",
  },
  {
    rep_id: "rep_007", region: "APAC",
    coverage_risk: "critical", coverage_pattern: "revenue_concentration",
    coverage_severity: "critical", recommended_action: "territory_restructure",
    account_breadth_score: 55.0, account_prioritization_score: 65.0,
    whitespace_exploitation_score: 55.0, churn_prevention_score: 55.0,
    territory_coverage_composite: 58.5, has_coverage_gap: true,
    requires_territory_rebalance: true, estimated_revenue_at_risk_usd: 78000.0,
    coverage_signal: "Revenue concentration — 12 accounts neglected — 30% high-value coverage — 8 whitespace opportunities missed — composite 62",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    coverage_risk: "critical", coverage_pattern: "revenue_concentration",
    coverage_severity: "critical", recommended_action: "territory_restructure",
    account_breadth_score: 75.0, account_prioritization_score: 85.0,
    whitespace_exploitation_score: 65.0, churn_prevention_score: 70.0,
    territory_coverage_composite: 75.0, has_coverage_gap: true,
    requires_territory_rebalance: true, estimated_revenue_at_risk_usd: 150000.0,
    coverage_signal: "Revenue concentration — 15 accounts neglected — 20% high-value coverage — 10 whitespace opportunities missed — 20% churn risk contacts — composite 75",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-territory-coverage-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.coverage_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.coverage_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_br = 0, total_pr = 0, total_ws = 0, total_ch = 0, total_rev = 0;

  for (const r of mockReps) {
    risk_counts[r.coverage_risk]         = (risk_counts[r.coverage_risk] || 0) + 1;
    pattern_counts[r.coverage_pattern]   = (pattern_counts[r.coverage_pattern] || 0) + 1;
    severity_counts[r.coverage_severity] = (severity_counts[r.coverage_severity] || 0) + 1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.territory_coverage_composite;
    total_br   += r.account_breadth_score;
    total_pr   += r.account_prioritization_score;
    total_ws   += r.whitespace_exploitation_score;
    total_ch   += r.churn_prevention_score;
    total_rev  += r.estimated_revenue_at_risk_usd;
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
      avg_territory_coverage_composite:     Math.round((total_comp / n) * 10) / 10,
      coverage_gap_count:                   mockReps.filter((r) => r.has_coverage_gap).length,
      rebalance_count:                      mockReps.filter((r) => r.requires_territory_rebalance).length,
      avg_account_breadth_score:            Math.round((total_br / n) * 10) / 10,
      avg_account_prioritization_score:     Math.round((total_pr / n) * 10) / 10,
      avg_whitespace_exploitation_score:    Math.round((total_ws / n) * 10) / 10,
      avg_churn_prevention_score:           Math.round((total_ch / n) * 10) / 10,
      total_estimated_revenue_at_risk_usd:  Math.round(total_rev * 100) / 100,
    },
  });
}
