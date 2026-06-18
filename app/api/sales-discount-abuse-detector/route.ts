import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    discount_risk: "low", discount_pattern: "none",
    discount_severity: "clean", recommended_action: "no_action",
    policy_violation_score: 0.0, revenue_impact_score: 0.0,
    behavioral_pattern_score: 5.0, dependency_score: 3.0,
    discount_composite: 1.5, is_abusing_discounts: false, requires_manager_review: false,
    estimated_margin_loss_usd: 0.0,
    discount_signal: "discount behavior within policy norms",
  },
  {
    rep_id: "rep_002", region: "East",
    discount_risk: "moderate", discount_pattern: "habitual_discounting",
    discount_severity: "watch", recommended_action: "flag_for_review",
    policy_violation_score: 8.0, revenue_impact_score: 15.0,
    behavioral_pattern_score: 22.0, dependency_score: 10.0,
    discount_composite: 13.5, is_abusing_discounts: false, requires_manager_review: false,
    estimated_margin_loss_usd: 5400.0,
    discount_signal: "rep initiated discounts in 8/12 deals — composite 14",
  },
  {
    rep_id: "rep_003", region: "Central",
    discount_risk: "moderate", discount_pattern: "policy_breach",
    discount_severity: "watch", recommended_action: "manager_approval",
    policy_violation_score: 26.0, revenue_impact_score: 20.0,
    behavioral_pattern_score: 18.0, dependency_score: 12.0,
    discount_composite: 19.9, is_abusing_discounts: false, requires_manager_review: false,
    estimated_margin_loss_usd: 23880.0,
    discount_signal: "5/10 deals above policy threshold — composite 20",
  },
  {
    rep_id: "rep_004", region: "Southeast",
    discount_risk: "high", discount_pattern: "dependency_pattern",
    discount_severity: "concerning", recommended_action: "manager_approval",
    policy_violation_score: 18.0, revenue_impact_score: 28.0,
    behavioral_pattern_score: 35.0, dependency_score: 42.0,
    discount_composite: 29.1, is_abusing_discounts: false, requires_manager_review: false,
    estimated_margin_loss_usd: 58200.0,
    discount_signal: "win rate gap 72% vs 41% — 5 repeat discount customers — composite 29",
  },
  {
    rep_id: "rep_005", region: "Northeast",
    discount_risk: "high", discount_pattern: "unauthorized",
    discount_severity: "concerning", recommended_action: "discount_freeze",
    policy_violation_score: 53.0, revenue_impact_score: 32.0,
    behavioral_pattern_score: 25.0, dependency_score: 18.0,
    discount_composite: 35.5, is_abusing_discounts: false, requires_manager_review: true,
    estimated_margin_loss_usd: 106500.0,
    discount_signal: "3 unauthorized discount(s) — avg 24.5% vs policy 15.0% — composite 36",
  },
  {
    rep_id: "rep_006", region: "Northwest",
    discount_risk: "high", discount_pattern: "margin_destruction",
    discount_severity: "concerning", recommended_action: "discount_freeze",
    policy_violation_score: 35.0, revenue_impact_score: 55.0,
    behavioral_pattern_score: 30.0, dependency_score: 22.0,
    discount_composite: 38.7, is_abusing_discounts: false, requires_manager_review: true,
    estimated_margin_loss_usd: 193500.0,
    discount_signal: "avg discount 28.0% vs company avg 10.0% (+18.0pts) — composite 39",
  },
  {
    rep_id: "rep_007", region: "Southwest",
    discount_risk: "critical", discount_pattern: "unauthorized",
    discount_severity: "abusive", recommended_action: "compensation_review",
    policy_violation_score: 85.0, revenue_impact_score: 60.0,
    behavioral_pattern_score: 55.0, dependency_score: 45.0,
    discount_composite: 65.8, is_abusing_discounts: true, requires_manager_review: true,
    estimated_margin_loss_usd: 395000.0,
    discount_signal: "6 unauthorized discount(s) — avg 38.0% vs policy 15.0% — composite 66",
  },
  {
    rep_id: "rep_008", region: "Mountain",
    discount_risk: "critical", discount_pattern: "dependency_pattern",
    discount_severity: "abusive", recommended_action: "compensation_review",
    policy_violation_score: 45.0, revenue_impact_score: 70.0,
    behavioral_pattern_score: 65.0, dependency_score: 80.0,
    discount_composite: 62.3, is_abusing_discounts: true, requires_manager_review: true,
    estimated_margin_loss_usd: 498400.0,
    discount_signal: "win rate gap 88% vs 35% — 8 repeat discount customers — composite 62",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-discount-abuse-detector`);
      if (risk)    url.searchParams.set("risk",    risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.discount_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.discount_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_pol = 0, total_rev = 0, total_beh = 0, total_dep = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.discount_risk]       = (risk_counts[r.discount_risk] || 0) + 1;
    pattern_counts[r.discount_pattern] = (pattern_counts[r.discount_pattern] || 0) + 1;
    severity_counts[r.discount_severity] = (severity_counts[r.discount_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.discount_composite;
    total_pol  += r.policy_violation_score;
    total_rev  += r.revenue_impact_score;
    total_beh  += r.behavioral_pattern_score;
    total_dep  += r.dependency_score;
    total_loss += r.estimated_margin_loss_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                           n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_discount_composite:          Math.round((total_comp / n) * 10) / 10,
      abusing_count:                   mockReps.filter((r) => r.is_abusing_discounts).length,
      review_required_count:           mockReps.filter((r) => r.requires_manager_review).length,
      avg_policy_violation_score:      Math.round((total_pol  / n) * 10) / 10,
      avg_revenue_impact_score:        Math.round((total_rev  / n) * 10) / 10,
      avg_behavioral_pattern_score:    Math.round((total_beh  / n) * 10) / 10,
      avg_dependency_score:            Math.round((total_dep  / n) * 10) / 10,
      total_estimated_margin_loss_usd: Math.round(total_loss * 100) / 100,
    },
  });
}
